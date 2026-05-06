# §4.6 Review Payload — Beyond Recall

## Context for the reviewer

This is **§4.6 Interpretation vs. Recall** of a research paper titled *"Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization."*

The paper studies whether a compact behavioral specification can improve AI prediction of how a specific person would respond in novel situations, layered on top of commercial memory systems (Mem0, Letta, Zep, Supermemory) and an open-source retrieval substrate (Base Layer).

**Where §4.6 sits in the paper:**
- §4.4 reports aggregate numbers per memory system (Δ_spec per system, sample sizes, effect sizes).
- §4.5 reports robustness and sensitivity checks (Tier 2 cross-provider response models, 5-judge vs 7-judge panels, what the robustness checks do *not* address).
- **§4.6 is the per-question mixture analysis.** It is where the paper looks inside the aggregates from §4.4 and explains, at the per-question level, what mechanisms produce them — improvements from pattern supply, regressions from over-theorization, regressions from specification-induced refusal on questions the held-out text cannot be answered from without fabrication.
- §4.7 discusses architectural convergence with Letta's stateful-agent path (not part of this review).

Key terms used in §4.6:
- **C1** = retrieval alone (memory system, no specification).
- **C3** = retrieval + specification (same memory system, with the behavioral specification layered in).
- **Δ (C3 − C1)** = per-question or aggregate delta introduced by the specification.
- **Δ_spec** = the aggregate specification delta for a system.
- **Held-out passage** = the actual passage by the subject that the model is trying to predict; it is removed from the training half of the corpus.
- **5-judge primary** vs **6-judge** vs **7-judge panel** = the LLM-judge panels used to score predictions against held-out text (§3 and §4.5 cover the methodology).

---

## §4.6 text (verbatim from `beyond_recall_v8_draft.md`)

### 4.6 Interpretation vs. Recall

§4.4's Supermemory section showed that the near-zero aggregate Δ_spec on Supermemory is not the specification doing nothing. The specification produces large improvements on some questions and large regressions on others, with roughly the same magnitude on each side; the number of regressions is slightly higher than the number of improvements, which is what produces the small negative aggregate. §4.6 documents that this pattern is not Supermemory-specific. Every memory system in the study shows the same per-question distribution: improvements and regressions of similar magnitude, with only the balance of counts shifting by system. The three mechanisms identified on Supermemory (the specification supplies a pattern retrieval cannot, the specification over-theorizes a question retrieval already answered plainly, the specification induces a refusal the content-match rubric penalizes) reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate. The single cleanest cross-substrate replication in the study is a spec-induced refusal on Keckley Q21 that produces an identical −2.33 per-question Δ on both Supermemory and Base Layer, despite the two systems using entirely different retrieval substrates.

---

**Per-subject paired-delta distributions reproduce the mixture on every system.**

Across a spread of low-baseline subjects per system, the aggregate spec-delta on every subject studied is a sum of wins and losses at the question level, not a uniform lift. Selected representative cases from the per-system paired analyses:

| System | Subject | C1 mean | C3 mean | Aggregate Δ | C3 wins (Δ > 0.3) | C3 losses (Δ < −0.3) | Big wins (Δ > 1.0) | Big losses (Δ < −1.0) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Mem0 | Yung Wing | 2.16 | 2.51 | **+0.35** | 21 | 12 | 7 | 1 |
| Mem0 | Keckley | 2.64 | 2.63 | −0.01 | 14 | 16 | 1 | 2 |
| Letta (archival) | Hamerton | 2.35 | 2.81 | **+0.46** | 21 | 8 | 10 | 2 |
| Letta (archival) | Keckley | 2.70 | 2.70 | 0.00 | 11 | 15 | 3 | 2 |
| Zep | Seacole | 2.27 | 2.79 | **+0.52** | 24 | 8 | 9 | 0 |
| Zep | Keckley | 2.49 | 2.59 | +0.10 | 16 | 12 | 5 | 3 |
| Base Layer | Yung Wing | 2.23 | 2.56 | **+0.33** | 22 | 10 | 7 | 2 |
| Base Layer | Keckley | 2.44 | 2.44 | −0.01 | 18 | 13 | 3 | 5 |
| Supermemory | 13-subject aggregate | 2.65 | 2.60 | −0.05 | see §4.4 | see §4.4 | 37 / 516 | 52 / 516 |

Every row is a mixture. Zep's best case (Seacole Δ +0.52, the strongest clean profile in the paired analyses) still has 8 questions where the spec hurts by >0.3 points. The near-zero Mem0 Keckley row (Δ −0.01) resolves into 14 wins + 16 losses at the per-question level, not 39 small effects. Across every system, aggregate direction tracks the balance of wins and losses, not a uniform lift or drop.

*Note on judge panel.* The per-question counts in this table use a 6-judge mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash) from the published paired analyses; the 5-judge primary panel gives qualitatively the same per-question distribution. The aggregate Δ values in this column are the same numbers the 5-judge primary recompute produces within rounding (see `docs/research/recompute_5judge_primary.md` for cross-check). The mixture pattern is not judge-panel-specific.

