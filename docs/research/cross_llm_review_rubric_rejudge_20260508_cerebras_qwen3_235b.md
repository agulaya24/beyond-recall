# Cross-LLM review — Cerebras Qwen3 235B

**Model:** `qwen-3-235b-a22b-instruct-2507`  
**Generated:** 2026-05-08 15:10:30  
**Status:** OK  
**Briefing:** `docs/reviews/_rubric_rejudge_briefing_20260508.md`  
**Script:** `scripts/cross_llm_review_rubric_rejudge_20260508.py`  

---

```
## Q1: Methodology soundness
The rejudge methodology is largely sound in design. The protocol isolates the rubric wording as the sole variable by holding constant the judge panel, prompt structure, blinding, temperature, truncation, seed, and input content. This allows for a clean causal attribution of score differences to rubric wording. However, one flaw weakens the interpretation: the use of seed = 42 for all re-runs introduces deterministic behavior in LLM judges, eliminating stochastic variation that may exist in real scoring. While this increases internal consistency, it risks overfitting to a single inference path per judge-response pair, potentially amplifying idiosyncratic interpretations (e.g., Haiku’s floor-shift). A more robust design would use multiple seeds or report variance across seeds. Additionally, the 1500-character truncation is preserved but not justified—some responses may be cut mid-logic, affecting rubric application. Still, since the same truncation was used originally, this is a consistent limitation rather than a new confound. The stratification across conditions and baseline levels is appropriate, though the substitution of cells from Sunity Devee (due to data gaps) introduces minor contamination. Overall, the design supports a valid within-sample comparison, but the deterministic re-scoring limits generalizability to broader judge behavior.

## Q2: Generalizability
The catastrophic-deflation conclusion for high-baseline subjects does not generalize from this evidence. The n=5 cells from Equiano alone are insufficient to support a claim about the five high-baseline subjects, especially given Equiano’s unique properties: he is the only non-Franklin high-baseline subject with full condition coverage, and his high pretraining coverage likely led to more confident but incorrect model predictions—particularly refusals when the model “knows” the answer but lacks access. The two refusal cases (spot-checks 2 and 3) exemplify this: the model declines to answer despite likely knowing the fact, triggering harsh paper-rubric penalties. This behavior may not transfer to Augustine, Cellini, Rousseau, or Zitkala-Sa, whose pretraining coverage is lower and response patterns may involve more guessing than refusal. Moreover, the high-baseline band’s mean Δ of −1.24 is driven entirely by refusal-type responses; if other high-baseline subjects produce fewer refusals under C5/C4a, the deflation may not recur. Without evidence of refusal frequency or response type distribution across the other four, the Equiano result is best treated as a case study, not a trend. The asymmetry in Δ may reflect subject-specific response modalities, not a systematic rubric effect.

## Q3: Spot-check responses
For Bābur / C4a / q2: a score of 4 under the original rubric ("general direction correct") is a defensible but generous read. The response outlines Babur’s strategic approach—intelligence, diplomacy, deterrence—but fails to predict the specific event (intelligence about Bīban/Shaikh Bāyazīd crossing the river). "General direction" could reasonably include this level of abstraction, but the lack of any mention of the actual threat undermines that justification. The score likely reflects fluency bias or over-rewarding structure. Alternative explanations include judges conflating the question ("approach to threats") with the held-out passage (specific intelligence event), or interpreting "general direction" as alignment with behavioral patterns rather than event prediction.

For Equiano / C5 / q13 and C4a / q27: scoring these 4.40 and 3.20 under the original rubric is indefensible. Both are explicit refusals ("I don’t have the specific text", "I don’t find any reference"), which anchor 1 ("Refuses or off-base") directly covers. No plausible interpretation of "general direction correct" (score 4) applies to a refusal. The high scores suggest either rubric misapplication, confusion between response quality and correctness, or over-penalization avoidance.

The agent’s two-mode mechanism—refusal over-scoring and genericity over-scoring—holds up strongly. These three cases exemplify both: spot-checks 2 and 3 show refusal over-scoring; spot-check 1 shows genericity over-scoring. No alternative pattern better explains the magnitude and direction of Δ.

## Q4: Recommended action
(b) Escalate to a larger sample first.

The rejudge reveals a serious rubric misalignment, but the high-baseline deflation is based on one subject and may not generalize. Option B—re-judging all five high-baseline subjects under the paper rubric—is necessary to determine whether the deflation is systematic or an Equiano-specific artifact. Without this, the paper risks either overcorrecting (if deflation is isolated) or underreporting bias (if it generalizes). The low-baseline results appear robust (mean Δ = −0.12), so headline claims may survive, but the magnitude and ceiling interpretations require recalibration. A selective rerun balances cost and rigor. I would change my mind if the paper team provided evidence that refusal rates and generic response patterns are similar across high-baseline subjects, or if they demonstrated via ablation that Equiano’s behavior is representative.

## Coverage notes (optional)
The briefing did not provide: (1) refusal rates per subject-condition, (2) distribution of response types (refusal, guess, correct) in high- vs low-baseline subjects, (3) inter-rater reliability (e.g., original ICC) for the primary scores, (4) whether the held-out passages were truncated or full-length in original vs rejudge. These would strengthen interpretation.
```
