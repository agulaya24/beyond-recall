# Repo polish + naming-convention audit — Beyond Recall v11.8 (2026-05-05)

Pre-publish hygiene sweep across `scripts/`, `results/`, `data/`, `docs/`, top-level. Audit only — no files modified.

---

## Top-level files: status

**Already covered.** A complete top-level review landed tonight at `docs/reviews/repo_signoff_v11_8_20260505_192632.md` (19:26). It enumerates 5 BLOCKING items (canonical-pointer flips in KEY_FINDINGS / DATA_REFERENCE / PROVENANCE_INDEX, the additivity-vs-interpretive-layer reframe in README + study-guide + STUDY_MEMORY, the broken §4.1.2 author-pilot citations in KEY_FINDINGS / PROVENANCE_INDEX, the v11.5/v11.8 contradiction in `mcp/README.md` vs `mcp/tools.py`) plus 5 DRIFT items and 2 CLEAN files (`requirements.txt`, `.gitignore`). **Adopt those findings as-is.** This audit covers everything that was not in scope of that signoff.

One additional top-level note: `docs/_pandoc_default_reference.docx` and `docs/_reference_arxiv_11pt.docx` sit at the docs root with leading underscores. They are pandoc style references for export, real artifacts, but the underscore prefix conventionally signals "scratch" in this repo. Consider moving to `docs/_pandoc_styles/` or annotating their purpose in `docs/README.md`.

---

## scripts/: cleanup candidates

68 of 218 script files have a leading underscore (`_`). The convention works but the directory is now hard to navigate. Action breakdown:

### Group 1 — Session-temporary auditing (BLOCK A — archive together)

| Files | Rationale | Fate |
|---|---|---|
| `_audit_keckley_q21.py`, `_audit_keckley_q21_debug.py`, `_audit_keckley_q21_judges.py`, `_audit_keckley_q21_v2.py`, `_audit_keckley_q21_v3.py` | 5 iterations of a single ad-hoc Keckley Q21 audit run today; not on reproduction path | Move to `scripts/_archive/keckley_q21_audit_20260505/` |
| `_probe_hamerton.py`, `_probe_hamerton2.py`, `_probe_hamerton3.py`, `_probe_hamerton_c4a.py`, `_probe_hamerton_sensitivity.py` | 5 iterations of Hamerton probing | Move to `scripts/_archive/probes_hamerton/` |
| `_probe_c4a.py`, `_probe_hedge_variants.py`, `_probe_keckley_q21.py`, `_probe_retrieval_styles.py`, `_probe_top_examples.py`, `_probe_zep_facts.py`, `_probe_zep_response.py`, `_probe_zitkala_q18.py` | 8 single-question session probes; per REPRODUCE.md §5.3 explicitly NOT on canonical reproduction path | Move to `scripts/_archive/probes_misc/` |
| `_audit_terms_v118.py`, `_audit_v11_8_subsets.py`, `_audit_with_c2c.py` | One-off v11.8-era audits | Move to `scripts/_archive/audits_v11_8/` |
| `_check_babur_sm.py`, `_diag_gpt54_health_test.py`, `_diag_wrong_spec_v2_count.py` | Diagnostics for resolved bugs (gpt54 batch failures + wrong_spec_v2 count) | Move to `scripts/_archive/diagnostics_resolved/` |
| `_examine_bernal_diaz.py`, `_p0b_inventory.py`, `_partb_reference_fixes.py`, `_partb_restructure.py`, `_repo_review_gpt55_20260424.py`, `_rerun_wrong_spec_v2_gpt54_20260425.py`, `_run_v9_groq_review.py`, `_sample_explicit.py`, `_supermemory_apply.py`, `_validate_classifier_sample.py`, `_verify_battery_leakage.py`, `_verify_claims.py`, `_wait_for_classifier.py`, `_write_wrong_spec_report.py`, `_judge_invocation` (KEEP — REPRODUCE.md §6.5.3 dependency), `_per_question_outcomes_v2.json`, `_battery_leakage_results.json` (data, not script) | Mixed scratch with strong session-temporary signal | Audit individually; the JSON files belong in `docs/research/`, scripts to `scripts/_archive/scratch_v9_v10/` |

