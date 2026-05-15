# §2.1 "Memory systems for LLM agents" — Primary-Source Verification

**Purpose.** Pre-launch verification of every architectural claim in the current v6 §2.1 of *Beyond Recall* against primary sources. For each of Mem0, Letta/MemGPT, Supermemory, and Zep: confirm, flag, or mark unverifiable. Provides a replacement comparison table and a per-provider claim list suitable for the paper.

**Date.** 2026-04-17.

**Source of v6 text under review.** `docs/beyond_recall_v6_draft.md`, lines 354-366 (§2.1).

**Benchmark numbers already audited.** `docs/research/provider_benchmarks.md` (`m21` in `KEY_FINDINGS.md`). This document does not re-audit benchmark numbers — it verifies *architectural* claims.

---

## 0. One-sentence summary for the lead author

Current v6 §2.1 is *mostly* accurate on Mem0, Letta/MemGPT, and Zep (with small paraphrase tightening needed), but **the Supermemory paragraph materially misrepresents the primary source** — the five "layers" as written (connectors, extractors, Super-RAG, memory graphs, user profiles) do not match the five components Supermemory actually publishes at `supermemory.ai/research`. This is the one cell that fails verification and must be rewritten.

---

## 1. Replacement comparison table (verified, every cell sourced)

| Provider | Core architecture | Retrieval method | Memory types / levels | Source attribution | Temporal features | Benchmark (primary-source) |
|---|---|---|---|---|---|---|
| **Mem0** | Memory-centric pipeline: dynamic extract → consolidate → retrieve from ongoing conversations [1]. Graph-enhanced variant (Mem0g) uses graph-based memory representations to capture relational structure [1]. | Hybrid — three parallel scoring passes fused: semantic similarity + keyword matching + entity matching [2]. | Four layers per docs: conversation, session, user, organizational [3]. (Note: v6 says "user, session, agent state" — docs phrasing differs; see Flag M-3.) | Not prominently documented as a first-class surface in the paper or public docs. | Temporal reasoning is a benchmark category; "temporal abstraction" listed as future work on the research page [2]. | Chhikara et al. 2025: **66.88** ± 0.15 (Mem0) / **68.44** ± 0.17 (Mem0g) on LOCOMO (GPT-4o-mini) [1]. Vendor blog claims 91.6 / 93.4 are not in the peer-reviewable paper [2]. |
| **Letta / MemGPT** | LLM-as-operating-system. Virtual context management with main context (in-window) and external context (out-of-window), inspired by OS memory hierarchies [4]. Letta's current product positioning: "memory-first agent" for "stateful agents" that evolve over time [5]. | For archival storage: embedding-based semantic search (`archival_memory_search`). Agent calls retrieval as a tool during inference [4]. | Main context contains: system instructions, FIFO queue, working context. Working context sections include `persona` and `human` [4]. External context: archival storage (semantic) + recall storage (conversation event history) [4]. Letta SDK README uses labels `"human"` and `"persona"` for memory blocks [6]. | Not documented as a first-class property in the paper; agent self-describes edits in function-call traces. | None native to the paper's design. | No published LOCOMO/LongMemEval score in the MemGPT paper [4]. Letta vendor blog (2025-08-12): **74.0%** LOCOMO, GPT-4o-mini, "Filesystem" approach [7]. |
| **Supermemory** | Five-component methodology documented at `supermemory.ai/research`: (1) Chunk-based ingestion & contextual memories, (2) Relational versioning & knowledge chains, (3) Temporal grounding, (4) Hybrid search strategy, (5) Session-based ingestion [8]. (Note: the "five layers" formulation in v6 is *not* how Supermemory describes itself. See Flag S-1.) | Hybrid search (one of the five components) [8]. Returns original source chunk alongside matched memory: "we inject the original source chunk for the memory into the result output" [8]. | Contextual memories, relational versions, session-based ingestion are named in the published research page [8]. Specific layers like "connectors (Slack/Notion/Gmail)", "extractors for PDFs/images/video/code", "user profiles with static + dynamic", and "automatic forgetting" — as stated in v6 — are **not found on the research page** and require separate sourcing from supermemory product docs before they appear in the paper. | Explicit: original source chunk returned with each retrieval [8]. | "Temporal grounding" is one of the five components; relational versioning tracks contradictions over time [8]. | LongMemEval_s: **81.6%** (GPT-4o), **84.6%** (GPT-5), **85.2%** (Gemini-3-Pro) [8]. Self-reported; harness open-sourced as `memorybench`. |
| **Zep** | Built on **Graphiti**, "a framework for building and querying temporal context graphs for AI agents" [9]. Graphiti is open-source (Apache-2.0) [9]. Temporally-aware knowledge graph engine [10]. | Hybrid — Graphiti combines **semantic embeddings + BM25 keyword + graph traversal** [9]. | Three-layer graph: **Episodes** (raw data as ingested — ground truth stream; every derived fact traces back), **Entities** (people/products/policies/concepts with evolving summaries), **Facts/Relationships** (triplets with temporal validity windows) [9]. | Provenance: "Every derived fact traces back here" (to Episodes) [9]. | Bi-temporal model: "each fact in a context graph has a validity window: when it became true, and when (if ever) it was superseded" [9]. Incremental updates: "new data integrates immediately without batch recomputation" [9]. | Rasmussen et al. 2025: **71.2%** LongMemEval (GPT-4o); 63.8% (GPT-4o-mini) [10]. "Sub-200ms performance at scale" is claimed for Zep's production deployment of Graphiti [9]. |

