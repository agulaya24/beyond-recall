# `results/global_augustine/` — Results for Augustine of Hippo

**What's in this folder:** Every AI response and every judge score for Augustine of Hippo (North African / Roman, 354-430, C5 baseline 2.79). Source text: *Confessions*.

Augustine sits in the higher-baseline end of the 14-subject gradient. The model already knows him fairly well, so the expected spec lift is smaller than for low-baseline subjects like Sunity Devee or Ebers.

## Contents (~113 files)

The full per-subject schema is documented in `../README.md` and `docs/FILE_NAMING.md`. Brief summary of what you will see here:

- `results.json` / `results_v2.json`: Model responses across the core conditions. `_v2` is the paper version.
- `battery.json`, `battery_v2.json`, `battery_gpt54.json`: The question battery (primary, v2, and GPT-5.4-generated for Tier 2 circularity tests).
- `heldout.txt`: The held-out half of the source corpus. Feeds judges only, never response models.
- `judgments.json`, `judgments_v2.json`, `judgments_v2_gemini_pro2.json`, `judgments_v2_gemini_pro_key2.json`: Judge-score files at various stages.
- `spec.md`: The behavioral specification used in conditions C2a, C3, C4a, C9.
- `facts.json`: Extracted behavioral facts.
- Per memory system (Mem0, Letta, Supermemory, Zep): `<system>_ingestion.json`, `<system>_retrieval.json`, `<system>_results.json`, plus `<system>_judgments_<judge>.json` for each of seven judges, plus `<system>_judgments_merged.json`.
- Per memory system native config: `<system>_fullpipeline_*` variants.
- `baselayer_*`: Base Layer substrate retrieval (MiniLM + ChromaDB).
- `c8_c9_*`: Raw corpus (C8) and raw corpus + spec (C9).

## How naming works here

Standard per-subject schema from `docs/FILE_NAMING.md`. Judge short names: `haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`, `gemini_flash`, `gemini_pro`. Memory-system short names: `mem0`, `letta`, `supermemory`, `zep`, `baselayer`. Condition codes: `C1`, `C2a`, `C3`, `C4`, `C4a`, `C5`, `C8`, `C9` (plain-English meanings in `docs/FILE_NAMING.md`).

## Where these files come from / go to

Inputs: source corpus and spec under `data/global_subjects/augustine/`. Outputs: aggregate into `results/RESULTS_S113.json` (and the forthcoming `RESULTS_S114.json`) and feed per-claim verification in `docs/PROVENANCE_INDEX.md`.

## Caveats worth knowing

- If a judge cell looks empty or shows `parse_failure: true`, do not silently drop it; the 5-judge primary recompute handles those correctly. Aggregating raw without filtering will skew numbers.
- S114 backfills for any missing judge cells live in `results/_s114_backfills/` with filenames like `global_augustine__<condition>__<judge>.json`.
