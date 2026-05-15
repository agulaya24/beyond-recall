# Cross-LLM review — Gemini 2.5 Pro

**Model:** `gemini-2.5-pro`  
**Generated:** 2026-05-08 15:11:11  
**Status:** OK  
**Briefing:** `docs/reviews/_rubric_rejudge_briefing_20260508.md`  
**Script:** `scripts/cross_llm_review_rubric_rejudge_20260508.py`  

---

## Q1: Methodology soundness
The rejudge methodology is sound for its stated purpose: testing the construct equivalence of the two rubric wordings. The experimental design is clean and well-controlled. By holding constant the judge panel, prompt template, input data (held-out passages and response texts), and technical parameters (temperature, truncation), the design successfully isolates the rubric wording as the sole independent variable. This allows for a direct causal attribution of any observed scoring differences to the change in rubric text.

The stratification of the n=25 sample across subjects and conditions is a strength, ensuring the test covers a range of performance levels and contexts present in the main study. While a sample size of 25 is small for drawing precise quantitative conclusions about the overall effect size or correlation across the entire dataset, it is more than sufficient to detect a large discrepancy, which is precisely what occurred. The pre-registered threshold (ρ ≥ 0.70) provided a clear, falsifiable hypothesis.

There are no obvious flaws in the operationalization. The use of a fixed seed ensures reproducibility. The only minor limitation is the sample size itself, which affects the generalizability of the *quantitative* results (e.g., the exact value of ρ or the mean Δ), but it does not invalidate the core qualitative finding that the two rubrics are not applied interchangeably by the LLM judges.

## Q2: Generalizability
The conclusion of catastrophic deflation for high-baseline subjects is premature and cannot be generalized from the evidence provided. The limitation of using n=5 cells from a single subject (Equiano) is severe and makes the finding highly susceptible to being an artifact of that specific subject's data.

Several properties of the Equiano data could be unique and not representative of the other high-baseline subjects (Augustine, Cellini, Rousseau, Zitkala-Sa):
1.  **High Pre-training Familiarity:** Equiano's narrative is a canonical text. Models may have a strong, pre-existing representation of it, leading them to produce more confident and well-structured refusals when a specific fact is not present in the provided context. This could interact with the judges' tendency to over-score helpful-sounding refusals.
2.  **Question Type Distribution:** The questions for Equiano might be more focused on specific, verifiable factual recall compared to more philosophical or interpretive questions for a subject like Augustine. This would naturally lead to a higher proportion of "I don't find that fact" responses, making the "refusal over-scoring" issue more prominent for Equiano than for others.
3.  **Selection Bias in Spot-Checks:** Two of the three largest-divergence examples provided are from Equiano, and both are refusals. While this highlights a key failure mode, it may also overstate the prevalence of this specific response type within the high-baseline band as a whole.

Without data from the other high-baseline subjects, it is impossible to know if this deflationary effect is a general property of high-performing conditions or an idiosyncratic interaction between the original rubric's flaws and the specific nature of the Equiano evaluation set. The finding should be treated as an "Equiano artifact" until proven otherwise.

## Q3: Spot-check responses
My reading of the three spot-check cases strongly suggests the agent's two-mode mechanism is correct. The original judges are systematically mis-applying the original rubric.

**Bābur / C4a / q2:** A score of 4 ("General direction correct") is a *defensible but poor* reading of the original rubric. It is defensible only under a very loose interpretation where "general direction" means "describes the subject's general strategic character." The response is a fluent, well-structured essay on Babur's military doctrine, which is thematically relevant. However, this reading ignores the primary instruction to "PREDICT what actually happened" and the anchor "5=Predicts specific outcome." The held-out passage is a specific intelligence event (Bīban/Bāyazīd crossing the Sarū), which the response completely misses. A more rigorous application would score this a 2 ("Wrong prediction") or at best a 3 ("Right domain wrong outcome"). The unanimous score of 4 strongly suggests the judges are over-rewarding fluency and thematic relevance at the expense of predictive accuracy. This is a clear case of "genericity over-scoring."

**Equiano / C5 / q13 and Equiano / C4a / q27:** The original scores of 4.40 and 3.20 are indefensible mis-applications of the rubric. Both responses are explicit, unambiguous refusals. The original rubric's anchor 1 is "Refuses or off-base." There is no ambiguity. The judges failed to follow a direct instruction. The most likely alternative explanation is a failure mode common to instruction-tuned LLMs: they are rewarding "helpfulness." The models' refusals are polite and offer suggestions for how the user could find the information elsewhere. The judges appear to be scoring this helpfulness rather than the predictive accuracy of the response, directly contravening the prompt's goal.

**Agent's Mechanism:** The agent's two-mode mechanism (refusal over-scoring + genericity over-scoring) holds up perfectly. It provides a comprehensive and parsimonious explanation for the divergence seen in all three spot-check cases. The Babur case is a textbook example of genericity over-scoring, and the two Equiano cases are textbook examples of refusal over-scoring. I do not see a different pattern; this mechanism appears to correctly identify the two major ways the judges mis-applied the original prompt's rubric. The paper rubric, with its stricter anchor 5 ("Captures the behavioral pattern observable in the verbatim held-out ground-truth passage"), correctly penalizes both failure modes.

## Q4: Recommended action
My recommendation is **(b) Escalate to a larger sample first**.

The rejudge has successfully demonstrated that the two rubrics are not equivalent and that the original rubric was systematically mis-applied, inflating scores for generic responses and helpful refusals. This finding is robust and must be addressed. However, the *consequences* of this finding for the paper's central claims—particularly the contrast between low- and high-baseline subjects—are currently obscured by the n=1 subject design for the high-baseline band.

Option (a) is insufficient because it leaves the paper's headline quantitative claims resting on data known to be generated by a flawed process. It discloses the problem but doesn't fix it, undermining the credibility of the results. Option (c) is incorrect because the finding of a discrepancy is clearly real and well-supported by the spot-checks.

Therefore, Option (b) is the most scientifically rigorous and responsible path forward. Re-judging the headline conditions for all five high-baseline subjects will directly test the generalizability of the catastrophic deflation finding. This will clarify whether the paper's "ceiling effect" framing is fundamentally sound (even if the ceiling is lower) or if it is an artifact of Equiano's data. This targeted re-run is a cost-effective way to resolve the single biggest uncertainty raised by the rejudge before deciding on the final framing of the paper's results.

My mind would change to Option (a) only if the time and cost of the re-run were absolutely prohibitive and the paper's claims could be substantially re-written to rely only on the low-baseline results, effectively excising the high-baseline contrast.

## Coverage notes (optional)
To better assess generalizability (Q2), it would have been helpful to see:
- The distribution of question types (e.g., factual recall vs. interpretation) for Equiano compared to other high-baseline subjects.
- A few random, non-outlier examples from both low- and high-baseline subjects to understand typical responses, not just the most divergent ones.
