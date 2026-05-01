# Wins-Analysis Pipeline State Snapshot

_Last updated: 2026-04-28, mid-session_
_Created during a stretch where Anthropic API has been throwing intermittent server 500s; this doc is a durable state snapshot in case a process crashes._

## Origin

C105 in `docs/reviews/v11_comments_extracted_20260427.md` was a flag on the +0.05 C9-vs-C8 Δ ("Honestly interesting that it even adds over raw corpus"). Across the walk it expanded into a multi-stream analytical investigation, then a recursive review pipeline per Aarik's directive that past framings have been wrong (gradient slope as coupling artifact; Stream X arithmetic errors) and major framing changes need multiple recursive review rounds before paper edits.

## Terminology rule (paper-facing)

DO NOT use "wins" / "big wins" in paper prose. Use "increases in representational accuracy," "extreme upward anchor crossings," "multi-anchor jumps." Mean Δ stays the primary evaluation metric. Per-question phenomena are CONTEXT, not headline. Wins-as-headline pivot was explicitly dropped.

Memory: `feedback_no_wins_terminology.md`.

## Phase status

### Phase 1 — wins inventory: DONE

- Output: `docs/research/wins_inventory_20260428.json` (247 KB)
- Script: `scripts/build_wins_inventory.py`
- 18 condition pairs analyzed across direct, corpus, and memory-system layering
- 150 paired questions with extreme upward anchor crossings (≥3 bands), 60 unique after dedup by (subject, qid)
- Cross-checks reproduce published numbers exactly
- C5→C2c also surfaces extreme downward jumps under wrong-spec

### Phase 2 Stream X — big-wins characterization: DONE WITH ARITHMETIC ERRORS

