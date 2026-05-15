# Example A & C: Fresh re-judge under the verbatim rubric

**Date:** 2026-05-08
**Script:** `scripts/example_a_c_fresh_rejudge_20260508.py`
**Rubric:** verbatim original-prompt rubric from `scripts/judge_hamerton_5judge.py` lines 57-68
**Temperature:** 0; primary 5-judge panel; identical held-out + response inputs as cached run

## Question

Two cells were flagged as worked examples in paper §4.1. We ask: under a fresh execution at temperature 0, with the same rubric prompt and the same response text already in the repo, do the 5 primary judges reproduce the cached panel scores, or does the score drift?

Cells:

| Cell | Subject | qid | Condition | Cached panel (h/s/o/g4o/g54) | Cached mean |
|---|---|---:|---|---|---:|
| fukuzawa_q35_C4 | global_fukuzawa | 35 | C4_factdump | 1/1/1/1/1 | 1.00 |
| seacole_q2_C4 | global_seacole | 2 | C4_factdump | 5/2/3/3/1 | 2.80 |

## Per-cell comparison: cached vs fresh

### fukuzawa_q35_C4

**Held-out (verbatim ground truth):** "For this kind of war, if they wanted figureheads in their ranks, they could as well hire farmers from the provinces. My students were too precious"

**Response (first 300 chars):** # Fukuzawa's Reasoning for Keeping Students from War

Based on the facts provided, Fukuzawa's reasoning would likely be **practical concern** rather than moral principle.

## Evidence for Practical Concern:

1. **His demonstrated pragmatism**: Throughout his life, Fukuzawa showed a utilitarian appro...

| Judge | Cached score | Fresh score | Delta (fresh - cached) |
|---|---:|---:|---:|
| haiku | 1 | 5 | +4 |
| sonnet | 1 | 4 | +3 |
| opus | 1 | 4 | +3 |
| gpt4o | 1 | 4 | +3 |
| gpt54 | 1 | 4 | +3 |

- Cached mean: 1.00 (SD=0.00)
- Fresh mean:  4.20 (SD=0.40)
- Mean drift (fresh - cached): +3.20

### seacole_q2_C4

**Held-out (verbatim ground truth):** "Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour"

**Response (first 300 chars):** # Mary Seacole's Response to a Delirious Soldier

Based on the extensive facts about Mary's character, **yes, she would absolutely comfort such a soldier**, and she would do so without hesitation or self-consciousness.

## Evidence from Her Character

**Her compassionate nature:**
- Mary "is pleased...

| Judge | Cached score | Fresh score | Delta (fresh - cached) |
|---|---:|---:|---:|
| haiku | 5 | 5 | +0 |
| sonnet | 2 | 3 | +1 |
| opus | 3 | 4 | +1 |
| gpt4o | 3 | 4 | +1 |
| gpt54 | 1 | 4 | +3 |

- Cached mean: 2.80 (SD=1.33)
- Fresh mean:  4.00 (SD=0.63)
- Mean drift (fresh - cached): +1.20

## Verdict

Reproduction criterion: |fresh mean - cached mean| <= 0.5 -> reproduces; otherwise drifts.

| Cell | Cached mean | Fresh mean | Mean drift | Within +/-0.5? | Verdict |
|---|---:|---:|---:|:---:|---|
| fukuzawa_q35_C4 | 1.00 | 4.20 | +3.20 | no | DRIFTS |
| seacole_q2_C4 | 2.80 | 4.00 | +1.20 | no | DRIFTS |

## Implications for the worked examples in §4.1

**Fukuzawa Q35 C4_factdump.** Cached panel was 1.00 unanimous. Aarik flagged the unanimous 1.00 as inconsistent with the verbatim rubric: a substantively engaged correct-direction response (the model identifies "practical concern rather than moral principle... students were more valuable to Japan's future as scholars than as soldiers") should score 3 or 4 under the rubric, not 1. Fresh execution under the same rubric yields 4.20 (drift +3.20). 
Result: fresh judges drift away from the cached unanimous 1 by +3.20, suggesting the cached score is not stable under the rubric and the worked example may be a stochastic artifact rather than a structural rubric pattern.

**Seacole Q2 C4_factdump.** Cached panel was 2.80 with wide variance (5/2/3/3/1). Fresh execution yields 4.00 (drift +1.20, fresh SD 0.63 vs cached SD 1.33). 
Result: fresh judges drift outside the +/-0.5 band, suggesting the cached panel is not stable and the wide-variance worked example reflects run-to-run noise rather than a structural rubric pattern.

## Files

- Per-(cell, judge) raw responses: `results/_example_a_c_fresh_rejudge_20260508/<cell_id>/<judge>.json`
- Verbatim prompts saved per cell: `results/_example_a_c_fresh_rejudge_20260508/<cell_id>/_prompt.txt`
- This synthesis: `docs/research/example_a_c_fresh_rejudge_20260508.md`
- Reproducibility script: `scripts/example_a_c_fresh_rejudge_20260508.py`
