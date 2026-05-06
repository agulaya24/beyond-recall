# Appendix completeness audit — Beyond Recall v11.8 (2026-05-05)

## Summary
- Appendices present: A / B / C / D / E / F / G / H (all 8)
- Body-to-appendix references: 42 occurrences across the body (§1-§9 + footnotes)
- Resolved: 39
- Broken: 3 (one placeholder, one missing-content pointer, one verbatim chain claim)
- Orphan content: 0 within scope of "appendix subsection not reachable from body"; multiple subsections reachable only via parent-appendix reference (acceptable for reference material, not flagged as orphan)
- Structural anomaly: 1 (Appendix G has no labelled subsections; A-F + H all use sub-numbering)
- Body-text drift: 1 (the L1810 §9 "Appendices" summary undersells Appendix B)

Source paper: `docs/beyond_recall_v11_8_draft.md`, 3,222 lines, Appendices L1814-L3222 (1,409 lines, ~23,679 words).

## Per-appendix audit

### Appendix A — Predicate Vocabulary (L1814-L1921, ~1,386 words, 109 lines)
- Subsections: A.1 The 46 Constrained Predicates (with 7 grouped tables); A.2 Provenance and design choices; A.3 Not in the vocabulary; A.4 Live deployment.
- Body references: L645 ("full predicate list is in [Appendix A]"), L1810 §9 summary.
- Predicate count check: 46 entries across the seven tables (verified by grep `\| \`[a-z_]+\` \|`).
- Body-claim match: §3.7 says "fixed vocabulary of 46 behavioral predicates" — A.1 delivers exactly 46. Match.
- Status: COMPLETE. Subsections A.2/A.3/A.4 reachable only via parent ref; this is appropriate for reference material.

### Appendix B — Question Batteries (L1923-L2128, ~3,725 words, 206 lines)
- Subsections: B.1 The 10 fixed behavioral-prediction categories; B.2 Per-subject battery composition (10x15 matrix); B.3 Behavioral-axis distribution (LITERAL/INTERPRETIVE/REFUSAL-TRIGGERING); B.4 Category-level effect size; B.5 Per-subject by axis Δ_spec; B.6 Battery-composition sensitivity (with B.6.1-B.6.5); B.7 Coupling-free reframing (B.7.1-B.7.4); B.8 Per-predicate ablation (Phase 2c); B.9 Footnote-redirect technical detail (B.9.1-B.9.3); B.10 Pre-registered hypotheses and post-hoc analyses (table).
- Body references: L56 (B.10), L122 (B.9), L351 (B.1, B.2), L769 (B.6), L817 (B.9), L1424 (B.6), L2117-L2119 (B.6, B.7 from within the B.10 table itself).
- Match check: B.1+B.2 deliver categories and 15-subject by 10-category matrix. B.6 delivers full regression detail. B.7 delivers level-regression + permutation + bootstrap. B.9.1 delivers +0.89 vs +0.93 reconciliation. B.10 delivers H1-H5 + post-hoc table. All match body promises.
- L1810 §9 "Appendices" summary describes B as "per-subject battery composition and category-level effect sizes" — this undersells B.6/B.7/B.8/B.9/B.10 (sensitivity, coupling, predicate ablation, footnote redirect, pre/post-hoc). Body-content drift but not a broken cross-reference.
- Status: COMPLETE; the L1210 / L1214 "Appendix B.X" placeholder is a separate issue documented below.

### Appendix C — Conditions, Models, and Memory-System Configurations (L2129-L2231, ~1,212 words, 103 lines)
- Subsections: C.1 Condition identifiers (summary card); C.2 Shared response-model invocation; C.3 Response models; C.4 Pipeline models; C.5 Judge panel; C.6 Memory-system ingestion and retrieval parameters; C.7 Ingestion exclusions and failure cases; C.8 Analysis plan lock.
- Body references: L410 (Appendix C), L442 (Appendix C), L464 (summarized in Appendix C), L949 footnote `[^multi-anchor-rates]` ("§3.4 and Appendix C"), L2078 ("Appendix C / §4.3").
- Match check: C.1 delivers C5/C2a/C2c/C4/C4a/C8/C9/C1/C3 condition table promised by §3.4. C.3-C.4 deliver model identifiers promised by §3.5. C.5 delivers 7-judge panel from §3.6.3. C.6 delivers memory-system parameters from §3.4. All match.
- Status: COMPLETE.

