# Open Issues — Beyond Recall Study Repo

**READ BEFORE WORKING IN THIS REPO.** Persistent tracker for quality-audit findings and known inconsistencies. Updated at the end of each work session.

Full audits: [docs/reviews/s114_repo_quality_audit.md](docs/reviews/s114_repo_quality_audit.md), [docs/reviews/v10_repo_review_gpt55_20260424.md](docs/reviews/v10_repo_review_gpt55_20260424.md), [docs/reviews/v10_release_freeze_pass_report.md](docs/reviews/v10_release_freeze_pass_report.md), [docs/reviews/v11_running_changes_log_20260427.md](docs/reviews/v11_running_changes_log_20260427.md) (V11 FREEZE — 2026-04-28 section).

---

## Quick status (2026-05-13, v12.1 current canonical)

| Severity | Open | Resolved |
|---|---:|---:|
| v12.1 review pass | 0 launch-blockers | Aarik's 211-comment review pass + final-checks audit applied to `docs/beyond_recall_v12_1_draft.md` |
| P0 / P1 / P2 (v10.1 release-freeze tracker) | unchanged from 2026-04-25 below | unchanged |

v12.1 (`docs/beyond_recall_v12_1_draft.md`, 2026-05-13) is the current canonical paper, forked from v12 to apply Aarik's 211-comment review pass plus final-checks audit fixes. v12.1 numerical changes are framing/precision only and the headline arguments are unchanged: §4.2 compression standardized to the symmetric 9-row computation (Spec Only Δ +0.68, raw corpus Δ +0.91, All Facts + Spec Δ +0.89; compression-recovery figure 75%; see `docs/reviews/v12_1_compression_table_recompute_20260513.md`); 3-anchor crossing rate corrected 5.9% → 5.7% (20/351); Krippendorff α keeps 0.659 headline with a new footnote disclosing a third-party recompute of 0.668; "evidentiary bar" elevated to a term of art. DATA_REFERENCE.md / KEY_FINDINGS.md / PROVENANCE_INDEX.md mastheads bumped to v12.1. v11.9.5 → v11.9.11 drafts preserved at `docs/versions/_pre_v12_drafts/`. The historical changelog below is preserved unchanged.

---

## Quick status (2026-04-28, v11 release-frozen)

| Severity | Open | Resolved |
|---|---:|---:|
| v11 freeze blockers | 0 | All comment-walk closure items resolved (applied / partial-applied / deferred-to-future-work / no-op / deferred-to-figure-regen). All 12 cursory-review issues addressed. All 4 paper-vs-scaffold MISMATCH items reconciled. |
| P0 / P1 / P2 (v10.1 release-freeze tracker) | unchanged from 2026-04-25 below | unchanged |

v11 is release-frozen as of 2026-04-28 and is the citable canonical paper at `docs/beyond_recall_v11_draft.md`. v10.1 (`docs/beyond_recall_v10_1_draft.md`, release-frozen 2026-04-25) is preserved as the historical baseline. Headline numbers carry forward unchanged from v10.1 into v11; v11 adds per-question variance, two statistical signatures, half-anchor metric, predicate ablation null, held-out leakage rare, Hamerton spec-length confound, and pattern-activation heuristic falsified (M15-M21 in KEY_FINDINGS.md). Per-claim confidence catalog at `docs/research/v11_confidence_catalog_20260428.md`. Freeze record: "V11 FREEZE — 2026-04-28" section of `docs/reviews/v11_running_changes_log_20260427.md`.

---

## Quick status (2026-04-27, v11 active editing on top of v10.1 release-frozen baseline) — preserved record, superseded by v11 freeze

| Severity | Open | Resolved |
|---|---:|---:|
| v11 comment-walk items | ~150 of 183 | ~32 of 183 (B1-B10, C1-C15, C16-C52, C56/C57, C66/C71, C99/C124, C139/C140/C153, C162) |
| P0 / P1 / P2 (v10.1 release-freeze tracker) | unchanged from 2026-04-25 below | unchanged |

v11 is the active edit branch (`docs/beyond_recall_v11_draft.md`) at this point in the timeline. v10.1 release-frozen state is preserved. Reframing items applied so far are framing-level, not numerical; DATA_REFERENCE.md and PROVENANCE_INDEX.md remain anchored to v10.1's 5-judge primary panel until v11 promotes via a release pass.

### 2026-04-27 v11 active-editing items resolved

