# Repo Cleanup Candidates — v11 audit, 2026-04-27

Read-only audit of `C:/Users/Aarik/Anthropic/memory-study-repo/`. No files were modified or deleted. The candidate list below should be confirmed by the author before any destructive action.

**Canonical keep-set (do not flag).** Cross-referenced against:
- `docs/beyond_recall_v10_1_draft.md` (release-frozen for arXiv)
- `docs/beyond_recall_v11_draft.md` (current working draft)
- `REPRODUCE.md`, `README.md`, `AGENTS.md`, `agents/study-guide.md`, `agents/STUDY_MEMORY.md`
- `docs/DATA_REFERENCE.md`, `docs/KEY_FINDINGS.md`, `docs/PROVENANCE_INDEX.md`, `docs/METHODOLOGY.md`
- `docs/reviews/v11_release_freeze_status_20260425.md` (canonical pointer list)
- `docs/research/v11_emit/_ARCHITECTURE.md` (v11 emit contract)
- `docs/versions/README.md` (explicit archival policy: "Versioned files keep v1, v2, etc. suffixes ... earlier versions are retained, not deleted, so provenance is preserved")

Anything cited in those files is excluded from the candidate list, or downgraded to "likely keep."

---

## High-confidence cleanup (likely safe to delete)

| Path | Type | Last modified | Why a candidate | Recommended action |
|---|---|---|---|---|
| `docs/~$yond_recall_v10_1_draft.docx` | Word lock file | 2026-04-27 | Word-process lock; 162 bytes; orphaned if Word is closed | DELETE |
| `docs/~WRL0003.tmp` | Word recovery temp | 2026-04-27 | 3.3 MB orphaned recovery file; prefix `~WRL` is a Word temp-write artifact | DELETE |
| `docs/beyond_recall_v10_1_draft.docx.bak` | Backup | 2026-04-25 | 2.8 MB pre-pass backup; v10.1 is itself the locked baseline; current docx is 3.4 MB and ~24 hrs newer | DELETE (or move to a single archive folder if backup discipline matters) |
| `docs/research/v11_panel_completeness_waivers.json.bak` | Backup | (recent) | `.bak` of an active waivers JSON; live file is at the same path without `.bak` | DELETE |
| `scripts/__pycache__/` | Build artifact | active | Python bytecode cache; should never be in the repo. ~380 KB | DELETE + add to `.gitignore` if not present |
| `scripts/_judge_invocation/__pycache__/` | Build artifact | active | Same as above. ~44 KB | DELETE |
| `scripts/_v10_verification/__pycache__/` | Build artifact | active | Same as above. ~12 KB | DELETE |
| `docs/versions/_latex_test_artifacts/beyond_recall_test.aux` | LaTeX intermediate | 2026-04-15 | LaTeX build intermediate explicitly described as "Not load-bearing" in `docs/versions/README.md`; pdf can be regenerated from `.tex` | DELETE (entire `_latex_test_artifacts/` dir is fair game except possibly the `.tex`) |
| `docs/versions/_latex_test_artifacts/beyond_recall_test.log` | LaTeX log | 2026-04-15 | Same. Build log only; pre-v6 era | DELETE |
| `docs/versions/_latex_test_artifacts/beyond_recall_test.out` | LaTeX intermediate | 2026-04-15 | Same | DELETE |
| `docs/versions/_latex_test_artifacts/beyond_recall_test.pdf` | LaTeX output | 2026-04-15 | Test artifact, not load-bearing per README | DELETE |
| `scripts/review_round6.log` | Stray log | 2026-04-17 | Plain `.log` in scripts/, not referenced | DELETE |
| `docs/research/_band_examples.txt` | Intermediate scratch | 2026-04-21 | One-off score-band scratch; produced by `_print_band_examples.py`; not referenced in any core doc | DELETE or move to `_archive` |
| `docs/research/_score_band_pool.json` | Intermediate scratch | 2026-04-21 | Same family — pool building output; not referenced | DELETE or archive |
| `docs/research/_score_band_stats.json` | Intermediate scratch | 2026-04-21 | Same family | DELETE or archive |
| `docs/research/_baselayer_c1_c3_candidates.json` | Intermediate | 2026-04-20 | Underscore-prefixed candidate file; the named output `baselayer_c1_vs_c3_paired_analysis.md` is what's cited | DELETE or archive |
| `docs/research/_mlz_c1_c3_candidates.json` | Intermediate | 2026-04-20 | Same family | DELETE or archive |
| `docs/research/_sm_c1_c3_candidates.json` | Intermediate | 2026-04-20 | Same family | DELETE or archive |
| `docs/research/_sm_paired_5judge.json` | Intermediate | 2026-04-22 | Underscore-prefixed pair file; replaced by named outputs cited in v10.1/v11 | DELETE or archive |

