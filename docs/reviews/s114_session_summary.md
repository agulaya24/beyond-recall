# S114 Session Summary — Beyond Recall paper review

**Date:** 2026-04-20
**Target launch:** Tuesday 2026-04-21
**Status at session end:** v8 draft exists with §1 + §2 locked, §3-§8 ported from v6 with sweeps applied. §3 review begins next session.

---

## Top-line outcome

- **v8 draft built** at `docs/beyond_recall_v8_draft.md`. Complete paper structure (1,101 lines).
- **§1 Introduction rewritten end-to-end** (§1.1 through §1.5, five subsections).
- **§2 Related Work rewritten end-to-end** (§2 intro + §2.1 through §2.5, five subsections).
- **Em-dashes removed from v6 prose** (304 instances restructured to zero across the paper body; editorial HTML comment block at v6 L1-197 left untouched, will be deleted pre-publication).
- **Paper-wide 85%+ recall-benchmark claim swept** (6 replacements) to "publish recall-benchmark scores in the 68–85% range (methodology disputed, see §2.1)".
- **Figures 10 (Letta scaling) and 11 (Tier 2 replication) generated** at `figures/fig10_letta_scaling.png` and `figures/fig11_tier2_replication.png`.
- **Nine research agents deployed** this session; findings integrated into v8 and `KEY_FINDINGS.md`.
- **KEY_FINDINGS.md substantially expanded:** m15-m22 added (eight new minor findings), F8-F11 added (four new open questions), per-provider character-summary section added.
- **One git commit** landed at `0da9a7a`: "S114: paired analyses across all 5 memory systems + v7 §1 locked." Not pushed.

---

## Artifacts produced or modified

### Paper drafts

| File | State |
|---|---|
| `docs/beyond_recall_v6_draft.md` | Em-dashes removed across prose (304 → 0). Editorial HTML block unchanged. §1+§2 content still present but superseded by v7/v8. |
| `docs/beyond_recall_v7_draft.md` | NEW this session. §1 + §2 locked content (no §3+). Used as review working copy. |
| `docs/beyond_recall_v8_draft.md` | NEW. v7 §1+§2 + v6 §3-§8 with 85% sweep. Starting point for §3 review next session. |

### Review artifacts

| File | Purpose |
|---|---|
| `docs/reviews/s114_paragraph_review.md` | Running review log with every round of feedback captured verbatim + actions taken. Read top-to-bottom for complete history. |
| `docs/reviews/s114_word_annotations.md` | Overwritten on each extraction; latest batch is always in this file. Historical batches preserved in the paragraph review log above. |
| `docs/reviews/s114_session_summary.md` | This document. High-level summary. |
| `docs/beyond_recall_review.docx` (v6 review) | Generated early in session for §1.1 review round. |
| `docs/beyond_recall_v7_review.docx` | Generated mid-session for docx review of §1 + §2 locked content. Aarik annotated with 10 comments. |

### Research reports (all at `docs/research/`)

| File | Scope |
|---|---|
| `provider_benchmarks.md` | Primary-source audit of Mem0, Letta, Supermemory, Zep benchmark claims. Source for the 68–85% honest range. |
| `supermemory_c1_vs_c3_paired_analysis.md` | Paired C1 vs. C3 response analysis for Supermemory. Discovered the mixture-of-swings pattern and the Keckley Q21 refusal case. |
| `mem0_letta_zep_c1_vs_c3_analysis.md` | Mirror analysis on the other three commercial memory systems. Generalized the mixture pattern and found Letta retrieval-duplication. |
| `baselayer_c1_vs_c3_paired_analysis.md` | Mirror analysis on Base Layer's retrieval substrate. Partially contradicted the §4.4 prompt-template hedging hypothesis. |
| `letta_stateful_deep_read.md` | Block content characterization for Hamerton, Ebers, Babur. Surfaced battery mismatch + anonymization premise + ceiling phrasing issues. |
| `letta_stateful_matched_rerun.md` | Resolved the three concerns with a clean matched-conditions rerun. Corrected numbers (Ebers Δ +0.75, Babur Δ +0.29). |
| `wrong_spec_detection_analysis.md` | Quantified the 60.6% explicit-detection rate across 587 wrong-spec responses. |
| `section_2_1_verification.md` | Deep verification of §2.1 memory-system architectural claims. Found 6 issues (Supermemory architecture most substantive). |
| `section_2_3_verification.md` | Verified LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo. Found Wu/Samuel author corrections + Twin-2K 71.72% (not 71.83%). |
| `section_2_4_verification.md` | Verified Bartlett, Hinton, Chen, Jiang, Jain, Lu. Found Jain is about sycophancy (not hedging) and Lu is about Assistant Axis (not hedging-as-structural). |

