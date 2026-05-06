# v10 §4.1 Coupling Sensitivity Analysis

**Date:** 2026-04-24
**Reviewer concern:** GPT-5.5 flagged "delta-vs-baseline coupling." Regressing
Delta_C4a = C4a - C5 on C5 mechanically induces a negative slope on a bounded 1-5
scale, especially with floor or ceiling effects. The §4.1 headline (slope = -0.96,
R^2 = 0.82) is therefore vulnerable to a coupling artifact.
**Script:** `scripts/_v10_coupling_sensitivity.py`
**Arrays (reproducibility):** `docs/research/v10_coupling_sensitivity_arrays.npz`
**Seed:** 20260424.

This complements the existing two §4.1 sensitivity checks (LITERAL_RECALL multiple
regression; GPT-5.4-only subset regression) in `_v10_battery_sensitivity.py`.

---

## 1. Per-subject input data

N = 14 main-study gradient subjects (Franklin excluded as high-baseline control).
Source: §4.1 table, `docs/beyond_recall_v10_draft.md` lines 727-741. C4a is
recovered as C5 + delta_C4a; the data is identical to the data used by the existing
battery-sensitivity script.

| Subject       | C5    | delta_C4a | C4a   |
|---------------|-------|-----------|-------|
| Ebers         | 1.02  | 1.05      | 2.07  |
| Sunity Devee  | 1.03  | 1.38      | 2.41  |
| Hamerton      | 1.26  | 1.51      | 2.77  |
| Fukuzawa      | 1.67  | 1.11      | 2.78  |
| Bernal Diaz   | 1.70  | 0.78      | 2.48  |
| Babur         | 1.76  | 0.25      | 2.01  |
| Seacole       | 1.77  | 0.82      | 2.59  |
| Keckley       | 1.84  | 0.59      | 2.43  |
| Yung Wing     | 1.88  | 0.52      | 2.40  |
| Zitkala-Sa    | 2.34  | -0.32     | 2.02  |
| Cellini       | 2.38  | 0.15      | 2.53  |
| Rousseau      | 2.44  | 0.10      | 2.54  |
| Augustine     | 2.58  | 0.11      | 2.69  |
| Equiano       | 2.77  | -0.35     | 2.42  |

C4a summary: mean 2.46, SD 0.25, min 2.01, max 2.78, range 0.77.
C5 range: 1.02 to 2.77 (range 1.75).
The spread of C4a is ~14% of the spread of C5.

## 2. Sanity check: original Delta-on-C5 slope

Replicates the §4.1 headline.

```
slope = -0.9598  [95% CI -1.2450, -0.6746]
R^2   =  0.8175
p     =  9.07e-06
```

Headline in §4.1: slope = -0.96 [95% CI -1.24, -0.67], R^2 = 0.82, p < 0.001.
Match.

## 3. (a) Level regression C4a ~ C5 (no subtraction)

```
intercept = +2.3626
slope     = +0.0402  [95% CI -0.2450, +0.3254]
R^2       =  0.0078
p         =  0.7639
F         =  0.0944
```

Algebraic identity (must hold): slope_level = slope_delta + 1.
+0.0402 = -0.9598 + 1.0000. Verified.

**Reading.** With baselines spanning 1.02-2.77 (range 1.75), C4a varies between
2.01 and 2.78 with mean 2.46. The slope of C4a on C5 is statistically
indistinguishable from zero, the R^2 is 0.008, and the 95% CI for the slope
straddles zero by a wide margin in both directions. C4a is functionally flat
across baselines.

Anchors stated in the §4.1 reframe:
- slope_level ~ 0  → spec floors prediction near a constant regardless of
  baseline (true gradient finding under coupling-free framing).
- slope_level ~ 1  → C4a tracks C5 one-for-one; original Delta-on-C5 slope
  is entirely the coupling artifact.
- slope_level in (0, 1) → partial gradient survives.

The observed +0.040 sits at the "spec floors near a constant" anchor, not in the
middle, and not at 1. The original Delta-on-C5 slope is mechanically the
"distance from a near-constant ceiling" rather than a heterogeneous treatment
effect.

## 4. (b) Permutation test on the Delta-on-C5 slope

Null: C4a values are exchangeable across subjects. We shuffle C4a 10,000 times,
recompute Delta = perm(C4a) - C5, regress on C5, and record the slope.

