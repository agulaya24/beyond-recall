# `data/global_subjects/babur/` — Input data for Babur

**What's in this folder:** The source facts, question battery, and behavioral-specification layers for Babur (Central Asian / Muslim, 1483-1530, C5 baseline 1.98). Source text: *Baburnama*.

Low-baseline subject. Used in the Letta stateful-agent test (paper §4.7).

## Contents

Standard per-subject schema. See `../README.md` for full file list and meanings. In brief: `facts.json`, `battery.json`, `spec.md`, `spec_production.md`, `anchors_v4.md`, `core_v4.md`, `predictions_v4.md`, `brief_v5.md`, plus subject-level `results.json` and `judgments.json`.

## Caveats worth knowing

- Babur's final Letta memory block reached 335,349 characters with HTTP 400 rejections starting at ~332,585 characters. This is the scaling-ceiling datapoint in paper §4.7.
- 1 of 40 held-out passages contains a 52-character fragment that also appears in training. Corpus-internal repetition, not test-set leakage.
- Babur's C9 (raw corpus + spec) failed because the corpus exceeded the response model's context window. Single disclosed exclusion in C8/C9 results.
