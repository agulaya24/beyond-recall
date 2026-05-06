# `docs/research/_letta_rerun/` — Letta stateful-agent rerun with corrections

**What's in this folder:** A corrected rerun of the Letta stateful-agent comparison (paper §4.7) after battery-mismatch and anonymization fixes. Numeric outputs here supersede the earlier run in `_letta_blocks/`.

Letta self-edits a "human" memory block during conversation. This folder rescored that block against the Base Layer C2a spec (spec-only condition) on matched batteries and matched response models.

## Contents

**Diagnostic scripts (numbered by order in the rerun):**

- `01_inspect_stateful.py` through `08_sample_c2a.py`: Inspection and sampling scripts that diagnosed the original run's issues (battery mismatch, named-vs-anonymized spec, judge parse behavior).
- `10_extract_batteries.py`, `20_run_c2a_named.py`: Extract the matched batteries and rerun C2a with the named (non-anonymized) spec for a fair comparison.
- `30_inspect_letta_judges.py`, `31_inspect_gpt54.py`, `32_reread_judges.py`: Judge-side inspection.
- `40_judge_responses.py`, `42_progress_check.py`: The actual rejudging run and its progress monitor.
- `50_aggregate.py`, `51_refusal_check.py`: Aggregation and refusal-rate check.

**Data files (Babur and Ebers, the two subjects rerun here):**

- `babur_bl_c2a_named_responses.json`, `ebers_bl_c2a_named_responses.json`: Base Layer C2a responses using the named-spec version (for fair comparison against Letta's named ingestion).
- `babur_letta_battery.json`, `ebers_letta_battery.json`: The matched batteries used.
- `babur_spec_named.md`, `ebers_spec_named.md`: The named (non-anonymized) spec versions used in the rerun.
- `babur_stateful_summary.json`, `ebers_stateful_summary.json`: Per-subject stateful-run summary.
- `<subject>_judgments_<judge>.json` for each of 7 judges: Per-judge rejudge results (haiku, sonnet, opus, gpt4o, gpt54, gemini_flash, gemini_pro).

## How naming works here

Scripts are prefixed with two-digit ordinals to indicate run order. Data files follow `<subject>_<artifact>.json` or `<subject>_judgments_<judge>.json`. Judge short names follow `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: original Letta run at `_letta_blocks/` plus the batteries and specs under `data/global_subjects/<subject>/`. Outputs update the corrected Letta numbers in `STUDY_MEMORY.md` and paper §4.7.

## Caveats worth knowing

- The corrected numbers are the ones the paper uses. Earlier numbers in `_letta_blocks/` are retained for audit, not citation.
- Only Babur and Ebers were rerun here. Hamerton's numbers come from the original full-stack Letta run.
- S114 corrected results: Ebers Letta 3.00 vs Base Layer 2.25 (Δ +0.75, down from earlier +1.21). Babur 2.73 vs 2.44 (Δ +0.29, down from earlier +0.57).
