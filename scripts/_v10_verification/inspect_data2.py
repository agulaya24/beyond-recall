"""Inspect more data for hamerton."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path('C:/Users/Aarik/Anthropic/memory-study-repo')

# 1) hamerton: aggregate all judgment files (per-judge files for C5/C2a/C2c/C4/C4a)
print('=== hamerton: scan per-judge files for global-style conditions ===')
# first look for hamerton judgments_v2.json
fv2 = ROOT / 'results/hamerton/judgments_v2.json'
print('Has judgments_v2.json?', fv2.exists())
# look for gpt4o_judgments.json etc
for fname in ['gpt4o_judgments.json', 'opus_judgments.json', 'sonnet_judgments.json', 'gpt54_judgments.json', 'gemini_pro_judgments.json']:
    p = ROOT / 'results/hamerton' / fname
    if p.exists():
        with open(p) as f:
            d = json.load(f)
        if isinstance(d, list):
            cs = set()
            for r in d:
                if isinstance(r, dict):
                    cs.add(r.get('condition','?'))
            print(f'{fname}: {len(d)} records, conditions: {sorted(cs)}, first: {d[0] if d else None}')

# 2) judgments.json structure for hamerton more deeply
print('\n=== hamerton/judgments.json detail ===')
with open(ROOT / 'results/hamerton/judgments.json') as f:
    h = json.load(f)
# count per condition
cnt_cond = defaultdict(int)
for r in h:
    cnt_cond[r.get('condition','?')] += 1
print('Per-cond count:', dict(cnt_cond))
# unique question_ids per condition
qids = defaultdict(set)
for r in h:
    qids[r.get('condition','?')].add(r.get('question_id'))
for k, v in qids.items():
    print(f'  {k}: {len(v)} unique qids, range {min(v)}-{max(v)}')
# fields available
fields = set()
for r in h:
    fields.update(r.keys())
print('All fields:', sorted(fields))
print('Sample 3 records:')
for r in h[:3]:
    print('  ', r)

# 3) hamerton fullstack_haiku.json
print('\n=== hamerton/fullstack_haiku.json ===')
with open(ROOT / 'results/hamerton/fullstack_haiku.json') as f:
    fs = json.load(f)
print('Type:', type(fs).__name__)
if isinstance(fs, dict):
    print('Keys:', list(fs.keys())[:15])
    for k in list(fs.keys())[:3]:
        v = fs[k]
        print(f'  {k}: type {type(v).__name__}', f'len {len(v)}' if hasattr(v,'__len__') else '')
elif isinstance(fs, list):
    print('Len:', len(fs))
    if fs: print('First:', fs[0])

# 4) hamerton judgments_harmonized
print('\n=== hamerton/judgments_harmonized.json ===')
fh = ROOT / 'results/hamerton/judgments_harmonized.json'
if fh.exists():
    with open(fh) as f:
        jh = json.load(f)
    print('Type:', type(jh).__name__)
    if isinstance(jh, list):
        print('Len:', len(jh))
        if jh: print('First:', jh[0])
        # collect conds + judges
        cs, js = set(), set()
        for r in jh:
            if isinstance(r,dict):
                cs.add(r.get('condition','?'))
                js.add(r.get('judge','?'))
        print('Conds:', sorted(cs))
        print('Judges:', sorted(js))

# 5) results.json hamerton
print('\n=== hamerton/results.json structure ===')
with open(ROOT / 'results/hamerton/results.json') as f:
    rh = json.load(f)
print('Type:', type(rh).__name__)
if isinstance(rh, dict):
    print('Keys:', list(rh.keys())[:15])
elif isinstance(rh, list):
    print('Len:', len(rh))
    if rh: print('First keys:', list(rh[0].keys()))
