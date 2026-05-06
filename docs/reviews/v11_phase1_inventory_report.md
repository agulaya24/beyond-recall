# V11 Phase 1: Paper Numbers Inventory and Phase 2 Build Plan

**Source paper:** `docs/beyond_recall_v10_1_draft.md` (release-frozen 2026-04-24)
**Cross-checked against:** `docs/reviews/v10_numerical_verification_report.md`
**Inventory CSV:** `docs/research/v11_paper_numbers_inventory.csv`
**Generated:** 2026-04-25

## 1. Why this exists

V10 release is blocked on the architectural rule that every reported number must be producible from a canonical, idempotent scaffold script that reads primary data only. This Phase 1 deliverable inventories every numeric claim in v10, locates each to either an existing canonical scaffold or to a documentation artifact (analysis `*.md`) without a canonical recompute, and produces a Phase 2 build plan. No paper edits, no scaffold edits.

## 2. Counting

Total numbers inventoried: **339 rows** across §1 to §9 and Appendices A to F.

| Status | Count | What it means |
|---|---:|---|
| EXISTING | 172 | A canonical script reproduces the number from primary data files. |
| MISSING | 126 | The number lives in an analysis doc or per-judge JSON aggregate but no canonical scaffold reads primary data and emits it. Includes 9 INC-flagged cases where a scaffold exists but its output disagrees with the paper. |
| EXTERNAL | 35 | Cited from prior work (LongMemEval, Twin-2K, etc.). Out of Phase 2 scope. |
| EXCLUDE | 35 | Same set as EXTERNAL. |
| GAP (subset of MISSING) | 1 | The §8 "USD 350" study cost, not in any single file. |

The inventory over-includes by enumerating per-subject table cells separately (~150 rows for the §4.1 / §4.2 / D.1 / D.2 per-subject tables alone) and listing each headline both at its §1.3 occurrence and its §4 occurrence. The verification report counted 194 distinct "claims"; this inventory counts ~339 "rows" because Phase 2 needs to know which scaffold output covers each cell.

## 3. Per-section summary

| Section | Total | EXISTING | MISSING | EXTERNAL | Phase 2 priority |
|---|---:|---:|---:|---:|---|
| §1 Introduction | 51 | 28 | 21 | 2 | Mostly recaps; reduces once §4 scaffolds exist |
| §2 Prior Work | 17 | 0 | 0 | 17 | EXCLUDE |
| §3 Study Design | 32 | 13 | 19 | 0 | HIGH (calibration, agreement, Franklin) |
| §4.1 Gradient | 50 | 44 | 6 | 0 | LOW residual (mostly covered) |
| §4.2 Compression | 33 | 24 | 9 | 0 | MEDIUM (Table 4.2 mean row INC-2/7/8) |
| §4.3 Mechanism | 26 | 14 | 12 | 0 | MEDIUM (per-question examples) |
| §4.4 Memory-Systems | 60 | 0 | 60 | 0 | **HIGHEST single Phase 2 target** |
| §4.5 Letta Stateful | 14 | 0 | 14 | 0 | HIGH |
| §4.6 Robustness | 19 | 9 | 10 | 0 | HIGH (Tier 2 INC-1) |
| §5 Discussion | 9 | 6 | 3 | 0 | LOW |
| §6 Limitations | 10 | 7 | 3 | 0 | LOW |
| §7 Future Work | 2 | 0 | 2 | 0 | LOW |
| §8 Reproducibility | 1 | 0 | 1 | 0 | LOW (cost claim) |
| Appendix A | 5 | 1 | 4 | 0 | LOW |
| Appendix B | 30 | 0 | 30 | 0 | HIGH (battery audit) |
| Appendix D | 35 | 33 | 2 | 0 | LOW residual |
| Appendix E | 18 | 0 | 0 | 18 | EXCLUDE |
| Appendix F | 16 | 0 | 16 | 0 | HIGH (Letta full case study) |

## 4. Top 5 highest-priority Phase 2 build targets

### 4.1 §4.4 Memory-System Composition (60 missing)

The single largest gap. Every controlled / native Δ_spec aggregate, every per-system per-subject paired row, every per-question Supermemory swing, and every Wilcoxon p-value lives in `docs/research/memory_systems_5judge_primary.md`, `_sm_paired_5judge.json`, the four `*_c1_vs_c3_*.md` analysis docs, and `supermemory_7judge_aggregate.md`. A handful of existing scripts (`compute_memory_systems_5judge.py`, `analyze_mlz_c1_vs_c3.py`, `analyze_baselayer_c1_vs_c3.py`, `analyze_sm_c1_vs_c3.py`, `compute_supermemory_paid_tier_aggregate.py`) cover the computation but are not in the task's canonical list and do not all read directly from per-judge JSON in one consolidated entry point.

