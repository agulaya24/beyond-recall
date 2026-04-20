# AGENTS.md — How to work with this repo as an AI agent

Primary entry point for AI agents (Claude Code, custom agents, etc.) working in or against this repository. Read this first.

This is the companion repo for the paper **"Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"** (Aarik Gulaya, Base Layer, 2026, Apache 2.0).

---

## What's in this repo

- `docs/beyond_recall_v6_draft.md` — canonical paper draft (~24K words)
- `docs/DATA_REFERENCE.md` — **single source of truth for every number** in the paper
- `docs/KEY_FINDINGS.md` — 9 major + 14 minor findings catalog with evidence and paper section refs
- `agents/study-guide.md` — navigation guide for agents working on the study
- `agents/STUDY_MEMORY.md` — persistent study-only memory (constants, gotchas, framing discipline)
- `data/` — subject corpora, facts, specs (per-subject directories)
- `results/` — judgments, retrieval logs, generated responses (hundreds of files per subject)
- `scripts/` — analysis and indexing scripts (see `scripts/README.md`)
- `figures/`, `charts/` — paper figures and exploratory visualizations
- `docs/reviews/` — cross-LLM review rounds (R1-R3) plus Gemini-only earlier reviews

For a one-page paper-status snapshot, read `docs/KEY_FINDINGS.md`. For numbers, read `docs/DATA_REFERENCE.md`. For methodology, read `docs/METHODOLOGY.md`.

---

## Read these BEFORE working on anything

1. `agents/STUDY_MEMORY.md` — analysis plan lock, naming conventions, data-integrity checks, framing discipline
2. `docs/DATA_REFERENCE.md` — canonical numbers (resolve any conflict in favor of this)
3. `docs/ANALYSIS_PLAN_LOCK.md` — pre-registered methodology commitments (gradient is continuous; no post-hoc thresholds for primary results)

---

## Searchable knowledge index

The repo includes a built-in semantic + full-text search over every paper section, every result file, every judgment file, and every analysis script. Build/refresh and query it with:

```bash
# Build the index (run once after major changes; ~5-10 min)
python scripts/index_study_repo.py

# Search (FTS + semantic; both run, both display)
python scripts/index_study_repo.py --search "Letta scaling ceiling"
python scripts/index_study_repo.py --search "Babur duplication"
python scripts/index_study_repo.py --search "Wilcoxon p value"
python scripts/index_study_repo.py --search "memory provider strengths"
```

Index storage: `workspace/study_knowledge.db` (SQLite + FTS5) and `workspace/study_vectors/` (ChromaDB, MiniLM-L6-v2 embeddings).

What's indexed:
- All canonical paper docs (paper draft, KEY_FINDINGS, DATA_REFERENCE, METHODOLOGY, PROVENANCE_INDEX, ANALYSIS_PLAN_LOCK, PAPER_CORRECTIONS, REFERENCE_TABLE, README, study-guide, STUDY_MEMORY)
- All review rounds (`docs/reviews/`)
- Blog post (`docs/blog_post_v2.md`)
- Per-subject specs (`data/**/spec*.md`, `data/**/brief*.md`, `data/**/*_v4.md`)
- Per-subject facts (sample of 20)
- Aggregate results files (`RESULTS_*.json`, `summary*.json`, retrieval-disagreement analysis, Letta block duplication analysis)
- Letta stateful-agent test results (memory blocks, judgments, responses)
- Analysis scripts (study + experiment dir, by function/class)

Use this when: you need to find where a finding lives, which file contains a specific number, what a script does, or how a condition was defined.

---

## Common agent workflows

### "Verify a number in the paper"
1. Look it up in `docs/DATA_REFERENCE.md` first (single source of truth)
2. Cross-check `docs/PROVENANCE_INDEX.md` for which raw file it derives from
3. If still uncertain, query the indexer: `python scripts/index_study_repo.py --search "<the number or claim>"`

