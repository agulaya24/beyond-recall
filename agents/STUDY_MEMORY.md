# Study Memory — "Beyond Recall" Experiment Only

Persistent memory for agents/sessions working on the "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization" study. Scoped to this experiment only — not the broader Base Layer project memory.

> **v11 RELEASE-FROZEN 2026-04-28; v10.1 PRESERVED AS HISTORICAL BASELINE.** Citable canonical paper draft: `docs/beyond_recall_v11_draft.md` (release-frozen 2026-04-28). Effective 2026-04-28, this is the canonical artifact for citation, reproduction, and any external reference. Headline numbers carry forward unchanged from v10.1; v11 adds new content registered in the 2026-04-28 data-locking pass (see "v11 numbers status" below). Freeze record: "V11 FREEZE — 2026-04-28" section of `docs/reviews/v11_running_changes_log_20260427.md`. Per-claim source of truth for v11: `docs/research/v11_confidence_catalog_20260428.md`.
>
> **v10.1 preserved historical baseline: `docs/beyond_recall_v10_1_draft.md`** (release-frozen 2026-04-25, pass 3 closed). Was the citable canonical until v11's freeze on 2026-04-28; preserved as reference. Do not edit. Earlier drafts (v10 lineage prose, v9, v8, v7, v6) are also preserved baselines. Release-pass closures: `docs/reviews/v10_release_freeze_pass_report.md` (2026-04-24, v10 pass 1), `docs/reviews/v11_release_freeze_status_20260425.md` (2026-04-25, v10.1 pass 2), v10.1 pass 3 record (2026-04-25, see ISSUES.md), and the v11 freeze record in `docs/reviews/v11_running_changes_log_20260427.md` (2026-04-28).
>
> **2026-04-25 release-freeze pass 3 deltas (GPT-5.5 v10.1 review fixes):**
>
> 1. **§4.1 battery-generator wording corrected.** Ground truth: ALL 14 main-study batteries (Hamerton + 13 globals) are Haiku-generated. The legacy "13 globals = GPT-5.4 batteries" wording was wrong. Subset regression in `_v10_battery_sensitivity.py` is the drop-Hamerton subset, not a "restrict to GPT-5.4-battery subjects" subset. GPT-5.4-regenerated batteries exist as a circularity control (§3.4.1 + Tier 2 cross-provider), not as the main-study batteries.
> 2. **Tier 2 cross-provider directional probe is 2 response models** (Sonnet 4.6, Gemini 2.5 Pro), NOT 4. Opus and GPT-5.4 in Tier 2 are judges, not response models. Tier 2 batteries are GPT-5.4-generated.
> 3. **§4.3 wrong-spec denominator clarified:** 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers).
> 4. **§4.4.2 Table 4.6 rebuilt on strict 5-judge primary panel.** Entire table (all 8 rows), no sign flips; Letta/Hamerton drops to n=38.
>
> **Revision-quality items applied in pass 3:** §1.4 / §5.3 living-user "expected by construction" softened to "closest available proxy"; §4.1 / §5.5 "C4a ceiling" reframed to "post-spec operating level"; §5.2 H5 reframed (fact extraction does most volume-reduction; spec adds marginal per-question value); §4.4 memory-system additivity nuanced (Zep + Mem0-native strongest, Mem0-controlled small, Letta archival positive controlled / near-null native, Supermemory mixture); §4.6.1 "not Haiku-specific" softened to "small probe reduces likelihood, does not establish model-family invariance"; v11 mechanistic-check audit relabeled "verification audit" in paper prose (file paths to `v11_emit/` preserved).
>
> **2026-04-25 release-freeze pass 2 deltas (preserved record):** §4.3 random-derangement +0.22 → +0.15 cascaded across §1.3, §4.3, §4.6.2, §5; §4.4.2 Supermemory mixture-of-swings counts updated to 5-judge primary panel (89/516 (17.2%) → 110/546 (20.1%); 37/52 helps/hurts → 57/53; +1.45/−1.41 mean swings → +1.55/−1.38); §4.6.1 Tier 2 cross-provider replication demoted to direction-only with sensitivity ranges (no specific magnitudes carry through; directional claim of 5 of 6 cells retained); panel-completeness audit GREEN on all 441 unwaived rows.
>
> **v11 mechanistic-check architecture compliance (deferred post-arXiv).** All 8 `_v11_emit_*.py` scripts are MAJOR or BLOCKER offenders against the schema contract; representative `_v11_emit_4_1_gradient.py` is the BLOCKER reference. Hardcoded `PAPER_*` dicts, no SHA manifests, no claim-tag injection, no full numeric-literal census tool, no §4.6.1 emit script. Estimated 80-100 hours to close. Status detail: `docs/research/v11_emit/_ARCHITECTURE.md` §12. v10 arXiv submission proceeds on the basis of the GREEN panel-completeness audit, the cleared reconciliation diff (1,089 MATCH / 65 MINOR / 206 SUBSTANTIVE resolved by Tier 1+2+3 edits), and the §4.6.1 demotion.
>
> **Before any work: read [`../ISSUES.md`](../ISSUES.md) at repo root.** Tracks open quality-audit findings.

**Source of truth for numbers:** `docs/DATA_REFERENCE.md` (5-judge primary; v10.1 numbers carried forward unchanged into v11; v11 additions registered in the 2026-04-28 data-locking pass). The 5-judge primary recompute is canonical across §4; the 7-judge mixed panel is the sensitivity layer. For v11-specific claims, the per-claim source of truth is `docs/research/v11_confidence_catalog_20260428.md`.

