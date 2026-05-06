# A10 Section-Reference Sweep Report

**Paper:** `docs/beyond_recall_v9_draft.md` (v9 draft, 2,441 lines)
**Rule:** Every forward/backward reference that points at a DIFFERENT section of the paper must include an explicit `§X.Y` pointer. In-paragraph and same-subsection locators are left as-is.
**Scope:** Body sections §1-§7 (appendices A-E scanned but not modified; they are read selectively and their locators are all internal or already-§-pointered).

## Summary

- **Files scanned:** 1 (full v9 draft)
- **Grep matches on `below|above|later|earlier|following|preceding`:** 71 lines (many with multiple hits)
- **Genuine cross-subsection candidates identified:** 2
- **Fixes applied:** 2
- **Left as-is (locally clear, word-sense, or already-§-pointered):** the remainder

## Fixes applied

### 1. Line 1291 — cross-subsection reference to mechanisms defined in §4.4.2

**Before:** `Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-system refusal)...`

**After:** `Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal from §4.4.2, and the Keckley Q21 cross-system refusal from §4.4.3)...`

**Rationale:** Sits inside §4.4.3's "What this means for measurement" block. Patterns 1/2/3 are defined in §4.4.2 and the Keckley Q21 case study is §4.4.3. The `above` locator spans the subsection boundary; explicit pointers remove the ambiguity without changing meaning.

### 2. Line 1299 — transition paragraph bridging §4.4 and §4.5

**Before:** `Letta exposes a second memory mode, separate from the archival retrieval path evaluated above, in which the agent writes and revises a persistent memory block...`

**After:** `Letta exposes a second memory mode, separate from the archival retrieval path evaluated above in §4.4, in which the agent writes and revises a persistent memory block...`

**Rationale:** This is the transitional paragraph ending §4.4 (and its sub-sections) before §4.5 begins. The "archival retrieval path evaluated above" is the whole of §4.4, not a single local table. Adding `§4.4` makes the cross-section reference explicit.

## Locators reviewed and left as-is (sampled rationale)

The 71 matches break into four non-candidate buckets:

### Bucket A — Rubric / score language (not section references)
- "score below 2.0", "above baseline", "at or above 3.0", "below the rubric floor", "above the anchor-3 band", "score 4.5 or above", "score below 2.0", "mean 1.14, roughly 0.27 points above..."
- Sample: Line 614 ("pretraining baseline sits at or below 2.0 on the 1-5 rubric"), Lines 2166, 2175, 2177, 2214, 2216.
- These are numeric-comparison locutions, not paper-internal cross-references.

### Bucket B — List / table / procedure introductions (referent immediately adjacent)
- "the three-step procedure below" (line 567) — rule is the numbered list directly below.
- "examples below are drawn from..." (line 329) — blockquote examples immediately below.
- "the following parameters" (line 2023) — parameter list immediately follows.
- "the following table gives the count" (line 1915) — table on next line.
- "the numeric breakdowns below are produced by that script" (line 577) — same subsection.
- These are local introducers; adding `§X.Y` would be noise since the referent is the next line.

### Bucket C — Same-subsection proximity (locally clear)
- Line 64: "this path is not exercised by the retrieval conditions above" — §1.2 referring to the conditions table in the same §1.2.
- Line 329: "examples below are drawn from the Hamerton specification" — blockquote examples in §3.3 itself.
- Line 412: "archival retrieval (the path tested in C1 / C3 above)" — condition table immediately preceding in §3.5.
- Line 466: "the rubric table above" — same subsection (§3.7).
- Line 634: "Three representative examples below show..." — examples immediately below in §4.1.
- Line 901, 929, 933, 939, 942: Example B/C "below" references — same subsection (§4.3).
- Line 1098, 1112: "explained below" / "dedicated Supermemory section below" — Supermemory deep dive is in the same §4.4.1.
- Line 1130: "Each illustrated below with a paired C1 vs C3 example" — same Supermemory block in §4.4.1.
- Line 1200-1202: "Pattern 1 and Pattern 4 ... The three mechanisms above" — Patterns defined inline in §4.4.1.
- Line 1216: "Letta's archival-retrieval path is reported above in the §4.4.1 memory-system table" — already carries explicit §4.4.1 pointer. LEAVE.
- Line 1228: "Each row below is one subject under one memory system" — table immediately below in §4.4.2.
- Line 1305: "stateful-agent design... with the caveats above" — caveats in §4.5's opening paragraph.
- Line 1321: "The table column header below reflects this" — table immediately below in §4.5.
- Line 1353: "see content comparison below" — Content comparison subsection at line 1357 in §4.5.
- Line 1365: "hoisted above the result Table at the top of this section" — self-reference within §4.5.
- Line 1466: "narrower than any of the above" — the five anti-patterns just listed above in §5.1.
- Line 1538: "The discussion below distinguishes..." — the §5.5 discussion that immediately follows.
- Line 1616: "alternative approaches above" — the three bullets in the preceding §5.5 "Positioning against alternative approaches" subsection.
- Line 1633: "does not demonstrate the following" — the list directly below within §5.6.
- Line 1663: "interacts with safety-relevant contexts in the way described above" — in §5.7, references the "Where the two axes bleed together" paragraph in the same §5.7.
- Appendix D lines 2154, 2166, 2175, 2177, 2210, 2214, 2216 — all rubric / score arithmetic, same-subsection.

### Bucket D — False-positive word matches (not locators at all)
- Line 81 ("following official advice"), Line 115 (same quote), Line 1904 ("difficulty following spoken French") — verb "following" as in "obeying", not a locator.
- Line 183 ("An earlier Zep claim"), Line 202 ("An earlier exploratory Base Layer run"), Line 2397 (same), Line 2409 ("queried in a later session"), Line 2327 ("queried in a later session"), Line 2415 ("earlier Zep claim") — "earlier" / "later" referring to historical events or time sequences, not to earlier sections of the paper.
- Line 125, 1703, 2397 — "prior iteration", "following" inside other constructions.

### Bucket E — Already correct
- Line 765 already has "§1.4 made the extrapolation argument..." — explicit.
- Line 1216 already has "reported above in the §4.4.1 memory-system table" — explicit.
- Line 1331 already has "above the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec...)" — explicit.
- Line 1285 already has "(§3.7.6 validity audit, §4.4 Example 3)" — explicit.

## Ambiguous cases flagged for author review

**None.** Every locator in the draft either (i) references something locally adjacent (same subsection or immediately-next block) or (ii) already carries an explicit `§X.Y` pointer. The prose is tightly sectioned. The two edits applied fix the only two genuine cross-subsection ambiguities I could identify.

## Note on scope

Appendices A-E were scanned. All locator uses there are appendix-internal ("the 45 above" on line 1874 refers to the predicate list in the same Appendix A table) or already carry explicit pointers ("(see §2.1 dispute note)" line 2415, "(see §2.3)" line 2397). No appendix edits were needed.

## Files modified

- `C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.md` (2 edits, lines 1291 and 1299)
