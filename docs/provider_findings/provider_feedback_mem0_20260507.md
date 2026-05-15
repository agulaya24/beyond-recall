# Mem0: Beyond Recall paper findings

This document summarizes everything Beyond Recall (arXiv: pending) observes about Mem0. It is a companion to the headline paper, shared with the Mem0 team pre-publish. The paper compares four commercial memory systems plus a substrate retrieval layer across 14 subjects, 546 questions, 5-judge primary panel.

## 1. Headline summary

Mem0 is one of three commercial systems where adding the Behavioral Specification on top of retrieval produces a positive aggregate Δ under both controlled and native configurations (§4.4.1, line 1174). Δ_spec rises from +0.12 controlled to +0.33 native, the largest controlled-to-native jump of any system tested. The per-question picture is more textured than the aggregate. On interpretation-heavy questions, Mem0's atomic-fact retrieval supplies accurate biographical material and the specification supplies the interpretive pattern (Pattern 1 in §4.4.2; the anchor example at line 1251 is Ebers Q11, Δ +1.67). On literal-recall questions where retrieved facts already answer the question, the specification can pull the response into over-theorization (Pattern 2). On questions where retrieved facts cannot ground a prediction, the specification triggers principled refusal (Pattern 3). The aggregate Δ is the net of these three patterns. Mem0's atomic-sentence retrieval style is also the most consensus-aligned of the four commercial systems: mean Jaccard with the other three commercial systems is 0.099, roughly 2.7x Zep's 0.036 mean across its three commercial pairs (§4.4.1, lines 1192-1204).

## 2. Aggregate Δ_spec results

5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). Source: `docs/research/memory_systems_5judge_primary.md`.

| Configuration | Δ_spec (n=14) | Subjects improved | Δ_spec (n=9 low-baseline) | Improved (low-baseline) | Wilcoxon W, p (n=14) |
|---|---:|---:|---:|---:|---:|
| Mem0 controlled (C1_mem0 vs C3_mem0) | +0.121 | 10/14 | +0.101 | 6/9 | W=15.0, p=0.0166 |
| Mem0 native (C1_mem0_fp vs C3_mem0_fp) | +0.332 | 10/14 | +0.320 | 7/9 | W=8.0, p=0.0088 |

Native lift on top of controlled is +0.21 points (the largest such gap of any system: Zep +0.14, Letta −0.22, Supermemory ~flat). The published `infer=True` reformulation in the native ingestion path appears to do real work on this evaluation; we did not isolate the mechanism (§4.6 future work). The 7-judge sensitivity (adds Gemini Flash + Pro) shifts Mem0 controlled to +0.149 and native to +0.380; direction holds, magnitude widens by roughly +0.05. Per-judge consistency is in the per-subject sidecar files at `results/global_<subject>/mem0_judgments_<judge>.json`.

Note: §4.4.1 footnote `[^memsys-stats]` (line 1182) describes Mem0 controlled as not significant at α = 0.05; the source recompute file lists p=0.0166. Flagged for our reconciliation pass; native p=0.0088 is consistent across both sources.

## 3. Per-question improvement rates (|Δ| ≥ 1.0 threshold)

The paper's per-question metric is "increases" / "decreases" at |Δ| ≥ 1.0 on the 5-point rubric, controlled configuration, paired by question_id across C1 and C3. Source: §4.4.2 footnote `[^memsys-pattern-appendix]` (line 1232) and Appendix B.11 (line 2188).

| Subject | Aggregate Δ_spec | Increases (Δ ≥ +1.0) | Decreases (Δ ≤ −1.0) | Net |
|---|---:|---:|---:|---|
| Yung Wing | +0.33 | 21 | 10 | 21 helps outnumber 10 hurts 2.1× |
| Keckley | −0.02 | 12 | 13 | counts even, aggregate near zero |

