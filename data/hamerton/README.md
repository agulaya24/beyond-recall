# `data/hamerton/` — Input data for Philip Gilbert Hamerton (primary subject)

**What's in this folder:** The source facts, question battery, and behavioral-specification layers for Philip Gilbert Hamerton (British, 1834-1894, C5 baseline 1.25). Source text: *Autobiography* (posthumous).

Hamerton has the lowest C5 baseline of any subject in the study. He was the first subject piloted, so his data layout is slightly different from the 13 globals: the specification layers live in a `spec/` subfolder rather than alongside the other files.

## Contents

- `facts.json`: Behavioral facts extracted from the training half of the corpus. Uses the 46-predicate vocabulary.
- `battery.json`: Held-out behavioral-prediction question set.
- `questions_80.json`: Early 80-question variant of the battery (superseded by `battery.json`; kept for provenance).
- `shared_facts.json`: Facts shared across conditions (subset of `facts.json`).
- `analysis/`: Per-subject analysis outputs (see its README).
- `spec/`: The four-layer behavioral specification (see its README).

## How naming works here

Hamerton's layout is a legacy structure from when he was the pilot subject. The 13 global subjects adopted a flatter layout later. Underlying file roles and naming conventions are described in `docs/FILE_NAMING.md`.

## Where these files come from / go to

Inputs: Hamerton's public-domain autobiography. Outputs: `results/hamerton/` holds every response and judge score that use these inputs.

## Caveats worth knowing

- `questions_80.json` is the earlier question set. The paper uses `battery.json` (39 questions).
- Hamerton had the most method iterations (full-stack rerun, Letta stateful-agent test, S114 3-judge backfill). Most iteration artifacts live in `results/hamerton/`, not here.
- Hamerton's spec layers use the same `_v4` / `_v5` versioning pattern as the globals.
