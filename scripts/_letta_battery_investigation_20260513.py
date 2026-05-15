# Scratch: Letta battery investigation 2026-05-13 -- PART G
# Haiku-only check on the Letta battery (battery.json 40q): main-study C2a/C4_factdump
# vs Letta block haiku score, to see if even a 1-judge same-battery comparison exists.
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import json, os
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MEMSYS = os.path.join(os.environ.get("MEMORY_SYSTEM_ROOT", ""), "data", "experiments", "memory_systems")
def load(p): return json.load(io.open(p, encoding="utf-8"))

# Ebers/Babur: judgments.json is haiku-only on the 40q battery
for s in ["ebers", "babur"]:
    print("="*60); print(s, "- haiku-only, 40q Letta battery (battery.json)"); print("="*60)
    j = load(os.path.join(REPO, f"results/global_{s}/judgments.json"))
    bycond = defaultdict(list)
    for r in j:
        bycond[r["condition"]].append(r["haiku_score"])
    for c, scores in sorted(bycond.items()):
        print(f"  {c}: haiku mean = {sum(scores)/len(scores):.4f}  (n={len(scores)})")
    # Letta block haiku score on same battery -- from canonical 5judge file per-judge
    fj = load(os.path.join(REPO, "docs/research/_letta_rerun/5judge_primary_results.json"))
    for row in fj["rows"]:
        if row["subject"].lower().startswith(s[:4]):
            print(f"  Letta block haiku (per-judge): {row['letta_per_judge'].get('haiku')}")
            print(f"  BL unified-brief haiku (per-judge): {row['bl_per_judge'].get('haiku')}")
    print()

# Confirm: does the 5judge_primary_results.json BL side trace to unified brief?
print("5judge_primary_results.json metadata:")
fj = load(os.path.join(REPO, "docs/research/_letta_rerun/5judge_primary_results.json"))
for k,v in fj.items():
    if k != "rows":
        print(f"  {k}: {v}")
print("  row[0] keys:", list(fj["rows"][0].keys()))
print("  row[0]:", json.dumps(fj["rows"][0], ensure_ascii=False)[:500])

# What battery does the paper gradient (Table 4.4) cite? check DATA_REFERENCE gradient section
print()
print("DATA_REFERENCE.md gradient/Table 4.4 battery reference:")
dr = io.open(os.path.join(REPO, "docs/DATA_REFERENCE.md"), encoding="utf-8").read()
import re
for m in re.finditer(r"(?i)(ebers|babur|battery_v2|battery\.json|gradient|C2a)", dr):
    pass
# just print lines mentioning battery_v2 or 80-question
for ln in dr.splitlines():
    if "battery_v2" in ln.lower() or "80-question" in ln.lower() or "80 question" in ln.lower() or "battery.json" in ln.lower():
        print("  ", ln.strip()[:160])
