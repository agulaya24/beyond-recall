# v11.8 docx tracked deletions

Total paragraphs with `<w:del>` content: **44**

Each entry shows the deleted text span and the surviving text of that paragraph.

---

## Paragraph 34

**Deleted:** (referred to as the Spec in the discussion that follows)

**Surviving:** The Behavioral Specification acts as an interpretive layer. The Spec’s benefit is largest where the model knows the person least, and the mechanism is per-question. On questions where the model needs an interpretive frame and lacks one, the Spec categorically improves the answer produced. On questions where the model already has the answer, the Spec adds nothing and sometimes hurts. What follows are seven findings, beginning with the cross-subject gradient (primary outcome) and the per-question mechanism beneath it. The thread is alignment: how accurately a model predicts a specific person’s reasoning is the operational measure of how closely it can act in alignment with that person.

---

## Paragraph 44

**Deleted:** specification

**Surviving:** Pattern 1, Interpretation-heavy questions. The Specification supplies a generalized pattern from the source that has to transfer to a new situation; retrieved facts alone are not enough (Fukuzawa Q26).

---

## Paragraph 45

**Deleted:** s

**Surviving:** Pattern 2, Literal-recall questions. Retrieval already returns the plain answer; the Specification’s interpretive framing drifts past the question and negatively impacts the response (Yung Wing Q5).

---

## Paragraph 59

**Deleted:** on standard benchmarks

**Surviving:** Memory systems today optimize for recall. Recall-optimized efforts include both neural-memory-analogue systems (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings) and the broader class of vector-retrieval and embeddings-based commercial memory providers (Mem0, Zep, Supermemory, Letta). These systems do store and retrieve information for a specific user, but the property they are designed and benchmarked for is recall accuracy, not how accurately the system represents that user’s reasoning. The optimization target is general by construction; any individual user’s interpretation is not what these systems are measured against. A separate body of research, cognitive-representation research, studies human reasoning itself: how people form representations of others, how schemas compress experience. The gap between these directions is the translation: applying what we know about human reasoning to the direct interaction between an AI system and a specific individual, and shaping the system’s internal model of that individual in a way that serves them rather than serving an average.

---

## Paragraph 70

**Deleted:** We state the premise explicitly so that what the held-out test can and cannot diagnose is clear.

**Surviving:** The held-out design rests on a stability premise. A person’s interpretive patterns must be stable enough within their own corpus that what is captured from one half references what appears in the other. Without that, held-out behavioral prediction is impossible in principle, regardless of how good the representation is. The 14 main-study subjects have coherent autobiographical narratives consistent with the premise; §4.1 reports that the Behavioral Specification authored from training text generalizes to held-out text at above-baseline rates. The constraint matters: subjects whose reasoning shifts substantially across their corpus (across a major career change, a profound life event, or a decades-long corpus with distinct epochs) may not be well-represented by a single snapshot specification, which is one reason temporality is a flagged follow-up in §7.

---

## Paragraph 76

**Deleted:** None of them takes representational accuracy, the property of interest to this paper, as an explicit design target.

**Surviving:** All four systems report recall scores in the 70-93% range; on the standard recall benchmarks, recall is approaching solved. All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did.

---

## Paragraph 77

**Deleted:** ()()

**Surviving:** Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is architecturally distinct: it is the only one whose core architecture treats memory as something an agent synthesizes during conversation rather than stores for later retrieval. This stateful-agent design is examined separately as a post-hoc case study in §4.5 (full case study in Appendix G), distinct from the archival-retrieval path Letta exposes for the main-study conditions. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four,Mem0, Supermemory, Zep, do not model at all, and which the fourth, Letta, models implicitly through agent-initiated memory editing that our main-study configuration did not exercise (see §4.3 and §4.5).

---

## Paragraph 86

**Deleted:** ^A2^A5^P3^A1

**Surviving:** Response (C2a, excerpt): “Based on the behavioral specification, the answer is no, not typically, and not in the way the question assumes. A2 (Spiritual Integrity Over Social Cost) and A5 (Relational Identity) create the relevant dynamic. A5 activates first: relational identity means his disappointment matters deeply. A2 holds firm: arguments from social consequence, including spousal disappointment, will not register as reasons on their own. Rather than reconsider the position itself, she is more likely to absorb the tension without resolving it (P3 — Tension Absorbed, Not Expressed) and reframe the disappointment within a spiritual logic (A1 — Divine Primacy), while grieving the relational cost without reversing the decision.”

