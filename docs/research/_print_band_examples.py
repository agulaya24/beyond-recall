"""Print 2-3 short-form examples from each band for qualitative reading."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parents[2]
POOL = str(REPO / "docs/research/_score_band_pool.json")
with open(POOL, "r", encoding="utf-8") as f:
    pool = json.load(f)

PICK = {
    "1.0-1.3": 3,
    "1.5-1.8": 3,
    "2.0-2.3": 3,
    "2.6-2.9": 3,
    "3.0-3.3": 4,  # extra — advisor said focus here
    "3.4-3.7": 3,
    "3.8-4.1": 3,
    "4.2-4.5": 3,
    "4.6-5.0": 3,
}

for band, n in PICK.items():
    recs = pool["bands"].get(band, [])
    if not recs:
        continue
    print("=" * 80)
    print(f"BAND {band}  (n sample={len(recs)})")
    print("=" * 80)
    for r in recs[:n]:
        print(f"\n--- {r['subject']} q{r['qid']} {r['condition']} | mean={r['mean_score']} scores={r['scores']} ---")
        print(f"Q: {r['question'][:280]}")
        print(f"GROUND TRUTH: {r['held_out'][:400]}")
        print(f"RESPONSE (first 900 chars):\n{r['response'][:900]}")
        print()
