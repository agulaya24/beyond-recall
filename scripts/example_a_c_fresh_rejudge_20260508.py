"""Fresh re-judge of two specific cells used as worked examples in §4.1.

Question. Does a fresh execution under the verbatim original-prompt rubric
(scripts/judge_hamerton_5judge.py lines 57-68), on the same response text
already in the repo, reproduce the cached primary-panel scores for these
two cells, or does the score drift?

Cells:
  1. global_fukuzawa  C4_factdump  q35  -- cached 1.00 unanimous (5/5 judges = 1)
  2. global_seacole   C4_factdump  q2   -- cached 2.80 with wide variance (5/2/3/3/1)

Primary 5-judge panel (model IDs identical to the per-judge ablation script):
  haiku  -> claude-haiku-4-5-20251001
  sonnet -> claude-sonnet-4-6
  opus   -> claude-opus-4-6
  gpt4o  -> gpt-4o-2024-08-06
  gpt54  -> gpt-5.4

Outputs:
  - results/_example_a_c_fresh_rejudge_20260508/<cell>/<judge>.json   (10 raw response files)
  - docs/research/example_a_c_fresh_rejudge_20260508.md               (synthesis)

Spend cap: ~$0.50, 10 calls. Temperature 0; verbatim original-prompt rubric.
"""
from __future__ import annotations

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
OUT_DIR = RESULTS / '_example_a_c_fresh_rejudge_20260508'
OUT_DIR.mkdir(parents=True, exist_ok=True)
SYNTH_MD = DOCS / 'research' / 'example_a_c_fresh_rejudge_20260508.md'

PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

