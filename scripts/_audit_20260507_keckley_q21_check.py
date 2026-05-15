"""Check Keckley Q21 across all judges for both C1_baselayer and C3_baselayer."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
print('=== Keckley Q21 baselayer judge cells ===')
for judge in ['haiku','sonnet','opus','gpt4o','gpt54','gemini_flash','gemini_pro']:
    p = REPO / f'results/global_keckley/baselayer_judgments_{judge}.json'
    if not p.exists():
        print(f'{judge}: FILE MISSING')
        continue
    rows = json.load(p.open(encoding='utf-8'))
    q21_c1 = [r for r in rows if r.get('question_id')==21 and r.get('condition')=='C1_baselayer']
    q21_c3 = [r for r in rows if r.get('question_id')==21 and r.get('condition')=='C3_baselayer']
    print(f'{judge}: C1={q21_c1} C3={q21_c3}')

# Check backfill
print('\n=== Keckley Q21 backfills ===')
for judge in ['haiku','sonnet','opus','gpt4o','gpt54','gemini_flash','gemini_pro']:
    for cond in ['C1_baselayer','C3_baselayer']:
        p = REPO / f'results/_s114_backfills/global_keckley__{cond}__{judge}.json'
        if not p.exists():
            continue
        rows = json.load(p.open(encoding='utf-8'))
        q21 = [r for r in rows if r.get('question_id')==21]
        if q21:
            print(f'{judge}/{cond}: {q21}')

# Check the response for Q21
print('\n=== Keckley Q21 responses ===')
p = REPO / 'results/global_keckley/baselayer_results.json'
data = json.load(p.open(encoding='utf-8'))
for q in data:
    if q.get('question_id') == 21:
        print('Q21 found, conditions present:', list(q.get('responses', {}).keys()))
        for cond in ['C1_baselayer', 'C3_baselayer']:
            r = q.get('responses', {}).get(cond)
            if r:
                print(f'  {cond}: text len={len(r.get("text",""))}, first 100={r.get("text","")[:100]!r}')
        break
