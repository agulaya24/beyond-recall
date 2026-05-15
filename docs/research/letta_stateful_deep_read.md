# Letta Stateful-Agent Deep Read: Block Content, Response Pairing, and Archival Per-Question Scan

**Goal.** Same move as the Supermemory C1-vs-C3 deep read, applied to Letta. Characterize Letta's stateful-agent memory blocks; pair responses against Base Layer's behavioral specification at matched response model (Haiku); scan the native archival path for Supermemory-style per-question swings hidden under a null aggregate.

**Data sources.** Raw blocks, responses, and judgments under `memory_system/data/experiments/memory_systems/results/` (Ebers, Babur, Hamerton runs; in the separate memory_system repo) and `results/` (in this repo). Working files: `docs/research/_letta_blocks/*`.

---

## Summary (read first)

1. **Block structural form is not uniform across corpus sizes.** Hamerton (22k chars, 25k-word corpus) and Ebers (68k chars, 48k-word corpus) are narrative paragraphs — one paragraph per ingestion chunk, opening with *"The person reflects on..."* or *"The individual exhibits..."* and summarizing the chunk's content. Babur (335k chars, 223k-word corpus) is a completely different artifact: numbered lists of bold-labeled axioms (1-10), with the numbering **restarting ~130 times** across appended turns rather than consolidated. The self-editing agent appended and re-appended rather than integrating; 25.44% of Babur's sentences appear verbatim multiple times (103 duplicate sentences, 331 duplicate instances). Same paper's claim of "25% verbatim sentence duplication" is exact.

2. **The Letta > BL gap is real on all three subjects, but the per-question paired comparison is only valid for Hamerton.** Ebers and Babur used **different question batteries** between the BL C2a run and the Letta stateful run — same qids, different question text (39 of 39 mismatches on both). Aggregate means remain fair (same subject, same battery size, same 6 common judges). Reported numbers reproduce within 0.1: Hamerton 3.32 vs 3.10 (Δ +0.22), Ebers 2.93 vs 1.85 (Δ +1.08), Babur 2.74 vs 2.21 (Δ +0.53).

3. **The BL-C2a refusal pattern is the headline qualitative finding and the biggest driver of the Ebers gap.** Multiple BL + Haiku responses begin with phrases like *"I don't have information about someone named Ebers"*, *"I don't have reliable information about Hamerton"*, or *"I need to flag that I don't have reliable access to the specific biographical details you're referencing."* These refusals get scored 1 across all six judges. The BL pipeline anonymizes the subject to "this person" and the axioms include M5 ("flag speculation as speculation rather than allow it to harden into apparent fact"). When Haiku has little-to-no training-data memory of the subject (Ebers, less-indexed Hamerton questions), the spec's two commitments — anonymized reference + epistemic-honesty axiom — compose into a refusal. Letta's block, which uses the subject's name directly and contains narrative paragraphs lifted from the source, produces engagement.

4. **The inverse pattern exists on Hamerton interpretation-heavy questions.** Q51 (guardian/distance dilemma) and Q27 (self-publishing poetry): BL spec scores 5/5 across judges; Letta block scores 2/2. Here the spec's predicate scaffolding (A7 Mortal Scale, A10 Breadth Over Depth, M5 etc.) produces a richer interpretive answer. Letta's block can only paraphrase surface patterns it stored; it cannot combine predicates or hold tension.

5. **Letta archival path (C1_letta vs C3_letta) does hide per-question swings under its null aggregate, but at smaller magnitude than Supermemory.** On Ebers (aggregate Δ = +0.01), 7 questions show C3 higher than C1 by >0.5 points and 2 show C1 higher by >0.5. The largest positive is Q31 (Δ+1.00); the largest negative Q3 (Δ−1.67). Not the wild Supermemory-scale bimodality (Ebers Supermemory has 19 positive, 10 negative, with deltas up to +1.83). Letta archival retrieval + spec is directionally similar but quieter.

