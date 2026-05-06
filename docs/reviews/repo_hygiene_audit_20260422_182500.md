# Repository Hygiene Audit — v8 pre-publication

**Auditor:** Claude (Opus 4.7, 1M context)
**Date:** 2026-04-22
**Scope:** Organization, naming conventions, and traceability. Distinct from and complementary to `repo_completeness_audit_20260422_173831.md` (which asks "does it exist?"); this pass asks "is it well-organized, consistently named, and traceable?".
**Non-scope:** File contents, paper claims/numbers (see completeness audit, review rounds, and the separate figure review), figure quality, script correctness.

---

## Summary grades

| Folder / area | Grade | One-line reason |
|---|:---:|---|
| Top-level repo | A- | README, AGENTS.md, agents/, CITATION.cff, LICENSE, clean top-level layout. |
| `docs/` | B → A- after this pass | Top level was cluttered with v6/v7/arXiv drafts and LaTeX test artifacts (A/F-grade clutter). Now clean: only v8 + authoritative refs. |
| `docs/reviews/` | C → A- after this pass | Had 40 files mixing 2026-04 gate review with 2026-04-14 round_01 and 2026-04-18 round_02. Now 11 at top level + 29 in `_archive/`. |
| `docs/versions/` | B+ | Destination now holds 18 snapshots + LaTeX subfolder with an updated README. |
| `docs/research/` | B | Good logical grouping. Leading-underscore helpers are well-documented in the folder README, but the leading-underscore convention collides with the folder convention (see Naming below). |
| `docs/internal/` | A- | Clear "not for public consumption" scoping; small, focused set. |
| `data/` | B+ | Sensible subject-per-folder, README per folder. Minor asymmetry: `data/global_subjects/<subject>/` vs `data/hamerton/` (flat, no parent folder). |
| `results/` | B | Sensible per-subject layout, but uses `results/global_<subject>/` while `data/global_subjects/<subject>/` drops the prefix — two conventions for the same 13 subjects (see Naming). |
| `results/_s114_backfills/` | C | Uses **double-underscore** separators (`global_augustine__C1_baselayer__gemini_flash.json`) — inconsistent with every other folder in the repo. Load-bearing enough that renaming now would break references; flag for post-launch cleanup. |
| `scripts/` | C | 93 files at one level. `_probe_*`, `_check_*`, `review_paper_round2*`, export utilities, and one-off diagnostics mix with the canonical runners. Convention noted in research/README (leading `_` = helper) is not visibly applied here. |
| `figures/` | B+ | Has fig1-11 (v6-era, 7-judge) alongside fig_4_1/4_2/4_2_1 (v8-era, 5-judge). README discloses. Flagged below. |
| `charts/` | B+ | Exploratory set; README discloses it predates the `figures/` set. |
| `agents/` | A | Three files, cleanly scoped. |
| `workspace/` | A | Build artifact (search index); appropriately named and isolated. |

---

## 1. Per-folder assessment

### 1a. `docs/` (top level)

**Before this pass:**
- 21 `beyond_recall_*` files intermingled at top level: v8 current + v7 + v6 + `arxiv_draft` + `arxiv_draft_v2` through `_v5` .docx + review .docx/.html/.clean.md + LaTeX `.aux/.log/.out/.pdf/.tex` test-build intermediates.
- Any reader opening `docs/` could not tell at a glance which draft was current.

**Fix applied:**
- Moved v6_draft, v7_draft, v7_review (.docx + .clean.md), arxiv_draft (.md + 5 .docx), review (.docx + .clean.md + .html) → `docs/versions/`.
- Created `docs/versions/_latex_test_artifacts/` subfolder.
- Moved 4 of 5 LaTeX test-build intermediates (`beyond_recall_test.tex`, `.log`, `.out`, `.pdf`) → `docs/versions/_latex_test_artifacts/`.
- `beyond_recall_test.aux` could not be moved due to a persistent filesystem sandbox block on that one file. Flagged as manual-move item below.
- Updated `docs/README.md`, `docs/versions/README.md`, and `docs/reviews/README.md` to reflect the new layout and name v8 as canonical.

