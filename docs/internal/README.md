# `docs/internal/` — Working review notes not for public consumption

**What's in this folder:** In-progress review checklists, paper dashboards, and fix lists that the author uses while iterating on the paper. These are working notes, not published artifacts.

## Contents

- `_archive/`: Session-specific tracking docs from earlier paper revisions (S110-era review notes, LLM review fixes, paper dashboard, review guide, main-repo update list). Superseded once v11 was release-frozen 2026-04-28; retained for provenance.
- `_archive/ARCHIVE_NOTES_20260428.md`: Catalog of what was archived in the v11 freeze cleanup pass.

Currently no active in-flight tracking files live at the top level of `internal/`. New session-specific tracking docs are added here when an active review pass starts.

## How naming works here

No strict schema. Files are named after their role (review, dashboard, fix list). Session tags like `S110` follow the convention described in `docs/FILE_NAMING.md`.

## Where these files come from / go to

Hand-maintained during paper drafting. They inform edits to the canonical paper draft at `docs/beyond_recall_v11_draft.md`. Once a fix is applied, the corresponding checklist item is struck through or moved to a "done" section. Once a paper revision is release-frozen, the session-specific tracking is moved to `_archive/`.

## Caveats worth knowing

- These files can go stale quickly. When a paper section is locked, its dashboard entry may lag behind.
- Not part of the public story of the paper. If you are evaluating the study externally, the relevant files are in `docs/` directly and in `docs/reviews/`, not here.