Subtotal: ~17 high-confidence, est. ~7-8 MB plus the `__pycache__` dirs.

---

## Medium-confidence cleanup (worth reviewing)

### Old-version paper drafts in `docs/` (NOT in `docs/versions/`)

The `docs/versions/README.md` policy says old drafts go in `docs/versions/`. v8 and v9 drafts are still at the top of `docs/`. v10 (no `_1`) is also stranded.

| Path | Type | Last modified | Why a candidate | Recommended action |
|---|---|---|---|---|
| `docs/beyond_recall_v8_draft.md` | Old paper draft | 2026-04-22 | Superseded by v9 → v10 → v10.1 → v11. v8 is preserved per CLAUDE.md as a baseline | MOVE to `docs/versions/` |
| `docs/beyond_recall_v8_draft.clean.md` | Old paper draft | 2026-04-23 | Same | MOVE to `docs/versions/` |
| `docs/beyond_recall_v8_draft.docx` | Old docx export | 2026-04-23 | Same | MOVE to `docs/versions/` |
| `docs/beyond_recall_v9_draft.md` | Old paper draft | 2026-04-24 | Superseded by v10 → v10.1 → v11; preserved per CLAUDE.md as baseline | MOVE to `docs/versions/` |
| `docs/beyond_recall_v9_draft.clean.md` | Old paper draft | 2026-04-24 | Same | MOVE to `docs/versions/` |
| `docs/beyond_recall_v9_draft.docx` | Old docx export | 2026-04-24 | Same | MOVE to `docs/versions/` |
| `docs/beyond_recall_v10_draft.clean.md` | Old paper draft | 2026-04-25 | v10 (no `_1`) — superseded by v10.1; v10 release-freeze report exists, so prov. trail is preserved | MOVE to `docs/versions/` (or DELETE if v10.1 is treated as the canonical "v10" baseline) |

### Versioned figure-generation scripts

The v3 scripts are cited in figure outputs; v1 and v2 are pre-decision iterations.

| Path | Type | Why | Action |
|---|---|---|---|
| `scripts/generate_fig_4_1_gradient_scatter.py` | v1 script (no suffix) | Superseded by `_v3` which is the cited current generator | ARCHIVE or DELETE |
| `scripts/generate_fig_4_1_gradient_scatter_v2.py` | v2 script | Same | ARCHIVE or DELETE |
| `scripts/generate_fig_4_2_1.py` | v1 script | Superseded by `_v3` | ARCHIVE or DELETE |
| `scripts/generate_fig_4_2_1_v2.py` | v2 script | Same | ARCHIVE or DELETE |
| `scripts/generate_fig_4_2_compression.py` | v1 script | Superseded by `_v3` | ARCHIVE or DELETE |
| `scripts/generate_fig_4_2_compression_v2.py` | v2 script | Same | ARCHIVE or DELETE |
| `scripts/generate_fig5_condition_effects_v2.py` | v2 script | Superseded by `_v3` | ARCHIVE or DELETE |
| `scripts/generate_fig7_memory_systems_v2.py` | v2 script | Superseded by `_v3` | ARCHIVE or DELETE |

