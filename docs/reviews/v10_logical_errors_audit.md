# v10 Logical-Errors Audit

**Reviewer:** opus 4.7 review agent
**Source file:** `docs/beyond_recall_v10_draft.md` (2,379 lines)
**Date:** 2026-04-23
**Scope:** logical errors only (contradictions, broken inferences, orphaned premises, scope overreach, framing inconsistencies, sensitivity-analysis logic, numerical cross-checks). Not prose polish.

---

## Executive Summary

**Overall verdict.** The paper holds up logically on its headline claims and on the new §4.1 sensitivity block. The gradient slope, the wrong-spec controls, the compression result, and the Wilcoxon / regression statistics are internally consistent and correctly inferred from the underlying data. The §4.1.2 author-pilot removal and the §1.5 / §5.7 alignment-section folds did not leave behind orphaned premises that break the core argument.

What the audit did surface is a cluster of **MAJOR navigation/labeling defects** introduced by the structural moves: the §4 roadmap and the §5 roadmap both promise sections the paper no longer contains. There are two **CRITICAL** stale-number cells in §3.7.3 that contradict the §4.1 gradient table for Hamerton and Ebers. There are several MAJOR numerical inconsistencies (compression range, question count for §4.5 subjects, mean C5 reported as 1.52 vs 1.55 computable). One **MAJOR** orphan: a `Pattern 4` reference appears in §4.4 with no Pattern 4 defined.

| Severity | Count |
|---|---:|
| CRITICAL | 3 |
| MAJOR | 8 |
| MINOR | 6 |

CRITICAL findings break a headline claim or contradict primary data the reader will check against. MAJOR findings actively mislead a reader. MINOR findings are inconsistencies that should be cleaned up.

The CRITICAL items can all be fixed by editing single paragraphs; none requires a re-run or re-analysis.

---

## CRITICAL Findings

### C1. §3.7.3 Hamerton example uses stale 1.41 / 2.97 numbers

**Location:** §3.7.3 line 532.
**Type:** Class 1 (within-paper contradiction) and Class 8 (numerical claims vs primary data).
**Current claim:** "Hamerton C5 (baseline) at **1.41** → C4a (facts + spec) at **2.97**: crosses the 2 / 3 anchor."
**Problem:** §4.1 main gradient table (line 717) and Appendix D.1 (line 2050) and Appendix D.4 per-judge matrix (line 2174) all give Hamerton 5-judge primary C5 = **1.26** and C4a = **2.77**. The 1.41 / 2.97 numbers do not appear in the 5-judge primary aggregate anywhere in the rest of the paper. They look like values from an earlier 6-judge or 7-judge aggregate that was the headline before the §3.7.2 primary-aggregate lock.

**Why it matters.** §3.7.3 is the canonical worked example of the cross-anchor interpretation rule. A reader who consults the gradient table to verify the example will find different numbers for the same condition cell, which undermines confidence in every cross-section comparison that follows. This is the kind of inconsistency a careful reviewer flags within minutes.

**Suggested fix language.** Replace "Hamerton C5 (baseline) at 1.41 → C4a (facts + spec) at 2.97" with "Hamerton C5 (baseline) at 1.26 → C4a (facts + spec) at 2.77". The "crosses the 2 / 3 anchor" claim is preserved by the corrected numbers (1.26 sits in band 1, 2.77 sits in band 2 only because 2.77 < 3; this actually crosses 1/2 not 2/3). Recheck the anchor claim or pick a different example whose corrected numbers do cross 2/3 cleanly. Hamerton C4a at 2.77 is still close to anchor 3 but does not cross it; "crosses the 2 / 3 anchor" should be "approaches the 2 / 3 anchor" or be replaced with a different example. Sunity Devee C5 = 1.03 → C4a = 2.41 actually crosses 1/2; Bernal Diaz C5 = 1.70 → C4a = 2.48 stays in band 2.

### C2. §3.7.3 Ebers example uses stale 1.04 / 2.47 numbers

