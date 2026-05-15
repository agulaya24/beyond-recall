"""Analyze Base Layer (MiniLM-L6-v2 + ChromaDB) C1 vs C3 per-question.

Mirrors scripts/analyze_mlz_c1_vs_c3.py but for Base Layer's own retrieval
substrate. For a hand-picked spread of low-baseline subjects, pair responses
by question_id across C1_baselayer and C3_baselayer, compute per-question mean
judge score (six judges), and bucket into similar / C3-higher / C3-lower.

Output:
  prints per-subject distribution table + candidate examples
  writes docs/research/_baselayer_c1_c3_candidates.json
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

RESULTS_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = RESULTS_ROOT / "docs" / "research" / "_baselayer_c1_c3_candidates.json"

# Low-baseline subjects: include ebers + keckley for continuity with prior
# analyses, plus hamerton (paper's named subject for M1), yung_wing, babur
# for spread across baseline/corpus size.
SUBJECTS = ["ebers", "keckley", "hamerton", "yung_wing", "babur"]
SYSTEM = "baselayer"
C1_KEY = "C1_baselayer"
C3_KEY = "C3_baselayer"


def load_subject(subject: str) -> dict:
    sdir_candidates = [
        RESULTS_ROOT / "results" / f"global_{subject}",
        RESULTS_ROOT / "results" / subject,
    ]
    results_name = f"{SYSTEM}_results.json"
    judgments_name = f"{SYSTEM}_judgments_merged.json"
    sdir = next((p for p in sdir_candidates if (p / results_name).exists()), None)
    if sdir is None:
        return {}

    with open(sdir / results_name, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(sdir / judgments_name, "r", encoding="utf-8") as f:
        judgments = json.load(f)

    by_q: dict = {}
    for entry in results:
        qid = entry["question_id"]
        responses = entry.get("responses", {})
        c1 = responses.get(C1_KEY) or {}
        c3 = responses.get(C3_KEY) or {}
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
        if cond == C1_KEY:
            by_q[qid]["C1_scores"][judge] = score
        elif cond == C3_KEY:
            by_q[qid]["C3_scores"][judge] = score

    for q in by_q.values():
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
        "n_c3_higher_big": sum(1 for d in deltas if d > 1.0),
        "n_c3_lower_big": sum(1 for d in deltas if d < -1.0),
    }


def bucket_questions(by_q: dict, band: float = 0.3):
    similar, higher, lower = [], [], []
    for qid, q in by_q.items():
        if q["delta"] is None:
            continue
        d = q["delta"]
        if abs(d) <= band:
            similar.append((qid, q))
        elif d > band:
            higher.append((qid, q))
        else:
            lower.append((qid, q))
    similar.sort(key=lambda x: -(x[1]["C1_mean"] + x[1]["C3_mean"]))
    higher.sort(key=lambda x: -x[1]["delta"])
    lower.sort(key=lambda x: x[1]["delta"])
    return similar, higher, lower


HEDGE_TRIGGERS = [
    "i don't know",
    "i don't have",
    "i do not have",
    "i cannot",
    "i can't",
    "i need to be direct",
    "i should acknowledge",
    "i should be direct",
    "i must be direct",
    "the retrieved facts do not",
    "the retrieved facts don't",
    "the provided",
    "not enough",
    "insufficient",
    "without more",
    "no direct information",
    "no specific information",
    "speculat",
    "acknowledge what i don't",
    "without speculating",
]


def hedge_count(text: str) -> int:
    t = text.lower()
    return sum(1 for h in HEDGE_TRIGGERS if h in t)


def main():
    summaries = []
    buckets_by_subj: dict = {}

    for subj in SUBJECTS:
        by_q = load_subject(subj)
        if not by_q:
            print(f"[WARN] missing data for {subj}")
            continue
        summaries.append(subject_summary(subj, by_q))
        buckets_by_subj[subj] = (by_q, *bucket_questions(by_q))

    print("\n=== SUMMARIES ===")
    for s in summaries:
        print(
            f"  {s['subject']:14s}  C1={s['C1_mean']:.2f}  C3={s['C3_mean']:.2f}  "
            f"d={s['delta_mean']:+.3f}  "
            f"higher={s['n_c3_higher']:2d}  similar={s['n_similar']:2d}  lower={s['n_c3_lower']:2d}  "
            f"bigpos={s['n_c3_higher_big']}  bigneg={s['n_c3_lower_big']}"
        )

    # Hedging comparison: for each subject, compute mean hedge-trigger counts
    # in C1 vs C3 responses.
    print("\n=== HEDGE-TRIGGER COUNTS (lexical proxy) ===")
    hedge_stats = {}
    for subj, (by_q, *_rest) in buckets_by_subj.items():
        c1_hedges = [hedge_count(q["C1_text"]) for q in by_q.values() if q["C1_text"]]
        c3_hedges = [hedge_count(q["C3_text"]) for q in by_q.values() if q["C3_text"]]
        c1_flagged = sum(1 for h in c1_hedges if h > 0)
        c3_flagged = sum(1 for h in c3_hedges if h > 0)
        hedge_stats[subj] = {
            "c1_mean_hedges": mean(c1_hedges) if c1_hedges else 0,
            "c3_mean_hedges": mean(c3_hedges) if c3_hedges else 0,
            "c1_flagged_questions": c1_flagged,
            "c3_flagged_questions": c3_flagged,
            "n_questions": len(by_q),
        }
        print(
            f"  {subj:14s}  C1 avg={hedge_stats[subj]['c1_mean_hedges']:.2f} "
            f"flagged={c1_flagged}/{len(by_q)} | "
            f"C3 avg={hedge_stats[subj]['c3_mean_hedges']:.2f} "
            f"flagged={c3_flagged}/{len(by_q)}"
        )

    # Pick candidate examples per bucket
    picks = {"similar": [], "higher": [], "lower": []}
    for subj in SUBJECTS:
        if subj not in buckets_by_subj:
            continue
        _, similar, higher, lower = buckets_by_subj[subj]
        if len(picks["higher"]) < 3 and higher:
            picks["higher"].append((subj, higher[0]))
        if len(picks["lower"]) < 3 and lower:
            picks["lower"].append((subj, lower[0]))
        if len(picks["similar"]) < 3 and similar:
            chosen = next(
                ((qid, q) for (qid, q) in similar if (q["C1_mean"] + q["C3_mean"]) / 2 >= 2.5),
                similar[0],
            )
            picks["similar"].append((subj, chosen))

    print("\n=== CANDIDATE EXAMPLES ===")
    for bucket, items in picks.items():
        print(f"\n--- {bucket} ---")
        for subj, (qid, q) in items:
            print(f"[{subj}] Q{qid}  C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f} d={q['delta']:+.2f}")
            print(f"  Q: {q['question'][:160]}")
            print(f"  C1 (first 300ch): {q['C1_text'][:300]}")
            print(f"  C3 (first 300ch): {q['C3_text'][:300]}")

    # Specifically probe Keckley Q21 for the refusal test
    print("\n=== KECKLEY Q21 PROBE ===")
    if "keckley" in buckets_by_subj:
        by_q = buckets_by_subj["keckley"][0]
        q = by_q.get(21)
        if q:
            print(f"Q21 C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f} d={q['delta']:+.2f}")
            print(f"C1 per-judge: {q['C1_scores']}")
            print(f"C3 per-judge: {q['C3_scores']}")
            print(f"C1 full text:\n{q['C1_text']}\n")
            print(f"C3 full text:\n{q['C3_text']}\n")

    serializable = {
        "summaries": summaries,
        "hedge_stats": hedge_stats,
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
            for bucket, items in picks.items()
        },
    }
    # Add Keckley Q21 explicitly for the refusal-reproducibility check
    if "keckley" in buckets_by_subj:
        by_q = buckets_by_subj["keckley"][0]
        q = by_q.get(21)
        if q:
            serializable["keckley_q21"] = {
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
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"\nSaved candidates to: {OUT_PATH}")


if __name__ == "__main__":
    main()