### Group 2 — Triplicate figure generators (single fate)

Only the `_v3` outputs are present in `figures/`. The base + `_v2` versions exist alongside. Per env memory and `figures/_archive/` (which already holds 24 superseded PNGs), the convention is to retire the older versions.

| File group | Latest version in use | Fate for older versions |
|---|---|---|
| `generate_fig_4_1_gradient_scatter{_,_v2,_v3}.py` | `_v3` | Move base + `_v2` to `scripts/_archive/figure_generators_superseded/` |
| `generate_fig_4_2_1{_,_v2,_v3}.py` | `_v3` | same |
| `generate_fig_4_2_compression{_,_v2,_v3}.py` | `_v3` | same |
| `generate_fig5_condition_effects{_,_v2,_v3}.py` | `_v3` | same |
| `generate_fig7_memory_systems{_,_v2,_v3}.py` | `_v3` | same |

10 files moved; 5 active generators kept. (Exception: `_v3` versions of fig5 + fig7 themselves may be obsolete — `figures/` shows fig_4_4_1_jaccard_heatmap_v1.{pdf,png} but the v11.8 paper figures are fig_4_1, fig_4_2, fig_4_2_1, fig_4_4_1. fig5 + fig7 generators may be entirely retired. Confirm against paper figure list before archiving any v3.)

### Group 3 — Versioned export-to-docx scripts

8 versioned exporters: `export_v7`, `export_v8`, `export_v9`, `export_v10`, `export_v11`, `export_v11_1`, `export_v11_2`, `export_v11_5_locked`, `export_v11_6`, `export_v11_7`. The active draft is v11.8; there is no `export_v11_8_to_docx.py`.

| Action | Files |
|---|---|
| Author still needs to create | `export_v11_8_to_docx.py` (mentioned for post-content-lock step in env memory). Block until written. |
| Keep | `export_v11_7_to_docx.py` (most recent; serves as template) |
| Archive | `export_v7_to_docx.py` through `export_v11_6_to_docx.py` (7 files) → `scripts/_archive/export_docx_superseded/` |

### Group 4 — Single-use review scripts

These were API-call scripts for specific cross-LLM review rounds; the outputs landed in `docs/reviews/_archive/`. The scripts themselves do not run on canonical reproduction path.

| Files | Fate |
|---|---|
| `gate_review_v8.py`, `gate_review_v8_retry.py`, `gate_review_cerebras_retry.py` | Archive: `scripts/_archive/reviews_v8/` |
| `review_v9_gemini_pro.py`, `review_v9_mistral.py`, `review_v9_triage.py`, `extract_v9_comments.py`, `review_paper_v9_prefinal.py` | Archive: `scripts/_archive/reviews_v9/` |
| `review_v10_gpt55.py`, `review_v10_gpt55_postfix.py`, `extract_v10_1_comments.py` | Archive: `scripts/_archive/reviews_v10/` |
| `cursory_review_v11.py`, `cursory_review_v11_gemini_retry.py`, `review_v11_c96_framing.py`, `review_v11_post_comments_gemini_pro.py`, `review_v11_post_comments_gpt55.py`, `review_v11_scaffolding_gpt55.py`, `review_v11_8_closing_5_4_opus.py`, `review_v11_8_intro_s5_closing.py`, `review_paper_v11_5_sections_1_4.py` | Archive: `scripts/_archive/reviews_v11_v11_8/` |
| `review_paper_round2.py`, `review_paper_round2_focused.py`, `review_paper_round2_groq_minimal.py`, `review_paper_round3.py`, `review_section4_plan.py`, `review_section4_structure.py`, `review_section5_structure.py`, `review_section_4_6.py`, `review_section_4_6_gemini_retry.py`, `review_framing_report_round2.py`, `review_pattern_activation_claim.py`, `review_compression_framing.py`, `review_benchmark_metric.py`, `review_figures.py`, `figure_review_20260422.py`, `figure_layout_spotcheck.py`, `final_locked_content_review.py`, `gemini_review_script.py`, `title_panel_review.py` | Archive: `scripts/_archive/reviews_topical/` |
| **KEEP** `review_paper.py` | Generic cross-LLM review pipeline; not version-stamped |

