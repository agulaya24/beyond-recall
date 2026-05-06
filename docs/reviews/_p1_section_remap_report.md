# P1 Section-Number Remap Report

**Date:** 2026-04-23
**Scope:** `docs/DATA_REFERENCE.md` and `docs/KEY_FINDINGS.md`
**Goal:** Resync stale paper-location section numbers to v9 structure.

## Context

The v9 paper restructure moved several sections. DATA_REFERENCE and KEY_FINDINGS
retained pre-v9 numbering (a mix of v6, v7, and v8 anchors). This report records
the mechanical remap applied under the "treat as v9-anchored" instruction.

## v9 structure (for reference)

| v9 ref | Section title |
|---|---|
| §4.1 | The Cross-Subject Gradient |
| §4.1.1 | Franklin as the high-baseline reference |
| §4.1.2 | Living-user replication (author) |
| §4.2 | Compression: Structure vs. Raw Text |
| §4.2.1 | Question-Improvement Rate |
| §4.3 | Mechanism: Content, Not Format (wrong-spec lives here in v9) |
| §4.4 | Memory-System Composition |
| §4.4.1 | Aggregate Performance Across Systems |
| §4.4.2 | Common Mechanisms: Interpretation, Over-theorization, Principled Refusal |
| §4.4.3 | Case Study: Cross-System Refusal on Keckley Q21 |
| §4.5 | Architectural Convergence: Letta Stateful-Agent |
| §4.6 | Robustness and Sensitivity |
| §4.6.1 | Cross-provider response generation (Tier 2 replication) |
| §4.6.2 | Judge panel sensitivity |
| §5.5 | Practical Implications |
| §5.7 | Behavioral Alignment and Safety Alignment |
| §7 | Future Work |

## Mapping rules applied

- old §4.3.1 (Letta stateful) → §4.5
- old §4.5 (Robustness) → §4.6 (but wrong-spec content → §4.3, by context)
- old §4.6 (Interpretation vs Recall) → §4.4.2 (Pattern 1/2/3) or §4.4.3 (Keckley Q21 case)
- old §4.7 (Letta) → §4.5
- old §4.8 (Tier 2 / Scaling) → §4.6.1 (Tier 2) or §5.5 (practical scaling)
- old §4.1.2 (Gemini sensitivity) → §4.6.2
- old §4.3 (Memory systems aggregate) → §4.4
- old §4.3.2 (provider character sketch) → §4.4 (or §4.4.1 for aggregate-specific)
- old §4.1.3 (failure-mode analysis) → §4.1 (content folded into main §4.1 narrative)
- old §8 (Future Work) → §7

## DATA_REFERENCE.md (line-by-line)

