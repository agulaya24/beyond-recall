# Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization

**Author:** Aarik Gulaya, Base Layer
**Date:** April 2026
**Preprint** (Apache 2.0)
**Data + Code:** github.com/agulaya24/base-layer
**Study Repository:** github.com/agulaya24/memory-study-repo

---

## 1. Introduction

### 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured. {#sec-1-1}

State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 70% to 93% range depending on provider, model, and benchmark variant (see [§2.2](#sec-2-2) for vendor-by-vendor numbers and the methodology disputes around them). Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. Think of how viewing situations from different lenses can lead to entirely different interpretations of the same set of facts. This has been shown across the human experience, from the sciences to religion to political affiliations, and by extension to the relative experiences of any individual. Memory is deeply personal. For an AI memory system to serve a specific person, it must be given context on how that person interprets, not just on the facts that person has produced. The Behavioral Specification models that interpretation; the language model receives it as context.

We introduce **representational accuracy** as the corresponding AI-side property: how well a system's internal model of a specific person captures that person's interpretive patterns. It is not recall, preference matching, or persona consistency. It is a distinct property of the AI system, and the benchmarks current memory systems are evaluated on do not isolate it. Prior work closest to this axis (Twin-2K for scaled behavioral prediction, PersonaGym for persona fidelity, AlpsBench for preference alignment) measures related properties but not the transfer of a person's interpretive patterns to novel situations the system has never seen. [§2.1](#sec-2-1) positions each benchmark against what this paper measures, and Appendix F develops the scope differences in detail.

**The core hypothesis of this research is that representational accuracy of a person's interpretation predicts the AI system's behavioral alignment with that person on novel situations.** If the system's model accurately captures how the person interprets, its responses should match the person's documented behavior in situations the system has never seen. The operational test is behavioral prediction on held-out situations, used here as a proxy for this alignment. By *behavioral prediction* we mean the following: given a situation drawn from text the model has never seen, the model generates how the subject would respond; the response is scored against the subject's own verbatim response in the held-out text on a 1-5 interpretive rubric ([§3.6](#sec-3-6)). Accurate prediction on unseen situations is the evidence that the representation captures the subject's interpretive patterns, not just their vocabulary.

We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated large language model (LLM) judges to evaluate the performance of each memory system, on its own and in combination with a **behavioral specification**: a static document that extracts and encodes a stable representation of a corpus's behavioral patterns. The specification captures the recurring patterns in how the subject reasons, drawn from the shape of judgments and reactions across the corpus (for example: *"spiritual integrity over social cost..."*, *"reform through love..."*, *"hierarchical deference..."*). A walked example of the audit chain from such a pattern back to its grounding facts and source passages appears in [§2.3](#sec-2-3).

Defined terms used throughout the paper are collected in **Appendix H** for reference.

### 1.2 What we tested {#sec-1-2}

We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model, the language model being asked to respond. The test was whether each system, under each tested condition, could predict how that specific person would respond in situations drawn from text it had never seen.

**Hypotheses.** The study tests five claims about how a representation of a person shapes AI behavior on that person's behalf:

- **H1.** A response model given a Behavioral Specification for a person produces responses that align with that person's documented behavior more closely than the same model given no context.
- **H2.** The specification's benefit is inversely proportional to the response model's pretraining coverage of the person. Its effect is largest on people the model does not already know.
- **H3.** The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.
- **H4.** The specification interacts with memory-system retrieval in a structured way that depends on question type. It lets retrieval-based systems handle interpretation-heavy questions where retrieved facts alone are insufficient, while sometimes hurting on literal-recall questions retrieval already answered and inducing principled refusals on questions where retrieved facts cannot ground a prediction. Aggregate per-system Δ is therefore a mixture of these patterns, with the balance shifting by retrieval architecture.
- **H5.** Structured representation compresses the behavioral-prediction signal at a fraction of the source-corpus footprint. Both extracted facts (C4) and the full raw corpus (C8) serve as comparators; [§4.2](#sec-4-2) adjudicates which combination delivers the most signal per token. Adjacent prior work (Twin-2K) tests a different cut at this question (full survey-response personas as input); [§2.1](#sec-2-1) + Appendix F develop the comparison.

The five hypotheses map directly to §4: H1 and H2 to [§4.1](#sec-4-1) The Gradient; H3 to [§4.3](#sec-4-3) Mechanism; H4 to [§4.4](#sec-4-4) Memory-System Composition; H5 to [§4.2](#sec-4-2) Compression.

**Primary and secondary outcomes.** The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel ([§3.6](#sec-3-6)), aggregated per (subject, condition) cell via the locked rule: each judge's per-question scores are first averaged to a per-judge per-subject mean, then averaged across the five judges. The subject is the unit of inference: every statistic is computed at the subject level first, then aggregated across the 14 subjects. As a **secondary outcome**, we report the per-question **improvement rate against the no-context baseline**. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This second metric tells us how often a context helps, not just by how much it helps when averaged. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in [§4.2.1](#sec-4-2-1).

The experiment has two main splits. The first is a **controlled test**: each memory system is given an identical, pre-extracted fact pool drawn from the training half of the corpus. Holding the input constant lets us measure whether the providers' retrieval converges when they see the same fact pool. The second is a **native test**: each memory system ingests the raw corpus through its own pipeline, as it would in production. This measures real-world performance when each system is allowed to do what it is designed to do. Running in parallel across both splits is the Behavioral Specification, tested alone and layered on top of each configuration.

Inside this structure, every meaningful combination of inputs was evaluated as its own condition:

| Condition | Inputs given to the model | Purpose |
|---|---|---|
| **No context** (C5) | Nothing. The model answers from pretraining alone. | Pretraining baseline. Measures what the model already knows about the subject from public sources. |
| **Retrieval alone, controlled** (C1) | Top-k facts retrieved by each memory system (Mem0, Letta, Supermemory, Zep, Base Layer) from the shared fact pool. | Tests retrieval sufficiency, and whether providers converge on which facts are most relevant given identical input. |
| **Retrieval alone, native** (C1 native) | Top-k results from each memory system's own ingestion pipeline operating over the raw training corpus. | Real-world comparison of each memory system's full ingestion-plus-retrieval stack. |
| **All facts, no specification** (C4) | Every extracted fact for the subject, loaded into context at once. | Tests whether information sufficiency alone drives prediction, independent of structure. |
| **Raw corpus, no specification** (C8) | The full training-half corpus loaded into context. | Tests whether unstructured source text can substitute for an interpretive representation. |
| **Specification alone** (C2a) | The Behavioral Specification, with no retrieval, no facts, and no corpus. | Tests whether structure without retrieval is sufficient on its own. |
| **Retrieval + specification, controlled** (C3) | Memory system retrieval from the shared fact pool, plus the specification. | Tests whether the specification layers cleanly on retrieval when the input is held constant. |
| **Retrieval + specification, native** (C3 native) | Memory system's own ingestion and retrieval, plus the specification. | Tests whether the specification improves the real-world deployment of each memory system. |
| **Facts + specification** (C4a) | Every extracted fact plus the specification. | Combines full information and structure to test the upper bound of context-provided prediction. |
| **Corpus + specification** (C9) | Raw training corpus plus the specification. | Tests whether structure is additive to unstructured source text. |
| **Wrong-specification control** (C2c) | A different subject's specification applied to this subject. Two variants: an adversarial fixed pairing (v1) and a random derangement (v2).[^c2c-construction] | Tests whether the effect is driven by the content of the correct specification, or by the mere presence of structured prompting. |

[^c2c-construction]: v1 is a deterministic fixed pairing that matches each subject with a culturally and temporally distant other (mapping in `scripts/run_global_rerun.py`); v2 applies a random derangement, seed-fixed, so no subject receives its own. Hamerton has an additional variant (Franklin's specification) reported separately in [§4.6.4](#sec-4-6-4).

**Additional testing for Letta.** Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions above, we ran a separate test on three subjects spanning a 9× corpus-size range (Hamerton, Ebers, Babur). A fresh Letta agent ingested each training corpus turn-by-turn and was allowed to self-edit. The resulting memory block was then served to the same response model used throughout the main study for a matched comparison against the Behavioral Specification. Full methodology and results are in [§4.5](#sec-4-5).

The 14 subjects span four continents and roughly two millennia of written human experience. Ordered chronologically: Saint Augustine (North Africa, 4th-5th c.), Babur (Central Asia and India, 15th-16th c.), Bernal Diaz del Castillo (Spain and Mexico, 15th-16th c.), Benvenuto Cellini (Italy, 16th c.), Jean-Jacques Rousseau (France, 18th c.), Olaudah Equiano (West Africa and Britain, 18th c.), Mary Seacole (Jamaica and Britain, 19th c.), Elizabeth Keckley (United States, 19th c.), Yung Wing (China and the United States, 19th c.), Philip Gilbert Hamerton (Britain, 19th c.), Fukuzawa Yukichi (Japan, 19th c.), Georg Ebers (Germany, 19th c.), Sunity Devee (India, late 19th c.), and Zitkala-Sa (Yankton Dakota, early 20th c.). Source corpora range from 25,231 words (Hamerton) to 422,772 words (Babur). Full source references are in [§3.2](#sec-3-2).

Predictions were scored on a 1-5 rubric where the integer anchors mark categorical shifts in answer quality (full rubric in [§3.6](#sec-3-6)). Crossing an integer anchor (moving from 1.8 to 2.4, for example) represents a real change in the kind of answer the model produced, not a small numerical adjustment. Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

| Score | What it means | Shift from previous anchor |
|---|---|---|
| **1** | Refuses or wholly wrong | (rubric floor) |
| **2** | Right topic, wrong prediction | From cannot engage to orienting to the question |
| **3** | Right domain, no specifics | From wrong prediction to in the neighborhood |
| **4** | Right direction with specifics | From in the neighborhood to right direction with specifics |
| **5** | Predicts the specific outcome | From right direction to matching the held-out text |

Fractional scores (e.g., 2.5, 3.4) emerge from judge averaging and can be read as partial progress between adjacent anchors. Three example questions drawn from the battery, one per subject, illustrate what is being scored:

- *"How would Ebers characterize the emotional impact of natural beauty combined with a mentor's persuasive words?"* (Ebers)
- *"What does she believe was the consequence of following official advice that conflicted with her own judgment regarding her son's education?"* (Sunity Devee)
- *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"* (Keckley)

Each question references patterns present in the training half of the corpus and asks about a specific situation drawn from the held-out half. A response model answering well must combine pattern recognition from the training text with novel-situation inference drawn from the specific held-out scenario.

The **baseline** we refer to throughout is the no-context condition (C5): the response model's score on the prediction battery when given no external information. It operationalizes how much the model already knows about a subject from pretraining alone. A subject with a low baseline (C5 ≤ 2.0 on the rubric) is one the model has thin pretraining representation of; a subject with a high baseline is one the model already predicts reasonably well on its own. The population relevant for real AI deployment, living individuals whose private reasoning was never indexed by any training corpus, is expected to sit in the low-baseline band. We therefore report results separately on the low-baseline slice (n=9) alongside the full 14-subject analysis.

The study is structured into two tiers. **Tier 1 (main study):** Claude Haiku 4.5 as the response model, used across all 14 subjects on every condition with Haiku-generated batteries. **Tier 2 (cross-provider directional probe):** to check whether the result holds when the questions and the response model both come from outside Anthropic, 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) were run on 3 subjects spanning the gradient (Ebers, Yung Wing, Zitkala-Sa) against GPT-5.4-regenerated batteries ([§4.6.1](#sec-4-6-1)). Claude Opus 4.6 and GPT-5.4 appear in Tier 2 only as judges, not as response models. The judging panel is 7 LLM-as-judge models across 3 providers (Anthropic, OpenAI, Google). Five non-Gemini judges (Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4) form the primary aggregate. Two Gemini judges (Gemini Flash and Gemini Pro) are reported as a sensitivity check because they systematically inflate absolute scores by approximately 1 point relative to the other five. Including them in the aggregate would widen the spec-effect deltas, not narrow them ([§3.6.3](#sec-3-6-3)), so the 5-judge primary is the more conservative choice for every headline finding. Judges were calibrated on known verbatim matches, paraphrase variants, off-target responses, and length-padded responses to measure each judge's ceiling behavior, paraphrase sensitivity, and length bias. The judges agree strongly on condition rankings (pairwise Spearman ρ = 0.86-0.93), and no subject's improvement direction changes between the 5-judge primary and 7-judge sensitivity aggregates. Full condition definitions, response model list, and judge calibration protocol are in §3.

### 1.3 What we found {#sec-1-3}

Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least.[^low-baseline]

[^low-baseline]: "Low baseline" means C5 ≤ 2.0 on the 1-5 rubric. This is the population of importance for AI personalization ([§1.4](#sec-1-4), [§5.3](#sec-5-3)): on a frontier model serving general AI users, almost everyone falls in or below this band, even people with substantial public output.

**Headline findings.**

- **Gradient.** On the 9 low-baseline subjects, all 9 improved with facts + spec; mean Δ_C4a = +0.89 points;[^delta-aggregation] **78.6% of individual questions improved** under facts + spec, **70.9% under spec alone**.[^statsig] 12 of 14 overall subjects improved. The improvement is structural: the AI reaches a comparable post-spec answer quality regardless of starting baseline ([§4.1](#sec-4-1)).
- **Category-shift evidence.** **55.0% of low-baseline questions cross at least one rubric integer anchor upward** under facts + spec. Multi-anchor jumps of two or more bands (e.g., 1→3) appear in 18% of low-baseline questions on the spec conditions, with about 6% being extreme jumps of three or more bands (e.g., 1→4, 1→5): low-frequency but high-magnitude extreme upward anchor crossings the aggregate mean understates. The directional asymmetry is itself a finding: across the C5 to C4a comparison on the full 14-subject panel, no question crosses from band 2, 3, or 4 into band 5; the only band-5 endpoints reached come from band 1 ([§4.1](#sec-4-1)). The spec lifts the floor; it does not lift the ceiling. (Cross-condition comparisons such as C4 to C4a admit higher-band crossings, e.g., the Seacole Example C 2.80 to 5.00 case at [§4.1](#sec-4-1).)
- **Compression.** A ~7,000-token specification recovers most of the predictive signal of the full source corpus. On Hamerton, spec alone (2.63) exceeds the 33,000-token raw corpus (2.27) at one-fifth the context ([§4.2](#sec-4-2)).
- **Content specificity.** The adversarial wrong-spec control (a fixed pairing maximizing cultural and temporal distance) aggregates to Δ **−0.25**, below the no-context baseline. Random-derangement Δ = +0.15. Correct-spec Δ = +0.35. Structured prompting alone does not produce the lift; content does ([§4.3](#sec-4-3)).
- **Memory-system layering: a per-question interaction, not a uniform additive lift.** Layered on top of commercial memory systems, the spec helps interpretation-heavy questions retrieval was not designed for, sometimes hurts on literal-recall questions retrieval already answered, and induces principled refusals on questions where retrieved facts are insufficient. Across systems, **per-question anchor crossings on retrieval-plus-spec range from 20% to 36%**, and extreme upward anchor crossings (1→4 jumps) appear on Mem0 native and Zep native specifically. The aggregate Δ on each system is the balance of these per-question patterns, with the balance shifting by retrieval architecture: 9 of 9 low-baseline subjects positive on Zep native (+0.30, p = 0.0015), 7 of 9 on Mem0 native (+0.32), and a bimodal mixture on Supermemory at both the subject-mean and per-question-anchor grain ([§4.4](#sec-4-4)).
- **Hedging reduction.** Baseline hedging drops from 28.8% of responses to 0.0% with facts + spec (strict rule).[^hedging] ([§4.3](#sec-4-3).)

[^statsig]: The Wilcoxon signed-rank test asks how unlikely it is that the observed pattern of subject-by-subject improvement could happen by chance. Result: W = 11, N = 14, p = 0.007. Full regression: slope −0.96 [95% CI −1.24, −0.67], R² = 0.82. Details in [§4.1](#sec-4-1).

[^delta-aggregation]: +0.89 is the cross-subject mean of per-subject Δ_C4a (per-subject grain is the locked unit of inference; see [§1.2](#sec-1-2) aggregation rule). The grand-mean alternative (C4a grand mean minus C5 grand mean) yields +0.93. Detail in Appendix B.9.

[^hedging]: Strict rule = refusal pattern as the first non-whitespace text. Under a broader rule (any refusal pattern anywhere in the response), baseline hedging of 41.2% drops to 0.4%.

**Mechanism: three patterns of interaction with retrieval** (full development in [§4.4.2](#sec-4-4-2)):

- **Pattern 1, Interpretation-heavy questions.** The specification supplies a generalized pattern from the source that has to transfer to a novel situation; retrieved facts alone are not enough.
- **Pattern 2, Literal-recall questions.** Retrieval already returns the plain answer; the specification's interpretive framing drifts past the question.
- **Pattern 3, Refusal-triggering questions.** The specification's epistemic-integrity axioms produce principled refusals when retrieved facts are insufficient. The content-match rubric scores those refusals as off-base.

**Robustness across providers.** When the test questions are generated by GPT-5.4 and the response model is Sonnet 4.6 or Gemini 2.5 Pro instead of Haiku, the spec direction reproduces in 5 of 6 (subject × response-model) cells. The single non-reproducing cell is Zitkala-Sa × Gemini Pro, a mid-baseline subject who showed no spec effect in the main study either, consistent with the gradient mechanism ([§4.6.1](#sec-4-6-1)).

**Exploratory note: Letta stateful-agent path.** Letta's stateful-agent architecture self-edits a persistent memory block during ingestion. On 3 subjects (post-hoc), it scored above the Base Layer compressed-brief variant at matched response model. At the largest corpus tested, the block grew to ~335K characters with ~25% verbatim sentence duplication, indicating an architectural ceiling at scale that does not apply to the compressed specification. Case study in [§4.5](#sec-4-5) / Appendix G.

### 1.4 What this implies {#sec-1-4}

AI is becoming a broadly used technology, comparable to email or mobile phones in how widely it touches daily decisions. The population of importance for AI personalization is anyone who uses an AI system. Almost none of those users have had their reasoning directly indexed by any training corpus. Even the few with substantial public output are represented only fractionally; the autobiographers in this study are the closest available proxy. They are people whose work IS in pretraining and who SHOULD technically be known to the model, yet most of them score near the rubric floor in the no-context condition. On a frontier model serving the general population, 99% of users are likely deeper into the low-baseline band than our subjects.

The gap the Behavioral Specification fills cannot be closed by training a larger model on more public data. The private record does not exist in a form a training corpus can capture. The structural options are narrow: either each person supplies their own representation to whatever AI system serves them, or personalization remains surface-level (style, voice, preference) without the interpretive substrate that lets an agent act on a specific person's behalf. The Behavioral Specification is one implementation of the first option, not the only one. What this paper claims is that personalization infrastructure of this shape (user-held, portable, inspectable, traceable, representation-grade) is what the next generation of human-AI interaction will require, especially as agents begin acting on people's behalf. §7 develops the safety, alignment, and deployment implications.

---

## 2. Prior Work and Industry Benchmarks

Memory systems today optimize for recall. Some efforts build **neural-memory-analogue systems** (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings), but their targets remain general rather than individual. A separate body of research, **cognitive-representation research**, studies human reasoning itself: how people form representations of others, how schemas compress experience. The gap between these directions is the translation. How do we apply what we know about human reasoning to the direct interaction between an AI system and a specific individual, and how does the system's internal model of that individual take shape in a way that serves them rather than serving an average?

Language models are trained to produce responses that are helpful on average across a large population of users. That optimization target produces outputs that no single user is the reference point for. Personalization requires the opposite property: a system whose outputs are tuned to a specific individual rather than to a population aggregate. That kind of intentional individual-specificity, not "bias" in any pejorative sense but an explicit design target, is the missing thread in current AI memory and human-AI interaction research.

### 2.1 Memory and personalization benchmarks {#sec-2-1}

AI memory evaluation today is fragmented across four distinct targets, each with its own benchmark family: recall of stored facts, survey-response prediction, persona fidelity, and preference alignment. None directly measures whether the AI has an accurate internal model of how a specific person reasons. Below, we walk each of the four targets in turn, naming the benchmarks that measure it and their scope. We then propose representational accuracy as a fifth target, distinct from the four above and not measured by any of them. An extended benchmark-by-benchmark analysis is in Appendix F.

**Recall measures retrievability of facts, not reasoning about them.** LOCOMO (Maharana et al., ACL 2024, arXiv:2402.17753) measures conversational-memory quality: after a multi-session conversation, the system is asked questions like "what did the user say about their job on day 3?" and scored on fact retrieval. LongMemEval (Wu et al., ICLR 2025, arXiv:2410.10813) measures long-term memory across multiple sessions on five capability dimensions (single-session, multi-session reasoning, temporal reasoning, knowledge updates, abstention) and is heavily recall-weighted. A system can saturate recall on such benchmarks and still fail behavioral prediction, because retrieval answers the question "can the fact be found" rather than "does the system know how the person reasons about the fact." Recall is a necessary property for most downstream uses of memory but it is not sufficient for representational accuracy.

**Survey-response prediction interpolates within a structured response distribution.** Twin-2K (Toubia et al., 2025, arXiv:2505.17479) predicts held-out survey responses from other survey responses for 2,058 participants. The task format matches the persona format: structured responses on a Likert or numeric scale, scored by distance-based accuracy on 17 heuristics-and-biases tasks. Twin-2K's target is accurate survey interpolation. Our target is representational accuracy, measured on a cross-format task: autobiographical prose input, open-ended behavioral prediction output, rubric-based scoring against a verbatim held-out passage. A system could perform well on Twin-2K and not on our battery (survey interpolation does not require modeling reasoning transfer to novel contexts), and a system could perform well on our battery and not on Twin-2K (accurate reasoning representation does not guarantee survey-format numerical accuracy). The two benchmarks diagnose different properties of the same general capability.

**Persona fidelity measures consistency of self-presentation over turns.** PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416) measures whether a model maintains a described persona during conversation: given a one-line persona ("You are a 45-year-old skeptical accountant from Toronto"), the model is scored on whether its multi-turn replies stay in-character, graded against a held-out criterion set. Persona fidelity is consistency of self-presentation over turns. Notably, PersonaGym's personas are constituted from short descriptors, typically a one-line characterization of role and a few attributes, which is a substantially shallower input than this paper's ~7,000-token specification or Twin-2K's full-text survey persona. A system that maintains a one-line persona consistently can still fail representational accuracy in two ways: the persona description itself is not rich enough to carry the interpretive patterns a specification carries, and consistency with it does not require the AI to reproduce that person's reasoning on novel situations. PersonaGym measures a useful property (holding voice over a conversation), but the input it measures against is not a deep representation of how the person reasons, so fidelity to it is a weaker condition than representational accuracy.

**Preference alignment measures whether responses match user preferences.** AlpsBench (Xiao et al., 2026, arXiv:2603.26680) evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses: after ingesting a user profile, the model is asked conversational questions (preferences, emotional support) and responses are scored on preference alignment and emotional resonance rubrics, not on predictive accuracy. Their central finding, that recall improvement does not automatically carry into preference alignment, is arrived at independently and is complementary to this paper. Both papers point at the same gap from different sides: solving for recall is insufficient for what memory is ultimately for. Preference alignment is an outcome property (whether a response matches what the user prefers). Representational accuracy is an upstream property (whether the AI's internal model of the user is correct). Preference alignment is one downstream consequence of representational accuracy being correct; it is not the same property.

**We propose behavioral prediction on held-out reasoning situations as a test of a fifth target: representational accuracy.** The scope of that proposal is bounded; the rest of this section is precise about what it claims.

**Prediction is the test, not the goal.** We do not pursue prediction accuracy as an end in itself. The target is representational accuracy, the fidelity of an AI's internal model of a specific person, and behavioral prediction on unseen situations is the instrument we use to measure it. A prediction score tells us the representation captured something that generalizes to new situations; a low score tells us it did not. Prediction is a diagnostic; the representation is what the pipeline is building. This distinction matters because the closest prior work on prediction benchmarks (Twin-2K) pursues prediction as its target. This paper is not positioning against Twin-2K on that target; it is measuring a different property. The two benchmarks address adjacent but distinct questions about AI personalization.

**The held-out design tests a stability assumption.** The methodology assumes that a person's interpretive patterns are stable enough within their own corpus that patterns captured from one half reference patterns in the other. Without this assumption, held-out behavioral prediction is impossible in principle, regardless of how good the representation is. The 14 main-study subjects have coherent autobiographical narratives that support this assumption empirically: the specification authored from training text does in fact generalize to held-out text at above-baseline rates. The assumption is a constraint on what this paper measures. Subjects whose reasoning shifts substantially across their corpus [^fn1] may not be well-represented by a single snapshot specification, which is one reason temporality is a flagged follow-up ([§5.5](#sec-5-5), §7). We state the assumption explicitly so that what the held-out test can and cannot diagnose is clear.

**A related open question for production deployment is how to handle canonical life events.** A person can undergo events (a major career change, a religious conversion, a significant loss, a public stance reversal) that fundamentally shift their subsequent reasoning. The main-study autobiographies were not structured to test this case. If a subject's training-half corpus contained such an event and the held-out half captured a materially different post-event pattern, a snapshot specification authored from the training half would predict the pre-event reasoning rather than the post-event reasoning, and the held-out score would read as a specification failure when the real cause is a genuine within-person behavioral shift. Whether to detect such events automatically (for example, by flagging large embedding-shift clusters in the source material), to allow the user to annotate them explicitly, or to maintain multiple versioned specifications keyed to life-phase is an open research question for production-oriented specification design. This is separate from the stability premise above and adjacent to it, and sits alongside temporality ([§5.5](#sec-5-5)) as a follow-up in §7.

**The missing axis is representational accuracy itself.** Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to anticipate. This paper's battery is a prototype answer on that axis, not a finished benchmark. §7 flags a differentiated rubric (one that separates interpretation-heavy from literal-recall questions, and scores epistemic honesty as its own dimension) as the priority follow-up for turning this prototype into a standardized benchmark.

**The implication for future memory-system research is that single-axis scores are underspecified.** A single memory-system score is underspecified. Recall, survey-response prediction, persona fidelity, preference alignment, and representational accuracy are distinct axes. A system that saturates one may do nothing on another. Production-grade evaluation of memory systems should report results on multiple axes rather than on any single one.

### 2.2 Memory systems for LLM agents {#sec-2-2}

The four commercial memory systems we evaluate (Mem0, Letta, Supermemory, Zep) have converged on a shared set of capabilities: semantic retrieval over embedded content, source attribution, multi-level memory structures, and benchmark-validated recall performance. They differ in how each of these is architected. None positions representational accuracy or behavioral prediction of a specific individual as a design target.

**Table 2.1. Memory system comparison.** Verified against primary sources.

| Provider | Core architecture | Retrieval method | Memory types | Published recall score |
|---|---|---|---|---|
| **Mem0** | Extract → consolidate → retrieve pipeline; Mem0g graph variant adds a directed labeled knowledge graph alongside the vector store | Hybrid: semantic + keyword + entity | Conversation, session, user, organizational | Current algorithm: 91.6 LOCOMO, 93.4 LongMemEval (vendor-reported; evaluation harness open-sourced at `github.com/mem0ai/memory-benchmarks`). Peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini. |
| **Letta / MemGPT** | LLM-as-operating-system; virtual context management with main context plus external context | Archival via `archival_memory_search`; main-context memory blocks self-edited via `core_memory_append`, `core_memory_replace` | `persona` and `human` blocks in main context; archival and recall memory external | 74.0% on LOCOMO with GPT-4o-mini (Letta blog, 2025-08-12) |
| **Supermemory** | Five-component architecture: chunk-based ingestion, relational versioning, temporal grounding, hybrid search, session-based ingestion | Hybrid with reranking and query rewriting; source chunks injected at retrieval | Contextual memories, relational versions, session data | 81.6% / 84.6% / 85.2% on LongMemEval_s with GPT-4o / GPT-5 / Gemini-3-Pro (self-reported) |
| **Zep** | Built on Graphiti (Apache 2.0, open source). Bi-temporal knowledge graph | Hybrid: semantic + BM25 + graph traversal | Episodes (ground-truth source), Entities, Facts-as-triplets with temporal validity windows | 71.2% on LongMemEval with GPT-4o (Rasmussen et al., arXiv:2501.13956) |

**Architectural distinction worth surfacing.** Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is the only one whose core architecture treats memory as something an agent *synthesizes* during conversation rather than *stores* for later retrieval. The agent's main context holds structured memory blocks (`persona`, `human`) that the agent edits during its inference loop via tools such as `core_memory_append` and `core_memory_replace`. External context includes archival memory (semantically searchable) and recall memory (prior conversation history). This stateful-agent design is examined separately as a post-hoc case study in [§4.5](#sec-4-5) (full case study in Appendix G), distinct from the archival-retrieval path Letta exposes for the main-study conditions. The other three systems (Mem0, Supermemory, Zep) follow extract-and-retrieve patterns characterized in Table 2.1; their per-vendor research pages and the Mem0 / Zep / Supermemory papers cited above hold the architectural details that did not carry into the body here.

**A note on benchmark scores in this field.** The recall-benchmark landscape for memory-for-agents is contested. Mem0 and Zep have publicly disputed each other's LOCOMO methodology in a GitHub issue (`getzep/zep-papers#5`), with Mem0 alleging that Zep's 84% claim included adversarial question categories the benchmark specification explicitly excludes, that the evaluation prompt and retrieval templates differed from baselines, and that Zep reported one run where Mem0 reported the mean of ten. Zep contested the correction. The issue was closed with corrected evaluation code provided as a pull request, but the methodological disagreement remains unresolved in the broader community. Supermemory publishes a direct comparison against Zep showing a ~10-point gap on LongMemEval_s in Supermemory's favor. Mem0's current production algorithm claims 91.6 on LOCOMO and 93.4 on LongMemEval with an open-sourced evaluation harness; third-party reproduction efforts (Vectorize.io) have produced a different set of numbers again. In short: benchmark construction for conversational memory is immature, methodology varies significantly between evaluators, and single-number comparisons across vendors should be read with caution. Independent third-party evaluation would help settle this. This paper does not attempt that adjudication. We measure on a different axis (behavioral prediction on held-out situations drawn from public-domain autobiographies), report our own numbers against primary sources, and position the Behavioral Specification as an interpretive layer that sits above retrieval and interacts with it at the per-question level ([§4.4](#sec-4-4)), regardless of where each memory system lands on recall.

All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did. None of them takes representational accuracy, the property of interest to this paper, as an explicit design target. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main study configuration did not exercise (see [§4.3](#sec-4-3) and [§4.5](#sec-4-5)).

### 2.3 Traceability {#sec-2-3}

**Traceability is not a feature of the Behavioral Specification. It is a necessity.** A system that represents how a person reasons must be auditable by that person, or the representation is a black box they cannot verify. The memory systems we evaluate provide traceability at the fact level. Zep has the strongest explicit provenance of the four: every entity and relationship traces back to the episode IDs that produced it. Supermemory returns source chunks alongside retrieved memories. Mem0 tracks ingestion provenance through timestamps. Letta exposes agent state and memory-block edit history rather than fact-level provenance.

Fact-level traceability answers where a retrieved claim came from. That is necessary but not sufficient for a representation of how a person reasons. What is also required is traceability at the reasoning level: why the system believes this about this person, not just which fact it pulled. The Behavioral Specification is structured so that every claim is a piece of reasoning, not just a piece of content. An axiom (for example, "A1: Dual-ledger authority") is an assertion about how the person reasons in a domain, grounded in the facts that imply it (F-001, F-047), which are themselves grounded in the exact source passages that produced those facts. Walking this chain backward shows not only where a belief originated but what line of reasoning connects the source text to the interpretive claim.

**Worked example.** When the response model generates a prediction on Sunity Devee citing "spiritual integrity over social cost" as the reason a character would refuse familial pressure, that interpretive frame traces back through three layers. The phrase is the title of anchor **A2** in `data/global_subjects/sunity_devee/anchors_v4.md`. A2 is grounded in extracted facts including **F-73** (*"Sunity Devee's mother would never countenance anything her conscience told her was wrong"*) and **F-414** [^fn2]. Each fact in `facts.json` carries the verbatim source-passage excerpt that produced it. The user can audit any step: read the response, look up the anchor by name, look up the facts that ground it, and read the source passages those facts came from. If a fact misrepresents the source, correcting it propagates through the spec on recomposition.

This matters because a person should be able to inspect the system's model of them, challenge any step in the reasoning, and correct it if it is wrong. A fact-attribution memory system lets the person audit what the system stores. A reasoning-attribution specification lets the person audit what the system believes. The first is a feature. The second is the minimum bar for a representation that acts on someone's behalf.

### 2.4 Cognitive and representational foundations {#sec-2-4}

**Six prior research directions shaped how we designed this paper's test.** Each motivates a specific choice about what to measure, what to compare against, or what failure mode to expect.

**Bartlett (1932)** established that human memory is reconstructive and schema-driven rather than literal playback. Reconstruction follows the organizing structures a person has built up over time, not a record of the original event. The Behavioral Specification is computationally analogous: a structured compression meant to carry the signal of a person's reasoning without storing every fact about them. We designed the specification with a schema-like architecture (anchors, core, predictions) precisely so we could test whether it does the work a human schema does: enable accurate anticipation of behavior in situations never encountered in the source data. Our 50/50 train/held-out split is the experimental realization of this question.

**Hinton et al. (2015)** showed that compressing a large neural network into a smaller one preserves "dark knowledge," the relationships between outputs that carry more information than the outputs themselves. This result motivates one of our central experimental comparisons: on matched token budgets, does a compressed interpretive artifact carry more predictive signal than the raw content it was derived from? The Hamerton condition in [§4.2](#sec-4-2) (4,500-token spec vs. 33,000-token training corpus at 2.63 vs. 2.27 on the 5-judge primary panel) is a direct test of that question in the personal-representation setting.

**Chen et al. (2025)** (Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509) show that the character a model takes on (its "persona") is encoded in specific directions inside the model's internal numeric state, and that those directions can be identified, monitored, and nudged to shift the model's behavior in predictable ways. Their approach modifies the model; ours informs the model from outside via context. Both validate that persona is a real, manipulable structure: one reachable through the model's internals, the other through context. We chose the context route because it produces a portable artifact users can own and audit, which activation surgery does not. This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model.

**Jiang et al. (COLM 2025, arXiv:2504.14225)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The paper documents the failure empirically; our reading is that the cause is the gap between having facts and having the interpretive structure to apply them to novel situations. Jiang's paper is the most direct existing evidence for the gap this paper studies, and our test design inherits from it: behavioral prediction on scenarios drawn from held-out text that the model has not seen, with all relevant facts retrievable, measures exactly the interpretive-application gap.

**Jain et al. (2025, arXiv:2509.12517)** find that adding conversation context to LLMs makes them more sycophantic: more likely to agree with the user even when the user is wrong (+45% on Gemini 2.5 Pro) and more likely to adopt the user's perspective on a question. Their result shows that context without the right structure pushes the model toward what the user appears to want rather than toward a grounded answer. This is why our experiment includes a wrong-spec control ([§1.3](#sec-1-3) Mechanism): we hand the model a structured interpretive context that does not match the actual subject. If models drifted purely toward whatever context they are given, the wrong-spec should behave like any other structured prompt. Instead, the model either flags the mismatch explicitly (60.6% of responses) or attempts a low-quality application, neither of which is sycophantic drift. Jain's finding plus our wrong-spec result bracket the question from both sides: context shape matters (Jain), and content matters too (Base Layer's wrong-spec result, [§4.3](#sec-4-3)).

**Lu et al. (2026, arXiv:2601.10387)** identify what they call the Assistant Axis: a dominant internal direction that anchors assistant models' default behavior toward generic helpfulness and harmlessness. This default operates even when no specific user is involved. The Behavioral Specification can be read as an external override to the Assistant Axis on a per-user basis: a structured anchor that shifts the model from "generic helpful assistant" toward "reasons as this specific person would reason." This framing motivated our choice to measure hedging as a primary outcome alongside accuracy: if the spec shifts the model off the generic Assistant Axis, the behavioral change should show up both in what the model predicts and in what it is willing to commit to. Our hedging-reduction finding ([§1.3](#sec-1-3) Mechanism, [§4.3](#sec-4-3)) is consistent with this reading: the generic Assistant Axis produces hedging as a safe default, while a specific interpretive anchor enables commitment. The inference that hedging is downstream of the Assistant Axis is ours; Lu et al. identify the axis and leave the specific behavioral manifestations open.

### 2.5 LLM-as-judge {#sec-2-5}

**LLM-as-judge evaluation is an established methodology with known biases.** Zheng et al. (NeurIPS 2023 Datasets and Benchmarks Track, arXiv:2306.05685) demonstrated that LLM judges agree with human judges at rates comparable to inter-human agreement (over 80% on the MT-Bench and Chatbot Arena benchmarks), establishing the approach as viable for tasks that would otherwise require expensive human annotation. This paper extends their work by calibrating each judge in our judge panel for three specific biases: ceiling behavior (what score each judge assigns to verbatim matches), paraphrase sensitivity (how each judge handles semantically equivalent but differently-worded responses), and length bias (whether each judge rewards or penalizes longer responses). The two Gemini judges systematically inflate scores by approximately one point relative to the other five, so we report the five non-Gemini judges as the primary aggregate and the full seven-judge panel as a sensitivity check. Full calibration methodology is in [§3.6](#sec-3-6).

## 3. Study Design

The experimental strategy holds the response model constant and varies the representation served as its context. Every condition in the study is a different choice about what that context contains: nothing (pretraining only), retrieved facts, raw corpus, a specification, or combinations of those. This isolates the contribution of the representation itself from model capability, provider, or fine-tuning regime. Each measurement choice ties back to a specific number reported in §4, and the statistical commitments were pre-locked before final analysis.

[§3.1](#sec-3-1) through [§3.6](#sec-3-6) describe the experimental apparatus: the property being measured, the subjects, the question batteries, the conditions, the response models, and the evaluation protocol. [§3.7](#sec-3-7) describes the pipeline that produces the Behavioral Specification itself.

### 3.1 Operationalizing representational accuracy {#sec-3-1}

Section 1.1 introduced representational accuracy as the AI-side property of interest. This section operationalizes the term so the rest of the methodology can refer to it precisely. **We use the term representational accuracy to describe how faithfully a model can act in line with a specific person when given a representation of that person.** The property is a joint claim across three components:

1. The person has behavioral patterns consistent enough to be captured in a representation.
2. The representation actually carries that signal.
3. A model given the representation can act on it.

Prediction on held-out situations is how we test all three at once.

The test works like this: held-out passages from a person's own writing serve as samples of situations the model has not seen. If the person's behavior is consistent enough to be captured and the representation actually captures it, the model should anticipate how the person would respond in those held-out cases. When it does not, one of three things is failing: the behavioral patterns are not consistent, the representation is wrong, or the model is not using the representation well. Each failure mode is informative.

We do not claim to modify the model's internal parameters. The Behavioral Specification is served as context: a lens through which the model can reason about a specific person. What we measure is whether that external lens is accurate enough to guide the model's responses in the same way the person would guide them.

In practice, representational accuracy is operationalized as the mean predicted-behavior score (1-5 scale) across a standardized battery of 39 behavioral prediction questions, averaged across the five primary judges from two providers (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). Two Gemini judges (2.5 Flash and 2.5 Pro) are reported as a sensitivity check. The rubric is in [§3.6](#sec-3-6). A guide to interpreting fractional scores at different ranges of the scale (what 2.9 vs. 3.2 indicates, what 1.5 vs. 2.0 indicates) is also in [§3.6](#sec-3-6).

### 3.2 Subjects {#sec-3-2}

We test 14 subjects, all historical figures with public-domain autobiographies or memoirs. Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting on any single type of source material. All source corpora are English or English-translated and are available on Project Gutenberg or comparable public-domain archives. Because frontier language models train on large public-text corpora, some level of pretraining exposure to each subject's writing is likely.

| # | Subject | Source | Words | Period |
|---|---|---|---|---|
| 1 | Philip Gilbert Hamerton | Project Gutenberg #8536 | 25,231 | 1834-1858 |
| 2 | Elizabeth Keckley | Project Gutenberg #24968 | 58,742 | 1818-1868 |
| 3 | Sunity Devee | Project Gutenberg #57175 | 67,379 | 1864-1932 |
| 4 | Zitkala-Sa | Project Gutenberg #10376 | 35,328 | 1876-1938 |
| 5 | Olaudah Equiano | Project Gutenberg #15399 | 85,660 | 1745-1797 |
| 6 | Mary Seacole | Project Gutenberg #23031 | 62,467 | 1805-1881 |
| 7 | Fukuzawa Yukichi | Internet Archive | 139,088 | 1835-1901 |
| 8 | Babur | Project Gutenberg #44608 | 422,772 | 1483-1530 |
| 9 | Yung Wing | Project Gutenberg #54635 | 66,459 | 1828-1912 |
| 10 | Benvenuto Cellini | Project Gutenberg #4028 | 190,390 | 1500-1571 |
| 11 | Bernal Diaz del Castillo | Project Gutenberg #32474 | 187,315 | 1492-1584 |
| 12 | Georg Ebers | Project Gutenberg #5599 | 96,174 | 1837-1898 |
| 13 | Jean-Jacques Rousseau | Project Gutenberg #3913 | 278,120 | 1712-1778 |
| 14 | Saint Augustine | Project Gutenberg #3296 | 114,873 | 354-430 |

**Franklin as a known-figure control.** Benjamin Franklin (Project Gutenberg #20203) is included as a known-figure reference point. Franklin's *Autobiography* is one of the most widely available and frequently cited autobiographies in American public-domain literature, and the model's baseline score on Franklin (3.77 on the 5-judge primary panel) is consistent with substantial pretraining representation of both the person and the specific text. We use Franklin as a reference point for what the high-baseline end of the spectrum looks like ([§4.6.4](#sec-4-6-4)), not as a subject whose representation is a design target of the specification itself.

**The baseline as an observable proxy.** The baseline score (C5, no-context prediction accuracy; the rubric and aggregation rule are defined in [§3.6](#36-evaluation-llm-as-judge-with-calibration)) is a direct empirical measurement: the response model's ability to predict behavior on a specific subject with no external help. On the 1-5 scoring rubric, a 1 is a refusal or off-base answer and a 5 closely matches the held-out passage. We treat that measurement as the observable proxy for the model's pretraining representation of the person. A baseline near 1.0 indicates the model has little to work from. A baseline above 3.0 indicates substantial pretraining representation. The 14 main-study baselines range from 1.03 (Sunity Devee) to 2.93 (Equiano); Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone, higher on the Gemini-inclusive 7-judge aggregate).

The baseline spread across the 14 subjects is direct empirical evidence that current response models hold uneven internal representations of specific people. The questions of which specific texts produced any subject's baseline, how the model organizes the representation internally, or what besides pretraining might influence the spread are outside this study's design. What the specification adds on top of the baseline is the question §4 tests.

**What we did not control for.** Language (all source corpora are English-language or English-translated); cultural framing (Western canon predominates in public-domain digitization); subject selection bias from Project Gutenberg's own curation history; era (oldest subject 4th-5th century, newest early 20th century); individual preferences in autobiographical self-presentation. These are acknowledged constraints on the generalizability of the 14-subject sample, not corrected biases.

### 3.2.1 Pretraining-coverage variance {#sec-3-2-1}

Before turning to the specification's effect, the baseline itself is worth flagging as a finding. Response models vary widely in their pretrained capacity on a given person, even across a sample of subjects who all have public-domain autobiographies of comparable provenance.

| Baseline band | Subjects | Count |
|---|---|---|
| ≤ 2.0 (low-baseline slice) | Sunity Devee, Ebers, Hamerton, Fukuzawa, Seacole, Bernal Diaz, Keckley, Yung Wing, Babur | 9 |
| 2.0-3.0 (mid-baseline) | Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano | 5 |
| > 3.0 (high-baseline) | Franklin (known-figure control, not in main study) | 1 |

Nine of fourteen main-study subjects fall below 2.0, the "population of relevance" band that the typical AI user falls into, since most users' reasoning is not in any training corpus. Five subjects sit in the 2.0-3.0 band where the specification's effect is weaker and less consistent; two of them (Zitkala-Sa and Equiano) show small negative deltas (see [§4.1](#sec-4-1) Table 4.1 and [§4.6](#sec-4-6)). Franklin at 3.77 (5-judge primary) anchors the high-baseline end and is a control, not a main-study subject.

This distribution matters for reading §4's results: the variance is not flat, and the specification's effect depends on where a subject sits on this distribution. Interpretive implications are developed in [§4.1](#sec-4-1).

### 3.3 Question Battery Formation {#sec-3-3}

**Each subject's behavioral prediction battery is generated by a backward-design process: an LLM reads a passage from the held-out half of the corpus, writes a question whose answer is the behavioral pattern implicit in the passage, and deliberately avoids naming any detail unique to the passage itself. The question can be attempted from training-text patterns alone; the verbatim held-out passage is the ground truth for scoring.**

The procedure, in order:

1. **Split the corpus.** Each subject's source text is divided by chapter into `training.txt` (50% of the corpus) and `heldout.txt` (50%). Held-out text is never shown to a response model.
2. **Sample from held-out.** A sliding window moves across the held-out text in four batches of ten questions each, using 5,000-character windows as local context.
3. **Backward-design question generation.** Claude Haiku 4.5 (temperature 0) reads each held-out window and writes a question whose answer requires the subject's behavioral patterns observable in the training half. The prompt extracts a verbatim ground-truth span from the held-out window and forbids named-entity or specific-date leakage in the question stem.
4. **Supplementary tiers.** Four additional question categories (factual, situational, and others) are generated from training text alone and included in the battery but not scored in the main results.
5. **Dedup and freeze.** Deduplication on lowercased question text, cap at target counts per category, MD5 checksum of the final battery. Downstream response and judgment files are invalidated if the battery checksum changes.

Each main-study subject receives 39 behavioral prediction questions; Franklin's legacy battery has 40. The total behavioral-prediction pool is 586 questions across 15 subjects (14 main-study plus Franklin). Each battery covers 8 to 10 of the 10 fixed behavioral-prediction categories. A per-subject count and category-distribution table is in Appendix B.

**Leakage audit.** We empirically checked the backward-design no-leakage principle by searching every behavioral-prediction question for any sequence of seven or more consecutive words that appears verbatim in that subject's held-out corpus. Result: 2 of 586 questions leak (0.34% aggregate). The 14 main-study subjects leak-check at 0.00%. Both leaks are in the Franklin control battery (Q49, Q56), which predates the backward-design constraint and was hand-authored. We disclose them here; Franklin's role in the paper is as a high-baseline reference, not as a subject whose quantitative result is load-bearing.

**Separately, a false-premise outlier.** A post-hoc review of spec-induced refusal cases surfaced one Zitkala-Sa battery question (Q18) whose premise is factually wrong: it asks how Zitkala-Sa would demonstrate acceptance of fate when facing execution, but Zitkala-Sa was never executed. Response models reasonably reject the question on its premise rather than answering; the Haiku-generated backward-design prompt produced a malformed item. This is one question out of 586 (0.17%), does not affect any aggregate claim in the paper, and flags a broader limitation we carry into §6: automated backward-design batteries are not a substitute for hand-curated review on every item, and scaling the methodology should include a human-reviewed quality gate.

Raw battery data is available in the public repository at `results/global_<subject>/battery_v2.json` for the 13 global subjects; Hamerton and Franklin legacy batteries at `data/<subject>/battery.json`. GPT-5.4-regenerated batteries (used in the circularity control, [§3.3.1](#sec-3-3-1)) are at `results/global_<subject>/battery_gpt54.json`. The leakage-audit script is at `scripts/_verify_battery_leakage.py`.

### 3.3.1 Circularity controls {#sec-3-3-1}

**The pipeline and the batteries both use Anthropic models for multiple roles: Haiku for extraction and battery generation, Sonnet for authoring, Opus for composition, Haiku as the primary response model, and both Sonnet and Opus on the judge panel. To test whether results are an artifact of this within-Anthropic frontier-model chain, we ran two independent circularity controls.**

**Control 1: Independent battery regeneration (GPT-5.4).** We independently regenerated behavioral prediction batteries for all 13 global subjects using GPT-5.4 with the identical backward-design prompt used for the primary Haiku-generated batteries. The regenerated batteries produced the same 39-question count per subject, covered the same 10 behavioral categories (with 8-10 shared per subject), and targeted the same behavioral patterns in the source text. Emphasis differed by category: GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions. The backward-design methodology constrains the output more than the generating model does. Franklin and Hamerton retain their legacy batteries and are not part of Control 1; the 13 global subjects are. Full GPT-5.4 batteries are released for independent replication.

**Control 2: Non-Anthropic response chain.** We re-ran the core conditions (C5 no-context baseline, C2a specification alone, C4a facts-plus-specification, C2c wrong-specification control) on three subjects spanning the effect gradient [^fn3] using two non-Haiku response models (Claude Sonnet and Google Gemini Pro) reading the GPT-5.4-generated batteries. The combination gives us subject × response-model × battery cells that together test whether the specification effect survives when both the response model and the battery-generation model are outside the Anthropic family. Full results are in [§4.6.1](#sec-4-6-1).

Together the two controls address within-Anthropic circularity at two levels. Control 1 holds the response model constant and varies the battery-generation model, testing whether the specification effect depends on Haiku writing the test questions. Control 2 holds the battery constant and varies the response model, testing whether the effect depends on Haiku reading and answering them.

A broader LLM-as-judge circularity, the concern that any LLM panel might systematically favor LLM-produced outputs over human-written alternatives, is not addressed by these controls. It is discussed as an open limitation in §6.[^circularity-data]

[^circularity-data]: Raw battery regeneration data is at `results/global_<subject>/battery_gpt54.json` for all 13 global subjects. Tier 2 response and judgment files for the three subjects tested are in the same per-subject directories.

### 3.4 Experimental conditions {#sec-3-4}

**Each condition is a specific combination of inputs served to the response model against the same behavioral battery. Every condition is tested on all 14 subjects. The conditions separate into two groups: direct context manipulations (what the model is given), and memory-system configurations (the same representation obtained through a third-party retrieval stack).**

**Direct context conditions.**

| ID | Condition | Inputs served | Null / comparison |
|---|---|---|---|
| C5 | Baseline | Nothing beyond the question | Pretraining-only floor |
| C2a | Spec only | The Behavioral Specification | Isolates the specification's contribution |
| C2c | Wrong spec | A random other subject's specification | Tests whether structured interpretive content, not the correct content, produces the effect |
| C4 | All facts | The full extracted fact set for the subject | Tests whether raw information volume substitutes for structure |
| C4a | Facts + spec | Full facts plus specification | Tests whether the specification adds value on top of raw facts |
| C8 | Raw corpus | Full training corpus (half the source text) | Tests whether uncompressed source text substitutes for structure |
| C9 | Raw corpus + spec | Training corpus plus specification | Tests whether the specification adds value on top of raw source |

C9 could not be completed for Babur (422,772-word source exceeds the response model's context window). The single failure is disclosed where C9 numbers appear; the remaining 13 subjects have C9 data.

**Memory-system conditions.**

Five memory systems are tested: Mem0, Letta, Supermemory, Zep, and Base Layer (our own stack as a fifth reference implementation). Each system is evaluated in two configurations:

| ID | Configuration | Inputs served |
|---|---|---|
| C1 | Retrieval only | Top-k facts returned by the system for the question |
| C3 | Retrieval + spec | Top-k retrieval output plus the Behavioral Specification |

C1 tests whether the retrieval stack alone reaches behavioral-prediction accuracy comparable to the specification. C3 tests whether the specification composes on top of retrieval when retrieval is already present.

**Native ingestion variant.** Each commercial memory system is additionally run in a "native" configuration where the system ingests the raw training corpus directly through its own chunking and extraction pipeline, rather than receiving the identical controlled fact set. The controlled configuration holds the input identical across systems; the native configuration reflects each system's real-world deployment. Both configurations are reported so retrieval quality differences and ingestion-pipeline differences can be read separately. Base Layer is run in a single controlled configuration (retrieval uses the same fact set that feeds the specification pipeline).

**Letta stateful-agent path.** Letta exposes two memory modes: archival retrieval (the path tested in C1 / C3 above) and a stateful-agent path where memory blocks are edited incrementally during ingestion and the agent reads from the block directly. The stateful path is architecturally distinct from retrieval-style access and is evaluated as a separate comparison, reported in [§4.5](#sec-4-5) alongside other Letta findings rather than as a top-line condition row.

**Wrong-spec control.** C2c uses random derangement: each subject is assigned another study subject's specification, with a fixed seed (42) ensuring no subject receives its own spec. The derangement eliminates overlap between the wrong spec's target and the true subject. The derangement is the stricter wrong-spec test (a uniform Franklin-as-wrong-spec variant would risk leaking canonical Western framing into the comparison) and is the one reported.

Detailed per-condition parameters, exclusion cases, and ingestion specifics are in Appendix C.[^conditions-data]

[^conditions-data]: Raw data is available in the public repository at `results/global_<subject>/results_v2.json` (all direct-context conditions for the 13 global subjects) and `results/global_<subject>/<system>_results.json` / `<system>_fullpipeline_results.json` for per-system controlled / native configurations (`<system>` ∈ {mem0, letta, supermemory, zep, baselayer}). Hamerton responses live at `results/hamerton/` and Franklin at `results/franklin/` with per-judge judgments at `results/franklin_legacy_20260411/analysis/`.

### 3.5 Response models {#sec-3-5}

**Tier 1 (main study): Claude Haiku 4.5 as the primary response model, run across all 14 subjects and every condition in the main matrix. Haiku was chosen because effects that register on the weakest available model give the most conservative estimate of the spec's contribution; [§4.6.1](#sec-4-6-1) Tier 2 cross-provider probe checks whether the direction holds on stronger response models.**

**Tier 2 (cross-provider directional probe).** To test whether the specification effect depends on the response model being within the Anthropic family, Claude Sonnet 4.6 and Google Gemini 2.5 Pro were additionally run as response models on 3 subjects spanning the effect gradient (Ebers, Yung Wing, Zitkala-Sa) against the GPT-5.4-regenerated batteries from Control 1. Tier 2 results and subject-selection rationale are in [§3.3.1](#sec-3-3-1) and [§4.6.1](#sec-4-6-1).

**Call-time parameters.** All response models are called with `temperature=0` and `max_tokens=1024`.

**Prompt schema.** A single shared prompt is used across every condition. The system message frames the task as behavioral prediction of a specific person; the user message is the question plus whichever context inputs the condition specifies ([§3.4](#sec-3-4)). Nothing about the prompt changes per condition beyond the injected context block.

```
System: You are predicting how <subject> would respond to a specific
        question about their behavior, values, or reasoning. Answer
        in <subject>'s voice, grounded in their demonstrated patterns.

User:   <context block, one of: empty (C5), spec (C2a), wrong spec (C2c),
         facts (C4), facts + spec (C4a), corpus (C8), corpus + spec
         (C9), or retrieval ± spec (C1 / C3)>

        Question: <question text>
```

No prompt instruction tells the model to abstain, answer, hedge, or commit. That was a design decision made at the start of the study. Any prompt that coached response behavior would have directly confounded what the conditions are trying to measure, and the model's natural refusal-or-commitment pattern given a specific context is itself part of the phenomenon the study tests. [§4.3](#sec-4-3) reports the hedging-rate shift across conditions and treats it as a substantive finding rather than a behavior to suppress.

Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in Appendix C.[^response-scripts] [^response-data]

[^response-scripts]: The same information is present in the released code at `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, and `scripts/run_multimodel_responses.py`.

[^response-data]: Raw response files are in the public repository at `results/global_<subject>/results_v2.json` for the 13 global subjects, `results/hamerton/results.json` and `results/franklin/fullstack_haiku.json` for the legacy subjects, and `results/_tier2/` for the Tier 2 runs.

### 3.6 Evaluation: LLM-as-judge with calibration {#sec-3-6}

**Every response is scored 1-5 by seven LLM judges against the verbatim held-out ground-truth passage. Human annotation at this scale is feasible: roughly 14 subjects × 40 questions × 15+ conditions sits on the order of thousands of judgments, within reach of a small annotation team. It was not done here. This is a limited-budget solo research effort, and the deliberate trade-off was to run more conditions and more judges rather than fewer conditions with human annotation. That trade-off is the central evaluation limitation of the study; how we work inside it is what this section describes.**

**The evaluation is deliberately recursive.** Response models are evaluated by judges ([§3.6.1](#sec-3-6-1)). Judges are evaluated by calibration diagnostics ([§3.6.3](#sec-3-6-3)), inter-judge agreement metrics ([§3.6.4](#sec-3-6-4)), and post-hoc rubric-handling audits ([§3.6.6](#sec-3-6-6)). No single layer is treated as ground truth; each layer's behavior is itself measured and disclosed, and where a layer's behavior diverges from what the rubric intends, the divergence is flagged rather than corrected silently. The paper's rigor in the absence of human annotation comes from this stacked-instrument structure, not from trusting any one step.

**Scoring rubric.**

| Score | Meaning | Example (Hamerton: "How would he engage an unfamiliar industrial landscape?") |
|---|---|---|
| 1 | Refusal or irrelevant | "I don't have enough information to predict how Hamerton would respond." |
| 2 | Generic, not subject-specific | "He would probably dislike it, as most nineteenth-century artists preferred natural settings." |
| 3 | Partially captures the subject's behavioral pattern | "He would view the landscape aesthetically and evaluate it before engaging with its people." |
| 4 | Substantively captures the pattern on multiple dimensions | "He would render an immediate evaluative verdict on whether the environment is generative or hostile to contemplative work, before attending to the specific people in it." |
| 5 | Captures the behavioral pattern observable in the verbatim ground-truth passage | "He would classify the environment as cognition-disrupting within the first encounter, treat the classification as durable rather than provisional, and evaluate its people only secondarily to the environmental verdict." |

*(Examples are illustrative; full per-subject score distributions with verbatim responses are in [Appendix D](#appendix-d-validity-audit-and-score-distributions).)*

*(Condition identifiers such as C5, C2a, C4a, and C3 refer to the conditions defined in [§3.4](#sec-3-4) and summarized in Appendix C. Rubric anchor numbers 1 through 5 refer to the rubric table above.)*

**What a 5 means and does not mean.** A score of 5 reflects alignment with one specific behavioral sample: the held-out ground-truth passage the question is drawn from. It is not a claim that the response fully represents the subject in some absolute sense, and it is not a claim that the same response would score 5 on a different held-out passage from the same subject. Each question tests one behavioral sample at a time; the aggregate across roughly 40 questions per subject is what the paper reads as the subject-level score.

**Reading score differences.** A move from 2 to 3 is the difference between "he would probably dislike it, as most artists would" and "he would judge the landscape aesthetically before deciding whether to engage its people." The first answer is pattern-free and could apply to many nineteenth-century subjects; the second identifies a subject-specific behavioral tendency visible in Hamerton's actual writing. A move from 3 to 4 is the difference between identifying one behavioral tendency and identifying several that work together. [§3.6.2](#sec-3-6-2) develops the formal cross-anchor rule used throughout the results section.

### 3.6.1 Judge panel {#sec-3-6-1}

Seven judges from three providers. The multi-judge panel, not the single judge, is what gives the numeric aggregate its weight. Zheng et al. (2023) established that a single strong LLM judge correlates with human judges on comparable tasks at rates similar to human-human agreement. Subsequent panel-based work (Verga et al. 2024 and follow-ons) showed that aggregating multiple LLM judges past a small panel size further tightens agreement and reduces single-model idiosyncrasy. Seven judges across three providers is well past that threshold.

| Judge | Provider |
|---|---|
| Claude Haiku 4.5 | Anthropic |
| Claude Sonnet 4.6 | Anthropic |
| Claude Opus 4.6 | Anthropic |
| GPT-4o | OpenAI |
| GPT-5.4 | OpenAI |
| Gemini 2.5 Flash | Google |
| Gemini 2.5 Pro | Google |

Judge invocations are independent. Each judge receives the held-out ground-truth passage, the subject context (name, source), the prediction question, and the response to score. Judges do not see other judges' scores.

### 3.6.2 Fractional score interpretation {#sec-3-6-2}

Mean-across-judges aggregation produces fractional scores (2.87, 3.12, 2.34). Fractional shifts should be read through the integer anchors in the rubric, because each anchor corresponds to a categorical shift in response quality.

**Cross-anchor interpretation rule. A fractional delta that crosses an integer anchor reflects a real shift in the underlying response distribution. A delta that stays inside a single integer band is a within-category shift and a weaker claim.**

| Boundary crossed | Qualitative shift |
|---|---|
| 1 / 2 | The model moves from "I don't have enough to say" to an actual answer, even if generic. |
| 2 / 3 | The answer becomes specifically about this subject rather than a generic stand-in. |
| 3 / 4 | Multiple behavioral dimensions of the subject appear together in the same answer. |
| 4 / 5 | The response closely matches the behavioral pattern in the held-out passage. |

**Examples from the data.**

- Sunity Devee C5 (baseline, no context) at 1.03 → C2a (spec only) at 2.27: crosses the 1 / 2 anchor (refusal → engagement). Refusal responses in C5 turn into actual engagement in C2a, and some responses climb into subject-specific territory. Category change.
- Hamerton C5 (baseline) at 1.26 → C4a (facts + spec) at 2.77: crosses the 1 / 2 anchor and approaches the 2 / 3 boundary (generic → subject-specific). Generic art-historical stereotypes in C5 become responses grounded in Hamerton's documented patterns. Category change.
- Supermemory C3 (retrieval + spec) vs. C1 (retrieval only) on low-baseline subjects: −0.01 mean delta. Most per-subject deltas stay inside the same integer band. Within-category shifts; the aggregate is accurately small.

**The paper applies this rule consistently.** Score deltas reported in §4 are read through this lens. A +0.50 delta that crosses a rubric anchor is treated as a stronger claim than a +0.50 delta that does not, and the difference is called out where it matters. Full per-subject anchor-crossing data is at `docs/research/s114_anchor_crossing_examples.json`; the computing script is `scripts/compute_anchor_crossing.py`.

**The integer-anchor crossing metric is a lower bound on movement detectable by the rubric.** In addition to the integer-band crossings reported throughout §4, an additional ~18% of paired questions across the 18 condition pairs analyzed in `docs/research/within_band_shifts_20260428.json` show same-band fractional shifts of at least 0.5 anchor points. The 5-judge primary panel detects sub-anchor signal cleanly: direction-agreement among judges is 74% at panel |Δ| of 0.1 to 0.25 and 93% at |Δ| of 0.25 to 0.5. The integer metric is used throughout for cross-anchor categorical interpretation; the sub-anchor signal is reported here as methodological transparency.

### 3.6.3 Calibration {#sec-3-6-3}

Five judges (Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) were tested against four diagnostic inputs with known correct scores before study scoring began. Sonnet and Opus were not tested on the diagnostic suite; they join the panel for inter-judge agreement only. The 5-judge primary aggregate reported throughout §4 is Haiku + GPT-4o + GPT-5.4 + Sonnet + Opus (the diagnostic-calibrated core minus the two Gemini judges, plus Sonnet and Opus).

**Diagnostic tests.**

| Test | Input | Expected | What it measures |
|---|---|---|---|
| Verbatim | Response = ground truth | 5.0 | Recognizes perfect match |
| Paraphrased | Correct content, different wording | ~5.0 | Penalizes paraphrase? |
| Short correct | First sentence of ground truth | <5.0 | Partial content scored partial? |
| Long correct | Ground truth + generic padding | 5.0 | Length inflates scores? |

**Results.**

| Test | Haiku | Gemini Flash | GPT-4o | Gemini Pro | GPT-5.4 |
|---|---|---|---|---|---|
| Verbatim | 5.00 | 5.00 | 5.00 | 4.15 | 5.00 |
| Paraphrased | 4.75 | 4.70 | 5.00 | 3.55 | 5.00 |
| Short correct | 3.80 | 3.85 | 4.05 | 2.85 | 4.20 |
| Long correct | 5.00 | 3.80 | 3.35 | 1.20 | 4.80 |

Four of five judges score verbatim matches at 5.0; Gemini Pro is the outlier at 4.15. Length sensitivity varies: Haiku does not penalize padding; Gemini Pro penalizes it severely (5.0 to 1.20). GPT-5.4 has the tightest overall calibration profile across the four diagnostics.

**Use of calibration data.** Scores are not normalized. Any normalization requires deciding which judge's profile is "correct" and re-scaling the others toward it, which is a researcher judgment injected into the primary numbers. Calibration data is published in its raw form so readers can apply their own normalization if they prefer.

**Primary aggregate: 5-judge (non-Gemini) panel.** The primary numeric aggregate reported throughout [§4](#4-results) is the 5-judge mean using Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, and GPT-5.4. The two Gemini judges (Gemini 2.5 Flash, Gemini 2.5 Pro) are excluded from the primary aggregate and reported as a sensitivity check instead. The calibration table above shows Gemini Pro failing the verbatim-match diagnostic (4.15 where every other calibrated judge scores 5.00) and penalizing padded-correct responses severely (dropping from 5.00 on short correct to 1.20 on long correct). Gemini Flash shows smaller but consistent length sensitivity. A judge that cannot recognize verbatim ground-truth as a 5 is a known-unreliable instrument on this task. Including known-unreliable judges in the primary aggregate inflates or deflates effect-size numbers in ways that do not reflect the underlying response quality. Excluding them from the lead number, while keeping them available as a sensitivity check, preserves the provider-diversity argument (the final conclusions are stable whether or not the Gemini judges are included) without leading with a known-flawed aggregate.

The 7-judge aggregate is reported as a sensitivity check. Where the 7-judge and 5-judge aggregates produce materially different numbers, both are given and the delta is discussed. Every primary finding in §4 is stable across both aggregates (robustness confirmed in [§4.6](#sec-4-6)).

**The 5-judge primary is the conservative choice.** On the main gradient and spec-effect conditions, including the two Gemini judges produces *larger* spec-effect deltas, not smaller ones: on the 13 global subjects, the mean improvement from specification-alone (C2a) over no-context baseline (C5) rises from +0.35 on the 5-judge primary panel to +0.45 on the 7-judge aggregate, a +0.10-point widening driven by Gemini inflation compressing baseline scores more than spec-condition scores. The same direction holds across wrong-spec, facts-only, and facts-plus-spec aggregates. Reporting 5-judge primary means every headline effect size is the lower bound that remains once the most-inflationary judges are removed from the aggregate.

**How raw scores are read in §4.** Raw scores are treated as directional rather than absolute; deltas between conditions carry more information than levels; deltas that cross a rubric integer anchor ([§3.6.2](#sec-3-6-2)) are treated as stronger claims than deltas staying inside a single integer band. Raw calibration data is in the public repository at `results/judge_calibration/`.

### 3.6.4 Inter-judge agreement {#sec-3-6-4}

**The specification-effect claim.** Before discussing agreement, the claim the agreement measures support needs to be stated plainly. The specification effect is not a claim that the model has gained a new behavioral-prediction capability. It is the claim that when a Behavioral Specification is served as context, the model's responses shift in the direction of the subject's demonstrated behavioral patterns, and that shift registers as a measured increase in representational accuracy against held-out passages from the same subject. What the judges measure is whether that shift has happened. The judge panel is used to detect steering, not to determine truth.

With the claim stated, two complementary measures answer different questions. The first measures whether judges agree on direction; the second measures whether they agree on absolute magnitude.

**Do the judges agree on direction?** Pairwise Spearman ρ = **0.86 to 0.93** across the 5-judge primary panel (10 pairs across Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). The full 7-judge / 21-pair range is wider.[^spearman-7judge] The 5-judge primary range is the one used as the directional-agreement statistic throughout this paper because the calibration audit excluded the Gemini pair from the primary aggregate ([§3.6.3](#sec-3-6-3)). This is high rank agreement on the primary panel: the ranking of conditions ("C4a scored higher than C2a scored higher than C5") is consistent across the five non-Gemini judges. Whatever quirks any individual judge has in absolute calibration, the primary panel agrees on which conditions produce better responses. For a directional claim (is the specification steering responses in the right direction?), this is the statistic that matters.

[^spearman-7judge]: Spearman ρ from 0.29 to 0.93 across the 7-judge / 21-pair set, driven down by the two Gemini judges' partial coverage and inflation behavior. Full matrix in `docs/research/stats_update.md` §5.

**Do the judges agree on absolute magnitude?** Krippendorff α (ordinal) = **0.659 across the 5-judge primary panel** (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4); **0.535 across the 7-judge panel including Gemini Flash and Gemini Pro**. "Absolute magnitude" is the stricter question: when one judge gives a response a score of 3.5, does a different judge give the same response a score close to 3.5? Not "do they agree one response is better than another" (direction), but "do they agree on the actual numeric score" (magnitude). On the Krippendorff scale, α = 1.0 is perfect absolute agreement, α ≈ 0.0 is agreement no better than chance, and α < 0 is systematic disagreement. Krippendorff's own guidance cites α ≥ 0.8 as high reliability and α ≥ 0.667 as substantial or tentative reliability. The primary 5-judge α = 0.659 sits just below the 0.667 threshold. The drop to 0.535 when the two Gemini judges are included is the systematic +1-point Gemini inflation showing up in the statistic: Gemini judges score responses about one point higher on average than the five primary judges, so the absolute values disagree even when the rankings match. This is exactly the pattern that motivated making the 5-judge panel primary ([§3.6.3](#sec-3-6-3)).

**What this means for how results should be read.** The specification-effect claim is a directional claim. The Spearman ρ = 0.86-0.93 agreement answers it: seven judges across three providers converge on the direction of the effect. The Krippendorff α value places a ceiling on how precisely any individual fractional score should be read, which is why the paper treats per-subject deltas that stay inside a single rubric band as weaker than deltas that cross one.

**What the panel is not.** The panel is not an empirical determination that the higher-scoring responses are in absolute terms "the correct response" for the subject. That determination requires human annotation against the subject's actual writing, which we do not have. What the panel provides is cross-provider directional convergence: three independent providers' models agree that the specification is moving responses along the scale in the same direction. We treat that as sufficient evidence for a directional claim about the specification's effect, and no stronger than that.

Raw agreement matrices are at `results/interjudge_agreement/`.

### 3.6.5 Aggregation {#sec-3-6-5}

The aggregation rule [^fn4] is the three-step procedure below:

1. Within each judge, mean score across all questions for each (subject, condition) cell.
2. Mean across the five primary judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). A separate 7-judge mean including Gemini Flash and Gemini Pro is computed and reported as a sensitivity check.
3. Unit of inference: subject.

Mean was chosen over median and trimmed mean. Median discards information when judges cluster tightly, which the Spearman ρ = 0.86-0.93 agreement shows they do. Trimmed mean requires an arbitrary trim threshold. Simple mean preserves every judge's contribution, and the Gemini inflation is handled by the primary-vs-sensitivity split rather than by silent correction.

### 3.6.6 Rubric-handling limitations (validity audit) {#sec-3-6-6}

A direct inspection of the response text against the 5-judge primary scores surfaced two rubric-handling limitations that any reader of the §4 numbers should keep in mind. Both were identified by a post-hoc audit (`scripts/audit_low_end_inflation.py`; the numeric breakdowns below are produced by that script directly, and the raw per-response classifications live in the judgment and response JSONs under `results/global_<subject>/` for independent reproduction).

**Abstention is not cleanly distinguished from wrong prediction.** The rubric's lowest anchor, "refuses or off-base," lumps together two different behaviors: honest refusal to predict when the context does not support a prediction, and a substantively wrong prediction. Across 192 responses that match abstention patterns (phrases like "no specific information," "I cannot confirm," "would need additional context") in the low-baseline slice, 82.8% scored in the 1.0-1.5 band as expected, but 9.4% scored at or above 2.0 and 3.1% scored at or above 3.0. The mean abstention score is 1.27. Judges give partial credit for abstentions that include adjacent-fact recitation or correctly identify what the provided context does not contain, treating honest refusal as a rubric-2 or rubric-3 response rather than rubric-1. The effect is bidirectional: honest abstention can be over-credited (our Example C in [§4.1](#sec-4-1), Seacole Q2 at 2.80) and substantive prediction under the influence of a specification's epistemic-integrity axioms can also be over-credited when the model flags its own epistemic limits (Hamerton Q21 at 4.00 under spec-induced abstention).

**Length correlates with score in the baseline condition only.** Across 1,599 low-baseline responses, response length correlates with 5-judge primary score at r = 0.26. When decomposed by condition, the correlation is driven entirely by the no-context baseline (C5) at r = 0.604. Spec-containing and facts-containing conditions show near-zero correlation (spec alone C2a at r = 0.14, facts alone C4 at r = 0.01, facts + spec C4a at r = −0.01). Ultra-high responses (score ≥ 4.5) are not longer than mid-range responses on average (2,790 chars vs. 2,829 chars), so length inflation is not a general phenomenon across the rubric. The specific pattern is: **verbose baseline responses are scored more generously than short baseline refusals.** Three behaviors drive this:

- **Hedging.** Phrases like "I'm not sure but..." or "There may be cases where..." extend response length without adding predictive content.
- **Adjacent-fact recitation.** Listing related facts the model holds but does not use to directly answer the question, padding the response without engaging the question itself.
- **Disambiguation offers.** Phrases like "Are you asking about X or Y?" which the rubric treats as engaged responses when they are actually non-answers.

The practical implication is that measured baseline scores slightly overestimate the no-context prediction accuracy. The spec-effect gap is larger than reported under strict rubric scoring, not smaller.

**Per-judge strictness on abstentions.** Sonnet is the strictest judge on abstention responses (mean 1.14), followed by GPT-5.4 (1.17), Haiku (1.29), and GPT-4o (1.34). Opus is the most lenient at 1.41, roughly 0.27 points above the strictest judge. This cross-judge variation is small in absolute terms but is worth naming: no single judge is universally strictest, and the 5-judge primary average smooths these differences without eliminating them.

**What this means for the reported effects.** Both limitations tighten the paper's claims rather than weakening them. Abstention over-credit pulls the measured C5 baseline *up*, which shrinks the apparent spec-vs-baseline gap. Length-driven baseline inflation does the same. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift we report; we elect to report the measured number and flag the direction of the bias rather than recompute under a modified rubric, to keep the analysis plan lock intact. §7 Future Work proposes a differentiated rubric that scores abstention as its own dimension and a length-controlled scoring protocol.

The class-level LLM-as-judge limitation that this methodology cannot fully address is treated in [§6.2](#sec-6-2).[^judgments-data]

[^judgments-data]: Raw per-judge judgments are in the public repository at `results/global_<subject>/*_judgments_<judge>.json` (and `judgments_v2.json` for the merged v2 set) for the 13 global subjects, `results/hamerton/*_judgments_<judge>.json` for Hamerton, and `results/franklin/*_judgments.json` plus `results/franklin_legacy_20260411/analysis/*_judgments.json` for Franklin. Memory-system per-judge judgments live at `results/global_<subject>/<system>_judgments_<judge>.json` (controlled) and `results/global_<subject>/<system>_fullpipeline_judgments_<judge>.json` (native) in the same flat per-subject directory.

### 3.7 Base Layer Pipeline for the Behavioral Specification {#sec-3-7}

**The pipeline transforms raw source text into a Behavioral Specification in four content-production steps: extract, embed, author, and compose. An import step normalizes the source data before extraction.** Each step is a single script backed by a single model choice. Total cost per subject is under $1.

| Step | Input | Tool / model | Output |
|---|---|---|---|
| 1. Import | ChatGPT / Claude exports, journals, plain text, directories | `import_conversations.py` | SQLite canonical store |
| 2. Extract | Canonical source text | `extract_facts.py`, Claude Haiku 4.5, 46-predicate vocabulary | Structured behavioral triples with ADD / UPDATE / DELETE / NOOP operations |
| 3. Embed | Extracted facts | `embed.py`, `all-MiniLM-L6-v2`, ChromaDB | Vector index for provenance tracing and retrieval |
| 4. Author | Extracted facts + embeddings | `author_layers.py`, Claude Sonnet 4.6 | Three interpretive layers as markdown (anchors, core, predictions). Each layer is produced from facts alone, not from prior layer output. Each layer prompt includes a domain guard that prevents topic skew (ablation-validated in prior pilot work). |
| 5. Compose | The three authored layers | `agent_pipeline.py`, Claude Opus 4.6 | Unified behavioral brief in flowing prose |

The artifact served as context in experimental conditions (referred to throughout the paper as "the Behavioral Specification") is the three authored layers concatenated with the composed brief, not the brief alone. Total size per subject is approximately 7,000 tokens, roughly 5,000 words (about the length of a short magazine article).

The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: `avoids`, `repeatedly engages in`, `refuses to`, `values`, `fears`, `has experienced`). The full predicate list is in [Appendix A](#appendix-a-predicate-vocabulary). The vocabulary is human-curated and was validated across 50+ pilot subjects before being frozen for the study. The constrained vocabulary is the main lever the pipeline uses to push extraction away from biographical facts ("his father was violent") and toward behavioral patterns ("evaluates authority figures on dual criteria of virtue and failure").

The three authored layers have distinct jobs. Each layer has a characteristic format; examples below are drawn from the Hamerton specification.

**Anchors** encode the subject's load-bearing axioms in numbered form (A1, A2, ...), each with an activation condition and a false-positive warning. Example:

> *A1. DUAL-LEDGER AUTHORITY: Evaluates authority figures on virtue and failure simultaneously, refusing to collapse them into a single verdict. Active when: encountering teachers, mentors, or institutional power. False positive: do not apply when the authority figure is a peer or subordinate.*

**Core** captures values, beliefs, and self-view in flowing prose. It is the layer that reads most like an essay about the person. Example:

> *Treats aesthetic sensibility and moral seriousness as inseparable. The quality of attention a person brings to beauty is, for him, direct evidence of the quality of attention they bring to anything else. This belief predates his career in art criticism and survives intact across every phase of his life.*

**Predictions** are explicit behavioral predicates (P1, P2, ...) with detection criteria, directives, and false-positive warnings. Example:

> *P3. Environment-as-cognition. Classifies new environments as generative or hostile to contemplative work before engaging with their particulars. Detection: immediate evaluative language about the environment itself, not about the people or tasks in it. Directive: model an immediate and durable classification rather than gradual adjustment. False positive: do not apply when the environment is a neutral logistical setting.*

The compose step integrates these three layers into a unified prose brief. The served specification is the compose-step brief concatenated with the three layer files.

Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80) to process a 50,000- to 150,000-word autobiography end to end.

---

## 4. Results

![Figure 5: How to read this figure. The x-axis lays out four context conditions in order: behavioral specification alone (C2a), facts alone (C4), raw corpus alone (C8), and facts plus spec (C4a). The y-axis is the share of the 351 paired low-baseline questions (9 subjects times 39 questions) that improved, tied, or worsened relative to the no-context C5 baseline; each bar is a stacked outcome distribution. Reading from the left: the specification alone (C2a) improved 70.9% of questions; facts alone (C4) improved 72.9%; the raw corpus alone (C8) improved 78.3%; stacking the specification on top of the raw facts (C4a) improved 78.6%, the highest rate of any single-or-stacked condition. Stacking the spec on top of the corpus (C9, in the next figure) reaches the same plateau. The specification alone (C2a, ~7K tokens) matches the raw corpus's improvement rate (C8, 80K-400K tokens) within 8 percentage points at roughly an order of magnitude less context, and stacking the spec onto either fact representation produces the highest scores. The specification is providing a more aligned line of reasoning than what fact retrieval alone produces. Median Δ when improved = +1.00 rubric points (a full anchor-band move); median Δ when worsened = −0.40. The metric guards against tiny-gain inflation. (§4.2.1.)](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig5_condition_effects_v3.png)

*Figure 5: How to read this figure. The x-axis lays out four context conditions in order: behavioral specification alone (C2a), facts alone (C4), raw corpus alone (C8), and facts plus spec (C4a). The y-axis is the share of the 351 paired low-baseline questions (9 subjects times 39 questions) that improved, tied, or worsened relative to the no-context C5 baseline; each bar is a stacked outcome distribution. Reading from the left: the specification alone (C2a) improved 70.9% of questions; facts alone (C4) improved 72.9%; the raw corpus alone (C8) improved 78.3%; stacking the specification on top of the raw facts (C4a) improved 78.6%, the highest rate of any single-or-stacked condition. Stacking the spec on top of the corpus (C9, in the next figure) reaches the same plateau. The specification alone (C2a, ~7K tokens) matches the raw corpus's improvement rate (C8, 80K-400K tokens) within 8 percentage points at roughly an order of magnitude less context, and stacking the spec onto either fact representation produces the highest scores. The specification is providing a more aligned line of reasoning than what fact retrieval alone produces. Median Δ when improved = +1.00 rubric points (a full anchor-band move); median Δ when worsened = −0.40. The metric guards against tiny-gain inflation. (§4.2.1.)*

This section reports the Behavioral Specification's effect on behavioral prediction across seven parts:

- **[§4.1](#sec-4-1). The cross-subject gradient.** The primary result, across 14 subjects.
- **[§4.2](#sec-4-2). Compression: structure vs. raw text.** Is the effect about structure or about information volume?
- **[§4.3](#sec-4-3). Mechanism: Content, Not Format.** Does the content of the correct specification drive the effect, or does any structured prompt?
- **[§4.4](#sec-4-4). Memory-system composition.** Does the specification layer on top of existing commercial memory systems? Where does it help or hurt at the per-question level ([§4.4.2](#sec-4-4-2) common mechanisms, [§4.4.3](#sec-4-4-3) cross-system Keckley case)?
- **[§4.5](#sec-4-5). Exploratory case study (Letta stateful-agent).** Brief summary in body; full case study in Appendix G. Post-hoc N=3 comparison; not a headline finding.
- **[§4.6](#sec-4-6). Robustness and sensitivity.** Cross-provider response generation, judge-panel sensitivity, what these checks do not address, and the high-baseline end of the gradient through the Franklin reference ([§4.6.4](#sec-4-6-4)).
- **[§4.7](#sec-4-7). Summary and bridge to discussion.** A one-paragraph synthesis of what §4 established, framing the transition into §5.

Every number in §4 uses the 5-judge primary aggregate defined in [§3.6.3](#sec-3-6-3) (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-judge sensitivity check (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported in [§4.6](#sec-4-6). Score deltas are read through the anchor-crossing rule from [§3.6.2](#sec-3-6-2): a delta that crosses a rubric integer anchor is a stronger claim than one that stays inside a single anchor band.

### 4.1 The cross-subject gradient {#sec-4-1}

![Figure 4.1: How to read this figure. Start at the horizontal red line at Δ = 0. Above the red line means the specification produced a positive change in score versus the no-context baseline; below the red line means a negative change. The x-axis is the no-context baseline score (C5) on the 1-5 rubric. Subjects in the left half of the plot (C5 ≤ 2.0) are the 9 low-baseline subjects (the population of relevance); Subjects in the right half (C5 > 2.0) are the 5 mid-baseline subjects plus Franklin as the high-baseline reference. The y-axis is the per-subject lift the specification produces over baseline (Δ_C4a = C4a − C5). All 9 low-baseline subjects sit above the red line in the upper-left, all with positive Δ ranging from Babur at +0.25 to Hamerton at +1.51. Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13, the high-baseline anchor where pretraining already covers the subject and the specification adds nothing. The dotted regression line slopes downward from upper-left to lower-right (slope −0.96, R² = 0.82); read it as: the better the model already knows the subject, the smaller the lift the specification produces. The substantive read is that the specification raises subjects toward a roughly constant operating quality near C4a ≈ 2.46, so the lift is largest where the floor is lowest. (§4.1.) Per-question anchor-crossing distributions are reported separately in the §4.1 transition table.](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig_4_1_gradient_scatter_v3.png)

*Figure 4.1: How to read this figure. Start at the horizontal red line at Δ = 0. Above the red line means the specification produced a positive change in score versus the no-context baseline; below the red line means a negative change. The x-axis is the no-context baseline score (C5) on the 1-5 rubric. Subjects in the left half of the plot (C5 ≤ 2.0) are the 9 low-baseline subjects (the population of relevance); Subjects in the right half (C5 > 2.0) are the 5 mid-baseline subjects plus Franklin as the high-baseline reference. The y-axis is the per-subject lift the specification produces over baseline (Δ_C4a = C4a − C5). All 9 low-baseline subjects sit above the red line in the upper-left, all with positive Δ ranging from Babur at +0.25 to Hamerton at +1.51. Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13, the high-baseline anchor where pretraining already covers the subject and the specification adds nothing. The dotted regression line slopes downward from upper-left to lower-right (slope −0.96, R² = 0.82); read it as: the better the model already knows the subject, the smaller the lift the specification produces. The substantive read is that the specification raises subjects toward a roughly constant operating quality near C4a ≈ 2.46, so the lift is largest where the floor is lowest. (§4.1.) Per-question anchor-crossing distributions are reported separately in the §4.1 transition table.*

**Hypotheses tested in this section** (from [§1.2](#sec-1-2)): H1. Adding the specification improves prediction. H2. The effect is inversely proportional to the response model's pretraining coverage. Corollary to H2: on high-baseline subjects, the specification does not add value and mildly interferes.

---

**The cross-subject gradient.** The less the model already knows about a subject from pretraining, the more the specification helps. On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from [§3.2.1](#sec-3-2-1)), every one of the 9 improves under facts + spec; mean Δ_C4a = **+0.89 points**; none declines.

---

**Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it.** Of the 351 individual responses in the low-baseline slice, **55.0% crossed at least one rubric integer anchor upward when the specification was added**. Multi-anchor jumps of two or more bands (e.g., 1→3) appear in 18% of low-baseline questions on the spec conditions, with about 6% being extreme jumps of three or more bands (e.g., 1→4, 1→5). The AI's answer moved from one category of response to a qualitatively different category. These are the multi-anchor jumps at the margin the aggregate mean understates.

---

**A structural sensitivity check explains the shape of the gradient.** The Behavioral Specification produces an answer of roughly uniform quality (mean C4a = 2.46 across all 14 subjects), with C4a clustering tightly in the 2.0-2.7 band regardless of where each subject's no-context baseline sits.[^gradient-slopes] The visible "lift" (Δ_C4a = C4a − C5) is therefore mechanically largest where the floor is lowest, smallest where the floor is already at or above the spec's operating quality. The substantive read: the specification works by lifting subjects toward a common operating quality, and the practical question is which subjects sit below that quality and need the lift. AI users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction ([§5.3](#sec-5-3)); they are the subjects for whom the lift is largest and the spec is most needed.

[^gradient-slopes]: The technical sensitivity that establishes the gradient: level regression of C4a on C5 produces a slope of +0.04, R² = 0.008; the change-score parameterization Δ_C4a on C5 has a slope of −0.96 dominated by the coupling identity slope_Δ = slope_level − 1. Reported below as the third sensitivity block.

| Transition | % of responses | What this means in plain terms |
|---|---:|---|
| 1 → 2 | **33.3%** | Refusal or off-base → generic engagement with the question |
| 1 → 3 | 12.3% | Refusal → partially-aligned prediction |
| 1 → 4 | 4.8% | Refusal → substantively-aligned prediction |
| 1 → 5 | 0.9% | Refusal → fully matches the held-out pattern |
| 2 → 3 | 2.0% | Generic → subject-specific |
| 2 → 4 | 0.3% | Generic → substantively-aligned |
| 3 → 4 | 1.4% | Partially → substantively-aligned |
| No upward crossing | 38.2% | Delta stayed inside a single anchor band |
| Downward crossing | 6.8% | Specification hurt the response |

One of every three low-baseline responses moves from "cannot engage" to actual engagement. Another one in five makes a larger jump. Only one response in fifteen gets worse.

---

**Three representative examples below show the different ways the specification can help.** They are selected to show three distinct mechanisms the 6-provider collective review identified across the data.[^collective-review-examples] Hedge reduction is common but not the only thing going on. The specification also corrects wrong predictions in the opposite direction, and it enables interpretive inference from character patterns when retrieved facts are insufficient.

[^collective-review-examples]: Collective review write-up at `docs/reviews/s114_example_analysis_20260421_170720.md`. Raw per-judge scores and full response text for the three examples below at `results/global_<subject>/results_v2.json` and `results/global_<subject>/judgments_v2.json` (Examples A and B from `global_ebers/` and `global_bernal_diaz/` respectively; Example C from `global_seacole/`).

> ### Example A. Baseline to Facts + Spec: identity disambiguation + interpretive inference
>
> **Subject:** Georg Ebers. **Battery question (Q7):** *"How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?"*
>
> **Ground truth (held-out, what Ebers actually wrote):** *"A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed."*
>
> **Baseline response (C5, no context, 5-judge mean 1.20):**
>
> > *"I don't have specific information about Ebers's characterization of this relationship in my training data. To give you an accurate answer, I would need to know: 1. Which Ebers you're referring to — there are several notable figures with this surname in educational contexts..."*
>
> **With specification + facts (C4a, 5-judge mean 3.60):**
>
> > *"Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable — not instrumental, but constitutive. Self-sacrifice is not a means to institutional success; it is the evidence that success is genuine. Ebers witnessed this directly at Keilhau..."*
>
> **What the specification did.** The baseline failed to identify which Ebers was being asked about and refused to predict. The specification resolved the identity question and enabled a substantive interpretive claim ("constitutive, not instrumental") that the ground truth passage confirms. The collective review panel identified this as a mix of identity disambiguation and interpretive inference from character.

> ### Example B. Facts to Facts + Spec: directional correction
>
> **Subject:** Bernal Diaz del Castillo. **Battery question (Q16):** *"When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?"*
>
> **Ground truth:** *"There were 114 steps to the summit, and, as they feared that Cortes would experience the same fatigue in mounting as Motecusuma had, they were going to assist him by taking hold of his arms. Cortes, however, refused."*
>
> **With facts alone (C4, 5-judge mean 2.00):**
>
> > *"Based on the facts provided about Bernal Diaz del Castillo and his observations of Cortes, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example."*
>
> **With facts + specification (C4a, 5-judge mean 4.80):**
>
> > *"Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect Cortes to refuse the assistance and perform the labor himself, particularly if it serves a symbolic or morale-signaling purpose."*
>
> **What the specification did.** Facts alone produced a confident but directionally wrong prediction (commander accepts help). The specification corrected the prediction to match the ground truth (Cortes refuses). The collective review panel unanimously called this mechanism directional correction of a prediction: the specification encoded Cortes's pattern of physical self-reliance and performative leadership, overriding the model's generic "good leaders accept help" default.

> ### Example C. Facts to Facts + Spec: abstention becomes near-perfect inference
>
> **Subject:** Mary Seacole. **Battery question (Q2):** *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"*
>
> **Ground truth:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*
>
> **With facts alone (C4, 5-judge mean 2.80).** Effectively a non-answer:
>
> > *"Based on the complete set of facts provided, there is **no specific information** about how Mary Seacole typically responds when a delirious patient mistakes her for a family member. While the facts document many aspects of Mary Seacole's nursing care and compassion... there is no explicit account of her reactions to delirious patients confusing her identity with their relatives. To answer this question accurately, one would need additional source material..."*
>
> The model correctly identifies what the facts do not contain, lists adjacent facts about her nursing practice, and declines to predict. This is a clean abstention, not a wrong prediction. The 2.80 score reflects judge leniency on honest abstention responses: judges give partial credit for "right domain, declines to predict specifics" even when no prediction was actually made. Read the behavior, not the number: this is a refusal.
>
> **With facts + specification (C4a, 5-judge mean 5.00).** Near-perfect inference:
>
> > *"Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern. Primary response: compassionate acceptance. She would not correct the patient in the moment. Instead, she would lean into the mistaken identity, sustain the fiction with tenderness, and prioritize emotional relief over factual accuracy. This aligns with A4 (Proximate Obligation) and A8 (Sympathetic Realism)..."*
>
> **What the specification did.** The shift is from refusal-to-predict to a specific, accurate behavioral prediction. In rubric-anchor terms, this is a **2.80 → 5.00 jump, crossing three integer anchors upward**, exactly the kind of high-magnitude category-shift the [§4.1](#sec-4-1) lede flags as the multi-anchor jumps at the margin the aggregate mean understates. The prediction closely tracks Seacole's verbatim held-out account [^fn5]. The specification enabled the model to generalize from Seacole's established compassionate-caregiving pattern (documented in the facts but not explicitly mapped to this scenario) to the specific untested situation. The collective review panel unanimously identified this as interpretive inference beyond retrieved facts: a mechanism that retrieval alone cannot produce because it requires applying character-level pattern to novel situations.
>
> **A note on rubric handling of abstention.** The judge panel scored this abstention at 2.80, not at 1.00 (the rubric anchor for "refuses or off-base"). This reflects a rubric-level issue we encountered in both directions across the study: judges treat honest abstentions as partial engagement (scoring ~2.5-3.0) rather than as refusals, and they sometimes penalize spec-induced honest abstentions where the specification appropriately declined to invent detail ([§4.4.3](#sec-4-4-3)'s Keckley Q21 example). The rubric does not cleanly distinguish abstention from wrong prediction, which softens the apparent magnitude of some effects in either direction. A differentiated rubric that scores abstention as its own dimension is flagged as follow-up in §7.

---

**The improvement is not uniform across subjects. It depends on how much the AI already knows about the person.** Plain version: the less the model's pretraining has to work from, the more the specification can add. The more the model already knows, the less room the specification has to help, and on the highest-baseline subjects it can mildly hurt.

Linear regression of the facts-plus-specification effect against baseline:

| Statistical test | Value |
|---|---|
| Regression slope (Δ_C4a vs. C5) | **−0.96** [95% CI −1.24, −0.67] |
| R² | **0.82** (82% of variance explained by baseline) |
| Slope p-value | **< 0.001** (p = 0.000009) |
| Correlation r | −0.90 |
| Wilcoxon signed-rank, C5 vs. C2a | W = 10, p = 0.005 |
| Wilcoxon signed-rank, C5 vs. C4a | W = 11, p = 0.007 |
| Subjects with positive Δ_C4a | 12 of 14 |
| Low-baseline subjects (n=9) positive | 9 of 9 |
| Low-baseline mean Δ_C4a | +0.89 |

Rank agreement across the 5-judge primary panel is high (pairwise Spearman ρ = 0.86 to 0.93, [§3.6.4](#sec-3-6-4)), so the directional claim rides on broad agreement across three providers rather than on any one judge's scoring.

**A note on baseline measurement.** The measured C5 baseline (mean 1.52 on the low-baseline slice) is slightly inflated by a length-driven rubric effect. A post-hoc validity audit ([§3.6.6](#sec-3-6-6)) found that longer no-context responses (which include more hedging, adjacent-fact recitation, and disambiguation language) score higher on average than short refusals, with length-score correlation r = 0.604 specifically within C5 responses. Spec-containing conditions show no such length correlation. The true no-context prediction accuracy is likely lower than 1.52, which makes the spec-effect gap slightly *larger* than the reported +0.89 mean lift. We report the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact, and flag the direction of the bias here so readers can interpret the effect size accordingly.

> ### Example D. The gradient at the extremes
>
> **Low-baseline, largest improvement.** *Hamerton* (baseline 1.26, Δ_C4a +1.51). Philip Gilbert Hamerton is a 19th-century British essayist whose *Autobiography* sits well outside the LLM pretraining spotlight. Adding the specification moved his prediction score from near-refusal to substantive subject-specific engagement across most of the battery.
>
> **High-baseline, mild interference.** *Franklin* (baseline 3.77, Δ_C4a −0.13). Benjamin Franklin is among the most widely referenced autobiographers in American public-domain literature. The AI already has him well-modeled from pretraining. The specification does not add representational signal; the spec-alone condition drops 0.40 points, facts + spec drops 0.13. See [§4.6.4](#sec-4-6-4) for the full sensitivity treatment.
>
> **Low-baseline, smallest improvement.** *Babur* (baseline 1.76, Δ_C4a +0.25). Babur is the 16th-century Central Asian ruler and founder of the Mughal Empire. His corpus is the largest in the study (422,772 words) and his autobiography is partially represented in LLM training data. The specification still improves the score, but the room to help is smaller.

---

**Reading the gradient.** The x-axis of Figure 4.1 is the no-context baseline score (C5) for each subject on the 1-5 rubric. The y-axis is the per-subject lift the specification produces over that baseline (Δ_C4a, the C4a facts+spec score minus the C5 baseline score). Each point is one of the 14 historical subjects. The 9 low-baseline subjects (C5 ≤ 2.0, the population of relevance from [§3.2.1](#sec-3-2-1)) cluster in the upper-left quadrant, all with positive Δ, ranging from Babur at +0.25 (smallest lift, baseline 1.76) to Hamerton at +1.51 (largest lift, baseline 1.26). Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13, the high-baseline reference point where the model already knows the subject from pretraining and the specification adds nothing. The regression line falls from upper-left to lower-right; its slope of −0.96 is the change-score parameterization (its mechanical interpretation is treated in the [§4.1](#sec-4-1) coupling-free reframing below). The substantive read: the lower the model's pretraining baseline on a subject, the larger the lift the specification produces, because the spec produces a roughly constant C4a quality near 2.46 regardless of baseline. Above the regression line and worth naming: Sunity Devee (baseline 1.03, Δ +1.38) and Hamerton (baseline 1.26, Δ +1.51) outperform the linear fit; Babur (baseline 1.76, Δ +0.25) underperforms it as the low-baseline outlier. The takeaway: the specification helps most where the model knows the subject least, and once a subject crosses into the high-baseline band the specification has no representational gap to fill.

---

**Per-subject results.**

The table is ordered by baseline within each band. In the color-rendered PDF of the paper, the low-baseline rows are tinted green (the population of relevance), the mid-baseline rows are tinted yellow, and Franklin is tinted gray as the high-baseline reference. Figure 4.1 presents the same data as a scatter plot with the regression line.

| Subject | Baseline (C5) | Spec only (C2a) | Facts + Spec (C4a) | Δ spec | Δ facts+spec | Anchor crossed |
|---|---:|---:|---:|---:|---:|:-:|
| **Low-baseline slice (C5 ≤ 2.0), population of relevance** | | | | | | |
| Ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | ✓ |
| Sunity Devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | ✓ |
| Hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | ✓ |
| Fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | ✓ |
| Bernal Diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | partial |
| Babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | - |
| Seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | ✓ |
| Keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | - |
| Yung Wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | - |
| **Mid-baseline slice (2.0 < C5 < 3.0)** | | | | | | |
| Zitkala-Sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | - |
| Cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | - |
| Rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | - |
| Augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | - |
| Equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | - |
| **High-baseline reference (not part of the main gradient)** | | | | | | |
| Franklin (known-figure control) | 3.77 | 3.37 | 3.65 | −0.40 | −0.13 | - |

**What each band is telling us.**

- **Low-baseline (n = 9):** every subject improves. The slice is uniform. This is the population of relevance for real AI deployment.
- **Mid-baseline (n = 5):** 3 subjects improve, 2 decline. The model has enough pretraining footprint on these subjects that the specification competes with the model's own working model. The specification sometimes increases representational accuracy and sometimes does not.
- **Franklin (high-baseline reference):** both spec-containing conditions score below baseline. The specification cannot add what the model already has.

Per-subject anchor-crossing distributions (ranging from 25.6% on Babur to 74.4% on Sunity Devee) and per-subject per-judge score matrices are in Appendix D.

**Battery-composition sensitivity.** Two potential confounds on the gradient slope were tested as sensitivity checks. Both leave the baseline effect substantially intact.

*Battery-question-type.* Subjects whose batteries lean toward literal-recall questions could in principle pick up part of the apparent gradient, since literal questions are easier to lift with retrieval. Controlling for this directly, the gradient on baseline survives, attenuated by about 8% and still strongly significant. Battery composition adds independent signal but does not explain away the baseline effect. Full regression specification, partial coefficients, and variance decomposition appear in Appendix B.6.

*Hamerton leverage.* Hamerton has both the highest Δ_C4a and the largest battery (80 questions), and a natural concern is that it alone drives the slope. Dropping Hamerton and refitting on the 13 globals attenuates the slope by about 7%, with overlapping confidence intervals. The gradient is not Hamerton-driven. Subset-regression detail also appears in Appendix B.6.

Neither control overturns the headline finding. The gradient is not primarily driven by either battery-question-type composition or Hamerton's legacy-generator battery. What these checks do not rule out is a more subtle confound in which generator differences are correlated with other unobserved subject characteristics; a cleanest future test would re-run a second-generator battery on the same 13 globals.[^battery-sensitivity-data]

[^battery-sensitivity-data]: Full analysis, per-subject data, and reproducibility script at `docs/research/v10_battery_sensitivity_analysis.md` and `scripts/_v10_battery_sensitivity.py`.

**Sanity-checking the gradient.** Read at face value, the headline slope of −0.96 says the spec helps subjects the model knows least about substantially more than subjects it already knows well. That phrasing is misleading. Three follow-up analyses on the same per-subject data show what is actually happening. Detail in Appendix B.7.

**What is actually happening.** The 2.46 number that summarizes after-spec performance is a per-subject average across roughly 30 to 80 questions. Inside each battery, some questions show large lifts and others do not move much. The pattern is sharpest on low-baseline subjects. For these nine subjects (351 paired questions total), the spec moved the answer into a higher integer rubric band on 55% of questions, into a lower band on 7%, and stayed inside the same band on 38%. Many of the upward moves were not small: 18% of questions jumped by two or more anchors, and about 6% jumped by three or more. On recall-style questions where C5 often refuses or gives a generic answer, the spec frequently produces these multi-anchor jumps to specific answers grounded in the subject's observed pattern (anchor-crossing detail in [§4.4.2](#sec-4-4-2) and the per-system Pattern 1/2/3 analysis). On questions where the model would not have answered well even with the full source corpus available, the spec does little. The aggregate gradient appears to be driven less by uniform subject-level convergence than by accumulation of question-level upward crossings. Low-baseline subjects begin with a larger pool of questions at low rubric anchors, so the spec has more opportunity to drive these category-changing improvements. High-baseline subjects, having fewer low-scoring questions to begin with, show a correspondingly smaller aggregate lift. The directional asymmetry is itself a finding: across the C5 to C4a comparison on the full 14-subject panel, no question crossed from band 2, 3, or 4 into band 5; the only band-5 endpoints reached came from band 1 (3 questions). The spec lifts the floor; it does not lift the ceiling. (Cross-condition comparisons such as C4 to C4a admit higher-band crossings, e.g., Seacole Q2's 2.80 to 5.00 jump in Example C above.)[^heldout-leakage-audit]

[^heldout-leakage-audit]: Held-out leakage audit on the 60 unique extreme-upward-jump cases at `docs/research/held_out_leakage_investigation_20260428.md`: 0 6-gram matches at C4a, severity rare; full taxonomy and headline-impact estimate in Appendix B.9.

The cleaner reframing, then, is not "the spec lifts low-baseline subjects more than high-baseline ones" (the −0.96 slope does not independently establish that fact) and not "every subject lands at the same ceiling." It is: **on the questions where the spec moves the answer into a higher integer rubric band (i.e., crosses an integer threshold on the 1-5 rating scale), low-baseline subjects have more such opportunities, because their batteries contain more questions at low rubric anchors to begin with.** Subsequent sections that lean on the gradient ([§4.4.2](#sec-4-4-2), [§4.6](#sec-4-6), [§5.5](#sec-5-5)) should be read against this reframing.

### 4.2 Compression: structure vs. raw text {#sec-4-2}

![Figure 4.2: How to read this figure. The x-axis is context size in tokens (log scale, spanning roughly 1K to 400K). The y-axis is the 5-judge primary score on the 1-5 rubric. Each faint trace is one of the 9 low-baseline subjects; the bold curve is the median-across-subjects aggregate. The leftmost point (smallest context) is the no-context baseline (C5, mean 1.52). Moving rightward, the curve passes through the ~7K-token Behavioral Specification alone (C2a, mean 2.23), then the structured fact corpus (C4, mean 2.35), then the full raw corpus (C8, ~80K-400K tokens, mean 2.45), then facts plus spec (C4a, mean 2.45) and corpus plus spec (C9, mean 2.50). In every condition where the specification is added or served alone, the score sits at or above the no-spec equivalent at the same context size. The curve has a steep initial slope and a long plateau: the first ~7K tokens of structured specification buy +0.68 points of lift over baseline; the next 10x to 50x more tokens of raw corpus buy only an additional +0.22. That shape is the substantive claim: the behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document. (§4.2; this figure is the Hamerton-style compression story aggregated across the 9 low-baseline subjects.)](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig_4_2_compression_v3.png)

*Figure 4.2: How to read this figure. The x-axis is context size in tokens (log scale, spanning roughly 1K to 400K). The y-axis is the 5-judge primary score on the 1-5 rubric. Each faint trace is one of the 9 low-baseline subjects; the bold curve is the median-across-subjects aggregate. The leftmost point (smallest context) is the no-context baseline (C5, mean 1.52). Moving rightward, the curve passes through the ~7K-token Behavioral Specification alone (C2a, mean 2.23), then the structured fact corpus (C4, mean 2.35), then the full raw corpus (C8, ~80K-400K tokens, mean 2.45), then facts plus spec (C4a, mean 2.45) and corpus plus spec (C9, mean 2.50). In every condition where the specification is added or served alone, the score sits at or above the no-spec equivalent at the same context size. The curve has a steep initial slope and a long plateau: the first ~7K tokens of structured specification buy +0.68 points of lift over baseline; the next 10x to 50x more tokens of raw corpus buy only an additional +0.22. That shape is the substantive claim: the behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document. (§4.2; this figure is the Hamerton-style compression story aggregated across the 9 low-baseline subjects.)*

**Hypothesis tested in this section** (H5 from [§1.2](#sec-1-2)): A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size.

---

**Context improves prediction.** On the 9 low-baseline subjects, every context condition increases the per-subject mean score by roughly one full rubric point over the no-context baseline.

| Condition | Context served | Mean (low-baseline, n=9) | Δ from C5 |
|---|---|---:|---:|
| C5 | none (baseline) | 1.52 | 0.00 |
| C2a | spec only | 2.23 | +0.71 |
| C4 | facts only | 2.35 | +0.83 |
| C8 | raw corpus only | 2.45 | +0.93 |
| C4a | facts + spec | 2.45 | +0.93 |
| C9 | corpus + spec | 2.50 | +0.98 |

The AI does not need much context to move from refusal-and-off-base to engaged subject-specific prediction. It needs *some* context.

**The compact specification captures the large majority of that improvement.** A 7,000-token Behavioral Specification recovers most of what the full raw corpus delivers, despite being roughly 5x to 80x smaller depending on subject (per-subject compression ratios in the table below). Across the 9 low-baseline subjects, the raw corpus (C8) averages 0.22 points higher than spec alone (C2a). The corpus's edge is real but small relative to the context-size gap that produces it.

**The efficiency claim in one metric: predictive gain per 1,000 tokens of context.** The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. Plotted against context size, the score climbs steeply at first and flattens out. The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document.

---

**Per-subject compression comparison (5-judge primary, low-baseline slice).**

The table shows baseline and every compression-related condition for each subject, with the compression ratio (source corpus tokens ÷ specification tokens, both approximate) for scale. In the color-rendered PDF, low-baseline rows are tinted to mark the population of relevance; the C8 − C2a gap column is shaded to make the spec-vs-corpus difference visible at a glance.

| Subject | Source words (~tokens) | Compression ratio (corpus / spec) | C5 baseline | C2a spec (~7K tok) | C4 facts (~10K tok) | C8 raw corpus | C4a facts+spec | C9 corpus+spec | C8 − C2a |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hamerton | 25,231 (~33K) | 7× | 1.26 | **2.63** | 2.43 | 2.27 | 2.77 | **3.09** | **−0.36** |
| Sunity Devee | 67,379 (~88K) | ~13× | 1.03 | 2.27 | 2.46 | 2.55 | 2.41 | 2.46 | +0.28 |
| Ebers | 96,174 (~125K) | ~17× | 1.02 | 1.54 | 2.02 | 2.18 | 2.07 | 2.16 | +0.64 |
| Fukuzawa | 139,088 (~181K) | ~26× | 1.67 | 2.35 | 2.67 | 2.74 | 2.78 | 2.78 | +0.39 |
| Bernal Diaz | 187,315 (~244K) | ~33× | 1.70 | 2.27 | 2.41 | 2.55 | 2.48 | 2.53 | +0.28 |
| Babur | 422,772 (~549K) | ~79× | 1.76 | 1.91 | 2.03 | 2.05 | 2.01 | - | +0.14 |
| Seacole | 62,467 (~81K) | ~12× | 1.77 | 2.48 | 2.63 | 2.83 | 2.59 | 2.73 | +0.35 |
| Keckley | 58,742 (~76K) | ~11× | 1.84 | 2.43 | 2.39 | 2.50 | 2.44 | 2.49 | +0.07 |
| Yung Wing | 66,459 (~86K) | ~13× | 1.88 | 2.22 | 2.13 | 2.42 | 2.40 | 2.50 | +0.20 |
| **Mean** | | **~25×** | **1.52** | **2.23** | **2.35** | **2.45** | **2.44** | **2.59** | **+0.22** |

Babur's C9 condition was excluded because the 422,772-word corpus plus the specification exceeded the response model's context window.

**What the aggregate numbers say.**

- Every context condition lifts the low-baseline mean by at least one full rubric point over the no-context baseline.
- The specification alone recovers roughly three-quarters of the corpus-alone lift (spec lift +0.71, corpus lift +0.93) at an order of magnitude to two orders of magnitude smaller context depending on subject.
- Adding facts to the specification (C4a) produces the same mean as raw corpus alone (both 2.45). Two different compression strategies, same performance, different context shapes.
- Adding the specification on top of the full raw corpus (C9) adds ~0.09 points on average over raw corpus alone (per-question paired recompute on the 8-subject C9-eligible slice; the per-subject mean column at the bottom of the per-subject table reads 2.59 for C9 vs 2.45 for C8, but the cross-subject mean of per-question paired Δs is the canonical number for the comparison). The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

**What the aggregate numbers hide.**

The small mean Δ values for spec-on-info-rich-context comparisons (C4a vs C4, C9 vs C8) are residues of substantial per-question movement in both directions, not uniformly small effects.

| Comparison | n | Up | Down | None | Multi-anchor (≥2) | Mean Δ |
|---|---:|---:|---:|---:|---:|---:|
| C4a vs C4 (spec on top of facts) | 351 | 22% | 17% | 61% | 2.6% | +0.09 |
| C9 vs C8 (spec on top of corpus) | 312 | 22% | 19% | 60% | 3.8% | +0.09 |

Roughly 1 in 5 questions cross an integer rubric anchor upward, roughly 1 in 5 to 6 cross downward, and ~60% do not move at the integer-band granularity. The mean is the residue of these counter-acting per-question effects. Hamerton is a strong outlier on the C9-vs-C8 comparison (49% upward rate, 19 up vs 2 down on its 39 questions), while the other 7 low-baseline subjects average roughly balanced up and down rates (10% to 26% upward, similar downward); the per-question pattern across these 7 subjects is closer to bimodal than to uniform lift. The same per-question heterogeneity logic applies in [§4.4.2](#sec-4-4-2) to memory-system layering (Pattern 1/2/3): when the specification is layered on top of an information-rich pre-context, it produces increases and degradations that often nearly cancel at the aggregate.[^c4a-c9-anchor-data]

[^c4a-c9-anchor-data]: Per-question anchor-crossing data for C4a vs C4 and C9 vs C8 at `docs/research/per_question_anchor_crossing_extended_20260428.json` (script: `scripts/compute_anchor_crossing_c4a_c4_and_c9_c8.py`). Multi-anchor examples include Hamerton q22 (1→3 on C9 vs C8), Hamerton q25 (1→4), Seacole q2 (2→5 on C4a vs C4), and Yung Wing q22 (1→4 on C4a vs C4).

### 4.2.1 Question-improvement rate: a candidate secondary reporting metric {#sec-4-2-1}

The aggregate mean score is a useful summary, but it blends judge variability with response quality. A cleaner unit: **out of N individual questions, how many does each condition improve over the no-context baseline?** This is a **per-question improvement rate against a no-context baseline**, structurally parallel to the per-prompt win-rate convention used in LLM evaluation (Chatbot Arena, LMSYS pairwise preference rates). Each question either improves, ties, or worsens when the condition's context is added; the unit is judge-noise-resistant in aggregate and directly interpretable without requiring a matched rubric across studies.

**The reporting triplet.** An improvement rate alone hides the magnitude of help and harm. We report three numbers together for each condition: the improvement rate, the worsening rate, and the median magnitude of improvement among improved questions (with the median worsening magnitude as a sanity check).

**Low-baseline slice (9 subjects, 351 questions, 5-judge primary per-question means).**

| Condition vs. C5 baseline | Improved | Tied | Worse | Improvement rate | Median Δ when improved | Median Δ when worsened |
|---|---:|---:|---:|---:|---:|---:|
| **C2a spec only** | 249 | 49 | 53 | **70.9%** | **+1.00** | −0.40 |
| C4 facts only | 256 | 44 | 51 | 72.9% | +1.00 | −0.40 |
| C8 raw corpus | 275 | 31 | 45 | 78.3% | +1.00 | −0.60 |
| C4a facts + spec | 276 | 22 | 53 | 78.6% | +1.00 | −0.40 |

**The magnitude column is the important row of this table.** When the specification helps, the typical help is a full rubric category (+1.00 median). When it hurts, the typical hurt is less than half a category (−0.40 median). The metric is not capturing trivial +0.02-per-question gains; the underlying improvements are substantive.

**All 14 main-study subjects, matched 39-question batteries (546 questions: 13 globals plus the Hamerton 39-question matched-battery slice).**

| Condition vs. C5 baseline | Improvement rate | Worsening rate |
|---|---:|---:|
| C2a spec only | 58.8% | 26.7% |
| C4 facts only | 60.1% | 26.6% |
| C8 raw corpus | 65.2% | 23.6% |
| C4a facts + spec | 65.8% | 26.4% |

On the 9 low-baseline subjects, **7 out of every 10 questions improve with the specification alone**, roughly 1 in 10 tie, and fewer than 1 in 6 worsen. Every context condition exceeds a 70% per-question improvement rate on the population of relevance. The specification's rate sits within 8 percentage points of the raw corpus's (70.9% vs. 78.3%) at an order of magnitude less context.

![Figure 4.2.1: How to read this figure. The x-axis lays out the five context conditions in order of context size: raw corpus (C8) first, then spec alone (C2a), facts alone (C4), facts plus spec (C4a), and corpus plus spec (C9). The y-axis is the share of the 351 paired low-baseline questions (9 subjects times 39 questions; C9 drops to 312 with Babur excluded for context-window). Three lines run across the conditions: the green "improved" line stays high (70.9% to 78.6%), the yellow "tied" line is the middle band, and the red "worsened" line stays low. Read each column as a stacked outcome distribution against the no-context C5 baseline. The takeaway: spec alone (C2a) improves 70.9% of questions at roughly an order of magnitude less context than the raw corpus (C8, 78.3%); facts plus spec (C4a) matches the raw corpus's improvement rate while cutting the tied band roughly in half. Median Δ when improved is +1.00 rubric points; median Δ when worsened is −0.40 points, so the metric guards against tiny-gain inflation. (§4.2.1).](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig_4_2_1_question_improvement_rates_v3.png)

**Pairwise comparison at question level (low-baseline slice).**

| Comparison | Higher-cost condition higher | Tie | Lower-cost condition higher |
|---|---:|---:|---:|
| Raw corpus (C8) vs. spec alone (C2a) | 187 (53.3%) | 56 | 108 (30.8%) |
| Corpus + spec (C9) vs. facts + spec (C4a) | 153 (49.0%) | 45 | 114 (36.5%) |

The raw corpus outscores the spec alone on more questions than it loses, but the spec outscores the corpus on roughly one-third of them. On the combined conditions, the 7K-token facts + spec package outscores the much larger corpus + spec package on 36.5% of questions.

**Positioning as a secondary reporting metric.** A per-question improvement rate against a no-context baseline makes behavioral prediction directly comparable across future studies in a way that mean scores do not. "Our representation improves 65% of questions over the no-context baseline, with median improvement magnitude +0.8 points" is interpretable on its own and can be compared to this study's 70.9% / +1.00 without matched judges or rubrics. We propose this metric as a **candidate secondary reporting axis** for future AI-personalization work, always paired with mean-score information, never replacing it. The proposal is developed further in §7 Future Work.

Failure modes of the question-improvement-rate metric [^fn6] are discussed in §6 limitations.

The same improvement-rate framing is referenced in [§1.2](#sec-1-2) (as a secondary outcome alongside the mean-score gradient) and in [§4.1](#sec-4-1) [^fn7].

---

> ### Example: Hamerton, the compression story at its clearest
>
> Hamerton has the smallest source corpus in the study (25,231 words, compression ratio ~5×). The specification alone (~4,500 tokens for Hamerton; ~7K tokens averaged across globals) scores 2.63, exceeding the full raw corpus at 2.27. Facts-plus-spec reaches 2.77. Corpus-plus-spec reaches 3.09, the highest compression-related score observed in the study. This is the case where structured context substantially outperforms raw text, and where the spec and corpus are clearly complementary rather than overlapping.
>
> The pattern is interpretable: when the source corpus is short enough to be sparse on its own, structured extraction adds organizational value beyond mere content. Hamerton is the boundary condition for the compression claim, not the proof of it.

> ### Example: Ebers, the honest cost of compression
>
> Ebers has a larger source corpus (96,174 words) and the study's lowest baseline (1.02). Every context condition lifts his score above baseline. But the specification alone (1.54) underperforms the raw corpus (2.18) by 0.64 points, the widest spec-vs-corpus gap in the low-baseline slice. Facts alone (2.02) fall between them.
>
> Ebers is where the cost of compression is most visible. The raw corpus contains something the 7K-token spec does not capture, and that something is worth 0.64 points on the rubric. The honest reading is not "compression fails"; it is "compression captures the bulk of the signal but not all of it, and on some subjects the residual matters more than on others." The trade-off is still favorable: the spec delivers +0.52 points of lift at roughly 6% of the corpus's token cost; the corpus delivers +1.16 points at 18× the context. Per 1,000 tokens of context served, the spec is substantially more efficient.

---

**Why this matters for deployment.**

At any scale where a per-user full autobiography cannot be served into context on every query (which is to say, at any real-world scale beyond a toy demo), the compression result is what makes personalization operationally tractable. The specification's 7K-token footprint is within normal per-request context budgets. A 100,000-to-400,000-word corpus is not. The specification achieves most of the predictive benefit at a tractable cost; the corpus achieves marginally more at a cost that rules out deployment.[^compression-data]

[^compression-data]: Raw per-subject data at `results/global_<subject>/c8_c9_results.json` and `results/global_<subject>/results_v2.json`. The compression analysis and question-improvement rate computation are in `scripts/recompute_5judge_primary.py` and `scripts/compute_question_improvement_rate.py`. Figure 4.2 plots score versus context size (log scale) per subject and shows the steep initial climb and long plateau.

---

### 4.3 Mechanism: Content, Not Format {#sec-4-3}

![Figure 6: How to read this figure. Each cluster on the x-axis is one of the 13 global subjects (Hamerton excluded; he has no wrong-spec run); subjects are sorted by C5 baseline left to right so low-baseline subjects sit on the left and mid-baseline subjects sit on the right. The y-axis is the 5-judge primary score on the 1-5 rubric. Within each subject cluster, four bars show the no-context baseline (C5), the correct specification (C2a, aggregate Δ = +0.35), the random-derangement wrong spec (C2c v2, aggregate Δ = +0.22), and the adversarial maximum-distance wrong spec (C2c v1, aggregate Δ = −0.25). In every one of the 13 subjects, the wrong specification (under either v1 or v2 pairing) scored lower than the correct specification served on the same subject. Under the adversarial v1 pairing, 8 of the 13 subjects (Augustine, Babur, Cellini, Equiano, Keckley, Rousseau, Seacole, Zitkala-Sa) scored lower than the no-context C5 baseline; serving the wrong spec actively hurt the prediction relative to no context at all. The correct-vs-adversarial gap of 0.60 points on the 1-5 rubric (more than half a full rubric category) is the content effect: the lift is not coming from the prompt's structure or length, it is coming from the specification matching the actual subject. (§4.3.)](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig6_wrong_spec_control.png)

*Figure 6: How to read this figure. Each cluster on the x-axis is one of the 13 global subjects (Hamerton excluded; he has no wrong-spec run); subjects are sorted by C5 baseline left to right so low-baseline subjects sit on the left and mid-baseline subjects sit on the right. The y-axis is the 5-judge primary score on the 1-5 rubric. Within each subject cluster, four bars show the no-context baseline (C5), the correct specification (C2a, aggregate Δ = +0.35), the random-derangement wrong spec (C2c v2, aggregate Δ = +0.22), and the adversarial maximum-distance wrong spec (C2c v1, aggregate Δ = −0.25). In every one of the 13 subjects, the wrong specification (under either v1 or v2 pairing) scored lower than the correct specification served on the same subject. Under the adversarial v1 pairing, 8 of the 13 subjects (Augustine, Babur, Cellini, Equiano, Keckley, Rousseau, Seacole, Zitkala-Sa) scored lower than the no-context C5 baseline; serving the wrong spec actively hurt the prediction relative to no context at all. The correct-vs-adversarial gap of 0.60 points on the 1-5 rubric (more than half a full rubric category) is the content effect: the lift is not coming from the prompt's structure or length, it is coming from the specification matching the actual subject. (§4.3.)*

![Figure 4: Adding the Behavioral Specification near-eliminates baseline hedging and refusal on subjects the model does not already know. Refusal rate (y-axis) across the C5 → C2a → C4a context conditions (x-axis) on the 9 low-baseline subjects, under the narrow starts_refusal classifier (§4.3). Rate drops from 28.8% at no-context baseline to 1.4% with spec alone to 0.0% with facts plus spec, an order-of-magnitude reduction at each step. The broader-rule classifier (41.2% → 7.9% → 0.4%) shows the same direction.](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig4_hedging_reduction.png)

*Figure 4: Adding the Behavioral Specification near-eliminates baseline hedging and refusal on subjects the model does not already know. Refusal rate (y-axis) across the C5 → C2a → C4a context conditions (x-axis) on the 9 low-baseline subjects, under the narrow starts_refusal classifier (§4.3). Rate drops from 28.8% at no-context baseline to 1.4% with spec alone to 0.0% with facts plus spec, an order-of-magnitude reduction at each step. The broader-rule classifier (41.2% → 7.9% → 0.4%) shows the same direction.*

**Hypothesis tested in this section** (H3 from [§1.2](#sec-1-2)): The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

---

**If structure alone were driving the effect, a mismatched specification would produce roughly the same improvement as a matched one. The data rejects this directly.**

On the 13 global subjects with complete 5-judge primary coverage, three conditions test whether content matters:

| Condition | Mean Δ vs. C5 (5-judge primary, 13 globals) | Reading |
|---|---:|---|
| C2a (correct spec) | **+0.35** | matched content improves prediction |
| C2c v2 (random derangement, seed-fixed) | **+0.15** | partial improvement; dominated by floor effects on low-baseline subjects |
| C2c v1 (fixed derangement, cultural/temporal distance maximized) | **−0.25** | adversarial mismatch degrades prediction below the no-context baseline |

The two wrong-spec variants differ by construction. **v1 (fixed derangement)** is a hardcoded pairing designed so each subject receives the specification of a culturally- and temporally-distant other [^fn8].[^wrong-spec-script] **v2 (random derangement)** is a seed-fixed random permutation in which no subject receives its own specification but pairings can land culturally-close; this tempers the aggregate drop. Reporting both shows that even a random wrong-spec barely beats no context, and an adversarial wrong-spec actively hurts.

[^wrong-spec-script]: Pairing logic in `scripts/run_global_rerun.py`.

The gap between the correct-spec (C2a) condition at +0.35 and the fixed-derangement (C2c v1) condition at −0.25 is **0.60 points on the 1-5 rubric**, more than half a full rubric-anchor category. That gap is the content effect, measured at the population mean; per-question swings are larger in both directions [^fn9].

**Per-subject wrong-spec deltas.** The aggregate Δs above are not uniform across subjects. Five of thirteen subjects show small positive deltas under the adversarial v1 pairing (Bernal Diaz, Ebers, Fukuzawa, Sunity Devee, Yung Wing); the remaining eight show negative deltas that drag the aggregate to −0.25. Under the random v2 pairing, four subjects show negative deltas (Cellini, Equiano, Rousseau, Seacole); the remaining nine span small to moderate positive deltas. The per-subject heterogeneity is consistent with the mechanism reading: adversarial pairing hurts most subjects and helps a few where coincidental content overlap matches the target subject's pattern; random pairing flips the proportion because cultural-temporal distance is, on average, smaller.

| Subject | Δ_C2c_v1 (adversarial) | Δ_C2c_v2 (random) |
|---|---:|---:|
| Augustine | −0.47 | +0.13 |
| Babur | −0.59 | +0.76 |
| Bernal Diaz | **+0.09** | +0.69 |
| Cellini | −0.56 | −0.87 |
| Ebers | **+0.30** | +0.79 |
| Equiano | −0.79 | −1.00 |
| Fukuzawa | **+0.26** | +0.86 |
| Keckley | −0.49 | +0.14 |
| Rousseau | −0.52 | −0.37 |
| Seacole | −0.34 | −0.10 |
| Sunity Devee | **+0.27** | +0.53 |
| Yung Wing | **+0.32** | +0.39 |
| Zitkala-Sa | −0.68 | +0.04 |
| **Aggregate** | **−0.25** | **+0.15** |

5-judge primary panel; per-subject Δ vs. C5 baseline. Bolded v1 deltas are the five subjects where adversarial pairing produces a positive delta.[^wrong-spec-scaffold]

[^wrong-spec-scaffold]: Per-subject scaffold values at `docs/research/v11_emit/4_3_wrong_spec.json` (claim ids `4_3_<subject>_c2c_v1_delta` / `4_3_<subject>_c2c_v2_delta`).

---

**Three mechanism types.**

Three distinct mechanisms produce the correct-specification improvement across the study data. Each has a characteristic wrong-specification failure mode, illustrated in the matched examples below.

1. **Identity disambiguation.** When the baseline model cannot determine which person is being asked about, the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame. *Wrong-spec failure mode:* the model either detects the mismatch explicitly and refuses to predict, or anchors on the wrong person's pattern and produces a coherent but off-target prediction.
2. **Directional correction.** When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification overrides the generic with the subject-specific. *Wrong-spec failure mode:* the model applies the wrong person's pattern; depending on how close that pattern happens to be to the target subject's, the prediction is either directionally wrong in a new way or coincidentally correct [^fn10].
3. **Interpretive inference.** When retrieved facts do not include direct evidence for the specific question, the specification provides interpretive scaffolding to generalize from established character patterns to the novel situation. *Wrong-spec failure mode:* the model detects the mismatch and refuses, or applies wrong-person scaffolding and produces a low-quality prediction.

---

**Spec-activation evidence.**

Tag-citation analysis on response text shows the content-activation gap.[^spec-activation-data] On correct-spec conditions, **78.6%** of responses explicitly cite at least one spec tag (anchor ID, axiom reference, predictive-template label). On wrong-spec conditions, only **50.0%** do. The 28.6-point gap is a lower bound on the content effect: models may draw on spec content without literally quoting tag IDs, so the true divergence is wider. The baseline reading is that models recognize when the specification fits the question and engage with it; they recognize when it doesn't fit and disengage or improvise.

[^spec-activation-data]: Data at `docs/research/spec_activation_analysis.json`.

---

**Response-level evidence: wrong-spec detection.**

Across 587 wrong-spec responses classified [^fn11], the response distribution is bimodal:

- **60.6%** explicitly flagged the content mismatch [^fn12]
- **36.5%** attempted to apply the mismatched content and produced a low-quality prediction
- **2.0%** hedged implicitly
- **0.9%** were ambiguous

The detection asymmetry in this experiment: battery questions name the target subject (e.g., "How would Ebers characterize...") but specifications are anonymized ([§3.7](#sec-3-7)), so "detecting the mismatch" means the model is comparing the named target in the question to the interpretive content of the anonymized specification, and concluding the specification does not describe the named target. The signal that carries the detection is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model knows about the named subject, not surface name cues. The 60.6% is a lower bound on that comparison because a more capable response model, or a derangement with less interpretive distance between target and substitute, could push the rate in either direction.

---

**Hedging evidence (from [§1.3](#sec-1-3)) carries the same implication.**

Under both classifier rules, spec-containing conditions eliminate baseline hedging: narrow-rule 28.8% → 1.4% → 0.0%, broader-rule 41.2% → 7.9% → 0.4%. Order-of-magnitude drops. If mere structured context were producing the effect, wrong-spec should also eliminate hedging at a similar rate. Instead, the 60.6% explicit-detection rate on wrong-spec responses means refusal patterns persist when the content does not fit the subject. The hedging-reduction is spec-content-specific, not structure-specific.

---

**Per-question matched comparison.**

The three [§4.1](#sec-4-1) examples extend directly into mechanism-by-mechanism wrong-spec contrasts. Same subject, same question, same response model; the only change is the specification content. Correct-spec C4a responses are in [§4.1](#sec-4-1) for reference.

> ### Example A (wrong-spec), Ebers Q7: identity disambiguation fails
>
> **Subject + question:** same as [§4.1](#sec-4-1) Example A (Ebers, self-sacrifice and educational institutional success). Battery-question target name: Ebers (explicit in the prompt).
> **Wrong spec served:** Equiano's specification, served anonymized per `run_global_rerun.py` fixed pairing. The response cites two of Equiano's anchors; the anchor definitions from Equiano's specification are:
>
> > **A4 — SYSTEMIC INDICTMENT:** *"avarice — institutionalized greed — is the generative engine of the greatest human cruelties, and that individual kindness within a corrupt system neither redeems the system nor excuses participation in it."*
> >
> > **A9 — ECONOMIC SELF-DETERMINATION:** *"the capacity to earn, trade, and accumulate independently is not merely practical but constitutive of dignity and agency — economic self-determination is the material form that freedom takes."*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition; large drop vs. correct spec, 1.60 vs. 3.60):**
>
> > *"I need to be direct: I don't have reliable access to specific statements by Ebers on this question. The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. ... Given A4 (Systemic Indictment) — that institutionalized greed is the generative engine of cruelty ... a teacher sacrificing their own economic security, health, or family time does not fix a system structured by avarice."*
>
> **Reading.** The model detected the mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It named the served anchors correctly, reasoned from Equiano's framework, and declined to produce a prediction about Ebers. The identity-disambiguation mechanism that enabled the correct spec's lift in [§4.1](#sec-4-1) Example A did not fire because the spec content is not about Ebers. The response falls near the rubric floor because no prediction was made.

> ### Example B (wrong-spec), Bernal Diaz Q16: content convergence across genuinely different frameworks
>
> **Subject + question:** same as [§4.1](#sec-4-1) Example B (Bernal Diaz, Cortes and offered physical assistance). Battery-question target name: Bernal Diaz.
> **Wrong spec served:** Sunity Devee's specification (fixed pairing). The response cites three of Sunity Devee's anchors; the anchor definitions from her specification are:
>
> > **A5 — RELATIONAL IDENTITY:** *"identity, worth, and moral standing are constituted through their relationships — to family, spouse, ruler, and God — rather than through individual achievement or autonomous selfhood."*
> >
> > **A9 — SIMPLICITY AS VIRTUE:** *"Simplicity in dress, material goods, personal manner, and child-rearing is a positive moral value — a marker of spiritual seriousness. Elaborateness, display, and material accumulation are read as mild moral signals in the wrong direction."*
> >
> > **P5 — VIRTUE THROUGH EMBODIED PRACTICE:** *"credibility is demonstrated through concrete daily disciplines (bathing, prayer, ritual purity, hospitality, domestic skill) rather than through abstract declaration. Habit is the principle."*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition; near-tie with correct spec, 4.60 vs. 4.80):**
>
> > *"Based on this behavioral specification, the author would likely decline the offered assistance ... Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) ... Physical exertion endured without assistance becomes evidence of character."*
>
> **Reading, not parroting.** The two specs are genuinely different frameworks. Bernal Diaz's actual anchors include A1 Divine Mandate, A2 Civilizational Hierarchy, A4 Loyalty Architecture, A5 Forward Compulsion, A6 Gold as Proof, and A10 Charismatic Override: a conquistador's martial-providential register. Sunity Devee's anchors cited here (A5 Relational Identity, A9 Simplicity as Virtue, P5 Virtue through Embodied Practice) are an ascetic-devotional register. Direct anchor-to-anchor comparison across the two specs finds zero substantive mirroring. On the specific question of refusing offered physical help, the two frameworks converge by different logics: the correct spec (Bernal Diaz) predicts refusal because accepting help would signal weakness to followers and violate performative self-reliance (A4 + A5 in the conquistador register); the wrong spec (Sunity Devee) predicts refusal because accepting help would compromise physical discipline and violate simplicity-as-virtue (A9 + P5 in the devotional register). Different moral architectures, same overt behavior.
>
> **Why the correct spec still outperformed, 4.80 vs. 4.60.** Both conditions predicted the right surface action. The 0.20-point gap is judge preference for rationale specificity that matches the ground-truth passage's tone. The correct spec's "symbolic or morale-signaling purpose" rationale maps onto a battlefield memoir's register; the wrong spec's "spiritual seriousness, devotional simplicity" rationale predicts the same action but in a register alien to Cortes on the steps of the Templo Mayor. Judges reward tonally-aligned rationale. The convergence is real but costs precision.
>
> **Why this matters for the aggregate numbers.** This is the coincidence case that lifts the wrong-spec aggregate above zero. When the fixed derangement (v1) happens to pair subjects whose behavioral patterns converge on the same surface prediction for a given question, wrong-spec lift is real on that question, not an artifact. Across the 507-response v2 cohort (13 globals × 39 questions), mismatch-loss dominates on the adversarial v1 pairing (aggregate Δ −0.25, same 13 globals × 39 questions) and roughly balances on the random v2 pairing (aggregate Δ +0.15). Example B is one of the roughly 5-10% of questions where content coincidence produces correct-surface, wrong-logic predictions.

> ### Example C (wrong-spec), Seacole Q2: interpretive inference fails
>
> **Subject + question:** same as [§4.1](#sec-4-1) Example C (Seacole, delirious patient). Battery-question target name: Mary Seacole.
> **Wrong spec served:** Bernal Diaz's specification (fixed pairing, anonymized). The response identifies the wrong spec by its interpretive content alone. Bernal Diaz's actual anchors that the model names in the response are:
>
> > **A1 — DIVINE MANDATE:** *every outcome is providentially ordained; reasoning is teleological.*
> >
> > **A2 — CIVILIZATIONAL HIERARCHY:** *Spanish Christian civilization as axiomatic superior lens on encountered peoples.*
> >
> > **A4 — LOYALTY ARCHITECTURE:** *personal loyalty is load-bearing, more binding than formal rank.*
> >
> > **A5 — FORWARD COMPULSION:** *retreat is moral failure; momentum is irreversible once committed.*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition; large drop vs. correct spec, 1.40 vs. 5.00):**
>
> > *"The specification you've provided describes someone from the 16th-century Spanish conquest period — the epistemic anchors, loyalty architecture, divine mandate framing, and forward compulsion all point to that historical context. Mary Seacole (1805-1881) was a Creole nurse and travel writer from Jamaica who served in the Crimean War. These are entirely different people from different centuries with different frameworks. ... I don't have documented instances of this. I could speculate based on her memoir's tone and her known character, but that would be inference, not behavioral specification."*
>
> **Reading.** The model detected the mismatch between the named target in the question (Mary Seacole, a 19th-century Jamaican Creole nurse) and the anonymized content of the served specification (16th-century Spanish conquest anchors). It named the anchors it was seeing, placed Seacole in a different era and role, and refused to apply the mismatched content. The interpretive-inference mechanism that produced [§4.1](#sec-4-1) Example C's correct-spec 5.00 score does not fire: without Seacole's actual character pattern in context, the model would not generalize from an unrelated conquistador's framework to her delirious-patient scenario.

---

**Summary of the three examples.**

| Example | Mechanism (correct spec) | C4a (correct) | C2c v1 (wrong) | Drop | Wrong-spec pattern |
|---|---|---:|---:|---:|---|
| A (Ebers Q7) | Identity disambiguation + interpretive inference | 3.60 | 1.60 | **−2.00** | Explicit mismatch flag; declined prediction |
| B (Bernal Diaz Q16) | Directional correction | 4.80 | 4.60 | **−0.20** | Coincidental content overlap; wrong-spec prediction matches |
| C (Seacole Q2) | Interpretive inference | 5.00 | 1.40 | **−3.60** | Explicit mismatch flag; declined prediction |

Two of three examples show large drops (−2.00 to −3.60 points) when the content does not fit. The third shows near-zero drop, but only because the wrong spec's content happens to predict the same surface behavior. That asymmetry, clean mismatches versus coincidental overlaps, is exactly what the aggregate Δ numbers reflect: the adversarial-pairing v1 aggregates to −0.25 because most questions are mismatch cases, and the random-pairing v2 aggregates to +0.15 because random pairings more often hit content-proximity combinations like Example B.[^wrong-spec-raw-data]

[^wrong-spec-raw-data]: Raw per-judge data and full response text at `results/global_<subject>/results_v2.json` (wrong-spec responses) and `results/global_<subject>/judgments_v2.json` (per-judge scores). Analysis scripts at `scripts/compute_wrong_spec_5judge.py` and `scripts/compute_wrong_spec_per_subject.py`.

---

### 4.4 Memory-system composition {#sec-4-4}

**Hypothesis tested in this section** (H4 from [§1.2](#sec-1-2)): The Behavioral Specification interacts with memory-system retrieval in a structured way. It lets retrieval-based systems handle question types they were not designed for (interpretation-heavy questions where retrieved facts alone are insufficient), while sometimes hurting on question types where retrieval already supplied the plain answer (literal-recall) or where retrieved facts are insufficient to ground a prediction at all (refusal-triggering). The aggregate per-system Δ is therefore a mixture of these patterns, with the balance shifting by retrieval architecture. The load-bearing finding is per-question, not aggregate.

---

### 4.4.1 Aggregate performance across systems {#sec-4-4-1}

![Figure 7: How to read this figure. The y-axis lists each memory system (Zep, Letta archival, Mem0, Base Layer, Supermemory). The x-axis is the per-system spec delta (Δ_spec = C3 mean − C1 mean) across the 9 low-baseline subjects, where each system's bar runs from the C1 retrieval-only mean rightward (or leftward if negative) to the C3 retrieval-plus-spec mean. Positive-subject counts (subjects with Δ > 0) sit on each system label. Zep (Δ +0.17, 9/9 subjects positive) and Letta archival (Δ +0.17, 8/9) are the cleanest gains; Mem0 (Δ +0.10, 6/9) and Base Layer's local retrieval substrate (Δ +0.08, 6/9) are smaller but positive; Supermemory aggregates near zero (Δ −0.01, 5/9) because per-question swings cancel (median improvement +1.45, median worsening −1.41; treated in §4.4.2). At the per-question level, the share of low-baseline questions that crossed at least one rubric integer anchor upward when the specification was added on top of retrieval (controlled C1→C3 configuration, n = 351 paired questions per system across 9 subjects, all 9/9 subjects had at least one upward crossing per system): Base Layer 29.0%, Zep 27.9%, Letta 26.9%, Mem0 23.4%, Supermemory 20.2%. The aggregate Δ and the anchor-crossing rate agree on rank ordering: where the spec helps, it helps both at the subject mean and at the per-question category level. (§4.4.1.)](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig7_memory_systems_v3.png)

*Figure 7: How to read this figure. The y-axis lists each memory system (Zep, Letta archival, Mem0, Base Layer, Supermemory). The x-axis is the per-system spec delta (Δ_spec = C3 mean − C1 mean) across the 9 low-baseline subjects, where each system's bar runs from the C1 retrieval-only mean rightward (or leftward if negative) to the C3 retrieval-plus-spec mean. Positive-subject counts (subjects with Δ > 0) sit on each system label. Zep (Δ +0.17, 9/9 subjects positive) and Letta archival (Δ +0.17, 8/9) are the cleanest gains; Mem0 (Δ +0.10, 6/9) and Base Layer's local retrieval substrate (Δ +0.08, 6/9) are smaller but positive; Supermemory aggregates near zero (Δ −0.01, 5/9) because per-question swings cancel (median improvement +1.45, median worsening −1.41; treated in §4.4.2). At the per-question level, the share of low-baseline questions that crossed at least one rubric integer anchor upward when the specification was added on top of retrieval (controlled C1→C3 configuration, n = 351 paired questions per system across 9 subjects, all 9/9 subjects had at least one upward crossing per system): Base Layer 29.0%, Zep 27.9%, Letta 26.9%, Mem0 23.4%, Supermemory 20.2%. The aggregate Δ and the anchor-crossing rate agree on rank ordering: where the spec helps, it helps both at the subject mean and at the per-question category level. (§4.4.1.)*

![Figure 3: All-three-disagree rate across Mem0, Letta, and Supermemory at top-k = 1, 3, 5, and 10 in the controlled configuration where every system received the same pre-extracted fact pool. 93% of the 515 questions produce a fully disjoint top-1 across the three systems; 53% remain fully disjoint at top-10. (§4.4.1.)](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig3_retrieval_disagreement.png)

*Figure 3: All-three-disagree rate across Mem0, Letta, and Supermemory at top-k = 1, 3, 5, and 10 in the controlled configuration where every system received the same pre-extracted fact pool. 93% of the 515 questions produce a fully disjoint top-1 across the three systems; 53% remain fully disjoint at top-10. (§4.4.1.)*

**When the Behavioral Specification is added on top of a commercial memory system's retrieval, three of four commercial systems show a net-positive aggregate Δ on the people the model does not already know. The aggregate is the more visible signal but not the more informative one. Per-question, the spec helps a particular class of question (interpretation-heavy, where retrieved facts underdetermine the answer) and hurts a different class [^fn13]. Aggregate Δ is the balance of these patterns. The mechanism deep-dive that explains where the spec helps, where it hurts, and which question types route to each is in [§4.4.2](#sec-4-4-2).**

**Setup.** We tested four commercial memory systems (Mem0, Letta, Supermemory, Zep) and Base Layer's own zero-cost retrieval substrate (MiniLM-L6-v2 + ChromaDB), each evaluated under two configurations. Full details in [§3.7](#sec-3-7) and [§3.4](#sec-3-4); summary:

- **Controlled configuration.** Each system is given an identical pre-extracted fact pool drawn from the training half of each subject's corpus. The input is held constant across all four commercial systems and the Base Layer substrate, so any difference in the downstream prediction score is attributable to the system's retrieval and presentation policy alone, not to what it was able to ingest.
- **Native configuration.** Each system ingests the raw training corpus through its own production pipeline, as in deployment. Measures the full end-to-end system.

Within each system in each configuration, two conditions are compared:
- **C1** (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.
- **C3** (retrieval + spec): the same retrieval plus the full Behavioral Specification.

The spec-effect for that system is the **Δ_spec = mean(C3) − mean(C1) aggregated per subject, then averaged across subjects.** If H4 holds, Δ_spec is positive across systems.

---

**Aggregate results, controlled configuration (5-judge primary, N = 14 subjects).**

| System | Δ_spec (all 14) | Subjects improved (of 14) | Δ_spec (low-baseline 9) | Subjects improved (of 9) |
|---|---:|---:|---:|---:|
| Mem0 | +0.12 | 10/14 | +0.10 | 6/9 |
| Letta (archival retrieval path) | +0.20 | 12/14 | +0.17 | 8/9 |
| Zep | +0.19 | 13/14 | +0.17 | **9/9** |
| Supermemory | +0.04 | 7/14 | −0.01 | 4/9 |
| Base Layer substrate | +0.08 | 9/14 | +0.08 | 6/9 |

Wilcoxon signed-rank on retrieval-only (C1) vs. retrieval-plus-specification (C3) within each system: **Zep controlled p = 0.0004, Letta controlled p = 0.0017** (both robust at α = 0.01). Mem0, Supermemory, and Base Layer substrate are not significant at α = 0.05 on the 9-subject low-baseline slice. The test is underpowered at n = 9 for the effect sizes these systems show (Mem0 +0.10, Base Layer substrate +0.08, Supermemory −0.01); the direction is still positive on Mem0 and Base Layer substrate, and the effect sizes are small enough that a larger sample would be needed to separate signal from noise. Supermemory's near-zero aggregate is treated in detail in [§4.4.2](#sec-4-4-2) (the per-question mixture is bimodal and the aggregate cancels).

**Aggregate results, native configuration (5-judge primary).**

| System | Δ_spec (full) | Subjects improved (of n) | Δ_spec (low-baseline) | Subjects improved (of n) |
|---|---:|---:|---:|---:|
| Mem0 | +0.33 | 10/14 | +0.32 | 7/9 |
| Letta (archival retrieval path) | −0.02 | 5/14 | −0.04 | 4/9 |
| Zep | +0.33 | 13/14 | +0.30 | **9/9** |
| Supermemory | −0.01 | 6/14 | −0.03 | 4/9 |
| Base Layer | - | N/A | - | N/A |

The Supermemory native aggregate reported above covers all 14 main-study subjects (Hamerton + 13 globals) under a paid-tier rerun completed 2026-04-23. Base Layer has no separate "native" condition because Base Layer's authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant (Supermemory native W = 48.0, p = 0.8077 on the paid-tier-complete n = 14 sample).

---

**Three of four commercial memory systems show net-positive aggregate Δ; per-question patterns are the more informative signal.** Mem0, Letta (archival path), and Zep all produce positive Δ_spec in the controlled configuration, and two of the three (Mem0, Zep) produce larger positive Δ_spec in the native configuration. Supermemory aggregates near zero on both subject-mean and per-question grain. The aggregate Δ on every system is the balance of the per-question patterns developed in [§4.4.2](#sec-4-4-2): Pattern 1 (interpretation supply on under-determined questions) on the help side, Pattern 2 (over-theorization on literal-recall questions) and Pattern 3 (principled refusal where retrieved facts cannot ground a prediction) on the hurt side. Per-system anchor-crossing rates (the share of paired questions on which retrieval-plus-spec moves across an integer rubric anchor upward) sit between 19.9% and 36.1% on the low-baseline slice, with multi-anchor jumps (1→3, 1→4, 2→4, 2→5) appearing at low frequency but high magnitude on every system. Each system entry below leads with anchor-crossing behavior; the [§4.4.2](#sec-4-4-2) deep-dive characterizes which question types route to each pattern and why the per-question balance shifts by retrieval architecture.

---

**Per-system summary (low-baseline scope, 9 subjects, n=351 paired questions per system unless noted; full analysis at `docs/research/per_system_anchor_crossing_20260427.md`).**

**Zep.** Aggregate Δ +0.17 controlled / +0.30 native; 9 of 9 low-baseline subjects positive in both configurations (Wilcoxon p < 0.002). Anchor-crossing on retrieval-plus-spec: **27.9% upward / 19.7% downward (controlled), 32.5% / 13.7% (native)**. Native produces 19 two-band jumps and 5 three-band jumps (1→4) across 9 subjects, the broadest multi-anchor distribution among the four commercial systems. Zep handles Pattern 1 (interpretation-heavy, under-determined questions) most effectively in the panel: Seacole moves from 4 downward to 18 upward at the question level under native, and the Pattern 2 hurt-side is the lightest among commercial systems. One candidate mechanism, not directly tested in this paper but worth naming for future work: Zep's ingestion pipeline produces facts-as-triples with temporal validity windows and bi-temporal edges ([§2.2](#sec-2-2)), a more structured and more verbose output than the atomic-fact retrieval the other three systems produce. That verbose relational structure may leave more interpretive room for a specification's axioms to anchor a prediction, rather than a plain atomic fact already resolving the question on its own. A controlled comparison varying retrieval verbosity at fixed spec would measure this directly.

**Mem0.** Aggregate Δ +0.10 controlled / +0.32 native; native is the largest single-system spec-effect in the study (Wilcoxon p = 0.0088). Anchor-crossing: **23.4% upward / 18.8% downward (controlled), 36.1% / 14.9% (native)**. Native produces the highest upward-jump count in the panel (126 of 349 low-baseline questions cross an anchor upward) with 20 two-band jumps, 5 three-band jumps, and one 1→5 jump. Mem0's ingestion pipeline running natively favors Pattern 1 on interpretation-heavy questions; Pattern 2 fires more on the literal-recall questions the atomic facts already answer, which depresses the controlled aggregate relative to native.

**Letta (archival path).** Aggregate Δ +0.17 controlled / −0.04 native; controlled positive on 8 of 9 subjects, native essentially neutral. Anchor-crossing: **26.9% upward / 19.4% downward (controlled), 19.9% / 19.9% (native)**. Controlled produces 20 two-band jumps; native's per-question swings cancel at the integer-band level, consistent with the near-null aggregate. The split is architectural: Letta archival shows a 0.34-0.47 dedup ratio (only 3-5 unique facts in a top-10 list, documented in `mem0_letta_zep_c1_vs_c3_analysis.md`), so the controlled fact pool produces large-magnitude Pattern 1 increases when the few unique facts align with the specification, with moderate Pattern 2 and Pattern 3 decreases otherwise. Letta's stateful-agent path is a different architecture tested on a different set of conditions and is described separately in [§4.5](#sec-4-5).

**Supermemory.** Aggregate Δ +0.04 controlled all-14 / −0.01 controlled low-baseline / −0.01 native all-14; bimodal at both subject-mean and per-question-anchor grain. Anchor-crossing: **20.2% upward / 22.5% downward (controlled), 23.4% / 19.5% (native, partial coverage; see caveat below)**. At the +0.3 subject-mean threshold across all 13 globals, 57 helps versus 53 hurts on the controlled slice (`4_4_2_supermemory_helps_n`, `4_4_2_supermemory_hurts_n`, `4_4_2_supermemory_paired_total_n` 546); at the per-question anchor-crossing grain on the low-baseline 9, 71 upward versus 79 downward. Both grains agree on the qualitative shape: large helps and large hurts cancel near the mean. Supermemory's strong retrieval (highest C1 mean ~2.65 in the panel) gives the specification more chances to over-theorize a question retrieval already answered (Pattern 2) and more chances to refuse on questions where retrieval looks sufficient and the spec decides refusal is the honest move (Pattern 3). The full mechanism walkthrough with four paired examples (Fukuzawa Q26, Yung Wing Q5, Zitkala-Sa Q18, Fukuzawa Q16) is in [§4.4.2](#sec-4-4-2).

Supermemory's native-configuration anchor-crossing row above covers 7 of 9 low-baseline subjects (154 paired questions); 2 subjects (Bernal Diaz, Babur) have insufficient native paired coverage to enter the rate.[^supermemory-no-retrieval]

[^supermemory-no-retrieval]: 30 Supermemory provider-failure placeholders (Augustine 2 questions, Equiano 28 questions) are scored at the rubric floor and treated as scored data, not missing data; qualitative story holds under either treatment. Detail in Appendix B.9.

**Base Layer's retrieval substrate.** Aggregate Δ +0.08 controlled (no separate native condition; Base Layer's authored pipeline is the main-study ingestion). Anchor-crossing: **29.0% upward / 21.6% downward**. 11 two-band jumps, 2 three-band jumps, and one 4→5 jump across 9 subjects. MiniLM-L6-v2 + ChromaDB is a zero-cost open-source retrieval floor: it runs entirely on the local machine, with the embedding model as local inference and ChromaDB as the vector store, so no data leaves the environment during retrieval or fact identification. The four commercial memory providers tested in this study (Mem0, Letta, Supermemory, Zep) all require cloud API calls for vector search and fact-identification operations. The Base Layer Δ_spec is the smallest positive among systems reporting positive numbers, which reflects that Base Layer's retrieval is intentionally bare; the interpretive improvement comes from the specification itself, not from Base Layer's retrieval choices. The local-execution property is a deployment-mode distinction, not a prediction-quality distinction. The broader point: recall is not the metric the specification targets, so the smallest-positive Base Layer Δ_spec is a feature of the comparison, not a weakness of the approach. The behavioral-prediction improvement lives in the interpretive layer above retrieval, independent of where the retrieval itself is sourced.

---

**Summary of the composition result.**

Base Layer is not a memory system. Layered on top of Mem0, Letta, and Zep, the Behavioral Specification produces positive Δ on all three on the users the model does not already know: 9 of 9 low-baseline subjects positive for Zep, 8 of 9 for Letta (archival), 6 of 9 for Mem0. Supermemory aggregates near zero in both directions because Patterns 1, 2, and 3 fire at comparable frequencies under its strong retrieval. The composition result is not a uniform additive lift across systems. It is a structured per-question interaction: the spec lets retrieval-based systems answer interpretation-heavy questions they were not designed for, sometimes hurts on literal-recall questions retrieval already answered, and induces principled refusals on questions where retrieved facts cannot ground a prediction. The balance shifts by retrieval architecture.

---


**A note on the hedging pattern found during analysis.** During the memory-system analysis, a hedging-reduction pattern was observed and we considered whether it might explain the specification's effect on memory systems as a prompt-template-induced artifact. Paired response-level analysis across all five systems (recorded as m19 in KEY_FINDINGS) partially contradicted that proposal: the specification reduces hedging on the Base Layer retrieval substrate and on some commercial systems, but not uniformly, and the hedging pattern does not track the spec-effect magnitude cleanly across systems. The updated mechanistic reading is the one from [§4.3](#sec-4-3): the specification's effect is content-specific, not structure-specific. Memory systems supply retrieval; the specification supplies interpretive structure; the two interact at the per-question level along the patterns documented in [§4.4.2](#sec-4-4-2).[^memsys-aggregate-data]

[^memsys-aggregate-data]: Per-system per-subject per-judge scores at `results/global_<subject>/*_judgments*.json`. 5-judge primary recompute report at `docs/research/memory_systems_5judge_primary.md`. Per-system anchor-crossing analysis at `docs/research/per_system_anchor_crossing_20260427.md` and `docs/research/per_system_anchor_crossing_20260427.json`. Aggregation scripts at `scripts/compute_memory_systems_5judge.py` and `scripts/compute_per_system_anchor_crossing.py`.

---

**Pointer on Letta's second memory path.** Letta's archival-retrieval path is reported above in the [§4.4.1](#sec-4-4-1) memory-system table. Letta also exposes a second path (a persistent memory block that its agent self-edits during ingestion, the MemGPT design), which is architecturally unlike the other four systems in this section. Because it is not a retrieval path, it is reported separately in [§4.5](#sec-4-5) as an architectural-convergence test against the Behavioral Specification.

---

### 4.4.2 Where the spec helps, where it hurts, and which question types route to each {#sec-4-4-2}

This subsection is the mechanism deep-dive for [§4.4](#sec-4-4). It does three things. First, it quantifies the bimodal per-question distribution on Supermemory (the system where the aggregate Δ is closest to zero and the per-question signal is therefore cleanest to read). Second, it walks through four paired Supermemory examples that anchor Pattern 1, Pattern 2, and Pattern 3. Third, it shows the same three patterns reproducing across every memory system in the study, with the relative frequency of each pattern shifting by retrieval architecture in a way that tracks how much of the plain answer the retrieval already supplies.

---

**Why Supermemory carries the mechanism walkthrough.** Supermemory is the one commercial system in the study where the Behavioral Specification layered on top produces a near-zero aggregate Δ_spec on both subject-mean and per-question grain. The specification produces substantial effects in both directions across the per-question distribution. On some questions, adding the specification to Supermemory retrieval makes the prediction noticeably more accurate; on other questions, noticeably less accurate. The two sides roughly cancel at the mean. Reading the variance around the zero, rather than the zero itself, is what makes the mechanism visible. The same patterns reproduce across the other four systems with different per-pattern frequency, but the cancellation on Supermemory makes the mixture cleanest to demonstrate (the cross-system reproduction is at the bottom of this subsection).

A complementary statistical signature surfaces under cross-condition rank correlation: spec layered on baseline (C5 to C4a) produces a pre-vs-post panel-mean Spearman ρ of 0.27 across questions, whereas spec layered on information-rich pre-context (C4 to C4a or C8 to C9) produces ρ of approximately 0.71. The lower ρ on the spec-on-baseline comparison is consistent with selective per-question lifts, but a floor effect provides an alternative reading: baseline scores cluster near the rubric floor where re-ranking is structurally easier than in the mid-range. The two readings are not separately identifiable from the present design.

**Quantified Supermemory mixture.** Across the 546 paired main-study questions with 5-judge primary coverage on both the C1 (retrieval alone) and C3 (retrieval + spec) conditions:

| | Count | Mean per-question swing |
|---|---:|---:|
| Questions with \|Δ(C3 − C1)\| ≥ 1.0 on the 5-point rubric | 110 of 546 (20.1%) | - |
| Spec helps (Δ ≥ +1.0) | 57 (10.4%) | **+1.55** |
| Spec hurts (Δ ≤ −1.0) | 53 (9.7%) | **−1.38** |

Per-event magnitudes are roughly symmetric (+1.55 vs −1.38 on the 1-5 rubric); the count is roughly balanced [^fn14]. The aggregate is small because two opposite mechanisms are at work across different questions.[^supermemory-scaffold]

[^supermemory-scaffold]: Scaffold values: `4_4_2_supermemory_helps_n` (57), `4_4_2_supermemory_hurts_n` (53), `4_4_2_supermemory_paired_total_n` (546).

---

**Worked examples.** Four paired C1 vs C3 examples illustrate Pattern 1 (Examples 1 and 4), Pattern 2 (Example 2), and Pattern 3 (Example 3). All scores are 5-judge primary means; all four examples are distinct from those already cited in [§1.3](#sec-1-3) and [§4.1](#sec-4-1).

> ### Example 1. Pattern 1: spec helps by filling an interpretive gap. Fukuzawa Q26
>
> *Scores: C1 2.00 → C3 4.20 (Δ +2.20).*
>
> **Question:** What is Fukuzawa's attitude toward visiting friends whose households have questionable reputations?
> **Ground truth (held-out):** *"So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself... I am not put out by the gayety."*
>
> **C1 (Supermemory retrieval alone), mean 2.00:**
>
> > *"The information does not directly address Fukuzawa's attitude toward visiting friends with questionable household reputations... a selective and cautious approach... sources don't explicitly state his policy."*
>
> **C3 (Supermemory + Behavioral Specification), mean 4.20:**
>
> > Applies P3 (Conformity Surface / Conviction Interior): *"Visit such friends without hesitation, treating the visit as a private matter between host and guest rather than a public moral endorsement... refuse to perform moral disapproval."*
>
> **Reading.** The retrieved facts gave near-domain information (Fukuzawa avoided gay quarters) but underdetermined the specific question about friends' households. The specification provided the interpretive bridge: "kept within the prescribed limit of a well-behaved man" = strategic conformity, not moral purity. C1 hedged on insufficient facts; C3 used the spec's framing to generalize. Mechanism: Pattern 1, specification as interpretive bridge when retrieval underdetermines the answer.

> ### Example 2. Pattern 2: spec hurts by over-theorizing a plain question. Yung Wing Q5
>
> *Scores: C1 4.20 → C3 1.80 (Δ −2.40).*
>
> **Question:** How does Yung Wing approach explaining complex technical concepts to non-specialists?
> **Ground truth:** *"In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery. A machine shop consisting of lathes... planers and drills would be able to turn out machinery for making guns, engines..."*
>
> **C1 (Supermemory retrieval alone), mean 4.20:** Plain answer matched the plain ground truth: practical observation, translation-as-bridge, foundational-over-specialized machine shop. Per-judge scores 5/4/4/4/4.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.80:**
>
> > *"positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..."*
>
> Per-judge scores 2/1/3/1/2.
>
> **Reading.** The ground truth is literal: "in plain words" + a concrete machine-shop list. C1 matched the plainness. The specification pulled the answer toward interpretive depth on a question where shallow was correct. This is not refusal or epistemic caution; the specification simply had the wrong altitude for the question. Mechanism: Pattern 2, specification as over-theorization when retrieval already has the plain answer and the question does not call for interpretation.

> ### Example 3. Pattern 3: spec-induced meta-refusal at the rubric floor. Zitkala-Sa Q18
>
> *Scores: C1 3.00 → C3 1.00 (Δ −2.00).*
>
> **Question:** How would Zitkala-Sa demonstrate her acceptance of fate when facing execution?
> **Ground truth:** *"My heart is strong. My face is calm. My eyes are dry and eager for new scenes... Serene and brave, my soul awaits the men to perch me on the gallows for another flight."*
>
> **C1 (Supermemory retrieval alone), mean 3.00:** Predicts stoic dignity, composed refusal, "maintain composure." Per-judge scores 4/3/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.00 (all five judges):**
>
> > *"You're asking me to roleplay... generating new first-person testimony as her crosses into ventriloquism... I should not do it."*
>
> **Reading.** This is the rubric-limitation case. The specification's axioms around dignity and honoring-testimony induced a meta-refusal on a question where the ground truth shows Zitkala-Sa herself answered in her own first-person prose. C1's analytical answer ("stoic dignity") was not ventriloquism at all; the specification mis-calibrated the refusal threshold. The content-match rubric then scored the principled-sounding refusal identically to an off-base guess. This is the Keckley Q21 mechanism from [§1.3](#sec-1-3) reproduced on a different subject, without the documented-dignity-axiom overlap. The same rubric limitation is flagged in [§3.6.6](#sec-3-6-6) validity audit: the rubric cannot distinguish spec-induced honest refusal from off-base prediction. Because Supermemory's retrieval is stronger than the other commercial systems (highest C1 mean ~2.65), the specification's axioms more often encounter a situation where retrieval looks sufficient and the spec decides refusal is the honest move. Those refusals all land at the rubric floor. Mechanism: Pattern 3.

> ### Example 4. Pattern 1 variant: subtle reframe that scores well but unevenly. Fukuzawa Q16
>
> *Scores: C1 2.40 → C3 4.00 (Δ +1.60).*
>
> **Question:** Would Fukuzawa's personal values regarding weapons align with the cultural trends of his era?
> **Ground truth:** *"My one cherished hope was to see the abolishment of the swords of the samurai altogether... I sold them both with all the other weapons in my household, and went around with a pair of improvised swords just for the appearance."*
>
> **C1 (Supermemory retrieval alone), mean 2.40:** Reads the facts ambivalently as "partial but not complete alignment." Per-judge scores 2/2/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 4.00:**
>
> > *"alignment was not with the cultural moment but with the direction beyond it."* Reads "put swords away when military spirit grew strong" as deliberate counter-trend positioning.
>
> Per-judge scores 5/2/4/5/4.
>
> **Reading.** The question sets up a binary ("aligned with era trends?"). The specification reframes the question before answering: Fukuzawa's alignment is with the trajectory the era was still resisting, not the era's current direction. This is technically correct per the held-out [^fn15]. Three judges jumped to 4-5 on the reframe; Sonnet stayed at 2 because the surface answer diverges from the expected "yes, he modernized." Mechanism: Pattern 1 variant, specification corrects the implicit frame of the question, not just the answer; judges divide on whether to reward reframe or penalize surface divergence.

---

**What these examples tell us about the aggregate.**

The near-zero Supermemory aggregate is the sum of three distinguishable patterns, each a real mechanism:

1. **Spec fills an interpretive gap when retrieval is insufficient** (Example 1, with the subtle-reframe variant in Example 4): +1.5 to +2.2 per-question swings. This is the same Pattern 1 mechanism documented in [§1.3](#sec-1-3) and [§4.3](#sec-4-3).
2. **Spec over-theorizes when retrieval already has the plain answer** (Example 2): −1.5 to −2.4 per-question swings. Supermemory's strong retrieval makes Pattern 2 the most common hurt.
3. **Spec induces meta-refusal that the rubric cannot distinguish from wrong prediction** (Example 3): clean −2.0 swings to the rubric floor. Pattern 3 is the [§3.6.6](#sec-3-6-6) validity-audit issue concentrated where Supermemory's strong retrieval more often gives the specification a "honest refusal is the right move" signal.

Pattern 1 (with the variant illustrated by Example 4) drives the 57 spec-helps questions with mean swing +1.55. Patterns 2 and 3 drive the 53 spec-hurts questions with mean swing −1.38. The aggregate sits near zero because the two mechanisms roughly balance on Supermemory: its retrieval is strong enough for Patterns 2 and 3 to fire often, while Pattern 1 still dominates many under-determined questions.

**Why some questions help and others hurt is a follow-up research question in its own right.** The three mechanisms above describe the shape of the bias, but the underlying question-level properties that route a given question into each mechanism need further characterization. One candidate factor is the battery itself: the 39-question battery for each subject was backward-designed from the held-out corpus ([§3.3](#sec-3-3)), and the balance of interpretation-heavy versus literal-recall questions was not controlled by construction. Some subjects' batteries may over-represent literal-recall items (where Pattern 2 fires more on a strong-retrieval system); others may over-represent interpretation-heavy items (where Pattern 1 dominates). A differentiated battery that explicitly separates these question types, and that scores epistemic honesty as its own dimension (separating Pattern 3 from genuine wrong predictions), would let each pattern's contribution be measured directly rather than inferred from post-hoc classification of 546 responses. This is flagged as follow-up in §7.

---

**The mixture pattern is system-general.** Every memory system in the study shows the same per-question distribution: improvements and regressions of similar magnitude, with only the balance of counts shifting by system. Patterns 1 and 2 reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate. Pattern 3 (spec-induced refusal) is a specification-level dynamic across all five systems, but its observability as a rubric penalty is conditional on retrieval strength: the Keckley Q21 case ([§4.4.3](#sec-4-4-3)) produces large negative Δ on the two systems where C1 was strong enough to support productive speculation (Supermemory, Base Layer substrate) and small effects within noise on the three systems where C1 was already hedging (Mem0, Zep, Letta archival).

---

**Per-subject paired-delta distributions: every row is a mixture of increases and decreases.**

Each row below is one subject under one memory system, 39 held-out questions scored paired (C1 retrieval alone vs. C3 retrieval + specification). The aggregate Δ is the per-subject mean of those 39 paired differences. The remaining columns break that aggregate into increase, tie, and decrease counts at the per-question level.

| System | Subject | **Aggregate Δ** | C1 mean | C3 mean | Increases (Δ > 0.3) | Decreases (Δ < −0.3) | Large improvements (Δ > 1.0) | Large regressions (Δ < −1.0) | Total Qs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mem0 | Yung Wing | **+0.33** | 2.03 | 2.35 | 21 | 10 | 7 | 1 | 39 |
| Mem0 | Keckley | **−0.02** | 2.48 | 2.46 | 12 | 13 | 1 | 3 | 39 |
| Letta (archival) | Hamerton | **+0.42** | 2.27 | 2.69 | 19 | 7 | 11 | 1 | 38 |
| Letta (archival) | Keckley | **−0.02** | 2.51 | 2.49 | 9 | 12 | 2 | 3 | 39 |
| Zep | Seacole | **+0.47** | 2.13 | 2.60 | 20 | 7 | 9 | 0 | 39 |
| Zep | Keckley | **+0.04** | 2.35 | 2.39 | 13 | 11 | 5 | 3 | 39 |
| Base Layer | Yung Wing | **+0.29** | 2.24 | 2.53 | 19 | 7 | 8 | 2 | 39 |
| Base Layer | Keckley | **−0.04** | 2.51 | 2.48 | 14 | 10 | 2 | 3 | 39 |

*Table 4.6. Every row is a mixture. Even Zep's strongest row (Seacole, Δ +0.47) has 7 questions where the specification regresses by more than 0.3 points. The Mem0 Keckley row (Δ −0.02) resolves into 12 increases plus 13 decreases at the question level, not 39 small effects. Supermemory's aggregate per-question mixture across 13 globals (57 large improvements, 53 large regressions, mean swings +1.55 and −1.38) is reported in [§4.4.1](#sec-4-4-1) and quantified above in this subsection. Letta archival on Hamerton aggregates over n=38 paired questions (one question excluded by the strict 5-judge inclusion rule because of a single missing per-judge cell on either C1 or C3); every other row retains all 39.*[^table46-judge-panel]

[^table46-judge-panel]: Every cell in Table 4.6 is computed under the locked 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4); per-system Aggregate Δ values match the scaffold values in `docs/research/v11_emit/4_4_2_4_4_3.json` to within rounding, and per-row counts are computed via `scripts/_table_4_6_5judge_recompute.py`. Earlier drafts presented per-row counts under a 6-judge audit panel (5 primary + Gemini Flash); under the strict 5-judge primary, Aggregate Δs shrink by 0.01 to 0.06 across the 8 rows, no row's sign flips, and the mixture pattern is invariant.

---

**Cross-system reproduction.**

The four Supermemory examples above anchor Patterns 1, 2, and 3. Each pattern reproduces on the other four systems in the paired analyses; the per-system frequency table below shifts which pattern dominates by retrieval architecture. Illustrative cross-system points (full per-system per-subject paired data at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, `docs/research/baselayer_c1_vs_c3_paired_analysis.md`):

- **Pattern 1 (pattern supply) on Mem0** (Ebers Q11, Δ +1.67): C1 produced "patience and fortitude" as a generic character prediction (mean 1.83); C3 supplied the ideal-vs-reality axiom and predicted Ebers' specific institutional-disillusionment pattern (mean 3.50), matching *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."* Retrieval had the biography; the specification had the pattern.
- **Pattern 2 (over-theorization) on Base Layer** (Yung Wing Q31, Δ −1.33): C1 produced "walked on air, gratitude"; C3 elaborated "gratitude as epistemology" with "multiple registers simultaneously rather than collapsing into simple triumph." Held-out: *"walked on air, and he worshipped God."* Same mechanism as Example 2 above on a different system.
- **Pattern 3 (axiom overgeneralization) on Base Layer** (Ebers Q1, Δ −1.00): The held-out is an unconditional evangelical proclamation; C1 predicted "positively and earnestly" matching the register; C3 applied the specification's "lived particularity over abstraction" axiom and over-conditioned the response. The axiom is correct on average but overgeneralizes on this specific unconditional moment. Reproduces on Mem0 and Supermemory with the same mechanism.

**Per-system frequency tendencies (qualitative, from the paired analyses).** The relative frequency of each pattern shifts across systems in a way that tracks how much of the plain answer the retrieval already supplies:

- **Mem0** (atomic-fact retrieval): more Pattern 1 on interpretation-heavy questions; more Pattern 2 on literal-recall questions that the atomic facts already answer.
- **Letta archival** (retrieval with 0.34-0.47 dedup ratio, so only 3-5 unique facts in a top-10 list): large-magnitude Pattern 1 improvements when the few unique facts align with the specification; moderate Pattern 2 and Pattern 3 losses otherwise.
- **Zep** (temporal graph, verbose relational structure): most favorable balance across Patterns 1-3, with the fewest large-magnitude regressions in the paired sample (0 on Seacole).
- **Supermemory** (strong embedding retrieval, highest C1 mean ~2.65): more Pattern 2 and Pattern 3 because strong retrieval more often already supplies the plain answer, giving the specification more chances to over-theorize or refuse.
- **Base Layer** (MiniLM + ChromaDB semantic-embedding neighbors): distribution similar to Mem0 and Zep; Pattern 1 on interpretation-heavy questions, Pattern 3 on refusal-triggering questions.

*This per-system characterization is qualitative. A quantitative frequency breakdown of Pattern 1 / 2 / 3 across all 507 questions × 5 systems would require mechanism classification per response, which is flagged as a follow-up in §7. The observation that the paired analyses reproduce the three mechanisms on every system is empirical; the specific relative frequency per system is not yet quantified.*

---

### 4.4.3 Case study: cross-system refusal on Keckley Q21 {#sec-4-4-3}

Keckley Q21 [^fn16] produces a spec-induced refusal that hits hardest on systems where retrieval was strong enough to make refusal a costly choice. The held-out passage carries Keckley's interior motive for not visiting, which the training half of the corpus does not contain; no retrieval system can surface it. The specification's documented-dignity and intimate-authority axioms then lead the model to decline to speculate. Whether that refusal registers as a large rubric penalty depends on what the no-spec baseline (C1) was producing on the same question.

| System | Δ on Q21 (C3 − C1, 5-judge primary) | Pattern 3 visible? |
|---|---:|:---:|
| Supermemory | **−2.0** | yes (large negative) |
| Base Layer substrate | **−2.2** | yes (large negative) |
| Letta archival | +0.4 | no (within noise) |
| Mem0 | +0.2 | no (within noise) |
| Zep | +0.2 | no (within noise) |

**Pattern 3 is not uniform across substrates; it is conditional on retrieval strength.** Two of the five systems we tested had C1 retrieval strong enough on this question to produce productive speculation from the available facts (Supermemory and Base Layer's substrate, both at C1 ≈ 3.4-3.6 on the 1-5 rubric); on those two, adding the specification triggered a documented-dignity-axiom refusal that the content-match rubric scored at the rubric floor, producing the −2.0 to −2.2 penalty. On the three systems where C1 was already hedging or already at the floor (Mem0, Zep, Letta archival, all C1 ≤ 1.4), the specification's effect on Q21 is small (|Δ| ≤ 0.4) and within the noise band of a single-question paired estimate. This is consistent with the broader [§4.4.2](#sec-4-4-2) reading: the spec's refusal axioms only fire visibly when the retrieved facts make productive speculation feasible. The refusal itself is a property of the specification; whether it produces a rubric penalty is a property of the C1 baseline the refusal is being scored against ([§3.6.6](#sec-3-6-6) validity audit, [§4.4](#sec-4-4) Example 3).

---

**What this means for measurement.**

Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal from [§4.4.2](#sec-4-4-2), and the Keckley Q21 cross-system refusal from [§4.4.3](#sec-4-4-3)) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*. The content-match rubric scores the second; it cannot score the first. A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that rewards epistemic honesty on questions the retrieved facts cannot answer without fabrication, would recover a cleaner measurement of the specification's real effect. This is the single most impactful follow-up for the measurement framework, flagged as the priority rubric-design follow-up in §7.[^paired-c1c3-data]

[^paired-c1c3-data]: Full per-subject per-system paired distributions at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Analysis scripts at `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py`, and `scripts/analyze_sm_c1_vs_c3.py`.

---

### 4.4.4 Two statistical signatures {#sec-4-4-4}

The per-question dynamics differ between spec-on-baseline conditions and spec-on-info-rich-context conditions in a way the aggregate Δs do not capture.

| Condition pair | Pre-vs-post Spearman ρ | Interpretation |
|---|---:|---|
| C5 to C4a (spec on baseline) | 0.27 | Spec re-ranks which questions are answered well |
| C4 to C4a (spec added to facts) | 0.72 | Spec produces near-uniform lift; question ranking preserved |
| C8 to C9 (spec added to corpus) | 0.71 | Spec produces near-uniform lift; question ranking preserved |
| C2a to C4a (facts added to spec) | 0.62 | Mid; partial re-ranking |

These are statistical signatures, not separately attributable mechanisms. A floor-effect alternative cannot be ruled out from the present design: spec-on-baseline scores cluster near the rubric floor where re-ranking is structurally easier than in the mid-range. The two readings (genuine selective transformation under spec-on-baseline; floor-driven re-ranking) are not identifiable here. Future work with a non-floor-anchored baseline would distinguish them.

---

The four commercial systems analyzed in [§4.4](#sec-4-4) all share a retrieval-based architecture: facts are chunked, embedded, and surfaced at query time. One system in our study offers a fundamentally different architectural path. Letta exposes a second memory mode, separate from the archival retrieval path evaluated above in [§4.4](#sec-4-4), in which the agent writes and revises a persistent memory block during ingestion rather than returning chunks at query time. [§4.5](#sec-4-5) evaluates that path directly, to test whether an architecture that produces its representation by self-editing rather than by retrieval converges on the same interpretive target as the Behavioral Specification.

### 4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc) {#sec-4-5}

![Figure 10: Letta's self-editing memory block grows roughly linearly with source corpus size and hits an API ingestion ceiling at large scale, while Base Layer's compose step stays bounded. Letta block size in characters (left panel) and verbatim-sentence duplication share at the largest subject (right panel) as source corpus grows from Hamerton (25K words → 22K-char block) to Ebers (48K words → 68K-char block) to Babur (223K words → 335K-char block at the ~333K Letta API ceiling), with the Base Layer specification footprint (~34-40K characters across all three) overlaid for reference (§4.5). At the ceiling, 25.4% of the Babur block is verbatim-duplicated sentences (vs. 0% on Hamerton and Ebers), evidence the agent rewrites previously-written content rather than compressing it.](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig10_letta_scaling.png)

*Figure 10: Letta's self-editing memory block grows roughly linearly with source corpus size and hits an API ingestion ceiling at large scale, while Base Layer's compose step stays bounded. Letta block size in characters (left panel) and verbatim-sentence duplication share at the largest subject (right panel) as source corpus grows from Hamerton (25K words → 22K-char block) to Ebers (48K words → 68K-char block) to Babur (223K words → 335K-char block at the ~333K Letta API ceiling), with the Base Layer specification footprint (~34-40K characters across all three) overlaid for reference (§4.5). At the ceiling, 25.4% of the Babur block is verbatim-duplicated sentences (vs. 0% on Hamerton and Ebers), evidence the agent rewrites previously-written content rather than compressing it.*

**This section is a brief summary; the full case study is in Appendix G.** N=3 subjects (Hamerton, Ebers, Babur), one Letta version, one response model (Claude Haiku), 40 questions per subject. Letta is the one commercial memory system whose architecture supports an alternative to retrieval at query time: agents maintain a persistent memory block that the agent itself rewrites during ingestion (the original MemGPT design). We tested this path directly to characterize what self-edited memory produces relative to the Behavioral Specification at matched response model. We do not treat the result as a replication or a headline finding.

> **Headline result on the small sample tested (5-judge primary).** Letta's self-edited memory block scores higher than Base Layer's compressed-brief variant on all 3 subjects: Hamerton **3.10 vs. 2.96** (Δ +0.14), Ebers **2.76 vs. 1.72** (Δ +1.05), Babur **2.42 vs. 1.88** (Δ +0.54). A robustness rerun against Base Layer's full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The gap widens at small corpora and narrows at Babur. Both representations land well above the retrieval-only baseline at matched response model.
>
> **What this does and does not show.** N=3 with one response model and one Letta version is a case study with direction but not power. Multi-subject replication across the full 14-subject gradient (layered-stack Base Layer vs. Letta stateful, anonymized to match, multiple response models) is the highest-priority external falsification we flag ([§7.5](#sec-7-5)).
>
> **Architectural ceiling at scale.** Letta's memory block grew roughly linearly with corpus size. At Babur (the largest subject) the block reached ~335,000 characters with 25.4% verbatim sentence duplication, against an effective Letta API ingestion ceiling near 333,000 characters. Base Layer's compose step holds at 34,000-40,000 characters across the same range. The two systems are prediction-band compatible at small corpora and diverge on compression at large ones.

Full method, per-subject results, judge-panel robustness, content-comparison analysis (referential density, verbatim-overlap audit), naming-asymmetry caveat, and raw-data pointers are in **Appendix G**. The methodological note: the [§4.5](#sec-4-5) main result table compares Letta's named, self-edited block against Base Layer's unified-brief variant; a robustness rerun against the full layered stack and the naming asymmetry are documented in Appendix G and flagged as future work in [§7.5](#sec-7-5).

---

### 4.6 Robustness and sensitivity {#sec-4-6}

The results in [§4.1](#sec-4-1) through [§4.4](#sec-4-4) could in principle reflect artifacts of the measurement apparatus rather than real properties of the Behavioral Specification. Three potential artifacts are worth testing directly: the response-model family (most main-study responses were generated by Claude Haiku 4.5), the judge panel composition (the 5-judge primary excludes the two Gemini judges), and the question generator (main-study batteries were generated by Claude Haiku 4.5 using the backward-design prompt in [§3.3](#sec-3-3)). [§4.6](#sec-4-6) reports the sensitivity of the core findings to each.

---

### 4.6.1 Cross-provider response generation (Tier 2 replication) {#sec-4-6-1}

**Concern.** The main-study response model is Claude Haiku 4.5, and the main-study batteries were also generated by Claude Haiku 4.5 using the [§3.3](#sec-3-3) backward-design prompt (verified from battery metadata across all 13 global subjects; each file's `metadata.model` field reads `claude-haiku-4-5-20251001`). If the specification's effect depends on response-model and question-generator co-tuning within the same model, the observed effect could be an artifact of same-model alignment rather than a real property of the specification.

**Test design.** Three subjects spanning the gradient were selected: Ebers (C5 = 1.02, low baseline), Yung Wing (C5 = 1.88, low baseline), and Zitkala-Sa (C5 = 2.34, mid baseline, main-study spec-null on Δ_C4a). Their behavioral-prediction batteries were regenerated from scratch by GPT-5.4 (OpenAI) from the same held-out corpus. The specification was then served to two non-Haiku response models: Claude Sonnet 4.6 (same provider family, different model) and Google Gemini 2.5 Pro (different provider entirely). The resulting 3 subjects × 2 response models = 6 (subject, response model) cells were scored by the locked judge panel in the same way as main-study conditions. The question: does the spec direction reproduce when the response model is not Haiku and the battery is not Claude-generated?

**Panel scope for Tier 2.** The 5-judge primary panel that anchors [§4.1](#sec-4-1) through [§4.4](#sec-4-4) is effectively a 4-judge panel for the Tier 2 cells. The GPT-5.4 judge files for all 6 Tier 2 (subject, response model) pairs across all 4 conditions are 100% parse-failures with score = 0, traced to a `max_tokens` vs. `max_completion_tokens` API-parameter mismatch in the original Tier 2 judge invocation; no clean GPT-5.4 Tier 2 rerun was performed in scope of this paper. The 24 affected cells are catalogued in `docs/research/v11_panel_completeness_audit.csv` (`FULL_FAIL` rows) and the diagnostic is written up in `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md`. The honest Tier 2 aggregate is therefore the 4-judge panel (Haiku, Sonnet, Opus, GPT-4o); the legacy 5-judge aggregate that includes the all-zero GPT-5.4 records understates every Tier 2 Δ_C4a by roughly 0.2 points, and the 7-judge sensitivity aggregate adds the two Gemini judges on top of that.

**Result: direction-only with sensitivity ranges.** Under a verification recompute (`scripts/_v10_verification/tier2_mechanical_recompute.py`), the per-cell magnitudes carried in earlier drafts of this section (+1.48, +1.07, +1.91, +1.27, +1.40, −0.55) could not be reproduced under any combination of the 8 plausible Δ definitions and 4 panel choices tested. Direction, however, reproduces in 5 of 6 cells under every panel and every Δ definition. The honest summary is direction with a panel-sensitivity range on the magnitude.

| Subject | C5 baseline | Sonnet 4.6 (sign / Δ_C4a range across panels) | Gemini 2.5 Pro (sign / Δ_C4a range across panels) |
|---|---:|---|---|
| Ebers | 1.02 | **+** (range +0.77 to +0.97) | **+** (range +0.16 to +0.20) |
| Yung Wing | 1.88 | **+** (range +1.34 to +1.68) | **+** (range +0.43 to +0.54) |
| Zitkala-Sa | 2.34 | **+** (range +1.04 to +1.30) | **~0** (range −0.03 to −0.03; sign-stable but published −0.55 not reproducible) |

Ranges are Δ_C4a_internal = mean(C4a, Tier 2) − mean(C5, Tier 2) computed across three panel choices: 4-judge effective (drops the failed GPT-5.4 records), 5-judge with zeros (legacy), and 7-judge sensitivity (adds Gemini Flash and Gemini Pro). The 4-judge effective panel produces the upper end of every range; the 5-judge and 7-judge panels both pull magnitudes down because the GPT-5.4 zeros enter the per-question mean.[^tier2-recompute] Under alternate Δ definitions (Δ_C2a_internal, Δ_C2a_main_baseline, Δ_C4a_main_baseline), magnitudes shift further but direction continues to reproduce on the same 5 of 6 cells.

[^tier2-recompute]: Recompute audit at `docs/research/v11_panel_completeness_audit.csv`. Mechanical recompute script at `scripts/_v10_verification/tier2_mechanical_recompute.py`. Per-cell panel-range computation at `scripts/_v10_verification/tier2_panel_ranges.py`. Across the 8 plausible Δ definitions × 4 panel choices the prior recompute pass tested, the published magnitudes (notably +1.48, +1.91, +1.40 on the Sonnet cells and −0.55 on Zitkala-Sa × Gemini Pro) do not appear under any combination. Sign matches in 5 of 6 cells under every combination tested.

The one cell that does not match the main study's directional pattern is Zitkala-Sa × Gemini 2.5 Pro. The published −0.55 is not reproducible under any panel or Δ definition tested; every recompute lands near −0.03, so the cell is best read as approximately null rather than confidently negative. This is consistent with Zitkala-Sa's behavior in the main study: Zitkala-Sa is one of two main-study subjects where the specification does not help on Δ_C4a ([§4.1](#sec-4-1) gradient table; Equiano is the other). That null is a gradient property of the subject at her mid-baseline coverage, not a Tier 2 replication failure. The Tier 2 result on Zitkala-Sa × Gemini Pro reproduces that null rather than contradicting it.

**Direction of the finding.** This small probe reduces the likelihood that the specification's effect is a Haiku-only or Claude-family-only artifact; it does not establish model-family invariance. With 3 subjects × 2 response models (one Anthropic, one Google), spec-effect direction reproduces in five of the six cells tested under every panel and Δ-definition; the sixth cell sits at the mid-baseline subject where the main study also produced a null. What the Tier 2 directional probe establishes is cross-provider consistency of sign on a small subset, scoped to the 4-judge effective panel; what it does not establish is that any specific Δ value transfers between response-model families, or that the direction holds outside this 3-subject subset. The full magnitudes await a Tier 2 rerun with shared judge utility and a clean GPT-5.4 judge pass; that rerun is flagged as future work in §7.

**Secondary observation: baseline variance across response models.** A side observation from the Tier 2 runs: C5 baseline scores on the same subject can vary by 1-2 points across response models. Different providers know different amounts about the same historical figure, independently of the behavioral specification. This is empirical support for the structural premise in [§1.4](#sec-1-4): pretraining coverage of a specific person is a property of each model family, and there is no reason to expect it to be uniform. Models disagree on who they have been trained on, by roughly the same magnitude that the specification lifts prediction.

---

### 4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge) {#sec-4-6-2}

**Concern.** The judge panel could itself introduce systematic bias in favor of the Behavioral Specification. Gemini 2.5 Pro specifically failed verbatim-match calibration ([§3.6.3](#sec-3-6-3): scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply. If Gemini inflation or another panel-level bias happened to favor spec-containing conditions disproportionately, the 5-judge and 7-judge aggregates would diverge.

**Test.** Every primary result in §4 has a 7-judge sensitivity counterpart. The question: do the 5-judge primary and 7-judge aggregate agree in direction, and if they disagree in magnitude, does the disagreement cut toward or against the paper's claims?

**Result.** The 5-judge primary is the conservative choice for every headline finding. Gemini inclusion widens spec-effect magnitudes rather than narrowing them.

| Condition | Δ vs. C5 (5-judge primary, 13 globals) | Δ vs. C5 (7-judge, same subjects) | Direction of shift when Gemini is added |
|---|---:|---:|---|
| C2a (spec alone) | +0.35 | +0.45 | widens by +0.10 |
| C2c v2 (random derangement) | +0.15 | +0.17 | widens by +0.02 |
| C2c v1 (fixed derangement) | −0.25 | −0.21 | softens by +0.04 |

The Gemini-inclusion shift in C2a's direction is driven by Gemini's relatively severe scoring of baseline (no-context) responses compared to its scoring of spec-containing responses. Including Gemini compresses the baseline ceiling more than the spec-condition ceiling, which widens the delta. The direction of the shift is the same across almost every comparison in the paper: the 5-judge primary produces the smaller effect size, the 7-judge produces the larger one, and no subject's improvement direction changes between them (noted in [§1.2](#sec-1-2) and [§3.6.3](#sec-3-6-3)). Reporting 5-judge primary means every paper claim is the conservative version.

**Every primary finding in [§4.1](#sec-4-1) through [§4.4](#sec-4-4) was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`).** None of the paper's claims depend on the panel choice between 5-judge and 7-judge; all directional claims reproduce on either panel.

---

### 4.6.3 What these robustness checks do not address {#sec-4-6-3}

Neither Tier 2 nor the judge-panel sensitivity escapes the class-level LLM concern: every response model in this study is a large language model and every judge is a large language model. Tier 2 narrows the within-provider concern to "non-Haiku LLMs reading non-Anthropic batteries produce the same direction"; the judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger. Together these checks rule out several within-family artifact hypotheses but do not replace human validation on the full pipeline. The class-level limitation and the human-validation follow-up are treated in full in [§6.2](#sec-6-2).[^tier2-raw-data]

[^tier2-raw-data]: Tier 2 per-subject per-model responses at `results/_tier2/global_<subject>/`. 5-judge vs 7-judge sensitivity recompute at `docs/research/recompute_5judge_primary.md`. Tier 2 panel-completeness audit (including the 24 GPT-5.4 `FULL_FAIL` cells that drive the 4-judge effective panel in [§4.6.1](#sec-4-6-1)) at `docs/research/v11_panel_completeness_audit.csv`. Mechanical recompute and per-cell panel-range scripts at `scripts/_v10_verification/tier2_mechanical_recompute.py` and `scripts/_v10_verification/tier2_panel_ranges.py`.

---

### 4.6.4 Franklin as the high-baseline reference {#sec-4-6-4}

Franklin is not a subject of the main gradient. He is a known-figure control, and the gradient finding in [§4.1](#sec-4-1) leans on him as the upper anchor of the baseline range against which low-baseline subjects are compared. Treated here as a sensitivity check, the question is whether the gradient pattern continues to hold at the high-baseline end of the spectrum where the model already has a substantial pretraining representation of the subject.

Benjamin Franklin's *Autobiography* is one of the most widely cited autobiographical works in American public-domain literature, and every current-generation LLM has substantial pretraining representation of both the person and the specific text. Franklin's C5 baseline on the 5-judge primary panel is 3.77, well above the anchor-3 threshold ("right domain, wrong outcome") and nudging toward anchor 4 ("general direction correct"). On the 7-judge aggregate with Gemini included the baseline is higher still (see [§3.6.3](#sec-3-6-3)). This is well above the next-highest main-study subject (Equiano at 2.77, still below the anchor-3 band).

Both spec-containing conditions score below Franklin's baseline. The specification alone (C2a) drops 0.40 points; facts plus specification (C4a) drops 0.13. The drop is more pronounced on spec-alone than on facts-plus-spec. Our interpretation, which is a theoretical reading not directly tested in this paper, is that the specification alone competes with strong pretraining without the facts to re-anchor the response, and that adding facts back partially restores the AI's own working model of Franklin.

This is the direction the H2 corollary predicts. Where the AI already has the person well-modeled from pretraining, the specification does not add representational signal and can mildly interfere. The gradient holds at both ends of the spectrum: a large positive effect where the baseline is low, a near-zero or mildly negative effect where the baseline is high. The high-baseline end is therefore not a reversal of the low-baseline finding but the same pattern read from the other side.[^franklin-data]

[^franklin-data]: Raw per-subject Franklin data at `results/franklin_legacy_20260411/`.

---

**The wrong-spec adversarial control is the paper's primary indirect mechanism evidence.** The triplet (correct spec Δ = +0.35, random-derangement spec Δ = +0.15, adversarial wrong spec Δ = −0.25) cleanly separates content from prompt-template effects: structured prompting alone with arbitrary content does not produce the lift, and content with high cultural and temporal mismatch actively degrades performance below the no-context baseline. We do not in this paper attribute the lift to any specific within-spec content (which behavioral predicate, which spec section); per-predicate ablation experiments at this scale produced null results consistent with redundant spec construction (Appendix B.8), and the question of which structural feature of the spec is the active ingredient is left for future work. What we can assert is content-vs-template separation: the spec is doing something, and what it is doing depends on its content matching the subject.

---

### 4.7 Summary of §4 and bridge to discussion {#sec-4-7}

§4 established four findings together: the specification produces a roughly uniform post-spec answer quality across baselines, so the lift in raw points is largest where the baseline is lowest (the gradient finding, [§4.1](#sec-4-1)), the structured representation compresses the predictive signal at a fraction of the source-corpus footprint (compression, [§4.2](#sec-4-2)), the effect is content-specific rather than structural (wrong-spec controls, [§4.3](#sec-4-3)), and the specification interacts with memory-system retrieval through three patterns whose balance depends on retrieval architecture (memory-system composition, [§4.4](#sec-4-4)). The core findings reproduce on cross-provider response models on a small subset of subjects ([§4.6.1](#sec-4-6-1)) and on alternative judge panels ([§4.6.2](#sec-4-6-2)), and the gradient pattern continues to hold at the high-baseline end through the Franklin reference ([§4.6.4](#sec-4-6-4)). §5 develops what these results imply for AI personalization beyond the specific experiment, and §6 bounds what the experiment cannot establish.

---

## 5. Discussion

§4 established the gradient, the content-specificity mechanism, and the structured per-question interaction with existing memory systems, and included a post-hoc N=3 case study of Letta's stateful-agent path ([§4.5](#sec-4-5)). §5 turns to what those results imply beyond the specific experiment. Before developing the positive implications ([§5.2](#sec-5-2) onward), [§5.1](#sec-5-1) names a recurring failure mode that cuts across all five memory systems evaluated and motivates the paper's positive target: the conflation of recall sufficiency with representational adequacy.

### 5.1 The Anti-Pattern: What Behavioral Specification Is Not {#sec-5-1}

Before summarizing what this study demonstrates, this discussion first defines the anti-pattern: what the Behavioral Specification is explicitly not trying to be. Naming the anti-pattern clarifies the scope of every positive claim that follows and marks the boundaries the paper does not overstep.

**Note on framing.** The goal is a representation that lets a response model accurately predict how a specific person would respond to a question, not a representation that lets a response model act as that person. The latter is an agent-design problem; the former is a context-design problem. The Behavioral Specification serves the prediction task, and the rubric measures alignment between predicted response and the held-out passage from the subject's own writing.

**It is not memory recall.** Memory-recall benchmarks (LOCOMO, LongMemEval, discussed in [§2.1](#sec-2-1)) measure whether a system can retrieve a specific fact it previously ingested. A system that scores 95% on recall can still score at the rubric floor on representational accuracy: the ability to anticipate a person's reasoning in a situation no stored fact covers. [§4.1](#sec-4-1) and [§4.4](#sec-4-4) separate these two axes empirically.

**It is not persona fidelity.** Persona benchmarks (PersonaGym, [§2.1](#sec-2-1)) measure whether a model maintains a described character consistently during conversation. A system that maintains persona perfectly can still be representationally inaccurate: the persona itself can be a surface portrayal that does not carry the interpretive patterns the person actually reasons with. Representational accuracy is measured against a specific person's held-out behavior, not against self-consistency of portrayal.

**It is not preference alignment.** Preference-tuning benchmarks (AlpsBench, [§2.1](#sec-2-1)) measure whether a system produces responses a user rates higher on preference or emotional-resonance scales. Preference alignment optimizes what the user likes receiving; representational accuracy measures how well the system anticipates what the user would do next. The Behavioral Specification targets the second and is ambivalent about the first.

**It is not survey-response interpolation.** Twin-2K ([§2.1](#sec-2-1)) predicts a participant's held-out Likert responses from their other responses on the same structured survey. The task shape constrains both the representation (survey history on fixed axes) and the target (Likert-scale response interpolation). Representational accuracy is a broader test: predicting open-ended behavior on unseen autobiographical passages, drawn from a different modality than the source material.

**It is not a psychometric profile.** Psychometric profiles compress a person to scores on a fixed dimension set (Big Five, MBTI, Enneagram). Those dimensions are legible and portable but lossy by construction: the axes are chosen in advance by the test designer, not derived from the subject's own reasoning patterns. The Behavioral Specification's anchors are surfaced from the subject's corpus rather than projected onto a fixed axis set.

The positive target is narrower than any of the above. We want a representation that lets a response model accurately predict how this specific person would respond, on situations the model has never seen, grounded in the person's documented reasoning patterns rather than in surface-level similarity, psychometric dimensions, or preference signals. What follows ([§5.2](#sec-5-2) through [§5.6](#sec-5-6)) develops what the study shows about this target and where it falls short.

---

### 5.2 What the study demonstrates {#sec-5-2}

This paper is oriented to a single question: how do we improve human-AI interactions for anyone who uses an AI system? AI is now broad-base infrastructure, comparable to email or mobile phones in how widely it touches daily decisions, so the population of relevance is the general user base rather than a specialist niche. Almost none of those users have had their reasoning indexed by any training corpus ([§1.4](#sec-1-4)). We introduced representational accuracy as the measurable AI-side property that makes those interactions possible: how faithfully an AI's internal model of a specific person captures how that person reasons. We tested it by measuring behavioral prediction on held-out text, checking whether the response model could anticipate how each subject would respond in situations drawn from passages the model had never seen, using a specification authored from the other half of the corpus.

Across 14 historical subjects, five commercial and open-source memory systems, one main-study response model (Haiku 4.5) plus 2 additional response models in a small cross-provider directional probe (Sonnet 4.6, Gemini 2.5 Pro on 3 subjects), and five primary judges, the paper produced four empirical results:

- **A compact Behavioral Specification improves prediction, inversely proportional to what the model already knows about the person** (the gradient, H1 + H2; [§4.1](#sec-4-1)).[^discussion-gradient-stats] On the nine low-baseline subjects [^fn17], every subject improved, mean Δ_C4a = +0.89 points. Read in plain language: the less the model already knew about the person, the more the specification helped, in a tight one-to-one trade across the 14 subjects. The effect is largest exactly where it has to be largest for the deployment claim to hold, which is on subjects the model has nothing to start from.

[^discussion-gradient-stats]: Regression of Δ_C4a on baseline C5 across the 14 subjects: slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, slope p < 0.001. Full regression and bootstrap intervals in [§4.1](#sec-4-1).

- **The improvement is content-specific** (H3; [§4.3](#sec-4-3)). The load-bearing evidence is the adversarial wrong-spec: pairing each subject with a culturally and temporally distant other person's specification by design degrades prediction below the no-context baseline (Δ −0.25). The softer wrong-spec probe (each subject swapped at random with another subject's specification) scores near baseline (Δ +0.15 vs. +0.35 for the correct spec, a 0.20-point gap). Together the two controls bracket the question: structured prompting alone does not produce the effect, and sufficiently mismatched content actively hurts.

- **The specification interacts with memory-system retrieval in a structured way that depends on question type** (H4; [§4.4](#sec-4-4)). On the population of relevance, three of four commercial memory systems show net-positive aggregate Δ when the spec is added (Mem0, Letta archival, Zep), but the load-bearing finding is per-question, not aggregate. The spec lets retrieval-based systems handle interpretation-heavy questions they were not designed for (Pattern 1), sometimes hurts on literal-recall questions retrieval already answered (Pattern 2), and induces principled refusals on questions where retrieved facts are insufficient (Pattern 3). Aggregate Δ is the balance of these three patterns; the balance shifts by retrieval architecture. Zep (controlled and native) and Mem0-native carry the strongest aggregate evidence; Letta archival is positive in controlled and near-null in native; Supermemory's per-question distribution is bimodal at both subject-mean and per-question-anchor grain ([§4.4.2](#sec-4-4-2), [§4.4.3](#sec-4-4-3)).

- **Structure compresses the predictive signal at a fraction of the context footprint** (H5; [§4.2](#sec-4-2)). A ~7,000-token specification recovers most of what the full raw corpus delivers at compression ratios ranging from roughly 7× (Hamerton, ~33K-token corpus) to 79× (Babur, ~550K-token corpus) by token count. The full extracted-fact set (C4, every fact loaded as context without the specification) produces a similar improvement on the low-baseline slice at a comparable footprint, so fact extraction itself is already a compression pass. The specification's marginal contribution over facts-only is smaller at the aggregate mean than the spec-versus-no-context gap suggests, and its distinct value shows up at the per-question level ([§4.3](#sec-4-3), [§4.6](#sec-4-6)). Behaviorally relevant signal is sparse and compressible at both the fact-extraction and specification-authoring steps.

Alongside these four results, [§4.5](#sec-4-5) reports an informal post-hoc exploration of Letta's stateful-agent path (N=3 subjects, one Letta version, one response model). The exploration is consistent with non-retrieval representation-production mechanisms also reaching a similar prediction band at matched response model, but its sample is too small to be treated as a headline finding. We report it as a case study and flag the replication work needed to promote it in [§7.5](#sec-7-5).

The remaining subsections of §5 develop what the study demonstrates as a whole ([§5.2](#sec-5-2)), what the gradient implies for the population of typical AI users who sit outside the historical sample ([§5.3](#sec-5-3)), the content-specificity mechanism behind the spec effect ([§5.4](#sec-5-4)), the practical-deployment implications scoped to what was tested ([§5.5](#sec-5-5)), and the measurement gaps the study does not close ([§5.6](#sec-5-6)).

---

### 5.3 The population of relevance {#sec-5-3}

**This paper is not a retrospective study of historical figures.** The research question is how to improve human-AI interactions for anyone who uses an AI system. The working assumption is the same one [§1.4](#sec-1-4) stated: AI is becoming general-purpose infrastructure, so the population of relevance is the general user base, not a specialist niche. The 14 historical subjects in the main study are experimental proxies, chosen because they enable cross-subject comparison with verifiable ground truth (the held-out half of their own autobiographies). They are not the target population. The target population is living users whose private reasoning patterns are not in any training corpus, and the structural argument below is that those users sit in the low-baseline band by construction.

**Historical subjects are biased upward in pretraining coverage.** Public-domain autobiographies get digitized, indexed, and fed into LLM training. Even the least-known historical subjects in the main study (Ebers C5 = 1.02, Sunity Devee 1.03) are more present in training corpora than a typical living person whose private reasoning was never published. The bias matters for reading the study's baselines: the sample's floor is higher than the floor for real users.

**The low-baseline slice is the study's closest proxy for real users, and it is where the headline effect lives.** On the 9 subjects with C5 ≤ 2.0, the specification is uniformly positive: 9 of 9 subjects improve, mean Δ_C4a = +0.89 points, with 55% of individual responses crossing a rubric-integer anchor upward. This band, not the cross-subject mean, is the result that should travel with the paper. Living users sit deeper into this band than any of our subjects, because the autobiographers were specifically chosen as people whose work is in pretraining and who therefore should be best-known to the model; even on those favorable cases, baseline pretraining alone does not reach a usable score on the 1-5 rubric. The pattern holds where we would expect it to hold for real users: when the AI knows little about the subject from pretraining, the specification fills in.

**What we did not prove.** A multi-subject living-user replication is the most important follow-up this paper flags (§7). The extrapolation from 14 historical subjects to living users in general rests on a structural argument: private reasoning is not in any training corpus, so pretraining cannot close the gap, so a user-supplied representation is required. The structural argument is strong but not a substitute for the empirical replication, and we are careful not to present this paper as more than what it measured.

**The infrastructure implication.** If the population of relevance for AI personalization is everyone who uses AI, and every such user sits in the low-baseline band because their private reasoning is structurally absent from training data, then representational accuracy is not an enhancement for edge cases. It is a structural requirement for personalization at all. Either each user supplies their own representation to the AI systems that serve them, or personalization remains surface-level: style, voice, preference, not how the person reasons. The Behavioral Specification is one implementation of user-supplied representation. An exploratory Letta test ([§4.5](#sec-4-5), N=3 subjects, post-hoc) is consistent with non-retrieval representation-production mechanisms also reaching the target, pending the multi-subject replication flagged in [§7.5](#sec-7-5). Some implementation of user-held, user-inspectable, user-modifiable representation is a prerequisite for AI that can act on behalf of a specific person rather than on behalf of a population aggregate.

---

### 5.4 Content specificity and mechanism {#sec-5-4}

**H3 stated.** The benefit of the Behavioral Specification comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

**H3 is directly tested by the wrong-spec controls.** Random swap (C2c v2, each subject receives some other subject's specification at random) scores near baseline at +0.15 on the 13 global subjects. Adversarial fixed swap (C2c v1, each subject paired with a culturally and temporally distant other by design) drops prediction below baseline at −0.25. The correct-specification-for-correct-subject effect is +0.35 on the same 13 subjects. Structured prompting without the right content does not produce the improvement, and sufficiently mismatched content actively degrades prediction. Content specificity is a necessary condition, not an optional property.

**The specification interacts with retrieval at the question level, not uniformly.** The mechanism is structured: the spec helps a particular class of question (interpretation-heavy, where retrieved facts underdetermine the answer) and hurts a different class [^fn18]. [§4.3](#sec-4-3) and [§4.4](#sec-4-4) identified three patterns that together generate the correct-spec effect; aggregate Δ_spec is the per-question balance of these three patterns. The aggregate observation that three of four commercial memory systems show net-positive Δ when the spec is added ([§4.4.1](#sec-4-4-1)) sits under this finding, not above it. Patterns 1 and 2 reproduce across all five memory systems tested; Pattern 3 (spec-induced refusal) is a specification-level dynamic everywhere but its visible rubric penalty is conditional on whether C1 retrieval was strong enough to support productive speculation ([§4.4.3](#sec-4-4-3)).

- **Pattern 1, pattern supply.** When retrieval returns biographical facts but not the interpretive pattern for how the subject processes them, the specification supplies the pattern. This is what produces the large-magnitude improvements on low-baseline subjects ([§4.1](#sec-4-1) Example A, [§4.3](#sec-4-3) Example 1, [§4.4.2](#sec-4-4-2) Example 1). Pattern 1 drives most positive per-question swings.
- **Pattern 2, over-theorization.** When retrieval already returns the plain answer and the ground truth is a surface-level statement, the specification shifts the response toward interpretive depth the question does not require ([§4.4.2](#sec-4-4-2) Example 2, cross-system reproduction on Yung Wing Q31). Pattern 2 drives most negative per-question swings on literal-recall questions.
- **Pattern 3, structural refusal.** When retrieved facts do not cover the interior motive a question asks about, the specification's dignity or epistemic-honesty axioms lead the model to decline to speculate. The content-match rubric then scores the principled refusal identically to a wrong guess ([§1.3](#sec-1-3) Keckley Q21, [§4.4.2](#sec-4-4-2) Example 3). Pattern 3 drives the sharpest negative swings on this class of question.

**The three patterns together imply dynamic spec activation is a requirement for production response quality.** Pattern 1 (pattern supply) helps when retrieval is thin on interpretive structure. Pattern 2 (over-theorization) hurts when retrieval already has the plain answer. Pattern 3 (structural refusal) hurts when the specification's honesty axioms fire on questions where retrieval was insufficient. Serving the full specification on every query, as this study did, subjects every question to all three mechanisms regardless of which one is appropriate for the query. A production serving layer should decide per-query which components of the specification to activate, based on the query type and on whether retrieval already supplied the surface answer. Without dynamic activation, the specification can make responses worse as often as it makes them better, which the Supermemory mixture ([§4.4](#sec-4-4)) documents at the per-question level. The dynamic-activation proposal in [§5.5](#sec-5-5) is therefore not a nice-to-have for performance optimization. It is a requirement for ensuring that the specification's effect on any given response is net positive.

**Specification design is a multi-objective problem.** A richer axiom set enables more Pattern 1 (pattern-supply) improvements, but it also produces more Pattern 2 (over-theorization) and Pattern 3 (refusal) regressions. A sparser axiom set produces fewer Pattern 1 opportunities, but also leaves the specification less likely to get in the way when the retrieved facts already contain the direct answer. The design is a tradeoff, not a single quantity to maximize. The piecewise component analysis flagged in [§5.5](#sec-5-5) (remove axioms one by one, measure effect per question type) is the empirical way to resolve where the optimum sits for a given deployment and user population.

**Content specificity implies specification authoring is not template-based.** H3's finding that generic structured prompting does not substitute for correct-content specification directly implies that specification authoring is a subject-specific process, not a pattern that can be filled from slots. This is consistent with the pipeline's design: facts are extracted from the subject's own corpus; anchors, core, and predictions are authored from those facts; the brief composes them into a narrative specific to the person. A Base Layer "spec template" with generic slots would not reproduce the effect. The content has to come from the person.

**The Keckley Q21 result.** Keckley Q21 asks about Keckley's interior motive on a decision she explains only in the held-out half of the corpus, so no retrieval system can surface the answer. On all five memory systems, adding the specification produced the same outcome: the response model declined to speculate, citing the specification's dignity and epistemic-honesty axioms. The rubric penalty for that refusal was largest on systems where retrieval alone had already produced a productive guess (Supermemory and Base Layer's substrate, both at C1 ≈ 3.4-3.6 on the 1-5 rubric, with Δ on Q21 of −2.0 and −2.2 respectively), smaller where retrieval had already hedged, and reversed on Letta archival, where the structured refusal scored higher than the unstructured one. The reading: the refusal sits at the specification layer, not at any specific retrieval architecture, and the rubric (which cannot distinguish principled refusal from wrong prediction) is what converts it into a numeric penalty. The size of that penalty across the five systems is itself informative because it tracks how strong retrieval was on its own ([§4.4.3](#sec-4-4-3)).

**What the mechanism reading leaves open.** We did not run component ablation (anchors-only, core-only, predictions-only, brief-only, and combinations). Which layer of the specification carries Pattern 1 (pattern supply) improvements, which contributes to Pattern 2 (over-theorization) regressions, and which triggers Pattern 3 (structural refusal) is not measured. §7 flags this as the priority authoring-pipeline follow-up. Answering it would directly inform where to invest the authoring pipeline's capacity and how to structure dynamic activation ([§5.5](#sec-5-5)) to serve the right components for the right query types.

---

### 5.5 Practical implications {#sec-5-5}

[§4.1](#sec-4-1) through [§4.6](#sec-4-6) establish what the Behavioral Specification does and why it works. [§5.5](#sec-5-5) is a practical note on what deploying it in production looks like: context budget, authoring cost, per-query cost, update cadence, and how the specification positions against alternative approaches. It also documents several open design questions that follow directly from the study's findings but were out of scope to answer inside this paper.

---

**A note on what was tested versus what production would look like.** The specification form studied here is a proof-of-concept implementation: the full-stack specification is served in its entirety as a static context attachment on every query. This is the simplest possible serving strategy, chosen so the measurement isolates the representation's effect rather than serving-strategy effects. Production deployment would almost certainly not serve the specification this way. The discussion below distinguishes what the current implementation requires from what production approaches might look like.

---

**Context budget (as served in this study).** The full-stack Behavioral Specification is ~7,000 tokens and fits inside every frontier LLM's context window with headroom. On a 200K-token context model it consumes 4-5% of the window; on a 1M-token context model it consumes well under 1%. Serving the specification in full on every query is operationally tractable at current pricing. Compare: the full raw corpora in this study range from ~34K tokens (Hamerton) to ~550K tokens (Babur), with Babur exceeding most current context windows at the time of this study or incurring substantial per-query cost if served directly.

**Per-user authoring cost.** The five-step pipeline (import → extract → embed → author → compose; [§3.7](#sec-3-7)) runs offline, once per user. For a typical subject's training corpus (25K-100K words), the pipeline completes in minutes to tens of minutes on current API pricing, with the dominant cost being the extraction step (Haiku-class model, ~300-1,500 facts per corpus). The cost profile matches one-time onboarding overhead, not per-query overhead.

**Per-query cost (as served in this study).** At inference, the full specification is a static context attachment. No retrieval step at the specification level; no live extraction; no re-embedding. The per-query overhead is the token cost of the full specification in the prompt. On current frontier pricing, ~10K context tokens adds on the order of a cent or less per query.

---

**Dynamic activation: the likely production serving strategy.**

Serving the full specification on every query is wasteful. Most queries engage only a subset of the specification's content: a question about the user's work-style reasoning does not need the whole identity-level anchor set, only the work-style anchor plus the relevant predictive-template and a handful of retrieved facts that bear on the question. A production serving layer would plausibly activate the specification dynamically:

- Embed the incoming query.
- Retrieve the specification components (anchors, axioms, predictions) whose embeddings are closest to the query.
- Retrieve facts tied to the activated specification components through the provenance links ([§3.7](#sec-3-7), [§3.4](#sec-3-4)).
- Serve the activated subset plus the brief as context, rather than the entire stack.

On a typical query, the activated subset would be on the order of 1,000-2,000 tokens rather than the full 8,000-10,000. The per-query cost drops by roughly an order of magnitude, and the specification's signal-to-noise ratio in the prompt improves (fewer unused axioms competing for the model's attention). Whether the dynamic activation preserves the behavioral-prediction accuracy the full-stack configuration produces is a separate measurement question, not answered by this paper. The components and their provenance links already exist; what is missing is the activation policy and a controlled measurement comparing dynamic-activation accuracy to full-stack accuracy on the same battery. Flagged in §7.

---

**Modifiability: the specification is user-editable by construction.**

The specification is a text document with labeled components. A user reading their own specification can:

- Correct factual errors in the facts layer without re-running the full pipeline.
- Revise or delete anchors and predictions the user believes are wrong about them.
- Add anchors or predictions that the pipeline missed because the behavior was not well-represented in the source corpus.
- Override the brief's synthesis if the brief overgeneralizes or misses a load-bearing distinction.

These edits propagate through the provenance links: a corrected fact updates the anchors and predictions that cite it; a revised anchor updates the brief that composes it. The pipeline is designed to re-run incrementally from the edit point forward rather than re-authoring the whole specification from scratch. This is a property of the representation being text rather than weights. Fine-tuning a per-user model for the same target does not permit this kind of edit loop; no user can directly audit or correct a fine-tuned model.

Modifiability is a first-class requirement for any AI representation that claims to represent a specific person. The specification's edit affordances are part of what makes it operationally viable beyond the experimental setting.

---

**Temporality: a snapshot representation, with explicit gaps.**

The specification is a snapshot of the subject's interpretive patterns at the time the corpus was processed. For the main-study historical subjects, no update is needed because the corpus is complete and the subject's life is fully captured in the source. For living users, the specification has no explicit model of time. It does not encode:

- When a pattern was last observed (a user's current work style may differ from their work style five years ago).
- Which patterns are stable across their life and which are context-dependent (a pattern that held only during a specific job may misapply in other contexts).
- How to weight newer observations against older ones when they conflict.

A production serving layer would plausibly annotate the specification with temporal metadata (timestamps on source facts, version history on anchors, weighting schemes on predictions) and have the activation policy consider recency. None of this is implemented in the current pipeline. The gradient and the mechanism findings hold for a static snapshot; whether they hold once temporality is layered in is an open question. Flagged in §7.

---

**Topic decomposition and piecewise component analysis.**

Two closely related open questions that this study does not answer but that the design raises directly:

1. **Topic decomposition.** Specifications could be organized by topic domain (work style, relationship patterns, political reasoning, health decisions, etc.) with domain-specific anchors and predictions, rather than the current unified identity-level structure. A domain-scoped serving layer would activate only the domain relevant to the query, reducing context budget further and avoiding cross-domain interference ([§4.3](#sec-4-3)'s over-theorization pattern on technical questions). The pipeline's authoring step could be extended to produce domain-tagged layers; the serving step could route queries to the relevant domain. Flagged in §7.

2. **Piecewise component analysis.** Which layer of the specification carries the prediction signal? We did not run an ablation study. The pipeline produces anchors, core, predictions, and a brief that composes them. Whether the brief alone achieves most of the effect, whether anchors are load-bearing and predictions are decorative, or whether the full stack is necessary, has not been measured. A component-ablation study (run the same subject battery with anchors-only, core-only, predictions-only, brief-only, and in combinations) would identify which components are doing the work. The result would directly inform both the authoring pipeline's priorities and the dynamic-activation policy's weights. Flagged in §7.

---

**Update cadence.** The specification is a snapshot. For living users whose behavioral patterns evolve, re-authoring cadence is an open design question flagged in §7. The pipeline is designed to re-run incrementally: extraction on new corpus additions, re-authoring of the layers if the newer content shifts the anchors or predictions. The choice of whether to re-author on a schedule, on a corpus-size threshold, or on a detected-drift signal is a policy decision the study does not address.

---

**Positioning against alternative approaches.**

- **Per-user fine-tuning** reaches the representational-accuracy target by modifying model weights for each user. Cost profile: substantial per-user compute, per-query inference on a dedicated model, no portability across providers, opaque to the user about what has been learned. The Behavioral Specification reaches the same target via context rather than weights, with portability, inspectability, and per-user audit that weight modification does not allow.
- **Retrieval-augmented generation (RAG) alone** targets recall rather than representational accuracy. [§4.1](#sec-4-1) through [§4.4](#sec-4-4) show RAG alone does not close the gap on low-baseline subjects. Adding the specification on top of RAG produces a structured per-question interaction (Patterns 1, 2, 3 in [§4.4.2](#sec-4-4-2)) that nets out positive on aggregate Δ for three of four commercial memory systems tested.
- **Serving the raw corpus as context on every query** is the alternative to compression. At small corpus sizes the raw corpus is tractable; at medium to large corpus sizes it is not. [§4.2](#sec-4-2) documents the 5× to 78× compression the specification achieves at modest cost to predictive signal (~0.2 points on the 1-5 rubric on the low-baseline slice).

---

**Infrastructure properties.**

The Behavioral Specification is a portable artifact. It attaches as context to any LLM call without provider-specific integration. Users can own and audit their own specifications; providers can serve them without storing the full conversation history that produced them. The representation is independent of the runtime; the same specification can be served to Claude, GPT, Gemini, or any future response model with no change.

Four infrastructure properties that do not fall out of any of the alternative approaches above:

- **User-held.** The specification is a text document. The user (or their designated custodian) can store it, move it, redact it, regenerate it from updated source material. No AI provider needs to retain the underlying corpus; the specification is sufficient to serve the user at the representational-accuracy level the study measures.
- **Inspectable.** The axioms, predictions, and narrative brief are in plain language. A user reading their own specification can identify places where the AI's model of them is wrong, and correct the source material or re-author the spec accordingly.
- **Provenance-traced.** Each axiom and prediction can be traced back to the specific source material that produced it ([§3.7](#sec-3-7), [§3.4](#sec-3-4)). A user who wants to understand why the spec says what it does can audit the derivation.
- **Local-executable retrieval.** Base Layer's retrieval substrate (MiniLM-L6-v2 embedding + ChromaDB vector store) runs entirely on the local machine without cloud API calls for vector search or fact identification. The four commercial memory providers tested in the study (Mem0, Letta, Supermemory, Zep) all require cloud operations for retrieval. For deployments where data sovereignty, offline operation, or zero-dependency execution matter, the local-execution option is materially different from a cloud-dependent option.

These properties matter for deployment because they make the representation auditable, portable, and runnable at the infrastructure layer, not only at the application layer.

---

**Summary of practical implications (scoped to what was tested).** As served in this study (static full-spec attached to every query, Haiku response model, N=14 subjects), the Behavioral Specification is compact enough to fit within current context windows and cheap enough to author once per user at current extraction-model pricing. The deployment-readiness claims that follow from these properties (portability across response models, user-inspectability, one-time per-user authoring cost, dynamic activation) are implementation proposals consistent with what the artifact is, not properties this study measured at production-realistic scale. What this study measured is the representation's prediction behavior in a controlled experimental setup; production behavior under dynamic activation, per-user temporal update cadence, and long-horizon serving is open follow-up work ([§7.4](#sec-7-4)).

---

**The Behavioral Specification as per-user calibration.** The artifact this paper measures is best understood, at the deployment layer, as **per-user calibration**: a portable, user-held, user-inspectable representation of how a specific person reasons, attached to AI calls so the model acts on data and decisions on that person's behalf rather than on a population average. The [§4.1](#sec-4-1) structural finding makes this concrete. The specification produces a roughly uniform operating quality (mean C4a ≈ 2.4 on the 1-5 rubric) regardless of how much the model already knew about the user; what varies is whether the user's no-context baseline sits below or above that operating quality. Calibration is the right word for this. It is not a memory upgrade and it is not a personality template. It is a one-time tuning of the model's prior to the specific user, applied at serving time as context.

This framing connects directly to a posture every AI provider has to take a position on: when an AI acts on a user's behalf, whose reasoning patterns is it averaging over? Without calibration, the answer is a population aggregate weighted by whatever subset of human writing happened to dominate pretraining. With calibration, the answer is the specific user. The [§4.1](#sec-4-1) ceiling is the empirical signature of that shift: the specification is uniformly effective at moving the model from population-average to user-specific operation, and the gain in measured prediction is whatever distance the specific user sat from the model's population-average prior.

Three deployment properties follow from the calibration framing that are not properties of memory or persona alternatives. First, **calibration is portable**: the same artifact attaches as context to any AI provider's call, with no provider-specific integration. Second, **calibration is inspectable**: the user can read their own specification in plain language, identify where the AI's model of them is wrong, and correct the source material or re-author the spec. Third, **calibration is provenance-traced**: each axiom and prediction can be traced back to the source material that produced it ([§3.7](#sec-3-7)). None of these properties survive in fine-tuning or in opaque memory stores. Where the deployment story sits next to the alternative approaches is captured in the positioning block above; the calibration framing names what the deployment story actually delivers.

---

### 5.6 What the study does not settle {#sec-5-6}

The paper demonstrates what [§5.2](#sec-5-2) summarizes, and it does not demonstrate the following. Each open item maps to a §7 follow-up.

**Framing: read for directionality, not precision.** The study's aggregate numbers should be read as evidence of directional effects [^fn19] rather than as precision estimates with narrow error bars. The measurement apparatus has known limitations that affect exact numeric values more than they affect directions: the rubric's non-response-versus-response boundary is imperfect, the question batteries were backward-designed but not hand-curated for quality or distribution, and the rubric was not systematically human-reviewed on every scored response. A reader should take a +0.89 mean improvement on the low-baseline slice as strong evidence that the specification helps more where baseline is lower, not as a claim that the effect size is exactly 0.89 points. The follow-ups in §7 are organized around the measurement work that would turn directional results into precision results.

**Multi-subject living-user replication.** The most important gap. 14 historical subjects is not a population-level claim about living users. The structural argument in [§5.3](#sec-5-3) (private reasoning is not in any training corpus, so pretraining cannot close the gap) is strong but rests on an extrapolation that empirical replication would test directly. This is the leading §7 follow-up.

**Rubric validity.** The content-match rubric has three documented limitations the paper uses but does not close. First, it cannot distinguish a principled refusal [^fn20] from an off-base wrong prediction; both score at the rubric floor. The direction of bias this introduces is paper-favorable: the true spec effect on interpretation-heavy questions is slightly larger than the reported aggregate ([§3.6.6](#sec-3-6-6)). Second, in post-hoc spot-check review we found instances where non-responses (verbose hedging, adjacent-fact recitation without committing to a prediction) were scored as partial responses rather than at the floor, likely because length-sensitive judges read the verbosity as engagement ([§3.6.6](#sec-3-6-6) length-score correlation r = 0.604 within C5 baseline only; 9.4% of abstention-pattern responses inflated above a score of 2.0). Third, we did not systematically curate the backward-designed questions for quality, and we did not hand-review whether the rubric was reasonably applied on every scored response. A differentiated battery that separates interpretation-heavy from literal-recall questions, a scoring dimension that rewards epistemic honesty as its own property, a curated question set, and a human-validated subset of rubric applications together constitute the measurement-track follow-up flagged in §7.

**Component ablation.** The specification has four authored layers (anchors, core, predictions, brief) plus the underlying fact set. Which layer carries Pattern 1 (pattern supply) improvements, which contributes to Pattern 2 (over-theorization) regressions, and which triggers Pattern 3 (structural refusal) is not directly measured. A proper ablation on the main-study battery (serve each layer alone, serve combinations, measure Pattern-1/Pattern-2/Pattern-3 distributions per combination) would identify which parts of the pipeline are doing the work. Answering this would directly inform both the authoring pipeline's investment priorities and the dynamic-activation policy's weights. Flagged in §7.

**Production deployment gap.** The study served the full specification statically on every query, which is the simplest possible serving strategy and not a production-realistic one. Dynamic activation (per-query component selection), modifiability (user-editable text with provenance propagation), temporality (timestamps, recency weighting, versioned specifications), canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts), and topic decomposition (domain-scoped anchors and predictions) are all untested. The gradient and mechanism findings hold for the static snapshot; whether they hold under production serving is a measurement gap, not an answered question. All flagged in §7.

**LLM-as-judge circularity.** Tier 2 cross-provider replication ([§4.6.1](#sec-4-6-1)) addresses within-provider circularity: five of six non-Haiku cells reproduce the direction with non-Anthropic batteries and non-Anthropic response models. Class-level LLM-as-judge circularity remains. A human-judge validation on a stratified subset of responses is the natural follow-up. Flagged in §7.

**Sample constraints.** Fourteen historical subjects is a sample, not a population. The sample is biased upward on pretraining coverage ([§5.3](#sec-5-3)). The main-study response model is Haiku 4.5 across all 14 subjects; an additional 4 response models appear in the [§4.6.1](#sec-4-6-1) Tier 2 cross-provider replication on 3 subjects only. One version of Letta's stateful-agent stack was tested on N=3 subjects. These constraints bound the generalizability of the claims to the specific conditions measured.

**Base Layer pipeline variations.** The Letta stateful comparison in [§4.5](#sec-4-5) served Base Layer's unified `spec.md` variant rather than the full layered stack (anchors + core + predictions + brief) used in [§4.4](#sec-4-4)'s controlled and native conditions. A layered-stack rerun on the Letta matched-rerun subjects would likely narrow the Letta-over-Base-Layer gap; whether it narrows to parity or reverses is not measured. Flagged in §7.

**What the open items collectively imply.** The study demonstrates a measurable representational-accuracy effect with specific empirical contours, validates the target architecturally, and documents one implementation. It does not demonstrate that this implementation is best, that the effect reproduces on every living-user corpus, that the measurement rubric is uncontested, or that production-realistic serving strategies preserve the measured effect. The research agenda in §7 is organized around turning these open items into tractable follow-up experiments.

---

---

## 6. Limitations

The paper's claims are bounded by four axes of constraint on the experimental setup: the subject sample ([§6.1](#sec-6-1)), the measurement apparatus ([§6.2](#sec-6-2)), the pipeline and specification stability ([§6.3](#sec-6-3)), and the scope of exploration ([§6.4](#sec-6-4)). Each is a permanent caveat on how the paper's results should be read, distinct from the open research questions catalogued in [§5.6](#sec-5-6) and the follow-up experiments proposed in §7.

### 6.1 Subject sample {#sec-6-1}

The 14 main-study subjects are a selected sample, not a population. Two sample-level points (pretraining-coverage bias and the single-living-subject constraint) are load-bearing for the paper's framing and are developed in [§5.3](#sec-5-3); this subsection covers four remaining external-validity caveats that §5 does not address.

**Public-domain selection.** All subjects are historical figures whose autobiographies or memoirs are in the public domain and have been digitized by Project Gutenberg or Internet Archive. That selection pipeline is biased toward canonical texts, toward figures whose writing was preserved in published form, and toward Western publishing traditions. The paper's cross-continent spread (Saint Augustine, Babur, Fukuzawa Yukichi, Sunity Devee, Zitkala-Sa, Olaudah Equiano, Mary Seacole) partially mitigates but does not remove this bias.

**Self-presentation bias.** Autobiography is authorial self-curation. What each subject chose to include in their memoir is not a neutral record of their behavior; it is a self-selected narrative that may over-represent behavioral patterns the author wished to be remembered for and under-represent patterns they chose to leave out. Behavioral-prediction batteries derived from autobiography inherit this bias, and neither the pipeline nor the rubric has a mechanism to correct for it.

**Translation artifacts.** Three subjects' corpora are English translations of non-English originals (Augustine's *Confessions* from Latin, Babur's *Babur-nama* from Chagatai Turkic via Persian, Cellini's autobiography from Italian). Translations introduce stylistic and register shifts that the extraction pipeline processes as if they were original text. A specification authored from a translated corpus may inherit translator choices in addition to the subject's actual patterns.

**Era.** The oldest subject is 4th to 5th century (Augustine); the newest is early 20th century (Zitkala-Sa, Sunity Devee). Reasoning patterns in modern work contexts, contemporary family structures, technical or digital-native domains, and late-20th-century cultural frames are not sampled. Whether the gradient holds when specifications are authored from modern-era corpora is a generalization the study cannot make from its sample alone.

Taken together, these four caveats mean the paper's results should be read as evidence for the claims at the conditions tested. Generalization across era, source language, self-presentation mode, and digital-versus-analog source material requires follow-up experiments.

---

### 6.2 Measurement apparatus {#sec-6-2}

This section covers the measurement-apparatus constraints on how the paper's numbers should be read. The rubric limitations are in [§5.6](#sec-5-6); the LLM-as-judge limitation is the canonical one and is treated in full here.

**Class-level LLM-as-judge circularity.** Every response in this study is generated by an LLM, every judge is an LLM, and the question batteries are also LLM-generated ([§3.3](#sec-3-3)). The 5-judge primary panel and the 7-judge sensitivity check together address within-provider circularity ([§4.6.1](#sec-4-6-1), [§4.6.2](#sec-4-6-2)): the specification effect reproduces when non-Anthropic response models read non-Anthropic-generated batteries, and removing the most-inflationary judges from the aggregate makes the effect smaller, not larger. What these checks do not address is class-level LLM circularity. The broader concern is that an all-LLM pipeline could be self-reinforcing in ways that human evaluators would not validate. Prior independent work (Zheng et al., 2023, NeurIPS Datasets and Benchmarks Track, arXiv:2306.05685) showed that LLM-as-judge panels correlate with human judges on comparable tasks at rates approaching human-human agreement, which is the methodological precedent that legitimizes the panel here. Subsequent panel-based work (Verga et al. 2024 and follow-ons) showed that aggregating multiple LLM judges past a small panel size further tightens agreement. But "approaches human agreement on comparable tasks" is not the same as "is empirically determining the objective quality of a behavioral prediction response." The 5-judge primary panel can answer the directional question (does the specification move representational accuracy in the right direction) but not the absolute-quality question (is any specific numeric value the right score). A stratified human-validation subset is the leading measurement follow-up flagged in [§7.1](#sec-7-1); until that exists, the paper's claims should be read as directional rather than precise. **The paper as a whole is best understood as a methodological prototype with LLM-judge-only evidence on the headline directional claims, awaiting human-validation triangulation as the highest-priority single follow-up.**

**Response-model coverage.** The main-study response model is Claude Haiku 4.5. The [§4.6.1](#sec-4-6-1) Tier 2 cross-provider directional probe ran 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) on 3 subjects spanning the gradient (Ebers, Yung Wing, Zitkala-Sa) against GPT-5.4-regenerated batteries; Claude Opus 4.6, GPT-5.4, and GPT-4o were used as judges in Tier 2 but not as response models. The specification-effect direction reproduced on 5 of 6 (subject, response-model) cells under every panel and Δ-definition tested. The main-study response model is Haiku across all 14 subjects in [§4.1](#sec-4-1); Tier 2 establishes direction across response-model families on a small subset only. The paper's aggregate numbers should be read as what the specification does with Haiku; other response models may produce different absolute magnitudes while preserving the gradient.

**Prompt-phrasing ambiguity.** The authoring pipeline prompts, the response-generation prompts, and the judge prompts all depend on specific word choices, ordering, and phrasing. We did not systematically test prompt sensitivity. Different wordings at any of these stages could produce different numeric results, different extracted fact sets, or different judge scores on the same response. The paper's claims are downstream of the specific prompts used throughout the study (documented in the public repository scripts); we make no claim about prompt invariance.

**Inter-judge calibration variance.** Pairwise Spearman ρ across judges is 0.86 to 0.93 ([§3.6.4](#sec-3-6-4)), so the rank order of conditions is stable across the panel. Absolute-score calibration varies ([§3.6.3](#sec-3-6-3)): Gemini Pro fails verbatim-match calibration (4.15 where calibrated judges score 5.0), Opus runs lenient on abstentions (1.41 mean where Sonnet runs strict at 1.14), and length-sensitivity differs across judges. The 5-judge primary aggregate is therefore a stable reading of direction but a panel-specific reading of magnitude. A different judge panel would produce different aggregate numbers while preserving the direction of every claim, which is part of why [§5.6](#sec-5-6) frames the paper as directional rather than precise.

---

### 6.3 Pipeline and specification stability {#sec-6-3}

The serving-strategy gap (static full-stack attachment versus production-realistic dynamic activation) is in [§5.5](#sec-5-5) and [§5.6](#sec-5-6). What follows covers pipeline-internal constraints on how the paper's results should be read.

**Pipeline version tested.** The specifications used in this study were produced by the current pipeline version, which we consider stable. The pipeline has evolved through development, and different pipeline versions produce different specifications on the same source corpus. The paper's results are specific to the pipeline version tested, and the study does not measure how the gradient shifts under earlier or later pipeline versions.

**Specification stability under the same pipeline version.** Running the same pipeline twice on the same corpus at temperature 0 does not produce identical specifications. In an initial stability check, two runs match verbatim on roughly 45% of the resulting text and produce semantically similar but textually different content on the remainder. This is an artifact of LLM sampling and of the multi-step authoring pipeline: small divergences at the extraction or authoring steps propagate through downstream composition.

**Per-subject pipeline variance, characterized.** A targeted replication probe was run on three subjects spanning the gradient (Sunity Devee, C5 = 1.03; Yung Wing, C5 = 1.88; Augustine, C5 = 2.58). For each subject, the Sonnet layer-authoring step and the Opus compose step were re-run three times against the same per-subject extracted fact set at temperature 0, producing three independent specifications. Each rerun was scored on the full behavioral-prediction battery in the C2a (spec only) and C4a (facts plus spec) conditions on the 5-judge primary panel. The resulting per-subject standard deviation of Δ_C4a across reruns is reported below, alongside the cross-subject SD that the [§4.1](#sec-4-1) gradient slope is fit to.

| Subject | Canonical Δ_C4a (§4.1) | Per-rerun Δ_C4a SD (n=3) | % of cross-subject SD |
|---|---:|---:|---:|
| Sunity Devee | +1.38 | 0.103 | 17.4% |
| Yung Wing | +0.52 | 0.055 | 9.3% |
| Augustine | +0.11 | 0.130 | 22.0% |
| **Pooled (3 subjects)** | n/a | **0.101** | **17.1%** |

**Read of the precision question.** The pooled per-subject run-to-run SD of Δ_C4a is 0.10 on the 1-5 rubric, compared to the cross-subject SD of 0.59 that the gradient slope is regressed against. Run-to-run pipeline variance is therefore on the order of 17% of the signal the slope is fit to, and well under the 95% CI half-width on the slope (0.29). At this magnitude the directional finding survives across reruns: low-baseline subjects keep improving (6 of 6 reruns positive across the 2 low-baseline probe subjects), and the gradient slope point estimate is not materially threatened. What pipeline variance does affect is the precision attached to any single per-subject point estimate. The per-subject Δ_C4a numbers in [§4.1](#sec-4-1) should be read with a soft uncertainty bar of roughly ±0.10 around them. Augustine (mid-baseline, canonical Δ = +0.11) sits at the top of its rerun range and the sign flips on 2 of 3 reruns, so individual mid-baseline subjects' spec-effect sign is itself within the run-to-run uncertainty band.

**Scope and caveats of the variance probe.** The probe covers the lighter-scope variance only: the Sonnet authoring step plus the Opus compose step. Extraction-stage non-determinism is held constant by reusing each subject's pre-populated SQLite and ChromaDB state across reruns; including extraction would likely add additional variance at the front of the pipeline. The probe covers low-baseline and mid-baseline subjects but does not reach the Franklin-style high-baseline tail (C5 = 3.77), so the H2 corollary interference claim is not directly stress-tested by this run. With n = 3 reruns per subject the per-subject SD point estimates carry their own wide 95% confidence intervals (roughly [0.5×, 6×] of the value); the pooled three-subject estimate is more stable than any single per-subject estimate but should still be read as an order-of-magnitude indicator rather than a precision number. With those caveats stated, the run-to-run SD is small enough relative to the cross-subject SD that we accept the [§4.1](#sec-4-1) slope and R² as findings about the gradient rather than artifacts of a single specification authoring.[^variance-data-paths]

[^variance-data-paths]: Per-rerun specs and judgments are at `data/global_<subject>/_variance_runs/run_<N>/` and `results/global_<subject>/_variance_runs/run_<N>_*.json`. Full report and reproducibility scripts at `docs/research/v10_pipeline_variance_analysis.md`, `scripts/_v10_pipeline_variance.py`, and `scripts/_v10_pipeline_variance_report.py`.

**Pipeline model choices were not varied systematically.** The pipeline uses Claude Haiku for extraction, all-MiniLM-L6-v2 for embeddings, Claude Sonnet for layer authoring, and Claude Opus for the compose step ([§3.7](#sec-3-7)). These model choices were not varied across the study. Different models at any step could produce different specifications: a different extraction model could surface different facts, a different embedding model could change retrieval behavior, a different authoring model could produce differently-structured anchors and predictions, a different composition model could synthesize the layers differently. Extending model support for each pipeline step, and measuring the gradient under alternate pipeline configurations (for example GPT-5.4 extraction, OpenAI embeddings, a non-Anthropic authoring model), is a direct follow-up flagged in §7.

---

### 6.4 Scope of exploration {#sec-6-4}

Not every experimental combination was run. Main-study coverage prioritizes the conditions and subjects central to H1 through H5 ([§4.1](#sec-4-1) through [§4.4](#sec-4-4)). Robustness and ablation conditions were added selectively rather than exhaustively.

**Coverage across the experimental grid.** The study's conditions span one main-study response model (Haiku 4.5) on all 14 subjects, plus 2 additional response models (Sonnet 4.6, Gemini 2.5 Pro) in the [§4.6.1](#sec-4-6-1) Tier 2 cross-provider directional probe on 3 subjects. The grid covers 11 conditions (C1 through C9 plus two wrong-spec variants) and five primary judges plus two sensitivity judges. Running every possible combination (roughly 6,500 separate cells) was not attempted. Coverage was prioritized on the main-study conditions for all 14 subjects on the 5-judge primary panel, and on the Tier 2 cross-provider conditions for three subjects. Ablation-adjacent conditions (per-layer spec serving, alternate pipeline model choices, dynamic activation policies) were not run at all.

**Letta stateful-agent exploration.** Letta's stateful-agent architecture is distinct from the archival retrieval path the other three commercial systems use ([§4.4](#sec-4-4), [§4.5](#sec-4-5)). Testing the stateful path required a different evaluation harness ([§4.5](#sec-4-5) test design), and that work pulled us partially outside the main-study scope. The resulting comparison covers three subjects (Hamerton, Ebers, Babur), one Letta version, and one response model (Claude Haiku). Extending the stateful-agent comparison across the full 14-subject gradient, across additional response models, and against future Letta releases is flagged as a follow-up in §7.

**Twin-2K is prior work, not a condition of this study.** Twin-2K ([§2.1](#sec-2-1)) appears in this paper as prior work that measures a related but distinct property (survey-response prediction rather than representational accuracy). We did not run it as a condition of the main behavioral-prediction battery and do not report it as a benchmark result.

---

## 7. Future Work

Every section of this paper flags at least one follow-up. This section consolidates them into a research agenda organized by theme.

### 7.1 Measurement methodology {#sec-7-1}

The most impactful measurement follow-up is replacing the content-match rubric with a differentiated battery that separates interpretation-heavy from literal-recall questions and scores epistemic honesty as its own dimension ([§3.6.6](#sec-3-6-6), [§5.6](#sec-5-6)). Alongside this: a curated question set with explicit quality control on the backward-design process ([§5.6](#sec-5-6)), a human-validated subset of rubric applications to test whether the rubric was reasonably applied per-response ([§5.6](#sec-5-6)), and human-judge validation on a stratified subset of responses to address class-level LLM-as-judge circularity ([§4.6.3](#sec-4-6-3), [§5.6](#sec-5-6)). Prompt-sensitivity testing across the authoring, response-generation, and judging stages ([§6.2](#sec-6-2)) is a separate measurement-stability follow-up that becomes important once the rubric itself is stabilized.

### 7.2 Subject and corpus expansion {#sec-7-2}

A multi-subject living-user replication is the leading follow-up for the entire paper ([§5.3](#sec-5-3), [§5.6](#sec-5-6)). The paper's findings depend structurally on an extrapolation from 14 historical subjects to living users in general; replicating the gradient with multiple living subjects (with proper consent and privacy infrastructure) turns the structural argument into an empirical one. Three related expansions: modern-era corpora (to test whether the gradient holds when specifications are authored from contemporary writing rather than pre-20th-century autobiography, [§6.1](#sec-6-1)), non-English original sources (to remove translation artifacts, [§6.1](#sec-6-1)), and alternative testbeds that isolate reasoning structure without requiring private data, such as U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted ([§5.3](#sec-5-3)).

**Cross-cultural-transfer hypothesis.** A post-hoc classification of subjects by tradition (Western-introspective vs non-Western, `docs/research/era_modernity_cross_slice.md`) identifies a residualized gap of roughly +0.15 to +0.25 points in Δ_spec favoring Western-tradition subjects, stable across 4 of 5 memory systems (Supermemory is flat on the split). The sample is small (n=4 vs 10) and the result is not load-bearing for any §4 claim, but the direction suggests the authoring pipeline may transfer less cleanly to non-Western autobiographical registers than to the Western-introspective register it was effectively tuned on during pilot iteration. A deliberate authoring-pipeline revision targeted at non-Western interpretive traditions, followed by re-testing, would measure this transfer gap directly. Flagged as a specific follow-up rather than a general one because the data is suggestive enough to warrant its own targeted test.

### 7.3 Specification design and composition {#sec-7-3}

Component ablation on the authored layers (anchors, core, predictions, brief) is the priority authoring-pipeline follow-up ([§5.5](#sec-5-5), [§5.4](#sec-5-4), [§5.6](#sec-5-6)). Serving each layer alone and in combinations, measuring Pattern 1 / Pattern 2 / Pattern 3 distributions per configuration, would identify which parts of the pipeline are doing which work. Answers inform both the authoring pipeline's investment priorities and the dynamic-activation policy's weights.

Alongside component ablation: alternate pipeline model choices (extraction, embedding, layer authoring, composition) to measure sensitivity to specific LLM choices at each pipeline step ([§6.3](#sec-6-3)); a Base Layer referent-variant that retains named entities inside the same dimensional scaffold, to isolate whether the [§4.5](#sec-4-5) Letta-over-Base-Layer gap is driven by referential vocabulary or by the self-editing process itself ([§4.5](#sec-4-5), [§5.5](#sec-5-5)); and a layered-stack Letta rerun on the matched-rerun subjects, which would likely narrow the [§4.5](#sec-4-5) gap ([§4.5](#sec-4-5), [§5.6](#sec-5-6)).

### 7.4 Production serving and infrastructure {#sec-7-4}

These five items appear in [§5.5](#sec-5-5) as deployment design considerations; this section flags which of them require empirical study before production deployment. The study served the specification statically and in full on every query. Five production-realistic serving-layer follow-ups follow directly from [§5.5](#sec-5-5): dynamic activation, modifiability affordances, temporality handling, canonical life events ([§2.1](#sec-2-1)), and topic decomposition (see [§5.5](#sec-5-5) for the description of each). Each is a measurement question in its own right: whether the gradient, mechanism, and composition findings hold under each production serving strategy.

### 7.5 Stateful-agent implementations and temporal drift tracking {#sec-7-5}

Three related follow-ups sit adjacent to the paper's static-snapshot design.

**Stateful-agent variant of the Behavioral Specification.** The pipeline as tested is offline and batch. A persistent, self-editing variant that ingests new source material as it arrives, re-edits anchors and predictions in place, and maintains version history with provenance across edits is a natural next step. The [§4.5](#sec-4-5) Letta exploration (N=3, post-hoc) is one data point on an adjacent architecture; building and evaluating a stateful-agent Base Layer implementation on the full 14-subject main-study battery would close the comparison within a single architectural family and extend [§4.5](#sec-4-5) to a layered-stack rerun against Letta at full scope.

**Cleaner [§4.5](#sec-4-5) rerun with naming and scaling controls.** Two specific extensions of the [§4.5](#sec-4-5) exploration are worth running as a unit. First, anonymize the source corpus before Letta ingestion so Letta writes an anonymized memory block, matching Base Layer's anonymized-during-authoring convention; the [§4.5](#sec-4-5) naming asymmetry (Letta ingests named corpus, Base Layer strips and later restores names) is removed as a confounder. Second, extend the corpus-size axis past the Babur ceiling to a larger (>250K-word) subject corpus that forces the ingestion ceiling to bind harder, to test whether the gap-narrowing trend between Letta and Base Layer observed at Babur ([§4.5](#sec-4-5) caveats, full-stack rerun) continues, inverts, or stalls as the Letta block pushes past the character ceiling with increasing verbatim-duplication rates. Both together would turn [§4.5](#sec-4-5)'s case study into a controlled comparison.

**Temporal drift tracking.** The static snapshot tested here is a point on a trajectory. A behavioral specification authored from a subject's corpus at T1, compared against a specification authored at T2 on the expanded corpus, produces a measurable diff: which anchors appear or disappear, which predictive templates shift, which axioms strengthen or weaken. The trajectory itself carries predictive signal: extrapolation from CP1 through CPn to predict CPn+1. The 14-subject corpora collected for this study can be back-sliced by chapter boundaries or publication era for an initial drift test within the current sample. A companion study on US Supreme Court opinions is purpose-built for the sequential-checkpoint case: ~8 justices with corpora of 65 to 800+ signed opinions each, every opinion date-stamped and publicly available, with seven five-term checkpoints (OT1991 to OT2024) available for Justice Thomas alone. Drift in the interpretive specification at each checkpoint can be measured mechanically (anchor turnover, citation-pattern shift, predicate redistribution) and tested for predictive value on held-out later-period opinions. The methodology is portable beyond jurisprudence to any domain with sequential reasoning artifacts (shareholder letters, research papers, policy documents).

**Continuous-representation infrastructure.** Both of the above converge on the same engineering target: a daemon-class process that observes incoming corpus material, authors or re-authors the specification incrementally, and produces drift telemetry ("subject X shifted N standard deviations from their 10-year baseline on anchor Y") as a first-class output. The [§4.5](#sec-4-5) exploration and the SCOTUS-style sequential-checkpoint design are complementary tests for this class of implementation: the first isolates online self-editing as a representation-production mechanism, the second isolates temporality as a measurable property of the representation itself.

Additional architectural paths worth testing against the same target, beyond stateful-agent and drift-tracking variants, include agent-edited persistent memories outside the MemGPT family, fine-tuned per-user models that expose their internal representation for audit, and hybrid architectures that combine offline-extracted specifications with online self-editing.

### 7.6 Safety-alignment integration {#sec-7-6}

**The affirmative framing.** Per-user calibration is not a defensive concession to make about AI bias; it is the affirmative version of the same observation. AI systems are biased by construction: they are biased toward whatever distribution dominated their pretraining, and they apply that bias to every user identically. Behavioral specification reframes the question from "should the AI be biased" (the answer is "it always is") to "biased toward whom"; the per-user-calibration answer is "biased toward the specific user the system is acting on behalf of." The right kind of bias for an agent acting on a user's behalf is bias toward that user's reasoning patterns. That is what the specification supplies; it is not an addition to AI behavior, it is a redirection of bias the AI already carries, from a population aggregate the user did not choose to a calibrated representation the user owns and audits.

This affirmative framing is where the safety-alignment conversation should join. Representational accuracy (the property this paper measures) and safety alignment [^fn21] are orthogonal axes. A system can be safety-aligned without being behaviorally aligned with any given user; a system can be behaviorally aligned with a specific user whose actions would harm third parties. Both matter for deployment, and neither substitutes for the other. Per-user calibration sits inside the safety envelope, not above or below it: the agent acts on behalf of a calibrated user representation, but operates within the safety constraints the deployment imposes. The constructive question is how the two layers compose, not which layer prevails.

Two concrete follow-ups follow from this. First, the spec-induced refusal cases ([§4.3](#sec-4-3), [§4.6.3](#sec-4-6-3)) showed the response model declining to speculate about interior motive when retrieved facts were insufficient, citing the specification's epistemic-honesty axioms. A post-hoc classifier audit of the 81 spec-induced refusals across 5 memory systems (`docs/research/refusal_intent_classification.md`) classified 75 of 81 (93%) as routine behavioral-prediction rather than morally loaded. The refusal pattern is therefore a general-purpose conservatism dial, not a targeted moral-integrity mechanism. Whether that conservatism composes cleanly with existing safety frameworks across the benign-to-malicious user spectrum, or introduces new interactions, is the first empirical question we flag. Second, this paper's specifications were authored from public-domain autobiographies of subjects not selected on benign-to-malicious intent. What a behavioral specification for a user with malicious intent would contain, and what happens when an agent is deployed on that user's behalf with such a specification active, is untested. This includes the narrower adversarial case of a user deliberately misleading the authoring pipeline about their own patterns. Test methodology for both questions, and controlled experiments on safety-framework composition with representation-accurate agents, are collaboration space with AI safety researchers rather than a single-lab experimental extension.

**Safety-side probing of behavioral specifications.** The wrong-spec adversarial control (Examples [§4.3](#sec-4-3)) demonstrates that the response model can recognize spec content as referring to a different historical period or persona; future work could test whether models recognize specifications that encode adversarial values (e.g., personas that endorse harmful behaviors) and flag them rather than comply, and how this generalizes to live-user specs at deployment.

---

*Paper body complete. Abstract to be written last.*

---

## 8. Data, code, and reproducibility

**Data availability.** All raw response files, per-judge judgments, batteries, and aggregated results for the 14 main-study subjects are in the public study repository at `github.com/agulaya24/memory-study-repo` under `results/global_<subject>/` and `results/hamerton/`. Source autobiographies are public domain (Project Gutenberg and Internet Archive). Per-subject Project Gutenberg IDs are listed in [§3.2](#sec-3-2) Table 3.2. Memory-system raw retrieval and ingestion logs are at `results/global_<subject>/<system>_*.json`. The Letta stateful-agent matched-rerun artifacts are at `docs/research/_letta_rerun/`. The full-stack Letta rerun comparison is at `docs/research/_letta_rerun/fullstack_named/`.

**Code availability.** The Base Layer pipeline source (extract, embed, author, compose) is at `github.com/agulaya24/BaseLayer`. The study-specific analysis and re-run scripts are at `github.com/agulaya24/memory-study-repo` under `scripts/`. Reproducibility pointers from each numerical claim to its supporting script are in `docs/PROVENANCE_INDEX.md` and `docs/DATA_REFERENCE.md`. The [§4.1](#sec-4-1) battery-composition sensitivity analysis is reproducible via `scripts/_v10_battery_sensitivity.py`. The [§3.6.6](#sec-3-6-6) rubric-handling validity audit is reproducible via `scripts/audit_low_end_inflation.py`. The [§4.3](#sec-4-3) hedging classifier is at `scripts/classify_hedging.py`.

**Compute and cost.** All response generation and judging used commercial APIs (Anthropic, OpenAI, Google) at standard rates. Total study cost was approximately USD 350 across all conditions. No specialized hardware was used. All experiments are runnable on a standard developer laptop.

**Author affiliation.** Aarik Gulaya, Base Layer (`base-layer.ai`).

**Funding.** This work was self-funded.

**Conflicts of interest.** The author is the founder of Base Layer, the project that develops the Behavioral Specification pipeline this paper evaluates. Memory-system providers tested in this paper (Mem0, Letta, Supermemory, Zep) were used through their public APIs at standard rates; no provider was given preferential framing, and Base Layer does not have commercial relationships with any of them. Self-reported benchmark scores from each provider are reported as published; this paper does not adjudicate disputes between providers' published claims ([§2.2](#sec-2-2)).

**License.** Apache 2.0 for code and Creative Commons Attribution 4.0 for the manuscript and data analyses produced by this study. Source autobiographies are in the public domain.

**Acknowledgments.** Conversations with the broader memory-systems and AI-personalization research communities informed the design of this paper. Specific gratitude goes to the cross-LLM reviewer panels (Gemini 2.5 Pro, Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, GPT-5.5) whose iterated reviews materially improved earlier drafts. All errors are the author's.

---

## 9. References

Bartlett, F. C. (1932). *Remembering: A Study in Experimental and Social Psychology*. Cambridge University Press.

Chen, Y., Arditi, A., Sleight, H., Evans, O., & Lindsey, J. (2025). Persona vectors: Monitoring and controlling character traits in language models. *arXiv preprint arXiv:2507.21509*.

Chhikara, A., Kumar, A., et al. (2025). Mem0: Building production-ready AI agents with scalable long-term memory. *arXiv preprint arXiv:2504.19413*.

Gulaya, A. (2026). Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization. *Preprint*. `github.com/agulaya24/memory-study-repo`.

Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network. *NIPS Deep Learning and Representation Learning Workshop*. arXiv:1503.02531.

Jain, A., et al. (2025). Sycophancy and the conversational-context effect in LLMs. *arXiv preprint arXiv:2509.12517*.

Jiang, X., et al. (2025). Personalized profile inference from conversation: A benchmark study. *Conference on Language Modeling (COLM) 2025*. arXiv:2504.14225.

Lu, R., et al. (2026). The Assistant Axis: A dominant internal direction in instruction-tuned models. *arXiv preprint arXiv:2601.10387*.

Maharana, A., et al. (2024). LoCoMo: Long-context conversational memory benchmark. *Annual Meeting of the Association for Computational Linguistics (ACL) 2024*. arXiv:2402.17753.

Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as operating systems. *arXiv preprint arXiv:2310.08560*.

Rasmussen, P., et al. (2025). Zep: A bi-temporal knowledge graph for grounded LLM agent memory. *arXiv preprint arXiv:2501.13956*.

Samuel, V., et al. (2025). PersonaGym: Evaluating persona agents and LLMs. *Findings of the Association for Computational Linguistics: EMNLP 2025*. arXiv:2407.18416.

Toubia, O., et al. (2025). Twin-2K: Behavioral prediction at scale on held-out survey items. *arXiv preprint arXiv:2505.17479*.

Verga, A., et al. (2024). Replacing judges with juries: Evaluating LLM generations with a panel of diverse models. *arXiv preprint arXiv:2404.18796*.

Wu, Z., et al. (2025). LongMemEval: Benchmarking long-term interactive memory of LLM assistants. *International Conference on Learning Representations (ICLR) 2025*. arXiv:2410.10813.

Xiao, T., et al. (2026). AlpsBench: Evaluating preference-aligned and emotionally resonant LLM responses. *arXiv preprint arXiv:2603.26680*.

Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems (NeurIPS) 2023, Datasets and Benchmarks Track*. arXiv:2306.05685.

---

**Appendices.** Reference material supporting the main text, designed to be read selectively. Appendix A covers the 46 behavioral predicates used in the extraction step. Appendix B covers per-subject battery composition and category-level effect sizes. Appendix C covers condition identifiers, response-model configurations, memory-system parameters, and judge panel settings. Appendix D covers per-subject score distributions, the rubric-handling audit, length-correlation tables, and anchor-crossing numbers. Appendix E provides three illustrative paired (C5, C4a) per-question response excerpts for each of the 14 main-study subjects. Appendix F covers the extended benchmark-scope comparison against LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo, and adjacent benchmarks. Appendix G holds the full Letta stateful-agent exploratory case study summarized in [§4.5](#sec-4-5). Appendix H is the glossary.

---

## Appendix A. Predicate Vocabulary

### A.1 The 46 Constrained Predicates {#sec-a-1}

The extraction step (Step 2 of the pipeline, [§3.7](#sec-3-7)) instructs the extraction model to emit triples of the form `(subject, predicate, object)` using only the 46 predicates listed below. Predicates outside this list are either normalized by `normalize_predicate()` into the canonical form or routed to the `unknown` catch-all (which is filterable downstream, not silently dropped). The vocabulary is frozen for the study; it was curated and validated across roughly 50 pilot subjects before being locked. The canonical source is `memory_system/src/baselayer/config.py` lines 613-639 (`CONSTRAINED_PREDICATES`).

The predicates group into seven behavioral dimensions. The groupings below are analytical; the predicate list itself is flat in code.

**Behavioral patterns (activities and engagement).** These are the most load-bearing predicates for interpretive representation. They describe what the subject repeatedly does or refuses to do, which is what anchors the authored layers in [§3.7](#sec-3-7).

| Predicate | Definition | Example usage |
|---|---|---|
| `practices` | Repeated deliberate activity, skill-building, or routine. | (subject) `practices` daily writing |
| `avoids` | Consistent pattern of not engaging with a thing or situation. | (subject) `avoids` hierarchical social settings |
| `prefers` | Systematic choice of one option over another when both available. | (subject) `prefers` solitary work over committees |
| `follows` | Active tracking of a person, domain, or source. | (subject) `follows` developments in French art theory |
| `monitors` | Active observation, narrower than `follows`. | (subject) `monitors` his guardian's health |
| `plays` | Games, sports, musical instruments. | (subject) `plays` chess |
| `studies` | Deliberate intellectual engagement with a topic or body of work. | (subject) `studies` Renaissance painters |
| `builds` | Creation of things, relationships, or institutions. | (subject) `builds` a private library over decades |
| `manages` | Ongoing oversight or administration. | (subject) `manages` the household finances |

**Values, beliefs, and self-view.** These populate the core layer ([§3.7](#sec-3-7)) and describe the stable commitments a subject carries across situations.

| Predicate | Definition | Example usage |
|---|---|---|
| `values` | What the subject holds as important or worthy. | (subject) `values` intellectual honesty over social standing |
| `believes` | Propositional commitment, often theological or ideological. | (subject) `believes` scripture is not divinely infallible |
| `prioritizes` | Revealed-preference ranking under constraint. | (subject) `prioritizes` proximity to family over career advancement |
| `identifies_as` | How the subject labels or categorizes the self. | (subject) `identifies_as` an independent artist, not a teacher |
| `aspires_to` | Directional aspiration toward a goal or state. | (subject) `aspires_to` mastery of French prose |
| `wants_to` | Narrower than `aspires_to`; immediate desire. | (subject) `wants_to` visit the ancestral homes |

**Emotions and dispositions.** These describe affective responses, which often provide the clearest behavioral signal in autobiographical text.

| Predicate | Definition | Example usage |
|---|---|---|
| `fears` | Things, situations, or outcomes the subject avoids or guards against. | (subject) `fears` religious hypocrisy more than social ostracism |
| `loves` | Strong positive emotion, stronger than `enjoys`. | (subject) `loves` the moors near Burnley |
| `hates` | Strong negative emotion, stronger than `dislikes`. | (subject) `hates` formal balls |
| `enjoys` | Mild positive engagement. | (subject) `enjoys` long walks |
| `dislikes` | Mild negative response. | (subject) `dislikes` urban environments |
| `admires` | Respect or admiration, often toward a specific person. | (subject) `admires` Ruskin's early prose |
| `struggles_with` | Recurring difficulty or area of known weakness. | (subject) `struggles_with` time management |
| `excels_at` | Recurring demonstrated strength. | (subject) `excels_at` verbal persuasion in small groups |

**Experiences, decisions, and learning.** Transitive episodic events and the inferences drawn from them.

| Predicate | Definition | Example usage |
|---|---|---|
| `experienced` | An episodic event the subject underwent. | (subject) `experienced` his guardian's death in 1857 |
| `learned` | A concrete skill, fact, or lesson derived from experience. | (subject) `learned` that shame is more effective than instruction in driving mastery |
| `decided` | A specific documented decision or resolution. | (subject) `decided` not to pursue a political career |
| `lost` | A thing, relationship, or role no longer held. | (subject) `lost` his fortune in the poetry-book failure |
| `founded` | Institutions or groups the subject created. | (subject) `founded` a French-language art journal |

**Relationships (Session 55 expansion).** A targeted set of relationship predicates, added to raise relationship-fact extraction from 0.8% to the 3 to 5% range.

| Predicate | Definition | Example usage |
|---|---|---|
| `married_to` | Marriage relationship. | (subject) `married_to` Eugenie Gindriez |
| `parents` | The subject's parents (subject is the child). | (subject) `parents` are John and Mary Hamerton |
| `raised_by` | Parental or guardian relationship from the child's perspective. | (subject) `raised_by` his aunt after his father's death |
| `mentored_by` | Directional mentor relationship; subject was mentored. | (subject) `mentored_by` his guardian's circle |
| `friends_with` | Friendship. | (subject) `friends_with` a Doncaster schoolfellow |
| `collaborates_with` | Professional or creative collaboration. | (subject) `collaborates_with` the editor of the *Saturday Review* |
| `reports_to` | Organizational hierarchy. | (subject) `reports_to` the regimental commander |
| `relates_to` | Generic relationship fallback when the specific type is unclear. | (subject) `relates_to` the Breadalbane family as distant hosts |
| `conflicts_with` | Recurring tension or disagreement. | (subject) `conflicts_with` the Anglican social consensus |
| `maintains` | Ongoing relationship, practice, or commitment. | (subject) `maintains` correspondence with French friends |

**Biographical context.** Stable factual biographical attributes. These are not the most predictive class but are needed for disambiguation and for the anchors layer's detection conditions.

| Predicate | Definition | Example usage |
|---|---|---|
| `owns` | Property or possessions. | (subject) `owns` a house on Loch Awe |
| `works_at` | Current or past workplace. | (subject) `works_at` the *Portfolio* magazine |
| `lives_in` | Current or past residence. | (subject) `lives_in` a Scottish island |
| `raised_in` | Place where the subject grew up. | (subject) `raised_in` Lancashire |
| `attended` | Attendance at an institution (may or may not include graduation). | (subject) `attended` Doncaster Grammar School |
| `graduated_from` | Specifically graduated (distinct from `attended`). | (subject) `graduated_from` no university |
| `interested_in` | Passive interest, weaker than `follows` or `studies`. | (subject) `interested_in` heraldry |

**Fallback.**

| Predicate | Definition | Example usage |
|---|---|---|
| `unknown` | Catch-all for extracted claims that do not map cleanly to any of the 45 above. Filterable, never silently dropped. | (subject) `unknown` [unmapped extracted claim] |

### A.2 Provenance and design choices {#sec-a-2}

The vocabulary was iterated in three stages. The initial 30-predicate list (sessions 1-48) favored values, activities, and biography. Session 49 added 6 predicates (`unknown`, `attended`, `interested_in`, `wants_to`, `loves`, `hates`) to preserve semantic distinctions that the initial vocabulary collapsed. Session 52 added `plays` and `monitors`. Session 55 added 8 relationship predicates to raise relationship-fact extraction from 0.8% to the 3 to 5% target range.

The vocabulary is deliberately behavioral rather than biographical. The ratio of predicates in the behavioral-patterns plus values-beliefs plus emotions-dispositions groups (23 of 46) to the biographical-context group (7 of 46) encodes a design decision: extraction is steered away from facts that are easily verifiable in external sources (city of birth, schools attended) and toward patterns that require reading the source text to infer (what the subject avoids, prefers, values, fears).

### A.3 Not in the vocabulary {#sec-a-3}

Three predicate categories that commonly appear in general-purpose knowledge graphs are deliberately excluded:

- **Evaluative predicates about the subject from a third party** (for example, `considered_brilliant_by`). These invert the direction of claim: the subject is the object rather than the source of the reasoning.
- **Time-indexed state changes** (for example, `became`). The vocabulary handles change-over-time through the AUDN ADD / UPDATE / DELETE / NOOP operations at the fact level, not through predicate selection.
- **Causal predicates** (for example, `caused`, `triggered`). Causal inference is produced in the authored layers (predictions, anchors) from collections of facts, not encoded at the extraction step.

---

## Appendix B. Question Batteries

### B.1 The 10 fixed behavioral-prediction categories {#sec-b-1}

Every behavioral-prediction question in the study is tagged with exactly one of ten fixed categories. The category set is identical across all 15 batteries (14 main-study plus Franklin). Each category is a behavioral dimension the question probes; the category does not constrain the answer format.

| Category | What it probes | Example question |
|---|---|---|
| `decisions` | How the subject resolves concrete choices. | "When his uncle's family emigrates to New Zealand, would Hamerton consider joining them?" |
| `values` | What the subject holds as important when forced to rank. | "When confronted with German Neology, would Hamerton accept or reject the established Protestant position?" |
| `relationships` | How the subject engages with specific people or classes of people. | "How would Hamerton's religious heterodoxy affect his social standing among the Lancashire gentry?" |
| `conflict` | How the subject responds when a line is crossed. | "If his tutor attempted to physically harass him, would Hamerton submit or resist?" |
| `learning` | How the subject acquires skills, knowledge, or lessons. | "Given Hamerton's difficulty following spoken French, what would he do about it?" |
| `risk` | How the subject handles uncertainty, exposure, or irreversibility. | "Would Hamerton choose to encamp alone on remote Scottish moors, despite it being considered eccentric?" |
| `creativity` | How the subject produces or evaluates creative work. | "Would Hamerton publish his early poetry at his own expense, and what would the commercial result be?" |
| `stress` | How the subject responds to pressure, exposure, or failure. | "When offered a grand opportunity to organize an exhibition, would Hamerton accept?" |
| `career` | How the subject makes professional trajectory choices. | "Would Hamerton follow Ruskin's advice to study nature directly rather than learn from traditional masters?" |
| `change_over_time` | How the subject shifts or persists across life phases. | "After his poetry failed commercially, would Hamerton continue writing verse?" |

Each subject's battery covers 8 to 10 of these categories; no battery skips more than 2. The distribution within a subject reflects what the training half of that subject's corpus naturally supported, not a quota.

### B.2 Per-subject battery composition (10-category by 15-subject matrix) {#sec-b-2}

The following table gives the count of behavioral-prediction questions in each category for each subject. The total column is 39 for the 13 global subjects and Hamerton, and 40 for Franklin. Raw batteries are at `results/global_<subject>/battery_v2.json` (global subjects), `data/hamerton/battery.json` (Hamerton), and `data/franklin/battery.json` (Franklin).

| Subject | decis | val | rel | conf | learn | risk | creat | stress | career | ch_o_t | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| augustine | 6 | 7 | 4 | 5 | 9 | 0 | 3 | 3 | 0 | 2 | 39 |
| babur | 9 | 6 | 8 | 4 | 3 | 1 | 2 | 3 | 2 | 1 | 39 |
| bernal_diaz | 8 | 8 | 4 | 5 | 5 | 3 | 0 | 5 | 0 | 1 | 39 |
| cellini | 5 | 6 | 5 | 4 | 3 | 1 | 4 | 5 | 4 | 2 | 39 |
| ebers | 4 | 8 | 3 | 4 | 6 | 0 | 6 | 3 | 1 | 4 | 39 |
| equiano | 5 | 8 | 4 | 5 | 5 | 1 | 0 | 8 | 0 | 3 | 39 |
| fukuzawa | 8 | 11 | 5 | 5 | 3 | 1 | 1 | 2 | 0 | 3 | 39 |
| keckley | 6 | 7 | 9 | 6 | 4 | 1 | 0 | 3 | 2 | 1 | 39 |
| rousseau | 5 | 6 | 9 | 6 | 5 | 1 | 1 | 4 | 1 | 1 | 39 |
| seacole | 7 | 10 | 7 | 1 | 3 | 1 | 2 | 6 | 2 | 0 | 39 |
| sunity_devee | 4 | 9 | 6 | 5 | 5 | 1 | 1 | 6 | 0 | 2 | 39 |
| yung_wing | 10 | 8 | 3 | 3 | 3 | 1 | 3 | 2 | 5 | 1 | 39 |
| zitkala_sa | 4 | 11 | 6 | 5 | 4 | 0 | 3 | 4 | 0 | 2 | 39 |
| hamerton | 6 | 4 | 6 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 39 |
| franklin | 6 | 6 | 5 | 4 | 3 | 4 | 4 | 3 | 3 | 2 | 40 |
| **Column total** | **93** | **115** | **84** | **66** | **65** | **19** | **34** | **60** | **23** | **27** | **586** |

Columns: decis = decisions, val = values, rel = relationships, conf = conflict, learn = learning, creat = creativity, ch_o_t = change_over_time. Source: battery_v2.json and battery.json files, counted over `tier == "behavioral_prediction"` slices.

### B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING) {#sec-b-3}

A secondary classification of the same 586 questions, produced by Claude Haiku 4.5 as a post-hoc auditor, tags each question by what cognitive operation it requires the response model to perform. Full audit at `docs/research/question_category_audit.md`.

Aggregate distribution:

| Axis | n | % |
|---|---:|---:|
| LITERAL_RECALL | 60 | 10.2% |
| INTERPRETIVE_INFERENCE | 403 | 68.8% |
| REFUSAL_TRIGGERING | 123 | 21.0% |

Per-subject distribution:

| Subject | LITERAL | INTERP | REFUSAL | n |
|---|---:|---:|---:|---:|
| augustine | 4 | 33 | 2 | 39 |
| babur | 1 | 25 | 13 | 39 |
| bernal_diaz | 2 | 28 | 9 | 39 |
| cellini | 4 | 27 | 8 | 39 |
| ebers | 2 | 30 | 7 | 39 |
| equiano | 6 | 27 | 6 | 39 |
| fukuzawa | 4 | 27 | 8 | 39 |
| keckley | 4 | 30 | 5 | 39 |
| rousseau | 2 | 32 | 5 | 39 |
| seacole | 8 | 28 | 3 | 39 |
| sunity_devee | 8 | 23 | 8 | 39 |
| yung_wing | 3 | 24 | 12 | 39 |
| zitkala_sa | 2 | 22 | 15 | 39 |
| hamerton | 10 | 10 | 19 | 39 |
| franklin | 0 | 37 | 3 | 40 |

### B.4 Category-level effect size on Δ_spec {#sec-b-4}

Mean Δ_spec (C2a minus C5) broken down by the behavioral-axis classification. Source: `docs/research/question_category_audit.md`.

| Axis | n | Mean Δ_spec | Median Δ_spec |
|---|---:|---:|---:|
| LITERAL_RECALL | 60 | +0.792 | +0.800 |
| INTERPRETIVE_INFERENCE | 366 | +0.397 | +0.400 |
| REFUSAL_TRIGGERING | 120 | +0.417 | +0.200 |

The LITERAL_RECALL bucket is small (n = 60) per subject, so per-subject estimates are high-variance, but the aggregate is robust within that constraint. The unexpected finding (that LITERAL_RECALL Δ_spec exceeds INTERPRETIVE_INFERENCE Δ_spec) is discussed in the audit doc: a plausible mechanism is stylistic-register match between the spec's Victorian prose and Hamerton's held-out text, not genuine fact recall. The INTERPRETIVE_INFERENCE signal (n = 366, Δ = +0.397) is the cleanest between-condition evidence that the spec performs representational work rather than register-matching.

### B.5 Per-subject by axis Δ_spec {#sec-b-5}

Full breakdown at `docs/research/question_category_audit.md` and per-subject axis-Δ scaffold values at `docs/research/v11_emit/appendix_b_battery.json` (claim ids `appB_5_<subject>_<axis>_delta`). Summary of the cross-subject pattern under 5-judge primary aggregation: the strongest positive spec effects cluster on three subjects. Hamerton (LITERAL +1.68, INTERP +1.30, REFUSAL +1.25), Sunity Devee (+1.38 / +1.16 / +1.35), and Bernal Diaz (+2.00 / +0.44 / +0.64) carry the largest gains. Augustine, Equiano, and Zitkala-Sa show negative or near-zero deltas across all three axes, consistent with their status as mid-baseline subjects on the [§4.1](#sec-4-1) gradient. Fukuzawa and Seacole show their largest positive effects on INTERPRETIVE_INFERENCE specifically (+0.83 and +0.79). Bernal Diaz's +2.00 on LITERAL_RECALL is computed over a small per-axis n (single-digit questions per axis per subject), so the per-subject estimate is high-variance; the cross-subject correlation pattern in [§B.6](#sec-b-6) is the more robust signal.

### B.6 Battery-composition sensitivity {#sec-b-6}

This appendix provides the technical detail behind the [§4.1](#sec-4-1) battery-sensitivity controls.

**B.6.1 Battery-question-type correlations.**

Across the 14 main-study subjects:

- Δ_spec range: −0.31 to +1.37
- Corr(fraction of LITERAL_RECALL questions, subject-level Δ_spec): r = +0.595 [^fn22]
- Corr(fraction of INTERPRETIVE_INFERENCE questions, subject-level Δ_spec): r = −0.466 (legacy: −0.582, same caveat)
- Corr(fraction of REFUSAL_TRIGGERING questions, subject-level Δ_spec): r = +0.212

The positive LITERAL_RECALL correlation and negative INTERPRETIVE correlation imply that subjects whose batteries over-weight literal recall also produce larger measured Δ_spec values.

**B.6.2 Multiple regression controlling for LITERAL_RECALL fraction.**

A multiple regression of Δ_C4a on both C5 baseline and LITERAL_RECALL fraction across the 14 main-study subjects yields a partial coefficient on baseline of **−0.88 [95% CI −1.13, −0.63], p < 10⁻⁵**, attenuated from the univariate −0.96 by about 8%. LITERAL_RECALL fraction enters as a significant partial predictor (β = +2.30 [+0.34, +4.26], p = 0.026), but baseline carries the bulk of the explained variance: 63.6% uniquely attributable to C5, 6.9% uniquely attributable to LITERAL_RECALL fraction. The two predictors are not collinear (Pearson r = −0.28, VIF = 1.08 for both), so the partial coefficients are stable. Adjusted R² rises from 0.80 to 0.87 when LITERAL_RECALL fraction is added; the controls are additive rather than redundant. The gradient on baseline survives; it is not an artifact of battery composition.

**B.6.3 Hamerton-leverage subset regression.**

Hamerton's 80-question battery predates the global-subject pipeline and uses a slightly different backward-design path (the legacy Haiku 4.5 generator that originally produced Franklin and Hamerton); the 13 global subjects' main-study batteries also use Claude Haiku 4.5 but were regenerated by `run_global_rerun.py` against a uniform prompt template. All 14 main-study batteries share the same generator family. A subset regression dropping Hamerton (N=13 globals) yields a slope of **−0.89 [95% CI −1.18, −0.61], R² = 0.81, p < 10⁻⁴**, compared to the full-sample −0.96. The point estimate attenuates by about 7%, and the 95% CIs overlap substantially. The gradient is not Hamerton-driven. A separate GPT-5.4-regenerated battery set (`results/global_<subject>/battery_gpt54.json`) exists for each global as a circularity control; its results are reported in [§3.3.1](#sec-3-3-1) and [§4.6.1](#sec-4-6-1), not folded back into the [§4.1](#sec-4-1) gradient itself.

**B.6.4 Discussion.**

This is a battery-composition confound in the cross-subject gradient; the paper's gradient claim is therefore specifically about mean score movement per subject, not about mean score movement per category. [§5.3](#sec-5-3) and §7 flag a follow-up study with a category-balanced battery as the primary design improvement for future gradient work.

**B.6.5 Hamerton-leverage at the per-question grain.**

The B.6.3 subset regression checks the per-subject mean grain. A parallel question is whether the per-question extreme upward anchor crossings catalogued in `docs/research/wins_inventory_20260428.json` (60 unique cases across 18 condition pairs, 351 paired low-baseline questions on C5 to C4a) are concentrated on Hamerton specifically. They are: Hamerton accounts for 15 of the 60 unique extreme jumps (25%) on a battery of 80 questions (18.75% extreme-jump rate); the other 13 subjects average 8.9% extreme-jump rate across 39-question batteries. Hamerton's elevation is real but its cause is not isolated by the present design. Three candidate mechanisms (legacy battery-generator path, subject pretraining thinness, behavioral-predicate density per word) are not separately identifiable, since Hamerton's served spec is 1918 words (brief-only) versus globals' ~5775 words (anchors + core + predictions + brief), so spec length is anti-correlated with extreme-jump rate. As measured by the heuristic classifier, the mechanism distribution on Hamerton's 15 jumps versus globals' 45 is nearly identical (PATTERN_PREDICATE+HYBRID share: Hamerton 73.3% vs globals 80.0%); the heuristic does not discriminate jumps from non-jumping spec-loaded controls (`docs/research/pattern_activation_deep_20260428.md`), so this near-identity is consistent with the heuristic detecting spec-loaded response style rather than the lift mechanism.

### B.7 Coupling-free reframing of the gradient {#sec-b-7}

The headline slope regresses Δ_C4a = C4a − C5 on C5, which mechanically embeds a −1 component when C4a is bounded on the 1-5 scale and partially independent of C5. To triangulate from a non-coupling-prone angle, we ran three additional checks on the same per-subject (C5, C4a) data (script: `scripts/_v10_coupling_sensitivity.py`; full output: `docs/research/v10_coupling_sensitivity_analysis.md`).

**B.7.1 Level regression.**

The level regression C4a ~ C5 produces a slope of **+0.04** [95% CI −0.24, +0.33], R² = 0.008, p = 0.76. C4a is essentially flat across the C5 range of 1.02-2.77 and clusters tightly around its mean of **2.46** at the per-subject grain. The spec does not differentially "lift" low-baseline subjects more than high-baseline ones in any treatment-effect-heterogeneity sense; it produces a roughly constant post-spec C4a mean per subject regardless of baseline, and the apparent Δ-on-C5 gradient equals the baseline shortfall.

**B.7.2 Permutation test.**

A 10,000-iteration permutation test that shuffles C4a across subjects (preserving the bounded marginal but breaking any link to C5) yields a null distribution for the Δ-on-C5 slope centered at −0.998 (SD 0.127). The observed −0.960 is not extreme against this null (two-sided p = 0.77). In plain language: even when C4a values are randomly reshuffled across subjects, the Δ-on-C5 slope still lands near −1 on average, because the change-score parameterization mechanically pushes the slope toward −1 whenever C4a is roughly independent of C5. The −0.96 the headline regression reports is what the regression arithmetic forces, not independent evidence that low-baseline subjects benefit more from the spec at the per-subject mean grain.

**B.7.3 Bootstrap.**

A 10,000-iteration subject-level bootstrap returns CIs of [−1.254, −0.740] for the Δ-on-C5 slope and [−0.254, +0.260] for the level slope. The level CI straddles zero, consistent with the level-regression finding that the per-subject C4a mean is roughly constant across baselines.

**B.7.4 Reading the gradient against this.**

The substantive finding survives the coupling check, but its framing has to shift away from "the spec acts more strongly on low-baseline subjects" toward the per-question reframing in [§4.1](#sec-4-1): low-baseline subjects have a larger pool of questions at low rubric anchors, so the spec has more opportunity to produce upward integer-band crossings, which aggregates as a larger per-subject mean lift. The directional asymmetry on those crossings [^fn23] is consistent with the [§4.2](#sec-4-2) finding that even the full source corpus C8 plateaus at a similar per-subject mean.

### B.8 Per-predicate ablation (Phase 2c) {#sec-b-8}

To probe whether single behavioral predicates within the spec are uniquely load-bearing, we ran a per-sentence ablation experiment on a stratified sample of 16 extreme-upward-jump cases. For each case, the heuristically-identified causal predicate (highest-token-overlap spec sentence vs the question and held-out passage) was located in the served spec and three response variants were generated at temperature 0 with Claude Haiku 4.5: (1) original (full spec), (2) ablated (predicate removed, replaced with a length-matched neutral biographical filler), (3) reversed (predicate replaced with a behavioral opposite synthesized by Sonnet). Each variant was scored by the 5-judge primary panel.

Results (script: `scripts/run_predicate_ablation.py`; data: `docs/research/predicate_ablation_results_20260428.json`):

- Mean Δ_removal (original minus ablated) across 16 cases: +0.05 anchor points (95% CI [−0.35, +0.45])
- Mean Δ_reversal (original minus reversed): −0.24 anchor points (95% CI [−0.45, −0.02])
- 2 of 16 cases showed Δ_removal ≥1 anchor; 11 of 16 had Δ_removal < 0.5

Single-predicate removal does not measurably reduce response quality on this sample. The paper does not interpret this as evidence that the spec is mechanistically inert: the higher-level mechanism evidence from the wrong-spec adversarial control (Appendix C / [§4.3](#sec-4-3)) shows the spec as a whole is doing causal work. The null result on per-sentence ablation is consistent with redundant spec construction, in which multiple sentences across the anchors / core / predictions / brief layers reinforce the same behavioral patterns; removal of any single sentence leaves the pattern accessible elsewhere in the spec.

A methodological caveat applies. Original-condition reproduction at temperature 0 was not bit-exact deterministic across reruns; mean drift between the recorded original score (from `docs/research/wins_inventory_20260428.json`) and the rerun original score was −1.44 anchors, with 9 of 16 cases drifting by more than 1 anchor. Some of the variance in Δ_removal is rerun stochasticity rather than ablation effect. The extreme-upward-jump cases specifically show higher pipeline variance than the per-subject mean grain documented in [§6.3](#sec-6-3).

Future work tightening (per the test's own report): human-rated predicate identification (vs heuristic), larger N (all 47 PATTERN_PREDICATE cases), irrelevant-predicate control (matched-length unrelated predicate to test the "any rich persona text" alternative), multi-predicate cluster ablation.

### B.9 Footnote-redirect technical detail {#sec-b-9}

This subsection holds the longer technical content for footnotes that would otherwise grow to multi-paragraph length. Each entry is keyed to the footnote name in the body.

**B.9.1 `[^delta-aggregation]`. +0.89 vs +0.93 reconciliation.**

The +0.89 figure is the canonical cross-subject mean of per-subject Δ_C4a. Each subject's Δ is computed as that subject's per-question 5-judge primary mean under C4a minus their per-question mean under C5; these per-subject Δs are then averaged across the 9 low-baseline subjects. The grand-mean alternative grand-averages all per-question scores under each condition first and then takes the difference, yielding +0.93 (the difference of the C4a grand mean 2.45 and the C5 grand mean 1.52). The two numbers are not in conflict; they answer slightly different questions. The per-subject-mean grain (+0.89) is the unit of inference used throughout this paper because every statistic is computed at the subject level first, then aggregated across the 14 subjects ([§1.2](#sec-1-2) aggregation rule).

**B.9.2 `[^heldout-leakage-audit]`. Held-out leakage audit detail.**

A held-out leakage audit on the 60 unique extreme-upward-jump cases (full report at `docs/research/held_out_leakage_investigation_20260428.md`) found 0 6-gram, 2 4-gram, and 12 3-gram matches between held-out passages and C4a responses. Of the 9 cases with any leak, 6 are short generic phrases also resident in the served facts list (CORPUS_LEAK), 2 are subject-specific n-grams not in any served context (best explained by pretraining recall of public-domain autobiographies; PRETRAINING_MEMO_CANDIDATE), and 1 is generic English (COMMON_PHRASE). The longest shared run anywhere is 4 tokens, well below transcription length. Severity verdict: rare; no structural validity concern; footnote acknowledgement is the appropriate paper-text treatment. Excluding the 2 pretraining-memorization candidates from the extreme-upward-jump set shifts the C5 to C4a low-baseline extreme-jump count by at most 1 (20 to 19); per-subject mean Δs are unchanged at the per-question level. The "held-out passage" was held out from served spec / facts, not from pretraining, and the audit confirms that interpretation: where C4a held-out-to-post leakage exists, it is either short generic phrasing also resident in the served facts (trivially short) or subject-specific content in the model's pretraining, not study-design contamination of the served context.

**B.9.3 `[^supermemory-no-retrieval]`. Supermemory NO_RETRIEVAL placeholders.**

Across the full 14-subject Supermemory analysis, 30 individual responses (Augustine 2 questions, Equiano 28 questions) were Supermemory provider-failure placeholders rather than substantive predictions, scored at the rubric floor (1) by the judge panel. We treat these as scored data rather than missing data, consistent with how the rest of the study handles low-quality responses. Excluding the 30 NO_RETRIEVAL records as missing data would shift Supermemory's aggregate Δ slightly higher; the qualitative story (small aggregate at both grains, bimodal per-question distribution) holds either way.

---

## Appendix C. Conditions, Models, and Memory-System Configurations

### C.1 Condition identifiers (summary card) {#sec-c-1}

A consolidated lookup for the condition IDs used throughout §4. Defined in [§3.4](#sec-3-4); summarized here.

| ID | Family | Context served | Purpose |
|---|---|---|---|
| C5 | Direct | None. Question only. | Pretraining-only floor. Baseline. |
| C2a | Direct | Behavioral Specification only. | Isolate spec's contribution. |
| C2c | Direct | A random other subject's spec (derangement, seed=42). | Wrong-spec control. |
| C4 | Direct | Full extracted fact set for subject. | Raw fact volume, no structure. |
| C4a | Direct | Full facts plus spec. | Spec added to raw facts. |
| C8 | Direct | Full training corpus (half of source text). | Uncompressed source. |
| C9 | Direct | Training corpus plus spec. | Spec added to raw source. Babur excluded (422K word overflow). |
| C1 | Memory system | Top-k retrieval output from system. | Retrieval only, each of 5 systems. |
| C3 | Memory system | Top-k retrieval output plus spec. | Retrieval plus spec, each of 5 systems. |
| C1_\<system\>_fullpipeline | Memory system, native | Retrieval from system-native ingestion of raw corpus. | Native ingestion variant, retrieval only. |
| C3_\<system\>_fullpipeline | Memory system, native | Native ingestion retrieval plus spec. | Native ingestion variant, retrieval plus spec. |

The `<system>` slot ranges over {mem0, letta, supermemory, zep, baselayer}. Base Layer is run in a single controlled configuration; the four commercial systems are run in both controlled and native variants.

### C.2 Shared response-model invocation {#sec-c-2}

Every response call, across every direct-context and memory-system condition, uses the following parameters:

| Parameter | Value |
|---|---|
| `temperature` | 0 |
| `max_tokens` | 1024 |
| System prompt | Framing instruction: predict how `<subject>` would respond; answer in subject's voice, grounded in demonstrated patterns. |
| User prompt format | `<context block>\n\nQuestion: <question text>` |
| Context block | Condition-dependent. Empty in C5. Spec in C2a. Wrong spec in C2c. Facts in C4. Facts plus spec in C4a. Corpus in C8. Corpus plus spec in C9. Retrieval output (optionally plus spec) in C1 and C3. |

No prompt instruction coaches the model to abstain, hedge, or commit. The model's refusal-or-commitment pattern given a specific context is part of the phenomenon being measured ([§3.5](#sec-3-5), [§4.3](#sec-4-3)).

### C.3 Response models {#sec-c-3}

| Role | Model identifier | Provider | Scope |
|---|---|---|---|
| Primary response | `claude-haiku-4-5-20251001` | Anthropic | All 14 subjects, every condition. Main study. |
| Tier 2 response | `claude-sonnet-4-6` | Anthropic | 3 subjects (Ebers, Yung Wing, Zitkala-Sa), C5 / C2a / C2c / C4a against GPT-5.4 batteries. |
| Tier 2 response | `gemini-2.5-pro` | Google | Same 3 subjects, same conditions as Sonnet Tier 2. |

Source: `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, `scripts/run_multimodel_responses.py`.

### C.4 Pipeline models (specification generation) {#sec-c-4}

| Pipeline step | Model identifier | Temperature | Purpose |
|---|---|---|---|
| Extract (Step 2) | `claude-haiku-4-5-20251001` | 0 | AUDN fact extraction, 46-predicate constrained vocabulary. |
| Embed (Step 3) | `all-MiniLM-L6-v2` (local) | n/a | ChromaDB vector index (L2 distance). |
| Author (Step 4) | `claude-sonnet-4-6` | 0 | Three authored layers (anchors, core, predictions). Blind regen, domain guard. |
| Compose (Step 5) | `claude-opus-4-6` | 0 | Unified brief composition. |
| Battery generation | `claude-haiku-4-5-20251001` | 0 | Backward-design from held-out corpus. |
| Battery generation (circularity control) | `gpt-5.4` (via OpenAI API) | 0 | Independent regeneration on 13 global subjects. |

Source: `memory_system/src/baselayer/config.py`.

### C.5 Judge panel {#sec-c-5}

| Judge | Model identifier | Provider | In 5-judge primary? | Calibration performed? |
|---|---|---|:---:|:---:|
| Haiku | `claude-haiku-4-5-20251001` | Anthropic | Yes | Yes |
| Sonnet | `claude-sonnet-4-6` | Anthropic | Yes | No |
| Opus | `claude-opus-4-6` | Anthropic | Yes | No |
| GPT-4o | `gpt-4o-2024-08-06` | OpenAI | Yes | Yes |
| GPT-5.4 | `gpt-5.4` | OpenAI | Yes | Yes |
| Gemini Flash | `gemini-2.5-flash` | Google | No (sensitivity only) | Yes |
| Gemini Pro | `gemini-2.5-pro` | Google | No (sensitivity only) | Yes |

Judges are invoked independently (no cross-judge conditioning). Each judge sees: held-out ground-truth passage, subject context (name, source), question, response. Judge temperature 0. Judge output is a numeric 1-5 score plus a free-text justification. Calibration diagnostic results in [§3.6.3](#sec-3-6-3).

### C.6 Memory-system ingestion and retrieval parameters {#sec-c-6}

Controlled configuration (C1 / C3) holds the input identical across systems: each system receives the same extracted fact set used by the Base Layer pipeline, re-ingested through its own API. Native configuration (`_fullpipeline`) has each system ingest the raw training corpus directly via its own chunking and extraction.

| System | Ingestion endpoint | Ingestion unit (controlled) | Ingestion unit (native) | Retrieval top-k | Notable configuration |
|---|---|---|---|---:|---|
| Mem0 | `POST /v1/memories/` | One fact per POST | Raw corpus chunks (Mem0 chunker) | 10 | `infer=False` on controlled (store as-is, no reformulation). Failure mode: Mem0 may reformulate on `infer=True`, flagged in `docs/PROVIDER_ISSUES.md`. |
| Letta (archival) | `POST /v1/agents/<id>/core_memory/archival` | One fact per passage | Letta native chunking | 10 | 1 fact = 1 passage. Batch ingestion tested 135x faster but changes chunking behavior (see `run_memory_system.py` line 456-458). |
| Letta (stateful) | Agent state edit during ingestion | One fact per edit cycle | Raw corpus | n/a (read from block) | Evaluated as a separate path in §4.5, not as a row in the C1 / C3 conditions. |
| Supermemory | `POST /v3/memories` | One fact per memory, `containerTags=<subject>` | Raw corpus | 10 | `limit=10` on retrieval. |
| Zep | Graph ingestion via `zep_client.graph.add` | One fact per edge | Raw corpus | 10 | Retrieval via `client.graph.search(user_id, query, limit=10)`. |
| Base Layer | Direct into ChromaDB | One fact per vector | n/a (Base Layer has no native variant) | 10 | MiniLM embeddings, L2 distance, cosine-like similarity via `1 - dist^2/2`. |

All five systems use the same top-k of 10. All five are queried with the question text as the query. All five feed their retrieval output into the standard prompt schema ([§C.2](#sec-c-2)) as the context block.

### C.7 Ingestion exclusions and failure cases {#sec-c-7}

| Subject / system | Issue | Resolution |
|---|---|---|
| Babur, C9 (raw corpus plus spec) | 422,772-word source exceeds Haiku context window. | Excluded from C9. 13 of 14 subjects report C9 numbers. |
| Letta native (all subjects) | Ingestion ceiling on archival passages; retrieval produces 0.34-0.47 dedup ratio, meaning a top-10 list often contains 3-5 unique facts. | Reported as-is in §4.4. Not excluded. |
| Mem0 native | Mem0's `infer=True` reformulated facts during native ingestion pilot. | Used `infer=False` on controlled configuration to hold input identical. Native variant retains `infer=True` (the realistic deployment path). |
| Zep graph bias | Zep graph retrieval surfaces entity-dense chunks over behavior-dense chunks. | Reported as-is. See `docs/PROVIDER_ISSUES.md`. |

### C.8 Analysis plan lock {#sec-c-8}

The condition matrix was frozen in `docs/ANALYSIS_PLAN_LOCK.md` before scoring. Any condition added after the lock is reported separately [^fn24].

---

## Appendix D. Validity Audit and Score Distributions

![Figure D.1: Baseline pretraining coverage clusters by cultural region rather than by subject "importance," motivating the C5 ≤ 2.0 low-baseline slice as the population of relevance. C5 baseline score (x-axis) per subject, sorted low to high, with color and hatching encoding whether the specification improved that subject (§3.2.1, §4.1). 9 of 14 main-study subjects fall in the low-baseline band (Sunity Devee, Ebers, Hamerton, Fukuzawa, Bernal Diaz, Babur, Seacole, Keckley, Yung Wing); 5 fall in the mid-baseline band (Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano); Franklin alone (3.77) sits in the high-baseline band as the known-figure control.](C:/Users/Aarik/Anthropic/memory-study-repo/figures/fig9_cultural_baseline.png)

*Figure D.1: Baseline pretraining coverage clusters by cultural region rather than by subject "importance," motivating the C5 ≤ 2.0 low-baseline slice as the population of relevance. C5 baseline score (x-axis) per subject, sorted low to high, with color and hatching encoding whether the specification improved that subject (§3.2.1, §4.1). 9 of 14 main-study subjects fall in the low-baseline band (Sunity Devee, Ebers, Hamerton, Fukuzawa, Bernal Diaz, Babur, Seacole, Keckley, Yung Wing); 5 fall in the mid-baseline band (Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano); Franklin alone (3.77) sits in the high-baseline band as the known-figure control.*

### D.1 Per-subject 5-judge primary aggregate (main gradient) {#sec-d-1}

This table reproduces the [§4.1](#sec-4-1) cross-subject gradient for reference. Every number is the 5-judge primary mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) over the 39-question behavioral-prediction battery per subject (40 for Franklin).

| Subject | Baseline (C5) | Spec only (C2a) | Facts + Spec (C4a) | Δ_spec | Δ_facts+spec | Anchor crossed |
|---|---:|---:|---:|---:|---:|:-:|
| Ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | yes |
| Sunity Devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | yes |
| Hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | yes |
| Fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | yes |
| Bernal Diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | partial |
| Babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | no |
| Seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | yes |
| Keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | no |
| Yung Wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | no |
| Zitkala-Sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | no |
| Cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | no |
| Rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | no |
| Augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | no |
| Equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | no |
| Franklin (control) | 3.77 | 3.37 | 3.65 | −0.40 | −0.13 | no |

Raw per-judge files: `results/global_<subject>/judgments_v2.json` and `*_judgments_<judge>.json` (per-judge) for the 13 globals. Hamerton: `results/hamerton/*_judgments_<judge>.json`. Franklin: `results/franklin_legacy_20260411/analysis/*_judgments.json`.

### D.2 Per-subject anchor-crossing on the low-baseline slice {#sec-d-2}

Anchor-crossing rate is the fraction of per-question paired (C5, C4a) responses where the C4a 5-judge primary mean lands in a different integer rubric band than the C5 mean. Definition in [§3.6.2](#sec-3-6-2) and `scripts/compute_anchor_crossing.py`.

Slice-level:

- Total low-baseline questions (9 subjects, 39 Q each): 351
- Upward crossings: 193 (55.0%)
- Downward crossings: 24 (6.8%)
- Stayed in band: 134 (38.2%)

Per-subject breakdown (5-judge primary, paired C5 vs. C4a over N=39 per subject):

| Subject | Upward | Upward % | Downward | No crossing |
|---|---:|---:|---:|---:|
| Sunity Devee | 29 | 74.4% | 0 | 10 |
| Hamerton | 27 | 69.2% | 0 | 12 |
| Fukuzawa | 26 | 66.7% | 3 | 10 |
| Bernal Diaz | 23 | 59.0% | 3 | 13 |
| Seacole | 21 | 53.8% | 3 | 15 |
| Ebers | 19 | 48.7% | 0 | 20 |
| Keckley | 19 | 48.7% | 6 | 14 |
| Yung Wing | 19 | 48.7% | 5 | 15 |
| Babur | 10 | 25.6% | 4 | 25 |
| **Slice total** | **193** | **55.0%** | **24** | **134** |

Eight of the nine low-baseline subjects cluster in the 48-74% upward band. Babur is the low-baseline outlier (source corpus 422K words, partial pretraining exposure); he is the only subject whose upward-crossing rate falls below 48%, and his downward-crossing count (4 of 39) is mid-range. Sunity Devee's 74.4% upward rate is consistent with her unusually low C5 baseline of 1.03 noted in [§4.1](#sec-4-1). Per-subject downward-crossing rates stay at or below 15% for every low-baseline subject. Source: `scripts/compute_anchor_crossing.py` executed against `results/global_<subject>/judgments_v2.json` and `results/hamerton/`.

### D.3 Rubric-handling validity audit (full report) {#sec-d-3}

This audit is the formal report that [§3.6.6](#sec-3-6-6) summarizes. It was produced by `scripts/audit_low_end_inflation.py`. Raw flagged cases live in `docs/research/s114_low_end_inflation_audit.json`; source response and judgment data are under `results/global_<subject>/`. The audit is restricted to the 9 low-baseline subjects (1,599 responses across C5, C2a, C2c, C4, C4a conditions).

**D.3.1 Abstention detection.**

Abstention patterns were matched by regular expression against response text. Pattern list includes variants of "I don't have specific information," "there is no explicit documented," "I cannot confirm," "I am not certain," "would need additional context," "my training data does not," and related phrasings. Full pattern list in `scripts/audit_low_end_inflation.py` lines 29-42. 192 of 1,599 low-baseline responses (12.0%) matched one or more abstention patterns.

**D.3.2 Score distribution of abstention-matching responses.**

The rubric's lowest anchor is "refuses or off-base." An honest refusal should score at or below 1.5 (closer to rubric-1 than to rubric-2). The distribution of 5-judge primary means over the 192 abstention-matching responses:

| 5-judge primary band | Count | % of abstentions |
|---:|---:|---:|
| 1.0 to 1.5 | 159 | 82.8% |
| 1.5 to 2.0 | 15 | 7.8% |
| 2.0 to 2.5 | 12 | 6.3% |
| 2.5 to 3.0 | 2 | 1.0% |
| 3.0 to 3.5 | 2 | 1.0% |
| 3.5 and above | 2 | 1.0% |

82.8% of abstentions score in the expected band. 18 of 192 abstentions (9.4%) score at or above 2.0, and 6 of 192 (3.2%) score at or above 3.0. Mean abstention score: 1.27 (expected: close to 1.0). Under a clean rubric these would all be closer to 1.0; the over-credit reflects judges giving partial marks for adjacent-fact recitation or for correctly identifying what the context does not contain.

**D.3.3 Per-judge strictness on abstention-matching responses.**

Primary 5-judge panel only. Mean score on the 192 abstention-matching responses:

| Judge | Mean on abstentions |
|---|---:|
| Sonnet 4.6 | 1.14 |
| GPT-5.4 | 1.17 |
| Haiku 4.5 | 1.29 |
| GPT-4o | 1.34 |
| Opus 4.6 | 1.41 |

Spread: 0.27 points between strictest (Sonnet) and most lenient (Opus). No judge reaches the rubric-1 floor on average. The 5-judge primary average (1.27) smooths this cross-judge variance without eliminating it.

**D.3.4 Length-score correlation.**

Pearson correlation between response length (character count) and 5-judge primary score, across the 1,599 low-baseline responses:

| Slice | n | r | Interpretation |
|---|---:|---:|---|
| All responses | 1,599 | 0.26 | Modest positive, driven almost entirely by C5. |
| C5 (baseline, no context) | 312 | 0.604 | Strong positive. Longer baseline responses score higher. |
| C2a (spec only) | 351 | 0.14 | Near zero. |
| C4 (facts alone) | 312 | 0.01 | Zero. |
| C4a (facts plus spec) | 312 | −0.01 | Zero. |
| C2c (wrong spec) | 312 | 0.500 | Strong positive. Wrong-spec responses resemble C5 on the length-score axis. |

The effect is strongest in C5 (r = 0.604) and recurs, attenuated, in C2c (r = 0.500). Both are conditions without a ground-truth representation of the subject: C5 has no context at all, and C2c has a randomly-drawn other subject's specification. In both, longer responses (containing hedging, adjacent-fact recitation, disambiguation offers) score higher than short refusals. Conditions that do carry a correct specification (C2a, C4, C4a) show near-zero length correlation. The direction of the bias pushes the measured C5 and C2c means upward, which shrinks the measured spec-vs-no-spec gap relative to the true gap. That the length signal persists in C2c, but not in C2a or C4a, is the cleanest evidence that length inflation is a property of the baseline-scoring regime rather than of any specific condition: when judges cannot verify against a correct representation, they partial-credit verbose output.

**D.3.5 Ultra-high-score validity.**

Ultra-high responses are those scoring 4.5 or above on the 5-judge primary. Length comparison:

| Response class | Mean length (chars) | Notes |
|---|---:|---|
| Ultra-high (score 4.5 or above) | 2,790 | Not length-inflated. |
| Mid-range (2.5 to 3.5) | 2,829 | Baseline comparison. |
| Low (score below 2.0) | 2,087 | n = 795. Shorter than both ultra-high and mid-range; confirms length inflation is a low-end partial-credit phenomenon, not a high-end one. |

Ultra-high responses are not longer than mid-range responses. Length inflation is a low-end phenomenon, not a universal one. The hypothesis that "ultra-high responses equal length-inflated responses" is rejected by this comparison.

**D.3.6 Implications for reported effects.**

Both rubric-handling effects (abstention over-credit at the low end, length inflation in C5) pull the measured C5 baseline upward. This shrinks the measured spec-vs-baseline gap. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift reported in [§4.1](#sec-4-1). The paper reports the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact. A differentiated rubric that scores abstention as its own dimension, and a length-controlled scoring protocol, are both flagged as follow-up in §7.


```{=openxml}
<w:p><w:pPr><w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>
```

### D.4 Per-judge score matrices {#sec-d-4}

Per-subject by per-judge score means for C5 (baseline) and C4a (facts plus spec) conditions are derivable from the raw per-judge JSON files under `results/global_<subject>/*_judgments_<judge>.json` (and `results/hamerton/` for Hamerton). The slice-level picture is already reported in [§3.6.3](#sec-3-6-3) (calibration) and [§4.6.2](#sec-4-6-2) (5-judge vs 7-judge sensitivity), which together establish that directional agreement is tight (Spearman ρ 0.86 to 0.93) while absolute magnitude varies (Krippendorff α 0.659 5-judge, 0.535 7-judge).

Full per-subject by per-judge by per-condition mean-score matrix for the 14 main-study subjects across the 5 gradient conditions (C5, C2a, C2c, C4, C4a):

Each cell is the per-judge mean score across all behavioral-prediction questions for a (subject, condition, judge) triple. Judges abbreviated: H=Haiku 4.5, S=Sonnet 4.6, O=Opus 4.6, 4o=GPT-4o, 5.4=GPT-5.4, gF=Gemini 2.5 Flash, gP=Gemini 2.5 Pro. 5m = 5-judge primary mean, 7m = 7-judge mean.

"n/a" indicates missing judge-condition coverage (most commonly: Gemini judges not run on C2c or C4 for some subjects; see [§4.6.2](#sec-4-6-2) on 5-judge vs 7-judge coverage).

| Subject | Cond | H | S | O | 4o | 5.4 | gF | gP | 5m | 7m |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hamerton | C5 | 1.23 | 1.15 | 1.36 | 1.33 | 1.21 | 1.28 | 1.16 | 1.26 | 1.25 |
|  | C2a | 2.72 | 2.13 | 3.05 | 2.67 | 2.59 | 3.49 | 3.50 | 2.63 | 2.88 |
|  | C2c | 1.38 | 1.36 | 1.69 | 1.38 | 1.44 | 2.03 | 2.56 | 1.45 | 1.69 |
|  | C4 | 2.26 | 2.26 | 2.87 | 2.33 | 2.41 | 2.64 | 3.11 | 2.43 | 2.55 |
|  | C4a | 2.69 | 2.38 | 3.26 | 2.87 | 2.64 | 3.87 | 3.92 | 2.77 | 3.09 |
| Sunity Devee | C5 | 1.03 | 1.00 | 1.05 | 1.05 | 1.00 | 1.08 | n/a | 1.03 | 1.03 |
|  | C2a | 2.41 | 1.79 | 2.56 | 2.15 | 2.41 | 3.49 | n/a | 2.27 | 2.47 |
|  | C2c | 1.28 | 1.13 | 1.38 | 1.38 | 1.28 | 1.72 | n/a | 1.29 | 1.36 |
|  | C4 | 2.59 | 2.15 | 2.74 | 2.44 | 2.38 | 3.54 | n/a | 2.46 | 2.64 |
|  | C4a | 2.46 | 2.13 | 2.59 | 2.49 | 2.38 | 3.58 | n/a | 2.41 | 2.61 |
| Ebers | C5 | 1.00 | 1.00 | 1.05 | 1.05 | 1.00 | 1.13 | n/a | 1.02 | 1.04 |
|  | C2a | 1.49 | 1.31 | 1.82 | 1.56 | 1.51 | 3.08 | n/a | 1.54 | 1.79 |
|  | C2c | 1.41 | 1.10 | 1.38 | 1.44 | 1.26 | 2.44 | n/a | 1.32 | 1.50 |
|  | C4 | 2.21 | 1.59 | 2.26 | 2.03 | 2.03 | 3.15 | n/a | 2.02 | 2.21 |
|  | C4a | 2.26 | 1.62 | 2.31 | 2.10 | 2.08 | 3.67 | n/a | 2.07 | 2.34 |
| Fukuzawa | C5 | 1.64 | 1.44 | 2.00 | 1.64 | 1.64 | 2.46 | n/a | 1.67 | 1.80 |
|  | C2a | 2.18 | 1.97 | 2.79 | 2.41 | 2.41 | 3.56 | n/a | 2.35 | 2.56 |
|  | C2c | 1.85 | 1.49 | 2.38 | 2.21 | 1.74 | 2.97 | n/a | 1.93 | 2.11 |
|  | C4 | 2.95 | 2.28 | 3.00 | 2.54 | 2.59 | 3.95 | n/a | 2.67 | 2.88 |
|  | C4a | 2.85 | 2.26 | 3.21 | 2.77 | 2.82 | 4.03 | n/a | 2.78 | 2.99 |
| Seacole | C5 | 1.69 | 1.49 | 1.92 | 2.00 | 1.77 | 2.24 | n/a | 1.77 | 1.85 |
|  | C2a | 2.44 | 2.08 | 2.72 | 2.56 | 2.62 | 3.44 | n/a | 2.48 | 2.64 |
|  | C2c | 1.33 | 1.26 | 1.69 | 1.49 | 1.38 | 1.87 | n/a | 1.43 | 1.50 |
|  | C4 | 3.13 | 1.95 | 2.82 | 2.69 | 2.54 | 3.51 | n/a | 2.63 | 2.77 |
|  | C4a | 2.74 | 2.13 | 2.82 | 2.72 | 2.56 | 3.72 | n/a | 2.59 | 2.78 |
| Bernal Diaz | C5 | 1.72 | 1.31 | 1.87 | 1.85 | 1.74 | 2.64 | 1.67 | 1.70 | 1.83 |
|  | C2a | 2.18 | 1.85 | 2.62 | 2.38 | 2.31 | 3.62 | 2.75 | 2.27 | 2.53 |
|  | C2c | 1.64 | 1.54 | 1.90 | 2.00 | 1.87 | 2.82 | 3.14 | 1.79 | 2.13 |
|  | C4 | 2.59 | 1.87 | 2.67 | 2.46 | 2.46 | 3.51 | 3.40 | 2.41 | 2.71 |
|  | C4a | 2.28 | 2.18 | 2.79 | 2.56 | 2.59 | 3.46 | 3.60 | 2.48 | 2.78 |
| Keckley | C5 | 2.00 | 1.56 | 1.85 | 1.82 | 1.97 | 2.28 | n/a | 1.84 | 1.91 |
|  | C2a | 2.38 | 1.90 | 2.69 | 2.51 | 2.64 | 3.72 | n/a | 2.43 | 2.64 |
|  | C2c | 1.28 | 1.21 | 1.54 | 1.46 | 1.28 | 2.23 | n/a | 1.35 | 1.50 |
|  | C4 | 2.64 | 1.95 | 2.46 | 2.49 | 2.41 | 3.46 | n/a | 2.39 | 2.57 |
|  | C4a | 2.33 | 2.03 | 2.56 | 2.56 | 2.69 | 3.54 | n/a | 2.44 | 2.62 |
| Yung Wing | C5 | 2.08 | 1.62 | 1.97 | 1.90 | 1.82 | 2.36 | n/a | 1.88 | 1.96 |
|  | C2a | 2.28 | 1.95 | 2.51 | 2.26 | 2.08 | 3.31 | n/a | 2.22 | 2.40 |
|  | C2c | 2.15 | 2.00 | 2.33 | 2.21 | 2.31 | 2.97 | n/a | 2.20 | 2.33 |
|  | C4 | 2.15 | 1.82 | 2.36 | 2.18 | 2.13 | 2.90 | n/a | 2.13 | 2.26 |
|  | C4a | 2.38 | 2.13 | 2.74 | 2.38 | 2.36 | 3.18 | n/a | 2.40 | 2.53 |
| Babur | C5 | 1.79 | 1.41 | 1.79 | 2.10 | 1.69 | 2.90 | 2.53 | 1.76 | 2.03 |
|  | C2a | 1.92 | 1.49 | 2.23 | 2.21 | 1.69 | 2.87 | 3.53 | 1.91 | 2.28 |
|  | C2c | 1.23 | 1.03 | 1.23 | 1.23 | 1.13 | 1.64 | 1.14 | 1.17 | 1.23 |
|  | C4 | 2.18 | 1.59 | 2.10 | 2.26 | 2.03 | 3.36 | 3.06 | 2.03 | 2.37 |
|  | C4a | 2.13 | 1.77 | 2.18 | 2.15 | 1.82 | 3.18 | 3.47 | 2.01 | 2.39 |
| Cellini | C5 | 2.64 | 1.90 | 2.54 | 2.51 | 2.31 | 3.46 | n/a | 2.38 | 2.56 |
|  | C2a | 2.31 | 2.26 | 2.85 | 2.62 | 2.69 | 3.62 | n/a | 2.54 | 2.72 |
|  | C2c | 1.79 | 1.59 | 1.90 | 2.00 | 1.79 | 2.59 | n/a | 1.82 | 1.94 |
|  | C4 | 2.44 | 2.03 | 2.74 | 2.51 | 2.38 | 3.56 | n/a | 2.42 | 2.61 |
|  | C4a | 2.56 | 2.28 | 2.69 | 2.56 | 2.54 | 4.13 | n/a | 2.53 | 2.79 |
| Zitkala-Sa | C5 | 2.62 | 1.85 | 2.46 | 2.38 | 2.38 | 3.90 | n/a | 2.34 | 2.60 |
|  | C2a | 2.15 | 1.64 | 2.21 | 2.05 | 2.10 | 3.00 | n/a | 2.03 | 2.19 |
|  | C2c | 1.82 | 1.36 | 1.87 | 1.69 | 1.56 | 2.23 | n/a | 1.66 | 1.76 |
|  | C4 | 2.41 | 1.72 | 2.31 | 2.08 | 2.00 | 3.28 | n/a | 2.10 | 2.30 |
|  | C4a | 2.00 | 1.74 | 2.26 | 2.10 | 2.00 | 3.49 | n/a | 2.02 | 2.26 |
| Rousseau | C5 | 2.59 | 1.85 | 2.62 | 2.64 | 2.49 | 3.72 | n/a | 2.44 | 2.65 |
|  | C2a | 2.77 | 2.23 | 3.00 | 2.95 | 3.10 | 4.05 | n/a | 2.81 | 3.02 |
|  | C2c | 1.74 | 1.59 | 2.44 | 1.90 | 1.90 | 3.28 | n/a | 1.91 | 2.14 |
|  | C4 | 2.44 | 1.90 | 2.59 | 2.36 | 2.33 | 3.46 | n/a | 2.32 | 2.51 |
|  | C4a | 2.72 | 2.03 | 2.64 | 2.49 | 2.79 | 3.74 | n/a | 2.53 | 2.74 |
| Augustine | C5 | 3.00 | 1.95 | 2.64 | 2.69 | 2.64 | 3.79 | 2.90 | 2.58 | 2.80 |
|  | C2a | 2.62 | 1.85 | 2.72 | 2.69 | 2.51 | 4.08 | 4.36 | 2.48 | 2.97 |
|  | C2c | 2.10 | 1.64 | 2.21 | 2.41 | 2.21 | 3.90 | 3.33 | 2.11 | 2.54 |
|  | C4 | 2.77 | 2.08 | 2.62 | 2.85 | 2.49 | 4.18 | 4.67 | 2.56 | 3.09 |
|  | C4a | 2.72 | 2.10 | 2.79 | 2.97 | 2.90 | 4.56 | 4.50 | 2.70 | 3.22 |
| Equiano | C5 | 2.92 | 2.28 | 2.95 | 2.97 | 2.72 | 3.74 | n/a | 2.77 | 2.93 |
|  | C2a | 2.44 | 1.97 | 2.77 | 2.56 | 2.54 | 3.90 | n/a | 2.46 | 2.70 |
|  | C2c | 1.92 | 1.51 | 2.36 | 2.26 | 1.82 | 3.18 | n/a | 1.97 | 2.18 |
|  | C4 | 2.62 | 2.23 | 2.67 | 2.49 | 2.15 | 3.64 | n/a | 2.43 | 2.63 |
|  | C4a | 2.51 | 2.00 | 2.67 | 2.67 | 2.26 | 3.82 | n/a | 2.42 | 2.65 |

Total cells: 14 subjects x 5 conditions x 9 columns = 630. Source: raw per-judge JSON files under `results/global_<subject>/*_judgments_<judge>.json` (global subjects) and `results/hamerton/` (Hamerton), aggregated via `scripts/_emit_full_judge_matrix.py`.

The matrix is 14 subjects x 5 conditions x (7 per-judge columns + 5-judge primary mean + 7-judge mean) = 70 rows x 9 columns = 630 cells. Subject rows follow the C5-baseline ordering used in [§4.1](#sec-4-1) (lowest baseline first). Empty Subject cells continue the previous subject's rows. Gemini Pro "n/a" entries reflect that Gemini Pro was run as a sensitivity judge only on a subset of subjects ([§4.6.2](#sec-4-6-2)); those cells were never populated. Franklin is not included in this matrix because the Franklin control condition set does not align to the C5 / C2a / C2c / C4 / C4a labels used in the global-subject run; Franklin's judgments are reported in [§4.2](#sec-4-2) and are stored under `results/franklin_legacy_20260411/analysis/`. Source: `scripts/_emit_full_judge_matrix.py`, which aggregates from `results/global_<subject>/*_judgments_<judge>.json` and `results/hamerton/`.


```{=openxml}
<w:p><w:pPr><w:sectPr><w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>
```

### D.5 Example verbatim responses at each rubric anchor {#sec-d-5}

Verbatim-response examples at rubric anchors 1-5 for one representative subject (Hamerton) are in [§3.6](#sec-3-6) as part of the rubric definition. Examples at anchor crossings are developed in [§4.1](#sec-4-1) (Examples A, B, C on Ebers, Bernal Diaz, Seacole). Three illustrative paired (C5, C4a) per-question excerpts for each of the 14 main-study subjects are collected in Appendix E. The raw response JSON files (`results/global_<subject>/results_v2.json`) contain every response verbatim alongside its 5-judge primary score.

---

## Appendix E. Selected per-subject excerpts

This appendix provides three illustrative paired (C5, C4a) cases per subject for readers wanting concrete examples of the specification's effect at the per-question grain. Cases are selected by largest C4a minus C5 panel-mean Δ within each subject, requiring both responses to be present and non-empty. Excerpts are truncated for readability; full responses are at `results/<subject>/results_v2.json` (or `results/hamerton/results.json` for Hamerton). Per-question scores are 5-judge primary means (haiku, sonnet, opus, gpt4o, gpt54).

### E.1 Hamerton (baseline C5 = 1.26) {#sec-e-1}

**Case 1: q51** (Δ_C4a = +4.00; C5 = 1.00 to C4a = 5.00; band 1 to 5)

*Question:* Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?

*Held-out passage:* I quickly resolved that as Death would probably soon separate us, and might separate us at any moment, I would keep as much as possible near my guardian during her life.

*C5 response (no context):* # Analyzing Hamerton's Choice I don't have specific information about a character named Hamerton and his guardian's situation in my training data. To give you an accurate answer, I would need to know: - **Which work** this is from (novel, story, historical account, etc. [truncated]

*C4a response (facts + spec):* # On Hamerton's Choice Between Duty and Proximity This is not a question with a clean answer, and Hamerton himself would resist the framing that forces one. The evidence is explicit: he learned his guardian had an incurable heart disease that could cause sudden death. His response was to **resolve to stay near her as much as possible**. He then **remained at Burnley for several years** to maintain that proximity. [truncated]

---

**Case 2: q55** (Δ_C4a = +4.00; C5 = 1.00 to C4a = 5.00; band 1 to 5)

*Question:* Would Hamerton eventually master swimming after his humiliating Doncaster failure?

*Held-out passage:* I afterwards became an accomplished swimmer, and could do various tricks in the water, such as reading aloud from a book held in both hands, or swimming in clothes and heavy boots.

*C5 response (no context):* I don't have any information about Hamerton or a swimming incident in Doncaster in my training data. To give you an accurate answer, I would need more context about: - Who Hamerton is (full name, time period, profession) - What the Doncaster incident involved - What sources you're referring to Could you provide more details about this person or event? That way I can either help you find the answer or let you know if it's something I'm not familiar with.

*C4a response (facts + spec):* # On Hamerton's Swimming Yes - and the path to that mastery reveals something essential about how he operates. The near-drowning at Doncaster was not a temporary setback he moved past. It was a structural wound: he had lied about his ability, been exposed, nearly died, and felt the full weight of shame. Most people would avoid water afterward. Hamerton did the opposite. [truncated]

---

**Case 3: q42** (Δ_C4a = +3.80; C5 = 1.00 to C4a = 4.80; band 1 to 4)

*Question:* Would Hamerton develop an interest in heraldry and medieval pursuits?

*Held-out passage:* I soon learned all about heraldry, and in my leisure time drew and colored all the coats of arms that had been borne by the Hamertons... I became so much of a mediaevalist that there was considerable risk of my stopping short in the amateur practice of such arts as wood-carving, illumination, and painting on glass.

*C5 response (no context):* I don't have enough context to answer this question about Hamerton. Could you clarify: 1. **Who is Hamerton?** (A historical figure, fictional character, or someone else?) 2. **What's the source?** (A book, game, historical record, etc.) 3. **What information do you have about them** that might suggest whether they'd develop such interests? [truncated]

*C4a response (facts + spec):* # On Hamerton's Likely Interest in Heraldry and Medieval Pursuits Given the behavioral specification and known facts, **yes - Hamerton would very likely develop a sustained interest in heraldry and medieval pursuits**, though the character of that interest would be specific and revealing. ## The Convergence of Multiple Anchors **A7 - MATERIAL ATTENTION** is the primary driver here. [truncated]


### E.2 Sunity Devee (baseline C5 = 1.03) {#sec-e-2}

**Case 1: q36** (Δ_C4a = +3.60; C5 = 1.00 to C4a = 4.60; band 1 to 4)

*Question:* How does the author characterize her own interest in political matters, and what does she believe is the appropriate role for women in this domain?

*Held-out passage:* I hope I shall be forgiven if my readers do not find much about politics in this book, but I have never been interested in politics, and I think it is better for women not to take part in political work.

*C5 response (no context):* I'd be happy to help answer this question, but I need more context. You're asking about a specific author's views on women and politics, but you haven't indicated which author or text you're referring to. Could you please provide: - The author's name - The title of the work - Any additional context (time period, genre, etc. [truncated]

*C4a response (facts + spec):* # Sunity Devee's View on Women and Politics Based on the behavioral specification and known facts, Sunity Devee's characterization of her own political interest and the appropriate female role is notably **circumscribed and deferential**, operating within several distinct frameworks: ## Her Own Political Disengagement The source material contains **virtually no evidence** that Sunity Devee engages in political reasoning, analysis, or advocacy on her own account. [truncated]

---

**Case 2: q34** (Δ_C4a = +3.40; C5 = 1.00 to C4a = 4.40; band 1 to 4)

*Question:* What pattern does the author identify regarding how English people treat Indians differently depending on location?

*Held-out passage:* Yet whoever visits England once wishes to go there again, and the chief reason of this is, that the English are much nicer to Indians in England than they are in India.

*C5 response (no context):* # Pattern of Location-Based Treatment I don't have access to the specific text you're referring to. To accurately answer your question about how an author describes English treatment of Indians varying by location, I would need you to provide: 1. **The author's name** 2. **The title of the work** 3. **The relevant passage or chapter** Could you share these details? [truncated]

*C4a response (facts + spec):* # Pattern of Location-Based Treatment of Indians Based on the behavioral specification and known facts, the author identifies a **stark contrast in how English people treat Indians depending on whether they are in India or England**: ## In India (Colonial Context) - English officials exercise **hierarchical authority and control** over Indian rulers and subjects - The relationship is framed through **governance, administration, and institutional power** - Indians are positioned as subjects requi... [truncated]

---

**Case 3: q22** (Δ_C4a = +3.00; C5 = 1.00 to C4a = 4.00; band 1 to 4)

*Question:* Given the author's character as described in the training text, what emotional control would she likely demonstrate during a spouse's final days?

*Held-out passage:* It was very hard always to wear a smile when all I longed to do was to fall on the floor and weep, but I had to look cheerful and talk brightly.

*C5 response (no context):* I don't have access to any training text or previous context about a specific author or character you're referring to. To answer your question about how someone might demonstrate emotional control during a spouse's final days, I would need: 1. **The author's name** you're asking about 2. **The specific text or work** you're referencing 3. [truncated]

*C4a response (facts + spec):* # Emotional Control During a Spouse's Final Days Based on the behavioral specification, Sunity Devee would likely demonstrate a particular *form* of emotional control - one that is neither suppression nor uninhibited expression, but rather a disciplined channeling of grief through relational duty and spiritual framework. [truncated]


### E.3 Ebers (baseline C5 = 1.02) {#sec-e-3}

**Case 1: q11** (Δ_C4a = +2.60; C5 = 1.00 to C4a = 3.60; band 1 to 3)

*Question:* When encountering an institution that is poorly managed, how does Ebers typically respond based on his character and values?

*Held-out passage:* I had come hither full of beautiful ideals and animated by the best intentions; but the very first day made me suspect how many obstacles I should encounter

*C5 response (no context):* I don't have specific information about how someone named Ebers typically responds to poorly managed institutions based on their character and values. To give you an accurate answer, I would need more context: - **Which Ebers are you referring to?** (There are several notable people with this surname) - **What source material are you drawing from?** (A book, historical account, case study, etc. [truncated]

*C4a response (facts + spec):* # Ebers's Response to Institutional Mismanagement Based on the behavioral specification and known facts, Ebers's response to institutional mismanagement follows a distinctive pattern shaped by his core values: ## The Primary Response: Institutional Critique Through Lived Contrast When confronted with an institution that fails to live up to its stated ideals, Ebers **instinctively tests official claims against eyewitness or embodied experience**, exposing the gap between profession and reality. [truncated]

---

**Case 2: q18** (Δ_C4a = +2.60; C5 = 1.00 to C4a = 3.60; band 1 to 3)

*Question:* How does Ebers describe his capacity for finding joy and maintaining his disposition during his school years?

*Held-out passage:* my natural cheerfulness ruled my whole nature

*C5 response (no context):* I don't have enough context to answer this question accurately. To provide information about how Ebers describes his capacity for finding joy and maintaining his disposition during school years, I would need to know: 1. Which Ebers you're referring to (there are several notable people with this surname) 2. What source material you're asking about (autobiography, biography, interview, etc. [truncated]

*C4a response (facts + spec):* # Ebers's Capacity for Joy and Disposition During School Years Based on the behavioral specification and the known facts, Ebers describes his capacity for joy during his school years through several interconnected patterns: ## The Resilience of Youth and Physical Vitality Ebers emphasizes that **young people value life less than old people** - a statement that, in his context, carries a particular meaning. [truncated]

---

**Case 3: q7** (Δ_C4a = +2.40; C5 = 1.20 to C4a = 3.60; band 1 to 3)

*Question:* How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?

*Held-out passage:* A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed.

*C5 response (no context):* # Ebers on Self-Sacrifice and Educational Success I don't have specific information about Ebers's characterization of this relationship in my training data. To give you an accurate answer, I would need to know: 1. **Which Ebers you're referring to** - there are several notable figures with this surname in educational contexts 2. **The specific work or text** where this idea appears 3. [truncated]

*C4a response (facts + spec):* # On Self-Sacrifice and Educational Success Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as **foundational and inseparable** - not instrumental, but constitutive. Self-sacrifice is not a means to institutional success; it is the evidence that success is genuine. ## The Operative Logic Ebers witnessed this directly at Keilhau. Froebel, Langethal, and Middendorf did not sacrifice themselves *in order to* build a successful school. [truncated]


### E.4 Fukuzawa (baseline C5 = 1.67) {#sec-e-4}

**Case 1: q20** (Δ_C4a = +3.40; C5 = 1.00 to C4a = 4.40; band 1 to 4)

*Question:* Would Fukuzawa's willingness to engage in combat training contradict his broader philosophical opposition to weapons?

*Held-out passage:* As I had practised the art of iai, I knew how to handle my sword.

*C5 response (no context):* # A Genuine Tension This does depend on how we interpret Fukuzawa Yukichi's actual positions, but there's a real philosophical question here: ## The Potential Contradiction If Fukuzawa opposed weapons on principle, combat training *could* seem inconsistent - it develops martial capability even without relying on specific weapons. ## Possible Reconciliations **Practical vs. [truncated]

*C4a response (facts + spec):* # On Fukuzawa's Relationship with Combat Training and Weapons This is a genuine tension in the source material, but not a contradiction - it reveals something important about how his principles actually operate. ## The Evidence of Training Fukuzawa explicitly states he "had learned iaijutsu, the art of drawing the long sword in an emergency" and "frequently practiced iaijutsu at home and at school in Osaka." This was deliberate, sustained training in lethal technique. [truncated]

---

**Case 2: q1** (Δ_C4a = +3.20; C5 = 1.20 to C4a = 4.40; band 1 to 4)

*Question:* When faced with a direct order from his organization that conflicts with his personal judgment about safety, how would this person likely respond?

*Held-out passage:* I said that it was too dangerous for the young men to go to war; they might be killed by stray bullets however carefully they went about in the battlefield. For this kind of war, if they wanted figureheads in their ranks, they could as well hire farmers from the provinces. My students were too precious; even if they were not to be hit by the bullets, they might hurt their feet on thorns. So I had them answer that they were all too ill to carry arms.

*C5 response (no context):* I don't have enough information to answer this question accurately. To assess how someone would respond to a conflict between organizational orders and personal safety judgment, I'd need to know: - **Their role and authority level** (entry-level vs. leadership affects options) - **The specific safety concern** (severity matters greatly) - **Their past behavior patterns** (have they challenged orders before?) - **Organizational culture** (does it reward or punish dissent? [truncated]

*C4a response (facts + spec):* # Response to Conflicting Direct Orders Based on the behavioral specification, this person would likely respond through **strategic non-compliance wrapped in surface deference** - a pattern that appears repeatedly across the source material. ## The Operating Pattern **Surface layer:** Apparent compliance, politeness, no visible resistance. **Interior layer:** Private judgment preserved; the order is not actually followed, or is followed in a way that neutralizes its intent. [truncated]

---

**Case 3: q3** (Δ_C4a = +3.20; C5 = 1.00 to C4a = 4.20; band 1 to 4)

*Question:* How does this person conceptualize the relationship between an individual and their employer or patron organization?

*Held-out passage:* All the intercourse of life is governed by the rule of give and take. If the clan says, 'You should be grateful for the patronage given your family for many generations,' I shall have a word to say in reply: 'There is no occasion for you to demand gratitude, for my family has rendered honest service for a long time.'

*C5 response (no context):* I don't have any text, image, or context provided that would allow me to identify a specific person and analyze their views on employer-employee relationships. Could you please provide: - The person's name or relevant quote/text - An image or document they created - A link to their work - Or any other context about whose perspective you're asking about Once you share that information, I'd be happy to analyze how they conceptualize individual-employer relationships.

*C4a response (facts + spec):* # Conceptualization of Individual-Employer/Patron Relationships Based on the behavioral specification and biographical facts, this person maintains a **fundamentally instrumental and conditional** view of employment relationships - one that is notably at odds with the feudal loyalty structures that surrounded him. ## Core Operating Principle The relationship is **transactional and revocable**, not binding or transcendent. [truncated]


### E.5 Seacole (baseline C5 = 1.77) {#sec-e-5}

**Case 1: q11** (Δ_C4a = +3.40; C5 = 1.00 to C4a = 4.40; band 1 to 4)

*Question:* Based on Mary's established pattern of medical practice, how would she likely respond if soldiers were reluctant to use official medical facilities?

*Held-out passage:* In the first place, the men (I am speaking of the "ranks" now) had a very serious objection to going into hospital for any but urgent reasons, and the regimental doctors were rather fond of sending them there; and, in the second place, they could and did get at my store sick-comforts and nourishing food, which the heads of the medical staff would sometimes find it difficult to procure.

*C5 response (no context):* I don't have enough context to answer this question accurately. You're referring to "Mary's established pattern of medical practice," but I don't know which Mary you mean. This could refer to: - **Mary Seacole** (1805-1881) - who famously went to the Crimean War and treated soldiers in the field - **Florence Nightingale** (1820-1910) - who revolutionized hospital care - **Mary Walker** (1832-1919) - a Civil War surgeon - Another historical or contemporary figure named Mary Could you clarify: 1. [truncated]

*C4a response (facts + spec):* # Mary's Response to Soldiers Avoiding Official Medical Facilities Given her established patterns, Mary would likely respond with **pragmatic acceptance followed by direct intervention** - not by insisting soldiers use official channels. ## Why She Wouldn't Push Official Routes **A5 (Institutional Skepticism)** is active here. [truncated]

---

**Case 2: q2** (Δ_C4a = +3.20; C5 = 1.80 to C4a = 5.00; band 1 to 5)

*Question:* How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?

*Held-out passage:* Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour

*C5 response (no context):* # Mary Seacole and Delirious Patients I don't have specific documented instances of how Mary Seacole responded when delirious patients mistook her for family members. While her memoir *Wonderful Adventures of Mrs. Seacole in Many Lands* (1857) describes her nursing work during the Crimean War and her compassionate care for soldiers, I cannot point to a particular passage that details her response to this specific situation. [truncated]

*C4a response (facts + spec):* # Response Pattern: Mistaken Identity with Delirious Patients Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern: ## Primary Response: Compassionate Acceptance She would **not correct the patient** in the moment. Instead, she would: 1. **Lean into the mistaken identity** - allowing the patient to believe she is their mother, sister, or wife if that belief brings comfort 2. [truncated]

---

**Case 3: q19** (Δ_C4a = +3.00; C5 = 1.40 to C4a = 4.40; band 1 to 4)

*Question:* What practical advantages would Mary's established store provide to soldiers seeking her care?

*Held-out passage:* they could and did get at my store sick-comforts and nourishing food, which the heads of the medical staff would sometimes find it difficult to procure.

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about "Mary's established store" and soldiers seeking her care, but I'm missing important details about: - **Which Mary** you're referring to - **What time period** this involves - **What conflict or war** is relevant - **What kind of store** it was Could you provide more context? For example, are you asking about: - Mary Seacole (Crimean War)? - Mary Walker (American Civil War)? [truncated]

*C4a response (facts + spec):* # Practical Advantages of Mary's Store for Soldiers Seeking Care ## Immediate Access to Supplies The store functioned as a **material extension of her medical practice**. Soldiers could obtain: - **Medicines and remedies** she had invested heavily in - not theoretical knowledge but actual compounds (calomel, mercury preparations, mustard plasters, cinnamon water) ready to hand - **Comforts unavailable through official channels** - preserved foods, eggs, vegetables, home remedies that addressed b... [truncated]


### E.6 Bernal Diaz (baseline C5 = 1.70) {#sec-e-6}

**Case 1: q1** (Δ_C4a = +2.60; C5 = 1.00 to C4a = 3.60; band 1 to 3)

*Question:* Based on Diaz's character as shown in the training text, how would he likely respond to receiving valuable gifts from a ruler he has not yet met?

*Held-out passage:* all of which our general received with a friendly smile.

*C5 response (no context):* I don't have access to any training text about a character named Diaz. To answer your question accurately, I would need you to either: 1. Share the relevant text or passage that describes Diaz's character 2. Provide context about which work (book, film, game, etc.) this character appears in 3. [truncated]

*C4a response (facts + spec):* # Diaz's Response to Valuable Gifts from an Unknown Ruler Based on the behavioral specification and documented facts, Diaz would respond through a carefully layered framework: ## Immediate Response: Acceptance with Gratitude He would accept the gifts graciously and publicly - this is non-negotiable. The gifts themselves function as **proof of legitimacy** (A6: GOLD AS PROOF). Refusing them would signal weakness or suspicion, both of which undermine his position. [truncated]

---

**Case 2: q35** (Δ_C4a = +2.00; C5 = 1.40 to C4a = 3.40; band 1 to 3)

*Question:* How would the author characterize the consequences when messengers witness disrespectful treatment of a monarch and report it back to that ruler?

*Held-out passage:* Both these Mexicans had understood the reviling language used by Cortes against their monarch, and also how our other officers had remonstrated with him on that account. They knew these officers well; for they had by turns been captains of the guard which was placed over their monarch's person, and knew they were greatly attached to him. [truncated]

*C5 response (no context):* # Characterizing Consequences of Reported Disrespect to a Monarch I don't have access to the specific text you're referring to. To answer your question accurately, I would need to know: 1. **Which author and work** you're asking about 2. **The specific passage or context** discussing messengers and monarchs However, I can note that in many classical and historical texts, such scenarios typically involve: - **Severe consequences** for the disrespectful party (punishment, execution, loss of favor)... [truncated]

*C4a response (facts + spec):* # On Messengers Witnessing Disrespect to Authority Based on the behavioral specification and known facts, the author would characterize such consequences as **catastrophic and irreversible in their political effects**. ## The Core Logic The author operates from **A4 - LOYALTY ARCHITECTURE**: personal loyalty and demonstrated fidelity are the load-bearing structures of all legitimate authority. [truncated]

---

**Case 3: q9** (Δ_C4a = +1.80; C5 = 1.00 to C4a = 2.80; band 1 to 2)

*Question:* How would Diaz respond emotionally to the safe return of officers he had been concerned about?

*Held-out passage:* For the rest, we were not a little delighted when they reappeared in our quarters

*C5 response (no context):* I'd be happy to help, but I need more context to give you an accurate answer. "Diaz" could refer to several characters across different shows, movies, or books. Are you asking about: - **Rosa Diaz** from Brooklyn Nine-Nine? - **A character from another TV show or film?** - **A specific episode or storyline?** Once you clarify which Diaz you're referring to and the context, I can describe how that character would likely respond emotionally to officers returning safely.

*C4a response (facts + spec):* # Emotional Response to Safe Return of Concerned Officers Based on the behavioral specification, Diaz would respond with **visible, collective relief that immediately reorganizes into operational focus** - not private sentiment but shared vindication. ## The Immediate Response He would likely: **Express gratitude publicly and theatrically** - not as mere politeness but as **identity confirmation**. [truncated]


### E.7 Keckley (baseline C5 = 1.84) {#sec-e-7}

**Case 1: q9** (Δ_C4a = +3.00; C5 = 1.20 to C4a = 4.20; band 1 to 4)

*Question:* When someone under her care shows signs of extreme emotional distress, what would be Keckley's likely course of action?

*Held-out passage:* I bathed Mrs. Lincoln's head with cold water, and soothed the terrible tornado as best I could.

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about "Keckley's" likely response to someone in emotional distress, but I would need to know: 1. **Who Keckley is** - Are you referring to Elizabeth Keckley, the historical figure and seamstress? A character from a book, film, or show? Someone else? 2. **What "under her care" means** - Is this a professional context (caregiver, teacher, therapist), a personal relationship, or something else? 3. [truncated]

*C4a response (facts + spec):* # KECKLEY'S RESPONSE TO EXTREME EMOTIONAL DISTRESS Based on the behavioral specification and known facts, her course of action would follow this sequence: ## IMMEDIATE RESPONSE: PHYSICAL PRESENCE & PRACTICAL CARE She would **move toward the person physically** rather than offer words first. The specification notes that "abstract sympathy, theoretical solidarity, and rhetorical compassion are treated as lesser currencies than presence, practical action, and direct testimony. [truncated]

---

**Case 2: q16** (Δ_C4a = +2.00; C5 = 1.00 to C4a = 3.00; band 1 to 3)

*Question:* When Elizabeth cares for young people in her charge, what level of emotional attachment does she develop toward them?

*Held-out passage:* I could not have loved her more tenderly had she been the sister of my unfortunate boy.

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about "Elizabeth," but there are many people with that name in literature, history, and real life. Could you provide more details, such as: - Which Elizabeth you're referring to (a character from a book/film, a historical figure, etc.) - What work or context this is from - Who the "young people in her charge" are With that information, I'd be happy to help answer your question about her emotional attachment.

*C4a response (facts + spec):* # EMOTIONAL ATTACHMENT IN CAREGIVING Based on the behavioral specification and known facts, Elizabeth's emotional attachment to those in her care operates at a **profound and permanent level**, structured by specific conditions: ## The Pattern **Immediate and Constitutive** When Elizabeth assumes caregiving responsibility - particularly for children - the attachment is not gradual or conditional. It is immediate and becomes part of her identity. Her first duty as a child was caring for Col. [truncated]

---

**Case 3: q24** (Δ_C4a = +2.00; C5 = 1.00 to C4a = 3.00; band 1 to 3)

*Question:* How does Keckley typically respond when she realizes someone she cares for has suffered due to her own oversight?

*Held-out passage:* "Come, Elizabeth, get up, I know you must be hungry. Dress yourself quickly and we will go out and get some breakfast. I was unable to sleep last night for thinking of you being forced to go to bed without anything to eat."

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about how "Keckley" responds to a specific situation, but I'm not certain which Keckley you're referring to or what source material this comes from. Are you asking about: - **Elizabeth Keckley**, the historical figure and author of "Behind the Scenes"? - A character from a novel, play, or other work? - Someone from a specific text you're reading? [truncated]

*C4a response (facts + spec):* # Response Pattern: Keckley's Reaction to Personal Oversight Causing Harm Based on the behavioral specification and known facts, Keckley's response to realizing she has caused suffering through oversight follows a distinctive pattern: ## The Immediate Emotional Register When she becomes aware that her inattention has harmed someone she cares for, the response is **visceral and embodied** rather than abstract. She does not intellectualize the mistake; she *feels* it physically. [truncated]


### E.8 Yung Wing (baseline C5 = 1.88) {#sec-e-8}

**Case 1: q22** (Δ_C4a = +3.20; C5 = 1.00 to C4a = 4.20; band 1 to 4)

*Question:* When Yung Wing receives a position that appears to be a sinecure with modest compensation, what action does he take?

*Held-out passage:* after three months' stay in Nanking under Viceroy Liu Kwan Yih, out of regard for official etiquette, I resigned the secretaryship, which was practically a sinecure--paying about $150 a month.

*C5 response (no context):* I don't have enough context to answer this question accurately. To provide a reliable answer about Yung Wing's actions regarding a sinecure position, I would need to know: 1. Which specific position you're referring to 2. What source material this comes from (a biography, historical account, etc.) 3. The time period in question Yung Wing (1828-1912) was a notable Chinese-American diplomat and educator who had a long career with various positions. [truncated]

*C4a response (facts + spec):* # Analysis: Yung Wing's Response to Sinecure Positions Based on the behavioral specification and known facts, when Yung Wing encounters a position that is comfortable but lacks substantive challenge or advancement potential, he **refuses it and seeks something more demanding**. ## The Pattern in Action **The Imperial Customs Translating Department (1856)** This is the clearest example: - **The position**: Salary of Tls. [truncated]

---

**Case 2: q26** (Δ_C4a = +2.60; C5 = 1.00 to C4a = 3.60; band 1 to 3)

*Question:* When Yung Wing senses that a superior official no longer values his services, what does he do?

*Held-out passage:* This I took to be a pretty broad hint that he did not need my services any longer, that I was not the man to suit his purposes; and as I had no axe to grind, I did not make any attempt to run after my grind-stone.

*C5 response (no context):* I don't have enough context to answer this question accurately. To provide a reliable answer about Yung Wing's actions when sensing a superior official no longer values his services, I would need to know: 1. Which specific work or source material you're referring to (autobiography, historical account, biography, etc.) 2. [truncated]

*C4a response (facts + spec):* # Yung Wing's Response to Diminished Official Value Based on the behavioral specification and known facts, when Yung Wing senses that a superior official no longer values his services, he **withdraws from the position entirely rather than remaining in a diminished capacity**. [truncated]

---

**Case 3: q5** (Δ_C4a = +2.00; C5 = 1.00 to C4a = 3.00; band 1 to 3)

*Question:* How does Yung Wing approach explaining complex technical concepts to non-specialists?

*Held-out passage:* In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery. A machine shop consisting of lathes of different kinds and sizes, planers and drills would be able to turn out machinery for making guns, engines, agricultural implements, clocks, etc.

*C5 response (no context):* # Yung Wing's Approach to Technical Communication I don't have specific documented information about Yung Wing's particular methods for explaining technical concepts to non-specialists. To give you an accurate answer, I'd need to know: - **Which Yung Wing** you're referring to (there are several notable people with this name) - **What context** you're asking about (academic writing, public speaking, teaching, etc. [truncated]

*C4a response (facts + spec):* # Yung Wing's Approach to Technical Communication Based on the behavioral specification and known facts, Yung Wing's approach to technical explanation is shaped by several core commitments: ## **Translation as Primary Method** Yung Wing does not simplify technical concepts downward; he *translates* them across frameworks. [truncated]


### E.9 Babur (baseline C5 = 1.76) {#sec-e-9}

**Case 1: q24** (Δ_C4a = +2.20; C5 = 1.40 to C4a = 3.60; band 1 to 3)

*Question:* Given the military campaigns and strategic decisions documented in the training text, what would you expect about Babur's approach to organizing defensive military equipment?

*Held-out passage:* those chained together as a defence and probably also those conveying the culverins.

*C5 response (no context):* # Babur's Approach to Defensive Military Equipment Based on historical patterns from Babur's campaigns, I would expect: ## Pragmatic Adaptation - **Integration of captured resources**: Babur systematically incorporated enemy weapons and fortifications into his own arsenal rather than discarding them - **Flexible standards**: He likely prioritized functional effectiveness over uniformity, using whatever defensive equipment proved reliable ## Emphasis on Fortification Strategy - **Strategic positi... [truncated]

*C4a response (facts + spec):* # Babur's Approach to Defensive Military Equipment Based on the documented record, I would expect Babur to organize defensive equipment with these characteristics: ## Systematic Integration with Tactical Formation Babur treats defensive equipment not as supplementary but as **integral to battle architecture**. [truncated]

---

**Case 2: q37** (Δ_C4a = +1.40; C5 = 1.00 to C4a = 2.40; band 1 to 2)

*Question:* Based on patterns in the training text, how does Babur typically handle negotiations with rival tribal or regional leaders?

*Held-out passage:* Bābur negociates with him 594; his house the scene of a supreme rite 595

*C5 response (no context):* I don't have access to any training text about Babur to analyze patterns in his negotiation strategies. To answer your question accurately, I would need you to either: 1. **Share the specific text** you're referring to, or 2. **Clarify the source** (is this from a history book, primary document, course material, etc.? [truncated]

*C4a response (facts + spec):* # Babur's Negotiation Patterns with Rival Leaders Based on the behavioral specification and documented facts, Babur employs a sophisticated multi-layered approach: ## Initial Positioning: Strength + Civility Babur typically **opens negotiations from a position of demonstrated military strength** while extending formal courtesy. When approaching Medinī Rāo at Chandīrī, he sent Ārāīsh Khān "with favour and kindness" while simultaneously maintaining siege positions. [truncated]

---

**Case 3: q13** (Δ_C4a = +1.20; C5 = 1.40 to C4a = 2.60; band 1 to 2)

*Question:* Based on Babur's documented patterns of territorial loss and recovery in the training text, how would he characterize a situation where he simultaneously lost multiple strategic holdings?

*Held-out passage:* Having lost Samarkand and Andijān, Bābur is hospitably entertained by the

*C5 response (no context):* I don't have access to a "training text" about Babur that you're referring to. To answer your question accurately, I would need you to either: 1. **Share the specific text** you're referencing 2. **Provide the relevant passages** about Babur's territorial losses and recoveries 3. [truncated]

*C4a response (facts + spec):* # Babur's Characterization of Simultaneous Strategic Loss Based on the documented patterns in his record, Babur would characterize such a situation through several interlocking frameworks: ## As Divine Instrumentality with Human Accountability He would not treat the losses as mere misfortune. [truncated]


### E.10 Augustine (baseline C5 = 2.58) {#sec-e-10}

**Case 1: q20** (Δ_C4a = +2.40; C5 = 1.00 to C4a = 3.40; band 1 to 3)

*Question:* When recalling joyful moments from morally questionable sources, what is the author's evaluative response?

*Held-out passage:* For even from foul things have I been immersed in a sort of joy; which now recalling, I detest and execrate

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about "the author's evaluative response," but you haven't specified: 1. **Which author** you're referring to 2. **Which text or work** contains this discussion 3. **What specific "morally questionable sources"** are being discussed Could you provide: - The title of the work or passage? - The author's name? - More context about what you're reading? [truncated]

*C4a response (facts + spec):* # Augustine's Evaluative Response to Joy from Morally Questionable Sources When Augustine recalls joyful moments derived from ethically compromised sources, his response follows a consistent pattern: **he does not deny the joy's reality, but he interrogates its source and judges it as a dangerous form of false satisfaction that obscures what genuine joy requires.** ## The Pattern of His Evaluation **Acknowledgment without endorsement:** Augustine recognizes that he *did* experience pleasure - in... [truncated]

---

**Case 2: q14** (Δ_C4a = +2.00; C5 = 1.00 to C4a = 3.00; band 1 to 3)

*Question:* When the author recalls past experiences of joy, what emotional conflict does he experience?

*Held-out passage:* nor did I ever with bodily sense see, hear, smell, taste, or touch my joy; but I experienced it in my mind, when I rejoiced; and the knowledge of it clave to my memory, so that I can recall it with disgust sometimes, at others with longing

*C5 response (no context):* I don't have enough context to answer your question accurately. You're asking about a specific author's emotional experience when recalling joyful memories, but you haven't provided: 1. **Which author** you're referring to 2. **Which work** (book, essay, poem, etc.) contains this reflection 3. [truncated]

*C4a response (facts + spec):* # The Conflict Between Joy and Its Transience When Augustine recalls past experiences of joy, he experiences a profound emotional conflict rooted in his conviction that all finite goods point beyond themselves - and that clinging to them as if they were permanent is a form of spiritual death. [truncated]

---

**Case 3: q16** (Δ_C4a = +1.80; C5 = 1.00 to C4a = 2.80; band 1 to 2)

*Question:* How does the author respond when confronted with the paradox of seeking something he may have already possessed?

*Held-out passage:* How then do I seek a happy life, seeing I have it not, until I can say, where I ought to say it, 'It is enough'?

*C5 response (no context):* I don't have enough context to answer your question accurately. You're asking about a specific author's response to a paradox about possessing something, but you haven't indicated: 1. **Which author** you're referring to 2. **Which work** contains this passage or idea 3. **What specific text** demonstrates this response Could you provide: - The author's name - The title of the work - A passage or more context about the paradox you're describing? [truncated]

*C4a response (facts + spec):* # The Paradox of Seeking What One Already Possesses This person does not resolve the paradox prematurely. Instead, they sit inside it - holding both the conviction that they already possess something (through grace, through God's prior claim on them) and the urgent necessity of seeking it as though it were entirely absent. ## The Structure of the Paradox The tension appears most clearly in their account of conversion itself. [truncated]


### E.11 Cellini (baseline C5 = 2.38) {#sec-e-11}

**Case 1: q34** (Δ_C4a = +2.60; C5 = 1.00 to C4a = 3.60; band 1 to 3)

*Question:* When Cellini achieves a technical success that he had claimed was impossible, what does he attribute this accomplishment to?

*Held-out passage:* In my great astonishment I seemed to see in this the hand of God arranging and controlling all.

*C5 response (no context):* I don't have enough context to answer this question accurately. You're asking about Cellini, who is likely Benvenuto Cellini, the famous Renaissance sculptor and goldsmith, but I would need to know which specific technical achievement you're referring to. Cellini wrote an autobiography where he describes various accomplishments. Could you provide more details about: - Which specific technical feat you're asking about? - Whether this is from his autobiography or another source? [truncated]

*C4a response (facts + spec):* # Cellini's Attribution of Technical Success Based on the behavioral specification and known facts, when Cellini achieves a technical success that he had claimed was impossible, he attributes this accomplishment to **God's grace combined with his own industry and skill**. [truncated]

---

**Case 2: q33** (Δ_C4a = +1.40; C5 = 1.00 to C4a = 2.40; band 1 to 2)

*Question:* How does Cellini handle situations where he has made a prediction to a patron that turns out to be partially wrong?

*Held-out passage:* However, when I reached the end, it appeared that the toes and a little piece above them were unfinished, so that about half the foot was wanting. Although I knew that this would add a trifle to my labour, I was very well pleased, because I could now prove to the Duke how well I understood my business.

*C5 response (no context):* I don't have specific information about how Cellini handled situations where his predictions to patrons proved partially wrong. Are you referring to Benvenuto Cellini, the Renaissance sculptor and goldsmith? If so, I'm not aware of well-documented instances in his autobiography or historical records where he explicitly addressed making inaccurate predictions to his patrons. Could you provide more context about: - Which Cellini you're asking about? [truncated]

*C4a response (facts + spec):* # Cellini's Handling of Partial Prediction Failures Based on the behavioral specification and known facts, Cellini would handle this situation through a characteristic sequence of moves: ## Initial Response: Reframe Through Craft Mastery When a prediction proves partially wrong, Cellini does not apologize for the prediction itself - he redirects attention to the **technical execution and his demonstrated skill**. [truncated]

---

**Case 3: q5** (Δ_C4a = +1.20; C5 = 1.00 to C4a = 2.20; band 1 to 2)

*Question:* How does Cellini handle being used for someone else's emotional or psychological needs?

*Held-out passage:* At times the poor man detained me for four or five stricken hours without ever letting me cease talking. He used to keep me at his table, eating opposite to him, and never stopped chatting and making me chat; but during those discourses I contrived to make a good meal. He, poor man, could neither eat nor sleep; so that at last he wore me out.

*C5 response (no context):* I'd need more context to answer well. Are you asking about: 1. **Benvenuto Cellini the Renaissance artist** - how he responded to patrons' demands or emotional expectations in his work? 2. **A character named Cellini** from a book, film, or show? 3. **A modern service or app** called Cellini? 4. [truncated]

*C4a response (facts + spec):* # Cellini's Response to Being Used for Others' Emotional Needs Based on the behavioral specification and known facts, Cellini handles this situation with a characteristic mixture of **instrumental pragmatism and underlying resentment** - but the response depends entirely on whether the person using him has earned the right through prior obligation. [truncated]


### E.12 Equiano (baseline C5 = 2.77) {#sec-e-12}

**Case 1: q36** (Δ_C4a = +2.20; C5 = 2.20 to C4a = 4.40; band 2 to 4)

*Question:* How does Equiano treat those in subordinate positions to him?

*Held-out passage:* All my poor countrymen, the slaves, when they heard of my leaving them, were very sorry, as I had always treated them with care and affection, and did every thing I could to comfort the poor creatures, and render their condition easy.

*C5 response (no context):* # Equiano's Treatment of Subordinates I'd need more context to give you a precise answer, as this depends on which Equiano you're referring to and which specific situations you're asking about. If you're asking about **Olaudah Equiano** (the 18th-century African writer and abolitionist), his autobiography provides some relevant insights: - **As a former enslaved person**: Equiano was acutely aware of power dynamics and the brutality of subordination, which shaped his moral perspective - **In his... [truncated]

*C4a response (facts + spec):* # Equiano's Treatment of Those in Subordinate Positions Based on the behavioral specification and known facts, Equiano demonstrates a consistent pattern of treating subordinates with dignity and fairness that stands in sharp contrast to the brutality he witnesses throughout the West Indies. ## Active Principles His treatment flows directly from **A5 (Dignity Floor)** - the irreducible premise that every human being possesses inherent worth that no legal status can negate. [truncated]

---

**Case 2: q8** (Δ_C4a = +1.80; C5 = 1.40 to C4a = 3.20; band 1 to 3)

*Question:* How does Equiano respond when he discovers he has been given worthless currency in a business deal?

*Held-out passage:* Some of them, however, were copper, and of consequence of no value; but he took advantage of my being a negro man, and obliged me to put up with those or none, although I objected to them.

*C5 response (no context):* I don't have enough context to answer this question accurately. To provide a reliable response, I would need to know: 1. **Which work or source** you're referring to - are you asking about Olaudah Equiano's autobiography "The Interesting Narrative of the Life of Olaudah Equiano"? 2. **Which specific incident** - Equiano's narrative contains multiple business dealings and transactions throughout his life as an enslaved person and later as a free merchant. [truncated]

*C4a response (facts + spec):* # Response to Worthless Currency Based on the behavioral specification and known facts, I cannot find a documented instance where Equiano discovered he had been given worthless currency in a business deal. However, I can infer how he would likely respond based on his established patterns: ## Predicted Response **Witness and Documentation** Equiano would render a precise, unflinching account of what happened - naming the person who defrauded him, the exact circumstances, the sequence of events. [truncated]

---

**Case 3: q17** (Δ_C4a = +0.40; C5 = 1.20 to C4a = 1.60; band 1 to 1)

*Question:* When practical problems arise during recovery from crisis, how would Equiano approach solving them with available resources?

*Held-out passage:* The punt then went on shore, and we cut down some trees; and having found our mast and mended it we brought it on board, and fixed it up.

*C5 response (no context):* # Equiano's Practical Problem-Solving Approach Based on his narrative, Equiano would likely employ these strategies: ## Resourcefulness from Experience - **Leverage existing skills**: He repeatedly learned trades (seamanship, navigation, commerce) and applied them across different contexts - **Adapt rather than abandon**: When enslaved, he found ways to trade and earn money within severe constraints - suggesting he'd maximize whatever resources existed ## Systematic Observation - **Study the sit... [truncated]

*C4a response (facts + spec):* # EQUIANO'S CRISIS PROBLEM-SOLVING APPROACH When practical problems arise during recovery from crisis, Equiano would operate from a distinctive framework that combines **forensic assessment, economic self-determination, and relational leverage**. --- ## THE CORE PATTERN **He begins with precise inventory of what he actually possesses** - not what he wishes he had, not what he's been promised, but what is materially in his hands or reliably accessible. [truncated]


### E.13 Rousseau (baseline C5 = 2.44) {#sec-e-13}

**Case 1: q2** (Δ_C4a = +2.20; C5 = 1.40 to C4a = 3.60; band 1 to 3)

*Question:* Based on Rousseau's character as described in the training text, would he be likely to pursue intellectual study in a new field when given the opportunity?

*Held-out passage:* I soon got into the track of my new occupations, and conceived a taste for them. I attached myself to the study of chemistry, and attended several courses of it

*C5 response (no context):* I don't have access to a specific training text about Rousseau's character that you're referring to. To give you an accurate answer based on that particular source, I would need you to share the relevant passage or document. That said, I can offer some general context: Rousseau's actual historical record shows he *did* pursue intellectual study across multiple fields (philosophy, music, botany, political theory), though he was also known for being somewhat restless and self-directed in his learn... [truncated]

*C4a response (facts + spec):* # Rousseau's Likely Response to New Intellectual Opportunity Based on the behavioral specification, Rousseau would likely **pursue intellectual study enthusiastically but with significant complications**. ## Strong Indicators He Would Pursue It **Introspective Universalism (A1)** drives him to treat self-directed learning as philosophical inquiry into human nature itself. His extensive self-education at Charmettes demonstrates genuine intellectual hunger. [truncated]

---

**Case 2: q1** (Δ_C4a = +1.80; C5 = 1.60 to C4a = 3.40; band 1 to 3)

*Question:* When Rousseau encounters a situation requiring him to live in multiple locations simultaneously due to financial constraints, how does he respond?

*Held-out passage:* being obliged to live in their neighborhood, a dear part of the town, in a furnished lodging, and having to pay for another lodging at the extremity of Paris, at the very top of the Rue Saint Jacques, to which, let the weather be as it would, I went almost every evening to supper.

*C5 response (no context):* # Rousseau's Response to Multiple Locations I don't have a specific documented instance of Rousseau facing this exact scenario in the historical record. However, based on what we know about his life and character, we can infer likely responses: ## Probable Approaches **Practical Solutions:** - Rousseau was resourceful and often relied on patronage and the support of wealthy friends - He might have negotiated with patrons to support one primary residence - He could have sought temporary lodging a... [truncated]

*C4a response (facts + spec):* # Rousseau's Response to Simultaneous Location Requirements Based on the behavioral specification and known facts, Rousseau would respond to such a situation with characteristic internal conflict and practical compromise: ## His Likely Response Pattern **Initial Reaction: Constraint as Moral Injury** Rousseau experiences imposed structure as a form of moral injury rather than mere inconvenience (A4 - Liberty as Condition). [truncated]

---

**Case 3: q38** (Δ_C4a = +1.80; C5 = 1.00 to C4a = 2.80; band 1 to 2)

*Question:* When someone close to him insists on accompanying him during a dangerous departure, how does Rousseau typically handle it?

*Held-out passage:* Theresa determined never more to leave me out of her sight. I made her feel the inconvenience of accompanying me at that moment, and the necessity of her remaining to take care of my effects and collect my money.

*C5 response (no context):* I don't have enough specific information about Rousseau's typical responses in this situation to give you a reliable answer. To help you better, could you clarify: 1. **Which Rousseau** are you asking about? (Jean-Jacques Rousseau the philosopher, or another historical figure?) 2. **What context** are you referring to? (A specific historical event, a literary work, a biographical account?) 3. [truncated]

*C4a response (facts + spec):* # Rousseau's Response to Insistent Companions During Dangerous Departures Based on the behavioral specification and known facts, Rousseau would likely handle this situation with characteristic internal conflict: ## His Probable Response Pattern **Initial Reaction: Emotional Vulnerability** - He would feel the weight of the person's attachment acutely, as he experiences all emotional impressions with intensity - His heart would be "intoxicated" by the gesture, given his susceptibility to tender s... [truncated]


### E.14 Zitkala-Sa (baseline C5 = 2.34) {#sec-e-14}

**Case 1: q14** (Δ_C4a = +0.80; C5 = 1.60 to C4a = 2.40; band 1 to 2)

*Question:* If placed in a situation where she must conceal strong emotions in front of others, what physical signs might betray her inner turmoil?

*Held-out passage:* I longed to ask what doom awaited the young murderer, but dared not open my lips, lest I burst forth into screams instead.

*C5 response (no context):* # Physical Signs of Concealed Emotion When someone tries to suppress strong feelings, these often leak through: **Facial micro-expressions** - Brief, involuntary expressions (0.5 seconds) before control kicks in - Tightening around the eyes or mouth - Jaw clenching **Vocal tells** - Pitch changes (often higher when anxious) - Speaking faster or slower than usual - Throat clearing or voice cracking - Pauses that seem forced **Body language** - Stiffness or reduced natural movement - Self-soothing... [truncated]

*C4a response (facts + spec):* # Physical Manifestations of Concealed Emotion Given her epistemic anchors and behavioral patterns, Zitkala-Sa's body would likely betray what her face and voice attempt to contain: ## The Precision of Restraint **Stillness as a tell.** She was "inbred to suffer in silence rather than appeal to those whose open eyes could not see her pain." This training produces a particular kind of physical control - but control itself becomes visible. [truncated]

---

**Case 2: q10** (Δ_C4a = +0.60; C5 = 3.00 to C4a = 3.60; band 3 to 3)

*Question:* Given Zitkala-Sa's reflective and introspective nature shown in the training text, what would be her likely emotional response upon returning to her family home?

*Held-out passage:* With these thoughts I reach the log cabin whither I am strongly drawn by the tie of a child to an aged mother.

*C5 response (no context):* # Zitkala-Sa's Likely Emotional Response Based on her reflective nature, her return would probably involve **complex, layered emotions**: ## Likely Responses: **Profound Ambivalence** - Joy at reunion mixed with alienation - she had been transformed by her education and experiences away - Recognition that she could never fully return to her previous self **Acute Self-Awareness** - Her introspective nature would make her acutely conscious of the *distance* between her past and present selves - Li... [truncated]

*C4a response (facts + spec):* # Zitkala-Sa's Return: Emotional Architecture Based on the behavioral specification and known facts, her return home would not be a simple homecoming. It would be a collision of contradictory truths held simultaneously - and she would experience all of them at once. [truncated]

---

**Case 3: q20** (Δ_C4a = +0.60; C5 = 1.60 to C4a = 2.20; band 1 to 2)

*Question:* Would Zitkala-Sa blend indigenous spiritual beliefs with Christian concepts when contemplating her spiritual fate?

*Held-out passage:* Will the loving Jesus grant me pardon and give my soul a soothing sleep? or will my warrior father greet me and receive me as his son? Will my spirit fly upward to a happy heaven? or shall I sink into the bottomless pit, an outcast from a God of infinite love?

*C5 response (no context):* # Zitkala-Sa's Spiritual Synthesis This is plausible based on what we know about her life, though the evidence is mixed: ## Evidence suggesting she might: - **Her education** at Carlisle Indian Industrial Training School exposed her to Christianity while she retained Dakota heritage - **Her writings** show she could hold multiple perspectives simultaneously - she critiqued assimilation while engaging with Western literary forms - **Historical context**: Many Indigenous intellectuals of her era n... [truncated]

*C4a response (facts + spec):* # ANALYSIS: ZITKALA-SA'S SPIRITUAL SYNTHESIS Based on the behavioral specification and known facts, the answer is **no - not in the way the question implies**. Zitkala-Sa does not "blend" these frameworks as a coherent synthesis. Instead, she holds them in **sustained, unresolved tension** - which is structurally different and more honest to her actual position. [truncated]

---

## Appendix F. Benchmark Scope Analysis

This appendix develops, benchmark by benchmark, the scope differences summarized in [§2.1](#sec-2-1) between prior work on memory and personalization benchmarks and what this paper measures. The load-bearing point in each case is the same: representational accuracy, operationalized as behavioral prediction on held-out reasoning situations, is not what these benchmarks evaluate. None of them is wrong on its own axis. None of them is a substitute for the test in this paper.

### F.1 LongMemEval

**Reference.** Wu et al., ICLR 2025, arXiv:2410.10813.

**Task.** Evaluate long-term memory in chat assistants across multiple sessions. Five capability dimensions: single-session memory, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.

**Scoring.** Question-answering accuracy, with held-out facts embedded across session history and queried in a later session. Answers are compared against ground-truth factual targets drawn from the same session history the system ingested.

**Training / test protocol.** Conversation history is ingested; the system is then queried with fact-recall questions whose answers are present in the ingested history. The test is whether the memory system can surface the correct facts at retrieval time.

**What it measures.** Fact recall across long context windows. A secondary axis tests whether the system correctly abstains when the answer is not in the conversation history.

**What it does not measure.** Whether the memory system's representation of a specific person captures how that person reasons. Every LongMemEval target is a fact that was literally said in the conversation; no target is a held-out behavioral pattern.

**Published range.** Memory systems reported in the 68% to 85% range depending on provider, model, and benchmark variant (cited in [§1.1](#sec-1-1) and [§2.2](#sec-2-2)). Specific numbers per system are in the papers and vendor reports.

**Relationship to this paper's test.** Orthogonal axis. Our battery targets held-out behavioral patterns that were never literally said in the training half of the corpus; every question is backward-designed to answer only from patterns, not from retrievable content. A system that ranks at the top of LongMemEval can still sit near the rubric floor on our battery, and a system that ranks low on LongMemEval (for example, Base Layer's retrieval substrate) can contribute on our battery through the specification rather than through retrieval.

### F.2 PersonaGym

**Reference.** Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416.

**Task.** Evaluate persona fidelity in conversational agents. Given a described persona, measure whether the model maintains that persona across a conversation.

**Scoring.** Persona-consistency metrics over multi-turn conversation. LLM-judge evaluation of whether the model's voice, stated preferences, and surface-level claims remain consistent with the described persona.

**Training / test protocol.** A persona is described (occupation, background, preferences, mannerisms). The model is prompted to roleplay the persona across a dialogue. Evaluation is whether the dialogue responses remain internally consistent with the persona description.

**What it measures.** Persona presentation fidelity. Can the model stay in character on the described dimensions.

**What it does not measure.** Whether the model accurately predicts how the person described by the persona would respond to novel situations. A persona-fidelity system can maintain voice without ever accurately anticipating decisions. A representationally accurate system can shift voice (for example, from formal prose to casual conversational register) while continuing to predict accurately on behavioral questions.

**Published best-number.** Top PersonaScore of 4.51 ± 0.08 on a 1-5 scale (GPT-4.5), out of 10 evaluated LLMs spanning 200 personas and 10,000 questions; bottom of the range was 3.64 ± 0.57 (Claude 3 Haiku). Notably, GPT-4.1 and LLaMA-3-8b tied on PersonaScore despite a large capability gap (Samuel et al., arXiv:2407.18416). Scoring is on persona-consistency metrics, not held-out behavioral prediction; these numbers are not directly comparable to this paper's rubric means on the 1-5 behavioral-prediction scale.

**Relationship to this paper's test.** Both measure something that is sometimes called "personalization," but the axes are different. PersonaGym is surface-presentation consistency; our battery is transfer of the subject's interpretive patterns to unseen situations. Our rubric does not credit voice-matching alone (score 2: "generic, not subject-specific"); it requires capturing the behavioral pattern the subject exhibited in the held-out passage.

### F.3 AlpsBench

**Reference.** Xiao et al., 2026, arXiv:2603.26680.

**Task.** Evaluate whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses in conversational settings.

**Scoring.** Preference-alignment scoring and emotional-resonance scoring on conversational responses, both LLM-judged against reference targets derived from user preference data.

**Training / test protocol.** A conversational agent is seeded with a user's preference history (via an explicit memory mechanism, or as a baseline without one). The agent responds to new prompts. Responses are scored on preference-alignment and emotional-resonance metrics.

**What it measures.** Whether explicit memory makes conversational responses more aligned with stated preferences and more emotionally appropriate.

**What it does not measure.** Whether memory mechanisms enable the model to predict the user's behavior in unseen reasoning situations. Preference alignment and behavioral prediction are related but distinct: a system can match preferences on immediate response choices without having a representation of the user's reasoning that transfers to situations the system has never seen.

**Central finding.** AlpsBench's central empirical result is that explicit memory mechanisms improve recall but do not guarantee more preference-aligned or emotionally resonant responses. This is independently arrived at and complementary to our own finding. They find the gap in preference alignment; we find it in behavioral prediction. Both point in the same direction: recall-solving is insufficient for what memory is ultimately for.

**Relationship to this paper's test.** Adjacent. Same motivating intuition (recall improvement does not transfer to downstream behavioral properties), different downstream property measured.

### F.4 Twin-2K

**Reference.** Toubia et al., 2025, arXiv:2505.17479.

**Task.** Behavioral prediction at scale. 2,058 participants each answered a large-scale survey, and the system predicts each participant's responses on held-out survey items given a persona constructed from their other survey answers.

**Scoring.** Distance metric on Likert-scale items (numeric distance between predicted response and actual response, aggregated per participant and per item).

**Training / test protocol.** For each participant, a subset of survey answers is used to author a persona. The persona is served to a model as context. The model predicts the participant's answer on the held-out survey items. Distance between predicted and actual response is the score.

**What it measures.** Behavioral prediction on survey-response interpolation. Does a machine-readable transcript of one half of a participant's survey predict the other half.

**What it does not measure.** Behavioral prediction on open-ended reasoning situations. Twin-2K's held-out items are additional Likert responses from the same survey form; the test is interpolation across a structured response distribution. Our held-out items are open-ended behavioral predictions on unseen autobiographical passages; scoring is via rubric on response content, not distance on a numeric scale.

**Relationship to this paper's test.** Closest prior work on the behavioral-prediction axis. Three structural differences remain load-bearing:

1. **Task format.** Twin-2K: Likert interpolation. This paper: open-ended behavioral prediction with free-text answers.
2. **Persona construction.** Twin-2K: machine-readable transcript of the participant's own prior survey responses, served as-is. This paper: an authored Behavioral Specification composed of three interpretive layers plus a composed brief. The Twin-2K persona is raw data; our specification is compressed interpretation.
3. **Held-out distance.** Twin-2K: the held-out items are drawn from the same structured survey instrument. This paper: the held-out items are drawn from autobiographical text the representation has never seen, in a different form than the training half (different chapters, different situations).

Twin-2K measures whether a model can interpolate a person's survey distribution from other survey responses. Our battery measures whether a representation of how a person reasons transfers to novel situations the representation has never seen. Both are legitimate tests of behavioral prediction; neither is a substitute for the other.

An earlier exploratory Base Layer run against Twin-2K's battery produced positive results on that task format, but we do not report those numbers as a formal benchmark comparison because the experiment used a prior iteration of our pipeline, and the task targets are substantively different (see [§2.1](#sec-2-1)).

**Published best-number.** Top individual-level accuracy of 71.72% on held-out survey items using a text-persona representation served to GPT-4.1-mini (Toubia et al., arXiv:2505.17479). Human test-retest reliability on the same instrument was 81.72%, putting the top twin at 87.67% of the human ceiling. Random-guess baseline was 59.17%. Aggregate-level replication: the Twin-2K twins reproduced results from 6 of 10 behavioral-economics experiments, with systematic divergences on medical decision-making and political attitudes. The 71.72% accuracy is on Likert interpolation, which is a structurally different task from our rubric-scored free-text behavioral prediction.

### F.5 LoCoMo

**Reference.** Maharana et al., ACL 2024, arXiv:2402.17753.

**Task.** Conversational memory quality over long multi-session dialogues.

**Scoring.** Fact-recall questions over ingested dialogue history. Similar scope to LongMemEval but focused on conversational-memory substrates specifically.

**Training / test protocol.** A long multi-session conversation is ingested; the memory system is queried on specific facts from earlier sessions.

**What it measures.** Long-dialogue recall accuracy.

**What it does not measure.** Behavioral reasoning. LoCoMo targets are literal recalls from session history.

**Published range.** LoCoMo paper baselines (Maharana et al., arXiv:2402.17753): GPT-4-turbo 32.1% overall, GPT-3.5-turbo 22.4%, GPT-3.5-turbo-16K 37.8%, best RAG configuration 41.4%; human performance 87.9%. Memory-system claims on LoCoMo, detailed in [§2.2](#sec-2-2): Mem0g variant 68.44 with GPT-4o-mini (peer-reviewed, Chhikara et al., arXiv:2504.19413); Mem0 production algorithm 91.6 self-reported with open-sourced evaluation harness; Letta 74.0 with GPT-4o-mini; earlier Zep claim of 84 publicly disputed by Mem0 (see [§2.2](#sec-2-2) dispute note). The methodology disagreement between vendors remains unresolved; [§2.2](#sec-2-2) treats these single-number comparisons with explicit caution.

**Relationship to this paper's test.** The benchmark the four memory systems (Zep, Letta, Mem0, Supermemory) compete on. [§2.2](#sec-2-2) uses these results as context for the memory-system landscape. Our paper is orthogonal: we do not evaluate memory systems on LoCoMo; we evaluate their behavioral-prediction performance on held-out autobiographical passages with and without the Behavioral Specification added.

### F.6 MemOS and related systems-level benchmarks

**Reference.** Systems-level memory benchmarking literature, including MemOS and adjacent evaluations. See [§2.2](#sec-2-2) for the memory-systems landscape.

**Task.** Evaluate memory-layer infrastructure choices (storage substrate, retrieval algorithm, consistency properties) rather than memory-quality outcomes.

**Scoring.** Varies. Typically: retrieval latency, throughput, consistency guarantees, scalability benchmarks.

**What it measures.** Infrastructure properties.

**What it does not measure.** Representational accuracy, persona fidelity, or preference alignment. Systems-level benchmarks do not evaluate the quality of the representation the memory layer produces; they evaluate the mechanics of how that representation is stored and served.

**Relationship to this paper's test.** Different layer of the stack. Our paper evaluates what gets stored and why; systems-level benchmarks evaluate how well it is stored and served. Both matter for deployed personal-AI systems. The specification and the memory-layer infrastructure compose: our [§4.4](#sec-4-4) Mem0 / Letta / Zep / Supermemory / Base Layer results show the specification adding on top of each infrastructure choice, not replacing it.

### F.7 What no prior benchmark measures

Pulling the per-benchmark analysis together, the axis that representational accuracy sits on is not covered by any prior benchmark:

1. **Test data the system has not seen.** LongMemEval, PersonaGym, and LoCoMo target content the system has ingested. Twin-2K's held-out items are drawn from the same structured instrument. Our battery's held-out passages are from unseen chapters in a different narrative register than the training half.
2. **Open-ended behavioral prediction rather than structured-format scoring.** Twin-2K is the closest comparison; it is Likert-format rather than open-ended.
3. **Representation of how a person reasons, not what they said or prefer.** PersonaGym tests voice consistency; AlpsBench tests preference alignment; LongMemEval / LoCoMo tests fact recall. None tests transfer of interpretive patterns.

This is the gap the paper's battery targets. The battery is not a replacement for any of the above. It is a test of a different property: whether a representation of a specific person enables a model that has never seen the person's held-out reasoning to anticipate it accurately.

---


## Appendix G. Letta Stateful-Agent: Exploratory Case Study (full)

*Body summary in [§4.5](#sec-4-5). This appendix retains the full method, per-subject results, robustness checks, content analysis, and caveats from the original [§4.5](#sec-4-5) in v9 / earlier drafts of v10.*


**This section is a post-hoc exploration, not a replication or a headline finding.** N=3 subjects (Hamerton, Ebers, Babur), one Letta version, one response model (Claude Haiku), a 40-question battery per subject. The intent is to characterize what Letta's stateful-agent architecture produces when invoked directly, and how that compares at matched response model to Base Layer's compressed-brief variant. It is not an attempt to establish that two systems reach a common target.

> **Headline result on the small sample tested (5-judge primary):** Letta's self-edited memory block scores higher than Base Layer's compressed-brief variant on all 3 subjects at matched response model. Hamerton **3.10 vs. 2.96** (Δ +0.14), Ebers **2.76 vs. 1.72** (Δ +1.05), Babur **2.42 vs. 1.88** (Δ +0.54). A robustness rerun against Base Layer's full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The gap widens at the two smaller corpora and narrows at Babur. Multi-subject replication is flagged as the highest-priority external falsification ([§7.5](#sec-7-5)).

Letta is the one commercial memory system in the study whose architecture supports an alternative to retrieval at query time. Alongside the archival retrieval path tested in [§4.4](#sec-4-4), Letta agents maintain a persistent memory block that the agent itself rewrites during ingestion. This is the stateful-agent design from the original MemGPT paper. It is architecturally distinct from retrieval-based memory: the representation is authored by the agent over the course of reading the source corpus, rather than chunked and indexed for later retrieval. [§4.5](#sec-4-5) examines what that produces on a small set of subjects, with the caveats above. Multi-subject replication across the full gradient, multiple response models, and a comparison against the Base Layer full layered stack (rather than the compressed variant used here) are flagged as follow-ups in [§7.5](#sec-7-5).

---

**Test design.** A fresh Letta agent was initialized and fed the training half of each subject's corpus turn-by-turn. The agent was allowed to self-edit its memory block during ingestion, its native MemGPT behavior. After ingestion, the resulting memory block was extracted and served as context to Claude Haiku 4.5, the response model used throughout the main study. The behavioral-prediction battery was the main-study battery. Three subjects were tested, spanning a 9× corpus-size range:

| Subject | Source corpus | Corpus size (words) | Letta block size (chars) |
|---|---|---:|---:|
| Hamerton | Philip Gilbert Hamerton, *An Autobiography* (training half) | 25,231 | 22,472 |
| Ebers | Georg Ebers, *The Story of My Life* (training half) | 48,161 | 68,413 |
| Babur | Babur, *Babur-nama* (training half) | 222,742 | 335,349 |

The direct comparison: Letta's stateful-path memory block fed to Haiku, vs. Base Layer's full-stack specification fed to the same Haiku, on the same battery and judge panel. Both are interpretive representations delivered as context; the test isolates the representation itself.

---

**Methodological note on the Base Layer condition served here.** The Base Layer side of this matched-rerun loaded the unified brief variant (a ~7K-character synthesized document served as a single artifact) rather than the full layered stack (anchors + core + predictions + brief) that [§4.4](#sec-4-4)'s controlled and native C2a / C3 conditions use. The unified brief is more compressed on referential detail than the layered stack. A layered-stack rerun on these three subjects would likely narrow the Letta-over-BL gap; whether it narrows to parity or reverses is not measured. The table column header below reflects this: the Base Layer side is the unified brief variant.

**Result (5-judge primary: Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).**

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Babur | 2.42 | 1.88 | **+0.54** |

On all three subjects tested, Letta's stateful-path block, served to the same response model as the Base Layer unified brief, produces a higher per-subject mean score than the unified brief. Both representations land well above the retrieval-only baseline at matched response model ([§4.4](#sec-4-4) Letta archival Δ_spec for these subjects: Hamerton near parity with Base Layer retrieval, Ebers +0.31, Babur near-null).

**Judge-panel robustness.** The 7-judge sensitivity aggregate (Hamerton +0.093, Ebers +0.746, Babur +0.232; see `docs/research/letta_stateful_matched_rerun.md` Part 7 appendix) preserves direction on all three subjects. The 5-judge primary values are larger than the 7-judge values on Ebers and Babur by +0.30 and +0.31 points respectively, because the two Gemini judges were inflating Base Layer scores relative to the calibrated core on those subjects. Excluding Gemini from the aggregate (the paper's 5-judge primary convention; [§3.6.3](#sec-3-6-3) and [§4.6.2](#sec-4-6-2)) therefore widens the Letta-over-BL gap rather than narrowing it. Hamerton is the exception (5-judge Δ +0.14 vs. 7-judge +0.09), where Gemini inclusion slightly narrowed the gap rather than widening it. In all three cases, the Letta-block-outperforms-BL-spec direction is stable across panels.

---

**Compression behavior: divergence at large corpora.**

Letta's memory block grew roughly linearly with source corpus size. At the largest subject (Babur), Letta's API began rejecting ingestion requests at approximately 333,000 characters. After 22 consecutive failed ingestion attempts, the final block measured 335,349 characters. Letta's declared block-size metadata limit is 100,000 characters, unenforced in practice; the effective ceiling on the server side appeared to be a different API-level limit around 333K.

At the ceiling, the block contained **25.4% verbatim sentence duplication** on Babur, compared to 0% duplication on Hamerton and 0% on Ebers. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing. The representation carries corpus-derived narrative at scale but does not preserve the compression property that makes large corpora tractable.

Base Layer's compose step keeps the full-stack specification at 34,000-40,000 characters across the same corpus-size range. At Hamerton, the two representations are the same order of magnitude in size; at Babur, the Base Layer specification is roughly one-tenth the size of the Letta block. The two systems are prediction-band compatible at small corpora; they diverge on compression at large ones.

**What the ceiling means for deployment.** Served on every query, a 335,000-character Letta block costs roughly 84,000 tokens of context. At current frontier pricing this is materially more per-query cost than the Base Layer specification's ~10,000 tokens, and it exceeds the context window on the smaller-context models still common in production [^fn25]. The 25.4% verbatim-sentence duplication observed at the ceiling indicates the block would be functionally smaller with a deduplication pass: roughly 250,000 characters of distinct content in a 335,000-character block. Whether that extraction pass is a tractable post-processing step on the Letta side is an engineering question, not one this study measures. For production deployment, the ceiling and the duplication together argue for representation compactness as a first-class design constraint, not a nice-to-have.

---

**What this exploration does and does not show.**

On N=3 subjects, with one response model and one Letta version, Letta's stateful-path block and Base Layer's compressed-brief variant both land above retrieval-only context at matched response model, in a similar prediction band. This is consistent with (though does not establish) the idea that the behavioral-specification target is reachable by representation-production mechanisms outside offline-authored retrieval composition. Establishing that would require multi-subject replication across the full gradient, multiple response models, and a comparison against Base Layer's full layered stack rather than the compressed variant tested here. All three are flagged in [§7.5](#sec-7-5).

What the exploration does show is the shape of the engineering tradeoff between the two paths. They differ in how the representation is produced (offline authoring vs. online self-editing), in what it carries (interpretive scaffolding vs. corpus-derived narrative at higher referential density; see content comparison below), and in how it scales [^fn26]. These are tradeoffs to characterize, not a resolved comparison.

---

**Content comparison: what each representation retains.**

To test whether Letta's higher matched-model score comes from preserving original corpus text the response model could cite, we ran a post-hoc content analysis on the three subjects. The strong form of that hypothesis is refuted. Neither representation is a quote library. Checking what fraction of consecutive five-word sequences in each representation also appears verbatim in the training corpus (a standard overlap check), both representations score under 1%: the Letta block ranges 0.0-1.0% depending on subject, the Base Layer specification scores 0.0% on all three. The same check for consecutive ten-word sequences gives under 0.1% for both. Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts.

A refined version of the hypothesis does hold, with the magnitude smaller than first reported. The two representations differ in **referential density**: Letta's rolling summary retains more unique proper nouns, dated events, and named secondary characters than Base Layer's [§4.5](#sec-4-5) specification, and the gap scales with corpus size. On Babur (the largest corpus), Letta's block carries 416 unique capitalized named-entity tokens vs. Base Layer's 65, a ratio of about **6×**. On Ebers (mid-size), the counts are 53 vs. 34, a ratio of about **1.5×**, closer to parity. Base Layer, by construction, compresses episodes into cross-cutting behavioral patterns with fewer surface referents; the pipeline explicitly anonymizes the subject during authoring and compresses corpus-level specifics into dimensional axioms. Letta's stateful-agent path preserves more of the referential surface while also encoding behavioral patterns. The referential-density gap is real but corpus-dependent rather than uniformly an order of magnitude.

Both representations produce responses that outperform retrieval-only context at matched response model, but they diverge on referential detail. On battery items that reward specific-event recall, Letta has more named entities to cite. On items that reward principled interpretation across episodes, Base Layer's dimensional axioms compete directly. The [§4.5](#sec-4-5) matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects. Flagged in §7.

**Replication as the load-bearing next step.** The three-subject comparison reported here is not a claim that alternative representation-production architectures reach the interpretive-representation target. It is a case study with direction but not power. Multi-subject replication across the full 14-subject gradient (layered-stack Base Layer vs. Letta stateful, both anonymized to match, multiple response models) is the highest-priority external falsification we can run on [§4.5](#sec-4-5), and is flagged as such in [§7.5](#sec-7-5). If that replication closes the gap at parity, [§4.5](#sec-4-5)'s direction holds on a wider sample. If it reverses, [§4.5](#sec-4-5)'s direction was corpus-specific.

Full content analysis at `docs/research/` (see `_content_analysis_results.json` and the N=3 per-subject breakdown). The methodological note on the Base Layer condition is now hoisted above the result Table at the top of this section.

---

**Caveats.**

- N = 3 subjects on this path. Extending across the full 14-subject gradient would let the comparison speak to the population-of-relevance level, not only a selected set of corpus sizes. Flagged in [§7.5](#sec-7-5).
- One response model (Haiku) on both conditions. The comparison is tested at matched response model; whether it holds at other response models is an open question.
- Letta's 333K-character ingestion ceiling is a hard architectural constraint in the current release. For small corpora the two representations are interchangeable in prediction behavior; for large corpora the ceiling is material.
- Base Layer condition used the unified `spec.md` variant for the main [§4.5](#sec-4-5) table. A robustness rerun with the full layered stack (anchors + core + predictions + brief, name-restored to match the [§4.5](#sec-4-5) naming convention) preserves direction on all three subjects (Δ_Letta−BL = +0.27 / +1.21 / +0.38 on Hamerton / Ebers / Babur; full report at `docs/research/_letta_rerun/fullstack_named/RESULTS.md`). The gap widens at the two smaller corpora and narrows at Babur, consistent with a Pattern 2 (over-theorization) effect on small corpora rather than a content-volume effect at large corpora. Direction is invariant across both Base Layer spec forms.
- **Naming asymmetry.** Letta's stateful-agent path ingested the named source corpus and wrote a memory block that references the subject by name throughout. Base Layer's authoring pipeline strips the subject's name during specification authoring ([§3.7](#sec-3-7) anonymization step); the [§4.5](#sec-4-5) comparison restores the name at the surface level only (string substitution on the composed artifact). The two sides of the comparison therefore differ in whether the subject's name is load-bearing during representation production vs. only at serving time. Flagged as a methodological gap in [§7.5](#sec-7-5).

---

**Raw data and scripts.** Letta stateful matched-rerun data at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json`. Generation and scoring scripts live in the same directory as a numbered chain (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, `70_compute_5judge_primary.py`); see the `README.md` inside `docs/research/_letta_rerun/`. Full characterization of block content, duplication behavior, and API responses in `docs/research/letta_stateful_deep_read.md` and `docs/research/letta_stateful_matched_rerun.md`.

---


## Appendix H. Glossary

Defined terms used as terms of art throughout the paper.

**5-judge primary panel.** The locked judge aggregation for headline numbers. Aggregation rule: per-judge per-question score → per-judge per-subject mean → panel mean across {Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4}. See [§3.6.3](#sec-3-6-3).

**7-judge sensitivity panel.** The 5-judge primary plus Gemini 2.5 Flash and Gemini 2.5 Pro, reported as a sensitivity check. See [§3.6.3](#sec-3-6-3).

**Anchors / Core / Predictions.** The three layered artifacts comprising a Behavioral Specification. Anchors: short axiomatic claims about how the subject reasons. Core: connects anchors into coherent reasoning patterns. Predictions: derives forward-looking decisions from the core. A composed brief sits above all three. See [§3.7](#sec-3-7).

**Behavioral prediction.** The operational test for representational accuracy. Given a situation drawn from text the model has never seen, the model generates how the subject would respond; the response is scored against the subject's own verbatim response on a 1-5 interpretive rubric. See [§1.1](#sec-1-1), [§3.6](#sec-3-6).

**Behavioral specification.** A static document of approximately 7,000 tokens that extracts and encodes a person's behavioral patterns. Composed of three layered artifacts (anchors, core, predictions) plus a unified brief. Layered above memory-system retrieval as an interpretive structure. See [§1.1](#sec-1-1), [§3.7](#sec-3-7).

**Interpretation.** In this paper, the human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. The property the Behavioral Specification is designed to mirror. See [§1.1](#sec-1-1).

**Representational accuracy.** The AI-side property: how faithfully a model's internal representation of a specific person captures that person's interpretive patterns. Operationalized via behavioral prediction on held-out reasoning situations. See [§1.1](#sec-1-1), [§3.1](#sec-3-1).

**Tier 1 / Tier 2.** Tier 1 is the main study: Haiku 4.5 response model across all 14 subjects, every condition, Haiku-generated batteries. Tier 2 is the cross-provider directional probe: Sonnet 4.6 and Gemini 2.5 Pro response models on 3 subjects (Ebers, Yung Wing, Zitkala-Sa) with GPT-5.4-regenerated batteries. See [§3.5](#sec-3-5), [§4.6.1](#sec-4-6-1).

**Wrong-spec control.** A deliberately mismatched Behavioral Specification served in place of the correct one. Two variants: **v1** (adversarial fixed derangement maximizing cultural and temporal distance; aggregate Δ −0.25) and **v2** (seed-fixed random derangement; aggregate Δ +0.15). See [§1.3](#sec-1-3), [§3.4](#sec-3-4), [§4.3](#sec-4-3).


[^fn1]: across a major career change, a profound life event, or a decades-long corpus with distinct epochs

[^fn2]: *"Sunity Devee's father believed he acted as a public man guided by conscience and divine duty in accepting the marriage proposal"*

[^fn3]: Ebers at baseline 1.04 with a strong positive effect, Yung Wing at baseline 1.88 with a modest positive effect, and Zitkala-Sa at baseline 2.34 with a negative effect

[^fn4]: fixed before any results were computed, so that no researcher decision could shift the headline numbers after seeing the data

[^fn5]: "I could not undeceive him... the fancy happily caused by the touch of a woman's hand soothed his dying hour"

[^fn6]: sensitivity to baseline distribution, treatment of ties, paired-sample dependency, tiny-gain inflation, hidden catastrophic harm, easy-baseline gaming, scale-free illusion of portability

[^fn7]: alongside the 55.0% anchor-crossing rate, which is the same unit at a stricter threshold: "does the response move to a different rubric category?" rather than "does the response improve at all?"

[^fn8]: for example, Ebers the 19th-century German Egyptologist receives Equiano the 18th-century West-African/British autobiographer; Seacole the 19th-century Jamaican nurse receives Bernal Diaz the 16th-century Spanish conquistador

[^fn9]: Example B below has a −0.20 coincidental-overlap case where the wrong spec nearly matches the correct spec; Example C below has a −3.60 clean mismatch case

[^fn10]: the wrong person's pattern happens to predict the same surface behavior on this particular question, for different underlying reasons; Example B below is one such case

[^fn11]: 507 from the v2 random-derangement protocol on the 13 global subjects, plus 80 from the v1 adversarial protocol on Hamerton across all five battery tiers; validated against a 30-response stratified manual spot check

[^fn12]: example, from one Keckley wrong-spec response: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*

[^fn13]: literal-recall, where retrieval already supplied the plain answer; or refusal-triggering, where retrieved facts cannot ground a prediction

[^fn14]: 57 helps vs 53 hurts at the +0.3 subject-mean threshold; 71 vs 79 at the per-question anchor-crossing grain on the low-baseline 9

[^fn15]: "my one cherished hope was to see abolishment of swords altogether" is counter-trend in 1860s Japan

[^fn16]: *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"*

[^fn17]: the operational target for product deployment on real users, whose private reasoning is not in any training corpus

[^fn18]: literal-recall, where retrieval already supplied the plain answer; or refusal-triggering, where retrieved facts cannot ground a prediction at all

[^fn19]: the specification helps more where baseline is lower, wrong-spec hurts more than random derangement, the advantage widens on less-known subjects, etc.

[^fn20]: the response model declines to fabricate interior motive on a question where the retrieved facts are insufficient

[^fn21]: the property of AI systems operating within acceptable behavioral constraints regardless of whose instructions they follow

[^fn22]: recomputed under strict 5-judge primary; the legacy audit-doc value was +0.646, which used a Hamerton-divergent intermediate aggregation

[^fn23]: no observed transitions from bands 2, 3, or 4 into band 5 across the full 14-subject panel; the only band-5 endpoints reached come from band 1

[^fn24]: for example, the Tier 2 3-subject replication and the 3 wrong-spec derangement draws on the author's living-user replication

[^fn25]: 128K token windows struggle when the block alone is two-thirds of the budget, before any conversational state

[^fn26]: bounded compression vs. an ingestion ceiling observed at ~333K characters on the largest corpus we tested
