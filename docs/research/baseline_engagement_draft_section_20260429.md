# §4.x When does the C5 baseline engage vs. abstain?

*Draft for v11.2. Style follows v11 conventions: italics for emphasis, no em-dashes in prose, mean Δ as the primary evaluation metric. Companion data file: `docs/research/baseline_engagement_analysis_20260429.json`. Reproducibility script: `scripts/analyze_baseline_engagement.py`.*

## What this subsection answers

Treating the C5 baseline as a single per-subject number obscures its structure. Pooled across 546 questions on 14 main-study subjects (39 prediction-tier questions per subject, 5-judge primary panel), the per-question C5 distribution is *bimodal*. On 41.2 percent of questions the model abstains entirely (mean of 5 primary judges = 1.00); on 21.2 percent it engages substantively (mean ≥ 3.0). The middle band is thin. Where the baseline abstains, the spec produces large positive lift; where the baseline already engages, the spec lift collapses and frequently turns negative. This is data-grounded support for the v11 framing in §1.3 ("the AI never knew, not the AI forgot"): the spec's value is concentrated on the behavioral patterns that the model's pretraining did not encode.

## Per-question bin distribution across 14 subjects

We bin each question by its C5 baseline mean: REFUSE (= 1.00), MARGINAL (1.00 < c5 < 2.0), GENERIC (2.0 ≤ c5 < 3.0), ENGAGED (3.0 ≤ c5 < 4.0), STRONG (c5 ≥ 4.0).

| Bin | N (of 546) | Share | Mean lift Δ_C4a | SD lift | % positive lift |
|---|---:|---:|---:|---:|---:|
| REFUSE (c5 = 1.00) | 225 | 41.2% | **+1.32** | 0.88 | 94.2% |
| MARGINAL (1 < c5 < 2) | 110 | 20.1% | +0.66 | 0.83 | 78.2% |
| GENERIC (2 ≤ c5 < 3) | 95 | 17.4% | +0.04 | 0.63 | 39.0% |
| ENGAGED (3 ≤ c5 < 4) | 82 | 15.0% | −0.47 | 0.81 | 25.6% |
| STRONG (c5 ≥ 4) | 34 | 6.2% | **−0.99** | 0.78 | 8.8% |

Per-subject distributions match the v11 §4.1 gradient (lower-baseline subjects are REFUSE-heavy; higher-baseline subjects retain a substantial REFUSE tail). Sunity Devee and Ebers sit at the floor (37 of 39 and 36 of 39 questions in REFUSE, respectively). Equiano sits at the top of the C5 range (only 2 of 39 in REFUSE, 5 in STRONG). Even Augustine, the highest-baseline subject in the gradient, has 8 of 39 questions in REFUSE: the bimodality is *within-subject*, not just across subjects.

## What predicts engagement: training-data depth, not naming

We tagged each question for two surface features that might modulate baseline engagement:
1. *Naming label*: does the question text contain the subject's full canonical name (FULL), only a first or last name (PARTIAL), or no name at all (NONE)?
2. *Disambiguator*: does the question text contain a place, profession, era, or work-title keyword that fixes the referent (e.g., "Crimea" for Seacole, "Mughal" for Babur)?

Naming has a measurable association with engagement, but it is not the differentiator the user hypothesis predicted.

| Naming label | N | Mean C5 | Engaged rate (C5 ≥ 2) | Strong rate (C5 ≥ 3) |
|---|---:|---:|---:|---:|
| FULL | 183 | 2.18 | 50.8% | 29.0% |
| PARTIAL | 272 | 1.93 | 41.2% | 22.4% |
| NONE | 91 | 1.19 | 6.6% | 2.2% |

These pooled rates conflate naming with subject mix: NONE-named questions cluster on the low-baseline subjects whose batteries skew refuse-heavy regardless of phrasing. The within-subject test below (Yung Wing) is the cleaner isolation, holding subject identity constant.

Two patterns matter. *First*, NONE-named questions almost never engage (6.6%). This is what the model's behavior naively predicts: with no referent at all, it has nothing to retrieve. *Second*, full naming does not guarantee engagement. 38 of 183 FULL-named questions land in REFUSE (20.8%). The model is given the canonical name and still abstains.

The clearest within-subject test is Yung Wing. He has C5 mean 1.88, one of the lowest in the gradient. Yet 16 of his 39 questions are REFUSE (his name appears in full in every question), and 7 are ENGAGED or STRONG. The REFUSE responses look like this (Q4):

> *I don't have specific information about Yung Wing's management style or approach to delegating technical decisions to subordinates. Yung Wing (1818-1912) was a Chinese educational reformer and diplomat, best known for establishing the Chinese Educational Mission that sent Chinese students to study...*

The model knows *who* Yung Wing is. It abstains on the *behavioral pattern* the question asks about. Q23 (about how he reasons in negotiations) gets C5 mean 4.4. The naming, disambiguators, and dates are constant across his battery; the variance is in whether the specific behavioral pattern was attested in his pretraining sources.

