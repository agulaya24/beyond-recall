# C96 §4.1 Reframing — Collective Review

_Date: 2026-04-28_
_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_

## Reviewer 1 — OpenAI (gpt-5.5-2026-04-23)

## 1. Is the proposed §4.1 reframing fair?

Broadly, yes—but the bolded claim is slightly ahead of the evidence as stated.

The per-question breakdown **does support** the idea that, among low-baseline subjects, the spec often changes the kind of answer the model gives: **193/351 questions, or 55.0%, cross upward at least one integer anchor**, versus **24/351, or 6.8%, crossing downward**. It also supports the claim that some of these are not small nudges: **64/351, or 18.2%, move upward by at least two anchors**, and **20/351, or 5.7%, move upward by at least three anchors**.

What it does **not by itself prove** is the comparative part: “low-baseline subjects have more such questions to be changed.” To support that literally, the reader needs either:

- the same upward-crossing rates for mid/high-baseline subjects, or  
- a per-subject plot/table showing upward-crossing rate versus C5 baseline, or  
- a statement that low-baseline batteries contain more low-anchor C5 responses, creating more room for upward crossings.

Right now, the evidence shown is strong for: “low-baseline subjects have many such questions.” It is weaker for: “low-baseline subjects have more such questions than high-baseline subjects.”

I would tighten the bolded sentence to avoid overclaiming:

> **The gradient is best read as a question-level opportunity pattern: in the low-baseline batteries, many questions start in low rubric bands, and the spec often moves those answers into a higher band.**

If the author has comparable high-baseline crossing rates, then the stronger claim is fine, but it should be backed with those numbers.

Also, “questions where the spec changes the category of answer” should be narrowed to **upward** category changes. Otherwise the 24 downward crossings are being silently swept into the same phrase.

## 2. Is the per-question breakdown in the proposed prose adequate?

No. The proposed prose gestures at the right phenomenon, but it does not surface the key quantitative fact: **how often** the category change happens. Since the author wants the body to carry the interpretive reframing, the body needs at least one compact numerical sentence.

I would include something like:

> Among the 351 questions for the nine low-baseline subjects, C4a moved the mean rating into a higher integer rubric band on **193 questions, or 55%**, and into a lower band on **24 questions, or 7%**. Most upward moves were one-band shifts, but **64 questions, or 18%, crossed two or more bands**, and **20 questions, or 6%, crossed three or more bands**.

That sentence does a lot of work. It defines the phenomenon as integer-band movement, gives the numerator/denominator, distinguishes upward from downward, and preserves the “low-frequency but high-magnitude” point without hiding the base rate.

If space is tight, the minimum inline numbers should be:

- **351 low-baseline questions**
- **55% upward anchor crossing**
- **7% downward anchor crossing**
- **18% multi-anchor upward jumps, ≥2 anchors**
- **6% extreme upward jumps, ≥3 anchors**

The per-subject range, **25.6% to 74.4% upward-crossing**, is also useful if the author wants to avoid implying uniformity across low-baseline subjects. I would include it if §4.1 is making a subject-level interpretive claim.

A small table in the body would be even better than prose if this is central to the reframing. For example:

| Outcome, C4a vs C5 | Low-baseline questions |
|---|---:|
| Upward integer-band crossing | 193/351, 55% |
| Downward integer-band crossing | 24/351, 7% |
| No integer-band crossing | 134/351, 38% |
| Upward ≥2 bands | 64/351, 18% |
| Upward ≥3 bands | 20/351, 6% |

That table is simple enough for the body and would prevent the reader from having to infer the quantitative basis from Appendix B.7.

## 3. The §1.3 5–10% multi-anchor claim — keep, fix, or replace?

Recommend **(c): split into two numbers: 18% multi-anchor, 6% extreme.**

The current wording is not defensible as written. It says “multi-anchor jumps” and then gives examples including **1→3**, which is a two-anchor jump. But **1→3 alone is 12.3%**, already above the claimed 5–10% range. The literal bundle “1→3, 1→4, 2→5” is also odd because **2→5 never occurs** in the provided data, while **1→5 does occur** but is not listed.

The clean replacement is:

> In the low-baseline batteries, upward multi-anchor jumps are not rare: **18% of questions move up by two or more rubric bands**, while more extreme jumps of **three or more bands occur in about 6%**.

This preserves both ideas:

- multi-anchor improvements are meaningfully present, not just anecdotal;
- the most dramatic “no idea” to substantive answer cases are lower-frequency but high-magnitude.

If the author wants to keep the “5–10%” phrase, it must be explicitly tied to **extreme jumps**, not multi-anchor jumps. But I would avoid “5–10%” when the exact value is available. Say **6%**.