**Result after pass:** `docs/` top level now contains only: the 7 ALL_CAPS reference docs, README.md, v8_draft (.md + .clean.md + .docx), blog_post_v2.md, `_results_snapshot.txt`, and the four subfolders (`internal/`, `research/`, `reviews/`, `versions/`). Plus `beyond_recall_test.aux` (manual-move needed).

### 1b. `docs/reviews/`

**Before this pass:** 40 files at top level mixing the current v8 gate review (dated 2026-04-22) with round_01 (2026-04-14), round_02 (2026-04-18), round_03, round_06, six gemini-* reviews of v2/v3/pre-v6 drafts, the GTM jargon scan, multiple S114 session review artifacts, and section-4.6 review retries.

**Fix applied:**
- Created `docs/reviews/_archive/` and moved 29 historical files into it:
  - All 12 `round_0*` files.
  - All 6 historical `gemini_*_review*` files (predating v8).
  - 6 of 8 `s114_*` files (the session-internal review artifacts: benchmark_metric, compression_framing, example_analysis, section4_planning, title_panel, word_annotations).
  - Both `gtm_jargon_scan_*` files.
  - Three `section_4_6_*` files (retry, review, payload).
- Updated `docs/reviews/README.md` to reflect the new layout and v8-as-current.
- Updated cross-references in `agents/STUDY_MEMORY.md` and in two session logs (`s114_session_summary.md`, `s114_paragraph_review.md`) where paths to the archived files were quoted.

**Retained at top level (11 files):** README.md, the v8 gate review (`full_paper_gate_review_*`, `gate_review_synthesis_*`), `session_close_handoff_v8_complete.md`, `s114_full_data_audit.md`, `s114_final_locked_content_review_20260421_215603.md`, the two session logs (`s114_paragraph_review.md`, `s114_session_summary.md`), `s114_session_close_handoff.md`, `figure_review_20260422.md` (from parallel agent), `repo_completeness_audit_20260422_173831.md`, and this hygiene audit.

**Flag for author:** `s114_final_locked_content_review_20260421_215603.md` and `s114_session_close_handoff.md` are ambiguous — session-internal but potentially referenced in current drafts. Left in place pending author review.

### 1c. `docs/versions/`

**Before this pass:** 4 files (README + 3 versioned).

**After pass:** 18 files (13 draft snapshots + 2 blog snapshots + README) + `_latex_test_artifacts/` subfolder. README updated to explain every file.

### 1d. `docs/research/`

**No files moved** — folder is well-organized and README.md explains the leading-underscore convention for helper scripts. Minor inconsistency: the leading underscore is overloaded (see Naming §2).

### 1e. `docs/internal/`

**No files moved** — clearly scoped "not for public consumption," small set of 5 working docs.

### 1f. `scripts/` (93 files at one level)

**No mass moves applied** — per advisor guidance, propose-don't-execute, because (a) the repo lacks a scripts/_archive/ precedent, and (b) several leading-underscore scripts (especially `_verify_battery_leakage.py`) are referenced as canonical data-integrity checks in `STUDY_MEMORY.md`. Moving them changes an active reference.

**Proposed scripts/_archive/ candidates (author decision — do NOT auto-move):**
- `review_paper_round2.py`, `review_paper_round2_focused.py`, `review_paper_round2_groq_minimal.py`, `review_paper_round3.py`, `review_paper.py`, `gemini_review_script.py`, `gate_review_cerebras_retry.py`, `gate_review_v8_retry.py`, `review_benchmark_metric.py`, `review_compression_framing.py`, `review_section_4_6.py`, `review_section_4_6_gemini_retry.py`, `review_section4_plan.py`, `title_panel_review.py`, `final_locked_content_review.py`, `review_round6.log` — one-off cross-LLM review scripts for specific rounds / sections. Retain the latest (`gate_review_v8.py`) as primary.
- `scan_gtm_jargon.py`, `scan_parse_failures.py`, `sm_paired_5judge_examples.py`, `collective_analysis_examples.py` — one-off scans.
- `export_to_docx.py`, `export_v7_to_docx.py`, `build_review_html.py`, `remove_em_dashes.py`, `extract_docx_annotations.py` — format utilities. Retain `export_v8_to_docx.py` + `build_v8.py` as primary.
- `_check_babur_sm.py`, `_examine_bernal_diaz.py`, `_probe_hedge_variants.py`, `_probe_keckley_q21.py`, `_probe_retrieval_styles.py`, `_probe_top_examples.py`, `_probe_zep_facts.py`, `_probe_zep_response.py`, `_sample_explicit.py`, `_validate_classifier_sample.py`, `_verify_claims.py`, `_wait_for_classifier.py`, `_write_wrong_spec_report.py`, `_battery_leakage_results.json` — private probes. **Retain `_verify_battery_leakage.py` (canonical data-integrity check, referenced in `STUDY_MEMORY.md`).**