**Location:** §3.7.3 line 531.
**Type:** Class 1 (within-paper contradiction) and Class 8 (numerical claims vs primary data).
**Current claim:** "Ebers C5 (baseline, no context) at **1.04** → C2a (spec only) at **2.47**: crosses the 1 / 2 anchor."
**Problem:** §4.1 gradient table (line 715) gives Ebers 5-judge primary C5 = **1.02** and C2a = **1.54**. Appendix D.4 line 2185 confirms 1.02 / 1.54 (Ebers 5-judge primary). The claimed C2a = 2.47 does not appear in any Ebers row anywhere in the paper. The 7-judge aggregate for Ebers C2a is 1.79 (line 2185), not 2.47. The 2.47 figure does not match Ebers under any condition or judge panel.

**Why it matters.** Same reason as C1. The §3.7.3 example is the load-bearing illustration of how to read fractional deltas. A reader who consults Appendix D for Ebers will not find these numbers and will lose confidence in the rubric explanation. Worse, the corrected delta (1.02 → 1.54, ΔC2a = +0.52) is too small to cross the 1/2 anchor, so the "crosses the 1 / 2 anchor (refusal → engagement)" interpretation cannot survive the correction.

**Suggested fix language.** Either (a) update to Sunity Devee C5 = 1.03 → C2a = 2.27 (crosses 1/2 cleanly) or Hamerton C5 = 1.26 → C2a = 2.63 (also crosses 1/2 cleanly), or (b) update to Ebers C5 = 1.02 → C4a = 2.07 (also crosses 1/2). The narrative ("refusal responses turn into actual engagement") still works on any of these. The specific 1.04/2.47 pair must be replaced.

### C3. §4 roadmap promises eight parts; §4 has six. §4.6 label mismatched.

**Location:** §4 introduction line 585-592.
**Type:** Class 3 (orphaned premise after structural change) and Class 1 (within-paper contradiction).
**Current claim:** "This section reports the Behavioral Specification's effect on behavioral prediction across **eight parts**." The list that follows enumerates only six (§4.1 through §4.6). The §4.6 entry reads "**§4.6. Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level?" The actual §4.6 header (line 1343) is "**Robustness and Sensitivity**".

**Problem.** Two structural defects in one paragraph. (1) The "eight parts" count is left over from a prior §4 organization that included the now-removed §4.5 author-pilot block plus an earlier sub-organization. (2) The §4.6 label and description match what is now embedded in §4.4.2 / §4.4.3 (Common Mechanisms, Keckley Q21 cross-system refusal), not what §4.6 is in the current draft. A reader who skims the roadmap will arrive at §4.6 expecting a per-question interpretation-vs-recall analysis and instead find a robustness section.

**Why it matters.** This is a navigation contract the introduction makes with the reader. Failing it on the very first paragraph of §4 erodes confidence in everything downstream. Any reviewer reading top-to-bottom flags this immediately.

**Suggested fix language.**

```
This section reports the Behavioral Specification's effect on behavioral
prediction across six parts:

- §4.1. The Cross-Subject Gradient. The primary result, across 14 subjects.
- §4.2. Compression: Structure vs. Raw Text. Is the effect about structure
  or about information volume?
- §4.3. Mechanism: Content, Not Format. Does the content of the correct
  specification drive the effect, or does any structured prompt?
- §4.4. Memory-System Composition. Does the specification layer on top of
  existing commercial memory systems, and where does it help or hurt at
  the per-question level (§4.4.2, §4.4.3)?
- §4.5. Exploratory case study. A post-hoc N=3 comparison of Letta's
  stateful-agent path against the Base Layer specification. Not a
  headline finding.
- §4.6. Robustness and Sensitivity. Cross-provider response generation,
  judge-panel sensitivity, and what these checks do not address.
```

This also folds the per-question-mixture analysis into the §4.4 entry where it now lives, removing the orphaned label.

---

## MAJOR Findings

### M1. §5 roadmap labels do not match §5 headers

**Location:** §5 introduction line 1446.
**Type:** Class 3 (orphaned premise after structural change).
**Current claim:** "The remaining subsections of §5 develop what these results imply for how AI memory systems should be evaluated (§5.2), for real users who sit outside the sample this study could run (§5.3), for the mechanism of interpretation itself (§5.4), for the specification target as a general AI-design primitive rather than a Base Layer-specific claim (§5.5), and for the measurement gaps the study does not close (§5.6)."

