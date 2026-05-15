"""Debug Hamerton load."""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from recompute_5judge_primary import load_hamerton_judgments

rows = load_hamerton_judgments()
print(f'Hamerton rows: {len(rows)}')
if rows:
    print(f'Sample row: {rows[0]}')

from collections import Counter
conds = Counter(r.get('condition') for r in rows)
print(f'Conditions: {dict(conds)}')
judges = Counter(r.get('judge') for r in rows)
print(f'Judges: {dict(judges)}')
