# Study Memory — "Beyond Recall" Experiment Only

Persistent memory for agents/sessions working on the "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization" study. Items here are scoped to this experiment only — **not** the broader Base Layer project memory.

**Source of truth for every number:** `docs/DATA_REFERENCE.md`. Resolve conflicts in favor of that file.

**Read this before:** any analysis, any paper edit, any new run, any data discussion.

---

## STUDY-CRITICAL CONSTANTS

- **N = 14 subjects** (13 global subjects + Hamerton). Public-domain autobiographies, all pre-1940.
- **Battery: 39-40 behavioral-prediction questions per subject** (varies slightly per subject; Babur=40, others=39)
- **Judge panel = 7 judges** (Haiku 4.5, Sonnet 4.6, Opus 4.6 or 4.7 — verify, GPT-4o, GPT-5.4, Gemini 2.5 Flash, Gemini 2.5 Pro)
- **Coverage caveat:** Gemini 2.5 Pro ran on Hamerton + Tier 2 + wrong-spec v2 only — global subjects' main gradient was judged by 6 judges.
- **GPT-5.4 has ~19% parse-failure rate** (returns text beyond the 1-5 digit). Gemini Pro ~0.5% parse failures.
- **Gemini judges (both) inflate by ~1 point** vs the 5-judge non-Gemini panel. Always report both 7-judge and 5-judge non-Gemini means for headline claims.

## ANALYSIS PLAN LOCK (immutable, pre-registered)

`docs/ANALYSIS_PLAN_LOCK.md` was committed before final analysis runs. Critical commitments:

- **Gradient is reported as a continuous relationship.** Linear regression (slope + 95% CI) replaces the dropped "~2.4 threshold" language. **Do not introduce post-hoc thresholds for primary results.** If the paper currently uses a "C5 ≤ 2.0 / 9 of 9" framing, that is a sensitivity analysis, not the headline.
- **Locked aggregation rule:** within each judge, mean across questions for each (subject, condition) cell; mean across judges; unit of inference is subject. Do not change.
- **Wilcoxon signed-rank** is the primary inference test, not t-tests.
- **Bootstrap 95% CIs** on memory-system deltas; do not substitute parametric CIs without re-running analysis.
- **Wrong-spec v1 = Franklin-for-all-13-non-Franklin**; **v2 = random derangement seed=42.** v1 is the cleaner null; v2 is a noisier null.

## CONDITION NAMING (memorize these)

- **C5_baseline** — no memory, no spec; pretraining baseline
- **C2a_full_spec** — Base Layer full-stack spec served as context, no facts retrieval
- **C2c_wrong_spec** — wrong-spec control (v1 Franklin / v2 derangement)
- **C4_factdump** — all extracted facts in context, no spec
- **C4a_full_facts_plus_spec** — all facts + spec
- **C8_raw_corpus** — raw training corpus in context, no spec
- **C9_raw_corpus_plus_spec** — raw training corpus + spec
- **C1_<system>** — memory system retrieval only (e.g., C1_mem0, C1_zep, C1_baselayer)
- **C3_<system>** — memory system retrieval + spec (e.g., C3_letta, C3_supermemory)
- **`_fp` suffix** = native (full-pipeline) configuration; absence = controlled config (identical fact pool)
- **C_letta_memory_haiku** — matched-response-model test (Haiku reading Letta's stateful-agent block as system prompt)
- **C_letta_stateful** — Letta's native stateful-agent loop (gpt-4o-mini reasoning over its own self-edited block)

## DATA INTEGRITY — VERIFIED CHECKS

- **Train/test split is honored for all 3 stateful-agent test subjects.**
  - Hamerton: 0/39 held-out passages appear in training. CLEAN.
  - Ebers: 0/40 held-out passages appear in training. CLEAN.
  - Babur: 1/40 (Q26) — 52-character fragment ("some had come in submissive and accepting my service") appears once in training due to corpus-internal repetition. Not test-set leakage.
- **No held-out passage was ever fed to a response model.** Held-out passages go ONLY to judges.
- **Letta stateful-agent test was fed `training.txt` only**, never `heldout.txt`. Verified by inspection of `run_letta_stateful_test.py` `load_training_text()`.

## ARCHITECTURAL FRAMING (load-bearing — do not collapse)

- **Base Layer is NOT a memory provider.** It is a behavioral-specification layer that layers on top of any memory system. The MiniLM + ChromaDB included in the benchmark is a zero-cost local retrieval substrate, not a competitive memory product.
- **Base Layer does NOT outperform memory providers in general.** BL retrieval is comparable-not-superior. BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias).
- **Flagship sentence (use verbatim or close paraphrase):** "Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know."
- **Paper §1.1 framing:** "Recall Is Not Interpretation. Interpretation Can Be Measured." (Note: "interpretation" not "understanding" — the latter triggers reviewer skepticism.)
- **99% of real AI users are low-baseline** (model has negligible pretraining representation of their personal behavior). The low-baseline slice in the study is the operationally relevant population.

## KEY NUMBERS (canonical — match DATA_REFERENCE.md)

