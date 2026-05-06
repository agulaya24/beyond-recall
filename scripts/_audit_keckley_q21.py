"""Audit script: re-derive per-system Q21 deltas (C1 retrieval-only vs C3 retrieval+spec)
for §4.4.3 case study (Keckley Q21).

Paper claims (line 1305-1311):
  Supermemory:    -2.0  (retrieval-only ~3.4)
  Base Layer:     -2.2  (retrieval-only ~3.6)
  Letta:          +0.4  (retrieval-only <= 1.4)
  Mem0:           +0.2  (retrieval-only <= 1.4)
  Zep:            +0.2  (retrieval-only <= 1.4)
"""
import json
from pathlib import Path
from statistics import mean

RESULTS = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley")
TARGET_QID = 21
PRIMARY_JUDGES = {"haiku", "sonnet", "opus", "gpt4o", "gpt54"}  # 5-judge primary panel

# (system_name, judgments_file, c1_label, c3_label)
SYSTEMS = [
    ("Supermemory",  "supermemory_judgments_merged.json",  "C1_supermemory", "C3_supermemory"),
    ("Base Layer",   "baselayer_judgments_merged.json",    "C1_baselayer",   "C3_baselayer"),
    ("Letta",        "letta_judgments_merged.json",        "C1_letta",       "C3_letta"),
    ("Mem0",         "mem0_judgments_merged.json",         "C1_mem0",        "C3_mem0"),
    ("Zep",          "zep_judgments_merged.json",          "C1_zep",         "C3_zep"),
]

def main():
    print(f"Keckley Q21 — per-system C3 vs C1 (5-judge primary panel)")
    print(f"{'System':<14} {'C1 mean':>10} {'C3 mean':>10} {'Delta':>10} {'n_judges':>10}")
    print("-" * 60)
    for sys_name, fname, c1_label, c3_label in SYSTEMS:
        fpath = RESULTS / fname
        if not fpath.exists():
            print(f"{sys_name:<14} (FILE MISSING: {fname})")
            continue
        data = json.loads(fpath.read_text(encoding="utf-8"))
        c1_scores, c3_scores = [], []
        c1_judges, c3_judges = set(), set()
        for j in data:
            if j.get("question_id") != TARGET_QID:
                continue
            if j.get("parse_failure"):
                continue
            score = j.get("score")
            if score is None:
                continue
            judge = j.get("judge", "unknown")
            if judge not in PRIMARY_JUDGES:
                continue
            cond = j.get("condition")
            if cond == c1_label:
                c1_scores.append(score)
                c1_judges.add(judge)
            elif cond == c3_label:
                c3_scores.append(score)
                c3_judges.add(judge)
        if not c1_scores or not c3_scores:
            print(f"{sys_name:<14} (NO MATCH: c1={len(c1_scores)} c3={len(c3_scores)})")
            continue
        c1_mean = mean(c1_scores)
        c3_mean = mean(c3_scores)
        delta = c3_mean - c1_mean
        n_str = f"{len(c1_scores)}/{len(c3_scores)}"
        print(f"{sys_name:<14} {c1_mean:>10.3f} {c3_mean:>10.3f} {delta:>+10.3f} {n_str:>10}")

if __name__ == "__main__":
    main()
