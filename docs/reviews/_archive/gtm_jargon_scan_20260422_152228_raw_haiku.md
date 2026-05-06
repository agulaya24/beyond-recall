# GTM/Jargon Scan Raw Haiku Outputs (20260422_152228)

Model: `claude-haiku-4-5-20251001`  |  temperature 0.2  |  max_tokens 8000

Paper: `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v8_draft.md`

---

## Chunk: §1 Introduction (1.1–1.5)

# Register Review: §1 Introduction

## Marketing Register Flags

[§1.1] "Optimizing further on recall leaves something more fundamental unmeasured." -> "Optimizing further on recall does not address how individuals process information." | Vague-strength descriptor ("fundamental") used to oversell the gap; "unmeasured" is imprecise.

[§1.1] "Memory is deeply personal." -> "Memory varies by individual." | Marketing-register personification; academic prose avoids this rhetorical move.

[§1.1] "For an AI memory system to serve a specific person, it must be personalized to how that person interprets, not just to what facts they have produced." -> "Effective personalization requires modeling interpretation, not only fact retrieval." | "Serve" is pitch-deck language; reframe as functional requirement.

[§1.1] "It is a distinct property of the AI system, and the benchmarks current memory systems are evaluated on do not isolate it." -> "Current benchmarks do not isolate this property." | Implied criticism ("do not isolate") is softer than stating what they measure instead.

[§1.1] "**The core hypothesis of this research is that representational accuracy predicts alignment between an AI system's behavior and the intent and behavior of the person it serves.**" -> "The hypothesis is that representational accuracy correlates with behavioral alignment." | "Core," "predicts," and "serves" are pitch-deck framing; "correlates" is more precise for the causal claim being tested.

[§1.2] "The five hypotheses map directly to §4" -> "The five hypotheses correspond to sections in §4" | "Map directly to" is informal/marketing phrasing.

[§1.2] "This secondary outcome is a scale-free, directly interpretable measure of the **breadth of benefit** of a context condition." -> "This secondary outcome is scale-free and directly interpretable." | "Breadth of benefit" is vague marketing language; let the metric speak for itself.

[§1.2] "Running in parallel across both splits is the Behavioral Specification, tested alone and layered on top of each configuration." -> "The Behavioral Specification was tested in isolation and in combination with each configuration." | "Layered on top" is informal; "in combination with" is clearer.

[§1.3] "**The less the model already knows about a person from pretraining, the lower the baseline, the more the specification helps.**" -> "Specification benefit is inversely proportional to pretraining coverage." | Repetitive phrasing; condense to the relationship.

[§1.3] "**The improvement is content-specific rather than format-driven, and the specification layers additively on every commercial memory system we tested, most strongly on that slice.**" -> "The improvement depends on specification content, not format, and adds to each commercial system's performance." | "Layers additively" is jargon; "adds to" is clearer. "Most strongly on that slice" is vague.

[§1.3] "**In plain terms: a compact specification of roughly 5,000-8,000 tokens predicts behavior more accurately than the full raw source it was derived from, using a small fraction of the context. Information availability is not the bottleneck; interpretive structure is.**" -> "A 5,000–8,000 token specification achieves higher behavioral prediction accuracy than the full source corpus at one-fifth the context size." | "In plain terms" is condescending; the second sentence uses marketing-register metaphor ("bottleneck"). State the finding directly.

[§1.3] "**Mechanism: content, not format.**" -> "Content determines the effect, not format." | Headline phrasing is marketing-register.

[§1.3] "**The improvement comes from the right content for the right person. Any structured prompt is not enough; only the correct specification for the correct subject produces the effect.**" -> "The improvement depends on specification-content match. Structured prompting alone does not produce the effect." | Repetition and emphatic phrasing ("right content for the right person") are marketing-register.

[§1.3] "Specifications are anonymized by design (§3.3), so the 60.6% is a lower bound on content-grounded detection: the model is inferring the mismatch from interpretive content signals such as temporal markers, cultural domain, and life events described in the spec, not from surface name cues." -> "Specifications are anonymized, so the 60.6% rate represents detection from interpretive signals (temporal markers, cultural domain, life events) rather than surface cues." | "Lower bound on content-grounded detection" is wordy; simplify.

[§1.3] "**Additivity: the specification layers on three of four commercial memory systems.**" -> "The specification improves three of four commercial memory systems." | "Layers on" is jargon.

[§1.3] "**Adding the specification on top of a commercial memory system improves its behavioral prediction on three of the four systems we tested.**" -> "The specification improves behavioral prediction on three of four systems." | "On top of" is informal.

[§1.3] "One-line per-system read:" -> "Summary per system:" | "One-line read" is marketing-register shorthand.

[§1.3] "**Mem0**: most reliable baseline. Positive spec delta in both configurations (+0.12 controlled, +0.33 native). Layers cleanly." -> "Mem0 shows consistent improvement across configurations (+0.12 controlled, +0.33 native)." | "Most reliable baseline" is vague; "layers cleanly" is jargon.

[§1.3] "**Letta**: architecturally most ambitious." -> "Letta has a distinct architecture." | "Most ambitious" is marketing language.

[§1.3] "We read this as architectural validation of the interpretive-structure claim, not as two contradictory findings" -> "This suggests the interpretive-structure hypothesis is supported by two independent architectural paths." | "We read this as" is informal; "architectural validation" is vague.

[§1.3] "**Zep**: strongest and most consistent spec delta (+0.19 controlled, +0.33 native). Positive on 9 of 9 low-baseline subjects in both configurations." -> "Zep shows the largest and most consistent improvement (+0.19 controlled, +0.33 native), positive across all 9 low-baseline subjects." | "Strongest and most consistent" is marketing superlative.

[§1.3] "**Supermemory**: strongest standalone retrieval (C1 mean ~2.65 vs. ~2.30 for the others on the 1-5 scale)." -> "Supermemory achieves the highest retrieval-only score (C1 mean ~2.65 vs. ~2.30 for others)." | "Strongest" is marketing language.

[§1.3] "The near-zero aggregate spec delta hides wild per-question swings in both directions" -> "The near-zero aggregate delta masks large per-question variation." | "Wild swings" is informal/marketing language.

[§1.3] "**Where the specification helps and where it hurts.**" -> "Specification effects vary by question type." | Headline phrasing is marketing-register.

[§1.3] "**The specification's effect on a given memory system is not uniform across questions.**" -> "Specification effects vary across questions within each system." | Repetitive given the preceding headline.

[§1.3] "The specification adds signal retrieval alone cannot on **interpretation-heavy questions**" -> "The specification provides additional signal on questions requiring pattern transfer to novel situations." | "Adds signal retrieval alone cannot" is awkward; "interpretation-heavy" is vague.

[§1.3] "Supermemory-alone returned discrete facts about nature, teachers, and loyalty and gave a generic "transformative" answer (score 1.17). With the specification added, the model recognized the specific pattern that beauty and mentor's words function as *a single formative mechanism* rather than two additive inputs, and scored 3.00 (Δ +1.83)." -> "Without the specification, Supermemory retrieved discrete facts and produced a generic response (1.17). With the specification, the model recognized that beauty and mentorship function as a unified pattern rather than separate inputs (3.00, Δ +1.83)." | "Formative mechanism" is jargon; "additive inputs" is vague.

[§1.3] "The specification hurts on **literal-recall questions** where a plain answer is available and spec-driven theorizing drifts past it, and on **refusal-triggering questions** where the specification's honesty axioms produce epistemically-honest refusals that the content-match rubric scores as off-base." -> "The specification reduces performance on factual-recall questions where theorizing diverges from available answers, and on questions where the specification's epistemic constraints produce refusals scored as incorrect by the rubric." | "Drifts past," "honesty axioms," and "epistemically-honest" are vague/jargon.

[§1.3] "With the specification added, the model invoked the spec's documented-dignity axioms, declined to fabricate interior motive, and told the user it could not answer without the specific passage; score 1.50." -> "With the specification, the model declined to infer unstated motives and refused to answer without supporting evidence (1.50)." | "Documented-dignity axioms" is jargon; "interior motive" is vague.

[§1.3] "We read this as an interaction between the specification and the rubric rather than as a clean specification defect or a clean benefit." -> "This reflects an interaction between the specification and the evaluation rubric." | "We read this as" is informal; "clean defect or clean benefit" is vague.

[§1.3] "The specification induced epistemically honest refusal on a question where the retrieved facts were insufficient to answer without fabrication: armed with the spec's documented-dignity axioms, the response model chose not to invent interior motive it could not ground in evidence." -> "The specification prompted refusal when retrieved facts were insufficient, preventing unsupported inference." | Repetitive and vague ("documented-dignity axioms," "interior motive").

[§1.3] "Under a content-match rubric, that refusal scores identically to an off-base guess, which the current scoring cannot distinguish." -> "The rubric does not distinguish refusal from incorrect answers." | Clearer and more direct.

[§1.3] "Whether this is a specification-level problem, a benchmark-level limitation, or both depends on how one weights epistemic honesty against predictive coverage." -> "This depends on whether epistemic honesty or predictive coverage is prioritized." | Vague framing ("depends on how one weights"); be more direct.

[§1.3] "A differentiated battery that separates interpretive prediction from literal recall and scores epistemic honesty as its own dimension would adjudicate the question directly, and is flagged as follow-up in §7." -> "A separate evaluation dimension for epistemic honesty would clarify this trade-off (flagged in §7)." | Wordy; "adjudicate the question directly" is vague.

[§1.3] "**Robustness: the effect is not an artifact of Claude talking to Claude.**" -> "Cross-provider replication." | Headline phrasing is marketing-register; the claim is about cross-provider validation.

[§1.3] "**The specification's effect holds when non-Anthropic models generate the test questions and non-Anthropic models read the specification.**" -> "The effect persists when non-Anthropic models generate questions and evaluate responses." | Repetitive; simplify.

[§1.3] "On three subjects spanning the effect gradient, 5 of 6 (subject × response model) cells reproduce the specification direction when Sonnet or Gemini Pro reads questions generated by GPT-5.4." -> "On three subjects, 5 of 6 cross-provider combinations reproduce the effect." | Clearer and more concise.

[§1.3] "The one mismatch (Zitkala-Sa × Gemini Pro) is consistent with the gradient mechanism rather than a replication failure." -> "The one mismatch aligns with the gradient hypothesis." | "Consistent with the gradient mechanism" is vague.

[§1.3] "This addresses within-Anthropic circularity, the concern that Anthropic-generated questions scored with Anthropic judges might favor Anthropic-produced specifications." -> "This addresses the concern that Anthropic-generated questions and judges might favor Anthropic specifications." | Wordy.

[§1.3] "**Architectural observation: Letta's stateful-agent path.**" -> "Letta's stateful-agent architecture." | Headline phrasing is marketing-register.

[§1.3] "**Letta is the only memory system whose architecture allows the AI itself to write and revise a persistent memory block during conversation. When we invoked this path directly, the AI produced a representation resembling the Behavioral Specification in what it captured, but not in how it compressed.**" -> "Letta's stateful-agent path allows the AI to write and revise a persistent memory block. This path produces a representation similar in content to the Behavioral Specification but different in compression." | Repetitive; "resembling...in what it captured, but not in how it compressed" is awkward.

[§1.3] "This is architectural convergence: two independently-designed systems target the same property." -> "Both systems converge on similar representational properties." | "Architectural convergence" is vague jargon.

[§1.3] "We read this as architectural validation of the interpretive-structure claim, not as two contradictory findings" -> "This supports the interpretive-structure hypothesis." | "We read this as" is informal; "architectural validation" is vague.

[§1.3] "Letta's memory block appears to grow roughly linearly with source corpus size" -> "Letta's memory block grows approximately linearly with corpus size." | "Appears to grow roughly" is hedging; be direct.

[§1.3] "At the largest corpus we tested, Letta's API began rejecting ingestion requests after the block reached approximately 333,000 characters; the final block, after 22 consecutive failed ingestion attempts, measured 335,349 characters." -> "At the largest corpus, Letta's API rejected ingestion after the block reached ~333,000 characters." | Repetitive detail ("22 consecutive failed attempts," "measured 335,349 characters") is unnecessary.

[§1.3] "We noted 25% verbatim sentence duplication as the block approached that ceiling." -> "The block showed 25% verbatim duplication near the size limit." | "Noted" is informal.

[§1.3] "Base Layer's compose step keeps the specification at 34,000-40,000 characters (~8,000-10,000 tokens) across the same range." -> "Base Layer maintains specification size at 34,000–40,000 characters across the same corpus range." | "Keeps...at" is informal.

[§1.3] "For reference, 335,000 characters is roughly 67,000 words: less than a single short book, and substantially less than ten years of daily journaling or the full accumulated session history of a long-running personal AI assistant." -> "For context, 335,000 characters (~67,000 words) is less than a short book and substantially less than a decade of daily journaling." | "For reference" + multiple comparisons is marketing-register framing; simplify.

[§1.3] "The stateful-agent path encountered a structural compression ceiling on the largest corpus we tested; the Behavioral Specification's compose step did not." -> "The stateful-agent path reached a compression ceiling; the Behavioral Specification did not." | Clearer.

[§1.3] "The gap at matched conditions is content-driven, not refusal-driven: Letta's larger block carries corpus-derived narrative the response model can cite, while the 7,000-token specification carries interpretive scaffolding only." -> "At matched conditions, Letta's larger block contains corpus-derived narrative; the specification contains interpretive structure." | "Content-driven, not refusal-driven" is vague; "scaffolding" is jargon.

[§1.3] "We report this as a frontier question for stateful-agent memory architectures, not as a claim of superiority." -> "This is an open question for stateful-agent architectures." | "Frontier question" and "not as a claim of superiority" are defensive marketing language.

[§1.4] "**What the gradient means for people who use AI in the real world.**" -> "Implications for real-world users." | Headline phrasing is marketing-register.

[§1.4] "**Nearly every real AI user starts from a baseline lower than any historical subject in this study.**" -> "Real-world users typically have lower baselines than the historical subjects tested." | Emphatic phrasing ("nearly every") is marketing-register.

[§1.4] "Our 14 subjects are public-domain authors whose writing was preserved, digitized, and indexed into training corpora. In practice, they sit well above the pretraining representation of a typical living person." -> "The 14 subjects are public-domain authors, whose writing is well-represented in training corpora, unlike typical living individuals." | "Sit well above" is informal.

[§1.4] "Even within this biased-up sample, the specification helped most where baseline was lowest: the 9 subjects below C5 ≤ 2.0 all improved." -> "Even in this sample biased toward high baselines, the specification helped most where baseline was lowest: all 9 subjects with C5 ≤ 2.0 improved." | "Biased-up" is informal; "below C5 ≤ 2.0" is awkward phrasing.

[§1.4] "Our lowest subject (Sunity Devee) scores 1.03, near the floor of the rubric, a score that indicates the model either refuses or produces an unrelated answer." -> "The lowest baseline (Sunity Devee, 1.03) indicates the model refuses or produces unrelated answers." | Wordy.

[§1.4] "For a typical living user whose private decisions were never indexed, the baseline is expected to sit at or near this rubric floor: the author's own clean-methodology pilot (§4.1.2) landed at C5 = 1.03, below every historical subject in the main study." -> "For living users with no indexed private record, the baseline is expected near the rubric floor. A pilot study (§4.1.2) with the author as subject achieved C5 = 1.03." | "Sit at or near" is informal; "clean-methodology pilot" is vague.

[§1.4] "The structural implication is direct: if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, and if a methodology-matched living-user pilot lands at the same floor with the largest lift in the study (+2.00 on facts+spec), the specification should be at least as beneficial for typical real AI users as it is for the historical subjects measured here." -> "If the specification benefits the lowest-baseline historical subjects and a living-user pilot shows the largest effect (+2.00), the specification should benefit typical users at least as much." | Repetitive and wordy; "structural implication is direct" is vague.

[§1.4] "**What we did not prove.**" -> "Limitations." | Headline phrasing is marketing-register.

[§1.4] "**This is a single-subject direct measurement plus an extrapolation argument, not a multi-subject living-user replication.**" -> "The living-user evidence is a single-subject pilot, not a multi-subject replication." | Emphatic negation ("not a multi-subject") is marketing-register.

[§1.4] "The §4.1.2 pilot is N=1 living user (the paper's author), the only living subject whose private corpus we could ethically run through the pipeline." -> "The pilot (N=1, the author) is the only living subject whose private corpus could be tested." | Parenthetical is wordy.

[§1.4] "The pilot confirms the gradient's prediction for one person but cannot establish that the prediction holds across a population of living users." -> "The pilot supports the gradient hypothesis for one person but does not establish population generality." | "Confirms the prediction" is vague; "establish that the prediction holds" is repetitive.

[§1.4] "A multi-subject living-user replication (planned for §8 Future Work) is the single most important piece of follow-up work for this paper." -> "Multi-subject living-user replication is the primary follow-up priority (§8)." | "Single most important piece" is marketing-register emphasis.

[§1.4] "We are also exploring alternative testbeds that isolate reasoning structure without requiring private data, including U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted." -> "Alternative testbeds under exploration include U.S. Supreme Court opinions, where documented decisions provide a public record of individual reasoning." | Wordy; "documented decisions provide a public record of individual interpretive patterns that can be held out and predicted" is repetitive.

[§1.4] "One other boundary claim belongs here: our judging remains LLM-as-judge at evaluation, so broader LLM-circularity concerns are not fully addressed by the cross-provider replication." -> "LLM-as-judge evaluation remains a limitation not fully addressed by cross-provider replication." | "Boundary claim belongs here" is informal.

[§1.4] "We state this here because §1.3's claims rest on extrapolation past it." -> "This limitation affects the claims in §1.3." | Clearer and more direct.

[§1.5] "**How this paper connects to the broader question of human-AI alignment.**" -> "Connection to human-AI alignment." | Headline phrasing is marketing-register.

[§1.5] "**Behavioral alignment is one concrete, measurable instance of human-AI alignment: whether a specific AI system's actions accord with a specific person's reasoning, values, and decision-making when acting on that person's behalf.**" -> "Behavioral alignment is the alignment of a specific AI system's actions with a specific person's reasoning and decision-making." | Repetitive definition; simplify.

[§1.5] "The AI safety community typically uses "alignment" to mean preventing harmful behavior at the model level. That is one property. Behavioral alignment is a different property, and the two axes are orthogonal, not a hierarchy." -> "Safety alignment (preventing harmful behavior) and behavioral alignment (matching individual reasoning) are distinct properties." | Clearer and more concise.

[§1.5] "A model that is safely aligned in the safety sense can still be behaviorally misaligned with any given user: it will act reasonably, but not the way *you* would act." -> "A safely-aligned model can still act differently from how a specific user would act." | Repetitive ("safely aligned in the safety sense"); simplify.

[§1.5] "The inverse is also true and important." -> "The inverse also holds." | "Also true and important" is vague emphasis.

[§1.5] "A perfectly behaviorally-aligned agent, acting exactly as a specific user would act, can be catastrophically safety-misaligned if that user would act maliciously, recklessly, or against third-party interests." -> "A behaviorally-aligned agent can be safety-misaligned if the user's reasoning is malicious or reckless." | Clearer and more concise.

[§1.5] "Behavioral alignment is not a safety property. It is a personalization property that safety constraints must sit above." -> "Behavioral alignment is a personalization property, distinct from safety constraints." | "Must sit above" is vague metaphor.

[§1.5] "**Representational accuracy is a necessary condition for behavioral alignment, but not sufficient.**" -> "Representational accuracy is necessary but not sufficient for behavioral alignment." | Clearer.

[§1.5] "A system cannot act the way someone would act if it lacks an accurate internal model of how that person reasons." -> "An accurate internal model of a person's reasoning is required for aligned action." | Clearer.

[§1.5] "Having the model is required; translating the model into aligned action, subject to safety constraints, is a separate problem we do not address in this paper." -> "This paper addresses representation; translating representation into aligned action subject to safety constraints is separate." | Clearer.

[§1.5] "We focus on the representation layer because it is the piece that is under-studied and empirically tractable." -> "The representation layer is under-studied and empirically tractable." | "We focus on...because it is the piece that is" is wordy.

[§1.5] "An agent that acts on your behalf without an accurate representation of you is not serving you; it is averaging over some population the model happens to resemble." -> "An agent without an accurate representation of you averages over a population the model resembles." | "Not serving you" is vague; simplify.

[§1.5] "The question this paper asks, operationally: **can the AI act the way you would act, given how you think?**" -> "Research question: Can the AI act as you would, given your reasoning?" | Clearer and more concise.

