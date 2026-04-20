# Mem0 / Letta / Zep: C1 vs C3 Paired Response Analysis

**Question:** When the quantitative aggregate score delta between a commercial memory system alone (C1) and the same system + Behavioral Specification (C3) looks modest, are the per-question effects uniformly modest, or is the aggregate a *mixture* of large positive and large negative per-question effects — as the Supermemory paired analysis showed? Do the three systems interact differently with the specification?

**Method:** Mirrors `docs/research/supermemory_c1_vs_c3_paired_analysis.md`. For a hand-picked spread of 4 low-baseline subjects per system (including `ebers` for cross-system comparability, plus the system's strongest-delta subject, weakest-delta subject, and one in the middle), pair responses by `question_id` across `C1_<sys>` and `C3_<sys>` in `<sys>_results.json`. Compute per-question mean score across all six judges from `<sys>_judgments_merged.json` (judges: haiku, sonnet, opus, gpt4o, gpt54, gemini_flash). Bucket into (a) similar |Δ| ≤ 0.3, (b) C3 higher, Δ > +0.3, (c) C3 lower, Δ < −0.3. Each subject has 39 held-out questions.

Data script: `scripts/analyze_mlz_c1_vs_c3.py`. Raw candidate bundle: `docs/research/_mlz_c1_c3_candidates.json`. Ad-hoc probes: `scripts/_probe_keckley_q21.py`, `scripts/_probe_top_examples.py`, `scripts/_probe_retrieval_styles.py`.

---

## 1. Per-subject distribution of paired deltas

Columns: C1 mean (over 39 Qs), C3 mean, aggregate Δ, count of Qs where C3 > C1 by >0.3, count similar |Δ|≤0.3, count where C3 < C1 by >0.3, and large-swing counts where |Δ| > 1.0.

### 1.1 Mem0

| Subject | C1 mean | C3 mean | Δ | C3 higher (>0.3) | similar | C3 lower (<−0.3) | C3 big-win (>1.0) | C3 big-loss (<−1.0) |
|---|---|---|---|---|---|---|---|---|
| ebers | 2.03 | 2.26 | +0.22 | 18 | 15 | 6 | 4 | 2 |
| yung_wing | 2.16 | 2.51 | **+0.35** | 21 | 6 | 12 | 7 | 1 |
| sunity_devee | 2.46 | 2.38 | −0.08 | 15 | 10 | 14 | 1 | 5 |
| keckley | 2.64 | 2.63 | −0.01 | 14 | 9 | 16 | 1 | 2 |

### 1.2 Letta (archival)

| Subject | C1 mean | C3 mean | Δ | C3 higher (>0.3) | similar | C3 lower (<−0.3) | C3 big-win (>1.0) | C3 big-loss (<−1.0) |
|---|---|---|---|---|---|---|---|---|
| ebers | 1.91 | 2.22 | +0.31 | 19 | 13 | 7 | 8 | 2 |
| hamerton | 2.35 | 2.81 | **+0.46** | 21 | 10 | 8 | 10 | 2 |
| sunity_devee | 2.45 | 2.44 | −0.01 | 13 | 11 | 15 | 3 | 4 |
| keckley | 2.70 | 2.70 | 0.00 | 11 | 13 | 15 | 3 | 2 |

### 1.3 Zep

| Subject | C1 mean | C3 mean | Δ | C3 higher (>0.3) | similar | C3 lower (<−0.3) | C3 big-win (>1.0) | C3 big-loss (<−1.0) |
|---|---|---|---|---|---|---|---|---|
| ebers | 1.76 | 2.16 | +0.40 | 24 | 8 | 7 | 6 | 1 |
| seacole | 2.27 | 2.79 | **+0.52** | 24 | 7 | 8 | 9 | 0 |
| bernal_diaz | 2.44 | 2.50 | +0.06 | 14 | 12 | 13 | 1 | 1 |
| keckley | 2.49 | 2.59 | +0.10 | 16 | 11 | 12 | 5 | 3 |

### 1.4 Headline: aggregate Δ is a redistribution, not a uniform lift, in all three systems

On every subject studied — including subjects whose aggregate Δ is near zero — the paired distribution shows simultaneous large positive and large negative per-question swings. Even on the strong-win cases (Zep/seacole +0.52 aggregate) 8/39 questions *still* lose by >0.3. On the near-zero cases (mem0/keckley Δ=−0.01) the 39 questions split 14/9/16 across the three buckets — the aggregate flatness is canceled-out swings, not a uniform neutrality. This matches the Supermemory finding qualitatively.

However, the **asymmetry** differs across systems. Zep has the cleanest positive profile: on its strong subjects (ebers, seacole) C3 wins 24 of 39 and has essentially no catastrophic big-losses (ebers: 1 big-loss; seacole: 0). Letta has a similar win-tilt on strong subjects but more big-losses when things go wrong. Mem0 is the most mixed: on yung_wing the spec wins 21 of 39 *and* loses 12 of 39 — aggregate +0.35, but with 7 big-wins AND 1 big-loss co-existing.

---

## 2. System-specific retrieval characteristics

Before reading the paired examples it helps to know what each memory system actually returns — the generation model sees very different substrate across the three.

**Mem0.** Returns a flat list of ~10 atomic fact statements, each a complete sentence (e.g., *"Georg Ebers does not accept Strauss' religious views."*). Style is close to what the extraction pipeline produced upstream. Occasional semantic-mismatch facts appear (e.g., *"Ebers' aunt Henriette had jealousy that almost bordered on insanity"* returned for a question about institution management). Model has to filter.

**Letta (archival).** Returns 10 facts per retrieval, but with heavy duplication — across the four subjects studied, the dedup ratio is **0.34–0.47** (i.e., only 3–5 *unique* facts in a top-10 retrieval), and the most-repeated fact appears on average **2.9–4.5 times** in a single top-10 (verified in `scripts/_verify_claims.py`). E.g., *"Friedrich Froebel... told Georg that he would wander far through the world based on his wide-set teeth"* surfaces 3-4x in the same result list. The model effectively sees a handful of unique facts with high visual prominence, and often anchors heavily on one or two high-frequency facts. For comparison, Mem0's dedup ratio is 1.00 on the same subjects.

**Zep (temporal graph).** Returns a list of 7 items, but the items are stringified Python reprs of the Graphiti SDK response — the list is actually `[("communities", None), ("context", None), ("edges", [EntityEdge(...), EntityEdge(...), ...]), ("episodes", []), ("nodes", []), ("sagas", None)]`. Only the `edges` element contains substantive facts. The edges carry edge-type labels (`INHERITED_INTEREST_FROM`, `SCREAMED_TO_ALERT`, `USED_FOR_RUBBING`, `PERCEIVED_NO_FLAWS_IN`) and the `fact` attribute on each edge is what gets parsed into prose by the generation model. This is fundamentally a more verbose, more relational substrate — but it is *not* time-anchored retrieval in the paired responses (no question-answering use of `valid_at` / `expired_at`), so the "temporal graph" value proposition is not operationalized in this study's query pattern. The generation model extracts ~8-12 edge facts from the blob and reasons from them.

These three substrates produce qualitatively different C1 responses, which then sets the counterfactual against which C3 is scored.

---

## 3. Paired examples

For each system: one clear spec-wins case, one clear spec-loses case, and one neutral/illustrative case. Pairs drawn from the candidate bundle.

### 3.1 Mem0

#### M-WIN. Ebers Q11 — "How does Ebers respond to poor institutional management?"

**Held-out passage:** *"I had come hither full of beautiful ideals and animated by the best intentions; but the very first day made me suspect how many obstacles I should encounter."*

**C1 (1.83 mean, scores 2,1,2,3,2,1):** Produces a generic "patience and fortitude" answer built from miscellaneous retrieved facts (Ebers "demonstrated fortitude in adversity"; Frau Marx the near-blind cook). Explicitly concedes the facts "don't directly address his response to institutional management, so this assessment is based on extrapolation from his broader character traits."

**C3 (3.50 mean, scores 4,2,3,3,4,5):** Delivers a load-bearing structural claim: Ebers responds by *"instinctively testing the institution's stated ideals against eyewitness reality, exposing the gap between what is professed and what actually happens."* This is close to the held-out's "beautiful ideals" / "first day made me suspect how many obstacles" structure. The spec supplies the ideal-vs-reality axiom; retrieval alone offered only Patience and Fortitude.

**Observation:** This is the archetypal "spec supplies the interpretive pattern retrieval can't" case — analogous to Supermemory's Ebers Q3. The Mem0 atomic-fact retrieval gave the model correct biographical material but no *pattern* for how Ebers processes institutional failure. The spec carried that pattern.

#### M-LOSS. Ebers Q1 — "How would Ebers respond to a persuasive appeal centered on spiritual duty and service?"

**Held-out passage:** *"Like the apostle, I would fain proclaim the gospel to all men according to the best of my powers, in order to bring them into close communion with the Redeemer."* (Strong, unconditional, enthusiastic.)

**C1 (3.83 mean):** Predicts "positively and deeply" — response would resonate. Cites "early felt a desire to share with those he loved whatever charmed him" and his mother's service model. Matches the held-out's unconditional tone.

**C3 (2.50 mean):** Predicts "genuine receptivity, but only if certain conditions are met — and the conditions matter more than the appeal itself." Builds a conditions-framework: must be grounded in lived example, must flow from love not obligation, must honor family commitments, activates resistance to coercive framing. This is a *hedged* prediction where the held-out is a *direct enthusiastic affirmation*.

**Observation:** The "Sunity Q11"-style default-axiom failure from the Supermemory analysis reproduces here. The spec contains a "resistance to coercion / love-not-duty" axiom that is *correct on average* for Ebers' biographical data but *overfires on this specific unconditional-evangelical moment*. C1 stayed shallow, C3 over-conditionalized.

#### M-NEUTRAL. Yung Wing Q35 — similar score, different content

**C1 / C3 both 3.33, Δ=0.00.** C1 predicts "humility and principled correction." C3 predicts multi-register response "operating across several registers simultaneously, and the tension between them is instructive." Same core prediction, different texture — C3 adds typology (modest-public-correction vs internal-record-setting) that is absent from C1. Mirrors Supermemory's "A1-A3 similar-content-different-texture" pattern.

### 3.2 Letta

#### L-WIN. Ebers Q38 — "How does Ebers characterize intellectual resilience of someone with strong faith facing opposing views?"

**Held-out passage:** *"Her soul was like a polished plate of metal on which a picture is etched. This, her belief, remained uninjured. Whatever else might be reflected from the mirror-like surface soon vanished, leaving no trace."*

**C1 (1.00 mean — all six judges scored 1):** Admits it "cannot find a direct characterization from Ebers." Lists generic household-discussion facts and Ebers' own fortitude. Concludes: "the retrieved information doesn't explicitly state his theoretical characterization." The duplication pattern (same fact returned 3x about rejecting Strauss) didn't help the model — it just made one fact loom larger without adding interpretive frame.

**C3 (3.17 mean):** Builds the framework directly: resilience is "not imperviousness to opposing views but the capacity to engage them seriously while remaining rooted in core conviction." Then: "A person with strong faith, exposed to opposing views, would be resilient to the degree that their faith had been lived and transmitted through concrete example and relational depth, not merely asserted as doctrine." This reaches for a mirror/polished-plate-style unchangeable-core structure that tracks the held-out's metaphor.

**Observation:** Clear spec-driven interpretive recovery. Letta's retrieval was semantically on-target but lacked any axiom the model could use to produce a *theoretical characterization* — which is exactly what the question demanded.

#### L-LOSS. Ebers Q17 — "When given the opportunity to spend time in natural settings, what is Ebers's typical behavior?"

**C1 (3.50 mean):** Direct answer — "Active Engagement: Ebers had an inborn love of travel, suggesting he actively sought natural environments; immersive appreciation; contemplative reverence."

**C3 (1.83 mean):** Spirals into epistemic humility: "Based on the retrieved facts, I can establish what is directly documented... What we know with certainty: Ebers spent a large portion of his boyhood amid surroundings that led back to Nature..." Becomes a meditation on the *limits* of what the data supports rather than predicting behavior. All six judges scored the hedging response at 2-3.

**Observation:** This is a clean reproduction of the Supermemory *Keckley Q21 pattern* — the spec's epistemic-humility axioms induce a de-facto refusal to predict on a question where direct prediction was available. The spec's axiom 8 (Beauty as Evidence) and axiom about fidelity to documented evidence combined to make the model retreat from inference. On a content-match rubric this is a 1.67-point Pareto loss.

#### L-NEUTRAL. Ebers Q37 — similar score, different content

C1=3.33, C3=3.50, Δ=+0.17. Both answer "empathy and resonance." C3 adds "not as sentiment, but as evidence of something foundational" — spec-driven interpretive layer on top of the same prediction. Same pattern as Mem0-NEUTRAL and Supermemory-A1.

### 3.3 Zep

#### Z-WIN. Seacole Q2 — "How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?" (Δ = +4.00; verified as the largest single-question positive swing across all 12 system-subject pairs studied. The next four largest positive swings are also Zep (Keckley Q20, +2.83; Bernal Diaz Q16, +2.83) and Letta (Hamerton Q33, +2.67; Sunity Devee Q10, +2.33).)

**Held-out passage:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*

**C1 (1.00 mean — unanimous 1s):** "Based on the retrieved facts about Mary Seacole, I don't have specific information about how she typically responds when a delirious patient mistakes her for a family member. The available data focuses on her medical practices and actions, such as: rubbing patients with warm oil, camphor, and spirits of wine..." Complete failure to predict.

**C3 (5.00 mean — unanimous 5s):** "She would not correct the misidentification." Cites A4 (Proximate Obligation), A8 (Sympathetic Realism). Then: *"The obligation to comfort the vulnerable takes precedence over the obligation to be accurately named. Her response would be to lean into the comfort the patient is seeking, not to withdraw it. She would maintain physical contact — hand-holding, gentle touch... She would speak reassuringly in whatever register the patient expects (familial, tender, authoritative). She would not narrate the correction."* Directly predicts the held-out's "could not undeceive him / touch of a woman's hand soothed his dying hour" mechanism.

**Observation:** The single largest paired swing in this analysis. Zep's retrieval returned relational edges (`USED_FOR_RUBBING`, `SCREAMED_TO_ALERT`, `PRACTICED_ON`) that were biographically correct but semantically orthogonal to the question of misidentified-patient response. Without the spec, the model had no bridge from Seacole's documented medical practice to her social-psychological behavior at bedside. The spec carries exactly the "proximate obligation overrides precision" pattern the question needs.

#### Z-LOSS. Ebers Q18 — "How does Ebers describe his capacity for finding joy and maintaining his disposition during his school years?"

**Held-out passage:** *"my natural cheerfulness ruled my whole nature."* (Simple, direct, one-line.)

**C1 (3.67 mean):** Direct answer — "notably positive and uncritical disposition... idealization of mentors... nostalgia and contentment... optimistic and appreciative disposition." Matches the held-out's plainness.

**C3 (2.33 mean):** "The retrieved facts about Ebers himself are sparse and fragmentary — mostly edges documenting which schools he attended... They tell us he studied by tallow-dips, numbered those years among the fairest. But the facts do not tell us *how* he maintained joy or what his disposition was like... I cannot ground this in his own words about his disposition without speculating beyond what the evidence supports." Ends by asking the user for source passages.

**Observation:** Reproduces the Supermemory *Keckley Q21 refusal* almost verbatim, but in the Zep context — when Zep's retrieval substrate is edge-facts (not prose), the spec's documented-dignity axioms seem especially liable to induce "I cannot ground this" refusals. The held-out is *one line*, answerable from "numbered those years among the fairest" + inference. C1 made the inference and scored 3.67. C3 refused and scored 2.33.

#### Z-NEUTRAL. Seacole Q15 — similar, both ≥ 2.5

Both around 3.0. C1 asserts "very likely accept and enthusiastically provide her medical expertise." C3 qualifies with "accept and act immediately, but the manner of her acceptance would depend on whether the request came with institutional legitimacy." Same prediction, C3 adds conditions.

---

## 4. The Keckley Q21 refusal check — does it reproduce?

In the Supermemory analysis, Keckley Q21 ("How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?") was the single most striking case: the spec induced a direct "I need to be direct: the facts do not contain..." refusal that all six judges penalized. I probed the same question across the three systems:

| System | C1 mean | C1 content | C3 mean | C3 content | Δ |
|---|---|---|---|---|---|
| Supermemory (prior) | 3.83 | Productive speculation | 1.50 | Explicit refusal + axiom citation | **−2.33** |
| Mem0 | 2.00 | Hedged "no information, here are related facts" | 1.50 | Explicit "I must be direct: the retrieved facts do not contain..." | −0.50 |
| Letta | 1.33 | Explicit "no information about... decision" | 2.33 | Refuses *and* provides spec-grounded analysis | **+1.00** |
| Zep | 1.83 | "No information... focuses on..." | 1.33 | Explicit "I need to be direct: the retrieved facts do not contain..." | −0.50 |

**Finding:** The C3 refusal pattern reproduces in all three systems. *But the penalty size depends on the C1 counterfactual.* When the C1 response is already a hedged non-answer (Mem0, Zep), the spec-driven refusal only costs ~0.5 points. When the C1 is a *stronger* non-answer (Letta, more candid but with no interpretive overlay), the C3's spec-justified analysis actually scored higher (+1.00). Supermemory is the outlier because its retrieval was strong enough to *produce* a productive speculation in C1 (3.83), and the spec's refusal then costs the full 2.33 points by comparison.

This says something useful: **the cost of spec-induced epistemic humility is a function of how well the unconditioned retrieval could have answered the question**. Strong retrievers pay a larger refusal tax.

---

## 5. System-specific findings

### 5.1 Mem0 — mixed, no single dominant dynamic

Mem0's yung_wing (+0.35 aggregate) and ebers (+0.22) profiles look similar to Supermemory's — lots of per-question variance, modest aggregate lift, both wins and losses. On keckley/sunity_devee (aggregate near-zero) the distribution is 14-16 on each side with 1-5 big losses. The Q1 Ebers case (spec-over-conditionalizes an unconditional-evangelical response) is the clearest system-specific fingerprint — Mem0's sentence-style atomic retrieval gives the model an *accurate* unconditional base that the spec then over-qualifies. Closest cousin to Supermemory's pattern.

### 5.2 Letta — duplication in retrieval amplifies spec dependency

Letta's retrieval frequently returns the same fact 2-3x in the top-10. When the duplicate fact is on-topic, that's fine. When it isn't, the model has *fewer* unique bases to reason from, which makes C1 more likely to stall into "cannot find a direct characterization" mode. Letta's C1 is the lowest of the three systems on ebers (1.91) and keckley (2.70 — tied with others). Because Letta's C1 is often *already* a hedged non-answer, Letta shows the **largest benefit from spec addition** at the aggregate level for hamerton (+0.47), rousseau (+0.60 per the broader analysis table) — the spec is filling a gap Letta's retrieval creates via duplication. But when C3 *also* produces a refusal-style response (Ebers Q17, Q18), the loss is steep: the spec fails to rescue exactly the questions where retrieval has already partially failed.

**Letta-specific finding:** Duplicate retrieval + spec-induced humility is a failure-mode multiplier. Both dynamics compress the response toward "I cannot ground this," and when they co-occur the loss is large.

### 5.3 Zep — cleanest positive profile *and* the largest single win, driven by retrieval substrate quality

Zep shows the fewest big-losses across the four subjects studied (ebers 1, seacole 0, bernal_diaz 1, keckley 3). The Seacole Q2 +4.00 swing is the largest single-question paired delta seen in either this analysis or the Supermemory one. Mechanically: Zep's retrieval substrate is relational edge-facts (`USED_FOR_RUBBING`, `HOLDS_PREJUDICE_AGAINST`, `INHERITED_INTEREST_FROM`) that are *biographically accurate but interpretively thin*. When a question asks about the subject's *behavior pattern* (not a documented event), retrieval alone cannot produce the answer — see Seacole Q2, where Zep retrieval surfaced edges about rubbing patients with warm oil but nothing about Mary's response to delirium. The spec carries the behavioral axioms directly and the model grafts them onto Zep's relational skeleton, yielding the largest observed swings.

**Zep-specific finding:** On low-baseline subjects Zep's retrieval substrate is *relationally correct but behaviorally empty*. The spec is doing almost all of the interpretive work. This is why Zep has the cleanest positive aggregate profile on strong subjects but does NOT have a clean temporal-graph story — no observed question in this analysis used `valid_at`/`expired_at` to privilege recency, and the retrieval edges are returned as an unstructured blob. The "temporal graph" value proposition is not operationalized in this study's question set.

**There is not a distinctive Zep-style "time-anchored fact surfacing" pattern in the paired responses.** The observed wins are all behavioral-axiom-driven, not temporal.

### 5.4 Keckley Q21-style refusal pattern — reproduces everywhere, penalty depends on C1 strength

The specification's documented-dignity / "do not fabricate interior motive" axioms induce refusal-phrased responses across all four memory systems studied (Supermemory, Mem0, Letta, Zep) on the same question. The penalty size is inversely proportional to how well C1's retrieval could answer: Supermemory penalized −2.33 (strong C1 counterfactual), Letta *gained* +1.00 (weak C1 counterfactual — the spec's humility at least added structure). This is not a system-specific pattern — it is a specification-level pattern that interacts with retrieval strength.

### 5.5 Over-theorization on simple questions — reproduces in Letta and Zep, less clearly in Mem0

Letta Ebers Q17, Zep Ebers Q18 both show the spec turning a simple held-out (one-line affirmations of love of nature / natural cheerfulness) into multi-paragraph meditations on evidentiary limits. Same failure mode Supermemory Ebers Q34 documented. Mem0 Ebers Q1 is a variant — over-conditionalization rather than over-humility, but the same "spec adds scaffolding the held-out doesn't need" root cause.

---

## 6. Honest read

**Three observations hold across all three systems:**

1. **Aggregate deltas are mixtures of large positive and large negative per-question effects.** Even when aggregate Δ is near-zero (keckley, sunity_devee), per-question swings are large on both sides. This reproduces the Supermemory finding. The aggregate "memory system + spec ≈ memory system alone" framing is a genuine statistical artifact that hides real redistribution.

2. **The spec's three documented failure modes (refusal, over-theorization, default-axiom errors) reproduce across all three systems.** These are specification-level dynamics, not system-specific ones. Refusals are universally penalized by content-match rubrics; the size of the penalty depends on how well the retrieval counterfactual could have answered.

3. **The spec's interpretive contribution is largest where retrieval is behaviorally thinnest.** Zep's relational-edge substrate is the thinnest behaviorally, which is why Zep has the largest single observed paired win (Seacole Q2 +4.00) and the cleanest positive profile. Mem0's atomic-sentence substrate is denser, so the spec's value-add is smaller and more mixed. Letta sits in between but is handicapped by fact-duplication.

**One thing we thought might hold but didn't:** there is no evidence in this paired analysis of Zep's "temporal graph surfacing time-anchored facts" — none of the observed wins trace to a time-anchored retrieval. Zep wins when the spec fills in behavioral inference, not when the graph produces recency-weighted facts. This should calibrate any paper claim that frames Zep's graph temporality as central to its performance profile.

**What this implies for the paper's framing:** The "spec as interpretive primitive on top of retrieval" story survives this analysis, but the story has three distinct mechanisms that should be separately named:

- Pattern supply (Mem0 Q11 Ebers): retrieval has facts, spec supplies the pattern that makes the facts answerable.
- Interpretive recovery (Letta Q38 Ebers, Zep Q2 Seacole): retrieval is behaviorally orthogonal, spec bridges to the answer.
- Structural refusal (Q21 Keckley universally, Q17/Q18 Ebers on Letta/Zep): spec's humility axioms produce correct-but-unhelpful refusals that content-match rubrics punish.

A question-routing layer (spec-on for interpretation-heavy questions, spec-off for simple-recall questions) would plausibly outperform both C1 and C3 on low-baseline subjects across all three systems.