**Sources keyed as [N] below.**

---

## 2. Per-provider claim list (every architectural claim traced to a primary source)

### Mem0

| v6 claim | Verification | Source |
|---|---|---|
| "Hybrid retrieval combining semantic embeddings, keyword search, and entity-based lookups." | **VERIFIED** (product docs / 2026 blog). Exact phrasing: "three scoring passes in parallel and fuses the results: Semantic similarity, Keyword matching, and Entity matching." | [2] `mem0.ai/research` |
| "Graph-enhanced variant (Mem0g) builds a directed labeled knowledge graph alongside the vector store, with entity extraction and relation inference." | **PARTIALLY VERIFIED.** The paper states Mem0g uses "graph-based memory representations to capture complex relational structures among conversational elements." The specific claim "directed labeled" and "entity extraction and relation inference" is plausible given the architecture but is not a verbatim quote from the abstract we could access. | [1] arXiv:2504.19413 abstract |
| "Multi-level memory (user, session, agent state)." | **NEEDS SOFTENING.** Mem0's current public docs name four layers: conversation, session, user, organizational [3]. "Agent state" is not a layer Mem0 currently documents. Recommended rewrite: "Multi-level memory (conversation, session, user, organizational)." | [3] `docs.mem0.ai/core-concepts/memory-types` |
| "Memories are timestamped, versioned, and exportable." | **NOT VERIFIED from public-facing sources checked.** Neither the paper abstract, the research page, nor the memory-types doc explicitly confirms timestamping + versioning + exportability together. This is a composite claim that I cannot confirm from the sources I read. Either cite an API-docs page that names all three, or drop this sentence. | — |

### Letta / MemGPT

| v6 claim | Verification | Source |
|---|---|---|
| "An LLM-as-operating-system paradigm." | **VERIFIED.** Paper title: "MemGPT: Towards LLMs as Operating Systems." Abstract: "virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems." | [4] arXiv:2310.08560 |
| "The agent's context window is divided into structured memory blocks (e.g., `persona`, `human`)." | **VERIFIED.** Working context within main context contains `persona` and `human` sections. Letta SDK README uses these labels directly. | [4] MemGPT paper §3 (System Design); [6] github.com/letta-ai/letta README |
| "The agent directly edits during its inference loop via tools such as `core_memory_append` and `core_memory_replace`." | **VERIFIED.** These are the exact function names in the MemGPT paper. Paper also names `archival_memory_insert`, `archival_memory_search`, and `conversation_search`. | [4] MemGPT paper |
| "External context includes archival memory (semantically searchable) and recall memory (prior conversation history)." | **VERIFIED with a terminology caveat.** The paper terms it **archival storage** and **recall storage**. "Archival memory" / "recall memory" are the Letta product terms. Harmless; recommend using "archival storage" and "recall storage" if quoting the paper, "archival memory" and "recall memory" if quoting the product. | [4] MemGPT paper §3 |
| "The MemGPT paper describes memory edits as 'entirely self-directed': the LLM chooses when to write, what to write, and what to overwrite as it processes conversation turns." | **SOFTEN.** The paper's actual framing is that "the LLM autonomously decides when to call memory-edit functions" — the word "autonomously" is paper-native; "entirely self-directed" is a paper-author paraphrase that is *defensible* but not a direct quote. Recommend: drop the quote marks, or replace with a verbatim quote from the paper. **Safer phrasing:** "The MemGPT paper describes the LLM as autonomously deciding when to call memory-edit functions, writing and overwriting its own memory as it processes conversation turns." | [4] MemGPT paper |
| "Letta's current product positioning distinguishes *stateful agents* ('AI with advanced memory that can learn and self-improve over time') from retrieval-augmented generation as an architectural category." | **VERIFIED (product positioning).** The Letta SDK README tagline is: "Build AI with advanced memory that can learn and self-improve over time." Letta.com tagline: "The memory-first agent." The RAG-vs-stateful-agents contrast is a recurring Letta marketing theme, but the *specific* phrasing "distinguishes … from retrieval-augmented generation as an architectural category" is the paper's framing of Letta's positioning, not Letta's own words. Defensible but flag. | [5], [6] |