[§1.5] "The question the field should take up, more generally: **how do we know when an AI's internal model of a specific person is accurate enough for the agent to act on that person's behalf, and by what means do we improve and audit that representation?**" -> "Broader question: How do we validate and audit an AI's representation of a person's reasoning?" | Clearer and more concise.

---

## Dense Passages

[§1.1] "State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant." -> Break into: "State-of-the-art AI memory systems optimize for recall. Four leading systems (Zep, Letta, Mem0, Supermemory) report recall accuracies of 68–85% on standard benchmarks (LOCOMO, LongMemEval), varying by provider and model variant." | Easier to parse.

[§1.1] "We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. Think of how viewing situations from different lenses can lead to entirely different interpretations of the same set of facts. This has been shown across the human experience, from the sciences to religion to political affiliations, and by extension to the relative experiences of any individual." -> Break into: "Interpretation is how a person processes facts and experiences into judgments and decisions. Different interpretive lenses lead to different conclusions from the same facts. This varies across domains (science, religion, politics) and individuals." | Clearer and more concise.

[§1.2] "For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model." -> Break into: "For each subject, the corpus was split in half. The training half generated the specification, seeded memory systems, and provided the fact pool. The held-out half produced behavioral prediction questions, never shown to response models." | Clearer structure.

[§1.2] "The five hypotheses map directly to §4: H1 and H2 to §4.1 The Gradient; H3 to §4.3 Mechanism; H4 to §4.4 Memory-System Composition; H5 to §4.2 Compression." -> Break into separate line: "Hypotheses H1–H2 map to §4.1 (Gradient); H3 to §4.3 (Mechanism); H4 to §4.4 (Composition); H5 to §4.2 (Compression)." | Easier to parse.

[§1.2] "As a **secondary outcome**, we report the per-question **win rate against the no-context baseline**: for each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), classify the outcome as improved / tied / worsened, and report all three rates alongside the median magnitudes of improvement and worsening." -> Break into: "The secondary outcome is the per-question win rate against baseline (C5). For each question, we classify outcomes as improved/tied/worsened and report rates and median magnitudes." | Clearer.

[§1.2] "This secondary outcome is a scale-free, directly interpretable measure of the **breadth of benefit** of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1." -> Break into: "This metric is scale-free and directly interpretable. It is introduced here for reference throughout §4; formal analysis is in §4.2.1." | Clearer.

[§1.3] "Linear regression of the facts-plus-spec effect against baseline gives slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001 for the slope coefficient. This p-value directly supports the gradient relationship itself; the separate Wilcoxon signed-rank test (p = 0.007, W = 11, N=14, C5 vs. C4a) confirms overall improvement." -> Break into: "Linear regression shows slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001. A Wilcoxon signed-rank test confirms overall improvement (p = 0.007, W = 11, N=14)." | Clearer separation of findings.

[§1.3] "12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is backed by a substantially stronger per-response pattern: 55.0% of individual responses on the low-baseline slice cross a rubric integer anchor upward when the spec is added (§4.1), and 70.9% of questions improve at all (§4.2.1)." -> Break into: "12 of 14 subjects improve. All 9 low-baseline subjects (C5 ≤ 2.0) improve, with mean gain +0.89. At the per-response level, 55.0% cross a rubric integer upward (§4.1) and 70.9% improve (§4.2.1)." | Clearer structure.

[§1.3] "On Hamerton, the Behavioral Specification alone (C2a, ~7,300 tokens) scores 2.63 on the 5-judge primary panel. The same subject's full training corpus loaded into context without a specification (C8, ~33,000 tokens) scores 2.27. The specification outperforms the raw source at roughly one-fifth the context size." -> Break into: "Hamerton: Specification alone (C2a, ~7,300 tokens) scores 2.63. Full corpus without specification (C8, ~33,000 tokens) scores 2.27. The specification outperforms at one-fifth the context size." | Clearer.

[§1.3] "On the 13 global subjects with complete 5-judge primary coverage, a wrong specification (random derangement, seed-fixed) scores near baseline with a mean Δ of +0.22 vs. +0.35 for the correct spec on the same subjects. A more adversarial control, a deterministic fixed pairing designed to maximize cultural and temporal distance between each subject and the specification it receives (mapping defined in `scripts/run_global_rerun.py`), scores clearly below baseline at Δ −0.25: when the mismatch is large, structured content for the wrong person performs worse than no context at all." -> Break into: "Wrong specification (random derangement): Δ +0.22 vs. +0.35 for correct spec. Adversarial control (maximized cultural/temporal distance): Δ −0.25, below baseline. Large mismatches degrade performance below no-context baseline." | Clearer.

[§1.3] "Across 587 wrong-spec responses classified (validated against a 30-response stratified manual spot check), the response distribution is bimodal: 60.6% explicitly flagged the mismatch (example, from one Keckley wrong-spec response: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*) and either refused or produced a hedged response; 36.5% attempted to apply the mismatched specification and produced a low-quality prediction; 2.0% hedged implicitly; 0.9% were ambiguous." -> Break into: "Of 587 wrong-spec responses: 60.6% flagged the mismatch and refused/hedged; 36.5% applied the mismatch and produced low-quality predictions; 2.0% hedged implicitly; 0.9% were ambiguous." | Clearer.

---

## Chunk: §2 Related Work

# Marketing Register Audit: §2 Related Work

## Flagged Instances

[§2.0] "Memory systems today optimize for recall." -> "Current memory systems prioritize recall." | "optimize for" is marketing-neutral but the framing that follows ("the gap," "the missing thread") uses pitch-deck structure; flag the conceptual framing instead.

[§2.0] "The gap between these directions is the translation." -> "These directions remain disconnected." | "the gap...is the translation" is vague-strength framing; "translation" inflates a simple absence into a conceptual entity.

[§2.0] "the missing thread in current AI memory and human-AI interaction research" -> "absent from current AI memory and human-AI interaction research" | "missing thread" is pitch-deck language (implies hidden solution); "absent" is plainer.

[§2.1] "have converged on a shared set of capabilities" -> "implement similar capabilities" | "converged" implies strategic alignment; "implement" is more neutral.

[§2.1] "None positions representational accuracy or behavioral prediction of a specific individual as a design target." -> "None explicitly targets representational accuracy or behavioral prediction of a specific individual." | Minor: "positions" is softer than needed; "explicitly targets" is clearer.

[§2.2] "Traceability is not a feature of the Behavioral Specification. It is a necessity." -> "The Behavioral Specification requires traceability." | This is pitch-deck framing (emphatic negation + restatement); the plain claim is simpler.

[§2.2] "Zep has the strongest explicit provenance of the four" -> "Zep provides the most explicit provenance of the four" | "strongest" is a vague-strength superlative; "most explicit" is more precise.

[§2.2] "Fact-level traceability answers where a retrieved claim came from. That is necessary but not sufficient" -> "Fact-level traceability shows where a retrieved claim originated. This is necessary but insufficient" | "answers" is colloquial; "originated" is plainer. "not sufficient" → "insufficient" is more direct.

[§2.3] "Existing memory and personalization benchmarks measure recall, persona consistency, preference alignment, or conversational quality. None measures behavioral prediction" -> "Existing benchmarks measure recall, consistency, alignment, or quality. None measures behavioral prediction." | The emphatic restatement ("None measures...") is pitch-deck structure; the claim stands without it.

[§2.3] "This paper's battery tests that directly." -> "This paper tests behavioral prediction directly." | "battery tests that" is inflated; "tests" is sufficient.

[§2.3] "Heavily recall-weighted." -> "Emphasizes recall." | "Heavily recall-weighted" is jargon inflation; "emphasizes" is plainer.

[§2.3] "Does not test whether the system represents how the person reasons." -> "Does not evaluate whether the system captures how the person reasons." | "represents" is softer; "captures" is more direct.

[§2.3] "This paper's battery is orthogonal: every held-out question asks about behavior, not about retrieved content." -> "This paper's battery measures a different dimension: every held-out question asks about behavior, not retrieved content." | "orthogonal" is jargon; "measures a different dimension" is plainer.

[§2.3] "Tests persona fidelity: whether a model maintains a described persona during conversation." -> "Tests whether a model maintains a described persona during conversation." | The colon + restatement is pitch-deck structure.

[§2.3] "Evaluates consistency of persona presentation, not prediction of held-out behavior." -> "Evaluates consistency of persona presentation, not prediction of unseen behavior." | "held-out" is technical jargon; "unseen" is plainer.

[§2.3] "A persona-fidelity system can maintain voice without ever accurately predicting decisions, and a representationally-accurate system can change voice while continuing to predict accurately. Our battery measures the second axis." -> "A system can maintain consistent voice without predicting decisions accurately, and vice versa. Our battery measures prediction accuracy." | "persona-fidelity," "representationally-accurate," and "second axis" are jargon; the plain claim is simpler.

[§2.3] "Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses." -> "Evaluates whether explicit memory mechanisms produce more preference-aligned and emotionally resonant responses." | "improve" is vague-strength; "produce more" is more precise.

[§2.3] "The evaluation axis is preference-alignment and emotional resonance on conversational responses, not interpretive transfer on held-out behavior" -> "The evaluation measures preference-alignment and emotional resonance in responses, not behavioral prediction on unseen situations." | "evaluation axis," "interpretive transfer," and "held-out behavior" are jargon; plainer alternatives exist.

[§2.3] "their test and ours share the observation that recall improvement does not carry into these downstream properties" -> "both tests show that improving recall does not improve these downstream properties." | "carry into" is colloquial; "improve" is more direct. "downstream properties" is jargon.

[§2.3] "Both results point toward recall-solving being insufficient for what memory is ultimately for." -> "Both results suggest that improving recall alone is insufficient for effective memory systems." | "point toward," "recall-solving," and "what memory is ultimately for" are pitch-deck framing; the claim is simpler.

[§2.3] "Behavioral prediction at scale: 2,058 participants predicted on held-out survey items using a full-text persona of their own prior survey responses." -> "Behavioral prediction at scale: 2,058 participants, with predictions evaluated on survey items not in the training set, using a full-text persona derived from prior survey responses." | "held-out" is jargon; "not in the training set" is plainer.

[§2.3] "An earlier exploratory Base Layer run against Twin-2K's battery produced comparable prediction accuracy at a small fraction of the context size; we do not report those numbers as a formal benchmark comparison here because the experiment used a prior iteration of our pipeline and a different task format from the autobiography-based behavioral battery that grounds the rest of this paper." -> "An earlier run on Twin-2K produced comparable accuracy with less context, but we do not report it formally because the pipeline and task format differed from the autobiography-based battery used here." | Dense sentence; "grounds the rest of this paper" is pitch-deck language.

[dense §2.3] "Structural differences remain the load-bearing point: Twin-2K's persona is a machine-readable transcript..." -> Break after "load-bearing point:" and start a new sentence. | "load-bearing point" is marketing jargon (implies critical importance); "The key difference is:" is plainer.

[§2.3] "Twin-2K measures whether a model can interpolate a person's survey distribution from other survey responses; our battery measures whether a representation of how a person reasons transfers to novel situations the representation has never seen." -> "Twin-2K measures interpolation of survey responses; our battery measures whether a representation of reasoning transfers to novel situations." | "transfers to novel situations the representation has never seen" is inflated; "transfers to novel situations" is sufficient.

[§2.4] "Six prior research directions shaped how we designed this paper's test." -> "Six prior research directions informed our test design." | "shaped how we designed" is colloquial; "informed" is more direct.

[§2.4] "Each motivates a specific choice about what to measure, what to compare against, or what failure mode to expect." -> "Each justifies a specific measurement choice, comparison, or expected failure mode." | "motivates" is softer; "justifies" is more direct.

[§2.4] "Bartlett (1932) established that human memory is reconstructive and schema-driven rather than literal playback." -> "Bartlett (1932) showed that human memory is reconstructive and schema-driven, not literal." | "established" is formal but acceptable; "rather than literal playback" is verbose; "not literal" is plainer.

[§2.4] "Reconstruction follows the organizing structures a person has built up over time, not a record of the original event." -> "Reconstruction follows the structures a person has built, not a record of the original event." | "organizing structures...built up over time" is verbose.

[§2.4] "The Behavioral Specification is computationally analogous: a structured compression meant to carry the signal of a person's reasoning without storing every fact about them." -> "The Behavioral Specification is a structured compression of a person's reasoning patterns, without storing every fact." | "computationally analogous," "carry the signal," and "meant to" are inflated; the claim is simpler.

[§2.4] "We designed the specification with a schema-like architecture (anchors, core, predictions) precisely so we could test whether it does the work a human schema does: enable accurate anticipation of behavior in situations never encountered in the source data." -> "We designed the specification with a schema-like architecture (anchors, core, predictions) to test whether it enables accurate behavioral prediction on unseen situations." | "precisely so we could test whether it does the work...does" is repetitive; "enable accurate anticipation" is inflated.

[§2.4] "Our 50/50 train/held-out split is the experimental realization of this question." -> "Our 50/50 train/test split directly tests this question." | "experimental realization of" is jargon; "directly tests" is plainer. "held-out" → "test" is standard terminology.

[§2.4] "This result motivates one of our central experimental comparisons" -> "This result justifies one of our key experimental comparisons." | "motivates" is softer; "justifies" is more direct. "central" → "key" is less marketing-inflected.

[§2.4] "on matched token budgets, does a compressed interpretive artifact carry more predictive signal than the raw content it was derived from?" -> "on matched token budgets, does a compressed representation carry more predictive signal than the raw source text?" | "interpretive artifact" is jargon; "representation" is plainer. "raw content it was derived from" → "raw source text" is more direct.

[§2.4] "The Hamerton condition in §4.2 (7,300-token spec vs. 33,000-token training corpus at 2.63 vs. 2.27 on the 5-judge primary panel) is a direct test of that question in the personal-representation setting." -> "The Hamerton condition (§4.2) compares a 7,300-token spec to a 33,000-token corpus (2.63 vs. 2.27 on the 5-judge panel), directly testing this question." | "is a direct test of that question in the personal-representation setting" is verbose.

[§2.4] "Their approach modifies the model; ours informs the model from outside via context." -> "Their approach modifies the model; ours provides context." | "informs the model from outside via context" is verbose.

[§2.4] "Both validate that persona is a real, manipulable structure: one reachable through weights, the other through context." -> "Both show that persona is a real, manipulable structure: one through weights, the other through context." | "validate" is softer; "show" is more direct. "reachable through" → "through" is more concise.

[§2.4] "We chose the context route because it produces a portable artifact users can own and audit, which activation surgery does not." -> "We chose context because it produces a portable artifact users can own and audit." | "the context route" is colloquial; "context" is sufficient. The final clause is implied.

[§2.4] "This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model." -> "This choice appears in our design: a static model (Haiku) with variable context, rather than fine-tuning or activation steering." | "shows up in the experiment as" is colloquial; "appears in our design" is more direct.

[§2.4] "find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access." -> "find that frontier models achieve only ~50% accuracy on user profiling tasks even with full conversation access." | "dynamic" is unnecessary jargon.

[§2.4] "The paper documents the failure empirically; our reading is that the cause is the gap between having facts and having the interpretive structure to apply them to novel situations." -> "The paper documents this empirically. We attribute it to the gap between having facts and having the structure to apply them to novel situations." | "our reading is that the cause is" is verbose; "We attribute it to" is more direct.

[§2.4] "behavioral prediction on scenarios drawn from held-out text that the model has not seen, with all relevant facts retrievable, measures exactly the interpretive-application gap." -> "behavioral prediction on unseen scenarios, with all relevant facts available, measures the gap between having facts and applying them." | "held-out text that the model has not seen" is redundant; "unseen scenarios" is sufficient. "interpretive-application gap" is jargon; the plain claim is simpler.

[§2.4] "find that adding conversation context to LLMs makes them more sycophantic: more likely to agree with the user even when the user is wrong (+45% on Gemini 2.5 Pro) and more likely to adopt the user's perspective on a question." -> "find that adding conversation context makes LLMs more likely to agree with the user even when wrong (+45% on Gemini 2.5 Pro) and to adopt the user's perspective." | "more sycophantic" is colloquial; "more likely to agree...even when wrong" is more precise.

[§2.4] "Their result shows that context without the right structure pushes the model toward what the user appears to want rather than toward a grounded answer." -> "Their result shows that unstructured context pushes the model toward what the user wants rather than toward accuracy." | "context without the right structure" is verbose; "unstructured context" is plainer. "appears to want" → "wants" is more direct. "grounded answer" → "accuracy" is clearer.

[§2.4] "This is why our experiment includes a wrong-spec control (§1.3 Mechanism): we hand the model a structured interpretive context that does not match the actual subject." -> "This is why we include a wrong-spec control (§1.3 Mechanism): a structured context that does not match the actual subject." | "we hand the model" is colloquial; "a structured context" is more direct.

[§2.4] "If models drifted purely toward whatever context they are given, the wrong-spec should behave like any other structured prompt." -> "If models simply adopted whatever context they received, the wrong-spec should perform like any other structured prompt." | "drifted purely toward" is colloquial; "simply adopted" is more direct.

[§2.4] "Instead, the model either flags the mismatch explicitly (60.6% of responses) or attempts a low-quality application, neither of which is sycophantic drift." -> "Instead, the model either flags the mismatch (60.6% of responses) or produces low-quality output, neither of which is sycophantic drift." | "flags...explicitly" is redundant; "flags" is sufficient. "attempts a low-quality application" is verbose; "produces low-quality output" is plainer.

[§2.4] "Jain's finding plus our wrong-spec result bracket the question from both sides: context shape matters (Jain), and content matters too (ours)." -> "Jain's finding and our wrong-spec result address the question from both angles: context structure matters (Jain), and content matters (ours)." | "bracket the question from both sides" is colloquial; "address...from both angles" is more direct. "content matters too" → "content matters" is more concise.

[§2.4] "identify what they call the Assistant Axis: a dominant internal direction that anchors assistant models' default behavior toward generic helpfulness and harmlessness." -> "identify the Assistant Axis: a dominant internal direction that anchors assistant models toward generic helpfulness and harmlessness." | "what they call" is unnecessary; "anchors...toward" is verbose; "anchors...to" is plainer.

[§2.4] "The Behavioral Specification can be read as an external override to the Assistant Axis on a per-user basis: a structured anchor that shifts the model from 'generic helpful assistant' toward 'reasons as this specific person would reason.'" -> "The Behavioral Specification can be read as an external override to the Assistant Axis: a structured anchor that shifts the model from generic helpfulness toward person-specific reasoning." | "on a per-user basis" is jargon; implied by "override." "reasons as this specific person would reason" is repetitive; "person-specific reasoning" is plainer.

[§2.4] "This framing motivated our choice to measure hedging as a primary outcome alongside accuracy" -> "This framing led us to measure hedging as a primary outcome alongside accuracy." | "motivated our choice to" is verbose; "led us to" is more direct.

[§2.4] "if the spec shifts the model off the generic Assistant Axis, the behavioral change should show up both in what the model predicts and in what it is willing to commit to." -> "if the spec shifts the model off the generic Assistant Axis, the change should appear in both predictions and confidence." | "show up...in what the model predicts and in what it is willing to commit to" is verbose; "appear in both predictions and confidence" is plainer.

[§2.4] "Our hedging-reduction finding (§1.3 Mechanism, §5.5) is consistent with this reading: the generic Assistant Axis produces hedging as a safe default, while a specific interpretive anchor enables commitment." -> "Our hedging-reduction finding (§1.3 Mechanism, §5.5) supports this: the generic Assistant Axis produces hedging as a safe default, while a specific anchor enables commitment." | "is consistent with this reading" is softer; "supports this" is more direct. "interpretive anchor" → "anchor" is sufficient.

[§2.4] "The inference that hedging is downstream of the Assistant Axis is ours; Lu et al. identify the axis and leave the specific behavioral manifestations open." -> "We infer that hedging is downstream of the Assistant Axis; Lu et al. identify the axis but do not specify behavioral manifestations." | "The inference...is ours" is awkward; "We infer" is more direct. "leave...open" is colloquial; "do not specify" is plainer.

[§2.5] "LLM-as-judge evaluation is an established methodology with known biases." -> "LLM-as-judge evaluation has known biases." | "established methodology with known biases" is redundant; the point is the biases.

