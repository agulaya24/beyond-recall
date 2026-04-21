# `data/franklin_obscure/` — Input data for the Franklin cross-corpus test

**What's in this folder:** A small exploratory battery built from Franklin's lesser-known letters (not the autobiography). Used for a one-off cross-corpus test that did not make the paper.

## Why this folder exists

Franklin's autobiography is famous; his letters are less so. The question was: does the model's pretraining advantage shrink when Franklin is probed with obscure scenarios? The results were exploratory and did not support a paper claim, so this folder sits as an artifact of that line of inquiry.

## Contents

- `battery.json`: Exploratory battery built from Franklin's obscure letters.
- `facts.json`: Facts extracted from the same corpus.

## How naming works here

Follows the same basic convention as the main `data/franklin/` folder but with a different source corpus (letters, not the autobiography).

## Where these files come from / go to

Inputs: Franklin's public-domain letters. Outputs: `results/franklin_obscure/`. Not consumed by any paper section.

## Caveats worth knowing

- Exploratory, not main-paper data. Ignore unless specifically needed for follow-up work.
- Thin coverage; no specification was generated here.