**Citable canonical paper draft:** `docs/beyond_recall_v11_draft.md` (v11, release-frozen 2026-04-28). **Preserved historical baseline:** `docs/beyond_recall_v10_1_draft.md` (v10.1, release-frozen 2026-04-25). v10 lineage prose, v9, v8, v7 also preserved as baselines.

---

## v11 active edits 2026-04-27 (preserved record, pre-freeze)

v11 was forked from v10.1 on 2026-04-27 to walk through 183 review comments captured in `docs/reviews/v11_comments_extracted_20260427.md` and indexed at `docs/reviews/v11_comment_index.json` (`scripts/query_v11_comments.py` to query). Running log of changes: `docs/reviews/v11_running_changes_log_20260427.md`.

**Items applied as of 2026-04-27 evening (~32 of 183):**

- **Bavani structural notes B1-B10** applied (B3 Table 2.1 deferred to Aarik). §1.1 hypothesis statement rewritten to mirror terms-of-art (representational accuracy + interpretation); Pattern 1/2/3 headers promoted in §1.3; worked example Sunity Devee A2 -> F-73 / F-414 added in §2.2; §3.1 retitled "Operationalizing representational accuracy"; new Appendix G Glossary built; cross-anchor interpretation rule fully bolded in §3.7.3.
- **C1-C15** layman pass on §1.1 + §1.2: vendor recall range "68% to 85%" -> "70% to 93%"; "shown to a response model" -> "...the language model being asked to respond"; aggregation rule expanded; "win rate" -> "per-question improvement rate" globally; H5 reframed to credit fact extraction; rubric-cross-anchor framing prefigured with the 1.8 -> 2.4 example; Tier 2 layman motivation added.
- **C16-C52** wholesale: §1.3 v5 lede "Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it"; bulleted highlights (gradient / category-shift / compression / content-specificity / memory-system layering / hedging); per-system anchor-crossing range (20-36%) folded into Memory-system layering. §1.4 retitled "What this implies"; "Why the gradient matters" framing dropped; population-of-relevance pivoted to "anyone who uses an AI system" / "broad technology like email or cell phones" / 99%-of-real-AI-users-are-frontier-low-baseline observation. "What we did not prove" disclaimer paragraph removed.
- **C56 / C57:** §2 reordered. §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1; final order §2.1 -> §2.2 Memory systems for LLM agents -> §2.3 Traceability -> §2.4 Cognitive and representational foundations -> §2.5 LLM-as-judge.
- **C66 / C71:** §3 reorder. §3.6 weakest-model rationale compressed to two sentences. §3.7 subsection order is now §3.7.1 Judge panel -> §3.7.2 Fractional score interpretation (was §3.7.3) -> §3.7.3 Calibration (was §3.7.2) -> §3.7.4 Inter-judge agreement -> §3.7.5 Aggregation -> §3.7.6 Rubric-handling.
- **C99 / C124:** §4 restructure. §4.1.1 Franklin moved to §4.6.4 (high-baseline reference under sensitivities). §4.7 closing paragraph added bridging into §5.
- **C139 / C140 / C153 (load-bearing reframe):** "Additivity" replaced with "interaction with retrieval" throughout §1.3 / §4.4 / §5.2 / §5.4. The per-question Pattern 1/2/3 framing (interpretation supply / over-theorization / principled refusal) is now the load-bearing description of the spec-on-memory-systems result; aggregate Δs are characterized as small and informative only as the balance of those patterns. Supermemory deep-dive collapsed into §4.4.2 (aggregate paragraph kept in §4.4.1 with §4.4.2 pointer).
- **C162:** §1.2 conditions table C2c row long parenthetical pulled to footnote `[^c2c-construction]`.
- **Per-system anchor-crossing data (C131):** `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. Per-system upward anchor-crossing rates on the low-baseline 9: Mem0 controlled 23.4% / native 36.1%, Letta controlled 26.9% / native 19.9%, Zep controlled 27.9% / native 32.5%, Supermemory controlled 20.2% / native 23.4% (partial coverage), Base Layer controlled 29.0%. Folded into §1.3 Memory-system layering bullet and §4.4.1.

**Population-of-relevance language sweep** (consequence of §1.4 v2): "real living users" -> "the typical AI user falls into, since most users' reasoning is not in any training corpus" (§3.2.1); "real AI users" -> "typical AI users" (§5.1).

**Remaining (~150 items)** are tracked in the running log. Figure-walkthrough comments (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173) and the C171 table color-coding pass are queued pending Aarik direction.

**v11 numbers status (frozen 2026-04-28).** Headline numbers (slope, R², Wilcoxon, low-baseline mean Δ_C4a, all-14 mean Δ_C4a, wrong-spec deltas, memory-system deltas, Letta n=3 stateful-agent values) carry forward unchanged from v10.1. The 2026-04-27 reframing items are framing-level, not numerical. The 2026-04-28 data-locking pass added v11-specific findings (M15-M21 in `docs/KEY_FINDINGS.md`): per-question variance, two statistical signatures, half-anchor metric, predicate ablation null, held-out leakage rare, Hamerton spec-length confound, pattern-activation heuristic falsified. DATA_REFERENCE.md and PROVENANCE_INDEX.md mirror the 5-judge primary panel; v11 additions are registered in those files. Per-claim confidence catalog: `docs/research/v11_confidence_catalog_20260428.md`.

---

**Read this before:** any analysis, any paper edit, any new run, any data discussion.

---

## Current state (2026-04-24, v10 release-frozen — preserved as historical lineage)

**v10 was the canonical paper draft as of 2026-04-24; v10.1 superseded it on 2026-04-25; v11 is now the canonical (see top of file).** Forked from v9; release-frozen 2026-04-24 after the GPT-5.5 repo review (`docs/reviews/v10_repo_review_gpt55_20260424.md`) and the v10 release-freeze pass (closure: `docs/reviews/v10_release_freeze_pass_report.md`). Key v10 changes from v9:

- §4.1.2 author pilot removed from main body (folded back into §4 narrative; pilot data still cited in DATA_REFERENCE).
- §1.5 / §5.7 alignment fold: behavioral alignment + safety alignment merged into §1.5 framing, §5.7 carries the implication.
- Battery-composition sensitivity added as §4.1 sub-treatment: multiple regression partial slope = −0.88 [−1.13, −0.63]; drop-Hamerton subset slope = −0.89 [−1.18, −0.61]. (All 14 main-study batteries are Haiku-generated; the subset regression isolates Hamerton's legacy battery, not a generator family. The legacy "GPT-5.4-battery subset" wording was incorrect; corrected in v10.1 release-freeze pass 3.) Reproducibility script `scripts/_v10_battery_sensitivity.py`; report `docs/research/v10_battery_sensitivity_analysis.md`.
- Coupling-free reframing added: level regression C4a ~ C5 slope = +0.04 [−0.25, +0.33], R² = 0.008, mean C4a = 2.46. Permutation null centered at −0.998. Honest reframing: roughly constant C4a ceiling under spec, not heterogeneous treatment effects across baseline strata. Reproducibility script `scripts/_v10_coupling_sensitivity.py`; report `docs/research/v10_coupling_sensitivity_analysis.md`.
- §4.5 Letta stateful-agent demoted to exploratory case study with explicit n=3 scope (Hamerton + Ebers + Babur). Architectural-convergence framing retained; primary-result framing removed.
- References / Bibliography appended.
- Spearman ρ corrected from `0.89-0.98` (4-judge Hamerton historical) to `0.86-0.93` (5-judge primary, 10 pairs).
- Headline numbers (5-judge primary): slope **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001; Wilcoxon W=11, p=0.007 (C5 vs C4a); low-baseline mean Δ_C4a = +0.89; all-14 mean Δ_C4a = +0.55.

Reproducibility infrastructure added in this pass: `requirements.txt` and `REPRODUCE.md` at repo root.

---

## Current state (2026-04-23, S114 v9 revision — preserved for reference)

**Session focus:** process all 233 Word-annotations from author on v8; produce v9 with structural + data updates.

**v9 location:** `docs/versions/_pre_v11_drafts/beyond_recall_v9_draft.md` (archived 2026-04-28; v8 also preserved at `docs/versions/_pre_v11_drafts/`).

**§4 restructured per cross-LLM consensus** (Mistral + Gemini Pro; synthesis at `docs/reviews/s114_section4_structure_review.md`):
- §4.4 absorbed former §4.6 content → §4.4.1 Aggregate Performance, §4.4.2 Common Mechanisms, §4.4.3 Keckley Q21 case study
- §4.5 = Letta Stateful-Agent (was §4.7)
- §4.6 = Robustness (was §4.5)
- §4.8 Scaling content moved out of Results into §5.5

**§5 rebuilt:**
- NEW §5.1 The Anti-Pattern
- Old §5.2 Recall/prediction/persona → moved up to new §2.3.1
- NEW §5.5 Practical Implications (was §4.8 content)
- §5.7 Behavioral Alignment and Safety Alignment (was top-level §7)

**Full appendices A-E built** (581 lines, 6 `[pending]` placeholders): Predicate Vocabulary (46 predicates), Question Batteries, Conditions/Models/Memory Systems, Validity Audit, Benchmark Scope.

**Post-restructure section-reference audit complete:** 48 stale §N references fixed across the body.

**Em-dash sweep complete:** 57 em-dashes restructured + 28 en-dashes to hyphens (verbatim-quoted em-dashes preserved in italic quotes and code blocks).

**Fact corrections applied:**
- Spearman ρ: `0.89-0.98` → `0.86-0.93` (stats recompute; `0.89-0.98` does not reproduce)
- "batteries generated by Sonnet" → "Claude Haiku 4.5" (verified in battery_v2.json metadata for all 13 globals)
- "honesty axioms" → "epistemic-integrity axioms" (bernal_diaz + seacole specs contain zero; language corrected)
- Spearman range + Krippendorff α ordinal (0.659 5-judge / 0.535 7-judge) verified by stats agent; interval α is a separate statistic the paper doesn't need to cite

**Phase 1 data jobs completed tonight:**
- P0-2 Supermemory paid-tier rerun: 4 subjects (bernal_diaz, babur, cellini, rousseau) × 199/199 chunks, 0 errors; 7-judge panel (~2,184 calls) completed — aggregate computation pending
- P0-6 author derangement on Franklin battery: random (Seacole) Δ +1.16, max-distance (Babur) Δ +1.32, Franklin (shared-anchor) Δ +1.56, correct spec Δ +1.84 — **zero downward crossings across all 120 wrong-spec responses** (H6 holds robustly). §4.1.2 updated.
- P0-4 spec-activation trace, P0-5 refusal audit, P0-7 spec-similarity, P0-15 question-category audit, P0-16 rubric-sensitivity (engagement-conditional Δ), P0-17 judge floor-test all done
- Q32 era/modernity/exoticism cross-slice: era + modernity collinear with C5 baseline (not findings); **Western-tradition vs non-Western shows +0.15 to +0.25 residualized gap favoring Western-tradition** across 4/5 memory systems (n=4 vs 10, flagged as §8.2 follow-up hypothesis)
- Q47 refusal-intent classifier: 75 of 81 refusals are routine behavioral-prediction (not morally loaded); **spec is a general-purpose conservatism dial, not a targeted moral-integrity mechanism**. Zitkala-Sa Q18 is a false-premise battery outlier (flagged in §3.4).

**Mistake made + recovered:** Early in the session, the editor (Claude) propagated a flawed prior-session research-doc claim that §4.1 used a simpler Haiku-generated spec (`spec.md`) instead of the 4-layer `spec_production.md`. Built a "Hamerton unified rerun" on this premise. When the author pushed back, verified against `run_global_rerun.py:283-285` and confirmed all 14 §4.1 subjects use the full 4-layer spec. The rerun artifacts were wiped from the repo. Lesson captured in `memory_system/docs/analysis/CLAUDE-ANALYSIS.md`.

**Figure v2 rebuilds ready for author review** (not yet swapped into paper): `scripts/generate_fig_*_v2.py` + `figures/*_v2.png` for 4.1, 4.2, 4.2.1, 5, 7. Figure 9 → appendix, Figure 11 → drop.

**Spend tonight:** ~$25 committed across reruns + analyses + judges. Well inside the $30-50 projected Phase 1 budget.

**Remaining work:** complete Part A sweeps (A1 layman-ize stats, A3 anchor-crossing framing, A10 section refs, A11 cited-work examples); Part F ~100 wording-level annotations; figure v2 swap-in (pending approval); appendix `[pending]` items (rendering only, no new research); abstract last.

---

## Current state (2026-04-23, v8 final session close — preserved for reference)

- **Paper body complete through §8.** Working draft: `docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.md` (archived 2026-04-28; ~1700 lines).
- **Word doc regenerated** at `docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.docx` (archived 2026-04-28; 2.15 MB, 11 figures embedded, auto-TOC, 32 tables).
- **Abstract pending** — to be written last, after author read-through completes.
- **All collective gate-review consensus fixes applied.** 5 providers (Mistral + Cerebras + Groq + GPT-5.4 + Claude Opus) converged on READY WITH MINOR FIXES; all critical consensus items applied.
- **Title locked:** "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization."
- **Locked sections:** §1 (all), §2 (all), §3 (through §3.7.6), §4.1 through §4.8, §5.1 through §5.6, §6.1 through §6.4, §7 Behavioral alignment and safety alignment, §8.1 through §8.6 Future Work.
- **Primary judge panel:** 5-judge non-Gemini (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). All backfills complete.
- **Wrong-spec label correction** applied paper-wide + 9 support docs.
- **All 14 figures publication-ready** — colorblind palette, paper-scale typography, caption mismatches resolved, label collisions fixed. `figures/fig_4_1_gradient_scatter` + `figures/fig2_compression_curve` both passed vision spot-check on 2026-04-23 after a label-placement fix.
- **BaseLayer (memory_system) optimization pass complete.** README leads with Twin-2K, 5-step pipeline aligned across all docs + CLI + config, "No black box" softened to "Auditability, Not Black-Box Claims" section, positioning merged as one-product-at-different-scales, pyproject.toml cleaned (version bumped 0.1.0 → 0.1.1), methodology doc at `memory_system/docs/eval/methodology.md`, TECH_DEBT.md tracker created.
- **Primary handoff artifact:** `docs/reviews/session_close_handoff_v8_complete.md` — read this first when resuming.
- **Tech debt tracker:** `memory_system/TECH_DEBT.md` — all deferred code-level and repo-hygiene work, P0/P1/P2/P3 tiered.
- **Hygiene moves applied:** 13 historical drafts to `docs/versions/`, 29 review artifacts to `docs/reviews/_archive/`, 4 LaTeX intermediates to `docs/versions/_latex_test_artifacts/`, 3 README.md files rewritten, PROVENANCE_INDEX S115 addendum added for v8-only claims.

---

## STUDY-CRITICAL CONSTANTS

- **N = 14 subjects** (13 global subjects + Hamerton). Public-domain autobiographies, all pre-1940. Franklin is a known-figure control, not in the main N=14 gradient.
- **Battery: 39-40 behavioral-prediction questions per subject** (varies slightly per subject; Franklin=40, Hamerton=39, most globals=39)
- **Total behavioral-prediction pool:** 586 questions across 15 subjects (14 main + Franklin)
- **Leakage audit:** 2 of 586 questions have held-out n-gram leakage (0.34%), both in Franklin legacy battery (Q49, Q56). 14 main-study subjects: 0.00%.
- **Primary judge panel (5):** Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4
- **Sensitivity judges (2):** Gemini 2.5 Flash, Gemini 2.5 Pro
- **Gemini Pro coverage caveat:** only covers Hamerton (harmonized for C5/C4), Augustine, Babur, Bernal Diaz for main conditions. The "7-judge" label in S113 outputs was "all available judges per subject" not a uniform 7-judge panel.
- **Extraction vocabulary:** 46 behavioral predicates (not 47; config.py:607 comment is stale)
- **Embedding model:** `all-MiniLM-L6-v2` (note the `all-` prefix)

---

## PRIMARY JUDGE PANEL DECISION (S114)

5-judge non-Gemini is the primary aggregate for §4. 7-judge is the sensitivity check.

**Why:**
- Gemini Pro fails verbatim-match calibration (4.15 where every other calibrated judge scores 5.00).
- Gemini Pro penalizes padded-correct responses severely (5.00 → 1.20).
- Gemini inflation adds roughly +0.22 to per-subject Δ on average; leaves rank order stable but shifts magnitudes.
- Including known-unreliable instruments in the primary aggregate was not defensible.

**How it's reported:**
- §4 headline numbers are 5-judge primary.
- Where Gemini inclusion materially changes a number, paper reports both the 5-judge and the 7-judge values, with the delta called out.
- Calibration data is published raw; readers can apply their own normalization.

**Spec: §3.7.2** in v8 contains the full reasoning.

---

## ANALYSIS PLAN LOCK (immutable, pre-registered)

`docs/ANALYSIS_PLAN_LOCK.md` was committed before final analysis runs. Critical commitments:

- **Gradient is reported as a continuous relationship.** Linear regression (slope + 95% CI + R² + p-value). Do not introduce post-hoc thresholds for primary results. The "C5 ≤ 2.0 / 9 of 9" framing is a sensitivity analysis, not the headline.
- **Locked aggregation rule:** within each judge, mean across questions for each (subject, condition) cell; mean across judges (5 primary; 7-judge sensitivity); unit of inference is subject. Do not change.
- **Wilcoxon signed-rank** is the primary inference test, not t-tests.
- **Bootstrap 95% CIs** on memory-system deltas; do not substitute parametric CIs without re-running analysis.
- **Wrong-spec v2 (random derangement seed=42)** is reported in main results. v1 (fixed derangement, designed for cultural/temporal distance; mapping in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING) is mentioned as a prior iteration but not the primary control. Hamerton's separate Franklin-for-all comparison (from `run_full_study.py`) is reported in §4.1.1 and is distinct from the v1 global-subject control.

---

## CONDITION NAMING (memorize these)

- **C5_baseline** — no memory, no spec; pretraining baseline
- **C2a_full_spec** — Base Layer full-stack spec served as context, no facts retrieval
- **C2c_wrong_spec** — wrong-spec control (v2 random derangement is the reported version)
- **C4_factdump** — all extracted facts in context, no spec
- **C4a_full_facts_plus_spec** — all facts + spec
- **C8_raw_corpus** — raw training corpus in context, no spec
- **C9_raw_corpus_plus_spec** — raw training corpus + spec
- **C1_<system>** — memory system retrieval only (e.g., C1_mem0, C1_zep, C1_baselayer)
- **C3_<system>** — memory system retrieval + spec (e.g., C3_letta, C3_supermemory)
- **`_fullpipeline` or `_fp`** = native configuration (system's own ingestion); absence = controlled (identical fact pool)
- **Letta stateful-agent path** — architecturally separate from C1/C3 archival path; reported in §4.3.1 / §4.7 as architectural convergence, not a top-line condition row

### Paper-wide gloss convention

Every condition gets an inline gloss on first mention per section: "C5 (baseline, no context)", "C2a (spec only)", etc. Plain identifier after. Task #27 tracks the sweep.

---

## DATA INTEGRITY — VERIFIED CHECKS

- **Train/test split is honored for all stateful-agent test subjects.**
  - Hamerton: 0/39 held-out passages appear in training. CLEAN.
  - Ebers: 0/40 held-out passages appear in training. CLEAN.
  - Babur: 1/40 (Q26) — 52-character fragment appears once in training due to corpus-internal repetition. Not test-set leakage.
- **No held-out passage was ever fed to a response model.** Held-out passages go ONLY to judges.
- **Letta stateful-agent test was fed `training.txt` only.** Verified by inspection of the pipeline under `docs/research/_letta_rerun/` (`20_run_c2a_named.py`, `40_judge_responses.py`, etc.).
- **Specs are anonymized.** Zero subject-name instances across the 13 global spec files. Wrong-spec detection rate (60.6%) is content-grounded, not name-based. KEY_FINDINGS F9 is closed.
- **Full data audit 2026-04-21:** see `docs/reviews/s114_full_data_audit.md` for the comprehensive file-by-file review.

---

## ARCHITECTURAL FRAMING (load-bearing — do not collapse)

- **Base Layer is NOT a memory provider.** It is a behavioral-specification layer that layers on top of any memory system. The MiniLM + ChromaDB substrate is a zero-cost local retrieval floor, not a competitive memory product.
- **Base Layer does NOT outperform memory providers in general.** BL retrieval is comparable, not superior. BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias).
- **Flagship sentence (use verbatim or close paraphrase):** "Base Layer is not a memory system. Layered on top of four commercial ones (Mem0, Letta, Zep, Supermemory), it produces a net-positive aggregate lift on three of four (Mem0, Letta, Zep) on the users the model doesn't already know; Supermemory's aggregate is near-zero (small positive +0.04, bimodal at the per-question level)."
- **Paper §1.1 framing:** "Recall Is Not Interpretation. Interpretation Can Be Measured." Use "interpretation" not "understanding".
- **Low-baseline is the population of interest.** Nearly every real AI user has negligible pretraining representation of their personal behavior. The low-baseline slice is operationally relevant.
- **Specification effect is a claim about steering, not a claim about a new prediction capability.** §3.7.4 develops this; §4 applies it.

---

## KEY NUMBERS — 5-judge primary canonical (S114 close)

These are the final §4-bound numbers on 5-judge primary, with Hamerton and Franklin backfilled and the full parse-failure rerun applied. The S113 7-judge numbers below are retained as sensitivity.

### §4.1 Gradient (N=14, 5-judge primary)
- Regression slope: **−0.96** [95% CI −1.24, −0.67]
- R²: **0.82**
- Slope p-value: **< 0.001** (0.000009)
- Wilcoxon signed-rank C5 vs C4a: **W=11, p=0.007**
- Wilcoxon signed-rank C5 vs C2a: **W=10, p=0.005**
- Subjects positive on Δ_C4a: **12 of 14**
- Low-baseline (C5 ≤ 2.0): **9 of 9 positive**, mean Δ_C4a = **+0.89**
- Per-response anchor-crossing rate (low-baseline, 351 responses): **55.0% upward**
- Franklin high-baseline reference: C5 = 3.77, C2a = 3.37, C4a = 3.65

### §4.1.2 Living-user pilot (author, clean methodology, N=40)
- C5 baseline: **1.03** (study-low, consistent with H1/H2)
- C2a spec: 2.86, Δ +1.84
- C2c wrong-spec (Franklin): 2.59, Δ +1.56
- C4 facts: 2.93, Δ +1.90
- **C4a facts + spec: 3.02, Δ +2.00 — study's largest lift**
- Anchor-crossing rate: **75.0%**, zero downward

### §4.2 Compression (low-baseline slice, 9 subjects)
- Mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50
- Mean C8 − C2a gap: **+0.22** (corpus edges spec but by small margin)
- Compression ratio range: **5× (Hamerton) to 78× (Babur)**

### §4.2.1 Question-improvement rate (low-baseline, 351 questions)
- Spec-only win rate vs baseline: **70.9%**
- Facts-only: 72.9%
- Raw corpus: 78.3%
- Facts + spec: 78.6%
- **Median Δ when improved: +1.00** (one full anchor category)
- Median Δ when worsened: −0.40

### §3.7.6 Rubric-handling audit
- 82.8% of abstention-pattern responses scored in 1.0-1.5 (clean)
- 9.4% scored ≥ 2.0 (inflated)
- Length-score correlation: r = **0.604** on C5 baseline only; near zero elsewhere
- Per-judge strictness on abstentions: Sonnet 1.14 (strictest), Opus 1.41 (most lenient)

### §4.3 Spec-activation (ready for next session)
- Correct spec tag citation rate: **78.6%** of responses cite ≥1 spec tag
- Wrong spec tag citation rate: **50.0%** (partial content filtering)
- Data at `docs/research/spec_activation_analysis.json`
- Three mechanism types (from collective review): identity disambiguation, directional correction, interpretive inference

### §4.3 Wrong-spec controls (13 globals with complete coverage, Δ vs C5)
- C2a (correct spec): **+0.35**
- C2c v2 (random derangement, seed=42): **+0.15** (updated 2026-04-25 release-freeze pass 2; was +0.22 before the locked 5-judge primary aggregation; cascade applied across §1.3, §4.3, §4.6.2, §5 summary). Wrong-spec denominator: 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers).
- C2c v1 (fixed derangement, cultural/temporal distance): **−0.25**
- Correct-vs-adversarial gap: **0.60 points** on the 1-5 rubric
- Source: v10 §4.3 line 901

### §4.4 Memory-system spec deltas (5-judge primary, v10 §4.4)
- Controlled, all 14: Mem0 +0.12, Letta archival +0.20, Zep +0.19, Supermemory −0.05, Base Layer +0.08
- Controlled, low-baseline (n=9): Mem0 +0.10, Letta archival +0.17, Zep +0.17, Supermemory −0.01, Base Layer +0.08
- Native, all 14: Mem0 +0.33, Letta archival −0.02, Zep +0.33, Supermemory −0.01 (paid-tier rerun n=14)
- Native, low-baseline: Mem0 +0.32, Letta archival −0.04, Zep +0.30, Supermemory −0.03
- Wilcoxon C1 vs C3 within system (low-baseline): Zep controlled p=0.0004, Letta controlled p=0.0017, Zep native p=0.0015, Mem0 native p=0.0088 (all robust at α=0.01)
- Source: v10 §4.4 line 1048

### §4.5 Letta stateful-agent (5-judge primary, n=3 exploratory, v10 §4.5)
- Letta block → Haiku vs BL unified brief → Haiku
- Hamerton: 3.10 vs 2.96, **Δ +0.14**
- Ebers: 2.76 vs 1.72, **Δ +1.05**
- Babur: 2.42 vs 1.88, **Δ +0.54**
- Full-stack BL rerun preserves direction: Δ +0.27 / +1.21 / +0.38
- Babur block saturated at 335,349 chars (HTTP 400 from ~332,585); 25.4% verbatim sentence duplication at the ceiling
- Source: v10 §4.5 line 2426; raw at `docs/research/_letta_rerun/5judge_primary_results.json`

---

## KEY NUMBERS — LEGACY (S113 7-judge mixed; sensitivity values)

These are the S113 7-judge mixed-panel aggregates retained as sensitivity values. v10 promotes the 5-judge primary panel (above) to canonical; treat the values below as the secondary panel for sensitivity comparisons only.

- **Wilcoxon C5 vs C4a (7-judge):** W = 9.0, p = 0.0063 (N=14)
- **Wilcoxon C5 vs C2a (7-judge):** W = 10.0, p = 0.0076
- **Regression slope (Δ vs C5, 7-judge):** −0.98 [95% CI −1.30, −0.74], R² ≈ 0.82, p < 0.001
- **Krippendorff α:** 0.535 (all 7 judges) / 0.659 (5 primary judges)
- **Pairwise Spearman ρ:** 0.89 – 0.98 across 21 judge pairs
- **All-14 mean Δ_facts+spec (7-judge):** +0.67
- **Low-baseline (C5 ≤ 2.0) mean Δ_facts+spec (7-judge):** +1.04 (sensitivity slice, not headline)
- **Letta stateful matched-model comparison (Haiku + block as context):**
  - Hamerton: 3.24 vs BL C2a 3.04, Δ +0.20
  - Ebers: 3.00 vs BL C2a 2.25, Δ +0.75 (corrected from earlier +1.21 after battery-mismatch + anonymization fix)
  - Babur: 2.73 vs BL C2a 2.44, Δ +0.29 (corrected from earlier +0.57)
- **Memory-system aggregate spec deltas (controlled, 7-judge):** Mem0 +0.15, Letta +0.25, Zep +0.22, Supermemory −0.04, Base Layer +0.12
- **Retrieval disagreement (controlled, all-3 disagreement):** 93.4% top-1, 83.3% top-3, 73.8% top-5, 53.2% top-10 (n=515 questions)
- **Retrieval disagreement (native):** 100% at every top-k (n=410)
- **Letta block duplication at scale:** Hamerton 0%, Ebers 0%, Babur 25.4%
- **Wrong-spec v2 aggregate Δ:** +0.28 (near-baseline; correct-spec at +0.53)
- **Wrong-spec detection rate (content-grounded):** 60.6% of 587 responses explicitly flagged the mismatch
- **Aarik internal pilot (S114, 5-judge primary, N=10):** C5 = 1.86, C2a = 2.14, Δ = +0.28

### 5-judge primary canonical (v10 release-frozen, 2026-04-24)

Task #31 closed; the 5-judge primary recompute is now canonical and is reflected in the "KEY NUMBERS — 5-judge primary canonical" section above. The 7-judge mixed panel (above) is the sensitivity layer. v10 §4 reports 5-judge primary headline numbers throughout, with 7-judge sensitivity called out where Gemini inclusion materially changes a magnitude.

---

## MEMORY-SYSTEM CHARACTER (one line each)

- **Mem0** — most reliable baseline; positive in both configs (+0.15 ctrl / +0.38 native); no surprises.
- **Letta** — architecturally most ambitious; native archival path null; stateful-agent path matches BL spec at small/medium scale; collapses at large scale (HTTP 400 from ~332,585 chars, final block 335,349 chars on Babur).
- **Zep** — strongest aggregate spec delta and most consistent (9/9 low-baseline native positive); temporal graph layers cleanly under spec.
- **Supermemory** — strongest standalone retrieval (C1 mean ~2.65); near-zero aggregate spec delta due to mixture pattern (per-question swings roughly cancel); free tier limited ingestion for 4/14 subjects.
- **Base Layer** — open-source spec layer + zero-cost local retrieval floor; not a memory provider.

---

## METHODOLOGY GOTCHAS — DO NOT REPEAT

- **All 14 main-study batteries are Haiku-generated.** Hamerton + 13 globals. The legacy "13 globals = GPT-5.4 batteries" framing is WRONG. The drop-Hamerton subset regression in `_v10_battery_sensitivity.py` isolates Hamerton's legacy battery, not a generator family. GPT-5.4-regenerated batteries exist only as a circularity control (§3.4.1) and as the Tier 2 cross-provider battery family.
- **Tier 2 cross-provider response models = 2, not 4.** Sonnet 4.6 and Gemini 2.5 Pro are the response models. Opus 4.6 and GPT-5.4 in Tier 2 are judges, not response models.
- **§4.6.1 Tier 2 magnitudes are demoted to direction-only.** 5 of 6 cells reproduce direction across the 3 subjects probed (Hamerton, Babur, Augustine). Magnitudes are not reproducible across aggregations; do not cite specific deltas.
- **§4.4.2 Table 4.6 is on strict 5-judge primary panel.** Entire table; Letta/Hamerton drops to n=38 from coverage filter. No sign flips from earlier panel definitions.
- **§4.3 wrong-spec denominator:** 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). Don't conflate.
- **Brief-only vs full-stack spec confusion (S110 → S113, resolved).** Always load the full 5-layer stack: anchors + core + predictions + brief. Paths: `data/<subject>/spec/` or `data/global_subjects/<subject>/`.
- **Race conditions on parallel pipeline runs.** Background scripts kept writing to target paths after backups. Kill old processes (do not just rename); delete files before relaunch; confirm prior subprocesses completed.
- **GPT-5.4 model ID.** Use `gpt-5.4` (dot), not `gpt-5-4` (dash).
- **OpenAI GPT-5.x family rejects `max_tokens`. Use `max_completion_tokens`.** GPT-5.x and the o1/o3 reasoning families reject the legacy `max_tokens` parameter with HTTP 400. The fix is the new parameter name. Never hand-roll an OpenAI judge call. The shared judge-call utility at `scripts/_judge_invocation/openai_judge_call.py` selects the correct parameter automatically based on the model id; route every judge call through it via `from _judge_invocation import call_judge`. Every large-batch (>50 calls) judging job MUST first run `scripts/_v11_validation/preflight_judge_health.py`. Every emit script aggregating judgments MUST run `scripts/_v11_validation/check_panel_completeness.py` to fail loudly on >5% panel-coverage gaps. Closure: `docs/reviews/v11_judge_call_controls_implementation_20260425.md`.
- **Letta archival vs stateful-agent paths are fundamentally different.** "Letta native" tested in §4.4.1 (was §4.3) is the archival-retrieval path (source attachment). The stateful-agent path (v9 §4.5) requires multi-turn conversation with self-editing (`core_memory_append/replace`). Scripts: the numbered pipeline under `docs/research/_letta_rerun/` (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, etc.).
- **Data contamination check is not optional.** Before reporting any matched-model score, verify training.txt does not contain held-out passages.
- **5-judge primary, not 7-judge.** Primary aggregate excludes the Gemini pair. Sensitivity aggregate includes them. Do not revert to 7-judge primary without re-reading §3.7.2.
- **Scripts reference path mismatch (S114 fix).** Earlier §3.6 draft referenced non-existent `scripts/run_condition.py`; actual runners are `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, `scripts/run_multimodel_responses.py`.

---

## KNOWN OPEN ITEMS (S114)

- Paper-wide recompute: §4 numbers on 5-judge primary (task #31)
- Paper-wide sweep: §1 and §2 prose to align with 5-judge primary numbers (task #32)
- Paper-wide condition-identifier gloss sweep (task #27)
- Paper-wide units consistency sweep — chars / words / tokens (task #30)
- Appendix C authoring: extended experimental conditions (task #26)
- Appendix D authoring: per-subject breakdown (task #29)
- Appendix E authoring: extended benchmark analysis (task #16)
- Figure: per-subject judge-agreement visualization (task #28)
- Letta stateful-agent generalization across all 14 subjects (currently n=3 with scaling ceiling)
- Living-user replication (structural extrapolation)
- Component ablation of the spec (anchors vs core vs predictions)
- Human-judge validation on a subset (§8 Future Work)
- 47 → 46 predicate count sweep in §5.1 and §6 (task #25)

---

## REVIEW HISTORY

- Round 1: Mistral Large + Cerebras Qwen3 235B (2026-04-14)
- Round 2: 4 free providers (Gemini Pro, Mistral Large, Cerebras Qwen3, Groq) (2026-04-18)
- Collective consultations: positioning + takeaway + data-first review across Aarik's curated specs
- S114 §4 structure review: Gemini Flash, Gemini Pro, Mistral Large, Cerebras Qwen3 (2026-04-21). Converged on 7-8 section narrative spine for §4. Report at `docs/reviews/_archive/s114_section4_planning_20260421_134857.md`.
- Full data audit: 2026-04-21 (task #33). Report at `docs/reviews/s114_full_data_audit.md`.

---

## LAUNCH CONTEXT

- Launch target was Tuesday 2026-04-21 pre-review; shifted to post-§4 through §8 review and final sweep.
- Paper draft: `docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.md` (archived 2026-04-28)
- Public repo: this repo, Apache 2.0
- Author: Aarik Gulaya, Base Layer (one-person operation, non-PhD, unfunded)
- Phase 1 launch: blog + Reddit + founder emails (no arXiv required)
- Phase 2 launch: HN + researcher emails (after arXiv submission and endorsement)

---

## VOICE / FRAMING DISCIPLINE

- Direct declaratives, parallel structure.
- "Interpretation" not "understanding" in the paper context.
- Continuous gradient (slope) is the headline; the low-baseline slice is sensitivity.
- Lead with what the data supports; do not lead with what BL "beats".
- Acknowledge limitations upfront (N=14, known subjects, Anthropic-family pipeline, LLM-as-judge, non-uniform judge coverage for Hamerton until backfill); these are credibility assets.
- Position Base Layer as the *referee* who introduced a new axis, not a competitor on the existing axis.
- **No em-dashes in prose.** Restructure sentences; do not substitute hyphens.
- **No GTM / marketing verbs.** "beats", "crushes", "dominates" are out; prefer "exceeds", "outperforms".
- "Recall is not interpretation. Interpretation can be measured." is the 8-word collapse — use as social-media hook, not as the paper's load-bearing sentence.
- "Raw data available at..." convention for every experimental mention in the paper prose.

---

## HAMERTON DATA NOTE (S114)

Hamerton's spec-condition judgments (C2a, C2c, C3_mem0, C3_supermemory, C4a) were originally scored by Haiku + Gemini Flash + GPT-5.4 + Gemini Pro only — Sonnet, Opus, and GPT-4o were not in the original judge panel for Hamerton's gradient conditions. This created a non-uniform 5-judge primary panel when compared to the 13 globals.

S114 ran a Sonnet + Opus + GPT-4o backfill on Hamerton's spec-condition responses (`scripts/judge_hamerton_5judge.py`). Output files: `results/hamerton/{sonnet,opus,gpt4o}_judgments.json`. With the backfill in place, Hamerton's 5-judge primary panel is complete and matches the 13 globals.
