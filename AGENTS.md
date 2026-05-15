# AGENTS.md — Navigation for AI Agents

You are reading the companion repository for the paper **"Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"** (Aarik Gulaya, Base Layer, 2026). This file tells you how the repo is laid out, where the authoritative numbers live, how to verify claims, and how to report problems.

If you are a human reader, start with [README.md](README.md).

## What this repo is

This repo contains the paper, the data the paper was scored on, the scripts that produced the numbers, the pipeline snapshot used to author the 14 specifications, and a knowledge index optimized for agent queries. Everything in the paper is reproducible from artifacts in this repo. If a paper claim does not have a recompute pointer in [`docs/PROVENANCE_INDEX.md`](docs/PROVENANCE_INDEX.md), treat it as a bug and file under "How to report problems" below.

## What to read first

| Goal | File |
|---|---|
| Read the paper | [`build/beyond_recall.pdf`](build/beyond_recall.pdf) |
| Verify a numerical claim | [`docs/DATA_REFERENCE.md`](docs/DATA_REFERENCE.md) and the recompute pointer in [`docs/PROVENANCE_INDEX.md`](docs/PROVENANCE_INDEX.md) |
| Understand a finding | [`docs/KEY_FINDINGS.md`](docs/KEY_FINDINGS.md) |
| Methodology details | §3 of the paper + [`REPRODUCE.md`](REPRODUCE.md) |
| Open quality-audit findings | [`ISSUES.md`](ISSUES.md) |
| Search the repo semantically | [`workspace/study_knowledge.db`](workspace/study_knowledge.db) + [`workspace/study_vectors/`](workspace/study_vectors/) (build/search with `scripts/index_study_repo.py`) |
| Query the indexed knowledge base | MCP server at [`mcp/`](mcp/) |

## Repository layout

```
build/         LaTeX source + final PDF + bibliography
data/          Source corpora (Project Gutenberg / Internet Archive) + per-subject batteries, facts, specifications
results/       Per-judge judgments, retrieval logs, response caches per subject x condition
scripts/       Recompute, sensitivity, audit scripts (one per §4 claim)
docs/          Methodology, provenance index, data reference, findings catalog, research artifacts
figures/       Paper figures (PNG + generators)
baselayer/     Pipeline source snapshot used to author the 14 specifications scored in §4
mcp/           MCP server exposing the indexed knowledge base
workspace/     SQLite + ChromaDB index over the full repo
agents/        Agent-onboarding files (study-guide.md, STUDY_MEMORY.md)
```

## Single source of truth

**[`docs/DATA_REFERENCE.md`](docs/DATA_REFERENCE.md)** is the canonical source for every number in the paper. If a number in the paper differs from `DATA_REFERENCE.md`, `DATA_REFERENCE.md` is correct.

For per-claim recompute, [`docs/PROVENANCE_INDEX.md`](docs/PROVENANCE_INDEX.md) names the script and data file behind each claim. To verify a specific claim:

1. Locate the claim in the paper (e.g., "mean Δ_C4a = +0.89 on 9 low-baseline subjects")
2. Find it in `DATA_REFERENCE.md` (search by section reference)
3. Find the recompute pointer in `PROVENANCE_INDEX.md`
4. Run the script. It should produce the same number to two decimals.

If your recompute disagrees with the paper, file an issue per the section below.

## Working policies

- **Read before you act.** Any script that modifies data, deletes files, or hits an external API: read it first.
- **Never run destructive operations (delete / reset / clear) without confirming.** Even in a sandbox.
- **The paper is preprint-locked.** Suggesting changes is fine; making changes requires the author.
- **Cite by section number.** When referring to claims, cite the paper section (§4.1, §4.4.2, etc.). Section numbers are stable across the paper.
- **All response models, judges, and battery generators in the study are LLMs.** This is acknowledged class-level circularity (§6.2). Human annotation on a stratified subset is the leading follow-up; until then, treat magnitudes as directional.

## How to verify a claim end-to-end

Example: "On the 9 low-baseline subjects, the Behavioral Specification produces a mean Δ_C4a of +0.89 points."

1. Paper claim location: §4.1 "Per-subject results" table.
2. `DATA_REFERENCE.md` confirms: mean Δ_C4a (low-baseline, 5-judge primary) = +0.89.
3. `PROVENANCE_INDEX.md` points to `scripts/recompute_5judge_primary.py` and `results/global_<subject>/judgments_v2.json`.
4. Run: `python scripts/recompute_5judge_primary.py`. Output should include `mean_delta_c4a_low_baseline = 0.89`.
5. Per-judge breakdown: `results/global_<subject>/judgments_v2.json` for any of the 9 low-baseline subjects.

If step 4 produces a different number than the paper, that is a bug. File it.

## How to report problems

If you find a discrepancy between the paper and the data, an unreachable script reference, a stale path, or an empirical claim that the data does not support:

1. Open an issue at [`github.com/agulaya24/beyond-recall/issues`](https://github.com/agulaya24/beyond-recall/issues) with the section of the paper, the specific claim, the recompute you ran, and the disagreement.
2. Or, if you are an agent inside a longer session, append a structured entry to [`ISSUES.md`](ISSUES.md) under a new top-level item with: date, section reference, claim, observed disagreement, recompute steps, suggested resolution.

Issues with reproducible disagreement are higher priority than stylistic findings.

## Related artifacts

- **Pipeline source (deployed):** [`github.com/agulaya24/BaseLayer`](https://github.com/agulaya24/BaseLayer). Stable production version. The study-specific snapshot is preserved at [`baselayer/`](baselayer/) in this repo.
- **Project page:** [`base-layer.ai`](https://base-layer.ai). Vision essay, examples, blog.
- **Author:** Aarik Gulaya. ORCID [`0009-0009-5902-9557`](https://orcid.org/0009-0009-5902-9557). Contact `aarik@base-layer.ai`.

## License

Apache 2.0 for code. CC-BY-4.0 for manuscript and analyses. Source autobiographies are public domain.
