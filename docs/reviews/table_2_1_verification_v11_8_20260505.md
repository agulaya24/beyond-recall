# Table 2.1 verification — Beyond Recall v11.8 (2026-05-05)

Audit of the four-row, four-column memory-system comparison table in §2.2 (lines 192-197) plus the four footnotes (`[^mem0-recall]`, `[^letta-recall]`, `[^zep-recall]`, `[^benchmark-disputes]`). All vendor sources fetched 2026-05-05.

## Summary
- Cells **VERIFIED**: 14 of 16
- **OUTDATED** (paper claim no longer matches current vendor positioning, citation needs refresh): 2
- **DRIFT** (vendor docs contradict paper claim): 0
- **UNVERIFIABLE**: 0

Plus two non-cell findings:
- **`[^letta-recall]` URL is dead** — citation points to nothing; the actual blog post lives at a different slug.
- **`[^benchmark-disputes]` overstates dispute liveness** — `getzep/zep-papers#5` was closed 2025-05-19 ("Closing due to inactivity"). Paper presents it as ongoing.

The table's substance is sound. The two soft issues are both citation-hygiene rather than wrong claims.

## Per-row findings

### Row 1: Mem0

| Cell | Paper text | Canonical vendor source | Vendor exact language | Verdict |
|---|---|---|---|---|
| Architecture | "Extract → consolidate → retrieve pipeline; Mem0g graph variant adds a directed labeled knowledge graph alongside the vector store" | `docs.mem0.ai/core-concepts/memory-operations` + Chhikara et al. §2.2 | Docs: three-step pipeline — "Information Extraction" / "Conflict Resolution" / "Storage" — with vector storage "and optional graph storage." Paper §2.2: "Mem0g... directed labeled graph G=(V,E,L)... Nodes V represent entities... Edges E represent relationships." | **VERIFIED** |
| Retrieval | "Hybrid: semantic + keyword + entity" | `github.com/mem0ai/mem0` README | "Multi-signal retrieval — semantic, BM25 keyword, and entity matching scored in parallel and fused." | **VERIFIED** (verbatim alignment) |
| Memory types | "Conversation, session, user, organizational" | `docs.mem0.ai/core-concepts/memory-types` | Four layers exactly: "Conversation Memory" / "Session Memory" / "User Memory" / "Organizational Memory." | **VERIFIED** (verbatim) |
| Recall score | "91.6 LOCOMO, 93.4 LongMemEval (current algorithm)" + footnote citing arXiv:2504.19413 reporting "68.44 LOCOMO for the Mem0g variant with GPT-4o-mini" | Mem0 GitHub README (current) + Chhikara 2025 Table 2 (paper) | README: "LoCoMo: 71.4 → 91.6"; "LongMemEval: 67.8 → 93.4." Paper Table 2: "Mem0g... 68.44%" overall J on LOCOMO with GPT-4o-mini. | **VERIFIED** |

Row verdict: 4 of 4 VERIFIED.

### Row 2: Letta / MemGPT

