# v11 Release-Freeze Status, 2026-04-25

Closure record for the 2026-04-25 release-freeze pass. v10 paper draft (`docs/beyond_recall_v10_1_draft.md`) is ready for arXiv submission. v11 mechanistic-check architecture compliance gaps are deferred to post-arXiv v11+ work and are catalogued in `docs/research/v11_emit/_ARCHITECTURE.md` §12.

## Closure actions taken today

- **Panel-completeness waivers expanded** to cover all four cluster classes (GPT-5.4 wrong-spec-v2 across 13 subjects, §4.4 Base Layer C1/C3 936 records, §4.2 Bernal Diaz C8/C9 78 records, §4.5 Letta Hamerton 39 records). Audit now GREEN on all 441 unwaived rows. Waivers file: `docs/research/v11_panel_completeness_waivers.json`.
- **Tier 1 paper edits applied** (silent cleanup of running-list placeholders that never reached published paper cells; 14 reconciliation-diff sign flips closed at the running-list level with zero v10 paper-text sign flips remaining).
- **Tier 2 paper edits applied** (minor numeric drift cells: §4.2.1 pairwise comparison counts, §4.2 per-subject compression ratios, §4.5 main result table cells, §4.5 named-entity counts including Babur Letta 540 → 416, Appendix B.4 REFUSAL_TRIGGERING mean Δ, Appendix B.6 Δ_spec range max, Appendix D.3.2 abstention pct).
- **Tier 3 paper edits applied** (substantive author decisions: §4.3 random-derangement aggregate +0.22 → +0.15 cascaded across §1.3, §4.3 line 892, §4.6.2 line 1325, §5 summary line 1374; §4.4.2 Supermemory mixture counts updated to 5-judge primary panel with paired_total_n 507/516 → 546 and helps/hurts 37/52 → 57/53 and mean swings +1.45/−1.41 → +1.55/−1.38; §4.4.1 Letta archival "Subjects improved (of 9)" 9/9 → 8/9 and Mem0 native 9/9 → 7/9 verified against scaffold).
- **§4.6.1 Tier 2 cross-provider replication demoted to direction-only** with sensitivity ranges. Published magnitudes could not be reproduced under any aggregation tested. Directional claim (5 of 6 cells reproduce the spec direction across non-Anthropic response models) retained. No specific magnitudes carry through as primary results pending a dedicated `_v11_emit_tier2.py` scaffold (post-arXiv).
- **§4.1 sensitivity status verified.** `docs/research/v11_emit/4_1_gradient.json` regression-summary numbers (Δ-on-C5 slope −0.96, R² = 0.82, p < 1e-5; level regression C4a~C5 slope +0.04, R² = 0.008, p = 0.76) match v10 paper text at lines 749, 751, 1372 within rounding. The reconciliation diff entries flagging "paper = -0.67" and "paper = 0.95" for these claims are stale running-list extractions, not paper-text claims. No §4.1 body-table or paper-text rebuild required.
- **Legibility blockers fixed** (paper-text reframing prose at line 749 confirmed correct; 8-of-14 paper-text confirmations done directly against v10 file before any cell-level edits applied).

## Pass 3 (evening of 2026-04-25)

Paper version bumped v10 → v10.1. Manuscript paths: `docs/beyond_recall_v10_1_draft.md` + `.docx`. Triggered by a fresh GPT-5.5 review of v10.1 at `docs/reviews/v10_1_review_gpt55_20260425.md` (verdict NEEDS_REVISION pre-fix; addressed in this pass).

**Four critical contradictions resolved:**

1. **§4.1 battery-generator wording corrected.** All 14 main-study batteries are Haiku-generated; subset regression is drop-Hamerton, not "restrict to GPT-5.4". Verified by direct reads of `metadata.model` across `results/global_<subject>/battery_v2.json` for every global and `data/hamerton/battery.json`. Verifier: `scripts/_v11_validation/verify_4_1_sensitivity.py` (all numbers reproduce within rounding).
2. **Tier 2 response-model count corrected to 2** (Sonnet 4.6 + Gemini 2.5 Pro). Opus and GPT-5.4 are Tier 2 judges only; Tier 2 batteries are GPT-5.4-generated. Propagated through §1.2, §1.3, §5.2, §6.2. Verified by file enumeration under `results/_tier2/`.
3. **§4.3 wrong-spec denominator disambiguated.** 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). Disambiguated in §1.3 and §4.3. Verified against `docs/research/wrong_spec_detection_raw.json`.
4. **§4.4.2 Table 4.6 rebuilt on strict 5-judge primary panel** (entire table, not just Aggregate Δ). Recompute script: `scripts/_table_4_6_5judge_recompute.py`. All 8 rows updated; no sign flips; Aggregate Δs shrink by 0.01 to 0.06; Letta and Hamerton n drops to 38 under strict rule. Closes Tier 3 author-decision item #6 from the table-rebuild proposal.

