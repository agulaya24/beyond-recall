# docs/research/ Traceability Matrix

Generated: 2026-05-11. Source: paper text + all `docs/supplementary/*.md` appendices.

**Purpose:** Per Aarik 2026-05-11, `docs/research/` was flagged HIGH cascade risk in the repo cleanup audit because the paper has 30+ direct footnote references by exact path. Rather than restructure `docs/research/` (post-launch), this matrix is the canonical machine-readable list of inbound references so any future file move can update referrers in lock-step.

**Regenerate** after any paper edit that touches a `docs/research/<file>` mention:

```
python scripts/build_research_traceability_matrix_20260511.py
```

**Summary.** Paper references 35 distinct files in `docs/research/`. Of those, **0** do not exist on disk (broken refs to fix). Supplementary appendices reference 4 additional files not cited from the paper body.

## Paper-referenced files

| Path | On disk | Size | Paper lines | Supp refs |
|---|---|---:|---|---|
| `docs/research/DATA_LOCKS.md` | OK | 4,004 | 128 | — |
| `docs/research/baselayer_c1_vs_c3_paired_analysis.md` | OK | 18,138 | 1483 | — |
| `docs/research/battery_v1_v2_cache_alignment_diagnostic_20260508.md` | OK | 9,508 | 803 | — |
| `docs/research/held_out_leakage_investigation_20260428.md` | OK | 8,435 | 905, 2243 | — |
| `docs/research/joint_battery_sensitivity_4_6_3_20260507.md` | OK | 2,883 | 1623 | — |
| `docs/research/letta_semantic_duplication_20260501.json` | OK | 17,608 | 1529 | appendix_G_letta_full_case_study.md:47 |
| `docs/research/letta_vs_spec_leakage_analysis_20260507.md` | OK | 27,930 | 1533 | appendix_G_letta_full_case_study.md:47 |
| `docs/research/letta_vs_spec_per_question_scores_20260507.csv` | OK | 96,688 | 1533 | — |
| `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md` | OK | 25,727 | 1483 | — |
| `docs/research/multi_anchor_rates_all_pairs_20260430.json` | OK | 135,313 | 1067 | — |
| `docs/research/pattern_activation_deep_20260428.md` | OK | 37,564 | 2195 | — |
| `docs/research/per_system_anchor_crossing_20260427.json` | OK | 46,521 | 1377, 2291 | — |
| `docs/research/per_system_anchor_crossing_20260427.md` | OK | 16,159 | 1347 | — |
| `docs/research/permutation_test_4_1_gradient_20260507.md` | OK | 2,128 | 1627 | — |
| `docs/research/predicate_ablation_results_20260428.json` | OK | 208,356 | 2221 | — |
| `docs/research/question_category_audit.md` | OK | 5,284 | 2138, 2148, 2152, 2164 | appendix_B_per_subject_paired_delta_tables.md:46, README.md:24 |
| `docs/research/recompute_5judge_primary.md` | OK | 4,066 | 1593, 1735 | — |
| `docs/research/refusal_intent_classification.md` | OK | 16,260 | 1997 | — |
| `docs/research/retrieval_overlap_analysis_20260501.json` | OK | 50,136 | 1275, 1305 | — |
| `docs/research/retrieval_overlap_semantic_20260501.json` | OK | 144,154 | 1683 | — |
| `docs/research/rubric_handling_validity_full.json` | OK | 516,702 | 2456 | — |
| `docs/research/s114_anchor_crossing_examples.json` | OK | 6,626 | 430 | — |
| `docs/research/spec_activation_analysis.json` | OK | 29,110 | 1176 | — |
| `docs/research/stats_update.md` | OK | 14,484 | 504 | — |
| `docs/research/supermemory_c1_vs_c3_paired_analysis.md` | OK | 22,377 | 1483 | — |
| `docs/research/v10_battery_sensitivity_analysis.md` | OK | 8,602 | 1609 | — |
| `docs/research/v10_coupling_sensitivity_analysis.md` | OK | 7,682 | 2199 | — |
| `docs/research/v10_pipeline_variance_analysis.md` | OK | 8,486 | 1913 | — |
| `docs/research/v11_9_6_pipeline_variance_similarity_20260510.json` | OK | 6,725 | 1898 | — |
| `docs/research/v11_9_6_pipeline_variance_similarity_20260510.md` | OK | 3,107 | 1898 | — |
| `docs/research/v11_emit/4_3_wrong_spec.json` | OK | 91,556 | 1660 | — |
| `docs/research/v11_emit/appendix_b_battery.json` | OK | 170,036 | 2164 | — |
| `docs/research/v11_panel_completeness_audit.csv` | OK | 419,460 | 1735 | — |
| `docs/research/wins_inventory_20260428.json` | OK | 253,381 | 2195, 2229 | — |
| `docs/research/within_band_shifts_20260428.json` | OK | 654,595 | 436 | — |

## Supplementary-only references

These files are referenced by supplementary appendices but not by the paper body. They still matter for `docs/supplementary/*.md` reproducibility.

- `docs/research/_letta_rerun/fullstack_named/RESULTS.md` (OK)
- `docs/research/letta_stateful_deep_read.md` (OK)
- `docs/research/letta_stateful_matched_rerun.md` (OK)
- `docs/research/s114_low_end_inflation_audit.json` (OK)