Also, qualify the population: these numbers are for **low-baseline questions**, not necessarily “the spec conditions” overall unless the same rate holds across the full sample.

## 4. Is “categories” the right word?

“Categories” is understandable only if the reader has just been reminded that the rubric has integer anchor bands. Otherwise it is too vague. Use a parenthetical pointer.

Exact replacement:

> **on questions where the spec moves the answer into a higher integer rubric band—e.g., from refusal/irrelevant to generic, or from generic to partially subject-specific—low-baseline subjects have more such upward-crossing opportunities.**

If the author wants a shorter version:

> **on questions where the spec moves the answer into a higher integer rubric band, low-baseline subjects have more such opportunities.**

But again, I would prefer “opportunities” or “observed upward crossings” over “questions to be changed” unless the comparative high-baseline evidence is shown.

## 5. Anything else that misleads or overstates?

Yes, several phrases should be tightened.

First:

> “The gradient is the residue of those question-level wins”

This is rhetorically strong but too causal and too totalizing. The gradient reflects upward wins, downward movements, no-move cases, baseline distribution, and averaging. Better:

> “The gradient appears to be driven less by uniform subject-level convergence than by the accumulation of question-level upward crossings, especially in low-baseline batteries.”

Second:

> “on recall-style questions where the model otherwise refuses or guesses off-base”

This is plausible, but if not all upward crossings are recall-style or refusal-like, avoid making that sound universal. Better:

> “especially on recall-style questions where C5 often refuses, gives a generic answer, or guesses off-base…”

Third:

> “from ‘no idea’ to ‘specific, grounded, correct’”

“Correct” may overstate what the rubric measures unless correctness is independently judged. The anchors describe behavioral-pattern capture relative to ground truth, not necessarily factual correctness in a simple sense. Safer:

> “from refusal or generic response to a specific answer grounded in the subject’s observed pattern.”

Fourth:

> “not ‘the spec lifts low-baseline subjects more than high-baseline ones’”

This is too strong as a rejection, because the aggregate means may in fact show larger lifts for low-baseline subjects. The problem is not that the statement is false; it is that the **−0.96 slope should not be treated as clean evidence for it**. Better:

> “not simply ‘the spec lifts low-baseline subjects more,’ as if the −0.96 slope independently established that fact…”

Finally, the proposed prose should explicitly say that the original Δ-on-C5 slope is not very informative because the level regression is flat and the permutation null produces similar slopes. That can be one plain sentence:

> Because Δ subtracts C5, a near −1 slope can arise even when after-spec scores are roughly unrelated to baseline; here, the direct C4a-on-C5 slope is near zero.

That is still accessible and keeps the statistical sanity check tied to the substantive reframing.

---

## Reviewer 2 — Google (gemini-2.5-pro)

Excellent. This is a classic and important statistical issue to handle with care. The author is right to move away from a simple interpretation of the change-score regression. The proposed reframing is a strong step in the right direction. Here is a detailed fairness check and set of recommendations.

***

## 1. Is the proposed §4.1 reframing fair?

Yes, the reframing is fair and represents a significant improvement in scientific communication. It correctly identifies the headline slope as misleading and replaces a statistical abstraction with a more plausible, mechanistic explanation grounded in the data-generating process.

The bolded claim—**"on the questions where the spec changes the category of answer, low-baseline subjects have more such questions to be changed"**—is strongly supported by the logic of the experimental setup and the provided data.

**Where it is well-supported:**
*   **Logical necessity:** A "low-baseline" subject is, by definition, one for whom the model produces answers that score low on the 1-5 rubric (e.g., many 1s and 2s). A "high-baseline" subject has answers that already score high (e.g., many 3s and 4s). There is simply more mathematical "room" for a score to cross an integer anchor upward when it starts at 1 or 2 than when it starts at 4. The claim is a direct consequence of how the subjects were stratified.
*   **Provided data:** The per-question breakdown for low-baseline subjects shows that a majority of questions (55%) are indeed "changed" upward. This demonstrates that the mechanism the author describes is not a rare event but the dominant mode of action for this subgroup.

**Where it could be tightened:**
The phrase "more such questions to be changed" is slightly ambiguous. It could mean a higher absolute number of questions, a higher proportion of questions, or simply more *opportunity* for change. The latter is the most accurate. I would tighten the bolded claim to be more precise about this mechanism of opportunity.

**Suggested tightening for the bolded sentence:**

> It is: **low-baseline subjects begin with a larger pool of questions at lower performance anchors, creating more opportunity for the spec to drive category-changing improvements.**

