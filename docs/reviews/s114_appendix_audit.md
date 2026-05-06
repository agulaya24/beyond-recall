# S114 Appendix Audit — `beyond_recall_v9_draft.md`

**Date:** 2026-04-23
**Source:** `C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v9_draft.md` (1,742 lines)
**Scope:** every appendix reference in the paper body, mapped to current state and required action.
**Deliverable:** audit only. No edits made to v9 or v8.

---

## TL;DR

- **10 paper-appendix references total** (plus 1 reference to an in-doc "Part 7 appendix" inside an external research doc — not a paper-appendix reference).
- **v9 has no appendix content at all.** File ends at line 1740 (`---`) after §8.6 with "Paper body complete. Abstract to be written last." Everything pointing into an appendix is currently an orphan pointer.
- **v8 is identical on this dimension** — same references, no appendix body. This is a v8-inherited gap, not something v9 introduced.
- **No `appendix*.md` file exists anywhere in the study repo.** Supporting material lives scattered across `docs/research/`, `scripts/`, `docs/METHODOLOGY.md`, and `docs/DATA_REFERENCE.md`, but not in a citable appendix.
- **Highest-risk gap: Appendix D.** Three separate references, including a "full report in Appendix D" for an audit script whose markdown report does not exist.
- **Clean A–E layout is achievable** by assigning the two unspecified `the appendix` references to A and B.

### Summary table

| Action | Count | Notes |
|---|---:|---|
| `MATCHES` | 0 | No appendix exists to match against. |
| `NEEDS_SPECIFIC_POINTER` | 2 | Lines 293, 325 — "the appendix" with no letter. Assign to A and B. |
| `APPENDIX_MISSING` | 10 | All 10 paper references resolve to appendices that do not exist. |
| `APPENDIX_INCOMPLETE` | 0 | There is no appendix to be incomplete. |
| `CONTENT_LIVES_ELSEWHERE` | 0 | Source material for most appendices exists in research docs/scripts, but the paper cannot cite a reviewer's verification doc or a .py file as an appendix — the references must resolve to a published appendix section. See "Source material inventory" below for what can be lifted. |
| `NOT_A_PAPER_APPENDIX` | 1 | Line 1364 "Part 7 appendix" refers to Part 7 of `docs/research/letta_stateful_matched_rerun.md` (which exists). Confirmed, not a paper-appendix reference. |

Every paper-appendix reference in v9 is simultaneously `APPENDIX_MISSING`. The two unspecified ones additionally need a letter assignment.

---

## Reference inventory (by line number)

All quotes below are verbatim from v9. "Action" tags use the legend above.

### Ref 1 — Line 24 (§1 Introduction)

> "§2.3 positions each benchmark against what this paper measures, and **Appendix E** develops the scope differences in detail."

**Claim:** Appendix E contains a benchmark-by-benchmark analysis of scope differences between this paper's test and prior memory / personalization benchmarks (LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo).
**Current target:** `Appendix E`.
**Action:** `APPENDIX_MISSING`. Needs writing. Source material: §2.3 already has one-paragraph writeups per benchmark (lines 186–198); Appendix E should extend each into a full-scope analysis.

### Ref 2 — Line 188 (§2.3 Memory and personalization benchmarks)

> "Below, we position each existing benchmark against what this paper measures; an extended benchmark-by-benchmark analysis is in **Appendix E**."

**Claim:** Same as Ref 1.
**Current target:** `Appendix E`.
**Action:** `APPENDIX_MISSING`. This and Ref 1 are the same appendix promise.

### Ref 3 — Line 293 (§3.3 Pipeline)

> "The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: `avoids`, `repeatedly engages in`, `refuses to`, `values`, `fears`, `has experienced`). **The full predicate list is in the appendix.**"

