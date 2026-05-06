# Judge Floor Test (P0-17)

_8 diagnostics × 5 wrong-answer variants × 5 judges_

**Expected:** all variants score near 1. Any judge that systematically scores > 1.5 across all variants has a floor-leak; that's a known calibration gap.

## Per-judge overall mean on wrong answers

| Judge | n | mean | std | pct ≤ 1.5 | pct ≤ 2.5 |
|---|---:|---:|---:|---:|---:|
| haiku ⚠ | 40 | 2.17 | 1.02 | 20% | 82% |
| sonnet ⚠ | 40 | 1.75 | 0.70 | 38% | 90% |
| opus ⚠ | 40 | 2.15 | 0.82 | 22% | 68% |
| gpt4o ⚠ | 40 | 2.38 | 0.62 | 5% | 60% |
| gpt54 ⚠ | 40 | 2.12 | 0.75 | 12% | 85% |

## Per-judge × variant mean

| Judge | wrong_factual | wrong_direction | topically_adjacent | off_topic_generic | plausible_unsupported |
|---|---|---|---|---|---|
| haiku | 1.75 ⚠ | 1.50 | 2.50 ⚠ | 2.50 ⚠ | 2.62 ⚠ |
| sonnet | 1.75 ⚠ | 1.50 | 1.88 ⚠ | 1.12 | 2.50 ⚠ |
| opus | 2.00 ⚠ | 1.50 | 2.25 ⚠ | 1.88 ⚠ | 3.12 ⚠ |
| gpt4o | 1.88 ⚠ | 1.88 ⚠ | 2.50 ⚠ | 2.88 ⚠ | 2.75 ⚠ |
| gpt54 | 1.88 ⚠ | 1.75 ⚠ | 2.12 ⚠ | 2.12 ⚠ | 2.75 ⚠ |

## Which variants leak the floor the most?

| Variant | mean across 5 judges | max judge mean | worst judge |
|---|---:|---:|---|
| wrong_factual | 1.85 | 2.00 | opus |
| wrong_direction | 1.62 | 1.88 | gpt4o |
| topically_adjacent | 2.25 | 2.50 | haiku |
| off_topic_generic | 2.10 | 2.88 | gpt4o |
| plausible_unsupported | 2.75 | 3.12 | opus |

## Recommendation

Judges with **floor leakage** (mean > 1.5 on wrong-answer variants):
- **gpt4o** mean 2.38
- **haiku** mean 2.17
- **opus** mean 2.15
- **gpt54** mean 2.12
- **sonnet** mean 1.75

Tight-at-floor judges: none.

If floor leakage is concentrated in `plausible_unsupported` or `topically_adjacent` variants, the 5-judge aggregate may under-rank wrong predictions that hedge or gesture plausibly. Consider either down-weighting the leaky judge or adding a rubric clarification that `1` is the correct score for any response that does not identify a held-out-consistent outcome.
