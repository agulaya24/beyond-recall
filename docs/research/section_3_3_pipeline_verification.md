# §3.3 Pipeline — Verification Against Source Code

Verification task for the "Beyond Recall" paper §3.3 "Pipeline" subsection. Every claim in the v6 draft's pipeline prose was cross-checked against primary source (code in `memory_system/src/baselayer/` and `CLAUDE.md`). Sources cited inline.

## 1. Step-by-Step Pipeline (Confirmed)

| Step | Script | Model | Output |
|---|---|---|---|
| 1. IMPORT | `import_conversations.py` | Local (no LLM) | SQLite records with source attribution |
| 2. EXTRACT | `extract_facts.py` | Claude Haiku (`claude-haiku-4-5-20251001`) or Ollama | Structured (subject, predicate, object) triples |
| 3. EMBED | `embed.py` | `all-MiniLM-L6-v2` | ChromaDB vectors |
| 4. AUTHOR | `author_layers.py` | Claude Sonnet (`claude-sonnet-4-6`) | Three layers: anchors, core, predictions |
| 5. COMPOSE | `agent_pipeline.py` | Claude Opus (`claude-opus-4-6`) | Unified behavioral specification (prose) |

### Step 1: IMPORT
- **Script:** `import_conversations.py` (verified at `memory_system/src/baselayer/import_conversations.py`)
- **Accepted inputs (verified from CLI args, lines 912-945):**
  - ChatGPT export (`--chatgpt`, `conversations.json`)
  - Claude web export (`--claude-web`, zip file)
  - Claude Code (`--claude-code`)
  - Plus text files and directories per CLAUDE.md
- **Output:** SQLite rows (conversations, messages tables)

### Step 2: EXTRACT
- **Script:** `extract_facts.py`
- **Backend:** Configurable via `BASELAYER_EXTRACTION_BACKEND`; default `"anthropic"` (config.py:115). Model: `claude-haiku-4-5-20251001` (config.py:116). Ollama path (local Qwen) still supported.
- **AUDN ops confirmed:** `extract_facts.py` line 4: *"Implements the AUDN (ADD/UPDATE/DELETE/NOOP) fact lifecycle from Mem0's approach."* `AUDN_SCHEMA` at line 620. Four operations: `ADD` / `UPDATE` / `DELETE` / `NOOP`.
- **Predicate vocabulary:** `CONSTRAINED_PREDICATES` in `config.py` lines 612-638 — see §7 below.
- **Structure:** Subject-predicate-object triples with provenance IDs, fact types (behavioral / biographical / positional / preference), commitment depth (factual / preference / position / conviction), and source message/chunk linkage.

### Step 3: EMBED
- **Script:** `embed.py`
- **Model identifier (EXACT):** `"all-MiniLM-L6-v2"` — confirmed at `config.py:98`:
  ```python
  EMBEDDING_MODEL = "all-MiniLM-L6-v2"
  ```
  The v6 §3.3 table currently lists **`MiniLM-L6-v2`** which is **wrong** — the sentence-transformers identifier requires the `all-` prefix. This is a real model-identifier error and should be corrected.
- **Vector store:** ChromaDB (confirmed — `VECTORS_DIR` at `config.py:84`, collection `"messages"` at line 305).
- **Distance metric:** L2 on normalized vectors; similarity computed as `1 - dist²/2` (config.py:323).

### Step 4: AUTHOR LAYERS
- **Script:** `author_layers.py`
- **Model:** `LAYER_GENERATION_MODEL = claude-sonnet-4-6` (config.py:458 + 501).
- **Three layers confirmed:**
  - **Anchors** — "Epistemic Axioms" (author_layers.py docstring lines 6-14; spec_production.md file begins `# ANCHORS`).
  - **Core** — operational constraints.
  - **Predictions** — testable behavioral patterns with false positive guards.
- **Blind regeneration:** CLAUDE.md DO NOT section confirms D-053: "Show prior layer output to Sonnet during regeneration. Causes 26% anchoring. Blind regen only."
- **Anonymization layer:** confirmed (author_layers.py lines 1185 and 1209 — anonymize facts, replace subject names with "this person").
- **Domain guard:** phrase is `DOMAIN-AGNOSTIC REQUIREMENT`, appears three times (author_layers.py lines 594, 629, 674) — once per layer prompt. The prompt: *"You are writing a UNIVERSAL operating guide — not a summary of interests or positions. Every item must apply ACROSS this person's life..."* This is a real, load-bearing prompt constraint.
- **H3 prompts:** No formal term "H3 prompts" exists in the code. This is CLAUDE.md shorthand for the fact that layer prompts use Markdown H3 (`###`) headers for section structure. **Recommendation: drop "H3 prompts" from §3.3 prose** — it adds no information and could confuse readers. "Domain guard" is worth keeping (with a one-line gloss) because it describes a real ablation-validated constraint.

