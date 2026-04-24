# V10 Numerical Drift Reconciliation Report

**Date:** 2026-04-25
**Source of truth:** `docs/beyond_recall_v10_draft.md` (v10, release-frozen 2026-04-24).
**Trigger:** Voice/alignment review (`docs/reviews/v10_voice_alignment_review_20260425.md`) and prior GPT-5.5 repo review (`docs/reviews/v10_repo_review_gpt55_20260424.md`) flagged stale numbers in public-facing repo docs after the v10 release-freeze pass.

## Method

Each in-scope repo file was swept for numerical claims (slopes, CIs, R², p-values, percentages, mean Δ, sample sizes, deltas, per-subject scores). Every value was cross-checked against the v10 paper's 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4); 7-judge values are now sensitivity only. Where docs disagreed with v10, the docs were corrected; v10 was not modified. Where ambiguous percent uplift was used against an unspecified baseline, it was replaced with absolute Δ values per task constraint.

## Per-file diff summary

### `README.md` — 5 substantive blocks corrected

1. **Key Finding #2 (memory-system spec deltas)** — replaced 7-judge values (Mem0 +0.13, Letta +0.23, Zep +0.20, Supermemory +0.004, Base Layer +0.13; aggregate −0.04 / −0.11) with v10 §4.4 5-judge primary (Mem0 +0.10, Letta archival +0.17, Zep +0.17, Supermemory −0.01, Base Layer +0.08 on low-baseline; aggregate −0.05 controlled / −0.01 native paid-tier). Reframed Supermemory from "ceiling artifact" to "bimodal mixture" matching v10 §4.4 mechanism (37 helps at +1.45, 52 hurts at −1.41).
2. **Key Finding #3 (Hamerton compression)** — replaced 7-judge C2a 3.04 / C8 2.32 / C9 3.22 with v10 §4.2 5-judge primary 2.63 / 2.27 / 3.09. Removed "matches" framing for C9 (5-judge primary shows C9 3.09 > C4a 2.77, not equal).
3. **Repository Structure dir comment** — Hamerton baseline 1.25 → 1.26 (5-judge primary qualifier added).
4. **Subjects table (14 rows)** — replaced all 14 7-judge baselines with v10 §4.1 5-judge primary values. Re-sorted by ascending C5; cutoff line moved (the 5-judge ordering differs from the 7-judge ordering at several positions; e.g., Bernal Diaz now sits at 1.70 rather than 1.85). Added panel-disclosure note above the table.
5. **Hamerton dir-listing comment** — "low baseline, 1.25" → "low baseline, 1.26 on 5-judge primary".

Total numerical edits to README.md: ~25.

### `docs/KEY_FINDINGS.md` — 5 sections rewritten