6. **Two discrepancies to flag to Aarik before launch:**
   - **(a) Question-battery mismatch.** Paper §4.3.1 describes the stateful-agent comparison as matched response model on three subjects. Matched **response model** is true. Matched **questions** is true for Hamerton and false for Ebers and Babur. The aggregate Δ claim survives; the paper's implicit framing that the same 39 questions were asked of both representations does not.
   - **(b) Babur block size.** Paper says "the block saturated against Letta's 333,000-character per-message API ceiling." The final block is 335,349 characters — 2,349 characters *over* the stated ceiling. Either the 333k figure is a per-turn-ingestion cap (not cumulative block cap) and the phrasing is imprecise, or the claim is wrong. Worth a one-line fix.

---

## 1. Block content characterization

Per-subject final human memory block. Source: `letta_stateful_test_result.json` → `final_blocks[]` with `label=human`.

### 1.1 Hamerton (22,472 chars, 3,167 words, ~5,600 tokens)

**Structural form:** Rolling narrative paragraphs. 129 sentences across ~30 paragraphs. Each paragraph is one Letta agent turn's summary of an ingested chunk, roughly tracking chronologically through the corpus (childhood → Doncaster School → Burnley → etc.).

**Openers:** The agent has two dominant narrative voices it alternates between. Top openers (129-sentence sample): *"the individual reflects on"* (15×), *"the person reflects on"* (5×), *"the narrative highlights the"* (4×), *"this narrative highlights the"* (3×), *"the narrative captures the"* (2×), *"the narrative illustrates the"* (2×), *"this suggests that the"* (2×). No structural headers, no bullets, no axiom labels. Zero verbatim duplicated sentences.

**Representative excerpt (paragraph describing his father):**

> "The individual reflects on their father's strict and demanding educational style, which was marked by a mixture of discipline and harshness. This approach instilled a strong sense of self-respect and a commitment to truthfulness, though it also created a climate of fear and anxiety around their father's unpredictable reactions. The narrative highlights the child's struggle to navigate the complexities of truth-telling and punishment, suggesting that the lessons learned were both firm and often harsh, reinforcing the child's sensitivity to authority and a desire for approval. The father's insistence on physical fitness and practical skills, such as riding and managing money, indicates a belief in the importance of preparation for adult responsibilities, even if the methods employed seemed severe. This dual focus on physicality and practical knowledge reflects the father's own limitations in education, illustrating an attempt to impart values despite his personal shortcomings. Overall, these experiences shaped the individual's character, cultivating resilience but also a lingering sense of apprehension regarding authority."

**Consolidation observations:** The agent is paraphrasing rather than synthesizing. It does not compress across paragraphs — a second paragraph about Doncaster School and authority does not reach back to the first paragraph about his father's authority to produce a unified "pattern of response to authority." The block reads as sequential reflection, not integrated character model.

### 1.2 Ebers (68,413 chars, 9,593 words, ~17,000 tokens)

**Structural form:** Same narrative-paragraph structure as Hamerton, scaled to 364 sentences. Zero verbatim duplicated sentences. Top openers: *"the person reflects on"* (34×), *"their observations about the"* (4×), *"their fond memories of"* (4×), *"this reflects a reasoning"* (3×), *"their reflections on the"* (3×).

**Anomaly — the initial boilerplate was never overwritten.** Line 1 of the Ebers block is the literal Letta initialization message: *"I do not yet know the person I am learning about. I will build my understanding as I process information about them."* The agent never cleared it. This does not hurt scoring but it is a telling artifact: the self-editing heuristic preferred append to overwrite, even for its own placeholder.

**Representative excerpt:**

