# V10 Paper Numerical Verification Report

**Paper:** `docs/beyond_recall_v10_draft.md` (Beyond Recall, v10, release-frozen 2026-04-24)
**Generated:** 2026-04-25
**Verification scripts:** `scripts/_v10_verification/`

## 1. Executive summary

A mechanical pass across §1 through §9 and Appendix A through F of the v10 paper. Every numeric claim was traced to either a primary data file (per-judge JSON) or an analysis report under `docs/research/`. Where feasible, claims were re-derived from primary data using `scipy` and `numpy`.

### 1.1 Counts

| Category | Count |
|---|---:|
| **VERIFIED** (re-derived to <=0.01 tolerance) | 122 |
| **CONSISTENT** (matches DATA_REFERENCE / KEY_FINDINGS / source doc) | 46 |
| **INCONSISTENT** (paper conflicts with primary data, source doc, or another section) | 9 |
| **UNVERIFIABLE** (no source data found in repository) | 1 |
| **CITED-FROM-EXTERNAL** (numbers from cited prior work, not in scope) | 16 |
| **TOTAL** | 194 |

### 1.2 Top inconsistencies

1. **§4.6.1 Tier 2 deltas don't reconcile with primary data.** Paper reports Δ +1.48 / +1.07 / +1.91 / +1.27 / +1.40 / -0.55 across 6 (subject × response model) cells, citing DATA_REFERENCE §10. The 5-judge primary recompute (`docs/research/tier2_recompute_s114.json`, `scripts/recompute_tier2_from_raw.py`) yields Δ_C2a +1.19 / +0.37 / +1.33 / +0.22 / +1.11 / -0.13. Δ_C4a values are also different. The s114 audit (`docs/reviews/s114_full_data_audit.md`) flagged this as HIGH priority. The paper's numbers cannot be reproduced from `results/_tier2/global_<subject>/tier2_<sonnet|gemini_pro>_judgments_*.json`. **5 of 6 directional matches still hold, but the magnitudes do not.**

2. **§4.2 Table 4.2 mean row contains internal arithmetic errors.** Paper reports column means 1.52 / 2.23 / 2.35 / 2.45 / 2.45 / 2.50 across (C5, C2a, C4, C8, C4a, C9). Recompute over the same 9-subject low-baseline rows gives 1.55 / 2.23 / 2.35 / 2.45 / 2.44 / 2.59. The C5 mean (1.52 vs 1.55) appears to be an 8-row mean (Babur excluded), while C2a-C8 means are 9-row including Babur (inconsistent aggregation across columns within the same row). The C9 mean (paper 2.50 vs row-derived 2.59) is off by 0.09; summing the paper's own 8 row values yields 20.74 / 8 = 2.59, contradicting the printed 2.50.

3. **§4.3 / §1.3 wrong-spec detection rate is documented as computed on NAMED specs, not anonymized specs, which inverts the paper's bound interpretation.** Paper line 932 claims "Specifications are anonymized by design (§3.3), so the 60.6% is a lower bound on content-grounded detection." The source analysis (`docs/research/wrong_spec_detection_analysis.md`) explicitly notes "Specs are named, not anonymized... A portion of 'explicit detection' is therefore triggered by trivial name-mismatch rather than deeper behavioral-mismatch recognition." The 60.6% number is correctly computed, but if specs were named (per the doc), then 60.6% is an UPPER bound on content-grounded detection (some fraction is trivial name-mismatch flagging), not a LOWER bound. The directional framing flips depending on which methodology was actually used.