**Build:** one master script `scripts/scaffold_memory_systems.py` (~600-800 lines) reading per-judge JSON for all 14 subjects × 5 systems × {C1, C3} × {controlled, native}, computing per-subject Δ_spec, aggregating to full-N and low-baseline-9 means with subjects-improved counts, running paired Wilcoxon for every (system, configuration), and emitting (a) the §4.4.1 controlled and native tables, (b) the §4.4.2 per-subject paired distributions, (c) the §4.4.3 Keckley Q21 cross-system table, (d) the Supermemory mixture analysis (§4.4 last block).

### 4.2 §4.6.1 Tier 2 (10 numbers, 6 INC-flagged) and Appendix F Letta Stateful (16 missing)

Tier 2 has a canonical scaffold (`tier2_mechanical_recompute.py`) but its output does not reproduce the published Δ values. INC-1 in the verification report flags this as HIGH priority and unresolved. Appendix F has no canonical scaffold at all; the data lives in `_letta_rerun/5judge_primary_results.json`, `_letta_rerun/fullstack_named/RESULTS.md`, and the numbered execution chain (`20_run_c2a_named.py` through `70_compute_5judge_primary.py`).

**Build / repair:**
- Tier 2: ~50-100 lines to identify the legacy aggregation that produced the paper's +1.48/+1.07/+1.91/+1.27/+1.40/-0.55, and either recompute under it or replace with the new recompute output (paper edit out of scope).
- Letta stateful: `scripts/scaffold_letta_stateful.py` (~300-500 lines) reading per-judge JSON in `_letta_rerun/` and `_letta_rerun/fullstack_named/`, emitting the matched-rerun 5-judge primary table, the full-stack-named follow-up, the 7-judge robustness check, the block-size and verbatim-duplication metrics, and the referential-density numbers from `letta_stateful_deep_read.md`.

### 4.3 §3 Study Design and Inter-judge Agreement (19 missing)

The judge calibration table (§3.7.2), the 5-judge / 7-judge Spearman ρ ranges, the Krippendorff α values (5j 0.659 / 7j 0.535), and Franklin's legacy baseline numbers all live in `docs/research/stats_update.md` or `legacy_20260411`. None has a canonical scaffold producing them from per-judge JSON.

**Build:** `scripts/scaffold_judges_and_franklin.py` (~300-500 lines) covering (a) per-judge calibration recompute against `results/judge_calibration/`, (b) pairwise Spearman ρ on the 5-judge primary panel and the 7-judge panel, (c) Krippendorff α (ordinal) on both panels, (d) Franklin's C5/C2a/C4a/Δ values from `franklin_legacy_20260411/analysis/*_judgments.json`.

### 4.4 §4.2 Table 4.2 Mean Row (3 INC-flagged numbers)

`recompute_5judge_primary.py` produces 9-subject means of 1.55/2.23/2.35/2.45/2.44/2.59. The paper prints 1.52/2.23/2.35/2.45/2.45/2.50. INC-2/7/8 in the verification report. The C5 column is an 8-subject mean (Babur excluded), the rest are 9-subject; the C9 mean (2.50) does not match its own row sum. The `+0.68` and `+0.71` spec-lift figures in the same paragraph use two different C5 means.

**Repair:** ~30 lines extension to `recompute_5judge_primary.py` to print a single canonical mean row (recommendation: 9-subject everywhere with explicit "Babur excluded" annotation on C9 only), plus paper edits to align prose with the canonical row. Paper edits are out of Phase 2 scope but should land before v11 release.

### 4.5 Appendix B Battery Audit (30 missing)

Every per-subject category count, every axis (LITERAL / INTERPRETIVE / REFUSAL) classification, every per-axis Δ_spec mean and median, and the cross-subject correlation set (r = +0.646, -0.582, +0.321 cited in §4.1) lives in `docs/research/question_category_audit.md`. The underlying classifier (`classify_question_categories.py`) is in-tree but does not aggregate the report tables in one canonical pass.

**Build:** `scripts/scaffold_battery_audit.py` (~250-400 lines) reading `battery_v2.json` and `judgments_v2.json` per subject (plus `data/<subject>/battery.json` for Hamerton and Franklin), emitting (a) the §B.2 10×15 category matrix and column totals, (b) the §B.3 axis distribution, (c) §B.4 per-axis Δ_spec means and medians, (d) §B.5 per-subject by axis breakdowns, (e) §B.6 correlation set with explicit aggregation method. Resolves INC-9 by stating the per-question vs per-subject aggregation distinction directly in the script's emitted table.

## 5. Honest read on Phase 2 scope

