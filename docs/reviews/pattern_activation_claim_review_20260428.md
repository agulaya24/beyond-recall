# Pattern-Predicate Activation Claim — Collective Review

_Date: 2026-04-28_
_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_

**Claim under review:**

> Pattern-predicate activation, not direct quote lookup or anchor-fact recall, is the dominant mechanism by which the Behavioral Specification produces extreme upward anchor-crossing lifts on prediction questions about subjects the model has minimal pretraining footprint on.

**Data summary:**

- Wins inventory: 60 unique paired questions across 18 condition pairs with extreme upward jumps (>=3 rubric anchors).
- 20-question mechanism classification:
  - PATTERN_PREDICATE: 12/20
  - INFERENCE_CHAIN: 7/20
  - ANCHOR_FACT: 1/20
  - DIRECT_QUOTE_MATCH: 0/20
- Question-axis distribution among the 60 jumps: LITERAL_RECALL 28.3% (panel rate 10.2%, 2.77x overrepresented); INTERPRETIVE_INFERENCE 0.75x; REFUSAL_TRIGGERING 0.95x.
- Pre-response failure mode at C5 baseline: FULL_REFUSAL 71.7%, CLARIFY_REQUEST 8.3%, other 20%.

---

## Reviewer 1 — OpenAI (gpt-5.5-2026-04-23)

## 1. Is the dominant-mechanism claim defensible from the 20-case sample?

Partly, but it is stronger as a provisional mechanism claim than as a settled causal conclusion.

The 20-case audit is enough to say that direct quote lookup is not a plausible dominant explanation in the sampled cases: 0/20 DIRECT_QUOTE_MATCH is informative, although the 95% upper bound is still nontrivial, roughly 14 to 17% depending on interval. It is also suggestive against anchor-fact recall as the dominant mechanism: 1/20 ANCHOR_FACT makes a fact-lookup account unlikely to explain most of the audited jumps.

But the stronger claim, that PATTERN_PREDICATE is the dominant mechanism, is less secure. The observed rate is 12/20, or 60%. A rough 95% confidence interval is wide, around 39% to 78%. So the sample supports “pattern-predicate is the modal coded mechanism in this audit,” but not a precise estimate of dominance across the full 60 cases.

Also, the distinction between PATTERN_PREDICATE and INFERENCE_CHAIN matters. If INFERENCE_CHAIN means “predicate-mediated inference without answer text,” then the more defensible aggregate is 19/20 predicate-mediated or non-fact mechanisms versus 1/20 fact lookup. If the paper treats PATTERN_PREDICATE narrowly, 12/20 is suggestive but not decisive.

I would want all 60 extreme-jump cases coded if feasible. The finite population is small, and coding all 60 is cheaper than defending sampling uncertainty. If only sampling, I would want roughly 40 cases for a ±10 percentage point estimate on the pattern rate within the 60-case inventory, assuming random sampling. I would also want stratification by question axis, especially LITERAL_RECALL, because that axis is doing interpretive work.

Disconfirming evidence would include:

- Several additional cases where the spec contains named facts, paraphrased facts, chronology, locations, or distinctive events that the model uses.
- High rates of answer success when behavioral predicates are removed but general subject framing remains.
- Independent blinded raters assigning many cases to “plausible post-hoc attribution” or “ground truth recoverable from latent world knowledge.”
- A strong concentration of lifts among literal questions whose answers are actually inferable from hidden factual cues in the spec.

## 2. What's the alternative hypothesis the author should rule out?

The key alternative is rater-induced mechanism confabulation: because the rater sees the spec, the response, and the ground truth, it retrofits a behavioral-predicate explanation onto any successful post-spec response.

Concrete tests:

1. **Blinded attribution test**  
   Give raters the post-spec response and ground truth, but not the original spec. Instead, show them one of several specs: the true spec, a same-subject predicate-ablated spec, a different-subject spec, or a shuffled predicate bank. Ask them to identify which spec best explains the response.  
   If genuine activation is occurring, raters should select the true spec above chance and cite the same predicates. If rater confabulation dominates, they will find plausible predicates in many decoy specs.

2. **Predicate ablation test**  
   For each audited case, remove the specific predicate judged to drive the answer while preserving length, tone, and unrelated subject description. Regenerate answers.  
   If the claim is true, the extreme lift should drop disproportionately when the implicated predicate is removed. If not, answers should remain similarly successful.

3. **Predicate reversal test**  
   Replace the relevant predicate with its behavioral opposite. For example, change “evaluates landscapes aesthetically before engaging people” to “treats landscapes instrumentally and foregrounds social interaction.”  
   If the model is using predicates causally, responses should shift in the predicted direction, often away from the ground truth. If responses remain stable, the predicate attribution is weak.

