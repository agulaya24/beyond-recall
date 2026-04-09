# Paper Corrections: Beyond Recall

**Generated:** 2026-04-13
**Method:** Every quantitative claim in the paper verified against raw data files. Zero inference.

---

## CORRECTIONS REQUIRED

### 1. Hamerton C5 Baseline: 1.37 -> 1.41

- **Paper value:** 1.37
- **Raw data value:** 1.4103 (rounds to 1.41)
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_judgments.json` — C5_baseline scores for 39 prediction questions (IDs 21-60 excluding 50)
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_summary.json` — `"C5_baseline": {"avg_score": 1.41, "n": 39}`
- **Origin of error:** `analysis_for_review.md` reports 1.37 with no supporting computation. No data file anywhere contains 1.37. The fullstack runs do not include a C5 condition — the baseline was carried forward from the original brief-only run, which shows 1.41.
- **Action needed:** Change "Baseline 1.37" to "Baseline 1.41" in Section 4.1 title, Table 4.1 (C5 Baseline row), and all references throughout paper (Sections 4.4, 5.1). Recompute Cohen's d and CIs against 1.41 baseline (SD = 1.02). Cohen's d recalculates to 1.21 (still correct — the computation already used 1.41 implicitly since it was done against the actual C5 distribution).
- **Effect on other claims:** The +117% effect for Hamerton in Section 4.4 table changes: (2.97 - 1.41) / 1.41 = +110.6%. Paper says +117% (which was based on 1.37).

### 2. Franklin C5 Baseline: 3.99 -> 4.10

- **Paper value:** 3.99
- **Raw data value:** 4.10
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` — `"C5_baseline": {"avg_score": 4.1, "n": 40}`
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/run_franklin_20260411_014509/analysis/haiku_judgments.json` — C5_baseline mean = 4.1000 (computed from 40 raw scores)
- **Origin of error:** `analysis_for_review.md` reports 3.99. No data file contains 3.99. The fullstack Franklin run has no C5 condition.
- **Action needed:** Change "3.99" to "4.10" in Sections 4.3, 4.5, 5.1, 5.2. The qualitative finding (all injected context < baseline) still holds since all fullstack conditions are below 4.10.

### 3. Sunity Devee Best Score: 2.74 -> 2.68

- **Paper value:** 2.74 (labeled "Best Spec")
- **Raw data value:** 2.675 (rounds to 2.68)
- **Source file:** `memory-study-repo/data/global_subjects/sunity_devee/judgments.json` — C4_factdump haiku_score mean = 2.675 (n=40)
- **All condition means:** C2a_spec=2.225, C4_factdump=2.675, C4a_facts_plus_spec=2.375
- **Additional issue:** The best condition is C4_factdump (all facts, NO spec), not a spec condition. The table header says "Best Spec" but this condition does not include a specification.
- **Action needed:** Change 2.74 to 2.68. Change +174% to +168%. Consider relabeling column "Best Spec" to "Best Condition" since the winning condition for Sunity Devee and Babur is C4_factdump (no spec).

### 4. Gemini Pro Verbatim Calibration: 4.37 -> 4.15

