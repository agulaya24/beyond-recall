# Mechanistic data audit — 2026-05-07

**Auditor:** Claude (overnight job; v11.8 stage; spec at `docs/beyond_recall_v11_8_draft.md`).
**Inputs:** `docs/reviews/numerical_claims_audit_v11_8_20260505.md`, `docs/research/s114_parse_failure_manifest.json` (215 cells, 12,603 PFs, S114 baseline 2026-05-05), all `results/<subject>/*_judgments_*.json` files, `results/_s114_backfills/*.json` (125 cells, 2,744 rescued rows).
**Working artifacts:** `_audit_20260507_remaining_work.json`, `_audit_20260507_actionable.json`.

**Status:** Complete. Audit consumed 18 of 500 budgeted judge API calls.

---

## Executive summary

1. **The 2026-05-05 audit's headline P1 finding (Keckley Q21 BL Δ = −2.333) is wrong.** That number is the 3-judge subset mean computed from the merged judgment file pre-S114 backfills. With `_s114_backfills/` overlaid (which the v11 emit script does and `_v11_emit/4_4_2_4_4_3.json` reflects), the **5-judge primary panel mean is BL C1 = 3.4, C3 = 1.2, Δ = −2.2**, matching the v11.2 paper draft at line 1582 and the `_v11_emit` JSON exactly.

2. **A NEW load-bearing P0 drift was found in v11.8.** Paper §4.4.4 line 1438-1439 (case study table) reports Base Layer Q21 as **C1 = 2.0, C3 = 0.6, Δ = −1.4** with a footnote claiming "covers 3 judges (Haiku, Sonnet, Opus)." None of these three numbers reproduce from any data source. The 3-judge subset gives 3.33 / 1.00 / Δ = −2.33 (matching the existing supporting analysis at `docs/research/baselayer_c1_vs_c3_paired_analysis.md`); the 5-judge primary with backfills gives 3.4 / 1.2 / Δ = −2.2 (matching `_v11_emit/4_4_2_4_4_3.json`); no subset of available judge scores produces 2.0 / 0.6. **This appears to be a manual data-entry error introduced between v11.2 (which used the correct 3.4/3.6/−2.2 framing) and v11.8.**

3. **Parse-failure inventory:** 5,267 historical failure rows across 816 judgment files. 2,744 rescued by 2026-05-05 S114 backfills. **2,523 unrescued failures remain.** Of these:
   - 1,624 are gemini_flash failures (1,478 empty_response + 146 http_403). These are 7-judge sensitivity panel only; primary-panel claims unaffected. Empty-response pattern is a likely API-key permission or content-filter issue and rerun is unlikely to rescue.
   - 209 are 5-primary-judge failures × 5 judges, concentrated in non-actionable cells where response data does not exist:
     - 190 across Babur C9 (already documented at paper line 366, 990, 2470 as context-window omission).
     - 19 across `C1_<system>_fullpipeline` cells for 4 SM-paid-tier-failure subjects + 1 small Mem0 gap (already documented at paper line 1304 footnote).
   - **No unrescued failures exist on cells that affect paper §4.1 / §4.2 / §4.4 main aggregate tables on the 5-judge primary panel.**

4. **The §4.4.4 finding above does NOT come from a parse failure.** All 5 primary judges have valid scores for BL Q21 in the post-backfill data. The drift is in the paper, not the data. Stress-tested via four independent paths (fresh emit script run, direct recompute from per-judge files, v11.2 paper draft cross-reference, question-id alignment check).

5. **Targeted reruns:** the primary-panel 5-judge data is complete. A 10-call pilot on gemini_flash empty-response cells with `maxOutputTokens=8` returned 0/10 rescues. A 3-call follow-up debugging revealed the **bug is mechanical**: Gemini 2.5 Flash spends "thinking tokens" against `maxOutputTokens`, so an 8-token cap leaves zero tokens for the visible response, producing empty text with `finishReason: MAX_TOKENS`. With `maxOutputTokens=64` (or `thinkingConfig.thinkingBudget=0`), the same prompts return a valid integer score. The empty-response gemini_flash failures are mechanically rescuable; whether to do so is a budget question (1,478 calls). Skipped per cost constraint after verifying the §4.6.2 gradient cells (Spec-effect 7-judge sensitivity values) are NOT affected by the gemini_flash gap (zero unrescued gemini_flash failures on `C5_baseline`, `C2a_full_spec`, `C2c_wrong_spec`, `C4`, or `C4a` conditions). This audit consumed **18 new judge API calls** (10 gemini_flash pilot + 5 gemini_pro pilot + 3 gemini_flash debug calls). 482 calls remain in budget; not used.

