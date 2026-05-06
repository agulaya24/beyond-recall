# `results/global_zitkala_sa/` — Results for Zitkala-Sa

**What's in this folder:** Every AI response and every judge score for Zitkala-Sa (Native American, 1876-1938, C5 baseline 2.60). Source text: *American Indian Stories*.

Higher-baseline subject. The model knows Zitkala-Sa well; she is one of two subjects (the other is Equiano) where the spec effect is flat or slightly negative.

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

Inputs: `data/global_subjects/zitkala_sa/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Zitkala-Sa is one of three subjects in the Tier 2 circularity control (`results/_tier2/global_zitkala_sa/`). The GPT-5.4-generated battery run tests whether the Haiku-authored-battery pattern holds at higher baseline too.
- Zitkala-Sa and Equiano are the two main-gradient subjects that show negative spec delta. Consistent with the gradient mechanism.
