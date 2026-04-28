# V11 Table Rebuild Proposal

_Generated 2026-04-25. Author-review document. The v10 paper is **not** modified by this proposal._

> **Closure note (2026-04-25 evening).** All Tier 1 + Tier 2 + Tier 3 items in this proposal have been closed during release-freeze pass 2 + pass 3. Specifically, the §4.4.2 Table 4.6 panel rebuild that this proposal flagged as Tier 3 author-decision item #6 has been applied on 2026-04-25 evening; the entire table now uses the strict 5-judge primary panel (recompute script: `scripts/_table_4_6_5judge_recompute.py`; no sign flips; Aggregate Δs shrink by 0.01 to 0.06). Closure record: `docs/reviews/v11_release_freeze_status_20260425.md` "Pass 3" subsection. Manuscript path is now `docs/beyond_recall_v10_1_draft.md`.

**Source of truth.** All scaffold values come from `docs/research/v11_emit/*.json` (regenerated 2026-04-25 17:51 UTC). The cell-level reconciliation lives at `docs/research/v11_reconciliation_diff.md` (1,509 claim_ids, 206 substantive mismatches, 14 sign flips). This proposal walks the v10 paper's tables one at a time and surfaces only the cells that change under the locked aggregation rule (5-judge primary panel `{haiku, sonnet, opus, gpt4o, gpt54}`).

**Locked aggregation rule.** Per-judge × per-question score → per-judge × per-subject mean → panel mean across the 5 judges. No fallback panels. No per-judge rounding before averaging. This rule produces the scaffold values; v10 paper text predates the lock in many places.

**Three failure modes to keep distinct.**

1. **Numeric drift.** The paper has a stale value because the underlying data has been re-aggregated. Replace.
2. **Panel-composition asymmetry.** The paper used a different (audit) panel; the scaffold uses the locked primary panel. Author chooses, not a typo "fix."
3. **Column-header rounding convention.** The paper's table column header uses a rounded shared estimate (e.g., "~7K tok"). The scaffold has per-subject values. This is a structural choice, not a number error.

Cells in the proposal are tagged with which failure mode they are.

---

## Executive summary

| Metric | Count |
|---|---:|
| Tables reviewed | 18 (across §3, §4.1, §4.1.2, §4.2, §4.2.1, §4.3, §4.4.1, §4.4.2, §4.4.3, §4.5, §4.6.1, §4.6.2, App B.2, B.3, B.4, App D.1, D.2, D.3, D.4) |
| Total scaffold-emitted cells reviewed | ~1,360 (1,509 claim_ids minus 149 NON_CLAIM scaffold-only) |
| Cells with NO_CHANGE (MATCH) | 1,089 (72.2%) |
| Cells with MINOR_ROUNDING (\|Δ\| < 0.05) | 65 (4.3%) |
| Cells with SUBSTANTIVE_CHANGE (\|Δ\| ≥ 0.05 OR sign flip) | 206 (13.7%) |
| Sign flips at the cell level (against running-list) | 14 |
| Sign flips at the cell level (against published v10 paper body) | **0** |
| Coverage gaps (paper-only with no scaffold claim) | 0 (PAPER_ONLY heuristic scan returned empty) |

**Sign flips — direct verification against v10 paper text (NOT against the reconciliation running-list, which the advisor caught as containing stale-extraction artifacts):**
- **§4.1 regression sign flips:** ZERO at the paper-text level. Paper line 749 already cites the corrected level-regression numbers ("slope +0.04, R² = 0.008, p = 0.76"). The reconciliation diff's "paper = -0.67" entries are stale running-list values, not paper-text claims. **No body-table or paper-text sign flips in §4.1.**
- **§4.3 wrong-spec per-subject sign flips:** ZERO at the paper-text level. Paper line 889-893 only shows aggregate Δ values; no per-subject c2c v1 / v2 table currently exists in v10. The 8 per-subject sign flips would only surface IF a per-subject table is added in the rebuild. **Sign flips are between scaffold and a never-published per-subject running-list.**
- **§4.4.1 Wilcoxon:** ZERO at the paper-text level. Paper line 1058 already reports "Supermemory native W = 48.0, p = 0.8077" matching scaffold. The diff's "paper = -0.01" is a stale-extraction artifact (probably "0.01" mis-OCRed as "-0.01" in the running-list).
- **§4.4.3 Keckley Q21:** ZERO at the paper-text level. Direct read of v10 line 1244-1250 confirms Mem0 +0.2, Zep +0.2 — scaffold matches. The diff's "paper = -0.50" entries are stale-running-list, not v10 cell values.

**The 14 sign flips reported by the reconciliation diff are between the scaffold and an upstream running-list extraction, NOT between the scaffold and the v10 paper body. The author-facing implication: zero published-table sign flips remain after rebuild.** The running list itself needs regeneration as a cleanup step, but no published table cell flips sign.

This finding is load-bearing for the proposal's apply-order: every "sign flip" item drops from Tier 3 (substantive author-decision) to Tier 1 (silent cleanup of running-list).

**Per-section cell counts (from reconciliation §3 walkthrough table):**

| Section | Total claims | MATCH | MINOR | SUBSTANTIVE | NON_CLAIM | Substantive % |
|---|---:|---:|---:|---:|---:|---:|
| §3 (study design) | 61 | 32 | 4 | 16 | 9 | 26.2% |
| §4.1 cross-subject gradient | 115 | 73 | 3 | 9 | 30 | 7.8% |
| §4.2 + §4.2.1 compression | 146 | 74 | 22 | 46 | 4 | 31.5% |
| §4.3 wrong-spec | 45 | 6 | 8 | 31 | 0 | 68.9% |
| §4.4.1 memory systems | 50 | 27 | 6 | 9 | 8 | 18.0% |
| §4.4.2 / §4.4.3 mechanisms | 45 | **0** | 0 | 43 | 2 | 95.6% |
| §4.5 + Appendix F Letta | 44 | 12 | 5 | 21 | 6 | 47.7% |
| Appendix B (battery) | 242 | 190 | 4 | 14 | 34 | 5.8% |
| Appendix D (validity audit) | 761 | 675 | 13 | 17 | 56 | 2.2% |

**The two highest-priority rebuild zones.**
- §4.4.2 / §4.4.3 (paired-Δ mechanism mixture tables): 0 of 45 cells match. Every one is a panel-composition asymmetry. The author needs to choose which panel governs publication.
- §4.3 wrong-spec per-subject table (does not currently exist as a v10 table; only the +0.35 / +0.15 / −0.25 aggregate appears at line 891). The 31 substantive per-subject deltas live in scaffold but have no paper home. **Coverage decision needed: add a per-subject §4.3 table, or move the per-subject data to an appendix.**

---

## Per-table proposals

### Table 1: §4.1 Cross-subject gradient (heading line 712)

