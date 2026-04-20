# Supermemory C1 vs C3: Paired Response Analysis

**Question:** When the quantitative score delta between Supermemory-alone (C1) and Supermemory + Behavioral Specification (C3) is near-zero, are the responses *qualitatively* the same, or are they qualitatively different in ways that aggregate scores hide?

**Method:** Within each low-baseline subject (`sunity_devee, ebers, hamerton, fukuzawa, seacole, bernal_diaz, keckley, yung_wing, babur`), pair responses by `question_id` across `C1_supermemory` and `C3_supermemory` from `supermemory_results.json`. Compute per-question mean score across all six judges from `supermemory_judgments_merged.json` (judges: haiku, sonnet, opus, gpt4o, gpt54, gemini_flash). Bucket questions into (a) similar score |Δ| ≤ 0.3, (b) C3 higher, Δ > +0.3, (c) C3 lower, Δ < −0.3. Each subject has 39 held-out questions.

Data script: `scripts/analyze_sm_c1_vs_c3.py`. Raw candidate bundle: `docs/research/_sm_c1_c3_candidates.json`.

## Per-subject distribution of paired deltas

| Subject | C1 mean | C3 mean | Δ | C3 higher (>0.3) | similar (|Δ|≤0.3) | C3 lower (<−0.3) |
|---|---|---|---|---|---|---|
| ebers | 2.01 | 2.21 | **+0.21** | 19 | 10 | 10 |
| hamerton | 2.72 | 2.86 | +0.14 | 18 | 13 | 8 |
| seacole | 2.74 | 2.86 | +0.12 | 14 | 16 | 9 |
| yung_wing | 2.47 | 2.58 | +0.11 | 17 | 8 | 14 |
| babur | 2.03 | 2.08 | +0.05 | 11 | 20 | 8 |
| bernal_diaz | 2.61 | 2.58 | −0.03 | 13 | 13 | 13 |
| fukuzawa | 2.85 | 2.71 | −0.13 | 9 | 14 | 16 |
| sunity_devee | 2.70 | 2.54 | −0.16 | 10 | 14 | 15 |
| keckley | 2.90 | 2.65 | **−0.26** | 10 | 12 | 17 |

The aggregate Supermemory Δ is not a smooth near-zero distribution. It is a *mixture* of large positive and large negative per-question effects that average out. Even the Δ=+0.21 Ebers case hides 10 questions where the spec actively hurt by >0.3 points; even the Δ=−0.26 Keckley case has 10 questions where the spec helped by >0.3.

---

## Bucket A — Similar score, different content/tone

### A1. Ebers Q7 (C1=3.50, C3=3.50, Δ=0.00)

**Question:** *How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?*

**Held-out passage:** *"A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed."*

**C1 (retrieval only):** 317-token answer. Concludes "Ebers would likely view self-sacrifice not as separate from educational success, but as its **foundation**—a necessary commitment that, combined with genuine care for people and institutions, produces lasting prosperity and positive outcomes." Cites father's example at Konigstadt Theater, values of loyalty and blessed toil, endorsement of Froebel.

**C3 (+spec):** ~630-token answer. Makes the same foundational claim but adds: a distinction between *institutions sustained by self-sacrifice* vs *institutions that extract labor without sacrifice*; names predicate A5 (Fortitude Through Suffering) × A10 (Love as Force); adds an internal counterweight ("self-sacrifice can become coercive... the burden can fall unequally on those with fewer resources to bear it").

**Judge behavior:** Scores identical on average (3.50) but the distribution differs. haiku: C1=5 → C3=4 (penalized verbosity). gpt54: C1=2 → C3=4 (rewarded named axioms). Net zero at the mean masks a judge-disagreement widening.

**Observation:** Same core prediction, same factual grounding. C3 adds a typology and a counter-position that is *absent* from C1. The held-out ("built by the hand of God! Implicit devotion...") is an unconditional moral assertion — and C1's unconditional language ("foundation", "necessary") actually matches it more tightly than C3's hedged typology. The spec did not produce a better answer; it produced a more argumentatively elaborated one that different judges scored in opposite directions.

