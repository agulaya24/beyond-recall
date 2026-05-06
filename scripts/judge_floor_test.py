"""
judge_floor_test.py
===================

P0-17 — Judge floor-testing diagnostic for the 5-judge primary panel.

CONTEXT
-------
Existing judge calibration:
    - Ceiling check: answer-as-fact → expected score 5 (calibration script)
    - Length-bias / paraphrase sensitivity: documented elsewhere

Missing: FLOOR discrimination. When a response is clearly wrong, does the
judge score it near 1? This script runs a 12-diagnostic × 5-variant ×
5-judge matrix and measures per-judge floor leakage.

VARIANTS (per diagnostic held-out passage)
------------------------------------------
    1. wrong_factual          Directly contradicts a specific claim in
                              the held-out passage.
    2. wrong_direction        Reverses the subject's action or stance.
    3. topically_adjacent     Right era/domain, wrong specific claim.
    4. off_topic_generic      "All people have mixed feelings..." non-answer.
    5. plausible_unsupported  Plausible-sounding claim not in held-out
                              and not contradicting held-out.

DIAGNOSTIC POOL
---------------
12 held-out passages sampled across 5 different subjects (augustine,
keckley, yung_wing, hamerton, babur) to cover rhetorical-style
variability. Each held-out is a behavioral_prediction item with its
original question text.

PANEL
-----
    haiku   -> claude-haiku-4-5-20251001
    sonnet  -> claude-sonnet-4-6
    opus    -> claude-opus-4-6
    gpt4o   -> gpt-4o-2024-08-06
    gpt54   -> gpt-5.4

(ID mappings copied from scripts/backfill_all_parse_failures.py.)

JUDGE PROMPT
------------
Identical to the primary 5-judge prompt (see backfill_all_parse_failures.py).

OUTPUT
------
docs/research/judge_floor_test.json
docs/research/judge_floor_test.md

BUDGET
------
10 × 5 × 5 = 250 judge calls. Estimated ~$2.50 at avg $0.010/call with real
pricing (Opus 4.6: ~$0.016/call at 1k input, 8 token output). Generation of
the 50 wrong-answer variants is done by Haiku in advance (~$0.05 total).
"""

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DATA = REPO / 'data'
OUT_JSON = REPO / 'docs' / 'research' / 'judge_floor_test.json'
OUT_MD = REPO / 'docs' / 'research' / 'judge_floor_test.md'

