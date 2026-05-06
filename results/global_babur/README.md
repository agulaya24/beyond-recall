# `results/global_babur/` — Results for Babur

**What's in this folder:** Every AI response and every judge score for Babur (Central Asian / Muslim, 1483-1530, C5 baseline 1.98). Source text: *Baburnama*.

Babur sits at the low-baseline end of the gradient. The model knows relatively little about him from pretraining, so he is part of the population where the spec effect is expected to be strongest.

## Contents

Standard per-subject schema. See `../README.md` and `docs/FILE_NAMING.md` for the full file list. In short:

- `results.json` / `results_v2.json`, `battery*.json`, `heldout.txt`, `spec.md`, `facts.json`.
- Per memory system (Mem0, Letta, Supermemory, Zep): controlled config `<system>_*` and native config `<system>_fullpipeline_*`.
- `baselayer_*`: Base Layer substrate retrieval.
- `c8_c9_*`: Raw corpus and raw corpus + spec conditions.
- Per-judge files use the short names `haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`, `gemini_flash`, `gemini_pro`.

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`. Condition codes and judge short names follow the repo-wide convention.

## Where these files come from / go to

Inputs: `data/global_subjects/babur/`. Outputs: `results/RESULTS_S113.json` and the 5-judge primary recompute.

## Caveats worth knowing

- Supermemory native ingestion failed for Babur; `C1_supermemory_fp` responses are empty. Ingestion issue, not a judge issue.
- Babur's C9 (raw corpus + spec) run failed because the corpus exceeded the response model's context window. This is the one disclosed exclusion in the C8/C9 results.
- Babur is one of three subjects used in the Letta stateful-agent test (paper §4.7). Related outputs live in `docs/research/_letta_blocks/` and `docs/research/_letta_rerun/`.
- Babur has corpus-internal repetition: 1 of 40 held-out passages contains a 52-character fragment that also appears in training. This is not test-set leakage; it is a natural artifact of the source text.
