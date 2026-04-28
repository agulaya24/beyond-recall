# Beyond Recall v11 -- Final Cursory Review

_Date: 2026-04-28 12:57_
_Paper: `docs/beyond_recall_v11_draft.md` (429,955 chars)_
_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_
_Scope: cursory error-check only -- glaring numerical/cross-ref/factual issues. Not a substantive review._

## Headline

- **OpenAI verdict:** BLOCKING-ISSUES-12 (12 issue headers)
- **Gemini verdict:** BLOCKING-ISSUES-12 (12 issue headers; retry with thinking-budget tuned)
- **Convergent issues (heuristic title match):** 1

## Convergent issues

Manual synthesis after re-reading both reports. Heuristic title-token match found 1; substantive overlap is 5.

1. **Broken anchor `#37-evaluation-llm-as-judge-with-calibration` in §3.2 baseline paragraph.** Both reviewers flagged. Anchor slug points at §3.7 but link text says §3.6; the heading is §3.6. Fix: replace with `#36-evaluation-llm-as-judge-with-calibration` or drop the anchor and use plain `§3.6`.
2. **Stale `v10_battery_sensitivity_analysis.md` / `_v10_battery_sensitivity.py` paths in §4.1 footnote.** Both reviewers flagged. Update to v11 artifact names or verify current canonical paths.
3. **Stale `_v10_verification/tier2_mechanical_recompute.py` path in §4.6.1.** Both reviewers flagged. Same fix pattern as above.
4. **Stale `v10_pipeline_variance_analysis.md` and `_v10_pipeline_variance*.py` paths in §6.3 / Appendix B.7 footnotes.** Both reviewers flagged. Same fix pattern.
5. **Multi-anchor jump percentage inconsistency in §1.3 vs §4.1.** GPT flagged "5-10% wins" prose violating the no-wins rule and being numerically off; Gemini independently flagged the 5-10% (§4.1) vs 18% (§1.3) contradiction. Fix: pick one canonical framing and propagate. Both reviewers' diagnoses point at the same prose passage.

Issues unique to one reviewer (not duplicated above):

GPT-only:
- §1.3 footnote `§1.4, §3.2.1` should be `§1.4, §5.3` (population-of-importance).
- §4.1 numerical contradiction: mean C4a stated as 2.41 in one sentence and 2.46 in another within §4.1.
- §4.2.1 "All 14 subjects (546 questions)" -- 14 x 39 = 546 implies subject count or per-subject question count is misstated.
- §4.1 "§1.3's Keckley Q21 example" should point at §4.4.3.
- Em-dash style violation (e.g., `Pattern 1 — Interpretation-heavy questions`).
- "wins" terminology in §1.3 and §4.1 prose despite explicit author rule.
- §4.1 introduces `H2a (corollary, introduced here)` without prior definition in §1.2 hypothesis enumeration.

Gemini-only:
- §4.1 "no question crossed from band 2, 3, or 4 into band 5" contradicted by Example C in same section (Seacole 2.80 -> 5.00).
- §4.6.4 cross-reference `(see §4.5)` for Gemini inflation discussion -- §4.5 is the Letta case study; Gemini inflation lives in §3.6.3.
- §5.4 Keckley Q21 numbers (Supermemory 3.83, Base Layer 3.33, -2.33 penalty) inconsistent with §4.4.3 numbers (~3.4-3.6, -2.0 to -2.2 penalty).
- §5.5 spec size "~8,000-10,000 tokens" inconsistent with §3.7 "approximately 5,000-8,000 tokens."
- §8 audit script name `scripts/audit_rubric.py` inconsistent with §3.6.6 `scripts/audit_low_end_inflation.py`.
- §5.2 compression ratios "roughly 5x (Hamerton)... 78x (Babur)" inconsistent with §4.2 table values (7x, 79x).

---

## Reviewer 1 -- OpenAI (gpt-5.4-2026-03-05)

## Issue: Cross-reference points to wrong section for low-baseline note
- **Section:** §1.3, footnote [^low-baseline]
- **Verbatim quote:** `"Low baseline" means C5 ≤ 2.0 on the 1-5 rubric. This is the population of importance for AI personalization (§1.4, §3.2.1): on a frontier model serving general AI users, almost everyone falls in or below this band, even people with substantial public output.`
- **Issue:** §3.2.1 defines the low-baseline slice, but the “population of importance for AI personalization” argument is developed in §5.3, not §3.2.1. Pointer is misleading.
- **Recommended fix:** Replace `§1.4, §3.2.1` with `§1.4, §5.3`

