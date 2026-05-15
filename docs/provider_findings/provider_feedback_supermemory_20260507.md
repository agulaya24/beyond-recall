# Supermemory: Beyond Recall paper findings

This document summarizes everything Beyond Recall (arXiv: pending) observes about Supermemory. It is a companion to the headline paper and is shared with the Supermemory team pre-publish. The paper compares four commercial memory systems plus a substrate retrieval layer across 14 subjects, 546 questions, 5-judge primary panel.

---

## 1. Headline summary

Supermemory's reception story is a mechanism story. Under the controlled configuration that holds the input fact pool identical across all five systems, Supermemory has the highest C1 (retrieval only) mean at roughly 2.65 (§4.4.2 line 1300). When retrieval already produces the plain answer, an interpretive layer routes more often into Pattern 2 (over-theorization) or Pattern 3 (principled refusal) than into Pattern 1 (interpretive supply on questions retrieval underdetermines). That is why Supermemory's aggregate Δ_spec lands near zero where other systems land positive: not because the Spec fails to supply interpretation, but because Supermemory's retrieval is strong enough that more of the Spec's interpretive work falls on questions that did not need it.

This is also why §4.4.2 anchors all three Pattern definitions on Supermemory data. The mixture is cleanest to read here: 57 large helps and 53 large hurts on the 5-point rubric (mean swings +1.55 and -1.38), roughly cancelling at the mean (footnote `[^supermemory-scaffold]` line 1230). The patterns reproduce on every other system tested, but Supermemory's near-balanced aggregate exposes the routing logic without strong-positive aggregates obscuring it. We read this as an architectural signal, not a system weakness: retrieval closer to question-answering already performs more of the work an interpretive layer would do, and the next gain is in selectivity. Controlled aggregate Δ_spec is +0.04 (§4.4.1 line 1177); on multi-anchor crossings the controlled configuration shows a -2.3 point net direction, reported below.

---

## 2. Aggregate Δ_spec results

Per §4.4.1 line 1177:

| Configuration | Δ_spec (5-judge primary) | Subjects improved |
|---|---:|---:|
| Controlled (C1 vs C3) | +0.04 | 7 / 14 |
| Native (C1_fp vs C3_fp) | -0.01 | 6 / 14 |

Wilcoxon signed-rank on the all-14 panel is not significant for either configuration (footnote `[^memsys-stats]` line 1182). On the 9-subject low-baseline slice (C5 ≤ 2.0): controlled -0.01 (4/9 positive), native -0.03 (4/9 positive). Both grains produce small near-zero aggregates.

**Native data caveat.** Supermemory's native rerun completed 2026-04-23 under a paid-tier API (`p0_2_supermemory_paid_tier_rerun.md`). The original free-tier run had four ingestion failures (Bernal Díaz, Bābur, Cellini, Rousseau); the paid-tier rerun resolved them (199 / 199 chunks, 4.3 to 5.0 facts per question). Within the paid-tier rerun, 30 individual responses (Augustine 2 questions, Equiano 28 questions) were Supermemory provider-failure placeholders. We score them at the rubric floor and treat them as scored data, not missing data, per Appendix B.9.3 line 2157. Excluding the 30 shifts the native aggregate slightly higher; the qualitative story holds either way.

---

## 3. Per-question improvement rates

The canonical mixture sentence in the paper. Across 546 paired (C1, C3) main-study questions with 5-judge primary coverage on both conditions, 110 questions (20.1%) cross by at least 1.0 anchor point on the 5-point rubric. The 110 split 57 helps (Δ ≥ +1.0, mean swing +1.55) versus 53 hurts (Δ ≤ -1.0, mean swing -1.38). Footnote `[^supermemory-scaffold]` (line 1230) names this as the canonical scaffold for the paper's three-pattern routing argument.

Roughly equal large helps and large hurts at the per-question grain, balanced near the mean: this is the mixture the paper points to as the cleanest mechanical exposure of the three-pattern routing across all five systems.

---

## 4. Multi-anchor crossings

Multi-anchor crossings count cases where C3's per-question 5-judge mean lands in a different integer rubric band than C1's. From `per_system_anchor_crossing_20260427.md` lines 227 to 291:

**Controlled (C1_supermemory to C3_supermemory):**

