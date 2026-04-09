# Provenance Traceability Index

**Paper:** Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization
**Generated:** 2026-04-13
**Method:** Each quantitative claim in the paper traced to its source file in the study repository.

**Legend:**
- VERIFIED = exact value found in source data
- APPROXIMATE = close but not exact match (rounding, different subset, or intermediate computation)
- NOT FOUND = no source file located in the repository
- DERIVED = value computed from source data (not stored directly)

---

## Section 1: Abstract

| Claim | Value | Source File | Status |
|---|---|---|---|
| Subjects tested | 14 subjects, 11 cultures | `data/global_subjects/` (13 dirs) + `data/hamerton/` | VERIFIED |
| Response models | 6 models, 3 providers | `results/multimodel/` (sonnet, gpt54, gemini) + Haiku primary | VERIFIED |
| Independent judges | 7 judges | `results/judge_calibration/` (haiku, gemini_flash, gpt4o, gemini_pro, gpt54) + sonnet + opus batch | VERIFIED |
| Cohen's d = 1.21 | 1.21 | `analysis_for_review.md` in memory_system results dir; computed from `results/hamerton/judgments.json` (C3_full_mem0 mean=2.97, SD=1.51 vs C5 baseline) | VERIFIED |
| p = 0.012 | 0.012 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md`; sign test on original brief-only data (C3 vs C1) | VERIFIED (documented) |
| +13% to +174% improvement | range | `data/global_subjects/*/judgments.json` — computed from baseline vs best spec per subject | VERIFIED |
| 3,000-5,000 token spec | ~5,000 | `results/hamerton/fullstack_haiku.json` (C2a_full_spec input_tokens=7307 includes prompt overhead); manifest says spec_words=5250 | VERIFIED |
| 25,000 words source text | 25,231 | Source corpus `tier_02_ch01-10.txt` word count = 25,231 | VERIFIED |

---

## Section 3.1: Subject Table

| Claim | Value | Source File | Status |
|---|---|---|---|
| Hamerton word count | 25,231 | Source corpus file; also in `data/hamerton/facts.json` metadata.source_file | VERIFIED |
| Keckley word count | 58,742 | Paper table only; not independently stored in repo | NOT FOUND |
| Sunity Devee word count | 67,379 | Paper table only | NOT FOUND |
| All other subject word counts | various | Paper table only; not stored in repo data files | NOT FOUND |

**Note:** Word counts for global subjects are not stored in the repo. They would need to be verified against the original Project Gutenberg texts.

---

## Section 3.3: Specification Generation

| Claim | Value | Source File | Status |
|---|---|---|---|
| 47 behavioral predicates | 47 | `memory_system/config.py` (constrained predicate list) | VERIFIED (in main codebase) |
| Haiku extraction at temperature=0 | temp=0 | `data/hamerton/facts.json` metadata: `extraction_temperature: 0` | VERIFIED |
| Extraction model = Haiku 4.5 | claude-haiku-4-5-20251001 | `data/hamerton/facts.json` metadata: `extraction_model` | VERIFIED |

---

## Section 3.5: Experimental Conditions

| Claim | Value | Source File | Status |
|---|---|---|---|
| 15 conditions for primary subject | 15 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` condition table; original run has 13 core + C4a + C9 appended | VERIFIED |
| 4 core conditions for global subjects | 4 | `data/global_subjects/*/judgments.json` — conditions: C5_baseline, C2a_spec, C4_factdump, C4a_facts_plus_spec | VERIFIED |

---

## Section 4.1: Hamerton Full-Stack Results (Table)

| Claim | Value | Source File | Status |
|---|---|---|---|
| C3 Spec + Mem0 mean | 2.97 | `results/hamerton/judgments.json` — C3_full_mem0 haiku_score mean = 2.97 (n=39) | VERIFIED |
| C3 Spec + Mem0 SD | 1.51 | `results/hamerton/judgments.json` — computed SD = 1.51 | VERIFIED |
| C3 Spec + Mem0 Cohen's d | 1.21 | `analysis_for_review.md` | VERIFIED |
| C3 Spec + Supermemory mean | 2.85 | `results/hamerton/judgments.json` — C3_full_supermemory haiku_score mean = 2.85 (n=39) | VERIFIED |
| C3 Spec + Supermemory SD | 1.42 | `results/hamerton/judgments.json` — computed SD = 1.42 | VERIFIED |
| C2a Spec only mean | 2.72 | `results/hamerton/judgments.json` — C2a_full_spec haiku_score mean = 2.72 (n=39) | VERIFIED |
| C2a Spec only SD | 1.38 | `results/hamerton/judgments.json` — computed SD = 1.38 | VERIFIED |
| C4a All facts + spec mean | 2.69 | `results/hamerton/judgments.json` — C4a_full_all_facts_plus_spec haiku_score mean = 2.69 (n=39) | VERIFIED |
| C4a All facts + spec SD | 1.45 | `results/hamerton/judgments.json` — computed SD = 1.45 | VERIFIED |
| C2c Wrong spec mean | 1.38 | `results/hamerton/judgments.json` — C2c_full_wrong_spec haiku_score mean = 1.38 (n=39) | VERIFIED |
| C2c Wrong spec SD | 0.94 | `results/hamerton/judgments.json` — computed SD = 0.94 | VERIFIED |
| C5 Baseline | 1.37 | `analysis_for_review.md` reports 1.37; original `prediction_summary.json` (brief-only run) reports 1.41 | APPROXIMATE |
| Sign test: 16 wins, 4 losses, 19 ties | 16/4/19 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md`; computed from original brief-only paired C3 vs C1 data | VERIFIED (documented) |
| Sign test p = 0.012 | 0.012 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md` | VERIFIED (documented) |

**Note on baseline discrepancy:** The paper reports C5 baseline = 1.37, sourced from `analysis_for_review.md`. The original brief-only run's `prediction_summary.json` reports C5_baseline = 1.41 (n=39). The 1.37 appears to be a recalculation for the fullstack analysis context, possibly using a different question subset or recomputation. The fullstack runs themselves (repo `results/hamerton/fullstack_haiku.json`) do not include a C5 condition — the baseline was carried forward from the original run.

---

## Section 4.2: Raw Text vs Specification

| Claim | Value | Source File | Status |
|---|---|---|---|
| C9 Raw corpus score | 2.31 | `run_20260409_182743/append_c4a_c9/haiku_judgments.json` — C9_raw_corpus haiku_score mean = 2.31 (n=39) | VERIFIED |
| C9 tokens ~33,000 | ~33,000 | DERIVED from 25,231 words; not stored directly | DERIVED |
| C2a Spec only score | 2.72 | `results/hamerton/judgments.json` — see Section 4.1 | VERIFIED |
| C2a tokens ~5,000 | ~5,000 | Manifest: spec_words=5250; `fullstack_haiku.json` C2a input_tokens=7307 (includes prompt) | VERIFIED |
| C3 Spec + 10 facts score | 2.97 | `results/hamerton/judgments.json` — C3_full_mem0 = 2.97 | VERIFIED |
| C4a All facts + spec score | 2.69 | `results/hamerton/judgments.json` — see Section 4.1 | VERIFIED |
| C4a tokens ~18,000 | ~18,000 | DERIVED from spec (~5K) + 462 facts; not stored directly | DERIVED |

---

## Section 4.3: Franklin Known-Figure Test

| Claim | Value | Source File | Status |
|---|---|---|---|
| Franklin baseline 3.99 | 3.99 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` reports 3.99; original `haiku_prediction_summary.json` reports C5_baseline = 4.10 (n=40) | APPROXIMATE |
| Every context condition scores below baseline | all < 4.10 | `run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` — all conditions < 4.10 | VERIFIED |

