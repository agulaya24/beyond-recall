# Provenance Traceability Index

**Paper:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
**Generated:** 2026-04-13
**Updated:** 2026-04-18 (Session 113, full-stack refresh); 2026-04-25 (V10.1 update prepended; pre-v10 sections retained as historical raw-data provenance); 2026-05-05 (`data/source_corpora/` mirror added — Project Gutenberg + archive.org source autobiographies for all 14 main-study subjects + Franklin reference + Franklin letters, with per-subject `provenance.md` and SHA-256 hashes; reference PDFs pulled into `docs/references/` with `MANIFEST.md`).

**Canonical paper:** `docs/beyond_recall_v11_8_draft.md` (v11.8, active edit branch as of 2026-05-05). v11.9 will lock figures, data, and repo state. v12 is the planned release. v10.1 preserved at `docs/beyond_recall_v10_1_draft.md` as historical baseline.

**SINGLE SOURCE OF TRUTH:** For the current, paper-ready values, see [`DATA_REFERENCE.md`](DATA_REFERENCE.md). That file is synced to v11.8's 5-judge primary panel. This Provenance Index traces individual claims to underlying raw data files; where DATA_REFERENCE.md and any row below disagree, DATA_REFERENCE.md wins. Where the v11.8 paper draft disagrees with either, the v11.8 paper wins.

**Method:** Each quantitative claim in the paper traced to its source file in the study repository.

**Legend:**
- VERIFIED = exact value found in source data
- APPROXIMATE = close but not exact match (rounding, different subset, or intermediate computation)
- NOT FOUND = no source file located in the repository
- DERIVED = value computed from source data (not stored directly)
- S113 = value corrected in the Session 113 full-stack refresh; see `PAPER_CORRECTIONS.md` S113 section
- V10.1 = value updated for the v10.1 5-judge primary panel; see "V10.1 Update" section below

---

## V11 active-editing note (2026-04-27 / 2026-04-28)

v11 (`docs/beyond_recall_v11_draft.md`) is the active edit branch on top of the v10.1 release-frozen baseline. v10.1 remains the citable canonical paper and the anchoring reference for every entry in this file. The v11 comment-walk shifted some section numbers; when chasing a v10.1 paper-section reference from this file into v11, apply these mappings:

- **v10.1 §2.3 + §2.3.1 (Memory and personalization benchmarks)** -> v11 **§2.1** (merged).
- **v10.1 §3.7.2 (Calibration)** -> v11 **§3.6.3** (Calibration; same content; full §3.7 -> §3.6 in v11).
- **v10.1 §3.7.3 (Fractional score interpretation / cross-anchor rule)** -> v11 **§3.6.2** (same content).
- **v10.1 §4.1.1 (Franklin high-baseline reference)** -> v11 **§4.6.4** (moved under sensitivities).
- **v11 §4.4.4 (Two statistical signatures)** is a new subsection added in v11; no v10.1 equivalent.
- **v11 §4.7** is a new closing paragraph bridging into §5; no v10.1 equivalent.
- **v11 §3.6.6 (Rubric-handling limitations)** is the audit subsection; numbers reconcile via `scripts/audit_low_end_inflation.py`.

Numerical entries below are unchanged from v10.1; v11 paper-numbers verification (`docs/research/v11_paper_numbers_verification_20260428.md`) shows 298 of 312 audited claims MATCH, 10 MINOR_ROUNDING, 4 MISMATCH. The 4 MISMATCH items are all in §4.4.1 Supermemory aggregate (sign / improved-count drift; flagged for paper edit) and §4.2.1 all-14 C8 row (sub-1pp drift; flagged for paper edit). Direction of every finding is unchanged.

### v11 research artifacts added 2026-04-28 (Phase 1 / 2 / 2c wins-analysis pipeline)

These artifacts back the per-question variance, multi-anchor-jump, statistical-signature, and predicate-ablation claims that v11 §1.3 / §4.1 / §4.2 / §4.4.4 / Appendix B.6.5 / Appendix B.8 cite. Pipeline state and rationale: `docs/research/wins_analysis_pipeline_state_20260428.md`. Confidence catalog: `docs/research/v11_confidence_catalog_20260428.md`.

| Artifact | Description | Generating script | Cited in v11 paper |
|---|---|---|---|
| `docs/research/wins_inventory_20260428.json` | Comprehensive paired anchor-crossing analysis across 18 condition pairs (direct, corpus, memory-system layering). 4,206 anchor crossings; 150 paired questions with extreme upward jumps (≥3 bands); 60 unique extreme upward (subject, qid) cases after dedup. Cross-checks reproduce published numbers exactly. | `scripts/build_wins_inventory.py` | §1.3 (multi-anchor 18% / extreme 6%); §4.4.2 footnote; Appendix B.6.5; Appendix B.8 (Phase 2c sampling source) |
| `docs/research/big_wins_characterization_20260428.{json,md}` | Stream X characterization of the 60 unique extreme upward jumps (axis distribution, mechanism distribution by heuristic). Reported with arithmetic-error caveats; Hamerton-leverage misattribution called out and corrected in `hamerton_confound_note_20260428.md`. | `scripts/characterize_big_wins.py` | Appendix B.6.5 (Hamerton-leverage at per-question grain) |
| `docs/research/within_band_shifts_20260428.{json,md}` | Stream Y within-band fractional-shift inventory across the same 18 pairs (8,804 paired-comparison instances). Half-anchor metric: 759 same-band ≥0.5 shifts on top of 4,206 crossings (~18% extra movement the binary anchor-crossing metric does not record). Per-judge nonzero rates, panel-direction-agreement curve, pre-vs-post Spearman ρ across pairs (C5→C4a 0.27 vs C4→C4a 0.72 vs C8→C9 0.70). | `scripts/within_band_and_meta_judging.py` | §3.6.2 (half-anchor methodological note); §4.4.4 (two statistical signatures); Appendix D-extension |
| `docs/research/pattern_activation_deep_20260428.{json,md}` | Phase 2 deeper pattern-activation analysis. Heuristic-level pattern-activation claim falsified: fair-comparison spec_doing_work rate is 78.9% on extreme jumps vs 80.6% on non-jumping spec-loaded controls (Δ = −1.7pp). 0 spec→held-out 6-grams (direct-quote lookup ruled out). Surfaces narrower surviving claim: 11 of 60 INFERENCE_CHAIN cases with verdict `genuine_inference_via_spec`. | `scripts/deep_pattern_activation_analysis.py` | §4.4.2 caveat; Appendix B.6.5 |
| `docs/research/predicate_ablation_results_20260428.{json,md}` | Phase 2c predicate-ablation experiment on 16 stratified extreme-upward-jump cases. Verdict: NOT_SUPPORTED for the strong predicate-mediated mechanism claim. Mean Δ_removal = +0.05 (CI95 [−0.35, +0.45]); mean Δ_reversal = −0.24 (CI95 [−0.45, −0.02]); 11 of 16 cases Δ_removal < 0.5. Original-condition reproduction drift mean = −1.44 anchors (stochasticity caveat). | `scripts/run_predicate_ablation.py` | Appendix B.8 (per-predicate ablation, asserted as null with redundant-spec-construction caveat) |
| `docs/research/predicate_ablation_sampling_20260428.json` | Stratified-sampling spec for the 16 ablation cases (PATTERN_PREDICATE_high / INFERENCE_CHAIN / MIXED_OTHER × LITERAL / INTERPRETIVE / REFUSAL axes). | Sampling driver inside `scripts/run_predicate_ablation.py` | Appendix B.8 sampling spec |
| `docs/research/held_out_leakage_investigation_20260428.{json,md}` | Held-out passage leakage audit on the same 60 extreme-upward-jump cases. C4a responses scanned for held-out → response n-gram leaks (3, 4, 6 token windows). Result: 0 6-gram, 2 4-gram, 12 3-gram leaks; severity verdict RARE. Most concerning case: hamerton q51 (`as much as possible`, CORPUS_LEAK 4-gram). Recommendation: footnote acknowledgement sufficient. | `scripts/investigate_held_out_leakage.py` | §3.3 leakage audit + held-out leakage footnote (severity RARE) |
| `docs/research/hamerton_confound_note_20260428.md` | Verified spec-length inversion: Hamerton served spec is 1,918 words (`brief_v5_clean.md`); globals' served spec averages ~5,775 words (`spec_production.md`). Hamerton extreme-jump rate is 18.75%; globals average 8.9%. Stream X "long unified-brief" attribution corrected. Spec length is anti-correlated with extreme-jump rate; cause not isolated by present design. Candidate explanations: legacy battery generator path, subject pretraining thinness, predicate density per word. | (audit note; spec word count via `Path('data/...').read_text(encoding='utf-8').split()`) | Appendix B.6.5 (cited verbatim for spec word counts and 18.75% / 8.9% comparison) |
| `docs/research/per_subject_excerpts_20260428.json` | Curated illustrative per-subject excerpts (response/spec text) sampled from the wins inventory for paper figures and case-study callouts. | `scripts/build_per_subject_excerpts.py` | §4.1 / §4.4 figure captions and case-study callouts |
| `docs/research/per_question_anchor_crossing_extended_20260428.json` | Per-question anchor-crossing data for C4a vs C4 and C9 vs C8 pairs (351 / 312 paired questions). Multi-anchor examples include Hamerton q22 (1→3 on C9 vs C8), Hamerton q25 (1→4), Seacole q2 (2→5 on C4a vs C4), Yung Wing q22 (1→4 on C4a vs C4). | `scripts/compute_anchor_crossing_c4a_c4_and_c9_c8.py` | §4.2 footnote `[^c4a-c9-anchor-data]`; §4.2 within-band table at line 802 |
| `docs/research/per_system_anchor_crossing_20260427.{json,md}` | Cross-system per-question anchor-crossing analysis on the low-baseline 9. Per-system upward / downward % at C1→C3 controlled and native, all 5 systems. Aggregation: per-judge per-question score, mean across 5 primary judges, paired C1_<sys> → C3_<sys> per (subject, question). | `scripts/compute_per_system_anchor_crossing.py` | §1.3 Memory-system layering bullet; §4.4 per-system anchor-crossing table; closes v11 comment C131 |
| `docs/research/wins_analysis_pipeline_state_20260428.md` | Durable state snapshot for the multi-stream wins-analysis pipeline (origin, terminology rule, phase status, framing-pivot disposition). Anchors what was built, what was falsified, what survived. | (handwritten state doc) | Internal reference only; not cited in paper body |
| `docs/research/v11_confidence_catalog_20260428.md` | Source of truth for what v11 paper claims at what confidence (HIGH / MEDIUM / LOW / UNRESOLVED). Maps every body-text claim to its evidence and hedge level. Includes "What the paper SHOULD NOT claim" section. | (handwritten catalog) | Implicit anchor for v11 framing discipline; cited in this index and in `KEY_FINDINGS.md` |
| `docs/research/v11_paper_numbers_verification_20260428.md` | Mechanical paper-vs-scaffold verification of 312 audited numerics in v11. Result: 298 MATCH / 10 MINOR_ROUNDING / 4 MISMATCH / 0 PAPER_ONLY. The 4 MISMATCH items are documented as pending paper edits, not silent reconciliations. | `scripts/_v11_validation/*` (orchestrator + per-section verifiers) | Source of truth for paper-vs-data reconciliation; cited in DATA_REFERENCE §K-v11 addendum |
| `docs/reviews/framing_implications_20260428.md` | Phase 3 Round 1 framing report. Disposition of 8 framing pivots (APPLY-AS-DRAFTED / REFINE-FIRST / PHASE-2C-DEPENDENT / DROPPED / APPENDIX-ONLY). | `scripts/build_framing_implications.py` (or handwritten) | Internal review record |
| `docs/reviews/framing_report_round1_update_20260428.md` | Phase 3 Round 1 update integrating deeper-analysis falsification of the heuristic pattern-activation claim. | (handwritten) | Internal review record |
| `docs/reviews/framing_report_round2_review_20260428.md` | Phase 3 Round 2 cross-LLM review on the framing report. | `scripts/review_framing_report.py` (or analogue) | Internal review record |
| `docs/reviews/pattern_activation_claim_review_20260428.md` | Phase 2 collective review on the pre-deeper-analysis pattern-activation claim. Both GPT-5.5 and Gemini Pro endorsed cautious framing pre-deeper-analysis; superseded by the falsification result. | `scripts/review_pattern_activation_claim.py` | Internal review record |
| `docs/reviews/v11_c96_framing_review_20260428.md` | Cross-LLM review of v11 comment C96 framing. | (review pipeline) | Internal review record |

