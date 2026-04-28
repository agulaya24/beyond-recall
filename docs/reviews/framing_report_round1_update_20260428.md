# Round 1 Framing Report — Critical Update (2026-04-28)

The deeper pattern-activation analysis (`docs/research/pattern_activation_deep_20260428.md`) completed AFTER the Round 1 framing-report agent was briefed. The agent must integrate these findings before producing its draft. The findings change Pivot 6 and Pivot 7 substantially.

## Headline

**The heuristic-level pattern-activation claim is falsified.** The fair-comparison spec_doing_work rate is:
- Extreme jumps (wins): 78.9% (n=38)
- Non-jumping controls: 80.6% (n=36)
- Delta: -1.7 percentage points

Pattern activation is the dominant rhetorical mode under spec-loaded conditions but is NOT a discriminator between wins and non-wins. The token-overlap heuristic detects "response generated under spec-loaded condition" rather than "spec drove a band jump."

## Stream X errors the deeper analysis caught

1. Used wrong spec file. Stream X analyzed `spec.md` (931 words for Ebers) but the actually-served spec at C2a/C4a is `spec_production.md` (5775 words for Ebers). All Stream X PATTERN_PREDICATE counts were against the wrong spec text.

2. Hamerton spec-length backwards (already noted in `hamerton_confound_note_20260428.md`).

3. 9 of 47 PATTERN_PREDICATE jumps in Stream X's count came from degenerate C5 to C4 (factdump-only) pairs where the disconfirmation reference IS the post-condition. Tautological classification. Excluding these gives the fair-comparison 78.9% rate above; including them dragged Stream X's spec_doing_work rate down to 66.0% on a non-comparable basis.

4. Control group 94.7% PATTERN_PREDICATE+HYBRID rate — HIGHER than the 78.3% on extreme jumps. Heuristic is uniformly hot whether the spec lifted or not.

## What the data DOES support

- Spec produces extreme upward anchor crossings on a measurable subset of questions (60 unique cases across 18 condition pairs).
- Direct quote lookup is essentially zero. Spec to held-out 6-gram match: 0. So the spec is NOT containing the answer text. This part survives.
- The lift mechanism is positively unidentified at the heuristic level. The data does not yet support a specific mechanism claim.

## What the data does NOT support (currently)

- "Pattern-predicate activation is the dominant mechanism" (heuristic-level falsified)
- "The mechanism is behavioral-predicate activation, not retrieval" (heuristic-level falsified; ablation pending)
- Even the cautious "evidence favors predicate-mediated" framing the collective review endorsed pre-deeper-analysis is now shaky, because the evidence base it rested on (Stream X's N=20) had multiple errors.

## Likely co-drivers worth investigating (per deeper analysis)

- Facts list providing specific anchors that the spec doesn't contain
- Rubric upgrading band-1 refusals to band-4 patterned responses on the basis of "feels grounded" rather than ground-truth match
- Retrieval surfacing held-out matches in some condition pairs

## Implications for the Round 1 framing report

The framing-report agent must:

### Update Pivot 6 (cautious mechanism description)

OLD recommendation (from collective review): apply cautious framing "evidence favors predicate-mediated, ablations needed"

NEW status: the data does not support even this cautious framing pre-ablation. The heuristic is non-discriminating, so the basis for "evidence favors predicate-mediated" is gone.

Replace Pivot 6's recommendation with: HOLD-FOR-PHASE-2C-RESULTS. No mechanism claim should enter the paper based on the heuristic analysis alone. The honest current statement is: "The specification produces extreme upward anchor crossings on a measurable subset of questions. Direct-quote lookup is empirically ruled out (spec-to-held-out 6-gram match: 0). The mechanism by which the lift occurs is not identified by token-overlap analysis at the per-question grain; predicate ablation experiments (Appendix __) are needed to attribute mechanism."

### Update Pivot 7 (strong mechanism description)

OLD recommendation: PHASE-2C-DEPENDENT, only defensible if ablation succeeds

NEW status: same recommendation, but the framing report should be MORE explicit that the heuristic-level evidence has been falsified and ablation is the only remaining route to a positive mechanism claim. If ablation also fails, the paper has to ship without a mechanism claim and treat the lift as a measurable phenomenon with unidentified mechanism.

### Add a NEW section to the report

"### Mechanism uncertainty: what the data does and does not support"

Body:
1. The spec produces extreme upward anchor crossings (Phase 1 wins inventory).
2. Direct-quote lookup is empirically ruled out as the mechanism (deeper analysis n-gram check).
3. Pattern-predicate activation as the dominant mechanism is not supported at the heuristic level (deeper analysis fair-comparison test).
4. The mechanism is therefore positively unidentified. Three candidate co-drivers warrant future investigation: (a) facts-list anchoring, (b) rubric-rater bias toward grounded-feeling responses regardless of ground-truth match, (c) condition-specific retrieval surfacing held-out content.
5. Phase 2c predicate ablation experiments will test (a) and (b). Without those results, the paper makes no mechanism claim.

This new section becomes the honest substrate for the Discussion-section recommendation.

## Implications for cross-cutting risks

The "rater confabulation" risk the collective review flagged is now empirically supported, not just a hypothetical. The control group's 94.7% PATTERN_PREDICATE+HYBRID rate suggests the LLM rater (in this case the Stream X classifier, but the same logic applies to the rubric judges) attributes pattern-grounding to ANY successful response under a spec-loaded condition.

The framing report should elevate rater confabulation from "hypothetical alternative" to "demonstrated property of the heuristic" and use this in Pivot 6's risk treatment.

## Implications for sections of the paper

The Round 1 framing report's "Sections that DO NOT need framing change" subsection should ADD: the paper's mechanism claims, since none currently exist in body text. The current paper's restraint on mechanism claims (it does not say "the spec works via predicate activation") is now confirmed to be the right stance.

## What the framing report still has to recommend on

Iterative refinements 1-5 (per-question variance subsection, mean-Δ reconciliation, Spearman ρ in 4.4.2, half-anchor metric, Hamerton-leverage at per-question grain) are unaffected by this update. Apply the original Pivot recommendations on those.
