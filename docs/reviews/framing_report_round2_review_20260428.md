# Framing-Implications Report -- Round 2 Cross-LLM Review

_Date: 2026-04-28_
_Source report: `docs/reviews/framing_implications_20260428.md`_
_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_

---

## Reviewer 1 -- OpenAI (gpt-5.5-2026-04-23)

## 1. Are the 5 APPLY-AS-DRAFTED iterative refinements justified by evidence?

### Refinement 1: §4.2 “What the aggregate numbers hide”

**Partially justified.** The per-question disaggregation numbers are justified and useful, but the drafted language over-interprets them: “dissolves,” “two opposite mechanisms,” “bimodal,” “generalizes,” and “per-subject mean is misleading” go beyond the cited evidence and conflict with the author’s rule that mean Δ remains primary while per-question phenomena are context.

The right edit is narrower: add the C4→C4a and C8→C9 paired-question breakdowns, explicitly label them as per-question context, and avoid claiming a mechanism or distributional form unless the distribution itself is shown. “Small aggregate Δ coexists with substantial bidirectional item movement” is supported. “The aggregate claim dissolves” is not.

### Refinement 2: §4.2 mean Δ numerical reconciliation

**Justified.** The evidence clearly supports reconciling the inconsistent C8→C9 numbers by reporting both grains: subject-mean +0.14 and per-question +0.088/+0.09 on the low-baseline-8 slice.

This is exactly the kind of clarification the paper needs. It reduces ambiguity rather than changing the result. The only caution is to avoid making the per-question number the new headline if the table and primary analysis use subject means.

### Refinement 3: §4.4.2 strengthen Pattern 1/2/3 with Spearman ρ

**Partially justified.** The Spearman split supports a descriptive rank-order observation, but it does not strongly support Pattern 1/2/3 as mechanism.

The report correctly flags the key alternative: C5 has many tied low scores/refusals, so low ρ may be mechanically induced by floor/tie structure rather than by a distinct “spec-on-baseline mechanism.” The paragraph should be softened to: “A rank-correlation view is consistent with the Pattern 1/2/3 reading,” not “strengthens” or “shows” it. Also, “spec-on-baseline pairs … mean ρ near 0.27 on the C5-to-C4a flagship pair” is imprecise: either report the actual mean across pairs or just cite C5→C4a.

### Refinement 4: §3.6 add half-anchor metric note

**Justified, with wording tightening.** The evidence supports a methodological note that integer-anchor crossings are conservative and miss some same-band movement.

But the paragraph should not imply that all same-band half-anchor shifts are “spec effects” in a causal sense. They are detected score movements, not necessarily meaningful representational changes. “Lower bound on movement detectable by the integer-anchor metric” is safer than “lower bound on spec effects.” The author should keep mean Δ and integer-anchor crossings primary, and place the half-anchor material as a sensitivity/measurement note.

### Refinement 5: Appendix B Hamerton-leverage at per-question grain

**Partially justified.** An appendix-level Hamerton leverage check is justified, especially because Hamerton contributes 25% of the unique extreme upward anchor crossings and has a 2.1x elevated rate.

But the drafted language overstates “mechanism distribution is invariant.” With Hamerton n=15 and globals n=45, and with the same post-hoc classifier whose predicate code has already failed as a discriminator, “similar in this coding” is the maximum defensible claim. The appendix should report the concentration and candidate confounds, not reassure too strongly that mechanism is invariant.

---

## 2. Refinement 6: is REFINE-FIRST the right disposition?

I would go further than REFINE-FIRST: **HOLD-FOR-PHASE-2C-RESULTS for any body-text positive mechanism claim**, including the narrow INFERENCE_CHAIN claim.

The deep analysis does justify removing or weakening any predicate-activation language. It also justifies a limitation-style disclosure that the post-hoc rhetoric classifier did not discriminate extreme upward anchor crossings from non-crossing spec-loaded controls. But the surviving “11 of 60 vs 2 of 38 genuine_inference_via_spec” result is too small and too classifier-dependent to become a body-text mechanism claim in §5.4.

The narrow result is suggestive. It says: in the audited extreme-upward population, a minority of cases appear to involve specification-enabled inference not grounded by retrieval. That belongs in an appendix or a cautious limitations note, not in the main mechanism story. Phrases like “that subset is real signal” and “strongest mechanism signal in the wins data” are too strong before Phase 2c.

So the right body-text move is:

- **Do add**: “A post-hoc mechanism audit did not support the stronger predicate-activation interpretation; details and Phase 2c ablations are in the appendix.”
- **Do not add yet**: “About 1 in 6 extreme upward cases show genuine specification-enabled inference” as a substantive §5.4 claim.
- **Do hold** the positive mechanism framing until ablations land.

This is especially important because the author’s operating principle is caution after prior framing errors. A public correction is good; replacing one premature mechanism claim with a narrower but still underpowered mechanism claim is less good.

---

## 3. Pivot 7: is the pre-condition correctly framed?

Yes: the strong claim — “the mechanism is predicate activation, not retrieval” — should be **Phase-2c-dependent**. The report is right that the current evidence is not merely incomplete; it is partly negative, because the predicate-rhetoric code does not discriminate extreme upward anchor crossings from non-crossing spec-loaded controls.

But the proposed Phase 2c bar should be raised and made more specific.

The experiments need to show **causal specificity**, not just degradation after deleting useful text. Specifically:

1. **Targeted predicate removal must reduce the incremental spec effect.**  
   For questions where a particular predicate is hypothesized to drive the increase in representational accuracy, removing that predicate while preserving other spec content, length, style, and factual anchors should selectively reduce the C4a/C9 response relative to the intact-spec condition.

2. **The drop must be larger than matched-control edits.**  
   Remove or alter comparable non-implicated predicates, neutral descriptive sentences, or stylistic material. If any deletion of subject-specific prose causes the same degradation, the result supports generic context enrichment, not predicate activation.

3. **The effect must be question-specific.**  
   Removing predicate P should harm questions whose answer depends on P more than questions whose answer does not. Otherwise the intervention is just weakening the specification globally.

4. **Predicate substitution should behave directionally.**  
   Replacing the implicated predicate with a plausible but irrelevant or contradictory predicate should either remove the lift or redirect the answer in the predicted way. This would be stronger than simple deletion.

5. **Retrieval controls must remain fixed.**  
   The experiment must distinguish “the spec contained answer-like content” from “the spec’s predicate enabled inference.” Same retrieval, same question, same model, blinded judging.

6. **Judging and mechanism coding must be blinded.**  
   Raters should not know whether they are seeing intact, ablated, or sham-ablated specs. Mechanism labels should be independently coded, with acceptable agreement, but reliability alone is not enough; the causal score movement is the core evidence.

7. **The effect must cover enough of the population to justify “primary mechanism.”**  
   Showing this in 12 originally selected cases would justify “a mechanism,” not “the primary mechanism.” For “primary,” the ablation effect needs to account for a substantial share of the aggregate/spec incremental lift or of the extreme upward anchor crossings across the full audited set or a preregistered stratified sample.

Without those results, the defensible language is representational and descriptive: the specification sometimes increases representational accuracy, and some cases appear inference-like. Not “predicate activation, not retrieval.”

---

## 4. Pivot 8: two-mechanism story — strongest claim?

I do **not** agree that Pivot 8 is the strongest pivot if it is framed as a “two-mechanism story.” It is probably the strongest **descriptive statistical addition**, but not the strongest **mechanism** claim.

The Spearman split is interesting:

- spec-on-baseline: C5→C4a ρ=0.27;
- spec-on-info-rich: C4→C4a ρ=0.72, C8→C9 ρ=0.70, C2a→C4a ρ=0.61.

That supports this claim:

> When the pre-condition already contains subject-specific information, adding the specification tends to preserve question rank order more than when the pre-condition is baseline-empty.

That is a good body-text observation if carefully framed.

But the report’s stronger claim — “two mechanisms” — is under-supported. The strongest objection is the floor/tie artifact: C5 likely contains many tied refusals or generic low-band answers. Spearman correlation from a tied floor to a differentiated post-condition is mechanically suppressed. Info-rich pre-conditions begin more spread out, so their rank correlations will naturally be higher. That can happen with one mechanism operating over different baseline score distributions.

Also, the pivot text says “spec-on-info-rich uniformly lifts” in the heading/question, but the actual evidence is bidirectional: roughly a fifth improve and a fifth worsen. “Uniformly lifts” should be avoided entirely.

Should it enter the paper? **Yes, but as a cautious body-text descriptive claim or a short subsection, not as a major mechanism pivot.** A good formulation:

> A rank-correlation view suggests that the specification behaves differently depending on the information already present: from baseline-empty conditions it differentiates many previously low/tied responses, while on information-rich conditions it more often modulates already differentiated responses. Because baseline floor/tie structure can also produce this pattern, we treat this as a descriptive regularity rather than a causal mechanism claim.

If space is tight, put the full table and robustness checks in the appendix, with one body paragraph in §4.2 or §4.4. The claim should not be elevated above mean Δ.

---

## 5. What’s missing from the framing report?

### Evidence streams not addressed enough

The report says several sections do not need change, but it does not sufficiently use them as constraints on the proposed pivots.

Missing or underused evidence streams include:

- **Wrong-spec controls (§4.3):** These are relevant to whether the model is using spec content specifically versus responding to generic richness/style.
- **Judge/provider sensitivity:** The report cites direction agreement but does not ask whether per-question phenomena replicate across judges/providers or are driven by particular judges.
- **Baseline score distributions and tie rates:** Essential for interpreting the Spearman split.
- **Per-subject robustness of Spearman ρ:** Especially low-baseline-only and Hamerton-dropped versions.
- **Question-type composition:** Literal recall overrepresentation among extreme upward anchor crossings may reflect battery design, not mechanism.
- **Spec component composition:** Length is ruled out for Hamerton, but predicate density, anchor density, and brief/core/prediction mix remain open.
- **Model-output length/style effects:** Since the mechanism heuristic tracks spec-loaded response style, the report should more directly consider verbosity/coherence/style as score drivers.
- **Bootstrap/confidence intervals:** Many rates are presented as stable without uncertainty.

### Alternative explanations not surfaced enough

The report mentions floor effects and rater confabulation, but it underweights them in recommendations. Other alternatives:

- **Regression from refusal floor:** Large upward crossings may reflect moving out of abstention, not special representational recovery.
- **Rubric category compression:** Integer bands may exaggerate apparent discontinuities.
- **Question ambiguity:** Spec may license plausible answers where the rubric rewards coherence, not factual grounding.
- **Generic persona enrichment:** A rich subject sketch may help without predicates being causal.
- **Unequal question counts / Simpson effects:** Subject-mean and per-question grains diverge; the report should treat this as a standing risk.
- **Battery-generator artifacts:** Especially for Hamerton and literal-recall concentration.
- **Retrieval quality variation:** Info-rich conditions are not uniformly “info-rich” per question.

### Pivots to add or remove

Add:

- A **grain-and-slice discipline note**: every Δ or rate should label subject-mean vs per-question, low-baseline-8/9 vs all subjects, and whether Babur is excluded.
- A **Phase 2c protocol appendix** before results: preregister ablation logic, controls, sample, thresholds.
- A **terminology cleanup**: avoid “wins” in paper prose; use “increases in representational accuracy” or “extreme upward anchor crossings.”

Remove or downgrade:

- “Apply as drafted” for Refinement 1.
- “Strengthen Pattern 1/2/3” language for Refinement 3.
- Any body-text positive mechanism claim in Refinement 6 before Phase 2c.
- “Strongest pivot” status for Pivot 8 unless reframed as descriptive rank-correlation evidence.

### Is risk treatment honest or defensive?

Both. The risk sections are unusually honest in naming prior errors and alternative hypotheses. But the recommendations are often more aggressive than the risk analysis warrants. The pattern is: the report identifies a serious alternative, then still recommends APPLY-AS-DRAFTED. That reads defensive. A genuinely cautious report would more often say APPLY-WITH-SOFTENING or APPENDIX-ONLY.

---

## 6. What’s overclaimed in the framing report?

Specific overclaims:

- **“The ‘spec adds little when corpus is already there’ claim … dissolves at the per-question grain.”**  
  It does not dissolve. It remains true at the aggregate grain. The per-question grain contextualizes it.

- **“Two opposite mechanisms are roughly balancing across questions.”**  
  Opposite score movements are observed. Opposite mechanisms are inferred, not established.

- **“Spec-on-info-rich produces a bimodal per-question distribution.”**  
  The cited rates show bidirectional movement, not necessarily bimodality. Show the histogram or soften.

- **“A per-subject mean is a misleading summary.”**  
  Too strong. It is the primary metric by author policy. Say “incomplete” or “not sufficient to characterize item-level heterogeneity.”

- **“Pattern 1 / Pattern 2 / Pattern 3 mechanism analysis … generalizes.”**  
  The report itself says the typology was characterized on Supermemory and not independently characterized on facts-only/corpus-only.

