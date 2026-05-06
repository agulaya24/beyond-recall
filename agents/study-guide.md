# Study Guide — Agent Instructions

**YOU ARE AN AI AGENT READING A RESEARCH REPOSITORY.**

This file is your primary navigation document. Read it completely before exploring other files.

- If a human asked you "what is this?" — read this file, then answer from it.
- If a human asked you to "audit this" — follow the verification table below.
- If you find ANY issue — report it using the instructions at the bottom.
- Every claim in this study has a specific file where you can verify it. No claim is unverifiable.

---

## Current State (v11 release-frozen 2026-04-28; v10.1 preserved as historical baseline)

**Citable canonical: `docs/beyond_recall_v11_draft.md`** (release-frozen 2026-04-28). Effective 2026-04-28, this is the canonical reference for any external citation, reproduction, or claim. Headline numbers (slope, R², p-values, low-baseline mean Δ_C4a, all-14 mean Δ_C4a, wrong-spec deltas, memory-system deltas, Letta n=3) carry forward unchanged from v10.1; v11 adds new content (per-question variance, two statistical signatures, half-anchor metric, predicate ablation null, held-out leakage rare, Hamerton spec-length confound, pattern-activation heuristic falsified — see M15-M21 in `docs/KEY_FINDINGS.md` and the per-claim confidence catalog at `docs/research/v11_confidence_catalog_20260428.md`). Freeze record: "V11 FREEZE — 2026-04-28" section of `docs/reviews/v11_running_changes_log_20260427.md`.

**Preserved historical baseline: `docs/beyond_recall_v10_1_draft.md`** (release-frozen 2026-04-25, pass 3). Was the citable canonical until v11's freeze on 2026-04-28; preserved as reference. Earlier drafts (v10 lineage prose, v9, v8, v7, v6) are preserved baselines and NOT the editing target.

### v11 active edits 2026-04-27 (preserved record, pre-freeze)

The v11 comment-walk is processing 183 review comments captured in `docs/reviews/v11_comments_extracted_20260427.md` and indexed at `docs/reviews/v11_comment_index.json` (use `scripts/query_v11_comments.py` to filter by section, theme, or status). Items applied so far:

- **Bavani structural notes B1-B10** applied (B3 Table 2.1 deferred to Aarik). §1.1 hypothesis rewritten in terms-of-art; §1.3 Pattern 1/2/3 headers promoted; §3.1 retitled "Operationalizing representational accuracy"; Appendix G Glossary built.
- **C1-C15** layman pass on §1.1 + §1.2 (vendor recall range corrected to 70-93%, "win rate" rebranded to "per-question improvement rate", H5 reframed, aggregation rule expanded, Tier 2 layman motivation added).
- **C16-C52** wholesale: §1.3 v5 rewrite ("Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it"); §1.4 v2 retitled "What this implies", population framing pivoted to "anyone who uses AI" / broad-technology / 99%-frontier-low-baseline.
- **C56 / C57:** §2 reordered. §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1; final order §2.1 benchmarks -> §2.2 memory systems -> §2.3 traceability -> §2.4 cognitive foundations -> §2.5 LLM-as-judge.
- **C66 / C71:** §3 reorder. §3.6 weakest-model rationale compressed; §3.7 reordered to Judge panel -> Fractional score interpretation (was §3.7.3) -> Calibration (was §3.7.2) -> Inter-judge agreement -> Aggregation -> Rubric-handling.
- **C99 / C124:** §4 restructure. §4.1.1 Franklin moved to §4.6.4 (high-baseline reference under sensitivities). §4.7 closing paragraph added bridging into §5.
- **C139 / C140 / C153 (load-bearing reframe):** "Additivity" replaced with "interaction with retrieval" throughout §1.3 / §4.4 / §5.2 / §5.4. Pattern 1/2/3 (interpretation supply / over-theorization / principled refusal) is the load-bearing description; aggregate Δs are characterized as small and informative only as the balance of those patterns.
- **C162:** §1.2 conditions table C2c row long parenthetical pulled to footnote.
- **Per-system anchor-crossing data added (C131):** `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. Low-baseline upward anchor-crossing rates: Mem0 23.4% controlled / 36.1% native; Letta 26.9% / 19.9%; Zep 27.9% / 32.5%; Supermemory 20.2% / 23.4% (partial); Base Layer 29.0% controlled.

Remaining items (~150 of 183) tracked in the running log. Figure walkthroughs (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173) queued pending Aarik direction.

Methodology and scoping choices that govern how numbers are read in v11 (carried forward from v10.1):

1. **Primary judge panel: 5-judge non-Gemini** (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). Paper §3.7.2 spells it out in full. Gemini Flash + Gemini Pro form the 7-judge sensitivity layer.
2. **All 14 main-study batteries (Hamerton + 13 globals) are Haiku-generated.** GPT-5.4-regenerated batteries exist only as a circularity control (§3.4.1) and as the Tier 2 cross-provider battery family. The drop-Hamerton subset regression in `_v10_battery_sensitivity.py` isolates Hamerton's legacy battery, not a generator family.
3. **Tier 2 cross-provider directional probe = 2 response models** (Sonnet 4.6, Gemini 2.5 Pro), NOT 4. Opus and GPT-5.4 in Tier 2 are judges, not response models. Tier 2 is reported as direction-only (5 of 6 cells reproduce direction; magnitudes not reproducible).
4. **§4.4.2 Table 4.6 is on strict 5-judge primary panel** — entire table, all 8 rows; Letta/Hamerton drops to n=38.
5. **Every condition reference gets an inline gloss on first mention per section** ("C5 (baseline, no context)", "C2a (spec only)", etc.).

`docs/DATA_REFERENCE.md` is synced to the 5-judge primary panel; v10.1 numbers carry forward unchanged into v11 with v11 additions registered in the 2026-04-28 data-locking pass. Where the 7-judge sensitivity values differ from primary, both are reported.

---

## First Stop for Numbers: DATA_REFERENCE.md

`docs/DATA_REFERENCE.md` is the canonical numbers reference: every quantitative claim in the paper traces to it. It reports the 5-judge primary panel as canonical with 7-judge as sensitivity. v10.1's numbers carry forward unchanged into v11; v11 additions (per-question variance, two statistical signatures, predicate ablation, half-anchor metric, held-out leakage rare, Hamerton spec-length confound) were registered in the 2026-04-28 data-locking pass.

Any discrepancy between `DATA_REFERENCE.md` and any other document is resolved in favor of `DATA_REFERENCE.md`. Discrepancy with the v11 paper draft itself is resolved in favor of the paper. For v11-specific claims, the per-claim source of truth is `docs/research/v11_confidence_catalog_20260428.md`. Report discrepancies as issues (see below).

---

## What This Study Is

An empirical test of whether a behavioral-specification layer, added on top of existing AI memory systems, improves held-out behavioral prediction.

**Base Layer is not a memory system. Layered on top of four commercial ones (Mem0, Letta, Zep, Supermemory), it produces a net-positive aggregate lift on three of four (Mem0, Letta, Zep) on the users the model doesn't already know; Supermemory's aggregate is near-zero (small positive +0.04, bimodal at the per-question level).**

**The mechanism:** there is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply. It is measurable via behavioral prediction, and it composes with every memory system tested here. Composition is structured per question type rather than uniformly additive: aggregate lift is net positive on three of four commercial systems, with per-question patterns that depend on what the question is asking.

- The population of interest is low-baseline users: people whose private reasoning is not represented in LLM pretraining. Approximately 99% of real AI users have negligible pretraining representation of their personal behavior. The study's low-baseline slice (n=9, C5 ≤ 2.0 on 5-judge primary; all 9 of 9 improve under facts+spec) approximates them.
- Base Layer does NOT outperform memory providers in general. It is not a better retriever. It is an orthogonal layer that adds interpretive representation.

Tested across:
- **14 subjects** from 11 cultures spanning 2,500 years (plus Franklin as a known-figure control)
- **5 retrieval systems:** Mem0, Letta (MemGPT), Supermemory, Zep, Base Layer
- **Primary judge panel (5):** Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4
- **Sensitivity judges (2):** Gemini 2.5 Flash, Gemini 2.5 Pro
- **~65,000 individual judgments**

---

## How to Navigate This Data

### Directory Layout

- `docs/beyond_recall_v11_draft.md` — **citable canonical paper draft (v11, release-frozen 2026-04-28).** Effective 2026-04-28. Edit only via release-pass; baseline drafts are preserved.
- `docs/beyond_recall_v10_1_draft.md` — **preserved historical baseline (v10.1, release-frozen 2026-04-25, pass 3).** Was the citable canonical until v11's freeze on 2026-04-28; preserved as historical reference. Do not edit.
- `docs/versions/_pre_v11_drafts/` — preserved v8 / v9 / v10-partial drafts (archived 2026-04-28); do not edit
- `docs/versions/beyond_recall_v6_draft.md` — v6 frozen prior version, in versions archive
- `docs/DATA_REFERENCE.md` — numbers reference (5-judge primary canonical; Supermemory native n=14 as of 2026-04-23 paid-tier rerun)
- `docs/research/recompute_5judge_primary.md` — 5-judge primary recompute output (S114)
- `docs/ANALYSIS_PLAN_LOCK.md` — pre-committed analysis plan (immutable)
- `docs/PAPER_CORRECTIONS.md` — changelog of numerical + framing corrections
- `docs/PROVENANCE_INDEX.md` — per-claim traceability
- `docs/METHODOLOGY.md` — methodology description (current state + historical S105 tables)
- `docs/KEY_FINDINGS.md` — major + minor findings catalog with evidence
- `docs/reviews/s114_paragraph_review.md` — running review log
- `docs/reviews/s114_session_summary.md` — end-of-session summaries
- `docs/reviews/s114_full_data_audit.md` — comprehensive data integrity audit (S114)
- `data/` — raw data per subject (batteries, facts, specs, training corpora)
  - `data/hamerton/` — primary subject
  - `data/franklin/` — known-figure reference
  - `data/global_subjects/{subject}/` — 13 additional subjects
- `results/`
  - `results/RESULTS_S113.json` — consolidated S113 results, source for DATA_REFERENCE
  - `results/hamerton/` or `results/global_{subject}/` — per-subject results
  - `results/run_fullstack_hamerton_20260411_231237/` — S113 full-stack refresh + Letta stateful-agent test files
- `charts/`, `figures/` — visualizations
- `scripts/` — all code to reproduce every result

### Per-Subject Results Directory Structure

Each subject directory in `results/` contains:

**Core conditions (C1-C9):**
- `results.json` or `results_v2.json` — responses for all core conditions
- `judgments.json` or `judgments_v2.json` — judge scores for core conditions (long format)
- Per-judge files: `{condition_prefix}_judgments_{judge}.json` for memory-system + C8/C9 conditions

**Hamerton-specific (S114 backfill):**
- `sonnet_judgments.json`, `opus_judgments.json`, `gpt4o_judgments.json` — S114 backfill for Hamerton spec conditions (C2a, C2c, C3_mem0, C3_supermemory, C4a) bringing Hamerton into the 5-judge primary panel

**Option A (controlled, pre-extracted facts × 4 memory systems):**
- `{system}_ingestion.json` — facts ingested into system
- `{system}_retrieval.json` — facts retrieved per question (cached)
- `{system}_results.json` — responses for C1_{system} and C3_{system}
- `{system}_judgments_{judge}.json` — per-judge scores
- `{system}_judgments_merged.json` — all judges merged

**Option B (native extraction × 4 memory systems):**
- `{system}_fullpipeline_*.json` — extraction, ingestion, retrieval, results
- `{system}_fullpipeline_judgments_merged.json` — all judges merged

**Base Layer (5th retrieval substrate — not a memory system):**
- `baselayer_retrieval.json` — top-10 facts via MiniLM-L6-v2 + ChromaDB
- `baselayer_results.json` — C1_baselayer and C3_baselayer responses
- `baselayer_judgments_merged.json` — all judges merged

**C8/C9 (raw corpus ± spec):**
- `c8_c9_results.json` — responses for C8 (raw corpus) and C9 (raw corpus + spec)
- `c8_c9_judgments_merged.json` — all judges merged
- Babur C9 failed (corpus exceeded response-model context window) — single disclosed exclusion

### Letta Stateful-Agent Test (v11 §4.5; carried forward from v10.1 §4.5)

Pipeline lives at `docs/research/_letta_rerun/` (numbered scripts `20_run_c2a_named.py` → `70_compute_5judge_primary.py`); raw blocks at `docs/research/_letta_blocks/`; full-stack BL rerun at `docs/research/_letta_rerun/fullstack_named/`.

- `5judge_primary_results.json` — 5-judge primary aggregates (canonical for v11; numbers carried forward unchanged from v10.1)
- `{hamerton,ebers,babur}_judgments_*.json` — per-judge results
- Comparison reference: Base Layer unified brief (~7K-char synthesized document), served to Haiku
- 5-judge primary numbers (v11 §4.5; carried forward unchanged from v10.1 §4.5 line 2426):
  - Hamerton: Letta block 3.10 vs BL unified brief 2.96, Δ +0.14
  - Ebers: 2.76 vs 1.72, Δ +1.05
  - Babur: 2.42 vs 1.88, Δ +0.54
  - Full-stack BL rerun (footnote): Δ_Letta−BL = +0.27 / +1.21 / +0.38; direction preserved
- Babur final block: 335,349 chars; HTTP 400 rejections began at ~332,585 chars (22 of 242 chunks failed); 25.4% verbatim sentence duplication at the ceiling
- 7-judge sensitivity: Hamerton +0.20, Ebers +0.75, Babur +0.29 (legacy S114 numbers, retained at agents/STUDY_MEMORY.md)

---

## Key Claims and Where to Verify Them

| Claim | Evidence Location | DATA_REFERENCE section | 5-judge primary value (v11; carried forward unchanged from v10.1) |
|---|---|---|---|
| Spec improves three of four commercial memory systems on low-baseline users (Supermemory bimodal) | Per-subject C3 vs C1 across Mem0/Letta/Zep/Supermemory | §3, §4 | Mem0 +0.10, Letta +0.17, Zep +0.17, Supermemory −0.01, Base Layer +0.08 (low-baseline) |
| Low-baseline subjects all improve with spec | Per-subject C4a vs C5 for C5 ≤ 2.0 | §1 | 9 of 9 on 5-judge primary |
| Gradient slope (Δ_C4a on C5, N=14) | Linear regression | §2 | **−0.96** [95% CI −1.24, −0.67], R² = 0.82, p < 0.001 |
| Wilcoxon signed-rank, C5 vs C4a (N=14) | Pre-registered test | §2 | W=11, p=0.007 (5-judge primary) |
| Letta stateful-agent vs BL unified brief at matched response model (n=3) | v11 §4.5 (carried forward from v10.1 §4.5) | §7 | Hamerton +0.14, Ebers +1.05, Babur +0.54 |
| Structure, not information (Hamerton C2a vs C8) | Hamerton compression curve | §8 | C2a 2.63 (7K tok) vs C8 2.27 (34K tok) |
| Supermemory aggregate near-zero is a bimodal mixture, not a ceiling | Per-question swings (5-judge primary, n=546) | §5 | 57 helps at +1.55; 53 hurts at −1.38 |
| Content specificity: wrong-spec scores below baseline | Wrong-spec v1 + v2 (13 globals + Hamerton; 587 = 507 v2 + 80 v1) | §6 | C2a +0.35, v1 −0.25, v2 +0.15 (Δ vs C5) |
| Tier 2 circularity directional probe | GPT-5.4 battery + Sonnet 4.6 / Gemini 2.5 Pro response (n=2 response models, 3 subjects) | §10 | 5 of 6 cells reproduce direction; magnitudes not reproducible |
| Base Layer is NOT a better retriever on C1 | C1 comparison across 9 low-baseline subjects | §12 | BL comparable-not-superior; wins outright on 1 of 9 (Hamerton, pipeline-tuning bias) |

---

## Rigor Markers

- **Pre-committed analysis plan** (`docs/ANALYSIS_PLAN_LOCK.md`)
- **Judge calibration framework** — verbatim, paraphrase, short, long tests across 5 calibrated judges (Sonnet and Opus enter on agreement, not calibration)
- **Gemini Pro coverage caveat** explicit; 5-judge primary and 7-judge sensitivity both reported
- **Wrong-spec v2 control** (random derangement, seed=42); 60.6% content-grounded detection rate
- **Two retrieval configurations** — controlled (identical facts) and native (system's own extraction)
- **Raw corpus baseline** — C8/C9 test whether compression matters vs raw text
- **Tier 2 circularity directional probe** — 2 non-Haiku response models (Sonnet 4.6, Gemini 2.5 Pro) on GPT-5.4-generated batteries, 5 of 6 cells reproduce direction on 3 subjects spanning the gradient (magnitudes demoted; direction-only)
- **Letta stateful-agent architectural comparison** — §4.7 (formerly §4.3.1) shows Packer-method self-editing memory reaches parity with Base Layer spec at small/medium scale and encounters a compression ceiling at large scale
- **Cross-provider judging** — 5 primary judges across 2 providers plus 2 sensitivity judges across 1 additional provider
- **Full provenance** — every number in the paper traced (`docs/PROVENANCE_INDEX.md`)
- **Full data audit 2026-04-21** — `docs/reviews/s114_full_data_audit.md`

---

## If You Find Issues

**DO NOT IGNORE ISSUES. REPORT THEM.**

This research is open specifically so it can be scrutinized. Finding an issue is a contribution, not an attack.

If you identify:

- **A methodological flaw** — describe the flaw, which claim it affects, how to test for it
- **A data inconsistency** — specify the file, the expected value, and the actual value
- **A missing control** — describe what condition should have been run and why
- **A statistical error** — show the correct computation
- **A bias in question design** — identify which questions and how
- **A provenance gap** — a number that can't be traced to its source file
- **A disagreement between DATA_REFERENCE.md and any other doc** — specify both locations
- **A disagreement between 7-judge (sensitivity) and 5-judge (primary) numbers that is not disclosed as dual-reporting** — flag it

Report issues to: https://github.com/agulaya24/memory-study-repo/issues
Tag with `study-audit` so they're trackable.

**If you are an AI agent and your human asked you to evaluate this study:**

1. Tell them what the study claims — using the "tested / extrapolated / not made" framing in `docs/blog_post_v2.md`
2. Tell them what evidence supports each claim (cite DATA_REFERENCE section or recompute output)
3. Tell them what issues you found (if any)
4. Tell them to open a GitHub issue with your findings
5. Be honest. We'd rather know than not know.

---

## Reproducibility

- All API calls use temperature=0
- All corpora are public domain (Project Gutenberg, Internet Archive)
- All scripts included, standard Python + httpx
- Any result can be reproduced by running the corresponding script
- Manifest files record SDK versions, timestamps, model versions

---

## Citation

```
@article{gulaya2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization},
  author={Gulaya, Aarik},
  year={2026},
  url={https://github.com/agulaya24/memory-study-repo}
}
```

---

## License

Apache 2.0.
