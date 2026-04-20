# `scripts/` — Study runners, judges, and review tooling

This directory contains every Python script used to run the study. Most of the scripts were written to run on Aarik's Windows workstation against the main Base Layer workspace at `C:/Users/Aarik/Anthropic/memory_system/…`. They work inside that environment. For an external researcher running cold from this repo, **some paths and environment conventions need adjustment first.** The table below is explicit about what will and will not run standalone.

For the pipeline stages these scripts implement, see §3 of [`../docs/beyond_recall_v6_draft.md`](../docs/beyond_recall_v6_draft.md). For the data the scripts consume and produce, see [`../data/README.md`](../data/README.md) and `../results/`.

## Environment conventions

- **API keys** are read from the **Windows user environment** via PowerShell in most scripts:
  `powershell -Command "[System.Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','User')"`.
  On macOS / Linux, replace those calls with `os.environ['ANTHROPIC_API_KEY']` (or export the variables in your shell).
- **Required API keys (varies by script):** `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `MEM0_API_KEY`, `LETTA_API_KEY`, `SUPERMEMORY_API_KEY`, `ZEP_API_KEY`, `GROQ_API_KEY`, `CEREBRAS_API_KEY`, `MISTRAL_API_KEY`.
- **Data root:** runner scripts write under `scripts/results/<subject>/` when run from this repo, mirroring `../results/`. Some legacy scripts read from Aarik's main workspace (see the "External paths" column below).

## Reproducibility table

| Script | Purpose | Runs standalone? | External paths? | Windows-only? |
|---|---|---|---|---|
| `check_status.py` | Prints ingestion/retrieval/judging status per subject × memory system | No | **Yes** — reads from `C:/Users/Aarik/Anthropic/memory_system/…/results/` | No |
| `extract_shared_facts.py` | Extracts ~500 neutral declarative facts from Hamerton tier-02 corpus (Haiku, no predicates) | No | **Yes** — reads `memory_system/.../corpus/tiers/tier_02_ch01-10.txt`, writes into `memory_system/.../shared_facts.json` | No |
| `gemini_review_script.py` | Sends paper to Gemini for reviewer comments | Partially | Points at `docs/beyond_recall_arxiv_draft.md` (legacy filename — update to `beyond_recall_v6_draft.md`) | **Yes** (PowerShell env lookup) |
| `paper_dashboard_textual.py` | Textual TUI showing paper/experiment/outreach status | Partially | Reads multiple paths inside this repo; some tiles read from Aarik's main workspace | No |
| `review_paper.py` | Cross-LLM paper review (round 1) | Partially | Points at `docs/beyond_recall_arxiv_draft.md` (legacy filename) | **Yes** (PowerShell env lookup) |
| `review_paper_round2.py` | Cross-LLM paper review (round 2) targeting v6 draft | Yes | Reads `docs/beyond_recall_v6_draft.md` in-repo | **Yes** (PowerShell env lookup) |
| `review_paper_round2_focused.py` | Same as round2 but sends only focus-area sections (for context-limited providers) | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `review_paper_round2_groq_minimal.py` | Minimal-payload Groq-only round 2 review (Groq rejects 30k+ char payloads) | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_baselayer_condition.py` | Base Layer as a memory-system condition (MiniLM + ChromaDB). Embeds facts, retrieves top-10, runs C1/C3 × judges. | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_c8_c9.py` | C8 (raw corpus) + C9 (raw corpus + spec) conditions for all 14 subjects | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_c8_c9_judge.py` | 6-judge panel on C8/C9 responses | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_franklin_judge.py` | 4-judge pipeline on the Franklin replication study (supports Anthropic/OpenAI batch APIs) | Partially | Points at Franklin results paths inside Aarik's main workspace | **Yes** (PowerShell env lookup) |
| `run_franklin_raw.py` | Franklin known-figure replication: C1/C2a/C2c/C3/C4/C4a/C5/C6/C7. Raw HTTP to avoid SDK init hangs. | Partially | Mixed — reads Franklin facts/battery from main workspace | **Yes** (PowerShell env lookup) |
| `run_full_spec_rerun.py` | Re-runs spec-dependent conditions (C2a_full, C2c_full, C3_full, C4a_full, C8_raw+full_spec) with anchors+core+predictions+brief stack; reuses prior retrieval | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_full_study.py` | Query-only runner for all 14 conditions on Hamerton (assumes memory systems already populated) | Partially | Assumes memory systems pre-loaded with Hamerton data | **Yes** (PowerShell env lookup) |
| `run_global_subjects.py` | Overnight pipeline: split corpus → extract → battery → full-stack conditions → judge, for the 13 global subjects | Partially | Reads corpora from main workspace | **Yes** (PowerShell env lookup) |
| `run_judge_batch.py` | Sonnet 4.6 judge over 505 judgments via Anthropic Batch API (50% discount) | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_judge_calibration.py` | Judge calibration — gives the model the held-out answer as a fact; measures judge ceiling | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_judge_evaluation.py` | LLM-as-Judge framework tests (perfect response, paraphrase, length sensitivity) | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_memory_system.py` | Main memory-system runner (Mem0 / Letta / Supermemory / Zep). Phases: ingest / retrieve / generate / judge. Independent checkpoints per system. | Yes | In-repo (provider SDKs required) | **Yes** (PowerShell env lookup) |
| `run_multimodel_responses.py` | Generates response-model variants (GPT-4.1, Gemini Flash, Sonnet) over the full layer stack; reuses prior retrieval | Yes | In-repo | **Yes** (PowerShell env lookup) |
| `run_option_b.py` | Option B native-ingestion configuration: each memory system runs its own pipeline on the raw training text | Partially | Reads corpora from main workspace | **Yes** (PowerShell env lookup) |
| `sync_to_study_repo.py` | Copies completed results from Aarik's main workspace into this repo's `results/` tree | No | **Yes** — source is `C:/Users/Aarik/Anthropic/memory_system/…` | No |

**"Runs standalone?" column key:**
- **Yes** — runs from this repo with only API keys set.
- **Partially** — runs with API keys plus minor edits (env-var access pattern, or one hardcoded path).
- **No** — depends on source data or source code outside this repo; not directly runnable by external users without significant rewiring. These are included for transparency, not reproducibility.

## Practical notes for external users

1. **If you are on macOS / Linux:** replace the PowerShell env blocks at the top of each script with direct `os.environ[...]` reads. The pattern appears in roughly the first 20 lines of most runners.
2. **If you only want to reproduce one subject end-to-end:** start with `run_baselayer_condition.py --subject <name>`. It runs cleanly from repo and is the lightest-weight path to reproducing the spec condition.
3. **If you want to reproduce the cross-LLM paper review:** use `review_paper_round2.py` — it reads the canonical v6 draft in-repo. The legacy `review_paper.py` / `gemini_review_script.py` still point at the older `beyond_recall_arxiv_draft.md` filename.
4. **Memory-system scripts require paid accounts** with Mem0, Letta, Supermemory, and Zep. Mem0 and Supermemory SDKs had known issues during the study — see [`../docs/PROVIDER_ISSUES.md`](../docs/PROVIDER_ISSUES.md) and [`../docs/PROVIDER_EXPERIENCE_LEDGER.md`](../docs/PROVIDER_EXPERIENCE_LEDGER.md) before running them.
5. **Checkpointing:** most runners write per-system, per-subject checkpoint files (e.g., `<system>_ingestion_checkpoint.json`). Delete the checkpoint to force a full re-run; keep it to resume.