**Problem.** The actual §5 headers are:
- §5.1 The Anti-Pattern: What Behavioral Specification Is Not
- §5.2 What the study demonstrates
- §5.3 The population of relevance
- §5.4 Content specificity and mechanism
- §5.5 Practical Implications
- §5.6 What the study does not settle

The roadmap describes §5.5 as "the specification target as a general AI-design primitive" but actual §5.5 is practical-deployment scoped (context budgets, dynamic activation, modifiability). The roadmap describes §5.2 as "how AI memory systems should be evaluated" but §5.2 is "What the study demonstrates" (a summary of findings). §5.1 is not mentioned in the roadmap at all.

**Suggested fix language.** Rewrite the roadmap sentence to match the current headers, and add §5.1 to the list:

> §5.1 first names the anti-pattern (what Behavioral Specification is not). §5.2 summarizes what the study demonstrates. §5.3 develops the population of relevance for real users. §5.4 unpacks the content-specificity mechanism and the three-pattern reading. §5.5 turns to practical implications under static-full-spec serving and flags the production-deployment gaps. §5.6 catalogues what the study does not settle.

### M2. Compression range "30× to 78×" in §5.5 contradicts study sample

**Location:** §5.5 line 1566.
**Type:** Class 1 (within-paper contradiction) and Class 8 (numerical claim vs primary data).
**Current claim:** "§4.2 documents the **30× to 78×** compression the specification achieves at modest cost to predictive signal."
**Problem.** §4.2 Table at line 779 reports per-subject compression ratios from **~5×** (Hamerton) to **~78×** (Babur). The mean is ~23×. No subject sits at "30×" anywhere in the table. The lower bound "30×" is unsupported.

§5.2 line 1442 already states the correct range: "compression ratios ranging from roughly **5× (Hamerton, ~33K-token corpus) to 78× (Babur, ~550K-token corpus)**". §1.3 line 98 says "roughly 5% of the context" (= ~20× compression).

**Suggested fix language.** Replace "30× to 78× compression" with "5× to 78× compression" or "~23× mean compression" to match the §4.2 table and §5.2's own statement.

### M3. §4.5 claims "40-question battery per subject" for Hamerton, Ebers, Babur

**Location:** §4.5 line 1261.
**Type:** Class 1 (within-paper contradiction).
**Current claim:** "N=3 subjects (Hamerton, Ebers, Babur), one Letta version, one response model (Claude Haiku), **a 40-question battery per subject**."
**Problem.** §3.4 (line 347) and Appendix B.2 (lines 1853-1872) both establish that every main-study subject (including Hamerton, Ebers, Babur) has **39** behavioral-prediction questions. Appendix B.2 column total is 39 for all three of these subjects (lines 1858, 1861, 1870). Only Franklin has 40, and Franklin is not in §4.5.

The Hamerton legacy battery file does contain 80 questions in total, but only 39 of those are tagged as behavioral prediction. The §4.4.2 Letta archival paired-row for Hamerton (line 1192) lists "Total Qs = 39", confirming that the rest of the paper treats Hamerton as 39-BP.

**Needs author verification.** If §4.5 actually used the full 80-question Hamerton legacy battery (and the equivalent for Ebers, Babur), the table comparison to "Base Layer compressed-brief" should specify which question slice was scored. If §4.5 used 39-BP per subject, the line should read "39-question battery per subject".

**Suggested fix language.** Replace "a 40-question battery per subject" with "the main-study 39-BP battery per subject" — or, if a different slice was used, name it explicitly.

### M4. "Pattern 4" reference in §4.4 is undefined

**Location:** §4.4 line 1158 (also recurs as Example 4 the reframe in §4.4 example block at line 1133).
**Type:** Class 3 (orphaned premise) / Class 4 (undefined term).
**Current claim:** "Pattern 1 and **Pattern 4** (Example 4's reframe) drive the 37 spec-helps questions with mean swing +1.45."
**Problem.** §4.4 ("Three mechanisms generate the swings") and §4.4.2 ("The three mechanisms from §4.4 reproduce") and §5.4 ("The three mechanisms (Pattern 1, Pattern 2, Pattern 3) are not alternatives") all formally enumerate exactly three patterns. There is no Pattern 4 in the canonical list. Example 4 (Fukuzawa Q16, the reframe case) is described in the §4.4 paragraph block but is never promoted to its own pattern in the formal mechanism list.

