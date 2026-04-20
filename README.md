<!-- IF YOU ARE AN AI AGENT: Start with agents/study-guide.md — it tells you how to navigate this repo, verify every claim, and report issues you find. The single source of truth for every number is docs/DATA_REFERENCE.md. -->

# Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization

> **If you're an AI agent reading this repository**, see [agents/study-guide.md](agents/study-guide.md) for structured navigation, claim verification paths, and issue reporting instructions. The single source of truth for every number in this repo is [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md).

## The Flagship Claim

**Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know.**

The mechanism: **there is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply — measurable via behavioral prediction, and additive to every memory system tested here.**

This study tests whether a behavioral specification (a compressed, structured model of how someone reasons) adds predictive accuracy when layered on top of state-of-the-art memory systems. It does. The effect is a gradient in the baseline: the less the model already knows about the subject from pretraining, the more the spec helps.

## The Claim — Tested, Extrapolated, Not Made

- **Tested (primary result):** Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know.
- **Extrapolated:** ~99% of real AI users are the users the model doesn't already know. The study's low-baseline slice (n=9) approximates them.
- **Not made:** Base Layer does not outperform memory providers in general. It isn't a better retriever. It's an orthogonal layer.

## What This Study Is — And Is Not

- It **is** a test of a behavioral-specification layer as an additive primitive on top of existing memory systems.
- It **is not** a benchmark of memory systems against each other.
- It **is not** a claim that Base Layer outperforms memory providers in general — it doesn't, and it's not supposed to.
- **Base Layer is an orthogonal layer**, not a replacement retriever.

## The Population That Matters

The 9 "low-baseline" subjects (C5 ≤ 2.0) are the sample subset whose baseline is low enough to matter. The population *outside* this study — living people with private decisions not in any training corpus — is overwhelmingly low-baseline by construction. Approximately **99% of real AI users have negligible pretraining representation of their personal behavior**. The low-baseline slice is the operationally relevant population for real deployment; everything else is a sub-analysis.

## Study Scale

- **14 public-domain autobiographical subjects** from 11 cultures spanning 2,500 years (Augustine of Hippo to Zitkala-Sa)
- **5 retrieval systems tested:** Mem0, Letta (MemGPT), Supermemory, Zep, Base Layer
- **Two memory-system configurations:** controlled (identical pre-extracted facts) and native (each system's own ingestion)
- **7 judges, 3 providers:** Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google). Gemini Pro has limited coverage (Hamerton + Tier 2 only); effective 6-judge panel on the global gradient.
- **6 response models** across conditions; primary response model Haiku 4.5
- **~65,000 individual judgments**

## Key Findings

See [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md) for the authoritative numbers and CIs. The summaries below are paraphrases; the source of truth is the data reference.

### 1. The gradient: the less the model knows, the more the spec helps

On the 9 low-baseline subjects (C5 ≤ 2.0 — the population of interest), the spec improves prediction on **9 of 9**. Across all 14 subjects (including 5 higher-baseline), 12 of 14 show positive lift from spec+facts; the two negatives (Zitkala-Sa, Equiano) sit at the top of the low-baseline-adjacent range, consistent with the gradient mechanism. Linear regression of Δ on C5 baseline yields slope −0.98 [95% CI −1.30, −0.74].

### 2. The spec improves every commercial memory system — on the users the model doesn't already know

In the controlled configuration on the 9 low-baseline subjects, adding the behavioral specification to retrieved facts produces **positive mean delta on all four commercial systems**: Mem0 +0.13, Letta +0.23, Zep +0.20, Supermemory +0.004, plus Base Layer +0.13. Aggregated across all 14 subjects, Supermemory's spec-delta is near-zero (−0.04 controlled, −0.11 native) — a ceiling artifact: on subjects where Supermemory's own retrieval has already saturated, the spec has no headroom to add. See DATA_REFERENCE §3–§5.

### 3. Information is not what's missing — structure is