6. **Back-check 35 PASS.** 30 §4.1 gradient cells (5 conditions × 6 subjects) + 5 §4.4.1 memory-system controlled all-14 aggregates independently recomputed from raw judgments + S114 backfills. **35/35 within ±0.01 tolerance** (every cell drift ≤ 0.001). The 5-judge primary panel scaffolds for §4.1 and §4.4.1 are mechanically reproducible. Detail in `back_check_30_20260507.csv` + `back_check_30_extra_20260507.csv`.

---

## Parse-failure inventory

### Counts

- Total failure rows scanned: **5,267**
- Rescued by S114 backfills (2026-05-05): **2,744** (52.1%)
- Unrescued: **2,523**

### By judge (rescued / unrescued)

| Judge | Total failures | Rescued | Unrescued |
|---|---:|---:|---:|
| gpt4o | 1,541 | 1,332 | 209 |
| gpt54 | 1,527 | 1,318 | 209 |
| gemini_flash | 1,478 | 0 | 1,478 |
| haiku | 242 | 33 | 209 |
| sonnet | 240 | 31 | 209 |
| opus | 239 | 30 | 209 |

### By failure class (rescued / unrescued)

| Class | Total | Rescued | Unrescued |
|---|---:|---:|---:|
| http_429 | 2,909 | 2,588 | 321 |
| empty_response | 2,026 | 0 | 2,026 |
| no_score_extracted | 183 | 153 | 30 |
| http_403 | 146 | 0 | 146 |
| out_of_range | 3 | 3 | 0 |

The S114 backfill was effective on http_429 (89% rescue rate) and no_score_extracted (84%). It was zero-effective on http_403 and empty_response, both of which are gemini_flash failure modes.

### Files

- Inventory CSV: `docs/research/parse_failure_inventory_20260507.csv` (5,267 rows, columns: subject, condition, question_id, judge, judgment_file_path, failure_class, score, raw_response_excerpt, s114_backfill_rescued)
- Impact CSV: `docs/research/parse_failure_impact_20260507.csv` (43 unrescued cells, severity-classified)

---

## Impact on paper claims

### Severity P0: load-bearing drift

#### **§4.4.4 Keckley Q21 case-study table (line 1438-1439). NEW DRIFT, found by this audit.**

| Source | BL C1 | BL C3 | BL Δ |
|---|---:|---:|---:|
| **Paper v11.8 line 1438-1439** | **2.0** | **0.6** | **−1.4** |
| 3-judge subset (haiku/sonnet/opus, pre-backfill) | 3.33 | 1.00 | −2.33 |
| 5-judge primary panel with S114 backfills (canonical) | 3.4 | 1.2 | −2.2 |
| `_v11_emit/4_4_2_4_4_3.json` `4_4_3_keckley_q21_baselayer_*` | 3.4 | 1.2 | −2.2 |
| `docs/research/baselayer_c1_vs_c3_paired_analysis.md` line 40 | 3.33 | 1.00 | −2.33 |
| **v11.2 paper draft line 1582** ("BL C1 ≈ 3.4-3.6, Δ −2.2") | ~3.4 | — | −2.2 |

The paper's footnote `[^baselayer-q21-judges]` (line 1444) says coverage is 3 judges (Haiku, Sonnet, Opus). With S114 backfills overlaid, **all 5 primary judges have valid scores on BL Q21** — the footnote is also stale. Primary-panel coverage is complete; the v11.2 draft used the 5-judge mean correctly.

**No 2-judge / 3-judge / 4-judge / 5-judge subset of the available judge scores produces 2.0 / 0.6.** The numbers do not appear in any data file. They appear to be a manual data-entry error introduced between v11.2 (when the §4.4.4 walk apparently transcribed the correct 5-judge values) and v11.8.

**Stress-tested via four independent paths:**
1. Fresh re-emit of `_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py`: produces 3.4 / 1.2 / −2.2.
2. Direct recompute from per-judge files + `_s114_backfills/` (haiku=5, sonnet=2, opus=3, gpt4o=3, gpt54=4 for C1; haiku=1, sonnet=1, opus=1, gpt4o=2, gpt54=1 for C3): mean = 3.4 / 1.2 / −2.2.
3. v11.2 paper draft (line 1582) used the same numbers: "Base Layer's substrate, both at C1 ≈ 3.4-3.6 on the 1-5 rubric, with Δ on Q21 of −2.0 and −2.2 respectively".
4. Question-id alignment verified: paper line 1423 matches `baselayer_results.json` Q21 verbatim ("How does Elizabeth explain her decision not to visit her mother's grave"); held_out_passage matches paper line 1425.

