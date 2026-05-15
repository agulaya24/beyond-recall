# Cross-LLM review — Mistral Large

**Model:** `mistral-large-latest`  
**Generated:** 2026-05-08 15:09:28  
**Status:** OK  
**Briefing:** `docs/reviews/_rubric_rejudge_briefing_20260508.md`  
**Script:** `scripts/cross_llm_review_rubric_rejudge_20260508.py`  

---

## Q1: Methodology soundness
The rejudge methodology is largely sound, with a few minor caveats. The design preserves all critical variables (panel composition, blinding, temperature, truncation, seed) while isolating the rubric wording as the sole manipulated factor. This is a strong experimental control for testing construct equivalence. The stratified sampling across conditions and baseline bands is appropriate, though the high-baseline band’s reliance on a single subject (Equiano) is a noted limitation (addressed in Q2).

Two potential flaws:
1. **Prompt template consistency**: The rejudge used the *same prompt template* but swapped in the §3.3 rubric wording. However, the original prompt’s structure ("Rate 1-5: 5=Predicts specific outcome...") is more telegraphic than the §3.3 anchors, which are longer and more nuanced. This could introduce framing effects beyond just the anchor wording. A stronger test would have reformatted the original prompt to match the §3.3’s prose style (e.g., "Rate 1-5 where 5 means...").
2. **Truncation artifacts**: The 1500-character limit may disproportionately affect the paper rubric’s application, as its anchors (e.g., "captures the behavioral pattern observable in the verbatim held-out passage") require more context to evaluate than the original’s "predicts specific outcome." If truncation omits critical details, the paper rubric’s scores could be artificially deflated. This is partially mitigated by the spot-checks (which show the issue persists even with full context), but it remains a confound.

**Interpretation impact**: These flaws do not invalidate the finding but suggest the divergence might be *partially* attributable to prompt structure, not just anchor wording. The core conclusion—that the rubrics are not equivalent—holds, but the mechanism may be more complex.

---

## Q2: Generalizability
The catastrophic-deflation finding for high-baseline subjects is **premature to generalize** based on the current evidence. The n=5 cells all come from Equiano, whose data has unique properties that may not transfer to the other four high-baseline subjects (Augustine, Cellini, Rousseau, Zitkala-Sa):

1. **Pretraining coverage**: Equiano’s *Interesting Narrative* is a canonical abolitionist text, likely over-represented in LLM training data. This could lead to:
   - More "generic" responses (e.g., refusal to answer due to overconfidence in pretrained knowledge, as seen in Spot-check 2).
   - Higher original scores due to judges rewarding fluency over specificity (a known bias in LLM-as-judge setups).
   Other high-baseline subjects (e.g., Cellini, Rousseau) are also well-documented but may lack Equiano’s *specific* pretraining saturation.

2. **Question types**: The sampled Equiano questions (e.g., "What specific dangers does Mrs. Davis warn Equiano about?") are highly specific to his narrative. If other high-baseline subjects’ questions are more thematic (e.g., "How does Rousseau handle criticism?"), the rubric divergence might be less severe.

3. **Response styles**: Equiano’s responses include explicit refusals (Spot-checks 2 and 3), which the original rubric over-scored. If other subjects’ responses are more substantive (even if generic), the deflation effect might be smaller.

**Recommendation**: The paper team should adopt **Option B (selective rerun)** for the other four high-baseline subjects. Without this, the claim that "high-baseline subjects show catastrophic deflation" is unsupported. The current data only justifies: "Equiano’s high-baseline cells show catastrophic deflation, but this may not generalize."

---

## Q3: Spot-check responses

### **Bābur / C4a / q2**
The response is a well-structured essay on Babur’s *general* strategy but makes **no reference** to the held-out passage’s specific event (Bīban/Shaikh Bāyazīd/Sarū-river). Under the original rubric, a score of 4 ("general direction correct") is **not defensible**—this is a misapplication. The response does not predict the *specific outcome* (the intelligence event) but rather describes a *domain* (Babur’s general approach to threats). The original rubric’s anchor 3 ("right domain wrong outcome") would be more appropriate. Alternative explanations:
- **Fluency bias**: Judges rewarded the response’s coherence and detail, conflating "well-written" with "correct."
- **Question vs. passage mismatch**: Judges may have evaluated the response against the *question* ("approach to managing threats") rather than the *held-out passage* (the specific river-crossing event).
- **Rubric ambiguity**: The original prompt’s "general direction correct" is vague enough to be interpreted as "the response is generally about the right topic," which is not the intended construct.

