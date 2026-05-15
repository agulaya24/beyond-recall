"""Published-rubric robustness check (Option B from
`docs/reviews/rubric_defensibility_analysis_20260508.md`).

Goal. The published §3.3 rubric in `docs/beyond_recall_v11_8_draft.md` describes
"behavioral pattern" granularity (Refusal -> Generic -> Partial pattern ->
Substantive multi-dimensional -> Verbatim held-out match). The judge prompt
actually used in scoring (see `scripts/judge_hamerton_5judge.py`) wires
"outcome prediction" granularity (Refusal -> Wrong prediction -> Right domain
wrong outcome -> General direction correct -> Predicts specific outcome).

The textual claim is that the two are construct-equivalent under different
wordings. This script converts that claim into an empirical claim by
re-judging a stratified sample of 25 (subject, condition, question_id) cells
with the paper rubric verbatim and comparing to the original-prompt scores.

Inputs are the existing canonical response files plus held-out passages.
Outputs:
  - results/_published_rubric_robustness_20260508/<subject>/<cond>_q<qid>_<judge>.json
  - docs/research/published_rubric_robustness_check_20260508.csv
  - docs/research/published_rubric_robustness_check_20260508.md (synthesis)

Spend cap: $10. Budget: 25 cells * 5 judges = 125 calls. At typical pricing
this is ~$1-2.

Reproducibility seed: 42. Sample design recorded in the synthesis md.
"""
from __future__ import annotations

import csv
import json
import os
import random
import re
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DOCS = REPO / 'docs'
OUT_DIR = RESULTS / '_published_rubric_robustness_20260508'
OUT_DIR.mkdir(parents=True, exist_ok=True)
SYNTH_CSV = DOCS / 'research' / 'published_rubric_robustness_check_20260508.csv'
SYNTH_MD = DOCS / 'research' / 'published_rubric_robustness_check_20260508.md'

SEED = 42
PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