### A2. Keckley Q1 (C1=4.50, C3=4.50, Δ=0.00)

**Question:** *Based on Keckley's demonstrated approach to witnessing grief and emotional distress, how would she likely respond if asked to comfort a family member experiencing acute sorrow?*

**Held-out passage:** *"I bathed Mrs. Lincoln's head with cold water, and soothed the terrible tornado as best I could."*

**C1:** Predicts "active, physical presence and tender care." Names the Mrs. Lincoln episode directly ("laid her hand upon Mrs. Lincoln's hot brow"). Lists: immediate embodied comfort, sustained engagement, emotional attunement, dignified respect.

**C3:** Predicts the same ("presence and physical care rather than words"). Adds a sequence ("First: She would go... Second: She would attend to the body... Third: She would hold the emotional labor visible"), names A7 (family loyalty), A6 (Witness Over Abstraction), P1 (Documentary Witness Reflex), P4 (protective omission). Introduces a new claim not in C1: that Keckley treats acute sorrow as *epistemically* significant, producing a form of knowledge.

**Judge behavior:** All six judges gave identical scores to both responses (5,4,4,5,4,5).

**Observation:** This is the clearest case where the two responses score identically and *both answer the question correctly* — the essential prediction (cool hand on brow, physical presence) is in both. C3 differs only in texture: more commitment language ("Not hesitantly, not after being asked twice"), more predicate scaffolding, one additional interpretive claim. The judges could not (or chose not to) distinguish them. If one believes the spec's added texture matters for downstream use, the identical score hides real qualitative difference. If one does not, the spec is paying output tokens for zero predictive improvement.

### A3. Sunity Devee Q28 (C1=3.00, C3=3.17, Δ=+0.17)

**Question:** *How would the author likely interpret her spouse's final words and actions?*

**Held-out passage:** *"He looked round with such loving eyes just before he breathed his last at all his children, his brother-in-law, and staff; held my hands, calling me 'poor girl'; and after saying a prayer, with a smile he quietly passed away."*

**C1:** Frames interpretation through "deep devotion and spiritual connection," notes her formal address ("Ogo"), cites "the pang of death is happiness compared with waiting to rejoin a beloved husband." Five short sections.

**C3:** Introduces five named interpretive moves — "The Providential Reading," "Moral Vindication Through Sacrifice," "Relational Identity Crystallized," "The Unspoken as Evidence," "Integration with Her Own Sacrifice." Adds: "if he *did not* speak certain things... she would read that silence as equally meaningful." Claims her memory of his words would function "as a kind of scripture."

**Observation:** C1 and C3 agree on the spiritual-providential framing. C3 goes further with an **unsolicited generative layer**: "the absence of certain words would be evidence of spiritual discipline." This is not in the held-out text and is not supported by retrieved facts; it is spec-driven inference. It neither helps nor hurts scoring, but it is qualitatively a *different kind* of answer — more interpretive, more committed, with more epistemic load placed on silences the spec has instructed the model to read.

---

## Bucket B — C3 scored higher, what did the spec add?

### B1. Ebers Q3 (C1=1.17, C3=3.00, Δ=+1.83)

**Question:** *How would Ebers characterize the emotional impact of natural beauty combined with a mentor's persuasive words?*

**Held-out passage:** *"The heart of the young clergyman, tortured by anxious doubts, swelled at the sight of this magnificence, and Froebel, seeing what was passing in his mind, exclaimed: 'Come, comrade, let us have one of our old war-songs.'"*

**C1:** Generic "profoundly transformative" framing, lists "natural beauty as foundational," "mentorship as the catalyst," "emotional depth." Does not capture the *unifying mechanism* — it describes both inputs as separate forces.

**C3:** Opens with a load-bearing shift: "not as two separate forces but as a single formative architecture — where the landscape becomes the medium through which the mentor's words take root." Introduces "Awakening rather than persuasion," "Indelible impression," "Loyalty to the source." The key insight — beauty and words are *fused*, not additive — directly mirrors the held-out's structure (the swelling heart and the war-song come together in one moment).

**Judge behavior:** All six judges scored C3 higher. C1 got unanimous 1s (and one 2); C3 got 2-5.

