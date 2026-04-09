# Memory Systems Study — Provider Issues Log

Issues encountered during the study, documented for reproducibility and as feedback for each provider.

---

## Mem0 (mem0ai 1.0.11)

### Issues
1. **SDK init hang.** `from mem0 import MemoryClient` hangs indefinitely after ~50 queries. Root cause: urllib3 2.3.0 / chardet 7.1.0 version mismatch triggers a blocking import cycle.
   - **Workaround:** Raw HTTP via `requests.post("https://api.mem0.ai/v1/memories/search/", ...)` — bypasses SDK entirely.
   - **Impact:** First 55 questions used SDK, remaining 25 used raw HTTP. Results identical.

2. **`filters` parameter format.** Early SDK version expected `filters={"user_id": ...}` but API sometimes returned empty results. Switching to raw HTTP with the same JSON body worked consistently.

3. **No bulk text ingestion.** `client.add()` accepts one memory at a time. For 1,133 Franklin facts: 1,133 sequential API calls. Slow (~15-20 minutes).
   - **Suggestion:** Batch ingestion endpoint or document upload.

### What Worked Well
- Search API is fast and reliable via raw HTTP (~300ms per query)
- Retrieval quality was consistent (10 facts per query, good relevance)
- Mem0 was the most reliable system across the entire study

---

## Letta / MemGPT (letta-client 1.10.2)

### Issues
1. **SDK init hang (same as Mem0).** `from letta_client import Letta` followed by `client.agents.list()` hangs after sustained use. Same urllib3/chardet root cause.
   - **Workaround:** Standalone runner script with fresh process per session.
   - **Impact:** Letta ran as standalone, results merged with main dataset.

2. **Free tier: 3 agent limit.** Cannot create more than 3 agents. Franklin study required a new agent — had to verify existing agents wouldn't be overwritten.
   - **Suggestion:** Allow more agents on free tier, or agent archiving.

3. **`agents.list()` hangs under sustained load.** After ~50 list operations, the SDK stops responding.
   - **Workaround:** Kill process, restart, resume from checkpoint.

### What Worked Well
- Passage-based ingestion is well-suited for document text
- Retrieval via `agents.passages.search()` returned good results
- Letta consistently ranked highest in C3 (spec + facts) condition

---

## Supermemory (supermemory 3.32.0)

### Issues
1. **Franklin facts never indexed.** Ingested 1,133 facts with `memories.create()` — API returned success (200/201) — but search returned 0 results for all 80 questions. Container tag `franklin_study_v1` appears empty despite successful ingestion.
   - **Hamerton facts (462) work fine** with container tag `hamerton_v2`.
   - **Possible cause:** Custom ID deduplication silently skipping, or indexing delay exceeding query time.
   - **Impact:** C1_supermemory and C3_supermemory have no data for Franklin.

2. **Endpoint confusion.** SDK uses `client.memories.create()` but raw HTTP endpoint is `POST /v3/memories` (not `/v3/add` as some docs suggest). The `/v3/add` endpoint returns 404.
   - **Confirmed working:** `POST https://api.supermemory.ai/v3/memories` with `{"content": "...", "containerTags": ["..."]}`.

3. **500 errors during C8 raw corpus ingestion.** Hamerton raw text chunked into 74 pieces (~2K chars each). First chunks returned 500, then 401 ("Unauthorized"). Possibly rate limiting or API instability.
   - **Workaround:** Slower rate (0.5s between calls) appears to help.

4. **Search endpoint format.** Search is `POST /v3/search` with `{"q": "...", "containerTags": ["..."]}` (camelCase array, not `container_tag` singular). Inconsistent naming between create and search.

5. **308 Permanent Redirect on POST.** `POST /v3/memories` returns 308 redirect. The Python `httpx` library does NOT follow redirects on POST by default — must pass `follow_redirects=True`. The `requests` library follows redirects by default but has the urllib3 hang issue. This caused ALL httpx-based Supermemory calls to silently fail (308 treated as error). **Root cause of Franklin shared-facts ingestion failure.**
   - **Fix:** Always use `follow_redirects=True` with httpx for Supermemory.
   - **Suggestion to Supermemory:** Either don't redirect on POST, or document the redirect requirement prominently.

### What Worked Well
- Hamerton data (462 facts) indexed and retrieved correctly
- Search quality was comparable to Mem0 when data was present
- API response times were fast (~250ms)

---

## Zep (zep-cloud 3.20.0)

### Issues
1. **`user_id` mismatch.** `list_ordered()` returns named tuples, not User objects. Extracting `user_id` required `hasattr` checks. Initial runs failed silently with wrong user IDs.
   - **Workaround:** Standalone runner with explicit user_id handling.

2. **Graph traversal bias.** Zep's knowledge graph retrieves the same high-connectivity node for unrelated queries. The father-property-settlement fact appeared for 39% of all Hamerton questions — regardless of query topic.
   - **Impact:** Zep consistently scored lowest (C1_zep: 1.64). This appears to be a structural issue with graph-based retrieval for behavioral queries.

3. **10,000 character limit per `graph.add()`.** Documentation recommends 500-char chunks with 50-char overlap for optimal graph construction. Raw corpus (142K-241K chars) requires 280-480+ API calls.
   - **Impact:** C8 ingestion is slow for Zep.

4. **SDK dependency conflict.** `zep-python` (self-hosted) vs `zep-cloud` (cloud) are different packages with different APIs. Initial attempt used wrong package — all endpoints returned 404.

### What Worked Well
- Knowledge graph extraction produces interesting entity-relationship structures
- Once properly configured, search is fast
- `graph.add(type="text")` accepts multi-line text, handles its own extraction

---

## General Issues (All Providers)

1. **urllib3 / chardet version mismatch** affects ALL Python SDK-based providers. The `requests` library warns, then SDK init operations hang. Raw HTTP via `requests` or `httpx` bypasses the issue entirely.

2. **No standardized document ingestion.** Each system has a different approach:
   - Mem0: one fact at a time
   - Letta: passages (medium chunks)
   - Supermemory: memories (individual)
   - Zep: graph.add with text (chunked)
   
   None offer a "here's a document, process it" endpoint that handles chunking internally (Supermemory has `/v3/documents/file` but it was not tested in this study).

3. **Rate limiting is undocumented.** Supermemory returned 500s that may be rate limits. Zep recommends 1s between calls. Mem0 appears unlimited. Letta has no published rate limits.

4. **Container/user namespace management.** Creating study-specific namespaces (user_ids, container_tags, agent names) requires manual setup per system. No standard API for "create an isolated environment for this experiment."

---

## Recommendations for Providers

1. **Publish rate limits explicitly.** Undocumented limits cause study failures.
2. **Offer bulk document ingestion.** One endpoint, one document, system handles chunking.
3. **Standardize namespace management.** API for creating/listing/deleting isolated environments.
4. **Fix SDK dependency conflicts.** Pin urllib3/chardet versions or use httpx internally.
5. **Verify ingestion completion.** Return a "ready" signal — don't return 200 on create if the data isn't searchable yet.