### Appendix D — Validity Audit and Score Distributions (L2232-L2446, ~3,414 words, 215 lines)
- Subsections: D.1 Per-subject 5-judge primary aggregate (main gradient table, 15 rows); D.2 Per-subject anchor-crossing on the low-baseline slice (9 rows); D.3 Rubric-handling validity audit (with D.3.1 Abstention detection, D.3.2 Score distribution, D.3.3 Per-judge strictness, D.3.4 Length-score correlation, D.3.5 Ultra-high-score validity, D.3.6 Implications); D.4 Per-judge score matrices (14 subjects x 5 conditions x 9 columns = 630 cells); D.5 Example verbatim responses at each rubric anchor (cross-pointer to §3.6 + §4.1 + Appendix E).
- Body references: L464 ("[Appendix D](#appendix-d-validity-audit-and-score-distributions)"), L811 ("anchor-crossing distributions... in Appendix D"), L1810 §9 summary.
- Match check: D.1 reproduces the §4.1 gradient (15 subjects, including Franklin). D.2 delivers anchor-crossing across the 9-low-baseline slice. D.3 is the formal validity audit §3.6.6 summarizes. D.4 is the per-judge matrix promised by L811. D.5 cross-references rather than holds new content (acceptable).
- Status: COMPLETE.

### Appendix E — Selected per-subject excerpts (L2447-L2969, ~9,008 words, 523 lines)
- Subsections: E.1 Hamerton through E.14 Zitkala-Sa, one per main-study subject (14 sections).
- Each section: ~36 lines, 3 paired (C5, C4a) per-question excerpts with response text and 5-judge primary scores.
- Body references: L2443 (D.5 redirect: "Three illustrative paired (C5, C4a) per-question excerpts for each of the 14 main-study subjects are collected in Appendix E"); L1810 §9 summary repeats this promise.
- Match check: 14 subjects covered (E.1-E.14), all matching the body's "three illustrative paired (C5, C4a) per-question excerpts" claim.
- Status: COMPLETE.

### Appendix F — Benchmark Scope Analysis (L2970-L3098, ~1,931 words, 129 lines)
- Subsections: F.1 LongMemEval; F.2 PersonaGym; F.3 AlpsBench; F.4 Twin-2K; F.5 LoCoMo; F.6 MemOS and related systems-level benchmarks; F.7 What no prior benchmark measures.
- Body references: L30 ("Appendix F develops the scope differences in detail"), L162 ("extended benchmark-by-benchmark analysis is in Appendix F"), L170 footnote `[^twin2k-persona-size]` ("Full breakdown of persona-input depth across benchmarks in Appendix F"), L1810 §9 summary.
- Match check: F.1-F.6 deliver per-benchmark Reference / Task / Scoring / Protocol / What it measures / What it does not measure / Relationship-to-this-paper schema. F.4 (Twin-2K) describes persona construction qualitatively ("subset of survey answers is used to author a persona... served to a model as context") but does NOT include the persona-input-depth breakdown the L170 footnote promises (no token counts for `persona_text` ~32K vs `persona_summary` ~3,750, and no comparison row across PersonaGym one-line / AlpsBench preference history / Twin-2K persona / Base Layer 7K spec).
- Status: PARTIAL. F.1-F.7 land the qualitative scope analysis. The persona-input depth breakdown promised by the `[^twin2k-persona-size]` footnote is missing.