### Group 5 — Miscellaneous noise

| File | Issue | Fate |
|---|---|---|
| `scripts/review_round6.log` | Log file checked into scripts/; `.gitignore` line 30 catches `*.log` BUT this one made it in | Delete (or move to `logs/`) |
| `scripts/__pycache__/` | Bytecode dir | Verify `.gitignore` is filtering correctly (it should — line 2). If any `.pyc` files are committed, untrack |
| `scripts/_v10_verification/` | Subdir from v10 release-freeze; `external_methodology_verification.py`, `verify_paper.py`, `verify_wrongspec_v2.py` etc. — historical verification scaffolding | Either keep alongside `_v11_validation/` (parallel structure) or archive to `scripts/_archive/v10_verification/`. Verify whether REPRODUCE.md or any current doc references it. (Searched: REPRODUCE.md only references `_v11_validation/`, not `_v10_verification/`.) Lean toward archive. |
| `scripts/_v11_emit_*.py` (8 files) + `_v11_audit_paper_numbers.py` + `_v11_paper_numbers.py` | Per env memory: architecture compliance deferred post-arXiv; per `_ARCHITECTURE.md` §12 these are MAJOR/BLOCKER offenders against the schema contract but are still the sanctioned paper-number scaffolding | **KEEP**. Add a one-paragraph header comment in `docs/research/v11_emit/_ARCHITECTURE.md` already explains; consider clustering all 10 into a `scripts/_v11_emit/` subdirectory for visual cleanup |
| `_table_4_6_5judge_recompute.py`, `_topk_aggregate.py`, `_topk_sensitivity_test.py`, `_topk_stats.py`, `_emit_full_judge_matrix.py`, `_p0b_inventory.py` | Mid-tier scratch | Keep if referenced from any DATA_REFERENCE provenance entry; otherwise archive |

### Naming inconsistency in scripts/ — call out

- **Paper-version stamps mixed:** `_audit_terms_v118.py` (no separator) vs `_audit_v11_8_subsets.py` (underscored) vs `review_v11_8_*` (underscored). Pick one — prefer `v11_8` since it dominates. Rename `_audit_terms_v118.py` → `_audit_terms_v11_8.py`.
- **Date stamps:** `figure_review_20260422.py` (YYYYMMDD), `_repo_review_gpt55_20260424.py` (YYYYMMDD). Consistent. Good.
- **Prefix discipline:** `_` for scratch is consistent across the directory.

---

## results/: completeness check

### supermemory_fullpipeline gap (FLAG FOR AUTHOR — possibly intentional)

Of 13 global subjects, only **2** (Augustine, Keckley) have the full 11-file `supermemory_fullpipeline_*` set (extracted, ingestion, retrieval, results, judgments × 7 judges, judgments_merged). The other 11 subjects have only `supermemory_fullpipeline_retrieval.json` — no extracted, ingestion, results, or judgments files.

Confirmed missing by spot-check: Babur, Bernal Diaz, Cellini, Rousseau. Babur additionally has a `supermemory_fullpipeline_archive_free_tier_20260423_181634/` folder containing the original full free-tier 11-file set; the others do not visibly have such an archive folder.

**This is the supermemory paid-tier rerun.** Either (a) the rerun was scoped to a subset by design (verify against `compute_supermemory_paid_tier_aggregate.py` and the §4.4.2 paid-tier rerun report at `docs/research/p0_2_supermemory_paid_tier_rerun.md`), or (b) the rerun is incomplete. **Do not delete or rename anything in this set without author confirmation.** Likely intentional aggregate-only design, but the asymmetric on-disk shape will look like a gap to a fresh reader.

Recommended action: add a one-line note to `results/README.md` "supermemory paid-tier rerun is intentionally scoped to aggregate analysis; per-judge files exist for Augustine + Keckley only" — or whatever the actual scope is.

### Augustine extras

- `results/global_augustine/judgments_v2_gemini_pro2.json`, `judgments_v2_gemini_pro_key2.json` — only Augustine has these. Likely scratch from a Gemini Pro key-rotation test (`_key2` suffix is the tell). Verify and archive or delete; no other subject has them and they are not referenced in DATA_REFERENCE.