- **“Direction-agreement … rules this out” / “well above chance.”**  
  It partially mitigates noise; it does not rule it out. “Chance” needs a defined null.

- **“Numbers reported as ‘the spec moves X%’ are lower bounds on movement.”**  
  Safer: integer crossings undercount same-band score movement. They are not necessarily lower bounds on causal spec effects.

- **“Mechanism distribution is invariant to dropping Hamerton.”**  
  Too strong for n=15 and a compromised classifier. Say “similar under this coding.”

- **“That subset is real signal.”**  
  The 11/60 INFERENCE_CHAIN subset is suggestive, not established as real causal signal.

- **“Strongest pivot in the set.”**  
  Pivot 8 is the cleanest descriptive statistic, but the mechanism interpretation is vulnerable to floor/tie artifacts.

- **“Panel-judge agnostic.”**  
  Spearman ρ is computed from panel scores. It is less vulnerable to post-hoc mechanism coding, but not judge-agnostic.

- **“The spec is doing first-pass identity and pattern-supply work.”**  
  This is plausible but mechanistic. The data show re-ranking and anchor movement, not directly “identity and pattern-supply work.”

---

## 7. Strongest single objection to the report’s overall stance

The strongest objection is that the report repeatedly converts **descriptive per-question statistics into mechanism-facing body text** despite the author’s stated caution and despite fresh evidence that prior mechanism framing was wrong.

The core evidence is solid in places: numerical reconciliation, per-question movement rates, half-anchor sensitivity, Hamerton concentration, and rank correlations are all useful. But the proposed paper edits too often turn those into claims about “mechanisms,” “bimodality,” “pattern supply,” “two mechanisms,” or “real signal.” That is exactly the failure mode the author is trying to avoid.

My recommendation: split the report’s actions into three tiers.

1. **Apply now:** numerical reconciliation; grain labels; half-anchor methodological note; appendix Hamerton concentration check.
2. **Apply only with softened language:** per-question disaggregation; Spearman rank-correlation observation.
3. **Hold for Phase 2c or appendix-only:** predicate activation, INFERENCE_CHAIN mechanism claims, and any “two-mechanism” causal story.

The paper will be stronger if it says less mechanistically and labels grains more rigorously. The evidence supports “small mean Δ can hide substantial bidirectional item-level movement.” It does not yet support a confident account of why that movement happens.

---

## Reviewer 2 -- Google (gemini-2.5-pro)

Excellent. This is a well-structured and evidence-rich framing report. My assessment follows the requested format.

### 1. Are the 5 APPLY-AS-DRAFTED iterative refinements (Refinements 1-5) justified by evidence?

**Refinement 1: §4.2 "What the aggregate numbers hide" subsection**
**Justified.** The proposed text is a direct, factual summary of the per-question data from the wins inventory, providing necessary context for the small aggregate `mean Δ` and aligning with the author's principle of treating per-question phenomena as context, not headline.

**Refinement 2: §4.2 mean Δ numerical reconciliation**
**Justified.** This is a matter of numerical accuracy and transparency; the report correctly identifies a discrepancy and proposes a clear, statistically sound solution by reporting both the subject-mean and per-question grain values.

**Refinement 3: §4.4.2 strengthen Pattern 1/2/3 with Spearman ρ**
**Justified.** The Spearman ρ split provides a robust, quantitative statistical signature that corroborates the more qualitative Pattern 1/2/3 story, strengthening the paper's mechanistic claims without depending on the now-suspect predicate-level heuristics.

**Refinement 4: §3.6 add half-anchor metric note**
**Justified.** This is a straightforward act of methodological transparency that preempts potential reviewer objections about the metric's coarseness and correctly frames the paper's primary metric as a conservative lower bound on the spec's effect.

**Refinement 5: Appendix B Hamerton-leverage at per-question grain**
**Justified.** Given Hamerton's 2.1x higher jump rate and 25% share of the extreme-wins population, this sensitivity analysis is non-negotiable; placing it in the appendix is appropriate, and the finding that the mechanism distribution is invariant is an important null result to document.

### 2. Refinement 6 (cautious mechanism description) -- is REFINE-FIRST the right disposition?

**HOLD-FOR-PHASE-2C-RESULTS is the right call.**

