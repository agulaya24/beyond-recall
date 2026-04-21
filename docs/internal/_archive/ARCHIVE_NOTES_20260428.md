# Archive Notes — V11 Freeze Cleanup, 2026-04-28

**Trigger:** v11 paper release-frozen 2026-04-28. `docs/beyond_recall_v11_draft.md` is the citable canonical paper. `docs/beyond_recall_v10_1_draft.md` is preserved as the immediate-predecessor baseline alongside v11 at the top of `docs/`.

**Audit basis:** Independent classification cross-checked against the prior v11 cleanup audit at `docs/reviews/v11_repo_cleanup_candidates_20260427.md`. Conclusions agree.

**Method:** Files moved, not deleted. Cross-references in `docs/README.md`, `docs/internal/README.md`, `docs/versions/README.md` updated to reflect new locations and the v11 / v10.1 canonical pair.

---

## Files moved

### `docs/` → `docs/versions/_pre_v11_drafts/`

Paper drafts that were canonical under earlier versions and should not clutter the top of `docs/` now that v11 is canonical. v8 and v9 were retained as preserved baselines through the v9-and-v10 cycles; v11 supersedes that need.

| File | Why archived |
|---|---|
| `beyond_recall_v8_draft.md` | v8 paper draft; canonical Apr 22; superseded by v9, v10, v10.1, v11 |
| `beyond_recall_v8_draft.clean.md` | v8 export-ready clean variant |
| `beyond_recall_v8_draft.docx` | v8 Word export |
| `beyond_recall_v9_draft.md` | v9 paper draft; canonical Apr 24; superseded |
| `beyond_recall_v9_draft.clean.md` | v9 export-ready clean variant |
| `beyond_recall_v9_draft.docx` | v9 Word export |
| `beyond_recall_v10_draft.clean.md` | v10 partial leftover; v10.1 is the preserved v10-line baseline |
| `beyond_recall_v10_1_draft.docx.bak` | Backup of preserved baseline; v10.1 itself remains at top of `docs/` |

### `docs/internal/` → `docs/internal/_archive/`

Session-specific paper-tracking docs that were active during paper drafting and are now superseded by the v11 freeze.

| File | Why archived |
|---|---|
| `AARIK_REVIEW_S110.md` | Session S110 review pass; comments long since incorporated |
| `LLM_REVIEW_FIXES.md` | Cross-LLM review fixes tracker spanning S110-S113; closed under v9/v10 review cycles |
| `MAIN_REPO_UPDATES_NEEDED.md` | Main BaseLayer repo handoff list from pre-launch; addressed in main repo |
| `PAPER_DASHBOARD.md` | Pre-launch dashboard targeting v6 / Apr 21 launch; superseded by v11 freeze |
| `REVIEW_GUIDE.md` | Structural review guide written for the v6-era draft; section line numbers and structure no longer match v11 |

Note on git mechanics: `docs/internal/*` files were git-tracked, so `git mv` was used for those. `docs/beyond_recall_v8/v9/v10*` files were untracked at the time of move (build artifacts not committed), so plain `mv` was used.

---

## Cross-references updated

These files cited archived content as "current" and would have been wrong after the move. Edited for content, not just paths.

- `docs/README.md` — was calling `beyond_recall_v9_draft.md` "the current active working draft" and v8 the "preserved baseline." Updated to v11 canonical, v10.1 preserved baseline. Also added pointer to `versions/_pre_v11_drafts/` and updated the `PROVENANCE_INDEX.md` caveat (was referencing a v6→v8 section remap).
- `docs/internal/README.md` — was pointing review-pass workflow at `docs/beyond_recall_v8_draft.md`. Updated to v11. Documented the `_archive/` subdir.
- `docs/versions/README.md` — was telling readers "the current draft is `docs/beyond_recall_v8_draft.md`." Updated to v11. Added entry for `_pre_v11_drafts/` subfolder.

Top-level navigation files (`README.md`, `AGENTS.md`, `agents/STUDY_MEMORY.md`, `agents/study-guide.md`) were already in modified state from the v11 freeze pass and reference the v8/v9 drafts only as "preserved baselines" — paths that still resolve under `docs/versions/_pre_v11_drafts/`. **Not updated in this pass** because they're already part of an in-flight v11 freeze edit; updating them now would interleave with that work. Flagged for Aarik below.

---

## Files reviewed and KEPT in place

