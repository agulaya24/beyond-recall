"""v10 Coupling Sensitivity Analysis (third sensitivity check, §4.1)

Addresses GPT-5.5 reviewer concern: regressing Delta_C4a = C4a - C5 on C5 mechanically
induces a negative slope on a bounded 1-5 scale (especially with floor/ceiling effects).
The headline §4.1 result (slope = -0.96, R^2 = 0.82) is therefore vulnerable to a
delta-vs-baseline coupling artifact.

This script triangulates from a non-coupling-prone angle by computing:

(a) Level regression: C4a ~ C5 (no subtraction). If the spec floors prediction near
    a constant for low-baseline subjects while baseline varies 1.0-3.0, the level-slope
    should be close to 0. If C4a tracks C5 perfectly, the level-slope is close to 1.
    The honest "real gradient" reading lands strictly between 0 and 1.

(b) Permutation test on the original Delta-on-C5 slope. Shuffle the C4a values across
    subjects 10,000 times (preserving the marginal distribution of C4a, which encodes
    the bounded 1-5 scale and any floor/ceiling effects) and recompute the Delta-on-C5
    slope each time. The empirical p-value is the share of permutations with slope
    <= the observed -0.96.

(c) Subject-level bootstrap confidence intervals for both the original Delta-on-C5
    slope and the new C4a-level-on-C5 slope. Resample subjects with replacement
    10,000 times.

Per-subject (C5, C4a) data is identical to that loaded by _v10_battery_sensitivity.py.
delta_C4a values from that script are inverted to recover C4a = C5 + delta_C4a.

Output
------
Prints all regression outputs, null and bootstrap distribution summaries, and the
per-subject input frame. Saves a copy of the per-subject frame and the bootstrap
distribution arrays to docs/research/v10_coupling_sensitivity_arrays.npz for
reproducibility.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

RNG_SEED = 20260424
N_PERM = 10_000
N_BOOT = 10_000

# ---------------------------------------------------------------------------
# Per-subject data, identical to _v10_battery_sensitivity.py.
# C4a = C5 + delta_C4a (recovered from the same source table).
# ---------------------------------------------------------------------------

DATA = [
    # (subject, C5_baseline, delta_C4a)
    ("Ebers",        1.02,  1.05),
    ("Sunity Devee", 1.03,  1.38),
    ("Hamerton",     1.26,  1.51),
    ("Fukuzawa",     1.67,  1.11),
    ("Bernal Diaz",  1.70,  0.78),
    ("Babur",        1.76,  0.25),
    ("Seacole",      1.77,  0.82),
    ("Keckley",      1.84,  0.59),
    ("Yung Wing",    1.88,  0.52),
    ("Zitkala-Sa",   2.34, -0.32),
    ("Cellini",      2.38,  0.15),
    ("Rousseau",     2.44,  0.10),
    ("Augustine",    2.58,  0.11),
    ("Equiano",      2.77, -0.35),
]
df = pd.DataFrame(DATA, columns=["subject", "c5", "delta_c4a"])
df["c4a"] = df["c5"] + df["delta_c4a"]

print("=" * 78)
print("INPUT DATA (N=14 main-study gradient subjects)")
print("=" * 78)
print(df.to_string(index=False))
print()

c5    = df["c5"].values
delta = df["delta_c4a"].values
c4a   = df["c4a"].values

# ---------------------------------------------------------------------------
# 0. Replicate the original Delta-on-C5 slope (sanity check).
# ---------------------------------------------------------------------------

X1 = sm.add_constant(c5)
m_delta = sm.OLS(delta, X1).fit()
ci_delta = m_delta.conf_int(alpha=0.05)[1]
slope_delta = m_delta.params[1]
print("=" * 78)
print("0. ORIGINAL DELTA-ON-C5 SLOPE (sanity check vs §4.1 headline)")
print("=" * 78)
print(f"slope = {slope_delta:+.4f}  "
      f"[95% CI {ci_delta[0]:+.4f}, {ci_delta[1]:+.4f}]  "
      f"R^2 = {m_delta.rsquared:.4f}  p = {m_delta.pvalues[1]:.6g}")
print("Headline in §4.1: slope = -0.96 [95% CI -1.24, -0.67], R^2 = 0.82, p < 0.001")
print()

# ---------------------------------------------------------------------------
# (a) Level regression: C4a ~ C5
# ---------------------------------------------------------------------------

print("=" * 78)
print("(a) LEVEL REGRESSION  C4a ~ C5  (no subtraction; coupling-free)")
print("=" * 78)
m_level = sm.OLS(c4a, X1).fit()
ci_level = m_level.conf_int(alpha=0.05)[1]
slope_level = m_level.params[1]
intercept_level = m_level.params[0]
print(m_level.summary())
print()
print(f"intercept = {intercept_level:+.4f}")
print(f"slope     = {slope_level:+.4f}  "
      f"[95% CI {ci_level[0]:+.4f}, {ci_level[1]:+.4f}]  "
      f"p = {m_level.pvalues[1]:.6g}")
print(f"R^2       = {m_level.rsquared:.4f}")
print()
print("Identity check (algebraic, must hold exactly):")
print(f"  slope_level should equal slope_delta + 1: "
      f"{slope_level:+.4f} vs {slope_delta + 1:+.4f}")
print()

# Interpretation anchors
print("Interpretation anchors for slope_level:")
print("  ~ 0  : C4a is roughly flat across baselines  -> spec floors prediction")
print("         near a constant (true gradient finding).")
print("  ~ 1  : C4a tracks C5 one-for-one             -> no real gradient,")
print("         the original Delta-on-C5 slope is entirely the coupling artifact.")
print("  in (0, 1): partial gradient survives.")
print()

# ---------------------------------------------------------------------------
# (b) Permutation test on the Delta-on-C5 slope
#     Null: C4a values are exchangeable across subjects (bounded but otherwise
#     independent of C5). For each permutation, recompute delta = perm(c4a) - c5,
#     then regress on c5.
# ---------------------------------------------------------------------------

print("=" * 78)
print("(b) PERMUTATION TEST  on the Delta-on-C5 slope")
print("=" * 78)
rng = np.random.default_rng(RNG_SEED)
null_slopes = np.empty(N_PERM)
c5_centered = c5 - c5.mean()
denom = (c5_centered ** 2).sum()
for i in range(N_PERM):
    perm = rng.permutation(c4a)
    delta_perm = perm - c5
    delta_centered = delta_perm - delta_perm.mean()
    null_slopes[i] = (c5_centered * delta_centered).sum() / denom

# Two-sided empirical p-value
p_left  = float(np.mean(null_slopes <= slope_delta))
p_right = float(np.mean(null_slopes >= slope_delta))
p_two   = 2 * min(p_left, p_right)
p_two   = min(p_two, 1.0)
null_mean = float(null_slopes.mean())
null_sd   = float(null_slopes.std(ddof=1))

print(f"Permutations:           {N_PERM:,}")
print(f"Null slope mean:        {null_mean:+.4f}")
print(f"Null slope SD:          {null_sd:+.4f}")
print(f"Null slope 2.5/97.5 pct: "
      f"{np.percentile(null_slopes, 2.5):+.4f}, "
      f"{np.percentile(null_slopes, 97.5):+.4f}")
print(f"Observed slope:         {slope_delta:+.4f}")
print(f"P(null <= observed):    {p_left:.5f}")
print(f"P(null >= observed):    {p_right:.5f}")
print(f"Two-sided p-value:      {p_two:.5f}")
print()
print("Note: under random permutation of C4a across subjects, delta inherits")
print("the bounded marginal of C4a. If the headline slope were entirely a")
print("coupling artifact, the null distribution should NOT be centered near 0;")
print("it would carry the mechanical -1 component. The mean/SD shown above")
print("reveal whether the observed -0.96 is extreme conditional on that null.")
print()

# ---------------------------------------------------------------------------
# (c) Subject-level bootstrap CIs for both slopes
# ---------------------------------------------------------------------------

print("=" * 78)
print("(c) SUBJECT-LEVEL BOOTSTRAP CIs  (resample subjects w/ replacement)")
print("=" * 78)
rng_b = np.random.default_rng(RNG_SEED + 1)
n = len(df)
boot_delta = np.empty(N_BOOT)
boot_level = np.empty(N_BOOT)
n_skipped = 0
for i in range(N_BOOT):
    idx = rng_b.integers(0, n, size=n)
    xb = c5[idx]
    if xb.std() == 0:
        # Degenerate resample (all-same C5). Skip; negligible at N=14.
        boot_delta[i] = np.nan
        boot_level[i] = np.nan
        n_skipped += 1
        continue
    db = delta[idx]
    lb = c4a[idx]
    Xb = sm.add_constant(xb)
    boot_delta[i] = sm.OLS(db, Xb).fit().params[1]
    boot_level[i] = sm.OLS(lb, Xb).fit().params[1]

boot_delta_clean = boot_delta[~np.isnan(boot_delta)]
boot_level_clean = boot_level[~np.isnan(boot_level)]

ci_boot_delta = np.percentile(boot_delta_clean, [2.5, 97.5])
ci_boot_level = np.percentile(boot_level_clean, [2.5, 97.5])

print(f"Bootstrap iterations:    {N_BOOT:,}  (skipped degenerate: {n_skipped})")
print()
print(f"Delta-on-C5 slope:")
print(f"  point estimate:  {slope_delta:+.4f}")
print(f"  bootstrap mean:  {boot_delta_clean.mean():+.4f}")
print(f"  bootstrap SD:    {boot_delta_clean.std(ddof=1):+.4f}")
print(f"  bootstrap 95% CI: "
      f"[{ci_boot_delta[0]:+.4f}, {ci_boot_delta[1]:+.4f}]")
print(f"  parametric  95% CI: "
      f"[{ci_delta[0]:+.4f}, {ci_delta[1]:+.4f}]")
print()
print(f"C4a-level-on-C5 slope:")
print(f"  point estimate:  {slope_level:+.4f}")
print(f"  bootstrap mean:  {boot_level_clean.mean():+.4f}")
print(f"  bootstrap SD:    {boot_level_clean.std(ddof=1):+.4f}")
print(f"  bootstrap 95% CI: "
      f"[{ci_boot_level[0]:+.4f}, {ci_boot_level[1]:+.4f}]")
print(f"  parametric  95% CI: "
      f"[{ci_level[0]:+.4f}, {ci_level[1]:+.4f}]")
print()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("=" * 78)
print("SUMMARY")
print("=" * 78)
print(f"(a) Level slope C4a ~ C5:")
print(f"      {slope_level:+.4f}  [95% CI {ci_level[0]:+.4f}, {ci_level[1]:+.4f}]"
      f"  R^2 = {m_level.rsquared:.4f}")
print(f"(b) Permutation p-value on Delta-on-C5 slope ({slope_delta:+.4f}):")
print(f"      two-sided p = {p_two:.5f}  "
      f"(null mean {null_mean:+.4f}, null SD {null_sd:+.4f})")
print(f"(c) Bootstrap 95% CIs:")
print(f"      Delta-on-C5 slope:   "
      f"[{ci_boot_delta[0]:+.4f}, {ci_boot_delta[1]:+.4f}]")
print(f"      C4a-level slope:     "
      f"[{ci_boot_level[0]:+.4f}, {ci_boot_level[1]:+.4f}]")
print()

# ---------------------------------------------------------------------------
# Persist arrays for reproducibility
# ---------------------------------------------------------------------------

out = Path(__file__).resolve().parents[1] / "docs" / "research" / "v10_coupling_sensitivity_arrays.npz"
out.parent.mkdir(parents=True, exist_ok=True)
np.savez_compressed(
    out,
    subjects=np.array(df["subject"].tolist()),
    c5=c5,
    delta_c4a=delta,
    c4a=c4a,
    null_slopes=null_slopes,
    boot_delta=boot_delta_clean,
    boot_level=boot_level_clean,
)
print(f"Saved arrays: {out}")
