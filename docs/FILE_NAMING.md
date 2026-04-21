# Navigating This Repo — A Plain-Language Guide

Last updated 2026-04-21 (S114).
Last reviewed: 2026-04-28 (v11 freeze). Naming conventions, subject list, condition list, and judge panel are unchanged from v11. The "Where to look" table near the bottom still references the v8 draft and the S113 / S114 aggregate filenames; the v11-canonical paper is `docs/beyond_recall_v11_draft.md` and the v10.1 preserved baseline sits next to it. v8 / v9 / v10 drafts moved to `docs/versions/_pre_v11_drafts/` in the v11 cleanup.

Read this if you are coming back to the repo after time away, or if you are new and want to find something quickly without needing to know the jargon.

---

## What this repo is

This is the companion to a research paper called **"Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization."** The paper asks: *can you make an AI respond more like a specific person by handing it a short document that describes how that person thinks, rather than handing it all their raw writing?*

To answer that, we tested 14 historical figures (plus Benjamin Franklin as a reference case), wrote up a "behavioral specification" for each one, and asked an AI to predict what that person would say in situations they actually wrote about — with and without the specification, with and without retrieval from memory systems.

This repo holds every input, every AI response, every judge score, every analysis, every paper draft, and every piece of data the paper cites.

---

## The three folders that matter most

If you are trying to orient quickly, these three folders answer three different questions:

- **`docs/`** — "What does the paper say?" Paper drafts, findings summaries, and numbers references live here.
- **`data/`** — "What did we feed into the experiment?" Each subject's source writing, the questions we asked, the behavioral specification we wrote.
- **`results/`** — "What came out of the experiment?" Every AI response, every judge's score, every computed result.

Three supporting folders:

- **`scripts/`** — The code that ran the experiments and analysis.
- **`figures/`** and **`charts/`** — Visualizations used in the paper.
- **`agents/`** — Instructions for AI agents (like Claude Code) working on this repo.

---

## What a "subject" is

A subject is one of the 14 people whose behavior we tried to predict. Each subject has:

- A source corpus (their autobiography or memoir) split 50/50 into a training half and a held-out half.
- A behavioral specification — roughly 5,000 to 8,000 tokens of structured text about how this person reasons.
- A battery of ~39-40 behavioral-prediction questions pulled from the held-out half.
- A pile of AI responses to those questions under different conditions.
- A pile of judge scores rating how well each response matches what the person actually wrote.

**Subjects:**

13 "global" subjects: augustine, babur, bernal_diaz, cellini, ebers, equiano, fukuzawa, keckley, rousseau, seacole, sunity_devee, yung_wing, zitkala_sa.

1 main subject: hamerton (Philip Gilbert Hamerton — the lowest-baseline subject in the original pilot; extra analyses were run on him first).

