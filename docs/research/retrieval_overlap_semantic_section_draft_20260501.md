# §4.4.1 sensitivity insertion: soft-Jaccard cross-system retrieval overlap

Status: draft for §4.4.1, after the existing exact-Jaccard table and accompanying prose.
Generated 2026-05-01 from `scripts/analyze_retrieval_overlap_semantic.py`.
Data: `docs/research/retrieval_overlap_semantic_20260501.json`.
Purpose: stress-test the divergence claim under semantic-similarity matching, varying threshold and K.

---

## Headline answer

Semantic-similarity matching does not change the conclusion. Across 14 subjects and 546 behavioral-prediction questions, soft Jaccard (cosine-similarity match between fact embeddings, symmetrized over A→B and B→A directions) raises the controlled-config mean only marginally and only at thresholds loose enough to capture topical adjacency rather than referential identity. At the calibrated near-duplicate threshold (cosine ≥ 0.85, the same threshold the Letta semantic-duplication study uses to flag near-paraphrases) mean pairwise soft Jaccard at K=10 is 0.102, against an exact-set baseline of 0.083. At the verbatim-paraphrase threshold (≥ 0.95) it is 0.093. Even at the loosest threshold tested (≥ 0.70, where the metric is no longer measuring "the same fact" so much as "facts about the same topic") the mean only reaches 0.191. None of the tested cells crosses 0.30, let alone 0.50 or 0.70. Providers do not converge on which facts are most relevant under any defensible reading of "match."

## Cleanest single-number sensitivity statement for §4.4.1

> Relaxing the match criterion from exact set identity to cosine similarity ≥ 0.85 raises mean pairwise Jaccard at K=10 from 0.083 to 0.102 across ten controlled-config pairs (14 subjects, 546 questions). The margin compresses further at the verbatim-paraphrase threshold (≥ 0.95: 0.093) and never crosses 0.30 even at a loose topical threshold (≥ 0.70: 0.191). Native-pipeline soft Jaccard at the same thresholds remains effectively zero (0.004 at ≥ 0.85, 0.016 at ≥ 0.70).

## Sensitivity grid (mean soft Jaccard across pairs)

| Config     | K    | T=0.95 | T=0.90 | T=0.85 | T=0.80 | T=0.70 |
|------------|------|--------|--------|--------|--------|--------|
| controlled | 5    | 0.089  | 0.093  | 0.097  | 0.104  | 0.173  |
| controlled | 10   | 0.093  | 0.097  | 0.102  | 0.110  | 0.191  |
| controlled | all  | 0.093  | 0.097  | 0.102  | 0.110  | 0.191  |
| native     | 5    | 0.001  | 0.002  | 0.004  | 0.004  | 0.013  |
| native     | 10   | 0.001  | 0.002  | 0.004  | 0.005  | 0.016  |
| native     | all  | 0.001  | 0.002  | 0.004  | 0.005  | 0.016  |

K=all is identical to K=10 in the controlled config because every system returns at most ten facts. The K=5 column shows that truncating to top-5 lowers soft Jaccard by 5–10% relative across thresholds rather than raising it. Smaller K does not surface a hidden agreement at the very top of each ranking; it slightly amplifies the disagreement, consistent with each system putting different items first.

## Prose for §4.4.1 insertion

Soft-match overlap is monotonic in threshold and produces no surprise. Relaxing match identity from exact strings to cosine similarity ≥ 0.85 (the calibrated near-duplicate threshold from the Letta semantic-duplication analysis in Appendix G) raises mean pairwise Jaccard at K=10 from 0.083 to 0.102 across the ten controlled-config pairs and 546 behavioral-prediction questions. At the verbatim-paraphrase threshold (≥ 0.95) the figure is 0.093, slightly above exact match because the controlled all-facts pool contains a small number of duplicate-but-not-identical strings the literal-set check missed. At a loose topical threshold (≥ 0.70, where two facts share a theme but not a referent), the mean only reaches 0.191. None of the tested cells crosses the 0.30 mark at which "the systems converge under semantic match" would become a defensible reading.

Truncating to K=5 lowers soft Jaccard slightly across all thresholds (0.097 at T=0.85 vs. 0.102 at K=10). Smaller K does not surface a hidden top-ranked agreement; it amplifies the observed disagreement, consistent with each provider placing different items first.

The native-pipeline configuration is more striking. Even at the loosest threshold (≥ 0.70), mean pairwise soft Jaccard across the four native systems and six pairs is 0.016. At calibrated thresholds it is effectively zero (0.004 at ≥ 0.85, 0.001 at ≥ 0.95). Native retrievals return heterogeneous objects (Mem0 third-person summary sentences, Letta raw multi-sentence book passages, Supermemory atomic facts, Zep graph rows), so neither exact nor semantic match recovers shared content across them. The controlled configuration is the cleaner test, and it survives.

This connects to the §4.4.2 patterns. Interpretive supply, over-theorization, and spec-induced refusal each emerge in part from this retrieval divergence: when the same question routes to different evidentiary substrates, the downstream reading model has different material to interpret before any judgment-level differences enter. Soft matching does not fix that, because the divergence is not a surface-form artifact. Each provider's ranking algorithm encodes its own theory of what counts as relevant, and those theories produce nearly disjoint top-Ks even under generous similarity tolerances. Recall benchmarks measure recall, and that is what they should measure. The point of this sensitivity check is narrower: representational accuracy operates downstream of retrieval, at the layer where the system decides what a fact means for the person being modeled, and the layer below it does not deliver the same starting material to two providers given the same input.
