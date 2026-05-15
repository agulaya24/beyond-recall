"""Per-judge ablation on the highest-divergence cells from
`docs/research/published_rubric_robustness_check_20260508.{md,csv}`.

Goal. The prior robustness check found Spearman rho = 0.389 between the
original-prompt rubric ("outcome prediction" wording) and the paper rubric
("behavioral pattern" wording) across 25 stratified cells. This script
isolates whether that divergence is:
  (a) judge-specific (one judge mis-applies one rubric and drives it), or
  (b) rubric-specific (all 5 judges show the same cross-rubric pattern).

Design. Pick the 5 (subject, condition, qid) cells with largest |delta| from
the prior CSV, then for each cell call all 5 primary judges with BOTH
rubrics: 5 cells * 5 judges * 2 rubrics = 50 calls. Both rubrics run fresh
in the same execution at temperature 0 with identical held-out + response
inputs.

Selected cells:
  1. global_equiano   C5_baseline q13  (delta = -3.20)
  2. global_babur     C4a         q2   (delta = -2.60)
  3. global_equiano   C4a         q27  (delta = -2.20)
  4. global_yung_wing C2a         q2   (delta = +1.20) -- opposite sign
  5. global_yung_wing C8          q14  (delta = -0.60) -- raw-corpus diversity

Outputs:
  - results/_per_judge_ablation_20260508/<cell>_<judge>_<rubric>.json (50 raw responses)
  - docs/research/published_rubric_per_judge_ablation_20260508.csv (50 rows: cell x judge x rubric)
  - docs/research/published_rubric_per_judge_ablation_20260508.md (synthesis)

Spend cap: $5. Reproducibility: temperature=0, identical inputs across rubrics.
"""
from __future__ import annotations

import csv
import json
import os
import re
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DOCS = REPO / 'docs'
OUT_DIR = RESULTS / '_per_judge_ablation_20260508'
OUT_DIR.mkdir(parents=True, exist_ok=True)
SYNTH_CSV = DOCS / 'research' / 'published_rubric_per_judge_ablation_20260508.csv'
SYNTH_MD = DOCS / 'research' / 'published_rubric_per_judge_ablation_20260508.md'

PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