1 known-figure control: franklin (Benjamin Franklin — a widely-represented historical figure; used to show the AI already "knows" him well, so the specification doesn't help).

1 exploratory: franklin_obscure (lesser-known letters of Franklin; ignore unless specifically needed).

---

## What a "condition" is

A condition is one experimental setting — one specific combination of inputs served to the AI. The condition IDs look cryptic but each one answers a specific question:

| Condition | In plain terms | What it tests |
|---|---|---|
| `C5_baseline` | No extra context. AI answers from its pretraining alone. | How much the AI already knows about this person. |
| `C2a_full_spec` | Only the behavioral specification, no facts. | Whether the specification alone improves prediction. |
| `C2c_wrong_spec` | A different person's specification assigned to this subject. | Whether it's the *correct* specification that matters, not any structured prompt. |
| `C4_factdump` | All extracted facts about the person, no specification. | Whether raw information substitutes for structure. |
| `C4a_full_facts_plus_spec` | Facts + specification. | Whether the specification adds value on top of raw facts. |
| `C8_raw_corpus` | The entire training corpus (half of the person's source text). | Whether more text beats structured compression. |
| `C9_raw_corpus_plus_spec` | Corpus + specification. | Whether the specification adds value on top of raw text. |
| `C1_<system>` | A memory system's retrieval output (like Mem0 or Zep retrieving relevant facts). | Whether retrieval alone reaches the specification's performance. |
| `C3_<system>` | A memory system's retrieval + specification. | Whether the specification composes on top of retrieval. |

Five memory systems are tested: `mem0`, `letta`, `supermemory`, `zep`, and `baselayer` (our own reference stack).

Two ingestion setups per commercial system: **controlled** (each system given an identical pre-extracted fact list) and **native** (each system runs its own ingestion pipeline). Native-config files have `_fullpipeline` or `_fp` in their name.

---

## What a "judge" is

A judge is an LLM that scored each AI response 1-5 against the verbatim held-out ground-truth passage. Seven judges across three providers were used:

- **Anthropic:** Haiku 4.5, Sonnet 4.6, Opus 4.6
- **OpenAI:** GPT-4o, GPT-5.4
- **Google:** Gemini 2.5 Flash, Gemini 2.5 Pro

The 5-judge primary panel excludes the two Gemini judges, because Gemini Pro failed calibration diagnostics and inflated absolute scores. The 7-judge aggregate is reported as a sensitivity check. §3.7.2 of the paper explains in detail.

---

## How files are named

Naming rules (if you are reading a filename and want to decode it):

1. **Subject first, then system, then condition, then role.**
   - Example: `mem0_fullpipeline_judgments_gpt4o.json` = Mem0 system, native config, judgments by GPT-4o.
2. **Conditions use the C-number naming above** (e.g. `C5_baseline`, `C2a_full_spec`).
3. **Judges use short names** (no capitals, no dots): `haiku`, `sonnet`, `opus`, `gpt4o`, `gpt54`, `gemini_flash`, `gemini_pro`.
4. **Versioned files keep `_v2` or `_v3` suffixes** — earlier versions retained for provenance, not deleted.
5. **Folders with a leading underscore are computed-off-the-main-tree**: `_tier2/`, `_wrong_spec_v2/`, `_s114_backfills/`, `_letta_blocks/`. These are experimental controls or backfill outputs kept separate from the main per-subject data.
6. **Session backfills end with a session tag.** Example: `baselayer_judgments_gpt4o_s114.json` = S114 rerun for the Base Layer / GPT-4o cell.
7. **Consolidated aggregates at the top of `results/` use `RESULTS_S<session>.json`.** `RESULTS_S113.json` was the last big aggregate; `RESULTS_S114.json` will appear once the S114 backfills finish and the 5-judge primary numbers are locked.

---

## Where to look for each kind of thing

| If you want… | Look at… |
|---|---|
| The paper draft | `docs/beyond_recall_v8_draft.md` (current) or `docs/beyond_recall_v6_draft.md` (frozen older). |
| The "what every number means" reference | `docs/DATA_REFERENCE.md`. |
| A specific person's raw source text | `data/global_subjects/<subject>/heldout.txt` and `training.txt` (or `data/hamerton/` for Hamerton). |
| A person's behavioral specification | `data/global_subjects/<subject>/spec_production.md` or `data/hamerton/spec/`. |
| A person's AI responses for a specific condition | `results/global_<subject>/results_v2.json` (direct conditions) or `results/global_<subject>/<system>_results.json` (memory-system conditions). |
| Judge scores for a specific condition × judge | `results/global_<subject>/<system>_judgments_<judge>.json`. |
| The consolidated numbers the paper cites | `results/RESULTS_S113.json` (current) or `results/RESULTS_S114.json` (pending). |
| The circularity-control data (Tier 2) | `results/_tier2/`. |
| The wrong-spec control data | `results/_wrong_spec_v2/`. |
| The Letta stateful-agent experiment | `docs/research/_letta_blocks/` and `docs/research/_letta_rerun/`. |
| The latest cross-LLM review of the paper | `docs/reviews/`. |
| The paper's findings catalog | `docs/KEY_FINDINGS.md`. |
| Scripts to re-run any analysis | `scripts/`. |

---

## Gotchas

- **Parse failures are encoded as `score: 0, parse_failure: true`** in the judgment files. If you aggregate without filtering on `parse_failure`, you'll get wrong numbers. The 5-judge primary recompute script handles this correctly.
- **The canonical aggregate `RESULTS_S113.json` was generated using a 7-judge flat aggregate, not the 5-judge primary the paper uses.** The S114 recompute re-does this correctly; use `docs/research/recompute_5judge_primary.md` until `RESULTS_S114.json` is finalized.
- **Hamerton and Franklin have some files in `data/` that the 13 globals don't have there** (batteries, facts). Hamerton/Franklin use a slightly different layout because they were the first two subjects in the pipeline and kept their original structure.
- **Supermemory native ingestion failed for 4 subjects** (babur, bernal_diaz, cellini, rousseau). Their `C1_supermemory_fp` responses are empty. This is an ingestion-level failure, not a judge issue.
- **12 of 13 globals had sustained 429 rate-limits from OpenAI and Google** during the original Base Layer judgment runs. S114 backfills those.

---

## Every folder has (or will soon have) its own README

Each folder-level README covers:

- What's in the folder.
- The naming pattern for its files.
- What the folder's data feeds into downstream.
- Any caveats specific to that folder.

If you are adding a new folder, add its README in the same commit. Keep the language plain.

---

## When numbers disagree

Three rules of thumb for resolving conflicts between sources in this repo:

1. **Raw per-judge JSON files are ground truth.** If a report number doesn't match what the raw files produce under the locked aggregation rule, trust the raw files.
2. **The 5-judge primary is the reporting default going forward.** The 7-judge sensitivity is reported alongside where Gemini inclusion materially shifts a number.
3. **`DATA_REFERENCE.md` is being updated to match the S114 5-judge primary recompute.** Until that update lands, cross-check against `docs/research/recompute_5judge_primary.md` for §4-bound numbers.