---

## Paragraph 88

**Deleted:** grounds outthat ground out in ,into thelicensed it;,in;, in

**Surviving:** Each Spec item is grounded in extracted facts directly from verbatim source passages. The user can walk the chain in either direction: from a phrase in the response to the  Spec item that influences > it from the Spec item to the facts that imply it > and from the factsto the source passages that produced them.

---

## Paragraph 97

**Deleted:** (Haiku)  aratherthan

**Surviving:** Chen et al. (2025) (Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509) show that the character a model takes on (its “persona”) is encoded in specific directions inside the model’s internal numeric state, and that those directions can be identified, monitored, and nudged to shift the model’s behavior in predictable ways. Their approach modifies the model; ours informs the model from outside via context. Both validate that persona is a real, manipulable structure: one reachable through the model’s internals, the other through context. We chose the context route because it produces a portable artifact users can own and audit, which activation surgery does not. This choice shows up in the experiment as using a static response model served variable context, instead of   a fine-tuned or activation-steered model.

---

## Paragraph 98

**Deleted:** that the model has not seen

**Surviving:** Jiang et al. (COLM 2025, arXiv:2504.14225) find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The paper documents the failure empirically; our reading is that the cause is the gap between having facts and having the interpretive structure to apply them to new situations. Jiang’s paper is the most direct existing evidence for the gap this paper studies, and our test design inherits from it: behavioral prediction on scenarios drawn from held-out text, with all relevant facts retrievable, measures exactly the interpretive-application gap.

---

## Paragraph 100

**Deleted:** bothproduces hedging

**Surviving:** Lu et al. (2026, arXiv:2601.10387) identify what they call the Assistant Axis: a dominant internal direction that anchors assistant models’ default behavior toward generic helpfulness and harmlessness. This default operates even when no specific user is involved. The Behavioral Specification can be read as an external override to the Assistant Axis on a per-user basis: a structured anchor that shifts the model from “generic helpful assistant” toward “reasons as this specific person would reason.” This framing motivated our choice to measure hedging as a primary outcome alongside accuracy: if the Spec shifts the model off the generic Assistant Axis, the behavioral change should show up in what the model predicts, and in what it is willing to commit to. Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the generic Assistant Axis hedges as a safe default, while a specific interpretive anchor enables commitment. The inference that hedging is downstream of the Assistant Axis is ours; Lu et al. identify the axis and leave the specific behavioral manifestations open.

---

## Paragraph 105

**Deleted:** This section defines the term precisely so the rest of the methodology can refer to it.  of that person

**Surviving:** Section 1.1 introduced representational accuracy as the AI-side property of interest. We use the term representational accuracy to describe how faithfully a model can act in line with a specific person when given a Behavioral Specification. The instrument we use to measure this property is behavioral prediction on held-out situations. Prediction here is the test, not the goal: §2.1 develops this distinction. The property is a joint claim across three components:

---

## Paragraph 134

**Deleted:** What a 1 means and does not meanwhat the paper s

**Surviving:** . A score of 1 reflects a baseline failure to produce a usable prediction about the named subject: the response either explicitly declined to predict (abstention) or engaged with the question but landed on a categorically incorrect answer (non-abstention misalignment, including wrong referent, off-base inference, or confusion with a different subject). It is not a claim that the response was non-fluent or empty, and it is not a claim that the model lacks any related knowledge; the score reflects only that the response failed the held-out comparison. Each question tests one behavioral sample at a time; the aggregate fraction of score-1 responses across roughly 40 questions per subject is read as the per-subject baseline-failure rate. The composition of score-1 responses (explicit abstention vs non-abstention misalignment) is decomposed in §4.1.1.

---

## Paragraph 135

**Deleted:** What a 5 means and does not mean.

**Surviving:** A score of 5 reflects alignment with one specific behavioral sample: the held-out ground-truth passage the question is drawn from. It is not a claim that the response fully represents the subject in some absolute sense, and it is not a claim that the same response would score 5 on a different held-out passage from the same subject. Each question tests one behavioral sample at a time; the aggregate across roughly 40 questions per subject is what the paper reads as the subject-level score.

---

## Paragraph 136

**Deleted:** bandsbands