This version replaces the slightly vague "more such questions to be changed" with the more precise "larger pool of questions at lower performance anchors" and "more opportunity." This directly links the "low-baseline" status to the observed effect.

## 2. Is the per-question breakdown in the proposed prose adequate?

No, the current prose is not adequate. It makes qualitative claims ("some questions show large lifts") where quantitative data is available and essential. The author's instinct to surface these numbers is correct; they are the most compelling evidence for the new framing. Hiding them in an appendix undermines the argument at the exact moment it is being made.

The prose should be updated to include the key statistics directly. A full table is unnecessary for §4.1, but sentence-level numbers are critical.

**The specific numbers that should appear inline are:**
1.  **The overall rate of upward change:** The 55% of questions that crossed an anchor upward is a powerful, top-line summary.
2.  **The rate of high-magnitude change:** The 18% of questions that were "multi-anchor" jumps (≥2) directly supports the narrative of "high-magnitude wins" and shows the effect is not just marginal tweaking.

**Suggested replacement text for the second paragraph:**

> **What is actually happening.** The 2.46 number that summarizes after-spec performance is a per-subject average. It masks significant per-question drama, which is sharpest on low-baseline subjects. For this group, the spec changed the answer's quality category on over half of all questions (**55% crossed an integer anchor upward**). Many of these were not small nudges: nearly one-in-five questions (**18%**) jumped by two or more anchors. On recall-style questions where the model otherwise refuses (score 1), the spec often produces multi-anchor jumps to "specific, grounded, correct" answers (details in §4.4.2). Conversely, on questions where even the full source corpus would not help, the spec does little. The misleading gradient is the aggregate residue of these question-level wins: low-baseline subjects have more questions starting from the bottom, so their per-subject mean has further to climb.

This revision is more concrete, credible, and impactful.

## 3. The §1.3 5-10% multi-anchor claim — keep, fix, or replace?

Fix it by choosing option **(c) split into two numbers: 18% multi-anchor, 6% extreme.**

**Justification:**
This is the most informative and honest approach.
*   It corrects the record by providing the accurate, and frankly more impressive, 18% figure for "multi-anchor" (≥2) jumps. This is a significant finding and should not be understated.
*   It preserves the author's original, valuable insight that there is a smaller class of truly "extreme" (≥3) jumps. The ~6% figure (5.7% rounded) captures this "low-frequency but high-magnitude" effect perfectly.

Presenting both numbers tells a richer story that aligns perfectly with the paper's thesis. It shows that meaningful lifts are common, and transformative lifts, while rarer, are a real and recurring phenomenon.

**Suggested replacement text for the §1.3 callout box:**

> Multi-anchor jumps (e.g., 1→3, 2→4) appear in roughly 18% of questions for low-baseline subjects on the spec conditions. A smaller subset of these are extreme, high-magnitude wins (e.g., 1→4), occurring in about 6% of cases. These are the specific, transformative gains the aggregate mean understates.

## 4. Is "categories" the right word?

"Categories" is acceptable but not ideal. It relies on the reader to connect the word to the integer score bands, which they may not do automatically. Given that this concept is the linchpin of the entire reframing, clarity is paramount. A brief parenthetical pointer is the best solution.

**Suggested replacement text:**

> "...on the questions where the spec changes the **category of answer (i.e., crosses an integer threshold on the 1-5 rating scale)**, low-baseline subjects have more such questions to be changed."

Or, if you adopt the tightening from my answer to Question 1:

> "...creating more opportunity for the spec to drive **category-changing improvements (i.e., upward jumps across integer score thresholds)**."

This small addition removes all ambiguity at minimal cost to readability.

## 5. Anything else that misleads or overstates?

The proposed prose is very strong and largely avoids overstatement. It does an admirable job of adding nuance. Here are two minor points for consideration:

1.  **"The gradient is the residue..."**: "Residue" is a slightly technical term. While it works for a statistical audience, a simpler word like "result" or "byproduct" might be more accessible. However, "residue" does nicely capture the sense of being "what's left over" after the real action has happened elsewhere, so this is a stylistic choice. I would lean toward keeping it but flag it for the author's consideration.

2.  **Implicit comparison:** The entire argument rests on a comparison between low-baseline and high-baseline subjects. However, the prose only provides data and description for the low-baseline subjects. It would be slightly more complete to add a single clause acknowledging the high-baseline side of the coin. For example, after describing the wins for low-baseline subjects, the author could add: "...while high-baseline subjects, having fewer such low-scoring questions to begin with, show a correspondingly smaller aggregate lift." This closes the logical loop and makes the explanation for the negative slope even more watertight. It preempts the reader's question: "So what happens with the high-baseline subjects?"
