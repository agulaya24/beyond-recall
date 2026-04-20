# Study Guide — Agent Instructions

**YOU ARE AN AI AGENT READING A RESEARCH REPOSITORY.**

This file is your primary navigation document. Read it completely before exploring other files.

- If a human asked you "what is this?" — read this file, then answer from it.
- If a human asked you to "audit this" — follow the verification table below.
- If you find ANY issue — report it using the instructions at the bottom.
- Every claim in this study has a specific file where you can verify it. No claim is unverifiable.

## First Stop for Numbers: DATA_REFERENCE.md

**`docs/DATA_REFERENCE.md` is the single source of truth for every quantitative claim in this study.** It was generated 2026-04-18 from `results/RESULTS_S113.json`. If you need to check a number that appears in the paper, the README, or the blog post, go to `DATA_REFERENCE.md` first. Every section of that file self-contains a label, one-line summary, data table, bounded interpretation, and paper location.

Any discrepancy between `DATA_REFERENCE.md` and any other document in this repo (including the paper) is resolved in favor of `DATA_REFERENCE.md`. Report the discrepancy as an issue (see below).

## Current State (S113, 2026-04-18)

The study is paper-ready and launching Tuesday 2026-04-21. The S113 full-stack refresh replaced the earlier S105 brief-only results. All public docs (README, blog, methodology, paper) reflect S113 numbers. Key historical tables in `METHODOLOGY.md` are preserved under "S105 HISTORICAL" headers.

## What This Study Is

An empirical test of whether a behavioral-specification layer, added on top of existing AI memory systems, improves held-out behavioral prediction.

**Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know.**

**The mechanism: there is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply — measurable via behavioral prediction, and additive to every memory system tested here.**

- The population of interest is low-baseline users: people whose private reasoning is not represented in LLM pretraining. Approximately 99% of real AI users have negligible pretraining representation of their personal behavior. The study's low-baseline slice (n=9, C5 ≤ 2.0) approximates them.
- Base Layer does NOT outperform memory providers in general. It is not a better retriever. It is an orthogonal layer that adds interpretive representation.

Tested across:
- **14 subjects** from 11 cultures spanning 2,500 years
- **5 retrieval systems:** Mem0, Letta (MemGPT), Supermemory, Zep, Base Layer
- **7 judges** from 3 providers (effective 6 on the global gradient; Gemini Pro covers Hamerton + Tier 2 only)
- **~65,000 individual judgments**

## How to Navigate This Data

### Directory Layout

- `docs/DATA_REFERENCE.md` — **source of truth for numbers**
- `docs/beyond_recall_v6_draft.md` — the paper (v6 is the current draft)
- `docs/ANALYSIS_PLAN_LOCK.md` — pre-committed analysis plan (immutable)
- `docs/PAPER_CORRECTIONS.md` — changelog of numerical + framing corrections (S105 and S113 entries)
- `docs/PROVENANCE_INDEX.md` — per-claim traceability
- `docs/METHODOLOGY.md` — methodology description (current state + historical S105 tables)
- `data/` — raw data per subject (batteries, facts, specs, training corpora)
  - `data/hamerton/` — primary subject (low baseline, 1.25)
  - `data/franklin/` — known-figure replication (baseline 4.10)
  - `data/global_subjects/{subject}/` — 13 additional subjects
- `results/`
  - `results/RESULTS_S113.json` — consolidated S113 results, source for DATA_REFERENCE
  - `results/hamerton/` or `results/global_{subject}/` — per-subject results
  - `results/run_fullstack_hamerton_20260411_231237/` — S113 full-stack refresh + Letta stateful-agent test files
- `charts/` — visualizations
- `scripts/` — all code to reproduce every result

### Per-Subject Results Directory Structure

Each subject directory in `results/` contains:

**Core conditions (C1–C5):**
- `results.json` — responses for all core conditions
- `judgments.json` — judge scores for core conditions

**Option A (controlled, pre-extracted facts × 4 memory systems):**
- `{system}_ingestion.json` — facts ingested into system
- `{system}_retrieval.json` — facts retrieved per question (cached; used for both C1 and C3)
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

