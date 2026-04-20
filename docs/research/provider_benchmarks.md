# Provider Benchmark Scores — Primary Source Audit

**Purpose:** verify the paper's claim that Mem0, Letta, Supermemory, and Zep all "score 85%+ on recall benchmarks."

**Date of audit:** 2026-04-17

## Summary Table

| Provider | Benchmark | Best reported score | Model | Self / Independent | Source type | Date | Hits 85%+? |
|---|---|---|---|---|---|---|---|
| Mem0 | LOCOMO | **91.6** | unspecified in blog; paper used GPT-4o-mini at 66.88 | Self-reported (vendor blog); paper is academic but reports lower numbers | Blog `mem0.ai/research` + arXiv 2504.19413 | Apr 2025 (paper), 2026 blog | Yes on blog, No in peer-reviewable paper |
| Mem0 | LongMemEval | **93.4** | unspecified | Self-reported (vendor blog only) | `mem0.ai/research` | 2026 | Yes (blog only) |
| Letta | LOCOMO | **74.0%** | GPT-4o-mini, Filesystem approach | Self-reported (vendor blog) | `letta.com/blog/benchmarking-ai-agent-memory` | 2025-08-12 | **No** |
| Letta | LongMemEval | no published score found | — | — | — | — | **No** |
| Supermemory | LongMemEval_s | **85.2%** | Gemini-3-Pro | Self-reported (vendor research page) | `supermemory.ai/research` | 2026 | **Yes** (narrowly) |
| Supermemory | LongMemEval_s | **~99%** | Agent Swarm (ASMR, experimental, not prod) | Self-reported | `blog.supermemory.ai/we-broke-the-frontier-...` | ~Mar 2026 | Yes, but experimental |
| Zep | LongMemEval | **71.2%** | GPT-4o | Self-reported + arXiv paper | arXiv 2501.13956 + `blog.getzep.com/state-of-the-art-agent-memory` | 2025-01-22 | **No** |

## 1. Mem0 ([mem0.ai](https://mem0.ai))

- **Benchmark (paper):** LOCOMO
- **Score (paper):** 66.88 ± 0.15 on LLM-as-Judge metric (Mem0 base); 68.44 ± 0.17 (Mem0 with graph, "Mem0^g"); per-category: Single-Hop 67.13, Multi-Hop 51.15, Open-Domain 72.93, Temporal 55.51
- **Model (paper):** GPT-4o-mini
- **Source (paper):** Chhikara et al., "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413, submitted 2025-04-28. <https://arxiv.org/abs/2504.19413>
- **Benchmark (vendor blog):** LOCOMO, LongMemEval, BEAM
- **Score (vendor blog):** 91.6 on LOCOMO, 93.4 on LongMemEval, 64.1 / 48.6 on BEAM 1M / 10M
- **Source (vendor blog):** <https://mem0.ai/research> and <https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm> (blog post "Introducing The Token-Efficient Memory Algorithm," ~April 2026 per search snippets)
- **Self-reported or independent:** paper numbers are peer-reviewable; blog numbers are vendor self-report for a newer "token-efficient algorithm" that does not appear to have a corresponding published paper yet
- **Confidence:** **Medium-Low on the 91.6 / 93.4 claim.** The gap between the April 2025 paper (66.88 on LOCOMO) and the 2026 blog (91.6 on LOCOMO) is +25 points and is not independently verified. Zep has published a critical post titled "Lies, Damn Lies, and Statistics: Is Mem0 Really SOTA in Agent Memory?" disputing Mem0's claims (<https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/>). There is also an open GitHub issue "Failed to reproduce the accuracy on LOCOMO via Mem0 platform" (`mem0ai/mem0` #3944).
- **Citable academic number:** 68.44 on LOCOMO (Mem0^g), GPT-4o-mini, Chhikara et al. 2025 — **this does not hit 85%+.**

## 2. Letta ([letta.com](https://letta.com), formerly MemGPT)

