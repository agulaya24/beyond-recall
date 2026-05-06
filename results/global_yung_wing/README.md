# `results/global_yung_wing/` — Results for Yung Wing

**What's in this folder:** Every AI response and every judge score for Yung Wing (Chinese, 1828-1912, C5 baseline 1.96). Source text: *My Life in China and America*.

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

Inputs: `data/global_subjects/yung_wing/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Yung Wing is one of three subjects used in the Tier 2 circularity control (`results/_tier2/global_yung_wing/`). GPT-5.4-generated batteries were run with Sonnet and Gemini Pro as response models to test whether the spec advantage persists off the Haiku-authored battery.
- Parse-failure entries are handled by the primary recompute.