### Step 5: COMPOSE
- **Script:** `agent_pipeline.py` — function `compose_unified_brief()` at line 577.
- **Model:** `LAYER_REVIEW_MODEL` = `claude-opus-4-6` (config.py:459 + 504). Comment at config.py:502: *"LAYER_REVIEW_MODEL is actively used as the compose model in agent_pipeline.py."*
- **Output:** Unified behavioral specification (flowing prose, ~5,000 tokens — confirmed by IDENTITY_TOKEN_BUDGET = 3500 + 1500 retrieved = 5000 TOTAL_TOKEN_BUDGET at config.py:129-132; paper says 5,000-8,000 which matches real-world range).
- **Gates:** `verify_brief_completeness` (line 217) and hallucination gate (line 285), with up to 2 retry iterations (line 728).

## 2. Embedding Model Identifier — CORRECTION REQUIRED

- **v6 §3.3 table line 449:** `MiniLM-L6-v2 (local)`
- **Actual model ID in config.py line 98:** `all-MiniLM-L6-v2`
- **Recommendation:** Change §3.3 and all other occurrences in the paper to `all-MiniLM-L6-v2`. This is the canonical sentence-transformers identifier; anything else will confuse replicators.

## 3. Predicate Count — DISCREPANCY

- **v6 §3.3 claim:** "47-predicate vocabulary" (appears on lines 249, 441, 464).
- **Actual count in `CONSTRAINED_PREDICATES` (config.py lines 612-638):** **46 predicates.**
- Counted by running `len(CONSTRAINED_PREDICATES)` on the list: 46.
- The comment at config.py:607 *also* says "47 verbs" — which is the source of the paper's number — but the list itself contains 46 entries. Either:
  - (a) One predicate was removed without updating the comment, or
  - (b) The count comment is off-by-one.
- **Resolution options:**
  1. Change paper to say **46** (match code).
  2. Check git history of config.py — possibly a predicate was dropped post-comment. If there is a missing predicate, restore it. Safer to just correct the paper: the comment is stale.
- **Recommendation:** Update paper to **46** (or more vaguely "~45 constrained predicates"). Also flag to Aarik that `config.py` comment is wrong and should be updated to match the list.

Full list of the 46: `owns, values, practices, studies, prefers, avoids, works_at, lives_in, married_to, raised_in, graduated_from, manages, builds, believes, fears, enjoys, dislikes, struggles_with, excels_at, identifies_as, maintains, follows, aspires_to, lost, founded, parents, experienced, learned, decided, prioritizes, unknown, attended, interested_in, wants_to, loves, hates, plays, monitors, relates_to, collaborates_with, mentored_by, raised_by, friends_with, reports_to, admires, conflicts_with`.

## 4. Cost Confirmation

- **v6 §3.3 claim:** "Under $1 per subject" for generating a new spec.
- **Table breakdown in v6 draft (line 447-451):**
  - IMPORT: $0
  - EXTRACT: $0.10-0.50 (Haiku)
  - EMBED: $0 (local)
  - AUTHOR: $0.05-0.15 (Sonnet)
  - COMPOSE: $0.05-0.15 (Opus)
  - **Sum: $0.20-0.80**
- This is consistent with "under $1". The paper also claims full-study reproduction is $500-700. No contradictions from source inspection. Approved.

## 5. Spec Variants — `spec.md` vs `spec_production.md`

Inspection of `memory-study-repo/data/global_subjects/augustine/` (and other subjects) shows two distinct files:

| File | Line count | Content | Anonymization |
|---|---|---|---|
| `spec.md` | ~28 lines (Augustine) | Opus-composed **unified brief** — single flowing prose document ("Augustine decides through..."). Named subject. | **Not** anonymized — subject named |
| `spec_production.md` | ~310 lines | Concatenated **three layers** with metadata headers: `# ANCHORS`, `# CORE`, `# PREDICTIONS`, each with injectable blocks. Uses "this person" throughout. | Anonymized (they/them, "this person") |

The `sync_to_study_repo.py` script only mentions `spec.md` (line 98); `spec_production.md` is produced upstream by the full pipeline (anchors + core + predictions blocks concatenated). Both files are generated by the pipeline; `spec_production.md` is the anonymized three-layer artifact used as the deployed specification context, while `spec.md` is the named human-readable brief.

