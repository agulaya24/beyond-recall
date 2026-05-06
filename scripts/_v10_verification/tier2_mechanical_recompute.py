"""
Mechanical recompute of §4.6.1 Tier 2 deltas.

No inference. No interpretation. Aggregation rule is fixed:
  1. Per-judge per-question score from raw JSON
  2. Per-judge per-subject mean = mean(per-question scores within subject)
  3. Panel mean per-subject per-condition = mean(per-judge means across panel members)

Outputs every plausible Δ definition for the 6 (subject, response_model) Tier 2 cells:
  - Δ_C2a_internal = C2a - C5 (both Tier 2, same response model)
  - Δ_C4a_internal = C4a - C5 (both Tier 2, same response model)
  - Δ_C4a_main_baseline = Tier 2 C4a - main-study Haiku C5
  - Δ_C2a_main_baseline = Tier 2 C2a - main-study Haiku C5

For each Δ, reports both 5-judge primary panel and 7-judge panel.

Output is a table the author can compare against §4.6.1 to determine which
combination of (Δ definition, panel) the paper's published numbers came from.
"""
from __future__ import annotations

import glob
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TIER2_DIR = REPO / "results" / "_tier2"
MAIN_DIR = REPO / "results"

PRIMARY_5 = {"haiku", "sonnet", "opus", "gpt4o", "gpt54"}
ALL_7 = PRIMARY_5 | {"gemini_flash", "gemini_pro"}

TIER2_CELLS = [
    ("ebers", "sonnet"),
    ("ebers", "gemini_pro"),
    ("yung_wing", "sonnet"),
    ("yung_wing", "gemini_pro"),
    ("zitkala_sa", "sonnet"),
    ("zitkala_sa", "gemini_pro"),
]

PUBLISHED = {
    ("ebers", "sonnet"): +1.48,
    ("ebers", "gemini_pro"): +1.07,
    ("yung_wing", "sonnet"): +1.91,
    ("yung_wing", "gemini_pro"): +1.27,
    ("zitkala_sa", "sonnet"): +1.40,
    ("zitkala_sa", "gemini_pro"): -0.55,
}


