# Em-dash / En-dash Sweep Report

**Target:** `docs/beyond_recall_v9_draft.md`
**Preserved (untouched):** `docs/beyond_recall_v8_draft.md` (77 em-dashes, 27 en-dashes, 270,138 bytes, unchanged)

## Summary

| Metric | Em-dash (U+2014) | En-dash (U+2013) |
|---|---:|---:|
| Found at start | 77 | 28 |
| Restructured / converted | 57 | 28 |
| Skipped (verbatim quotes or code block) | 20 | 0 |
| Remaining at end | 20 | 0 |

Note: starting count for en-dashes was 28 (task estimated ~27). One additional dash lived inside a Unicode minus-sign context but was verified distinct.

Minus signs (U+2212) such as `−0.31` were explicitly left intact. Only U+2014 and U+2013 were targeted.

## Em-dashes: what was done

**Category: heading / caption / label separators (colon or comma).** 23 replacements.

- Table 2.1 caption: em-dash to period.
- Section TOC bullets L565-L572 (§4.1 through §4.8): em-dash to period.
- Example A/B/C/D headers L604, L620, L636, L678: em-dash to period.
- Section 4.2.1 heading L807: em-dash to colon.
- Hamerton / Ebers example headers L859, L865: em-dash to comma.
- Wrong-spec example headers L942, L957, L978 (already had colon after the em-dash): em-dash to comma to avoid double-colon.
- Supermemory example headers L1096, L1111, L1126, L1139: em-dash to period.
- Pattern 1 / 2 / 3 bullets L1282-L1284: em-dash to period.
- Table 4.6 caption L1272: em-dash to period.

**Category: table-cell null placeholders.** 13 replacements (`| — |` to `| - |`).

All in §4.1 gradient table body (L700-L711, including the pair on L1054 `| Base Layer | - | N/A | - | N/A |`), L741, L792, L1088. These are data-cell nulls, rendered as plain hyphens per the paper-wide no-em-dash rule.

**Category: prose em-dashes restructured.** 11 replacements across 9 sentences.

| Line | Original structure | New structure |
|---|---|---|
| L11 | `*v7 working draft — appended section by section...*` | comma |
| L642 | `**With facts alone (...) — effectively a non-answer:**` | comma |
| L648 | `**With facts + specification (...) — near-perfect inference:**` | comma |
| L652 | matched-pair em-dashes around "documented in the facts but not explicitly mapped to this scenario" | parentheses |
| L694 | table subheader `**Low-baseline slice (C5 ≤ 2.0) — population of relevance**` | comma |
| L835 | figure caption `Figure 4.2.1 — Per-question outcome distribution...` | period |
| L972 | `**Reading — not parroting.**` and `A10 Charismatic Override — a conquistador's martial-providential register.` | comma; colon |
| L1116 | `Plain answer matched the plain ground truth — practical observation, translation-as-bridge...` | colon |
| L1144 | `Reads the facts ambivalently — "partial but not complete alignment."` | restructured as `Reads the facts ambivalently as "partial but not complete alignment."` |
| L1306 | matched-pair em-dashes around the Keckley Q21 question text | parentheses |
| L1362 | matched-pair em-dashes around `5-judge Δ +0.14 vs. 7-judge +0.20` parenthetical | parentheses + comma |
| L1392 | `The two systems converge on interpretive behavior — both produce responses that outperform retrieval-only context` | colon |

## Em-dashes: what was skipped

**20 em-dashes remain, all inside verbatim-quoted material or a code block.** No restructuring applied per task rule.

| Line | Reason |
|---|---|
| L399 | Inside fenced code block (prompt-template pseudocode between triple backticks on L394 and L404). Task instruction: code blocks left alone. |
| L612 | Verbatim model response text inside `*"..."*` italic quotation (baseline Ebers response). |
| L616 | Verbatim model response text inside `*"..."*` italic quotation (facts + spec Ebers response). |
| L947 (x3) | Anchor label `**A4 — SYSTEMIC INDICTMENT:**` verbatim from `data/global_subjects/equiano/spec_production.md:48` plus 2 em-dashes inside the italic-quoted spec body text `*"avarice — institutionalized greed —..."*` which is verbatim from `spec_production.md:50`. |
| L949 (x2) | Anchor label `**A9 — ECONOMIC SELF-DETERMINATION:**` verbatim from spec + 1 em-dash inside quoted spec body. |
| L953 | Verbatim model response text inside `*"..."*` (wrong-spec Ebers response). |
| L962 (x3) | Sunity Devee anchor label `**A5 — RELATIONAL IDENTITY:**` verbatim + 2 em-dashes inside the verbatim italic-quoted spec body. |
| L964 (x2) | Anchor label `**A9 — SIMPLICITY AS VIRTUE:**` verbatim + 1 em-dash in verbatim body text. |
| L966 | Anchor label `**P5 — VIRTUE THROUGH EMBODIED PRACTICE:**` verbatim. |
| L983 | Anchor label `**A1 — DIVINE MANDATE:**` verbatim from `data/global_subjects/bernal_diaz/spec_production.md:19`. |
| L985 | Anchor label `**A2 — CIVILIZATIONAL HIERARCHY:**` verbatim from spec L25. |
| L987 | Anchor label `**A4 — LOYALTY ARCHITECTURE:**` verbatim from spec L38. |
| L989 | Anchor label `**A5 — FORWARD COMPULSION:**` verbatim from spec L44. |
| L993 | Verbatim model response text inside `*"..."*` (wrong-spec Seacole response). |

Verification of anchor-label verbatim status was done by opening the source spec files (`equiano/spec_production.md`, `bernal_diaz/spec_production.md`) and confirming the exact `**A<n> — LABEL**` format used in the paper matches the source format.

## En-dashes: what was done

All 28 en-dashes were numeric / year ranges (e.g., `1834–1858`, `2.0–3.0`, `7,000–11,000`, `1–5`, `~300–1,500`). All converted to plain ASCII hyphens via a single replace-all pass. No ambiguous cases.

## Ambiguous sentences flagged for human review

None. Every restructure was a local punctuation change that preserves meaning. No paragraph-level rewrites were attempted.

## Caveat on the L399 code block

L399 is a pseudo-prompt template inside a fenced code block:

```
User:   <context block — empty (C5), spec (C2a), wrong spec (C2c),
```

The em-dash here is prose-style (it annotates a placeholder) and the author may wish to replace it with a colon for absolute consistency. Left alone because the task explicitly exempts code blocks. Flagged here for the author to decide.
