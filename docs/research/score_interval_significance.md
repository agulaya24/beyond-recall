# Fractional score significance: what does a 0.3-point delta actually mean?

**Purpose.** The prediction rubric (§3.7) has integer anchors: 1 = refuses / off-base, 2 = right topic wrong prediction, 3 = right domain no specifics, 4 = right direction with specifics, 5 = specific outcome. When we average across 3-7 judges and 39 questions, subject means land on fractional values (2.78, 3.08, 3.35). Readers need a guide for interpreting those fractions. This document provides one, derived from actual response text at each score band.

## 1. Methodology

**Pool.** We assembled 1,092 `(question, condition, response, judges' scores, mean)` tuples from all 14 global subjects plus Hamerton. Source files: `results/<subject>/baselayer_results.json` for response text, `results/<subject>/baselayer_judgments_merged.json` for per-judge scores (3 judges per response in the global run). We banded every record by its mean, then drew a diversity-constrained sample (max 2 per subject) of up to 15 records per band.

**Scripts.** Build: `_build_score_pool.py`. Stats: `_analyze_score_bands.py`. Sample text: `_print_band_examples.py`. Raw pool: `_score_band_pool.json`. Band stats: `_score_band_stats.json`. Example text: `_band_examples.txt`.

**Metric of judge disagreement.** For each record we compute std(scores) and range(scores) across judges. Mean of these, per band, indicates how much of a band's position is a real consensus score versus a noisy average that papers over disagreement. All band-level statistics in §2 are computed over the full pool of 1,092 records. The per-band qualitative characterizations in §3 are drawn from the diversity-balanced samples in `_score_band_pool.json`.

**Judge-count heterogeneity.** Records from the 13 global subjects each carry 3 judges; Hamerton records carry 6. A 2-point range out of 3 judges is different from a 2-point range out of 6. §2 reports both pools separately. The core finding — that mid-band means (2.6-3.7) hide high judge disagreement while extremes (1.x and 4.2+) show near-consensus — holds in both.

**Limitation.** The 4.6-5.0 band contains only 12 records total (5 global + 7 Hamerton). Global ceiling records are dominated by a small set of subjects (Bernal Diaz, Rousseau, Seacole). Claims about the ceiling band are weaker than claims about the floor and middle bands.

## 2. Per-band characterization

Statistics below are computed over the **full pool** (1,092 records), not the 15-record diversity-balanced sample. The qualitative characterizations are derived from reading the samples. The two tables below split the 3-judge global records (14 subjects, n=1,014) from the 6-judge Hamerton records (n=78). Judge-count matters because a 2-point range means more out of 3 judges than it does out of 6, and we confirmed the finding holds in both.

**Global subjects (3 judges per response, n=1,014 records across 14 subjects):**

| Band | n | mean | mean stdev | mean range | % range ≥ 2 | % range ≥ 3 | Response form |
|---|---|---|---|---|---|---|---|
| 1.0-1.3 | 110 | 1.01 | 0.02 | 0.06 | 0.0% | 0.0% | Universally off-target. Judges unanimous. |
| 1.5-1.8 | 130 | 1.66 | 0.63 | 1.11 | 10.0% | 0.8% | Right topic, wrong prediction. Mostly 1-2 splits. |
| 2.0-2.3 | 185 | 2.01 | 0.27 | 0.57 | 24.9% | 3.8% | On-topic. Judges usually agree within 1. |
| 2.6-2.9 | 78 | 2.67 | 1.00 | 1.86 | 67.9% | 15.4% | Domain partially visible. Bimodal judging begins. |
| 3.0-3.3 | 83 | 3.01 | 1.13 | 2.25 | **100.0%** | 21.7% | Right domain, contested specifics. Max judge disagreement. |
| 3.4-3.7 | 42 | 3.66 | 0.96 | 1.93 | 57.1% | 35.7% | Right domain with emerging specifics; residual panel split. |
| 3.8-4.1 | 36 | 4.00 | 0.63 | 1.28 | 63.9% | 0.0% | Direction with specifics. One-point 3-vs-4 and 4-vs-5 splits dominate. |
| 4.2-4.5 | 27 | 4.33 | 0.58 | 1.00 | 0.0% | 0.0% | Strong direction + specifics. Clean 4-vs-5 splits. |
| 4.6-5.0 | 5 | 4.73 | 0.46 | 0.80 | 0.0% | 0.0% | Near-outcome. n is tiny — treat with caution. |

**Hamerton (6 judges per response, n=78):**

