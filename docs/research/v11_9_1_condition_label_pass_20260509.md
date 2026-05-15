# V11.9.1 Condition Label Consistency Pass — 2026-05-09

## Format chosen

**Body prose:** `the No-Context Baseline (C5)` — Title Case natural-language label first, code in parens, with definite article "the" when grammatically natural.

**Reasoning.**
1. Aarik's example was "C5- The No-Context Baseline" (Title Case proper-noun phrasing). Em-dash form would conflict with the saved "no em-dashes" rule (LLM tell), so the substitute is parenthetical with the natural label leading.
2. The paper already uses lowercase parenthetical pairing in many places (§3.2 line 112: "the no-context condition (C5)"; §4.1 line 875: "ordered by C5 baseline ascending"; §4.1.1 line 915: "the no-context baseline (C5)"). The pass elevates this existing pattern to Title Case where the label is being introduced as a proper-noun reference, leaving table cells, math expressions, code paths, and intra-table definitional rows untouched.
3. Mid-sentence, "the No-Context Baseline (C5)" reads as the natural English construction. The alternative "C5: The No-Context Baseline" is reserved for headers / definition lines / standalone topic positions but is not used in this pass because the v11.9.1 §3.2 and Appendix C.1 lookup tables already cover that role.
4. The §3.2 first table at lines 82-92 ("**No context** (C5)" bold sentence-case) and Appendix C.1 (line 2416+) are kept as-is. They are definitional lookup tables; introducing Title Case there would be an architecture-style edit and would create different label phrasings between the two tables.

## Canonical labels (derived from §3.2 first table, lines 82-92)

| Code | Title-Case label (body prose) |
|---|---|
| C5 | The No-Context Baseline |
| C2a | Spec Alone (or Specification Alone) |
| C2c | The Wrong-Spec Control |
| C4 | All Facts |
| C4a | Facts + Spec (the Full Pipeline) |
| C8 | Raw Corpus |
| C9 | Corpus + Spec |
| C1 | Retrieval Only (controlled / native) |
| C3 | Retrieval + Spec (controlled / native) |

The paper consistently uses "Spec" (315 occurrences) over "Specification" in body prose, so labels follow that convention.

## Inventory (before)

279 condition-code mentions distributed approximately as follows:

- §3.2 + §3.6 + Appendix C definitional tables: ~50 cells (all with paired natural label by structure of the table)
- §1.3 / §1.4 lookup table (lines 82-92): ~20 mentions, already paired with bold sentence-case labels
- §4.1 / §4.1.1 / §4.2 / §4.2.1: heavy concentration of bare codes in tables (Subject × Condition × Score), all in column headers / row labels where bare is appropriate
- §4.4 / §4.4.3 / §4.4.4: C1 / C3 dominate, mostly already paired with `(retrieval only)` / `(retrieval + Spec)` because §4.4 introduced both terms in §4.4.2
- §4.6.7 / §4.7 summary bullets: ~6 bare-code body prose mentions (the cluster needing label elevation)
- Footnotes: ~30 mentions, mostly definitional or in math expressions
- Appendix B / C / D: ~120 mentions in tables, math, or definitional contexts
- Math / statistical expressions across all sections (`Δ_C4a`, `C5 ≤ 2.0`, `C2a vs. C4`, `C5 vs. C4a`, level slope `C4a ~ C5`): ~80 mentions

## Edits applied

7 substantive prose edits, all clustered in §3.3.6, §4.2, §4.4.4, §4.6.7, and §4.7 where the bare-code-in-prose pattern was unrelieved by a nearby paired label:

1. **Line 573 (§3.3.6 Direction of bias).** `Both effects raise C5 baseline scores` → `Both effects raise the No-Context Baseline (C5) scores`.
2. **Line 1039 (§4.2 corpus exclusion).** `Bābur's C9 condition was excluded` → `Bābur's Corpus + Spec (C9) condition was excluded`.
3. **Line 1466 (§4.4.4 Keckley Q21 lead bold).** `Where C1 was already hedging at the rubric floor … Where C1 was producing a productive answer` → `Where retrieval-only (C1) was already hedging at the rubric floor … Where retrieval-only (C1) was producing a productive answer`.
4. **Line 1719 (§4.6.7 Result).** `raise C5 baseline scores more than they raise Spec-condition scores` → `raise the No-Context Baseline (C5) scores more than they raise Spec-condition scores`.
5. **Line 1731 (§4.6.7 Verbose responses).** `the correlation is concentrated almost entirely in C5 (responses with no provided context; r = 0.60) … Three behaviors drive the C5 pattern` → `the correlation is concentrated almost entirely in the No-Context Baseline (C5; responses with no provided context; r = 0.60) … Three behaviors drive the No-Context Baseline (C5) pattern`.
6. **Line 1757 (§4.6.7 What this establishes).** `Both effects raise C5 baseline scores more than they raise Spec-condition scores` → `Both effects raise the No-Context Baseline (C5) scores more than they raise Spec-condition scores`.
7. **Line 1791 (§4.7 summary bullet).** `length-score correlation in C5); both bias the C5 baseline upward` → `length-score correlation in the No-Context Baseline (C5)); both bias the No-Context Baseline (C5) upward`.

## Edits deliberately NOT applied (deferred decisions)

- **§3.2 lookup tables (lines 314-360) and Appendix C.1 (lines 2414-2426).** Definitional lookup tables. Bare codes are appropriate because the natural label appears in the adjacent column. Title-Casing these tables is a paper-architecture decision; flagged as a one-shot follow-up if Aarik wants it.
- **§1.4 lookup table (lines 82-92).** Already uses bold sentence-case labels with the code in parens. Elevating to Title Case ("**The No-Context Baseline** (C5)") would be the consistency-pass extension; deliberately not done because this table is the introductory definition and the existing form is clear.
- **All worked-example blockquote headers** (e.g., "**C2a (Spec only):**", "**C4 facts only (mean 1.00):**", "**C1 (Supermemory retrieval alone), mean 2.00:**"). These already carry the natural-language label inline. Title Case would over-decorate. Left as-is.
- **All math / statistical expressions:** `Δ_C4a`, `Δ_C4a ~ C5`, `C5 ≤ 2.0`, `C5 vs. C4a`, `C2a vs. C4 / C8`, `mean(C3) − mean(C1)`. Inserting natural labels into these expressions would produce clunky math prose ("Δ_C4a on the No-Context Baseline (C5)"). The advisor explicitly flagged this as a "do not pursue" pivot signal.
- **Code/script paths** (`results/global_<subject>/c8_c9_results.json`, `_letta_rerun/`, etc.). File references; bare codes are correct.
- **Listing of identifier ranges** (e.g., line 411: "Condition identifiers (C5, C2a, C4a, C3) refer to the conditions defined in §3.2"; line 1965: "11 conditions (C1 through C9 plus two wrong-Spec variants)"). These read as ID enumerations, not body-prose descriptions of a specific condition.
- **§4.1 Table 4.1 and similar tables** with column headers like `C5 baseline | C4 facts | C2a Spec | C4a facts+Spec`. The natural label is in the column header; row cells stay bare.
- **§4.4.3 anchor-example blockquotes** (Pattern 1 / 2 / 3). Each blockquote header bolds the C1/C3 codes alongside `(Supermemory retrieval alone)` / `(Supermemory + Behavioral Specification)`. Already paired.
- **Footnote-internal stats** like `[^wilcoxon]: C5 vs. C2a *W* = 10`. Math comparisons; bare is correct.
- **§3.6 prompt pseudocode block** (lines 690-692): code block, leave bare.

## Counts (after)

- Bare-code mentions in body prose elevated to natural label: **7 edits**
- Bare-code mentions in tables / math / code paths / definitional rows / blockquote headers: ~272, deliberately untouched
- Total mention count: 279 → 279 (no new codes introduced; 7 codes now paired with a Title-Case natural-language label that did not exist on the same line before)

## Open follow-up if Aarik wants further consistency

If Aarik wants the §3.2 first-introduction table at lines 82-92 lifted to Title Case (e.g., "**The No-Context Baseline** (C5)"), it is a 10-line edit with no downstream impact. Same applies to §3.2 second table (lines 318-328), Appendix C.1 (lines 2414-2426), and Appendix D.1 column headers. These were left alone because they are definitional lookups, not paragraphs of body prose, and elevating them is an architecture-style choice not strictly required by the consistency rule in body prose.