JUDGE_SPEC = {
    'haiku':  {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai',    'model': 'gpt-5.4'},
}

# Sample design. 5 subjects spanning the gradient + 2 patches for missing data.
# - Hamerton: C2a, C4a, C8, C9 (no C5 in this subject's data)
# - Sunity Devee: C5 (lowest-baseline subject; patches Hamerton C5 + Babur C9)
# - Ebers, Yung Wing, Equiano: full 5 conditions
# - Babur: C5, C2a, C4a, C8 (C9 data absent)
# Total: 4 + 1 + 5 + 5 + 4 + 5 + 1 = 25 cells. Each condition stratum has 5 cells.

SAMPLE_DESIGN = [
    ('hamerton',         ['C2a', 'C4a', 'C8', 'C9']),
    ('global_sunity_devee', ['C5_baseline', 'C9']),
    ('global_ebers',     ['C5_baseline', 'C2a', 'C4a', 'C8', 'C9']),
    ('global_yung_wing', ['C5_baseline', 'C2a', 'C4a', 'C8', 'C9']),
    ('global_babur',     ['C5_baseline', 'C2a', 'C4a', 'C8']),
    ('global_equiano',   ['C5_baseline', 'C2a', 'C4a', 'C8', 'C9']),
]

CONDITION_ALIASES = {
    'C5_baseline': ['C5_baseline'],
    'C2a': ['C2a_full_spec', 'C2a_spec'],
    'C4a': ['C4a_full_facts_plus_spec', 'C4a_full_all_facts_plus_spec', 'C4a_facts_plus_spec'],
    'C8':  ['C8_raw_corpus'],
    'C9':  ['C9_raw_corpus_plus_spec'],
}


# ----------------------------------------------------------------------------
# Paper-rubric prompt (§3.3 verbatim wording, lines 380-386 of v11.8 draft)
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


# ----------------------------------------------------------------------------
# Loader: response + held-out + original 5-judge scores for a (subject, cond, qid)
# ----------------------------------------------------------------------------

def load_jsonl_array(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def find_response(subj_dir: Path, qid: int, paper_cond: str):
    aliases = CONDITION_ALIASES[paper_cond]
    for fname in ['results.json', 'baselayer_results.json', 'c8_c9_results.json',
                  'fullstack_haiku.json', 'results_v2.json']:
        d = load_jsonl_array(subj_dir / fname)
        if not d:
            continue
        for r in d:
            if r.get('question_id') != qid:
                continue
            ho = r.get('held_out_passage')
            if not ho:
                continue
            for alias in aliases:
                resps = r.get('responses', {})
                if alias in resps:
                    rec = resps[alias]
                    text = rec.get('text', '') if isinstance(rec, dict) else (rec or '')
                    if text and len(text.strip()) > 50:
                        return {
                            'response_text': text,
                            'held_out': ho,
                            'raw_cond_label': alias,
                            'response_source_file': fname,
                            'question_text': r.get('question_text', ''),
                        }
    return None


def find_original_scores(subj_dir: Path, qid: int, raw_cond: str) -> dict:
    """Return {judge: score} from existing judgment files. Looks across all
    *.json in subj_dir + the _s114_backfills/ directory."""
    out: dict = {}

    def _consume_record(r):
        if not isinstance(r, dict):
            return
        if r.get('question_id') != qid or r.get('condition') != raw_cond:
            return
        # unified schema
        j = r.get('judge')
        sc = r.get('score')
        if j and sc not in (None, 0):
            jc = j.lower().replace('-', '').replace('.', '')
            jc = {'haiku': 'haiku', 'sonnet': 'sonnet', 'opus': 'opus',
                  'gpt4o': 'gpt4o', 'gpt54': 'gpt54', 'gpt5': 'gpt54'}.get(jc, jc)
            if jc in PRIMARY_JUDGES:
                out[jc] = sc
        # wide schema with <judge>_score columns
        for jname, jc in [('haiku', 'haiku'), ('sonnet', 'sonnet'), ('opus', 'opus'),
                          ('gpt4o', 'gpt4o'), ('gpt54', 'gpt54')]:
            key = f'{jname}_score'
            if key in r and r[key] not in (None, 0):
                out[jc] = r[key]

    for fp in sorted(subj_dir.glob('*.json')):
        n = fp.name.lower()
        if 'retrieval' in n or 'manifest' in n or 'extracted' in n or 'ingestion' in n:
            continue
        if 'results' in n and 'judgments' not in n:
            continue
        d = load_jsonl_array(fp)
        if not d or not isinstance(d, list):
            continue
        for r in d:
            _consume_record(r)

    backfill_dir = RESULTS / '_s114_backfills'
    if backfill_dir.exists():
        prefix = subj_dir.name
        for jc in PRIMARY_JUDGES:
            fp = backfill_dir / f'{prefix}__{raw_cond}__{jc}.json'
            if fp.exists():
                d = load_jsonl_array(fp)
                if d:
                    for r in d:
                        if r.get('question_id') == qid and r.get('condition') == raw_cond:
                            sc = r.get('score')
                            if sc not in (None, 0):
                                out[jc] = sc
                                break
    return out


# ----------------------------------------------------------------------------
# Sampling
# ----------------------------------------------------------------------------

def sample_cells():
    """Return list of dicts: {subject, paper_cond, qid, raw_cond_label,
    response_text, held_out, original_scores}."""
    rnd = random.Random(SEED)
    cells = []
    for subject, conds in SAMPLE_DESIGN:
        sd = RESULTS / subject
        # Find all qids with held-out passages, restricted to those that have
        # responses for ALL the requested conditions (so the sample is
        # genuinely paired across the conditions used per subject).
        all_qids = set()
        # Use the union of qids appearing in any of the canonical response files
        for fname in ['results.json', 'baselayer_results.json', 'c8_c9_results.json',
                      'fullstack_haiku.json', 'results_v2.json']:
            d = load_jsonl_array(sd / fname)
            if not d:
                continue
            for r in d:
                if r.get('held_out_passage'):
                    all_qids.add(r['question_id'])

        valid_qids = []
        for qid in sorted(all_qids):
            ok_all = True
            cell_data = {}
            for pc in conds:
                resp = find_response(sd, qid, pc)
                if not resp:
                    ok_all = False
                    break
                # Require all 5 original judges
                orig = find_original_scores(sd, qid, resp['raw_cond_label'])
                if any(j not in orig for j in PRIMARY_JUDGES):
                    ok_all = False
                    break
                cell_data[pc] = (resp, orig)
            if ok_all:
                valid_qids.append((qid, cell_data))
        if not valid_qids:
            print(f'[WARN] {subject}: no qids satisfy all required conditions ({conds})')
            continue
        # Per-condition: pick one random qid from valid_qids for that condition.
        # We want one (qid) per (subject, condition). Sample 1 qid per cond
        # independently. (Could be same qid; that is fine.)
        for pc in conds:
            qid, cdata = rnd.choice(valid_qids)
            resp, orig = cdata[pc]
            cells.append({
                'subject': subject,
                'paper_cond': pc,
                'raw_cond_label': resp['raw_cond_label'],
                'qid': qid,
                'response_text': resp['response_text'],
                'held_out': resp['held_out'],
                'question_text': resp['question_text'],
                'response_source_file': resp['response_source_file'],
                'original_scores': orig,
            })
    return cells


# ----------------------------------------------------------------------------
# Judge calls
# ----------------------------------------------------------------------------

def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']:
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


def cell_outdir(cell):
    return OUT_DIR / cell['subject']


def cell_outpath(cell, judge):
    return cell_outdir(cell) / f'{cell["paper_cond"]}_q{cell["qid"]}_{judge}.json'


def rejudge_all(cells):
    load_env()
    anth_key = os.environ.get('ANTHROPIC_API_KEY')
    oai_key = os.environ.get('OPENAI_API_KEY')
    if not anth_key:
        print('FATAL: ANTHROPIC_API_KEY missing'); sys.exit(1)
    if not oai_key:
        print('FATAL: OPENAI_API_KEY missing'); sys.exit(1)

    total = len(cells) * len(PRIMARY_JUDGES)
    done = 0
    new_calls = 0
    new_results = []  # all rerun records, also re-loaded from disk if existing
    for cell in cells:
        cell_outdir(cell).mkdir(parents=True, exist_ok=True)
        prompt = paper_rubric_prompt(cell['held_out'], cell['response_text'])
        for judge in PRIMARY_JUDGES:
            outp = cell_outpath(cell, judge)
            if outp.exists():
                # Resume: skip
                rec = json.loads(outp.read_text(encoding='utf-8'))
                done += 1
                new_results.append(rec)
                print(f'[{done}/{total}] cached: {cell["subject"]}/{cell["paper_cond"]}/q{cell["qid"]}/{judge} -> {rec.get("paper_rubric_score")}')
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
                'paper_rubric_score': score,
                'paper_rubric_raw': str(raw)[:200],
                'parse_failure': score is None,
                'original_score': cell['original_scores'].get(judge),
                'timestamp': datetime.utcnow().isoformat() + 'Z',
            }
            outp.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding='utf-8')
            new_results.append(rec)
            done += 1
            new_calls += 1
            print(f'[{done}/{total}] {cell["subject"]}/{cell["paper_cond"]}/q{cell["qid"]}/{judge} -> orig={rec["original_score"]} new={score}')
    print(f'\n  Total cells: {len(cells)}; cell-judge records: {len(new_results)}; new API calls this run: {new_calls}')
    return new_results