- Output: `docs/research/big_wins_characterization_20260428.{json,md}`
- Script: `scripts/characterize_big_wins.py`
- Errors caught by deeper analysis:
  - Used wrong spec file (`spec.md` 931 words instead of `spec_production.md` 5775 words served at C2a/C4a)
  - Hamerton spec-length backwards (claimed Hamerton has long unified-brief vs globals' six-section spec; actual is opposite)
  - 9 of 47 PATTERN_PREDICATE counts came from degenerate C5→C4 pairs where disconfirmation reference IS the post-condition

### Hamerton confound note: SAVED

- Output: `docs/research/hamerton_confound_note_20260428.md`
- Verified: Hamerton's served spec (`brief_v5_clean.md`) is 1918 words; globals' served spec (`spec_production.md`) is ~5775 words. Hamerton spec is 0.33x globals' size.
- Hamerton extreme-jump rate is 2.1x globals' (18.75% vs 8.9%) but cause is NOT spec length
- Candidate explanations: legacy battery generator path, subject pretraining thinness, predicate density per word

### Phase 2 Stream Y — within-band + meta-judging: DONE

- Output: `docs/research/within_band_shifts_20260428.{json,md}`
- Script: `scripts/within_band_and_meta_judging.py`
- Findings:
  - Integer-anchor metric is 18% lossy (half-anchor shifts add ~18% recorded movement)
  - Panel detects sub-anchor signal cleanly (74% direction-agreement at panel |Δ| 0.1-0.25, 93% at 0.25-0.5)
  - All 5 primary judges add coherent signal (Spearman ρ 0.55-0.59 vs panel-minus-judge)
  - **Two-mechanism finding (Stream Y's headline):** spec-on-baseline (C5→C4a) Spearman ρ = 0.27 (re-ranks); spec-on-info-rich (C4→C4a, C8→C9) ρ ≈ 0.71 (uniformly lifts). Distinct empirical signatures.

### Phase 2 collective review on pattern-activation: DONE

- Output: `docs/reviews/pattern_activation_claim_review_20260428.md`
- Script: `scripts/review_pattern_activation_claim.py`
- Both GPT-5.5 and Gemini Pro endorsed cautious framing pre-deeper-analysis
- Both nominated predicate ablation regeneration with reversal control as highest-priority disconfirmation test
- This review is now superseded by the deeper analysis findings; the cautious framing the reviewers endorsed is no longer data-supported

### Phase 2 deeper pattern-activation analysis: DONE — HEURISTIC CLAIM FALSIFIED

- Output: `docs/research/pattern_activation_deep_20260428.{json,md}`
- Script: `scripts/deep_pattern_activation_analysis.py`
- **Heuristic-level pattern-activation claim is falsified.** Fair-comparison spec_doing_work rate: extreme jumps 78.9% (n=38) vs non-jumping controls 80.6% (n=36). Delta -1.7 pp.
- Heuristic detects "response generated under spec-loaded condition" not "spec drove the lift"
- Direct quote lookup empirically ruled out (0 spec→held-out 6-grams)
- Held-out → post-response leakage: 1 6-gram, 2 4-gram, 9 3-gram (potential pretraining memorization concern; investigation in flight)
- Narrower claim that survives: 11 of 60 INFERENCE_CHAIN cases with verdict genuine_inference_via_spec (vs 2 of 38 controls; ~1 in 6 extreme upward anchor crossings shows specification-enabled inference)

### Phase 2c predicate ablation: DONE — VERDICT: NOT_SUPPORTED

- Output: `docs/research/predicate_ablation_results_20260428.{json,md}`
- Script: `scripts/run_predicate_ablation.py`
- Final run: bash id `bl6kj088n` (resumed from checkpoint after first-run truncation)
- 16 cases stratified across mechanism categories (PATTERN_PREDICATE_high, INFERENCE_CHAIN, MIXED_OTHER) and question axes
- **Mean Δ_removal: +0.050 anchor points** (CI95: [-0.349, +0.449]; straddles zero)
- **Mean Δ_reversal: -0.237** (CI95: [-0.450, -0.025]; replacing the predicate with its opposite slightly RAISED the score, opposite of predicate-mediation prediction)
- 2 of 16 cases supported the strong claim (Δ_removal ≥1.0): bernal_diaz q16, rousseau q28. Both showed correct-direction reversal effects too.
- 11 of 16 cases had Δ_removal < 0.5
- **Important methodological caveat: original-condition reproduction drift is large.** Mean drift = -1.442 anchors between the wins-inventory recorded score and the rerun score. 9 of 16 cases had |drift| > 1.0. This is a stochasticity confound: the "original" score that's the baseline for Δ measurement is itself unstable across reruns. Some of the variance in Δ_removal is original-run drift, not pure ablation effect.
- Verdict per pre-registered decision rule: NOT_SUPPORTED. Rater-confabulation alternative more parsimonious: removing the heuristically-identified causal predicate did not reduce performance, suggesting the lift was either generic persona enrichment, latent world knowledge, or that the heuristic mis-identified the true enabling content.
- Future work for tightening: human rater for predicate identification, larger N, irrelevant-predicate control (matched-length unrelated predicate), multi-predicate ablation
- Each case runs original + ablated (predicate removed, length-matched filler) + reversed (predicate replaced with behavioral opposite)
- 5-judge primary panel scoring on each variant
- ~320 API calls, under $5
- Decision rule:
  - mean Δ_removal ≥ 1.0 anchor: STRONG predicate-mediated mechanism claim supported
  - 0.5 ≤ mean Δ_removal < 1.0: CAUTIOUS framing only
  - mean Δ_removal < 0.5: NOT supported; rater-confabulation alternative more parsimonious
- Results land in appendix per Aarik directive

### Phase 3 Round 1 framing report: DONE

- Output: `docs/reviews/framing_implications_20260428.md` (7,589 words)
- Update integrating deeper-analysis findings: `docs/reviews/framing_report_round1_update_20260428.md`
- Disposition of 8 framing pivots:
  - APPLY-AS-DRAFTED: Refinements 1-5 (per-question variance subsection in §4.2; mean-Δ numerical reconciliation in §4.2; Spearman ρ in §4.4.2; half-anchor metric note in §3.6; Hamerton-leverage at per-question grain in Appendix B)
  - REFINE-FIRST then HOLD-FOR-PHASE-2C: Refinement 6 (cautious mechanism description; superseded by deeper-analysis falsification)
  - PHASE-2C-DEPENDENT: Pivot 7 (strong mechanism description, only if ablation succeeds)
  - APPLY-AS-DRAFTED with reviewer-conditional fallback: Pivot 8 (two-mechanism story at metric level — Spearman split is the strongest pivot; fold into §4.4 as small section + future work, layman language per Aarik)

### Phase 3 Round 2 cross-LLM review on framing report: RUNNING (retry after server 500)

- Output target: `docs/reviews/framing_report_round2_review_20260428.md`
- Script target: `scripts/review_framing_report_round2.py`
- Agent: `a877fc46ccef8daa4` (retry after first attempt's server 500)
- GPT-5.5 + Gemini Pro evaluate the 8 proposed pivots: justification, alternatives, overclaims, missing items, strongest objection
- Author noted: don't expand into full paper re-review; reviewers should evaluate the framing report only

### Held-out passage leakage investigation: DONE — leakage concern CLOSED as RARE

- Output: `docs/research/held_out_leakage_investigation_20260428.{json,md}`
- Script: `scripts/investigate_held_out_leakage.py`
- **Substantive correction:** the deeper-analysis 12-case leakage count was computed on truncated post_response from variable post-conditions (C2a / C4 / C8 / C9 / C3_*). Five of the originally flagged 12 cases were at non-C4a posts where corpus or facts are deliberately served (C9, C4) and "leakage" is by design.
- **At C4a specifically (relevant for the wins inventory): 0 6-gram leakage.** Total raw matches: 0 6-gram, 2 4-gram, 12 3-gram across 60 cases.
- 2 of 60 unique cases meet substantive-leak threshold. 6 are CORPUS_LEAK (short generic phrases also resident in served facts), 2 are PRETRAINING_MEMO_CANDIDATE (best explained by pretraining recall of public-domain autobiography), 1 is COMMON_PHRASE.
- Most concerning case: hamerton q51 (jump=4 bands, 4-gram "as much as possible" classified CORPUS_LEAK; phrase appears in served facts). Longest shared run anywhere is 4 tokens.
- **Severity verdict: RARE.** Footnote acknowledgement sufficient. No structural validity concern. No sensitivity analysis required.
- Headline impact: at most 1 case excluded (sunity_devee q34) if pretraining-memo cases are dropped. 20 → 19 extreme jumps for C5→C4a low-baseline. Mean deltas unchanged at the per-question level.
- Framing point worth keeping: "held-out passage" was held out from served spec / facts, not from pretraining. The audit confirms this interpretation.

## Server 500 issues note

Anthropic API has been returning intermittent 500s during this session (2026-04-28). Both the held-out leakage investigation agent and the Round 2 cross-LLM review agent failed on first launch with 500 server errors and were retried. If further crashes occur:

1. Check this state snapshot for the most recent durable state
2. Each completed phase has its own output file on disk; nothing is lost from completed phases
3. Re-spawn agents with the same brief (briefs are recorded in conversation history)
4. The predicate ablation script has checkpoint resume support (`--go --resume` flag with `docs/research/_predicate_ablation_checkpoint.json`)

## Major framing changes on the table (concrete enumeration)

### Iterative refinements (paper-shape preserving, low-risk)

1. §4.2 — add "What the aggregate numbers hide" subsection with C4→C4a / C8→C9 per-question table + bimodal interpretation
2. §4.2 — mean Δ numerical reconciliation (paper has +0.05 / +0.10 / +0.14 floating around for C9 vs C8; pin to per-question paired recompute)
3. §4.4.2 — strengthen Pattern 1/2/3 with Spearman ρ split (spec-on-baseline ρ=0.27 vs spec-on-info-rich ρ=0.71)
4. §3.6 — add half-anchor metric note (integer-anchor metric is 18% lossy per Stream Y)
5. Appendix B — Hamerton-leverage at per-question grain (existing check is per-subject mean grain only)
6. ~~Discussion / §4.6 — cautious mechanism description~~ HOLD per deeper-analysis falsification

### Higher-stakes pivots (require recursive review before adoption)

7. Strong mechanism description ("the mechanism is predicate activation, not retrieval") — PHASE-2C-DEPENDENT
8. Two-mechanism story explicit (spec-on-baseline re-ranks; spec-on-info-rich uniformly lifts) — fold into §4.4 as small section + future work, layman language per Aarik

### Explicitly dropped

- Wins-as-headline pivot

### Appendix-only

- Predicate ablation experiment results (Phase 2c) — go in appendix

### Still pending

- 9. Held-out leakage finding integration — depends on leakage investigation results

## Next steps (when in-flight work completes)

1. ✓ Round 2 cross-LLM review on framing report DONE
2. ✓ Held-out leakage investigation DONE (closed RARE)
3. ✓ Phase 2c predicate ablation DONE (NOT_SUPPORTED; reframed correctly per Aarik clarification: result does not undermine wrong-spec mechanism evidence; goes in Appendix B.8)
4. ✓ Aarik decision walk DONE: 9 framing-pivot edits + 5 comment-walk edits all applied via agents
5. ✓ Confidence catalog written at `docs/research/v11_confidence_catalog_20260428.md` (HIGH H1-H6 / MEDIUM M1-M2 / LOW L1-L3 / UNRESOLVED U1-U3)
6. ✓ Selected per-subject excerpts appendix (Appendix E) added: 42 cases × 14 subjects
7. ✓ Data-locking pass DONE: DATA_REFERENCE / PROVENANCE_INDEX / KEY_FINDINGS / ISSUES updated; README / AGENTS / study-guide / STUDY_MEMORY / REPRODUCE preserved as-is (already version-aware with v10.1 canonical / v11 active edit)
8. ✓ 4 MISMATCH items reconciled in paper body (line 430 +0.004 → -0.01; line 1069 5/9 → 4/9 controlled lowB Supermemory improved; line 1102 prose -0.05 → +0.04 controlled all-14 / -0.01 controlled lowB / -0.01 native all-14)
9. ▷ Study repo reindex IN FLIGHT (refresh `workspace/study_knowledge.db`)
10. ▷ Cursory collective review IN FLIGHT (GPT-5.5 + Gemini Pro, glaring-errors scope)
11. After cursory review returns: address any blocking issues, then v11 freeze candidate

## V11 freeze readiness

- Paper draft: complete; em-dash count locked at 35 (matches v10.1 baseline)
- Index files: reconciled to v11
- Research artifacts: 17 new artifacts indexed in PROVENANCE_INDEX
- Confidence catalog: explicit map of every claim's confidence level
- All comment-walk items resolved (applied / partial-applied / deferred-to-future-work / no-op)
- Awaiting cursory review verdict
