# Beyond Recall Study MCP Server (MVP)

An MCP server that exposes the Beyond Recall study's data and indexes as
agent-callable tools and resources. Lets any MCP client (Claude Desktop,
Claude Code, custom clients) interrogate the study without grepping files
manually.

## What this exposes

### Tools
- **search_study(query, mode, limit)** wraps the existing FTS + ChromaDB index
  at `workspace/study_knowledge.db` and `workspace/study_vectors/`.
- **get_subject_score(subject, condition, panel)** recomputes the per-judge
  mean score for any (subject, condition, panel) cell directly from the raw
  judgment files. Honors the locked aggregation rule (paper §3.6.5).
- **list_subjects()** returns the 14 main-study subjects with C5 baseline,
  C4a (facts+spec), Δ_spec, low-baseline flag, and on-disk paths.
- **get_provenance(claim)** searches PROVENANCE_INDEX.md and
  DATA_REFERENCE.md for sections matching a claim.
- **list_anchor_crossings(condition_pair, min_jump)** returns per-question
  multi-anchor jumps for any of 8 condition pairs, enriched with held-out
  passage text for C5_to_C4a.

### Resources
- **paper://index** Markdown index of every paper section.
- **paper://section/{id}** text of paper section `{id}` (e.g. `3.6.2`,
  `4.1`, `4.4.4`). Source: `docs/beyond_recall_v11_8_draft.md`.

## Install

```bash
pip install 'mcp[cli]'
# Plus the existing study repo requirements:
pip install -r ../requirements.txt
```

The server reads (read-only) from:
- `workspace/study_knowledge.db` (SQLite + FTS5)
- `workspace/study_vectors/` (ChromaDB collection `study`)
- `results/<subject_dir>/judgments*.json`
- `docs/beyond_recall_v11_8_draft.md`
- `docs/research/multi_anchor_rates_all_pairs_20260430.json`
- `docs/research/s114_anchor_crossing_examples.json`

If the index is stale or missing, refresh it with:

```bash
python ../scripts/index_study_repo.py
```

## Run

```bash
python server.py
```

The server speaks JSON-RPC over stdio. Logs go to stderr.

## Register with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "memory-study": {
      "command": "python",
      "args": ["C:/Users/Aarik/Anthropic/memory-study-repo/mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. The server's tools and resources will appear in the
MCP picker.

## Register with Claude Code

```bash
claude mcp add --transport stdio memory-study -- python C:/Users/Aarik/Anthropic/memory-study-repo/mcp/server.py
```

Or add to the `mcpServers` section of `~/.claude.json` directly using the
same JSON block as above.

## Tool reference

### search_study

```python
search_study(query="Wilcoxon gradient", mode="both", limit=10)
```

Returns up to `limit` results from FTS, plus up to `limit` from semantic
search when `mode="both"`. Each row carries the chunk's `file_path`,
`scope` ("paper", "results_judgments", etc.), `label` (section heading or
JSON key), and a 400-char `content_preview`. FTS rows include an
`rank`-derived score; semantic rows include the cosine distance.

### get_subject_score

```python
get_subject_score(subject="seacole", condition="C4a", panel="5-judge-primary")
# {'mean': 2.595, 'n_questions': 39, 'per_judge': {...}, ...}
```

Accepts both short subject names ("seacole") and directory names
("global_seacole", "hamerton"). Conditions can be short ("C4a") or full
("C4a_full_facts_plus_spec"). The aggregation is the locked rule: per-judge
per-question scores averaged within judge, then averaged across the panel.

Returns mean, `n_questions`, `per_judge` breakdown (each judge's mean and
n), the `condition_variant_used` (so you can see which form the data is
stored under), and the `aggregation_rule` for traceability.

### list_subjects

```python
list_subjects()
# [{'subject': 'ebers', 'c5_baseline': 1.02, 'c4a_facts_plus_spec': 2.07, ...}, ...]
```

Returns the 14 main-study subjects in C5-ascending order. Source values are
the v10.1 5-judge primary canonical numbers, hardcoded from
`DATA_REFERENCE.md` §1 because the table changes ~once per release.

### get_provenance

```python
get_provenance(claim="Wilcoxon p value gradient", limit=8)
```

Semantic search across the index, post-filtered to
`PROVENANCE_INDEX.md` and `DATA_REFERENCE.md`, with FTS as fallback /
supplement. Returns `{filename, file_path, section_label, content_preview}`
rows.

### list_anchor_crossings

```python
list_anchor_crossings(condition_pair="C5_to_C4a", min_jump=2, limit=25)
```

Reads from `docs/research/multi_anchor_rates_all_pairs_20260430.json`
(8 pairs), filters per-question crossings by minimum jump magnitude. For
`C5_to_C4a`, enriches rows with question text and held-out passages from
`s114_anchor_crossing_examples.json` where qids match.

Available pairs: `C5_to_C4a`, `C5_to_C4`, `C5_to_C2a`, `C2c_to_C2a`,
`C4_to_C4a`, `C5_to_C8`, `C5_to_C9`, `C8_to_C9`.

## Resource reference

### paper://index

Returns a Markdown bullet list of every paper section with its
`paper://section/<id>` URI and title.

### paper://section/{id}

Returns the text of a paper section. The `id` is the leading numeric token
of the heading (e.g. `3.6.2`, `4.4.4`, `1.2`). Headings without a numeric
prefix fall back to a slug derived from the title; call `paper://index`
to see the full inventory.

## Smoke tests

```bash
python test_smoke.py
```

Runs each tool function directly against the on-disk study data without
going through the MCP wire protocol. Exits non-zero on failure.

## Files

- `server.py` -- FastMCP server, thin wrapper around tools.py
- `tools.py` -- pure typed Python tool functions (no MCP imports)
- `resources.py` -- paper section resource helpers
- `test_smoke.py` -- direct smoke tests for the tool functions
- `README.md` -- this file

## Known data-shape quirks the server handles

- Globals ship a single long-format `judgments_v2.json` with all judges in
  one file (`{qid, condition, judge, score}` rows).
- Hamerton ships per-judge files in mixed long/wide formats:
  `judgments.json` is wide with `haiku_score` + `gemini_score` columns,
  `gpt54_judgments.json` is wide with `gpt54_score`, and Sonnet / Opus /
  GPT-4o files are long format. Hamerton's C5 baseline rows live in
  `judgments_harmonized.json`.
- Condition strings drift across subjects: globals use
  `C2c_wrong_spec` / `C4a_full_facts_plus_spec`; Hamerton uses
  `C2c_full_wrong_spec` / `C4a_full_all_facts_plus_spec`. The
  `_normalize_condition` + `CONDITION_VARIANTS` table handles both.
