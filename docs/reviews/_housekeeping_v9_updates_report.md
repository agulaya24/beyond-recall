# Housekeeping v9 Updates Report

**Date:** 2026-04-23
**Scope:** Apply three housekeeping updates to study docs reflecting v9 revisions. No v9 or v8 paper file edits.
**Primary source of truth consulted:** `docs/research/supermemory_7judge_aggregate.md` (paid-tier rerun recompute, n=14).

---

## Source verification

Canonical paid-tier aggregate (from `docs/research/supermemory_7judge_aggregate.md`):

- n subjects: 14 (Hamerton + 13 globals)
- Mean Δ_spec (5-judge primary): -0.0125, rounded -0.01
- Mean Δ_spec (7-judge sensitivity): -0.0241, rounded -0.02
- Low-baseline slice (C5 <= 2.0, n=9): Mean Δ_spec = -0.0268, rounded -0.03, 4 of 9 positive
- Paid-tier rerun completed 2026-04-23 covering bernal_diaz, babur, cellini, rousseau
- Ingestion: 199/199 chunks indexed (0 failures) per `docs/research/p0_2_supermemory_paid_tier_rerun.md`

Shift from previous published numbers (v8):
- Native full (5-judge): -0.073 (n=10) -> -0.013 (n=14), delta +0.060
- Native full (7-judge): -0.103 (n=10) -> -0.024 (n=14), delta +0.079
- Direction unchanged (still near-zero negative).

---

## Update 1 — `docs/KEY_FINDINGS.md` line 71

**Before:**
```
**Native config:** Mem0 +0.38, Zep +0.38, Letta −0.01 (archival path — see M5), Supermemory −0.11 (ceiling).
```

**After:**
```
**Native config:** Mem0 +0.38, Zep +0.38, Letta −0.01 (archival path — see M5), Supermemory −0.01 (n=14, paid-tier rerun 2026-04-23; see `docs/research/supermemory_7judge_aggregate.md`).
```

Rationale: -0.11 was the 7-judge sensitivity on n=10 free-tier. Paid-tier rerun brings native SM to n=14 with 5-judge primary aggregate of -0.01. The word "ceiling" was retained conceptually elsewhere in M1/M2/m8; no ceiling-artifact claim lost.

---

## Update 2 — `docs/DATA_REFERENCE.md` line 106 (and line 142)

**Line 106 Before:**
```
| Supermemory (n=10) | −0.11 | [−0.24, +0.04] | Near-zero; 4 subjects failed free-tier ingestion |
```

**Line 106 After:**
```
| Supermemory (n=14) | −0.01 | [see `docs/research/supermemory_7judge_aggregate.md`] | Near-zero. Paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures) across bernal_diaz, babur, cellini, rousseau. Supermemory native aggregate now reflects all 14 main-study subjects. |
```

**Line 142 Before (low-baseline native, same free-tier-incomplete framing):**
```
| Supermemory | −0.06 (n=7) | 2 of 7 |
```

**Line 142 After:**
```
| Supermemory | −0.03 (n=9) | 4 of 9 |
```

Rationale: n=7 was the free-tier low-baseline subset after 4 ingest failures (2 of which were in the low-baseline slice: babur, bernal_diaz). Paid-tier rerun restores the full n=9 low-baseline cohort. Mean Δ = -0.0268 per `supermemory_7judge_aggregate.md`, rounded -0.03. 4 of 9 positive per the same table.

CI for the n=14 aggregate not recomputed here — deferred to the aggregate doc, which is cited inline.

---

## Update 3 — `docs/PROVENANCE_INDEX.md` line 394

**Before:**
```
| Supermemory 4-of-14 ingest failures on free tier (n=10 shown for native SM) | §4.3 line 830 | DATA_REFERENCE §3 footnote (n=10) | VERIFIED |
```

**After:**
```
| Supermemory native SM aggregate n=14 (paid-tier rerun 2026-04-23 indexed all 199 chunks, 0 failures, across bernal_diaz, babur, cellini, rousseau) | §4.3 line 830 | `docs/research/p0_2_supermemory_paid_tier_rerun.md`; `docs/research/supermemory_7judge_aggregate.md`; DATA_REFERENCE §3 footnote (updated to n=14) | VERIFIED (v9 housekeeping 2026-04-23) |
```

Rationale: row rewritten to reflect that the free-tier 4 failures are resolved, the cited sources are the two research docs that carry the canonical numbers, and DATA_REFERENCE §3 footnote has been updated in Update 2 above.

---

## Update 4 — v9 revision paragraph added to `docs/KEY_FINDINGS.md`

Inserted a new H3 section titled `### v9 revision 2026-04-23 (updates)` directly after the "For AI agents working in this repo" paragraph (around line 12) and before the `## S114 update` heading. Contents listed:

- Supermemory native n=10 -> n=14 with Δ_spec shift -0.07 -> -0.01
- Spearman ρ correction 0.89-0.98 -> 0.86-0.93, 7 occurrences
- Haiku-not-Sonnet battery generator (§4.5 correction)
- H8 reframe from "spec teaches ethics" to "conservatism dial" per P0-5 (93% routine refusals)
- §4 structural restructure + Appendix A-E build + Part F safe edits

No v9 or v8 paper file edits performed.

---

## Files modified

- `C:/Users/Aarik/Anthropic/memory-study-repo/docs/KEY_FINDINGS.md` (2 edits: native config line + new v9 revision paragraph)
- `C:/Users/Aarik/Anthropic/memory-study-repo/docs/DATA_REFERENCE.md` (2 edits: native config row + low-baseline native row)
- `C:/Users/Aarik/Anthropic/memory-study-repo/docs/PROVENANCE_INDEX.md` (1 edit: line 394 row)

## Files NOT modified

- `docs/beyond_recall_v9_draft.md` (excluded by constraint)
- v8 paper file (excluded by constraint)

## Constraints honored

- No em-dashes introduced (all existing em-dashes preserved in untouched text only).
- No API calls made.
- All numeric claims verified against `docs/research/supermemory_7judge_aggregate.md`.
