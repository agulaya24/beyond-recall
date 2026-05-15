"""Detailed breakdown: where are the 730 unrescued failures per primary judge?"""

import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent

state = json.load((REPO / 'docs' / 'research' / '_audit_20260507_remaining_work.json').open(encoding='utf-8'))

# Build per-judge cell breakdown
per_judge_cells = defaultdict(list)
for c in state['unrescued_cells']:
    per_judge_cells[c['judge']].append(c)
for c in state['never_attempted_cells']:
    per_judge_cells[c['judge']].append({
        'subject': c['subject'], 'condition': c['condition'], 'judge': c['judge'],
        'manifest_pf': c['manifest_pf'], 'rescued': 0,
        'still_failed': c['manifest_pf'], 'total_in_backfill': 0, 'never_attempted': True,
    })

PRIMARY = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']
print('Cells with remaining failures, by primary judge:')
for j in PRIMARY:
    cells = per_judge_cells[j]
    total_failed = sum(c['still_failed'] for c in cells)
    print(f'\n=== {j} ({total_failed} remaining failures across {len(cells)} cells) ===')
    for c in sorted(cells, key=lambda x: -x['still_failed']):
        na = ' [never attempted]' if c.get('never_attempted') else ''
        print(f'  {c["subject"]:<22} {c["condition"]:<35} failed={c["still_failed"]:>3}/{c["manifest_pf"]:>3}{na}')

print('\n--- gemini_flash 7-judge concern (top 30) ---')
for c in sorted(per_judge_cells['gemini_flash'], key=lambda x: -x['still_failed'])[:30]:
    na = ' [never attempted]' if c.get('never_attempted') else ''
    print(f'  {c["subject"]:<22} {c["condition"]:<35} failed={c["still_failed"]:>3}/{c["manifest_pf"]:>3}{na}')
