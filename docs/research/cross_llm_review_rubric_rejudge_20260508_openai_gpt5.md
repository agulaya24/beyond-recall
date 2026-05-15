# Cross-LLM review — OpenAI GPT-5 family

**Model:** `gpt-5.5 (with fallback)`  
**Generated:** 2026-05-08 15:11:38  
**Status:** OK  
**Briefing:** `docs/reviews/_rubric_rejudge_briefing_20260508.md`  
**Script:** `scripts/cross_llm_review_rubric_rejudge_20260508.py`  

---

[model=gpt-4.1]

## Q1: Methodology soundness

The rejudge methodology is fundamentally sound for the stated purpose: it isolates the effect of rubric wording by holding all other variables constant (same judge panel, same response and ground-truth texts, same blinding, temperature, and seed). The stratified sampling across conditions and baseline bands is appropriate for a robustness check, and the n=25 cell sample is reasonable for a targeted equivalence test (though not for fine-grained subgroup inference). The only variable changed is the rubric wording in the prompt, which is precisely what needs to be tested.

Potential limitations include: (1) The 1500-character truncation could, in rare cases, omit critical content from longer responses, but this is consistent across both rounds and thus unlikely to bias the comparison. (2) The sample size for the high-baseline band (n=5, all Equiano) is small, limiting generalizability for that subgroup. (3) The reliance on LLM judges (rather than humans) is a broader limitation of the study but does not affect the internal validity of the rejudge. (4) The rejudge does not test for inter-judge reliability under the new rubric, but per-judge Δs are reported.

Overall, the methodology is appropriate for testing rubric equivalence. The main interpretive limitation is the small and unbalanced sample in the high-baseline band, which restricts claims about generalizability there.

## Q2: Generalizability

The catastrophic-deflation finding in the high-baseline band (mean Δ = −1.24, n=5, all Equiano) cannot be confidently generalized to the other high-baseline subjects (Augustine, Cellini, Rousseau, Zitkala-Sa) based on this evidence alone. The sample is both small and unrepresentative—Equiano is unique in the dataset as a globally canonical figure with high pretraining coverage, and the specific questions and responses sampled may not reflect the types of errors or over-scoring that would occur for other high-baseline subjects.

Specific properties that may not transfer: (1) Equiano's data likely contains more refusals or generic responses in the baseline condition, which may have been over-scored under the original rubric but would be less common for other high-baseline subjects with richer, more specific fact coverage. (2) The types of questions asked and the model's ability to answer them may differ for Augustine or Rousseau, whose works and historical contexts are distinct. (3) The observed pattern (refusal/genericity over-scoring) may be less prevalent if the other high-baseline subjects' responses are more consistently specific.

In summary, the n=5/1-subject limitation is severe enough that the catastrophic-deflation conclusion is premature for the broader high-baseline group. A larger, more representative sample is needed.

## Q3: Spot-check responses

**Bābur / C4a / q2:**  
The response is a well-structured essay about Babur's general approach to managing rival powers, but it does not reference the specific event in the held-out passage (Bīban, Shaikh Bāyazīd, Sarū-river). Under the original rubric, a score of 4 ("general direction correct") could be defensible if the judge interprets "general direction" as matching the broad strategy described in the ground truth, even if the specific event is not mentioned. However, the rubric's anchor 5 ("Predicts specific outcome") and 4 ("General direction correct") both imply some degree of event-level alignment, not just thematic similarity. The unanimous 4s suggest judges may have over-rewarded fluency or general subject-matter alignment, or interpreted "general direction" too loosely. Alternatively, there could be confusion between the question (about general approach) and the held-out passage (about a specific intelligence event). On balance, this looks like rubric mis-application—judges are rewarding generic, plausible answers rather than specific behavioral alignment.

**Equiano / C5 / q13 and C4a / q27:**  
Both responses are explicit refusals, stating that the model does not have the relevant information. The original rubric's anchor 1 is "Refuses or off-base," which should map directly to these cases. Scoring them 4.40 and 3.20 is not defensible under the rubric as written; this is clear rubric mis-application. Possible explanations: judges may be over-rewarding politeness, hedging, or the appearance of engagement, or may be defaulting to higher scores for well-written refusals. There may also be a failure to distinguish between "not answering" and "answering incorrectly" in practice.

**Agent's mechanism:**  
The two-mode mechanism—refusal over-scoring and genericity over-scoring—holds up in these cases. The spot-checks directly illustrate both phenomena. I see no alternative explanation that better fits the pattern in these examples.

## Q4: Recommended action

**(b) Escalate to a larger sample first.**

Reasoning: The rejudge robustly demonstrates that the original rubric was mis-applied in ways that systematically inflated scores for refusals and generic responses, especially in the high-baseline Equiano sample. However, the catastrophic-deflation finding in the high-baseline band is based on only five cells from a single subject, which is insufficient to generalize to the other high-baseline subjects. Since the main risk to the paper's claims is in this band (where the largest Δs and lowest ρ are observed), and since a selective rerun is feasible (Option B), the prudent course is to re-judge all high-baseline subjects' headline conditions under the paper rubric before finalizing claims or reframing the paper. If the pattern holds, the paper can be reframed with confidence; if not, the team can report the more nuanced result.

## Coverage notes (optional)

- It would be helpful to see a few spot-checks from the low-baseline band to confirm that the refusal/genericity over-scoring is indeed less prevalent there.
- More detail on the distribution of refusal/generic responses across subjects/conditions would clarify the mechanism's generality.
- Inter-judge reliability statistics under the paper rubric would strengthen the assessment.
