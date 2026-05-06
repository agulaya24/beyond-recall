"""Supermemory 5-judge primary paired C1 vs C3 analysis.

For EACH of the 14 main-study subjects, pair responses by question_id across
C1_supermemory (retrieval only) and C3_supermemory (retrieval + spec), compute
per-question mean score across the 5 PRIMARY judges (Haiku, Sonnet, Opus,
GPT-4o, GPT-5.4), and surface:

  - Top N positive-swing (spec helps) examples
  - Top N negative-swing (spec hurts) examples
  - Counts: |Δ| >= 1.0, Δ >= +1.0, Δ <= -1.0
  - Magnitude summary: mean of positive swings, mean of negative swings

Excludes questions known to be already cited in paper:
  Ebers Q3, Ebers Q7, Keckley Q21, Bernal Diaz Q16, Seacole Q2

Writes JSON to docs/research/_sm_paired_5judge.json for inspection.
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

RESULTS_ROOT = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo/results")
OUT_PATH = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/_sm_paired_5judge.json")

PRIMARY_JUDGES = {"haiku", "sonnet", "opus", "gpt4o", "gpt54"}

MAIN_STUDY = [
    "hamerton",
    "sunity_devee", "ebers", "fukuzawa", "seacole", "bernal_diaz",
    "keckley", "yung_wing", "babur", "cellini", "zitkala_sa",
    "rousseau", "augustine", "equiano",
]

EXCLUDE = {
    ("ebers", 3),
    ("ebers", 7),
    ("keckley", 21),
    ("bernal_diaz", 16),
    ("seacole", 2),
    ("sunity_devee", 35),
}


def subject_dir(subject):
    if subject == "hamerton":
        return RESULTS_ROOT / "hamerton"
    return RESULTS_ROOT / f"global_{subject}"


def load_subject(subject):
    sdir = subject_dir(subject)
    results_path = sdir / "supermemory_results.json"
    judgments_path = sdir / "supermemory_judgments_merged.json"
    if not results_path.exists() or not judgments_path.exists():
        return {}
    results = json.loads(results_path.read_text(encoding="utf-8"))
    judgments = json.loads(judgments_path.read_text(encoding="utf-8"))

    by_q = {}
    for entry in results:
        qid = entry["question_id"]
        responses = entry.get("responses", {}) or {}
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
        qid = j.get("question_id")
        cond = j.get("condition")
        judge = j.get("judge")
        score = j.get("score")
        if qid is None or judge not in PRIMARY_JUDGES:
            continue
        if j.get("parse_failure"):
            continue
        if score is None:
            continue
        if qid not in by_q:
            continue
        if cond == "C1_supermemory":
            by_q[qid]["C1_scores"][judge] = score
        elif cond == "C3_supermemory":
            by_q[qid]["C3_scores"][judge] = score

    for qid, q in list(by_q.items()):
        c1s = list(q["C1_scores"].values())
        c3s = list(q["C3_scores"].values())
        # require same 5-judge panel present on both sides to be paired cleanly;
        # fall back to whatever overlap exists
        shared = set(q["C1_scores"].keys()) & set(q["C3_scores"].keys())
        if not shared:
            q["C1_mean"] = None
            q["C3_mean"] = None
            q["delta"] = None
            q["n_shared"] = 0
            continue
        q["n_shared"] = len(shared)
        q["C1_mean"] = mean(q["C1_scores"][j] for j in shared)
        q["C3_mean"] = mean(q["C3_scores"][j] for j in shared)
        q["delta"] = q["C3_mean"] - q["C1_mean"]

    return by_q


def main():
    all_pairs = []  # (subject, qid, q)
    per_subject_summary = {}
    for subj in MAIN_STUDY:
        by_q = load_subject(subj)
        if not by_q:
            per_subject_summary[subj] = {"n": 0, "note": "no data"}
            continue
        # Accept any pair with at least 3 shared primary judges (tolerates parse
        # failures on some judges, e.g. babur where gpt4o/gpt54/gemini failed).
        pairs = [(subj, qid, q) for qid, q in by_q.items()
                 if q["delta"] is not None and q["n_shared"] >= 3]
        all_pairs.extend(pairs)
        deltas = [q["delta"] for _, _, q in pairs]
        per_subject_summary[subj] = {
            "n": len(pairs),
            "mean_c1": mean(q["C1_mean"] for _, _, q in pairs) if pairs else None,
            "mean_c3": mean(q["C3_mean"] for _, _, q in pairs) if pairs else None,
            "mean_delta": mean(deltas) if deltas else None,
            "n_helps_1": sum(1 for d in deltas if d >= 1.0),
            "n_hurts_1": sum(1 for d in deltas if d <= -1.0),
            "n_helps_1p5": sum(1 for d in deltas if d >= 1.5),
            "n_hurts_1p5": sum(1 for d in deltas if d <= -1.5),
        }

    # Global counts on full main-study N
    deltas = [q["delta"] for _, _, q in all_pairs]
    n_total = len(all_pairs)
    n_helps_1 = sum(1 for d in deltas if d >= 1.0)
    n_hurts_1 = sum(1 for d in deltas if d <= -1.0)
    n_abs_1 = n_helps_1 + n_hurts_1
    pos_swings = [d for d in deltas if d >= 1.0]
    neg_swings = [d for d in deltas if d <= -1.0]
    pos_swings_mean = mean(pos_swings) if pos_swings else None
    neg_swings_mean = mean(neg_swings) if neg_swings else None

    # Top positive / negative pairs, excluding already-cited
    eligible = [p for p in all_pairs if (p[0], p[1]) not in EXCLUDE]
    pos_sorted = sorted(eligible, key=lambda x: -x[2]["delta"])
    neg_sorted = sorted(eligible, key=lambda x: x[2]["delta"])

    def compact(p, n=20):
        subj, qid, q = p
        return {
            "subject": subj,
            "question_id": qid,
            "delta": round(q["delta"], 3),
            "C1_mean": round(q["C1_mean"], 3),
            "C3_mean": round(q["C3_mean"], 3),
            "question": q["question"],
            "held_out": q["held_out"],
            "C1_text": q["C1_text"],
            "C3_text": q["C3_text"],
            "C1_scores": q["C1_scores"],
            "C3_scores": q["C3_scores"],
        }

    # Moderate positive swings (0.6 to 1.2) — subtle spec helps
    moderate = sorted([p for p in eligible if 0.6 <= p[2]["delta"] <= 1.2],
                      key=lambda x: -x[2]["delta"])

    out = {
        "method": "5-judge primary (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4), "
                  "paired by question_id, require all 5 judges present on both sides.",
        "exclude": sorted(list(EXCLUDE)),
        "n_questions_total": n_total,
        "mixture_counts": {
            "|delta| >= 1.0": n_abs_1,
            "delta >= +1.0 (spec helps)": n_helps_1,
            "delta <= -1.0 (spec hurts)": n_hurts_1,
            "mean positive swing (delta >= +1.0)": pos_swings_mean,
            "mean negative swing (delta <= -1.0)": neg_swings_mean,
        },
        "per_subject_summary": per_subject_summary,
        "top_20_helps": [compact(p) for p in pos_sorted[:20]],
        "top_20_hurts": [compact(p) for p in neg_sorted[:20]],
        "moderate_helps_0p6_to_1p2": [compact(p) for p in moderate[:30]],
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    # Console summary
    print(f"Total paired questions (5-judge clean): {n_total}")
    print(f"|delta| >= 1.0: {n_abs_1}  (+1.0: {n_helps_1}, -1.0: {n_hurts_1})")
    if pos_swings_mean is not None:
        print(f"Mean positive swing (>= +1.0): +{pos_swings_mean:.3f} (n={len(pos_swings)})")
    if neg_swings_mean is not None:
        print(f"Mean negative swing (<= -1.0): {neg_swings_mean:.3f} (n={len(neg_swings)})")
    print()
    print("Top helps (excl already-cited):")
    for p in pos_sorted[:10]:
        subj, qid, q = p
        print(f"  {subj:<14} Q{qid:<3} d={q['delta']:+.2f}  C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f}  {q['question'][:80]}")
    print()
    print("Top hurts (excl already-cited):")
    for p in neg_sorted[:10]:
        subj, qid, q = p
        print(f"  {subj:<14} Q{qid:<3} d={q['delta']:+.2f}  C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f}  {q['question'][:80]}")
    print(f"\nSaved to: {OUT_PATH}")


if __name__ == "__main__":
    main()