| Line | Before | After | Notes |
|---|---|---|---|
| 5 (header note) | "still reference `beyond_recall_v6_draft.md` ... have not yet been mechanically re-synced" | "v9-anchored as of 2026-04-23 (see `_p1_section_remap_report.md`). Table numbers not renumbered." | Doc header updated to reflect resync state. |
| 13 | "(see note above about v6 vs v8)" | "(v9-anchored as of 2026-04-23)" | Reading-guide bullet. |
| 80 | "§4.1, with full Gemini sensitivity in §4.1.2" | "§4.1, with full Gemini sensitivity in §4.6.2" | v9 §4.6.2 is judge-panel sensitivity; v9 §4.1.2 is now living-user replication. |
| 104 | "see §7 for stateful-agent test" | unchanged | Internal DATA_REFERENCE §7 ref (this doc's Letta section). Audit-flagged but verified correct. |
| 111 | "see §7" | unchanged | Same internal ref. Audit-flagged but verified correct. |
| 114 | "Table 4.3 in §4.3" | "Table 4.3 in §4.4" | Memory-systems aggregate lives in v9 §4.4 Memory-System Composition. |
| 149 | "Table 4.3 low-baseline rows, §4.3 key findings" | "Table 4.3 low-baseline rows, §4.4 key findings" | Same. |
| 176 | "§4.3 Supermemory paragraph" | "§4.4 Supermemory paragraph" | Provider character sketches in v9 §4.4. |
| 197 | "Table 4.5 in §4.5" | "Table 4.5 in §4.3" | Wrong-spec mechanism content in v9 §4.3 "Mechanism: Content, Not Format". Audit-flagged. |
| 224 | "§4.3.1" | "§4.5" | Letta stateful-agent section. Under v9, single-subject Letta stateful test sits in §4.5 Architectural Convergence. |
| 271 | "§4.1.2 sensitivity analysis" | "§4.6.2 sensitivity analysis" | Judge panel sensitivity now §4.6.2. |
| 275 | "§3.7 judge calibration, §4.1.2 sensitivity analysis" | "§3.7 judge calibration, §4.6.2 sensitivity analysis" | Same. |
| 295 | "§4.1.3 failure-mode analysis" | "§4.1 failure-mode discussion; see also §4.6) [CHECK]" | v9 has no §4.1.3 subsection; failure-mode content is folded into §4.1 narrative and §4.6 robustness checks. Flagged [CHECK]. |
| 298 | "§4.8" | "§4.6.1" | Tier 2 cross-provider replication is §4.6.1 in v9. Audit-flagged. Note: user mapping rule says "§4.8 old Scaling → §5.5", but the content at line 298 is Tier 2 circularity which is cross-provider replication, v9 §4.6.1. Content override applied. |
| 305 | "extend §4.3.1 from n=1 to n=2" | "extend §4.5 from n=1 to n=2" | Letta stateful in v9 = §4.5. |
| 307 | "comparison to §7 when complete" | unchanged | Internal DATA_REFERENCE §7 ref. Audit-flagged but verified correct. |
| 309 | "Planned addition to §4.3.1 or §7 pending result" | "Planned addition to §4.5 (paper) or §7 (this doc's Letta stateful-agent section) pending result" | Disambiguated: §4.3.1 paper ref → §4.5 (v9 Letta stateful); §7 clarified as internal ref to DATA_REFERENCE own Letta section. Audit-flagged. |
| 337 | "§4.4" | unchanged | v9 §4.4 Memory-System Composition includes BL retrieval floor discussion. Correct in v9. |

**Internal DATA_REFERENCE refs left unchanged (these point to sections of this doc, not paper):** lines 23 (§9), 78 (§9), 96 (§4), 104 (§7), 111 (§7), 112 (§4), 307 (§7).

## KEY_FINDINGS.md (line-by-line)

| Line | Before | After | Notes |
|---|---|---|---|
| 19 | "§4.5 wrong-spec battery generator corrected" | "§4.3 wrong-spec battery generator corrected" | Wrong-spec in v9 = §4.3. |
| 85 (M2) | "§4.3, Table 4.3" | "§4.4, Table 4.3" | M2 is memory systems aggregate → v9 §4.4. Table number preserved. |
| 99 (M3) | "§4.5, Table 4.5" | "§4.3, Table 4.5" | M3 is wrong-spec controls → v9 §4.3. Table number preserved. |
| 117 (M4) | "§4.3 finding #5" | "§4.4 finding #5" | M4 is memory-system disagreement → v9 §4.4. |
| 142 (M5) | "§4.3.1" | "§4.5" | M5 is Letta stateful → v9 §4.5. Audit-flagged. |
| 158 (M6) | "§4.3.1" | "§4.5" | M6 is Letta scaling → v9 §4.5. Audit-flagged. |
| 176 (M7) | "§4.3.1" | "§4.5" | M7 is Letta duplication → v9 §4.5. Audit-flagged. |
| 210 (table note) | "consistent with §4.1.3" | "consistent with §4.1 failure-mode discussion [CHECK: v9 has no §4.1.3 subsection]" | v9 has no §4.1.3; folded into §4.1. |
| 214 (M9) | "§4.8, §4.8.1" | "§4.6.1" | M9 is cross-provider Tier 2 → v9 §4.6.1. Audit-flagged. Mechanical §4.8→§5.5 rule does not apply because content is Tier 2, not Scaling. |
| 224 (m1) | "§4.6" | "§4.4.2 [CHECK]" | m1 is Hamerton Q21 qualitative case (hedging → committed prediction). Fits §4.4.2 Common Mechanisms, not the §4.4.3 Keckley Q21 case study. Flagged [CHECK] because the user mapping rule says §4.6 → §4.4.2 OR §4.4.3 by context. Audit-flagged. |
| 230 (m2) | "§4.7" | "§4.1.1 [CHECK]" | m2 is Franklin baseline (high-baseline reference). In v9 that is §4.1.1. Mechanical §4.7→§4.5 rule does not apply because the line was stale-Franklin pointing at an incorrect old section, not stale-Letta. Content override applied; flagged [CHECK]. Audit-flagged. |
| 246 (m4) | "§4.1.2" | "§4.6.2" | m4 is Gemini inflation → v9 §4.6.2 judge sensitivity. |
| 258 (m6) | "§3.7, §4.1.2" | "§3.7, §4.6.2" | m6 is inter-judge agreement → v9 §4.6.2. |
| 262 (m7 body) | "configuration we initially tested in §4.3 ... stateful-agent path (§4.3.1, M5)" | "configuration we initially tested in §4.4 ... stateful-agent path (§4.5, M5)" | m7 body text carrying same two stale refs. |
| 264 (m7 paper ref) | "§4.3 scope caveat, §4.3.1" | "§4.4 scope caveat, §4.5" | m7 is Letta archival vs stateful → memory systems scope §4.4 + Letta stateful §4.5. |
| 270 (m8) | "§4.3 finding #2, §5.7" | "§4.4 finding #2, §5.7" | m8 is Supermemory ceiling in memory systems → v9 §4.4. §5.7 preserved. |
| 284 (m9) | "§4.3.1" | "§4.5" | m9 is Letta block scaling → v9 §4.5. Audit-flagged. |
| 296 (m11) | "§4.4" | unchanged | m11 is BL retrieval comparable. v9 §4.4 Memory-System Composition includes BL discussion. Correct in v9. |
| 302 (m12) | "§4.5" | "§4.3" | m12 is wrong-spec v1 vs v2 → v9 §4.3. Audit-flagged. |
| 308 (m13) | "§4.5" | "§4.3" | m13 is wrong-spec incongruence detection → v9 §4.3. Audit-flagged. |
| 312 (m14 text) | "§4.1.3 explores hypotheses" | "§4.1 (and §4.6 robustness) explores hypotheses [CHECK]" | v9 has no §4.1.3; flagged. |
| 314 (m14 paper ref) | "§4.1.3" | "§4.1 [CHECK]" | Same. |
| 337 (m17) | "§1.3 ... + §4.3 detail" | "§1.3 ... + §4.4.2 detail [CHECK]" | m17 is three system-general failure modes. v9 §4.4.2 "Common Mechanisms: Interpretation, Over-theorization, Principled Refusal" maps to two of three; default-axiom overfires sits in the same section. Flagged [CHECK]. |
| 343 (m18) | "§4.3.2 Letta character sketch" | "§4.4 Letta character sketch [CHECK]" | v9 has no §4.3.2; provider character sketches live in §4.4. Flagged [CHECK]. |
| 349 (m19) | "§4.4 mechanism claim" | unchanged | m19 is BL hedging hypothesis in §4.4. v9 §4.4 includes BL discussion. Correct in v9. |
| 355 (m20) | "§1.3 Mechanism + §4.5 expansion" | "§1.3 Mechanism + §4.3 expansion" | m20 is wrong-spec detection → v9 §4.3. Audit-flagged. |
| 409 (F8 text) | "§4.3.2 framing implies Zep" | "§4.4 framing [CHECK]" | No §4.3.2 in v9. |
| 417 (F10) | "§4.3.1 architectural-convergence" | "§4.5 architectural-convergence" | Letta stateful in v9 = §4.5. |
| 453 (Zep character) | "§4.3.2 framing" | "§4.4 framing [CHECK]" | No §4.3.2 in v9. |
| 465 (BL hedging) | "§4.4's prompt-template" | unchanged | v9 §4.4 includes BL; correct. |
| 475 (M2 summary) | "§4.3" | "§4.4" | Memory systems. |
| 476 (M3 summary) | "§4.5" | "§4.3" | Wrong-spec. |
| 477 (M4 summary) | "§4.3" | "§4.4" | Memory systems. Audit-flagged. |
| 478 (M5 summary) | "§4.3.1" | "§4.5" | Letta stateful. |
| 479 (M6 summary) | "§4.3.1" | "§4.5" | Letta stateful. |
| 480 (M7 summary) | "§4.3.1" | "§4.5" | Letta stateful. |
| 482 (M9 summary) | "§4.8" | "§4.6.1" | Cross-provider Tier 2. Audit-flagged. |
| 484 (F1-F7 summary) | "§7" | unchanged | v9 §7 is Future Work. Ref is already v9-correct. Audit-flagged but verified correct (recorded here for reviewer). |
| 515-519 (F8-F12) | "§8 Future Work" | "§7 Future Work" | Old §8 = Future Work. In v9 Future Work is §7. Applied to all five F-entries. |

## [CHECK] items summary

The following refs were remapped with context-based judgment rather than a
clean one-to-one rule. Flagged inline in both files so a reviewer can confirm
or adjust.

1. **DATA_REFERENCE line 295 and KEY_FINDINGS lines 210, 312, 314:**
   old §4.1.3 failure-mode analysis mapped to §4.1 (and §4.6 for robustness).
   v9 has no §4.1.3 subsection; failure-mode content is folded into §4.1
   narrative (Zitkala-Sa / Equiano paragraph around line 309 of v9) and the
   robustness discussion in §4.6.
2. **KEY_FINDINGS line 224 (m1 Hamerton Q21):** old §4.6 mapped to §4.4.2.
   Mapping rule allows §4.4.2 or §4.4.3 by context. Hamerton Q21 is not the
   Keckley Q21 case study in §4.4.3; the "hedging to committed prediction"
   framing matches the Interpretation pattern in §4.4.2 Common Mechanisms.
3. **KEY_FINDINGS line 230 (m2 Franklin):** old §4.7 mapped to §4.1.1, not
   §4.5. The mechanical rule says §4.7 → §4.5 (Letta), but the content at
   line 230 is Franklin high-baseline, not Letta. The original §4.7 ref was
   already content-wrong before v9; content override applied.
4. **KEY_FINDINGS line 337 (m17 three failure modes):** old §4.3 detail
   mapped to §4.4.2. Content is "three failure modes of specification-based
   reasoning across systems"; v9 §4.4.2 maps two of three (over-theorization,
   principled refusal) and the third (default-axiom overfires) is in the
   same vicinity. Flagged so reviewer can confirm §4.4.2 fits all three.