### Generated figures

- `figures/fig10_letta_scaling.png` — Letta block size vs. corpus size with 333K ceiling + duplication % bar chart.
- `figures/fig11_tier2_replication.png` — Cross-provider replication grouped bar chart.

### Scripts added

- `scripts/remove_em_dashes.py` — idempotent em-dash removal with 210 rewrites.
- `scripts/build_review_html.py` — generates HTML review artifact with inline figures.
- `scripts/export_to_docx.py` — v6 pandoc-based docx export.
- `scripts/export_v7_to_docx.py` — v7 variant with §1.3 bold-label figure anchors.
- `scripts/build_v8.py` — merges v7 §1+§2 with v6 §3-§8 and applies the 85% sweep.
- `scripts/extract_docx_annotations.py` — extracts comments/highlights/tracked-changes from .docx.
- `scripts/classify_wrong_spec_detection.py` — classifier for wrong-spec response categorization.
- `scripts/generate_fig10_letta_scaling.py`, `scripts/generate_fig11_tier2_replication.py` — new figure generators.
- `scripts/analyze_sm_c1_vs_c3.py`, `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py` — paired-analysis scripts.

---

## Locked §1 — Introduction

### §1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

Complete rewrite. Key moves:
- Opens with state of the art (not thesis-first).
- Defines **interpretation** (human-side property) and **representational accuracy** (AI-side property) as paired concepts.
- States the core hypothesis explicitly: representational accuracy predicts alignment between an AI system's behavior and the intent and behavior of the person it serves.
- Cites the 68-85% benchmark range (softened from 85%+ blanket claim).

### §1.2 What We Tested

