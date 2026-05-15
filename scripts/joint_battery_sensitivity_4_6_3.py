"""§4.6.3 Joint Battery Sensitivity Analysis (S119, 2026-05-07).

Reviewer attack: §4.6.3 currently tests literal-recall fraction OR Hamerton-
leverage in isolation. What if we drop Hamerton AND control for literal-recall
fraction simultaneously?

Joint test:
    drop Hamerton (n=13 GPT-5.4-battery globals)
    fit  delta_C4a ~ C5 + literal_recall_fraction (OLS)
    report partial slope on C5, partial slope on lit_frac, R^2, adj R^2

Comparison cascade:
    -0.96 (univariate, n=14, no controls)              [headline]
    -0.88 (multivariate, n=14, +literal-recall)        [§4.6.3 confound 1]
    -0.89 (univariate, n=13, drop Hamerton)            [§4.6.3 confound 2]
    -???  (multivariate, n=13, drop Hamerton + lit)    [JOINT, this script]

Data sources match _v10_battery_sensitivity.py: §4.1 table for C5/delta_C4a,
question_category_audit.md for LITERAL_RECALL counts, BP_DENOM = 39.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Mirrors DATA in _v10_battery_sensitivity.py exactly so the joint analysis
# is layered cleanly on top of the per-confound analyses already in the paper.
DATA = [
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
BP_DENOM = 39

df = pd.DataFrame(DATA, columns=["subject", "c5", "delta_c4a", "lit_count", "gen"])
df["lit_frac"] = df["lit_count"] / BP_DENOM

print("=" * 78)
print("INPUT DATA (N=14 main-study gradient subjects)")
print("=" * 78)
print(df.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# Reference: full-sample univariate (the published headline)
# ---------------------------------------------------------------------------
X_full = sm.add_constant(df["c5"].values)
m_full = sm.OLS(df["delta_c4a"].values, X_full).fit()
ci_full = m_full.conf_int(alpha=0.05)[1]

# ---------------------------------------------------------------------------
# Reference: full-sample multivariate (literal-recall confound only)
# ---------------------------------------------------------------------------
X_multi_full = sm.add_constant(df[["c5", "lit_frac"]].values)
m_multi_full = sm.OLS(df["delta_c4a"].values, X_multi_full).fit()
ci_multi_full = m_multi_full.conf_int(alpha=0.05)

# ---------------------------------------------------------------------------
# Reference: subset univariate (Hamerton-dropped only)
# ---------------------------------------------------------------------------
sub = df[df["gen"] == "gpt-5.4"].reset_index(drop=True)
X_sub_uni = sm.add_constant(sub["c5"].values)
m_sub_uni = sm.OLS(sub["delta_c4a"].values, X_sub_uni).fit()
ci_sub_uni = m_sub_uni.conf_int(alpha=0.05)[1]

# ---------------------------------------------------------------------------
# JOINT: drop Hamerton AND control for literal-recall fraction
# ---------------------------------------------------------------------------
print("=" * 78)
print("JOINT TEST (n=13, drop Hamerton, control for LITERAL_RECALL fraction)")
print("=" * 78)
print(f"Subjects (n={len(sub)}): {sub['subject'].tolist()}")
print(f"Dropped (legacy Haiku generator): "
      f"{df[df['gen'] == 'haiku']['subject'].tolist()}")
print()

# Collinearity diagnostics on the n=13 subset
r_c5_lit, p_c5_lit = stats.pearsonr(sub["c5"], sub["lit_frac"])
print(f"Pearson r(C5, LITERAL_fraction) on n=13 subset: {r_c5_lit:+.3f}  "
      f"(p = {p_c5_lit:.3f})")
X_joint = sm.add_constant(sub[["c5", "lit_frac"]].values)
print(f"VIF(C5)               = {variance_inflation_factor(X_joint, 1):.3f}")
print(f"VIF(LITERAL_fraction) = {variance_inflation_factor(X_joint, 2):.3f}")
print()

m_joint = sm.OLS(sub["delta_c4a"].values, X_joint).fit()
print(m_joint.summary())
print()

ci_joint = m_joint.conf_int(alpha=0.05)
print(f"Partial slope on C5 baseline:")
print(f"  beta = {m_joint.params[1]:+.3f}  "
      f"[95% CI {ci_joint[1, 0]:+.3f}, {ci_joint[1, 1]:+.3f}]  "
      f"p = {m_joint.pvalues[1]:.6f}")
print(f"Partial slope on LITERAL_RECALL fraction:")
print(f"  beta = {m_joint.params[2]:+.3f}  "
      f"[95% CI {ci_joint[2, 0]:+.3f}, {ci_joint[2, 1]:+.3f}]  "
      f"p = {m_joint.pvalues[2]:.6f}")
print(f"R^2          = {m_joint.rsquared:.3f}")
print(f"Adjusted R^2 = {m_joint.rsquared_adj:.3f}")
print(f"F            = {m_joint.fvalue:.3f}  (p = {m_joint.f_pvalue:.6f})")
print()

# Partial R^2 (added-last variance) for each predictor in the n=13 model
def partial_r2(y, x_all, keep_idx_list, full_r2):
    X = sm.add_constant(x_all[:, keep_idx_list])
    r2_red = sm.OLS(y, X).fit().rsquared
    return full_r2 - r2_red

x_all_sub = sub[["c5", "lit_frac"]].values
full_r2 = m_joint.rsquared
dr2_c5  = partial_r2(sub["delta_c4a"].values, x_all_sub, [1], full_r2)
dr2_lit = partial_r2(sub["delta_c4a"].values, x_all_sub, [0], full_r2)
print(f"Unique variance from C5 (delta R^2, added last)             = {dr2_c5:.3f}")
print(f"Unique variance from LITERAL fraction (delta R^2, added last) = {dr2_lit:.3f}")
print()

# ---------------------------------------------------------------------------
# Cascade summary
# ---------------------------------------------------------------------------
print("=" * 78)
print("CASCADE SUMMARY (slope on C5 baseline)")
print("=" * 78)
print(f"  univariate, n=14, no controls (headline)        : "
      f"{m_full.params[1]:+.3f}  [{ci_full[0]:+.3f}, {ci_full[1]:+.3f}]  "
      f"p = {m_full.pvalues[1]:.4g}  R^2 = {m_full.rsquared:.3f}")
print(f"  multivariate, n=14, +literal-recall              : "
      f"{m_multi_full.params[1]:+.3f}  "
      f"[{ci_multi_full[1, 0]:+.3f}, {ci_multi_full[1, 1]:+.3f}]  "
      f"p = {m_multi_full.pvalues[1]:.4g}  R^2 = {m_multi_full.rsquared:.3f}")
print(f"  univariate, n=13, drop Hamerton                  : "
      f"{m_sub_uni.params[1]:+.3f}  [{ci_sub_uni[0]:+.3f}, {ci_sub_uni[1]:+.3f}]  "
      f"p = {m_sub_uni.pvalues[1]:.4g}  R^2 = {m_sub_uni.rsquared:.3f}")
print(f"  JOINT: n=13, drop Hamerton + literal-recall      : "
      f"{m_joint.params[1]:+.3f}  "
      f"[{ci_joint[1, 0]:+.3f}, {ci_joint[1, 1]:+.3f}]  "
      f"p = {m_joint.pvalues[1]:.4g}  R^2 = {m_joint.rsquared:.3f}  "
      f"AdjR^2 = {m_joint.rsquared_adj:.3f}")