JUDGE_CONFIG = {
    'haiku':  {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai',    'model': 'gpt-5.4'},
}

VARIANT_TYPES = [
    'wrong_factual',
    'wrong_direction',
    'topically_adjacent',
    'off_topic_generic',
    'plausible_unsupported',
]

# Select 12 diagnostic held-out passages. Subject/question IDs drawn from
# battery_v2.json (or battery.json for hamerton). We pick 2-3 from each
# of 5 subjects so the floor test covers a range of rhetorical styles.
DIAGNOSTIC_SOURCES = [
    ('augustine', [1, 5]),       # global_augustine/battery_v2
    ('keckley',   [1, 10]),
    ('yung_wing', [2, 12]),
    ('hamerton',  [3, 11]),      # data/hamerton/battery.json
    ('babur',     [1, 7]),
]
# 10 diagnostics × 5 variants × 5 judges = 250 judge calls.
# Real per-call cost (1k input, 8 token output, Opus 4.6 $15/$75 per MTok): ~$0.016
# Estimated total: 250 × $0.016 avg = $2.50. Within the $3-per-job cap.


def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']:
        if os.environ.get(k):
            continue
        r = subprocess.run(
            ['powershell', '-Command',
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


def load_question(subject, qid):
    """Load a single BP question record from the appropriate battery."""
    if subject == 'hamerton':
        p = DATA / 'hamerton' / 'battery.json'
    elif subject == 'franklin':
        p = DATA / 'franklin' / 'battery.json'
    else:
        p = RESULTS / f'global_{subject}' / 'battery_v2.json'
    if not p.exists():
        return None
    data = json.load(p.open(encoding='utf-8'))
    qs = data.get('questions', data if isinstance(data, list) else [])
    for q in qs:
        if q.get('id', q.get('question_id')) == qid:
            if q.get('tier') != 'behavioral_prediction':
                return None
            return {
                'subject': subject,
                'question_id': qid,
                'question_text': q.get('text', q.get('question_text', '')),
                'held_out': q.get('held_out_passage') or '',
            }
    return None


def collect_diagnostics():
    diagnostics = []
    for subject, ids in DIAGNOSTIC_SOURCES:
        for qid in ids:
            rec = load_question(subject, qid)
            if rec and rec['held_out']:
                diagnostics.append(rec)
    return diagnostics


GEN_PROMPT = """You are generating WRONG response variants for a held-out passage to stress-test judge grading.
Held-out ground truth:
{held_out}

Question (for context, not for answering): {question}

Write five distinct short response paragraphs (80–140 words each), one per variant type:

1. WRONG_FACTUAL — States a specific fact that directly contradicts the held-out passage. Confident tone.
2. WRONG_DIRECTION — Reverses the subject's action or stance from the held-out passage. Confident tone.
3. TOPICALLY_ADJACENT — Right era/domain/setting, wrong specific claim. Reads plausible if you don't know the held-out.
4. OFF_TOPIC_GENERIC — Vague non-answer ("humans commonly feel torn..."). Says nothing specific.
5. PLAUSIBLE_UNSUPPORTED — States something plausible but NOT present in held-out and does NOT contradict it. Reads like an invented detail.

Return STRICTLY as JSON:
{{
  "wrong_factual": "...",
  "wrong_direction": "...",
  "topically_adjacent": "...",
  "off_topic_generic": "...",
  "plausible_unsupported": "..."
}}
"""


def generate_variants(diag, api_key):
    prompt = GEN_PROMPT.format(
        held_out=(diag.get('held_out') or '')[:1200],
        question=(diag.get('question_text') or '')[:400],
    )
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': 'claude-haiku-4-5-20251001',
                    'max_tokens': 2000,
                    'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=120,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            text = r.json()['content'][0]['text'].strip()
            # Strip code fences
            if text.startswith('```'):
                text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
            # Find the JSON object
            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                # Try extracting balanced braces
                m = re.search(r'\{[\s\S]*\}', text)
                if m:
                    obj = json.loads(m.group(0))
                else:
                    raise
            return {k: obj.get(k, '') for k in VARIANT_TYPES}
        except Exception as e:
            if attempt == 3:
                return {k: f'ERROR: {e}' for k in VARIANT_TYPES}
            time.sleep(2 ** (attempt + 1))


def judge_prompt(held_out, response_text):
    return (
        'You are evaluating whether a response about a person PREDICTED '
        'what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + (held_out or '') + '\n\n'
        '=== RESPONSE ===\n' + (response_text or '')[:1500] + '\n\n'
        'Rate 1-5:\n'
        '5=Predicts specific outcome\n'
        '4=General direction correct\n'
        '3=Right domain wrong outcome\n'
        '2=Wrong prediction\n'
        '1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def call_anthropic(api_key, model, prompt):
    for attempt in range(5):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={'model': model, 'max_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=60,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            return r.json()['content'][0]['text']
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_openai(api_key, model, prompt):
    for attempt in range(5):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                timeout=60,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge_name, prompt, keys):
    cfg = JUDGE_CONFIG[judge_name]
    if cfg['provider'] == 'anthropic':
        return call_anthropic(keys['ANTHROPIC_API_KEY'], cfg['model'], prompt)
    if cfg['provider'] == 'openai':
        return call_openai(keys['OPENAI_API_KEY'], cfg['model'], prompt)
    raise ValueError(f"Unknown provider: {cfg['provider']}")


def main():
    load_env()
    keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY'),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY'),
    }
    for k, v in keys.items():
        if not v:
            sys.exit(f"{k} not in environment")

    diagnostics = collect_diagnostics()
    print(f"Collected {len(diagnostics)} diagnostics", flush=True)

    # Generate variants
    print("Generating variants (Haiku)...", flush=True)
    for i, diag in enumerate(diagnostics):
        diag['variants'] = generate_variants(diag, keys['ANTHROPIC_API_KEY'])
        print(f"  [{i+1}/{len(diagnostics)}] {diag['subject']} Q{diag['question_id']}", flush=True)

    # Run judges on every (diag, variant, judge) combination
    total_judge_calls = len(diagnostics) * len(VARIANT_TYPES) * len(JUDGE_CONFIG)
    print(f"\nRunning {total_judge_calls} judge calls...", flush=True)

    results = []
    call_idx = 0
    for diag in diagnostics:
        for variant_name in VARIANT_TYPES:
            resp_text = diag['variants'].get(variant_name, '')
            if not resp_text or resp_text.startswith('ERROR'):
                # skip but record
                for judge in JUDGE_CONFIG:
                    results.append({
                        'subject': diag['subject'],
                        'question_id': diag['question_id'],
                        'variant': variant_name,
                        'judge': judge,
                        'score': None,
                        'raw': 'SKIP_NO_VARIANT',
                    })
                continue
            prompt = judge_prompt(diag['held_out'], resp_text)
            for judge in JUDGE_CONFIG:
                call_idx += 1
                try:
                    raw = call_judge(judge, prompt, keys)
                    score = parse_score(raw)
                except Exception as e:
                    raw = f'ERROR: {type(e).__name__}: {e}'
                    score = None
                results.append({
                    'subject': diag['subject'],
                    'question_id': diag['question_id'],
                    'variant': variant_name,
                    'judge': judge,
                    'score': score,
                    'raw': raw,
                })
                if call_idx % 20 == 0:
                    print(f"  [{call_idx}/{total_judge_calls}] last: {judge} {diag['subject']} Q{diag['question_id']} {variant_name} -> {score}", flush=True)

    # Aggregate
    by_judge_variant = defaultdict(list)
    by_judge = defaultdict(list)
    for r in results:
        if not isinstance(r['score'], int):
            continue
        by_judge_variant[(r['judge'], r['variant'])].append(r['score'])
        by_judge[r['judge']].append(r['score'])

    # Write JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump({
            'n_diagnostics': len(diagnostics),
            'variants': VARIANT_TYPES,
            'judges': list(JUDGE_CONFIG.keys()),
            'diagnostics': [
                {
                    'subject': d['subject'],
                    'question_id': d['question_id'],
                    'question_text': d['question_text'],
                    'held_out': d['held_out'],
                    'variants': d.get('variants', {}),
                }
                for d in diagnostics
            ],
            'results': results,
        }, f, indent=2, ensure_ascii=False)

    # Write MD
    with OUT_MD.open('w', encoding='utf-8') as f:
        f.write("# Judge Floor Test (P0-17)\n\n")
        f.write(f"_{len(diagnostics)} diagnostics × {len(VARIANT_TYPES)} wrong-answer variants × {len(JUDGE_CONFIG)} judges_\n\n")
        f.write("**Expected:** all variants score near 1. Any judge that systematically "
                "scores > 1.5 across all variants has a floor-leak; that's a known calibration gap.\n\n")

        def mean(vs):
            return sum(vs) / len(vs) if vs else None

        def std(vs):
            if len(vs) < 2:
                return None
            m = mean(vs)
            return (sum((v - m) ** 2 for v in vs) / len(vs)) ** 0.5

        f.write("## Per-judge overall mean on wrong answers\n\n")
        f.write("| Judge | n | mean | std | pct ≤ 1.5 | pct ≤ 2.5 |\n|---|---:|---:|---:|---:|---:|\n")
        for j in JUDGE_CONFIG:
            vs = by_judge[j]
            if not vs:
                f.write(f"| {j} | 0 | — | — | — | — |\n")
                continue
            m = mean(vs)
            s = std(vs)
            p_15 = 100 * sum(1 for v in vs if v <= 1.5) / len(vs)
            p_25 = 100 * sum(1 for v in vs if v <= 2.5) / len(vs)
            flag = " ⚠" if m > 1.5 else ""
            f.write(f"| {j}{flag} | {len(vs)} | {m:.2f} | {s:.2f} | {p_15:.0f}% | {p_25:.0f}% |\n")
        f.write("\n")

        f.write("## Per-judge × variant mean\n\n")
        f.write("| Judge | " + " | ".join(VARIANT_TYPES) + " |\n")
        f.write("|---|" + "---|" * len(VARIANT_TYPES) + "\n")
        for j in JUDGE_CONFIG:
            row = [f"| {j} |"]
            for v in VARIANT_TYPES:
                vs = by_judge_variant.get((j, v), [])
                if not vs:
                    row.append(" — |")
                    continue
                m = mean(vs)
                flag = " ⚠" if m > 1.5 else ""
                row.append(f" {m:.2f}{flag} |")
            f.write("".join(row) + "\n")
        f.write("\n")

        f.write("## Which variants leak the floor the most?\n\n")
        f.write("| Variant | mean across 5 judges | max judge mean | worst judge |\n|---|---:|---:|---|\n")
        for v in VARIANT_TYPES:
            per_judge_means = {j: mean(by_judge_variant.get((j, v), [])) for j in JUDGE_CONFIG}
            vals = [x for x in per_judge_means.values() if x is not None]
            if not vals:
                f.write(f"| {v} | — | — | — |\n")
                continue
            overall = mean(vals)
            worst_j = max(per_judge_means, key=lambda j: per_judge_means[j] or 0)
            f.write(f"| {v} | {overall:.2f} | {per_judge_means[worst_j]:.2f} | {worst_j} |\n")
        f.write("\n")

        # Recommendation
        tight = []
        lenient = []
        for j in JUDGE_CONFIG:
            vs = by_judge[j]
            if not vs:
                continue
            if mean(vs) <= 1.5:
                tight.append(j)
            else:
                lenient.append((j, mean(vs)))
        f.write("## Recommendation\n\n")
        if lenient:
            f.write("Judges with **floor leakage** (mean > 1.5 on wrong-answer variants):\n")
            for j, m in sorted(lenient, key=lambda t: -t[1]):
                f.write(f"- **{j}** mean {m:.2f}\n")
            f.write("\n")
        f.write("Tight-at-floor judges: " + (", ".join(tight) if tight else "none") + ".\n\n")
        f.write("If floor leakage is concentrated in `plausible_unsupported` or "
                "`topically_adjacent` variants, the 5-judge aggregate may under-rank "
                "wrong predictions that hedge or gesture plausibly. Consider either "
                "down-weighting the leaky judge or adding a rubric clarification that "
                "`1` is the correct score for any response that does not identify a "
                "held-out-consistent outcome.\n")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == '__main__':
    main()