Keep the `_v3` versions for all four families — those are current.

### Per-version review-script families

| Path | Why | Action |
|---|---|---|
| `scripts/review_paper.py` | Round 1 review (S109); the `scripts/README.md` notes it points at the legacy `beyond_recall_arxiv_draft.md` filename | ARCHIVE |
| `scripts/review_paper_round2.py`, `*_focused.py`, `*_groq_minimal.py` | Round 2 reviews; superseded by gate / v9 / v10 / v11 review scripts | ARCHIVE |
| `scripts/review_paper_round3.py` | Round 3; same | ARCHIVE |
| `scripts/review_paper_v9_prefinal.py` | v9-specific; superseded | ARCHIVE |
| `scripts/review_v9_gemini_pro.py`, `review_v9_mistral.py`, `review_v9_triage.py`, `_run_v9_groq_review.py` | v9 review pass; v9 is no longer the working draft. `_run_v9_groq_review.py` IS cited in PROVENANCE_INDEX though — verify before deleting | KEEP `_run_v9_groq_review.py`; ARCHIVE the rest |
| `scripts/review_section4_plan.py`, `review_section4_structure.py`, `review_section_4_6.py`, `review_section_4_6_gemini_retry.py` | Section-4 working-pass scripts | ARCHIVE |
| `scripts/review_benchmark_metric.py`, `review_compression_framing.py`, `review_figures.py` | One-off review passes for v8/v9 era | ARCHIVE |
| `scripts/review_v10_gpt55.py`, `review_v10_gpt55_postfix.py` | v10 review passes; output already saved as `docs/reviews/v10_review_gpt55_20260424.md` | ARCHIVE (output preserved) |
| `scripts/gate_review_v8.py`, `gate_review_v8_retry.py`, `gate_review_cerebras_retry.py` | v8 gate review; output in `_archive` | ARCHIVE |
| `scripts/gemini_review_script.py` | Earliest review script; per `scripts/README.md` "points at legacy `beyond_recall_arxiv_draft.md`" | ARCHIVE or DELETE |
| `scripts/figure_review_20260422.py`, `figure_layout_spotcheck.py`, `final_locked_content_review.py`, `title_panel_review.py` | One-off review-pass scripts (S114 era) | ARCHIVE |

### Investigative `_probe_*` and `_diag_*` scripts

These are ad-hoc; one is cited in PROVENANCE_INDEX (`_probe_hedge_variants.py`). The rest do not appear in any core doc.

| Path | Why | Action |
|---|---|---|
| `scripts/_probe_hamerton.py`, `_probe_hamerton2.py`, `_probe_hamerton3.py`, `_probe_hamerton_c4a.py`, `_probe_hamerton_sensitivity.py` | Five Hamerton probe variants. Most likely scratch | DELETE or ARCHIVE all but the most recent if any output is cited |
| `scripts/_probe_c4a.py`, `_probe_keckley_q21.py`, `_probe_retrieval_styles.py`, `_probe_top_examples.py`, `_probe_zep_facts.py`, `_probe_zep_response.py`, `_probe_zitkala_q18.py` | One-off probes; not cited | DELETE or ARCHIVE |
| `scripts/_diag_gpt54_health_test.py`, `_diag_wrong_spec_v2_count.py` | Diagnostics for v11 GPT-5.4 batch failures (April 25); the failure write-up is preserved at `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md`, which IS cited | KEEP — diagnostics for cited issue |
| `scripts/_check_babur_sm.py`, `_examine_bernal_diaz.py`, `_sample_explicit.py`, `_validate_classifier_sample.py`, `_wait_for_classifier.py`, `_verify_claims.py`, `_write_wrong_spec_report.py` | Investigative scratch scripts; none cited in canonical docs | ARCHIVE or DELETE |
| `scripts/_audit_with_c2c.py`, `_p0b_inventory.py`, `_partb_reference_fixes.py`, `_partb_restructure.py`, `_supermemory_apply.py` | One-off S114-era restructuring scripts | ARCHIVE |
| `scripts/_compute_per_question_v2.py`, `_per_question_outcomes_v2.json` | Working file from S114; superseded by `_v11_emit_*` family | ARCHIVE |
| `scripts/_battery_leakage_results.json`, `_repo_review_gpt55_20260424.py` | One-off; output preserved elsewhere | ARCHIVE |

