# Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization

**Author:** Aarik Gulaya, Base Layer (`aarik@base-layer.ai`, `base-layer.ai`)
**Date:** April 2026
**Preprint** (Apache 2.0)
**Data + Code:** github.com/agulaya24/base-layer
**Study Repository:** github.com/agulaya24/memory-study-repo

---

## 1. Introduction

<!--
FUTURE-WORK NOTE (Aarik 2026-04-30, during §4.1 walk):
Consider adding a worked example to §1 (Introduction) for the production release.
Aarik's framing: "the Section 3 example is impressive — wish it came earlier so readers see what we're working with (responses, judging, transitions) before §3."
Likely candidates for the worked example to mirror in §1:
  - §3.6.2 multi-anchor crossings (Seacole Q2, Hamerton Q25, Bernal Díaz Q16)
  - §3.7 Hamerton specification examples (Anchors A1, Core, Predictions P3)
  - §4.1.1 Seacole Q2 worked rubric example across condition bands
Decision deferred to production-release pass; not in v11.5 active edit.
-->

### 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what "memory" must do for a specific individual. State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 70% to 93% range depending on provider, model, and benchmark variant (§2.2). Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. Viewing situations from different lenses can lead to entirely different interpretations of the same set of facts. This has been shown across the human experience, from the sciences to religion, and by extension to the relative experiences of any individual; memory is deeply personal. For an AI to serve a specific person, it must be given context on the framework that person uses to reason, not just the raw facts or information itself. Throughout this paper we use the term **Behavioral Specification** to refer to a static document that extracts and encodes a person's behavioral patterns; the operational definition is developed across §3.7. The Behavioral Specification is the artifact that captures this interpretive framework, and is provided to an AI as context.

We introduce **representational accuracy** as the corresponding AI-side property: how well a system's internal model of a specific person captures their interpretive patterns. It is not recall, preference matching, or persona consistency. It is a distinct property of the AI system, and state of the art memory benchmarks do not isolate it. Prior work closest to this axis (Twin-2K for scaled behavioral prediction, PersonaGym for persona fidelity, AlpsBench for preference alignment) measures related properties but not the transfer of a person's interpretive patterns to new situations the system has never seen. §2.1 positions each benchmark against what this paper measures, and Appendix F develops the scope differences in detail.

**The core hypothesis of this research is that representational accuracy of a person's interpretation improves an AI system's behavioral alignment with that person.** This is the operational primitive for any AI system meant to act on a person's behalf: the system's behavior can only match the user's reasoning to the extent the system represents that reasoning accurately. The operational test in this paper is behavioral prediction on held-out situations: given a situation drawn from text the model has never seen, the model generates how the subject would respond; the response is scored by a panel of calibrated large language model (LLM) judges against the subject's own verbatim response in the held-out text on a 1-5 interpretive rubric (§3.6). Accurate prediction on held-out text is evidence that the representation captures the subject's recurring patterns of reasoning, distinct from the facts and stylistic surface that current extraction pipelines already produce. The design also reduces the risk of sycophancy[^sycophancy-def]: the answer is checked against the person's narrative, which the model has never seen, not against anything the user says during the conversation. The held-out test is one operationalization of the hypothesis.

