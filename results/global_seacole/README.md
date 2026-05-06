# `results/global_seacole/` — Results for Mary Seacole

**What's in this folder:** Every AI response and every judge score for Mary Seacole (Caribbean / British, 1805-1881, C5 baseline 1.85). Source text: *Wonderful Adventures of Mrs. Seacole in Many Lands*.

Low-baseline subject. Part of the population where the spec effect is expected to be strongest.

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

Inputs: `data/global_subjects/seacole/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Parse-failure entries are handled by the primary recompute; do not drop them manually.
