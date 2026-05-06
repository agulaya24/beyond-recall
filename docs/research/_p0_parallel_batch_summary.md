# P0 Parallel Batch — Summary

_Generated 2026-04-23. All three post-hoc analyses on the "Beyond Recall" study completed as pure-data local computation (no API calls)._

## Status

| Job | Status | Report | Data |
|---|---|---|---|
| P0-7 Pairwise spec similarity | DONE | [`spec_similarity_analysis.md`](spec_similarity_analysis.md) | [`spec_similarity_matrices.json`](spec_similarity_matrices.json) |
| P0-16 Rubric sensitivity (refusals) | DONE | [`rubric_sensitivity_refusals.md`](rubric_sensitivity_refusals.md) | [`rubric_sensitivity_refusals.json`](rubric_sensitivity_refusals.json) |
| P0-4 Spec-tag citation trace | DONE | [`spec_tag_citation_trace.md`](spec_tag_citation_trace.md) | [`spec_tag_citation_trace.json`](spec_tag_citation_trace.json) |

## Runtime

| Job | Wall-clock (fresh cold cache) |
|---|---:|
| P0-7 (MiniLM embedding of 14 specs × 2 modes) | 9.1 s |
| P0-16 (load judgments + recode + aggregate, 14 subjects) | 1.3 s |
| P0-4 (content-bigram matching, 1,092 responses × ~17 tags × 14 subjects) | 3.3 s |

All three scripts runnable from repo root via `python scripts/<name>.py`.

## Surprising findings — flag to the author

### 1. JOB 2 IS THE HEADLINE FINDING. The paper's aggregate Δ_spec is almost entirely refusal-displacement.

- Under broader-rule refusal recoding (response contains any refusal pattern → score 2.5 if judge scored ≤ 2), mean Δ_spec collapses from **+0.427 to +0.008** across 14 subjects. Mean Δ_facts+spec drops from **+0.552 to +0.050**.
- Under narrow-rule recoding (response starts with explicit refusal), Δ_spec drops from **+0.427 to +0.059**. Still a ~86% absorption.
- **Why it matters.** The paper's §4.1 transition-category table already shows that 33.3% of low-baseline gains are 1→2 refusal-to-engagement crossings. This sensitivity check quantifies what that transition is worth at the aggregate mean: nearly all of it. The right framing is: the specification's main aggregate mechanism on the low-baseline slice is *replacing refusals with substantive engagement*, not *producing more-accurate predictions at matched engagement levels*.
- **Two subjects survive even broader recoding:** Hamerton (Δ_c4a = +1.66 → paper thesis for "unknown figure" holds), Fukuzawa (+0.55). Other 12 subjects compress toward zero.
- **The low-baseline slice becomes fragile:** N drops from 9 (original) to 4 (narrow) to 1 (broader) because recoding lifts many C5 scores above 2. The "9 of 9 positive" framing in §4.1 is rubric-dependent.
- **Recommendation for §4.5 or Appendix D:** cite this sensitivity check explicitly; state that roughly 90-98% of the reported aggregate Δ_spec is refusal-displacement under a refusal-neutral rubric, and that the Hamerton result survives.

### 2. JOB 1: discrete spec content is essentially non-overlapping across subjects.

- Anchor-name Jaccard (uppercase header names like `RESTLESS ORIGIN`): mean **0.003**, max 0.056. Prediction-name Jaccard: mean **0.001**.
- Only **1 anchor name** appears verbatim in ≥3 subjects (`DIGNITY FLOOR`: Equiano, Yung Wing, Zitkala-Sa). **Zero** prediction names repeat at that threshold.
- Semantic cosine on full-stack concatenation is moderate (mean 0.658), but that's within the shared-register range for 35-40KB English prose documents on broadly human-behavioral topics.
- **Reading:** the C2c v2 partial-match result (+0.22 above baseline in paper §4.3) cannot be explained by discrete cross-spec content leakage. Supports §4.3's "Content, Not Format" thesis rather than undercutting it.
- **Nuance:** the Hamerton–Equiano full-stack cosine is 0.859 (the highest pair); this is soft thematic overlap (both slave-era autobiographical subjects) that discrete-content analysis doesn't capture. The full report flags this.

### 3. JOB 3: the 78.6% vs 50.0% §4.3 claim tightens under the expanded lexicon.

- Under the 3-layer matching (short-form + full-name + content-bigram), **96.9% of C2a responses cite ≥1 own-spec tag; 70.0% of C2c own-tag; 89.3% of C2c served-tag**.
- The **full-name column is the cleanest signal** (2+ word uppercase names = effectively zero accidental collision): **75.8% C2a own vs 0.2% C2c own vs 67.3% C2c served**. A 67-point gap between served and own on C2c = direct evidence the model is following the spec it was given, not pretraining-leak describing the target subject.
- **Short-form (A1/P1 IDs) is vacuous for the C2c own-vs-served distinction** because all specs reuse the same ID range. The C2c own/served short-form rates are 48.9%/50.1% for this reason.
- Spearman ρ (tag-hit count vs 5-judge score):
  - C2a: ρ = +0.054, p = 0.21 — near-zero because C2a is ceiling-heavy (97% have ≥1 hit). Mean score at 0 hits = 1.80; at ≥1 hits = 2.33 (0.53-point contrast). Use the mean-contrast, not Spearman, for the C2a claim.
  - C2c: ρ = +0.284, p < 1e-10 — meaningful, driven by wider hit-count distribution.

## Caveats / methodological notes for §4.5 or Appendix

- **Rubric-recoded baseline is counterfactual.** Job 2's recoding changes how the scale is read, not the underlying response quality. Both the original and recoded numbers are defensible; the paper should report both and name the choice explicitly.
- **Hamerton served-spec unavailable.** Hamerton's C2c used Franklin's spec, which is not in the study repo. Job 3's served-tag hit rate for Hamerton is `---`. Everything else works for Hamerton.
- **C2c wrong-spec-v2 not analyzed in Job 3.** The task asked for C2c from results_v2.json, which is v1 (fixed derangement). v2 (random derangement, at `results/_wrong_spec_v2/`) uses different response text and would produce separate numbers. Out of task scope; flag if the author wants it.
- **Paper §4.3 uses a narrower lexicon than Job 3.** The published 78.6% / 50.0% come from `compute_spec_activation.py` (short-form only, 9 low-baseline subjects). The Job 3 any-hit numbers are not a direct replacement for those paper claims — they're a wider lens. The short-form column in Job 3 across 14 subjects is the direct comparison: 68.9% / 48.9%.

## Scripts added

- `scripts/compute_spec_similarity.py` (new)
- `scripts/rubric_sensitivity_refusals.py` (new)
- `scripts/trace_tag_citation.py` (new; extends `compute_spec_activation.py`)

No paper files modified. No data files moved. All outputs under `docs/research/`.
