# Beyond Recall v11 — Paper Numbers Verification (2026-04-28)

## Summary

- Total numerics audited: **312**
- MATCH: **298**
- MINOR_ROUNDING: **10**
- MISMATCH: **4**
- PAPER_ONLY: **0**

Tolerance rules: scores/deltas MATCH if |Δ| < 0.005, MINOR_ROUNDING if |Δ| < 0.05; percentages MATCH if |Δ| < 0.5pp, MINOR_ROUNDING if |Δ| < 1.5pp; n-counts MATCH if exact, MINOR_ROUNDING if |Δ| < 1.5; approximate claims allowed 10% relative.

## Re-confirmation of today's already-verified items

- **§3.6.6 audit**: re-ran `scripts/audit_low_end_inflation.py` → 1,599 responses, 192 abstentions, mean 1.27, strictness Sonnet 1.14 / GPT-5.4 1.17 / Haiku 1.29 / GPT-4o 1.34 / Opus 1.41, length r=0.26 / C5 r=0.604 — all reconcile.
- **§4.1 sensitivity**: re-ran `scripts/_v11_validation/verify_4_1_sensitivity.py` → slope −0.96, R²=0.82, partial −0.88, subset (drop Hamerton) −0.89, level slope +0.04 R²=0.008, level CI [−0.245, +0.325], permutation p=0.77 — all reconcile.
- **§4.4.2 Table 4.6**: re-ran `scripts/_table_4_6_5judge_recompute.py` → 8 rows reproduce to within rounding.
- **Per-system anchor-crossing (§4.4)**: cross-checked against `docs/research/per_system_anchor_crossing_20260427.json` → Mem0 controlled 23.4/18.8, native 36.1/14.9; Letta controlled 26.9/19.4, native 19.9/19.9; Zep controlled 27.9/19.7, native 32.5/13.7; Supermemory controlled 20.2/22.5, native 23.4/19.5; Base Layer controlled 29.0/21.6 — all reconcile.

## MISMATCH items (recommend paper edit)

These are claims where the paper number differs from the scaffold by more than rounding tolerance. Each requires either (a) a paper edit to the scaffold value, or (b) re-running the source script to re-emit the scaffold.

| Section | Claim | Paper value | Scaffold value | |Δ| | Recommended edit |
|---|---|---|---|---|---|
| §4.4.1 | §4.4.1 Supermemory controlled Δ −0.05 | -0.05 | 0.03993 | 0.08993 | Use scaffold value |
| §4.2.1 | §4.2.1 all14 C8 improve 64.5% (paper) | 64.5 | 65.2 | 0.7015 | Use scaffold value |
| §4.2.1 | §4.2.1 all14 C8 worsen 24.5% | 24.5 | 23.63 | 0.8736 | Use scaffold value |
| §4.4.1 | §4.4.1 Supermemory controlled all14 improved 5/14 | 5 | 7 | 2 | Use scaffold value |

### MISMATCH diagnostic notes

- **§4.4.1 Supermemory controlled aggregate.** Paper Table 4.4.1 says Δ_spec (all 14) = -0.05 with 5/14 improved and Δ_spec (low-baseline) = -0.01 with 5/9 improved. Scaffold gives +0.04 with 7/14 improved and -0.018 with 4/9 improved. Same direction at low-baseline grain (small negative), but the all-14 sign flips and the n-positive count is off by 2 on all-14 and by 1 on low-baseline. The paper's prose immediately below also says 'Supermemory +0.004' (line 1049), a third number not matching either the table or the scaffold. This row is the single most consequential edit on the table; the rest of the §4.4.1 narrative (bimodal mixture, near-zero aggregate) survives either reading.
- **§4.2.1 all-14 C8 row.** Paper says 64.5% improved / 24.5% worsened; scaffold says 65.2% / 23.6%. Less than 1pp drift on each; substantively the paper's claim 'Every context condition exceeds a 70% per-question improvement rate on the population of relevance' (line 807) is unaffected. Edit is mechanical.

## PAPER_ONLY items (no scaffold backing — flag for review)

_None._

## MINOR_ROUNDING items (acceptable rounding)

| Section | Claim | Paper | Scaffold |
|---|---|---|---|
| §4.4.1 | §4.4.1 Base Layer controlled Δ +0.08 | 0.08 | 0.08645 |
| §4.5 | §4.5 Ebers Δ +1.05 | 1.05 | 1.045 |
| §4.5 | §4.5 Babur Δ +0.54 | 0.54 | 0.535 |
| §4.2 | §4.2 bernal_diaz C8=2.55 | 2.55 | 2.574 |
| §4.2 | §4.2 babur C8=2.05 | 2.05 | 2.077 |
| §4.2 | §4.2 mean C8-C2a +0.22 | 0.22 | 0.2285 |
| §B.4 | §B.4 LITERAL_RECALL mean Δ +0.792 | 0.792 | 0.75 |
| §B.4 | §B.4 INTERPRETIVE mean Δ +0.397 | 0.397 | 0.377 |
| §4.4.1 | §4.4.1 Supermemory controlled lowB improved 5/9 | 5 | 4 |
| §4.1 | §4.1 Franklin Δ_C4a -0.13 | -0.13 | -0.125 |

