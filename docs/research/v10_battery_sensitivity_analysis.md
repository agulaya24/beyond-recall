# §4.1 Gradient Battery-Composition Sensitivity Analysis (v10)

**Date:** 2026-04-24
**Script:** `scripts/_v10_battery_sensitivity.py`
**Target result:** §4.1 headline slope of the cross-subject gradient, y = Δ_C4a vs. x = C5 baseline. Headline: slope **−0.96** [95% CI −1.24, −0.67], R² = 0.82, p < 0.001, N = 14.

## 1. Purpose

Two distinct confounds were flagged by cross-LLM reviewers of v9 and v10:

1. **Battery-question-type confound** (Gemini Pro, Mistral, earlier feedback round). Appendix B.6 reports r = +0.646 between each subject's LITERAL_RECALL fraction and their subject-level Δ_spec; INTERPRETIVE fraction correlates at r = −0.582. Under this concern, the cross-subject slope on baseline could be partly an artifact of which subjects happened to get batteries weighted toward literal-recall questions (where the spec's prose register can piggy-back on verbatim-passage matching).

2. **Battery-generator confound** (Cerebras). Hamerton's battery is the legacy Haiku-generated 80-item set at `data/hamerton/battery.json` (no model field in metadata; verified legacy Haiku-generated in v6 draft §3.6 and METHODOLOGY.md). The 13 global subjects all use GPT-5.4-generated 39-item BP batteries at `results/global_<subj>/battery_gpt54.json` with `metadata.model = gpt-5.4`, `method = backward_design`. Franklin (high-baseline control, not in the N=14 gradient) is also legacy. Under this concern, Hamerton being the lowest-baseline AND highest-Δ subject could reflect generator differences rather than pretraining coverage.

## 2. Data inputs

### 2.1 Per-subject C5, Δ_C4a, LITERAL_RECALL count, and battery generator

C5 baseline and Δ_C4a are taken verbatim from the §4.1 per-subject table at lines 727-741 of `docs/beyond_recall_v10_draft.md`. These are the same values that produced the headline −0.96 slope, so the sensitivity checks are directly comparable.

LITERAL_RECALL counts come from the per-subject table in `docs/research/question_category_audit.md` (P0-15 audit, Haiku-classifier, 586 BP questions total across 15 subjects). Denominator is 39 for all 14 main-study subjects. Franklin is excluded (not part of the gradient; also n=0 LITERAL_RECALL in Franklin's battery by the audit classifier, a known quirk because Franklin's BP tier has 40 questions and the audit reports a zero for the LITERAL bucket).

Battery-generator assignment was verified by reading `metadata.model` from each battery file.

| Subject | C5 | Δ_C4a | LITERAL count | LITERAL fraction | Battery generator |
|---|---:|---:|---:|---:|---|
| Ebers | 1.02 | +1.05 | 2 | 0.051 | gpt-5.4 |
| Sunity Devee | 1.03 | +1.38 | 8 | 0.205 | gpt-5.4 |
| Hamerton | 1.26 | +1.51 | 10 | 0.256 | haiku (legacy) |
| Fukuzawa | 1.67 | +1.11 | 4 | 0.103 | gpt-5.4 |
| Bernal Diaz | 1.70 | +0.78 | 2 | 0.051 | gpt-5.4 |
| Babur | 1.76 | +0.25 | 1 | 0.026 | gpt-5.4 |
| Seacole | 1.77 | +0.82 | 8 | 0.205 | gpt-5.4 |
| Keckley | 1.84 | +0.59 | 4 | 0.103 | gpt-5.4 |
| Yung Wing | 1.88 | +0.52 | 3 | 0.077 | gpt-5.4 |
| Zitkala-Sa | 2.34 | −0.32 | 2 | 0.051 | gpt-5.4 |
| Cellini | 2.38 | +0.15 | 4 | 0.103 | gpt-5.4 |
| Rousseau | 2.44 | +0.10 | 2 | 0.051 | gpt-5.4 |
| Augustine | 2.58 | +0.11 | 4 | 0.103 | gpt-5.4 |
| Equiano | 2.77 | −0.35 | 6 | 0.154 | gpt-5.4 |

### 2.2 Univariate replication (sanity check)

With N = 14, the univariate regression y = Δ_C4a ~ x = C5 reproduces the headline to three decimal places:

| Quantity | Value | Headline |
|---|---|---|
| Slope | **−0.960** | −0.96 |
| 95% CI | [−1.245, −0.675] | [−1.24, −0.67] |
| R² | 0.818 | 0.82 |
| p | 9.1 × 10⁻⁶ | < 0.001 |

This confirms the §4.1 table values and the regression pipeline are internally consistent.

## 3. Sensitivity check 1: battery-question-type confound

**Model:** y = Δ_C4a = β₀ + β₁ · C5 + β₂ · LITERAL_fraction + ε, N = 14.

### Collinearity and leverage