## Issue: Broken internal anchor link to nonexistent §3.7 heading
- **Section:** §3.2, baseline paragraph
- **Verbatim quote:** `the rubric and aggregation rule are defined in [§3.6](#37-evaluation-llm-as-judge-with-calibration)`
- **Issue:** The anchor slug `#37-evaluation-llm-as-judge-with-calibration` corresponds to §3.7, but the heading is §3.6. This link will break in rendered markdown.
- **Recommended fix:** Replace with `[§3.6](#36-evaluation-llm-as-judge-with-calibration)`

## Issue: Numerical contradiction on low-baseline facts+spec mean
- **Section:** §1.3 vs §4.2
- **Verbatim quote:** `On the 9 low-baseline subjects, all 9 improved with facts + spec; mean Δ_C4a = +0.89 points`
- **Verbatim quote:** `| C4a | facts + spec | 2.45 | +0.93 |`
- **Issue:** With baseline mean C5 = 1.52 and C4a mean 2.45, Δ should be +0.93, not +0.89. Same conflict recurs later where +0.89 is treated as the low-baseline headline.
- **Recommended fix:** Verify canonical low-baseline Δ_C4a and make all instances consistent (`+0.89` or `+0.93`)

## Issue: Numerical contradiction on mean C4a level
- **Section:** §4.1
- **Verbatim quote:** `The Behavioral Specification produces an answer of roughly uniform quality (mean C4a = 2.41 across all 14 subjects)`
- **Verbatim quote:** `the spec produces a roughly constant C4a quality near 2.46 regardless of baseline`
- **Issue:** Same quantity is given as 2.41 and 2.46 within the same section. One is wrong unless they refer to different subject sets, which is not stated.
- **Recommended fix:** Verify number and use one value consistently; if different populations, label explicitly

## Issue: Subject count contradiction in full-question totals
- **Section:** §4.2.1
- **Verbatim quote:** `All 14 subjects (546 questions).`
- **Issue:** 14 subjects × 39 questions = 546 is impossible; 546 corresponds to 14 main-study subjects only if Hamerton has 39 and one subject count is off, or to 13 globals + Hamerton, but the label “All 14 subjects” is ambiguous against earlier 14-subject main study plus Franklin control framing. This needs verification because totals are load-bearing.
- **Recommended fix:** Verify total and replace heading with exact population, e.g. `All 14 main-study subjects (546 questions)` or correct the number

## Issue: Wrong section pointer to Keckley example
- **Section:** §4.1, Example C note
- **Verbatim quote:** `they sometimes penalize spec-induced honest abstentions where the specification appropriately declined to invent detail (§1.3's Keckley Q21 example).`
- **Issue:** Keckley Q21 is developed in §4.4.3, not §1.3. §1.3 mentions refusal patterns but not this example.
- **Recommended fix:** Replace `§1.3's Keckley Q21 example` with `§4.4.3's Keckley Q21 example`

## Issue: Stale v10 reference in main text
- **Section:** §4.1, battery-composition sensitivity footnote
- **Verbatim quote:** `[^battery-sensitivity-data]: Full analysis, per-subject data, and reproducibility script at `docs/research/v10_battery_sensitivity_analysis.md` and `scripts/_v10_battery_sensitivity.py`.`
- **Issue:** Explicit v10 artifact naming remains in freeze text where v11 references are expected.
- **Recommended fix:** Replace with v11 artifact names if updated, or remove version label from prose reference

## Issue: Stale v10 references in Tier 2 robustness section
- **Section:** §4.6.1 and footnote [^tier2-recompute]
- **Verbatim quote:** `Under a verification recompute (`scripts/_v10_verification/tier2_mechanical_recompute.py`)`
- **Verbatim quote:** `Mechanical recompute script at `scripts/_v10_verification/tier2_mechanical_recompute.py`. Per-cell panel-range computation at `scripts/_v10_verification/tier2_panel_ranges.py`.`
- **Issue:** Stale v10 paths embedded in v11 paper.
- **Recommended fix:** Update paths to v11 equivalents or remove versioned directory names from prose

