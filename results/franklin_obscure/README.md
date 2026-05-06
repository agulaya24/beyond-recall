# `results/franklin_obscure/` — Exploratory Franklin cross-corpus test

**What's in this folder:** A small exploratory run where Franklin is tested on lesser-known letters rather than his well-known autobiography. Not a main-paper result.

## Why this folder exists

Franklin's autobiography is famous; his letters are less so. Testing on the letters was a thought experiment: does the model's pretraining advantage shrink when Franklin is probed with obscure scenarios? Results were exploratory and did not make the paper.

## Contents

- `fullstack_haiku.json`: Full-stack spec run on the obscure-letters battery, Haiku as the response model.

## How naming works here

Same naming schema as other per-subject result folders. See `../README.md` and `docs/FILE_NAMING.md`.

## Where these files come from / go to

Generated from the battery at `data/franklin_obscure/`. Not consumed by any paper section. Ignore unless specifically needed for follow-up work.

## Caveats worth knowing

- This is an exploratory folder. It is not part of the main paper's results.
- Thin coverage (one response-model run). Do not draw conclusions from it alone.
