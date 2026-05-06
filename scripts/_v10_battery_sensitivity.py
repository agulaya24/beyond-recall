"""v10 Battery Sensitivity Analysis

Two sensitivity checks on the §4.1 headline gradient slope (y = delta_C4a, x = C5 baseline):

1) Multiple regression with LITERAL_RECALL fraction as a second predictor.
   Controls for the battery-question-type confound flagged by Gemini Pro + Mistral.

2) Subset regression restricted to the 13 GPT-5.4-generated-battery subjects
   (drops Hamerton, which used a legacy Haiku-generated battery).
   Controls for the battery-generator confound flagged by Cerebras.

Data sources
------------
- C5 and delta_C4a: §4.1 table in docs/beyond_recall_v10_draft.md (lines 727-741).
- LITERAL_RECALL counts: docs/research/question_category_audit.md per-subject table.
- Denominator for LITERAL_RECALL fraction: 39 BP questions for all 14 main-study subjects.
- Battery-generator classification: results/global_<subj>/battery_gpt54.json metadata
  (all 13 globals: model = gpt-5.4); data/hamerton/battery.json has no model field
  and is known legacy Haiku-generated (cross-checked against v6 draft + METHODOLOGY.md).

Output
------
Prints a full regression report. Reproducible under Python 3.12 with numpy, pandas,
statsmodels, scipy.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# ---------------------------------------------------------------------------
# Data. Subjects ordered as in the §4.1 table (low-baseline then mid-baseline).
# N=14 main-study gradient subjects (Franklin excluded as high-baseline control).
# ---------------------------------------------------------------------------

DATA = [
    # (subject, C5_baseline, delta_C4a, literal_recall_count, battery_generator)
    ("Ebers",        1.02, 1.05,  2, "gpt-5.4"),
    ("Sunity Devee", 1.03, 1.38,  8, "gpt-5.4"),
    ("Hamerton",     1.26, 1.51, 10, "haiku"),
    ("Fukuzawa",     1.67, 1.11,  4, "gpt-5.4"),
    ("Bernal Diaz",  1.70, 0.78,  2, "gpt-5.4"),
    ("Babur",        1.76, 0.25,  1, "gpt-5.4"),
    ("Seacole",      1.77, 0.82,  8, "gpt-5.4"),
    ("Keckley",      1.84, 0.59,  4, "gpt-5.4"),
    ("Yung Wing",    1.88, 0.52,  3, "gpt-5.4"),
    ("Zitkala-Sa",   2.34, -0.32, 2, "gpt-5.4"),
    ("Cellini",      2.38, 0.15,  4, "gpt-5.4"),
    ("Rousseau",     2.44, 0.10,  2, "gpt-5.4"),
    ("Augustine",    2.58, 0.11,  4, "gpt-5.4"),
    ("Equiano",      2.77, -0.35, 6, "gpt-5.4"),
]
BP_DENOM = 39  # BP-tier questions per battery across all 14 subjects

df = pd.DataFrame(DATA, columns=["subject", "c5", "delta_c4a", "lit_count", "gen"])
df["lit_frac"] = df["lit_count"] / BP_DENOM

print("=" * 78)
print("INPUT DATA (N=14 main-study gradient subjects)")
print("=" * 78)
print(df.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 0. Replicate univariate headline slope (sanity check)
# ---------------------------------------------------------------------------

x_full = df["c5"].values
y_full = df["delta_c4a"].values

X1 = sm.add_constant(x_full)
m_uni = sm.OLS(y_full, X1).fit()
ci_lo_u, ci_hi_u = m_uni.conf_int(alpha=0.05)[1]
print("=" * 78)
print("0. UNIVARIATE REPLICATION (sanity check against headline)")
print("=" * 78)
print(f"slope (delta_C4a ~ C5): {m_uni.params[1]:+.3f}  "
      f"[95% CI {ci_lo_u:+.3f}, {ci_hi_u:+.3f}]  "
      f"p = {m_uni.pvalues[1]:.6f}  R^2 = {m_uni.rsquared:.3f}")
print("Headline in §4.1: slope = -0.96 [95% CI -1.24, -0.67], R^2 = 0.82, p < 0.001")
print()

# ---------------------------------------------------------------------------
# 1. Multiple regression: y = delta_C4a; x1 = C5, x2 = LITERAL_RECALL fraction
# ---------------------------------------------------------------------------

print("=" * 78)
print("1. MULTIPLE REGRESSION (battery-question-type confound control)")
print("=" * 78)

# Check collinearity first
r_c5_lit, p_c5_lit = stats.pearsonr(df["c5"], df["lit_frac"])
print(f"Pearson r(C5, LITERAL_RECALL fraction) = {r_c5_lit:+.3f}  (p = {p_c5_lit:.3f})")

# VIF for each predictor in the multi-regression
from statsmodels.stats.outliers_influence import variance_inflation_factor
X2 = sm.add_constant(df[["c5", "lit_frac"]].values)
vif_c5 = variance_inflation_factor(X2, 1)
vif_lit = variance_inflation_factor(X2, 2)
print(f"VIF(C5)                 = {vif_c5:.3f}")
print(f"VIF(LITERAL_fraction)   = {vif_lit:.3f}")
print()

m_multi = sm.OLS(y_full, X2).fit()
print(m_multi.summary())
print()

# Extract partial coefficients with 95% CI
ci_multi = m_multi.conf_int(alpha=0.05)
print(f"Partial coefficient for C5 baseline:")
print(f"  beta = {m_multi.params[1]:+.3f}  "
      f"[95% CI {ci_multi[1, 0]:+.3f}, {ci_multi[1, 1]:+.3f}]  "
      f"p = {m_multi.pvalues[1]:.6f}")
print(f"Partial coefficient for LITERAL_RECALL fraction:")
print(f"  beta = {m_multi.params[2]:+.3f}  "
      f"[95% CI {ci_multi[2, 0]:+.3f}, {ci_multi[2, 1]:+.3f}]  "
      f"p = {m_multi.pvalues[2]:.6f}")
print(f"R^2           = {m_multi.rsquared:.3f}")
print(f"Adjusted R^2  = {m_multi.rsquared_adj:.3f}")
print(f"F             = {m_multi.fvalue:.3f}  (p = {m_multi.f_pvalue:.6f})")
print()

# Partial R^2 for each predictor via Type II (additional variance explained
# by adding predictor to a model already containing the other predictor).
def partial_r2(y, x_keep_idx_list, x_all, full_r2):
    """R^2 of reduced model (drops the predictor of interest)."""
    X = sm.add_constant(x_all[:, x_keep_idx_list])
    r2_red = sm.OLS(y, X).fit().rsquared
    return full_r2 - r2_red

x_all = df[["c5", "lit_frac"]].values
full_r2 = m_multi.rsquared
dr2_c5  = partial_r2(y_full, [1], x_all, full_r2)  # drop C5, keep lit
dr2_lit = partial_r2(y_full, [0], x_all, full_r2)  # drop lit, keep C5
print(f"Unique variance attributable to C5 (delta R^2 when added last)            = {dr2_c5:.3f}")
print(f"Unique variance attributable to LITERAL fraction (delta R^2 added last)   = {dr2_lit:.3f}")
print()

# Compare to univariate baselines
X_lit_only = sm.add_constant(df["lit_frac"].values)
m_lit_only = sm.OLS(y_full, X_lit_only).fit()
print(f"Univariate R^2, y ~ C5 only        = {m_uni.rsquared:.3f}")
print(f"Univariate R^2, y ~ LITERAL only   = {m_lit_only.rsquared:.3f}")
print(f"Multivariate R^2, y ~ C5 + LITERAL = {m_multi.rsquared:.3f}")
print(f"Adjusted R^2, y ~ C5 + LITERAL     = {m_multi.rsquared_adj:.3f}")
print()

# ---------------------------------------------------------------------------
# 2. Subset regression: GPT-5.4-generated batteries only (n = 13, drops Hamerton)
# ---------------------------------------------------------------------------

print("=" * 78)
print("2. SUBSET REGRESSION (battery-generator confound control)")
print("=" * 78)
sub = df[df["gen"] == "gpt-5.4"].reset_index(drop=True)
print(f"Subjects in GPT-5.4 subset (n={len(sub)}): {sub['subject'].tolist()}")
print(f"Dropped (legacy Haiku generator): "
      f"{df[df['gen'] == 'haiku']['subject'].tolist()}")
print()

x_sub = sub["c5"].values
y_sub = sub["delta_c4a"].values
X_sub = sm.add_constant(x_sub)
m_sub = sm.OLS(y_sub, X_sub).fit()
ci_lo_s, ci_hi_s = m_sub.conf_int(alpha=0.05)[1]
print(f"Subset slope (delta_C4a ~ C5):  {m_sub.params[1]:+.3f}  "
      f"[95% CI {ci_lo_s:+.3f}, {ci_hi_s:+.3f}]")
print(f"Subset R^2:    {m_sub.rsquared:.3f}")
print(f"Subset p:      {m_sub.pvalues[1]:.6f}")
print(f"Subset r:      {np.corrcoef(x_sub, y_sub)[0,1]:+.3f}")
print(f"Full-sample headline: slope -0.96 [95% CI -1.24, -0.67], R^2 0.82, p < 0.001")
print()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("=" * 78)
print("SUMMARY")
print("=" * 78)
print(f"Univariate (headline replication):")
print(f"  slope = {m_uni.params[1]:+.3f}  [{ci_lo_u:+.3f}, {ci_hi_u:+.3f}]  "
      f"p = {m_uni.pvalues[1]:.4g}  R^2 = {m_uni.rsquared:.3f}")
print(f"Multiple regression (controls for LITERAL_RECALL fraction):")
print(f"  partial slope C5           = {m_multi.params[1]:+.3f}  "
      f"[{ci_multi[1, 0]:+.3f}, {ci_multi[1, 1]:+.3f}]  p = {m_multi.pvalues[1]:.4g}")
print(f"  partial slope LITERAL_frac = {m_multi.params[2]:+.3f}  "
      f"[{ci_multi[2, 0]:+.3f}, {ci_multi[2, 1]:+.3f}]  p = {m_multi.pvalues[2]:.4g}")
print(f"  R^2 = {m_multi.rsquared:.3f}  Adj R^2 = {m_multi.rsquared_adj:.3f}")
print(f"Subset regression (GPT-5.4 batteries only, n=13):")
print(f"  slope = {m_sub.params[1]:+.3f}  [{ci_lo_s:+.3f}, {ci_hi_s:+.3f}]  "
      f"p = {m_sub.pvalues[1]:.4g}  R^2 = {m_sub.rsquared:.3f}")