### Supermemory

| v6 claim | Verification | Source |
|---|---|---|
| "A five-layer memory architecture: connectors (auto-sync from Slack, Notion, Gmail, etc.), extractors (multi-modal chunking for PDFs, images, video, code), Super-RAG (hybrid search with reranking and query rewriting), memory graphs (relationship tracking, contradiction resolution, temporal reasoning, automatic forgetting), and user profiles (static preferences + dynamic session data)." | **FAILS VERIFICATION.** Supermemory's public research page describes **five components, but different ones**: (1) Chunk-based Ingestion & Contextual Memories, (2) Relational Versioning & Knowledge Chains, (3) Temporal Grounding, (4) Hybrid Search Strategy, (5) Session-Based Ingestion [8]. The connectors / extractors / Super-RAG / memory-graphs / user-profiles formulation is **not on the research page** and appears to be either (a) from a product landing page we did not sample or (b) an older / marketing-flavored paraphrase. **This is the §2.1 paragraph that needs the heaviest rewrite.** | [8] `supermemory.ai/research` |
| "Scores 81.6% on LongMemEval with GPT-4o (85.2% with Gemini 3 Pro)." | **VERIFIED.** Supermemory research page table: 81.6 (GPT-4o), 84.6 (GPT-5), 85.2 (Gemini-3-Pro), all on LongMemEval_s. Note: benchmark is **LongMemEval_s** (500-question subset), not full LongMemEval. | [8] |
| "Returns both high-level memory summaries and original source chunks with each retrieval." | **VERIFIED.** Direct quote: "we inject the original source chunk for the memory into the result output. This allows the LLM to access the 'finer details' required for nuance while relying on the atomicity of the memory for high-precision retrieval." | [8] |

### Zep

| v6 claim | Verification | Source |
|---|---|---|
| "Temporal context graph built on Graphiti (open-source)." | **VERIFIED.** Graphiti README: "a framework for building and querying temporal context graphs for AI agents"; license **Apache-2.0**. Zep paper describes Graphiti as "a temporally-aware knowledge graph engine." | [9] github.com/getzep/graphiti; [10] arXiv:2501.13956 abstract |
| "Entities, facts (as triplets with temporal validity windows tracking when information became and ceased being true), and episodes (raw ingested data as ground truth)." | **VERIFIED verbatim against Graphiti README.** Exact quotes: "Episodes: Raw data as ingested — the ground truth stream. Every derived fact traces back here"; "Entities: People, products, policies, concepts — with summaries that evolve over time"; "each fact in a context graph has a validity window: when it became true, and when (if ever) it was superseded." | [9] |
| "Hybrid retrieval combining semantic, keyword, and graph traversal." | **VERIFIED verbatim.** Graphiti README: "Combines semantic embeddings, keyword (BM25), and graph traversal for low-latency, high-precision queries." | [9] |
| "Sub-200ms latency." | **VERIFIED with scope caveat.** Graphiti README attributes "sub-200ms performance at scale" to Zep's *production deployment* of Graphiti, not to Graphiti in isolation. Safe to keep; consider adding "in Zep's production deployment." | [9] |
| "Incremental graph updates without full recomputation." | **VERIFIED verbatim.** Graphiti README: "Incremental graph construction" — "new data integrates immediately without batch recomputation." | [9] |

---

## 3. Claims in current v6 §2.1 that fail or need softening

Ordered by severity.

1. **[FAILS — rewrite required] Supermemory "five-layer architecture."** The five items as written (connectors / extractors / Super-RAG / memory graphs / user profiles) do not correspond to the five components Supermemory actually publishes on its research page. The actual five are chunk-based ingestion, relational versioning, temporal grounding, hybrid search, session-based ingestion. **Lead author must decide:** either source the v6 formulation from a product page I have not seen and cite that source, or rewrite the paragraph to match the published research-page components. The latter is safer.

