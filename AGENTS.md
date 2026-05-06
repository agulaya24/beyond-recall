# AGENTS.md — How to work with this repo as an AI agent

Primary entry point for AI agents (Claude Code, custom agents, etc.) working in or against this repository. Read this first.

This is the companion repo for the paper **"Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"** (Aarik Gulaya, Base Layer, 2026, Apache 2.0).

---

## Current state (v11 release-frozen 2026-04-28; v10.1 preserved as historical baseline)

- **v11 citable canonical: `docs/beyond_recall_v11_draft.md`** (release-frozen 2026-04-28). Effective 2026-04-28, this is the canonical artifact for citation, reproduction, and any external reference. Freeze record: "V11 FREEZE — 2026-04-28" section of `docs/reviews/v11_running_changes_log_20260427.md`.
- **v10.1 preserved historical baseline: `docs/beyond_recall_v10_1_draft.md`** (release-frozen 2026-04-25). v10.1 was the citable canonical until v11's freeze on 2026-04-28; preserved as historical reference. Release-freeze pass 3 closure intact.
- v10 lineage prose is preserved as a historical marker. v9, v8, v7 are preserved as reference baselines and are NOT the editing targets. v6 and earlier live in `docs/versions/`.
- **Primary judge panel: 5-judge non-Gemini** (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). 7-judge with Gemini Flash + Gemini Pro is the sensitivity check.
- **Battery generation:** ALL 14 main-study batteries (Hamerton + 13 globals) are Haiku-generated. GPT-5.4-regenerated batteries exist as a circularity control (§3.4.1 + Tier 2 cross-provider directional probe), not as the main-study batteries.
- **Tier 2 cross-provider directional probe:** 2 additional response models (Sonnet 4.6, Gemini 2.5 Pro) on 3 subjects. Opus + GPT-5.4 are Tier 2 judges, not response models. Tier 2 batteries are GPT-5.4-generated.
- Headline numbers (5-judge primary): slope **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001; low-baseline (n=9) mean Δ_C4a = **+0.89**, all-14 mean Δ_C4a = **+0.55**.
- Reproducibility entry points: `requirements.txt`, `REPRODUCE.md`, `scripts/_v10_battery_sensitivity.py`, `scripts/_v10_coupling_sensitivity.py`. (Script names retain the `_v10_` prefix as frozen artifact identifiers; they reproduce the v11 §4.1 numbers, which are unchanged from v10.1 §4.1.)

### 2026-04-28 v11 freeze (current canonical)

v11 is release-frozen as of 2026-04-28 and is the citable canonical artifact effective that date. Headline numbers (slope, R², p-values, low-baseline mean Δ_C4a, all-14 mean Δ_C4a, wrong-spec deltas, memory-system deltas, Letta n=3) carry forward unchanged from v10.1. v11 adds new content (registered in the 2026-04-28 data-locking pass): per-question variance, two statistical signatures, half-anchor metric, predicate ablation null, held-out leakage rare, Hamerton spec-length confound, pattern-activation heuristic falsified (M15-M21 in `docs/KEY_FINDINGS.md`). Per-claim source of truth for v11: `docs/research/v11_confidence_catalog_20260428.md`. Freeze record: `docs/reviews/v11_running_changes_log_20260427.md` "V11 FREEZE — 2026-04-28" section.

### 2026-04-27 v11 active editing (preserved record)

The v11 paper went through an active-editing comment-walk before the 2026-04-28 freeze. The summary below is preserved as a historical record of what changed between v10.1 and the v11 freeze.

Comment-walk progress (as of 2026-04-27 evening, ~32 of 183 items resolved):