If the author approves, a single move (all the above into `scripts/_archive/`) would take `scripts/` from 93 files to ~45.

### 1g. `data/`, `results/`

**No files moved.** Both are data folders; renaming would break scripts. Naming asymmetry between `data/global_subjects/<subject>/` and `results/global_<subject>/` is flagged below, not fixed.

### 1h. `figures/`, `charts/`

**No files moved.** `figures/README.md` already explains that `fig1_*`-`fig11_*` are v6-era (7-judge) and `fig_4_1_*`/`fig_4_2_*`/`fig_4_2_1_*` are v8-era (5-judge primary). I added an "archive candidate" note in the README.

---

## 2. Naming inconsistencies (inventory)

### 2a. Subject-folder prefix asymmetry

- `data/global_subjects/augustine/` ... `/zitkala_sa/` — **no prefix**
- `results/global_augustine/` ... `/global_zitkala_sa/` — **`global_` prefix**
- `results/_wrong_spec_v2/global_augustine/` — prefixed (matches `results/`)
- `results/_tier2/global_ebers/` — prefixed (matches `results/`)

The same 13 subject names use two different conventions depending on which top-level folder you're in. Not fixable now without breaking scripts; note in docs/FILE_NAMING.md as a documented-inconsistency rather than trying to resolve.

**Additional asymmetry:** `data/hamerton/` and `data/franklin/` sit at the same level as `data/global_subjects/` (which contains subject subdirs). Hamerton is in effect a 14th subject but lives one level up. `data/FILE_NAMING.md` already explains this is historical (Hamerton was first).

### 2b. Separator convention in `results/_s114_backfills/`

The 125 files in this folder use **double-underscore** as separator:
```
global_augustine__C1_baselayer__gemini_flash.json
global_babur__C8_raw_corpus__gpt4o.json
```
Everywhere else in the repo the convention is **single-underscore**:
```
baselayer_judgments_gemini_flash.json
c8_c9_judgments_gpt4o.json
```
The double-underscore is a one-off separator choice for session-backfill provenance; inside the file the fields still follow the standard ordering (subject-system-condition-judge). Retain for now; note in `FILE_NAMING.md`; consider consolidating during post-launch cleanup.

### 2c. Date formats

Three different date conventions in `docs/reviews/` alone:

- `round_01_20260414_121257.md` — compact `YYYYMMDD_HHMMSS` timestamp.
- `gemini_pro_paper_review_v2.md` — no date, just version suffix.
- `s114_title_panel_20260421_154300.md` — session tag + compact timestamp.
- `gtm_jargon_scan_20260422_152228.md` — compact timestamp without session tag.
- `session_close_handoff_v8_complete.md` — no date, descriptive suffix.

`FILE_NAMING.md` already specifies the compact `YYYYMMDD_HHMMSS` as the convention; older files predate the convention. No retroactive renaming needed since most are now in `_archive/`.

### 2d. Leading underscore — two semantics collide

- **Folders:** `results/_tier2/`, `results/_wrong_spec_v2/`, `results/_s114_backfills/`, `docs/research/_letta_rerun/`, `docs/research/_letta_blocks/`, `docs/reviews/_archive/`, `docs/versions/_latex_test_artifacts/` — means "computed off the main tree / archival / special-purpose subtree."
- **Files:** `docs/research/_analyze_score_bands.py`, `_build_score_pool.py`, `scripts/_probe_*.py`, `scripts/_verify_battery_leakage.py` — means "supporting script / probe / internal helper."