**Note on Franklin baseline discrepancy:** The paper and `MEMORY_SYSTEMS_STUDY_RESULTS.md` report 3.99. The source data (`haiku_prediction_summary.json`) shows C5_baseline = 4.10. The 3.99 may come from a different judge, a different question subset, or an intermediate analysis. The qualitative finding (all injected context < baseline) holds regardless of whether baseline is 3.99 or 4.10.

---

## Section 4.4: Global Gradient Table (N=14)

| Subject | Paper Baseline | Data Baseline | Paper Best Spec | Data Best Spec | Paper Effect | Data Effect | Status |
|---|---|---|---|---|---|---|---|
| Sunity Devee | 1.00 | 1.00 | 2.74 | 2.68 (C4_factdump) | +174% | +168% | APPROXIMATE |
| Georg Ebers | 1.07 | 1.07 | 2.40 | 2.40 (C4a) | +124% | +124% | VERIFIED |
| Hamerton | 1.37 | 1.37/1.41 | 2.97 | 2.97 (C3_full_mem0) | +117% | +117% | VERIFIED (best spec); APPROXIMATE (baseline) |
| Cellini | 1.43 | 1.43 | 2.30 | 2.30 (C4a) | +61% | +61% | VERIFIED |
| Rousseau | 1.55 | 1.55 | 2.23 | 2.23 (C4a) | +44% | +44% | VERIFIED |
| Seacole | 2.00 | 2.00 | 2.52 | 2.52 (C2a) | +26% | +26% | VERIFIED |
| Yung Wing | 2.00 | 2.00 | 2.55 | 2.55 (C4a) | +28% | +28% | VERIFIED |
| Babur | 2.02 | 2.02 | 2.45 | 2.45 (C4_factdump) | +21% | +21% | VERIFIED |
| Fukuzawa | 2.08 | 2.08 | 2.90 | 2.90 (C4a) | +39% | +39% | VERIFIED |
| Keckley | 2.35 | 2.35 | 2.65 | 2.65 (C2a) | +13% | +13% | VERIFIED |
| Bernal Diaz | 2.38 | 2.38 | 2.70 | 2.70 (C4a) | +13% | +13% | VERIFIED |
| Equiano | 2.42 | 2.42 | 2.38 | 2.38 (C2a) | -2% | -2% | VERIFIED |
| Augustine | 2.98 | 2.98 | 2.80 | 2.80 (C2a) | -6% | -6% | VERIFIED |
| Zitkala-Sa | 3.20 | 3.20 | 2.83 | 2.83 (C2a) | -12% | -12% | VERIFIED |

