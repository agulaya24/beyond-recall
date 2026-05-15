# Data Reference — Single Source of Truth

**Canonical paper:** `docs/beyond_recall_v12_1_draft.md` (v12.1, active edit branch as of 2026-05-13 — applying Aarik's 211-comment review pass + final-checks audit fixes). v12 docx retained as historical baseline with comments preserved.

**Generated:** 2026-04-18 from `data/experiments/memory_systems/results/RESULTS_S113.json`. **Updated 2026-04-25 (v10.1 point release)** to match the v10.1 paper's 5-judge primary panel: Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4. The legacy 7-judge mixed panel (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported as a sensitivity check where it materially changes a number; the primary aggregate excludes the Gemini pair per §3.7.2 of the paper.

**How to read this doc.** Each numbered section is a self-contained experiment result. Each section contains:

- **Label** — the condition name used elsewhere in the paper
- **One-line summary** — what this data says in one sentence
- **Data table** — the numbers themselves (5-judge primary unless explicitly marked sensitivity)
- **Bounded interpretation** — what to conclude from this data alone, without needing other sections
- **Paper location** — where this appears in `docs/beyond_recall_v12_1_draft.md`

All scores are on the 1-5 behavioral-prediction scale. Every number traces back to source files listed in §K.

> **v11 active-editing note (2026-04-27 / 2026-04-28).** This file is anchored to v10.1's section numbering; v10.1 remains the citable canonical paper. v11 (`docs/beyond_recall_v11_draft.md`) is the active edit branch and has shifted some section numbers. When chasing a paper-section reference from this file into v11, apply these mappings: §2.3 / §2.3.1 (memory and personalization benchmarks) merged into v11 §2.1; v10.1 §3.7.2 (Calibration) is v11 §3.6.3; v10.1 §3.7.3 (Fractional score interpretation / cross-anchor rule) is v11 §3.6.2; v10.1 §4.1.1 (Franklin high-baseline reference) moved to v11 §4.6.4; v11 added a new §4.4.4 (Two statistical signatures) and a new §4.7 closing paragraph; v11 added §3.6.6 (Rubric-handling limitations / validity audit). Numerical entries (5-judge primary panel) carry forward unchanged into v11; v11 paper-numbers verification at `docs/research/v11_paper_numbers_verification_20260428.md` shows 298 of 312 audited numerics MATCH, 10 MINOR_ROUNDING, 4 MISMATCH (all flagged for paper edit, not silent reconciliation).

### v11 numerical additions and reconciliations (2026-04-28)

These are values v11 paper text references that v10.1 did not. All carry from artifacts in `docs/research/*_20260428.*`; provenance for each is in `PROVENANCE_INDEX.md` "v11 research artifacts added 2026-04-28" table.

- **Per-question anchor-crossing analysis: 18 condition pairs.** Wins inventory at `docs/research/wins_inventory_20260428.json` analyzes 18 paired condition pairs across direct, corpus, and memory-system layering. 4,206 anchor crossings + 759 same-band ≥0.5 within-band shifts + 995 same-band 0.25-0.5 shifts (per `within_band_shifts_20260428.{json,md}`). 150 paired questions show extreme upward jumps (≥3 bands); **60 unique** extreme upward (subject, qid) cases after dedup. Cited in v11 §1.3 (multi-anchor 18% / extreme 6% framing) and §4.4.2 footnote. Script: `scripts/build_wins_inventory.py`.
- **Multi-anchor jump rates (low-baseline slice, C5→C4a).** 18% of low-baseline questions show multi-anchor jumps (≥2 bands); 6% show extreme jumps (≥3 bands). Direction asymmetry: across the full 14-subject panel, **no question** crosses from band 2, 3, or 4 into band 5; only band-1 → band-5 transitions reach the ceiling. Cited in v11 §1.3 callout. Source: `wins_inventory_20260428.json`. (Note: corrects a broken "5-10%" wording in earlier v11 drafts.)
- **C9 vs C8 mean Δ on per-question paired recompute: +0.09.** v11 §4.2 within-band table (line 802-805) shows mean Δ = +0.09 for both C4a vs C4 and C9 vs C8 on the 351 / 312 paired-question slice. The per-subject mean column at the bottom of the per-subject compression table reads C9 = 2.59 vs C8 = 2.45 (cross-subject mean = +0.14 at the per-subject grain); the canonical comparison number is the per-question paired Δ = +0.09. Source: `docs/research/per_question_anchor_crossing_extended_20260428.json`. Script: `scripts/compute_anchor_crossing_c4a_c4_and_c9_c8.py`.
- **Half-anchor metric is 18% lossy** (methodological note added in v11 §3.6.2). For every 1 anchor crossing, ~0.18 additional same-band ≥0.5 shifts exist that the binary anchor-crossing metric does not record. The panel detects sub-anchor signal cleanly: 74% direction-agreement at panel |Δ| 0.1-0.25, 93% at 0.25-0.5, 99.9% at panel |Δ| ≥ 1.0. Source: `within_band_shifts_20260428.{json,md}`. Script: `scripts/within_band_and_meta_judging.py`.
- **Two statistical signatures (v11 §4.4.4 NEW).** Pre-vs-post Spearman ρ across questions:
  - C5 → C4a (spec on baseline) ρ = **0.27** (re-ranks)
  - C4 → C4a (spec added to facts) ρ = **0.72** (uniform lift)
  - C8 → C9 (spec added to corpus) ρ = **0.71** (uniform lift)
  - C2a → C4a (facts added to spec) ρ = **0.62** (mid; partial re-ranking)

  Statistical signatures, not separately attributable mechanisms. Floor-effect alternative not ruled out (spec-on-baseline scores cluster near rubric floor where re-ranking is structurally easier). Source: `within_band_shifts_20260428.{json,md}`.
- **Predicate ablation (v11 Appendix B.8 NEW).** 16 stratified extreme-upward-jump cases. Mean Δ_removal = **+0.05** (CI95 [−0.35, +0.45]); mean Δ_reversal = **−0.24** (CI95 [−0.45, −0.02]); 11 of 16 cases Δ_removal < 0.5; 2 of 16 cases Δ_removal ≥ 1 (bernal_diaz q16, rousseau q28). Original-condition reproduction drift mean = −1.44 anchors (stochasticity caveat). Verdict: NOT_SUPPORTED for the strong predicate-mediated mechanism claim; consistent with redundant spec construction. Sources: `predicate_ablation_results_20260428.{json,md}`, `predicate_ablation_sampling_20260428.json`. Script: `scripts/run_predicate_ablation.py`.
- **Held-out leakage audit on the 60 extreme-upward-jump cases (v11 §3.3 footnote).** 0 6-gram, 2 4-gram, 12 3-gram leaks at C4a; severity verdict RARE. Most concerning case: hamerton q51 (`as much as possible`, CORPUS_LEAK 4-gram). Recommended paper treatment: footnote acknowledgement sufficient. Source: `held_out_leakage_investigation_20260428.{json,md}`. Script: `scripts/investigate_held_out_leakage.py`.
- **Hamerton confound (v11 Appendix B.6.5).** Hamerton served spec is **1,918 words** (`data/hamerton/spec/brief_v5_clean.md`, brief-only); globals' served spec averages **~5,775 words** (`data/global_subjects/<subject>/spec_production.md`, anchors + core + predictions + brief). Hamerton extreme-jump rate is **18.75%** (15 of 80 questions); globals average **8.9%** (45 of 13 × 39 = 507 questions); Hamerton's rate is 2.1× globals'. Spec length is anti-correlated with extreme-jump rate; cause not isolated by present design. Candidate explanations (legacy battery generator path, subject pretraining thinness, predicate density per word) are not separately identifiable. v11 §4.1 / Appendix B.6.5 cite this verbatim; the inversion corrects an earlier-draft Stream X claim that "Hamerton has the long unified-brief vs. globals' six-section spec." Source: `hamerton_confound_note_20260428.md`.
- **Pattern-activation deep analysis (v11 §4.4.2 caveat).** Heuristic-level pattern-activation claim falsified: fair-comparison spec_doing_work rate on extreme jumps is 78.9% (n=38) vs non-jumping spec-loaded controls 80.6% (n=36); Δ = −1.7pp. The heuristic detects "response generated under spec-loaded condition," not "spec drove the lift." Surviving narrower claim: 11 of 60 INFERENCE_CHAIN cases verdict `genuine_inference_via_spec` (vs 2 of 38 controls; ~1 in 6 extreme upward anchor crossings shows specification-enabled inference). Source: `pattern_activation_deep_20260428.{json,md}`. Script: `scripts/deep_pattern_activation_analysis.py`.
- **Per-question improvement rate on the all-14 panel (v11 §4.2.1).** v11 paper §4.2.1 reports 64.5% / 24.5% improvement / worsening for C8 on all-14; verification scaffold gives 65.2% / 23.6%. Sub-1pp drift; 4 of 312 audited numerics in `v11_paper_numbers_verification_20260428.md` are MISMATCH (Supermemory controlled Δ all-14 sign and improved-count, all-14 C8 improvement / worsening rate). Pending paper edit, not silent reconciliation here.

### Per-system anchor-crossing (added 2026-04-27 for v11 §1.3 + §4.4.1)

The cross-system anchor-crossing analysis on the low-baseline 9 lives at `docs/research/per_system_anchor_crossing_20260427.md` and `docs/research/per_system_anchor_crossing_20260427.json`; the computing script is `scripts/compute_per_system_anchor_crossing.py`. Aggregation rule: per-judge per-question score, mean across the 5 primary judges, paired C1_<sys> -> C3_<sys> per (subject, question). Upward = response moves across an integer rubric anchor in the upward direction.

| System | Configuration | Low-baseline N questions | Upward % | Subjects with >= 1 upward (of 9) |
|---|---|---:|---:|---:|
| Mem0 | controlled | 351 | 23.4% | 9 |
| Mem0 | native | 349 | 36.1% | 9 |
| Letta archival | controlled | 350 | 26.9% | 9 |
| Letta archival | native | 351 | 19.9% | 9 |
| Zep | controlled | 351 | 27.9% | 9 |
| Zep | native | 351 | 32.5% | 9 |
| Supermemory | controlled | 351 | 20.2% | 9 |
| Supermemory | native | 154 | 23.4% | 6 (partial coverage; Bernal Diaz + Babur excluded) |
| Base Layer | controlled | 348 | 29.0% | 9 |

Base Layer has no native (`_fp`) configuration by design (it IS the full pipeline; no separate native ingestion path). Letta stateful path is out of scope (separate exploratory case study; see §7). Multi-anchor jumps (1 -> 3, 1 -> 4, 2 -> 4, 2 -> 5) appear at low frequency but high magnitude on every system; per-boundary breakdowns are in the source `.md`.

This data closes v11 comment C131 (per-system anchor-crossing for §4.4.1) and feeds the v11 §1.3 Memory-system layering bullet.

**Population-of-interest framing.** The 9 "low-baseline" subjects (C5 ≤ 2.0) are the sample subset whose baseline is low enough to matter. The low-baseline historical slice is the *closest available proxy* for typical living users, whose private decisions are not in any training corpus. The structural extrapolation (low-baseline historical figures sit near the rubric floor; the spec is uniformly beneficial there; living users are reasonably expected to land in the same band) is what the v10.1 paper claims, not direct measurement. Use this framing whenever the low-baseline result is quoted; per v10.1 §1.4, direct living-user replication is required before deployment claims can be validated empirically rather than structurally.

---

## 1. THE GRADIENT — Spec effect vs. baseline knowledge (14 subjects, 5-judge primary)

**Label:** Gradient. 14 public-domain autobiographical subjects. **5-judge primary panel** (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).
**One-line summary:** The worse the model's pretraining knows the subject, the more the spec helps; on the low-baseline slice (the population of interest), 9 of 9 subjects improve.

**Data (ordered by C5 baseline, ascending; v10.1 §4.1 per-subject table, line 718):**

| Subject | C5 baseline | C2a spec only | C4a facts+spec | Δ spec | Δ facts+spec | Anchor crossed |
|---|---:|---:|---:|---:|---:|:-:|
| ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | yes |
| sunity_devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | yes |
| hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | yes |
| fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | yes |
| bernal_diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | partial |
| babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | no |
| seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | yes |
| keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | no |
| yung_wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | no |
| *— low-baseline cutoff (C5 ≤ 2.0) —* | | | | | | |
| zitkala_sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | no |
| cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | no |
| rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | no |
| augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | no |
| equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | no |

**Aggregates (5-judge primary, recomputed from the per-subject table):**
- All 14: mean Δ spec = +0.43, mean Δ facts+spec = +0.55, positive on 12 of 14 for Δ_C4a (Zitkala-Sa, Equiano negative)
- Low-baseline only (n=9): mean Δ spec = +0.69, mean Δ facts+spec = **+0.89**, positive on **9 of 9**
- Mid-baseline (n=5, 2.0 < C5 < 3.0): mean Δ facts+spec = −0.06, positive on 3 of 5
- Mean C4a across all 14 = **2.44** (the spec ceiling: roughly constant across the C5 range; see §2 coupling reframing)

**7-judge sensitivity (legacy S113 panel, retained for reference):** All-14 mean Δ_facts+spec = +0.67; low-baseline (n=9) mean Δ_facts+spec = +1.04; positive on 9 of 9. The 7-judge values are systematically higher than the 5-judge primary because Gemini Flash and Gemini Pro inflate scores by roughly +1.0 point each (§9). Direction and rank order match across panels; magnitudes differ.

**Interpretation (bounded to this experiment):**
- The spec helps more where the baseline is lower. The effect is a gradient, not a binary.
- On the low-baseline slice (the 9 subjects that approximate real AI users), the spec is uniformly beneficial. No exceptions.
- Two subjects decline (Zitkala-Sa, Equiano); both sit in the mid-baseline band where pretraining coverage is more substantial. Consistent with the gradient mechanism.

**Paper location:** v10.1 §4.1 (Table at line 718). Appendix D.1 reproduces the same table at line 2116.

---

## 2. STATISTICAL TESTS — Gradient significance (5-judge primary)

**Label:** Gradient statistical significance.
**One-line summary:** The change-score parameterization gives a steep negative slope; the level regression triangulates that the spec produces a roughly constant C4a near 2.44 across the C5 range (the canonical 5-judge primary all-14 value, per §1 line 93).

| Test | 5-judge primary value (canonical) | 7-judge sensitivity |
|---|---|---|
| Wilcoxon signed-rank, C5 vs C2a (N=14) | W = 10, p = 0.005 | W = 10.0, p = 0.0076 |
| Wilcoxon signed-rank, C5 vs C4a (N=14) | W = 11, p = 0.007 | W = 9.0, p = 0.0063 |
| Δ_C4a-on-C5 regression slope | **−0.96** | −0.98 |
| Slope 95% CI | **[−1.24, −0.67]** | [−1.30, −0.74] |
| R² | **0.82** | ~0.82 |
| Slope p-value | < 0.001 (0.000009) | < 0.001 |
| Krippendorff α (ordinal) | 0.659 (5-judge primary, substantial agreement) | 0.535 (7-judge, moderate agreement) |
| Pairwise Spearman ρ across judges | 0.86 – 0.93 (5-judge primary, 10 pairs) | 0.89 – 0.98 (7-judge historical 4-judge Hamerton; see KEY_FINDINGS m6 and PAPER_CORRECTIONS S113-L) |

**Battery-composition sensitivity (v10.1 §4.1, line 749):**
- Multiple regression of Δ_C4a on C5 baseline + LITERAL_RECALL fraction (N=14): partial slope on baseline = **−0.88 [95% CI −1.13, −0.63], p < 10⁻⁵**, attenuated about 8% from the univariate −0.96. Adjusted R² rises from 0.80 to 0.87. LITERAL_RECALL fraction enters as a significant partial predictor (β = +2.30 [+0.34, +4.26], p = 0.026). Pearson r between predictors = −0.28; VIF = 1.08.
- Subset regression on the 13 GPT-5.4-battery subjects (drops Hamerton's legacy Haiku-generated battery): slope = **−0.89 [95% CI −1.18, −0.61], R² = 0.81, p < 10⁻⁴**. About 7% attenuation from the full-sample −0.96. CIs overlap substantially.
- Reproducibility script: `scripts/_v10_battery_sensitivity.py`. Full report: `docs/research/v10_battery_sensitivity_analysis.md`.

**Coupling-free reframing (v10.1 §4.1, line 755):**
- The headline regression is Δ_C4a = C4a − C5 on C5; this mechanically embeds a −1 component on a bounded 1-5 scale. Three checks triangulate from a non-coupling-prone angle.
- Level regression C4a ~ C5: slope = **+0.04 [95% CI −0.24, +0.33], R² = 0.008, p = 0.76**. C4a is essentially flat across the C5 range of 1.02-2.77 and clusters tightly around its mean of **2.46**.
- Permutation null (10,000 iterations, shuffles C4a across subjects): centered at −0.998 (SD 0.127); observed −0.960 not extreme (two-sided p = 0.77). The mechanical −1 anchor is what the permutation null reproduces.
- Subject-level bootstrap (10,000 iterations): Δ-on-C5 slope CI = [−1.254, −0.740]; level slope CI = [−0.254, +0.260] (straddles zero).
- **Honest reframing:** the gradient is "the spec produces a roughly constant C4a near 2.5 across baselines spanning 1.0-2.8, so the lift in raw points is mechanically larger where the floor is lower" rather than "low-baseline subjects benefit differentially more from the spec" in a treatment-effect-heterogeneity sense. The substantive finding survives; the framing of the §4.1 prose follows the reframing.
- Reproducibility script: `scripts/_v10_coupling_sensitivity.py`. Full report: `docs/research/v10_coupling_sensitivity_analysis.md`.

**Interpretation (bounded):**
- p < 0.01 on both Wilcoxon tests (5-judge primary). Aggregate improvement is reliably positive.
- The Δ-on-C5 slope is dominated by the coupling identity slope_Δ = slope_level − 1, not by independent treatment-effect heterogeneity. Practical claim ("spec is the tool for the unknown") survives; treatment-effect-heterogeneity interpretation does not.
- Battery-composition controls do not overturn the gradient. Slope holds at −0.88 controlling for LITERAL_RECALL fraction; holds at −0.89 dropping Hamerton.

**Paper location:** v10.1 §4.1 (lines 686-694 headline; lines 747-759 sensitivity + coupling reframing). Appendix B.6 (battery-question-type breakdown).

---

## 3. MEMORY SYSTEMS × SPEC — Aggregate spec-delta (all 14 subjects)

**Label:** Memory system × spec table. Mem0/Letta/Supermemory/Zep/BaseLayer, two configs each.
**One-line summary:** Adding the Base Layer spec to any of the 4 commercial memory systems produces positive delta in at least one configuration; 3 of the 4 are positive in both.

**Controlled configuration** (5-judge primary panel, all systems given identical extracted fact set):

| System | Mean Δ (C3 − C1) | Subjects positive (of 14) | Low-baseline mean Δ | Low-baseline positive (of 9) |
|---|---:|---:|---:|---:|
| Mem0 | +0.12 | 10 | +0.10 | 6 |
| Letta (archival) | +0.20 | 12 | +0.17 | 8 |
| Zep | +0.19 | 13 | +0.17 | 9 |
| Supermemory | −0.05 | 5 | −0.01 | 5 |
| Base Layer | +0.08 | 9 | +0.08 | 6 |

**Native configuration** (5-judge primary panel; each system runs its own ingestion pipeline on raw corpus):

| System | Mean Δ (C3 − C1) | Subjects positive (of 14) | Low-baseline mean Δ | Low-baseline positive (of 9) |
|---|---:|---:|---:|---:|
| Mem0 | +0.33 | 10 | +0.32 | 7 |
| Letta (archival) | −0.02 | 5 | −0.04 | 4 |
| Zep | +0.33 | 13 | +0.30 | 9 |
| Supermemory (n=14, paid-tier rerun 2026-04-23) | −0.01 | 6 | −0.03 | 4 |

Wilcoxon (low-baseline, controlled): Zep p = 0.0004, Letta p = 0.0017 robust at α = 0.01; others not significant on n=9. Native: Zep p = 0.0015, Mem0 p = 0.0088 robust.

**7-judge sensitivity (legacy, for reference):** controlled Mem0 +0.15, Letta +0.25, Zep +0.22, Supermemory −0.04, Base Layer +0.12. Direction matches across panels; magnitudes are ~0.05-0.06 higher than 5-judge primary because Gemini Flash and Gemini Pro inflate scores by roughly +1 point each. Source: `RESULTS_S113.json` > `memory_systems`.

**Interpretation (bounded):**
- Controlled config: 4 of 5 systems positive (all except Supermemory, which is near-zero).
- Native config: Mem0 and Zep clearly positive; Letta archival null; Supermemory near-zero.
- The Letta native null is explained by architectural path: archival retrieval is not Letta's signature mechanism. The stateful-agent path is reported separately in §4.5 (and §K below).
- Supermemory aggregate is near-zero on its high-baseline subjects; see §4 for the low-baseline breakdown.

**Paper location:** v10.1 §4.4 (Memory-System Composition).

---

## 4. MEMORY SYSTEMS × SPEC ON LOW-BASELINE — Population of interest only

**Label:** Memory system low-baseline slice (C5 ≤ 2.0, n=9 subjects).
**One-line summary:** On the 9 low-baseline subjects (the population approximating real AI users), the Base Layer spec produces positive mean delta on ALL 4 commercial memory systems in the controlled configuration.

**Controlled configuration, low-baseline slice:**

| System | Mean Δ on low-baseline | Positive subjects |
|---|---:|---:|
| Mem0 | +0.13 | 6 of 9 |
| Letta | +0.23 | 7 of 9 |
| Zep | +0.20 | 9 of 9 |
| Supermemory | +0.004 | 5 of 9 |
| Base Layer | +0.13 | 7 of 9 |

**All 5 systems have positive (or barely positive) mean delta on the low-baseline slice.**

**Native configuration, low-baseline slice:**

| System | Mean Δ on low-baseline | Positive subjects |
|---|---:|---:|
| Mem0 | +0.38 | 7 of 9 |
| Letta | −0.01 | 4 of 9 |
| Zep | +0.37 | 9 of 9 |
| Supermemory | −0.03 (n=9) | 4 of 9 |

**Interpretation (bounded):**
- Load-bearing result: in the controlled config, adding the spec improves all 4 commercial memory systems on the population of interest (low-baseline subjects). This generalizes the spec's usefulness across memory-provider architectures.
- Zep is the strongest, most uniform case: 9/9 positive on low-baseline in both configs.
- Supermemory controlled is barely above zero (+0.004); the weakest case but still positive in mean. Its native config is slightly negative, reflecting the ceiling effect.

**Paper location:** v10.1 §4.4 low-baseline rows.

---

## 5. SUPERMEMORY DEEP-DIVE — Per-subject on low-baseline

**Label:** Supermemory per-subject detail, low-baseline only.
**One-line summary:** Supermemory's spec delta is mixed on low-baseline (5 of 9 positive), with positive deltas concentrated on subjects where Supermemory's own retrieval leaves headroom.

| Subject | C5 baseline | C1 (SM alone) | C3 (SM + spec) | Δ |
|---|---:|---:|---:|---:|
| sunity_devee | 1.03 | 2.70 | 2.54 | −0.16 |
| ebers | 1.04 | 2.01 | 2.21 | **+0.20** |
| hamerton | 1.25 | 2.72 | 2.86 | **+0.14** |
| fukuzawa | 1.80 | 2.85 | 2.71 | −0.14 |
| seacole | 1.85 | 2.74 | 2.86 | **+0.12** |
| bernal_diaz | 1.85 | 2.61 | 2.58 | −0.03 |
| keckley | 1.91 | 2.90 | 2.65 | −0.25 |
| yung_wing | 1.96 | 2.47 | 2.58 | **+0.11** |
| babur | 1.98 | 2.03 | 2.08 | **+0.05** |

**Interpretation (bounded):**
- 5 of 9 subjects show positive delta. Aggregate = +0.004.
- On subjects where SM's C1 is low (ebers 2.01, yung_wing 2.47, babur 2.03), the spec adds positive delta consistent with the gradient mechanism.
- On subjects where SM's C1 is already high (fukuzawa 2.85, keckley 2.90), the spec adds negative delta. Retrieval has already captured what it could, and the spec introduces competing signal.
- The overall near-zero aggregate for Supermemory is explained by its retrieval distribution, not by spec failure.

**Paper location:** v10.1 §4.4 Supermemory paragraph.

---

## 6. WRONG-SPEC CONTROLS — Content specificity tests

**Label:** Wrong-spec v1 (fixed derangement) + v2 (random derangement).
**One-line summary:** A subject's spec, when wrong, scores near or below baseline; the correct spec is what produces improvement, not the format.

| Condition | Mean | Δ vs C5 baseline | Δ vs C2a correct spec |
|---|---:|---:|---:|
| C5 (no spec) | 2.02 | — | − |
| C2a (correct spec) | 2.55 | +0.53 | − |
| C2c v1 (fixed derangement; pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING) | 1.86 | −0.16 | −0.69 |
| C2c v2 (random derangement, seed=42) | 2.30 | +0.28 | −0.25 |

5-judge primary recompute (v10.1 §4.3 line 891, 13 globals): mean Δ vs C5 for C2a (correct) **+0.35**, C2c v2 (random derangement) **+0.15**, C2c v1 (fixed derangement) **−0.25**. Direction unchanged across panels, magnitudes shift. See `scripts/compute_wrong_spec_5judge.py`. The level-score table above is the 7-judge sensitivity panel and is retained for reference only; the v10.1 canonical wrong-spec aggregates are the Δ-vs-C5 values quoted in this paragraph.

**Interpretation (bounded):**
- v1 (fixed derangement) is the cleanest null: pairings were hand-chosen to maximize cultural and temporal distance between each subject and its assigned wrong spec (six 2-cycle swaps plus one 5-cycle across 13 subjects), and assigning it produces scores below baseline. Mapping in `scripts/run_global_rerun.py` (WRONG_SPEC_PAIRING, lines 51-60). Hamerton's separate Franklin-for-all comparison (from `run_full_study.py`) is reported in §4.1.1 and is NOT the v1 global-subject control.
- v2 (random derangement) is a noisier null: some random pairings happen to produce loosely similar specs, so v2 is slightly elevated above v1. Still far below correct-spec scores.
- In both v1 and v2, wrong specs do NOT reach correct-spec scores. The content specificity of the correct spec matters.
- Wrong-spec content-grounded detection rate: 60.6% across N=587 classified responses (see KEY_FINDINGS m20).

**Paper location:** v10.1 §4.3 (Specification Content vs. Format).

---

## 7. LETTA STATEFUL-AGENT TEST — Hamerton + Ebers + Babur (n=3)

**Label:** Letta stateful-agent loop, Packer methodology.
**One-line summary:** When Letta's stateful-agent path is invoked properly (turn-by-turn ingestion with self-editing memory blocks), it produces a representation that predicts as well as or better than Base Layer's full-stack spec at matched response model on all three subjects tested.

| Subject | Letta block size | BL spec size | Letta block / BL spec | Letta block + Haiku (5-judge primary) | BL full-stack spec + Haiku (5-judge primary) | Δ |
|---|---:|---:|---:|---:|---:|---:|
| Hamerton | 22,472 chars | 34,579 chars | 0.65× | 3.10 | 2.83 | **+0.27** |
| Ebers | 68,413 chars | 39,708 chars | 1.72× | 2.76 | 1.56 | **+1.21** |
| Babur | 335,349 chars (saturated at chunk 220/242) | 37,063 chars | 9.0× | 2.42 | 2.04 | **+0.38** |

5-judge primary numbers, canonical source `docs/research/_letta_rerun/fullstack_named/5judge_fullstack_results.json`; agree exactly with paper Appendix G.2 and KEY_FINDINGS M5. The comparison baseline is Base Layer's **full-stack Behavioral Specification** (anchors + core + predictions + brief), the same artifact class used in the main-study gradient, at matched response model (Haiku). Hamerton's score is the full-stack spec scored with the consistent short-form judge prompt; Ebers and Bābur are full-stack regenerations on the Letta battery. The earlier 7K-char unified-brief run (Hamerton 2.96 / Ebers 1.72 / Bābur 1.88, Δ +0.14 / +1.05 / +0.54) is superseded and no longer cited in the paper; superseded source `docs/research/_letta_rerun/5judge_primary_results.json`. Reconciliation: `docs/reviews/v12_1_data_naming_review_20260513.md`.

**Direction preserved across all three subjects:** Letta's self-edited block scores higher than the full-stack Behavioral Specification at matched response model on all three. This is the strongest single result in the Letta case study and is reported in Appendix G.

**Hamerton corpus / Letta block scaling:**
- Hamerton: 25,231 source words → 22,472-char block (full ingestion)
- Ebers: 48,161 source words → 68,413-char block (full ingestion)
- Babur: 222,742 source words → 335,349-char block; HTTP 400 rejections began at ~332,585 chars, last 22 chunks (~10% of corpus) failed to ingest

**Block-coherence ceiling at scale (verbatim sentence duplication):** Hamerton 0%, Ebers 0%, Babur **25.4%** (103 of 1,301 sentences). At Babur scale the agent's consolidation loop loses coherence well before the size ceiling. Effective unique content in Babur block ≈ 250K chars, not 335K. See KEY_FINDINGS M6/M7.

**Interpretation (bounded):**
- Generalizes to n=3 across the corpus-size range (25K → 48K → 223K source words).
- Letta's stateful-agent path produces an interpretive representation (not just retrieval). At matched response model it predicts as well as or better than Base Layer's full-stack spec.
- Block grows ~linearly with corpus; saturates near Letta's per-message API ceiling (~333K characters). Base Layer keeps the spec at 34-40K characters across the range.
- Architectural convergence on the same interpretive-representation target by two independently-designed systems.

**Paper location:** v10.1 §4.5 (demoted to "exploratory case study" with explicit n=3 scope; reported as architectural convergence rather than primary result).

---

## 8. TABLE 4.2 — HAMERTON COMPRESSION (token efficiency)

**Label:** Hamerton compression curve (5-judge primary).
**One-line summary:** On Hamerton, a ~7K-token spec (C2a) outperforms 34K tokens of raw corpus (C8) and is in the same band as spec-augmented raw corpus (C9).

| Condition | Avg input tokens | Score (1-5, 5-judge primary) |
|---|---:|---:|
| C8 Raw corpus, no spec | 34,168 | 2.27 |
| C9 Raw corpus + spec | 41,452 | 3.09 |
| C4a All facts + spec | 16,874 | 2.77 |
| C4 All facts, no spec | 7,723 | 2.43 |
| C2a Spec only | 7,320 | 2.63 |
| C5 Baseline (no context) | ~40 | 1.26 |

Numbers from v10.1 §4.2 per-subject compression table (line 791, Hamerton row). 7-judge sensitivity values (S113) are higher across the board: C8=2.32, C9=3.22, C4a=3.22, C4=2.53, C2a=3.04, C5=1.25; see legacy values archived in this section for reference. Direction is identical across panels.

**Per-subject low-baseline aggregate (v12.1 §4.2):** mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.59. Mean C8 − C2a gap = +0.22. (C9 updated 2026-05-13 from 2.50 → 2.59 to reflect the 2026-05-11 Bernal Díaz C9 5-judge-primary rerun; the §4.2 compression Δs are being standardized to the symmetric 9-row computation in v12.1 — see `docs/reviews/v12_1_compression_table_recompute_20260513.md`.)

**Interpretation (bounded):**
- Information is not what's missing: C4 (all facts, no spec) at 7,723 tokens scores 2.43, while C2a (spec alone) at 7,320 tokens scores 2.63 on Hamerton. Same token budget, ~+0.20 lift from the structured spec.
- Raw 34K-token corpus (C8) only reaches 2.27 on Hamerton. The model cannot extract interpretive structure from unstructured text alone.
- Adding spec on top of raw corpus (C9) closes the gap and exceeds C4a level on Hamerton, confirming structure is the limiting factor, not information.
- The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average (low-baseline slice). The next 80K-400K tokens of raw corpus buy an additional +0.22 points on average. Steep initial slope, long plateau.

**Paper location:** v10.1 §4.2 (line 791 per-subject table; line 777 low-baseline aggregate).

---

## 9. JUDGE PANEL — Coverage and calibration

**Label:** Judge panel. LLM-as-judge for behavioral-prediction grading.
**One-line summary:** Five non-Gemini judges form the primary panel; Gemini Flash and Gemini Pro are sensitivity-only because both fail calibration diagnostics by inflating scores by roughly +1 point and (Gemini Pro) penalizing padded-correct responses severely.

| Judge | In 5-judge primary? | Coverage | Parse-failure rate | Score offset vs 5-judge primary |
|---|:---:|---|---:|---:|
| Claude Haiku 4.5 | yes | All conditions, all subjects | ~0.2% | baseline |
| Claude Sonnet 4.6 | yes | All conditions, all subjects | ~0.4% | baseline |
| Claude Opus 4.6 | yes | All conditions, all subjects | ~0.3% | baseline |
| GPT-4o | yes | All conditions, all subjects | ~1% | baseline |
| GPT-5.4 | yes | All conditions, all subjects | **~19%** | +0.1 |
| Gemini 2.5 Flash | no (sensitivity) | All conditions, all subjects | ~2% | **+0.9** |
| Gemini 2.5 Pro | no (sensitivity) | Hamerton, Tier 2, wrong-spec v2 only | **~0.5%** | **+1.0** |

**Interpretation (bounded):**
- The five non-Gemini judges form the primary panel for all v10.1 §4 numbers. Direction and rank order match the 7-judge sensitivity panel; magnitudes differ by Gemini's roughly +1 point inflation.
- Krippendorff α (ordinal): 0.659 across the 5-judge primary panel (substantial agreement); 0.535 across the full 7-judge panel including Gemini Flash/Pro (moderate agreement).
- GPT-5.4 parse-failure rate 19%: roughly 19% of its judgments are dropped per the aggregation rule; effective coverage remains > 80% of questions.
- Gemini Pro did NOT run on the 13 global subjects' main gradient conditions (only Hamerton, Tier 2 replication, wrong-spec v2). The "7-judge" label in S113 outputs was "all available judges per subject," not a uniform 7-judge panel.

**Paper location:** v10.1 §3.7 (calibration), §3.7.2 (5-judge primary decision), Appendix C.5 (judge panel table).

---

## 10. TIER 2 CIRCULARITY — Cross-provider replication

**Label:** Tier 2 circularity. 3 subjects × 2 non-Haiku response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) × GPT-5.4-generated battery. Note: Opus 4.6 and GPT-5.4 appear in Tier 2 only as judges, not as response models.
**One-line summary:** The spec effect replicates across non-Haiku response models on non-Haiku batteries in 5 of 6 cells (direction-only in v10.1).

> **2026-04-25 v10.1 status:** §4.6.1 is **demoted to direction-only with sensitivity ranges**. The directional 5-of-6 claim is retained; the per-cell magnitudes below are preserved for cross-reference but are **not reproducible** under the verification audit and do **not carry through as primary results** in v10.1. Status detail: `docs/research/v11_emit/_ARCHITECTURE.md` §12.4 and `docs/reviews/v11_release_freeze_status_20260425.md`.

| Subject | Response Model | Battery | Spec-effect Δ (earlier draft, not reproducible) | Direction |
|---|---|---|---:|---|
| Ebers | Sonnet | GPT-5.4 | +1.48 | positive |
| Ebers | Gemini Pro | GPT-5.4 | +1.07 | positive |
| Yung Wing | Sonnet | GPT-5.4 | +1.91 | positive |
| Yung Wing | Gemini Pro | GPT-5.4 | +1.27 | positive |
| Zitkala-Sa | Sonnet | GPT-5.4 | +1.40 | positive |
| Zitkala-Sa | Gemini Pro | GPT-5.4 | −0.55 (v10.1 reframing: ~−0.03, approximately null) | null/mismatch |

**Interpretation (bounded):**
- 5 of 6 cells reproduce the spec direction. Effect is not an artifact of Haiku-answering-Haiku-generated batteries.
- The Zitkala-Sa × Gemini Pro cell is reframed in v10.1 as approximately null (~−0.03), not a clean negative. Zitkala-Sa is also one of two main-study subjects where the spec hurts on the gradient.
- Baseline accuracy varies by 1-2 points across response models on the same subject. Independent empirical evidence for cross-provider variance.
- Per-cell magnitudes shown above are **earlier draft values, not reproducible under v10.1 verification audit**. Use direction only.

**Paper location:** v10.1 §4.6.1 (Robustness, demoted to direction-only).

---

## 11. EBERS STATEFUL-AGENT TEST — Complete (n=3 generalization)

**Label:** Ebers Letta stateful-agent loop (2nd-subject generalization check).
**One-line summary:** Ebers and Babur reruns complete; n=3 reported in §4.5 as architectural convergence on n=3, with Babur saturating the API-level ceiling.

See §7 above for full Letta stateful-agent results across the n=3 subject set. Section retained as a heading for older paper anchors.

---

## 12. BASE LAYER AS RETRIEVAL FLOOR — Where BL wins, where it doesn't

**Label:** BL standalone retrieval (MiniLM + ChromaDB) vs commercial systems' retrieval.
**One-line summary:** BL's retrieval is comparable to commercial systems (in the same band), wins only on Hamerton (pipeline development subject), usually middle-of-pack.

**C1 comparisons (retrieval only) on low-baseline subjects (C5 ≤ 2.0):**

| Subject | C5 | Mem0 C1 | Letta C1 | SM C1 | Zep C1 | **BL C1** | Best |
|---|---:|---:|---:|---:|---:|---:|---|
| sunity_devee | 1.03 | 2.13 | 2.59 | 2.57 | 2.24 | 2.41 | letta |
| ebers | 1.04 | 1.65 | 2.21 | 1.80 | 1.60 | 1.76 | letta |
| hamerton | 1.25 | 1.72 | 2.56 | 2.20 | 1.98 | **2.73** | **BL** |
| fukuzawa | 1.80 | 2.59 | 3.07 | 2.90 | 2.41 | 2.45 | letta |
| seacole | 1.85 | 2.16 | 2.89 | 2.74 | 2.18 | 2.44 | letta |
| bernal_diaz | 1.85 | 2.44 | 2.65 | — | 2.25 | 2.36 | letta |
| keckley | 1.91 | 2.45 | 2.70 | 2.58 | 2.48 | 2.44 | letta |
| yung_wing | 1.96 | 1.79 | 2.53 | 2.52 | 2.01 | 2.23 | letta |
| babur | 1.98 | 1.62 | 2.03 | — | 1.68 | 1.67 | letta |

**Interpretation (bounded):**
- BL wins C1 outright on 1 of 9 low-baseline subjects: Hamerton (which was also the pipeline development subject; pipeline-tuning bias is present).
- BL is typically middle-of-pack or behind Letta on C1.
- BL is not a "better retriever" than the commercial systems. Its contribution is the spec layer, not the retrieval substrate.

**Paper location:** v10.1 §4.4.

---

## K. PROVENANCE — Source files for every number

| Data category | Source file path |
|---|---|
| Gradient 14 subjects, 7-judge sensitivity | `data/experiments/memory_systems/results/RESULTS_S113.json` > `gradient` |
| Gradient 14 subjects, 5-judge primary | per-subject `results/global_<subject>/judgments_v2.json` and `results/hamerton/{sonnet,opus,gpt4o,haiku,gpt54}_judgments.json`, aggregated by `scripts/recompute_5judge_primary.py` |
| Memory systems aggregate | `RESULTS_S113.json` > `memory_systems`; 5-judge primary recompute at `docs/research/memory_systems_5judge_primary.md` |
| Statistical tests (5-judge primary) | `scripts/recompute_5judge_primary.py` over per-judge files |
| Battery-composition sensitivity | `scripts/_v10_battery_sensitivity.py`; full report `docs/research/v10_battery_sensitivity_analysis.md` |
| Coupling-free reframing | `scripts/_v10_coupling_sensitivity.py`; full report `docs/research/v10_coupling_sensitivity_analysis.md`; arrays at `docs/research/v10_coupling_sensitivity_arrays.npz` |
| Tier 2 circularity | `RESULTS_S113.json` > `tier2_circularity`; per-judge under `results/multimodel/` |
| Letta stateful-agent main rerun (n=3, 5-judge primary) | `docs/research/_letta_rerun/5judge_primary_results.json`; pipeline scripts `docs/research/_letta_rerun/{20_run_c2a_named.py, 40_judge_responses.py, 50_aggregate.py, 70_compute_5judge_primary.py}`; per-subject judgments `docs/research/_letta_rerun/{hamerton,ebers,babur}_judgments_*.json` and `docs/research/_letta_rerun/{ebers,babur}_letta_battery.json` |
| Letta stateful-agent full-stack BL rerun (§4.5 footnote) | `docs/research/_letta_rerun/fullstack_named/5judge_fullstack_results.json` and `docs/research/_letta_rerun/fullstack_named/{hamerton,ebers,babur}_fullstack_judgments_*.json`; pipeline scripts `docs/research/_letta_rerun/fullstack_named/fs_{01..07}_*.py` |
| Letta block dumps (raw `human` memory blocks) | `docs/research/_letta_blocks/{hamerton,ebers,babur}_human_block.txt` |
| Letta stateful matched-rerun summary | `docs/research/letta_stateful_matched_rerun.md`; `docs/research/letta_stateful_deep_read.md` |
| Hamerton Table 4.2 conditions (5-judge primary) | `results/hamerton/{c8_c9_judgments_haiku.json, c8_c9_judgments_sonnet.json, c8_c9_judgments_opus.json, c8_c9_judgments_gpt4o.json, c8_c9_judgments_gpt54.json}` for C8/C9; `results/hamerton/{judgments.json, sonnet_judgments.json, opus_judgments.json, gpt4o_judgments.json, gpt54_judgments.json}` (and `judgments_harmonized.json` for legacy harmonization) for C2a/C2c/C4a/C5 |
| Wrong-spec v1 | `results/global_*/judgments_v2.json` > condition `C2c_wrong_spec`; pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING; 5-judge recompute at `scripts/compute_wrong_spec_5judge.py` |
| Wrong-spec v2 | `results/_wrong_spec_v2/`; 5-judge recompute at `scripts/compute_wrong_spec_5judge.py` |
| Hedging analysis | `scripts/classify_hedging.py` (rules `starts_refusal` and `refusal_ge_1`) over `results/global_<subject>/results_v2.json`; artifact `docs/research/hedging_analysis.json` |
| Wrong-spec detection rate (60.6%) | `scripts/classify_wrong_spec_detection.py` → `docs/research/wrong_spec_detection_analysis.md` and `wrong_spec_detection_raw.json` |
| Anchor-crossing rate | `scripts/compute_anchor_crossing.py` → `docs/research/s114_anchor_crossing_examples.json` |
| Spec activation | `scripts/compute_spec_activation.py` → `docs/research/spec_activation_analysis.json` |
| Question-improvement rate | inlined in `scripts/generate_fig_4_2_1.py` (render-time); compute script flagged for follow-up in PROVENANCE_INDEX S115 addendum |
| Judge calibration | `results/judge_calibration/{judgments.json, gpt4o_calibration.json, gpt54_calibration.json, gemini_pro_calibration.json}` |
| Wins inventory (18 condition pairs, 4,206 anchor crossings, 60 unique extreme upward) | `docs/research/wins_inventory_20260428.json`; script `scripts/build_wins_inventory.py` |
| Within-band fractional shifts (Stream Y) | `docs/research/within_band_shifts_20260428.{json,md}`; script `scripts/within_band_and_meta_judging.py` |
| Pattern-activation deep analysis | `docs/research/pattern_activation_deep_20260428.{json,md}`; script `scripts/deep_pattern_activation_analysis.py` |
| Predicate ablation (16-case Phase 2c) | `docs/research/predicate_ablation_results_20260428.{json,md}` + `predicate_ablation_sampling_20260428.json`; script `scripts/run_predicate_ablation.py` |
| Held-out leakage audit (60 extreme upward cases) | `docs/research/held_out_leakage_investigation_20260428.{json,md}`; script `scripts/investigate_held_out_leakage.py` |
| Hamerton spec-length confound (1,918 vs ~5,775 words; 18.75% vs 8.9% extreme-jump rates) | `docs/research/hamerton_confound_note_20260428.md`; spec word counts via `Path(...).read_text(encoding='utf-8').split()` on `data/hamerton/spec/brief_v5_clean.md` and `data/global_subjects/<subject>/spec_production.md` |
| Per-subject excerpts | `docs/research/per_subject_excerpts_20260428.json`; script `scripts/build_per_subject_excerpts.py` |
| Per-question anchor crossings, C4a vs C4 + C9 vs C8 | `docs/research/per_question_anchor_crossing_extended_20260428.json`; script `scripts/compute_anchor_crossing_c4a_c4_and_c9_c8.py` |
| Per-system anchor crossing (low-baseline 9, all 5 systems × controlled/native) | `docs/research/per_system_anchor_crossing_20260427.{json,md}`; script `scripts/compute_per_system_anchor_crossing.py` |
| Big-wins characterization (Stream X, with arithmetic-error caveats) | `docs/research/big_wins_characterization_20260428.{json,md}`; script `scripts/characterize_big_wins.py` |
| v11 paper-numbers verification (mechanical paper-vs-scaffold audit; 312 numerics, 298 MATCH / 10 MINOR / 4 MISMATCH) | `docs/research/v11_paper_numbers_verification_20260428.md`; orchestrator `scripts/_v11_validation/*` |
| v11 confidence catalog (HIGH / MEDIUM / LOW / UNRESOLVED claim mapping) | `docs/research/v11_confidence_catalog_20260428.md` |
| Wins-analysis pipeline state snapshot | `docs/research/wins_analysis_pipeline_state_20260428.md` |

Any discrepancy between this document and the v11 paper draft should be resolved in favor of the v11 paper. v11 is the citable canonical artifact (release-frozen 2026-04-28); this document mirrors v11's 5-judge primary panel, sensitivity reframing, and v11-specific claims (per-question variance, multi-anchor jumps, two statistical signatures, predicate ablation, held-out leakage, Hamerton spec confound). v10.1 is preserved as historical baseline at `docs/beyond_recall_v10_1_draft.md` for reference; v11 headline numbers carry forward from v10.1 unchanged with the additions noted in the v11 numerical-additions subsection above.

---

## Addendum 2026-05-07 — C4 (facts only) coverage and the spec-ceiling reconciliation

Two findings landed during the v11.8 §4.1 walk that affect this reference:

### C4 (facts only) means recomputed for mid-baseline subjects

Earlier drafts of the §4.1 per-subject table omitted C4 (facts only) values for mid-baseline subjects, claiming C4 was run on the 9 low-baseline subjects only. The data shows otherwise: all 5 mid-baseline subjects have C4_factdump entries judged by all 5 primary judges (haiku, sonnet, opus, gpt4o, gpt54) at 39 questions each, sourced from `results/global_<subject>/judgments_v2.json`. Recompute via canonical 5-judge primary aggregation (per-question 5-judge mean, then mean across questions) 2026-05-07:

| Subject (mid-baseline) | C5 | C4 (facts only, 5-judge primary) | C4a | Δ C4a−C5 | Δ C4a−C4 |
|---|---:|---:|---:|---:|---:|
| zitkala_sa | 2.34 | **2.10** | 2.02 | −0.32 | **−0.08** |
| cellini | 2.38 | **2.42** | 2.53 | +0.15 | **+0.11** |
| rousseau | 2.44 | **2.32** | 2.53 | +0.10 | **+0.21** |
| augustine | 2.58 | **2.56** | 2.70 | +0.11 | **+0.14** |
| equiano | 2.77 | **2.43** | 2.42 | −0.35 | **−0.01** |

Mid-baseline mean Δ C4a−C4 = **+0.07** (parallel to low-baseline mean +0.09; the Spec-on-facts increment is small and mixed in sign across both bands).

**Franklin C4 was NOT scored on the 5-judge primary panel.** Franklin C4_factdump responses were generated and live in `results/franklin/results.json` and `results/franklin_legacy_20260411/results.json`, but per `results/franklin/judgments.json` Franklin was scored only by haiku + gemini (legacy 2-judge). Franklin C4 cells stay dashed in §4.1 table and any subsequent paper-wide table that includes Franklin.

### Spec-ceiling value reconciliation: 2.44 vs 2.46 (paper-wide audit pending)

§1 line 93 of this document: "Mean C4a across all 14 = **2.44**". §2 line 109 (this document, pre-fix 2026-05-07): "the spec produces a roughly constant C4a near 2.46". Internal inconsistency. Recompute from the §1 per-subject table 14-row mean = 2.439 ≈ **2.44**. §2 fixed 2026-05-07.

Memory entry `project_v11_8_anchor_crossing_prominence.md` flags that the "2.46 ceiling" framing also appears in the paper's §1.3, §4.2, §5.1, §5.2, and abstract. Either 2.44 is canonical paper-wide (mechanically derived from per-subject means under 5-judge primary) and the other sections need updating, or 2.46 is a different aggregation (7-judge sensitivity, low-baseline-only subset, or another denominator) that should be made explicit. **Paper-wide reconciliation pending; audit task added.**

### Mechanistic figure-check principle (Aarik's directive 2026-05-07)

Numerical claims in the paper need a recompute-from-source pipeline, not manual reading. The C4 mid-baseline omission and the 2.44 vs 2.46 inconsistency both escaped the prior numerical claims audit (`docs/reviews/numerical_claims_audit_v11_8_20260505.md` found P0 = 0, P1 = 0). The audit was reading-paper-claim vs reading-data-summary, not recomputing-from-source.

**Paper-wide infrastructure task:** build `scripts/recompute_paper_numbers.py` that ingests every numerical claim in the paper (body + footnotes + figure captions + appendices) and recomputes against canonical data files (`judgments_v2.json`, anchor-crossing JSON files, retrieval-overlap JSON files), with an automated discrepancy report. This becomes part of the §8 reproducibility commitment and a launch-blocking gate per the master release roadmap.