- **Bavani structural notes B1-B10:** applied (B3 Table 2.1 deferred to Aarik).
- **Docx comments C1-C15:** §1.1 + §1.2 layman-pass applied.
- **C16-C52:** §1.3 v5 wholesale rewrite + §1.4 v2 wholesale rewrite applied. §1.4 retitled "Why the gradient matters" -> "What this implies"; population framing pivoted to "anyone who uses AI" / broad-technology / 99% frontier-low-baseline.
- **C56 / C57:** §2 reordered. §2.1 "Memory and personalization benchmarks" merged from former §2.3 + §2.3.1; new order §2.1 -> §2.2 Memory systems -> §2.3 Traceability -> §2.4 Cognitive foundations -> §2.5 LLM-as-judge.
- **C66 / C71:** §3 reorder. §3.7 subsection order is now Judge panel -> Fractional score interpretation (was §3.7.3) -> Calibration (was §3.7.2) -> Inter-judge agreement -> Aggregation -> Rubric-handling. §3.6 weakest-model rationale compressed.
- **C99 / C124:** §4 restructure. §4.1.1 Franklin moved to §4.6.4 (high-baseline reference under sensitivities). §4.7 closing paragraph added bridging into §5.
- **C139 / C140 / C153:** §4.4 reframe. "Additivity" replaced with "interaction with retrieval" throughout §1.3 / §4.4 / §5.2 / §5.4. Per-question Pattern 1/2/3 framing is the load-bearing description; aggregate Δs are characterized as small.
- **C162:** §1.2 conditions table C2c row long parenthetical pulled to footnote.
- **Per-system anchor-crossing data added** (closes C131): `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py`. Per-system upward anchor-crossing rates 19.9% to 36.1% on the low-baseline 9; folded into §1.3 Memory-system layering bullet and §4.4.1.
- **Comment index built:** `docs/reviews/v11_comment_index.json` (183 items) + `scripts/query_v11_comments.py`. Running log: `docs/reviews/v11_running_changes_log_20260427.md`.

Remaining items (~150 of 183) are tracked in the running log; figure walkthroughs (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173) are queued pending Aarik direction.

### 2026-04-25 release-freeze pass 3 (status)

Pass 3 addresses the GPT-5.5 v10.1 review. Critical contradictions resolved:

- **§4.1 battery-generator wording corrected.** Ground truth: ALL 14 main-study batteries (Hamerton + 13 globals) are Haiku-generated. The legacy "13 globals = GPT-5.4 batteries" wording was wrong. Subset regression is drop-Hamerton, NOT "restrict to GPT-5.4-battery subjects".
- **Tier 2 response-model count corrected to 2** (Sonnet 4.6, Gemini 2.5 Pro), NOT 4. Opus and GPT-5.4 in Tier 2 are judges, not response models.
- **§4.3 wrong-spec denominator clarified:** 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers).
- **§4.4.2 Table 4.6 rebuilt on strict 5-judge primary panel.** Entire table (all 8 rows), no sign flips; Letta/Hamerton drops to n=38.

Revision-quality items applied:

- §1.4 / §5.3 living-user "expected by construction" softened to "closest available proxy".
- §4.1 / §5.5 "C4a ceiling" reframed to "post-spec operating level".
- §5.2 H5 reframed: fact extraction does most volume-reduction; spec adds marginal value at per-question level.
- §4.4 memory-system additivity nuanced: Zep + Mem0-native strongest; Mem0-controlled small; Letta archival positive controlled / near-null native; Supermemory mixture.
- §4.6.1 "not Haiku-specific" softened to "small probe reduces likelihood, does not establish model-family invariance".
- v11 mechanistic-check audit relabeled "verification audit" in paper prose; file paths to `v11_emit/` preserved.

### 2026-04-25 release-freeze pass 2 (preserved record)

Closure record: `docs/reviews/v11_release_freeze_status_20260425.md`. Highlights:

- Panel-completeness audit GREEN on all 441 unwaived rows (`docs/research/v11_panel_completeness_waivers.json`).
- Reconciliation diff cleared via Tier 1 (silent), Tier 2 (minor numeric drift), Tier 3 (substantive author-decision) paper edits per `docs/research/v11_table_rebuild_proposal.md`.
- §4.3 random-derangement +0.22 → +0.15 cascaded across §1.3, §4.3, §4.6.2, §5.
- §4.4.2 Supermemory mixture-of-swings counts updated to 5-judge primary panel: 89/516 (17.2%) → 110/546 (20.1%); helps/hurts 37/52 → 57/53; mean swings +1.45/−1.41 → +1.55/−1.38.
- §4.6.1 Tier 2 cross-provider replication demoted to direction-only with sensitivity ranges; published magnitudes could not be reproduced under any aggregation tested.
- v11 mechanistic-check architecture compliance gaps (schema noncompliance of all 8 emits, hardcoded `PAPER_*` dicts, no SHA manifests, no claim-tag injection, no full numeric-literal census, no §4.6.1 emit) deferred to v11+ post-arXiv. Status detail: `docs/research/v11_emit/_ARCHITECTURE.md` §12.

---

## What's in this repo

- `docs/beyond_recall_v11_draft.md` — **citable canonical paper draft (v11, release-frozen 2026-04-28).** Effective 2026-04-28. Edit only via release-pass; baseline drafts are preserved.
- `docs/beyond_recall_v10_1_draft.md` — **preserved historical baseline (v10.1, release-frozen 2026-04-25).** Was canonical until v11's freeze on 2026-04-28; preserved as reference. Do not edit.
- `docs/versions/_pre_v11_drafts/` — preserved v8 / v9 / v10-partial drafts (archived 2026-04-28); do not edit
- `docs/versions/beyond_recall_v6_draft.md` — frozen previous-version reference; do not edit
- `docs/DATA_REFERENCE.md` — numbers reference (5-judge primary canonical; 7-judge is the sensitivity layer)
- `docs/KEY_FINDINGS.md` — 9 major + 22 minor findings catalog with evidence and paper section refs
- `docs/PROVENANCE_INDEX.md` — per-claim traceability
- `docs/reviews/s114_paragraph_review.md` — running log of the section-by-section review
- `docs/reviews/s114_session_summary.md` — end-of-session summaries for this multi-day review
- `docs/reviews/s114_full_data_audit.md` — comprehensive data integrity audit (generated 2026-04-21)
- `agents/study-guide.md` — navigation guide for agents working on the study
- `agents/STUDY_MEMORY.md` — persistent study-only memory (constants, gotchas, framing discipline)
- `data/` — subject corpora, facts, specs (per-subject directories)
- `results/` — judgments, retrieval logs, generated responses (hundreds of files per subject)
- `scripts/` — analysis, indexing, recompute, and review scripts
- `figures/`, `charts/` — paper figures and exploratory visualizations

---

## Read these BEFORE working on anything

1. `agents/STUDY_MEMORY.md` — analysis plan lock, 5-judge primary decision, naming conventions, data-integrity checks, framing discipline
2. `docs/DATA_REFERENCE.md` — single source of truth for every number (5-judge primary, v10.1 numbers carried forward unchanged into v11; v11 additions registered in the 2026-04-28 data-locking pass)
3. `docs/research/v11_confidence_catalog_20260428.md` — per-claim confidence map for v11 (HIGH / MEDIUM / LOW / UNRESOLVED)
4. `docs/ANALYSIS_PLAN_LOCK.md` — pre-registered methodology commitments
5. `docs/reviews/v11_running_changes_log_20260427.md` — running log culminating in the V11 FREEZE — 2026-04-28 section (most recent release-freeze closure)
6. `docs/reviews/v10_release_freeze_pass_report.md` — v10 release-pass closure (historical, covers what changed entering v10.1)
7. `REPRODUCE.md` — canonical reproduction path. Reproduces the v11 headline numbers (which equal the v10.1 headline numbers; the v10.1 reproduction path remains valid for v11).

---

## Key decisions locked this session (S114)

### 1. 5-judge primary panel