**Observation:** Here the spec added a *structural* insight the retrieval layer could not supply. Retrieval returned discrete facts about nature, the Steiger, the mother, the loyal atmosphere. The spec carried a theory of formation ("load-bearing structure of adult character") that let the model see these facts as a *single mechanism* rather than a list. This is the strongest case for the spec-as-interpreter thesis in the bucket.

### B2. Keckley Q20 (C1=2.00, C3=3.67, Δ=+1.67)

**Question:** *When Elizabeth learns that family members she cared for are dying, how does she respond to their requests?*

**Held-out passage:** *"Both are now dead, and when the death-film was gathering in the eyes, each called for me and asked to die in my arms."*

**C1:** Retrieval pulled only facts about her mother's refusal to be placed in service with strangers and her feeling of being forgotten. C1 extrapolates cautiously to "protective action and personal responsibility" and concedes "the facts also note that Mr. Garland died... but they don't specify what requests, if any, he made of her during his final illness." C1 effectively says: I don't have evidence for the specific pattern.

**C3:** Predicts "Be present physically. She does not send money or messages; she goes." Adds "compliance with the request, even at great cost." Names A7 (family obligation), C1/P6 (presence and practical care), A5/P6 (grief as restructuring). Gets close to the held-out pattern: dying family members *request her presence and she gives it*.

**Observation:** The retrieved facts underdetermine the answer for C1. The spec contains the pattern — Keckley's axiom of presence-over-words — and this axiom transfers across instances. C3 correctly applies the pattern to a case retrieval did not cover. This is a case for hypothesis (a)-being-**incomplete**: retrieval does not capture this interpretive signal; the spec does.

### B3. Sunity Devee Q35 (C1=2.33, C3=4.33, Δ=+2.00)

**Question:** *Based on the author's account of a son's education, what does she believe was the consequence of following official advice that conflicted with her own judgment?*

**Held-out passage:** *"By his advice I had dear Victor brought back to India and thus all his future career was spoilt as he was sent to the Cadet Corps."*

**C1:** Generic "negative consequences for her child's health and well-being." Does not land on the specific "career was spoilt" reading. Cites a fact about school officials that is only tangentially related.

**C3:** Predicts "harm to the child" and places the moral weight on self-accusation: "she held herself morally responsible for that harm despite the advice coming from authority figures she otherwise respected." This matches the held-out's structure precisely — she is narrating her own misstep, not officials' failure.

**Observation:** The spec's explicit anchor (A2 — Spiritual Integrity Over Social Cost) encodes that she frames her own conscience as the truer guide. That framing is the actual structure of the held-out sentence. Retrieval missed it. Spec captured it. This is a genuine spec-contribution case.

---

## Bucket C — C3 scored lower, what did the spec disrupt?

### C1. Ebers Q34 (C1=3.67, C3=2.00, Δ=−1.67)

**Question:** *When seeking a place of rest and recovery, what kind of environment does Ebers value most highly?*

**Held-out passage:** *"A quieter spot cannot be imagined, for I was the first who sought recreation here. Surrounded by memories of olden days, and absolutely undisturbed, I could create admirably."*

**C1:** Answers plainly: "natural, peaceful environments that offered both beauty and freedom." Four concise points.

**C3:** Adds a theoretical layer: "A8 (Beauty as Evidence)", distinguishes "cultivated setting" from "wilderness for its own sake," adds "moral and physical restoration," "freedom within structure," "the environment itself carries the imprint of thoughtful care in its selection and maintenance."

**Judge behavior:** Every single judge scored C3 lower (2s across the board) vs C1's 3-5 range.

**Observation:** The held-out passage describes something simple — *quiet, undisturbed, memory-laden solitude for creative work*. C1's "peaceful... natural... freedom" lands near this. C3's elaborate "refined... aesthetically presented... cultivated interpenetration of domestic and natural" drifts *away from quietness and toward beauty-as-theory*. The spec over-interpreted and the answer became ornamental. This is evidence for a failure mode: when the question's correct answer is plain, spec-driven theorizing is a Pareto loss.

### C2. Keckley Q21 (C1=3.83, C3=1.50, Δ=−2.33)