## Issue: Stale v10 references in pipeline-variance appendix
- **Section:** Appendix B.7 / §6.3 footnotes
- **Verbatim quote:** `scripts/_v10_coupling_sensitivity.py`
- **Verbatim quote:** `docs/research/v10_pipeline_variance_analysis.md`, `scripts/_v10_pipeline_variance.py`, and `scripts/_v10_pipeline_variance_report.py`
- **Issue:** Multiple stale v10 references remain in the body/appendices.
- **Recommended fix:** Update to v11 artifact names or neutral paths

## Issue: Em dash usage violates stated style rule
- **Section:** multiple, first occurrence in §1.3
- **Verbatim quote:** `Pattern 1 — Interpretation-heavy questions.`
- **Issue:** Paper has a no-em-dash rule; em dashes appear repeatedly in headings and prose.
- **Recommended fix:** Replace all `—` with colon/comma/parentheses or plain hyphen as appropriate, e.g. `Pattern 1: Interpretation-heavy questions.`

## Issue: “wins” terminology appears in prose despite author rule
- **Section:** §1.3 and §4.1
- **Verbatim quote:** `low-frequency but high-magnitude wins the aggregate mean understates.`
- **Verbatim quote:** `These are the wins at the margin the aggregate mean understates.`
- **Issue:** Author explicitly barred “wins” terminology in paper prose.
- **Recommended fix:** Replace with `cases`, e.g. `low-frequency but high-magnitude cases the aggregate mean understates.` and `These are the cases at the margin the aggregate mean understates.`

## Issue: Undefined term appears as hypothesis without prior definition
- **Section:** §4.1 opening
- **Verbatim quote:** `H2a (corollary, introduced here). On high-baseline subjects, the specification does not add value and mildly interferes.`
- **Issue:** H2a is introduced ad hoc in Results but not defined in §1.2 where hypotheses are enumerated and mapped. This reads like an undefined new hypothesis.
- **Recommended fix:** Replace `H2a (corollary, introduced here).` with `Corollary to H2:` or remove the label `H2a`

BLOCKING-ISSUES-12

---

## Reviewer 2 -- Google (gemini-2.5-pro, retry; finish=STOP)

This cursory error-check has identified several glaring issues that should be addressed before release.

## Issue: Broken cross-reference link
- **Section:** 3.2 Subjects
- **Verbatim quote:** `The baseline score (C5, no-context prediction accuracy; the rubric and aggregation rule are defined in [§3.6](#37-evaluation-llm-as-judge-with-calibration)) is a direct empirical measurement...`
- **Issue:** The markdown link anchor `#37-evaluation...` is incorrect. The section is 3.6, not 3.7. This will result in a broken link in rendered documents.
- **Recommended fix:** Change `[§3.6](#37-evaluation-llm-as-judge-with-calibration)` to `[§3.6](#36-evaluation-llm-as-judge-with-calibration)`.

## Issue: Contradictory claim about multi-anchor jumps
- **Section:** 4.1 The cross-subject gradient
- **Verbatim quote:** `...and a small share (5-10%) made multi-anchor jumps (1→3, 1→4, 2→5).`
- **Issue:** This contradicts Section 1.3, which states: "Multi-anchor jumps of two or more bands (e.g., 1→3) appear in 18% of low-baseline questions on the spec conditions, with about 6% being extreme jumps of three or more bands (e.g., 1→4, 1→5)". The range "5-10%" is inconsistent with "18%".
- **Recommended fix:** Verify the correct percentage and update the text in §4.1 to match §1.3, or vice-versa.

## Issue: Contradictory claim about rubric band crossings
- **Section:** 4.1 The cross-subject gradient (in the "What is actually happening" paragraph)
- **Verbatim quote:** `The directional asymmetry is itself a finding: across the full 14-subject panel, no question crossed from band 2, 3, or 4 into band 5; the only band-5 endpoints reached came from band 1 (3 questions).`
- **Issue:** This is directly contradicted by Example C in the same section, which describes a Seacole question as a "2.80 → 5.00 jump, crossing three integer anchors upward". This is a jump from band 2 into band 5.
- **Recommended fix:** Remove or revise the claim about band crossings. The evidence presented in the same section refutes it.

## Issue: Stale v10 reference in footnote
- **Section:** 4.1 The cross-subject gradient
- **Verbatim quote:** `[^battery-sensitivity-data]: Full analysis, per-subject data, and reproducibility script at docs/research/v10_battery_sensitivity_analysis.md and scripts/_v10_battery_sensitivity.py.`
- **Issue:** The file paths reference `v10`, which is a stale version number for a v11 paper. This undermines reproducibility and suggests copy-pasting from an old draft.
- **Recommended fix:** Change `v10_battery_sensitivity_analysis.md` to `v11_battery_sensitivity_analysis.md` and `_v10_battery_sensitivity.py` to `_v11_battery_sensitivity.py` (or verify correct v11 filenames).