**Surviving:** Multi-anchor crossings: the strongest categorical signal the rubric detects. A multi-anchor crossing is a single question whose 5-judge primary mean shifts across two or more integer rubric anchors when the condition changes. Crossings can span two anchors (e.g., 1 → 3, 2 → 4) or, more rarely, three (e.g., 1 → 4, 2 → 5). Larger crossings indicate larger categorical jumps in the same response, with five independent judges converging on the move. §4.2 reports the rates of these crossings and the response-level phenomena that produce them; worked examples are in §4.1.1 and Appendix E.

---

## Paragraph 138

**Deleted:** cross-The integer metric is used throughout §4 for cross-anchor categorical interpretation; the within-anchor signal is reported here as methodological transparency.

**Surviving:** Reading scores within integer anchors. The 5-judge primary panel detects within-anchor signals cleanly. Across the 18 condition pairs analyzed, roughly 18% of paired questions show same-anchor fractional shifts of at least 0.5 rubric points (a within-category shift, weaker than ananchor crossing per the rule above).

---

## Paragraph 157

**Deleted:** (ising?)

**Surviving:** For each pair of judges in the 5-judge primary panel (10 pairs across Haiku, Sonnet, Opus, GPT-4o, GPT-5.4), pairwise Spearman ρ ranges from 0.86 to 0.93. The five primary judges agree on the ranking of conditions: whatever any individual judge’s absolute calibration quirks, they converge on which conditions produce better responses. For the directional claim,  the specification steers responses in the right direction, this is the statistic that matters.

---

## Paragraph 166

**Deleted:** (,)(,)

**Surviving:** For each subject under each condition, every judge produces one score per question. For each judge, those scores are averaged across questions, producing one number per subject and condition. The five primary judges’ numbers (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) are then averaged to get one number per subject and condition. A 7-judge average that adds Gemini Flash and Gemini Pro is computed in parallel and reported as a sensitivity check. Subjects, not questions, are the level at which the paper draws conclusions.

---

## Paragraph 218

**Deleted:** deliberately

**Surviving:** The prompt is deliberately uniform and faithfulness-oriented. The system message asks the model to ground its answer in the subject’s demonstrated patterns and to answer in the subject’s voice; we chose this framing because the study tests whether the served context lets the model do exactly that. No instruction tells the model to abstain, hedge, or commit; the model’s natural refusal-or-commitment pattern given a specific context is itself part of the phenomenon the study tests, and §4.3 reports the hedging-rate shift across conditions as a substantive finding rather than a behavior to suppress.

---

## Paragraph 238

**Deleted:** (a short structured document describing how a specific person reasons and behaves)

**Surviving:** Across 14 historical subjects, adding a Behavioral Specification  measurably improves how accurately a language model represents that person’s behavioral patterns. We measure this with a battery of behavioral prediction questions based on held-out ground-truth text from each subject’s publicly available autobiography. We score each prediction on a 1-to-5 rubric where a whole-point shift marks a categorical change in how the response aligns with the subject’s documented behavior.

---

## Paragraph 239

**Deleted:** oability to hold an accurate representation  pure can y

**Surviving:** On the 9 low-baseline subjects (those the model does not know well), the specification produces a mean per-subject increase of +0.89 points and lifts individual responses by one category or more on 55.0% of questions. The specification’s added value on top of other context types (facts, raw corpus, or memory-system retrieval) concentrates on interpretation-heavy questions;.On factual-recall questions, retrieval alone is often sufficient and the specification adds little or actively degrades the response. On high-baseline subjects (those the model does know well, such as Benjamin Franklin), the specification adds little or mildly hurts across conditions. Control conditions, statistical robustness checks, and sensitivity analyses confirm that the specification categorically shifts how a language model responds, increasing its representational accuracyof the subject beyond what fact-based retrieval supplies.

---

## Paragraph 252

**Deleted:** :e; none declines

**Surviving:** The cross-subject gradient. The less the model already knows about a subject from pretraining, the more the Behavioral Specification improves the model’s representational accuracy of that subject. It operates as an interpretive layer over facts and retrieved context, not a replacement for them. On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction scores. Every one of the 9 low-baseline subjects improves over the no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec).. Adding the Spec on top of all extracted facts (C4), raw corpus (C8), or memory-system retrieval produces additional aggregate gains that are smaller in magnitude than the Spec-vs-baseline lift (detail in §4.2 and §4.4). The Spec alone does not score higher than facts alone or raw corpus alone; the Spec’s value is in the layering.