JUDGE_SPEC = {
    'haiku':  {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai',    'model': 'gpt-5.4'},
}

# ----------------------------------------------------------------------------
# 5 selected cells (top |delta| from prior 25-cell CSV)
# ----------------------------------------------------------------------------
SELECTED_CELLS = [
    {'subject': 'global_equiano',   'paper_cond': 'C5_baseline', 'raw_cond_label': 'C5_baseline',                  'qid': 13, 'prior_delta': -3.20},
    {'subject': 'global_babur',     'paper_cond': 'C4a',         'raw_cond_label': 'C4a_full_facts_plus_spec',     'qid': 2,  'prior_delta': -2.60},
    {'subject': 'global_equiano',   'paper_cond': 'C4a',         'raw_cond_label': 'C4a_full_facts_plus_spec',     'qid': 27, 'prior_delta': -2.20},
    {'subject': 'global_yung_wing', 'paper_cond': 'C2a',         'raw_cond_label': 'C2a_full_spec',                'qid': 2,  'prior_delta': +1.20},
    {'subject': 'global_yung_wing', 'paper_cond': 'C8',          'raw_cond_label': 'C8_raw_corpus',                'qid': 14, 'prior_delta': -0.60},
]


# ----------------------------------------------------------------------------
# Rubric prompts (verbatim from the prior robustness script + judge_hamerton_5judge.py)
# ----------------------------------------------------------------------------
def paper_rubric_prompt(held_out: str, response_text: str) -> str:
    return (
        'You are evaluating a response about a person against a verbatim '
        'held-out ground-truth passage from the source corpus.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + (held_out or '').strip() + '\n\n'
        '=== RESPONSE ===\n' + (response_text or '').strip()[:1500] + '\n\n'
        'Score the response on the following 1-5 rubric (this is the paper '
        '§3.3 rubric, applied verbatim):\n\n'
        '1 | Refusal or off-base prediction\n'
        '2 | Generic, not subject-specific\n'
        '3 | Partially captures the subject\'s behavioral pattern\n'
        '4 | Substantively captures the pattern on multiple dimensions\n'
        '5 | Captures the behavioral pattern observable in the verbatim '
        'held-out ground-truth passage\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def original_rubric_prompt(held_out: str, response_text: str) -> str:
    """Verbatim from scripts/judge_hamerton_5judge.py lines 57-68."""
    return (
        'You are evaluating whether a response about a person PREDICTED '
        'what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + (held_out or '').strip() + '\n\n'
        '=== RESPONSE ===\n' + (response_text or '').strip()[:1500] + '\n\n'
        'Rate 1-5:\n'
        '5=Predicts specific outcome\n'
        '4=General direction correct\n'
        '3=Right domain wrong outcome\n'
        '2=Wrong prediction\n'
        '1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


RUBRICS = {
    'paper': paper_rubric_prompt,
    'original': original_rubric_prompt,
}


# ----------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------
def load_jsonl_array(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def find_response(subject: str, qid: int, raw_cond: str):
    """Return {response_text, held_out, question_text, source_file} for the cell."""
    sd = RESULTS / subject
    for fname in ['results.json', 'baselayer_results.json', 'c8_c9_results.json',
                  'fullstack_haiku.json', 'results_v2.json']:
        d = load_jsonl_array(sd / fname)
        if not d:
            continue
        for r in d:
            if r.get('question_id') != qid:
                continue
            ho = r.get('held_out_passage')
            if not ho:
                continue
            resps = r.get('responses', {})
            if raw_cond not in resps:
                continue
            rec = resps[raw_cond]
            text = rec.get('text', '') if isinstance(rec, dict) else (rec or '')
            if text and len(text.strip()) > 50:
                return {
                    'response_text': text,
                    'held_out': ho,
                    'question_text': r.get('question_text', ''),
                    'source_file': fname,
                }
    return None


# ----------------------------------------------------------------------------
# API calls
# ----------------------------------------------------------------------------
def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']:
        if os.environ.get(k):
            continue
        r = subprocess.run(
            ['powershell', '-Command',
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = (r.stdout or '').strip()
        if val:
            os.environ[k] = val


def parse_score(text: str) -> Optional[int]:
    if not text:
        return None
    m = re.search(r'[1-5]', str(text).strip())
    return int(m.group()) if m else None


def call_anthropic(api_key, model, prompt, max_tokens=8):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': model, 'max_tokens': max_tokens, 'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={
                    'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()['content'][0]['text']
        except Exception:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_openai(api_key, model, prompt, max_tokens=8):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={
                    'model': model, 'max_completion_tokens': max_tokens,
                    'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge: str, prompt: str, anth_key: str, oai_key: str) -> str:
    spec = JUDGE_SPEC[judge]
    if spec['provider'] == 'anthropic':
        return call_anthropic(anth_key, spec['model'], prompt)
    return call_openai(oai_key, spec['model'], prompt)


def out_path(cell, judge, rubric):
    return OUT_DIR / f'{cell["subject"]}__{cell["paper_cond"]}__q{cell["qid"]}__{judge}__{rubric}.json'


# ----------------------------------------------------------------------------
# Failure-mode classification
# ----------------------------------------------------------------------------
REFUSAL_MARKERS = (
    "i cannot", "i can't", "i'm not able", "i am not able",
    "i don't have", "i do not have",
    "without more", "without specific", "without additional",
    "as an ai", "i'm an ai", "i am an ai",
    "i'm sorry", "i apologize", "unfortunately, i",
    "there isn't enough", "there's not enough",
    "insufficient information", "insufficient context",
    "i would need", "i'd need",
    "i cannot predict", "i can't predict",
    "based on the limited",
)


def classify_response_type(response_text: str) -> str:
    """Classify the response itself (independent of judges)."""
    t = (response_text or '').strip().lower()
    head = t[:300]
    if any(marker in head for marker in REFUSAL_MARKERS):
        return 'refusal'
    if len(t) < 200:
        return 'short'
    # Generic-spec heuristic: heavy use of generic personality language
    generic_markers = ['someone who', 'a person who', 'an individual who', 'this person would likely',
                       'they would likely', 'might', 'could', 'tends to']
    hits = sum(1 for m in generic_markers if m in t[:1500])
    if hits >= 5:
        return 'generic_spec'
    return 'substantive'


def classify_divergence(orig_score, paper_score, response_type) -> str:
    """Classify a (judge, cell) cross-rubric divergence."""
    if orig_score is None or paper_score is None:
        return 'parse_failure'
    diff = abs(orig_score - paper_score)
    if diff <= 0.5:
        return 'no_divergence'
    # Substantial divergence: orig_score - paper_score > 0 means orig was higher
    if response_type == 'refusal' and orig_score >= 4 and paper_score <= 2:
        return 'polite_refusal_as_engagement'
    if response_type == 'generic_spec' and orig_score >= 4 and paper_score <= 2:
        return 'generic_spec_as_pattern'
    if response_type == 'substantive' and orig_score <= 2 and paper_score >= 3:
        return 'substantive_underscored_by_original'
    return 'other'


# ----------------------------------------------------------------------------
# Main flow
# ----------------------------------------------------------------------------
def run_calls():
    load_env()
    anth_key = os.environ.get('ANTHROPIC_API_KEY')
    oai_key = os.environ.get('OPENAI_API_KEY')
    if not anth_key:
        print('FATAL: ANTHROPIC_API_KEY missing'); sys.exit(1)
    if not oai_key:
        print('FATAL: OPENAI_API_KEY missing'); sys.exit(1)

    # Load all responses + held-out passages first
    enriched = []
    for cell in SELECTED_CELLS:
        resp = find_response(cell['subject'], cell['qid'], cell['raw_cond_label'])
        if not resp:
            print(f'FATAL: no response found for {cell}')
            sys.exit(1)
        c = dict(cell)
        c.update(resp)
        c['response_type'] = classify_response_type(resp['response_text'])
        enriched.append(c)
        print(f'Loaded {c["subject"]} {c["paper_cond"]} q{c["qid"]}: '
              f'response_type={c["response_type"]}, len={len(resp["response_text"])}')
    print()

    total = len(enriched) * len(PRIMARY_JUDGES) * len(RUBRICS)
    done = 0
    new_calls = 0
    records = []

    for cell in enriched:
        for rubric_name, rubric_fn in RUBRICS.items():
            prompt = rubric_fn(cell['held_out'], cell['response_text'])
            for judge in PRIMARY_JUDGES:
                outp = out_path(cell, judge, rubric_name)
                if outp.exists():
                    rec = json.loads(outp.read_text(encoding='utf-8'))
                    done += 1
                    records.append(rec)
                    print(f'[{done}/{total}] cached: {cell["subject"]}/{cell["paper_cond"]}/q{cell["qid"]}/{judge}/{rubric_name} -> {rec.get("score")}')
                    continue
                try:
                    raw = call_judge(judge, prompt, anth_key, oai_key)
                    score = parse_score(raw)
                except Exception as e:
                    raw = f'ERROR: {e}'
                    score = None
                rec = {
                    'subject': cell['subject'],
                    'paper_cond': cell['paper_cond'],
                    'raw_cond_label': cell['raw_cond_label'],
                    'qid': cell['qid'],
                    'judge': judge,
                    'rubric': rubric_name,
                    'score': score,
                    'raw': str(raw)[:200],
                    'parse_failure': score is None,
                    'response_type': cell['response_type'],
                    'response_text': cell['response_text'][:1500],
                    'held_out': cell['held_out'],
                    'question_text': cell.get('question_text', ''),
                    'prior_delta': cell['prior_delta'],
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                }
                outp.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding='utf-8')
                records.append(rec)
                done += 1
                new_calls += 1
                print(f'[{done}/{total}] {cell["subject"]}/{cell["paper_cond"]}/q{cell["qid"]}/{judge}/{rubric_name} -> {score}')
    print(f'\nTotal records: {len(records)}; new API calls: {new_calls}\n')
    return enriched, records


# ----------------------------------------------------------------------------
# Aggregation + analysis
# ----------------------------------------------------------------------------
def write_csv(records):
    """Write 50-row CSV: one row per (cell, judge, rubric)."""
    fieldnames = ['subject', 'paper_cond', 'qid', 'judge', 'rubric', 'score',
                  'response_type', 'parse_failure', 'prior_delta']
    SYNTH_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNTH_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in sorted(records, key=lambda x: (x['subject'], x['paper_cond'], x['qid'], x['judge'], x['rubric'])):
            w.writerow({k: r.get(k) for k in fieldnames})
    print(f'CSV written: {SYNTH_CSV} ({len(records)} rows)')


def aggregate(enriched, records):
    """Aggregate per-judge cross-rubric drift and per-cell-per-judge deltas."""
    # Index records: (subject, paper_cond, qid, judge, rubric) -> score
    idx = {}
    for r in records:
        key = (r['subject'], r['paper_cond'], r['qid'], r['judge'], r['rubric'])
        idx[key] = r['score']

    # Per-(cell, judge) cross-rubric deltas
    per_cell_judge = []  # rows for table
    for cell in enriched:
        for judge in PRIMARY_JUDGES:
            orig = idx.get((cell['subject'], cell['paper_cond'], cell['qid'], judge, 'original'))
            paper = idx.get((cell['subject'], cell['paper_cond'], cell['qid'], judge, 'paper'))
            delta = (paper - orig) if (orig is not None and paper is not None) else None
            classification = classify_divergence(orig, paper, cell['response_type'])
            per_cell_judge.append({
                'subject': cell['subject'],
                'paper_cond': cell['paper_cond'],
                'qid': cell['qid'],
                'judge': judge,
                'response_type': cell['response_type'],
                'orig_score': orig,
                'paper_score': paper,
                'delta_paper_minus_orig': delta,
                'abs_delta': abs(delta) if delta is not None else None,
                'classification': classification,
            })

    # Per-judge aggregates
    per_judge = {}
    for j in PRIMARY_JUDGES:
        rows = [r for r in per_cell_judge if r['judge'] == j and r['delta_paper_minus_orig'] is not None]
        deltas = [r['delta_paper_minus_orig'] for r in rows]
        abs_deltas = [abs(d) for d in deltas]
        per_judge[j] = {
            'n': len(rows),
            'mean_delta': statistics.mean(deltas) if deltas else None,
            'sd_delta': statistics.pstdev(deltas) if len(deltas) > 1 else 0,
            'mean_abs_delta': statistics.mean(abs_deltas) if abs_deltas else None,
            'sum_abs_delta': sum(abs_deltas),
            'classifications': [r['classification'] for r in rows],
            'per_response_type': {},
        }
        for rt in ('refusal', 'generic_spec', 'substantive', 'short'):
            sub = [r['delta_paper_minus_orig'] for r in rows if r['response_type'] == rt]
            if sub:
                per_judge[j]['per_response_type'][rt] = {
                    'n': len(sub),
                    'mean_delta': statistics.mean(sub),
                }

    # Total |drift| across all 25 (cell, judge) pairs
    total_abs_drift = sum(r['abs_delta'] for r in per_cell_judge if r['abs_delta'] is not None)

    # Per-judge share of total |drift|
    judge_share = {}
    for j in PRIMARY_JUDGES:
        share = per_judge[j]['sum_abs_delta'] / total_abs_drift if total_abs_drift else 0
        judge_share[j] = share

    # Failure-mode counts
    cls_counts = {}
    for r in per_cell_judge:
        cls_counts[r['classification']] = cls_counts.get(r['classification'], 0) + 1

    # Verdict rule (pre-registered): if one judge accounts for >50% of total |drift|
    # AND the other 4 judges have |mean_delta| < 0.5, declare judge-specific.
    # Otherwise rubric-specific.
    max_share_judge = max(PRIMARY_JUDGES, key=lambda j: judge_share[j])
    max_share = judge_share[max_share_judge]
    others_max_abs_mean = max(abs(per_judge[j]['mean_delta']) for j in PRIMARY_JUDGES
                               if j != max_share_judge and per_judge[j]['mean_delta'] is not None)
    if max_share > 0.5 and others_max_abs_mean < 0.5:
        verdict = 'JUDGE_SPECIFIC'
        verdict_detail = (
            f'{max_share_judge} accounts for {max_share*100:.0f}% of total |drift| '
            f'and the other four judges have |mean delta| < 0.5. The cross-rubric divergence is concentrated '
            f'in {max_share_judge} rather than distributed.'
        )
    else:
        verdict = 'RUBRIC_SPECIFIC'
        verdict_detail = (
            f'No single judge exceeds the 50% threshold of total |drift| (max share: {max_share_judge} = '
            f'{max_share*100:.0f}%) and / or multiple judges show |mean delta| >= 0.5 '
            f'(largest non-leader: {others_max_abs_mean:.2f}). The cross-rubric divergence is distributed '
            f'across judges and is rubric-driven.'
        )

    return {
        'per_cell_judge': per_cell_judge,
        'per_judge': per_judge,
        'judge_share': judge_share,
        'total_abs_drift': total_abs_drift,
        'cls_counts': cls_counts,
        'verdict': verdict,
        'verdict_detail': verdict_detail,
        'max_share_judge': max_share_judge,
        'max_share': max_share,
    }


def write_synth(enriched, records, agg):
    md = []
    md.append('# Per-judge ablation on highest-divergence rubric cells\n')
    md.append('**Date:** 2026-05-08')
    md.append('**Script:** `scripts/published_rubric_per_judge_ablation_20260508.py`')
    md.append('**Source data:** `docs/research/published_rubric_robustness_check_20260508.csv`')
    md.append('**Prior finding:** Spearman rho = 0.389 between original ("outcome prediction") and paper ("behavioral pattern") rubrics across 25 cells.')
    md.append('**Question:** is the rho = 0.389 divergence judge-specific (one judge mis-applies one rubric and drives it) or rubric-specific (all judges show the same cross-rubric pattern)?\n')

    md.append('## Method')
    md.append('')
    md.append('5 cells with largest |delta| from the prior 25-cell CSV. Each cell judged by all 5 primary judges (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4) under BOTH rubrics. 5 cells x 5 judges x 2 rubrics = 50 calls. Temperature 0; identical held-out + response inputs across rubrics.')
    md.append('')
    md.append('### Selected cells')
    md.append('')
    md.append('| Subject | Cond | qid | Prior delta (paper - orig) | Response type |')
    md.append('|---|---|---:|---:|---|')
    for c in enriched:
        md.append(f'| {c["subject"]} | {c["paper_cond"]} | {c["qid"]} | {c["prior_delta"]:+.2f} | {c["response_type"]} |')
    md.append('')
    md.append('### Pre-registered verdict rule')
    md.append('')
    md.append('- **Judge-specific** if one judge accounts for >50% of total |drift| AND the other four judges have |mean delta| < 0.5.')
    md.append('- **Rubric-specific** otherwise.')
    md.append('')

    # 5x5 cell-by-judge cross-rubric delta table -- the load-bearing visualization
    md.append('## 5x5 per-cell per-judge cross-rubric delta (paper - original)')
    md.append('')
    md.append('Rows = cells, columns = judges. Cell entries: `paper_score / original_score (delta)`.')
    md.append('')
    md.append('| Cell | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | Cell mean delta |')
    md.append('|---|---|---|---|---|---|---:|')
    by_cell = {}
    for r in agg['per_cell_judge']:
        key = (r['subject'], r['paper_cond'], r['qid'])
        by_cell.setdefault(key, {})[r['judge']] = r
    for cell in enriched:
        key = (cell['subject'], cell['paper_cond'], cell['qid'])
        row_cells = by_cell.get(key, {})
        cell_label = f"{cell['subject']} {cell['paper_cond']} q{cell['qid']}"
        cells_out = [cell_label]
        deltas = []
        for j in PRIMARY_JUDGES:
            r = row_cells.get(j)
            if r and r['orig_score'] is not None and r['paper_score'] is not None:
                d = r['delta_paper_minus_orig']
                deltas.append(d)
                cells_out.append(f'{r["paper_score"]} / {r["orig_score"]} ({d:+d})')
            else:
                cells_out.append('n/a')
        mean_d = statistics.mean(deltas) if deltas else 0
        cells_out.append(f'{mean_d:+.2f}')
        md.append('| ' + ' | '.join(cells_out) + ' |')
    md.append('')

    md.append('## Per-judge cross-rubric drift summary')
    md.append('')
    md.append('| Judge | n | Mean delta (paper - orig) | SD | Mean \\|delta\\| | Sum \\|delta\\| | Share of total \\|drift\\| |')
    md.append('|---|---:|---:|---:|---:|---:|---:|')
    for j in PRIMARY_JUDGES:
        s = agg['per_judge'][j]
        share = agg['judge_share'][j]
        md.append(f'| {j} | {s["n"]} | {s["mean_delta"]:+.2f} | {s["sd_delta"]:.2f} | {s["mean_abs_delta"]:.2f} | {s["sum_abs_delta"]:.2f} | {share*100:.0f}% |')
    md.append('')

    md.append('### Per-judge drift broken out by response type')
    md.append('')
    md.append('| Judge | Refusal (n, mean delta) | Generic-spec (n, mean delta) | Substantive (n, mean delta) |')
    md.append('|---|---|---|---|')
    for j in PRIMARY_JUDGES:
        s = agg['per_judge'][j]
        cells_out = [j]
        for rt in ('refusal', 'generic_spec', 'substantive'):
            d = s['per_response_type'].get(rt)
            cells_out.append(f'{d["n"]}, {d["mean_delta"]:+.2f}' if d else '-')
        md.append('| ' + ' | '.join(cells_out) + ' |')
    md.append('')

    md.append('## Failure-mode classification')
    md.append('')
    md.append('Each (cell, judge) cross-rubric divergence labeled:')
    md.append('- **polite_refusal_as_engagement**: response is a polite refusal; original gave 4-5, paper gave 1-2.')
    md.append('- **generic_spec_as_pattern**: response is generic-spec language; original gave 4, paper gave 1-2.')
    md.append('- **substantive_underscored_by_original**: response is substantive; original gave <=2, paper gave >=3.')
    md.append('- **other**: divergence > 0.5 not fitting above.')
    md.append('- **no_divergence**: |paper - orig| <= 0.5.')
    md.append('')
    md.append('| Classification | Count (of 25 cell-judge pairs) |')
    md.append('|---|---:|')
    for cls, cnt in sorted(agg['cls_counts'].items(), key=lambda x: -x[1]):
        md.append(f'| {cls} | {cnt} |')
    md.append('')

    md.append('## Verdict')
    md.append('')
    md.append(f'**{agg["verdict"]}**')
    md.append('')
    md.append(agg['verdict_detail'])
    md.append('')

    md.append('## Implications for paper claims')
    md.append('')
    if agg['verdict'] == 'JUDGE_SPECIFIC':
        md.append('Because cross-rubric drift concentrates in a single judge, the 5-judge mean used for paper headline scores is more robust than the cell-level Spearman rho = 0.389 suggests:')
        md.append('- Per-judge weighted means (excluding the high-drift judge) would still be cross-rubric stable.')
        md.append('- Rank-order claims (gradient direction, anchor crossings) survive because 4 of 5 judges agree across rubrics.')
        md.append('- The footnote in the prior robustness check should be expanded: report the per-judge drift table + the judge-specific verdict.')
    else:
        md.append('Because cross-rubric drift is distributed across judges, the divergence is genuinely rubric-driven:')
        md.append('- The 5-judge mean is no more robust than any single judge to rubric choice.')
        md.append('- Paper claims that depend on absolute score magnitude (anchor levels, ceiling near 2.46, hedging absolute numbers) are at risk; rerun-under-paper-rubric is the conservative response.')
        md.append('- Paper claims that depend on rank order (gradient direction, who-rises-most) are likelier to survive but should be checked under the paper rubric on the full dataset before relying on them.')
    md.append('')

    md.append('## Files')
    md.append('')
    md.append('- Per-(cell, judge, rubric) raw data: `results/_per_judge_ablation_20260508/<subject>__<cond>__q<qid>__<judge>__<rubric>.json` (50 files)')
    md.append('- 50-row CSV: `docs/research/published_rubric_per_judge_ablation_20260508.csv`')
    md.append('- This synthesis: `docs/research/published_rubric_per_judge_ablation_20260508.md`')
    md.append('- Reproducibility script: `scripts/published_rubric_per_judge_ablation_20260508.py`')
    md.append('')

    SYNTH_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'Synthesis written: {SYNTH_MD}')


def main():
    print('=== Per-judge ablation on highest-divergence rubric cells ===')
    print(f'Cells: {len(SELECTED_CELLS)}; judges: {len(PRIMARY_JUDGES)}; rubrics: {len(RUBRICS)}')
    print(f'Total calls: {len(SELECTED_CELLS) * len(PRIMARY_JUDGES) * len(RUBRICS)}')
    print()

    enriched, records = run_calls()
    write_csv(records)
    agg = aggregate(enriched, records)
    write_synth(enriched, records, agg)

    print()
    print('=== HEADLINE ===')
    print(f'Verdict: {agg["verdict"]}')
    print(f'Detail: {agg["verdict_detail"]}')
    print()
    print('Per-judge mean cross-rubric drift (paper - original):')
    for j in PRIMARY_JUDGES:
        s = agg['per_judge'][j]
        print(f'  {j}: mean delta = {s["mean_delta"]:+.2f}, share of total |drift| = {agg["judge_share"][j]*100:.0f}%')
    print()
    print('Failure-mode counts:')
    for cls, cnt in sorted(agg['cls_counts'].items(), key=lambda x: -x[1]):
        print(f'  {cls}: {cnt}')


if __name__ == '__main__':
    main()