JUDGE_SPEC = {
    'haiku':  {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai',    'model': 'gpt-5.4'},
}

# ---------------------------------------------------------------------------
# Cells
# ---------------------------------------------------------------------------
CELLS = [
    {
        'cell_id': 'fukuzawa_q35_C4',
        'subject': 'global_fukuzawa',
        'qid': 35,
        'condition_key': 'C4_factdump',  # the response key inside results.json
        'cached_panel': {'haiku': 1, 'sonnet': 1, 'opus': 1, 'gpt4o': 1, 'gpt54': 1},
        'cached_mean': 1.00,
    },
    {
        'cell_id': 'seacole_q2_C4',
        'subject': 'global_seacole',
        'qid': 2,
        'condition_key': 'C4_factdump',
        'cached_panel': {'haiku': 5, 'sonnet': 2, 'opus': 3, 'gpt4o': 3, 'gpt54': 1},
        'cached_mean': 2.80,
    },
]


# ---------------------------------------------------------------------------
# Verbatim rubric prompt -- lifted exactly from scripts/judge_hamerton_5judge.py
# lines 57-68. DO NOT MODIFY.
# ---------------------------------------------------------------------------
def judge_prompt(held_out: str, response_text: str) -> str:
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
            '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
            'Rate 1-5:\n'
            '5=Predicts specific outcome\n'
            '4=General direction correct\n'
            '3=Right domain wrong outcome\n'
            '2=Wrong prediction\n'
            '1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------
def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']:
        if os.environ.get(k):
            continue
        try:
            r = subprocess.run(
                ['powershell', '-Command',
                 f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
                capture_output=True, text=True
            )
            val = (r.stdout or '').strip()
            if val:
                os.environ[k] = val
        except Exception:
            pass


def parse_score(text: str) -> Optional[int]:
    if not text:
        return None
    m = re.search(r'[1-5]', str(text).strip())
    return int(m.group()) if m else None


def call_anthropic(api_key, model, prompt, max_tokens=8):
    last_err = None
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
        except Exception as e:
            last_err = e
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_openai(api_key, model, prompt, max_tokens=8):
    last_err = None
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
        except Exception as e:
            last_err = e
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge: str, prompt: str, anth_key: str, oai_key: str) -> str:
    spec = JUDGE_SPEC[judge]
    if spec['provider'] == 'anthropic':
        return call_anthropic(anth_key, spec['model'], prompt)
    return call_openai(oai_key, spec['model'], prompt)


# ---------------------------------------------------------------------------
# Cell loaders
# ---------------------------------------------------------------------------
def load_cell(cell):
    p = RESULTS / cell['subject'] / 'results.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    for r in d:
        if r.get('question_id') == cell['qid']:
            held_out = r.get('held_out_passage')
            resp = r.get('responses', {}).get(cell['condition_key'])
            text = resp.get('text', '') if isinstance(resp, dict) else (resp or '')
            if not held_out or not text:
                raise SystemExit(f'Missing held_out or response text for {cell["cell_id"]}')
            return {
                'held_out': held_out,
                'response_text': text,
                'question_text': r.get('question_text', ''),
            }
    raise SystemExit(f'qid {cell["qid"]} not found in {p}')


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------
def run_calls():
    load_env()
    anth_key = os.environ.get('ANTHROPIC_API_KEY')
    oai_key = os.environ.get('OPENAI_API_KEY')
    if not anth_key:
        print('FATAL: ANTHROPIC_API_KEY missing'); sys.exit(1)
    if not oai_key:
        print('FATAL: OPENAI_API_KEY missing'); sys.exit(1)

    enriched = []
    for cell in CELLS:
        loaded = load_cell(cell)
        c = dict(cell)
        c.update(loaded)
        enriched.append(c)
        print(f'[load] {c["cell_id"]}: held_out_len={len(c["held_out"])}, '
              f'response_len={len(c["response_text"])}')
    print()

    fresh_records = []
    total = len(enriched) * len(PRIMARY_JUDGES)
    done = 0
    new_calls = 0

    for cell in enriched:
        cell_dir = OUT_DIR / cell['cell_id']
        cell_dir.mkdir(parents=True, exist_ok=True)
        prompt = judge_prompt(cell['held_out'], cell['response_text'])
        # Save the prompt once per cell for inspection
        (cell_dir / '_prompt.txt').write_text(prompt, encoding='utf-8')
        for judge in PRIMARY_JUDGES:
            outp = cell_dir / f'{judge}.json'
            if outp.exists():
                rec = json.loads(outp.read_text(encoding='utf-8'))
                done += 1
                fresh_records.append(rec)
                print(f'[{done}/{total}] cached: {cell["cell_id"]} {judge} -> {rec.get("score")}')
                continue
            try:
                raw = call_judge(judge, prompt, anth_key, oai_key)
                score = parse_score(raw)
                err = None
            except Exception as e:
                raw = f'ERROR: {e}'
                score = None
                err = str(e)
            rec = {
                'cell_id': cell['cell_id'],
                'subject': cell['subject'],
                'qid': cell['qid'],
                'condition_key': cell['condition_key'],
                'judge': judge,
                'judge_model': JUDGE_SPEC[judge]['model'],
                'judge_provider': JUDGE_SPEC[judge]['provider'],
                'rubric': 'original_judge_hamerton_5judge_lines_57_68',
                'temperature': 0,
                'score': score,
                'raw': str(raw)[:500],
                'parse_failure': score is None,
                'error': err,
                'held_out': cell['held_out'],
                'response_text_snippet': cell['response_text'][:1500],
                'cached_score': cell['cached_panel'].get(judge),
                'timestamp': datetime.utcnow().isoformat() + 'Z',
            }
            outp.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding='utf-8')
            fresh_records.append(rec)
            done += 1
            new_calls += 1
            print(f'[{done}/{total}] {cell["cell_id"]} {judge} -> fresh={score} (cached={cell["cached_panel"].get(judge)})')

    print(f'\nTotal records: {len(fresh_records)}; new API calls: {new_calls}\n')
    return enriched, fresh_records