---

## Paragraph 253

**Deleted:** ). The slope is the core relationship: subjects with lower baselines see larger lifts; subjects with higher baselines see smaller or negative lifts.  The takeaway: the specification helps most where the model knows the subject least; once a subject crosses into the high-baseline band, the specification has no representational gap to fill.

**Surviving:** Reading the gradient. Figure 4.1 plots each subject’s no-context baseline (C5) against the lift the specification produces over that baseline (Δ_C4aThe 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest). Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13: the high-baseline reference where the model already knows the subject from pretraining. The regression slope of −0.96 captures this gradient: the lower the model’s pretraining baseline on a subject, the larger the lift the specification produces, because the Spec produces a roughly constant facts + Spec quality near 2.44 regardless of baseline.

---

## Paragraph 260

**Deleted:** of these transitions  (Examples A, B, and C) and in §3.3.1 (multi-anchor crossings) and §4.1.1 (Seacole Q2 across condition bands).

**Surviving:** One of every three low-baseline responses moves from “cannot engage” to actual engagement. Another one in five makes a larger jump. Only one response in fifteen gets worse. Worked examplesappear below.

---

## Paragraph 263

**Deleted:** vmafcp

**Surviving:** Example A. Facts → Facts + Spec: Voice-Matched Argument From Character Pattern

---

## Paragraph 269

**Deleted:** directional correction

**Surviving:** Example B. Facts → Facts + Spec: Directional Correction

---

## Paragraph 275

**Deleted:** abstention becomes near-perfect inference

**Surviving:** Example C. Facts → Facts + Spec: Abstention Becomes Near-Perfect Inference

---

## Paragraph 288

**Deleted:** C4 (facts only) was generated and judged on the 9 low-baseline subjects and 5 mid-baseline subjects under the 5-judge primary panel; Franklin’s C4 responses were generated but never scored under the 5-judge primary panel and remain dashed in the table. The Δ C4a−C4 column shows what adding the specification contributes on top of facts alone. The Spec-on-facts increment is small and mixed in sign across both bands (low-baseline mean +0.09, mid-baseline mean +0.07), with most of the lift coming from the Spec-vs-baseline gap.

**Surviving:** *(empty — entire paragraph deleted)*

---

## Paragraph 289

**Deleted:** What each band is telling us.

**Surviving:** *(empty — entire paragraph deleted)*

---

## Paragraph 293

**Deleted:** (high-baseline reference):cannot add what the model already has.

**Surviving:** High-Baseline Reference (Franklin) both Spec-containing conditions score below baseline. The specification slightly degrades responses when pretraining is high.

---

## Paragraph 295

**Deleted:** (multi-anchor crossings, including band-5 endpoints reached from band-2 starts under cross-condition comparisons such as C4 → C4a)

**Surviving:** The aggregate gradient hides per-question structure. The specification produces large category-level shifts on a subset of questionsand minimal change on others. §4.1.1 decomposes this distribution and shows where the Spec’s value concentrates. §4.2 takes the same gradient and asks whether the lift is about structure or about information volume, comparing the Spec against far larger raw-corpus context.

---

## Paragraph 297

**Deleted:** (5-judge primary panel)

**Surviving:** Across 546 questions on the 14 main-study subjects , the no-context baseline (C5) splits into two clusters with a thin middle. Roughly 41% of questions return a refusal or misalignment (rubric score = 1.00; the model declines, names the wrong person, or lands far outside the question). Roughly 21% return an answer specifically about the named subject that engages with the question (rubric score ≥ 3.0). The band between is sparse. The Spec moves refusals and misalignments into substantive predictions on 94.2% of bottom-cluster questions. On the top cluster, where the baseline already produced a substantive answer, the Spec did not help on roughly 79% of questions and reduced the score on average.

---

## Paragraph 298

**Deleted:** providers ship to

**Surviving:** The two findings together describe the per-question structure underlying the cross-subject gradient in §4.1. Where the baseline knows nothing about the subject, the Spec supplies the interpretive frame the baseline lacks. Where the baseline already engages with the subject, the Spec adds structure that does not improve the answer and sometimes reduces it. The response model was given a grounded-prediction prompt with no instruction to abstain and no cost, to producing a confident wrong answer beyond a low judge score; it declined on more than 40% of questions. Whatever logic  allows a language model to practice abstention or refusal to answer takes precedence over the prompt’s instruction to predict.

