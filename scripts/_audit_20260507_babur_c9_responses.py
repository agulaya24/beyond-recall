"""Inspect Babur C9 response shape directly."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
p = REPO / 'results' / 'global_babur' / 'c8_c9_results.json'
data = json.load(p.open(encoding='utf-8'))

print(f'Q1 keys: {list(data[0].keys())}')
print(f'Q1 has responses: {list(data[0].get("responses", {}).keys())}')
for cond in ['C8_raw_corpus', 'C9_raw_corpus_plus_spec']:
    r = data[0].get('responses', {}).get(cond)
    if r is None:
        print(f'  {cond}: None')
        continue
    print(f'\n=== {cond} ===')
    if isinstance(r, dict):
        print(f'  keys: {list(r.keys())}')
        text = r.get('text', '')
        print(f'  text len: {len(text)}')
        print(f'  text first 500: {(text[:500] or "").encode("ascii", "replace").decode("ascii")!r}')
    else:
        print(f'  raw: {r[:500]}')

# Check held_out_passage existence
print(f'\nQ1 has held_out_passage: {"held_out_passage" in data[0]}')
print(f'Q1 keys: {list(data[0].keys())}')

# Check what the failure mode is in the existing per-judge file
print('\nPer-judge C9 row for Q1, haiku:')
pj = REPO / 'results' / 'global_babur' / 'c8_c9_judgments_haiku.json'
rows = json.load(pj.open(encoding='utf-8'))
c9_q1 = [r for r in rows if r.get('question_id')==1 and r.get('condition')=='C9_raw_corpus_plus_spec']
for r in c9_q1:
    print(json.dumps(r, indent=2)[:800])
