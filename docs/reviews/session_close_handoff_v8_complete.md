# Session-Close Handoff: v8 Draft Complete Through §8

**Last updated:** 2026-04-23 (session close after extended optimization run)
**Status:** Paper body complete §1-§8. Word doc regenerated. All gate-review consensus fixes applied. BaseLayer main-repo optimization (README + canonicality + provenance + methodology + package-surface) applied. Figure correctness pass applied (14 PNGs regenerated; 2 label-collision fixes in flight as of session close). Abstract intentionally deferred to next-session, post-author-read-through.
**Next session:** likely a new Claude instance. Read **this section** first, then jump to specific sections as needed.

---

## Start here (new instance, 2026-04-23)

**The paper lives at:** `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v8_draft.md` (~1700 lines, §1-§8 complete, abstract pending).
**The Word doc for author review is at:** `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v8_draft.docx` (1.8 MB, 11 figures embedded, TOC, 32 tables).
**The main BaseLayer repo lives at:** `C:\Users\Aarik\Anthropic\memory_system\` (tech-debt tracker at `memory_system/TECH_DEBT.md`).

### First actions

1. Read this file top-to-bottom (skim the canonical numbers reference; read the consolidated todo list section in full).
2. Ask the author what they want to tackle first. Likely options: (a) apply their own read-through feedback, (b) apply items from the consolidated todo list, (c) write the abstract.
3. Do NOT start new scope-creep items from §8 Future Work. That's the post-publication research agenda.

### Consolidated todo list (what remains open)

Compiled from: gate-review synthesis, hygiene audit, completeness audit, figure review, methodology doc, BaseLayer tech debt.

**Paper (memory-study-repo):**
- Author's own read-through feedback (scheduled for 2026-04-23)
- Abstract (write last, after all edits settle)
- Gate-review items NOT applied this session (judgment calls deferred to author):
  - §3.1 / §3.4 Haiku vs Sonnet battery-generator ambiguity (Anthropic flagged; pick one and verify against scripts)
  - Token-count reconciliation 5-8K vs 8-10K (partially addressed in §1.3 compression headline)
  - §7 transition sentence from §6 (one-sentence fix; Anthropic noted §7 feels orphaned)
  - §4.1.2 Franklin wrong-spec overlap emphasis (Mistral; current wording defensible)
  - §4.4 Supermemory one-line summary polish (Mistral; paragraph body already documents mixture)
- ~~Fig2 + fig_4_1 label-collision fix~~ ✓ RESOLVED 2026-04-23. Both now CLEAN on vision spot-check. Word doc regenerated (now 2.15 MB). All 14 figures publication-ready on layout.

**Paper-support hygiene (memory-study-repo):**
- `figures/fig1_*` through `fig11_*` (v6-era scripts now regenerated with v8 palette/typography but with the v6-era filename scheme) vs v8-era `fig_4_1`/`fig_4_2`/`fig_4_2_1` — decide whether to archive the v6-scheme names or keep both
- ~45 scripts are archive candidates (review_paper_round2*, _probe_*, one-off scans); retain `_verify_battery_leakage.py` (load-bearing)
- One `.aux` LaTeX file blocked by sandbox during hygiene audit — one-line manual `mv` clears it
- Two ambiguous `s114_*` files at `docs/reviews/` top level — keep as current or archive
- PROVENANCE_INDEX §-number remap v6 → v8 across existing rows (~1 hour, row-by-row)
- DATA_REFERENCE §4 legacy 7-judge → 5-judge primary number sync (Base Layer +0.13 should be +0.08; other systems similar)

**Paper-support completeness gaps (memory-study-repo):**
- `results/interjudge_agreement/` cited but directory doesn't exist — persist or remove the citation
- `docs/research/_content_analysis_results.json` cited in §4.7; numbers exist only in paper prose — persist as artifact
- `scripts/compute_question_improvement_rate.py` cited in §4.2 and `KEY_FINDINGS.md` M11 — create or remove citation

**Methodology doc gap (memory_system):**
- Exact judge-prompt version for the 10 README scores (rubric reconstructed from D079_RUBRIC_CALIBRATION + BRIEF_ABLATION_REVIEW, but the specific Opus judge prompt is not archived as a single artifact)

**BaseLayer mechanical hygiene (memory_system — minutes each):**
- `src/__init__.py` empty — delete
- `baselayer.egg-info/` — add to `.gitignore`
- `src_backup_s101/`, `scripts_backup_s101/`, `backups/` at repo root — archive or delete
- Duplicate `detect_contradictions.py` (active vs `archive/utilities/`) — diff and consolidate
- README number audit (57+ subjects, 93 decisions, 112 sessions badges/counts may be stale)

**BaseLayer medium hygiene (memory_system — ~1 hour each):**
- `cmd_run` runner split embed into explicit Step 3/5 (currently bundled in post-compose traceability phase; only prose was reconciled this session, not the orchestration)
- DATA_REFERENCE §4 5-judge primary update (covers both repos since it's in memory-study-repo)

**BaseLayer engineering debt (memory_system — P1 in TECH_DEBT, defer past launch):**
- CLI `sys.argv` → typed internal service-layer refactor
- Config + state globals reduction (config.py + api_client.py singletons)
- Markdown-contract → structured-data (schema) migration for layer/brief
- Provenance verifier threshold calibration (C13 empirical)
- Test suite broad-guardrail → deep-invariant hardening

**Research direction (TECH_DEBT P3 — GitHub issues; not blocking any review):**
- Temporal trajectory/drift model
- Component ablation
- Dynamic activation policy
- Differentiated rubric + multi-dimensional scoring

### Canonical file map

| What | Where |
|---|---|
| Paper draft (markdown) | `memory-study-repo/docs/beyond_recall_v8_draft.md` |
| Paper draft (Word, for author review) | `memory-study-repo/docs/beyond_recall_v8_draft.docx` |
| Handoff doc (this file) | `memory-study-repo/docs/reviews/session_close_handoff_v8_complete.md` |
| Canonical numbers reference | below in this file, §"Canonical numbers reference" |
| Voice rules | below in this file, §"Voice rules" |
| Gate review synthesis | `memory-study-repo/docs/reviews/gate_review_synthesis_20260422_173703.md` |
| Figure review (first round) | `memory-study-repo/docs/reviews/figure_review_20260422.md` |
| Figure fixes log | `memory-study-repo/docs/reviews/figure_fixes_20260422.md` |
| Figure layout spot-check | `memory-study-repo/docs/reviews/figure_layout_spotcheck_20260423.md` |
| Hygiene audit | `memory-study-repo/docs/reviews/repo_hygiene_audit_20260422_182500.md` |
| Completeness audit | `memory-study-repo/docs/reviews/repo_completeness_audit_20260422_173831.md` |
| BaseLayer tech debt | `memory_system/TECH_DEBT.md` |
| BaseLayer README rewrite log | `memory_system/docs/reviews/readme_rewrite_20260422.md` |
| Methodology doc (BaseLayer) | `memory_system/docs/eval/methodology.md` |
| Study memory (persistent) | `memory-study-repo/agents/STUDY_MEMORY.md` |

---

## TL;DR

The "Beyond Recall" paper draft at `docs/beyond_recall_v8_draft.md` is now complete through §8 Future Work. Major content work done this session:

- **§4.3 through §4.8** drafted and revised
- **§5.1 through §5.6** Discussion drafted with author feedback applied
- **§6.1 through §6.4** Limitations drafted (scoped to avoid double-claiming with §5)
- **§7 Behavioral alignment and safety alignment** drafted as short standalone section
- **§8 Future Work** drafted as consolidated research agenda (6 thematic subsections)
- **Multiple surgical voice / jargon / reference passes** applied across §1-§5 per Haiku GTM scan feedback
- **GPT-5.4 HTTP 400 bug fixed** on Letta stateful judging (it was `max_tokens` vs `max_completion_tokens`, not context size); 5-judge primary numbers now canonical in §4.7
- **Wrong-spec labeling correction** applied across §1.3, §4.1.2, §1.2 condition table, and 9 support docs (v1 was fixed derangement, not Franklin-for-all — that mislabel lived throughout)
- **Four new content additions** per author direction: Letta content analysis subsection (§4.7), §4.8 rough-implementation caveat + dynamic activation + modifiability + temporality + topic decomposition + piecewise, local-vs-cloud distinction (§4.4 + §4.8), canonical life events (§5.2)
- **§4.6 collective review applied** (3+ provider consensus: Keckley Q21 "cleanest" softened, table surgery, voice cleanup, mechanism quantification gap flagged)

---

## What's still outstanding for next session

Priority ordered.

### 1. Review collective gate review results (COMPLETED AND CONSENSUS FIXES APPLIED THIS SESSION)

Full-paper gate review completed across Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, GPT-5.4, and Claude Opus 4.6. **All 5 providers converged: READY FOR PUBLICATION AFTER TARGETED FIX PASS.** No provider asked for rewrites, new experiments, or structural overhaul.

Synthesis: `docs/reviews/gate_review_synthesis_20260422_173703.md`. Raw reviews: `docs/reviews/full_paper_gate_review_20260422_173703.md`.

**8 consensus fixes applied this session after the gate review completed:**

1. §1.2 reference error `§4.3.1` → `§4.4.1 and §4.7` (material exists in §4.4.1 pointer + §4.7 full development; no §4.3.1 subsection)
2. §5.1 compression ratio `30× (Hamerton)` → `roughly 5× (Hamerton, ~33K-token corpus) to 78× (Babur, ~550K-token corpus)` (arithmetic fix; 33K÷7K ≈ 4.7× not 30×)
3. §1.3 Letta matched-comparison numbers aligned to 5-judge primary (3.10 / 2.76 / 2.42 vs 2.96 / 1.72 / 1.88) to match §4.7 Table; `BL spec.md variant` flagged inline
4. §4.7 Table column header `BL spec → Haiku` → `BL unified brief → Haiku` (Anthropic's labeling suggestion)
5. §4.7 methodological note hoisted from paragraphs-after-Table to immediately-before-Table, with closing pointer on the old location
6. §1.3 compression headline narrowed from "outperforms raw source" to "captures most of the raw-source predictive signal" — the old headline contradicted the same paragraph's "corpus slightly exceeds the spec on most subjects"
7. §1.4 `Nearly every real AI user starts from a baseline lower` → `By structural extrapolation from the sample (not by direct measurement), real AI users are expected to sit at baselines lower` (OpenAI's overclaim flag)
8. §2.3 + §5.2 Twin-2K `comparable prediction accuracy` → `positive results on a different task format` (Anthropic + OpenAI flagged the unsupported "comparable" claim since numbers are not reported)
9. §1.2 C8 description `The entire training corpus` → `The full training-half corpus` (Anthropic precision flag)

**Word doc regenerated** after fixes at `docs/beyond_recall_v8_draft.docx`.

**Items flagged in the synthesis but NOT applied this session (defer to author):**
- §3.1 / §3.4 Haiku vs Sonnet battery-generator ambiguity (needs verification against scripts; Anthropic flag)
- Token-count reconciliation 5-8K vs 8-10K (partially handled in the revised §1.3 compression headline; may need further polish)
- §7 transition sentence from §6 Limitations (Anthropic noted §7 feels orphaned; easy to add but judgment call)
- §4.1.2 Franklin wrong-spec overlap disclosure emphasis (Mistral flag; current wording defensible)
- §4.4 Supermemory one-line summary polish (Mistral flag; paragraph body already documents mixture)

### 2. Review author's full read-through feedback

Author said "will review in one pass tomorrow." Apply their feedback before abstract drafting.

### 3. Write the abstract

Done last, after author's read-through + gate review are resolved. The paper has gone through significant framing evolution; the abstract should lead with "representational accuracy" as the measurable AI-side property, behavioral prediction as the test (not the goal), the gradient as the primary empirical result, and architectural convergence as independent validation. ~300 words.

### 4. Review §4.2.1 improvement-rate figure

Figure-generation agent was running at session close. Output should land at `figures/fig_4_2_1_question_improvement_rates.png` (+ .pdf). Confirm it's legible and reference is correctly placed in §4.2.1.

### 5. Review repo completeness audit results

Audit agent was running at session close. Output at `docs/reviews/repo_completeness_audit_<timestamp>.md`. Some fixes applied directly; others flagged for author decision (especially dead-weight files and old draft versions).

### 6. Word doc generation

To run after the above land. Pandoc conversion of v8 draft. Author will use this for final review pass.

### 7. Minor items flagged but deferred

- §6 review: four subsections are in. Author reviewed and approved through §6.4.
- Residual cases from the wrong-spec label cleanup (blog_post_v2.md, wrong_spec_detection_analysis.md, name_blind_wrong_spec_pilot.md) were deliberately skipped this session per author decision ("ignore the residual cases for now we'll do a final full review later"). Pick these up in the final pass.

---

## Current state of v8 draft — full section map

Working file: `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v8_draft.md` (~1700 lines).

### §1 Introduction
- §1.1 Recall Is Not Interpretation. Interpretation Can Be Measured. (Opening framing; representational accuracy defined; research question threaded)
- §1.2 What We Tested (5 hypotheses H1-H5; primary + secondary outcomes; conditions table; panel description now 5-judge primary with Gemini-as-sensitivity)
- §1.3 What We Found (Primary result gradient; Compression; Mechanism with hedging under two rules; Additivity with 5-judge numbers; Where spec helps and hurts; Robustness note; Letta stateful architectural observation)
- §1.4 Why the Gradient Matters for Real Users
- §1.5 Behavioral Alignment and the Human-AI Interaction Problem

### §2 Related Work
- §2 intro (reframed, median → "on average across a large population")
- §2.1 Memory systems for LLM agents (Table 2.1; benchmark-dispute paragraph)
- §2.2 Traceability
- §2.3 Memory and personalization benchmarks (5 benchmarks, each with scope-difference framing; Twin-2K simplified per author direction — no specific numbers reported as benchmark)
- §2.4 Cognitive and representational foundations (Bartlett, Hinton with 5-judge primary numbers, Chen, Jiang, Jain reframed to sycophancy, Lu reframed to Assistant Axis)
- §2.5 LLM-as-judge (content ported from v7)

### §3 Study Design
- §3.1 Representational Accuracy
- §3.2 Subjects (14 main + Franklin control; baseline-as-observable-proxy section)
- §3.2.1 Pretraining-coverage variance
- §3.3 Pipeline (5-step table, 46 predicates, Hamerton examples, all-MiniLM-L6-v2)
- §3.4 Question Batteries (backward-design + leakage audit)
- §3.4.1 Circularity Controls
- §3.5 Experimental Conditions
- §3.6 Response Models
- §3.7 Evaluation: LLM-as-Judge with Calibration
- §3.7.1 Judge Panel
- §3.7.2 Calibration (5-judge primary decision + Gemini-conservatism note)
- §3.7.3 Fractional Score Interpretation
- §3.7.4 Inter-Judge Agreement
- §3.7.5 Aggregation
- §3.7.6 Rubric-handling limitations (validity audit)

### §4 Results
- §4.1 The Cross-Subject Gradient
- §4.1.1 Franklin as the high-baseline reference
- §4.1.2 Living-user replication (author pilot) — Franklin-for-all language removed, partition argument rewritten with 5-judge per-subject matched-baseline data (+0.27 / +0.30 / +0.20, mean +0.25)
- §4.2 Compression: Structure vs. Raw Text
- §4.2.1 Question-Improvement Rate (sports-register cleanup applied; new comparison figure in flight)
- §4.3 Mechanism: Content, Not Format
- §4.4 Memory-System Composition (5-judge primary numbers; dedicated Supermemory mixture section with four examples: Fukuzawa Q26, Yung Wing Q5, Zitkala-Sa Q18, Fukuzawa Q16; local-vs-cloud distinction noted in BL substrate per-system read)
- §4.4.1 Letta stateful-agent path: a pointer
- §4.5 Robustness and Sensitivity
- §4.5.1 Cross-provider response generation (Tier 2 replication): 5/6 cells reproduce direction
- §4.5.2 Judge panel sensitivity (5-judge vs 7-judge): 5-judge is conservative choice
- §4.5.3 What these do not address: class-level circularity
- §4.6 Interpretation vs. Recall (cross-system mixture; three mechanisms reproduce; Keckley Q21 most-consistent cross-substrate replication; hedging hypothesis removed per author direction)
- §4.7 Architectural Convergence: Letta Stateful-Agent (5-judge primary numbers after GPT-5.4 fix; content comparison subsection; methodological note on spec.md variant)
- §4.8 Scaling and Practical Implications (context budget; authoring cost; per-query cost; **dynamic activation section**; **modifiability section**; **temporality section**; **topic decomposition + piecewise ablation as §8 flags**; four infrastructure properties with **local-executable retrieval** as fourth bullet)

### §5 Discussion
- §5.1 What the study demonstrates (research question threaded; 5 bulleted empirical results with §4 cross-refs)
- §5.2 Recall, prediction, persona: what we measure and what it isn't (prediction is the test not the goal; behavioral stability premise; canonical life events as separate open question; Twin-2K / PersonaGym / AlpsBench / LOCOMO-LongMemEval all positioned)
- §5.3 The population of relevance (not a retrospective study framing; historical bias; low-baseline slice as proxy; author pilot; structural argument)
- §5.4 Content specificity and mechanism (H3 stated directly; Patterns 1/2/3 explicitly named and re-asserted on each reference; dynamic activation as requirement paragraph; Keckley Q21 fully layman-ized; component ablation flagged)
- §5.5 Architectural convergence (target not implementation; BL is one among many; three divergence axes; constraint on claims)
- §5.6 What the study does not settle (directionality-vs-precision framing; expanded rubric-validity with 3 documented issues; Twin-2K as component-ablation proxy)

### §6 Limitations (scoped to avoid double-claiming with §5)
- §6.1 Subject sample (public-domain selection / self-presentation / translation artifacts / era)
- §6.2 Measurement apparatus (response-model coverage / prompt-phrasing ambiguity / inter-judge calibration variance)
- §6.3 Pipeline and specification stability (pipeline version / stability check ~45% verbatim / model choices not varied)
- §6.4 Scope of exploration (grid coverage / Letta stateful pulled from main scope / Twin-2K as separate study)

### §7 Behavioral alignment and safety alignment
- Three paragraphs: two separate priorities; where the axes bleed together (prediction as proxy for understanding); open research question on specifications for users with malicious intent

### §8 Future Work
- §8.1 Measurement methodology
- §8.2 Subject and corpus expansion
- §8.3 Specification design and composition
- §8.4 Production serving and infrastructure
- §8.5 Architectural convergence and alternative implementations
- §8.6 Safety-alignment integration

### Pending: Abstract (to be written last)

---

## Active background agents at session close

Three agents running when session ended. Their outputs will be ready for next session:

1. **`af32261ad11ea4ebc` — Full paper collective gate review.** Mistral + Cerebras + Groq + GPT-5.4 + Claude Opus. Output: `docs/reviews/full_paper_gate_review_*.md` + `docs/reviews/gate_review_synthesis_*.md`.

2. **`ac45d96373d7b1aab` — §4.2.1 improvement-rate figure generator.** Output: `figures/fig_4_2_1_question_improvement_rates.png` + figure reference added to §4.2.1.

3. **`a269d028d6e5c5b38` — Repo completeness audit.** ✓ COMPLETED. Output: `docs/reviews/repo_completeness_audit_20260422_173831.md`.

**Mechanical fixes applied directly:**
- 6 broken path references corrected in the paper draft (§3.5, §3.7, §3.7.3, §3.7.4, §4.7)
- `scripts/run_global_rerun.py` copied into the public repo (was only in the private `memory_system/` tree)
- `README.md` updated: paper pointer → v8, repo structure tree, 5-judge primary stats (slope −0.96, R² 0.82, p < 0.001; Wilcoxon W=10 p=0.005, W=11 p=0.007), low-baseline +0.89, Letta finding N=3, v1 condition label corrected
- `docs/blog_post_v2.md`, `docs/PAPER_CORRECTIONS.md`, `figures/README.md`: "Franklin-for-all" → "fixed derangement" where v1 is meant
- `docs/DATA_REFERENCE.md`: added header note that paper-location pointers reference v6 and section numbers should be cross-confirmed against v8

**Missing with no obvious target (flagged for tomorrow):**
- `results/interjudge_agreement/` — cited but directory does not exist
- `docs/research/_content_analysis_results.json` — cited in §4.7 referential density; numbers exist only in paper prose, not in a named artifact
- `scripts/compute_question_improvement_rate.py` — cited in §4.2 and `KEY_FINDINGS.md` M11; does not exist

**Dead weight flagged for author decision (not deleted):**
- v6/v7 drafts, 5 `.docx` iterations of the S105 draft at top-level `docs/`
- v6/v7 review artifacts (`.html`/`.docx`/`.clean.md`)
- LaTeX test-build intermediates (`.aux`/`.log`/`.out`/`.tex`/`.pdf`)
- 20+ historical review round files in `docs/reviews/`
- Probe and exploration scripts in `scripts/` (`_probe_*`, `_check_*`, round-review scripts)
- Recommended: archive v6/v7 drafts to `docs/versions/`; historical review rounds to `docs/reviews/_archive/`

4. **`a3a0640452c76cb61` — Word doc generation.** ✓ COMPLETED. Output: `docs/beyond_recall_v8_draft.docx` (1.8 MB, ~140-180 Word pages, 38,414 words). Method: pandoc via pypandoc. Script: `scripts/export_v8_to_docx.py`. Intermediate cleaned markdown: `docs/beyond_recall_v8_draft.clean.md`. Includes auto-generated TOC, 32 native Word tables, 12 embedded figures (11 at section anchors + fig_4_2_1_question_improvement_rates inline at §4.2.1). Editorial scaffolding stripped; closing marker "*Paper body complete. Abstract to be written last.*" kept intentionally so the reviewer sees the abstract-pending state.

Note on regeneration: if tomorrow's session applies gate-review fixes or other edits to the v8 draft, regenerate the Word doc with `python scripts/export_v8_to_docx.py` before the author's read-through.

5. **`a7246bff17ad75e18` — Figure quality review (first attempt).** ❌ INCOMPLETE. Agent returned a truncated summary with no deliverables. Relaunched as agent `ad632e0bf755907bc` with tighter scope (see below).

5b. **`ad632e0bf755907bc` — Figure quality review (relaunched, review-only).** ✓ COMPLETED. Output: `docs/reviews/figure_review_20260422.md`. 14 figures × 2 vision providers (Claude Opus 4.5 + GPT-5.4) = 28 vision calls, all succeeded. **Verdict: NOT PUBLICATION-READY due to correctness issues, not just polish.**

   **Grade distribution:** B on 11 of 14 figures, C on fig5, mixed (B/C range) on fig3 and fig4. No A grades.

   **Critical findings (correctness issues — fix before publication):**
   - **fig3 retrieval disagreement:** numbers on figure (68/11) do not match paper-stated values (93/53)
   - **fig4 hedging reduction:** shows 2 bars; paper reports 3 conditions × 2 rules = 6 bars
   - **fig5 condition effects:** uses named conditions instead of C1-C9 labels from the paper
   - **fig7 memory systems:** missing Base Layer from the system set
   - **fig8 judge agreement:** shows 7 judges, paper's 5-judge primary panel would be 5 (plus 2 sensitivity)

   **High-priority findings (visible to any reviewer):**
   - 9 of 14 figures use palettes that are not colorblind-safe or grayscale-legible
   - 9 figures have oversized presentation-style typography (not conference two-column scale)
   - Reference lines / shaded regions on fig1, fig_4_1, fig9, fig_4_2 lack in-figure labels
   - fig2, fig5, fig_4_2_1 use condition codes (C2a/C4/C8) without in-figure legend

   **Minimum fix path to publication-ready:** reconcile the 5 caption/figure mismatches, replace remaining non-colorblind-safe palettes, explain or drop unlabeled reference lines on fig1 and fig_4_1.

   **For tomorrow:** these are the single most substantive outstanding items. Address before the abstract is written. Regeneration scripts exist at `scripts/generate_figures_v3.py`, `scripts/generate_fig_4_2_1.py`, and individual `generate_fig_*.py` files. Pick up the Critical list first.

6. **`af299f7ae5abd5796` — Repo hygiene + naming + traceability audit.** ✓ COMPLETED. Report: `docs/reviews/repo_hygiene_audit_20260422_182500.md`. Substantial reorganization applied.

   **Per-folder grades (after this pass):**
   - Top-level: A-
   - `docs/` overall: A- (from B)
   - `docs/reviews/`: A- (from C — 40 files at top level reduced to 11, 29 moved to `_archive/`)
   - `docs/versions/`: B+ (new; holds 18 archived drafts + LaTeX test-build subfolder)
   - `docs/research/`: B
   - `data/`: B+
   - `results/`: B (`global_<subject>/` prefix inconsistent with `data/global_subjects/<subject>/` — documented, not fixed)
   - `scripts/`: C (93 files, no convention separating active runners from probes / one-off reviews — flagged)
   - `figures/`: B+ (v6-era fig1-11 alongside v8-era fig_4_1 / fig_4_2 / fig_4_2_1 — flagged)

   **Mechanical moves applied:**
   - 13 historical drafts + .docx exports moved from `docs/` top-level → `docs/versions/`
   - 29 historical review artifacts (round_0*, gemini_*, s114_* session reviews, gtm_jargon_scan, section_4_6_*) moved to `docs/reviews/_archive/`
   - 4 of 5 LaTeX build intermediates moved to `docs/versions/_latex_test_artifacts/` (5th `.aux` blocked by a single-file filesystem sandbox — flagged for manual `mv`)
   - Three README.md files rewritten (`docs/`, `docs/versions/`, `docs/reviews/`) + one-liner updates to `figures/README.md` and `scripts/README.md`

   **PROVENANCE_INDEX addendum applied.** S115 addendum added covering 8 claim categories present in v8 but not previously indexed: question-improvement rate, Letta stateful N=3 matched-rerun numbers, wrong-spec v1/v2 means, 60.6% content-grounded detection, hedging rates under both classifier rules, per-response anchor-crossing, spec-activation tag-citation, provider benchmark 68-85% range. Also flagged 2 missing scripts and 2 missing persisted files.

   **Traceability-matrix assessment.** PROVENANCE_INDEX is substantial and well-structured (85+ rows, VERIFIED / APPROXIMATE / NOT FOUND legend). S115 addendum closed the v8-specific gaps. Remaining work: (a) v6 → v8 section-number remap across existing rows (~1 hour, §-by-§; author task); (b) no reverse-lookup index (script → outputs → paper-section) exists yet (2-hour post-launch addition).

   **Flagged for author decision:**
   - Figures: `fig1_*` through `fig11_*` are v6-era (7-judge numbers). Move to `figures/_archive/`? Coordinate with figure-review fix list above (which flags caption-mismatch correctness issues on the same files).
   - Scripts: ~45 scripts (`review_paper_round2*`, `_probe_*`, export utilities, one-off scans) are archive candidates. Retain `_verify_battery_leakage.py` (load-bearing).
   - One `.aux` LaTeX file blocked by sandbox; one-line manual `mv` will clear it.
   - Two ambiguous `s114_*` files at `docs/reviews/` top level (`final_locked_content_review`, `session_close_handoff`) — keep current or archive?
   - PROVENANCE_INDEX §-number remap v6 → v8 across existing rows.

   **Scope-collision note from the hygiene audit itself:** the completeness audit (`a269d028d6e5c5b38`) flagged historical drafts / reviews / LaTeX artifacts as "do NOT delete — flag for author decision." The hygiene audit's task explicitly authorized moving them into `_archive/` subfolders (moving is not deleting). Moves executed per the hygiene audit's scope authorization; no files deleted.

---

## Canonical numbers reference (for cross-section consistency checks)

All on 5-judge primary (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4) unless noted as sensitivity.

### Gradient (§4.1, N=14)
- Regression slope: −0.96 [95% CI −1.24, −0.67]
- R²: 0.82
- Slope p-value: < 0.001 (0.000009)
- Wilcoxon C5 vs C4a: W = 11, p = 0.007
- Wilcoxon C5 vs C2a: W = 10, p = 0.005
- Subjects positive on Δ_C4a: 12 of 14
- Low-baseline (n=9): mean Δ_C4a = +0.89, all positive
- Franklin baseline: C5 = 3.77, C2a = 3.37, C4a = 3.65

### Author pilot (§4.1.2, N=40)
- C5 = 1.03, C2a = 2.86, C2c = 2.59, C4 = 2.93, C4a = 3.02
- Δ_C4a = +2.00 (study's largest)
- Anchor-crossing rate: 75.0%

### Matched-baseline Franklin-for-all (§4.1.2)
- Sunity Devee Δ = +0.27 (C5 = 1.03)
- Ebers Δ = +0.30 (C5 = 1.02)
- Hamerton Δ = +0.20 (C5 = 1.26)
- Mean = +0.25

### Wrong-spec aggregates (§1.3, §4.3, 13 globals)
- C2a (correct): Δ +0.35
- C2c v2 random derangement: Δ +0.22
- C2c v1 fixed derangement: Δ −0.25

### Memory-system spec deltas (§4.4, 5-judge primary)
Controlled / Low-baseline / Wilcoxon p:
- Mem0: +0.12 full / +0.10 low / ns
- Letta archival: +0.20 full / +0.17 low / p = 0.0017
- Zep: +0.19 full / +0.17 low / p = 0.0004 (9/9 low-baseline positive)
- Supermemory: −0.05 full / −0.01 low / ns
- Base Layer substrate: +0.08 full / +0.08 low / ns

Native:
- Mem0: +0.33 full / +0.32 low / p = 0.0088
- Zep: +0.33 full / +0.30 low / p = 0.0015 (9/9 low-baseline positive)
- Letta: −0.02 full / −0.04 low / ns
- Supermemory: −0.07 full (n=10) / −0.03 low (n=7) / ns
- Base Layer: N/A by design

### Supermemory mixture (§4.4, 516 questions)
- |Δ| ≥ 1.0: 89 of 516 (17.2%)
- Δ ≥ +1.0 (helps): 37 (7.2%), mean +1.45
- Δ ≤ −1.0 (hurts): 52 (10.1%), mean −1.41

### Hedging (§1.3, two rules)
- Narrow rule (`starts_refusal`): C5 = 28.8%, C2a = 1.4%, C4a = 0.0% (of 507)
- Broader rule (`refusal_ge_1`): C5 = 41.2%, C2a = 7.9%, C4a = 0.4% (of 507)

### Wrong-spec detection (§1.3, §4.3, N=587)
- 60.6% explicit mismatch flag
- 36.5% applied mismatched content
- 2.0% hedged implicitly
- 0.9% ambiguous

### Spec-activation (§4.3)
- 78.6% correct-spec tag citation
- 50.0% wrong-spec tag citation

### Per-question improvement rates (§4.2.1, low-baseline 351 questions)
- C2a spec only: 58.8% improve, 26.7% worsen
- C4 facts only: 60.1% / 26.6%
- C8 raw corpus: 64.5% / 24.5%
- C4a facts+spec: 65.8% / 26.4%
- Win rate (any improvement): spec 70.9%, facts 72.9%, corpus 78.3%, facts+spec 78.6%
- Median Δ when improved: +1.00
- Median Δ when worsened: −0.40

### Letta stateful matched-rerun (§4.7, 5-judge primary)
- Hamerton: Letta 3.10, BL 2.96, Δ +0.14
- Ebers: Letta 2.76, BL 1.72, Δ +1.05
- Babur: Letta 2.42, BL 1.88, Δ +0.54
- Base Layer side used `spec.md` variant (not layered stack; noted in §4.7 methodological note)

### Tier 2 cross-provider (§4.5.1)
- 5 of 6 (subject, response-model) cells reproduce direction
- Non-matching: Zitkala-Sa × Gemini Pro (Δ −0.55, consistent with main-study Zitkala-Sa null)

### Letta scaling (§4.7)
- Hamerton block: 22,472 chars / ~5,600 tokens
- Ebers block: 68,413 chars / ~17,000 tokens
- Babur block: 335,349 chars / ~84,000 tokens (hit API ceiling at ~333K; 25.4% verbatim sentence duplication)
- BL compose keeps spec at 34,000-40,000 chars across corpus sizes

### Content comparison (§4.7)
- Verbatim corpus overlap: Letta 0.0-1.0% (5-gram), BL 0.0%; both ~0.1% (10-gram)
- Unique proper noun density: Letta ~10× higher (Babur 540 vs 46; Ebers 58 vs 19)

### Specification stability (§6.3)
- Run-to-run verbatim match at temp=0: ~45%
- Remainder: semantically similar variations
- Prediction band stable across runs

---

## Voice rules (active and enforced)

- **No em-dashes in prose.** Tables / code blocks OK. Restructure sentences to use colons, periods, semicolons, or parentheses.
- **No GTM verbs:** "beats," "crushes," "dominates," "unlocks," "leverages," "transforms," "revolutionizes" — absent.
- **Minimize pitch-deck superlatives:** "cleanest," "strongest," "most robust." Use factual descriptors with the numbers attached.
- **Minimize "load-bearing" / "flagship" / "drives" in GTM sense.** Reserved for technical descriptions.
- **"Lift" surgical.** Fine as a label next to a number ("spec lift +0.89"). Replace in prose ("specification lifts" → "specification improves").
- **Condition labels explicit on first mention per section.** C5 (baseline, no context), C2a (spec only), etc.
- **Patterns 1/2/3 always re-asserted with names.** Not just "Pattern 1" without the "(pattern supply)" gloss.
- **Plain-language over jargon.** "Five-word sequence" not "5-gram." "Consecutive word sequence" not "n-gram." Define technical terms on first use.
- **Claim hedging:** "directional, not precision" — §5.6 framing. Apply throughout.
- **"Raw data available at..." convention** for every experimental mention in paper prose.
- **Primary source references.**
- **"Interpretation" not "understanding"** in the paper's framing context.

---

## Wrong-spec labeling correction (important — was corrected this session)

The `C2c_wrong_spec` condition in `results/global_*/results_v2.json` is NOT "Franklin-for-all." It is a deterministic fixed derangement defined in `scripts/run_global_rerun.py` (WRONG_SPEC_PAIRING). Mapping:

```
augustine    → fukuzawa       ebers        → equiano
babur        → keckley        equiano      → ebers
bernal_diaz  → sunity_devee   fukuzawa     → augustine
cellini      → zitkala_sa     keckley      → babur
rousseau     → yung_wing      seacole      → bernal_diaz
sunity_devee → cellini        yung_wing    → rousseau
zitkala_sa   → seacole
```

(Six two-cycle swaps + one five-cycle. Designed to maximize cultural/temporal distance.)

Franklin-for-all is real only for Hamerton (the Hamerton-only pre-globals test).

Previous documentation called this "v1 Franklin-for-all" — that label was stale inherited text from the Hamerton-only era. Corrected in paper + 9 support docs this session.

---

## Key decisions made this session (by session chronology)

- **GPT-5.4 bug fix (Letta stateful):** `max_tokens` → `max_completion_tokens`. All 5-judge numbers now canonical.
- **Wrong-spec label correction:** fixed derangement, not Franklin-for-all. Applied paper-wide + 9 support docs.
- **Twin-2K simplification:** no specific numbers reported as benchmark; positioned as prior exploratory work in different pipeline version.
- **Hedging provenance:** original classifier unrecoverable; replacement classifier written at `scripts/classify_hedging.py` with two rules (`starts_refusal` narrow, `refusal_ge_1` broader); both rules reported in §1.3 and KEY_FINDINGS m3.
- **§4.7 Base Layer condition disclosure:** used `spec.md` variant (7K-char unified), not the full layered stack. Flagged in §4.7 methodological note and §5.6 / §6.4.
- **§7 Behavioral alignment and safety alignment:** kept as standalone short section per author request (originally proposed as optional §5.7, promoted to standalone).
- **Local-vs-cloud distinction:** Base Layer substrate runs locally (MiniLM + ChromaDB); all 4 commercial providers require cloud API calls. Added to §4.4 + §4.8.

---

## File map — key paths for next session

### Working draft
- `docs/beyond_recall_v8_draft.md` — the paper (v8)

### Support docs (updated this session)
- `agents/STUDY_MEMORY.md` — canonical numbers, pipeline conventions
- `docs/DATA_REFERENCE.md` — per-condition numbers
- `docs/KEY_FINDINGS.md` — M1-M9 major + m1+ minor findings
- `docs/PROVENANCE_INDEX.md` — number → source file index
- `docs/ANALYSIS_PLAN_LOCK.md` — aggregation rules
- `docs/METHODOLOGY.md`
- `docs/research/` — per-topic analysis reports

### Key scripts (used this session)
- `scripts/compute_wrong_spec_5judge.py` (aggregate, fixed-derangement label corrected)
- `scripts/compute_wrong_spec_per_subject.py` (per-subject for §4.1.2 matched-baseline)
- `scripts/compute_memory_systems_5judge.py` (§4.4 aggregates)
- `scripts/classify_hedging.py` (both rules)
- `scripts/review_paper.py` (now defaults to exclude Gemini; `--include-gemini` to enable)

### Results
- `results/global_<subject>/` — per-subject main-study data (14 subjects)
- `results/hamerton/` — Hamerton separate
- `results/_tier2/global_<subject>/` — cross-provider replication
- `results/_wrong_spec_v2/` — random-derangement seed=42 variant
- `results/_letta_rerun/` — Letta stateful matched-rerun

### Figures
- `figures/fig1_global_gradient.png`
- `figures/fig2_compression_curve.png`
- `figures/fig3_retrieval_disagreement.png`
- `figures/fig4_hedging_reduction.png`
- `figures/fig5_condition_effects.png`
- `figures/fig10_letta_scaling.png`
- `figures/fig11_tier2_replication.png`
- `figures/fig_4_1_gradient_scatter.png/.pdf`
- `figures/fig_4_2_compression.png/.pdf`
- `figures/fig_4_2_1_question_improvement_rates.png` **(pending from active agent)**

### Review artifacts
- `docs/reviews/s114_session_close_handoff.md` — prior session close (context for earlier decisions)
- `docs/reviews/section_4_6_review_*.md` — §4.6 collective review results
- `docs/reviews/gtm_jargon_scan_*.md` — Haiku voice scan with top-10 priority list
- `docs/reviews/full_paper_gate_review_*` **(pending from active agent)**
- `docs/reviews/gate_review_synthesis_*` **(pending from active agent)**
- `docs/reviews/repo_completeness_audit_*` **(pending from active agent)**
- `docs/reviews/session_close_handoff_v8_complete.md` — this document

---

## How to resume tomorrow

1. Read this file top to bottom.
2. Read the three pending agent outputs (collective gate review synthesis; figure generation; repo audit).
3. Apply consensus critical issues from gate review (if any are minor surgical edits).
4. Flag any non-trivial gate-review issues for author.
5. Generate the Word doc (pandoc on v8 draft) for author's read-through.
6. Ask author what to tackle first: the abstract, the author's own read-through feedback, or the gate review fixes.

The research agenda in §8 is not for this session — it's the post-publication plan. Resist scope creep into any §8 item.

---

*End of handoff.*