### `docs/research/` intermediate / scratch

| Path | Why | Action |
|---|---|---|
| `docs/research/_a4_emdash_sweep_report.md`, `_a4_emdash_second_pass_report.md` | Em-dash removal sweep working notes; the sweep is done | ARCHIVE |
| `docs/research/_p0_batch2_summary.md`, `_p0_parallel_batch_summary.md` | S114 batch progress notes | ARCHIVE |
| `docs/research/_qa_q32_q47_combined_summary.md` | One-off Q&A summary | ARCHIVE |
| `docs/research/_supermemory_update_block.md` | One-off update fragment | ARCHIVE |
| `docs/research/_letta_blocks/archival_pair_extract.py`, `archival_scan.py`, `extract_responses.py`, `compute_paired.py`, `check_babur_alignment.py`, `check_ebers_hamerton_alignment.py` | One-off scripts inside a research-data dir; only `paired_scores.json` from this directory is cited | KEEP `paired_scores.json`; consider archiving the helper scripts (or leaving in place — they're small) |
| `docs/research/judge_floor_test.json`, `judge_floor_test.md` | Judge-floor experiment; not cited in v10.1 / v11 | KEEP — small and may be referenced from internal/PROVIDER_EXPERIENCE_LEDGER |

### Long, version-specific review files (under `docs/reviews/`)

| Path | Why | Action |
|---|---|---|
| `docs/reviews/figure_fixes_20260422.md`, `figure_layout_spotcheck_20260423.md`, `figure_review_20260422.md` | S114 figure review trail | KEEP for provenance OR move to `_archive` |
| `docs/reviews/full_paper_gate_review_20260422_173703.md`, `gate_review_synthesis_20260422_173703.md` | v8 gate review pair | MOVE to `_archive` |
| `docs/reviews/repo_completeness_audit_20260422_173831.md`, `repo_hygiene_audit_20260422_182500.md` | S114 repo audits superseded by v10/v11 release-freeze + this audit | MOVE to `_archive` |
| `docs/reviews/s114_*` files (~16 files) | S114 session artifacts; some referenced (`s114_full_data_audit.md`, `s114_paragraph_review.md`, `s114_section4_structure_review.md`, `s114_session_summary.md`, `s114_example_analysis_*` in `_archive/`). Verify each before moving | KEEP referenced ones; MOVE the rest to `_archive` |
| `docs/reviews/session_close_handoff_v8_complete.md` | v8 handoff; superseded by v10 release-freeze | MOVE to `_archive` |
| `docs/reviews/v9_docx_comments.md`, `v9_final_review_*` (4 files) | v9 review trail; v9 is no longer the working draft | MOVE to `_archive` (provenance is preserved) |
| `docs/reviews/v10_logical_errors_audit.md`, `v10_numerical_drift_reconciliation_report.md`, `v10_numerical_verification_report.md`, `v10_repo_review_gpt55_20260424.md`, `v10_review_gpt55_20260424.md`, `v10_tier2_methodology_external_verification_20260425.md`, `v10_voice_alignment_review_20260425.md` | v10 round; v10.1 is the canonical baseline. Release-freeze status doc cites the gpt55 v10 review + the release-freeze report. These provide the v10→v10.1 paper-trail | KEEP `v10_release_freeze_pass_report.md`, `v10_review_gpt55_20260424.md`, `v10_repo_review_gpt55_20260424.md`. The other four can MOVE to `_archive` if you want to thin the live dir |
| `docs/reviews/v11_phase1_inventory_report.md`, `v11_orchestrator_run_20260425.md`, `v11_option_c_rerun_completion_20260425.md`, `v11_judge_call_controls_implementation_20260425.md`, `v11_gpt54_batch_failures_diagnostic_rerun_20260425.md` | v11 emit-architecture working-pass notes. `v11_gpt54_batch_failures_diagnostic_rerun_*` IS cited in v11 paper. Others are operational logs | KEEP the cited one; the rest can MOVE to `_archive` post-arXiv |

### `docs/internal/`

| Path | Why | Action |
|---|---|---|
| `docs/internal/AARIK_REVIEW_S110.md` | S110 review notes; older session | KEEP as historical context OR move under `docs/internal/_archive/` |
| `docs/internal/LLM_REVIEW_FIXES.md` | S109-S110 LLM-review fix log; superseded | KEEP or archive |
| `docs/internal/MAIN_REPO_UPDATES_NEEDED.md` | S109 handoff | ARCHIVE |
| `docs/internal/PAPER_DASHBOARD.md` | S109-S110 dashboard snapshot | ARCHIVE |
| `docs/internal/REVIEW_GUIDE.md` | Review-process guide; check whether it's still the operative one | KEEP if current; archive if superseded by v11 release-freeze process |

---

## Likely keep but worth confirming

| Path | Notes |
|---|---|
| `docs/versions/` (entire dir, 5.1 MB) | Per `versions/README.md`, explicit policy: "earlier versions are retained, not deleted, so provenance is preserved." Do not flag this dir. |
| `docs/research/v11_emit/*.json,*.md` (8 sections + `_ARCHITECTURE.md`) | Load-bearing — every paper number is supposed to flow through these per the v11 architecture spec |
| `docs/research/_letta_rerun/` (1.5 MB, ~50 files) | Letta full-stack rerun working dir; `5judge_primary_results.json`, `fullstack_named/RESULTS.md`, `fullstack_named/5judge_fullstack_results.json` are cited. Keep entire dir for now |
| `docs/research/_letta_blocks/` (604 KB) | `paired_scores.json` is cited; rest are small support files. Keep |
| `docs/reviews/_archive/` | Already an archive dir — leave alone |
| `scripts/_v10_battery_sensitivity.py`, `_v10_coupling_sensitivity.py`, `_v10_pipeline_variance.py`, `_v10_pipeline_variance_report.py` | Cited in §4.1 of v10.1/v11; KEEP |
| `scripts/_v11_emit_*.py` (8 emit scripts) + `_v11_paper_numbers.py` + `_v11_validation/*` | v11 architecture; KEEP all |
| `scripts/_v10_verification/` directory | Cited in v10.1; KEEP. Note `__pycache__` inside should still be deleted |
| `scripts/_judge_invocation/` (anthropic, gemini, openai callers) | Active infrastructure for judge invocation across panels; KEEP |
| `scripts/_emit_full_judge_matrix.py`, `_table_4_6_5judge_recompute.py`, `_verify_battery_leakage.py` | Cited in v10.1/v11 prose; KEEP |
| `scripts/build_v8.py`, `build_review_html.py`, `extract_docx_annotations.py`, `extract_v9_comments.py`, `extract_v10_1_comments.py` | Building / docx-comment infrastructure. v8 builder is older but tooling is reused; KEEP unless explicitly retired |
| `scripts/export_v7_to_docx.py`, `export_v8_to_docx.py`, `export_v9_to_docx.py`, `export_v10_to_docx.py`, `export_v11_to_docx.py` | Per-version exporters. Keeping current `v11` and possibly `v10` is plenty; older ones are clutter | Recommend ARCHIVE older ones (v7, v8, v9) |
| `scripts/remove_em_dashes.py` (210 KB) | Large because it inlines a paper's worth of replacements. Not cited but the em-dash sweep is in `feedback_no_em_dashes.md` | KEEP if still the canonical tool, else archive |
| `workspace/study_knowledge.db` (7.9 MB) + `workspace/study_vectors/` (~53 MB) | Total 61 MB. Per CLAUDE.md it's the indexed search store; regeneratable via `python scripts/index_study_repo.py`. Active tool, not waste — but worth flagging as a candidate for an `--archive-vectors` toggle on release tags. KEEP for now |

---

## Naming / organization fixes

| Issue | Detail | Recommended fix |
|---|---|---|
| **`scripts/_v11_emit/` directory does NOT exist** | The audit task referred to `scripts/_v11_emit/`, but the v11 emit scripts are flat-named in `scripts/` (e.g. `_v11_emit_3_study_design.py`, `_v11_emit_4_1_gradient.py`, etc.). The output dir IS at `docs/research/v11_emit/`. The `_v11_validation/`, `_v10_verification/`, `_judge_invocation/` siblings ARE directories. | Create a `scripts/_v11_emit/` subdirectory and move the 8 `_v11_emit_*.py` scripts + `_v11_paper_numbers.py` into it. Mirrors the `_v10_verification/` and `_v11_validation/` pattern and matches the implicit convention. |
| **Top-of-`docs/` legacy drafts** | v8 + v9 + v10 (no `_1`) drafts, both `.md` and `.docx`, sit in `docs/` instead of `docs/versions/` | MOVE all v8/v9/v10 (no `_1`) drafts to `docs/versions/` (matches stated policy in `docs/versions/README.md`) |
| **`docs/beyond_recall_test.aux` reference** | `docs/versions/README.md` notes a Windows file lock previously prevented moving a `.aux` file. Confirmed not present at top of `docs/` now — already resolved. | No action |
| **Mixed underscore prefix usage in `scripts/`** | `_v10_*` (script that reads v10), `_v11_*` (script that reads v11), `_partb_*`, `_p0b_*`, `_probe_*`, `_diag_*`, `_check_*`, `_examine_*`, `_sample_*`, `_audit_*`, `_battery_leakage_results.json` (data file mixed in), `_per_question_outcomes_v2.json` (data file mixed in). The convention is unclear: underscore = "private/working", but it's mixed with stable infrastructure (`_judge_invocation/`, `_v10_verification/`, `_v11_validation/`, `_v11_emit_*`). | Adopt one convention: either reserve `_` prefix for "internal helper / not for external use" or for "working pass — to be archived." Currently it's both. |
| **Versioned figure scripts** | Three families have v1/v2/v3 living side-by-side in `scripts/`. The `_v3` is current. | After confirming `_v3` is the cited generator (and keeping if so), move v1/v2 of each family to `scripts/_archive/` or delete |
| **`docs/research/v11_panel_completeness_waivers.json.bak`** | A `.bak` file in a load-bearing data dir | DELETE |
| **`scripts/extract_v9_comments.py` vs `extract_v10_1_comments.py`** | Each is version-specific. v10.1 is current; v9 extractor is dead code | ARCHIVE the v9 extractor |
| **Two `s114_word_annotations.md` files** | One at `docs/reviews/s114_word_annotations.md` (134 KB, 2026-04-23), one at `docs/reviews/_archive/s114_word_annotations.md`. Likely the same content, archived twice | Verify content, then keep one canonical copy (probably the one in `_archive/`) |

---

## Empty / near-empty directories

None found. All directory listings have content.

(Note: `scripts/__pycache__` is non-empty but is a build artifact, listed under high-confidence delete.)

---

## Concerning findings

1. **`docs/~WRL0003.tmp` (3.3 MB) and `~$yond_recall_v10_1_draft.docx` (162 B)** — These indicate an open or recently-crashed Word session on the v10.1 docx. If Word is currently open editing the v10.1 docx, deleting `~WRL0003.tmp` will lose any unsaved buffer. Check Word state before deleting. The `~$` lock file is safe to delete after closing Word.

2. **Naming/path inconsistency for v11 emit infrastructure.** The architecture doc (`docs/research/v11_emit/_ARCHITECTURE.md` §2) describes scaffold scripts; the scripts are flat-named in `scripts/`. An external reproducer following the architecture doc could easily look for `scripts/_v11_emit/` (which does not exist) before finding `scripts/_v11_emit_4_1_gradient.py`. Worth either renaming to a directory, or adding a `scripts/_v11_emit/README.md → ../v11_emit_*.py` pointer.

3. **`scripts/__pycache__/` contains compiled bytecode for v11 emit scripts.** That means these scripts have been imported / executed. It's not a cleanup risk per se but confirms the v11 scaffolds are live, validating the recommendation to keep them.

4. **Duplicate `s114_word_annotations.md`** — same filename in `docs/reviews/` and in `docs/reviews/_archive/`. Verify they are identical content before consolidating.

5. **`docs/research/wrong_spec_detection_raw.json` (2.2 MB)** is the largest single research-dir file and IS cited in v10.1/v11. Keep, but note it's the dominant size driver in `docs/research/`.

6. **`results/` is 354 MB.** Out of scope for this audit (raw experimental data preserved per task constraint), but worth noting if a future "release-tag with frozen results" strategy is wanted, snapshotting to a git-LFS or external store could shrink the live tree substantially.

---

## Summary

- **High-confidence delete candidates: 17 files + 3 `__pycache__` dirs** (~7-8 MB + bytecode caches).
- **Medium-confidence candidates: ~80 files / dir-moves** spanning old paper drafts (move to `docs/versions/`), versioned figure-generation scripts, per-version review scripts, investigative `_probe_*` / `_diag_*` scripts, `docs/research/` scratch files, and S114-era review artifacts in `docs/reviews/` (most should move to `_archive/`).
- **Naming/organization fixes: 7** (most consequential: create `scripts/_v11_emit/` directory; move v8/v9/v10 drafts to `docs/versions/`).
- **Estimated repo size reduction:** 10-15 MB in high-confidence + medium-confidence file deletes (excluding `workspace/` which is regeneratable but live tooling). Bigger wins available only by archiving `results/` to LFS, which is out of scope.

### Three highest-priority cleanups

1. **Delete the four Word/LaTeX/log temp files at the top of `docs/`** (`~$yond_recall_v10_1_draft.docx`, `~WRL0003.tmp`, `beyond_recall_v10_1_draft.docx.bak`, plus the four files in `docs/versions/_latex_test_artifacts/`). Confirm Word is closed before deleting `~WRL0003.tmp`. Quick win, ~6 MB and removes obvious crap from the repo root.

2. **Move v8 / v9 / v10 (no `_1`) draft files (.md, .clean.md, .docx) from `docs/` to `docs/versions/`.** This is what the existing `docs/versions/README.md` policy says should happen; right now top-of-`docs` is cluttered with eight legacy paper files. ~10 MB shifted, much cleaner repo root.

3. **Reorganize the v11 emit scripts.** Either: (a) move all `_v11_emit_*.py` and `_v11_paper_numbers.py` into a new `scripts/_v11_emit/` directory to mirror `_v11_validation/` and `_v10_verification/`, OR (b) rename those sibling directories to use the same flat-prefix convention. The current mix is confusing for an external reproducer.

### Concerning findings (one-line each)

- Active Word session may have unsaved buffer in `~WRL0003.tmp` — verify before delete.
- `scripts/_v11_emit/` directory referenced in some context does not exist (scripts are flat-named).
- Possible duplicate of `s114_word_annotations.md` in `docs/reviews/` and `docs/reviews/_archive/` — verify content before consolidating.