| File | Why kept |
|---|---|
| `docs/README.md` | Navigation README; updated for v11 |
| `docs/DATA_REFERENCE.md` | Just updated to v11 canonical numbers |
| `docs/PROVENANCE_INDEX.md` | Just updated for v11 |
| `docs/KEY_FINDINGS.md` | Just updated for v11 |
| `docs/METHODOLOGY.md` | Version-spanning methodology description with current methods |
| `docs/FILE_NAMING.md` | Convention doc; version-agnostic |
| `docs/PROVIDER_EXPERIENCE_LEDGER.md`, `PROVIDER_ISSUES.md` | Memory-system API research notes; version-agnostic |
| `docs/blog_post_v2.md` | Companion blog post; separate from paper version |
| `docs/_pandoc_default_reference.docx`, `_reference_arxiv_11pt.docx` | Pandoc style reference templates; tooling, not paper text |
| `docs/ANALYSIS_PLAN_LOCK.md` | Pre-registered analysis plan. Pre-commitments don't get archived after execution; that defeats the audit purpose. KEEP indefinitely. |
| `docs/PAPER_CORRECTIONS.md` | Cross-revision changelog; cited as live reference in `PROVENANCE_INDEX.md`, `docs/README.md`, `agents/study-guide.md`. Functionally a historical record but indexed as a live navigation target — moving it would break those links. KEEP. |
| `docs/_results_snapshot.txt` | Plain-text snapshot of v10/v11-era headline numbers (Wilcoxon p=0.007 matches paper). Underscore prefix suggests scratch but content is current. Cleanup audit didn't flag it. KEEP. |
| `docs/internal/README.md` | Navigation README; updated for v11 |
| `docs/versions/README.md` | Navigation README; updated for v11 |

---

## Files flagged AMBIGUOUS for Aarik's decision

### `docs/REFERENCE_TABLE.md`

- **Last audited:** 2026-04-18 (S113) against `beyond_recall_v6_draft.md`.
- **Status:** Bibliography of external references with REF-XX keys. Not session-specific; not a paper draft. But the v11 paper has its own §9 References built in, so the standalone table may be redundant.
- **Question for Aarik:** Is `REFERENCE_TABLE.md` still load-bearing as a parallel bibliography, or has it been folded into v11 §9 entirely? If folded, archive as HISTORICAL to `docs/versions/_pre_v11_drafts/`. If still serving as the working bibliography (REF-XX key system), update its "Last audited" header against v11 and keep.
- **Default action taken:** Left in place to avoid breaking unverified citations.

### Top-level navigation files with stale v8/v9 baseline references

The following four files reference v8 and v9 drafts as "preserved baselines" at their old paths (`docs/beyond_recall_v8_draft.md`, `docs/beyond_recall_v9_draft.md`):

- `README.md` — top-level
- `AGENTS.md` — top-level
- `agents/STUDY_MEMORY.md`
- `agents/study-guide.md`

These paths now resolve to `docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.md` etc. All four are already in `git status` modified state from the in-flight v11 freeze edit pass. Updating them in this archival pass risks interleaving with that work.

- **Question for Aarik:** Should I update these path references in a follow-up pass, or fold them into the active v11 freeze edit?
- **Default action taken:** Not modified in this pass. Path references will appear stale until updated.

---

## Verification

`ls docs/` after archival should show only:

- Navigation: `README.md`
- Reference docs: `DATA_REFERENCE.md`, `KEY_FINDINGS.md`, `PROVENANCE_INDEX.md`, `METHODOLOGY.md`, `FILE_NAMING.md`, `PAPER_CORRECTIONS.md`, `REFERENCE_TABLE.md`, `ANALYSIS_PLAN_LOCK.md`
- Provider notes: `PROVIDER_EXPERIENCE_LEDGER.md`, `PROVIDER_ISSUES.md`
- Canonical paper: `beyond_recall_v11_draft.md`, `.clean.md`, `.docx`
- Preserved baseline: `beyond_recall_v10_1_draft.md`, `.clean.md`, `.docx`
- Companion: `blog_post_v2.md`
- Tooling: `_pandoc_default_reference.docx`, `_reference_arxiv_11pt.docx`, `_results_snapshot.txt`
- Subdirs: `internal/`, `research/`, `reviews/`, `versions/`

`ls docs/internal/` should show only `README.md` and `_archive/`.

`ls docs/versions/_pre_v11_drafts/` should show 8 files (v8/v9 each x3 + v10 partial + v10.1 backup).

---

# Supplementary Pass — 2026-04-28 (later same day)

**Trigger:** Second sweep targeting the nine `docs/` files with mtime ≤ 2026-04-22 to classify them against the v11 freeze. The prior pass (above) had explicit KEEP decisions on most of these; this sweep applies header refreshes where they were retained and reverses two KEEP decisions where verification against the v11 paper showed the content is genuinely superseded.

## Files moved in this pass

