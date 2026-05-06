<!-- IF YOU ARE AN AI AGENT: Start with agents/study-guide.md — it tells you how to navigate this repo, verify every claim, and report issues you find. The single source of truth for every number is docs/DATA_REFERENCE.md. -->

# Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization

> **Canonical paper draft:** [`docs/beyond_recall_v11_draft.md`](docs/beyond_recall_v11_draft.md) (v11, release-frozen 2026-04-28). Citable canonical effective 2026-04-28. Freeze record: see the "V11 FREEZE — 2026-04-28" section of [`docs/reviews/v11_running_changes_log_20260427.md`](docs/reviews/v11_running_changes_log_20260427.md).
>
> **Preserved historical baseline:** [`docs/beyond_recall_v10_1_draft.md`](docs/beyond_recall_v10_1_draft.md) (v10.1, release-frozen 2026-04-25). v10.1 was the citable canonical until v11's freeze on 2026-04-28; it is preserved as a reference baseline and is NOT the editing target. Earlier drafts (v8 / v9 / v10-partial) are preserved at [`docs/versions/_pre_v11_drafts/`](docs/versions/_pre_v11_drafts/); v6 / v7 / arxiv drafts are at [`docs/versions/`](docs/versions/).
>
> **Read [ISSUES.md](ISSUES.md) first** if you are working in this repo. It tracks open quality-audit findings. Release-freeze pass closures: `docs/reviews/v10_release_freeze_pass_report.md` (2026-04-24, v10), v10.1 pass 3 record (2026-04-25, see ISSUES.md), and the v11 freeze record in `docs/reviews/v11_running_changes_log_20260427.md` (2026-04-28).
>
> **If you're an AI agent reading this repository**, see [agents/study-guide.md](agents/study-guide.md) for structured navigation, claim verification paths, and issue reporting instructions. The single source of truth for every number in this repo is [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md). DATA_REFERENCE is anchored to the v10.1 5-judge primary panel; v11 carries those numbers forward unchanged and adds new content registered in the 2026-04-28 v11 data-locking pass (per-question variance, two statistical signatures, half-anchor metric, predicate ablation, held-out leakage rare, Hamerton spec-length confound). The v11 confidence catalog at [docs/research/v11_confidence_catalog_20260428.md](docs/research/v11_confidence_catalog_20260428.md) is the per-claim source of truth for v11.
>
> **Reproduce the v11 headline numbers:** see [REPRODUCE.md](REPRODUCE.md) and `requirements.txt`. v11 carries the v10.1 §4.1 headline numbers forward unchanged, so the v10.1 reproduction path remains valid for v11.

## What the study found

On 14 public-domain autobiographical subjects evaluated by a 5-judge LLM panel, adding a Behavioral Specification on top of four commercial memory systems (Mem0, Letta, Zep, Supermemory) produces a positive mean Δ on three of the four (full per-system numbers in [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md) and §4.4 of the v11 paper).

The structural finding underneath the gradient: the Behavioral Specification produces a roughly uniform post-spec operating level (mean C4a = 2.46 on the 1-5 rubric) regardless of how much the model already knew about the subject from pretraining. The visible per-subject lift varies because the no-context baseline varies (1.02 to 2.77 across the 14 subjects); subjects far below that operating level see large lifts, subjects already at or above see little or none. The technical sensitivity that established this (level regression of C4a on C5 yields slope = +0.04, R² = 0.008) is in §4.1 of the paper.

Plain-language version: the spec produces the same approximate quality of answer for everyone; the gain in raw points is largest where the user was furthest below that quality.

## What the study claims, and what it does not

- **Claim from measurement:** the Behavioral Specification, layered on top of retrieval-based memory, produces positive mean Δ on 3 of 4 commercial memory systems we tested, with a uniform post-spec operating level near 2.46 on the 1-5 rubric across 14 historical subjects.
- **Claim by structural extrapolation, not measurement:** living users whose private reasoning was never indexed by any AI training corpus are the closest available proxy for the historical low-baseline subjects (§5.3 of the v11 paper). For that population the specification supplies the operating-level lift the historical low-baseline subjects show. This is a structural argument, not an empirical replication; multi-subject living-user replication is the leading follow-up flagged in §7.
- **Not claimed:** that Base Layer outperforms memory providers in general. The Behavioral Specification is an orthogonal layer that adds interpretive structure on top of retrieval. It is not a better retriever, and it is not benchmarked as one (§5.1 Anti-Pattern in the paper).
- **Not claimed:** that the gradient generalizes to all living users by direct measurement. The 14 historical subjects are public-domain authors whose corpora were preserved and indexed; living users sit structurally lower on the baseline scale, but a multi-subject living-user replication has not been run.

