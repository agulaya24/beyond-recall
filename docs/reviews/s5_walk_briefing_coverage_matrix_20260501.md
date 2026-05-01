# §5 Walk Briefing — Per-Subsection Coverage Matrix (v11.6)

**Date:** 2026-05-01
**Purpose:** Reference checklist for each §5 subsection of the v11.6 paper. Before drafting any §5 subsection, consult this matrix to ensure full coverage of load-bearing claims, required stats, multi-LLM panel concerns, confidence-catalog tier honoring, and pre-registered/post-hoc labeling. Built against §1–§4 of `beyond_recall_v11_6_draft.md`, the §1–4 multi-LLM review (`round_v11_5_sections_1_4_20260501_141341.md`), the §5 structure review (`round_v11_6_section5_structure_20260501_152904.md`), the cold-read outline + drift diff, the v11 confidence catalog, and Appendix B.10.
**§5 panel-vetted structure (8 → 7 subsections):** §5.1 Synthesis (locked) · §5.2 Gradient + population of relevance · §5.3 Retrieval is not interpretation · §5.4 Composition with retrieval (Letta paragraph in-line) · §5.5 Wrong-spec mechanism + hedging · §5.6 Compression and operational tractability · §5.7 Closing argument.
**Locked aggregation rule:** Per-subject grain first, then cross-subject mean. Headline "+0.89 lift" = cross-subject mean of per-subject Δ_C4a on 9 low-baseline subjects (NOT the grand mean +0.93). Tag every stat with its grain.

---

## §5.1 Synthesis lede — DOCUMENTARY ENTRY (already locked)

**This entry documents what landed in §5.1 so §5.2–§5.7 stay consistent with it. Not prescriptive.**

1. **Lead claim.** Across 14 historical subjects, the Behavioral Specification operates as a portable, content-specific, structurally compressible interpretive layer that measurably increases representational accuracy where pretraining is thin, and the data also reveal that retrieval-only memory systems are not solving the same problem.

2. **§1.3 headlines covered.** All 7 (synthesis paragraph touches each at one-sentence depth; deeper development is delegated to §5.2–§5.6).