def load_judgments(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("judgments", [])
    return data


def per_subject_per_condition_mean(
    judgment_files: list[Path], panel: set[str]
) -> dict[str, float]:
    """Return per-condition mean using fixed two-step aggregation."""
    pq = defaultdict(lambda: defaultdict(list))  # cond -> qid -> [scores]
    for path in judgment_files:
        judge = path.stem.split("_")[-1]
        if judge not in panel:
            continue
        for record in load_judgments(path):
            cond = record.get("condition", "")
            qid = record.get("question_id")
            score = record.get("score")
            if score is None or qid is None:
                continue
            pq[cond][qid].append(score)
    out = {}
    for cond, q_to_scores in pq.items():
        per_q_means = [sum(scores) / len(scores) for scores in q_to_scores.values() if scores]
        if per_q_means:
            out[cond] = sum(per_q_means) / len(per_q_means)
    return out


def tier2_means(subject: str, response_model: str, panel: set[str]) -> dict[str, float]:
    pattern = TIER2_DIR / f"global_{subject}" / f"tier2_{response_model}_judgments_*.json"
    files = [
        Path(p)
        for p in glob.glob(str(pattern))
        if not p.endswith(".rl_backup") and "merged" not in p
    ]
    return per_subject_per_condition_mean(files, panel)


def main_study_haiku_c5(subject: str, panel: set[str]) -> float:
    """Main-study C5 baseline for the subject (Haiku response, original Haiku-generated battery)."""
    judg_path = MAIN_DIR / f"global_{subject}" / "judgments_v2.json"
    if not judg_path.exists():
        return None
    data = load_judgments(judg_path)
    pq = defaultdict(list)
    for d in data:
        if d.get("condition") != "C5_baseline":
            continue
        if d.get("judge") not in panel:
            continue
        score = d.get("score")
        qid = d.get("question_id")
        if score is None or qid is None:
            continue
        pq[qid].append(score)
    per_q = [sum(s) / len(s) for s in pq.values() if s]
    return sum(per_q) / len(per_q) if per_q else None


def fmt(x):
    return "    na" if x is None else f"{x:+7.3f}"


def fmt_p(x):
    return "    na" if x is None else f"{x:7.3f}"


def main():
    print("=" * 110)
    print("Tier 2 Mechanical Recompute — every plausible Δ definition")
    print("=" * 110)

    for panel_name, panel in [("5-judge primary", PRIMARY_5), ("7-judge", ALL_7)]:
        print(f"\nPanel: {panel_name}\n")
        print(
            f"{'subject':14} {'resp':12} {'T2_C5':>7} {'T2_C2a':>7} {'T2_C4a':>7} "
            f"{'main_C5':>8} {'Δ_C2a_int':>10} {'Δ_C4a_int':>10} "
            f"{'Δ_C2a_main':>11} {'Δ_C4a_main':>11} {'PUB':>7}"
        )
        for subject, resp in TIER2_CELLS:
            t2 = tier2_means(subject, resp, panel)
            t2_c5 = t2.get("C5_baseline")
            t2_c2a = t2.get("C2a_full_spec")
            t2_c4a = t2.get("C4a_full_facts_plus_spec")
            main_c5 = main_study_haiku_c5(subject, panel)
            d_c2a_int = (
                t2_c2a - t2_c5 if t2_c5 is not None and t2_c2a is not None else None
            )
            d_c4a_int = (
                t2_c4a - t2_c5 if t2_c5 is not None and t2_c4a is not None else None
            )
            d_c2a_main = (
                t2_c2a - main_c5 if main_c5 is not None and t2_c2a is not None else None
            )
            d_c4a_main = (
                t2_c4a - main_c5 if main_c5 is not None and t2_c4a is not None else None
            )
            pub = PUBLISHED[(subject, resp)]
            print(
                f"{subject:14} {resp:12} "
                f"{fmt_p(t2_c5)} {fmt_p(t2_c2a)} {fmt_p(t2_c4a)} "
                f"{fmt_p(main_c5)} "
                f"{fmt(d_c2a_int)} {fmt(d_c4a_int)} "
                f"{fmt(d_c2a_main)} {fmt(d_c4a_main)} "
                f"{pub:+7.2f}"
            )

    print("\n" + "=" * 110)
    print(
        "Closest-match analysis: which Δ definition best matches the published values?"
    )
    print("=" * 110)

    candidates = [
        ("Δ_C2a_internal_5judge", PRIMARY_5, "internal", "C2a"),
        ("Δ_C4a_internal_5judge", PRIMARY_5, "internal", "C4a"),
        ("Δ_C2a_internal_7judge", ALL_7, "internal", "C2a"),
        ("Δ_C4a_internal_7judge", ALL_7, "internal", "C4a"),
        ("Δ_C2a_main_baseline_5judge", PRIMARY_5, "main", "C2a"),
        ("Δ_C4a_main_baseline_5judge", PRIMARY_5, "main", "C4a"),
        ("Δ_C2a_main_baseline_7judge", ALL_7, "main", "C2a"),
        ("Δ_C4a_main_baseline_7judge", ALL_7, "main", "C4a"),
    ]
    print(
        f"\n{'definition':35} {'mean_abs_error':>15} {'max_abs_error':>15} "
        f"{'sign_matches':>12}"
    )
    for label, panel, basetype, condtype in candidates:
        errors = []
        sign_matches = 0
        for subject, resp in TIER2_CELLS:
            t2 = tier2_means(subject, resp, panel)
            cond_key = (
                "C2a_full_spec" if condtype == "C2a" else "C4a_full_facts_plus_spec"
            )
            cond_val = t2.get(cond_key)
            if basetype == "internal":
                base = t2.get("C5_baseline")
            else:
                base = main_study_haiku_c5(subject, panel)
            if cond_val is None or base is None:
                continue
            delta = cond_val - base
            pub = PUBLISHED[(subject, resp)]
            errors.append(abs(delta - pub))
            if (delta > 0) == (pub > 0):
                sign_matches += 1
        if errors:
            print(
                f"{label:35} {sum(errors)/len(errors):>15.3f} "
                f"{max(errors):>15.3f} {sign_matches:>10}/{len(errors)}"
            )


if __name__ == "__main__":
    main()
