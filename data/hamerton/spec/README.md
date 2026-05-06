# `data/hamerton/spec/` — Hamerton's behavioral-specification layers

**What's in this folder:** The four Markdown files that make up Hamerton's behavioral specification. These are what the model actually sees in the spec-only condition (C2a) and the spec-plus-facts condition (C4a).

A "behavioral specification" here is a compressed, structured description of how a person reasons, authored from extracted facts about them. Hamerton's spec is the production version used in the paper.

## Contents

- `anchors_v4.md`: Axiom-style behavioral anchors authored blind from the facts. The shortest of the four. Each anchor is a load-bearing claim about how Hamerton reasons.
- `core_v4.md`: About 800 words of behavioral narrative. Explains the through-lines in how Hamerton makes decisions.
- `predictions_v4.md`: Behavioral patterns and decision heuristics. More operational than the core.
- `brief_v5_clean.md`: Unified brief composed from the three layers. This is the final artifact used in conditions.

## How naming works here

The `_v4` suffix on the three authored layers marks the current generation; earlier `_v1`, `_v2`, `_v3` variants were iterated during the pilot and are no longer checked in. The brief is `_v5` because it composes on top of the `_v4` layers.

## Where these files come from / go to

- Produced by the authoring pipeline (Sonnet, blind regeneration) for the three layer files and by the compose step (Opus) for the brief.
- Consumed: these files are loaded as context in conditions C2a, C3_*, C4a, and C9 for Hamerton. Every `results/hamerton/baselayer_*.json` run that includes a spec uses `brief_v5_clean.md`.

## Caveats worth knowing

- The `_clean` suffix on the brief indicates it was post-processed (name anonymization, final polish). Use that version, not an earlier brief.
- For the 13 global subjects, the equivalent files live directly under `data/global_subjects/<subject>/` (not in a `spec/` subfolder). Hamerton keeps the subfolder for legacy reasons.