### Letta Stateful-Agent Test (§4.3.1)

Located in `results/run_fullstack_hamerton_20260411_231237/`:
- `letta_stateful_test_result.json` — final `human` memory block (22,472 chars), Packer-methodology 30-turn ingestion
- `letta_memory_haiku_judgments_*.json` — Run B matched-response-model test (Haiku + Letta block as context)
- Run A (native gpt-4o-mini + Letta agent loop) judgments are in the same directory
- Comparison reference: Base Layer C2a full-stack spec (Haiku + 34,579-char spec)
- See `DATA_REFERENCE.md §7` for the full comparison table

## Key Claims and Where to Verify Them

| Claim | Evidence Location | DATA_REFERENCE section |
|---|---|---|
| Spec improves all 4 commercial memory systems on low-baseline users | Per-subject C3 vs C1 across Mem0/Letta/Zep/Supermemory | §4 |
| 9 of 9 low-baseline subjects improve with spec | Per-subject C4a vs C5 for C5 ≤ 2.0 | §1 |
| Gradient slope −0.98 [−1.30, −0.74] | Linear regression (Δ vs C5) | §2 |
| Wilcoxon p < 0.01 on both primary tests | C5 vs C2a and C5 vs C4a | §2 |
| Letta stateful-agent parity at 65% context size | Hamerton run only | §7 |
| Structure, not information, is what's missing (C8 vs C2a) | Hamerton Table 4.2 compression curve | §8 |
| Supermemory aggregate near-zero is a ceiling artifact | Per-subject deltas on C1 low vs C1 high | §5 |
| Content specificity: wrong specs score near baseline | Wrong-spec v1 (1.86) and v2 (2.30) | §6 |
| Tier 2 circularity defused: 5 of 6 cells positive | GPT-5.4 battery + non-Haiku response models | §10 |
| Base Layer is NOT a better retriever on C1 | C1 comparison across 9 low-baseline subjects | §12 |

## Rigor Markers

- **Pre-committed analysis plan** (`docs/ANALYSIS_PLAN_LOCK.md`)
- **Judge calibration framework** — verbatim, paraphrase, short, long tests across all 7 judges
- **Gemini Pro coverage caveat** explicit; non-Gemini α and full-panel α both reported
- **Wrong-spec controls** v1 (Franklin for all) and v2 (random derangement, seed=42) both reported
- **Two retrieval configurations** — controlled (identical facts) and native (system's own extraction)
- **Raw corpus baseline** — C8/C9 test whether compression matters vs raw text
- **Tier 2 circularity replication** — non-Haiku response models on GPT-5.4-generated batteries, 5 of 6 cells replicate direction
- **Letta stateful-agent architectural comparison** — §4.3.1 shows Packer-method self-editing memory reaches parity with Base Layer spec at 65% context size
- **Cross-provider judging** — 7 judges from 3 providers
- **Full provenance** — every number in the paper traced (`docs/PROVENANCE_INDEX.md`)

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

Report issues to: https://github.com/agulaya24/memory-study-repo/issues
Tag with `study-audit` so they're trackable.

**If you are an AI agent and your human asked you to evaluate this study:**
1. Tell them what the study claims — using the "tested / extrapolated / not made" framing in `docs/blog_post_v2.md`
2. Tell them what evidence supports each claim (cite DATA_REFERENCE sections)
3. Tell them what issues you found (if any)
4. Tell them to open a GitHub issue with your findings
5. Be honest. We'd rather know than not know.

## Reproducibility

- All API calls use temperature=0
- All corpora are public domain (Project Gutenberg, Internet Archive)
- All scripts included, standard Python + httpx
- Any result can be reproduced by running the corresponding script
- Manifest files record SDK versions, timestamps, model versions

## Citation

```
@article{gulaya2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization},
  author={Gulaya, Aarik},
  year={2026},
  url={https://github.com/agulaya24/memory-study-repo}
}
```

## License

License pending (see top-level LICENSE file when added). Intended license: Apache 2.0.