**Suggested fix (Aarik to apply during §4.4.4 walk):**

- Update line 1438-1439 to:
  ```
  | Base Layer | 3.4 | 1.2 | **−2.2** |
  ```
- Drop footnote `[^baselayer-q21-judges]` line 1444 (the 3-judge coverage note is stale; full 5-judge primary coverage exists post-S114 backfill).
- Update line 1448 narrative:
  - "C1 was speculating productively (**3.6 and 2.0** respectively)" → "(**3.6 and 3.4** respectively)"
  - "near-floor (**1.6 and 0.6**)" → "(**1.6 and 1.2**)"
  - Both replacements preserve the analytical reading: SM and BL both had productive C1 baselines that the Spec converted to near-floor.

### Severity P1: case-study cells where the §4.4.4 narrative may need a small touch-up

(Same line-1448 narrative as above; the SM number is already correct.)

### Severity P2/P3: documented gaps

The 209 unrescued primary-judge failures per judge are concentrated on cells already documented in the paper as gaps:

1. **Bābur C9_raw_corpus_plus_spec (38 questions × 5 primary judges = 190 cells):** documented at paper line 366, 990, and 2470 as context-window omission. No action needed.
2. **`C1_<system>_fullpipeline` Supermemory cells (4 subjects × ~variable questions):** documented at paper line 1304 footnote `[^supermemory-native-coverage]` as paid-tier rerun failures. No action needed.
3. **`C1_mem0_fullpipeline` Ebers (2 questions):** small undocumented gap; affects Mem0 native aggregate by ≤ 0.01.

### gemini_flash failures (1,478 cells unrescued; 7-judge sensitivity panel only)

The 7-judge sensitivity panel adds Gemini Flash + Gemini Pro to the primary 5. The §3.6 panel calibration claims (α = 0.659 primary / 0.535 7-judge) compute over the cells with valid scores; missing gemini_flash cells reduce the effective n for the 7-judge α but do not bias the calculation. No action needed on these for v11.8 freeze, but worth a single-line acknowledgment in §3.6 if the 7-judge α gets re-emphasized.

The empty_response failure mode for gemini_flash is systematic across 25+ subject-condition cells; pilot rerun on one cell would establish whether it's an API-key permission issue or content-filter issue, but is not necessary for the paper's primary-panel claims.

---

## Reruns executed

**Total new API calls:** 18 (10 gemini_flash pilot + 5 gemini_pro pilot + 3 gemini_flash debug).
**Calls saved:** ~1,478 (avoided full gemini_flash rerun by establishing the bug is mechanical and §4.6.2 gradient coverage is clean).

The S114 backfill (2026-05-05) already exhausted the actionable rerun budget on cells that affect 5-judge primary panel claims. The remaining 209 unrescued primary-judge failures per judge are concentrated on already-documented gaps (Babur C9 omission, SM paid-tier failures). Pilot reruns on gemini empty-responses with the original `maxOutputTokens=8` parameter returned 0/15 successes; the diagnostic call established the issue is the thinking-token bug. Decision: do not consume budget on a rerun that does not move any v11.8 primary-panel paper number.

### Gemini 2.5 thinking-token bug — diagnosed but not patched

**Bug location:** `scripts/backfill_all_parse_failures.py` line 137 — `'generationConfig': {'temperature': 0, 'maxOutputTokens': 8}` for Gemini calls.

**Root cause:** Gemini 2.5 (Flash + Pro) spends thinking tokens against `maxOutputTokens`. An 8-token cap leaves zero tokens for visible output. Response is empty; `finishReason: MAX_TOKENS`.

