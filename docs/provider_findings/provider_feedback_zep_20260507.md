# Zep: Beyond Recall paper findings

This document summarizes everything Beyond Recall (arXiv: pending) observes about Zep. It is a companion to the headline paper and is shared with the Zep team pre-publish. The paper compares four commercial memory systems plus a substrate retrieval layer across 14 subjects, 546 questions, 5-judge primary panel.

---

## 1. Headline summary

Zep produces the strongest aggregate result among the four commercial systems on our primary memory-system contrast (C1 retrieval-only vs. C3 retrieval + Behavioral Specification). On the all-14-subject panel: controlled mean Δ_spec +0.19, 13/14 improved, Wilcoxon p = 0.0004; native mean Δ_spec +0.33, 13/14 improved, Wilcoxon p = 0.0015 (§4.4.1 line 1176; `[^memsys-stats]` line 1182). Zep's controlled p-value is the lowest among the four commercial systems' controlled tests. On the 9-subject low-baseline slice, Zep is 9 of 9 improved under both configurations, the only commercial system with that consistency under both (`v11_emit/4_4_1_memory_systems.json:1545,1728`). At the per-question grain, §4.4.2 line 1299 names Zep as showing "the most favorable balance across Patterns 1-3, with the fewest large-magnitude regressions in the paired sample." The one soft note is retrieval divergence: Zep's pairwise Jaccard with the other three commercial systems and Base Layer is materially lower than any other pair (0.025 to 0.056 across Zep's pairs vs. cross-system mean 0.083). We frame this as a research observation about cross-provider retrieval divergence (§4.4.1), not a Zep critique.

## 2. Aggregate Δ_spec results

Δ_spec = mean(C3) − mean(C1), aggregated per subject, then averaged across subjects, on the 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).

| Configuration | Mean Δ_spec | All-14 improved | Wilcoxon p (all-14) | Low-baseline 9 improved | Wilcoxon p (low-9) |
|---|---:|---:|---:|---:|---:|
| Controlled (C1_zep vs. C3_zep) | +0.19 | 13/14 | 0.0004 | 9/9 | 0.0039 |
| Native (C1_zep_fp vs. C3_zep_fp) | +0.33 | 13/14 | 0.0015 | 9/9 | 0.0039 |

Source: §4.4.1 line 1176; `[^memsys-stats]` line 1182; `docs/research/v11_emit/4_4_1_memory_systems.json:1441,1479,1583,1624,1662,1766`. Both configurations are significant at α = 0.01. Among the four commercial systems' controlled tests, only Zep and Letta archival pass α = 0.01 (Zep p = 0.0004, Letta p = 0.0017). Among native tests, only Zep and Mem0 pass α = 0.01 (Zep p = 0.0015, Mem0 p = 0.0088). Letta archival's native delta is approximately null (−0.02) and Supermemory native is also near zero (−0.01); Zep is one of two commercial systems where the Spec adds measurably under native ingestion.

## 3. Per-question improvement rates

The aggregate Δ_spec is a mixture of per-question helps and hurts (§4.4.2 lines 1218 to 1303). The per-question signature for Zep, captured in Appendix B.11 line 2198 and `[^memsys-pattern-appendix]` line 1232: on Seacole, 27 of 39 paired questions cross by ≥ 1.0 anchor point (20 increases vs. 7 decreases, 0 large regressions in this specific cell).

Across the four-subject Zep paired analysis (`mem0_letta_zep_c1_vs_c3_analysis.md:33-40`), large regressions per cell are: Ebers 1, Seacole 0, Bernal Díaz 1, Keckley 3. The Seacole 0 figure is per-cell, not paper-wide. The §4.4.2 line 1299 framing is comparative: "fewest large-magnitude regressions in the paired sample" relative to the other three commercial systems and Base Layer.

The single largest per-question paired delta observed across all 12 (system × subject) cells in the per-system paired analysis is Zep on Seacole Q2 ("How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"): C1 mean 1.00 → C3 mean 5.00, Δ +4.00, all judges scoring 5 in C3 (`mem0_letta_zep_c1_vs_c3_analysis.md:120-128`).

## 4. Multi-anchor crossings

We score multi-anchor crossings at the per-question level: a 2-band jump is 1.x → 3.x, a 3-band jump is 1.x → 4.x. Source: `per_system_anchor_crossing_20260427.md:160-225`.

