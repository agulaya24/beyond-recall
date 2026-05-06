# `results/global_fukuzawa/` — Results for Fukuzawa Yukichi

**What's in this folder:** Every AI response and every judge score for Fukuzawa Yukichi (Japanese, 1835-1901, C5 baseline 1.80). Source text: *Autobiography of Fukuzawa Yukichi*.

Low-baseline subject. The model knows little about him from pretraining, so he is part of the population where the spec effect is expected to be strongest.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full list.

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled and native configs.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus conditions.
- Per-judge files use short names.

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/fukuzawa/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Judge parse failures (if any) are handled correctly by the 5-judge primary recompute. Do not silently drop `score: 0, parse_failure: true` entries.