1. **M2 (memory systems)** — full rewrite. Replaced 7-judge values with v10 §4.4 5-judge primary on both controlled and native, all-14 and low-baseline. Added per-system Wilcoxon p-values from v10 §4.4 line 1056 / 1070. Reframed heading from "improves all 4" to "improves three of four" reflecting v10 §4.4 (Supermemory bimodal). Retained 7-judge sensitivity values labeled as such. Updated flagship sentence with the bimodal-mixture caveat.
2. **M3 (wrong-spec)** — replaced ambiguous absolute means (C5 = 2.02, C2a = 2.55, v1 = 1.86, v2 = 2.30) with v10 §4.3 5-judge primary 13-globals Δ vs C5 (C2a +0.35, v2 +0.22, v1 −0.25) per task constraint to disambiguate baselines or replace with absolute Δ. Added 7-judge sensitivity row.
3. **M5 (Letta stateful-agent)** — replaced 7-judge values (Hamerton 3.24 / Ebers 3.00 / Babur 2.73 vs BL C2a/C4a) and the +1.99/+1.96/+0.75 "uplift" framing (which was uplift vs C5 baseline, conflicting with v10 §4.5's BL-comparison framing) with v10 §4.5 5-judge primary table: Letta block → Haiku vs BL unified brief → Haiku, 3.10/2.76/2.42 vs 2.96/1.72/1.88, Δ +0.14/+1.05/+0.54. Added n=3 exploratory framing. Added full-stack BL rerun footnote (Δ +0.27/+1.21/+0.38). Added 7-judge sensitivity row.
4. **m7 (Letta archival)** — updated Letta archival path values from 7-judge (−0.01 native, +0.25 controlled) to 5-judge primary (−0.02 native, +0.20 controlled). Replaced "scores substantially higher (3.24-3.38 on Hamerton, 3.00 on Ebers vs 2.81-2.86 archival)" with v10 §4.5 5-judge primary deltas.
5. **MEMORY-SYSTEM CHARACTER (per-provider summary)** — full rewrite of all six provider sub-sections (Mem0, Letta archival, Letta stateful, Zep, Supermemory, Base Layer) with v10 5-judge primary values throughout. Added Wilcoxon p-values for Zep and Letta. Added panel-disclosure header.
6. **SUMMARY TABLE** — updated M2 row from "all 4" to "three of four"; M5 row "(n=2)" to "(n=3, exploratory)"; m8 / M8 GTM "beats raw corpus" to "exceeds raw corpus".

Total numerical edits to KEY_FINDINGS.md: ~45.

### `docs/PROVENANCE_INDEX.md` — V10 update prepended; historical addenda preserved

1. **Header** — added v10 canonical pointer; added V10 to legend.
2. **V10 Update section (new, prepended)** — added 7 canonical tables: per-subject gradient (5-judge primary, all 14 subjects + Franklin), statistical tests, memory-system spec deltas (4 cells), wrong-spec controls (3 conditions), Letta stateful-agent (n=3), Hamerton compression curve (6 conditions). Each table cites the v10 paper line number and the raw judgment-file path. Added "Status of pre-V10 sections below" note explicitly flagging Hamerton 1.41/1.37 → 1.26, Franklin 3.99/4.10 → 3.77, Letta uplift +1.99/+1.96/+0.75 (vs C5) → +0.14/+1.05/+0.54 (vs BL unified brief), Spearman 0.89-0.98 → 0.86-0.93, Krippendorff α 0.723 → 0.659/0.535.
3. **Historical S105 / S113 / S115 addenda** — left intact per the strategy decision (advisor recommendation): rewriting line-by-line risks introducing errors and misframes the historical raw-data traces, which remain accurate as raw provenance even when the canonical paper claims have moved. The new V10 Update section explicitly flags every conflict and tells readers V10 / DATA_REFERENCE wins in every case.

Total numerical edits to PROVENANCE_INDEX.md: ~5 row updates in header; ~50 new canonical rows added.

### `agents/STUDY_MEMORY.md` — added 5-judge primary canonical rows

1. **KEY NUMBERS — 5-judge primary canonical** — appended new sub-sections for §4.3 wrong-spec (3 Δ values), §4.4 memory-system spec deltas (4 system × 4 cell rows + per-system Wilcoxon p-values), §4.5 Letta stateful-agent (n=3 with full-stack rerun footnote). Did not duplicate already-correct §4.1 / §4.2 / §4.2.1 / §3.7.6 / §4.3 spec-activation sections.
2. **KEY NUMBERS — LEGACY (7-judge sensitivity)** — header reframed to indicate v10 promoted 5-judge to canonical; legacy values retained as accurate sensitivity-panel traces.
3. **Pending 5-judge primary numbers** subsection — replaced with "5-judge primary canonical (v10 release-frozen, 2026-04-24)" closure note. Task #31 marked closed.

Total numerical edits to STUDY_MEMORY.md: ~30 new canonical values added; 1 status-block rewrite.

### `agents/study-guide.md` — 3 sections corrected

1. **L43 population-of-interest framing** — "n≈8-9 on 5-judge primary pending recompute" → "all 9 of 9 improve under facts+spec" (v10 §4.1 confirms 9 of 9 on the low-baseline slice).
2. **Letta Stateful-Agent Test section (§4.3.1 / §4.7)** — heading corrected to v10 §4.5; pipeline location updated to `docs/research/_letta_rerun/`; values updated from 7-judge (Hamerton 3.24 / 3.04 / Δ +0.20; Ebers 3.00 / 2.25 / Δ +0.75; Babur 2.73 / 2.44 / Δ +0.29) to v10 5-judge primary (3.10 / 2.96 / +0.14; 2.76 / 1.72 / +1.05; 2.42 / 1.88 / +0.54). Full-stack BL rerun footnote added.
3. **Key Claims and Where to Verify Them table (10 rows)** — every row's "primary vs sensitivity" column updated from S114 placeholders to v10 5-judge primary values: gradient slope row replaced (was "−0.98 on 7-judge / −0.89 on 5-judge ... Hamerton pending backfill inclusion"; now "−0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001"). Memory-system row replaced. Letta row replaced. Wrong-spec row replaced. Compression row replaced.

Total numerical edits to study-guide.md: ~15.

### `ISSUES.md`, `REPRODUCE.md`, `requirements.txt` — no changes required

ISSUES.md is already release-frozen with the v10 status block; the historical resolved-items log is accurate as a session-by-session changelog. REPRODUCE.md was authored in the v10 release-freeze pass and reports the canonical 5-judge primary headline numbers. requirements.txt has no numbers.

## Total count of numerical fixes applied

Approximately **120 numerical changes** across 5 files:

- README.md: ~25
- KEY_FINDINGS.md: ~45
- PROVENANCE_INDEX.md: ~50 new rows + 5 header updates
- STUDY_MEMORY.md: ~30 new canonical values + 1 status rewrite
- study-guide.md: ~15

Three files unchanged: ISSUES.md, REPRODUCE.md, requirements.txt.

## Mismatches not reconciled

None blocking. One soft note for the author:

- **DATA_REFERENCE.md §3 (memory-system aggregates) is labeled as "computed on the 7-judge mixed panel as committed in S113 ... 5-judge primary recompute is at `docs/research/memory_systems_5judge_primary.md`; aggregate directions and ranks match the 7-judge values, magnitudes are within ~0.05 points."** v10 §4.4 line 1048 reports the 5-judge primary directly. The DATA_REFERENCE.md framing is technically accurate as a description of the data-state, but downstream readers (KEY_FINDINGS, README, study-guide) now report 5-judge primary memory-system values. Recommend updating DATA_REFERENCE.md §3 in a future pass to promote the 5-judge primary table inline rather than referencing it as a separate recompute. Not a blocker because the v10 paper, KEY_FINDINGS M2, and README all now agree on the 5-judge primary memory-system numbers; DATA_REFERENCE.md's continued 7-judge framing is the lone outlier and is internally honest about what it's reporting.

## Source of canonical values used

Every fix anchors to one or more of:

- v10 paper §4.1 (per-subject gradient, line 720)
- v10 paper §4.1 (sensitivity + coupling, lines 747-759)
- v10 paper §4.2 (compression, lines 791 + 777)
- v10 paper §4.3 (wrong-spec, line 901)
- v10 paper §4.4 (memory-system composition, line 1048 + 1056 + 1070 + Supermemory section line 1096)
- v10 paper §4.5 (Letta stateful-agent, line 2426)
- v10 paper §4.6.2 (judge-panel sensitivity, line 1330)
- v10 paper Appendix D.1 (per-subject 5-judge primary, line 2057)

The v10 paper draft was not modified.