**Which was used in the experiment?** This is the critical question. Based on the experiment condition definitions in the paper (C2a = "full behavioral specification", ~5,000 tokens) and Aarik's note in CLAUDE.md that "Table 4.4 (gradient) used brief-only specs. Must rerun with full-stack specs before publish", the paper now uses the **full-stack spec** (anchors + core + predictions + unified brief combined, ~5,000-7,500 tokens). This means **both files matter together** — the deployed context is the layers file (`spec_production.md`) plus the brief (`spec.md`), which corresponds to `IDENTITY_MODEL_FILE` in config.py:434: *"brief + layers combined — primary AI artifact"*.

**Recommendation for §3.3:** The current v6 §3.3 prose describes the pipeline as producing a **single** "Unified behavioral specification (~5,000 tokens)" at COMPOSE. The reality is that the deployed specification is the **brief + three layers concatenated** (which is what `identity_model.md` and the full-stack spec actually are). Two options:

1. **Single-spec framing (current draft, simpler):** Keep §3.3 describing one output artifact, call it "the specification", and note that it contains both the layer output and the composed brief. Defer the file-level structure to supplementary material. Cleaner for a reader who does not care about on-disk file names.
2. **Full-stack framing (more accurate):** State explicitly that the deployed specification consists of the three layers (anchors, core, predictions) plus the composed brief, concatenated to ~5,000-7,500 tokens. This matches CLAUDE.md D-081 ("brief + layers combined — primary AI artifact") and matches the condition definitions used in the experiment.

**Recommendation: Option 2.** The paper already says elsewhere (§3.4.1, line 513) that the "full-stack behavioral specification (anchors + core + predictions + unified brief, ~5,000-7,500 tokens)" is what was used. If §3.3 says the pipeline output is only the composed brief, it contradicts §3.4.1. Update §3.3 to say the deployed specification is the concatenation of the three authored layers and the composed brief. The file-level distinction (`spec.md` vs `spec_production.md`) can be a footnote or deferred to the released code repository — **not** worth putting in §3.3 prose.

## 6. Other Claims Checked

- **MCP serving** (paper line 474): confirmed. `mcp_server.py` exists; CLAUDE.md cites it with Identity Resource, recall/search/trace/verify tools.
- **Traceability chain** (paper line 472): `trace_claim` and `verify_claims` MCP tools confirmed in mcp_server.py.
- **Anti-contamination controls** (paper line 467-470): they/them pronouns, "this person" replacement, blind regen all confirmed in author_layers.py and config.py (D-040 AUTHORING_EXCLUSION_PATTERNS at config.py:546-580; anonymization calls at author_layers.py:1185, 1209).

## 7. Summary of Required Corrections to v6 §3.3

1. **`MiniLM-L6-v2` → `all-MiniLM-L6-v2`** (in Step 3 row of pipeline table, line 449). Canonical model identifier.
2. **"47-predicate" → "46-predicate"** throughout paper (or update `config.py` to restore the missing predicate). Count is verifiable; paper is currently off by one.
3. **Reframe §3.3 output artifact as the full stack** (layers + composed brief, ~5,000-7,500 tokens), not just the composed brief. Aligns §3.3 with §3.4.1 and with what was actually deployed.
4. **Drop "H3 prompts"** from §3.3 if it appears in draft prose (it is CLAUDE.md shorthand, not a real thing).
5. **Keep "domain guard" but gloss it**: a one-line note that every layer prompt carries a DOMAIN-AGNOSTIC REQUIREMENT constraint preventing the generator from summarizing topical interests rather than describing reasoning patterns. This is load-bearing (S99 ablation showed it eliminates topic skew).

## 8. Sources Consulted (absolute paths)

- `C:\Users\Aarik\Anthropic\CLAUDE.md` — Pipeline (5 Steps), Key Technical Facts
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\config.py` — EMBEDDING_MODEL (l.98), EXTRACTION_API_MODEL (l.116), LAYER_GENERATION_MODEL / LAYER_REVIEW_MODEL (l.501-504), CONSTRAINED_PREDICATES (l.612-638), IDENTITY_MODEL_FILE (l.434)
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\extract_facts.py` — AUDN docstring (l.4), AUDN_SCHEMA (l.620), predicate usage
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\embed.py` — imports EMBEDDING_MODEL
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\author_layers.py` — three-layer structure (docstring), DOMAIN-AGNOSTIC REQUIREMENT (l.594, 629, 674), anonymization (l.1185, 1209)
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\agent_pipeline.py` — `compose_unified_brief()` (l.577), gates (l.217, 285)
- `C:\Users\Aarik\Anthropic\memory_system\src\baselayer\import_conversations.py` — CLI args (l.907-945)
- `C:\Users\Aarik\Anthropic\memory-study-repo\data\global_subjects\augustine\spec.md` and `spec_production.md` — spec-variant structure
- `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v6_draft.md` — §3.3 (l.439-476), §3.4.1 (l.513)
