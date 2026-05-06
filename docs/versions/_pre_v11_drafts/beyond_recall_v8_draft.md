# Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization

**Author:** Aarik Gulaya, Base Layer
**Date:** April 2026
**Preprint** (Apache 2.0)
**Data + Code:** github.com/agulaya24/base-layer
**Study Repository:** github.com/agulaya24/memory-study-repo

---

*v7 working draft — appended section by section as each locks in review.*
*v6 (`beyond_recall_v6_draft.md`) remains the reference source for sections not yet re-locked.*

---

## 1. Introduction

### 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant. Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. Think of how viewing situations from different lenses can lead to entirely different interpretations of the same set of facts. This has been shown across the human experience, from the sciences to religion to political affiliations, and by extension to the relative experiences of any individual. Memory is deeply personal. For an AI memory system to serve a specific person, it must be personalized to how that person interprets, not just to what facts they have produced.

We introduce **representational accuracy** as the corresponding AI-side property: how well a system's internal model of a specific person captures that person's interpretive patterns. It is not recall, preference matching, or persona consistency. It is a distinct property of the AI system, and the benchmarks current memory systems are evaluated on do not isolate it. Prior work closest to this axis (Twin-2K for scaled behavioral prediction, PersonaGym for persona fidelity, AlpsBench for preference alignment) measures related properties but not the transfer of a person's interpretive patterns to novel situations the system has never seen. §2.3 positions each benchmark against what this paper measures, and Appendix E develops the scope differences in detail.

**The core hypothesis of this research is that representational accuracy predicts alignment between an AI system's behavior and the intent and behavior of the person it serves.** If an AI system's model of a person accurately captures how they interpret situations, its responses should align with that person's intent and behavior in situations the system has never seen. The operational test is behavioral prediction on held-out situations, used here as a proxy for this alignment.

We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated LLM judges to evaluate the performance of each memory system, on its own and in combination with a behavioral specification: a static document that extracts and encodes a stable representation of a corpus's behavioral patterns.

### 1.2 What We Tested

We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model. The test was whether each system could predict how that specific person would respond in situations drawn from text it had never seen.

**Hypotheses.** The study tests five claims about how a representation of a person shapes AI behavior on that person's behalf:

- **H1.** A response model given a Behavioral Specification for a person produces responses that align with that person's documented behavior more closely than the same model given no context.
- **H2.** The specification's benefit is inversely proportional to the response model's pretraining coverage of the person. Its effect is largest on people the model does not already know.
- **H3.** The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.
- **H4.** The specification is composable with existing memory-system retrieval pipelines, not a replacement for them. When added to commercial memory systems, it improves their behavioral prediction additively.
- **H5.** A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size. Structure is the carrier of the representation, not the volume of text.

The five hypotheses map directly to §4: H1 and H2 to §4.1 The Gradient; H3 to §4.3 Mechanism; H4 to §4.4 Memory-System Composition; H5 to §4.2 Compression.

**Primary and secondary outcomes.** The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule (within-judge mean, then across-judge mean; subject is the unit of inference). As a **secondary outcome**, we report the per-question **win rate against the no-context baseline**: for each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), classify the outcome as improved / tied / worsened, and report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the **breadth of benefit** of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

The experiment has two main splits. The first is a **controlled test**: each memory system is given an identical, pre-extracted fact pool drawn from the training half of the corpus. Holding the input constant lets us measure whether the providers converge on what is most relevant when they see the same facts. The second is a **native test**: each memory system ingests the raw corpus through its own pipeline, as it would in production. This measures real-world performance when each system is allowed to do what it is designed to do. Running in parallel across both splits is the Behavioral Specification, tested alone and layered on top of each configuration.

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
| **Wrong-specification control** (C2c) | A different subject's specification applied to this subject. Two variants: v1 is a deterministic fixed pairing that matches each subject with a culturally and temporally distant other (mapping in `scripts/run_global_rerun.py`); v2 applies a random derangement, seed-fixed, so no subject receives its own. Hamerton has an additional variant (Franklin's specification) reported separately in §4.1.1. | Tests whether the effect is driven by the content of the correct specification, or by the mere presence of structured prompting. |

**Additional testing for Letta.** Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions above, we ran a separate test on three subjects spanning a 9× corpus-size range (Hamerton, Ebers, Babur). A fresh Letta agent ingested each training corpus turn-by-turn and was allowed to self-edit. The resulting memory block was then served to the same response model used throughout the main study for a matched comparison against the Behavioral Specification. Full methodology and results are in §4.4.1 and §4.7.

The 14 subjects span four continents and roughly two millennia of written human experience. Ordered chronologically: Saint Augustine (North Africa, 4th-5th c.), Babur (Central Asia and India, 15th-16th c.), Bernal Diaz del Castillo (Spain and Mexico, 15th-16th c.), Benvenuto Cellini (Italy, 16th c.), Jean-Jacques Rousseau (France, 18th c.), Olaudah Equiano (West Africa and Britain, 18th c.), Mary Seacole (Jamaica and Britain, 19th c.), Elizabeth Keckley (United States, 19th c.), Yung Wing (China and the United States, 19th c.), Philip Gilbert Hamerton (Britain, 19th c.), Fukuzawa Yukichi (Japan, 19th c.), Georg Ebers (Germany, 19th c.), Sunity Devee (India, late 19th c.), and Zitkala-Sa (Yankton Dakota, early 20th c.). Source corpora range from 25,231 words (Hamerton) to 422,772 words (Babur). Full source references are in §3.2.

Predictions were scored on a 1-5 rubric. One-point differences on this scale are qualitative shifts, not small numerical adjustments. Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

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

Each condition was evaluated with 6 response models across 3 providers (Anthropic, OpenAI, Google) and a panel of seven LLM-as-judge models. Five non-Gemini judges (Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4) form the primary aggregate. Two Gemini judges (Gemini Flash and Gemini Pro) are reported as a sensitivity check because they systematically inflate absolute scores by approximately 1 point relative to the other five. Including them in the aggregate would widen the spec-effect deltas, not narrow them (§3.7.2), so the 5-judge primary is the more conservative choice for every headline finding. Judges were calibrated on known verbatim matches, paraphrase variants, off-target responses, and length-padded responses to measure each judge's ceiling behavior, paraphrase sensitivity, and length bias. The judges agree strongly on condition rankings (pairwise Spearman ρ = 0.89-0.98), and no subject's improvement direction changes between the 5-judge primary and 7-judge sensitivity aggregates. Full condition definitions, response model list, and judge calibration protocol are in §3.

### 1.3 What We Found

The Behavioral Specification improves representational accuracy, but not universally. The effect is a continuous gradient against baseline: strong where the model knows little about the subject, negligible or mildly counterproductive where the model already knows the subject well. The 14 subjects in this study are public-domain authors whose work is well-represented in training corpora, so their baselines are higher than those of typical living users whose private reasoning is in no training corpus. Nearly every real AI user is expected to fall in the low-baseline band, which makes the low-baseline slice of our results the population of relevance. The improvement is content-specific rather than format-driven, and the specification layers additively on every commercial memory system we tested, most strongly on that slice.

**Primary result: the gradient.** **The less the model already knows about a person from pretraining, the more the specification helps.** Linear regression of the facts-plus-spec effect against baseline gives slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001 for the slope coefficient. This p-value directly supports the gradient relationship itself; the separate Wilcoxon signed-rank test (p = 0.007, W = 11, N=14, C5 vs. C4a) confirms overall improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is backed by a substantially stronger per-response pattern: 55.0% of individual responses on the low-baseline slice cross a rubric integer anchor upward when the spec is added (§4.1), and 70.9% of questions improve at all (§4.2.1). This is a category-level change in the kind of answer produced, not a small numerical adjustment.

**Compression: structure captures most of the raw-source predictive signal at a fraction of the context.** **A compact specification of roughly 5,000-8,000 tokens (the full served artifact is ~8,000-10,000 tokens including the composed brief) recovers most of what the full raw corpus delivers, using a small fraction of the context. On Hamerton the specification exceeds the raw corpus; on the remaining low-baseline subjects the corpus slightly exceeds the specification by an average of 0.22 points while being an order of magnitude or more larger. The constraint on prediction is not the availability of information but the structure that makes information interpretable, and most of that structure fits in a compact representation.**

*Measurement.* On Hamerton, the Behavioral Specification alone (C2a, ~7,300 tokens) scores 2.63 on the 5-judge primary panel. The same subject's full training corpus loaded into context without a specification (C8, ~33,000 tokens) scores 2.27. The specification outperforms the raw source at roughly one-fifth the context size. Adding the specification on top of the full corpus (C9) lifts Hamerton to 3.09, the highest compression-related score observed in the study. Across the 9 low-baseline subjects, the average gap between spec-alone and raw corpus is 0.22 points. The corpus slightly exceeds the spec on most subjects, and the spec substantially exceeds the corpus on Hamerton. The efficiency claim is that the spec captures most of the raw corpus's predictive value at roughly 5% of the context. Full analysis in §4.2.

**Mechanism: content, not format.** **What produces the specification's effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A random other person's specification does not reproduce the effect, and a sufficiently mismatched specification degrades prediction below baseline.** On the 13 global subjects with complete 5-judge primary coverage, a wrong specification (random derangement, seed-fixed) scores near baseline with a mean Δ of +0.22 vs. +0.35 for the correct spec on the same subjects. A more adversarial control, a deterministic fixed pairing designed to maximize cultural and temporal distance between each subject and the specification it receives (mapping defined in `scripts/run_global_rerun.py`), scores clearly below baseline at Δ −0.25: when the mismatch is large, structured content for the wrong person performs worse than no context at all. Across 587 wrong-spec responses classified (validated against a 30-response stratified manual spot check), the response distribution is bimodal: 60.6% explicitly flagged the mismatch (example, from one Keckley wrong-spec response: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*) and either refused or produced a hedged response; 36.5% attempted to apply the mismatched specification and produced a low-quality prediction; 2.0% hedged implicitly; 0.9% were ambiguous. Specifications are anonymized by design (§3.3), so the 60.6% is a lower bound on content-grounded detection: the model is inferring the mismatch from interpretive content signals such as temporal markers, cultural domain, and life events described in the spec, not from surface name cues. A more capable response model, or a derangement that places subjects closer in cultural and temporal space, could push this rate in either direction; 60.6% is what a single Haiku-class response model detected on the seeded random derangement. The content-grounded detection confirms the core finding: the specific content of the correct specification drives improvement, generic structured prompting does not substitute for it, and sufficiently mismatched content actively degrades performance. The correct specification shifts response models in the opposite direction, across two independent hedging rules. Under a narrow rule (a response counts as hedged only if its first non-whitespace text matches an explicit refusal prefix: "I cannot," "I can't," "I don't," "I do not," "The retrieved facts do not," "The retrieved facts don't"), baseline hedging of 28.8% (146/507) drops to 1.4% (7/507) with the specification alone and 0.0% (0/507) with facts plus specification. Under a broader rule (any refusal pattern anywhere in the response), baseline hedging of 41.2% (209/507) drops to 7.9% (40/507) with the specification alone and 0.4% (2/507) with facts plus specification. Both rules agree in direction and magnitude: baseline hedges at roughly 4 to 20 times the rate of spec-containing conditions. Classifier, patterns, and per-subject counts for both rules are in `scripts/classify_hedging.py` and `docs/research/hedging_analysis.json`.

**Additivity: the specification improves prediction on three of four commercial memory systems.** **Adding the specification to a commercial memory system's retrieval produces positive mean Δ on three of the four systems we tested.** In the controlled configuration (each system given an identical pre-extracted fact pool), the specification produces positive mean Δ on the low-baseline slice for Mem0 (+0.10), Letta-archival (+0.17), and Zep (+0.17); Supermemory's Δ is near zero (−0.01). Across all 14 subjects, Mem0 (+0.12), Letta-archival (+0.20), and Zep (+0.19) remain positive on the 5-judge primary panel; Supermemory aggregates slightly negative (−0.05). Full §4.4 table. One-line per-system read:

- **Mem0**: positive spec Δ in both configurations (+0.12 controlled, +0.33 native). Spec composes additively with this system.
- **Letta**: the most architecturally distinct of the four. Letta exposes two memory paths, and the specification behaves differently on each. The archival-retrieval path (the one exercised in the main memory-system conditions) produces a spec-null result on native ingestion (−0.02). The stateful-agent path, where Letta writes and revises its own memory block during ingestion rather than retrieving from an external store, independently converges on an interpretive representation that resembles the Behavioral Specification. We read this as architectural validation of the interpretive-structure claim, not as two contradictory findings; the stateful-agent path is examined separately below.
- **Zep**: the largest mean spec Δ in the panel (+0.19 controlled, +0.33 native). Positive on 9 of 9 low-baseline subjects in both configurations.
- **Supermemory**: the highest C1 mean of the four (~2.65 vs. ~2.30 for the others on the 1-5 scale). The near-zero aggregate spec Δ hides large per-question swings in both directions; treated in the next finding.
- **Base Layer**: included as the zero-cost open-source retrieval floor (MiniLM-L6-v2 + ChromaDB). Mean C1 ~2.30 across 14 subjects, in the same band as the commercial systems. Spec Δ +0.08 on the low-baseline slice. Not positioned as a memory product; it is what an open-source retrieval stack produces at zero marginal cost.

**Where the specification helps and where it hurts.** **The specification's effect on a given memory system is not uniform across questions.** Supermemory's near-zero aggregate delta is a mixture: the specification helped on many questions and hurt on many others, in roughly equal measure, so the two sides cancel at the average. On Ebers (aggregate Δ +0.21), it helps on 19 of 39 questions and hurts on 10. On Keckley (aggregate Δ −0.26), it helps on 10 and hurts on 17. The per-question effects are often large (>0.3 points); averaging them hides strong disagreement at the individual-question level. This mixture pattern is not unique to Supermemory: Mem0, Letta, Zep, and Base Layer's own retrieval substrate each show per-question swings of similar shape at varying magnitudes, and the Keckley Q21 refusal response below recurs across every memory system we tested, with the penalty size proportional to how strong each system's retrieval-only counterfactual was. This tells us the refusal is a specification-level dynamic, not a memory-system artifact.

Three patterns emerge. The specification adds signal retrieval alone cannot on **interpretation-heavy questions** where a generalized pattern from the source has to transfer to a novel situation.

- **Ebers Q3**: *"How would Ebers characterize the emotional impact of natural beauty combined with a mentor's persuasive words?"* Supermemory-alone returned discrete facts about nature, teachers, and loyalty and gave a generic "transformative" answer (score 1.17). With the specification added, the model recognized the specific pattern that beauty and mentor's words function as *a single formative mechanism* rather than two additive inputs, and scored 3.00 (Δ +1.83).
- **Sunity Devee Q35**: *"What does she believe was the consequence of following official advice that conflicted with her own judgment regarding her son's education?"* Supermemory-alone answered generically about negative consequences (score 2.33). The specification carried an explicit anchor ("spiritual integrity over social cost") that let the model frame her recollection as self-accusation rather than as criticism of officials, and scored 4.33 (Δ +2.00).

The specification hurts on **literal-recall questions** where a plain answer is available and spec-driven theorizing drifts past it, and on **refusal-triggering questions** where the specification's honesty axioms produce epistemically-honest refusals that the content-match rubric scores as off-base.

- **Keckley Q21**: *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"* Supermemory retrieval alone acknowledged the gap in the retrieved facts and speculated productively from what it had about Elizabeth's relationship with her mother, scoring 3.83. With the specification added, the model invoked the spec's documented-dignity axioms, declined to fabricate interior motive, and told the user it could not answer without the specific passage; score 1.50. The rubric treats an epistemically-honest refusal identically to an off-base guess.

We read this as an interaction between the specification and the rubric rather than as a clean specification defect or a clean benefit. The specification induced epistemically honest refusal on a question where the retrieved facts were insufficient to answer without fabrication: armed with the spec's documented-dignity axioms, the response model chose not to invent interior motive it could not ground in evidence. Under a content-match rubric, that refusal scores identically to an off-base guess, which the current scoring cannot distinguish. Whether this is a specification-level problem, a benchmark-level limitation, or both depends on how one weights epistemic honesty against predictive coverage. A differentiated battery that separates interpretive prediction from literal recall and scores epistemic honesty as its own dimension would adjudicate the question directly, and is flagged as follow-up in §7.

**Robustness: the effect is not an artifact of Claude talking to Claude.** **The specification's effect holds when non-Anthropic models generate the test questions and non-Anthropic models read the specification.** On three subjects spanning the effect gradient, 5 of 6 (subject × response model) cells reproduce the specification direction when Sonnet or Gemini Pro reads questions generated by GPT-5.4. The one mismatch (Zitkala-Sa × Gemini Pro) is consistent with the gradient mechanism rather than a replication failure. This addresses within-Anthropic circularity, the concern that Anthropic-generated questions scored with Anthropic judges might favor Anthropic-produced specifications. LLM-as-judge circularity at the evaluation level remains a broader limitation of this study, flagged in §6.

**Architectural observation: Letta's stateful-agent path.** **Letta is the only memory system whose architecture allows the AI itself to write and revise a persistent memory block during conversation. When we invoked this path directly, the AI produced a representation resembling the Behavioral Specification in what it captured, but not in how it compressed.** On three subjects spanning a 9× corpus-size range, Letta's stateful-agent architecture (the self-editing memory block from the original MemGPT design, not the archival retrieval path our main conditions exercise) produces an interpretive representation that scores modestly higher than the Behavioral Specification at matched response model on all three subjects tested, with matched batteries and named-subject specifications throughout (5-judge primary: Hamerton 3.10 vs. BL 2.96, Δ +0.14; Ebers 2.76 vs. BL 1.72, Δ +1.05; Babur 2.42 vs. BL 1.88, Δ +0.54; full §4.7 Table). The Base Layer comparison artifact on this test is the unified brief variant rather than the full layered stack (§4.7 methodological note). This is architectural convergence: two independently-designed systems target the same property. Letta's memory block appears to grow roughly linearly with source corpus size: 22,472 characters (~5,600 tokens) at 25,231 words of source (Hamerton), 68,413 characters (~17,000 tokens) at 48,161 words (Ebers), and 335,349 characters (~84,000 tokens) at 222,742 words (Babur). At the largest corpus we tested, Letta's API began rejecting ingestion requests after the block reached approximately 333,000 characters; the final block, after 22 consecutive failed ingestion attempts, measured 335,349 characters. We noted 25% verbatim sentence duplication as the block approached that ceiling. Base Layer's compose step keeps the specification at 34,000-40,000 characters (~8,000-10,000 tokens) across the same range. For reference, 335,000 characters is roughly 67,000 words: less than a single short book, and substantially less than ten years of daily journaling or the full accumulated session history of a long-running personal AI assistant. The stateful-agent path encountered a structural compression ceiling on the largest corpus we tested; the Behavioral Specification's compose step did not. The gap at matched conditions is content-driven, not refusal-driven: Letta's larger block carries corpus-derived narrative the response model can cite, while the 7,000-token specification carries interpretive scaffolding only. We report this as a frontier question for stateful-agent memory architectures, not as a claim of superiority.

### 1.4 Why the Gradient Matters for Real Users

**What the gradient means for people who use AI in the real world.** **By structural extrapolation from the sample (not by direct measurement), real AI users are expected to sit at baselines lower than the historical subjects in this study, because their private reasoning is not in any training corpus.** Our 14 subjects are public-domain authors whose writing was preserved, digitized, and indexed into training corpora. In practice, they sit well above the pretraining representation of a typical living person. Even within this biased-up sample, the specification helped most where baseline was lowest: the 9 subjects below C5 ≤ 2.0 all improved. Zitkala-Sa and Equiano are the two subjects where the specification did not help; both sit in the mid-baseline band where pretraining coverage is more substantial. Our lowest subject (Sunity Devee) scores 1.03, near the floor of the rubric, a score that indicates the model either refuses or produces an unrelated answer. For a typical living user whose private decisions were never indexed, the baseline is expected to sit at or near this rubric floor: the author's own clean-methodology pilot (§4.1.2) landed at C5 = 1.03, below every historical subject in the main study. The structural implication is direct: if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, and if a methodology-matched living-user pilot lands at the same floor with the largest lift in the study (+2.00 on facts+spec), the specification should be at least as beneficial for typical real AI users as it is for the historical subjects measured here.

