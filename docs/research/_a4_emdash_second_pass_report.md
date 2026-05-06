# Em-dash Second-Pass Structural Review

**Target:** `docs/beyond_recall_v9_draft.md`
**Scope:** Re-review of the 57 sites converted by the first-pass sweep (report: `_a4_emdash_sweep_report.md`), plus any em-dashes the first pass missed.

## Summary

| Metric | Count |
|---|---:|
| Sites re-reviewed (first pass) | 57 |
| Sites fixed in second pass | 2 prose (L642, L648) |
| First-pass-missed em-dashes fixed (bonus) | 3 sites (L744, L745, L757; 4 em-dash characters) |
| **Total edits this pass** | **5** |
| Sites left as-is | 55 of the 57 first-pass sites |
| Em-dash character count before second pass | 17 (line matches 17) |
| Em-dash character count after second pass | 14 line matches (all inside italic-quoted verbatim material or the fenced code block) |

No new em-dashes introduced. Count decreased.

## Fixes applied

### 1. L642 — bold header gloss was a comma-splice with nested parens

**Before:**
```
> **With facts alone (C4, 5-judge mean 2.80), effectively a non-answer:**
```

**After:**
```
> **With facts alone (C4, 5-judge mean 2.80).** Effectively a non-answer:
```

**Rationale:** The first-pass comma put three separators (comma inside parens, second comma, terminal colon) inside a ~10-word bold header. Splitting into two sentences — the bold ends with a period and the gloss continues as a short fragment with its own colon — reads as header + gloss rather than comma-spliced compound caption. Matches the grammar-break the original em-dash was carrying.

### 2. L648 — same mechanism as L642

**Before:**
```
> **With facts + specification (C4a, 5-judge mean 5.00), near-perfect inference:**
```

**After:**
```
> **With facts + specification (C4a, 5-judge mean 5.00).** Near-perfect inference:
```

**Rationale:** Parallel to L642. Header + gloss rather than comma-spliced compound caption.

### 3. L744 — table-cell em-dash missed by first pass

**Before:**
```
| C2c_max-distance (wrong spec, Babur's — maximally different profile) | **2.34** | +1.32 | 0 |
```

**After:**
```
| C2c_max-distance (wrong spec: Babur's, maximally different profile) | **2.34** | +1.32 | 0 |
```

**Rationale:** First pass did not catch this em-dash (it was classed among "20 preserved in verbatim quotes" but is actually a live table-cell annotation inside parens, not a quoted verbatim). Replaced with colon + comma: colon introduces the named wrong-spec, comma gives the qualifier. Grammar inside the parens is now `wrong spec: Babur's, maximally different profile`.

### 4. L745 — table-cell em-dash missed by first pass

**Before:**
```
| C2c_random (wrong spec, Seacole's — seed=42 random draw) | **2.19** | +1.16 | 0 |
```

**After:**
```
| C2c_random (wrong spec: Seacole's, seed=42 random draw) | **2.19** | +1.16 | 0 |
```

**Rationale:** Parallel to L744.

### 5. L757 — prose matched-pair em-dashes missed by first pass

**Before:**
```
Both readings preserve the core claim — the *correct* spec still outperforms every wrong spec tested, and the ordering is strictly monotone in anchor overlap — but the magnitude of the floor-effect term is larger than the +0.25 estimate derived from the historical low-baseline slice.
```

**After:**
```
Both readings preserve the core claim: the *correct* spec still outperforms every wrong spec tested, and the ordering is strictly monotone in anchor overlap. What changes is the magnitude of the floor-effect term, which is larger than the +0.25 estimate derived from the historical low-baseline slice.
```

**Rationale:** First pass did not catch this. It is a real prose matched-pair em-dash, not a quote. Split into two sentences: first sentence uses a colon to carry the claim elaboration; second sentence starts a new thought ("What changes is...") that pivots to the magnitude caveat. Reads cleanly as two distinct ideas rather than one comma-spliced compound sentence. Preserves all factual content (core claim + ordering direction + magnitude caveat + comparison baseline).

## Sites considered but left as-is

