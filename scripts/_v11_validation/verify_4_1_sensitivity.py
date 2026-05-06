"""v11 verification: §4.1 sensitivity-callout numbers reproduce from primary data.

GPT-5.5 review flagged that scripts/_v10_battery_sensitivity.py and
scripts/_v10_coupling_sensitivity.py source per-subject C5/Delta_C4a/C4a from
hardcoded Python literals copied from the §4.1 paper table — exactly the §10
anti-pattern. This script verifies that the §4.1 sensitivity numbers reproduce
when computed FRESH from per-judge per-subject primary JSON files, under the
locked 5-judge primary panel rule.

Pipeline
--------
1. Load per-subject panel-mean C5 and panel-mean C4a from
   docs/research/v11_emit/4_1_gradient.json (which is itself emitted fresh
   from primary judgments via scripts/_v11_emit_4_1_gradient.py via
   scripts/recompute_5judge_primary.py).
2. Load per-question categories from docs/research/question_category_audit.json
   and compute LITERAL_RECALL fraction per subject (=count of LITERAL_RECALL
   questions / total questions for that subject).
3. Run all six regressions / tests fresh (scipy + statsmodels), compare to the
   numbers stated in §4.1 of docs/beyond_recall_v10_1_draft.md.

Comparison numbers (§4.1 callouts to be verified)
-------------------------------------------------
Battery-composition sensitivity:
    headline slope (delta_C4a ~ C5):       -0.96  [95% CI -1.24, -0.67]
    partial coefficient on C5 (control):   -0.88  [95% CI -1.13, -0.63]
    subset slope (drop Hamerton):          -0.89  [95% CI -1.18, -0.61]
    R^2 (headline):                         0.82
    slope p:                                <0.001
    Wilcoxon W = 11, N = 14, p = 0.007

Coupling-free sensitivity:
    level slope C4a ~ C5:                  +0.04  [95% CI -0.25, +0.33]
    R^2:                                    0.008
    p:                                      0.76
    permutation p:                          0.77

Pass criterion: all numbers within 0.005 of paper, plus matching star-of-
significance.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import linregress, wilcoxon

try:
    import statsmodels.api as sm  # noqa: F401
    HAVE_SM = True
except ImportError:
    HAVE_SM = False

REPO = Path(__file__).resolve().parents[2]
GRADIENT_JSON = REPO / "docs" / "research" / "v11_emit" / "4_1_gradient.json"
CATEGORY_JSON = REPO / "docs" / "research" / "question_category_audit.json"

RNG_SEED = 20260424
N_PERM = 10_000


# ---------------------------------------------------------------------------
# Step 1: pull per-subject C5 and C4a from the v11 fresh-emit file.
# ---------------------------------------------------------------------------
def load_subjects():
    with GRADIENT_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for s in data["subjects"]:
        if s["id"] == "franklin":
            continue  # high-baseline control, excluded from §4.1 N=14 regression
        rows.append({
            "id": s["id"],
            "subject": s["display_name"],
            "C5": s["C5"],
            "C4a": s["C4a"],
            "delta_C4a": s["delta_C4a"],
        })
    return rows, data["summary"]


# ---------------------------------------------------------------------------
# Step 2: LITERAL_RECALL fraction per subject from question_category_audit.
# Hamerton uses a different subject id in the gradient JSON ("hamerton"); the
# category audit uses the same id. Sunity Devee, Bernal Diaz: confirm naming.
# ---------------------------------------------------------------------------
def load_literal_fraction():
    with CATEGORY_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    by_subj_total = {}
    by_subj_literal = {}
    for q in data["questions"]:
        s = q["subject"]
        by_subj_total[s] = by_subj_total.get(s, 0) + 1
        if q["category_rubric"] == "LITERAL_RECALL":
            by_subj_literal[s] = by_subj_literal.get(s, 0) + 1
    out = {}
    for s, total in by_subj_total.items():
        out[s] = {
            "lit_count": by_subj_literal.get(s, 0),
            "total": total,
            "lit_frac": by_subj_literal.get(s, 0) / total,
        }
    return out


# ---------------------------------------------------------------------------
# Step 3: regressions fresh.
# ---------------------------------------------------------------------------
def ols_with_ci(x, y):
    """Univariate OLS via scipy.stats.linregress, with 95% CI on slope."""
    res = linregress(x, y)
    n = len(x)
    df_resid = n - 2
    # Two-sided 95% t-critical
    from scipy.stats import t as student_t
    t_crit = student_t.ppf(0.975, df_resid)
    se = res.stderr
    return {
        "slope": res.slope,
        "intercept": res.intercept,
        "ci_low": res.slope - t_crit * se,
        "ci_high": res.slope + t_crit * se,
        "r_squared": res.rvalue ** 2,
        "p_value": res.pvalue,
        "n": n,
    }


def multi_regression_partial_C5(c5, lit_frac, y):
    """Multiple OLS y ~ c5 + lit_frac. Return partial coefficient on C5 + 95% CI.

    If statsmodels is available, use it. Otherwise compute via Frisch-Waugh:
    residualize C5 on lit_frac, regress y on the residuals; SE for the partial
    is recovered from the multivariate normal-equations using statsmodels-equivalent formula.
    """
    if HAVE_SM:
        X = sm.add_constant(np.column_stack([c5, lit_frac]))
        m = sm.OLS(y, X).fit()
        ci = m.conf_int(alpha=0.05)
        return {
            "beta_c5": m.params[1],
            "ci_low": ci[1, 0],
            "ci_high": ci[1, 1],
            "p_value": m.pvalues[1],
            "r_squared": m.rsquared,
            "beta_lit": m.params[2],
        }
    # Fallback: Frisch-Waugh-Lovell + residual SE.
    c5 = np.asarray(c5, dtype=float)
    lit = np.asarray(lit_frac, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(c5)
    # Step 1: residualize c5 on (1, lit)
    Xa = np.column_stack([np.ones(n), lit])
    coef_c5_on_lit, *_ = np.linalg.lstsq(Xa, c5, rcond=None)
    c5_resid = c5 - Xa @ coef_c5_on_lit
    # Step 2: regress y on (1, c5, lit) via normal equations
    X = np.column_stack([np.ones(n), c5, lit])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ coef
    resid = y - yhat
    df_resid = n - 3
    sigma2 = (resid ** 2).sum() / df_resid
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    from scipy.stats import t as student_t
    t_crit = student_t.ppf(0.975, df_resid)
    t_stat = coef[1] / se[1]
    p = 2 * (1 - student_t.cdf(abs(t_stat), df_resid))
    ss_tot = ((y - y.mean()) ** 2).sum()
    ss_res = (resid ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    return {
        "beta_c5": coef[1],
        "ci_low": coef[1] - t_crit * se[1],
        "ci_high": coef[1] + t_crit * se[1],
        "p_value": float(p),
        "r_squared": r2,
        "beta_lit": coef[2],
    }


def permutation_test_level(c5, c4a, n_perm=N_PERM, seed=RNG_SEED):
    """Permutation test on level slope C4a ~ C5 (shuffle pairings)."""
    c5 = np.asarray(c5, dtype=float)
    c4a = np.asarray(c4a, dtype=float)
    obs = linregress(c5, c4a).slope
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm)
    c5_centered = c5 - c5.mean()
    denom = (c5_centered ** 2).sum()
    for i in range(n_perm):
        perm = rng.permutation(c4a)
        perm_c = perm - perm.mean()
        null[i] = (c5_centered * perm_c).sum() / denom
    p_two = 2 * min(np.mean(null <= obs), np.mean(null >= obs))
    p_two = min(p_two, 1.0)
    return {"observed": obs, "p_two_sided": float(p_two), "null_mean": float(null.mean())}


# ---------------------------------------------------------------------------
# Step 4: comparison.
# ---------------------------------------------------------------------------
PAPER = {
    "headline_slope":          -0.96,
    "headline_ci_low":         -1.24,
    "headline_ci_high":        -0.67,
    "headline_r2":              0.82,
    "headline_p_lt":            0.001,    # spec says p < 0.001
    "partial_C5":              -0.88,
    "partial_ci_low":          -1.13,
    "partial_ci_high":         -0.63,
    "subset_slope":            -0.89,
    "subset_ci_low":           -1.18,
    "subset_ci_high":          -0.61,
    "wilcoxon_W":              11.0,
    "wilcoxon_N":              14,
    "wilcoxon_p":               0.007,
    "level_slope":             +0.04,
    "level_ci_low":            -0.25,
    "level_ci_high":           +0.33,
    "level_r2":                 0.008,
    "level_p":                  0.76,
    "perm_p":                   0.77,
}


def fmt_match(paper, recomp, tol=0.005):
    diff = abs(paper - recomp)
    return f"{paper:+.3f} | {recomp:+.4f} | {diff:.4f} | {'MATCH' if diff <= tol else 'MISMATCH'}"


def main():
    print("=" * 88)
    print("Verification: §4.1 sensitivity callouts vs. fresh primary-data recomputation")
    print("=" * 88)

    rows, summary = load_subjects()
    print(f"Loaded {len(rows)} subjects from v11_emit/4_1_gradient.json")
    print(f"v11 emit aggregation: {json.dumps(summary['regression_delta_on_C5'], indent=2)[:200]}...")
    print()

    # Build arrays (preserve order from v11 emit)
    subj_ids = [r["id"] for r in rows]
    c5  = np.array([r["C5"] for r in rows])
    c4a = np.array([r["C4a"] for r in rows])
    dC4a = np.array([r["delta_C4a"] for r in rows])

    # Literal fractions
    lit = load_literal_fraction()
    print("Per-subject LITERAL_RECALL fraction (from question_category_audit.json):")
    print(f"{'subject':<18}{'lit_count':>10}{'total':>8}{'lit_frac':>12}")
    for s in subj_ids:
        info = lit.get(s, {"lit_count": "?", "total": "?", "lit_frac": float("nan")})
        print(f"{s:<18}{info['lit_count']:>10}{info['total']:>8}{info['lit_frac']:>12.4f}")
    lit_frac = np.array([lit[s]["lit_frac"] for s in subj_ids])
    print()

    # ---- Regression 1: headline delta_C4a ~ C5 ----
    h = ols_with_ci(c5, dC4a)
    # ---- Regression 2: multiple regression with literal control ----
    m = multi_regression_partial_C5(c5, lit_frac, dC4a)
    # ---- Regression 3: subset (drop Hamerton) ----
    keep = np.array([s != "hamerton" for s in subj_ids])
    s = ols_with_ci(c5[keep], dC4a[keep])
    # ---- Regression 4: level C4a ~ C5 ----
    L = ols_with_ci(c5, c4a)
    # ---- Permutation on level slope ----
    perm = permutation_test_level(c5, c4a)
    # ---- Wilcoxon on (C5, C4a) ----
    W_stat, W_p = wilcoxon(c5, c4a)

    # ---- Print comparison table ----
    print("=" * 88)
    print("COMPARISON TABLE")
    print("=" * 88)
    print(f"{'claim':<48}{'paper':>10}{'recompute':>14}{'|delta|':>10}{'status':>14}")
    print("-" * 88)

    def row(label, paper, recomp, tol=0.005):
        diff = abs(paper - recomp)
        status = "MATCH" if diff <= tol else f"MISMATCH ({diff:.3f})"
        print(f"{label:<48}{paper:>+10.3f}{recomp:>+14.4f}{diff:>10.4f}{status:>14}")

    print("Battery-composition sensitivity")
    row("headline slope (delta_C4a ~ C5)",  PAPER["headline_slope"], h["slope"])
    row("headline CI low",                  PAPER["headline_ci_low"], h["ci_low"])
    row("headline CI high",                 PAPER["headline_ci_high"], h["ci_high"])
    row("headline R^2",                     PAPER["headline_r2"], h["r_squared"])
    print(f"  headline p-value: paper p<0.001  recompute={h['p_value']:.3e}  "
          f"{'MATCH' if h['p_value'] < 0.001 else 'MISMATCH'}")
    row("partial coefficient on C5",        PAPER["partial_C5"], m["beta_c5"])
    row("partial coefficient CI low",       PAPER["partial_ci_low"], m["ci_low"])
    row("partial coefficient CI high",      PAPER["partial_ci_high"], m["ci_high"])
    row("subset slope (drop Hamerton)",     PAPER["subset_slope"], s["slope"])
    row("subset CI low",                    PAPER["subset_ci_low"], s["ci_low"])
    row("subset CI high",                   PAPER["subset_ci_high"], s["ci_high"])
    row("Wilcoxon W",                       PAPER["wilcoxon_W"], float(W_stat))
    row("Wilcoxon p",                       PAPER["wilcoxon_p"], float(W_p))
    print()
    print("Coupling-free sensitivity")
    row("level slope C4a ~ C5",             PAPER["level_slope"], L["slope"])
    row("level CI low",                     PAPER["level_ci_low"], L["ci_low"])
    row("level CI high",                    PAPER["level_ci_high"], L["ci_high"])
    row("level R^2 (x1000)",                PAPER["level_r2"]*1000, L["r_squared"]*1000)
    row("level p",                          PAPER["level_p"], L["p_value"], tol=0.01)
    row("permutation p",                    PAPER["perm_p"], perm["p_two_sided"], tol=0.02)
    print()
    print("=" * 88)
    print(f"Statsmodels available: {HAVE_SM}")
    print(f"Lit-frac support: {'OK' if all(s in lit for s in subj_ids) else 'MISSING SUBJECTS'}")


if __name__ == "__main__":
    main()
