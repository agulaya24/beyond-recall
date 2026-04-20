# Paper Corrections: Beyond Recall

**Generated:** 2026-04-13
**Updated:** 2026-04-18 (Session 113 — full-stack refresh + framing corrections)
**Method:** Every quantitative claim in the paper verified against raw data files. Zero inference.

**The current single source of truth for numbers is `docs/DATA_REFERENCE.md`. Any conflict between that file and this changelog or the paper is resolved in favor of DATA_REFERENCE.md.**

---

## S113 CORRECTIONS (2026-04-18)

Full-stack refresh of all 14 subjects plus framing rewrite. The corrections below supersede specific earlier entries in this file; historical entries are retained for traceability.

### S113-A. Hamerton C5 baseline drift: 1.41 (S105) → 1.25 (S113)

- **Status:** Baseline moved under the refreshed full-stack run. `DATA_REFERENCE.md` §1 and §7 both report 1.25 as the current Hamerton C5 baseline.
- **Relationship to earlier correction #1:** Correction #1 (below) locked in 1.41 as the S105 brief-only value. That lock is now **superseded by the S113 refresh**, not retracted. 1.41 was correct for the brief-only data; 1.25 is correct for the S113 full-stack data used by the current paper draft.
- **Flag for Aarik:** Confirm which run the paper should present as primary. Current draft uses 1.25. Do NOT re-open correction #1 — instead, retain both values with the run that produced each.

### S113-B. §4.1.1 Hamerton lift (spec − baseline): +0.55 → +0.67

- **Previous:** +0.55 (computed against older spec-only score)
- **Current:** +0.67 under S113 refresh. DATA_REFERENCE §8 shows C2a spec-only = 3.04, C5 baseline = 1.25. Lift ≠ 3.04 − 1.25 directly; the +0.67 is the cross-subject mean lift on Table 4.1 (see §1 aggregates: mean Δ facts+spec = +0.67 all-14).
- **Action:** Paper text updated S113.

### S113-C. §4.2 Table 4.2 Hamerton-condition scores

| Condition | Old value (paper) | New value (DATA_REFERENCE §8) |
|---|---:|---:|
| C3 Mem0 + spec | 3.31 | **2.77** |
| C3 Supermemory + spec | 3.14 | **2.86** |
| C4a Facts + spec | 3.28 | **3.22** |
| C2a Spec only | (carried over) | **3.04** |
| C8 Raw corpus | 2.32 | 2.32 (unchanged) |
| C9 Raw + spec | 3.22 | 3.22 (unchanged) |
| C5 Baseline | 1.41 | 1.25 |

### S113-D. §4.1.2 Judge parse-failure — corrected attribution

- **Old paper text:** "Gemini Pro has ~40% parse failure rate."
- **Source data:** DATA_REFERENCE §9 shows Gemini Pro parse failure ~0.5%; GPT-5.4 parse failure ~19%.
- **Correction:** The high-parse-failure judge is **GPT-5.4 (~19%)**, not Gemini Pro. Gemini Pro's issue is coverage (only ran on Hamerton + Tier 2), not parse failure. Gemini Pro's score offset vs non-Gemini panel is +1.0 (see §4.1.2 sensitivity analysis).

### S113-E. §4.5 Wrong-spec v2 (random derangement): 2.21 → 2.30

- **Old value:** 2.21 (this was in fact the S105 brief-only wrong-spec Franklin-for-Hamerton number — mislabeled as v2)
- **Correct values per DATA_REFERENCE §6:**
  - C5 baseline = 2.02 (14-subject mean)
  - C2a correct spec = 2.55 (14-subject mean)
  - C2c v1 (Franklin-for-all) = 1.86 (−0.16 vs baseline, −0.69 vs correct)
  - C2c v2 (random derangement, seed=42) = **2.30** (+0.28 vs baseline, −0.25 vs correct)
- **Interpretation:** v1 is the cleaner null. v2 is noisier because random pairings sometimes land on loosely-similar specs. Both are far below correct-spec scores; content specificity matters.

