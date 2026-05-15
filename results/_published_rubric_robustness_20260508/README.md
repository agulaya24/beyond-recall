# `_published_rubric_robustness_20260508/` — Rubric-robustness rejudgments

**What's in this folder:** Example-cell rejudgments produced 2026-05-08 to test how
sensitive a cell's score is to the exact rubric wording. For a selected set of
(subject, condition, question) cells, the response was rejudged under the paper's
published rubric and the result is stored alongside the score that cell originally
received.

The leading underscore means this is not part of the main per-subject results tree;
it is a targeted robustness check.

## Layout

One subdirectory per subject. Ten subjects are covered:
`global_augustine`, `global_babur`, `global_cellini`, `global_ebers`,
`global_equiano`, `global_rousseau`, `global_sunity_devee`, `global_yung_wing`,
`global_zitkala_sa`, and `hamerton`. This is a sampled robustness probe, not the
full 14-subject study, so only the subjects whose example cells were selected for
rechecking appear here. `global_zitkala_sa/` is present but empty.

About 350 files total. Each covered cell is rejudged by all five primary-panel
judges (`haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`), so a subject with three
example cells contributes 15 files.

## File naming

Inside each subject folder:

```
<paper_cond>_q<qid>_<judge>.json
```

- `<paper_cond>` — the paper condition label (`C2a`, `C4a`, `C5_baseline`, `C8`, `C9`).
- `<qid>` — the question id within that subject's battery.
- `<judge>` — one of the five primary-panel judges.

Example: `global_augustine/C2a_q24_haiku.json`.

## File contents

Each JSON file is a single rejudgment record. Fields seen:

- `subject`, `paper_cond`, `raw_cond_label`, `qid`, `judge` — cell identity.
- `paper_rubric_score` / `paper_rubric_raw` — the 1-5 score under the published
  paper rubric (the rejudgment), with the raw model output before parsing.
- `parse_failure` — whether the judge output failed to parse.
- `original_score` — the score this cell received in the original judging run, kept
  for side-by-side comparison.
- `timestamp` — when the rejudgment was run. Some records also carry a `seed`.

For the schema of the underlying conditions and judge files, see `results/README.md`
and `docs/FILE_NAMING.md`.