# ----------------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------------

def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def spearman(xs, ys):
    def rank(vs):
        sv = sorted([(v, i) for i, v in enumerate(vs)])
        out = [0.0] * len(vs)
        i = 0
        while i < len(sv):
            j = i
            while j + 1 < len(sv) and sv[j + 1][0] == sv[i][0]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[sv[k][1]] = avg_rank
            i = j + 1
        return out
    return pearson(rank(xs), rank(ys))


def analyze(cells, rerun_records):
    """Aggregate per-cell original/new mean scores, run correlations, write CSV."""
    # Group by (subject, paper_cond, qid)
    by_cell = {}
    for r in rerun_records:
        key = (r['subject'], r['paper_cond'], r['qid'])
        by_cell.setdefault(key, []).append(r)

    rows = []
    for cell in cells:
        key = (cell['subject'], cell['paper_cond'], cell['qid'])
        rerun = by_cell.get(key, [])
        # Skip if not all judges complete
        rerun = {r['judge']: r for r in rerun}
        # Per-judge data
        per_judge_orig = cell['original_scores']
        per_judge_new = {j: rerun[j]['paper_rubric_score'] for j in PRIMARY_JUDGES if j in rerun and rerun[j]['paper_rubric_score'] is not None}
        if len(per_judge_new) < 5 or len(per_judge_orig) < 5:
            print(f'[SKIP] cell {key} incomplete ({len(per_judge_new)} new, {len(per_judge_orig)} orig)')
            continue
        orig_mean = sum(per_judge_orig[j] for j in PRIMARY_JUDGES) / 5
        new_mean = sum(per_judge_new[j] for j in PRIMARY_JUDGES) / 5
        delta = new_mean - orig_mean
        rows.append({
            'subject': cell['subject'],
            'paper_cond': cell['paper_cond'],
            'raw_cond_label': cell['raw_cond_label'],
            'qid': cell['qid'],
            'orig_mean': round(orig_mean, 4),
            'new_mean': round(new_mean, 4),
            'delta_new_minus_orig': round(delta, 4),
            **{f'orig_{j}': per_judge_orig[j] for j in PRIMARY_JUDGES},
            **{f'new_{j}': per_judge_new[j] for j in PRIMARY_JUDGES},
        })

    # Write CSV
    SYNTH_CSV.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(SYNTH_CSV, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f'\nCSV written: {SYNTH_CSV} ({len(rows)} rows)')

    # Correlations
    orig_means = [r['orig_mean'] for r in rows]
    new_means = [r['new_mean'] for r in rows]
    deltas = [r['delta_new_minus_orig'] for r in rows]
    pr = pearson(orig_means, new_means)
    sr = spearman(orig_means, new_means)
    mean_delta = sum(deltas) / len(deltas) if deltas else None
    sd_delta = statistics.pstdev(deltas) if len(deltas) > 1 else 0
    # 95% Bland-Altman limits of agreement
    loa_lo = (mean_delta or 0) - 1.96 * sd_delta
    loa_hi = (mean_delta or 0) + 1.96 * sd_delta
    abs_max = max(abs(d) for d in deltas) if deltas else 0
    abs_min = min(abs(d) for d in deltas) if deltas else 0

    # Per-judge consistency (Pearson r between orig_score and new_score across cells, per judge)
    per_judge = {}
    for j in PRIMARY_JUDGES:
        xs = [r[f'orig_{j}'] for r in rows]
        ys = [r[f'new_{j}'] for r in rows]
        per_judge[j] = {
            'n': len(xs),
            'pearson': pearson(xs, ys),
            'spearman': spearman(xs, ys),
            'mean_delta': sum((y - x) for x, y in zip(xs, ys)) / len(xs) if xs else None,
        }

    return {
        'n_cells': len(rows),
        'pearson_r': pr,
        'spearman_rho': sr,
        'mean_delta': mean_delta,
        'sd_delta': sd_delta,
        'loa_95_lo': loa_lo,
        'loa_95_hi': loa_hi,
        'abs_min': abs_min,
        'abs_max': abs_max,
        'per_judge': per_judge,
        'rows': rows,
    }