Both semantics are documented (FILE_NAMING.md rule 5 for folders; research/README.md and scripts/README.md for files), but the character is overloaded. Recommend keeping both conventions and adding a sentence in `FILE_NAMING.md` rule 5 that explicitly acknowledges the overload.

### 2e. `.clean.md` suffix

`beyond_recall_v7_review.clean.md`, `beyond_recall_v8_draft.clean.md`, `beyond_recall_review.clean.md` — "cleaned markdown" for docx export. Undocumented convention. Add one line to `FILE_NAMING.md`.

### 2f. `_fullpipeline` vs `_fp`

Both appear in the repo. `FILE_NAMING.md` and the glossary in `STUDY_MEMORY.md` both accept both. File names uniformly use `_fullpipeline`; column labels in DATA_REFERENCE and a few analysis reports use `_fp`. No action — consistent enough.

### 2g. Singular vs plural folder names

All use plural correctly (`scripts/`, `results/`, `figures/`, `charts/`, `docs/`, `data/`, `agents/`). No issue.

### 2h. `fig_4_1_*` vs `fig1_*` — two generations of figure naming

`figures/` has both:
- Old (v6, 7-judge): `fig1_global_gradient.png` through `fig11_tier2_replication.png`
- New (v8, 5-judge primary): `fig_4_1_gradient_scatter.{png,pdf}`, `fig_4_2_compression.{png,pdf}`, `fig_4_2_1_question_improvement_rates.{png,pdf}`

The new set uses section-numbered names aligned with the paper; the old set uses ordinal names aligned with the earlier draft's figure ordering. Both live at the same level. Reader opening `figures/` sees 21 files and cannot tell which set the paper cites without reading the README. **Critical confuser.** Recommended fix: move `fig1_*`-`fig11_*` + `generate_figures.py`/`_v2.py`/`_v3.py` to `figures/_archive/`. Flagged — author decision (the figure-quality review agent may be touching these).

---

## 3. Traceability matrix — `PROVENANCE_INDEX.md` assessment

**One-sentence assessment:** PROVENANCE_INDEX is substantial (~85 claims across 11 sections) and already layered with an S113 addendum (v6-draft numbers); after this pass it also has an S115 addendum covering eight claim categories that appeared only in v8 or only in support docs.

**What's good:**
- Legend is explicit: VERIFIED / APPROXIMATE / NOT FOUND / DERIVED / S113 / (new) S115.
- The S113 corrections summary at the top is a model of traceability discipline.
- Source File Index at the bottom is a usable starting point.
- Every "Source File" row is a real path in the repo (verified during this pass for spot-checks).

**What's missing / problematic:**
1. **§-section references use v6 numbering.** Many rows say "Paper location: §4.1 line 626" referring to v6 line numbers. v8 renumbered some sections (most notably §4.3 / §4.7 split for Letta). Each row needs individual remapping; not a find-and-replace. Flagged in the completeness audit §7 and reflected in the S115 addendum.
2. **Missing claims now added in S115 addendum** (this pass):
   - §4.2.1 question-improvement rates (70.9/72.9/78.3/78.6; median Δ +1.00 / −0.40)
   - §4.7 Letta stateful N=3 (Hamerton +0.14 / Ebers +1.05 / Babur +0.54 at 5-judge primary)
   - §4.5 Wrong-spec v1 mean 1.86 and v2 mean 2.30 (7-judge) / 2.21 (5-judge)
   - 60.6% content-grounded wrong-spec detection rate
   - Hedging rates under the `starts_refusal` rule (28.8 → 1.4 → 0.0%) and broader `refusal_ge_1` rule (41.2 → 7.9 → 0.4%)
   - Anchor-crossing rates (55.0% low-baseline, 75.0% author pilot)
   - Spec-activation rates (78.6% correct-spec, 50.0% wrong-spec)
   - Provider recall-benchmark range claim (68-85%)
   - Author pilot numbers (flagged as not in public repo)
