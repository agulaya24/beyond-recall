# `docs/research/` — Per-section verification notes and sub-study outputs

**What's in this folder:** Analysis scripts, recompute outputs, and verification notes that back specific sections of the paper. When a paper claim needs a receipt, the receipt often lives here.

> ⚠️ **Section-number anchor note.** Files in this directory were written against v6/v7/v8 paper structures and reference those section numbers (e.g., `§4.5` for Robustness, `§4.7` for Letta stateful, `§4.8` for Scaling, `§7` for Safety). v9 renumbered these. When cross-referencing a research doc against v9, consult `ISSUES.md` at repo root or the §-mapping in `docs/reviews/s114_v9_reference_audit.md` for the current mapping (v8 § X → v9 § Y). Research docs are preserved v8-anchored for historical accuracy; only the paper body was remapped.

## Contents

**Per-section verification notes (read these to cross-check a specific paper section):**

- `section_2_1_verification.md`, `section_2_3_verification.md`, `section_2_4_verification.md`, `section_3_verification.md`, `section_3_3_pipeline_verification.md`, `section_3_4_battery_verification.md`: Each checks a specific paper section against the raw data.

**Recompute outputs and pooled analyses:**

- `recompute_5judge_primary.md`: The 5-judge primary recompute output. This is the preferred source for §4 numbers in the paper until `DATA_REFERENCE.md` is updated.
- `tier2_recompute_s114.json`: Recomputed Tier 2 results for S114.
- `s114_parse_failure_manifest.json`: Manifest of judge parse failures (`score: 0, parse_failure: true` entries) across the S114 data sweep.
- `_score_band_pool.json`, `_score_band_stats.json`, `_band_examples.txt`: Pool and stats used to build score-band analyses.
- `_baselayer_c1_c3_candidates.json`, `_mlz_c1_c3_candidates.json`, `_sm_c1_c3_candidates.json`: Candidate question pools for C1 vs C3 paired comparisons, per provider group.

**Paired and named analyses:**

- `baselayer_c1_vs_c3_paired_analysis.md`, `mem0_letta_zep_c1_vs_c3_analysis.md`, `supermemory_c1_vs_c3_paired_analysis.md`: Paired analyses of the spec delta (C3 vs C1) per memory system.
- `letta_stateful_deep_read.md`, `letta_stateful_matched_rerun.md`: The Letta stateful-agent subanalysis that feeds paper §4.7.
- `name_blind_wrong_spec_pilot.md`, `wrong_spec_detection_analysis.md`, `wrong_spec_detection_raw.json`, `wrong_spec_validation_sample.json`: Wrong-spec control analyses (name-blind pilot and full detection analysis).
- `provider_benchmarks.md`: Per-provider behavior notes from working with each memory system.
- `score_interval_significance.md`: Score-interval significance analysis.

**Helper scripts with leading underscores:**

- `_analyze_score_bands.py`, `_build_score_pool.py`, `_print_band_examples.py`, `_recompute_variance_full_pool.py`: One-off analysis helpers. Underscore prefix means "supporting script, not the main runner".

**Subfolders:**

- `_letta_blocks/`: Letta human-memory-block ingestion study (see its README).
- `_letta_rerun/`: Letta stateful-agent rerun with matched specs and renamed batteries (see its README).

## How naming works here

Filenames with a leading underscore are supporting scripts or intermediate outputs. Section verification files are named `section_<X>_<Y>_verification.md` where `<X>_<Y>` maps to a paper section. Recompute outputs use `recompute_*` prefixes. See `docs/FILE_NAMING.md` for the full scheme.

## Caveats worth knowing

- `_*.json` pool files are intermediate artifacts. They can be regenerated from the `_*.py` scripts; do not treat them as primary data.
- The wrong-spec raw JSON is the detection-analysis input, not the response data (responses live under `results/_wrong_spec_v2/`).
