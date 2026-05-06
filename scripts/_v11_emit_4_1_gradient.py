"""v11 canonical emit script for the §4.1 cross-subject gradient table.

Every number reported in §4.1 of `docs/beyond_recall_v10_1_draft.md` is
re-derived from primary per-judge JSON files by this script. There are no
hardcoded per-subject means.

Aggregation rule (locked across the v10/v11 paper):

    1. For each (subject, condition, judge), gather every per-question score
       from primary JSON. Drop rows where score is None or parse_failure is
       True.
    2. Per-judge per-subject mean = mean of per-question scores within that
       (subject, condition, judge) cell.
    3. Panel mean per-subject per-condition = mean of the per-judge means
       across the 5 panel members {haiku, sonnet, opus, gpt4o, gpt54}.

The 5-judge primary panel is the locked main-text panel. Gemini judges are
sensitivity-only and are NOT part of this emit.

Schema variance is handled in three named branches:

    A. Global subjects (13)
       Source: results/global_<subject>/judgments_v2.json
       Schema: list of {question_id, condition, judge, score, parse_failure}
       Loader: recompute_5judge_primary.load_global_judgments
              (also overlays results/_s114_backfills/global_<subject>__*.json)

    B. Hamerton
       Source: results/hamerton/{judgments_harmonized,judgments,
              <judge>_judgments,gpt54_judgments}.json
       Schema: heterogeneous - long format for some judges/conditions,
              wide format (haiku_score, gemini_score) for others.
              Condition names use legacy 'C2c_full_wrong_spec' and
              'C4a_full_all_facts_plus_spec' which are normalized to
              'C2c_wrong_spec' and 'C4a_full_facts_plus_spec' by the
              shared loader.
       Loader: recompute_5judge_primary.load_hamerton_judgments

    C. Franklin (high-baseline reference, not part of the regression)
       Source: results/franklin_legacy_20260411/analysis/<judge>_judgments.json
       Schema: 5 separate per-judge files. Each has
              {question_id, condition, <judge>_score} (e.g. haiku_score).
              Legacy condition names: 'C2a_spec_only', 'C4a_factdump_plus_spec',
              'C2c_wrong_spec', 'C4_factdump', 'C5_baseline'. These are
              normalized to the v10 paper names below.
              C4_factdump and C2c_wrong_spec only have 3 of the 5 panel
              judges (haiku, sonnet, opus). The 5-judge panel mean is
              emitted as null for these conditions and the cells are
              flagged in summary.franklin_partial_judges.
       Loader: load_franklin_judgments (defined in this script)

The Hamerton 'fullstack_haiku.json' and 'judgments.json' single-judge files
are NOT used here; they predate the 5-judge backfill. The 5-judge panel for
Hamerton lives in:
    judgments_harmonized.json   (C5_baseline + C4_factdump, 7 judges)
    sonnet/opus/gpt4o_judgments.json   (s114 backfill, spec conditions)
    gpt54_judgments.json   (gpt54_score wide field, spec conditions)
    judgments.json   (haiku_score wide field, spec conditions)

Outputs (atomic-written):
    docs/research/v11_emit/4_1_gradient.json
    docs/research/v11_emit/4_1_gradient.md

Constraints:
    - Pure Python.
    - Idempotent: timestamp is a literal, no datetime.now() calls. Running
      twice on unchanged primary data produces byte-identical output.
    - Atomic write: each output is written to <path>.tmp then renamed via
      pathlib.Path.replace().
    - No em-dashes in markdown output.

Verification:
    --verify   Run emit, then compare every emitted scalar to the value as
               stated in §4.1 of docs/beyond_recall_v10_1_draft.md. Exit 0 if
               all match within 0.005 tolerance, exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from scipy.stats import linregress, t as student_t, wilcoxon

# Make sibling scripts importable.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from recompute_5judge_primary import (  # noqa: E402
    load_global_judgments,
    load_hamerton_judgments,
    GLOBAL_SUBJECTS,
)

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OUT_DIR = REPO / "docs" / "research" / "v11_emit"
OUT_JSON = OUT_DIR / "4_1_gradient.json"
OUT_MD = OUT_DIR / "4_1_gradient.md"

# --- Locked constants ---------------------------------------------------------

EMIT_DATE = "2026-04-25"  # literal, for idempotency
SCHEMA_VERSION = "v11.0"
PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]

# Conditions present in main data and required for §4.1.
CONDITIONS = [
    "C5_baseline",
    "C2a_full_spec",
    "C2c_wrong_spec",
    "C4_factdump",
    "C4a_full_facts_plus_spec",
]

# Subject ordering for the §4.1 table (within-band ascending baseline).
# This matches the v10 §4.1 per-subject table.
TABLE_ORDER = [
    "ebers", "sunity_devee", "hamerton", "fukuzawa", "bernal_diaz",
    "babur", "seacole", "keckley", "yung_wing",  # low-baseline (9)
    "zitkala_sa", "cellini", "rousseau", "augustine", "equiano",  # mid (5)
    "franklin",  # high-baseline reference
]

DISPLAY_NAME = {
    "ebers": "Ebers",
    "sunity_devee": "Sunity Devee",
    "hamerton": "Hamerton",
    "fukuzawa": "Fukuzawa",
    "bernal_diaz": "Bernal Diaz",
    "babur": "Babur",
    "seacole": "Seacole",
    "keckley": "Keckley",
    "yung_wing": "Yung Wing",
    "zitkala_sa": "Zitkala-Sa",
    "cellini": "Cellini",
    "rousseau": "Rousseau",
    "augustine": "Augustine",
    "equiano": "Equiano",
    "franklin": "Franklin",
}

# Franklin legacy condition -> v10 paper condition.
FRANKLIN_COND_MAP = {
    "C5_baseline": "C5_baseline",
    "C2a_spec_only": "C2a_full_spec",
    "C4_factdump": "C4_factdump",
    "C2c_wrong_spec": "C2c_wrong_spec",
    "C4a_factdump_plus_spec": "C4a_full_facts_plus_spec",
}

# v10 paper claims, for --verify. Pulled from §4.1 of beyond_recall_v10_1_draft.md.
PAPER_PER_SUBJECT = {
    # subject -> (C5, C2a, C4a, delta_C4a)
    "ebers":        (1.02, 1.54, 2.07, 1.05),
    "sunity_devee": (1.03, 2.27, 2.41, 1.38),
    "hamerton":     (1.26, 2.63, 2.77, 1.51),
    "fukuzawa":     (1.67, 2.35, 2.78, 1.11),
    "bernal_diaz":  (1.70, 2.27, 2.48, 0.78),
    "babur":        (1.76, 1.91, 2.01, 0.25),
    "seacole":      (1.77, 2.48, 2.59, 0.82),
    "keckley":      (1.84, 2.43, 2.44, 0.59),
    "yung_wing":    (1.88, 2.22, 2.40, 0.52),
    "zitkala_sa":   (2.34, 2.03, 2.02, -0.32),
    "cellini":      (2.38, 2.54, 2.53, 0.15),
    "rousseau":     (2.44, 2.81, 2.53, 0.10),
    "augustine":    (2.58, 2.48, 2.70, 0.11),
    "equiano":      (2.77, 2.46, 2.42, -0.35),
    "franklin":     (3.77, 3.37, 3.65, -0.13),
}

PAPER_SUMMARY = {
    "low_baseline_n": 9,
    "low_baseline_mean_delta_C4a": 0.89,
    "all14_n_positive": 12,
    "low_baseline_n_positive": 9,
    "regression_delta_on_C5_slope": -0.96,
    "regression_delta_on_C5_ci_low": -1.24,
    "regression_delta_on_C5_ci_high": -0.67,
    "regression_delta_on_C5_r_squared": 0.82,
    "regression_delta_on_C5_p": 0.000009,  # paper says < 0.001, p = 0.000009
    "regression_C4a_level_on_C5_slope": 0.04,
    "regression_C4a_level_on_C5_ci_low": -0.25,
    "regression_C4a_level_on_C5_ci_high": 0.33,
    "regression_C4a_level_on_C5_r_squared": 0.008,
    "regression_C4a_level_on_C5_p": 0.76,
    "wilcoxon_C5_vs_C2a_W": 10.0,
    "wilcoxon_C5_vs_C2a_p": 0.005,
    "wilcoxon_C5_vs_C4a_W": 11.0,
    "wilcoxon_C5_vs_C4a_p": 0.007,
}

VERIFY_TOLERANCE = 0.005


# --- Loaders ------------------------------------------------------------------


def load_franklin_judgments():
    """Load Franklin per-judge rows from `results/franklin_legacy_20260411/analysis/`.

    Each per-judge file has its own field name (e.g. `haiku_score`). Returns
    list of {question_id, condition, judge, score, parse_failure} dicts in
    the same shape used by the global/hamerton loaders.

    NOTE: only haiku/sonnet/opus have rows for C4_factdump and C2c_wrong_spec
    in the legacy data. gpt4o and gpt54 only have C5/C2a/C4a there. The
    aggregator handles this by emitting null for cells with fewer than the
    full 5 panel judges.
    """
    base = RESULTS / "franklin_legacy_20260411" / "analysis"
    rows = []
    file_map = {
        "haiku": "haiku_judgments.json",
        "sonnet": "sonnet_judgments.json",
        "opus": "opus_judgments.json",
        "gpt4o": "gpt4o_judgments.json",
        "gpt54": "gpt54_judgments.json",
    }
    for judge, fname in file_map.items():
        path = base / fname
        if not path.exists():
            continue
        score_field = f"{judge}_score"
        for r in json.load(path.open(encoding="utf-8")):
            cond_raw = r.get("condition")
            cond = FRANKLIN_COND_MAP.get(cond_raw)
            if cond is None:
                continue
            score = r.get(score_field)
            if score is None:
                continue
            rows.append({
                "question_id": r.get("question_id"),
                "condition": cond,
                "judge": judge,
                "score": score,
                "parse_failure": False,
            })
    return rows


# --- Aggregation --------------------------------------------------------------


def panel_means_for_subject(rows):
    """Return {condition: panel_mean} where panel_mean is the mean of per-judge
    means across the 5 primary panel judges. If a condition is missing one or
    more panel judges, the panel mean is None and the missing judges are listed.

    Returns:
        means: {condition: float | None}
        partial: {condition: [missing_judge_names]} for any condition missing
                 a panel judge. Empty if all conditions have all 5.
    """
    # 1. per-judge per-question scores -> per-judge per-condition mean
    per_jc_scores = defaultdict(list)  # (cond, judge) -> [scores]
    for r in rows:
        if r.get("judge") not in PRIMARY_PANEL:
            continue
        if r.get("parse_failure"):
            continue
        score = r.get("score")
        if score is None:
            continue
        per_jc_scores[(r["condition"], r["judge"])].append(score)

    per_jc_mean = {
        key: statistics.mean(scores)
        for key, scores in per_jc_scores.items()
        if scores
    }

    # 2. for each condition, panel mean = mean across 5 panel judges
    means = {}
    partial = {}
    for cond in CONDITIONS:
        judge_means = []
        missing = []
        for j in PRIMARY_PANEL:
            jm = per_jc_mean.get((cond, j))
            if jm is None:
                missing.append(j)
            else:
                judge_means.append(jm)
        if len(judge_means) == 5:
            means[cond] = statistics.mean(judge_means)
        else:
            means[cond] = None
            if missing and (cond in CONDITIONS):
                # Only flag conditions that had at least one judge present.
                if judge_means:
                    partial[cond] = missing
    return means, partial


# --- Stats --------------------------------------------------------------------


def linregress_with_ci(x, y):
    """scipy.stats.linregress + parametric 95% CI on the slope via t-distribution."""
    res = linregress(x, y)
    n = len(x)
    df = n - 2
    t_crit = student_t.ppf(0.975, df)
    ci_low = res.slope - t_crit * res.stderr
    ci_high = res.slope + t_crit * res.stderr
    return {
        "slope": float(res.slope),
        "intercept": float(res.intercept),
        "ci95_low": float(ci_low),
        "ci95_high": float(ci_high),
        "r_squared": float(res.rvalue ** 2),
        "r": float(res.rvalue),
        "p_value": float(res.pvalue),
        "stderr": float(res.stderr),
        "n": int(n),
    }


# --- Build emit payload -------------------------------------------------------


def build_payload():
    """Compute everything; return a dict matching the locked JSON shape."""
    primary_data_paths = []
    subjects_out = []
    franklin_partial = {}

    for subject in TABLE_ORDER:
        # Pick loader by named branch, document each.
        if subject == "hamerton":
            rows = load_hamerton_judgments()
            primary_data_paths.append("results/hamerton/{judgments_harmonized,judgments,sonnet_judgments,opus_judgments,gpt4o_judgments,gpt54_judgments}.json")
        elif subject == "franklin":
            rows = load_franklin_judgments()
            primary_data_paths.append("results/franklin_legacy_20260411/analysis/{haiku,sonnet,opus,gpt4o,gpt54}_judgments.json")
        else:
            rows = load_global_judgments(subject)
            primary_data_paths.append(f"results/global_{subject}/judgments_v2.json")

        means, partial = panel_means_for_subject(rows)
        if subject == "franklin" and partial:
            franklin_partial = partial

        c5 = means.get("C5_baseline")
        c2a = means.get("C2a_full_spec")
        c2c = means.get("C2c_wrong_spec")
        c4 = means.get("C4_factdump")
        c4a = means.get("C4a_full_facts_plus_spec")

        delta_c4a = (c4a - c5) if (c4a is not None and c5 is not None) else None

        subjects_out.append({
            "id": subject,
            "display_name": DISPLAY_NAME[subject],
            "C5": c5,
            "C2a": c2a,
            "C2c": c2c,
            "C4": c4,
            "C4a": c4a,
            "delta_C4a": delta_c4a,
            "C4a_minus_C5": delta_c4a,  # alias retained per spec
        })

    # Build summary stats over the 14 main-study subjects (Franklin excluded).
    main14 = [s for s in subjects_out if s["id"] != "franklin"]
    assert len(main14) == 14, f"expected 14 main-study subjects, got {len(main14)}"

    # Drop any subjects with missing C5 or C4a from regression (defensive).
    reg_rows = [s for s in main14 if s["C5"] is not None and s["C4a"] is not None]
    c5_vals = [s["C5"] for s in reg_rows]
    c4a_vals = [s["C4a"] for s in reg_rows]
    delta_vals = [s["delta_C4a"] for s in reg_rows]
    c2a_vals = [s["C2a"] for s in reg_rows if s["C2a"] is not None]
    c5_for_c2a = [s["C5"] for s in reg_rows if s["C2a"] is not None]

    reg_delta = linregress_with_ci(c5_vals, delta_vals)
    reg_level = linregress_with_ci(c5_vals, c4a_vals)

    w_c4a, p_c4a = wilcoxon(c5_vals, c4a_vals, alternative="two-sided")
    w_c2a, p_c2a = wilcoxon(c5_for_c2a, c2a_vals, alternative="two-sided")

    low_subjects = [s for s in main14 if s["C5"] is not None and s["C5"] <= 2.0]
    low_subjects_ids = [s["id"] for s in low_subjects]
    low_n = len(low_subjects)
    low_mean_delta = statistics.mean(s["delta_C4a"] for s in low_subjects) if low_subjects else None
    low_mean_c4a = statistics.mean(s["C4a"] for s in low_subjects) if low_subjects else None
    low_n_pos = sum(1 for s in low_subjects if s["delta_C4a"] is not None and s["delta_C4a"] > 0)

    all14_n_pos = sum(1 for s in main14 if s["delta_C4a"] is not None and s["delta_C4a"] > 0)
    all14_mean_delta = statistics.mean(s["delta_C4a"] for s in main14)
    all14_mean_c4a = statistics.mean(s["C4a"] for s in main14)

    franklin = next(s for s in subjects_out if s["id"] == "franklin")

    # Count expected judgments to support provenance audit.
    expected_n_judgments = 0
    for s in subjects_out:
        # Each cell is one (subject, condition, judge, question) record.
        # We count loosely: length of loaded rows after panel-only filter is
        # what feeds the aggregation. Use post-load count for honesty.
        pass  # see provenance.expected_n_judgments below.

    payload = {
        "schema_version": SCHEMA_VERSION,
        "aggregation": "5-judge primary; per-judge per-question -> per-judge per-subject mean -> panel mean",
        "panel": PRIMARY_PANEL,
        "subjects": subjects_out,
        "summary": {
            "n_subjects_total": len(main14),
            "low_baseline_subjects": low_subjects_ids,
            "low_baseline_n": low_n,
            "low_baseline_mean_delta_C4a": low_mean_delta,
            "low_baseline_mean_C4a": low_mean_c4a,
            "low_baseline_n_positive": low_n_pos,
            "all14_mean_delta_C4a": all14_mean_delta,
            "all14_mean_C4a": all14_mean_c4a,
            "all14_n_positive": all14_n_pos,
            "regression_delta_on_C5": {
                "slope": reg_delta["slope"],
                "intercept": reg_delta["intercept"],
                "ci95_low": reg_delta["ci95_low"],
                "ci95_high": reg_delta["ci95_high"],
                "r_squared": reg_delta["r_squared"],
                "r": reg_delta["r"],
                "p_value": reg_delta["p_value"],
                "n": reg_delta["n"],
            },
            "regression_C4a_level_on_C5": {
                "slope": reg_level["slope"],
                "intercept": reg_level["intercept"],
                "ci95_low": reg_level["ci95_low"],
                "ci95_high": reg_level["ci95_high"],
                "r_squared": reg_level["r_squared"],
                "r": reg_level["r"],
                "p_value": reg_level["p_value"],
                "n": reg_level["n"],
            },
            "wilcoxon_C5_vs_C4a": {"W": float(w_c4a), "p": float(p_c4a), "n": len(c5_vals)},
            "wilcoxon_C5_vs_C2a": {"W": float(w_c2a), "p": float(p_c2a), "n": len(c2a_vals)},
            "franklin_high_baseline": {
                "C5": franklin["C5"],
                "C2a": franklin["C2a"],
                "C4a": franklin["C4a"],
                "delta_C4a": franklin["delta_C4a"],
            },
            "franklin_partial_judges": franklin_partial,
        },
        "provenance": {
            "primary_data_paths": primary_data_paths,
            "script": "scripts/_v11_emit_4_1_gradient.py",
            "timestamp": EMIT_DATE,
            "expected_n_judgments": (
                # Each main-study subject has up to 5 conditions x 5 judges
                # x ~39-40 questions; Franklin has 3 conditions full + 2
                # conditions partial. Stored as a coarse audit hint.
                "main14: 5 conds x 5 judges x ~40 questions per subject; "
                "franklin: 3 conds (C5/C2a/C4a) x 5 judges x 40 + 2 conds (C4/C2c) x 3 judges x 40"
            ),
        },
    }
    return payload


# --- Output rendering ---------------------------------------------------------


def fmt(x, digits=2):
    if x is None:
        return "n/a"
    return f"{x:.{digits}f}"


def fmt_signed(x, digits=2):
    if x is None:
        return "n/a"
    sign = "+" if x >= 0 else "-"
    return f"{sign}{abs(x):.{digits}f}"


def compare(scaffold, paper, tol=VERIFY_TOLERANCE):
    """Return ('MATCH', 0.0) or ('MISMATCH(<delta>)', delta_abs) for a paper-vs-scaffold comparison.

    Tolerance is `<= tol` plus a tiny FP epsilon, so values rounded to 2 decimal
    places in the paper (e.g. -0.13) match scaffold values like -0.125 cleanly.
    """
    if scaffold is None and paper is None:
        return ("MATCH", 0.0)
    if scaffold is None or paper is None:
        return ("MISMATCH(missing)", float("inf"))
    delta = scaffold - paper
    if abs(delta) <= tol + 1e-9:
        return ("MATCH", abs(delta))
    return (f"MISMATCH({delta:+.4f})", abs(delta))


def render_markdown(payload):
    lines = []
    lines.append("# v11 emit: §4.1 cross-subject gradient table")
    lines.append("")
    lines.append(f"_Generated by `scripts/_v11_emit_4_1_gradient.py` (timestamp: {EMIT_DATE})_")
    lines.append("")
    lines.append("Aggregation: " + payload["aggregation"])
    lines.append("")
    lines.append("Panel: " + ", ".join(payload["panel"]))
    lines.append("")
    lines.append("## Per-subject table (15 rows: 14 main-study + Franklin reference)")
    lines.append("")
    lines.append("Compared cell-by-cell to the v10 paper §4.1 table. MATCH means within 0.005 of the paper value.")
    lines.append("")
    lines.append("| Subject | C5 (scaffold) | C5 (paper) | C5 verify | C2a (scaffold) | C2a (paper) | C2a verify | C4a (scaffold) | C4a (paper) | C4a verify | dC4a (scaffold) | dC4a (paper) | dC4a verify |")
    lines.append("|---|---:|---:|:--|---:|---:|:--|---:|---:|:--|---:|---:|:--|")

    for s in payload["subjects"]:
        sid = s["id"]
        c5_p, c2a_p, c4a_p, dc4a_p = PAPER_PER_SUBJECT[sid]
        m_c5, _ = compare(s["C5"], c5_p)
        m_c2a, _ = compare(s["C2a"], c2a_p)
        m_c4a, _ = compare(s["C4a"], c4a_p)
        m_dc4a, _ = compare(s["delta_C4a"], dc4a_p)
        lines.append(
            f"| {s['display_name']} | "
            f"{fmt(s['C5'])} | {fmt(c5_p)} | {m_c5} | "
            f"{fmt(s['C2a'])} | {fmt(c2a_p)} | {m_c2a} | "
            f"{fmt(s['C4a'])} | {fmt(c4a_p)} | {m_c4a} | "
            f"{fmt_signed(s['delta_C4a'])} | {fmt_signed(dc4a_p)} | {m_dc4a} |"
        )
    lines.append("")

    sm = payload["summary"]
    rd = sm["regression_delta_on_C5"]
    rl = sm["regression_C4a_level_on_C5"]
    wc4a = sm["wilcoxon_C5_vs_C4a"]
    wc2a = sm["wilcoxon_C5_vs_C2a"]

    lines.append("## Summary statistics (n = 14 main-study; Franklin excluded)")
    lines.append("")
    lines.append("| Metric | Scaffold value | Paper claim | Verify |")
    lines.append("|---|---:|---:|:--|")

    rows = [
        ("Regression slope (Δ_C4a vs C5)", rd["slope"], PAPER_SUMMARY["regression_delta_on_C5_slope"]),
        ("Regression CI low",  rd["ci95_low"], PAPER_SUMMARY["regression_delta_on_C5_ci_low"]),
        ("Regression CI high", rd["ci95_high"], PAPER_SUMMARY["regression_delta_on_C5_ci_high"]),
        ("Regression R^2", rd["r_squared"], PAPER_SUMMARY["regression_delta_on_C5_r_squared"]),
        ("Regression p-value", rd["p_value"], PAPER_SUMMARY["regression_delta_on_C5_p"]),
        ("Level slope (C4a vs C5)", rl["slope"], PAPER_SUMMARY["regression_C4a_level_on_C5_slope"]),
        ("Level CI low",  rl["ci95_low"], PAPER_SUMMARY["regression_C4a_level_on_C5_ci_low"]),
        ("Level CI high", rl["ci95_high"], PAPER_SUMMARY["regression_C4a_level_on_C5_ci_high"]),
        ("Level R^2", rl["r_squared"], PAPER_SUMMARY["regression_C4a_level_on_C5_r_squared"]),
        ("Level p-value", rl["p_value"], PAPER_SUMMARY["regression_C4a_level_on_C5_p"]),
        ("Wilcoxon C5 vs C4a W", wc4a["W"], PAPER_SUMMARY["wilcoxon_C5_vs_C4a_W"]),
        ("Wilcoxon C5 vs C4a p", wc4a["p"], PAPER_SUMMARY["wilcoxon_C5_vs_C4a_p"]),
        ("Wilcoxon C5 vs C2a W", wc2a["W"], PAPER_SUMMARY["wilcoxon_C5_vs_C2a_W"]),
        ("Wilcoxon C5 vs C2a p", wc2a["p"], PAPER_SUMMARY["wilcoxon_C5_vs_C2a_p"]),
        ("Low-baseline n", sm["low_baseline_n"], PAPER_SUMMARY["low_baseline_n"]),
        ("Low-baseline n positive", sm["low_baseline_n_positive"], PAPER_SUMMARY["low_baseline_n_positive"]),
        ("Low-baseline mean dC4a", sm["low_baseline_mean_delta_C4a"], PAPER_SUMMARY["low_baseline_mean_delta_C4a"]),
        ("All-14 n positive", sm["all14_n_positive"], PAPER_SUMMARY["all14_n_positive"]),
    ]
    for label, scaffold, paper in rows:
        m, _ = compare(scaffold, paper)
        lines.append(f"| {label} | {scaffold:.4f} | {paper:.4f} | {m} |"
                     if isinstance(scaffold, float) and isinstance(paper, float)
                     else f"| {label} | {scaffold} | {paper} | {m} |")

    lines.append("")
    lines.append("Franklin (high-baseline reference): " +
                 f"C5={fmt(sm['franklin_high_baseline']['C5'])}, " +
                 f"C2a={fmt(sm['franklin_high_baseline']['C2a'])}, " +
                 f"C4a={fmt(sm['franklin_high_baseline']['C4a'])}, " +
                 f"dC4a={fmt_signed(sm['franklin_high_baseline']['delta_C4a'])}")
    if sm["franklin_partial_judges"]:
        lines.append("")
        lines.append("Franklin partial-judge cells (panel mean emitted as null because not all 5 panel judges have data):")
        for cond, missing in sm["franklin_partial_judges"].items():
            lines.append(f"- {cond}: missing {', '.join(missing)}")

    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    for p in payload["provenance"]["primary_data_paths"]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append(f"Script: `{payload['provenance']['script']}`")
    lines.append("")
    return "\n".join(lines) + "\n"


# --- Atomic write -------------------------------------------------------------


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# --- Verify -------------------------------------------------------------------


def run_verify(payload, verbose=True):
    """Compare every emitted scalar to the v10 paper claim. Return True if all
    pass within VERIFY_TOLERANCE, else False. Prints a per-claim diff."""
    diffs = []  # list of (label, scaffold, paper, status)

    # Per-subject (15 rows x 4 cells)
    for s in payload["subjects"]:
        sid = s["id"]
        c5_p, c2a_p, c4a_p, dc4a_p = PAPER_PER_SUBJECT[sid]
        for label, val, paper_val in [
            (f"{sid}.C5", s["C5"], c5_p),
            (f"{sid}.C2a", s["C2a"], c2a_p),
            (f"{sid}.C4a", s["C4a"], c4a_p),
            (f"{sid}.delta_C4a", s["delta_C4a"], dc4a_p),
        ]:
            status, _ = compare(val, paper_val)
            diffs.append((label, val, paper_val, status))

    # Summary stats
    sm = payload["summary"]
    rd = sm["regression_delta_on_C5"]
    rl = sm["regression_C4a_level_on_C5"]
    wc4a = sm["wilcoxon_C5_vs_C4a"]
    wc2a = sm["wilcoxon_C5_vs_C2a"]
    summary_pairs = [
        ("regression_delta_on_C5.slope", rd["slope"], PAPER_SUMMARY["regression_delta_on_C5_slope"]),
        ("regression_delta_on_C5.ci95_low", rd["ci95_low"], PAPER_SUMMARY["regression_delta_on_C5_ci_low"]),
        ("regression_delta_on_C5.ci95_high", rd["ci95_high"], PAPER_SUMMARY["regression_delta_on_C5_ci_high"]),
        ("regression_delta_on_C5.r_squared", rd["r_squared"], PAPER_SUMMARY["regression_delta_on_C5_r_squared"]),
        ("regression_delta_on_C5.p_value", rd["p_value"], PAPER_SUMMARY["regression_delta_on_C5_p"]),
        ("regression_C4a_level_on_C5.slope", rl["slope"], PAPER_SUMMARY["regression_C4a_level_on_C5_slope"]),
        ("regression_C4a_level_on_C5.ci95_low", rl["ci95_low"], PAPER_SUMMARY["regression_C4a_level_on_C5_ci_low"]),
        ("regression_C4a_level_on_C5.ci95_high", rl["ci95_high"], PAPER_SUMMARY["regression_C4a_level_on_C5_ci_high"]),
        ("regression_C4a_level_on_C5.r_squared", rl["r_squared"], PAPER_SUMMARY["regression_C4a_level_on_C5_r_squared"]),
        ("regression_C4a_level_on_C5.p_value", rl["p_value"], PAPER_SUMMARY["regression_C4a_level_on_C5_p"]),
        ("wilcoxon_C5_vs_C4a.W", wc4a["W"], PAPER_SUMMARY["wilcoxon_C5_vs_C4a_W"]),
        ("wilcoxon_C5_vs_C4a.p", wc4a["p"], PAPER_SUMMARY["wilcoxon_C5_vs_C4a_p"]),
        ("wilcoxon_C5_vs_C2a.W", wc2a["W"], PAPER_SUMMARY["wilcoxon_C5_vs_C2a_W"]),
        ("wilcoxon_C5_vs_C2a.p", wc2a["p"], PAPER_SUMMARY["wilcoxon_C5_vs_C2a_p"]),
        ("low_baseline_n", float(sm["low_baseline_n"]), float(PAPER_SUMMARY["low_baseline_n"])),
        ("low_baseline_n_positive", float(sm["low_baseline_n_positive"]), float(PAPER_SUMMARY["low_baseline_n_positive"])),
        ("low_baseline_mean_delta_C4a", sm["low_baseline_mean_delta_C4a"], PAPER_SUMMARY["low_baseline_mean_delta_C4a"]),
        ("all14_n_positive", float(sm["all14_n_positive"]), float(PAPER_SUMMARY["all14_n_positive"])),
    ]
    for label, scaffold, paper in summary_pairs:
        status, _ = compare(scaffold, paper)
        diffs.append((label, scaffold, paper, status))

    n_match = sum(1 for d in diffs if d[3] == "MATCH")
    n_total = len(diffs)
    if verbose:
        print()
        print("=" * 78)
        print(f"VERIFY: {n_match}/{n_total} cells MATCH within {VERIFY_TOLERANCE}")
        print("=" * 78)
        for label, scaffold, paper, status in diffs:
            if status != "MATCH":
                if isinstance(scaffold, float) and isinstance(paper, float):
                    print(f"  {label:50s} scaffold={scaffold:.4f} paper={paper:.4f} -> {status}")
                else:
                    print(f"  {label:50s} scaffold={scaffold} paper={paper} -> {status}")
        if n_match < n_total:
            print()
            print("(MATCH cells suppressed for brevity; see emit markdown for full table.)")
    return n_match == n_total


# --- Main ---------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--verify", action="store_true",
                        help="After emit, compare every value against v10 paper claims; exit 1 on mismatch.")
    args = parser.parse_args()

    payload = build_payload()

    # Atomic-write JSON
    json_text = json.dumps(payload, indent=2, sort_keys=False)
    atomic_write(OUT_JSON, json_text + "\n")

    # Atomic-write Markdown
    md_text = render_markdown(payload)
    atomic_write(OUT_MD, md_text)

    # Per-subject one-line stdout summary
    print("Section 4.1 gradient emit (5-judge primary panel)")
    print("-" * 78)
    for s in payload["subjects"]:
        marker = "[ref]" if s["id"] == "franklin" else "    "
        print(f"  {marker} {s['display_name']:14s} "
              f"C5={fmt(s['C5'])} "
              f"C2a={fmt(s['C2a'])} "
              f"C2c={fmt(s['C2c'])} "
              f"C4={fmt(s['C4'])} "
              f"C4a={fmt(s['C4a'])} "
              f"dC4a={fmt_signed(s['delta_C4a'])}")

    sm = payload["summary"]
    rd = sm["regression_delta_on_C5"]
    rl = sm["regression_C4a_level_on_C5"]
    wc4a = sm["wilcoxon_C5_vs_C4a"]
    wc2a = sm["wilcoxon_C5_vs_C2a"]
    print()
    print("Stats (n=14 main-study; Franklin excluded):")
    print(f"  Regression Delta_C4a on C5: slope={rd['slope']:+.4f} "
          f"[95% CI {rd['ci95_low']:+.4f}, {rd['ci95_high']:+.4f}] "
          f"R^2={rd['r_squared']:.4f} p={rd['p_value']:.6g}")
    print(f"  Level regression C4a on C5: slope={rl['slope']:+.4f} "
          f"[95% CI {rl['ci95_low']:+.4f}, {rl['ci95_high']:+.4f}] "
          f"R^2={rl['r_squared']:.4f} p={rl['p_value']:.4g}")
    print(f"  Wilcoxon C5 vs C4a: W={wc4a['W']:.1f} p={wc4a['p']:.5f}")
    print(f"  Wilcoxon C5 vs C2a: W={wc2a['W']:.1f} p={wc2a['p']:.5f}")
    print(f"  Low-baseline (n={sm['low_baseline_n']}): "
          f"mean dC4a = {sm['low_baseline_mean_delta_C4a']:+.4f}, "
          f"{sm['low_baseline_n_positive']}/{sm['low_baseline_n']} positive, "
          f"mean C4a = {sm['low_baseline_mean_C4a']:.4f}")
    print(f"  All-14: {sm['all14_n_positive']}/14 positive, mean C4a = {sm['all14_mean_C4a']:.4f}")
    print()
    print(f"JSON: {OUT_JSON}")
    print(f"MD:   {OUT_MD}")

    if args.verify:
        ok = run_verify(payload, verbose=True)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
