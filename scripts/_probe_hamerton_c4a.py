import json
from pathlib import Path
D = Path('C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton')
# List all conditions across files
all_conds = set()
for fp in D.glob('*.json'):
    try:
        data = json.load(open(fp))
    except Exception:
        continue
    if isinstance(data, list) and data and isinstance(data[0], dict):
        conds = set(r.get('condition') for r in data if isinstance(r, dict))
        for c in conds:
            if c and ('C4a' in c or 'facts_plus_spec' in c or '4a' in str(c)):
                print(f'{fp.name}: found condition "{c}" (n_records for this cond: {sum(1 for r in data if r.get("condition")==c)})')
        all_conds.update(x for x in conds if x)
print('All unique conditions:', sorted(all_conds))
