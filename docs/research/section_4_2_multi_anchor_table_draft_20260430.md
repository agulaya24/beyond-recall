# §4.2 multi-anchor crossing table (replacement draft, v11.5)

Source data: `docs/research/multi_anchor_rates_all_pairs_20260430.json`
Script: `scripts/compute_anchor_crossing_all_pairs.py`
Aggregation: 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4); per-question 5-judge mean.

---

## Replacement text for §4.2 "What the aggregate numbers hide"

The small mean Δ values for spec-on-info-rich-context comparisons (C4a vs C4, C9 vs C8) are residues of substantial per-question movement in both directions. The same lens, applied to every relevant condition pair, makes the structural pattern visible: *multi-anchor crossings* (the strongest categorical signal the rubric detects, defined in §3.6.2) occur much more often when context is added on top of a no-context baseline than when the specification is layered on top of facts or raw corpus.

| Comparison | Subject set | n paired | Multi-anchor (≥2 bands) | Extreme (≥3 bands) | Mean Δ |
|---|---|---:|---:|---:|---:|
| C5 → C4a (full pipeline from baseline) | all 14 | 546 | 13.0% | 3.7% | +0.55 |
| C5 → C4 (facts only from baseline) | all 14 | 546 | 12.5% | 4.4% | +0.47 |
| C5 → C2a (spec only from baseline) | all 14 | 546 | 9.0% | 2.0% | +0.43 |
| C2c → C2a (correct vs wrong spec) | all 14 | 546 | 14.5% | 2.4% | +0.64 |
| C5 → C8 (raw corpus from baseline) | 13 (Babur excl.) | 507 | 15.4% | 4.3% | +0.59 |
| C5 → C9 (corpus + spec from baseline) | 13 (Babur excl.) | 507 | 14.8% | 4.7% | +0.62 |
| C4 → C4a (spec on top of facts) | all 14 | 546 | 2.2% | 0.9% | +0.08 |
| C8 → C9 (spec on top of corpus) | 13 (Babur excl.) | 507 | 2.4% | 0.4% | +0.03 |

The rate is largest for context-from-baseline comparisons (any condition that adds context to no-context C5 produces *multi-anchor crossings* at 9% to 15% of paired questions) and smallest for spec-on-top-of-information-rich-context comparisons (C4 → C4a at 2.2%, C8 → C9 at 2.4%). Read through the *anchor-crossing rule* (§3.6.2), this pattern is consistent with the §1 thesis: category-level moves are the strongest claim the rubric supports, and the specification produces the most of them where prior context is sparsest. Adding context from a no-context baseline shifts categorical bands on roughly 1 in 7 paired questions; layering the specification on top of facts or raw corpus shifts categorical bands on roughly 1 in 45. The extreme-jump (≥3 bands) row tracks the same gradient: 3% to 5% of questions on baseline-relative comparisons, under 1% on info-rich-relative comparisons.

The behaviorally meaningful unit is the per-question crossing, not the subject-mean Δ. Per-question phenomena, including the bimodal cancellation that produces near-zero aggregate Δ on spec-on-info-rich-context pairs, are decomposed in §4.4.2 (memory-system layering, where the *anchor-crossing rule* meets the question-routing taxonomy).

---

## Notes on subject set, methodology, and reconciliation

**All 14 main-study subjects are used** for any pair that does not involve C8 or C9. Babur is excluded *only* from C8/C9 pairs because the 422,772-word corpus exceeds the response model's context window when paired with the specification. Hamerton is included via the special judgments loader at `scripts/recompute_5judge_primary.py:load_hamerton_judgments`; the other 13 subjects load from `results/global_<subject>/judgments_v2.json` (or `c8_c9_judgments_merged.json` for C8/C9).

The §4.2 small-table previously reported C4a-vs-C4 multi-anchor at 2.6% and C9-vs-C8 at 3.8% on the 9-subject low-baseline slice (n=351 and n=312 respectively). Those numbers are the canonical *low-baseline* figures and reproduce from `compute_anchor_crossing_c4a_c4_and_c9_c8.py`. The all-14 numbers reported in the table above are 2.2% and 2.4%; the difference comes from including the 5 high-baseline subjects (Augustine, Equiano, Cellini, Rousseau, Zitkala-Sa), which have less room to cross anchors upward at the integer-band granularity.

The headline §4.2 table should report the all-14 numbers (the broader population) with a footnote pointing to the 9-subject low-baseline numbers and to `multi_anchor_rates_all_pairs_20260430.json` for per-pair detail and per-subject breakdowns.