4. **§4.2 efficiency-claim numbers use two different C5 means.** The paragraph at line 781 says "+0.68 points of lift above baseline on average" (consistent with 9-subject C5 = 1.55) and at line 807 says "spec lift +0.71" (consistent with the table's 1.52). Same paragraph, two implicit C5 means. Only one can be right.

5. **§4.4.1 controlled Wilcoxon Mem0 W = 15.0 result not reported in paper.** Mem0 controlled is given Wilcoxon p=0.0166 in `docs/research/memory_systems_5judge_primary.md` and `docs/research/stats_update.md`, but paper §4.4.1 says only "Mem0... not significant at α = 0.05" (true at α=0.01 not α=0.05). Marginal phrasing inconsistency, not a number conflict per se.

### 1.3 Highest-confidence verifications

The §4.1 gradient table, the §4.3 wrong-spec deltas, the §4.2.1 question-improvement rates, the hedging-rate counts, the anchor-crossing percentages, the memory-system Δ_spec aggregates, the Letta stateful results, and the Wilcoxon statistics all match primary data to 2 decimal places.

---

## 2. Per-section walkthrough

### 2.1 §1 Introduction

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §1.1 | "accuracies in roughly the 68% to 85% range" | 68%-85% | Cited from §2.1 vendor reports | CITED-FROM-EXTERNAL |
| §1.2 | "14 historical subjects" | 14 | §3.2 subject list | VERIFIED |
| §1.2 | "39 behavioral prediction questions" per subject | 39 | Battery files; §3.4 line 353 | VERIFIED |
| §1.2 | "586 questions across 15 subjects (14 + Franklin)" | 586 | §3.4 line 353; Appendix B.2 column total | VERIFIED |
| §1.2 | "0.34% aggregate" leakage; "0.00%" main study | 2/586 | §3.4 line 355; `_verify_battery_leakage.py` | CONSISTENT |
| §1.2 | "5 non-Gemini judges" + "2 Gemini judges" | 5 / 2 | §3.7.1 panel | VERIFIED |
| §1.2 | "approximately 1 point" Gemini inflation | ~1 pt | §3.7.2 calibration table; verbatim 5.00→4.15 etc. | VERIFIED |
| §1.2 | "pairwise Spearman ρ = 0.86-0.93" | 0.86-0.93 | `docs/research/stats_update.md` 5-judge range [0.858, 0.932] | VERIFIED |
| §1.3 | "C4a-level regression on C5: slope +0.04 [-0.25, +0.33], R² = 0.008" | +0.04 / R²=0.008 | `docs/research/v10_coupling_sensitivity_analysis.md` | VERIFIED |
| §1.3 | "Wilcoxon signed-rank... p = 0.007 (W = 11, N = 14)" | W=11 / p=0.007 | `recompute_5judge_primary.py`: W=11.0, p=0.006714 | VERIFIED |
| §1.3 | "12 of 14 overall; 9 of 9 on the low-baseline slice" | 12/14, 9/9 | gradient table § 4.1 | VERIFIED |
| §1.3 | "Mean Δ_C4a on low-baseline slice: +0.89 points" | +0.89 | recompute = +0.8923 | VERIFIED |
| §1.3 | "55.0% upward; 70.9% questions improve" | 55.0% / 70.9% | `compute_anchor_crossing.py`; `_compute_per_question_v2.py` | VERIFIED |
| §1.3 | "correct +0.35 vs random-derangement +0.22 vs adversarial-derangement -0.25" | +0.35/+0.22/-0.25 | recompute: +0.3538 / +0.2161 / -0.2469 | VERIFIED |
| §1.3 | "28.8% → 1.4% → 0.0%" | 28.8/1.4/0.0 | `hedging_analysis.json` C5/C2a/C4a starts_refusal: 146/507=0.288, 7/507=0.0138, 0/507=0.0 | VERIFIED |
| §1.3 | "Mem0 +0.10, Letta-archival +0.17, Zep +0.17, Supermemory −0.01" | +0.10/+0.17/+0.17/-0.01 | `memory_systems_5judge_primary.md` low-baseline controlled: +0.101/+0.165/+0.166/-0.010 | VERIFIED |
| §1.3 | "Slope of −0.96 (95% CI: −1.24, −0.67)" | -0.96 / [-1.24, -0.67] | recompute: -0.9597 / [-1.2447, -0.6747] | VERIFIED |
| §1.3 | "R² = 0.82" | 0.82 | recompute: 0.8177 | VERIFIED |
| §1.3 | "p < 0.001" | <0.001 | recompute p = 9.0e-6 | VERIFIED |
| §1.3 | "+0.89 mean, 9 of 9 improve" | +0.89, 9/9 | recompute | VERIFIED |
| §1.3 | "60.6% explicit-detection rate" | 60.6% | `wrong_spec_detection_analysis.md`: 356/587=60.6% | VERIFIED |
| §1.3 | Hamerton C2a 2.63, C8 2.27, C9 3.09, C4a 2.77 | as stated | recompute confirms exactly | VERIFIED |
| §1.3 | "0.22 points" mean spec-vs-corpus gap | +0.22 | recompute: C8-C2a 9-subj mean = +0.2226 | VERIFIED |
| §1.3 | "narrow rule" 28.8/1.4/0.0; "broader rule" 41.2/7.9/0.4 | both rules | `hedging_analysis.json`: secondary_metrics.refusal_ge_1 = 209/507/40/507/2/507 = 41.22%/7.89%/0.39% | VERIFIED |
| §1.3 | "146/507", "7/507", "0/507", "209/507", "40/507", "2/507" | as stated | hedging_analysis.json | VERIFIED |
| §1.3 | "Mem0 (+0.12 controlled, +0.33 native)" | +0.12 / +0.33 | memory_systems_5judge_primary.md: +0.121/+0.332 | VERIFIED |
| §1.3 | "Zep... (+0.19 controlled, +0.33 native)" | +0.19/+0.33 | doc: +0.186/+0.327 | VERIFIED |
| §1.3 | "Letta archival... -0.02 native" | -0.02 | doc: -0.023 | VERIFIED |
| §1.3 | Supermemory "median improvement +1.45, median worsening −1.41" | +1.45/-1.41 | `_sm_paired_5judge.json`: mean positive swing 1.4541, mean negative swing -1.4064 | VERIFIED |
| §1.3 | "Base Layer ... C1 mean ~2.30 across 14 subjects" | ~2.30 | computed across-subject mean of C1_baselayer not stored as single number; consistent with per-subject distribution | CONSISTENT |
| §1.3 | "highest retrieval-only (C1) mean of the four (~2.65) [Supermemory]" | ~2.65 | per-subject C1_supermemory means range ~2.0-2.9; 14-subject mean falls near 2.65 | CONSISTENT |
| §1.3 | "Letta block sizes: 22,472, 68,413, 335,349 chars" | as stated | `letta_stateful_matched_rerun.md` | VERIFIED |
| §1.3 | "Hamerton 3.10 vs. 2.96; Ebers 2.76 vs. 1.72; Babur 2.42 vs. 1.88" Letta vs BL | as stated | `5judge_primary_results.json`: 3.103/2.964, 2.760/1.715, 2.415/1.880 | VERIFIED |
| §1.3 | "Δ +0.27 / +1.21 / +0.38" full-stack rerun | +0.27/+1.21/+0.38 | `RESULTS.md` fullstack_named: +0.272/+1.205/+0.380 | VERIFIED |
| §1.3 | "25.4% verbatim sentence duplication" Babur block | 25.4% | `letta_stateful_matched_rerun.md` | CONSISTENT |
| §1.3 | "approximately 333,000 characters" Letta API ceiling | ~333,000 | `letta_stateful_matched_rerun.md` | CONSISTENT |

### 2.2 §2 Prior Work

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §2.1 | "Mem0 91.6 LOCOMO, 93.4 LongMemEval" | 91.6 / 93.4 | Vendor reports | CITED-FROM-EXTERNAL |
| §2.1 | "Mem0g 68.44 with GPT-4o-mini" (Chhikara et al., 2025) | 68.44 | Cited paper arXiv:2504.19413 | CITED-FROM-EXTERNAL |
| §2.1 | "Letta 74.0% on LOCOMO" | 74.0% | Letta blog 2025-08-12 | CITED-FROM-EXTERNAL |
| §2.1 | "Supermemory 81.6% / 84.6% / 85.2% LongMemEval_s" | 3 numbers | Vendor self-report | CITED-FROM-EXTERNAL |
| §2.1 | "Zep 71.2% LongMemEval (Rasmussen et al.)" | 71.2% | arXiv:2501.13956 | CITED-FROM-EXTERNAL |
| §2.5 | "over 80% MT-Bench, Chatbot Arena" (Zheng et al.) | 80% | NeurIPS 2023 | CITED-FROM-EXTERNAL |
| §2.3.4 (Twin-2K) | "2,058 participants" | 2,058 | Toubia et al. 2025 | CITED-FROM-EXTERNAL |
| §2.3 (PersonaGym) | "4.51 ± 0.08", "3.64 ± 0.57" | as stated | Samuel et al. 2025 | CITED-FROM-EXTERNAL |
| §2.3 (LoCoMo) | "GPT-4-turbo 32.1%, GPT-3.5-turbo 22.4%, ... best RAG 41.4%, human 87.9%" | 5 numbers | Maharana et al. 2024 | CITED-FROM-EXTERNAL |
| §2.3.4 | Twin-2K "71.72% individual-level accuracy" | 71.72% | Toubia et al. 2025 | CITED-FROM-EXTERNAL |
| §2.3.4 | "Human test-retest 81.72%, top twin at 87.67% of human ceiling, random 59.17%" | 4 numbers | Toubia et al. 2025 | CITED-FROM-EXTERNAL |
| §2.3.4 | "6 of 10 behavioral-economics experiments" replicated | 6/10 | Toubia et al. 2025 | CITED-FROM-EXTERNAL |
| §2.3 / §2.4 | "+45% Gemini 2.5 Pro" sycophancy (Jain et al.) | +45% | Jain et al. 2025 | CITED-FROM-EXTERNAL |
| §2.4 | "Jiang ~50% accuracy on dynamic profiling" | ~50% | Jiang et al. COLM 2025 | CITED-FROM-EXTERNAL |

### 2.3 §3 Study Design

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §3.2 | Subject word counts (14 subjects) | as stated | Source corpora; matches `data/<subject>/training.txt` size estimates | CONSISTENT |
| §3.2 | "Hamerton 25,231 words" | 25,231 | letta_stateful_matched_rerun.md | VERIFIED |
| §3.2 | "Babur 422,772 words" | 422,772 | same | VERIFIED |
| §3.2 | "Franklin baseline 3.77 on 5-judge" | 3.77 | `recompute_5judge_primary.py` Franklin data; computed via legacy_20260411 files | CONSISTENT |
| §3.2 | "Franklin 4.10 on Haiku alone" | 4.10 | KEY_FINDINGS.md, S105 results | CONSISTENT |
| §3.2.1 | "9 / 5 / 1" baseline-band counts | 9/5/1 | direct from §4.1 table | VERIFIED |
| §3.4 | "586 BP questions, 0.34% aggregate leak (2/586), 0% main study" | 2/586=0.34% | §3.4; `_verify_battery_leakage.py` | VERIFIED |
| §3.4 | "Zitkala-Sa Q18 false-premise outlier" | 1/586=0.17% | §3.4 line 357 | CONSISTENT |
| §3.7.2 | Calibration scores: Haiku 5.00/4.75/3.80/5.00 etc. | as stated | `results/judge_calibration/` raw data assumed; matches v9 numbers | CONSISTENT |
| §3.7.4 | "Spearman ρ = 0.86-0.93 across 21 judge pairs" | 0.86-0.93 | `stats_update.md` 5-judge range [0.858, 0.932]. NOTE: paper says "21 judge pairs" but the 0.86-0.93 range is the **10-pair 5-judge primary**, not 21 pairs. The 7-judge 21-pair range is [0.29, 0.93] (per stats_update.md §5). | INCONSISTENT |
| §3.7.4 | "Krippendorff α (ordinal) = 0.659 (5-judge), 0.535 (7-judge)" | 0.659 / 0.535 | v9 ordinal values; recompute (interval) gives 0.654/0.522. Ordinal vs interval distinction not stated but ordinal claim is unchanged from v9 | CONSISTENT |
| §3.7.5 | "ρ = 0.86-0.93" again | same | as above (5-judge range) | CONSISTENT |
| §3.7.6 | "192 abstention responses... 82.8% / 9.4% / 3.2%" | 192/82.8/9.4/3.2 | `audit_low_end_inflation.py` output | CONSISTENT |
| §3.7.6 | "Mean abstention score 1.27" | 1.27 | doc | CONSISTENT |
| §3.7.6 | "1,599 low-baseline responses, length r = 0.26 overall, 0.604 in C5" | 1,599 / 0.26 / 0.604 | doc | CONSISTENT |
| §3.7.6 | "C2a r = 0.14, C4 r = 0.01, C4a r = -0.01" | 0.14/0.01/-0.01 | doc | CONSISTENT |
| §3.7.6 | "Ultra-high (4.5+) 2,790 chars vs mid-range 2,829" | 2,790 / 2,829 | doc | CONSISTENT |
| §3.7.6 | "Per-judge strictness Sonnet 1.14, GPT-5.4 1.17, Haiku 1.29, GPT-4o 1.34, Opus 1.41" | 5 numbers | doc | CONSISTENT |

### 2.4 §4 Results: gradient

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.1 | Per-subject 5-judge primary table (14 + Franklin) | full table | recompute_5judge_primary.py | VERIFIED |
| §4.1 | "351 individual responses, 55.0% upward crossings" | 351 / 55.0% | `compute_anchor_crossing.py`: 193/351=55.0% | VERIFIED |
| §4.1 | All 7 transition % (33.3, 12.3, 4.8, 0.9, 2.0, 0.3, 1.4) | as stated | same script | VERIFIED |
| §4.1 | "38.2% no upward crossing, 6.8% downward" | 38.2/6.8 | same: 134/351=38.2%, 24/351=6.8% | VERIFIED |
| §4.1 | "Slope -0.96 [95% CI -1.24, -0.67], R²=0.82" | as stated | recompute -0.9597 [-1.2447, -0.6747], R²=0.8177 | VERIFIED |
| §4.1 | "p = 0.000009" | 9e-6 | recompute 9.02e-06 | VERIFIED |
| §4.1 | "Correlation r = -0.90" | -0.90 | recompute -0.9043 | VERIFIED |
| §4.1 | "Wilcoxon C5 vs C2a: W=10, p=0.005" | W=10/p=0.005 | recompute W=10, p=0.005249 | VERIFIED |
| §4.1 | "Wilcoxon C5 vs C4a: W=11, p=0.007" | W=11/p=0.007 | recompute W=11, p=0.006714 | VERIFIED |
| §4.1 | "Hamerton baseline 1.26, Δ_C4a +1.51" | 1.26/+1.51 | gradient table | VERIFIED |
| §4.1 | "Babur 1.76, +0.25" | 1.76/+0.25 | gradient table | VERIFIED |
| §4.1 | "Franklin baseline 3.77, Δ_C4a -0.13" | 3.77/-0.13 | gradient table | VERIFIED |
| §4.1 | "C5 baseline mean 1.52" (line 698) | 1.52 | recompute 9-subj 1.55, paper number is 8-subj 1.521 (excludes Babur) | INCONSISTENT |
| §4.1 (sensitivity) | "Partial coefficient C5 baseline -0.88 [-1.13, -0.63], p < 10⁻⁵" | -0.88 [-1.13, -0.63] | `v10_battery_sensitivity_analysis.md`: -0.880 [-1.127, -0.633] p=7.9e-6 | VERIFIED |
| §4.1 (sensitivity) | "LITERAL_RECALL +2.30 [+0.34, +4.26], p = 0.026" | +2.30 [+0.34, +4.26] / p=0.026 | doc: +2.297 [+0.337, +4.256] p=0.026 | VERIFIED |
| §4.1 (sensitivity) | "63.6% unique to C5, 6.9% to LITERAL_RECALL" | 63.6 / 6.9 | doc | VERIFIED |
| §4.1 (sensitivity) | "Adjusted R² rises 0.80 to 0.87" | 0.80 → 0.87 | doc adj R²: univariate=0.803, multivariate=0.866 | VERIFIED |
| §4.1 (sensitivity) | "Pearson r = -0.28, VIF = 1.08" | -0.28 / 1.08 | doc: -0.275 / 1.082 | VERIFIED |
| §4.1 (sensitivity) | "GPT-5.4 subset: -0.89 [-1.18, -0.61], R²=0.81, p<10⁻⁴" | -0.89 [-1.18, -0.61] R²=0.81 | doc: -0.892 [-1.180, -0.605] R²=0.810 p=2.8e-5 | VERIFIED |
| §4.1 (coupling) | "level slope +0.04 [-0.25, +0.33], R²=0.008, p=0.76" | as stated | `v10_coupling_sensitivity_analysis.md`: +0.0402 [-0.245, +0.325] R²=0.0078 p=0.76 | VERIFIED |
| §4.1 (coupling) | "C4a clusters near 2.46" | 2.46 | doc: mean 2.46 | VERIFIED |
| §4.1 (coupling) | "permutation null centered -0.998 SD 0.127, p = 0.77" | as stated | doc: -0.9984/0.1270/p=0.77 | VERIFIED |
| §4.1 (coupling) | "bootstrap CI Δ-on-C5 [-1.254, -0.740]" | as stated | doc: [-1.2535, -0.7396] | VERIFIED |
| §4.1 (coupling) | "level slope bootstrap [-0.254, +0.260]" | as stated | doc: [-0.2535, +0.2604] | VERIFIED |
| §4.1.1 | "Franklin C2a -0.40, C4a -0.13" | -0.40 / -0.13 | gradient table; recompute confirms | VERIFIED |

### 2.5 §4 Results: compression and §4.2.1

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.2 | Per-subject C2a/C4/C8/C4a/C9 table (low-baseline 9 subj) | full table | recompute confirms each cell exactly | VERIFIED |
| §4.2 | "Hamerton 7,300-token spec C2a 2.63" | 2.63 | recompute | VERIFIED |
| §4.2 | "C8 2.27, C9 3.09, C4a 2.77" Hamerton | as stated | recompute | VERIFIED |
| §4.2 | "Mean C5 = 1.52" | 1.52 | recompute 9-subj = 1.55; matches 8-subj (Babur excluded) = 1.521 | INCONSISTENT |
| §4.2 | "Mean C2a = 2.23" | 2.23 | recompute 9-subj = 2.232 | VERIFIED |
| §4.2 | "Mean C4 = 2.35" | 2.35 | recompute 9-subj = 2.352 | VERIFIED |
| §4.2 | "Mean C8 = 2.45" | 2.45 | recompute 9-subj = 2.455 | VERIFIED |
| §4.2 | "Mean C4a = 2.45" | 2.45 | recompute 9-subj = 2.439 (rounds to 2.44) | INCONSISTENT (off by 0.01) |
| §4.2 | "Mean C9 = 2.50" | 2.50 | recompute 8-subj (Babur excluded) = 2.593; sum of paper's own 8 row values is 20.74 / 8 = 2.59 | INCONSISTENT |
| §4.2 | "C8-C2a mean +0.22" | +0.22 | recompute 9-subj diff = +0.2226 | VERIFIED |
| §4.2 | "spec lift +0.71" (line 807) vs "+0.68" (line 781) | 0.71/0.68 | 2.23 - 1.52 = 0.71; 2.23 - 1.55 = 0.68. Two different C5 means used in same section | INCONSISTENT |
| §4.2 | "corpus lift +0.93" | +0.93 | 2.45 - 1.52 = 0.93 (using paper 1.52 mean); using 1.55 → 0.90 | CONSISTENT (with paper's chosen mean) |
| §4.2 | "Ebers C2a 1.54 vs C8 2.18, gap 0.64" | 0.64 | 2.18 - 1.54 = 0.64 | VERIFIED |
| §4.2 | "Ebers spec lift +0.52, corpus lift +1.16" | +0.52/+1.16 | 1.54-1.02=0.52; 2.18-1.02=1.16 | VERIFIED |
| §4.2 | "spec at ~6%, corpus at 18× (Ebers)" | 6% / 18× | computed from token budgets | CONSISTENT |
| §4.2.1 | Low-baseline win rate: C2a 70.9, C4 72.9, C8 78.3, C4a 78.6, median +1.00 / -0.40 | 4 rates / 2 medians | `_compute_per_question_v2.py`: 70.9/72.9/78.3/78.6, median imp +1.00, wor -0.40 | VERIFIED |
| §4.2.1 | "351 questions" low-baseline | 351 | 9 × 39 = 351 | VERIFIED |
| §4.2.1 | "C9 n = 312 with Babur excluded" | 312 | 8 × 39 = 312 | VERIFIED |
| §4.2.1 | All-14 win rates: C2a 58.8/26.7, C4 60.1/26.6, C8 64.5/24.5, C4a 65.8/26.4 | 8 rates | recompute 14×39=546, 58.8/26.7, 60.1/26.6, 64.5/24.5, 65.8/26.4 | VERIFIED |
| §4.2.1 | "Raw corpus (C8) vs spec alone (C2a) | 190 (54.1%) | 46 | 115 (32.8%)" | as stated | recompute pairwise: 190/46/115, 54.1%/13.1%/32.8% | VERIFIED |
| §4.2.1 | "Corpus + spec (C9) vs facts + spec (C4a) | 155 (49.7%) | 42 | 115 (36.9%)" | as stated | recompute pairwise: 155/42/115 | VERIFIED |

### 2.6 §4.3 Mechanism, wrong-spec

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.3 | "C2a +0.35, C2c v2 +0.22, C2c v1 -0.25 on 13 globals" | as stated | recompute: +0.3538 / +0.2161 / -0.2469 | VERIFIED |
| §4.3 | "0.60 points gap" (correct vs adversarial) | 0.60 | 0.35 - (-0.25) = 0.60 | VERIFIED |
| §4.3 | "78.6% spec-tag citation, 50.0% wrong-spec" | 78.6/50.0 | `compute_spec_activation.py`: 276/351=78.6%, 156/312=50.0% | VERIFIED |
| §4.3 | "28.6-point gap" | 28.6 | 78.6 - 50.0 | VERIFIED |
| §4.3 | "587 wrong-spec responses... 60.6% / 36.5% / 2.0% / 0.9%" | 587 / 60.6 / 36.5 / 2.0 / 0.9 | `wrong_spec_detection_analysis.md`: 587, 356/214/12/5 = 60.6/36.5/2.0/0.9 | VERIFIED |
| §4.3 | "Anonymized by design (§3.3), so the 60.6% is a lower bound" | claim | `wrong_spec_detection_analysis.md` says: "Specs are NAMED, not anonymized." Source-doc methodological caveat contradicts paper's framing. The 60.6% number is right but its anonymization framing is wrong. | INCONSISTENT |
| §4.3 | Three example deltas A/B/C: -2.00 / -0.20 / -3.60 | as stated | doc with verbatim text confirms | VERIFIED |
| §4.3 | "Ebers Q7: C5 1.20, C4a 3.60 (paper §4.1 Example A)" | 1.20/3.60 | per-question recompute would confirm; paper claims match analysis docs | CONSISTENT |
| §4.3 | "narrow-rule 28.8 → 1.4 → 0.0" + "broader 41.2 → 7.9 → 0.4" | as stated | hedging_analysis.json | VERIFIED |
| §4.3 | "146/507, 7/507, 0/507, 209/507, 40/507, 2/507" | 6 counts | hedging_analysis.json: starts_refusal C5=146/507, C2a=7/507, C4a=0/507; refusal_ge_1 C5=209/507, C2a=40/507, C4a=2/507 | VERIFIED |

### 2.7 §4.4 Memory-system composition

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.4.1 | Controlled config Δ_spec full 14: Mem0 +0.12, Letta +0.20, Zep +0.19, Sup -0.05, BL +0.08 | 5 numbers | `memory_systems_5judge_primary.md`: +0.121/+0.198/+0.186/-0.054/+0.078 | VERIFIED |
| §4.4.1 | Controlled subjects-improved 10/14, 12/14, 13/14, 5/14, 9/14 | 5 fractions | doc | VERIFIED |
| §4.4.1 | Controlled low-baseline Δ_spec: +0.10/+0.17/+0.17/-0.01/+0.08 | 5 | doc: +0.101/+0.165/+0.166/-0.010/+0.083 | VERIFIED |
| §4.4.1 | Low-baseline subjects improved: 6/9, 8/9, 9/9, 5/9, 6/9 | 5 fractions | doc | VERIFIED |
| §4.4.1 | "Zep controlled p = 0.0004, Letta controlled p = 0.0017" | both | `stats_update.md`: zep W=2.0 p=0.0004, letta W=6.0 p=0.0017 | VERIFIED |
| §4.4.1 | Native config Δ_spec: Mem0 +0.33, Letta -0.02, Zep +0.33, Sup -0.01 | 4 | doc: +0.332/-0.023/+0.327/-0.0125 (paid-tier rerun) | VERIFIED |
| §4.4.1 | Native low-baseline: Mem0 +0.32, Letta -0.04, Zep +0.30, Sup -0.03 | 4 | doc: +0.320/-0.036/+0.303/-0.0268 (paid-tier rerun) | VERIFIED |
| §4.4.1 | Native subjects improved: 10/14, 5/14, 13/14, 6/14 | 4 | doc | VERIFIED |
| §4.4.1 | "Zep native p = 0.0015, Mem0 native p = 0.0088" | both | doc | VERIFIED |
| §4.4.1 | "Supermemory native W = 48.0, p = 0.8077 on n = 14" | W=48.0 / p=0.8077 / n=14 | `supermemory_7judge_aggregate.md`: W=48.0 p=0.8077 (paid-tier 14-subject) | VERIFIED |
| §4.4.1 | Mem0 W=15.0 p=0.0166 not stated as significant at α=0.05 | claim | p=0.0166 < 0.05; paper text "not significant at α = 0.05" is a misstatement; Mem0 IS significant at α=0.05. | INCONSISTENT |
| §4.4.1 | Mem0 native +0.33 / Zep native +0.33 in narrative | +0.33 / +0.33 | doc 0.332/0.327 | VERIFIED |
| §4.4 (Supermemory) | "516 paired questions; 89/516 (17.2%) with \|Δ\|≥1.0" | 516/89/17.2 | `_sm_paired_5judge.json`: n_questions_total=516, mixture |Δ|≥1.0 = 89 (17.2%) | VERIFIED |
| §4.4 | "37 (7.2%) helps, 52 (10.1%) hurts; +1.45 / -1.41" | as stated | doc: 37/52, mean swings 1.4541/-1.4064 | VERIFIED |
| §4.4 | "Ebers helps 19/39, hurts 10/39; aggregate +0.21" | 19/10/+0.21 | `supermemory_c1_vs_c3_paired_analysis.md` | VERIFIED |
| §4.4 | "Keckley helps 10/39, hurts 17/39; aggregate -0.26" | 10/17/-0.26 | doc | VERIFIED |
| §4.4 (per-question examples) | Ebers Q3 +1.83, Sunity Devee Q35 +2.00, Fukuzawa Q26 +2.20, Yung Wing Q5 -2.40, Zitkala-Sa Q18 -2.00, Fukuzawa Q16 +1.60 | 6 deltas | doc and `_sm_paired_5judge.json` top-20-helps / per-question | VERIFIED |
| §4.4.2 | Per-subject paired-delta table (8 rows: Mem0/Letta/Zep/BL × Yung Wing/Hamerton/Seacole/Keckley) | 8 rows | `mem0_letta_zep_c1_vs_c3_analysis.md`, `baselayer_c1_vs_c3_paired_analysis.md` | CONSISTENT |
| §4.4.3 | Cross-system Keckley Q21 table (5 rows) with Δ -2.33/-2.33/-0.50/-0.50/+1.00 | 5 deltas | analysis docs | CONSISTENT |
| §4.4.2 | "0.34-0.47 dedup ratio, 3-5 unique facts" Letta archival | as stated | mem0_letta_zep_c1_vs_c3_analysis.md | CONSISTENT |

### 2.8 §4.5 Letta stateful

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.5 | "3.10 vs 2.96, +0.14" Hamerton | 3.10/2.96/+0.14 | `5judge_primary_results.json`: 3.103/2.964/+0.138 | VERIFIED |
| §4.5 | "2.76 vs 1.72, +1.05" Ebers | 2.76/1.72/+1.05 | doc: 2.760/1.715/+1.045 | VERIFIED |
| §4.5 | "2.42 vs 1.88, +0.54" Babur | 2.42/1.88/+0.54 | doc: 2.415/1.880/+0.535 | VERIFIED |
| §4.5 | "Δ +0.27 / +1.21 / +0.38" full-stack rerun | as stated | `RESULTS.md`: +0.272/+1.205/+0.380 | VERIFIED |
| §4.5 | Letta block sizes 22,472 / 68,413 / 335,349 chars | 3 numbers | `letta_stateful_matched_rerun.md` | CONSISTENT |
| §4.5 | "25.4% verbatim sentence duplication on Babur" | 25.4% | letta_stateful_matched_rerun.md | CONSISTENT |
| §4.5 | "Base Layer compose 34,000-40,000 chars" | 34-40K | spec files; consistent with composed brief sizes | CONSISTENT |
| §4.5 | "335,349 chars ≈ 84,000 tokens" | 84K | char/4 = ~84K | VERIFIED |

### 2.9 §4.6 Robustness

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §4.6.1 | Tier 2 Δ: Ebers Sonnet +1.48, Ebers Gemini Pro +1.07, Yung Wing Sonnet +1.91, Yung Wing Gemini Pro +1.27, Zitkala-Sa Sonnet +1.40, Zitkala-Sa Gemini Pro -0.55 | 6 deltas | DATA_REFERENCE §10. **Cannot reproduce from `tier2_recompute_s114.json`:** recompute (5j primary) gives Ebers Sonnet Δ_C2a=+1.19, Δ_C4a=+0.97; Ebers Gemini Pro Δ_C2a=+0.37, Δ_C4a=+0.20; Yung Wing Sonnet Δ_C2a=+1.33, Δ_C4a=+1.68; Yung Wing Gemini Pro Δ_C2a=+0.22, Δ_C4a=+0.55; Zitkala-Sa Sonnet Δ_C2a=+1.11, Δ_C4a=+1.30; Zitkala-Sa Gemini Pro Δ_C2a=-0.13, Δ_C4a=-0.05. None of paper's six numbers reconcile with either Δ_C2a or Δ_C4a from the recompute. The s114 audit (`docs/reviews/s114_full_data_audit.md`) flagged this as HIGH priority unresolved. | INCONSISTENT |
| §4.6.1 | "5 of 6 cells reproduce specification direction" | 5/6 | The directional pattern (5 positive, 1 negative for Zitkala-Sa × Gemini Pro) DOES match recompute directions on Δ_C4a (5j-primary). Magnitudes differ but direction is preserved. | CONSISTENT |
| §4.6.1 | C5 baselines listed: Ebers 1.02, Yung Wing 1.88, Zitkala-Sa 2.34 | 3 baselines | These are main-study Haiku C5 baselines. The Tier 2 actual C5s (Sonnet × Ebers = 2.12 etc.) differ. Listing the Haiku C5 in the Tier 2 result table is conceptually inconsistent but the values are correct as Haiku C5. | CONSISTENT (with caveat) |
| §4.6.2 | "C2a 5j +0.35, 7j +0.45, widens by +0.10" | +0.35/+0.45/+0.10 | recompute 5j +0.354, 7j +0.454; widening +0.10 | VERIFIED |
| §4.6.2 | "C2c v2 5j +0.22, 7j +0.22" | +0.22/+0.22 | recompute 5j +0.216, 7j +0.217 | VERIFIED |
| §4.6.2 | "C2c v1 5j -0.25, 7j -0.21" | -0.25/-0.21 | recompute 5j -0.247, 7j -0.213 | VERIFIED |

### 2.10 §5 Discussion / §6 Limitations / §7 Future Work

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §5.2 | Recap of -0.96 / [-1.24, -0.67] / R²=0.82 | as stated | recompute | VERIFIED |
| §5.2 | "+0.89 mean Δ_C4a low-baseline" | +0.89 | recompute | VERIFIED |
| §5.2 | "9 of 9 improve" | 9/9 | recompute | VERIFIED |
| §5.2 | "Δ +0.22 random vs +0.35 correct, gap 0.13" | as stated | recompute deltas; 0.35 - 0.22 = 0.13 | VERIFIED |
| §5.2 | "5× to 78× compression" | 5×/78× | Hamerton 25,231/spec~5K = 5×; Babur 422,772/spec~5.5K = 78× (per paper Table 4.2 ratios); paper's §3.2 gives 25,231 to 422,772 corpus range | VERIFIED |
| §5.4 | "+0.22 v2, +0.35 correct, +0.13 gap" repeated | as above | VERIFIED |
| §5.4 | Cross-system Keckley Q21 -2.33/-0.50 etc. | as stated | analysis docs | CONSISTENT |
| §6.2 | "Spearman ρ 0.86-0.93", "Krippendorff α 0.659/0.535" | as stated | as in §3.7.4 | CONSISTENT |
| §6.2 | Per-judge strictness Sonnet 1.14, Opus 1.41 | as stated | §3.7.6 | CONSISTENT |
| §6.3 | Per-rerun SDs Sunity 0.103 / Yung 0.055 / Augustine 0.130 / Pooled 0.101 | 4 numbers | `v10_pipeline_variance_analysis.md` table | VERIFIED |
| §6.3 | "17.4% / 9.3% / 22.0% / 17.1%" of cross-subject SD | 4 percentages | doc | VERIFIED |
| §6.3 | "cross-subject SD 0.589" | 0.589 | doc; computed cross-subject SD of Δ_C4a over 14 subjects | CONSISTENT |
| §6.3 | "95% CI half-width 0.285" | 0.285 | (1.245-0.675)/2 = 0.285; paper rounds to 0.29 in §6.3 | VERIFIED |
| §6.3 | "n=3 reruns per subject, sign flips on 2 of 3 reruns Augustine" | 2/3 | doc per-rerun table | VERIFIED |
| §6.3 | "all 6 low-baseline reruns produced positive Δ_C4a" | 6/6 | doc per-rerun table for sunity_devee/yung_wing | VERIFIED |
| §7.2 | "+0.15 to +0.25 points cross-tradition gap, 4 vs 10 split" | +0.15 to +0.25 / 4-10 | `era_modernity_cross_slice.md`; per-doc, suggestive 4:10 split | CONSISTENT |
| §7.6 | "75 of 81 (93%) routine" refusals | 75/81/93% | `refusal_intent_classification.md` | VERIFIED |

### 2.11 §8 Data, code, reproducibility

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| §8 | "Total study cost approximately USD 350" | $350 | Author estimate; not in any single data file but consistent with cumulative API cost reports in `EXPERIMENT_LOG.md` | UNVERIFIABLE |

### 2.12 Appendix A (Predicates)

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| A.1 | "46 constrained predicates" | 46 | `memory_system/src/baselayer/config.py` `CONSTRAINED_PREDICATES`, lines 613-639 | VERIFIED |
| A.2 | "Session 49 added 6, Session 52 added 2, Session 55 added 8" | 6/2/8 | session history | CONSISTENT |
| A.2 | "8 relationship predicates raise from 0.8% to 3-5%" | 0.8/3-5 | session history; cited from prior pipeline pilot | CONSISTENT |

### 2.13 Appendix B (Batteries)

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| B.2 | Per-subject category counts (10×15 matrix) | full table | battery_v2.json (globals) and battery.json (Hamerton, Franklin) | CONSISTENT |
| B.2 | Column totals 93/115/84/66/65/19/34/60/23/27/586 | 11 sums | sum of column = 586 | CONSISTENT (math checks within-table) |
| B.3 | "60 LITERAL_RECALL (10.2%), 403 INTERPRETIVE (68.8%), 123 REFUSAL (21.0%)" | 3 counts | `question_category_audit.md` per-subject table; sum reproduces | CONSISTENT |
| B.3 | Per-subject (LITERAL/INTERP/REFUSAL) for each subject | full table | doc | CONSISTENT |
| B.4 | "LITERAL Δ_spec +0.792, INTERP +0.397, REFUSAL +0.489" | 3 means | `question_category_audit.md` | CONSISTENT |
| B.5 | "Hamerton LITERAL +1.93, INTERP +2.02, REFUSAL +1.71" | 3 deltas | doc | CONSISTENT |
| B.6 | "Δ_spec range -0.31 to +1.85" | 2 endpoints | The actual Δ_C2a min in §4.1 is -0.31 (Zitkala-Sa or Equiano = -0.31). Max is Hamerton +1.37. Doc says "range -0.31 to +1.85" but that doesn't match §4.1 max of +1.37 (or +1.51 for Δ_C4a). Discrepancy in source `question_category_audit.md` quoted value. | INCONSISTENT |
| B.6 | "r LITERAL = +0.646, INTERP = -0.582, REFUSAL = +0.321" | 3 correlations | doc; paper §4.1 also cites +0.646 / -0.582 | CONSISTENT |

### 2.14 Appendix C / D / E / F

| Section | Quote | Number | Source | Status |
|---|---|---:|---|---|
| C (model identifiers) | claude-haiku-4-5-20251001, gpt-5.4, etc. | strings | `scripts/run_*.py` | VERIFIED |
| D.1 | Per-subject 5-judge primary table | 14 rows | identical to §4.1 table | VERIFIED |
| D.2 | Anchor-crossing per-subject (Sunity 74.4%, Hamerton 69.2%, etc.) | 9 rows | `compute_anchor_crossing.py` per-subject output | VERIFIED |
| D.3.1 | "192 abstention responses (12.0% of 1,599)" | 192/1599/12.0% | `audit_low_end_inflation.py` | CONSISTENT |
| D.3.2 | Score-band distribution 159/15/12/2/2/2 (82.8%/7.8%/6.3%/1.0%/1.0%/1.0%) | 6 counts | doc | CONSISTENT |
| D.3.3 | Per-judge means on abstentions: 1.14/1.17/1.29/1.34/1.41 | 5 numbers | doc | CONSISTENT |
| D.3.4 | r length×score by condition: all 1599 r=0.26, C5=0.604, C2a=0.14, C4=0.01, C4a=-0.01, C2c=0.500 | 6 corr | doc | CONSISTENT |
| D.4 | Per-subject by per-judge by per-condition score matrix (14 × 5 × 9 = 630 cells) | full matrix | `_emit_full_judge_matrix.py` against per-judge JSONs | CONSISTENT (sampled spot-checks against recompute_5judge_primary all match) |
| E | All cited prior-work numbers (LongMemEval 68-85%, Twin-2K 71.72%, etc.) | as stated | external papers | CITED-FROM-EXTERNAL |
| F | Letta full case study (3.10/2.76/2.42 vs 2.96/1.72/1.88, full-stack +0.27/+1.21/+0.38) | as stated | `5judge_primary_results.json`, `RESULTS.md` | VERIFIED |
| F | Babur block 335,349 chars ≈ 84K tokens at ~333K char ceiling | as stated | letta_stateful_matched_rerun.md | CONSISTENT |
| F | Referential-density 540 vs 46, 58 vs 19 | 4 numbers | letta_stateful_deep_read.md (cited indirectly) | CONSISTENT |

---

## 3. Inconsistencies report

### INC-1. §4.6.1 Tier 2 deltas don't reconcile

- **Section / paragraph:** §4.6.1, Table at line ~1299
- **Exact quote:** Six rows in the Tier 2 result table with Δ values +1.48, +1.07, +1.91, +1.27, +1.40, -0.55 across (Ebers/Yung Wing/Zitkala-Sa) × (Sonnet/Gemini Pro)
- **Source where cross-checked:** `docs/research/tier2_recompute_s114.json`, `scripts/recompute_tier2_from_raw.py`. The recompute uses primary data at `results/_tier2/global_<subject>/tier2_<sonnet|gemini_pro>_judgments_<judge>.json`.
- **Conflict:** Recompute on the 5-judge primary panel gives Δ_C2a = +1.19 / +0.37 / +1.33 / +0.22 / +1.11 / -0.13 and Δ_C4a = +0.97 / +0.20 / +1.68 / +0.55 / +1.30 / -0.05. None of the paper's six numbers match either column. The s114 audit (`docs/reviews/s114_full_data_audit.md` line 12) explicitly flagged this as a HIGH priority unresolved discrepancy.
- **Suggested fix:** Determine the original aggregation that produced the published numbers (possibly per-judge mean across questions then mean against a different baseline; or 6-judge with Gemini Flash; or against question-set-specific per-question C5). Either replace with the verifiable recompute numbers or document the alternate computation in DATA_REFERENCE.md §10. The 5/6 directional claim is robust either way.

### INC-2. §4.2 Table 4.2 mean row mixes 8-subject and 9-subject aggregations

- **Section / paragraph:** §4.2, Table 4.2 at line 800
- **Exact quote:** "Mean | | ~23× | 1.52 | 2.23 | 2.35 | 2.45 | 2.45 | 2.50 | +0.22"
- **Source where cross-checked:** Recompute over the 9 low-baseline subjects in `recompute_5judge_primary.py` and `_compute_per_question_v2.py`
- **Conflict:** The C5 mean printed (1.52) is the 8-subject mean (Babur excluded; 12.17/8 = 1.521). Other column means (C2a, C4, C8, C4a) are 9-subject means including Babur. C9 mean printed (2.50) does not match either the 9-subject mean (n/a, no Babur) or the 8-subject mean (sum of paper's printed C9 column for 8 rows = 20.74 / 8 = 2.59).
- **Suggested fix:** Recompute with a uniform 9-subject mean (with Babur excluded only on the C9 column where data is missing): C5 1.55, C2a 2.23, C4 2.35, C8 2.45, C4a 2.44, C9 2.59. Or adopt 8-subject means everywhere (Babur excluded throughout for an apples-to-apples row): C5 1.52, C2a 2.27, C4 2.39, C8 2.50, C4a 2.49, C9 2.59.

### INC-3. §4.2 efficiency claim uses two different C5 means in adjacent paragraphs

- **Section / paragraph:** §4.2 line 781 ("first ~7K tokens... +0.68") vs line 807 ("spec lift +0.71, corpus lift +0.93")
- **Exact quote:** "+0.68 points of lift above baseline on average" (line 781); "spec lift +0.71" (line 807)
- **Source:** Same data; +0.68 = 2.23 - 1.55 (using 9-subject C5), +0.71 = 2.23 - 1.52 (using 8-subject C5)
- **Conflict:** Two C5 means in the same section. The numbers can't both be right against the same data.
- **Suggested fix:** Pick one C5 mean (1.52 if Babur excluded; 1.55 if 9-subject). Recompute both lifts under the chosen convention. If 1.55 is chosen, +0.68 / +0.90; if 1.52, +0.71 / +0.93.

### INC-4. §3.7.4 attributes Spearman ρ = 0.86-0.93 to "21 judge pairs" but it is actually 5-judge / 10 pairs

- **Section / paragraph:** §3.7.4 line 549 ("Pairwise Spearman ρ = 0.86 to 0.93 across all 21 judge pairs")
- **Source:** `docs/research/stats_update.md` §5: "5-judge primary (10 pairs): range [0.858, 0.932]"; "7-judge full panel (21 pairs): range [0.294, 0.932]"
- **Conflict:** The 0.86-0.93 range is the 5-judge / 10-pair range. The 7-judge / 21-pair range is much wider [0.29, 0.93], driven down by Gemini Pro's partial coverage and absolute-bias.
- **Suggested fix:** Either restate as "across 10 pairs in the 5-judge primary panel" or report the full 7-judge range alongside the 5-judge range.

### INC-5. §4.3 wrong-spec detection: paper says lower bound, source doc says specs were named (which makes it an upper bound)

- **Section / paragraph:** §4.3 / §1.3 claim that "Specifications are anonymized by design (§3.3), so the 60.6% is a lower bound on content-grounded detection"
- **Source where cross-checked:** `docs/research/wrong_spec_detection_analysis.md` lines 26-28 explicitly say: "**Specs are named, not anonymized.** ... A portion of 'explicit detection' is therefore triggered by trivial name-mismatch rather than deeper behavioral-mismatch recognition."
- **Conflict:** The 60.6% number is right; the bound interpretation flips. If specs were named (as the audit doc states), 60.6% is an UPPER bound on content-grounded detection (some unknown fraction is trivial name-mismatch detection inflating the rate). Paper claims the opposite: 60.6% is a LOWER bound on content-grounded detection, implying specs were anonymized so the model couldn't have detected via name cues. Either §3.3's anonymization claim is right and the audit doc's "specs are named" caveat needs revision, or vice versa. Both cannot be correct.
- **Suggested fix:** Verify which serving convention was actually used in the wrong-spec C2c condition. If specs were served anonymized, update the analysis doc to remove the "specs are named" caveat and re-confirm the 60.6%. If specs were served named, reframe the paper claim: 60.6% is the explicit-mismatch flag rate with name cues available, of which content-grounded detection is an unknown subset; or rerun the analysis on a uniformly anonymized variant.

### INC-6. §4.4.1 "Mem0 not significant at α = 0.05"

- **Section / paragraph:** §4.4.1 line 1050: "Mem0, Supermemory, and Base Layer substrate are not significant at α = 0.05 on the 9-subject low-baseline slice."
- **Source:** `stats_update.md` §1: Mem0 controlled (full N=14): W=15.0, **p=0.0166** (significant at α=0.05). On the low-baseline n=9 slice, Mem0 controlled is W=7.0, p=0.0742 (not significant).
- **Conflict:** Claim phrasing is correct only on low-baseline subset. Paper's §4.4.1 line 1050 phrasing implies the n=9 slice tests, but the full-N test was significant at p=0.0166.
- **Suggested fix:** The phrasing is technically correct (n=9 is "underpowered"), but should be read carefully. No actual numeric error.

### INC-7. §4.2 mean C4a = 2.45 (off by 0.01 from recompute 2.44)

- **Section / paragraph:** §4.2 line 800 mean row
- **Exact quote:** "C4a... | 2.45"
- **Source:** Recompute 9-subject C4a mean = 2.4393 → standard rounding gives **2.44**, not 2.45.
- **Suggested fix:** Trivial round-up correction (2.44 vs 2.45). Practically negligible for any conclusion but technically inconsistent with the printed per-subject values.

### INC-8. §4.2 mean C9 = 2.50 (off by 0.09 from recompute 2.59)

- **Section / paragraph:** §4.2 line 800 mean row
- **Exact quote:** "C9... | 2.50"
- **Source:** Sum of the 8 row C9 values printed in the same Table 4.2 (3.09 + 2.46 + 2.16 + 2.78 + 2.53 + 2.73 + 2.49 + 2.50) = 20.74; 20.74 / 8 = 2.5925 ≈ **2.59**, not 2.50. The paper's mean row for C9 contradicts its own per-subject values printed in the same table.
- **Suggested fix:** Replace 2.50 with 2.59 in Table 4.2 mean row.

### INC-9. Appendix B.6 cites Δ_spec range "-0.31 to +1.85" but §4.1 max is +1.37 (Δ_C2a) or +1.51 (Δ_C4a)

- **Section / paragraph:** Appendix B.6 line 1939: "Δ_spec range: −0.31 to +1.85"
- **Source:** `question_category_audit.md` line 63 produces this range from a per-question category-weighted Δ_spec aggregation (Hamerton: weighted mean of (LITERAL +1.93 × 10/39, INTERP +2.02 × 10/39, REFUSAL +1.71 × 19/39) = +1.846). The §4.1 gradient table reports the per-subject mean-score difference (C2a − C5) where Hamerton = +1.37. These are arithmetically different aggregations and produce different range endpoints.
- **Conflict:** B.6 cites a "Δ_spec range" without making clear it uses a different (category-weighted, per-question-mean) aggregation than the §4.1 gradient table. A reader cross-referencing the two will see a +1.85 max in B.6 vs +1.37 max in §4.1.
- **Suggested fix:** Add a one-line note in B.6 stating that the Δ_spec computation here is per-question (averaged within category, then mean across categories weighted by category count), distinct from the per-subject mean-score Δ in §4.1. Or recompute B.6's correlation using the §4.1 per-subject Δ_C2a/Δ_C4a so the ranges match.

---

## 4. Unchecked / out-of-scope

- **§8 cost claim "approximately USD 350".** This is an aggregate dollar figure that no single file in the repo records canonically. Multiple session experiment logs cite per-task costs (e.g., `p0_2_supermemory_paid_tier_rerun.md` $2.53; per-subject pipeline ~$1) but no totals file. Marked UNVERIFIABLE in the strict mechanical sense; consistent with order-of-magnitude expectations.
- **§3.7.2 calibration table values (Haiku 5.00/4.75/3.80/5.00, etc.).** Numbers cited but raw `results/judge_calibration/` was not opened in this verification pass; values match v9 calibration table and DATA_REFERENCE. Marked CONSISTENT.
- **§2.5, §2.4 prior-work citations.** All numbers from external papers (Zheng et al. 80% MT-Bench, Jain et al. +45% Gemini sycophancy, Toubia 71.72%, etc.) are CITED-FROM-EXTERNAL, not in scope.
- **Per-subject baselayer/mem0/letta/zep C1/C3 cell scores.** Not all 14 × 5 × 2 = 140 cells were re-derived from raw judgment files; the aggregate Δ_spec by system was verified, and `compute_memory_systems_5judge.py` produces the per-subject details consistent with `memory_systems_5judge_primary.md`. Per-subject C1/C3 cells in §4.4.2 Table 4.6 (8 rows: Mem0 Yung Wing/Keckley, Letta Hamerton/Keckley, Zep Seacole/Keckley, BL Yung Wing/Keckley) match `mem0_letta_zep_c1_vs_c3_analysis.md` and `baselayer_c1_vs_c3_paired_analysis.md` to within the reported rounding. Marked CONSISTENT.
- **Token estimates ("~7K", "~33K", "~549K") in §4.2 compression table.** These are word-to-token approximations (×1.3 conventional ratio); the exact token count per spec is not stored centrally but the order-of-magnitude is consistent with composed brief sizes. Marked CONSISTENT.

---

## 5. Re-derivation log (for reproducibility)

All Python re-derivations performed via `scripts/_v10_verification/`:

- `verify_paper.py`: main per-subject 5-judge primary aggregate, gradient regression, Wilcoxon, low-baseline mean Δ_C4a, all-14 anchor-crossings, compression-table re-derivation
- `verify_wrongspec_v2.py`: v1 vs v2 wrong-spec deltas (5j and 7j) on 13 globals
- `per_question_all14.py`: paper §4.2.1 second table all-14 win rates
- `pairwise_compare.py`: paper §4.2.1 pairwise C8-vs-C2a and C9-vs-C4a tables
- `check_hedging.py`: `hedging_analysis.json` narrow-rule and broad-rule rates

Existing in-repo scripts re-run as part of this pass:
- `scripts/recompute_5judge_primary.py` (gradient, Wilcoxon)
- `scripts/_compute_per_question_v2.py` (low-baseline win rates)
- `scripts/compute_anchor_crossing.py` (anchor crossings)
- `scripts/compute_spec_activation.py` (78.6%/50.0% spec-tag citation)
- `scripts/recompute_tier2_from_raw.py` (Tier 2 recompute, flagged INC-1)

Everything ran on a single Python 3.12 environment with `scipy`, `numpy`, `statistics`. Bootstrap and permutation p-values use seeds documented in their scripts.

---

*End of report.*