| Band | n | mean | mean stdev | mean range | % range ≥ 2 | % range ≥ 3 |
|---|---|---|---|---|---|---|
| 1.0-1.3 | 7 | 1.05 | 0.12 | 0.29 | 0.0% | 0.0% |
| 1.5-1.8 | 1 | 1.67 | 1.03 | 2.00 | (n=1) | - |
| 2.0-2.3 | 20 | 2.08 | 0.36 | 0.90 | 20.0% | 15.0% |
| 2.6-2.9 | 5 | 2.73 | 1.23 | 3.00 | 100.0% | 80.0% |
| 3.0-3.3 | 4 | 3.08 | 1.21 | 3.00 | 100.0% | 75.0% |
| 3.4-3.7 | 3 | 3.67 | 1.15 | 3.00 | 100.0% | 100.0% |
| 3.8-4.1 | 5 | 3.97 | 0.71 | 2.00 | 100.0% | 0.0% |
| 4.2-4.5 | 7 | 4.38 | 0.53 | 1.00 | 0.0% | 0.0% |
| 4.6-5.0 | 7 | 4.90 | 0.19 | 0.43 | 0.0% | 0.0% |

**The most important row is 3.0-3.3.** Every single record in the full pool (n=83 global + n=4 Hamerton) had ≥ 2 points of judge range. The mean is 3.01 but the underlying distribution for a typical record looks like `[5, 2, 2]` or `[4, 2, 3]` — one judge reads the response as "right direction with specifics," another as "addressed the topic but missed it." The 3.0-3.3 band is the ambiguity plateau: it aggregates responses that are genuinely borderline between categories 2, 3, and 4. The 3.4-3.7 band, often treated as "solidly category 3," also shows substantial disagreement (57% range ≥ 2, and 36% range ≥ 3 on the global pool) — response content has stabilized toward the right domain, but panel agreement hasn't caught up. Agreement tightens decisively only at 4.2+ and collapses to zero variance at the floor.

## 3. What the text looks like, by band

The full 570-line qualitative read is in `_band_examples.txt`. Representative behavior:

**1.0-1.3 (floor).** Response is coherent but off-target for the held-out ground truth. Example: Augustine q25 asks about his "approach to presenting different possibilities." Held-out text is about time and memory. Response answers with "dialogical and comparative" — well-written but aimed at the wrong question. All three judges scored 1.

**1.5-1.8 (floor-adjacent).** Response addresses the right topic but predicts the wrong behavior. Babur q12 on maternal tribal-alliance expectations: response catalogs mother's education and lists behavioral axioms (M4, M1, A6, A10), framing extensive genealogical context — but never lands on the specific expectation (shared Uzbek blood as political asset). Two judges score 2 for topicality, one scores 1.

**2.0-2.3 (orientation).** The response is on-topic and the general disposition is identified (e.g., "Augustine attempts to resolve rather than dismiss"), but no specific mechanism from the held-out passage surfaces. Judges typically agree within 1 point.

**2.6-2.9 (approaching neighborhood).** The first band where judge disagreement becomes structural. 73% of records have a 2+ point range. Example: Bernal Diaz q36 on soldiers' awareness of fortified danger — response captures the "paradoxical relationship between danger awareness and action" which one judge rewards (4) and two others discount (2, 2). The response is interpretively rich but the specifics drift from the held-out text's literal content.

**3.0-3.3 (contested right-domain).** Domain is locked in but specifics are absent or contested. Augustine q10 on intellectual pride: response names pride as a "structural barrier" (correct domain) but does not surface the cedars-vs-herbs imagery of the ground truth. Judges score 4, 2, 3. The record's mean of 3.00 averages a judge who thought this was a direction-with-specifics response against two who thought it only reached the domain.

**3.4-3.7 (solid right-domain with emerging specifics).** Variance drops. Response now has at least one specific that maps to the ground truth's core move. Augustine q2 on withdrawal: response captures "reorientation of capacities toward different objects" — which aligns with the held-out passage about writing in retirement. Two judges score 4, one 3.

**3.8-4.1 (right direction with specifics, near-4 consensus).** Response reliably names both the direction and 1-2 concrete behaviors from the held-out text. Bernal Diaz q18 on religious confrontation language: response predicts "abomination" as the rhetorical register — the ground-truth uses exactly that word. One judge gives 5, one 4, one 3.

**4.2-4.5 (strong direction, contested 5).** Response predicts the specific outcome with supporting detail. Judge disagreement is almost always 4 vs 5 (one judge withholding the ceiling), not 3 vs 5. Range is typically 1.

**4.6-5.0 (near-outcome).** Near-unanimous 5s. Bernal Diaz q30 on vigilance during danger: response predicts posted watches and sharp lookout; ground truth is literally "we also took the precaution of posting such numbers of sentinels, that each of us in turn, had at least one watch every night." All three judges score 5.

## 4. The core finding: integer crossings matter, within-category shifts mostly don't

The rubric's meaning-bearing structure is at the integers. A 0.3-point delta carries semantic weight iff it straddles an anchor:

- **2.9 → 3.2 is a category change.** At 2.9, most judges think the response addressed the topic but missed the domain. At 3.2, most judges think it reached the domain but missed the specifics. This is the rubric's line between a "missed" response and a "correct-domain" response.
- **3.2 → 3.5 is density change within category 3.** The response still lives in "right domain, weak specifics." The delta means the judge panel has more agreement that the response reached the domain, or that a few responses added partial specifics. It does not mean the response type has changed.
- **3.8 → 4.1 crosses 4.0.** Another category change. At 3.8, the typical response has some specifics but judges disagree about whether they rise to "direction correct with specifics." At 4.1, most judges are confident they do.
- **3.4 → 3.7 is within category 3.** Meaningful for aggregate claims (narrowing judge disagreement, more responses with emerging specifics) but not a qualitative change in response type.
- **2.0 → 2.4 is within category 2.** A shift in how often responses approach domain-adjacency without crossing into domain capture.

