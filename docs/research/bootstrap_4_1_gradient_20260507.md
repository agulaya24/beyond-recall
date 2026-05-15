# Bootstrap 95% CI on §4.1 Gradient Slope

**Date:** 2026-05-07
**Regression:** delta_C4a ~ C5 (5-judge primary panel, N=14 main-study subjects)
**Method:** Nonparametric bootstrap, resample subjects with replacement, OLS slope per iteration
**Iterations:** 10,000
**RNG seed:** 20260507

## Point estimate (from v11_emit/4_1_gradient.json)

- slope = -0.9597
- intercept = +2.3635
- (paper: slope = -0.96, p < 1e-5)

## Bootstrap distribution

| Statistic | Value |
|---|---|
| Mean slope | -0.9698 |
| Median slope (50th pct) | -0.9611 |
| SE (bootstrap SD) | 0.1311 |
| 2.5th percentile | -1.2496 |
| 97.5th percentile | -0.7380 |
| 95% CI | [-1.2496, -0.7380] |
| Fraction of resamples with slope < 0 | 1.0000 |
| Fraction of resamples with slope < -0.5 | 1.0000 |

## Verdict

- 95% CI excludes zero: **TRUE**
- 95% CI excludes -0.5 (gradient robust at attenuated magnitude): **TRUE**

## Histogram (20 equal-width bins)

```
  bin range                count  bar (scaled to max)
  [-2.300, -2.211)      1  
  [-2.211, -2.121)      0  
  [-2.121, -2.032)      0  
  [-2.032, -1.943)      0  
  [-1.943, -1.853)      2  
  [-1.853, -1.764)      1  
  [-1.764, -1.675)      3  
  [-1.675, -1.585)      1  
  [-1.585, -1.496)      8  
  [-1.496, -1.407)     20  
  [-1.407, -1.317)     66  #
  [-1.317, -1.228)    231  ###
  [-1.228, -1.139)    643  #########
  [-1.139, -1.049)   1521  ######################
  [-1.049, -0.960)   2538  #####################################
  [-0.960, -0.871)   2741  ########################################
  [-0.871, -0.781)   1631  ########################
  [-0.781, -0.692)    507  #######
  [-0.692, -0.603)     76  #
  [-0.603, -0.513)     10  
```

## Inputs

- N subjects = 14
- Subjects: ebers, sunity_devee, hamerton, fukuzawa, bernal_diaz, babur, seacole, keckley, yung_wing, zitkala_sa, cellini, rousseau, augustine, equiano
- Degenerate resamples retried: 0

## Provenance

- Source data: `docs/research/v11_emit/4_1_gradient.json`
- Script: `scripts/bootstrap_4_1_gradient_slope.py`
- Full distribution: `docs/research/bootstrap_4_1_gradient_20260507.json` (`full_distribution` field)