**Why it matters.** A reader who tries to trace Pattern 4 back to its definition will not find one. The mechanism story is the load-bearing causal explanation in §4.4 and §5.4, so "Pattern 4" introduced casually here weakens the otherwise tight three-pattern framing.

**Suggested fix language.** Either (a) drop "and Pattern 4" and rephrase as "Pattern 1 (and the reframe variant illustrated by Example 4) drive the 37 spec-helps questions...", or (b) formally promote the reframe case to Pattern 4 in the §4.4 mechanism list and §5.4 carries through. Option (a) is cleaner and preserves the three-pattern symmetry.

### M5. Mean C5 reported as 1.52 disagrees with §4.1 table by +0.03

**Location:** §4.2 line 765, line 788 (table summary row), line 844; §4.1 line 696.
**Type:** Class 1 (numerical inconsistency between body and table) and Class 8 (numerical claim vs primary data).
**Current claim.** §4.2 says "mean C5 = **1.52**" (and C4a = 2.45, C2a = 2.23). §4.1 gradient table (line 715-723) reports per-subject C5 values that aggregate to 13.93 / 9 = **1.548** (rounds to 1.55). Per-subject C4a values aggregate to 21.95 / 9 = **2.439** (matches 2.44). C2a aggregates to 20.10 / 9 = 2.233 (matches 2.23).

**Why it matters.** The discrepancy is small but the C5 figure is the load-bearing baseline that the +0.89 mean lift and the spec-effect gap are computed against. Either the per-subject table values are rounded down from a higher-precision underlying mean (in which case the body claim is right and the table is rounded), or the body claim is computed wrong. Either way, the source of the 0.03-point gap should be reconciled.

**Needs author verification.** Likely cause: the §4.2 row aggregates a higher-precision per-judge × per-question mean before averaging across subjects, while the §4.1 table per-subject means are rounded to two decimal places before the inter-subject mean. If so, the §4.1 table needs a footnote explaining that "Slice means in §4.2 are computed from full-precision per-question scores, not from the per-subject means in this table."

**Suggested fix language (footnote on §4.1 table or §4.2 mean row):** "Slice-level means are computed from per-question 5-judge primary scores at full precision; the per-subject means in §4.1 Table 4.1 are rounded to two decimals, so simple averages of the table values may differ from the slice means by ≤0.03 points."

### M6. §4.5 referential-density caveat partially undermines headline conclusion

**Location:** §4.5 lines 1315-1321 ("Content comparison: what each representation retains") and 1334 (caveats footnote: "the gap widens at the two smaller corpora and narrows at Babur, consistent with a Pattern 2 (over-theorization) effect on small corpora").
**Type:** Class 5 (scope overreach by understatement) and Class 7 (sensitivity-analysis logic).
**Current claim.** §4.5 reports Letta-over-Base-Layer Δ = +0.14 / +1.05 / +0.54, then in caveats reports a full-stack rerun gives Δ = +0.27 / +1.21 / +0.38. The caveat says "Direction is invariant across both Base Layer spec forms."
**Problem.** "Direction is invariant" is technically true (all six values are positive), but the magnitude shift on Babur (+0.54 → +0.38, a 30% reduction) and the *increase* at Hamerton (+0.14 → +0.27, a near-doubling) suggests the comparison is sensitive to which Base Layer artifact is served, not just to the representation production mechanism. The body language ("Letta's stateful-path block produces a higher per-subject mean score than the unified brief") understates how much the spec form affects the gap. The reader is told to read this as evidence that both representations land in a similar prediction band, but the caveat shows the gap depends on the Base Layer side's spec form.

**Why it matters.** §4.5 is already labeled exploratory, and §7.5 promises a layered-stack rerun. The body of §4.5 should match the caveat's hedge. As currently written, a casual reader walks away with "Letta wins by +0.14 / +1.05 / +0.54" and only a careful reader notes the caveat changing the range to +0.27 / +1.21 / +0.38.