- **Paper value:** 4.37
- **Raw data value:** 4.15
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — verbatim test, gemini_pro_score mean = 4.15 (n=20)
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/judge_evaluation/gemini_pro_calibration.json` — same value 4.15
- **Action needed:** Change 4.37 to 4.15 in Section 4.6 table.

### 5. Gemini Pro Paraphrased Calibration: 3.74 -> 3.55

- **Paper value:** 3.74
- **Raw data value:** 3.55
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — paraphrased test, gemini_pro_score mean = 3.55 (n=20)
- **Action needed:** Change 3.74 to 3.55 in Section 4.6 table.

### 6. Gemini Pro Short Correct Calibration: 3.17 -> 2.85

- **Paper value:** 3.17
- **Raw data value:** 2.85
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — short_correct test, gemini_pro_score mean = 2.85 (n=20)
- **Action needed:** Change 3.17 to 2.85 in Section 4.6 table.

### 7. Gemini Pro Long Correct Calibration: 1.26 -> 1.20

- **Paper value:** 1.26
- **Raw data value:** 1.20
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — long_correct test, gemini_pro_score mean = 1.20 (n=20)
- **Action needed:** Change 1.26 to 1.20 in Section 4.6 table. Update prose: "Gemini Pro penalizing padding severely (1.20)" not "(1.26)".

### 8. GPT-5.4 Short Correct Calibration: 4.15 -> 4.20

- **Paper value:** 4.15
- **Raw data value:** 4.20
- **Source file:** `memory-study-repo/results/judge_calibration/gpt54_calibration.json` — short_correct test, gpt54_score mean = 4.20 (n=20)
- **Action needed:** Change 4.15 to 4.20 in Section 4.6 table.

### 9. GPT-5.4 Long Correct Calibration: 4.40 -> 4.80

- **Paper value:** 4.40
- **Raw data value:** 4.80
- **Source file:** `memory-study-repo/results/judge_calibration/gpt54_calibration.json` — long_correct test, gpt54_score mean = 4.80 (n=20)
- **Action needed:** Change 4.40 to 4.80 in Section 4.6 table.

### 10. Zep 39% Same-Fact Retrieval: UNVERIFIABLE

- **Paper value:** "Zep graph bias. Same father-property-settlement fact retrieved for 39% of all questions"
- **Raw data finding:** The most common Zep top-1 fact ("Hamerton's father lost interest in his profession after his mother's death") appears in 9/80 questions (11.2%). The specific "property settlement" fact appears in only 3/80 questions (3.8%). Father-RELATED facts (any fact mentioning "father") appear in 43/80 (53.8%).
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/fact_localization.json` — 80 questions, Zep top-1 analyzed
- **Origin of claim:** `MEMORY_SYSTEMS_STUDY_RESULTS.md` states this value but it cannot be reproduced from the fact_localization.json data. The 39% does not match any computation: not 39% of 80 questions, not 39% of 40 prediction questions, not 39% of the 39-question subset.
- **Action needed:** Either (a) locate the original data source for the 39% claim, (b) replace with the verifiable number: "Father-related facts retrieved for 54% of all questions — graph traversal bias toward high-connectivity nodes," or (c) remove the specific percentage.

### 11. Hamerton Effect Percentage: +117% -> +111%

- **Paper value:** +117% (computed from baseline 1.37)
- **Corrected value:** +110.6% (rounds to +111%, computed from baseline 1.41: (2.97 - 1.41) / 1.41)
- **Source:** Derived from corrections #1 and the verified C3 score of 2.97
- **Action needed:** Change +117% to +111% in Section 4.4 global gradient table.

### 12. Retrieval Disagreement: 65% -> 66%