**Question:** *How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?*

**Held-out passage:** *"As I did not visit my mother's grave at the time, the Garlands were much surprised, but I offered no explanation. The reason is not difficult to understand."*

**C1:** Admits the retrieved facts don't contain the explanation, but then *productively speculates* from the facts about her mother — avoidance of "disappointed hopes," emotional pain, resignation. Judges rewarded this with 3-5 across the board.

**C3:** *Refuses to answer.* Opens with "I need to be direct: the behavioral specification and retrieved facts provided do not contain Elizabeth Keckley's explanation of a decision not to visit her mother's grave." Cites axioms A2 (Documented Dignity) and A1 (Intimate Authority) to justify the refusal: "I should not fabricate interior motive or supply explanations that aren't grounded in her own documented account." Ends by asking the user for the source passage.

**Judge behavior:** Catastrophic. 5 of 6 judges gave 1 or 2. Even opus gave only 3.

**Observation:** This is the most striking case in the entire analysis. The spec's epistemic humility axioms — designed to prevent fabrication — induced a refusal the judges treated as failure. The C1 answer was a careful speculation labeled as such. The C3 answer was a correct but unhelpful disclaimer. **The spec did not produce a worse prediction; it produced a refusal to predict.** For an evaluation framework that rewards content match with the held-out passage, epistemic honesty is indistinguishable from ignorance. This surfaces a real cost of specification-induced humility: benchmarks that score on predictive content will penalize it.

### C3. Sunity Devee Q11 (C1=4.00, C3=2.17, Δ=−1.83)

**Question:** *Based on the author's expressed values about parental involvement and family separation, how would she likely react to being prevented from visiting her child abroad during their education?*

**Held-out passage:** *"I think it was most unkind the way in which the State officials prevented me from going to England to be with my boy. Every time the question was raised, they made the excuse of money difficulties, which I know for certain did not exist."*

**C1:** Predicts "significant distress and resistance" and "unjust constraint on her maternal rights." Directly matches the held-out's *direct accusatory* tone.

**C3:** Predicts the opposite posture at the surface level: "she would not express this grief as protest or complaint... Perform acceptance while experiencing deprivation... **What She Would NOT Do: Directly challenge the authority preventing the visit (A4)... Frame it as injustice (A1 + A4).**" The spec has encoded a "hierarchical deference" axiom (A4) and a "tension absorbed, not expressed" predicate (P3). These are the *wrong* axioms for this specific incident: she *did* directly call it "most unkind," *did* frame the money excuse as a lie.

**Judge behavior:** Every judge scored C3 lower. C1 got 3-5s across the board; C3 got 2s and one 3.

