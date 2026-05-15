"""Identify actionable parse failures: cells where a response exists but the judge call failed."""

import json
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))

# Reuse helpers from backfill script
from backfill_all_parse_failures import infer_cell_prefix, load_response_for_cell, find_existing_scores

state = json.load((REPO / 'docs' / 'research' / '_audit_20260507_remaining_work.json').open(encoding='utf-8'))

actionable_cells = []
non_actionable_cells = []

# Combine unrescued + never-attempted
all_remaining = []
for c in state['unrescued_cells']:
    all_remaining.append(dict(c))
for c in state['never_attempted_cells']:
    all_remaining.append({
        'subject': c['subject'], 'condition': c['condition'], 'judge': c['judge'],
        'manifest_pf': c['manifest_pf'], 'rescued': 0, 'still_failed': c['manifest_pf'],
        'never_attempted': True,
    })

for c in all_remaining:
    s, cond, j = c['subject'], c['condition'], c['judge']
    response_path, _ = infer_cell_prefix(s, cond)
    if not response_path or not response_path.exists():
        c['actionable'] = False
        c['reason'] = 'no_response_file'
        non_actionable_cells.append(c)
        continue
    responses = load_response_for_cell(response_path, cond)
    if not responses:
        c['actionable'] = False
        c['reason'] = 'no_responses_for_condition'
        non_actionable_cells.append(c)
        continue
    # If the cell was attempted, check overlap with backfill
    if not c.get('never_attempted'):
        bf_path = REPO / 'results' / '_s114_backfills' / f'{s}__{cond}__{j}.json'
        if bf_path.exists():
            try:
                rows = json.load(bf_path.open(encoding='utf-8'))
            except Exception:
                rows = []
        else:
            rows = []
        # Existing failures in backfill
        bf_failed_qids = [r['question_id'] for r in rows if r.get('parse_failure') or r.get('score') in (0, None)]
        bf_done_qids = {r['question_id'] for r in rows if not r.get('parse_failure') and r.get('score') is not None}
    else:
        bf_failed_qids = []
        bf_done_qids = set()

    # Check originating per-judge file for unsuccessful rows
    jfile, existing_scores = find_existing_scores(s, cond, j)
    pf_qids = []
    for qid, score in existing_scores.items():
        if score in (0, None) and qid not in bf_done_qids:
            pf_qids.append(qid)
    # Filter: must have response
    response_qids = set(responses.keys())
    actionable_qids = [q for q in pf_qids if q in response_qids]

    c['actionable_qids'] = actionable_qids
    c['n_actionable'] = len(actionable_qids)
    c['actionable'] = c['n_actionable'] > 0
    c['response_path'] = str(response_path.relative_to(REPO))
    c['judge_file'] = str(jfile.relative_to(REPO)) if jfile else None
    if c['actionable']:
        actionable_cells.append(c)
    else:
        c['reason'] = 'no_actionable_qids (all done or no response)'
        non_actionable_cells.append(c)

print(f'Actionable cells: {len(actionable_cells)}')
total_act_calls = sum(c['n_actionable'] for c in actionable_cells)
print(f'Total actionable judge calls remaining: {total_act_calls}')
print()
print('Top 30 actionable cells:')
for c in sorted(actionable_cells, key=lambda x: -x['n_actionable'])[:30]:
    print(f'  {c["subject"]:<22} {c["condition"]:<35} {c["judge"]:<14} n={c["n_actionable"]:>3}')

# Aggregate by judge
by_j = defaultdict(int)
for c in actionable_cells:
    by_j[c['judge']] += c['n_actionable']
print('\nActionable calls by judge:')
for j, n in sorted(by_j.items(), key=lambda x: -x[1]):
    print(f'  {j:<14} {n:>5}')

# Save
out = {
    'actionable_cells': actionable_cells,
    'non_actionable_cells': non_actionable_cells,
    'total_actionable_calls': total_act_calls,
    'by_judge': dict(by_j),
}
out_path = REPO / 'docs' / 'research' / '_audit_20260507_actionable.json'
out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')
print(f'\nWrote {out_path}')
