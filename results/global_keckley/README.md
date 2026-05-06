# `results/global_keckley/` — Results for Elizabeth Keckley

**What's in this folder:** Every AI response and every judge score for Elizabeth Keckley (Black American, 1818-1907, C5 baseline 1.91). Source text: *Behind the Scenes; or, Thirty Years a Slave, and Four Years in the White House*.

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

Inputs: `data/global_subjects/keckley/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Parse-failure entries are handled by the primary recompute; do not drop them manually.