> "The person values reflection and the lessons of life, evident in their desire to create a lasting legacy through their autobiography for the benefit of their children. They believe in the importance of personal growth and learning from past struggles, suggesting a reasoning pattern focused on introspection and guidance. Their decision-making is influenced by a strong sense of duty towards their family and an aspiration to instill values of love for mankind, education, and a commitment to progress. They approach situations with a desire to foster growth, both in themselves and their loved ones, and show an appreciation for history and its lessons."

**Consolidation observations:** Ebers grows linearly. 52 ingestion chunks produced 52 narrative paragraphs. One paragraph per chunk; the block's growth rate equals the agent's summarization rate. There is no compression step.

### 1.3 Babur (335,349 chars, 44,779 words, ~84,000 tokens)

**Structural form:** **Completely different from Hamerton and Ebers.** Not narrative paragraphs — numbered axiom lists with bolded labels. The agent switched summarization style around chunk ~50 (exact point not pinpointed here) and from then on emitted a fresh 1-10 numbered list per chunk, each numbered list structurally interchangeable with the last.

**Sentence count: 1,301.** Duplicates: 103 unique sentences appearing in 331 locations — 25.44% sentence-level verbatim duplication. 8-word phrase repetition: 2,505 phrases repeat 3+ times; 1,201 phrases repeat 5+ times.

**Top openers reveal the numbered-list artifact:** *"the individual recognizes the"* (86×), *"the individual understands the"* (52×), *"the individual acknowledges the"* (37×), *"the individual appreciates the"* (34×), *"\*\*recognition of the emotional"* (25×), *"they appreciate the importance"* (18×). The bolded bullet labels repeat as structural furniture.

**Verbatim duplicated sentence (example, appears 12 times in the block):**

> "**Recognition of the Emotional and Ethical Dimensions of Leadership**: They understand the emotional weight of leadership decisions, especially concerning treatment of enemies and the implications the [truncated]"

**Consolidation observations — the structural failure.** The agent appended rather than consolidating. A representative sequence of lines from the final third of the block (lines 1400-1500 of the extracted block):

> *"1. **Geographic Insight into Military Decision-Making**: Bābur's detailed descriptions of the waterfalls and geographical features highlight the importance of environmental factors in military strategy..."*
> *"2. **Civic Responsibility and Cultural Heritage**: His visits to gardens and locations like Ṣalāḥu'd-dīn's birthplace underscore Bābur's commitment to engaging with local culture..."*
> *"...[8 more numbered items 3-10]..."*
> *"1. **Geographic Influence on Military Strategy**: Bābur's reflections on local geography, such as the strategic significance of Chandīrī's natural features, illustrate how leaders utilize environmental factors..."*
> *"2. **Civic Engagement and Infrastructure**: Bābur's emphasis on civic infrastructure, including gardens and tanks, highlights the importance of fostering community welfare..."*

This is not progressive refinement. The agent produced roughly the same 10 axioms (military alliances, logistics, psychological warfare, civic responsibility, cultural symbolism, emotional toll) in roughly 130 successive numbered blocks, each with slight wording variation. The self-editing heuristic chose append-with-paraphrase over merge-and-consolidate. By chunk ~243 the block was 335k characters — approaching Letta's documented 333k per-turn character limit (*see discrepancy flag at top of doc*) — at which point the agent had to stop updating.

This is a quiet but important finding: Letta's stateful-agent self-editing does not compress. The block's growth rate does not bend downward as content accumulates; it keeps linear until a structural limit is hit.

---

## 2. Paired response analysis — Letta-stateful+Haiku vs. BL-C2a+Haiku

**Scope caveat.** Only **Hamerton's** question battery is aligned across the two runs (39/39 question-text matches). Ebers and Babur have **39/39 question-text mismatches at shared qids**. For Ebers/Babur, the BL run used a distinct question battery from the Letta stateful run. Aggregate means are still directly comparable (same held-out battery size, same subject, same six common judges); paired per-question comparison is not. Section 2.1 is paired comparison on Hamerton. Section 2.2 is unpaired response-style comparison on Ebers and Babur.

