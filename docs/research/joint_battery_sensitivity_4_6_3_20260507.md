# §4.6.3 Joint Battery Sensitivity — drop Hamerton AND control for literal-recall

**Date:** 2026-05-07
**Script:** `scripts/joint_battery_sensitivity_4_6_3.py`
**Reproduces:** Python 3.12, numpy, pandas, statsmodels, scipy

## Reviewer attack

§4.6.3 currently tests two battery-related confounds in isolation:
1. **Question-type confound:** controls for LITERAL_RECALL fraction → slope attenuates from −0.96 to −0.88
2. **Battery-generator confound:** drops Hamerton (legacy Haiku-generated battery) → slope attenuates to −0.89

Reviewer challenge: what if both confounds are applied simultaneously?

## Joint test

Drop Hamerton (n = 13 GPT-5.4-battery globals) AND fit
`Δ_C4a ~ C5 + literal_recall_fraction` (OLS).

### Collinearity diagnostics on n=13

- Pearson r(C5, lit_frac) = −0.104 (p = 0.735)
- VIF(C5) = 1.011
- VIF(lit_frac) = 1.011

No collinearity. Hamerton was the high-leverage observation; without it C5 and literal-recall fraction are essentially orthogonal.

### Joint regression results (n = 13)

| coefficient | β | 95% CI | p |
|---|---|---|---|
| C5 baseline (partial) | **−0.870** | [−1.136, −0.604] | **2.6 × 10⁻⁵** |
| LITERAL_RECALL fraction (partial) | +2.034 | [−0.465, +4.533] | 0.100 |
| intercept | +1.960 | [+1.351, +2.570] | 1.6 × 10⁻⁵ |

- R² = 0.857
- Adjusted R² = 0.828
- F(2, 10) = 29.91 (p = 6.0 × 10⁻⁵)
- Unique variance from C5 (Δ R² added last) = 0.761
- Unique variance from literal-recall (Δ R² added last) = 0.047

## Cascade

| model | n | slope on C5 | 95% CI | R² |
|---|---|---|---|---|
| univariate, no controls (§4.1 headline) | 14 | −0.960 | [−1.245, −0.675] | 0.818 |
| multivariate, +literal-recall (§4.6.3 confound 1) | 14 | −0.880 | [−1.127, −0.633] | 0.886 |
| univariate, drop Hamerton (§4.6.3 confound 2) | 13 | −0.892 | [−1.180, −0.605] | 0.810 |
| **joint: drop Hamerton + literal-recall** | **13** | **−0.870** | **[−1.136, −0.604]** | **0.857** |

## Verdict

**The gradient survives both confounds simultaneously.** The joint partial slope is −0.870 (95% CI excludes zero by a wide margin; p = 2.6 × 10⁻⁵). Cumulative attenuation from headline to joint is ~9% in magnitude (−0.96 → −0.87) — within the 95% CI of the headline estimate. Adjusted R² of 0.828 indicates the joint model is not over-fitting on n=13. C5 baseline carries 76 percentage points of unique variance after both controls; literal-recall fraction is not statistically significant on the n=13 subset (p = 0.10).

## Suggested addition to §4.6.3

> Applied jointly — Hamerton dropped and literal-recall fraction added as a covariate on the remaining 13 globals — the partial slope on C5 is −0.870 (95% CI [−1.136, −0.604], p = 2.6 × 10⁻⁵, adjusted R² = 0.828), confirming the gradient survives both battery-related confounds simultaneously.