Both rows are mixtures: 31 of 39 paired questions on Yung Wing cross by ≥ 1.0 in some direction; 25 of 39 on Keckley do. The aggregate Δ near zero on Keckley is canceled-out swings, not a flat per-question profile. This shape reproduces across every (system, subject) cell tested in Appendix B.11; full per-cell paired-delta arrays at `docs/research/per_system_anchor_crossing_20260427.json`.

A second per-question metric (integer-band crossing, controlled configuration, low-baseline 9 subjects only) is available at `per_system_anchor_crossing_20260427.md:51-60`. Counts are smaller than the |Δ| ≥ 1.0 metric because integer-band crossing requires moving across an integer rubric anchor (e.g., 1.x → 2.x). On the 9 low-baseline subjects, Mem0 controlled crosses 23.4% of paired questions upward and 18.8% downward; native crosses 36.1% upward and 14.9% downward. Both metrics agree in direction across all 14 subjects.

## 4. Multi-anchor crossings (low-baseline 9 subjects)

Source: `docs/research/per_system_anchor_crossing_20260427.md:336-345`. A "1-band" upward crossing is a question moving across one integer anchor (e.g., 1.x → 2.x); a "2-band" jump is e.g. 1.x → 3.x.

| Configuration | Total upward | 1-band | 2-band | 3-band | 4-band |
|---|---:|---:|---:|---:|---:|
| Mem0 controlled | 82 | 73 | 5 | 4 | 0 |
| Mem0 native | 126 | 100 | 20 | 5 | 1 |

Per-boundary breakdown, Mem0 native (low-baseline, line 73): 1→2: 79 (22.6%), 1→3: 18 (5.2%), 1→4: 5 (1.4%), 1→5: 1 (0.3%), 2→3: 17 (4.9%), 2→4: 2 (0.6%), 3→4: 4 (1.1%). Mem0 native produces 26 multi-anchor jumps (≥ 2-band) on 351 low-baseline paired questions. The 1→5 jump is one question; the 4 instances of 1→4 are the next-largest swings.

All-14-subjects scope for Mem0 native: 202 upward crossings (158 / 32 / 11 / 1 across 1-band / 2-band / 3-band / 4-band).

## 5. Pattern frequency (§4.4.2 routing)

The paper identifies three per-question patterns (§4.4.2, line 1222 onward):

1. **Pattern 1: Interpretive supply.** Retrieval underdetermines the answer; the specification provides the pattern. Increases score.
2. **Pattern 2: Over-theorization.** Retrieval already supplies the plain answer; the specification pulls toward depth the question does not need. Decreases score.
3. **Pattern 3: Spec-induced refusal.** Specification axioms trigger a meta-refusal where retrieval lacks evidence to ground a prediction. Lowers measured score; the §3.3.6 / §4.6.6 rubric does not credit principled refusal.

Mem0-specific reading from §4.4.2 (line 1297): atomic-fact retrieval shows more Pattern 1 on interpretation-heavy questions; more Pattern 2 on literal-recall questions atomic facts already answer.

**Pattern 1 anchor on Mem0 (Ebers Q11, Δ +1.67), §4.4.2 line 1251:** retrieval-only produced "patience and fortitude" as a generic character prediction; retrieval + Spec supplied the ideal-vs-reality axiom and predicted the institutional-disillusionment pattern, matching the held-out *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."*

**Pattern 2 on Mem0 (Ebers Q1, Δ −1.33).** Source: `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md` §3.1 M-LOSS. Held-out is an unconditional evangelical proclamation. C1 (retrieval only, mean 3.83) predicted "positively and deeply." C3 (retrieval + Spec, mean 2.50) over-conditionalized into a conditions-framework. The specification's resistance-to-coercion axiom is correct on average for Ebers but over-fired on this specific unconditional moment.

**Pattern 3 on Mem0 (Keckley Q21, Δ −0.50).** Source: §4.4.3 (line 1313) cross-system case study. Mem0's retrieval-only response was already a hedged non-answer at mean 2.00 ("no information, here are related facts"); Mem0 + Spec at mean 1.50 issued an explicit refusal. Penalty is small because the C1 counterfactual was weak. Under the same axioms on Supermemory, where C1 was at mean 3.83, the Spec-induced refusal cost −2.33 points. The Spec-induced refusal pattern is universal across systems; the rubric penalty depends on retrieval strength.