| Configuration | Upward / 351 | % upward | Downward / 351 | % downward | Net (pp) |
|---|---:|---:|---:|---:|---:|
| Controlled (low-baseline 9) | 98 | 27.9% | 69 | 19.7% | +8.3 |
| Native (low-baseline 9) | 114 | 32.5% | 48 | 13.7% | +18.8 |

Under controlled, Zep's net upward direction (+8.3 pp) is the highest among the five systems (`per_system_anchor_crossing_20260427.md:371-379`: Mem0 +4.6, Letta +7.4, Supermemory −2.3, Base Layer +7.5). Under native, Mem0 is +21.2 pp and Zep is +18.8 pp; Zep is second-highest under native.

**Multi-anchor jumps (low-baseline 9 scope):** Zep controlled has 21 multi-anchor jumps (2+ bands: 18+2+1), the highest count under any controlled configuration in the study (Letta 20, Base Layer 13, Mem0 9, Supermemory 10) (`per_system_anchor_crossing_20260427.md:336-345`). Under native, Zep's 24 multi-anchor jumps (19+5+0) sit second to Mem0 native at 26 (Mem0 20+5+1).

**Per-boundary breakdown (native, low-baseline 9):** 1→2 = 70 (19.9%), 1→3 = 16 (4.6%), 1→4 = 5 (1.4%), 2→3 = 15 (4.3%), 2→4 = 3 (0.9%), 3→4 = 5 (1.4%) (`per_system_anchor_crossing_20260427.md:204-211`).

## 5. Pattern frequency (§4.4.2 routing)

§4.4.2 names three per-question patterns memory systems display under the Spec: interpretive supply (P1, helps), over-theorization (P2, hurts), Spec-induced refusal (P3, scored at floor). Per §4.4.2 line 1299: "Zep (temporal graph, verbose relational structure): most favorable balance across Patterns 1-3, with the fewest large-magnitude regressions in the paired sample."

On the Keckley Q21 cross-system case study (§4.4.3 lines 1322 to 1331), Zep's Δ on Q21 is +0.2 (within noise), unlike Supermemory (−2.0) and Base Layer (−2.3) where C1 retrieval was strong enough to make Spec-induced refusal a costly choice. Zep's C1 retrieval-only baseline on Q21 was already at or near the rubric floor (≤ 1.4), so the Spec's refusal axioms had no expensive ground to cede.

Zep's largest observed Pattern 1 anchor is Seacole Q2 (Δ +4.00, see §3): retrieval surfaced relational edges (`USED_FOR_RUBBING`, `SCREAMED_TO_ALERT`, `PRACTICED_ON`) that were biographically correct but semantically orthogonal to the question; the Spec carried the "proximate obligation overrides precision" pattern needed (`mem0_letta_zep_c1_vs_c3_analysis.md:175-181`).

## 6. Per-subject view (low-baseline 9, both configurations)

Per-subject Δ_spec means are not emitted per system in the paper (the all-14 aggregate is reported in §2; 13/14 improved under both configurations). This section reports the per-subject anchor-crossing direction available in `per_system_anchor_crossing_20260427.md:181-225`.

**Anchor crossings per 39 questions, low-baseline 9 scope:**

| Subject | Controlled (up / down / none) | Native (up / down / none) |
|---|---|---|
| Hamerton | 13 / 7 / 19 | 21 / 6 / 12 |
| Sunity Devee | 13 / 10 / 16 | 13 / 8 / 18 |
| Ebers | 9 / 4 / 26 | 8 / 3 / 28 |
| Fukuzawa | 8 / 9 / 22 | 14 / 7 / 18 |
| Seacole | 18 / 4 / 17 | 14 / 5 / 20 |
| Bernal Díaz | 11 / 8 / 20 | 12 / 6 / 21 |
| Keckley | 9 / 11 / 19 | 11 / 5 / 23 |
| Yung Wing | 12 / 9 / 18 | 14 / 4 / 21 |
| Bābur | 5 / 7 / 27 | 7 / 4 / 28 |

Zep's strongest cell in the paired analysis is Seacole, controlled aggregate Δ +0.52 across 39 paired questions on a six-judge merged panel (`mem0_letta_zep_c1_vs_c3_analysis.md:38`); the 5-judge primary aggregate at Appendix B.11 line 2198 is Δ +0.47 on the same 39 questions. Softer controlled cells: Bābur and Keckley. Largest native gain in anchor-crossing terms: Hamerton (21 vs. 6) and Rousseau (26 vs. 1, all-14 native scope, `per_system_anchor_crossing_20260427.json`). The only Zep cell with a clearly negative direction across the all-14 panel under native is Zitkala-Ša (3 up vs. 12 down).

