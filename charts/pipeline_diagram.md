# Pipeline Diagram Description

For generating a visual diagram of the Base Layer pipeline.

## Flow

```
+------------------+
|   SOURCE TEXT     |
|  (25,000+ words)  |
+--------+---------+
         |
         v
+------------------+     +-------------------------+
|   1. EXTRACT     |---->| 47 behavioral predicates |
|   (Haiku 4.5)    |     | Structured triples       |
|   temperature=0  |     | AUDN deduplication       |
+--------+---------+     | ~460 facts per subject   |
         |                +-------------------------+
         v
+------------------+     +-------------------------+
|   2. EMBED       |---->| MiniLM-L6-v2 vectors     |
|   (local model)  |     | Dedup + provenance        |
+--------+---------+     +-------------------------+
         |
         v
+------------------+     +-------------------------+
|   3. AUTHOR      |---->| ANCHORS: 8-10 axioms     |
|   (Sonnet 4.6)   |     | CORE: ~800 words         |
|   blind gen      |     | PREDICTIONS: 6-8 patterns |
+--------+---------+     +-------------------------+
         |
         v
+------------------+     +-------------------------+
|   4. COMPOSE     |---->| Unified specification     |
|   (Opus 4.6)     |     | ~5,000 tokens            |
|   quality gates  |     | Completeness + fidelity  |
+--------+---------+     +-------------------------+
         |
         v
+------------------+     +-------------------------+
|   5. SERVE       |---->| memory://identity        |
|   (MCP Server)   |     | Always-on resource       |
|   stdio transport|     | + recall/search/trace    |
+------------------+     +-------------------------+
```

## Compression Ratio

25,000 words source --> 462 facts --> 3 layers --> 5,000 token spec

## Key Labels for Diagram

- Source: "Autobiography, journals, chat logs, emails"
- Extract: "47 predicates force behavioral > biographical"
- Embed: "Vector dedup prevents redundancy"
- Author: "Three interpretive layers, blind generation"
- Compose: "Narrative reasoning framework, not summary"
- Serve: "Persistent context + on-demand retrieval"