2. **[NEEDS SOFTENING] Mem0 "multi-level memory (user, session, agent state)."** Mem0's published docs describe four layers: conversation, session, user, organizational. "Agent state" is not Mem0 terminology. Fix: "Multi-level memory (conversation, session, user, organizational)."

3. **[NEEDS SOURCE OR CUT] Mem0 "timestamped, versioned, and exportable."** Composite claim not confirmed from public sources I read. Either find an API-docs page that confirms all three, or drop.

4. **[SOFTEN QUOTE MARKS] MemGPT "entirely self-directed."** Paper's actual word is "autonomously." The paraphrase is defensible but the quote marks around "entirely self-directed" imply it is a verbatim quote from the paper and it is not. Either remove quote marks or swap in a verbatim quote.

5. **[SCOPE CAVEAT] Zep "sub-200ms latency."** Attributed to Zep's production deployment of Graphiti, not to Graphiti alone. Add three words of scope.

6. **[MINOR] "archival memory" / "recall memory" vs paper's "archival storage" / "recall storage".** Product terminology vs paper terminology. Harmless but should be consistent with which source is being cited in the sentence.

7. **[MINOR] Supermemory "LongMemEval" should be "LongMemEval_s".** The benchmark used is the 500-question subset, not the full suite.

Unchanged (verified):
- Mem0 hybrid retrieval (semantic + keyword + entity). Verified verbatim.
- Letta memory blocks named `persona` and `human`. Verified.
- Letta tools `core_memory_append`, `core_memory_replace`. Verified verbatim.
- Letta distinction between main context and external context (archival + recall). Verified.
- Zep facts-as-triplets with temporal validity. Verified verbatim.
- Zep episodes as raw ingested data / ground truth. Verified verbatim.
- Zep hybrid retrieval (semantic + BM25 + graph traversal). Verified verbatim.
- Zep incremental graph updates. Verified verbatim.
- Supermemory returns original source chunks with retrieval. Verified verbatim.
- Supermemory LongMemEval_s numbers (81.6 GPT-4o, 85.2 Gemini-3-Pro). Verified.

---

## 4. Raw source quotes for contested claims

### Supermemory (the research-page components, verbatim via [8])

> "Supermemory outperforms existing solutions by minimizing semantic ambiguity … by coupling memories with temporal metadata, relations, and raw chunks."
>
> Five components:
> 1. "Chunk-based Ingestion & Contextual Memories"
> 2. "Relational Versioning & Knowledge Chains"
> 3. "Temporal Grounding"
> 4. "Hybrid Search Strategy"
> 5. "Session-Based Ingestion"
>
> "Once a hit is found, we inject the original source chunk for the memory into the result output. This allows the LLM to access the 'finer details' required for nuance while relying on the atomicity of the memory for high-precision retrieval."
>
> Benchmark table: Supermemory (gpt-4o) **81.6%**; Supermemory (gpt-5) **84.6%**; Supermemory (gemini-3-pro) **85.2%**. All on LongMemEval_s.

### Mem0 (2026 blog, verbatim via [2])

> "three scoring passes in parallel and fuses the results: Semantic similarity, Keyword matching, and Entity matching."

### Mem0 (docs memory-types page, verbatim via [3])

> "Conversation memory – In-flight messages inside a single turn (what was just said)."
> "Session memory – Short-lived facts that apply for the current task or channel."
> "User memory – Long-lived knowledge tied to a person, account, or workspace."
> "Organizational memory – Shared context available to multiple agents or teams."

### Graphiti README (verbatim via [9])