4. **Irrelevant predicate control**  
   Provide a matched-length specification containing plausible but irrelevant predicates.  
   If the mechanism is specific pattern activation, lift should be much lower than with the true spec. If the mechanism is just “any rich persona text helps,” the control may perform similarly.

5. **Rater-blind pre-coding**  
   Have human coders mark, before seeing model responses or ground truths, which predicates in the spec could plausibly answer each question. Then compare post-response mechanism labels against this pre-registered predicate map.  
   This reduces post-hoc rationalization.

6. **Response-only causal trace**  
   Ask the model after generation to cite the spec sentence or predicate it used, but compare this to ablation effects. Self-reports alone are weak, but if cited predicates are also causally necessary under ablation, the evidence is stronger.

## 3. The LITERAL_RECALL overrepresentation is interpretively load-bearing

No, it does not automatically follow that literal-recall lifts are produced by pattern-predicate activation rather than fact retrieval. The LITERAL_RECALL label describes the evaluation target, not necessarily the cognitive or computational mechanism. A question can have a literal ground-truth answer while the model reaches it by inference, guesswork, latent knowledge, or hidden factual cues in the spec.

The strongest version of the claim is:

Even for questions whose ground truth is literal autobiographical content, the specification usually does not contain the answer text or a direct fact. Instead, it contains behavioral regularities that constrain the plausible answer space enough for the model to generate the correct or rubric-sufficient response. Thus “literal recall” is being solved by predicate-mediated reconstruction, not recall of an embedded fact.

That is an interesting and non-obvious result, especially because baseline failure is mostly FULL_REFUSAL. The model is not merely improving from vague to precise. It is moving from “I do not know this person” to a substantive answer after receiving behavioral structure.

The weakest version is:

The LITERAL_RECALL overrepresentation may simply show that literal questions have more room for anchor-crossing because baseline responses refuse, and any plausible subject-specific answer earns a much higher band. The rater may then classify successful responses as predicate-driven because the spec is full of predicates. On this reading, literal-recall overrepresentation is a scoring artifact plus attribution artifact, not evidence of a distinct mechanism.

So the paper should not say that LITERAL_RECALL overrepresentation proves predicate activation. It should say it makes the mechanism question more important, because the observed gains occur where one might have expected fact recall, yet the audit found little direct fact or quote support.

## 4. Specific framing recommendation for the paper

The candidate sentence is directionally good but too strong. “The specification’s mechanism is” overstates causality, and “not from the spec containing the answer text” is only audited for the sample unless all 60 are checked.

A sharper and more defensible replacement:

> “In the audited extreme-lift cases, improvements were rarely traceable to copied answer text or explicit anchor facts; instead, they were usually coded as predicate-mediated, with the specification supplying behavioral regularities that the model used to reconstruct answers even on questions scored as literal recall.”

If the author wants an even more cautious version:

> “The evidence favors a predicate-mediated account over a quote- or fact-lookup account for the audited extreme lifts, but causal ablations are needed to confirm that the coded predicates, rather than post-hoc attribution or generic persona enrichment, drive the gains.”

I would use the first in the results section and the second in the discussion or limitations.

## 5. What would weaken or refute the claim?

### Test 1: Code all 60 extreme jumps

- **Manipulation:** Apply the same mechanism coding to every unique extreme-jump case, with at least two independent blinded raters.
- **Prediction if claim is true:** PATTERN_PREDICATE plus INFERENCE_CHAIN remains dominant, and ANCHOR_FACT plus DIRECT_QUOTE_MATCH remains rare.
- **Prediction if alternative is true:** Fact-like support, paraphrased factual cues, or ambiguous attribution rises substantially.
- **Cost:** 60 judge calls per rater, plus adjudication. Cheap and high value.

### Test 2: Predicate ablation regeneration

- **Manipulation:** For each case, remove the predicate identified as causal while preserving the rest of the spec. Regenerate responses.
- **Prediction if claim is true:** The extreme lift often disappears or falls by at least one to two rubric anchors.
- **Prediction if alternative is true:** Performance remains similar because the predicate was not actually causal.
- **Cost:** One new condition per case, 20 to 60 generations plus judging.

### Test 3: Predicate reversal

- **Manipulation:** Replace the implicated predicate with its opposite.
- **Prediction if claim is true:** Answers shift systematically toward the reversed behavioral expectation, often becoming wrong.
- **Prediction if alternative is true:** Answers remain close to the original successful response.
- **Cost:** 20 to 60 generations plus judging. Very discriminating.

### Test 4: Matched irrelevant-spec control

