"""Build cross-subject pool of (response_text, mean_judge_score) tuples banded by score range.

Writes _score_band_pool.json in same directory for downstream qualitative read.
"""
import json, os, sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

REPO = Path(__file__).resolve().parents[2]
RESULTS_DIR = str(REPO / "results")

# subjects folder list
subjects = []
for d in sorted(os.listdir(RESULTS_DIR)):
    full = os.path.join(RESULTS_DIR, d)
    if not os.path.isdir(full):
        continue
    subjects.append(d)

print(f"Found {len(subjects)} subject directories", file=sys.stderr)

# For each subject, load baselayer_results.json + baselayer_judgments_merged.json
# Build (subject, question_id, condition, question, held_out, response_text, scores_list, mean_score) records.
records = []
for s in subjects:
    sd = os.path.join(RESULTS_DIR, s)
    res_p = os.path.join(sd, "baselayer_results.json")
    jud_p = os.path.join(sd, "baselayer_judgments_merged.json")
    if not (os.path.exists(res_p) and os.path.exists(jud_p)):
        continue
    try:
        with open(res_p, "r", encoding="utf-8") as f:
            results = json.load(f)
        with open(jud_p, "r", encoding="utf-8") as f:
            judgments = json.load(f)
    except Exception as e:
        print(f"skip {s}: {e}", file=sys.stderr)
        continue

    # build question_id -> condition -> response_text, etc
    qmap = {}
    for q in results:
        qid = q["question_id"]
        qmap[qid] = {
            "question": q.get("question_text", ""),
            "held_out": q.get("held_out_passage", ""),
            "responses": q.get("responses", {}),
        }

    # build (qid, condition) -> list of scores
    jmap = defaultdict(list)
    for j in judgments:
        qid = j["question_id"]
        cond = j["condition"]
        if j.get("parse_failure"):
            continue
        sc = j.get("score")
        if sc is None:
            continue
        jmap[(qid, cond)].append(sc)

    for (qid, cond), scores in jmap.items():
        if qid not in qmap:
            continue
        resp = qmap[qid]["responses"].get(cond)
        if not resp:
            continue
        text = resp["text"] if isinstance(resp, dict) else str(resp)
        if not text:
            continue
        mscore = mean(scores)
        records.append({
            "subject": s,
            "question_id": qid,
            "condition": cond,
            "question": qmap[qid]["question"],
            "held_out": qmap[qid]["held_out"],
            "response": text,
            "scores": scores,
            "mean_score": mscore,
            "n_judges": len(scores),
        })

print(f"Collected {len(records)} records", file=sys.stderr)

# Define bands
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

banded = {name: [] for name, _, _ in BANDS}
for r in records:
    ms = r["mean_score"]
    for name, lo, hi in BANDS:
        if lo <= ms <= hi:
            banded[name].append(r)
            break

print("Band counts:", file=sys.stderr)
for name, _, _ in BANDS:
    print(f"  {name}: {len(banded[name])}", file=sys.stderr)

# Within each band, sample diverse records: spread across subjects and conditions.
import random
random.seed(7)

sampled = {}
for name, _, _ in BANDS:
    pool = banded[name]
    # diversity: group by subject; take up to 2 per subject; fill to 15
    by_subj = defaultdict(list)
    for r in pool:
        by_subj[r["subject"]].append(r)
    for subj in by_subj:
        random.shuffle(by_subj[subj])
    picked = []
    max_per_subj = 2
    while len(picked) < 15:
        added = False
        for subj, lst in by_subj.items():
            if lst and sum(1 for p in picked if p["subject"] == subj) < max_per_subj:
                picked.append(lst.pop())
                added = True
                if len(picked) >= 15:
                    break
        if not added:
            break
    # if still short, fill from remaining
    if len(picked) < 15:
        remaining = [r for lst in by_subj.values() for r in lst]
        random.shuffle(remaining)
        picked.extend(remaining[: 15 - len(picked)])
    sampled[name] = picked

# Emit
out = {
    "meta": {
        "n_records_total": len(records),
        "subjects": sorted(set(r["subject"] for r in records)),
        "band_counts": {name: len(banded[name]) for name, _, _ in BANDS},
    },
    "bands": {},
}
for name in sampled:
    out["bands"][name] = [
        {
            "subject": r["subject"],
            "qid": r["question_id"],
            "condition": r["condition"],
            "question": r["question"],
            "held_out": r["held_out"][:800],
            "response": r["response"][:2500],
            "response_len_chars": len(r["response"]),
            "scores": r["scores"],
            "mean_score": round(r["mean_score"], 3),
            "n_judges": r["n_judges"],
        }
        for r in sampled[name]
    ]

out_path = str(REPO / "docs/research/_score_band_pool.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Wrote {out_path}", file=sys.stderr)
