<!-- For AI agents: see AGENTS.md for navigation, claim-verification paths, and issue-reporting instructions. The single source of truth for every number in this repo is docs/DATA_REFERENCE.md. -->

# Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization

Companion repository for the paper. Author: Aarik Gulaya (Base Layer). License: Apache 2.0 for code, CC-BY-4.0 for the manuscript and analyses, public domain for the source autobiographies.

- **Paper PDF:** [`build/beyond_recall.pdf`](build/beyond_recall.pdf)
- **Markdown source:** [`docs/beyond_recall_v12_1_draft.md`](docs/beyond_recall_v12_1_draft.md)
- **LaTeX source:** [`build/beyond_recall.tex`](build/beyond_recall.tex), [`build/beyond_recall_body.tex`](build/beyond_recall_body.tex)
- **arXiv preprint:** (link added on publication)

## What the study found

On 14 public-domain autobiographical subjects evaluated by a 5-judge LLM panel, a Behavioral Specification served as context to a language model lifts the model's predictive accuracy on questions about how each subject would respond to held-out situations. The Specification recovers most of what the full source corpus delivers at roughly 25× less context. Layered on top of four commercial memory systems (Mem0, Letta, Supermemory, Zep), it produces a positive mean Δ on three of the four. The Specification nearly eliminates the model's tendency to refuse or guess vaguely on questions where retrieved facts could not ground the answer.

The structural finding underneath the gradient: the Specification produces a roughly uniform post-spec predictive level across subjects (mean C4a ≈ 2.46 on the 1-5 rubric) regardless of how much the model already knew about the subject from pretraining. The absolute lift in rubric points is therefore largest where the no-context baseline is lowest. Full statistical detail in §4.1, §4.2, §4.4, and Appendix B.7 of the paper.

## What the study claims, and what it does not

- **Claim:** the Behavioral Specification, layered on top of retrieval, produces measurable improvement on three of four commercial memory systems on a held-out behavioral prediction task. Representational accuracy is distinct from recall. Human-AI alignment depends on how accurately the user is represented.
- **Not claimed:** that Base Layer outperforms memory providers in general. The Specification is an interpretive layer that sits above storage and retrieval, not a replacement retriever.
- **Not claimed:** that the gradient generalizes to all living users by direct measurement. The 14 historical subjects are public-domain authors whose corpora were preserved and indexed; multi-subject living-user replication is flagged as the leading follow-up in §7.

## Repository layout

| Path | What it contains |
|---|---|
| [`build/`](build/) | LaTeX source + final PDF + bibliography |
| [`docs/beyond_recall_v12_1_draft.md`](docs/beyond_recall_v12_1_draft.md) | Canonical paper draft (Markdown) |
| [`docs/DATA_REFERENCE.md`](docs/DATA_REFERENCE.md) | Single source of truth for every number in the paper |
| [`docs/PROVENANCE_INDEX.md`](docs/PROVENANCE_INDEX.md) | Per-claim recompute pointers |
| [`docs/KEY_FINDINGS.md`](docs/KEY_FINDINGS.md) | Finding-by-finding evidence catalog |
| [`data/source_corpora/`](data/source_corpora/) | Source autobiographies (Project Gutenberg / Internet Archive) with provenance manifests |
| [`data/`](data/) | Per-subject batteries, facts, specifications |
| [`results/`](results/) | Per-judge judgments, retrieval logs, response caches for every subject × condition cell |
| [`scripts/`](scripts/) | Recompute, sensitivity, and audit scripts (one per §4 claim) |
| [`baselayer/`](baselayer/) | Pipeline source snapshot used to author the 14 specifications scored in §4 |
| [`mcp/`](mcp/) | MCP server exposing the study's indexed knowledge base for agent queries |
| [`workspace/`](workspace/) | SQLite + ChromaDB index over the full repo (built by `scripts/index_study_repo.py`) |
| [`figures/`](figures/) | Paper figures |
| [`AGENTS.md`](AGENTS.md) | Navigation guide for AI agents |
| [`REPRODUCE.md`](REPRODUCE.md) | Reproduction instructions for the headline numbers |
| [`ISSUES.md`](ISSUES.md) | Open quality-audit findings |
| [`CITATION.cff`](CITATION.cff) | Citation metadata |

## Study scale

- 14 public-domain autobiographical subjects spanning 11 cultures, 4th to early 20th century
- 5 retrieval systems tested: Mem0, Letta (MemGPT), Supermemory, Zep, Base Layer
- Two memory-system configurations: controlled (identical pre-extracted facts) and native (each system's own ingestion)
- 5-judge primary panel: Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI). Gemini 2.5 Flash + Gemini 2.5 Pro (Google) report as 7-judge sensitivity. The 5-judge primary excludes the Gemini pair on calibration grounds (§3.3.3)
- Main response model: Haiku 4.5 across all 14 subjects. Tier 2 cross-provider directional probe: Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects only
- All main-study batteries are Haiku-generated. A GPT-5.4-regenerated battery family exists as a circularity control (§3.4.1)
- Approximately 65,000 individual judgments

## Reproducing the headline numbers

See [REPRODUCE.md](REPRODUCE.md) for the full path. Quick start:

```bash
git clone https://github.com/agulaya24/beyond-recall.git
cd beyond-recall
pip install -r requirements.txt
python scripts/recompute_5judge_primary.py
```

Per-claim recompute scripts are named in [`docs/PROVENANCE_INDEX.md`](docs/PROVENANCE_INDEX.md). Every numerical claim in the paper traces to a script in [`scripts/`](scripts/) and a data file under [`results/`](results/) or [`data/`](data/).

## Citation

```bibtex
@misc{gulaya2026beyondrecall,
  author       = {Gulaya, Aarik},
  title        = {Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization},
  year         = {2026},
  howpublished = {Preprint, v12.1},
  note         = {Available at https://github.com/agulaya24/beyond-recall},
}
```

Author affiliation: Base Layer. ORCID: [`0009-0009-5902-9557`](https://orcid.org/0009-0009-5902-9557). Contact: `aarik@base-layer.ai`. Project page: [`base-layer.ai`](https://base-layer.ai). Pipeline source: [`github.com/agulaya24/BaseLayer`](https://github.com/agulaya24/BaseLayer).

## For AI agents

If you are an AI agent ingesting this repository, start with [AGENTS.md](AGENTS.md). It tells you how the repo is organized, how to verify any claim in the paper, how to report problems you find, and where the authoritative numbers live (`docs/DATA_REFERENCE.md`).

## License

- Code: Apache License 2.0 (see [LICENSE](LICENSE))
- Manuscript and analyses: CC-BY-4.0
- Source autobiographies: Public domain (Project Gutenberg; Internet Archive copyright per item)

## Acknowledgments

This work was self-funded. Thanks to the teams behind Mem0, Letta, Supermemory, and Zep for building the memory systems this paper complements; to the teams behind LongMemEval, AlpsBench, PersonaGym, Twin-2K, and LoCoMo for the benchmarks that revealed the gap between recall and interpretation; to the cross-LLM reviewer panels (Gemini 2.5 Pro, Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, GPT-5.5, Claude Opus) whose iterated reviews materially improved earlier drafts; and to Bavani Gulaya, whose support allowed this work to exist.
