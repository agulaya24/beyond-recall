<!-- IF YOU ARE AN AI AGENT: Start with agents/study-guide.md — it tells you how to navigate this repo, verify every claim, and report issues you find. -->

# Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization

> **If you're an AI agent reading this repository**, see [agents/study-guide.md](agents/study-guide.md) for structured navigation, claim verification paths, and issue reporting instructions.

> **TLDR:** Enter into your LLM: *"What in the world is this? (github.com/agulaya24/baselayer) and how can it help me"*

What if the bottleneck in AI personalization isn't retrieval — it's representation?

This study tests whether a behavioral specification (a structured model of how someone thinks, decides, and communicates) improves held-out behavioral prediction when added to state-of-the-art (SOTA) memory systems. Across 14 subjects from 11 cultures, 6 response models, and 7 judges: it does. Adding a spec to any of four funded SOTA memory systems makes them better. The effect is largest for subjects the model has never seen — which is every real user.

## Key Findings

### Hamerton Study (Unknown Subject — Baseline 1.41)

| Condition | 4-Judge Avg | What it proves |
|---|---|---|
| **C4a (all facts + spec)** | **3.23** | Spec helps even with complete information |
| C3 (spec + retrieved facts) | 2.96-3.13 | **Spec + facts beats facts alone (p=0.012)** |
| C4 (all 462 facts, no spec) | 2.69 | All facts without framework |
| C1 (memory system facts only) | 1.64-2.67 | Memory systems alone |
| C9 (raw corpus, 25K words) | 2.31 | **Raw text loses to spec + 10 facts** |
| C5 (baseline) | 1.41 | Model doesn't know the subject |

### Franklin Study (Known Subject — Baseline 4.10)

| Condition | 4-Judge Avg | What it proves |
|---|---|---|
| **C5 (baseline, no context)** | **4.10** | Model already knows Franklin |
| C3 (spec + facts) | 3.83 | Context hurts when model already knows |
| C7 (named baseline) | 3.89 | Model identifies Franklin without being told |

### The Meta-Finding

The spec's value is inversely proportional to the model's prior knowledge.

- **Unknown subjects (every real user):** Spec transforms prediction (+128%)
- **Known subjects (famous figures):** Spec is unnecessary (-4%)
- **Raw text in context:** Loses to spec + 10 facts despite having 8x more information

## Study Design

- **2 subjects:** Philip Gilbert Hamerton (unknown) + Benjamin Franklin (known)
- **4 memory systems:** Mem0, Letta (MemGPT), Supermemory, Zep
- **15 conditions:** C1-C9, C4a, C7 (see methodology)
- **80 questions per subject:** 40 behavioral prediction with held-out ground truth
- **7 judges, 3 providers:** Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google)
- **Inter-rater reliability:** Pairwise Spearman rho 0.89-0.98

## Repository Structure

```
data/
  hamerton/                       # Primary subject (unknown to model)
    battery.json                  # 80 questions with held-out passages
    facts.json                    # 462 extracted facts
    shared_facts.json             # Facts shared across conditions
    questions_80.json             # Question battery
    spec/                         # Behavioral specification layers
  franklin/                       # Known-figure replication
    battery.json                  # Franklin question battery
    facts.json                    # 1,133 extracted facts
    franklin_shared_facts.json
    questions_80_franklin.json
  franklin_obscure/               # Cross-corpus test (letters)
    battery.json
    facts.json
  global_subjects/                # 13 subjects across 11 cultures
    augustine/ babur/ bernal_diaz/ cellini/ ebers/ equiano/
    fukuzawa/ keckley/ rousseau/ seacole/ sunity_devee/
    yung_wing/ zitkala_sa/
    # Each contains: battery.json, facts.json, spec.md,
    # spec_production.md, judgments.json, results.json,
    # anchors_v4.md, core_v4.md, predictions_v4.md, brief_v5.md
results/
  hamerton/                       # Haiku full-stack responses + judge scores
  franklin/                       # Franklin responses + judge scores
  franklin_obscure/               # Obscure letters responses
  multimodel/                     # Sonnet, GPT-5.4, Gemini Flash responses
  judge_calibration/              # Calibration tests across 5+ judges
scripts/
  run_full_study.py               # Main study runner
  run_franklin_raw.py             # Franklin runner (raw HTTP)
  run_franklin_judge.py           # Franklin 5-judge pipeline
  run_judge_batch.py              # Anthropic batch judge
  run_judge_calibration.py        # Judge calibration framework
  run_judge_evaluation.py         # Judge evaluation pipeline
  run_multimodel_responses.py     # Multi-model response generation
  run_global_subjects.py          # Global subjects pipeline
  run_full_spec_rerun.py          # Full-stack spec rerun
  extract_shared_facts.py         # Fact extraction (Haiku)
  review_paper.py                 # Cross-LLM paper review
  gemini_review_script.py         # Gemini API review script
docs/
  beyond_recall_arxiv_draft.md    # Full research paper (ArXiv preprint)
  beyond_recall_arxiv_draft.docx  # Word export for sharing
  blog_post_v2.md                 # Blog post (current draft)
  METHODOLOGY.md                  # Full methodology and conditions
  PROVIDER_ISSUES.md              # Issues encountered per memory system
  PROVENANCE_INDEX.md             # Every number traced to source file
  PAPER_CORRECTIONS.md            # 13 corrections from provenance audit
  REFERENCE_TABLE.md              # 19 references with verification status
  reviews/                        # All LLM paper reviews (Gemini, Mistral, etc.)
  versions/                       # Version snapshots of paper and blog
charts/
  unknown_vs_known.png            # Headline chart
  hamerton_full_hierarchy.png
  hamerton_vs_franklin.png
  bimodal_to_gradient.png
  compression_story.png
  judge_agreement.png
  franklin_judge_agreement.png
  pipeline_diagram.md             # Pipeline diagram specification
agents/
  study-guide.md                  # Agent navigation guide
```

## Reproducibility

- All API calls use temperature=0
- Corpus files checksummed (SHA-256)
- All responses logged with full system prompts, retrieved facts, token counts
- Manifest files record SDK versions, timestamps, model versions
- Question batteries include exact held-out passages from source text

## Corpora

- **Hamerton:** Philip Gilbert Hamerton, *An Autobiography* (1834-1858), Project Gutenberg #8536
- **Franklin:** Benjamin Franklin, *Autobiography*, Project Gutenberg #20203

## Memory Systems Tested

| System | Version | Architecture |
|---|---|---|
| Mem0 | mem0ai 1.0.11 | Flat embedding, cosine similarity |
| Letta (MemGPT) | letta-client 1.10.2 | Tiered agent-driven retrieval |
| Supermemory | supermemory 3.32.0 | Atomic memories, hybrid retrieval |
| Zep | zep-cloud 3.20.0 | Knowledge graph, entity-relationship |

## License

Apache 2.0

## Citation

```
@article{baselayer2026beyondrecall,
  title={Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization},
  author={Base Layer},
  year={2026},
  url={https://base-layer.ai}
}
```

## Links

- [Blog post](https://base-layer.ai/research/memory-study)
- [Interactive data explorer](https://base-layer.ai/research/memory-study/explorer)
- [Base Layer](https://base-layer.ai)
