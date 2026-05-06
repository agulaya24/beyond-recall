# `results/global_sunity_devee/` — Results for Sunity Devee

**What's in this folder:** Every AI response and every judge score for Sunity Devee (Indian, 1864-1932, C5 baseline 1.03). Source text: *Autobiography of an Indian Princess*.

Lowest baseline in the study. The model knows almost nothing about her from pretraining. One of the cleanest test cases for the spec effect.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full list.

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system: controlled and native configs.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus conditions.
- Per-judge files use short names.

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/sunity_devee/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Sunity Devee's lowest-baseline status makes her the anchor of the low-baseline slice in the paper. Related analyses cite her frequently.
- Parse-failure entries are handled by the primary recompute.