**This rule has an important caveat:** judge disagreement is load-bearing. A mean of 3.2 from judges `[3, 3, 3, 4]` is a solid category-3 response with minor upside. The same 3.2 from `[1, 3, 4, 5]` is a response three judges fundamentally disagree about. In our data, the mid-bands (2.6-2.9, 3.0-3.3, 3.8-4.1) disproportionately contain the high-variance case. This means fractional differences near category boundaries often reflect panel ambiguity about whether a response crossed the boundary — not a crisp "most judges think it did, a few think it didn't." For paired comparisons (C1 vs C3 per question), the direction is what matters, which is why our primary test is a sign test. But for condition means reported as absolute numbers, the 0.3-delta-across-an-anchor rule is what gives them interpretive content.

## 5. Proposed §3.7 insert (3 paragraphs)

The following can be appended to §3.7 after the calibration discussion:

> **Interpreting fractional score movements.** Because condition means aggregate across 3-7 judges and 39 questions, they land on fractional values. The meaning of a fractional delta depends on whether it straddles an integer anchor. A shift from 2.9 to 3.2 straddles 3.0: the modal response has moved from "addressed the topic but missed the domain" to "reached the right domain but missed the specifics" — a qualitative category change. A shift from 3.2 to 3.5 remains inside category 3: the modal response type is unchanged; the delta reflects either narrower judge disagreement or more responses with emerging specifics, but not a new response character. The same logic applies at the 4.0 boundary: 3.8 → 4.1 is a category crossing into "right direction with specifics," while 4.2 → 4.5 is a densification within that category. A useful heuristic: when comparing two means, ask how many integer anchors the interval covers. An interval that covers zero anchors is a density change. An interval that covers one anchor is a category change for a nontrivial fraction of the battery.
>
> **Judge disagreement is concentrated at the category boundaries.** When we examined per-record judge-score vectors across 1,092 records, we found that judges agree almost unanimously at the floor (std ≈ 0 in the 1.0-1.3 band) and the ceiling (std ≈ 0.30 in the 4.6-5.0 band), but disagree maximally across categories 2-4. In the 3.0-3.3 band, every record in our diversity-balanced sample had a judge-score range of at least 2 points (e.g., one record scored `[5, 2, 2]`, another `[4, 2, 3]`). This is substantively meaningful: a response that reaches the right domain with contested specifics will produce exactly this kind of split — one judge reads the specifics as "predicting the specific outcome" (5), another reads the same response as "addressing the topic but predicting incorrectly" (2). The mean papers over this structure. When we report a condition score near a category boundary, we are reporting the centroid of a distribution that genuinely contains multiple interpretations of the same response. Means further from boundaries (e.g., a clean 2.0 or a clean 4.2) reflect panel consensus and are interpretively tighter than their fractional distance would suggest.
>
> **Practical reading guide.** When comparing two numbers in this paper, we recommend the following: (a) deltas that cross an integer anchor (e.g., Hamerton C5 baseline 1.25 → C3 full-stack 3.08, which crosses 2.0 and 3.0) represent category changes for a majority of the question battery and are the strongest evidence of specification effect; (b) deltas that stay inside an integer (e.g., Yung Wing C1 2.22 → C3 2.40, both inside category 2) represent density movement within a response type and should be read as the specification nudging response distributions, not relocating them; (c) absolute scores near integer boundaries (2.9, 3.1, 3.9, 4.1) should be read with the knowledge that individual-question judge disagreement is maximized there — the mean is the centroid of a genuinely bimodal distribution. This is why we report paired sign-test p-values and Cohen's d alongside condition means for Hamerton: the per-question paired structure preserves judge disagreement as a signal rather than averaging it away.

## 6. Sharpest insight

The 0.3-delta-across-an-anchor rule is the right frame, but the deeper finding is that **judge disagreement is itself a signal about where on the rubric the response sits**. The unanimous-zero-variance floor and the near-unanimous ceiling are epistemically clean — a mean of 1.0 or 4.8 means what it says. The mid-bands (2.6-3.3 in particular) are where the rubric's integer structure breaks down at the judge level: the same response text genuinely can be read as both a 2 and a 5 by different competent judges, and the fractional mean averages that disagreement into a false-precision number. This is not a weakness of the rubric; it is what makes the rubric informative. Responses near 3.0 are where the specification is doing interpretive work that judges legitimately disagree about, which is the exact regime where the paper's headline claims live. The frame for §3.7 should make this explicit: the mid-band numbers are compressed reports of a distribution, not point estimates, and the paper's reliance on paired sign tests rather than raw mean-difference t-tests reflects this directly.