A quantitative per-pattern frequency breakdown across all 507 questions × 5 systems is not yet available. The paper flags this as future work in §7.

## 6. Per-subject view

5-judge primary, controlled and native Δ_spec. Source: `memory_systems_5judge_primary.md:80-93` (controlled) and `:99-112` (native).

| Subject | Mem0 controlled Δ_spec | Mem0 native Δ_spec |
|---|---:|---:|
| hamerton | +0.103 | +0.841 |
| sunity_devee | −0.082 | +0.344 |
| ebers | +0.149 | +0.378 |
| fukuzawa | +0.046 | +0.026 |
| seacole | +0.154 | +0.410 |
| bernal_diaz | −0.026 | −0.056 |
| keckley | −0.021 | +0.000 |
| yung_wing | +0.328 | +0.662 |
| babur | +0.256 | +0.277 |
| cellini | +0.364 | +0.533 |
| zitkala_sa | −0.123 | −0.036 |
| rousseau | +0.108 | +0.779 |
| augustine | +0.349 | −0.021 |
| equiano | +0.092 | +0.513 |

**Strongest Mem0 cells (native):** Hamerton (+0.841), Rousseau (+0.779), Yung Wing (+0.662). Hamerton is the pipeline-development subject for our substrate, tuned against; Rousseau and Yung Wing are not. The controlled-to-native gap on these subjects is the source of most of Mem0's +0.21 native lift.

**Weakest Mem0 cells:** Zitkala-Ša (controlled −0.123, native −0.036), Sunity Devee (controlled −0.082), Bernal Díaz (controlled −0.026, native −0.056). Zitkala-Ša is also one of two subjects where the Behavioral Specification did not measurably improve prediction in §4.1's main gradient (Equiano is the other); this cell tracks the gradient pattern rather than a Mem0-specific failure.

## 7. Abstention/refusal behavior

Source: `docs/research/abstention_extensions_draft_20260429.md` Section B.

Memory-system retrieval inflates refusal scores by +0.21 to +0.23 anchor points relative to pure C5 (no-context) refusals (Welch 95% CI [+0.103, +0.310], p = 0.0001). The lift is essentially the same whether the response visibly recites a retrieved n-gram (+0.027 between recite and no-recite cells, 95% CI crosses zero, p = 0.67). The inflation is a property of the retrieval condition; recitation does not add to it.

Per-provider recite rates among controlled refusals (line 54): Mem0 62.5%, Supermemory 60.0%, Letta 60.9%, Zep 26.8%. Mem0's highest-of-four rate is consistent with the atomic-sentence retrieval style: when a refusal occurs, the response model has clean sentence-shaped retrieved tokens to quote.

The §3.6.6 / §4.6.6 rubric limitation applies: the content-match rubric cannot distinguish a principled refusal from a wrong prediction. A scoring dimension that credits epistemic honesty where retrieved facts cannot answer the question is flagged as the priority rubric-design follow-up in §7.

## 8. Retrieval divergence (Mem0's pairwise Jaccard with other systems)

Source: §4.4.1 (line 1192) and `docs/research/retrieval_overlap_analysis_20260501.json`. Controlled configuration, n = 5,460 instances (14 subjects × 39 questions × 10 system pairs).

| Pair | Mean Jaccard |
|---|---:|
| Mem0 ↔ Letta | 0.126 |
| Base Layer ↔ Mem0 | 0.123 |
| Mem0 ↔ Supermemory | 0.114 |
| Mem0 ↔ Zep | 0.056 |
| **Mem0 mean across 4 pairs** | **0.105** |