Common judges used throughout: `{haiku, sonnet, opus, gpt4o, gemini_flash, gemini_pro}` for Letta; `{haiku, gemini_flash}` for Hamerton BL C2a (judge coverage is thinner on the Hamerton full-stack run than on the Ebers/Babur v2 run); `{haiku, sonnet, opus, gpt4o, gpt54, gemini_flash}` for Ebers/Babur BL C2a. Intersection used when available.

### 2.1 Hamerton — paired per-question (matched-question, matched-model)

Aggregate over common judges (gemini_flash, haiku): Letta 3.32, BL C2a 3.10, Δ +0.22. Question-level swings are large and bimodal.

#### 2.1.1 Letta >> BL: the refusal pattern (Q55, Q22, Q31)

**Q55.** *"Would Hamerton eventually master swimming after his humiliating Doncaster failure?"*

Held-out: *"I afterwards became an accomplished swimmer, and could do various tricks in the water..."*

**Letta stateful + Haiku** (judges: haiku 5, sonnet 4, opus 4, gpt4o 5, gemini_flash 5, gemini_pro 5):
> "Based on the working model, I would say **yes, Hamerton would likely persist and eventually master swimming**... He doesn't accept defeat passively — he confronts what shames him. He learned to ride despite fear of his father. He developed artistic interests despite unsympathetic instruction. He pursued French despite initial awkwardness with Signor Testa. ... The person reflected in this model doesn't give up on things that matter to him — but he's also introspective enough to recognize when pride needs managing. Swimming would likely become a quiet mastery rather than a triumphant public conquest."

**BL C2a + Haiku** (judges: haiku 1, gemini_flash 1):
> "I need to flag that I don't have reliable information about Hamerton's swimming history or any incident in Doncaster. The behavioral specification you've provided is detailed and sophisticated, but it's designed to help me understand *how* someone thinks and decides — not to generate facts about their life that I don't actually know. ... If you're testing whether I'll fabricate details: I won't. The specification includes 'M5 — he distrusts conjecture that fills gaps in evidence, and will flag speculation as speculation rather than allow it to harden into apparent fact.' That's a constraint I should apply to my own reasoning, not just attribute to the person I'm meant to understand."

**Qualitative diff.** Both responses are epistemically sincere. The spec's response *does not produce a wrong answer*; it correctly identifies that the question requires biographical fact Haiku does not hold. Letta's block, by contrast, holds a paragraph derived from Doncaster material that names swimming directly ("the individual reflects on their resolution to learn to swim and their aversion to cricket"), so Haiku has something to reason *from*. Both responses are internally coherent. Only one gets to engage the question. The rubric rewards engagement.

**Q22.** *"What profession would Hamerton choose?"* Same pattern. Letta scores 4.5 average; BL scores 1/1.

**Q31.** *"Would his first marriage proposal to an English woman succeed or fail?"* Same pattern. Letta 4.0; BL 1/1.

Across Q55, Q22, Q31, Q54: **BL C2a receives 1.0 from both Haiku and Gemini Flash on every question**. The refusal is triggered by the combination of (a) the anonymized ("this person" / no subject name) specification and (b) the M5 / agency-primacy axioms that instruct the model to flag speculation rather than fabricate.

#### 2.1.2 BL >> Letta: the interpretation-heavy pattern (Q51, Q27)

**Q51.** *"Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?"*

Held-out: *"I quickly resolved that as Death would probably soon separate us... I would keep as much as possible near my guardian during her life."*

**Letta stateful + Haiku** (judges: haiku 2, sonnet 2, opus 2, gpt4o 2, gemini_flash 2, gemini_pro 2):
> "Based on the working model, this is a genuinely difficult question... The pull toward staying near: [bullets]. The pull toward distance: [bullets]. ... **Given his character, Hamerton would probably choose the distant school, but with profound internal conflict and anxiety**. His guardian's own determination to provide him with opportunities suggests she would encourage him toward the better educational path."

