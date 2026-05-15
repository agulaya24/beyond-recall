# `_per_judge_ablation_20260508/` — Per-judge rubric ablation

**What's in this folder:** A per-judge ablation produced 2026-05-08. For a small set
of (subject, condition, question) cells, every primary-panel judge rejudges the same
response twice: once under the `original` rubric and once under the `paper` rubric.
The two files for a judge differ only in which rubric was used, so they isolate the
effect of the rubric change judge by judge.

The leading underscore means this is not part of the main per-subject results tree;
it is a targeted ablation.

## Layout

Flat directory, about 50 files. Each cell selected for the ablation contributes ten
files: five primary-panel judges (`haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`) times
two rubric variants (`original`, `paper`).

## File naming

```
<subject>__<paper_cond>__q<qid>__<judge>__<rubric>.json
```

- `<subject>` — subject directory name (e.g. `global_babur`, `global_equiano`,
  `global_yung_wing`).
- `<paper_cond>` — the paper condition label (`C4a`, `C5_baseline`, `C2a`, `C8`).
- `<qid>` — question id within that subject's battery.
- `<judge>` — one of the five primary-panel judges.
- `<rubric>` — `original` or `paper`. The `__original` and `__paper` pair for the
  same (subject, condition, qid, judge) is the unit of comparison.

Example pair:
`global_babur__C4a__q2__haiku__original.json` and
`global_babur__C4a__q2__haiku__paper.json`.

## File contents

Each JSON file is a single judgment record. Fields seen:

- `subject`, `paper_cond`, `raw_cond_label`, `qid`, `judge` — cell identity.
- `rubric` — `original` or `paper`, matching the filename suffix.
- `score` / `raw` — the 1-5 score under that rubric, with the raw model output
  before parsing.
- `parse_failure` — whether the judge output failed to parse.
- `response_type`, `response_text` — the response being judged.
- `held_out`, `question_text` — the held-out passage and the question prompt.
- `prior_delta` — the cell's delta from the prior run, kept for context.
- `timestamp` — when the judgment was run.

For the schema of the underlying conditions and judge files, see `results/README.md`
and `docs/FILE_NAMING.md`.
