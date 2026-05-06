# `results/franklin/` — Results for Benjamin Franklin (known-figure control)

**What's in this folder:** Responses and judge scores for Franklin, used as a known-figure control. Franklin is not part of the main N=14 gradient; his role is to show what happens when the model already knows the subject well.

## Why Franklin is a control, not a subject

Franklin is widely represented in LLM pretraining. His C5 baseline is 4.10 out of 5. When the model already knows the subject that well, adding a behavioral specification does not help (and can slightly hurt). This confirms that the spec is a tool for the subjects the model doesn't already know. The paper cites this in §1.

## Contents

- `judgments.json`: Core judge scores.
- `fullstack_haiku.json`: Full-stack spec run with Haiku as the response model.
- `gemini_pro_judgments.json`, `opus_judgments.json`, `sonnet_judgments.json`: Per-judge score files.

## How naming works here

Same schema as the other per-subject folders, described in `docs/FILE_NAMING.md` and `../README.md`. Franklin's folder is thinner than the globals because he is a control, not a main-gradient subject.

## Where these files come from / go to

Generated from batteries under `data/franklin/`. Feeds the known-figure control discussion in paper §1 and related sections.

## Caveats worth knowing

- Franklin's legacy battery has 2 of 40 questions with held-out n-gram leakage (Q49 and Q56). The 14 main-study subjects have zero leakage.
- Franklin is not included in the main gradient regression or Wilcoxon tests. He sits alone as a high-baseline comparison point.
