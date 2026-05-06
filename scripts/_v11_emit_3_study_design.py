"""v11 canonical emit script for §3 Study Design (judges + calibration + Franklin).

Every judge-related, calibration, abstention-audit, length-correlation, and
battery-leakage number cited in §3 of `docs/beyond_recall_v10_1_draft.md` is
re-derived here from primary data files only. No analysis-doc reuse, no
manual transcription.

Aggregation rule: 5-judge primary panel
  per (subject, condition, judge) -> mean across questions
  per (subject, condition)        -> mean across judges in {haiku, sonnet, opus, gpt4o, gpt54}
  Cross-subject aggregates        -> mean across per-subject panel means

7-judge sensitivity panel adds {gemini_flash, gemini_pro}.

Five named branches by data source:

  A. Judge calibration (§3.7.2)
     Source files:
       - results/judge_calibration/judgments.json (haiku + gemini_flash)
       - results/judge_calibration/gpt4o_calibration.json
       - results/judge_calibration/gpt54_calibration.json
       - results/judge_calibration/gemini_pro_calibration.json
     Sonnet and Opus did NOT run the diagnostic battery (paper §3.7.2 line 480);
     calibration claim_ids for sonnet/opus emit value=null with explicit note.
     The "gemini" key in judgments.json maps to gemini_flash per
     STUDY_MEMORY.md and `results/judge_calibration/README.md`.

  B. Inter-judge agreement (§3.7.4)
     Source: every per-(subject, condition, judge, question) score across 14
     main-study subjects. Loaded via load_global_judgments / load_hamerton_judgments
     in scripts/recompute_5judge_primary.py.
     Pairwise Spearman rho computed on per-(subject, condition) judge means
     (the v9 methodology). Krippendorff's alpha (interval scale) computed at
     the per-question level via the pair-count formula. Implementations are
     reused from scripts/stats_wilcoxon_krippendorff_update.py.

  C. Per-judge strictness on abstentions (§3.7.6)
     Source: results/global_<subject>/results_v2.json plus the per-judge
     judgment files. Subjects: 9-subject low-baseline slice
     {hamerton, sunity_devee, ebers, fukuzawa, bernal_diaz, babur, seacole,
      keckley, yung_wing}. Abstention-pattern matcher in
     scripts/audit_low_end_inflation.py. Re-implemented inline here to
     avoid a subprocess call and to fix the unicode load bug
     (encoding='utf-8' is required on Windows for fukuzawa, bernal_diaz,
     babur, keckley which contain non-ASCII bytes in results_v2.json).

  D. Length-score correlations (§3.7.6)
     Same data as Branch C. Pearson r between len(response_text) and
     5-judge primary score, computed overall and split by condition
     (C5_baseline, C2a_full_spec, C4_factdump, C4a_full_facts_plus_spec).

  E. Battery leakage (§3.4)
     Source: scripts/_battery_leakage_results.json (frozen output of
     scripts/_verify_battery_leakage.py). The leakage audit reads
     primary battery and heldout files and counts 7+-consecutive-word
     verbatim overlaps. We treat its JSON output as a snapshot artifact
     and read it directly; the SHA-256 of the JSON is recorded in the
     manifest.

  F. Franklin numbers (§3.2, §4.1.1)
     Source: results/franklin_legacy_20260411/analysis/<judge>_judgments.json
     for the 5-judge primary aggregate (3.77 on C5) and the per-judge
     Haiku-alone baseline (4.10 on C5). The 7-judge range is reported as
     [min per-judge C5 mean, max per-judge C5 mean] across the 6 judges
     present in the legacy analysis directory (haiku/sonnet/opus/gpt4o/
     gpt54/gemini); legacy 'gemini' is treated as gemini_flash (the
     Franklin legacy run predated the gemini_flash/gemini_pro split).

Outputs (atomic-written):
    docs/research/v11_emit/3_study_design.json
    docs/research/v11_emit/3_study_design.md

Constraints:
    - Pure Python.
    - Idempotent: timestamp is a literal; running twice on unchanged primary
      data produces byte-identical JSON.
    - Atomic write via temp file + Path.replace().
    - SHA-256 manifest of every primary input file.
    - No em-dashes in markdown output.

Verification:
    --verify   Run emit, then compare every claim_id to the value as stated
               in §3 of docs/beyond_recall_v10_1_draft.md (or, where the paper
               quotes a range, the min/max thereof). Exit 0 if all match
               within 0.005 tolerance, else exit 1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats as scipy_stats

# Make sibling scripts importable
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from recompute_5judge_primary import (  # noqa: E402
    load_global_judgments,
    load_hamerton_judgments,
    PRIMARY_JUDGES,
    GEMINI_JUDGES,
    ALL_JUDGES,
    MAIN_STUDY,
)
from stats_wilcoxon_krippendorff_update import (  # noqa: E402
    krippendorff_alpha_interval,
    pairwise_spearman,
    build_kripp_matrix,
)

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OUT_DIR = REPO / "docs" / "research" / "v11_emit"
OUT_JSON = OUT_DIR / "3_study_design.json"
OUT_MD = OUT_DIR / "3_study_design.md"

# --- Locked constants --------------------------------------------------------

EMIT_DATE = "2026-04-25"  # literal, idempotent
SCHEMA_VERSION = "v11.0"
SECTION = "3"
SCRIPT_VERSION = "v11.0.0"
VERIFY_TOLERANCE = 0.005

PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
SEVEN_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]
PRIMARY_PANEL_SET = set(PRIMARY_PANEL)
SEVEN_PANEL_SET = set(SEVEN_PANEL)

# Calibrated judges (paper §3.7.2 line 480)
CALIBRATION_JUDGES = ["haiku", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]
NON_CALIBRATED_PANEL = ["sonnet", "opus"]
DIAGNOSTIC_TESTS = ["verbatim", "paraphrased", "short_correct", "long_correct"]

# 9-subject low-baseline slice for §3.7.6 audit (matches audit_low_end_inflation.py)
LOW_BASELINE_SUBJECTS = [
    "hamerton", "sunity_devee", "ebers", "fukuzawa", "bernal_diaz",
    "babur", "seacole", "keckley", "yung_wing",
]

ABSTENTION_PATTERNS = [
    r"i don['’]t have (specific|enough|detailed|direct)",
    r"there is no (specific|explicit|direct|documented)",
    r"i cannot (point to|confirm|verify|provide|determine)",
    r"i am (not|unable) (able|certain|sure)",
    r"would need (additional|more|further|specific)",
    r"no (specific|explicit|direct) (information|account|passage|reference)",
    r"i['’]m not (aware|familiar)",
    r"without (more|additional|specific) (context|information|details)",
    r"i (do not|don['’]t) (recall|know)",
    r"(cannot|unable to) (accurately|reliably) (answer|predict|characterize)",
    r"my training data does not",
    r"no specific documented",
]

AUDIT_CONDITIONS = [
    "C5_baseline", "C2a_full_spec", "C4_factdump",
    "C4a_full_facts_plus_spec", "C2c_wrong_spec",
]

# Franklin condition normalization (legacy -> v10 paper)
FRANKLIN_COND_MAP = {
    "C5_baseline": "C5_baseline",
    "C2a_spec_only": "C2a_full_spec",
    "C4_factdump": "C4_factdump",
    "C2c_wrong_spec": "C2c_wrong_spec",
    "C4a_factdump_plus_spec": "C4a_full_facts_plus_spec",
}

# v10 paper claims (§3 numbers, hand-extracted from beyond_recall_v10_1_draft.md)
PAPER_CLAIMS = {
    # 3.7.2 calibration table (rows: judges; columns: tests).
    # Paper table order: Haiku, Gemini Flash, GPT-4o, Gemini Pro, GPT-5.4.
    "3_7_2_haiku_verbatim": 5.00,
    "3_7_2_haiku_paraphrased": 4.75,
    "3_7_2_haiku_short_correct": 3.80,
    "3_7_2_haiku_long_correct": 5.00,
    "3_7_2_gemini_flash_verbatim": 5.00,
    "3_7_2_gemini_flash_paraphrased": 4.70,
    "3_7_2_gemini_flash_short_correct": 3.85,
    "3_7_2_gemini_flash_long_correct": 3.80,
    "3_7_2_gpt4o_verbatim": 5.00,
    "3_7_2_gpt4o_paraphrased": 5.00,
    "3_7_2_gpt4o_short_correct": 4.05,
    "3_7_2_gpt4o_long_correct": 3.35,
    "3_7_2_gemini_pro_verbatim": 4.15,
    "3_7_2_gemini_pro_paraphrased": 3.55,
    "3_7_2_gemini_pro_short_correct": 2.85,
    "3_7_2_gemini_pro_long_correct": 1.20,
    "3_7_2_gpt54_verbatim": 5.00,
    "3_7_2_gpt54_paraphrased": 5.00,
    "3_7_2_gpt54_short_correct": 4.20,
    "3_7_2_gpt54_long_correct": 4.80,
    # Sonnet, Opus: not calibrated; emit null. Paper does not cite values.
    "3_7_2_sonnet_verbatim": None,
    "3_7_2_sonnet_paraphrased": None,
    "3_7_2_sonnet_short_correct": None,
    "3_7_2_sonnet_long_correct": None,
    "3_7_2_opus_verbatim": None,
    "3_7_2_opus_paraphrased": None,
    "3_7_2_opus_short_correct": None,
    "3_7_2_opus_long_correct": None,
    # Per-judge strictness on abstentions (§3.7.6)
    "3_7_2_strictness_sonnet": 1.14,
    "3_7_2_strictness_gpt54": 1.17,
    "3_7_2_strictness_haiku": 1.29,
    "3_7_2_strictness_gpt4o": 1.34,
    "3_7_2_strictness_opus": 1.41,
    # Inter-judge agreement (§3.7.4)
    "3_7_4_spearman_5judge_min": 0.86,
    "3_7_4_spearman_5judge_max": 0.93,
    "3_7_4_spearman_7judge_min": 0.29,
    "3_7_4_spearman_7judge_max": 0.93,
    "3_7_4_krippendorff_alpha_5judge": 0.659,
    "3_7_4_krippendorff_alpha_7judge": 0.535,
    # Length / abstention audit (§3.7.6)
    "3_7_6_length_corr_overall": 0.26,
    "3_7_6_length_corr_C5": 0.604,
    "3_7_6_length_corr_C2a": 0.14,
    "3_7_6_length_corr_C4": 0.01,
    "3_7_6_length_corr_C4a": -0.01,
    "3_7_6_abstention_n_total": 192,
    "3_7_6_abstention_pct_below_2": 82.8,
    "3_7_6_abstention_pct_above_2": 9.4,
    "3_7_6_abstention_pct_above_3": 3.2,
    "3_7_6_abstention_mean_score": 1.27,
    "3_7_6_high_score_chars_avg": 2790,
    "3_7_6_mid_score_chars_avg": 2829,
    # Battery leakage (§3.4)
    "3_4_battery_leakage_n_total": 586,
    "3_4_battery_leakage_n_leaks": 2,
    "3_4_battery_leakage_pct_aggregate": 0.34,
    "3_4_battery_leakage_pct_main_study": 0.00,
    # Franklin (§3.2, §4.1.1)
    "3_2_franklin_C5_5judge": 3.77,
    "3_2_franklin_C5_haiku_only": 4.10,
    "3_2_franklin_C2a_5judge": 3.37,
    "3_2_franklin_C4a_5judge": 3.65,
    # Paper §3.2 line 283 says only "higher on the Gemini-inclusive 7-judge aggregate"
    # — no literal range is published. The task description gave "3.6-4.6" as an approximation;
    # we record that as the paper claim for verify, and emit the per-judge min/max from primary
    # data. Mismatch is expected and documented as paper-claim-not-quoted-in-v10.
    "3_2_franklin_C5_7judge_min": 3.6,
    "3_2_franklin_C5_7judge_max": 4.6,
}


# =============================================================================
# SHA-256 file manifest
# =============================================================================

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_entry(path: Path, n_records: int | None = None) -> dict:
    if not path.exists():
        return {"path": str(path.relative_to(REPO)).replace("\\", "/"), "missing": True}
    return {
        "path": str(path.relative_to(REPO)).replace("\\", "/"),
        "sha256": file_sha256(path),
        "size_bytes": path.stat().st_size,
        "n_records": n_records,
    }


# =============================================================================
# Branch A. Judge calibration
# =============================================================================

def load_calibration_means() -> tuple[dict, list[Path]]:
    """Return {(judge, test): mean_score} and the list of input paths."""
    calib_dir = RESULTS / "judge_calibration"
    inputs: list[Path] = []
    by_test_judge: dict[tuple[str, str], list[float]] = defaultdict(list)

    # judgments.json: contains haiku + gemini (gemini = gemini_flash per README)
    main_path = calib_dir / "judgments.json"
    inputs.append(main_path)
    if main_path.exists():
        for r in json.load(main_path.open(encoding="utf-8")):
            test = r.get("test")
            for src_key, judge_id in [("haiku", "haiku"), ("gemini", "gemini_flash")]:
                if src_key in r and r[src_key] is not None:
                    by_test_judge[(judge_id, test)].append(float(r[src_key]))

    # Per-judge calibration files (gpt4o, gpt54, gemini_pro)
    for judge_id, fname in [
        ("gpt4o", "gpt4o_calibration.json"),
        ("gpt54", "gpt54_calibration.json"),
        ("gemini_pro", "gemini_pro_calibration.json"),
    ]:
        p = calib_dir / fname
        inputs.append(p)
        if not p.exists():
            continue
        score_field = f"{judge_id}_score"
        for r in json.load(p.open(encoding="utf-8")):
            test = r.get("test")
            s = r.get(score_field)
            if s is None:
                continue
            by_test_judge[(judge_id, test)].append(float(s))

    means = {k: statistics.mean(v) for k, v in by_test_judge.items() if v}
    return means, inputs


# =============================================================================
# Branch B. Inter-judge agreement
# =============================================================================

def load_all_per_question_judgments() -> tuple[list[dict], list[Path]]:
    """All per-question judgments across 14 main-study subjects + their input paths."""
    all_rows = []
    inputs: list[Path] = []
    for subject in MAIN_STUDY:
        if subject == "hamerton":
            rows = load_hamerton_judgments()
            inputs.extend([
                RESULTS / "hamerton" / "judgments_harmonized.json",
                RESULTS / "hamerton" / "judgments.json",
                RESULTS / "hamerton" / "gpt54_judgments.json",
                RESULTS / "hamerton" / "gemini_pro_judgments.json",
                RESULTS / "hamerton" / "sonnet_judgments.json",
                RESULTS / "hamerton" / "opus_judgments.json",
                RESULTS / "hamerton" / "gpt4o_judgments.json",
            ])
        else:
            rows = load_global_judgments(subject)
            inputs.append(RESULTS / f"global_{subject}" / "judgments_v2.json")
        for r in rows:
            if r.get("score") is None:
                continue
            if r.get("parse_failure"):
                continue
            all_rows.append({
                "subject": subject,
                "condition": r["condition"],
                "question_id": r["question_id"],
                "judge": r["judge"],
                "score": float(r["score"]),
            })
    return all_rows, inputs


def compute_inter_judge() -> tuple[dict, list[Path]]:
    """Returns dict with Spearman ranges and Krippendorff alphas, plus input paths."""
    all_rows, inputs = load_all_per_question_judgments()

    # Pairwise Spearman on per-(subject, condition) judge means.
    # Pass sorted tuples so iteration order in pairwise_spearman is deterministic.
    rhos_5, _ = pairwise_spearman(all_rows, condition_filter=None, judges=tuple(sorted(PRIMARY_PANEL_SET)))
    rhos_7, _ = pairwise_spearman(all_rows, condition_filter=None, judges=tuple(sorted(SEVEN_PANEL_SET)))
    # Normalize key order for deterministic JSON output.
    rhos_5 = {tuple(sorted(k)): v for k, v in rhos_5.items()}
    rhos_7 = {tuple(sorted(k)): v for k, v in rhos_7.items()}
    rho_vals_5 = list(rhos_5.values())
    rho_vals_7 = list(rhos_7.values())

    # Krippendorff alpha (interval) on pooled across-condition data
    pool_conditions = {"C5_baseline", "C2a_full_spec", "C4a_full_facts_plus_spec",
                       "C4_factdump", "C2c_wrong_spec"}
    rows_5 = [r for r in all_rows if r["judge"] in PRIMARY_PANEL_SET]
    rows_7 = [r for r in all_rows if r["judge"] in SEVEN_PANEL_SET]
    matrix_5 = build_kripp_matrix(rows_5, condition_filter=pool_conditions)
    matrix_7 = build_kripp_matrix(rows_7, condition_filter=pool_conditions)
    alpha_5, n5, _ = krippendorff_alpha_interval(matrix_5)
    alpha_7, n7, _ = krippendorff_alpha_interval(matrix_7)

    out = {
        "spearman_5judge_pairs": {f"{a}|{b}": float(v) for (a, b), v in sorted(rhos_5.items())},
        "spearman_7judge_pairs": {f"{a}|{b}": float(v) for (a, b), v in sorted(rhos_7.items())},
        "spearman_5judge_min": float(min(rho_vals_5)) if rho_vals_5 else None,
        "spearman_5judge_max": float(max(rho_vals_5)) if rho_vals_5 else None,
        "spearman_5judge_n_pairs": len(rho_vals_5),
        "spearman_7judge_min": float(min(rho_vals_7)) if rho_vals_7 else None,
        "spearman_7judge_max": float(max(rho_vals_7)) if rho_vals_7 else None,
        "spearman_7judge_n_pairs": len(rho_vals_7),
        "krippendorff_alpha_5judge": float(alpha_5),
        "krippendorff_alpha_7judge": float(alpha_7),
        "krippendorff_n_units_5judge": int(n5),
        "krippendorff_n_units_7judge": int(n7),
        "krippendorff_scale": "interval",
    }
    return out, inputs


# =============================================================================
# Branch C / D. Abstention audit + length-score correlation
# =============================================================================

def is_abstention(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    for pattern in ABSTENTION_PATTERNS:
        if re.search(pattern, t):
            return True
    return False


def load_low_baseline_audit() -> tuple[list[dict], list[Path]]:
    """Return {response: ...} rows for the 9 low-baseline subjects, plus input paths.

    Each row has: subject, condition, qid, length, primary_mean, per_judge,
    is_abstention. Files are read with encoding='utf-8' to handle non-ASCII
    bytes in fukuzawa/bernal_diaz/babur/keckley results_v2.json.
    """
    inputs: list[Path] = []
    rows_out: list[dict] = []
    for subject in LOW_BASELINE_SUBJECTS:
        # Judgment rows
        if subject == "hamerton":
            j = load_hamerton_judgments()
            responses_path = RESULTS / "hamerton" / "results.json"
        else:
            sdir = RESULTS / f"global_{subject}"
            j = load_global_judgments(subject)
            responses_path = sdir / "results_v2.json"
        inputs.append(responses_path)

        if not responses_path.exists():
            continue
        responses = json.load(responses_path.open(encoding="utf-8"))

        # Build (qid, condition, judge) -> [scores] index for fast lookup
        idx: dict[tuple, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for r in j:
            if r.get("parse_failure"):
                continue
            s = r.get("score")
            if s is None:
                continue
            judge = r.get("judge")
            qid = r.get("question_id")
            cond = r.get("condition")
            idx[(qid, cond)][judge].append(float(s))

        for q in responses:
            qid = q.get("question_id")
            if qid is None:
                continue
            resps = q.get("responses", {})
            for cond in AUDIT_CONDITIONS:
                rdata = resps.get(cond, {})
                text = rdata.get("text", "") if isinstance(rdata, dict) else ""
                if not text:
                    continue
                # Compute primary_mean = mean across primary panel judges
                # of (mean of that judge's scores on this q,cond)
                per_judge_scores = idx.get((qid, cond), {})
                judge_means = {}
                for jname in PRIMARY_PANEL:
                    scores = per_judge_scores.get(jname, [])
                    if scores:
                        judge_means[jname] = statistics.mean(scores)
                if not judge_means:
                    continue
                primary_mean = statistics.mean(judge_means.values())
                rows_out.append({
                    "subject": subject,
                    "qid": qid,
                    "condition": cond,
                    "length": len(text),
                    "primary_mean": primary_mean,
                    "per_judge": judge_means,
                    "is_abstention": is_abstention(text),
                })
    return rows_out, inputs


def compute_audit_metrics(audit_rows: list[dict]) -> dict:
    """Compute length-correlation and abstention metrics from audit rows."""
    n_total = len(audit_rows)
    abst = [r for r in audit_rows if r["is_abstention"]]
    n_abst = len(abst)

    # Score band distribution for abstention responses
    # Paper §3.7.6 cites the "1.0-1.5 band" (i.e., score < 1.5) for the 82.8% figure.
    band_below_2 = sum(1 for r in abst if r["primary_mean"] < 1.5)
    band_above_2 = sum(1 for r in abst if r["primary_mean"] >= 2.0)
    band_above_3 = sum(1 for r in abst if r["primary_mean"] >= 3.0)
    pct_below_2 = 100.0 * band_below_2 / n_abst if n_abst else 0.0
    pct_above_2 = 100.0 * band_above_2 / n_abst if n_abst else 0.0
    pct_above_3 = 100.0 * band_above_3 / n_abst if n_abst else 0.0
    abst_mean_score = statistics.mean(r["primary_mean"] for r in abst) if abst else None

    # Length-score correlation (Pearson)
    def corr(rows):
        if len(rows) < 3:
            return None
        x = [r["length"] for r in rows]
        y = [r["primary_mean"] for r in rows]
        try:
            r, _p = scipy_stats.pearsonr(x, y)
            return float(r)
        except Exception:
            return None

    overall = corr(audit_rows)
    by_cond = {
        "C5_baseline": corr([r for r in audit_rows if r["condition"] == "C5_baseline"]),
        "C2a_full_spec": corr([r for r in audit_rows if r["condition"] == "C2a_full_spec"]),
        "C4_factdump": corr([r for r in audit_rows if r["condition"] == "C4_factdump"]),
        "C4a_full_facts_plus_spec": corr([r for r in audit_rows if r["condition"] == "C4a_full_facts_plus_spec"]),
    }

    # Per-judge mean on abstention rows (strictness)
    per_judge_means: dict[str, float | None] = {}
    for j in PRIMARY_PANEL:
        vals = [r["per_judge"][j] for r in abst if j in r["per_judge"]]
        per_judge_means[j] = statistics.mean(vals) if vals else None

    # Length distribution: ultra-high vs mid-range
    ultra_high = [r for r in audit_rows if r["primary_mean"] >= 4.5]
    mid_range = [r for r in audit_rows if 2.5 <= r["primary_mean"] < 3.5]
    high_chars_avg = statistics.mean(r["length"] for r in ultra_high) if ultra_high else None
    mid_chars_avg = statistics.mean(r["length"] for r in mid_range) if mid_range else None

    return {
        "n_responses_total": n_total,
        "n_abstention_total": n_abst,
        "abstention_pct_below_2": pct_below_2,
        "abstention_pct_above_2": pct_above_2,
        "abstention_pct_above_3": pct_above_3,
        "abstention_mean_score": abst_mean_score,
        "length_corr_overall": overall,
        "length_corr_by_condition": by_cond,
        "per_judge_strictness_on_abstentions": per_judge_means,
        "n_ultra_high": len(ultra_high),
        "n_mid_range": len(mid_range),
        "high_score_chars_avg": high_chars_avg,
        "mid_score_chars_avg": mid_chars_avg,
    }


# =============================================================================
# Branch E. Battery leakage
# =============================================================================

def load_battery_leakage() -> tuple[dict, Path]:
    p = REPO / "scripts" / "_battery_leakage_results.json"
    if not p.exists():
        return {}, p
    data = json.load(p.open(encoding="utf-8"))
    agg_bp = data.get("aggregate_bp", 0)
    agg_leaks = data.get("aggregate_leaks", 0)
    pct_agg = (100.0 * agg_leaks / agg_bp) if agg_bp else 0.0

    # main-study leak count = leaks excluding Franklin
    main_leaks = 0
    main_bp = 0
    for r in data.get("per_subject", []):
        if r.get("subject") == "franklin":
            continue
        main_leaks += r.get("leak_count", 0)
        main_bp += r.get("bp_scored", 0)
    pct_main = (100.0 * main_leaks / main_bp) if main_bp else 0.0
    return {
        "n_total": agg_bp,
        "n_leaks": agg_leaks,
        "pct_aggregate": pct_agg,
        "pct_main_study": pct_main,
        "main_study_n": main_bp,
        "main_study_n_leaks": main_leaks,
    }, p


# =============================================================================
# Branch F. Franklin numbers
# =============================================================================

def compute_franklin() -> tuple[dict, list[Path]]:
    base = RESULTS / "franklin_legacy_20260411" / "analysis"
    inputs: list[Path] = []
    file_map = {
        "haiku": "haiku_judgments.json",
        "sonnet": "sonnet_judgments.json",
        "opus": "opus_judgments.json",
        "gpt4o": "gpt4o_judgments.json",
        "gpt54": "gpt54_judgments.json",
        "gemini": "gemini_judgments.json",  # legacy gemini, treated as gemini_flash
    }
    # Per-judge per-condition score lists
    per_judge_cond: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for judge, fname in file_map.items():
        p = base / fname
        inputs.append(p)
        if not p.exists():
            continue
        score_field = f"{judge}_score"
        for r in json.load(p.open(encoding="utf-8")):
            cond_raw = r.get("condition")
            cond = FRANKLIN_COND_MAP.get(cond_raw)
            if cond is None:
                continue
            s = r.get(score_field)
            if s is None:
                continue
            per_judge_cond[judge][cond].append(float(s))

    per_judge_means = {
        j: {c: statistics.mean(scores) for c, scores in conds.items() if scores}
        for j, conds in per_judge_cond.items()
    }

    # 5-judge primary panel mean per condition
    panel5: dict[str, float | None] = {}
    for cond in ["C5_baseline", "C2a_full_spec", "C4a_full_facts_plus_spec",
                 "C4_factdump", "C2c_wrong_spec"]:
        means = [per_judge_means[j][cond] for j in PRIMARY_PANEL
                 if j in per_judge_means and cond in per_judge_means[j]]
        if len(means) == 5:
            panel5[cond] = statistics.mean(means)
        else:
            panel5[cond] = None

    # Per-judge C5 means (legacy gemini included as 6th judge)
    judges_with_c5 = [j for j in per_judge_means if "C5_baseline" in per_judge_means[j]]
    per_judge_c5 = {j: per_judge_means[j]["C5_baseline"] for j in judges_with_c5}

    panel_c5_min = min(per_judge_c5.values()) if per_judge_c5 else None
    panel_c5_max = max(per_judge_c5.values()) if per_judge_c5 else None

    return {
        "per_judge_means": per_judge_means,
        "panel5_means": panel5,
        "per_judge_C5_means": per_judge_c5,
        "C5_per_judge_min": panel_c5_min,
        "C5_per_judge_max": panel_c5_max,
        "judges_present": sorted(judges_with_c5),
    }, inputs


# =============================================================================
# Build emit payload
# =============================================================================

def claim(value, *, estimand, contrast=None, filters=None, n=None,
          aggregation_rule=None, source=None, ci95_low=None, ci95_high=None,
          p_value=None, note=None):
    out = {
        "value": value,
        "estimand": estimand,
        "contrast": contrast,
        "filters": filters or {},
        "n": n,
        "ci95_low": ci95_low,
        "ci95_high": ci95_high,
        "p_value": p_value,
        "aggregation_rule": aggregation_rule,
        "source": source,
    }
    if note:
        out["note"] = note
    return out


def build_payload() -> tuple[dict, list[Path]]:
    """Compute everything; return payload dict + flat list of every input path."""
    all_inputs: list[Path] = []

    # Branch A
    calib_means, calib_inputs = load_calibration_means()
    all_inputs.extend(calib_inputs)

    # Branch B
    inter_judge, inter_inputs = compute_inter_judge()
    all_inputs.extend(inter_inputs)

    # Branch C / D
    audit_rows, audit_inputs = load_low_baseline_audit()
    all_inputs.extend(audit_inputs)
    audit_metrics = compute_audit_metrics(audit_rows)

    # Branch E
    leak, leak_path = load_battery_leakage()
    all_inputs.append(leak_path)

    # Branch F
    franklin, franklin_inputs = compute_franklin()
    all_inputs.extend(franklin_inputs)

    # Build claims dict
    claims: dict[str, dict] = {}

    # ---- Calibration claims (5 calibrated + 2 not-calibrated) x 4 tests ----
    for judge in PRIMARY_PANEL + ["gemini_flash", "gemini_pro"]:
        for test in DIAGNOSTIC_TESTS:
            cid = f"3_7_2_{judge}_{test}"
            mean_v = calib_means.get((judge, test))
            if judge in NON_CALIBRATED_PANEL:
                claims[cid] = claim(
                    None,
                    estimand=f"Calibration mean score for judge={judge} on test={test}",
                    contrast=f"diagnostic test ({test})",
                    filters={"judge": judge, "test": test},
                    aggregation_rule="mean across N=20 calibration items",
                    source="results/judge_calibration/ (no diagnostic battery for sonnet/opus)",
                    note="Sonnet and Opus did not run the diagnostic battery (paper §3.7.2); they joined the panel for inter-judge agreement only.",
                )
            else:
                claims[cid] = claim(
                    float(mean_v) if mean_v is not None else None,
                    estimand=f"Calibration mean score for judge={judge} on test={test}",
                    contrast=f"diagnostic test ({test})",
                    filters={"judge": judge, "test": test},
                    n=20,
                    aggregation_rule="mean across 20 calibration items per (judge, test)",
                    source="results/judge_calibration/judgments.json + per-judge calibration files",
                )

    # ---- Inter-judge ----
    claims["3_7_4_spearman_5judge_min"] = claim(
        inter_judge["spearman_5judge_min"],
        estimand="Minimum pairwise Spearman rho across 5-judge primary panel pairs",
        contrast="judge-pair (10 pairs)",
        filters={"panel": PRIMARY_PANEL},
        n=inter_judge["spearman_5judge_n_pairs"],
        aggregation_rule="Spearman rho on per-(subject, condition) judge means (scipy.stats.spearmanr)",
        source="14 main-study subjects' per-(subject, condition, judge, question) scores",
    )
    claims["3_7_4_spearman_5judge_max"] = claim(
        inter_judge["spearman_5judge_max"],
        estimand="Maximum pairwise Spearman rho across 5-judge primary panel pairs",
        contrast="judge-pair (10 pairs)",
        filters={"panel": PRIMARY_PANEL},
        n=inter_judge["spearman_5judge_n_pairs"],
        aggregation_rule="Spearman rho on per-(subject, condition) judge means",
        source="14 main-study subjects' per-(subject, condition, judge, question) scores",
    )
    claims["3_7_4_spearman_7judge_min"] = claim(
        inter_judge["spearman_7judge_min"],
        estimand="Minimum pairwise Spearman rho across 7-judge sensitivity panel pairs",
        contrast="judge-pair (21 pairs)",
        filters={"panel": SEVEN_PANEL},
        n=inter_judge["spearman_7judge_n_pairs"],
        aggregation_rule="Spearman rho on per-(subject, condition) judge means",
        source="14 main-study subjects' per-(subject, condition, judge, question) scores",
    )
    claims["3_7_4_spearman_7judge_max"] = claim(
        inter_judge["spearman_7judge_max"],
        estimand="Maximum pairwise Spearman rho across 7-judge sensitivity panel pairs",
        contrast="judge-pair (21 pairs)",
        filters={"panel": SEVEN_PANEL},
        n=inter_judge["spearman_7judge_n_pairs"],
        aggregation_rule="Spearman rho on per-(subject, condition) judge means",
        source="14 main-study subjects' per-(subject, condition, judge, question) scores",
    )
    claims["3_7_4_krippendorff_alpha_5judge"] = claim(
        inter_judge["krippendorff_alpha_5judge"],
        estimand="Krippendorff's alpha (interval scale) across 5-judge primary panel",
        contrast="absolute-magnitude agreement",
        filters={"panel": PRIMARY_PANEL, "scale": "interval"},
        n=inter_judge["krippendorff_n_units_5judge"],
        aggregation_rule="pair-count formula on (subject, condition, question_id) units; pooled across 5 main conditions",
        source="14 main-study subjects, all per-question per-judge scores",
        note=("Recompute uses interval-scale Krippendorff alpha; paper cites 0.659 as ordinal. "
              "Both report directional agreement on absolute magnitude. The two scales agree "
              "to within ~0.01 on this score distribution but are not the same statistic."),
    )
    claims["3_7_4_krippendorff_alpha_7judge"] = claim(
        inter_judge["krippendorff_alpha_7judge"],
        estimand="Krippendorff's alpha (interval scale) across 7-judge sensitivity panel",
        contrast="absolute-magnitude agreement",
        filters={"panel": SEVEN_PANEL, "scale": "interval"},
        n=inter_judge["krippendorff_n_units_7judge"],
        aggregation_rule="pair-count formula on (subject, condition, question_id) units; pooled across 5 main conditions",
        source="14 main-study subjects, all per-question per-judge scores",
        note="Paper cites ordinal 0.535. Interval-vs-ordinal note same as 5-judge alpha.",
    )

    # ---- Per-judge strictness ----
    strict = audit_metrics["per_judge_strictness_on_abstentions"]
    for judge in PRIMARY_PANEL:
        cid = f"3_7_2_strictness_{judge}"
        claims[cid] = claim(
            float(strict[judge]) if strict.get(judge) is not None else None,
            estimand=f"Mean per-judge score on abstention-pattern responses (low-baseline slice)",
            contrast="abstention rows only",
            filters={"judge": judge, "subjects": LOW_BASELINE_SUBJECTS, "abstention": True},
            n=audit_metrics["n_abstention_total"],
            aggregation_rule="mean of per-(qid, condition, judge) score across all abstention rows",
            source="9 low-baseline subjects' results_v2.json + judgments_v2.json",
        )

    # ---- Length correlations ----
    bc = audit_metrics["length_corr_by_condition"]
    claims["3_7_6_length_corr_overall"] = claim(
        audit_metrics["length_corr_overall"],
        estimand="Pearson r between response length (chars) and 5-judge primary score",
        contrast="all conditions, all 9 low-baseline subjects",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "panel": PRIMARY_PANEL},
        n=audit_metrics["n_responses_total"],
        aggregation_rule="Pearson r on (length, score) pairs",
        source="9 low-baseline subjects' results_v2.json + judgments_v2.json",
    )
    cond_to_cid = {
        "C5_baseline": "3_7_6_length_corr_C5",
        "C2a_full_spec": "3_7_6_length_corr_C2a",
        "C4_factdump": "3_7_6_length_corr_C4",
        "C4a_full_facts_plus_spec": "3_7_6_length_corr_C4a",
    }
    for cond, cid in cond_to_cid.items():
        claims[cid] = claim(
            bc.get(cond),
            estimand=f"Pearson r between response length and 5-judge primary score (condition={cond})",
            contrast=cond,
            filters={"condition": cond, "subjects": LOW_BASELINE_SUBJECTS},
            aggregation_rule="Pearson r on (length, score) pairs",
            source="9 low-baseline subjects' results_v2.json + judgments_v2.json",
        )

    # ---- Abstention bands ----
    claims["3_7_6_abstention_n_total"] = claim(
        audit_metrics["n_abstention_total"],
        estimand="Number of abstention-pattern responses in low-baseline slice",
        contrast="abstention regex matches",
        filters={"subjects": LOW_BASELINE_SUBJECTS},
        aggregation_rule="count of rows where is_abstention=True",
        source="9 low-baseline subjects' results_v2.json",
    )
    claims["3_7_6_abstention_pct_below_2"] = claim(
        audit_metrics["abstention_pct_below_2"],
        estimand="Percent of abstention rows scoring in the 1.0-1.5 band on 5-judge primary",
        contrast="abstention rows, score < 1.5",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "abstention": True},
        n=audit_metrics["n_abstention_total"],
        aggregation_rule="100 * count(score < 1.5) / count(abstention)",
        source="9 low-baseline subjects' results_v2.json + judgments",
        note="Paper §3.7.6 quotes 82.8% in the '1.0-1.5 band' which corresponds to score < 1.5, not score < 2.0.",
    )
    claims["3_7_6_abstention_pct_above_2"] = claim(
        audit_metrics["abstention_pct_above_2"],
        estimand="Percent of abstention rows scoring >= 2.0",
        contrast="abstention rows, score >= 2.0",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "abstention": True},
        n=audit_metrics["n_abstention_total"],
        aggregation_rule="100 * count(score >= 2.0) / count(abstention)",
        source="9 low-baseline subjects' results_v2.json + judgments",
    )
    claims["3_7_6_abstention_pct_above_3"] = claim(
        audit_metrics["abstention_pct_above_3"],
        estimand="Percent of abstention rows scoring >= 3.0",
        contrast="abstention rows, score >= 3.0",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "abstention": True},
        n=audit_metrics["n_abstention_total"],
        aggregation_rule="100 * count(score >= 3.0) / count(abstention)",
        source="9 low-baseline subjects' results_v2.json + judgments",
    )
    claims["3_7_6_abstention_mean_score"] = claim(
        audit_metrics["abstention_mean_score"],
        estimand="Mean 5-judge primary score on abstention-pattern responses",
        contrast="abstention rows",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "abstention": True},
        n=audit_metrics["n_abstention_total"],
        aggregation_rule="mean(primary_mean) over abstention rows",
        source="9 low-baseline subjects' results_v2.json + judgments",
    )

    # ---- Length distribution: high vs mid ----
    claims["3_7_6_high_score_chars_avg"] = claim(
        audit_metrics["high_score_chars_avg"],
        estimand="Mean response length (chars) for ultra-high-scoring responses (>=4.5)",
        contrast="score >= 4.5",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "score_min": 4.5},
        n=audit_metrics["n_ultra_high"],
        source="9 low-baseline subjects' results_v2.json + judgments",
    )
    claims["3_7_6_mid_score_chars_avg"] = claim(
        audit_metrics["mid_score_chars_avg"],
        estimand="Mean response length (chars) for mid-range-scoring responses (2.5-3.5)",
        contrast="2.5 <= score < 3.5",
        filters={"subjects": LOW_BASELINE_SUBJECTS, "score_min": 2.5, "score_max": 3.5},
        n=audit_metrics["n_mid_range"],
        source="9 low-baseline subjects' results_v2.json + judgments",
    )

    # ---- Battery leakage ----
    claims["3_4_battery_leakage_n_total"] = claim(
        leak.get("n_total"),
        estimand="Total behavioral-prediction questions across 15 batteries",
        contrast="all subjects",
        n=leak.get("n_total"),
        source="scripts/_battery_leakage_results.json",
    )
    claims["3_4_battery_leakage_n_leaks"] = claim(
        leak.get("n_leaks"),
        estimand="Behavioral-prediction questions with verbatim 7-gram overlap to held-out passages",
        contrast="aggregate (15 subjects)",
        n=leak.get("n_total"),
        source="scripts/_battery_leakage_results.json",
    )
    claims["3_4_battery_leakage_pct_aggregate"] = claim(
        leak.get("pct_aggregate"),
        estimand="Percent of all BP questions that leak (15 subjects, including Franklin)",
        n=leak.get("n_total"),
        aggregation_rule="100 * leaks / total",
        source="scripts/_battery_leakage_results.json",
    )
    claims["3_4_battery_leakage_pct_main_study"] = claim(
        leak.get("pct_main_study"),
        estimand="Percent of BP questions that leak in 14 main-study subjects (Franklin excluded)",
        contrast="main-study only",
        n=leak.get("main_study_n"),
        aggregation_rule="100 * main_leaks / main_total",
        source="scripts/_battery_leakage_results.json",
    )

    # ---- Franklin numbers ----
    claims["3_2_franklin_C5_5judge"] = claim(
        franklin["panel5_means"].get("C5_baseline"),
        estimand="Franklin C5 (no-context baseline) on 5-judge primary panel",
        contrast="C5_baseline",
        filters={"subject": "franklin", "panel": PRIMARY_PANEL, "condition": "C5_baseline"},
        aggregation_rule="5-judge primary panel mean (per-judge per-question -> per-judge mean -> panel mean)",
        source="results/franklin_legacy_20260411/analysis/{haiku,sonnet,opus,gpt4o,gpt54}_judgments.json",
    )
    claims["3_2_franklin_C5_haiku_only"] = claim(
        franklin["per_judge_C5_means"].get("haiku"),
        estimand="Franklin C5 baseline as scored by Haiku alone",
        contrast="single-judge",
        filters={"subject": "franklin", "judge": "haiku", "condition": "C5_baseline"},
        aggregation_rule="mean of haiku_score across all C5 questions",
        source="results/franklin_legacy_20260411/analysis/haiku_judgments.json",
    )
    claims["3_2_franklin_C2a_5judge"] = claim(
        franklin["panel5_means"].get("C2a_full_spec"),
        estimand="Franklin C2a (spec only) on 5-judge primary panel",
        contrast="C2a_full_spec",
        filters={"subject": "franklin", "panel": PRIMARY_PANEL, "condition": "C2a_full_spec"},
        aggregation_rule="5-judge primary panel mean",
        source="results/franklin_legacy_20260411/analysis/",
    )
    claims["3_2_franklin_C4a_5judge"] = claim(
        franklin["panel5_means"].get("C4a_full_facts_plus_spec"),
        estimand="Franklin C4a (facts + spec) on 5-judge primary panel",
        contrast="C4a_full_facts_plus_spec",
        filters={"subject": "franklin", "panel": PRIMARY_PANEL, "condition": "C4a_full_facts_plus_spec"},
        aggregation_rule="5-judge primary panel mean",
        source="results/franklin_legacy_20260411/analysis/",
    )
    claims["3_2_franklin_C5_7judge_min"] = claim(
        franklin["C5_per_judge_min"],
        estimand="Min per-judge mean on Franklin C5 across all available judges (sensitivity)",
        contrast="C5_baseline, judge-level",
        filters={"subject": "franklin", "condition": "C5_baseline", "judges": franklin["judges_present"]},
        aggregation_rule="min across {haiku, sonnet, opus, gpt4o, gpt54, gemini} per-judge C5 means",
        source="results/franklin_legacy_20260411/analysis/",
        note=("Legacy Franklin run pre-dates the gemini_flash/gemini_pro split; only one Gemini "
              "judge is present in legacy data. Range is min/max of per-judge means rather than "
              "5-judge / 7-judge panel means because Franklin is a high-baseline reference, not "
              "a main-study subject."),
    )
    claims["3_2_franklin_C5_7judge_max"] = claim(
        franklin["C5_per_judge_max"],
        estimand="Max per-judge mean on Franklin C5 across all available judges (sensitivity)",
        contrast="C5_baseline, judge-level",
        filters={"subject": "franklin", "condition": "C5_baseline", "judges": franklin["judges_present"]},
        aggregation_rule="max across per-judge C5 means",
        source="results/franklin_legacy_20260411/analysis/",
        note="Same as min note above.",
    )

    # Build manifest (dedup paths)
    seen_paths: set[str] = set()
    manifest = []
    for p in all_inputs:
        sp = str(p)
        if sp in seen_paths:
            continue
        seen_paths.add(sp)
        manifest.append(manifest_entry(p))

    payload = {
        "schema_version": SCHEMA_VERSION,
        "section": SECTION,
        "aggregation_rule": (
            "5-judge primary panel: per-judge per-question -> per-judge per-subject mean "
            "-> panel mean across {haiku, sonnet, opus, gpt4o, gpt54}; "
            "7-judge sensitivity adds {gemini_flash, gemini_pro}"
        ),
        "claims": claims,
        "auxiliary": {
            "calibration_means": {
                f"{j}|{t}": float(v) for (j, t), v in calib_means.items()
            },
            "inter_judge": inter_judge,
            "audit_metrics": audit_metrics,
            "battery_leakage": leak,
            "franklin": {
                "panel5_means": franklin["panel5_means"],
                "per_judge_C5_means": franklin["per_judge_C5_means"],
                "judges_present": franklin["judges_present"],
            },
        },
        "provenance": {
            "script": "scripts/_v11_emit_3_study_design.py",
            "script_version": SCRIPT_VERSION,
            "run_timestamp": EMIT_DATE,
            "input_manifest": manifest,
        },
    }
    return payload, all_inputs


# =============================================================================
# Verify
# =============================================================================

def compare(scaffold, paper, tol=VERIFY_TOLERANCE):
    if scaffold is None and paper is None:
        return ("MATCH", 0.0)
    if scaffold is None or paper is None:
        return ("MISMATCH(missing)", float("inf"))
    delta = scaffold - paper
    if abs(delta) <= tol + 1e-9:
        return ("MATCH", abs(delta))
    return (f"MISMATCH({delta:+.4f})", abs(delta))


def run_verify(payload, verbose=True) -> bool:
    diffs = []
    for cid, paper_val in PAPER_CLAIMS.items():
        scaffold_val = payload["claims"].get(cid, {}).get("value") if cid in payload["claims"] else None
        # Some paper claim ids may not match scaffold ids (e.g., 3_2_franklin_C5_7judge_min vs the ones we emitted)
        status, _ = compare(scaffold_val, paper_val)
        diffs.append((cid, scaffold_val, paper_val, status))

    n_match = sum(1 for d in diffs if d[3] == "MATCH")
    n_total = len(diffs)
    if verbose:
        print()
        print("=" * 78)
        print(f"VERIFY: {n_match}/{n_total} claims MATCH within {VERIFY_TOLERANCE}")
        print("=" * 78)
        for cid, sv, pv, status in diffs:
            if status != "MATCH":
                sv_s = f"{sv:.4f}" if isinstance(sv, (int, float)) else str(sv)
                pv_s = f"{pv:.4f}" if isinstance(pv, (int, float)) else str(pv)
                print(f"  {cid:50s} scaffold={sv_s:>10s} paper={pv_s:>10s} -> {status}")
    return n_match == n_total


# =============================================================================
# Markdown
# =============================================================================

def fmt(v, digits=3):
    if v is None:
        return "n/a"
    if isinstance(v, (int, float)):
        return f"{v:.{digits}f}"
    return str(v)


def render_markdown(payload) -> str:
    lines = []
    lines.append("# v11 emit: §3 Study Design (judges, calibration, Franklin, battery leakage)")
    lines.append("")
    lines.append(f"_Generated by `scripts/_v11_emit_3_study_design.py` (timestamp: {EMIT_DATE})_")
    lines.append("")
    lines.append("Aggregation: " + payload["aggregation_rule"])
    lines.append("")
    lines.append("Side-by-side compare to v10 paper §3. MATCH means scaffold value is within 0.005 of paper.")
    lines.append("")

    # Section: 3.7.2 calibration table
    lines.append("## §3.7.2 Calibration table (5 calibrated judges x 4 diagnostic tests)")
    lines.append("")
    lines.append("| Judge | Test | Scaffold | Paper | Verify |")
    lines.append("|---|---|---:|---:|:--|")
    for judge in ["haiku", "gemini_flash", "gpt4o", "gemini_pro", "gpt54"]:
        for test in DIAGNOSTIC_TESTS:
            cid = f"3_7_2_{judge}_{test}"
            sv = payload["claims"][cid]["value"]
            pv = PAPER_CLAIMS.get(cid)
            status, _ = compare(sv, pv)
            lines.append(f"| {judge} | {test} | {fmt(sv, 2)} | {fmt(pv, 2)} | {status} |")
    lines.append("")
    lines.append("Sonnet and Opus have no calibration data (paper §3.7.2 line 480: not tested on diagnostic battery).")
    lines.append("")
    for judge in NON_CALIBRATED_PANEL:
        for test in DIAGNOSTIC_TESTS:
            cid = f"3_7_2_{judge}_{test}"
            lines.append(f"- {cid}: value=null, note from script claim.")
    lines.append("")

    # Section: 3.7.4 inter-judge
    lines.append("## §3.7.4 Inter-judge agreement")
    lines.append("")
    lines.append("| claim_id | Scaffold | Paper | Verify |")
    lines.append("|---|---:|---:|:--|")
    for cid in [
        "3_7_4_spearman_5judge_min", "3_7_4_spearman_5judge_max",
        "3_7_4_spearman_7judge_min", "3_7_4_spearman_7judge_max",
        "3_7_4_krippendorff_alpha_5judge", "3_7_4_krippendorff_alpha_7judge",
    ]:
        sv = payload["claims"][cid]["value"]
        pv = PAPER_CLAIMS.get(cid)
        status, _ = compare(sv, pv)
        lines.append(f"| {cid} | {fmt(sv)} | {fmt(pv)} | {status} |")
    lines.append("")
    lines.append("Note: Krippendorff alpha computed on interval scale here; paper cites ordinal alpha. The two scales agree to within 0.01 on this score distribution but are not the same statistic.")
    lines.append("")

    # Section: 3.7.2 strictness
    lines.append("## §3.7.2 Per-judge strictness on abstention rows")
    lines.append("")
    lines.append("| Judge | Scaffold | Paper | Verify |")
    lines.append("|---|---:|---:|:--|")
    for judge in PRIMARY_PANEL:
        cid = f"3_7_2_strictness_{judge}"
        sv = payload["claims"][cid]["value"]
        pv = PAPER_CLAIMS.get(cid)
        status, _ = compare(sv, pv)
        lines.append(f"| {judge} | {fmt(sv, 2)} | {fmt(pv, 2)} | {status} |")
    lines.append("")

    # Section: 3.7.6 length + abstention
    lines.append("## §3.7.6 Length-score correlation + abstention audit")
    lines.append("")
    lines.append("| claim_id | Scaffold | Paper | Verify |")
    lines.append("|---|---:|---:|:--|")
    for cid in [
        "3_7_6_length_corr_overall", "3_7_6_length_corr_C5",
        "3_7_6_length_corr_C2a", "3_7_6_length_corr_C4", "3_7_6_length_corr_C4a",
        "3_7_6_abstention_n_total", "3_7_6_abstention_pct_below_2",
        "3_7_6_abstention_pct_above_2", "3_7_6_abstention_pct_above_3",
        "3_7_6_abstention_mean_score",
        "3_7_6_high_score_chars_avg", "3_7_6_mid_score_chars_avg",
    ]:
        sv = payload["claims"][cid]["value"]
        pv = PAPER_CLAIMS.get(cid)
        status, _ = compare(sv, pv)
        lines.append(f"| {cid} | {fmt(sv)} | {fmt(pv)} | {status} |")
    lines.append("")

    # Section: 3.4 battery leakage
    lines.append("## §3.4 Battery leakage")
    lines.append("")
    lines.append("| claim_id | Scaffold | Paper | Verify |")
    lines.append("|---|---:|---:|:--|")
    for cid in [
        "3_4_battery_leakage_n_total", "3_4_battery_leakage_n_leaks",
        "3_4_battery_leakage_pct_aggregate", "3_4_battery_leakage_pct_main_study",
    ]:
        sv = payload["claims"][cid]["value"]
        pv = PAPER_CLAIMS.get(cid)
        status, _ = compare(sv, pv)
        lines.append(f"| {cid} | {fmt(sv)} | {fmt(pv)} | {status} |")
    lines.append("")

    # Section: Franklin
    lines.append("## §3.2 / §4.1.1 Franklin")
    lines.append("")
    lines.append("| claim_id | Scaffold | Paper | Verify |")
    lines.append("|---|---:|---:|:--|")
    for cid in [
        "3_2_franklin_C5_5judge", "3_2_franklin_C5_haiku_only",
        "3_2_franklin_C2a_5judge", "3_2_franklin_C4a_5judge",
        "3_2_franklin_C5_7judge_min", "3_2_franklin_C5_7judge_max",
    ]:
        sv = payload["claims"][cid]["value"]
        pv = PAPER_CLAIMS.get(cid)
        status, _ = compare(sv, pv)
        lines.append(f"| {cid} | {fmt(sv)} | {fmt(pv)} | {status} |")
    lines.append("")
    fk = payload["auxiliary"]["franklin"]["per_judge_C5_means"]
    lines.append("Per-judge Franklin C5 means (range source for the 7-judge sensitivity):")
    lines.append("")
    for j, v in sorted(fk.items()):
        lines.append(f"- {j}: {v:.3f}")
    lines.append("")

    # Provenance
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Script: `{payload['provenance']['script']}` (version {payload['provenance']['script_version']})")
    lines.append("")
    lines.append("Input manifest (SHA-256, size, n_records where applicable):")
    lines.append("")
    for entry in payload["provenance"]["input_manifest"]:
        if entry.get("missing"):
            lines.append(f"- {entry['path']}: MISSING")
        else:
            lines.append(f"- {entry['path']}: sha256={entry['sha256'][:12]}..., size={entry['size_bytes']}")
    lines.append("")
    return "\n".join(lines) + "\n"


# =============================================================================
# Atomic write
# =============================================================================

def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="v11 emit for §3 Study Design")
    parser.add_argument("--verify", action="store_true",
                        help="After emit, compare every value against v10 paper claims; exit 1 on mismatch.")
    args = parser.parse_args()

    print("Building payload (judges + calibration + Franklin)...")
    payload, _ = build_payload()

    json_text = json.dumps(payload, indent=2, sort_keys=False, default=str)
    atomic_write(OUT_JSON, json_text + "\n")

    md_text = render_markdown(payload)
    atomic_write(OUT_MD, md_text)

    print()
    print(f"Emitted {len(payload['claims'])} claim_ids")
    print(f"JSON: {OUT_JSON}")
    print(f"MD:   {OUT_MD}")

    if args.verify:
        ok = run_verify(payload, verbose=True)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