The same pattern shows up on the partial-naming side. Cellini Q2 ("When faced with confinement or restriction, what is Cellini's likely course of action?") names only the surname yet returns C5 = 4.6, because Cellini's escape from Castel Sant'Angelo is canonical. Hamerton Q21 anchors itself in chapter numbers rather than disambiguating biography ("his deep attachment to the countryside and his distaste for towns shown in chapters 1-10") and returns C5 = 4.2 because Hamerton's autobiography is unusually well-represented in pretraining. Conversely, eight FULL-named "Mary Seacole" questions about Crimea-era resourcefulness, espionage accusation, mourning rituals, or religious art appreciation all return C5 = 1.00. Naming and disambiguators are present; the *pattern* is not.

## Lift correlates negatively with baseline engagement

Pooled across all 546 questions, the rank correlation between C5 baseline and the C4a − C5 lift is Spearman ρ = **−0.73, p ≈ 1.7 × 10⁻⁹¹** (n = 546). Per-subject Spearman ρ is negative for 14 of 14 subjects; 12 of 14 reach p < 0.01. The two non-significant subjects (Sunity Devee ρ = −0.24, p = 0.15; Ebers ρ = −0.15, p = 0.36) are the two lowest-baseline subjects in the gradient, where C5 has almost no within-subject variance to correlate against.

A within-question Mann-Whitney U test on lift in REFUSE (n = 225) versus ENGAGED-or-STRONG (n = 116) gives mean lift +1.32 vs. −0.62, U = 24,886, p ≈ 5.5 × 10⁻⁴³. The spec's effect on a question reverses sign once the model already knows the pattern.

## Implication

The spec's value is concentrated on *deep-cut* behavioral patterns, the ones that did not surface in canonical biographical summaries. Where the model has the pattern, the spec adds little or actively interferes; where the model abstains, the spec is reliably positive (94.2% of REFUSE-bin questions show positive lift, mean +1.32). This is a sharper version of the v11 §1.3 thesis. It also explains the gradient of v11 §4.1 mechanically: low-baseline subjects are simply the ones whose batteries skew toward REFUSE-bin questions, and the spec's per-question lift on those questions is uniformly large. The C4a ceiling near 2.46 reported in §4.1 (coupling-free reframing) is consistent with this reading: once a question crosses out of REFUSE, the spec's marginal contribution shrinks.

The naming finding adds a second-order point: providing a full canonical name is *necessary but not sufficient* for engagement. The model needs to have encoded the specific behavioral pattern, not just the identity. This is part of why memory-system retrieval that surfaces only identifying biographical facts (D-O-B, profession, location) does not move the needle on prediction tasks: it disambiguates *who* without supplying the interpretive depth the question requires.

## Methodological caveat: REFUSE = abstention, not always

The bin definition collapses two phenomena that v11 §3.6.6 already flags. We classified the C5 response text for all 225 REFUSE-bin rows using length and abstention-marker heuristics:

| Classification | N | Share |
|---|---:|---:|
| Honest abstention ("I don't have information about ...") | 207 | 92.0% |
| Wrong-but-confident substantive prediction | 16 | 7.1% |
| Hedge (substantive prediction inside abstention framing) | 2 | 0.9% |

The 16 wrong-confident responses are concentrated on questions where the model has *something* in pretraining (a biographical sketch) but the held-out passage describes a behavior the sketch does not contain. The model fills in plausibly and the judge rejects it. This means REFUSE is not a clean "abstention" bin: 7 percent of the time the model is confidently wrong rather than honestly silent. The §4.1 lift figure on REFUSE (+1.32) is therefore a mixture of *spec corrects abstention* and *spec corrects confident error*. Both are improvements in representational accuracy, but they differ behaviorally and they have different downstream implications for how a deployed system should disclose what it knows.

## Reproducibility

- Per-question table and aggregates: `docs/research/baseline_engagement_analysis_20260429.json`
- Analysis script: `scripts/analyze_baseline_engagement.py`
- Loaders reused (canonical 5-judge primary aggregation): `scripts/recompute_5judge_primary.py`
- C5 response text sources: `results/global_<subject>/results_v2.json` (13 globals); `results/hamerton/results_harmonized.json` (Hamerton, prediction-tier qids 21-60)

## Open questions for the integration step

0. *Section placement.* This draft is labeled §4.x. Natural homes are: (a) immediately after §4.1 (gradient) as a per-question disaggregation that explains the gradient mechanically, or (b) in §4.6 (alongside other within-question analyses) with a forward reference from §4.1. Recommendation is (a); it makes the §4.1 C4a-ceiling-near-2.46 finding feel less surprising and prepares the §1.3 framing for the rest of §4.

1. *Hamerton's battery provenance.* Hamerton uses a legacy Haiku-generated battery flagged in DATA_REFERENCE as a sensitivity concern. Including it does not move the headline (drop-Hamerton ρ remains around −0.73; bin distributions shift only marginally). A footnote calling out the battery-composition difference would suffice; the v10.1 footnote on this can be reused.
2. *Refuse-bin classification accuracy.* The 92 / 7.1 / 0.9 percent split is heuristic. A small Sonnet-as-judge spot-check on ~30 randomly sampled REFUSE responses would tighten the methodological caveat. Estimated ~$0.50.
3. *Disambiguator hit rate.* Our keyword-based disambiguator detection only fires on 16 of 546 questions because question authors generally avoid stuffing context keywords into prediction prompts. If the integration agent wants a stronger naming-vs-context comparison, the disambiguator lexicon should be expanded or the analysis re-cast as "does the question reference an *event* the model would know" rather than "does it contain a keyword."
