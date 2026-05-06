# `results/global_cellini/` — Results for Benvenuto Cellini

**What's in this folder:** Every AI response and every judge score for Benvenuto Cellini (Italian, 1500-1571, C5 baseline 2.56). Source text: *Vita*.

Cellini is in the mid-to-higher-baseline end of the gradient. The spec effect is expected to be smaller than for low-baseline subjects.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full list.

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled `<system>_*` and native `<system>_fullpipeline_*`.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus and raw corpus + spec conditions.
- Per-judge files use short names.

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/cellini/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Supermemory native ingestion failed for Cellini; `C1_supermemory_fp` responses are empty.
- If judge cells show `parse_failure: true`, the primary recompute filters them correctly.