## Issue: Stale v10 reference in footnote
- **Section:** 4.6.1 Cross-provider response generation (Tier 2 replication)
- **Verbatim quote:** `[^tier2-recompute]: Recompute audit at docs/research/v11_panel_completeness_audit.csv. Mechanical recompute script at scripts/_v10_verification/tier2_mechanical_recompute.py.`
- **Issue:** The script path `_v10_verification` is a stale reference to v10.
- **Recommended fix:** Update the script path to the correct v11 version (e.g., `_v11_verification`).

## Issue: Broken cross-reference to Gemini inflation
- **Section:** 4.6.4 Franklin as the high-baseline reference
- **Verbatim quote:** `On the 7-judge aggregate with Gemini included the baseline is higher still (see §4.5).`
- **Issue:** Section 4.5 is the exploratory case study on the Letta stateful-agent. It does not mention Franklin or Gemini inflation. The correct discussion of Gemini inflation is in §3.6.3 and §4.6.2.
- **Recommended fix:** Change `(see §4.5)` to `(see §3.6.3)`.

## Issue: Numerical contradiction on Keckley Q21 case
- **Section:** 5.4 Content specificity and mechanism
- **Verbatim quote:** `Supermemory C1 = 3.83, Base Layer C1 = 3.33; both took an identical −2.33 penalty`
- **Issue:** This contradicts the numbers in §4.4.3, which states: "Supermemory and Base Layer's substrate, both at C1 ≈ 3.4-3.6 on the 1-5 rubric" and "producing the −2.0 to −2.2 penalty". The C1 scores and the penalty value are inconsistent between the two sections.
- **Recommended fix:** Verify the correct numbers for the Keckley Q21 case and ensure they are consistent in both §4.4.3 and §5.4.

## Issue: Numerical contradiction on specification size
- **Section:** 5.5 Practical implications
- **Verbatim quote:** `The full-stack Behavioral Specification is ~8,000-10,000 tokens...`
- **Issue:** This contradicts Section 3.7, which states: "Total size per subject is approximately 5,000-8,000 tokens...". The token count range is inconsistent.
- **Recommended fix:** Verify the correct token range and use it consistently in both sections.

## Issue: Stale v10 reference in footnote
- **Section:** 6.3 Pipeline and specification stability
- **Verbatim quote:** `[^variance-data-paths]: Per-rerun specs and judgments are at ... Full report and reproducibility scripts at docs/research/v10_pipeline_variance_analysis.md, scripts/_v10_pipeline_variance.py, and scripts/_v10_pipeline_variance_report.py.`
- **Issue:** The file paths reference `v10`, which is a stale version number.
- **Recommended fix:** Update all `v10` file paths to their correct v11 equivalents.

## Issue: Stale v10 reference in reproducibility section
- **Section:** 8. Data, code, and reproducibility
- **Verbatim quote:** `The §4.1 battery-composition sensitivity analysis is reproducible via scripts/_v10_battery_sensitivity.py.`
- **Issue:** The script path references `v10`, a stale version number.
- **Recommended fix:** Update the script path to the correct v11 version.

## Issue: Contradictory script name
- **Section:** 8. Data, code, and reproducibility
- **Verbatim quote:** `The §3.6.6 rubric-handling validity audit is reproducible via scripts/audit_rubric.py.`
- **Issue:** This contradicts Section 3.6.6, which states the audit was "produced by `scripts/audit_low_end_inflation.py`". The script names are different.
- **Recommended fix:** Verify the correct script name and use it consistently in both sections.

## Issue: Minor numerical inconsistency on compression ratios
- **Section:** 5.2 What the study demonstrates
- **Verbatim quote:** `...compression ratios ranging from roughly 5× (Hamerton, ~33K-token corpus) to 78× (Babur, ~550K-token corpus) by token count.`
- **Issue:** The table in §4.2 reports these ratios as 7x for Hamerton and 79x for Babur. While "roughly" allows some latitude, these are off by a non-trivial amount and should be consistent.
- **Recommended fix:** Verify numbers. Suggest changing the text to "roughly 7x" and "roughly 79x" to match the data table in §4.2.

---
BLOCKING-ISSUES-12
