"""Check hedging numbers vs paper claims."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / 'docs/research/hedging_analysis.json') as f:
    h = json.load(f)

print('Top-level keys:', list(h.keys()))
print()
for k in h.keys():
    if isinstance(h[k], dict) and 'hedged' in h[k]:
        d = h[k]
        print(f'{k}: hedged={d["hedged"]} total={d["total"]} rate={d["rate"]:.4f}')

# Paper §1.3 claims:
# Narrow rule: 28.8% (146/507) -> 1.4% (7/507) -> 0.0% (0/507) [C5 -> C2a -> C4a]
# Broad rule:  41.2% (209/507) -> 7.9% (40/507) -> 0.4% (2/507)
print('\nPaper claims (narrow rule):')
print('  C5: 28.8% (146/507)')
print('  C2a: 1.4% (7/507)')
print('  C4a: 0.0% (0/507)')
print('Paper claims (broader rule):')
print('  C5: 41.2% (209/507)')
print('  C2a: 7.9% (40/507)')
print('  C4a: 0.4% (2/507)')

# Look for broader rule
print('\n=== broader rule ===')
for k in ['C5_broad', 'C2a_broad', 'C4a_broad', 'broad_rule', 'broader_rule']:
    if k in h:
        print(f'  {k}:', h[k] if isinstance(h[k], (int, float, str)) else json.dumps(h[k])[:200])

# Print full structure (top-level values)
print('\n=== Full top-level keys+types ===')
for k, v in h.items():
    if isinstance(v, dict):
        sub = list(v.keys())
        print(f'  {k} (dict): subkeys={sub}')
    else:
        print(f'  {k}: {type(v).__name__} = {v if isinstance(v,(int,float,str)) else "..."}')

# Now look at secondary_metrics
print('\n=== secondary_metrics ===')
sm = h.get('secondary_metrics', {})
for k, v in sm.items():
    if isinstance(v, dict):
        print(f'\n{k}:')
        for k2, v2 in v.items():
            if isinstance(v2, dict):
                if 'hedged' in v2:
                    print(f'  {k2}: hedged={v2["hedged"]} total={v2["total"]} rate={v2["rate"]:.4f}')
                else:
                    print(f'  {k2}: {list(v2.keys())[:5]}')
            else:
                print(f'  {k2}: {v2}')
    else:
        print(f'{k}: {v}')
