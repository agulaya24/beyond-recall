"""Analyze Mem0 / Letta / Zep C1 (retrieval only) vs C3 (retrieval + spec) per question.

Mirrors scripts/analyze_sm_c1_vs_c3.py but for the other three commercial memory
systems. For a hand-picked spread of low-baseline subjects per system, pair
responses by question_id across C1_<sys> and C3_<sys>, compute per-question
mean judge score (six judges), and bucket into similar / C3-higher / C3-lower.

Output:
  prints per-subject distribution table + candidate examples
  writes docs/research/_mlz_c1_c3_candidates.json
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

RESULTS_ROOT = Path(r"C:/Users/Aarik/Anthropic/memory-study-repo")
OUT_PATH = RESULTS_ROOT / "docs" / "research" / "_mlz_c1_c3_candidates.json"

# Per-system picks: include ebers + a strongest-delta + a weakest-delta among
# the canonical low-baseline subjects, plus one extra for spread.
SYSTEM_SUBJECTS = {
    "mem0":  ["ebers", "yung_wing", "sunity_devee", "keckley"],
    "letta": ["ebers", "hamerton",  "sunity_devee", "keckley"],
    "zep":   ["ebers", "seacole",   "bernal_diaz",  "keckley"],
}


def load_subject(system: str, subject: str) -> dict:
    sdir_candidates = [
        RESULTS_ROOT / "results" / f"global_{subject}",
        RESULTS_ROOT / "results" / subject,
    ]
    results_name = f"{system}_results.json"
    judgments_name = f"{system}_judgments_merged.json"
    sdir = next((p for p in sdir_candidates if (p / results_name).exists()), None)
    if sdir is None:
        return {}

    with open(sdir / results_name, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(sdir / judgments_name, "r", encoding="utf-8") as f:
        judgments = json.load(f)

    c1_key = f"C1_{system}"
    c3_key = f"C3_{system}"

    by_q: dict = {}
    for entry in results:
        qid = entry["question_id"]
        responses = entry.get("responses", {})
        c1 = responses.get(c1_key) or {}
        c3 = responses.get(c3_key) or {}
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
        if cond == c1_key:
            by_q[qid]["C1_scores"][judge] = score
        elif cond == c3_key:
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


def subject_summary(system: str, subject: str, by_q: dict) -> dict:
    c1_means = [q["C1_mean"] for q in by_q.values() if q["C1_mean"] is not None]
    c3_means = [q["C3_mean"] for q in by_q.values() if q["C3_mean"] is not None]
    deltas   = [q["delta"]   for q in by_q.values() if q["delta"]   is not None]
    return {
        "system": system,
        "subject": subject,
        "n_questions": len(by_q),
        "C1_mean": mean(c1_means) if c1_means else None,
        "C3_mean": mean(c3_means) if c3_means else None,
        "delta_mean": mean(deltas) if deltas else None,
        "n_c3_higher": sum(1 for d in deltas if d > 0.3),
        "n_c3_lower":  sum(1 for d in deltas if d < -0.3),
        "n_similar":   sum(1 for d in deltas if -0.3 <= d <= 0.3),
        # Also capture large-swing variants for the mixture read
        "n_c3_higher_big": sum(1 for d in deltas if d > 1.0),
        "n_c3_lower_big":  sum(1 for d in deltas if d < -1.0),
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


def main():
    by_system_summaries: dict = {s: [] for s in SYSTEM_SUBJECTS}
    by_system_buckets: dict = {s: {} for s in SYSTEM_SUBJECTS}

    for system, subjects in SYSTEM_SUBJECTS.items():
        for subj in subjects:
            by_q = load_subject(system, subj)
            if not by_q:
                print(f"[WARN] missing data for {system}/{subj}")
                continue
            by_system_summaries[system].append(subject_summary(system, subj, by_q))
            by_system_buckets[system][subj] = (by_q, *bucket_questions(by_q))

    print("\n=== SUMMARIES ===")
    for system, summ_list in by_system_summaries.items():
        print(f"\n--- {system} ---")
        for s in summ_list:
            print(f"  {s['subject']:14s}  C1={s['C1_mean']:.2f}  C3={s['C3_mean']:.2f}  d={s['delta_mean']:+.3f}  "
                  f"higher={s['n_c3_higher']:2d}  similar={s['n_similar']:2d}  lower={s['n_c3_lower']:2d}  "
                  f"bigpos={s['n_c3_higher_big']}  bigneg={s['n_c3_lower_big']}")

    # Pick candidate examples per system: 1 similar, 1 higher, 1 lower,
    # preferring the ebers subject for the higher/lower buckets when possible.
    emissions: dict = {}
    for system, buckets_by_subj in by_system_buckets.items():
        picks = {"similar": [], "higher": [], "lower": []}
        # Priority ordering: ebers first, then strongest-delta subject, then rest
        priority = SYSTEM_SUBJECTS[system]
        for subj in priority:
            if subj not in buckets_by_subj:
                continue
            _, similar, higher, lower = buckets_by_subj[subj]
            if len(picks["higher"]) < 2 and higher:
                picks["higher"].append((subj, higher[0]))
            if len(picks["lower"]) < 2 and lower:
                picks["lower"].append((subj, lower[0]))
            if len(picks["similar"]) < 2 and similar:
                # prefer high-magnitude similar (both >= 2.5)
                chosen = next(((q_id, q) for (q_id, q) in similar if (q["C1_mean"] + q["C3_mean"]) / 2 >= 2.5), similar[0])
                picks["similar"].append((subj, chosen))
        emissions[system] = picks

    print("\n=== CANDIDATE EXAMPLES ===")
    for system, picks in emissions.items():
        print(f"\n### {system.upper()} ###")
        for bucket, items in picks.items():
            print(f"\n--- {bucket} ---")
            for subj, (qid, q) in items:
                print(f"[{subj}] Q{qid}  C1={q['C1_mean']:.2f} C3={q['C3_mean']:.2f} d={q['delta']:+.2f}")
                print(f"  Q: {q['question'][:160]}")
                print(f"  C1 (first 260ch): {q['C1_text'][:260]}")
                print(f"  C3 (first 260ch): {q['C3_text'][:260]}")

    serializable = {
        "summaries": by_system_summaries,
        "examples": {
            system: {
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
            }
            for system, picks in emissions.items()
        },
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"\nSaved candidates to: {OUT_PATH}")


if __name__ == "__main__":
    main()