These artifacts are all dated 2026-04-28 (per-system anchor-crossing dated 2026-04-27, per task-spec). They post-date the v10.1 release-freeze and are unique to v11.

---

## V10.1 Update (2026-04-25) — read first

The v10.1 paper (point release 2026-04-25, on top of v10 release-frozen 2026-04-24) reports the 5-judge primary panel (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4) as canonical for §4. The 7-judge panel (adding Gemini Flash and Gemini Pro) is sensitivity only. The S113 / S115 ADDENDUM sections below are anchored to the 7-judge panel and to the v6/v8 draft section numbering; they remain accurate as raw-data traces but are not the canonical paper claims for v10.1.

**v10.1 numerical changes from v10** (this section updated to reflect them):
- Wrong-spec random-derangement v2 aggregate: +0.22 → **+0.15** (5-judge primary, 13 globals, vs C5).
- Tier 2 magnitudes **demoted to direction-only**; per-cell values are not reproducible under verification audit. Direction (5 of 6 cells positive) retained.
- Tier 2 response model count corrected: 4 → **2** (Claude Sonnet 4.6, Google Gemini 2.5 Pro). Opus 4.6 and GPT-5.4 are Tier 2 *judges*, not response models.
- Level-CI rounding: −0.25 → **−0.24** (lower bound of 95% CI on the C4a ~ C5 level slope).
- Letta 7-judge sensitivity Δs: Hamerton +0.20 → **+0.09**, Babur +0.29 → **+0.232** (Ebers ≈ +0.746).
- Letta named-entity counts (§4.5): Babur 540 → **416**; Hamerton Letta 19 → **26**; Hamerton BL 19 → **22**.
- §4.4.2 Supermemory mixture (paired analysis): 89/516 (17.2%) → **110/546 (20.1%)**; 37 helps / 52 hurts → **57 helps / 53 hurts**; mean swings +1.45 / −1.41 → **+1.55 / −1.38**.
- Table 4.6 rebuilt under strict 5-judge primary: Mem0/Yung Wing +0.35 → +0.33; Mem0/Keckley −0.01 → −0.02; Letta arch/Hamerton +0.46 → +0.42 (n=39 → n=38); Letta arch/Keckley 0.00 → −0.02; Zep/Seacole +0.52 → +0.47; Zep/Keckley +0.10 → +0.04; Base Layer/Yung Wing +0.33 → +0.29; Base Layer/Keckley −0.01 → −0.04. Aggregate Δs shrink by 0.01-0.06; no row sign flips.
- §4.2.1 pairwise-table counts: 190/46/115 → **187/56/108** (C8 vs C2a); 155/42/115 → **153/45/114** (C9 vs C4a).
- App B.4 REFUSAL_TRIGGERING mean Δ: +0.489 → **+0.417**.
- App B.6 Δ_spec range max: +1.85 → **+1.37**; REFUSAL × Δ_spec correlation: +0.321 → **+0.212**.
- App B.5 Hamerton axis: +1.93 / +2.02 / +1.71 → **+1.68 / +1.30 / +1.25**.
- App D.3.4 length-correlation n: 351 → **312** for C5/C4/C4a (C2a stays at 351).
- §4.5 Babur block coherence ceiling: 25% → **25.4%** (unchanged in this doc; reflects the source-of-truth value).
- Living-user language softened: "expected by construction" replaced with **"closest available proxy"** framing.
- §4.1 "C4a ceiling" replaced with **"post-spec operating level"** near 2.46.
- §5.2 H5 reframed: fact extraction does most volume-reduction work; spec adds marginal value at per-question level.
- §4.4 memory-system additivity nuanced: "3 of 4 commercial systems" (was inconsistent at "all 4" in earlier prose).
- Wrong-spec total N=587 disambiguated: 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers).
- Main-study batteries: ALL 14 subjects are Haiku-generated (the wording "13 globals = GPT-5.4 batteries" was wrong); Tier 2 batteries are GPT-5.4-generated.

### V10.1 canonical per-subject gradient (5-judge primary, v10.1 §4.1 line 720; Appendix D.1 line 2061)

| Subject | C5 baseline | C2a spec | C4a facts+spec | Δ_C2a | Δ_C4a | Source |
|---|---:|---:|---:|---:|---:|---|
| Ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | `results/global_ebers/judgments_v2.json` per-judge files |
| Sunity Devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | `results/global_sunity_devee/judgments_v2.json` |
| Hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | `results/hamerton/{haiku,sonnet,opus,gpt4o,gpt54}_judgments.json` |
| Fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | `results/global_fukuzawa/judgments_v2.json` |
| Bernal Diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | `results/global_bernal_diaz/judgments_v2.json` |
| Babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | `results/global_babur/judgments_v2.json` |
| Seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | `results/global_seacole/judgments_v2.json` |
| Keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | `results/global_keckley/judgments_v2.json` |
| Yung Wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | `results/global_yung_wing/judgments_v2.json` |
| Zitkala-Sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | `results/global_zitkala_sa/judgments_v2.json` |
| Cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | `results/global_cellini/judgments_v2.json` |
| Rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | `results/global_rousseau/judgments_v2.json` |
| Augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | `results/global_augustine/judgments_v2.json` |
| Equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | `results/global_equiano/judgments_v2.json` |
| Franklin (control) | 3.77 | 3.37 | 3.65 | −0.40 | −0.13 | `results/franklin_legacy_20260411/analysis/*_judgments.json` |

Aggregation: within-judge mean across the 39-question battery (40 for Franklin), then mean across the 5 primary judges. Aggregated by `scripts/recompute_5judge_primary.py`.

### V10.1 canonical statistical tests (5-judge primary)

