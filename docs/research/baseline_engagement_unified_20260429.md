# §4.X When the C5 baseline engages, when it abstains, and what it costs to score

*Companion data: `docs/research/baseline_engagement_analysis_20260429.json`, `docs/research/abstention_extensions_analysis_20260429.json`. Reproducibility scripts: `scripts/analyze_baseline_engagement.py`, `scripts/analyze_abstention_extensions.py`.*

## Lede

The C5 baseline is not one number per subject. Pooled across 546 prediction-tier questions on 14 main-study subjects (5-judge primary panel), the per-question baseline is *bimodal*: roughly 41% of questions land in *refusal* (mean = 1.00), roughly 21% engage substantively (mean ≥ 3.0), and the middle is thin. The spec's lift inverts cleanly with this baseline: where the model already engages, lift collapses or turns negative; where the model abstains, lift is reliably large and positive. *Abstention itself is not score-neutral.* The judge panel rewards different kinds of abstention at different rates depending on response model and retrieval condition. Together these phenomena give a per-question view of where the +0.89 mean Δ headline in §4.1 comes from.

## C5 baseline distribution across questions

Each question is binned by its C5 mean across the 5-judge primary panel: *REFUSE* (mean = 1.00), *MARGINAL* (1.00 < mean < 2.0), *GENERIC* (2.0 ≤ mean < 3.0), *ENGAGED* (3.0 ≤ mean < 4.0), *STRONG* (mean ≥ 4.0).

| Bin | N (of 546) | Share | Mean Δ_C4a (lift) | SD | Positive lift |
|---|---:|---:|---:|---:|---:|
| REFUSE (c5 = 1.00) | 225 | 41.2% | +1.32 | 0.88 | 94.2% |
| MARGINAL (1 < c5 < 2) | 110 | 20.1% | +0.66 | 0.83 | 78.2% |
| GENERIC (2 ≤ c5 < 3) | 95 | 17.4% | +0.04 | 0.63 | 39.0% |
| ENGAGED (3 ≤ c5 < 4) | 82 | 15.0% | −0.47 | 0.81 | 25.6% |
| STRONG (c5 ≥ 4) | 34 | 6.2% | −0.99 | 0.78 | 8.8% |

Per-subject distributions match the §4.1 gradient. Sunity Devee and Ebers sit at the floor (37 of 39 and 36 of 39 questions in REFUSE). Equiano sits at the high end (2 of 39 in REFUSE, 5 in STRONG). Even Augustine, the highest-baseline subject in the gradient, has 8 of 39 questions in REFUSE. The bimodality is *within-subject*, not just across subjects.

## What predicts engagement: training-data depth, not naming alone

Each question was tagged for naming label (FULL, PARTIAL, NONE):

| Naming | N | Mean C5 | C5 ≥ 2 rate | C5 ≥ 3 rate |
|---|---:|---:|---:|---:|
| FULL | 183 | 2.18 | 50.8% | 29.0% |
| PARTIAL | 272 | 1.93 | 41.2% | 22.4% |
| NONE | 91 | 1.19 | 6.6% | 2.2% |

Pooled rates conflate naming with subject mix (NONE-named questions cluster on low-baseline subjects). The cleanest within-subject test is Yung Wing: every one of his 39 questions names him in full, his C5 mean is 1.88, yet 16 still land in REFUSE while 7 reach ENGAGED or STRONG. A representative REFUSE response on Q4:

> *I don't have specific information about Yung Wing's management style or approach to delegating technical decisions to subordinates. Yung Wing (1818-1912) was a Chinese educational reformer and diplomat...*

The model knows *who* Yung Wing is. It abstains on the specific behavioral pattern. Q23 (how he reasons in negotiations) returns C5 = 4.4 on the same battery, naming and dates constant. The variance is in whether the asked-about pattern was attested in pretraining, not in surface phrasing. Cellini Q2 names only the surname yet returns C5 = 4.6 because the Castel Sant'Angelo escape is canonical; eight FULL-named Mary Seacole questions about Crimea-era resourcefulness, espionage accusations, mourning rituals, or religious art appreciation all return C5 = 1.00.

