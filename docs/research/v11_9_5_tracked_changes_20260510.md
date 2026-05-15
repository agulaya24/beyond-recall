# v11.9.5 docx tracked changes

Total paragraphs with tracked changes: **9**

---

## Change 1 (paragraph 623)
**Inserted:** WT
**Deleted:** t
**Paragraph (post-accept):** 5.1 Synthesis: What The seven findings together establish

---

## Change 2 (paragraph 624)
**Inserted:** g when using their native ingestion pipelines
**Deleted:** g.
**Paragraph (post-accept):** Across 14 historical subjects and five memory-system configurations, the study tested whether a static interpretive layer increases an AI system’s representational accuracy of a specific person. This was operationalized via behavioral prediction on held-out autobiographical text scored by a calibrated, baselined five-judge LLM panel. The layer reliably moves the model from refusal or generic guessing to grounded subject-specific responses where the model has insufficient pretraining on the subject . 55% of low-baseline questions cross at least one rubric anchor upward, and roughly 1 in 5 cross two or more anchors, meaning the model goes from refusal to a grounded subject-specific prediction in qualitative steps rather than incremental score nudges. The matched layer’s content does the work, not the structure of the prompt: an adversarial wrong-Spec control actively degrades performance below baseline. On interpretation-heavy questions where retrieved facts alone underdetermine the answer, the layer supplies the interpretive pattern existing memory systems cannot; three of four commercial systems show positive aggregate prediction-accuracy lift under at least one configuration as a result. The layer recovers most of the predictive accuracy of the full source corpus at 5x to 80x smaller context, and it eliminates response hedging on questions retrieval alone could not ground (41.2% baseline hedging drops to 0.4%). Current memory-system providers do not converge on which facts are most relevant given identical input, even under relaxed similarity matching when using their native ingestion pipelines

---

## Change 3 (paragraph 626)
**Inserted:** RA,
**Deleted:** The construct (ra)
**Paragraph (post-accept):** Representational Accuracy, has been validated directionally by the data but not absolutely by human annotation; that human-validation follow-up is the highest-priority next step (§7). Robustness checks against cross-provider response models, judge-panel composition, and protocol choices are in §4.6.

---

## Change 4 (paragraph 631)
**Inserted:** ,
**Deleted:** .
**Paragraph (post-accept):** The per-question mechanism beneath the gradient is that the Spec categorically lifts interpretation-required questions while leaving questions the model already answers correctly, largely unchanged. This conditional benefit is why the aggregate is not inflated by Spec-induced noise on questions where retrieval already suffices, and why the gradient’s slope is real rather than artifactual

---

## Change 5 (paragraph 637)
**Deleted:** §5.4 picks up what happens when the interpretive layer is composed with memory-system retrieval.
**Paragraph (post-accept):** Interpretation in this study’s context has to do with representational accuracy: how well an AI system represents the patterns that shape how a specific person reasons. Stored facts and observed preferences are surface outputs of those reasoning patterns; the interpretive layer is the implicit understanding of the patterns themselves. Recall, preferences, and interpretation are forms of calibrating an AI toward a specific person at different depths: facts and preferences calibrate to surface outputs, while the interpretive layer calibrates to the patterns that produce those outputs. Behavioral alignment requires the deeper calibration.

---

## Change 6 (paragraph 646)
**Deleted:** The §4.6.5 sensitivity check confirms the finding holds across both derangement protocols.
**Paragraph (post-accept):** The wrong-Spec controls in §4.3 establish that the matched layer’s content does the work, not the structure of the prompt. Three conditions bracket the finding: a matched layer increases representational accuracy; a random derangement of specifications lands near baseline; an adversarial mismatch (a culturally and temporally distant subject’s specification) actively degrades performance below baseline. Structured prompting alone with arbitrary content does not produce the lift; sufficiently mismatched content makes the model worse than no context at all.

---

## Change 7 (paragraph 654)
**Inserted:** .T
**Deleted:** ;t
**Paragraph (post-accept):** Compression is a peculiar property to lean on. Regardless of how well a language model uses long context, there is always more context to add. Today’s models cannot actively serve or construct a representationally accurate understanding of a person from a long-context corpus, which is why compression is load-bearing. That capability gap could close. But even if models acquire that capability, the question is not whether they can use the context well; it is whether they have the right context at all. The conversation shifts from context to representation: the question is which representation the model should reason from, who owns it, and whether it is faithful. Compression makes personalization operationally tractable today; a user-owned, portable, accurate representation of how a specific person interprets and reasons is what the personalization problem reduces to forever.

---

## Change 8 (paragraph 705)
**Inserted:** memory system
**Paragraph (post-accept):** Retrieval-overlap follow-ups (from the surfaced §4.4.1 finding). Two measurement studies remain open after the §4.4.1 sensitivity check that already covers K=5 and semantic-similarity matching for K=10 in both controlled and native memory system configurations:

---

## Change 9 (paragraph 743)
**Deleted:** and cost
**Paragraph (post-accept):** Compute. All response generation and judging used commercial APIs (Anthropic, OpenAI, Google) at standard rates. No specialized hardware was used. All experiments are runnable on a standard developer laptop.

---
