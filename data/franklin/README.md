# `data/franklin/` — Input data for Benjamin Franklin (known-figure control)

**What's in this folder:** The source facts and question battery for Benjamin Franklin. Franklin is used as a known-figure control, not as a main-gradient subject.

Franklin's C5 baseline is 4.10 out of 5, meaning the model already knows him very well from pretraining. The paper uses Franklin to show that adding a behavioral specification does not help when the model already knows the subject (and can slightly hurt).

## Contents

- `battery.json`: Held-out behavioral-prediction questions for Franklin.
- `facts.json`: Extracted behavioral facts about Franklin.
- `franklin_shared_facts.json`: Subset of facts shared across conditions.
- `questions_80_franklin.json`: Early 80-question variant of the battery (superseded; kept for provenance).
- `analysis/`: Per-subject analysis outputs (currently empty).

## How naming works here

Similar layout to Hamerton (both were early subjects and keep a slightly different structure from the 13 globals). File roles follow `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: Franklin's autobiography (public domain). Outputs: `results/franklin/`.

## Caveats worth knowing

- Franklin's battery has 2 of 40 questions with held-out n-gram leakage (Q49 and Q56). The 14 main-study subjects have zero leakage.
- Franklin is not in the main N=14 gradient. He is a standalone high-baseline comparison.
- No `spec/` folder here because Franklin was used primarily for the baseline comparison. A spec does exist for him and was applied in the wrong-spec v1 control; look in earlier-run results for traces of that.