- **Benchmark:** LOCOMO
- **Score:** 74.0% accuracy
- **Model:** GPT-4o-mini, using Letta's Filesystem approach (conversation history stored as files with semantic search / grep / answer_question tools)
- **Source:** "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" <https://www.letta.com/blog/benchmarking-ai-agent-memory>
- **Self-reported or independent:** self-reported
- **Date:** 2025-08-12
- **Note on the original MemGPT paper:** Packer et al., "MemGPT: Towards LLMs as Operating Systems," arXiv:2310.08560 — does not report on LOCOMO or LongMemEval (those benchmarks postdate it) and does not report an 85%+ recall number on any standard memory benchmark. The paper evaluates on document QA and nested KV retrieval tasks.
- **LongMemEval:** no Letta-published LongMemEval score was found. Letta does maintain a "Letta Leaderboard" (<https://www.letta.com/blog/letta-leaderboard>) but it benchmarks LLMs, not Letta-as-a-memory-system.
- **Confidence:** **High** that 74.0% on LOCOMO is the best publicly available Letta score. **High** that there is no Letta-published 85%+ number.
- **Verdict:** **Does not hit 85%+ on any published benchmark.**

## 3. Supermemory ([supermemory.ai](https://supermemory.ai))

- **Benchmark:** LongMemEval_s (500-question variant from the ICLR 2025 LongMemEval paper)
- **Score:** 81.6% with GPT-4o; **85.2% with Gemini-3-Pro** (production system); ~99% with experimental "Agent Swarm / ASMR" (not production)
- **Model:** Gemini-3-Pro for the 85.2% figure
- **Source:** <https://supermemory.ai/research/> and <https://blog.supermemory.ai/we-broke-the-frontier-in-agent-memory-introducing-99-sota-memory-system/>
- **Self-reported or independent:** self-reported. Supermemory also open-sourced their harness as `memorybench` (<https://github.com/supermemoryai/memorybench>), which is a partial mitigation of the self-report concern.
- **Date:** 2026 (research page); ~March 2026 (99% blog post)
- **Confidence:** **High** that 85.2% is what Supermemory claims; **Medium** that the number is reproducible by a third party (the open harness helps but no independent re-run has been cited in the sources I checked).
- **Verdict:** **Hits 85%+, but only with Gemini-3-Pro and only as a self-reported number.** The 81.6% with GPT-4o (the cross-vendor-comparable setting) does not clear 85%.

## 4. Zep ([getzep.com](https://getzep.com))

- **Benchmark:** LongMemEval (full, not the 's' variant)
- **Score:** 71.2% with GPT-4o; 63.8% with GPT-4o-mini
- **Model:** GPT-4o for the headline number
- **Source:** Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory," arXiv:2501.13956 <https://arxiv.org/abs/2501.13956>; blog: <https://blog.getzep.com/state-of-the-art-agent-memory/>
- **Self-reported or independent:** self-reported in both venues (same authors)
- **Date:** 2025-01-20 (paper); 2025-01-22 (blog)
- **Confidence:** **High.** 71.2% is the number in Zep's own arXiv paper. No higher Zep number on a standard recall benchmark was located.
- **Verdict:** **Does not hit 85%+.**

---

## Cross-Provider Honest Assessment

- Only **one of the four providers (Supermemory) has a self-reported score at or above 85%** on a standard recall benchmark, and only with Gemini-3-Pro on LongMemEval_s.
- **Zep's** best self-reported number on a comparable benchmark is 71.2% (LongMemEval, GPT-4o).
- **Letta's** best self-reported number is 74.0% (LOCOMO, GPT-4o-mini). They have no LongMemEval score.
- **Mem0's** peer-reviewable paper number is 68.44% on LOCOMO. Their blog claims 91.6 / 93.4, but these lack a published methodology, are disputed by a competitor (Zep), and have at least one open reproduction issue on their own GitHub.
- The four systems also do not report on the same benchmark with the same model, so head-to-head comparisons are messy: Mem0 (paper) and Letta use LOCOMO; Zep and Supermemory use LongMemEval; scores across benchmarks are not directly comparable.

## Recommended Rewrite for the Paper

The claim "all four score 85%+ on recall benchmarks" is **not supportable from primary sources**. Tightest honest versions in descending order of safety:

1. **Safest:** "Each of these systems reports strong results on a long-term-conversational-memory benchmark (LOCOMO or LongMemEval), with scores ranging from roughly 68% to 85%+ depending on provider, model, and benchmark variant. Scores are self-reported and not directly comparable."
2. **Specific, still safe:** "Published numbers: Mem0 68.44 (LOCOMO, paper) / 91.6 (blog); Letta 74.0 (LOCOMO); Zep 71.2 (LongMemEval); Supermemory 81.6 (LongMemEval_s, GPT-4o) rising to 85.2 (Gemini-3-Pro)."
3. **If the paper only needs a rhetorical gesture toward "these vendors claim high recall":** "Vendors report LOCOMO/LongMemEval accuracies in the 70s–90s range, though numbers are self-reported, methodologies vary, and independent replications are limited."
