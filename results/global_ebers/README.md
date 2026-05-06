# `results/global_ebers/` — Results for Georg Ebers

**What's in this folder:** Every AI response and every judge score for Georg Ebers (German, 1837-1898, C5 baseline 1.04). Source text: *Story of My Life*.

Ebers has one of the lowest baselines in the study. The model knows almost nothing about him from pretraining, making him a clean test case for the spec effect.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full list.

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled `<system>_*` and native `<system>_fullpipeline_*`.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus conditions.
- Per-judge files use short names (`haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`, `gemini_flash`, `gemini_pro`).

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: `data/global_subjects/ebers/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Ebers is one of three subjects used in the Letta stateful-agent test (paper §4.7). Related outputs live in `docs/research/_letta_blocks/` and `docs/research/_letta_rerun/`. S114 corrected numbers: Letta stateful 3.00 vs Base Layer C2a 2.25 (Δ +0.75).
- Ebers is also one of three subjects in the Tier 2 circularity control (`results/_tier2/global_ebers/`).
- Data integrity check: 0 of 40 held-out passages appear in training. Clean split.
