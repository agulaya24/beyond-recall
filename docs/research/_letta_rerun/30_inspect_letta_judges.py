"""Inspect the Letta stateful+Haiku judgments to determine judge coverage and mean score."""
import json
import os
from collections import defaultdict

# This script depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
BASE = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results")

for subject in ("ebers", "babur"):
    print(f"\n===== {subject} =====")
    sub_dir = os.path.join(BASE, f"global_{subject}")
    judges = {}
    for judge_name in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
        path = os.path.join(sub_dir, f"letta_memory_haiku_judgments_{judge_name}.json")
        if not os.path.exists(path):
            print(f"  {judge_name}: MISSING")
            continue
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        # Inspect structure
        # May be {judgments: [...]} or list
        if isinstance(d, dict):
            items = d.get("judgments") or d.get("results") or d.get("scores") or d
            if isinstance(items, dict):
                # Already mapping
                scores = items
            elif isinstance(items, list):
                scores = {it.get("question_id"): it.get("score", it.get("judgment", 0)) for it in items}
            else:
                scores = None
        elif isinstance(d, list):
            scores = {it.get("question_id"): it.get("score", it.get("judgment", 0)) for it in d}
        else:
            scores = None

        if scores is None:
            print(f"  {judge_name}: UNKNOWN STRUCTURE")
            continue
        # non-zero count
        vals = [v for v in scores.values() if isinstance(v, (int, float)) and v >= 1]
        if not vals:
            print(f"  {judge_name}: no valid scores (top keys={list(d.keys()) if isinstance(d, dict) else 'list'})")
        else:
            mean = sum(vals) / len(vals)
            print(f"  {judge_name}: n={len(vals)} mean={mean:.3f}")
        judges[judge_name] = scores

    # Aggregate 6-judge mean (no gemini_pro)
    six_names = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash"]
    qids = set()
    for j in six_names:
        if j in judges and isinstance(judges[j], dict):
            qids.update(judges[j].keys())
    print(f"\n  Six-judge computation over {len(qids)} qids")
    all_scores = []
    for qid in qids:
        for j in six_names:
            if j not in judges:
                continue
            s = judges[j].get(qid, 0)
            if isinstance(s, (int, float)) and s >= 1:
                all_scores.append(s)
    if all_scores:
        print(f"    6-judge all-score mean: {sum(all_scores)/len(all_scores):.3f} (n={len(all_scores)} scores)")

    # Also 7-judge
    seven_names = six_names + ["gemini_pro"]
    all_scores7 = []
    for qid in qids:
        for j in seven_names:
            if j not in judges:
                continue
            s = judges[j].get(qid, 0)
            if isinstance(s, (int, float)) and s >= 1:
                all_scores7.append(s)
    if all_scores7:
        print(f"    7-judge all-score mean: {sum(all_scores7)/len(all_scores7):.3f} (n={len(all_scores7)} scores)")

    # Per-question mean (average of valid judges, then mean over questions)
    for name_set, names in [("6-judge", six_names), ("7-judge", seven_names)]:
        pq = []
        for qid in qids:
            jscores = []
            for j in names:
                if j not in judges:
                    continue
                s = judges[j].get(qid, 0)
                if isinstance(s, (int, float)) and s >= 1:
                    jscores.append(s)
            if jscores:
                pq.append(sum(jscores)/len(jscores))
        if pq:
            print(f"    {name_set} per-question-mean: {sum(pq)/len(pq):.3f} (n_q={len(pq)})")