5. **KEY_FINDINGS lines 343, 409, 453 (§4.3.2):** old §4.3.2 mapped to §4.4.
   v9 has no §4.3.2 subsection; provider character sketches live inside §4.4
   Memory-System Composition. Could alternatively map to §4.4.1 for aggregate-
   specific numbers; §4.4 chosen as the safer less-specific anchor.

## No-change records (audit-flagged but verified correct under v9)

- **DATA_REFERENCE line 104:** `(see §7 for stateful-agent test)` is an
  internal ref to DATA_REFERENCE's own §7 Letta stateful-agent test section.
  Not a paper ref. Unchanged.
- **DATA_REFERENCE line 111:** Same internal §7 ref. Unchanged.
- **DATA_REFERENCE line 307:** "comparison to §7 when complete" is the same
  internal ref. Unchanged.
- **KEY_FINDINGS line 484:** `F1-F7 | Open | Future work | §7`. In v9
  Future Work is §7, so this is already correct.

## Out-of-scope items (not touched)

- v9 and v8 paper drafts themselves: not modified per user constraint.
- Table numbers: preserved as-is; only section anchors were remapped.
- Refs in the v7-locked / v8-anchored tracking notes (lines 240, 367, 373 of
  KEY_FINDINGS): left alone because they explicitly identify which paper
  version they are tracking.
- `§2.1`, `§5.7`, `§3.7`, `§3.7.2`, `§3.7.6`, `§1.3`, `§1.4`, `§6
  Limitations`: verified against v9 structure and found correct; no edits.

## Constraints honored

- No em-dashes introduced in new prose. Existing em-dashes preserved when
  replacing section numbers in otherwise-unchanged sentences.
- Only DATA_REFERENCE.md and KEY_FINDINGS.md modified. v9 and v8 paper
  drafts untouched.