### Appendix G — Letta Stateful-Agent: Exploratory Case Study (full) (L3099-L3190, ~2,361 words, 92 lines)
- Subsections: NONE labelled. Content organized as prose with `---` separators across blocks: headline result + framing, Test design, Methodological note on Base Layer condition, Result table, Judge-panel robustness, Compression behavior + Semantic-similarity duplication, What this exploration does and does not show, Content comparison, Replication as load-bearing next step, Caveats, Raw data and scripts.
- Body references: L56 (`[^pre-vs-post-hoc]`: "§4.5; Appendix G"), L134 ("Case study in §4.5 / Appendix G"), L207 ("examined separately as a post-hoc case study in §4.5 (full case study in Appendix G)"), L677 ("Brief summary in body; full case study in Appendix G"), L1352 ("the full case study is in Appendix G"), L1364 ("...are in **Appendix G**"), L1472 (G referenced for Letta duplication threshold context), L1710 (§7.5 ref), L2112 (B.10 table), L2113 (B.10 table), L1810 §9 summary.
- Match check: Headline N=3 result table + 5/7-judge robustness + compression + verbatim + semantic-similarity duplication + content comparison + caveats + raw-data pointers all present and match §4.5 body summary.
- Status: COMPLETE on content. STRUCTURAL ANOMALY: no G.1/G.2/etc. sub-numbering in an appendix this long; A-F and H all use sub-numbering. Not a broken reference (no body ref says "Appendix G.X"), but inconsistent with the rest.

