# v11 reconciliation diff (scaffold-emit vs v10 paper text)

_Generated: 2026-04-25T17:52:03+00:00_

Aggregation rule (locked, architecture spec §1): 5-judge primary panel `{haiku, sonnet, opus, gpt4o, gpt54}`. Per-judge per-question -> per-judge per-subject mean -> panel mean across the 5 judges.

## Executive summary

- Total claim_ids aggregated: **1509**
- MATCH: **1089** (72.2%)
- MINOR_ROUNDING: **65** (4.3%)
- MISMATCH_SUBSTANTIVE: **206** (13.7%)
- STAT_TYPE: **0**
- NON_CLAIM: **149** (scaffold has a value but paper text does not cite it)
- SIGN_FLIPS surfaced: **14**

PAPER_ONLY items are catalogued in their own section below.

## Substantive mismatches

| claim_id | section | paper | scaffold | abs_delta | sign_flip | contrast | suggested_fix |
|---|---|---:|---:|---:|:--:|---|---|
| `4_2_hamerton_corpus_tokens` | §4.2 + §4.2.1 | 25231.0000 | 32800 | 7569.0000 |   |  | replace paper 25231.0000 with scaffold 32800 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_hamerton_spec_tokens` | §4.2 + §4.2.1 | 5000.0000 | 4478 | 522.0000 |   |  | replace paper 5000.0000 with scaffold 4478 (emit script: _v11_emit_4_2_compression.py) |
| `appD_3_5_chars` | Appendix D | 1599.0000 | 2086.6679 | 487.6679 |   | primary_mean < 2.0 across all 5 audit conditions | replace paper 1599.0000 with scaffold 2086.6679 (emit script: _v11_emit_appendix_d.py) |
| `4_2_yung_wing_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 6657 | 343.0000 |   |  | replace paper 7000.0000 with scaffold 6657 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_sunity_devee_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 6771 | 229.0000 |   |  | replace paper 7000.0000 with scaffold 6771 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_seacole_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 6787 | 213.0000 |   |  | replace paper 7000.0000 with scaffold 6787 (emit script: _v11_emit_4_2_compression.py) |
| `4_5_babur_letta_unique_named_entities` | §4.5 + Appendix F | 540.0000 | 416 | 124.0000 |   | Referential density: Letta block | replace paper 540.0000 with scaffold 416 (emit script: _v11_emit_4_5_letta.py) |
| `4_2_fukuzawa_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 7086 | 86.0000 |   |  | replace paper 7000.0000 with scaffold 7086 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_babur_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 6922 | 78.0000 |   |  | replace paper 7000.0000 with scaffold 6922 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_spec_tag_citation_rate_correct_numerator` | §4.3 | 209.0000 | 276 | 67.0000 |   | C2a_full_spec citation rate (no contrast) | replace paper 209.0000 with scaffold 276 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_ebers_spec_tokens` | §4.2 + §4.2.1 | 7300.0000 | 7244 | 56.0000 |   |  | replace paper 7300.0000 with scaffold 7244 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_bernal_diaz_spec_tokens` | §4.2 + §4.2.1 | 7300.0000 | 7349 | 49.0000 |   |  | replace paper 7300.0000 with scaffold 7349 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_2_baselayer_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 546 | 39.0000 |   | C3_baselayer − C1_baselayer | replace paper 507.0000 with scaffold 546 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_mem0_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 546 | 39.0000 |   | C3_mem0 − C1_mem0 | replace paper 507.0000 with scaffold 546 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 546 | 39.0000 |   | C3_supermemory − C1_supermemory | replace paper 507.0000 with scaffold 546 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_supermemory_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 546 | 39.0000 |   | C3_supermemory − C1_supermemory | replace paper 507.0000 with scaffold 546 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_zep_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 546 | 39.0000 |   | C3_zep − C1_zep | replace paper 507.0000 with scaffold 546 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appD_3_4_C5_n` | Appendix D | 351.0000 | 312 | 39.0000 |   | C5_baseline | replace paper 351.0000 with scaffold 312 (emit script: _v11_emit_appendix_d.py) |
| `appD_3_4_C4_n` | Appendix D | 351.0000 | 312 | 39.0000 |   | C4_factdump | replace paper 351.0000 with scaffold 312 (emit script: _v11_emit_appendix_d.py) |
| `appD_3_4_C4a_n` | Appendix D | 351.0000 | 312 | 39.0000 |   | C4a_full_facts_plus_spec | replace paper 351.0000 with scaffold 312 (emit script: _v11_emit_appendix_d.py) |
| `4_4_2_letta_archival_paired_total_n` | paper.4.4.2_4.4.3 | 507.0000 | 545 | 38.0000 |   | C3_letta − C1_letta | replace paper 507.0000 with scaffold 545 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_zep_helps_n` | paper.4.4.2_4.4.3 | 52.0000 | 82 | 30.0000 |   | C3_zep − C1_zep | replace paper 52.0000 with scaffold 82 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_baselayer_helps_n` | paper.4.4.2_4.4.3 | 39.0000 | 64 | 25.0000 |   | C3_baselayer − C1_baselayer | replace paper 39.0000 with scaffold 64 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appD_2_bernal_diaz_n_questions` | Appendix D | 23.0000 | 39 | 16.0000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 23.0000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `4_4_2_baselayer_hurts_n` | paper.4.4.2_4.4.3 | 39.0000 | 54 | 15.0000 |   | C3_baselayer − C1_baselayer | replace paper 39.0000 with scaffold 54 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appD_2_seacole_n_questions` | Appendix D | 53.8000 | 39 | 14.8000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 53.8000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `appD_2_slice_no_crossing_pct` | Appendix D | 24.0000 | 38.1766 | 14.1766 |   |  | replace paper 24.0000 with scaffold 38.1766 (emit script: _v11_emit_appendix_d.py) |
| `4_2_keckley_spec_tokens` | §4.2 + §4.2.1 | 7000.0000 | 7014 | 14.0000 |   |  | replace paper 7000.0000 with scaffold 7014 (emit script: _v11_emit_4_2_compression.py) |
| `appD_2_babur_n_questions` | Appendix D | 25.6000 | 39 | 13.4000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 25.6000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `appD_2_fukuzawa_n_questions` | Appendix D | 26.0000 | 39 | 13.0000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 26.0000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `4_5_ebers_bl_unique_named_entities` | §4.5 + Appendix F | 46.0000 | 34 | 12.0000 |   | Referential density: BL spec | replace paper 46.0000 with scaffold 34 (emit script: _v11_emit_4_5_letta.py) |
| `appD_2_hamerton_n_questions` | Appendix D | 27.0000 | 39 | 12.0000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 27.0000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `4_3_spec_tag_citation_rate_wrong_numerator` | §4.3 | 146.0000 | 156 | 10.0000 |   | C2c_wrong_spec citation rate (no contrast) | replace paper 146.0000 with scaffold 156 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `appD_2_sunity_devee_n_questions` | Appendix D | 29.0000 | 39 | 10.0000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 29.0000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `appD_2_ebers_n_questions` | Appendix D | 48.7000 | 39 | 9.7000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 48.7000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `appD_2_keckley_n_questions` | Appendix D | 48.7000 | 39 | 9.7000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 48.7000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `appD_2_yung_wing_n_questions` | Appendix D | 48.7000 | 39 | 9.7000 |   | C5_baseline vs C4a_full_facts_plus_spec, per-question | replace paper 48.7000 with scaffold 39 (emit script: _v11_emit_appendix_d.py) |
| `4_2_1_C8_vs_C2a_worse_n` | §4.2 + §4.2.1 | 115.0000 | 108 | 7.0000 |   | C8 < C2a | replace paper 115.0000 with scaffold 108 (emit script: _v11_emit_4_2_compression.py) |
| `4_5_hamerton_letta_unique_named_entities` | §4.5 + Appendix F | 19.0000 | 26 | 7.0000 |   | Referential density: Letta block | replace paper 19.0000 with scaffold 26 (emit script: _v11_emit_4_5_letta.py) |
| `4_5_babur_bl_unique_named_entities` | §4.5 + Appendix F | 58.0000 | 65 | 7.0000 |   | Referential density: BL spec | replace paper 58.0000 with scaffold 65 (emit script: _v11_emit_4_5_letta.py) |
| `4_4_2_mem0_hurts_n` | paper.4.4.2_4.4.3 | 39.0000 | 45 | 6.0000 |   | C3_mem0 − C1_mem0 | replace paper 39.0000 with scaffold 45 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_zep_hurts_n` | paper.4.4.2_4.4.3 | 24.0000 | 30 | 6.0000 |   | C3_zep − C1_zep | replace paper 24.0000 with scaffold 30 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_2_1_low_baseline_C4_worsen_pct` | §4.2 + §4.2.1 | 9.0000 | 14.5299 | 5.5299 |   | C4 vs C5 | replace paper 9.0000 with scaffold 14.5299 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_2_spec_helps_n` | paper.4.4.2_4.4.3 | 52.0000 | 57 | 5.0000 |   | C3_supermemory − C1_supermemory | replace paper 52.0000 with scaffold 57 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_supermemory_helps_n` | paper.4.4.2_4.4.3 | 52.0000 | 57 | 5.0000 |   | C3_supermemory − C1_supermemory | replace paper 52.0000 with scaffold 57 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_5_ebers_letta_unique_named_entities` | §4.5 + Appendix F | 58.0000 | 53 | 5.0000 |   | Referential density: Letta block | replace paper 58.0000 with scaffold 53 (emit script: _v11_emit_4_5_letta.py) |
| `4_2_1_low_baseline_C8_worsen_pct` | §4.2 + §4.2.1 | 9.0000 | 12.2507 | 3.2507 |   | C8 vs C5 | replace paper 9.0000 with scaffold 12.2507 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_1_C8_vs_C2a_better_n` | §4.2 + §4.2.1 | 190.0000 | 187 | 3.0000 |   | C8 > C2a | replace paper 190.0000 with scaffold 187 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_1_C9_vs_C4a_tie_n` | §4.2 + §4.2.1 | 42.0000 | 45 | 3.0000 |   | C9 = C4a | replace paper 42.0000 with scaffold 45 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_2_letta_archival_hurts_n` | paper.4.4.2_4.4.3 | 39.0000 | 36 | 3.0000 |   | C3_letta − C1_letta | replace paper 39.0000 with scaffold 36 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_5_hamerton_bl_unique_named_entities` | §4.5 + Appendix F | 19.0000 | 22 | 3.0000 |   | Referential density: BL spec | replace paper 19.0000 with scaffold 22 (emit script: _v11_emit_4_5_letta.py) |
| `4_2_1_C8_vs_C2a_worse_pct` | §4.2 + §4.2.1 | 32.8000 | 30.7692 | 2.0308 |   | C8 < C2a | replace paper 32.8000 with scaffold 30.7692 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_hamerton_compression_ratio` | §4.2 + §4.2.1 | 5.0000 | 7 | 2.0000 |   |  | replace paper 5.0000 with scaffold 7 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_bernal_diaz_compression_ratio` | §4.2 + §4.2.1 | 35.0000 | 33 | 2.0000 |   |  | replace paper 35.0000 with scaffold 33 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_1_C9_vs_C4a_better_n` | §4.2 + §4.2.1 | 155.0000 | 153 | 2.0000 |   | C9 > C4a | replace paper 155.0000 with scaffold 153 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_1_mem0_native_low_baseline_n_positive` | paper.4.4.1 | 9.0000 | 7 | 2.0000 |   | C3_mem0_fp − C1_mem0_fp | replace paper 9.0000 with scaffold 7 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_2_1_C8_vs_C2a_tie_n` | §4.2 + §4.2.1 | 54.1000 | 56 | 1.9000 |   | C8 = C2a | replace paper 54.1000 with scaffold 56 (emit script: _v11_emit_4_2_compression.py) |
| `3_2_franklin_C4a_5judge` | 3 | 2.3400 | 3.6450 | 1.3050 |   | C4a_full_facts_plus_spec | replace paper 2.3400 with scaffold 3.6450 (emit script: _v11_emit_3_study_design.py) |
| `4_5_ebers_letta_block_score_haiku` | §4.5 + Appendix F | 1.4800 | 2.7600 | 1.2800 |   | Letta block -> Haiku, 5-judge primary panel | replace paper 1.4800 with scaffold 2.7600 (emit script: _v11_emit_4_5_letta.py) |
| `3_7_2_gemini_pro_verbatim` | 3 | 5.4000 | 4.1500 | 1.2500 |   | diagnostic test (verbatim) | replace paper 5.4000 with scaffold 4.1500 (emit script: _v11_emit_3_study_design.py) |
| `3_2_franklin_C2a_5judge` | 3 | 2.3400 | 3.3700 | 1.0300 |   | C2a_full_spec | replace paper 2.3400 with scaffold 3.3700 (emit script: _v11_emit_3_study_design.py) |
| `4_2_ebers_compression_ratio` | §4.2 + §4.2.1 | 18.0000 | 17 | 1.0000 |   |  | replace paper 18.0000 with scaffold 17 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_babur_compression_ratio` | §4.2 + §4.2.1 | 78.0000 | 79 | 1.0000 |   |  | replace paper 78.0000 with scaffold 79 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_yung_wing_compression_ratio` | §4.2 + §4.2.1 | 12.0000 | 13 | 1.0000 |   |  | replace paper 12.0000 with scaffold 13 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_table_mean_C9_n_rows` | §4.2 + §4.2.1 | 9.0000 | 8 | 1.0000 |   |  | replace paper 9.0000 with scaffold 8 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_1_C9_vs_C4a_worse_n` | §4.2 + §4.2.1 | 115.0000 | 114 | 1.0000 |   | C9 < C4a | replace paper 115.0000 with scaffold 114 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_1_letta_archival_controlled_low_baseline_n_positive` | paper.4.4.1 | 9.0000 | 8 | 1.0000 |   | C3_letta − C1_letta | replace paper 9.0000 with scaffold 8 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_4_1_supermemory_controlled_all14_n_positive` | paper.4.4.1 | 6.0000 | 7 | 1.0000 |   | C3_supermemory − C1_supermemory | replace paper 6.0000 with scaffold 7 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_4_2_spec_hurts_n` | paper.4.4.2_4.4.3 | 52.0000 | 53 | 1.0000 |   | C3_supermemory − C1_supermemory | replace paper 52.0000 with scaffold 53 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_supermemory_hurts_n` | paper.4.4.2_4.4.3 | 52.0000 | 53 | 1.0000 |   | C3_supermemory − C1_supermemory | replace paper 52.0000 with scaffold 53 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appB_5_rousseau_refusal_triggering_delta` | Appendix B | 1.7100 | 0.7200 | 0.9900 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 0.7200 (emit script: _v11_emit_appendix_b_battery.py) |
| `appB_5_seacole_interpretive_inference_delta` | Appendix B | 1.7100 | 0.7929 | 0.9171 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 0.7929 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_3_bernal_diaz_c2c_v2_delta` | §4.3 | -0.2000 | 0.6876 | 0.8876 | YES | C2c_wrong_spec_v2 vs C5_baseline | replace paper -0.2000 with scaffold 0.6876 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `appB_5_fukuzawa_interpretive_inference_delta` | Appendix B | 1.7100 | 0.8296 | 0.8804 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 0.8296 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_2_1_all14_C8_worsen_pct` | §4.2 + §4.2.1 | 24.5000 | 23.6264 | 0.8736 |   | C8 vs C5 | replace paper 24.5000 with scaffold 23.6264 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_1_C8_vs_C2a_better_pct` | §4.2 + §4.2.1 | 54.1000 | 53.2764 | 0.8236 |   | C8 > C2a | replace paper 54.1000 with scaffold 53.2764 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_1_supermemory_native_wilcoxon_p` | paper.4.4.1 | -0.0100 | 0.8077 | 0.8177 | YES | C3_supermemory_fp − C1_supermemory_fp | replace paper -0.0100 with scaffold 0.8077 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_3_ebers_c2c_v2_delta` | §4.3 | 1.6000 | 0.7895 | 0.8105 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 1.6000 with scaffold 0.7895 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_5_ebers_bl_unified_brief_score_haiku_7judge` | §4.5 + Appendix F | 1.4800 | 2.2536 | 0.7736 |   | BL unified -> Haiku, 7-judge sensitivity | replace paper 1.4800 with scaffold 2.2536 (emit script: _v11_emit_4_5_letta.py) |
| `4_3_equiano_c2c_v2_delta` | §4.3 | -0.2500 | -0.9992 | 0.7492 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper -0.2500 with scaffold -0.9992 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_1_summary_regression_level_slope` | §4.1 cross-subject gradient | -0.6700 | 0.0403 | 0.7103 | YES | C4a vs C5 | replace paper -0.6700 with scaffold 0.0403 (emit script: _v11_emit_4_1_gradient.py) |
| `4_2_1_all14_C8_improve_pct` | §4.2 + §4.2.1 | 64.5000 | 65.2015 | 0.7015 |   | C8 vs C5 | replace paper 64.5000 with scaffold 65.2015 (emit script: _v11_emit_4_2_compression.py) |
| `3_7_2_gemini_flash_paraphrased` | 3 | 5.4000 | 4.7000 | 0.7000 |   | diagnostic test (paraphrased) | replace paper 5.4000 with scaffold 4.7000 (emit script: _v11_emit_3_study_design.py) |
| `4_4_3_keckley_q21_mem0_delta` | paper.4.4.2_4.4.3 | -0.5000 | 0.2000 | 0.7000 | YES | C3_mem0 − C1_mem0 | replace paper -0.5000 with scaffold 0.2000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_zep_delta` | paper.4.4.2_4.4.3 | -0.5000 | 0.2000 | 0.7000 | YES | C3_zep − C1_zep | replace paper -0.5000 with scaffold 0.2000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_1_summary_regression_level_r_squared` | §4.1 cross-subject gradient | -0.6700 | 0.0078 | 0.6778 | YES | C4a vs C5 | replace paper -0.6700 with scaffold 0.0078 (emit script: _v11_emit_4_1_gradient.py) |
| `4_1_summary_regression_delta_p` | §4.1 cross-subject gradient | -0.6700 | 9.017e-06 | 0.6700 | YES | delta_C4a vs C5 | replace paper -0.6700 with scaffold 9.017e-06 (emit script: _v11_emit_4_1_gradient.py) |
| `4_2_1_C9_vs_C4a_better_pct` | §4.2 + §4.2.1 | 49.7000 | 49.0385 | 0.6615 |   | C9 > C4a | replace paper 49.7000 with scaffold 49.0385 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_fukuzawa_c2c_v2_delta` | §4.3 | 0.2200 | 0.8647 | 0.6447 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.8647 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_1_summary_regression_level_ci_high` | §4.1 cross-subject gradient | 0.9500 | 0.3253 | 0.6247 |   | C4a vs C5 | replace paper 0.9500 with scaffold 0.3253 (emit script: _v11_emit_4_1_gradient.py) |
| `4_3_cellini_c2c_v2_delta` | §4.3 | -0.2500 | -0.8745 | 0.6245 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper -0.2500 with scaffold -0.8745 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_seacole_delta_C9_minus_C5` | §4.2 + §4.2.1 | 0.3500 | 0.9590 | 0.6090 |   | C9 vs C5 | replace paper 0.3500 with scaffold 0.9590 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_3_keckley_q21_letta_archival_delta` | paper.4.4.2_4.4.3 | 1.0000 | 0.4000 | 0.6000 |   | C3_letta − C1_letta | replace paper 1.0000 with scaffold 0.4000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_3_rousseau_c2c_v2_delta` | §4.3 | 0.2200 | -0.3659 | 0.5859 | YES | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold -0.3659 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_keckley_delta_C9_minus_C5` | §4.2 + §4.2.1 | 0.0700 | 0.6462 | 0.5762 |   | C9 vs C5 | replace paper 0.0700 with scaffold 0.6462 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_yung_wing_c2c_v1_delta` | §4.3 | -0.2500 | 0.3231 | 0.5731 | YES | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold 0.3231 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_fukuzawa_delta_C9_minus_C5` | §4.2 + §4.2.1 | 1.6700 | 1.1077 | 0.5623 |   | C9 vs C5 | replace paper 1.6700 with scaffold 1.1077 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_bernal_diaz_delta_C9_minus_C5` | §4.2 + §4.2.1 | 0.2800 | 0.8410 | 0.5610 |   | C9 vs C5 | replace paper 0.2800 with scaffold 0.8410 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_ebers_c2c_v1_delta` | §4.3 | -0.2500 | 0.2974 | 0.5474 | YES | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold 0.2974 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_4_2_spec_helps_mean_swing` | paper.4.4.2_4.4.3 | 1.0000 | 1.5474 | 0.5474 |   | C3_supermemory − C1_supermemory | replace paper 1.0000 with scaffold 1.5474 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_supermemory_helps_mean_swing` | paper.4.4.2_4.4.3 | 1.0000 | 1.5474 | 0.5474 |   | C3_supermemory − C1_supermemory | replace paper 1.0000 with scaffold 1.5474 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_3_equiano_c2c_v1_delta` | §4.3 | -0.2500 | -0.7949 | 0.5449 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.7949 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_3_babur_c2c_v2_delta` | §4.3 | 0.2200 | 0.7560 | 0.5360 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.7560 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_3_sunity_devee_c2c_v1_delta` | §4.3 | -0.2500 | 0.2667 | 0.5167 | YES | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold 0.2667 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_4_2_zep_helps_mean_swing` | paper.4.4.2_4.4.3 | 1.0000 | 1.5122 | 0.5122 |   | C3_zep − C1_zep | replace paper 1.0000 with scaffold 1.5122 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_3_fukuzawa_c2c_v1_delta` | §4.3 | -0.2500 | 0.2615 | 0.5115 | YES | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold 0.2615 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_3_wrong_spec_detection_ambiguous_pct` | §4.3 | 0.3500 | 0.8518 | 0.5018 |   | ambiguous / total | replace paper 0.3500 with scaffold 0.8518 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_5_ebers_letta_block_score_haiku_7judge` | §4.5 + Appendix F | 2.5000 | 3.0000 | 0.5000 |   | Letta block -> Haiku, 7-judge sensitivity | replace paper 2.5000 with scaffold 3.0000 (emit script: _v11_emit_4_5_letta.py) |
| `appB_6_delta_max` | Appendix B | 1.8500 | 1.3744 | 0.4756 |   | C2a_full_spec vs C5_baseline | replace paper 1.8500 with scaffold 1.3744 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_4_3_keckley_q21_letta_archival_c3` | paper.4.4.2_4.4.3 | 1.3300 | 1.8000 | 0.4700 |   | C3_letta − C1_letta | replace paper 1.3300 with scaffold 1.8000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_letta_archival_helps_mean_swing` | paper.4.4.2_4.4.3 | 2.0000 | 1.5356 | 0.4644 |   | C3_letta − C1_letta | replace paper 2.0000 with scaffold 1.5356 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `3_7_6_length_corr_C5` | 3 | 0.1400 | 0.6037 | 0.4637 |   | C5_baseline | replace paper 0.1400 with scaffold 0.6037 (emit script: _v11_emit_3_study_design.py) |
| `appB_5_cellini_literal_recall_delta` | Appendix B | 1.7100 | 1.2500 | 0.4600 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.2500 (emit script: _v11_emit_appendix_b_battery.py) |
| `appB_5_hamerton_refusal_triggering_delta` | Appendix B | 1.7100 | 1.2526 | 0.4574 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.2526 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_4_2_baselayer_helps_mean_swing` | paper.4.4.2_4.4.3 | 1.0000 | 1.4563 | 0.4563 |   | C3_baselayer − C1_baselayer | replace paper 1.0000 with scaffold 1.4563 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_zep_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.4400 | 0.4400 |   | C3_zep − C1_zep | replace paper -1.0000 with scaffold -1.4400 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_1_summary_low_baseline_mean_C4a` | §4.1 cross-subject gradient | 2.0000 | 2.4393 | 0.4393 |   | C4a | replace paper 2.0000 with scaffold 2.4393 (emit script: _v11_emit_4_1_gradient.py) |
| `4_2_hamerton_delta_C9_minus_C5` | §4.2 + §4.2.1 | 2.2700 | 1.8308 | 0.4392 |   | C9 vs C5 | replace paper 2.2700 with scaffold 1.8308 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_zitkala_sa_c2c_v1_delta` | §4.3 | -0.2500 | -0.6769 | 0.4269 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.6769 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_yung_wing_delta_C9_minus_C5` | §4.2 + §4.2.1 | 0.2000 | 0.6256 | 0.4256 |   | C9 vs C5 | replace paper 0.2000 with scaffold 0.6256 (emit script: _v11_emit_4_2_compression.py) |
| `4_1_summary_regression_level_ci_low` | §4.1 cross-subject gradient | -0.6700 | -0.2447 | 0.4253 |   | C4a vs C5 | replace paper -0.6700 with scaffold -0.2447 (emit script: _v11_emit_4_1_gradient.py) |
| `4_4_2_mem0_helps_mean_swing` | paper.4.4.2_4.4.3 | 1.0000 | 1.4149 | 0.4149 |   | C3_mem0 − C1_mem0 | replace paper 1.0000 with scaffold 1.4149 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appB_5_hamerton_interpretive_inference_delta` | Appendix B | 1.7100 | 1.3000 | 0.4100 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.3000 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_2_sunity_devee_delta_C9_minus_C5` | §4.2 + §4.2.1 | 1.0300 | 1.4359 | 0.4059 |   | C9 vs C5 | replace paper 1.0300 with scaffold 1.4359 (emit script: _v11_emit_4_2_compression.py) |
| `3_7_6_mid_score_chars_avg` | 3 | 2829.0000 | 2829.4000 | 0.4000 |   | 2.5 <= score < 3.5 | replace paper 2829.0000 with scaffold 2829.4000 (emit script: _v11_emit_3_study_design.py) |
| `appD_3_5_mid_range_chars` | Appendix D | 2829.0000 | 2829.4000 | 0.4000 |   |  | replace paper 2829.0000 with scaffold 2829.4000 (emit script: _v11_emit_appendix_d.py) |
| `3_7_2_gemini_flash_verbatim` | 3 | 5.4000 | 5.0000 | 0.4000 |   | diagnostic test (verbatim) | replace paper 5.4000 with scaffold 5.0000 (emit script: _v11_emit_3_study_design.py) |
| `4_4_2_spec_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.3811 | 0.3811 |   | C3_supermemory − C1_supermemory | replace paper -1.0000 with scaffold -1.3811 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_2_supermemory_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.3811 | 0.3811 |   | C3_supermemory − C1_supermemory | replace paper -1.0000 with scaffold -1.3811 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `appD_3_2_abstention_pct_above_3` | Appendix D | 3.5000 | 3.1250 | 0.3750 |   | abstention rows, score >= 3.0 | replace paper 3.5000 with scaffold 3.1250 (emit script: _v11_emit_appendix_d.py) |
| `4_2_1_C9_vs_C4a_worse_pct` | §4.2 + §4.2.1 | 36.9000 | 36.5385 | 0.3615 |   | C9 < C4a | replace paper 36.9000 with scaffold 36.5385 (emit script: _v11_emit_4_2_compression.py) |
| `appB_5_sunity_devee_refusal_triggering_delta` | Appendix B | 1.7100 | 1.3500 | 0.3600 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.3500 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_3_babur_c2c_v1_delta` | §4.3 | -0.2500 | -0.5897 | 0.3397 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.5897 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_1_summary_all14_mean_delta_C4a` | §4.1 cross-subject gradient | 0.8900 | 0.5516 | 0.3384 |   | delta_C4a | replace paper 0.8900 with scaffold 0.5516 (emit script: _v11_emit_4_1_gradient.py) |
| `appB_5_sunity_devee_literal_recall_delta` | Appendix B | 1.7100 | 1.3750 | 0.3350 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.3750 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_4_2_letta_archival_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.3333 | 0.3333 |   | C3_letta − C1_letta | replace paper -1.0000 with scaffold -1.3333 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_2_1_low_baseline_C8_improve_pct` | §4.2 + §4.2.1 | 78.3000 | 78.6325 | 0.3325 |   | C8 vs C5 | replace paper 78.3000 with scaffold 78.6325 (emit script: _v11_emit_4_2_compression.py) |
| `4_4_3_keckley_q21_supermemory_delta` | paper.4.4.2_4.4.3 | -2.3300 | -2.0000 | 0.3300 |   | C3_supermemory − C1_supermemory | replace paper -2.3300 with scaffold -2.0000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_3_seacole_c2c_v2_delta` | §4.3 | 0.2200 | -0.1044 | 0.3244 | YES | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold -0.1044 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_3_sunity_devee_c2c_v2_delta` | §4.3 | 0.2200 | 0.5349 | 0.3149 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.5349 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_3_cellini_c2c_v1_delta` | §4.3 | -0.2500 | -0.5641 | 0.3141 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.5641 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `appB_5_yung_wing_literal_recall_delta` | Appendix B | 1.7100 | 1.4000 | 0.3100 |   | C2a_full_spec vs C5_baseline | replace paper 1.7100 with scaffold 1.4000 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_5_babur_delta_letta_minus_bl_7judge` | §4.5 + Appendix F | 0.5400 | 0.2321 | 0.3079 |   | Letta - BL unified, 7-judge sensitivity | replace paper 0.5400 with scaffold 0.2321 (emit script: _v11_emit_4_5_letta.py) |
| `4_3_bernal_diaz_c2c_v1_delta` | §4.3 | -0.2000 | 0.0923 | 0.2923 | YES | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2000 with scaffold 0.0923 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_5_babur_block_duplication_rate` | §4.5 + Appendix F | 0.5400 | 0.2540 | 0.2860 |   | Babur block duplication rate | replace paper 0.5400 with scaffold 0.2540 (emit script: _v11_emit_4_5_letta.py) |
| `4_4_2_mem0_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.2800 | 0.2800 |   | C3_mem0 − C1_mem0 | replace paper -1.0000 with scaffold -1.2800 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_5_ebers_delta_letta_minus_bl_7judge` | §4.5 + Appendix F | 1.0200 | 0.7464 | 0.2736 |   | Letta - BL unified, 7-judge sensitivity | replace paper 1.0200 with scaffold 0.7464 (emit script: _v11_emit_4_5_letta.py) |
| `4_3_rousseau_c2c_v1_delta` | §4.3 | -0.2500 | -0.5231 | 0.2731 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.5231 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_4_2_baselayer_hurts_mean_swing` | paper.4.4.2_4.4.3 | -1.0000 | -1.2667 | 0.2667 |   | C3_baselayer − C1_baselayer | replace paper -1.0000 with scaffold -1.2667 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_1_letta_archival_native_wilcoxon_p` | paper.4.4.1 | 0.2000 | 0.4629 | 0.2629 |   | C3_letta_fp − C1_letta_fp | replace paper 0.2000 with scaffold 0.4629 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_3_correct_minus_adversarial_gap` | §4.3 | 0.3500 | 0.6008 | 0.2508 |   | C2a_full_spec vs C2c_wrong_spec (v1 adversarial) | replace paper 0.3500 with scaffold 0.6008 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_5_babur_letta_block_score_haiku_7judge` | §4.5 + Appendix F | 2.4200 | 2.6679 | 0.2479 |   | Letta block -> Haiku, 7-judge sensitivity | replace paper 2.4200 with scaffold 2.6679 (emit script: _v11_emit_4_5_letta.py) |
| `4_3_keckley_c2c_v1_delta` | §4.3 | -0.2500 | -0.4872 | 0.2372 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.4872 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_5_ebers_bl_unified_brief_score_haiku` | §4.5 + Appendix F | 1.4800 | 1.7150 | 0.2350 |   | BL unified brief -> Haiku, 5-judge primary panel | replace paper 1.4800 with scaffold 1.7150 (emit script: _v11_emit_4_5_letta.py) |
| `3_7_6_abstention_mean_score` | 3 | 1.5000 | 1.2698 | 0.2302 |   | abstention rows | replace paper 1.5000 with scaffold 1.2698 (emit script: _v11_emit_3_study_design.py) |
| `4_4_3_keckley_q21_supermemory_c1` | paper.4.4.2_4.4.3 | 3.8300 | 3.6000 | 0.2300 |   | C3_supermemory − C1_supermemory | replace paper 3.8300 with scaffold 3.6000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `3_2_franklin_C5_7judge_min` | 3 | 3.7000 | 3.4750 | 0.2250 |   | C5_baseline, judge-level | replace paper 3.7000 with scaffold 3.4750 (emit script: _v11_emit_3_study_design.py) |
| `4_3_augustine_c2c_v1_delta` | §4.3 | -0.2500 | -0.4718 | 0.2218 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.4718 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `3_7_2_strictness_opus` | 3 | 1.2000 | 1.4115 | 0.2115 |   | abstention rows only | replace paper 1.2000 with scaffold 1.4115 (emit script: _v11_emit_3_study_design.py) |
| `4_4_3_keckley_q21_baselayer_c3` | paper.4.4.2_4.4.3 | 1.0000 | 1.2000 | 0.2000 |   | C3_baselayer − C1_baselayer | replace paper 1.0000 with scaffold 1.2000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_1_summary_regression_level_p` | §4.1 cross-subject gradient | 0.9500 | 0.7633 | 0.1867 |   | C4a vs C5 | replace paper 0.9500 with scaffold 0.7633 (emit script: _v11_emit_4_1_gradient.py) |
| `4_5_ebers_fullstack_delta_letta_minus_bl` | §4.5 + Appendix F | 1.0200 | 1.2050 | 0.1850 |   | Letta - BL full-stack, 5-judge primary | replace paper 1.0200 with scaffold 1.2050 (emit script: _v11_emit_4_5_letta.py) |
| `4_3_zitkala_sa_c2c_v2_delta` | §4.3 | 0.2200 | 0.0365 | 0.1835 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.0365 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `3_2_franklin_C5_7judge_max` | 3 | 4.1000 | 4.2750 | 0.1750 |   | C5_baseline, judge-level | replace paper 4.1000 with scaffold 4.2750 (emit script: _v11_emit_3_study_design.py) |
| `4_3_yung_wing_c2c_v2_delta` | §4.3 | 0.2200 | 0.3931 | 0.1731 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.3931 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_4_1_zep_controlled_wilcoxon_p` | paper.4.4.1 | 0.1700 | 3.662e-04 | 0.1696 |   | C3_zep − C1_zep | replace paper 0.1700 with scaffold 3.662e-04 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_4_1_zep_native_wilcoxon_p` | paper.4.4.1 | 0.1700 | 0.0015 | 0.1685 |   | C3_zep_fp − C1_zep_fp | replace paper 0.1700 with scaffold 0.0015 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_5_babur_fullstack_delta_letta_minus_bl` | §4.5 + Appendix F | 0.5400 | 0.3800 | 0.1600 |   | Letta - BL full-stack, 5-judge primary | replace paper 0.5400 with scaffold 0.3800 (emit script: _v11_emit_4_5_letta.py) |
| `4_5_babur_fullstack_bl_score_haiku` | §4.5 + Appendix F | 1.8800 | 2.0350 | 0.1550 |   | BL full-stack named -> Haiku, 5-judge primary | replace paper 1.8800 with scaffold 2.0350 (emit script: _v11_emit_4_5_letta.py) |
| `4_2_ebers_corpus_lift` | §4.2 + §4.2.1 | 1.0200 | 1.1641 | 0.1441 |   | C8 vs C5 | replace paper 1.0200 with scaffold 1.1641 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_low_baseline_C9_minus_C8_mean` | §4.2 + §4.2.1 | 0.2200 | 0.0859 | 0.1341 |   | C9 vs C8 | replace paper 0.2200 with scaffold 0.0859 (emit script: _v11_emit_4_2_compression.py) |
| `4_1_summary_regression_delta_r_squared` | §4.1 cross-subject gradient | 0.9500 | 0.8177 | 0.1323 |   | delta_C4a vs C5 | replace paper 0.9500 with scaffold 0.8177 (emit script: _v11_emit_4_1_gradient.py) |
| `4_5_hamerton_fullstack_delta_letta_minus_bl` | §4.5 + Appendix F | 0.1400 | 0.2718 | 0.1318 |   | Letta - BL full-stack, 5-judge primary | replace paper 0.1400 with scaffold 0.2718 (emit script: _v11_emit_4_5_letta.py) |
| `4_4_3_keckley_q21_zep_c1` | paper.4.4.2_4.4.3 | 1.3300 | 1.2000 | 0.1300 |   | C3_zep − C1_zep | replace paper 1.3300 with scaffold 1.2000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_baselayer_delta` | paper.4.4.2_4.4.3 | -2.3300 | -2.2000 | 0.1300 |   | C3_baselayer − C1_baselayer | replace paper -2.3300 with scaffold -2.2000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_5_hamerton_fullstack_bl_score_haiku` | §4.5 + Appendix F | 2.9600 | 2.8308 | 0.1292 |   | BL full-stack named -> Haiku, 5-judge primary | replace paper 2.9600 with scaffold 2.8308 (emit script: _v11_emit_4_5_letta.py) |
| `4_2_ebers_delta_C9_minus_C5` | §4.2 + §4.2.1 | 1.0200 | 1.1436 | 0.1236 |   | C9 vs C5 | replace paper 1.0200 with scaffold 1.1436 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_ebers_spec_lift` | §4.2 + §4.2.1 | 0.6400 | 0.5179 | 0.1221 |   | C2a vs C5 | replace paper 0.6400 with scaffold 0.5179 (emit script: _v11_emit_4_2_compression.py) |
| `appB_6_interpretive_inference_corr_with_delta` | Appendix B | -0.5820 | -0.4656 | 0.1164 |   | C2a_full_spec vs C5_baseline | replace paper -0.5820 with scaffold -0.4656 (emit script: _v11_emit_appendix_b_battery.py) |
| `3_7_6_length_corr_overall` | 3 | 0.1400 | 0.2564 | 0.1164 |   | all conditions, all 9 low-baseline subjects | replace paper 0.1400 with scaffold 0.2564 (emit script: _v11_emit_3_study_design.py) |
| `appB_6_refusal_triggering_corr_with_delta` | Appendix B | 0.3210 | 0.2118 | 0.1092 |   | C2a_full_spec vs C5_baseline | replace paper 0.3210 with scaffold 0.2118 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_5_hamerton_letta_block_score_haiku_7judge` | §4.5 + Appendix F | 3.1000 | 3.2088 | 0.1088 |   | Letta block -> Haiku, 7-judge sensitivity | replace paper 3.1000 with scaffold 3.2088 (emit script: _v11_emit_4_5_letta.py) |
| `4_4_3_keckley_q21_mem0_c3` | paper.4.4.2_4.4.3 | 1.5000 | 1.6000 | 0.1000 |   | C3_mem0 − C1_mem0 | replace paper 1.5000 with scaffold 1.6000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_supermemory_c3` | paper.4.4.2_4.4.3 | 1.5000 | 1.6000 | 0.1000 |   | C3_supermemory − C1_supermemory | replace paper 1.5000 with scaffold 1.6000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_2_table_mean_C8_minus_C2a` | §4.2 + §4.2.1 | 0.3280 | 0.2285 | 0.0995 |   |  | replace paper 0.3280 with scaffold 0.2285 (emit script: _v11_emit_4_2_compression.py) |
| `4_2_low_baseline_C8_minus_C2a_mean` | §4.2 + §4.2.1 | 0.3280 | 0.2285 | 0.0995 |   | C8 vs C2a | replace paper 0.3280 with scaffold 0.2285 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_augustine_c2c_v2_delta` | §4.3 | 0.2200 | 0.1254 | 0.0946 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.1254 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_2_table_mean_C9` | §4.2 + §4.2.1 | 2.5000 | 2.5942 | 0.0942 |   |  | replace paper 2.5000 with scaffold 2.5942 (emit script: _v11_emit_4_2_compression.py) |
| `4_3_seacole_c2c_v1_delta` | §4.3 | -0.2500 | -0.3436 | 0.0936 |   | C2c_wrong_spec (v1 adversarial) vs C5_baseline | replace paper -0.2500 with scaffold -0.3436 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `4_4_1_mem0_native_wilcoxon_p` | paper.4.4.1 | 0.1000 | 0.0088 | 0.0912 |   | C3_mem0_fp − C1_mem0_fp | replace paper 0.1000 with scaffold 0.0088 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `3_7_6_high_score_chars_avg` | 3 | 2790.0000 | 2790.0909 | 0.0909 |   | score >= 4.5 | replace paper 2790.0000 with scaffold 2790.0909 (emit script: _v11_emit_3_study_design.py) |
| `appD_3_5_ultra_high_chars` | Appendix D | 2790.0000 | 2790.0909 | 0.0909 |   |  | replace paper 2790.0000 with scaffold 2790.0909 (emit script: _v11_emit_appendix_d.py) |
| `4_2_low_baseline_corpus_lift_mean` | §4.2 + §4.2.1 | 1.0000 | 0.9134 | 0.0866 |   | C8 vs C5 (subject-mean lift) | replace paper 1.0000 with scaffold 0.9134 (emit script: _v11_emit_4_2_compression.py) |
| `3_7_2_strictness_haiku` | 3 | 1.2000 | 1.2865 | 0.0865 |   | abstention rows only | replace paper 1.2000 with scaffold 1.2865 (emit script: _v11_emit_3_study_design.py) |
| `4_4_1_mem0_controlled_wilcoxon_p` | paper.4.4.1 | 0.1000 | 0.0166 | 0.0834 |   | C3_mem0 − C1_mem0 | replace paper 0.1000 with scaffold 0.0166 (emit script: _v11_emit_4_4_1_memory_systems.py) |
| `4_3_keckley_c2c_v2_delta` | §4.3 | 0.2200 | 0.1390 | 0.0810 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.1390 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `3_7_6_abstention_pct_above_3` | 3 | 3.2000 | 3.1250 | 0.0750 |   | abstention rows, score >= 3.0 | replace paper 3.2000 with scaffold 3.1250 (emit script: _v11_emit_3_study_design.py) |
| `4_5_ebers_fullstack_bl_score_haiku` | §4.5 + Appendix F | 1.4800 | 1.5550 | 0.0750 |   | BL full-stack named -> Haiku, 5-judge primary | replace paper 1.4800 with scaffold 1.5550 (emit script: _v11_emit_4_5_letta.py) |
| `appB_4_refusal_triggering_mean_delta_spec` | Appendix B | 0.4890 | 0.4167 | 0.0723 |   | C2a_full_spec vs C5_baseline | replace paper 0.4890 with scaffold 0.4167 (emit script: _v11_emit_appendix_b_battery.py) |
| `4_4_3_keckley_q21_baselayer_c1` | paper.4.4.2_4.4.3 | 3.3300 | 3.4000 | 0.0700 |   | C3_baselayer − C1_baselayer | replace paper 3.3300 with scaffold 3.4000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_letta_archival_c1` | paper.4.4.2_4.4.3 | 1.3300 | 1.4000 | 0.0700 |   | C3_letta − C1_letta | replace paper 1.3300 with scaffold 1.4000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_mem0_c1` | paper.4.4.2_4.4.3 | 1.3300 | 1.4000 | 0.0700 |   | C3_mem0 − C1_mem0 | replace paper 1.3300 with scaffold 1.4000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_4_3_keckley_q21_zep_c3` | paper.4.4.2_4.4.3 | 1.3300 | 1.4000 | 0.0700 |   | C3_zep − C1_zep | replace paper 1.3300 with scaffold 1.4000 (emit script: _v11_emit_4_4_2_4_4_3_mechanisms_keckley.py) |
| `4_3_random_derangement_delta_13globals` | §4.3 | 0.2200 | 0.1525 | 0.0675 |   | C2c_wrong_spec_v2 vs C5_baseline | replace paper 0.2200 with scaffold 0.1525 (emit script: _v11_emit_4_3_wrong_spec.py) |
| `3_7_2_strictness_sonnet` | 3 | 1.2000 | 1.1406 | 0.0594 |   | abstention rows only | replace paper 1.2000 with scaffold 1.1406 (emit script: _v11_emit_3_study_design.py) |
| `appB_6_literal_recall_corr_with_delta` | Appendix B | 0.6460 | 0.5949 | 0.0511 |   | C2a_full_spec vs C5_baseline | replace paper 0.6460 with scaffold 0.5949 (emit script: _v11_emit_appendix_b_battery.py) |