## Full per-claim table

| Section | Claim | Paper | Scaffold | Status | Kind |
|---|---|---|---|---|---|
| §1.3 | §1.3 mean Δ_C4a low-baseline | 0.89 | 0.8923 | MATCH | empirical |
| §1.3 | §1.3 78.6% questions improved C4a (low-baseline) | 78.6 | 78.63 | MATCH | empirical |
| §1.3 | §1.3 70.9% questions improved C2a (low-baseline) | 70.9 | 70.94 | MATCH | empirical |
| §1.3 | §1.3 12 of 14 overall improved | 12 | 12 | MATCH | empirical |
| §1.3 | §1.3 9 of 9 low-baseline improved | 9 | 9 | MATCH | empirical |
| §1.3 | §1.3 55.0% anchor crossings low-baseline | 55.0 | 54.99 | MATCH | empirical |
| §1.3 | §1.3 ~7,000-token spec | 7000 | 7000 | MATCH | approximate |
| §1.3 | §1.3 Hamerton spec alone 2.63 | 2.63 | 2.631 | MATCH | empirical |
| §1.3 | §1.3 Hamerton C8 raw corpus 2.27 | 2.27 | 2.267 | MATCH | empirical |
| §1.3 | §1.3 33,000-token corpus (Hamerton) | 33000 | 3.28e+04 | MATCH | approximate |
| §1.3 | §1.3 wrong-spec adversarial Δ −0.25 | -0.25 | -0.2469 | MATCH | empirical |
| §1.3 | §1.3 wrong-spec random Δ +0.15 | 0.15 | 0.1525 | MATCH | empirical |
| §1.3 | §1.3 correct-spec Δ +0.35 | 0.35 | 0.3538 | MATCH | empirical |
| §1.3 | §1.3 hedging 28.8% baseline (narrow) | 28.8 | 28.8 | MATCH | empirical |
| §1.3 | §1.3 hedging 0.0% C4a (narrow) | 0.0 | 0 | MATCH | empirical |
| §1.3 | §1.3 hedging 41.2% baseline (broad) | 41.2 | 41.22 | MATCH | empirical |
| §1.3 | §1.3 hedging 0.4% C4a (broad) | 0.4 | 0.39 | MATCH | empirical |
| §1.3 | §1.3 Wilcoxon W=11 | 11 | 11 | MATCH | empirical |
| §1.3 | §1.3 Wilcoxon p=0.007 | 0.007 | 0.006714 | MATCH | empirical |
| §1.3 | §1.3 slope −0.96 | -0.96 | -0.9597 | MATCH | empirical |
| §1.3 | §1.3 CI low −1.24 | -1.24 | -1.245 | MATCH | empirical |
| §1.3 | §1.3 CI high −0.67 | -0.67 | -0.6747 | MATCH | empirical |
| §1.3 | §1.3 R² = 0.82 | 0.82 | 0.8177 | MATCH | empirical |
| §4.4 | §4.4 Mem0 controlled upward 23.4% | 23.4 | 23.36 | MATCH | empirical |
| §4.4 | §4.4 Mem0 controlled downward 18.8% | 18.8 | 18.8 | MATCH | empirical |
| §4.4 | §4.4 Mem0 native upward 36.1% | 36.1 | 36.1 | MATCH | empirical |
| §4.4 | §4.4 Mem0 native downward 14.9% | 14.9 | 14.9 | MATCH | empirical |
| §4.4 | §4.4 Letta controlled upward 26.9% | 26.9 | 26.86 | MATCH | empirical |
| §4.4 | §4.4 Letta controlled downward 19.4% | 19.4 | 19.43 | MATCH | empirical |
| §4.4 | §4.4 Letta native upward 19.9% | 19.9 | 19.94 | MATCH | empirical |
| §4.4 | §4.4 Letta native downward 19.9% | 19.9 | 19.94 | MATCH | empirical |
| §4.4 | §4.4 Zep controlled upward 27.9% | 27.9 | 27.92 | MATCH | empirical |
| §4.4 | §4.4 Zep controlled downward 19.7% | 19.7 | 19.66 | MATCH | empirical |
| §4.4 | §4.4 Zep native upward 32.5% | 32.5 | 32.48 | MATCH | empirical |
| §4.4 | §4.4 Zep native downward 13.7% | 13.7 | 13.68 | MATCH | empirical |
| §4.4 | §4.4 Supermemory controlled upward 20.2% | 20.2 | 20.23 | MATCH | empirical |
| §4.4 | §4.4 Supermemory controlled downward 22.5% | 22.5 | 22.51 | MATCH | empirical |
| §4.4 | §4.4 Supermemory native upward 23.4% | 23.4 | 23.38 | MATCH | empirical |
| §4.4 | §4.4 Supermemory native downward 19.5% | 19.5 | 19.48 | MATCH | empirical |
| §4.4 | §4.4 Base Layer controlled upward 29.0% | 29.0 | 29.02 | MATCH | empirical |
| §4.4 | §4.4 Base Layer controlled downward 21.6% | 21.6 | 21.55 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 controlled Δ +0.12 | 0.12 | 0.1212 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 native Δ +0.33 | 0.33 | 0.3321 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta controlled Δ +0.20 | 0.2 | 0.1979 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta native Δ −0.02 | -0.02 | -0.02344 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep controlled Δ +0.19 | 0.19 | 0.1864 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep native Δ +0.33 | 0.33 | 0.3271 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory controlled Δ −0.05 | -0.05 | 0.03993 | MISMATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory native Δ −0.01 | -0.01 | -0.0125 | MATCH | empirical |
| §4.4.1 | §4.4.1 Base Layer controlled Δ +0.08 | 0.08 | 0.08645 | MINOR_ROUNDING | empirical |
| §4.4.1 | §4.4.1 Mem0 native lowB improved 7/9 | 7 | 7 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta controlled lowB improved 8/9 | 8 | 8 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep controlled lowB improved 9/9 | 9 | 9 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep native lowB improved 9/9 | 9 | 9 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep controlled Wilcoxon p=0.0004 | 0.0004 | 0.0003662 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta controlled Wilcoxon p=0.0017 | 0.0017 | 0.001709 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep native Wilcoxon p=0.0015 | 0.0015 | 0.001519 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 native Wilcoxon p=0.0088 | 0.0088 | 0.008775 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory native Wilcoxon p=0.8077 | 0.8077 | 0.8077 | MATCH | empirical |
| §4.4.2 | §4.4.2 Supermemory helps n=57 | 57 | 57 | MATCH | empirical |
| §4.4.2 | §4.4.2 Supermemory hurts n=53 | 53 | 53 | MATCH | empirical |
| §4.4.2 | §4.4.2 Supermemory helps mean swing +1.55 | 1.55 | 1.547 | MATCH | empirical |
| §4.4.2 | §4.4.2 Supermemory hurts mean swing −1.38 | -1.38 | -1.381 | MATCH | empirical |
| §4.4.2 | §4.4.2 Supermemory paired_total 546 | 546 | 546 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Supermemory Δ −2.0 | -2.0 | -2 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Base Layer Δ −2.2 | -2.2 | -2.2 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Letta Δ +0.4 | 0.4 | 0.4 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Mem0 Δ +0.2 | 0.2 | 0.2 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Zep Δ +0.2 | 0.2 | 0.2 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Supermemory C1=3.6 | 3.6 | 3.6 | MATCH | empirical |
| §4.4.3 | §4.4.3 Keckley Q21 Base Layer C1=3.4 | 3.4 | 3.4 | MATCH | empirical |
| §4.5 | §4.5 Hamerton Letta block score 3.10 | 3.1 | 3.103 | MATCH | empirical |
| §4.5 | §4.5 Hamerton BL unified 2.96 | 2.96 | 2.964 | MATCH | empirical |
| §4.5 | §4.5 Hamerton Δ +0.14 | 0.14 | 0.1385 | MATCH | empirical |
| §4.5 | §4.5 Ebers Letta block 2.76 | 2.76 | 2.76 | MATCH | empirical |
| §4.5 | §4.5 Ebers BL unified 1.72 | 1.72 | 1.715 | MATCH | empirical |
| §4.5 | §4.5 Ebers Δ +1.05 | 1.05 | 1.045 | MINOR_ROUNDING | empirical |
| §4.5 | §4.5 Babur Letta block 2.42 | 2.42 | 2.415 | MATCH | empirical |
| §4.5 | §4.5 Babur BL unified 1.88 | 1.88 | 1.88 | MATCH | empirical |
| §4.5 | §4.5 Babur Δ +0.54 | 0.54 | 0.535 | MINOR_ROUNDING | empirical |
| §4.5 | §4.5 Hamerton fullstack Δ +0.27 | 0.27 | 0.2718 | MATCH | empirical |
| §4.5 | §4.5 Ebers fullstack Δ +1.21 | 1.21 | 1.205 | MATCH | empirical |
| §4.5 | §4.5 Babur fullstack Δ +0.38 | 0.38 | 0.38 | MATCH | empirical |
| §4.5 | §4.5 Babur block 335,349 chars | 335349 | 3.353e+05 | MATCH | empirical |
| §4.5 | §4.5 Hamerton block 22,472 chars | 22472 | 2.247e+04 | MATCH | empirical |
| §4.5 | §4.5 Ebers block 68,413 chars | 68413 | 6.841e+04 | MATCH | empirical |
| §4.5 | §4.5 Babur duplication 25.4% | 25.4 | 25.4 | MATCH | empirical |
| §4.5 | §4.5 Letta API ceiling ~333K chars | 333000 | 3.33e+05 | MATCH | approximate |
| §4.5 | §4.5 Babur unique named entities Letta 416 | 416 | 416 | MATCH | empirical |
| §4.5 | §4.5 Babur unique named entities BL 65 | 65 | 65 | MATCH | empirical |
| §4.5 | §4.5 Ebers unique named entities Letta 53 | 53 | 53 | MATCH | empirical |
| §4.5 | §4.5 Ebers unique named entities BL 34 | 34 | 34 | MATCH | empirical |
| §4.1 | §4.1 partial coef on baseline −0.88 | -0.88 | -0.8801 | MATCH | empirical |
| §4.1 | §4.1 subset slope drop Hamerton −0.89 | -0.89 | -0.8924 | MATCH | empirical |
| §4.1 | §4.1 level slope C4a~C5 +0.04 | 0.04 | 0.0403 | MATCH | empirical |
| §4.1 | §4.1 level R² 0.008 | 0.008 | 0.007849 | MATCH | empirical |
| §4.1 | §4.1 level p 0.76 | 0.76 | 0.7633 | MATCH | empirical |
| §4.1 | §4.1 level CI low −0.25 | -0.25 | -0.2447 | MATCH | empirical |
| §4.1 | §4.1 level CI high +0.33 | 0.33 | 0.3253 | MATCH | empirical |
| §4.1 | §4.1 mean C4a 14 subj 2.41 | 2.41 | 2.44 | MATCH | empirical |
| §4.1 | §4.1 mean C4a low-baseline 2.46 | 2.46 | 2.439 | MATCH | empirical |
| §4.2 | §4.2 hamerton C5=1.26 | 1.26 | 1.256 | MATCH | empirical |
| §4.2 | §4.2 hamerton C2a=2.63 | 2.63 | 2.631 | MATCH | empirical |
| §4.2 | §4.2 hamerton C4a=2.77 | 2.77 | 2.769 | MATCH | empirical |
| §4.2 | §4.2 hamerton C8=2.27 | 2.27 | 2.267 | MATCH | empirical |
| §4.2 | §4.2 sunity_devee C5=1.03 | 1.03 | 1.026 | MATCH | empirical |
| §4.2 | §4.2 sunity_devee C2a=2.27 | 2.27 | 2.267 | MATCH | empirical |
| §4.2 | §4.2 sunity_devee C4a=2.41 | 2.41 | 2.41 | MATCH | empirical |
| §4.2 | §4.2 sunity_devee C8=2.55 | 2.55 | 2.554 | MATCH | empirical |
| §4.2 | §4.2 ebers C5=1.02 | 1.02 | 1.021 | MATCH | empirical |
| §4.2 | §4.2 ebers C2a=1.54 | 1.54 | 1.538 | MATCH | empirical |
| §4.2 | §4.2 ebers C4a=2.07 | 2.07 | 2.072 | MATCH | empirical |
| §4.2 | §4.2 ebers C8=2.18 | 2.18 | 2.185 | MATCH | empirical |
| §4.2 | §4.2 fukuzawa C5=1.67 | 1.67 | 1.672 | MATCH | empirical |
| §4.2 | §4.2 fukuzawa C2a=2.35 | 2.35 | 2.354 | MATCH | empirical |
| §4.2 | §4.2 fukuzawa C4a=2.78 | 2.78 | 2.779 | MATCH | empirical |
| §4.2 | §4.2 fukuzawa C8=2.74 | 2.74 | 2.738 | MATCH | empirical |
| §4.2 | §4.2 bernal_diaz C5=1.7 | 1.7 | 1.697 | MATCH | empirical |
| §4.2 | §4.2 bernal_diaz C2a=2.27 | 2.27 | 2.267 | MATCH | empirical |
| §4.2 | §4.2 bernal_diaz C4a=2.48 | 2.48 | 2.482 | MATCH | empirical |
| §4.2 | §4.2 bernal_diaz C8=2.55 | 2.55 | 2.574 | MINOR_ROUNDING | empirical |
| §4.2 | §4.2 babur C5=1.76 | 1.76 | 1.759 | MATCH | empirical |
| §4.2 | §4.2 babur C2a=1.91 | 1.91 | 1.908 | MATCH | empirical |
| §4.2 | §4.2 babur C4a=2.01 | 2.01 | 2.01 | MATCH | empirical |
| §4.2 | §4.2 babur C8=2.05 | 2.05 | 2.077 | MINOR_ROUNDING | empirical |
| §4.2 | §4.2 seacole C5=1.77 | 1.77 | 1.774 | MATCH | empirical |
| §4.2 | §4.2 seacole C2a=2.48 | 2.48 | 2.482 | MATCH | empirical |
| §4.2 | §4.2 seacole C4a=2.59 | 2.59 | 2.595 | MATCH | empirical |
| §4.2 | §4.2 seacole C8=2.83 | 2.83 | 2.831 | MATCH | empirical |
| §4.2 | §4.2 keckley C5=1.84 | 1.84 | 1.841 | MATCH | empirical |
| §4.2 | §4.2 keckley C2a=2.43 | 2.43 | 2.426 | MATCH | empirical |
| §4.2 | §4.2 keckley C4a=2.44 | 2.44 | 2.436 | MATCH | empirical |
| §4.2 | §4.2 keckley C8=2.5 | 2.5 | 2.497 | MATCH | empirical |
| §4.2 | §4.2 yung_wing C5=1.88 | 1.88 | 1.877 | MATCH | empirical |
| §4.2 | §4.2 yung_wing C2a=2.22 | 2.22 | 2.215 | MATCH | empirical |
| §4.2 | §4.2 yung_wing C4a=2.4 | 2.4 | 2.4 | MATCH | empirical |
| §4.2 | §4.2 yung_wing C8=2.42 | 2.42 | 2.421 | MATCH | empirical |
| §4.2 | §4.2 mean C5 1.52 | 1.52 | 1.547 | MATCH | empirical |
| §4.2 | §4.2 mean C2a 2.23 | 2.23 | 2.232 | MATCH | empirical |
| §4.2 | §4.2 mean C4 2.35 | 2.35 | 2.352 | MATCH | empirical |
| §4.2 | §4.2 mean C8 2.45 | 2.45 | 2.46 | MATCH | empirical |
| §4.2 | §4.2 mean C4a 2.45 | 2.45 | 2.439 | MATCH | empirical |
| §4.2 | §4.2 mean C9 2.59 | 2.59 | 2.594 | MATCH | empirical |
| §4.2 | §4.2 mean C8-C2a +0.22 | 0.22 | 0.2285 | MINOR_ROUNDING | empirical |
| §4.2 | §4.2 hamerton compression ratio ≈7× | 7 | 7 | MATCH | empirical |
| §4.2 | §4.2 sunity_devee compression ratio ≈13× | 13 | 13 | MATCH | empirical |
| §4.2 | §4.2 ebers compression ratio ≈17× | 17 | 17 | MATCH | empirical |
| §4.2 | §4.2 fukuzawa compression ratio ≈26× | 26 | 26 | MATCH | empirical |
| §4.2 | §4.2 bernal_diaz compression ratio ≈33× | 33 | 33 | MATCH | empirical |
| §4.2 | §4.2 babur compression ratio ≈79× | 79 | 79 | MATCH | empirical |
| §4.2 | §4.2 seacole compression ratio ≈12× | 12 | 12 | MATCH | empirical |
| §4.2 | §4.2 keckley compression ratio ≈11× | 11 | 11 | MATCH | empirical |
| §4.2 | §4.2 yung_wing compression ratio ≈13× | 13 | 13 | MATCH | empirical |
| §4.2.1 | §4.2.1 C2a improve 70.9% | 70.9 | 70.94 | MATCH | empirical |
| §4.2.1 | §4.2.1 C4 improve 72.9% | 72.9 | 72.93 | MATCH | empirical |
| §4.2.1 | §4.2.1 C8 improve 78.3% | 78.3 | 78.63 | MATCH | empirical |
| §4.2.1 | §4.2.1 C4a improve 78.6% | 78.6 | 78.63 | MATCH | empirical |
| §4.2.1 | §4.2.1 median improvement +1.0 | 1.0 | 1 | MATCH | empirical |
| §4.2.1 | §4.2.1 median worsening -0.4 | -0.4 | -0.4 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C2a improve 58.8% | 58.8 | 58.79 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C4 improve 60.1% | 60.1 | 60.07 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C8 improve 64.5% (paper) | 64.5 | 65.2 | MISMATCH | empirical |
| §4.2.1 | §4.2.1 all14 C4a improve 65.8% | 65.8 | 65.75 | MATCH | empirical |
| §4.2.1 | §4.2.1 C8 vs C2a better 53.3% | 53.3 | 53.28 | MATCH | empirical |
| §4.2.1 | §4.2.1 C8 vs C2a worse 30.8% | 30.8 | 30.77 | MATCH | empirical |
| §4.2.1 | §4.2.1 C9 vs C4a better 49.0% | 49.0 | 49.04 | MATCH | empirical |
| §4.2.1 | §4.2.1 C9 vs C4a worse 36.5% | 36.5 | 36.54 | MATCH | empirical |
| §4.2.1 | §4.2.1 C8 vs C2a better n=187 | 187 | 187 | MATCH | empirical |
| §4.2.1 | §4.2.1 C8 vs C2a worse n=108 | 108 | 108 | MATCH | empirical |
| §4.2.1 | §4.2.1 C9 vs C4a better n=153 | 153 | 153 | MATCH | empirical |
| §4.2.1 | §4.2.1 C9 vs C4a worse n=114 | 114 | 114 | MATCH | empirical |
| §4.3 | §4.3 augustine v1 Δ=-0.47 | -0.47 | -0.4718 | MATCH | empirical |
| §4.3 | §4.3 augustine v2 Δ=0.13 | 0.13 | 0.1254 | MATCH | empirical |
| §4.3 | §4.3 babur v1 Δ=-0.59 | -0.59 | -0.5897 | MATCH | empirical |
| §4.3 | §4.3 babur v2 Δ=0.76 | 0.76 | 0.756 | MATCH | empirical |
| §4.3 | §4.3 bernal_diaz v1 Δ=0.09 | 0.09 | 0.09231 | MATCH | empirical |
| §4.3 | §4.3 bernal_diaz v2 Δ=0.69 | 0.69 | 0.6876 | MATCH | empirical |
| §4.3 | §4.3 cellini v1 Δ=-0.56 | -0.56 | -0.5641 | MATCH | empirical |
| §4.3 | §4.3 cellini v2 Δ=-0.87 | -0.87 | -0.8745 | MATCH | empirical |
| §4.3 | §4.3 ebers v1 Δ=0.3 | 0.3 | 0.2974 | MATCH | empirical |
| §4.3 | §4.3 ebers v2 Δ=0.79 | 0.79 | 0.7895 | MATCH | empirical |
| §4.3 | §4.3 equiano v1 Δ=-0.79 | -0.79 | -0.7949 | MATCH | empirical |
| §4.3 | §4.3 equiano v2 Δ=-1.0 | -1.0 | -0.9992 | MATCH | empirical |
| §4.3 | §4.3 fukuzawa v1 Δ=0.26 | 0.26 | 0.2615 | MATCH | empirical |
| §4.3 | §4.3 fukuzawa v2 Δ=0.86 | 0.86 | 0.8647 | MATCH | empirical |
| §4.3 | §4.3 keckley v1 Δ=-0.49 | -0.49 | -0.4872 | MATCH | empirical |
| §4.3 | §4.3 keckley v2 Δ=0.14 | 0.14 | 0.139 | MATCH | empirical |
| §4.3 | §4.3 rousseau v1 Δ=-0.52 | -0.52 | -0.5231 | MATCH | empirical |
| §4.3 | §4.3 rousseau v2 Δ=-0.37 | -0.37 | -0.3659 | MATCH | empirical |
| §4.3 | §4.3 seacole v1 Δ=-0.34 | -0.34 | -0.3436 | MATCH | empirical |
| §4.3 | §4.3 seacole v2 Δ=-0.1 | -0.1 | -0.1044 | MATCH | empirical |
| §4.3 | §4.3 sunity_devee v1 Δ=0.27 | 0.27 | 0.2667 | MATCH | empirical |
| §4.3 | §4.3 sunity_devee v2 Δ=0.53 | 0.53 | 0.5349 | MATCH | empirical |
| §4.3 | §4.3 yung_wing v1 Δ=0.32 | 0.32 | 0.3231 | MATCH | empirical |
| §4.3 | §4.3 yung_wing v2 Δ=0.39 | 0.39 | 0.3931 | MATCH | empirical |
| §4.3 | §4.3 zitkala_sa v1 Δ=-0.68 | -0.68 | -0.6769 | MATCH | empirical |
| §4.3 | §4.3 zitkala_sa v2 Δ=0.04 | 0.04 | 0.03654 | MATCH | empirical |
| §4.3 | §4.3 detection explicit 60.6% | 60.6 | 60.65 | MATCH | empirical |
| §4.3 | §4.3 detection misapply 36.5% | 36.5 | 36.46 | MATCH | empirical |
| §4.3 | §4.3 detection hedged 2.0% | 2.0 | 2.044 | MATCH | empirical |
| §4.3 | §4.3 detection ambiguous 0.9% | 0.9 | 0.8518 | MATCH | empirical |
| §4.3 | §4.3 wrong-spec total n=587 | 587 | 587 | MATCH | empirical |
| §4.3 | §4.3 spec-tag citation correct 78.6% | 78.6 | 78.63 | MATCH | empirical |
| §4.3 | §4.3 spec-tag citation wrong 50.0% | 50.0 | 50 | MATCH | empirical |
| §4.3 | §4.3 hedging narrow C2a 1.4% | 1.4 | 1.38 | MATCH | empirical |
| §4.3 | §4.3 hedging broad C2a 7.9% | 7.9 | 7.89 | MATCH | empirical |
| §4.3 | §4.3 wrong-spec gap 0.60 | 0.6 | 0.6008 | MATCH | empirical |
| §3.6.6 | §3.6.6 abstention n=192 | 192 | 192 | MATCH | empirical |
| §3.6.6 | §3.6.6 abstention pct<2: 82.8% | 82.8 | 82.81 | MATCH | empirical |
| §3.6.6 | §3.6.6 abstention pct>=2: 9.4% | 9.4 | 9.375 | MATCH | empirical |
| §3.6.6 | §3.6.6 abstention pct>=3: 3.1% | 3.1 | 3.125 | MATCH | empirical |
| §3.6.6 | §3.6.6 abstention mean 1.27 | 1.27 | 1.27 | MATCH | empirical |
| §3.6.6 | §3.6.6 strictness Sonnet 1.14 | 1.14 | 1.141 | MATCH | empirical |
| §3.6.6 | §3.6.6 strictness GPT-5.4 1.17 | 1.17 | 1.167 | MATCH | empirical |
| §3.6.6 | §3.6.6 strictness Haiku 1.29 | 1.29 | 1.286 | MATCH | empirical |
| §3.6.6 | §3.6.6 strictness GPT-4o 1.34 | 1.34 | 1.344 | MATCH | empirical |
| §3.6.6 | §3.6.6 strictness Opus 1.41 | 1.41 | 1.411 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=0.26 (overall) | 0.26 | 0.2564 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=0.604 (C5) | 0.604 | 0.6037 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=0.14 (C2a) | 0.14 | 0.144 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=0.01 (C4) | 0.01 | 0.008759 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=-0.01 (C4a) | -0.01 | -0.01271 | MATCH | empirical |
| §3.6.6 | §3.6.6 length r=0.500 C2c | 0.5 | 0.4996 | MATCH | empirical |
| §3.6.6 | §3.6.6 ultra-high chars 2790 | 2790 | 2790 | MATCH | empirical |
| §3.6.6 | §3.6.6 mid-range chars 2829 | 2829 | 2829 | MATCH | empirical |
| §3.6.6 | §3.6.6 low-range chars 2087 | 2087 | 2087 | MATCH | empirical |
| §3.6.6 | §3.6.6 total responses 1599 | 1599 | 1599 | MATCH | empirical |
| §3.6.4 | §3.6.4 Spearman 5j min 0.86 | 0.86 | 0.8577 | MATCH | empirical |
| §3.6.4 | §3.6.4 Spearman 5j max 0.93 | 0.93 | 0.9324 | MATCH | empirical |
| §3.6.4 | §3.6.4 Krippendorff 5j 0.659 | 0.659 | 0.6543 | MATCH | empirical |
| §3.6.4 | §3.6.4 Krippendorff 7j 0.535 | 0.535 | 0.5221 | MATCH | empirical |
| §3.2 | §3.2 Franklin C5 5-judge 3.77 | 3.77 | 3.77 | MATCH | empirical |
| §3.2 | §3.2 Franklin Haiku-only 4.10 | 4.1 | 4.1 | MATCH | empirical |
| §3.6.3 | §3.6.3 haiku verbatim=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 haiku paraphrased=4.75 | 4.75 | 4.75 | MATCH | empirical |
| §3.6.3 | §3.6.3 haiku short_correct=3.8 | 3.8 | 3.8 | MATCH | empirical |
| §3.6.3 | §3.6.3 haiku long_correct=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_flash verbatim=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_flash paraphrased=4.7 | 4.7 | 4.7 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_flash short_correct=3.85 | 3.85 | 3.85 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_flash long_correct=3.8 | 3.8 | 3.8 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt4o verbatim=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt4o paraphrased=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt4o short_correct=4.05 | 4.05 | 4.05 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt4o long_correct=3.35 | 3.35 | 3.35 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_pro verbatim=4.15 | 4.15 | 4.15 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_pro paraphrased=3.55 | 3.55 | 3.55 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_pro short_correct=2.85 | 2.85 | 2.85 | MATCH | empirical |
| §3.6.3 | §3.6.3 gemini_pro long_correct=1.2 | 1.2 | 1.2 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt54 verbatim=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt54 paraphrased=5.0 | 5.0 | 5 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt54 short_correct=4.2 | 4.2 | 4.2 | MATCH | empirical |
| §3.6.3 | §3.6.3 gpt54 long_correct=4.8 | 4.8 | 4.8 | MATCH | empirical |
| §B.3 | §B.3 LITERAL_RECALL 10.2% | 10.2 | 10.2 | MATCH | empirical |
| §B.3 | §B.3 INTERPRETIVE 68.8% | 68.8 | 68.8 | MATCH | empirical |
| §B.3 | §B.3 REFUSAL 21.0% | 21.0 | 21 | MATCH | empirical |
| §B.4 | §B.4 LITERAL_RECALL mean Δ +0.792 | 0.792 | 0.75 | MINOR_ROUNDING | empirical |
| §B.4 | §B.4 LITERAL_RECALL median +0.800 | 0.8 | 0.8 | MATCH | empirical |
| §B.4 | §B.4 INTERPRETIVE mean Δ +0.397 | 0.397 | 0.377 | MINOR_ROUNDING | empirical |
| §B.4 | §B.4 REFUSAL mean Δ +0.417 | 0.417 | 0.4167 | MATCH | empirical |
| §B.4 | §B.4 LITERAL_RECALL n=60 | 60 | 60 | MATCH | empirical |
| §B.4 | §B.4 INTERPRETIVE n=366 | 366 | 366 | MATCH | empirical |
| §B.4 | §B.4 REFUSAL n=120 | 120 | 120 | MATCH | empirical |
| §B.6 | §B.6 LITERAL_RECALL corr +0.595 | 0.595 | 0.5949 | MATCH | empirical |
| §B.6 | §B.6 INTERPRETIVE corr -0.466 | -0.466 | -0.4656 | MATCH | empirical |
| §B.6 | §B.6 REFUSAL corr +0.212 | 0.212 | 0.2118 | MATCH | empirical |
| §3.3 | §3.3 leakage 2/586 | 2 | 2 | MATCH | empirical |
| §3.3 | §3.3 leakage pct 0.34% | 0.34 | 0.3413 | MATCH | empirical |
| §D.2 | §D.2 hamerton upward 69.2% | 69.2 | 69.23 | MATCH | empirical |
| §D.2 | §D.2 sunity_devee upward 74.4% | 74.4 | 74.36 | MATCH | empirical |
| §D.2 | §D.2 fukuzawa upward 66.7% | 66.7 | 66.67 | MATCH | empirical |
| §D.2 | §D.2 bernal_diaz upward 59.0% | 59.0 | 58.97 | MATCH | empirical |
| §D.2 | §D.2 seacole upward 53.8% | 53.8 | 53.85 | MATCH | empirical |
| §D.2 | §D.2 ebers upward 48.7% | 48.7 | 48.72 | MATCH | empirical |
| §D.2 | §D.2 keckley upward 48.7% | 48.7 | 48.72 | MATCH | empirical |
| §D.2 | §D.2 yung_wing upward 48.7% | 48.7 | 48.72 | MATCH | empirical |
| §D.2 | §D.2 babur upward 25.6% | 25.6 | 25.64 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C2a worsen 26.7% | 26.7 | 26.74 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C4 worsen 26.6% | 26.6 | 26.56 | MATCH | empirical |
| §4.2.1 | §4.2.1 all14 C8 worsen 24.5% | 24.5 | 23.63 | MISMATCH | empirical |
| §4.2.1 | §4.2.1 all14 C4a worsen 26.4% | 26.4 | 26.37 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory controlled all14 improved 5/14 | 5 | 7 | MISMATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory controlled lowB improved 5/9 | 5 | 4 | MINOR_ROUNDING | empirical |
| §4.4.1 | §4.4.1 Supermemory controlled lowB Δ −0.01 | -0.01 | -0.01823 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory native lowB improved 4/9 | 4 | 4 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory native lowB Δ −0.03 | -0.03 | -0.02678 | MATCH | empirical |
| §4.4.1 | §4.4.1 Supermemory native all14 improved 6/14 | 6 | 6 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta native lowB improved 4/9 | 4 | 4 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 controlled lowB improved 6/9 | 6 | 6 | MATCH | empirical |
| §4.4.1 | §4.4.1 Base Layer controlled lowB improved 6/9 | 6 | 6 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 controlled all14 improved 10/14 | 10 | 10 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta controlled all14 improved 12/14 | 12 | 12 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep controlled all14 improved 13/14 | 13 | 13 | MATCH | empirical |
| §4.4.1 | §4.4.1 Zep native all14 improved 13/14 | 13 | 13 | MATCH | empirical |
| §4.4.1 | §4.4.1 Letta native all14 improved 5/14 | 5 | 5 | MATCH | empirical |
| §4.4.1 | §4.4.1 Mem0 native all14 improved 10/14 | 10 | 10 | MATCH | empirical |
| §4.4.1 | §4.4.1 Base Layer controlled all14 improved 9/14 | 9 | 9 | MATCH | empirical |
| §4.1 | §4.1 Hamerton Δ_C4a +1.51 | 1.51 | 1.513 | MATCH | empirical |
| §4.1 | §4.1 Sunity Devee Δ_C4a +1.38 | 1.38 | 1.385 | MATCH | empirical |
| §4.1 | §4.1 Ebers Δ_C4a +1.05 | 1.05 | 1.051 | MATCH | empirical |
| §4.1 | §4.1 Fukuzawa Δ_C4a +1.11 | 1.11 | 1.108 | MATCH | empirical |
| §4.1 | §4.1 Bernal Diaz Δ_C4a +0.78 | 0.78 | 0.7846 | MATCH | empirical |
| §4.1 | §4.1 Babur Δ_C4a +0.25 | 0.25 | 0.2513 | MATCH | empirical |
| §4.1 | §4.1 Seacole Δ_C4a +0.82 | 0.82 | 0.8205 | MATCH | empirical |
| §4.1 | §4.1 Keckley Δ_C4a +0.59 | 0.59 | 0.5949 | MATCH | empirical |
| §4.1 | §4.1 Yung Wing Δ_C4a +0.52 | 0.52 | 0.5231 | MATCH | empirical |
| §4.1 | §4.1 Zitkala-Sa Δ_C4a -0.32 | -0.32 | -0.3179 | MATCH | empirical |
| §4.1 | §4.1 Cellini Δ_C4a +0.15 | 0.15 | 0.1487 | MATCH | empirical |
| §4.1 | §4.1 Rousseau Δ_C4a +0.10 | 0.1 | 0.09744 | MATCH | empirical |
| §4.1 | §4.1 Augustine Δ_C4a +0.11 | 0.11 | 0.1128 | MATCH | empirical |
| §4.1 | §4.1 Equiano Δ_C4a -0.35 | -0.35 | -0.3487 | MATCH | empirical |
| §4.1 | §4.1 Franklin Δ_C4a -0.13 | -0.13 | -0.125 | MINOR_ROUNDING | empirical |
