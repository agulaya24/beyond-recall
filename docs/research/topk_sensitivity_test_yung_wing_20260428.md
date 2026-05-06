# Top-K Retrieval Sensitivity Test (Yung Wing, Base Layer)

Date: 2026-04-28
Status: Research-only probe. Not part of paper. v11 paper unchanged.
Subject: Yung Wing (1 subject, N=39 BP questions)
Response model: Claude Haiku 4.5 (claude-haiku-4-5-20251001)
Judge panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54)

## Hypothesis

The paper's C1 (retrieval only) condition uses K=10 retrieval, returning roughly 500 tokens of context, while C2a (spec only) injects roughly 7,000 tokens of behavioral specification. The §4.4 additivity finding could in principle be partly attributable to spec adding more text to context rather than to its structural content. This probe sweeps K to test whether scaling retrieval volume closes the C3' (retrieval+spec) vs C1' (retrieval-only) gap.

## Summary

Three sentences:

1. The K=10 to K=140 sweep does NOT cleanly support the "spec gap is volume" hypothesis: Δ partially shrinks from +0.32 at K=10 to +0.20 at K=140, but the K=10 vs K=140 difference is not statistically significant (paired Wilcoxon p=0.235), and the trajectory is non-monotonic (drops to +0.06 at K=50, rebounds at K=140).
2. The cleanest finding is that C3' (spec+retrieval) sits flat at 2.45-2.50 across all three K values (paired Wilcoxon for K=10 vs K=140 p=0.82), consistent with the v10 §4.1 finding that spec performance has a uniform ceiling near 2.46 regardless of how facts are added underneath.
3. The intended size-match did not actually land: K=140 produced 2,782 tokens of retrieved-fact context, which is roughly 30% of the spec's roughly 9,200 tokens, so the test as run does not fully answer the original size-match question; full size-matching to spec would require K of roughly 350.

## Caveat on test design (read first)

The task brief estimated 50 tokens per fact, so K=140 was chosen as a rough size-match to a 7K-token spec. **Actual measurement: roughly 20 tokens per fact (Yung Wing fact corpus).** K=140 = 2,782 average context tokens, only roughly 30% of the spec's roughly 9,200 cl100k_base tokens. Yung Wing has 747 facts in pool, so a K of roughly 350 would be needed to fully size-match. This was not run.

What this test CAN say: at K=10 / K=50 / K=140, does C3' still beat C1' meaningfully?
What this test CANNOT say: whether at full spec-token-equivalent retrieval volume (K of roughly 350), C1' would close the gap.

## Per-K aggregates (5-judge primary, all judges 39/39 coverage)

| K | k_actual | Avg ctx tokens | C1' mean | C3' mean | Δ = C3' − C1' | Wilcoxon p (Δ vs 0) |
|---|---|---:|---:|---:|---:|---:|
| 10 | 10 | 183 | 2.185 | 2.503 | +0.318 | 0.024 |
| 50 | 50 | 971 | 2.395 | 2.451 | +0.056 | 0.347 |
| 140 | 140 | 2,782 | 2.282 | 2.482 | +0.200 | 0.136 |