The REFINE-FIRST disposition is a reasonable middle ground, but it doesn't go far enough in acknowledging the core finding of the deep analysis: the rhetorical-classification heuristic itself is unreliable. The analysis didn't just falsify the *strong* pattern-activation claim; it cast serious doubt on the ability of this specific LLM-based classifier to distinguish causal mechanisms from stylistic artifacts *at all*.

The narrower claim that survives—that 11 of 60 `INFERENCE_CHAIN` cases are "genuine_inference_via_spec"—is still a product of this same flawed heuristic. The signal (18.3% in jumps vs. 5.3% in controls) is suggestive, but it's a correlation generated by a tool that has been shown to be non-discriminating on its primary task. To include this in the body text, even cautiously, is to grant the heuristic a degree of credibility it no longer deserves.

The most cautious and intellectually honest path, consistent with the author's operating principles, is to state that the deep analysis invalidated the heuristic-level approach to mechanism attribution and that *all* such claims are now deferred pending the causal evidence from Phase 2c predicate ablations. Adding the `INFERENCE_CHAIN` claim now risks having to retract a second mechanism claim later. It's better to hold all fire until the ablation results are in.

### 3. Pivot 7 (strong mechanism description, PHASE-2C-DEPENDENT) -- is the pre-condition correctly framed?

**Yes, the pre-condition is correctly and rigorously framed.**

The pivot correctly identifies that the current evidence is not just insufficient but actively *negative* (the heuristic fails the discriminator test). The proposed bar for reinstating the claim is therefore not mere confirmation, but "restoring positive discrimination" through causal intervention. This is exactly the right standard.

The specific experiments required are excellent:
1.  **Ablation (a):** Shows necessity. Removing the predicate must break the effect.
2.  **Replacement/Reversal (b):** Shows specificity. A plausible-but-wrong predicate must also fail to produce the effect, ruling out generic "persona enrichment."
3.  **Inter-rater reliability (c):** Shows the heuristic is not just an idiosyncratic artifact of one classifier. A Cohen's κ > 0.5 is a standard, defensible threshold for moderate agreement.

These three tests, if passed, would provide the necessary evidence to move from a correlational, heuristic-based claim to a defensible causal one. The pre-condition is not only correctly framed but serves as a model for how to validate such mechanism claims in future work.

### 4. Pivot 8 (two-mechanism story, APPLY-AS-DRAFTED) -- strongest claim?

**Yes, this is the strongest *new* claim in the report, but its framing requires extreme care.**

I agree with the report's assessment that this is the most significant and well-supported new pivot. It's grounded in a robust, panel-wide statistical primitive (Spearman ρ) that is independent of the flawed mechanism heuristics. It offers a powerful, elegant way to unify observations across the entire experimental matrix.

**The strongest objection is the floor-effect artifact, and it is a very strong objection.** The report identifies it correctly: the low correlation in spec-on-baseline conditions could be a mathematical artifact of starting with a low-variance, tied-at-the-bottom distribution (C5 refusals) and then spreading it out. This isn't a minor caveat; it's a plausible alternative explanation that reframes the finding from "two distinct mechanisms" to "one mechanism operating on two statistically distinct input distributions."

**This should enter the paper as a body-text claim, but not as a definitive "two-mechanism story."** It should be framed as a "two-signature finding." The proposed text is good, but it should be edited to more explicitly foreground the alternative hypothesis.

Instead of:
> "A two-mechanism reading of the spec's behavior across conditions."

A more cautious and defensible framing would be:
> "Two distinct statistical signatures of the spec's effect."

The body of the paragraph should then present the Spearman ρ split as a core empirical finding and explicitly discuss the two competing interpretations: (1) a genuine difference in the spec's mechanism (re-ranking vs. modulation) or (2) a statistical artifact of the baseline score distributions (floor effect). This presents the finding honestly, shows the author has considered the primary objection, and turns a potential weakness into a sign of intellectual rigor. It is still the strongest pivot because the statistical signature itself is a novel and important discovery, regardless of its ultimate interpretation.

### 5. What's missing from the framing report?

The report is exceptionally thorough, but there are a few missing connections and one missing pivot.

*   **Missing Connection: Interaction of Confounds.** The report treats the Hamerton confound, the floor-effect confound (for Pivot 8), and the rater-confabulation confound (for Pivot 7) as separate issues. It's missing a synthesis of how they interact. For example: The floor effect in C5 creates the population of low-scoring questions eligible for "extreme upward jumps." Hamerton's battery, for reasons not yet understood (legacy generator, question types), seems to contain a high density of these questions. The flawed rhetorical heuristic is then applied to this Hamerton-heavy population of floor-effect-driven jumps. The report analyzes each risk in isolation but misses the opportunity to describe this cascading chain of confounds, which would further strengthen the case for extreme caution on all mechanism claims.

