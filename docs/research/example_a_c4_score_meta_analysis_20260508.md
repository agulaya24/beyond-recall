# Meta-analysis: Example A (Fukuzawa Q35) C4 = 1.00 unanimous, Example C (Seacole Q2) abstention asymmetry

**Date:** 2026-05-08
**Trigger:** Aarik flagged that the C4 score in Example A looks higher than 1 to a careful reader, especially compared to the Example C Seacole abstention scored 2.80.
**Data:** `results/global_fukuzawa/judgments_v2.json`, `results/global_seacole/judgments_v2.json`, `results/global_*/results.json`

---

## TL;DR

The Fukuzawa C4 = 1.00 score is **unanimous across 5 primary judges**, not noisy: every primary judge gave it a 1. Under a literal reading of the verbatim rubric anchor ("1 = Refuses or off-base"), the C4 response is hard to defend at 1: it is neither a refusal nor categorically off-base; it correctly identifies the practical-vs-moral binary the question asks for, and even names the "students more valuable as scholars than as soldiers" framing that maps directly onto the held-out's "students too precious." Anchor 3 ("right domain wrong outcome") or 4 ("general direction correct") is more defensible.

What the unanimous 1 reveals is **judge norm convergence on a stricter held-out-specific-match standard than the verbatim rubric specifies.** The same panel scored the Seacole Q2 explicit abstention with a 5/2/3/3/1 split — wide variance, mean 2.80. The two cases together illustrate exactly the §3.3.6 refusal-anchor-ambiguity the paper already documents: the rubric's lowest anchor lumps together honest refusals, substantively wrong predictions, and (in practice) "didn't reach the held-out's specific framing," and judges apply different norms across these.

The Spec lift mechanism in Example A (voice-matched argument from character pattern) is real regardless of the C4 anchor placement. The 1.00 → 4.20 magnitude is partly inflated by the strict-anchor-1 reading on C4. The substantive worked-example claim survives; the headline magnitude has a caveat.

---

## Raw per-judge scores

### Example A: Fukuzawa Q35 ("Would Fukuzawa's reasoning for keeping students from war be based on moral principle or practical concern?")

| Condition | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | **Primary mean** | Gemini Flash |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| C5 baseline | 1 | 1 | 1 | 1 | 1 | **1.00** | 1 |
| C4 factdump | 1 | 1 | 1 | 1 | 1 | **1.00** | 2 |
| C2a spec | 2 | 1 | 3 | 2 | 2 | **2.00** | 5 |
| C2c wrong-spec | 2 | 1 | 3 | 2 | 2 | **2.00** | 5 |
| C4a facts+spec | 5 | 2 | 4 | 5 | 5 | **4.20** | 5 |

Notes:
- C4 unanimous 1 across 5 primary judges. Not a noise artifact; a consensus.
- Sonnet is the C4a outlier at 2 (others 4-5).
- C2a and C2c are score-identical (2.00 each), an indicator that Spec content alone — independent of whether the Spec is Fukuzawa's or someone else's — was scored similarly on this Q. Worth a separate wrong-spec note.

### Example C: Seacole Q2 ("How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?")

| Condition | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | **Primary mean** | Gemini Flash |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| C5 baseline | 1 | 1 | 3 | 3 | 1 | **1.80** | 1 |
| C4 factdump | 5 | 2 | 3 | 3 | 1 | **2.80** | 1 |
| C2a spec | 5 | 4 | 4 | 4 | 4 | **4.20** | 5 |
| C2c wrong-spec | 1 | 1 | 3 | 1 | 1 | **1.40** | 1 |
| C4a facts+spec | 5 | 5 | 5 | 5 | 5 | **5.00** | 5 |

Notes:
- C4 has wide variance: 5 / 2 / 3 / 3 / 1. Five judges, five different views on what an explicit abstention deserves.
- C4a unanimous 5 across 5 primary + Gemini Flash. Strong consensus on the Spec response.

---

## Verbatim rubric reading vs actual scoring

**Verbatim rubric anchors (from `scripts/judge_hamerton_5judge.py`):**

| Anchor | Label |
|---|---|
| 1 | Refuses or off-base |
| 2 | Wrong prediction |
| 3 | Right domain wrong outcome |
| 4 | General direction correct |
| 5 | Predicts specific outcome |

### Example A C4 response (verbatim)

> "Fukuzawa's reasoning would likely be **practical concern** rather than moral principle... [evidence list]... Fukuzawa would likely argue that students were more valuable to Japan's future as scholars than as soldiers — a practical calculation rather than a moral one."

### Example A held-out (verbatim)

> "For this kind of war, if they wanted figureheads in their ranks, they could as well hire farmers from the provinces. My students were too precious."

### Anchor reading

- **Refusal?** No. The response engages the binary question and answers it.
- **Off-base?** No. The response correctly identifies practical reasoning, not moral, which matches the held-out's framing.
- **Wrong prediction?** No. The C4 prediction (Fukuzawa would frame this practically; students more valuable as scholars) is directionally correct.
- **Right domain wrong outcome?** Plausible. The response is in the right domain (practical/utility framing) but doesn't reach the specific "figureheads/farmers" outcome.
- **General direction correct?** Defensible. The held-out's general direction ("students too precious to spend on figurehead duty") is a practical-utility argument; C4 captures this.
- **Predicts specific outcome?** No. Misses "figureheads as substitutes."

A literal reading of the verbatim rubric places this response at **anchor 3 or 4**. Five primary judges placed it at **anchor 1**.

### What the unanimous 1 likely reflects

Three plausible mechanisms, listed by how well they explain the data:

1. **Strict held-out-specific-match norm.** Judges treat anchor 5 as "matches held-out's specific outcome" and anchor 1 as "any miss of the specific outcome," collapsing anchors 2-4 in practice. Under this norm, anything that doesn't reach "figureheads/farmers" defaults to 1 regardless of whether the practical-vs-moral binary is correctly answered. This norm is not in the rubric text but is consistent with what we see.

2. **Meta-analysis penalty.** The C4 response stays third-person ("Fukuzawa would likely argue..."). Judges may treat predictive language *about* the subject's reasoning as off-target relative to a prediction *of* the subject's response. This would explain why C4 (third-person) → 1 and C4a (first-person voice-matched) → 4-5, with the substantive practical-vs-moral framing remaining stable across both.

3. **Judge convergence on tacit construct.** Five frontier models from three providers all converge on 1 for C4. Whatever rule they're applying, they agree on it. The §3.3.4 finding that frontier models converge on the construct from minimal scaffolding cuts both ways — the convergence here may reflect a shared norm not made explicit in the rubric.

These are not mutually exclusive. Mechanism 1 is the most parsimonious; mechanism 2 explains the C4 → C4a magnitude better.

### Sonnet's C4a = 2 outlier

Sonnet placed C4a at 2 (anchor "wrong prediction") while four other judges placed it at 4-5. The Sonnet score is inconsistent with the unanimous 5 on Seacole C4a. Two reads:
- Sonnet applies a stricter held-out-match norm and treats the C4a's specific outcome as off (the held-out is "students too precious to use as figureheads," and the C4a frames it as "you cannot advance learning if you are dead or conscripted" — different specific outcome).
- Sonnet noise on this question.

Either way, this is one outlier in a 5-judge panel, exactly the kind of noise the panel design absorbs by aggregation.

---

## Example C asymmetry confirms §3.3.6

**Seacole C4 (explicit abstention)** scored 5 / 2 / 3 / 3 / 1, mean 2.80. The judges have no shared norm on what an explicit information-gap acknowledgment deserves: Haiku gave it full credit, GPT-5.4 gave it the floor.

**Fukuzawa C4 (substantively engaged third-person analysis)** scored 1 / 1 / 1 / 1 / 1, mean 1.00. The judges have a shared norm here.

Both responses are anchor-1 candidates under a strict reading of "Refuses or off-base." Judges treat them very differently. The asymmetry is exactly the **refusal-anchor-ambiguity** §3.3.6 documents:

> "The rubric's lowest anchor ('refuses or off-base') lumps together honest refusals to answer and substantively wrong predictions. Judges sometimes score refusals at 2 or 3 instead of 1, especially when the refusal recites related facts."

Examples A and C in §4.1 are the worked illustrations of this ambiguity. They're useful; the magnitude on each is partly an artifact of how that specific judge norm landed.

---

## What this means for the paper

### What survives unchanged

- **The Spec lift mechanism in Example A is real.** The C4a response (voice-matched argument from character pattern using A2 Utility Gate) is substantively different from C4 (third-person practical analysis) regardless of where on the rubric judges place each. The mechanism is the substantive worked-example claim.
- **The Spec lift mechanism in Example C is real.** The C4a response is unanimously 5 across all 6 judges. That alignment is not a strict-reading artifact.
- **The §3.3.6 audit's "refusal anchor ambiguity" finding is reinforced**, not contradicted. The paper already documents this.
- **The aggregate Mean Δ_C4a = +0.89 is not threatened by these per-question observations.** Aggregate is a property of subject-level means across 14 subjects, not of any individual question's anchor placement.

### What needs softening

- **The 1.00 → 4.20 magnitude language in Example A.** The "1→4 jump" framing reads cleaner than the data supports. The C4 score's anchor-1 placement reflects judge norm convergence on a stricter standard than the verbatim rubric specifies.
- **The "C4 is off-target meta-analysis" prose in Example A.** This is the paper's interpretation of *why* judges scored C4 at 1; it's plausible but not directly verifiable from the scores alone. Frame it more cautiously.

### Options forward

**Option 1 — Footnote, no example change.** Keep both worked examples. Add a footnote on Example A (and a parallel one on Example C) acknowledging the per-judge variance / unanimous-strict-anchor pattern and pointing to §3.3.6. The mechanism in each example survives; the magnitude is a judge-norm reading.

**Option 2 — Replace Example A with a less rubric-strict case.** Find a Q where C4 → C4a has a less-extreme jump (e.g., 2.4 → 4.6) so the mechanism (voice-matched argument from character pattern) reads cleanly without the anchor-1 strictness layered in. This costs author time to identify and write up; mechanism quality of the replacement may not be as crisp.

**Option 3 — Run the Fukuzawa Q35 cell fresh under both rubrics in the same execution** (the methodology the per-judge ablation established as the right control). One cell × 5 judges × 2 rubrics = 10 calls, ~$0.10. If fresh judges still converge to 1.00 on C4, the unanimous strict reading is genuine and Option 1 (footnote) is the right move. If fresh judges drift toward 2-3, the cached scores are stale and the example needs a real recomputation.

**Recommendation:** Option 3 first ($0.10, ~5 min), then Option 1 with the resulting evidence.

---

## Files

- This memo: `docs/research/example_a_c4_score_meta_analysis_20260508.md`
- Raw judgments referenced: `results/global_fukuzawa/judgments_v2.json`, `results/global_seacole/judgments_v2.json`
- Response text: `results/global_fukuzawa/results.json` (Q35), `results/global_seacole/results.json` (Q2)
- Related: `docs/research/published_rubric_per_judge_ablation_20260508.md` (today's ablation), `docs/research/rubric_rejudge_reconciliation_20260508.md` (today's reconciliation), §3.3.6 of v11.9 paper draft.