Reference (canonical paper run, 5-judge primary, K=10): C1=2.231, C3=2.564, Δ=+0.333. Fresh K=10 reproduces within 0.05 / 0.06 / 0.02; pipeline-validation passes. Note: the canonical 5-judge primary had partial coverage on this subject (n_c1 = n_c3 = 117, vs. the fresh run's 195), so treat reproducibility as approximate, not exact.

Spec context: 36,793 chars / roughly 9,198 cl100k_base tokens.
Fact pool: 747 facts.

## Per-K movement breakdown (paired per-question 5-judge means, threshold ±0.10)

| K | Up (C3' > C1' + 0.1) | Down (C3' < C1' − 0.1) | None | Anchor crossing up (crosses 3.0) | Anchor crossing down |
|---|---:|---:|---:|---:|---:|
| 10 | 21 | 11 | 7 | 5 | 0 |
| 50 | 19 | 14 | 6 | 4 | 3 |
| 140 | 21 | 13 | 5 | 4 | 5 |

At K=10 the spec drove 5 questions across the 3.0 threshold and pushed 0 below it (clean asymmetric improvement). At K=50 and K=140 anchor crossings are bidirectional and roughly balanced, suggesting the spec is no longer differentially "rescuing" weak retrieval; it's mostly substituting in cases that were already at-ceiling for retrieval and degrading some cases.

## Cross-K paired tests

Paired Wilcoxon on per-question deltas across K values (n=39 each):

| Comparison | mean Δ_a | mean Δ_b | W | p |
|---|---:|---:|---:|---:|
| K=10 vs K=50 | +0.318 | +0.056 | 221.5 | **0.0497** |
| K=50 vs K=140 | +0.056 | +0.200 | 224.0 | 0.208 |
| K=10 vs K=140 | +0.318 | +0.200 | 305.0 | 0.235 |

Conclusion: only K=10 vs K=50 reaches conventional significance. K=10 vs K=140 is not distinguishable.

## C1' and C3' trajectories (paired tests)

| | mean change | p |
|---|---:|---:|
| C1' K=10 → K=50 | +0.210 | 0.203 |
| C1' K=50 → K=140 | −0.113 | 0.475 |
| C1' K=10 → K=140 | +0.097 | 0.382 |
| C3' K=10 → K=50 | −0.051 | 0.474 |
| C3' K=50 → K=140 | +0.031 | 0.651 |
| C3' K=10 → K=140 | −0.021 | 0.821 |

Two observations:

1. **C3' is essentially invariant across K.** All three paired tests fail to reject H0 with p ≥ 0.47. The 5-judge mean stays within a 0.05-point band (2.451 to 2.503). Spec performance does not depend on retrieval depth in this probe.
2. **C1' rises modestly from K=10 to K=50 then drops at K=140.** Neither change is statistically significant on its own. The mechanical reason Δ rebounds at K=140 is that the C1' point estimate fell back from 2.395 to 2.282 while C3' stayed at 2.482, but the C1' movement is within noise (p=0.475), so the rebound itself should not be over-interpreted. If the dip is real, distractor noise from low-similarity facts at the tail of K=140's neighbor set is one plausible mechanism worth probing in a follow-up.

## Saturation analysis

- C1' rises from 2.185 (K=10) to 2.395 (K=50), peaks there, then falls back to 2.282 (K=140). The K=50 peak is roughly +0.21 above K=10, the largest movement in the test.
- The roughly 5x increase in retrieval volume from K=10 (183 tokens) to K=50 (971 tokens) does most of the C1' work.
- The further roughly 3x to K=140 (2,782 tokens) does NOT increase C1'; it nudges it back down.
- C3' shows no meaningful trajectory across K. The spec already captures whatever signal is in the top retrieval slice; adding more facts at K=140 does not raise it.

## Interpretation (caveat: N=1 subject, single response model, undershot size-match)

Among the three framings the task brief proposed:

- **"Δ shrinks monotonically with K → spec was just compensating for low-K"**: not supported. Δ trajectory is V-shaped (+0.32 → +0.06 → +0.20). The K=50 minimum is statistically distinguishable from K=10 (p=0.05), but K=140 is not (p=0.23).
- **"Δ holds across K → spec is structural, not volume"**: partially supported, but with a key qualifier. C3' itself is provably flat (all p > 0.47). The C3' ceiling is robust to retrieval changes. The Δ is partially shrunk because C1' partially rises, but the spec's top-line score is not a function of how many facts sit underneath it.
- **"Δ widens → spec uses more facts as substrate"**: not supported. Δ does not widen at any K.

The most defensible read: the spec produces a ceiling near 2.46-2.50 that retrieval depth does not move. Retrieval-only performance is moderately responsive to K (peaks at K=50, ~5x context volume) but does not catch up to spec at the K values tested. Whether retrieval at K=350 (true size-match) would close the gap remains untested.

The K=10 anchor-crossing asymmetry (5 up, 0 down) is the cleanest qualitative finding: at K=10 the spec exclusively pushes weak-retrieval questions upward, and that asymmetry collapses at K=50 and K=140 (4-3, 4-5).

## Limits of this 1-subject probe

- N=39 questions on 1 subject (Yung Wing) with 1 response model (Haiku 4.5).
- The test undershot its intended size-match target by roughly 70%; conclusions about "what happens when retrieval is volume-equivalent to spec" are not available from this run.
- Yung Wing is a mid-baseline subject with visible Δ at K=10. Behavior may differ on subjects with higher (Franklin-like) or lower (Hamerton-like) baselines.
- Memory systems whose retrieval architectures differ from Base Layer's MiniLM-L6-v2 + ChromaDB cosine (Mem0 graph-aware, Letta archival, Supermemory hybrid, Zep entity-graph) would likely show different K-curves; do not extrapolate.
- 5-judge primary excludes gemini judges; numbers are not directly comparable to 7-judge sensitivity panel in the paper.
- This probe does not address pipeline variance (a subject-level rerun-rerun probe would be needed to bound noise on individual K cells; v10 §6.3 estimates pooled SD ~0.10).

## Suggested follow-up (NOT run)

- **True size-match: K=350 on Yung Wing.** This would put retrieved-fact context at roughly 7,000 tokens, matching the spec's roughly 9,200 tokens (within roughly 75%). Yung Wing's 747-fact pool supports this. The script is already parameterized; estimated runtime roughly 30 min and cost roughly USD 2. This is the most direct follow-up to actually answer the original size-match hypothesis.
- Width: same K sweep on a low-baseline subject (e.g., Sunity Devee, baseline 1.03) and a mid-baseline subject (e.g., Cellini) to test whether the C3' ceiling sits at 2.46 regardless of subject baseline.
- Cross-system: same K sweep with Mem0 / Letta to test whether the result is Base-Layer-retriever-specific or general.

## Raw data and scripts

- Script (parameterized K): `scripts/_topk_sensitivity_test.py`
- Aggregation: `scripts/_topk_aggregate.py`
- Stats: `scripts/_topk_stats.py`
- K=10 retrieval: `data/topk_test_20260428/yung_wing_K10_retrieval.json`
- K=10 results: `data/topk_test_20260428/yung_wing_K10_results.json`
- K=10 judgments: `data/topk_test_20260428/yung_wing_K10_judgments.json`
- K=50 retrieval / results / judgments: `data/topk_test_20260428/yung_wing_K50_*.json`
- K=140 retrieval / results / judgments: `data/topk_test_20260428/yung_wing_K140_*.json`
- Aggregate summary: `data/topk_test_20260428/_summary.json`
- Stats output: `data/topk_test_20260428/_stats.json`

## Reproducibility

```
python scripts/_topk_sensitivity_test.py --k 10 --phase all
python scripts/_topk_sensitivity_test.py --k 50 --phase all
python scripts/_topk_sensitivity_test.py --k 140 --phase all
python scripts/_topk_aggregate.py
python scripts/_topk_stats.py
```

Total wall time: roughly 30 minutes (3 generation runs in parallel + 3 sequential 5-judge passes).
Total API spend (Anthropic + OpenAI): under USD 5 (234 generation calls + 1170 judge calls; most calls under 1K tokens).