3. **§4 driving subsections.** §4.7 (six-finding summary) + §1.3 (seven headlines) + §4.6.1 (Tier 2 cross-provider replication; named explicitly per Opus' single-reviewer flag).

4. **Required stats (already present).** None as headline numbers — the synthesis is qualitative integration, not stat-listing. Stats live in §5.2–§5.6.

5. **Multi-LLM panel concerns absorbed here.**
   - **Construct-validity hedge on "representational accuracy"** — all three reviewers (Mistral, GPT-5.5, Opus) flagged in §1–4 review; absorbed at §5.1 so downstream subsections don't re-hedge.
   - **Tier 2 cross-provider replication mention** (Opus only, §5 structure review) — strongest within-paper response to LLM-monoculture concerns.
   - **Avoid "by construction cannot be passed by sycophancy" framing** (all three §1–4 reviewers) — soft-pedal in lede.

6. **Cold-read drift items absorbed.** Replaces current §5.1 Anti-Pattern (which was §2.1 recapitulation in discussion clothing).

7. **Confidence-catalog tier.** HIGH (synthesis stitches H1–H5 + post-hoc but-confirmed retrieval-divergence into one positive claim).

8. **Pre-registered vs post-hoc.** Mixed — the synthesis mentions both H1–H5 (pre-registered per B.10) and the retrieval-divergence finding (post-hoc per B.10). Labeling is per-finding, not per-subsection.

9. **Cross-references that must work.** Forward to §5.2 (gradient), §5.3 (retrieval-divergence), §5.4 (composition), §5.5 (mechanism), §5.6 (compression), §5.7 (closing). Back to §1.3, §4.7, §4.6.1.

10. **Anti-patterns absorbed (do NOT replicate downstream).**
    - Do not relist the seven headlines mechanically — synthesis integrates.
    - Do not re-do §2.1 positioning.
    - Do not assert "first empirical evidence" register; "first measured evidence on autobiographer subjects with constructive extrapolation" is the locked register.

---

## §5.2 — Why the gradient is the load-bearing finding (folds population of relevance)

1. **Lead claim.** The Behavioral Specification levels prediction quality across subjects to a roughly uniform post-spec answer quality near 2.46 on the 1–5 rubric; the lift in raw points is largest where the baseline is lowest, and almost every real AI user sits deep in the low-baseline band. The gradient is the load-bearing finding because it tells us *who* the spec is for.

2. **§1.3 headlines covered.**
   - **Headline 1 (Gradient)** — full development, primary home.
   - **Headline 2 (Step-changes / category-shift)** — partial; the per-question echo of the gradient (REFUSE-bin lift +1.32 vs ENGAGED/STRONG lift −0.47) fits here; multi-anchor crossing rates also live here.

3. **§4 driving subsections.**
   - **§4.1 Cross-subject gradient** — primary anchor.
   - **§4.1.1 Per-question baseline engagement** — bimodal C5 split (41% REFUSE, 21% STRONG) as per-question echo.
   - **§4.1.2 Franklin reference** — high-baseline end, gradient read from both ends.

4. **Required stats** (per-subject grain unless flagged):
   - **+0.89** mean Δ_C4a, low-baseline slice (n=9, cross-subject mean of per-subject means).
   - **9 of 9** low-baseline subjects positive.
   - **2.46** = post-spec C4a mean across all 14 subjects (the leveler quality).
   - **−0.96** Δ_C4a-on-baseline regression slope; **R² = 0.82**; **p < 0.001**.
   - **+0.04** level-regression slope (C4a on C5), **R² = 0.008** — the coupling-free reframe.
   - **W = 11, p = 0.007** (Wilcoxon signed-rank, n=9 low-baseline).
   - **Franklin C5 = 3.77**, Δ_C4a = **−0.13**.
   - **41.2%** of 546 questions REFUSE at C5 (mean Δ +1.32 in this bin); **21.2%** STRONG (mean Δ −0.47).
   - **ρ = −0.73** (Spearman, n=546, p ≈ 1.7 × 10⁻⁹¹) between C5 baseline and C4a − C5 lift.

5. **Multi-LLM panel concerns to address.**
   - **GPT-5.5 + Opus (§1-4 review):** −0.96 slope is mechanically coupled to a near-zero level slope. Slope_Δ = slope_level − 1 by identity. Lead with "post-spec quality is roughly constant near 2.46" not the regression slope. The catalog explicitly says do not claim differential treatment heterogeneity.
   - **Mistral (§1-4 review):** Battery question-type confound (literal-recall fraction). Note: §4.6.3 reports slope attenuation −0.96 → −0.88 with the partial predictor; baseline survives. Mention as already-controlled.
   - **GPT-5.5 + Opus (§1-4 review):** "Population of relevance" is L3 (constructive, not empirical). Phrase as "constructive extrapolation," not "established."
   - **Opus (§1-4 review):** §4.1.1 bimodal REFUSE/ENGAGED is one of the most informative findings; gets prominent treatment in §5.2 to prevent the "name-resolution lift = pattern-capture lift" misread.

6. **Cold-read drift items.**
   - **REORDERABLE-2:** Population of relevance folded into the gradient subsection (cold-read recommended; panel endorsed unanimously).
   - **UNDERWEIGHTED-1:** §5.2 four-result summary should mirror §4.7 five-finding structure (the divergence finding is the 5th and lives in §5.3, but §5.2 should still gesture at it in the closing sentence as a bridge).

7. **Confidence-catalog tier.**
   - **HIGH:** H1, H2 (gradient), H3 (per-question variance via §4.1.1).
   - **MEDIUM:** M1 (spec is the tool for the unknown — caveat: literal-recall correlation in catalog).
   - **LOW:** L3 (autobiographer → general AI users generalization is constructive).
   - **UNRESOLVED:** U2 (Hamerton elevated rate cause not isolated — flag if Hamerton is pulled out as headline).

8. **Pre-registered vs post-hoc** (per B.10):
   - **Pre-registered:** H1, H2 (the gradient itself), H3 (per-question variance), Franklin reference structure.
   - **Post-hoc reactive:** Battery-question-type sensitivity, Hamerton subset regression, coupling-free reframing of the gradient.
   - **Post-hoc:** Hedging-elimination is sometimes cited in §5.2 contexts but its primary home is §5.5; in §5.2 it's a cross-reference only.

9. **Cross-references that must work.**
   - Back: §1.3 (headlines 1, 2), §1.4 (population of relevance argument), §4.1, §4.1.1, §4.1.2, §4.6.3 (battery sensitivity).
   - Forward: §5.3 (the gradient sets up why retrieval can't do this alone), §5.6 (compression makes the leveler operationally deployable), §5.7 (closing).

10. **Anti-patterns to AVOID.**
    - Lead with "−0.96 slope" as if it were independent inferential evidence (it's coupled).
    - Claim spec "uniquely lifts low-baseline subjects" as treatment heterogeneity (catalog "should not claim").
    - Frame "population of relevance" as empirical generalization rather than constructive extrapolation.
    - Conflate name-resolution lift (1 → 2 transitions, 33.3% of low-baseline) with full pattern-capture lift (Opus' note that this oversells "step-changes").
    - Use "wins" / "big wins" terminology.

---

## §5.3 — Retrieval is not interpretation: what the cross-system divergence means

1. **Lead claim.** Recall accuracy and interpretive relevance are different properties. Given an identical fact pool and the same questions, four commercial memory systems plus our substrate disagree about which facts the question is asking for — not because they store different content, but because their ranking algorithms encode different theories of relevance.

2. **§1.3 headlines covered.**
   - **Headline 7 (Provider divergence on retrieval relevance, surfaced post-hoc)** — full development, primary home.

3. **§4 driving subsections.**
   - **§4.4.1 Aggregate performance + retrieval-overlap subsection** — primary anchor.
   - **§4.6.5 Retrieval-overlap sensitivity** — semantic-similarity matching robustness check.

4. **Required stats.**
   - **52.3%** of (system pair, question) instances share zero top-10 facts.
   - **71.4%** share one or fewer.
   - **Mean pairwise Jaccard = 0.083** across 10 system pairs (controlled config, n=546 questions).
   - **0.093 / 0.102 / 0.191** soft Jaccard at threshold ≥ 0.95 / ≥ 0.85 / ≥ 0.70 (controlled, K=10) — never crosses 0.30.
   - **Native pairs:** exact Jaccard = 0.000; soft Jaccard at ≥ 0.85 = 0.004; at ≥ 0.70 = 0.016.
   - **Strongest pair anywhere in 240-cell sensitivity grid:** Base Layer ↔ Supermemory at K=10, threshold ≥ 0.70 = **0.277**.

5. **Multi-LLM panel concerns to address.**
   - **GPT-5.5 + Opus (§5 structure review):** Cold-read outline said "no caveat needed." Panel said this is wrong: the finding is post-hoc per B.10 and should be labeled exploratory/post-hoc. Magnitude is robust under §4.6.5; status is post-hoc.
   - **GPT-5.5 + Opus (§1-4 + §5 reviews):** "Shared interpretive substrate" is loaded language. Use as interpretation, not demonstrated fact.
   - **GPT-5.5 (§1-4 review):** Top-K overlap is sensitive to retrieval implementation details (output schemas, dedup, normalization, top-k semantics). Don't claim "no shared substrate" as a general architectural fact about memory systems; claim "no convergence on relevance ranking under identical input on this test."
   - **GPT-5.5 (§5 structure review):** K > 10 is untested; flag as future work.

6. **Cold-read drift items.**
   - **MISSING-1 (CRITICAL):** This subsection IS the fix to the cold-read drift. Current §5 has only a one-phrase mention; this subsection makes it load-bearing.

7. **Confidence-catalog tier.**
   - **HIGH** for the empirical magnitude (numbers are pre-registered in `docs/research/retrieval_overlap_analysis_20260501.json` and confirmed at every threshold tested in §4.6.5).
   - **MEDIUM** for the interpretive claim ("interpretive relevance is a distinct property") — the empirical finding is high-confidence; the framing of what it implies for memory-system architecture is interpretive.
   - **POST-HOC** evidentiary tier (per B.10, this is exploratory/post-hoc, not pre-registered H1–H5).

8. **Pre-registered vs post-hoc** (per B.10):
   - **Post-hoc:** Cross-system retrieval-overlap divergence (§4.4.1; sensitivity in §4.6.5; §1.3 7th bullet). The semantic-similarity sensitivity grid in §4.6.5 was a planned robustness check on the post-hoc finding.

9. **Cross-references that must work.**
   - Back: §1.3 (7th headline), §2.1 (fifth-target argument), §2.2 (recall benchmarks LongMemEval / LOCOMO), §4.4.1 (full divergence subsection), §4.6.5 (sensitivity grid).
   - Forward: §5.4 (the spec layered on top of these systems is the other half of the memory-system story), §7.1 (meta-analysis follow-up: K > 10).

10. **Anti-patterns to AVOID.**
    - Frame as pre-registered (it isn't; it's post-hoc per B.10).
    - Claim "memory systems lack a shared interpretive substrate" as a general architectural fact (use scoped phrasing: "do not converge on relevance ranking under identical input on this test").
    - Treat divergence as a flaw without acknowledging it could reflect provider-specific design choices (Mistral's "could be a feature").
    - Imply this proves recall benchmarks are wrong (they measure recall, which they measure adequately; what they don't measure is the layer above).

---

## §5.4 — Composition with retrieval: three patterns and architectural implications (with Letta architectural-ceiling in-line paragraph)

1. **Lead claim.** Layered on top of memory-system retrieval, the Behavioral Specification interacts through three distinguishable per-question patterns (interpretive supply, over-theorization, spec-induced refusal); the aggregate Δ_spec on each system is the residue of these patterns and shifts with retrieval architecture. A static spec serving the same content on every question is the floor; the data point toward dynamic serving as the next architectural step. Two architectures (retrieval-based static spec, self-editing memory block) converge on the interpretive target on N=3, but the self-editing path has a scaling ceiling the static spec does not share.

2. **§1.3 headlines covered.**
   - **Headline 5 (Memory-system layering)** — full development, primary home.
   - **Exploratory note (Letta stateful-agent path)** — partial; in-line paragraph treatment per panel-vetted structure.

3. **§4 driving subsections.**
   - **§4.4 Memory-system composition** (lede).
   - **§4.4.1 Aggregate performance** (per-system Δ_spec table) — only the per-system aggregates here; divergence finding lives in §5.3.
   - **§4.4.2 Three patterns** (interpretive supply / over-theorization / spec-induced refusal).
   - **§4.4.3 Keckley Q21 cross-system case study** (Pattern 3 worked example).
   - **§4.4.4 Two statistical signatures** (ρ=0.27 spec-on-baseline re-ranking vs ρ=0.71 spec-on-info-rich uniform lift) — load-bearing for dynamic-serving framing.
   - **§4.5 Letta stateful-agent (N=3)** — short body summary; full case study in Appendix G.

4. **Required stats** (cross-subject, all-14 unless flagged):
   - **Per-system Δ_spec (controlled / native):** Mem0 +0.12 / +0.33; Letta archival +0.20 / −0.02; Zep +0.19 / +0.33; Supermemory +0.04 / −0.01; Base Layer +0.08 / N/A.
   - **3 of 4** commercial systems net-positive aggregate (under at least one configuration).
   - **Wilcoxon p (all-14, robust at α = 0.01):** Zep controlled p = 0.0004; Letta controlled p = 0.0017; Mem0 native p = 0.0088; Zep native p = 0.0015. Supermemory and Base Layer not significant.
   - **Pattern frequencies on Supermemory** (cleanest read): 110 of 546 questions (20.1%) have |Δ| ≥ 1.0 on the rubric; 57 large helps (mean +1.55) vs 53 large hurts (mean −1.38).
   - **Keckley Q21 cross-system Δ:** Supermemory −2.0; Base Layer −2.2; Letta archival +0.4; Mem0 +0.2; Zep +0.2 (split tracks retrieval strength).
   - **Two signatures (§4.4.4):** ρ = 0.27 (baseline → all facts + spec, re-ranking); ρ = 0.71 (raw corpus → corpus + spec, near-uniform lift); ρ = 0.72 (all facts → all facts + spec); ρ = 0.62 (spec → facts + spec, partial re-ranking).
   - **Letta in-line (N=3):** Hamerton 3.10 vs 2.96 (Δ +0.14); Ebers 2.76 vs 1.72 (Δ +1.05); Babur 2.42 vs 1.88 (Δ +0.54). Block-size scaling: 22,472 chars (Hamerton) → 68,413 (Ebers) → 335,349 (Babur, against ~333K ingestion ceiling). Base Layer compose holds 34K–40K across same range. Verbatim sentence duplication on Babur: 25.4%; semantic near-paraphrase ≥ 0.85: 56.1%; ≥ 0.95: 35.2%.

5. **Multi-LLM panel concerns to address.**
   - **All three reviewers (§5 structure review):** Soften "dynamic activation is a requirement" — catalog M1/U1/L1 do not support requirement-status framing. Use "the data point toward dynamic serving as the next architectural step" not "is a requirement."
   - **Mistral (§5 structure review):** §4.4.4 two statistical signatures missing from cold-read outline; explicitly required for the dynamic-serving framing.
   - **GPT-5.5 (§5 structure review):** §4.4.4 ρ=0.27 vs ρ=0.71 split could have a floor-effect alternative (catalog M2 — ruled out as a clean two-mechanism story; presented as "two statistical signatures").
   - **All three reviewers (§5 structure review):** Letta as peer §5.5 over-promotes N=3 post-hoc data. Demoted to in-line paragraph here. Hedge hard: "N=3, post-hoc, exploratory, one Letta version, one response model." Phrase architectural-ceiling claim as a "specific cost of the self-editing path on the test corpora" not "general architectural ceiling."
   - **Mistral (§1-4 review):** Spec helps "dramatically" overstates aggregate Δ (+0.12 to +0.33). Avoid "dramatic"; per-question pattern is the point.
   - **GPT-5.5 (§1-4 review):** Native memory-system failures scored as rubric floor — flag this hedge if Supermemory's near-zero aggregate is referenced as evidence.
   - **Opus (§5 structure review):** Pattern 3 / Keckley Q21 case — current rubric penalizes principled refusal that correctly reflects the subject's reasoning. §5.4 must carry the differentiated-rubric pointer to §7 without hyping it.

6. **Cold-read drift items.**
   - **MISSING-2 (CRITICAL):** Letta semantic-duplication observation absorbed here as in-line paragraph (not as separate subsection per panel verdict).
   - **STALE-1:** Three-pattern reference now §4.4.2, not "§4.3 and §4.4" (cold-read flagged).
   - **STALE-2:** Keckley Q21 case study now its own subsection §4.4.3; §5.4 should reference §4.4.3 and not re-narrate.
   - **OVERWEIGHTED-2:** "Dynamic activation is a requirement" was too strong — panel echoed; soften.
   - **MINOR-3 + MINOR-4:** Cross-reference Keckley Q21 and three Examples to correct §4 location.

7. **Confidence-catalog tier.**
   - **HIGH:** H4 (three patterns, §4.4.2).
   - **MEDIUM:** M1 (spec is the tool for the unknown — pattern-routing claim), M2 (two statistical signatures, with floor-effect caveat).
   - **LOW:** L1 (which spec component drives lift — flag, do not assert).
   - **UNRESOLVED:** U1 (internal mechanism by which spec produces lift), U3 (LLM-judge construct validity — relevant for Pattern 3 / Keckley reading).
   - **POST-HOC (Letta in-line):** Must be hedged as exploratory, not asserted as generalization.

8. **Pre-registered vs post-hoc** (per B.10):
   - **Pre-registered:** H4 (three-pattern interaction with retrieval, §4.4, §4.4.2).
   - **Post-hoc:** Cross-system retrieval-overlap divergence (lives in §5.3 but mentioned here as setup), Letta stateful-agent N=3 case study, Letta semantic-duplication scaling.
   - **Post-hoc reactive:** §4.4.4 two statistical signatures (added as M2 small section).

9. **Cross-references that must work.**
   - Back: §1.3 (5th headline + exploratory note), §4.4, §4.4.1 (aggregate Δ_spec table), §4.4.2 (three patterns), §4.4.3 (Keckley Q21), §4.4.4 (two signatures), §4.5 (Letta), Appendix G (full Letta case study), §3.6.6 (rubric abstention conflation).
   - Forward: §5.5 (content effect provides the bracketing argument that makes Pattern 1 visible as content-driven not template-driven), §6.2 (rubric limitations), §7.4 (dynamic serving), §7.5 (stateful-agent variant of the spec).

10. **Anti-patterns to AVOID.**
    - "Dynamic activation is a requirement for production response quality."
    - Promote Letta to peer subsection.
    - Claim Letta's architectural ceiling as a general fact (N=3, one version, one response model).
    - Claim three-pattern routing is fully understood (catalog: question-level routing factors are "follow-up question").
    - Use "dramatic help" for memory-system layering (aggregate Δ is +0.04 to +0.33).
    - Re-narrate Keckley Q21 case study (it's in §4.4.3).
    - Use "wins" / "beats" / "crushes" framing for cross-system comparison.

---

## §5.5 — Wrong-spec mechanism and hedging elimination

1. **Lead claim.** The lift comes from the content of the correct specification for the correct person, not from the presence of any structured prompt. Wrong content actively degrades performance; correct content lifts; and correct content also gives the model permission to commit to a specific prediction instead of hedging or refusing. Hedging-elimination is the same content-effect mechanism operating at the rubric floor.

2. **§1.3 headlines covered.**
   - **Headline 4 (Content specificity)** — full development, primary home.
   - **Headline 6 (Hedging reduction)** — folded in (per panel: same mechanism as content-effect at the floor).

3. **§4 driving subsections.**
   - **§4.3 Mechanism: Content, Not Format** — primary anchor (wrong-spec results, three mechanism types, three matched examples, hedging numbers).
   - **§4.6.4 Wrong-spec derangement protocol sensitivity** — v1 vs v2 protocol; per-subject heterogeneity table.

4. **Required stats** (cross-subject, 13 globals unless flagged):
   - **C2a correct spec Δ = +0.35** vs no-context baseline.
   - **C2c v2 random derangement Δ = +0.15.**
   - **C2c v1 adversarial pairing Δ = −0.25.**
   - **Correct-vs-adversarial gap = 0.60 anchor points** (the population-mean content effect).
   - **Spec-tag citation gap:** 78.6% on correct-spec responses vs 50.0% on wrong-spec (28.6-point gap).
   - **Mismatch detection:** Across 587 wrong-spec responses, **60.6% explicitly flagged the content mismatch** despite anonymization. 36.5% applied mismatched content; 3% hedged.
   - **Hedging:** **28.8% → 0.0%** (strict-pattern, first non-whitespace text); **41.2% → 0.4%** (broad-pattern, anywhere in response). Both under C4a (facts + spec).
   - **Per-subject v1:** 5 of 13 subjects positive (coincidental content overlap — Bernal Diaz, Ebers, Fukuzawa, Sunity Devee, Yung Wing); 8 negative.
   - **Per-subject v2:** 9 of 13 positive; 4 negative.
   - **Three matched examples:** A (Ebers Q7) drop −2.00; B (Bernal Diaz Q16) drop −0.20 (coincidental overlap); C (Seacole Q2) drop −3.60.

5. **Multi-LLM panel concerns to address.**
   - **GPT-5.5 + Opus (§1-4 review, CONTESTED):** v1 (−0.25, adversarial) is reported as headline; v2 (+0.15, random derangement) is the standard randomization control. Both reviewers say the headline framing reverses the standard methodological choice. **Aarik decides during walk** — paper §4.6.4 currently keeps v1 as headline because the negative aggregate is stronger evidence of the content effect. Surface this trade-off explicitly in the matrix entry; do not silently side with the paper or with the panel.
   - **GPT-5.5 (§1-4 review):** Hedging reduction can mean more willingness to commit, not necessarily more accurate reasoning. §5.5 must carry this distinction (don't equate hedge-elimination with accuracy improvement; they are correlated but not identical).
   - **Mistral (§1-4 review):** v2 +0.15 still positive — weakens the simple content-specificity story; some behavioral patterns transfer across people. The Bernal Diaz Q16 coincidental-overlap case (Example B) is the documented illustration. Frame this as the bracketing argument: sycophancy ruled out + transfer of patterns across subjects observed.
   - **Mistral + Opus (§1-4 review):** Wrong-spec coincidental overlap not quantified. §5.5 should acknowledge it (the 5 v1 positive subjects in §4.6.4 table, plus Example B).
   - **Opus (§1-4 review):** Hedging-elimination is a strong content-vs-structure result and is undersold relative to the noisier Δ_aggregate comparison. Lead with hedging in §5.5's content-effect framing.
   - **All three reviewers (§5 structure review):** §5.5 must acknowledge unresolved internal mechanism (catalog U1, L1) — which spec component is the active ingredient is not isolated by Phase 2c predicate ablation. State this honestly without inflating into a critique.

6. **Cold-read drift items.**
   - **REORDERABLE-3:** Cold-read recommended splitting current §5.4 (which mixed content-specificity and memory-system composition). §5.5 = content effect; §5.4 = memory-system composition. Drift addressed.
   - **UNDERWEIGHTED-2:** Hedging reduction (6th headline) folded in here per panel verdict (same mechanism).

7. **Confidence-catalog tier.**
   - **HIGH:** H4 (content specificity, §4.3).
   - **POST-HOC:** Hedging-elimination 28.8% → 0.0% (per B.10, surfaced from response-level audit).
   - **POST-HOC:** Per-subject wrong-spec heterogeneity table (per B.10).
   - **LOW:** L1 (which structural feature is the active ingredient).
   - **UNRESOLVED:** U1 (internal mechanism unresolved).

8. **Pre-registered vs post-hoc** (per B.10):
   - **Pre-registered:** H3 (content specificity), wrong-spec controls (v1 + v2).
   - **Reactive:** v1 vs v2 derangement protocol sensitivity (§4.6.4 — labeled "reactive" in B.10).
   - **Post-hoc:** Hedging-elimination, per-subject wrong-spec heterogeneity.

9. **Cross-references that must work.**
   - Back: §1.3 (4th + 6th headlines), §2.4 (Jain et al. 2025 sycophancy framing), §4.3, §4.6.4 (v1 vs v2 sensitivity), §3.6.6 (hedging classifier rules).
   - Forward: §6.1 (limitations on internal mechanism), §7.3 (specification design and composition follow-ups, including predicate ablation).

10. **Anti-patterns to AVOID.**
    - Claim sycophancy is "ruled out by construction" (Opus and GPT-5.5 flagged this in §1.1 framing; bracket the claim in §5.5).
    - Equate hedge-elimination with accuracy improvement (related but not identical).
    - Assert which spec component drives the lift (catalog U1, L1 unresolved).
    - Use v1 number without protocol context (the v1 number depends on adversarial pairing by construction).
    - Dismiss the +0.15 v2 result as noise (it carries the transfer-of-patterns argument).

---

## §5.6 — Compression and what makes personalization operationally tractable

1. **Lead claim.** A 7K-token Behavioral Specification recovers most of what a full 80K–400K-token raw corpus delivers, at 5x to 80x smaller context. Compression is not a cost-saver; it is the property that makes per-user personalization deployable at any real-world scale.

2. **§1.3 headlines covered.**
   - **Headline 3 (Compression)** — full development, primary home.

3. **§4 driving subsections.**
   - **§4.2 Compression: structure vs. raw text** — primary anchor (per-condition table, per-subject compression table).
   - **§4.2.1 Per-question improvement rate** — secondary outcome (improvement / tied / worse rates).

4. **Required stats** (low-baseline slice unless flagged):
   - **C5 baseline = 1.52** (low-baseline mean, n=9).
   - **C2a spec only = 2.23** (~7K tokens) — Δ +0.71.
   - **C4 facts = 2.35** (~10K tokens) — Δ +0.83.
   - **C8 raw corpus = 2.45** (~163K mean, range 33K–549K) — Δ +0.93.
   - **C4a facts + spec = 2.45** (~17K tokens) — Δ +0.93. Same mean as C8 at ~10x less context.
   - **C9 corpus + spec = 2.50** (~170K) — Δ +0.98 (small marginal over C8 alone).
   - **Compression range 5x to 80x** depending on subject (per-subject ratios in §4.2 table).
   - **Hamerton boundary case:** 4.5K-token spec scores 2.63, exceeding 33K-token raw corpus at 2.27. C9 = 3.09.
   - **Ebers honest cost:** 7K-token spec at 1.54 underperforms raw corpus at 2.18 by **−0.64 points** (widest gap).
   - **Per-question improvement rate (low-baseline):** spec-only 70.9%; facts-only 72.9%; raw corpus 78.3%; facts + spec 78.6%.
   - **Median Δ when improved = +1.00** (full rubric category).
   - **Median Δ when worsened = −0.40** (less than half a category).

5. **Multi-LLM panel concerns to address.**
   - **All three reviewers (§1-4 review):** "Matches or exceeds" overstated. Spec-only underperforms raw corpus by 0.22 mean points (low-baseline); Hamerton is the boundary case, not the proof. Frame as "recovers most of the lift" not "matches or exceeds." The catalog explicitly supports "recovers most of the signal" only.
   - **GPT-5.5 (§1-4 review):** Token accounting risks confusion — corpus split is 50/50, raw-corpus conditions use training half. Confirm body matches §3.4 / §4.2 token math. Babur exclusion at C9 (422K-word source exceeds Haiku context) is the right place to make this concrete.
   - **GPT-5.5 (§5 structure review):** §5.6 must include the C4/C4a nuance — facts-only (10K tokens) is already a strong compression pass; spec's marginal contribution over facts-only (low-baseline mean +0.09) is smaller than spec-vs-baseline. Don't let the discussion become "spec vs raw corpus" only.
   - **Mistral (§1-4 review):** Ebers gap (−0.64) underplays compression cost. Surface it as a worked example.
   - **All three reviewers (§5 structure review):** Cut deployment proposals (dynamic activation, modifiability, temporality, topic decomposition, update cadence, infrastructure properties) to §7. Keep one tight production-deployment-tractability paragraph; one sentence pointing to §7 for the rest.

6. **Cold-read drift items.**
   - **OVERWEIGHTED-1:** Cut current §5.5 Practical Implications by ~60%; production-architecture proposals → §7.
   - **OUT-OF-SCOPE-1:** "Per-user calibration" framing without §4 anchor — drop or move to §7.
   - **OUT-OF-SCOPE-2:** Four "infrastructure properties" bullet block — drop or fold to one sentence pointing back to §1.4 / §2.3 / §3.7.

7. **Confidence-catalog tier.**
   - **HIGH:** H5 (compression: 7K-token spec recovers most of corpus signal).
   - All compression numbers are pre-registered headline (H5 in B.10).

8. **Pre-registered vs post-hoc** (per B.10):
   - **Pre-registered:** H5 (compression). §4.2 + §4.2.1.
   - All §5.6 stats are pre-registered.

9. **Cross-references that must work.**
   - Back: §1.3 (3rd headline), §1.4 (structural options for filling the gap), §4.2, §4.2.1.
   - Forward: §7 (dynamic serving, modifiability, temporality, topic decomposition all flagged but not unpacked).

10. **Anti-patterns to AVOID.**
    - "Matches or exceeds" raw corpus (use "recovers most of the lift").
    - Lead with Hamerton (it's the boundary case, not the headline).
    - Hide Ebers gap (make it a worked example).
    - Unpack dynamic-serving architecture in §5.6 (it's §7 territory).
    - Rebuild §1.4's structural-options argument here (one-sentence pointer back is enough).
    - Use "operationally tractable at any scale" (overreaches; supports tested artifact / context budget, not production economics or temporal cadence).

---

## §5.7 — Closing argument

1. **Lead claim.** Personalization at the layer current memory systems address (style, voice, preferences, recall) is the part everyone is solving. The interpretive layer the Behavioral Specification fills is the part no one is, and the data show it is the layer that determines whether an agent acting on someone's behalf actually represents them or merely returns their facts. This paper provides the first measured evidence on autobiographer subjects that an interpretive layer at this resolution can be built, served, compressed, and evaluated; multi-subject living-user replication is what the next phase looks like.

2. **§1.3 headlines covered.** All 7 — implicit synthesis, no new development.

3. **§4 driving subsections.** §4 in toto; specifically §4.7 (summary) feeds the closing posture.

4. **Required stats.** None as headline numbers — closing is qualitative argument tying back to §1.4. Single sentence-level numbers may be cited (e.g., "9 of 9 low-baseline subjects improved" or "Mean lift +0.89 on the population of relevance"); these are recall-of-§5.2, not new claims.

5. **Multi-LLM panel concerns to address.**
   - **GPT-5.5 + Opus (§1-4 review):** "The gap cannot be closed by training a larger model on more public data" overreaches — empirical claim with no direct evidence. §5.7 should frame the structural argument from §1.4 as a constructive deployment argument, not as established empirical result.
   - **Opus (§5 structure review):** "First measured evidence that the layer exists" framing is L3 territory. Keep in "first measured evidence on autobiographer subjects, with constructive extrapolation to the population of relevance" register.
   - **GPT-5.5 (§1-4 review):** Don't say the paper proves the final primitive for all AI personalization. State what the data establish (interpretive layer is buildable, compressible, content-specific, complementary to retrieval at this scope) and what the next phase is.
   - **All three reviewers (§5 structure review):** Keep tight. One to two paragraphs.

6. **Cold-read drift items.**
   - **MINOR-1:** Align "What we did not prove" / "What the study does not settle" language across §5.7 and §6 (current draft has both phrases overlapping); cold-read flagged.
   - Closing must not redo §6 (limitations) or §7 (future work) at length — pointers only.

7. **Confidence-catalog tier.**
   - **HIGH (qualified):** §5.7 stitches H1–H5 + post-hoc-confirmed retrieval-divergence into the closing posture.
   - **LOW:** L3 (autobiographer → general AI users generalization is constructive).
   - The closing must honor L3; don't slide into "first empirical evidence" register.

8. **Pre-registered vs post-hoc.** Mixed — qualitative closing references both; per-finding labeling done upstream in §5.2–§5.6.

9. **Cross-references that must work.**
   - Back: §1.1 (operational primitive), §1.4 (structural options), §4 in toto.
   - Forward: §6 (limitations), §7 (future work — differentiated rubrics, dynamic serving, multi-subject living-user replication).

10. **Anti-patterns to AVOID.**
    - "First empirical evidence" (use "first measured evidence on autobiographer subjects").
    - "The gap cannot be closed by training a larger model" as established result (constructive argument, not empirical).
    - Rebuild §1.4's structural-options argument in full.
    - Announce the question is settled.
    - Use "wins" / "beats" / "crushes" framing.

---

## A. Term-consistency reference

| Term pair | When to use which |
|---|---|
| **"interpretive layer" vs "Behavioral Specification"** | "Behavioral Specification" = the artifact (the served document, the pipeline output). "Interpretive layer" = the conceptual position of that artifact in memory architecture (above retrieval, below the response). Use "Behavioral Specification" when discussing what was built, served, scored. Use "interpretive layer" when arguing about where it sits in the architecture or what category of personalization it addresses. §5.1 + §5.7 use both; §5.2–§5.6 lean toward "Behavioral Specification" (artifact) with one or two "interpretive layer" mentions per subsection at most. |
| **"all facts" vs "facts"** | "All facts" or "all extracted facts" = the full extracted fact pool (C4 condition). Disambiguate from memory-system retrieved facts (top-10 from each system, C1). Phrase ambiguous cases as "all extracted facts (C4)" or "memory-system retrieval (C1, top-10)." |
| **"no-context baseline" vs "C5"** | Body prose: "no-context baseline." Footnotes / tables: "C5" allowed. Never lead with "C5" in §5 prose. |
| **"matched layer / matched specification" vs "wrong-spec"** | "Matched specification" or "correct specification" = the specification authored for the subject in question (C2a / C4a). "Wrong specification" = a different subject's specification served (C2c). Don't say "matched layer" — terminology drift from earlier drafts. |
| **"low-baseline subjects" vs "9 of 14"** | Body prose: "low-baseline subjects" (n=9). Numerical citations: "9 of 14" or "n=9" allowed in stat callouts. The slice definition is "C5 ≤ 2.0" (operational threshold, §3.2.1). Never imply low-baseline = 9 picked at random; the threshold is locked. |
| **"spec-induced refusal" vs "abstention" vs "hedging"** | These are distinct concepts — do not interchange. **Spec-induced refusal** (Pattern 3, §4.4.2) = the model declines to answer because the served specification's epistemic axioms support refusing. **Abstention** = §3.6.6 broader category for "did not commit to a prediction"; includes spec-induced refusal but also retrieval-inflated refusal and baseline non-commitment. **Hedging** = §3.6.6 / §4.3 specific patterns ("I'd need to know," "It's hard to say") classified by the strict (first non-whitespace text) or broad (anywhere in response) rule. Hedging is one form of abstention; abstention is not always hedging; spec-induced refusal is its own distinct mechanism. |
| **"memory-system retrieval" vs "retrieval"** | "Memory-system retrieval" or "retrieval from <system>" when system-specific. "Retrieval" alone is ambiguous in §5 because §5.3 makes a point about cross-system divergence on the same retrieval task. Default to qualifying which retrieval. |
| **"pre-registered" vs "post-hoc" vs "exploratory" vs "post-hoc reactive"** | **Pre-registered** = H1–H5 + the locked controls (Tier 2, GPT-5.4 battery regen, judge-panel composition). **Post-hoc** = surfaced during the work (retrieval-overlap divergence, Letta stateful-agent, semantic-duplication, abstention-credit audit, per-subject wrong-spec heterogeneity, hedging-elimination). **Exploratory** = synonym for post-hoc; B.10 sometimes uses both. **Post-hoc reactive** = added in response to reviewer feedback (battery-question-type sensitivity, Hamerton subset regression, coupling-free reframing, v1 vs v2 derangement protocol sensitivity). Use these terms exactly as B.10 labels them; do not rename. |

---

## B. Style constraints (every §5 draft must satisfy)

- **No em-dashes in body prose.** Allowed only in verbatim spec/response quotes as data. Restructure sentences; do not substitute hyphens.
- **No "wins" / "beats" / "crushes" terminology.** Use "increases in representational accuracy," "extreme upward anchor crossings," "multi-anchor jumps," "lift," "Δ vs no-context baseline."
- **Layman-accessible.** Someone who read only §1 should be able to follow §5.
- **Conclusion-led.** Lead each subsection with the result; push method/caveats to footnotes or cross-references.
- **Representational accuracy as through-line term.** Anchor every interpretive claim to "increases representational accuracy" / "decreases representational accuracy" framing. Don't slip into "alignment" / "fidelity" / "captures the subject's reasoning" without the through-line.
- **Mean Δ stays primary evaluation metric.** Per-question rates and category-shift rates are CONTEXT, not headline.
- **Natural-language condition labels** in body prose. "No-context baseline" not "C5"; "facts plus specification" not "C4a"; "specification alone" not "C2a"; "wrong specification" not "C2c"; "raw corpus" not "C8". Codes in tables / footnotes only.
- **Don't unpack robustness checks in §5;** point to §4.6.x.
- **Don't restate §2 positioning in §5.** §5 should stand on its own from §4.
- **Locked aggregation rule:** Per-subject grain first, then cross-subject mean. Tag every stat with its grain. "+0.89" = cross-subject mean of per-subject Δ_C4a on n=9 low-baseline (NOT grand mean +0.93).
- **Construct-validity hedge absorbed at §5.1.** §5.2–§5.7 don't re-hedge; they reference §5.1 if needed.
- **Pre-registered vs post-hoc labels** must appear at first mention of every post-hoc finding (per B.10). Not every paragraph; just the introduction of each post-hoc result.
- **Bold sparingly.** Reserve for the lead claim of each subsection and for stat callouts of headline numbers.
- **No GTM language.** Avoid product-marketing register ("revolutionary," "best-in-class," "state-of-the-art" outside of §2 positioning).
- **Voice consistency.** Match the §5.1 locked draft and the §5 lede locked register. Aarik's voice pass already shaped these; downstream subsections inherit.

---

## C. Pre-flight checklist for each subsection draft

Before showing Aarik a §5.x draft, verify:

1. **All required stats from item 4 are in the draft** (and tagged for grain — per-subject vs cross-subject vs grand-mean).
2. **All §1.3 headlines this subsection should cover are addressed.**
3. **All applicable panel concerns from item 5 are addressed.** Don't silently side with the paper or with the panel on contested items (§5.5 v1/v2 framing); surface explicitly.
4. **All cold-read drift items from item 6 are addressed.**
5. **Lead is the primary claim** (not buried beneath methodology or caveats).
6. **No em-dashes in body prose.** No "wins" / "beats" / "crushes." No undefined jargon.
7. **Cross-references resolve to valid §X.Y locations.** Run `grep` on §X.Y references against the draft; broken refs are common.
8. **Confidence-catalog tier is honored.**
   - HIGH = stated as established (no hedge required beyond construct-validity at §5.1).
   - MEDIUM = stated with hedge (e.g., "the data point toward X" not "X is established").
   - LOW = future work; do not assert.
   - UNRESOLVED = explicitly flagged as open.
9. **Term consistency** per item A.
10. **Voice consistency.** Reads as continuation of §5.1 + §5 lede locked drafts.
11. **Mean Δ stays primary evaluation metric.** Per-question rates and category-shift rates are context, not headline.
12. **Natural-language condition labels** in body prose; codes in tables / footnotes only.
13. **§5 doesn't redo §2** (positioning) or §6 (limitations) or §7 (future work). Pointers only.
14. **Pre-registered vs post-hoc labels at first mention of each post-hoc finding.**
15. **Locked aggregation rule** honored (per-subject grain first; flag any grand-mean number explicitly).