## Sign flips and direction changes

| claim_id | section | paper | scaffold | abs_delta | estimand |
|---|---|---:|---:|---:|---|
| `4_1_summary_regression_delta_p` | §4.1 cross-subject gradient | -0.6700 | 9.017e-06 | 0.6700 | Regression slope p-value (delta) |
| `4_1_summary_regression_level_slope` | §4.1 cross-subject gradient | -0.6700 | 0.0403 | 0.7103 | Level regression slope (C4a on C5) |
| `4_1_summary_regression_level_r_squared` | §4.1 cross-subject gradient | -0.6700 | 0.0078 | 0.6778 | Level R^2 |
| `4_3_bernal_diaz_c2c_v1_delta` | §4.3 | -0.2000 | 0.0923 | 0.2923 | Bernal Diaz per-subject (C2c_wrong_spec - C5_baseline) (5-judge primary). |
| `4_3_bernal_diaz_c2c_v2_delta` | §4.3 | -0.2000 | 0.6876 | 0.8876 | Bernal Diaz per-subject (C2c_wrong_spec_v2 - C5_baseline) (5-judge primary). |
| `4_3_ebers_c2c_v1_delta` | §4.3 | -0.2500 | 0.2974 | 0.5474 | Ebers per-subject (C2c_wrong_spec - C5_baseline) (5-judge primary). |
| `4_3_fukuzawa_c2c_v1_delta` | §4.3 | -0.2500 | 0.2615 | 0.5115 | Fukuzawa per-subject (C2c_wrong_spec - C5_baseline) (5-judge primary). |
| `4_3_rousseau_c2c_v2_delta` | §4.3 | 0.2200 | -0.3659 | 0.5859 | Rousseau per-subject (C2c_wrong_spec_v2 - C5_baseline) (5-judge primary). |
| `4_3_seacole_c2c_v2_delta` | §4.3 | 0.2200 | -0.1044 | 0.3244 | Seacole per-subject (C2c_wrong_spec_v2 - C5_baseline) (5-judge primary). |
| `4_3_sunity_devee_c2c_v1_delta` | §4.3 | -0.2500 | 0.2667 | 0.5167 | Sunity Devee per-subject (C2c_wrong_spec - C5_baseline) (5-judge primary). |
| `4_3_yung_wing_c2c_v1_delta` | §4.3 | -0.2500 | 0.3231 | 0.5731 | Yung Wing per-subject (C2c_wrong_spec - C5_baseline) (5-judge primary). |
| `4_4_1_supermemory_native_wilcoxon_p` | paper.4.4.1 | -0.0100 | 0.8077 | 0.8177 | Wilcoxon signed-rank paired p-value, full paired panel (native config, n=14) |
| `4_4_3_keckley_q21_mem0_delta` | paper.4.4.2_4.4.3 | -0.5000 | 0.2000 | 0.7000 | Mem0 Keckley Q21 DELTA (5-judge primary panel mean). |
| `4_4_3_keckley_q21_zep_delta` | paper.4.4.2_4.4.3 | -0.5000 | 0.2000 | 0.7000 | Zep Keckley Q21 DELTA (5-judge primary panel mean). |