On Hamerton, a 7K-token spec (C2a, score 3.04) outperforms 34K tokens of raw corpus (C8, score 2.32) and matches spec-augmented raw corpus (C9, 3.22). The raw corpus contains every fact the spec is derived from. The model cannot extract interpretive structure from unstructured text alone. See DATA_REFERENCE §8.

### 4. Letta's stateful-agent path produces a parity result at 65% context size (n=1, Hamerton)

When Letta's stateful-agent path is invoked properly (30-turn ingestion with self-editing memory blocks, per Packer et al.), it produces a 22,472-character `human` memory block that predicts **3.24** (matched response model, 6 judges) vs Base Layer's full-stack spec at **3.04** — at 65% the context size. This is architectural convergence on the same finding reached by two independent methods: the value is in compressed interpretive representation. Single-subject result (Ebers follow-up in flight). See DATA_REFERENCE §7.

### 5. Content specificity matters — wrong specs score near baseline

Wrong-spec v1 (Franklin's spec applied to 13 other subjects): 1.86 (−0.16 vs baseline). Wrong-spec v2 (random derangement, seed=42): 2.30 (+0.28 vs baseline, but −0.25 vs correct spec). Neither reaches correct-spec scores. See DATA_REFERENCE §6.

### 6. Statistical robustness

- Wilcoxon signed-rank, C5 vs C2a (N=14): W=10.0, p=0.0076
- Wilcoxon signed-rank, C5 vs C4a (N=14): W=9.0, p=0.0063
- Regression slope on gradient: −0.98 [−1.30, −0.74]
- Krippendorff α = 0.535 across all 7 judges (ordinal, moderate); 0.659 across non-Gemini 5-judge panel (substantial)

## Experimental Conditions

| Condition | Description |
|---|---|
| C1_{system} | Retrieved facts only (no spec), per memory system |
| C2a | Spec only (no facts) |
| C3_{system} | Spec + retrieved facts (per memory system) |
| C4 | All extracted facts, no spec |
| C4a | All extracted facts + spec |
| C5 | Baseline (no context — model only) |
| C8 | Raw training corpus in context |
| C9 | Raw training corpus + spec |
| C2c v1 | Franklin's spec applied to the other 13 subjects (wrong-spec control) |
| C2c v2 | Random-derangement wrong-spec (seed=42) |

Memory-system conditions run in two configurations:
- **Option A (controlled):** identical pre-extracted fact set given to every system
- **Option B (native):** raw corpus fed to each system's own ingestion pipeline

## Repository Structure

```
data/
  hamerton/                       # Primary subject (low baseline, 1.25)
    battery.json                  # 80 questions with held-out passages
    facts.json                    # 462 extracted facts
    spec/                         # Behavioral specification layers
  franklin/                       # Known-figure replication
  franklin_obscure/               # Cross-corpus test (letters)
  global_subjects/                # 13 subjects across 11 cultures
    augustine/ babur/ bernal_diaz/ cellini/ ebers/ equiano/
    fukuzawa/ keckley/ rousseau/ seacole/ sunity_devee/
    yung_wing/ zitkala_sa/

results/
  hamerton/                       # Full results for all conditions
  run_fullstack_hamerton_*/       # S113 full-stack refresh + Letta stateful-agent test
  franklin/                       # Franklin responses + judge scores
  global_{subject}/               # Per-subject results
  multimodel/                     # Sonnet, GPT-5.4, Gemini response models
  judge_calibration/              # Calibration tests across judges
  RESULTS_S113.json               # Consolidated S113 results (source for DATA_REFERENCE)

scripts/
  run_full_study.py               # Main study runner
  run_full_spec_rerun.py          # Full-stack spec rerun
  run_global_subjects.py          # Global subjects pipeline
  run_multimodel_responses.py     # Multi-model response generation
  run_judge_batch.py              # Batch judging
  review_paper.py                 # Cross-LLM paper review

docs/
  DATA_REFERENCE.md               # SINGLE SOURCE OF TRUTH for all numbers
  beyond_recall_v6_draft.md       # Full research paper (v6 draft)
  METHODOLOGY.md                  # Full methodology and conditions
  PROVENANCE_INDEX.md             # Every number traced to source file
  PAPER_CORRECTIONS.md            # Corrections changelog (S105 + S113)
  ANALYSIS_PLAN_LOCK.md           # Pre-committed analysis plan
  PROVIDER_EXPERIENCE_LEDGER.md   # Working with each memory system API
  PROVIDER_ISSUES.md              # Technical issues per system
  blog_post_v2.md                 # Blog post (launch artifact)

charts/                           # Visualizations
agents/
  study-guide.md                  # Agent navigation guide
```

## Memory Systems Tested

| System | Version | Architecture | Option A | Option B |
|---|---|---|---|---|
| Mem0 | mem0ai 1.0.11 | Flat embedding, cosine similarity | Pre-extracted facts | `infer=True` (native extraction) |
| Letta (MemGPT) | letta-client 1.10.2 | Tiered agent-driven, archival + stateful blocks | Pre-extracted facts (archival path) | Archival chunks + stateful-agent loop (§4.3.1) |
| Supermemory | supermemory 3.32.0 | Atomic memories, hybrid retrieval | Pre-extracted facts | `/v3/documents` with chunks |
| Zep | zep-cloud 3.20.0 | Knowledge graph, entity-relationship | Pre-extracted facts | `graph.add` with 500-word chunks |
| Base Layer | MiniLM-L6-v2 + ChromaDB | Sentence embeddings, cosine similarity | Pre-extracted facts | N/A (Base Layer is the spec layer, not a memory provider) |

## Subjects

| Subject | Culture | Era | C5 Baseline | Source |
|---|---|---|---:|---|
| Sunity Devee | Indian | 1864-1932 | 1.03 | *Autobiography* |
| Georg Ebers | German | 1837-1898 | 1.04 | *Story of My Life* |
| Philip Gilbert Hamerton | British | 1834-1894 | 1.25 | *Autobiography* |
| Fukuzawa Yukichi | Japanese | 1835-1901 | 1.80 | *Autobiography* |
| Mary Seacole | Caribbean/British | 1805-1881 | 1.85 | *Wonderful Adventures* |
| Bernal Diaz del Castillo | Spanish/Latin American | 1492-1584 | 1.85 | *True History* |
| Elizabeth Keckley | Black American | 1818-1907 | 1.91 | *Behind the Scenes* |
| Yung Wing | Chinese | 1828-1912 | 1.96 | *My Life in China* |
| Babur | Central Asian/Muslim | 1483-1530 | 1.98 | *Baburnama* |
| — low-baseline cutoff (n=9 above) — | | | | |
| Benvenuto Cellini | Italian | 1500-1571 | 2.56 | *Vita* |
| Zitkala-Sa | Native American | 1876-1938 | 2.60 | *American Indian Stories* |
| Jean-Jacques Rousseau | French | 1712-1778 | 2.65 | *Confessions* |
| Augustine of Hippo | North African/Roman | 354-430 | 2.79 | *Confessions* |
| Olaudah Equiano | West African/British | 1745-1797 | 2.93 | *Interesting Narrative* |

All source texts are public domain (Project Gutenberg, Internet Archive). Baselines from [DATA_REFERENCE.md §1](docs/DATA_REFERENCE.md).

## Reproducibility

- All API calls use temperature=0
- Corpus files checksummed (SHA-256)
- All responses logged with full system prompts, retrieved facts, token counts
- Manifest files record SDK versions, timestamps, model versions
- Question batteries include exact held-out passages from source text
- Any result can be reproduced by running the corresponding script
- Analysis plan pre-committed in [docs/ANALYSIS_PLAN_LOCK.md](docs/ANALYSIS_PLAN_LOCK.md) before final runs

## License

License pending (see top-level LICENSE file when added). Intended license: Apache 2.0.

## Citation

```
@article{gulaya2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization},
  author={Gulaya, Aarik},
  year={2026},
  url={https://github.com/agulaya24/memory-study-repo}
}
```