**Claim:** Full list of the 46 extraction predicates.
**Current target:** unspecified ("the appendix").
**Action:** `NEEDS_SPECIFIC_POINTER` + `APPENDIX_MISSING`. Assign to **Appendix A**. Source material: full list is enumerated in `docs/research/section_3_3_pipeline_verification.md:78` (reviewer's verification doc, not citable as an appendix) and lives canonically in `memory_system/config.py` lines 612–638 (`CONSTRAINED_PREDICATES`). Must be lifted into Appendix A.

### Ref 4 — Line 325 (§3.4 Behavioral Prediction Battery)

> "Each main-study subject receives 39 behavioral prediction questions; Franklin's legacy battery has 40. The total behavioral-prediction pool is 586 questions across 15 subjects (14 main-study plus Franklin). Each battery covers 8 to 10 of the 10 fixed behavioral-prediction categories. **A per-subject count and category-distribution table is in the appendix.**"

**Claim:** Per-subject question count + question-category distribution table.
**Current target:** unspecified ("the appendix").
**Action:** `NEEDS_SPECIFIC_POINTER` + `APPENDIX_MISSING`. Assign to **Appendix B**. Source material: fully tabulated in `docs/research/question_category_audit.md` — aggregate distribution (LITERAL_RECALL 60, INTERPRETIVE_INFERENCE 403, REFUSAL_TRIGGERING 123), per-subject distribution table (15 subjects), and per-subject × category Δ_spec table. All three tables are appendix-ready; lift verbatim into Appendix B.

### Ref 5 — Line 380 (§3.5 Experimental Conditions)

> "Detailed per-condition parameters, exclusion cases, and ingestion specifics are in **Appendix C**."

**Claim:** Per-condition parameters (beyond the §3.5 table), exclusion cases (e.g., Babur C9 422K-word overflow), and ingestion specifics (how each memory system was configured).
**Current target:** `Appendix C`.
**Action:** `APPENDIX_MISSING`. Source material: scattered. §3.5 (lines 345–382) has the condition ID table but lacks ingestion specifics; memory-system configs are implicit in `scripts/run_global_subjects.py`, `scripts/run_memory_systems.py`, and `docs/PROVIDER_ISSUES.md`. Appendix C needs consolidation — not a simple copy-paste.

### Ref 6 — Line 408 (§3.6 Response Models)

> "Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in **Appendix C**. The same information is present in the released code at `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, and `scripts/run_multimodel_responses.py`."

**Claim:** Exact model identifiers (e.g., `claude-haiku-4-5-20251001`), full prompt text, and Tier 2 (Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects) invocation parameters.
**Current target:** `Appendix C`.
**Action:** `APPENDIX_MISSING`. Same appendix as Ref 5. Source material exists in the cited scripts and in `data/global_subjects/README.md`; needs lift-and-consolidate into Appendix C.

### Ref 7 — Line 428 (§3.7 Rubric)

> "*(Examples are illustrative; full per-subject score distributions with verbatim responses are in **Appendix D**.)*"

**Claim:** Full per-subject score distributions (all 14 main-study subjects across all conditions) + verbatim example responses at each anchor score.
**Current target:** `Appendix D`.
**Action:** `APPENDIX_MISSING`. **HIGH-RISK**. Source material: raw per-judge judgments at `results/global_<subject>/*_judgments_<judge>.json` plus merged `judgments_v2.json`. Distributions are computable (scripts exist) but no appendix-ready markdown or table has been produced. Requires rendering step.

### Ref 8 — Line 430 (§3.7 Rubric)

> "*(Condition identifiers such as C5, C2a, C4a, and C3 refer to the conditions defined in §3.5 and summarized in **Appendix C**. Rubric anchor numbers 1 through 5 refer to the rubric table above.)*"

**Claim:** Summary condition table in Appendix C (a lookup for readers encountering C5/C2a/C3/C4a throughout §4).
**Current target:** `Appendix C`.
**Action:** `APPENDIX_MISSING`. Same appendix as Refs 5 and 6. The §3.5 table already does most of this job; Appendix C just needs a 1-page summary card extracted from §3.5 and §3.7.

### Ref 9 — Line 543 (§3.7.x Rubric limitations)

> "A direct inspection of the response text against the 5-judge primary scores surfaced two rubric-handling limitations that any reader of the §4 numbers should keep in mind. Both were identified by a post-hoc audit (`scripts/audit_low_end_inflation.py`, **full report in Appendix D**)."

**Claim:** Full report of the rubric-handling audit — low-end score inflation analysis (abstention classification, length-score correlation, judge-leniency comparison, high-score validity).
**Current target:** `Appendix D`.
**Action:** `APPENDIX_MISSING`. **HIGHEST-RISK**. Source material: `scripts/audit_low_end_inflation.py` exists (verified, 30+ lines read) but **no published markdown report of its output exists anywhere in the repo**. Paper is asserting that a report exists. Either (a) run the script and write the report into Appendix D, or (b) soften the reference to "audit findings summarized in §3.7.x" if the full report is not going to ship. **This is a factual claim about the paper's own contents.**

### Ref 10 — Line 719 (§4.1 The Cross-Subject Gradient)

> "Per-subject anchor-crossing distributions (ranging from 25.6% on Babur to 74.4% on Sunity Devee) and per-subject per-judge score matrices are in **Appendix D**."

**Claim:** Per-subject anchor-crossing distributions (numbers already cited in §4.1 prose: 25.6% Babur, 74.4% Sunity Devee) + per-subject per-judge score matrices.
**Current target:** `Appendix D`.
**Action:** `APPENDIX_MISSING`. Source material: anchor-crossing data at `docs/research/s114_anchor_crossing_examples.json`, generated by `scripts/compute_anchor_crossing.py` (both cited in v9 line 513). Per-judge matrices derivable from `results/global_<subject>/*_judgments_<judge>.json`. Data exists; rendering step required.

### Ref 11 — Line 1364 (§4.4.x Letta stateful sensitivity)

> "The 7-judge sensitivity aggregate (Hamerton +0.20, Ebers +0.75, Babur +0.29; see `docs/research/letta_stateful_matched_rerun.md` **Part 7 appendix**) preserves direction on all three subjects."

**Claim:** Part 7 of the external research doc (not a paper appendix).
**Current target:** `docs/research/letta_stateful_matched_rerun.md` Part 7.
**Action:** `NOT_A_PAPER_APPENDIX` / `MATCHES` (external). Verified: `docs/research/letta_stateful_matched_rerun.md` line 277 has `## Part 7 — 5-judge primary panel (GPT-5.4 fix, post-rerun)`. The reference resolves correctly. **No action required.** One stylistic flag: the phrase "Part 7 appendix" is slightly confusing because it uses the word "appendix" loosely — consider rewording to "Part 7" or "Part 7 section" to avoid readers hunting for an Appendix in the paper. Optional.

---

## Source material inventory (what can be lifted into each appendix)

| Appendix | Paper claim | Source that exists | Source is appendix-ready? | Writing needed |
|---|---|---|---:|---|
| A (proposed) | 46 behavioral predicates, full list | `section_3_3_pipeline_verification.md:78` (one-line list); `memory_system/config.py:612-638` (canonical) | Partial (list is appendix-ready; grouping + brief definitions would help) | ~0.5 page: lift list, add one-line definition per predicate, note vocabulary provenance (50+ pilot subjects, frozen pre-study). |
| B (proposed) | Per-subject question count + category distribution table | `docs/research/question_category_audit.md` (3 ready tables) | Yes | ~1 page: lift three tables (aggregate distribution, per-subject distribution, per-subject × category Δ_spec). Already appendix-quality. |
| C | Per-condition parameters, exclusion cases, ingestion specifics, exact model IDs, prompt text, Tier 2 params, condition summary card | Scattered: §3.5 table (conditions), §3.6 (response models list), `scripts/run_global_subjects.py`, `scripts/run_full_study.py`, `scripts/run_multimodel_responses.py`, `docs/PROVIDER_ISSUES.md`, `data/global_subjects/README.md` | No — needs consolidation | ~3-5 pages: condition summary card, per-system ingestion configs (Mem0, Letta, Supermemory, Zep, Base Layer, both controlled and native variants), exclusion cases (Babur C9 overflow, Letta ingestion ceiling), Tier 2 invocation, prompt text. |
| D | Full per-subject score distributions with verbatim responses + rubric-handling audit report + per-subject anchor-crossing distributions + per-subject per-judge score matrices | Raw data: `results/global_<subject>/*_judgments_*.json`. Anchor-crossing: `docs/research/s114_anchor_crossing_examples.json` (data exists). Audit script: `scripts/audit_low_end_inflation.py` (**script only, no report**). | Data yes; markdown rendering no | ~5-10 pages: (a) run `audit_low_end_inflation.py` and write a prose report; (b) render per-subject distribution tables from JSON; (c) render per-subject per-judge score matrices; (d) select verbatim response examples at each rubric anchor for one representative subject (Hamerton already has them in §3.7 rubric). **BLOCKER until the audit report is written.** |
| E | Extended benchmark-by-benchmark scope analysis | §2.3 already has per-benchmark paragraphs (LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo). `docs/research/section_2_3_verification.md` has supporting verification notes. | Partial — existing prose is paragraph-length, appendix should go deeper | ~3-4 pages: for each benchmark, cover (i) task format, (ii) what the benchmark measures, (iii) what this paper measures, (iv) which claims transfer and which don't. Twin-2K deserves the longest treatment given it's closest to this paper's axis. |

---

## Prioritized to-do list for building the appendix

### P0 — BLOCKER (ship-gating)

1. **Write Appendix D's rubric-handling audit report.** Line 543 claims a "full report in Appendix D" that does not exist anywhere in the repo. Either:
   - Run `scripts/audit_low_end_inflation.py`, capture output, write a markdown report into Appendix D, OR
   - Soften the line 543 reference to point at §3.7.x findings only (removes the claim that a report exists).
   *This is a factual claim about the paper's own contents and is the single most dangerous current reference. Everything else is structural.*

### P1 — Pointer assignments (trivial, deterministic)

2. **Line 293**: change "in the appendix" → "in Appendix A".
3. **Line 325**: change "in the appendix" → "in Appendix B".
   *Pure edits once A and B exist.*

### P2 — Appendix writing (ordered by lift)

4. **Appendix B** (lightest lift, ~1 page). Copy three tables from `docs/research/question_category_audit.md` verbatim. Done.
5. **Appendix A** (~0.5–1 page). Lift predicate list from `section_3_3_pipeline_verification.md:78` or `config.py`; add brief annotations + frozen-vocabulary provenance note.
6. **Appendix E** (~3–4 pages). Extend the §2.3 per-benchmark paragraphs into fuller treatments. Paper already makes the central arguments; appendix fleshes out task format and scope for each benchmark. Twin-2K needs the most depth.
7. **Appendix C** (~3–5 pages). Consolidate scattered condition/model/ingestion material into one reference. Required for reproducibility. Script paths are already cited inline; appendix needs to replace "the same information is in the code" (line 408) with actual tables a reader can use without opening `scripts/`.
8. **Appendix D** (largest lift, ~5–10 pages). Render per-subject distributions, per-judge score matrices, anchor-crossing distributions, verbatim responses. Data all exists. This is a rendering task, not a research task — but it's the biggest writing job on the list.

### P3 — Stylistic (optional)

9. **Line 1364**: consider rewording "Part 7 appendix" → "Part 7" or "§Part 7" to avoid confusing readers looking for a paper-level appendix.

---

## High-risk references (flag summary)

| Line | Risk | Why |
|---:|---|---|
| 543 | **Highest** | Paper says "full report in Appendix D"; audit script exists but **no report has been written**. Shipping the paper with this line unchanged asserts something false about the paper's own contents. |
| 428, 719 | High | Both promise Appendix D content that does not exist. Source data exists, but rendering is unfinished. |
| 24, 188 | Medium | Appendix E promised twice; §2.3 has one-paragraph writeups that a reader might accept as sufficient, but the explicit "extended analysis" promise needs matching content or the line softened. |
| 380, 408, 430 | Medium | Three references into Appendix C; §3.5 and §3.6 carry most of the info in body text. Reader can piece it together, but a reference to a specific appendix that doesn't exist is weaker than no reference at all. |
| 293, 325 | Low-medium | Unspecified "the appendix" references. Low risk because they're factual pointers (predicate list, battery table) that a reader can verify against released data, but they still need specific resolution (Appendix A / B) once the appendix exists. |
| 1364 | None | External reference resolves correctly. |

---

## One-sentence bottom line

Ten paper-appendix references point into an appendix that does not exist in v9; the single most urgent fix is line 543's claim of a "full report in Appendix D" that has never been written, and the cleanest path forward is to assign the two unspecified references to A and B, write appendices A / B / C / D / E as scoped above, and soften or delete any claim the body makes about appendix content that will not actually ship.