**Fix (one-line):** Either bump `maxOutputTokens` to ≥ 16 (with the prompt's "ONLY a single digit" instruction, the model spends ~3-7 thinking tokens and 1 output token); or add `'thinkingConfig': {'thinkingBudget': 0}` to disable thinking entirely.

**Rerun yield:** Pilot established 0/10 rescue at `maxOutputTokens=8` and 1/1 rescue at `maxOutputTokens=64`. A full-batch rerun with the fix would likely rescue most of the 1,478 gemini_flash failures + 111 gemini_pro failures.

**Impact:** Affects only the 7-judge sensitivity panel. The primary 5-judge panel does not include Gemini, so no §4.1 / §4.2 / §4.3 / §4.4 paper claim depends on these cells. The §4.6.2 7-judge sensitivity table (lines 1548-1552) reports +0.45 / +0.17 / −0.21 — these are computed on gradient conditions (C5, C2a, C2c, C4a) and the inventory CSV confirms zero unrescued gemini_flash failures on gradient conditions. So §4.6.2 is unaffected even at the current degraded gemini coverage. The 7-judge α = 0.535 (line 499) is computed across all conditions including memory-system; that value would shift if a full gemini rerun were executed, but α is not a paper-headline number — it's a sensitivity check noted alongside the primary α = 0.659.

**Recommendation:** Apply the patch. Run a full gemini batch rerun post-arXiv-launch (one-off, 1,500 calls, ~$1.50 at Gemini Flash pricing). Update §4.6.2 + §3.6.2 7-judge α if any directional claim moves. Not launch-blocking.

---

## Back-check 30 numerical claims

**Scope:** 30 paper numbers in the audit's VERIFIED list whose source is `_v11_emit/4_1_gradient.json` — the §4.1 gradient table cells. The 2026-05-05 audit verified these cells against the scaffold; this back-check verifies the scaffold against raw judgment files (with S114 backfills overlaid). Detail in `back_check_30_20260507.csv`.

**Selection:** 5 gradient conditions (C5_baseline, C2a_full_spec, C2c_wrong_spec, C4_factdump, C4a_full_facts_plus_spec) × 6 subjects (hamerton, sunity_devee, ebers, fukuzawa, keckley, augustine — covering low-baseline, mid-baseline, and Hamerton).

**Result: 30 of 30 within ±0.01 tolerance.** Every cell drift is 0.0; the scaffold is exactly reproducible from raw data. Per-question 5-judge mean → mean across questions matches the v11_emit scaffold to two decimal places.

| Cell | Scaffold | Recomputed | Drift |
|---|---:|---:|---:|
| Hamerton C5 | 1.26 | 1.26 | 0.00 |
| Hamerton C4a | 2.77 | 2.77 | 0.00 |
| Sunity Devee C5 | 1.03 | 1.03 | 0.00 |
| Sunity Devee C4a | 2.41 | 2.41 | 0.00 |
| Ebers C5 | 1.02 | 1.02 | 0.00 |
| Ebers C4a | 2.07 | 2.07 | 0.00 |
| Fukuzawa C5 | 1.67 | 1.67 | 0.00 |
| Fukuzawa C4a | 2.78 | 2.78 | 0.00 |
| Keckley C5 | 1.84 | 1.84 | 0.00 |
| Keckley C4a | 2.44 | 2.44 | 0.00 |
| Augustine C5 | 2.58 | 2.58 | 0.00 |
| Augustine C4a | 2.70 | 2.70 | 0.00 |
| ... (all 30 cells, all 0.00 drift) | | | |

**Reading:** The §4.1 gradient is mechanically clean. The 2026-05-05 audit's claim that this section is reproducible was correct, and the underlying scaffold is consistent with raw data when S114 backfills are applied.

### Extension: 5 §4.4.1 memory-system aggregate cells (`back_check_30_extra_20260507.csv`)

| Cell | Scaffold | Recomputed | Drift |
|---|---:|---:|---:|
| 4_4_1_baselayer_substrate_controlled_all14_delta | 0.0864 | 0.0864 | 0.0000 |
| 4_4_1_letta_archival_controlled_all14_delta | 0.1979 | 0.1989 | 0.0010 |
| 4_4_1_mem0_controlled_all14_delta | 0.1212 | 0.1212 | 0.0000 |
| 4_4_1_supermemory_controlled_all14_delta | 0.0399 | 0.0399 | 0.0000 |
| 4_4_1_zep_controlled_all14_delta | 0.1864 | 0.1864 | 0.0000 |

5 of 5 within ±0.01 tolerance. The §4.4.1 controlled all-14 deltas (paper line 1294-1302) recompute exactly from raw judgments + S114 backfills.

**Total back-check 35 of 35 PASS.** Combined with the audit doc's hand-verification of §4.4.1 retrieval-overlap subset cuts (the 35.9%/65.6% bug class), the §4.1 + §4.4.1 + scaffold-derived numerical surface is in clean shape.

The §4.4.4 BL Q21 finding above (paper 2.0 / 0.6 / Δ = −1.4 vs. data 3.4 / 1.2 / Δ = −2.2) is on a case-study cell that is NOT in the §4.1 gradient or §4.4.1 aggregate scaffolds. It is a paper transcription error on a per-case-study row, distinct from the scaffold-coverage class this back-check exercises.

---

## Open items requiring Aarik decision

1. **§4.4.4 line 1438-1439 BL Q21 fix.** Apply the 3.4 / 1.2 / −2.2 correction or a different reconciliation. Suggested wording above.
2. **Footnote `[^baselayer-q21-judges]` removal.** Once corrected to the 5-judge primary, the 3-judge coverage note is stale.
3. **§4.4.4 line 1448 narrative consistency.** "C1 was speculating productively (3.6 and 2.0 respectively)" → "(3.6 and 3.4 respectively)"; "near-floor (1.6 and 0.6)" → "(1.6 and 1.2)".
4. **Minor: `C1_mem0_fp` Ebers 2 questions.** Tiny gap; flag in §4.4.1 line 1304-style footnote if §4.4.1 native Mem0 numbers ever get reprinted.

---

## Process notes

- The 2026-05-05 audit explicitly disclaimed (line 348) that it could not catch errors in raw judgment files. The §4.4.4 BL Q21 drift this audit found is not in the raw judgment files; it is in the paper itself. Both audits are needed; they catch different error classes.
- **Source-of-truth reconciliation rule:** for every primary-panel number in §4.1, §4.2, §4.4, the canonical source is `_v11_emit/*.json` (which overlays S114 backfills). The merged `*_judgments_merged.json` files are stale relative to backfills and should NOT be used for paper-number reconciliation. The audit's mistake on Keckley Q21 was a result of reading merged files directly.
- **The audit's mechanistic discipline** (figure / number checks via re-runnable scripts, per Aarik's directive 2026-05-07) would catch this class of error. Building `scripts/recompute_paper_numbers.py` per the audit doc's Addendum 2026-05-07 is the right Phase 0 follow-up.

