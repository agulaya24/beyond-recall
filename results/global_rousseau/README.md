# `results/global_rousseau/` — Results for Jean-Jacques Rousseau

**What's in this folder:** Every AI response and every judge score for Jean-Jacques Rousseau (French, 1712-1778, C5 baseline 2.65). Source text: *Confessions*.

Higher-baseline subject. The model knows Rousseau well; the expected spec effect is modest.

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

Inputs: `data/global_subjects/rousseau/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Supermemory native ingestion failed for Rousseau; `C1_supermemory_fp` responses are empty.
- Parse-failure entries are handled by the primary recompute.