## 7. Abstention/refusal behavior: the graph-protocol token-emission artifact

The paper logs an extension analysis of refusal behavior across memory-system conditions (`abstention_extensions_draft_20260429.md:30-58`):

| Cell | Definition | N | Mean | % ≥ 2.0 |
|---|---|---:|---:|---:|
| Pure C5 refusal | no facts, no retrieval | 292 | 1.26 | 10.3% |
| Memory-system refusal + recitation | refuses AND quotes retrieved n-gram | 148 | 1.50 | 18.2% |
| Memory-system refusal, no recitation | refuses, does not quote retrieval | 240 | 1.47 | 17.1% |

Memory-system refusals score +0.21 to +0.23 anchor points higher than pure C5 refusals; whether the response visibly recites a retrieved n-gram adds nothing on top (Δ between recite and no-recite = +0.027, p = 0.67). The lift is condition-based (retrieval-conditioned vs. pure C5), not recitation-based, and applies uniformly across all four memory systems.

Provider-level recite rates among refusals (`abstention_extensions_draft_20260429.md:54`): Mem0 controlled 62.5%, Supermemory controlled 60.0%, Letta controlled 60.9%, Zep controlled 26.8%. Zep's lower recite rate has a structural cause: Zep's graph-protocol retrieval emits tuple-encoded tokens such as `('communities', None)`, `('episodes', [])`, `('edges', [...])` on most subjects (`mem0_letta_zep_c1_vs_c3_analysis.md:58`). Our recitation detector uses 4-word, ≥15-character n-gram substring matching on lowercased text; the tuple-encoded wrapper gets filtered as noise before the n-gram match runs, so Zep recitation is effectively undetectable in this analysis. The substantive facts live on the `fact='...'` attribute of `EntityEdge` objects inside the wrapper; the wrapper is what filters as noise. This is a research observation about retrieval-token surface form as it reaches third-party n-gram-based analyses, not a critique of the graph approach.

## 8. Retrieval divergence (per-pair vs. other systems)

§4.4.1 lines 1186 to 1214 reports cross-system retrieval overlap on the controlled configuration (every system reads the same all-facts pool, top-10). Pairwise Jaccard similarity is the metric. Across all ten pairs over 546 questions, mean pairwise Jaccard is 0.083 raw, 0.088 after lowercase + whitespace normalization.

| Pair | Mean Jaccard |
|---|---:|
| Mem0 ↔ Zep | 0.056 |
| Base Layer ↔ Zep | 0.027 |
| Letta ↔ Zep | 0.026 |
| Supermemory ↔ Zep | 0.025 |

Zep's row is the lowest of the four commercial-system pairings. The §4.4.1 reading: "graph-traversal scoring overlaps weakly with embedding-similarity retrieval" (line 1206). Native config drops to exact-set Jaccard 0.000 across all four native pairs (heterogeneous return shapes); soft Jaccard at a near-paraphrase semantic-similarity threshold lifts native overlap only to 0.004 (§4.4.1 line 1214; §4.6.5 lines 1481 to 1494).

Frame: Zep produces the most distinctive retrieval profile in the four-system set on identical input. The §4.4.1 lede reframes the question from "which provider is right" to "providers do not converge on relevance given identical input." Convergence at larger K is flagged as future work (§7.1).

A separate axis: Zep's published LongMemEval score (71.2% with GPT-4o, Rasmussen et al. 2025, arXiv:2501.13956, cited at §2.2 line 186) is on a recall-shaped task. Beyond Recall measures representational accuracy on held-out behavioral prediction. The paper does not adjudicate against LongMemEval (§2.2 reports the 71.2% as published context).

## 9. Zep-specific findings

**Configuration.** Zep was used through `zep_client.graph.add` for ingestion and `client.graph.search(user_id, query, limit=10)` for retrieval (Appendix C.6, line 2290). Controlled ingests one fact per edge; native ingests the raw corpus through Zep's own pipeline.