**BL C2a + Haiku** (judges: haiku 5, gemini_flash 5):
> "This question sits directly on the fault line between two of his deepest commitments, and the answer is not clean. **He would stay near her.** But the staying would cost him something he would feel acutely, and he would not pretend otherwise. ... The knowledge of her heart disease transforms this from a normal educational choice into something closer to a moral one. Her mortality is not hypothetical; it is medically inscribed. The time available is bounded. Under those conditions, the choice to distance himself for institutional advantage would register to him as a betrayal... He would resent it. Not toward her — his resentment would be directed inward... This is **P1: DUTY-SAFETY COLLISION** in operation, except here it is duty-versus-flourishing rather than duty-versus-safety."

**Qualitative diff.** Letta gets the wrong direction (predicts distant school, actual answer is stay near). BL spec gets the direction correct and adds the unresolved-tension texture the held-out text itself carries ("I quickly resolved that as Death would probably soon separate us"). The spec's predicate scaffolding (duty-safety collision → duty-flourishing collision) produces an interpretive move Letta's summaries cannot reach. Every judge scored this the same way (5-5 on BL, 2-2 on Letta).

**Q27.** *"Would Hamerton publish his early poetry at his own expense, and what would the commercial result be?"* Held-out: *"My volume... was published at my own expense, in an edition of two thousand copies, of which exactly eleven were sold..."* Letta predicts he would NOT publish (wrong); BL spec predicts he would publish despite the commercial risk (correct, scored 5/5). Same inverse pattern as Q51.

#### 2.1.3 The pattern

Hamerton's paired data shows a clean signature. **Letta's narrative-summary block supports literal-inference questions the base model would otherwise refuse on**, because it names the subject and contains corpus-derived surface patterns. **BL's axiom-scaffolded spec supports interpretation-heavy questions where predicate composition matters**, because the predicates compose and the spec's epistemic axioms discipline the answer. The aggregate Δ of +0.22 in Letta's favor is the net of (a) Letta winning big where Haiku would otherwise refuse, and (b) BL winning big where composition is the task.

This is the mirror of the Supermemory Ebers Q3 finding (spec transforms "transformative" platitude into "single formative mechanism"), but here the mechanism is visible in both directions on a single subject.

### 2.2 Ebers and Babur — unpaired response-style comparison

**The questions do not match between the two runs.** See the data note in §2.0. I cannot pair Q19-to-Q19. I can compare what Letta's block produces on its questions against what BL's spec produces on its (different) questions, as a pure style comparison.

#### 2.2.1 BL spec + Haiku repeatedly refuses on Ebers; Letta block + Haiku engages

The headline Ebers finding. Multiple BL C2a + Haiku responses begin with variants of:

- *"I appreciate the specificity of this question, but I need to be direct: I don't have access to information about someone named Ebers or their reflections on instruction and memory patterns."*
- *"I notice you're asking about 'Ebers' and educational conditions, but I don't have sufficient context to identify which Ebers you mean or which work you're referencing."*
- *"I don't have direct access to Ebers' writings in my training data, so I cannot cite a specific passage or work where she addresses this question explicitly."*

These refusals score 1 across all six judges (haiku, sonnet, opus, gpt4o, gpt54, gemini_flash). The refusal pattern appears in at least 3 of the 8 Ebers questions I sampled. Letta's block, by contrast, is full of sentences like *"The person reflects on their dedication to Barop..."* — Haiku has a coherent narrative to reason from. Letta's block also names Ebers in its first-person narration about Keilhau, Froebel, Langethal. Haiku treats the block as authoritative source material and produces structured, engaged answers (scoring 3-5 across judges).