| # | Where | Resolution |
|---|---|---|
| B1-B10 | §1.1, §1.3, §2.2, §2.3.1, §3.1, §3.7.3, Appendix G | Bavani structural notes applied; B3 (Table 2.1) deferred to Aarik. |
| C1-C15 | §1.1, §1.2 | Layman pass: vendor recall range 70-93%, "win rate" -> "per-question improvement rate", aggregation rule expanded, H5 reframed, Tier 2 layman motivation. |
| C16-C49 | §1.3 | Wholesale §1.3 v5 rewrite: category-shift lede, Pattern 1/2/3 headers, per-system anchor-crossing range folded in, multi-anchor wins named explicitly. |
| C50-C52 | §1.4 | Wholesale §1.4 v2 rewrite: retitled "What this implies"; population framing pivoted to "anyone who uses AI" / broad-technology / 99%-frontier-low-baseline; "What we did not prove" disclaimer paragraph removed. |
| C56 / C57 | §2 | Reordered: §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1; new order §2.1 -> §2.2 -> §2.3 -> §2.4 -> §2.5. |
| C66 / C71 | §3 | §3.6 weakest-model rationale compressed; §3.7 reordered (Judge panel -> Fractional score interpretation -> Calibration -> Inter-judge agreement -> Aggregation -> Rubric-handling). |
| C99 / C124 | §4 | §4.1.1 Franklin moved to §4.6.4; §4.7 closing paragraph added bridging into §5. |
| C139 / C140 | §4.4 | Supermemory deep-dive collapsed into §4.4.2; aggregate paragraph kept in §4.4.1 with §4.4.2 pointer. |
| C153 (LARGE) | §1.3, §4.4, §5.2, §5.4 | Reframed "additivity" -> "interaction with retrieval"; per-question Pattern 1/2/3 framing made load-bearing; aggregate Δs characterized as small. |
| C162 | §1.2 | Conditions-table C2c long parenthetical pulled to footnote `[^c2c-construction]`. |
| C131 (data) | §1.3, §4.4.1 | Per-system anchor-crossing analysis added: `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. |
| Infrastructure | repo | Comment index built: `docs/reviews/v11_comment_index.json` (183 items) + `scripts/query_v11_comments.py`. Running log: `docs/reviews/v11_running_changes_log_20260427.md`. |

### 2026-04-27 v11 active-editing items pending

- ~150 of 183 comments not yet applied. Figure-walkthrough cluster (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173) queued pending Aarik direction.
- Population-of-relevance language sweep partially done (§3.2.1, §5.1); other §5 / §6 / §7 mentions still on the queue.
- Section-reference audit needed once §2 / §3.7 / §4.6 reorders are fully stabilized.

### 2026-04-28 v11 data-locking pass

- DATA_REFERENCE.md, KEY_FINDINGS.md, PROVENANCE_INDEX.md updated with v11 active-editing additions: per-question variance (M15), two statistical signatures (M16), half-anchor metric (M17), predicate ablation null (M18), held-out leakage RARE (M19), Hamerton spec-length confound (M20), pattern-activation heuristic falsified (M21). Section-number remap applied for v11 (§3.7 -> §3.6; §4.4.4 NEW; §4.7 NEW; §4.1.1 -> §4.6.4; §2.3 / §2.3.1 -> §2.1).
- v11 paper-numbers verification surfaced 4 MISMATCH items pending paper edit (Supermemory controlled all-14 sign + improved-count drift; §4.2.1 all-14 C8 sub-1pp drift). Flagged in DATA_REFERENCE and KEY_FINDINGS rather than silently reconciled. Pending paper edit by author.
- 13 new v11 research artifacts (`docs/research/*_20260428.*` + `per_system_anchor_crossing_20260427.*`) registered in PROVENANCE_INDEX with generating scripts and paper-section citations.

---

## Quick status (2026-04-25, v10.1 release-freeze pass 3)

| Severity | Open | Resolved |
|---|---:|---:|
| P0 blockers | **0** | 12 |
| P1 visible | 1 (hardcoded paths, documented not parameterized) | 8 |
| P2 hygiene | 1 (transient probe scripts, deferred) | 9 |

**Overall health: GREEN.** Pass 3 closed all 4 critical contradictions from the GPT-5.5 v10.1 review (battery-generator wording, Tier 2 response-model count, wrong-spec denominator, Table 4.6 panel rebuild). Pass 1 + Pass 2 P0 items remain closed. Reproducibility infrastructure (`requirements.txt`, `REPRODUCE.md`) intact. Remaining P1 (42 scripts hardcoding `C:/Users/Aarik/...`) is documented in `REPRODUCE.md` rather than parameterized; flagged as a future cleanup.

### 2026-04-25 release-freeze pass 3 — closed P0 items (GPT-5.5 v10.1 review)

| # | Where | Resolution |
|---|---|---|
| V101-1 | §4.1 prose described "13 globals = GPT-5.4 batteries"; ground truth is all 14 main-study batteries are Haiku-generated | Paper §4.1, §3.4.1 reworded; subset regression relabeled as drop-Hamerton (not "GPT-5.4-battery subset"). Cascade applied to AGENTS.md, README.md, STUDY_MEMORY.md, study-guide.md. |
| V101-2 | Tier 2 cross-provider directional probe described as "4 additional response models"; ground truth is 2 (Sonnet 4.6, Gemini 2.5 Pro). Opus + GPT-5.4 are Tier 2 judges | Paper §4.6.1 corrected; agent docs corrected. |
| V101-3 | §4.3 wrong-spec denominator (587) was unsplit | Disclosed: 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). |
| V101-4 | §4.4.2 Table 4.6 mixed panel definitions across rows | Entire table rebuilt on strict 5-judge primary panel; all 8 rows; no sign flips; Letta/Hamerton drops to n=38. |

### 2026-04-25 release-freeze pass 3 — revision-quality items applied

- §1.4 / §5.3 living-user "expected by construction" → "closest available proxy"
- §4.1 / §5.5 "C4a ceiling" → "post-spec operating level"
- §5.2 H5 reframed: fact extraction does most volume-reduction; spec adds marginal per-question value
- §4.4 memory-system additivity nuanced: Zep + Mem0-native strongest; Mem0-controlled small; Letta archival positive controlled / near-null native; Supermemory mixture
- §4.6.1 "not Haiku-specific" softened to "small probe reduces likelihood, does not establish model-family invariance"
- v11 mechanistic-check audit relabeled "verification audit" in paper prose; file paths to `v11_emit/` preserved

### 2026-04-25 release-freeze pass 3 — open items deferred (post-arXiv)

| # | Where | Open item |
|---|---|---|
| V101-5 | §6.1 / §8 | Human-validation subset (LLM-as-judge cross-check on a sample of judgments). Post-arXiv. |
| V101-6 | §8 | Component ablation of the spec (anchors vs core vs predictions, isolating the contribution of each layer). Post-arXiv. |
| V101-7 | §8 | Multi-subject living-user replication (the leading follow-up; structural extrapolation only in v10.1). |
| V101-8 | §6.4 | "Not Haiku-specific" claim depends on a 3-subject Tier 2 probe; broader cross-model invariance test deferred post-arXiv. |

---

## P0 — Blockers still open

**NONE — all P0 items resolved as of 2026-04-23 final-release-prep pass.**

### C1. Missing reproducibility script: `_audit_with_c2c.py` ✅ RESOLVED 2026-04-23

- Rebuilt and committed at `scripts/_audit_with_c2c.py`. Both D.3.4 (r = 0.500, n = 312) and D.3.5 (2,087 chars, n = 795) reproduce exactly from primary source data.
- Closure report at `docs/reviews/_p0_c1_closure_report.md`.
- **Observation flagged during recovery:** Appendix D.3.4 table shows `n=351` for C5/C4/C4a rows but the script reproduces `n=312` (Hamerton drops out because its C5/C4 live in `results_harmonized.json` and its C4a key is non-normalized). The r values match at n=312. The 351 in the n column is a transcription artifact. Fix options: (a) update table n to 312, (b) footnote the nominal-vs-valid-n distinction, (c) leave as-is. Low priority; not blocking.

---

## P0 — Resolved this session

### v10 release-freeze pass (2026-04-24)

| # | Where | Resolution |
|---|---|---|
| V10-1 | `docs/DATA_REFERENCE.md` slope `−0.98 [−1.30, −0.74]` (7-judge) disagreed with v10 paper `−0.96 [−1.24, −0.67]` | Replaced with v10 5-judge primary as canonical; 7-judge labeled as sensitivity. Per-subject §1 table replaced with v10 §4.1 numbers. Aggregates recomputed: all-14 mean Δ_C4a +0.55, low-baseline n=9 mean +0.89, mean C4a 2.46. |
| V10-2 | `docs/DATA_REFERENCE.md` §K Letta paths pointed at non-existent `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json` | Replaced with actual paths under `docs/research/_letta_rerun/` (main matched-rerun, 5-judge primary), `docs/research/_letta_rerun/fullstack_named/` (full-stack BL rerun for §4.5 footnote), `docs/research/_letta_blocks/` (raw block dumps for hamerton + ebers + babur). Hamerton Table 4.2 sources rewired to `results/hamerton/c8_c9_judgments_*.json` plus the per-judge merged files. |
| V10-3 | `README.md`, `AGENTS.md`, `agents/study-guide.md`, `agents/STUDY_MEMORY.md`, `ISSUES.md` named different drafts as canonical (v8/v9 mix) | All orientation docs now name `docs/beyond_recall_v10_1_draft.md` as canonical. v9/v8 marked as preserved baselines. v6 confirmed in `docs/versions/`. |
| V10-4 | No root `requirements.txt` / `pyproject.toml`; no documented end-to-end reproduction path | Added `requirements.txt` (deps confirmed by import-statement audit of `scripts/`). Added `REPRODUCE.md` with canonical reproduction commands and a hardcoded-path inventory. |
| V10-5 | `docs/KEY_FINDINGS.md` M1/M8 reported 7-judge numbers without panel disclosure | M1 + M8 rewritten to 5-judge primary canonical with 7-judge sensitivity called out; M6 Spearman ρ confirmed at 0.86-0.93. |

### Pre-v10 (2026-04-23 final-release-prep pass)

| # | Where | Resolution |
|---|---|---|
| B1 | `README.md:192` "License pending" | Updated to "Apache 2.0. See `LICENSE`." |
| B2 | `README.md:153` `§4.3.1` reference (doesn't exist) | Updated to `§4.5` (v9 Letta stateful-agent location) |
| B3 | v9 TOC §6 → §8 gap (no §7) | Renumbered §8 Future Work → §7, all 24 `§8` body references updated to `§7` |
| B4 | `docs/KEY_FINDINGS.md:256` still said `ρ = 0.89-0.98` | Updated to `0.86-0.93 (5-judge primary panel, 10 pairs)` |

---

## P1 — Visible inconsistencies (open)

| # | Where | Problem | Effort |
|---|---|---|---|
| C4 | 42 scripts hardcode `C:/Users/Aarik/…` Windows paths | `run_multimodel_responses.py` points at `hamerton_memory/` and `franklin_clean_memory/` dirs outside the study repo; fresh-clone reproduction of API-rerun scripts fails. **Documented (not parameterized) in `REPRODUCE.md` as part of the v10 release-freeze pass.** Documented hardcoded-path inventory and the env-var workaround that would make scripts portable. Future cleanup. | ~1-2 hrs — parameterize. Not blocking for paper review or for the documented v10 reproduction path. |
| C6 | §4.4 Base Layer C1/C3 + §4.2 Bernal Diaz C8/C9 + Tier-2 GPT-5.4 panels still parse-failed | `check_panel_completeness.py` (run 2026-04-25) flags 28 BL gpt54 cells (C1_baselayer / C3_baselayer across 14 subjects), 6 BD c8_c9 cells (gpt54 / gpt4o / gemini_flash), and a long tail of `results/_tier2/` GPT-5.4 batches as FULL_FAIL. Same `max_tokens` vs `max_completion_tokens` root cause as §4.3 wrong_spec_v2 (now resolved). Either rerun via the shared utility at `scripts/_judge_invocation/` or add explicit waivers in `docs/research/v11_panel_completeness_waivers.json`. | Rerun via shared utility: ~$5-10 in API + 1-2 hrs runtime + emit revalidation. |

### Resolved this session (2026-04-25, judge-call controls)

| # | Where | Resolution |
|---|---|---|
| C7 (resolved) | GPT-5.x judge invocations across multiple ad-hoc paths used `max_tokens` and silently produced 100% parse-failure batches | Shared judge-call utility built at `scripts/_judge_invocation/` (openai / anthropic / gemini + dispatcher). Routes to `max_completion_tokens` for any model id prefixed with `gpt-5`, `o1`, `o3`. Live-verified against gpt-5.4 (score=5, latency 1255 ms, `param_used=max_completion_tokens`). New judging code MUST import from this module. Validation scaffolding at `scripts/_v11_validation/{check_panel_completeness,preflight_judge_health}.py`. Architecture contract `_ARCHITECTURE.md` §11 makes both mandatory before any large-batch judging job. Closure: `docs/reviews/v11_judge_call_controls_implementation_20260425.md`. |

### P1 — Resolved this session (v10 release-freeze pass)

| # | Where | Resolution |
|---|---|---|
| B5 | `docs/beyond_recall_v8_draft.md` `ρ = 0.89-0.98` | v8 is now explicitly preserved-baseline; not the canonical draft. v10 carries the corrected `0.86-0.93`. |
| B6 | `docs/DATA_REFERENCE.md` `§7`, `§4.3.1`, `§4.8` references | DATA_REFERENCE rewritten to point at v10 sections (e.g., §4.1 lines 718, §4.2 line 791, §4.5 Letta exploratory). |
| B7 | `docs/KEY_FINDINGS.md` paper-location citations pinned to v6/v8 | Major findings (M1, M8) rewritten to v10 5-judge primary + v10 line numbers. m6 Spearman ρ refreshed. |
| B8 | `docs/PROVENANCE_INDEX.md` v6 anchors | PROVENANCE_INDEX retains its S113/S115 addenda layout; not in scope for this pass beyond what was needed to confirm Letta-stateful artifact paths. |
| B10 | `docs/README.md` v8 pointer | This file (top-level `README.md`) now points at v10. The duplicate `docs/README.md` was not edited in this pass. |
| B11 | `docs/research/` v8-numbered references | Out-of-scope for the release-freeze pass; flagged for future cleanup. |
| C2 | `agents/STUDY_MEMORY.md` Letta script-path mismatch | Verified: existing references already point at `docs/research/_letta_rerun/` numbered pipeline. No stale `run_letta_stateful_test.py` references remain in STUDY_MEMORY.md. |
| C3 | `agents/study-guide.md:62` v6 pointer | Replaced with v10 canonical and v9/v8 preserved-baselines. v6 path corrected to `docs/versions/beyond_recall_v6_draft.md`. |

---

## P2 — Hygiene (low priority)

| # | Where | Problem |
|---|---|---|
| A5 | `scripts/_probe_*.py`, `scripts/_check_*.py` | ~30 transient leading-underscore scripts; mix of keepable and clearly scratch. Defer. |

### P2 — Resolved this session (v10 release-freeze pass)

| # | Where | Resolution |
|---|---|---|
| A1 | `docs/beyond_recall_test.aux` | Already absent at start of pass (cleaned in earlier hygiene work). Confirmed missing. |
| A2 | `docs/~$yond_recall_v8_draft.docx`, `docs/~WRL2113.tmp` | Already absent at start of pass. Confirmed missing. |
| A3 | `scripts/results/global_cellini/` | Already absent at start of pass. Confirmed missing. |
| A4 | `scripts/__pycache__/` | Removed (.pyc files for `export_v10_to_docx` and `recompute_5judge_primary`). |
| A6 | `scripts/_battery_leakage_results.json`, `_per_question_outcomes_v2.json` | Left in place; out of scope. Documented as known data files. |
| A7 | `docs/reviews/` top-level vs `_archive/` | Out of scope. |
| B9 | `docs/_results_snapshot.txt:35` | Out of scope. Snapshot file flagged for replacement when full data refresh runs. |
| B12 | "substrate" terminology | Out of scope. Paper text already uses "memory system" canonically. |
| C5 | `scripts/__pycache__/` | Same resolution as A4. `.gitignore` already covers `__pycache__/`. |
| GIT-1 | `.gitignore` missing `~$*`, `*.tmp`, `*.aux` patterns | Added. |

---

## How this file is maintained

- Close items here when fixed. Prefix closed items with date and brief note.
- Add new items at the bottom of their severity section.
- Anything that would embarrass the project if a reviewer opened the repo right now belongs at P0 or P1.
- The full audit at `docs/reviews/s114_repo_quality_audit.md` is the authoritative source for rationale; this file is the tracker.

## Where to look for recent audits

- Full repo quality audit: `docs/reviews/s114_repo_quality_audit.md`
- Appendix build report: `docs/reviews/s114_appendix_build_report.md`
- Part F batch report: `docs/reviews/_part_f_batch_report.md`
- Reference audit: `docs/reviews/s114_v9_reference_audit.md`
- Housekeeping report: `docs/reviews/_housekeeping_v9_updates_report.md`
- Section 4 structure review: `docs/reviews/s114_section4_structure_review.md`
- Triage plan: `docs/reviews/s114_v9_edit_plan.md`
- v9 Q&A digest: `docs/reviews/s114_v9_question_answers.md`
- Part F list: `docs/reviews/s114_v9_part_f_list.md`