### Other results/ structure

- `_tier2/` covers 3 subjects (Ebers, Yung Wing, Zitkala-Sa) — matches paper §4.6.1 "Tier 2 cross-provider directional probe on 3 subjects." CLEAN.
- `_wrong_spec_v2/` covers all 13 globals + Hamerton. CLEAN.
- `_s114_backfills/` covers per-cell judge backfills, 100+ files. CLEAN structurally; opaque without README. Verify `_s114_backfills/README.md` explains.
- `franklin_legacy_20260411/` — historical Franklin run. Date-stamped clearly. CLEAN as preserved historical baseline.
- `multimodel/` — 3 Hamerton response files (gemini, gpt54, sonnet). Matches paper Tier 2 description. CLEAN.

### Per-subject judgments file count (sanity check)

Counts vary 103-115. Variation is dominated by (a) supermemory_fullpipeline gap (10 fewer files for 11 subjects), (b) Augustine's gemini_pro2 extras (+2 files). Once supermemory paid-tier scope is documented, the variance is explained.

---

## data/: completeness check

| Subdir | Status | Notes |
|---|---|---|
| `data/source_corpora/` | CLEAN | All 14 main subjects have `raw.txt` + `provenance.md`. Plus `franklin_autobiography/` (chapters/, entity_map.json) and `franklin_letters/` (raw.txt + provenance.md). MANIFEST.md + manifest.json present. |
| `data/global_subjects/` | CLEAN | All 13 globals have spec/facts/battery/results, plus `anchors_v4.md`, `core_v4.md`, `predictions_v4.md`, `brief_v5.md`, `spec.md`, `spec_production.md` |
| `data/hamerton/` | CLEAN | battery, facts, questions_80, shared_facts, spec/ |
| `data/franklin/` | CLEAN | Standard set |
| `data/franklin_obscure/` | THIN — only README + battery + facts. No spec/, no anchors/core/predictions. May be intentional (cross-corpus probe, not a full subject) but flag for confirmation. |
| `data/topk_test_20260428/` | CLEAN — appendix data for Yung Wing top-K sensitivity test (K=10, K=50, K=140) |

---

## docs/: naming consistency

### docs/ root (paper drafts)

13 paper-draft files exist: v10_1, v11, v11_1, v11_2, v11_5_locked, v11_6, v11_7, v11_8 — each in `.md` form, most with `.docx` and `.clean.md` siblings. **v11.8 has only `.md`** (no `.docx`, no `.clean.md`). This is consistent with v11.8 being the active edit branch; .docx + .clean.md are produced at release-freeze. No action needed unless v11.8 is being frozen.

| Version | .md | .clean.md | .docx |
|---|:-:|:-:|:-:|
| v10_1 | yes | yes | yes |
| v11 | yes | yes | yes |
| v11_1 | yes | yes | yes |
| v11_2 | yes | yes | yes |
| v11_5_locked | (no plain .md, only locked variant) | yes | yes |
| v11_6 | yes | yes | yes |
| v11_7 | yes | yes | yes |
| v11_8 | **yes only** | no | no |

(There is also `beyond_recall_v11_5_draft.md` without locked + .docx siblings, distinct from v11_5_locked.)

Note: 8 in-flight paper-version-stamped drafts living in `docs/` root is excessive for a public release. Recommend: at freeze, **move v10_1, v11, v11_1, v11_2, v11_5, v11_5_locked, v11_6, v11_7 into `docs/versions/_pre_v11_8_drafts/`** (parallel to the existing `docs/versions/_pre_v11_drafts/`). Keep v11_8 + v10_1 (preserved baseline) at `docs/` root.

### docs/research/

200+ files. Date stamps consistent (`YYYYMMDD`). Naming prefixes consistent (`_` for scratch). Specific items to clean:

