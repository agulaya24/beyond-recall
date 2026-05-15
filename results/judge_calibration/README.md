# `results/judge_calibration/` — Judge calibration diagnostics

**What's in this folder:** Diagnostic tests that score each judge against verbatim, paraphrased, partial, and length-padded responses with known correct scores. Used to decide which judges belong in the primary panel and which belong in the sensitivity panel.

## Why calibration matters for this study

The study uses LLM judges to score how well a response matches a held-out ground-truth passage. If a judge is miscalibrated (for example, refuses to give a perfect 5 even for a verbatim match), it distorts aggregate numbers. The calibration tests ran four kinds of responses past each judge:

- Verbatim match (should score 5)
- Paraphrase (should score high)
- Short response (tests whether judges penalize length unfairly)
- Long / padded response (tests whether judges inflate for length)

Gemini Pro failed the verbatim-match test (4.15 where every other calibrated judge scored 5.00) and penalized padded-correct responses severely (5.00 on short correct dropping to 1.20 on long correct). Gemini Flash passes verbatim cleanly but shows consistent length sensitivity (5.00 verbatim dropping to 3.80 on long correct). On actual study responses, both Gemini judges show a +1-point magnitude inflation relative to the five primary judges. That combination is why the primary panel is 5-judge (non-Gemini) and the sensitivity panel is 7-judge.

## All seven judges are calibrated

All 7 judges in the panel have diagnostic data in this folder. Five (Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) were tested before the main-study response-scoring run on 2026-04-09. Sonnet 4.6 and Opus 4.6 were tested on the same diagnostic inputs via Anthropic's Batch API on 2026-04-12 (3 days after the main-study run); the batch results were retrieved and saved to this folder on 2026-05-06. Both Sonnet and Opus pass the diagnostic cleanly: verbatim 5.00, paraphrased 5.00, short_correct 4.20-4.35, long_correct 5.00.

## Contents

- `results.json`: Calibration responses (the verbatim / paraphrased / short / long answers fed to each judge).
- `judgments.json`: Haiku and Gemini Flash scores on the calibration set (key names `haiku`, `gemini`).
- `gpt4o_calibration.json`, `gpt54_calibration.json`, `gemini_pro_calibration.json`, `sonnet_calibration.json`, `opus_calibration.json`: Per-judge calibration outputs in `[{"test": "...", "qid": ..., "<judge>_score": ...}]` format.
- `_seven_judge_summary.json`: Combined 7-judge summary aggregator output.
- `README.md`: this file.

## How naming works here

Plain descriptive names. No per-subject layout because this folder is judge-side, not subject-side.

## Where these files come from / go to

Inputs: a small fixed calibration set built from a 20-question subset of Hamerton's behavioral-prediction battery (verbatim ground truth + paraphrased + first-sentence + ground-truth-with-padding variants). Outputs feed paper §3.3.3 (calibration) and Appendix C.5 (judge panel composition with per-judge calibration-status flags).

## Caveats worth knowing

- Calibration is performed on a small diagnostic set, not the full study battery. The purpose is identifying judge pathologies, not producing study-level scores.
- Sonnet and Opus calibration data was retrieved post-main-study run (Batch API submitted 2026-04-12, retrieved 2026-05-06). The pre-locked panel composition decision was made before the main run on cross-Anthropic-coverage grounds; the post-hoc diagnostic confirms the composition rather than driving it. See paper §3.3.3 lede for the timing disclosure.
- Run scripts: `scripts/run_judge_evaluation.py` (original 5-judge calibration; produced `gpt4o_calibration.json`, `gpt54_calibration.json`, `gemini_pro_calibration.json`, and the Haiku + Gemini Flash entries in `judgments.json`) and `scripts/run_calibration_sonnet_opus.py` (Batch API retrieval that produced `sonnet_calibration.json` and `opus_calibration.json`).