def write_synth(stats, cells):
    n = stats['n_cells']
    rho = stats['spearman_rho']
    pr = stats['pearson_r']
    mean_delta = stats['mean_delta']
    sd_delta = stats['sd_delta']
    loa_lo = stats['loa_95_lo']
    loa_hi = stats['loa_95_hi']

    # Verdict
    if rho is None:
        verdict = 'INCONCLUSIVE (insufficient data)'
        verdict_detail = 'Not enough valid cells to compute Spearman correlation.'
    elif rho > 0.85:
        verdict = 'CONSTRUCT EQUIVALENCE EMPIRICALLY VALIDATED'
        verdict_detail = (
            'Spearman ρ > 0.85 indicates the two rubrics produce '
            'rank-equivalent cell-level scores. The textual claim that the '
            'two rubrics describe the same construct under different wordings '
            'survives empirical test.'
        )
    elif rho > 0.70:
        verdict = 'MODERATELY EQUIVALENT (NOTE-WORTHY VARIANCE)'
        verdict_detail = (
            'Spearman ρ in (0.70, 0.85] indicates the two rubrics rank cells '
            'similarly but show non-trivial per-cell variance. The textual '
            'equivalence claim should be qualified by a footnote in §3.3 '
            'reporting this Spearman ρ and the per-cell delta distribution.'
        )
    else:
        verdict = 'EQUIVALENCE NOT EMPIRICALLY SUPPORTED. ESCALATE.'
        verdict_detail = (
            'Spearman ρ ≤ 0.70 indicates the two rubrics produce divergent '
            'cell-level rankings. The textual equivalence claim does NOT '
            'survive empirical test; expanding the sample, redesigning the '
            'rubric prompt, or rerunning headline scores under the published '
            'rubric should be considered before launch.'
        )

    # Per-cell distribution
    deltas = [r['delta_new_minus_orig'] for r in stats['rows']]
    delta_min = min(deltas) if deltas else 0
    delta_max = max(deltas) if deltas else 0
    delta_med = statistics.median(deltas) if deltas else 0

    # Per-judge table
    pj_lines = ['| Judge | n | Pearson r (orig vs new) | Spearman ρ | Mean Δ (new − orig) |',
                '|---|---:|---:|---:|---:|']
    for j in PRIMARY_JUDGES:
        s = stats['per_judge'][j]
        pj_lines.append(
            f'| {j} | {s["n"]} | '
            f'{s["pearson"]:.3f} | {s["spearman"]:.3f} | '
            f'{s["mean_delta"]:+.3f} |' if s["pearson"] is not None and s["spearman"] is not None and s["mean_delta"] is not None
            else f'| {j} | {s["n"]} | n/a | n/a | n/a |'
        )

    # Sample design lines
    sd_lines = ['| Subject | Conditions sampled |', '|---|---|']
    by_subj = {}
    for r in stats['rows']:
        by_subj.setdefault(r['subject'], []).append(r['paper_cond'])
    for s, cs in by_subj.items():
        sd_lines.append(f'| {s} | {", ".join(sorted(set(cs)))} |')

    # Cells table
    cells_lines = ['| Subject | Cond | qid | Orig 5-judge mean | New 5-judge mean | Δ |',
                   '|---|---|---:|---:|---:|---:|']
    for r in sorted(stats['rows'], key=lambda x: (x['subject'], x['paper_cond'], x['qid'])):
        cells_lines.append(
            f"| {r['subject']} | {r['paper_cond']} | {r['qid']} | "
            f"{r['orig_mean']:.2f} | {r['new_mean']:.2f} | {r['delta_new_minus_orig']:+.2f} |"
        )

    md = []
    md.append(f'# Published-rubric robustness check (Option B)\n')
    md.append(f'**Date:** 2026-05-08')
    md.append(f'**Script:** `scripts/published_rubric_robustness_20260508.py` (seed = {SEED})')
    md.append(f'**Spec source:** `docs/reviews/rubric_defensibility_analysis_20260508.md` Option B')
    md.append(f'**Paper rubric source:** `docs/beyond_recall_v11_8_draft.md` §3.3, lines 380–386')
    md.append(f'**Original prompt rubric source:** `scripts/judge_hamerton_5judge.py` lines 57–68\n')

    md.append('## Executive summary')
    md.append('')
    if rho is not None:
        md.append(f'**Spearman ρ = {rho:.3f}** between the original-prompt 5-judge primary mean and the paper-rubric 5-judge primary mean across {n} stratified (subject, condition, qid) cells. Pearson r = {pr:.3f}. Mean cell-level delta = {mean_delta:+.3f} (SD {sd_delta:.3f}); 95% Bland–Altman limits of agreement [{loa_lo:+.3f}, {loa_hi:+.3f}]. Verdict: **{verdict}**.')
    else:
        md.append('Insufficient data to compute Spearman ρ.')
    md.append('')
    md.append(verdict_detail)
    md.append('')

    md.append('## Method')
    md.append('')
    md.append('**Sample design.** 25 stratified cells, 5 conditions × 5 cells each, drawn from 6 subjects spanning the gradient. Each (subject, condition, qid) cell has both (a) a response with held-out passage and (b) all 5 primary judges\' original scores already computed.\n')
    md.append('\n'.join(sd_lines))
    md.append('')
    md.append('Two patches were applied where the canonical data lacks a condition for a named subject:')
    md.append('- Hamerton has no `C5_baseline` row in `results.json`; substituted Sunity Devee\'s C5 cell.')
    md.append('- Babur\'s `c8_c9_results.json` has empty `C9_raw_corpus_plus_spec` response text; substituted Sunity Devee\'s C9 cell.')
    md.append('')
    md.append('Each cell is re-judged by the 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4) using a prompt that quotes the published §3.3 rubric verbatim. The original judge prompt rubric (used in scoring) and the paper rubric are textually distinct: the original wires "outcome prediction" wording, the paper wires "behavioral pattern" wording.')
    md.append('')
    md.append('**Cost.** 25 cells × 5 judges = 125 API calls. Below the $10 spend cap.')
    md.append('')

    md.append('## Results')
    md.append('')
    md.append(f'- Cells with complete data (5 orig + 5 new judges): **{n}**')
    md.append(f'- **Spearman ρ = {rho:.3f}**' if rho is not None else '- Spearman ρ: n/a')
    md.append(f'- Pearson r = {pr:.3f}' if pr is not None else '- Pearson r: n/a')
    md.append(f'- Mean delta (new − orig) = {mean_delta:+.3f}; SD {sd_delta:.3f}')
    md.append(f'- 95% Bland–Altman limits of agreement: [{loa_lo:+.3f}, {loa_hi:+.3f}]')
    md.append(f'- Per-cell delta range: [{delta_min:+.2f}, {delta_max:+.2f}]; median {delta_med:+.2f}')
    md.append('')
    md.append('### Per-cell scores')
    md.append('')
    md.append('\n'.join(cells_lines))
    md.append('')

    md.append('### Per-judge consistency across the two rubrics')
    md.append('')
    md.append('\n'.join(pj_lines))
    md.append('')

    md.append('## Verdict')
    md.append('')
    md.append(f'**{verdict}**')
    md.append('')
    md.append(verdict_detail)
    md.append('')

    md.append('## Recommendation for §3.3 paper text')
    md.append('')
    if rho is not None and rho > 0.85:
        md.append('Add a footnote in §3.3 of the paper after the rubric table:')
        md.append('')
        md.append(f'> The judge prompt actually used in scoring (released in `scripts/judge_hamerton_5judge.py`) wires the rubric in outcome-prediction wording rather than the behavioral-pattern wording shown above. To validate that the two rubrics describe the same construct, we re-judged a stratified 25-cell sample (5 subjects × 5 conditions) with the published rubric verbatim under the same 5-judge primary panel; cell-level mean scores correlated at Spearman ρ = {rho:.2f} (Pearson r = {pr:.2f}); 95% Bland–Altman limits of agreement [{loa_lo:+.2f}, {loa_hi:+.2f}]. Detailed methodology and per-cell data: `docs/research/published_rubric_robustness_check_20260508.{{md,csv}}`; reproducibility script: `scripts/published_rubric_robustness_20260508.py`.')
    elif rho is not None and rho > 0.70:
        md.append('Add a footnote in §3.3 of the paper acknowledging that the prompt rubric and the published rubric correlate at Spearman ρ in (0.70, 0.85], and report the per-cell delta distribution. The footnote should be longer than the equivalent-construct case and should note that the relationship between the two rubrics is "moderately equivalent with notable per-cell variance" rather than "construct-equivalent."')
    else:
        md.append('**Do not publish under the current rubric mismatch.** Spearman ρ is at or below 0.70, indicating that the published rubric and the actual scoring rubric are not interchangeable. Either rerun the headline scores under the published rubric, or restate §3.3 to publish the actual prompt rubric verbatim.')
    md.append('')

    md.append('## Files')
    md.append('')
    md.append('- Per-cell, per-judge raw rerun data: `results/_published_rubric_robustness_20260508/<subject>/`')
    md.append('- Per-cell aggregate CSV: `docs/research/published_rubric_robustness_check_20260508.csv`')
    md.append('- This synthesis: `docs/research/published_rubric_robustness_check_20260508.md`')
    md.append('- Reproducibility script: `scripts/published_rubric_robustness_20260508.py`')
    md.append('')

    SYNTH_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'\nSynthesis written: {SYNTH_MD}')
    print(f'\nHEADLINE: Spearman rho = {rho if rho is not None else "n/a"}; verdict: {verdict}')


def main():
    print('=== Published-rubric robustness check (Option B) ===')
    print(f'Sampling 25 cells with seed={SEED}')
    cells = sample_cells()
    print(f'Sampled {len(cells)} cells:')
    by_cond = {}
    for c in cells:
        by_cond.setdefault(c['paper_cond'], []).append((c['subject'], c['qid']))
    for pc, lst in sorted(by_cond.items()):
        print(f'  {pc}: {lst}')

    if len(cells) < 20:
        print('FATAL: under-sampled. Aborting.')
        sys.exit(1)

    print('\nRe-judging with paper rubric...\n')
    rerun = rejudge_all(cells)
    stats = analyze(cells, rerun)
    write_synth(stats, cells)


if __name__ == '__main__':
    main()
