"""Recompute per-band variance statistics over the FULL pool (all 1,092 records),
not just the diversity-balanced samples. Also split Hamerton (6-judge) from global (3-judge).
"""
import json
import os
from collections import defaultdict
from statistics import mean, stdev

RESULTS_DIR = "C:/Users/Aarik/Anthropic/memory-study-repo/results"

# Rebuild full records list (same logic as _build_score_pool.py) but keep all records.
subjects = sorted([d for d in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, d))])

records = []
for s in subjects:
    sd = os.path.join(RESULTS_DIR, s)
    res_p = os.path.join(sd, "baselayer_results.json")
    jud_p = os.path.join(sd, "baselayer_judgments_merged.json")
    if not (os.path.exists(res_p) and os.path.exists(jud_p)):
        continue
    with open(res_p, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(jud_p, "r", encoding="utf-8") as f:
        judgments = json.load(f)

    qmap = {q["question_id"]: q for q in results}
    jmap = defaultdict(list)
    for j in judgments:
        if j.get("parse_failure"):
            continue
        sc = j.get("score")
        if sc is None:
            continue
        jmap[(j["question_id"], j["condition"])].append(sc)

    for (qid, cond), scores in jmap.items():
        if qid not in qmap:
            continue
        resp = qmap[qid].get("responses", {}).get(cond)
        if not resp:
            continue
        text = resp["text"] if isinstance(resp, dict) else str(resp)
        if not text:
            continue
        records.append(
            {
                "subject": s,
                "qid": qid,
                "condition": cond,
                "scores": scores,
                "mean_score": mean(scores),
                "n_judges": len(scores),
            }
        )

print(f"Total records: {len(records)}")

BANDS = [
    ("1.0-1.3", 1.0, 1.3),
    ("1.5-1.8", 1.5, 1.8),
    ("2.0-2.3", 2.0, 2.3),
    ("2.6-2.9", 2.6, 2.9),
    ("3.0-3.3", 3.0, 3.3),
    ("3.4-3.7", 3.4, 3.7),
    ("3.8-4.1", 3.8, 4.1),
    ("4.2-4.5", 4.2, 4.5),
    ("4.6-5.0", 4.6, 5.0),
]


def band_stats(recs, label):
    print(f"\n=== {label} (n={len(recs)}) ===")
    print(f"{'band':>10} {'n':>5} {'mean':>6} {'stdev':>6} {'range':>6} {'%>=2':>6} {'%>=3':>6} {'judges':>7}")
    for name, lo, hi in BANDS:
        in_band = [r for r in recs if lo <= r["mean_score"] <= hi]
        n = len(in_band)
        if n == 0:
            print(f"{name:>10} {n:>5} {'':>6} {'':>6} {'':>6} {'':>6} {'':>6} {'':>7}")
            continue
        stds = [stdev(r["scores"]) if len(r["scores"]) > 1 else 0 for r in in_band]
        rngs = [max(r["scores"]) - min(r["scores"]) for r in in_band]
        ge2 = sum(1 for x in rngs if x >= 2)
        ge3 = sum(1 for x in rngs if x >= 3)
        nj = in_band[0]["n_judges"]
        print(
            f"{name:>10} {n:>5} {mean(r['mean_score'] for r in in_band):>6.3f} "
            f"{mean(stds):>6.3f} {mean(rngs):>6.3f} "
            f"{100*ge2/n:>5.1f}% {100*ge3/n:>5.1f}% {nj:>7}"
        )


# All subjects together (but normalized to 3 judges only for comparability)
# Hamerton has 6-judge merged records; global has 3-judge merged. Check n_judges distribution.
from collections import Counter
nj_counts = Counter((r["subject"], r["n_judges"]) for r in records)
print("\nJudge-count distribution (subject, n_judges): top entries")
for (s, n), c in sorted(nj_counts.items())[:25]:
    print(f"  {s} n_judges={n}: {c}")

# Split Hamerton from global
hamerton = [r for r in records if r["subject"] == "hamerton"]
global_recs = [r for r in records if r["subject"].startswith("global_")]

band_stats(records, "ALL RECORDS (mixed judge counts)")
band_stats(global_recs, "GLOBAL ONLY (3 judges per record)")
band_stats(hamerton, "HAMERTON ONLY (6 judges per record)")

# Also do Hamerton with only 3 judges (subsample) to make apples-to-apples
import random
random.seed(7)
hamerton_3j = [
    {
        **r,
        "scores": random.sample(r["scores"], 3) if len(r["scores"]) >= 3 else r["scores"],
        "n_judges": 3,
    }
    for r in hamerton
]
for r in hamerton_3j:
    r["mean_score"] = mean(r["scores"])
band_stats(hamerton_3j, "HAMERTON subsampled to 3 judges")