Zep's mean across its 4 pairs is 0.034 (Mem0 0.056, Letta 0.026, Supermemory 0.025, Base Layer 0.027). Mem0's atomic-fact retrieval lands closer to other systems' rankings than graph-traversal does, while still sharing only 8-13% of top-10 facts on average with any given pair. Mean across all 10 pairs in the study is 0.083; on 35.9% of (system pair, question) instances two systems share zero facts in their top-10s. The systems do not converge on which facts the question is asking for, given identical input. §7.1 flags meta-analysis follow-ups: convergence at larger K, recall-benchmark vs. retrieval-overlap correlation.

## 9. Mem0-specific findings

**Atomic-fact retrieval style.** Source: `mem0_letta_zep_c1_vs_c3_analysis.md` §2 (line 54). Mem0 returns ~10 atomic fact statements, each a complete sentence. Dedup ratio is 1.00 on the four subjects studied closely (vs. Letta's 0.34-0.47), so the response model sees ten distinct facts rather than fewer with repeats. Occasional semantic-mismatch facts surface (e.g., a fact about Ebers' aunt returned for a question about institution management); the response model has to filter.

**`infer=True` reformulation in the native path.** Source: Appendix C.7 (line 2301). Native retains `infer=True` (the realistic deployment path); controlled used `infer=False` to hold input identical across systems. The +0.21-point native lift on top of controlled is consistent with `infer=True` doing useful work for representational accuracy, but the mechanism is not isolated in our data.

**Sentence-shape recitation.** Mem0's 62.5% recite rate among refusals (highest of the four systems) is a testable property of the atomic-sentence style. Recitation does not inflate refusal scores beyond the +0.21 retrieval-condition floor (§7); the rate itself is a Mem0-specific signature your team may want visibility on for deployment scoring.

## Integration experience

The Beyond Recall study integrated with Mem0 via raw HTTP after the official Python SDK exhibited urllib3/chardet hangs under sustained use. Findings below reflect study-time integration experience (mem0ai 1.0.11) and may not match Mem0's current SDK state.

**API/SDK positives observed during integration:**
- `infer=False` parameter lets facts be stored verbatim without LLM reformulation, critical for controlled-experiment integrity. Verified end-to-end: sent fact, retrieved identical fact.
- Fast ingestion at sustained ~5-10 facts/sec under raw HTTP, fastest of the four memory systems tested.
- Immediate availability: facts searchable within seconds of ingestion, no async indexing lag.
- v2 search endpoint supports filters, top_k, and semantic search beyond v1.

**Issues encountered and workarounds:**
- **SDK init hang.** `from mem0 import MemoryClient` hung indefinitely after ~50 queries. Root cause: urllib3 2.3.0 / chardet 7.1.0 version mismatch. Workaround: raw HTTP via `requests.post("https://api.mem0.ai/v1/memories/search/", ...)`. The first 55 questions used the SDK; the remaining 25 used raw HTTP; results were identical.
- **API version split.** Ingestion is v1, search is v2. Not obvious which to use without reading docs carefully; v1 search still works but is deprecated.
- **No bulk text ingestion.** `client.add()` accepts one memory at a time. For 1,133 Franklin facts: 1,133 sequential API calls (~15-20 minutes).
- **Response format inconsistency.** v2 search returns a flat list; some endpoints return `{"results": [...]}` vs `{"memories": [...]}`. Required defensive parsing.

