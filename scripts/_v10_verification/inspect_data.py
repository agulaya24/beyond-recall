"""Inspect data file structure for v10 verification."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# 1) Inspect global ebers judgments_v2
with open(ROOT / 'results/global_ebers/judgments_v2.json') as f:
    data = json.load(f)
print('=== global_ebers/judgments_v2.json ===')
print('Type:', type(data).__name__, 'Total records:', len(data))
judges = set()
conditions = set()
for r in data:
    judges.add(r['judge'])
    conditions.add(r['condition'])
print('Judges:', sorted(judges))
print('Conditions:', sorted(conditions))
print('First record:', data[0])
# count per condition x judge
cnt = defaultdict(int)
for r in data:
    cnt[(r['condition'], r['judge'])] += 1
print('\nCounts per (condition, judge) (first 30):')
for k in sorted(cnt.keys())[:30]:
    print(f'  {k}: {cnt[k]}')

# 2) Inspect hamerton judgments
print('\n=== hamerton/judgments.json ===')
with open(ROOT / 'results/hamerton/judgments.json') as f:
    h_data = json.load(f)
print('Type:', type(h_data).__name__)
if isinstance(h_data, list):
    print('Total records:', len(h_data))
    print('First record:', h_data[0])
    h_judges = set(); h_conds = set()
    for r in h_data:
        if isinstance(r, dict):
            h_judges.add(r.get('judge', '?'))
            h_conds.add(r.get('condition', '?'))
    print('Judges:', sorted(h_judges))
    print('Conditions:', sorted(h_conds))
elif isinstance(h_data, dict):
    print('Top keys:', list(h_data.keys())[:20])

# 3) Inspect a memory-system-specific judgments file for hamerton
print('\n=== hamerton/baselayer_judgments_haiku.json ===')
with open(ROOT / 'results/hamerton/baselayer_judgments_haiku.json') as f:
    bl = json.load(f)
print('Type:', type(bl).__name__)
if isinstance(bl, list):
    print('Total:', len(bl))
    print('First:', bl[0])
    conds = set()
    for r in bl:
        conds.add(r.get('condition', '?'))
    print('Conds:', sorted(conds))
elif isinstance(bl, dict):
    print('keys:', list(bl.keys())[:20])

# 4) c8_c9 judgments for hamerton
print('\n=== hamerton/c8_c9_judgments_haiku.json ===')
with open(ROOT / 'results/hamerton/c8_c9_judgments_haiku.json') as f:
    cc = json.load(f)
print('Type:', type(cc).__name__)
if isinstance(cc, list):
    print('Total:', len(cc))
    if cc: print('First:', cc[0])
    conds = set()
    for r in cc:
        if isinstance(r, dict):
            conds.add(r.get('condition', '?'))
    print('Conds:', sorted(conds))