## What this study is, and is not

- It is a test of how a Behavioral Specification layer composes with existing memory-system retrieval — net-positive aggregate on three of four commercial systems tested, with structured per-question patterns rather than uniform additivity.
- It is not a benchmark of memory systems against each other.
- It is not a claim that Base Layer outperforms memory providers in general; that is not what was tested.
- The Behavioral Specification is an interpretive layer that sits above storage and retrieval, not a replacement retriever.

## Study Scale

- **14 public-domain autobiographical subjects** from 11 cultures spanning 2,500 years (Augustine of Hippo to Zitkala-Sa)
- **5 retrieval systems tested:** Mem0, Letta (MemGPT), Supermemory, Zep, Base Layer
- **Two memory-system configurations:** controlled (identical pre-extracted facts) and native (each system's own ingestion)
- **5-judge primary panel:** Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI). Gemini 2.5 Flash and Gemini 2.5 Pro (Google) report as 7-judge sensitivity. Gemini Pro has limited coverage (Hamerton + Tier 2 only); the 5-judge primary excludes the Gemini pair per v11 §3.6 / v10.1 §3.7.2 (Gemini Pro fails verbatim-match calibration; both Gemini judges inflate scores by ~+1 point).
- **Main-study response model:** Haiku 4.5 across all 14 subjects. **Tier 2 cross-provider directional probe:** 2 additional response models (Sonnet 4.6, Gemini 2.5 Pro) on 3 subjects only. Opus and GPT-5.4 in Tier 2 are judges, not response models.
- **All 14 main-study batteries are Haiku-generated.** A GPT-5.4-regenerated battery family exists as a circularity control (§3.4.1 + Tier 2), not as the main-study batteries.
- **~65,000 individual judgments**

## Key Findings

See [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md) for the authoritative numbers and CIs. The summaries below are paraphrases; the source of truth is the data reference.

### 1. The gradient: the less the model knows, the more the spec helps