*Full canonical naming is necessary but not sufficient for baseline engagement. The differentiator is training-data depth on the specific behavioral pattern, not on the identity.*

## Spec lift inverts with baseline engagement

Pooled across 546 questions, Spearman ρ between C5 baseline and C4a − C5 lift is **−0.73, p ≈ 1.7 × 10⁻⁹¹** (n = 546). Per-subject ρ is negative for 14 of 14 subjects; 12 of 14 reach p < 0.01. The two non-significant subjects (Sunity Devee, Ebers) sit at the REFUSE floor and have almost no within-subject baseline variance to correlate against. A Mann-Whitney test on lift in REFUSE (n = 225) versus ENGAGED-or-STRONG (n = 116) gives means +1.32 and −0.62, U = 24,886, p ≈ 5.5 × 10⁻⁴³.

The spec's value concentrates on deep-cut behavioral patterns that did not surface in canonical biographical summaries. Where the model already has the pattern, the spec adds little or actively interferes; the C4a ceiling near 2.46 from §4.1 is consistent (once a question crosses out of REFUSE, marginal contribution shrinks). Memory-system retrieval that surfaces only identifying biographical facts does not move the needle on prediction tasks for the same reason: it disambiguates *who* without supplying the interpretive depth the question requires.

## Worked rubric example: Seacole Q2 across condition bands

Mary Seacole Q2: *Based on Mary's character, would she comfort a delirious soldier who mistakes her for his wife?* Held-out: *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."* The 5-judge primary panel scores five conditions on this question across four rubric bands (band 3 was not observed here).

| Band | Definition (from §3.6) |
|---:|---|
| 1 | Refusal or non-answer. |
| 2 | Generic, pattern-free; could apply to many subjects. |
| 3 | Subject-specific behavioral tendency identified. |
| 4 | Multiple behavioral dimensions together. |
| 5 | Closely matches the held-out behavioral pattern. |

| Condition | Mean | Band | Excerpt (verbatim) |
|---|---:|---:|---|
| C2c_wrong_spec (Babur spec) | 1.40 | 1 | "Mary would **not sustain the deception**, but she would **not abandon the soldier either**. ... She would correct him — gently, but directly ... allowing him to die in a false belief violates her epistemic obligation." |
| C5_baseline | 1.80 | 1 | "I'd need to know which Mary you're referring to. There are many famous Marys in literature, history, and other works. Could you provide more context?" |
| C4_factdump | 2.80 | 2 | "Based on the extensive facts about Mary's character, **yes, she would absolutely comfort such a soldier** ... Mary would likely gently accept the soldier's confusion while providing comfort..." |
| C2a_full_spec | 4.20 | 4 | "Yes, she would comfort him. But not by correcting him. ... She would *not* say 'I am your wife' or sustain the delusion. ... Stay present. Touch him. Speak to the need beneath the confusion." |
| C4a_full_facts_plus_spec | 5.00 | 5 | "Yes, absolutely ... She would **accept the mistake without correcting it**, not out of deception, but out of A8 (Sympathetic Realism). She understands that his delusion is a mercy, a refuge his mind has built to survive unbearable pain." |

The example traces the *cross-anchor interpretation rule* of §3.6.2 on a single question. C5 declines for lack of referent; C2c (a Babur spec) is articulate but mis-applied. C4 with raw facts reaches a generic affirmative. C2a, working from the full spec without retrieved facts, produces an internally articulate multi-dimensional answer about presence and tenderness but lands on a *less specific* prediction about whether Mary would correct him. C4a, with both facts and spec, explicitly endorses non-correction; the held-out shows Mary chose not to undeceive him, and C4a matches that direction outright while C2a is less clear on it. Categorical movement from band 1 through band 5 on a single question is what the per-subject means in §4.1 aggregate.

## Per-response-model abstention behavior

The 9.4% / 3.1% pooled abstention over-credit in §3.6.6 averages over three response models. Disaggregating along that axis (abstention identified by 27-marker regex):