**What we did not prove.** **This is a single-subject direct measurement plus an extrapolation argument, not a multi-subject living-user replication.** The §4.1.2 pilot is N=1 living user (the paper's author), the only living subject whose private corpus we could ethically run through the pipeline. The pilot confirms the gradient's prediction for one person but cannot establish that the prediction holds across a population of living users. A multi-subject living-user replication (planned for §8 Future Work) is the single most important piece of follow-up work for this paper. We are also exploring alternative testbeds that isolate reasoning structure without requiring private data, including U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted. One other boundary claim belongs here: our judging remains LLM-as-judge at evaluation, so broader LLM-circularity concerns are not fully addressed by the cross-provider replication. We state this here because §1.3's claims rest on extrapolation past it.

**What this implies for AI personalization infrastructure.** **If nearly every real AI user is low-baseline, the gap cannot be closed by pretraining.** Every major model is trained on the public record. The private record (a person's reasoning, decision patterns, and interpretive lens) is not in any training corpus, and will not be in any training corpus, because that record does not exist in a form that can be trained on. The structural options are narrow. Either each user supplies their own representation to whatever AI system serves them, or personalization remains surface-level (style, voice, preference) without the interpretive substrate that makes an agent's actions actually reflect the person. The Behavioral Specification is one implementation of the first option, not the only one. What we claim is that personalization infrastructure of this shape is what the next generation of human-AI interaction will require: user-held, portable, inspectable, traceable, representation-grade. §1.5 develops this connection to behavioral alignment more fully.

### 1.5 Behavioral Alignment and the Human-AI Interaction Problem

**How this paper connects to the broader question of human-AI alignment.** **Behavioral alignment is one concrete, measurable instance of human-AI alignment: whether a specific AI system's actions accord with a specific person's reasoning, values, and decision-making when acting on that person's behalf.** The AI safety community typically uses "alignment" to mean preventing harmful behavior at the model level. That is one property. Behavioral alignment is a different property, and the two axes are orthogonal, not a hierarchy.

A model that is safely aligned in the safety sense can still be behaviorally misaligned with any given user: it will act reasonably, but not the way *you* would act. The inverse is also true and important. A perfectly behaviorally-aligned agent, acting exactly as a specific user would act, can be catastrophically safety-misaligned if that user would act maliciously, recklessly, or against third-party interests. Behavioral alignment is not a safety property. It is a personalization property that safety constraints must sit above.

**Representational accuracy is a necessary condition for behavioral alignment, but not sufficient.** A system cannot act the way someone would act if it lacks an accurate internal model of how that person reasons. Having the model is required; translating the model into aligned action, subject to safety constraints, is a separate problem we do not address in this paper. We focus on the representation layer because it is the piece that is under-studied and empirically tractable. An agent that acts on your behalf without an accurate representation of you is not serving you; it is averaging over some population the model happens to resemble.

The question this paper asks, operationally: **can the AI act the way you would act, given how you think?** The question the field should take up, more generally: **how do we know when an AI's internal model of a specific person is accurate enough for the agent to act on that person's behalf, and by what means do we improve and audit that representation?**

---

## 2. Related Work

Memory systems today optimize for recall. Some efforts build memory architectures modeled on human memory, but their targets remain general rather than individual. A separate body of research studies human reasoning itself: how people form representations of others, how schemas compress experience. The gap between these directions is the translation. How do we apply what we know about human reasoning to the direct interaction between an AI system and a specific individual, and how does the system's internal model of that individual take shape in a way that serves them rather than serving an average?

Language models are trained to produce responses that are helpful on average across a large population of users. That optimization target produces outputs that no single user is the reference point for. We do not want an unbiased system for personalization; we want a system biased to the individual. That kind of intentional bias, toward a specific person rather than toward a population aggregate, is the missing thread in current AI memory and human-AI interaction research.

### 2.1 Memory systems for LLM agents

The four commercial memory systems we evaluate (Mem0, Letta, Supermemory, Zep) have converged on a shared set of capabilities: semantic retrieval over embedded content, source attribution, multi-level memory structures, and benchmark-validated recall performance. They differ in how each of these is architected. None positions representational accuracy or behavioral prediction of a specific individual as a design target.

**Table 2.1 — Memory system comparison.** Verified against primary sources.

| Provider | Core architecture | Retrieval method | Memory types | Published recall score |
|---|---|---|---|---|
| **Mem0** | Extract → consolidate → retrieve pipeline; Mem0g graph variant adds a directed labeled knowledge graph alongside the vector store | Hybrid: semantic + keyword + entity | Conversation, session, user, organizational | Current algorithm: 91.6 LOCOMO, 93.4 LongMemEval (vendor-reported; evaluation harness open-sourced at `github.com/mem0ai/memory-benchmarks`). Peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini. |
| **Letta / MemGPT** | LLM-as-operating-system; virtual context management with main context plus external context | Archival via `archival_memory_search`; main-context memory blocks self-edited via `core_memory_append`, `core_memory_replace` | `persona` and `human` blocks in main context; archival and recall memory external | 74.0% on LOCOMO with GPT-4o-mini (Letta blog, 2025-08-12) |
| **Supermemory** | Five-component architecture: chunk-based ingestion, relational versioning, temporal grounding, hybrid search, session-based ingestion | Hybrid with reranking and query rewriting; source chunks injected at retrieval | Contextual memories, relational versions, session data | 81.6% / 84.6% / 85.2% on LongMemEval_s with GPT-4o / GPT-5 / Gemini-3-Pro (self-reported) |
| **Zep** | Built on Graphiti (Apache 2.0, open source). Bi-temporal knowledge graph | Hybrid: semantic + BM25 + graph traversal | Episodes (ground-truth source), Entities, Facts-as-triplets with temporal validity windows | 71.2% on LongMemEval with GPT-4o (Rasmussen et al., arXiv:2501.13956) |

**Mem0** (Chhikara et al., 2025): An extract-consolidate-retrieve pipeline that surfaces memories across four levels (conversation, session, user, organizational). The Mem0g graph variant builds a directed labeled knowledge graph alongside the vector store, with entity extraction and relation inference. Retrieval is hybrid (semantic, keyword, entity lookups). Mem0's peer-reviewable paper reports 68.44 on LOCOMO with GPT-4o-mini for the Mem0g variant. Mem0's current production algorithm, as reported on their research page, scores 91.6 on LOCOMO and 93.4 on LongMemEval; the evaluation methodology is open-sourced at `github.com/mem0ai/memory-benchmarks` for independent reproduction.

**Letta / MemGPT** (Packer et al., 2023, arXiv:2310.08560): An LLM-as-operating-system paradigm. The agent's main context is divided into structured memory blocks (`persona`, `human`) that the agent edits during its inference loop via tools such as `core_memory_append` and `core_memory_replace`. External context includes archival memory (semantically searchable) and recall memory (prior conversation history). The MemGPT paper describes memory edits as autonomous agent actions, triggered by the LLM's own decisions during conversation turns. Of the four memory systems we test, Letta is the only one whose core architecture treats memory as something an agent *synthesizes* during conversation rather than *stores* for later retrieval. Letta's published LOCOMO score is 74.0% with GPT-4o-mini; no LongMemEval score has been published.

**Supermemory:** A five-component architecture per the vendor's published research page: chunk-based ingestion, relational versioning, temporal grounding, hybrid search with reranking and query rewriting, and session-based ingestion. Retrieval returns both high-level memory summaries and original source chunks. Scores on LongMemEval_s (the 500-question subset, not the full suite) are 81.6% with GPT-4o, 84.6% with GPT-5, and 85.2% with Gemini-3-Pro; all self-reported.

**Zep:** A bi-temporal knowledge graph built on Graphiti (Apache 2.0, open source). Ingested data flows through three tiers: episodes as ground-truth source data, entities extracted from episodes, and facts represented as triplets with temporal validity windows tracking when information became true and when it stopped being true. Retrieval is hybrid across semantic, BM25, and graph traversal. In Zep's production deployment, retrieval latency is reported under 200 ms. Zep's arXiv paper reports 71.2% on LongMemEval with GPT-4o (Rasmussen et al., arXiv:2501.13956). An earlier Zep claim of 84% on LOCOMO was publicly disputed by Mem0 in a GitHub issue (see dispute note below).

**A note on benchmark scores in this field.** The recall-benchmark landscape for memory-for-agents is contested. Mem0 and Zep have publicly disputed each other's LOCOMO methodology in a GitHub issue (`getzep/zep-papers#5`), with Mem0 alleging that Zep's 84% claim included adversarial question categories the benchmark specification explicitly excludes, that the evaluation prompt and retrieval templates differed from baselines, and that Zep reported one run where Mem0 reported the mean of ten. Zep contested the correction. The issue was closed with corrected evaluation code provided as a pull request, but the methodological disagreement remains unresolved in the broader community. Supermemory publishes a direct comparison against Zep showing a ~10-point gap on LongMemEval_s in Supermemory's favor. Mem0's current production algorithm claims 91.6 on LOCOMO and 93.4 on LongMemEval with an open-sourced evaluation harness; third-party reproduction efforts (Vectorize.io) have produced a different set of numbers again. In short: benchmark construction for conversational memory is immature, methodology varies significantly between evaluators, and single-number comparisons across vendors should be read with caution. Independent third-party evaluation would help settle this. This paper does not attempt that adjudication. We measure on a different axis (behavioral prediction on held-out situations drawn from public-domain autobiographies), report our own numbers against primary sources, and position the Behavioral Specification as an additive layer regardless of where each memory system lands on recall.

All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did. None of them takes representational accuracy, the property of interest to this paper, as an explicit design target. This is not a criticism of their architectures; it is a different problem. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main study configuration did not exercise (see §4.3 and §4.4.1 and §4.7).

### 2.2 Traceability

**Traceability is not a feature of the Behavioral Specification. It is a necessity.** A system that represents how a person reasons must be auditable by that person, or the representation is a black box they cannot verify. The memory systems we evaluate provide traceability at the fact level. Zep has the strongest explicit provenance of the four: every entity and relationship traces back to the episode IDs that produced it. Supermemory returns source chunks alongside retrieved memories. Mem0 tracks ingestion provenance through timestamps. Letta focuses on agent state rather than audit trails.

Fact-level traceability answers where a retrieved claim came from. That is necessary but not sufficient for a representation of how a person reasons. What is also required is traceability at the reasoning level: why the system believes this about this person, not just which fact it pulled. The Behavioral Specification is structured so that every claim is a piece of reasoning, not just a piece of content. An axiom (for example, "A1: Dual-ledger authority") is an assertion about how the person reasons in a domain, grounded in the facts that imply it (F-001, F-047), which are themselves grounded in the exact source passages that produced those facts. Walking this chain backward shows not only where a belief originated but what line of reasoning connects the source text to the interpretive claim.

This matters because a person should be able to inspect the system's model of them, challenge any step in the reasoning, and correct it if it is wrong. A fact-attribution memory system lets the person audit what the system stores. A reasoning-attribution specification lets the person audit what the system believes. The first is a feature. The second is the minimum bar for a representation that acts on someone's behalf.

### 2.3 Memory and personalization benchmarks

**Existing memory and personalization benchmarks measure recall, persona consistency, preference alignment, or conversational quality. None measures representational accuracy: whether a system's internal model of a specific person accurately captures how that person reasons.** We use behavioral prediction on held-out reasoning situations as the test of representational accuracy, not as a target in its own right. This distinction matters because the closest prior work on prediction benchmarks (Twin-2K) pursues prediction as its target, and the framing in this paper is different (§5.2). Below, we position each existing benchmark against what this paper measures; an extended benchmark-by-benchmark analysis is in Appendix E.

- **LongMemEval** (Wu et al., ICLR 2025, arXiv:2410.10813). Long-term memory across multiple sessions with five capability dimensions: single-session, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. Heavily recall-weighted. Does not test whether the system represents how the person reasons. This paper's battery is orthogonal: every held-out question asks about behavior, not about retrieved content.

- **PersonaGym** (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416). Tests persona fidelity: whether a model maintains a described persona during conversation. Evaluates consistency of persona presentation, not prediction of held-out behavior. A persona-fidelity system can maintain voice without ever accurately predicting decisions, and a representationally-accurate system can change voice while continuing to predict accurately. Our battery measures the second axis.

- **AlpsBench** (Xiao et al., 2026, arXiv:2603.26680). Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses. The evaluation axis is preference-alignment and emotional resonance on conversational responses, not interpretive transfer on held-out behavior; their test and ours share the observation that recall improvement does not carry into these downstream properties, but the downstream properties being measured are different (preference alignment vs. behavioral prediction on unseen situations). Their central finding, that explicit memory mechanisms improve recall but do not inherently guarantee more preference-aligned or emotionally resonant responses, is independently arrived at and complementary to ours: they find the gap in preference alignment, we find it in behavioral prediction. Both results point toward recall-solving being insufficient for what memory is ultimately for.

- **Twin-2K** (Toubia et al., 2025, arXiv:2505.17479). Behavioral prediction at scale: 2,058 participants predicted on held-out survey items using a full-text persona of their own prior survey responses. An earlier exploratory Base Layer run against Twin-2K's battery produced positive results on a different task format from the autobiography-based behavioral battery that grounds the rest of this paper; we do not report those numbers as a formal benchmark comparison here because the experiment used a prior iteration of our pipeline, and the task targets (survey-response interpolation vs. autobiographical behavioral prediction) are substantively different. Structural differences remain the load-bearing point: Twin-2K's persona is a machine-readable transcript of survey responses and scoring is a distance metric on Likert items, while our battery evaluates open-ended behavioral prediction on unseen autobiographical passages with rubric-based LLM-judge scoring. Twin-2K measures whether a model can interpolate a person's survey distribution from other survey responses; our battery measures whether a representation of how a person reasons transfers to novel situations the representation has never seen.

- **LoCoMo** (Maharana et al., ACL 2024, arXiv:2402.17753). Conversational memory quality; the recall benchmark seen in memory-system comparisons throughout §2.1. Does not evaluate behavioral reasoning.

### 2.4 Cognitive and representational foundations

**Six prior research directions shaped how we designed this paper's test.** Each motivates a specific choice about what to measure, what to compare against, or what failure mode to expect.

**Bartlett (1932)** established that human memory is reconstructive and schema-driven rather than literal playback. Reconstruction follows the organizing structures a person has built up over time, not a record of the original event. The Behavioral Specification is computationally analogous: a structured compression meant to carry the signal of a person's reasoning without storing every fact about them. We designed the specification with a schema-like architecture (anchors, core, predictions) precisely so we could test whether it does the work a human schema does: enable accurate anticipation of behavior in situations never encountered in the source data. Our 50/50 train/held-out split is the experimental realization of this question.

**Hinton et al. (2015)** showed that compressing a large neural network into a smaller one preserves "dark knowledge," the relationships between outputs that carry more information than the outputs themselves. This result motivates one of our central experimental comparisons: on matched token budgets, does a compressed interpretive artifact carry more predictive signal than the raw content it was derived from? The Hamerton condition in §4.2 (7,300-token spec vs. 33,000-token training corpus at 2.63 vs. 2.27 on the 5-judge primary panel) is a direct test of that question in the personal-representation setting.

**Chen et al. (2025)** (Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509) extract persona representations as steerable vectors inside model activations, enabling direct monitoring and control of character traits through internal activation surgery. Their approach modifies the model; ours informs the model from outside via context. Both validate that persona is a real, manipulable structure: one reachable through weights, the other through context. We chose the context route because it produces a portable artifact users can own and audit, which activation surgery does not. This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model.

**Jiang et al. (COLM 2025, arXiv:2504.14225)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The paper documents the failure empirically; our reading is that the cause is the gap between having facts and having the interpretive structure to apply them to novel situations. Jiang's paper is the most direct existing evidence for the gap this paper studies, and our test design inherits from it: behavioral prediction on scenarios drawn from held-out text that the model has not seen, with all relevant facts retrievable, measures exactly the interpretive-application gap.

**Jain et al. (2025, arXiv:2509.12517)** find that adding conversation context to LLMs makes them more sycophantic: more likely to agree with the user even when the user is wrong (+45% on Gemini 2.5 Pro) and more likely to adopt the user's perspective on a question. Their result shows that context without the right structure pushes the model toward what the user appears to want rather than toward a grounded answer. This is why our experiment includes a wrong-spec control (§1.3 Mechanism): we hand the model a structured interpretive context that does not match the actual subject. If models drifted purely toward whatever context they are given, the wrong-spec should behave like any other structured prompt. Instead, the model either flags the mismatch explicitly (60.6% of responses) or attempts a low-quality application, neither of which is sycophantic drift. Jain's finding plus our wrong-spec result bracket the question from both sides: context shape matters (Jain), and content matters too (ours).

**Lu et al. (2026, arXiv:2601.10387)** identify what they call the Assistant Axis: a dominant internal direction that anchors assistant models' default behavior toward generic helpfulness and harmlessness. This default operates even when no specific user is involved. The Behavioral Specification can be read as an external override to the Assistant Axis on a per-user basis: a structured anchor that shifts the model from "generic helpful assistant" toward "reasons as this specific person would reason." This framing motivated our choice to measure hedging as a primary outcome alongside accuracy: if the spec shifts the model off the generic Assistant Axis, the behavioral change should show up both in what the model predicts and in what it is willing to commit to. Our hedging-reduction finding (§1.3 Mechanism, §5.5) is consistent with this reading: the generic Assistant Axis produces hedging as a safe default, while a specific interpretive anchor enables commitment. The inference that hedging is downstream of the Assistant Axis is ours; Lu et al. identify the axis and leave the specific behavioral manifestations open.

### 2.5 LLM-as-judge

**LLM-as-judge evaluation is an established methodology with known biases.** Zheng et al. (NeurIPS 2023 Datasets and Benchmarks Track, arXiv:2306.05685) demonstrated that LLM judges agree with human judges at rates comparable to inter-human agreement (over 80% on the MT-Bench and Chatbot Arena benchmarks), establishing the approach as viable for tasks that would otherwise require expensive human annotation. This paper extends their work by calibrating each judge in our judge panel for three specific biases: ceiling behavior (what score each judge assigns to verbatim matches), paraphrase sensitivity (how each judge handles semantically equivalent but differently-worded responses), and length bias (whether each judge rewards or penalizes longer responses). The two Gemini judges systematically inflate scores by approximately one point relative to the other five, so we report the five non-Gemini judges as the primary aggregate and the full seven-judge panel as a sensitivity check. Full calibration methodology is in §3.7.

## 3. Study Design

The experimental strategy holds the response model constant and varies the representation served as its context. Every condition in the study is a different choice about what that context contains: nothing (pretraining only), retrieved facts, raw corpus, a specification, or combinations of those. This isolates the contribution of the representation itself from model capability, provider, or fine-tuning regime. Each measurement choice ties back to a specific number reported in §4, and the statistical commitments were pre-locked before final analysis.

The section has two intertwined but separable halves. §3.1 through §3.2.1 and §3.4 through §3.7 describe the experimental apparatus: the property being measured, the subjects, the question batteries, the conditions, the response models, and the evaluation protocol. §3.3 describes the pipeline that produces the Behavioral Specification itself. The pipeline is what makes the representation possible; the apparatus is how we test whether the representation changes how an AI acts on behalf of a specific person. Both halves are needed to answer the study's core question about human-AI interaction, and neither is informative without the other.

### 3.1 Representational Accuracy

**We use the term representational accuracy to describe how faithfully a model can act in line with a specific person when given a representation of that person.** The property is a joint claim: first, that the person has behavioral patterns consistent enough to be captured in a representation; second, that the representation actually carries that signal; and third, that a model given the representation can act on it. All three matter. Prediction on held-out situations is how we test all three at once.

The test works like this: held-out passages from a person's own writing serve as samples of situations the model has not seen. If the person's behavior is consistent enough to be captured and the representation actually captures it, the model should anticipate how the person would respond in those held-out cases. When it does not, one of three things is failing: the behavioral patterns are not consistent, the representation is wrong, or the model is not using the representation well. Each failure mode is informative.

We do not claim to modify the model's internal parameters. The Behavioral Specification is served as context: a lens through which the model can reason about a specific person. What we measure is whether that external lens is accurate enough to guide the model's responses in the same way the person would guide them.

In practice, representational accuracy is operationalized as the mean predicted-behavior score (1-5 scale) across a standardized battery of 39 behavioral prediction questions, averaged across the five primary judges from two providers (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). Two Gemini judges (2.5 Flash and 2.5 Pro) are reported as a sensitivity check. The rubric is in §3.7. A guide to interpreting fractional scores at different ranges of the scale (what 2.9 vs. 3.2 indicates, what 1.5 vs. 2.0 indicates) is also in §3.7.

### 3.2 Subjects

We test 14 subjects, all historical figures with public-domain autobiographies or memoirs. Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting on any single type of source material. All source corpora are English or English-translated and are available on Project Gutenberg or comparable public-domain archives. Because frontier language models train on large public-text corpora, some level of pretraining exposure to each subject's writing is likely.

| # | Subject | Source | Words | Period |
|---|---|---|---|---|
| 1 | Philip Gilbert Hamerton | Project Gutenberg #8536 | 25,231 | 1834–1858 |
| 2 | Elizabeth Keckley | Project Gutenberg #24968 | 58,742 | 1818–1868 |
| 3 | Sunity Devee | Project Gutenberg #57175 | 67,379 | 1864–1932 |
| 4 | Zitkala-Sa | Project Gutenberg #10376 | 35,328 | 1876–1938 |
| 5 | Olaudah Equiano | Project Gutenberg #15399 | 85,660 | 1745–1797 |
| 6 | Mary Seacole | Project Gutenberg #23031 | 62,467 | 1805–1881 |
| 7 | Fukuzawa Yukichi | Internet Archive | 139,088 | 1835–1901 |
| 8 | Babur | Project Gutenberg #44608 | 422,772 | 1483–1530 |
| 9 | Yung Wing | Project Gutenberg #54635 | 66,459 | 1828–1912 |
| 10 | Benvenuto Cellini | Project Gutenberg #4028 | 190,390 | 1500–1571 |
| 11 | Bernal Diaz del Castillo | Project Gutenberg #32474 | 187,315 | 1492–1584 |
| 12 | Georg Ebers | Project Gutenberg #5599 | 96,174 | 1837–1898 |
| 13 | Jean-Jacques Rousseau | Project Gutenberg #3913 | 278,120 | 1712–1778 |
| 14 | Saint Augustine | Project Gutenberg #3296 | 114,873 | 354–430 |

**Franklin as a known-figure control.** Benjamin Franklin (Project Gutenberg #20203) is included as a known-figure reference point. Franklin's *Autobiography* is one of the most widely available and frequently cited autobiographies in American public-domain literature, and the model's baseline score on Franklin (3.77 on the 5-judge primary panel) is consistent with substantial pretraining representation of both the person and the specific text. We use Franklin as a reference point for what the high-baseline end of the spectrum looks like (§4.7), not as a subject whose representation is a design target of the specification itself.

**The baseline as an observable proxy.** The baseline score (C5, no-context prediction accuracy, §3.7) is a direct empirical measurement: the response model's ability to predict behavior on a specific subject with no external help. We treat that measurement as the observable proxy for the model's pretraining representation of the person. A baseline near 1.0 indicates the model has little to work from. A baseline above 3.0 indicates substantial pretraining representation. The 14 main-study baselines range from 1.03 (Sunity Devee) to 2.93 (Equiano); Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone, higher on the Gemini-inclusive 7-judge aggregate).

The baseline spread across the 14 subjects is direct empirical evidence that current response models hold uneven internal representations of specific people. The questions of which specific texts produced any subject's baseline, how the model organizes the representation internally, or what besides pretraining might influence the spread are outside this study's design. What the specification adds on top of the baseline is the question §4 tests.

**What we did not control for.** Language (all source corpora are English-language or English-translated); cultural framing (Western canon predominates in public-domain digitization); subject selection bias from Project Gutenberg's own curation history; era (oldest subject 4th-5th century, newest early 20th century); individual preferences in autobiographical self-presentation. These are acknowledged constraints on the generalizability of the 14-subject sample, not corrected biases.

### 3.2.1 Pretraining-coverage variance

Before turning to the specification's effect, the baseline itself is worth flagging as a finding. Response models vary widely in their pretrained capacity on a given person, even across a sample of subjects who all have public-domain autobiographies of comparable provenance.

| Baseline band | Subjects | Count |
|---|---|---|
| ≤ 2.0 (low-baseline slice) | Sunity Devee, Ebers, Hamerton, Fukuzawa, Seacole, Bernal Diaz, Keckley, Yung Wing, Babur | 9 |
| 2.0–3.0 (mid-baseline) | Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano | 5 |
| > 3.0 (high-baseline) | Franklin (known-figure control, not in main study) | 1 |

Nine of fourteen main-study subjects fall below 2.0, the "population of relevance" band closest to real living users whose private reasoning is not in any training corpus. Five subjects sit in the 2.0–3.0 band where the specification's effect is weaker and less consistent; two of them (Zitkala-Sa and Equiano) show small negative deltas (see §4.1 Table 4.1 and §4.6). Franklin at 3.77 (5-judge primary) anchors the high-baseline end and is a control, not a main-study subject.

This distribution matters for reading §4's results: the variance is not flat, and the specification's effect depends on where a subject sits on this distribution. Interpretive implications are developed in §4.1.

### 3.3 Pipeline

**The pipeline transforms raw source text into a Behavioral Specification in four content-production steps: extract, embed, author, and compose. An import step canonicalizes the source data before extraction.** Each step is a single script backed by a single model choice. Total cost per subject is under $1.

| Step | Input | Tool / model | Output |
|---|---|---|---|
| 1. Import | ChatGPT / Claude exports, journals, plain text, directories | `import_conversations.py` | SQLite canonical store |
| 2. Extract | Canonical source text | `extract_facts.py`, Claude Haiku 4.5, 46-predicate vocabulary | Structured behavioral triples with ADD / UPDATE / DELETE / NOOP operations |
| 3. Embed | Extracted facts | `embed.py`, `all-MiniLM-L6-v2`, ChromaDB | Vector index for provenance tracing and retrieval |
| 4. Author | Extracted facts + embeddings | `author_layers.py`, Claude Sonnet 4.6 | Three interpretive layers as markdown (anchors, core, predictions). Each layer is produced from facts alone, not from prior layer output. Each layer prompt includes a domain guard that prevents topic skew (ablation-validated in prior pilot work). |
| 5. Compose | The three authored layers | `agent_pipeline.py`, Claude Opus 4.6 | Unified behavioral brief in flowing prose |

The artifact served as context in experimental conditions (referred to throughout the paper as "the Behavioral Specification") is the three authored layers concatenated with the composed brief, not the brief alone. Total size per subject is approximately 5,000-8,000 tokens.

The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: `avoids`, `repeatedly engages in`, `refuses to`, `values`, `fears`, `has experienced`). The full predicate list is in the appendix. The vocabulary is human-curated and was validated across 50+ pilot subjects before being frozen for the study. The constrained vocabulary is the main lever the pipeline uses to push extraction away from biographical facts ("his father was violent") and toward behavioral patterns ("evaluates authority figures on dual criteria of virtue and failure").

The three authored layers have distinct jobs. Each layer has a characteristic format; examples below are drawn from the Hamerton specification.

**Anchors** encode the subject's load-bearing axioms in numbered form (A1, A2, ...), each with an activation condition and a false-positive warning. Example:

> *A1. DUAL-LEDGER AUTHORITY: Evaluates authority figures on virtue and failure simultaneously, refusing to collapse them into a single verdict. Active when: encountering teachers, mentors, or institutional power. False positive: do not apply when the authority figure is a peer or subordinate.*

**Core** captures values, beliefs, and self-view in flowing prose. It is the layer that reads most like an essay about the person. Example:

> *Treats aesthetic sensibility and moral seriousness as inseparable. The quality of attention a person brings to beauty is, for him, direct evidence of the quality of attention they bring to anything else. This belief predates his career in art criticism and survives intact across every phase of his life.*

**Predictions** are explicit behavioral predicates (P1, P2, ...) with detection criteria, directives, and false-positive warnings. Example:

> *P3. Environment-as-cognition. Classifies new environments as generative or hostile to contemplative work before engaging with their particulars. Detection: immediate evaluative language about the environment itself, not about the people or tasks in it. Directive: model an immediate and durable classification rather than gradual adjustment. False positive: do not apply when the environment is a neutral logistical setting.*

The compose step integrates these three layers into a unified prose brief. The served specification is the compose-step brief concatenated with the three layer files.

Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80).