3. **Missing scripts flagged:** `compute_question_improvement_rate.py` referenced in paper §4.2 + KEY_FINDINGS M11 does not exist — rates are inlined in the figure script, not computed separately. Author should either write the compute script or reword the paper citation.
4. **Missing persisted files flagged:** `results/interjudge_agreement/` (Krippendorff/Spearman matrix) and `docs/research/_content_analysis_results.json` (§4.7 referential-density) do not exist; values computed inline only.

**Reverse lookup — does not exist.** No `SCRIPTS_INDEX.md` or equivalent mapping script → outputs → paper sections. Building one would take ~2 hours (list every script in `scripts/` and `docs/research/`, list its output files, list which §/table/figure in v8 cites those outputs). **Proposal:** Add a `docs/SCRIPTS_INDEX.md` post-launch; do not block launch on it.

**KEY_FINDINGS.md paper-section citations:** Spot-check says every entry (M1-M11, m12-m22) cites a paper section and a DATA_REFERENCE section. Good.

---

## 4. Cross-cutting findings

### 4a. READMEs

Every canonical folder has a README.md:
- Top-level: `README.md` — current with v8, correct flagship sentence, correct 5-judge primary stats.
- `data/`, `results/`, `scripts/`, `docs/`, `figures/`, `charts/`, `agents/` — all have READMEs.
- Per-subject folders under `data/global_subjects/<subject>/` and `results/global_<subject>/` — all have READMEs.
- `docs/versions/README.md` and `docs/reviews/README.md` — **updated this pass** (v6→v8, new `_archive/` noted, new file list).

**Stale v6 references still live in:** `DATA_REFERENCE.md` section headers, `KEY_FINDINGS.md` paper-location entries, `FILE_NAMING.md`, `REFERENCE_TABLE.md`, `METHODOLOGY.md`, `PROVENANCE_INDEX.md` pre-S115 sections. Each needs §-by-§ remapping, not find-and-replace. Flagged as author task.

### 4b. `AGENTS.md` / `STUDY_MEMORY.md` currency

- `AGENTS.md` — refers to "Session S114" state; paper is "through §8" in v8. Mostly accurate; one line still says "v6 draft was the primary" which is obsolete. No edit this pass (low priority, author-voice content).
- `STUDY_MEMORY.md` — updated this pass for one stale path reference (s114_section4_planning_*.md → `_archive/`).

### 4c. Scripts with ambiguous entry-point status

- `scripts/review_paper_round2.py` (and `_focused`, `_groq_minimal`) all point at `docs/beyond_recall_v6_draft.md` which now lives in `versions/`. The scripts will fail with file-not-found unless paths are updated. **Not fixed this pass** (changing script behavior is out of scope for organization/naming/traceability). Updated `scripts/README.md` to call this out explicitly.

### 4d. Path references across docs

- README.md says `docs/research/` holds "per-analysis reports (paired analyses, hedging, spec activation, Letta stateful)" — accurate.
- FILE_NAMING.md `Where to look` table says Letta stateful lives at `docs/research/_letta_blocks/` and `docs/research/_letta_rerun/` — accurate.
- The completeness audit applied a set of path corrections to v8 §3.5, §3.7, §3.7.3, §4.7. These are canonical now. Do not re-correct.

### 4e. `LICENSE` file empty

`LICENSE` exists at repo root but its size is unchecked by this audit. Completeness audit noted "License pending." Not a hygiene issue; flag for pre-publication.

---

## 5. Prioritized fix list

### Critical — blocks publication / confuses readers

