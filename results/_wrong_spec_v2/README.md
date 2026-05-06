# `results/_wrong_spec_v2/` — Wrong-spec control (random derangement)

**What's in this folder:** Results for the wrong-spec control. Every subject is given a different subject's behavioral specification, assigned by random derangement (seed=42). Tests whether the correct spec matters, or whether any structured prompt would produce similar lift.

## What the wrong-spec control tests

If giving the model any specification (even the wrong one) produces the same accuracy lift as the correct one, then the spec is not capturing anything subject-specific. This control rules that out. The paper reports: wrong-spec lift is near-baseline (+0.28) while correct-spec lift is meaningfully higher (+0.53). Additionally, the response model explicitly flags the mismatch on 60.6% of questions (content-grounded detection).

## Contents

One subfolder per subject (same 13 globals as elsewhere): `global_augustine/`, `global_babur/`, `global_bernal_diaz/`, `global_cellini/`, `global_ebers/`, `global_equiano/`, `global_fukuzawa/`, `global_keckley/`, `global_rousseau/`, `global_seacole/`, `global_sunity_devee/`, `global_yung_wing/`, `global_zitkala_sa/`.

Each subfolder contains `wrong_spec_v2_judgments_<judge>.json` for each of the seven judges, plus occasional `.rl_backup` files (rate-limit-retry saves) and one `.brief_only_backup` file (pre-fullstack backup).

Top-level files:

- `hamerton_results.json`: Hamerton's wrong-spec v2 run.
- `wrong_spec_v2_manifest.json`: Manifest for the whole wrong-spec v2 run (seed, derangement mapping, timestamps).

## How naming works here

Same judge short names as the main per-subject folders. The `wrong_spec_v2_` prefix marks these as the v2 (random-derangement) version of the wrong-spec control. An earlier v1 used a deterministic fixed cross-subject pairing (designed for cultural/temporal distance; see `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING, lines 51-60) for the 13 global subjects. Hamerton's v1 separately uses Franklin's spec via `run_full_study.py` and is reported in §4.1.1. v1 is mentioned as historical context only.

## Where these files come from / go to

Inputs: each subject's battery (same as core runs) plus a scrambled spec from a randomly chosen other subject. Outputs feed paper §6 and `docs/research/wrong_spec_detection_analysis.md`.

## Caveats worth knowing

- Use v2 numbers, not v1. v1 is non-primary.
- The derangement seed is 42; the mapping is recorded in the manifest.
- "Content-grounded detection" (60.6%) means the response itself flagged the mismatch, not that a judge flagged it. Specs were name-anonymized, so detection is by content, not by name.