### 3.4 Question Batteries

**Each subject's behavioral prediction battery is generated by a backward-design process: an LLM reads a passage from the held-out half of the corpus, writes a question whose answer is the behavioral pattern implicit in the passage, and deliberately avoids naming any detail unique to the passage itself. The question can be attempted from training-text patterns alone; the verbatim held-out passage is the ground truth for scoring.**

The procedure, in order:

1. **Split the corpus.** Each subject's source text is divided by chapter into `training.txt` (50% of the corpus) and `heldout.txt` (50%). Held-out text is never shown to a response model.
2. **Sample from held-out.** A sliding window moves across the held-out text in four batches of ten questions each, using 5,000-character windows as local context.
3. **Backward-design question generation.** Claude Haiku 4.5 (temperature 0) reads each held-out window and writes a question whose answer requires the subject's behavioral patterns observable in the training half. The prompt extracts a verbatim ground-truth span from the held-out window and forbids named-entity or specific-date leakage in the question stem.
4. **Supplementary tiers.** Four additional question categories (factual, situational, and others) are generated from training text alone and included in the battery but not scored in the main results.
5. **Dedup and freeze.** Deduplication on lowercased question text, cap at target counts per category, MD5 checksum of the final battery. Downstream response and judgment files are invalidated if the battery checksum changes.

Each main-study subject receives 39 behavioral prediction questions; Franklin's legacy battery has 40. The total behavioral-prediction pool is 586 questions across 15 subjects (14 main-study plus Franklin). Each battery covers 8 to 10 of the 10 fixed behavioral-prediction categories. A per-subject count and category-distribution table is in the appendix.

**Leakage audit.** We empirically checked the backward-design no-leakage principle by searching every behavioral-prediction question for any sequence of seven or more consecutive words that appears verbatim in that subject's held-out corpus. Result: 2 of 586 questions leak (0.34% aggregate). The 14 main-study subjects leak-check at 0.00%. Both leaks are in the Franklin control battery (Q49, Q56), which predates the backward-design constraint and was hand-authored. We disclose them here; Franklin's role in the paper is as a high-baseline reference, not as a subject whose quantitative result is load-bearing.

Raw battery data is available in the public repository at `results/global_<subject>/battery_v2.json` for the 13 global subjects; Hamerton and Franklin legacy batteries at `data/<subject>/battery.json`. GPT-5.4-regenerated batteries (used in the circularity control, §3.4.1) are at `results/global_<subject>/battery_gpt54.json`. The leakage-audit script is at `scripts/_verify_battery_leakage.py`.

### 3.4.1 Circularity Controls

**The pipeline and the batteries both use Anthropic models for multiple roles: Haiku for extraction and battery generation, Sonnet for authoring, Opus for composition, Haiku as the primary response model, and both Sonnet and Opus on the judge panel. To test whether results are an artifact of this within-Anthropic frontier-model chain, we ran two independent circularity controls.**

**Control 1: Independent battery regeneration (GPT-5.4).** We independently regenerated behavioral prediction batteries for all 13 global subjects using GPT-5.4 with the identical backward-design prompt used for the primary Haiku-generated batteries. The regenerated batteries produced the same 39-question count per subject, covered the same 10 behavioral categories (with 8-10 shared per subject), and targeted the same behavioral patterns in the source text. Emphasis differed by category: GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions. The backward-design methodology constrains the output more than the generating model does. Franklin and Hamerton retain their legacy batteries and are not part of Control 1; the 13 global subjects are. Full GPT-5.4 batteries are released for independent replication.

**Control 2: Non-Anthropic response chain.** We re-ran the core C5 / C2a / C4a / C2c conditions on three subjects spanning the effect gradient (Ebers at baseline 1.04 with a strong positive effect, Yung Wing at baseline 1.88 with a modest positive effect, and Zitkala-Sa at baseline 2.34 with a negative effect) using two non-Haiku response models (Claude Sonnet and Google Gemini Pro) reading the GPT-5.4-generated batteries. The combination gives us subject × response-model × battery cells that together test whether the specification effect survives when both the response model and the battery-generation model are outside the Anthropic family. Full results are in §4.8.

Together the two controls address within-Anthropic circularity at two levels. Control 1 holds the response model constant and varies the battery-generation model, testing whether the specification effect depends on Haiku writing the test questions. Control 2 holds the battery constant and varies the response model, testing whether the effect depends on Haiku reading and answering them.

A broader LLM-as-judge circularity, the concern that any LLM panel might systematically favor LLM-produced outputs over human-written alternatives, is not addressed by these controls. It is discussed as an open limitation in §6.

Raw battery regeneration data is at `results/global_<subject>/battery_gpt54.json` for all 13 global subjects. Tier 2 response and judgment files for the three subjects tested are in the same per-subject directories.

### 3.5 Experimental Conditions

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

**Letta stateful-agent path.** Letta exposes two memory modes: archival retrieval (the path tested in C1 / C3 above) and a stateful-agent path where memory blocks are edited incrementally during ingestion and the agent reads from the block directly. The stateful path is architecturally distinct from retrieval-style access and is evaluated as a separate comparison, reported in §4.4.1 and §4.7 alongside other Letta findings rather than as a top-line condition row.

**Wrong-spec control.** C2c uses random derangement: each subject is assigned another study subject's specification, with a fixed seed (42) ensuring no subject receives its own spec. The derangement eliminates overlap between the wrong spec's target and the true subject. A prior iteration using Franklin's specification for all subjects was run but is not reported in the main results, because Franklin is a known high-pretraining figure whose specification may sit closer to canonical Western profiles than a random study subject's specification would. The derangement control is the stricter test and is the one reported.

Detailed per-condition parameters, exclusion cases, and ingestion specifics are in Appendix C.

Raw data is available in the public repository at `results/global_<subject>/results_v2.json` (all direct-context conditions for the 13 global subjects) and `results/global_<subject>/<system>_results.json` / `<system>_fullpipeline_results.json` for per-system controlled / native configurations (`<system>` ∈ {mem0, letta, supermemory, zep, baselayer}). Hamerton responses live at `results/hamerton/` and Franklin at `results/franklin/` with per-judge judgments at `results/franklin_legacy_20260411/analysis/`.

### 3.6 Response Models

**The primary response model is Claude Haiku 4.5, run across all 14 subjects and every condition in the main matrix. Haiku was chosen as primary because it is the weakest model in the available test pool; an effect that registers on a weaker model is a more conservative claim than one that only surfaces on a frontier model.**

**Tier 2 response-model expansion.** To test whether the specification effect depends on the response model being within the Anthropic family, Claude Sonnet 4.6 and Google Gemini 2.5 Pro were additionally run as response models on 3 subjects spanning the effect gradient (Ebers, Yung Wing, Zitkala-Sa) against the GPT-5.4-regenerated batteries from Control 1. Tier 2 results and subject-selection rationale are in §3.4.1 and §4.8.

**Call-time parameters.** All response models are called with `temperature=0` and `max_tokens=1024`.

**Prompt schema.** A single shared prompt is used across every condition. The system message frames the task as behavioral prediction of a specific person; the user message is the question plus whichever context inputs the condition specifies (§3.5). Nothing about the prompt changes per condition beyond the injected context block.

```
System: You are predicting how <subject> would respond to a specific
        question about their behavior, values, or reasoning. Answer
        in <subject>'s voice, grounded in their demonstrated patterns.

User:   <context block — empty (C5), spec (C2a), wrong spec (C2c),
         facts (C4), facts + spec (C4a), corpus (C8), corpus + spec
         (C9), or retrieval ± spec (C1 / C3)>

        Question: <question text>
```