*   **Missing Alternative Explanation: Spec Format.** The Hamerton confound note mentions that Hamerton used a "brief only" spec, which is ~0.33x the size of the globals' spec. The report lists this as a candidate explanation for the jump rate but doesn't explore the implication: **Could a shorter, denser, more predicate-heavy spec be *more* effective at triggering lift than a longer one diluted with other material?** This inverts the naive "more context is better" assumption and provides a testable hypothesis for Phase 2c (e.g., run globals with a "brief only" spec). This is a more specific and compelling alternative than "subject pretraining thinness."

*   **Missing Pivot: Elevating the Wrong-Spec Control.** The report notes that the §4.3 wrong-spec analysis is unaffected. This is a missed opportunity. The deep analysis has shown that post-hoc rhetorical analysis of *correct-spec* responses is unreliable. In contrast, the wrong-spec condition (§4.3) is a clean, interventional experiment. The paper's overall argument would be stronger if it explicitly pivoted to frame the wrong-spec results as the *primary source of evidence for mechanism*, while framing the correct-spec mechanism analysis as exploratory and inconclusive. The report should propose a pivot to re-center the paper's narrative weight onto the adversarial C2c results, as they represent a more robust form of evidence than the now-suspect wins-analysis.

*   **Risk Treatment:** The risk treatment is honest, not defensive. This is a major strength. It doesn't need to be changed, but the missing synthesis of interacting confounds would make it even stronger.

### 6. What's overclaimed in the framing report?

The report is commendably well-calibrated. Overclaims are minor and subtle.

*   **"The narrower mechanism claim that does survive" (Refinement 6):** As discussed in Q2, calling the `INFERENCE_CHAIN` finding a "surviving claim" is slightly too generous. It's a "surviving correlation from a compromised source." The language implies more robustness than is warranted pre-ablation.

*   **"Strongest pivot in the set" (Pivot 8 Recommendation):** While I agree it's the most *interesting* and *substantive* pivot, calling it the "strongest" could be misread as "most defensible." The floor-effect objection is significant enough that simple, corrective refinements like R1 and R2 are arguably "stronger" in the sense of being less open to interpretation. This is a minor semantic point, but precision matters. The pivot is the most *consequential*, not necessarily the most irrefutable.

*   **"The mechanism distribution is invariant to dropping Hamerton" (Refinement 5):** The report states this as a fact. While the numbers support it, it should be caveated with "...as measured by the heuristic classifier." Since the classifier's validity is in question, its findings of invariance are also provisional. The statement is true of the *data*, but its implication for the *actual mechanism* is uncertain.

### 7. Strongest single objection to the report's overall stance

The strongest single objection is:

**The report's strategy is an incremental retreat when the evidence justifies a full-scale realignment.**

The deep analysis did not just weaken a specific claim; it effectively invalidated an entire *class* of evidence (post-hoc rhetorical classification) for this paper. The report's stance is to carefully walk back the claims that relied on that evidence, hedge where necessary, and defer the strongest claims pending new, better evidence (ablations).

This is a sensible and responsible path. However, a more aggressive—and arguably more honest—stance would be to declare the entire wins-analysis/mechanism-classification effort a dead end for the current paper. This would mean:

1.  **Removing** the qualitative Pattern 1/2/3 story from the body text and moving it to an appendix as a "post-hoc exploratory analysis whose heuristic was later found to be non-discriminating."
2.  **Elevating** the clean, interventional evidence from the wrong-spec controls (§4.3) and the robust statistical signature from the Spearman ρ analysis (Pivot 8) to become the paper's central claims about mechanism.
3.  **Framing** the paper not as "here is how spec-driven lift works," but as "we show that specs produce lift, and while our initial attempts to classify the mechanism via rhetoric proved unreliable, the effect's statistical signature and behavior under adversarial controls point toward two distinct operational modes."

The report's current stance tries to salvage as much of the existing paper structure and analysis as possible. My strongest objection is that it should be bolder in its conclusions from the deep analysis and fundamentally restructure the paper's narrative around the evidence that *survived* scrutiny, rather than trying to patch the holes in the evidence that didn't.