- **Manipulation:** Use a same-length, same-style behavioral spec from another subject or a synthetic decoy spec.
- **Prediction if claim is true:** Extreme lifts drop sharply relative to the true spec.
- **Prediction if alternative is true:** Rich behavioral prose alone produces similar lift.
- **Cost:** 60 generations plus judging.

### Test 5: Rater decoy attribution

- **Manipulation:** Give raters the response and ground truth with multiple candidate specs, only one true.
- **Prediction if claim is true:** Raters identify the true spec and relevant predicate above chance.
- **Prediction if alternative is true:** Raters confidently justify decoy predicates.
- **Cost:** 20 to 60 multi-choice judge calls. Cheap.

### Test 6: Pre-registered predicate-question map

- **Manipulation:** Before looking at model answers, coders map which spec predicates could answer which questions.
- **Prediction if claim is true:** Successful extreme lifts concentrate in pre-mapped predicate-question pairs.
- **Prediction if alternative is true:** Post-hoc labels often cite predicates not predicted in advance.
- **Cost:** Moderate human coding, no new generations.

The most efficient sequence is: code all 60, run predicate ablations on the 20 audited cases, then run reversal controls on the strongest 10. If the claim survives those, it becomes much more than a rater-coded interpretation.

---

## Reviewer 2 — Google (gemini-2.5-pro)

As an experienced empirical reviewer, I have stress-tested the claim based on the evidence provided. Here are my direct responses.

### 1. Is the dominant-mechanism claim defensible from the 20-case sample?

The claim is plausible but not robustly defensible from an N=20 sample alone. The distribution is compellingly skewed: "pattern-based" mechanisms (Predicate + Inference) account for 19/20 cases, while "fact-based" mechanisms (Anchor Fact + Quote) account for only 1/20. This is a strong signal.

However, the small sample size makes the conclusion vulnerable to two key issues:

1.  **Sampling Error:** The 20-question sample might not be representative of the full 60-question set of extreme jumps. While a random sample should be representative on average, with N=20, there is a non-trivial chance of drawing an unrepresentative sample by luck.
2.  **Classification Error:** The entire claim rests on the accuracy of the LLM rater's classifications. With a small N, a few misclassifications could meaningfully alter the conclusion. For example, if 4 of the 12 PATTERN_PREDICATE cases were borderline and could have been classified as ANCHOR_FACT with a slightly different rubric, the ratio would shift dramatically.

**Required Sample Size:** To have confidence, you must analyze the **full population of 60 extreme-jump questions**. This eliminates sampling error entirely and makes the analysis a direct census of the phenomenon. The cost of generating and classifying 40 more examples is minor compared to the confidence gained.

**Disconfirming Evidence:** The conclusion would be invalidated if, upon analyzing the remaining 40 cases, a significant number were classified as ANCHOR_FACT. For instance, if 15 of the remaining 40 were ANCHOR_FACT, the total distribution would be 16 ANCHOR_FACT vs. 43 pattern-based cases (assuming the 7/20 inference chain ratio holds). While pattern-based mechanisms would still be the majority, a 2.7-to-1 ratio is far less "dominant" than a 19-to-1 ratio and would require a significant qualification of the claim. A second piece of disconfirming evidence would be a low inter-rater reliability score if the classification task were given to a blind human expert, suggesting the categories are not robust.

### 2. What's the alternative hypothesis the author should rule out?

The primary alternative hypothesis is **Rater-Side Confabulation**.

This hypothesis states that the model is not genuinely activating specific behavioral predicates. Instead, it is using the full specification as a diffuse semantic guide to produce a plausible answer. The LLM rater, tasked with finding a mechanism and primed by the spec's predicate-heavy design, then performs a post-hoc rationalization, successfully finding a plausible-sounding predicate to attribute the success to. The rater is not discovering a causal mechanism; it is confabulating a justification.

To test this, you must design an experiment that breaks the correlation between the presence of a predicate and the rater's attribution. Here are two concrete controls:

1.  **The Minimal Predicate Ablation Test:** For a subset of the 12 PATTERN_PREDICATE wins, re-run the model with a modified specification where the *single predicate identified by the rater has been removed*.
    *   **If the claim is true:** The model's performance on that specific question should collapse back toward the baseline refusal. This demonstrates the predicate was causally necessary for the lift.
    *   **If the alternative is true:** The model will still produce a high-quality answer. This shows the lift was due to other information in the spec, and the rater's attribution to the now-absent predicate was spurious.

2.  **The Sham Predicate Test:** Create a "sham" specification for one of the autobiographers. This spec should be well-formed, containing plausible-sounding behavioral predicates, but these predicates should be intentionally generic, irrelevant, or sourced from a different person's profile. Then, ask the same questions.
    *   **If the claim is true:** The model should fail to produce the correct answer, as the necessary causal predicates are missing.
    *   **If the alternative is true:** The model might still produce some correct answers (perhaps from latent knowledge activated by the general topic). Crucially, the LLM rater, when shown the successful response and the sham spec, would likely *still identify a predicate in the sham spec* as the driver. This would strongly suggest the rater is simply performing post-hoc pattern matching.