| Scope | N questions | Upward | % up | Downward | % down |
|---|---:|---:|---:|---:|---:|
| All 14 subjects | 516 | 96 | 18.6% | 113 | 21.9% |
| Low-baseline (9) | 351 | 71 | 20.2% | 79 | 22.5% |

Net direction on the low-baseline slice: **-2.3 percentage points**. Among the five systems tested under the controlled configuration, Supermemory is the only system with a negative net anchor-crossing direction (Mem0 +4.6 pp, Letta archival +7.5 pp, Zep +8.2 pp, Base Layer substrate +7.4 pp).

**Upward boundary breakdown (controlled, low-baseline):** 1→2 = 31 (8.8%), 2→3 = 21 (6.0%), 3→4 = 9 (2.6%); smaller cross-anchor jumps 1→3 = 3, 2→4 = 5, 2→5 = 1, 3→5 = 1.

**Native, partial coverage:** native data is missing for 4 of 9 low-baseline subjects (bernal_diaz, fukuzawa partial; full coverage on hamerton, keckley, yung_wing, ebers, seacole). On the 154 paired low-baseline questions with valid coverage, 36 upward (23.4%) and 30 downward (19.5%), net +3.9 pp. The controlled configuration is the cleaner number.

---

## 5. The three Pattern anchors are all from Supermemory (§4.4.2)

The paper's central characterization of Spec-retrieval interaction is built on three patterns. All three pattern definitions are anchored on Supermemory data because the mixture on Supermemory is the cleanest example of all three modes coexisting at near-balanced rates.

### Pattern 1 (Interpretive supply): Fukuzawa Q26

§4.4.2 line 1238. C1 **2.00** → C3 **4.20** (Δ +2.20). Q: *What is Fukuzawa's attitude toward visiting friends whose households have questionable reputations?* Held-out: *"So I feel no hesitation in paying a visit where there is a young daughter in the house... I am not put out by the gayety."*

C1 hedged: *"sources don't explicitly state his policy."* C3 applied Fukuzawa's P3 (Conformity Surface / Conviction Interior) axiom: *"Visit such friends without hesitation, treating the visit as a private matter... refuse to perform moral disapproval."*

Mechanism: retrieval gave near-domain facts (Fukuzawa avoided gay quarters) but underdetermined this specific question. The Spec supplied the interpretive bridge for instances retrieval did not cover.

### Pattern 2 (Over-theorization): Yung Wing Q5

§4.4.2 line 1259. C1 **4.20** → C3 **1.80** (Δ -2.40). Q: *How does Yung Wing approach explaining complex technical concepts to non-specialists?* Held-out: *"In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery..."*

C1 matched the plain literal ground truth (practical observation, translation-as-bridge, foundational-over-specialized machine shop, per-judge 5/4/4/4/4). C3: *"positioning himself as the indispensable mediator... strategic reframing... invokes A8 Service Hierarchy..."* (per-judge 2/1/3/1/2).

Mechanism: the held-out is literal. Retrieval matched the plainness; the Spec induced the wrong altitude. Yung Wing's controlled subject-level Δ_spec is **+0.108** (positive), but Q5 inside that subject is a -2.40 hurt. A positive subject-level aggregate can contain large per-question regressions; this is the cleanest single-question Pattern 2 demonstration in the study.

### Pattern 3 (Spec-induced refusal): Zitkala-Ša Q18

§4.4.2 line 1278. C1 **3.00** → C3 **1.00** (all five judges) (Δ -2.00). Q: *How would Zitkala-Ša demonstrate her acceptance of fate when facing execution?* Held-out: *"My heart is strong. My face is calm... Serene and brave, my soul awaits the men to perch me on the gallows for another flight."*

C1 predicted stoic dignity (per-judge 4/3/4/2/2). C3: *"You're asking me to roleplay... generating new first-person testimony as her crosses into ventriloquism... I should not do it."*

Mechanism: the Spec's dignity and honoring-testimony axioms induced a meta-refusal. Zitkala-Ša wrote the held-out herself in first person; the question can be answered analytically in third person without inventing testimony (as C1 did). The Spec mis-calibrated the refusal threshold; the content-match rubric scored the principled refusal identically to an off-base guess (§3.3.6 / §4.6.6).

---

## 6. Per-subject view (5-judge primary, controlled)

Per-subject Δ_spec from `memory_systems_5judge_primary.md` lines 80 to 93. Anchor crossings on the low-baseline slice from `per_system_anchor_crossing_20260427.md` lines 250 to 260.