- **Paper value:** 65% retrieval disagreement
- **Raw data value:** 66.2% (53/80 questions all-different top-1 for Mem0/Letta/Supermemory)
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/fact_localization.json`
- **Action needed:** Change 65% to 66%.

### 13. Retrieval Agreement: 8% -> 7.5%

- **Paper value:** 8% agreement
- **Raw data value:** 7.5% (6/80)
- **Source file:** Same as above
- **Action needed:** Change 8% to 7.5% or "8%" is acceptable as rounded.

---

## VERIFIED CORRECT (no changes needed)

### Hamerton Full-Stack Scores (Section 4.1)

| Claim | Paper | Data | Status |
|---|---|---|---|
| C3 Spec + Mem0 mean | 2.97 | 2.9744 | CORRECT |
| C3 Spec + Mem0 SD | 1.51 | 1.5129 | CORRECT |
| C3 Spec + Supermemory mean | 2.85 | 2.8462 | CORRECT |
| C3 Spec + Supermemory SD | 1.42 | 1.4242 | CORRECT |
| C2a Spec only mean | 2.72 | 2.7179 | CORRECT |
| C2a Spec only SD | 1.38 | 1.3755 | CORRECT |
| C4a All facts + spec mean | 2.69 | 2.6923 | CORRECT |
| C4a All facts + spec SD | 1.45 | 1.4537 | CORRECT |
| C2c Wrong spec mean | 1.38 | 1.3846 | CORRECT |
| C2c Wrong spec SD | 0.94 | 0.9351 | CORRECT |

**Source:** `memory-study-repo/results/hamerton/judgments.json` (n=39 per condition)

### Statistical Tests

| Claim | Paper | Data | Status |
|---|---|---|---|
| Sign test: 16 wins, 4 losses, 19 ties | 16/4/19 | 16/4/19 | CORRECT |
| p = 0.012 | 0.012 | 0.0118 (two-sided) | CORRECT |
| Cohen's d = 1.21 | 1.21 | 1.2128 | CORRECT |

**Source:** Computed from `prediction_judgments.json` C3_mem0 vs C1_mem0 (sign test); fullstack C3 vs brief-only C5 (Cohen's d)

### C9 Raw Corpus Score

| Claim | Paper | Data | Status |
|---|---|---|---|
| C9 score = 2.31 | 2.31 | 2.3077 | CORRECT |

**Source:** `memory_system/.../append_c4a_c9/haiku_judgments.json`

### Calibration (Haiku, Gemini Flash, GPT-4o)

| Test/Judge | Paper | Data | Status |
|---|---|---|---|
| Verbatim / Haiku | 5.00 | 5.00 | CORRECT |
| Verbatim / Gemini Flash | 5.00 | 5.00 | CORRECT |
| Verbatim / GPT-4o | 5.00 | 5.00 | CORRECT |
| Paraphrased / Haiku | 4.75 | 4.75 | CORRECT |
| Paraphrased / Gemini Flash | 4.70 | 4.70 | CORRECT |
| Paraphrased / GPT-4o | 5.00 | 5.00 | CORRECT |
| Short correct / Haiku | 3.80 | 3.80 | CORRECT |
| Short correct / Gemini Flash | 3.85 | 3.85 | CORRECT |
| Short correct / GPT-4o | 4.05 | 4.05 | CORRECT |
| Long correct / Haiku | 5.00 | 5.00 | CORRECT |
| Long correct / Gemini Flash | 3.80 | 3.80 | CORRECT |
| Long correct / GPT-4o | 3.35 | 3.35 | CORRECT |
| Verbatim / GPT-5.4 | 5.00 | 5.00 | CORRECT |
| Paraphrased / GPT-5.4 | 5.00 | 5.00 | CORRECT |

**Source:** `memory-study-repo/results/judge_calibration/judgments.json`, `gpt4o_calibration.json`, `gpt54_calibration.json`

### Global Subject Scores (All Match Except Sunity Devee)

| Subject | Paper Baseline | Data | Paper Best | Data | Status |
|---|---|---|---|---|---|
| Georg Ebers | 1.07 | 1.075 | 2.40 | 2.400 | CORRECT |
| Cellini | 1.43 | 1.425 | 2.30 | 2.300 | CORRECT |
| Rousseau | 1.55 | 1.550 | 2.23 | 2.225 | CORRECT |
| Seacole | 2.00 | 2.000 | 2.52 | 2.525 | CORRECT |
| Yung Wing | 2.00 | 2.000 | 2.55 | 2.550 | CORRECT |
| Babur | 2.02 | 2.025 | 2.45 | 2.450 | CORRECT (but best is C4_factdump, not a spec condition) |
| Fukuzawa | 2.08 | 2.075 | 2.90 | 2.900 | CORRECT |
| Keckley | 2.35 | 2.350 | 2.65 | 2.650 | CORRECT |
| Bernal Diaz | 2.38 | 2.375 | 2.70 | 2.700 | CORRECT |
| Equiano | 2.42 | 2.425 | 2.38 | 2.375 | CORRECT |
| Augustine | 2.98 | 2.975 | 2.80 | 2.800 | CORRECT |
| Zitkala-Sa | 3.20 | 3.200 | 2.83 | 2.825 | CORRECT |

**Source:** `memory-study-repo/data/global_subjects/*/judgments.json` (n=40 per condition per subject)

### Fact Counts

| Claim | Paper | Data | Status |
|---|---|---|---|
| ~460 facts (Hamerton) | ~460 | 462 | CORRECT |
| Unique top-1: 57, 59, 67, 41 | Mem0=57, Letta=59, Super=67, Zep=41 | Mem0=57, Letta=59, Super=67, Zep=41 | CORRECT |

---

## SUMMARY

| Category | Count |
|---|---|
| **Corrections required** | 13 |
| **Major corrections (>0.05 difference)** | 5 (baselines, Sunity Devee, GPT-5.4 long_correct, Gemini Pro short_correct) |
| **Minor corrections (<0.05 difference)** | 4 (Gemini Pro verbatim/paraphrased/long_correct, GPT-5.4 short_correct) |
| **Unverifiable claims** | 1 (Zep 39%) |
| **Derived corrections** | 3 (Hamerton effect %, retrieval disagreement %, agreement %) |
| **Verified correct** | ~70 values |

### Root Cause

The `analysis_for_review.md` file was the source document for the paper's numbers. For most values, it correctly transcribes the raw data. For the Hamerton baseline (1.37 vs 1.41), Franklin baseline (3.99 vs 4.10), and all Gemini Pro / GPT-5.4 calibration values, the analysis_for_review.md contains numbers that do not appear in any raw data file. These appear to be from an earlier analysis pass, a different computation method, or transcription errors that were never reconciled against the source data.