**Suggested fix language.** Move the bullet about the layered-stack rerun (caveats line 1334) up to the result block and replace "On all three subjects tested, Letta's stateful-path block ... produces a higher per-subject mean score than the unified brief" with: "On all three subjects tested, Letta's stateful-path block produces a higher per-subject mean score than the Base Layer compressed-brief variant; a rerun against Base Layer's full layered-stack variant produces a similar direction with shifted magnitudes (+0.27 / +1.21 / +0.38 on Hamerton / Ebers / Babur). The Babur gap shrinks substantially under the layered-stack comparison; the Hamerton gap widens. Magnitudes are spec-form-dependent."

### M7. §4.1 sensitivity block "8% attenuation" understates if read as "negligible"

**Location:** §4.1 line 743-747 (battery-composition sensitivity).
**Type:** Class 7 (logic of sensitivity analyses).
**Current claim.** "A multiple regression of Δ_C4a on both C5 baseline and LITERAL_RECALL fraction across the 14 main-study subjects yields a partial coefficient on baseline of −0.88 [95% CI −1.13, −0.63], p < 10⁻⁵, **attenuated from the univariate −0.96 by about 8%**. ... **The gradient on baseline survives; it is not an artifact of battery composition.**"
**Problem.** The conclusion does logically follow on direction (the partial coefficient remains significantly negative, p < 10⁻⁵). But the sensitivity report itself (`docs/research/v10_battery_sensitivity_analysis.md` §3) acknowledges that LITERAL_fraction is **also significant as a partial predictor (β = +2.30, p = 0.026)**, and the 6.9% unique-variance contribution is non-trivial relative to the 14-subject sample. The body skips this counterweight: it states the gradient survives (true) without acknowledging that battery composition is itself a real predictor that the cross-subject sample under-controls for.

**Why it matters.** §5.3 and §5.6 lean on the gradient slope to make the deployment-relevance argument for low-baseline real users. If LITERAL_fraction is partly driving the gradient, the deployment extrapolation is partially confounded with battery-composition heterogeneity, not purely with pretraining coverage. The paper acknowledges this confound elsewhere (Appendix B.6 line 1932-1933, §5.3 implicitly), but §4.1's "the gradient survives" language reads as a stronger conclusion than the data supports.

**Suggested fix language.** After "the gradient on baseline survives; it is not an artifact of battery composition," append: "though LITERAL_RECALL fraction is itself a significant partial predictor (β = +2.30, p = 0.026; uniquely explains 6.9% of variance), so the cross-subject gradient is partly compounded with between-subject differences in question-type composition. A category-balanced battery would let the two effects be separated cleanly; flagged as the priority gradient-design follow-up in §7."

### M8. "Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate" claim is partly aspirational

**Location:** §4.6.2 line 1390.
**Type:** Class 5 (scope overreach).
**Current claim.** "Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`)."
**Problem.** The 7-judge per-subject sensitivity check is only directly tabulated for a subset of conditions (the §4.6.2 table covers C2a, C2c v2, C2c v1 on the 13 globals). The paper does not report 7-judge aggregates for §4.4.1 memory-system Δ_spec values, the §4.4.2 per-subject paired distributions, or the §4.4.3 Keckley Q21 cross-system table. The Appendix D.4 per-judge matrix has Gemini Pro "n/a" cells for many subject × condition pairs, so the 7-judge aggregate cannot have been computed for those cells.

**Why it matters.** The "every primary finding ... was checked" framing implies more coverage than the paper actually shows. A careful reviewer following the citation will find the analysis plan lock document but no §4.4 7-judge table.

**Suggested fix language.** Soften to: "The §4.1 gradient and the §4.3 wrong-spec Δ values were checked against the 7-judge aggregate in §4.6.2; the §4.4 memory-system per-system Δ values and the §4.4.3 Keckley Q21 table were not separately re-aggregated to 7-judge because the Gemini judges have incomplete coverage on memory-system conditions (see Appendix D.4 for n/a cells). The 5-judge primary directions in §4.4 are stable across judge subset; the 7-judge sensitivity is limited to the conditions where Gemini coverage is complete."

---

## MINOR Findings

### N1. §1.3 token-budget parenthetical is internally redundant

