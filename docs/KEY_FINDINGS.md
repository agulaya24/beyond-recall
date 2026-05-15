# Key Findings

**Paper:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
**Canonical paper draft:** `docs/beyond_recall_v12_1_draft.md` (v12.1, active edit branch as of 2026-05-13 — applying Aarik's 211-comment review pass + final-checks audit fixes). v12 docx retained as historical baseline with comments preserved.
**Generated:** 2026-04-18 (Session 113). Last updated: 2026-05-13 (v12.1 fork; final-checks audits landed; data + repo lock in progress).
**Source of truth for numbers:** `docs/DATA_REFERENCE.md` (5-judge primary panel; v12.1 reconciliation in progress).

This document catalogs every finding the study produced. Each entry includes: the finding, the evidence, and the paper section that contains it. Findings are grouped as MAJOR (load-bearing for the paper's central claim) or MINOR (supporting observations and side findings).

---

**For AI agents working in this repo:** read this file + `docs/DATA_REFERENCE.md` before running new analyses. `DATA_REFERENCE.md` is the canonical source for every number; this file catalogs findings with evidence links. If your work could add, refine, or contradict findings here, propose updates inline and surface to the lead author.

### v11 active edits 2026-04-27 (framing reframes; numbers carry forward from v10.1)

**Status:** v11 (`docs/beyond_recall_v11_draft.md`) is the active edit branch; v10.1 remains the citable canonical paper. The framing changes below are applied in v11 prose only; numerical findings (slope, R², Wilcoxon, low-baseline mean Δ_C4a, all-14 mean Δ_C4a, wrong-spec deltas, memory-system deltas, Letta n=3 stateful-agent values) carry forward unchanged from v10.1. Running log: `docs/reviews/v11_running_changes_log_20260427.md`.

- **§1.3 / §4.4 / §5.2 / §5.4 framing reframe (C139 / C140 / C153):** "additivity" replaced with **"interaction with retrieval"** throughout. Per-question Pattern 1/2/3 framing (interpretation supply on under-determined questions / over-theorization on literal-recall questions / principled refusal where retrieval cannot ground a prediction) is now the load-bearing description of M2; aggregate Δs are characterized as small and informative only as the balance of those patterns. M2 finding direction is unchanged (3 of 4 commercial systems positive on the population of interest); the explanatory frame shifts.
- **§1.3 lede category-shift framing (load-bearing):** "Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it." This category-shift framing is now load-bearing for §1.3 / §4.1 and ties to the cross-anchor interpretation rule from §3.7.3 (ex §3.7.2 in v10.1 numbering).
- **Per-system anchor-crossing data added (M2 evidence row):** `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. Per-system upward anchor-crossing rates on the low-baseline 9: Mem0 23.4% controlled / 36.1% native; Letta archival 26.9% / 19.9%; Zep 27.9% / 32.5%; Supermemory 20.2% / 23.4% (partial native coverage, 7 of 9 subjects); Base Layer 29.0% controlled. Folded into §1.3 Memory-system layering bullet and §4.4.1.
- **§1.4 retitled "What this implies"** (was "Why the gradient matters"). Population-of-relevance pivoted to "anyone who uses an AI system" / broad-technology framing (email, cell phones) / 99% of real AI users sit at the frontier-low-baseline floor. Autobiographers reframed as the closest available imperfect proxy. "What we did not prove" disclaimer paragraph removed (the same disclaimers live in §5.3 and §7).
- **§1.1 hypothesis statement** rewritten in terms-of-art (representational accuracy + interpretation) per B1.
- **§2 reorder (C56 / C57):** §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1. Final order §2.1 benchmarks -> §2.2 memory systems -> §2.3 traceability -> §2.4 cognitive foundations -> §2.5 LLM-as-judge.
- **§3.7 reorder (C71):** Judge panel -> Fractional score interpretation (was §3.7.3) -> Calibration (was §3.7.2) -> Inter-judge agreement -> Aggregation -> Rubric-handling. Section-number references in this file that point at v10.1 §3.7.2 / §3.7.3 should be read as v11 §3.7.3 / §3.7.2 respectively until the sweep completes.
- **§4 restructure (C99 / C124):** §4.1.1 Franklin (m2 evidence section) moved to §4.6.4 under sensitivities. §4.7 closing paragraph added bridging into §5. Section-number references "Paper: §4.1.1" in this file map to v11 §4.6.4.
- **C162:** §1.2 conditions-table C2c long parenthetical pulled to footnote.

### v11 active edits 2026-04-28 (wins-analysis pipeline complete)

The post-comment-walk wins-analysis pipeline (Phase 1 wins inventory, Phase 2 Stream X big-wins characterization, Phase 2 Stream Y within-band shifts, Phase 2 deeper pattern-activation analysis, Phase 2c predicate ablation, Phase 3 framing report) completed 2026-04-28. Source-of-truth claim catalog at `docs/research/v11_confidence_catalog_20260428.md`. Pipeline state snapshot at `docs/research/wins_analysis_pipeline_state_20260428.md`. New findings below; M1 - M14 and m1 - m26 carry forward unchanged.

#### Findings added in v11 (2026-04-28)

| # | Finding | Confidence | Evidence | Paper section |
|---|---|---|---|---|
| M15 | **Per-question variance is substantial beneath aggregate Δs.** Across the same 18 condition pairs, 4,206 anchor crossings + 759 same-band ≥0.5 within-band shifts coexist with aggregate Δs that the 14-subject means understate. C5→C4a low-baseline: 55% upward crossings, 6.8% downward, 38% no movement. Multi-anchor jumps (≥2 bands): 18% of low-baseline questions; extreme jumps (≥3 bands): 6%. Direction asymmetry: across the full 14-subject panel, no question crosses from band 2, 3, or 4 into band 5; only band-1 → band-5 transitions reach the ceiling. The aggregate Δ is a residue of substantial per-question variance, not a uniform lift. (HIGH confidence per H3 in confidence catalog.) | HIGH | `docs/research/wins_inventory_20260428.json`; script `scripts/build_wins_inventory.py` | v11 §1.3 (callout); §4.1; §4.4.2 |
| M16 | **Two statistical signatures.** Pre-vs-post Spearman ρ across questions splits cleanly: spec-on-baseline (C5→C4a) ρ = 0.27 (re-ranks); spec-on-info-rich (C4→C4a ρ = 0.72; C8→C9 ρ = 0.71) (uniform lift). C2a→C4a ρ = 0.62 (mid; partial re-ranking). Statistical signatures, not separately attributable mechanisms; floor-effect alternative (spec-on-baseline scores cluster near rubric floor where re-ranking is structurally easier) is not ruled out. Future work with a non-floor-anchored baseline would distinguish them. (MEDIUM confidence per M2 in confidence catalog.) | MEDIUM | `docs/research/within_band_shifts_20260428.{json,md}`; script `scripts/within_band_and_meta_judging.py` | v11 §4.4.4 (NEW subsection) |
| M17 | **Half-anchor metric is 18% lossy.** For every 1 anchor crossing the binary metric records, ~0.18 additional same-band ≥0.5 shifts exist that the metric does not capture. Panel detects sub-anchor signal cleanly: 74% direction-agreement at panel \|Δ\| 0.1-0.25, 93% at 0.25-0.5, 99.9% at \|Δ\| ≥ 1.0. Methodological transparency note, not a new finding; the paper acknowledges the metric is a lower bound on movement. (HIGH confidence per H6 in confidence catalog.) | HIGH | `within_band_shifts_20260428.{json,md}`; script `scripts/within_band_and_meta_judging.py` | v11 §3.6.2 (methodological note) |
| M18 | **Predicate ablation null result on the strong predicate-mediated mechanism claim.** 16 stratified extreme-upward-jump cases. Mean Δ_removal = +0.05 (CI95 [−0.35, +0.45]); mean Δ_reversal = −0.24 (CI95 [−0.45, −0.02]). 11 of 16 cases Δ_removal < 0.5; only 2 of 16 (bernal_diaz q16, rousseau q28) showed Δ_removal ≥ 1. Verdict: NOT_SUPPORTED for the strong predicate-mediated mechanism claim. Consistent with redundant spec construction (multiple sentences across anchors / core / predictions / brief reinforce the same patterns; removal of any single sentence leaves the pattern accessible elsewhere). Important caveat: original-condition reproduction drift mean = −1.44 anchors (rerun stochasticity confound). Does NOT contradict M3 (wrong-spec content specificity, the higher-level mechanism evidence): the spec as a whole does causal work; the internal mechanism question (which structural feature of the spec carries the lift) remains open. (LOW confidence per L1 in confidence catalog; appendix-only.) | LOW | `docs/research/predicate_ablation_results_20260428.{json,md}` + sampling spec `predicate_ablation_sampling_20260428.json`; script `scripts/run_predicate_ablation.py` | v11 Appendix B.8 (NEW) |
| M19 | **Held-out passage leakage audit on the 60 extreme-upward-jump cases: severity RARE.** 0 6-gram, 2 4-gram, 12 3-gram leaks at C4a. Most concerning case: hamerton q51 (`as much as possible`, CORPUS_LEAK 4-gram). 6-gram-zero finding rules out direct-quote lookup as the lift mechanism on this population. Recommended treatment: footnote acknowledgement sufficient. | HIGH | `docs/research/held_out_leakage_investigation_20260428.{json,md}`; script `scripts/investigate_held_out_leakage.py` | v11 §3.3 footnote (severity RARE) |
| M20 | **Hamerton spec-length inversion identified and corrected.** Hamerton served spec is 1,918 words (`brief_v5_clean.md`, brief-only); globals' served spec averages ~5,775 words (`spec_production.md`, anchors + core + predictions + brief). Hamerton extreme-jump rate 18.75% vs globals 8.9% (2.1× elevation). Spec length is anti-correlated with extreme-jump rate; cause not isolated by the present design. Candidate explanations (legacy battery-generator path, subject pretraining thinness, predicate density per word) not separately identifiable. Corrects an earlier-draft Stream X attribution that read the spec-length direction backwards. (UNRESOLVED per U2 in confidence catalog.) | UNRESOLVED (at mechanism grain) | `docs/research/hamerton_confound_note_20260428.md`; spec word counts via `Path(...).read_text(encoding='utf-8').split()` | v11 Appendix B.6.5 (NEW) |
| M21 | **Pattern-activation heuristic falsified.** Heuristic-level pattern-activation claim falsified on deeper analysis: fair-comparison spec_doing_work rate on extreme jumps is 78.9% (n=38) vs non-jumping spec-loaded controls 80.6% (n=36); Δ = −1.7pp. The heuristic detects "response generated under spec-loaded condition," not "spec drove the lift." Surviving narrower claim: 11 of 60 INFERENCE_CHAIN cases (~1 in 6 extreme upward anchor crossings) verdict `genuine_inference_via_spec` (vs 2 of 38 controls). | HIGH (claim is null; null is well-evidenced) | `docs/research/pattern_activation_deep_20260428.{json,md}`; script `scripts/deep_pattern_activation_analysis.py` | v11 §4.4.2 caveat; Appendix B.6.5 |

#### Findings carrying forward unchanged from v10.1 with v11 paper-section remap

The verification audit at `docs/research/v11_paper_numbers_verification_20260428.md` confirms every numeric finding in M1 through M14 (and m1 through m26) carries forward to v11 unchanged. 298 of 312 audited numerics MATCH; 10 MINOR_ROUNDING; 4 MISMATCH (all flagged for paper edit, not silent reconciliation). MISMATCH items:

- §4.4.1 Supermemory controlled Δ all-14: paper says −0.05; scaffold says +0.04 (sign flips on aggregate; low-baseline grain still −0.018 ~ −0.01, sign-stable)
- §4.4.1 Supermemory controlled all-14 improved: paper says 5/14; scaffold says 7/14
- §4.4.1 Supermemory controlled low-baseline improved: paper says 5/9; scaffold says 4/9
- §4.2.1 all-14 C8 improve: paper says 64.5%; scaffold says 65.2% (sub-1pp)
- §4.2.1 all-14 C8 worsen: paper says 24.5%; scaffold says 23.6% (sub-1pp)

The Supermemory aggregate cluster is the consequential one; it does not flip the §4.4.1 narrative (bimodal mixture, near-zero aggregate) but the all-14 sign is the load-bearing edit. Pending v11 paper edit. Surfaced here per the flagging-don't-silently-reconcile rule.

#### What we explicitly do NOT claim (v11)

Sourced from `docs/research/v11_confidence_catalog_20260428.md`. These are claims the data does not support, that the paper does not make in body, and that downstream readers should not extract from secondary citations.

- **We do not claim predicate-mediated mechanism.** Phase 2c per-sentence ablation null on 16 cases (Δ_removal +0.05, CI95 straddles zero). Single-predicate removal does not measurably reduce response quality. The high-level mechanism question (does the spec cause the lift?) is settled by H1 (changes behavior) + H4 (wrong content degrades); the internal mechanism question (which structural feature of the spec is the active ingredient: anchors / core / predictions / brief; specific predicate types; spec length; predicate density per word) is UNRESOLVED. (Confidence catalog L1 / U1.)
- **We do not claim the spec lifts low-baseline subjects more than high-baseline ones in a treatment-effect-heterogeneity sense.** The −0.96 Δ-on-C5 slope is dominated by the coupling identity slope_Δ = slope_level − 1; the level regression C4a ~ C5 slope = +0.04, R² = 0.008 (essentially flat), mean C4a = 2.46. The substantive finding ("spec is the tool for the unknown") survives reframed as "spec produces a roughly constant post-spec C4a ceiling near 2.46; lift in raw points is mechanically larger where the floor is lower" rather than as differential treatment effect. v10.1 §4.1 framing carries forward; v11 retains it. (Confidence catalog body framing.)
- **We do not use "wins" / "big wins" terminology in paper prose.** Internal pipeline used these terms (`wins_inventory`, `big_wins_characterization`); paper-facing prose uses "increases in representational accuracy," "extreme upward anchor crossings," "multi-anchor jumps." Mean Δ stays the primary evaluation metric. Per-question phenomena are CONTEXT, not headline. The wins-as-headline pivot was explicitly considered and dropped.
- **We do not claim the LLM-as-judge panel measures behavioral pattern capture rather than grounded-feeling response style.** The control-group anomaly in deep pattern-activation analysis (94.7% PATTERN_PREDICATE+HYBRID rate on non-jumping spec-loaded controls) suggests the LLM rater attributes pattern-grounding to ANY successful spec-loaded response. This is the rater-confabulation alternative the collective review flagged; the deep analysis confirmed it. Future work: human annotation on a calibration subset. (Confidence catalog U3.)
- **We do not claim Hamerton's elevated extreme-jump rate is driven by spec format / spec length / battery generator / subject thinness specifically.** All three candidate explanations remain identifiable-as-confounds; the present design does not separate them. Spec length is anti-correlated with extreme-jump rate (Hamerton's spec is 0.33× globals'), so the "richer specifications produce more wins" reading is empirically wrong on this population. (Confidence catalog U2.)
- **We do not claim direct empirical generalization from autobiographers to "anyone who uses AI."** The 14 historical autobiographers are a constructive-argument proxy for the population of typical AI users (whose reasoning is not in any training corpus); this is a structural extrapolation, not an empirical replication. Multi-subject living-user replication is flagged as the leading follow-up (§7). (Confidence catalog L3.)

### v10.1 revision 2026-04-25 (point release)

Numerical and framing updates carried into v10.1 from the v10 body. Aggregate direction of all findings is unchanged; magnitudes and scope statements tightened.

- **Wrong-spec aggregate, random derangement v2:** **+0.22 → +0.15** (5-judge primary, 13 globals, vs C5). Cascades through M3 evidence row, m12, and the v10.1 §1.3/§4.3/§4.6.2 prose. Correct-spec C2a stays at +0.35; adversarial v1 stays at −0.25.
- **Tier 2 response model count corrected: 4 → 2.** Tier 2 cross-provider replication runs **2** non-Haiku response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro). Claude Opus 4.6 and GPT-5.4 appear in Tier 2 only as judges, not as response models. M9 row reads accurately as written; the historical "6 response models" framing in PROVENANCE_INDEX is corrected separately.
- **Tier 2 magnitudes (M9):** demoted to **direction-only with sensitivity ranges**. Per-cell magnitudes (+1.48, +1.07, +1.91, +1.27, +1.40, −0.55) are preserved as historical evidence under M9 but **do not carry through as primary results** in v10.1. Zitkala-Sa × Gemini Pro reframed as approximately null (~−0.03), not −0.55. Verification audit cannot reproduce the published per-cell magnitudes under any aggregation tested. Status: `docs/research/v11_emit/_ARCHITECTURE.md` §12.4 and `docs/reviews/v11_release_freeze_status_20260425.md`.
- **Wrong-spec total N=587 disambiguation:** 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). m20 and M3 evidence row updated to reflect both halves.
- **Living-user language softened:** "expected by construction" replaced with "closest available proxy" framing in line with v10.1 §1.4 / §5.3.
- **§4.1 framing:** "C4a ceiling" replaced with "post-spec operating level" near 2.46.
- **§5.2 H5 reframed:** fact extraction does most of the volume-reduction work; the spec adds marginal value at the per-question level.
- **§4.4 memory-system additivity nuanced:** Zep + Mem0-native strongest; Mem0-controlled small/non-significant; Letta archival positive controlled, near-null native; Supermemory mixture. The "3 of 4 commercial systems" framing is preserved (was inconsistent at "all 4" in earlier prose).
- **§4.4.2 Supermemory mixture (paired analysis):** **89/516 (17.2%) → 110/546 (20.1%)**; 37 helps / 52 hurts → **57 helps / 53 hurts**; mean swings +1.45 / −1.41 → **+1.55 / −1.38**. The Memory-System Character Supermemory section already reflects the v10.1 numbers; this entry is the audit-trail anchor.
- **§4.5 Letta named-entity counts:** Babur Letta 540 → **416**; Hamerton Letta 19 → **26**; Hamerton BL 19 → **22**.
- **§4.5 7-judge sensitivity Δs (Letta block vs BL):** Hamerton +0.20 → **+0.09**, Ebers +0.75 → **+0.75** (~0.746 unrounded), Babur +0.29 → **+0.232**. M5 row updated.
- **§4.2 Table 4.2** compression ratios + means rebuilt under the strict 5-judge primary; per-subject low-baseline aggregates reconciled.
- **§4.2.1 pairwise-table counts:** 190/46/115 → **187/56/108** (C8 vs C2a); 155/42/115 → **153/45/114** (C9 vs C4a).
- **§4.5 Babur block duplication:** 25% → **25.4%** (already reflected here; audit-trail anchor).
- **§4.4.2 Table 4.6 rebuilt on strict 5-judge primary** (per-cell shifts of 0.01-0.06; no row sign flips). Mem0/Yung Wing +0.35 → +0.33; Mem0/Keckley −0.01 → −0.02; Letta arch/Hamerton +0.46 → +0.42 (n=39 → n=38); Letta arch/Keckley 0.00 → −0.02; Zep/Seacole +0.52 → +0.47; Zep/Keckley +0.10 → +0.04; Base Layer/Yung Wing +0.33 → +0.29; Base Layer/Keckley −0.01 → −0.04. Per-cell values are not aggregated in this doc; entries here are the audit-trail anchor.
- **§4.1 level-CI rounding:** −0.25 → **−0.24** (lower bound of the 95% CI on the C4a ~ C5 level slope).
- **Appendix B.4** REFUSAL_TRIGGERING mean Δ: +0.489 → **+0.417**.
- **Appendix B.6** Δ_spec range max: +1.85 → **+1.37**; REFUSAL × Δ_spec correlation: +0.321 → **+0.212**.
- **Appendix B.5** Hamerton axis: +1.93 / +2.02 / +1.71 → **+1.68 / +1.30 / +1.25**.
- **Appendix D.3.4** length-correlation n columns: 351 → **312** for C5/C4/C4a (C2a remains at 351).

### v10 revision 2026-04-24 (release-freeze pass)

Numerical updates to align with the v10 paper's 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4):

- §4.1 gradient slope corrected from 7-judge `−0.98 [−1.30, −0.74]` to 5-judge primary **−0.96 [−1.24, −0.67], R² = 0.82, p < 0.001**.
- All-14 mean Δ_C4a corrected from 7-judge +0.67 to 5-judge primary **+0.55**; low-baseline (n=9) mean Δ_C4a from +1.04 to **+0.89**.
- Battery-composition sensitivity added: multiple regression partial slope **−0.88 [−1.13, −0.63]**, GPT-5.4-battery-only subset slope **−0.89 [−1.18, −0.61]**.
- Coupling-free reframing added: level regression C4a ~ C5 produces slope **+0.04 [−0.25, +0.33], R² = 0.008**, mean C4a = **2.46**. Headline Δ-on-C5 slope is dominated by the coupling identity slope_Δ = slope_level − 1; substantive claim ("spec is the tool for the unknown") survives but framing shifts to "roughly constant C4a ceiling, lift larger where floor lower."
- Spearman ρ across 5-judge primary panel reported as **0.86 - 0.93** (10 pairs); the legacy 0.89 - 0.98 was a 4-judge Hamerton historical statistic.
- §4.5 Letta stateful-agent demoted to exploratory case study with explicit n=3 scope. Hamerton/Ebers/Babur Δ values unchanged at +0.14 / +1.05 / +0.54 (5-judge primary).
- Wilcoxon C5 vs C4a 5-judge primary: W=11, p=0.007 (replaces 7-judge W=9.0, p=0.0063).

### v9 revision 2026-04-23 (updates)

Numeric and structural changes carried into v9 from the v8 body. Aggregate direction of all findings is unchanged.

- Supermemory native n=10 (free-tier, 4 ingestion failures) is superseded by n=14 (paid-tier rerun indexed all 199 chunks, 0 failures). Mean Δ_spec shifted from −0.07 to −0.01 (5-judge primary). Source: `docs/research/supermemory_7judge_aggregate.md`, `docs/research/p0_2_supermemory_paid_tier_rerun.md`.
- Spearman ρ values reported as 0.89-0.98 corrected to 0.86-0.93 across 7 occurrences in the paper body.
- §4.3 wrong-spec battery generator corrected: Haiku, not Sonnet.
- H8 reframed from "spec teaches ethics" to "conservatism dial" per the P0-5 refusal-intent audit, which found 93% of spec-induced refusals are routine rather than morally loaded.
- §4 structural restructure, Appendix A-E build, and Part F safe edits applied; no changes to the v8 or v9 paper files in this housekeeping pass.

## S114 update (April 2026, pre-launch)

The paired C1-vs-C3 analysis originally run only on Supermemory has been extended to every memory system in the study. Findings summary:

- **Mixture-of-swings is system-general.** Every commercial memory system (Mem0, Letta, Zep, Supermemory) plus Base Layer's own retrieval substrate shows bilateral per-question swings hiding near-null aggregates. Added as m15.
- **Three failure modes of specification-based reasoning are system-general.** Over-theorization, spec-induced refusal, and default-axiom overfires each reproduce across systems. Added as m17.
- **Keckley Q21 refusal is a spec-level dynamic, not a memory-system artifact.** Same −2.33 penalty on Supermemory and Base Layer; reproduces with proportional penalties across all 5 systems. Added as m16.
- **Provider recall-benchmark claims are 68-85% range, not uniformly 85%+.** Primary-source audit documented at `docs/research/provider_benchmarks.md`. Paper-wide punch-list item for §2.1 / §5.7 / abstract. Added as m21.
- **Wrong-spec detection upper bound: 60.6%** (N=587, validated), with name-mismatch confound flagged. Added as m20.
- **Letta archival retrieval has severe fact duplication** (dedup 0.34-0.47). New finding. Added as m18.
- **Base Layer prompt-template hedging hypothesis partially contradicted.** §4.4 mechanism claim needs rewrite. Added as m19.
- **Aarik author baseline pilot.** C5 = 1.90 on private data; consistent with low-baseline-is-typical-user thesis. Added as m22.

Research reports supporting these findings:
- `docs/research/supermemory_c1_vs_c3_paired_analysis.md`
- `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`
- `docs/research/baselayer_c1_vs_c3_paired_analysis.md`
- `docs/research/letta_stateful_deep_read.md`
- `docs/research/letta_stateful_matched_rerun.md` (pending)
- `docs/research/wrong_spec_detection_analysis.md`
- `docs/research/provider_benchmarks.md`

---

## TAKEAWAY

> "There is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply — measurable via behavioral prediction, and additive to every memory system tested here."

Eight-word collapse: *"Recall is not interpretation. Interpretation can be measured."*

---

# MAJOR FINDINGS

## M1. The Gradient — spec helps inversely proportional to baseline knowledge

**Finding:** The Behavioral Specification's value is inversely proportional to what the model already knows about the subject from pretraining. On the 9 low-baseline subjects (C5 ≤ 2.0, the slice approximating real AI users), the spec is uniformly beneficial: 9 of 9 positive, mean Δ_C4a = +0.89 points.

**Evidence (5-judge primary, v10):**
- Wilcoxon C5 vs C4a: W = 11, p = 0.007 (N=14); Wilcoxon C5 vs C2a: W = 10, p = 0.005
- Linear regression slope (Δ_C4a on C5): **−0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001**
- Battery-composition sensitivity: partial slope on baseline = −0.88 [95% CI −1.13, −0.63] controlling for LITERAL_RECALL fraction; subset slope on the 13 GPT-5.4-battery subjects = −0.89 [95% CI −1.18, −0.61]
- Coupling-free reframing: level regression C4a ~ C5 slope = +0.04 [95% CI −0.25, +0.33], R² = 0.008, mean C4a = 2.46. The Δ-on-C5 slope is dominated by the coupling identity slope_Δ = slope_level − 1.
- 12 of 14 subjects show positive Δ_C4a (Zitkala-Sa and Equiano negative)
- Low-baseline (n=9): mean Δ_C4a = **+0.89**, mean Δ_spec_alone = +0.69
- Mid-baseline (n=5, 2.0 < C5 < 3.0): mean Δ_C4a = −0.06 (3 of 5 positive)

**7-judge sensitivity (legacy):** slope −0.98 [−1.30, −0.74]; all-14 mean Δ_C4a = +0.67; low-baseline mean Δ_C4a = +1.04. Direction matches; magnitudes are higher because Gemini Flash and Gemini Pro inflate scores by ~+1 point each.

**Paper:** v10.1 §4.1 (per-subject table line 718; sensitivity + coupling reframing lines 747-759). **DATA_REFERENCE:** §1, §2.

## M2. The specification improves three of four commercial memory systems on the population of interest

**Finding:** Layered on top of three of the four commercial memory providers (Mem0, Letta archival, Zep), the Base Layer specification produces positive mean delta on low-baseline subjects in the controlled configuration. Supermemory aggregates near-zero on the low-baseline slice (bimodal per-question distribution; see m15). Three of the four (Mem0, Letta archival, Zep) also show positive aggregate delta across all 14 subjects.

**Evidence (controlled config, 5-judge primary, v10.1 §4.4):**
- Mem0: +0.12 aggregate (10/14 positive); +0.10 on low-baseline (6/9 positive)
- Letta (archival retrieval path): +0.20 aggregate (12/14 positive); +0.17 on low-baseline (8/9 positive)
- Zep: +0.19 aggregate (13/14 positive); +0.17 on low-baseline (9/9 positive)
- Supermemory: +0.04 aggregate (7/14 positive); −0.01 on low-baseline (4/9 positive)
- Base Layer substrate (own retrieval + spec): +0.08 aggregate (9/14 positive); +0.08 on low-baseline (6/9 positive)

Wilcoxon signed-rank within system on the low-baseline slice (C1 vs C3): Zep controlled p = 0.0004, Letta controlled p = 0.0017 (both robust at α = 0.01). Mem0, Supermemory, and Base Layer substrate are not significant at α = 0.05 on n=9; the test is underpowered for the smaller effect sizes those systems show.

**Native config (5-judge primary, paid-tier Supermemory rerun 2026-04-23, all 14 subjects):**
- Mem0 +0.33 aggregate (10/14 positive); +0.32 on low-baseline (7/9 positive)
- Letta (archival) −0.02 aggregate (5/14 positive); −0.04 on low-baseline (4/9 positive)
- Zep +0.33 aggregate (13/14 positive); +0.30 on low-baseline (9/9 positive)
- Supermemory −0.01 aggregate (6/14 positive, n=14 paid-tier); −0.03 on low-baseline (4/9 positive)

Wilcoxon (native): Zep p = 0.0015, Mem0 p = 0.0088 (both robust). Letta and Supermemory native are not significant.

**7-judge sensitivity (legacy S113):** controlled Mem0 +0.15, Letta +0.25, Zep +0.22, Supermemory −0.04, Base Layer +0.12. Direction matches across panels; magnitudes are higher because Gemini Flash and Gemini Pro inflate scores by ~+1 point each (m4).

**Flagship sentence:** "Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know" (carries on three of four uniformly; Supermemory's near-zero aggregate is a bimodal per-question mixture, not a uniform null; see m15).

**Paper:** v10.1 §4.4 (Memory-System Composition). **DATA_REFERENCE:** §3, §4.

## M3. Content specificity — wrong-spec controls fail at baseline

**Finding:** The improvement is not a prompt-engineering trick or a structured-context-helps effect. A wrong subject's spec applied to this subject scores at or below baseline.

**Evidence (5-judge primary, 13 global subjects with complete coverage, v10.1 §4.3 line 891):**

| Condition | Mean Δ vs. C5 |
|---|---:|
| C2a (correct spec) | **+0.35** |
| C2c v2 (random derangement, seed=42) | **+0.15** |
| C2c v1 (fixed derangement; pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING) | **−0.25** |

The fixed-derangement v1 control is the cleanest null because pairings were hand-chosen to maximize cultural and temporal distance between each subject and its assigned wrong spec; the random v2 control is noisier because some random pairings happen to land culturally close. The gap between correct-spec C2a (+0.35) and adversarial v1 (−0.25) is **0.60 points on the 1-5 rubric**, more than half a full rubric-anchor category.

**Per-question evidence:** wrong-spec content-grounded detection rate is 60.6% across **587 classified responses (507 from v2 random-derangement on the 13 globals × 39q + 80 from v1 adversarial-derangement on Hamerton across all 5 battery tiers)** (m20); 28.6-point spec-tag-citation gap between correct-spec (78.6%) and wrong-spec (50.0%) responses (m14).

Both wrong-spec controls score below correct-spec; v1 scores below baseline. The content of the *correct* spec for the *correct* subject is what produces the improvement.

**7-judge sensitivity:** C2a +0.45, v2 +0.22, v1 −0.21. Direction unchanged; correct-spec magnitude widens slightly when Gemini judges are added.

**Paper:** v10.1 §4.3 (Specification Content vs. Format), table at line 891. **DATA_REFERENCE:** §6.

## M4. Memory systems do not converge on which facts are relevant given identical input (retrieval-divergence finding)

**Finding (v11.5+ headline framing, share-zero stats reconciled in v11.8):** Five memory systems (Mem0, Letta, Supermemory, Zep, Base Layer substrate) given the *identical* fact pool retrieve substantially non-overlapping top-K sets. Mean pairwise Jaccard across all ten system pairs is **0.083** (raw) / **0.088** (lowercase + whitespace normalized) at K=10. On **35.9%** of (system pair, question) instances two systems share zero facts in their top-10s; on **65.6%** they share one or fewer (n = 5,460 = all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs, controlled config). Native pairs share zero facts on every question (heterogeneous output shapes). Semantic-similarity matching at near-paraphrase thresholds raises native overlap only marginally.

**Evidence (v11.8 §4.4.1, retrieval-overlap analysis 2026-05-01):**
- Mean controlled Jaccard at K=10: 0.083 raw / 0.088 normalized
- Per-pair K=10 Jaccards: BL↔Supermemory 0.146; Mem0↔Letta 0.126; BL↔Mem0 0.123; Mem0↔Supermemory 0.114; Letta↔Supermemory 0.099; BL↔Letta 0.092; Mem0↔Zep 0.056; BL↔Zep 0.027; Letta↔Zep 0.026; Supermemory↔Zep 0.025
- Native: mean 0.000 (raw 3.2 × 10⁻⁵)
- Sensitivity (semantic-similarity matching, K=10): controlled T≥0.95 → 0.093; T≥0.85 → 0.102; T≥0.70 → 0.191. Native T≥0.95 → 0.001; T≥0.85 → 0.004; T≥0.70 → 0.016
- Strongest single pair: BL↔Supermemory at K=10, T≥0.70 → 0.277 (soft Jaccard)
- Source: `scripts/analyze_retrieval_overlap.py`, `scripts/analyze_retrieval_overlap_semantic.py` → `docs/research/retrieval_overlap_analysis_20260501.json`, `docs/research/retrieval_overlap_semantic_20260501.json`

**Legacy framing (preserved as supporting evidence, no longer the headline):** earlier audits at K=1/3/5/10 measured all-3-disagreement on Mem0 + Letta + Supermemory at 93.4% / 83.3% / 73.8% / 53.2% on the controlled config. The Jaccard reframing supersedes these as the headline since it covers all five systems and reports the structural overlap distribution rather than a single-threshold disagreement count.

**Why it matters:** Recall benchmarks (LOCOMO, LongMemEval, etc.) measure whether the right chunk is in the top-K. They do not measure whether systems agree on *which* chunk is most relevant. Given identical input, the systems do not converge on relevance.

**Paper:** v11.8 §1.3, §4.4.1, §4.6.5 (sensitivity), §4.7. **DATA_REFERENCE:** §K.

## M5. Letta stateful-agent path produces a representation in the same prediction band as Base Layer's spec — at matched response model (n=3, exploratory)

**Finding:** Letta's signature mechanism (stateful self-editing memory blocks during multi-turn conversation) produces an interpretive representation that, when fed to the same response model used elsewhere in the study, scores higher than Base Layer's full-stack specification on all three subjects tested. v12.1 §4.5 reports this as an exploratory case study at n=3, not as a primary result.

**Evidence (5-judge primary; Letta block → Haiku vs. Base Layer full-stack spec → Haiku):**

| Subject | Letta block → Haiku | BL full-stack spec → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.83 | **+0.27** |
| Ebers | 2.76 | 1.56 | **+1.21** |
| Babur | 2.42 | 2.04 | **+0.38** |

The Base Layer side of this comparison is the full-stack Behavioral Specification (anchors + core + predictions + brief), the same artifact class used in v12.1 §4.4's controlled and native conditions; per-subject sizes 34.6K / 39.7K / 37.1K characters. Hamerton's score is the full-stack spec scored with the consistent short-form judge prompt; Ebers and Bābur are full-stack regenerations on the Letta battery. Direction is preserved on all three subjects, with the gap widest at the mid-corpus subject (Ebers). Full report at `docs/research/_letta_rerun/fullstack_named/RESULTS.md`. The earlier 7K-char unified-brief run (Δ +0.14 / +1.05 / +0.54) is superseded; reconciliation at `docs/reviews/v12_1_data_naming_review_20260513.md`.

**Letta block sizes:**
- Hamerton: 22,472 chars (~5,600 tokens), 0.65× BL spec size; full ingestion
- Ebers: 68,413 chars, 1.72× BL spec size; full ingestion
- Babur: 335,349 chars (saturated at ~333K, last 22 of 242 chunks failed to ingest); 9.0× BL spec size; 25.4% verbatim sentence duplication at the ceiling

**7-judge sensitivity (superseded 7K-char run):** Hamerton **+0.09**, Ebers **+0.75** (~0.746 unrounded), Babur **+0.232**. These 7-judge values are for the deprecated 7K-char unified-brief run; a 7-judge sensitivity pass on the full-stack rerun has not been run (the full-stack rerun is 5-judge primary only). Direction matched on the 7K run.

**Caveats (v12.1 §4.5):** N=3, one Letta version, one response model (Haiku), small selected sample of corpus sizes. Multi-subject replication across the full 14-subject gradient is the highest-priority external falsification (§7.5).

**Paper:** v12.1 §4.5 (Letta Stateful-Agent Case Study), Appendix G. **DATA_REFERENCE:** §7.

## M6. Letta's stateful-agent compression does not scale — and we observed the ceiling

**Finding:** Letta's `human` memory block grows roughly linearly with corpus size. At ~333,000 characters, the API begins rejecting further messages. Babur's 223K-word corpus saturated after chunk 220 of 242 — the last 22 chunks (~10% of the corpus) failed to ingest. Base Layer's compose step, by contrast, produces specs of 34-40K characters across a 9× corpus-size range.

**Evidence:**

| Subject | Corpus words | Letta block (chars) | BL spec (chars) | Ratio | Outcome |
|---|---:|---:|---:|---:|---|
| Hamerton | 25,231 | 22,472 | 34,579 | 0.65× | Full ingestion |
| Ebers | 48,161 | 68,413 | 39,708 | 1.72× | Full ingestion |
| Babur | 222,742 | 335,349 | 37,063 | 9.0× | **Saturated at 333K chars; 22 chunks lost** |

**Architectural consequence:** At realistic user-corpus scale (10 years of journals, accumulated session history), Letta's block hits the ceiling we observed. Base Layer's compose step keeps the spec at 5-8K tokens regardless. This is structural, not implementation-detail.

**Paper:** §4.5. **DATA_REFERENCE:** §7.

## M7. Letta's coherence degrades before its size ceiling — the block becomes heavily duplicative

**Finding:** Block-size saturation is the proximate failure; the deeper failure is that the agent's consolidation loop loses coherence well before the size ceiling. At Babur scale, 25% of all sentences in the final block are verbatim duplicates.

**Evidence:**

| Subject | Block | Sentences | Duplicate sentences | % duplicate | Repeated 8-word phrases (3+ occurrences) |
|---|---:|---:|---:|---:|---:|
| Hamerton | 22K chars | 129 | 0 | 0% | 0 |
| Ebers | 68K chars | 364 | 0 | 0% | 1 |
| Babur | 335K chars | 1,301 | 103 | **25.4%** | **2,505** |

At small/medium corpus scale, the agent self-edits cleanly (zero verbatim duplication). At large corpus scale, the agent loses track of what is already in the block and re-asserts the same axioms with each new chunk. One Babur sentence appears verbatim **12 times**. The opener "the individual recognizes the…" appears **86 times** in 1,301 sentences.

**Effective unique content in Babur block ≈ 250K chars, not 335K.** The block hit a coherence ceiling before the size ceiling.

**Paper:** §4.5. **DATA_REFERENCE:** §7 (will be added with Babur data).

## M8. Compression test — 7K-token spec outperforms 34K-token raw corpus

**Finding:** On Hamerton, a ~7K-token Behavioral Specification (C2a) outperforms 34,168 tokens of raw autobiography (C8). Information availability is not the bottleneck; interpretive structure is.

**Evidence (Hamerton, 5-judge primary):**

| Condition | Tokens | Score (1-5) |
|---|---:|---:|
| C8 Raw corpus, no spec | 34,168 | 2.27 |
| C9 Raw corpus + spec | 41,452 | 3.09 |
| C4a All facts + spec | 16,874 | 2.77 |
| C4 All facts, no spec | 7,723 | 2.43 |
| C2a Spec only | 7,320 | 2.63 |
| C5 Baseline | ~40 | 1.26 |

C2a (spec alone, 7K tokens) exceeds C4 (all 462 extracted facts, 7K tokens) by 0.20 points at the same token budget. Structure carries more signal than the raw fact list. C2a (spec alone) exceeds C8 (raw corpus, 34K tokens) by 0.36 points using 22% of the tokens.

**7-judge sensitivity (legacy):** C8=2.32, C9=3.22, C4a=3.22, C4=2.53, C2a=3.04, C5=1.25. Direction identical, magnitudes higher because of Gemini inflation.

**Low-baseline aggregate (v10.1 §4.2):** mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50; mean C8 − C2a gap = +0.22.

**Paper:** v10.1 §4.2 (per-subject table line 791; aggregate line 777). **DATA_REFERENCE:** §8.

## M9. Cross-provider replication — the effect is not Anthropic-specific

**Finding:** The spec effect replicates with non-Anthropic response models on non-Anthropic-generated batteries. Tier 2 circularity test: 5 of 6 (subject × response model) cells reproduce the spec direction, with non-Haiku response models (Sonnet, Gemini Pro) reading GPT-5.4-generated batteries.

> **2026-04-25 v10.1 status:** §4.6.1 is **demoted to direction-only with sensitivity ranges** in v10.1. The directional 5-of-6 claim is retained; the per-cell magnitudes below are preserved here as historical evidence but **do not carry through as primary results** in v10.1. Published magnitudes could not be reproduced under any aggregation tested in the verification audit. A dedicated `_v11_emit_tier2.py` scaffold is post-arXiv work. Tier 2 runs **2** non-Haiku response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro); Opus and GPT-5.4 appear in Tier 2 only as judges. Status detail: `docs/research/v11_emit/_ARCHITECTURE.md` §12.4 and `docs/reviews/v11_release_freeze_status_20260425.md`.

**Evidence (historical magnitudes; direction-only in v10):**

| Subject | Response Model | Battery | Δ | Direction |
|---|---|---|---:|---|
| Ebers | Sonnet | GPT-5.4 | +1.48 | ✓ |
| Ebers | Gemini Pro | GPT-5.4 | +1.07 | ✓ |
| Yung Wing | Sonnet | GPT-5.4 | +1.91 | ✓ |
| Yung Wing | Gemini Pro | GPT-5.4 | +1.27 | ✓ |
| Zitkala-Sa | Sonnet | GPT-5.4 | +1.40 | ✓ |
| Zitkala-Sa | Gemini Pro | GPT-5.4 | −0.55 (v10.1 reframing: ~−0.03, approximately null) | null/mismatch (consistent with §4.1 failure-mode discussion — spec hurts Zitkala-Sa on the gradient) |

**Bonus finding (M9b — see below):** baseline accuracy varies by 1-2 points across response models on the same subject, independent empirical evidence for cross-provider pretraining variance.

**Paper:** §4.6.1 (direction-only in v10.1). **DATA_REFERENCE:** §10.

---

# MINOR FINDINGS

## m1. Hamerton qualitative case — the specification shifts the model from hedging to committed prediction

**Finding:** On Hamerton's London-rejection question (Q21), the baseline model hedges ("Significant discomfort, more nuanced than rejection") while the spec-equipped model commits ("immediate visceral rejection, not gradual disillusionment") — matching the held-out passage.

**Paper:** §4.4.2 [CHECK: Hamerton Q21 qualitative case illustrates the hedging-to-committed interpretation pattern; fits §4.4.2 Common Mechanisms, not the §4.4.3 Keckley Q21 case study]. Score: baseline 2 → C4a 5.

## m2. Franklin baseline ceiling — context can hurt for famous figures

**Finding:** For subjects with high pretraining baseline (Franklin C5 ≈ 4.10), adding context can introduce competing interpretive signals that hurt prediction. The spec is "the right tool for the unknown," not for what the model already knows.

**Paper:** §4.1.1 [CHECK: content is Franklin as high-baseline reference, v9 §4.1.1; mechanical §4.7→§4.5 rule does not apply because this ref was stale-Franklin, not stale-Letta]. **DATA_REFERENCE:** §1 (Franklin not in main 14, separate test).

## m3. Hedging metric — the spec moves models from "I don't know" to committed predictions

**Finding:** Across 13 global subjects (507 responses per condition), baseline hedging drops substantially under every reasonable classifier rule.
- **Narrow rule** (response begins with an explicit refusal prefix: "I cannot," "I don't," "The retrieved facts do not," etc.): C5 = 28.8% (146/507), C2a = 1.4% (7/507), C4a = 0.0% (0/507).
- **Broader rule** (any refusal pattern anywhere in the response): C5 = 41.2% (209/507), C2a = 7.9% (40/507), C4a = 0.4% (2/507).

Both rules agree in direction and magnitude: baseline hedges at roughly 4 to 20 times the rate of spec-containing conditions. The spec changes what the model is willing to commit to, not just the score. Classifier: `scripts/classify_hedging.py` (both `starts_refusal` and `refusal_ge_1` rules, each run over the same 507-response corpus). Artifact: `docs/research/hedging_analysis.json`.

**Paper:** v8 §1.3 Mechanism line 100 reports both rules side by side. **DATA_REFERENCE:** (TBD — add to §K). **Note:** Earlier drafts (v6/v7) reported 25.0%/2.6%/0.6% (127/13/3); that classifier was unrecoverable and the numbers above are the canonical replacement. Directional story unchanged.

## m4. Both Gemini judges inflate scores by ~1 point

**Finding:** Gemini 2.5 Flash and Gemini 2.5 Pro systematically score ~1.0 point higher than the other 5 judges. This shifts aggregates but not directions. The spec effect remains positive 9/9 on low-baseline under both 7-judge and 5-judge non-Gemini aggregations; no subject flips sign.

**Paper:** §4.6.2.

## m5. GPT-5.4 has a high parse-failure rate (~19%)

**Finding:** GPT-5.4 frequently returns text beyond the requested 1-5 digit, requiring exclusion under the locked aggregation rule. Gemini Pro's parse-failure rate, by contrast, is ~0.5%.

**Paper:** §3.7 (judge coverage paragraph). **DATA_REFERENCE:** §9.

## m6. Inter-judge agreement: substantial on rank order, moderate on absolute

**Finding:** Pairwise Spearman ρ = 0.86-0.93 (rank agreement on condition orderings) across the 5-judge primary panel (10 pairs). Krippendorff α (ordinal) = 0.659 across the 5-judge primary panel (substantial); drops to 0.535 with both Gemini judges included due to systematic Gemini inflation.

**Paper:** v10.1 §3.7, §4.6 (Robustness). **DATA_REFERENCE:** §2, §9.

## m7. Letta's archival-retrieval path is not its strength

**Finding:** Letta's source-attachment / archival-retrieval path (tested in v10.1 §4.4) produces near-null spec-delta in the native config (−0.02 on the 5-judge primary, all 14) and modest positive in controlled (+0.20 5-judge primary). Letta's signature mechanism is the stateful-agent path (§4.5, M5), which produces an interpretive memory block that, served to Haiku, scores higher than the BL full-stack specification on all three subjects tested (5-judge primary Δ +0.27 / +1.21 / +0.38). The architecture that does the interpretive work is the conversation loop with memory-block editing, not the archival store.

**Paper:** v10.1 §4.4 scope caveat, §4.5.

## m8. Supermemory ceiling effect — high baseline retrieval, low spec headroom

**Finding:** Supermemory's C1 baselines are systematically higher than the other systems (mean ~2.65 vs ~2.30). On its own low-baseline subjects (ebers, babur, yung_wing) the spec still helps. On its high-baseline subjects, the spec hurts (model has already committed; spec adds competing signal). Aggregate near-zero is a *retrieval distribution* artifact, not a spec failure mechanism.

**Paper:** §4.4 finding #2, §5.7.

## m9. Letta block scaling is sub-linear but ceiling-bound

**Finding:** Per-chunk additions to Letta's `human` block:
- Hamerton: ~749 chars/chunk (30 chunks, ends at 22K)
- Ebers: ~1,315 chars/chunk (52 chunks, ends at 68K)
- Babur: ~625 chars/chunk early, slowing as it grows, hard wall at 333K (chunks 221-242 fail)

Compression rate (corpus/block, words):
- Hamerton: 25K/3.2K = 7.9×
- Ebers: 48K/9.6K = 5.0×
- Babur: 223K/45K = 5.0× (but with 25% duplication, effective unique compression ~6.7×)

**Paper:** §4.5. **DATA_REFERENCE:** §7.

## m10. Specification stability — temperature 0 not perfectly deterministic

**Finding:** Re-generating the spec for the same subject at temperature=0 produces 45% exact-text match across runs but >95% semantic similarity. The spec is semantically stable; sentence-level variation is from local non-determinism in the authoring chain.

**Paper:** §6 Limitations.

## m11. Base Layer retrieval is comparable to commercial systems but not superior

**Finding:** Base Layer's MiniLM-L6-v2 + ChromaDB retrieval produces C1 scores in the same band as the four commercial systems (within 0.05-0.40 points on most subjects). BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias). On no subject does BL's C3 exceed the best commercial C3. **BL is the open-source floor — comparable, not superior.**

**Paper:** §4.4. **DATA_REFERENCE:** §12.

## m12. Wrong-spec v1 vs v2 — different nulls, both below correct-spec

**Finding:** v1 (deterministic fixed cross-subject pairing for the 13 globals, defined in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING and designed to maximize cultural/temporal distance; Hamerton separately paired with Franklin via `run_full_study.py` and reported in §4.1.1) scores below baseline (5-judge primary Δ vs C5 = **−0.25**). v2 (random derangement, seed=42) scores between baseline and correct spec (5-judge primary Δ vs C5 = **+0.15**). v1 is a cleaner null because the pairings were hand-chosen to put each subject alongside a structurally distant other; v2 admits accidental loose similarity from random pairing. (Legacy 7-judge level scores: v1 = 1.86, v2 = 2.30; baseline 2.02. The 5-judge primary Δs above are v10.1 canonical.)

**Paper:** §4.3.

## m13. Models can detect incongruent specs

**Finding:** In wrong-spec responses, the model frequently flags the mismatch explicitly ("this specification describes someone fundamentally different from [subject]") and either refuses or hedges. The wrong-spec score distribution is bimodal: detection-plus-refusal vs misapplied-interpretation. Both pathways confirm content matters.

**Paper:** §4.3.

## m14. Two subjects where spec hurts: Zitkala-Sa and Equiano

**Finding:** Both have C5 baselines near the high end of the low-baseline range (Zitkala-Sa 2.60, Equiano 2.93). Spec produces negative Δ (−0.41, −0.24). Likely mechanism: model has partial pretraining knowledge that conflicts with the spec's interpretive frame. §4.1 (and §4.6 robustness) explores hypotheses (pretraining sufficiency / spec misalignment / retrieval interference); pretraining sufficiency preferred. [CHECK: v9 has no §4.1.3 subsection; failure-mode content folded into §4.1 narrative.]

**Paper:** §4.1 [CHECK].

## m15. Mixture-not-cancellation is system-general

**Finding:** Paired C1 vs. C3 analysis across all 5 memory systems (Mem0, Letta archival, Zep, Supermemory, Base Layer retrieval) shows near-null aggregate deltas hide bilateral per-question swings. Supermemory Ebers (aggregate Δ +0.21): 19 of 39 helped, 10 hurt. Supermemory Keckley (aggregate Δ −0.26): 10 helped, 17 hurt. Same shape reproduces on Mem0, Letta, Zep, BL at varying magnitudes. Per-question effects are often large (>0.3 points); averaging them hides strong disagreement.

**Paper:** §1.3 "Where the specification helps and where it hurts." Source reports: `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `mem0_letta_zep_c1_vs_c3_analysis.md`, `baselayer_c1_vs_c3_paired_analysis.md`.

## m16. Keckley Q21 refusal is a specification-level dynamic

**Finding:** On the question "How does Elizabeth explain her decision not to visit her mother's grave?", the specification's documented-dignity axioms induce refusal — the response model declines to fabricate interior motive when the retrieved facts do not contain it. Reproduces across all 5 memory systems at penalty proportional to each system's retrieval-only counterfactual: Supermemory −2.33, Base Layer −2.33, Mem0 −0.50, Zep −0.50, Letta +1.00 (net positive because C1 was already weak). The content-match rubric scores epistemically-honest refusals identically to off-base guesses. **This is a spec-level pattern, not a memory-system artifact.**

**Paper:** §1.3 (Where helps vs. hurts). Source: paired analysis reports.

## m17. Three failure modes of specification-based reasoning are system-general

**Finding:** Paired analyses surface three spec failure modes that reproduce across systems:
- **Over-theorization on literal-recall questions** (spec-driven elaboration drifts past a plain answer)
- **Spec-induced refusals** (axioms designed to prevent fabrication also prevent productive speculation)
- **Default-axiom overfires** on counter-example moments (subject departs from their own modal pattern; spec encodes the default)

Each reproduces on multiple systems. Supermemory Sunity Devee Q11 (hierarchical deference axiom A4 overrides explicit accusatory tone) and Mem0 Ebers Q1 (love-not-duty axiom over-conditionalizes unconditional affirmation) are matched default-axiom failures on different systems.

**Paper:** §1.3 (Where helps vs. hurts) + §4.4.2 detail [CHECK: v9 §4.4.2 "Common Mechanisms: Interpretation, Over-theorization, Principled Refusal" maps to two of three failure modes; default-axiom overfires is a closely-related third mode covered in the same section]. Source: paired analysis reports.

## m18. Letta archival retrieval has severe fact duplication

**Finding:** Letta archival-path retrieval has dedup ratio 0.34-0.47 on tested subjects — top-10 retrieval returns only 3-5 unique facts, with the most-repeated fact appearing ~4× on average. Mem0's dedup ratio is 1.00 (every top-10 position is unique). This thin substrate inflates Letta's controlled spec delta (+0.25 aggregate, low-baseline) because the spec has more interpretive gap to close, and also makes Letta C1 hedge into "cannot find direct characterization" responses that the spec layers onto.

**Paper:** §4.4 Letta character sketch (punch-list item to add) [CHECK: v9 has no §4.3.2; provider character sketches live in §4.4 Memory-System Composition]. Source: `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`.

## m19. Base Layer prompt-template hedging hypothesis partially contradicted

**Finding:** §4.4 currently hypothesizes that BL's smaller spec delta (+0.12) is from prompt-template-induced hedging. Paired-response analysis measures hedge-trigger lexicon C1→C3 per subject: ebers 0.31→0.15 (drops), keckley 0.23→0.08 (drops), yung_wing flat, hamerton 0.41→0.69 (rises), babur 0.10→0.28 (rises). Two drop, two rise, one flat — not uniform template bias. Actual pattern: when spec can be retrieval-grounded, C3 hedges *less*; when it cannot, C3 surfaces the ungroundedness explicitly.

**Paper:** §4.4 mechanism claim requires rewrite. Source: `docs/research/baselayer_c1_vs_c3_paired_analysis.md`.

## m20. Wrong-spec detection upper bound: 60.6%

**Finding:** Across 587 classified wrong-spec responses (507 random derangement v2 + 80 Franklin-for-Hamerton v1), validated against 30-response stratified manual spot check (30/30 agreement with classifier), response distribution is bimodal: 60.6% explicit detection/refusal (flag the mismatch, refuse or hedge), 36.5% misapply, 2.0% implicit hedge, 0.9% ambiguous. Detection + misapply = 97.1%; bimodal framing supported. **The 60.6% is content-grounded, not an upper-bound-inflated-by-name-mismatch.** The `spec_production.md` artifacts that feed C2c wrong-spec are already anonymized (empirically verified April 2026 via `docs/research/name_blind_wrong_spec_pilot.md`: zero instances of any subject name across 19 name variants in all 13 global-subject wrong-spec artifacts). Detection works by content inference: temporal markers, cultural domain, life events, characteristic interpretive patterns. Hamerton Franklin-spec 88% explicit; Bernal Diaz 21% explicit; detection depends on how distinguishable the wrong spec is from the true subject at the behavioral-content level.

**Paper:** §1.3 Mechanism + §4.3 expansion. Source: `docs/research/wrong_spec_detection_analysis.md`.

## m21. Provider recall-benchmark claims are contested; methodology is immature

**Finding:** Primary-source audit of the four commercial memory systems' published benchmark scores reveals a contested landscape:
- **Mem0:** Peer-reviewable paper (Chhikara et al. arXiv:2504.19413) reports 68.44% LOCOMO with GPT-4o-mini on the Mem0g graph variant. Current production algorithm, per vendor research page, claims 91.6% LOCOMO and 93.4% LongMemEval. **Evaluation harness is open-sourced at `github.com/mem0ai/memory-benchmarks`** — methodology is publicly reproducible.
- **Letta:** 74.0% LOCOMO with GPT-4o-mini (blog, 2025-08-12). No published LongMemEval score. Letta's public leaderboard at `leaderboard.letta.com` is "Context-Bench" (benchmarking LLMs on agentic tasks), not a memory-system leaderboard.
- **Supermemory:** 81.6% / 84.6% / 85.2% on LongMemEval_s (GPT-4o / GPT-5 / Gemini-3-Pro, self-reported). Published comparison vs. Zep shows ~10-point gap favoring Supermemory on LongMemEval_s overall.
- **Zep:** 71.2% LongMemEval with GPT-4o (Rasmussen et al., arXiv:2501.13956). An earlier Zep claim of 84% LOCOMO was publicly contested by Mem0 in GitHub issue `getzep/zep-papers#5`, with Mem0 alleging Zep included adversarial question categories the benchmark explicitly excludes, modified evaluation prompts and retrieval templates, and reported a single run vs. Mem0's mean-of-ten. Issue closed; methodological disagreement unresolved publicly.

**The real finding:** benchmark construction for conversational memory is immature. Methodology varies significantly between evaluators. Mem0 and Zep publicly disputed each other's LOCOMO numbers; Supermemory publishes direct head-to-head comparisons; third-party reproduction efforts (Vectorize.io) produce different numbers again. The paper's original abstract / §2.1 / §5.7 claim "all four score 85%+ on recall benchmarks" is not defensible from primary sources, but a simple numerical range misses the point. The point is that independent third-party evaluation is needed, and this paper does not attempt to provide it — we measure on a different axis (behavioral prediction) with our own data.

**Paper:** Abstract L217, §2.1, §5.7 L1134 all require sweep. §1.1 (v7 locked) already frames as "68-85% range." §2.1 (v7 locked) includes a dedicated benchmark-dispute note. Source: `docs/research/provider_benchmarks.md`, `docs/research/section_2_1_verification.md`, plus direct WebFetch audit of mem0.ai/research, supermemory.ai/research, leaderboard.letta.com, atlan.com/know/zep-vs-mem0, github.com/getzep/zep-papers/issues/5.

## m22. Author baseline pilot — real user in Hamerton regime

**Finding:** Pilot C5 baseline measurement on the paper's author (private corpus of ~41K user-role messages ≈ 12.2M chars, Haiku no-context, 10 questions, single-judge). Mean C5 = 1.90 (95% CI 1.16-2.64), refusal rate 60%, 50% of responses at rubric floor (score 1). Places the author in the Hamerton (1.41) regime, not Franklin (4.10) regime. Consistent with the paper's claim that typical real AI users are low-baseline. One data point with the right sign and plausible magnitude; N=10 and single-judge are caveats. Stricter re-judging would likely pull mean to ~1.5-1.7.

**Paper:** §1.4 ¶2 (v7 locked). Source: `_internal/aarik_baseline_pilot/` (internal evidence, not in public repo).

---

# OPEN QUESTIONS / FUTURE WORK

## F1. Generalization across 14 subjects for Letta stateful-agent test

Currently n=2 (Hamerton, Ebers) plus partial n=3 (Babur, ceiling-saturated). Full battery against 11 remaining subjects required to confirm Letta's stateful-agent path matches BL's spec on prediction across the full population.

## F2. Living-user replication

The 14 subjects are historical figures with public autobiographies, a sample biased *upward* on pretraining representation. Direct replication on living users with private data is the structural extrapolation that turns the paper's central claim into direct measurement. The low-baseline historical slice is the closest available proxy for typical living users, whose private decisions are not in any training corpus.

## F3. Component ablation of the spec

Anchors vs core vs predictions — which layer carries how much of the prediction-improvement signal? Reviewers (Gemini Pro, Mistral) flagged this as the most important methodological extension.

## F4. Human-judge validation

All judges in this study are LLMs. Human validation on a subset is the standard mitigation for LLM-as-judge concerns.

## F5. Live multi-turn agent tasks

Held-out passage prediction is one task. Live agent workflows with tool use, longer horizons, and genuine multi-turn dynamics are the deployment-relevant tests.

## F6. Independent pretraining-representation proxy

C5 baseline is currently the proxy for "what the model already knows." Mistral suggested independent measures (n-gram frequency, memorization probes) to break the C5-as-proxy circularity concern.

## F7. Supermemory architectural-incompatibility hypothesis test

Is Supermemory's near-zero spec delta truly a ceiling effect, or is there an architectural incompatibility between SM's 5-layer stack and the spec's interpretive structure? Designable test. (Partially resolved by m15 mixture-of-swings finding: the aggregate is not uniform; a differentiated battery separating interpretation from recall would resolve more fully.)

## F8. Zep temporal-graph mechanism direct test

§4.4 framing [CHECK: v9 has no §4.3.2; Zep character sketch lives in §4.4 Memory-System Composition] implies Zep's Graphiti temporal-graph substrate drives its spec layerability. Paired-response analysis (m15 source) found Zep's relational edges are biographically correct but behaviorally thin; spec wins come from axiom inference, not time-anchored retrieval. Whether temporal structure is load-bearing or ornamental for this task needs a direct test (time-inversion ablation, temporal-reasoning-specific battery).

## F9. Name-blind wrong-spec control [RESOLVED April 2026]

Original premise: current wrong-spec controls use named specifications, so the 60.6% detection rate (m20) includes trivial name-mismatch. Resolution: empirically tested and falsified. The `spec_production.md` artifacts used by C2c are already fully anonymized (zero subject-name instances across 13 files, 19 name variants checked). See `docs/research/name_blind_wrong_spec_pilot.md`. The 60.6% stands as a content-grounded detection rate.

## F10. Anonymized vs. named BL spec on low-baseline subjects

BL specs are authored with "this person" anonymization. On low-baseline subjects where the response model has no pretraining footing, the anonymization + epistemic-honesty axioms compose into refusals. Letta's stateful-agent block names the subject directly and avoids this. A de-anonymized rerun of BL C2a against Letta's battery is in progress (agent pending). If the gap narrows substantially, §4.5 architectural-convergence framing needs refinement.

## F11. Differentiated battery — interpretation-only

Current battery mixes interpretation-heavy questions (where spec helps) with literal-recall questions (where spec hurts or theorizes past a plain answer). A battery that deliberately targets only cross-domain generalization or counterfactual-from-axiom reasoning would isolate the spec's interpretive contribution cleanly. This would also resolve the "are facts enough when well-retrieved" question (addressed partially by Supermemory paired analysis, m15).

---

# MEMORY-SYSTEM CHARACTER (per-provider summary)

Compact per-provider read with references to the major findings that apply to each. Full detail in paired-analysis reports under `docs/research/`.

All numbers below are 5-judge primary unless explicitly marked as 7-judge sensitivity. Source: v10.1 §4.4.

## Mem0
- Most reliable baseline in the study. Positive spec delta in both configurations (5-judge primary: +0.12 controlled, +0.33 native).
- Mixture-of-swings: moderate (m15). Yung Wing swing distribution 21/6/12 is illustrative; large wins coexist with large losses even when the aggregate is positive.
- Reproduces default-axiom overfire failure on Ebers Q1 (love-not-duty axiom over-conditionalizes; similar to Supermemory Sunity Q11).
- Dedup ratio 1.00 (clean retrieval, no duplication).

## Letta (archival-retrieval path)
- 5-judge primary: −0.02 native, +0.20 controlled.
- **Severe fact-duplication** (m18): dedup 0.34-0.47, top-10 returns 3-5 unique facts. Thin substrate inflates spec delta in controlled config.
- C1 hedges frequently ("cannot find direct characterization") because retrieval is thin.
- See also Letta stateful path below.

## Letta (stateful-agent path)
- Signature architecture (MemGPT paper, Packer et al. arXiv:2310.08560). Self-editing memory block during multi-turn conversation.
- n=3 subjects tested (Hamerton, Ebers, Babur) (M5, M6, M7).
- Scaling ceiling: block grows linearly with corpus size; saturates near Letta's per-message API ceiling (~333K characters, observed on Babur).
- 25.4% verbatim sentence duplication at Babur scale (M7).
- Letta block scores higher than the BL full-stack specification at matched response model on all 3 subjects tested (5-judge primary Δ +0.27 / +1.21 / +0.38). v12.1 §4.5 reports this as exploratory at n=3, not a primary result. **Anonymization asymmetry** (Letta ingested named corpora; Base Layer authoring strips the subject name) is flagged as a methodological gap (§7.5).
- Architecturally the only system in the study that autonomously builds an interpretive representation from multi-turn interaction.

## Zep
- Strongest and most consistent positive spec delta (5-judge primary: +0.19 controlled, +0.33 native). 9 of 9 low-baseline subjects positive in native; 9 of 9 positive in controlled on the low-baseline slice.
- Wilcoxon C1 vs C3 within-system: controlled p = 0.0004, native p = 0.0015 (both robust at α = 0.01).
- Mixture-of-swings present but cleanest distribution of the four: 0-1 big-losses on Ebers and Seacole.
- Holds the largest single swing observed: Seacole Q2 = +4.00 (C1 unanimous 1s → C3 unanimous 5s; m15).
- **Open question (F8):** paired-response analysis suggests Zep's temporal-graph edges are biographically correct but behaviorally thin; spec wins come from axiom inference, not time-anchored retrieval. v10 §4.4 names the verbose-relational-structure-leaves-room-for-axioms hypothesis but does not test it directly.

## Supermemory
- Strongest standalone retrieval (C1 mean ~2.65 vs. ~2.30 for others on 1-5 scale).
- 5-judge primary spec delta: −0.05 controlled (all 14), −0.01 controlled (low-baseline). Native paid-tier rerun (2026-04-23, n=14): −0.01 all-14, −0.03 low-baseline.
- **Most pronounced mixture-of-swings** (v10.1 §4.4 Supermemory section, updated 2026-04-25 to the strict 5-judge primary panel): of 546 paired questions, 110 (20.1%) shifted by ≥1.0 rubric point; 57 improvements at mean +1.55, 53 regressions at mean −1.38. Roughly cancels at the aggregate. Prior audit-panel values (89/516 (17.2%); 37 helps mean +1.45 / 52 hurts mean −1.41) preserved here for cross-reference; the 5-judge primary panel adds 30 NO_RETRIEVAL responses the audit panel had dropped, shifting the helps/hurts mixture upward at both tails.
- Keckley Q21 refusal case: −2.33 penalty (m16).
- 85.2% LongMemEval_s with Gemini-3-Pro is the only primary-source 85%+ benchmark number across all 4 commercial providers (m21).

## Base Layer (substrate)
- Open-source retrieval floor (MiniLM-L6-v2 + ChromaDB). Not positioned as a memory product.
- Mean C1 ~2.30 across 14 subjects, in the same band as commercial systems. 5-judge primary spec delta +0.08 controlled aggregate; +0.08 on low-baseline.
- Comparable, not superior (m11 confirmed from paired-response side).
- **Hedging-hypothesis partially contradicted (m19):** the prompt-template-induced-hedging explanation is not supported by paired-response measurement.
- Keckley Q21 refusal reproduces with substantial penalty — confirms m16 as spec-level universal.

---

# SUMMARY TABLE

| Finding ID | Type | Status | Paper section |
|---|---|---|---|
| M1. Gradient | Major | ✓ Tested, supported | §4.1 |
| M2. Spec improves three of four memory systems on population of interest | Major | ✓ Tested, supported | §4.4 |
| M3. Wrong-spec controls fail | Major | ✓ Tested, supported | §4.3 |
| M4. Memory systems do not converge on relevance given identical input (mean Jaccard 0.083 across 5 systems) | Major | ✓ Tested, supported | §4.4 |
| M5. Letta stateful-agent reaches BL spec band at matched-model | Major | ✓ Tested (n=3, exploratory) | §4.5 |
| M6. Letta scaling ceiling at 333K chars | Major | ✓ Tested, observed | §4.5 |
| M7. Letta block becomes 25% duplicative at scale | Major | ✓ Tested, observed | §4.5 |
| M8. Spec exceeds raw corpus at 22% the tokens | Major | ✓ Tested, supported | §4.2 |
| M9. Cross-provider replication 5/6 | Major | ✓ Tested, supported | §4.6.1 |
| m1-m14 | Minor | ✓ Various | various |
| F1-F7 | Open | Future work | §7 |

All findings trace to source files documented in `DATA_REFERENCE.md` §K (Provenance).

---

## S114 Additions (2026-04-21)

### New major findings

| # | Finding | Evidence | Paper section |
|---|---|---|---|
| M10 | **Per-response anchor-crossing rate 55.0% on low-baseline slice** (193 of 351 responses moved up at least one rubric integer anchor with spec; only 6.8% moved down) | `scripts/compute_anchor_crossing.py` | §4.1 |
| M11 | **Question-improvement rate 70.9% on spec-alone, low-baseline** (249 improve / 49 tie / 53 worsen); median Δ when improved = +1.00 (full rubric anchor) | `scripts/compute_question_improvement_rate.py` | §4.2.1 |
| M12 | **Compression efficiency: spec at ~5% of corpus context captures ~77% of corpus lift.** Mean C8 − C2a gap = +0.22 across 9 low-baseline subjects | `docs/research/recompute_5judge_primary.md` | §4.2 |
| M14 | **Spec-activation measurable.** 78.6% of C4a responses cite spec anchor/prediction tags (A1..An, P1..Pn). Wrong-spec cites at only 50.0% — partial content filtering. | `docs/research/spec_activation_analysis.json` | §4.3 (pending) |

### New minor findings

| # | Finding | Evidence | Paper section |
|---|---|---|---|
| m23 | **Rubric does not cleanly distinguish abstention from wrong prediction.** 9.4% of abstention-pattern responses scored ≥ 2.0 (mean 1.27, 82.8% clean). Bidirectional: abstentions can be over-credited (Seacole Q2 at 2.80) and spec-induced honest abstentions can be penalized (Keckley Q21). | `scripts/audit_low_end_inflation.py` | §3.7.6 |
| m24 | **Length-score correlation r = 0.604 within C5 baseline only.** Spec-containing conditions show near-zero length correlation. Verbose baseline hedging partially credited. Direction of bias: true spec-effect gap is larger than reported. | Same audit | §3.7.6, §4.1 |
| m25 | **Per-judge strictness on abstentions varies 0.27 points.** Sonnet strictest (1.14), Opus most lenient (1.41). | Same audit | §3.7.6 |
### New open questions

| # | Question | Status | Follow-up section |
|---|---|---|---|
| F8 | Multi-subject living-user replication. | Planned | §7 Future Work |
| F9 | Differentiated rubric that scores abstention as its own dimension. | Planned | §7 Future Work |
| F10 | Length-controlled scoring protocol. | Planned | §7 Future Work |
| F11 | Component ablation (anchors vs. core vs. predictions). | Planned | §7 Future Work |
| F12 | Cross-provider specification portability. | Open | §7 Future Work |

### Title change (S114)

Changed from "Missing Primitive" to **"An Interpretive Layer"** after 6-provider unanimous vote. "Missing Primitive" was a field-level foundational claim the empirical work does not support. "Interpretive Layer" names the artifact's function accurately.

### Methodology change (S114)

Primary judge panel: 5-judge non-Gemini (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). 7-judge is sensitivity check. See `agents/STUDY_MEMORY.md` + paper §3.7.2 for full reasoning.

### Benchmark metric proposal (S114)

Per-question win rate against no-context baseline + median magnitudes (reporting triplet). Framed as secondary reporting axis, not primary benchmark. Panel unanimous on scoping. See §4.2.1.
