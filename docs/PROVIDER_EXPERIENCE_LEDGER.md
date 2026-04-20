# Provider Experience Ledger — Memory Systems Expansion (2026-04-15)

Running all 4 memory systems x 14 subjects simultaneously. Real-time notes on what each platform is like to work with.

## Supermemory

**Tier:** Free (1M tokens, 10K searches)
**API style:** REST, clean endpoints

### Positives
- **Generous free tier.** 1M tokens and 10K searches is enough for a serious research run (14 subjects, ~24K facts). No credit card needed. This is remarkable.
- **Simple, clean API.** POST `/v3/documents` for ingest, POST `/v3/search` for retrieval. Straightforward JSON. No SDK dependency required.
- **Custom ID support for deduplication.** `customId` field means we can safely retry failures without creating duplicate entries.
- **Container tags** are an elegant namespace mechanism. Easy to isolate subjects by tag.
- **Fast status feedback.** Returns `"status":"done"` or `"status":"queued"` — tells you immediately whether indexing happened synchronously or was deferred.

### Negatives
- **308 redirect on POST.** Must use `follow_redirects=True` with httpx. If you don't know this, all your ingestion silently fails. Not documented prominently.
- **Async indexing uncertainty.** Some documents index immediately ("done"), others queue ("queued"). Search returns empty for queued documents — you need to poll. The delay varies from seconds to minutes.
- **Slow throughput.** ~2-3 seconds per document including network round-trip + rate limiting. For 24K facts, that's ~16 hours. The free tier may have lower priority.
- **Search result format is nested.** Results contain `chunks` arrays, where the actual content is buried in `chunks[0].content`. Not intuitive.

### Notes for Supermemory team
The free tier generosity is a genuine differentiator — it's the only system that let us run this full study without a paid subscription. The 308 redirect is a silent killer though — it probably causes a lot of "why aren't my documents indexed?" support tickets.

---

## Mem0

**Tier:** Starter ($19/mo)
**API style:** REST, two API versions (v1 ingest, v2 search)

### Positives
- **`infer=False` parameter.** Lets us store facts verbatim without LLM reformulation. Critical for controlled experiments. Verified: sent fact, got back identical fact. Excellent.
- **Fast ingestion.** 1000 req/min rate limit, but actual throughput is ~5-10 facts/sec. Fastest of all 4 systems.
- **Immediate availability.** Facts are searchable within seconds of ingestion. No async lag.
- **v2 search endpoint** is more capable than v1. Supports filters, top_k, semantic search.

### Negatives
- **SDK hangs (urllib3/chardet).** The official Python SDK becomes unresponsive after ~50 calls due to a connection pool issue. Must use raw HTTP instead. This is a known issue since at least early 2026.
- **API version split.** Ingestion is v1, search is v2. Not obvious which to use without reading docs carefully. v1 search still works but is deprecated.
- **No bulk ingestion endpoint.** Must POST facts one at a time. Not a problem at 1000/min, but wasteful for large datasets.
- **Response format inconsistency.** v2 search returns a flat list; some endpoints return `{"results": [...]}` vs `{"memories": [...]}`. Need defensive parsing.

### Notes for Mem0 team
The `infer=False` parameter is a thoughtful addition — it shows awareness that not everyone wants the LLM reformulation. Fix the SDK hang (it's been months) and add a bulk ingestion endpoint and this becomes the easiest platform to integrate with.

---

## Letta

**Tier:** Pro ($20/mo)
**API style:** REST, agent-oriented

### Positives
- **Clean agent lifecycle.** Create → ingest → search → delete. Each agent is an isolated namespace.
- **Archival memory search** returns well-structured results with timestamps and IDs.
- **Pro tier agent limit (20)** is enough for our 14 subjects with room to spare.

### Negatives
- **Endpoint confusion.** Three possible search endpoints: `/passages/search` (404), `/archival-memory/search` (works), and agent message-based retrieval. Documentation doesn't clearly distinguish between them. We had to test all three to find the working one.
- **`/passages` endpoint doesn't exist** despite appearing in what seems like official documentation. The working endpoint is `/archival-memory` for both ingest and search.
- **Agent creation overhead.** Each subject needs a new agent (with its own model config), which means 14 agent creations before any ingestion starts. Not slow, but adds complexity.
- **SDK hangs under load.** Same urllib3 issue as Mem0. Raw HTTP is the only reliable option for sustained throughput.
- **Field name discrepancy.** Ingestion uses `{"text": "..."}` (not `{"content": "..."}`), which is a 422 error if you guess wrong.

### Notes for Letta team
The agent paradigm is powerful but the API surface area is confusing. Multiple endpoint versions, deprecated routes that still appear in docs, and inconsistent field names between endpoints. A clear "here's the one endpoint for X" guide would save every integrator significant debugging time.

---

## Zep

**Tier:** Flex ($25/mo)
**API style:** SDK-first (zep-cloud Python package)

### Positives
- **Knowledge graph approach** is genuinely different from the others. Facts become graph nodes with relationships, enabling structured reasoning.
- **Batch-friendly.** `graph.add()` accepts concatenated text, so we can batch 20 facts into one call.
- **Credit system with auto-top-up** prevents mid-run failures. If credits run low, they auto-replenish.
- **User model** with `first_name` is a nice touch — contextualizes the graph.

### Negatives
- **Slow by design.** 15-second mandatory wait between batches for graph processing. This is not a rate limit — it's how long the graph needs to process. For 24K facts in batches of 20, that's ~300 minutes of waiting alone.
- **Graph traversal bias.** Known issue from Hamerton run: high-connectivity nodes dominate retrieval regardless of query topic. The single most-common Zep top-1 fact appears in ~11% of Hamerton questions; father-related facts (any fact mentioning "father") appear in ~54% of questions. Earlier drafts cited a "39% same-fact" figure that could not be reproduced from the source data and has been corrected (see `PAPER_CORRECTIONS.md` #10). The structural pattern — graph hubs creating retrieval hotspots — is the replicable finding.
- **10K character limit per `graph.add()`.** Must pre-chunk large inputs. The system doesn't do this for you.
- **Credit consumption is unpredictable.** 1 credit per episode base, 2 for episodes >350 bytes. Hard to estimate total cost before running.
- **SDK-only approach.** No simple REST API for basic operations. Must install `zep-cloud` package and use Python SDK. Some operations (like listing users) don't have SDK methods.

### Notes for Zep team
The graph approach is the most intellectually interesting of the four — it's the only system that tries to understand relationships between facts rather than just storing and retrieving them. But the 15s processing wait and graph traversal bias limit its practical throughput and retrieval quality. Consider offering a "fast mode" that skips graph processing for batch ingestion scenarios.

---

## Comparative Summary (will update as run progresses)

| Dimension | Mem0 | Letta | Supermemory | Zep |
|---|---|---|---|---|
| **Setup difficulty** | Easy | Medium | Easy | Medium |
| **Ingestion speed** | Fast (~5-10/sec) | Medium (~1-2/sec) | Slow (~0.4/sec) | Slow (batch + 15s waits) |
| **Search reliability** | High | High | Medium (async lag) | Medium (graph bias) |
| **Free tier** | No | No | Yes (generous) | No |
| **SDK quality** | Broken (use HTTP) | Broken (use HTTP) | N/A (REST only) | Functional but incomplete |
| **Documentation** | Good | Confusing | Adequate | Good |
| **Unique strength** | Speed + infer=False | Agent isolation | Free tier | Knowledge graph |
| **Biggest weakness** | SDK hang | Endpoint confusion | Slow throughput | Graph bias + slow processing |