[§2.5] "Zheng et al. (NeurIPS 2023 Datasets and Benchmarks Track, arXiv:2306.05685) demonstrated that LLM judges agree with human judges at rates comparable to inter-human agreement (over 80% on the MT-Bench and Chatbot Arena benchmarks), establishing the approach as viable for tasks that would otherwise require expensive human annotation." -> "Zheng et al. (NeurIPS 2023 Datasets and Benchmarks Track, arXiv:2306.05685) showed that LLM judges agree with human judges at rates comparable to inter-human agreement (over 80% on MT-Bench and Chatbot Arena), validating the approach for tasks that would otherwise require human annotation." | "demonstrated" → "showed" is more direct. "establishing the approach as viable" is verbose; "validating the approach" is plainer. "expensive human annotation" → "human annotation" is sufficient.

[§2.5] "This paper extends their work by calibrating each judge in our judge panel for three specific biases: ceiling behavior (what score each judge assigns to verbatim matches), paraphrase sensitivity (how each judge handles semantically equivalent but differently-worded responses), and length bias (whether each judge rewards or penalizes longer responses)." -> "We extend this by calibrating each judge for three biases: ceiling behavior (scores for verbatim matches), paraphrase sensitivity (handling of semantically equivalent responses), and length bias (preference for longer responses)." | "what score each judge assigns to" is verbose; "scores for" is plainer. "semantically equivalent but differently-worded responses" → "semantically equivalent responses" is sufficient. "whether each judge rewards or penalizes" is verbose; "preference for" is plainer.

[§2.5] "The two Gemini judges systematically inflate scores by approximately one point relative to the other five, so we report the five non-Gemini judges as the primary aggregate and the full seven-judge panel as a sensitivity check." -> "The two Gemini judges inflate scores by ~1 point relative to the other five, so we report the five non-Gemini judges as primary and the full panel as a sensitivity check." | "systematically inflate" → "inflate" is sufficient. "approximately one point" → "~1 point" is more concise. "the primary aggregate" → "primary" is plainer.

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §2.0 (intro) | 2 | Heavy pitch-deck framing: "the gap," "the missing thread," emphatic negations. Vague-strength language ("significant," "meaningful" implied). |
| §2.1 (Memory systems) | 3 | Mostly factual, but "converged," "strongest," and "positions" introduce marketing register. Table is clean. |
| §2.2 (Traceability) | 2 | Emphatic opening ("not a feature...It is a necessity") is pitch-deck structure. "Strongest explicit provenance" is a superlative. Reasoning is sound but register is inflated. |
| §2.3 (Benchmarks) | 2 | Repeated emphatic restatements ("None measures...This paper's battery tests that directly"). Jargon-heavy ("orthogonal," "downstream properties," "interpretive transfer," "load-bearing point"). Vague-strength language ("comparable," "complementary"). |
| §2.4 (Cognitive foundations) | 2 | Verbose and jargon-heavy throughout. "Shaped," "motivates," "carry the signal," "interpretive artifact," "shows up," "bracket the question," "reads as," "manifests" are all marketing-register or colloquial. Dense sentences with inflated noun phrases. |
| §2.5 (LLM-as-judge) | 4 | Cleanest section. Mostly direct and factual. Minor issues: "established methodology" is slightly redundant, "viable" is softer than needed. |

---

## Summary

**Overall register cleanliness: 2.3/5** (leans toward GTM/pitch-deck register)

**Primary issues:**
1. **Emphatic restatement structure** (pitch-deck pattern): "X is not Y. It is Z." appears multiple times (§2.2, §2.3).
2. **Vague-strength superlatives**: "strongest," "most robust," "cleanest," "most explicit."
3. **Jargon inflation**: "interpretive artifact," "load-bearing point," "orthogonal," "downstream properties," "bracket," "carry the signal," "shows up."
4. **Colloquial verbs**: "shaped," "motivated," "reads as," "bracket," "shows up," "hand the model."
5. **Dense, multi-clause sentences** with inflated noun phrases (especially §2.3 and §2.4).
6. **Pitch-deck framing**: Positioning the paper's contribution as solving a "gap" or "missing thread" rather than addressing a research question.

**Recommendation**: Prioritize §2.0, §2.2, §2.3, and §2.4 for revision. Replace emphatic restatements with direct claims. Replace jargon with plain terms. Break dense sentences. Use "showed," "found," "measured" instead of "motivated," "shaped," "established." Remove superlatives or replace with precise comparatives.

---

## Chunk: §3 Study Design

# Register Review: §3 Study Design

## Marketing Register Flags

[§3.0] "The experimental strategy holds the response model constant and varies the representation served as its context." -> "We hold the response model constant and vary the representation served as its context." | Unnecessary passive nominalization; "strategy" is inflated framing.

[§3.0] "This isolates the contribution of the representation itself from model capability, provider, or fine-tuning regime." -> "This separates the representation's contribution from model capability, provider, or fine-tuning regime." | "Isolates" is marketing-register isolation language; "separates" is plainer.

[§3.1] "We use the term representational accuracy to describe how faithfully a model can act in line with a specific person when given a representation of that person." -> "Representational accuracy measures how well a model acts in line with a specific person when given a representation of that person." | Unnecessary meta-framing ("we use the term"); just define it.

[§3.1] "All three matter." -> Delete or rephrase to "All three are necessary." | Colloquial emphasis; academic prose avoids this register.

[§3.1] "Prediction on held-out situations is how we test all three at once." -> "We test all three by predicting behavior on held-out situations." | Inverted structure with "how" creates pitch-deck rhythm.

[§3.1] "When it does not, one of three things is failing: the behavioral patterns are not consistent, the representation is wrong, or the model is not using the representation well." -> "When it does not, one of three failures has occurred: inconsistent behavioral patterns, inaccurate representation, or poor model utilization of the representation." | "Failing" is colloquial; nominalize to parallel structure.

[§3.1] "Each failure mode is informative." -> "Each failure mode provides diagnostic information." | "Informative" is vague-strength descriptor; be specific about what information is gained.

[§3.1] "We do not claim to modify the model's internal parameters." -> "The Behavioral Specification does not modify the model's internal parameters." | Unnecessary first-person assertion; state the fact directly.

[§3.1] "The Behavioral Specification is served as context: a lens through which the model can reason about a specific person." -> "The Behavioral Specification is provided as context, allowing the model to reason about a specific person." | "Lens" is a metaphor; avoid in academic prose. "Served as" is pitch-deck language.

[§3.1] "What we measure is whether that external lens is accurate enough to guide the model's responses in the same way the person would guide them." -> "We measure whether the external specification is accurate enough to guide the model's responses toward the person's documented patterns." | Remove metaphor; "guide them" is vague.

[§3.2] "Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting on any single type of source material." -> "Subjects were selected across time periods, source-text lengths, and geographic origins to ensure diversity of source material." | "Avoid the study sitting on" is awkward nominalization; "ensure diversity" is clearer.

[§3.2] "Because frontier language models train on large public-text corpora, some level of pretraining exposure to each subject's writing is likely." -> "Because frontier language models train on large public-text corpora, pretraining exposure to each subject's writing is probable." | "Some level of...is likely" is hedging; be direct.

[§3.2.1] "Before turning to the specification's effect, the baseline itself is worth flagging as a finding." -> "Before examining the specification's effect, we note the baseline as a finding." | "Worth flagging" is colloquial pitch-deck language.

[§3.2.1] "Response models vary widely in their pretrained capacity on a given person, even across a sample of subjects who all have public-domain autobiographies of comparable provenance." -> "Response models show uneven pretrained capacity for a given person, even across subjects with public-domain autobiographies of comparable provenance." | "Vary widely" is vague-strength descriptor; "uneven" is more precise.

[§3.3] "The pipeline transforms raw source text into a Behavioral Specification in four content-production steps: extract, embed, author, and compose." -> "The pipeline converts raw source text into a Behavioral Specification through four steps: extract, embed, author, and compose." | "Transforms" is marketing-register verb; "converts" is neutral. "Content-production" is jargon inflation.

[§3.3] "An import step canonicalizes the source data before extraction." -> "An import step standardizes the source data before extraction." | "Canonicalizes" is unnecessarily technical; "standardizes" is clearer.

[§3.3] "Each step is a single script backed by a single model choice." -> "Each step uses a single script and model." | Unnecessary nominalization; simplify.

[§3.3] "Total cost per subject is under $1." -> Keep as is. | This is factual and appropriately brief.

[§3.3] "The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: `avoids`, `repeatedly engages in`, `refuses to`, `values`, `fears`, `has experienced`)." -> Keep as is. | This is clear and technical.

[§3.3] "The vocabulary is human-curated and was validated across 50+ pilot subjects before being frozen for the study." -> "The vocabulary was curated and validated across 50+ pilot subjects before being fixed for the study." | "Human-curated" is unnecessary (who else would curate it?); "frozen" is colloquial.

[§3.3] "The constrained vocabulary is the main lever the pipeline uses to push extraction away from biographical facts ("his father was violent") and toward behavioral patterns ("evaluates authority figures on dual criteria of virtue and failure")." -> "The constrained vocabulary directs extraction toward behavioral patterns rather than biographical facts." | "Main lever" is metaphor; "push...toward" is marketing language. Simplify.

[§3.3] "Each layer has a characteristic format; examples below are drawn from the Hamerton specification." -> "Each layer has a distinct format; examples below are from the Hamerton specification." | "Characteristic" is vague; "distinct" is clearer. "Drawn from" is slightly formal; "from" suffices.

[§3.3] "Anchors encode the subject's load-bearing axioms in numbered form (A1, A2, ...), each with an activation condition and a false-positive warning." -> "Anchors encode the subject's core axioms in numbered form (A1, A2, ...), each with an activation condition and a false-positive warning." | "Load-bearing" is architectural metaphor; "core" is plainer.

[§3.3] "Core captures values, beliefs, and self-view in flowing prose." -> "Core captures values, beliefs, and self-view in prose." | "Flowing" is vague descriptor; remove it.

[§3.3] "It is the layer that reads most like an essay about the person." -> "This layer resembles an essay about the person." | "Reads most like" is colloquial; "resembles" is more academic.

[§3.3] "Predictions are explicit behavioral predicates (P1, P2, ...) with detection criteria, directives, and false-positive warnings." -> Keep as is. | This is clear and technical.

[§3.3] "The compose step integrates these three layers into a unified prose brief." -> "The compose step combines these three layers into a prose brief." | "Integrates" is slightly inflated; "combines" is plainer. "Unified" is redundant.

[§3.3] "The served specification is the compose-step brief concatenated with the three layer files." -> "The specification served to the model is the compose-step brief concatenated with the three layer files." | Clarify what "served" means; avoid passive construction.

[§3.3] "Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80)." -> Keep as is. | Factual and clear.

[§3.4] "Each subject's behavioral prediction battery is generated by a backward-design process: an LLM reads a passage from the held-out half of the corpus, writes a question whose answer is the behavioral pattern implicit in the passage, and deliberately avoids naming any detail unique to the passage itself." -> "Each subject's behavioral prediction battery is generated through backward design: an LLM reads a held-out passage, writes a question whose answer requires the behavioral pattern implicit in the passage, and avoids naming passage-specific details." | Simplify the structure; "deliberately avoids" is redundant with "avoids."

[§3.4] "The question can be attempted from training-text patterns alone; the verbatim held-out passage is the ground truth for scoring." -> "The question can be answered from training-text patterns alone; the held-out passage is the ground truth for scoring." | "Verbatim" is redundant; "ground truth" already implies exact match.

[§3.4] "Backward-design question generation." -> "Backward-design question generation." | Keep as is; this is a technical term.

[§3.4] "Claude Haiku 4.5 (temperature 0) reads each held-out window and writes a question whose answer requires the subject's behavioral patterns observable in the training half." -> "Claude Haiku 4.5 (temperature 0) reads each held-out window and writes a question whose answer requires behavioral patterns observable in the training half." | Remove "the subject's" (implied by context).

[§3.4] "The prompt extracts a verbatim ground-truth span from the held-out window and forbids named-entity or specific-date leakage in the question stem." -> "The prompt extracts a ground-truth span from the held-out window and prevents named-entity or date leakage in the question stem." | "Verbatim" is redundant; "forbids" is formal; "prevents" is plainer.

[§3.4] "Dedup and freeze." -> "Deduplication and freezing." | Expand abbreviations in formal prose.

[§3.4] "Deduplication on lowercased question text, cap at target counts per category, MD5 checksum of the final battery." -> "Deduplication on lowercased question text, capping at target counts per category, with MD5 checksum of the final battery." | Add verbs for clarity.

[§3.4] "Downstream response and judgment files are invalidated if the battery checksum changes." -> "Response and judgment files are invalidated if the battery checksum changes." | Remove "downstream" (implied).

[§3.4] "Each main-study subject receives 39 behavioral prediction questions; Franklin's legacy battery has 40." -> Keep as is. | Clear and factual.

[§3.4] "The total behavioral-prediction pool is 586 questions across 15 subjects (14 main-study plus Franklin)." -> Keep as is. | Clear.

[§3.4] "Each battery covers 8 to 10 of the 10 fixed behavioral-prediction categories." -> Keep as is. | Clear.

[§3.4] "Leakage audit." -> Keep as is. | Technical term.

[§3.4] "We empirically checked the backward-design no-leakage principle by searching every behavioral-prediction question for a seven-or-more-consecutive-word n-gram appearing verbatim in that subject's held-out corpus." -> "We checked for leakage by searching every behavioral-prediction question for seven-or-more-consecutive-word n-grams appearing in that subject's held-out corpus." | Remove "empirically" (implied by "checked"); "verbatim" is redundant.

[§3.4] "Result: 2 of 586 questions leak (0.34% aggregate)." -> Keep as is. | Clear and factual.

[§3.4] "The 14 main-study subjects leak-check at 0.00%." -> "The 14 main-study subjects show 0.00% leakage." | "Leak-check at" is awkward; "show leakage" is clearer.

[§3.4] "Both leaks are in the Franklin control battery (Q49, Q56), which predates the backward-design constraint and was hand-authored." -> "Both leaks appear in the Franklin control battery (Q49, Q56), which predates the backward-design constraint and was hand-authored." | "Are in" is passive; "appear in" is slightly more active but still acceptable. Keep as is.

[§3.4] "We disclose them here; Franklin's role in the paper is as a high-baseline reference, not as a subject whose quantitative result is load-bearing." -> "We disclose them here; Franklin serves as a high-baseline reference, not as a subject whose quantitative result is central to the claims." | "Load-bearing" is architectural metaphor; "central to the claims" is plainer.

[§3.4.1] "To test whether results are an artifact of this within-Anthropic frontier-model chain, we ran two independent circularity controls." -> "To test whether results depend on the within-Anthropic frontier-model chain, we ran two independent circularity controls." | "Artifact of" is vague; "depend on" is clearer.

[§3.4.1] "Control 1: Independent battery regeneration (GPT-5.4)." -> Keep as is. | Clear heading.

[§3.4.1] "We independently regenerated behavioral prediction batteries for all 13 global subjects using GPT-5.4 with the identical backward-design prompt used for the primary Haiku-generated batteries." -> "We regenerated behavioral prediction batteries for all 13 global subjects using GPT-5.4 with the same backward-design prompt used for the primary Haiku-generated batteries." | "Independently regenerated" is redundant; "identical" → "same."

[§3.4.1] "The regenerated batteries produced the same 39-question count per subject, covered the same 10 behavioral categories (with 8-10 shared per subject), and targeted the same behavioral patterns in the source text." -> Keep as is. | Clear.

[§3.4.1] "Emphasis differed by category: GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions." -> Keep as is. | Clear.

[§3.4.1] "The backward-design methodology constrains the output more than the generating model does." -> Keep as is. | Clear.

[§3.4.1] "Franklin and Hamerton retain their legacy batteries and are not part of Control 1; the 13 global subjects are." -> Keep as is. | Clear.

[§3.4.1] "Full GPT-5.4 batteries are released for independent replication." -> Keep as is. | Clear.

[§3.4.1] "Control 2: Non-Anthropic response chain." -> Keep as is. | Clear heading.

[§3.4.1] "We re-ran the core C5 / C2a / C4a / C2c conditions on three subjects spanning the effect gradient (Ebers at baseline 1.04 with a strong positive effect, Yung Wing at baseline 1.88 with a modest positive effect, and Zitkala-Sa at baseline 2.34 with a negative effect) using two non-Haiku response models (Claude Sonnet and Google Gemini Pro) reading the GPT-5.4-generated batteries." -> "We re-ran conditions C5, C2a, C4a, and C2c on three subjects spanning the effect gradient (Ebers: baseline 1.04, strong positive effect; Yung Wing: baseline 1.88, modest positive effect; Zitkala-Sa: baseline 2.34, negative effect) using two non-Haiku response models (Claude Sonnet and Google Gemini Pro) with GPT-5.4-generated batteries." | Simplify the structure with semicolons and remove "reading."

[§3.4.1] "The combination gives us subject × response-model × battery cells that together test whether the specification effect survives when both the response model and the battery-generation model are outside the Anthropic family." -> "These cells test whether the specification effect persists when both the response model and the battery-generation model are outside the Anthropic family." | Remove "gives us" and "together"; simplify.

[§3.4.1] "Full results are in §4.8." -> Keep as is. | Clear.

[§3.4.1] "Together the two controls address within-Anthropic circularity at two levels." -> "The two controls address within-Anthropic circularity at two levels." | Remove "Together" (implied).

[§3.4.1] "Control 1 holds the response model constant and varies the battery-generation model, testing whether the specification effect depends on Haiku writing the test questions." -> Keep as is. | Clear.

[§3.4.1] "Control 2 holds the battery constant and varies the response model, testing whether the effect depends on Haiku reading and answering them." -> Keep as is. | Clear.

[§3.4.1] "A broader LLM-as-judge circularity, the concern that any LLM panel might systematically favor LLM-produced outputs over human-written alternatives, is not addressed by these controls." -> "A broader concern—that any LLM panel might systematically favor LLM-produced outputs over human-written alternatives—is not addressed by these controls." | Simplify with em-dash.

[§3.4.1] "It is discussed as an open limitation in §6." -> "This is discussed as an open limitation in §6." | "It" is vague; "This" is clearer.

[§3.5] "Each condition is a specific combination of inputs served to the response model against the same behavioral battery." -> "Each condition specifies a combination of inputs served to the response model with the same behavioral battery." | "Against" is awkward; "with" is clearer.

[§3.5] "Every condition is tested on all 14 subjects." -> Keep as is. | Clear.

[§3.5] "The conditions separate into two groups: direct context manipulations (what the model is given), and memory-system configurations (the same representation obtained through a third-party retrieval stack)." -> "Conditions fall into two groups: direct context manipulations (what the model receives) and memory-system configurations (the same representation obtained through third-party retrieval stacks)." | "Separate into" is slightly formal; "fall into" is plainer. "Is given" → "receives." "A third-party" → "third-party."

[§3.5] "Direct context conditions." -> Keep as is. | Clear heading.

[§3.5] "C9 could not be completed for Babur (422,772-word source exceeds the response model's context window)." -> Keep as is. | Clear and factual.

[§3.5] "The single failure is disclosed where C9 numbers appear; the remaining 13 subjects have C9 data." -> Keep as is. | Clear.

[§3.5] "Memory-system conditions." -> Keep as is. | Clear heading.

[§3.5] "Five memory systems are tested: Mem0, Letta, Supermemory, Zep, and Base Layer (our own stack as a fifth reference implementation)." -> "Five memory systems are tested: Mem0, Letta, Supermemory, Zep, and Base Layer (our own implementation)." | Remove "as a fifth reference" (implied by context).

[§3.5] "Each system is evaluated in two configurations:" -> Keep as is. | Clear.

[§3.5] "C1 tests whether the retrieval stack alone reaches behavioral-prediction accuracy comparable to the specification." -> Keep as is. | Clear.

[§3.5] "C3 tests whether the specification composes on top of retrieval when retrieval is already present." -> Keep as is. | Clear.

[§3.5] "Native ingestion variant." -> Keep as is. | Clear heading.

[§3.5] "Each commercial memory system is additionally run in a "native" configuration where the system ingests the raw training corpus directly through its own chunking and extraction pipeline, rather than receiving the identical controlled fact set." -> "Each commercial memory system is additionally run in a 'native' configuration where the system ingests the raw training corpus through its own chunking and extraction pipeline, rather than receiving the controlled fact set." | Remove "directly" and "identical" (implied).

[§3.5] "The controlled configuration holds the input identical across systems; the native configuration reflects each system's real-world deployment." -> "The controlled configuration holds input constant across systems; the native configuration reflects each system's real-world deployment." | "Holds the input identical" is awkward; "holds input constant" is clearer.

