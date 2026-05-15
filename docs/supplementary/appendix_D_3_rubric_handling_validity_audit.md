# Appendix D.3 — Rubric-handling validity audit (full report)

*Mirrored from beyond_recall_v11.9.1. Body summary in §4.6.7.*

---

### D.3 Rubric-handling validity audit (full report)

This audit is the formal report that §3.3.6 summarizes. It was produced by `scripts/audit_low_end_inflation.py`. Raw flagged cases live in `docs/research/s114_low_end_inflation_audit.json`; source response and judgment data are under `results/global_<subject>/`. The audit is restricted to the 9 low-baseline subjects (1,599 responses across C5, C2a, C2c, C4, C4a conditions).

**D.3.1 Abstention detection.**

Abstention patterns were matched by regular expression against response text. Pattern list includes variants of "I don't have specific information," "there is no explicit documented," "I cannot confirm," "I am not certain," "would need additional context," "my training data does not," and related phrasings. Full pattern list in `scripts/audit_low_end_inflation.py` lines 29-42. 192 of 1,599 low-baseline responses (12.0%) matched one or more abstention patterns.

**D.3.2 Score distribution of abstention-matching responses.**

The rubric's lowest anchor is "refuses or off-base." An honest refusal should score at or below 1.5 (closer to rubric-1 than to rubric-2). The distribution of 5-judge primary means over the 192 abstention-matching responses:

| 5-judge primary anchor | Count | % of abstentions |
|---:|---:|---:|
| 1.0 to 1.5 | 159 | 82.8% |
| 1.5 to 2.0 | 15 | 7.8% |
| 2.0 to 2.5 | 12 | 6.3% |
| 2.5 to 3.0 | 2 | 1.0% |
| 3.0 to 3.5 | 2 | 1.0% |
| 3.5 and above | 2 | 1.0% |

82.8% of abstentions score in the expected anchor. 18 of 192 abstentions (9.4%) score at or above 2.0, and 6 of 192 (3.2%) score at or above 3.0. Mean abstention score: 1.27 (expected: close to 1.0). Under a clean rubric these would all be closer to 1.0; the over-credit reflects judges giving partial marks for adjacent-fact recitation or for correctly identifying what the context does not contain.

**D.3.3 Per-judge strictness on abstention-matching responses.**

Primary 5-judge panel only. Mean score on the 192 abstention-matching responses:

| Judge | Mean on abstentions |
|---|---:|
| Sonnet 4.6 | 1.14 |
| GPT-5.4 | 1.17 |
| Haiku 4.5 | 1.29 |
| GPT-4o | 1.34 |
| Opus 4.6 | 1.41 |

Spread: 0.27 points between strictest (Sonnet) and most lenient (Opus). No judge reaches the rubric-1 floor on average. The 5-judge primary average (1.27) smooths this cross-judge variance without eliminating it.

**D.3.4 Length-score correlation.**

Pearson correlation between response length (character count) and 5-judge primary score, across the 1,599 low-baseline responses:

| Slice | n | r | Interpretation |
|---|---:|---:|---|
| All responses | 1,599 | 0.26 | Modest positive, driven almost entirely by C5. |
| C5 (baseline, no context) | 312 | 0.604 | Strong positive. Longer baseline responses score higher. |
| C2a (Spec only) | 351 | 0.14 | Near zero. |
| C4 (facts alone) | 312 | 0.01 | Zero. |
| C4a (facts plus Spec) | 312 | −0.01 | Zero. |
| C2c (wrong Spec) | 312 | 0.500 | Strong positive. Wrong-Spec responses resemble C5 on the length-score axis. |

The effect is strongest in C5 (r = 0.604) and recurs, attenuated, in C2c (r = 0.500). Both are conditions without a ground-truth representation of the subject: C5 has no context at all, and C2c has a randomly-drawn other subject's specification. In both, longer responses (containing hedging, adjacent-fact recitation, disambiguation offers) score higher than short refusals. Conditions that do carry a correct specification (C2a, C4, C4a) show near-zero length correlation. The direction of the bias pushes the measured C5 and C2c means upward, which shrinks the measured Spec-vs-no-Spec gap relative to the true gap. That the length signal persists in C2c, but not in C2a or C4a, is the cleanest evidence that length inflation is a property of the baseline-scoring regime rather than of any specific condition: when judges cannot verify against a correct representation, they partial-credit verbose output.

**D.3.5 Ultra-high-score validity.**

Ultra-high responses are those scoring 4.5 or above on the 5-judge primary. Length comparison:

| Response class | Mean length (chars) | Notes |
|---|---:|---|
| Ultra-high (score 4.5 or above) | 2,790 | Not length-inflated. |
| Mid-range (2.5 to 3.5) | 2,829 | Baseline comparison. |
| Low (score below 2.0) | 2,087 | n = 795. Shorter than both ultra-high and mid-range; confirms length inflation is a low-end partial-credit phenomenon, not a high-end one. |

Ultra-high responses are not longer than mid-range responses. Length inflation is a low-end phenomenon, not a universal one. The hypothesis that "ultra-high responses equal length-inflated responses" is rejected by this comparison.

**D.3.6 Implications for reported effects.**

Both rubric-handling effects (abstention over-credit at the low end, length inflation in C5) pull the measured C5 baseline upward. This shrinks the measured Spec-vs-baseline gap. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift reported in §4.1. The paper reports the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact. A differentiated rubric that scores abstention as its own dimension, and a length-controlled scoring protocol, are both flagged as follow-up in §7.