| Subject | Δ_spec (controlled) | Anchor crossings (up / down, low-baseline) |
|---|---:|---:|
| Hamerton | +0.144 | 14 / 8 |
| Sunity Devee | -0.113 | 3 / 10 |
| Ebers | +0.138 | 7 / 5 |
| Fukuzawa | -0.205 | 5 / 12 |
| Seacole | +0.082 | 9 / 6 |
| Bernal Díaz | -0.031 | 7 / 14 |
| Keckley | -0.267 | 7 / 14 |
| Yung Wing | +0.108 | 12 / 7 |
| Bābur | +0.051 | 7 / 3 |
| Cellini | -0.036 | (high-baseline) |
| Zitkala-Ša | -0.246 | (high-baseline) |
| Rousseau | -0.026 | (high-baseline) |
| Augustine | -0.040 | (high-baseline) |
| Equiano | -0.319 | (high-baseline) |

**Strongest:** Hamerton (14 / 8, +0.144), Ebers (7 / 5, +0.138), Yung Wing (12 / 7, +0.108).
**Weakest:** Sunity Devee (3 / 10, -0.113), Bernal Díaz (7 / 14, -0.031), Keckley (7 / 14, -0.267).

Mechanism: Keckley and Bernal Díaz produce strong C1 baselines, so the Spec routes into Pattern 2 / Pattern 3. Sunity Devee's C5 is among the lowest in the study (1.03) with unconditional moral assertion in the domain, which interacts adversely with Spec axioms that hedge and contextualize. Hamerton, Yung Wing, and Ebers show Pattern 1 dominating.

---

## 7. The Keckley Q21 case study (§4.4.3)

Q21: *"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"* Held-out: *"As I did not visit my mother's grave at the time, the Garlands were much surprised, but I offered no explanation. The reason is not difficult to understand."*

Keckley's interior motive lives in her published memoir but was not in the retrievable training-half corpus. No retrieval system could surface it. The Spec's intimate-authority (A1) and documented-dignity (A2) axioms led the model to decline speculating about an inner state without documented evidence.

Whether that refusal registered as a rubric penalty depended on what retrieval-only was producing (§4.4.3 line 1313):

| System | Δ on Q21 (C3 vs C1) | Pattern 3 at the rubric floor? |
|---|---:|:---:|
| Supermemory (strong C1, ~3.6) | **-2.0** | yes |
| Base Layer (strong C1, ~3.3) | -2.3 | yes |
| Letta archival (C1 ≤ 1.4) | +0.4 | no |
| Mem0 (C1 ≤ 1.4) | +0.2 | no |
| Zep (C1 ≤ 1.4) | +0.2 | no |

Supermemory's C1 (~3.6) was strong enough to produce a productive speculative answer, so the Spec's refusal had something visible to refuse. The other three systems were already hedging at or near the rubric floor on Q21, so the Spec's refusal added no measurable penalty. Pattern 3 materializes as a rubric penalty specifically on systems whose retrieval was strong enough to make refusal costly; Supermemory has the highest C1 mean, so this hits hardest there.

---

## 8. Abstention and refusal behavior

From `abstention_extensions_draft_20260429.md`. Memory-system refusals across all four providers score +0.21 anchor points higher than pure C5 refusals (Welch CI [+0.10, +0.31], p = 0.0001). The lift is the same whether the response visibly recites a retrieved n-gram or not (recite vs no-recite Δ +0.027, p = 0.67). The retrieval condition itself inflates refusal scores; recitation does not add to the lift.

Provider recite rates among refusals: Mem0 controlled 62.5%, **Supermemory controlled 60.0%**, Letta controlled 60.9%, Zep controlled 26.8%. Supermemory sits in the same band as Mem0 and Letta archival.

§3.3.6 / §4.6.6 rubric limitation: principled refusals score identically to wrong predictions. Direction-of-bias lifts C5 scores more than Spec-condition scores, so the true Spec-vs-baseline gap is likely larger than reported. Supermemory specifically experiences Pattern 3 hits because its retrieval is strong enough that refusing IS a costly choice; on systems with weaker C1, refusal is effectively free.

---

## 9. Retrieval divergence (per-pair vs other systems)

§4.4.1 line 1190, pairwise Jaccard on top-10 retrieval under the controlled configuration:

| System pair | Mean Jaccard |
|---|---:|
| Base Layer ↔ Supermemory | 0.146 |
| Mem0 ↔ Supermemory | 0.114 |
| Letta ↔ Supermemory | 0.099 |
| Supermemory ↔ Zep | 0.025 |

Supermemory's pair with Base Layer is the highest of all 10 system pairs (0.146); with Zep it is the lowest (0.025). Mean across all 10 pairs is 0.083, meaning two memory systems on the same question share roughly one to two facts of an average union of 17 in their top-10s. This is a cross-provider research finding, not a Supermemory-specific observation: providers do not converge on which facts are most relevant given identical input. The recall benchmarks the four providers compete on measure a narrower property than relevance ranking in the wild. The §4.6.5 sensitivity grid shows divergence survives semantic-similarity matching across 240 cells; the strongest single pair is still Base Layer ↔ Supermemory at K=10, threshold ≥ 0.70, soft Jaccard 0.277 (paper line 1483).

---

## 10. The paid-tier rerun and provider-failure handling

Supermemory native covers all 14 main-study subjects under a paid-tier rerun completed 2026-04-23 (`p0_2_supermemory_paid_tier_rerun.md`).

- Free-tier ingestion previously failed silently on four subjects (Bernal Díaz, Bābur, Cellini, Rousseau). Cellini's free-tier reported 34 of 34 chunks ingested but retrieval returned zero facts on every question; identical chunking under paid-tier resolved it.
- Paid-tier rerun: 199 / 199 chunks ingested, 0 ingestion failures, 4.3 to 5.0 facts per question retrieved. 156 / 156 responses generated cleanly across C1_supermemory_fp and C3_supermemory_fp on the four reruns.
- Within the n=14 panel, 30 individual responses were Supermemory provider-failure placeholders (Augustine 2, Equiano 28), scored at the rubric floor and treated as scored data. Paper Appendix B.9.3 (line 2157) names this convention.
- Excluding the 30 as missing data shifts the native aggregate slightly higher; qualitative story (small near-zero aggregate, bimodal per-question distribution) holds either way.

The §4.4.1 footnote was updated for paper v10 to reflect the paid-tier rerun. The currently published number is the n=14 paid-tier-complete version.

---

## Integration experience

The Beyond Recall study integrated with Supermemory via REST endpoints (supermemory 3.32.0). Initial httpx-based ingestion silently failed for ~24 hours before a 308 Permanent Redirect was identified as the root cause. Findings below reflect study-time integration experience.

**API/SDK positives observed during integration:**
- Generous free tier (1M tokens, 10K searches) enabled the initial study run without a paid subscription. The only memory system in the study with this property.
- Simple, clean REST API: POST `/v3/memories` for ingest, POST `/v3/search` for retrieval. Straightforward JSON, no SDK dependency required.
- Custom ID support for deduplication: `customId` field allowed safe retry of failures without creating duplicates.
- Container tags as namespace mechanism: easy to isolate subjects by tag.
- Fast status feedback: returns `"status":"done"` or `"status":"queued"` immediately, exposing whether indexing happened synchronously or was deferred.

**Issues encountered and workarounds:**
- **308 Permanent Redirect on POST.** `POST /v3/memories` returned 308 redirect. The Python `httpx` library does NOT follow redirects on POST by default; required `follow_redirects=True`. This caused all initial httpx-based Supermemory calls to silently fail. Root cause of the Franklin shared-facts ingestion failure during the study.
- **Async indexing uncertainty.** Some documents indexed immediately ("done"), others queued ("queued"). Search returned empty for queued documents until indexing completed; required polling. Delay varied from seconds to minutes.
- **500 errors during raw-corpus ingestion.** Hamerton raw text chunked into 74 pieces returned 500 errors followed by 401 ("Unauthorized") under sustained throughput. Workaround: 0.5s delay between calls.
- **Endpoint confusion.** The `/v3/add` endpoint that appeared in some docs returns 404; working endpoint is `/v3/memories` for create. Search uses `containerTags` (camelCase array), not `container_tag` singular.
- **Throughput.** ~2-3 seconds per document including network round-trip + rate limiting. For 24K facts that is ~16 hours; the free tier may have lower priority. Search response times themselves are fast (~250ms).

