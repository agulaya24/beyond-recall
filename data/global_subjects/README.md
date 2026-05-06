# `data/global_subjects/` — Inputs for the 13 global subjects

**What's in this folder:** One subfolder per global subject holding that subject's source corpus split, extracted facts, question battery, and behavioral specification layers. These are the inputs that feed the experiment; outputs live in `results/global_<subject>/`.

The 13 global subjects span 11 cultures across 2,500 years. Together with Hamerton, they make up the N=14 main-gradient sample. Franklin is a control and lives separately.

## Contents

One subfolder per subject. Each has the same file schema:

- `augustine/`, `babur/`, `bernal_diaz/`, `cellini/`, `ebers/`, `equiano/`, `fukuzawa/`, `keckley/`, `rousseau/`, `seacole/`, `sunity_devee/`, `yung_wing/`, `zitkala_sa/`

### Per-subject file schema

Inside every subject folder (for example `data/global_subjects/augustine/`):

| File | What it is |
|---|---|
| `facts.json` | Behavioral facts extracted from the training half of the corpus. Uses the 46-predicate vocabulary. Fed to memory systems in the controlled condition. |
| `battery.json` | The held-out behavioral-prediction question set. Each item has a scenario plus the ground-truth passage from the held-out half. This is the test set. |
| `spec.md` | Early short-form specification (pre-final-layer). |
| `spec_production.md` | The production behavioral specification used in the paper. Layered composition of anchors + core + predictions + brief. Size roughly 5,000 to 8,000 tokens. |
| `anchors_v4.md` | Anchors layer. Axiom-style behavioral anchors authored blind from the facts. |
| `core_v4.md` | Core layer. A ~800-word behavioral narrative. |
| `predictions_v4.md` | Predictions layer. Behavioral patterns and decision heuristics. |
| `brief_v5.md` | Unified brief composed from the three layers. |
| `judgments.json` | Subject-level judge output (per-item scores, rubric). |
| `results.json` | Subject-level aggregated results snapshot (condition means, raw responses). |

The paper's "behavioral specification" is `spec_production.md`. The four layered `.md` files (anchors, core, predictions, brief) are the intermediate artifacts that compose into it.

## How naming works here

Subject folder names use lowercase underscore-separated short names. Files use stable short names within each folder. Versioning is visible in suffixes: `_v4.md` (authored layers) and `_v5.md` (brief). Earlier versions are retained per the convention in `docs/FILE_NAMING.md`.

## Where these files come from / go to

- `facts.json` is produced by the extraction pipeline (Haiku extraction using the 46 behavioral predicates).
- `anchors_v4.md`, `core_v4.md`, `predictions_v4.md` are produced by the authoring pipeline (Sonnet, blind regeneration).
- `brief_v5.md` and `spec_production.md` are produced by the compose step (Opus).
- `battery.json` is hand-curated from the held-out corpus half and formatted by the battery-generation script.

Downstream: everything in `results/global_<subject>/` consumes these files.

## Caveats worth knowing

- Source corpora (full `training.txt` and `heldout.txt`) are referenced from per-subject folders; `heldout.txt` for most subjects is located inside `results/global_<subject>/` rather than here. This is a legacy of when the two folders were first wired up.
- The extraction vocabulary is 46 predicates, not 47. An older comment in the pipeline code said 47; it is stale.
- Each subject has 39 or 40 battery items depending on the source. Most globals have 39. See `STUDY_MEMORY.md` for the exact count.