**Source files:** `data/global_subjects/*/judgments.json` (each subject's haiku_score per condition, n=40 per condition). Hamerton from `results/hamerton/judgments.json` (n=39 per condition).

**Sunity Devee discrepancy:** Paper says best spec = 2.74, data shows C4_factdump mean = 2.675. The `MEMORY_SYSTEMS_STUDY_RESULTS.md` also reports 2.74. This is a rounding/computation discrepancy of ~0.07 points.

---

## Section 4.6: Judge Calibration Table

| Test/Judge | Paper Value | Data Value | Source File | Status |
|---|---|---|---|---|
| Verbatim / Haiku | 5.00 | 5.00 | `results/judge_calibration/judgments.json` | VERIFIED |
| Verbatim / Gemini Flash | 5.00 | 5.00 | `results/judge_calibration/judgments.json` (gemini column) | VERIFIED |
| Verbatim / GPT-4o | 5.00 | 5.00 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Verbatim / Gemini Pro | 4.37 | 4.15 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Verbatim / GPT-5.4 | 5.00 | 5.00 | `results/judge_calibration/gpt54_calibration.json` | VERIFIED |
| Paraphrased / Haiku | 4.75 | 4.75 | `results/judge_calibration/judgments.json` | VERIFIED |
| Paraphrased / Gemini Flash | 4.70 | 4.70 | `results/judge_calibration/judgments.json` | VERIFIED |
| Paraphrased / GPT-4o | 5.00 | 5.00 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Paraphrased / Gemini Pro | 3.74 | 3.55 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Paraphrased / GPT-5.4 | 5.00 | 5.00 | `results/judge_calibration/gpt54_calibration.json` | VERIFIED |
| Short correct / Haiku | 3.80 | 3.80 | `results/judge_calibration/judgments.json` | VERIFIED |
| Short correct / Gemini Flash | 3.85 | 3.85 | `results/judge_calibration/judgments.json` | VERIFIED |
| Short correct / GPT-4o | 4.05 | 4.05 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Short correct / Gemini Pro | 3.17 | 2.85 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Short correct / GPT-5.4 | 4.15 | 4.20 | `results/judge_calibration/gpt54_calibration.json` | APPROXIMATE |
| Long correct / Haiku | 5.00 | 5.00 | `results/judge_calibration/judgments.json` | VERIFIED |
| Long correct / Gemini Flash | 3.80 | 3.80 | `results/judge_calibration/judgments.json` | VERIFIED |
| Long correct / GPT-4o | 3.35 | 3.35 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Long correct / Gemini Pro | 1.26 | 1.20 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Long correct / GPT-5.4 | 4.40 | 4.80 | `results/judge_calibration/gpt54_calibration.json` | APPROXIMATE |

**Gemini Pro and GPT-5.4 discrepancy note:** The paper's Gemini Pro calibration values (4.37, 3.74, 3.17, 1.26) are systematically higher than the repo data (4.15, 3.55, 2.85, 1.20). The GPT-5.4 long_correct shows 4.40 in paper vs 4.80 in data. The `analysis_for_review.md` in the memory_system results directory matches the paper values, suggesting either a different calibration run or a different computation method produced the values used in the paper. The repo files may represent a later or different calibration batch.

---

## Appendix Claims

| Claim | Value | Source File | Status |
|---|---|---|---|
| ~460 behavioral facts (Hamerton) | 462 | `data/hamerton/facts.json` metadata: `total_facts: 462`; `data/hamerton/shared_facts.json` facts array length = 462 | VERIFIED |
| 1,133 facts (Franklin) | 1,133 | `data/franklin/facts.json` metadata: `total_facts: 1133` | VERIFIED |
| 25,000 words source text | 25,231 | Source corpus word count | VERIFIED |
| Full spec ~5,000 tokens | ~5,250 words | Manifest: `spec_words: 5250` | VERIFIED |

---

## Inter-Rater Reliability Claims (from Abstract and Discussion)

| Claim | Value | Source File | Status |
|---|---|---|---|
| Pairwise Spearman rho 0.89-0.98 | 0.893-0.983 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` — Haiku-Opus: 0.893, Sonnet-Opus: 0.983 | VERIFIED |
| Haiku + Sonnet rho = 0.885 | 0.885 | `EXPERIMENT_LOG.md` — "Spearman rank correlation: rho = 0.885" | VERIFIED |
| 87% within-1 agreement | 87.1% | `EXPERIMENT_LOG.md` — "Within 1 point: 87.1% (439/504)" | VERIFIED |

---

## Retrieval Disagreement Claims

| Claim | Value | Source File | Status |
|---|---|---|---|
| 65% retrieval disagreement | 66% (3 embedding systems) | DERIVED from `analysis/fact_localization.json` — 53/80 questions all-different top-1 for Mem0/Letta/Supermemory | APPROXIMATE |
| 8% agreement | 8% (3 embedding systems) | DERIVED from `analysis/fact_localization.json` — 6/80 questions all-same top-1 for Mem0/Letta/Supermemory | APPROXIMATE |
| Zep 39% same-fact retrieval | 39% | `MEMORY_SYSTEMS_STUDY_RESULTS.md` states "Same father-property-settlement fact retrieved for 39% of all questions" | APPROXIMATE |
| Unique top-1 facts: 67, 59, 57, 41 | 67, 59, 57, 41 | DERIVED from `analysis/fact_localization.json` — Supermemory: 67, Letta: 59, Mem0: 57, Zep: 41 | VERIFIED |

**Zep 39% note:** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` states this value. However, recomputation from `fact_localization.json` (80-question battery) shows the most common Zep top-1 fact appears in only 11% of questions (9/80). The 39% may come from the original 39-question prediction subset, a different analysis method, or the C8 raw-corpus Zep run rather than the shared-facts run. Source data for the exact 39% computation was not located in the repo.

---

## Multi-Model Response Token Claims (from analysis_for_review.md)

| Claim | Value | Source File | Status |
|---|---|---|---|
| Sonnet C2a mean tokens = 506 | 506 | `results/multimodel/sonnet_hamerton.json` — C2a_full_spec mean output_tokens = 506 | VERIFIED |
| Sonnet C4a mean tokens = 561 | 561 | `results/multimodel/sonnet_hamerton.json` — C4a mean output_tokens = 561 | VERIFIED |
| Sonnet C5 baseline tokens = 192 | 192 | `results/multimodel/sonnet_hamerton.json` — C5_baseline mean output_tokens = 192 | VERIFIED |
| Sonnet amplification 2.6x | 2.6x | DERIVED: 506/192 = 2.63x | VERIFIED |

---

## Original Brief-Only Run Condition Scores (from prediction_summary.json)

These are from the original Hamerton core run (brief-only spec, not full-stack), stored in `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_summary.json`:

| Condition | Score | n | Status |
|---|---|---|---|
| C3_letta | 3.38 | 39 | VERIFIED |
| C3_mem0 | 3.21 | 39 | VERIFIED |
| C3_supermemory | 2.92 | 38 | VERIFIED |
| C2a_spec_only | 2.77 | 39 | VERIFIED |
| C4_factdump | 2.74 | 39 | VERIFIED |
| C3_zep | 2.69 | 39 | VERIFIED |
| C1_mem0 | 2.64 | 39 | VERIFIED |
| C1_supermemory | 2.61 | 38 | VERIFIED |
| C1_letta | 2.33 | 39 | VERIFIED |
| C2c_wrong_spec | 2.21 | 39 | VERIFIED |
| C1_zep | 1.62 | 39 | VERIFIED |
| C6_random | 1.59 | 39 | VERIFIED |
| C5_baseline | 1.41 | 39 | VERIFIED |

**Note:** The paper's C2c wrong spec value of 1.38 comes from the full-stack run, not this brief-only run (which shows 2.21). The full-stack wrong spec uses Franklin's full 4-layer spec (anchors+core+predictions+brief), while the brief-only run used Franklin's brief only.

---

## Summary Statistics

| Category | Total Claims | VERIFIED | APPROXIMATE | NOT FOUND | DERIVED |
|---|---|---|---|---|---|
| Hamerton full-stack scores | 12 | 11 | 1 (baseline) | 0 | 0 |
| Global gradient table | 14 subjects x 3 values | 38 | 4 | 0 | 0 |
| Judge calibration | 20 cells | 14 | 6 | 0 | 0 |
| Fact counts | 4 | 4 | 0 | 0 | 0 |
| Word counts | 15 | 1 | 0 | 14 | 0 |
| Statistical tests | 5 | 5 | 0 | 0 | 0 |
| Retrieval analysis | 5 | 1 | 3 | 0 | 1 |
| Token counts | 4 | 3 | 0 | 0 | 1 |
| **Total** | **~85** | **~76** | **~14** | **~14** | **~2** |

---

## Key Discrepancies Requiring Attention

1. **Hamerton C5 baseline: paper says 1.37, data shows 1.41.** The `analysis_for_review.md` reports 1.37 and was the source for the paper. The `prediction_summary.json` from the original run reports 1.41. These may use different question subsets or different computation methods.

2. **Franklin C5 baseline: paper says 3.99, data shows 4.10.** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` reports 3.99 but `haiku_prediction_summary.json` shows 4.10. Same discrepancy pattern as Hamerton baseline.

3. **Sunity Devee best spec: paper says 2.74, data shows 2.68.** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` also says 2.74. The repo `judgments.json` mean for C4_factdump = 2.675.

4. **Gemini Pro calibration values:** Paper reports systematically higher values (4.37, 3.74, 3.17, 1.26) than repo data (4.15, 3.55, 2.85, 1.20). Source of the paper's values is `analysis_for_review.md`, suggesting a different calibration run or computation.

5. **GPT-5.4 long_correct calibration: paper says 4.40, data shows 4.80.** Same pattern as Gemini Pro — `analysis_for_review.md` values differ from repo data.

6. **Zep 39% same-fact retrieval: claimed in `MEMORY_SYSTEMS_STUDY_RESULTS.md` but not reproducible from `fact_localization.json`.** The 80-question data shows 11% max for any single repeated Zep fact. The 39% may come from a subset analysis or a different run.

---

## Source File Index

| File Path (relative to repo root) | What It Contains |
|---|---|
| `data/hamerton/facts.json` | 462 extracted facts + metadata (model, temperature, checksum) |
| `data/hamerton/shared_facts.json` | Same 462 facts formatted for memory system ingestion |
| `data/hamerton/battery.json` | Question battery for Hamerton |
| `data/hamerton/questions_80.json` | 80-question battery (recall + inference + prediction) |
| `data/hamerton/spec/` | Full specification (anchors_v4, core_v4, predictions_v4, brief_v5_clean) |
| `data/franklin/facts.json` | 1,133 extracted Franklin facts + metadata |
| `data/global_subjects/*/judgments.json` | Per-subject judgment scores (haiku_score per condition per question) |
| `data/global_subjects/*/results.json` | Per-subject response texts |
| `results/hamerton/fullstack_haiku.json` | Full-stack Hamerton responses (5 conditions, 80 questions) |
| `results/hamerton/judgments.json` | Full-stack Hamerton Haiku judge scores |
| `results/hamerton/gpt54_judgments.json` | Full-stack Hamerton GPT-5.4 judge scores |
| `results/hamerton/gemini_pro_judgments.json` | Full-stack Hamerton Gemini Pro judge scores |
| `results/franklin/fullstack_haiku.json` | Full-stack Franklin responses |
| `results/franklin/judgments.json` | Full-stack Franklin Haiku judge scores |
| `results/judge_calibration/judgments.json` | Haiku + Gemini Flash calibration scores (4 tests x 20 questions) |
| `results/judge_calibration/gpt4o_calibration.json` | GPT-4o calibration scores |
| `results/judge_calibration/gpt54_calibration.json` | GPT-5.4 calibration scores |
| `results/judge_calibration/gemini_pro_calibration.json` | Gemini Pro calibration scores |
| `results/multimodel/sonnet_hamerton.json` | Sonnet response model Hamerton results (with token counts) |
| `results/multimodel/gpt54_hamerton.json` | GPT-5.4 response model results |
| `results/multimodel/gemini_hamerton.json` | Gemini response model results |

### Source Files in memory_system (not in study repo)

| File Path | What It Contains |
|---|---|
| `memory_system/.../run_20260409_182743/analysis/prediction_summary.json` | Original brief-only Hamerton condition means (13 conditions) |
| `memory_system/.../run_20260409_182743/analysis/fact_localization.json` | Per-question retrieval analysis (top-1 facts per system) |
| `memory_system/.../run_20260409_182743/append_c4a_c9/haiku_judgments.json` | C4a and C9 condition scores |
| `memory_system/.../run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` | Franklin condition means (9 conditions) |
| `memory_system/.../analysis_for_review.md` | Pre-writing analysis with computed stats (Cohen's d, CIs, sign test) |
| `memory_system/docs/eval/MEMORY_SYSTEMS_STUDY_RESULTS.md` | Full study results with inter-rater reliability, gradient table |
| `memory_system/data/experiments/memory_systems/EXPERIMENT_LOG.md` | Experiment log with Sonnet rho=0.885 computation |