| File(s) | Issue | Fate |
|---|---|---|
| `_predicate_ablation_log_20260428_113635.txt`, `..._113907.txt`, `..._115014.txt`, `..._115036.txt` | 4 retry logs with `.txt` extension (so .gitignore `*.log` doesn't catch). Same date, same script | Move to `docs/research/_archive/predicate_ablation_logs/` or delete |
| `_a4_emdash_second_pass_report.md`, `_a4_emdash_sweep_report.md` | Em-dash sweep reports from earlier release-freeze passes | Verify still useful as audit trail; otherwise archive |
| `v11_panel_completeness_waivers.json.bak` | `.bak` file (`.gitignore` line 31 catches it but this one made it in) | Delete |

The README at `docs/research/README.md` already warns about v6/v7/v8 §-anchor drift in research-doc citations. Acceptable as a known-issue note.

### docs/reviews/

100+ files. Tonight's batch (2026-05-05) is well-named with `_v11_8_20260505_HHMMSS.md` pattern. Consistent. Good.

Potential orphan: `docs/reviews/round_v11_5_sections_1_4_20260501_141341.md` and `round_v11_6_section5_structure_20260501_152904.md` use `round_<topic>_v<paper>_<timestamp>` — a different pattern from the dominant `<topic>_v<paper>_<timestamp>`. Cosmetic, not a fix priority.

`docs/reviews/_archive/` looks healthy (28 files, clearly archived round artifacts).

### docs/versions/

`_pre_v11_drafts/` cleanly archives v8/v9/v10. `_latex_test_artifacts/` is descriptive. Standalone files (`beyond_recall_arxiv_draft*`, `beyond_recall_v6_draft.md`, `beyond_recall_v7_draft.md`, `blog_post_v1_aarik_notes.md`, `blog_post_v2_claude_draft.md`) sit alongside the archive subdirectory. Recommend moving the v6/v7/arxiv drafts into `_pre_v11_drafts/` for consistency.

`docs/internal/_archive/` — 7 files (AARIK_REVIEW_S110, MAIN_REPO_UPDATES_NEEDED, PAPER_DASHBOARD, REVIEW_GUIDE, etc.) properly archived. CLEAN.

### charts/ at top level

8 PNGs (bimodal_to_gradient.png, compression_story.png, franklin_judge_agreement.png, hamerton_full_hierarchy.png, hamerton_vs_franklin.png, judge_agreement.png, unknown_vs_known.png) + pipeline_diagram.md + README.md. Referenced from `README.md`, `AGENTS.md`, `agents/study-guide.md`, `figures/README.md`, `docs/FILE_NAMING.md`, but **not from any v11.8 paper draft.** These are pre-v8 visualization scratch, kept around as reference.

Recommend: add a header to `charts/README.md` clarifying "These are visualization sketches, not paper figures. Paper figures live in `figures/`." Or archive entirely if not actively used. Not a publish-day blocker.

---

## Recommended actions (P0 = publish-day blocking, P1 = should fix before public, P2 = cosmetic)

### P0 — publish-day blocking

1. **Adopt all 5 BLOCKING items from `repo_signoff_v11_8_20260505_192632.md`** (canonical-pointer flips × 4, additivity-vs-interpretive reframe in 3 docs, broken §4.1.2 citations, mcp/README contradiction, README §1 framing). That report has exact line numbers and replacement strings.
2. **Resolve the `supermemory_fullpipeline` per-subject asymmetry.** Either complete the paid-tier rerun for the 11 missing subjects, or document the intentional aggregate-only scope in `results/README.md`. Currently a fresh reader sees 1 file for 11 subjects vs 11 files for 2 subjects without explanation.
3. **Create `export_v11_8_to_docx.py` before any release-freeze.** Currently no docx exporter exists for the active draft; release-freeze needs one.
4. **Delete or relocate `scripts/review_round6.log`.** Should never have been committed (`.gitignore` line 30 covers `*.log`).
5. **Delete `docs/research/v11_panel_completeness_waivers.json.bak`.** Same — `.gitignore` covers `*.bak`.

### P1 — should fix before public

6. **Archive 65 of 68 underscore-prefixed scripts per Group 1, Group 4, and select items in Group 5 above** (~50 files into `scripts/_archive/` subdirectories). Keep `_v10_battery_sensitivity.py`, `_v10_coupling_sensitivity.py`, `_v10_pipeline_variance.py`, `_v10_pipeline_variance_report.py`, `_v11_emit_*.py` (8), `_v11_audit_paper_numbers.py`, `_v11_paper_numbers.py`, `_v11_validation/`, `_judge_invocation/`, `_figure_style.py`, `_build_reference_docx.py`, `_build_v11_comment_index.py`, `_compute_per_question_v2.py`. (~22 keepers; ~46 archives.)
7. **Archive 10 superseded figure-generator scripts** (Group 2: base + `_v2` of the 5 figure families) → `scripts/_archive/figure_generators_superseded/`. Keep only `_v3` versions.
8. **Archive 7 superseded export-to-docx scripts** (Group 3: v7 through v11_6) → `scripts/_archive/export_docx_superseded/`. Keep `export_v11_7_to_docx.py` as template.
9. **Archive 4 in-flight paper drafts** (v10_1 stays; v11_5/v11_5_locked/v11_6/v11_7 + their .clean.md and .docx siblings) → `docs/versions/_pre_v11_8_drafts/`. Reduces `docs/` root noise from ~25 paper-related files to ~5.
10. **Archive 4 predicate-ablation log files** (`docs/research/_predicate_ablation_log_*.txt`) — same script, 4 retries.
11. **Move `docs/_pandoc_default_reference.docx` and `docs/_reference_arxiv_11pt.docx`** to `docs/_pandoc_styles/` or annotate in `docs/README.md` (currently look like scratch).
12. **Verify `data/franklin_obscure/` thinness is intentional** (only README + battery + facts, no spec/anchors/core/predictions). Probably intentional cross-corpus probe scope, but document in its README if not already.

### P2 — cosmetic

13. **Rename `_audit_terms_v118.py` → `_audit_terms_v11_8.py`** for naming-stamp consistency.
14. **Cluster `_v11_emit_*.py` (8) + `_v11_audit_paper_numbers.py` + `_v11_paper_numbers.py`** into `scripts/_v11_emit/` subdirectory (parallel to `_v11_validation/`).
15. **Move `docs/versions/beyond_recall_v6_draft.md`, `beyond_recall_v7_draft.md`, `beyond_recall_arxiv_*`** into `docs/versions/_pre_v11_drafts/` for consistency with the existing archive structure.
16. **Add `charts/README.md` header** clarifying these are visualization sketches, not paper figures. Or archive `charts/` entirely if not actively referenced.
17. **Clear `scripts/__pycache__/`** (gitignored but check whether any .pyc files are committed; if so, untrack).
18. **`docs/reviews/` round-report naming inconsistency** (`round_<topic>_v<paper>_<timestamp>` vs `<topic>_v<paper>_<timestamp>`) — pick one. Not a publish blocker.

---

## What's already polished

- 5 of the 6 explicitly-called-out paper scripts exist and are correctly named (`analyze_retrieval_overlap.py`, `analyze_retrieval_overlap_semantic.py`, `recompute_5judge_primary.py`, `audit_section_pointers.py`, `migrate_source_corpora.py`, `fetch_references.py`). Figure generators all 4 exist.
- `data/source_corpora/` migration is complete with MANIFEST.md, manifest.json, and per-subject `raw.txt` + `provenance.md` for all 14 subjects.
- `data/global_subjects/` per-subject layer-files are complete (anchors_v4, core_v4, predictions_v4, brief_v5, spec, spec_production for all 13).
- `docs/references/` MANIFEST + 18 PDFs (17 arXiv + 1 Bartlett note) are well-organized.
- `requirements.txt` and `.gitignore` are correctly version-agnostic.
- `mcp/tools.py` correctly points at v11.8 (the README pointing at v11.5 is the bug).
- `scripts/_v11_validation/` and `scripts/_judge_invocation/` are well-organized as REPRODUCE.md §6.5 dependencies.
- Tonight's review batch (`*_v11_8_20260505_*.md`) follows clean naming.
- `docs/internal/_archive/` and `docs/reviews/_archive/` are properly populated with historical artifacts.
- The recurring underscore-prefix convention for scratch is consistent across the repo.