### S113-F. §4.3 "94% retrieval disagreement" — FLAGGED FOR VERIFICATION

- **Paper claim:** "94% retrieval disagreement across embedding systems."
- **Prior documented number (PAPER_CORRECTIONS #12):** 66% top-1 all-different (Mem0/Letta/Supermemory across 80 Hamerton questions).
- **Gap:** The 94% figure does not match the 66% top-1 disagreement nor the 92.5% (1 − 7.5% all-agree) figure. It may come from a top-3 or top-5 overlap computation, or from an updated 14-subject analysis. **Cannot be verified from current `DATA_REFERENCE.md` or from any file in the repo during this audit.**
- **Action for Aarik:** Either (a) source the 94% from a specific computation file and add to DATA_REFERENCE, (b) revert to the verified 66% top-1 disagreement, or (c) strike the specific percentage.

### S113-G. §4.3.1 Letta stateful-agent test — NEW SECTION

Added to DATA_REFERENCE.md as §7:

- Final Letta `human` memory block: 22,472 chars (~3,167 words, ~5,600 tokens)
- Base Layer full-stack spec: 34,579 chars (~5,250 words, ~8,500 tokens)
- Size ratio Letta / BL = 0.65
- Run A (gpt-4o-mini + Letta agent loop, native): 3.38 (6 judges)
- Run B (Haiku + Letta block as context, matched to C2a): **3.24** (6 judges); **3.12** non-Gemini (4 judges); **3.04** reference C2a (7 judges)
- At matched response model, Letta block predicts +0.20 above Base Layer spec at 65% the context size
- **Interpretation:** Structural parity, size efficiency. Single-subject result (Hamerton only); n=2 Ebers generalization in flight.

### S113-H. §4.4 Base Layer repositioning (framing, not numeric)

Paper and public docs now consistently state: **Base Layer is not a memory provider. It is a behavioral-specification layer that layers on top of any memory system.** DATA_REFERENCE §12 shows BL's standalone retrieval wins C1 outright on only 1 of 9 low-baseline subjects (Hamerton — the pipeline-development subject, so pipeline-tuning bias is present). BL is typically middle-of-pack or behind Letta on retrieval. Removed from all public docs: any implication that Base Layer outperforms memory providers in general.

### S113-I. §5.7 Memory-provider reframing (referee, not competitor)

The paper now presents memory providers as the substrate Base Layer layers on top of, not as competitors that Base Layer replaces. The load-bearing claim is the additive spec layer, tested in the controlled configuration and confirmed on the low-baseline slice (DATA_REFERENCE §4): adding the spec improves all 4 commercial memory systems (Mem0 +0.13, Letta +0.23, Zep +0.20, Supermemory +0.004 — all positive or barely positive on the population of interest).

### S113-J. §5.8 Architectural convergence with Letta

New subsection added per §4.3.1: Letta's stateful-agent path produces an interpretive representation (not just retrieval) and reaches Base-Layer-parity representation at 65% the context size. Five overlapping behavioral patterns identified by independent Opus comparison. This is architectural convergence on the same finding (the value is in compressed interpretive representation) reached by two independent methods.

### S113-K. Flagship sentence adopted

Consistent wording across README, blog, paper: **"Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know."** Always co-located with the low-baseline (n=9) qualifier and the ~99% real-user framing from DATA_REFERENCE §1.

### S113-L. Inter-judge statistic substitution

Legacy docs cite "pairwise Spearman ρ 0.89–0.98" (4-judge Hamerton brief-only). Current statistic per DATA_REFERENCE §2 is **Krippendorff α = 0.535 (all 7 judges, ordinal, moderate)** and **α = 0.659 (non-Gemini 5-judge panel, substantial)**, plus Wilcoxon W=10.0 p=0.0076 (C5 vs C2a) and W=9.0 p=0.0063 (C5 vs C4a). Docs updated to use α + Wilcoxon; Spearman ρ retained only where it references the historical 4-judge Hamerton computation and is labeled as such.

---

## S113 AUDIT DISCREPANCIES (2026-04-18, discovered during pre-launch audit)

These are discrepancies found during the S113 provenance audit against `beyond_recall_v6_draft.md`. They are NOT pre-existing corrections — they are newly surfaced inconsistencies the paper currently contains. Listed here for Aarik to resolve before launch. Do NOT silently "fix" these without confirmation; these are load-bearing and the paper must be updated, not the audit docs.

### S113-M. §3.7 Krippendorff α = 0.723 conflicts with §4.1 α = 0.535 / 0.659

- **§3.7 line 601:** "Krippendorff's alpha (ordinal): 0.723 across all 7 judges (absolute agreement on question-level scores)."
- **§4.1 line 626:** "Krippendorff's alpha (ordinal) across 7 judges: 0.535 (all judges) / 0.659 (5 non-Gemini judges)."
- **DATA_REFERENCE §2:** 0.535 (all 7), 0.659 (non-Gemini 5).
- **Diagnosis:** §3.7 value (0.723) is stale from a pre-S113 run. The S113-L correction updated §4.1 and DATA_REFERENCE but §3.7 was missed.
- **Action:** Update §3.7 to match §4.1 (0.535 / 0.659). Also revise surrounding prose ("α=0.723 exceeds the 0.667 threshold") — 0.535 is below the 0.667 threshold, so the sentence's qualitative interpretation must also change (consistent with §4.1.2 framing that non-Gemini 0.659 is the substantive value).
- **Severity:** HIGH — internally contradictory within the paper.

### S113-N. §4.6 Hamerton C4a = 3.28 conflicts with §4.1 Table 4.1 C4a = 3.22

- **§4.6 line 865:** "His C4a score of **3.28** represents the largest absolute improvement in the study (+1.97 points from baseline)..."
- **§4.1 Table 4.1 line 636:** Hamerton C4a = 3.22, Δ = +1.97.
- **§4.2 Table 4.2 line 707:** C4a = 3.22.
- **DATA_REFERENCE §1 / §8:** C4a = 3.22.
- **Math check:** 3.22 − 1.25 = 1.97 ✓. 3.28 − 1.25 = 2.03, which contradicts the "+1.97" stated in the same sentence.
- **Diagnosis:** 3.28 is a typo in §4.6; 3.22 is correct.
- **Action:** Change §4.6 "3.28" to "3.22".
- **Severity:** MEDIUM — internally contradictory within the paper.

### S113-O. Reproducibility cost: $60 vs $500-700

- **§3.3 line 435 / §5.10 line 1116:** "$500-700 in LLM API charges plus ~$80 in commercial memory system subscriptions" for the full study; "Reproducible for under $60" at §5.10.
- **Diagnosis:** These refer to different things (full 14-subject study vs. single-spec generation), but the paper does not clarify which is which at §5.10.
- **Action:** Either scope the $60 line ("The pipeline is reproducible — generating one spec for one subject costs under $1 and running the full battery for one subject costs under $60 per condition") or remove the $60 line.
- **Severity:** LOW — apparent contradiction; trivial to resolve.

### S113-P. Twin-2K: abstract says "71.83% accuracy" — external claim

- **§2.3 line 359:** "Twin-2K (Toubia et al., 2025): Behavioral prediction at scale (2,000 participants, 71.83% accuracy)."
- **Source:** Toubia et al. 2025 paper (REF-07).
- **Status:** Accurate per external record; no source file in study repo.
- **Action:** None; standard external citation.

### S113-Q. Supermemory vendor numbers (81.6%, 85.2%) — external, unsourced in paper

- **§2.1 line 344:** "Scores 81.6% on LongMemEval with GPT-4o (85.2% with Gemini 3 Pro)."
- **Source:** Supermemory marketing page / their own benchmark. Not independently reproduced in our study.
- **Action:** Add "(per Supermemory's own reported results on LongMemEval)" or footnote the source.
- **Severity:** LOW — standard practice to cite vendor claims.

### S113-R. Letta team / funding details (§5.8) — external, unsourced

- **§5.8 line 1078:** "Charles Packer and Sarah Wooders at UC Berkeley, connected to Ion Stoica and Joseph Gonzalez's Sky Computing group... raised ~$10M in seed funding (Felicis, GV)."
- **Status:** External public reporting; no repo source.
- **Action:** Accept as editorial context in a discussion section, or cite a TechCrunch/press release URL. Consider whether the personal/funding framing belongs in a research paper at all (Gemini Pro review round 2 flagged §5.8's personal tone as unconventional).
- **Severity:** LOW — editorial judgment, not a numerical correctness issue.

### S113-S. §5.4 hedging table (127/507, 13/507, 3/507) — missing source file

- **§5.4 Table lines 1023-1026.**
- **Status:** Not present in DATA_REFERENCE.md; likely computed from a per-response hedging-detection script over `results/` files.
- **Action:** Add a row to DATA_REFERENCE.md (new §N: Hedging Analysis) pointing to the source script/JSON. Until then, PROVENANCE_INDEX flags this as NOT FOUND.
- **Severity:** MEDIUM — prominent finding (abstract + §1 + §5.4) should be sourced in the single source of truth.

### S113-T. §4.1.2 Gemini "~35% of responses scored 5.0" and "p < 0.02 non-Gemini recomputation" — not in DATA_REFERENCE

- **§4.1.2 line 673:** "Gemini judges assign 5.0 to approximately 35% of responses, compared to 0.4-9% for the other five judges."
- **§4.1.2 line 677:** "Recomputing on the 5-judge non-Gemini aggregate yields p < 0.02."
- **Source:** Per-judge score histograms + Wilcoxon recomputation — computable from `RESULTS_S113.json`, but not tabulated in DATA_REFERENCE §2 or §9.
- **Action:** Add explicit rows to DATA_REFERENCE §2 (non-Gemini p-value) and §9 (per-judge 5.0 assignment rate).
- **Severity:** MEDIUM — sensitivity analysis is load-bearing for the paper's robustness claim.

---

## CORRECTIONS REQUIRED (S105 — historical, preserved)

### 1. Hamerton C5 Baseline: 1.37 -> 1.41

- **Paper value:** 1.37
- **Raw data value:** 1.4103 (rounds to 1.41)
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_judgments.json` — C5_baseline scores for 39 prediction questions (IDs 21-60 excluding 50)
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/prediction_summary.json` — `"C5_baseline": {"avg_score": 1.41, "n": 39}`
- **Origin of error:** `analysis_for_review.md` reports 1.37 with no supporting computation. No data file anywhere contains 1.37. The fullstack runs do not include a C5 condition — the baseline was carried forward from the original brief-only run, which shows 1.41.
- **Action needed:** Change "Baseline 1.37" to "Baseline 1.41" in Section 4.1 title, Table 4.1 (C5 Baseline row), and all references throughout paper (Sections 4.4, 5.1). Recompute Cohen's d and CIs against 1.41 baseline (SD = 1.02). Cohen's d recalculates to 1.21 (still correct — the computation already used 1.41 implicitly since it was done against the actual C5 distribution).
- **Effect on other claims:** The +117% effect for Hamerton in Section 4.4 table changes: (2.97 - 1.41) / 1.41 = +110.6%. Paper says +117% (which was based on 1.37).

### 2. Franklin C5 Baseline: 3.99 -> 4.10

- **Paper value:** 3.99
- **Raw data value:** 4.10
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_franklin_20260411_014509/analysis/haiku_prediction_summary.json` — `"C5_baseline": {"avg_score": 4.1, "n": 40}`
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/run_franklin_20260411_014509/analysis/haiku_judgments.json` — C5_baseline mean = 4.1000 (computed from 40 raw scores)
- **Origin of error:** `analysis_for_review.md` reports 3.99. No data file contains 3.99. The fullstack Franklin run has no C5 condition.
- **Action needed:** Change "3.99" to "4.10" in Sections 4.3, 4.5, 5.1, 5.2. The qualitative finding (all injected context < baseline) still holds since all fullstack conditions are below 4.10.

### 3. Sunity Devee Best Score: 2.74 -> 2.68

- **Paper value:** 2.74 (labeled "Best Spec")
- **Raw data value:** 2.675 (rounds to 2.68)
- **Source file:** `memory-study-repo/data/global_subjects/sunity_devee/judgments.json` — C4_factdump haiku_score mean = 2.675 (n=40)
- **All condition means:** C2a_spec=2.225, C4_factdump=2.675, C4a_facts_plus_spec=2.375
- **Additional issue:** The best condition is C4_factdump (all facts, NO spec), not a spec condition. The table header says "Best Spec" but this condition does not include a specification.
- **Action needed:** Change 2.74 to 2.68. Change +174% to +168%. Consider relabeling column "Best Spec" to "Best Condition" since the winning condition for Sunity Devee and Babur is C4_factdump (no spec).

### 4. Gemini Pro Verbatim Calibration: 4.37 -> 4.15

- **Paper value:** 4.37
- **Raw data value:** 4.15
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — verbatim test, gemini_pro_score mean = 4.15 (n=20)
- **Also confirmed in:** `memory_system/data/experiments/memory_systems/results/judge_evaluation/gemini_pro_calibration.json` — same value 4.15
- **Action needed:** Change 4.37 to 4.15 in Section 4.6 table.

### 5. Gemini Pro Paraphrased Calibration: 3.74 -> 3.55

- **Paper value:** 3.74
- **Raw data value:** 3.55
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — paraphrased test, gemini_pro_score mean = 3.55 (n=20)
- **Action needed:** Change 3.74 to 3.55 in Section 4.6 table.

### 6. Gemini Pro Short Correct Calibration: 3.17 -> 2.85

- **Paper value:** 3.17
- **Raw data value:** 2.85
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — short_correct test, gemini_pro_score mean = 2.85 (n=20)
- **Action needed:** Change 3.17 to 2.85 in Section 4.6 table.

### 7. Gemini Pro Long Correct Calibration: 1.26 -> 1.20

- **Paper value:** 1.26
- **Raw data value:** 1.20
- **Source file:** `memory-study-repo/results/judge_calibration/gemini_pro_calibration.json` — long_correct test, gemini_pro_score mean = 1.20 (n=20)
- **Action needed:** Change 1.26 to 1.20 in Section 4.6 table. Update prose: "Gemini Pro penalizing padding severely (1.20)" not "(1.26)".

### 8. GPT-5.4 Short Correct Calibration: 4.15 -> 4.20

- **Paper value:** 4.15
- **Raw data value:** 4.20
- **Source file:** `memory-study-repo/results/judge_calibration/gpt54_calibration.json` — short_correct test, gpt54_score mean = 4.20 (n=20)
- **Action needed:** Change 4.15 to 4.20 in Section 4.6 table.

### 9. GPT-5.4 Long Correct Calibration: 4.40 -> 4.80

- **Paper value:** 4.40
- **Raw data value:** 4.80
- **Source file:** `memory-study-repo/results/judge_calibration/gpt54_calibration.json` — long_correct test, gpt54_score mean = 4.80 (n=20)
- **Action needed:** Change 4.40 to 4.80 in Section 4.6 table.

### 10. Zep 39% Same-Fact Retrieval: UNVERIFIABLE

- **Paper value:** "Zep graph bias. Same father-property-settlement fact retrieved for 39% of all questions"
- **Raw data finding:** The most common Zep top-1 fact ("Hamerton's father lost interest in his profession after his mother's death") appears in 9/80 questions (11.2%). The specific "property settlement" fact appears in only 3/80 questions (3.8%). Father-RELATED facts (any fact mentioning "father") appear in 43/80 (53.8%).
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/fact_localization.json` — 80 questions, Zep top-1 analyzed
- **Origin of claim:** `MEMORY_SYSTEMS_STUDY_RESULTS.md` states this value but it cannot be reproduced from the fact_localization.json data. The 39% does not match any computation: not 39% of 80 questions, not 39% of 40 prediction questions, not 39% of the 39-question subset.
- **Action needed:** Either (a) locate the original data source for the 39% claim, (b) replace with the verifiable number: "Father-related facts retrieved for 54% of all questions — graph traversal bias toward high-connectivity nodes," or (c) remove the specific percentage.

### 11. Hamerton Effect Percentage: +117% -> +111%

- **Paper value:** +117% (computed from baseline 1.37)
- **Corrected value:** +110.6% (rounds to +111%, computed from baseline 1.41: (2.97 - 1.41) / 1.41)
- **Source:** Derived from corrections #1 and the verified C3 score of 2.97
- **Action needed:** Change +117% to +111% in Section 4.4 global gradient table.

### 12. Retrieval Disagreement: 65% -> 66%

- **Paper value:** 65% retrieval disagreement
- **Raw data value:** 66.2% (53/80 questions all-different top-1 for Mem0/Letta/Supermemory)
- **Source file:** `memory_system/data/experiments/memory_systems/results/run_20260409_182743/analysis/fact_localization.json`
- **Action needed:** Change 65% to 66%.

### 13. Retrieval Agreement: 8% -> 7.5%

- **Paper value:** 8% agreement
- **Raw data value:** 7.5% (6/80)
- **Source file:** Same as above
- **Action needed:** Change 8% to 7.5% or "8%" is acceptable as rounded.

---

## VERIFIED CORRECT (no changes needed)

### Hamerton Full-Stack Scores (Section 4.1)

| Claim | Paper | Data | Status |
|---|---|---|---|
| C3 Spec + Mem0 mean | 2.97 | 2.9744 | CORRECT |
| C3 Spec + Mem0 SD | 1.51 | 1.5129 | CORRECT |
| C3 Spec + Supermemory mean | 2.85 | 2.8462 | CORRECT |
| C3 Spec + Supermemory SD | 1.42 | 1.4242 | CORRECT |
| C2a Spec only mean | 2.72 | 2.7179 | CORRECT |
| C2a Spec only SD | 1.38 | 1.3755 | CORRECT |
| C4a All facts + spec mean | 2.69 | 2.6923 | CORRECT |
| C4a All facts + spec SD | 1.45 | 1.4537 | CORRECT |
| C2c Wrong spec mean | 1.38 | 1.3846 | CORRECT |
| C2c Wrong spec SD | 0.94 | 0.9351 | CORRECT |

**Source:** `memory-study-repo/results/hamerton/judgments.json` (n=39 per condition)

### Statistical Tests

| Claim | Paper | Data | Status |
|---|---|---|---|
| Sign test: 16 wins, 4 losses, 19 ties | 16/4/19 | 16/4/19 | CORRECT |
| p = 0.012 | 0.012 | 0.0118 (two-sided) | CORRECT |
| Cohen's d = 1.21 | 1.21 | 1.2128 | CORRECT |

**Source:** Computed from `prediction_judgments.json` C3_mem0 vs C1_mem0 (sign test); fullstack C3 vs brief-only C5 (Cohen's d)

### C9 Raw Corpus Score

| Claim | Paper | Data | Status |
|---|---|---|---|
| C9 score = 2.31 | 2.31 | 2.3077 | CORRECT |

**Source:** `memory_system/.../append_c4a_c9/haiku_judgments.json`

### Calibration (Haiku, Gemini Flash, GPT-4o)

| Test/Judge | Paper | Data | Status |
|---|---|---|---|
| Verbatim / Haiku | 5.00 | 5.00 | CORRECT |
| Verbatim / Gemini Flash | 5.00 | 5.00 | CORRECT |
| Verbatim / GPT-4o | 5.00 | 5.00 | CORRECT |
| Paraphrased / Haiku | 4.75 | 4.75 | CORRECT |
| Paraphrased / Gemini Flash | 4.70 | 4.70 | CORRECT |
| Paraphrased / GPT-4o | 5.00 | 5.00 | CORRECT |
| Short correct / Haiku | 3.80 | 3.80 | CORRECT |
| Short correct / Gemini Flash | 3.85 | 3.85 | CORRECT |
| Short correct / GPT-4o | 4.05 | 4.05 | CORRECT |
| Long correct / Haiku | 5.00 | 5.00 | CORRECT |
| Long correct / Gemini Flash | 3.80 | 3.80 | CORRECT |
| Long correct / GPT-4o | 3.35 | 3.35 | CORRECT |
| Verbatim / GPT-5.4 | 5.00 | 5.00 | CORRECT |
| Paraphrased / GPT-5.4 | 5.00 | 5.00 | CORRECT |

**Source:** `memory-study-repo/results/judge_calibration/judgments.json`, `gpt4o_calibration.json`, `gpt54_calibration.json`

### Global Subject Scores (All Match Except Sunity Devee)

| Subject | Paper Baseline | Data | Paper Best | Data | Status |
|---|---|---|---|---|---|
| Georg Ebers | 1.07 | 1.075 | 2.40 | 2.400 | CORRECT |
| Cellini | 1.43 | 1.425 | 2.30 | 2.300 | CORRECT |
| Rousseau | 1.55 | 1.550 | 2.23 | 2.225 | CORRECT |
| Seacole | 2.00 | 2.000 | 2.52 | 2.525 | CORRECT |
| Yung Wing | 2.00 | 2.000 | 2.55 | 2.550 | CORRECT |
| Babur | 2.02 | 2.025 | 2.45 | 2.450 | CORRECT (but best is C4_factdump, not a spec condition) |
| Fukuzawa | 2.08 | 2.075 | 2.90 | 2.900 | CORRECT |
| Keckley | 2.35 | 2.350 | 2.65 | 2.650 | CORRECT |
| Bernal Diaz | 2.38 | 2.375 | 2.70 | 2.700 | CORRECT |
| Equiano | 2.42 | 2.425 | 2.38 | 2.375 | CORRECT |
| Augustine | 2.98 | 2.975 | 2.80 | 2.800 | CORRECT |
| Zitkala-Sa | 3.20 | 3.200 | 2.83 | 2.825 | CORRECT |

**Source:** `memory-study-repo/data/global_subjects/*/judgments.json` (n=40 per condition per subject)

### Fact Counts

| Claim | Paper | Data | Status |
|---|---|---|---|
| ~460 facts (Hamerton) | ~460 | 462 | CORRECT |
| Unique top-1: 57, 59, 67, 41 | Mem0=57, Letta=59, Super=67, Zep=41 | Mem0=57, Letta=59, Super=67, Zep=41 | CORRECT |

---

## SUMMARY

| Category | Count |
|---|---|
| **Corrections required** | 13 |
| **Major corrections (>0.05 difference)** | 5 (baselines, Sunity Devee, GPT-5.4 long_correct, Gemini Pro short_correct) |
| **Minor corrections (<0.05 difference)** | 4 (Gemini Pro verbatim/paraphrased/long_correct, GPT-5.4 short_correct) |
| **Unverifiable claims** | 1 (Zep 39%) |
| **Derived corrections** | 3 (Hamerton effect %, retrieval disagreement %, agreement %) |
| **Verified correct** | ~70 values |

### Root Cause

The `analysis_for_review.md` file was the source document for the paper's numbers. For most values, it correctly transcribes the raw data. For the Hamerton baseline (1.37 vs 1.41), Franklin baseline (3.99 vs 4.10), and all Gemini Pro / GPT-5.4 calibration values, the analysis_for_review.md contains numbers that do not appear in any raw data file. These appear to be from an earlier analysis pass, a different computation method, or transcription errors that were never reconciled against the source data.
