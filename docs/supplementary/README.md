# Supplementary Materials

These materials are part of the Beyond Recall study and are referenced from the main paper at the indicated section pointers. They were placed in supplementary materials for length reasons; all scientific content is preserved verbatim.

## Contents

| File | Maps to paper section | What it contains |
|---|---|---|
| [`appendix_E_per_subject_worked_examples.md`](https://github.com/agulaya24/beyond-recall/blob/main/docs/supplementary/appendix_E_per_subject_worked_examples.md) | Appendix E (stub at paper §E) | Three illustrative paired (C5, C4a) per-question response excerpts for each of the 14 main-study subjects. Cited from §3.3 (rubric definition), §4.1 (worked examples A, B, C), §4.1.1 (multi-anchor crossings), and Appendix D.5. |
| [`appendix_B_per_subject_paired_delta_tables.md`](https://github.com/agulaya24/beyond-recall/blob/main/docs/supplementary/appendix_B_per_subject_paired_delta_tables.md) | Appendix B.2 (stub) and B.3 per-subject distribution (stub) | The 10-category by 15-subject battery composition matrix (B.2) and the 15-row LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING per-subject distribution (B.3 per-subject table). Aggregate distributions and surrounding prose remain in the main paper. |

## How the cross-references resolve

The main paper retains the appendix anchors (`Appendix E`, `B.2`, `B.3`) as stubs that point to this directory. Existing in-text references (for example, `(see Appendix E)` or `Appendix B.2`) continue to resolve to the paper at the same anchor; the stub then directs the reader here for the moved content. Readers who do not need the raw per-subject material can read the paper end-to-end without following the pointer.

## What was not moved (and why)

- **Appendix B.4, B.5, B.6, B.7, B.8, B.9, B.10** stay in the paper. Each is load-bearing for §4 claims (effect-size breakdowns, sensitivity analyses, coupling-free reframing, predicate ablation, the pre-vs-post-hoc table).
- **Appendix B.11** (per-system per-subject paired-delta distributions) stays in the paper. Inspection showed it is a 6-row representative table, not a 14-row per-subject table; it does not bloat the PDF in the way B.2 and B.3 do.
- **Appendix D.4** (per-judge score matrices, 70 rows × 9 columns) stays in the paper. It is referenced as the master per-judge audit and the design choice was to keep it visible alongside the §4.6.2 inter-judge sensitivity analysis.

## Reproducibility

These supplementary files are reproducible from the same data and scripts that produced the in-paper analyses. Source pointers are in [`docs/PROVENANCE_INDEX.md`](https://github.com/agulaya24/beyond-recall/blob/main/docs/PROVENANCE_INDEX.md) and [`docs/DATA_REFERENCE.md`](https://github.com/agulaya24/beyond-recall/blob/main/docs/DATA_REFERENCE.md). Battery JSON files are at `results/global_<subject>/battery_v2.json` and `data/hamerton/battery.json`. Per-subject response artifacts are at `results/global_<subject>/results_v2.json` and `results/hamerton/results.json`. Behavioral-axis classification is at `docs/research/question_category_audit.md`.