**Location:** v10 line 712-731. 17 rows × 7 columns (Subject / Baseline (C5) / Spec only (C2a) / Facts + Spec (C4a) / Δ spec / Δ facts+spec / Anchor crossed).

**Body row count under each status (per the diff's per-section walkthrough):**
- Total claims to this section's tables: 115 (includes regression-summary numbers, not just per-subject rows)
- MATCH: 73, MINOR_ROUNDING: 3, SUBSTANTIVE: 9
- For the 14 per-subject score-cells in the body table specifically (Subject × C5/C2a/C4a/Δ_spec/Δ_C4a → 70 numeric cells), every per-subject score cell **MATCHES** the scaffold within rounding. **The substantive changes in §4.1 are NOT in the per-subject score table — they are in the regression-summary numbers reported in the body text around the table.**

**NO_CHANGE on 14 of 14 subject rows for the score columns** (C5, C2a, C4a, Δ_spec, Δ_C4a all confirmed against `4_1_gradient.json` and Appendix D.1's repeat). Re-verified from the v10 file lines 715-731 against scaffold.

**Substantive changes in §4.1 (regression frame, NOT score table):**

| Claim | Paper | Scaffold | |Δ| | Failure mode | Note |
|---|---:|---:|---:|---|---|
| `4_1_summary_regression_level_slope` | -0.67 | +0.04 | 0.71 | Numeric drift (+SIGN_FLIP) | Level regression C4a~C5 is essentially flat. Same finding paper already discusses at line 749 ("Honest reframing"). |
| `4_1_summary_regression_level_r_squared` | -0.67 | 0.008 | 0.68 | Numeric drift | R² near-zero confirms flat. Paper text at line 749 says "R² = 0.008" already; the placeholder -0.67 in the running list is the artifact. |
| `4_1_summary_regression_level_p` | 0.95 | 0.7633 | 0.19 | Numeric drift | |
| `4_1_summary_regression_level_ci_high` | +0.95 | +0.3253 | 0.62 | Numeric drift | |
| `4_1_summary_regression_level_ci_low` | -0.67 | -0.2447 | 0.43 | Numeric drift | |
| `4_1_summary_regression_delta_p` | -0.67 | 9.0e-06 | 0.67 | Numeric drift (+SIGN_FLIP) | Delta-regression p-value, line 1372 reports `< 0.001`. Reconcile placeholder. |
| `4_1_summary_regression_delta_r_squared` | 0.95 | 0.8177 | 0.13 | Numeric drift | Paper line 1372 says R² = 0.82, scaffold 0.8177. Paper rounds correctly; running-list placeholder is stale. |
| `4_1_summary_all14_mean_delta_C4a` | +0.89 | +0.5516 | 0.34 | Numeric drift | **CRITICAL.** Paper headline says "+0.89 mean Δ_C4a" (line 1372, line 92, line 1392). Scaffold computes mean over all 14 subjects = +0.55. The +0.89 is the **low-baseline-9 mean**, not the all-14 mean. The label in the paper is correct ("low-baseline" at line 92 and 1392); claim_id is mislabeled in scaffold. **Verify the scaffold claim_id, not the paper text.** |
| `4_1_summary_low_baseline_mean_C4a` | 2.00 | 2.4393 | 0.44 | Numeric drift | The actual low-baseline mean C4a. Paper line 794 reports "**2.45**" in the §4.2 mean row, scaffold 2.44 — within rounding. The 2.00 in the running list is the placeholder bug. |

**Recommended structural change to §4.1:** rewrite the regression-summary paragraph (lines 749, 751, 1372) to use scaffold values. The reframing prose is already correct; only the numbers inserted into it are stale.

**Methodology flag (load-bearing).** Diff §3 walkthrough notes that §4.1's per-subject body table matches scaffold cleanly. Do not rebuild the body table — only update the regression-summary numbers around it.

---

### Table 2: §4.1.2 Anchor-crossing transition table (heading line 602)

**Location:** v10 line 602-612. 9 rows × 3 columns (Transition / % of responses / Plain-language meaning).

**Verified against scaffold.** Reconciliation surfaces no cells in this transition table as substantive mismatches — `appD_2_slice_no_crossing_pct` (24% paper → 38.18% scaffold, ID **flag below**) is in Appendix D.2, not this table. The aggregate slice numbers in the body text immediately above (line 600: "55.0%", 351 questions) match scaffold (`appD_2_slice_upward_pct = 55.0`).

**NO_CHANGE on all 9 transition rows.** Apply silently as cleanup if any wording polish is needed.

**Adjacent flag:** the **Appendix D.2 slice "no crossing" denominator** is a separate table (line 2098) whose numbers are affected. Treated below in Appendix D.2 entry.

---

### Table 3: §4.2 Per-subject compression table (heading line 783)

**Location:** v10 line 783-794. 10 subject rows + 1 mean row × 10 columns (Subject / Source words / Compression ratio / C5 / C2a / C4 / C8 / C4a / C9 / C8 − C2a).

**Body row count under each status:**
- 10 subject rows × ~9 numeric cells = 90 cells; plus 1 mean row × 9 = 9 cells. ≈99 cells in the body table.
- Score columns (C5, C2a, C4, C8, C4a, C9): scaffold matches paper to within rounding on every subject; **NO_CHANGE on score columns for all 10 subjects**.
- C9 column has Babur as `-` (excluded for context window) — scaffold confirms.
- The substantive changes are concentrated in the **leftmost two columns** (Source words and Compression ratio) because §4.2 uses estimated tokens and shared rounded estimates.

**Substantive changes in §4.2 body table:**

| Subject | Column | Paper | Scaffold | |Δ| | Failure mode |
|---|---|---:|---:|---:|---|
| Hamerton | Source words (~tokens) | 25,231 (~33K) | 32,800 actual tokens; 25,231 source words is correct | 7,569 | Column-header convention. The "tokens" parenthetical is the disagreement; word count itself matches. **Decision needed:** keep "(~33K)" as a token estimate, replace with actual `32,800`, or drop the parenthetical. |
| Hamerton | Compression ratio | ~5× | 7× | 2 | Numeric drift. Paper carries the older ratio; recompute is 7×. |
| Hamerton | C2a (also referenced in §1.3 as "~7K tok" header) | "~7K tok" | per-subject `4,478` | 522 | Column-header convention. **Decision needed:** keep group estimate, or switch column to per-subject token counts. |
| Sunity Devee | Spec tokens | (column header `~7K tok`) | 6,771 | 229 | Column-header convention |
| Yung Wing | Spec tokens | header `~7K tok` | 6,657 | 343 | Column-header convention |
| Seacole | Spec tokens | header `~7K tok` | 6,787 | 213 | Column-header convention |
| Fukuzawa | Spec tokens | header `~7K tok` | 7,086 | 86 | Column-header convention |
| Babur | Spec tokens | header `~7K tok` | 6,922 | 78 | Column-header convention |
| Ebers | Spec tokens | header `~7,300 tok` (line 106) | 7,244 | 56 | Column-header convention |
| Bernal Diaz | Spec tokens | header `~7,300 tok` (line 106) | 7,349 | 49 | Column-header convention |
| Keckley | Spec tokens | header `~7K tok` | 7,014 | 14 | Column-header convention |
| Bernal Diaz | Compression ratio | 35× | 33× | 2 | Numeric drift |
| Ebers | Compression ratio | 18× | 17× | 1 | Minor drift |
| Babur | Compression ratio | 78× | 79× | 1 | Minor drift |
| Yung Wing | Compression ratio | 12× | 13× | 1 | Minor drift |
| Seacole | δ (C9 − C5) | +0.35 | +0.96 | 0.61 | Numeric drift in C9 column. Paper C9 reads 2.73, baseline 1.77 → diff +0.96 — paper number 0.35 in running list is stale |
| Keckley | δ (C9 − C5) | +0.07 | +0.65 | 0.58 | Numeric drift. Paper C9 = 2.49, C5 = 1.84 → diff +0.65. |
| Fukuzawa | δ (C9 − C5) | +1.67 | +1.11 | 0.56 | Numeric drift. Paper C9 = 2.78, C5 = 1.67 → diff +1.11. |
| Bernal Diaz | δ (C9 − C5) | +0.28 | +0.84 | 0.56 | Numeric drift. Paper C9 = 2.53, C5 = 1.70 → diff +0.83. |
| Hamerton | δ (C9 − C5) | +2.27 | +1.83 | 0.44 | Numeric drift. Paper C9 = 3.09, C5 = 1.26 → diff +1.83. |
| Yung Wing | δ (C9 − C5) | +0.20 | +0.63 | 0.43 | Numeric drift |
| Sunity Devee | δ (C9 − C5) | +1.03 | +1.44 | 0.41 | Numeric drift |
| Ebers | δ (C9 − C5) | +1.02 | +1.14 | 0.12 | Minor drift |
| Babur | (C9 excluded) | n/a | n/a | n/a | Confirmed |

**Mean row in §4.2:**
| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| Mean compression ratio | ~23× | (per-row recompute needed) | small | Recompute from above |
| C8 − C2a mean | +0.22 (line 794), +0.328 (running-list `4_2_table_mean_C8_minus_C2a`) | +0.2285 | 0.10 | Minor drift. Paper line 794 says **+0.22**; running list `+0.328` is the placeholder — replace running-list, paper text already correct. |
| Mean C9 | 2.50 (line 794) | 2.5942 (8 rows; Babur excluded) | 0.09 | Minor drift |
| Mean C9 n_rows | 9 (line 794) | 8 | 1 | Numeric correction. Babur is excluded so n=8, not 9. |

**Recommended structural change to §4.2:** decide column-header convention for spec tokens (group estimate vs. per-subject). If keeping "~7K tok" in header, add a footnote disclosing the actual per-subject range (4,478 to 7,349). If switching to per-subject, every subject row gets a corrected number. Replace compression ratios cleanly. Replace C9-minus-C5 deltas in the C9 column (these were never consistent with the C9 score values shown).

---

### Table 4: §4.2.1 Question-improvement rate tables (heading lines 813, 824, 837)

**Three sub-tables:**
- Table 4.2.1-A (line 813-818): Low-baseline 351-question per-condition win/tie/loss + median Δ. 4 condition rows × 7 columns.
- Table 4.2.1-B (line 824-829): All-14 546-question per-condition rate table. 4 condition rows × 3 columns.
- Table 4.2.1-C (line 837-840): Pairwise comparison (C8 vs. C2a, C9 vs. C4a). 2 rows × 4 columns.

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| C8 vs. C2a worse n (line 839, "115 (32.8%)") | 115 / 32.8% | 108 / 30.77% | 7 / 2.03 | Numeric drift |
| C8 vs. C2a better n (line 839, "190 (54.1%)") | 190 / 54.1% | 187 / 53.28% | 3 / 0.82 | Numeric drift |
| C8 vs. C2a tie n (line 839, "46") | 46 / "(54.1% running list)" | 56 | 1.9-10 | Number-check needed, paper table has 46 which scaffold confirms via separate cell |
| C9 vs. C4a better (line 840, "155 (49.7%)") | 155 / 49.7% | 153 / 49.04% | 2 / 0.66 | Numeric drift |
| C9 vs. C4a worse (line 840, "115 (36.9%)") | 115 / 36.9% | 114 / 36.54% | 1 / 0.36 | Minor drift |
| C9 vs. C4a tie (line 840, "42") | 42 | 45 | 3 | Numeric drift |
| Low-baseline C4 worsen pct (paper running-list field) | 9% | 14.53% | 5.53 | Numeric drift |
| Low-baseline C8 worsen pct (running-list field) | 9% | 12.25% | 3.25 | Numeric drift |
| Low-baseline C8 improve pct (running-list field) | 78.3% (matches paper line 817) | 78.63% | 0.33 | Minor — paper text correct, running-list placeholder stale |
| All-14 C8 improve pct (line 828, "64.5%") | 64.5% | 65.20% | 0.70 | Minor drift |
| All-14 C8 worsen pct (line 828, "24.5%") | 24.5% | 23.63% | 0.87 | Minor drift |

**Recommended:** Update the four pairwise-comparison cells in line 839 (115/190/46 → 108/187/56) and line 840 (155/42/115 → 153/45/114). Win-rate tables (the more visible part) shift by < 1 pp on percentages — minor cleanup only.

---

### Table 5: §4.3 Wrong-spec aggregate table (heading line 889)

**Location:** v10 line 889-893. 3 rows × 2 columns. Aggregate Δ vs. C5 for C2a, C2c v2, C2c v1.

**MATCHES on the three aggregate cells (paper +0.35 / +0.15 / −0.25 vs. scaffold values are within rounding).** No body-table changes needed.

**§4.3 substantive changes are NOT in this aggregate table — they are in 31 per-subject c2c v1 and v2 deltas that exist in the scaffold but have no v10 paper table.** This is the single largest coverage decision in the proposal.

**Per-subject wrong-spec deltas under strict 5-judge primary:**

| Subject | C2c v1 (paper, all share placeholder) | C2c v1 (scaffold) | sign_flip | C2c v2 (paper, placeholder) | C2c v2 (scaffold) | sign_flip |
|---|---:|---:|:--:|---:|---:|:--:|
| Augustine | -0.25 | -0.4718 | | +0.22 | +0.1254 | |
| Babur | -0.25 | -0.5897 | | +0.22 | +0.7560 | |
| Bernal Diaz | -0.20 | +0.0923 | **YES** | -0.20 | +0.6876 | **YES** |
| Cellini | -0.25 | -0.5641 | | -0.25 | -0.8745 | |
| Ebers | -0.25 | +0.2974 | **YES** | +1.60 | +0.7895 | |
| Equiano | -0.25 | -0.7949 | | -0.25 | -0.9992 | |
| Fukuzawa | -0.25 | +0.2615 | **YES** | +0.22 | +0.8647 | |
| Keckley | -0.25 | -0.4872 | | +0.22 | +0.1390 | |
| Rousseau | -0.25 | -0.5231 | | +0.22 | -0.3659 | **YES** |
| Seacole | -0.25 | -0.3436 | | +0.22 | -0.1044 | **YES** |
| Sunity Devee | -0.25 | +0.2667 | **YES** | +0.22 | +0.5349 | |
| Yung Wing | -0.25 | +0.3231 | **YES** | +0.22 | +0.3931 | |
| Zitkala-Sa | -0.25 | -0.6769 | | +0.22 | +0.0365 | |

**The paper's per-subject placeholders (-0.25 for v1, +0.22 for v2) appear to be aggregate fill-ins rather than per-subject computations.** The scaffold gives real per-subject numbers; eight cells flip sign from negative to positive (or vice versa).

**Other §4.3 substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| `4_3_correct_minus_adversarial_gap` | +0.35 (line 897) | +0.6008 | 0.25 | Numeric drift. Paper text says "0.60 points on the 1-5 rubric" at line 897 — scaffold confirms. The running-list placeholder of +0.35 is stale. |
| `4_3_random_derangement_delta_13globals` | +0.22 (line 1325 + body) | +0.1525 | 0.07 | Numeric drift. Paper carries +0.22 as primary across §1.3, line 892, line 1374, line 1325. Scaffold computes +0.15. **Decision needed.** |
| `4_3_wrong_spec_detection_ambiguous_pct` | 0.35% (line 924) | 0.85% | 0.50 | Numeric drift. Paper line 924 reports 0.9% rounded; scaffold computes 0.85%. Within rounding — minor. |
| `4_3_spec_tag_citation_rate_correct_numerator` | 209 | 276 | 67 | Numeric drift on the 78.6% denominator. |
| `4_3_spec_tag_citation_rate_wrong_numerator` | 146 | 156 | 10 | Numeric drift on the 50.0% denominator. |

**Recommended structural change:** add a §4.3 per-subject wrong-spec table (13 globals × 4 columns: subject, C2c v1 Δ, C2c v2 Δ, sign vs. aggregate) before the Example A/B/C narrative. Move the placeholder per-subject −0.25 / +0.22 estimates out of the running list. Update the +0.22 random-derangement aggregate to +0.15. Update tag citation counts.

**Sign-flip flag (load-bearing for §4.3 mechanism narrative).** Eight subjects' v1 wrong-spec delta signs flip. The "adversarial wrong-spec hurts" claim still holds at the aggregate (-0.25 → -0.31 unchanged direction), but at the per-subject level, four subjects (Bernal Diaz, Ebers, Fukuzawa, Sunity Devee, Yung Wing) actually had **positive** v1 deltas. The §4.3 narrative needs to be checked for any place that implies all subjects show negative v1; currently the paper avoids this by reporting only the aggregate.

---

### Table 6: §4.4.1 Aggregate memory-system tables (heading lines 1036, 1048)

**Two sub-tables:**
- Table 4.4.1-A (line 1036-1042): Controlled config. 5 system rows × 4 columns (Δ_spec all-14 / Subjects improved of 14 / Δ_spec low-9 / Subjects improved of 9).
- Table 4.4.1-B (line 1048-1054): Native config. Same shape but Base Layer is "−"/"N/A".

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| `4_4_1_supermemory_native_wilcoxon_p` | -0.01 (line 1058 typo) | 0.8077 | 0.82 | Numeric drift + sign flip. Paper line 1058 reads "Supermemory native W = 48.0, p = 0.8077" — paper text already has scaffold value. The running-list -0.01 is the bad placeholder. |
| `4_4_1_zep_controlled_wilcoxon_p` | 0.17 (placeholder) | 3.66e-04 | 0.17 | Numeric drift. Paper line 1044 reports "Zep controlled p = 0.0004" — paper text correct. Replace running-list. |
| `4_4_1_zep_native_wilcoxon_p` | 0.17 (placeholder) | 0.0015 | 0.17 | Numeric drift. Paper line 1058 says "Zep native p = 0.0015" — paper text correct. Replace running-list. |
| `4_4_1_letta_archival_native_wilcoxon_p` | 0.20 | 0.4629 | 0.26 | Numeric drift. |
| `4_4_1_mem0_native_wilcoxon_p` | 0.10 | 0.0088 | 0.09 | Numeric drift. Paper line 1058 says "Mem0 native p = 0.0088" — paper text correct. |
| `4_4_1_mem0_controlled_wilcoxon_p` | 0.10 | 0.0166 | 0.08 | Numeric drift. |
| `4_4_1_mem0_native_low_baseline_n_positive` | 9 | 7 | 2 | Numeric drift in the "Subjects improved (of 9)" column for Mem0 native row. |
| `4_4_1_letta_archival_controlled_low_baseline_n_positive` | 9 | 8 | 1 | Numeric drift in Letta controlled row's "Subjects improved (of 9)" cell. Paper currently says "8/9" at line 1039 — scaffold confirms. Running-list placeholder is "9". |
| `4_4_1_supermemory_controlled_all14_n_positive` | 6 | 7 | 1 | Numeric drift. |

**Recommended:** the body-table cells in Table 4.4.1-A and 4.4.1-B match scaffold within rounding for every Δ_spec value; the only body-table cell change is **Letta archival controlled "Subjects improved (of 9)" 9/9 → 8/9** (paper currently has "8/9", running-list is stale; verify against line 1039) and **Mem0 native "Subjects improved (of 9)" 9/9 → 7/9** (paper has 7/9 already at line 1050; verify). Wilcoxon p-values match paper text inline. **The body tables are largely already correct; the running-list placeholders in §4.4.1 are what's stale.**

---

### Table 7: §4.4.2 Per-subject paired-Δ distribution table (heading line 1196 / Table 4.6)

**Location:** v10 line 1196-1206. 8 rows (System × Subject) × 9 columns (Aggregate Δ / C1 mean / C3 mean / Wins / Losses / Large improvements / Large regressions / Total Qs).

**Per-section walkthrough: §4.4.2 / §4.4.3 has 0 of 45 cells matching.** Every claim in this section fires as MISMATCH_SUBSTANTIVE.

**Why: panel-composition asymmetry.** The reconciliation methodology note (lines 265-267) is explicit:

> §4.4.2 paired_total_n. Scaffold reports paired_total_n = 546 for the strict 5-judge primary panel across every system. The paper reports 516 (line 1084) and 507 (line 1233) in places where the panel was implicitly the audit panel rather than the locked 5-judge primary.
>
> §4.4.3 Keckley Q21 (Mem0, Zep deltas). Scaffold uses the strict 5-judge primary panel mean. The paper table presents per-judge-rounded means under a relaxed inclusion rule that flips the sign on Mem0 and Zep deltas (paper -0.50 vs scaffold +0.20). This is a primary-vs-relaxed panel asymmetry, not a numeric error in either source.

**The body table at line 1196 explicitly reports "6-judge mean" in the *Note on judge panel* paragraph at line 1209.** This table is intentionally on a different panel from the 5-judge primary. The reconciliation flags every cell as substantive but **the asymmetry is methodologically declared in the paper itself**.

**Substantive changes that ARE worth surfacing under primary-panel rebuild:**

Per-system aggregate counts (across all subjects, paired questions):

| System | Cell | Paper (audit panel) | Scaffold (primary panel) | |Δ| | Note |
|---|---|---:|---:|---:|---|
| Supermemory | Total paired n | 507 (line 1086) / 516 (line 1090) | 546 | 39 | **Primary panel includes more responses.** Audit panel dropped 30 NO_RETRIEVAL responses. |
| Supermemory | "Spec helps Δ ≥ +1.0" n | 37 (line 1091) | 57 | 20 | Primary panel has more |
| Supermemory | "Spec hurts Δ ≤ -1.0" n | 52 (line 1092) | 53 | 1 | Within rounding |
| Supermemory | "Spec helps mean swing" | +1.45 (line 1091) | +1.5474 | 0.10 | Minor drift |
| Supermemory | "Spec hurts mean swing" | -1.41 (line 1092) | -1.3811 | 0.03 | Minor drift |
| Mem0 | Total paired n (per-system) | 507 | 546 | 39 | Same primary-panel inclusion shift |
| Mem0 | "helps n" | 39 | 64 | 25 | Primary panel inclusion |
| Mem0 | "hurts n" | 39 | 45 | 6 | Primary panel inclusion |
| Zep | Total paired n | 507 | 546 | 39 | Same |
| Zep | "helps n" | 52 | 82 | 30 | Primary panel inclusion |
| Zep | "hurts n" | 24 | 30 | 6 | Primary panel inclusion |
| Letta archival | Total paired n | 507 | 545 | 38 | Same (1 fewer than other systems) |
| Letta archival | "hurts n" | 39 | 36 | 3 | Within noise |
| Base Layer | Total paired n | 507 | 546 | 39 | Same |
| Base Layer | "helps n" | 39 | 64 | 25 | Primary panel inclusion |
| Base Layer | "hurts n" | 39 | 54 | 15 | Primary panel inclusion |
| Mean swings (helps and hurts) | various | within ±0.5 | within ±0.5 | minor | Drift only |

**Recommended structural decision:** Either (a) keep the §4.4.2 body table on its declared 6-judge panel and note the discrepancy explicitly (preserving the existing line 1209 note); OR (b) rebuild the table on the 5-judge primary panel and update the n's to 546 / 545 throughout. The paper currently does (a) implicitly but with stale cell values. **Author choice — this is methodologically declared, not a typo.**

---

### Table 8: §4.4.3 Keckley Q21 cross-system table (heading line 1243)

**Location:** v10 line 1243-1249. 5 rows × 3 columns (System / Δ on Q21 / Pattern 3 visible).

**Direct verification against v10 line 1244-1250 shows the body table already matches scaffold within rounding:**

| System | Paper Δ (line 1244-1250) | Scaffold Δ | |Δ| | Status |
|---|---:|---:|---:|---|
| Supermemory | -2.0 | -2.00 | 0 | NO_CHANGE |
| Base Layer | -2.2 | -2.20 | 0 | NO_CHANGE |
| Letta archival | +0.4 | +0.40 | 0 | NO_CHANGE |
| Mem0 | +0.2 | +0.20 | 0 | NO_CHANGE |
| Zep | +0.2 | +0.20 | 0 | NO_CHANGE |

**The body table is fully aligned with the locked 5-judge primary panel.** The reconciliation diff's substantive-mismatch entries `4_4_3_keckley_q21_mem0_delta` (paper -0.50 vs scaffold +0.20), `4_4_3_keckley_q21_zep_delta` (paper -0.50 vs scaffold +0.20), and `4_4_3_keckley_q21_letta_archival_delta` (paper +1.00 vs scaffold +0.40) are flagging a **stale running-list extraction**, not the v10 paper table cell. The C1 / C3 component cells in the running-list (e.g., `4_4_3_keckley_q21_mem0_c1` paper 1.33 → scaffold 1.40) are minor arithmetic rounding differences that propagate into incorrect Δ extraction values in the running list itself.

**Recommended:** **NO BODY-TABLE CHANGES.** Apply silently as cleanup. The 12 running-list entries for §4.4.3 Keckley Q21 deltas should be regenerated from scaffold; this affects only the running list, not the published table.

**Methodology note line 266 of the reconciliation file references a "primary-vs-relaxed panel asymmetry."** That note appears to describe an earlier draft where the table did present audit-panel deltas; the current v10 line 1244-1250 already presents primary-panel values. **The asymmetry is resolved in the current paper.** No author-decision required.

---

### Table 9: §4.5 Letta stateful main table (heading line 2432)

**Location:** v10 line 2432-2436. 3 rows × 4 columns (Subject / Letta block → Haiku / BL unified brief → Haiku / Δ Letta − BL).

**Important locator-bug flag (per reconciliation note line 268):** the diff's `paper_value` cell for Ebers BL row reads `46`, but that's actually a co-mention of Babur's BL value from the paragraph at line 2466, not a value from this table. **Verify by reading line 2432-2436 directly.**

**Substantive changes (table cells):**

| Cell | Paper (line 2432) | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| Hamerton Letta block → Haiku | 3.10 | 3.21 | 0.11 | Minor drift |
| Hamerton BL unified brief → Haiku | 2.96 | 2.83 | 0.13 | Minor drift |
| Hamerton Δ | +0.14 | +0.27 | 0.13 | Minor drift, follows |
| Ebers Letta block → Haiku | 2.76 | 2.76 | 0 | NO_CHANGE |
| Ebers BL unified brief → Haiku | 1.72 | 1.72 | 0 | NO_CHANGE |
| Ebers Δ | +1.05 | +1.21 | 0.16 | Minor drift |
| Babur Letta block → Haiku | 2.42 | 2.67 | 0.25 | Minor drift |
| Babur BL unified brief → Haiku | 1.88 | 2.04 | 0.15 | Minor drift |
| Babur Δ | +0.54 | +0.38 | 0.16 | Minor drift |

**Substantive changes (referenced in body text but NOT in the table itself):**

| Cell | Paper | Scaffold | |Δ| | Failure mode | Note |
|---|---:|---:|---:|---|---|
| Ebers BL named-entity count (line 2466 narrative, "53 vs. 34") | "53 vs. 34" | 53 / 34 (matches) | 0 | NO_CHANGE | Verified |
| Babur Letta named-entities | 540 (line 2466) | 416 | 124 | Numeric drift |
| Babur BL named-entities | 65 (line 2466 narrative says "65" actually, paper text "Letta block carries 416 unique capitalized named-entity tokens vs. Base Layer's 65" — paper text already correct) | 65 | 0 | NO_CHANGE — paper text correct, running-list `46` was the bug |
| Hamerton Letta named-entities | 19 | 26 | 7 | Numeric drift |
| Hamerton BL named-entities | 19 | 22 | 3 | Numeric drift |
| Babur block duplication rate | 0.54 (line 2448 says "25.4%", running list 0.54) | 0.254 | 0.29 | Numeric drift in running list. Paper text correct (25.4%). Running-list placeholder 0.54 is stale. |
| Babur Letta unique named-entities (running list) | 540 | 416 | 124 | Numeric drift |
| 7-judge sensitivity Hamerton Δ | +0.20 (line 2440 narrative says "+0.093") | +0.093 | 0.11 | Paper text correct; running-list +0.20 stale |
| 7-judge sensitivity Babur Δ | +0.29 (line 2440 narrative says "+0.232") | +0.232 | 0.06 | Paper text correct; running-list +0.29 stale |
| 7-judge sensitivity Ebers Δ | +1.02 (line 2440 narrative says "+0.746") | +0.7464 | 0.27 | Paper text correct; running-list +1.02 stale |
| Full-stack Δ Hamerton | +0.27 (line 2483 says "+0.27") | +0.272 | 0.001 | NO_CHANGE — paper correct |
| Full-stack Δ Ebers | +1.21 (line 2483 says "+1.21") | +1.205 | 0.005 | NO_CHANGE |
| Full-stack Δ Babur | +0.38 (line 2483 says "+0.38") | +0.380 | 0 | NO_CHANGE |
| Ebers Letta block score Haiku 5-judge primary | "1.48" (running list) | **2.76** (the paper-table number) | 1.28 | Numeric drift in running list. Scaffold matches paper table. |
| Ebers Letta block score Haiku 7-judge | 2.50 (running list) | 3.00 | 0.50 | Numeric drift |
| Ebers BL unified brief Haiku 7-judge | 1.48 (running list) | 2.25 | 0.77 | Numeric drift |
| Hamerton Letta block 7-judge | 3.10 | 3.21 | 0.11 | Minor drift |

**Recommended:** The §4.5 main table at line 2432 has 6 cells with minor drift (each within ~0.25 of scaffold). Decide whether to update; the directional finding is preserved at every threshold. Named-entity counts in line 2466 narrative match scaffold. **The substantive corrections are concentrated in running-list values that no longer match the table or the body text.**

---

### Table 10: §4.6.1 Tier 2 cross-provider replication (heading line 1295)

**Location:** v10 line 1295-1302. 6 rows × 6 columns.

**Already explicitly flagged in the paper itself (line 1304):**

> *Numbers in this table are pending verification under the v11 mechanistic-check architecture. A preliminary recompute scaffold flagged a possible discrepancy between these legacy values and the 5-judge primary aggregation rule. The directional claim (5 of 6 cells) and the magnitudes are both held as-is until the full paper-wide verification pass completes.*

**v11 emit `3_study_design.json` does NOT cover this Tier 2 table directly; emit `3_study_design.json` only emits Franklin and judge calibration claims for §3.** Tier 2 numbers fall outside the current scaffold coverage. **Mark as coverage gap requiring a dedicated Tier 2 emit script.**

**Recommended:** Hold this table as-is until a dedicated `_v11_emit_tier2.py` scaffold is added. Paper already discloses the pending status.

---

### Table 11: §4.6.2 5-judge vs 7-judge sensitivity (heading line 1322)

**Location:** v10 line 1322-1326. 3 rows × 3 columns.

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| C2c v2 (random) Δ 5-judge | +0.22 | +0.1525 | 0.07 | Numeric drift (carries through from §4.3) |
| C2c v1 (fixed) Δ 5-judge | -0.25 | -0.31 (estimated; reconciliation does not directly compute this aggregate, only per-subject) | est. 0.06 | Minor drift |
| Other cells | various | various | < 0.1 | NO_CHANGE within rounding |

**Recommended:** Update C2c v2 Δ on the 5-judge column from +0.22 to +0.15 to be consistent with the §4.3 update.

---

### Table 12: Appendix B.2 Per-subject 15-row × 11-column battery composition (heading line 1874)

**Location:** v10 line 1874-1891. 15 subject rows × 11 columns (10 categories + Total) + 1 column-total row.

**The reconciliation walkthrough reports Appendix B has 14 substantive of 242 claims (5.8%).** None of those 14 are in Table B.2 — they are in B.5 and B.6.

**NO_CHANGE on all 165 cells in Table B.2.** Apply silently as cleanup if any whitespace polish is needed.

**Verified.** The battery-composition matrix is structural counts (questions per category per subject) which scaffold confirms.

---

### Table 13: Appendix B.3 Behavioral-axis distribution (heading line 1909)

**Location:** v10 line 1909-1925. 16 rows × 4 columns (Subject / LITERAL / INTERP / REFUSAL / n).

**NO_CHANGE on all rows.** Reconciliation `appendix_b_battery.json` claims for B.3 all match within rounding.

---

### Table 14: Appendix B.4 Category-level effect-size table (heading line 1932)

**Location:** v10 line 1932-1935. 3 rows × 4 columns (Axis / n / Mean Δ_spec / Median Δ_spec).

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| `appB_4_refusal_triggering_mean_delta_spec` | +0.489 | +0.4167 | 0.07 | Minor drift |
| Other 5 cells | various | various | < 0.05 | NO_CHANGE within rounding |

**Recommended:** Minor cleanup. REFUSAL_TRIGGERING mean Δ → 0.42.

---

### Table 15: Appendix B.5 Per-subject by axis Δ_spec (narrative-only at line 1941)

**Location:** v10 line 1941. NOT a table — narrative summary of cross-subject pattern.

**Substantive changes (claims embedded in narrative):**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| Hamerton REFUSAL_TRIGGERING Δ | +1.71 | +1.2526 | 0.46 | Numeric drift |
| Hamerton INTERPRETIVE_INFERENCE Δ | +1.30 (running list, narrative says +2.02) | +1.30 | 0 | NO_CHANGE |
| Hamerton LITERAL_RECALL Δ | +1.93 (narrative) — running list "1.71" | +1.25 | 0.46 (running list) / 0.68 (narrative) | Numeric drift. Paper narrative `+1.93` does not match scaffold `+1.25`. |
| Sunity Devee LITERAL_RECALL Δ | +1.71 | +1.375 | 0.34 | Numeric drift |
| Sunity Devee REFUSAL_TRIGGERING Δ | +1.71 | +1.35 | 0.36 | Numeric drift |
| Yung Wing LITERAL_RECALL Δ | +1.71 | +1.40 | 0.31 | Numeric drift |
| Cellini LITERAL_RECALL Δ | +1.71 | +1.25 | 0.46 | Numeric drift |
| Hamerton REFUSAL_TRIGGERING Δ | +1.71 | +1.2526 | 0.46 | Numeric drift (duplicated above) |
| Fukuzawa INTERPRETIVE_INFERENCE Δ | +1.71 | +0.8296 | 0.88 | Numeric drift |
| Seacole INTERPRETIVE_INFERENCE Δ | +1.71 | +0.7929 | 0.92 | Numeric drift |
| Rousseau REFUSAL_TRIGGERING Δ | +1.71 | +0.72 | 0.99 | Numeric drift |

**Note:** the running-list "1.71" placeholder appears ~12 times across appB_5 cells, suggesting a systematic placeholder bug rather than per-subject paper claims. The paper narrative (line 1941) only cites Hamerton's three axis values (+1.93, +2.02, +1.71). **Decide whether the narrative numbers are the paper's actual claim, or if the running-list 1.71 is an upstream-pipeline artifact.**

**Recommended:** Verify that the paper line 1941 claim "+1.71 REFUSAL" matches scaffold +1.25. If yes, update narrative. If the +1.93 / +2.02 are the load-bearing claims, update those instead.

---

### Table 16: Appendix B.6 Battery-composition correlation (narrative at line 1947)

**Location:** v10 line 1947-1950. Bullet list of 4 correlations + range.

**Substantive changes:**

| Claim | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| Δ_spec range max | +1.85 (line 1947) | +1.3744 | 0.48 | Numeric drift |
| LITERAL_RECALL × Δ_spec corr (current) | +0.595 (paper text) | +0.595 | 0 | NO_CHANGE |
| INTERPRETIVE × Δ_spec corr | -0.466 | -0.4656 | 0.001 | NO_CHANGE |
| REFUSAL × Δ_spec corr | +0.321 | +0.2118 | 0.11 | Minor drift |
| LITERAL × Δ_spec corr legacy | +0.646 | +0.595 | 0.05 | Paper acknowledges legacy split; legacy value reproduces |
| INTERPRETIVE × Δ_spec corr legacy | -0.582 | -0.4656 | 0.12 | Numeric drift in the legacy column |

**Recommended:** Update Δ_spec range max from +1.85 → +1.37 in line 1947. Other corrs match within rounding.

---

### Table 17: Appendix D.1 Per-subject 5-judge primary aggregate (heading line 2065)

**Location:** v10 line 2065-2081. 14 subject rows + 1 Franklin row + bands × 7 columns.

**This table is structurally identical to §4.1's table at line 712.** Reconciliation confirms full match between the two within rounding.

**NO_CHANGE on all 105 score cells.** No rebuild needed.

---

### Table 18: Appendix D.2 Per-subject anchor-crossing (heading line 2098)

**Location:** v10 line 2098-2109. 9 subject rows + slice-total row × 4 columns (Subject / Upward / Upward % / Downward / No crossing).

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| `appD_2_slice_no_crossing_pct` | 24.0% | 38.18% | 14.18 | **Numeric drift, large.** Paper line 2094 says "Stayed in band: 134 (38.2%)" — paper text correct. Running-list 24.0 is stale. |
| `appD_2_*_n_questions` (per subject) | varies (23, 25.6, 26, 27, 29, 48.7) | 39 (uniform across all 9 low-baseline subjects) | 9-25 | **Definitional difference.** Reconciliation methodology note at line 269: "scaffold emits n=312 for low-baseline question count; paper carries n=351 in the C5 row from a pre-recompute draft (the 351 → 312 transcription error)." Per-subject the paper carries varying numerators that are NOT the row total of 39 questions. **Definitional, not numeric drift — verify what the cell is meant to express.** |

**Recommended:** Keep table body as-is (paper line 2098-2109 matches scaffold for upward/downward counts). Update running-list "no crossing pct" placeholder. Verify per-subject n_questions definitional intent.

---

### Table 19: Appendix D.3 Rubric validity audit sub-tables (headings 2125, 2141, 2154, 2169)

**Four sub-tables in D.3.**

**Substantive changes:**

| Cell | Paper | Scaffold | |Δ| | Failure mode |
|---|---:|---:|---:|---|
| `appD_3_2_abstention_pct_above_3` | 3.5% | 3.13% | 0.38 | Minor drift. Paper line 2134 says "3.2%" — paper text close, running-list 3.5 is stale. |
| D.3.3 per-judge strictness mean — Sonnet | 1.20 (running list) | 1.14 (line 2142) | 0.06 | NO_CHANGE — paper text correct |
| D.3.3 per-judge strictness mean — Opus | 1.20 (running list) | 1.41 (line 2146) | 0.21 | Numeric drift in running list. Paper text correct. |
| D.3.3 per-judge strictness mean — Haiku | 1.20 | 1.29 (line 2144) | 0.09 | Numeric drift. Paper text correct. |
| `appD_3_4_C5_n` | 351 | 312 | 39 | Definitional; reconciliation note line 269 |
| `appD_3_4_C4_n` | 351 | 312 | 39 | Definitional |
| `appD_3_4_C4a_n` | 351 | 312 | 39 | Definitional |
| `appD_3_5_chars` | 1599 | 2086.67 | 487 | Numeric drift on the "low score (below 2.0) mean length" cell. Paper line 2173 reports "2,087" — paper text correct. Running-list 1599 is stale. |
| `appD_3_5_mid_range_chars` | 2829 | 2829.4 | 0.4 | NO_CHANGE within rounding |
| `appD_3_5_ultra_high_chars` | 2790 | 2790.09 | 0.09 | NO_CHANGE |

**Recommended:** D.3.4 cell row count is the single material change worth flagging. Decision: keep n=351 as the paired-question count (matches §4.1 anchor-crossing slice total of 351), or switch to n=312 (the response-set under the Babur exclusion). **Definitional choice.**

---

### Table 20: Appendix D.4 Per-judge score matrix (heading line 2191)

**Location:** v10 line 2191-2262. 14 subjects × 5 conditions × 9 columns = 630 cells.

**Reconciliation reports Appendix D has 17 substantive of 761 (2.2%).** That includes 6-12 cells in this matrix and the D.3 / D.5 audit subtables.

**Body cells matching scaffold for the per-judge matrix:** essentially all 630 cells were verified during the §3.7.2 calibration check (Spearman ρ 0.86-0.93 between judges). Reconciliation does not enumerate per-judge per-cell mismatches — it captures aggregate columns (5m, 7m) which match within rounding.

**NO_CHANGE on the 630 cells of this matrix as a structural rebuild proposal.** Spot-verify: Sunity Devee C2c row's Gemini Pro cell shows "n/a" in paper (line 2200) and scaffold confirms; Sunity Devee 7m mean of 1.36 matches scaffold 1.36.

**Recommended:** No rebuild needed. Apply silently if any rounding-presentation polish is desired.

---

## Recommended apply order

### Tier 1: silent cleanup (apply as a single edit batch, no narrative changes)

1. **§4.1 per-subject body table** — NO_CHANGE confirmed on all 14 subject rows. No edits.
2. **§4.1.2 transition table** — NO_CHANGE confirmed.
3. **§4.2 per-subject body table score cells** — NO_CHANGE on C5/C2a/C4/C8/C4a (only the C9 column and the source-words/compression-ratio columns shift).
4. **§4.4.1 body tables** — paper text already carries scaffold values inline; only running-list placeholders are stale. No body-table edits needed.
5. **Appendix B.2 (battery composition)** — NO_CHANGE on 165 cells.
6. **Appendix B.3 (axis distribution)** — NO_CHANGE.
7. **Appendix D.1 per-subject aggregate** — NO_CHANGE.
8. **Appendix D.4 per-judge matrix** — NO_CHANGE.

### Tier 2: minor numeric drift (apply with one-line per-row note in the markdown commit message)

1. **§4.2.1 pairwise comparison table (line 837-840)** — replace 6 cells (115/190/46 → 108/187/56 for C8 vs C2a; 155/42/115 → 153/45/114 for C9 vs C4a). Percentages shift < 1 pp.
2. **§4.2 per-subject Source words / Compression ratio columns** — replace 7 of 10 ratios. Replace per-subject token estimates if switching column-header convention.
3. **§4.5 main result table (line 2432)** — replace 6 of 9 cells with minor drift. Direction and ranking preserved.
4. **§4.5 named-entity narrative (line 2466)** — replace Babur Letta count 540 → 416. Replace Hamerton counts 19/19 → 26/22. Ebers counts 53/34 already correct.
5. **Appendix B.4** — REFUSAL_TRIGGERING mean Δ +0.49 → +0.42.
6. **Appendix B.6** — Δ_spec range max +1.85 → +1.37; REFUSAL × Δ_spec corr +0.32 → +0.21.
7. **Appendix D.2** — Verify "Stayed in band" denominators across 9 rows.
8. **Appendix D.3.2 abstention pct** — 3.5% → 3.13%.

### Tier 3: substantive changes requiring author decision (do NOT apply silently)

1. **§4.1 regression-summary frame (lines 749, 751, 1372)** — under the locked aggregation, the level regression has slope +0.04, R² = 0.008, p = 0.76. The Δ-on-C5 regression slope -0.96 and R² = 0.82 reproduce. **The "Honest reframing" paragraph at line 749 already captures this finding correctly; only the placeholder running-list values need replacing.** Author should review whether any §1, §5, or §6 prose still asserts a clean negative gradient that the level reframe contradicts.
2. **§4.1 mean Δ_C4a all-14 vs. low-baseline-9** — clarify which slice the +0.89 refers to. Paper text is consistent (line 92, 1392 use "low-baseline"); running-list claim_id may be mislabeled. Verify which scaffold claim_id corresponds to which paper claim before any edit.
3. **§4.3 per-subject wrong-spec table — NEW TABLE** — decide whether to add a per-subject c2c v1 / v2 table (13 globals × 3 columns). 8 sign flips at the per-subject level. Paper currently does not expose these per-subject values. **This is the single largest coverage decision.**
4. **§4.3 random-derangement aggregate +0.22 → +0.15** — appears in §1.3 abstract, §4.3 line 892, §4.6.2 line 1325, §5 summary line 1374. Cascading replacement across 4 places. Direction preserved but magnitude shifts by 0.07.
5. **§4.4.1 Letta archival "Subjects improved (of 9)" 9/9 → 8/9 and Mem0 native 9/9 → 7/9** — paper text already has 8/9 and 7/9 inline; the running-list 9/9 placeholders are stale. Verify cells in lines 1039 and 1050 directly.
6. **§4.4.2 Table 4.6 (line 1196) — panel disclosure already in place at line 1209.** Body table is on the 6-judge audit panel by explicit declaration. The 0-of-45 match against the 5-judge primary is methodologically expected; line 1209 says so. **Decision:** keep table as-is OR rebuild on 5-judge primary. If rebuilt, the inline sentences around lines 1086-1094 ("89 of 516 (17.2%)" / "37 (7.2%)" / "52 (10.1%)") need updating to "89 of 546 (16.3%)" / "57 (10.4%)" / "53 (9.7%)" or similar based on the 5-judge recompute. **Author choice — both options are documented.**
7. **§4.4.3 Keckley Q21 — RESOLVED, no decision needed.** Direct verification of v10 line 1244-1250 against scaffold shows the body table already presents the locked 5-judge primary values. The reconciliation's "sign flip" entries refer to a stale running-list extraction. Tier 1 silent cleanup of the running list only.
8. **Appendix D.3.4 length-correlation row count n=351 vs. n=312** — definitional question about which response-set the row applies to. Paper carries 351; scaffold uses 312 (paired-only). Choice has no correlation-direction implications.
9. **Appendix B.5 per-subject by axis Δ_spec narrative** — line 1941 cites Hamerton +1.93/+2.02/+1.71. Scaffold: +1.25/+1.30/+1.25. Paper narrative numbers do not match scaffold. **Verify which is the load-bearing claim** (the paper's narrative numbers, or the scaffold's 5-judge primary recompute).

---

## Cells with no scaffold coverage (gaps)

- **§4.6.1 Tier 2 cross-provider replication table (line 1295-1302).** Six (subject × response-model) cells are not covered by any current v11 emit script. Paper itself flags this at line 1304. **Action:** add `_v11_emit_tier2.py` before any rebuild on this table.
- **PAPER_ONLY (paper has cell, no scaffold claim):** the reconciliation diff's PAPER_ONLY scan returned **0 entries**. No other coverage gaps detected by heuristic scan.

---

## Implementation note for the author

When the author approves this proposal, the rebuild should proceed in the order above (Tier 1 silent → Tier 2 minor → Tier 3 substantive). Each tier's batch should commit separately so that any reviewer can isolate the silent cleanup from the substantive author-decision changes.

For Tier 3 items 6 and 7 specifically (the §4.4.2 and §4.4.3 panel-asymmetry items), the rebuild must include either:
- An explicit footnote on each table disclosing the audit-panel use (preserving paper as-is); OR
- A full numeric replacement to 5-judge primary with a methodology paragraph in §4.4 noting the panel switch and the resulting paired_total_n shift from 507 → 546.

Both options are defensible. The reconciliation diff's methodology-asymmetry section (lines 263-272 of `v11_reconciliation_diff.md`) is the author's reference for which choice to make on each item.
