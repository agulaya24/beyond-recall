# `results/global_equiano/` — Results for Olaudah Equiano

**What's in this folder:** Every AI response and every judge score for Olaudah Equiano (West African / British, 1745-1797, C5 baseline 2.93). Source text: *The Interesting Narrative of the Life of Olaudah Equiano*.

Equiano is at the high-baseline end of the gradient. He sits in the cohort where the spec effect may be flat or slightly negative because the model already knows him well.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full list.

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled `<system>_*` and native `<system>_fullpipeline_*`.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus conditions.
- Per-judge files use short names.

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/equiano/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Equiano and Zitkala-Sa are the two high-baseline subjects that show negative spec deltas across all 14. This is consistent with the gradient mechanism (high-baseline subjects do not benefit from structured context).
- Supermemory native ingestion succeeded for Equiano; `C1_supermemory_fp` is populated.
