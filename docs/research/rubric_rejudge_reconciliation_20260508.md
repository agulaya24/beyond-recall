# Rubric rejudge reconciliation: did existing instrumentation underweight a real gap?

**Date:** 2026-05-08
**Scope:** Reconcile the published-rubric rejudge finding (`docs/research/published_rubric_robustness_check_20260508.md`, ρ = 0.389 on 25 cells) against the paper's existing robustness instrumentation (§3.3.3, §3.3.4, §3.3.6, §4.6.1, §4.6.2, §4.6.7) and the same-day rubric-defensibility analysis (`docs/reviews/rubric_defensibility_analysis_20260508.md`).
**Headline question (Aarik's framing):** is this a knee-jerk-change-on-incomplete-information situation, or is it a genuine measurement gap that the existing instrumentation underweighted?
**Read-only analytical task.** No paper edits, no API calls, no claim about whether the rejudge result is correct.

## Verdict up front

**Mostly the second, partially the first.** Three of the rejudge's component findings were already in the paper at varying levels of explicitness; one is genuinely new and one directly contradicts a published direction-of-bias claim. The paper's existing instrumentation is well-designed for the questions it was scoped to ask, but it was *not* scoped to ask whether the published anchor table and the prompt-anchor wording produce equivalent score distributions on real responses. The defensibility analysis dated the same day flags exactly that exposure as the only open attack surviving every other defense; the rejudge is the empirical test of that exposure.

The numbers are concerning, but the existence and shape of the issue are not surprising in the context of what the paper team has already disclosed. What is new: a quantification (ρ = 0.39 cell-level), a second failure mode (genericity-over-scoring), an asymmetry by baseline band (severe deflation on the one high-baseline subject sampled), and an empirical contradiction of §3.3.6's published direction-of-bias claim.

The rest of this document walks through each existing check, identifies what it tested vs. did not, and lands on whether the rejudge finding extends, confirms, or contradicts what the paper already said.

---

## Part 1. What each existing robustness check tests vs. doesn't

### §3.3.3 Calibration on synthetic inputs
*Tests:* per-judge rubric application on four constructed inputs with known correct scores: verbatim ground truth, paraphrased ground truth, partial (first sentence only), and ground truth plus generic padding. Surfaces verbatim-match failure (Gemini Pro at 4.15), length sensitivity (Gemini Flash, Gemini Pro), and partial-content scoring. The diagnostic is judge-side, not subject-side.
*Does not test:* judge behavior on the response types that drive the rejudge's largest divergences. Specifically, polite-refusal-with-context responses ("I don't have specific information about Mrs. Davis but if you're referring to..." — Equiano q13, where five judges scored 4-5 under the prompt rubric and 1-2 under the paper rubric) and generic spec-driven responses that articulate a behavioral pattern without predicting the specific event in the held-out passage (Babur C4a q2). The four synthetic inputs were chosen to probe length, paraphrase, and partial-correctness — three of the most common LLM-judge pathologies in the literature — but not the refusal-vs-engagement boundary at score 1, and not the genericity-vs-specificity boundary at score 2-3. These are precisely the two boundaries the rejudge isolates as the source of the divergence. Calibration as currently scoped tests anchor 5 (verbatim match) and a length covariate; it does not test anchor 1 (refusal handling) or anchor 2-3 (genericity boundary).

### §3.3.4 Inter-judge agreement
*Tests:* pairwise Spearman ρ and Krippendorff α among judges *under a single rubric*. Reports ρ = 0.86 to 0.93 across the 5-judge primary panel and α = 0.659. Establishes that the panel converges on rank order and that absolute magnitude diverges by roughly +1 point on the Gemini judges.
*Does not test:* cross-rubric agreement. Both metrics are computed on the same rubric-prompt the judges were given. Whether the same judges, given the §3.3 published-table rubric verbatim, would produce scores that rank-correlate at 0.86 to 0.93 with their original prompt-rubric scores is a different empirical question the existing inter-judge agreement statistic cannot answer. The defensibility analysis flagged this distinction explicitly the same day: a judge can be highly self-consistent under one rubric and still produce score distributions that diverge from another rubric meant to operationalize the same construct. The rejudge's per-judge cross-rubric Pearson r (0.347 to 0.544) and Spearman ρ (0.234 to 0.480) are the missing measurement; they sit substantially below the within-rubric numbers reported in §3.3.4.

### §3.3.6 Post-hoc validity audit
*Tests:* per-condition refusal score distribution, length-correlation by condition, per-judge strictness, per-response-model abstention behavior, memory-system effect on abstention. The audit script (`scripts/audit_low_end_inflation.py`) is *structurally low-baseline-only* — its `LOW_BASELINE` constant enumerates nine subjects and does not iterate over the five mid-baseline globals or the Franklin reference. This was a defensible scoping choice at the time (the failure modes the audit was looking for were expected to concentrate in the low-baseline slice where score-1 frequency is highest), but it is a structural blind spot for any failure mode that concentrates at the *high-baseline* end.
*Does not test:* cross-rubric construct equivalence at scale, and never sees the five mid-baseline subjects or the Franklin reference. The audit's headline finding (9.4% of refusals scored ≥ 2.0, mean refusal score 1.27) is the same mechanism the rejudge identifies in spot-check (Equiano q13 polite refusal scored 4.40 under the prompt rubric, 1.20 under the paper rubric). The mechanism is not new; what *is* new is the magnitude tail. The 9.4% / 3.1% rates were the audit's per-rubric estimate. The rejudge spot-check shows the failure mode produces unanimous five-judge 4-or-5 scores on the most extreme cells and a mean cell-level deflation of −1.24 anchor points on the one high-baseline subject sampled. The audit's 9.4% rate is conservative both because the rubric anchors used were the prompt rubric (which the rejudge shows is the source of the inflation) and because the audit slice excludes high-baseline subjects entirely.

### §4.6.1 Tier 2 cross-provider replication
*Tests:* whether the gradient direction reproduces across response models from two providers (Anthropic Sonnet 4.6, Google Gemini Pro) on three subjects (Ebers, Yung Wing, Zitkala-Ša) with batteries regenerated by GPT-5.4. The Spec produces positive lift on 7 of 9 (subject, response-model) cells.
*Does not test:* the rubric. Tier 2 holds the rubric constant and varies the response model, the question generator, and the subject. The rubric the judges receive is identical to the main study's. So Tier 2's positive replication on 7 of 9 cells confirms that the spec-effect direction reproduces under apparatus changes downstream of the rubric, but it carries no information about whether the rubric the judges see is operationalizing the construct the §3.3 table claims to operationalize. The two confounds are orthogonal.

### §4.6.2 Judge panel sensitivity
*Tests:* whether headline findings change between the 5-judge primary panel and the 7-judge sensitivity panel (adding Gemini Flash and Gemini Pro). Establishes that no directional claim flips and that the 5-judge primary is the conservative choice for every effect except wrong-Spec fixed derangement.
*Does not test:* the rubric. Panel sensitivity varies the judges, not the rubric the judges read. The +1-point Gemini inflation that drives the α drop is documented as a per-judge calibration artifact, not as a per-rubric divergence. If anything, the §4.6.2 framing reinforces the implicit assumption that the prompt rubric *is* the rubric — the analysis treats absolute-magnitude divergence as a property of the judge, not of the prompt-rubric wording the judge happens to be reading.

### §4.6.7 Rubric-handling limitations
*Tests:* the same audit content as §3.3.6, expanded with per-response-model abstention disaggregation and the memory-system / abstention interaction. Reports that refusals at ≥ 2.0 occur at 9.4% pooled, 14.3% on Haiku (the main-study response model), 26.3% on Sonnet 4.6 (Tier 2), and 100% (n=2) on Gemini Pro.
*Does not test:* cross-rubric construct equivalence at scale, and inherits the §3.3.6 audit's low-baseline-only structural scope. §4.6.7 also makes a published direction-of-bias claim ("both effects raise C5 baseline scores more than they raise Spec-condition scores; the true Spec-vs-baseline gap is therefore likely *larger* than the +0.89 mean lift reported in §4, not smaller") that is directly relevant to the rejudge result. The rejudge's per-condition decomposition shows mean Δ for C5 is −0.48 and for C4a is −1.04 — i.e., C4a deflates *more* than C5 under the paper rubric. On the n=4 subjects in the rejudge sample with both C5 and C4a scored, within-rubric Δ_C4a is +0.05 under the paper rubric vs +0.75 under the prompt rubric. This is a direct empirical contradiction of the §4.6.7 published direction-of-bias claim, on the small rejudge sample. The §4.6.7 claim was based on the assumption that the audit's rubric and the paper's rubric were operationalizing the same construct — which is the assumption the rejudge tests and rejects.

---

## Part 2. The §3.3.6 connection: was this direction already known, just not quantified?

**Partially yes, partially no, and one direction is contradicted.**

What §3.3.6 already noted qualitatively, and the rejudge confirms empirically:

- **Refusal-over-scoring is real and recurrent.** §3.3.6 published that 9.4% of refusals scored ≥ 2.0 under the prompt rubric. The rejudge spot-checks two cells where the same mechanism produces unanimous five-judge scores of 4 or 5 (Equiano q13, Equiano q27). Same mechanism, more extreme tail than the 9.4% rate suggested. The mechanism is in the paper.
- **Per-judge strictness varies.** §4.6.7 published per-judge mean refusal scores from 1.14 (Sonnet, strictest) to 1.41 (Opus, most lenient) — a spread of 0.27 points. The rejudge's per-judge cross-rubric Pearson r ranges from 0.347 (Opus) to 0.544 (Haiku) and per-judge mean Δ ranges from +0.12 (Opus) to −0.72 (Haiku). The same per-judge variance the §4.6.7 audit measured under one rubric reappears in cross-rubric form.
- **The rubric-prompt language gap is a known exposure.** The same-day defensibility analysis (`docs/reviews/rubric_defensibility_analysis_20260508.md`) listed the published-vs-prompt language gap as the only attack surface still open after every existing defense. The rejudge is the empirical test of that exposure, and the result confirms the analysis's prediction that the gap is real and has measurable consequences.

What is genuinely new in the rejudge:

- **Genericity-over-scoring as a second failure mode.** §3.3.6 documented refusal-over-scoring. It did *not* document the case where a generic spec-driven response that articulates the subject's pattern without predicting the held-out event scores 4 or 5 (Babur C4a q2: original prompt rubric 4.00 unanimous, paper rubric 1.40). The rejudge identifies this as a second mechanism distinct from refusal-over-scoring; it sits at the anchor 4-vs-5 boundary, not the anchor 1-vs-2 boundary. The audit's 9.4% / 3.1% refusal-tail rate cannot detect this mechanism because the responses in question are not refusals.
- **High-baseline asymmetry.** §3.3.6 was structurally low-baseline-only. The rejudge's largest divergences are on the one high-baseline subject sampled (Equiano, ρ = 0.10, mean Δ = −1.24). This slice is a structural blind spot of the existing audit — not a mistake the team should have caught, but a scope constraint of the script. The rejudge explicitly caveats that n=5 high-baseline cells from a single subject cannot be claimed to generalize to the other four high-baseline globals (Augustine, Cellini, Rousseau, Zitkala-Ša) without further sampling, so the asymmetric finding is suggestive rather than conclusive.
- **Direction-of-bias contradiction.** §4.6.7 publishes the claim that "the true Spec-vs-baseline gap is therefore likely *larger* than the +0.89 mean lift reported in §4, not smaller." The rejudge's per-condition decomposition shows C4a deflates more than C5 (−1.04 vs −0.48), implying the gap may be *smaller* under the paper rubric, not larger. This is a direct empirical contradiction on n=25, on a sample stratified by condition. It is paper-text-relevant regardless of whether the rejudge's per-condition pattern generalizes to the full study.
- **Quantified cross-rubric correlation.** The defensibility analysis claimed the two rubrics describe the same construct under different wordings. The rejudge tests that claim and produces ρ = 0.389. The pre-registered threshold (ρ ≥ 0.70) was not met on the n=25 sample. This number did not exist before the rejudge.

**Net read.** The mechanism (refusal-over-scoring) was known at low baseline and partially documented as a minor caveat. The second mechanism (genericity-over-scoring) was not previously documented. The high-baseline asymmetry was structurally invisible to the existing audit. The direction-of-bias claim in §4.6.7 was based on an assumption the rejudge contradicts.

**Why was refusal-over-scoring treated as a minor caveat rather than a P0 issue?** Three reasons that are visible in the existing instrumentation. First, the §3.3.6 audit measured the rate (9.4%) under the prompt rubric and compared it to nothing — there was no second rubric to anchor it against, so 9.4% looked like a tail rather than a structural problem. Second, the §4.6.7 disclosure framed both length-inflation and refusal-over-scoring as effects that raise C5 more than Spec conditions, which makes them conservative against the headline (gap likely larger, not smaller); under that framing the failure modes are *bias toward null*, which lowers the alarm. Third, the audit was scoped to low-baseline subjects only, where refusals are more frequent and Spec-condition scores are bounded above by the gradient ceiling — both of which damp the per-condition asymmetry the rejudge surfaces on the high-baseline cells. Each of these decisions was defensible on its own terms; the failure mode is that taken together they produced a portrait of the rubric pathology that was directionally wrong on the high-baseline slice.

---

## Part 3. What additional check pre-launch would have surfaced this

Three options ranked by surface-area-of-coverage:

1. **Cross-rubric construct-equivalence test (what the rejudge ran).** The cleanest single test. Sample 25 to 100 cells stratified by condition and baseline band, score each under both rubrics with the same 5-judge primary panel, compute cell-level Spearman ρ, per-judge consistency, and per-condition Δ. Cost: 125 to 500 API calls, well under $10. This test would have produced the ρ = 0.39 number, the per-condition Δ asymmetry, and the spot-check evidence in one shot. The defensibility analysis explicitly listed this as Option B the same day; the rejudge implements that option on a 25-cell sample.

2. **Calibration on additional synthetic inputs.** Extend the §3.3.3 four-input diagnostic with two new categories: polite-refusal-with-related-context (a constructed response that declines to predict but recites adjacent facts) and generic-spec-pattern-without-event-prediction (a constructed response that articulates a subject's general approach but does not capture the specific held-out event). Both are constructable from the existing held-out passages; per-judge expected scores are 1 under both rubrics. This test would have surfaced refusal-over-scoring and genericity-over-scoring as per-judge calibration deficits well before any main-study scoring run. The cost is comparable to the existing §3.3.3 calibration run. The reason this was not done is that the original calibration set was designed to probe the response-quality boundaries (length, paraphrase, partial-correctness) rather than the response-type boundaries (refusal, genericity), which is a gap in the calibration methodology rather than in any specific check.

3. **Run the paper rubric verbatim from the start.** The cleanest version of (1): use the §3.3 published table as the prompt rubric the judges literally see. This eliminates the gap by construction. The cost is zero — it is a prompt-template change, not a new test. The reason this was not done is path-dependent: the prompt rubric in `scripts/judge_hamerton_5judge.py` predates the §3.3 table phrasing in the paper draft, and the table was edited downstream of the run scripts during paper revision rather than the run scripts being updated to match. The defensibility analysis frames this as the highest-leverage cheap fix; a future paper would adopt this convention by default.

The first two are detectability checks the project could have run. The third is a design hygiene rule that would have prevented the gap from existing in the first place.

---

## Part 4. Honest assessment: how surprising should this be to the paper team?

**Some of it should not be surprising at all. Some of it is mildly surprising. None of it is fundamentally outside the limitations the paper has already disclosed.**

Not surprising:
- The mechanism (refusal-over-scoring) is in the paper at §3.3.6 and §4.6.7. The 9.4% rate was published.
- The rubric-prompt language gap was identified the same day as the rejudge in the defensibility analysis as the only open attack surface. The rejudge is the empirical test of an exposure the team had already named.
- Per-judge variance under the cross-rubric condition tracks per-judge variance under the within-rubric condition. Sonnet's strictness, Opus's leniency, and the +1-point Gemini inflation all reappear in the cross-rubric data.

Mildly surprising:
- The cell-level Spearman ρ = 0.39 is well below the 0.7 pre-registered threshold and below typical inter-judge ρ on the same panel under one rubric (0.86 to 0.93). The defensibility analysis predicted the ρ would be in the "construct-equivalent" range; the actual ρ is in the "different operationalization" range. This is a quantification gap rather than a directional surprise: the existence of divergence was predicted, the magnitude was not.
- Genericity-over-scoring as a second failure mode at the anchor 4-vs-5 boundary is not in the paper and was not predicted by the defensibility analysis. The mechanism is real (Babur C4a q2 unanimous 4 under prompt rubric, 1.40 under paper rubric) and is the largest single divergence cell on a low-baseline subject. The paper's existing anchor 5 verbatim-match calibration would not detect it because the response is not a match attempt; it is a pattern articulation.
- The high-baseline cell-level mean Δ of −1.24 on Equiano is the most striking single number in the rejudge. The §3.3.6 audit could not see this because of its low-baseline-only scope, and the §4.6.7 disclosure inherits the same scope. The asymmetry by baseline band is the most paper-relevant of the rejudge's findings because it intersects directly with the gradient claim, but the rejudge author's own caveat (n=5 cells, single subject) flags that it cannot generalize without further sampling. So the high-baseline number is suggestive of a real asymmetry, not yet conclusive.

Genuine empirical surprise the paper has not absorbed:
- §4.6.7's published direction-of-bias claim (true gap likely larger, not smaller) is contradicted by the rejudge's per-condition decomposition (C4a deflates more than C5). This is one paragraph of paper text whose underlying assumption the rejudge falsifies on n=25. Whether the per-condition pattern generalizes to the full study is the open question; the *direction-of-bias claim* is no longer defensible as written even on the rejudge sample alone.

**Overall framing.** This is closer to "genuine measurement gap that existing instrumentation underweighted in one specific way" than to "knee-jerk change on incomplete information." The paper team had identified the rubric-prompt language gap as an open exposure. The rejudge is the empirical test of that exposure and produces three results, two of which were anticipated in shape (refusal-over-scoring direction, per-judge variance) and one of which was not (genericity-over-scoring; high-baseline asymmetry; direction-of-bias contradiction). The paper has the language to absorb the anticipated results in §3.3.6 and §4.6.7; it does not currently have language for the contradiction or the asymmetry, and §4.6.7's direction-of-bias claim is now the load-bearing problem regardless of what the team decides about the broader rejudge.

The cheapest possible response treats the rejudge as the empirical realization of the §3.3.6 / §4.6.7 caveats, adopts the defensibility analysis's Option A footnote, and revises the §4.6.7 direction-of-bias paragraph to drop the "true gap likely larger" claim or scope it to where it still holds. The fuller response runs the defensibility analysis's Option B (re-judge high-baseline subjects' headline numbers under the paper rubric) to determine whether the asymmetric deflation is an Equiano artifact or a generalized high-baseline phenomenon. That decision is upstream of this reconciliation and exceeds the analytical scope here.

---

## Files referenced

- Rejudge result: `docs/research/published_rubric_robustness_check_20260508.md`, `docs/research/published_rubric_robustness_check_20260508.csv`
- Spot-check evidence: `docs/research/_spotcheck_rubric_robustness_20260508.md`
- Defensibility analysis: `docs/reviews/rubric_defensibility_analysis_20260508.md`
- Paper sections: `docs/beyond_recall_v11_8_draft.md` §3.3 (lines 372 to 546), §4.6 (lines 1525 to 1721), §6.2 (lines 1874 to 1885)
- §3.3.6 audit script: `scripts/audit_low_end_inflation.py` (low-baseline-only constant at line 26-27)
- Calibration data: `results/judge_calibration/`
- Rejudge run script: `scripts/published_rubric_robustness_20260508.py`