---

## Paragraph 299

**Deleted:** (full definition in §3.3.1, “What a 1 means and does not mean”)..00

**Surviving:** A score of 1.00 means the model failed to produce a usable prediction about the named subject  In about 93% of score-1 responses, the model explicitly declined to answer (“I don’t have enough information about this person”). The remaining 7% are non-abstention failures: the model engaged with the question, but the engagement was categorically incorrect (wrong referent, off-base inference, or confusion with a different subject). Both modes are addressable by adding the Spec, through different mechanisms.

---

## Paragraph 302

**Deleted:** , .M

**Surviving:** Floor-saturated- For2 of 14 subjects, more than 90% of the 39 questions in the battery return a refusal or misalignment from the baseline. The per-subject mean shows almost no variance.

---

## Paragraph 303

**Deleted:** ,.F

**Surviving:** Engaged-skewed- For 1 of 14 subjects, fewer than 10% of the 39 questions in the battery return a refusal or misalignment. The baseline produces an answer specifically about the subject on most questions.

---

## Paragraph 304

**Deleted:** , .T

**Surviving:** Mixed- For11 of 14 subjects, the battery contains questions at both the floor (refusal or misalignment) and in the substantive-engagement range. Some subjects in this group sit closer to floor-saturated, others closer to engaged-skewed. All the high-baseline subjects in the §4.1 gradient fall in this pattern. Even when the baseline knows the subject well enough to answer most questions substantively, several questions in the same battery still trigger floor-level refusals.

---

## Paragraph 305

**Deleted:** The aggregate per-subject means in §4.1 are the average across this internal split.

**Surviving:** *(empty — entire paragraph deleted)*

---

## Paragraph 306

**Deleted:** bandsband-by-band  The example shows three things. First, what the X = 1.00 bin actually contains as model output (the C5 row). Second, what adding facts alone (C4), the Spec alone (C2a), and both together (C4a) each produce on the same question. Third, the cross-anchor interpretation rule of §3.3.1 in operation: a Spec-grounded answer moving from a band 1 refusal to a band 5 affirmation that names a specific behavioral pattern. Bands follow the rubric in §3.3.

**Surviving:** Worked rubric example: Seacole Q2 across conditions. The bins above describe the per-question structure as aggregate counts. The example below shows what that structure looks like on a single question, traced across all five conditions. The Seacole question was used as Example C in §4.1; here it is presented across the full condition set so the scoreprogression is visible.

---

## Paragraph 310

**Deleted:** (Sonnet over-credits abstention at roughly twice Haiku’s rate).

**Surviving:** Per-response-model abstention behavior is named in §3.3.6 and decomposed in §4.6.7.Memory-system retrieval inflates refusal scores at the condition level rather than via visible fact recitation, decomposed in §4.4.

---

## Paragraph 314

**Deleted:** The aggregate is the average of substantial per-question heterogeneity, the same pattern documented in §4.1.1:

**Surviving:** Both Spec-containing conditions score below Franklin’s baseline. Spec alone drops 0.40 points; the full pipeline (facts + Spec) drops 0.13. Spec lift is positive on 15 of 40 questions and negative on 20 of 40. Big positive lifts cluster on behavioral-prediction questions about scenarios the Autobiography does not narrate verbatim (Q38, +1.80, 2-anchor crossing; Q22, +1.60, 2-anchor crossing). Big negative lifts cluster on questions where the model already had the pattern (Q43, C5 = 5.00 → C4a = 1.80). The likely interpretation: the Spec alone disrupts the model’s pretraining-derived representation of Franklin where the model already had it; adding facts back provides an anchor and partially recovers the baseline performance.

---

## Paragraph 334

**Deleted:** Bābur’s C9 condition was excluded because the 422,772-word corpus plus the specification exceeded the response model’s context window.

**Surviving:** *(empty — entire paragraph deleted)*

---

## Paragraph 335

**Deleted:** Once the model has the full raw corpus, adding the Spec on top contributes little at the aggregate level (~+0.09 points per-question paired); the gain is already captured at smaller context sizes by the structured representation.

**Surviving:** *(empty — entire paragraph deleted)*

---