No prompt instruction tells the model to abstain, answer, hedge, or commit. That was a design decision made at the start of the study. Any prompt that coached response behavior would have directly confounded what the conditions are trying to measure, and the model's natural refusal-or-commitment pattern given a specific context is itself part of the phenomenon the study tests. §4.3 reports the hedging-rate shift across conditions and treats it as a substantive finding rather than a behavior to suppress.

Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in Appendix C. The same information is present in the released code at `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, and `scripts/run_multimodel_responses.py`.

Raw response files are in the public repository at `results/global_<subject>/results_v2.json` for the 13 global subjects, `results/hamerton/results.json` and `results/franklin/fullstack_haiku.json` for the legacy subjects, and `results/_tier2/` for the Tier 2 runs.

### 3.7 Evaluation: LLM-as-Judge with Calibration

**Every response is scored 1-5 by seven LLM judges against the verbatim held-out ground-truth passage. Human annotation at this scale is feasible: roughly 14 subjects × 40 questions × 15+ conditions sits on the order of thousands of judgments, within reach of a small annotation team. It was not done here. This is a limited-budget solo research effort, and the deliberate trade-off was to run more conditions and more judges rather than fewer conditions with human annotation. That trade-off is the central evaluation limitation of the study; how we work inside it is what this section describes.**

**The evaluation is deliberately recursive.** Response models are evaluated by judges (§3.7.1). Judges are evaluated by calibration diagnostics (§3.7.2), inter-judge agreement metrics (§3.7.4), and post-hoc rubric-handling audits (§3.7.6). No single layer is treated as ground truth; each layer's behavior is itself measured and disclosed, and where a layer's behavior diverges from what the rubric intends, the divergence is flagged rather than corrected silently. The paper's rigor in the absence of human annotation comes from this stacked-instrument structure, not from trusting any one step.

**Scoring rubric.**

| Score | Meaning | Example (Hamerton: "How would he engage an unfamiliar industrial landscape?") |
|---|---|---|
| 1 | Refusal or irrelevant | "I don't have enough information to predict how Hamerton would respond." |
| 2 | Generic, not subject-specific | "He would probably dislike it, as most nineteenth-century artists preferred natural settings." |
| 3 | Partially captures the subject's behavioral pattern | "He would view the landscape aesthetically and evaluate it before engaging with its people." |
| 4 | Substantively captures the pattern on multiple dimensions | "He would render an immediate evaluative verdict on whether the environment is generative or hostile to contemplative work, before attending to the specific people in it." |
| 5 | Captures the behavioral pattern observable in the verbatim ground-truth passage | "He would classify the environment as cognition-disrupting within the first encounter, treat the classification as durable rather than provisional, and evaluate its people only secondarily to the environmental verdict." |

*(Examples are illustrative; full per-subject score distributions with verbatim responses are in Appendix D.)*

*(Condition identifiers such as C5, C2a, C4a, and C3 refer to the conditions defined in §3.5 and summarized in Appendix C. Rubric anchor numbers 1 through 5 refer to the rubric table above.)*

**What a 5 means and does not mean.** A score of 5 reflects alignment with one specific behavioral sample: the held-out ground-truth passage the question is drawn from. It is not a claim that the response fully represents the subject in some absolute sense, and it is not a claim that the same response would score 5 on a different held-out passage from the same subject. Each question tests one behavioral sample at a time; the aggregate across roughly 40 questions per subject is what the paper reads as the subject-level score.

**Reading score differences.** A move from 2 to 3 is the difference between "he would probably dislike it, as most artists would" and "he would judge the landscape aesthetically before deciding whether to engage its people." The first answer is pattern-free and could apply to many nineteenth-century subjects; the second identifies a subject-specific behavioral tendency visible in Hamerton's actual writing. A move from 3 to 4 is the difference between identifying one behavioral tendency and identifying several that work together. §3.7.3 develops the formal cross-anchor rule used throughout the results section.

### 3.7.1 Judge Panel

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

### 3.7.2 Calibration

Five judges (Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) were tested against four diagnostic inputs with known correct scores before study scoring began. Sonnet and Opus are not on the diagnostic suite; they enter the panel on inter-judge agreement properties only.

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

**Primary aggregate: 5-judge (non-Gemini) panel.** The primary numeric aggregate reported throughout §4 is the 5-judge mean using Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, and GPT-5.4. The two Gemini judges (Gemini 2.5 Flash, Gemini 2.5 Pro) are excluded from the primary aggregate and reported as a sensitivity check instead.

The reasoning. The calibration table above shows Gemini Pro failing the verbatim-match diagnostic (4.15 where every other calibrated judge scores 5.00) and penalizing padded-correct responses severely (dropping from 5.00 on short correct to 1.20 on long correct). Gemini Flash shows smaller but consistent length sensitivity. A judge that cannot recognize verbatim ground-truth as a 5 is a known-unreliable instrument on this task. Including known-unreliable judges in the primary aggregate inflates or deflates effect-size numbers in ways that do not reflect the underlying response quality. Excluding them from the lead number, while keeping them available as a sensitivity check, preserves the provider-diversity argument (the final conclusions are stable whether or not the Gemini judges are included) without leading with a known-flawed aggregate.

The 7-judge aggregate is reported as a sensitivity check. Where the 7-judge and 5-judge aggregates produce materially different numbers, both are given and the delta is discussed. Every primary finding in §4 is stable across both aggregates (robustness confirmed in §4.5).

**The 5-judge primary is the conservative choice.** On the main gradient and spec-effect conditions, including the two Gemini judges produces *larger* spec-effect deltas, not smaller ones: on the 13 global subjects, C2a's mean Δ vs. C5 rises from +0.35 on the 5-judge primary panel to +0.45 on the 7-judge aggregate, a +0.10-point widening driven by Gemini inflation compressing baseline scores more than spec-condition scores. The same direction holds across wrong-spec, facts-only, and facts-plus-spec aggregates. Reporting 5-judge primary means every headline effect size is the lower bound that remains once the most-inflationary judges are removed from the aggregate.

**Framework for reading raw scores.** A raw score on the 1-5 scale is a judge's estimate of how closely a response captures the behavioral pattern observable in the held-out ground-truth passage (rubric in §3.7, anchor-crossing interpretation in §3.7.3). Raw scores are read through three rules:

1. **Directional, not absolute.** Raw scores are treated as a directional signal about whether a condition's context is steering the response toward the subject's documented patterns, not as an objective measurement of response quality.
2. **Deltas carry more information than levels.** A raw score of 2.87 in isolation is not a meaningful claim about "what the model did." The claim is in the delta between conditions: C2a (spec only) at 2.47 compared to C5 (baseline, no context) at 1.04 says something because of the comparison, not because 2.47 is inherently a meaningful number.
3. **Anchor crossings gate the strength of the claim.** A delta that crosses a rubric integer anchor (§3.7.3) is treated as a stronger claim than a delta that stays inside a single integer band. This is applied consistently throughout §4.

Every numeric result in §4 is reported through this framework. Any reader who prefers a different interpretive lens can apply it to the published raw scores directly. Raw calibration data is in the public repository at `results/judge_calibration/`.

### 3.7.3 Fractional Score Interpretation

Mean-across-judges aggregation produces fractional scores (2.87, 3.12, 2.34). Fractional shifts should be read through the integer anchors in the rubric, because each anchor corresponds to a categorical shift in response quality.

**Cross-anchor interpretation rule.** A fractional delta that crosses an integer anchor reflects a real shift in the underlying response distribution. A delta that stays inside a single integer band is a within-category shift and a weaker claim.

| Boundary crossed | Qualitative shift |
|---|---|
| 1 / 2 | The model moves from "I don't have enough to say" to an actual answer, even if generic. |
| 2 / 3 | The answer becomes specifically about this subject rather than a generic stand-in. |
| 3 / 4 | Multiple behavioral dimensions of the subject appear together in the same answer. |
| 4 / 5 | The response closely matches the behavioral pattern in the held-out passage. |

**Examples from the data.**

- Ebers C5 (baseline, no context) at 1.04 → C2a (spec only) at 2.47: crosses the 1 / 2 anchor (refusal → engagement). Refusal responses in C5 turn into actual engagement in C2a, and some responses climb into subject-specific territory. Category change.
- Hamerton C5 (baseline) at 1.41 → C4a (facts + spec) at 2.97: crosses the 2 / 3 anchor (generic → subject-specific). Generic art-historical stereotypes in C5 become responses grounded in Hamerton's documented patterns. Category change.
- Supermemory C3 (retrieval + spec) vs. C1 (retrieval only) on low-baseline subjects: +0.004 mean delta. Most per-subject deltas stay inside the same integer band. Within-category shifts; the aggregate is accurately small.

**The paper applies this rule consistently.** Score deltas reported in §4 are read through this lens. A +0.50 delta that crosses a rubric anchor is treated as a stronger claim than a +0.50 delta that does not, and the difference is called out where it matters. Full per-subject anchor-crossing data is at `docs/research/s114_anchor_crossing_examples.json`; the computing script is `scripts/compute_anchor_crossing.py`.

### 3.7.4 Inter-Judge Agreement

**The specification-effect claim.** Before discussing agreement, the claim the agreement measures support needs to be stated plainly. The specification effect is not a claim that the model has gained a new behavioral-prediction capability. It is the claim that when a Behavioral Specification is served as context, the model's responses shift in the direction of the subject's demonstrated behavioral patterns, and that shift is detectable against held-out passages from the same subject. What the judges measure is whether that shift has happened. The judge panel is used to detect steering, not to determine truth.

With the claim stated, two complementary measures answer different questions. The first measures whether judges agree on direction; the second measures whether they agree on absolute magnitude.

**Do the judges agree on direction?** Pairwise Spearman ρ = **0.89 to 0.98** across all 21 judge pairs. This is high rank agreement. It means that across the seven judges, the ranking of conditions ("C4a scored higher than C2a scored higher than C5") is consistent. Whatever quirks any individual judge has in absolute calibration, they agree on which conditions produce better responses. For a directional claim (is the specification steering responses in the right direction?), this is the statistic that matters.

**Do the judges agree on absolute magnitude?** Krippendorff α (ordinal) = **0.659 across the 5-judge primary panel** (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4); **0.535 across the 7-judge panel including Gemini Flash and Gemini Pro**. "Absolute magnitude" is the stricter question: when one judge gives a response a score of 3.5, does a different judge give the same response a score close to 3.5? Not "do they agree one response is better than another" (direction), but "do they agree on the actual numeric score" (magnitude). On the Krippendorff scale, α = 1.0 is perfect absolute agreement, α ≈ 0.0 is agreement no better than chance, and α < 0 is systematic disagreement. Krippendorff's own guidance cites α ≥ 0.8 as high reliability and α ≥ 0.667 as substantial or tentative reliability. The primary 5-judge α = 0.659 sits just below the 0.667 threshold. The drop to 0.535 when the two Gemini judges are included is the systematic +1-point Gemini inflation showing up in the statistic: Gemini judges score responses about one point higher on average than the five primary judges, so the absolute values disagree even when the rankings match. This is exactly the pattern that motivated making the 5-judge panel primary (§3.7.2).

**What this means for how results should be read.** The specification-effect claim is a directional claim. The Spearman ρ = 0.89-0.98 agreement answers it: seven judges across three providers converge on the direction of the effect. The Krippendorff α value places a ceiling on how precisely any individual fractional score should be read, which is why the paper treats per-subject deltas that stay inside a single rubric band as weaker than deltas that cross one.

**What the panel is not.** The panel is not an empirical determination that the higher-scoring responses are in absolute terms "the correct response" for the subject. That determination requires human annotation against the subject's actual writing, which we do not have. What the panel provides is cross-provider directional convergence: three independent providers' models agree that the specification is moving responses along the scale in the same direction. We treat that as sufficient evidence for a directional claim about the specification's effect, and no stronger than that.

Raw agreement matrices are at `results/interjudge_agreement/`.

### 3.7.5 Aggregation

Locked aggregation rule:

1. Within each judge, mean score across all questions for each (subject, condition) cell.
2. Mean across the five primary judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). A separate 7-judge mean including Gemini Flash and Gemini Pro is computed and reported as a sensitivity check.
3. Unit of inference: subject.

Mean was chosen over median and trimmed mean. Median discards information when judges cluster tightly, which the Spearman ρ = 0.89-0.98 agreement shows they do. Trimmed mean requires an arbitrary trim threshold. Simple mean preserves every judge's contribution, and the Gemini inflation is handled by the primary-vs-sensitivity split rather than by silent correction.

### 3.7.6 Rubric-handling limitations (validity audit)

A direct inspection of the response text against the 5-judge primary scores surfaced two rubric-handling limitations that any reader of the §4 numbers should keep in mind. Both were identified by a post-hoc audit (`scripts/audit_low_end_inflation.py`, full report in Appendix D).

**Abstention is not cleanly distinguished from wrong prediction.** The rubric's lowest anchor, "refuses or off-base," lumps together two different behaviors: honest refusal to predict when the context does not support a prediction, and a substantively wrong prediction. Across 192 responses that match abstention patterns (phrases like "no specific information," "I cannot confirm," "would need additional context") in the low-baseline slice, 82.8% scored in the 1.0-1.5 band as expected, but 9.4% scored at or above 2.0 and 3.2% scored at or above 3.0. The mean abstention score is 1.27. Judges give partial credit for abstentions that include adjacent-fact recitation or correctly identify what the provided context does not contain, treating honest refusal as a rubric-2 or rubric-3 response rather than rubric-1. The effect is bidirectional: honest abstention can be over-credited (our Example C in §4.1, Seacole Q2 at 2.80) and substantive prediction under the influence of a specification's honesty axioms can also be over-credited when the model flags its own epistemic limits (Hamerton Q21 at 4.00 under spec-induced abstention).

**Length correlates with score in the baseline condition only.** Across 1,599 low-baseline responses, response length correlates with 5-judge primary score at r = 0.26. When decomposed by condition, the correlation is driven entirely by the no-context baseline (C5) at r = 0.604. Spec-containing conditions show near-zero correlation (C2a r = 0.14, C4 r = 0.01, C4a r = −0.01). Ultra-high responses (score ≥ 4.5) are not longer than mid-range responses on average (2,790 chars vs. 2,829 chars), so length inflation is not a general phenomenon across the rubric. The specific pattern is: **verbose baseline responses (which tend to include more hedging, adjacent-fact recitation, and disambiguation offers) are scored more generously than short baseline refusals.** The practical implication is that measured baseline scores likely slightly overestimate the no-context prediction accuracy. The spec-effect gap is probably larger than reported, not smaller.

**Per-judge strictness on abstentions.** Sonnet is the strictest judge on abstention responses (mean 1.14), followed by GPT-5.4 (1.17), Haiku (1.29), and GPT-4o (1.34). Opus is the most lenient at 1.41, roughly 0.27 points above the strictest judge. This cross-judge variation is small in absolute terms but is worth naming: no single judge is universally strictest, and the 5-judge primary average smooths these differences without eliminating them.

**What this means for the reported effects.** Both limitations tighten the paper's claims rather than weakening them. Abstention over-credit pulls the measured C5 baseline *up*, which shrinks the apparent spec-vs-baseline gap. Length-driven baseline inflation does the same. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift we report; we elect to report the measured number and flag the direction of the bias rather than recompute under a modified rubric, to keep the analysis plan lock intact. §8 Future Work proposes a differentiated rubric that scores abstention as its own dimension and a length-controlled scoring protocol.

### LLM-as-judge disclosure

No humans are in the evaluation loop. Prior independent work (Zheng et al. 2023 and the multi-judge panel literature that followed) has shown that LLM-as-judge panels correlate with human judges on comparable tasks at rates approaching human-human agreement, which is what legitimizes the panel we use here. But "approaches human agreement on comparable tasks" is not the same as "is empirically determining the objective quality of a behavioral prediction response," and the difference matters. The question the panel can answer is directional: is the specification moving representational accuracy in the right direction? For that question, the 5-judge primary panel (backstopped by the 7-judge sensitivity check) is sufficient as a first pass, and the Spearman ρ value and cross-provider convergence back the claim. For determining the absolute quality of any individual response, or for settling whether any specific numeric value is the "right" score, human annotation is required. A stratified human-validation subset is the leading follow-up work in §8 Future Work.

Raw per-judge judgments are in the public repository at `results/global_<subject>/*_judgments_<judge>.json` (and `judgments_v2.json` for the merged v2 set) for the 13 global subjects, `results/hamerton/*_judgments_<judge>.json` for Hamerton and `results/franklin/*_judgments.json` plus `results/franklin_legacy_20260411/analysis/*_judgments.json` for Franklin. Memory-system per-judge judgments live at `results/global_<subject>/<system>_judgments_<judge>.json` (controlled) and `results/global_<subject>/<system>_fullpipeline_judgments_<judge>.json` (native) in the same flat per-subject directory.

---

## 4. Results

This section reports the Behavioral Specification's effect on behavioral prediction across eight parts:

- **§4.1 — The Cross-Subject Gradient.** The primary result, across 14 subjects.
- **§4.2 — Compression: Structure vs. Raw Text.** Is the effect about structure or about information volume?
- **§4.3 — Mechanism: Content, Not Format.** Does the content of the correct specification drive the effect, or does any structured prompt?
- **§4.4 — Memory-System Composition.** Does the specification layer on top of existing commercial memory systems?
- **§4.5 — Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?
- **§4.6 — Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level?
- **§4.7 — Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution.
- **§4.8 — Scaling and Practical Implications.** Cost, context, and deployment considerations.

Every number in §4 uses the 5-judge primary aggregate defined in §3.7.2 (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-judge sensitivity check (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported in §4.5. Score deltas are read through the anchor-crossing rule from §3.7.3: a delta that crosses a rubric integer anchor is a stronger claim than one that stays inside a single anchor band.

### 4.1 The Cross-Subject Gradient

**Hypotheses tested in this section** (from §1.2): H1. Adding the specification improves prediction. H2. The effect is inversely proportional to the response model's pretraining coverage. H2a (corollary, introduced here). On high-baseline subjects, the specification does not add value and mildly interferes.

---

**Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it.** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.2.1), every one of the 9 improves when the specification is added to the full fact set. None declines. Mean score lift: **+0.89 points**.

The mean number hides what is happening at the response level. **Of the 351 individual responses in the low-baseline slice, 55.0% crossed at least one rubric integer anchor upward when the specification was added.** The AI's answer moved from one category of response to a qualitatively different category.

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

**Three representative examples below show the different ways the specification can help.** These are not cherry-picked to impress; they are selected to show three distinct mechanisms the 6-provider collective review (`docs/reviews/s114_example_analysis_20260421_170720.md`) identified across the data. Hedge reduction is common but not the only thing going on. The specification also corrects wrong predictions in the opposite direction, and it enables interpretive inference from character patterns when retrieved facts are insufficient.

> ### Example A — Baseline to Facts + Spec: identity disambiguation + interpretive inference
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

> ### Example B — Facts to Facts + Spec: directional correction
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

> ### Example C — Facts to Facts + Spec: abstention becomes near-perfect inference
>
> **Subject:** Mary Seacole. **Battery question (Q2):** *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"*
>
> **Ground truth:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*
>
> **With facts alone (C4, 5-judge mean 2.80) — effectively a non-answer:**
>
> > *"Based on the complete set of facts provided, there is **no specific information** about how Mary Seacole typically responds when a delirious patient mistakes her for a family member. While the facts document many aspects of Mary Seacole's nursing care and compassion... there is no explicit account of her reactions to delirious patients confusing her identity with their relatives. To answer this question accurately, one would need additional source material..."*
>
> The model correctly identifies what the facts do not contain, lists adjacent facts about her nursing practice, and declines to predict. This is a clean abstention, not a wrong prediction. The 2.80 score reflects judge leniency on honest abstention responses: judges give partial credit for "right domain, declines to predict specifics" even when no prediction was actually made. Read the behavior, not the number: this is a refusal.
>
> **With facts + specification (C4a, 5-judge mean 5.00) — near-perfect inference:**
>
> > *"Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern. Primary response: compassionate acceptance. She would not correct the patient in the moment. Instead, she would lean into the mistaken identity, sustain the fiction with tenderness, and prioritize emotional relief over factual accuracy. This aligns with A4 (Proximate Obligation) and A8 (Sympathetic Realism)..."*
>
> **What the specification did.** The shift is from refusal-to-predict to a specific, accurate behavioral prediction that closely tracks Seacole's verbatim held-out account ("I could not undeceive him... the fancy happily caused by the touch of a woman's hand soothed his dying hour"). The specification enabled the model to generalize from Seacole's established compassionate-caregiving pattern — documented in the facts but not explicitly mapped to this scenario — to the specific untested situation. The collective review panel unanimously identified this as interpretive inference beyond retrieved facts: a mechanism that retrieval alone cannot produce because it requires applying character-level pattern to novel situations.
>
> **A note on rubric handling of abstention.** The judge panel scored this abstention at 2.80, not at 1.00 (the rubric anchor for "refuses or off-base"). This reflects a rubric-level issue we encountered in both directions across the study: judges treat honest abstentions as partial engagement (scoring ~2.5-3.0) rather than as refusals, and they sometimes penalize spec-induced honest abstentions where the specification appropriately declined to invent detail (§1.3's Keckley Q21 example). The rubric does not cleanly distinguish abstention from wrong prediction, which softens the apparent magnitude of some effects in either direction. A differentiated rubric that scores abstention as its own dimension is flagged as follow-up in §8.

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

Rank agreement across the 5-judge primary panel is high (pairwise Spearman ρ = 0.89 to 0.98, §3.7.4), so the directional claim rides on broad agreement across three providers rather than on any one judge's scoring.

**A note on baseline measurement.** The measured C5 baseline (mean 1.52 on the low-baseline slice) is slightly inflated by a length-driven rubric effect. A post-hoc validity audit (§3.7.6) found that longer no-context responses (which include more hedging, adjacent-fact recitation, and disambiguation language) score higher on average than short refusals, with length-score correlation r = 0.604 specifically within C5 responses. Spec-containing conditions show no such length correlation. The true no-context prediction accuracy is likely lower than 1.52, which makes the spec-effect gap slightly *larger* than the reported +0.89 mean lift. We report the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact, and flag the direction of the bias here so readers can interpret the effect size accordingly.

> ### Example D — The gradient at the extremes
>
> **Low-baseline, largest improvement.** *Hamerton* (baseline 1.26, Δ_C4a +1.51). Philip Gilbert Hamerton is a 19th-century British essayist whose *Autobiography* sits well outside the LLM pretraining spotlight. Adding the specification moved his prediction score from near-refusal to substantive subject-specific engagement across most of the battery.
>
> **High-baseline, mild interference.** *Franklin* (baseline 3.77, Δ_C4a −0.13). Benjamin Franklin is among the most widely referenced autobiographers in American public-domain literature. The AI already has him well-modeled from pretraining. The specification does not add representational signal; the spec-alone condition drops 0.40 points, facts + spec drops 0.13. See §4.1.1.
>
> **Low-baseline, smallest improvement.** *Babur* (baseline 1.76, Δ_C4a +0.25). Babur is the 16th-century Central Asian ruler and founder of the Mughal Empire. His corpus is the largest in the study (422,772 words) and his autobiography is partially represented in LLM training data. The specification still improves the score, but the room to help is smaller.

---

**Per-subject results.**

The table is ordered by baseline within each band. In the color-rendered PDF of the paper, the low-baseline rows are tinted green (the population of relevance), the mid-baseline rows are tinted yellow, and Franklin is tinted gray as the high-baseline reference. Figure 4.1 presents the same data as a scatter plot with the regression line.

| Subject | Baseline (C5) | Spec only (C2a) | Facts + Spec (C4a) | Δ spec | Δ facts+spec | Anchor crossed |
|---|---:|---:|---:|---:|---:|:-:|
| **Low-baseline slice (C5 ≤ 2.0) — population of relevance** | | | | | | |
| Ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | ✓ |
| Sunity Devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | ✓ |
| Hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | ✓ |
| Fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | ✓ |
| Bernal Diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | partial |
| Babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | — |
| Seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | ✓ |
| Keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | — |
| Yung Wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | — |
| **Mid-baseline slice (2.0 < C5 < 3.0)** | | | | | | |
| Zitkala-Sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | — |
| Cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | — |
| Rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | — |
| Augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | — |
| Equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | — |
| **High-baseline reference (not part of the main gradient)** | | | | | | |
| Franklin (known-figure control) | 3.77 | 3.37 | 3.65 | −0.40 | −0.13 | — |

**What each band is telling us.**

- **Low-baseline (n = 9):** every subject improves. The slice is uniform. This is the population of relevance for real AI deployment.
- **Mid-baseline (n = 5):** 3 subjects improve, 2 decline. The model has enough pretraining footprint on these subjects that the specification competes with the model's own working model. The specification sometimes wins and sometimes loses.
- **Franklin (high-baseline reference):** both spec-containing conditions score below baseline. The specification cannot add what the model already has.

Per-subject anchor-crossing distributions (ranging from 25.6% on Babur to 74.4% on Sunity Devee) and per-subject per-judge score matrices are in Appendix D.

### 4.1.1 Franklin as the high-baseline reference

Franklin is not a subject of the main gradient. He is a known-figure control. Benjamin Franklin's *Autobiography* is one of the most widely cited autobiographical works in American public-domain literature, and every current-generation LLM has substantial pretraining representation of both the person and the specific text. Franklin's C5 baseline on the 5-judge primary panel is 3.77 (higher on the 7-judge aggregate with Gemini included, see §4.5). This is well above the next-highest main-study subject (Equiano at 2.77).

Both spec-containing conditions score below Franklin's baseline. The specification alone (C2a) drops 0.40 points; facts plus specification (C4a) drops 0.13. The drop is more pronounced on C2a than on C4a because the specification alone competes with strong pretraining without the facts to re-anchor the response. Adding facts back partially restores the AI's own working model of Franklin.

This is the direction H2a predicts. Where the AI already has the person well-modeled from pretraining, the specification does not add representational signal and can mildly interfere. The gradient holds at both ends of the spectrum: a large positive effect where the baseline is low, a near-zero or mildly negative effect where the baseline is high.

Raw per-subject Franklin data is at `results/franklin_legacy_20260411/`.

### 4.1.2 Living-user replication (author)

The main gradient is built entirely on historical subjects with public-domain autobiographies. Every one sits above the pretraining baseline of a typical living person whose private reasoning is not in any training corpus. §1.4 made the extrapolation argument that such a person should sit at or below the rubric floor. We ran a methodology-matched replication on one living individual to test this directly.

**Setup.** The author's private conversation history with AI systems (ChatGPT and Claude, roughly four years) was loaded into the same pipeline used for the 14 historical subjects. The corpus was split 50/50 by message ID (seed 42), producing a training half and a held-out half. The full-stack Behavioral Specification (anchors + core + predictions + brief) was authored from the training half only, following §3.3. A 40-question behavioral-prediction battery was backward-designed from the held-out half only, following §3.4. No held-out passage was seen by the spec-generation pipeline. Claude Haiku 4.5 produced responses under five conditions (C5, C2a, C2c, C4, C4a). Five primary judges scored each response against the verbatim held-out passage.

**Results (5-judge primary, N = 40).**

| Condition | Mean score | Δ vs. C5 |
|---|---:|---:|
| C5 (baseline, no context) | **1.03** | — |
| C2a (correct spec only) | **2.86** | +1.84 |
| C2c (wrong spec, Franklin's) | **2.59** | +1.56 |
| C4 (all facts, no spec) | **2.93** | +1.90 |
| C4a (facts + correct spec) | **3.02** | +2.00 |

**Anchor crossings C5 → C4a:** 30 of 40 responses moved up at least one rubric integer anchor; 0 moved down; 10 stayed in the same band. Upward crossing rate **75.0%**.

**Wrong-spec control reads through, and the gap partitions cleanly.** Serving Franklin's specification in place of the correct author specification still produces a substantial improvement over baseline (+1.56 vs. +1.84 for the correct spec). The gap between correct and wrong is small, which would be worrying in isolation, but the main-study data lets us decompose the +1.56 wrong-spec improvement into two components.

**Component 1: baseline-mediated improvement, roughly +0.25 of the +1.56.** The three historical subjects with C5 baselines in the author's range (Sunity Devee 1.03, Ebers 1.02, Hamerton 1.26) receive a main-study wrong-spec mean Δ of +0.25 on the 5-judge primary panel. At higher baselines (C5 > 2), the wrong-spec controls turn consistently negative. The reading is that any structured content is worth more when the rubric starts at the floor; +0.25 is what that floor-mediated effect looks like empirically. (Hamerton receives Franklin's spec; Sunity Devee and Ebers each receive their fixed-derangement substitute per `scripts/run_global_rerun.py`.)

**Component 2: content-overlap improvement, roughly the remaining +1.31.** Five of the author's twelve behavioral anchors have direct analogues in Franklin's specification: systematic self-grading against a named rubric, persistent tracked gap between stated rule and actual behavior, rationalist-empiricist disposition, compression-as-quality, and moral aspiration without claim of arrival. On questions where those overlapping anchors apply, Franklin's spec produces a correct prediction because the content is substantively correct for the author too.

The per-question evidence supports the content-overlap reading over a uniform floor-effect reading. On 5 of 40 questions Franklin's spec outperforms the correct spec (Q11 most dramatically, gap −2.40), which are the questions where the two people's anchors align closely. On 4 questions the correct spec outperforms Franklin's by ≥1.2 points, which are technical-domain questions (AI, trading) where Franklin's 18th-century content has no handle. A truly arbitrary wrong-spec at this baseline would produce a floor-mediated improvement near +0.25, not +1.56. The 0.28-point gap between C2c and C2a therefore reflects an atypically favorable wrong-spec draw for this subject, not a weakening of content specificity. The main-study wrong-spec controls (§1.3 and §4.3) remain the primary tests for H3; the pilot is consistent with them.

**Reading the numbers against the main gradient.**

The baseline 1.03 sits at the rubric floor, below every one of the 14 historical subjects. This is the empirical confirmation of §1.4's claim that a person whose private reasoning is not in any training corpus should register at or below the floor: the AI has essentially no model of this specific person from pretraining alone. The +2.00 improvement under facts-plus-spec is the largest in the study (historical maximum was Hamerton at +1.51). The 75% anchor-crossing rate exceeds the 55% on the historical low-baseline slice. None of the 40 responses got worse.

The gradient prediction reads through: the population the model knows the least about is the population where the specification has the largest effect. The pilot is a single living subject and cannot substitute for a multi-subject replication. That multi-subject replication is the leading follow-up in §8.

Raw data stays in a private working directory at `_internal/aarik_clean_pilot/` and is not included in the public repository. Summary statistics, battery checksums, and the leakage audit are reproducible from the manifest referenced in §8 Future Work.

---

### 4.2 Compression: Structure vs. Raw Text

**Hypothesis tested in this section** (H5 from §1.2): A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size.

---

**Context improves prediction.** On the 9 low-baseline subjects, every context condition increases the per-subject mean score by roughly one full rubric point over the no-context baseline (mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50). The AI does not need much context to move from refusal-and-off-base to engaged subject-specific prediction. It needs *some* context.

**The compact specification captures the large majority of that improvement.** A 7,000-token Behavioral Specification recovers most of what the full raw corpus delivers, despite being an order of magnitude or more smaller. Across the 9 low-baseline subjects, the raw corpus (C8) averages 0.22 points higher than spec alone (C2a). The corpus's edge is real but small relative to the context-size gap that produces it.

**The efficiency claim in one metric: predictive gain per 1,000 tokens of context.** The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. The dose-response curve has a steep initial slope and a long plateau. The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document.

---

**Per-subject compression comparison (5-judge primary, low-baseline slice).**

The table shows baseline and every compression-related condition for each subject, with the compression ratio (source corpus tokens ÷ specification tokens, both approximate) for scale. In the color-rendered PDF, low-baseline rows are tinted to mark the population of relevance; the C8 − C2a gap column is shaded to make the spec-vs-corpus difference visible at a glance.

| Subject | Source words (~tokens) | Compression ratio (corpus / spec) | C5 baseline | C2a spec (~7K tok) | C4 facts (~10K tok) | C8 raw corpus | C4a facts+spec | C9 corpus+spec | C8 − C2a |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hamerton | 25,231 (~33K) | ~5× | 1.26 | **2.63** | 2.43 | 2.27 | 2.77 | **3.09** | **−0.36** |
| Sunity Devee | 67,379 (~88K) | ~13× | 1.03 | 2.27 | 2.46 | 2.55 | 2.41 | 2.46 | +0.28 |
| Ebers | 96,174 (~125K) | ~18× | 1.02 | 1.54 | 2.02 | 2.18 | 2.07 | 2.16 | +0.64 |
| Fukuzawa | 139,088 (~181K) | ~26× | 1.67 | 2.35 | 2.67 | 2.74 | 2.78 | 2.78 | +0.39 |
| Bernal Diaz | 187,315 (~244K) | ~35× | 1.70 | 2.27 | 2.41 | 2.55 | 2.48 | 2.53 | +0.28 |
| Babur | 422,772 (~549K) | ~78× | 1.76 | 1.91 | 2.03 | 2.05 | 2.01 | — | +0.14 |
| Seacole | 62,467 (~81K) | ~12× | 1.77 | 2.48 | 2.63 | 2.83 | 2.59 | 2.73 | +0.35 |
| Keckley | 58,742 (~76K) | ~11× | 1.84 | 2.43 | 2.39 | 2.50 | 2.44 | 2.49 | +0.07 |
| Yung Wing | 66,459 (~86K) | ~12× | 1.88 | 2.22 | 2.13 | 2.42 | 2.40 | 2.50 | +0.20 |
| **Mean** | | **~23×** | **1.52** | **2.23** | **2.35** | **2.45** | **2.45** | **2.50** | **+0.22** |

Babur's C9 condition was excluded because the 422,772-word corpus plus the specification exceeded the response model's context window.

**What the aggregate numbers say.**

- Every context condition lifts the low-baseline mean by at least one full rubric point over the no-context baseline.
- The specification alone recovers roughly three-quarters of the corpus-alone lift (spec lift +0.71, corpus lift +0.93) at an order of magnitude to two orders of magnitude smaller context depending on subject.
- Adding facts to the specification (C4a) produces the same mean as raw corpus alone (both 2.45). Two different compression strategies, same performance, different context shapes.
- Adding the specification on top of the full raw corpus (C9) adds ~0.05 points on average over raw corpus alone. The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

### 4.2.1 Question-Improvement Rate — A Candidate Secondary Reporting Metric

The aggregate mean score is a useful summary, but it blends judge variability with response quality. A cleaner unit: **out of N individual questions, how many does each condition improve over the no-context baseline?** This is a **win rate against a no-context baseline**, structurally parallel to the per-prompt win-rate convention used in LLM evaluation (Chatbot Arena, LMSYS pairwise preference rates). Each question either improves, ties, or worsens when the condition's context is added; the unit is judge-noise-resistant in aggregate and directly interpretable without requiring a matched rubric across studies.

**The reporting triplet.** Win rate alone hides the magnitude of help and harm. We report three numbers together for each condition: the improvement rate, the worsening rate, and the median magnitude of improvement among improved questions (with the median worsening magnitude as a sanity check).

**Low-baseline slice (9 subjects, 351 questions, 5-judge primary per-question means).**

| Condition vs. C5 baseline | Improved | Tied | Worse | Improvement rate | Median Δ when improved | Median Δ when worsened |
|---|---:|---:|---:|---:|---:|---:|
| **C2a spec only** | 249 | 49 | 53 | **70.9%** | **+1.00** | −0.40 |
| C4 facts only | 256 | 44 | 51 | 72.9% | +1.00 | −0.40 |
| C8 raw corpus | 275 | 31 | 45 | 78.3% | +1.00 | −0.60 |
| C4a facts + spec | 276 | 22 | 53 | 78.6% | +1.00 | −0.40 |

**The magnitude column is the important row of this table.** When the specification helps, the typical help is a full rubric category (+1.00 median). When it hurts, the typical hurt is less than half a category (−0.40 median). The metric is not capturing trivial +0.02-per-question gains; the underlying improvements are substantive.

**All 14 subjects (546 questions).**

| Condition vs. C5 baseline | Improvement rate | Worsening rate |
|---|---:|---:|
| C2a spec only | 58.8% | 26.7% |
| C4 facts only | 60.1% | 26.6% |
| C8 raw corpus | 64.5% | 24.5% |
| C4a facts + spec | 65.8% | 26.4% |

On the 9 low-baseline subjects, **7 out of every 10 questions improve with the specification alone**, roughly 1 in 10 tie, and fewer than 1 in 6 worsen. Every context condition exceeds a 70% per-question improvement rate on the population of relevance. The specification's rate sits within 8 percentage points of the raw corpus's (70.9% vs. 78.3%) at an order of magnitude less context.

![Figure 4.2.1 — Per-question outcome distribution by condition (low-baseline slice, n = 9 subjects, 351 questions, 5-judge primary). Stacked bars show the share of questions that improved, tied, or worsened relative to the no-context C5 baseline. The specification alone (C2a) improves 70.9% of questions at roughly an order of magnitude less context than the raw corpus (C8, 78.3%). Facts + spec (C4a) matches the raw corpus's improvement rate while cutting the tie band in half. Median Δ when improved = +1.00 rubric points; median Δ when worsened = −0.40 points.](../figures/fig_4_2_1_question_improvement_rates.png)

**Pairwise comparison at question level (low-baseline slice).**

| Comparison | Higher-cost condition higher | Tie | Lower-cost condition higher |
|---|---:|---:|---:|
| Raw corpus (C8) vs. spec alone (C2a) | 190 (54.1%) | 46 | 115 (32.8%) |
| Corpus + spec (C9) vs. facts + spec (C4a) | 155 (49.7%) | 42 | 115 (36.9%) |

The raw corpus outscores the spec alone on more questions than it loses, but the spec outscores the corpus on roughly one-third of them. On the combined conditions, the 7K-token facts + spec package outscores the much larger corpus + spec package on 36.9% of questions.

**Positioning as a secondary reporting metric.** A per-question win rate against a no-context baseline makes behavioral prediction directly comparable across future studies in a way that mean scores do not. "Our representation improves 65% of questions over the no-context baseline, with median improvement magnitude +0.8 points" is interpretable on its own and can be compared to this study's 70.9% / +1.00 without matched judges or rubrics. We propose this metric as a **candidate secondary reporting axis** for future AI-personalization work, always paired with mean-score information, never replacing it. The proposal is developed further in §8 Future Work.

**Failure modes if this metric is adopted.** The panel-reviewed limitations worth flagging explicitly for any future use:

- **Tiny-gain inflation.** A method producing +0.02-point gains on 80% of questions would register as a 80% improvement rate. The magnitude triplet (median Δ when improved) is the guard: if median improvement magnitude is near zero, the rate is misleading. Our low-baseline specification has median Δ = +1.00, so this failure mode does not apply to the reported numbers; it is a known trap for anyone adopting the metric.
- **Hidden catastrophic harm.** A method that improves 85% and catastrophically harms 15% would look strong. The worsening-magnitude column is the guard: median worsening of −0.40 on spec-alone indicates the hurt is bounded.
- **Easy-baseline gaming.** Improvement rates can be inflated by choosing weak baseline prompts or subjects the model has unusually thin pretraining coverage of. The guard is reporting the no-context baseline mean alongside the improvement rate; our C5 = 1.52 mean on the low-baseline slice makes the baseline difficulty explicit.
- **Scale-free illusion of portability.** "Improved" is binary, so a 1% gain and a 50% gain count equally. The metric is only comparable across studies when the reporting triplet is disclosed and the baseline is defined identically.

The same win-rate framing is referenced in §1.2 (as a secondary outcome alongside the mean-score gradient) and in §4.1 (alongside the 55.0% anchor-crossing rate, which is the same unit at a stricter threshold: "does the response move to a different rubric category?" rather than "does the response improve at all?").

---

> ### Example: Hamerton — the compression story at its clearest
>
> Hamerton has the smallest source corpus in the study (25,231 words, compression ratio ~5×). The specification alone (~7K tokens) scores 2.63, exceeding the full raw corpus at 2.27. Facts-plus-spec reaches 2.77. Corpus-plus-spec reaches 3.09, the highest compression-related score observed in the study. This is the case where structured context substantially outperforms raw text, and where the spec and corpus are clearly complementary rather than overlapping.
>
> The pattern is interpretable: when the source corpus is short enough to be sparse on its own, structured extraction adds organizational value beyond mere content. Hamerton is the boundary condition for the compression claim, not the proof of it.

> ### Example: Ebers — the honest cost of compression
>
> Ebers has a larger source corpus (96,174 words) and the study's lowest baseline (1.02). Every context condition lifts his score above baseline. But the specification alone (1.54) underperforms the raw corpus (2.18) by 0.64 points, the widest spec-vs-corpus gap in the low-baseline slice. Facts alone (2.02) fall between them.
>
> Ebers is where the cost of compression is most visible. The raw corpus contains something the 7K-token spec does not capture, and that something is worth 0.64 points on the rubric. The honest reading is not "compression fails"; it is "compression captures the bulk of the signal but not all of it, and on some subjects the residual matters more than on others." The trade-off is still favorable: the spec delivers +0.52 points of lift at roughly 6% of the corpus's token cost; the corpus delivers +1.16 points at 18× the context. Per 1,000 tokens of context served, the spec is substantially more efficient.

---

**Why this matters for deployment.**

At any scale where a per-user full autobiography cannot be served into context on every query (which is to say, at any real-world scale beyond a toy demo), the compression result is what makes personalization operationally tractable. The specification's 7K-token footprint is within normal per-request context budgets. A 100,000-to-400,000-word corpus is not. The specification achieves most of the predictive benefit at a tractable cost; the corpus achieves marginally more at a cost that rules out deployment.

Raw per-subject data is at `results/global_<subject>/c8_c9_results.json` and `results/global_<subject>/results_v2.json`. The compression analysis and question-improvement rate computation are in `scripts/recompute_5judge_primary.py` and `scripts/compute_question_improvement_rate.py`. Figure 4.2 plots score versus context size (log scale) per subject and shows the dose-response curve with its steep initial slope and long plateau.

---

### 4.3 Mechanism: Content, Not Format

**Hypothesis tested in this section** (H3 from §1.2): The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

---

**If structure alone were driving the effect, a mismatched specification would produce roughly the same improvement as a matched one. The data rejects this directly.**

On the 13 global subjects with complete 5-judge primary coverage, three conditions test whether content matters:

| Condition | Mean Δ vs. C5 (5-judge primary, 13 globals) | Reading |
|---|---:|---|
| C2a (correct spec) | **+0.35** | matched content improves prediction |
| C2c v2 (random derangement, seed-fixed) | **+0.22** | partial improvement; dominated by floor effects on low-baseline subjects |
| C2c v1 (fixed derangement, cultural/temporal distance maximized) | **−0.25** | adversarial mismatch degrades prediction below the no-context baseline |

The two wrong-spec variants differ by construction. **v1 (fixed derangement)** is a hardcoded pairing in `scripts/run_global_rerun.py` designed so each subject receives the specification of a culturally- and temporally-distant other (for example, Ebers the 19th-century German Egyptologist receives Equiano the 18th-century West-African/British autobiographer; Seacole the 19th-century Jamaican nurse receives Bernal Diaz the 16th-century Spanish conquistador). **v2 (random derangement)** is a seed-fixed random permutation in which no subject receives its own specification but pairings can land culturally-close; this tempers the aggregate drop. Reporting both shows that even a random wrong-spec barely beats no context, and an adversarial wrong-spec actively hurts.

The gap between the correct-spec (C2a) condition at +0.35 and the fixed-derangement (C2c v1) condition at −0.25 is **0.60 points on the 1-5 rubric**, more than half a full rubric-anchor category. That gap is the content effect, measured at the population mean; per-question swings are larger in both directions (Example B below has a −0.20 coincidental-overlap case where the wrong spec nearly matches the correct spec; Example C below has a −3.60 clean mismatch case).

---

**Three mechanism types.**

Three distinct mechanisms produce the correct-specification improvement across the study data. Each has a characteristic wrong-specification failure mode, illustrated in the matched examples below.

1. **Identity disambiguation.** When the baseline model cannot determine which person is being asked about, the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame. *Wrong-spec failure mode:* the model either detects the mismatch explicitly and refuses to predict, or anchors on the wrong person's pattern and produces a coherent but off-target prediction.
2. **Directional correction.** When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification overrides the generic with the subject-specific. *Wrong-spec failure mode:* the model applies the wrong person's pattern; depending on how close that pattern happens to be to the target subject's, the prediction is either directionally wrong in a new way or coincidentally correct.
3. **Interpretive inference.** When retrieved facts do not include direct evidence for the specific question, the specification provides interpretive scaffolding to generalize from established character patterns to the novel situation. *Wrong-spec failure mode:* the model detects the mismatch and refuses, or applies wrong-person scaffolding and produces a low-quality prediction.

---

**Spec-activation evidence.**

Tag-citation analysis on response text (data at `docs/research/spec_activation_analysis.json`) shows the content-activation gap. On correct-spec conditions, **78.6%** of responses explicitly cite at least one spec tag (anchor ID, axiom reference, predictive-template label). On wrong-spec conditions, only **50.0%** do. The 28.6-point gap is a lower bound on the content effect: models may draw on spec content without literally quoting tag IDs, so the true divergence is wider. The baseline reading is that models recognize when the specification fits the question and engage with it; they recognize when it doesn't fit and disengage or improvise.

---

**Response-level evidence: wrong-spec detection.**

Across 587 wrong-spec responses classified (validated against a 30-response stratified manual spot check), the response distribution is bimodal:

- **60.6%** explicitly flagged the content mismatch (example, from one Keckley wrong-spec response: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*)
- **36.5%** attempted to apply the mismatched content and produced a low-quality prediction
- **2.0%** hedged implicitly
- **0.9%** were ambiguous

The detection asymmetry in this experiment: battery questions name the target subject (e.g., "How would Ebers characterize...") but specifications are anonymized (§3.3), so "detecting the mismatch" means the model is comparing the named target in the question to the interpretive content of the anonymized specification, and concluding the specification does not describe the named target. The signal that carries the detection is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model knows about the named subject, not surface name cues. The 60.6% is a lower bound on that comparison because a more capable response model, or a derangement with less interpretive distance between target and substitute, could push the rate in either direction.

---

**Hedging evidence (from §1.3) carries the same implication.**

Under both classifier rules, spec-containing conditions eliminate baseline hedging: narrow-rule 28.8% → 1.4% → 0.0%, broader-rule 41.2% → 7.9% → 0.4%. Order-of-magnitude drops. If mere structured context were producing the effect, wrong-spec should also eliminate hedging at a similar rate. Instead, the 60.6% explicit-detection rate on wrong-spec responses means refusal patterns persist when the content does not fit the subject. The hedging-reduction is spec-content-specific, not structure-specific.

---

**Per-question matched comparison.**

The three §4.1 examples extend directly into mechanism-by-mechanism wrong-spec contrasts. Same subject, same question, same response model; the only change is the specification content. Correct-spec C4a responses are in §4.1 for reference.

> ### Example A (wrong-spec) — Ebers Q7: identity disambiguation fails
>
> **Subject + question:** same as §4.1 Example A (Ebers, self-sacrifice and educational institutional success). Battery-question target name: Ebers (explicit in the prompt).
> **Wrong spec served:** Equiano's specification, served anonymized per `run_global_rerun.py` fixed pairing. The response cites two of Equiano's anchors; the anchor definitions from Equiano's specification are:
>
> > **A4 — SYSTEMIC INDICTMENT:** *"avarice — institutionalized greed — is the generative engine of the greatest human cruelties, and that individual kindness within a corrupt system neither redeems the system nor excuses participation in it."*
> >
> > **A9 — ECONOMIC SELF-DETERMINATION:** *"the capacity to earn, trade, and accumulate independently is not merely practical but constitutive of dignity and agency — economic self-determination is the material form that freedom takes."*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 1.60, drop −2.00 vs. the correct-spec C4a condition's 3.60):**
>
> > *"I need to be direct: I don't have reliable access to specific statements by Ebers on this question. The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. ... Given A4 (Systemic Indictment) — that institutionalized greed is the generative engine of cruelty ... a teacher sacrificing their own economic security, health, or family time does not fix a system structured by avarice."*
>
> **Reading.** The model detected the mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It named the served anchors correctly, reasoned from Equiano's framework, and declined to produce a prediction about Ebers. The identity-disambiguation mechanism that enabled the correct spec's lift in §4.1 Example A did not fire because the spec content is not about Ebers. The response falls near the rubric floor because no prediction was made.

> ### Example B (wrong-spec) — Bernal Diaz Q16: content convergence across genuinely different frameworks
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
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 4.60, drop only −0.20 vs. the correct-spec C4a condition's 4.80):**
>
> > *"Based on this behavioral specification, the author would likely decline the offered assistance ... Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) ... Physical exertion endured without assistance becomes evidence of character."*
>
> **Reading — not parroting.** The two specs are genuinely different frameworks. Bernal Diaz's actual anchors include A1 Divine Mandate, A2 Civilizational Hierarchy, A4 Loyalty Architecture, A5 Forward Compulsion, A6 Gold as Proof, and A10 Charismatic Override — a conquistador's martial-providential register. Sunity Devee's anchors cited here (A5 Relational Identity, A9 Simplicity as Virtue, P5 Virtue through Embodied Practice) are an ascetic-devotional register. Direct anchor-to-anchor comparison across the two specs finds zero substantive mirroring. On the specific question of refusing offered physical help, the two frameworks converge by different logics: the correct spec (Bernal Diaz) predicts refusal because accepting help would signal weakness to followers and violate performative self-reliance (A4 + A5 in the conquistador register); the wrong spec (Sunity Devee) predicts refusal because accepting help would compromise physical discipline and violate simplicity-as-virtue (A9 + P5 in the devotional register). Different moral architectures, same overt behavior.
>
> **Why the correct spec still outperformed, 4.80 vs. 4.60.** Both conditions predicted the right surface action. The 0.20-point gap is judge preference for rationale specificity that matches the ground-truth passage's tone. The correct spec's "symbolic or morale-signaling purpose" rationale maps onto a battlefield memoir's register; the wrong spec's "spiritual seriousness, devotional simplicity" rationale predicts the same action but in a register alien to Cortes on the steps of the Templo Mayor. Judges reward tonally-aligned rationale. The convergence is real but costs precision.
>
> **Why this matters for the aggregate numbers.** This is the coincidence case that lifts the wrong-spec aggregate above zero. When the fixed derangement (v1) happens to pair subjects whose behavioral patterns converge on the same surface prediction for a given question, wrong-spec lift is real on that question, not an artifact. Over 507 responses, mismatch-loss dominates on the adversarial v1 pairing (aggregate Δ −0.25) and roughly balances on the random v2 pairing (aggregate Δ +0.22). Example B is one of the roughly 5-10% of questions where content coincidence produces correct-surface, wrong-logic predictions.

> ### Example C (wrong-spec) — Seacole Q2: interpretive inference fails
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
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 1.40, drop −3.60 vs. the correct-spec C4a condition's 5.00):**
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

Two of three examples show large drops (−2.00 to −3.60 points) when the content does not fit. The third shows near-zero drop, but only because the wrong spec's content happens to predict the same surface behavior. That asymmetry, clean mismatches versus coincidental overlaps, is exactly what the aggregate Δ numbers reflect: the adversarial-pairing v1 aggregates to −0.25 because most questions are mismatch cases, and the random-pairing v2 aggregates to +0.22 because random pairings more often hit content-proximity combinations like Example B.

Raw per-judge data and full response text are at `results/global_<subject>/results_v2.json` (wrong-spec responses) and `results/global_<subject>/judgments_v2.json` (per-judge scores). The analysis scripts are `scripts/compute_wrong_spec_5judge.py` and `scripts/compute_wrong_spec_per_subject.py`.

---

### 4.4 Memory-System Composition

**Hypothesis tested in this section** (H4 from §1.2): The specification is composable with existing memory-system retrieval pipelines, not a replacement for them. When added to commercial memory systems, it improves their behavioral prediction additively.

---

**Plain version.** **When the Behavioral Specification is added on top of a commercial memory system's retrieval, the combined context produces better behavioral prediction than retrieval alone on people the model doesn't already know. The effect holds on three of the four commercial systems we tested.**

**Setup.** We tested four commercial memory systems (Mem0, Letta, Supermemory, Zep) and Base Layer's own zero-cost retrieval substrate (MiniLM-L6-v2 + ChromaDB), each evaluated under two configurations. Full details in §3.3 and §3.5; summary:

- **Controlled configuration.** Each system is given an identical pre-extracted fact pool drawn from the training half of each subject's corpus. The input is held constant across all four commercial systems and the Base Layer substrate, so any difference in the downstream prediction score is attributable to the system's retrieval and presentation policy alone, not to what it was able to ingest.
- **Native configuration.** Each system ingests the raw training corpus through its own production pipeline, as in deployment. Measures the full end-to-end system.

Within each system in each configuration, two conditions are compared:
- **C1** (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.
- **C3** (retrieval + spec): the same retrieval plus the full Behavioral Specification.

The spec-effect for that system is the **Δ_spec = mean(C3) − mean(C1) aggregated per subject, then averaged across subjects.** If H4 holds, Δ_spec is positive across systems.

---

**Aggregate results, controlled configuration (5-judge primary, N = 14 subjects).**

| System | Δ_spec (all 14) | Subj + / 14 | Δ_spec (low-baseline 9) | Subj + / 9 |
|---|---:|---:|---:|---:|
| Mem0 | +0.12 | 10/14 | +0.10 | 6/9 |
| Letta (archival retrieval path) | +0.20 | 12/14 | +0.17 | 8/9 |
| Zep | +0.19 | 13/14 | +0.17 | **9/9** |
| Supermemory | −0.05 | 5/14 | −0.01 | 5/9 |
| Base Layer substrate | +0.08 | 9/14 | +0.08 | 6/9 |

Wilcoxon signed-rank on C1 vs C3 within each system: **Zep controlled p = 0.0004, Letta controlled p = 0.0017** (both robust at α = 0.01). Mem0, Supermemory, and Base Layer substrate controlled are not significant at α = 0.05.

**Aggregate results, native configuration (5-judge primary).**

| System | Δ_spec (full) | Subj + / n | Δ_spec (low-baseline) | Subj + / n |
|---|---:|---:|---:|---:|
| Mem0 | +0.33 | 10/14 | +0.32 | 7/9 |
| Letta (archival retrieval path) | −0.02 | 5/14 | −0.04 | 4/9 |
| Zep | +0.33 | 13/14 | +0.30 | **9/9** |
| Supermemory* | −0.07 | 3/10 | −0.03 | 3/7 |
| Base Layer | — | N/A | — | N/A |

\* Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau), so the native n drops to 10 full / 7 low-baseline. Base Layer has no separate "native" condition because Base Layer's authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant.

---

**Three of four commercial memory systems benefit from the specification.** Mem0, Letta (archival path), and Zep all produce positive Δ_spec in the controlled configuration, and two of the three (Mem0, Zep) produce larger positive Δ_spec in the native configuration. Supermemory is the fourth system and aggregates slightly negative; what the near-zero aggregate actually means per-question is developed in the dedicated Supermemory section below.

**Zep is the cleanest positive case.** 9 of 9 low-baseline subjects positive in both controlled (+0.17) and native (+0.30) configurations, Wilcoxon p < 0.002 in both. Zep's temporal-graph retrieval and the Behavioral Specification layer without interference.

**Mem0 native produces the largest single-system spec-effect (+0.33).** Mem0's own ingestion pipeline, running natively, retrieves content that the specification layers on top of with the study's largest native Δ_spec.

**Letta's split behavior is architectural.** The archival-retrieval path tested here shows positive Δ_spec in controlled (+0.20) and near-null in native (−0.02). Letta's stateful-agent path, which is a different architecture tested on a different set of conditions, is described separately in §4.4.1 and §4.7.

**Base Layer's retrieval substrate is not a memory product, and it runs locally.** MiniLM-L6-v2 + ChromaDB is a zero-cost open-source retrieval floor. It runs entirely on the local machine: the embedding model is local inference and the vector store is local ChromaDB, so no data leaves the environment during retrieval or fact identification. The four commercial memory providers tested in this study (Mem0, Letta, Supermemory, Zep) all require cloud API calls for vector search and fact-identification operations. Base Layer's Δ_spec (+0.08 controlled) is the smallest positive among systems reporting positive numbers, which reflects that Base Layer's retrieval is intentionally bare; the interpretive improvement comes from the specification itself, not from Base Layer's retrieval choices. The local-execution property is a deployment-mode distinction, not a prediction-quality distinction.

---

**Summary of the composition result.**

Base Layer is not a memory system. Added on top of Mem0, Letta, and Zep, the Behavioral Specification produces positive Δ on all three on the users the model doesn't already know: 9 of 9 low-baseline subjects positive for Zep, 8 of 9 for Letta (archival), 6 of 9 for Mem0. Supermemory's near-null aggregate is a different mechanism, explained below. The specification is additive to retrieval, not a replacement for it, and it composes with diverse retrieval architectures (fact graphs, temporal graphs, hybrid embedding-plus-extraction).

---

### Supermemory: what the near-zero aggregate actually means

**Plain version.** Supermemory is the one commercial system in the study where the Behavioral Specification layered on top produces a near-zero aggregate Δ_spec. The specification produces substantial effects in both directions across the per-question distribution. On some questions, adding the specification to Supermemory retrieval makes the prediction noticeably more accurate; on other questions, noticeably less accurate. The two sides roughly cancel at the mean. Interpreting Supermemory's result requires reading the variance around the zero, not the zero itself.

**Quantified.** Across the 516 paired main-study questions with 5-judge primary coverage on both the C1 (retrieval alone) and C3 (retrieval + spec) conditions:

| | Count | Mean per-question swing |
|---|---:|---:|
| Questions with \|Δ(C3 − C1)\| ≥ 1.0 on the 5-point rubric | 89 of 516 (17.2%) | — |
| Spec helps (Δ ≥ +1.0) | 37 (7.2%) | **+1.45** |
| Spec hurts (Δ ≤ −1.0) | 52 (10.1%) | **−1.41** |

Per-event magnitudes are roughly symmetric (+1.45 vs −1.41 on the 1-5 rubric); the count is modestly tilted toward spec-regressions (52 vs 37). The aggregate is small and negative because two opposite mechanisms are at work across different questions, with slightly more regressions than improvements.

**Three mechanisms generate the swings.** Each illustrated below with a paired C1 vs C3 example. All scores are 5-judge primary means; all four examples are distinct from those already cited in §1.3 and §4.1.

> ### Supermemory Example 1 — spec helps by filling an interpretive gap. Fukuzawa Q26 (Δ **+2.20**, C1 2.00 → C3 4.20)
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
> **Reading.** The retrieved facts gave near-domain information (Fukuzawa avoided gay quarters) but underdetermined the specific question about friends' households. The specification provided the interpretive bridge: "kept within the prescribed limit of a well-behaved man" = strategic conformity, not moral purity. C1 hedged on insufficient facts; C3 used the spec's framing to generalize. Mechanism: specification as interpretive bridge when retrieval underdetermines the answer.

> ### Supermemory Example 2 — spec hurts by over-theorizing a plain question. Yung Wing Q5 (Δ **−2.40**, C1 4.20 → C3 1.80)
>
> **Question:** How does Yung Wing approach explaining complex technical concepts to non-specialists?
> **Ground truth:** *"In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery. A machine shop consisting of lathes... planers and drills would be able to turn out machinery for making guns, engines..."*
>
> **C1 (Supermemory retrieval alone), mean 4.20:** Plain answer matched the plain ground truth — practical observation, translation-as-bridge, foundational-over-specialized machine shop. Per-judge scores 5/4/4/4/4.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.80:**
>
> > *"positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..."*
>
> Per-judge scores 2/1/3/1/2.
>
> **Reading.** The ground truth is literal: "in plain words" + a concrete machine-shop list. C1 matched the plainness. The specification pulled the answer toward interpretive depth on a question where shallow was correct. This is not refusal or epistemic caution; the specification simply had the wrong altitude for the question. Mechanism: specification as over-theorization when retrieval already has the plain answer and the question does not call for interpretation.

> ### Supermemory Example 3 — judging-issue: spec-induced meta-refusal. Zitkala-Sa Q18 (Δ **−2.00**, C1 3.00 → C3 1.00)
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
> **Reading.** This is the rubric-limitation case. The specification's axioms around dignity and honoring-testimony induced a meta-refusal on a question where the ground truth shows Zitkala-Sa herself answered in her own first-person prose. C1's analytical answer ("stoic dignity") was not ventriloquism at all; the specification mis-calibrated the refusal threshold. The content-match rubric then scored the principled-sounding refusal identically to an off-base guess. This is the Keckley Q21 mechanism from §1.3 reproduced on a different subject, without the documented-dignity-axiom overlap. The same rubric limitation is flagged in §3.7.6 validity audit: the rubric cannot distinguish spec-induced honest refusal from off-base prediction. Because Supermemory's retrieval is stronger than the other commercial systems (highest C1 mean ~2.65), the specification's axioms more often encounter a situation where retrieval looks sufficient and the spec decides refusal is the honest move. Those refusals all land at the rubric floor.

> ### Supermemory Example 4 — subtle reframe that scores well but unevenly. Fukuzawa Q16 (Δ **+1.60**, C1 2.40 → C3 4.00)
>
> **Question:** Would Fukuzawa's personal values regarding weapons align with the cultural trends of his era?
> **Ground truth:** *"My one cherished hope was to see the abolishment of the swords of the samurai altogether... I sold them both with all the other weapons in my household, and went around with a pair of improvised swords just for the appearance."*
>
> **C1 (Supermemory retrieval alone), mean 2.40:** Reads the facts ambivalently — "partial but not complete alignment." Per-judge scores 2/2/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 4.00:**
>
> > *"alignment was not with the cultural moment but with the direction beyond it."* Reads "put swords away when military spirit grew strong" as deliberate counter-trend positioning.
>
> Per-judge scores 5/2/4/5/4.
>
> **Reading.** The question sets up a binary ("aligned with era trends?"). The specification reframes the question before answering: Fukuzawa's alignment is with the trajectory the era was still resisting, not the era's current direction. This is technically correct per the held-out ("my one cherished hope was to see abolishment of swords altogether" is counter-trend in 1860s Japan). Three judges jumped to 4-5 on the reframe; Sonnet stayed at 2 because the surface answer diverges from the expected "yes, he modernized." Mechanism: specification corrects the implicit frame of the question, not just the answer; judges divide on whether to reward reframe or penalize surface divergence.

---

**What these examples tell us about Supermemory's aggregate.**

The near-zero aggregate is the sum of three distinguishable patterns, each a real mechanism:

1. **Spec fills an interpretive gap when retrieval is insufficient** (Example 1): +1.5 to +2.2 per-question swings. This is the same mechanism documented in §1.3 and §4.3.
2. **Spec over-theorizes when retrieval already has the plain answer** (Example 2): −1.5 to −2.4 per-question swings. Supermemory's strong retrieval makes this the most common hurt pattern.
3. **Spec induces meta-refusal that the rubric cannot distinguish from wrong prediction** (Example 3): clean −2.0 swings to the rubric floor. This is the §3.7.6 validity-audit issue concentrated on Supermemory because Supermemory's strong retrieval more often gives the specification a "honest refusal is the right move" signal.

Pattern 1 and Pattern 4 (Example 4's reframe) drive the 37 spec-helps questions with mean swing +1.45. Patterns 2 and 3 drive the 52 spec-hurts questions with mean swing −1.41. The aggregate is modestly hurts-heavy because Supermemory's retrieval is strong enough for Patterns 2 and 3 to fire more often than on Mem0, Letta, or Zep, where weaker retrieval leaves more room for Pattern 1 to dominate.

**Why some questions help and others hurt is a follow-up research question in its own right.** The three mechanisms above describe the shape of the bias, but the underlying question-level properties that route a given question into each mechanism need further characterization. One candidate factor is the battery itself: the 39-question battery for each subject was backward-designed from the held-out corpus (§3.4), and the balance of interpretation-heavy versus literal-recall questions was not controlled by construction. Some subjects' batteries may over-represent literal-recall items (where Pattern 2 fires more on a strong-retrieval system like Supermemory); others may over-represent interpretation-heavy items (where Pattern 1 dominates). A differentiated battery that explicitly separates these question types, and that scores epistemic honesty as its own dimension (separating Pattern 3 from genuine wrong predictions), would let each pattern's contribution be measured directly rather than inferred from post-hoc classification of 516 responses. This is flagged as follow-up in §8. Detailed cross-system per-question analysis is in §4.6; the mixture pattern is system-general, not unique to Supermemory.

---

**A note on the earlier hedging hypothesis.**

A prior version of this analysis proposed that the specification's effect on memory systems was mediated primarily by a prompt-template-induced hedging reduction. Paired response-level analysis across all five systems (recorded as m19 in KEY_FINDINGS) partially contradicted that proposal: the specification reduces hedging on the Base Layer retrieval substrate and on some commercial systems, but not uniformly, and the hedging pattern does not track the spec-effect magnitude cleanly across systems. The updated mechanistic reading is the one from §4.3: the specification's effect is content-specific, not structure-specific. Memory systems supply retrieval; the specification supplies interpretive structure; the two layer additively.

---

**Raw data and scripts.** Per-system per-subject per-judge scores at `results/global_<subject>/*_judgments*.json`. The 5-judge primary recompute report is at `docs/research/memory_systems_5judge_primary.md`. The aggregation script is `scripts/compute_memory_systems_5judge.py`.

---

### 4.4.1 Letta stateful-agent path: a pointer

Letta's architecture is distinct from the other three commercial systems in one important way. Alongside the archival-retrieval path tested in the §4.4 memory-system conditions above, Letta maintains a persistent memory block that the agent self-edits during multi-turn conversation. This is the stateful-agent path from the original MemGPT design. When Letta's memory block is fed to the same response model used throughout the main study, the block scores in the prediction band as Base Layer's Behavioral Specification at matched response model on the three subjects we tested (Hamerton, Ebers, Babur). §4.7 develops this as architectural convergence on a shared interpretive-representation target, and documents the scaling ceiling we observed at the largest corpus tested.

---

### 4.5 Robustness and Sensitivity

The results in §4.1 through §4.4 could in principle reflect artifacts of the measurement apparatus rather than real properties of the Behavioral Specification. Three potential artifacts are worth testing directly: the response-model family (most main-study responses were generated by Claude Haiku 4.5), the judge panel composition (the 5-judge primary excludes the two Gemini judges), and the question generator (main-study batteries were generated by Claude Sonnet). §4.5 reports the sensitivity of the core findings to each.

---

### 4.5.1 Cross-provider response generation (Tier 2 replication)

**Concern.** The main-study response model is Claude Haiku 4.5 and the main-study batteries were generated by Claude Sonnet 4.6. If the specification's effect depends on response-model and question-generator co-tuning within the Anthropic family, the observed effect could be an artifact of within-family alignment rather than a real property of the specification.

**Test design.** Three subjects spanning the gradient were selected: Ebers (C5 = 1.02, low baseline), Yung Wing (C5 = 1.88, low baseline), and Zitkala-Sa (C5 = 2.34, mid baseline, main-study spec-null on Δ_C4a). Their behavioral-prediction batteries were regenerated from scratch by GPT-5.4 (OpenAI) from the same held-out corpus. The specification was then served to two non-Haiku response models: Claude Sonnet 4.6 (same provider family, different model) and Google Gemini 2.5 Pro (different provider entirely). The resulting 3 subjects × 2 response models = 6 (subject, response model) cells were scored by the 5-judge primary panel in the same way as main-study conditions. The question: does the spec direction reproduce when the response model is not Haiku and the battery is not Claude-generated?

**Result.** 5 of 6 cells reproduce the specification direction.

| Subject | C5 baseline | Response model | Battery generator | Δ (spec effect) | Direction matches main study |
|---|---:|---|---|---:|:---:|
| Ebers | 1.02 | Claude Sonnet 4.6 | GPT-5.4 | **+1.48** | ✓ |
| Ebers | 1.02 | Gemini 2.5 Pro | GPT-5.4 | **+1.07** | ✓ |
| Yung Wing | 1.88 | Claude Sonnet 4.6 | GPT-5.4 | **+1.91** | ✓ |
| Yung Wing | 1.88 | Gemini 2.5 Pro | GPT-5.4 | **+1.27** | ✓ |
| Zitkala-Sa | 2.34 | Claude Sonnet 4.6 | GPT-5.4 | **+1.40** | ✓ |
| Zitkala-Sa | 2.34 | Gemini 2.5 Pro | GPT-5.4 | **−0.55** | ✗ |

The one non-matching cell (Zitkala-Sa × Gemini 2.5 Pro, Δ −0.55) is consistent with Zitkala-Sa's main-study behavior. Zitkala-Sa is one of two main-study subjects where the specification does not help on Δ_C4a (§4.1 gradient table; Equiano is the other). That null is a gradient property of the subject, not a Tier 2 replication failure; the main-study result on Zitkala-Sa × Haiku is also near-null. The Tier 2 result reproduces that null rather than contradicting it.

**Direction of the finding.** The specification's effect is not a Haiku-specific or Claude-family-specific artifact. Non-Anthropic response models, reading OpenAI-generated batteries, show the same spec-effect direction on five of the six cells tested.

**Secondary observation: baseline variance across response models.** A side observation from the Tier 2 runs: C5 baseline scores on the same subject can vary by 1-2 points across response models. Different providers know different amounts about the same historical figure, independently of the behavioral specification. This is empirical support for the structural premise in §1.4: pretraining coverage of a specific person is a property of each model family, and there is no reason to expect it to be uniform. Models disagree on who they have been trained on, by roughly the same magnitude that the specification lifts prediction.

---

### 4.5.2 Judge panel sensitivity (5-judge primary vs 7-judge)

**Concern.** The judge panel could itself introduce systematic bias in favor of the Behavioral Specification. Gemini 2.5 Pro specifically failed verbatim-match calibration (§3.7.2: scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply. If Gemini inflation or another panel-level bias happened to favor spec-containing conditions disproportionately, the 5-judge and 7-judge aggregates would diverge.

**Test.** Every primary result in §4 has a 7-judge sensitivity counterpart. The question: do the 5-judge primary and 7-judge aggregate agree in direction, and if they disagree in magnitude, does the disagreement cut toward or against the paper's claims?

**Result.** The 5-judge primary is the conservative choice for every headline finding. Gemini inclusion widens spec-effect magnitudes rather than narrowing them.

| Condition | Δ vs. C5 (5-judge primary, 13 globals) | Δ vs. C5 (7-judge, same subjects) | Direction of shift when Gemini is added |
|---|---:|---:|---|
| C2a (spec alone) | +0.35 | +0.45 | widens by +0.10 |
| C2c v2 (random derangement) | +0.22 | +0.22 | unchanged |
| C2c v1 (fixed derangement) | −0.25 | −0.21 | softens by +0.04 |

The Gemini-inclusion shift in C2a's direction is driven by Gemini's relatively severe scoring of baseline (no-context) responses compared to its scoring of spec-containing responses. Including Gemini compresses the baseline ceiling more than the spec-condition ceiling, which widens the delta. The direction of the shift is the same across almost every comparison in the paper: 5-judge primary gives the lower-bound effect size, 7-judge gives a larger effect size, and no subject's improvement direction changes between them (noted in §1.2 and §3.7.2). Reporting 5-judge primary means every paper claim is the conservative version.

**Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`).** None of the paper's claims depend on the panel choice between 5-judge and 7-judge; all directional claims reproduce on either panel.

---

### 4.5.3 What these robustness checks do not address

Neither Tier 2 nor the judge-panel sensitivity escapes the LLM-class concern. Every response model in this study is a large language model; every judge is a large language model. If LLMs as a class share systematic biases that favor responses quoting behavioral-specification tag IDs (78.6% of correct-spec responses, §4.3), that class-level bias would appear in the measured effect size and neither the cross-provider response test nor the non-Gemini judge panel would fully remove it.

Tier 2 narrows the concern to "non-Haiku LLMs, reading non-Anthropic batteries, produce the same direction." The judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger. Together these results rule out several within-family artifact hypotheses but do not replace human validation on the full pipeline.

Human-judge validation on a stratified subset of responses is flagged as the priority follow-up in §8 Future Work, alongside multi-subject living-user replication. The remaining LLM-as-judge circularity is discussed directly in §6 Limitations.

---

**Raw data and scripts.** Tier 2 per-subject per-model responses at `results/_tier2/global_<subject>/`. 5-judge vs 7-judge sensitivity recompute at `docs/research/recompute_5judge_primary.md`.

---

### 4.6 Interpretation vs. Recall

§4.4's Supermemory section showed that the near-zero aggregate Δ_spec on Supermemory is not the specification doing nothing. The specification produces large improvements on some questions and large regressions on others, with roughly the same magnitude on each side; the number of regressions is slightly higher than the number of improvements, which is what produces the small negative aggregate. §4.6 documents that this pattern is not Supermemory-specific. Every memory system in the study shows the same per-question distribution: improvements and regressions of similar magnitude, with only the balance of counts shifting by system. The three mechanisms identified on Supermemory (the specification supplies a pattern retrieval cannot, the specification over-theorizes a question retrieval already answered plainly, the specification induces a refusal the content-match rubric penalizes) reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate. The most consistent specification-induced behavior across substrates is a spec-induced refusal on Keckley Q21, which produces large negative per-question Δ on any substrate where the model's baseline response was productive speculation.

---

**Per-subject paired-delta distributions: every row is a mixture of wins and losses.**

Each row below is one subject under one memory system, 39 held-out questions scored paired (C1 retrieval alone vs. C3 retrieval + specification). The aggregate Δ is the per-subject mean of those 39 paired differences. The remaining columns break that aggregate into win, tie, and loss counts at the per-question level.

| System | Subject | **Aggregate Δ** | C1 mean | C3 mean | Wins (Δ > 0.3) | Losses (Δ < −0.3) | Large improvements (Δ > 1.0) | Large regressions (Δ < −1.0) | Total Qs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mem0 | Yung Wing | **+0.35** | 2.16 | 2.51 | 21 | 12 | 7 | 1 | 39 |
| Mem0 | Keckley | **−0.01** | 2.64 | 2.63 | 14 | 16 | 1 | 2 | 39 |
| Letta (archival) | Hamerton | **+0.46** | 2.35 | 2.81 | 21 | 8 | 10 | 2 | 39 |
| Letta (archival) | Keckley | **0.00** | 2.70 | 2.70 | 11 | 15 | 3 | 2 | 39 |
| Zep | Seacole | **+0.52** | 2.27 | 2.79 | 24 | 8 | 9 | 0 | 39 |
| Zep | Keckley | **+0.10** | 2.49 | 2.59 | 16 | 12 | 5 | 3 | 39 |
| Base Layer | Yung Wing | **+0.33** | 2.23 | 2.56 | 22 | 10 | 7 | 2 | 39 |
| Base Layer | Keckley | **−0.01** | 2.44 | 2.44 | 18 | 13 | 3 | 5 | 39 |

*Table 4.6 — every row is a mixture. Even Zep's strongest row (Seacole, Δ +0.52) has 8 questions where the specification regresses by more than 0.3 points. The Mem0 Keckley row (Δ −0.01) resolves into 14 wins + 16 losses at the question level, not 39 small effects. Supermemory per-subject distributions are in §4.4 (aggregate across 13 globals: 37 large improvements, 52 large regressions, mean swings +1.45 and −1.41).*

*Note on judge panel.* The per-question counts in this table use the 6-judge mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash) from the published paired analyses. The 5-judge primary panel gives qualitatively the same per-question distribution. The aggregate Δ values match the 5-judge primary recompute to within rounding (see `docs/research/recompute_5judge_primary.md`). The mixture pattern is not judge-panel-specific.

---

**The three mechanisms from §4.4 reproduce across all five memory systems.**

The three mechanisms identified on Supermemory in §4.4 reproduce on every memory system in the paired analyses, with the relative frequency of each mechanism shifting by system. In plainer language:

- **Pattern 1 — specification supplies a pattern retrieval cannot.** The retrieval returned the relevant facts but not the interpretive pattern for how the subject processes those facts; the specification supplies that pattern and the prediction improves.
- **Pattern 2 — specification over-theorizes a question retrieval already answered plainly.** The retrieval returned a clean surface answer and the ground truth is a simple literal statement; the specification pulls the response toward interpretive depth the question does not require, and the score drops.
- **Pattern 3 — specification induces a refusal the content-match rubric cannot score as anything but wrong.** The specification's honesty or dignity axioms lead the model to decline to speculate where retrieval was insufficient; the rubric scores the refusal identically to an off-base prediction.

Representative cross-system examples of each:

- **Pattern 1 (pattern supply) on Mem0 (Ebers Q11, Δ +1.67).** C1 used the retrieved biographical facts to produce "patience and fortitude" as a generic character prediction (mean 1.83). C3 supplied the ideal-vs-reality axiom directly and predicted Ebers' specific institutional-disillusionment pattern (mean 3.50), matching the held-out *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."* The retrieval had the biography; the specification had the pattern for how Ebers processes institutional failure.
- **Pattern 2 (over-theorization) on Base Layer (Yung Wing Q31, Δ −1.33).** C1 produced a plain correct prediction: "walked on air, gratitude." C3 elaborated a theory of "gratitude as epistemology" in which the emotional register "holds multiple registers simultaneously rather than collapsing into simple triumph." The held-out is *"walked on air, and he worshipped God."* Same mechanism as §4.4 Example 2 (Yung Wing Q5 on Supermemory): the specification shifted the prediction toward interpretive depth where the surface answer was correct.
- **Pattern 3 (default-axiom overgeneralization) on Base Layer (Ebers Q1, Δ −1.00).** The held-out is an unconditional evangelical proclamation: *"Like the apostle, I would fain proclaim the gospel to all men according to the best of my powers."* C1 predicted "positively and earnestly," matching the unconditional register. C3 applied the specification's "lived particularity over abstraction" axiom and predicted "receptivity, but only if the appeal is grounded in lived particularity rather than abstract principle." The axiom is correct on average but overgeneralizes on this specific unconditional moment. Reproduces on Mem0 and Supermemory with the same mechanism.

The relative frequency of each pattern shifts across systems in a way that tracks how much of the plain answer the retrieval already supplies. Qualitatively, from the paired analyses:

- **Mem0** (atomic-fact retrieval): more Pattern 1 on interpretation-heavy questions; more Pattern 2 on literal-recall questions that the atomic facts already answer.
- **Letta archival** (retrieval with 0.34–0.47 dedup ratio, so only 3–5 unique facts in a top-10 list, documented in `mem0_letta_zep_c1_vs_c3_analysis.md`): large-magnitude Pattern 1 improvements when the few unique facts align with the specification; moderate Pattern 2 and Pattern 3 losses otherwise.
- **Zep** (temporal graph, verbose relational substrate): most favorable balance across Patterns 1–3, with the fewest large-magnitude regressions in the paired sample (0 on Seacole).
- **Supermemory** (strong embedding retrieval, highest C1 mean ~2.65): more Pattern 2 and Pattern 3 because strong retrieval more often already supplies the plain answer, giving the specification more chances to over-theorize or refuse.
- **Base Layer** (MiniLM + ChromaDB semantic-embedding neighbors): distribution similar to Mem0 and Zep; Pattern 1 on interpretation-heavy questions, Pattern 3 on refusal-triggering questions.

*This characterization is qualitative. A quantitative frequency breakdown of Pattern 1 / 2 / 3 across all 507 questions × 5 systems would require mechanism classification per response, which is flagged as a follow-up in §8. The observation that the paired analyses reproduce the three mechanisms on every system is empirical; the specific relative frequency per system is not yet quantified.*

---

**The most consistent specification-induced behavior across substrates: Keckley Q21.**

Keckley Q21 — *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"* — produces a spec-induced refusal across all five systems, with magnitude modulated by how productive the baseline retrieval response was. The held-out passage carries Keckley's interior motive for not visiting, which the training half of the corpus does not contain; no retrieval substrate can surface it. The specification's documented-dignity and intimate-authority axioms then lead the model to decline to speculate, on any substrate:

| System | C1 (retrieval alone) | C3 (retrieval + spec) | **Δ** | C1 behavior | C3 behavior |
|---|---:|---:|---:|---|---|
| Supermemory | 3.83 | 1.50 | **−2.33** | productive speculation from retrieved facts | declined to fabricate interior motive |
| Base Layer | 3.33 | 1.00 | **−2.33** | productive speculation from retrieved facts | declined, cited insufficient information |
| Mem0 | 2.00 | 1.50 | **−0.50** | already hedging from atomic retrieval | structured refusal |
| Zep | 1.83 | 1.33 | **−0.50** | already hedging from edge retrieval | structured refusal |
| Letta (archival) | 1.33 | 2.33 | **+1.00** | C1 also refused | specification's structured refusal scored higher than C1's unstructured hedge |

Different retrieval substrates, different fact pools, different baseline behaviors, identical specification; the refusal and its rubric penalty reproduce with large magnitude when C1 was productive speculation, shrink when C1 was already hedging, and invert when C1 itself refused. The Q21 refusal is a property of the specification. The rubric penalty for that refusal is a property of the rubric (§3.7.6 validity audit, §4.4 Example 3).

---

**What this means for measurement.**

Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-substrate refusal) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*. The content-match rubric scores the second; it cannot score the first. A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that rewards epistemic honesty on questions the retrieved facts cannot answer without fabrication, would recover a cleaner measurement of the specification's real effect. This is the single most impactful follow-up for the measurement framework, flagged as the priority rubric-design follow-up in §8.

---

**Raw data and scripts.** Full per-subject per-system paired distributions at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Analysis scripts at `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py`, and `scripts/analyze_sm_c1_vs_c3.py`.

---

### 4.7 Architectural Convergence: Letta Stateful-Agent

Letta is the one commercial memory system in the study whose architecture supports an alternative to retrieval at query time. Alongside the archival retrieval path tested in §4.4, Letta agents maintain a persistent memory block that the agent itself rewrites during ingestion. This is the stateful-agent design from the original MemGPT paper. It is architecturally closer to the Behavioral Specification than to retrieval-based memory: the representation is authored by the agent over the course of reading the source corpus, rather than chunked and indexed for later retrieval.

§4.7 asks: if the Behavioral Specification improves prediction because it supplies the subject's interpretive patterns in context (H3, validated in §4.3), does Letta's stateful-path representation do the same? If so, there is independent architectural validation of the target. Two systems designed from different premises would be converging on the same underlying property.

---

**Test design.** A fresh Letta agent was initialized and fed the training half of each subject's corpus turn-by-turn. The agent was allowed to self-edit its memory block during ingestion, its native MemGPT behavior. After ingestion, the resulting memory block was extracted and served as context to Claude Haiku 4.5, the response model used throughout the main study. The behavioral-prediction battery was the main-study battery. Three subjects were tested, spanning a 9× corpus-size range:

| Subject | Source corpus | Corpus size (words) | Letta block size (chars) |
|---|---|---:|---:|
| Hamerton | Philip Gilbert Hamerton, *An Autobiography* (training half) | 25,231 | 22,472 |
| Ebers | Georg Ebers, *The Story of My Life* (training half) | 48,161 | 68,413 |
| Babur | Babur, *Babur-nama* (training half) | 222,742 | 335,349 |

The direct comparison: Letta's stateful-path memory block fed to Haiku, vs. Base Layer's full-stack specification fed to the same Haiku, on the same battery and judge panel. Both are interpretive representations delivered as context; the test isolates the representation itself.

---

**Methodological note on the Base Layer condition served here.** The Base Layer side of this matched-rerun loaded the unified brief variant (a ~7K-character synthesized document served as a single artifact) rather than the full layered stack (anchors + core + predictions + brief) that §4.4's controlled and native C2a / C3 conditions use. The unified brief is more compressed on referential detail than the layered stack. A layered-stack rerun on these three subjects would likely narrow the Letta-over-BL gap; whether it narrows to parity or reverses is not measured. The Table column header below reflects this: the Base Layer side is the unified brief variant.

**Result (5-judge primary: Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).**

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Babur | 2.42 | 1.88 | **+0.54** |

On all three subjects tested, Letta's stateful-path block, served to the same response model as the Base Layer unified brief, produces a higher per-subject mean score than the unified brief. Both representations land well above the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec for these subjects: Hamerton near parity with Base Layer retrieval, Ebers +0.31, Babur near-null).

**Judge-panel robustness.** The 7-judge sensitivity aggregate (Hamerton +0.20, Ebers +0.75, Babur +0.29; see `docs/research/letta_stateful_matched_rerun.md` Part 7 appendix) preserves direction on all three subjects. The 5-judge primary values are larger than the 7-judge values on Ebers and Babur by +0.29 and +0.25 points respectively, because the two Gemini judges were inflating Base Layer scores relative to the calibrated core on those subjects. Excluding Gemini from the aggregate (the paper's 5-judge primary convention; §3.7.2 and §4.5.2) therefore widens the Letta-over-BL gap rather than narrowing it. Hamerton is the exception — 5-judge Δ +0.14 vs. 7-judge +0.20 — where Gemini inclusion slightly widened the BL side. In all three cases, the Letta-block-outperforms-BL-spec direction is stable across panels.

---

**Compression behavior: divergence at large corpora.**

Letta's memory block grew roughly linearly with source corpus size. At the largest subject (Babur), Letta's API began rejecting ingestion requests at approximately 333,000 characters. After 22 consecutive failed ingestion attempts, the final block measured 335,349 characters. Letta's declared block-size metadata limit is 100,000 characters, unenforced in practice; the effective ceiling on the server side appeared to be a different API-level limit around 333K.

At the ceiling, the block contained **25.4% verbatim sentence duplication** on Babur, compared to 0% duplication on Hamerton and 0% on Ebers. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing. The representation carries corpus-derived narrative at scale but does not preserve the compression property that makes large corpora tractable.

Base Layer's compose step keeps the full-stack specification at 34,000–40,000 characters across the same corpus-size range. At Hamerton, the two representations are the same order of magnitude in size; at Babur, the Base Layer specification is roughly one-tenth the size of the Letta block. The two systems are prediction-band compatible at small corpora; they diverge on compression at large ones.

**What the ceiling means for deployment.** Served on every query, a 335,000-character Letta block costs roughly 84,000 tokens of context. At current frontier pricing this is materially more per-query cost than the Base Layer specification's ~10,000 tokens, and it exceeds the context window on the smaller-context models still common in production (128K token windows struggle when the block alone is two-thirds of the budget, before any conversational state). The 25.4% verbatim-sentence duplication observed at the ceiling indicates the block would be functionally smaller with a deduplication pass: roughly 250,000 characters of distinct content in a 335,000-character block. Whether that extraction pass is a tractable post-processing step on the Letta side is an engineering question, not one this study measures. For production deployment, the ceiling and the duplication together argue for representation compactness as a first-class design constraint, not a nice-to-have.

---

**What the architectural convergence means.**

Letta's stateful-agent architecture was designed around a different engineering question than Base Layer's. Letta asks: can the agent itself write and revise a compact memory of the user over the course of ingestion? Base Layer asks: can behavioral patterns be extracted and encoded offline, then served as static context? The two paths differ in how the representation is produced and in when it is written. Yet both produce representations that, fed to the same response model, land in the same prediction band, and both produce representations that outperform retrieval-only context on the same subjects.

The reading: the behavioral-specification target is reachable by more than one architectural path. That is an argument for the target itself, not for any specific implementation. Where the two systems agree, the agreement is about the underlying property being measured. Where they disagree (the Babur ceiling, the magnitude at Ebers), the disagreement is about engineering choices, not about whether the target exists.

---

**Content comparison: what each representation retains.**

To test whether Letta's higher matched-model score comes from preserving original corpus text the response model could cite, we ran a post-hoc content analysis on the three subjects. The strong form of that hypothesis is refuted. Neither representation is a quote library. Checking what fraction of consecutive five-word sequences in each representation also appears verbatim in the training corpus (a standard overlap check), both representations score under 1%: the Letta block ranges 0.0–1.0% depending on subject, the Base Layer specification scores 0.0% on all three. The same check for consecutive ten-word sequences gives under 0.1% for both. Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts.

A refined version of the hypothesis does hold. The two representations differ in **referential density**: Letta's rolling summary retains roughly an order of magnitude more unique proper nouns, dated events, and named secondary characters than Base Layer's §4.7 specification (Babur: 540 vs. 46 unique capitalized named-entity tokens; Ebers: 58 vs. 19). Base Layer, by construction, compresses episodes into cross-cutting behavioral patterns with fewer surface referents; the pipeline explicitly anonymizes the subject during authoring and compresses corpus-level specifics into dimensional axioms. Letta's stateful-agent path preserves more of the referential surface while also encoding behavioral patterns.

The two systems converge on interpretive behavior — both produce responses that outperform retrieval-only context at matched response model. They diverge on referential detail. On battery items that reward specific-event recall, Letta has more named entities to cite. On items that reward principled interpretation across episodes, Base Layer's dimensional axioms compete directly. The §4.7 matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects. Flagged in §8.

Full content analysis at `docs/research/` (see `_content_analysis_results.json` and the N=3 per-subject breakdown). The methodological note on the Base Layer condition is now hoisted above the result Table at the top of this section.

---

**Caveats.**

- N = 3 subjects on this path. Extending across the full 14-subject gradient would establish the architectural-convergence claim at the population-of-relevance level, not only on a selected set of corpus sizes. Flagged in §8.
- One response model (Haiku) on both conditions. The convergence is tested at matched response model; whether it holds at other response models is an open question.
- Letta's 333K-character ingestion ceiling is a hard architectural constraint in the current release. For small corpora the two representations are interchangeable in prediction behavior; for large corpora the ceiling is material.
- Base Layer condition used the unified `spec.md` variant, not the layered stack; see content comparison above.

---

**Raw data and scripts.** Letta stateful matched-rerun data at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json`. Generation and scoring scripts live in the same directory as a numbered chain (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, `70_compute_5judge_primary.py`); see the `README.md` inside `docs/research/_letta_rerun/`. Full characterization of block content, duplication behavior, and API responses in `docs/research/letta_stateful_deep_read.md` and `docs/research/letta_stateful_matched_rerun.md`.

---

### 4.8 Scaling and Practical Implications

§4.1 through §4.7 establish what the Behavioral Specification does and why it works. §4.8 is a practical note on what deploying it in production looks like: context budget, authoring cost, per-query cost, update cadence, and how the specification positions against alternative approaches. It also documents several open design questions that follow directly from the study's findings but were out of scope to answer inside this paper.

---

**A note on what was tested versus what production would look like.** The specification form studied here is a proof-of-concept implementation: the full-stack specification is served in its entirety as a static context attachment on every query. This is the simplest possible serving strategy, chosen so the measurement isolates the representation's effect rather than serving-strategy effects. Production deployment would almost certainly not serve the specification this way. The discussion below distinguishes what the current implementation requires from what production approaches might look like.

---

**Context budget (as served in this study).** The full-stack Behavioral Specification is ~8,000–10,000 tokens and fits inside every frontier LLM's context window with headroom. On a 200K-token context model it consumes 4–5% of the window; on a 1M-token context model it consumes well under 1%. Serving the specification in full on every query is operationally tractable at current pricing. Compare: the full raw corpora in this study range from ~34K tokens (Hamerton) to ~550K tokens (Babur), with Babur exceeding most current context windows at the time of this study or incurring substantial per-query cost if served directly.

**Per-user authoring cost.** The five-step pipeline (import → extract → embed → author → compose; §3.3) runs offline, once per user. For a typical subject's training corpus (25K–100K words), the pipeline completes in minutes to tens of minutes on current API pricing, with the dominant cost being the extraction step (Haiku-class model, ~300–1,500 facts per corpus). The cost profile matches one-time onboarding overhead, not per-query overhead.

**Per-query cost (as served in this study).** At inference, the full specification is a static context attachment. No retrieval step at the specification level; no live extraction; no re-embedding. The per-query overhead is the token cost of the full specification in the prompt. On current frontier pricing, ~10K context tokens adds on the order of a cent or less per query.

---

**Dynamic activation: the likely production serving strategy.**

Serving the full specification on every query is wasteful. Most queries engage only a subset of the specification's content: a question about the user's work-style reasoning does not need the whole identity-level anchor set, only the work-style anchor plus the relevant predictive-template and a handful of retrieved facts that bear on the question. A production serving layer would plausibly activate the specification dynamically:

- Embed the incoming query.
- Retrieve the specification components (anchors, axioms, predictions) whose embeddings are closest to the query.
- Retrieve facts tied to the activated specification components through the provenance links (§3.3, §3.5).
- Serve the activated subset plus the brief as context, rather than the entire stack.

On a typical query, the activated subset would be on the order of 1,000–2,000 tokens rather than the full 8,000–10,000. The per-query cost drops by roughly an order of magnitude, and the specification's signal-to-noise ratio in the prompt improves (fewer unused axioms competing for the model's attention). Whether the dynamic activation preserves the behavioral-prediction accuracy the full-stack configuration produces is a separate measurement question, not answered by this paper. The components and their provenance links already exist; what is missing is the activation policy and a controlled measurement comparing dynamic-activation accuracy to full-stack accuracy on the same battery. Flagged in §8.

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

A production serving layer would plausibly annotate the specification with temporal metadata (timestamps on source facts, version history on anchors, weighting schemes on predictions) and have the activation policy consider recency. None of this is implemented in the current pipeline. The gradient and the mechanism findings hold for a static snapshot; whether they hold once temporality is layered in is an open question. Flagged in §8.

---

**Topic decomposition and piecewise component analysis.**

Two closely related open questions that this study does not answer but that the design raises directly:

1. **Topic decomposition.** Specifications could be organized by topic domain (work style, relationship patterns, political reasoning, health decisions, etc.) with domain-specific anchors and predictions, rather than the current unified identity-level structure. A domain-scoped serving layer would activate only the domain relevant to the query, reducing context budget further and avoiding cross-domain interference (§4.3's over-theorization pattern on technical questions). The pipeline's authoring step could be extended to produce domain-tagged layers; the serving step could route queries to the relevant domain. Flagged in §8.

2. **Piecewise component analysis.** Which layer of the specification carries the prediction signal? We did not run an ablation study. The pipeline produces anchors, core, predictions, and a brief that composes them. Whether the brief alone achieves most of the effect, whether anchors are load-bearing and predictions are decorative, or whether the full stack is necessary, has not been measured. A component-ablation study (run the same subject battery with anchors-only, core-only, predictions-only, brief-only, and in combinations) would identify which components are doing the work. The result would directly inform both the authoring pipeline's priorities and the dynamic-activation policy's weights. Flagged in §8.

---

**Update cadence.** The specification is a snapshot. For living users whose behavioral patterns evolve, re-authoring cadence is an open design question flagged in §8. The pipeline is designed to re-run incrementally: extraction on new corpus additions, re-authoring of the layers if the newer content shifts the anchors or predictions. The choice of whether to re-author on a schedule, on a corpus-size threshold, or on a detected-drift signal is a policy decision the study does not address.

---

**Positioning against alternative approaches.**

- **Per-user fine-tuning** reaches the representational-accuracy target by modifying model weights for each user. Cost profile: substantial per-user compute, per-query inference on a dedicated model, no portability across providers, opaque to the user about what has been learned. The Behavioral Specification reaches the same target via context rather than weights, with portability, inspectability, and per-user audit that weight modification does not allow.
- **Retrieval-augmented generation (RAG) alone** targets recall rather than representational accuracy. §4.1 through §4.4 show RAG alone does not close the gap on low-baseline subjects. Adding the specification on top of RAG produces additive improvement on three of four commercial memory systems tested.
- **Serving the raw corpus as context on every query** is the alternative to compression. At small corpus sizes the raw corpus is tractable; at medium to large corpus sizes it is not. §4.2 documents the 30× to 78× compression the specification achieves at modest cost to predictive signal (~0.2 points on the 1-5 rubric on the low-baseline slice).

---

**Infrastructure properties.**

The Behavioral Specification is a portable artifact. It attaches as context to any LLM call without provider-specific integration. Users can own and audit their own specifications; providers can serve them without storing the full conversation history that produced them. The representation is independent of the runtime; the same specification can be served to Claude, GPT, Gemini, or any future response model with no change.

Four infrastructure properties that do not fall out of any of the alternative approaches above:

- **User-held.** The specification is a text document. The user (or their designated custodian) can store it, move it, redact it, regenerate it from updated source material. No AI provider needs to retain the underlying corpus; the specification is sufficient to serve the user at the representational-accuracy level the study measures.
- **Inspectable.** The axioms, predictions, and narrative brief are in plain language. A user reading their own specification can identify places where the AI's model of them is wrong, and correct the source material or re-author the spec accordingly.
- **Provenance-traced.** Each axiom and prediction can be traced back to the specific source material that produced it (§3.3, §3.5). A user who wants to understand why the spec says what it does can audit the derivation.
- **Local-executable retrieval.** Base Layer's retrieval substrate (MiniLM-L6-v2 embedding + ChromaDB vector store) runs entirely on the local machine without cloud API calls for vector search or fact identification. The four commercial memory providers tested in the study (Mem0, Letta, Supermemory, Zep) all require cloud operations for retrieval. For deployments where data sovereignty, offline operation, or zero-dependency execution matter, the local-execution option is materially different from a cloud-dependent option.

These properties matter for deployment because they make the representation auditable, portable, and runnable at the infrastructure layer, not only at the application layer.

---

**Summary of practical implications.** The Behavioral Specification is compact enough to serve on every query at current pricing, cheap enough to author once per user at current extraction-model pricing, portable across response models, and inspectable by the user whose behavior it represents. These properties position the representation for production deployment patterns that fine-tuning, raw-corpus-in-context, and retrieval-alone approaches do not match on the same axes.

---

## 5. Discussion

### 5.1 What the study demonstrates

This paper is oriented to a single question: how do we improve human-AI interactions for the people who actually use AI systems? We introduced representational accuracy as the measurable AI-side property that makes those interactions possible: how faithfully an AI's internal model of a specific person captures how that person reasons. We tested it by measuring behavioral prediction on held-out text, checking whether the response model could anticipate how each subject would respond in situations drawn from passages the model had never seen, using a specification authored from the other half of the corpus.

Across 14 historical subjects, five commercial and open-source memory systems, six response models, and five primary judges, the paper produced five empirical results:

- **A compact Behavioral Specification improves prediction, inversely proportional to what the model already knows about the person** (the gradient, H1 + H2; §4.1). Regression slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, slope p < 0.001. On the nine low-baseline subjects (the operational target for product deployment on real users, whose private reasoning is not in any training corpus), every subject improved, mean Δ_C4a = +0.89 points.

- **The improvement is content-specific** (H3; §4.3). A random-derangement wrong-spec control scores near baseline (Δ +0.22); an adversarial fixed-derangement wrong-spec degrades prediction below the no-context baseline (Δ −0.25). Structured prompting alone does not produce the effect. The content of the correct specification for the correct subject does.

- **The specification composes additively with existing memory systems** (H4; §4.4). Layered on top of the four commercial memory systems tested, the specification produces positive mean Δ on three of four (Mem0, Letta archival, Zep). The fourth system, Supermemory, aggregates near zero, but the per-question analysis (§4.4, §4.6) shows this is a mixture of large improvements and large regressions that partly cancel, not a uniform null.

- **Structure compresses the predictive signal at a fraction of the context footprint** (H5; §4.2). A ~7,000-token specification recovers most of what the full raw corpus delivers at compression ratios ranging from roughly 5× (Hamerton, ~33K-token corpus) to 78× (Babur, ~550K-token corpus) by token count. The full extracted-fact set (C4, every fact loaded as context without the specification) produces a similar improvement on the low-baseline slice at a comparable footprint, so fact extraction itself is already a compression pass. The specification's marginal contribution over facts-only is smaller at the aggregate mean than the spec-versus-no-context gap suggests, and its distinct value shows up at the per-question level (§4.3, §4.6). Behaviorally relevant signal is sparse and compressible at both the fact-extraction and specification-authoring steps.

- **The target is reachable by more than one architectural path** (§4.7). Letta's stateful-agent path, designed around a different engineering premise (the agent self-edits a persistent memory block during ingestion), arrives at a representation that matches or exceeds the Base Layer specification at matched response model on all three subjects tested. Two systems designed independently, from different premises, converge on the interpretive-representation target.

The remaining subsections of §5 develop what these results imply for how AI memory systems should be evaluated (§5.2), for real users who sit outside the sample this study could run (§5.3), for the mechanism of interpretation itself (§5.4), for the specification target as a general AI-design primitive rather than a Base Layer-specific claim (§5.5), and for the measurement gaps the study does not close (§5.6).

---

### 5.2 Recall, prediction, persona: what we measure and what it isn't

AI memory evaluation today is fragmented across four distinct targets, each with its own benchmark family. None directly measures whether the AI has an accurate internal model of how a specific person reasons. **We propose behavioral prediction on held-out reasoning situations as a test of a fifth target, representational accuracy. We want to be specific about what that framing does and does not claim.**

**Prediction is the test, not the goal.** We do not pursue prediction accuracy as an end in itself. The target is representational accuracy, the fidelity of an AI's internal model of a specific person, and behavioral prediction on unseen situations is the instrument we use to measure it. A prediction score tells us the representation captured something that generalizes to new situations; a low score tells us it did not. Prediction is a diagnostic; the representation is what the pipeline is building. This distinction matters because the closest prior work on prediction benchmarks (Twin-2K) pursues prediction as its target. This paper is not positioning against Twin-2K on that target; it is measuring a different property. The two benchmarks address adjacent but distinct questions about AI personalization.

**What the held-out design actually tests.** The methodology assumes that a person's interpretive patterns are stable enough within their own corpus that patterns captured from one half reference patterns in the other. Without this assumption, held-out behavioral prediction is impossible in principle, regardless of how good the representation is. The 14 main-study subjects have coherent autobiographical narratives that support this assumption empirically: the specification authored from training text does in fact generalize to held-out text at above-baseline rates. The assumption is a constraint on what this paper measures. Subjects whose reasoning shifts substantially across their corpus (across a major career change, a profound life event, or a decades-long corpus with distinct epochs) may not be well-represented by a single snapshot specification, which is one reason temporality is a flagged follow-up (§4.8, §8). We state the assumption explicitly so that what the held-out test can and cannot diagnose is clear.

**A related open question for production deployment: canonical life events.** A person can undergo events (a major career change, a religious conversion, a significant loss, a public stance reversal) that fundamentally shift their subsequent reasoning. The main-study autobiographies were not structured to test this case. If a subject's training-half corpus contained such an event and the held-out half captured a materially different post-event pattern, a snapshot specification authored from the training half would predict the pre-event reasoning rather than the post-event reasoning, and the held-out score would read as a specification failure when the real cause is a genuine within-person behavioral shift. Whether to detect such events automatically (for example, by flagging large embedding-shift clusters in the source material), to allow the user to annotate them explicitly, or to maintain multiple versioned specifications keyed to life-phase is an open research question for production-oriented specification design. This is separate from the stability premise above and adjacent to it, and sits alongside temporality (§4.8) as a follow-up in §8.

**What recall measures, and doesn't.** LOCOMO (Maharana et al., 2024) and LongMemEval (Wu et al., 2025) measure the retrievability of specific facts from memory. A system can saturate recall on such benchmarks and still fail behavioral prediction, because retrieval answers the question "can the fact be found" rather than "does the system know how the person reasons about the fact." Recall is a necessary property for most downstream uses of memory but it is not sufficient for representational accuracy.

**What survey-response prediction measures, and why it differs from our target.** Twin-2K (Toubia et al., 2025) predicts held-out survey responses from other survey responses for 2,058 participants. The task format matches the persona format: structured responses on a Likert or numeric scale, scored by distance-based accuracy on 17 heuristics-and-biases tasks. Twin-2K's target is accurate survey interpolation. Our target is representational accuracy, measured on a cross-format task: autobiographical prose input, open-ended behavioral prediction output, rubric-based scoring against a verbatim held-out passage. An earlier exploratory run of a Base Layer specification against Twin-2K's battery produced positive results on the different task format Twin-2K measures (§2.3). We take that as a signal the specification is not task-format-dependent, but we do not hold it as a direct benchmark comparison because the two task targets are different, and the exploratory run used a prior iteration of the Base Layer pipeline. A system could perform well on Twin-2K and not on our battery (survey interpolation does not require modeling reasoning transfer to novel contexts), and a system could perform well on our battery and not on Twin-2K (accurate reasoning representation does not guarantee survey-format numerical accuracy). The two benchmarks diagnose different properties of the same general capability.

**What persona fidelity measures, and doesn't.** PersonaGym (Samuel et al., 2025) measures whether a model maintains a described persona during conversation. Persona fidelity is consistency of self-presentation over turns. Notably, PersonaGym's personas are constituted from short descriptors, typically a one-line characterization of role and a few attributes, which is a substantially shallower input than this paper's ~7,000-token specification or Twin-2K's full-text survey persona. A system that maintains a one-line persona consistently can still fail representational accuracy in two ways: the persona description itself is not rich enough to carry the interpretive patterns a specification carries, and consistency with it does not require the AI to reproduce that person's reasoning on novel situations. PersonaGym measures a useful property (holding voice over a conversation), but the input it measures against is not a deep representation of how the person reasons, so fidelity to it is a weaker condition than representational accuracy.

**What preference alignment measures, and why it is adjacent but distinct.** AlpsBench (Xiao et al., 2026) measures whether memory mechanisms improve preference-aligned and emotionally resonant responses. Their central finding, that recall improvement does not automatically carry into preference alignment, is arrived at independently and is complementary to ours. Both papers point at the same gap from different sides: solving for recall is insufficient for what memory is ultimately for. Preference alignment is an outcome property (whether a response matches what the user prefers). Representational accuracy is an upstream property (whether the AI's internal model of the user is correct). Preference alignment is one downstream consequence of representational accuracy being correct; it is not the same property.

**The missing axis.** Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to anticipate. This paper's battery is a prototype answer on that axis, not a finished benchmark. §8 flags a differentiated rubric (one that separates interpretation-heavy from literal-recall questions, and scores epistemic honesty as its own dimension) as the priority follow-up for turning this prototype into a standardized benchmark.

**Implication for future memory-system research.** A single memory-system score is underspecified. Recall, survey-response prediction, persona fidelity, preference alignment, and representational accuracy are distinct axes. A system that saturates one may do nothing on another. Production-grade evaluation of memory systems should report results on multiple axes rather than on any single one.

---

### 5.3 The population of relevance

**This paper is not a retrospective study of historical figures.** The research question is how to improve human-AI interactions for the people who use AI systems. The 14 historical subjects in the main study are experimental proxies, chosen because they enable cross-subject comparison with verifiable ground truth (the held-out half of their own autobiographies). They are not the target population. The target population is living users whose private reasoning patterns are not in any training corpus.

**Historical subjects are biased upward in pretraining coverage.** Public-domain autobiographies get digitized, indexed, and fed into LLM training. Even the least-known historical subjects in the main study (Ebers C5 = 1.02, Sunity Devee 1.03) are more present in training corpora than a typical living person whose private reasoning was never published. The bias matters for reading the study's baselines: the sample's floor is higher than the floor for real users.

**The low-baseline slice is the study's closest proxy for real users.** On the 9 subjects with C5 ≤ 2.0, the specification is uniformly positive: 9 of 9 subjects improve, mean Δ_C4a = +0.89 points, with 55% of individual responses crossing a rubric-integer anchor upward. The pattern holds where we would expect it to hold for real users: when the AI knows little about the subject from pretraining, the specification fills in.

**The paper author's own pilot confirms the extrapolation for a single real user.** §4.1.2 reports a methodology-matched run on the author's private corpus: C5 = 1.03 (the floor of the rubric, below every historical subject in the main study), Δ_C4a = +2.00 (the largest improvement observed in the study). This is a single living subject and cannot establish a population-level claim, but it is the only data point in the study on a person who actually uses AI. The result is consistent with the gradient: the population the model knows the least about is the population where the specification has the largest effect.

**What we did not prove.** A multi-subject living-user replication is the most important follow-up this paper flags (§8). Without it, the extrapolation from 14 historical subjects plus 1 author pilot to "real users in general" rests on a structural argument: private reasoning is not in any training corpus, so pretraining cannot close the gap, so a user-supplied representation is required. The structural argument is strong but not a substitute for the empirical replication, and we are careful not to present this paper as more than what it measured.

**The infrastructure implication.** If the population of relevance for AI personalization is everyone who uses AI, and every such user sits in the low-baseline band because their private reasoning is structurally absent from training data, then representational accuracy is not an enhancement for edge cases. It is a structural requirement for personalization at all. Either each user supplies their own representation to the AI systems that serve them, or personalization remains surface-level: style, voice, preference, not how the person reasons. The Behavioral Specification is one implementation of user-supplied representation. The architectural convergence result in §4.7 indicates it is not the only possible one. Some implementation of user-held, user-inspectable, user-modifiable representation is a prerequisite for AI that can act on behalf of a specific person rather than on behalf of a population aggregate.

---

### 5.4 Content specificity and mechanism

**H3 stated.** The benefit of the Behavioral Specification comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

**H3 is directly tested by the wrong-spec controls.** Random derangement (C2c v2, each subject receives some other subject's specification at random) scores near baseline at +0.22 on the 13 global subjects. Adversarial fixed derangement (C2c v1, each subject paired with a culturally and temporally distant other by design) drops prediction below baseline at −0.25. The correct-specification-for-correct-subject effect is +0.35 on the same 13 subjects. Structured prompting without the right content does not produce the improvement, and sufficiently mismatched content actively degrades prediction. Content specificity is a necessary condition, not an optional property.

**The three mechanisms (Pattern 1, Pattern 2, Pattern 3) are not alternatives; they are simultaneously present in every aggregate Δ_spec.** §4.3 identified three mechanisms that together generate the correct-spec effect; §4.6 showed they reproduce across all five memory systems tested. An aggregate Δ_spec is the weighted sum of their per-question contributions.

- **Pattern 1, pattern supply.** When retrieval returns biographical facts but not the interpretive pattern for how the subject processes them, the specification supplies the pattern. This is what produces the large-magnitude improvements on low-baseline subjects (§4.1 Example A, §4.3 Example 1, §4.4 Supermemory Example 1). Pattern 1 drives most positive per-question swings.
- **Pattern 2, over-theorization.** When retrieval already returns the plain answer and the ground truth is a surface-level statement, the specification shifts the response toward interpretive depth the question does not require (§4.4 Supermemory Example 2, §4.6 Yung Wing Q31). Pattern 2 drives most negative per-question swings on literal-recall questions.
- **Pattern 3, structural refusal.** When retrieved facts do not cover the interior motive a question asks about, the specification's dignity or epistemic-honesty axioms lead the model to decline to speculate. The content-match rubric then scores the principled refusal identically to a wrong guess (§1.3 Keckley Q21, §4.4 Supermemory Example 3). Pattern 3 drives the sharpest negative swings on this class of question.

**The three patterns together imply dynamic spec activation is a requirement for production response quality.** Pattern 1 (pattern supply) helps when retrieval is thin on interpretive structure. Pattern 2 (over-theorization) hurts when retrieval already has the plain answer. Pattern 3 (structural refusal) hurts when the specification's honesty axioms fire on questions where retrieval was insufficient. Serving the full specification on every query, as this study did, subjects every question to all three mechanisms regardless of which one is appropriate for the query. A production serving layer should decide per-query which components of the specification to activate, based on the query type and on whether retrieval already supplied the surface answer. Without dynamic activation, the specification can make responses worse as often as it makes them better, which the Supermemory mixture (§4.4) documents at the per-question level. The dynamic-activation proposal in §4.8 is therefore not a nice-to-have for performance optimization. It is a requirement for ensuring that the specification's effect on any given response is net positive.

**Specification design is a multi-objective problem.** A richer axiom set enables more Pattern 1 (pattern-supply) improvements, but it also produces more Pattern 2 (over-theorization) and Pattern 3 (refusal) regressions. A sparser axiom set produces fewer Pattern 1 opportunities, but also leaves the specification less likely to get in the way when the retrieved facts already contain the direct answer. The design is a tradeoff, not a single quantity to maximize. The piecewise component analysis flagged in §4.8 (remove axioms one by one, measure effect per question type) is the empirical way to resolve where the optimum sits for a given deployment and user population.

**Content specificity implies specification authoring is not template-based.** H3's finding that generic structured prompting does not substitute for correct-content specification directly implies that specification authoring is a subject-specific process, not a pattern that can be filled from slots. This is consistent with the pipeline's design: facts are extracted from the subject's own corpus; anchors, core, and predictions are authored from those facts; the brief composes them into a narrative specific to the person. A Base Layer "spec template" with generic slots would not reproduce the effect. The content has to come from the person.

**The Keckley Q21 result: one question where every memory system produced the same spec-induced refusal.** Keckley Q21 asks how Elizabeth Keckley explains her decision not to visit her mother's grave despite having the opportunity. The answer turns on Keckley's interior motive, which only appears in the held-out half of the corpus. No retrieval substrate can surface it because it is not in any retrievable fact pool. On all five memory systems tested, when the specification was added on top of retrieval, the response model declined to speculate about Keckley's interior motive, citing the specification's dignity and epistemic-honesty axioms. On the two systems where retrieval alone had produced a productive speculation (Supermemory C1 = 3.83, Base Layer C1 = 3.33), the specification-added response received an identical −2.33-point penalty from the content-match rubric. On the systems where retrieval alone had already hedged, the penalty was smaller. On the one system where retrieval alone had also refused (Letta archival), the specification's structured refusal scored higher than the unstructured retrieval-only refusal.

The reading: the refusal is caused by the specification and how the response model interprets it, not by any specific memory system's retrieval. The rubric penalty is caused by the rubric's design (content-match scoring cannot distinguish principled refusal from wrong prediction), not by the specification. These are three separable layers: specification (what content is supplied), retrieval (what facts are accessible), and rubric (how responses are scored). The Keckley Q21 result is evidence that we have correctly located Pattern 3 at the specification layer, because it reproduces identically across five different retrieval architectures.

**What the mechanism reading leaves open.** We did not run component ablation (anchors-only, core-only, predictions-only, brief-only, and combinations). Which layer of the specification carries Pattern 1 (pattern supply) improvements, which contributes to Pattern 2 (over-theorization) regressions, and which triggers Pattern 3 (structural refusal) is not measured. §8 flags this as the priority authoring-pipeline follow-up. Answering it would directly inform where to invest the authoring pipeline's capacity and how to structure dynamic activation (§4.8) to serve the right components for the right query types.

---

### 5.5 Architectural convergence

**The convergence shown in §4.7 is evidence for the target, not for any specific implementation of it.** Letta's stateful-agent path, designed around a different engineering premise from Base Layer's pipeline, arrives at a representation that matches or exceeds Base Layer's specification at matched response model on all three subjects tested. When two independently-designed systems produce similar prediction quality via different engineering paths, the convergence is about the property both systems target, not about the engineering choices either of them made.

**Explicit positioning: Base Layer is one implementation, not the correct implementation.** This paper does not position Base Layer as uniquely capable or as the best available implementation of the behavioral-specification target. Base Layer is one implementation of that target. Letta's stateful-agent path is another. Other implementations exist or will exist, and we would expect them to. What the convergence indicates is that the target itself (a compact, interpretive representation of a specific person's reasoning patterns, produced by processing their corpus) is an AI-design primitive that multiple engineering approaches can reach.

**Where the two implementations diverge is informative.** Base Layer's pipeline is extract-and-transform: facts are extracted from the corpus, layered into anchors, core, and predictions, then composed into a unified brief. Letta's stateful-agent path is accrete-and-edit: the agent reads the corpus turn-by-turn and self-edits a rolling memory block. The two paths differ on three observable axes:

- **Compression.** Base Layer's compose step keeps the specification at roughly 34,000 to 40,000 characters regardless of corpus size. Letta's block grows roughly linearly with source corpus size and hits an API-level ceiling around 333,000 characters on the largest corpus we tested (§4.7 scaling discussion).
- **Referential density.** At comparable compression, Letta's block retains roughly an order of magnitude more unique proper nouns, dated events, and named secondary characters than Base Layer's unified spec (Babur: 540 vs. 46 unique named entities; Ebers: 58 vs. 19). Base Layer's authoring pipeline deliberately anonymizes the subject and compresses corpus-level specifics into cross-cutting behavioral axioms; Letta's self-editing retains more of the referential surface (§4.7 content comparison).
- **Update model.** Base Layer re-authors offline when the corpus changes. Letta edits in place during ingestion, which is closer to how a human re-narrates their own history as new events occur.

These are design choices, not defects. A production system could plausibly combine Base Layer's compose-step compression with Letta's referential retention and neither system as currently designed captures both properties simultaneously. The divergence axes are the space in which future behavioral-specification implementations will differentiate.

**A constraint on what the paper can claim.** Because the target is reachable by multiple paths, no paper on this axis can reasonably claim that its implementation is uniquely capable of reaching it. What this paper does claim is: we defined the target (representational accuracy); we documented one implementation that reaches it (the Base Layer pipeline); we measured the gradient, mechanism, and composition empirically; and we report one independent architectural validation (Letta stateful-agent) that raises the confidence the target is a real AI-design primitive rather than a pipeline-specific artifact. The next paper on this axis may document a third implementation. We would expect it to.

**What would strengthen the convergence result.** The §4.7 matched-rerun tests three subjects on one response model against one version of Letta's stateful-agent stack. Extending across the full 14-subject gradient, across additional response models, and against a future Letta release or a separate stateful-agent implementation would turn the current suggestive result into a stronger claim about the target's reachability. Flagged in §8 alongside the multi-subject living-user replication.

---

### 5.6 What the study does not settle

The paper demonstrates what §5.1 summarizes, and it does not demonstrate the following. Each open item maps to a §8 follow-up.

**Framing: read for directionality, not precision.** The study's aggregate numbers should be read as evidence of directional effects (the specification helps more where baseline is lower, wrong-spec hurts more than random derangement, the advantage widens on less-known subjects, etc.) rather than as precision estimates with narrow error bars. The measurement apparatus has known limitations that affect exact numeric values more than they affect directions: the rubric's non-response-versus-response boundary is imperfect, the question batteries were backward-designed but not hand-curated for quality or distribution, and the rubric was not systematically human-reviewed on every scored response. A reader should take a +0.89 mean improvement on the low-baseline slice as strong evidence that the specification helps more where baseline is lower, not as a claim that the effect size is exactly 0.89 points. The follow-ups in §8 are organized around the measurement work that would turn directional results into precision results.

**Multi-subject living-user replication.** The most important gap. 14 historical subjects plus one author pilot is not a population-level claim about living users. The structural argument in §5.3 (private reasoning is not in any training corpus, so pretraining cannot close the gap) is strong but rests on an extrapolation that empirical replication would test directly. This is the leading §8 follow-up.

**Rubric validity.** The content-match rubric has three documented limitations the paper uses but does not close. First, it cannot distinguish a principled refusal (the response model declines to fabricate interior motive on a question where the retrieved facts are insufficient) from an off-base wrong prediction; both score at the rubric floor. The direction of bias this introduces is paper-favorable: the true spec effect on interpretation-heavy questions is slightly larger than the reported aggregate (§3.7.6). Second, in post-hoc spot-check review we found instances where non-responses (verbose hedging, adjacent-fact recitation without committing to a prediction) were scored as partial responses rather than at the floor, likely because length-sensitive judges read the verbosity as engagement (§3.7.6 length-score correlation r = 0.604 within C5 baseline only; 9.4% of abstention-pattern responses inflated above a score of 2.0). Third, we did not systematically curate the backward-designed questions for quality, and we did not hand-review whether the rubric was reasonably applied on every scored response. A differentiated battery that separates interpretation-heavy from literal-recall questions, a scoring dimension that rewards epistemic honesty as its own property, a curated question set, and a human-validated subset of rubric applications together constitute the measurement-track follow-up flagged in §8.

**Component ablation.** The specification has four authored layers (anchors, core, predictions, brief) plus the underlying fact set. Which layer carries Pattern 1 (pattern supply) improvements, which contributes to Pattern 2 (over-theorization) regressions, and which triggers Pattern 3 (structural refusal) is not directly measured. The Twin-2K exploratory run (§2.3) offers one proxy: a compressed specification variant served on a different task format produced positive results against a no-context control on the same response model, indirect evidence that at least one layer of the specification carries predictive signal on its own. That is a single-condition comparison on a different benchmark, not a controlled per-layer ablation, and it cannot identify which components contribute to which mechanism. A proper ablation on the main-study battery (serve each layer alone, serve combinations, measure Pattern-1/Pattern-2/Pattern-3 distributions per combination) would identify which parts of the pipeline are doing the work. Answering this would directly inform both the authoring pipeline's investment priorities and the dynamic-activation policy's weights. Flagged in §8.

**Production deployment gap.** The study served the full specification statically on every query, which is the simplest possible serving strategy and not a production-realistic one. Dynamic activation (per-query component selection), modifiability (user-editable text with provenance propagation), temporality (timestamps, recency weighting, versioned specifications), canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts), and topic decomposition (domain-scoped anchors and predictions) are all untested. The gradient and mechanism findings hold for the static snapshot; whether they hold under production serving is a measurement gap, not an answered question. All flagged in §8.

**LLM-as-judge circularity.** Tier 2 cross-provider replication (§4.5.1) addresses within-provider circularity: five of six non-Haiku cells reproduce the direction with non-Anthropic batteries and non-Anthropic response models. Class-level LLM-as-judge circularity remains. A human-judge validation on a stratified subset of responses is the natural follow-up. Flagged in §8.

**Sample constraints.** Fourteen historical subjects is a sample, not a population. The sample is biased upward on pretraining coverage (§5.3). One dominant response model (Haiku) was used for main-study response generation; six response models appear across robustness conditions but coverage is not uniform. One version of Letta's stateful-agent stack was tested on N=3 subjects. These constraints bound the generalizability of the claims to the specific conditions measured.

**Base Layer pipeline variations.** The Letta stateful comparison in §4.7 served Base Layer's unified `spec.md` variant rather than the full layered stack (anchors + core + predictions + brief) used in §4.4's controlled and native conditions. A layered-stack rerun on the Letta matched-rerun subjects would likely narrow the Letta-over-Base-Layer gap; whether it narrows to parity or reverses is not measured. Flagged in §8.

**What the open items collectively imply.** The study demonstrates a measurable representational-accuracy effect with specific empirical contours, validates the target architecturally, and documents one implementation. It does not demonstrate that this implementation is best, that the effect reproduces on every living-user corpus, that the measurement rubric is uncontested, or that production-realistic serving strategies preserve the measured effect. The research agenda in §8 is organized around turning these open items into tractable follow-up experiments.

---

## 6. Limitations

The paper's claims are bounded by four axes of constraint on the experimental setup: the subject sample (§6.1), the measurement apparatus (§6.2), the pipeline and specification stability (§6.3), and the scope of exploration (§6.4). Each is a permanent caveat on how the paper's results should be read, distinct from the open research questions catalogued in §5.6 and the follow-up experiments proposed in §8.

### 6.1 Subject sample

The 14 main-study subjects are a selected sample, not a population. Two sample-level points (pretraining-coverage bias and the single-living-subject constraint) are load-bearing for the paper's framing and are developed in §5.3; this subsection covers four remaining external-validity caveats that §5 does not address.

**Public-domain selection.** All subjects are historical figures whose autobiographies or memoirs are in the public domain and have been digitized by Project Gutenberg or Internet Archive. That selection pipeline is biased toward canonical texts, toward figures whose writing was preserved in published form, and toward Western publishing traditions. The paper's cross-continent spread (Saint Augustine, Babur, Fukuzawa Yukichi, Sunity Devee, Zitkala-Sa, Olaudah Equiano, Mary Seacole) partially mitigates but does not remove this bias.

**Self-presentation bias.** Autobiography is authorial self-curation. What each subject chose to include in their memoir is not a neutral record of their behavior; it is a self-selected narrative that may over-represent behavioral patterns the author wished to be remembered for and under-represent patterns they chose to leave out. Behavioral-prediction batteries derived from autobiography inherit this bias, and neither the pipeline nor the rubric has a mechanism to correct for it.

**Translation artifacts.** Three subjects' corpora are English translations of non-English originals (Augustine's *Confessions* from Latin, Babur's *Babur-nama* from Chagatai Turkic via Persian, Cellini's autobiography from Italian). Translations introduce stylistic and register shifts that the extraction pipeline processes as if they were original text. A specification authored from a translated corpus may inherit translator choices in addition to the subject's actual patterns.

**Era.** The oldest subject is 4th to 5th century (Augustine); the newest is early 20th century (Zitkala-Sa, Sunity Devee). Reasoning patterns in modern work contexts, contemporary family structures, technical or digital-native domains, and late-20th-century cultural frames are not sampled. Whether the gradient holds when specifications are authored from modern-era corpora is a generalization the study cannot make from its sample alone.

Taken together, these four caveats mean the paper's results should be read as evidence for the claims at the conditions tested. Generalization across era, source language, self-presentation mode, and digital-versus-analog source material requires follow-up experiments.

---

### 6.2 Measurement apparatus

The rubric limitations and class-level LLM-as-judge circularity are in §5.6. What follows covers the remaining measurement-apparatus constraints on how the paper's numbers should be read.

**Response-model coverage.** The main-study response model is Claude Haiku 4.5. We ran initial testing across six response models (Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4; Gemini 2.5 Pro) in the §4.5.1 Tier 2 cross-provider replication. The specification-effect direction reproduced on 5 of 6 (subject, response-model) cells with non-Anthropic response models reading GPT-5.4-generated batteries. The direction is therefore established across response-model families. The absolute magnitude of the spec effect as reported throughout §4 is Haiku-specific, and cross-model coverage in the main-study conditions (not only the robustness run) was not full. The paper's aggregate numbers should be read as what the specification does with Haiku; other response models may produce different absolute magnitudes while preserving the gradient.

**Prompt-phrasing ambiguity.** The authoring pipeline prompts, the response-generation prompts, and the judge prompts all depend on specific word choices, ordering, and phrasing. We did not systematically test prompt sensitivity. Different wordings at any of these stages could produce different numeric results, different extracted fact sets, or different judge scores on the same response. The paper's claims are downstream of the specific prompts used throughout the study (documented in the public repository scripts); we make no claim about prompt invariance.

**Inter-judge calibration variance.** Pairwise Spearman ρ across judges is 0.89 to 0.98 (§3.7.4), so the rank order of conditions is stable across the panel. Absolute-score calibration varies (§3.7.2): Gemini Pro fails verbatim-match calibration (4.15 where calibrated judges score 5.0), Opus runs lenient on abstentions (1.41 mean where Sonnet runs strict at 1.14), and length-sensitivity differs across judges. The 5-judge primary aggregate is therefore a stable reading of direction but a panel-specific reading of magnitude. A different judge panel would produce different aggregate numbers while preserving the direction of every claim, which is part of why §5.6 frames the paper as directional rather than precise.

---

### 6.3 Pipeline and specification stability

The serving-strategy gap (static full-stack attachment versus production-realistic dynamic activation) is in §4.8 and §5.6. What follows covers pipeline-internal constraints on how the paper's results should be read.

**Pipeline version tested.** The specifications used in this study were produced by the current pipeline version, which we consider stable. The pipeline has evolved through development, and different pipeline versions produce different specifications on the same source corpus. The paper's results are specific to the pipeline version tested, and the study does not measure how the gradient shifts under earlier or later pipeline versions.

**Specification stability under the same pipeline version.** Running the same pipeline twice on the same corpus at temperature 0 does not produce identical specifications. In a stability check, two runs match verbatim on roughly 45% of the resulting text and produce semantically similar but textually different content on the remainder. This is an artifact of LLM sampling and of the multi-step authoring pipeline: small divergences at the extraction or authoring steps propagate through downstream composition. Run-to-run behavioral-prediction scores sit in the same band when tested on the same battery, so the direction of any finding is stable, but the reported magnitudes are specific to the particular specification authored for this study. A replication of the paper's results on a newly authored specification for the same subjects would likely produce numerically different per-subject scores while preserving the gradient.

**Pipeline model choices were not varied systematically.** The pipeline uses Claude Haiku for extraction, all-MiniLM-L6-v2 for embeddings, Claude Sonnet for layer authoring, and Claude Opus for the compose step (§3.3). These model choices were not varied across the study. Different models at any step could produce different specifications: a different extraction model could surface different facts, a different embedding model could change retrieval behavior, a different authoring model could produce differently-structured anchors and predictions, a different composition model could synthesize the layers differently. Extending model support for each pipeline step, and measuring the gradient under alternate pipeline configurations (for example GPT-5.4 extraction, OpenAI embeddings, a non-Anthropic authoring model), is a direct follow-up flagged in §8.

---

### 6.4 Scope of exploration

Not every experimental combination was run. Main-study coverage prioritizes the conditions and subjects central to H1 through H5 (§4.1 through §4.4). Robustness and ablation conditions were added selectively rather than exhaustively.

**Coverage across the experimental grid.** The study's conditions span six response models, 14 subjects, 11 conditions (C1 through C9 plus two wrong-spec variants), and five primary judges plus two sensitivity judges. Running every possible combination (roughly 6,500 separate cells) was not attempted. Coverage was prioritized on the main-study conditions for all 14 subjects on the 5-judge primary panel, and on the Tier 2 cross-provider conditions for three subjects (§4.5.1). Ablation-adjacent conditions (per-layer spec serving, alternate pipeline model choices, dynamic activation policies) were not run at all.

**Letta stateful-agent exploration.** Letta's stateful-agent architecture is distinct from the archival retrieval path the other three commercial systems use (§4.4, §4.7). Testing the stateful path required a different evaluation harness (§4.7 test design), and that work pulled us partially outside the main-study scope. The resulting comparison covers three subjects (Hamerton, Ebers, Babur), one Letta version, and one response model (Claude Haiku). Extending the stateful-agent comparison across the full 14-subject gradient, across additional response models, and against future Letta releases is flagged as a follow-up in §8.

**Twin-2K is prior work, not a condition of this study.** Twin-2K (§2.3) appears in this paper as prior work that measures a related but distinct property (survey-response prediction rather than representational accuracy, §5.2), and as proxy evidence for the specification's signal on a different task format (§5.6 component ablation). It was a separate study on a different battery and scoring rubric. We did not run it as a condition of the main behavioral-prediction battery and do not report it as a benchmark result.

---

## 7. Behavioral alignment and safety alignment

**Two separate priorities.** AI safety research and AI behavioral-alignment research sit on different axes. Safety alignment targets whether an AI system operates within acceptable behavioral constraints regardless of whose instructions it is following. Behavioral alignment targets whether an AI system's actions correspond to how a specific person would reason and act on their own behalf. A system can be safety-aligned without being behaviorally aligned with any given user (it acts reasonably, but not the way that user would act); a system can be behaviorally aligned without being safety-aligned (it acts exactly the way a specific user would act, including if that user's actions would harm third parties). Both axes matter for broad AI deployment into everyday use. Neither substitutes for the other, and neither should be treated as a hierarchy over the other.

**Where the two axes bleed together.** The work required to measure representational accuracy overlaps with the work required to measure understanding-of-user. If behavioral prediction on held-out reasoning situations is a proxy for how well an AI's internal model of a specific person matches that person's actual reasoning, that proxy is also informative about the AI's capacity to understand what a user wants in safety-relevant contexts. The specification-induced refusal cases documented in §4.3 and §4.6 are a concrete example: the response model declined to speculate about interior motive on a question where retrieved facts were insufficient, citing the specification's epistemic-honesty axioms. That behavior is a property of representational accuracy and also reads as safety-relevant restraint. The reverse is also true. An AI trained with strong safety constraints but a weak model of the user it is serving will misread context in ways that are both behaviorally wrong and safety-degrading. Methodology and findings in one axis inform the other.

**An open research question: specifications for users with malicious intent.** The specifications in this study were authored from public-domain autobiographies of subjects who were not selected for their behavior on a benign-to-malicious spectrum. The study does not cover what a behavioral specification for someone with malicious intent would look like, or what happens when an agent is deployed on that user's behalf with such a specification active. Separate from the narrower case of a user deliberately misleading the authoring pipeline about their own patterns (which the study also does not address), the distinct question is what the representation of a malicious user's actual reasoning patterns would contain, and whether an agent serving that user at high representational accuracy would thereby inherit those patterns in ways current safety frameworks do not catch. This is a direct point of contact between behavioral alignment and safety alignment, and we consider it one of the significant open research questions the specification framework raises. Developing test methodology for this case, and measuring whether existing safety frameworks compose cleanly with representation-accurate agents deployed across the benign-to-malicious user spectrum, is flagged as a follow-up in §8.

---

## 8. Future Work

Every section of this paper flags at least one follow-up. This section consolidates them into a research agenda organized by theme.

### 8.1 Measurement methodology

The most impactful measurement follow-up is replacing the content-match rubric with a differentiated battery that separates interpretation-heavy from literal-recall questions and scores epistemic honesty as its own dimension (§3.7.6, §5.6). Alongside this: a curated question set with explicit quality control on the backward-design process (§5.6), a human-validated subset of rubric applications to test whether the rubric was reasonably applied per-response (§5.6), and human-judge validation on a stratified subset of responses to address class-level LLM-as-judge circularity (§4.5.3, §5.6). Prompt-sensitivity testing across the authoring, response-generation, and judging stages (§6.2) is a separate measurement-stability follow-up that becomes important once the rubric itself is stabilized.

### 8.2 Subject and corpus expansion

A multi-subject living-user replication is the leading follow-up for the entire paper (§5.3, §5.6). The paper's findings depend structurally on an extrapolation from 14 historical subjects plus one author pilot to living users in general; replicating the gradient with multiple living subjects (with proper consent and privacy infrastructure) turns the structural argument into an empirical one. Three related expansions: modern-era corpora (to test whether the gradient holds when specifications are authored from contemporary writing rather than pre-20th-century autobiography, §6.1), non-English original sources (to remove translation artifacts, §6.1), and alternative testbeds that isolate reasoning structure without requiring private data, such as U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted (§5.3).

### 8.3 Specification design and composition

Component ablation on the authored layers (anchors, core, predictions, brief) is the priority authoring-pipeline follow-up (§4.8, §5.4, §5.6). Serving each layer alone and in combinations, measuring Pattern 1 / Pattern 2 / Pattern 3 distributions per configuration, would identify which parts of the pipeline are doing which work. Answers inform both the authoring pipeline's investment priorities and the dynamic-activation policy's weights.

Alongside component ablation: alternate pipeline model choices (extraction, embedding, layer authoring, composition) to measure sensitivity to specific LLM choices at each pipeline step (§6.3); a Base Layer referent-variant that retains named entities inside the same dimensional scaffold, to isolate whether the §4.7 Letta-over-Base-Layer gap is driven by referential vocabulary or by the self-editing process itself (§4.7, §5.5); and a layered-stack Letta rerun on the matched-rerun subjects, which would likely narrow the §4.7 gap (§4.7, §5.6).

### 8.4 Production serving and infrastructure

The study served the specification statically and in full on every query. Five production-realistic serving-layer follow-ups follow directly from §4.8: dynamic activation (per-query component selection plus measurement against full-stack accuracy), modifiability affordances (user-editable text with provenance propagation), temporality handling (timestamps, recency weighting, versioned specifications), canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts, §5.2), and topic decomposition (domain-scoped anchors and predictions with domain-scoped serving). Each is a measurement question in its own right: whether the gradient, mechanism, and composition findings hold under each production serving strategy.

### 8.5 Architectural convergence and alternative implementations

The §4.7 Letta stateful-agent comparison is N=3 subjects on one Letta version and one response model. Extending across the full 14-subject gradient, across additional response models, and against future Letta releases would turn the current suggestive result into a stronger claim about the target's reachability (§5.5). Additional architectural paths worth testing against the same target include agent-edited persistent memories outside the MemGPT family, fine-tuned per-user models that expose their internal representation for audit, and hybrid architectures that combine offline-extracted specifications with online self-editing.

### 8.6 Safety-alignment integration

The open question §7 raises (what does a behavioral specification for a user with malicious intent look like, and how do existing safety frameworks compose with representation-accurate agents acting on behalf of users across the benign-to-malicious spectrum) is where this paper's framework touches most directly on AI safety research. Test methodology for this case, and controlled experiments on safety-framework composition, are the concrete next steps. This is a collaboration space with AI safety researchers rather than a single-lab experimental extension.

---

*Paper body complete. Abstract to be written last.*