[§3.5] "Both configurations are reported so retrieval quality differences and ingestion-pipeline differences can be read separately." -> Keep as is. | Clear.

[§3.5] "Base Layer is run in a single controlled configuration (retrieval uses the same fact set that feeds the specification pipeline)." -> Keep as is. | Clear.

[§3.5] "Letta stateful-agent path." -> Keep as is. | Clear heading.

[§3.5] "Letta exposes two memory modes: archival retrieval (the path tested in C1 / C3 above) and a stateful-agent path where memory blocks are edited incrementally during ingestion and the agent reads from the block directly." -> "Letta exposes two memory modes: archival retrieval (tested in C1 / C3) and a stateful-agent path where memory blocks are edited incrementally during ingestion and the agent reads from the block." | Remove "the path tested in...above" and "directly" (implied).

[§3.5] "The stateful path is architecturally distinct from retrieval-style access and is evaluated as a separate comparison, reported in §4.3.1 alongside other Letta findings rather than as a top-line condition row." -> "The stateful path is distinct from retrieval-style access and is evaluated separately, reported in §4.3.1 alongside other Letta findings rather than as a top-line condition." | Remove "architecturally" (implied); "comparison" → "evaluation"; "condition row" → "condition."

[§3.5] "Wrong-spec control." -> Keep as is. | Clear heading.

[§3.5] "C2c uses random derangement: each subject is assigned another study subject's specification, with a fixed seed (42) ensuring no subject receives its own spec." -> Keep as is. | Clear.

[§3.5] "The derangement eliminates overlap between the wrong spec's target and the true subject." -> Keep as is. | Clear.

[§3.5] "A prior iteration using Franklin's specification for all subjects was run but is not reported in the main results, because Franklin is a known high-pretraining figure whose specification may sit closer to canonical Western profiles than a random study subject's specification would." -> "A prior iteration using Franklin's specification for all subjects was run but is not reported, because Franklin is a known high-pretraining figure whose specification may align more closely with canonical Western profiles than a random study subject's specification." | "Sit closer to" is colloquial; "align more closely with" is more academic.

[§3.5] "The derangement control is the stricter test and is the one reported." -> Keep as is. | Clear.

[§3.5] "Detailed per-condition parameters, exclusion cases, and ingestion specifics are in Appendix C." -> Keep as is. | Clear.

[§3.6] "The primary response model is Claude Haiku 4.5, run across all 14 subjects and every condition in the main matrix." -> Keep as is. | Clear.

[§3.6] "Haiku was chosen as primary because it is the weakest model in the available test pool; an effect that registers on a weaker model is a more conservative claim than one that only surfaces on a frontier model." -> Keep as is. | Clear and well-reasoned.

[§3.6] "Tier 2 response-model expansion." -> Keep as is. | Clear heading.

[§3.6] "To test whether the specification effect depends on the response model being within the Anthropic family, Claude Sonnet 4.6 and Google Gemini 2.5 Pro were additionally run as response models on 3 subjects spanning the effect gradient (Ebers, Yung Wing, Zitkala-Sa) against the GPT-5.4-regenerated batteries from Control 1." -> Keep as is. | Clear.

[§3.6] "Tier 2 results and subject-selection rationale are in §3.4.1 and §4.8." -> Keep as is. | Clear.

[§3.6] "Call-time parameters." -> Keep as is. | Clear heading.

[§3.6] "All response models are called with `temperature=0` and `max_tokens=1024`." -> Keep as is. | Clear and factual.

[§3.6] "Prompt schema." -> Keep as is. | Clear heading.

[§3.6] "A single shared prompt is used across every condition." -> Keep as is. | Clear.

[§3.6] "The system message frames the task as behavioral prediction of a specific person; the user message is the question plus whichever context inputs the condition specifies (§3.5)." -> Keep as is. | Clear.

[§3.6] "Nothing about the prompt changes per condition beyond the injected context block." -> Keep as is. | Clear.

[§3.6] "No prompt instruction tells the model to abstain, answer, hedge, or commit." -> Keep as is. | Clear.

[§3.6] "That was a design decision made at the start of the study." -> "This was a deliberate design choice." | "That was a design decision made at the start" is wordy; simplify.

[§3.6] "Any prompt that coached response behavior would have directly confounded what the conditions are trying to measure, and the model's natural refusal-or-commitment pattern given a specific context is itself part of the phenomenon the study tests." -> Keep as is. | Clear and well-reasoned.

[§3.6] "§4.3 reports the hedging-rate shift across conditions and treats it as a substantive finding rather than a behavior to suppress." -> Keep as is. | Clear.

[§3.7] "Every response is scored 1-5 by seven LLM judges against the verbatim held-out ground-truth passage." -> "Every response is scored 1-5 by seven LLM judges against the held-out ground-truth passage." | "Verbatim" is redundant; "ground-truth" already implies exact match.

[§3.7] "Human annotation at this scale is feasible: roughly 14 subjects × 40 questions × 15+ conditions sits on the order of thousands of judgments, within reach of a small annotation team." -> "Human annotation at this scale is feasible: roughly 14 subjects × 40 questions × 15+ conditions yields thousands of judgments, within reach of a small annotation team." | "Sits on the order of" is colloquial; "yields" is clearer.

[§3.7] "It was not done here." -> Keep as is. | Clear and direct.

[§3.7] "This is a limited-budget solo research effort, and the deliberate trade-off was to run more conditions and more judges rather than fewer conditions with human annotation." -> "This is a limited-budget solo research effort; the deliberate trade-off was to run more conditions and more judges rather than fewer conditions with human annotation." | Change period to semicolon for better flow.

[§3.7] "That trade-off is the central evaluation limitation of the study; how we work inside it is what this section describes." -> Keep as is. | Clear.

[§3.7] "The evaluation is deliberately recursive." -> Keep as is. | Clear.

[§3.7] "Response models are evaluated by judges (§3.7.1)." -> Keep as is. | Clear.

[§3.7] "Judges are evaluated by calibration diagnostics (§3.7.2), inter-judge agreement metrics (§3.7.4), and post-hoc rubric-handling audits (§3.7.6)." -> Keep as is. | Clear.

[§3.7] "No single layer is treated as ground truth; each layer's behavior is itself measured and disclosed, and where a layer's behavior diverges from what the rubric intends, the divergence is flagged rather than corrected silently." -> Keep as is. | Clear and well-reasoned.

[§3.7] "The paper's rigor in the absence of human annotation comes from this stacked-instrument structure, not from trusting any one step." -> Keep as is. | Clear.

[§3.7] "Scoring rubric." -> Keep as is. | Clear heading.

[§3.7] "What a 5 means and does not mean." -> Keep as is. | Clear heading.

[§3.7] "A score of 5 reflects alignment with one specific behavioral sample: the held-out ground-truth passage the question is drawn from." -> Keep as is. | Clear.

[§3.7] "It is not a claim that the response fully represents the subject in some absolute sense, and it is not a claim that the same response would score 5 on a different held-out passage from the same subject." -> Keep as is. | Clear.

[§3.7] "Each question tests one behavioral sample at a time; the aggregate across roughly 40 questions per subject is what the paper reads as the subject-level score." -> Keep as is. | Clear.

[§3.7] "Reading score differences." -> Keep as is. | Clear heading.

[§3.7] "A move from 2 to 3 is the difference between "he would probably dislike it, as most artists would" and "he would judge the landscape aesthetically before deciding whether to engage its people."" -> Keep as is. | Clear.

[§3.7] "The first answer is pattern-free and could apply to many nineteenth-century subjects; the second identifies a subject-specific behavioral tendency visible in Hamerton's actual writing." -> Keep as is. | Clear.

[§3.7] "A move from 3 to 4 is the difference between identifying one behavioral tendency and identifying several that work together." -> Keep as is. | Clear.

[§3.7] "§3.7.3 develops the formal cross-anchor rule used throughout the results section." -> Keep as is. | Clear.

[§3.7.1] "Judge Panel." -> Keep as is. | Clear heading.

[§3.7.1] "Seven judges from three providers." -> Keep as is. | Clear.

[§3.7.1] "The multi-judge panel, not the single judge, is what gives the numeric aggregate its weight." -> "The multi-judge panel, not the single judge, provides the numeric aggregate its weight." | "Gives...its weight" is slightly colloquial; "provides...weight" is more academic.

[§3.7.1] "Zheng et al. (2023) established that a single strong LLM judge correlates with human judges on comparable tasks at rates similar to human-human agreement." -> Keep as is. | Clear and well-cited.

[§3.7.1] "Subsequent panel-based work (Verga et al. 2024 and follow-ons) showed that aggregating multiple LLM judges past a small panel size further tightens agreement and reduces single-model idiosyncrasy." -> Keep as is. | Clear.

[§3.7.1] "Seven judges across three providers is well past that threshold." -> Keep as is. | Clear.

[§3.7.1] "Judge invocations are independent." -> Keep as is. | Clear.

[§3.7.1] "Each judge receives the held-out ground-truth passage, the subject context (name, source), the prediction question, and the response to score." -> Keep as is. | Clear.

[§3.7.1] "Judges do not see other judges' scores." -> Keep as is. | Clear.

[§3.7.2] "Calibration." -> Keep as is. | Clear heading.

[§3.7.2] "Five judges (Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) were tested against four diagnostic inputs with known correct scores before study scoring began." -> Keep as is. | Clear.

[§3.7.2] "Sonnet and Opus are not on the diagnostic suite; they enter the panel on inter-judge agreement properties only." -> Keep as is. | Clear.

[§3.7.2] "Diagnostic tests." -> Keep as is. | Clear heading.

[§3.7.2] "Results." -> Keep as is. | Clear heading.

[§3.7.2] "Four of five judges score verbatim matches at 5.0; Gemini Pro is the outlier at 4.15." -> Keep as is. | Clear.

[§3.7.2] "Length sensitivity varies: Haiku does not penalize padding; Gemini Pro penalizes it severely (5.0 to 1.20)." -> Keep as is. | Clear.

[§3.7.2] "GPT-5.4 has the tightest overall calibration profile across the four diagnostics." -> Keep as is. | Clear.

[§3.7.2] "Use of calibration data." -> Keep as is. | Clear heading.

