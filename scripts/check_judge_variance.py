"""Check inter-judge disagreement variance on similar-score (|delta| <= 0.3) pairs
across the 9 low-baseline subjects, to validate Pattern 5 in the paired analysis.
"""
import json
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo/results")
SUBJECTS = ["sunity_devee", "ebers", "hamerton", "fukuzawa", "seacole",
            "bernal_diaz", "keckley", "yung_wing", "babur"]

similar_pairs = []

for subj in SUBJECTS:
    for p in [ROOT / f"global_{subj}", ROOT / subj]:
        jpath = p / "supermemory_judgments_merged.json"
        if jpath.exists():
            break
    else:
        continue
    with open(jpath, "r", encoding="utf-8") as f:
        judgments = json.load(f)

    by_q: dict = {}
    for j in judgments:
        if j.get("parse_failure"): continue
        s = j.get("score")
        if s is None: continue
        qid = j["question_id"]
        cond = j["condition"]
        judge = j["judge"]
        by_q.setdefault(qid, {"C1": {}, "C3": {}})
        if cond == "C1_supermemory":
            by_q[qid]["C1"][judge] = s
        elif cond == "C3_supermemory":
            by_q[qid]["C3"][judge] = s

    for qid, d in by_q.items():
        if not d["C1"] or not d["C3"]: continue
        common_judges = set(d["C1"]) & set(d["C3"])
        if len(common_judges) < 3: continue
        c1_mean = mean(d["C1"][j] for j in common_judges)
        c3_mean = mean(d["C3"][j] for j in common_judges)
        delta = c3_mean - c1_mean
        if abs(delta) <= 0.3:
            # Per-judge delta
            per_judge_deltas = {j: d["C3"][j] - d["C1"][j] for j in common_judges}
            # How many judges flipped direction?
            ups = sum(1 for v in per_judge_deltas.values() if v > 0)
            downs = sum(1 for v in per_judge_deltas.values() if v < 0)
            same = sum(1 for v in per_judge_deltas.values() if v == 0)
            range_ = max(per_judge_deltas.values()) - min(per_judge_deltas.values())
            similar_pairs.append({
                "subject": subj, "qid": qid,
                "c1_mean": round(c1_mean, 2), "c3_mean": round(c3_mean, 2),
                "delta_mean": round(delta, 2),
                "judges_up": ups, "judges_down": downs, "judges_same": same,
                "per_judge_range": range_,
                "per_judge": {k: int(v) for k, v in per_judge_deltas.items()},
            })

# Summaries
print(f"Total similar-score pairs (|d|<=0.3): {len(similar_pairs)}\n")

# How many pairs have at least one judge going each way?
splits = sum(1 for p in similar_pairs if p["judges_up"] >= 1 and p["judges_down"] >= 1)
print(f"Pairs where at least one judge went up AND at least one went down: {splits} ({100*splits/len(similar_pairs):.1f}%)")

# Distribution of per-judge range
ranges = [p["per_judge_range"] for p in similar_pairs]
print(f"Per-judge delta range (max - min across judges for same question):")
print(f"  mean={mean(ranges):.2f}, median={sorted(ranges)[len(ranges)//2]}, max={max(ranges)}")
print(f"  Pairs with range >= 2: {sum(1 for r in ranges if r >= 2)} ({100*sum(1 for r in ranges if r >= 2)/len(ranges):.1f}%)")
print(f"  Pairs with range >= 3: {sum(1 for r in ranges if r >= 3)} ({100*sum(1 for r in ranges if r >= 3)/len(ranges):.1f}%)")
print(f"  Pairs with range >= 4: {sum(1 for r in ranges if r >= 4)} ({100*sum(1 for r in ranges if r >= 4)/len(ranges):.1f}%)")

# Show the 5 most-disagreed pairs
print("\nTop 5 most disagreed-about similar-score pairs:")
for p in sorted(similar_pairs, key=lambda x: -x["per_judge_range"])[:5]:
    print(f"  {p['subject']} q{p['qid']}: C1={p['c1_mean']} C3={p['c3_mean']} d={p['delta_mean']:+.2f} "
          f"range={p['per_judge_range']} per-judge={p['per_judge']}")