**Revision items applied:**

- §1.4 and §5.3 living-user wording: "expected by construction" → "closest available proxy".
- §4.1 and §5.5: "C4a ceiling" → "post-spec operating level".
- §5.2 H5 reframed to credit fact extraction.
- §4.4 "3 of 4 commercial systems" nuanced.
- §4.6.1 "not Haiku-specific" softened to "small probe reduces likelihood".
- v10 / v11 nomenclature in paper prose: "v11 mechanistic-check audit" → "verification audit".

## Sign-off

Release-freeze pass 1 + 2 + 3 complete for arXiv submission. Pass 3 closes the four critical contradictions surfaced by the fresh GPT-5.5 review of v10.1; remaining items it flagged (human validation, component ablation, hierarchical modeling) are post-arXiv v11+ work. v11 architecture compliance gaps (schema noncompliance of all eight emit scripts, hardcoded PAPER_* dicts, no SHA manifests, no claim-tag injection, no full numeric-literal census, no §4.6.1 emit script, legacy non-v11 scripts not yet upgraded) remain deferred to v11+ post-arXiv. Estimated effort: 80-100 hours total.

## Pointers

- Scaffolding review: `docs/reviews/v11_scaffolding_review_gpt55_20260425.md` (GPT-5.5, 2026-04-25). Verdict: architecture is the right direction; the representative emit and the reconciliation pipeline do not yet satisfy the contract.
- Table rebuild proposal: `docs/research/v11_table_rebuild_proposal.md` (per-table walkthrough across §3, §4.1, §4.1.2, §4.2, §4.2.1, §4.3, §4.4.1, §4.4.2, §4.4.3, §4.5, §4.6.1, §4.6.2, App B.2-B.4, App D.1-D.4 with Tier 1 / Tier 2 / Tier 3 apply order).
- Reconciliation diff: `docs/research/v11_reconciliation_diff.md` (1,509 claim_ids; 1,089 MATCH / 65 MINOR / 206 SUBSTANTIVE before today's pass; cleared by Tier 1+2+3 edits).
- Panel-completeness waivers: `docs/research/v11_panel_completeness_waivers.json`.
- Architecture spec with status section: `docs/research/v11_emit/_ARCHITECTURE.md` §12.
- Diagnostic for the GPT-5.4 batch failures: `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md`.
- Judge-call controls implementation: `docs/reviews/v11_judge_call_controls_implementation_20260425.md`.

---

## Pass 4 (v11 active editing 2026-04-27)

Pass 4 covers the v11 comment-walk that began 2026-04-27 on top of the v10.1 release-frozen baseline. **v11 is an active edit branch, not a release-pass closure.** v10.1 remains the citable canonical paper at `docs/beyond_recall_v10_1_draft.md`; v11 lives at `docs/beyond_recall_v11_draft.md` and will not become canonical until a future release pass closes the comment-walk and re-runs the reconciliation diff against the v11 manuscript.

**Inputs.** 183 review comments captured in `docs/reviews/v11_comments_extracted_20260427.md`, indexed at `docs/reviews/v11_comment_index.json` with 10 Bavani structural items (B1-B10) plus 173 docx comments (C1-C173). Query helper: `scripts/query_v11_comments.py`. Running log: `docs/reviews/v11_running_changes_log_20260427.md`.

**Items applied (~32 of 183 as of 2026-04-27 evening):**

- **Bavani structural notes B1-B10** applied. B3 (Table 2.1) deferred to Aarik. Highlights: §1.1 hypothesis statement rewritten to mirror terms-of-art (representational accuracy + interpretation); §1.3 Pattern 1/2/3 headers promoted; §2.2 worked example (Sunity Devee A2 -> F-73 / F-414) added; §3.1 retitled "Operationalizing representational accuracy"; new Appendix G Glossary built (9 terms-of-art entries with §1.1 forward pointer); §3.7.3 cross-anchor interpretation rule fully bolded.
- **Docx comments C1-C15** (§1.1 + §1.2 layman pass): vendor recall range "68% to 85%" -> "70% to 93%"; "shown to a response model" expanded to "shown to a response model, the language model being asked to respond"; "win rate" rebranded to "per-question improvement rate" globally; H5 reframed to credit fact extraction; aggregation rule expanded to "each judge's per-question scores are first averaged to a per-judge per-subject mean, then averaged across the five judges"; rubric paragraph rewritten to set up the cross-anchor rule with the 1.8 -> 2.4 example; Tier 2 layman motivation added.
- **Docx comments C16-C52** (§1.3 v5 + §1.4 v2 wholesale rewrites):
  - **§1.3 v5 lede** "Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least."
  - Bulleted highlights covering gradient / category-shift / compression / content-specificity / memory-system layering / hedging.
  - **C2a 70.9% per-question improvement rate** distinguished from **C4a 78.6%** explicitly.
  - **55.0% anchor-crossing rate** (low-baseline 351 responses) added.
  - **Per-system anchor-crossing range (20-36%)** folded into the Memory-system layering bullet.
  - Multi-anchor wins (1 -> 3, 1 -> 4) explicitly named.
  - **§1.4 retitled "What this implies"** (was "Why the gradient matters"). "What we did not prove" disclaimer paragraph removed entirely. Population framing pivoted to "anyone who uses an AI system" / "broad technology like email or cell phones" / 99% of real AI users sit at the frontier-low-baseline floor; autobiographers reframed as the closest available imperfect proxy.
- **C56 / C57:** §2 reordered. §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1; final order §2.1 -> §2.2 Memory systems for LLM agents -> §2.3 Traceability -> §2.4 Cognitive and representational foundations -> §2.5 LLM-as-judge.
- **C66 / C71:** §3 reorder. §3.6 weakest-model rationale compressed to two sentences. §3.7 reordered: §3.7.1 Judge panel -> §3.7.2 Fractional score interpretation (was v10.1 §3.7.3) -> §3.7.3 Calibration (was v10.1 §3.7.2) -> §3.7.4 Inter-judge agreement -> §3.7.5 Aggregation -> §3.7.6 Rubric-handling.
- **C99 / C124:** §4 restructure. §4.1.1 Franklin (v10.1 high-baseline reference) moved to §4.6.4 under sensitivities. §4.7 closing paragraph added bridging into §5.
- **C139 / C140 / C153 (load-bearing reframe):** "Additivity" replaced with **"interaction with retrieval"** throughout §1.3 / §4.4 / §5.2 / §5.4. The per-question Pattern 1/2/3 framing (interpretation supply on under-determined questions / over-theorization on literal-recall questions / principled refusal where retrieved facts cannot ground a prediction) is now the load-bearing description of M2; aggregate Δs are characterized as small and informative only as the balance of those patterns. M2 finding direction is unchanged; the explanatory frame shifts. Supermemory deep-dive collapsed into §4.4.2; aggregate paragraph kept in §4.4.1 with §4.4.2 pointer.
- **C162:** §1.2 conditions table C2c row long parenthetical (deterministic fixed pairing / mapping / v2 random derangement / Hamerton-Franklin variant) pulled to footnote `[^c2c-construction]`.
- **Per-system anchor-crossing analysis (closes C131):** `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. Low-baseline upward anchor-crossing rates: Mem0 23.4% controlled / 36.1% native; Letta archival 26.9% / 19.9%; Zep 27.9% / 32.5%; Supermemory 20.2% / 23.4% (partial native coverage, 7 of 9 subjects); Base Layer 29.0% controlled. Folded into v11 §1.3 Memory-system layering bullet and v11 §4.4.1.

**Population-of-relevance language sweep** (consequence of §1.4 v2 framing change): "real living users" -> "the typical AI user falls into, since most users' reasoning is not in any training corpus" (§3.2.1 line 281); "real AI users" -> "typical AI users" (§5.1 line 1386). Other §5 / §6 / §7 mentions still on the queue.

**Reviews of the post-C16-C52 draft (2026-04-27):**

- `docs/reviews/v11_post_comments_review_gpt55_20260427.md` (GPT-5.5)
- `docs/reviews/v11_post_comments_review_gemini_pro_20260427.md` (Gemini Pro)

**Numerical status.** Headline numbers carry forward unchanged from v10.1: slope **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001; Wilcoxon C5 vs C4a W=11, p=0.007; low-baseline mean Δ_C4a = +0.89; all-14 mean Δ_C4a = +0.55; wrong-spec C2a +0.35 / v2 +0.15 / v1 −0.25; Letta n=3 stateful-agent Δs (Hamerton +0.14 / Ebers +1.05 / Babur +0.54). DATA_REFERENCE.md and PROVENANCE_INDEX.md remain anchored to v10.1's 5-judge primary panel; both files now carry a v11 section-number-mapping note. v11 reframing items applied so far are framing-level only; no reaggregation has been triggered.

**Pending (~150 of 183 items).** Tracked in the running log. Highest-volume clusters: figure walkthroughs (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173) pending Aarik direction; ~100 wording-level annotations (Part F equivalent) on §4 prose; section-reference audit needed once §2 / §3.7 / §4.6 reorders fully stabilize.

**Sign-off.** Pass 4 is an active-editing checkpoint, not a release-pass closure. v10.1 remains release-frozen and citable. The next release-pass closure for v11 will require: (a) comment-walk completion or explicit deferral of remaining items; (b) reconciliation diff regenerated against the v11 manuscript; (c) panel-completeness audit re-run if any condition rows changed; (d) a fresh cross-LLM review of the rebuilt v11.