- Pearson r(C5, LITERAL_fraction) = **−0.275** (p = 0.342). Baseline and literal-recall fraction are not collinear in this sample.
- VIF(C5) = **1.082**. VIF(LITERAL_fraction) = **1.082**. Both well below any concern threshold (>5). Partial coefficients are stable.
- Hamerton is the highest-leverage subject on both dimensions (lowest C5 band, highest LITERAL fraction). The subset regression in §4 is the direct leverage test.

### Partial coefficients

| Predictor | Partial β | 95% CI | p |
|---|---:|---|---:|
| C5 baseline | **−0.880** | [−1.127, −0.633] | 7.9 × 10⁻⁶ |
| LITERAL_fraction | **+2.297** | [+0.337, +4.256] | 0.026 |
| Intercept | +1.960 | [+1.381, +2.539] | < 0.001 |

### Model fit

| Metric | Value |
|---|---:|
| R² | **0.886** |
| Adjusted R² | **0.866** |
| F (df 2, 11) | 42.88 |
| F p-value | 6.4 × 10⁻⁶ |
| Durbin-Watson | 1.680 |

### Unique variance attribution (Type II ΔR²)

| Predictor added last | ΔR² |
|---|---:|
| C5 baseline (on top of LITERAL_fraction) | **0.636** |
| LITERAL_fraction (on top of C5 baseline) | 0.069 |

Univariate-for-comparison R² values: y ~ C5 alone = 0.818; y ~ LITERAL_fraction alone = 0.251; y ~ both = 0.886.

### Reading

The partial slope on C5 (−0.88) is attenuated from the univariate slope (−0.96) by **about 8%**. The 95% CIs overlap extensively. C5 alone accounts for 63.6% of variance after partialling out LITERAL_fraction; LITERAL_fraction accounts for 6.9% after partialling out C5. Adjusted R² rises from 0.80 (univariate) to 0.87 (multivariate), so the two predictors are additive rather than redundant. The battery-question-type confound is real and detectable (LITERAL_fraction is significant at p = 0.026 as a partial predictor) but the gradient on baseline is not an artifact of it.

## 4. Sensitivity check 2: battery-generator confound

**Model:** y = Δ_C4a ~ C5 restricted to subjects with GPT-5.4-generated batteries.

**Subjects kept (n = 13):** Ebers, Sunity Devee, Fukuzawa, Bernal Diaz, Babur, Seacole, Keckley, Yung Wing, Zitkala-Sa, Cellini, Rousseau, Augustine, Equiano.
**Dropped (n = 1, legacy Haiku battery):** Hamerton.

### Results

| Quantity | GPT-5.4 subset (n=13) | Full sample (N=14) | Δ |
|---|---:|---:|---:|
| Slope | **−0.892** | −0.960 | +0.068 (7% shallower) |
| 95% CI | [−1.180, −0.605] | [−1.245, −0.675] | overlapping |
| R² | 0.810 | 0.818 | −0.008 |
| r | −0.900 | −0.904 | −0.004 |
| p | 2.8 × 10⁻⁵ | 9.1 × 10⁻⁶ | both < 0.001 |

### Reading

Dropping Hamerton moves the slope from −0.96 to −0.89, a 7% attenuation. The 95% CIs overlap heavily and both regressions remain highly significant (p < 10⁻⁴). R² is essentially unchanged (0.81 vs 0.82). The gradient is not Hamerton-driven; restricting to the GPT-5.4-generated-battery subset produces the same qualitative result with only minor attenuation of the point estimate.

## 5. Combined read

Both confounds leave the headline result substantially intact:

| Analysis | Baseline slope | Change from headline | Significance |
|---|---:|---:|---:|
| Univariate (headline) | −0.960 | reference | p < 10⁻⁵ |
| Multiple regression, controlling for LITERAL_fraction | −0.880 | −8% | p < 10⁻⁵ |
| Subset regression, GPT-5.4 batteries only | −0.892 | −7% | p < 10⁻⁴ |

What this rules out: the gradient is not primarily driven by (a) between-subject differences in battery-question-type composition, or (b) generator-model differences between Hamerton and the 13 globals.

What this does not rule out: a more subtle confound in which battery-generator differences are correlated with other unobserved subject characteristics. The cleanest future test would run a second-generator battery on the same 13 globals and check whether the slope replicates on that generator's battery.

## 6. Reproduction

Script: `scripts/_v10_battery_sensitivity.py`. Requires Python 3.12 with `numpy`, `pandas`, `statsmodels`, `scipy`. Reproducible output is deterministic from the inline DATA table.

## 7. Provenance

- C5, Δ_C4a values: `docs/beyond_recall_v10_draft.md`, §4.1 table, lines 727-741.
- LITERAL_RECALL counts: `docs/research/question_category_audit.md`, per-subject table.
- Battery generators for globals: `results/global_<subj>/battery_gpt54.json`, `metadata.model = gpt-5.4` (confirmed for all 13).
- Hamerton battery-generator classification: `data/hamerton/battery.json` has no `model` field; legacy Haiku-generator confirmed via `docs/versions/beyond_recall_v6_draft.md` §3.6 and `docs/METHODOLOGY.md`.
