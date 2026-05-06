# `results/global_bernal_diaz/` — Results for Bernal Diaz del Castillo

**What's in this folder:** Every AI response and every judge score for Bernal Diaz del Castillo (Spanish / Latin American, 1492-1584, C5 baseline 1.85). Source text: *True History of the Conquest of New Spain*.

Low-baseline subject. Part of the population where the spec effect is expected to be strongest.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full file list. In short:

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled `<system>_*` and native `<system>_fullpipeline_*`.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus conditions.
- Per-judge files use short names (`haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`, `gemini_flash`, `gemini_pro`).

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/bernal_diaz/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Supermemory native ingestion failed for Bernal Diaz; `C1_supermemory_fp` responses are empty.
- If judge cells show `parse_failure: true`, do not drop them silently; the 5-judge primary recompute handles them.