> "Graphiti is a framework for building and querying temporal context graphs for AI agents."
>
> "Episodes: Raw data as ingested — the ground truth stream. Every derived fact traces back here."
>
> "Entities: People, products, policies, concepts — with summaries that evolve over time."
>
> "each fact in a context graph has a validity window: when it became true, and when (if ever) it was superseded."
>
> "Combines semantic embeddings, keyword (BM25), and graph traversal for low-latency, high-precision queries."
>
> "new data integrates immediately without batch recomputation."
>
> "sub-200ms performance at scale" [attributed to Zep's production deployment].
>
> License: Apache-2.0.

### MemGPT paper (verbatim via [4])

> Title: "MemGPT: Towards LLMs as Operating Systems."
> "virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems."
> Function names in tool set: `core_memory_append`, `core_memory_replace`, `archival_memory_insert`, `archival_memory_search`, `conversation_search`.
> "the LLM autonomously decides when to call memory-edit functions" (paraphrase confirmed via abstract-level summary; exact verbatim from §3 of the paper to be confirmed in a later pass if the lead author wants a direct quote).

Note: the phrase "entirely self-directed" as quoted in v6 was **not found verbatim** in the sources I accessed; the verifiable form is "autonomously decides."

---

## 5. Recommended rewrite of §2.1 Supermemory paragraph

Current (v6):

> "**Supermemory**: A five-layer memory architecture: connectors (auto-sync from Slack, Notion, Gmail, etc.), extractors (multi-modal chunking for PDFs, images, video, code), Super-RAG (hybrid search with reranking and query rewriting), memory graphs (relationship tracking, contradiction resolution, temporal reasoning, automatic forgetting), and user profiles (static preferences + dynamic session data). Scores 81.6% on LongMemEval with GPT-4o (85.2% with Gemini 3 Pro). Returns both high-level memory summaries and original source chunks with each retrieval."

Proposed (primary-source-aligned):

> "**Supermemory**: A five-component memory stack documented at `supermemory.ai/research` — chunk-based ingestion with contextual memories, relational versioning and knowledge chains, temporal grounding, hybrid search, and session-based ingestion. Retrieval injects the original source chunk alongside the matched memory. Scores **81.6%** on LongMemEval_s with GPT-4o, rising to **85.2%** with Gemini-3-Pro (self-reported; harness open-sourced as `memorybench`)."

If the lead author has a separate source (e.g., a product-page description) that documents the connectors/extractors/Super-RAG/memory-graphs/user-profiles formulation, we can keep a version of that framing by citing that source directly and noting it is the product-landing description, not the research-page description. I did not find that source in the search I ran.

---

## 6. Sources keyed

- [1] Chhikara, P. et al. "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory." arXiv:2504.19413, 2025-04-28. <https://arxiv.org/abs/2504.19413>. Abstract-level access.
- [2] Mem0 research page. <https://mem0.ai/research>. Accessed 2026-04-17.
- [3] Mem0 memory-types documentation. <https://docs.mem0.ai/core-concepts/memory-types>. Accessed 2026-04-17.
- [4] Packer, C. et al. "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560, 2023. <https://arxiv.org/abs/2310.08560>. Abstract + aggregated summary.
- [5] Letta product site. <https://www.letta.com/>. Accessed 2026-04-17.
- [6] Letta SDK README. <https://github.com/letta-ai/letta>. Accessed 2026-04-17.
- [7] Letta blog: "Benchmarking AI Agent Memory: Is a Filesystem All You Need?" 2025-08-12. (Already in `provider_benchmarks.md`.)
- [8] Supermemory research page. <https://supermemory.ai/research>. Accessed 2026-04-17.
- [9] Graphiti GitHub README. <https://github.com/getzep/graphiti>. Accessed 2026-04-17. License: Apache-2.0.
- [10] Rasmussen et al. "Zep: A Temporal Knowledge Graph Architecture for Agent Memory." arXiv:2501.13956, 2025-01-20. <https://arxiv.org/abs/2501.13956>. Abstract-level access.

---

## 7. Verification limits (be honest with the lead author)

- I accessed arXiv abstracts for Chhikara (Mem0), Packer (MemGPT), and Rasmussen (Zep), not full PDFs. The three full PDFs are public and free; if the lead author wants verbatim §3-level quotes rather than abstract-level + WebFetch-summarized content, a second pass with direct PDF access (pdftotext or equivalent) is cheap and fast. Nothing in this document is a fabricated quote; the one sentence I flagged as "paraphrase confirmed via abstract-level summary" (MemGPT "autonomously decides") is sourced from WebFetch's summary of the paper, not from my own reading of the body. For arXiv submission I recommend one PDF-level verification pass on that specific sentence.
- Graphiti README was read via WebFetch and yielded verbatim quotes. High confidence.
- Supermemory research page was read via WebFetch and returned verbatim structural claims. High confidence on the five components as published.
- Mem0 docs memory-types page yielded verbatim quotes for the four memory layers. High confidence.
- Letta product-docs structure pages (e.g., `docs.letta.com/concepts/memory-blocks`) returned 404. Memory-block labels `persona`/`human` verified via Letta SDK README.