| Response model | N | Abstain rate | Mean abstain score | % ≥ 2.0 |
|---|---:|---:|---:|---:|
| Claude Haiku 4.5 (main study) | 13,380 | 7.5% | 1.38 | 14.3% |
| Claude Sonnet 4.6 (Tier 2) | 468 | 21.2% | 1.62 | 26.3% |
| Gemini 2.5 Pro (Tier 2) | 420 | 0.5% | 2.63 | 100.0% |

Sonnet 4.6 abstains at roughly three times Haiku's rate and the panel rewards its abstentions nearly twice as often (26.3% ≥ 2.0 vs. 14.3% ≥ 2.0); mean abstain score is 0.24 anchor points higher. Sonnet's hedged abstentions tend to recite plausible behavioral framings before disclaiming, and the panel scores the framing rather than the disclaimer. Gemini 2.5 Pro almost never abstains by these markers (n = 2); its row is for completeness only.

*Haiku 4.5, the main-study response model, is the lowest over-credit case.* The §3.6.6 pooled 9.4% / 3.1% number is therefore a *floor*, not a worst case; stronger response models that hedge more elaborately extract more lift from the panel's reluctance to score abstentions at 1.0.

## Memory-system effect on abstention

Memory-system conditions retrieve facts and prepend them as context. The hypothesis was that responses *reciting* the retrieved facts (refusing in substance, but visibly engaging with the retrieval payload) would score higher than pure C5 refusals.

| Cell | Definition | N | Mean | % ≥ 2.0 |
|---|---|---:|---:|---:|
| Pure C5 refusal | no facts, no retrieval | 292 | 1.26 | 10.3% |
| C4 factdump refusal | facts in context, no retrieval | 20 | 1.33 | 10.0% |
| Memory-system refusal + recitation | refuses *and* quotes retrieved n-gram | 148 | 1.50 | 18.2% |
| Memory-system refusal, no recitation | refuses, no quote | 240 | 1.47 | 17.1% |
| Memory-system substantive engagement | non-refusal | 7,835 | 2.32 | 67.2% |

| Comparison | Δ | 95% CI | p (Welch) |
|---|---:|---|---:|
| Mem-refuse + recite vs. pure C5 refuse | +0.234 | [+0.113, +0.355] | 0.0002 |
| Mem-refuse no recite vs. pure C5 refuse | +0.206 | [+0.103, +0.310] | 0.0001 |
| Mem-refuse + recite vs. mem-refuse no recite | +0.027 | [−0.098, +0.153] | 0.67 |

Memory-system refusals score +0.21 to +0.23 anchor points higher than pure C5 refusals, and that lift is essentially the same whether or not the response recites a retrieved n-gram. The C4 factdump cell (n = 20) is underpowered but consistent: facts in context without retrieval inflate refusal scores by only +0.07. The §3.6.6 over-credit is therefore *not* a "judges reward the visible quote" effect; it is a "judges reward the retrieval condition" effect regardless of whether retrieved tokens surface in the response. Either judges infer that retrieval-conditioned answers are more grounded even when abstaining, or abstention text in retrieval conditions is systematically less terse and the panel scores the framing.

## Implication and limitations

The +0.89 mean Δ_C4a headline in §4.1 averages over a per-question structure that is itself uneven. On the 41.2% of questions where the baseline abstains, mean lift is +1.32 and 94.2% of lifts are positive. On the 21.2% where the baseline already engages, mean lift is negative. The headline is a true population-level summary, but its mechanism is concentrated. The active human population for whom AI personalization matters is the population for whom most behavioral prediction questions sit in the REFUSE bin, and that is precisely where the spec is reliably useful. The §1.3 framing ("AI never knew, not AI forgot") holds at the per-question level, not just the per-subject level.

Two limitations bound the abstention reading. The REFUSE bin is not a clean abstention category: roughly 7% of REFUSE-bin C5 responses are wrong-but-confident substantive predictions rather than honest refusals, so the +1.32 REFUSE-bin lift mixes *spec corrects abstention* with *spec corrects confident error*. Both are gains in representational accuracy but imply different deployment behaviors. Separately, the Sonnet 4.6 over-credit rate (almost twice Haiku's) means future replication on a stronger response model should expect the abstention floor of §3.6.6 to widen before mitigations are applied. Both are flagged in §6.2.
