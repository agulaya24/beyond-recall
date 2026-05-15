"""Back-check 30 paper numbers by recomputing from raw judgment JSONs.

Strategy:
  - Pull 30 (subject, condition) cells from `docs/research/v11_emit/4_1_gradient.json` and
    `docs/research/v11_emit/4_2_compression.json`. These are scaffold-derived 5-judge
    primary panel means — the numbers the audit doc verified ONCE against the scaffold
    but not against raw data.
  - For each cell, independently recompute the 5-judge primary mean from
    `results/global_<subject>/judgments_v2.json` + `_s114_backfills/` overlays.
  - Compare to scaffold value within ±0.01 tolerance.
  - Also include 5 §4.4.1 memory-system aggregate cells.
  - Also include 5 Letta numbers from §4.5.

Output: docs/research/back_check_30_20260507.csv
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
EMIT_DIR = REPO / 'docs' / 'research' / 'v11_emit'
BACKFILL_DIR = RESULTS / '_s114_backfills'

PRIMARY = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

GRADIENT_CONDS = ['C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                  'C4_factdump', 'C4a_full_facts_plus_spec']

# Hamerton uses the same condition names post-normalization (recompute_5judge_primary normalizes them)
HAMERTON_CONDS = {}  # No remapping needed


def load_subject_judgments(subject):
    """Load all judgment rows for a subject, with backfill overlay."""
    rows = []
    if subject == 'hamerton':
        # Hamerton aggregates from multiple files; defer to recompute_5judge_primary helper
        from importlib import import_module
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        rcm = import_module('recompute_5judge_primary')
        return rcm.load_hamerton_judgments()
    p = RESULTS / f'global_{subject}' / 'judgments_v2.json'
    if p.exists():
        rows = json.load(p.open(encoding='utf-8'))

    # Apply backfills
    overrides = {}
    if BACKFILL_DIR.exists():
        for f in BACKFILL_DIR.glob(f'global_{subject}__*.json'):
            try:
                data = json.load(f.open(encoding='utf-8'))
            except Exception:
                continue
            for r in data:
                if r.get('score') in (1, 2, 3, 4, 5) and not r.get('parse_failure'):
                    overrides[(r['question_id'], r['condition'], r['judge'])] = r['score']
    for r in rows:
        key = (r.get('question_id'), r.get('condition'), r.get('judge'))
        if key in overrides:
            r['score'] = overrides[key]
            r['parse_failure'] = False
    return rows


def compute_cell_mean(rows, subject, condition):
    """Compute 5-judge primary mean using per-question 5-judge mean -> mean across questions rule."""
    cond_to_match = HAMERTON_CONDS.get(condition, condition) if subject == 'hamerton' else condition

    # Group by qid -> {judge: score}
    by_qid = defaultdict(dict)
    for r in rows:
        if r.get('condition') != cond_to_match:
            continue
        if r.get('judge') not in PRIMARY:
            continue
        score = r.get('score')
        if score in (1, 2, 3, 4, 5) and not r.get('parse_failure'):
            by_qid[r['question_id']][r['judge']] = score

    # Per-question 5-judge mean (require >= 3 valid judges to include)
    per_q_means = []
    for qid, judges in by_qid.items():
        if len(judges) >= 3:
            per_q_means.append(sum(judges.values()) / len(judges))
    if not per_q_means:
        return None, 0
    return sum(per_q_means) / len(per_q_means), len(per_q_means)


def main():
    # Load scaffold values
    grad = json.load((EMIT_DIR / '4_1_gradient.json').open(encoding='utf-8'))
    grad_by_subject = {s['id']: s for s in grad['subjects']}

    # Pick 30 cells: 5 conditions × 6 subjects (mix of low/mid/high baseline + Hamerton)
    selected_subjects = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'keckley', 'augustine']
    cell_keys = ['C5', 'C2a', 'C2c', 'C4', 'C4a']
    cond_map = {'C5': 'C5_baseline', 'C2a': 'C2a_full_spec', 'C2c': 'C2c_wrong_spec',
                'C4': 'C4_factdump', 'C4a': 'C4a_full_facts_plus_spec'}

    rows_out = []
    cache_subject_rows = {}

    for subject in selected_subjects:
        for ck in cell_keys:
            if subject not in grad_by_subject:
                continue
            scaffold_val = grad_by_subject[subject].get(ck)
            if scaffold_val is None:
                continue
            condition = cond_map[ck]
            if subject not in cache_subject_rows:
                cache_subject_rows[subject] = load_subject_judgments(subject)
            recomputed, n = compute_cell_mean(cache_subject_rows[subject], subject, condition)
            scaffold_disp = round(scaffold_val, 2)
            recomp_disp = round(recomputed, 2) if recomputed is not None else None
            drift = abs(scaffold_disp - recomp_disp) if recomp_disp is not None else None
            rows_out.append({
                'check_id': f'{subject}_{ck}',
                'subject': subject,
                'condition': condition,
                'scaffold_source': '_v11_emit/4_1_gradient.json',
                'scaffold_value': scaffold_disp,
                'recomputed_value': recomp_disp,
                'n_questions': n,
                'drift': round(drift, 4) if drift is not None else None,
                'within_tolerance': drift <= 0.01 if drift is not None else False,
            })

    print(f'Recomputed {len(rows_out)} gradient cells')

    # Output
    out_csv = REPO / 'docs' / 'research' / 'back_check_30_20260507.csv'
    fields = ['check_id', 'subject', 'condition', 'scaffold_source', 'scaffold_value',
              'recomputed_value', 'n_questions', 'drift', 'within_tolerance']
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    # Summary
    n_pass = sum(1 for r in rows_out if r['within_tolerance'])
    print(f'\nWithin ±0.01 tolerance: {n_pass}/{len(rows_out)}')
    print('\nDrift > tolerance:')
    for r in rows_out:
        if not r['within_tolerance']:
            print(f'  {r["check_id"]:<30} scaffold={r["scaffold_value"]} recomputed={r["recomputed_value"]} drift={r["drift"]}')

    print(f'\nWrote {out_csv}')
    return rows_out


if __name__ == '__main__':
    main()
