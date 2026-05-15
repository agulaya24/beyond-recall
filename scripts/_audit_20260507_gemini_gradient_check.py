"""Check whether gemini_flash unrescued failures hit gradient conditions used in §4.6.2."""

import csv
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
INV = REPO / 'docs' / 'research' / 'parse_failure_inventory_20260507.csv'

GRADIENT_CONDS = {'C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                  'C4_factdump', 'C4a_full_facts_plus_spec'}

unrescued_gradient = defaultdict(int)
total_unrescued_gemini = 0

for r in csv.DictReader(INV.open(encoding='utf-8')):
    if r['judge'] not in ('gemini_flash', 'gemini_pro'):
        continue
    if r['s114_backfill_rescued'] == 'True':
        continue
    total_unrescued_gemini += 1
    if r['condition'] in GRADIENT_CONDS:
        key = (r['subject'], r['condition'], r['judge'])
        unrescued_gradient[key] += 1

print(f'Total unrescued gemini failures: {total_unrescued_gemini}')
print(f'Unrescued gemini failures on gradient conditions: {sum(unrescued_gradient.values())}')
print(f'Unique (subject, gradient_cond, judge) cells with unrescued gemini failures: {len(unrescued_gradient)}')
print()
if unrescued_gradient:
    print('Cells (top 30):')
    for (s, c, j), n in sorted(unrescued_gradient.items(), key=lambda x:-x[1])[:30]:
        print(f'  {s:<22} {c:<35} {j:<14} {n}')
else:
    print('NONE — gradient §4.6.2 coverage is clean')
