"""Debug: dump all Base Layer judgments for Keckley Q21."""
import json
from pathlib import Path
from collections import defaultdict

RESULTS = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley")
TARGET_QID = 21

print("=== Base Layer judgments for Keckley Q21 ===")
fpath = RESULTS / "baselayer_judgments_merged.json"
data = json.loads(fpath.read_text(encoding="utf-8"))
by_cond = defaultdict(list)
for j in data:
    if j.get("question_id") != TARGET_QID:
        continue
    by_cond[j.get("condition")].append(j)

for cond, entries in sorted(by_cond.items()):
    print(f"\n{cond}:")
    for j in entries:
        judge = j.get("judge", "?")
        score = j.get("score")
        parse_fail = j.get("parse_failure", False)
        print(f"  judge={judge:<14} score={score} parse_fail={parse_fail}")

# Also check separate per-judge files
print("\n=== Per-judge files ===")
for judge in ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]:
    fname = f"baselayer_judgments_{judge}.json"
    fpath = RESULTS / fname
    if not fpath.exists():
        print(f"{judge}: file missing")
        continue
    data = json.loads(fpath.read_text(encoding="utf-8"))
    rows = [j for j in data if j.get("question_id") == TARGET_QID]
    for j in rows:
        cond = j.get("condition")
        score = j.get("score")
        parse_fail = j.get("parse_failure", False)
        print(f"  {judge:<10} cond={cond:<14} score={score} parse_fail={parse_fail}")