[§3

---

## Chunk: §4.1 Gradient + 4.1.1 + 4.1.2

# Register Review: §4.1–4.1.2

---

## Marketing Register Flags

[§4.1] "Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it." -> "Adding a Behavioral Specification changes the category of answer the AI produces, not merely the magnitude." | Oversold framing; "not just X, but Y" is pitch-deck rhetoric

[§4.1] "Mean score lift: **+0.89 points**." -> "Mean score increase: +0.89 points." | "Lift" is marketing jargon for improvement

[§4.1] "The mean number hides what is happening at the response level." -> "The mean obscures response-level patterns." | Vague-strength descriptor; "hides" is melodramatic

[§4.1] "**Of the 351 individual responses in the low-baseline slice, 55.0% crossed at least one rubric integer anchor upward when the specification was added.**" -> "55.0% of the 351 responses in the low-baseline slice moved upward by at least one rubric integer when the specification was added." | Passive construction with "crossed" inflates the action; "when the specification was added" is clearer than "when added"

[§4.1] "The AI's answer moved from one category of response to a qualitatively different category." -> "The AI's answer shifted to a different response category." | "Qualitatively different" is vague-strength descriptor; "moved" is softer than needed

[§4.1] "One of every three low-baseline responses moves from 'cannot engage' to actual engagement." -> "One in three low-baseline responses shifts from refusal to engagement." | "Actual engagement" is vague-strength; "cannot engage" is imprecise

[§4.1] "Another one in five makes a larger jump." -> "One in five shows a larger increase." | "Jump" is informal/marketing; "larger" alone is sufficient

[§4.1] "Only one response in fifteen gets worse." -> "One in fifteen declines." | "Gets worse" is colloquial; "only" is pitch-deck hedging

[§4.1] "**Three representative examples below show the different ways the specification can help.**" -> "Three examples below illustrate distinct mechanisms by which the specification improves responses." | "Can help" is vague; "different ways" is imprecise; "show" is weaker than "illustrate"

[§4.1] "These are not cherry-picked to impress; they are selected to show three distinct mechanisms..." -> "These examples were selected to illustrate three distinct mechanisms..." | "Not cherry-picked to impress" is defensive marketing language; remove the justification and state selection criteria directly

[§4.1] "Hedge reduction is common but not the only thing going on." -> "Hedge reduction is one mechanism among several." | "Not the only thing going on" is colloquial

[§4.1] "The specification also corrects wrong predictions in the opposite direction, and it enables interpretive inference from character patterns when retrieved facts are insufficient." -> "The specification corrects directionally incorrect predictions and enables inference from character patterns when retrieved facts are insufficient." | "Also" is filler; "wrong predictions in the opposite direction" is wordy

[§4.1, Example A] "**What the specification did.**" -> "Mechanism." | Section header is colloquial; use standard academic label

[§4.1, Example A] "The baseline failed to identify which Ebers was being asked about and refused to predict." -> "The baseline could not identify which Ebers was referenced and declined to predict." | "Failed" is judgmental; "refused" is anthropomorphic

[§4.1, Example A] "The specification resolved the identity question and enabled a substantive interpretive claim..." -> "The specification resolved the identity ambiguity and supported a specific interpretive claim..." | "Resolved" is too strong; "substantive" is vague-strength; "enabled" is marketing verb

[§4.1, Example B] "**What the specification did.**" -> "Mechanism." | Consistency with Example A

[§4.1, Example B] "Facts alone produced a confident but directionally wrong prediction (commander accepts help)." -> "Facts alone produced a directionally incorrect prediction (commander accepts help)." | "Confident but wrong" is editorializing; "directionally wrong" is imprecise

[§4.1, Example B] "The specification corrected the prediction to match the ground truth (Cortes refuses)." -> "The specification produced a prediction matching the ground truth (Cortes refuses)." | "Corrected to match" is outcome-focused marketing language; state the result directly

[§4.1, Example B] "The collective review panel unanimously called this mechanism directional correction of a prediction: the specification encoded Cortes's pattern of physical self-reliance and performative leadership, overriding the model's generic 'good leaders accept help' default." -> "The review panel identified this as directional correction: the specification captured Cortes's pattern of physical self-reliance and performative leadership, which overrode the model's default assumption." | "Unanimously called" is pitch-deck emphasis; "encoded" is verb-noun inflation; "overriding" is weaker than "overrode"

[§4.1, Example C] "**What the specification did.**" -> "Mechanism." | Consistency

[§4.1, Example C] "The shift is from refusal-to-predict to a specific, accurate behavioral prediction that closely tracks Seacole's verbatim held-out account..." -> "The model shifted from declining to predict to producing a specific prediction that aligns with Seacole's held-out account..." | "Refusal-to-predict" is compound-noun inflation; "closely tracks" is vague-strength; "verbatim" is unnecessary

[§4.1, Example C] "The specification enabled the model to generalize from Seacole's established compassionate-caregiving pattern — documented in the facts but not explicitly mapped to this scenario — to the specific untested situation." -> "The specification allowed the model to apply Seacole's documented compassionate-caregiving pattern to the untested scenario." | "Enabled" is marketing verb; "established" is vague-strength; "not explicitly mapped" is wordy; "specific untested situation" is redundant

[§4.1, Example C] "The collective review panel unanimously identified this as interpretive inference beyond retrieved facts: a mechanism that retrieval alone cannot produce because it requires applying character-level pattern to novel situations." -> "The review panel identified this as inference beyond retrieved facts, requiring application of character patterns to novel situations." | "Unanimously identified" is pitch-deck emphasis; "mechanism that retrieval alone cannot produce" is wordy; "character-level pattern" is jargon

[§4.1, Example C, rubric note] "The judge panel scored this abstention at 2.80, not at 1.00 (the rubric anchor for 'refuses or off-base'). This reflects a rubric-level issue we encountered in both directions across the study: judges treat honest abstentions as partial engagement (scoring ~2.5-3.0) rather than as refusals, and they sometimes penalize spec-induced honest abstentions where the specification appropriately declined to invent detail..." -> "Judges scored this abstention at 2.80 rather than 1.00, reflecting a rubric inconsistency: honest abstentions were scored as partial engagement (~2.5–3.0) rather than refusals, and spec-induced abstentions were sometimes penalized when the specification appropriately declined to invent detail..." | "Rubric-level issue we encountered in both directions" is vague; "appropriately declined" is editorializing

[§4.1] "**The lift is not uniform across subjects. It depends on how much the AI already knows about the person.**" -> "The improvement varies by subject baseline. Subjects with lower pretraining coverage show larger gains." | "Lift" is marketing jargon; "how much the AI already knows" is colloquial; "Plain version:" is unnecessary

[§4.1] "Plain version: the less the model's pretraining has to work from, the more the specification can add. The more the model already knows, the less room the specification has to help, and on the highest-baseline subjects it can mildly hurt." -> [Delete; this is redundant with the preceding sentence] | Unnecessary simplification; already stated clearly

[§4.1] "Linear regression of the facts-plus-specification effect against baseline:" -> "Linear regression of specification effect on baseline:" | "Facts-plus-specification effect against baseline" is wordy

[§4.1, table note] "Rank agreement across the 5-judge primary panel is high (pairwise Spearman ρ = 0.89 to 0.98, §3.7.4), so the directional claim rides on broad agreement across three providers rather than on any one judge's scoring." -> "Rank agreement across the 5-judge primary panel is high (pairwise Spearman ρ = 0.89–0.98, §3.7.4), indicating broad consensus across judges." | "Rides on" is colloquial; "rather than on any one judge's scoring" is unnecessary

[§4.1] "**A note on baseline measurement.** The measured C5 baseline (mean 1.52 on the low-baseline slice) is slightly inflated by a length-driven rubric effect." -> "Baseline measurement note: The measured C5 baseline (mean 1.52 on the low-baseline slice) is slightly elevated due to a length-driven rubric effect." | "Slightly inflated" is vague-strength; "A note on" is colloquial

[§4.1] "A post-hoc validity audit (§3.7.6) found that longer no-context responses (which include more hedging, adjacent-fact recitation, and disambiguation language) score higher on average than short refusals, with length-score correlation r = 0.604 specifically within C5 responses." -> "A post-hoc validity audit (§3.7.6) found a length-score correlation of r = 0.604 within C5 responses, with longer responses scoring higher on average." | "Found that longer responses score higher" is passive; "which include more hedging..." is unnecessary detail in this context

[§4.1] "The true no-context prediction accuracy is likely lower than 1.52, which makes the spec-effect gap slightly *larger* than the reported +0.89 mean lift." -> "The true no-context accuracy is likely lower than 1.52, which would increase the specification effect." | "Spec-effect gap" is jargon; "mean lift" is marketing jargon

[§4.1] "We report the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact, and flag the direction of the bias here so readers can interpret the effect size accordingly." -> "We report the measured value to preserve the pre-registered analysis plan and note the direction of bias for interpretation." | "Keep intact" is colloquial; "flag the direction" is informal

[§4.1.1] "Franklin is not a subject of the main gradient. He is a known-figure control." -> "Franklin serves as a known-figure control and is not part of the main gradient analysis." | Repetitive; combine into one sentence

[§4.1.1] "Benjamin Franklin's *Autobiography* is one of the most widely cited autobiographical works in American public-domain literature, and every current-generation LLM has substantial pretraining representation of both the person and the specific text." -> "Benjamin Franklin's *Autobiography* is widely represented in public-domain literature and in current-generation LLM pretraining." | "One of the most widely cited" is vague-strength; "substantial pretraining representation of both the person and the specific text" is wordy

[§4.1.1] "Franklin's C5 baseline on the 5-judge primary panel is 3.77 (higher on the 7-judge aggregate with Gemini included, see §4.5). This is well above the next-highest main-study subject (Equiano at 2.77)." -> "Franklin's C5 baseline is 3.77 on the 5-judge panel (3.XX on the 7-judge aggregate; see §4.5), substantially higher than the next-highest subject (Equiano at 2.77)." | "Well above" is vague-strength; "This is" is filler

[§4.1.1] "Both spec-containing conditions score below Franklin's baseline. The specification alone (C2a) drops 0.40 points; facts plus specification (C4a) drops 0.13. The drop is more pronounced on C2a than on C4a because the specification alone competes with strong pretraining without the facts to re-anchor the response." -> "Both spec-containing conditions score below baseline: C2a drops 0.40 points, C4a drops 0.13. The larger drop in C2a reflects competition between the specification and strong pretraining without facts to re-anchor the response." | "Drops" is informal; "more pronounced" is vague-strength; "because" is explanatory but could be tightened

[§4.1.1] "Adding facts back partially restores the AI's own working model of Franklin." -> "Adding facts partially restores the model's pretraining representation." | "AI's own working model" is anthropomorphic jargon

[§4.1.1] "This is the direction H2a predicts. Where the AI already has the person well-modeled from pretraining, the specification does not add representational signal and can mildly interfere." -> "This pattern aligns with H2a: when pretraining provides strong representation, the specification adds no signal and may slightly interfere." | "This is the direction H2a predicts" is colloquial; "well-modeled" is vague; "can mildly interfere" is hedging

[§4.1.1] "The gradient mechanism reads through cleanly at both ends of the spectrum. Strong positive lift where the baseline is low. No lift or mild interference where the baseline is high." -> "The gradient mechanism is consistent at both extremes: strong gains at low baselines, no gains or slight interference at high baselines." | "Reads through cleanly" is colloquial; "Strong positive lift" is marketing jargon; "No lift" is jargon; "mild interference" is vague-strength

[§4.1.2] "The main gradient is built entirely on historical subjects with public-domain autobiographies. Every one sits above the pretraining baseline of a typical living person whose private reasoning is not in any training corpus." -> "The main gradient uses only historical subjects with public-domain autobiographies. A typical living person whose private reasoning is not in any training corpus would sit below this baseline." | "Built entirely on" is wordy; "Every one sits above" is imprecise

[§4.1.2] "§1.4 made the extrapolation argument that such a person should sit at or below the rubric floor. We ran a methodology-matched replication on one living individual to test this directly." -> "§1.4 predicts that such a person would score at or below the rubric floor. We tested this with a methodology-matched replication on one living individual." | "Made the extrapolation argument" is wordy; "test this directly" is vague

[§4.1.2] "**Setup.** The author's private conversation history with AI systems (ChatGPT and Claude, roughly four years) was loaded into the same pipeline used for the 14 historical subjects." -> "The author's private conversation history (ChatGPT and Claude, ~4 years) was processed through the same pipeline as the historical subjects." | "Loaded into" is colloquial; "roughly four years" is imprecise

[§4.1.2] "The corpus was split 50/50 by message ID (seed 42), producing a training half and a held-out half." -> "The corpus was split 50/50 by message ID (seed 42) into training and held-out halves." | "Producing" is passive; "training half and a held-out half" is repetitive

[§4.1.2] "The full-stack Behavioral Specification (anchors + core + predictions + brief) was authored from the training half only, following §3.3." -> "The Behavioral Specification was authored from the training half only (§3.3)." | "Full-stack" is jargon; "anchors + core + predictions + brief" is unnecessary detail here

[§4.1.2] "A 40-question behavioral-prediction battery was backward-designed from the held-out half only, following §3.4." -> "A 40-question battery was designed from the held-out half only (§3.4)." | "Behavioral-prediction battery" is jargon; "backward-designed" is jargon; "following" is unnecessary

[§4.1.2] "No held-out passage was seen by the spec-generation pipeline." -> "The spec-generation pipeline did not access held-out passages." | "Seen by" is anthropomorphic

[§4.1.2] "Claude Haiku 4.5 produced responses under five conditions (C5, C2a, C2c, C4, C4a). Five primary judges scored each response against the verbatim held-out passage." -> "Responses were generated under five conditions and scored by five judges against held-out passages." | "Produced responses under five conditions" is passive; "verbatim held-out passage" is redundant

[§4.1.2] "**Results (5-judge primary, N = 40).**" -> "Results (5-judge primary panel, N = 40)" | "Primary" is sufficient; "5-judge primary" is redundant

[§4.1.2] "**Anchor crossings C5 → C4a:** 30 of 40 responses moved up at least one rubric integer anchor; 0 moved down; 10 stayed in the same band. Upward crossing rate **75.0%**." -> "Anchor crossings (C5 → C4a): 30 of 40 responses increased by at least one rubric level, 0 decreased, 10 remained unchanged. Upward crossing rate: 75.0%." | "Moved up" is colloquial; "rubric integer anchor" is jargon; "stayed in the same band" is imprecise

[§4.1.2] "**Wrong-spec control reads through, and the gap partitions cleanly.**" -> "Wrong-spec control results and gap partitioning." | "Reads through" is colloquial; "partitions cleanly" is vague-strength

[§4.1.2] "Serving Franklin's specification in place of the correct author specification still lifts the score above baseline (+1.56 vs. +1.84 for the correct spec), a smaller-than-expected gap relative to the main-study fixed-derangement pattern..." -> "Franklin's specification produced a +1.56 gain vs. +1.84 for the correct specification, a smaller gap than expected relative to the main-study derangement pattern..." | "Lifts the score" is marketing jargon; "smaller-than-expected gap" is vague; "relative to" is wordy

[§4.1.2] "...though Franklin was not in the main-study derangement mapping." -> "[Delete or move to footnote; interrupts flow]" | Parenthetical aside breaks sentence flow

[§4.1.2] "The main-study data lets us partition the author's +1.56 into two components." -> "The main-study data allows decomposition of the author's +1.56 gain into two components." | "Lets us partition" is colloquial; "into two components" is jargon

[§4.1.2] "First, a baseline-driven component: in the main-study wrong-spec control (Hamerton receives Franklin's spec; Sunity Devee and Ebers each receive their fixed-derangement substitute per `scripts/run_global_rerun.py`), the three subjects with baselines in the author's range (Sunity Devee C5 = 1.03, Ebers 1.02, Hamerton 1.26) receive wrong-spec Δ of +0.20 to +0.30 with mean **+0.25** on the 5-judge primary panel; at higher baselines (C5 > 2) the wrong-spec controls are consistently negative." -> "First, a baseline-driven component: in the main-study wrong-spec control, subjects with baselines in the author's range (Sunity Devee 1.03, Ebers 1.02, Hamerton 1.26) showed wrong-spec gains of +0.20 to +0.30 (mean +0.25), while higher-baseline subjects showed consistent declines." | Extremely dense; see dense flag below

[§4.1.2] "Roughly 0.25 of the author's +1.56 is baseline-mediated: any structured content is worth more when the rubric starts at the floor." -> "Approximately 0.25 of the +1.56 gain reflects baseline effects: any structured content provides greater benefit at floor-level baselines." | "Roughly" is colloquial; "is worth more" is vague; "when the rubric starts at the floor" is imprecise

[§4.1.2] "Second, a content-overlap component: five of the author's twelve behavioral anchors have direct Franklin analogues (systematic self-grading against a named rubric, persistent tracked gap between stated rule and actual behavior, rationalist-empiricist disposition, compression-as-quality, moral aspiration without claim of arrival)." -> "Second, a content-overlap component: five of the author's twelve anchors align with Franklin's (systematic self-grading, persistent rule-behavior gaps, rationalist-empiricist disposition, compression-as-quality, moral aspiration without claim of arrival)." | "Have direct Franklin analogues" is wordy; "behavioral anchors" is jargon; "compression-as-quality" is invented compound noun

[§4.1.2] "The remaining ~1.31 points of lift reflects this convergence." -> "The remaining ~1.31 points reflect content overlap." | "Points of lift" is marketing jargon; "reflects this convergence" is vague

[§4.1.2] "The per-question evidence is consistent with content overlap rather than uniform floor-effect: Franklin-spec outperforms the correct spec on 5 of 40 questions (Q11 most dramatically, gap −2.40) on questions where the two personas' anchors align; the correct spec outperforms Franklin by ≥1.2 points on 4 questions in technical domains where Franklin has no content handle." -> "Per-question analysis supports content overlap: Franklin-spec outperforms on 5 questions where anchors align (Q11: −2.40), while the correct spec outperforms on 4 technical questions where Franklin lacks relevant content." | "Consistent with content overlap rather than uniform floor-effect" is wordy; "personas' anchors" is jargon; "has no content handle" is colloquial

[§4.1.2] "A truly arbitrary wrong-spec at this baseline would produce a floor-effect lift near +0.25, not +1.56. The 0.28-point gap between C2c and C2a therefore reflects an atypically favorable wrong-spec draw for this subject, not a weakening of content specificity." -> "An arbitrary wrong-spec at this baseline would produce ~+0.25 gain, not +1.56. The 0.28-point gap between C2c and C2a therefore reflects favorable content overlap, not weakened specificity." | "Truly arbitrary" is colloquial; "floor-effect lift" is jargon; "atypically favorable wrong-spec draw" is vague; "weakening of content specificity" is jargon

[§4.1.2] "The main-study wrong-spec controls (§1.3 and §4.3) remain the load-bearing tests for H3; the pilot is consistent with them." -> "The main-study wrong-spec controls (§1.3, §4.3) remain the primary tests for H3; the pilot is consistent with these results." | "Load-bearing tests" is jargon; "consistent with them" is vague

[§4.1.2] "**Reading the numbers against the main gradient.**" -> "Comparison to main gradient." | Colloquial header

[§4.1.2] "The baseline 1.03 sits at the rubric floor, below every one of the 14 historical subjects." -> "The baseline of 1.03 is at the rubric floor, below all 14 historical subjects." | "Sits at" is colloquial; "every one of" is redundant

[§4.1.2] "This is the empirical confirmation of §1.4's claim that a person whose private reasoning is not in any training corpus should register at or below the floor: the AI has essentially no model of this specific person from pretraining alone." -> "This confirms §1.4's prediction: a person not represented in training data scores at or below the floor, as the model has no pretraining representation." | "Empirical confirmation of §1.4's claim" is wordy; "register at or below" is jargon; "essentially no model" is vague

[§4.1.2] "The +2.00 lift under facts-plus-spec is the largest in the study (historical maximum was Hamerton at +1.51)." -> "The +2.00 gain under facts-plus-spec is the largest observed (historical maximum: Hamerton +1.51)." | "Lift" is marketing jargon; "was" is passive

[§4.1.2] "The 75% anchor-crossing rate exceeds the 55% on the historical low-baseline slice." -> "The 75% anchor-crossing rate exceeds the 55% rate on the historical low-baseline slice." | Minor: "rate" is implied but should be explicit

[§4.1.2] "None of the 40 responses got worse." -> "No responses declined." | "Got worse" is colloquial

[§4.1.2] "The gradient prediction reads through: the population the model knows the least about is the population where the specification has the largest effect." -> "The gradient prediction holds: the population with the least pretraining representation shows the largest specification effect." | "Reads through" is colloquial; "the population the model knows the least about" is wordy

[§4.1.2] "The pilot is a single living subject and cannot substitute for a multi-subject replication. That multi-subject replication is the leading follow-up in §8." -> "This single-subject pilot cannot substitute for multi-subject replication, which is the primary follow-up (§8)." | "Cannot substitute for" is wordy; "leading follow-up" is vague

[§4.1.2] "Raw data stays in a private working directory at `_internal/aarik_clean_pilot/` and is not included in the public repository." -> "Raw data are in a private directory (`_internal/aarik_clean_pilot/`) and not included in the public repository." | "Stays in" is colloquial; "is not included" is passive

[§4.1.2] "Summary statistics, battery checksums, and the leakage audit are reproducible from the manifest referenced in §8 Future Work." -> "Summary statistics, battery checksums, and leakage audit details are reproducible from the manifest in §8." | "Reproducible from the manifest referenced in §8 Future Work" is wordy

---

## Dense Passages

[dense §4.1.2] "First, a baseline-driven component: in the main-study wrong-spec control (Hamerton receives Franklin's spec; Sunity Devee and Ebers each receive their fixed-derangement substitute per `scripts/run_global_rerun.py`), the three subjects with baselines in the author's range (Sunity Devee C5 = 1.03, Ebers 1.02, Hamerton 1.26) receive wrong-spec Δ of +0.20 to +0.30 with mean **+0.25** on the 5-judge primary panel; at higher baselines (C5 > 2) the wrong-spec controls are consistently negative." -> Break into: (1) "First, a baseline-driven component. In the main-study wrong-spec control, subjects with baselines in the author's range (Sunity Devee 1.03, Ebers 1.02, Hamerton 1.26) showed wrong-spec gains of +0.20 to +0.30 (mean +0.25 on the 5-judge panel). At higher baselines (C5 > 2), wrong-spec controls consistently declined." | This sentence embeds three nested clauses, a code reference, and a parenthetical list. Split into 2–3 sentences.

[dense §4.1.2] "The per-question evidence is consistent with content overlap rather than uniform floor-effect: Franklin-spec outperforms the correct spec on 5 of 40 questions (Q11 most dramatically, gap −2.40) on questions where the two personas' anchors align; the correct spec outperforms Franklin by ≥1.2 points on 4 questions in technical domains where Franklin has no content handle." -> Break into: (1) "Per-question analysis supports content overlap. Franklin-spec outperforms on 5 questions where anchors align, most dramatically on Q11 (gap −2.40). The correct spec outperforms on 4 technical questions where Franklin lacks relevant content (≥1.2-point advantage)." | Semicolon joins two independent claims; split into 3 sentences for clarity.

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.1 (main gradient) | 2 | Heavy marketing register: "lift," "helps," "enables," "reads through cleanly," "hides," "moved," "can help." Oversold framings ("not just X but Y," "the key to"). Vague-strength descriptors ("significant," "meaningful," "actual engagement"). Defensive language ("not cherry-picked to impress"). |
| §4.1.1 (Franklin control) | 3 | Moderate marketing: "well-modeled," "can mildly interfere," "reads through cleanly," "strong positive lift." Cleaner than §4.1 but still uses jargon ("representational signal," "working model"). |
| §4.1.2 (living-user replication) | 2 | Heavy marketing and jargon: "lifts the score," "lets us partition," "load-bearing tests," "reads through," "got worse," "the population the model knows the least about." Dense sentences with nested clauses. Invented compounds ("compression-as-quality"). |

---

## Summary

**Total flags: 87 instances of marketing register or jargon**

**Primary issues:**
1. **Marketing verbs** dominate: "lift," "help," "enable," "reads through," "got worse"
2. **Vague-strength descriptors** throughout: "significant," "meaningful," "substantial," "well-modeled," "mildly," "cleanly"
3. **Pitch-deck framings**: "not just X but Y," "the key to," "load-bearing," "flagship"
4. **Jargon inflation**: "mechanism," "dynamic," "representational signal," "working model," "content handle," "compression-as-quality"
5. **Defensive language**: "not cherry-picked to impress," "not a weakening of"
6. **Colloquial prose**: "stays in," "got worse," "reads through," "lets us partition," "the population the model knows the least about"
7. **Dense sentences** with nested clauses, parenthetical asides, and code references (§4.1.2 especially)

**Cleanest passages:** The statistical tables and results summaries (e.g., "Results (5-judge primary, N = 40)") are clean. The methodology descriptions in §4.1.2 setup are relatively clear.

**Dirtiest passages:** §4.1 opening, Examples A–C ("What the specification did" sections), §4.1.2 wrong-spec control explanation.

---

## Chunk: §4.2 Compression + 4.2.1

# Editorial Review: §4.2 & §4.2.1

## Marketing Register Flags

[§4.2 intro] "Context works." -> "Context improves prediction." | Colloquial marketing opener; academic prose should state the finding directly.

[§4.2] "The compact specification captures the large majority of that lift." -> "The compact specification recovers most of the performance gain." | "Captures...lift" is pitch-deck framing; use neutral outcome language.

[§4.2] "The corpus's edge is real but small" -> "The corpus shows a measurable but modest advantage" | "Edge" is competitive/marketing language; "advantage" is more neutral.

[§4.2] "The efficiency claim in one metric" -> "Efficiency measured by predictive gain per 1,000 tokens" | "The efficiency claim" presells; state what is being measured.

[§4.2] "The dose-response curve has a steep initial slope and a long plateau." -> "The dose-response curve shows rapid initial gains followed by diminishing returns." | "Steep...long plateau" is descriptive marketing; use standard pharmacology/economics terminology.

[§4.2] "The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document." -> "Behaviorally relevant signal in autobiographical text is sparse and compressible; most predictive content fits into a compact structured document." | "Most of what matters can be packaged" is marketing framing; use passive/neutral construction.

[§4.2 table intro] "In the color-rendered PDF, low-baseline rows are tinted to mark the population of relevance; the C8 − C2a gap column is shaded to make the spec-vs-corpus difference visible at a glance." -> "Low-baseline rows are tinted; the C8 − C2a gap column is shaded to highlight the spec-vs-corpus difference." | "Mark the population of relevance" and "visible at a glance" are UX/design-speak.

[§4.2 after table] "What the aggregate numbers say." -> "Aggregate results." | Colloquial framing; use standard heading.

[§4.2.1 intro] "A cleaner unit:" -> "An alternative unit:" | "Cleaner" is a vague-strength descriptor (marketing register).

[§4.2.1 intro] "This is a **win rate against a no-context baseline**, structurally parallel to the per-prompt win-rate convention used in LLM evaluation" -> "This metric—win rate against no-context baseline—parallels per-prompt win-rate conventions in LLM evaluation." | "Structurally parallel" is inflated; "parallels" is sufficient.

[§4.2.1] "The reporting triplet." -> "Reporting structure." | "Triplet" is invented compound noun; use plain term.

[§4.2.1] "Win rate alone hides the magnitude of help and harm." -> "Win rate alone does not capture the magnitude of improvement or degradation." | "Help and harm" is colloquial; use neutral outcome terms.

[§4.2.1] "The magnitude column is the important row of this table." -> "The magnitude column is critical for interpretation." | "Important row" is vague emphasis; state why it matters.

[§4.2.1] "The metric is not capturing trivial +0.02-per-question gains; the underlying improvements are substantive." -> "The metric reflects meaningful improvements, not marginal gains (median Δ = +1.00)." | "Substantive" is a vague-strength descriptor; support with data.

[§4.2.1] "On the 9 low-baseline subjects, **7 out of every 10 questions improve with the specification alone**, roughly 1 in 10 tie, and fewer than 1 in 6 worsen." -> "On the 9 low-baseline subjects, 70.9% of questions improve with the specification alone, 14.0% tie, and 15.1% worsen." | Colloquial framing ("7 out of every 10") in academic prose; use percentages.

[§4.2.1] "Every context condition clears a 70% win rate on the population of relevance." -> "Every context condition achieves at least a 70% improvement rate on the low-baseline population." | "Clears" is marketing language (sports/performance register).

[§4.2.1] "The specification sits within 8 percentage points of the raw corpus (70.9% vs. 78.3%) at an order of magnitude less context." -> "The specification achieves 70.9% improvement rate versus 78.3% for raw corpus, using one order of magnitude less context." | "Sits within" is colloquial; "achieves" is more direct.

[§4.2.1 head-to-head section] "The raw corpus wins more head-to-head matchups than the spec alone, but the spec wins a non-trivial third of them at a fraction of the cost." -> "The raw corpus outperforms the specification in 54.1% of questions; the specification outperforms in 32.8%, at substantially lower context cost." | "Wins...non-trivial third...fraction of the cost" is competitive/marketing framing.

[§4.2.1] "On the combined conditions, the 7K-token facts + spec package wins 36.9% of questions outright against the much larger corpus + spec package." -> "The 7K-token facts + spec condition outperforms the corpus + spec condition in 36.9% of questions." | "Wins...outright...package" is marketing language; use neutral comparative terms.

[§4.2.1] "Positioning as a secondary reporting metric." -> "Secondary reporting metric." | "Positioning as" is pitch-deck framing.

[§4.2.1] "A per-question win rate against a no-context baseline makes behavioral prediction directly comparable across future studies in a way that mean scores do not." -> "A per-question win rate against a no-context baseline enables comparison across studies without requiring matched rubrics or judges." | "In a way that mean scores do not" is marketing contrast; state the advantage directly.

[§4.2.1] "We propose this metric as a **candidate secondary reporting axis** for future AI-personalization work, always paired with mean-score information, never replacing it." -> "We propose this metric as a secondary reporting measure for future AI-personalization work, always paired with mean-score information." | "Reporting axis" is invented jargon; "measure" is standard. "Never replacing it" is prescriptive marketing tone.

[§4.2.1 limitations] "The panel-reviewed limitations worth flagging explicitly for any future use:" -> "Known limitations for future adoption:" | "Panel-reviewed...worth flagging explicitly" is self-promotional framing.

[§4.2.1] "**Tiny-gain inflation.**" -> "Inflation from marginal gains." | Colloquial label; use neutral descriptor.

[§4.2.1] "A method producing +0.02-point gains on 80% of questions would register as a 80% improvement rate. The magnitude triplet (median Δ when improved) is the guard:" -> "A method producing +0.02-point gains on 80% of questions would register as 80% improvement rate. The magnitude triplet (median Δ when improved) prevents this:" | "Guard" is colloquial; "prevents" is more precise.

[§4.2.1] "Our low-baseline specification has median Δ = +1.00, so this failure mode does not apply to the reported numbers; it is a known trap for anyone adopting the metric." -> "Our specification has median Δ = +1.00, so this failure mode does not apply here. Future adopters should monitor for this." | "Known trap" is colloquial; "should monitor for" is more formal.

[§4.2.1] "**Hidden catastrophic harm.**" -> "Undetected harm concentration." | "Catastrophic" is marketing hyperbole; use neutral descriptor.

[§4.2.1] "A method that improves 85% and catastrophically harms 15% would look strong. The worsening-magnitude column is the guard: median worsening of −0.40 on spec-alone indicates the hurt is bounded." -> "A method improving 85% while degrading 15% could appear favorable. The worsening-magnitude column prevents this: median degradation of −0.40 indicates bounded harm." | "Look strong...hurt is bounded" is colloquial; use neutral language.

[§4.2.1] "**Easy-baseline gaming.**" -> "Baseline selection bias." | "Gaming" is colloquial; use technical term.

[§4.2.1] "Improvement rates can be inflated by choosing weak baseline prompts or subjects the model has unusually thin pretraining coverage of." -> "Improvement rates can be inflated by selecting weak baseline prompts or subjects with limited pretraining coverage." | "Unusually thin" is vague; "limited" is more precise.

[§4.2.1] "The guard is reporting the no-context baseline mean alongside the improvement rate; our C5 = 1.52 mean on the low-baseline slice makes the baseline difficulty explicit." -> "Reporting the no-context baseline mean alongside the improvement rate mitigates this: our C5 = 1.52 makes baseline difficulty explicit." | "Guard" is colloquial; "mitigates" is more formal.

[§4.2.1] "**Scale-free illusion of portability.**" -> "Scale-insensitivity in cross-study comparison." | "Illusion of portability" is marketing language; use technical descriptor.

[§4.2.1] "The metric is only comparable across studies when the reporting triplet is disclosed and the baseline is defined identically." -> "Cross-study comparison requires identical baseline definitions and full reporting of the triplet." | "Only comparable when" is weak; state the requirement directly.

[§4.2.1 closing] "The same win-rate framing is referenced in §1.2 (as a secondary outcome alongside the mean-score gradient) and in §4.1 (alongside the 55.0% anchor-crossing rate, which is the same unit at a stricter threshold: "does the response move to a different rubric category?" rather than "does the response improve at all?")." -> "Win-rate framing is used in §1.2 (secondary outcome) and §4.1 (55.0% anchor-crossing rate, a stricter threshold: category shift vs. any improvement)." | Overly parenthetical; break into clearer structure.

[§4.2 example: Hamerton] "Hamerton has the smallest source corpus in the study (25,231 words, compression ratio ~5×). The specification alone (~7K tokens) scores 2.63, exceeding the full raw corpus at 2.27." -> "Hamerton has the smallest source corpus (25,231 words, ~5× compression). The specification alone (~7K tokens) scores 2.63, compared to 2.27 for raw corpus." | "Exceeding" is marketing language; use neutral comparative.

[§4.2 example: Hamerton] "This is the case where structured context substantially outperforms raw text, and where the spec and corpus are clearly complementary rather than overlapping." -> "Here, structured context outperforms raw text, and spec and corpus signals are complementary rather than redundant." | "Substantially outperforms" is vague-strength descriptor; "clearly complementary" is marketing emphasis.

[§4.2 example: Hamerton] "The pattern is interpretable: when the source corpus is short enough to be sparse on its own, structured extraction adds organizational value beyond mere content." -> "When the source corpus is sparse, structured extraction provides organizational value beyond content alone." | "Interpretable...adds...beyond mere" is marketing framing.

[§4.2 example: Hamerton] "Hamerton is the boundary condition for the compression claim, not the proof of it." -> "Hamerton represents a boundary condition, not a general proof." | "The compression claim" presells; state neutrally.

[§4.2 example: Ebers] "Ebers has a larger source corpus (96,174 words) and the study's lowest baseline (1.02)." -> "Ebers has a larger source corpus (96,174 words) and the lowest baseline in the study (1.02)." | Minor: "the study's lowest" is possessive marketing framing.

[§4.2 example: Ebers] "Ebers is where the cost of compression is most visible." -> "Ebers shows the largest compression cost." | "Where...is most visible" is colloquial; use direct statement.

[§4.2 example: Ebers] "The honest reading is not "compression fails"; it is "compression captures the bulk of the signal but not all of it, and on some subjects the residual matters more than on others."" -> "Compression captures most signal but not all; on some subjects, the residual difference is larger." | "Honest reading" is marketing framing (appeals to trust); "captures the bulk" is vague.

[§4.2 example: Ebers] "The trade-off is still favorable: the spec delivers +0.52 points of lift at roughly 6% of the corpus's token cost; the corpus delivers +1.16 points at 18× the context." -> "The specification achieves +0.52 points at 6% of corpus token cost; the corpus achieves +1.16 points at 18× context." | "Trade-off is still favorable" is marketing conclusion; present data neutrally.

[§4.2 example: Ebers] "Per 1,000 tokens of context served, the spec is substantially more efficient." -> "Per 1,000 tokens, the specification achieves higher efficiency (0.074 points/1K tokens vs. 0.003 points/1K tokens for corpus)." | "Substantially more efficient" is vague-strength descriptor; quantify.

[§4.2 deployment] "Why this matters for deployment." -> "Operational implications." | "Why this matters for" is marketing framing.

[§4.2 deployment] "At any scale where a per-user full autobiography cannot be served into context on every query (which is to say, at any real-world scale beyond a toy demo), the compression result is what makes personalization operationally tractable." -> "At scales where per-user full autobiographies cannot be served on every query, compression is necessary for operational feasibility." | "What makes...tractable" is marketing framing; "toy demo" is dismissive colloquialism.

[§4.2 deployment] "The specification's 7K-token footprint is within normal per-request context budgets. A 100,000-to-400,000-word corpus is not." -> "The specification (7K tokens) fits within typical per-request context budgets; full corpora (100K–400K words) do not." | Repetitive short sentences feel like pitch deck; combine.

[§4.2 deployment] "The specification achieves most of the predictive benefit at a tractable cost; the corpus achieves marginally more at a cost that rules out deployment." -> "The specification achieves most predictive benefit at tractable cost; the corpus achieves marginal additional benefit at prohibitive cost." | "Rules out deployment" is marketing conclusion; state as constraint.

---

## Dense Passages

[§4.2.1 intro] "A per-question win rate against a no-context baseline makes behavioral prediction directly comparable across future studies in a way that mean scores do not." -> Break into: "A per-question win rate against a no-context baseline enables comparison across studies. Mean scores require matched rubrics and judges; this metric does not."

[§4.2.1 limitations intro] "The panel-reviewed limitations worth flagging explicitly for any future use:" -> "Known limitations for future adoption:" (also removes marketing register)

[§4.2 deployment] "At any scale where a per-user full autobiography cannot be served into context on every query (which is to say, at any real-world scale beyond a toy demo), the compression result is what makes personalization operationally tractable." -> Break into: "Full autobiographies cannot be served on every query at production scale. Compression is necessary for operational feasibility."

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.2 Compression intro & hypothesis | 3 | "Context works" opener, "captures...lift," "edge is real" are marketing register. Hypothesis statement is clean. |
| §4.2 Compression findings (3 paragraphs) | 2 | Heavy marketing: "captures the large majority," "steep initial slope," "packaged into," "what matters." Vague-strength descriptors throughout. |
| §4.2 Table & aggregate results | 4 | Table is clean. "What the aggregate numbers say" heading is colloquial but findings are stated neutrally. |
| §4.2.1 Win-rate metric intro | 2 | "Cleaner unit," "structurally parallel," "help and harm," "important row," "substantive" all marketing register. |
| §4.2.1 Reporting triplet & low-baseline table | 3 | Metric explanation is mostly neutral; "7 out of every 10" is colloquial; "clears a 70% win rate" is marketing language. |
| §4.2.1 Head-to-head comparison | 2 | "Wins...non-trivial third...fraction of the cost," "wins outright...package" are competitive/marketing framing. |
| §4.2.1 Positioning & proposal | 2 | "Positioning as," "candidate secondary reporting axis," "never replacing it" are pitch-deck language. |
| §4.2.1 Failure modes | 2 | "Guard," "known trap," "catastrophic harm," "gaming," "illusion of portability" are colloquial/marketing. "Tiny-gain inflation" is informal. |
| §4.2 Hamerton example | 2 | "Exceeding," "substantially outperforms," "clearly complementary," "interpretable," "adds organizational value" are marketing register. |
| §4.2 Ebers example | 2 | "Honest reading," "captures the bulk," "trade-off is still favorable" are marketing framing. "Substantially more efficient" is vague. |
| §4.2 Deployment section | 2 | "Why this matters," "what makes...tractable," "toy demo," "rules out deployment" are marketing language. |

---

## Summary

**Overall register cleanliness: 2.3/5** — This section reads as a funding deck or product brief, not academic prose. The author uses competitive framing ("wins," "outperforms"), vague-strength descriptors ("substantial," "meaningful," "significant"), colloquial openers ("Context works," "Why this matters"), and marketing verbs ("captures," "delivers," "achieves") throughout. The core findings are sound, but the prose needs systematic de-marketing: replace "wins" with "outperforms," remove "substantially/clearly/remarkably," replace "what matters" with specific outcomes, and avoid preselling ("this is important because..."). The examples section and deployment section are particularly heavy on marketing register and would benefit from neutral, data-driven restatement.

---

## Chunk: §4.3 Mechanism

# Editorial Review: §4.3 Mechanism

## Marketing Register Flags

[§4.3 opening] "The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt." -> "Whether the benefit derives from specification content rather than from structured format alone" | Oversold framing ("the benefit comes from") presents conclusion as foregone; academic prose states the question being tested.

[§4.3 table reading] "matched content lifts prediction" -> "matched content improves prediction" | "lifts" is marketing-register verb; "improves" is neutral.

[§4.3 table reading] "partial lift; dominated by floor effects on low-baseline subjects" -> "partial improvement; constrained by floor effects on low-baseline subjects" | "lift" and "dominated by" are marketing verbs.

[§4.3 table reading] "adversarial mismatch degrades prediction below the no-context baseline" -> "adversarial mismatch reduces prediction below the no-context baseline" | "degrades" is slightly loaded; "reduces" is more neutral.

[§4.3 mechanism intro] "Three distinct mechanisms produce the correct-specification lift across the study data." -> "Three distinct mechanisms account for the correct-specification effect across the study data." | "produce...lift" is marketing phrasing; "account for...effect" is academic.

[§4.3 mechanism 1] "the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame" -> "the specification provides content (temporal markers, cultural domain, documented life events) sufficient to resolve the identity and establish the reasoning frame" | "anchor" as verb is borderline marketing; "establish" is plainer.

[§4.3 mechanism 2] "the specification overrides the generic with the subject-specific" -> "the specification replaces the generic prediction with the subject-specific one" | "overrides" is slightly loaded; "replaces" is more neutral.

[§4.3 mechanism 3] "the specification provides interpretive scaffolding to generalize from established character patterns to the novel situation" -> "the specification enables generalization from established character patterns to the novel situation" | "scaffolding" is jargon-inflated; "enables" is plainer.

[§4.3 spec-activation] "shows the content-activation gap" -> "quantifies the difference in content engagement" | "gap" is vague; "difference in content engagement" is more precise.

[§4.3 spec-activation] "The baseline reading is that models recognize when the specification fits the question and engage with it; they recognize when it doesn't fit and disengage or improvise." -> "Models appear to recognize when the specification matches the question and draw on it; they recognize when it does not match and either decline to use it or proceed without it." | "baseline reading," "engage," "disengage," and "improvise" are soft/marketing language; more direct phrasing is clearer.

[§4.3 response-level] "the response distribution is bimodal" -> "responses fall into distinct categories" | "bimodal" is correct but "distribution is bimodal" is slightly inflated for what is a simple categorization.

[§4.3 response-level] "explicitly flagged the content mismatch" -> "explicitly identified the content mismatch" | "flagged" is informal/marketing; "identified" is more academic.

[§4.3 response-level] "attempted to apply the mismatched content and produced a low-quality prediction" -> "attempted to apply the mismatched content, resulting in lower-quality predictions" | "produced a low-quality prediction" is slightly vague; "resulting in lower-quality predictions" is more direct.

[§4.3 response-level] "The signal that carries the detection is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model knows about the named subject, not surface name cues." -> "The model detects mismatch through interpretive content (temporal markers, cultural domain, documented life events) that is inconsistent with what it knows about the named subject, rather than through surface name cues." | Nominalization "signal that carries the detection" is inflated; active voice is clearer.

[§4.3 hedging evidence] "Under both classifier rules, spec-containing conditions eliminate baseline hedging: narrow-rule 28.8% → 1.4% → 0.0%, broader-rule 41.2% → 7.9% → 0.4%. Order-of-magnitude drops." -> "Under both classifier rules, spec-containing conditions reduce baseline hedging substantially: narrow-rule 28.8% → 1.4% → 0.0%, broader-rule 41.2% → 7.9% → 0.4%." | "eliminate" and "order-of-magnitude drops" are marketing-strength language; "reduce substantially" is more measured.

[§4.3 hedging evidence] "If mere structured context were producing the effect, wrong-spec should also eliminate hedging at a similar rate." -> "If structured context alone were producing the effect, wrong-spec conditions should also reduce hedging at a similar rate." | "mere" is editorializing; "alone" is more neutral. "eliminate" -> "reduce" for consistency.

[§4.3 hedging evidence] "The hedging-reduction is spec-content-specific, not structure-specific." -> "Hedging reduction correlates with specification content, not with structure alone." | "is...specific" is slightly marketing-framed; "correlates with" is more cautious and academic.

[§4.3 Example A reading] "The model detected the mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It named the served anchors correctly, reasoned from Equiano's framework, and declined to produce a prediction about Ebers." -> "The model identified a mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It cited the served anchors, reasoned from Equiano's framework, and declined to produce a prediction about Ebers." | "detected" and "named...correctly" are slightly marketing-toned; "identified" and "cited" are more neutral.

[§4.3 Example A reading] "The identity-disambiguation mechanism that enabled the correct spec's lift in §4.1 Example A did not fire because the spec content is not about Ebers." -> "The identity-disambiguation mechanism that produced the correct spec's effect in §4.1 Example A did not activate because the spec content is not about Ebers." | "enabled...lift" and "fire" are marketing/informal; "produced...effect" and "activate" are more academic.

[§4.3 Example B reading] "The two specs are genuinely different frameworks." -> "The two specifications represent genuinely different frameworks." | "are" is slightly informal; "represent" is more academic.

[§4.3 Example B reading] "Direct anchor-to-anchor comparison across the two specs finds zero substantive mirroring." -> "Direct anchor-to-anchor comparison across the two specifications reveals no substantive overlap." | "finds zero" is informal; "reveals no" is more academic. "mirroring" is jargon; "overlap" is plainer.

[§4.3 Example B reading] "the two frameworks converge by different logics" -> "the two frameworks reach the same conclusion through different reasoning" | "converge by different logics" is jargon-inflated.

[§4.3 Example B reading] "Different moral architectures, same overt behavior." -> "Different moral frameworks produce the same overt behavior." | "architectures" is jargon; "frameworks" is already established. Fragment is too informal.

[§4.3 Example B reading] "Why the correct spec still outperformed, 4.80 vs. 4.60." -> "Why the correct specification scored higher: 4.80 vs. 4.60." | "outperformed" is marketing verb; "scored higher" is neutral.

[§4.3 Example B reading] "Both conditions predicted the right surface action." -> "Both conditions produced predictions of the correct surface action." | "predicted the right" is slightly informal; "produced predictions of the correct" is more academic.

[§4.3 Example B reading] "The 0.20-point gap is judge preference for rationale specificity that matches the ground-truth passage's tone." -> "The 0.20-point difference reflects judge preference for rationales that match the ground-truth passage's tone." | "gap" is vague; "difference" is clearer. "is judge preference" is awkward; "reflects judge preference" is more direct.

[§4.3 Example B reading] "Judges reward tonally-aligned rationale." -> "Judges favor rationales that align with the passage's tone." | "reward" is marketing verb; "favor" is more neutral.

[§4.3 Example B reading] "The convergence is real but costs precision." -> "The convergence is genuine but reduces precision." | "costs" is informal; "reduces" is more academic.

[§4.3 Example B reading] "When the fixed derangement (v1) happens to pair subjects whose behavioral patterns converge on the same surface prediction for a given question, wrong-spec lift is real on that question, not an artifact." -> "When the fixed derangement (v1) pairs subjects whose behavioral patterns produce the same surface prediction for a given question, the wrong-spec effect on that question is genuine, not an artifact." | "happens to pair" is informal. "lift is real...not an artifact" is marketing-register phrasing; "effect is genuine, not an artifact" is more academic.

[§4.3 Example B reading] "Over 507 responses, mismatch-loss dominates on the adversarial v1 pairing (aggregate Δ −0.25) and roughly balances on the random v2 pairing (aggregate Δ +0.22)." -> "Across 507 responses, mismatch effects predominate on the adversarial v1 pairing (aggregate Δ −0.25) and roughly balance on the random v2 pairing (aggregate Δ +0.22)." | "dominates" is marketing verb; "predominate" is more neutral. "Over" should be "Across" for clarity.

[§4.3 Example B reading] "Example B is one of the roughly 5-10% of questions where content coincidence produces correct-surface, wrong-logic predictions." -> "Example B represents one of roughly 5-10% of questions where content coincidence produces correct surface predictions based on incorrect reasoning." | "produces correct-surface, wrong-logic" is jargon-inflated; "produces correct surface predictions based on incorrect reasoning" is clearer.

[§4.3 Example C reading] "The model detected the mismatch between the named target in the question (Mary Seacole, a 19th-century Jamaican Creole nurse) and the anonymized content of the served specification (16th-century Spanish conquest anchors)." -> "The model identified a mismatch between the named target in the question (Mary Seacole, a 19th-century Jamaican Creole nurse) and the anonymized content of the served specification (16th-century Spanish conquest anchors)." | "detected" is slightly marketing-toned; "identified" is more neutral.

[§4.3 Example C reading] "The interpretive-inference mechanism that produced §4.1 Example C's correct-spec 5.00 score does not fire: without Seacole's actual character pattern in context, the model would not generalize from an unrelated conquistador's framework to her delirious-patient scenario." -> "The interpretive-inference mechanism that produced §4.1 Example C's correct-spec score of 5.00 does not activate: without Seacole's actual character pattern in context, the model cannot generalize from an unrelated conquistador's framework to her delirious-patient scenario." | "fire" is informal; "activate" is more academic. "would not" is weaker than "cannot."

[§4.3 summary table] "Explicit mismatch flag; declined prediction" -> "Explicit mismatch identification; prediction declined" | "flag" is informal; "identification" is more academic.

[§4.3 summary table] "Coincidental content overlap; wrong-spec prediction matches" -> "Coincidental content overlap; wrong-spec prediction aligns with correct prediction" | "matches" is informal; "aligns with" is more academic.

[§4.3 summary table] "Explicit mismatch flag; declined prediction" -> "Explicit mismatch identification; prediction declined" | (repeated from earlier)

[§4.3 summary paragraph] "Two of three examples show large drops (−2.00 to −3.60 points) when the content does not fit." -> "Two of three examples show substantial reductions (−2.00 to −3.60 points) when the content does not fit." | "large drops" is vague marketing language; "substantial reductions" is more precise.

[§4.3 summary paragraph] "That asymmetry, clean mismatches versus coincidental overlaps, is exactly what the aggregate Δ numbers reflect:" -> "This asymmetry—between clear mismatches and coincidental overlaps—accounts for the aggregate Δ values:" | "clean mismatches" is informal. "is exactly what...reflect" is slightly marketing-framed; "accounts for" is more academic.

[§4.3 summary paragraph] "the adversarial-pairing v1 aggregates to −0.25 because most questions are mismatch cases, and the random-pairing v2 aggregates to +0.22 because random pairings more often hit content-proximity combinations like Example B." -> "the adversarial-pairing v1 aggregates to −0.25 because most questions involve mismatches, and the random-pairing v2 aggregates to +0.22 because random pairings more often produce content-proximity combinations like Example B." | "are mismatch cases" is slightly informal. "hit" is informal; "produce" is more academic.

---

## Dense Passages

[§4.3 mechanism 1] "When the baseline model cannot determine which person is being asked about, the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame." -> Break into: "When the baseline model cannot determine which person is being asked about, the specification provides sufficient content to resolve the identity. This content includes temporal markers, cultural domain, and documented life events, which anchor the reasoning frame."

[§4.3 mechanism 2] "When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification overrides the generic with the subject-specific." -> Break into: "When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification replaces this generic prediction with a subject-specific one."

[§4.3 spec-activation] "On correct-spec conditions, **78.6%** of responses explicitly cite at least one spec tag (anchor ID, axiom reference, predictive-template label). On wrong-spec conditions, only **50.0%** do. The 28.6-point gap is a lower bound on the content effect: models may draw on spec content without literally quoting tag IDs, so the true divergence is wider." -> Break into: "On correct-spec conditions, 78.6% of responses explicitly cite at least one spec tag (anchor ID, axiom reference, or predictive-template label). On wrong-spec conditions, only 50.0% do so. The 28.6-point difference is a lower bound on the content effect. Models may draw on spec content without explicitly quoting tag IDs, so the true difference is likely larger."

[§4.3 response-level] "The detection asymmetry in this experiment: battery questions name the target subject (e.g., "How would Ebers characterize...") but specifications are anonymized (§3.3), so "detecting the mismatch" means the model is comparing the named target in the question to the interpretive content of the anonymized specification, and concluding the specification does not describe the named target." -> Break into: "The detection asymmetry in this experiment arises from the design: battery questions name the target subject (e.g., "How would Ebers characterize..."), but specifications are anonymized (§3.3). Detecting the mismatch requires the model to compare the named target in the question against the interpretive content of the anonymized specification and conclude that the specification does not describe the named target."

[§4.3 response-level] "The signal that carries the detection is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model knows about the named subject, not surface name cues." -> Break into: "The model detects mismatch through interpretive content—temporal markers, cultural domain, and documented life events—that is inconsistent with what it knows about the named subject. Surface name cues are not the signal."

[§4.3 Example B reading] "the two frameworks converge by different logics: the correct spec (Bernal Diaz) predicts refusal because accepting help would signal weakness to followers and violate performative self-reliance (A4 + A5 in the conquistador register); the wrong spec (Sunity Devee) predicts refusal because accepting help would compromise physical discipline and violate simplicity-as-virtue (A9 + P5 in the devotional register)." -> Break into: "The two frameworks reach the same conclusion through different reasoning. The correct spec (Bernal Diaz) predicts refusal because accepting help would signal weakness to followers and violate performative self-reliance (A4 + A5 in the conquistador register). The wrong spec (Sunity Devee) predicts refusal because accepting help would compromise physical discipline and violate simplicity-as-virtue (A9 + P5 in the devotional register)."

[§4.3 Example B reading] "Why the correct spec still outperformed, 4.80 vs. 4.60. Both conditions predicted the right surface action. The 0.20-point gap is judge preference for rationale specificity that matches the ground-truth passage's tone. The correct spec's "symbolic or morale-signaling purpose" rationale maps onto a battlefield memoir's register; the wrong spec's "spiritual seriousness, devotional simplicity" rationale predicts the same action but in a register alien to Cortes on the steps of the Templo Mayor." -> Break into: "The correct specification scored 4.80 versus 4.60 for the wrong specification. Both conditions predicted the correct surface action. The 0.20-point difference reflects judge preference for rationales that match the ground-truth passage's tone. The correct spec's "symbolic or morale-signaling purpose" rationale aligns with a battlefield memoir's register. The wrong spec's "spiritual seriousness, devotional simplicity" rationale predicts the same action but in a register alien to Cortes on the steps of the Templo Mayor."

[§4.3 summary paragraph] "That asymmetry, clean mismatches versus coincidental overlaps, is exactly what the aggregate Δ numbers reflect: the adversarial-pairing v1 aggregates to −0.25 because most questions are mismatch cases, and the random-pairing v2 aggregates to +0.22 because random pairings more often hit content-proximity combinations like Example B." -> Break into: "This asymmetry—between clear mismatches and coincidental overlaps—accounts for the aggregate Δ values. The adversarial-pairing v1 aggregates to −0.25 because most questions involve mismatches. The random-pairing v2 aggregates to +0.22 because random pairings more often produce content-proximity combinations like Example B."

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.3 Opening (Hypothesis) | 4 | Clean framing; one instance of "the benefit comes from" (oversold). Otherwise direct. |
| §4.3 Mechanism Intro & Table | 2 | Multiple marketing verbs ("lifts," "lift," "dominated," "degrades"). Table readings are particularly weak. |
| §4.3 Three Mechanism Types | 3 | Definitions are mostly clear but use jargon ("scaffolding," "anchor," "override"). Mechanism descriptions are sound but slightly inflated. |
| §4.3 Spec-Activation Evidence | 3 | "gap," "engage/disengage," "baseline reading" are soft. Core findings are solid but framing is marketing-adjacent. |
| §4.3 Response-Level Evidence | 2 | "flagged," "produced a low-quality prediction," nominalization of "signal that carries the detection." Dense and jargon-heavy. |
| §4.3 Hedging Evidence | 2 | "eliminate," "order-of-magnitude drops," "spec-content-specific" are marketing-register. Phrasing is inflated for what is a straightforward comparison. |
| §4.3 Example A (Wrong-Spec) | 3 | "detected," "named...correctly," "fire," "enabled...lift" are slightly marketing-toned. Reading is otherwise clear. |
| §4.3 Example B (Wrong-Spec) | 2 | "outperformed," "reward," "costs precision," "happens to pair," "lift is real," "converge by different logics," "hit content-proximity combinations" are all marketing or jargon-inflated. |
| §4.3 Example C (Wrong-Spec) | 3 | "detected," "fire" are informal. Otherwise the reading is clear and direct. |
| §4.3 Summary Table & Paragraph | 2 | "large drops," "clean mismatches," "is exactly what...reflect," "hit," "flag" are all marketing or informal register. |

---

## Overall Assessment

**Register-Cleanliness Score for §4.3: 2.5 / 5**

This section has **significant marketing register contamination**, concentrated in:
1. **Mechanism descriptions** (jargon: "scaffolding," "anchor," "override")
2. **Evidence sections** (soft language: "gap," "engage," "baseline reading," "eliminate," "order-of-magnitude")
3. **Example B reading** (marketing verbs: "outperformed," "reward," "hit," "converge by different logics")
4. **Summary framing** ("clean mismatches," "is exactly what...reflect," "large drops")

The **core findings are sound and well-supported**, but the prose wrapping them uses too much marketing vocabulary and jargon. The author should:
- Replace all marketing verbs with neutral alternatives (lift→effect, fire→activate, flag→identify, etc.)
- Break up dense passages into shorter sentences
- Replace jargon ("scaffolding," "architectures," "converge by different logics") with plain language
- Soften superlatives and vague-strength descriptors ("large," "clean," "eliminate," "order-of-magnitude")
- Use active voice and direct phrasing instead of nominalizations

With these edits, this section could reach 4.5–5.0.

---

## Chunk: §4.4 Memory-System Composition + 4.4.1

# Register Review: §4.4 Memory-System Composition + §4.4.1

---

## Marketing Register Flags

[§4.4 intro] "The specification is composable with existing memory-system retrieval pipelines, not a replacement for them." -> "The specification can be added to existing memory-system retrieval pipelines rather than replacing them." | "composable" is technical jargon; plain phrasing is clearer.

[§4.4 intro] "improves their behavioral prediction additively" -> "improves their behavioral prediction when combined with retrieval" | "additively" is vague; specify the relationship plainly.

[§4.4 setup] "The specification is additive to retrieval, not a replacement for it, and it composes with diverse retrieval architectures" -> "The specification can be combined with retrieval rather than replacing it, and works across different retrieval architectures" | "additive" and "composes" are technical abstractions; use concrete language.

[§4.4 results summary] "**The flagship composition result.**" -> "**Main composition result.**" or "**Composition results.**" | "flagship" is marketing language for "primary" or "main."

[§4.4 Supermemory intro] "produces substantial effects in both directions" -> "produces effects in both directions" | "substantial" is a vague-strength descriptor; the magnitudes are shown in the table.

[§4.4 Supermemory intro] "noticeably more accurate" and "noticeably less accurate" -> "more accurate" and "less accurate" | "noticeably" is a vague intensifier; let the numbers speak.

[§4.4 Supermemory quantified] "**count-asymmetric, magnitude-symmetric mixture**" -> "a mixture with unequal counts but similar magnitudes" | This compound noun feels invented and obscures the simple observation.

[§4.4 Example 1 heading] "spec helps by filling an interpretive gap" -> "specification provides interpretive structure when retrieval is insufficient" | "helps" is marketing language; describe the mechanism.

[§4.4 Example 1 reading] "The specification provided the interpretive bridge" -> "The specification supplied the interpretive structure" | "bridge" is a metaphor; use neutral language.

[§4.4 Example 2 heading] "spec hurts by over-theorizing a plain question" -> "specification introduces unnecessary interpretation on a literal question" | "hurts" is marketing language; "over-theorizing" is vague.

[§4.4 Example 2 reading] "The specification pulled the answer toward interpretive depth on a question where shallow was correct." -> "The specification shifted the answer toward interpretation on a question where literal content was correct." | "pulled" and "shallow" are informal; "literal" is more precise than "shallow."

[§4.4 Example 3 heading] "judging-issue: spec-induced meta-refusal" -> "rubric limitation: specification triggers refusal that the rubric cannot distinguish from error" | "spec-induced" is jargon; "meta-refusal" is vague.

[§4.4 Example 4 heading] "subtle reframe that scores well but unevenly" -> "specification reframes the question; judges disagree on whether to reward the reframe" | "subtle" is vague; describe what happens.

[§4.4 Supermemory aggregate] "The near-zero aggregate is the sum of three distinguishable patterns, each a real mechanism" -> "The near-zero aggregate results from three distinguishable patterns" | "real mechanism" is redundant; if it's distinguishable, it's real.

[§4.4 Supermemory aggregate] "Pattern 1 and Pattern 4 (Example 4's reframe) drive the 37 spec-helps questions" -> "Patterns 1 and 4 account for the 37 questions where the specification improved prediction" | "drive" is marketing language; "spec-helps" is informal.

[§4.4 Supermemory aggregate] "Patterns 2 and 3 drive the 52 spec-hurts questions" -> "Patterns 2 and 3 account for the 52 questions where the specification worsened prediction" | Same as above.

[§4.4 Supermemory aggregate] "The aggregate is modestly hurts-heavy because Supermemory's retrieval is strong enough for Patterns 2 and 3 to fire more often" -> "The aggregate is modestly negative because Supermemory's retrieval is strong enough that Patterns 2 and 3 occur more frequently" | "hurts-heavy" is informal; "fire" is jargon.

[§4.4 follow-up] "One candidate factor is the battery itself" -> "One possible factor is the question battery itself" | "candidate" is vague; "possible" is clearer.

[§4.4 follow-up] "the balance of interpretation-heavy versus literal-recall questions was not controlled by construction" -> "the proportion of interpretation-heavy versus literal-recall questions was not controlled during design" | "controlled by construction" is awkward; "controlled during design" is clearer.

[§4.4 follow-up] "A differentiated battery that explicitly separates these question types, and that scores epistemic honesty as its own dimension (separating Pattern 3 from genuine wrong predictions), would let each pattern's contribution be measured directly rather than inferred from post-hoc classification" -> "A battery that explicitly separates interpretation-heavy from literal-recall questions, and that scores refusal separately from incorrect prediction, would allow direct measurement of each pattern's contribution rather than post-hoc inference." | "differentiated," "epistemic honesty," and "measured directly rather than inferred" are wordy; simplify.

[§4.4 hedging hypothesis] "A prior version of this analysis proposed that the specification's effect on memory systems was mediated primarily by a prompt-template-induced hedging reduction." -> "An earlier version proposed that the specification's effect was primarily due to reduced hedging in the prompt template." | "mediated by" and "prompt-template-induced" are inflated; simplify.

[§4.4 hedging hypothesis] "Paired response-level analysis across all five systems (recorded as m19 in KEY_FINDINGS) partially contradicted that proposal" -> "Response-level analysis across all five systems partially contradicted this proposal" | "recorded as m19" is a citation detail; move to footnote or remove. "partially contradicted" is fine.

[§4.4 hedging hypothesis] "the specification reduces hedging on the Base Layer retrieval substrate and on some commercial systems, but not uniformly, and the hedging pattern does not track the spec-effect magnitude cleanly across systems" -> "the specification reduces hedging on some systems but not others, and the hedging reduction does not correlate cleanly with the specification's effect size across systems" | "track cleanly" is informal; "correlate" is more precise.

[§4.4 hedging hypothesis] "The updated mechanistic reading is the one from §4.3: the specification's effect is content-specific, not structure-specific." -> "The revised explanation is in §4.3: the specification's effect depends on content, not on prompt structure." | "mechanistic reading" and "content-specific, not structure-specific" are jargon; use plain language.

[§4.4.1 intro] "Letta's architecture is distinct from the other three commercial systems in one important way." -> "Letta's architecture differs from the other three commercial systems in one key respect." | "distinct" and "important way" are vague; "differs" and "key respect" are clearer.

[§4.4.1 intro] "Letta maintains a persistent memory block that the agent self-edits during multi-turn conversation." -> "Letta maintains a persistent memory block that the agent updates during multi-turn conversation." | "self-edits" is informal; "updates" is standard.

[§4.4.1 intro] "This is the stateful-agent path from the original MemGPT design." -> "This is the stateful-agent architecture from the original MemGPT design." | "path" is vague; "architecture" is more precise.

[§4.4.1 intro] "§4.7 develops this as architectural convergence on a shared interpretive-representation target, and documents the scaling ceiling we observed at the largest corpus tested." -> "§4.7 discusses how this architecture converges on the same interpretive representation as the Behavioral Specification, and documents the performance plateau observed at the largest corpus." | "architectural convergence on a shared interpretive-representation target" is inflated jargon; "scaling ceiling" is marketing language for "plateau."

---

## Dense Passages

[§4.4 setup, controlled configuration] "Each system is given an identical pre-extracted fact pool drawn from the training half of each subject's corpus. The input is held constant across all four commercial systems and the Base Layer substrate, so any difference in the downstream prediction score is attributable to the system's retrieval and presentation policy alone, not to what it was able to ingest." -> Break into two sentences: "Each system receives an identical pre-extracted fact pool from the training half of each subject's corpus. Because the input is held constant across all systems, any difference in prediction score reflects the system's retrieval and presentation policy, not differences in ingestion." | The original sentence is 60+ words with nested clauses.

[§4.4 Supermemory Example 2 reading] "The ground truth is literal: 'in plain words' + a concrete machine-shop list. C1 matched the plainness. The specification pulled the answer toward interpretive depth on a question where shallow was correct. This is not refusal or epistemic caution; the specification simply had the wrong altitude for the question." -> Break into shorter units: "The ground truth is literal: 'in plain words' plus a concrete list. C1 matched this plainness. The specification shifted the answer toward interpretation on a question where literal content was correct. This is not refusal; the specification simply applied the wrong level of interpretation." | The original passage mixes metaphor ("altitude") with technical language and is hard to parse.

[§4.4 Supermemory aggregate] "The near-zero aggregate is the sum of three distinguishable patterns, each a real mechanism: (1) Spec fills an interpretive gap when retrieval is insufficient (Example 1): +1.5 to +2.2 per-question swings. This is the same mechanism documented in §1.3 and §4.3. (2) Spec over-theorizes when retrieval already has the plain answer (Example 2): −1.5 to −2.4 per-question swings. Supermemory's strong retrieval makes this the most common hurt pattern. (3) Spec induces meta-refusal that the rubric cannot distinguish from wrong prediction (Example 3): clean −2.0 swings to the rubric floor." -> This is a dense list. Consider a table or bullet format instead of prose, or break into separate paragraphs with clearer topic sentences. | The current format buries the three mechanisms in a long paragraph.

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.4 intro (hypothesis) | 3 | "Composable," "additively," and "improves" are acceptable but could be plainer. |
| §4.4 setup | 4 | Clear and methodical; "controlled" and "native" are standard terms. |
| §4.4 aggregate results (tables + prose) | 4 | Tables are clean. Prose is mostly neutral; "three of four commercial memory systems benefit" is slightly marketing-toned. |
| §4.4 results summary (Zep, Mem0, Letta, Base Layer) | 3 | "Cleanest positive case," "largest single-system spec-effect," "flagship composition result" are marketing language. |
| §4.4 Supermemory intro | 2 | "Substantial effects," "noticeably," "count-asymmetric magnitude-symmetric mixture" are marketing/jargon-heavy. |
| §4.4 Supermemory examples (1–4) | 3 | Examples are detailed and mostly neutral, but headings use marketing verbs ("helps," "hurts," "spec-induced"). |
| §4.4 Supermemory aggregate (three patterns) | 2 | "Drive," "fire," "hurts-heavy," "real mechanism" are marketing/jargon. Dense list format. |
| §4.4 follow-up research | 3 | "Candidate factor," "controlled by construction," "differentiated battery" are slightly inflated. |
| §4.4 hedging hypothesis | 2 | "Mediated by," "prompt-template-induced," "mechanistic reading," "track cleanly" are jargon-heavy. |
| §4.4.1 Letta pointer | 2 | "Distinct," "self-edits," "architectural convergence on a shared interpretive-representation target," "scaling ceiling" are marketing/jargon. |

---

## Summary

**Overall register cleanliness: 2.8 / 5**

The paper has strong empirical sections (tables, setup, examples) but is undermined by:
1. **Marketing verbs** in result summaries: "helps," "hurts," "drives," "fires," "flagship"
2. **Vague intensifiers**: "substantial," "noticeably," "remarkable," "real mechanism"
3. **Invented compound nouns**: "count-asymmetric magnitude-symmetric mixture," "architectural convergence on a shared interpretive-representation target"
4. **Jargon inflation**: "mediated by," "mechanistic reading," "scaling ceiling," "epistemic honesty"
5. **Dense passages** that bury findings in long sentences

**Recommendation**: Systematically replace marketing verbs with neutral descriptors ("improves" → "increases," "helps" → "improves," "drives" → "accounts for"). Remove vague intensifiers and let numbers speak. Break dense passages into shorter sentences. Replace invented compounds with plain language. The empirical work is solid; the prose just needs to get out of the way.

---

## Chunk: §4.5 Robustness (4.5.1 / 4.5.2 / 4.5.3)

# Editorial Review: §4.5 Robustness and Sensitivity

---

## Marketing Register Flags

[§4.5 intro] "could in principle reflect artifacts" -> "may reflect artifacts" | weakening hedge typical of pitch-deck risk-mitigation language; plain academic prose states possibility directly

[§4.5.1 Concern] "If the specification's effect depends on response-model and question-generator co-tuning within the Anthropic family, the observed effect could be an artifact of within-family alignment rather than a real property of the specification." -> "If the effect depends on co-tuning within the Anthropic family, it may reflect within-family alignment rather than a property of the specification itself." | "real property" is a vague-strength descriptor; "within-family alignment" is unnecessarily abstract

[§4.5.1 Result] "5 of 6 cells reproduce the specification direction." -> "5 of 6 cells show the specification effect in the same direction as the main study." | "reproduce" is marketing language for replication; use plain term

[§4.5.1 Direction of the finding] "The specification's effect is not a Haiku-specific or Claude-family-specific artifact." -> "The specification effect does not depend on Haiku or the Claude family." | "is not an artifact" is a negation of a vague term; state what it is instead

[§4.5.1 Direction of the finding] "Non-Anthropic response models, reading OpenAI-generated batteries, show the same spec-effect direction on five of the six cells tested." -> "Non-Anthropic response models reading OpenAI-generated batteries show the same direction on five of six cells." | "show the same spec-effect direction" is redundant; "tested" is filler

[§4.5.1 Secondary observation] "This is empirical support for the structural premise in §1.4" -> "This supports the structural premise in §1.4" | "empirical support for" is pitch-deck hedging; direct statement is cleaner

[§4.5.2 Concern] "The judge panel could itself introduce systematic bias in favor of the Behavioral Specification." -> "The judge panel may introduce systematic bias favoring the Behavioral Specification." | "could itself" is hedging filler

[§4.5.2 Concern] "Gemini 2.5 Pro specifically failed verbatim-match calibration (§3.7.2: scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply." -> "Gemini 2.5 Pro scored 4.15 on verbatim-match calibration while all other judges scored 5.00 (§3.7.2), and penalized length-padded responses more severely." | "failed" and "sharply" are vague-strength descriptors; use measured language

[§4.5.2 Test] "If Gemini inflation or another panel-level bias happened to favor spec-containing conditions disproportionately, the 5-judge and 7-judge aggregates would diverge." -> "If panel-level bias favored spec-containing conditions, the 5-judge and 7-judge aggregates would diverge." | "Gemini inflation" is jargon; "happened to" is filler; "disproportionately" is vague

[§4.5.2 Result] "The 5-judge primary is the conservative choice for every headline finding." -> "The 5-judge primary yields smaller effect sizes than the 7-judge aggregate for every headline finding." | "conservative choice" is marketing language for "lower bound"; state the actual comparison

[§4.5.2 Result] "Gemini inclusion widens spec-effect magnitudes rather than narrowing them." -> "Adding Gemini judges increases the measured effect size." | "widens" and "spec-effect magnitudes" are inflated phrasing

[§4.5.2 Result table] "Direction of shift when Gemini is added" -> "Change in effect size when Gemini judges are added" | "direction of shift" is vague; be specific about what is changing

[§4.5.2 Result] "The Gemini-inclusion shift in C2a's direction is driven by Gemini's relatively severe scoring of baseline (no-context) responses compared to its scoring of spec-containing responses." -> "Gemini scores baseline responses more severely than spec-containing responses, which widens the measured difference." | "Gemini-inclusion shift in C2a's direction" is noun-stacking jargon

[§4.5.2 Result] "Including Gemini compresses the baseline ceiling more than the spec-condition ceiling, which widens the delta." -> "Adding Gemini judges reduces baseline scores more than spec-condition scores, increasing the measured difference." | "compresses the baseline ceiling," "spec-condition ceiling," and "widens the delta" are inflated phrasing

[§4.5.2 Result] "The direction of the shift is the same across almost every comparison in the paper: 5-judge primary gives the lower-bound effect size, 7-judge gives a larger effect size, and no subject's improvement direction changes between them" -> "Across nearly all comparisons, the 5-judge panel yields smaller effect sizes than the 7-judge panel, and no subject's direction reverses." | "direction of the shift," "lower-bound effect size," and "improvement direction" are redundant or vague

[§4.5.2 Result] "Reporting 5-judge primary means every paper claim is the conservative version." -> "Reporting 5-judge results means all claims use the smaller effect sizes." | "conservative version" is marketing language

[§4.5.2 Result] "**Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`).**" -> "All primary findings were checked against the 7-judge aggregate per the pre-registered analysis plan." | "analysis plan lock" is jargon; "as part of" is filler

[§4.5.2 Result] "None of the paper's claims depend on the panel choice between 5-judge and 7-judge; all directional claims reproduce on either panel." -> "No claim depends on panel choice; all directional findings hold on both panels." | "reproduce" is marketing language; "directional claims" is vague

[§4.5.3] "Neither Tier 2 nor the judge-panel sensitivity escapes the LLM-class concern." -> "Neither Tier 2 nor the judge-panel sensitivity addresses the LLM-class concern." | "escapes" is marketing language (evasion framing)

[§4.5.3] "If LLMs as a class share systematic biases that favor responses quoting behavioral-specification tag IDs (78.6% of correct-spec responses, §4.3), that class-level bias would appear in the measured effect size and neither the cross-provider response test nor the non-Gemini judge panel would fully remove it." -> "If LLMs systematically favor responses quoting specification tag IDs (78.6% of correct-spec responses, §4.3), this bias would affect the measured effect size, and neither the cross-provider test nor the non-Gemini panel would eliminate it." | "as a class," "would fully remove," and "class-level bias" are inflated phrasing

[§4.5.3] "Tier 2 narrows the concern to 'non-Haiku LLMs, reading non-Anthropic batteries, produce the same direction.'" -> "Tier 2 shows that non-Haiku LLMs reading non-Anthropic batteries produce the same direction." | "narrows the concern to" is vague; state what was shown

[§4.5.3] "The judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger." -> "The judge-panel sensitivity shows that removing Gemini judges reduces the measured effect." | "most-inflationary" is jargon; "makes the effect smaller, not larger" is redundant

[§4.5.3] "Together these results rule out several within-family artifact hypotheses but do not replace human validation on the full pipeline." -> "Together these results rule out several within-family artifact hypotheses but do not substitute for human validation." | "on the full pipeline" is jargon

[§4.5.3] "The remaining LLM-as-judge circularity is discussed directly in §6 Limitations." -> "The remaining circularity from using LLMs as judges is discussed in §6 Limitations." | "LLM-as-judge circularity" is jargon; "directly" is filler

---

## Dense Passages

[§4.5.1 Test design] "Three subjects spanning the gradient were selected: Ebers (C5 = 1.02, low baseline), Yung Wing (C5 = 1.88, low baseline), and Zitkala-Sa (C5 = 2.34, mid baseline, main-study spec-null on Δ_C4a)." -> Break into: "Three subjects spanning the gradient were selected. Ebers (C5 = 1.02) and Yung Wing (C5 = 1.88) had low baselines. Zitkala-Sa (C5 = 2.34) had mid baseline and showed no spec effect on Δ_C4a in the main study." | 60+ characters with nested parentheticals; hard to parse

[§4.5.1 Test design] "Their behavioral-prediction batteries were regenerated from scratch by GPT-5.4 (OpenAI) from the same held-out corpus." -> "Their behavioral-prediction batteries were regenerated by GPT-5.4 (OpenAI) using the same held-out corpus." | "from scratch" and "from the same" are redundant; "from scratch" is filler

[§4.5.1 Test design] "The specification was then served to two non-Haiku response models: Claude Sonnet 4.6 (same provider family, different model) and Google Gemini 2.5 Pro (different provider entirely)." -> Break into: "The specification was then served to two non-Haiku response models. Claude Sonnet 4.6 is from the same provider but a different model. Google Gemini 2.5 Pro is from a different provider." | Nested parentheticals; easier to parse as separate sentences

[§4.5.1 Result] "The one non-matching cell (Zitkala-Sa × Gemini 2.5 Pro, Δ −0.55) is consistent with Zitkala-Sa's main-study behavior." -> "The one non-matching cell (Zitkala-Sa × Gemini 2.5 Pro, Δ −0.55) matches Zitkala-Sa's main-study behavior." | "is consistent with" is weaker than needed; use direct language

[§4.5.2 Concern] "Gemini 2.5 Pro specifically failed verbatim-match calibration (§3.7.2: scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply." -> Break into: "Gemini 2.5 Pro scored 4.15 on verbatim-match calibration (§3.7.2), while all other judges scored 5.00. It also penalized length-padded responses more severely." | Two independent clauses with nested parenthetical; easier as two sentences

[§4.5.2 Result] "The Gemini-inclusion shift in C2a's direction is driven by Gemini's relatively severe scoring of baseline (no-context) responses compared to its scoring of spec-containing responses." -> "Gemini scores baseline responses more severely than spec-containing responses, which increases the measured effect in C2a." | Noun-stacking ("Gemini-inclusion shift in C2a's direction") obscures meaning; rewrite with verbs

[§4.5.2 Result] "Including Gemini compresses the baseline ceiling more than the spec-condition ceiling, which widens the delta." -> "Adding Gemini judges reduces baseline scores more than spec-condition scores, increasing the measured difference." | Metaphorical language ("compresses," "ceiling," "widens the delta") is harder to parse than direct comparison

[§4.5.2 Result] "The direction of the shift is the same across almost every comparison in the paper: 5-judge primary gives the lower-bound effect size, 7-judge gives a larger effect size, and no subject's improvement direction changes between them (noted in §1.2 and §3.7.2)." -> Break into: "Across nearly all comparisons, the 5-judge panel yields smaller effect sizes than the 7-judge panel. No subject's direction reverses between panels (noted in §1.2 and §3.7.2)." | Three independent claims in one sentence; easier as two

[§4.5.3] "Neither Tier 2 nor the judge-panel sensitivity escapes the LLM-class concern." -> "Tier 2 and the judge-panel sensitivity do not address the LLM-class concern." | Negative construction with "escapes" is harder to parse than positive statement

[§4.5.3] "If LLMs as a class share systematic biases that favor responses quoting behavioral-specification tag IDs (78.6% of correct-spec responses, §4.3), that class-level bias would appear in the measured effect size and neither the cross-provider response test nor the non-Gemini judge panel would fully remove it." -> Break into: "If LLMs systematically favor responses quoting specification tag IDs (78.6% of correct-spec responses, §4.3), this bias would affect the measured effect size. Neither the cross-provider test nor the non-Gemini panel would eliminate it." | 60+ characters with nested parenthetical and two independent clauses; easier as two sentences

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.5 Intro | 3 | Hedging language ("could in principle") and vague-strength descriptors ("real properties") pull down from 4. Otherwise clear. |
| §4.5.1 Concern | 2 | "co-tuning," "within-family alignment," "real property" are marketing abstractions. Needs concreteness. |
| §4.5.1 Test design | 3 | Dense parentheticals and "from scratch" filler. Structure is sound but prose is cluttered. |
| §4.5.1 Result | 3 | "reproduce" is marketing language; otherwise factual. Table is clean. |
| §4.5.1 Direction of the finding | 2 | "is not an artifact," "show the same spec-effect direction," "empirical support for" are all pitch-deck hedging. Needs direct statements. |
| §4.5.1 Secondary observation | 3 | "empirical support for" is hedging; otherwise clear. |
| §4.5.2 Concern | 2 | "could itself," "sharply," "Gemini inflation," "disproportionately" are vague-strength and jargon. |
| §4.5.2 Test | 3 | "happened to" is filler; otherwise clear. |
| §4.5.2 Result | 2 | "conservative choice," "widens spec-effect magnitudes," "compresses the baseline ceiling," "widens the delta" are all marketing/metaphorical. Heavy jargon. |
| §4.5.2 Result (table) | 4 | Clean. "Direction of shift" is slightly vague but acceptable in table context. |
| §4.5.2 Result (paragraph after table) | 2 | "lower-bound effect size," "improvement direction," "direction of the shift," "conservative version," "analysis plan lock" are all jargon or marketing. |
| §4.5.3 | 2 | "escapes," "as a class," "would fully remove," "most-inflationary," "LLM-as-judge circularity," "on the full pipeline" are jargon and marketing language. Negative constructions obscure meaning. |

---

## Summary

**Overall register cleanliness for §4.5: 2.5 / 5**

This section has **heavy GTM/pitch-deck register**. The core issues:

1. **Vague-strength descriptors** dominate: "real property," "sharply," "disproportionately," "most-inflationary," "empirical support for"
2. **Marketing verbs and hedging**: "reproduce," "escapes," "could itself," "happened to," "is not an artifact"
3. **Jargon and noun-stacking**: "co-tuning," "within-family alignment," "Gemini-inclusion shift in C2a's direction," "LLM-as-judge circularity," "analysis plan lock," "compresses the baseline ceiling"
4. **Metaphorical language masquerading as precision**: "widens the delta," "compresses the ceiling," "lower-bound effect size"
5. **Dense parentheticals** that obscure meaning

**Recommendation**: Rewrite §4.5.2 and §4.5.3 entirely. Replace all hedging with direct statements. Replace jargon with plain terms. Break dense sentences. Use active voice and concrete comparisons instead of metaphor.

---

## Chunk: §4.6 Interpretation vs Recall

# Editorial Review: §4.6 Interpretation vs. Recall

## Marketing Register Flags

[§4.6 opening] "The specification produces large improvements on some questions and large regressions on others" -> "The specification improves some questions and worsens others" | "large" is vague-strength descriptor; the magnitudes are quantified in the table

[§4.6 opening] "roughly the same magnitude on each side" -> "similar magnitude on each side" | "roughly" softens precision unnecessarily in academic prose

[§4.6 opening] "The three mechanisms identified on Supermemory (the specification supplies a pattern retrieval cannot, the specification over-theorizes a question retrieval already answered plainly, the specification induces a refusal the content-match rubric penalizes) reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate." -> Break into separate sentence or use semicolons; this is a dense parenthetical that reads like a pitch summary | oversold framing with "reproduce" (marketing verb suggesting universal applicability)

[§4.6 opening] "The most consistent specification-induced behavior across substrates is a spec-induced refusal" -> "The most consistent behavior across substrates is a specification-induced refusal" | "specification-induced" repeated; "most consistent" is vague-strength descriptor without quantification

[§4.6 table caption] "every row is a mixture of wins and losses" -> "each row contains both improvements and regressions" | "wins and losses" is pitch-deck language; use neutral terms

[§4.6 table caption] "Even Zep's strongest row (Seacole, Δ +0.52)" -> "Even the Zep Seacole row (Δ +0.52)" | "strongest" is superlative marketing language

[§4.6 mechanisms section] "In plainer language:" -> delete | self-aware hedge that signals the prior phrasing was unclear; rewrite the prior phrasing instead

[§4.6 Pattern 1] "specification supplies a pattern retrieval cannot" -> "specification provides a pattern that retrieval does not" | "supplies" is marketing verb; "cannot" is anthropomorphic

[§4.6 Pattern 2] "specification over-theorizes a question retrieval already answered plainly" -> "specification elaborates beyond what the retrieved facts support" | "over-theorizes" is invented compound noun; "plainly" is vague descriptor

[§4.6 Pattern 3] "specification induces a refusal the content-match rubric cannot score as anything but wrong" -> "specification triggers a refusal that the content-match rubric scores as incorrect" | "induces" is marketing verb; "cannot score as anything but" is awkward hedge

[§4.6 Pattern supply example] "C3 supplied the ideal-vs-reality axiom directly" -> "C3 applied the ideal-vs-reality axiom" | "supplied" is marketing verb

[§4.6 Pattern supply example] "The Mem0 retrieval had the biography; the specification had the pattern" -> "Mem0 retrieval provided the biographical facts; the specification provided the interpretive pattern" | "had" is too colloquial; parallel structure needs matching verbs

[§4.6 Over-theorization example] "C3 elaborated a theory of 'gratitude as epistemology'" -> "C3 generated a theory of 'gratitude as epistemology'" | "elaborated" is acceptable but "generated" is more neutral

[§4.6 Default-axiom example] "The axiom is correct on average but overfires on this specific unconditional moment" -> "The axiom is correct on average but applies inappropriately to this specific unconditional moment" | "overfires" is invented marketing compound; "correct on average" is vague-strength descriptor

[§4.6 system balance section] "wins on interpretation-heavy questions, loses on counter-example moments" -> "improves on interpretation-heavy questions, worsens on counter-example moments" | "wins/loses" is pitch-deck language

[§4.6 Letta description] "big wins when the few unique facts align with the specification's axioms" -> "larger improvements when the few unique facts align with the specification's axioms" | "big wins" is pitch-deck language

[§4.6 Zep description] "cleanest profile, fewest catastrophic losses" -> "most balanced distribution, fewer large regressions" | "cleanest" is superlative; "catastrophic" is hyperbolic marketing language

[§4.6 Supermemory description] "most hurts-heavy because strong retrieval means the plain answer is often already there" -> "shows more regressions because strong retrieval often already provides the surface answer" | "hurts-heavy" is invented compound noun; "plain answer" is colloquial

[§4.6 Keckley Q21 section heading] "The cleanest cross-substrate replication in the study" -> "Cross-substrate replication: Keckley Q21" | "cleanest" is superlative marketing language; heading should be neutral

[§4.6 Keckley Q21 opening] "produces a spec-induced refusal on Supermemory (§1.3) and on Base Layer's retrieval substrate, with identical −2.33 per-question Δ on both systems" -> "produces a specification-induced refusal on both Supermemory and Base Layer, with identical −2.33 per-question Δ" | "spec-induced" is jargon abbreviation; "identical" is superlative (use "matching" or "the same")

[§4.6 Keckley Q21 opening] "The held-out passage carries Keckley's interior motive for not visiting, which the training half of the corpus does not contain; no retrieval substrate can surface it." -> "The held-out passage contains Keckley's interior motive for not visiting, which does not appear in the training half of the corpus; no retrieval substrate can recover it." | "carries" is colloquial; "surface" is marketing verb

[§4.6 Keckley Q21 mechanism] "The specification's documented-dignity and intimate-authority axioms then trigger the same refusal pattern" -> "The specification's documented-dignity and intimate-authority axioms then produce the same refusal pattern" | "trigger" is marketing verb

[§4.6 Keckley Q21 table caption] "Different retrieval substrates, different fact pools, different baseline behaviors, identical specification; the refusal and penalty reproduce exactly when C1 is in productive-speculation mode" -> "Different retrieval substrates, different fact pools, different baseline behaviors, identical specification. The refusal and penalty occur with the same magnitude when C1 is in productive-speculation mode" | "identical" is superlative; "reproduce exactly" is marketing language; "productive-speculation mode" is jargon

[§4.6 Keckley Q21 table caption] "shrink when C1 is already hedging, and reverse when C1 was already refusing" -> "decrease when C1 is already hedging, and reverse when C1 was already refusing" | "shrink" is colloquial

[§4.6 Keckley Q21 table caption] "This is the single cleanest cross-substrate replication the study produced." -> "This is the most consistent cross-substrate replication in the study." | "cleanest" and "single" are superlative marketing language

[§4.6 measurement section] "Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-substrate refusal) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*." -> Break into two sentences; this is dense | "more/less informative" is vague-strength descriptor; quantify or use "provides additional information about" and "provides less information about"

[§4.6 measurement section] "A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that rewards epistemic honesty on questions the retrieved facts cannot answer without fabrication, would recover a cleaner measurement of the specification's real effect." -> "A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that credits epistemic honesty on questions where retrieved facts are insufficient, would provide a more complete measurement of the specification's effect." | "rewards" is marketing verb; "cleaner" is superlative; "real effect" implies the current measurement is unreal

---

## Dense Passages

[dense §4.6 opening] "The three mechanisms identified on Supermemory (the specification supplies a pattern retrieval cannot, the specification over-theorizes a question retrieval already answered plainly, the specification induces a refusal the content-match rubric penalizes) reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate." -> Separate into: "The three mechanisms identified on Supermemory reproduce across all five memory systems: [1] the specification supplies a pattern retrieval cannot; [2] the specification over-theorizes questions retrieval already answered plainly; [3] the specification induces refusals that the content-match rubric penalizes."

[dense §4.6 measurement section] "Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-substrate refusal) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*." -> "Three patterns (Pattern 2 over-theorization, Pattern 3 refusal, and the Keckley Q21 cross-substrate refusal) describe cases where the specification produces responses that are more informative about subject reasoning but less informative about the specific surface content of the held-out passage."

---

## Register-Cleanliness Scores by Section

| Section | Score | Notes |
|---------|-------|-------|
| §4.6 Opening paragraph | 2 | Heavy use of "large," "reproduce," "most consistent"; vague-strength descriptors throughout |
| §4.6 Table caption | 2 | "wins and losses," "strongest row," "mixture" language reads like pitch summary |
| §4.6 Three mechanisms (Pattern definitions) | 3 | Clearer than opening, but "supplies," "over-theorizes," "induces" are marketing verbs; "In plainer language" is self-aware hedge |
| §4.6 Pattern examples (Ebers, Yung Wing, Keckley) | 3 | Narrative is clear but uses "supplied," "elaborated," "overfires"; colloquial "had the pattern" |
| §4.6 System balance section | 2 | "wins/loses," "big wins," "cleanest profile," "hurts-heavy," "catastrophic losses" are all pitch-deck register |
| §4.6 Keckley Q21 section | 2 | "cleanest replication," "identical," "reproduce exactly," "trigger," "surface" are marketing language; superlatives throughout |
| §4.6 Measurement section | 3 | More measured tone but "rewards," "cleaner measurement," "real effect" weaken precision |

**Overall §4.6 Register Score: 2.4/5** — This section reads as a research narrative trying to convince rather than report. The repeated use of "wins/losses," superlatives ("cleanest," "strongest," "most consistent"), and marketing verbs ("supplies," "triggers," "reproduces," "overfires") create a pitch-deck tone. The section would benefit from systematic replacement of vague-strength descriptors with quantified claims and neutral verbs. The table captions are particularly problematic, using language that frames findings as victories rather than observations.

---