On the 9 low-baseline subjects (C5 ≤ 2.0, the population of interest), the spec improves prediction on **9 of 9**, mean Δ_C4a = **+0.89 points**. Across all 14 subjects, 12 of 14 show positive lift from facts+spec; the two negatives (Zitkala-Sa, Equiano) sit in the mid-baseline band, consistent with the gradient mechanism. Linear regression of Δ_C4a on C5 baseline (5-judge primary panel, v11 §4.1, carried forward unchanged from v10.1 §4.1): slope **−0.96 [95% CI −1.24, −0.67], R² = 0.82, p < 0.001**. Battery-composition controls leave the slope at −0.88 (multiple regression on LITERAL_RECALL fraction) and −0.89 (drop-Hamerton subset; all 14 main-study batteries are Haiku-generated, so the subset regression isolates Hamerton's legacy battery, not a generator family). The level regression C4a ~ C5 produces a near-zero slope of +0.04 with mean C4a = 2.46, so the headline change-score slope is dominated by the coupling identity slope_Δ = slope_level − 1; the practical claim ("the spec is the tool for the unknown") survives, with the framing "roughly constant post-spec operating level, lift larger where floor lower" rather than treatment-effect-heterogeneity.

### 2. The spec improves every commercial memory system — on the users the model doesn't already know

In the controlled configuration on the 9 low-baseline subjects (5-judge primary, v11 §4.4), adding the behavioral specification to retrieved facts produces **positive mean delta on three of four commercial systems plus the Base Layer substrate**: Mem0 +0.10, Letta (archival) +0.17, Zep +0.17, Supermemory −0.01, plus Base Layer substrate +0.08. The pattern is nuanced: Zep and Mem0 native are strongest; Mem0 controlled is small but positive; Letta archival is positive in the controlled configuration and near-null in the native configuration; Supermemory's aggregate is a mixture rather than a uniform null. Aggregated across all 14 subjects, Supermemory's spec-delta is near-zero (−0.05 controlled, −0.01 native paid-tier rerun). The per-question distribution is bimodal (57 questions improve at mean +1.55, 53 worsen at mean −1.38; 110 of 546 carry meaningful magnitude on 5-judge primary, 20.1%); the two sides roughly cancel at the mean rather than the spec failing uniformly. See DATA_REFERENCE §3–§5.

### 3. Information is not what's missing — structure is

On Hamerton (5-judge primary, v11 §4.2), a 7K-token spec (C2a, score 2.63) outperforms 34K tokens of raw corpus (C8, score 2.27) and is exceeded only by spec-augmented raw corpus (C9, 3.09). The raw corpus contains every fact the spec is derived from. The model cannot extract interpretive structure from unstructured text alone. See DATA_REFERENCE §8.

### 4. Letta's stateful-agent path: architectural convergence on the specification target (n=3, exploratory)

When Letta's stateful-agent path is invoked properly (turn-by-turn ingestion with self-editing memory blocks, per Packer et al.), it produces a memory block that predicts as well as or better than Base Layer's full-stack spec at matched response model on all three subjects tested: Hamerton +0.14, Ebers +1.05, Babur +0.54 (5-judge primary). Two independently-designed systems converging on the same interpretive-representation target. Letta's block grows roughly linearly with corpus size and hits an API-level ceiling near 333K characters on Babur; Base Layer keeps the specification at 34K-40K characters across the range. v11 carries this forward as an exploratory case study at n=3 (paper §4.5). See `docs/research/letta_stateful_matched_rerun.md` and the rerun pipeline at `docs/research/_letta_rerun/`.

### 5. Content specificity matters — wrong specs score near or below baseline

Wrong-spec v1 (fixed derangement designed for cultural/temporal distance, pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING): 1.86 (−0.25 vs baseline on the 5-judge primary). Wrong-spec v2 (random derangement, seed=42): 2.13 (+0.15 vs baseline, but below correct-spec C2a). Neither reaches correct-spec scores. The adversarial fixed derangement is *below* baseline: structured prompting with the wrong content performs worse than no context at all. Wrong-spec denominator: 587 = 507 v2 (13 globals × 39q) + 80 v1 (Hamerton across all 5 battery tiers). See v11 paper §1.3, §4.3 (wrong-spec elevated in v11 §4.6.4); DATA_REFERENCE §6.

### 6. Statistical robustness (5-judge primary panel)

- Wilcoxon signed-rank, C5 vs C2a (N=14): W=10, p=0.005
- Wilcoxon signed-rank, C5 vs C4a (N=14): W=11, p=0.007
- Regression slope on gradient (Δ_C4a on C5): **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001
- Battery-composition partial slope (controls for LITERAL_RECALL fraction): −0.88 [95% CI −1.13, −0.63]
- Drop-Hamerton subset slope (all 14 main-study batteries are Haiku-generated; this is the drop-Hamerton subset, not a generator-family subset): −0.89 [95% CI −1.18, −0.61]
- Coupling-free reframing: level regression C4a ~ C5 slope = +0.04 [95% CI −0.25, +0.33], R² = 0.008, mean C4a = 2.46
- Krippendorff α = 0.659 across the 5-judge primary panel (ordinal, substantial agreement); 0.535 across the full 7-judge panel including Gemini Flash/Pro
- Pairwise Spearman ρ across the 5-judge primary panel: 0.86 - 0.93 (10 pairs, high rank agreement)

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
| C2c v1 | Fixed derangement wrong-spec (cultural/temporal distance; pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING) |
| C2c v2 | Random-derangement wrong-spec (seed=42, no subject receives its own) |

Memory-system conditions run in two configurations:
- **Option A (controlled):** identical pre-extracted fact set given to every system
- **Option B (native):** raw corpus fed to each system's own ingestion pipeline

## Repository Structure

```
data/
  hamerton/                       # Primary subject (low baseline, 1.26 on 5-judge primary)
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
  DATA_REFERENCE.md               # SINGLE SOURCE OF TRUTH for all numbers (5-judge primary)
  beyond_recall_v11_draft.md      # CANONICAL paper draft, v11 (release-frozen 2026-04-28)
  beyond_recall_v10_1_draft.md    # Preserved historical baseline, v10.1 (do not edit)
  versions/                       # Earlier drafts (v6, v7, arxiv) preserved
  versions/_pre_v11_drafts/       # v8, v9, v10-partial preserved (archived 2026-04-28)
  METHODOLOGY.md                  # Full methodology and conditions
  PROVENANCE_INDEX.md             # Every number traced to source file
  PAPER_CORRECTIONS.md            # Corrections changelog
  ANALYSIS_PLAN_LOCK.md           # Pre-committed analysis plan
  KEY_FINDINGS.md                 # Catalog of major and minor findings (v11-aligned, includes M15-M21 v11 additions)
  PROVIDER_EXPERIENCE_LEDGER.md   # Working with each memory system API
  PROVIDER_ISSUES.md              # Technical issues per system
  blog_post_v2.md                 # Blog post (launch artifact)
  research/                       # Per-analysis reports (paired analyses, hedging, spec activation, Letta stateful)
  reviews/                        # Review-round artifacts

charts/                           # Visualizations
figures/                          # Paper figures (fig_4_1, fig_4_2, fig_4_2_1)
agents/
  study-guide.md                  # Agent navigation guide
```

## Memory Systems Tested

| System | Version | Architecture | Option A | Option B |
|---|---|---|---|---|
| Mem0 | mem0ai 1.0.11 | Flat embedding, cosine similarity | Pre-extracted facts | `infer=True` (native extraction) |
| Letta (MemGPT) | letta-client 1.10.2 | Tiered agent-driven, archival + stateful blocks | Pre-extracted facts (archival path) | Archival chunks + stateful-agent loop (§4.5) |
| Supermemory | supermemory 3.32.0 | Atomic memories, hybrid retrieval | Pre-extracted facts | `/v3/documents` with chunks |
| Zep | zep-cloud 3.20.0 | Knowledge graph, entity-relationship | Pre-extracted facts | `graph.add` with 500-word chunks |
| Base Layer | MiniLM-L6-v2 + ChromaDB | Sentence embeddings, cosine similarity | Pre-extracted facts | N/A (Base Layer is the spec layer, not a memory provider) |

## Subjects

C5 baselines below are 5-judge primary (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4), per v11 §4.1 (carried forward unchanged from v10.1 §4.1).

| Subject | Culture | Era | C5 Baseline | Source |
|---|---|---|---:|---|
| Georg Ebers | German | 1837-1898 | 1.02 | *Story of My Life* |
| Sunity Devee | Indian | 1864-1932 | 1.03 | *Autobiography* |
| Philip Gilbert Hamerton | British | 1834-1894 | 1.26 | *Autobiography* |
| Fukuzawa Yukichi | Japanese | 1835-1901 | 1.67 | *Autobiography* |
| Bernal Diaz del Castillo | Spanish/Latin American | 1492-1584 | 1.70 | *True History* |
| Babur | Central Asian/Muslim | 1483-1530 | 1.76 | *Baburnama* |
| Mary Seacole | Caribbean/British | 1805-1881 | 1.77 | *Wonderful Adventures* |
| Elizabeth Keckley | Black American | 1818-1907 | 1.84 | *Behind the Scenes* |
| Yung Wing | Chinese | 1828-1912 | 1.88 | *My Life in China* |
| — low-baseline cutoff (n=9 above; C5 ≤ 2.0) — | | | | |
| Zitkala-Sa | Native American | 1876-1938 | 2.34 | *American Indian Stories* |
| Benvenuto Cellini | Italian | 1500-1571 | 2.38 | *Vita* |
| Jean-Jacques Rousseau | French | 1712-1778 | 2.44 | *Confessions* |
| Augustine of Hippo | North African/Roman | 354-430 | 2.58 | *Confessions* |
| Olaudah Equiano | West African/British | 1745-1797 | 2.77 | *Interesting Narrative* |

All source texts are public domain (Project Gutenberg, Internet Archive). Baselines from [DATA_REFERENCE.md §1](docs/DATA_REFERENCE.md) and v11 §4.1 (carried forward unchanged from v10.1 §4.1, line 720 in the v10.1 baseline).

## Reproducibility

- All API calls use temperature=0
- Corpus files checksummed (SHA-256)
- All responses logged with full system prompts, retrieved facts, token counts
- Manifest files record SDK versions, timestamps, model versions
- Question batteries include exact held-out passages from source text
- Any result can be reproduced by running the corresponding script
- Analysis plan pre-committed in [docs/ANALYSIS_PLAN_LOCK.md](docs/ANALYSIS_PLAN_LOCK.md) before final runs

## License

Apache 2.0. See [LICENSE](LICENSE) in the repository root.

## Citation

```
@article{gulaya2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization},
  author={Gulaya, Aarik},
  year={2026},
  url={https://github.com/agulaya24/memory-study-repo}
}
```