| From | To | Reason | Override of prior pass? |
|---|---|---|---|
| `docs/_results_snapshot.txt` | `docs/internal/_archive/_results_snapshot.txt` | Numbers are S113-era 7-judge aggregate; verified against `beyond_recall_v11_draft.md` Table values for Sunity Devee (snapshot C2a = 2.47 vs v11 5-judge primary 2.27, C4a = 2.60 vs v11 2.41). The Wilcoxon and Krippendorff α numbers do match v11, but the per-subject means do not, so the file is not a current snapshot. | YES — prior pass said "KEEP, content current" based on the Wilcoxon match alone. Per-subject scores were not cross-checked then. |
| `docs/REFERENCE_TABLE.md` | `docs/versions/_pre_v11_drafts/REFERENCE_TABLE.md` | Audited against `beyond_recall_v6_draft.md` per its own header, never re-audited. v11 §9 References (lines 1789-1823) is the canonical bibliography. | NO — prior pass left this AMBIGUOUS for Aarik's decision. This sweep resolves it: archive. |

`git mv` used for both (tracked files).

## Files refreshed with header annotation, kept in place

Each got 1-3 lines added or modified at the top of the file. Body unchanged.

| File | Header note added |
|---|---|
| `docs/PROVIDER_EXPERIENCE_LEDGER.md` | "Last reviewed: 2026-04-28 (v11 freeze; content unchanged, version-agnostic provider research log)." |
| `docs/PROVIDER_ISSUES.md` | "Last reviewed: 2026-04-28 (v11 freeze; content unchanged, version-agnostic provider issues log)." |
| `docs/ANALYSIS_PLAN_LOCK.md` | "Carried forward unchanged: 2026-04-28 (v11 freeze). The locked plan below applied to S113 runs and was carried into v10, v10.1, and v11 without modification. Pre-commitments are retained as-is for audit; do not edit the plan body retroactively." |
| `docs/METHODOLOGY.md` | "Last reviewed: 2026-04-28 (v11 freeze). Methodology described here was carried forward into v11 with additions (per-question variance, anchor-crossing analysis, half-anchor calibration). For v11-current numbers and the canonical methods narrative consult `beyond_recall_v11_draft.md` §3 and §4 plus `DATA_REFERENCE.md`. The body of this file is preserved as the version-spanning methods reference." |
| `docs/PAPER_CORRECTIONS.md` | "Last reviewed: 2026-04-28 (v11 freeze). All corrections logged below were incorporated into v9, v10, v10.1, and v11. This file is retained as a cross-revision audit trail and is referenced from `PROVENANCE_INDEX.md`, `docs/README.md`, and `agents/study-guide.md`. New v11-era corrections are not appended here; see `DATA_REFERENCE.md` and `beyond_recall_v11_draft.md` for current values." |
| `docs/FILE_NAMING.md` | "Last reviewed: 2026-04-28 (v11 freeze). Naming conventions, subject list, condition list, and judge panel are unchanged from v11. The 'Where to look' table near the bottom still references the v8 draft and the S113 / S114 aggregate filenames; the v11-canonical paper is `docs/beyond_recall_v11_draft.md` and the v10.1 preserved baseline sits next to it. v8 / v9 / v10 drafts moved to `docs/versions/_pre_v11_drafts/` in the v11 cleanup." |
| `docs/blog_post_v2.md` | "Last reviewed: 2026-04-28 (v11 freeze). Companion blog post; framing aligns with v11. Some headline tables below use the S113-era 7-judge aggregate (Hamerton C5 = 1.25, C2a = 3.04, C4a = 3.22, raw corpus = 2.32); v11 reports 5-judge primary as canonical. Headline framing (9 of 9 low-baseline positive, 12 of 14 overall, Wilcoxon p < 0.01) is consistent across both panels. Refresh against v11 5-judge primary numbers before publishing." |

## Verification

After this supplementary pass, `docs/` top-level mtime-stale files are:

- Refreshed in place: `ANALYSIS_PLAN_LOCK.md`, `METHODOLOGY.md`, `PAPER_CORRECTIONS.md`, `FILE_NAMING.md`, `PROVIDER_EXPERIENCE_LEDGER.md`, `PROVIDER_ISSUES.md`, `blog_post_v2.md`
- Moved out: `_results_snapshot.txt`, `REFERENCE_TABLE.md`

`docs/internal/_archive/` now contains: `_results_snapshot.txt`, `AARIK_REVIEW_S110.md`, `ARCHIVE_NOTES_20260428.md`, `LLM_REVIEW_FIXES.md`, `MAIN_REPO_UPDATES_NEEDED.md`, `PAPER_DASHBOARD.md`, `REVIEW_GUIDE.md`.

`docs/versions/_pre_v11_drafts/` adds `REFERENCE_TABLE.md` to the existing 8 paper-draft files.

## Files flagged AMBIGUOUS, NONE this pass

The two prior-pass ambiguous flags (`REFERENCE_TABLE.md` and the four top-level navigation files with stale v8/v9 baseline references) are addressed: REFERENCE_TABLE.md archived; the navigation files remain flagged for the in-flight v11 freeze edit pass to handle (per the prior pass's note).