**Bi-temporal architecture not exercised.** Zep's published architecture (Rasmussen et al. 2025) describes bi-temporal knowledge graph structure with `valid_at` / `expired_at` validity windows. Our question pattern is one-shot held-out-passage prediction; we do not query the graph with time-conditioning. Per `mem0_letta_zep_c1_vs_c3_analysis.md:179-203`: "no question used `valid_at` / `expired_at` to privilege recency... There is not a distinctive Zep-style 'time-anchored fact surfacing' pattern." Results here are graph-traversal retrieval with current-time queries; the bi-temporal feature is not operationalized in this study.

**Graph retrieval surface form.** The Graphiti SDK response surfaces as `[('communities', None), ('context', None), ('edges', [EntityEdge(...), ...]), ('episodes', []), ('nodes', []), ('sagas', None)]` (`mem0_letta_zep_c1_vs_c3_analysis.md:58`). Substantive facts live in the `edges` element on the `fact='...'` attribute of each `EntityEdge`; the response model parses ~8 to 12 edge facts from the blob. Edge labels include `USED_FOR_RUBBING`, `SCREAMED_TO_ALERT`, `INHERITED_INTEREST_FROM`, `PERCEIVED_NO_FLAWS_IN`.

**Native config matches or exceeds controlled magnitudes.** Across Mem0 (+0.12 → +0.33), Zep (+0.19 → +0.33), Letta archival (+0.20 → −0.02), and Supermemory (+0.04 → −0.01), Zep is one of two systems (with Mem0) where native does not lose ground relative to controlled. §4.4.1 line 1184: "Native ingestion shapes how much room the specification has to contribute on top, and that interaction varies by system."

**Provider issue logged.** §C.7 line 2302: "Zep graph retrieval surfaces entity-dense chunks over behavior-dense chunks. Reported as-is." Reported in the analysis without exclusion.

## Integration experience

The Beyond Recall study integrated with Zep via the `zep-cloud` Python package (3.20.0) after initial confusion between `zep-python` (self-hosted) and `zep-cloud` (cloud) returned 404s on all endpoints. Findings below reflect study-time integration experience.

**API/SDK positives observed during integration:**
- Knowledge graph approach is genuinely different from the other systems: facts become graph nodes with relationships, enabling structured reasoning paths (per `docs/references/rasmussen_2025_2501.13956_zep.pdf`).
- Batch-friendly: `graph.add()` accepts concatenated text, supporting batches of ~20 facts in one call.
- Credit system with auto-top-up prevents mid-run failures.
- User model with `first_name` field contextualizes the graph.
- `graph.add(type="text")` accepts multi-line text and handles its own extraction.