Per advisor guidance and re-reading: the label/caption conversions (periods after "Example A", "Pattern 1", section bullets, Supermemory example headers, table captions, "Reading." labels) follow caption grammar, not sentence grammar. Periods and colons read as native label separators in those positions. No change needed.

Specific sites considered and explicitly declined:

- **L11** (`*v7 working draft, appended section by section...*`) — comma before modifier is standard English. Reads fine.
- **L694** (table subheader `**Low-baseline slice (C5 ≤ 2.0), population of relevance**`) — two-beat caption, comma works.
- **L835** (figure caption) — period works as native caption separator.
- **L861, L867** (`Example: Hamerton, the compression story at its clearest`) — colon + comma works as header + subtitle + subtitle-modifier. See report discrepancy note below.
- **L942, L957, L978** wrong-spec example headers — same pattern as L861/867, reads fine.
- **L972/L974** (`**Reading, not parroting.**` and `A10 Charismatic Override: a conquistador's martial-providential register.`) — the first is a standard "X, not Y" contrastive construction; the second is a colon introducing a gloss. Both read fine.
- **L976** (`**Why the correct spec still outperformed, 4.80 vs. 4.60.**`) — borderline. Comma inside a bold caption introducing a score parenthetical reads as an aside; restructuring to parens would work but is not a material improvement. Left as-is.
- **L1116** (`Plain answer matched the plain ground truth: practical observation, translation-as-bridge, foundational-over-specialized machine shop.`) — colon reads well. Left as-is.
- **L1144 / L1146** (`Reads the facts ambivalently as "partial but not complete alignment."`) — first pass rewrote to `as` preposition rather than punctuation swap. Clean.
- **L1306, L1362** (matched-pair em-dashes converted to parentheses) — parentheses read cleanly in both cases.
- **L1392/L1394** (`The two systems converge on interpretive behavior: both produce responses...`) — colon introducing elaboration. Clean.
- **Table-cell null placeholders** (13 cells `| - |`) — these are data-cell nulls, not prose, plain ASCII is correct.

## Discrepancies flagged to author

### Reporting discrepancy in first-pass report

The first-pass report (`_a4_emdash_sweep_report.md`, L47) records L859/L865 as "em-dash to comma", but the actual current text at L861/L867 reads `Example: Hamerton, ...` and `Example: Ebers, ...` (colon + comma, not a single comma). The conversion itself is fine and reads well; the first-pass report entry was inaccurate about the substitution used. No fix needed to the text.

### First-pass under-counted preserved em-dashes

The first-pass report summary claimed "Remaining at end: 20" and classified all 20 as verbatim-quote or code-block content. In reality, the first pass missed 4 em-dash characters across 3 sites that are live prose/table content, not quoted verbatim:

- L744, L745 (2 em-dashes, table-cell annotations inside parens)
- L757 (2 em-dashes, prose matched pair)

All three sites are now fixed. The true starting "remaining" count after the first pass was therefore 17 line-matches (not 20), of which 3 were live-prose carry-overs that this second pass caught and fixed. Ending count is 14 line-matches, all inside italic-quoted verbatim spec material, verbatim model-response quotes, or the single code block on L399 (prompt-template pseudocode).

### Judgment call the author may want to revisit

**L976** (`**Why the correct spec still outperformed, 4.80 vs. 4.60.**`): left as-is. An alternative reading would prefer parentheses: `**Why the correct spec still outperformed (4.80 vs. 4.60).**` — this is cleaner because the score is strictly a parenthetical reference, not an apposition of the verb phrase "outperformed." If the author prefers the parenthetical reading, change this site.

## Verification

- Em-dash count decreased (17 → 14 line matches; 4 em-dash characters removed).
- All remaining em-dashes verified to be inside:
  - Verbatim italic-quoted model response text (L612, L616, L955, L995)
  - Verbatim italic-quoted specification body text and anchor labels copied from `data/global_subjects/` spec files (L949, L951, L964, L966, L968, L985, L987, L989, L991)
  - Fenced code block (L399)
- No new em-dashes introduced by any second-pass edit.
- No en-dashes touched.
- v8 draft untouched.