**Notes for the Mem0 team** (adapted from `memory_system/data/experiments/memory_systems/PROVIDER_EXPERIENCE_LEDGER.md`; em-dashes converted to colons for the project's voice convention):

> The `infer=False` parameter is a thoughtful addition: it shows awareness that not everyone wants the LLM reformulation. Fix the SDK hang (it has been months), add a bulk ingestion endpoint, and this becomes the easiest platform to integrate with.

---

## 10. What we think this means for Mem0's product roadmap

The Pattern 1 / Pattern 2 routing-by-question-type observation in §4.4.2 is the most useful product signal from our data. Atomic-fact retrieval helps on questions where the held-out answer requires generalizing from biographical material to a specific situation; it routes more responses into Pattern 2 on questions where retrieved facts already supply the literal answer.

A dynamic-serving policy (selecting which specification components to surface based on inferred question type) could in principle reduce Pattern 2 hurts while preserving Pattern 1 helps. §7.4 flags this as production-serving future work for our own pipeline; we mention it here because the Mem0 team is better positioned to test whether question-type routing on top of atomic-fact retrieval composes well with `infer=True` reformulation. Frame as a research hook, not a recommendation.

## 11. Limitations and what this study does NOT claim about Mem0

- The paper does not adjudicate Mem0's published LongMemEval (93.4) or LOCOMO (91.6) recall numbers (§2.2, line 183). Chhikara et al. arXiv:2504.19413 reports 68.44 LOCOMO for Mem0g with GPT-4o-mini; we do not run that benchmark. Our comparison is on representational accuracy in held-out behavioral prediction, a different layer of the stack.
- N = 14 subjects, 546 paired questions. Subject-level Wilcoxon tests treat subject as the unit of inference. Effect sizes at this N have wide intervals; we report direction, panel sensitivity, and p-values rather than point estimates.
- Mem0 was used through the public API at standard rates. No fine-tuning, no provider-side optimization, no off-public-roadmap configuration. Controlled used `infer=False`; native used `infer=True` (the realistic deployment path).
- The pattern-frequency breakdown across all 507 questions × 5 systems requires per-response mechanism classification, flagged as future work in §7.
- The content-match rubric does not credit principled refusal where retrieved facts cannot ground a prediction (§3.3.6, §4.6.6). This affects Mem0's Pattern 3 cells (and every system's Pattern 3 cells) by under-weighting the specification's epistemic-honesty contribution.
- The 5-judge primary is the conservative aggregate. The 7-judge panel (adds Gemini Flash + Gemini Pro) widens Mem0's Δ_spec by roughly +0.05; direction does not flip.
- Retrieval-overlap is computed on a single fact pool and a single battery design (39 behavioral-prediction questions per subject, backward-designed from held-out corpora). The §4.6.3 battery sensitivity check shows the gradient slope holds across question-type composition; the cross-system Jaccard finding has not been replicated on a second battery generator.

## 12. Open questions for the Mem0 team

1. The native +0.21 lift on top of controlled is the largest of any system tested. We did not isolate which part of the native pipeline (chunking, `infer=True` reformulation, retrieval ranking, or a combination) produces it. Has internal evaluation pulled these apart?
2. Atomic-fact retrieval routes more responses into Pattern 1 on interpretation-heavy questions and more into Pattern 2 on literal-recall questions (§4.4.2, line 1297). Does Mem0 internally test per-question retrieval-strategy variants, or is the retrieval policy uniform across question shapes?
3. Mem0's recite rate among refusals is 62.5% (highest of four systems). Has this been observed in deployment, and does it correlate with downstream user behavior (e.g., follow-up turns, satisfaction signals)?
4. Cross-system retrieval overlap is 0.083 mean Jaccard, with Mem0 sitting at 0.105 mean across its 4 pairs (more consensus-aligned than Zep's 0.034). At what K (top-25, top-50, top-100) would you expect Mem0's retrieval to converge with the other systems on identical input?
5. Mem0's published LongMemEval (93.4) and LOCOMO (91.6) place Mem0 within a few percentage points of the other commercial systems. The retrieval-overlap finding suggests these benchmarks may be measuring something narrower than retrieval relevance in the wild. Has the Mem0 team explored where on a benchmark-vs-overlap matrix Mem0 sits (high recall, low overlap; or some other quadrant)?

---

Reproducibility pointers: per-judge per-subject Mem0 scores at `results/global_<subject>/mem0_judgments_<judge>.json` (controlled) and `mem0_fullpipeline_judgments_<judge>.json` (native). Retrieval overlap at `docs/research/retrieval_overlap_analysis_20260501.json`. Paired-delta arrays at `docs/research/per_system_anchor_crossing_20260427.json`. Pattern walkthrough at `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`. Per-question payloads available on request.