**Issues encountered and workarounds:**
- **15-second processing wait between batches** is mandatory for graph processing, not a rate limit. For 24K facts in batches of 20 that is ~300 minutes of waiting alone.
- **Graph traversal bias.** Same high-connectivity node returned for many unrelated queries. The most common single Zep top-1 fact on Hamerton appeared in ~11% of questions; father-related facts (any fact mentioning "father") appeared in ~54% of questions. An earlier draft cited a specific "39% same-fact retrieval" figure that could not be reproduced from `fact_localization.json` (see `PAPER_CORRECTIONS.md` #10); the structural pattern of graph hubs dominating retrieval regardless of query is the replicable finding.
- **10,000-character limit per `graph.add()`** requires pre-chunking large inputs. Documentation recommends 500-char chunks with 50-char overlap for optimal graph construction.
- **`user_id` mismatch.** `list_ordered()` returned named tuples, not User objects. Extracting `user_id` required `hasattr` checks. Initial runs failed silently with wrong user IDs.
- **SDK package confusion.** `zep-python` (self-hosted) vs `zep-cloud` (cloud) are different packages with different APIs. Initial attempt used wrong package; all endpoints returned 404.
- **Credit consumption is unpredictable.** 1 credit per episode base, 2 for episodes >350 bytes. Hard to estimate total cost before running.
- **SDK-only approach.** No simple REST API for basic operations. Some operations (like listing users) lack SDK methods.

**Notes for the Zep team** (adapted from `memory_system/data/experiments/memory_systems/PROVIDER_EXPERIENCE_LEDGER.md`; em-dashes converted to colons for the project's voice convention):

> The graph approach is the most intellectually interesting of the four: it is the only system that tries to understand relationships between facts rather than just storing and retrieving them. But the 15s processing wait and graph traversal bias limit its practical throughput and retrieval quality. Consider offering a "fast mode" that skips graph processing for batch ingestion scenarios.

---

## 10. What we think this means for Zep's product roadmap

Three observations that may be useful, framed as research hooks rather than recommendations.

**Native config preserves the room the Spec needs.** Zep's native config matches controlled (+0.33 vs. +0.19), unlike Letta archival or Supermemory under native. The paper does not isolate the mechanism. Candidate readings: (a) Zep's ingestion preserves more interpretive content than Letta's archival passage chunking, (b) graph structure produces less retrieval-pool dilution under raw-corpus ingestion than embedding-based providers do.

**Graph-protocol surface form affects third-party observability.** The tuple-encoded wrapper around the `edges` payload filters as noise in n-gram-based detectors. For internal Zep observability this is moot; for third-party analyses the surface form matters. Our recitation detector is one example; the abstention extension analysis treats Zep as a special case.

**Most distinctive retrieval profile in the four-system set.** Zep's pairwise Jaccard with the other systems (0.025 to 0.056) is materially below the cross-system mean (0.083). For Zep this is consistent with graph-traversal scoring producing a different ranking than embedding-based scoring; it is also a clean experimental signal that Zep is doing something the embedding providers are not. The convergence-at-K research question (does overlap rise at K=20, 50, 100) is open and Zep's team is best-positioned to answer it on their corpus.

The paper is a measurement; what to do with the measurement is a Zep call.

## 11. Limitations and what this study does NOT claim about Zep

The paper does not benchmark Zep against its published LongMemEval scores (§2.2 line 186); recall and representational accuracy are different axes. The 14-subject N is small. Zep was used through public APIs at standard rates with `limit=10` retrieval; no fine-tuning, no custom configuration beyond `zep_client.graph.add` and `client.graph.search`.

The graph-protocol token-emission observation (§7) is incidental; it surfaced during the abstention extension analysis. It is a research observation about retrieval-token surface form, not a critique of the graph architecture. The bi-temporal `valid_at` / `expired_at` feature is not operationalized in this study's query pattern (§9); a study that queried with time-conditioning would test a different property of Zep's architecture.

The retrieval-divergence finding (§4.4.1, §8) is a property of provider ranking, not a property that ranks providers against each other. The paper does not say Zep's ranking is wrong or right relative to the other systems; it says all five systems disagree on top-K relevance given identical input. The Pattern 3 Spec-induced refusal cost (§5) depends on how strong C1 retrieval was on the same question. On Zep, C1 retrieval was often already at or near the rubric floor on refusal-prone questions, so the Spec's refusal axioms cost less than on stronger-retrieval systems. This is a property of how Zep's retrieval landed on those questions, not an axis of evaluation.

## 12. Open questions for the Zep team

Five questions Zep's team is best-positioned to answer:

1. **Convergence at larger K.** Cross-system Jaccard at K=10 is 0.083; at K=20, 50, 100, does graph-traversal converge with embedding-based rankings, or remain disjoint? Flagged as future work in §7.1.

2. **Time-conditioned retrieval.** The bi-temporal `valid_at` / `expired_at` feature was not exercised in our one-shot query pattern. On a query that asks the graph for "which facts about subject X were valid at time T," does the graph return a materially different fact set than current-time queries?

3. **Native vs. controlled mechanism.** Why does Zep's native config match controlled (+0.33 vs. +0.19), unlike Letta archival (+0.20 → −0.02) or Supermemory (+0.04 → −0.01)? Candidate mechanisms include ingestion preservation, graph structure dilution resistance, edge-fact granularity. Zep can ablate.

4. **Surface form for downstream observability.** The Graphiti SDK tuple-encoded response wrapper filters as noise in n-gram-based analyses. Have you considered an alternative surface form (e.g., a flat list of `fact='...'` strings, with relational metadata in a sidecar) for downstream tools?

5. **Per-question retrieval selectivity within the graph.** On Seacole Q2 the graph surfaced relational edges that were biographically correct but semantically orthogonal to the question. Can the graph layer detect this orthogonality at retrieval time, or does the question need to be reformulated?

These are research questions. The data behind every claim is at `docs/research/per_system_anchor_crossing_20260427.json` and `docs/research/v11_emit/4_4_1_memory_systems.json`. Reproducibility scripts at `scripts/_table_4_6_5judge_recompute.py` and `scripts/analyze_retrieval_overlap.py`. Per-subject per-judge raw scores at `results/global_<subject>/zep_judgments_*.json`.
