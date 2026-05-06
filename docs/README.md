# `docs/` — Paper drafts, findings, methodology, and review logs

**What's in this folder:** Everything written about the study in prose. The paper itself, the definitive numbers reference, the methodology description, the corrections changelog, and every review round.

## Contents

**The paper and supporting prose:**

- `beyond_recall_v11_draft.md`: **The citable canonical paper** (release-frozen 2026-04-28).
- `beyond_recall_v11_draft.clean.md` + `.docx`: Export-ready variants of the canonical draft.
- `beyond_recall_v10_1_draft.md`: **Preserved historical baseline** (immediate predecessor to v11). Do NOT edit.
- `beyond_recall_v10_1_draft.clean.md` + `.docx`: Frozen exports from v10.1.
- `blog_post_v2.md`: Companion blog post for public launch.

Frozen earlier drafts (v6, v7, v8, v9, v10 partial, pre-v6 arXiv drafts, v2-reframe, Word exports, LaTeX test artifacts) live in `versions/`. v8/v9/v10 drafts are grouped under `versions/_pre_v11_drafts/`. Do not edit those.

**The authoritative references:**

- `DATA_REFERENCE.md`: Single source of truth for every number cited in the paper. 5-judge primary recompute complete (S113). Supermemory native updated to n=14 per paid-tier rerun 2026-04-23.
- `FILE_NAMING.md`: Plain-language guide to how files, subjects, conditions, and judges are named across the repo. Read this first if a filename looks cryptic.
- `METHODOLOGY.md`: Full methodology description (current methods plus historical tables).
- `KEY_FINDINGS.md`: Catalog of major plus minor findings with the evidence file for each.
- `PROVENANCE_INDEX.md`: Traces every paper claim to the source data file that produced it.
- `PAPER_CORRECTIONS.md`: Changelog of numerical and framing corrections across revisions.
- `ANALYSIS_PLAN_LOCK.md`: Pre-committed analysis plan. Committed before final analysis runs so the decisions are auditable.
- `REFERENCE_TABLE.md`: Bibliography of external references cited in the paper.
- `PROVIDER_EXPERIENCE_LEDGER.md` and `PROVIDER_ISSUES.md`: Notes on working with each memory-system API (Mem0, Letta, Zep, Supermemory).

**Subfolders:**

- `internal/`: In-progress review notes not intended for public consumption.
- `research/`: Per-section verification notes, recompute outputs, and experimental sub-studies.
- `reviews/`: Cross-LLM paper-review output from each review round.
  - `reviews/_archive/` contains historical review rounds against superseded drafts (v2/v3/v6 rounds, most S114 session reviews, GTM jargon scans). Retained for provenance; not required reading.
- `versions/`: Frozen prior drafts of the paper and blog post (v6, v7, pre-v6 arXiv drafts, Word exports).
  - `versions/_pre_v11_drafts/` groups v8, v9, v10-partial drafts and the v10.1 docx backup.
  - `versions/_latex_test_artifacts/` holds LaTeX build intermediates from a PDF pipeline test.

## How naming works here

Paper drafts use `beyond_recall_v<N>_draft.md`. Older versions are kept, not deleted, and moved to `versions/`. Reference docs use ALL_CAPS filenames (for example, `DATA_REFERENCE.md`). Naming details for data files are in `FILE_NAMING.md`.

## Caveats worth knowing

- If numbers in any `.md` disagree with `DATA_REFERENCE.md`, the data reference wins. See `FILE_NAMING.md` for the tie-breaking rules.
- `PROVENANCE_INDEX.md` is canonical for v11; cross-check against `beyond_recall_v11_draft.md` directly when in doubt.
