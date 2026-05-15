"""Compute Hamerton C2a per-judge and per-question-subset means."""
import json
import os
from collections import defaultdict

# This script depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
base = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results", "run_fullstack_hamerton_20260411_231237")

# Combined C2a scores by judge
with open(f"{base}\\analysis\\judgments.json", encoding="utf-8") as f:
    data_main = json.load(f)
with open(f"{base}\\analysis\\gemini_pro_judgments.json", encoding="utf-8") as f:
    data_gp = json.load(f)
with open(f"{base}\\analysis\\gpt54_judgments.json", encoding="utf-8") as f:
    data_gpt54 = json.load(f)

# Build per-(qid, judge) score map for C2a_full_spec
scores = defaultdict(dict)  # qid -> judge -> score
for e in data_main:
    if e["condition"] != "C2a_full_spec":
        continue
    qid = e["question_id"]
    if "haiku_score" in e:
        scores[qid]["haiku"] = e["haiku_score"]
    if "gemini_score" in e:
        scores[qid]["gemini_flash"] = e["gemini_score"]
for e in data_gp:
    if e["condition"] != "C2a_full_spec":
        continue
    qid = e["question_id"]
    scores[qid]["gemini_pro"] = e["gemini_pro_score"]
for e in data_gpt54:
    if e["condition"] != "C2a_full_spec":
        continue
    qid = e["question_id"]
    scores[qid]["gpt54"] = e["gpt54_score"]

print(f"unique qids in C2a_full_spec: {len(scores)}")
print(f"sample qid: {sorted(scores.keys())[:5]}")
# judges per qid
from collections import Counter
judge_counts = Counter(tuple(sorted(v.keys())) for v in scores.values())
print(f"judge-set distribution: {judge_counts}")

# Load the Letta battery qids
with open(rf"{base}\\letta_memory_haiku_results.json", encoding="utf-8") as f:
    letta = json.load(f)
letta_qids = set(r["question_id"] for r in letta["results"])
print(f"Letta qids: n={len(letta_qids)}, sample={sorted(letta_qids)[:5]}")

# Intersection
inter = letta_qids & set(scores.keys())
print(f"intersection: {len(inter)}")

# Per-judge mean on the intersection, for C2a
available_judges = ["haiku", "gemini_flash", "gemini_pro", "gpt54"]
# where are sonnet, opus, gpt4o for this C2a?
