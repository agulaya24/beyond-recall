# Em-dash discretionary audit — Beyond Recall v11.8 (2026-05-05)

## Summary
- Total em-dashes: 33 lines (multiple instances on some lines; 33 distinct line occurrences across the file)
- STRUCTURAL_OK: 32
- PROSE_FLAGGED: 1

## STRUCTURAL_OK breakdown
- In tables (cell separator or table-cell quote): 11
  - Lines 796-801 (Table 4.1 missing-data separator): 6
  - Line 855 (verbatim quoted excerpt inside table cell): 1
  - Lines 1307-1311 (Table 4.4.3 cell qualifiers "yes — large", "no — within noise"): 5
- In blockquoted source / axiom labels / quoted model output: 20
  - Line 229 (quoted model response inside `> ` worked example, contains axiom label `**P3 — Tension Absorbed, Not Expressed**`): 1
  - Lines 240-243 (axiom label list `> - **A1 — Divine Primacy.**` etc.): 4
  - Lines 729, 731 (quoted model response inside `> ` worked example): 2
  - Lines 1059, 1061 (axiom label `**A4 — SYSTEMIC INDICTMENT:**` + em-dashes inside quoted spec content): 2
  - Line 1065 (quoted model response inside `> > *"..."*`): 1
  - Lines 1074, 1076, 1078 (axiom labels `**A5 — RELATIONAL IDENTITY:**` etc. + em-dashes inside quoted spec content): 3
  - Lines 1095, 1097, 1099, 1101 (axiom labels A1, A2, A4, A5 inside `> >` blockquote): 4
  - Line 1105 (quoted model response inside `> > *"..."*`): 1
  - Line 1301 (footnote with axiom labels + em-dashes inside quoted axiom source `*"..."*`): 1
  - Line 16 (HTML comment block, verbatim quote of author's spoken framing): 1
- Other: 0

## PROSE_FLAGGED items

| Line | Current text snippet | Proposed restructure | Rationale |
|---|---|---|---|
| 1170 | "...shifts share-zero to 40.4% (14 subjects) or 41.0% (13 globals) **— every cut shows substantial top-K divergence on identical input.** Reproducibility script at..." | "...shifts share-zero to 40.4% (14 subjects) or 41.0% (13 globals); every cut shows substantial top-K divergence on identical input." | Author-prose em-dash inside footnote `[^share-zero-cut]` connecting two independent clauses. Semicolon preserves the comparative bridge between the parenthetical figures and the summary clause without introducing a hyphen. Period would also work but would slightly weaken the linkage between data and reading. |

## Notes on conservative classifications

- **HTML comment (line 16):** The em-dash is inside `<!-- ... -->` and is also inside double-quoted spoken material attributed to the author. Two reasons to keep STRUCTURAL_OK: (a) the comment block does not render in any output, (b) it is a verbatim quote, not author-voice prose.
- **Table-cell qualifiers (lines 1307-1311):** "yes — large negative" / "no — within noise" function as compact labels inside a tabular column ("Pattern 3 ... ?"). The em-dash is acting as a structural separator between the yes/no token and the magnitude qualifier, not as prose punctuation. Restructuring would require splitting one column into two, which is a layout change, not a prose cleanup.
- **Footnote line 1301:** All em-dashes on this line are either inside an axiom label pattern (`**A1 — INTIMATE AUTHORITY:**`, `**A2 — DOCUMENTED DIGNITY:**`) or inside the verbatim italicized spec text quoted from the source axiom file (`*"...private life — domestic, relational, embodied — is treated..."*` and `*"...moral vindication — proof that..."*`). Spec-source quotes are STRUCTURAL_OK by the rubric.
- **Quoted model responses (lines 229, 729, 731, 1065, 1105):** All sit inside `> ` or `> > ` blockquote blocks and are either italicized with `*"..."*` or rendered as verbatim model output. None are author prose.
- **Axiom-label pattern (lines 240-243, 1059, 1061, 1074, 1076, 1078, 1095, 1097, 1099, 1101):** All match `**<ID> — <Title>**` or `**<ID> — <Title>:**` format, which the audit rubric specifies as STRUCTURAL_OK.

## Recommended action

Single PROSE_FLAGGED item at line 1170. Apply the semicolon restructure when convenient. All other em-dashes are inside tables, blockquoted source material, axiom labels, or non-rendered HTML comments and do not violate the no-em-dash-in-prose rule.
