"""Section 3.4 verification: battery statistics + n-gram leakage check.

For each of 14 main-study subjects:
  - count tiers in battery_v2.json (canonical battery used in rerun)
  - check BP question text for any 7+-consecutive-word n-gram that appears
    verbatim in heldout.txt
  - fallback to battery.json if battery_v2.json missing
"""
from __future__ import annotations
import json
import os
import re
import sys
from collections import Counter

REPO_RESULTS = r"C:\Users\Aarik\Anthropic\memory-study-repo\results"
REPO_DATA = r"C:\Users\Aarik\Anthropic\memory-study-repo\data"
MS_RESULTS = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"
MS_DATA_FRANKLIN = r"C:\Users\Aarik\Anthropic\memory_system\franklin_memory\data"
MS_DATA_HAMERTON = r"C:\Users\Aarik\Anthropic\memory_system\memory_core\data"

GLOBAL_SUBJECTS = [
    "augustine", "babur", "bernal_diaz", "cellini", "ebers", "equiano",
    "fukuzawa", "keckley", "rousseau", "seacole", "sunity_devee",
    "yung_wing", "zitkala_sa",
]
NON_GLOBAL = ["hamerton", "franklin"]

N = 7  # n-gram size for leakage check


def norm_tokens(text: str) -> list[str]:
    """Lowercase + word-tokenize; strip punctuation."""
    return re.findall(r"[a-z0-9]+", text.lower())


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return set(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))


def find_leak(question_tokens: list[str], heldout_ngrams: set[tuple[str, ...]], n: int):
    """Return the first overlapping n-gram, or None."""
    for i in range(len(question_tokens) - n + 1):
        g = tuple(question_tokens[i : i + n])
        if g in heldout_ngrams:
            return " ".join(g)
    return None


def load_battery(subject: str) -> tuple[dict | None, str]:
    """Try battery_v2.json first (canonical rerun), fall back to battery.json."""
    for fname in ("battery_v2.json", "battery.json"):
        # Study-repo side
        for base in (os.path.join(REPO_RESULTS, f"global_{subject}"),
                     os.path.join(REPO_RESULTS, subject),
                     os.path.join(REPO_DATA, subject),
                     os.path.join(REPO_DATA, "global_subjects", subject)):
            p = os.path.join(base, fname)
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as f:
                    return json.load(f), p
        # memory_system side
        for base in (os.path.join(MS_RESULTS, f"global_{subject}"),
                     os.path.join(MS_RESULTS, subject)):
            p = os.path.join(base, fname)
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as f:
                    return json.load(f), p
    return None, ""