## Per-section walkthrough

| section | total | MATCH | MINOR_ROUNDING | MISMATCH_SUBSTANTIVE | STAT_TYPE | NON_CLAIM |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 61 | 32 | 4 | 16 | 0 | 9 |
| Appendix B | 242 | 190 | 4 | 14 | 0 | 34 |
| Appendix D | 761 | 675 | 13 | 17 | 0 | 56 |
| paper.4.4.1 | 50 | 27 | 6 | 9 | 0 | 8 |
| paper.4.4.2_4.4.3 | 45 | 0 | 0 | 43 | 0 | 2 |
| §4.1 cross-subject gradient | 115 | 73 | 3 | 9 | 0 | 30 |
| §4.2 + §4.2.1 | 146 | 74 | 22 | 46 | 0 | 4 |
| §4.3 | 45 | 6 | 8 | 31 | 0 | 0 |
| §4.5 + Appendix F | 44 | 12 | 5 | 21 | 0 | 6 |

## Methodological asymmetry notes

- **§4.4.2 paired_total_n.** Scaffold reports paired_total_n = 546 for the strict 5-judge primary panel across every system. The paper reports 516 (line 1084) and 507 (line 1233) in places where the panel was implicitly the audit panel rather than the locked 5-judge primary. Scaffold value is the locked aggregation rule output.
- **§4.4.3 Keckley Q21 (Mem0, Zep deltas).** Scaffold uses the strict 5-judge primary panel mean. The paper table presents per-judge-rounded means under a relaxed inclusion rule that flips the sign on Mem0 and Zep deltas (paper -0.50 vs scaffold +0.20). Surfaced as SIGN_FLIP rows. This is a primary-vs-relaxed panel asymmetry, not a numeric error in either source.
- **§4.5 Letta 7-judge sensitivity rows.** Paper presents 7-judge deltas; scaffold reproduces both 5-judge and 7-judge variants. The paper values for 7-judge Hamerton (+0.20) and Babur (+0.29) predate the recompute against the current judgment files; scaffold produces +0.093 and +0.232 respectively (running-list items).
- **§4.5 named-entity counts.** Paper line 2466 cites Babur 540 vs 46 and Ebers 58 vs 19. Scaffold computes Babur 416/65 and Ebers 53/34. The locator on Ebers BL row picks 46 (the Babur BL value from the same sentence) due to co-mention proximity; the headline MISMATCH_SUBSTANTIVE classification is correct, but the displayed paper_value cell may sometimes show the co-mentioned subject's value rather than the correct subject's value. Verify against line 2466 directly when applying the fix.
- **Appendix D.3.4 length-correlation denominator.** Scaffold emits n=312 for low-baseline question count; paper carries n=351 in the C5 row from a pre-recompute draft (the 351 -> 312 transcription error from the running list).
- **NO_RETRIEVAL Supermemory methodology disclosure.** Supermemory's controlled config retrieved 30 records on a subset of subjects; the scaffold captures this in the substrate-controlled aggregate but the paper text does not surface this inline at §4.4.1. Recommendation: add a footnote at §4.4.1's Supermemory paragraph noting the 30-record retrieval cap.
- **§4.2 Hamerton spec_tokens.** Paper §1.3 line 106 says '~7,300 tokens'; §4.2 table column header says '~7K tok' as a shared estimate; scaffold computes per-subject tokens with Hamerton at 4,478 (notably below the ~7K group estimate). The paper's column-header rounding is a deliberate shared-estimate presentation, not a per-subject claim. Per-subject scaffold values disagree with the rounded column header for the smaller specifications (Hamerton, Sunity Devee).

## PAPER_ONLY items (coverage gaps)

_No PAPER_ONLY gaps detected by heuristic scan._

## Emit-script run log

| script | exit | json_present | stderr_tail |
|---|---:|:--:|---|
| `_v11_emit_3_study_design.py` | 0 | yes |  |
| `_v11_emit_4_1_gradient.py` | 0 | yes |  |
| `_v11_emit_4_2_compression.py` | 0 | yes |  |
| `_v11_emit_4_3_wrong_spec.py` | 0 | yes |  |
| `_v11_emit_4_4_1_memory_systems.py` | 0 | yes |  |
| `_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py` | 0 | yes |  |
| `_v11_emit_4_5_letta.py` | 0 | yes |  |
| `_v11_emit_appendix_b_battery.py` | 0 | yes |  |
| `_v11_emit_appendix_d.py` | 0 | yes |  |

Note: emit scripts with non-zero exit are expected. Each scaffold's `--verify` mode compares its emitted values to v10 paper text and exits 1 on any mismatch; this is the scaffold's job, not a failure of the orchestrator.