---

## Files produced by this audit

### Primary deliverables (per task spec)

- `docs/research/parse_failure_inventory_20260507.csv` — per-(subject, condition, question_id, judge) failure inventory, 5,267 rows
- `docs/research/parse_failure_impact_20260507.csv` — 43 unrescued cells, severity-classified
- `docs/research/mechanistic_audit_summary_20260507.md` — this file

### Supporting artifacts

- `docs/research/back_check_30_20260507.csv` — 30 §4.1 gradient cells, all PASS
- `docs/research/back_check_30_extra_20260507.csv` — 5 §4.4.1 memory-system cells, all PASS
- `docs/research/_audit_20260507_remaining_work.json` — backfill state snapshot (215 manifest cells, 88 rescued, 37 partial, 90 never-attempted)
- `docs/research/_audit_20260507_actionable.json` — actionable-rerun candidate list
- `docs/research/_audit_20260507_gemini_pilot.json` — gemini_flash 10-call pilot (0/10 rescue at maxOutputTokens=8)
- `docs/research/_audit_20260507_gemini_pro_pilot.json` — gemini_pro 5-call pilot (0/5 same root cause)

### Scripts (preserved for reproducibility; underscore-prefixed to denote audit-internal)

- `scripts/_audit_20260507_state.py` — initial backfill-state assessment
- `scripts/_audit_20260507_judge_breakdown.py` — per-judge unrescued breakdown
- `scripts/_audit_20260507_actionable.py` — actionable-cell identification
- `scripts/_audit_20260507_keckley_q21_check.py` — Q21 raw judgment check
- `scripts/_audit_20260507_keckley_full.py` — Q21 5-judge primary recompute
- `scripts/_audit_20260507_bl_subsets.py` — exhaustive BL Q21 subset enumeration
- `scripts/_audit_20260507_q21_alignment.py` — Q21 question-id verification across files
- `scripts/_audit_20260507_build_inventory.py` — emits inventory CSV
- `scripts/_audit_20260507_build_impact.py` — emits impact CSV
- `scripts/_audit_20260507_back_check_30.py` — §4.1 gradient back-check
- `scripts/_audit_20260507_back_check_441_45.py` — §4.4.1 + §4.5 back-check
- `scripts/_audit_20260507_back_check_extra.py` — emit structure inspector
- `scripts/_audit_20260507_babur_c9_check.py` — Babur C9 response coverage
- `scripts/_audit_20260507_babur_c9_responses.py` — Babur C9 response shape
- `scripts/_audit_20260507_gemini_pilot.py` — gemini_flash empty-response pilot
- `scripts/_audit_20260507_gemini_pro_pilot.py` — gemini_pro empty-response pilot
- `scripts/_audit_20260507_gemini_debug.py` — gemini API smoke test
- `scripts/_audit_20260507_gemini_debug2.py` — diagnosed thinking-token bug
- `scripts/_audit_20260507_gemini_gradient_check.py` — gemini gradient coverage check
- `scripts/_audit_20260507_hamerton_debug.py` — Hamerton load debug