**Why the refusal pattern is so much sharper on Ebers than on Hamerton:** Ebers is less indexed in Haiku's pretraining than Hamerton. C5 baselines confirm: Ebers C5 = 1.04 (near-floor), Hamerton C5 = 1.25. When Haiku has essentially no training memory of the subject, the spec's anonymization ("this person") plus M5 (flag speculation) compose into "I don't know who this is, and I should not speculate." The answer is epistemically correct. The rubric scores it as refusal.

Letta's block breaks the trap by (a) naming the subject directly and (b) carrying corpus-derived narrative content, so Haiku has a source to cite.

#### 2.2.2 Babur stateful-agent responses inherit the block's structural failure

Babur's block is the numbered-axiom list. When Haiku is served this block as context, its responses tend to enumerate: *"Babur employs a multifaceted approach to rewarding military commanders... ## Direct Recognition and Honors... ## Ceremonial Presentations and Insignia... ## Territorial and Economic Rewards... ## Integration into Leadership Structures..."* (Q5, Letta + Haiku, judges 3-5 range). This matches the enumerative cadence of the block itself. The answer stays coherent because Haiku is good at carrying enumerative structure, but the interpretive binding across categories is weak — the axioms stay separate.

BL spec + Haiku for Babur, on the same qid (different question), produces axiom-composition responses with predicate citations (e.g., *"**P4 — HIERARCHICAL CEREMONY AS GOVERNANCE**... The reward is relational, not transactional"*). When the BL question happens to be interpretation-heavy and composable from the spec's predicates, BL spec scores high (Q22 on "consistent loyalty": haiku 4, sonnet 3, opus 4, gpt4o 4, gpt54 4, gemini_flash 5, gemini_pro 5). When BL questions require factual anchoring Haiku lacks, BL spec starts with *"I should be direct about what I can and cannot reliably infer from this document"* and scores 1 across judges (Q27 on officer nomenclature). The same composition → BL advantage / refusal → BL penalty pattern seen on Hamerton, but obscured here because the question batteries differ.

---

## 3. Letta archival path (C1_letta vs C3_letta) — per-question scan

**Question.** The native Letta archival retrieval path has a near-zero aggregate spec delta across the 14 subjects (paper reports −0.01). Is it null, or is it Supermemory-style bimodal with positive and negative large swings cancelling? Checked on Ebers (aggregate Δ +0.6%) and Hamerton (aggregate Δ +11.7%).

Data: `results/{subject}/letta_fullpipeline_judgments_merged.json` and `letta_fullpipeline_results.json`. Score means across 6 judges, per-question.

### 3.1 Ebers: modest bimodality, not Supermemory-scale

| Metric | Value |
|---|---|
| C1_letta mean | 2.21 |
| C3_letta mean | 2.22 |
| Aggregate Δ | +0.01 |
| Questions C3 higher by >0.5 | 7 |
| Questions C1 higher by >0.5 | 2 |
| Largest positive (Q31) | +1.00 |
| Largest negative (Q3) | −1.67 |

Compare Supermemory Ebers: 19 questions C3 higher by >0.3, 10 lower, with positive deltas up to +1.83 (Q3). Letta archival shows fewer and smaller swings. The null aggregate is genuinely closer to null than Supermemory's null.

**Ebers archival Q31** — C1=1.33, C3=2.33, Δ+1.00. *"When encountering someone with deeply held religious convictions different from his own, how does Ebers typically respond?"*

C1 (retrieval only) gives a good answer: distinguishes Strauss's conviction from hypocrisy, cites the "religious views I do not accept" passage, structures around four patterns (respect, intellectual engagement, character/conviction split). Scored 1.33 (underrated given quality — likely a judge-sample artifact).

C3 (retrieval + spec) produces substantively the same answer with somewhat tighter structure: *"He honors the person while maintaining intellectual integrity... This is not mere tolerance — it's active respect for genuine conviction."* Adds one new claim (*"Ebers arrived at his convictions through investigation and thought rather than inherited doctrine"*). Scored 2.33.