| Test | V10.1 value | Source |
|---|---|---|
| Δ_C4a-on-C5 regression slope | **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001 | `scripts/_v10_battery_sensitivity.py` (univariate); `scripts/_v10_coupling_sensitivity.py` (level + permutation) |
| Battery-composition partial slope | **−0.88 [95% CI −1.13, −0.63]**, p < 10⁻⁵ (controls for LITERAL_RECALL fraction) | `scripts/_v10_battery_sensitivity.py`; report `docs/research/v10_battery_sensitivity_analysis.md` |
| GPT-5.4-battery subset slope (n=13, drops Hamerton) | **−0.89 [95% CI −1.18, −0.61]**, R² = 0.81, p < 10⁻⁴ | Same script |
| Level regression C4a ~ C5 | slope **+0.04 [95% CI −0.24, +0.33]**, R² = 0.008, p = 0.76; mean C4a = **2.46** | `scripts/_v10_coupling_sensitivity.py`; report `docs/research/v10_coupling_sensitivity_analysis.md` |
| Wilcoxon C5 vs C4a (N=14) | **W=11, p=0.007** | `scripts/recompute_5judge_primary.py` |
| Wilcoxon C5 vs C2a (N=14) | **W=10, p=0.005** | Same |
| Krippendorff α (ordinal) | **0.659** (5-judge primary); 0.535 (7-judge sensitivity) | Same |
| Pairwise Spearman ρ | **0.86 - 0.93** (5-judge primary, 10 pairs); 0.89 - 0.98 (legacy 4-judge Hamerton historical, retained for back-compat) | Same |

### V10.1 canonical memory-system spec deltas (5-judge primary, v10.1 §4.4 line 1048)

| Config | Mem0 | Letta archival | Zep | Supermemory | Base Layer |
|---|---:|---:|---:|---:|---:|
| Controlled, all 14 | +0.12 | +0.20 | +0.19 | −0.05 | +0.08 |
| Controlled, low-baseline (n=9) | +0.10 | +0.17 | +0.17 | −0.01 | +0.08 |
| Native, all 14 | +0.33 | −0.02 | +0.33 | −0.01 | n/a |
| Native, low-baseline | +0.32 | −0.04 | +0.30 | −0.03 | n/a |

Source: `RESULTS_S113.json` > `memory_systems`; 5-judge primary recompute at `docs/research/memory_systems_5judge_primary.md`. Native Supermemory n=14 reflects the 2026-04-23 paid-tier rerun (4 free-tier ingestion failures resolved); see `docs/research/p0_2_supermemory_paid_tier_rerun.md` and `docs/research/supermemory_7judge_aggregate.md`.

### V10.1 canonical wrong-spec controls (5-judge primary, 13 globals with complete coverage, v10.1 §4.3 line 891)

| Condition | Mean Δ vs C5 |
|---|---:|
| C2a (correct spec) | +0.35 |
| C2c v2 (random derangement, seed=42) | **+0.15** |
| C2c v1 (fixed derangement, cultural/temporal distance) | −0.25 |

Note on N=587 wrong-spec classified responses: 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). 60.6% content-grounded detection rate is computed across this combined N.

Source: `scripts/compute_wrong_spec_5judge.py` over `results/_wrong_spec_v2/`; pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING (lines 51-60).

### V10.1 canonical Letta stateful-agent (5-judge primary, n=3, v10.1 §4.5 line 2426)

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Babur | 2.42 | 1.88 | **+0.54** |

Full-stack BL rerun (footnote): Δ +0.27 / +1.21 / +0.38; direction preserved. Source: `docs/research/_letta_rerun/5judge_primary_results.json`; pipeline scripts `docs/research/_letta_rerun/{20_run_c2a_named.py, 40_judge_responses.py, 50_aggregate.py, 70_compute_5judge_primary.py}`; full-stack at `docs/research/_letta_rerun/fullstack_named/5judge_fullstack_results.json`. Babur saturated at 335,349 chars; 25.4% verbatim sentence duplication at the ceiling.

### V10.1 canonical Hamerton compression curve (5-judge primary, v10.1 §4.2 line 791)

| Condition | Tokens | Score |
|---|---:|---:|
| C5 baseline | ~40 | 1.26 |
| C2a spec only | 7,320 | 2.63 |
| C4 facts only | 7,723 | 2.43 |
| C4a facts + spec | 16,874 | 2.77 |
| C8 raw corpus | 34,168 | 2.27 |
| C9 raw corpus + spec | 41,452 | 3.09 |

Source: `results/hamerton/{c8_c9_judgments_haiku.json, c8_c9_judgments_sonnet.json, c8_c9_judgments_opus.json, c8_c9_judgments_gpt4o.json, c8_c9_judgments_gpt54.json}` for C8/C9; `results/hamerton/{judgments.json, sonnet_judgments.json, opus_judgments.json, gpt4o_judgments.json, gpt54_judgments.json}` for C2a/C2c/C4/C4a/C5.

### Status of pre-V10.1 sections below

The S105/S113 sections below this V10.1 update were anchored to the 7-judge mixed panel and to v6 or v8 paper draft section numbers. They are accurate as raw-data provenance traces (the underlying judgment files are unchanged) but are NOT canonical for v10.1 paper claims. Where a row below conflicts with the V10.1 update above or with `DATA_REFERENCE.md`, the V10.1 update / DATA_REFERENCE wins. Specific notes:

- Hamerton C5 1.41 / 1.37 references below are pre-S113. Canonical v10.1 value: **1.26** (5-judge primary).
- Franklin C5 3.99 / 4.10 references below: canonical v10.1 value is **3.77** (5-judge primary, Franklin batch with full panel).
- Global gradient table "+13% to +174%" framing below is the 7-judge percentage representation. Canonical v10.1 representation is per-subject (C5, C2a, C4a) means + Δ values, see V10.1 table above.
- "+1.99 / +1.96 / +0.75" Letta uplift framing in legacy Hamerton/Ebers/Babur traces is vs C5 (n=3 case study). Canonical v10.1 framing in §4.5 is Δ vs BL unified brief at matched response model: **+0.14 / +1.05 / +0.54**. The two framings answer different questions; the paper uses the BL-comparison framing.
- Pairwise Spearman ρ "0.89-0.98" rows below are the historical 4-judge Hamerton statistic. Canonical v10.1 value across the 5-judge primary panel (10 pairs) is **0.86-0.93**.
- v6 §3.7 "Krippendorff α = 0.723" was stale at S113; v10.1 reports **0.659** (5-judge primary) / 0.535 (7-judge).

---

## S113 Corrections Summary (read first)

The following paper numbers were corrected in S113. The full list is in `PAPER_CORRECTIONS.md` under the "S113 CORRECTIONS" header. Source for each is `DATA_REFERENCE.md`:

| Paper location | Old value | S113 value | DATA_REFERENCE section |
|---|---:|---:|---|
| §4.1.1 Lift (spec − baseline) | +0.55 | **+0.67** (all-14 mean Δ facts+spec) | §1 aggregates |
| §4.2 Table 4.2, C3 Mem0 + spec | 3.31 | **2.77** | §8 |
| §4.2 Table 4.2, C3 Supermemory + spec | 3.14 | **2.86** | §8 |
| §4.2 Table 4.2, C4a Facts + spec | 3.28 | **3.22** | §8 |
| §4.2 Table 4.2, C5 Baseline (Hamerton) | 1.41 | **1.25** | §1, §7, §8 |
| §4.1.2 Parse-failure judge attribution | Gemini Pro ~40% | **GPT-5.4 ~19%**; Gemini Pro ~0.5%, coverage-limited | §9 |
| §4.5 Wrong-spec v2 | 2.21 | **2.30** (random derangement); v1 = 1.86 (fixed derangement for the 13 globals per `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING; Hamerton-only Franklin-for-all is reported separately in §4.1.1) | §6 |
| §4.3 Retrieval disagreement | "94%" | **RESOLVED 2026-04-18.** 94% ≈ 93.4% is the *all-three-disagreement rate at top-1* (fraction of questions where no single fact appears in all three systems' top-1 sets) on the controlled-config retrieval data (n=515 analyzable questions). Verified: 93.4% top-1, 83.3% top-3, 73.8% top-5, 53.2% top-10. In the native config (each system runs its own ingestion), disagreement is 100% at every top-k. Script and output: `data/experiments/memory_systems/string_match_disagreement.py` → `results/string_match_disagreement.json`. | DATA_REFERENCE.md §K, paper §4.3 |
| §4.3.1 Letta stateful-agent test | (new section) | Block 22,472 chars; matched-model 3.24 vs C2a 3.04 at 65% context | §7 |

See `PAPER_CORRECTIONS.md` for the full S113 changelog including framing corrections (Base Layer repositioning, flagship sentence, memory-provider framing).

---

## Section 1: Abstract

| Claim | Value | Source File | Status |
|---|---|---|---|
| Subjects tested | 14 subjects, 11 cultures | `data/global_subjects/` (13 dirs) + `data/hamerton/` | VERIFIED |
| Response models | Main study: Haiku 4.5 only (all 14 subjects, every condition). Tier 2 cross-provider directional probe: 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) on 3 subjects against GPT-5.4-regenerated batteries. Note: Opus 4.6 and GPT-5.4 appear in Tier 2 only as judges, not as response models. | `results/multimodel/` (sonnet, gemini) + Haiku primary; v10.1 §1.2 / §3.6 | VERIFIED — corrected from prior "6 response models" framing to v10.1 scope |
| Independent judges | 7 judges | `results/judge_calibration/` (haiku, gemini_flash, gpt4o, gemini_pro, gpt54) + sonnet + opus batch | VERIFIED |
| Cohen's d = 1.21 | 1.21 | `analysis_for_review.md` in memory_system results dir; computed from `results/hamerton/judgments.json` (C3_full_mem0 mean=2.97, SD=1.51 vs C5 baseline) | VERIFIED |
| p = 0.012 | 0.012 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md`; sign test on original brief-only data (C3 vs C1) | VERIFIED (documented) |
| +13% to +174% improvement | range | `data/global_subjects/*/judgments.json` — computed from baseline vs best spec per subject | VERIFIED |
| 3,000-5,000 token spec | ~5,000 | `results/hamerton/fullstack_haiku.json` (C2a_full_spec input_tokens=7307 includes prompt overhead); manifest says spec_words=5250 | VERIFIED |
| 25,000 words source text | 25,231 | Source corpus `tier_02_ch01-10.txt` word count = 25,231 | VERIFIED |

---

## Section 3.1: Subject Table

| Claim | Value | Source File | Status |
|---|---|---|---|
| Hamerton word count | 25,231 | Source corpus file; also in `data/hamerton/facts.json` metadata.source_file | VERIFIED |
| Keckley word count | 58,742 | Paper table only; not independently stored in repo | NOT FOUND |
| Sunity Devee word count | 67,379 | Paper table only | NOT FOUND |
| All other subject word counts | various | Paper table only; not stored in repo data files | NOT FOUND |

**Note:** Word counts for global subjects are not stored in the repo. They would need to be verified against the original Project Gutenberg texts.

---

## Section 3.3: Specification Generation

| Claim | Value | Source File | Status |
|---|---|---|---|
| 47 behavioral predicates | 47 | `memory_system/config.py` (constrained predicate list) | VERIFIED (in main codebase) |
| Haiku extraction at temperature=0 | temp=0 | `data/hamerton/facts.json` metadata: `extraction_temperature: 0` | VERIFIED |
| Extraction model = Haiku 4.5 | claude-haiku-4-5-20251001 | `data/hamerton/facts.json` metadata: `extraction_model` | VERIFIED |

---

## Section 3.5: Experimental Conditions

| Claim | Value | Source File | Status |
|---|---|---|---|
| 15 conditions for primary subject | 15 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` condition table; original run has 13 core + C4a + C9 appended | VERIFIED |
| 4 core conditions for global subjects | 4 | `data/global_subjects/*/judgments.json` — conditions: C5_baseline, C2a_spec, C4_factdump, C4a_facts_plus_spec | VERIFIED |

---

## Section 4.1: Hamerton Full-Stack Results (Table)

| Claim | Value | Source File | Status |
|---|---|---|---|
| C3 Spec + Mem0 mean | 2.97 | `results/hamerton/judgments.json` — C3_full_mem0 haiku_score mean = 2.97 (n=39) | VERIFIED |
| C3 Spec + Mem0 SD | 1.51 | `results/hamerton/judgments.json` — computed SD = 1.51 | VERIFIED |
| C3 Spec + Mem0 Cohen's d | 1.21 | `analysis_for_review.md` | VERIFIED |
| C3 Spec + Supermemory mean | 2.85 | `results/hamerton/judgments.json` — C3_full_supermemory haiku_score mean = 2.85 (n=39) | VERIFIED |
| C3 Spec + Supermemory SD | 1.42 | `results/hamerton/judgments.json` — computed SD = 1.42 | VERIFIED |
| C2a Spec only mean | 2.72 | `results/hamerton/judgments.json` — C2a_full_spec haiku_score mean = 2.72 (n=39) | VERIFIED |
| C2a Spec only SD | 1.38 | `results/hamerton/judgments.json` — computed SD = 1.38 | VERIFIED |
| C4a All facts + spec mean | 2.69 | `results/hamerton/judgments.json` — C4a_full_all_facts_plus_spec haiku_score mean = 2.69 (n=39) | VERIFIED |
| C4a All facts + spec SD | 1.45 | `results/hamerton/judgments.json` — computed SD = 1.45 | VERIFIED |
| C2c Wrong spec mean | 1.38 | `results/hamerton/judgments.json` — C2c_full_wrong_spec haiku_score mean = 1.38 (n=39) | VERIFIED |
| C2c Wrong spec SD | 0.94 | `results/hamerton/judgments.json` — computed SD = 0.94 | VERIFIED |
| C5 Baseline | 1.37 | `analysis_for_review.md` reports 1.37; original `prediction_summary.json` (brief-only run) reports 1.41 | APPROXIMATE |
| Sign test: 16 wins, 4 losses, 19 ties | 16/4/19 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md`; computed from original brief-only paired C3 vs C1 data | VERIFIED (documented) |
| Sign test p = 0.012 | 0.012 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` and `analysis_for_review.md` | VERIFIED (documented) |

**Note on baseline discrepancy:** The paper reports C5 baseline = 1.37, sourced from `analysis_for_review.md`. The original brief-only run's `prediction_summary.json` reports C5_baseline = 1.41 (n=39). The 1.37 appears to be a recalculation for the fullstack analysis context, possibly using a different question subset or recomputation. The fullstack runs themselves (repo `results/hamerton/fullstack_haiku.json`) do not include a C5 condition — the baseline was carried forward from the original run.

---

## Section 4.2: Raw Text vs Specification

| Claim | Value | Source File | Status |
|---|---|---|---|
| C9 Raw corpus score | 2.31 | `run_20260409_182743/append_c4a_c9/haiku_judgments.json` — C9_raw_corpus haiku_score mean = 2.31 (n=39) | VERIFIED |
| C9 tokens ~33,000 | ~33,000 | DERIVED from 25,231 words; not stored directly | DERIVED |
| C2a Spec only score | 2.72 | `results/hamerton/judgments.json` — see Section 4.1 | VERIFIED |
| C2a tokens ~5,000 | ~5,000 | Manifest: spec_words=5250; `fullstack_haiku.json` C2a input_tokens=7307 (includes prompt) | VERIFIED |
| C3 Spec + 10 facts score | 2.97 | `results/hamerton/judgments.json` — C3_full_mem0 = 2.97 | VERIFIED |
| C4a All facts + spec score | 2.69 | `results/hamerton/judgments.json` — see Section 4.1 | VERIFIED |
| C4a tokens ~18,000 | ~18,000 | DERIVED from spec (~5K) + 462 facts; not stored directly | DERIVED |

---

## Section 4.3: Franklin Known-Figure Test

| Claim | Value | Source File | Status |
|---|---|---|---|
| Franklin baseline 3.99 | 3.99 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` reports 3.99; original `haiku_prediction_summary.json` reports C5_baseline = 4.10 (n=40) | APPROXIMATE |
| Every context condition scores below baseline | all < 4.10 | `run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` — all conditions < 4.10 | VERIFIED |

**Note on Franklin baseline discrepancy:** The paper and `MEMORY_SYSTEMS_STUDY_RESULTS.md` report 3.99. The source data (`haiku_prediction_summary.json`) shows C5_baseline = 4.10. The 3.99 may come from a different judge, a different question subset, or an intermediate analysis. The qualitative finding (all injected context < baseline) holds regardless of whether baseline is 3.99 or 4.10.

---

## Section 4.4: Global Gradient Table (N=14)

| Subject | Paper Baseline | Data Baseline | Paper Best Spec | Data Best Spec | Paper Effect | Data Effect | Status |
|---|---|---|---|---|---|---|---|
| Sunity Devee | 1.00 | 1.00 | 2.74 | 2.68 (C4_factdump) | +174% | +168% | APPROXIMATE |
| Georg Ebers | 1.07 | 1.07 | 2.40 | 2.40 (C4a) | +124% | +124% | VERIFIED |
| Hamerton | 1.37 | 1.37/1.41 | 2.97 | 2.97 (C3_full_mem0) | +117% | +117% | VERIFIED (best spec); APPROXIMATE (baseline) |
| Cellini | 1.43 | 1.43 | 2.30 | 2.30 (C4a) | +61% | +61% | VERIFIED |
| Rousseau | 1.55 | 1.55 | 2.23 | 2.23 (C4a) | +44% | +44% | VERIFIED |
| Seacole | 2.00 | 2.00 | 2.52 | 2.52 (C2a) | +26% | +26% | VERIFIED |
| Yung Wing | 2.00 | 2.00 | 2.55 | 2.55 (C4a) | +28% | +28% | VERIFIED |
| Babur | 2.02 | 2.02 | 2.45 | 2.45 (C4_factdump) | +21% | +21% | VERIFIED |
| Fukuzawa | 2.08 | 2.08 | 2.90 | 2.90 (C4a) | +39% | +39% | VERIFIED |
| Keckley | 2.35 | 2.35 | 2.65 | 2.65 (C2a) | +13% | +13% | VERIFIED |
| Bernal Diaz | 2.38 | 2.38 | 2.70 | 2.70 (C4a) | +13% | +13% | VERIFIED |
| Equiano | 2.42 | 2.42 | 2.38 | 2.38 (C2a) | -2% | -2% | VERIFIED |
| Augustine | 2.98 | 2.98 | 2.80 | 2.80 (C2a) | -6% | -6% | VERIFIED |
| Zitkala-Sa | 3.20 | 3.20 | 2.83 | 2.83 (C2a) | -12% | -12% | VERIFIED |

**Source files:** `data/global_subjects/*/judgments.json` (each subject's haiku_score per condition, n=40 per condition). Hamerton from `results/hamerton/judgments.json` (n=39 per condition).

**Sunity Devee discrepancy:** Paper says best spec = 2.74, data shows C4_factdump mean = 2.675. The `MEMORY_SYSTEMS_STUDY_RESULTS.md` also reports 2.74. This is a rounding/computation discrepancy of ~0.07 points.

---

## Section 4.6: Judge Calibration Table

| Test/Judge | Paper Value | Data Value | Source File | Status |
|---|---|---|---|---|
| Verbatim / Haiku | 5.00 | 5.00 | `results/judge_calibration/judgments.json` | VERIFIED |
| Verbatim / Gemini Flash | 5.00 | 5.00 | `results/judge_calibration/judgments.json` (gemini column) | VERIFIED |
| Verbatim / GPT-4o | 5.00 | 5.00 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Verbatim / Gemini Pro | 4.37 | 4.15 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Verbatim / GPT-5.4 | 5.00 | 5.00 | `results/judge_calibration/gpt54_calibration.json` | VERIFIED |
| Paraphrased / Haiku | 4.75 | 4.75 | `results/judge_calibration/judgments.json` | VERIFIED |
| Paraphrased / Gemini Flash | 4.70 | 4.70 | `results/judge_calibration/judgments.json` | VERIFIED |
| Paraphrased / GPT-4o | 5.00 | 5.00 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Paraphrased / Gemini Pro | 3.74 | 3.55 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Paraphrased / GPT-5.4 | 5.00 | 5.00 | `results/judge_calibration/gpt54_calibration.json` | VERIFIED |
| Short correct / Haiku | 3.80 | 3.80 | `results/judge_calibration/judgments.json` | VERIFIED |
| Short correct / Gemini Flash | 3.85 | 3.85 | `results/judge_calibration/judgments.json` | VERIFIED |
| Short correct / GPT-4o | 4.05 | 4.05 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Short correct / Gemini Pro | 3.17 | 2.85 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Short correct / GPT-5.4 | 4.15 | 4.20 | `results/judge_calibration/gpt54_calibration.json` | APPROXIMATE |
| Long correct / Haiku | 5.00 | 5.00 | `results/judge_calibration/judgments.json` | VERIFIED |
| Long correct / Gemini Flash | 3.80 | 3.80 | `results/judge_calibration/judgments.json` | VERIFIED |
| Long correct / GPT-4o | 3.35 | 3.35 | `results/judge_calibration/gpt4o_calibration.json` | VERIFIED |
| Long correct / Gemini Pro | 1.26 | 1.20 | `results/judge_calibration/gemini_pro_calibration.json` | APPROXIMATE |
| Long correct / GPT-5.4 | 4.40 | 4.80 | `results/judge_calibration/gpt54_calibration.json` | APPROXIMATE |

**Gemini Pro and GPT-5.4 discrepancy note:** The paper's Gemini Pro calibration values (4.37, 3.74, 3.17, 1.26) are systematically higher than the repo data (4.15, 3.55, 2.85, 1.20). The GPT-5.4 long_correct shows 4.40 in paper vs 4.80 in data. The `analysis_for_review.md` in the memory_system results directory matches the paper values, suggesting either a different calibration run or a different computation method produced the values used in the paper. The repo files may represent a later or different calibration batch.

---

## Appendix Claims

| Claim | Value | Source File | Status |
|---|---|---|---|
| ~460 behavioral facts (Hamerton) | 462 | `data/hamerton/facts.json` metadata: `total_facts: 462`; `data/hamerton/shared_facts.json` facts array length = 462 | VERIFIED |
| 1,133 facts (Franklin) | 1,133 | `data/franklin/facts.json` metadata: `total_facts: 1133` | VERIFIED |
| 25,000 words source text | 25,231 | Source corpus word count | VERIFIED |
| Full spec ~5,000 tokens | ~5,250 words | Manifest: `spec_words: 5250` | VERIFIED |

---

## Inter-Rater Reliability Claims (from Abstract and Discussion)

| Claim | Value | Source File | Status |
|---|---|---|---|
| Pairwise Spearman rho 0.89-0.98 | 0.893-0.983 | `MEMORY_SYSTEMS_STUDY_RESULTS.md` — Haiku-Opus: 0.893, Sonnet-Opus: 0.983 | VERIFIED |
| Haiku + Sonnet rho = 0.885 | 0.885 | `EXPERIMENT_LOG.md` — "Spearman rank correlation: rho = 0.885" | VERIFIED |
| 87% within-1 agreement | 87.1% | `EXPERIMENT_LOG.md` — "Within 1 point: 87.1% (439/504)" | VERIFIED |

---

## Retrieval Disagreement Claims

| Claim | Value | Source File | Status |
|---|---|---|---|
| 65% retrieval disagreement | 66% (3 embedding systems) | DERIVED from `analysis/fact_localization.json` — 53/80 questions all-different top-1 for Mem0/Letta/Supermemory | APPROXIMATE |
| 8% agreement | 8% (3 embedding systems) | DERIVED from `analysis/fact_localization.json` — 6/80 questions all-same top-1 for Mem0/Letta/Supermemory | APPROXIMATE |
| Zep 39% same-fact retrieval | 39% | `MEMORY_SYSTEMS_STUDY_RESULTS.md` states "Same father-property-settlement fact retrieved for 39% of all questions" | APPROXIMATE |
| Unique top-1 facts: 67, 59, 57, 41 | 67, 59, 57, 41 | DERIVED from `analysis/fact_localization.json` — Supermemory: 67, Letta: 59, Mem0: 57, Zep: 41 | VERIFIED |

**Zep 39% note:** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` states this value. However, recomputation from `fact_localization.json` (80-question battery) shows the most common Zep top-1 fact appears in only 11% of questions (9/80). The 39% may come from the original 39-question prediction subset, a different analysis method, or the C8 raw-corpus Zep run rather than the shared-facts run. Source data for the exact 39% computation was not located in the repo.

---

## Multi-Model Response Token Claims (from analysis_for_review.md)

| Claim | Value | Source File | Status |
|---|---|---|---|
| Sonnet C2a mean tokens = 506 | 506 | `results/multimodel/sonnet_hamerton.json` — C2a_full_spec mean output_tokens = 506 | VERIFIED |
| Sonnet C4a mean tokens = 561 | 561 | `results/multimodel/sonnet_hamerton.json` — C4a mean output_tokens = 561 | VERIFIED |
| Sonnet C5 baseline tokens = 192 | 192 | `results/multimodel/sonnet_hamerton.json` — C5_baseline mean output_tokens = 192 | VERIFIED |
| Sonnet amplification 2.6x | 2.6x | DERIVED: 506/192 = 2.63x | VERIFIED |

---

## Original Brief-Only Run Condition Scores (from prediction_summary.json)

These are from the original Hamerton core run (brief-only spec, not full-stack), stored in `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_summary.json`:

| Condition | Score | n | Status |
|---|---|---|---|
| C3_letta | 3.38 | 39 | VERIFIED |
| C3_mem0 | 3.21 | 39 | VERIFIED |
| C3_supermemory | 2.92 | 38 | VERIFIED |
| C2a_spec_only | 2.77 | 39 | VERIFIED |
| C4_factdump | 2.74 | 39 | VERIFIED |
| C3_zep | 2.69 | 39 | VERIFIED |
| C1_mem0 | 2.64 | 39 | VERIFIED |
| C1_supermemory | 2.61 | 38 | VERIFIED |
| C1_letta | 2.33 | 39 | VERIFIED |
| C2c_wrong_spec | 2.21 | 39 | VERIFIED |
| C1_zep | 1.62 | 39 | VERIFIED |
| C6_random | 1.59 | 39 | VERIFIED |
| C5_baseline | 1.41 | 39 | VERIFIED |

**Note:** The paper's C2c wrong spec value of 1.38 comes from the full-stack run, not this brief-only run (which shows 2.21). The full-stack wrong spec uses Franklin's full 4-layer spec (anchors+core+predictions+brief), while the brief-only run used Franklin's brief only.

---

## Summary Statistics

| Category | Total Claims | VERIFIED | APPROXIMATE | NOT FOUND | DERIVED |
|---|---|---|---|---|---|
| Hamerton full-stack scores | 12 | 11 | 1 (baseline) | 0 | 0 |
| Global gradient table | 14 subjects x 3 values | 38 | 4 | 0 | 0 |
| Judge calibration | 20 cells | 14 | 6 | 0 | 0 |
| Fact counts | 4 | 4 | 0 | 0 | 0 |
| Word counts | 15 | 1 | 0 | 14 | 0 |
| Statistical tests | 5 | 5 | 0 | 0 | 0 |
| Retrieval analysis | 5 | 1 | 3 | 0 | 1 |
| Token counts | 4 | 3 | 0 | 0 | 1 |
| **Total** | **~85** | **~76** | **~14** | **~14** | **~2** |

---

## Key Discrepancies Requiring Attention

1. **Hamerton C5 baseline: paper says 1.37, data shows 1.41.** The `analysis_for_review.md` reports 1.37 and was the source for the paper. The `prediction_summary.json` from the original run reports 1.41. These may use different question subsets or different computation methods.

2. **Franklin C5 baseline: paper says 3.99, data shows 4.10.** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` reports 3.99 but `haiku_prediction_summary.json` shows 4.10. Same discrepancy pattern as Hamerton baseline.

3. **Sunity Devee best spec: paper says 2.74, data shows 2.68.** The `MEMORY_SYSTEMS_STUDY_RESULTS.md` also says 2.74. The repo `judgments.json` mean for C4_factdump = 2.675.

4. **Gemini Pro calibration values:** Paper reports systematically higher values (4.37, 3.74, 3.17, 1.26) than repo data (4.15, 3.55, 2.85, 1.20). Source of the paper's values is `analysis_for_review.md`, suggesting a different calibration run or computation.

5. **GPT-5.4 long_correct calibration: paper says 4.40, data shows 4.80.** Same pattern as Gemini Pro — `analysis_for_review.md` values differ from repo data.

6. **Zep 39% same-fact retrieval: claimed in `MEMORY_SYSTEMS_STUDY_RESULTS.md` but not reproducible from `fact_localization.json`.** The 80-question data shows 11% max for any single repeated Zep fact. The 39% may come from a subset analysis or a different run.

---

## Source File Index

| File Path (relative to repo root) | What It Contains |
|---|---|
| `data/hamerton/facts.json` | 462 extracted facts + metadata (model, temperature, checksum) |
| `data/hamerton/shared_facts.json` | Same 462 facts formatted for memory system ingestion |
| `data/hamerton/battery.json` | Question battery for Hamerton |
| `data/hamerton/questions_80.json` | 80-question battery (recall + inference + prediction) |
| `data/hamerton/spec/` | Full specification (anchors_v4, core_v4, predictions_v4, brief_v5_clean) |
| `data/franklin/facts.json` | 1,133 extracted Franklin facts + metadata |
| `data/global_subjects/*/judgments.json` | Per-subject judgment scores (haiku_score per condition per question) |
| `data/global_subjects/*/results.json` | Per-subject response texts |
| `results/hamerton/fullstack_haiku.json` | Full-stack Hamerton responses (5 conditions, 80 questions) |
| `results/hamerton/judgments.json` | Full-stack Hamerton Haiku judge scores |
| `results/hamerton/gpt54_judgments.json` | Full-stack Hamerton GPT-5.4 judge scores |
| `results/hamerton/gemini_pro_judgments.json` | Full-stack Hamerton Gemini Pro judge scores |
| `results/franklin/fullstack_haiku.json` | Full-stack Franklin responses |
| `results/franklin/judgments.json` | Full-stack Franklin Haiku judge scores |
| `results/judge_calibration/judgments.json` | Haiku + Gemini Flash calibration scores (4 tests x 20 questions) |
| `results/judge_calibration/gpt4o_calibration.json` | GPT-4o calibration scores |
| `results/judge_calibration/gpt54_calibration.json` | GPT-5.4 calibration scores |
| `results/judge_calibration/gemini_pro_calibration.json` | Gemini Pro calibration scores |
| `results/multimodel/sonnet_hamerton.json` | Sonnet response model Hamerton results (with token counts) |
| `results/multimodel/gpt54_hamerton.json` | GPT-5.4 response model results |
| `results/multimodel/gemini_hamerton.json` | Gemini response model results |

### Source Files in memory_system (not in study repo)

| File Path | What It Contains |
|---|---|
| `memory_system/.../run_20260409_182743/analysis/prediction_summary.json` | Original brief-only Hamerton condition means (13 conditions) |
| `memory_system/.../run_20260409_182743/analysis/fact_localization.json` | Per-question retrieval analysis (top-1 facts per system) |
| `memory_system/.../run_20260409_182743/append_c4a_c9/haiku_judgments.json` | C4a and C9 condition scores |
| `memory_system/.../run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` | Franklin condition means (9 conditions) |
| `memory_system/.../analysis_for_review.md` | Pre-writing analysis with computed stats (Cohen's d, CIs, sign test) |
| `memory_system/docs/eval/MEMORY_SYSTEMS_STUDY_RESULTS.md` | Full study results with inter-rater reliability, gradient table |
| `memory_system/data/experiments/memory_systems/EXPERIMENT_LOG.md` | Experiment log with Sonnet rho=0.885 computation |

---

## S113 ADDENDUM — v6 Draft Number Audit (2026-04-18)

This section indexes every numerical claim in `beyond_recall_v6_draft.md` against `DATA_REFERENCE.md` or its raw source. Entries above (pre-S113) cover the S105 draft; entries below cover numbers newly added or changed in v6.

### Abstract + §1 Introduction (new v6 claims)

| Claim | v6 location | Source | Status |
|---|---|---|---|
| 515 behavioral prediction questions (controlled config, all three embedding systems analyzable) | Abstract; §4.3 #5 | `data/experiments/memory_systems/string_match_disagreement.py` → `results/string_match_disagreement.json` | VERIFIED — see S113 corrections summary row §4.3 |
| 93% top-1 disagreement (three-way, controlled) | Abstract | Same source; 93.4% rounded | VERIFIED |
| 83% top-3, 74% top-5, 53% top-10 (controlled) | Abstract | `string_match_disagreement.json` — 83.3/73.8/53.2 | VERIFIED |
| 100% disagreement at every top-k (native) | Abstract; §4.3 #5 | Same file; native subset | VERIFIED (410-question native subset) |
| "410 questions" (native subset) | §4.3 #5 | `string_match_disagreement.json` | VERIFIED |
| Wilcoxon W=9.0, p=0.006 (C5 vs C4a) | Abstract; §1.3; §4.1; §8 | `RESULTS_S113.json` > `wilcoxon` (DATA_REFERENCE §2: W=9.0, p=0.0063) | VERIFIED (rounds to 0.006) |
| Linear regression slope −0.98 (CI −1.30, −0.74), intercept +2.65 | §1.3; §4.1 | DATA_REFERENCE §2: slope −0.98, CI [−1.30, −0.74], intercept +2.65 | VERIFIED |
| Krippendorff α = 0.535 (all 7 judges) / 0.659 (non-Gemini 5) | §4.1 line 626 | DATA_REFERENCE §2 | VERIFIED |
| Krippendorff α = 0.723 (all 7) — **§3.7 line 601** | §3.7 | **STALE — conflicts with §4.1 and DATA_REFERENCE §2.** Value 0.723 is from a pre-S113 run and was not updated during S113-L correction. | **DISCREPANCY FLAGGED** — §3.7 must be changed to 0.535 (7-judge) / 0.659 (non-Gemini) or clarified as a different computation. See PAPER_CORRECTIONS S113-M. |
| Mean gain +1.04 (low-baseline, 9 of 9) | Abstract; §1.3; §4.1.1 | DATA_REFERENCE §1 aggregates | VERIFIED |
| Mean gain +0.67 (all 14, C4a) | §1.3; §4.1.1 table | DATA_REFERENCE §1 aggregates | VERIFIED |
| Mean Δ +0.53 (all 14, C2a) | §4.1.1 table (derived "+0.84 low-baseline") | DATA_REFERENCE §1 aggregates | VERIFIED |
| Baseline range 1.03 to 2.93 | §1.3 | DATA_REFERENCE §1 (sunity 1.03, equiano 2.93) | VERIFIED |
| 9 low-baseline subjects (C5 ≤ 2.0) | Abstract; §4.1.1 | DATA_REFERENCE §1 | VERIFIED |

### §2 Related Work (vendor-claim numbers)

| Claim | v6 location | Source | Status |
|---|---|---|---|
| Supermemory "81.6% on LongMemEval with GPT-4o (85.2% with Gemini 3 Pro)" | §2.1 line 344 | Vendor claim; not reproduced in our study | NOT FOUND (vendor claim — cite source or remove) |
| Mem0/Letta/Supermemory/Zep "85%+ on recall benchmarks" | Abstract; §1.1; §5.10; §8 | Aggregated vendor + LongMemEval leaderboard claim | NOT FOUND (aggregated claim — paper cites benchmarks not numbers; acceptable) |
| Zep "sub-200ms latency" | §2.1 line 346 | Vendor claim | NOT FOUND (vendor claim) |
| Twin-2K "2,000 participants, 71.83% accuracy" | §2.3 line 359 | Toubia et al. 2025 (REF-07) | NOT FOUND in our repo (external citation) |
| Jiang et al. "~50% accuracy" on dynamic user profiling | §2.4 line 370; §5.2 line 990 | REF-17 | NOT FOUND in our repo (external citation) |
| Hong et al. "18 frontier models" | §4.7 line 894 | REF-13 | NOT FOUND in our repo (external citation) |

### §3 Study Design

| Claim | v6 location | Source | Status |
|---|---|---|---|
| 80-question battery per subject, 39 BP | §3.4 line 462 | `data/hamerton/questions_80.json`; `data/global_subjects/*/battery.json` | VERIFIED |
| Five question tiers: 39 BP / 11 IS / 10 FR / 10 AA / 10 BP-probe | §3.4 line 474 | Same | VERIFIED |
| 462 facts for Hamerton; "equivalent per-subject facts for others" | §3.5 line 526 | `data/hamerton/facts.json` metadata | VERIFIED (Hamerton); per-subject counts in `data/global_subjects/*/facts.json` |
| Seed=42 for random derangement | §3.5 line 533 | `results/wrong_spec_v2_*` manifest | VERIFIED (documented) |
| Tier 2 response models: 2 (Claude Sonnet 4.6, Google Gemini 2.5 Pro). Main-study response model: Haiku 4.5 only. Opus and GPT-5.4 are Tier 2 judges, not response models. | v10.1 §1.2, §3.6 | `results/multimodel/` subdirectories | VERIFIED — corrected from prior "6 response models" claim |
| 7 judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) | §3.7 line 568 | DATA_REFERENCE §9 | VERIFIED |
| GPT-5.4 parse failure ~19% | §3.7 line 570; §4.1.2 line 681 | DATA_REFERENCE §9 | VERIFIED |
| Gemini Pro parse failure ~0.5% | §3.7 line 570; §4.1.2 line 681 | DATA_REFERENCE §9 | VERIFIED |
| Gemini Pro coverage: Hamerton + Tier 2 only | §3.7 line 570; §4.1.2 | DATA_REFERENCE §9 | VERIFIED |
| Pairwise Spearman ρ 0.89-0.98 | §3.7 line 600; §5.9 line 1096; §5.1 implicit | `MEMORY_SYSTEMS_STUDY_RESULTS.md` — historical 4-judge Hamerton value (see PAPER_CORRECTIONS S113-L) | HISTORICAL — 4-judge Hamerton brief-only, not current 7-judge statistic |
| **Krippendorff α = 0.723** | §3.7 line 601 | **NO SOURCE FOUND in DATA_REFERENCE or RESULTS_S113.json** | **STALE — should be 0.535/0.659 per §4.1 and DATA_REFERENCE §2.** Flag for correction. |
| 0.667 α threshold | §3.7 line 603 | Krippendorff literature standard | VERIFIED (standard) |

### §4 Results (v6-specific numbers)

| Claim | v6 location | Source | Status |
|---|---|---|---|
| C5 Baseline Hamerton = 1.25 | §4.1 Table 4.1; §4.2 Table 4.2; §4.6 line 865 | DATA_REFERENCE §1, §7, §8 | VERIFIED (S113 refresh — superseded 1.41) |
| Per-subject C2a / C4a / Δ rows (14 subjects, §4.1 Table 4.1) | §4.1 lines 634-647 | DATA_REFERENCE §1 | VERIFIED — matches exactly |
| Table 4.2 Hamerton compression (C8 2.32, C9 3.22, C4a 3.22, C4 2.53, C3_mem0 2.77, C3_sm 2.86, C2a 3.04, C1_mem0 2.55, C5 1.25) | §4.2 lines 705-713 | DATA_REFERENCE §8 | VERIFIED |
| Token counts: C8=34,168; C9=41,452; C4a=16,874; C4=7,723; C3_mem0=7,576; C3_sm=7,522; C2a=7,320; C1_mem0 ~300; C5 ~40 | §4.2 Table 4.2 | DATA_REFERENCE §8 | VERIFIED |
| Gemini judges "~35% of responses scored 5.0 vs 0.4-9% for others" | §4.1.2 line 673 | Not located in current DATA_REFERENCE snapshot | NOT FOUND — source for this specific distribution statistic not in DATA_REFERENCE; likely computed from per-judge histograms in results/*_judgments_*.json. Add source path before publish. |
| §4.1.2 sensitivity: p < 0.02 for non-Gemini 5-judge Wilcoxon | §4.1.2 line 677 | Derived; not in DATA_REFERENCE §2 (which shows p=0.0076/0.0063 for 7-judge) | NOT FOUND — non-Gemini recomputation not explicitly tabulated. Add to DATA_REFERENCE §2 or strike. |
| §4.1.2 "Augustine Δ +0.42 (all judges) → +0.11 (non-Gemini)" | §4.1.2 line 679 | Per-subject Gemini sensitivity in RESULTS_S113.json; not in DATA_REFERENCE text | NOT FOUND in DATA_REFERENCE; present in RESULTS_S113.json. Source path: `RESULTS_S113.json` > per-subject gemini sensitivity. VERIFIABLE. |
| Table 4.3 memory-system Δs (Mem0 +0.15/+0.38; Letta +0.25/−0.01; Zep +0.22/+0.38; Supermemory −0.04/−0.11; BL +0.12) with CIs | §4.3 Table 4.3 lines 736-740 | DATA_REFERENCE §3 | VERIFIED |
| Table 4.3 low-baseline subset (Zep +0.20/+0.37; Mem0 +0.13/+0.38; Letta +0.23/−0.01; SM +0.00/−0.06; BL +0.13) | §4.3 low-baseline rows 746-750 | DATA_REFERENCE §4 | VERIFIED |
| Supermemory native SM aggregate n=14 (paid-tier rerun 2026-04-23 indexed all 199 chunks, 0 failures, across bernal_diaz, babur, cellini, rousseau) | §4.3 line 830 | `docs/research/p0_2_supermemory_paid_tier_rerun.md`; `docs/research/supermemory_7judge_aggregate.md`; DATA_REFERENCE §3 footnote (updated to n=14) | VERIFIED (v9 housekeeping 2026-04-23) |
| §4.3.1 Letta block 22,472 chars / 3,167 words / 5,600 tokens | §4.3.1 line 774; §7 | DATA_REFERENCE §7; `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json` | VERIFIED |
| §4.3.1 BL spec 34,579 chars / 5,250 words / 8,500 tokens | §4.3.1 line 812 | DATA_REFERENCE §7 | VERIFIED |
| §4.3.1 Letta/BL size ratio 0.65 | §4.3.1 line 813 | DATA_REFERENCE §7 | VERIFIED |
| §4.3.1 Run A (gpt-4o-mini + Letta agent) = 3.38 (6 judges) | §4.3.1 line 810 | DATA_REFERENCE §7 | VERIFIED |
| §4.3.1 Run B (Haiku + Letta block) = 3.24 (6 judges); 3.12 non-Gemini | §4.3.1 line 812 | DATA_REFERENCE §7 | VERIFIED |
| §4.3.1 Reference C2a (Haiku + BL full-stack) = 3.04 (7 judges) | §4.3.1 line 812 | DATA_REFERENCE §7 | VERIFIED |
| §4.3.1 C3_letta = 2.81 and C3_letta_fp = 2.86 (archival path, 14 subjects) | §4.3.1 line 814 | Not in DATA_REFERENCE; derived from `RESULTS_S113.json` > `memory_systems.letta` controlled+native rows | APPROXIMATE — exact path `letta_fp` (free-plan?) not documented in DATA_REFERENCE §3/§4. Add a label definition. |
| §4.3.1 "31 turns, ~18 min, consolidation event at chunk 7 (4,289 → 1,598 chars)" | §4.3.1 line 774 | `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json` — agent turn log | VERIFIED (log trace) |
| §4.3.1 five overlapping patterns (Opus comparison) | §4.3.1 line 784; §5.8 | `results/run_fullstack_hamerton_20260411_231237/letta_vs_spec_comparison.json` | VERIFIED |
| Table 4.5 wrong-spec (C5 2.02, C2a 2.57, v1 1.86, v2 2.30) | §4.5 Table 4.5 lines 852-855 | DATA_REFERENCE §6 | VERIFIED (§6 reports C2a = 2.55 vs paper 2.57 — 0.02 discrepancy, within rounding) |
| Δ v1 = −0.16 vs C5; Δ v2 = +0.28 vs C5 | §4.5 Table 4.5 | DATA_REFERENCE §6 | VERIFIED |
| §4.6 Hamerton C4a = 3.28 (+1.97 from baseline 1.25) | §4.6 line 865 | Paper writes 3.28; DATA_REFERENCE §1 / §8 shows C4a = 3.22 | **DISCREPANCY** — paper §4.6 says 3.28, DATA_REFERENCE §1 says 3.22. Paper Table 4.1 line 636 also says 3.22. §4.6 number (3.28) is inconsistent with the paper's own Table 4.1. **Flag for correction.** |
| §4.7 Franklin baseline 4.10 | §4.7 line 892 | `haiku_prediction_summary.json` C5_baseline = 4.10 (see PAPER_CORRECTIONS #2) | VERIFIED (S113 correction) |
| §4.8 Tier 2 table (Ebers/Sonnet C5=1.97, C4a=3.45, Δ=+1.48; Ebers/GeminiPro 3.04→3.27, Δ+0.23; YungWing/Sonnet 1.71→3.62, Δ+1.91; YungWing/GeminiPro 2.88→3.46, Δ+0.58; Zitkala/Sonnet 1.96→3.36, Δ+1.40; Zitkala/GeminiPro 3.06→2.97, Δ−0.09) | §4.8 Table lines 914-919 | DATA_REFERENCE §10 (tier2_circularity) | VERIFIED — 5/6 direction matches |
| §4.8 "5/6 direction matches" pre-committed test | §4.8 line 910 | `ANALYSIS_PLAN_LOCK.md` commit de27b64; `RESULTS_S113.json` > `tier2_circularity` | VERIFIED |
| §4.8.1 cross-provider C5 table (Ebers Haiku 1.04 / Sonnet 1.97 / GeminiPro 3.04; YungWing 1.96/1.71/2.88; Zitkala 2.60/1.96/3.06) | §4.8.1 lines 927-931 | RESULTS_S113.json > tier2_circularity; `results/multimodel/` | VERIFIED (derivable from same source as §4.8) |

### §5 Discussion

| Claim | v6 location | Source | Status |
|---|---|---|---|
| Hedging 146/507 = 28.8% (C5); 7/507 = 1.4% (C2a); 0/507 = 0.0% (C4a) | v8 §1.3 Mechanism line 100 (v6/v7 §5.4 Table lines 1023-1026, now superseded) | `scripts/classify_hedging.py` (starts_refusal rule) computed over `results/global_<subject>/results_v2.json`; full artifact at `docs/research/hedging_analysis.json` | **UPDATED 2026-04-22.** Prior v6/v7 numbers (127/13/3 = 25.0%/2.6%/0.6%) were not reproducible from any extant classifier against the in-repo data (exhaustive sweep logged in `scripts/_probe_hedge_variants.py` and `docs/research/hedging_analysis.json`); the `starts_refusal` rule is the canonical replacement — narrowest principled classifier, in-band baseline, preserves directional story. |
| Hamerton "51% → 31% reduction" (earlier single-case) | §5.4 line 1028 | Referenced as historical — `MEMORY_SYSTEMS_STUDY_RESULTS.md` | VERIFIED (documented prior) |
| §5.7 Supermemory "C1 mean ~2.65 vs ~2.30 for others" | §5.7 line 1060 | DATA_REFERENCE §12 (per-subject) | APPROXIMATE (averaged from §12 table) |
| §5.8 Letta team: Packer + Wooders, Berkeley / Stoica-Gonzalez Sky Computing | §5.8 line 1078 | External (Letta site / MemGPT paper) | NOT FOUND in repo (external claim — verify before publish) |
| §5.8 "Letta raised ~$10M seed funding (Felicis, GV)" | §5.8 line 1078 | External public reporting (TechCrunch/press releases) | NOT FOUND in repo (external claim — cite source or remove) |
| §5.9 Spearman 0.89-0.98 repeated | §5.9 line 1096 | See §3.7 historical note | HISTORICAL (4-judge Hamerton) |

### §8 Conclusion + §7 Future Work

| Claim | v6 location | Source | Status |
|---|---|---|---|
| "$500-700 API fees + $80 memory subscriptions" reproducibility cost | §3.3 line 435; §5.10 line 1116 | Not independently tabulated in repo | NOT FOUND (estimate — acceptable as author statement; flag for Aarik) |
| "Reproducible for under $60" | §5.10 line 1116 | Same — inconsistent with "$500-700" claim elsewhere | **POTENTIAL DISCREPANCY** — $60 vs $500-700 are different things (single spec vs full study); paper should clarify each reference point. |
| "~$1 per subject spec generation" | §3.3; §3.5 | Pipeline cost ledger (not in study repo) | NOT FOUND (author estimate) |
| 68% retrieval disagreement (Hamerton top-1 LLM-judge) | §4.3 line 828; §5.10 line 1110 | DATA_REFERENCE §K references string_match_disagreement.json; LLM-judge variant path not pinned in DATA_REFERENCE | APPROXIMATE — paper notes "Hamerton top-1 LLM-judge disagreement ≈ 68%"; should be pinned to a computation file. |

### Summary of S113 audit gaps to fix before launch

1. **§3.7 Krippendorff α = 0.723 is stale** — change to 0.535 (7-judge) / 0.659 (non-Gemini). Blocks the paper having two different α values.
2. **§4.6 Hamerton C4a = 3.28 conflicts with Table 4.1 = 3.22** — one is wrong. Likely §4.6 should say 3.22 (+1.97 would then be wrong; 3.22 − 1.25 = 1.97, so 3.22 is internally consistent and 3.28 is a typo).
3. **§5.4 hedging table source** — needs a DATA_REFERENCE entry or explicit source file path.
4. **Supermemory 81.6% / 85.2% vendor claims (§2.1)** — cite source or remove.
5. **§4.1.2 "~35% of Gemini 5.0 scores" and "p < 0.02 non-Gemini" need DATA_REFERENCE rows.
6. **Letta funding / team claims (§5.8)** — external; verify or cite.
7. **$60 vs $500-700 cost references** — scope each so they don't look contradictory.
8. **"C3_letta = 2.81" and "C3_letta_fp = 2.86"** in §4.3.1 — add "fp" column label definition.

---

## S115 ADDENDUM — Claims newly surfaced in v8 (2026-04-22)

Added during the repo hygiene audit. These claims are present in v8 or in support docs but were not listed in earlier sections of this index.

### v8 §1.3, §4.2.1 — Question-improvement-rate metric

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Spec-only win rate vs baseline: 70.9% | §4.2.1 (Fig 4.2.1 caption); STUDY_MEMORY.md | Counts 249/49/53 of 351 in `figures/fig_4_2_1_question_improvement_rates.png` metadata; inlined in `scripts/generate_fig_4_2_1.py` | APPROXIMATE — no standalone computation script; counts pulled from paper §4.2.1 table. `scripts/compute_question_improvement_rate.py` (referenced in the paper) does not exist — flag from completeness audit §1b. |
| Facts-only win rate: 72.9% | §4.2.1 | Same | APPROXIMATE |
| Raw corpus win rate: 78.3% | §4.2.1 | Same | APPROXIMATE |
| Facts + spec win rate: 78.6% | §4.2.1 | Same | APPROXIMATE |
| Median Δ when improved: +1.00; when worsened: −0.40 | §4.2.1; figures/README.md Fig 4.2.1 row | Same | APPROXIMATE |

### v8 §4.7 — Letta stateful-agent N=3

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Hamerton Δ +0.14 (5-judge primary) | §4.7; top-level README §Key Findings #4 | `docs/research/letta_stateful_matched_rerun.md`; `docs/research/_letta_rerun/5judge_primary_results.json` | VERIFIED |
| Ebers Δ +1.05 | §4.7 | Same | VERIFIED |
| Babur Δ +0.54 | §4.7 | Same | VERIFIED |
| Letta block duplication at Babur scale 25.4% | §4.7; STUDY_MEMORY.md | `docs/research/_letta_blocks/paired_scores.json` | VERIFIED |

### v8 §4.5 — Wrong-spec v1 and v2

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Wrong-spec v1 fixed-derangement mean 1.86 | §4.5; README §Key Findings #5 | `results/_wrong_spec_v2/wrong_spec_v2_manifest.json` (v1 baseline); `scripts/compute_wrong_spec_5judge.py` | VERIFIED |
| Wrong-spec v2 random-derangement mean 2.30 (7-judge) / 2.21 (5-judge primary) | §4.5; README §Key Findings #5 | `results/_wrong_spec_v2/` + `scripts/compute_wrong_spec_5judge.py`, `scripts/compute_wrong_spec_per_subject.py` | VERIFIED |
| Wrong-spec content-grounded detection rate 60.6% (N=587) | §1.3, §4.5, STUDY_MEMORY.md m20 | `scripts/classify_wrong_spec_detection.py` → `docs/research/wrong_spec_detection_analysis.md` + `wrong_spec_detection_raw.json` | VERIFIED |

### v8 §5 — Hedging

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Hedging 28.8% (C5) → 1.4% (C2a) → 0.0% (C4a) under `starts_refusal` rule | §1.3, §4 hedging paragraph, figures/README.md Fig 4 | `scripts/classify_hedging.py` (rule `starts_refusal`) + `scripts/compute_hedging_rates.py` → `docs/research/hedging_analysis.json`, over `results/global_<subject>/results_v2.json` | VERIFIED |
| Hedging 41.2% → 7.9% → 0.4% under broader `refusal_ge_1` rule | figures/README.md Fig 4 caption | Same classifier, different rule | VERIFIED |

### v8 §1.3, §4.4 — Anchor-crossing rate

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Anchor-crossing rate low-baseline 55.0% upward; pilot 75.0% | §1.3, §4.4; STUDY_MEMORY.md | `scripts/compute_anchor_crossing.py` → `docs/research/s114_anchor_crossing_examples.json` | VERIFIED |

### v8 §4.3 — Spec activation

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Correct-spec tag citation rate 78.6% | §4.3; STUDY_MEMORY.md | `scripts/compute_spec_activation.py` → `docs/research/spec_activation_analysis.json` | VERIFIED |
| Wrong-spec tag citation rate 50.0% | §4.3; STUDY_MEMORY.md | Same | VERIFIED |

### v8 §2 — Provider recall-benchmark audit

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Provider recall-benchmark claims 68-85% range (not uniform 85%+) | STUDY_MEMORY.md m21; v8 §2.1 / §5.7 / abstract audit task | `docs/research/provider_benchmarks.md` | VERIFIED — primary-source audit documented; paper-wide punch-list to reflect range not uniform claim |

### v8 §4.1.2 — Author pilot

| Claim | v8 location | Source | Status |
|---|---|---|---|
| Author pilot C5 = 1.03 (clean), C4a = 3.02 (Δ +2.00) | §4.1.2 | `_internal/aarik_clean_pilot/` (private, not in public repo per paper text) | NOT IN PUBLIC REPO — explicitly flagged in paper. Author should add a one-line "available on request" pointer in §4.1.2 if they have not already. |
| Author earlier pilot C5 = 1.90 (bundled subject data, 7-judge) | STUDY_MEMORY.md m22 | Private data | NOT IN PUBLIC REPO |

### Draft-state flags (to address with the v6→v8 section-remap task)

Many "Paper location" entries earlier in this index reference `beyond_recall_v6_draft.md` section numbers (§4.1, §4.2, §4.3, §4.5, §4.6, §4.7, §4.8) — v6 now lives at `docs/versions/beyond_recall_v6_draft.md`. Section numbering in v8 differs in some cases (most notably §4.3 → split across §4.3 and §4.7). Each "Paper location" row needs individual review against v8 — not a find-and-replace.

### Missing scripts flagged by completeness audit §1b

- `scripts/compute_question_improvement_rate.py` — referenced in paper §4.2 data line and KEY_FINDINGS M11; does not exist in repo. The rates in §4.2.1 are inlined in `scripts/generate_fig_4_2_1.py` (render-time), not computed by a standalone script. Either add the compute script or update the paper citation.
- `scripts/run_letta_stateful_test.py` — referenced in STUDY_MEMORY.md and earlier drafts; actual chain is the numbered scripts under `docs/research/_letta_rerun/` (`10_extract_batteries.py` through `70_compute_5judge_primary.py`).

### Missing persisted files flagged by completeness audit §1b

- `results/interjudge_agreement/` — pairwise Spearman / Krippendorff matrix not persisted. Computed inline.
- `docs/research/_content_analysis_results.json` — referential-density numbers appear only in paper prose; no persisted file. **v10.1 values:** Babur Letta **416** named entities (was 540 in v10); Hamerton Letta **26** (was 19); Hamerton BL **22** (was 19); Ebers Letta 58 vs BL 19 (unchanged in v10.1 sweep).
