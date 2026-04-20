"""Verify claims in mem0_letta_zep_c1_vs_c3_analysis.md.

1. Zep/Seacole Q2 = +4.00 is largest single-question swing in this analysis.
2. Letta duplicate-fact pattern quantification (avg unique vs total in top-10).
"""
import json
from collections import Counter
from statistics import mean
from pathlib import Path

ROOT = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results")

# ----- 1. Max absolute swing per subject per system -----
SYS_SUBJ = {
    "mem0":  ["ebers", "yung_wing", "sunity_devee", "keckley"],
    "letta": ["ebers", "hamerton",  "sunity_devee", "keckley"],
    "zep":   ["ebers", "seacole",   "bernal_diaz",  "keckley"],
}

print("=== Largest absolute per-question delta across all 12 (sys, subj) ===")
all_swings = []
for system, subjects in SYS_SUBJ.items():
    for subj in subjects:
        cand = [ROOT / f"global_{subj}", ROOT / subj]
        sdir = next((d for d in cand if (d / f"{system}_results.json").exists()), None)
        if sdir is None: continue
        with open(sdir / f"{system}_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        with open(sdir / f"{system}_judgments_merged.json", "r", encoding="utf-8") as f:
            judgments = json.load(f)
        by_q = {}
        for entry in results:
            qid = entry["question_id"]
            by_q[qid] = {"c1": {}, "c3": {}}
        for j in judgments:
            qid = j["question_id"]
            if qid not in by_q or j.get("score") is None: continue
            cond = j["condition"]
            if cond == f"C1_{system}":
                by_q[qid]["c1"][j["judge"]] = j["score"]
            elif cond == f"C3_{system}":
                by_q[qid]["c3"][j["judge"]] = j["score"]
        for qid, scores in by_q.items():
            if scores["c1"] and scores["c3"]:
                c1m = mean(scores["c1"].values())
                c3m = mean(scores["c3"].values())
                all_swings.append((system, subj, qid, c1m, c3m, c3m - c1m))

# Top 5 positive and top 5 negative
all_swings.sort(key=lambda x: -x[5])
print("\nTop 5 POSITIVE swings:")
for s, subj, qid, c1, c3, d in all_swings[:5]:
    print(f"  {s:5s} {subj:14s} Q{qid:3d}  C1={c1:.2f}  C3={c3:.2f}  d={d:+.2f}")
print("\nTop 5 NEGATIVE swings:")
for s, subj, qid, c1, c3, d in all_swings[-5:]:
    print(f"  {s:5s} {subj:14s} Q{qid:3d}  C1={c1:.2f}  C3={c3:.2f}  d={d:+.2f}")

# ----- 2. Letta duplicate-fact quantification -----
print("\n\n=== Letta fact duplication in top-10 retrieval ===")
for subj in ["ebers", "hamerton", "sunity_devee", "keckley"]:
    cand = [ROOT / f"global_{subj}", ROOT / subj]
    sdir = next((d for d in cand if (d / "letta_results.json").exists()), None)
    if sdir is None: continue
    with open(sdir / "letta_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    total_len = 0
    unique_len = 0
    n_questions = 0
    max_repeat_counts = []
    for entry in data:
        facts = entry.get("retrieval", {}).get("facts", [])
        if not facts: continue
        n_questions += 1
        total_len += len(facts)
        unique_len += len(set(facts))
        # most common fact occurrence count
        c = Counter(facts)
        max_repeat_counts.append(max(c.values()))
    avg_unique = unique_len / n_questions if n_questions else 0
    avg_total = total_len / n_questions if n_questions else 0
    dedup_ratio = unique_len / total_len if total_len else 0
    avg_max_rep = mean(max_repeat_counts) if max_repeat_counts else 0
    print(f"  letta/{subj:14s}  avg_total={avg_total:.1f}  avg_unique={avg_unique:.1f}  dedup_ratio={dedup_ratio:.2f}  avg_max_same_fact_count={avg_max_rep:.2f}")

# For comparison, check mem0 and zep dedup
print("\n=== Mem0 fact duplication (should be ~1.0 dedup) ===")
for subj in ["ebers", "yung_wing", "sunity_devee", "keckley"]:
    cand = [ROOT / f"global_{subj}", ROOT / subj]
    sdir = next((d for d in cand if (d / "mem0_results.json").exists()), None)
    if sdir is None: continue
    with open(sdir / "mem0_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    total_len = unique_len = n = 0
    for entry in data:
        facts = entry.get("retrieval", {}).get("facts", [])
        if not facts: continue
        n += 1
        total_len += len(facts)
        unique_len += len(set(facts))
    print(f"  mem0/{subj:14s}  dedup_ratio={unique_len/total_len if total_len else 0:.2f}  avg_len={total_len/n if n else 0:.1f}")