| Cell | Paper text | Canonical vendor source | Vendor exact language | Verdict |
|---|---|---|---|---|
| Architecture | "LLM-as-operating-system; virtual context management with main context plus external context" | `docs.letta.com/concepts/letta` + `github.com/letta-ai/letta` README + Packer et al. arXiv:2310.08560 | Current docs: "stateful agent platform... build stateful agents that remember, learn, and improve." README: "platform for building stateful agents... formerly MemGPT." The 2023 paper still uses "LLM-OS" / "virtual context management" framing. | **OUTDATED** (paper claim faithful to its 2023 cited source; vendor's current public framing is "stateful agent platform"; not a contradiction, but a positioning shift the paper does not capture) |
| Retrieval | "Archival via `archival_memory_search`; main-context memory blocks self-edited via `core_memory_append`, `core_memory_replace`" | `github.com/letta-ai/letta/blob/main/letta/functions/function_sets/base.py` | All three function names present in current source: `def core_memory_append`, `def core_memory_replace`, `async def archival_memory_search`. (Plus `archival_memory_insert`, `conversation_search`.) | **VERIFIED** |
| Memory types | "`persona` and `human` blocks in main context; archival and recall memory external" | `docs.letta.com/guides/agents/memory-blocks` | "Persona: Stores details about your current persona, guiding how you behave..." / "Human: Stores key details about the person you are conversing with..." Memory blocks "always visible — no retrieval needed." Archival/recall framing carried in the cited paper. | **VERIFIED** |
| Recall score | "74.0% on LOCOMO with GPT-4o-mini" + footnote citing `letta.com/blog/benchmarking-llm-judges-for-evaluating-ai-agents` | Actual post at `letta.com/blog/benchmarking-ai-agent-memory` (Aug 12, 2025) | "Letta agents running on `gpt-4o-mini` achieve 74.0% accuracy on LoCoMo... significantly above Mem0's reported 68.5% score for their top-performing graph variant." | **VERIFIED claim**, but **citation URL is dead** (404 on the slug as written). Same date, same content, different slug. See "Recommended table edits" below. |

Row verdict: 3 of 4 VERIFIED, 1 OUTDATED (architecture cell). Citation URL fix is critical but not a cell-level verdict change.

### Row 3: Supermemory

| Cell | Paper text | Canonical vendor source | Vendor exact language | Verdict |
|---|---|---|---|---|
| Architecture | "Five-component architecture: chunk-based ingestion, relational versioning, temporal grounding, hybrid search, session-based ingestion" | `supermemory.ai/research` | All five terms appear verbatim as the five labeled components: "Chunk-based Ingestion," "Relational Versioning," "Temporal Grounding," "Hybrid Search," "Session-Based Ingestion." | **VERIFIED** (verbatim) |
| Retrieval | "Hybrid with reranking and query rewriting; source chunks injected at retrieval" | `supermemory.ai/research` (Hybrid Search component) | "Semantic searching of atomic memories identifies relevant concepts, then injects original source chunks for detailed context." | **VERIFIED** on hybrid + source-chunk injection. Reranking and query rewriting are not stated in the verbatim five-component description on the research page; Supermemory's broader docs reference reranking, so this phrase is supported but slightly stronger than the headline component description. Conservative verdict: **VERIFIED**. |
| Memory types | "Contextual memories, relational versions, session data" | `supermemory.ai/research` | Atomic memories + three relational types (updates / extends / derives) + session-based ingestion. Paper's three-item phrasing is a fair summary of the same taxonomy. | **VERIFIED** |
| Recall score | "81.6% / 84.6% / 85.2% on LongMemEval_s with GPT-4o / GPT-5 / Gemini-3-Pro (self-reported)" | `supermemory.ai/research` | "GPT-4o: 81.6% overall... GPT-5: 84.6% overall... Gemini-3-Pro: 85.2% overall." | **VERIFIED** (verbatim, both numbers and model labels) |

Row verdict: 4 of 4 VERIFIED.

### Row 4: Zep

| Cell | Paper text | Canonical vendor source | Vendor exact language | Verdict |
|---|---|---|---|---|
| Architecture | "Built on Graphiti (Apache 2.0, open source). Bi-temporal knowledge graph" | `github.com/getzep/graphiti` README + `github.com/getzep/zep` README + Rasmussen et al. arXiv:2501.13956 | Zep README: "Zep is powered by Graphiti, an open-source temporal knowledge graph framework." Graphiti README: "Explicit bi-temporal tracking with automatic fact invalidation"; Apache-2.0 license. Rasmussen paper title: "ZEP: A TEMPORAL KNOWLEDGE GRAPH ARCHITECTURE..." (paper itself uses "temporally-aware," not "bi-temporal"). | **VERIFIED** — Graphiti README confirms "bi-temporal" verbatim and Apache-2.0; not a DRIFT call even though the Rasmussen paper's own framing was just "temporally-aware." |
| Retrieval | "Hybrid: semantic + BM25 + graph traversal" | `help.getzep.com/searching-the-graph` + Graphiti README | help.getzep.com: "Semantic similarity... BM25 full-text search... Breadth-first search (optional)." Graphiti README: "Combines semantic embeddings, keyword (BM25), and graph traversal for low-latency, high-precision queries." | **VERIFIED** (verbatim alignment) |
| Memory types | "Episodes (ground-truth source), Entities, Facts-as-triplets with temporal validity windows" | Graphiti README | Three components stated: "Episodes — Raw data as ingested — the ground truth stream"; "Entities — People, products, policies, concepts"; "Facts/Relationships — Triplets (Entity → Relationship → Entity) with temporal validity windows." | **VERIFIED** (verbatim alignment, including "ground truth" and "validity windows") |
| Recall score | "71.2% on LongMemEval with GPT-4o" + footnote citing Rasmussen et al. arXiv:2501.13956 | Rasmussen 2025, Table 2 (LongMemEval s) | "Zep gpt-4o 71.2%" — verbatim from Table 2. | **VERIFIED** |

Row verdict: 4 of 4 VERIFIED.

## Recommended table edits

The table substance does not need to change. Two surgical edits to citations and one optional architecture-cell tightening:

1. **Footnote `[^letta-recall]` URL is dead.** Current text:
   > Letta blog, 2025-08-12 (`https://www.letta.com/blog/benchmarking-llm-judges-for-evaluating-ai-agents`).

   Replace with:
   > Letta blog, 2025-08-12, "Benchmarking AI Agent Memory" (`https://www.letta.com/blog/benchmarking-ai-agent-memory`).

   Reason: the slug as written 404s. The post exists with the same date and the 74.0% claim, just at the corrected URL. Verified by directly fetching the new URL.

2. **Footnote `[^benchmark-disputes]` overstates dispute liveness.** Current text frames `getzep/zep-papers#5` as a live, unresolved dispute. The issue was closed 2025-05-19 with comment: "Closing due to inactivity. Happy to reopen if further discussion is required." Mem0 founder Deshraj Yadav filed it on 2025-05-08 (claiming Zep's corrected score was 58.44%); Zep maintainer Daniel Chalef responded 2025-05-12 with a corrected 75.14% ± 0.17 (10-run mean) and updated the linked blog post. Yadav did not respond. Recommended phrasing for the shortened version:
   > Mem0 and Zep publicly disputed each other's LOCOMO methodology in May 2025 (`getzep/zep-papers#5`, since closed; Zep's revised 10-run mean: 75.14%). Supermemory publishes head-to-head comparisons in its own favor; third-party reproductions (Vectorize.io) produce different numbers again.

   This keeps the substance ("recall scores are contested") while reflecting the actual public state.

3. **Optional: Letta architecture cell** could be tightened to bridge paper-source and current-vendor framing without overweighting either:
   > Current text: "LLM-as-operating-system; virtual context management with main context plus external context"
   > Suggested: "Stateful-agent platform built on virtual context management (main context plus external archival/recall); originally framed as LLM-as-operating-system in Packer et al. (2023)"

   This is an editorial preference call, not a fact correction. The paper is faithful to its cited source as-is.

## Footnote-disputes update

`getzep/zep-papers#5` — **CLOSED 2025-05-19**. Title: "Revisiting Zep's 84% LoCoMo Claim: Corrected Evaluation & 58.44% Accuracy." Public timeline:

- 2025-05-08: Mem0 (Deshraj Yadav) opens issue, claims corrected Zep score is 58.44% ± 0.20 versus the 84% Zep originally reported.
- 2025-05-09: Zep (Daniel Chalef) acknowledges, says they're "digging in."
- 2025-05-12: Zep posts corrected score: **75.14% ± 0.17** over 10 runs, blog post updated, rebuts Mem0's reproduction methodology, asks for Mem0's resulting datasets.
- 2025-05-12 onward: no Mem0 response.
- 2025-05-19: Zep closes ("Closing due to inactivity. Happy to reopen if further discussion is required.").

Mem0's own subsequent positioning has moved on to the **91.6 LOCOMO / 93.4 LongMemEval** "current algorithm" numbers in the GitHub README — these are the figures the paper's Mem0 row cites and are vendor-current as of 2026-05-05. The Mem0 paper (Chhikara 2025) reports 68.44 J for Mem0g; the GitHub README's 91.6/93.4 represents post-paper algorithmic improvement on a methodology Mem0 controls.

Net effect for the paper: the contestation described in `[^benchmark-disputes]` is real and correctly characterized, but the specific GitHub issue is no longer the live artifact. Suggested footnote tightening above keeps the substance and removes the freshness mistake.

## What is solid (do not re-litigate)

- Mem0 retrieval phrase is verbatim from the README.
- Mem0 memory-types are verbatim from the docs.
- Supermemory five components match the research page word-for-word.
- Supermemory benchmark scores match the research page word-for-word.
- Zep retrieval triple (semantic / BM25 / graph traversal) is verbatim across both Graphiti README and `help.getzep.com/searching-the-graph`.
- Zep memory-types triple is verbatim from the Graphiti README.
- Zep 71.2% / GPT-4o is verbatim from Rasmussen Table 2.
- Letta tool names verified in current source code.
- Letta 74.0% / GPT-4o-mini claim verified in the actual blog post (despite the dead URL slug).

## Sources fetched (2026-05-05)

- `docs.mem0.ai/core-concepts/memory-types` — Mem0 memory types
- `docs.mem0.ai/core-concepts/memory-operations` — Mem0 pipeline
- `github.com/mem0ai/mem0` — README
- `supermemory.ai/research` — five components and benchmarks
- `docs.letta.com/concepts/letta` — current architecture framing
- `docs.letta.com/guides/agents/memory-blocks` — memory blocks
- `github.com/letta-ai/letta` — README
- `github.com/letta-ai/letta/blob/main/letta/functions/function_sets/base.py` — tool names
- `letta.com/blog` — blog index
- `letta.com/blog/benchmarking-ai-agent-memory` — actual benchmark post
- `help.getzep.com/concepts` — Zep concepts
- `help.getzep.com/searching-the-graph` — retrieval methods
- `github.com/getzep/zep` — README
- `github.com/getzep/graphiti` — README (bi-temporal, Apache 2.0)
- `github.com/getzep/zep-papers/issues/5` — dispute thread (CLOSED)
- `docs/references/chhikara_2025_2504.19413_mem0.pdf` — Mem0 paper
- `docs/references/rasmussen_2025_2501.13956_zep.pdf` — Zep paper