```
Permutations:           10,000
Null slope mean:        -0.9984
Null slope SD:           0.1270
Null slope 2.5/97.5 pct: -1.2440, -0.7541
Observed slope:         -0.9598
P(null <= observed):     0.6137
P(null >= observed):     0.3863
Two-sided p-value:       0.7726
```

**Reading.** Under random permutation of C4a (preserving the bounded marginal,
breaking any link to C5), the null distribution is centered almost exactly at
-1.0 with SD 0.13. This is the mechanical coupling component made visible: when
C4a is independent of C5, the Delta-on-C5 slope is approximately -1 by
arithmetic identity, with finite-sample noise around that point. The observed
-0.960 sits 0.30 SDs above the null mean. It is not extreme.

This is the strongest single piece of evidence that the headline -0.96 magnitude
is the coupling artifact. A real heterogeneous-effect signal would have driven
the observed slope below the bulk of the null distribution. It did not.

## 5. (c) Subject-level bootstrap CIs

Resample subjects with replacement 10,000 times. Compute the Delta-on-C5 slope
and the C4a-level slope on each resample. Skipped degenerate resamples: 0.

```
Delta-on-C5 slope:
  point estimate:   -0.9598
  bootstrap mean:   -0.9717
  bootstrap SD:      0.1317
  bootstrap 95% CI: [-1.2535, -0.7396]
  parametric  95% CI: [-1.2450, -0.6746]

C4a-level-on-C5 slope:
  point estimate:   +0.0402
  bootstrap mean:   +0.0283
  bootstrap SD:      0.1317
  bootstrap 95% CI: [-0.2535, +0.2604]
  parametric  95% CI: [-0.2450, +0.3254]
```

**Reading.** Both bootstrap CIs closely match the parametric CIs from OLS, which
indicates the OLS standard errors are well-behaved at N=14 despite the small
sample. The Delta-on-C5 CI is far from zero; the C4a-level CI straddles zero.
Both findings are stable to subject-level resampling.

## 6. Honest verdict

GPT-5.5 was right that the steep -0.96 slope is largely the coupling artifact.
The permutation null is centered at -1.00 with the observed -0.96 sitting well
inside its bulk (p = 0.77), and the C4a-level slope is +0.04 with a CI that
straddles zero. Two independent reframings agree: the magnitude of the headline
slope reflects the arithmetic identity slope_Delta = slope_level - 1 with the
level component statistically zero, not a heterogeneous treatment effect.

The substantive finding survives, but its framing must change. The correct
statement is not "low-baseline subjects benefit more from the spec" (which
implies treatment-effect heterogeneity by baseline). The correct statement is
"under the spec, C4a clusters near 2.5 across baselines spanning 1.0-2.8, so
the gain in raw points is mechanically larger where the floor is lower."

This is still load-bearing for the paper's argument. The paper's central claim
is that the spec is the tool for the unknown, where "unknown" maps onto
low-baseline subjects. A near-constant C4a ceiling under spec is the
operational meaning of that claim. But the paper should not lean on
"differential lift" or "heterogeneous treatment effect" language; it should
lean on "the spec produces a roughly constant ceiling near 2.5 regardless of
baseline" and let the gain magnitude follow from arithmetic.

Sections that build on the gradient should be reread against this reframing:
- §4.4.2 Common Mechanisms
- §4.6 Robustness
- §5.5 (the hedging metric block, formerly §4.8)

## 7. Summary table (for the paper insert)

| Check | Statistic | Value | 95% CI | Notes |
|------|-----------|-------|--------|-------|
| Sanity | Delta-on-C5 slope (OLS) | -0.960 | [-1.245, -0.675] | R^2 = 0.82, p < 0.001 |
| (a) | C4a-level slope (OLS) | +0.040 | [-0.245, +0.325] | R^2 = 0.008, p = 0.76 |
| (b) | Permutation p (Delta-on-C5) | 0.77 | null mean -1.00, SD 0.13 | observed not extreme |
| (c) | Bootstrap CI Delta-on-C5 slope | -0.972 (mean) | [-1.254, -0.740] | matches parametric |
| (c) | Bootstrap CI C4a-level slope | +0.028 (mean) | [-0.254, +0.260] | matches parametric |