**Location:** §1.3 line 96.
**Current claim.** "A compact specification of roughly **5,000-8,000 tokens** (the full served artifact is **~8,000-10,000 tokens** including the composed brief)..."
**Problem.** §3.3 line 313 is unambiguous: the served artifact is the three layers concatenated with the brief, total ~5,000-8,000 tokens, ~3,500-6,000 words. The §1.3 parenthetical introduces a second figure (8,000-10,000 tokens) without saying which one is the served artifact. Two different intros to the same artifact size is mildly confusing.
**Suggested fix.** Pick one range and keep §3.3 and §1.3 aligned. Probably ~8,000-10,000 tokens is the served-artifact range and ~5,000-8,000 is the layers-only range; if so, that distinction should be made once, in §3.3, and §1.3 should cite the served-artifact range.

### N2. Conditions table in §1.2 lists 11 conditions; §3.5 lists 7 direct + memory-system; §C.1 reconciles

**Location:** §1.2 conditions table line 50-62; §3.5 direct-context conditions line 376-385 plus memory-system conditions line 391-396; §C.1 line 1944-1956.
**Current claim.** The §1.2 introductory table includes "C8 raw corpus + C9 corpus+spec" as primary conditions. §3.5 also includes C8 and C9. But §6.4 line 1663 says "11 conditions (C1 through C9 plus two wrong-spec variants)". The arithmetic only works if C2c v1 and C2c v2 are counted as two separate conditions; otherwise, C1 through C9 is at most 9 condition labels (and several of them like C6/C7 are not present in the paper). Specifically, C6 and C7 do not appear anywhere; the labels jump from C5 to C8.
**Problem.** "C1 through C9" implies a continuous integer sequence; the actual study uses C1, C2a, C2c, C3, C4, C4a, C5, C8, C9 with two C2c variants. The label scheme is non-contiguous, which is fine, but "C1 through C9" undersells the number of conditions and could confuse a reviewer counting along.
**Suggested fix.** Replace "C1 through C9" with "the nine condition labels C1, C2a, C2c, C3, C4, C4a, C5, C8, C9, plus the two C2c derangement variants".

### N3. §1.3 5-of-6 cells claim phrasing inconsistent with §4.6.1 result

**Location:** §1.3 line 123 vs §4.6.1 line 1355.
**Current claim.** §1.3: "all 6 (subject × response model) cells follow the expected pattern when Sonnet or Gemini Pro reads questions generated by GPT-5.4. Five reproduce the specification direction directly, and the sixth (Zitkala-Sa × Gemini Pro) aligns with the gradient mechanism." §4.6.1: "Result. **5 of 6 cells reproduce the specification direction.**"
**Problem.** Both claims are defensible (the 6th cell aligns with H2 rather than reproduces H1), but the framing differs slightly: §1.3 says "all 6 follow the expected pattern" while §4.6.1 says "5 of 6 reproduce." A reviewer reading §1.3 then §4.6.1 will need a second to reconcile that "expected pattern" in §1.3 includes "the gradient mechanism predicts a null at Zitkala-Sa baseline."
**Suggested fix.** §1.3 phrasing could be tightened to: "5 of 6 cells reproduce the specification direction directly, and the 6th (Zitkala-Sa × Gemini Pro) reproduces the null direction the gradient predicts at her baseline (§4.1 mid-baseline slice)."

### N4. §3.7 line 438 says "14 subjects × 40 questions" but main study is 39 BP