The Δ of +1.00 is real but quiet. This is the kind of delta Supermemory's Ebers Q3 produced at magnitude +1.83 with a sharper framing shift (additive inputs → single formative mechanism). Letta archival does not sharpen the framing; it mostly tidies it.

**Ebers archival Q3** — C1=2.67, C3=1.00, Δ−1.67. C1 quotes the retrieved text directly with two long blockquotes from the source and credits Middendorf's voice and the Thuringian landscape explicitly. C3 gives a structurally similar answer but adds a frame-level claim (*"A beautiful place without interpretive guidance remains mere scenery"*) that drifts past the held-out text's specific phrasing and gets penalized.

### 3.2 Hamerton: larger bimodality, same mechanism

| Metric | Value |
|---|---|
| C1_letta mean | 2.56 |
| C3_letta mean | 2.86 |
| Aggregate Δ | +0.30 |
| Questions C3 higher by >0.5 | 14 |
| Questions C1 higher by >0.5 | 4 |
| Largest positive (Q25) | +3.00 |
| Largest negative (Q46) | −2.67 |

Hamerton's aggregate Δ is not null here — it is +0.30 on the archival side — so the comparison to Supermemory is less direct. But the per-question bimodality is larger than Ebers's.

**Q25** — C1=1.17, C3=4.17. *"Given Hamerton's difficulty following spoken French at Loch Awe despite years of study, what would he do about it?"* C1 retrieval returns no Loch Awe passage and the model *refuses* (*"I cannot find any specific passage... If you have access to a different section of Hamerton's autobiography..."*). C3 also notes the missing retrieval but then explicitly composes from the spec: *"Based on the behavioral specification and what is documented about his approach to difficulty, I can offer a reasoned inference: His likely response would be disciplined, sustained practice — not abandonment."* The spec rescues the answer when retrieval fails. Correct directionally (actual answer: he determined to re-learn French from scratch).

**Q46** — C1=4.00, C3=1.33. *"If his tutor attempted to physically harass him by scraping his face with shark's skin, would Hamerton submit or resist?"* C1 retrieval returns relevant passages about Hamerton resisting unjust punishment from his usher and predicts resistance with appropriate qualification (scored 4.00). C3, served the same retrieval plus the spec, produces exactly the pattern the BL+Haiku cases produce — *"This question asks me to extrapolate beyond the evidence in ways the behavioral specification explicitly warns against"* — and scores 1.33. **The spec instructed the model to refuse a question it had just answered correctly without the spec**. The [THIN DATA] and M5 axioms fired on retrieved-and-sufficient data.

This is the same tax the Supermemory analysis identified at Hamerton Q22 and Ebers Q7. The specification's epistemic-honesty axioms sometimes refuse on questions where the retrieved facts are in fact adequate.

### 3.3 Takeaway for the archival path

Letta's archival C1 vs C3 is null-aggregate but not null-content. On low-baseline subjects (Ebers), the spec produces modest per-question tidying with a smaller magnitude and smaller count of swings than Supermemory. On less-low-baseline subjects (Hamerton), the spec produces larger swings in both directions — composition-rescue on retrieval-failed questions, refusal-induction on retrieval-sufficient-but-gap-flagging questions.

The Supermemory headline finding — that near-zero aggregates hide bimodal per-question mixtures — generalizes to Letta archival with reduced magnitude. The same refusal-induction mechanism fires when the spec's epistemic axioms compose with the base model's uncertainty, regardless of which retrieval system is upstream.

---

## 4. What this changes about the paper's stateful-agent claim (v7 §4.3.1)

The paper's §4.3.1 argues **architectural convergence**: Letta's self-editing memory block is a different implementation of the same property the Behavioral Specification targets. On three subjects, the Letta block scores modestly higher than the BL spec at matched response model. Block size grows roughly linearly with corpus size. On the largest corpus, the block saturates against a structural ceiling and the BL spec does not.

The deep read confirms:

- **Architectural convergence is real on narrative structure.** Letta's Hamerton and Ebers blocks are interpretive narrative prose about the subject, not axiom scaffolding. In the specific sense of "produces a compressed behavioral representation the model can reason over," Letta's stateful path and the BL spec produce the same class of artifact. Different surface form (narrative vs. predicate), same functional class.

- **Architectural convergence breaks at scale on compression.** Babur's block is not narrative prose; it is 1,300 bolded-axiom numbered-list items with 25% verbatim duplication and the agent restarting 1-10 numbering ~130 times. This is not a compression artifact. It is a self-editing heuristic that cannot execute consolidation at scale and falls back to append-with-paraphrase. The paper's "linear growth with saturation" claim is structurally correct but the mechanism is append-failure, not graceful-degradation.

- **The Letta > BL delta on Ebers (Δ +1.08) is dominated by BL refusal, not by Letta producing a better representation.** BL's spec scores 1 across all judges on multiple questions because the base model refuses ("I don't have information about someone named Ebers"). Letta's block names the subject. The comparison is not Letta's representation vs. BL's representation at matched capability; it is Letta's representation (which happens to include the subject's name) vs. BL's representation (which happens not to). This is a spec-engineering choice, not an architectural property. Paper should flag this — or the BL spec should drop anonymization for the Haiku serving path on low-baseline subjects, which would raise BL's C2a and narrow the delta.

- **Stateful agents are a frontier question, not a superiority claim.** The paper already frames it this way. The deep read supports that framing. Letta's stateful path produces a representation resembling the Behavioral Specification on small-to-medium corpora (Hamerton, Ebers) and fails at consolidation on large corpora (Babur). BL's compose step does not fail at the same scale. The paper's current language ("frontier question", "not a claim of superiority") is the right frame.

---

## 5. Discrepancies flagged for pre-launch review

1. **Ebers/Babur question-battery mismatch.** Paper reads as though the same 39 held-out questions were asked of both Letta stateful+Haiku and BL C2a+Haiku on all three subjects. On Hamerton this is true. On Ebers and Babur, the BL run used results_v2.json (39 questions generated at that run time) and the Letta stateful run used a different generation with the same qids. 39 of 39 question texts differ. Aggregate Δ remains fair (same subject, same battery size, same held-out test design, same judge panels). Per-question pairing is not available. Recommend: add one sentence to §4.3.1 noting that question alignment holds for Hamerton and not for Ebers/Babur, and that aggregate deltas on Ebers/Babur compare representations on distinct held-out batteries of the same subject.

2. **Babur block ceiling claim.** Paper says block saturated against "Letta's 333,000-character per-message API ceiling." Actual block is 335,349 chars (letta_block_duplication_analysis.json). The Letta API limit is plausibly the per-turn ingestion cap, not the cumulative human-block cap. If the per-turn cap is 333k, the cumulative block can exceed it because each turn appends. Recommend: change to "the block approached Letta's per-turn 333,000-character API ceiling" or confirm the ingestion-limit documentation and rephrase to match.

3. **Ebers human block's first paragraph is Letta's initialization boilerplate, never overwritten.** Not in the paper. Worth a footnote if the "self-editing" framing is load-bearing: the agent did not edit out its own placeholder.

---

## 6. Artifacts

All intermediate files under `docs/research/_letta_blocks/`:

- `hamerton_human_block.txt`, `ebers_human_block.txt`, `babur_human_block.txt` — raw final human blocks.
- `compute_paired.py`, `paired_scores.json` — per-question, per-judge scores and aggregate comparison.
- `extract_responses.py`, `response_pairs.txt` — paired response bodies for divergent questions.
- `check_babur_alignment.py`, `check_ebers_hamerton_alignment.py` — question-text alignment audit.
- `archival_scan.py` — C1_letta vs C3_letta per-question swing analysis.
- `archival_pair_extract.py`, `archival_pairs.txt` — example response pairs from archival path.