**Observation:** This is the failure mode the Keckley case hints at, generalized. The spec contains an axiom that is *true on average* (Sunity Devee's cultural context encodes hierarchical deference) but *false for this instance* (she explicitly breaks that deference). Retrieval, unconstrained by an overgeneralized axiom, landed closer to the held-out. This is evidence for a real risk of behavioral specifications: they encode defaults that can override counter-evidence in specific moments.

---

## Systematic patterns

### Pattern 1 — The spec makes responses *more committed, more structured, longer, and more theoretically scaffolded*.

Across every paired example, C3 is longer (typically 2-3x), uses more headings, names axioms/predicates, and makes commitments ("She would go. Not hesitantly.") where C1 hedges ("Elizabeth would likely respond..."). This is invariant across buckets — even when the underlying prediction is identical (Keckley Q1), C3 is rhetorically bolder.

### Pattern 2 — The spec adds *typologies and structural claims* that retrieval alone cannot produce.

Ebers Q3 (beauty + mentor as "single formative architecture"), Ebers Q7 (institutions-sustained-by-sacrifice vs institutions-that-extract-labor), Sunity Q28 (silence-as-evidence-of-spiritual-discipline), Keckley Q20 (grief-as-permanent-restructuring). These are interpretive moves that come from the spec's predicates, not from retrieved facts. Sometimes they hit the held-out (Q3, Q20); sometimes they drift past it (Q7).

### Pattern 3 — The spec introduces three distinct *failure modes* that retrieval alone avoids.

- **Over-theorization on simple questions** (Ebers Q34). When the held-out is plain, spec-driven elaboration is a Pareto loss.
- **Spec-induced refusals** (Keckley Q21). Axioms designed to prevent fabrication also prevent helpful speculation and are penalized by content-match judges.
- **Default-axiom errors on counter-example moments** (Sunity Q11). Encoded defaults (A4 hierarchical deference) override correct context-specific inference when the subject departs from their own default.

### Pattern 4 — Score-identical pairs are rarely content-identical.

Even at |Δ| ≈ 0 (Ebers Q7, Keckley Q1, Sunity Q28), C3 introduces unsolicited interpretive layers that C1 does not — typologies, silences-as-evidence readings, axiom labels, commitment verbs. Aggregate parity masks real qualitative divergence in *what kind of answer* is being given.

### Pattern 5 — Score-similar pairs often mask strong judge-level disagreement.

Across 120 score-similar pairs (|Δ| ≤ 0.3) over the 9 subjects:

- **41.7% (50/120) have at least one judge scoring C3 higher AND at least one judge scoring C3 lower.** The aggregate parity is an artifact of judge cancellation, not of judge consensus.
- **41.7% have a per-judge delta range ≥ 2** (max-judge-delta minus min-judge-delta on the same question).
- **10% have a range ≥ 3**; two pairs hit range 5 (Keckley Q4: gpt54 dropped 2, haiku rose 3).

On Ebers Q7 (same mean 3.50), gpt54 shifts C1=2 → C3=4 (rewards axioms), while haiku shifts C1=5 → C3=4 (penalizes verbosity). In a production deployment where a single evaluator model would score, the observed score could flip sign depending on which judge was used. Validation script: `scripts/check_judge_variance.py`.

### Judge rubric (for interpreting the above)

All six judges use the same rubric (`scripts/run_judge_evaluation.py`):
- 5 = Predicts specific outcome
- 4 = General direction correct
- 3 = Right domain, wrong outcome
- 2 = Wrong prediction
- **1 = Refuses or off-base**

This is content-match-against-held-out-passage scoring. The rubric explicitly collapses "epistemically honest refusal" with "off-base guess" into a single 1. This is the mechanism behind the Keckley Q21 penalty.

---

## Honest read on the hypotheses

Both (a) and (b) are supported, but asymmetrically.

**Hypothesis (a) — Supermemory's retrieval captures most of the interpretive signal implicitly — is partially supported.** Retrieval did deliver the correct prediction on Keckley Q1, did deliver the correct moral framing on Ebers Q7, and on the whole kept C1 within 0.2-0.3 points of C3 on average. For Supermemory specifically, the retrieval layer is strong enough that *on many questions, the spec adds elaboration without adding predictive accuracy*.

**Hypothesis (b) — C3 responses are qualitatively different even at score parity — is strongly supported.** Every score-parity pair shows the spec producing more committed, more structured, more theorized answers. If downstream use (agentic delegation, high-stakes advice, voice persistence) cares about these qualities, the aggregate score hides real differences.

**But neither hypothesis is the full picture.** The paired analysis surfaces a third dynamic that the original framing missed: **the near-zero aggregate Δ is a sum of large positive and large negative per-question effects**. On Ebers, the spec helps on 19 questions and hurts on 10. On Keckley, it helps on 10 and hurts on 17. The aggregate parity is not a uniform "spec is neutral" effect — it is a *redistribution*: the spec adds interpretive generalization (Bucket B) while simultaneously introducing over-theorization, refusals, and default-axiom errors (Bucket C). These cancel on average. The policy implication is that specifications have differential value by question type, and a question-routing layer (spec-use on interpretation-heavy questions, retrieval-alone on literal-recall questions) would likely outperform both conditions on low-baseline subjects.

The most striking single example — **Keckley Q21, where the spec induced a refusal to answer that all judges penalized** — is the one most worth reproducing in the paper. It is a clean demonstration that the spec's epistemic humility axioms do real work the retrieval layer does not, at real cost to a predictive benchmark. This is not a bug to be fixed; it is a feature of specification-based systems that benchmarks must be designed to score honestly.