### 3. The LITERAL_RECALL overrepresentation is interpretively load-bearing

Yes, the overrepresentation of LITERAL_RECALL questions is a crucial piece of evidence. It creates a productive paradox: the questions demand facts, but the specification provides behavioral rules. The model's success on these questions forces a deeper look at the mechanism.

**Strongest Version of the Claim:** The specification induces a form of "generative recall." The model is not retrieving a static fact. Instead, it is using the behavioral predicates as a generative grammar or a set of first principles to *reconstruct* the factual answer. For example, given the predicate "consistently names projects after meteorological phenomena observed during their inception," the model can infer the project name "Operation Cyclone" when asked. The 2.77x overrepresentation is not an anomaly; it is the primary signal that the spec is enabling the model to bridge the gap from abstract disposition to concrete fact, a capability it completely lacks at baseline.

**Weakest Version of the Claim:** The predicates in the specification are simply high-level summaries of facts, and the model is performing a sophisticated semantic match. The predicate "evaluates landscapes aesthetically before engaging people" is not a deep behavioral rule but a close semantic proxy for the fact that "upon arriving at the camp, her first action was to sketch the mountain range." The model is not reasoning from first principles; it is just connecting closely related text. The LITERAL_RECALL overrepresentation simply shows that many of the chosen predicates happen to have direct factual correlates in the ground truth, making this semantic matching effective. The mechanism is still pattern-based, but it is less about deep inference and more about guided association.

### 4. Specific framing recommendation for the paper

The candidate sentence is strong but can be sharpened. The phrase "license inference of" is slightly academic and less direct. The term "reconstruct" better captures the generative nature of the proposed mechanism.

Here is a refined replacement:

**"The specification's primary mechanism is behavioral-predicate activation; it enables the model to reconstruct answers to factual questions by applying documented patterns, rather than by retrieving verbatim facts from the context."**

This version is more concise and uses stronger verbs ("reconstruct," "applying"). It clearly frames the core action as applying patterns to generate facts, directly contrasting it with simple retrieval. It preserves the essential components of the original while increasing its force and clarity.

### 5. What would weaken or refute the claim?

Here are three concrete, cheap, and discriminating empirical tests.

**Test 1: Minimal Predicate Ablation (as described in #2)**
*   **Manipulation:** For the 12 PATTERN_PREDICATE cases, create 12 new specs, each with the single rater-identified causal predicate removed.
*   **Predicted Result (Claim True):** Performance on the corresponding questions drops significantly (e.g., >2 rubric bands), approaching the baseline refusal.
*   **Predicted Result (Alternative True):** Performance remains high. The lift is not dependent on that specific predicate.
*   **Cost:** Low. 12 new response generations, plus ~12 judge calls to score the outputs. This is the highest-priority test.

**Test 2: Predicate-to-Fact Transformation**
*   **Manipulation:** Manually rewrite the 12 key behavioral predicates into simple declarative statements of fact. For example, transform "shows a preference for indirect, metaphorical communication" into "In her letters, she used metaphors instead of direct statements." Create a new "Fact-Only Spec" using these.
*   **Predicted Result (Claim True):** This Fact-Only Spec will perform significantly *worse* than the original predicate-based spec. The power of the predicate lies in its generality and abstract nature, which is lost when converted to a specific fact.
*   **Predicted Result (Alternative True):** The Fact-Only Spec will perform equally well or even better. This would show that the model only needs the core semantic information, and the "predicate" framing adds no value.
*   **Cost:** Medium. Requires careful manual rewriting of ~12 sentences, plus 12 new response generations and scoring.

**Test 3: Human Rater Blind Review**
*   **Manipulation:** Provide 2-3 trained human raters with the 20-sample set (question, spec, response, ground truth). Ask them to perform the same mechanism classification task without seeing the LLM rater's labels.
*   **Predicted Result (Claim True):** The human raters will achieve high inter-rater reliability (e.g., Cohen's Kappa > 0.7) and their classifications will largely agree with the LLM rater's, confirming that the PATTERN_PREDICATE category is robust and reliably identified.
*   **Predicted Result (Alternative True):** The human raters will have low agreement with each other and the LLM, indicating that the mechanism categories are subjective and the LLM's confident classifications are likely an artifact of its own internal biases.
*   **Cost:** Low to medium. Depends on the cost of expert human time for ~20 classification judgments. This test directly assesses the reliability of the core measurement.
