"""Analyze Supermemory C1 (retrieval only) vs C3 (retrieval + spec) per question.

For each of 9 low-baseline subjects, pair responses by question_id across the two
conditions and compute per-question mean judge scores. Bucket paired examples into:
  (a) similar score, different content/tone
  (b) C3 scored higher
  (c) C3 scored lower

Input:
  results/global_<subject>/supermemory_results.json        (both conditions' texts)
  results/global_<subject>/supermemory_judgments_merged.json (all judges)

Output: prints a structured summary and candidate examples for markdown write-up.
"""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from statistics import mean

RESULTS_ROOT = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo/results")
LOW_BASELINE_SUBJECTS = [
    "sunity_devee", "ebers", "hamerton", "fukuzawa", "seacole",
    "bernal_diaz", "keckley", "yung_wing", "babur",
]

def load_subject(subject: str) -> dict:
    """Return dict: question_id -> {question, held_out, C1_text, C3_text,
       C1_scores: {judge: score}, C3_scores: {judge: score},
       C1_mean, C3_mean, delta}."""
    candidates = [RESULTS_ROOT / f"global_{subject}", RESULTS_ROOT / subject]
    sdir = next((p for p in candidates if (p / "supermemory_results.json").exists()), None)
    if sdir is None:
        return {}
    results_path = sdir / "supermemory_results.json"
    judgments_path = sdir / "supermemory_judgments_merged.json"
    if not results_path.exists() or not judgments_path.exists():
        return {}

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(judgments_path, "r", encoding="utf-8") as f:
        judgments = json.load(f)

    by_q: dict = {}
    for entry in results:
        qid = entry["question_id"]
        responses = entry.get("responses", {})
        c1 = responses.get("C1_supermemory") or {}
        c3 = responses.get("C3_supermemory") or {}
        by_q[qid] = {
            "question_id": qid,
            "question": entry.get("question_text", ""),
            "held_out": entry.get("held_out_passage", ""),
            "C1_text": c1.get("text", ""),
            "C3_text": c3.get("text", ""),
            "C1_scores": {},
            "C3_scores": {},
        }

    for j in judgments:
        qid = j["question_id"]
        cond = j["condition"]
        if qid not in by_q:
            continue
        if j.get("parse_failure"):
            continue
        score = j.get("score")
        if score is None:
            continue
        judge = j.get("judge", "unknown")
        if cond == "C1_supermemory":
            by_q[qid]["C1_scores"][judge] = score
        elif cond == "C3_supermemory":
            by_q[qid]["C3_scores"][judge] = score

    for qid, q in by_q.items():
        c1s = list(q["C1_scores"].values())
        c3s = list(q["C3_scores"].values())
        q["C1_mean"] = mean(c1s) if c1s else None
        q["C3_mean"] = mean(c3s) if c3s else None
        if q["C1_mean"] is not None and q["C3_mean"] is not None:
            q["delta"] = q["C3_mean"] - q["C1_mean"]
        else:
            q["delta"] = None

    return by_q


def subject_summary(subject: str, by_q: dict) -> dict:
    c1_means = [q["C1_mean"] for q in by_q.values() if q["C1_mean"] is not None]
    c3_means = [q["C3_mean"] for q in by_q.values() if q["C3_mean"] is not None]
    deltas = [q["delta"] for q in by_q.values() if q["delta"] is not None]
    return {
        "subject": subject,
        "n_questions": len(by_q),
        "C1_mean": mean(c1_means) if c1_means else None,
        "C3_mean": mean(c3_means) if c3_means else None,
        "delta_mean": mean(deltas) if deltas else None,
        "n_c3_higher": sum(1 for d in deltas if d > 0.3),
        "n_c3_lower": sum(1 for d in deltas if d < -0.3),
        "n_similar": sum(1 for d in deltas if -0.3 <= d <= 0.3),
    }


def bucket_questions(by_q: dict, similar_band: float = 0.3):
    """Return three lists of (qid, q) tuples sorted by interesting-ness."""
    similar, higher, lower = [], [], []
    for qid, q in by_q.items():
        if q["delta"] is None:
            continue
        d = q["delta"]
        if abs(d) <= similar_band:
            similar.append((qid, q))
        elif d > similar_band:
            higher.append((qid, q))
        else:
            lower.append((qid, q))
    # For similar bucket, prefer high-magnitude answers (both >= 2)
    similar.sort(key=lambda x: -(x[1]["C1_mean"] + x[1]["C3_mean"]))
    higher.sort(key=lambda x: -x[1]["delta"])
    lower.sort(key=lambda x: x[1]["delta"])
    return similar, higher, lower


def compact_text(t: str, limit: int = 1800) -> str:
    t = t.strip()
    if len(t) <= limit:
        return t
    return t[:limit] + "\n... [truncated]"


def main():
    summaries = []
    per_subject_buckets = {}
    for subj in LOW_BASELINE_SUBJECTS:
        by_q = load_subject(subj)
        if not by_q:
            print(f"[WARN] no data for {subj}")
            continue
        summaries.append(subject_summary(subj, by_q))
        per_subject_buckets[subj] = (by_q, *bucket_questions(by_q))

    print("\n=== SUBJECT SUMMARIES ===")
    for s in summaries:
        print(json.dumps(s, indent=2))

    # Emit candidate examples per bucket across all subjects
    # We want ~2 from each of: similar, higher, lower
    # Priority: Ebers (+0.20), Keckley (−0.25) as focus, then fill with others
    emissions = {"similar": [], "higher": [], "lower": []}
    for subj in ["ebers", "keckley"] + [s for s in LOW_BASELINE_SUBJECTS if s not in ("ebers", "keckley")]:
        if subj not in per_subject_buckets:
            continue
        by_q, similar, higher, lower = per_subject_buckets[subj]
        if similar and len(emissions["similar"]) < 3:
            emissions["similar"].append((subj, similar[0]))
        if higher and len(emissions["higher"]) < 3:
            emissions["higher"].append((subj, higher[0]))
        if lower and len(emissions["lower"]) < 3:
            emissions["lower"].append((subj, lower[0]))

    print("\n=== CANDIDATE EXAMPLES ===")
    for bucket, items in emissions.items():
        print(f"\n--- {bucket.upper()} ---")
        for subj, (qid, q) in items:
            print(f"\nSubject: {subj}  QID: {qid}  C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f} d={q['delta']:+.2f}")
            print(f"Q: {q['question'][:200]}")
            print(f"C1 (first 400ch): {q['C1_text'][:400]}")
            print(f"C3 (first 400ch): {q['C3_text'][:400]}")

    # Persist the emissions for later markdown writing
    out_path = RESULTS_ROOT.parent / "docs" / "research" / "_sm_c1_c3_candidates.json"
    serializable = {
        "summaries": summaries,
        "examples": {
            bucket: [
                {
                    "subject": subj,
                    "question_id": qid,
                    "question": q["question"],
                    "held_out": q["held_out"],
                    "C1_text": q["C1_text"],
                    "C3_text": q["C3_text"],
                    "C1_scores": q["C1_scores"],
                    "C3_scores": q["C3_scores"],
                    "C1_mean": q["C1_mean"],
                    "C3_mean": q["C3_mean"],
                    "delta": q["delta"],
                }
                for subj, (qid, q) in items
            ]
            for bucket, items in emissions.items()
        },
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"\nSaved candidate examples to: {out_path}")


if __name__ == "__main__":
    main()