**Estimated work:**
- 4 new master scaffolds (memory systems, letta stateful, judges/franklin, battery audit): ~1,750-2,200 lines of Python.
- 5 existing scripts to promote to canonical (`compute_memory_systems_5judge.py`, `compute_wrong_spec_5judge.py`, `compute_wrong_spec_per_subject.py`, the three `analyze_*_c1_vs_c3.py`, and `compute_supermemory_paid_tier_aggregate.py`): ~250-400 lines of header / integration / docstring edits and consolidation.
- 3 repair tasks (Tier 2 INC-1, Table 4.2 mean row INC-2/7/8, B.6 INC-9): ~100-200 lines of code plus separate paper edits.

**Total: roughly 2,100-2,800 lines of Python and 25-35 hours of focused work** to reach a state where every paper number resolves to a canonical scaffold or is tagged EXTERNAL.

The largest single risk is §4.4 Memory Systems. Sixty paper numbers depend on consolidating five separate analysis docs and four ad-hoc analysis scripts into one canonical entry point. The work is mechanically straightforward but high in surface area: every memory system × every configuration × every subject × every condition × every judge needs to flow through one aggregator. Underestimating this is the single thing most likely to make Phase 2 slip.

The second-largest risk is the §4.6.1 Tier 2 reconciliation. The verification report flagged this as HIGH priority unresolved, and the legacy aggregation that produced the paper's published numbers has not been identified. Two outcomes are possible: (a) someone recovers the legacy aggregation, the recompute reproduces the paper, and §4.6.1 reverts to a normal scaffold target; or (b) the legacy aggregation cannot be recovered, the recompute output replaces the published numbers, and the paper's §4.6.1 table needs editing. The CSV marks all six Tier 2 cells MISSING because neither outcome is producible from a canonical scaffold today.

## 6. Things that did not classify cleanly

- **§4.4.1 "Mem0... not significant at α = 0.05"** (INC-6) is a phrasing inconsistency, not a number. Mem0 controlled is significant at α = 0.05 on the full N=14 (W=15.0, p=0.0166); not significant on the n=9 low-baseline slice. The paper's wording is technically correct under one reading and ambiguous under another. Logged in the CSV under §4.4.1 with a notes column flag. Classified MISSING because the one-line correction is a documentation task, not a scaffold task.
- **§1.3 / §4.3 wrong-spec "lower bound" framing** (INC-5). The 60.6% number is correct; the paper says specs are anonymized so 60.6% is a lower bound on content-grounded detection, but the source analysis doc says specs are named which would invert the bound interpretation. The number is reproducible from a scaffold (`wrong_spec_detection_analysis.md`), so it is tagged doc:NEEDS-script + HIGH; the framing question is a separate edit, out of Phase 2 scope.
- **§4.2 efficiency-claim numbers** ("+0.68 on average" vs "+0.71 spec lift" in the same paragraph, INC-3). Both are computable from the scaffold; the paper uses different C5 means in adjacent paragraphs. Tagged EXISTING with INC-3 flag. The actual fix is choosing one C5 mean and updating the prose; that is a paper edit, not a scaffold problem.
- **§3.2 Franklin baselines** (3.77 5-judge, 4.10 Haiku alone). Franklin is in `franklin_legacy_20260411`, which predates the global-subject pipeline. There is no current canonical script for Franklin, and any script for Franklin would have to handle the legacy battery format separately. Tagged MISSING; the §3 scaffold (item 4.3 above) absorbs this.
- **§3.7.4 "21 judge pairs" wording** (INC-4). The 0.86-0.93 range is the 5-judge / 10-pair range, not the 7-judge / 21-pair range (which is [0.29, 0.93]). Number is correct in the scaffold; the paper's wording is wrong. Tagged HIGH for documentation, not for build.
- **§4.4.2 6-judge note** (line 1207 of paper). The per-question paired distributions in Table 4.6 use a 6-judge mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash), not the 5-judge primary. This is footnoted in the paper. The aggregate Δ values match the 5-judge primary recompute "to within rounding." Phase 2 should standardize on the 5-judge primary throughout and decide whether to update the per-question paired analyses or leave them with the footnote.

## 7. Recommended Phase 2 sequence

1. Build `scaffold_memory_systems.py` first. It is the largest single block of MISSING numbers and the most user-visible §4 finding.
2. Build `scaffold_letta_stateful.py` and reconcile §4.6.1 Tier 2 in parallel (separate concerns, both unblock §4.5 / §4.6.1).
3. Build `scaffold_judges_and_franklin.py` for §3 numbers.
4. Build `scaffold_battery_audit.py` for Appendix B.
5. Repair Table 4.2 mean row, INC-9 documentation, and the seven existing scripts that need promotion-to-canonical.
6. Add a top-level `scripts/scaffold_all.py` driver that runs every canonical scaffold idempotently and emits a single PROVENANCE_INDEX.md mapping each paper claim to its scaffold output.

After step 6, every number in the inventory CSV resolves to either a script entry point that reproduces it from primary data, an EXTERNAL citation, or an explicit GAP (the §8 cost claim is the only one).

---

*End of report.*