1. **`figures/` two-generation problem** (author decision required). 11 v6-era figures live next to the v8 paper-referenced set; reader opening the folder sees 21 files and cannot tell which the paper cites. Recommended: create `figures/_archive/` and move fig1-11 + `generate_figures.py`/`_v2.py`/`_v3.py` there. Figure-review agent is running in parallel; coordinate.
2. **Missing `scripts/compute_question_improvement_rate.py`** — paper §4.2 data line and KEY_FINDINGS M11 cite a script that does not exist. Author must either write it (the inlined counts in `generate_fig_4_2_1.py` are the de facto source) or reword both citations.
3. **`beyond_recall_test.aux`** still at top level of `docs/` — a Windows filesystem sandbox block prevented moving this single file. Manual one-line fix by author: `move docs\beyond_recall_test.aux docs\versions\_latex_test_artifacts\`.

### High — visible inconsistency any careful reader would notice

4. **PROVENANCE_INDEX.md v6→v8 section-remap.** Each "Paper location: §X in v6_draft" row needs individual review. Do not bulk find-and-replace; several section numbers shifted (most notably Letta stateful §4.3.1 → §4.7). Author task, ~1 hour.
5. **`results/_s114_backfills/` uses double-underscore separator** — inconsistent with every other folder. 125 files would need renaming. Post-launch cleanup; not blocking.
6. **`scripts/review_paper_round2.py` et al. point at archived v6 draft path.** Either update the scripts or note in `scripts/README.md` that they are superseded. README updated this pass; scripts themselves left untouched.
7. **Propose scripts/_archive/** with ~45 files (round-review scripts, probes, format utilities). Author-decision.

### Low — minor polish

8. Add to `FILE_NAMING.md` rule 5: explicit acknowledgement that leading underscore has two semantics (off-main-tree folder vs helper script).
9. Add to `FILE_NAMING.md`: `.clean.md` = pre-docx export variant.
10. `data/global_subjects/<subject>/` vs `results/global_<subject>/` asymmetry — document as historical, do not fix.
11. Author pilot references (§4.1.2 `_internal/aarik_clean_pilot/`) — one-line "available on request" pointer in paper if not already there.
12. `docs/reviews/` has `s114_final_locked_content_review_20260421_215603.md` and `s114_session_close_handoff.md` — ambiguous whether current or archive-candidate. Author decision.

---

## 6. Flag for author decision

1. **Figure archive.** Move `figures/fig1_*`-`fig11_*` + `generate_figures.py`/`_v2.py`/`_v3.py` to `figures/_archive/`? (Coordinate with the figure-quality review agent.)
2. **Scripts archive.** Move ~45 one-off scripts (listed in §1f) to `scripts/_archive/`?
3. **`beyond_recall_test.aux`** manual move — the sandbox blocked only this one file.
4. **The two ambiguous `s114_*` files at `docs/reviews/` top level** — keep as current or move to `_archive/`?
5. **`LICENSE` file** — verify contents are actually Apache 2.0 before publication.
6. **`scripts/review_paper_round2*.py`** — update paths to v8, delete, or leave as-is with README disclaimer (current state)?
7. **PROVENANCE_INDEX v6 → v8 section-remap** — assign time; do not bulk replace.

---

## 7. What was applied mechanically this pass

**Moves (all to subfolders; no deletions):**
- 13 historical drafts + Word exports → `docs/versions/`
- 4 LaTeX test-build intermediates → `docs/versions/_latex_test_artifacts/` (5th, `.aux`, blocked by sandbox)
- 29 historical reviews → `docs/reviews/_archive/` (12 round_0*, 6 gemini_*, 6 s114_*, 2 gtm_*, 3 section_4_6_*)

**README / doc updates:**
- `docs/README.md` — new subfolder descriptions, archive notes, v6-provenance caveat.
- `docs/versions/README.md` — full new file list with subfolders.
- `docs/reviews/README.md` — v6 → v8, new `_archive/` explanation, review-script inventory updated.
- `figures/README.md` — archive-candidate note for fig1-11 added.
- `scripts/README.md` — v6 → v8 on pipeline ref; `review_paper_round2.py` path note; reproduction recommendation updated to `gate_review_v8.py`.
- `agents/STUDY_MEMORY.md` — one stale `s114_section4_planning_*.md` reference updated to `_archive/`.
- `docs/reviews/s114_session_summary.md` — five row paths updated to `_archive/`.
- `docs/reviews/s114_paragraph_review.md` — two path references updated.
- `docs/PROVENANCE_INDEX.md` — S115 addendum added covering 8 claim categories in v8 not previously indexed, including open flags for missing scripts and missing persisted files.

**Not applied (flagged for author):**
- Scripts archiving (~45 files).
- Figures archiving (v6-era fig1-11).
- PROVENANCE_INDEX §-number remapping from v6 to v8.
- Renaming `results/_s114_backfills/` files to single-underscore separator.
- The one `.aux` file manual move.
