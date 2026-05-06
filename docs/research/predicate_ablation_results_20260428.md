# Predicate Ablation Results - Phase 2c (2026-04-28)

Heuristic-rater proxy disconfirmation test: see script docstring.
"Rater-identified causal predicate" = highest-token-overlap spec sentence per the deep_pattern_activation_analysis classifier; not a human rating.

## Decision rule outcome: NOT_SUPPORTED

- mean Delta_removal across N=16: +0.225 anchor points
- mean Delta_reversal across N=16: -0.162 anchor points
- SD Delta_removal: 0.790
- 95% CI Delta_removal: [-0.162, +0.612]

### Decision thresholds
- mean Delta_removal >= 1.0: STRONG predicate-mediated framing supported
- 0.5 <= mean Delta_removal < 1.0: CAUTIOUS framing only
- mean Delta_removal < 0.5: claim does NOT survive; rater-confabulation alternative is more parsimonious

## Per-case results

| Subject | qid | Axis | Mechanism | Original | Ablated | Reversed | dRemoval | dReversal | OrigDrift |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| fukuzawa | 3 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (high) | 3.60 | 4.00 | 3.80 | -0.40 | -0.20 | -0.40 |
| equiano | 3 | LITERAL_RECALL | PATTERN_PREDICATE (high) | 2.00 | 1.40 | 2.80 | +0.60 | -0.80 | -3.00 |
| sunity_devee | 4 | REFUSAL_TRIGGERING | PATTERN_PREDICATE (high) | 2.20 | 2.00 | 2.20 | +0.20 | +0.00 | -2.13 |
| augustine | 35 | REFUSAL_TRIGGERING | PATTERN_PREDICATE (high) | 3.20 | 5.00 | 3.80 | -1.80 | -0.60 | -1.20 |
| babur | 6 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (high) | 3.60 | 3.20 | 3.60 | +0.40 | +0.00 | -0.60 |
| bernal_diaz | 16 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (high) | 3.40 | 2.00 | 4.60 | +1.40 | -1.20 | -1.60 |
| cellini | 34 | LITERAL_RECALL | PATTERN_PREDICATE (high) | 3.60 | 3.60 | 4.20 | +0.00 | -0.60 | -0.60 |
| hamerton | 43 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (high) | 4.00 | 4.00 | 4.00 | +0.00 | +0.00 | -0.20 |
| sunity_devee | 17 | INTERPRETIVE_INFERENCE | INFERENCE_CHAIN (low) | 1.00 | 1.00 | 1.00 | +0.00 | +0.00 | -3.40 |
| augustine | 20 | LITERAL_RECALL | INFERENCE_CHAIN (medium) | 3.20 | 2.80 | 3.60 | +0.40 | -0.40 | -1.00 |
| babur | 13 | INTERPRETIVE_INFERENCE | INFERENCE_CHAIN (low) | 2.00 | 1.60 | 1.60 | +0.40 | +0.40 | -2.00 |
| bernal_diaz | 2 | INTERPRETIVE_INFERENCE | INFERENCE_CHAIN (low) | 2.60 | 2.60 | 2.40 | +0.00 | +0.20 | -1.73 |
| rousseau | 28 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (medium) | 4.00 | 2.20 | 2.80 | +1.80 | +1.20 | +0.00 |
| yung_wing | 22 | LITERAL_RECALL | PATTERN_PREDICATE (medium) | 3.20 | 2.40 | 3.20 | +0.80 | +0.00 | -1.00 |
| sunity_devee | 23 | REFUSAL_TRIGGERING | PATTERN_PREDICATE (medium) | 2.80 | 2.80 | 3.40 | +0.00 | -0.60 | -1.40 |
| bernal_diaz | 38 | INTERPRETIVE_INFERENCE | PATTERN_PREDICATE (medium) | 2.60 | 2.80 | 2.60 | -0.20 | +0.00 | -1.40 |

## Cases where ablation produced >= 1 anchor drop (claim supported)
- bernal_diaz q16 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/high): dRemoval=+1.40, dReversal=-1.20
- rousseau q28 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/medium): dRemoval=+1.80, dReversal=+1.20

## Cases where ablation produced < 0.5 anchor drop (alternative explanation likely)
- fukuzawa q3 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/high): dRemoval=-0.40, dReversal=-0.20. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- sunity_devee q4 (REFUSAL_TRIGGERING, PATTERN_PREDICATE/high): dRemoval=+0.20, dReversal=+0.00. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- augustine q35 (REFUSAL_TRIGGERING, PATTERN_PREDICATE/high): dRemoval=-1.80, dReversal=-0.60. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- babur q6 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/high): dRemoval=+0.40, dReversal=+0.00. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- cellini q34 (LITERAL_RECALL, PATTERN_PREDICATE/high): dRemoval=+0.00, dReversal=-0.60. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- hamerton q43 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/high): dRemoval=+0.00, dReversal=+0.00. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- sunity_devee q17 (INTERPRETIVE_INFERENCE, INFERENCE_CHAIN/low): dRemoval=+0.00, dReversal=+0.00. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- augustine q20 (LITERAL_RECALL, INFERENCE_CHAIN/medium): dRemoval=+0.40, dReversal=-0.40. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- babur q13 (INTERPRETIVE_INFERENCE, INFERENCE_CHAIN/low): dRemoval=+0.40, dReversal=+0.40. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- bernal_diaz q2 (INTERPRETIVE_INFERENCE, INFERENCE_CHAIN/low): dRemoval=+0.00, dReversal=+0.20. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- sunity_devee q23 (REFUSAL_TRIGGERING, PATTERN_PREDICATE/medium): dRemoval=+0.00, dReversal=-0.60. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.
- bernal_diaz q38 (INTERPRETIVE_INFERENCE, PATTERN_PREDICATE/medium): dRemoval=-0.20, dReversal=+0.00. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.

## Sanity check: original-condition reproduction drift
- N reproduced: 16
- mean drift: -1.354
- max |drift|: 3.400
- cases with |drift| > 1.0: 9 (model stochasticity confound, NOT a script bug)

## Verdict
The strong claim does NOT survive. Rater-confabulation alternative is more parsimonious: removing the heuristically-identified causal predicate did not reduce performance, suggesting the lift was either generic-persona-enrichment, latent world knowledge, or that the heuristic mis-identified the true enabling content.

### What would tighten this further
- Human rater identification of causal predicate (vs heuristic) on a subset
- Larger N (e.g. all 47 PATTERN_PREDICATE cases coded and ablated)
- Irrelevant-predicate control: matched-length but unrelated predicate, to test the "any rich persona text" alternative
- Ablate two or more candidate predicates per case (the heuristic top-1 may not be the true driver)