def load_heldout(subject: str, battery: dict | None = None) -> tuple[str | None, str]:
    """Return heldout text and path.

    Prefer a dedicated heldout.txt file. If absent (Hamerton/Franklin), fall
    back to concatenating every held_out_passage in the battery: this covers
    the same text the generator used to seed questions and is the relevant
    corpus for checking that question text does not reveal ground truth.
    """
    candidates = [
        os.path.join(REPO_RESULTS, f"global_{subject}", "heldout.txt"),
        os.path.join(REPO_RESULTS, subject, "heldout.txt"),
        os.path.join(MS_RESULTS, f"global_{subject}", "heldout.txt"),
        os.path.join(MS_RESULTS, subject, "heldout.txt"),
        os.path.join(REPO_DATA, subject, "heldout.txt"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                return f.read(), p
    # Fallback: concatenate held_out_passage fields from battery
    if battery:
        passages = [q.get("held_out_passage", "") for q in battery.get("questions", [])
                    if q.get("held_out_passage")]
        if passages:
            return "\n".join(passages), "<concatenated held_out_passage fields from battery>"
    return None, ""


def analyze(subject: str) -> dict:
    battery, bat_path = load_battery(subject)
    if not battery:
        return {"subject": subject, "error": "no battery file found"}
    heldout, ho_path = load_heldout(subject, battery)
    questions = battery.get("questions", [])
    total = len(questions)
    tier_counts = Counter(q.get("tier", "unknown") for q in questions)
    category_counts = Counter(
        q.get("category") for q in questions
        if q.get("tier") == "behavioral_prediction" and q.get("category")
    )

    bp_qs = [q for q in questions if q.get("tier") == "behavioral_prediction"]
    bp_total = len(bp_qs)
    other_total = total - bp_total

    leak_details: list[dict] = []
    if heldout:
        ho_tokens = norm_tokens(heldout)
        ho_ngrams = ngrams(ho_tokens, N)
        for q in bp_qs:
            q_tokens = norm_tokens(q.get("text", ""))
            leak = find_leak(q_tokens, ho_ngrams, N)
            if leak:
                leak_details.append({
                    "qid": q.get("id"),
                    "text": q.get("text", "")[:180],
                    "leaked_ngram": leak,
                })

    return {
        "subject": subject,
        "battery_path": bat_path,
        "heldout_path": ho_path,
        "total": total,
        "bp_scored": bp_total,
        "other_generated_not_scored": other_total,
        "tier_counts": dict(tier_counts),
        "bp_category_counts": dict(category_counts),
        "leak_count": len(leak_details),
        "leak_rate": (len(leak_details) / bp_total) if bp_total else 0.0,
        "leak_examples": leak_details[:3],
        "heldout_available": bool(heldout),
    }


def main():
    all_subjects = NON_GLOBAL + GLOBAL_SUBJECTS
    results = []
    for s in all_subjects:
        r = analyze(s)
        results.append(r)

    # Print compact table
    print("\n== Per-subject battery statistics ==\n")
    print(f"{'subject':<14} {'total':>5} {'bp':>3} {'other':>5} "
          f"{'cats':>4} {'leak_n':>6} {'leak_rate':>9} {'ho?':>3}")
    agg_bp = agg_leak = 0
    for r in results:
        if "error" in r:
            print(f"{r['subject']:<14} ERROR: {r['error']}")
            continue
        ncat = len(r["bp_category_counts"])
        print(f"{r['subject']:<14} {r['total']:>5} {r['bp_scored']:>3} "
              f"{r['other_generated_not_scored']:>5} {ncat:>4} "
              f"{r['leak_count']:>6} {r['leak_rate']:>9.3f} "
              f"{'Y' if r['heldout_available'] else 'N':>3}")
        agg_bp += r["bp_scored"]
        agg_leak += r["leak_count"]

    print()
    print(f"Aggregate BP questions: {agg_bp}")
    print(f"Aggregate leaked BP questions (7+ consecutive words verbatim in heldout): {agg_leak}")
    if agg_bp:
        print(f"Aggregate leakage rate: {agg_leak / agg_bp:.4f}")

    # Category universe
    all_cats: Counter = Counter()
    for r in results:
        if "bp_category_counts" in r:
            all_cats.update(r["bp_category_counts"])
    print(f"\nBP categories across all subjects: {sorted(all_cats.keys())}")
    print(f"Total category tokens: {sum(all_cats.values())}")

    # Print any leakage examples
    print("\n== Leak examples (if any) ==")
    any_leaks = False
    for r in results:
        if r.get("leak_count"):
            any_leaks = True
            print(f"\n{r['subject']}: {r['leak_count']} questions with held-out n-gram overlap")
            for ex in r["leak_examples"]:
                print(f"  qid={ex['qid']} ngram='{ex['leaked_ngram']}'")
                print(f"    question: {ex['text']}")
    if not any_leaks:
        print("  None — zero leakage across all subjects.")

    # Also print subjects missing heldout
    missing = [r["subject"] for r in results if "error" not in r and not r["heldout_available"]]
    if missing:
        print(f"\nWARN: heldout.txt not found for: {missing}")

    # Dump JSON for downstream doc
    out = os.path.join(os.path.dirname(__file__), "_battery_leakage_results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "n_gram_size": N,
            "per_subject": results,
            "aggregate_bp": agg_bp,
            "aggregate_leaks": agg_leak,
            "aggregate_leak_rate": (agg_leak / agg_bp) if agg_bp else 0.0,
            "categories_universe": sorted(all_cats.keys()),
        }, f, indent=2, ensure_ascii=False)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