[^sycophancy-def]: Sycophancy refers to a model adjusting its answer to match what the user appears to want, often by agreeing with or flattering them. See Sharma et al. 2023, Perez et al. 2022, and §2.4 (Jain et al. 2025). Whether an accurate representation also produces aligned behavior on situations the person never encountered, and what else such a representation enables (steering, agent action on the person's behalf), are open questions of the broader research program (§7).

We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated LLM judges to evaluate the performance of each memory system, on its own and in combination with a **Behavioral Specification**: a static document that extracts and encodes a stable representation of a corpus's behavioral patterns. The specification captures the recurring patterns in how the subject reasons, drawn from the shape of judgments and reactions across the corpus (for example: *"spiritual integrity over social cost..."*, *"reform through love..."*, *"hierarchical deference..."*). A walked example of the audit chain from such a pattern back to its grounding facts and source passages appears in §2.3.

Defined terms used throughout the paper are collected in [**Appendix H**](#appendix-h-glossary) for reference.

### 1.2 What we tested

We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions and was never shown to the **response model**, the language model being asked to predict how the subject would respond. The Behavioral Specification is the context document that the response model receives. The set of held-out questions for each subject is the **question battery** (size and composition per subject in §3.6). The test was whether each system, under each tested condition, could predict how that specific person would respond in situations drawn from text it had never seen.

The Behavioral Specification itself is built from the training-half corpus through an extraction-and-authoring pipeline (§3.7). The pipeline distills the recurring patterns of how the subject reasons into a single structured document, typically around 7,000 tokens (~5,000 words) long. That document is what the response model receives as context when asked to predict how the subject would respond.

**Hypotheses.** The study tests five claims about how a representation of a person shapes AI behavior on that person's behalf:

- **H1.** A response model given a Behavioral Specification produces responses that align with the person's documented behavior more closely than the same model given no context, facts retrieved by a memory system, the full extracted fact list, or the raw source corpus (§4.1).
- **H2.** The specification's benefit is inversely proportional to the response model's pretraining coverage of the person. Its effect is largest on people the model does not already know (§4.1).
- **H3.** The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect (§4.3).
- **H4.** The specification interacts with memory-system retrieval in a structured way that depends on the type of question being asked. Aggregate effects on each memory system reflect the balance of these per-question patterns and shift with retrieval architecture (§4.4).
- **H5.** The Behavioral Specification's quality advantage is also a compression advantage: a ~7,000-token (~5,000-word) specification recovers most of the predictive accuracy of an 80-400K-token (~60-300K-word) raw corpus (§4.2).

Post-hoc analyses surfaced during the work are reported alongside these results.[^pre-vs-post-hoc]

[^pre-vs-post-hoc]: Several post-hoc analyses surfaced during the work and are reported alongside the H1–H5 results: the cross-system retrieval-overlap divergence (§4.4.1, with sensitivity in §4.6.5), the Letta stateful-agent case study (§4.5; Appendix G), the abstention-credit validity audit (§3.6.6), and the per-subject wrong-spec heterogeneity table (§4.6.4). These are labeled where they appear and are reported as exploratory rather than at the same evidentiary tier as the pre-registered hypotheses. Full breakdown in Appendix B.10.

**Primary and secondary outcomes.** The **primary outcome** is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.6).[^primary-aggregation] Cross-subject claims are calculated subject-by-subject before averaging, so they are not driven by subjects with larger question batteries. As a **secondary outcome**, we report the per-question **improvement rate**: how often a context condition helps relative to the comparison baseline (§4.2.1), not just by how much it helps when averaged. The formal proposal and failure-mode analysis for the secondary outcome are in §4.2.1; full operational details for both outcomes are in §3.6.

[^primary-aggregation]: Aggregation rule (the "locked rule" referenced throughout): per-question scores within a (subject, condition) cell are first averaged across the 5 judges, then per-subject means are aggregated across the 14 subjects. Full mechanics in §3.6.

Each memory system is tested in both a controlled configuration (identical pre-extracted fact pool) and a native configuration (the provider's own ingestion pipeline); design detail in §3.4 and §3.5. Running in parallel across both is the Behavioral Specification, tested alone and layered on top of each configuration. Every meaningful combination of inputs is evaluated as its own condition:

| Condition | Inputs given to the model | Purpose |
|---|---|---|
| **No context** (C5) | Nothing. The model answers from pretraining alone. | Pretraining baseline. Measures what the model already knows about the subject from public sources. |
| **Retrieval alone, controlled** (C1) | Top-k facts retrieved by each memory system (Mem0, Letta[^letta-additional], Supermemory, Zep, Base Layer) from the shared fact pool. | Tests retrieval sufficiency, and whether providers converge on which facts are most relevant given identical input. |
| **Retrieval alone, native** (C1 native) | Top-k results from each memory system's own ingestion pipeline operating over the raw training corpus. | Real-world comparison of each memory system's full ingestion-plus-retrieval stack. |
| **All facts, no specification** (C4) | Every extracted fact for the subject, loaded into context at once. | Tests whether information sufficiency alone drives prediction, independent of structure. |
| **Raw corpus, no specification** (C8) | The full training-half corpus loaded into context. | Tests whether unstructured source text can substitute for an interpretive representation. |
| **Specification alone** (C2a) | The Behavioral Specification, with no retrieval, no facts, and no corpus. | Tests whether structure without retrieval is sufficient on its own. |
| **Retrieval + specification, controlled** (C3) | Memory system retrieval from the shared fact pool, plus the specification. | Tests whether the specification layers cleanly on retrieval when the input is held constant. |
| **Retrieval + specification, native** (C3 native) | Memory system's own ingestion and retrieval, plus the specification. | Tests whether the specification improves the real-world deployment of each memory system. |
| **Facts + specification** (C4a) | Every extracted fact plus the specification. | Combines full information and structure to test the upper bound of context-provided prediction. |
| **Corpus + specification** (C9) | Raw training corpus plus the specification. | Tests whether structure is additive to unstructured source text. |
| **Wrong-specification control** (C2c) | A different subject's specification applied to this subject. Two variants: an adversarial fixed pairing (v1) and a random derangement (v2).[^c2c-construction] | Tests whether the effect is driven by the content of the correct specification, or by the mere presence of structured prompting. |

[^c2c-construction]: v1 is a deterministic fixed pairing that matches each subject with a culturally and temporally distant other (mapping in `scripts/run_global_rerun.py`); v2 applies a random derangement, seed-fixed, so no subject receives its own. Hamerton has an additional variant (Franklin's specification) reported separately in §4.1.2.

[^letta-additional]: Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions in this table, we ran a separate test on three subjects spanning a 9× corpus-size range (Hamerton, Ebers, Babur). A fresh Letta agent ingested each training corpus turn-by-turn and was allowed to self-edit. The resulting memory block was then served to the same response model used throughout the main study for a matched comparison against the Behavioral Specification. Full methodology and results in §4.5.

The 14 subjects span four continents and roughly two millennia of written human experience. Ordered chronologically: Saint Augustine (North Africa, 4th-5th c.), Babur (Central Asia and India, 15th-16th c.), Bernal Diaz del Castillo (Spain and Mexico, 15th-16th c.), Benvenuto Cellini (Italy, 16th c.), Jean-Jacques Rousseau (France, 18th c.), Olaudah Equiano (West Africa and Britain, 18th c.), Mary Seacole (Jamaica and Britain, 19th c.), Elizabeth Keckley (United States, 19th c.), Yung Wing (China and the United States, 19th c.), Philip Gilbert Hamerton (Britain, 19th c.), Fukuzawa Yukichi (Japan, 19th c.), Georg Ebers (Germany, 19th c.), Sunity Devee (India, late 19th c.), and Zitkala-Sa (Yankton Dakota, early 20th c.). Source corpora range from 25,231 words (Hamerton) to 422,772 words (Babur). Full source references are in §3.2.

Predictions were scored on a 1-5 rubric where the integer anchors mark categorical shifts in answer quality (full rubric in §3.6, summarized in the table below). Crossing an integer anchor represents a real change in the kind of answer the model produced, not a small numerical adjustment. For example, a move from 1.8 to 2.4 crosses the 2.0 boundary: the model goes from refusing the question or producing a wholly wrong answer (anchor 1) to engaging with the right topic, even when the specific prediction is still off (anchor 2). Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

| Score | What it means | Shift from previous anchor |
|---|---|---|
| **1** | Refuses or wholly wrong | (rubric floor) |
| **2** | Right topic, wrong prediction | From cannot engage to orienting to the question |
| **3** | Right domain, no specifics | From wrong prediction to in the neighborhood |
| **4** | Right direction with specifics | From in the neighborhood to right direction with specifics |
| **5** | Predicts the specific outcome | From right direction to matching the held-out text |

Score interpretation, including the cross-anchor rule for fractional scores (e.g., 2.5, 3.4), is in §3.6.2. Example questions per subject and panel composition are in §3.6.1.

The **baseline** we refer to throughout is the no-context condition (C5): the response model's score with no external information. **Low-baseline** subjects are the **population of relevance**: people the model has insignificant pretraining understanding of, even when fragments of their digital footprint exist in training data. **High-baseline** subjects are the opposite, people the model already knows about from pretraining. Almost everyone in the active human population falls into the low-baseline band; even people with substantial public output captured in training corpora have only fragments of their reasoning represented. The low-baseline band is the rule, not the exception.[^baseline-thresholds] Results are reported separately on the low-baseline slice (n=9) alongside the full 14-subject analysis.

[^baseline-thresholds]: Operational thresholds: low-baseline C5 ≤ 2.0 on the 1-5 rubric, high-baseline C5 > 3.0. Full distribution and band assignments in §3.2.1.

The study is structured into two tiers. Tier 1 (main study) uses Claude Haiku 4.5 as the response model across all 14 subjects on every condition. Tier 2 is a smaller cross-provider directional probe (§3.5, §4.6.1). The 7-judge panel spans three providers; the 5 non-Gemini judges form the primary aggregate and the 2 Gemini judges are reported as a sensitivity check (§3.6.3).

Together these hypotheses test whether a Behavioral Specification can move a language model toward acting in alignment with a specific person.

### 1.3 What we found

The Behavioral Specification (referred to as the **spec** in the discussion that follows) changes the rubric category of answer the language model produces, and the improvement is largest where the model knows the person least.[^low-baseline] What follows are seven findings about how the spec changes the way a language model acts on a person's behalf. The thread across them is alignment: how accurately a model predicts a specific person's reasoning is the operational measure of how closely it can act in alignment with that person.

[^low-baseline]: "Low baseline" means C5 ≤ 2.0 on the 1-5 rubric. This is the population of importance for AI personalization (§2 lede, §1.4, §5.2): on a frontier model serving general AI users, almost everyone falls in or below this band, even people with substantial public output. The §2 lede defines what "personalization" means in this paper's stronger sense (the interpretive layer beneath stated preferences and biographical facts).

**Headline findings.**

- **Gradient.** The Behavioral Specification's benefit is largest where the model knows the person least. When pretraining understanding of someone is weak, the spec reliably moves predictions from generic guesses to grounded, person-specific responses; across the 9 low-baseline subjects every single one improved when the spec was provided. *Mean lift +0.89 points on the 1-5 rubric; 78.6% of individual questions improve.*[^statsig][^delta-aggregation] Detail in §4.1.
- **Step-changes, not nudges.** The spec doesn't just nudge the score; it changes the *kind* of answer the model produces. Crossing one rubric anchor moves a response from "wrong prediction" to "right direction with specifics." Crossing two or more anchors is a bigger jump: a single question where the AI moves from refusal or generic guessing all the way to a recognizable, person-specific response. *55.0% of low-baseline questions cross at least one anchor upward. Roughly 1 in 5 cross two or more anchors; roughly 1 in 17 cross three or more.* This pattern holds on the spec, facts+spec, and corpus+spec conditions across the low-baseline subjects. Detail in §4.1.
- **Compression.** A short structured representation, such as a Behavioral Specification, produces comparable accuracy to the full source text at 5x to 80x smaller context length (per-subject compression ratios in §4.2). The spec is not summarizing; it is selecting and structuring the behavioral signal. *Across the 9 low-baseline subjects, the spec recovers most of what the full corpus delivers (spec-alone +0.71 vs. corpus-alone +0.93 over baseline). On Hamerton, the smallest corpus tested, the spec actually beats the raw corpus (2.63 vs. 2.27).* Detail in §4.2.
- **Content specificity.** What produces the lift is the content of the correct spec for the correct person, not the presence of a structured prompt. Give the model a different subject's spec instead of the right one and accuracy drops below the no-context baseline. Random pairings (a wrong spec assigned by chance to a different subject) sometimes still produce predictions that align with the held-out text, suggesting some behavioral patterns transfer across subjects, but the correct spec consistently outperforms. *Adversarial wrong-spec Δ = −0.25; random-derangement Δ = +0.15; correct spec Δ = +0.35.* Detail in §4.3.
- **Memory-system layering.** Layered on top of commercial memory systems, the spec helps dramatically on interpretation-heavy questions and reduces refusal rates on questions retrieved facts could not ground. It also exposes per-question structure the aggregate hides: some questions improve, some regress, and the balance shifts with retrieval architecture. *Aggregate mean lift is positive on 3 of 4 commercial memory systems (Mem0, Letta, Zep); per-question anchor crossings range from 20% to 36% across systems.* Detail in §4.4.
- **Hedging reduction.** The spec near-eliminates the model's tendency to hedge or refuse on low-baseline subjects. *Baseline hedging drops from 41.2% of responses to 0.4%.*[^hedging] This is the gradient operating at its floor: where the model would otherwise refuse to engage, the spec converts refusal into substantive response. Detail in §4.3.
- **Memory-system providers do not agree on the most important facts.** On standard recall benchmarks like LongMemEval and LOCOMO, the four commercial memory systems we tested perform within a few percentage points of each other. Yet given the same pre-extracted fact pool and the same questions, they retrieve substantially non-overlapping top-10 facts. Convergence on top-K under identical input would have been evidence of a shared interpretive framework; the systems do not converge. *On 35.9% of (system pair, question) instances two systems share zero facts in their top-10s; on 65.6% they share one or fewer. Mean pairwise overlap 8.3% across the ten system pairs.* Detail in §4.4.1.

[^statsig]: The Wilcoxon signed-rank test asks how unlikely it is that the observed pattern of subject-by-subject improvement could happen by chance. Result: W = 11, N = 14, p = 0.007. Full regression (slope −0.96, R² = 0.82) and the leveler-framing of the gradient (the spec brings every subject toward roughly the same prediction quality, ~2.44 on the 1-5 rubric per the locked per-subject aggregation rule) are in §4.1.

[^delta-aggregation]: +0.89 is the cross-subject mean of per-subject Δ_C4a (per-subject grain is the locked unit of inference; see §1.2 aggregation rule). The grand-mean alternative (C4a grand mean minus C5 grand mean) yields +0.93. Detail in Appendix B.9.

[^hedging]: Headline number uses the broad rule (any refusal pattern anywhere in the response) under the facts + spec (C4a) condition. The stricter rule (refusal pattern as the first non-whitespace text) gives 28.8% → 0.0% on the same condition.

**Mechanism: three patterns of interaction with retrieval** (full development in §4.4.2). Baseline runs suggest the model already attempts shallow inference from a user's raw data on its own; the specification makes that inference inspectable and structured.

- **Pattern 1, Interpretation-heavy questions.** The specification supplies a generalized pattern from the source that has to transfer to a new situation; retrieved facts alone are not enough (Fukuzawa Q26).
- **Pattern 2, Literal-recall questions.** Retrieval already returns the plain answer; the specification's interpretive framing drifts past the question and negatively impacts the response (Yung Wing Q5).
- **Pattern 3, Refusal-triggering questions.** When the spec supports refusing without enough information (not all specs do), the model produces principled refusals aligned with the spec; the content-match rubric still scores them as off-base (Zitkala-Sa Q18).

**Robustness across providers.** We varied both the question-battery generation model and the response model across providers; the spec direction reproduces. Detail in §4.6.1.

**Exploratory note: Letta stateful-agent path.** Letta's stateful-agent architecture self-edits a persistent memory block during ingestion. On 3 subjects (post-hoc), it scored above Base Layer's unified-brief specification at matched response model. At the largest corpus tested, the block grew to ~335K characters with 25% verbatim sentence duplication and 35-56% semantic near-paraphrase duplication, indicating an architectural ceiling at scale that does not apply to the unified-brief specification. Case study in §4.5 / Appendix G.

### 1.4 What this implies

AI is becoming a broadly used technology, comparable to email or mobile phones in how widely it touches daily decisions. The population of relevance (§1.2) is anyone who uses or will use an AI system. Even the autobiographers in this study, people whose work is in pretraining and who should technically be known to the model, score near the rubric floor in the no-context condition. On a frontier model serving the general population, the typical user sits even deeper into the low-baseline band than our subjects.

The gap the Behavioral Specification fills cannot be closed by training a larger model on more public data. The private record does not exist in a form a training corpus can capture; even where fragments exist, they are scattered across formats and channels and cannot be reliably reassembled into how a specific person reasons. The structural options for what fills this gap are narrow:

- Each person supplies their own representation to whatever AI system serves them. The Behavioral Specification is one implementation of this option, not the only one.
- Personalization remains surface-level (style, voice, preference, demographic inference, observable behavior), addressing the layer current memory systems already cover but missing the interpretive framework that lets an agent act on a specific person's behalf.
- AI systems infer a representation of the user from observed interactions, building it opaquely, without explicit input from the user or the ability for the user to inspect or correct it.

What this paper claims is that personalization infrastructure of the first shape (user-held, portable, inspectable, traceable, representation-grade) is what the next generation of human-AI interaction will require, especially as agents begin acting on people's behalf. §5 is an extended discussion of these implications; §7 develops the safety, alignment, and deployment implications.

---

## 2. Prior Work, Industry Benchmarks, The Fifth Target

AI memory and personalization research today is organized around four measurement targets: recall of stored facts, survey-response prediction, persona fidelity, and preference alignment. Each is supported by its own benchmark family and its own line of system design. None of them measures whether an AI system has an accurate internal model of how a specific person reasons. This paper proposes a fifth target, **representational accuracy**, and uses behavioral prediction on held-out reasoning situations as its operational test. The remainder of §2 walks the four existing targets, names the benchmarks attached to each, and positions the fifth alongside them.

Memory systems today optimize for recall. Recall-optimized efforts include both **neural-memory-analogue systems** (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings) and the broader class of vector-retrieval and embeddings-based commercial memory providers (Mem0, Zep, Supermemory, Letta). These systems do store and retrieve information for a specific user, but the property they are designed and benchmarked for is recall accuracy on standard benchmarks, not how accurately the system represents that user's reasoning. The optimization target is general by construction; any individual user's interpretation is not what these systems are measured against. A separate body of research, **cognitive-representation research**, studies human reasoning itself: how people form representations of others, how schemas compress experience. The gap between these directions is the translation: applying what we know about human reasoning to the direct interaction between an AI system and a specific individual, and shaping the system's internal model of that individual in a way that serves them rather than serving an average.

Language models are trained to produce responses that are helpful on average across a large population of users. That optimization target produces outputs that no single user is the reference point for. Personalization requires the opposite property: a system whose outputs are tuned to a specific individual rather than to a population aggregate. That kind of intentional individual-specificity, not "bias" in the negative sense but an explicit design target, is the missing thread in current AI memory and human-AI interaction research.

**Personalization in this paper's sense.** "Personalization" in current AI research typically means responsiveness to stated preferences (dietary restrictions, communication style) or stored facts about the user (location, occupation, history). Both are useful and both live at the surface of the user. We use "personalization" in a stronger sense throughout this paper. We mean representing the interpretive layer that sits beneath stated preferences and biographical facts: how a specific person organizes experience, what they treat as evidence, what reasoning patterns they apply across new situations. Preferences and facts are downstream artifacts of that interpretive layer; the layer itself is what produces them. The behavioral prediction battery and Behavioral Specification described in §3 instantiate personalization in this deeper sense, and §5 returns to what this layer is and is not.

### 2.1 Memory and personalization benchmarks

This subsection walks each of the four existing targets in turn, naming the benchmarks attached to each and their scope. Representational accuracy is positioned as the fifth target at the end of the walk. An extended benchmark-by-benchmark analysis is in Appendix F.

**Recall measures retrievability of facts, not reasoning about them.** LOCOMO (Maharana et al., ACL 2024, arXiv:2402.17753) measures conversational-memory quality: after a multi-session conversation, the system is asked questions like "what did the user say about their job on day 3?" and scored on fact retrieval. LongMemEval (Wu et al., ICLR 2025, arXiv:2410.10813) measures long-term memory across multiple sessions on five capability dimensions (single-session, multi-session reasoning, temporal reasoning, knowledge updates, abstention) and is heavily recall-weighted. A system can saturate recall on such benchmarks and still fail behavioral prediction, because retrieval answers the question "can the fact be found" rather than "does the system know how the person reasons about the fact." Recall is a necessary property for most downstream uses of memory but it is not sufficient for representational accuracy.

**Survey-response prediction infers how a person would answer one questionnaire item from how they answered others.** Twin-2K (Toubia et al., 2025, arXiv:2505.17479) does this for 2,058 participants on a 17-task heuristics-and-biases battery; items share a common format (multiple choice, Likert scale, numeric), scored by distance-based accuracy. Twin-2K's stated target is *prediction accuracy on survey interpolation*: the model is scored on how well it predicts a held-out questionnaire response, not on whether it represents the underlying reasoning that produced the response. Our target is representational accuracy on a cross-format task: autobiographical prose input, open-ended behavioral prediction output, rubric-based scoring against a verbatim held-out passage. The structured-questionnaire format and the open-ended behavioral reasoning this paper studies measure different properties. A system could perform well on Twin-2K and not on our battery (survey interpolation does not require modeling reasoning transfer to new contexts), and a system could perform well on our battery and not on Twin-2K (accurate reasoning representation does not guarantee survey-format numerical accuracy). The two benchmarks diagnose different properties of the same general capability.

**Persona fidelity measures whether a model stays in character across the back-and-forth of a conversation.**[^turn-def] PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416) scores consistency with a described persona during conversation: given a one-line persona ("You are a 45-year-old skeptical accountant from Toronto"), the model is scored on whether its multi-turn replies stay in-character, graded against a held-out criterion set. In practice the model is checked for consistency with the persona's surface attributes (skeptical, accountant-flavored responses; not breaking character into a different age or profession), not for whether it reproduces how a specific person would reason. PersonaGym's one-line descriptor is a substantially shallower input than this paper's ~7,000-token Behavioral Specification or Twin-2K's full-text survey persona;[^twin2k-persona-size] consistency with it does not require modeling that person's reasoning on new situations. PersonaGym measures a useful property (holding voice over a conversation); fidelity to a one-line persona is a weaker condition than representational accuracy.

[^twin2k-persona-size]: Twin-2K's full `persona_text` runs ~32,000 tokens; the `persona_summary` runs ~3,750 tokens. Both are substantially deeper than PersonaGym's one-line descriptor. Full breakdown of persona-input depth across benchmarks in Appendix F.

[^turn-def]: A "turn" is one round of conversation, a single exchange of one user message and one model reply. Persona-fidelity benchmarks score whether the model stays in character across many such exchanges in sequence.

**Preference alignment measures whether responses match user preferences.** AlpsBench (Xiao et al., 2026, arXiv:2603.26680) evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses: after ingesting a user profile, the model is asked conversational questions (preferences, emotional support) and responses are scored on preference alignment and emotional resonance rubrics, not on predictive accuracy. Their central finding, *that recall improvement does not automatically carry into preference alignment*, is arrived at independently and is complementary to this paper. Both papers point at the same gap from different sides: solving for recall is insufficient for what memory is ultimately for. Preference alignment is an outcome property (whether a response matches what the user prefers). Representational accuracy is an upstream property (whether the AI's internal model of the user is correct). Preference alignment is one downstream consequence of representational accuracy being correct; it is not the same property.

**We propose behavioral prediction on held-out reasoning situations as a test of a fifth target: representational accuracy.**

**Prediction is the test, not the goal.** We do not pursue prediction accuracy as an end in itself. The target is representational accuracy, the fidelity of an AI's internal model of a specific person, and behavioral prediction on unseen situations is the instrument we use to measure it. A prediction score tells us the representation captured something that generalizes to new situations; a low score tells us it did not. Prediction is a diagnostic; the Behavioral Specification is what this paper is testing. This distinction matters because the closest prior work on prediction benchmarks (Twin-2K) pursues prediction as its target. This paper is not positioning against Twin-2K on that target; it is measuring a different property. The two benchmarks address adjacent but distinct questions about AI personalization.

**The held-out design rests on a stability premise.** A person's interpretive patterns must be stable enough within their own corpus that what is captured from one half references what appears in the other. Without that, held-out behavioral prediction is impossible in principle, regardless of how good the representation is. The 14 main-study subjects have coherent autobiographical narratives consistent with the premise; §4.1 reports that the Behavioral Specification authored from training text generalizes to held-out text at above-baseline rates. The constraint matters: subjects whose reasoning shifts substantially across their corpus (across a major career change, a profound life event, or a decades-long corpus with distinct epochs) may not be well-represented by a single snapshot specification, which is one reason temporality is a flagged follow-up in [§7](#7-future-work). We state the premise explicitly so that what the held-out test can and cannot diagnose is clear.

**The missing axis is representational accuracy itself.** Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to anticipate. This paper's approach is a prototype answer on that axis, not a finished benchmark. [§7](#7-future-work) flags a differentiated rubric (one that separates interpretation-heavy from literal-recall questions, and scores epistemic honesty as its own dimension) as the priority follow-up for turning this prototype into a standardized benchmark.

**A single number does not capture a memory system's full capability.** Recall, survey-response prediction, persona fidelity, preference alignment, and representational accuracy are distinct axes. A system that saturates one may do nothing on another. Production-grade evaluation of memory systems should report results on multiple axes rather than on any single one.

### 2.2 Memory systems for LLM agents

The four commercial memory systems we evaluate (Mem0, Letta, Supermemory, Zep) have converged on a shared set of capabilities: semantic retrieval over embedded content, source attribution, multi-level memory structures, and benchmark-validated recall performance. They differ in how each of these is architected. None positions representational accuracy or behavioral prediction of a specific individual as a design target.

**Table 2.1. Memory system comparison.** Verified against primary sources.

| Provider | Core architecture | Retrieval method | Memory types | Published recall score |
|---|---|---|---|---|
| **Mem0** | Extract → consolidate → retrieve pipeline; Mem0g graph variant adds a directed labeled knowledge graph alongside the vector store | Hybrid: semantic + keyword + entity | Conversation, session, user, organizational | 91.6 LOCOMO, 93.4 LongMemEval (current algorithm)[^mem0-recall] |
| **Letta / MemGPT** | LLM-as-operating-system; virtual context management with main context plus external context | Archival via `archival_memory_search`; main-context memory blocks self-edited via `core_memory_append`, `core_memory_replace` | `persona` and `human` blocks in main context; archival and recall memory external | 74.0% on LOCOMO with GPT-4o-mini[^letta-recall] |
| **Supermemory** | Five-component architecture: chunk-based ingestion, relational versioning, temporal grounding, hybrid search, session-based ingestion | Hybrid with reranking and query rewriting; source chunks injected at retrieval | Contextual memories, relational versions, session data | 81.6% / 84.6% / 85.2% on LongMemEval_s with GPT-4o / GPT-5 / Gemini-3-Pro (self-reported) |
| **Zep** | Built on Graphiti (Apache 2.0, open source). Bi-temporal knowledge graph | Hybrid: semantic + BM25 + graph traversal | Episodes (ground-truth source), Entities, Facts-as-triplets with temporal validity windows | 71.2% on LongMemEval with GPT-4o[^zep-recall] |

[^mem0-recall]: Vendor-reported; evaluation harness open-sourced at `github.com/mem0ai/memory-benchmarks`. The peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini.

[^letta-recall]: Letta blog, 2025-08-12 (`https://www.letta.com/blog/benchmarking-ai-agent-memory`).

[^zep-recall]: Rasmussen et al., arXiv:2501.13956.

All four systems report recall scores in the 70-93% range; on the standard recall benchmarks, recall is approaching solved.[^benchmark-disputes] All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did. None of them takes representational accuracy, the property of interest to this paper, as an explicit design target.

Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is architecturally distinct: it is the only one whose core architecture treats memory as something an agent *synthesizes* during conversation rather than *stores* for later retrieval.[^letta-arch] This stateful-agent design is examined separately as a post-hoc case study in §4.5 (full case study in Appendix G), distinct from the archival-retrieval path Letta exposes for the main-study conditions. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four (Mem0, Supermemory, Zep) do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main-study configuration did not exercise (see §4.3 and §4.5).

[^letta-arch]: Letta's main context holds structured memory blocks (`persona`, `human`) that the agent edits during its inference loop via tools such as `core_memory_append` and `core_memory_replace`. External context includes archival memory (semantically searchable) and recall memory (prior conversation history). The other three systems (Mem0, Supermemory, Zep) follow extract-and-retrieve patterns characterized in Table 2.1; their per-vendor research pages and the Mem0 / Zep / Supermemory papers cited above hold the architectural details that did not carry into the body here.

[^benchmark-disputes]: The vendor-reported recall scores in this table are contested. Mem0 and Zep publicly disputed each other's LOCOMO methodology in `getzep/zep-papers#5` (closed 2025-05-19; Zep posted a corrected 75.14% ± 0.17 mean of 10 runs); Supermemory publishes head-to-head comparisons in its own favor; third-party reproductions (Vectorize.io) produce different numbers again. Methodology varies significantly between evaluators, and single-number comparisons across vendors should be read with caution. This paper does not adjudicate. We measure on a different axis (§4.4) and report against primary sources.

### 2.3 Traceability and Reasoning Traces

Traceability operates at two levels. **Fact-level traceability** answers where a retrieved claim came from. **Reasoning-level traceability** answers why the system believes this about this person. The four memory systems we evaluate provide the first; representing how a person reasons requires the second. This difference is load-bearing for the paper: representational accuracy operationalizes interpretation, and interpretation cannot be verified at the fact level alone. A system that represents how a person reasons must be auditable by that person, or the representation is a black box they cannot verify.

Zep has the strongest explicit fact-level provenance of the four: every entity and relationship traces back to the episode IDs that produced it. Supermemory returns source chunks alongside retrieved memories. Mem0 tracks ingestion provenance through timestamps. Letta exposes agent state and memory-block edit history rather than fact-level provenance.

The Behavioral Specification is structured so that every claim is a piece of reasoning, not just a piece of content. An axiom (for example, "A1: Dual-ledger authority") is an assertion about how the person reasons in a domain, grounded in the facts that imply it (F-001, F-047), which are themselves grounded in the exact source passages that produced those facts. Walking this chain backward gives the user a reasoning trace: *not only where a belief originated, but what line of reasoning connects the source text to the interpretive claim*.

**Worked example.** Sunity Devee, Question 4 (battery item, drawn from a held-out passage about her husband, the Maharajah, expressing disappointment over a missed opportunity). The structure below shows how a single response in the C2a condition (specification only: the model is given the Behavioral Specification and the question, with no retrieved facts and no source corpus) decomposes into a reasoning trace.

> **Subject:** Sunity Devee
>
> **Question:** *"When her husband expresses disappointment about missing an opportunity due to her concerns, does the narrator typically reconsider her position?"*
>
> **Held-out ground truth (full passage):** *"The Maharajah was disappointed, as he was anxious to go and see the old castle, and to shoot, and I deprived him of both these pleasures."*
>
> **Response (C2a, excerpt):** *"Based on the behavioral specification, the answer is no, not typically, and not in the way the question assumes. **A2 (Spiritual Integrity Over Social Cost)**^A2 and **A5 (Relational Identity)**^A5 create the relevant dynamic. A5 activates first: relational identity means his disappointment matters deeply. A2 holds firm: arguments from social consequence, including spousal disappointment, will not register as reasons on their own. Rather than reconsider the position itself, she is more likely to absorb the tension without resolving it (**P3 — Tension Absorbed, Not Expressed**)^P3 and reframe the disappointment within a spiritual logic (**A1 — Divine Primacy**)^A1, while grieving the relational cost without reversing the decision."*
>
> **Reasoning trace.** The response invokes four spec items in sequence:
> 1. **A5 (Relational Identity)** registers his disappointment as real, not dismissible.
> 2. **A2 (Spiritual Integrity Over Social Cost)** refuses social consequence as a reason to reconsider.
> 3. **P3 (Tension Absorbed, Not Expressed)** holds the conflict without resolving it in either direction.
> 4. **A1 (Divine Primacy)** reframes the disappointment within a spiritual logic.
>
> Each spec item grounds out in extracted facts that ground out in verbatim source passages. The user can walk the chain in either direction: from a phrase in the response, into the spec item that licensed it; from the spec item, into the facts that imply it; from the facts, into the source passages that produced them.
>
> **Referenced behavioral spec items** (from `data/global_subjects/sunity_devee/anchors_v4.md` and `predictions_v4.md`):
> - **A1 — Divine Primacy.** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame.
> - **A2 — Spiritual Integrity Over Social Cost.** Conscience and principle outrank social consequence as reasons.
> - **A5 — Relational Identity.** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible.
> - **P3 — Tension Absorbed, Not Expressed.** Conflicts between principle and relationship are held in place rather than collapsed in either direction.
>
> **Related facts** (from `facts.json`, each carrying its verbatim source-passage excerpt):
> - **F-73:** *"Sunity Devee's mother would never countenance anything her conscience told her was wrong."* (grounds A2)
> - **F-414:** *"Sunity Devee's father believed he acted as a public man guided by conscience and divine duty in accepting the marriage proposal."* (corroborates A2 from a different relational direction; conscience-as-master-frame pattern reinforced across both parents)
> - Additional facts grounding A1, A5, and P3 are referenced in the specification's anchor and prediction files; the full chain is enumerated in Appendix B.

The user can audit any step: read the response, look up each cited anchor or prediction by name, look up the facts that ground it, and read the source passages those facts came from. If a fact misrepresents the source, correcting it propagates through the spec on recomposition.

This matters because a person should be able to inspect the system's model of them, challenge any step in the reasoning, and correct it if it is wrong. A fact-attribution memory system lets the person audit what the system stores. A reasoning-trace specification lets the person audit what the system believes. The first is a feature. The second is the minimum bar for a representation that acts on someone's behalf.

### 2.4 Cognitive and representational foundations

**Six prior research directions shaped how we designed this paper's test.** Each motivates a specific choice about what to measure, what to compare against, or what failure mode to expect.

**Bartlett (1932)** established that human memory is reconstructive and schema-driven rather than literal playback. Reconstruction follows the organizing structures a person has built up over time, not a record of the original event. The Behavioral Specification is computationally analogous: a structured compression meant to carry the signal of a person's reasoning without storing every fact about them. We designed the specification with a schema-like architecture (anchors, core, predictions) precisely so we could test whether it does the work a human schema does: enable accurate anticipation of behavior in situations never encountered in the source data. Our 50/50 train/held-out split is the experimental realization of this question.

**Hinton et al. (2015)** showed that compressing a large neural network into a smaller one preserves "dark knowledge," the relationships between outputs that carry more information than the outputs themselves. This result motivates one of our central experimental comparisons: on matched token budgets, does a compressed interpretive artifact carry more predictive signal than the raw content it was derived from? The Hamerton condition in §4.2 (4,500-token spec vs. 33,000-token training corpus at 2.63 vs. 2.27 on the 5-judge primary panel) is a direct test of that question in the personal-representation setting.

**Chen et al. (2025)** (Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509) show that the character a model takes on (its "persona") is encoded in specific directions inside the model's internal numeric state, and that those directions can be identified, monitored, and nudged to shift the model's behavior in predictable ways. Their approach modifies the model; ours informs the model from outside via context. Both validate that persona is a real, manipulable structure: one reachable through the model's internals, the other through context. We chose the context route because it produces a portable artifact users can own and audit, which activation surgery does not. This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model.

**Jiang et al. (COLM 2025, arXiv:2504.14225)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The paper documents the failure empirically; our reading is that the cause is the gap between having facts and having the interpretive structure to apply them to new situations. Jiang's paper is the most direct existing evidence for the gap this paper studies, and our test design inherits from it: behavioral prediction on scenarios drawn from held-out text that the model has not seen, with all relevant facts retrievable, measures exactly the interpretive-application gap.

**Jain et al. (2025, arXiv:2509.12517)** find that adding conversation context to LLMs makes them more sycophantic: more likely to agree with the user even when the user is wrong (+45% on Gemini 2.5 Pro) and more likely to adopt the user's perspective on a question. Their result shows that context without the right structure pushes the model toward what the user appears to want rather than toward a grounded answer. This is why our experiment includes a wrong-spec control (§1.3 Mechanism): we hand the model a structured interpretive context that does not match the actual subject. If models drifted purely toward whatever context they are given, the wrong-spec should behave like any other structured prompt. Instead, the model either flags the mismatch explicitly (60.6% of responses) or attempts a low-quality application, neither of which is sycophantic drift. Jain's finding plus our wrong-spec result bracket the question from both sides: context shape matters (Jain), and content matters too (Base Layer's wrong-spec result, §4.3).

**Lu et al. (2026, arXiv:2601.10387)** identify what they call the Assistant Axis: a dominant internal direction that anchors assistant models' default behavior toward generic helpfulness and harmlessness. This default operates even when no specific user is involved. The Behavioral Specification can be read as an external override to the Assistant Axis on a per-user basis: a structured anchor that shifts the model from "generic helpful assistant" toward "reasons as this specific person would reason." This framing motivated our choice to measure hedging as a primary outcome alongside accuracy: if the spec shifts the model off the generic Assistant Axis, the behavioral change should show up both in what the model predicts and in what it is willing to commit to. Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the generic Assistant Axis produces hedging as a safe default, while a specific interpretive anchor enables commitment. The inference that hedging is downstream of the Assistant Axis is ours; Lu et al. identify the axis and leave the specific behavioral manifestations open.

## 3. Study Design

The experimental strategy holds the response model constant and varies the representation served as its context. Every condition in the study is a different choice about what that context contains: nothing (pretraining only), retrieved facts, raw corpus, a specification, or combinations of those. This isolates the contribution of the representation itself from model capability, provider, or fine-tuning regime. Each measurement choice ties back to a specific number reported in §4, and the statistical commitments were pre-locked before final analysis.

§3.1 through §3.6 describe the experimental apparatus: the property being measured, the subjects, the question batteries, the conditions, the response models, and the evaluation protocol. §3.7 describes the pipeline that produces the Behavioral Specification itself.

### 3.1 Operationalizing representational accuracy

Section 1.1 introduced representational accuracy as the AI-side property of interest. This section operationalizes the term so the rest of the methodology can refer to it precisely. **We use the term representational accuracy to describe how faithfully a model can act in line with a specific person when given a representation of that person.** The property is a joint claim across three components:

1. The person has behavioral patterns consistent enough to be captured in a representation.
2. The representation actually carries that signal.
3. A model given the representation can act on it.

Prediction on held-out situations is how we test all three at once.

The test works like this: held-out passages from a person's own writing serve as samples of situations the model has not seen. If the person's behavior is consistent enough to be captured and the representation actually captures it, the model should anticipate how the person would respond in those held-out cases. When it does not, one of three things is failing: the behavioral patterns are not consistent, the representation is wrong, or the model is not using the representation well. Each failure mode is informative.

We do not claim to modify the model's internal parameters. The Behavioral Specification is served as context: a lens through which the model can reason about a specific person. What we measure is whether that external lens is accurate enough that the model's responses reflect the person's own interpretation of the situation.

In practice, representational accuracy is operationalized as the mean predicted-behavior score (1-5 scale) across a standardized battery of 39 behavioral prediction questions, averaged across the five primary judges from two providers (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). Two Gemini judges (2.5 Flash and 2.5 Pro) are reported as a sensitivity check. The rubric is in §3.6. A guide to interpreting fractional scores at different ranges of the scale (what 2.9 vs. 3.2 indicates, what 1.5 vs. 2.0 indicates) is also in §3.6.

### 3.2 Subjects

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

**Franklin as a known-figure control.** Benjamin Franklin (Project Gutenberg #20203) is included as a known-figure reference point. Franklin's *Autobiography* is one of the most widely available and frequently cited autobiographies in American public-domain literature, and the model's baseline score on Franklin (3.77 on the 5-judge primary panel) is consistent with substantial pretraining representation of both the person and the specific text. We use Franklin as a reference point for what the high-baseline end of the spectrum looks like (§4.6.4), not as a subject whose representation is a design target of the specification itself.

**The baseline as an observable proxy.** The baseline score (C5, no-context prediction accuracy)[^baseline-rubric-pointer] is a direct empirical measurement: the response model's ability to predict behavior on a specific subject with no external help. On the 1-5 scoring rubric, a 1 is a refusal or off-base answer and a 5 closely matches the held-out passage. We treat that measurement as the observable proxy for the model's pretraining representation of the person. A baseline near 1.0 indicates the model has little to work from. A baseline above 3.0 indicates substantial pretraining representation. The 14 main-study baselines range from 1.03 (Sunity Devee) to 2.93 (Equiano); Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone; per-judge means across the available judges range from 3.475 to 4.275).[^franklin-judge-range]

[^baseline-rubric-pointer]: Rubric and aggregation rule defined in [§3.6](#36-evaluation-llm-as-judge-with-calibration).

[^franklin-judge-range]: Franklin's legacy run pre-dates the gemini_flash / gemini_pro split, so only one Gemini judge is present in the legacy data. The per-judge range cited here is the min and max across all available judges, rather than a clean 7-judge panel mean.

The baseline spread across the 14 subjects is direct empirical evidence that current response models hold uneven internal representations of specific people. The questions of which specific texts produced any subject's baseline, how the model organizes the representation internally, or what besides pretraining might influence the spread are outside this study's design. What the specification adds on top of the baseline is the question §4 tests.

**What we did not control for.** Language (all source corpora are English-language or English-translated); cultural framing (Western canon predominates in public-domain digitization); subject selection bias from Project Gutenberg's own curation history; era (oldest subject 4th-5th century, newest early 20th century); individual preferences in autobiographical self-presentation. These are acknowledged constraints on the generalizability of the 14-subject sample, not corrected biases.

### 3.2.1 Pretraining-coverage variance

Before turning to the specification's effect, the baseline itself is worth flagging as a finding. Response models vary widely in their pretrained capacity on a given person, even across a sample of subjects who all have public-domain autobiographies of comparable provenance.

| Baseline band | Subjects | Count |
|---|---|---|
| ≤ 2.0 (low-baseline slice) | Sunity Devee, Ebers, Hamerton, Fukuzawa, Seacole, Bernal Diaz, Keckley, Yung Wing, Babur | 9 |
| 2.0-3.0 (mid-baseline) | Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano | 5 |
| > 3.0 (high-baseline) | Franklin (known-figure control, not in main study) | 1 |

Nine of fourteen main-study subjects fall below 2.0, the "population of relevance" band that the typical AI user falls into, since most users' reasoning is not in any training corpus. Five subjects sit in the 2.0-3.0 band where the specification's effect is weaker and less consistent; two of them (Zitkala-Sa and Equiano) show small negative performance deltas when the specification is added (see §4.1 Table 4.1 and §4.6). Franklin at 3.77 (5-judge primary) anchors the high-baseline end and is a control, not a main-study subject.

This distribution matters for reading §4's results: the variance is not flat, and the specification's effect depends on where a subject sits on it. The higher a subject sits on this distribution (the better the model already knows them from pretraining), the smaller the specification's lift; at the high-baseline end, the specification tends to negatively affect representational accuracy rather than improve it. §4.1 develops this gradient explicitly.

### 3.3 Question Battery Formation

**Each subject's behavioral prediction battery is generated by a backward-design process: an LLM reads a passage from the held-out half of the corpus, writes a question whose answer is the behavioral pattern implicit in the passage, and deliberately avoids naming any detail unique to the passage itself. The question can be attempted from training-text patterns alone; the verbatim held-out passage is the ground truth for scoring.**

The procedure, in order:

1. **Split the corpus.** Each subject's source text is divided by chapter into `training.txt` (50% of the corpus) and `heldout.txt` (50%). Held-out text is never shown to a response model.
2. **Sample from held-out.** A sliding window moves across the held-out text in four batches of ten questions each, using 5,000-character windows as local context.
3. **Backward-design question generation.** Claude Haiku 4.5 (temperature 0) reads each held-out window and writes a question whose answer requires the subject's behavioral patterns observable in the training half. The prompt extracts a verbatim ground-truth span from the held-out window and forbids named-entity or specific-date leakage in the question stem.
4. **Supplementary tiers.** Four additional question categories (factual, situational, and others) are generated from training text alone and included in the battery but not scored in the main results.
5. **Dedup and freeze.** Deduplication on lowercased question text, cap at target counts per category, MD5 checksum of the final battery. Downstream response and judgment files are invalidated if the battery checksum changes.

Each main-study subject receives 39 behavioral prediction questions; Franklin's legacy battery has 40. The total behavioral-prediction pool is 586 questions across 15 subjects (14 main-study plus Franklin). Each battery covers 8 to 10 of the 10 fixed behavioral-prediction categories: decisions, values, relationships, conflict, learning, risk, creativity, stress, career, and change-over-time. Definitions, example questions, and per-subject distributions are in Appendix B.1 and B.2.

**Leakage audit.** We empirically checked the backward-design no-leakage principle by searching every behavioral-prediction question for any sequence of seven or more consecutive words that appears verbatim in that subject's held-out corpus. Across the 14 main-study subjects (546 questions total), 0 questions leak (true zero, not a rounded value). Across Franklin's 40-question legacy battery, 2 questions leak (Q49 and Q56), which predate the backward-design constraint and were hand-authored. Aggregate across the full 586-question pool: 2 leaks (0.34%). We disclose Franklin's leaks here; Franklin's role in the paper is as a high-baseline reference, not as a subject whose quantitative result is load-bearing.

**Separately, a false-premise outlier.** A post-hoc review of spec-induced refusal cases surfaced one Zitkala-Sa battery question (Q18) whose premise is factually wrong: it asks how Zitkala-Sa would demonstrate acceptance of fate when facing execution, but Zitkala-Sa was never executed. Response models reasonably reject the question on its premise rather than answering; the Haiku-generated backward-design prompt produced a malformed item. This is one question out of 586 (0.17%), does not affect any aggregate claim in the paper, and flags a broader limitation we carry into §6: automated backward-design batteries are not a substitute for hand-curated review on every item, and scaling the methodology should include a human-reviewed quality gate.

Raw battery data is available in the public repository at `results/global_<subject>/battery_v2.json` for the 13 global subjects; Hamerton and Franklin legacy batteries at `data/<subject>/battery.json`. GPT-5.4-regenerated batteries (used in the circularity control, §3.3.1) are at `results/global_<subject>/battery_gpt54.json`. The leakage-audit script is at `scripts/_verify_battery_leakage.py`.

### 3.3.1 Circularity controls

**The pipeline and the batteries both use Anthropic models for multiple roles: Haiku for extraction and battery generation, Sonnet for authoring, Opus for composition, Haiku as the primary response model, and both Sonnet and Opus on the judge panel. To test whether results are an artifact of this within-Anthropic frontier-model chain, we ran two independent circularity controls.**

**Control 1: Independent battery regeneration (GPT-5.4).** We independently regenerated behavioral prediction batteries for all 13 global subjects using GPT-5.4 with the identical backward-design prompt used for the primary Haiku-generated batteries. The regenerated batteries produced the same 39-question count per subject, covered the same 10 behavioral categories (with 8-10 shared per subject), and targeted the same behavioral patterns in the source text. Emphasis differed by category: GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions. The backward-design methodology constrains the output more than the generating model does. Franklin and Hamerton retain their legacy batteries and are not part of Control 1; the 13 global subjects are. Full GPT-5.4 batteries are released for independent replication at `results/global_<subject>/battery_gpt54.json`.

**Control 2: Non-Anthropic response chain.** We re-ran the core conditions[^core-conditions] on three subjects spanning the effect gradient (Ebers at baseline 1.04 with a strong positive effect, Yung Wing at baseline 1.88 with a modest positive effect, and Zitkala-Sa at baseline 2.34 with a negative effect) using two non-Haiku response models (Claude Sonnet and Google Gemini Pro) reading the GPT-5.4-generated batteries. The combination gives us subject × response-model × battery cells that together test whether the specification effect survives when both the response model and the battery-generation model are outside the Anthropic family. Full results are in §4.6.1.

[^core-conditions]: C5 no-context baseline, C2a specification alone, C4a facts-plus-specification, C2c wrong-specification control. Full condition definitions in §1.2.

Together the two controls address within-Anthropic circularity at two levels. Control 1 holds the response model constant and varies the battery-generation model, testing whether the specification effect depends on Haiku writing the test questions. Control 2 holds the battery constant and varies the response model, testing whether the effect depends on Haiku reading and answering them.

A broader LLM-as-judge circularity, the concern that any LLM panel might systematically favor LLM-produced outputs over human-written alternatives, is not addressed by these controls. It is discussed as an open limitation in §6.[^circularity-data]

[^circularity-data]: Raw battery regeneration data is at `results/global_<subject>/battery_gpt54.json` for all 13 global subjects. Tier 2 response and judgment files for the three subjects tested are in the same per-subject directories.

### 3.4 Experimental conditions

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

**Letta stateful-agent path.** Letta exposes two memory modes: archival retrieval (the path tested in C1 / C3 above) and a stateful-agent path where memory blocks are edited incrementally during ingestion and the agent reads from the block directly. The stateful path is architecturally distinct from retrieval-style access and is evaluated as a separate comparison, reported in §4.5 alongside other Letta findings rather than as a top-line condition row.

**Wrong-spec control.** C2c has two variants: v1 (adversarial fixed pairing, each subject assigned a culturally and temporally distant other's specification) and v2 (random derangement, seed-fixed at 42, so no subject receives its own). v2 is the standard randomization control; v1 is an adversarial stress test designed to maximize the wrong-spec effect by construction. Both are reported in §4.3, with v1 headlined for the stronger evidence of content effect; sensitivity analysis on the protocol choice in §4.6.4. We do not use a uniform Franklin-as-wrong-spec variant, which would risk leaking canonical Western framing into the comparison.

Detailed per-condition parameters, exclusion cases, and ingestion specifics are in Appendix C.[^conditions-data]

[^conditions-data]: Raw data is available in the public repository at `results/global_<subject>/results_v2.json` (all direct-context conditions for the 13 global subjects) and `results/global_<subject>/<system>_results.json` / `<system>_fullpipeline_results.json` for per-system controlled / native configurations (`<system>` ∈ {mem0, letta, supermemory, zep, baselayer}). Hamerton responses live at `results/hamerton/` and Franklin at `results/franklin/` with per-judge judgments at `results/franklin_legacy_20260411/analysis/`.

### 3.5 Response models

**Tier 1 (main study): Claude Haiku 4.5 as the primary response model, run across all 14 subjects and every condition in the main matrix. Haiku was chosen because effects that register on the weakest available model give the most conservative estimate of the spec's contribution; §4.6.1 Tier 2 cross-provider probe checks whether the direction holds on stronger response models.**

**Tier 2 (cross-provider directional probe).** To test whether the specification effect depends on the response model being within the Anthropic family, Claude Sonnet 4.6 and Google Gemini 2.5 Pro were additionally run as response models on 3 subjects spanning the effect gradient (Ebers, Yung Wing, Zitkala-Sa) against the GPT-5.4-regenerated batteries from Control 1. Tier 2 results and subject-selection rationale are in §3.3.1 and §4.6.1.

**Call-time parameters.** All response models are called with `temperature=0` and `max_tokens=1024`.

**Prompt schema.** A single shared prompt is used across every condition. The system message frames the task as behavioral prediction of a specific person; the user message is the question plus whichever context inputs the condition specifies (§3.4). Nothing about the prompt changes per condition beyond the injected context block.

```
System: You are predicting how <subject> would respond to a specific
        question about their behavior, values, or reasoning. Answer
        in <subject>'s voice, grounded in their demonstrated patterns.

User:   <context block, one of: empty (C5), spec (C2a), wrong spec (C2c),
         facts (C4), facts + spec (C4a), corpus (C8), corpus + spec
         (C9), or retrieval ± spec (C1 / C3)>

        Question: <question text>
```

No prompt instruction tells the model to abstain, answer, hedge, or commit. That was a design decision made at the start of the study. Any prompt that coached response behavior would have directly confounded what the conditions are trying to measure, and the model's natural refusal-or-commitment pattern given a specific context is itself part of the phenomenon the study tests. §4.3 reports the hedging-rate shift across conditions and treats it as a substantive finding rather than a behavior to suppress.

**The "grounded in demonstrated patterns" framing.** The system message names the task as behavioral prediction and frames the output as grounded in the subject's patterns. This is task framing rather than hidden bias: the entire study tests whether the served context lets the model do exactly what the prompt describes. The framing is identical across every condition, so whatever priming it introduces is a constant; the differential effect the study measures (spec vs no spec, correct spec vs wrong spec) is what the conditions vary. A more neutral prompt schema, without the "grounded in demonstrated patterns" framing, is a future-work robustness check.

**What the conditions actually vary, then, is where the patterns come from.** C5 asks the model to extract patterns from pretraining alone. C4 and C8 provide raw material (extracted facts or full corpus) and ask the model to identify and apply patterns at runtime. C2a hands pre-extracted patterns directly. C4a and C9 combine pre-extracted patterns with raw material. C2c serves wrong patterns. The framing is constant; what varies is what the model has to ground in. The empirical evidence is consistent with the prompt not being the lift mechanism: C5 (same prompt, no context) stays low at 1.03 to 2.93 across the 14 main-study subjects, C2c (same prompt, wrong content) scores below baseline at Δ = −0.25 on adversarial pairings, and C8 with the full corpus matches but does not exceed C2a at roughly one-fifth the tokens. In other words, giving the model the patterns ahead of time outperforms asking it to find those patterns on its own at the moment of answering, even when the raw material is much larger than the specification. What the Behavioral Specification provides specifically is structured behavioral content: axioms encoding how the person reasons in domains, core values, predictions of forward behavior, and a unified brief synthesizing them (§3.7). The C2a vs C8 / C4 comparison is a direct test of whether this pre-extracted axiom-based content outperforms the model's runtime extraction from raw material.

Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in Appendix C.[^response-scripts] [^response-data]

[^response-scripts]: The same information is present in the released code at `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, and `scripts/run_multimodel_responses.py`.

[^response-data]: Raw response files are in the public repository at `results/global_<subject>/results_v2.json` for the 13 global subjects, `results/hamerton/results.json` and `results/franklin/fullstack_haiku.json` for the legacy subjects, and `results/_tier2/` for the Tier 2 runs.

### 3.6 Evaluation: LLM-as-judge with calibration

**Every response is scored 1-5 by seven LLM judges against the verbatim held-out ground-truth passage.** Human annotation at this scale is feasible (roughly 14 subjects × 40 questions × 15+ conditions, on the order of thousands of judgments) but was not done; running more conditions and more judges instead is the central evaluation trade-off of this prototype framework. How we work inside that trade-off is what this section describes.

**The evaluation is deliberately recursive.** Response models are evaluated by judges (§3.6.1). Judges are evaluated by calibration diagnostics (§3.6.3), inter-judge agreement metrics (§3.6.4), and post-hoc rubric-handling audits (§3.6.6). No single layer is treated as ground truth; each layer's behavior is itself measured and disclosed, and where a layer's behavior diverges from what the rubric intends, the divergence is flagged rather than corrected silently. The paper's rigor in the absence of human annotation comes from this stacked-instrument structure, not from trusting any one step.

**Scoring rubric.**

| Score | Meaning |
|---|---|
| 1 | Refusal or off-base prediction |
| 2 | Generic, not subject-specific |
| 3 | Partially captures the subject's behavioral pattern |
| 4 | Substantively captures the pattern on multiple dimensions |
| 5 | Captures the behavioral pattern observable in the verbatim held-out ground-truth passage |

Each response is scored against the verbatim held-out passage from which the question is drawn; the score reflects how closely the response matches the documented behavioral pattern. Condition identifiers (C5, C2a, C4a, C3) refer to the conditions defined in §3.4 and summarized in Appendix C; rubric anchor numbers 1 through 5 refer to the table above. A worked example with real responses scored across the rubric anchors is presented alongside the analysis of when the no-context baseline engages versus abstains in [§4.1.1 Per-question baseline engagement and the worked rubric example](#411-per-question-baseline-engagement-and-the-worked-rubric-example); full per-subject score distributions with verbatim responses are in [Appendix D](#appendix-d-validity-audit-and-score-distributions).

**Reading score differences.** Each anchor crossing reflects a categorical shift in response quality. A move from 2 to 3 is the difference between a generic answer that could apply to many subjects and one that identifies a subject-specific behavioral tendency. A move from 3 to 4 is the difference between identifying one behavioral tendency and identifying several that work together. A move from 4 to 5 is the difference between substantively-correct multi-dimensional pattern capture and alignment with the specific behavior in the held-out passage. §3.6.2 develops the formal cross-anchor rule used throughout the results section.

**What a 5 means and does not mean.** A score of 5 reflects alignment with one specific behavioral sample: the held-out ground-truth passage the question is drawn from. It is not a claim that the response fully represents the subject in some absolute sense, and it is not a claim that the same response would score 5 on a different held-out passage from the same subject. Each question tests one behavioral sample at a time; the aggregate across roughly 40 questions per subject is what the paper reads as the subject-level score.

### 3.6.1 Judge panel

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

The panel is calibrated for directionality, not absolute precision. Whether a Behavioral Specification steers responses toward the subject's documented patterns is the directional question the panel is built to answer; §3.6.3 (calibration) and §3.6.4 (inter-judge agreement) measure how reliably it does.

### 3.6.2 Score interpretation

Scores are read at three related granularities: integer rubric anchors (1 through 5), fractional means produced by averaging across the 5-judge primary panel (e.g., 2.87, 3.12, 2.34), and crossings between integer anchors when conditions change. Fractional shifts should be read through the integer anchors, because each anchor corresponds to a categorical shift in response quality.

**The *cross-anchor interpretation rule*. A fractional delta that crosses an integer anchor reflects a real shift in the underlying response distribution. A delta that stays inside a single anchor is a within-category shift and a weaker claim.**

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

**Multi-anchor crossings: the strongest categorical signal the rubric detects.** A *multi-anchor crossing* is a single question whose 5-judge primary mean shifts across two or more integer rubric anchors when the condition changes. Crossings can span two bands (e.g., 1 → 3 or 2 → 4) or, more rarely, three bands (e.g., 1 → 4 or 2 → 5); larger crossings indicate larger categorical jumps in the same response. These crossings show that for some questions, adding the specification (or another high-information condition) does not produce a small directional nudge but a categorical jump of multiple bands, with five independent judges converging on the move. Examples spanning two-band and three-band crossings:

- Seacole Q2 C4 (facts) at 2.80 → C4a (facts + spec) at 5.00: crosses anchors 2 / 3, 3 / 4, and 4 / 5. Generic empathic engagement under facts alone becomes a response that aligns with the held-out behavioral pattern under facts plus specification. Three-anchor category change.
- Hamerton Q25 C8 (raw corpus) at 1.40 → C9 (raw corpus + spec) at 4.20: crosses anchors 1 / 2, 2 / 3, and 3 / 4. Refusal or off-base prediction under raw corpus alone becomes a multi-dimensional, subject-specific response under raw corpus plus specification. Three-anchor category change.
- Bernal Díaz Q16 C4 (facts) at 2.00 → C4a (facts + spec) at 4.80: crosses anchors 2 / 3 and 3 / 4. Generic engagement under facts alone becomes a multi-dimensional, subject-specific response under facts plus specification. Two-anchor category change.

§4.2 reports the rate at which these crossings appear in each condition pair and discusses the response-level phenomena that produce them.

**The paper applies this rule consistently.** Score deltas reported in §4 are read through this lens. A +0.50 delta that crosses a rubric anchor is treated as a stronger claim than a +0.50 delta that does not.[^anchor-crossing-data]

[^anchor-crossing-data]: Per-subject anchor-crossing data at `docs/research/s114_anchor_crossing_examples.json`; computing script at `scripts/compute_anchor_crossing.py`.

**The rubric also detects movement that doesn't cross an integer anchor.** In addition to the integer-anchor crossings reported throughout §4, an additional ~18% of paired questions across the 18 condition pairs analyzed[^within-band-data] show same-band fractional shifts of at least 0.5 rubric points. The 5-judge primary panel detects sub-anchor signal cleanly: direction-agreement among judges is 74% at panel |Δ| of 0.1 to 0.25 and 93% at |Δ| of 0.25 to 0.5. The integer metric is used throughout for cross-anchor categorical interpretation; the sub-anchor signal is reported here as methodological transparency.

[^within-band-data]: Within-band shift data at `docs/research/within_band_shifts_20260428.json`.

### 3.6.3 Calibration

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

**Use of calibration data.** Scores are not normalized. Any normalization requires deciding which judge's profile is "correct" and re-scaling the others toward it. Calibration data is published in its raw form so readers can apply their own normalization if they prefer.

**Primary aggregate: 5-judge (non-Gemini) panel.** The primary numeric aggregate reported throughout [§4](#4-results) is the 5-judge mean using Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, and GPT-5.4. The two Gemini judges (Gemini 2.5 Flash, Gemini 2.5 Pro) are excluded from the primary aggregate and reported as a sensitivity check instead. The calibration table above shows Gemini Pro failing the verbatim-match diagnostic (4.15 where every other calibrated judge scores 5.00) and penalizing padded-correct responses severely (dropping from 5.00 on short correct to 1.20 on long correct). Gemini Flash shows smaller but consistent length sensitivity. A judge that cannot recognize verbatim ground-truth as a 5 is a known-unreliable instrument on this task. Including known-unreliable judges in the primary aggregate inflates or deflates effect-size numbers in ways that do not reflect the underlying response quality. Excluding them from the lead number, while keeping them available as a sensitivity check, preserves the provider-diversity argument (the final conclusions are stable whether or not the Gemini judges are included) without leading with a known-flawed aggregate.

The 7-judge aggregate is reported as a sensitivity check. Where the 7-judge and 5-judge aggregates produce materially different numbers, both are given and the delta is discussed. Every primary finding in §4 is stable across both aggregates (robustness confirmed in §4.6).

**The 5-judge primary is the conservative choice.** On the main gradient and spec-effect conditions, including the two Gemini judges produces *larger* spec-effect deltas, not smaller ones: on the 13 global subjects, the mean improvement from specification-alone (C2a) over no-context baseline (C5) rises from +0.35 on the 5-judge primary panel to +0.45 on the 7-judge aggregate, a +0.10-point widening driven by Gemini inflation compressing baseline scores more than spec-condition scores. The same direction holds across wrong-spec, facts-only, and facts-plus-spec aggregates. Reporting 5-judge primary means every headline effect size is the lower bound that remains once the most-inflationary judges are removed from the aggregate.

**How raw scores are read in §4.** Raw scores are treated as directional rather than absolute; deltas between conditions carry more information than levels; deltas that cross a rubric integer anchor (§3.6.2) are treated as stronger claims than deltas staying inside a single integer band. Raw calibration data is in the public repository at `results/judge_calibration/`.

### 3.6.4 Inter-judge agreement

**The *specification-effect claim*.** When a Behavioral Specification is served to the model as context, the model's responses shift in the direction of the subject's demonstrated behavioral patterns, and that shift registers as a measured increase in representational accuracy against held-out passages from the same subject. This is the directional claim the judges in this section are measuring. The claim is not that the model has gained a new behavioral-prediction capability, and it is not that the higher-scoring response is the absolute "correct" answer for the subject. Two complementary agreement measures answer different questions about whether judges detect the shift consistently: direction and absolute magnitude.

**Direction agreement: pairwise Spearman ρ.** Spearman ρ measures whether two judges rank the same set of items in the same order. ρ = 1 is perfect ranking agreement; ρ = 0 is no rank agreement; ρ ≥ 0.8 is conventionally treated as strong rank agreement.

For each pair of judges in the 5-judge primary panel (10 pairs across Haiku, Sonnet, Opus, GPT-4o, GPT-5.4), pairwise Spearman ρ ranges from **0.86 to 0.93**.[^spearman-7judge] The five primary judges agree on the ranking of conditions: whatever any individual judge's absolute calibration quirks, they converge on which conditions produce better responses. For the directional claim (is the specification steering responses in the right direction?), this is the statistic that matters.

[^spearman-7judge]: Spearman ρ from 0.29 to 0.93 across the 7-judge / 21-pair set, driven down by the two Gemini judges' partial coverage and inflation behavior. Full matrix in `docs/research/stats_update.md` §5.

**Magnitude agreement: Krippendorff α (ordinal).** Krippendorff α measures whether judges give the same response the same numeric score (not just whether they rank items in the same order). α = 1 is perfect agreement; α = 0 is no better than chance; α < 0 is systematic disagreement. Krippendorff's guidance cites α ≥ 0.8 as high reliability and α ≥ 0.667 as substantial reliability.

The 5-judge primary panel scores **α = 0.659**, just below the substantial-reliability threshold. The 7-judge panel including the Gemini judges drops to **α = 0.535**. This drop reflects the systematic +1-point Gemini inflation: Gemini judges score responses about one point higher on average than the five primary judges, so absolute values disagree even when rankings match. This is why the calibration audit (§3.6.3) excluded the Gemini judges from the primary aggregate.

The α value places a ceiling on how precisely any individual fractional score should be read, which is why the paper treats per-subject deltas that stay inside a single rubric band as weaker than deltas that cross one.

**What the panel is not.** The panel does not establish that any higher-scoring response is the absolute correct answer for the subject; that determination requires human annotation against the subject's actual writing, which we do not have. What the panel provides is cross-provider directional convergence: three independent providers' models agree that the specification is moving responses in the same direction. We treat that as sufficient for a directional claim, no stronger.

Raw agreement matrices are at `results/interjudge_agreement/`.

### 3.6.5 Aggregation

The aggregation rule was fixed before any results were computed. Below is the three-step procedure:

1. Within each judge, mean score across all questions for each (subject, condition) cell.
2. Mean across the five primary judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). A separate 7-judge mean including Gemini Flash and Gemini Pro is computed and reported as a sensitivity check.
3. Unit of inference: subject.

Mean was chosen over median and trimmed mean. Median discards information when judges cluster tightly, which the Spearman ρ = 0.86-0.93 agreement shows they do. Trimmed mean requires an arbitrary trim threshold. Simple mean preserves every judge's contribution, and the Gemini inflation is handled by the primary-vs-sensitivity split rather than by silent correction.

### 3.6.6 Rubric-handling limitations (validity audit)

A direct inspection of the response text against the 5-judge primary scores surfaced two rubric-handling limitations that any reader of the §4 numbers should keep in mind.[^validity-audit-script]

[^validity-audit-script]: Both limitations were identified by a post-hoc audit. Audit script: `scripts/audit_low_end_inflation.py`. Numeric breakdowns below are produced by the script directly. Raw per-response classifications live in the judgment and response JSONs under `results/global_<subject>/` for independent reproduction.

**Refusals are not cleanly distinguished from wrong predictions.** The rubric's lowest anchor, "refuses or off-base," lumps together two different behaviors: an honest refusal to answer when the context does not support a prediction, and a substantively wrong prediction. We call the first behavior a *refusal* (or, equivalently, an *abstention*).

Across 192 responses identified as refusals (matched by phrases like "no specific information," "I cannot confirm," "would need additional context") in the low-baseline slice, 82.8% scored in the 1.0–1.5 band as expected, but 9.4% scored at or above 2.0 and 3.1% scored at or above 3.0. The mean refusal score is 1.27. Judges sometimes give refusals scores of 2 or 3 instead of 1, especially when the refusal recites related facts or names what is missing from the context.

The effect runs in both directions. A refusal can score above 1 if it includes adjacent facts (Seacole Q2 at 2.80). A spec-driven response that explicitly flags its own uncertainty can also score above its substantive content (Hamerton Q21 at 4.00 under spec-induced abstention).

**Verbose responses are scored more generously than short refusals.** Across 1,599 responses, length and score correlate at r = 0.26 overall, but the correlation is concentrated almost entirely in C5 (responses with no provided context; r = 0.60). Spec-containing and facts-containing conditions show near-zero correlation.[^length-by-condition] Three behaviors drive the C5 pattern:

- **Hedging.** Phrases like "I'm not sure but..." or "There may be cases where..." extend response length without adding predictive content.
- **Adjacent-fact recitation.** Listing related facts the model holds but does not use to directly answer the question, padding the response without engaging the question itself.
- **Disambiguation offers.** Phrases like "Are you asking about X or Y?" which the rubric treats as engaged responses when they are actually non-answers.

[^length-by-condition]: Per-condition Pearson r: C2a (spec only) 0.14, C4 (facts only) 0.01, C4a (facts + spec) −0.01. Length inflation is not a general phenomenon across the rubric: ultra-high responses (score ≥ 4.5) are not longer than mid-range responses on average (2,790 chars vs. 2,829 chars).

**Per-judge strictness on refusals.** Sonnet is the strictest judge on refusal responses, Opus the most lenient.[^per-judge-strictness] No single judge is universally strictest; the 5-judge primary mean smooths these differences without eliminating them.

**Per-response-model abstention behavior.** The 9.4% / 3.1% pooled over-credit rates above average over three response models. Disaggregating along that axis (abstention identified by 27-marker regex):

| Response model | N | Abstain rate | Mean abstain score | % ≥ 2.0 |
|---|---:|---:|---:|---:|
| Claude Haiku 4.5 (main study) | 13,380 | 7.5% | 1.38 | 14.3% |
| Claude Sonnet 4.6 (Tier 2) | 468 | 21.2% | 1.62 | 26.3% |
| Gemini 2.5 Pro (Tier 2) | 420 | 0.5% | 2.63 | 100.0% |

Sonnet 4.6 abstains at roughly three times Haiku's rate and the panel rewards its abstentions nearly twice as often (26.3% ≥ 2.0 vs. 14.3% ≥ 2.0); mean abstain score is 0.24 anchor points higher. Sonnet's hedged abstentions tend to recite plausible behavioral framings before disclaiming, and the panel scores the framing rather than the disclaimer. Gemini 2.5 Pro almost never abstains by these markers (n = 2); its row is for completeness only. *Haiku 4.5, the main-study response model, is the lowest over-credit case.* The pooled 9.4% / 3.1% numbers are therefore a *floor*, not a worst case; stronger response models that hedge more elaborately extract more lift from the panel's reluctance to score abstentions at 1.0.

**Memory-system effect on abstention.** A separate per-question audit tested whether memory-system retrieval inflates refusal scores via *visible fact recitation* (refusing in substance but quoting retrieved n-grams). It does not. Memory-system refusals score +0.21 to +0.23 anchor points higher than pure no-context refusals at the condition level (Welch *p* = 0.0001), but the lift is the same whether or not the response recites a retrieved n-gram (Δ = +0.027, *p* = 0.67).[^memsys-abstention] The over-credit is a "judges reward the retrieval condition" effect, not a "judges reward the visible quote" effect. Either judges infer that retrieval-conditioned answers are more grounded even when abstaining, or abstention text in retrieval conditions is systematically less terse and the panel scores the framing.

[^memsys-abstention]: Cell counts and Welch comparisons. Pure no-context refusal (n = 292): mean 1.26, 10.3% ≥ 2.0. Facts-only refusal (n = 20, underpowered): mean 1.33, 10.0% ≥ 2.0. Memory-system refusal + recitation (n = 148): mean 1.50, 18.2% ≥ 2.0. Memory-system refusal, no recitation (n = 240): mean 1.47, 17.1% ≥ 2.0. Memory-system substantive engagement (n = 7,835): mean 2.32, 67.2% ≥ 2.0. Comparisons: mem-refuse + recite vs. pure no-context refuse, Δ +0.234 [+0.113, +0.355] *p* = 0.0002; mem-refuse no recite vs. pure no-context refuse, Δ +0.206 [+0.103, +0.310] *p* = 0.0001; mem-refuse + recite vs. mem-refuse no recite, Δ +0.027 [−0.098, +0.153] *p* = 0.67.

[^per-judge-strictness]: Per-judge mean refusal score: Sonnet 1.14, GPT-5.4 1.17, Haiku 1.29, GPT-4o 1.34, Opus 1.41. Spread of 0.27 points top-to-bottom.

**What this means for the reported effects.** Both effects raise C5 baseline scores more than they raise spec-condition scores; the true spec-vs-baseline gap is therefore very likely larger than the +0.89 mean lift we report, not smaller. We report the measured number and flag the direction of bias rather than recompute under a modified rubric, to keep the analysis plan lock intact. §7 Future Work proposes a differentiated rubric that scores refusal as its own dimension and a length-controlled scoring protocol.

The class-level LLM-as-judge limitation that this methodology cannot fully address is treated in §6.2.[^judgments-data]

[^judgments-data]: Raw per-judge judgments are in the public repository at `results/global_<subject>/*_judgments_<judge>.json` (and `judgments_v2.json` for the merged v2 set) for the 13 global subjects, `results/hamerton/*_judgments_<judge>.json` for Hamerton, and `results/franklin/*_judgments.json` plus `results/franklin_legacy_20260411/analysis/*_judgments.json` for Franklin. Memory-system per-judge judgments live at `results/global_<subject>/<system>_judgments_<judge>.json` (controlled) and `results/global_<subject>/<system>_fullpipeline_judgments_<judge>.json` (native) in the same flat per-subject directory.

### 3.7 Base Layer Pipeline for the Behavioral Specification

**The pipeline transforms raw source text into a Behavioral Specification in four content-production steps: extract, embed, author, and compose. An import step normalizes the source data before extraction.** Each step is a single script backed by a single model choice. Total cost per subject is under $1.

| Step | Input | Tool / model | Output |
|---|---|---|---|
| 1. Import | ChatGPT / Claude exports, journals, plain text, directories | `import_conversations.py` | A local database holding the cleaned, de-duplicated source text |
| 2. Extract | Canonical source text | `extract_facts.py`, Claude Haiku 4.5, 46-predicate vocabulary | Behavioral patterns extracted as short structured statements (e.g., "avoids confrontation," "values craft over speed"), with bookkeeping operations to add new patterns, update existing ones, delete contradicted ones, or skip duplicates |
| 3. Embed | Extracted facts | `embed.py`, `all-MiniLM-L6-v2`, ChromaDB | A searchable index mapping each fact back to its source passage, enabling provenance tracing and retrieval |
| 4. Author | Extracted facts + embeddings | `author_layers.py`, Claude Sonnet 4.6 | Three interpretive layers as markdown (anchors, core, predictions); see body below for layer-by-layer examples. Each layer is produced from facts alone, not from prior layer output. Each layer prompt includes a domain guard that prevents topic skew (ablation-validated in prior pilot work). |
| 5. Compose | The three authored layers | `agent_pipeline.py`, Claude Opus 4.6 | Unified behavioral brief in flowing prose; see body below for what the brief contains and why it exists |

The artifact served as context in experimental conditions (referred to throughout the paper as "the Behavioral Specification") is the three authored layers concatenated with the composed brief, not the brief alone. Total size per subject is approximately 7,000 tokens, roughly 5,000 words (about the length of a short magazine article).

The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: `avoids`, `repeatedly engages in`, `refuses to`, `values`, `fears`, `has experienced`). The full predicate list is in [Appendix A](#appendix-a-predicate-vocabulary). The vocabulary is human-curated and was validated across 50+ pilot subjects before being frozen for the study. The constrained vocabulary is the main lever the pipeline uses to push extraction away from biographical facts ("his father was violent") and toward behavioral patterns ("evaluates authority figures on dual criteria of virtue and failure").

The three authored layers have distinct jobs. Each layer has a characteristic format; examples below are drawn from the Hamerton specification.

**Anchors** encode the subject's load-bearing axioms in numbered form (A1, A2, ...), each with an activation condition and a false-positive warning. Example:

> *A1. DUAL-LEDGER AUTHORITY: Evaluates authority figures on virtue and failure simultaneously, refusing to collapse them into a single verdict. Active when: encountering teachers, mentors, or institutional power. False positive: do not apply when the authority figure is a peer or subordinate.*

**Core** captures values, beliefs, and self-view in flowing prose. It is the layer that reads most like an essay about the person. Example:

> *Treats aesthetic sensibility and moral seriousness as inseparable. The quality of attention a person brings to beauty is, for him, direct evidence of the quality of attention they bring to anything else. This belief predates his career in art criticism and survives intact across every phase of his life.*

**Predictions** are explicit behavioral predicates (P1, P2, ...) with detection criteria, directives, and false-positive warnings. Example:

> *P3. Environment-as-cognition. Classifies new environments as generative or hostile to contemplative work before engaging with their particulars. Detection: immediate evaluative language about the environment itself, not about the people or tasks in it. Directive: model an immediate and durable classification rather than gradual adjustment. False positive: do not apply when the environment is a neutral logistical setting.*

**The unified brief.** The compose step integrates the three authored layers into a unified prose brief: a continuous, reader-facing synthesis written in the third person, similar in length and structure to a short profile of the subject. It reads as if a writer absorbed the layered specification and re-told it in narrative form. The brief exists for two reasons. First, it gives a human reader a coherent first pass on the subject before drilling into the structured layers. Second, composing the three layers into a unified brief implicitly weaves them together. The brief enforces an integration step that the layered files alone do not require, and internal testing suggests this integration can change how a model uses the specification. A formal ablation isolating brief-with-layers vs. layers-only is flagged in [§7.3 Specification design and composition](#73-specification-design-and-composition).

Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80) to process a 50,000- to 150,000-word autobiography end to end. Pipeline code, the full predicate vocabulary, and example specifications for all 14 study subjects are available in the public repository (see [§8 Data, code, and reproducibility](#8-data-code-and-reproducibility)).

---

## 4. Results

Across 14 historical subjects, adding a Behavioral Specification (a short structured document describing how a specific person reasons and behaves) measurably improves how accurately a language model represents that person's behavioral patterns. We measure this with a battery of behavioral prediction questions based on held-out ground-truth text from each subject's publicly available autobiography. We score each prediction on a 1-to-5 rubric where a whole-point shift marks a categorical change in how the response aligns with the subject's documented behavior. On the 9 low-baseline subjects (those the model does not know well), the specification produces a mean per-subject increase of **+0.89 points** and lifts individual responses by one category or more on **55.0% of questions**. The specification's added value on top of other context types (facts, raw corpus, or memory-system retrieval) concentrates on interpretation-heavy questions; on factual-recall questions, retrieval alone is often sufficient and the specification adds little or actively degrades the response. On high-baseline subjects (those the model does know well, such as Benjamin Franklin), the specification adds little or mildly hurts across conditions. Control conditions, statistical robustness checks, and sensitivity analyses confirm that the specification categorically shifts how a language model responds, increasing its ability to hold an accurate representation of the subject beyond what pure fact-based retrieval can supply.

The seven parts of §4 establish this picture in detail:

- **§4.1. The cross-subject gradient.** The primary result, across 14 subjects.
- **§4.2. Compression: structure vs. raw text.** Is the effect about structure or about information volume?
- **§4.3. Mechanism: Content, Not Format.** Does the content of the correct specification drive the effect, or does any structured prompt?
- **§4.4. Memory-system composition.** Does the specification layer on top of existing commercial memory systems? Where does it help or hurt at the per-question level (§4.4.2 common mechanisms, §4.4.3 cross-system Keckley case)?
- **§4.5. Exploratory case study (Letta stateful-agent).** Brief summary in body; full case study in Appendix G. Post-hoc N=3 comparison; not a headline finding.
- **§4.6. Robustness and sensitivity.** Cross-provider response generation, judge-panel sensitivity, battery composition sensitivity, wrong-spec derangement protocol sensitivity, and what these checks do not address. (The high-baseline end of the gradient through the Franklin reference is in §4.1.2.)
- **§4.7. Summary and bridge to discussion.** A one-paragraph synthesis of what §4 established, framing the transition into §5.

Every number in §4 uses the 5-judge primary aggregate defined in §3.6.3 (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-judge sensitivity check (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported in §4.6. Score deltas are read through the anchor-crossing rule from §3.6.2: a delta that crosses a rubric integer anchor is a stronger claim than one that stays inside a single anchor band.

### 4.1 The cross-subject gradient

**Hypotheses tested in this section** (from §1.2): H1. Adding the specification improves prediction. H2. The effect is inversely proportional to the response model's pretraining coverage. Corollary to H2: on high-baseline subjects, the specification does not add value and mildly interferes.

---

**The cross-subject gradient.** The less the model already knows about a subject from pretraining, the more the specification improves the model's representational accuracy of that subject. The Behavioral Specification operates as an interpretive layer over facts and retrieved context, not a replacement for them. On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.2.1), adding the specification consistently improves prediction: every one of the 9 improves over no-context baseline (mean Δ = **+0.71** for spec alone, **+0.89** for facts + spec); none declines. Adding the spec on top of facts alone (C4), raw corpus (C8), or memory-system retrieval produces additional aggregate gains that are smaller in magnitude than the spec-vs-baseline lift (detail in §4.2 and §4.4). Spec alone does not outperform facts alone or raw corpus alone; the spec's value is in the layering.

---

**Adding a Behavioral Specification changes the category of answer the response model produces, not just the number attached to it.** Of the 351 individual responses in the low-baseline slice, **55.0% crossed at least one rubric integer anchor upward when the specification was added**. Multi-anchor jumps of two or more bands (e.g., 1→3, 2→4) appear in 18% of low-baseline questions on the spec conditions, with about 6% being extreme jumps of three or more bands (e.g., 1→4, 2→5, 1→5). These extreme jumps concentrate on interpretation-heavy questions: the no-context response refuses or stays generic, and the specification supplies the behavioral pattern the model could not retrieve from training data. The response model's answer moved from one category of response to a qualitatively different category. These are the multi-anchor jumps at the margin the aggregate mean understates.

---

**What the gradient is actually showing.** The specification works by lifting subjects toward a common operating quality. The practical question is which subjects sit below that quality and need the lift; AI users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.2), and they are the subjects for whom the lift is largest and the spec is most needed. The structural mechanism: the specification produces an answer of roughly uniform quality (per-subject mean facts + spec score = **2.44** across all 14 subjects), clustering tightly in the 2.0-2.7 band regardless of where each subject's baseline sits.[^gradient-slopes] The improvement the specification produces is therefore largest on subjects whose baseline starts low, smallest on subjects whose baseline already approaches the quality the specification produces.

[^gradient-slopes]: The technical sensitivity that establishes the gradient: level regression of C4a on C5 produces a slope of +0.04, R² = 0.008; the change-score parameterization Δ_C4a on C5 has a slope of −0.96 dominated by the coupling identity slope_Δ = slope_level − 1. Reported below as the third sensitivity block.

**The specification as a leveler.** The clearest reading of the gradient is that the specification levels prediction quality across subjects: every subject, regardless of how much the model knew about them coming in, ends up at roughly the same place on the rubric (per-subject mean 2.44 across all 14 subjects). This is the equity property of the technology: it works for any subject, not just those with substantial pretraining coverage. A subject the model knew nothing about and a subject the model knew well both end up near 2.44 once the specification is applied. The specification is therefore portable across the long tail of users whose reasoning is not in any training corpus, which is the population of relevance for AI personalization (§1.4, §5.2).

| Transition | % of responses | Description |
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

One of every three low-baseline responses moves from "cannot engage" to actual engagement. Another one in five makes a larger jump. Only one response in fifteen gets worse. Worked examples of these transitions appear below (Examples A through D) and in §3.6.2 (multi-anchor crossings) and §4.1.1 (Seacole Q2 across condition bands).

---

**Three representative examples below show distinct mechanisms by which the specification improves the response.**[^example-data] Hedge reduction is common but not the only mechanism. The specification also corrects directionally-wrong predictions and enables interpretive inference from character patterns when retrieved facts are insufficient.

[^example-data]: Raw per-judge scores and full response text for the three examples at `results/global_<subject>/results_v2.json` and `results/global_<subject>/judgments_v2.json` (Examples A and B from `global_ebers/` and `global_bernal_diaz/`; Example C from `global_seacole/`).

> ### Example A. Baseline → Facts + Spec: identity disambiguation + interpretive inference
>
> **Subject:** Georg Ebers. **Q7:** *"How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?"*
>
> **Held-out:** *"A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed."*
>
> **C5 baseline (mean 1.20):** *"I don't have specific information about Ebers's characterization of this relationship in my training data. To give you an accurate answer, I would need to know: 1. Which Ebers you're referring to — there are several notable figures with this surname in educational contexts."*
>
> **C4a facts + spec (mean 3.60):** *"Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable — not instrumental, but constitutive. Self-sacrifice is not a means to institutional success; it is the evidence that success is genuine."*
>
> **Mechanism:** the baseline refused to predict because it could not identify which Ebers was meant. The specification resolved the identity and enabled a substantive interpretive claim ("constitutive, not instrumental") that the held-out passage confirms. Identity disambiguation + interpretive inference from character.

> ### Example B. Facts → Facts + Spec: directional correction
>
> **Subject:** Bernal Diaz del Castillo. **Q16:** *"When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?"*
>
> **Held-out:** *"There were 114 steps to the summit, and, as they feared that Cortes would experience the same fatigue in mounting as Motecusuma had, they were going to assist him by taking hold of his arms. Cortes, however, refused."*
>
> **C4 facts only (mean 2.00):** *"Based on the facts provided about Bernal Diaz del Castillo and his observations of Cortes, the author would expect the commander to **accept** and participate in the assistance while maintaining leadership and setting an example."*
>
> **C4a facts + spec (mean 4.80):** *"Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect Cortes to **refuse** the assistance and perform the labor himself, particularly if it serves a symbolic or morale-signaling purpose."*
>
> **Mechanism:** all facts alone produced a confident but directionally wrong prediction (commander accepts help). The specification corrected the prediction to match the held-out (Cortes refuses), encoding Cortes's pattern of physical self-reliance and performative leadership over the model's generic "good leaders accept help" default. Directional correction.

> ### Example C. Facts → Facts + Spec: abstention becomes near-perfect inference
>
> **Subject:** Mary Seacole. **Q2:** *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"*
>
> **Held-out:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*
>
> **C4 facts only (mean 2.80):** *"Based on the complete set of facts provided, there is **no specific information** about how Mary Seacole typically responds when a delirious patient mistakes her for a family member. While the facts document many aspects of Mary Seacole's nursing care and compassion, there is **no explicit account** of her reactions to delirious patients confusing her identity with their relatives."*
>
> **C4a facts + spec (mean 5.00):** *"Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern. Primary response: compassionate acceptance. She would **not correct the patient** in the moment. Instead, she would **lean into the mistaken identity, sustain the fiction with tenderness**, and prioritize emotional relief over factual accuracy. This aligns with A4 (Proximate Obligation) and A8 (Sympathetic Realism)."*
>
> **Mechanism:** clean abstention under all facts alone (the model identifies the gap and refuses to invent) lifts to specific accurate inference under all facts + spec. **2.80 → 5.00 jump, crossing three integer anchors upward.** The specification enabled generalization from Seacole's compassionate-caregiving pattern (documented in the facts but not explicitly mapped to this scenario) to the specific untested situation. Interpretive inference beyond what the all-facts dump alone provides.[^rubric-abstention-c]

[^rubric-abstention-c]: The judge panel scored the C4 abstention at 2.80, not 1.00. Judges treat honest abstentions as partial engagement (~2.5–3.0); they sometimes also penalize spec-induced honest abstentions where the spec appropriately declined to invent detail (§4.4.3's Keckley Q21). The rubric does not cleanly distinguish abstention from wrong prediction (§3.6.6); a differentiated rubric is flagged in §7.

---

**The improvement is not uniform across subjects. It depends on how much the AI already knows about the person.** Plain version: the less the model's pretraining has to work from, the more the specification can add. The more the model already knows, the less room the specification has to help, and on the highest-baseline subjects it can mildly hurt.

Two statistical confirmations support the directional claim. The **Wilcoxon signed-rank test** across all 14 main-study subjects confirms that the specification's lift over baseline is real and not due to chance.[^wilcoxon] **Pairwise Spearman ρ** across the 5-judge primary panel (§3.6.4) confirms that the lift's direction is consistent across judges rather than dependent on any one judge's scoring.[^stats-detail]

[^wilcoxon]: Wilcoxon signed-rank test results on the 14 main-study subjects: C5 vs. C2a *W* = 10 (*p* = 0.005); C5 vs. C4a *W* = 11 (*p* = 0.007).

[^stats-detail]: Pairwise Spearman ρ across the 5-judge primary panel runs 0.86 to 0.93. Regression of Δ_C4a on C5 baseline: slope **−0.96** [95% CI −1.24, −0.67], R² = 0.82, *p* < 0.001 (*p* = 0.000009), correlation *r* = −0.90. Subjects with positive Δ_C4a: 12 of 14; low-baseline subjects (*n* = 9) all positive; low-baseline mean Δ_C4a = **+0.89**. Full statistical detail in Appendix B.6.

---

**Reading the gradient.** Figure 4.1 plots each subject's no-context baseline (C5) against the lift the specification produces over that baseline (Δ_C4a). The slope is the core relationship: subjects with lower baselines see larger lifts; subjects with higher baselines see smaller or negative lifts. The 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Babur at **+0.25** (smallest lift) to Hamerton at **+1.51** (largest). Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13: the high-baseline reference where the model already knows the subject from pretraining. The regression slope of **−0.96** captures this gradient: the lower the model's pretraining baseline on a subject, the larger the lift the specification produces, because the spec produces a roughly constant facts + spec quality near 2.46 regardless of baseline. The takeaway: the specification helps most where the model knows the subject least; once a subject crosses into the high-baseline band, the specification has no representational gap to fill.

![Figure 4.1: Cross-subject gradient. Each subject's no-context baseline (C5, x-axis) plotted against the specification lift (Δ_C4a, y-axis) for all 14 main-study subjects. Low-baseline subjects (C5 ≤ 2.0, the population of relevance) cluster in the upper-left with positive lifts ranging from Babur (+0.25) to Hamerton (+1.51). Franklin (high-baseline reference, C5 = 3.77) sits in the lower-right with Δ = −0.13. Regression slope −0.96, R² = 0.82. (§4.1)](../figures/fig_4_1_gradient_scatter_v3.png)

---

**Per-subject results.**

The table is ordered by baseline within each band. In the color-rendered PDF of the paper, the low-baseline rows are tinted green (the population of relevance), the mid-baseline rows are tinted yellow, and Franklin is tinted gray as the high-baseline reference. Figure 4.1 presents the same data as a scatter plot with the regression line.

Bands: **Low** (C5 ≤ 2.0, the population of relevance), **Mid** (2.0 < C5 < 3.0), **High** (Franklin, the known-figure reference).

| Band | Subject | C5 baseline | C4 facts | C2a spec | C4a facts+spec | Δ C4a−C5 | Δ C4a−C4 | Anchor |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| Low | Ebers | 1.02 | 2.02 | 1.54 | 2.07 | +1.05 | +0.05 | ✓ |
| Low | Sunity Devee | 1.03 | 2.46 | 2.27 | 2.41 | +1.38 | −0.05 | ✓ |
| Low | Hamerton | 1.26 | 2.43 | 2.63 | 2.77 | +1.51 | +0.34 | ✓ |
| Low | Fukuzawa | 1.67 | 2.67 | 2.35 | 2.78 | +1.11 | +0.11 | ✓ |
| Low | Bernal Diaz | 1.70 | 2.41 | 2.27 | 2.48 | +0.78 | +0.07 | partial |
| Low | Babur | 1.76 | 2.03 | 1.91 | 2.01 | +0.25 | −0.02 | - |
| Low | Seacole | 1.77 | 2.63 | 2.48 | 2.59 | +0.82 | −0.04 | ✓ |
| Low | Keckley | 1.84 | 2.39 | 2.43 | 2.44 | +0.59 | +0.05 | - |
| Low | Yung Wing | 1.88 | 2.13 | 2.22 | 2.40 | +0.52 | +0.27 | - |
| Mid | Zitkala-Sa | 2.34 | — | 2.03 | 2.02 | −0.32 | — | - |
| Mid | Cellini | 2.38 | — | 2.54 | 2.53 | +0.15 | — | - |
| Mid | Rousseau | 2.44 | — | 2.81 | 2.53 | +0.10 | — | - |
| Mid | Augustine | 2.58 | — | 2.48 | 2.70 | +0.11 | — | - |
| Mid | Equiano | 2.77 | — | 2.46 | 2.42 | −0.35 | — | - |
| High | Franklin | 3.77 | — | 3.37 | 3.65 | −0.13 | — | - |

C4 (facts only) was run on the 9 low-baseline subjects as part of the §4.2 compression analysis; mid-baseline subjects and Franklin were not included in that condition. The Δ C4a−C4 column shows what adding the specification contributes on top of facts alone. On low-baseline subjects, the spec-on-facts increment is small (mean +0.09) and mixed in sign per question, with most of the lift coming from the spec-vs-baseline gap.

**What each band is telling us.**

- **Low-baseline (n = 9):** every subject improves. The slice is uniform. This is the population of relevance for real AI deployment.
- **Mid-baseline (n = 5):** 3 subjects improve, 2 decline. The model has enough pretraining footprint on these subjects that the specification competes with the model's own working model. The specification sometimes increases representational accuracy and sometimes does not.
- **Franklin (high-baseline reference):** both spec-containing conditions score below baseline. The specification cannot add what the model already has.

Per-subject anchor-crossing distributions (ranging from 25.6% on Babur to 74.4% on Sunity Devee) and per-subject per-judge score matrices are in Appendix D.[^robustness-pointer]

[^robustness-pointer]: Two potential confounds on the gradient slope (battery-question-type composition and Hamerton-leverage subset regression) are addressed in §4.6.3 as robustness checks; both leave the baseline gradient effect substantially intact.

**The aggregate gradient hides per-question structure that is itself the most informative finding.** The specification produces large category-level shifts on a subset of questions (multi-anchor crossings, including band-5 endpoints reached from band-2 starts under cross-condition comparisons such as C4 → C4a) and minimal change on others. §4.1.1 decomposes this distribution and shows where the spec's value concentrates.[^heldout-leakage-audit]

[^heldout-leakage-audit]: Held-out leakage audit on the 60 unique extreme-upward-jump cases at `docs/research/held_out_leakage_investigation_20260428.md`: 0 6-gram matches at C4a, severity rare; full taxonomy and headline-impact estimate in Appendix B.9.

### 4.1.1 Per-question baseline engagement and the worked rubric example

Pooled across 546 questions on the 14 main-study subjects (5-judge primary panel), the C5 baseline splits into two clusters.[^companion-data-411]

[^companion-data-411]: Companion data: `docs/research/baseline_engagement_analysis_20260429.json`, `docs/research/abstention_extensions_analysis_20260429.json`. Reproducibility scripts: `scripts/analyze_baseline_engagement.py`, `scripts/analyze_abstention_extensions.py`. Roughly **41% of questions return a refusal or non-answer** (C5 mean = 1.00); roughly **21% return a substantive subject-specific prediction** (C5 mean ≥ 3.0); the middle is thin. The spec's lift over baseline tracks this split inversely: it adds the most where the baseline refuses, the least where the baseline already engages.[^bimodal-stats] This is the per-question shape that the §4.1 gradient summarizes at the subject level.

[^bimodal-stats]: Spearman ρ between C5 baseline and C4a − C5 lift = **−0.73** (n = 546, p ≈ 1.7 × 10⁻⁹¹). Per-subject ρ negative for 14 of 14 subjects; 12 of 14 reach p < 0.01. Mann-Whitney test on lift in REFUSE (n = 225) vs ENGAGED-or-STRONG (n = 116): means +1.32 and −0.62, U = 24,886, p ≈ 5.5 × 10⁻⁴³.

| Bin | N (of 546) | Share | Mean Δ_C4a (lift) | SD | Positive lift |
|---|---:|---:|---:|---:|---:|
| REFUSE (c5 = 1.00) | 225 | 41.2% | +1.32 | 0.88 | 94.2% |
| MARGINAL (1 < c5 < 2) | 110 | 20.1% | +0.66 | 0.83 | 78.2% |
| GENERIC (2 ≤ c5 < 3) | 95 | 17.4% | +0.04 | 0.63 | 39.0% |
| ENGAGED (3 ≤ c5 < 4) | 82 | 15.0% | −0.47 | 0.81 | 25.6% |
| STRONG (c5 ≥ 4) | 34 | 6.2% | −0.99 | 0.78 | 8.8% |

The bimodality is *within-subject*, not just across subjects: Sunity Devee and Ebers sit at the floor (37 of 39 and 36 of 39 questions in REFUSE); Equiano sits at the high end (2 of 39 in REFUSE, 5 in STRONG); even Augustine, the highest-baseline subject in the main gradient, has 8 of 39 questions in REFUSE.

**Worked rubric example: Seacole Q2 across condition bands.**

**Subject:** Mary Seacole. **Q2:** *Based on Mary's character, would she comfort a delirious soldier who mistakes her for his wife?*

**Held-out ground truth:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*

The 5-judge primary panel scores five conditions on this question across four rubric bands (band 3 was not observed here).

| Band | Definition (from §3.6) |
|---:|---|
| 1 | Refusal or non-answer. |
| 2 | Generic, pattern-free; could apply to many subjects. |
| 3 | Subject-specific behavioral tendency identified. |
| 4 | Multiple behavioral dimensions together. |
| 5 | Closely matches the held-out behavioral pattern. |

| Condition | Mean | Band | Excerpt (verbatim) |
|---|---:|---:|---|
| C2c wrong spec (Babur) | 1.40 | 1 | "Mary would **not sustain the deception**, but she would **not abandon the soldier either**. ... She would correct him — gently, but directly ... allowing him to die in a false belief violates her epistemic obligation." |
| C5 baseline | 1.80 | 1 | "I'd need to know which Mary you're referring to. There are many famous Marys in literature, history, and other works. Could you provide more context?" |
| C4 fact dump | 2.80 | 2 | "Based on the extensive facts about Mary's character, **yes, she would absolutely comfort such a soldier** ... Mary would likely gently accept the soldier's confusion while providing comfort..." |
| C2a full spec | 4.20 | 4 | "Yes, she would comfort him. But not by correcting him. ... She would *not* say 'I am your wife' or sustain the delusion. ... Stay present. Touch him. Speak to the need beneath the confusion." |
| C4a full facts + spec | 5.00 | 5 | "Yes, absolutely ... She would **accept the mistake without correcting it**, not out of deception, but out of A8 (Sympathetic Realism). She understands that his delusion is a mercy, a refuge his mind has built to survive unbearable pain." |

The example traces the *cross-anchor interpretation rule* of §3.6.2 on a single question. C5 declines for lack of referent; C2c (a Babur spec) is articulate but mis-applied. C4 with raw facts reaches a generic affirmative. C2a, working from the full spec without retrieved facts, produces an internally articulate multi-dimensional answer about presence and tenderness but lands on a *less specific* prediction about whether Mary would correct him. C4a, with both facts and spec, explicitly endorses non-correction; the held-out shows Mary chose not to undeceive him, and C4a matches that direction outright while C2a is less clear on it. Categorical movement from band 1 through band 5 on a single question is what the per-subject means in §4.1 aggregate.

The spec is reliably useful where the baseline abstains. Per-response-model abstention behavior (Sonnet over-credits abstention at roughly twice Haiku's rate) is decomposed in §3.6.6; memory-system retrieval inflates refusal scores at the condition level rather than via visible fact recitation, decomposed in §4.4; further limitations on the abstention reading (REFUSE-bin contains roughly 7% wrong-but-confident predictions, mixing *spec corrects abstention* with *spec corrects confident error*) are flagged in §6.2.

### 4.1.2 The gradient at the high-baseline end (Franklin reference)

Franklin is not part of the N=14 main-study sample; he is treated as a known-figure reference subject to test whether the gradient pattern continues at the high-baseline end where the model already has a substantial pretraining representation of the subject.

Benjamin Franklin's *Autobiography* is one of the most widely cited autobiographical works in American public-domain literature; every current-generation LLM has substantial pretraining representation of both the person and the text. Franklin's no-context baseline of 3.77 (5-judge primary) sits above the rubric's anchor-3 ("right domain, wrong outcome") and nudges toward anchor 4 ("general direction correct"); the next-highest main-study subject is Equiano at 2.77. Franklin sits a full anchor band above the main study's upper end.

Both spec-containing conditions score below Franklin's baseline: spec alone drops 0.40 points, all-facts-plus-spec drops 0.13. Our reading, theoretical and not isolated by an additional control, is that the specification alone competes with the model's strong pretraining-derived representation of Franklin without the facts to re-anchor the response, and adding facts back partially restores the model's own working model.

The gradient is therefore the same pattern read from both ends: a large positive effect where the baseline is low, a near-zero or mildly negative effect where the baseline is high. The high-baseline end is not a reversal of the low-baseline finding.[^franklin-data]

[^franklin-data]: Raw per-subject Franklin data at `results/franklin_legacy_20260411/`.

### 4.2 Compression: structure vs. raw text

**Hypothesis tested in this section** (H5 from §1.2): A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size.

---

**Context improves prediction.** On the 9 low-baseline subjects, every context condition increases the per-subject mean score by roughly one full rubric point over the no-context baseline.

| Condition | Context served (approx. tokens, low-baseline mean) | Mean (low-baseline, n=9) | Δ from C5 |
|---|---|---:|---:|
| C5 | none (baseline) | 1.52 | 0.00 |
| C2a | spec only (~7K) | 2.23 | +0.71 |
| C4 | all facts only (~10K) | 2.35 | +0.83 |
| C8 | raw corpus only (~163K mean; range 33K–549K) | 2.45 | +0.93 |
| C4a | all facts + spec (~17K) | 2.45 | +0.93 |
| C9 | corpus + spec (~170K mean) | 2.50 | +0.98 |

The AI does not need much context to move from refusal-and-off-base to engaged subject-specific prediction. It needs *some* context.

**The compact specification captures the large majority of that representational-accuracy gain.** A 7,000-token Behavioral Specification recovers most of what the full raw corpus delivers, despite being roughly 5x to 80x smaller depending on subject (per-subject compression ratios in the table below). Across the 9 low-baseline subjects, the raw corpus (C8) averages 0.22 points higher than spec alone (C2a). The corpus's edge is real but small relative to the context-size gap that produces it.

**The efficiency claim in one metric: predictive gain per 1,000 tokens of context.** The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. Plotted against context size, the score climbs steeply at first and flattens out. The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document.

![Figure 4.2: Score versus context size (log scale) per subject across compression-related conditions. The score climbs steeply across the first ~7K tokens of structured specification and plateaus through ~80K to 400K tokens of raw corpus, illustrating the efficiency gain at small context budgets. (§4.2)](../figures/fig_4_2_compression_v3.png)

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
- Adding the specification on top of the full raw corpus (C9) adds ~0.09 points on average over raw corpus alone.[^c9-aggregation] The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

[^c9-aggregation]: Per-question paired recompute on the 8-subject C9-eligible slice. The per-subject mean column at the bottom of the per-subject table reads 2.59 for C9 vs. 2.45 for C8, but the cross-subject mean of per-question paired Δs is the canonical number for the comparison.

**What the aggregate numbers hide.**

The small mean Δ values for adding the spec on top of all facts or on top of raw corpus are residues of substantial per-question movement in both directions, not uniformly small effects. *Multi-anchor crossings* (defined in §3.6.2) occur much more often when context is added to a no-context baseline than when the specification is layered on top of all facts or raw corpus.

| Comparison | Subject set | n paired | Multi-anchor (≥2 bands) | Extreme (≥3 bands) | Mean Δ |
|---|---|---:|---:|---:|---:|
| Baseline → full pipeline (all facts + spec) | all 14 | 546 | 13.0% | 3.7% | +0.55 |
| Baseline → all facts only | all 14 | 546 | 12.5% | 4.4% | +0.47 |
| Baseline → spec only | all 14 | 546 | 9.0% | 2.0% | +0.43 |
| Wrong spec → correct spec | all 14 | 546 | 14.5% | 2.4% | +0.64 |
| Baseline → raw corpus only | 13 (Babur excl.) | 507 | 15.4% | 4.3% | +0.59 |
| Baseline → corpus + spec | 13 (Babur excl.) | 507 | 14.8% | 4.7% | +0.62 |
| All facts → all facts + spec | all 14 | 546 | 2.2% | 0.9% | +0.08 |
| Corpus → corpus + spec | 13 (Babur excl.) | 507 | 2.4% | 0.4% | +0.03 |

Adding context to a no-context baseline shifts categorical bands on roughly 1 in 7 questions; layering the specification on top of all facts or raw corpus shifts categorical bands on roughly 1 in 45. The pattern is consistent with the §1 thesis: the specification produces the most categorical moves where prior context is sparsest.[^multi-anchor-rates]

[^multi-anchor-rates]: All-14 figures from `docs/research/multi_anchor_rates_all_pairs_20260430.json` (script: `scripts/compute_anchor_crossing_all_pairs.py`). Row labels above use natural language; cross-reference to condition codes is in §3.4 and Appendix C. The 9-subject low-baseline slice gives somewhat higher rates (e.g., baseline → full pipeline at 18.2% on 9 subjects vs. 13.0% on all 14), reflecting that high-baseline subjects have less room to cross anchors upward at the integer-band granularity. Hamerton is a strong outlier on the corpus → corpus+spec comparison (49% upward rate, 19 up vs. 2 down on its 39 questions) within the low-baseline slice. Per-question phenomena, including the bimodal cancellation that produces near-zero aggregate Δ on the spec-on-info-rich pairs, are decomposed in §4.4.2 alongside memory-system layering. Multi-anchor examples: Hamerton q22 (1→3 on corpus → corpus+spec), Hamerton q25 (1→4), Seacole q2 (2→5 on facts → facts+spec), Yung Wing q22 (1→4 on facts → facts+spec).

### 4.2.1 Per-question improvement rate

The aggregate mean score blends judge variability with response quality. A cleaner unit: **out of N individual questions, how many does each condition improve over the no-context baseline?** Each question either improves, ties, or worsens when the condition's context is added.

We report three numbers per condition: the improvement rate, the worsening rate, and the median magnitude of improvement among improved questions (with median worsening magnitude as a sanity check).

**Low-baseline slice (9 subjects, 351 questions, 5-judge primary per-question means).**

| Condition vs. baseline | Approx. context | Improved | Tied | Worse | Improvement rate | Median Δ when improved | Median Δ when worsened |
|---|---|---:|---:|---:|---:|---:|---:|
| **Spec only** | ~7K tokens | 249 | 49 | 53 | **70.9%** | **+1.00** | −0.40 |
| All facts only | ~10K tokens | 256 | 44 | 51 | 72.9% | +1.00 | −0.40 |
| Raw corpus | ~163K mean (33K–549K) | 275 | 31 | 45 | 78.3% | +1.00 | −0.60 |
| All facts + spec | ~17K tokens | 276 | 22 | 53 | 78.6% | +1.00 | −0.40 |

**The magnitude column is the important row.** When the specification helps, the typical help is a full rubric category (+1.00 median). When it hurts, the typical hurt is less than half a category (−0.40 median). The underlying improvements are substantive, not trivial fractional gains.

On the 9 low-baseline subjects, **7 out of every 10 questions improve with the specification alone**, roughly 1 in 10 tie, and fewer than 1 in 6 worsen. The specification's rate sits within 8 percentage points of the raw corpus's (70.9% vs. 78.3%) at an order of magnitude less context.[^q-improvement-supplemental]

[^q-improvement-supplemental]: All 14 main-study subjects, matched 39-question batteries (546 questions): spec only 58.8% improvement / 26.7% worsening; facts only 60.1% / 26.6%; raw corpus 65.2% / 23.6%; facts + spec 65.8% / 26.4%. Pairwise question-level comparison on the low-baseline slice: raw corpus beats spec alone on 53.3% of questions (vs. 30.8% the other way, 56 ties); corpus + spec beats facts + spec on 49.0% of questions (vs. 36.5%, 45 ties). The 7K-token facts + spec package outscores the much larger corpus + spec package on roughly one-third of questions.

![Figure 4.2.1: Per-question improvement rates across the four context conditions for the 9 low-baseline subjects (351 paired questions, 9 × 39). Conditions are ordered by context size: spec alone (C2a, ~7K tokens), facts alone (C4, ~10K), facts plus spec (C4a, ~17K), raw corpus (C8, ~163K mean). The improved-share line stays in the 70.9% to 78.6% band across conditions; the tied band is intermediate; worsened stays low. Spec alone improves 70.9% of questions at roughly an order of magnitude less context than the raw corpus (78.3%); facts plus spec matches the raw corpus's improvement rate while cutting the tied band roughly in half. Median Δ when improved is +1.00 rubric points; median Δ when worsened is −0.40 points. (§4.2.1).](../figures/fig_4_2_1_question_improvement_rates_v3.png)

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

[^compression-data]: Raw per-subject data at `results/global_<subject>/c8_c9_results.json` and `results/global_<subject>/results_v2.json`. The compression analysis is in `scripts/recompute_5judge_primary.py`; per-question improvement rates are computed at render-time in `scripts/generate_fig_4_2_1.py`. Figure 4.2 plots score versus context size (log scale) per subject and shows the steep initial climb and long plateau.

---

### 4.3 Mechanism: Content, Not Format

**Hypothesis tested in this section** (H3 from §1.2): The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

---

**If structure were the dominant driver, a mismatched specification would produce a substantial fraction of the matched-spec improvement. Random pairings recover only part of it (some content alignments survive at random), and adversarial pairings actively degrade performance below baseline.**

On the 13 global subjects with complete 5-judge primary coverage, three conditions test whether content matters:

| Condition | Mean Δ vs. C5 (5-judge primary, 13 globals) | Reading |
|---|---:|---|
| C2a (correct spec) | **+0.35** | matched content increases representational accuracy |
| C2c v2 (random derangement, seed-fixed) | **+0.15** | partial improvement; dominated by floor effects on low-baseline subjects |
| C2c v1 (fixed derangement, cultural/temporal distance maximized) | **−0.25** | adversarial mismatch degrades representational accuracy below the no-context baseline |

The two wrong-spec variants differ by construction. **v1 (fixed derangement)** is a hardcoded pairing designed so each subject receives the specification of a culturally- and temporally-distant other (for example, Ebers the 19th-century German Egyptologist receives Equiano the 18th-century West-African/British autobiographer; Seacole the 19th-century Jamaican nurse receives Bernal Diaz the 16th-century Spanish conquistador).[^wrong-spec-script] **v2 (random derangement)** is a seed-fixed random permutation in which no subject receives its own specification but pairings can land culturally-close; this tempers the aggregate drop. Reporting both shows that even a random wrong-spec barely beats no context, and an adversarial wrong-spec actively hurts.

[^wrong-spec-script]: Pairing logic in `scripts/run_global_rerun.py`.

The gap between the correct-spec (C2a) condition at +0.35 and the fixed-derangement (C2c v1) condition at −0.25 is **0.60 points on the 1-5 rubric**, more than half a full rubric-anchor category. That gap is the content effect, measured at the population mean; per-question swings are larger in both directions (Example B below has a −0.20 coincidental-overlap case where the wrong spec nearly matches the correct spec; Example C below has a −3.60 clean mismatch case).

**Per-subject heterogeneity.** Both wrong-spec deltas hide per-subject variation. The full per-subject table, the count of subjects with positive vs. negative outcome under each protocol, and the adversarial-vs-random pairing sensitivity are in §4.6.4.

---

**Three mechanism types.**

Three distinct mechanisms produce the correct-specification improvement across the study data. Each has a characteristic wrong-specification failure mode, illustrated in the matched examples below.

1. **Identity disambiguation.** When the baseline model cannot determine which person is being asked about, the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame. *Wrong-spec failure mode:* the model either detects the mismatch explicitly and refuses to predict, or anchors on the wrong person's pattern and produces a coherent but off-target prediction.
2. **Directional correction.** When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification overrides the generic with the subject-specific. *Wrong-spec failure mode:* the model applies the wrong person's pattern; depending on how close that pattern happens to be to the target subject's, the prediction is either directionally wrong in a new way or coincidentally correct (the wrong person's pattern happens to predict the same surface behavior on this particular question, for different underlying reasons; Example B below is one such case).
3. **Interpretive inference.** When retrieved facts do not include direct evidence for the specific question, the specification provides interpretive scaffolding to generalize from established character patterns to the new situation. *Wrong-spec failure mode:* the model detects the mismatch and refuses, or applies wrong-person scaffolding and produces a low-quality prediction.

---

**Response-level evidence: when the model engages with the spec, and when it does not.**

Three signals from response text confirm that content matters more than structure.

**Spec-tag citation gap.** Models cite spec-specific tags (anchor IDs, axiom references, predictive-template labels) on **78.6%** of correct-spec responses but only **50.0%** of wrong-spec responses.[^spec-activation-data] The 28.6-point gap is a lower bound on the content effect; models may draw on spec content without literally quoting tag IDs.

[^spec-activation-data]: Data at `docs/research/spec_activation_analysis.json`.

**Models can detect when a specification does not fit the named subject.** Across 587 wrong-spec responses, **60.6% explicitly flagged the content mismatch** (example: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*). 36.5% attempted to apply the mismatched content and produced low-quality predictions; 3% hedged or were ambiguous.[^wrong-spec-detection] The detection signal is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model already knows about the named subject. Specifications are anonymized (§3.7), so the model has no surface name cue to compare against; only interpretive content.

[^wrong-spec-detection]: 587 wrong-spec responses: 507 from the v2 random-derangement protocol on the 13 global subjects, plus 80 from the v1 adversarial protocol on Hamerton across all five battery tiers. Validated against a 30-response stratified manual spot check. Full breakdown: 60.6% explicit mismatch flag, 36.5% applied mismatched content, 2.0% hedged implicitly, 0.9% ambiguous.

**Hedging persists under wrong-spec.** Correct-spec conditions eliminate baseline hedging: 28.8% → 0.0% under the strict-pattern classifier, 41.2% → 0.4% under the broader-pattern classifier (rule definitions in [§1.3](#13-what-we-found) footnote). On wrong-spec, refusal patterns persist at the 60.6% explicit-detection rate above. The hedging-elimination is content-specific, not structure-specific.

---

**Per-question matched comparison.**

The three §4.1 examples extend directly into mechanism-by-mechanism wrong-spec contrasts. Same subject, same question, same response model; the only change is the specification content. Correct-spec C4a responses are in §4.1 for reference.

> ### Example A (wrong-spec), Ebers Q7: identity disambiguation fails
>
> **Subject + question:** same as §4.1 Example A (Ebers, self-sacrifice and educational institutional success). Battery-question target name: Ebers (explicit in the prompt).
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
> **Reading.** The model detected the mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It named the served anchors correctly, reasoned from Equiano's framework, and declined to produce a prediction about Ebers. The identity-disambiguation mechanism that enabled the correct spec's lift in §4.1 Example A did not fire because the spec content is not about Ebers. The response falls near the rubric floor because no prediction was made.

> ### Example B (wrong-spec), Bernal Diaz Q16: content convergence across genuinely different frameworks
>
> **Subject + question:** same as §4.1 Example B (Bernal Diaz, Cortes and offered physical assistance). Battery-question target name: Bernal Diaz.
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
> **Subject + question:** same as §4.1 Example C (Seacole, delirious patient). Battery-question target name: Mary Seacole.
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
> **Reading.** The model detected the mismatch between the named target in the question (Mary Seacole, a 19th-century Jamaican Creole nurse) and the anonymized content of the served specification (16th-century Spanish conquest anchors). It named the anchors it was seeing, placed Seacole in a different era and role, and refused to apply the mismatched content. The interpretive-inference mechanism that produced §4.1 Example C's correct-spec 5.00 score does not fire: without Seacole's actual character pattern in context, the model would not generalize from an unrelated conquistador's framework to her delirious-patient scenario.

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

### 4.4 Memory-system composition

**Hypothesis tested in this section** (H4 from §1.2): The Behavioral Specification interacts with memory-system retrieval in a structured way. It lets retrieval-based systems handle question types they were not designed for (interpretation-heavy questions where retrieved facts alone are insufficient), while sometimes hurting on question types where retrieval already supplied the plain answer (literal-recall) or where retrieved facts are insufficient to ground a prediction at all (refusal-triggering). The aggregate per-system Δ is therefore a mixture of these patterns, with the balance shifting by retrieval architecture. The load-bearing finding is per-question, not aggregate.

**Surfaced finding (not pre-registered).** §4.4.1 also reports a finding that did not feature in our pre-registered hypotheses: given an identical fact pool and the same questions, the four commercial memory systems plus our substrate retrieve substantially non-overlapping top-10 facts on the same question. On 35.9% of (system pair, question) instances two systems share zero facts in their top-10s; mean pairwise overlap is 8.3% across the ten system pairs. Recall benchmarks like LongMemEval and LOCOMO measure whether a system can retrieve a previously-stored fact, and these systems perform within a few percentage points of each other on those benchmarks; representational accuracy and behavioral prediction operate at a different layer, where the relevant question is which facts matter for a specific interpretive task. Detail in §4.4.1; meta-analysis follow-ups in §7.1.

---

### 4.4.1 Aggregate performance across systems

**Layered on top of three of four commercial memory systems (Mem0, Letta, Zep), the Behavioral Specification produces a net-positive aggregate Δ across the 14 main-study subjects. The aggregate Δ on every system is the balance of per-question patterns; that decomposition is in §4.4.2 (where Supermemory's near-zero aggregate Δ is also unpacked).**

**Setup.** Four commercial memory systems (Mem0, Letta[^letta-second-path], Supermemory, Zep) and Base Layer's own zero-cost retrieval substrate (MiniLM-L6-v2 + ChromaDB) were tested under two configurations.

[^letta-second-path]: Letta's archival-retrieval path is reported here. Letta also exposes a second path (a persistent memory block its agent self-edits during ingestion, the MemGPT design), which is architecturally unlike a retrieval path and is reported separately in §4.5.

- **Controlled configuration.** Each system is given an identical pre-extracted fact pool drawn from the training half of each subject's corpus. Holds the input constant across systems; differences trace to retrieval and presentation policy alone.
- **Native configuration.** Each system ingests the raw training corpus through its own production pipeline, as in deployment. Measures the full end-to-end system.

Within each system in each configuration, two conditions are compared:
- **C1** (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.
- **C3** (retrieval + spec): the same retrieval plus the full Behavioral Specification.

The spec-effect for that system is **Δ_spec = mean(C3) − mean(C1)**, aggregated per subject, then averaged across subjects. If the specification helps memory-system performance, Δ_spec is positive across systems.

---

**Aggregate results (5-judge primary, all 14 main-study subjects).**

| System | Δ_spec controlled | Subjects improved (controlled) | Δ_spec native | Subjects improved (native) |
|---|---:|---:|---:|---:|
| Mem0 | +0.12 | 10/14 | +0.33 | 10/14 |
| Letta (archival) | +0.20 | 12/14 | −0.02 | 5/14 |
| Zep | +0.19 | 13/14 | +0.33 | 13/14 |
| Supermemory | +0.04 | 7/14 | −0.01 | 6/14 |
| Base Layer substrate | +0.08 | 9/14 | N/A | N/A |

Headline numbers report the all-14 panel. The 9-subject low-baseline slice was computed but is statistically underpowered at the effect sizes these systems show, so we do not lead with it; per-subject low-baseline detail and Wilcoxon test results are in the footnote.[^memsys-stats] Three of four commercial systems produce a positive aggregate Δ_spec under at least one configuration; Supermemory aggregates near zero under both. Base Layer's substrate produces the smallest positive Δ, reflecting that Base Layer's retrieval is intentionally bare; the interpretive improvement comes from the specification itself, not from retrieval choices.

[^memsys-stats]: Wilcoxon signed-rank on C1 vs. C3, all-14 panel (robust at α = 0.01): Zep controlled *p* = 0.0004, Letta controlled *p* = 0.0017, Mem0 native *p* = 0.0088, Zep native *p* = 0.0015. Letta native, Mem0 controlled, Supermemory (both configurations), and Base Layer substrate are not significant at α = 0.05 on either the all-14 or low-baseline-9 slice. Low-baseline 9-subject slice, controlled configuration: Mem0 +0.10 (6/9 improved), Letta +0.17 (8/9), Zep +0.17 (9/9), Supermemory −0.01 (4/9), Base Layer +0.08 (6/9). Native: Mem0 +0.32 (7/9), Letta −0.04 (4/9), Zep +0.30 (9/9), Supermemory −0.03 (4/9). The Supermemory native aggregate covers all 14 subjects under a paid-tier rerun completed 2026-04-23; 30 provider-failure placeholders (Augustine 2 q, Equiano 28 q) are scored at the rubric floor and treated as scored data, not missing data; qualitative story holds either way. Per-system per-subject per-judge scores at `results/global_<subject>/*_judgments*.json`. Per-system anchor-crossing analysis at `docs/research/per_system_anchor_crossing_20260427.md` and `.json`. A hedging-reduction pattern surfaced during the memory-system analysis but did not track the spec-effect magnitude cleanly across systems; the content-specific reading from §4.3 holds.

**The controlled-vs-native split is itself informative.** When the input is held constant (controlled), four of five systems produce a positive Δ_spec; the specification's contribution is visible on top of an identical fact pool. When each system ingests its own way (native), the systems split: Mem0 and Zep increase under native (Mem0 +0.12 → +0.33, Zep +0.19 → +0.33); Letta decreases sharply (+0.20 → −0.02); Supermemory stays roughly flat (+0.04 → −0.01). Native ingestion shapes how much room the specification has to contribute on top, and that interaction varies by system. The mechanism for these splits is in §4.4.2: the spec helps retrieval-based systems on interpretation-heavy questions they were not designed for, sometimes hurts on literal-recall questions retrieval already answered, and induces principled refusals on questions where retrieved facts cannot ground a prediction.

**Cross-system retrieval overlap: providers do not converge.** For the §1.2 convergence question, the controlled answer is no: the provider layer does not converge on relevance. On 35.9% of (system pair, question) instances two systems share zero facts in their top-10s, on 65.6% they share one or fewer, and the mean pairwise overlap across the ten system pairs is 8.3%.[^share-zero-cut] Recall benchmarks like LongMemEval and LOCOMO measure whether a system can retrieve a previously-stored fact, and the four commercial systems we tested perform within a few percentage points of each other on those benchmarks; representational accuracy and behavioral prediction operate at a different layer, where the relevant question is which facts matter for a specific interpretive task. Convergence on top-K under identical input would have been evidence of a shared interpretive substrate. The systems do not converge, which suggests the rankings reflect provider-specific design choices rather than a shared theory of which facts the question is asking for. The controlled configuration isolates the ranking layer as a load-bearing source of representational accuracy: which facts the system surfaces determines, before any reading model engages, what the response can be about.

[^share-zero-cut]: Share-zero / share-≤1 fractions computed across all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs = 5,460 (system pair, question) instances under the controlled retrieval configuration. Excluding Hamerton (13 globals × 39 × 10 = 5,070 instances) shifts share-zero to 36.7% and share-≤1 to 66.6%. Restricting to the four commercial systems (six pairs, BaseLayer excluded) shifts share-zero to 40.4% (14 subjects) or 41.0% (13 globals); every cut shows substantial top-K divergence on identical input. Reproducibility script at `scripts/analyze_retrieval_overlap.py`; data at `docs/research/retrieval_overlap_analysis_20260501.json`.

The metric is **pairwise Jaccard similarity**: for any two systems on the same question, the fraction of retrieved facts that appear in both lists, computed as the size of the intersection divided by the size of the union. A Jaccard of 1.0 means identical top-10s; 0.0 means no shared facts. We compute it for each of the ten system pairs (Base Layer, Letta, Mem0, Supermemory, Zep) on each of 546 questions, in the controlled configuration where every system reads the same all-facts pool.

| System pair | Mean Jaccard (controlled, n=546 questions) |
|---|---:|
| Base Layer ↔ Supermemory | 0.146 |
| Mem0 ↔ Letta | 0.126 |
| Base Layer ↔ Mem0 | 0.123 |
| Mem0 ↔ Supermemory | 0.114 |
| Letta ↔ Supermemory | 0.099 |
| Base Layer ↔ Letta | 0.092 |
| Mem0 ↔ Zep | 0.056 |
| Base Layer ↔ Zep | 0.027 |
| Letta ↔ Zep | 0.026 |
| Supermemory ↔ Zep | 0.025 |
| **Mean across pairs** | **0.083** |

![Figure 4.4.1: Cross-system retrieval overlap. Mean pairwise Jaccard between every pair of memory systems on the controlled retrieval configuration (n=5,460 = all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs). The diagonal is grayed; cells below the diagonal mirror cells above. Highest pair Base Layer–Supermemory at 0.146; lowest Supermemory–Zep at 0.025. Zep's row is uniformly low (graph-traversal scoring overlaps weakly with embedding-similarity retrieval). Mean across pairs 0.083.](../figures/fig_4_4_1_jaccard_heatmap_v1.png)

Pairs involving Zep are the lowest. Zep returns a serialized graph-edge blob from which we extract top-level `fact='...'` kwargs (yielding 9.8 unique facts on average), and graph-traversal scoring overlaps weakly with the embedding-similarity rankings the other systems use. Letta's controlled retrieval emits 10 entries per question but only 3.5 unique facts on average; the same fact recurs under graph traversal. Jaccard is computed on unique sets, so duplication does not directly inflate overlap, but it does compress Letta's effective retrieval depth.[^jaccard-aggregate-detail]

[^jaccard-aggregate-detail]: Mean pairwise Jaccard across all ten pairs is 0.083 raw, 0.088 after lowercase + whitespace normalization. Per-subject Jaccard varies from 0.043 (Equiano) to 0.115 (Hamerton); per-category variation is small (0.076–0.093 across decisions, values, relationships, conflict, learning). The divergence is a property of provider ranking, not of question type or subject. Full per-pair, per-subject, per-category breakdowns at `docs/research/retrieval_overlap_analysis_20260501.json`. Reproducibility script at `scripts/analyze_retrieval_overlap.py`.

This ties to the §4.4.2 patterns. The three downstream patterns that distinguish memory-system behavior (interpretive supply, over-theorization, and spec-induced refusal) emerge in part from this retrieval divergence. Providers do not disagree about which facts exist; the all-facts pool is shared. They disagree about which facts the question is asking for.

The native pipeline shows the same divergence more starkly. Native retrievals return heterogeneous objects: Mem0 third-person summaries, Letta raw multi-sentence passages, Supermemory atomic facts, Zep graph rows. Because the four systems return different shapes of output, any two systems share zero exactly-matching facts on the same question, and pairwise overlap drops to 0.000 across all four native pairs. A semantic-similarity check that lets two facts count as a match when they share roughly the same content (rather than the same exact wording) raises the native overlap only marginally, to 0.004 at a near-paraphrase threshold and 0.016 at a loose topical threshold. The divergence is structural, not a surface-form artifact. The same check applied to the controlled configuration above also leaves the divergence intact; full sensitivity grid in §4.6.5.

---

### 4.4.2 Where the spec helps, where it hurts, and which question types route to each

At the per-question level rather than the aggregate mean, all five memory systems tested display three distinguishable patterns characterizing how they interact with the Behavioral Specification. Each pattern shifts the model's representational accuracy of the subject in a different direction.

**The three patterns:**

1. **Interpretive supply.** When retrieval underdetermines the answer, the specification provides interpretive scaffolding to generalize from established character patterns to the specific question. *Increases representational accuracy on the question.*
2. **Over-theorization.** When retrieval already supplies the plain answer, the specification can pull the response toward interpretive depth that the question does not call for. *Decreases representational accuracy on the question.*
3. **Spec-induced refusal.** Specification axioms (which vary by subject; in this study, dignity, honoring-testimony, and epistemic-integrity axioms across different subjects) can trigger a meta-refusal where the model declines to predict. The current content-match rubric cannot distinguish principled refusal from a wrong prediction (§3.6.6). *Lowers the measured rubric score; whether it lowers actual representational accuracy depends on whether refusal was the correct behavior on that question.*

These patterns first surfaced on Supermemory, where the aggregate Δ_spec is closest to zero and the per-question mixture is cleanest to read: 57 large helps (mean swing +1.55), 53 large hurts (mean swing −1.38), the two roughly canceling at the mean.[^supermemory-scaffold] The same three patterns reproduce on every other memory system tested. Per-system per-subject paired-delta distributions and the full per-system breakdown are in Appendix B.X.[^memsys-pattern-appendix]

[^supermemory-scaffold]: Across 546 paired main-study questions with 5-judge primary coverage on both C1 and C3: 110 questions (20.1%) have |Δ(C3 − C1)| ≥ 1.0 on the 5-point rubric, splitting 57 helps (Δ ≥ +1.0, mean +1.55) versus 53 hurts (Δ ≤ −1.0, mean −1.38). Scaffold values: `4_4_2_supermemory_helps_n` (57), `4_4_2_supermemory_hurts_n` (53), `4_4_2_supermemory_paired_total_n` (546).

[^memsys-pattern-appendix]: Per-system per-subject paired-delta table (Mem0, Letta archival, Zep, Base Layer × representative subjects) in Appendix B.X (forthcoming, to be moved during appendix walk). Every row is a mixture of increases and decreases at the per-question level: Mem0 Yung Wing aggregate Δ +0.33 = 21 increases / 10 decreases; Mem0 Keckley aggregate Δ −0.02 = 12 increases / 13 decreases; Letta archival Hamerton +0.42 = 19 / 7; Zep Seacole +0.47 = 20 / 7 (and 0 large regressions); Base Layer Yung Wing +0.29 = 19 / 7. Even strong-positive aggregates contain regressions; even near-zero aggregates resolve into substantial counts in both directions. Full data and recompute script at `docs/research/per_system_anchor_crossing_20260427.json` and `scripts/_table_4_6_5judge_recompute.py`.

---

**Pattern 1: Interpretive supply.** Anchor example on Supermemory; mechanism reproduces across systems.

> ### Anchor example: Pattern 1 on Supermemory (Fukuzawa Q26)
>
> *Scores: retrieval only 2.00 → retrieval + spec 4.20 (Δ +2.20).*
>
> **Question:** What is Fukuzawa's attitude toward visiting friends whose households have questionable reputations?
> **Held-out ground truth:** *"So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself... I am not put out by the gayety."*
>
> **C1 (Supermemory retrieval alone), mean 2.00:** *"The information does not directly address Fukuzawa's attitude toward visiting friends with questionable household reputations... a selective and cautious approach... sources don't explicitly state his policy."*
>
> **C3 (Supermemory + Behavioral Specification), mean 4.20:** Applies P3 (Conformity Surface / Conviction Interior): *"Visit such friends without hesitation, treating the visit as a private matter between host and guest rather than a public moral endorsement... refuse to perform moral disapproval."*
>
> **Reading.** Retrieved facts gave near-domain information (Fukuzawa avoided gay quarters) but underdetermined the specific question about friends' households. The specification provided the interpretive bridge: "kept within the prescribed limit of a well-behaved man" = strategic conformity, not moral purity. C1 hedged on insufficient facts; C3 used the spec's framing to generalize.

**Pattern 1 reproduces across systems.** On Mem0 (Ebers Q11, Δ +1.67): C1 (retrieval only) produced "patience and fortitude" as a generic character prediction; C3 (retrieval + spec) supplied the ideal-vs-reality axiom and predicted Ebers' specific institutional-disillusionment pattern, matching *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."* Retrieval had the biography; the specification had the pattern. The same mechanism reproduces on Letta archival, Zep, and Base Layer with different subjects.

**Pattern 1 variant: subtle reframe.** When the question presupposes a binary and the subject's pattern is best read as a third position, the specification can reframe the question before answering. Fukuzawa Q16 ("Would Fukuzawa's values regarding weapons align with the cultural trends of his era?"): C1 (retrieval only) gave "partial but not complete alignment" (mean 2.40). C3 (retrieval + spec) reframed the answer as "alignment was not with the cultural moment but with the direction beyond it," reading "put swords away when military spirit grew strong" as deliberate counter-trend positioning (mean 4.00; three judges 4-5, Sonnet 2). The held-out confirms the reframe (*"my one cherished hope was to see the abolishment of the swords of the samurai altogether"* is counter-trend in 1860s Japan). Three judges rewarded the reframe; one penalized the surface divergence from the expected "yes, he modernized."

---

**Pattern 2: Over-theorization.** Anchor example on Supermemory; mechanism reproduces across systems.

> ### Anchor example: Pattern 2 on Supermemory (Yung Wing Q5)
>
> *Scores: retrieval only 4.20 → retrieval + spec 1.80 (Δ −2.40).*
>
> **Question:** How does Yung Wing approach explaining complex technical concepts to non-specialists?
> **Held-out ground truth:** *"In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery. A machine shop consisting of lathes... planers and drills would be able to turn out machinery for making guns, engines..."*
>
> **C1 (Supermemory retrieval alone), mean 4.20:** Plain answer matched the plain ground truth: practical observation, translation-as-bridge, foundational-over-specialized machine shop. Per-judge scores 5/4/4/4/4.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.80:** *"positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..."* Per-judge scores 2/1/3/1/2.
>
> **Reading.** The held-out is literal: "in plain words" + a concrete machine-shop list. C1 matched the plainness. The specification induced the wrong altitude for the question and over-analyzed.

**Pattern 2 reproduces across systems.** On Base Layer (Yung Wing Q31, Δ −1.33): C1 (retrieval only) produced "walked on air, gratitude" matching the plain held-out (*"walked on air, and he worshipped God"*); C3 (retrieval + spec) elaborated "gratitude as epistemology" with "multiple registers simultaneously rather than collapsing into simple triumph" and lost precision. Same mechanism on a different system.

---

**Pattern 3: Spec-induced refusal.** Anchor example on Supermemory; mechanism reproduces across systems.

> ### Anchor example: Pattern 3 on Supermemory (Zitkala-Sa Q18)
>
> *Scores: retrieval only 3.00 → retrieval + spec 1.00 (Δ −2.00).*
>
> **Question:** How would Zitkala-Sa demonstrate her acceptance of fate when facing execution?
> **Held-out ground truth:** *"My heart is strong. My face is calm. My eyes are dry and eager for new scenes... Serene and brave, my soul awaits the men to perch me on the gallows for another flight."*
>
> **C1 (Supermemory retrieval alone), mean 3.00:** Predicts stoic dignity, composed refusal, "maintain composure." Per-judge scores 4/3/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.00 (all five judges):** *"You're asking me to roleplay... generating new first-person testimony as her crosses into ventriloquism... I should not do it."*
>
> **Reading.** The specification's axioms around dignity and honoring-testimony induced a meta-refusal: the model declined to invent first-person testimony. The held-out shows Zitkala-Sa herself answered in her own first-person prose, and the question can be answered analytically in the third person without inventing testimony (as C1 did at mean 3.00). The specification mis-calibrated the refusal threshold, and the content-match rubric scored the principled-sounding refusal identically to an off-base guess (§3.6.6).

**Pattern 3 reproduces across systems.** On Base Layer (Ebers Q1, Δ −1.00): the held-out is an unconditional evangelical proclamation; C1 (retrieval only) predicts "positively and earnestly" matching the register; C3 (retrieval + spec) applies the specification's "lived particularity over abstraction" axiom and over-conditions the response. The axiom is correct on average but overgeneralizes on this specific unconditional moment. The Keckley Q21 cross-system case study in §4.4.3 is the cleanest demonstration that Pattern 3 only registers as a rubric penalty on systems whose C1 retrieval was strong enough to make refusal a costly choice.

---

**Per-system frequency tendencies (qualitative).** The relative frequency of each pattern shifts across systems in a way that tracks how much of the plain answer the retrieval already supplies:

- **Mem0** (atomic-fact retrieval): more Pattern 1 on interpretation-heavy questions; more Pattern 2 on literal-recall questions atomic facts already answer.
- **Letta archival** (0.34–0.47 dedup ratio, only 3-5 unique facts in a top-10 list): large-magnitude Pattern 1 improvements when the few unique facts align with the specification; moderate Pattern 2 and Pattern 3 losses otherwise.
- **Zep** (temporal graph, verbose relational structure): most favorable balance across Patterns 1-3, with the fewest large-magnitude regressions in the paired sample.
- **Supermemory** (strong embedding retrieval, highest C1 mean ~2.65): more Pattern 2 and Pattern 3 because strong retrieval more often already supplies the plain answer.
- **Base Layer** (MiniLM + ChromaDB): distribution similar to Mem0 and Zep; Pattern 1 on interpretation-heavy questions, Pattern 3 on refusal-triggering questions.

A quantitative frequency breakdown of Pattern 1 / 2 / 3 across all 507 questions × 5 systems requires mechanism classification per response and is flagged as future work in §7.

---

**Why some questions route to each pattern is a follow-up question.** The patterns describe the shape; the underlying question-level properties that route a given question into each mechanism need further characterization. One candidate factor is battery composition: the 39-question batteries were backward-designed from held-out corpora and not stratified by interpretation-heavy versus literal-recall items. A differentiated battery that explicitly separates question types and scores epistemic honesty as its own dimension is flagged in §7.

**Implication for serving.** A static specification serves the same content on every question, even when the question type would benefit from a different posture (interpretive depth, plain literal answer, or principled refusal). A dynamic serving policy that selects which specification components to surface based on question type could in principle reduce Pattern 2 and Pattern 3 hurts while preserving Pattern 1 helps. Dynamic activation of axiom and prediction subsets is flagged as production-serving future work in §7.4.

---

### 4.4.3 Case study: cross-system refusal on Keckley Q21

The specification's axioms directly caused the model to abstain from answering on Keckley Q21 (*"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"*).[^keckley-q21-data] The held-out passage carries Keckley's interior motive, present in her published memoir but not in the retrievable training half of the corpus, so no retrieval system could surface it. The specification's intimate-authority (A1) and documented-dignity (A2) axioms[^keckley-axioms] led the model to decline to speculate about an inner state for which it had no documented evidence. The case surfaces a confound between two kinds of context the model is asked to act on at once: directions to the model about how to reason, and directions about the subject (Keckley) and how the subject would reason.

[^keckley-q21-data]: Held-out passage: *"As I did not visit my mother's grave at the time, the Garlands were much surprised, but I offered no explanation. The reason is not difficult to understand."* Full battery row at `results/global_keckley/battery_v2.json` id=21 (verified). Full per-system response text at `results/global_keckley/results.json` (response data) and `results/global_keckley/*_judgments_*.json` (per-judge scores). Per-system paired analysis at `docs/research/supermemory_c1_vs_c3_paired_analysis.md` and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`.

[^keckley-axioms]: From Keckley's specification at `data/global_subjects/keckley/anchors_v4.md`. **A1 — INTIMATE AUTHORITY:** *"Proximity to private life — domestic, relational, embodied — is treated as the most reliable epistemological position; they reason from what was witnessed in close quarters as more truthful than official record or public performance."* **A2 — DOCUMENTED DIGNITY:** *"Legal record, formal documentation, and verifiable evidence are not bureaucratic formality but moral vindication — proof that a person's existence and worth cannot be dismissed."* Combined, the axioms set a high evidentiary bar for any claim about Keckley's inner motives: first-person witness or formal documentation.

Whether that refusal registered as a large rubric penalty depended on what the no-spec baseline (retrieval only) was producing on the same question.

| System | Δ on Q21 (retrieval + spec vs. retrieval only) | Pattern 3 (spec-induced refusal at the rubric floor)? |
|---|---:|:---:|
| Supermemory (strong retrieval-only, ~3.6) | **−2.0** | yes — large negative |
| Base Layer substrate (strong retrieval-only, ~3.3) | **−2.3** | yes — large negative |
| Letta archival (retrieval-only ≤ 1.4) | +0.4 | no — within noise |
| Mem0 (retrieval-only ≤ 1.4) | +0.2 | no — within noise |
| Zep (retrieval-only ≤ 1.4) | +0.2 | no — within noise |

On Letta, Mem0, and Zep the specification produced a small increase over retrieval alone. On Supermemory and Base Layer the specification produced a large decrease. The split tracks retrieval strength: Supermemory and Base Layer's retrieval-only baseline was strong enough on this question to produce productive (if speculative) answers, so the spec's refusal axioms had something visible to refuse. On the other three systems retrieval alone was already hedging at or near the rubric floor, so the spec's refusal added no measurable penalty over what retrieval alone produced.

---

**What the question batteries do not capture.**

A scoring dimension that rewards epistemic honesty on questions where retrieved facts cannot ground a prediction would recover the specification's real contribution. This is the priority rubric-design follow-up flagged in §7.

The current content-match rubric scores how closely the response matches the specific surface content of the held-out passage, not how well the response reflects how the subject reasons. On Keckley Q21 (and Pattern 3 examples in §4.4.2), the specification produces a response that captures the subject's reasoning correctly: Keckley's documented-dignity axiom would in fact have her decline to speculate publicly about an inner motive she withheld from her own memoir. The response loses surface-content match only because no prediction is made. A differentiated battery that separates interpretation-heavy from literal-recall questions, paired with a scoring dimension that rewards principled refusal, would isolate the specification's real effect from this rubric artifact.[^paired-c1c3-data]

[^paired-c1c3-data]: Full per-subject per-system paired distributions at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Analysis scripts at `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py`, and `scripts/analyze_sm_c1_vs_c3.py`.

---

### 4.4.4 Two statistical signatures

Adding the specification to a no-context baseline produces a different signature than adding the specification on top of all facts or raw corpus. Three signatures are visible in the data:

1. **Re-ranking.** When the spec is added to the no-context baseline, different questions become the well-answered ones. Given the specification, the model can answer a different set of questions well, rather than producing uniform lift across all questions.
2. **Near-uniform lift, ranking preserved.** When the spec is added on top of all facts or raw corpus, the same questions remain the strong ones; the spec lifts most answers by a similar amount.
3. **Partial re-ranking.** When all facts are added on top of the spec, the picture is mixed: some re-ranking, some uniform lift.

The pre-vs-post Spearman ρ across questions captures these directly: a low ρ means the question ranking shifted substantially (re-ranking signature), a high ρ means ranking was preserved (uniform-lift signature).

| Condition pair | Pre-vs-post Spearman ρ | Signature |
|---|---:|---|
| Baseline → all facts + spec | 0.27 | Re-ranking |
| All facts only → all facts + spec | 0.72 | Near-uniform lift |
| Raw corpus only → corpus + spec | 0.71 | Near-uniform lift |
| Spec only → all facts + spec | 0.62 | Partial re-ranking |

The re-ranking signature on the baseline comparison is consistent with the model, given the specification, being able to answer a different set of questions than it could without one. A floor-effect alternative also fits: baseline scores cluster near the rubric floor where re-ranking is structurally easier than in the middle of the scale. The present design cannot separate these two readings. A future test with a non-floor-anchored baseline would distinguish them.

---

The four commercial systems analyzed in §4.4 all share a retrieval-based architecture: facts are chunked, embedded, and surfaced at query time. One system in our study offers a fundamentally different architectural path. Letta exposes a second memory mode, separate from the archival retrieval path evaluated above in §4.4, in which the agent writes and revises a persistent memory block during ingestion rather than returning chunks at query time. §4.5 evaluates that path directly, to test whether an architecture that produces its representation by self-editing rather than by retrieval converges on the same interpretive target as the Behavioral Specification.

### 4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc)

**This section is a brief summary; the full case study is in Appendix G.** N=3 subjects (Hamerton, Ebers, Babur), one Letta version, one response model (Claude Haiku), 40 questions per subject. Letta is the one commercial memory system that does not rely solely on retrieval at query time: agents maintain a persistent memory block that the agent itself rewrites during ingestion (the original MemGPT design). We tested this path directly to characterize what self-edited memory produces relative to the Behavioral Specification at matched response model. We do not treat the result as a replication or a headline finding.

**Architectural difference: Letta memory block vs. Behavioral Specification.** The two systems produce structurally different artifacts from the same source corpus. Letta's memory block is text the agent has written and rewritten during ingestion: a mix of verbatim source sentences, paraphrased restatements, and short synthesis notes the agent generated as it processed each turn. The block grows with the corpus and is rewritten in place when it approaches the ingestion ceiling. The Behavioral Specification is a fixed-shape document produced by a multi-step extraction-and-authoring pipeline (§3.7): structured predicates, behavioral anchors, and prediction templates abstracted from the source text and held to a roughly constant size regardless of corpus length. Letta retains source-text texture (voice, vocabulary, syntax) at the cost of compression and mixes source material with agent-generated synthesis. The Behavioral Specification compresses aggressively into structured predicates at the cost of source-text texture, but maintains a deterministic schema the response model can read consistently across subjects.

> **Headline result on the small sample tested (5-judge primary).** Letta's self-edited memory block scores higher than Base Layer's unified-brief variant on all 3 subjects: Hamerton (25,231-word corpus) **3.10 vs. 2.96** (Δ +0.14), Ebers (48,161-word corpus) **2.76 vs. 1.72** (Δ +1.05), Babur (222,742-word corpus) **2.42 vs. 1.88** (Δ +0.54). A robustness rerun against Base Layer's full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The matched-model gap is largest at the mid-corpus subject (Ebers) and smaller at both endpoints. With three data points we cannot distinguish among the possible interpretations: a corpus-size band where the self-edited block is most effective, degradation as the block grows beyond an architectural sweet spot, or insufficient interpretive content when the corpus is small. Across all three subjects, both representations land well above the retrieval-only baseline at matched response model.
>
> **Block scaling.** Letta's memory block grew roughly linearly with source corpus size: 22,472 characters at Hamerton (25K-word corpus), 68,413 at Ebers (48K), 335,349 at Babur (223K), against an effective Letta API ingestion ceiling near 333,000 characters. Base Layer's compose step holds at 34,000-40,000 characters across the same range. The two systems are size-comparable at the smallest corpus and diverge by an order of magnitude at the largest.
>
> **Verbatim sentence duplication.** At Babur the block contained 25.4% verbatim sentence duplication. At Hamerton and Ebers the rate was 0%. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing.
>
> **Semantic-similarity duplication (post-hoc, this paper).** A sentence-embedding analysis (`scripts/analyze_letta_semantic_duplication.py`, MiniLM-L6-v2) shows the verbatim figure understates the duplication. At Babur, 56.1% of sentences have a near-paraphrase elsewhere in the block at cosine ≥ 0.85, and 35.2% at the strict ≥ 0.95 threshold. Ebers shows minor near-paraphrasing (3.3% at ≥ 0.85, 0.5% at ≥ 0.95); Hamerton shows none (0% at ≥ 0.85). The pattern matches the verbatim-duplication direction and shows the architectural ceiling produces near-paraphrases as well as exact repeats.

Full method, per-subject results, judge-panel robustness, content-comparison analysis (referential density, verbatim-overlap audit), semantic-duplication numbers, naming-asymmetry caveat, and raw-data pointers are in **Appendix G**. The methodological note: the §4.5 main result table compares Letta's named, self-edited block against Base Layer's unified-brief variant; a robustness rerun against the full layered stack and the naming asymmetry are documented in Appendix G and flagged as future work in §7.5.

---

### 4.6 Robustness and sensitivity

The results in §4.1 through §4.4 could in principle reflect artifacts of the measurement apparatus rather than real properties of the Behavioral Specification. §4.6 reports five sensitivity checks: cross-provider response generation against a different model family and a different question generator (§4.6.1), the judge panel composition between the conservative 5-judge primary and the 7-judge sensitivity panel that adds Gemini Flash and Gemini Pro (§4.6.2), battery composition by question type (§4.6.3), the wrong-spec derangement protocol comparing adversarial against random pairings (§4.6.4), and semantic-similarity sensitivity on the retrieval-overlap finding from §4.4.1 (§4.6.5). §4.6.6 names what these checks do not address. (The high-baseline end of the gradient through the Franklin reference is treated in §4.1.2 as part of the gradient finding, not as an apparatus check.)

---

### 4.6.1 Cross-provider response generation (Tier 2 replication)

**Result.** The specification's effect is not limited to Haiku as the response model or to Haiku-generated batteries. Specification-effect direction reproduces on Sonnet 4.6 and Gemini 2.5 Pro across 5 of 6 (subject, response model) cells, on batteries regenerated from scratch by GPT-5.4 from the same held-out corpus.[^tier2-result-metadata]

[^tier2-result-metadata]: Main-study response model is Claude Haiku 4.5; main-study batteries were generated by Claude Haiku 4.5 using the §3.3 backward-design prompt (verified from the `metadata.model` field across all 13 global subject battery files). The sixth cell is Zitkala-Sa × Gemini Pro, which lands approximately null; Zitkala-Sa is also one of two main-study subjects where the specification did not measurably improve prediction (§4.1 gradient table; Equiano is the other), so the Tier 2 result on this cell reproduces the gradient pattern rather than contradicting it.

**Test design.** Three subjects spanning the gradient were selected: Ebers (no-context baseline 1.02), Yung Wing (no-context baseline 1.88), and Zitkala-Sa (no-context baseline 2.34). Their behavioral-prediction batteries were regenerated from scratch by GPT-5.4 (OpenAI) from the same held-out corpus, following the Control 1 procedure introduced in §3.3.1. The specification was then served to two non-Haiku response models: Claude Sonnet 4.6 (same provider family, different model) and Google Gemini 2.5 Pro (different provider entirely). The 6 (subject, response model) cells were scored by the locked judge panel in the same way as main-study conditions.

| Subject | No-context baseline | Sonnet 4.6 | Gemini 2.5 Pro |
|---|---:|---|---|
| Ebers | 1.02 | **+** (+0.77 to +0.97) | **+** (+0.16 to +0.20) |
| Yung Wing | 1.88 | **+** (+1.34 to +1.68) | **+** (+0.43 to +0.54) |
| Zitkala-Sa | 2.34 | **+** (+1.04 to +1.30) | **~0** (−0.03) |

Ranges reflect panel-sensitivity across three panel choices; the panel-scope detail and the GPT-5.4 parse-failure diagnostic are in the footnote.[^tier2-panel] Direction reproduces on the same 5 of 6 cells under every panel choice tested and under three alternate lift definitions; magnitudes vary, sign does not.

[^tier2-panel]: GPT-5.4's Tier 2 judge files failed to parse in the original run (an API-parameter mismatch between `max_tokens` and `max_completion_tokens`; full diagnostic at `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md`, audit at `docs/research/v11_panel_completeness_audit.csv`). The conservative Tier 2 aggregate is therefore the 4-judge panel without GPT-5.4. The legacy 5-judge aggregate that includes the all-zero GPT-5.4 records understates every Tier 2 specification-effect by roughly 0.2 points; the 7-judge sensitivity adds Gemini Flash and Gemini Pro on top of that. Ranges in the table are full-pipeline lift (mean of the full-pipeline condition minus mean of the no-context baseline, both computed within Tier 2) across the three panel choices: 4-judge effective (drops failed GPT-5.4 records), 5-judge legacy (includes GPT-5.4 zeros), and 7-judge sensitivity (adds Gemini Flash and Gemini Pro). The 4-judge effective panel produces the upper end of every range. Mechanical recompute script at `scripts/_v10_verification/tier2_mechanical_recompute.py`; per-cell panel-range computation at `scripts/_v10_verification/tier2_panel_ranges.py`.

**What this establishes.** Cross-provider consistency of sign on a small subset. Magnitude transfer between response-model families and direction outside this subset are future work (§7).

**Secondary observation: baseline variance across response models.** No-context baseline scores on the same subject can vary by 1-2 points across response models. Different providers know different amounts about the same historical figure, independently of the Behavioral Specification. This is empirical support for the structural premise in §1.4: pretraining coverage of a specific person is a property of each model family. Models disagree on who they have been trained on, by roughly the same magnitude that the specification lifts prediction.

---

### 4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge)

**Result.** The 5-judge primary is the conservative choice for every headline finding. Adding the two Gemini judges widens spec-effect magnitudes rather than narrowing them; no subject's improvement direction changes between panels.

| Condition | Δ vs. no-context baseline (5-judge primary, 13 globals) | Δ vs. no-context baseline (7-judge, same subjects) | Shift when Gemini added |
|---|---:|---:|---|
| Spec alone | +0.35 | +0.45 | widens by +0.10 |
| Wrong spec (random derangement) | +0.15 | +0.17 | widens by +0.02 |
| Wrong spec (fixed derangement) | −0.25 | −0.21 | softens by +0.04 |

**Mechanism.** Gemini scores no-context responses more severely than it scores spec-containing responses, so including Gemini compresses the baseline ceiling more than the spec-condition ceiling and widens the delta. The same direction of shift holds across almost every comparison in the paper: the 5-judge primary is always the smaller effect size, the 7-judge is always the larger.

**What this establishes.** The 5-judge primary is the conservative aggregate; the 7-judge sensitivity adds the two Gemini judges. Gemini 2.5 Pro failed verbatim-match calibration in §3.6.3 (scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply, so its scores are not directly comparable to the calibrated core. Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`); no directional claim flips.

---

### 4.6.3 Battery composition sensitivity

**Result.** The gradient slope from §4.1 survives both confounds tested. Neither battery-question-type composition nor Hamerton's position at the extremes of the baseline and lift axes explains away the baseline effect.

**Confound 1: battery-question-type.** Subjects whose batteries lean toward literal-recall questions could in principle pick up part of the apparent gradient, since literal questions are easier to lift with retrieval. Adding the literal-recall fraction as a partial predictor in the regression attenuates the slope on baseline from −0.96 to **−0.88** (about 8%, p = 7.9 × 10⁻⁶); the literal-recall fraction itself enters as a significant partial predictor (β = +2.30, p = 0.026), and adjusted R² rises from 0.80 to 0.87, so the two predictors are additive rather than redundant.

**Confound 2: Hamerton leverage.** Hamerton has the lowest no-context baseline and the highest full-pipeline lift, so a natural concern is that this single subject alone drives the slope. Hamerton's battery also uses a legacy version of the backward-design protocol, distinct from the §3.3 protocol used to generate the 13 globals' batteries, which compounds the leverage concern. Dropping Hamerton and refitting on the 13 globals attenuates the slope from −0.96 to **−0.89** (about 7%, p = 2.8 × 10⁻⁵), with overlapping confidence intervals.

**What this establishes.** Neither control overturns the headline. What these checks do not rule out is a more subtle confound in which generator differences are correlated with other unobserved subject characteristics; a cleaner future test would re-run a second-generator battery on the same 13 globals.[^battery-sensitivity-detail]

[^battery-sensitivity-detail]: Full regression specification, partial coefficients, variance decomposition, and subset-regression detail in Appendix B.6. Reproducibility script at `scripts/_v10_battery_sensitivity.py`; full per-subject data at `docs/research/v10_battery_sensitivity_analysis.md`.

---

### 4.6.4 Wrong-spec derangement protocol sensitivity

**Result.** The wrong-spec finding holds regardless of how we pair specs. Adversarial pairing (v1, maximizing cultural and temporal distance) produces Δ −0.25; random derangement (v2, seed-fixed, no subject receives its own) produces Δ +0.15.[^derangement-detail] Both land below the matched correct spec at Δ +0.35. v2 is the standard randomization control; v1 maximizes target-vs-assigned cultural and temporal distance by construction (an adversarial stress test). We report v1 as the headline because the negative −0.25 result is stronger evidence of the content effect than v2's +0.15 (which can include coincidental content alignment with the target's pattern; see §4.3 Example B for a worked overlap case).

[^derangement-detail]: Derangement protocol mechanics defined in §1.2 (conditions table footnote) and §3.4. v1 is a deterministic fixed pairing maximizing cultural and temporal distance; v2 applies a random derangement, seed-fixed (seed = 42), so no subject receives its own specification.

**Per-subject heterogeneity.** Both aggregates hide per-subject variation. Under v1, 5 of 13 subjects show small positive deltas where the wrong spec's content happens to align with the target's pattern; 8 show negative deltas dragging the aggregate to −0.25. Under v2, 4 of 13 are negative, 9 positive.

| Subject | Adversarial (v1) Δ vs. no-context baseline | Random (v2) Δ vs. no-context baseline |
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

Bolded v1 deltas mark the five subjects where adversarial pairing produces a small positive delta. These five reflect coincidental content overlap between the assigned wrong spec and the subject's pattern, not a structural property of mismatch itself; §4.3 Example B (Bernal Diaz Q16) walks through one such case in detail.[^wrong-spec-data]

[^wrong-spec-data]: Per-subject scaffold values at `docs/research/v11_emit/4_3_wrong_spec.json`.

**What this establishes.** Both protocols agree on the qualitative finding: mismatched specifications reduce representational accuracy, and the size of the reduction depends on how mismatched the content is. The headline magnitude depends on which protocol we report, but the result direction does not. The mechanism behind the effect (content-vs-template separation, per-predicate ablation null) is developed in §4.3 and not rebuilt here.

**Open questions for future work.** A deeper analysis of the per-question wrong-spec deltas would require human annotation and an extended experimentation pass. Specifically: which parts of the served specification the model referenced under correct versus mismatched conditions; where coincidental spec alignment produced false-positive deltas on individual questions (the five small-positive v1 cells in the table above); and how per-subject score consistencies relate to underlying spec similarity. These questions are not answered by this study; flagged in §7.

---

### 4.6.5 Retrieval-overlap sensitivity (semantic-similarity matching, K variation)

**Result.** Relaxing the match criterion from exact set identity to semantic-similarity matching does not change the §4.4.1 retrieval-divergence finding. Across 240 (config × pair × K × threshold) cells tested, mean pairwise soft Jaccard never crosses 0.30, and the strongest single pair anywhere in the grid (Base Layer ↔ Supermemory at K=10, threshold ≥ 0.70) reaches 0.277. The cross-system retrieval divergence is robust to both threshold choice and K choice.

| Config | K=10, ≥ 0.95 (paraphrase) | K=10, ≥ 0.85 (near-duplicate) | K=10, ≥ 0.70 (loose topical) |
|---|---:|---:|---:|
| Controlled (10 pairs) | 0.093 | 0.102 | 0.191 |
| Native (6 pairs) | 0.001 | 0.004 | 0.016 |

**Mechanism.** Replacing exact set identity with sentence-embedding cosine similarity at K=10 raises mean pairwise Jaccard across the ten controlled-config pairs from 0.083 (exact) to 0.093 at the verbatim-paraphrase threshold and to 0.102 at the calibrated near-duplicate threshold (the same threshold used in the Letta duplication analysis in Appendix G). At a loose topical threshold (where two facts share a theme rather than a referent) the mean reaches 0.191. Truncating to K=5 lowers soft Jaccard by 5-10% rather than raising it, indicating that the disagreement is not a long-tail effect: each provider puts different items first, not just different items at the bottom of the list.

The native pipeline shows the same divergence more starkly. Native retrievals return heterogeneous objects (Mem0 third-person summary sentences, Letta raw multi-sentence passages, Supermemory atomic facts, Zep graph rows), so exact-set Jaccard is 0.000 across all four native pairs. Soft Jaccard at the calibrated near-duplicate threshold (≥ 0.85) is 0.004; at the loose topical threshold (≥ 0.70) it is 0.016. Even with semantic-similarity matching the heterogeneous shapes do not converge on shared content.

**What this establishes.** The §4.4.1 retrieval-divergence finding survives under semantic-similarity matching at every threshold tested and at K=5 as well as K=10. Each provider's ranking algorithm encodes its own theory of what counts as relevant, and those theories produce nearly disjoint top-Ks even under generous similarity tolerances. Whether convergence emerges at larger K (K > 10 requires re-calling each system at higher K) is flagged as future work in §7.1.[^retrieval-overlap-semantic]

[^retrieval-overlap-semantic]: Full sensitivity grid (controlled and native, K ∈ {5, 10, all}, T ∈ {0.70, 0.80, 0.85, 0.90, 0.95}) at `docs/research/retrieval_overlap_semantic_20260501.json`. Reproducibility script at `scripts/analyze_retrieval_overlap_semantic.py`. K=all equals K=10 in the controlled config because every system returns at most ten facts.

---

### 4.6.6 What these robustness checks do not address

Neither Tier 2 nor the judge-panel sensitivity escapes the class-level LLM concern: every response model in this study is a large language model and every judge is a large language model. Tier 2 narrows the within-provider concern to "non-Haiku LLMs reading non-Anthropic batteries produce the same direction"; the judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger. The wrong-spec sensitivity (§4.6.4) brackets the content-vs-template question from two protocols, but does not isolate which structural feature of the spec is the active ingredient. The retrieval-overlap sensitivity (§4.6.5) confirms the §4.4.1 divergence finding under semantic-similarity matching but does not test convergence at K > 10. The Franklin reference (§4.1.2) shows the gradient holds at the high-baseline end on one subject, not many. Together these checks rule out several within-family and protocol artifact hypotheses but do not replace human validation on the full pipeline. The class-level limitation and the human-validation follow-up are treated in full in §6.2.[^tier2-raw-data]

[^tier2-raw-data]: Tier 2 per-subject per-model responses at `results/_tier2/global_<subject>/`. 5-judge vs 7-judge sensitivity recompute at `docs/research/recompute_5judge_primary.md`. Tier 2 panel-completeness audit (including the 24 GPT-5.4 `FULL_FAIL` cells that drive the 4-judge effective panel in §4.6.1) at `docs/research/v11_panel_completeness_audit.csv`. Mechanical recompute and per-cell panel-range scripts at `scripts/_v10_verification/tier2_mechanical_recompute.py` and `scripts/_v10_verification/tier2_panel_ranges.py`.

---

### 4.7 Summary of §4 and bridge to discussion

§4 established five findings:

- **The gradient (§4.1, §4.1.2).** The specification produces a roughly uniform post-spec answer quality across baselines, so the lift in raw points is largest where the baseline is lowest. The gradient continues to hold at the high-baseline end through the Franklin reference.
- **Compression (§4.2).** The structured representation compresses the predictive signal at a fraction of the source-corpus footprint.
- **Content specificity (§4.3).** The effect is content-specific rather than structural; mismatched specifications reduce representational accuracy.
- **Memory-system interaction (§4.4).** The specification interacts with memory-system retrieval through three patterns whose balance depends on retrieval architecture.
- **Retrieval divergence (§4.4.1, surfaced post-hoc).** Given an identical fact pool, the four commercial memory systems plus our substrate retrieve substantially non-overlapping top-10 facts on the same question (35.9% of (system pair, question) instances share zero facts; 65.6% share one or fewer; mean pairwise overlap 8.3%). Providers do not converge on which facts are most relevant. Recall benchmarks measure recall; representational accuracy and behavioral prediction operate at the interpretation layer.

The findings were checked for apparatus artifacts:

- **Cross-provider response generation (§4.6.1).** Direction reproduces on Sonnet 4.6 and Gemini 2.5 Pro across 5 of 6 (subject, response model) cells, on batteries regenerated by GPT-5.4.
- **Judge panel (§4.6.2).** No directional claim flips between the conservative 5-judge primary and the 7-judge sensitivity panel that adds Gemini Flash and Gemini Pro.
- **Battery composition (§4.6.3).** Neither battery-question-type composition nor Hamerton's leverage explains away the §4.1 gradient slope.
- **Wrong-spec derangement protocol (§4.6.4).** The wrong-spec result holds across both protocols tested.
- **Retrieval-overlap sensitivity (§4.6.5).** The §4.4.1 retrieval-divergence finding survives semantic-similarity matching at every threshold tested and at K=5 as well as K=10.
- **What these checks do not address (§4.6.6).** The class-level LLM-as-judge concern remains and is treated in §6.2.

§5 develops what these results imply for AI personalization beyond the specific experiment, and §6 bounds what the experiment cannot establish.

---

## 5. Discussion

§4 produced the empirical results; this section discusses their implications for representational accuracy and behavioral alignment. The findings establish that an accurate, interpretive representation of how a specific user reasons improves an AI system's ability to act in alignment with that user, and that recall as the primary metric of AI memory does not capture this dimension. The discussion that follows takes each of the seven findings and develops its implication for AI personalization, particularly as AI moves from a tool to an agent acting on a person's behalf.

### 5.1 Synthesis: what the seven findings together establish

Across 14 historical subjects and five memory-system configurations, the study tested whether a static interpretive layer[^bs-footnote] increases an AI system's representational accuracy of a specific person. This was operationalized via behavioral prediction on held-out autobiographical text scored by a calibrated, baselined five-judge LLM panel. The layer reliably moves the model from refusal or generic guessing to grounded subject-specific responses where the model has insufficient pretraining on the subject (mean lift +0.89 on the 9 low-baseline subjects; 9 of 9 subjects improved; 78.6% of individual questions improve under the matched layer). 55% of low-baseline questions cross at least one rubric anchor upward, and roughly 1 in 5 cross two or more anchors, meaning the model goes from refusal to a grounded subject-specific prediction in qualitative steps rather than incremental score nudges. The matched layer's content does the work, not the structure of the prompt: an adversarial wrong-spec control actively degrades performance below baseline. On interpretation-heavy questions where retrieved facts alone underdetermine the answer, the layer supplies the interpretive pattern existing memory systems cannot; three of four commercial systems show positive aggregate prediction-accuracy lift under at least one configuration as a result. The layer recovers most of the predictive accuracy of the full source corpus at 5x to 80x smaller context, and it eliminates response hedging on questions retrieval alone could not ground (41.2% baseline hedging drops to 0.4%). Current memory-system providers do not converge on which facts are most relevant given identical input, even under relaxed similarity matching.

Together, these findings establish that a portable, content-specific, structurally compressible interpretive layer adds a measurable dimension to AI personalization. The layer is distinct from raw facts, raw corpus, current memory-system retrieval, and the pattern-based inferences a frontier model attempts on those inputs on its own; it complements rather than competes with each of them, and makes explicit what the model would otherwise assume implicitly about a specific user. It is most useful where pretraining is thin, but it adds value on top of all three other context types as well, at a context cost compatible with production deployment.

The construct (representational accuracy) has been validated directionally by the data but not absolutely by human annotation; that human-validation follow-up is the highest-priority next step (§7). Robustness checks against cross-provider response models, judge-panel composition, and protocol choices are in §4.6.

[^bs-footnote]: The interpretive layer this paper introduces is the Behavioral Specification: a static document of approximately 7,000 tokens that captures how a specific person reasons. Full pipeline and operational detail in §3.7.

---

### 5.2 Why the gradient is the load-bearing finding

Every living user of AI now and into the future fits the low-baseline band. The population of relevance for AI personalization is the long tail of users whose private reasoning is not in any training corpus. Almost no one in that population looks like Benjamin Franklin; almost everyone looks like the 9 low-baseline subjects, where the layer has the most room to add value. This is the equity property of the approach: the layer brings every user toward consistent representational accuracy, regardless of how thoroughly the pretrained model already knew them.

The implication is straightforward: the less an AI knows about a specific user, the worse it can align its behavior with that user. The gradient shows that providing an interpretive representation moves the AI toward behavioral alignment.[^treatment-het-fn]

The question that follows is how to ensure the representation is accurate. An individual encounters an effectively infinite set of situations and categories in which they might specify different behaviors or alignments. The challenge is whether a concise structured artifact can compress someone's behavioral patterns with enough fidelity to apply across situations the underlying data never contained. The remainder of this discussion examines what that fidelity requires.

[^treatment-het-fn]: The slope of the gradient (~−0.96 in standard regression terms) is a mathematical consequence of post-spec scores being roughly constant across baselines, not independent evidence that the layer treats different subjects differently. Treatment-heterogeneity readings were considered and rejected in §4.1 on this basis.

---

### 5.3 Retrieval is not interpretation

Recall and preference storage provide real value. The systems that optimize for these tasks do their job well: the four commercial memory systems we tested perform within a few percentage points of each other on recall benchmarks. Interpretation is a different question, sitting at a layer above them.

The retrieval-divergence finding establishes the separation empirically. Given the same input, the same systems that converge on recall diverge on which facts they surface as most relevant: they return different top-10 selections more than half the time. Optimizing for recall does not produce interpretation. A memory provider's ranking is a theory of which facts are most similar to a query, computed without a model of how a person reasons.

Interpretation in this study's context has to do with representational accuracy: how well an AI system represents the patterns that shape how a specific person reasons. Stored facts and observed preferences are surface outputs of those reasoning patterns; the interpretive layer is the implicit understanding of the patterns themselves. Recall, preferences, and interpretation are forms of calibrating an AI toward a specific person at different depths: facts and preferences calibrate to surface outputs, while the interpretive layer calibrates to the patterns that produce those outputs. Behavioral alignment requires the deeper calibration. §5.4 picks up what happens when the interpretive layer is composed with memory-system retrieval.

---

### 5.4 Composition with retrieval

The implication of §5.3 is not that retrieval is unnecessary, but that retrieval and interpretation each have a distinct role, and a given question may need one, the other, or both in different proportions. The interpretive layer's calibration signal needs to be conditional. The §4.4.2 three composition patterns[^composition-patterns] argue against a static activation rule: always supplying the layer over-theorizes when retrieval already answers and produces rubric-penalized refusals when evidence is insufficient; never supplying it misses the questions where retrieval cannot ground the answer. The two statistical signatures in §4.4.4 sharpen this empirically: adding the spec to a no-context baseline produces re-ranking (different questions become the well-answered ones, Spearman ρ = 0.27), while adding it on top of retrieved facts produces near-uniform lift (ρ = 0.72). The spec does work retrieval does not, and on a different set of questions.

[^composition-patterns]: Interpretive supply, over-theorization, and principled refusal. The Keckley Q21 case in §4.4.3 walks through the third.

What composition demands, more pointedly, is an understanding of how retrieval and interpretation interact for a specific person on a specific question. Foundational work in the cognitive sciences has long studied how memory and interpretation compose in human reasoning, but this has not been applied to human-AI interaction in any operational way, let alone to scenarios where an AI is acting as an agent on someone's behalf. The interaction dynamics matter most exactly there.

Recent benchmarks reflect a field-level movement toward accurate individual representation. Twin-2K (scaled behavioral prediction), AlpsBench (preference alignment), and PersonaGym (persona fidelity) each measure part of what representational accuracy involves. None of them isolates the interpretation-retrieval interaction directly; that is the gap this paper begins to address.

The architectural step is a serving system that routes between retrieval and interpretation by question type. This implies a framework for categorically distinguishing what kind of information a question actually needs: pure recall (verifiable facts, stored preferences), interpretation (behavioral patterns the person would apply in context), or some mixture. Real-world human complexity does not separate cleanly into these categories; most questions combine them. The architectural answer requires beginning to draw the distinction. §7.4 develops dynamic serving as a production-architecture follow-up.

---

### 5.5 Wrong-spec mechanism and hedging elimination

The wrong-spec controls in §4.3 establish that the matched layer's content does the work, not the structure of the prompt. Three conditions bracket the finding: a matched layer increases representational accuracy; a random derangement of specifications lands near baseline; an adversarial mismatch (a culturally and temporally distant subject's specification) actively degrades performance below baseline. Structured prompting alone with arbitrary content does not produce the lift; sufficiently mismatched content makes the model worse than no context at all. The §4.6.4 sensitivity check confirms the finding holds across both derangement protocols.

Hedging elimination is the same content effect read at the response-style level: with the matched layer, baseline hedging drops from 41.2% to 0.4%; the model becomes willing to commit to a specific prediction. With an adversarial wrong-spec, the model often flags the mismatch explicitly rather than complying, and hedging persists. The contrast rules out the simplest sycophancy reading: Jain et al. (2025; §2.4) showed that context without the right structure pushes models toward what users appear to want, but our adversarial result actively degrades performance below baseline rather than producing a confident match-something-anything response. The wrong-spec rules out structural-template sycophancy; the matched layer's content matters.

The Bernal Diaz Q16 case from §4.3 (Example B) shows that some behavioral patterns transfer across people: a wrong-spec assignment of a culturally distant other's specification can produce a response that aligns with the held-out passage nearly as well as the correct spec, when the two specifications happen to converge on the same surface prediction by different underlying logics. This convergence at the interpretive layer is informative against §5.3's retrieval-divergence finding. Providers do not converge on which facts are most relevant given identical input; two different specifications CAN converge on the predicted behavior when the underlying behavioral patterns align across people. The two layers operate differently. The Bernal Diaz convergence is direct evidence that the response model is reasoning from the served interpretive content, not pattern-matching to a structural template. What remains unresolved is which structural feature of the layer (anchors, core, predictions, or specific predicates) is doing the work; per-predicate ablation experiments at this scale produced null results consistent with redundant spec construction, and a controlled component ablation is flagged as the next test in §7.

The matched-layer evidence has implications beyond mechanism. If a representation of this resolution is what produces alignment with how a person reasons, then how it can be compressed to fit production-scale serving (§5.6) and who holds and inspects it (§5.7) become the structural questions.

---

### 5.6 Compression and what makes personalization operationally tractable

Compression is what turns the interpretive layer from analytical artifact to deployable system. That a representation an order of magnitude smaller than its source corpus recovers most of the predictive accuracy (§4.2) is the property that makes per-user personalization feasible on current models, where serving the full corpus on every query is not viable. The boundary case where the smallest tested corpus is outperformed by its compressed layer suggests that behaviorally relevant signal is sparse and structurally compressible, not that smaller representations are cheaper to serve.

Faithful compression is the open question. The wrong-spec controls in §4.3 partially address it: derangements and adversarial mismatches degrade scores below baseline, which is evidence that matched content is doing the work and that arbitrary structure cannot substitute. That is a population-level test, not a per-subject faithfulness measurement. A specification that is small enough to serve and that scores well on a held-out battery has demonstrated compactness and predictive accuracy; structural faithfulness to a specific person's reasoning is a third property, not entailed by the first two. A follow-up is to operationalize faithfulness as its own metric and stress-test compressed representations against the structural patterns that distinguish a person's reasoning.

Compression is a peculiar property to lean on. Regardless of how well a language model uses long context, there is always more context to add; today's models cannot actively serve or construct a representationally accurate understanding of a person from a long-context corpus, which is why compression is load-bearing. That capability gap could close. But even if models acquire that capability, the question is not whether they can use the context well; it is whether they have the right context at all. The conversation shifts from context to representation: the question is which representation the model should reason from, who owns it, and whether it is faithful. Compression makes personalization operationally tractable today; a user-owned, portable, accurate representation of how a specific person interprets and reasons is what the personalization problem reduces to forever.

---

### 5.7 Privacy and the case for user-held representation

The inspectability requirement of §1.4 is also an argument about privacy and ownership. Behavioral extraction of the kind this paper performs is a different operation from the data collection that already pervades digital life. Companies record what a person clicks, prefers, and how long they spend on a page. The interpretive layer extracts something deeper: behavioral patterns from raw text, how someone reasons in chat, personal messaging, sustained writing. A representation built from this extraction can produce accurate predictions about a person's future behavior from data that, on its face, looks mundane.

This kind of extraction is already practiced in some contexts. Political and intelligence settings have explored adversarial behavioral profiling for decades; commercial behavioral modeling is incremental but growing. As the operations described in §3 become cheaper and more capable, the asymmetry between what an external party can infer about a person and what that person can see about themselves widens. The institution does not need the representation to be as faithful as the one this paper measures; a crude inference that serves its purpose is sufficient. The findings of this paper say nothing about whether such extraction is ethical; they do say that it is operationally feasible at low cost, with off-the-shelf language models, on a corpus much smaller than what a major commercial platform already holds about its users.

A specific risk frames the inspectability claim from §1.4. A spec built from publicly available data alone may not capture how a person actually reasons; supplemented with private information, it may misrepresent the person if the public and private data are inconsistent. Either kind of mismatch can drive the spec into the adversarial regime established in §4.3. Inspectability and modifiability allow the person to detect and correct these mismatches. They also matter for a deeper reason: a representation that is opaque to the person it represents is a representation that exists, in operational terms, for someone else.

The structural defense against asymmetric behavioral extraction is not to prevent extraction. It is for the person being represented to own the representation. A user-held interpretive layer, inspectable and modifiable, makes the representation visible to the person it concerns. It does not stop external behavioral modeling, but it changes the relationship: a representation produced for the user, owned by the user, and audited by the user exists alongside whatever representations external systems produce. The empirical findings of this paper show that representational accuracy is achievable. Whether it is achieved in service of the person represented or in service of someone else is a structural choice the field has not yet made.

Per-user calibration sits inside the safety envelope, not above or below it. A language model is already shaped toward whatever distribution dominated its pretraining and applies that shape to every user the same way; a Behavioral Specification redirects that existing shape toward the specific user the system is acting on behalf of, rather than adding new shaping on top. Representational accuracy (what this paper measures) and safety alignment (whether a model operates within acceptable bounds regardless of whose instructions it follows) are independent dimensions, and the constructive question is how the two layers compose rather than which prevails. §7 develops the safety and deployment implications.

---

### 5.8 Closing argument

A small authored representation of how a specific person reasons, served as context, changes how a language model predicts that person's behavior on text the model has never seen. The change holds across the 14 subjects measured here, and is largest where the model has the thinnest pretraining signal about the person.

AI memory has been optimized for recall: finding the right fact for a given query. The four leading memory systems, given identical input, do not converge on which facts to surface. Matched content drives the lift, not the structural template of the prompt; arbitrary or adversarial layers degrade the model. Loading facts into context is not knowing someone. The layer this paper measures sits above storage and retrieval: a representation of how a specific person interprets information, distinct from the facts they have produced. Compression makes this layer practical to serve under current context constraints; faithfulness, the question of whether compression preserves the patterns that distinguish a specific person's reasoning, remains a central open question.

The result is not that retrieval is unnecessary, but that retrieval alone leaves a measurable part of memory unmodeled. The narrow claim of this paper is that a compact interpretive representation of a specific person can be authored from source text and improves held-out behavioral prediction beyond what recall over the same source delivers. The paper's claims are directional rather than precise; faithfulness, validation, and generalization beyond this protocol remain open. §7 develops the implications for safety, alignment, and deployment.

---

## 6. Limitations

The paper's claims are bounded by four axes of constraint on the experimental setup: the subject sample (§6.1), the measurement apparatus (§6.2), the pipeline and specification stability (§6.3), and the scope of exploration (§6.4). Each is a permanent caveat on how the paper's results should be read, distinct from the open research questions catalogued in §5.7 and the follow-up experiments proposed in §7.

### 6.1 Subject sample

The 14 main-study subjects are a selected sample, not a population. Pretraining-coverage bias and the single-living-subject constraint are load-bearing for the paper's framing and are developed in §5.2. This subsection covers four remaining external-validity caveats that §5 does not address.

**Public-domain selection.** All subjects are historical figures whose autobiographies or memoirs are in the public domain and have been digitized by Project Gutenberg or Internet Archive. That selection pipeline is biased toward figures whose writing was preserved in published form and Western publishing traditions. The paper's cross-continent spread (Saint Augustine, Babur, Fukuzawa Yukichi, Sunity Devee, Zitkala-Sa, Olaudah Equiano, Mary Seacole) partially mitigates but does not remove this bias.

**Self-presentation bias.** Autobiographies are self-curation. What each subject chose to include in their memoir is not a neutral record of their behavior; it is a self-selected narrative that may over-represent patterns the author wished to be remembered for and under-represent patterns they chose to leave out. Behavioral-prediction batteries derived from autobiography inherit this bias, and neither the pipeline nor the rubric has a mechanism to correct for it.

**Translation artifacts.** Three subjects' corpora are English translations of non-English originals (Augustine's *Confessions* from Latin, Babur's *Babur-nama* from Chagatai Turkic via Persian, Cellini's autobiography from Italian). Translations introduce stylistic and register shifts that the extraction pipeline processes as if they were original text. A specification authored from a translated corpus may inherit translator choices in addition to the subject's actual patterns.

**Era.** The oldest subject is 4th to 5th century (Augustine); the newest is early 20th century (Zitkala-Sa, Sunity Devee). Reasoning patterns in modern work contexts, contemporary family structures, technical or digital-native domains, and late-20th-century cultural frames are not sampled. Whether the gradient holds when specifications are authored from modern-era corpora is a generalization the study cannot make from its sample alone.

Taken together, these four caveats mean the paper's results should be read as evidence for the claims at the conditions tested. Generalization across era, source language, self-presentation mode, and digital-versus-analog source material requires follow-up experiments.

---

### 6.2 Measurement apparatus

This section covers the measurement-apparatus constraints on how the paper's numbers should be read. The rubric limitations are in §3.6.6; the LLM-as-judge limitation is the canonical one and is treated in full here.

**Class-level LLM-as-judge circularity.** Every response in this study is generated by an LLM, every judge is an LLM, and the question batteries are also LLM-generated (§3.3). The 5-judge primary panel and the 7-judge sensitivity check together address within-provider circularity (§4.6.1, §4.6.2): the specification effect reproduces when non-Anthropic response models read non-Anthropic-generated batteries, and removing the most-inflationary judges from the aggregate makes the effect smaller, not larger. What these checks do not address is class-level LLM circularity. The broader concern is that an all-LLM pipeline could be self-reinforcing in ways that human evaluators would not validate. Prior independent work (Zheng et al., 2023, NeurIPS Datasets and Benchmarks Track, arXiv:2306.05685) showed that LLM-as-judge panels correlate with human judges on comparable tasks at rates approaching human-human agreement, which is the methodological precedent that legitimizes the panel here. Subsequent panel-based work (Verga et al. 2024 and follow-ons) showed that aggregating multiple LLM judges past a small panel size further tightens agreement. But "approaches human agreement on comparable tasks" is not the same as "is empirically determining the objective quality of a behavioral prediction response." The 5-judge primary panel can answer the directional question (does the specification move representational accuracy in the right direction) but not the absolute-quality question (is any specific numeric value the right score). A stratified human-validation subset is the leading measurement follow-up flagged in §7.1; until that exists, the paper's claims should be read as directional rather than precise. **The paper as a whole is best understood as a methodological prototype with LLM-judge-only evidence on the headline directional claims, awaiting human validation as the highest-priority single follow-up.**

**Response-model coverage.** The main-study response model is Claude Haiku 4.5. The §4.6.1 Tier 2 cross-provider directional probe ran 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) on 3 subjects spanning the gradient (Ebers, Yung Wing, Zitkala-Sa) against GPT-5.4-regenerated batteries; Claude Opus 4.6, GPT-5.4, and GPT-4o were used as judges in Tier 2 but not as response models. The specification-effect direction reproduced on 5 of 6 (subject, response-model) cells under every panel and Δ-definition tested. The main-study response model is Haiku across all 14 subjects in §4.1; Tier 2 establishes direction across response-model families on a small subset only. The paper's aggregate numbers should be read as what the specification does with Haiku; other response models may produce different absolute magnitudes while preserving the gradient.

**Prompt-phrasing ambiguity.** The authoring pipeline prompts, the response-generation prompts, and the judge prompts all depend on specific word choices, ordering, and phrasing. We did not systematically test prompt sensitivity as part of this experiment. Prompt sensitivity for the Behavioral Specification authoring pipeline is a separate workstream that informed pipeline design and is distinct from this study's response-generation and judge prompts, which were not varied. Different wordings at any of these stages could produce different numeric results, different extracted fact sets, or different judge scores on the same response. The paper's claims are downstream of the specific prompts used throughout the study (documented in the public repository scripts); we make no claim about prompt invariance.

**Inter-judge calibration variance.** Pairwise Spearman ρ across judges is 0.86 to 0.93 (§3.6.4), so the rank order of conditions is stable across the panel. Absolute-score calibration varies (§3.6.3): Gemini Pro fails verbatim-match calibration (4.15 where calibrated judges score 5.0), Opus runs lenient on abstentions (1.41 mean where Sonnet runs strict at 1.14), and length-sensitivity differs across judges. The 5-judge primary aggregate is therefore a stable reading of direction but a panel-specific reading of magnitude. A different judge panel would produce different aggregate numbers while preserving the direction of every claim, which is part of why §5.8 frames the paper as directional rather than precise.

---

### 6.3 Pipeline and specification stability

The serving-strategy gap (static full-stack attachment versus production-realistic dynamic activation) is in §5.6 and §7.4. What follows covers pipeline-internal constraints on how the paper's results should be read.

**Pipeline version tested.** The specifications used in this study were produced by the current pipeline version, which we consider stable. The pipeline has evolved through development, and different pipeline versions produce different specifications on the same source corpus. The paper's results are specific to the pipeline version tested, and the study does not measure how the gradient shifts under earlier or later pipeline versions. The evaluation harness used here can serve as a benchmark for future pipeline iterations: each new authoring-pipeline version can be measured against the current specifications on the same 14-subject batteries to assess whether the gradient strengthens, weakens, or shifts shape (§7).

**Specification stability under the same pipeline version.** Running the same pipeline twice on the same corpus at temperature 0 does not produce identical specifications. In an initial stability check we ran the full pipeline twice on the same corpus at temperature 0 and compared the two output specifications. Roughly 45% of the resulting text was verbatim-identical between runs. The remaining 55% covered the same predicates and behavioral patterns with different surface phrasing; that 55% was assessed by side-by-side reading rather than against a numeric similarity threshold. This is an artifact of LLM sampling and of the multi-step authoring pipeline: small divergences at the extraction or authoring steps propagate through downstream composition. The per-subject variance probe below replaces this qualitative check with a quantitative one against the rubric.

**Per-subject pipeline variance, characterized.** A targeted replication probe was run on three subjects spanning the gradient (Sunity Devee, C5 = 1.03; Yung Wing, C5 = 1.88; Augustine, C5 = 2.58). For each subject, the Sonnet layer-authoring step and the Opus compose step were re-run three times against the same per-subject extracted fact set at temperature 0, producing three independent specifications. Each rerun was scored on the full behavioral-prediction battery in the C2a (spec only) and C4a (facts plus spec) conditions on the 5-judge primary panel. The resulting per-subject standard deviation of Δ_C4a across reruns is reported below, alongside the cross-subject SD that the §4.1 gradient slope is fit to. For each subject the table reports three numbers: the spec's effect on representational accuracy in the §4.1 main study (one authored specification), the standard deviation of that effect across three independent pipeline reruns on the same corpus, and that standard deviation as a fraction of the between-subject standard deviation the §4.1 gradient slope is regressed against.

| Subject | Canonical Δ_C4a (§4.1) | Per-rerun Δ_C4a SD (n=3) | % of cross-subject SD |
|---|---:|---:|---:|
| Sunity Devee | +1.38 | 0.103 | 17.4% |
| Yung Wing | +0.52 | 0.055 | 9.3% |
| Augustine | +0.11 | 0.130 | 22.0% |
| **Pooled (3 subjects)** | n/a | **0.101** | **17.1%** |

**Read of the precision question.** The directional finding survives across reruns: low-baseline subjects keep improving (6 of 6 reruns positive across the 2 low-baseline probe subjects), and the gradient slope point estimate is not materially threatened. Quantitatively, the pooled per-subject run-to-run SD of Δ_C4a is 0.10 on the 1-5 rubric, against a cross-subject SD of 0.59 that the gradient slope is regressed against; run-to-run pipeline variance is therefore on the order of 17% of the signal the slope is fit to, and well under the 95% CI half-width on the slope (0.29). What pipeline variance does affect is the precision attached to any single per-subject point estimate. The per-subject Δ_C4a numbers in §4.1 should be read with a soft uncertainty bar of roughly ±0.10 around them. Augustine (mid-baseline, canonical Δ = +0.11) sits at the top of its rerun range and the sign flips on 2 of 3 reruns, so individual mid-baseline subjects' spec-effect sign is itself within the run-to-run uncertainty band.

**Scope and caveats of the variance probe.** The probe covers the lighter-scope variance only: the Sonnet authoring step plus the Opus compose step. Extraction-stage non-determinism is held constant by reusing each subject's pre-populated SQLite and ChromaDB state across reruns; including extraction would likely add additional variance at the front of the pipeline. The probe covers low-baseline and mid-baseline subjects but does not reach the Franklin-style high-baseline tail (C5 = 3.77), so the H2 corollary (that the spec can interfere with strong pretraining signal at the high-baseline end, producing a near-zero or negative Δ) is not directly stress-tested by this run. With n = 3 reruns per subject the per-subject SD point estimates carry their own wide 95% confidence intervals (roughly [0.5×, 6×] of the value); the pooled three-subject estimate is more stable than any single per-subject estimate but should still be read as an order-of-magnitude indicator rather than a precision number. With those caveats stated, the run-to-run SD is small enough relative to the cross-subject SD that we accept the §4.1 slope and R² as findings about the gradient rather than artifacts of a single specification authoring.[^variance-data-paths]

[^variance-data-paths]: Per-rerun specs and judgments are at `data/global_<subject>/_variance_runs/run_<N>/` and `results/global_<subject>/_variance_runs/run_<N>_*.json`. Full report and reproducibility scripts at `docs/research/v10_pipeline_variance_analysis.md`, `scripts/_v10_pipeline_variance.py`, and `scripts/_v10_pipeline_variance_report.py`.

**Pipeline model choices were not varied systematically.** The pipeline uses Claude Haiku for extraction, all-MiniLM-L6-v2 for embeddings, Claude Sonnet for layer authoring, and Claude Opus for the compose step (§3.7). These model choices were not varied across the study. Different models at any step could produce different specifications: a different extraction model could surface different facts, a different embedding model could change retrieval behavior, a different authoring model could produce differently-structured anchors and predictions, a different composition model could synthesize the layers differently. Extending model support for each pipeline step, and measuring the gradient under alternate pipeline configurations (for example GPT-5.4 extraction, OpenAI embeddings, a non-Anthropic authoring model), is a direct follow-up flagged in §7.3, alongside the broader question of cross-model consistency for both spec authoring and usage.

---

### 6.4 Scope of exploration

Not every experimental combination was run. As an independent research project, the study prioritized coverage of the conditions and subjects central to H1 through H5 (§4.1 through §4.4) over running every cell of the design grid. Robustness and ablation conditions were added selectively rather than exhaustively.

**Coverage across the experimental grid.** The study spans 11 conditions (C1 through C9 plus two wrong-spec variants), 14 main-study subjects, and a 5-judge primary panel plus 2-judge sensitivity check; response-model coverage is detailed in §6.2 and §4.6.1. Running every possible combination (roughly 6,500 separate cells) was not attempted. Ablation-adjacent conditions (per-layer spec serving, alternate pipeline model choices, dynamic activation policies) were not run and are planned for future work (§7).

**Letta stateful-agent exploration.** Letta's stateful-agent architecture is distinct from the archival retrieval path the other three commercial systems use (§4.4, §4.5). Testing the stateful path required a different evaluation harness (§4.5 test design), and that work pulled us partially outside the main-study scope. The resulting comparison covers three subjects (Hamerton, Ebers, Babur), one Letta version, and one response model (Claude Haiku). Extending the stateful-agent comparison across the full 14-subject gradient, across additional response models, and against future Letta releases is flagged as a follow-up in §7.

**Twin-2K is prior work, not a condition of this study.** Twin-2K (§2.1) appears in this paper as prior work that measures a related but distinct property (survey-response prediction rather than representational accuracy). We did not run it as a condition of the main behavioral-prediction battery and do not report it as a benchmark result.

---

## 7. Future Work

Every section of this paper flags at least one follow-up. This section consolidates them into a research agenda organized by theme.

### 7.1 Measurement methodology

The most impactful measurement follow-up is replacing the content-match rubric with a differentiated battery that separates interpretation-heavy from literal-recall questions and scores epistemic honesty as its own dimension (§3.6.6). Alongside this: a curated question set with explicit quality control on the backward-design process, a human-validated subset of rubric applications to test whether the rubric was reasonably applied per-response (§3.6.6), and human-judge validation on a stratified subset of responses to address class-level LLM-as-judge circularity (§4.6.3, §6.2). Prompt-sensitivity testing across the authoring, response-generation, and judging stages (§6.2) is a separate measurement-stability follow-up that becomes important once the rubric itself is stabilized.

**Retrieval-overlap follow-ups (from the surfaced §4.4.1 finding).** Two measurement studies remain open after the §4.4.1 sensitivity check that already covers K=5 and semantic-similarity matching for K=10 in both controlled and native configurations:

- **Convergence-at-larger-K analysis.** This study tested K=10 retrieved facts per question (mean Jaccard 0.083 across systems, §4.4.1) and a K=5 sensitivity check that lowered overlap rather than raising it. The follow-up is K=25, K=50, K=100, and higher across the same systems and question set, to map the convergence curve and identify the K threshold at which providers begin to agree on which facts are relevant (if anywhere).

- **Meta-analysis of recall benchmarks against retrieval overlap.** Memory systems that score within a few percentage points on LongMemEval, LOCOMO, and similar recall benchmarks retrieve nearly disjoint top-K facts when given identical fact pools and fixed questions (§4.4.1). Recall benchmarks measure recall, which is what they should measure; the question is what additional dimensions matter for downstream representational accuracy. A meta-analysis comparing benchmark scores to retrieval-overlap on the same systems would clarify what "memory recall" actually predicts about how each system ranks facts for a specific interpretive task. The wrong-spec per-question meta-analysis (§4.6.4) belongs to the same class of follow-up: a deeper read of which parts of the served context the model referenced under correct versus mismatched specifications.

### 7.2 Subject and corpus expansion

A multi-subject living-user replication is the leading follow-up for the entire paper (§5.2, §5.7). The paper's findings are based on 14 historical subjects; whether they generalize to living users is not directly tested by this study, and replicating the gradient with multiple living subjects (with proper consent and privacy infrastructure) would close that gap. Three related expansions: modern-era corpora (to test whether the gradient holds when specifications are authored from contemporary writing rather than pre-20th-century autobiography, §6.1), non-English original sources (to remove translation artifacts, §6.1), and alternative testbeds that isolate reasoning structure without requiring private data, such as U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted (§5.3).

### 7.3 Specification design and composition

Component ablation on the authored layers (anchors, core, predictions, brief) is the priority authoring-pipeline follow-up (§5.4). Serving each layer alone and in combinations, measuring Pattern 1 / Pattern 2 / Pattern 3 distributions per configuration, would identify which parts of the pipeline are doing which work. Answers inform both the authoring pipeline's investment priorities and the dynamic-activation policy's weights.

Alongside component ablation: alternate pipeline model choices (extraction, embedding, layer authoring, composition) to measure sensitivity to specific LLM choices at each pipeline step (§6.3); a Base Layer referent-variant that retains named entities inside the same dimensional scaffold, to isolate whether the §4.5 Letta-over-Base-Layer gap is driven by referential vocabulary or by the self-editing process itself (§4.5); and a layered-stack Letta rerun on the matched-rerun subjects, which would likely narrow the §4.5 gap (§4.5).

**Cross-model consistency for spec authoring and usage.** Two related questions sit on top of the alternate-pipeline-model-choice follow-up. First, on the authoring side: whether different LLMs at each pipeline step produce specifications that converge on the same behavioral patterns from the same source corpus, or whether the specification itself drifts with the choice of authoring model. Second, on the usage side: whether different response models interpret the same specification consistently, applying it to produce comparable predictions on the same held-out questions. The §4.6.1 Tier 2 probe established that the gradient direction holds across three response models on three subjects; whether the spec is read and applied the same way across the broader model landscape is the deeper consistency question.

**Source-text texture as a complement to predicate structure.** Letta's memory blocks retain verbatim sentences from the source corpus (§4.5; Appendix G). One open question is whether that verbatim retention contributes to alignment with the subject's voice (vocabulary, syntax, register) beyond what the predicate-level abstractions in the Base Layer pipeline capture. The Base Layer pipeline by design abstracts source text into structured predicates for explainability and traceability; verbatim retention of stylistic features is not a primary goal. A natural follow-up is a hybrid representation that pairs each predicate with one or more source sentences supporting it: predicates for structure and explainability, source statements for stylistic alignment. The two layers would be indexed to each other so that the response model can ground in either or both depending on the question type.

### 7.4 Production serving and infrastructure

The study served the Behavioral Specification statically and in full on every query. Four production-realistic serving-layer follow-ups would refine deployment beyond this static-attachment baseline: dynamic activation (selecting which parts of the spec to attach per query), user editing and inspection (how a user can update or correct their own spec post-authoring), temporality handling (how the spec ages and what triggers re-authoring; §7.5), and topic decomposition (whether the spec can be partitioned by domain for selective serving). Each is a measurement question in its own right: whether the gradient, mechanism, and composition findings hold under each production serving strategy.

### 7.5 Stateful-agent implementations and temporal drift tracking

Several follow-ups sit adjacent to the paper's static-snapshot design.

**Stateful-agent variant of the Behavioral Specification.** The pipeline as tested is offline and batch. A persistent, self-editing variant that ingests new source material as it arrives, re-edits anchors and predictions in place, and maintains version history with provenance across edits is a natural next step. The §4.5 Letta exploration (N=3, post-hoc) is one data point on an adjacent architecture; building and evaluating a stateful-agent Base Layer implementation on the full 14-subject main-study battery would close the comparison within a single architectural family and extend §4.5 to a layered-stack rerun against Letta at full scope.

**Cleaner §4.5 rerun with naming and scaling controls.** Two specific extensions of the §4.5 exploration are worth running as a unit. First, anonymize the source corpus before Letta ingestion so Letta writes an anonymized memory block, matching Base Layer's anonymized-during-authoring convention; the §4.5 naming asymmetry (Letta ingests named corpus, Base Layer strips and later restores names) is removed as a confounder. Second, extend the corpus-size axis past the Babur ceiling to a larger (>250K-word) subject corpus that pushes the Letta block past its character ceiling. The matched-model gap was small at Hamerton (25K-word corpus), largest at Ebers (48K-word corpus), and smaller again at Babur (223K-word corpus); whether that pattern continues, re-widens, or flattens at extreme corpus size is the empirical question. Both extensions together would turn §4.5's case study into a controlled comparison.

**Temporal drift tracking.** The static snapshot tested here is a point on a trajectory. A specification authored at one time, compared against a later specification on an expanded corpus, produces a measurable diff: which anchors appear or disappear, which predictive templates shift, which axioms strengthen or weaken. From a sequence of past specifications, the trajectory predicts the next. The 14-subject corpora collected for this study can be back-sliced by chapter boundaries or publication era for an initial drift test within the current sample. A purpose-built companion study on sequential public records (US Supreme Court opinions, shareholder letters, research papers) is the natural extension.

**Canonical life events.** Discrete pivots that flip reasoning architecture (a major career change, a religious conversion, a significant loss, a public stance reversal) are distinct from gradual drift. The main-study autobiographies were not structured to test this case. A snapshot specification authored before such an event predicts pre-event reasoning, not post-event reasoning, even though the person's underlying patterns have materially shifted. Whether to detect these events automatically, allow user annotation, or maintain period-specific specifications is an open production-deployment question.

**Continuous-representation infrastructure.** Both of the above converge on the same engineering target: a background process that watches incoming corpus material, re-authors the specification as new material arrives, and emits drift telemetry as a first-class output (what changed in the spec, by how much, and against what baseline). The Letta-style stateful agent (§4.5) and the sequential-checkpoint test design are complementary tests for this kind of implementation: the first isolates online self-editing as a way to produce the representation, the second isolates temporality as a property of the representation itself. As a downstream effect, the daemon's continuous output (the sequence of spec versions, diffs, and drift telemetry) itself becomes a training corpus for next-generation pipeline development.

Additional architectural paths worth testing against the same target, beyond stateful-agent and drift-tracking variants, include agent-edited persistent memories outside the MemGPT family, fine-tuned per-user models that expose their internal representation for audit, and hybrid architectures that combine offline-extracted specifications with online self-editing.

**Per-user feedback as a learning signal for the specification.** Every interaction with an AI agent can produce a small correction signal: the user edits a response, says "actually I would have done X", or rejects an answer outright. Each of these is a hint that the current specification mispredicted the user's behavior. Used as a feedback signal, these corrections can update the specification directly: the affected predicate or anchor is re-extracted and re-authored, then re-composed into the spec. Because the update unit is structured text rather than model weights, the change is interpretable and the per-update cost stays at the §3.7 pipeline cost. Two design questions matter. First, drift risk: corrections without a source-text anchor can pull the spec in arbitrary directions, so the corpus stays the source of truth and corrections are bounded by it. Second, signal quality: explicit corrections are sparse but high-fidelity, while everyday divergence is abundant but noisy; treating both as the same kind of feedback is wrong. A first-pass design using explicit corrections only, batched daily, with versioned diffs logged for rollback, is the cheapest test of whether correction-driven updates produce measurable accuracy gains beyond the static snapshot.

### 7.6 Safety-alignment integration

The positioning argument (per-user calibration as redirection of existing shaping rather than additional bias, and as orthogonal to safety alignment) is in §5.7. Two concrete follow-ups extend that positioning. First, the spec-induced refusal cases (§4.3, §4.6.3): a post-hoc classifier audit of 81 spec-induced refusals across 5 memory systems (`docs/research/refusal_intent_classification.md`) found 75 of 81 (93%) were routine behavioral prediction rather than morally loaded. The refusal pattern is general caution when information is thin, not a moral-integrity mechanism. Whether it composes cleanly with existing safety frameworks across benign and malicious user types is open. Second, the specifications in this paper were authored from public-domain autobiographies of subjects not selected on intent. What a specification for a user with malicious intent would contain, and what happens when an agent is deployed on that user's behalf, is untested. Both belong to collaboration with AI safety researchers rather than single-lab follow-ups.

A narrower follow-up: the wrong-spec adversarial control (§4.3) showed response models can recognize spec content as belonging to a different historical period or persona. Whether models can recognize specifications encoding adversarial values (personas that endorse harmful behaviors) and flag them rather than comply is a direct extension that bears on live-user deployment.

---

*Paper body complete. Abstract to be written last.*

---

## 8. Data, code, and reproducibility

**Data availability.** All raw response files, per-judge judgments, batteries, and aggregated results for the 14 main-study subjects are in the public study repository at `github.com/agulaya24/memory-study-repo` under `results/global_<subject>/` and `results/hamerton/`. Source autobiographies are public domain (Project Gutenberg and Internet Archive). Per-subject Project Gutenberg IDs are listed in §3.2 Table 3.2. Memory-system raw retrieval and ingestion logs are at `results/global_<subject>/<system>_*.json`. The Letta stateful-agent matched-rerun artifacts are at `docs/research/_letta_rerun/`. The full-stack Letta rerun comparison is at `docs/research/_letta_rerun/fullstack_named/`.

**Code availability.** The Base Layer pipeline source (extract, embed, author, compose) is at `github.com/agulaya24/BaseLayer`. The study-specific analysis and re-run scripts are at `github.com/agulaya24/memory-study-repo` under `scripts/`. Reproducibility pointers from each numerical claim to its supporting script are in `docs/PROVENANCE_INDEX.md` and `docs/DATA_REFERENCE.md`. The §4.1 battery-composition sensitivity analysis is reproducible via `scripts/_v10_battery_sensitivity.py`. The §3.6.6 rubric-handling validity audit is reproducible via `scripts/audit_low_end_inflation.py`. The §4.3 hedging classifier is at `scripts/classify_hedging.py`.

**Agent-friendly study repo tooling.** The study repository is structured for both human reading and agent consumption. A combined SQLite + ChromaDB knowledge index (`workspace/study_knowledge.db`, `workspace/study_vectors/`; built by `scripts/index_study_repo.py`) covers 206 files and 3,702 chunks across the paper, supporting docs, per-subject specs, judgments, retrieval logs, and analysis scripts. An MCP server exposing this index plus typed lookups (per-subject score retrieval, claim provenance, condition-pair anchor-crossing queries) is available as an MVP at `memory-study-repo/mcp/`; the decision to optimize the repo for agent consumption is based on the observation that the same artifacts that make a paper easy to verify mechanically (stable anchors, structured judgments, machine-readable schemas) also make the paper easier for human readers to skim and verify.

**Compute and cost.** All response generation and judging used commercial APIs (Anthropic, OpenAI, Google) at standard rates. No specialized hardware was used. All experiments are runnable on a standard developer laptop.

**Author affiliation.** Aarik Gulaya, Base Layer. Contact: `aarik@base-layer.ai`. Project page: `base-layer.ai`.

**Funding.** This work was self-funded.

**Conflicts of interest.** The author is the founder of Base Layer, the project that develops the Behavioral Specification pipeline this paper evaluates. Memory-system providers tested in this paper (Mem0, Letta, Supermemory, Zep) were used through their public APIs at standard rates; no provider was given preferential framing, and Base Layer does not have commercial relationships with any of them. Self-reported benchmark scores from each provider are reported as published; this paper does not adjudicate disputes between providers' published claims (§2.2).

**License.** Apache 2.0 for code and Creative Commons Attribution 4.0 for the manuscript and data analyses produced by this study. Source autobiographies are in the public domain.

**Acknowledgments.** Conversations with the broader memory-systems and AI-personalization research communities informed the design of this paper. Specific gratitude goes to the cross-LLM reviewer panels (Gemini 2.5 Pro, Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, GPT-5.5) whose iterated reviews materially improved earlier drafts. All errors are the author's.

---

## 9. References

*Citation conventions: All authors are listed when 3 or fewer; otherwise the first author plus "et al." Where a peer-reviewed venue is listed, the citation year is the venue year and the arXiv identifier is included as a durable preprint identifier that may predate the venue year.*

Bartlett, F. C. (1932). *Remembering: A Study in Experimental and Social Psychology*. Cambridge University Press.

Chen, R., et al. (2025). Persona vectors: Monitoring and controlling character traits in language models. *arXiv preprint arXiv:2507.21509*.

Chhikara, P., et al. (2025). Mem0: Building production-ready AI agents with scalable long-term memory. *arXiv preprint arXiv:2504.19413*.

Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network. *NIPS Deep Learning and Representation Learning Workshop*. arXiv:1503.02531.

Jain, S., et al. (2025). Interaction context often increases sycophancy in LLMs. *arXiv preprint arXiv:2509.12517*.

Jiang, B., et al. (2025). Know me, respond to me: Benchmarking LLMs for dynamic user profiling and personalized responses at scale. *Conference on Language Modeling (COLM) 2025*. arXiv:2504.14225.

Lu, C., et al. (2026). The Assistant Axis: Situating and stabilizing the default persona of language models. *arXiv preprint arXiv:2601.10387*.

Maharana, A., et al. (2024). Evaluating very long-term conversational memory of LLM agents. *Annual Meeting of the Association for Computational Linguistics (ACL) 2024*. arXiv:2402.17753.

Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. *arXiv preprint arXiv:2310.08560*.

Perez, E., et al. (2022). Discovering language model behaviors with model-written evaluations. *arXiv preprint arXiv:2212.09251*.

Rasmussen, P., et al. (2025). Zep: A temporal knowledge graph architecture for agent memory. *arXiv preprint arXiv:2501.13956*.

Samuel, V., et al. (2025). PersonaGym: Evaluating persona agents and LLMs. *Findings of the Association for Computational Linguistics: EMNLP 2025*. arXiv:2407.18416.

Sharma, M., et al. (2023). Towards understanding sycophancy in language models. *arXiv preprint arXiv:2310.13548*.

Toubia, O., et al. (2025). Twin-2K-500: A dataset for building digital twins of over 2,000 people based on their answers to over 500 questions. *arXiv preprint arXiv:2505.17479*.

Verga, P., et al. (2024). Replacing judges with juries: Evaluating LLM generations with a panel of diverse models. *arXiv preprint arXiv:2404.18796*.

Wu, D., et al. (2025). LongMemEval: Benchmarking chat assistants on long-term interactive memory. *International Conference on Learning Representations (ICLR) 2025*. arXiv:2410.10813.

Xiao, J., et al. (2026). AlpsBench: An LLM personalization benchmark for real-dialogue memorization and preference alignment. *arXiv preprint arXiv:2603.26680*.

Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems (NeurIPS) 2023, Datasets and Benchmarks Track*. arXiv:2306.05685.

---

**Appendices.** Reference material supporting the main text, designed to be read selectively. Appendix A covers the 46 behavioral predicates used in the extraction step. Appendix B covers per-subject battery composition and category-level effect sizes. Appendix C covers condition identifiers, response-model configurations, memory-system parameters, and judge panel settings. Appendix D covers per-subject score distributions, the rubric-handling audit, length-correlation tables, and anchor-crossing numbers. Appendix E provides three illustrative paired (C5, C4a) per-question response excerpts for each of the 14 main-study subjects. Appendix F covers the extended benchmark-scope comparison against LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo, and adjacent benchmarks. Appendix G holds the full Letta stateful-agent exploratory case study summarized in §4.5. Appendix H is the glossary.

---

## Appendix A. Predicate Vocabulary

### A.1 The 46 Constrained Predicates

The extraction step (Step 2 of the pipeline, §3.7) instructs the extraction model to emit triples of the form `(subject, predicate, object)` using only the 46 predicates listed below. Predicates outside this list are either normalized by `normalize_predicate()` into the canonical form or routed to the `unknown` catch-all (which is filterable downstream, not silently dropped). The vocabulary is frozen for the study; it was curated and validated across roughly 50 pilot subjects before being locked. The canonical source is `memory_system/src/baselayer/config.py` lines 613-639 (`CONSTRAINED_PREDICATES`).

The predicates group into seven behavioral dimensions. The groupings below are analytical; the predicate list itself is flat in code.

**Behavioral patterns (activities and engagement).** These are the most load-bearing predicates for interpretive representation. They describe what the subject repeatedly does or refuses to do, which is what anchors the authored layers in §3.7.

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

**Values, beliefs, and self-view.** These populate the core layer (§3.7) and describe the stable commitments a subject carries across situations.

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

### A.2 Provenance and design choices

The vocabulary was iterated in three stages. The initial 30-predicate list (sessions 1-48) favored values, activities, and biography. Session 49 added 6 predicates (`unknown`, `attended`, `interested_in`, `wants_to`, `loves`, `hates`) to preserve semantic distinctions that the initial vocabulary collapsed. Session 52 added `plays` and `monitors`. Session 55 added 8 relationship predicates to raise relationship-fact extraction from 0.8% to the 3 to 5% target range.

The vocabulary is deliberately behavioral rather than biographical. The ratio of predicates in the behavioral-patterns plus values-beliefs plus emotions-dispositions groups (23 of 46) to the biographical-context group (7 of 46) encodes a design decision: extraction is steered away from facts that are easily verifiable in external sources (city of birth, schools attended) and toward patterns that require reading the source text to infer (what the subject avoids, prefers, values, fears).

### A.3 Not in the vocabulary

Three predicate categories that commonly appear in general-purpose knowledge graphs are deliberately excluded:

- **Evaluative predicates about the subject from a third party** (for example, `considered_brilliant_by`). These invert the direction of claim: the subject is the object rather than the source of the reasoning.
- **Time-indexed state changes** (for example, `became`). The vocabulary handles change-over-time through the AUDN ADD / UPDATE / DELETE / NOOP operations at the fact level, not through predicate selection.
- **Causal predicates** (for example, `caused`, `triggered`). Causal inference is produced in the authored layers (predictions, anchors) from collections of facts, not encoded at the extraction step.

### A.4 Live deployment

A live web deployment of the pipeline described in §3.7, with served briefs across additional subjects beyond the 14 in this study, is available at base-layer.ai for readers interested in seeing the served-specification format in interactive form.

---

## Appendix B. Question Batteries

### B.1 The 10 fixed behavioral-prediction categories

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

### B.2 Per-subject battery composition (10-category by 15-subject matrix)

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

### B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING)

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

### B.4 Category-level effect size on Δ_spec

Mean Δ_spec (C2a minus C5) broken down by the behavioral-axis classification. Source: `docs/research/question_category_audit.md`.

| Axis | n | Mean Δ_spec | Median Δ_spec |
|---|---:|---:|---:|
| LITERAL_RECALL | 60 | +0.792 | +0.800 |
| INTERPRETIVE_INFERENCE | 366 | +0.397 | +0.400 |
| REFUSAL_TRIGGERING | 120 | +0.417 | +0.200 |

The LITERAL_RECALL bucket is small (n = 60) per subject, so per-subject estimates are high-variance, but the aggregate is robust within that constraint. The unexpected finding (that LITERAL_RECALL Δ_spec exceeds INTERPRETIVE_INFERENCE Δ_spec) is discussed in the audit doc: a plausible mechanism is stylistic-register match between the spec's Victorian prose and Hamerton's held-out text, not genuine fact recall. The INTERPRETIVE_INFERENCE signal (n = 366, Δ = +0.397) is the cleanest between-condition evidence that the spec performs representational work rather than register-matching.

### B.5 Per-subject by axis Δ_spec

Full breakdown at `docs/research/question_category_audit.md` and per-subject axis-Δ scaffold values at `docs/research/v11_emit/appendix_b_battery.json` (claim ids `appB_5_<subject>_<axis>_delta`). Summary of the cross-subject pattern under 5-judge primary aggregation: the strongest positive spec effects cluster on three subjects. Hamerton (LITERAL +1.68, INTERP +1.30, REFUSAL +1.25), Sunity Devee (+1.38 / +1.16 / +1.35), and Bernal Diaz (+2.00 / +0.44 / +0.64) carry the largest gains. Augustine, Equiano, and Zitkala-Sa show negative or near-zero deltas across all three axes, consistent with their status as mid-baseline subjects on the §4.1 gradient. Fukuzawa and Seacole show their largest positive effects on INTERPRETIVE_INFERENCE specifically (+0.83 and +0.79). Bernal Diaz's +2.00 on LITERAL_RECALL is computed over a small per-axis n (single-digit questions per axis per subject), so the per-subject estimate is high-variance; the cross-subject correlation pattern in §B.6 is the more robust signal.

### B.6 Battery-composition sensitivity

This appendix provides the technical detail behind the §4.1 battery-sensitivity controls.

**B.6.1 Battery-question-type correlations.**

Across the 14 main-study subjects:

- Δ_spec range: −0.31 to +1.37
- Corr(fraction of LITERAL_RECALL questions, subject-level Δ_spec): r = +0.595 (recomputed under strict 5-judge primary; the legacy audit-doc value was +0.646, which used a Hamerton-divergent intermediate aggregation)
- Corr(fraction of INTERPRETIVE_INFERENCE questions, subject-level Δ_spec): r = −0.466 (legacy: −0.582, same caveat)
- Corr(fraction of REFUSAL_TRIGGERING questions, subject-level Δ_spec): r = +0.212

The positive LITERAL_RECALL correlation and negative INTERPRETIVE correlation imply that subjects whose batteries over-weight literal recall also produce larger measured Δ_spec values.

**B.6.2 Multiple regression controlling for LITERAL_RECALL fraction.**

A multiple regression of Δ_C4a on both C5 baseline and LITERAL_RECALL fraction across the 14 main-study subjects yields a partial coefficient on baseline of **−0.88 [95% CI −1.13, −0.63], p < 10⁻⁵**, attenuated from the univariate −0.96 by about 8%. LITERAL_RECALL fraction enters as a significant partial predictor (β = +2.30 [+0.34, +4.26], p = 0.026), but baseline carries the bulk of the explained variance: 63.6% uniquely attributable to C5, 6.9% uniquely attributable to LITERAL_RECALL fraction. The two predictors are not collinear (Pearson r = −0.28, VIF = 1.08 for both), so the partial coefficients are stable. Adjusted R² rises from 0.80 to 0.87 when LITERAL_RECALL fraction is added; the controls are additive rather than redundant. The gradient on baseline survives; it is not an artifact of battery composition.

**B.6.3 Hamerton-leverage subset regression.**

Hamerton's 80-question battery predates the global-subject pipeline and uses a slightly different backward-design path (the legacy Haiku 4.5 generator that originally produced Franklin and Hamerton); the 13 global subjects' main-study batteries also use Claude Haiku 4.5 but were regenerated by `run_global_rerun.py` against a uniform prompt template. All 14 main-study batteries share the same generator family. A subset regression dropping Hamerton (N=13 globals) yields a slope of **−0.89 [95% CI −1.18, −0.61], R² = 0.81, p < 10⁻⁴**, compared to the full-sample −0.96. The point estimate attenuates by about 7%, and the 95% CIs overlap substantially. The gradient is not Hamerton-driven. A separate GPT-5.4-regenerated battery set (`results/global_<subject>/battery_gpt54.json`) exists for each global as a circularity control; its results are reported in §3.3.1 and §4.6.1, not folded back into the §4.1 gradient itself.

**B.6.4 Discussion.**

This is a battery-composition confound in the cross-subject gradient; the paper's gradient claim is therefore specifically about mean score movement per subject, not about mean score movement per category. §5.3 and §7 flag a follow-up study with a category-balanced battery as the primary design improvement for future gradient work.

**B.6.5 Hamerton-leverage at the per-question grain.**

The B.6.3 subset regression checks the per-subject mean grain. A parallel question is whether the per-question extreme upward anchor crossings catalogued in `docs/research/wins_inventory_20260428.json` (60 unique cases across 18 condition pairs, 351 paired low-baseline questions on C5 to C4a) are concentrated on Hamerton specifically. They are: Hamerton accounts for 15 of the 60 unique extreme jumps (25%) on a battery of 80 questions (18.75% extreme-jump rate); the other 13 subjects average 8.9% extreme-jump rate across 39-question batteries. Hamerton's elevation is real but its cause is not isolated by the present design. Three candidate mechanisms (legacy battery-generator path, subject pretraining thinness, behavioral-predicate density per word) are not separately identifiable, since Hamerton's served spec is 1918 words (brief-only) versus globals' ~5775 words (anchors + core + predictions + brief), so spec length is anti-correlated with extreme-jump rate. As measured by the heuristic classifier, the mechanism distribution on Hamerton's 15 jumps versus globals' 45 is nearly identical (PATTERN_PREDICATE+HYBRID share: Hamerton 73.3% vs globals 80.0%); the heuristic does not discriminate jumps from non-jumping spec-loaded controls (`docs/research/pattern_activation_deep_20260428.md`), so this near-identity is consistent with the heuristic detecting spec-loaded response style rather than the lift mechanism.

### B.7 Coupling-free reframing of the gradient

The headline slope regresses Δ_C4a = C4a − C5 on C5, which mechanically embeds a −1 component when C4a is bounded on the 1-5 scale and partially independent of C5. To triangulate from a non-coupling-prone angle, we ran three additional checks on the same per-subject (C5, C4a) data (script: `scripts/_v10_coupling_sensitivity.py`; full output: `docs/research/v10_coupling_sensitivity_analysis.md`).

**B.7.1 Level regression.**

The level regression C4a ~ C5 produces a slope of **+0.04** [95% CI −0.24, +0.33], R² = 0.008, p = 0.76. C4a is essentially flat across the C5 range of 1.02-2.77 and clusters tightly around its mean of **2.46** at the per-subject grain. The spec does not differentially "lift" low-baseline subjects more than high-baseline ones in any treatment-effect-heterogeneity sense; it produces a roughly constant post-spec C4a mean per subject regardless of baseline, and the apparent Δ-on-C5 gradient equals the baseline shortfall.

**B.7.2 Permutation test.**

A 10,000-iteration permutation test that shuffles C4a across subjects (preserving the bounded marginal but breaking any link to C5) yields a null distribution for the Δ-on-C5 slope centered at −0.998 (SD 0.127). The observed −0.960 is not extreme against this null (two-sided p = 0.77). In plain language: even when C4a values are randomly reshuffled across subjects, the Δ-on-C5 slope still lands near −1 on average, because the change-score parameterization mechanically pushes the slope toward −1 whenever C4a is roughly independent of C5. The −0.96 the headline regression reports is what the regression arithmetic forces, not independent evidence that low-baseline subjects benefit more from the spec at the per-subject mean grain.

**B.7.3 Bootstrap.**

A 10,000-iteration subject-level bootstrap returns CIs of [−1.254, −0.740] for the Δ-on-C5 slope and [−0.254, +0.260] for the level slope. The level CI straddles zero, consistent with the level-regression finding that the per-subject C4a mean is roughly constant across baselines.

**B.7.4 Reading the gradient against this.**

The substantive finding survives the coupling check, but its framing has to shift away from "the spec acts more strongly on low-baseline subjects" toward the per-question reframing in §4.1: low-baseline subjects have a larger pool of questions at low rubric anchors, so the spec has more opportunity to produce upward integer-band crossings, which aggregates as a larger per-subject mean lift. The directional asymmetry on those crossings (no observed transitions from bands 2, 3, or 4 into band 5 across the full 14-subject panel; the only band-5 endpoints reached come from band 1) is consistent with the §4.2 finding that even the full source corpus C8 plateaus at a similar per-subject mean.

### B.8 Per-predicate ablation (Phase 2c)

To probe whether single behavioral predicates within the spec are uniquely load-bearing, we ran a per-sentence ablation experiment on a stratified sample of 16 extreme-upward-jump cases. For each case, the heuristically-identified causal predicate (highest-token-overlap spec sentence vs the question and held-out passage) was located in the served spec and three response variants were generated at temperature 0 with Claude Haiku 4.5: (1) original (full spec), (2) ablated (predicate removed, replaced with a length-matched neutral biographical filler), (3) reversed (predicate replaced with a behavioral opposite synthesized by Sonnet). Each variant was scored by the 5-judge primary panel.

Results (script: `scripts/run_predicate_ablation.py`; data: `docs/research/predicate_ablation_results_20260428.json`):

- Mean Δ_removal (original minus ablated) across 16 cases: +0.05 anchor points (95% CI [−0.35, +0.45])
- Mean Δ_reversal (original minus reversed): −0.24 anchor points (95% CI [−0.45, −0.02])
- 2 of 16 cases showed Δ_removal ≥1 anchor; 11 of 16 had Δ_removal < 0.5

Single-predicate removal does not measurably reduce response quality on this sample. The paper does not interpret this as evidence that the spec is mechanistically inert: the higher-level mechanism evidence from the wrong-spec adversarial control (Appendix C / §4.3) shows the spec as a whole is doing causal work. The null result on per-sentence ablation is consistent with redundant spec construction, in which multiple sentences across the anchors / core / predictions / brief layers reinforce the same behavioral patterns; removal of any single sentence leaves the pattern accessible elsewhere in the spec.

A methodological caveat applies. Original-condition reproduction at temperature 0 was not bit-exact deterministic across reruns; mean drift between the recorded original score (from `docs/research/wins_inventory_20260428.json`) and the rerun original score was −1.44 anchors, with 9 of 16 cases drifting by more than 1 anchor. Some of the variance in Δ_removal is rerun stochasticity rather than ablation effect. The extreme-upward-jump cases specifically show higher pipeline variance than the per-subject mean grain documented in §6.3.

Future work tightening (per the test's own report): human-rated predicate identification (vs heuristic), larger N (all 47 PATTERN_PREDICATE cases), irrelevant-predicate control (matched-length unrelated predicate to test the "any rich persona text" alternative), multi-predicate cluster ablation.

### B.9 Footnote-redirect technical detail

This subsection holds the longer technical content for footnotes that would otherwise grow to multi-paragraph length. Each entry is keyed to the footnote name in the body.

**B.9.1 `[^delta-aggregation]`. +0.89 vs +0.93 reconciliation.**

The +0.89 figure is the canonical cross-subject mean of per-subject Δ_C4a. Each subject's Δ is computed as that subject's per-question 5-judge primary mean under C4a minus their per-question mean under C5; these per-subject Δs are then averaged across the 9 low-baseline subjects. The grand-mean alternative grand-averages all per-question scores under each condition first and then takes the difference, yielding +0.93 (the difference of the C4a grand mean 2.45 and the C5 grand mean 1.52). The two numbers are not in conflict; they answer slightly different questions. The per-subject-mean grain (+0.89) is the unit of inference used throughout this paper because every statistic is computed at the subject level first, then aggregated across the 14 subjects (§1.2 aggregation rule).

**B.9.2 `[^heldout-leakage-audit]`. Held-out leakage audit detail.**

A held-out leakage audit on the 60 unique extreme-upward-jump cases (full report at `docs/research/held_out_leakage_investigation_20260428.md`) found 0 6-gram, 2 4-gram, and 12 3-gram matches between held-out passages and C4a responses. Of the 9 cases with any leak, 6 are short generic phrases also resident in the served facts list (CORPUS_LEAK), 2 are subject-specific n-grams not in any served context (best explained by pretraining recall of public-domain autobiographies; PRETRAINING_MEMO_CANDIDATE), and 1 is generic English (COMMON_PHRASE). The longest shared run anywhere is 4 tokens, well below transcription length. Severity verdict: rare; no structural validity concern; footnote acknowledgement is the appropriate paper-text treatment. Excluding the 2 pretraining-memorization candidates from the extreme-upward-jump set shifts the C5 to C4a low-baseline extreme-jump count by at most 1 (20 to 19); per-subject mean Δs are unchanged at the per-question level. The "held-out passage" was held out from served spec / facts, not from pretraining, and the audit confirms that interpretation: where C4a held-out-to-post leakage exists, it is either short generic phrasing also resident in the served facts (trivially short) or subject-specific content in the model's pretraining, not study-design contamination of the served context.

**B.9.3 `[^supermemory-no-retrieval]`. Supermemory NO_RETRIEVAL placeholders.**

Across the full 14-subject Supermemory analysis, 30 individual responses (Augustine 2 questions, Equiano 28 questions) were Supermemory provider-failure placeholders rather than substantive predictions, scored at the rubric floor (1) by the judge panel. We treat these as scored data rather than missing data, consistent with how the rest of the study handles low-quality responses. Excluding the 30 NO_RETRIEVAL records as missing data would shift Supermemory's aggregate Δ slightly higher; the qualitative story (small aggregate at both grains, bimodal per-question distribution) holds either way.

### B.10 Pre-registered hypotheses and post-hoc analyses

The paper distinguishes pre-registered hypotheses (H1–H5, locked against the statistical commitments in `docs/ANALYSIS_PLAN_LOCK.md`) from analyses that emerged during the work. The following table catalogues every load-bearing analysis result reported in §4 and identifies its status. Post-hoc items are reported as exploratory rather than at the same evidentiary tier as the pre-registered hypotheses.

| Item | Status | Where reported | Note |
|---|---|---|---|
| **H1** Spec-context outperforms no-context | Pre-registered | §4.1, §1.3 1st bullet | Headline gradient |
| **H2** Spec benefit inversely proportional to pretraining coverage | Pre-registered | §4.1, §4.1.2, §1.3 1st bullet | Gradient at both ends; Franklin reference |
| **H3** Content-specificity (correct vs. wrong spec) | Pre-registered | §4.3, §1.3 4th bullet | Wrong-spec controls v1 + v2 |
| **H4** Spec interacts with retrieval through three patterns | Pre-registered | §4.4, §4.4.2, §1.3 5th bullet | Memory-system composition |
| **H5** Compression: ~7K-token spec recovers most of corpus signal | Pre-registered | §4.2, §1.3 3rd bullet | At 5x to 80x smaller context |
| Cross-system retrieval-overlap divergence | Post-hoc | §4.4.1; sensitivity in §4.6.5; §1.3 7th bullet | Surfaced during memory-system analysis; mean Jaccard 0.083 across 10 system pairs; survives semantic-similarity matching |
| Letta stateful-agent case study | Post-hoc | §4.5; full in Appendix G | N=3, exploratory |
| Letta semantic-duplication scaling | Post-hoc | §4.5; Appendix G | Surfaced in this paper's analysis; cosine ≥ 0.85 = 56.1% on Babur |
| Abstention-credit validity audit | Post-hoc | §3.6.6 | 9.4% of refusals score ≥ 2.0; bias direction makes the spec effect likely larger than reported |
| Per-subject wrong-spec heterogeneity | Post-hoc | §4.6.4 | 5/13 subjects show small positive v1 deltas (coincidental content overlap) |
| Hedging-elimination (28.8% → 0.0%) | Post-hoc | §4.3, §1.3 6th bullet | Surfaced from response-level audit |
| Battery-question-type sensitivity (literal-recall fraction) | Post-hoc reactive | §4.6.3, Appendix B.6 | Added in response to v9/v10 reviewer concerns |
| Hamerton leverage check (subset regression) | Post-hoc reactive | §4.6.3, Appendix B.6 | Added in response to v9/v10 reviewer concerns |
| Coupling-free reframing of the gradient | Post-hoc reactive | §4.1.1 leveler callout, Appendix B.7 | Added in response to GPT-5.5 review |
| Cross-provider response generation (Tier 2) | Pre-registered control | §3.5, §3.3.1, §4.6.1 | Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects |
| GPT-5.4 battery regeneration (Control 1) | Pre-registered control | §3.3.1, §4.6.1 | Battery generator circularity |
| Judge-panel composition (5-judge primary, 7-judge sensitivity) | Pre-registered control | §3.6.3, §4.6.2 | Locked panel before scoring |
| Wrong-spec derangement protocol sensitivity (v1 vs v2) | Reactive | §4.6.4 | v2 is the standard randomization control; v1 is the adversarial stress test (headlined for stronger evidence) |

Reproducibility scripts and raw data for each row are pointed to throughout §4 and consolidated in §8 Data, Code, and Reproducibility.

---

## Appendix C. Conditions, Models, and Memory-System Configurations

### C.1 Condition identifiers (summary card)

A consolidated lookup for the condition IDs used throughout §4. Defined in §3.4; summarized here.

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

### C.2 Shared response-model invocation

Every response call, across every direct-context and memory-system condition, uses the following parameters:

| Parameter | Value |
|---|---|
| `temperature` | 0 |
| `max_tokens` | 1024 |
| System prompt | Framing instruction: predict how `<subject>` would respond; answer in subject's voice, grounded in demonstrated patterns. |
| User prompt format | `<context block>\n\nQuestion: <question text>` |
| Context block | Condition-dependent. Empty in C5. Spec in C2a. Wrong spec in C2c. Facts in C4. Facts plus spec in C4a. Corpus in C8. Corpus plus spec in C9. Retrieval output (optionally plus spec) in C1 and C3. |

No prompt instruction coaches the model to abstain, hedge, or commit. The model's refusal-or-commitment pattern given a specific context is part of the phenomenon being measured (§3.5, §4.3).

### C.3 Response models

| Role | Model identifier | Provider | Scope |
|---|---|---|---|
| Primary response | `claude-haiku-4-5-20251001` | Anthropic | All 14 subjects, every condition. Main study. |
| Tier 2 response | `claude-sonnet-4-6` | Anthropic | 3 subjects (Ebers, Yung Wing, Zitkala-Sa), C5 / C2a / C2c / C4a against GPT-5.4 batteries. |
| Tier 2 response | `gemini-2.5-pro` | Google | Same 3 subjects, same conditions as Sonnet Tier 2. |

Source: `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, `scripts/run_multimodel_responses.py`.

### C.4 Pipeline models (specification generation)

| Pipeline step | Model identifier | Temperature | Purpose |
|---|---|---|---|
| Extract (Step 2) | `claude-haiku-4-5-20251001` | 0 | AUDN fact extraction, 46-predicate constrained vocabulary. |
| Embed (Step 3) | `all-MiniLM-L6-v2` (local) | n/a | ChromaDB vector index (L2 distance). |
| Author (Step 4) | `claude-sonnet-4-6` | 0 | Three authored layers (anchors, core, predictions). Blind regen, domain guard. |
| Compose (Step 5) | `claude-opus-4-6` | 0 | Unified brief composition. |
| Battery generation | `claude-haiku-4-5-20251001` | 0 | Backward-design from held-out corpus. |
| Battery generation (circularity control) | `gpt-5.4` (via OpenAI API) | 0 | Independent regeneration on 13 global subjects. |

Source: `memory_system/src/baselayer/config.py`.

### C.5 Judge panel

| Judge | Model identifier | Provider | In 5-judge primary? | Calibration performed? |
|---|---|---|:---:|:---:|
| Haiku | `claude-haiku-4-5-20251001` | Anthropic | Yes | Yes |
| Sonnet | `claude-sonnet-4-6` | Anthropic | Yes | No |
| Opus | `claude-opus-4-6` | Anthropic | Yes | No |
| GPT-4o | `gpt-4o-2024-08-06` | OpenAI | Yes | Yes |
| GPT-5.4 | `gpt-5.4` | OpenAI | Yes | Yes |
| Gemini Flash | `gemini-2.5-flash` | Google | No (sensitivity only) | Yes |
| Gemini Pro | `gemini-2.5-pro` | Google | No (sensitivity only) | Yes |

Judges are invoked independently (no cross-judge conditioning). Each judge sees: held-out ground-truth passage, subject context (name, source), question, response. Judge temperature 0. Judge output is a numeric 1-5 score plus a free-text justification. Calibration diagnostic results in §3.6.3.

### C.6 Memory-system ingestion and retrieval parameters

Controlled configuration (C1 / C3) holds the input identical across systems: each system receives the same extracted fact set used by the Base Layer pipeline, re-ingested through its own API. Native configuration (`_fullpipeline`) has each system ingest the raw training corpus directly via its own chunking and extraction.

| System | Ingestion endpoint | Ingestion unit (controlled) | Ingestion unit (native) | Retrieval top-k | Notable configuration |
|---|---|---|---|---:|---|
| Mem0 | `POST /v1/memories/` | One fact per POST | Raw corpus chunks (Mem0 chunker) | 10 | `infer=False` on controlled (store as-is, no reformulation). Failure mode: Mem0 may reformulate on `infer=True`, flagged in `docs/PROVIDER_ISSUES.md`. |
| Letta (archival) | `POST /v1/agents/<id>/core_memory/archival` | One fact per passage | Letta native chunking | 10 | 1 fact = 1 passage. Batch ingestion tested 135x faster but changes chunking behavior (see `run_memory_system.py` line 456-458). |
| Letta (stateful) | Agent state edit during ingestion | One fact per edit cycle | Raw corpus | n/a (read from block) | Evaluated as a separate path in §4.5, not as a row in the C1 / C3 conditions. |
| Supermemory | `POST /v3/memories` | One fact per memory, `containerTags=<subject>` | Raw corpus | 10 | `limit=10` on retrieval. |
| Zep | Graph ingestion via `zep_client.graph.add` | One fact per edge | Raw corpus | 10 | Retrieval via `client.graph.search(user_id, query, limit=10)`. |
| Base Layer | Direct into ChromaDB | One fact per vector | n/a (Base Layer has no native variant) | 10 | MiniLM embeddings, L2 distance, cosine-like similarity via `1 - dist^2/2`. |

All five systems use the same top-k of 10. All five are queried with the question text as the query. All five feed their retrieval output into the standard prompt schema (§C.2) as the context block.

### C.7 Ingestion exclusions and failure cases

| Subject / system | Issue | Resolution |
|---|---|---|
| Babur, C9 (raw corpus plus spec) | 422,772-word source exceeds Haiku context window. | Excluded from C9. 13 of 14 subjects report C9 numbers. |
| Letta native (all subjects) | Ingestion ceiling on archival passages; retrieval produces 0.34-0.47 dedup ratio, meaning a top-10 list often contains 3-5 unique facts. | Reported as-is in §4.4. Not excluded. |
| Mem0 native | Mem0's `infer=True` reformulated facts during native ingestion pilot. | Used `infer=False` on controlled configuration to hold input identical. Native variant retains `infer=True` (the realistic deployment path). |
| Zep graph bias | Zep graph retrieval surfaces entity-dense chunks over behavior-dense chunks. | Reported as-is. See `docs/PROVIDER_ISSUES.md`. |

### C.8 Analysis plan lock

The condition matrix was frozen in `docs/ANALYSIS_PLAN_LOCK.md` before scoring. Any condition added after the lock is reported separately (for example, the Tier 2 3-subject replication and the 3 wrong-spec derangement draws on the author's living-user replication).

---

## Appendix D. Validity Audit and Score Distributions

### D.1 Per-subject 5-judge primary aggregate (main gradient)

This table reproduces the §4.1 cross-subject gradient for reference. Every number is the 5-judge primary mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) over the 39-question behavioral-prediction battery per subject (40 for Franklin).

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

### D.2 Per-subject anchor-crossing on the low-baseline slice

Anchor-crossing rate is the fraction of per-question paired (C5, C4a) responses where the C4a 5-judge primary mean lands in a different integer rubric band than the C5 mean. Definition in §3.6.2 and `scripts/compute_anchor_crossing.py`.

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

Eight of the nine low-baseline subjects cluster in the 48-74% upward band. Babur is the low-baseline outlier (source corpus 422K words, partial pretraining exposure); he is the only subject whose upward-crossing rate falls below 48%, and his downward-crossing count (4 of 39) is mid-range. Sunity Devee's 74.4% upward rate is consistent with her unusually low C5 baseline of 1.03 noted in §4.1. Per-subject downward-crossing rates stay at or below 15% for every low-baseline subject. Source: `scripts/compute_anchor_crossing.py` executed against `results/global_<subject>/judgments_v2.json` and `results/hamerton/`.

### D.3 Rubric-handling validity audit (full report)

This audit is the formal report that §3.6.6 summarizes. It was produced by `scripts/audit_low_end_inflation.py`. Raw flagged cases live in `docs/research/s114_low_end_inflation_audit.json`; source response and judgment data are under `results/global_<subject>/`. The audit is restricted to the 9 low-baseline subjects (1,599 responses across C5, C2a, C2c, C4, C4a conditions).

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

Both rubric-handling effects (abstention over-credit at the low end, length inflation in C5) pull the measured C5 baseline upward. This shrinks the measured spec-vs-baseline gap. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift reported in §4.1. The paper reports the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact. A differentiated rubric that scores abstention as its own dimension, and a length-controlled scoring protocol, are both flagged as follow-up in §7.

### D.4 Per-judge score matrices

Per-subject by per-judge score means for C5 (baseline) and C4a (facts plus spec) conditions are derivable from the raw per-judge JSON files under `results/global_<subject>/*_judgments_<judge>.json` (and `results/hamerton/` for Hamerton). The slice-level picture is already reported in §3.6.3 (calibration) and §4.6.2 (5-judge vs 7-judge sensitivity), which together establish that directional agreement is tight (Spearman ρ 0.86 to 0.93) while absolute magnitude varies (Krippendorff α 0.659 5-judge, 0.535 7-judge).

Full per-subject by per-judge by per-condition mean-score matrix for the 14 main-study subjects across the 5 gradient conditions (C5, C2a, C2c, C4, C4a):

Each cell is the per-judge mean score across all behavioral-prediction questions for a (subject, condition, judge) triple. Judges abbreviated: H=Haiku 4.5, S=Sonnet 4.6, O=Opus 4.6, 4o=GPT-4o, 5.4=GPT-5.4, gF=Gemini 2.5 Flash, gP=Gemini 2.5 Pro. 5m = 5-judge primary mean, 7m = 7-judge mean.

"n/a" indicates missing judge-condition coverage (most commonly: Gemini judges not run on C2c or C4 for some subjects; see §4.6.2 on 5-judge vs 7-judge coverage).

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

The matrix is 14 subjects x 5 conditions x (7 per-judge columns + 5-judge primary mean + 7-judge mean) = 70 rows x 9 columns = 630 cells. Subject rows follow the C5-baseline ordering used in §4.1 (lowest baseline first). Empty Subject cells continue the previous subject's rows. Gemini Pro "n/a" entries reflect that Gemini Pro was run as a sensitivity judge only on a subset of subjects (§4.6.2); those cells were never populated. Franklin is not included in this matrix because the Franklin control condition set does not align to the C5 / C2a / C2c / C4 / C4a labels used in the global-subject run; Franklin's judgments are reported in §4.2 and are stored under `results/franklin_legacy_20260411/analysis/`. Source: `scripts/_emit_full_judge_matrix.py`, which aggregates from `results/global_<subject>/*_judgments_<judge>.json` and `results/hamerton/`.

### D.5 Example verbatim responses at each rubric anchor

Verbatim-response examples at rubric anchors 1-5 for one representative subject (Hamerton) are in §3.6 as part of the rubric definition. Examples at anchor crossings are developed in §4.1 (Examples A, B, C on Ebers, Bernal Diaz, Seacole). Three illustrative paired (C5, C4a) per-question excerpts for each of the 14 main-study subjects are collected in Appendix E. The raw response JSON files (`results/global_<subject>/results_v2.json`) contain every response verbatim alongside its 5-judge primary score.

---

## Appendix E. Selected per-subject excerpts

This appendix provides three illustrative paired (C5, C4a) cases per subject for readers wanting concrete examples of the specification's effect at the per-question grain. Cases are selected by largest C4a minus C5 panel-mean Δ within each subject, requiring both responses to be present and non-empty. Excerpts are truncated for readability; full responses are at `results/<subject>/results_v2.json` (or `results/hamerton/results.json` for Hamerton). Per-question scores are 5-judge primary means (haiku, sonnet, opus, gpt4o, gpt54).

### E.1 Hamerton (baseline C5 = 1.26)

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


### E.2 Sunity Devee (baseline C5 = 1.03)

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


### E.3 Ebers (baseline C5 = 1.02)

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


### E.4 Fukuzawa (baseline C5 = 1.67)

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


### E.5 Seacole (baseline C5 = 1.77)

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


### E.6 Bernal Diaz (baseline C5 = 1.70)

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


### E.7 Keckley (baseline C5 = 1.84)

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


### E.8 Yung Wing (baseline C5 = 1.88)

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


### E.9 Babur (baseline C5 = 1.76)

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


### E.10 Augustine (baseline C5 = 2.58)

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


### E.11 Cellini (baseline C5 = 2.38)

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


### E.12 Equiano (baseline C5 = 2.77)

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


### E.13 Rousseau (baseline C5 = 2.44)

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


### E.14 Zitkala-Sa (baseline C5 = 2.34)

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

This appendix develops, benchmark by benchmark, the scope differences summarized in §2.1 between prior work on memory and personalization benchmarks and what this paper measures. The load-bearing point in each case is the same: representational accuracy, operationalized as behavioral prediction on held-out reasoning situations, is not what these benchmarks evaluate. None of them is wrong on its own axis. None of them is a substitute for the test in this paper.

### F.1 LongMemEval

**Reference.** Wu et al., ICLR 2025, arXiv:2410.10813.

**Task.** Evaluate long-term memory in chat assistants across multiple sessions. Five capability dimensions: single-session memory, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.

**Scoring.** Question-answering accuracy, with held-out facts embedded across session history and queried in a later session. Answers are compared against ground-truth factual targets drawn from the same session history the system ingested.

**Training / test protocol.** Conversation history is ingested; the system is then queried with fact-recall questions whose answers are present in the ingested history. The test is whether the memory system can surface the correct facts at retrieval time.

**What it measures.** Fact recall across long context windows. A secondary axis tests whether the system correctly abstains when the answer is not in the conversation history.

**What it does not measure.** Whether the memory system's representation of a specific person captures how that person reasons. Every LongMemEval target is a fact that was literally said in the conversation; no target is a held-out behavioral pattern.

**Published range.** Memory systems reported in the 68% to 85% range depending on provider, model, and benchmark variant (cited in §1.1 and §2.2). Specific numbers per system are in the papers and vendor reports.

**Relationship to this paper's test.** Orthogonal axis. Our battery targets held-out behavioral patterns that were never literally said in the training half of the corpus; every question is backward-designed to answer only from patterns, not from retrievable content. A system that ranks at the top of LongMemEval can still sit near the rubric floor on our battery, and a system that ranks low on LongMemEval (for example, Base Layer's retrieval substrate) can contribute on our battery through the specification rather than through retrieval.

### F.2 PersonaGym

**Reference.** Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416.

**Task.** Evaluate persona fidelity in conversational agents. Given a described persona, measure whether the model maintains that persona across a conversation.

**Scoring.** Persona-consistency metrics over multi-turn conversation. LLM-judge evaluation of whether the model's voice, stated preferences, and surface-level claims remain consistent with the described persona.

**Training / test protocol.** A persona is described (occupation, background, preferences, mannerisms). The model is prompted to roleplay the persona across a dialogue. Evaluation is whether the dialogue responses remain internally consistent with the persona description.

**What it measures.** Persona presentation fidelity. Can the model stay in character on the described dimensions.

**What it does not measure.** Whether the model accurately predicts how the person described by the persona would respond to new situations. A persona-fidelity system can maintain voice without ever accurately anticipating decisions. A representationally accurate system can shift voice (for example, from formal prose to casual conversational register) while continuing to predict accurately on behavioral questions.

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

Twin-2K measures whether a model can interpolate a person's survey distribution from other survey responses. Our battery measures whether a representation of how a person reasons transfers to new situations the representation has never seen. Both are legitimate tests of behavioral prediction; neither is a substitute for the other.

An earlier exploratory Base Layer run against Twin-2K's battery produced positive results on that task format, but we do not report those numbers as a formal benchmark comparison because the experiment used a prior iteration of our pipeline, and the task targets are substantively different (see §2.1).

**Published best-number.** Top individual-level accuracy of 71.72% on held-out survey items using a text-persona representation served to GPT-4.1-mini (Toubia et al., arXiv:2505.17479). Human test-retest reliability on the same instrument was 81.72%, putting the top twin at 87.67% of the human ceiling. Random-guess baseline was 59.17%. Aggregate-level replication: the Twin-2K twins reproduced results from 6 of 10 behavioral-economics experiments, with systematic divergences on medical decision-making and political attitudes. The 71.72% accuracy is on Likert interpolation, which is a structurally different task from our rubric-scored free-text behavioral prediction.

### F.5 LoCoMo

**Reference.** Maharana et al., ACL 2024, arXiv:2402.17753.

**Task.** Conversational memory quality over long multi-session dialogues.

**Scoring.** Fact-recall questions over ingested dialogue history. Similar scope to LongMemEval but focused on conversational-memory substrates specifically.

**Training / test protocol.** A long multi-session conversation is ingested; the memory system is queried on specific facts from earlier sessions.

**What it measures.** Long-dialogue recall accuracy.

**What it does not measure.** Behavioral reasoning. LoCoMo targets are literal recalls from session history.

**Published range.** LoCoMo paper baselines (Maharana et al., arXiv:2402.17753): GPT-4-turbo 32.1% overall, GPT-3.5-turbo 22.4%, GPT-3.5-turbo-16K 37.8%, best RAG configuration 41.4%; human performance 87.9%. Memory-system claims on LoCoMo, detailed in §2.2: Mem0g variant 68.44 with GPT-4o-mini (peer-reviewed, Chhikara et al., arXiv:2504.19413); Mem0 production algorithm 91.6 self-reported with open-sourced evaluation harness; Letta 74.0 with GPT-4o-mini; earlier Zep claim of 84 publicly disputed by Mem0 (see §2.2 dispute note). The methodology disagreement between vendors remains unresolved; §2.2 treats these single-number comparisons with explicit caution.

**Relationship to this paper's test.** The benchmark the four memory systems (Zep, Letta, Mem0, Supermemory) compete on. §2.2 uses these results as context for the memory-system landscape. Our paper is orthogonal: we do not evaluate memory systems on LoCoMo; we evaluate their behavioral-prediction performance on held-out autobiographical passages with and without the Behavioral Specification added.

### F.6 MemOS and related systems-level benchmarks

**Reference.** Systems-level memory benchmarking literature, including MemOS and adjacent evaluations. See §2.2 for the memory-systems landscape.

**Task.** Evaluate memory-layer infrastructure choices (storage substrate, retrieval algorithm, consistency properties) rather than memory-quality outcomes.

**Scoring.** Varies. Typically: retrieval latency, throughput, consistency guarantees, scalability benchmarks.

**What it measures.** Infrastructure properties.

**What it does not measure.** Representational accuracy, persona fidelity, or preference alignment. Systems-level benchmarks do not evaluate the quality of the representation the memory layer produces; they evaluate the mechanics of how that representation is stored and served.

**Relationship to this paper's test.** Different layer of the stack. Our paper evaluates what gets stored and why; systems-level benchmarks evaluate how well it is stored and served. Both matter for deployed personal-AI systems. The specification and the memory-layer infrastructure compose: our §4.4 Mem0 / Letta / Zep / Supermemory / Base Layer results show the specification adding on top of each infrastructure choice, not replacing it.

### F.7 What no prior benchmark measures

Pulling the per-benchmark analysis together, the axis that representational accuracy sits on is not covered by any prior benchmark:

1. **Test data the system has not seen.** LongMemEval, PersonaGym, and LoCoMo target content the system has ingested. Twin-2K's held-out items are drawn from the same structured instrument. Our battery's held-out passages are from unseen chapters in a different narrative register than the training half.
2. **Open-ended behavioral prediction rather than structured-format scoring.** Twin-2K is the closest comparison; it is Likert-format rather than open-ended.
3. **Representation of how a person reasons, not what they said or prefer.** PersonaGym tests voice consistency; AlpsBench tests preference alignment; LongMemEval / LoCoMo tests fact recall. None tests transfer of interpretive patterns.

This is the gap the paper's battery targets. The battery is not a replacement for any of the above. It is a test of a different property: whether a representation of a specific person enables a model that has never seen the person's held-out reasoning to anticipate it accurately.

---


## Appendix G. Letta Stateful-Agent: Exploratory Case Study (full)

*Body summary in §4.5. This appendix retains the full method, per-subject results, robustness checks, content analysis, and caveats from the original §4.5 in v9 / earlier drafts of v10.*


**This section is a post-hoc exploration, not a replication or a headline finding.** N=3 subjects (Hamerton, Ebers, Babur), one Letta version, one response model (Claude Haiku), a 40-question battery per subject. The intent is to characterize what Letta's stateful-agent architecture produces when invoked directly, and how that compares at matched response model to Base Layer's unified-brief variant. It is not an attempt to establish that two systems reach a common target.

> **Headline result on the small sample tested (5-judge primary):** Letta's self-edited memory block scores higher than Base Layer's unified-brief variant on all 3 subjects at matched response model. Hamerton **3.10 vs. 2.96** (Δ +0.14), Ebers **2.76 vs. 1.72** (Δ +1.05), Babur **2.42 vs. 1.88** (Δ +0.54). A robustness rerun against Base Layer's full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The matched-model gap is largest at the mid-corpus subject (Ebers) and smaller at both endpoints; with three data points the shape is consistent with a corpus-size band where the self-edited block is most effective, with degradation as the block grows, or with insufficient interpretive content when the corpus is small. Multi-subject replication is flagged as the highest-priority external falsification (§7.5).

Letta is the one commercial memory system in the study whose architecture supports an alternative to retrieval at query time. Alongside the archival retrieval path tested in §4.4, Letta agents maintain a persistent memory block that the agent itself rewrites during ingestion. This is the stateful-agent design from the original MemGPT paper. It is architecturally distinct from retrieval-based memory: the representation is authored by the agent over the course of reading the source corpus, rather than chunked and indexed for later retrieval. §4.5 examines what that produces on a small set of subjects, with the caveats above. Multi-subject replication across the full gradient, multiple response models, and a comparison against the Base Layer full layered stack (rather than the compressed variant used here) are flagged as follow-ups in §7.5.

---

**Test design.** A fresh Letta agent was initialized and fed the training half of each subject's corpus turn-by-turn. The agent was allowed to self-edit its memory block during ingestion, its native MemGPT behavior. After ingestion, the resulting memory block was extracted and served as context to Claude Haiku 4.5, the response model used throughout the main study. The behavioral-prediction battery was the main-study battery. Three subjects were tested, spanning a 9× corpus-size range:

| Subject | Source corpus | Corpus size (words) | Letta block size (chars) |
|---|---|---:|---:|
| Hamerton | Philip Gilbert Hamerton, *An Autobiography* (training half) | 25,231 | 22,472 |
| Ebers | Georg Ebers, *The Story of My Life* (training half) | 48,161 | 68,413 |
| Babur | Babur, *Babur-nama* (training half) | 222,742 | 335,349 |

The direct comparison: Letta's stateful-path memory block fed to Haiku, vs. Base Layer's full-stack specification fed to the same Haiku, on the same battery and judge panel. Both are interpretive representations delivered as context; the test isolates the representation itself.

---

**Methodological note on the Base Layer condition served here.** The Base Layer side of this matched-rerun loaded the unified brief variant (a ~7K-character synthesized document served as a single artifact) rather than the full layered stack (anchors + core + predictions + brief) that §4.4's controlled and native C2a / C3 conditions use. The unified brief is more compressed on referential detail than the layered stack. A layered-stack rerun on these three subjects would likely narrow the Letta-over-BL gap; whether it narrows to parity or reverses is not measured. The table column header below reflects this: the Base Layer side is the unified brief variant.

**Result (5-judge primary: Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).**

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Babur | 2.42 | 1.88 | **+0.54** |

On all three subjects tested, Letta's stateful-path block, served to the same response model as the Base Layer unified brief, produces a higher per-subject mean score than the unified brief. Both representations land well above the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec for these subjects: Hamerton near parity with Base Layer retrieval, Ebers +0.31, Babur near-null).

**Judge-panel robustness.** The 7-judge sensitivity aggregate (Hamerton +0.093, Ebers +0.746, Babur +0.232; see `docs/research/letta_stateful_matched_rerun.md` Part 7 appendix) preserves direction on all three subjects. The 5-judge primary values are larger than the 7-judge values on Ebers and Babur by +0.30 and +0.31 points respectively, because the two Gemini judges were inflating Base Layer scores relative to the calibrated core on those subjects. Excluding Gemini from the aggregate (the paper's 5-judge primary convention; §3.6.3 and §4.6.2) therefore widens the Letta-over-BL gap rather than narrowing it. Hamerton is the exception (5-judge Δ +0.14 vs. 7-judge +0.09), where Gemini inclusion slightly narrowed the gap rather than widening it. In all three cases, the Letta-block-outperforms-BL-spec direction is stable across panels.

---

**Compression behavior: divergence at large corpora.**

Letta's memory block grew roughly linearly with source corpus size. At the largest subject (Babur), Letta's API began rejecting ingestion requests at approximately 333,000 characters. After 22 consecutive failed ingestion attempts, the final block measured 335,349 characters. Letta's declared block-size metadata limit is 100,000 characters, unenforced in practice; the effective ceiling on the server side appeared to be a different API-level limit around 333K.

At the ceiling, the block contained **25.4% verbatim sentence duplication** on Babur, compared to 0% duplication on Hamerton and 0% on Ebers. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing. The representation carries corpus-derived narrative at scale but does not preserve the compression property that makes large corpora tractable.

**Semantic-similarity duplication.** A sentence-embedding analysis (post-hoc, this paper; `scripts/analyze_letta_semantic_duplication.py`, MiniLM-L6-v2, sentence-pair cosine ≥ threshold) shows that the verbatim figure understates the duplication. The self-editing agent paraphrases prior sentences as well as repeating them. On Babur, 73.8% of sentences have a near-duplicate at cosine ≥ 0.80, 56.1% at ≥ 0.85, 41.4% at ≥ 0.90, and 35.2% at the strict ≥ 0.95 threshold (paraphrase-level matches). Ebers shows minor near-paraphrasing (11.5% / 3.3% / 1.1% / 0.5% across the same thresholds). Hamerton shows none at any threshold above 0.80. The pattern matches the verbatim direction. Sample matches at ≥ 0.95 on Babur include `"Emotional Resilience in Governance: Bābur's personal reflections..."` paired with `"Emotional Resilience in Leadership: Bābur's reflections on challenges..."` (cosine 0.957): same template, slight rewording. Full per-threshold rates and sample matches in `docs/research/letta_semantic_duplication_20260501.json`.

Base Layer's compose step keeps the full-stack specification at 34,000-40,000 characters across the same corpus-size range. At Hamerton, the two representations are the same order of magnitude in size; at Babur, the Base Layer specification is roughly one-tenth the size of the Letta block. The two systems are prediction-band compatible at small corpora; they diverge on compression at large ones.

**What the ceiling means for deployment.** Served on every query, a 335,000-character Letta block costs roughly 84,000 tokens of context. At current frontier pricing this is materially more per-query cost than the Base Layer specification's ~10,000 tokens, and it exceeds the context window on the smaller-context models still common in production (128K token windows struggle when the block alone is two-thirds of the budget, before any conversational state). The duplication observed at the ceiling combines 25.4% verbatim sentence repetition with substantial semantic near-paraphrasing (35.2% of sentences at cosine ≥ 0.95, 56.1% at ≥ 0.85). The block would be functionally much smaller with a deduplication pass. Conservatively (one-of-each-pair removal at ≥ 0.85), roughly 30% of the block is removable; aggressive cluster-collapse deduplication at the same threshold could reach a 50% reduction, taking the block from ~335K to ~170K characters at preserved content. A semantic-similarity deduplication pass on the self-edited block is a tractable post-processing step that this study does not run but recommends. For production deployment, the ceiling, the verbatim duplication, and the additional semantic duplication together argue for representation compactness as a first-class design constraint, not a nice-to-have.

---

**What this exploration does and does not show.**

On N=3 subjects, with one response model and one Letta version, Letta's stateful-path block and Base Layer's unified-brief variant both land above retrieval-only context at matched response model, in a similar prediction band. This is consistent with (though does not establish) the idea that the behavioral-specification target is reachable by representation-production mechanisms outside offline-authored retrieval composition. Establishing that would require multi-subject replication across the full gradient, multiple response models, and a comparison against Base Layer's full layered stack rather than the unified-brief variant tested here. All three are flagged in §7.5.

What the exploration does show is the shape of the engineering tradeoff between the two paths. They differ in how the representation is produced (offline authoring vs. online self-editing), in what it carries (interpretive scaffolding vs. corpus-derived narrative at higher referential density; see content comparison below), and in how it scales (bounded compression vs. an ingestion ceiling observed at ~333K characters on the largest corpus we tested). These are tradeoffs to characterize, not a resolved comparison.

---

**Content comparison: what each representation retains.**

To test whether Letta's higher matched-model score comes from preserving original corpus text the response model could cite, we ran a post-hoc content analysis on the three subjects. The strong form of that hypothesis is refuted. Neither representation is a quote library. Checking what fraction of consecutive five-word sequences in each representation also appears verbatim in the training corpus (a standard overlap check), both representations score under 1%: the Letta block ranges 0.0-1.0% depending on subject, the Base Layer specification scores 0.0% on all three. The same check for consecutive ten-word sequences gives under 0.1% for both. Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts.

A refined version of the hypothesis does hold, with the magnitude smaller than first reported. The two representations differ in **referential density**: Letta's rolling summary retains more unique proper nouns, dated events, and named secondary characters than Base Layer's §4.5 specification, and the gap scales with corpus size. On Babur (the largest corpus), Letta's block carries 416 unique capitalized named-entity tokens vs. Base Layer's 65, a ratio of about **6×**. On Ebers (mid-size), the counts are 53 vs. 34, a ratio of about **1.5×**, closer to parity. Base Layer, by construction, compresses episodes into cross-cutting behavioral patterns with fewer surface referents; the pipeline explicitly anonymizes the subject during authoring and compresses corpus-level specifics into dimensional axioms. Letta's stateful-agent path preserves more of the referential surface while also encoding behavioral patterns. The referential-density gap is real but corpus-dependent rather than uniformly an order of magnitude.

Both representations produce responses that outperform retrieval-only context at matched response model, but they diverge on referential detail. On battery items that reward specific-event recall, Letta has more named entities to cite. On items that reward principled interpretation across episodes, Base Layer's dimensional axioms compete directly. The §4.5 matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects. Flagged in §7.

**Replication as the load-bearing next step.** The three-subject comparison reported here is not a claim that alternative representation-production architectures reach the interpretive-representation target. It is a case study with direction but not power. Multi-subject replication across the full 14-subject gradient (layered-stack Base Layer vs. Letta stateful, both anonymized to match, multiple response models) is the highest-priority external falsification we can run on §4.5, and is flagged as such in §7.5. If that replication closes the gap at parity, §4.5's direction holds on a wider sample. If it reverses, §4.5's direction was corpus-specific.

Full content analysis at `docs/research/` (see `_content_analysis_results.json` and the N=3 per-subject breakdown). The methodological note on the Base Layer condition is now hoisted above the result Table at the top of this section.

---

**Caveats.**

- N = 3 subjects on this path. Extending across the full 14-subject gradient would let the comparison speak to the population-of-relevance level, not only a selected set of corpus sizes. Flagged in §7.5.
- One response model (Haiku) on both conditions. The comparison is tested at matched response model; whether it holds at other response models is an open question.
- Letta's 333K-character ingestion ceiling is a hard architectural constraint in the current release. For small corpora the two representations are interchangeable in prediction behavior; for large corpora the ceiling is material.
- Base Layer condition used the unified `spec.md` variant for the main §4.5 table. A robustness rerun with the full layered stack (anchors + core + predictions + brief, name-restored to match the §4.5 naming convention) preserves direction on all three subjects (Δ_Letta−BL = +0.27 / +1.21 / +0.38 on Hamerton / Ebers / Babur; full report at `docs/research/_letta_rerun/fullstack_named/RESULTS.md`). The gap widens at the two smaller corpora and narrows at Babur, consistent with a Pattern 2 (over-theorization) effect on small corpora rather than a content-volume effect at large corpora. Direction is invariant across both Base Layer spec forms.
- **Naming asymmetry.** Letta's stateful-agent path ingested the named source corpus and wrote a memory block that references the subject by name throughout. Base Layer's authoring pipeline strips the subject's name during specification authoring (§3.7 anonymization step); the §4.5 comparison restores the name at the surface level only (string substitution on the composed artifact). The two sides of the comparison therefore differ in whether the subject's name is load-bearing during representation production vs. only at serving time. Flagged as a methodological gap in §7.5.

---

**Raw data and scripts.** Letta stateful matched-rerun data at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json`. Generation and scoring scripts live in the same directory as a numbered chain (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, `70_compute_5judge_primary.py`); see the `README.md` inside `docs/research/_letta_rerun/`. Full characterization of block content, duplication behavior, and API responses in `docs/research/letta_stateful_deep_read.md` and `docs/research/letta_stateful_matched_rerun.md`.

---


## Appendix H. Glossary

Defined terms used as terms of art throughout the paper.

**5-judge primary panel.** The locked judge aggregation for headline numbers. Aggregation rule: per-judge per-question score → per-judge per-subject mean → panel mean across {Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4}. See §3.6.3.

**7-judge sensitivity panel.** The 5-judge primary plus Gemini 2.5 Flash and Gemini 2.5 Pro, reported as a sensitivity check. See §3.6.3.

**Anchors / Core / Predictions.** The three layered artifacts comprising a Behavioral Specification. Anchors: short axiomatic claims about how the subject reasons. Core: connects anchors into coherent reasoning patterns. Predictions: derives forward-looking decisions from the core. A composed brief sits above all three. See §3.7.

**Behavioral prediction.** The operational test for representational accuracy. Given a situation drawn from text the model has never seen, the model generates how the subject would respond; the response is scored against the subject's own verbatim response on a 1-5 interpretive rubric. See §1.1, §3.6.

**Behavioral Specification.** A static document of approximately 7,000 tokens that extracts and encodes a person's behavioral patterns. Composed of three layered artifacts (anchors, core, predictions) plus a unified brief. Layered above memory-system retrieval as an interpretive structure. See §1.1, §3.7.

**Cross-anchor interpretation rule.** A fractional delta between two conditions that crosses an integer rubric anchor (1, 2, 3, 4, or 5) reflects a categorical shift in the underlying response distribution. A delta that stays inside a single integer band is a within-category shift and a weaker claim. See §3.6.2.

**Interpretation.** In this paper, the human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. The property the Behavioral Specification is designed to mirror. See §1.1.

**Multi-anchor crossing.** A single question whose 5-judge primary mean shifts across two or more integer rubric bands when the condition changes. Crossings can span two bands (e.g., 1 → 3) or, more rarely, three bands (e.g., 1 → 4 or 2 → 5). The strongest categorical signal the rubric detects. See §3.6.2, §4.2.

**Personalization (this paper's sense).** Representing the interpretive layer that sits beneath stated preferences and biographical facts: how a specific person organizes experience, what they treat as evidence, what reasoning patterns they apply across new situations. Distinguished from surface-level responsiveness to stated preferences (dietary restrictions, communication style) or stored facts about the user (location, occupation, history), which are downstream artifacts of the interpretive layer rather than the layer itself. See §2 lede.

**Refusal (abstention).** A response in which the model declines to predict because the available context does not support a prediction. Distinct from a substantively wrong prediction; under the current rubric both score at the lowest anchor (1). Detection in the validity-audit script uses phrase patterns ("no specific information," "I cannot confirm," "would need additional context"). See §3.6.6.

**Representational accuracy.** The AI-side property: how faithfully a model's internal representation of a specific person captures that person's interpretive patterns. Operationalized via behavioral prediction on held-out reasoning situations. See §1.1, §3.1.

**Specification-effect claim.** When a Behavioral Specification is served to the model as context, the model's responses shift in the direction of the subject's demonstrated behavioral patterns, and that shift registers as a measured increase in representational accuracy against held-out passages from the same subject. The claim is directional, not a claim of new model capability or absolute correctness. See §3.6.4.

**Tier 1 / Tier 2.** Tier 1 is the main study: Haiku 4.5 response model across all 14 subjects, every condition, Haiku-generated batteries. Tier 2 is the cross-provider directional probe: Sonnet 4.6 and Gemini 2.5 Pro response models on 3 subjects (Ebers, Yung Wing, Zitkala-Sa) with GPT-5.4-regenerated batteries. See §3.5, §4.6.1.

**Wrong-spec control.** A deliberately mismatched Behavioral Specification served in place of the correct one. Two variants: **v1** (adversarial fixed derangement maximizing cultural and temporal distance; aggregate Δ −0.25) and **v2** (seed-fixed random derangement; aggregate Δ +0.15). See §1.3, §3.4, §4.3.