- **Wilcoxon C5 vs C4a:** W = 9.0, p = 0.0063 (N=14)
- **Regression slope (Δ vs C5):** −0.98 [95% CI −1.30, −0.74]
- **Krippendorff α:** 0.535 (all 7 judges) / 0.659 (5 non-Gemini)
- **All-14 mean Δ_facts+spec:** +0.67
- **Low-baseline mean Δ_facts+spec:** +1.04 (sensitivity analysis, not headline)
- **Letta stateful matched-model on Hamerton:** 3.24 (Haiku + 22K-char block) vs BL C2a 3.04
- **Letta stateful on Ebers:** 3.00 (Haiku + 68K-char block) vs BL C2a 1.79
- **Letta stateful on Babur:** 2.73 (Haiku + 335K-char block, 25% duplicated, saturated at chunk 220/242) vs BL C2a 2.16
- **Memory-system aggregate spec deltas (controlled):** Mem0 +0.15, Letta +0.25, Zep +0.22, Supermemory −0.04, Base Layer +0.12
- **Retrieval disagreement (controlled, all-3 disagreement):** 93.4% top-1, 83.3% top-3, 73.8% top-5, 53.2% top-10 (n=515 questions)
- **Retrieval disagreement (native):** 100% at every top-k (n=410)
- **Letta block duplication at scale:** Hamerton 0%, Ebers 0%, Babur 25.4%

## MEMORY-SYSTEM CHARACTER (one line each)

- **Mem0** — most reliable baseline; positive in both configs (+0.15 ctrl / +0.38 native); no surprises.
- **Letta** — most architecturally ambitious; native archival path null; stateful-agent path matches BL spec at small/medium scale; collapses at large scale (333K char ceiling).
- **Zep** — strongest aggregate spec delta and most consistent (9/9 low-baseline native positive); Graphiti temporal graph layers cleanly under spec.
- **Supermemory** — strongest standalone retrieval; near-zero spec delta due to ceiling effect (high baseline leaves less headroom); free tier limited ingestion for 4/14 subjects.
- **Base Layer** — open-source spec layer + zero-cost local retrieval floor; not a memory provider.

## METHODOLOGY GOTCHAS — DO NOT REPEAT

- **brief-only vs full-stack spec confusion (S110→S113).** Original Tier 2 and wrong-spec scripts loaded `spec.md` (~900 words brief only) instead of full 5-layer stack from `identity_layers/` (~5000 words). Always use full-stack spec — load anchors_v4.md + core_v4.md + predictions_v4.md + brief_v5_clean.md with "## Injectable Block" markers.
- **Race conditions on parallel pipeline runs.** Background scripts kept writing to target paths after backups. **Kill old processes (don't just rename); delete files before relaunch; confirm prior subprocesses completed.**
- **GPT-5.4 model ID.** Use `gpt-5.4` (dot), not `gpt-5-4` (dash).
- **Letta archival vs stateful-agent path are fundamentally different.** "Letta native" config we tested in §4.3 used the archival-retrieval path (source attachment). The stateful-agent path requires multi-turn conversation with self-editing (`core_memory_append/replace`). Test scripts for the stateful path are at `run_letta_stateful_test.py` + `run_letta_memory_as_context.py`.
- **Data contamination check is not optional.** Before reporting any matched-model score, verify training.txt does not contain held-out passages.

## KNOWN OPEN ITEMS (as of 2026-04-18, S113)

- Letta stateful-agent generalization across all 14 subjects (currently n=3: Hamerton, Ebers, Babur with scaling ceiling)
- Living-user replication (the structural extrapolation that turns the paper from "existence proof" to "directly measured")
- Component ablation of the spec (anchors vs core vs predictions)
- Human-judge validation on a subset
- Independent pretraining-representation proxy (current C5-as-proxy has circularity concern flagged by Gemini Pro and Mistral in Round 2 review)

## REVIEW HISTORY

- Round 1: Mistral Large + Cerebras Qwen3 235B (2026-04-14)
- Round 2: 4 free providers (Gemini Pro, Mistral Large, Cerebras Qwen3, Groq) (2026-04-18)
- Collective consultations: positioning + takeaway + data-first review across Aarik's curated specs (Galef, Askell, Scott Alexander, Gwern, patio11, Matuschak)
- Pending: Round 3 paper review on the post-S113 draft (planned overnight 2026-04-18)

## LAUNCH CONTEXT

- **Target launch: Tuesday 2026-04-21**
- Paper draft: `docs/beyond_recall_v6_draft.md`
- Public repo: this repo, Apache 2.0
- Author: Aarik Gulaya, Base Layer (one-person operation, non-PhD, unfunded)
- Phase 1 launch: blog + Reddit + founder emails (no arXiv required)
- Phase 2 launch: HN + researcher emails (after arXiv submission and endorsement)

## VOICE / FRAMING DISCIPLINE

- Direct declaratives, values-loaded, parallel structure
- "Interpretation" not "understanding" in the paper context
- Continuous gradient (slope) is the headline; threshold/9-of-9 is sensitivity
- Lead with what the data supports; do not lead with what BL "beats"
- Acknowledge limitations upfront (N=14, known subjects, Anthropic-family pipeline, LLM-as-judge); these are credibility assets
- Position Base Layer as the *referee* who introduced a new axis, not a competitor on the existing axis
- "Recall is not interpretation. Interpretation can be measured." is the 8-word collapse — use as social-media hook, not as paper's load-bearing sentence