**Location:** §3.7 line 438.
**Current claim.** "Human annotation at this scale is feasible: roughly 14 subjects × 40 questions × 15+ conditions sits on the order of thousands of judgments."
**Problem.** Actual count is 39 main-study BP per subject (Franklin's 40 not in main study). "Roughly" softens the claim, but the figure is off by ~3.5%.
**Suggested fix.** Replace "40 questions" with "39 questions" or "~40 questions" and the back-of-envelope thousands-of-judgments still works.

### N5. §5.2 efficiency framing "fact extraction itself is already a compression pass"

**Location:** §5.2 line 1442.
**Current claim.** "The full extracted-fact set (C4, every fact loaded as context without the specification) produces a similar improvement on the low-baseline slice at a comparable footprint, so fact extraction itself is already a compression pass. The specification's marginal contribution over facts-only is smaller at the aggregate mean than the spec-versus-no-context gap suggests, and its distinct value shows up at the per-question level (§4.3, §4.6)."
**Problem.** The cross-reference "(§4.3, §4.6)" directs the reader to §4.3 (correct, mechanism) and §4.6 (wrong: §4.6 is robustness, not per-question analysis). The per-question analysis is now in §4.4.2 / §4.4.3 / §1.3 (Where the spec helps and where it hurts). Likely a stale §4.5/§4.6 cross-ref.
**Suggested fix.** Replace "(§4.3, §4.6)" with "(§4.3, §4.4.2)".

### N6. §3.7 description of post-hoc rubric audit cross-references §3.7.6

**Location:** §3.7 line 440.
**Current claim.** "Response models are evaluated by judges (§3.7.1). Judges are evaluated by calibration diagnostics (§3.7.2), inter-judge agreement metrics (§3.7.4), and post-hoc rubric-handling audits (§3.7.6)."
**Problem.** This is fine. §3.7.5 (aggregation) is omitted from the list, which is plausibly intentional, but readers tracking the recursive-evaluation argument may expect §3.7.5 to appear too.
**Suggested fix.** Optionally add "(§3.7.5 aggregation rule)" to the list to complete the recursion-of-instruments enumeration.

---

## What the Audit Did Not Find

The audit looked for and did not find the following potential issues:

- **Stale §4.1.2 author-pilot references.** No "author pilot", "N=1", "single-subject living", or "self-experiment" language remains. The §4.1.2 removal is clean. The "structural extrapolation argument" in §1.4 and §5.3 is consistent throughout.
- **Stale §1.5 / §5.7 Behavioral-Alignment references.** No capital-B "Behavioral Alignment" framing remains. The §7.6 fold uses lowercase "behavioral alignment" as a descriptive contrast in the safety-alignment discussion, which reads as appropriate.
- **§4.5 exploratory framing vs body confidence.** The header is labeled "exploratory case study (N=3, post-hoc)", the body uses appropriately hedged language ("does not establish", "is consistent with", "characterize" not "prove"), and §1.3 line 125 carries the same "post-hoc N=3 exploration" framing into the executive summary. The framing discipline holds.
- **Wilcoxon and Spearman statistics consistency.** §4.1 reports W = 11, p = 0.007 (C5 vs C4a) and W = 10, p = 0.005 (C5 vs C2a). These are internally consistent across §4.1, §1.3 (which cites W = 11, p = 0.007 for C4a), and §4.4.1 (which reports separate per-system Wilcoxons). Spearman ρ = 0.86 to 0.93 is consistent across §1.2, §1.3, §3.7.4, §4.1.
- **Headline regression statistics.** Slope −0.96, R² = 0.82, p < 0.001 reproduce in the §4.1 table, the §5.2 summary, and the v10 battery-sensitivity analysis at three decimal places.
- **"12 of 14 subjects improve" arithmetic.** Δ_C4a from §4.1 table: 9 low-baseline all positive, 3 of 5 mid-baseline positive (Cellini, Rousseau, Augustine) → 12/14. Confirmed.
- **Low-baseline mean Δ_C4a = +0.89.** Sum of low-baseline Δ_C4a = 8.01 / 9 = 0.890. Confirmed.
- **587 wrong-spec responses, 60.6% explicit-detection, 36.5% mismatch-application, 2.0% implicit hedge, 0.9% ambiguous.** These four percentages sum to 100.0% ± 0.0%. Internally consistent.
- **Compression efficiency claim "spec lift +0.71, corpus lift +0.93".** Computed from §4.2 means: C2a − C5 = 2.23 − 1.52 = 0.71, C8 − C5 = 2.45 − 1.52 = 0.93. Three-quarters of corpus lift = 0.93 × 0.75 = 0.6975 ≈ 0.71. The "roughly three-quarters" claim is logically consistent.

---

## Recommended Fix Order

The CRITICAL findings (C1, C2, C3) are surface-level edits that can be done in 30 minutes and substantially improve reader trust. M1, M2, M4 are similar — pure language fixes. M5 is the only finding that may require the author to consult the underlying analysis script to determine whether the 0.03-point discrepancy is a precision-rounding artifact or a real disagreement; if the former, a single-sentence footnote on §4.1 Table 4.1 closes it. M3 requires reading the §4.5 results file to confirm whether 39 or 40 questions were scored. M6, M7, M8 are language-tightening fixes that would take ~10 minutes each.

All MINOR findings can be batched into a final pre-launch sweep without changing the paper's structure or claims.