Complete rewrite. Added:
- Compact list of 14 subjects across four continents and two millennia.
- 1-5 rubric as table (revised this session in v8 per Aarik's docx feedback).
- Three explicit behavioral-battery question examples (added this session to v8 per docx feedback).
- Baseline concept defined (C5, low-baseline ≤ 2.0, population of relevance).
- Judge calibration paragraph naming all 7 judges and the Gemini +1 inflation finding.
- "Additional testing for Letta" note for the stateful-agent path.

### §1.3 What We Found

Complete rewrite with seven findings:
- **Primary result: the gradient** — slope −0.98, Wilcoxon p=0.0063, 12/14 positive; 9/9 low-baseline sensitivity check. +1.04 point significance tied to rubric (added to v8).
- **Compression: structure outperforms raw source** — 7,300-token spec (3.04) vs. 34,168-token corpus (2.32). "Beats" sweep applied (v8). Restructured as layman sub-header + *Measurement* sub-paragraph (v8).
- **Mechanism: content, not format** — wrong-spec near baseline (Δ +0.28), Franklin-for-all below baseline (Δ −0.16), 60.6% explicit detection rate (validated), hedging 25.0% → 2.6% → 0.6%.
- **Additivity: layers on three of four commercial memory systems** — Mem0 +0.13, Letta +0.23, Zep +0.20, Supermemory ~0. Per-system bullet list with Base Layer retrieval-floor performance.
- **Where the specification helps and where it hurts** — mixture-not-cancellation finding. Three example questions inline verbatim (Ebers Q3, Sunity Devee Q35, Keckley Q21).
- **Robustness: effect is not an artifact of Claude talking to Claude** — Tier 2 cross-provider replication, 5 of 6 cells positive; LLM-as-judge circularity remains broader limitation.
- **Architectural observation: Letta's stateful-agent path** — matched-conditions deltas (Hamerton +0.20, Ebers +0.75, Babur +0.29). Block growth, ceiling phrasing honest about 333K/335K, compose-step invariance.

### §1.4 Why the Gradient Matters for Real Users

Merged v6's §1.4 and §1.5. Three moves:
- Population-of-relevance: real AI users are below Sunity Devee's 1.03 baseline by construction.
- What we did not prove: two-user pilot acknowledged; one pilot (author's private data) cited with real numbers (C5 = 1.90, 95% CI 1.16-2.64, 60% refusal).
- Infrastructure implications: gap cannot be closed by pretraining; user-held, portable, inspectable, traceable representation is the next-generation requirement.

### §1.5 Behavioral Alignment and the Human-AI Interaction Problem (formerly §1.6)

Renumbered. Trimmed. Research-firm positioning removed per Aarik. Invitation-to-others cut.

---

## Locked §2 — Related Work

### §2 intro

Three prior directions: memory systems optimizing for recall, memory architectures modeled on human memory, human-reasoning research. Core argument: language models optimize for the median, which by construction fails every individual; we want a system biased to the individual.

### §2.1 Memory systems for LLM agents

Table 2.1 with Mem0, Letta, Supermemory, Zep. Verified architectural claims against primary sources (6 issues fixed from v6). Includes a benchmark-dispute paragraph naming the Mem0 / Zep LOCOMO dispute (`getzep/zep-papers#5`), the Atlan blog, the Supermemory comparison, and third-party reproductions (Vectorize.io). Explicitly flags benchmark methodology as immature and suggests independent third-party evaluation.

### §2.2 Traceability

Reframed as a necessity, not a feature. Fact-attribution vs. reasoning-attribution distinction. Closes on "A fact-attribution memory system lets the person audit what the system stores. A reasoning-attribution specification lets the person audit what the system believes. The first is a feature. The second is the minimum bar for a representation that acts on someone's behalf."

### §2.3 Memory and personalization benchmarks

Bulleted list of five benchmarks. Each entry positions this paper's battery against the benchmark. Verified references: Wu et al. (LongMemEval), Samuel et al. (PersonaGym), Xiao et al. (AlpsBench), Toubia et al. (Twin-2K), Maharana et al. (LoCoMo). Twin-2K 71.72% (theirs) vs. our 71.83% at 18:1 compression — distinct numbers, clarified.

### §2.4 Cognitive and representational foundations

Six references, each with an explicit experiment-design connection. Jain reframed to sycophancy (not hedging). Lu reframed to Assistant Axis (not hedging-as-structural). Chen, Arditi, Sleight, Evans, Lindsey full author list.

### §2.5 LLM-as-judge

Short. Zheng et al. (NeurIPS 2023 Datasets and Benchmarks Track) verified. Calibration framework described, detail deferred to §3.7.

---

## Major findings surfaced or confirmed this session

### Methodological findings

- **Mixture-not-cancellation is system-general** (m15). Every commercial memory system's near-null aggregate spec delta hides bilateral per-question swings. On Ebers (Δ +0.21) the spec helps on 19 of 39 and hurts on 10; on Keckley (Δ −0.26) helps on 10 hurts on 17. Reproduces on Mem0, Letta, Zep, Supermemory, and Base Layer retrieval.

- **Keckley Q21 is a specification-level dynamic** (m16). The spec's documented-dignity axioms induce refusal. Penalty at −2.33 on Supermemory and Base Layer, smaller penalties on Mem0/Zep/Letta proportional to how strong each system's retrieval-only counterfactual was. Not a memory-system artifact.

- **Three failure modes of spec-based reasoning generalize** (m17). Over-theorization on literal-recall questions; spec-induced refusals on underdetermined questions; default-axiom overfires when subject breaks their own modal pattern. Reproduces across systems.

- **Provider benchmark claims are contested, not just numerical** (m21). The real finding is that benchmark methodology is immature. Mem0 / Zep LOCOMO dispute (`getzep/zep-papers#5`). Supermemory publishes direct head-to-head vs. Zep. Vectorize.io third-party produces yet different numbers. Evaluation harness for Mem0 is open-sourced (`github.com/mem0ai/memory-benchmarks`). Evaluation harness for Supermemory is open-sourced (memorybench). Zep is on arXiv. Letta is blog-only.

- **Wrong-spec detection upper bound: 60.6% explicit** (m20). N=587 wrong-spec responses classified and spot-checked (30/30 agreement). Name-blind control is follow-up work (F9).

- **Letta archival retrieval has severe fact duplication** (m18). Dedup ratio 0.34-0.47. Paper's new punch-list item for §4.3.2.

- **Base Layer prompt-template hedging hypothesis partially contradicted** (m19). §4.4 mechanism claim needs rewrite. Actual pattern: spec hedges less when retrieval-grounded, more when it cannot be grounded.

- **Author baseline pilot: Hamerton regime, not Franklin regime** (m22). C5 = 1.90, 60% refusal, 50% at rubric floor. N=10, single-judge caveat. Private data, internal evidence only (outside public repo).

### Paper-structural findings

- **Letta stateful-agent matched-rerun corrections** (from the matched-rerun agent). Battery mismatch and anonymization premise resolved. Claim survives; magnitudes are ~40-60% smaller than v6 reported.
  - Ebers: Δ +1.21 (v6) → Δ +0.75 (corrected, matched).
  - Babur: Δ +0.57 (v6) → Δ +0.29 (corrected, matched).
- **Ceiling phrasing is directionally correct but slightly off**. Real pattern: HTTP 400 starting at 332,585 chars; final block 335,349; declared metadata limit 100,000 unenforced.
- **§4.3.1 "full-stack spec" terminology** means different artifacts for Hamerton vs. global subjects. Needs clarification.

---

## Punch-list for next session (§3 review start)

| # | Item | Status |
|---|---|---|
| 6 | §4.4 rewrite: BL hedging hypothesis | Pending |
| 7 | §4.3.2 Zep temporal-graph framing (F8) | Pending |
| 8 | §4.3.2 Letta retrieval-duplication note (m18) | Pending |
| 9 | §1.3 + §4.3.1 Letta stateful caveats (in-progress; §1.3 half done) | In progress |
| 16 | Appendix E: extended benchmark analysis | Pending |
| 19 | Lu/Jain paper-wide citation conventions | Pending |
| 20 | Update REFERENCE_TABLE.md per §2.4 verification | Pending |

Also tracked implicitly:
- Abstract rewrite (last per plan)
- §3 through §8 review (tomorrow start)
- v8 docx regeneration when needed
- Any further author-pilot expansion
- Name-blind wrong-spec control (F9)
- Differentiated interpretation-only battery (F11)
- Anonymized-vs-named BL spec on low-baseline (F10) — note: resolved by matched-rerun, which confirmed globals use named specs

---

## Voice signals calibrated this session

For continuity through §3+ and eventual abstract rewrite:

- Layman-first opening sentence per finding, followed by technical numbers (applies to findings; not every subsection needs bolded layman sentence).
- No em-dashes in prose. Tables may use em-dash for empty cells but prose uses periods, colons, semicolons, or parentheses.
- **GTM / marketing language avoided.** "Beats" → "exceeds" or "outperforms." Sweep flagged for ongoing enforcement.
- Direct declaratives, parallel structure where natural.
- "Interpretation" not "understanding" in the framing context.
- No meta-framing ("this paper makes rigorous"). Load-bearing claims are declared directly.
- Population of relevance named explicitly (not just "low-baseline subjects").
- References always attributed to primary sources. When the paper's claim is our inference, say so explicitly.
- Benchmark numbers always cited with source + model used; "self-reported" flagged where applicable.
- "Person" in conceptual framing; "user" when AI-deployment context is active; "subject" for the studied figure in methodology.

---

## Open durable-memory updates

The following memory-system / user-facing memory records should be updated based on this session:

- **feedback_no_em_dashes.md** — already exists; confirmed by session work.
- **feedback_no_gtm_language.md** — NEW candidate. Aarik flagged "beats" as too marketing-style. Voice rule extends beyond em-dashes to any marketing-style verbs in paper prose.
- **project_current_state.md** — should be updated: v8 draft exists, §1+§2 locked, §3 review scheduled for next session.
- **project_paper_redline_notes.md** — running list of corrections applied and remaining.

---

## Status at session close

- v6 frozen (em-dash edits aside).
- v7 locked §1 + §2 artifact, superseded by v8.
- v8 draft is the working paper for next session.
- All research reports preserved in `docs/research/`.
- All review annotations preserved in `docs/reviews/s114_paragraph_review.md`.
- Git status: one commit landed (`0da9a7a`), further uncommitted changes from today. Not pushed.

Next session starts §3 Study Design review.

---

## S114 continuation — §3 Study Design progress (through §3.4.1)

The following was locked in the continuation after context compaction:

- §3 opener (content-forward, no reader-addressing)
- §3.1 Representational Accuracy (joint-claim framing, not model-internal)
- §3.2 Subjects (+ Franklin known-figure control, baseline-as-observable-proxy)
- §3.2.1 Pretraining-coverage variance (new subsection; baseline banding)
- §3.3 Pipeline (5-step table, 46 predicates, Hamerton examples, all-MiniLM-L6-v2)
- §3.4 Question Batteries (backward-design procedure, 0.34% leakage disclosed honestly)
- §3.4.1 Circularity Controls (GPT-5.4 independent batteries + non-Anthropic response chain)

### Key corrections surfaced in §3 review

- 47 → 46 predicates. config.py:607 comment stale; grep confirmed 46 in production. Paper-wide sweep (§5.1, §6) flagged as task #25.
- `MiniLM-L6-v2` → `all-MiniLM-L6-v2`. Embedding model ID corrected.
- Franklin batteries were NOT regenerated with GPT-5.4 (grep verified). Control 1 applies to 13 global subjects only.
- Leakage audit added: 2 of 586 (0.34%), both in Franklin legacy battery (Q49, Q56); 0.00% on 14 main-study subjects.
- Name-blind wrong-spec premise was empirically false: specs are already anonymized. 60.6% detection is content-grounded, not an upper bound. Four corrections applied (v8 §1.3, KEY_FINDINGS m20, F9 closed, wrong-spec analysis flagged).
- Letta stateful matched-rerun corrected Ebers Δ from +1.21 → +0.75 and Babur Δ from +0.57 → +0.29 after battery mismatch + anonymization false-premise fixes.

### Pending task table — end of §3.4.1

| # | Item | Status |
|---|---|---|
| 6 | §4.4 rewrite: BL hedging hypothesis (m19 partial contradiction) | Pending |
| 7 | §4.3.2 Zep temporal-graph framing (F8) | Pending |
| 8 | §4.3.2 Letta retrieval-duplication note (m18) | Pending |
| 9 | §1.3 + §4.3.1 Letta stateful caveats (§1.3 done; §4.3.1 pending) | Partial |
| 16 | Appendix E: extended benchmark analysis | Pending |
| 19 | Lu / Jain paper-wide citation conventions | Pending |
| 20 | Update REFERENCE_TABLE.md per §2.4 verification | Pending |
| 23 | §3.7 fractional score interpretation guidance (integer-anchor crossing) | In progress |
| 24 | Update `wrong_spec_detection_analysis.md` per name-blind finding | Pending |
| 25 | 47→46 sweep for §5.1 and §6 | Pending |

### Still to review

- §3.5 Experimental Conditions (next up)
- §3.6 Response Models
- §3.7 Evaluation: LLM-as-Judge with Calibration
- §4 through §8
- Abstract rewrite (last per plan)

### Open items for continuation

- Aarik's detached Letta scale run may still be running; status unchecked.
- Author-pilot expansion (F9 now closed; F11 differentiated interpretation battery remains open).
- v8 docx regeneration is deferred until a larger review chunk is ready.

### Voice rules carried forward

All rules from earlier session continue to apply: no em-dashes in prose, no GTM language (feedback_no_gtm_language.md), layman-first on findings, direct declaratives, no reader-addressing in methodology, "raw data available at..." convention for every experimental mention, primary-source references, named-population framing.

---

## §4 Results — locked outline (S114)

Narrative spine: primary result → mechanism → application → robustness → per-question analysis → architectural convergence → scaling. Every section title is intentionally direct-declarative and maps to a specific finding.

| § | Title | Purpose |
|---|---|---|
| 4.1 | The Cross-Subject Gradient | Primary result: regression slope + low-baseline slice + Franklin anchor |
| 4.2 | Compression: Structure vs. Raw Text | Spec vs. raw corpus, Hamerton + generalization |
| 4.3 | Mechanism: Content, Not Format | Wrong-spec control + hedging + honest refusal |
| 4.4 | Memory-System Composition | 5 systems × 2 configurations, with §4.4.1 Letta stateful observation |
| 4.5 | Robustness and Sensitivity | Tier 2 cross-provider + 5-judge / 7-judge sensitivity |
| 4.6 | Interpretation vs. Recall | Per-question analysis, where the spec helps or hurts |
| 4.7 | Architectural Convergence: Letta Stateful-Agent | Independent validation of the interpretive-structure claim |
| 4.8 | Scaling and Practical Implications | Cost, context, and deployment considerations |

### Title-style commitment (S114 decision)

Paper section headings use direct-declarative framing in line with the voice rules. "Facts Do Not Carry Their Own Significance. People Do." (§5.3 candidate) is the target form; academic-formal replacements would dull the human-AI interaction thread that runs through the paper.

### Hypotheses locked in §1.2 (S114)

Four hypotheses added at the top of §1.2 as the organizing claims:

- **H1.** Specification improves behavioral prediction vs. no context.
- **H2.** Benefit is inversely proportional to pretraining coverage (the gradient).
- **H3.** Content specificity is necessary (wrong-spec control).
- **H4.** Additive to existing memory-system retrieval pipelines.

H1 + H2 → §4.1; H3 → §4.3; H4 → §4.4. Every downstream result maps to one of these.

**H5 added 2026-04-21 evening**: compression efficiency — "A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size." Maps to §4.2.

---

## Title locked — panel-decided (S114)

Paper title changed from "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization" to:

**"Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"**

Decision: 6-provider unanimous panel vote (Gemini Flash, Gemini Pro, Mistral Large, Cerebras Qwen3 235B, GPT-5.4, Claude Opus 4.6). Candidate T2 selected over current T1 which was flagged as overclaiming. Full panel report at `docs/reviews/s114_title_panel_20260421_154300.md`. Title applied across all 9 active files (v8 draft, AGENTS.md, STUDY_MEMORY.md, study-guide.md, FILE_NAMING.md, KEY_FINDINGS.md, PROVENANCE_INDEX.md, top-level README, docs/reviews/README.md).

---

## Methodology change — 5-judge primary panel (S114)

Primary aggregate moved from 7-judge mixed panel (as S113 generated) to 5-judge non-Gemini (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). 7-judge aggregate reported as sensitivity check. §3.7.2 explains the decision.

**Why:** Gemini Pro fails verbatim-match calibration (4.15 where every other calibrated judge scores 5.0) and penalizes padded-correct responses severely. Panel decision made after validity audit flagged Gemini's systematic +1-point inflation.

**Backfills run this session to make the panel consistent:**
- Hamerton: Sonnet + Opus + GPT-4o on 5 spec conditions (595 judge calls)
- Franklin: Sonnet + Opus + GPT-4o + GPT-5.4 on all 5 spec conditions (800 judge calls) plus GPT-4o + GPT-5.4 on C5 baseline (80 more)
- Base Layer on 12 globals: gpt4o + gpt5.4 backfill (rate-limit recovery)
- Plus 2,737 parse-failure rescues across the whole repo

**New canonical numbers (N=14, 5-judge primary, main gradient):**
- Slope: −0.96 [−1.24, −0.67]
- R²: 0.82
- p-value: <0.001 (0.000009)
- Wilcoxon C5 vs C4a: W=11, p=0.007
- Low-baseline (n=9) mean Δ_C4a: +0.89
- Low-baseline positive: 9/9
- All-14 positive: 12/14 (same negatives: Zitkala-Sa, Equiano)
- Per-response anchor-crossing rate (low-baseline): 55.0%

All output at `docs/research/recompute_5judge_primary.md` and `docs/research/s114_low_end_inflation_audit.json`.

---

## §1.2 revisions (S114 evening)

- Five hypotheses block (H1-H5) added after the opening paragraph.
- Primary + secondary outcomes block added at end: mean-score + per-question win rate against baseline.
- Hypothesis-to-section mapping named explicitly.

## §3 revisions (S114 evening)

### §3 opener
- Intertwined-but-separable framing: experimental apparatus + pipeline are two halves of the methodology, both needed to answer the core question.

### §3.7.6 new (Rubric-handling limitations)
- Abstention-vs-wrong-prediction non-distinction audit surfaced honestly (12.0% of responses match abstention patterns; mean score 1.27; 9.4% inflated above 2.0).
- Length-score correlation: r = 0.604 within C5 baseline only, near zero in spec-containing conditions. Verbose hedging in baseline inflates C5 scores.
- Per-judge strictness on abstentions: Sonnet 1.14 (strictest), GPT-5.4 1.17, Haiku 1.29, GPT-4o 1.34, Opus 1.41 (most lenient).
- Direction of bias: true spec-effect gap is likely slightly *larger* than reported, not smaller.

### §3.7 opener
- Recursive-evaluation framing added: response models evaluated by judges (§3.7.1); judges evaluated by calibration (§3.7.2), inter-judge agreement (§3.7.4), and rubric-handling audits (§3.7.6). No single layer treated as ground truth.

## §4.1 locked (S114 evening)

- Layman-first framing. Anchor-crossing table in-place at point of mention.
- Three mechanism-distinct response example callouts: A (Ebers, identity+inference), B (Bernal Diaz, directional correction), C (Seacole, abstention-to-inference). Each with collective-review-identified mechanism and transparent analysis.
- Example C specifically flags the abstention inflation issue in-context.
- Hypotheses H1, H2, H2a (new corollary) named at top.
- Gradient-extremes callout (Hamerton vs Franklin vs Babur).
- Per-subject table grouped by baseline band with color-coding note for PDF.
- Sensitivity-to-Gemini note (summary only; full analysis deferred to §4.5).
- Baseline-inflation note surfaced so readers can interpret the gradient correctly.

### §4.1.1 Franklin
- Locked. 5-judge primary = 3.77 (originally reported at 4.10 using Haiku alone). Spec conditions underperform baseline cleanly.

### §4.1.2 Living-user replication (author)
- Methodology-matched pilot on author's private corpus (50/50 train/heldout split, spec authored from training half only, battery from heldout half only, 40 BP questions).
- **Results (5-judge primary, N=40):** C5=1.03, C2a=2.86, C2c=2.59, C4=2.93, C4a=3.02.
- **Δ_C4a = +2.00 — study's largest lift.** Anchor-crossing rate 75.0%, zero downward.
- Wrong-spec control (C2c, Franklin's spec) lifts +1.56; correct spec lifts +1.84. Partial content filtering consistent with §1.3 mechanism finding.

## §4.2 + §4.2.1 locked (S114 evening)

### §4.2 Compression: Structure vs. Raw Text
- Compression-efficiency framing ("predictive gain per 1,000 tokens of context").
- Multi-subject comparison table with compression ratios (5× on Hamerton, up to 78× on Babur).
- Hamerton and Ebers callouts as boundary and honest-cost examples.
- Deployment framing at close.
- Opus's one-sentence mantra distilled in the opening: "Any structured context lifts behavioral prediction by ~1 point over baseline; the most compressed representation captures the large majority of that gain."

### §4.2.1 Question-Improvement Rate — A Candidate Secondary Reporting Metric
- Framed as win rate against no-context baseline (Chatbot Arena / LMSYS precedent).
- **Spec-alone low-baseline win rate: 70.9%** (249 improve / 49 tie / 53 worsen).
- **Median improvement magnitude = +1.00 points** (a full rubric-anchor category on median).
- Full reporting triplet (rate + worsening rate + median magnitudes).
- Failure modes named: tiny-gain inflation, hidden catastrophic harm, easy-baseline gaming, scale-free illusion of portability. Each with its guard.
- Positioned as secondary reporting metric, not primary benchmark. Panel unanimous on scoping.

---

## Collective reviews run this session (S114)

| Review topic | Providers | Output file |
|---|---|---|
| §4 structure planning | 4 (Gemini Flash/Pro, Mistral, Cerebras) | `_archive/s114_section4_planning_20260421_134857.md` |
| Title panel (T1-T6) | 6 | `_archive/s114_title_panel_20260421_154300.md` |
| §4.1 example analysis (3 response pairs) | 6 | `_archive/s114_example_analysis_20260421_170720.md` |
| §4.2 compression framing | 5 (Cerebras 429) | `_archive/s114_compression_framing_20260421_182523.md` |
| Benchmark metric proposal | 6 | `_archive/s114_benchmark_metric_review_20260421_183432.md` |

---

## Background runs completed this session (S114)

- Hamerton 3-judge backfill (Sonnet, Opus, GPT-4o on spec conditions)
- Franklin 4-judge backfill + Franklin C5 + C2a + C4a (5-judge primary coverage complete)
- Base Layer gpt4o + gpt5.4 backfill on 12 globals (rate-limit recovery)
- Parse-failure backfill: 2,737 rescues across the repo (126 cells completed)
- Clean Author Pilot — full pipeline, training/heldout split, 40 BP questions, 5 conditions, 5-judge panel (~1,500 calls)
- Clean Author Pilot C2c wrong-spec extension (Franklin spec as wrong-spec control)
- Spec-activation analysis (tag citation rate): **78.6% on correct spec, 50% on wrong spec** — strong §4.3 material
- Anchor-crossing analysis (low-baseline 351 questions): 55% upward, 33.3% cross 1→2 anchor
- Low-end inflation validity audit (§3.7.6 + Appendix D material)
- Per-question improvement rate + reporting triplet (§4.2.1 numbers)

## Status at S114 session close (2026-04-21 evening)

- v8 locked: §1 (all), §2 (all), §3 (through §3.7.6), §4.1 (with §4.1.1 Franklin + §4.1.2 Living-user pilot), §4.2 (with §4.2.1 Question-Improvement Rate).
- §4.3 is next up. Spec-activation numbers ready. Three mechanism types identified.
- All backfills complete. 5-judge primary is the canonical aggregate.
- No outstanding decisions blocking §4.3 drafting.

### Pending tasks carried into next session

| # | Item |
|---|---|
| 28 | Figure: per-subject judge-agreement visualization |
| 29 | Author Appendix D: Per-Subject Breakdown |
| 32 | Paper-wide 7→5-judge sweep of §1 and §2 prose |
| 43 | Figure 4.1 + 4.2: gradient scatter + anchor-crossing stacked bar |
| 49 | §8 Future Work: differentiated rubric + length-controlled scoring + benchmark proposal |
| 50 | Appendix D: fold validity audit numbers in |
| Remaining §4 | §4.3 (next) through §4.8 |
| Remaining | §5, §6, §7, §8, Appendix A, B, C, D, E, Abstract |

