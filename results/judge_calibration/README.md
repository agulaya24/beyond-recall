# `results/judge_calibration/` — Judge calibration diagnostics

**What's in this folder:** Diagnostic tests that score each judge against known-correct, known-wrong, short, and long responses. Used to decide which judges belong in the primary panel and which belong in the sensitivity panel.

## Why calibration matters for this study

The study uses LLM judges to score how well a response matches a held-out ground-truth passage. If a judge is miscalibrated (for example, refuses to give a perfect 5 even for a verbatim match), it distorts aggregate numbers. The calibration tests ran four kinds of responses past each judge:

- Verbatim match (should score 5)
- Paraphrase (should score high)
- Short response (tests whether judges penalize length unfairly)
- Long / padded response (tests whether judges inflate for length)

Gemini Pro failed the verbatim-match test (4.15 where every other calibrated judge scored 5.00) and penalized padded-correct responses severely (5.00 to 1.20). That failure is why the primary panel is 5-judge (non-Gemini) and the sensitivity panel is 7-judge.

## Contents

- `results.json`: Calibration responses (the verbatim / paraphrase / short / long answers fed to each judge).
- `judgments.json`: Each judge's scores on the calibration set.
- `gpt4o_calibration.json`, `gpt54_calibration.json`, `gemini_pro_calibration.json`: Per-judge calibration outputs. (Other judges' calibration is captured inside the merged `judgments.json`.)

## How naming works here

Plain descriptive names. No per-subject layout because this folder is judge-side, not subject-side.

## Where these files come from / go to

Inputs: a small fixed calibration set. Outputs feed paper §3.7.2 (primary panel decision) and `STUDY_MEMORY.md` (the "Gemini Pro fails verbatim-match calibration" constraint).

## Caveats worth knowing

- Calibration is performed on a small diagnostic set, not the full battery. The purpose is identifying judge pathologies, not producing study-level scores.
- Sonnet and Opus entered the panel on judge-agreement grounds, not calibration. Their addition is documented in paper §3.7.2.