### "Update the paper after running a new analysis"
1. Save analysis output to `data/experiments/memory_systems/results/` or equivalent
2. Update `docs/DATA_REFERENCE.md` first
3. Update `docs/KEY_FINDINGS.md` with the new finding
4. Edit the paper draft `docs/beyond_recall_v6_draft.md` to match
5. Append entry to `docs/PAPER_CORRECTIONS.md` (S113 section template)
6. Re-run `python scripts/index_study_repo.py` to refresh the index

### "Run a paper review against current draft"
- `python scripts/review_paper_round3.py` (or copy and increment the round number)
- Reviewers: Gemini Pro, Mistral Large, Cerebras Qwen3, Groq Llama 3.3 70B
- API keys in user env vars (PowerShell `[System.Environment]::GetEnvironmentVariable('KEY','User')`)

### "Add a new subject"
- See `data/global_subjects/` for the structure (battery.json, facts.json, spec_production.md)
- Hamerton uses a slightly different layout (`data/hamerton/spec/` with brief_v5_clean.md instead of spec_production.md)
- Use `STUDY_MEMORY.md` "CONDITION NAMING" section to name new conditions correctly

### "Test a new condition (e.g., new memory system)"
- Generate responses → save to `results/<subject>/<condition>_results.json`
- Judge with 7-panel via `data/experiments/memory_systems/judge_*.py` scripts
- Aggregate with `data/experiments/memory_systems/final_analysis.py` → updates `RESULTS_S113.json`
- Re-run indexer

---

## Data-integrity checks (do these before any new prediction-score claim)

1. **Train/test split honored.** No held-out passage should appear in `training.txt`. Quick check script: `data/experiments/memory_systems/string_match_disagreement.py` pattern, replicated for held-out check.
2. **Judge panel coverage documented.** If a judge isn't run for a subject, document it in §3.7 (Hamerton+Tier 2 had 7 judges; global subjects' main gradient had 6).
3. **Aggregation rule honored.** Mean within judge across questions; mean across judges; subject is the unit of inference. Don't change the rule.

---

## Framing discipline (load-bearing for the paper)

- **Base Layer is NOT a memory provider.** It is the behavioral-specification layer. The MiniLM + ChromaDB substrate included in the benchmark is a zero-cost local retrieval floor, not a competitive memory product.
- **Base Layer does NOT outperform memory providers in general.** BL retrieval is comparable-not-superior. BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias).
- **Position Base Layer as the *referee* who introduced a new axis** (held-out behavioral prediction), not a competitor on the existing axis (recall benchmarks).
- **Continuous gradient is the headline.** "9 of 9 low-baseline" is a sensitivity check, not the primary result (the analysis plan lock is explicit on this).
- **"Interpretation" not "understanding"** in the paper-framing context.
- **Letta scaling collapse is a constructive observation**, not a takedown. Stateful-agent memory architectures haven't solved compression-at-scale. The paper reports this as an open problem for the field.

See `agents/STUDY_MEMORY.md` for the full framing rules.

---

## What NOT to do

- Don't introduce post-hoc thresholds for primary results (analysis plan lock prohibits)
- Don't change the aggregation rule mid-analysis (subject is unit of inference; mean within judge then across judges)
- Don't claim "Base Layer outperforms memory providers" — the data doesn't support that framing
- Don't conflate aggregate delta vs low-baseline delta when discussing memory-system performance
- Don't write paper claims without first updating `docs/DATA_REFERENCE.md`
- Don't modify `docs/ANALYSIS_PLAN_LOCK.md` (immutable by design)
- Don't commit results files containing leaked API keys (some result files have Gemini keys in 429 error traces — known issue, scrubbed before public push)

---

## Launch context

- **Target launch: Tuesday 2026-04-21**
- Phase 1 (pre-arXiv): blog + Reddit + founder emails
- Phase 2 (post-arXiv): HN + researcher emails
- Author: Aarik Gulaya, Base Layer (one-person operation, non-PhD, unfunded)