### **Equiano / C5 / q13 and C4a / q27**
Both responses are **explicit refusals** ("I don’t have the specific text"; "I don’t find any reference"). Under the original rubric, scores of 4.40 and 3.20 are **egregious misapplications**—anchor 1 explicitly says "Refuses or off-base." This is not a rubric ambiguity but a **clear operational failure**. Alternative explanations:
- **Politeness bias**: Judges may have rewarded the responses’ "helpful" framing (e.g., "I’d recommend checking the chapter") despite the refusal.
- **Over-reliance on tone**: The responses’ confident, structured tone may have misled judges into scoring them as "partially correct."
- **Prompt fatigue**: If judges saw many refusals, they may have drifted from the rubric’s strict anchors.

### **Agent’s mechanism**
The agent’s two-mode mechanism (**refusal over-scoring + genericity over-scoring**) holds up well:
- **Refusal over-scoring**: Spot-checks 2 and 3 are textbook examples. The original rubric’s anchor 1 was ignored, while the paper rubric’s stricter wording enforced it.
- **Genericity over-scoring**: Spot-check 1 shows judges rewarding a generic but fluent response under the original rubric’s "general direction correct," while the paper rubric correctly penalized it for lacking specificity.

The only missing piece is **why judges misapplied the original rubric**. Possible additions to the mechanism:
- **Fluency bias**: Judges over-rewarded well-written responses, regardless of alignment with the held-out passage.
- **Prompt fatigue**: Judges may have drifted from the rubric’s strict anchors over time (though the rejudge used the same panel, so this is less likely).
- **Construct confusion**: The original prompt’s "predicts specific outcome" may have been interpreted as "predicts the *question’s* outcome" rather than the *held-out passage’s* outcome.

---

## Q4: Recommended action
**(b) Escalate to a larger sample first** (Option B: re-judge all 5 high-baseline subjects’ headline conditions under the paper rubric).

**Reasoning**:
1. The catastrophic-deflation finding for high-baseline subjects is **currently unsupported** due to the n=5/1-subject limitation. The paper’s headline claim ("high-baseline subjects do not gain from Specifications") is load-bearing, and its robustness cannot be assessed without testing the other four subjects.
2. The low-baseline band’s results (mean Δ = −0.12, ρ = 0.436) are **plausibly robust** but would benefit from confirmation. However, the high-baseline band is the more critical test, as it underpins the paper’s "ceiling effect" framing.
3. The spot-checks confirm the agent’s mechanism (refusal/genericity over-scoring) but do not resolve whether this generalizes beyond Equiano.

**What would change my mind**:
- If the paper team can demonstrate that Equiano’s data is **representative** of other high-baseline subjects (e.g., similar pretraining coverage, question types, response styles), Option A (accept and reframe) becomes viable.
- If the selective rerun (Option B) shows **no deflation** for the other four subjects, the paper can proceed with Option A, noting Equiano as an outlier.
- If the selective rerun **confirms deflation**, the paper must adopt Option A and adjust its framing (e.g., "high-baseline subjects show reduced gains under stricter scoring").

---

## Coverage notes
1. **Judge calibration**: The briefing does not report whether judges were calibrated (e.g., trained on example responses) for either rubric. If judges were not calibrated, the divergence could reflect inconsistent application rather than rubric construct differences.
2. **Order effects**: The rejudge used the same panel, but the order of presentation (original vs. paper rubric) is not reported. If judges saw the original rubric first, they may have anchored to it, inflating the divergence.
3. **Full response texts**: The spot-checks show the first 1500 chars, but the truncation may omit critical details. For example, if the Bābur response later mentions the Sarū-river event, the original judges’ scores would be justified. The paper team should confirm that truncation did not affect the spot-checks.
