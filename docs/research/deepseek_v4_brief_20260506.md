# DeepSeek V4 Brief

**Author:** Research agent for Aarik Gulaya (Beyond Recall paper distribution prep)
**Date:** 2026-05-06
**Purpose:** (1) decide whether to include DeepSeek V4 in any future replication of the Beyond Recall study, (2) decide how to position outreach to the DeepSeek team.
**Scope:** research only — no paper edits.

## Executive summary

DeepSeek V4 was previewed on 2026-04-24 as two open-weight MoE models (V4-Pro at 1.6T total / 49B active and V4-Flash at 284B / 13B active), both with 1M-token context, MIT license, and aggressive pricing. V4 closes most of the gap to frontier closed models on reasoning and code (SWE-bench Verified 80.6, LiveCodeBench 93.5, GPQA Diamond 90.1) while trailing Gemini 3.1 Pro and Opus 4.6/4.7 by roughly 2-4 points on broad knowledge benchmarks. The most consequential intersection with Beyond Recall is not the model itself but Liang Wenfeng's December 2025 paper "Conditional Memory via Scalable Lookup" introducing the **Engram** module — a sparse, externalized memory architecture that DeepSeek frames as a permanent axis of LLM design alongside MoE. This makes V4 a natural inclusion as a fifth response model in a Tier 2 replication and makes DeepSeek a high-relevance outreach target with a memory-axis hook the paper can speak to directly.

## 1. Release info

- **Date:** Preview released 2026-04-24. Two models live on the official DeepSeek API the same day. Release notes: `https://api-docs.deepseek.com/news/news260424`.
- **Announcer:** DeepSeek-AI organizationally. Liang Wenfeng (founder/CEO) is signed first author on the architectural antecedent paper, posted to arXiv 2025-12-31.
- **Press:** MIT Tech Review (`https://www.technologyreview.com/2026/04/24/1136422/why-deepseeks-v4-matters/`), TechCrunch (`https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/`), Bloomberg (`https://www.bloomberg.com/news/articles/2026-04-24/deepseek-unveils-newest-flagship-a-year-after-ai-breakthrough`).
- **Technical antecedent paper:** "Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models" — arXiv 2601.07372, Liang Wenfeng et al. with Peking University. Code at `https://github.com/deepseek-ai/Engram`.

## 2. Model variants

Both ship as **open weights under MIT license** and are simultaneously available via DeepSeek's first-party API.

| Variant | Total | Active | Precision | Context |
|---|---|---|---|---|
| V4-Pro | 1.6T | 49B | FP4 + FP8 | 1M |
| V4-Flash | 284B | 13B | FP4 + FP8 | 1M |

Both ship with `-Base` (unquantized, pre-SFT) checkpoints. Three reasoning modes per model: Non-Think, Think-High, Think-Max. Pro-Max is the highest-reasoning preset.

Architecture (per model card, `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro`): hybrid Compressed Sparse Attention + Heavily Compressed Attention (27% of V3.2 single-token FLOPs, 10% of the KV cache); Manifold-Constrained Hyper-Connections (mHC); Muon optimizer; two-stage post-training with on-policy distillation. 32T+ pre-training tokens.

Legacy `deepseek-chat` / `deepseek-reasoner` aliases deprecate **2026-07-24**, mapping to V4-Flash non-thinking / thinking modes in the interim.

## 3. Capabilities and benchmarks

V4-Pro-Max headline numbers from the official model card and corroborated by third-party reviews:

V4-Pro-Max headline numbers (model card + third-party reviews `https://www.morphllm.com/deepseek-v4`, `https://macaron.im/blog/deepseek-v4-benchmarks`):

| Benchmark | V4-Pro-Max | Comparison |
|---|---|---|
| MMLU-Pro | 87.5 | Opus 4.6 Max 89.1; Gemini 3.1 Pro / GPT-5.4 ~89 |
| GPQA Diamond | 90.1 | Gemini 3.1 Pro 94.3 |
| SimpleQA-Verified | 57.9 | Gemini 3.1 Pro High 75.6 |
| LiveCodeBench Pass@1 | **93.5** | best of compared |
| Codeforces | **3206** | best of compared |
| SWE-bench Verified | 80.6 | Opus 4.6: 80.8 |
| Terminal Bench 2.0 / BrowseComp / Toolathlon | 67.9 / 83.4 / 51.8 | — |
| MRCR / CorpusQA (1M) | 83.5 / 62.0 | — |
| IMOAnswerBench | 89.8 | — |

DeepSeek's framing: "almost closed the gap" with a claimed 3-6 month lag (`https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/`). V4 supersedes V3.2; no standalone R2 shipped — reasoning folded into V4's Think modes after R2 delays through 2025 (`https://restofworld.org/2025/deepseek-china-r2-ai-model-us-rivalry/`).