# ---------------------------------------------------------------------------
# Synthesis
# ---------------------------------------------------------------------------
def write_synth(enriched, fresh_records):
    # Index fresh records by (cell_id, judge)
    idx = {(r['cell_id'], r['judge']): r for r in fresh_records}

    md = []
    md.append('# Example A & C: Fresh re-judge under the verbatim rubric\n')
    md.append('**Date:** 2026-05-08')
    md.append('**Script:** `scripts/example_a_c_fresh_rejudge_20260508.py`')
    md.append('**Rubric:** verbatim original-prompt rubric from `scripts/judge_hamerton_5judge.py` lines 57-68')
    md.append('**Temperature:** 0; primary 5-judge panel; identical held-out + response inputs as cached run')
    md.append('')
    md.append('## Question')
    md.append('')
    md.append('Two cells were flagged as worked examples in paper §4.1. We ask: under a fresh execution at temperature 0, with the same rubric prompt and the same response text already in the repo, do the 5 primary judges reproduce the cached panel scores, or does the score drift?')
    md.append('')
    md.append('Cells:')
    md.append('')
    md.append('| Cell | Subject | qid | Condition | Cached panel (h/s/o/g4o/g54) | Cached mean |')
    md.append('|---|---|---:|---|---|---:|')
    for cell in enriched:
        cp = cell['cached_panel']
        panel_str = '/'.join(str(cp[j]) for j in PRIMARY_JUDGES)
        md.append(f'| {cell["cell_id"]} | {cell["subject"]} | {cell["qid"]} | {cell["condition_key"]} | {panel_str} | {cell["cached_mean"]:.2f} |')
    md.append('')

    # Per-cell comparison table
    md.append('## Per-cell comparison: cached vs fresh')
    md.append('')
    summary_rows = []
    for cell in enriched:
        md.append(f'### {cell["cell_id"]}')
        md.append('')
        md.append(f'**Held-out (verbatim ground truth):** "{cell["held_out"]}"')
        md.append('')
        md.append(f'**Response (first 300 chars):** {cell["response_text"][:300].strip()}{"..." if len(cell["response_text"]) > 300 else ""}')
        md.append('')
        md.append('| Judge | Cached score | Fresh score | Delta (fresh - cached) |')
        md.append('|---|---:|---:|---:|')
        cached_vals = []
        fresh_vals = []
        for j in PRIMARY_JUDGES:
            r = idx.get((cell['cell_id'], j))
            cached = cell['cached_panel'][j]
            fresh = r['score'] if r else None
            cached_vals.append(cached)
            if fresh is not None:
                fresh_vals.append(fresh)
                delta = fresh - cached
                md.append(f'| {j} | {cached} | {fresh} | {delta:+d} |')
            else:
                md.append(f'| {j} | {cached} | parse_failure | n/a |')
        cached_mean = statistics.mean(cached_vals) if cached_vals else None
        fresh_mean = statistics.mean(fresh_vals) if fresh_vals else None
        cached_sd = statistics.pstdev(cached_vals) if len(cached_vals) > 1 else 0
        fresh_sd = statistics.pstdev(fresh_vals) if len(fresh_vals) > 1 else 0
        mean_drift = (fresh_mean - cached_mean) if (cached_mean is not None and fresh_mean is not None) else None
        md.append('')
        md.append(f'- Cached mean: {cached_mean:.2f} (SD={cached_sd:.2f})')
        md.append(f'- Fresh mean:  {fresh_mean:.2f} (SD={fresh_sd:.2f})')
        if mean_drift is not None:
            md.append(f'- Mean drift (fresh - cached): {mean_drift:+.2f}')
        md.append('')
        summary_rows.append({
            'cell_id': cell['cell_id'],
            'cached_mean': cached_mean,
            'fresh_mean': fresh_mean,
            'cached_sd': cached_sd,
            'fresh_sd': fresh_sd,
            'mean_drift': mean_drift,
            'within_05_band': abs(mean_drift) <= 0.5 if mean_drift is not None else None,
        })

    md.append('## Verdict')
    md.append('')
    md.append('Reproduction criterion: |fresh mean - cached mean| <= 0.5 -> reproduces; otherwise drifts.')
    md.append('')
    md.append('| Cell | Cached mean | Fresh mean | Mean drift | Within +/-0.5? | Verdict |')
    md.append('|---|---:|---:|---:|:---:|---|')
    for s in summary_rows:
        verdict = 'REPRODUCES' if s['within_05_band'] else 'DRIFTS'
        md.append(f'| {s["cell_id"]} | {s["cached_mean"]:.2f} | {s["fresh_mean"]:.2f} | {s["mean_drift"]:+.2f} | {"YES" if s["within_05_band"] else "no"} | {verdict} |')
    md.append('')

    # Implications
    md.append('## Implications for the worked examples in §4.1')
    md.append('')
    fukuzawa = next(s for s in summary_rows if s['cell_id'] == 'fukuzawa_q35_C4')
    seacole = next(s for s in summary_rows if s['cell_id'] == 'seacole_q2_C4')

    md.append(f'**Fukuzawa Q35 C4_factdump.** Cached panel was 1.00 unanimous. Aarik flagged the unanimous 1.00 as inconsistent with the verbatim rubric: a substantively engaged correct-direction response (the model identifies "practical concern rather than moral principle... students were more valuable to Japan\'s future as scholars than as soldiers") should score 3 or 4 under the rubric, not 1. Fresh execution under the same rubric yields {fukuzawa["fresh_mean"]:.2f} (drift {fukuzawa["mean_drift"]:+.2f}). ')
    if fukuzawa['within_05_band']:
        md.append(f'Result: fresh judges reproduce the cached unanimous 1, indicating the score is rubric-stable rather than a stochastic anomaly. The unanimous 1 reflects how all 5 judges actually apply the rubric "1 = Refuses or off-base" to a substantively-engaged-but-non-anchor-matching response. The mismatch between rubric language and judge behavior is structural, not stochastic.\n')
    else:
        md.append(f'Result: fresh judges drift away from the cached unanimous 1 by {fukuzawa["mean_drift"]:+.2f}, suggesting the cached score is not stable under the rubric and the worked example may be a stochastic artifact rather than a structural rubric pattern.\n')

    md.append(f'**Seacole Q2 C4_factdump.** Cached panel was 2.80 with wide variance (5/2/3/3/1). Fresh execution yields {seacole["fresh_mean"]:.2f} (drift {seacole["mean_drift"]:+.2f}, fresh SD {seacole["fresh_sd"]:.2f} vs cached SD {seacole["cached_sd"]:.2f}). ')
    if seacole['within_05_band']:
        md.append('Result: fresh judges reproduce the wide-variance pattern within the +/-0.5 band, indicating the divergence across judges is a stable property of the cell rather than a stochastic artifact. The disagreement is driven by judges applying the same rubric language differently to the same response, not by run-to-run noise.\n')
    else:
        md.append('Result: fresh judges drift outside the +/-0.5 band, suggesting the cached panel is not stable and the wide-variance worked example reflects run-to-run noise rather than a structural rubric pattern.\n')

    md.append('## Files')
    md.append('')
    md.append('- Per-(cell, judge) raw responses: `results/_example_a_c_fresh_rejudge_20260508/<cell_id>/<judge>.json`')
    md.append('- Verbatim prompts saved per cell: `results/_example_a_c_fresh_rejudge_20260508/<cell_id>/_prompt.txt`')
    md.append('- This synthesis: `docs/research/example_a_c_fresh_rejudge_20260508.md`')
    md.append('- Reproducibility script: `scripts/example_a_c_fresh_rejudge_20260508.py`')
    md.append('')

    SYNTH_MD.parent.mkdir(parents=True, exist_ok=True)
    SYNTH_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'Synthesis written: {SYNTH_MD}')


def main():
    print('=== Example A & C fresh re-judge ===')
    print(f'Cells: {len(CELLS)}; judges: {len(PRIMARY_JUDGES)}; total calls (max): {len(CELLS) * len(PRIMARY_JUDGES)}')
    print()

    enriched, fresh_records = run_calls()
    write_synth(enriched, fresh_records)

    print()
    print('=== HEADLINE ===')
    for cell in CELLS:
        cached_mean = cell['cached_mean']
        fresh_scores = [r['score'] for r in fresh_records
                        if r['cell_id'] == cell['cell_id'] and r['score'] is not None]
        fresh_mean = statistics.mean(fresh_scores) if fresh_scores else None
        if fresh_mean is None:
            print(f'{cell["cell_id"]}: cached={cached_mean:.2f}, fresh=PARSE_FAILURE')
        else:
            drift = fresh_mean - cached_mean
            verdict = 'REPRODUCES' if abs(drift) <= 0.5 else 'DRIFTS'
            print(f'{cell["cell_id"]}: cached={cached_mean:.2f}, fresh={fresh_mean:.2f}, drift={drift:+.2f} -> {verdict}')


if __name__ == '__main__':
    main()
