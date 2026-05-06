# Repository Completeness Audit — v8 draft

**Auditor:** Claude (Opus 4.7, 1M context)
**Date:** 2026-04-22
**Paper draft audited:** `docs/beyond_recall_v8_draft.md` (1,738 lines, complete through §8)
**Scope:** Cross-reference every file path in the paper against the filesystem, flag dead weight, confirm README currency, and verify all canonical data/script/doc entry points.

---

## 1. Broken paths in the paper

The paper cites these paths; the files do not exist at the cited locations. Each was verified with a follow-up check for renamed/moved equivalents.

### 1a. FIXABLE — mechanical path corrections (applied below)

| Paper cite | Reality | Fix applied |
|---|---|---|
| `results/_letta_rerun/{subject}_judgments_{judge}.json` (§4.7) | Data and scripts both live at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json` | Paper updated to cite `docs/research/_letta_rerun/...` |
| `scripts/run_letta_stateful_test.py` (§4.7) | No single script by this name. Actual scoring chain is numbered scripts under `docs/research/_letta_rerun/` (`20_run_c2a_named.py`, `40_judge_responses.py`, `70_compute_5judge_primary.py`) | Paper updated to point at `docs/research/_letta_rerun/` directory as the script set |
| `scripts/run_global_rerun.py` (§1.2 condition table, §1.3 mechanism para, §3.5 wrong-spec para, §4.1.2 pilot para, §4.3 Example A, Table in §4.3) | Script actually lives outside the public study repo at `memory_system/data/experiments/memory_systems/run_global_rerun.py`. To keep paper self-contained, the script has been **copied** into `memory-study-repo/scripts/run_global_rerun.py`. | Copy added; paper citations now resolve. |
| `data/<subject>/results.json`, `data/<subject>/judgments.json`, `data/<subject>/responses/C<condition>.json` (§3.5, §3.7) for Hamerton and Franklin | Hamerton responses/judgments live at `results/hamerton/`. Franklin responses/judgments at `results/franklin/` and (per-judge) `results/franklin_legacy_20260411/analysis/`. | Paper §3.5 and §3.7 updated to reflect actual layout. |
| `results/memory_systems/<system>/<subject>/C<id>.json` and `results/memory_systems/<system>/<subject>/*_judgments_<judge>.json` (§3.5, §3.7) | Memory-system outputs are **flat** inside each subject directory: `results/global_<subject>/<system>_results.json`, `results/global_<subject>/<system>_judgments_<judge>.json`, with `<system>` ∈ {mem0, letta, supermemory, zep, baselayer} and `_fullpipeline` suffix for native configs. No nested `memory_systems/` subtree. | Paper §3.5 and §3.7 updated to describe the flat layout. |
| `results/anchor_crossing_analysis.json` (§3.7.3) | Per-subject anchor-crossing data lives at `docs/research/s114_anchor_crossing_examples.json`. Computed inline by `scripts/compute_anchor_crossing.py`. | Paper updated to point to `docs/research/s114_anchor_crossing_examples.json` and the computing script. |

### 1b. FLAG — missing, no obvious target, requires author decision

| Paper cite | Notes |
|---|---|
| `results/interjudge_agreement/` (§3.7.4) | No such directory exists. Pairwise Spearman and Krippendorff α values are computed inline by analysis scripts but no persisted matrix file exists. Author should either generate a persisted matrix file, or change the paper to reference the computing script (`scripts/compute_*.py` does not have an obvious owner for this particular analysis). |
| `docs/research/_content_analysis_results.json` (§4.7 content comparison) | No such file in repo. The referential-density numbers (Babur 540 vs. 46, Ebers 58 vs. 19) appear only in the paper and `docs/reviews/session_close_handoff_v8_complete.md`. No persisted analysis file backs them. Author should either persist the counts to a JSON file under `docs/research/` or remove the citation. |
| `scripts/compute_question_improvement_rate.py` (§4.2 data line; also referenced in `KEY_FINDINGS.md` M11) | No such file. The question-improvement-rate table in §4.2.1 appears to have been computed inline/ad-hoc. `scripts/generate_fig_4_2_1.py` consumes the output but does not compute it. Author should either write this script or revise the paper citation to point at wherever the rates actually come from. |
| `_internal/aarik_clean_pilot/` (§4.1.2) | Explicitly private per the paper text itself ("not included in the public repository"). No fix needed; paper already flags it. |

---

## 2. Canonical data verified present

All files below exist exactly where the paper cites them.

### Per-subject data (13 global subjects)

Every one of augustine, babur, bernal_diaz, cellini, ebers, equiano, fukuzawa, keckley, rousseau, seacole, sunity_devee, yung_wing, zitkala_sa has all of:

- `results/global_<subject>/battery_v2.json` ✓
- `results/global_<subject>/battery_gpt54.json` ✓ (Control 1 circularity)
- `results/global_<subject>/results_v2.json` ✓
- `results/global_<subject>/judgments_v2.json` ✓
- `results/global_<subject>/c8_c9_results.json` ✓

Every subject also has per-system outputs (mem0, letta, supermemory, zep, baselayer) in both controlled and `_fullpipeline` (native) variants.

### Hamerton

`results/hamerton/` present with full condition set (baselayer, letta, mem0, supermemory, zep; c8/c9; Gemini Pro and GPT-4o/5.4 judgments). `data/hamerton/battery.json` present.

### Franklin

`results/franklin/` and `results/franklin_legacy_20260411/` both present. `data/franklin/battery.json` present. Paper §4.1.1 cites `results/franklin_legacy_20260411/` — this exists.

### Tier 2 (cross-provider replication)

`results/_tier2/` present with `global_ebers/`, `global_yung_wing/`, `global_zitkala_sa/` each containing `tier2_sonnet_*` and `tier2_gemini_pro_*` files. Matches §3.4.1 / §4.5.1.

### Wrong-spec v2 (random derangement)

`results/_wrong_spec_v2/` present with all 13 global subject subdirectories plus `hamerton_results.json` and a manifest.

---

## 3. Canonical scripts verified present

All present at `scripts/`:
- `compute_wrong_spec_5judge.py`
- `compute_wrong_spec_per_subject.py`
- `compute_memory_systems_5judge.py`
- `classify_hedging.py`
- `recompute_5judge_primary.py`
- `analyze_mlz_c1_vs_c3.py`
- `analyze_baselayer_c1_vs_c3.py`
- `analyze_sm_c1_vs_c3.py`
- `_verify_battery_leakage.py`
- `audit_low_end_inflation.py`
- `run_global_subjects.py`
- `run_full_study.py`
- `run_multimodel_responses.py`
- `compute_anchor_crossing.py`
- `compute_hedging_rates.py`
- `compute_spec_activation.py`
- `classify_wrong_spec_detection.py`
- `generate_fig_4_1_gradient_scatter.py`
- `generate_fig_4_2_compression.py`

Absent (see §1 above): `run_global_rerun.py` (fixed by copy), `run_letta_stateful_test.py` (pointer fix), `compute_question_improvement_rate.py` (flagged).

---

## 4. Canonical research docs verified present

All present at `docs/research/`:
- `supermemory_c1_vs_c3_paired_analysis.md` ✓
- `mem0_letta_zep_c1_vs_c3_analysis.md` ✓
- `baselayer_c1_vs_c3_paired_analysis.md` ✓
- `letta_stateful_matched_rerun.md` ✓
- `letta_stateful_deep_read.md` ✓
- `recompute_5judge_primary.md` ✓
- `memory_systems_5judge_primary.md` ✓
- `hedging_analysis.json` ✓
- `spec_activation_analysis.json` ✓
- `wrong_spec_detection_analysis.md` ✓
- `provider_benchmarks.md` ✓

---

## 5. Stale labels — "Franklin-for-all" cleanup

The prior correction pass established that the v1 wrong-spec control is a **fixed derangement for cultural/temporal distance** (13 global subjects, pairing in `run_global_rerun.py` WRONG_SPEC_PAIRING), **not** "Franklin's spec applied to all." That label is stale. The paper itself (v8) uses the correct label. Support docs with stale copies:

| File | Lines | Status |
|---|---|---|
| `README.md` | L63, L84 | **FIXED** (this pass) |
| `docs/blog_post_v2.md` | L137, L140 | **FIXED** (this pass) |
| `docs/PAPER_CORRECTIONS.md` | L51 | **FIXED** (this pass) — annotated as historical record |
| `docs/reviews/session_close_handoff_v8_complete.md` | multiple | Historical session record; not updated. Retain as-is for provenance. |
| `docs/reviews/s114_*.md` | multiple | Historical review records; retain as-is. |
| `scripts/run_full_study.py` | L47 comment | Accurate — this is the Hamerton-only Franklin-for-all pre-globals test, correctly labeled. Do not change. |
| `docs/beyond_recall_v6_draft.md` | L959 | Frozen prior version; do not edit. |

Paper location references (docs saying "Paper location: Table X in `beyond_recall_v6_draft.md`"): DATA_REFERENCE.md, KEY_FINDINGS.md, METHODOLOGY.md, PROVENANCE_INDEX.md all still reference v6. Flagged in §7 README fixes — these should be bulk-updated to v8 before launch but involve re-verifying that every "Paper location: §X" still maps to the right section in v8 and is not a mechanical find-and-replace.

---

## 6. Dead-weight candidates (author decision — do NOT delete)

### Historical draft files in `docs/` (top level)

These should plausibly move to `docs/versions/` before the repo goes public to avoid reviewer confusion. Flag for author decision:

- `beyond_recall_arxiv_draft.md` (the S105 baseline draft; v6 supersedes it)
- `beyond_recall_arxiv_draft.docx`, `beyond_recall_arxiv_draft_v2.docx`, `_v3.docx`, `_v4.docx`, `_v5.docx` (iterative Word exports)
- `beyond_recall_v6_draft.md` (now fully superseded by v8; v8 line 12 calls v6 "the reference source for sections not yet re-locked" — with v8 complete through §8 plus §6-§7-§8, this statement is obsolete)
- `beyond_recall_v7_draft.md` (intermediate draft)
- `beyond_recall_v7_review.clean.md`, `beyond_recall_v7_review.docx` (v7 review artifacts)
- `beyond_recall_review.clean.md`, `beyond_recall_review.docx`, `beyond_recall_review.html` (v6-era review HTML/DOCX)
- `beyond_recall_test.aux`, `.log`, `.out`, `.tex`, `.pdf` (LaTeX test-build intermediates; `.aux` and `.log` in particular are never useful to readers)

### Historical review artifacts in `docs/reviews/`

- `round_01_*.md` (3 files, S105 round 1 reviews)
- `round_02_*.md`, `round_02_focused_*.md`, `round_02_groq_minimal_*.md`, `round_02_*_payload_*.md` (multiple round-2 review artifacts)
- `round_03_*.md`, `round_06_*.md` (intermediate-round reviews)
- `gemini_draft_review.md`, `gemini_abstract_review_*.md`, `gemini_flash_paper_review_v2.md`, `gemini_pro_paper_review_v2.md`, `gemini_pro_final_review.md`, `gemini_gemini-25-flash_full_review_v3.md` (earlier Gemini reviews against v5/v6)
- `s114_*.md` (7 files: S114 session review artifacts from 2026-04-21 — useful as context for v8 voice pass but clutter before public release)
- `section_4_6_gemini_retry.md`, `section_4_6_review_*.md`, `_section_4_6_payload.md` (intermediate section reviews)
- `gtm_jargon_scan_*.md` (2 files — GTM language audit outputs)

### Historical research scratch in `docs/research/`

The following appear to be exploratory/probe artifacts that do not feed any paper number. Flag only — author should decide:
- `_analyze_score_bands.py`, `_band_examples.txt`, `_build_score_pool.py`, `_print_band_examples.py`, `_score_band_pool.json`, `_score_band_stats.json`, `_recompute_variance_full_pool.py`
- `_baselayer_c1_c3_candidates.json`, `_mlz_c1_c3_candidates.json`, `_sm_c1_c3_candidates.json`, `_sm_paired_5judge.json`
- `name_blind_wrong_spec_pilot.md`, `score_interval_significance.md`, `section_*_verification.md` (6 verification files)
- `s114_*.json` (4 files: anchor-crossing examples, diverse examples, low-end inflation audit, parse-failure manifest)
- `tier2_recompute_s114.json`, `wrong_spec_detection_raw.json`, `wrong_spec_validation_sample.json`

### Scripts directory historical/probe files

Private probes and one-off diagnostics in `scripts/` that start with underscore and look historical:
- `_check_babur_sm.py`, `_examine_bernal_diaz.py`, `_probe_*.py` (5 files), `_sample_explicit.py`, `_validate_classifier_sample.py`, `_verify_battery_leakage.py` (keep), `_verify_claims.py`, `_wait_for_classifier.py`, `_write_wrong_spec_report.py`, `_battery_leakage_results.json`
- Round-review scripts: `review_paper.py`, `review_paper_round2*.py` (3), `review_paper_round3.py`, `review_benchmark_metric.py`, `review_compression_framing.py`, `review_section_4_6*.py` (2), `review_section4_plan.py`, `review_round6.log`, `title_panel_review.py`, `final_locked_content_review.py`, `scan_*.py` (2), `sm_paired_5judge_examples.py`, `collective_analysis_examples.py`
- Docx/format utilities: `build_review_html.py`, `build_v8.py`, `export_to_docx.py`, `export_v7_to_docx.py`, `extract_docx_annotations.py`, `remove_em_dashes.py`

Author decision: keep a subset in `scripts/` for reproducibility of each round, archive the rest to a `scripts/_archive/` or similar.

### Top-level results directory

- `results/letta_manifest.json`, `letta_analysis.json`, `mem0_*`, `supermemory_*`, `zep_*` (top-level per-provider analysis/manifest files alongside the per-subject directories) — these are aggregate manifests, likely fine to keep but author should confirm they reflect v8 numbers.

---

## 7. README update recommendations

Top-level `README.md` is stale in multiple ways. Fixes applied this pass:

1. **Paper reference:** Was `beyond_recall_v6_draft.md` → now `beyond_recall_v8_draft.md`.
2. **Wrong-spec v1 label:** Was "Franklin's spec applied to 13 other subjects" → now "fixed derangement designed for cultural/temporal distance (pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING)".
3. **Key Findings stats:** Slope was `−0.98 [95% CI −1.30, −0.74]` (from DATA_REFERENCE using the 7-judge aggregate). Paper v8 uses 5-judge primary: slope `−0.96 [95% CI −1.24, −0.67]`, R² 0.82, p < 0.001. Updated to 5-judge primary.
4. **Wilcoxon p-values:** README had `C5 vs C2a W=10.0, p=0.0076` and `C5 vs C4a W=9.0, p=0.0063` (7-judge). Paper v8 uses `C5 vs C2a p=0.005, W=10` and `C5 vs C4a p=0.007, W=11` (5-judge primary). Updated.
5. **Low-baseline mean gain:** README silent. v8 reports `+0.89` mean Δ_C4a on low-baseline slice. Added.
6. **Krippendorff α:** README says `0.535 (all 7)` and `0.659 (non-Gemini 5)`. Paper v8 agrees. Retained.
7. **Letta stateful finding:** README says "parity result at 65% context size (n=1, Hamerton)" with scores from §4.3.1 of v6. Paper v8 now reports N=3 (Hamerton, Ebers, Babur) with Letta-block > BL-spec on all three, 5-judge primary Δ +0.14/+1.05/+0.54 (see `docs/research/letta_stateful_matched_rerun.md`). README updated to reflect N=3 and §4.7.
7. **Reproduction-step doc pointers:** README listed `docs/beyond_recall_v6_draft.md` as main draft. Updated to v8. `docs/METHODOLOGY.md` and `docs/PROVENANCE_INDEX.md` still have "Paper location: ... v6_draft.md" entries internally — flagged for author pass.

Fixes NOT applied (author decision):
- Archiving v6/v7/review/test drafts to `docs/versions/`.
- Bulk-updating "Paper location: ...`beyond_recall_v6_draft.md`" strings inside DATA_REFERENCE.md / KEY_FINDINGS.md / PROVENANCE_INDEX.md to v8 (each entry needs §-section remapping, not a pure find-and-replace).
- Deciding whether to keep or archive `figures/fig1_global_gradient.png` through `fig11_tier2_replication.png` (the original S113 figures) alongside the v8 `fig_4_1_*`, `fig_4_2_*`, `fig_4_2_1_*` figures.

---

## 8. Summary of applied fixes

**Paper (`docs/beyond_recall_v8_draft.md`) — broken path corrections:**
1. §3.5 — `results/memory_systems/<system>/<subject>/C<id>.json` → updated to actual flat layout.
2. §3.7 — same correction for per-judge judgments line.
3. §3.5 — Hamerton/Franklin response location corrected.
4. §3.7 — Hamerton/Franklin judgments location corrected.
5. §3.7.3 — `results/anchor_crossing_analysis.json` → `docs/research/s114_anchor_crossing_examples.json`.
6. §4.7 — `results/_letta_rerun/` → `docs/research/_letta_rerun/` (and script pointer).

**Support docs — stale label cleanup:**
7. `README.md` — v6 → v8, wrong-spec v1 label, 5-judge primary stats, Letta N=3 finding.
8. `docs/blog_post_v2.md` — wrong-spec v1 label corrected.
9. `docs/PAPER_CORRECTIONS.md` — annotated stale Franklin-for-all entry with note.

**New file:**
10. `scripts/run_global_rerun.py` — copied from `memory_system/data/experiments/memory_systems/` so paper self-references work inside the public repo.

---

## 9. Remaining items for author decision (not fixed)

1. Generate or remove: `results/interjudge_agreement/` matrix file.
2. Generate or remove: `docs/research/_content_analysis_results.json` for §4.7 referential-density numbers.
3. Write or revise citation: `scripts/compute_question_improvement_rate.py` (§4.2 data line).
4. Archive historical drafts (`v6_draft.md`, `v7_draft.md`, `.docx`/`.aux`/`.log`/`.tex`/`.pdf` artifacts) to `docs/versions/` before public release.
5. Archive historical review rounds (`round_0*.md`, `gemini_*_review*.md`, `s114_*.md`) to a `docs/reviews/_archive/` before public release.
6. Bulk-update "Paper location: `beyond_recall_v6_draft.md`" → v8 inside `DATA_REFERENCE.md`, `KEY_FINDINGS.md`, `PROVENANCE_INDEX.md`, `FILE_NAMING.md`, `REFERENCE_TABLE.md`, with §-section remapping (requires review).
7. Decide whether S113-era figures (`fig1_*.png` through `fig11_*.png`) are archived or retained alongside the v8 `fig_4_1_*`/`fig_4_2_*`/`fig_4_2_1_*` set.
8. Scripts directory cleanup: private probes (`_probe_*.py`, `_check_*.py`, `_examine_*.py`, etc.), review-round scripts, export utilities — archive vs. keep.
