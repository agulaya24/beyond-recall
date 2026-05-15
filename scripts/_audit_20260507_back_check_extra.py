"""Add extra back-checks: 5 §4.4.1 memory-system aggregate cells + 5 §4.5 Letta cells."""

import csv
import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
EMIT_DIR = REPO / 'docs' / 'research' / 'v11_emit'
BACKFILL_DIR = RESULTS / '_s114_backfills'

m = json.load((EMIT_DIR / '4_4_1_memory_systems.json').open(encoding='utf-8'))
claims = m['claims']
print(f'4.4.1 total: {len(claims)}')
print('Keys (first 20):')
for k in list(claims.keys())[:20]:
    c = claims[k]
    v = c.get('value')
    n = c.get('n')
    print(f'  {k}: value={v}, n={n}')

l = json.load((EMIT_DIR / '4_5_letta.json').open(encoding='utf-8'))
claims_l = l['claims']
print(f'\n4.5 total: {len(claims_l)}')
print('Keys (first 20):')
for k in list(claims_l.keys())[:20]:
    c = claims_l[k]
    v = c.get('value')
    n = c.get('n')
    print(f'  {k}: value={v}, n={n}')