---

**The three mechanisms from §4.4 reproduce across all five memory systems.**

The three mechanisms identified on Supermemory in §4.4 (Pattern 1 pattern supply, Pattern 2 over-theorization, Pattern 3 structural refusal) appear on every memory system in the paired analyses, with the balance shifting by system. Representative cross-system examples:

- **Pattern supply on Mem0 (Ebers Q11, Δ +1.67).** C1 used the retrieved biographical facts to produce "patience and fortitude" as a generic character prediction (mean 1.83). C3 supplied the ideal-vs-reality axiom directly and predicted Ebers' specific institutional-disillusionment pattern (mean 3.50), matching the held-out *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."* The Mem0 retrieval had the biography; the specification had the pattern for how Ebers processes institutional failure.
- **Over-theorization on Base Layer (Yung Wing Q31, Δ −1.33).** C1 produced a plain correct prediction: "walked on air, gratitude." C3 elaborated a theory of "gratitude as epistemology" in which the emotional register "holds multiple registers simultaneously rather than collapsing into simple triumph." The held-out is *"walked on air, and he worshipped God."* Same mechanism as §4.4 Example 2 (Yung Wing Q5 on Supermemory): specification pulled the answer toward interpretive depth where shallow was correct.
- **Default-axiom overfire on Base Layer (Ebers Q1, Δ −1.00).** Held-out is an unconditional evangelical proclamation: *"Like the apostle, I would fain proclaim the gospel to all men according to the best of my powers."* C1 predicted "positively and earnestly" — matches the unconditional register. C3 applied the specification's "lived particularity over abstraction" axiom and predicted "receptivity, but only if the appeal is grounded in lived particularity rather than abstract principle." The axiom is correct on average but overfires on this specific unconditional moment. Reproduces on Mem0 and Supermemory with the same mechanism.

The shift in balance by system is a property of how much the retrieval already supplies the plain answer:

- **Mem0** (atomic-fact retrieval): wins on interpretation-heavy questions, loses on counter-example moments where atomic facts already have the plain answer.
- **Letta archival** (retrieval with 0.34-0.47 dedup ratio — only 3-5 unique facts in a top-10 list, documented in `mem0_letta_zep_c1_vs_c3_analysis.md`): big wins when the few unique facts align with the specification's axioms; moderate losses otherwise.
- **Zep** (temporal graph, verbose relational substrate): cleanest profile, fewest catastrophic losses (0 big-losses on Seacole), temporal structure and specification axioms compose well.
- **Supermemory** (strong embedding retrieval, highest C1 mean ~2.65): most hurts-heavy because strong retrieval means the plain answer is often already there, maximizing over-theorization and refusal triggers.
- **Base Layer** (MiniLM + ChromaDB semantic-embedding neighbors): distribution similar to Mem0 and Zep; helps on interpretation, hurts on refusal-triggering questions. Response form is indistinguishable from commercial systems' response form; the substrate differences sit below the generation layer.

---

**The cleanest cross-substrate replication in the study: Keckley Q21.**

Keckley Q21 — *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"* — produces a spec-induced refusal on Supermemory (§1.3) and on Base Layer's retrieval substrate, with identical −2.33 per-question Δ on both systems. The held-out passage carries Keckley's interior motive for not visiting, which the training half of the corpus does not contain; no retrieval substrate can surface it. The specification's documented-dignity and intimate-authority axioms then trigger the same refusal pattern on any substrate where C1 is otherwise willing to speculate productively:

| System | C1 (retrieval alone) | C3 (retrieval + spec) | Δ (C3 − C1) | C1 behavior |
|---|---:|---:|---:|---|
| Supermemory | 3.83 | 1.50 | **−2.33** | productive speculation from retrieved facts |
| Base Layer | 3.33 | 1.00 | **−2.33** | productive speculation from retrieved facts |
| Mem0 | 2.00 | 1.50 | −0.50 | already hedging from atomic retrieval |
| Zep | 1.83 | 1.33 | −0.50 | already hedging from edge retrieval |
| Letta archival | 1.33 | 2.33 | +1.00 | also refused; spec's structured refusal helped |

Different retrieval substrates, different fact pools, different baseline behaviors, identical specification; the refusal and penalty reproduce exactly when C1 is in productive-speculation mode, shrink when C1 is already hedging, and reverse when C1 was already refusing. The Q21 refusal is a property of the specification, not the memory system. The rubric penalty for that refusal is a property of the rubric, not the specification (§3.7.6 validity audit, §4.4 Example 3). This is the single cleanest cross-substrate replication the study produced.

---

**What this means for measurement.**

Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-substrate refusal) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*. The content-match rubric scores the second; it cannot score the first. A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that rewards epistemic honesty on questions the retrieved facts cannot answer without fabrication, would recover a cleaner measurement of the specification's real effect. This is the single most impactful follow-up for the measurement framework, flagged as the priority rubric-design follow-up in §8.

---

**Raw data and scripts.** Full per-subject per-system paired distributions at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Analysis scripts at `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py`, and `scripts/analyze_sm_c1_vs_c3.py`.