### Appendix H — Glossary (L3191-L3222, ~642 words, 32 lines)
- Subsections: NONE labelled (single bolded-term list, alphabetical-ish). 14 entries: 5-judge primary panel, 7-judge sensitivity panel, Anchors / Core / Predictions, Behavioral prediction, Behavioral specification, Cross-anchor interpretation rule, Interpretation, Multi-anchor crossing, Personalization (this paper's sense), Refusal (abstention), Representational accuracy, Specification-effect claim, Tier 1 / Tier 2, Wrong-spec control.
- Body references: L38 ("Defined terms... collected in [**Appendix H**](#appendix-h-glossary)"), L1810 §9 summary.
- Match check: "Personalization (this paper's sense)" entry confirmed present (the audit task flagged this as added tonight). All 14 entries are terms-of-art used in body §1-§7.
- Status: COMPLETE.

## Broken cross-references

| Body line | Reference | What's missing | Recommended fix |
|---|---|---|---|
| L1210 + L1214 (footnote `[^memsys-pattern-appendix]`) | "Appendix B.X" + "Appendix B.X (forthcoming, to be moved during appendix walk)" | The per-system per-subject paired-delta table referenced (Mem0 / Letta archival / Zep / Base Layer x representative subjects). Inline values appear in the footnote itself but the consolidated table promised in Appendix B has not been added. | Either (a) add new subsection **B.11 Per-system per-subject paired-delta distributions** holding the table, then change "Appendix B.X" → "Appendix B.11" in both L1210 body and L1214 footnote, or (b) drop the "in Appendix B.X" pointer if the inline footnote is intended to stand alone. The footnote explicitly self-flags "to be moved during appendix walk" — the appendix walk is now complete, so option (a) closes the open promise. |
| L170 (footnote `[^twin2k-persona-size]`) | "Full breakdown of persona-input depth across benchmarks in Appendix F" | Persona-input depth comparison table across LongMemEval / PersonaGym / AlpsBench / Twin-2K (`persona_text` ~32K, `persona_summary` ~3,750) / LoCoMo / Base Layer specification. F.4 prose mentions persona construction but no token-count comparison anywhere in Appendix F. | Add a "Persona-input depth across benchmarks" table either as new subsection **F.8 Persona-input depth comparison** at end of F, or fold a token-count column into the existing per-benchmark prose. Either drops the L170 footnote claim into resolved-state. |
| L248 (§2.3 audit walk-through, Sunity Devee fact-chain box) | "Additional facts grounding A1, A5, and P3 are referenced in the specification's anchor and prediction files; the full chain is enumerated in Appendix B." | The full fact-chain enumeration for Sunity Devee (F-73 + F-414 are shown inline; the "additional facts" grounding A1, A5, P3 are not enumerated anywhere in Appendix B). | Either (a) add **B.X Sunity Devee fact-chain audit** (small subsection enumerating ~6-10 facts grounding A1/A5/P3, sourced from her facts.json), or (b) soften L248 to "referenced in the specification's anchor and prediction files (`results/global_sunity_devee/anchors.md`, `predictions.md`)" and drop the "Appendix B" pointer. Option (b) is lighter-touch; option (a) closes the audit promise. |

## Orphan content
None in scope. All appendix subsections are reachable from body either by direct subsection reference (B.1, B.2, B.6, B.7, B.9, B.10) or via parent-appendix reference (A, C, D, E, F, G, H + the unreferenced B.3, B.4, B.5, B.8). For reference material this is acceptable; the L1810 §9 paragraph plus the within-section navigation cover the parent-level pointers.

If a tighter standard is desired: B.3 (axis distribution) + B.4 (category-level effect size) + B.5 (per-subject by axis) currently have no direct subsection reference from body. They feed §B.6.2's regression on LITERAL_RECALL fraction, so the content is load-bearing, but the body never points to B.3/B.4/B.5 by number. Adding a `(detail in Appendix B.3-B.5)` parenthetical at §3.3 (battery-formation) or §4.6.3 (battery-composition sensitivity) would close the loop. Optional, not blocking.

## "Appendix B.X" placeholder status
PENDING. Two occurrences both at the same content point (L1210 body + L1214 footnote). The reference is to a per-system per-subject paired-delta table for Mem0 / Letta archival / Zep / Base Layer over representative subjects. The footnote explicitly self-describes as "forthcoming, to be moved during appendix walk." The appendix walk through §4-§5 is now complete (per the v11 paper draft state in user's project memory), so this placeholder should resolve in the next pass.

Suggested landing: a new subsection **B.11 Per-system per-subject paired-delta distributions** (between B.10 pre/post-hoc table and the Appendix C divider). Inline values from the L1214 footnote already exist; the table can be machine-emitted from `docs/research/per_system_anchor_crossing_20260427.json` via `scripts/_table_4_6_5judge_recompute.py` (path cited in the footnote itself).

## Action list
1. **L1210 + L1214 "Appendix B.X" placeholder.** Decide: add B.11 subsection vs. drop the appendix pointer. If adding B.11, source from `docs/research/per_system_anchor_crossing_20260427.json`. Touches 2 lines body + 1 new appendix subsection.
2. **L170 footnote `[^twin2k-persona-size]` Appendix F persona-depth breakdown.** Add F.8 (or a comparison table inside F.4) covering persona-input token counts for the 4-5 benchmarks named in the footnote. Touches 1 footnote-claim resolution + 1 new appendix subsection or table.
3. **L248 Sunity Devee fact-chain Appendix B reference.** Lighter-touch: change "Appendix B" → direct file pointer (`anchors.md`, `predictions.md`). Heavier-touch: add subsection enumerating the full fact chain. Touches 1 line body or 1 new appendix block.
4. **L1810 §9 "Appendices" summary undersells Appendix B.** Optional. Current text describes B as "per-subject battery composition and category-level effect sizes" — does not mention sensitivity/coupling/ablation/footnote-redirect/pre-vs-post-hoc table. One-line update would re-align summary to Appendix B contents.
5. **Appendix G structural anomaly (no G.1/G.2 labelling).** Optional. Adding G.1 Test design / G.2 Result / G.3 Compression / G.4 Content comparison / G.5 Caveats / G.6 Raw data would bring G into structural parity with A-F + the H glossary's bolded-term-list convention. No body refs would break.
6. **B.3 / B.4 / B.5 unreferenced subsections.** Optional. Add a parenthetical pointer at §3.3 or §4.6.3 to close the navigation loop.

Items 1, 2, 3 are real broken references and should resolve before content freeze. Items 4, 5, 6 are polish.