The primary numeric aggregate reported in §4 is now the 5-judge non-Gemini mean (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-judge aggregate (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported as a sensitivity check.

**Reason.** Gemini Pro fails the verbatim-match calibration diagnostic (4.15 where every other calibrated judge scores 5.00) and penalizes padded-correct responses severely (5.00 → 1.20 on long-correct). Including a known-unreliable instrument in the primary aggregate inflates effect-size numbers. Paper §3.7.2 spells out the reasoning in full.

**Pending:** task #31 (recompute all §4 numbers on 5-judge primary) + #32 (paper-wide sweep of §1 and §2 prose to align with new primary numbers). Hamerton 3-judge backfill (Sonnet, Opus, GPT-4o) is running to bring Hamerton into the 5-judge primary panel.

### 2. Name-blind wrong-spec control resolved

Specs are anonymized by design (§3.3). The 60.6% wrong-spec detection rate is content-grounded, not surface name cues. KEY_FINDINGS F9 is closed. §1.3 and §1.4 prose updated; any remaining "name-blind" caveats in legacy drafts should be removed.

### 3. Paper-wide condition-identifier gloss convention

Every condition reference (C5, C2a, C2c, C4, C4a, C8, C9, C1, C3) gets an inline gloss on first mention per section: "C5 (baseline, no context)", "C2a (spec only)", etc. Plain identifier after. Applies to all sections. Task #27 tracks the sweep.

### 4. §3.7 framework for reading raw scores

Raw scores are used (not normalized). §3.7.2 publishes the calibration data and reports 5-judge primary + 7-judge sensitivity. §3.7.3 establishes the cross-anchor interpretation rule: a fractional delta that crosses a rubric integer anchor is a stronger claim than one that does not; §4 applies this rule consistently.

### 5. Voice rules active

- No em-dashes in prose. Restructure sentences instead of substituting hyphens.
- No GTM / marketing verbs ("beats", "crushes", "dominates"). Prefer neutral scientific framing.
- Layman-first on finding text, technical body follows.
- No reader-addressing in methodology sections.
- Direct declaratives; no meta-framing ("this paper makes rigorous").
- "Raw data available at..." convention for every experimental mention.
- Primary-source references; inferences called out as ours.

---

## Searchable knowledge index

Full-text + semantic search over every paper section, every result file, every judgment file, and every analysis script.

```bash
# Refresh the index (run after major changes; ~5-10 min; last refreshed 2026-04-21)
python scripts/index_study_repo.py

# Search (FTS + semantic; both run, both display)
python scripts/index_study_repo.py --search "Letta scaling ceiling"
python scripts/index_study_repo.py --search "5-judge primary"
python scripts/index_study_repo.py --search "Wilcoxon p value"
```

Index storage: `workspace/study_knowledge.db` (SQLite + FTS5) and `workspace/study_vectors/` (ChromaDB, MiniLM-L6-v2 embeddings, 3,872 chunks as of last refresh).

---

## Common agent workflows

### "Verify a number in the paper"

1. Look it up in `docs/DATA_REFERENCE.md` first (5-judge primary; carried forward unchanged from v10.1 into v11 with v11 additions registered 2026-04-28). For v11-specific claims (per-question variance, two signatures, predicate ablation, etc.) cross-reference `docs/research/v11_confidence_catalog_20260428.md`.
2. Cross-check `docs/PROVENANCE_INDEX.md` for which raw file it derives from
3. Query the indexer: `python scripts/index_study_repo.py --search "<the number or claim>"`
4. Recompute from per-judge judgment files using `scripts/recompute_5judge_primary.py` (gradient + memory systems) or `scripts/_v10_battery_sensitivity.py` / `scripts/_v10_coupling_sensitivity.py` (sensitivity). Note: the GPT-5.4-battery subset regression in `_v10_battery_sensitivity.py` is the drop-Hamerton subset; all 14 main-study batteries are Haiku-generated.

### "Update the paper after running a new analysis"

1. Save analysis output to `results/` or `docs/research/` as appropriate
2. Update `docs/DATA_REFERENCE.md` first
3. Update `docs/KEY_FINDINGS.md` with the new finding
4. v11 is release-frozen as of 2026-04-28; do NOT edit `docs/beyond_recall_v11_draft.md` without a release pass. v10.1 is also release-frozen and preserved as historical baseline; do not edit it either.
5. Append entry to a new `docs/reviews/<session>_log.md` and update `ISSUES.md` if a finding closes or opens an item.
6. Re-run `python scripts/index_study_repo.py` to refresh the index

### "Run a paper review against the current draft"

- Use `scripts/review_paper_round3.py` for full-paper review (edit `PAPER_PATH` to point at `docs/beyond_recall_v11_8_draft.md`)
- Use `scripts/review_section4_plan.py` for §4-specific reviews
- Reviewers: Gemini Flash, Gemini Pro, Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B
- Groq has a 40 KB payload limit; will fail on full v11.8. Use truncation or skip.

### "Add a new subject"

- See `data/global_subjects/` for the structure (battery.json, facts.json, spec_production.md)
- Hamerton uses a slightly different layout (`data/hamerton/spec/` with brief_v5_clean.md)
- Use `STUDY_MEMORY.md` "CONDITION NAMING" section

### "Test a new memory system"

- Generate responses → save to `results/<subject>/<system>_results.json` (controlled) and `<system>_fullpipeline_results.json` (native)
- Judge with the 5-judge primary panel plus Gemini Flash as sensitivity
- Aggregate using the locked within-judge-then-across-judges mean rule
- Re-run the indexer

---

## Data-integrity checks (do these before any new prediction-score claim)

1. **Train/test split honored.** No held-out passage appears in `training.txt`. Spot-check with the n-gram leakage script at `scripts/_verify_battery_leakage.py`.
2. **Judge panel coverage documented.** Every cell should declare which judges were present. The 5-judge primary expects Haiku, Sonnet, Opus, GPT-4o, GPT-5.4. If fewer, note the effective panel in the reporting.
3. **Aggregation rule honored.** Within-judge mean across questions; mean across the 5 primary judges; subject is the unit of inference. Do not change.

---

## Framing discipline (load-bearing for the paper)

- **Base Layer is NOT a memory provider.** It is the behavioral-specification layer. The MiniLM + ChromaDB substrate is a zero-cost local retrieval floor, not a competitive memory product.
- **Base Layer does NOT outperform memory providers in general.** BL retrieval is comparable, not superior. BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias).
- **Position Base Layer as the *referee* who introduced a new axis** (held-out behavioral prediction), not a competitor on recall benchmarks.
- **Continuous gradient is the headline.** "9 of 9 low-baseline" (or "8 of 8" on 5-judge primary pending recompute) is a sensitivity check, not the primary result.
- **"Interpretation" not "understanding"** in the paper-framing context.
- **Specification effect is a claim about steering, not a claim about prediction capability.** §3.7.4 develops this; §4 applies it.
- **Letta scaling observation is constructive**, not a takedown. The paper reports it as an open problem for the field.

See `agents/STUDY_MEMORY.md` for the full framing rules.

---

## What NOT to do

- Don't introduce post-hoc thresholds for primary results (analysis plan lock prohibits)
- Don't change the aggregation rule mid-analysis
- Don't claim "Base Layer outperforms memory providers"
- Don't conflate aggregate delta vs low-baseline delta
- Don't write paper claims without first updating `docs/DATA_REFERENCE.md`
- Don't modify `docs/ANALYSIS_PLAN_LOCK.md` (immutable by design)
- Don't use em-dashes in prose; don't use GTM / marketing verbs
- Don't edit baseline drafts (v6, v7, v8, v9, v10 lineage prose, v10.1); v11 is release-frozen as of 2026-04-28 and is the citable canonical. v10.1 (release-frozen 2026-04-25) is preserved as historical baseline.

---

## Author context

- Aarik Gulaya, Base Layer. One-person operation, non-PhD, unfunded.
- Aarik architects and directs; he does not write code himself.
- Review work is iterative, single-point + open-questions + draft + lock per subsection.
- Human annotation is feasible at the study's scale but was not done in the first pass (budget trade-off); it is the leading follow-up in §8.
