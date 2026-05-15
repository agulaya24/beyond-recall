# §4.1 Headline-Gradient Permutation Test

**Date:** 2026-05-07
**Script:** `scripts/permutation_test_4_1_gradient.py`
**Data:** `docs/research/v11_emit/4_1_gradient.json` (5-judge primary panel)
**Seed:** 20260507 | **Permutations:** 10,000

## Null hypothesis

Under H0, there is no real association between a subject's baseline (C5) and the spec lift (Delta_C4a). Reassigning Delta_C4a values to subjects at random should reproduce the observed slope as a matter of luck.

This is *distinct* from the v10 coupling-sensitivity permutation, which permuted the level C4a vector to test a spec-on-baseline coupling null. Here Delta_C4a is permuted directly.

## Observed statistic

- n = 14 subjects (Hamerton + 13 globals; Franklin excluded as high-baseline reference, matching the §4.1 regression)
- OLS slope (Delta_C4a ~ C5): **-0.9597**
- Pearson r: -0.9043

## Null distribution

- Mean: -0.0049 (expected ~0 under H0)
- SD: 0.2941
- Min: -0.9411
- Max: +0.9218
- Median: -0.0048
- 95% interval: [-0.5653, +0.5624]

## Test result

- Permutations with |slope| >= |observed| (0.9597): 0 of 10,000
- **Two-sided empirical p-value: 0.00000**
- One-sided (slope <= observed): 0.00000

## Verdict

The headline gradient slope of -0.96 is **not** a coincidence of the specific 14-subject configuration. The observed slope lies far in the tail of the permutation null distribution; only 0 of 10,000 random reassignments of Delta_C4a values across subjects produce a slope as extreme. The negative association between baseline and spec lift survives permutation testing at p < 0.001.

## Per-subject input

| Subject | C5 | Delta_C4a |
|---|---:|---:|
| Ebers | 1.021 | +1.051 |
| Sunity Devee | 1.026 | +1.385 |
| Hamerton | 1.256 | +1.513 |
| Fukuzawa | 1.672 | +1.108 |
| Bernal Diaz | 1.697 | +0.785 |
| Babur | 1.759 | +0.251 |
| Seacole | 1.774 | +0.821 |
| Keckley | 1.841 | +0.595 |
| Yung Wing | 1.877 | +0.523 |
| Zitkala-Sa | 2.338 | -0.318 |
| Cellini | 2.379 | +0.149 |
| Rousseau | 2.436 | +0.097 |
| Augustine | 2.585 | +0.113 |
| Equiano | 2.769 | -0.349 |