## 4. Availability

- **Open weights** under MIT: `https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro` and `-Flash`. Quantizations for llama.cpp, Ollama, LM Studio. Inference via Transformers, vLLM, SGLang.
- **First-party API** (`https://api-docs.deepseek.com/quick_start/pricing`, post 2026-04-26 cache-hit cut, V4-Pro at 75% discount through 2026-05-31): V4-Flash ~$0.14/M input miss, ~$0.028/M hit, ~$0.28/M output. V4-Pro ~$0.145/M hit (discounted), ~$3.48/M output. Prefix caching at ≥1024 shared tokens.
- **Third-party hosting:** Together AI, DeepInfra, Novita, HuggingFace Inference.
- **Fine-tuning:** open weights enable third-party FT; no first-party FT service advertised.
- **Context:** 1M on both variants.

## 5. Personalization / memory angles

This is the load-bearing intersection.

- **Engram = externalized conditional memory.** Liang Wenfeng's Dec 2025 paper (`https://arxiv.org/abs/2601.07372`) formalizes a *Sparsity Allocation Law*: 20-25% of sparse params in static external memory, 75-80% in MoE compute. Engram modernizes N-gram lookup as O(1) access. At 27B scale, gains span knowledge **and** reasoning (BBH +5.0, ARC-Challenge +3.7, HumanEval +3.0, MMLU +3.4); Needle-in-a-Haystack 84.2 → 97 (`https://venturebeat.com/data/deepseeks-conditional-memory-fixes-silent-llm-waste-gpu-cycles-lost-to`). Code: `https://github.com/deepseek-ai/Engram`.
- **DeepSeek's framing:** memory as a *separate axis* from reasoning, complementary to MoE. Structurally adjacent to Beyond Recall's "recall vs interpretation" distinction — DeepSeek splits *storage* from *computation*; Beyond Recall splits *retrieved facts* from *interpretive significance*. Not the same claim; mutually citable.
- **No first-party personalization product.** No user memory feature, profile system, or personalization API. Left to the application layer.
- **Agentic capabilities:** explicit. Tool use, MCPAtlas, Toolathlon, BrowseComp shipped on the model card. "Personal assistant" named in adjacent docs as a deployment target, not a product.

## 6. Outreach surface

DeepSeek does not elevate individual researchers the way US labs do. Corporate face is the founder; technical bylines are large.

- **Liang Wenfeng** (founder/CEO). First author on the Engram paper. Best single point of contact for a substantive research note.
- **Daya Guo** (`https://guoday.github.io/`). Senior researcher; consistent author across V3/R1/V4; NLP + code intelligence.
- **Damai Dai** (PKU PhD). Co-author across V3/R1/V4 and Engram alongside the PKU collaboration.
- **Bingxuan Wang.** Recurring author on V3/R1/V4 technical reports.
- **Org email:** `service@deepseek.com` (no public research aliases).
- **GitHub:** `https://github.com/deepseek-ai`, memory module at `https://github.com/deepseek-ai/Engram`.

## Relevance to Beyond Recall outreach

**Concrete recommendations:**

1. **Add V4-Flash as a Tier 2 response model in any v11+ replication.** MIT, 1M context, $0.14/M input — cheaper than every model in the current Tier 2 panel. Adds Chinese-lab coverage. Use Think-High to match GPT-5.4 / Gemini 2.5 Pro reasoning posture. Skip V4-Pro unless a subject demands it.
2. **Do not add V4 as a judge.** The 5-judge panel is locked; a sixth judge mid-replication corrupts inter-judge agreement.
3. **Lead outreach with the Engram intersection, not the benchmark.** DeepSeek argues memory is a separate axis; Beyond Recall argues interpretation is a separate layer above retrieval. Independent angles, converging structural claim: storage and use must be separated. That is the hook.
4. **Target order:** (a) short non-promotional discussion on `deepseek-ai/Engram`; (b) email Liang Wenfeng via `service@deepseek.com` with the paper PDF and a one-paragraph framing of the parallel; (c) tag Daya Guo on X if/when posting.
5. **No product or partnership pitch.** DeepSeek is research-first; commercial framing filters out. Send the paper, name the intersection, ask one question.
6. **Defer until after arXiv goes live.** No Letta-style relational reason for a pre-publish heads-up.

## Sources

All URLs are inlined in the relevant section. Primary sources: official release notes, HuggingFace model card, arXiv 2601.07372, MIT Tech Review, TechCrunch, Bloomberg, VentureBeat, DeepSeek API pricing page, Nature R1 paper, Daya Guo's site.