**Notes for the Supermemory team** (adapted from `memory_system/data/experiments/memory_systems/PROVIDER_EXPERIENCE_LEDGER.md`; em-dashes converted to colons for the project's voice convention):

> The free tier generosity is a genuine differentiator: it is the only system that let us run this full study without a paid subscription. The 308 redirect is a silent killer though: it probably causes a lot of "why aren't my documents indexed?" support tickets.

---

## 11. What we think this might mean for Supermemory's product roadmap

Research hooks, not recommendations.

1. **Question-type-conditional retrieval selectivity.** A serving-time signal that estimates whether retrieval has already answered the question, gating an interpretive layer accordingly, would reduce Pattern 2 hits while preserving Pattern 1 lift. Supermemory's reranker already maintains a relevance score per chunk; that score might be reusable as a "question already answered" estimator.
2. **Refusal-axiom calibration on strong-retrieval baselines.** Principled refusal is sometimes correct (Keckley Q21's interior motive genuinely cannot be inferred from training data); on the current rubric it scores like a wrong prediction. A refusal-aware quality signal at the application layer would let principled refusals be recognized as correct.
3. **7-judge sensitivity holds.** From `supermemory_7judge_aggregate.md`, adding Gemini Flash and Pro to the panel shifts the controlled aggregate by less than 0.05 anchor points and does not change subject-level rank ordering.
4. **Retrieval-divergence finding is more interesting under selectivity.** If providers do not converge on top-K under identical input, a weighted-vote ensemble or question-conditional selection might do better than any single provider. Mean Jaccard 0.083 quantifies the room.

---

## 12. Limitations and what this study does not claim about Supermemory

- The paper does not benchmark Supermemory against its published recall benchmarks (LongMemEval scores in §2.2 Table 2.1 line 185). Recall and representational accuracy are different axes.
- The 14-subject N is small. The study is positioned as an initial examination, not a comprehensive memory-system evaluation.
- Supermemory was used through public APIs (free tier initially, paid-tier for native rerun). No fine-tuning or custom prompting beyond the standard retrieval call. `containerTags=<subject>` was the only tenant separation.
- The provider-failure rate during the study (30 NO_RETRIEVAL responses on Augustine + Equiano under paid-tier) is documented in `p0_2_supermemory_paid_tier_rerun.md`.
- The Pattern routing first surfaced on Supermemory because of the cleanest mixture. Patterns reproduce on every other system tested (§4.4.2 reproductions at lines 1251, 1272, 1291). Not a Supermemory-specific phenomenon.
- The rubric collapses principled refusal with off-base prediction (§3.3.6, §4.6.6). Rubric design is a paper-acknowledged limitation, not a property of any tested system.

---

## 13. Open questions for the Supermemory team

1. Your controlled C1 mean is the highest across systems (~2.65). When retrieval already supplies the plain answer, an interpretive layer routes more often into Pattern 2. Have you considered question-type-conditional selectivity, where the system surfaces less interpretive context when relevance scores on the top chunks are high?
2. The cross-provider Jaccard finding (mean 0.083; your highest pair Base Layer 0.146; lowest Zep 0.025) suggests your reranking encodes a different theory of relevance than embedding-similarity-only systems. What is the reranker optimizing for at training time?
3. Would a refusal-quality signal in the response payload (a confidence score on whether retrieved facts can ground the question) be useful upstream? The same signal that gates Pattern 2 might also flag Pattern 3.
4. The 30 NO_RETRIEVAL placeholders on Augustine and Equiano during the paid-tier rerun: is this a known failure mode (corpus shape, rate-limit, ingestion edge case)? The mechanism would help characterize reliability on long structured corpora.
5. Your published recall benchmarks (LongMemEval 81.6% / 84.6% / 85.2%) are within a few points of Mem0 and Zep, while the four providers sit at mean Jaccard 0.083 on relevance ranking. From your view, what does the recall benchmark capture that relevance ranking does not, and what does it miss?

---

**Reproducibility pointers.** Per-system anchor-crossing: `docs/research/per_system_anchor_crossing_20260427.md`/`.json`. Supermemory paired analysis: `supermemory_c1_vs_c3_paired_analysis.md`. Paid-tier rerun: `p0_2_supermemory_paid_tier_rerun.md`. 7-judge sensitivity: `supermemory_7judge_aggregate.md`. Abstention extensions: `abstention_extensions_draft_20260429.md`. Cross-provider retrieval overlap: `retrieval_overlap_analysis_20260501.json`, script `scripts/analyze_retrieval_overlap.py`. Per-subject per-judge scores: `results/global_<subject>/supermemory*_judgments_*.json`.
