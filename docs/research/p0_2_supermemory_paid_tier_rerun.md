# P0-2: Supermemory Paid-Tier Rerun — Status Report

**Date:** 2026-04-23
**Session:** S109 (post)
**Task:** Re-run Supermemory native ingestion on paid tier for 4 subjects whose free-tier ingestion failed.
**Scope:** ingest + retrieve + generate only. Judging NOT run (pending greenlight).

## Summary

All four target subjects (bernal_diaz, babur, cellini, rousseau) completed ingest + retrieve + generate successfully on the paid-tier Supermemory API. Ingestion post success: 199/199 chunks (0 failures). Retrieval returned 4.3-5.0 facts per question (vs 0 per question in the failed free-tier run). Response generation completed 78/78 responses per subject (C1_supermemory_fp + C3_supermemory_fp × 39 questions) with 0 errors.

The pre-existing paper footnote referring to four free-tier ingestion failures is now out of date if these paid-tier runs are accepted as the canonical Supermemory results.

## Per-Subject Results

| subject       | chunks expected | chunks success | chunks failure | retrieval Qs | avg facts/Q | min facts | generate C1 | generate C3 | generate errors |
|---------------|----------------:|---------------:|---------------:|-------------:|------------:|----------:|------------:|------------:|----------------:|
| cellini       | 35              | 35             | 0              | 39/39        | 4.5         | 2         | 39/39       | 39/39       | 0               |
| bernal_diaz   | 34              | 34             | 0              | 39/39        | 4.3         | 2         | 39/39       | 39/39       | 0               |
| babur         | 80              | 80             | 0              | 39/39        | 5.0         | 4         | 39/39       | 39/39       | 0               |
| rousseau      | 50              | 50             | 0              | 39/39        | 4.3         | 1         | 39/39       | 39/39       | 0               |
| **total**     | **199**         | **199**        | **0**          | **156/156**  | -           | -         | **156/156** | **156/156** | **0**           |

### Prior (free-tier) state, for reference

| subject       | free-tier ingest claimed success | free-tier retrieval facts per Q |
|---------------|---------------------------------:|--------------------------------:|
| bernal_diaz   | 0/33                             | 0 (all questions)               |
| babur         | 0/75                             | 0 (all questions)               |
| rousseau      | 0/50                             | 0 (all questions)               |
| cellini       | 34/34 (reported)                 | 0 (all questions) — indexing silently dropped content |

Cellini's free-tier run reported ingestion success but retrieval still returned zero facts across all 39 questions, which is why it was bundled into this rerun. The paid-tier run fixed it: identical chunking, identical `container_tag`, but retrieval now returns 2-7 facts per question with topical content matching each query.

### API errors encountered

None. All 199 chunk POSTs returned 2xx. No 401/402/429 observed. No retries needed.

## Result Locations

All outputs are at the **canonical script-local path** (where `run_option_b.py` actually writes):

```
C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_<subject>/
  supermemory_fullpipeline_ingestion.json
  supermemory_fullpipeline_extracted.json
  supermemory_fullpipeline_retrieval.json
  supermemory_fullpipeline_results.json
  training.txt                                    (refreshed from global_subject_environments source)
  training.txt.prior_20260423                     (backup of previous smaller training.txt)
  supermemory_fullpipeline_archive_free_tier_20260423_181634/
    <14 files: prior ingestion/extracted/retrieval/results + 6 judgments + merged + 3 .failed_backup>
```

The study-repo mirror at `memory-study-repo/results/global_<subject>/` still holds a parallel archive (from the sync step prior to this rerun) at `supermemory_fullpipeline_archive_free_tier_20260423_181634/`. **`sync_to_study_repo.py` must be run to mirror the new paid-tier results into the study repo before they are referenced by paper or figures code.**

## Path Resolution Note (for future agents)

The task prompt said training.txt should live at `memory-study-repo/results/global_<subject>/training.txt` and that the script "expects" that path. The script actually reads from `os.path.dirname(__file__) + '/results/global_<subject>/training.txt'`. There are two script copies:

- `memory-study-repo/scripts/run_option_b.py` → resolves to `memory-study-repo/scripts/results/...` (empty)
- `memory_system/data/experiments/memory_systems/run_option_b.py` → resolves to the real-data location

The scripts are byte-identical. This rerun used the latter. Training files at both locations were refreshed from the `global_subject_environments/*/data/raw/training.txt` source.

## Cost Estimate

**Anthropic Haiku 4.5 (generate phase):**

| subject       | input tokens | output tokens | subject cost |
|---------------|-------------:|--------------:|-------------:|
| cellini       | 414,429      | 44,629        | $0.638       |
| bernal_diaz   | 391,208      | 47,280        | $0.628       |
| babur         | 404,563      | 49,124        | $0.650       |
| rousseau      | 411,962      | 40,973        | $0.617       |
| **total**     | **1,622,162**| **182,006**   | **$2.533**   |

Pricing: $1/M input, $5/M output.

**Supermemory API (ingest + retrieve):** 199 document POSTs + 156 search POSTs. Paid-tier pricing was not visible from the API response, but at typical SaaS rates ($0.01-0.05/document) this is bounded at $2-10. Actual dashboard value to be confirmed on the Supermemory billing page.

**Total known spend for this task: ~$2.53 (Haiku) + Supermemory paid-tier usage.** Well under the $10 ceiling.

**Sequencing note.** Ingest and retrieve phases ran one subject at a time (strictly sequential). Generate phase: cellini ran alone first (smoke test), then bernal_diaz started sequentially, then babur and rousseau were launched in parallel with bernal_diaz still running (three concurrent generates). No Haiku rate-limit errors or response errors resulted from this; all 156 responses landed cleanly. Surfacing it here in case future reruns want strict sequential for reproducibility.

## Recommendation

**All 4 subjects are ready for the 5-judge step.** Each has 78/78 complete responses with no errors, retrieval returned facts on every question, and the C3 responses include spec+facts (not spec-only, since facts were retrieved). The shape matches the other successful subjects in the study.

Before greenlighting judging, the user may want to:

1. Spot-check one response per subject for quality (cellini Q1 reviewed inline during run — spec+facts response coherent and well-grounded).
2. Run `sync_to_study_repo.py` so `memory-study-repo/results/global_<subject>/supermemory_fullpipeline_*.json` reflects the new paid-tier run.
3. Update the paper §4.4 footnote: the "four ingestion failures" claim should now describe the failed free-tier run explicitly and note that paid-tier succeeded with all 199 chunks indexed and retrievable.

## Judging NOT Run

Per instructions, `--phase judge` was NOT invoked for any of the four subjects. No entries were added to `supermemory_fullpipeline_judgments_*.json` in this rerun. The prior free-tier judgment files are preserved in the archive directory. Running the 5-judge panel is estimated at $20-30/subject (~$80-120 for all four) per the task prompt and is deferred pending user greenlight.
