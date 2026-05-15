# Published-rubric robustness check (Option B)

**Date:** 2026-05-08
**Script:** `scripts/published_rubric_robustness_20260508.py` (seed = 42)
**Spec source:** `docs/reviews/rubric_defensibility_analysis_20260508.md` Option B
**Paper rubric source:** `docs/beyond_recall_v11_8_draft.md` §3.3, lines 380–386
**Original prompt rubric source:** `scripts/judge_hamerton_5judge.py` lines 57–68

## Executive summary

**Spearman ρ = 0.389** between the original-prompt 5-judge primary mean and the paper-rubric 5-judge primary mean across 25 stratified (subject, condition, qid) cells. Pearson r = 0.491. Mean cell-level delta = -0.344 (SD 0.968); 95% Bland–Altman limits of agreement [-2.240, +1.552]. Verdict: **EQUIVALENCE NOT EMPIRICALLY SUPPORTED. ESCALATE.**.

Spearman ρ ≤ 0.70 indicates the two rubrics produce divergent cell-level rankings. The textual equivalence claim does NOT survive empirical test; expanding the sample, redesigning the rubric prompt, or rerunning headline scores under the published rubric should be considered before launch.

## Method

**Sample design.** 25 stratified cells, 5 conditions × 5 cells each, drawn from 6 subjects spanning the gradient. Each (subject, condition, qid) cell has both (a) a response with held-out passage and (b) all 5 primary judges' original scores already computed.

| Subject | Conditions sampled |
|---|---|
| hamerton | C2a, C4a, C8, C9 |
| global_sunity_devee | C5_baseline, C9 |
| global_ebers | C2a, C4a, C5_baseline, C8, C9 |
| global_yung_wing | C2a, C4a, C5_baseline, C8, C9 |
| global_babur | C2a, C4a, C5_baseline, C8 |
| global_equiano | C2a, C4a, C5_baseline, C8, C9 |

Two patches were applied where the canonical data lacks a condition for a named subject:
- Hamerton has no `C5_baseline` row in `results.json`; substituted Sunity Devee's C5 cell.
- Babur's `c8_c9_results.json` has empty `C9_raw_corpus_plus_spec` response text; substituted Sunity Devee's C9 cell.

Each cell is re-judged by the 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4) using a prompt that quotes the published §3.3 rubric verbatim. The original judge prompt rubric (used in scoring) and the paper rubric are textually distinct: the original wires "outcome prediction" wording, the paper wires "behavioral pattern" wording.

**Cost.** 25 cells × 5 judges = 125 API calls. Below the $10 spend cap.

## Results

- Cells with complete data (5 orig + 5 new judges): **25**
- **Spearman ρ = 0.389**
- Pearson r = 0.491
- Mean delta (new − orig) = -0.344; SD 0.968
- 95% Bland–Altman limits of agreement: [-2.240, +1.552]
- Per-cell delta range: [-3.20, +1.20]; median -0.20

### Per-cell scores

| Subject | Cond | qid | Orig 5-judge mean | New 5-judge mean | Δ |
|---|---|---:|---:|---:|---:|
| global_babur | C2a | 39 | 1.80 | 2.00 | +0.20 |
| global_babur | C4a | 2 | 4.00 | 1.40 | -2.60 |
| global_babur | C5_baseline | 33 | 1.00 | 1.40 | +0.40 |
| global_babur | C8 | 36 | 1.80 | 1.40 | -0.40 |
| global_ebers | C2a | 35 | 1.00 | 1.00 | +0.00 |
| global_ebers | C4a | 6 | 1.80 | 1.20 | -0.60 |
| global_ebers | C5_baseline | 7 | 1.20 | 1.00 | -0.20 |
| global_ebers | C8 | 38 | 2.00 | 1.80 | -0.20 |
| global_ebers | C9 | 28 | 1.80 | 1.20 | -0.60 |
| global_equiano | C2a | 35 | 3.00 | 2.40 | -0.60 |
| global_equiano | C4a | 27 | 3.20 | 1.00 | -2.20 |
| global_equiano | C5_baseline | 13 | 4.40 | 1.20 | -3.20 |
| global_equiano | C8 | 15 | 4.20 | 3.80 | -0.40 |
| global_equiano | C9 | 29 | 4.00 | 4.20 | +0.20 |
| global_sunity_devee | C5_baseline | 15 | 1.00 | 1.00 | +0.00 |
| global_sunity_devee | C9 | 9 | 1.80 | 2.40 | +0.60 |
| global_yung_wing | C2a | 2 | 1.20 | 2.40 | +1.20 |
| global_yung_wing | C4a | 6 | 1.60 | 1.80 | +0.20 |
| global_yung_wing | C5_baseline | 3 | 1.00 | 1.60 | +0.60 |
| global_yung_wing | C8 | 14 | 2.80 | 2.20 | -0.60 |
| global_yung_wing | C9 | 15 | 2.00 | 1.80 | -0.20 |
| hamerton | C2a | 28 | 1.60 | 1.80 | +0.20 |
| hamerton | C4a | 22 | 1.60 | 1.60 | +0.00 |
| hamerton | C8 | 38 | 1.00 | 1.00 | +0.00 |
| hamerton | C9 | 36 | 2.00 | 1.60 | -0.40 |

### Per-judge consistency across the two rubrics

| Judge | n | Pearson r (orig vs new) | Spearman ρ | Mean Δ (new − orig) |
|---|---:|---:|---:|---:|
| haiku | 25 | 0.544 | 0.480 | -0.720 |
| sonnet | 25 | 0.424 | 0.431 | +0.000 |
| opus | 25 | 0.347 | 0.317 | +0.120 |
| gpt4o | 25 | 0.382 | 0.234 | -0.480 |
| gpt54 | 25 | 0.413 | 0.282 | -0.640 |

## Verdict

**EQUIVALENCE NOT EMPIRICALLY SUPPORTED. ESCALATE.**

Spearman ρ ≤ 0.70 indicates the two rubrics produce divergent cell-level rankings. The textual equivalence claim does NOT survive empirical test; expanding the sample, redesigning the rubric prompt, or rerunning headline scores under the published rubric should be considered before launch.

## Recommendation for §3.3 paper text

**Do not publish under the current rubric mismatch.** Spearman ρ is at or below 0.70, indicating that the published rubric and the actual scoring rubric are not interchangeable. Either rerun the headline scores under the published rubric, or restate §3.3 to publish the actual prompt rubric verbatim.

## Files

- Per-cell, per-judge raw rerun data: `results/_published_rubric_robustness_20260508/<subject>/`
- Per-cell aggregate CSV: `docs/research/published_rubric_robustness_check_20260508.csv`
- This synthesis: `docs/research/published_rubric_robustness_check_20260508.md`
- Reproducibility script: `scripts/published_rubric_robustness_20260508.py`
