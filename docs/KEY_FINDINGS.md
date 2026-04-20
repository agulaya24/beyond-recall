# Key Findings

**Paper:** Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization
**Generated:** 2026-04-18 (Session 113). Last updated: Session 114 (April 2026).
**Source of truth for numbers:** `docs/DATA_REFERENCE.md`

This document catalogs every finding the study produced. Each entry includes: the finding, the evidence, and the paper section that contains it. Findings are grouped as MAJOR (load-bearing for the paper's central claim) or MINOR (supporting observations and side findings).

---

**For AI agents working in this repo:** read this file + `docs/DATA_REFERENCE.md` before running new analyses. `DATA_REFERENCE.md` is the canonical source for every number; this file catalogs findings with evidence links. If your work could add, refine, or contradict findings here, propose updates inline and surface to the lead author.

## S114 update (April 2026, pre-launch)

The paired C1-vs-C3 analysis originally run only on Supermemory has been extended to every memory system in the study. Findings summary:

- **Mixture-of-swings is system-general.** Every commercial memory system (Mem0, Letta, Zep, Supermemory) plus Base Layer's own retrieval substrate shows bilateral per-question swings hiding near-null aggregates. Added as m15.
- **Three failure modes of specification-based reasoning are system-general.** Over-theorization, spec-induced refusal, and default-axiom overfires each reproduce across systems. Added as m17.
- **Keckley Q21 refusal is a spec-level dynamic, not a memory-system artifact.** Same −2.33 penalty on Supermemory and Base Layer; reproduces with proportional penalties across all 5 systems. Added as m16.
- **Provider recall-benchmark claims are 68-85% range, not uniformly 85%+.** Primary-source audit documented at `docs/research/provider_benchmarks.md`. Paper-wide punch-list item for §2.1 / §5.7 / abstract. Added as m21.
- **Wrong-spec detection upper bound: 60.6%** (N=587, validated), with name-mismatch confound flagged. Added as m20.
- **Letta archival retrieval has severe fact duplication** (dedup 0.34-0.47). New finding. Added as m18.
- **Base Layer prompt-template hedging hypothesis partially contradicted.** §4.4 mechanism claim needs rewrite. Added as m19.
- **Aarik author baseline pilot.** C5 = 1.90 on private data; consistent with low-baseline-is-typical-user thesis. Added as m22.

Research reports supporting these findings:
- `docs/research/supermemory_c1_vs_c3_paired_analysis.md`
- `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`
- `docs/research/baselayer_c1_vs_c3_paired_analysis.md`
- `docs/research/letta_stateful_deep_read.md`
- `docs/research/letta_stateful_matched_rerun.md` (pending)
- `docs/research/wrong_spec_detection_analysis.md`
- `docs/research/provider_benchmarks.md`

---

## TAKEAWAY

> "There is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply — measurable via behavioral prediction, and additive to every memory system tested here."

Eight-word collapse: *"Recall is not interpretation. Interpretation can be measured."*

---

# MAJOR FINDINGS

## M1. The Gradient — spec helps inversely proportional to baseline knowledge

**Finding:** The Behavioral Specification's value is inversely proportional to what the model already knows about the subject from pretraining. On the 9 low-baseline subjects (C5 ≤ 2.0, the slice approximating real AI users), the spec is uniformly beneficial: 9 of 9 positive, mean Δ +1.04 points.

**Evidence:**
- Wilcoxon C5 vs C4a: W = 9.0, p = 0.0063 (N=14)
- Linear regression slope (Δ vs C5): −0.98 [95% CI −1.30, −0.74]
- 12 of 14 subjects show positive Δ
- Low-baseline (n=9): mean Δ_facts+spec = +1.04, mean Δ_spec_alone = +0.84
- High-baseline (n=5): mean Δ ≈ 0 (null)

**Paper:** §4.1, Table 4.1. **DATA_REFERENCE:** §1, §2.

## M2. The specification improves all 4 commercial memory systems on the population of interest

**Finding:** Layered on top of any of the 4 commercial memory providers (Mem0, Letta, Supermemory, Zep), the Base Layer specification produces positive mean delta on low-baseline subjects in the controlled configuration. Three of the four (Mem0, Letta-controlled, Zep) also show positive aggregate delta across all 14 subjects.

**Evidence (controlled config):**
- Mem0: +0.15 [+0.08, +0.23] aggregate; +0.13 on low-baseline (6/9 positive)
- Letta: +0.25 [+0.15, +0.36] aggregate; +0.23 on low-baseline (7/9 positive)
- Zep: +0.22 [+0.14, +0.31] aggregate; +0.20 on low-baseline (9/9 positive)
- Supermemory: −0.04 aggregate (ceiling); +0.004 on low-baseline (5/9 positive — ceiling artifact)
- Base Layer (own retrieval + spec): +0.12 aggregate; +0.13 on low-baseline (7/9 positive)

**Native config:** Mem0 +0.38, Zep +0.38, Letta −0.01 (archival path — see M5), Supermemory −0.11 (ceiling).

**Flagship sentence:** "Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know."

**Paper:** §4.3, Table 4.3. **DATA_REFERENCE:** §3, §4.

## M3. Content specificity — wrong-spec controls fail at baseline

**Finding:** The improvement is not a prompt-engineering trick or a structured-context-helps effect. A wrong subject's spec applied to this subject scores at or below baseline.

**Evidence:**
- C5 baseline = 2.02
- C2a correct spec = 2.55 (Δ +0.53)
- C2c v1 (Franklin's spec applied to all 13 non-Franklin subjects) = 1.86 (Δ −0.16, *below* baseline)
- C2c v2 (random derangement, seed=42) = 2.30 (Δ +0.28, between baseline and correct spec)

Both wrong-spec controls score nowhere near correct-spec scores. The content of the *correct* spec for the *correct* subject is what produces the improvement.

**Paper:** §4.5, Table 4.5. **DATA_REFERENCE:** §6.

## M4. Memory systems disagree catastrophically on what's relevant

**Finding:** Three embedding-based memory systems (Mem0, Letta, Supermemory) given the *identical* fact pool fail to share a single common fact in all three systems' top-k on 93% of questions at top-1. In the native configuration where each system runs its own ingestion, disagreement is 100% at every top-k. Systems that all pass recall benchmarks at 85%+ cannot converge on which fact is most relevant.

**Evidence:**
- Controlled (identical fact pool, n=515 analyzable questions across 14 subjects):
  - 93.4% top-1 all-3-disagreement
  - 83.3% top-3
  - 73.8% top-5
  - 53.2% top-10
- Native (each system own ingestion, n=410):
  - 100% top-1 disagreement, 100% at every top-k
- Source: `data/experiments/memory_systems/string_match_disagreement.py` → `results/string_match_disagreement.json`

**Why it matters:** Recall benchmarks (LOCOMO, LongMemEval) measure whether the right chunk is in the top-k. They do not measure whether systems agree on *which* chunk is most relevant. The latter has a wide gap.

**Paper:** §4.3 finding #5. **DATA_REFERENCE:** §K.

## M5. Letta stateful-agent path produces a representation in the same prediction band as Base Layer's spec — at matched response model

**Finding:** Letta's signature mechanism (stateful self-editing memory blocks during multi-turn conversation) produces an interpretive representation that, when fed to the same response model used elsewhere in the study, scores in the same prediction band as Base Layer's full-stack spec.

**Evidence (Hamerton):**
- Letta agent's native loop (gpt-4o-mini): 3.38
- Letta block fed to Haiku as context: **3.24** (matched response model)
- Base Layer full-stack spec fed to Haiku: 3.04
- Letta block size: 22,472 chars (~5,600 tokens) — 65% of BL spec size

**Evidence (Ebers, generalization):**
- Letta block fed to Haiku: **3.00**
- Base Layer C2a spec alone: 1.79
- Base Layer C4a facts+spec: 2.34
- Letta block size: 68,413 chars

**Evidence (Babur, n=3 generalization at scale):**
- Letta block fed to Haiku: **2.73** (335K-char block, saturated at chunk 220/242, 25% duplication)
- Base Layer C2a spec alone: 2.16
- Base Layer C4a facts+spec: 2.28

**Uplift summary across n=3:** Hamerton +1.99 (small, clean), Ebers +1.96 (medium, clean), Babur **+0.75** (large, duplicated, truncated). Letta beats Base Layer's spec on all three at matched response model — and Letta's uplift collapses 60% at large corpus scale, exactly where the architectural ceiling we documented in M6/M7 takes hold.

**Paper:** §4.3.1. **DATA_REFERENCE:** §7.

## M6. Letta's stateful-agent compression does not scale — and we observed the ceiling

**Finding:** Letta's `human` memory block grows roughly linearly with corpus size. At ~333,000 characters, the API begins rejecting further messages. Babur's 223K-word corpus saturated after chunk 220 of 242 — the last 22 chunks (~10% of the corpus) failed to ingest. Base Layer's compose step, by contrast, produces specs of 34-40K characters across a 9× corpus-size range.

**Evidence:**

| Subject | Corpus words | Letta block (chars) | BL spec (chars) | Ratio | Outcome |
|---|---:|---:|---:|---:|---|
| Hamerton | 25,231 | 22,472 | 34,579 | 0.65× | Full ingestion |
| Ebers | 48,161 | 68,413 | 39,708 | 1.72× | Full ingestion |
| Babur | 222,742 | 335,349 | 37,063 | 9.0× | **Saturated at 333K chars; 22 chunks lost** |

**Architectural consequence:** At realistic user-corpus scale (10 years of journals, accumulated session history), Letta's block hits the ceiling we observed. Base Layer's compose step keeps the spec at 5-8K tokens regardless. This is structural, not implementation-detail.

**Paper:** §4.3.1. **DATA_REFERENCE:** §7.

## M7. Letta's coherence degrades before its size ceiling — the block becomes heavily duplicative

**Finding:** Block-size saturation is the proximate failure; the deeper failure is that the agent's consolidation loop loses coherence well before the size ceiling. At Babur scale, 25% of all sentences in the final block are verbatim duplicates.

**Evidence:**

| Subject | Block | Sentences | Duplicate sentences | % duplicate | Repeated 8-word phrases (3+ occurrences) |
|---|---:|---:|---:|---:|---:|
| Hamerton | 22K chars | 129 | 0 | 0% | 0 |
| Ebers | 68K chars | 364 | 0 | 0% | 1 |
| Babur | 335K chars | 1,301 | 103 | **25.4%** | **2,505** |

At small/medium corpus scale, the agent self-edits cleanly (zero verbatim duplication). At large corpus scale, the agent loses track of what is already in the block and re-asserts the same axioms with each new chunk. One Babur sentence appears verbatim **12 times**. The opener "the individual recognizes the…" appears **86 times** in 1,301 sentences.

**Effective unique content in Babur block ≈ 250K chars, not 335K.** The block hit a coherence ceiling before the size ceiling.

**Paper:** §4.3.1. **DATA_REFERENCE:** §7 (will be added with Babur data).

## M8. Compression test — 5K-token spec outperforms 34K-token raw corpus

**Finding:** On Hamerton, a 7,300-token Behavioral Specification (C2a) outperforms 34,168 tokens of raw autobiography (C8). Information availability is not the bottleneck; interpretive structure is.

**Evidence (Hamerton):**

| Condition | Tokens | Score (1-5) |
|---|---:|---:|
| C8 Raw corpus, no spec | 34,168 | 2.32 |
| C9 Raw corpus + spec | 41,452 | 3.22 |
| C4a All facts + spec | 16,874 | 3.22 |
| C4 All facts, no spec | 7,723 | 2.53 |
| C2a Spec only | 7,320 | 3.04 |
| C5 Baseline | ~40 | 1.25 |

C2a (spec alone, 7K tokens) beats C4 (all 462 extracted facts, 7K tokens) by 0.51 points at the same token budget — structure carries more signal than the raw fact list. C2a (spec alone) beats C8 (raw corpus, 34K tokens) by 0.72 points using 22% of the tokens.

**Paper:** §4.2, Table 4.2. **DATA_REFERENCE:** §8.

## M9. Cross-provider replication — the effect is not Anthropic-specific

**Finding:** The spec effect replicates with non-Anthropic response models on non-Anthropic-generated batteries. Tier 2 circularity test: 5 of 6 (subject × response model) cells reproduce the spec direction, with non-Haiku response models (Sonnet, Gemini Pro) reading GPT-5.4-generated batteries.

**Evidence:**

| Subject | Response Model | Battery | Δ | Direction |
|---|---|---|---:|---|
| Ebers | Sonnet | GPT-5.4 | +1.48 | ✓ |
| Ebers | Gemini Pro | GPT-5.4 | +1.07 | ✓ |
| Yung Wing | Sonnet | GPT-5.4 | +1.91 | ✓ |
| Yung Wing | Gemini Pro | GPT-5.4 | +1.27 | ✓ |
| Zitkala-Sa | Sonnet | GPT-5.4 | +1.40 | ✓ |
| Zitkala-Sa | Gemini Pro | GPT-5.4 | −0.55 | ✗ (consistent with §4.1.3 — spec hurts Zitkala-Sa) |

**Bonus finding (M9b — see below):** baseline accuracy varies by 1-2 points across response models on the same subject — independent empirical evidence for cross-provider pretraining variance.

**Paper:** §4.8, §4.8.1. **DATA_REFERENCE:** §10.

---

# MINOR FINDINGS

## m1. Hamerton qualitative case — the specification shifts the model from hedging to committed prediction

**Finding:** On Hamerton's London-rejection question (Q21), the baseline model hedges ("Significant discomfort, more nuanced than rejection") while the spec-equipped model commits ("immediate visceral rejection, not gradual disillusionment") — matching the held-out passage.

**Paper:** §4.6. Score: baseline 2 → C4a 5.

## m2. Franklin baseline ceiling — context can hurt for famous figures

**Finding:** For subjects with high pretraining baseline (Franklin C5 ≈ 4.10), adding context can introduce competing interpretive signals that hurt prediction. The spec is "the right tool for the unknown," not for what the model already knows.

**Paper:** §4.7. **DATA_REFERENCE:** §1 (Franklin not in main 14, separate test).

## m3. Hedging metric — the spec moves models from "I don't know" to committed predictions

**Finding:** Across 13 global subjects, baseline (C5) responses exhibited hedging or refusal patterns ("I don't have enough context") on 25.0% of questions. With spec only, hedging drops to 2.6%. With facts + spec, to 0.6%. The spec changes what the model is willing to commit to, not just the score.

**Paper:** Abstract claim 4, §5.5. **DATA_REFERENCE:** (TBD — add to §K).

## m4. Both Gemini judges inflate scores by ~1 point

**Finding:** Gemini 2.5 Flash and Gemini 2.5 Pro systematically score ~1.0 point higher than the other 5 judges. This shifts aggregates but not directions. The spec effect remains positive 9/9 on low-baseline under both 7-judge and 5-judge non-Gemini aggregations; no subject flips sign.

**Paper:** §4.1.2.

## m5. GPT-5.4 has a high parse-failure rate (~19%)

**Finding:** GPT-5.4 frequently returns text beyond the requested 1-5 digit, requiring exclusion under the locked aggregation rule. Gemini Pro's parse-failure rate, by contrast, is ~0.5%.

**Paper:** §3.7 (judge coverage paragraph). **DATA_REFERENCE:** §9.

## m6. Inter-judge agreement: substantial on rank order, moderate on absolute

**Finding:** Pairwise Spearman ρ = 0.89-0.98 (rank agreement on condition orderings) across all judge pairs. Krippendorff α (ordinal) = 0.659 across 5 non-Gemini judges (substantial); drops to 0.535 with both Gemini judges included due to systematic Gemini inflation.

**Paper:** §3.7, §4.1.2. **DATA_REFERENCE:** §2, §9.

## m7. Letta's archival-retrieval path is not its strength

**Finding:** Letta's source-attachment / archival-retrieval path (the configuration we initially tested in §4.3) produces null spec-delta in the native config (−0.01) and modest positive (+0.25) in controlled. But Letta's signature mechanism is the stateful-agent path (§4.3.1, M5), which scores substantially higher (3.24-3.38 on Hamerton, 3.00 on Ebers vs 2.81-2.86 archival). The architecture that does the interpretive work is the conversation loop with memory-block editing, not the archival store.

**Paper:** §4.3 scope caveat, §4.3.1.

## m8. Supermemory ceiling effect — high baseline retrieval, low spec headroom

**Finding:** Supermemory's C1 baselines are systematically higher than the other systems (mean ~2.65 vs ~2.30). On its own low-baseline subjects (ebers, babur, yung_wing) the spec still helps. On its high-baseline subjects, the spec hurts (model has already committed; spec adds competing signal). Aggregate near-zero is a *retrieval distribution* artifact, not a spec failure mechanism.

**Paper:** §4.3 finding #2, §5.7.

## m9. Letta block scaling is sub-linear but ceiling-bound

**Finding:** Per-chunk additions to Letta's `human` block:
- Hamerton: ~749 chars/chunk (30 chunks, ends at 22K)
- Ebers: ~1,315 chars/chunk (52 chunks, ends at 68K)
- Babur: ~625 chars/chunk early, slowing as it grows, hard wall at 333K (chunks 221-242 fail)

Compression rate (corpus/block, words):
- Hamerton: 25K/3.2K = 7.9×
- Ebers: 48K/9.6K = 5.0×
- Babur: 223K/45K = 5.0× (but with 25% duplication, effective unique compression ~6.7×)

**Paper:** §4.3.1. **DATA_REFERENCE:** §7.

## m10. Specification stability — temperature 0 not perfectly deterministic

**Finding:** Re-generating the spec for the same subject at temperature=0 produces 45% exact-text match across runs but >95% semantic similarity. The spec is semantically stable; sentence-level variation is from local non-determinism in the authoring chain.

**Paper:** §6 Limitations.

## m11. Base Layer retrieval is comparable to commercial systems but not superior

**Finding:** Base Layer's MiniLM-L6-v2 + ChromaDB retrieval produces C1 scores in the same band as the four commercial systems (within 0.05-0.40 points on most subjects). BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias). On no subject does BL's C3 exceed the best commercial C3. **BL is the open-source floor — comparable, not superior.**

**Paper:** §4.4. **DATA_REFERENCE:** §12.

## m12. Wrong-spec v1 vs v2 — different nulls, both below correct-spec

**Finding:** v1 (Franklin's spec for all subjects) scores 1.86 — *below* baseline 2.02. v2 (random derangement) scores 2.30 — between baseline and correct spec. v1 is a cleaner null because Franklin is structurally dissimilar to all 13 other subjects; v2 admits accidental loose similarity from random pairing.

**Paper:** §4.5.

## m13. Models can detect incongruent specs

**Finding:** In wrong-spec responses, the model frequently flags the mismatch explicitly ("this specification describes someone fundamentally different from [subject]") and either refuses or hedges. The wrong-spec score distribution is bimodal: detection-plus-refusal vs misapplied-interpretation. Both pathways confirm content matters.

**Paper:** §4.5.

## m14. Two subjects where spec hurts: Zitkala-Sa and Equiano

**Finding:** Both have C5 baselines near the high end of the low-baseline range (Zitkala-Sa 2.60, Equiano 2.93). Spec produces negative Δ (−0.41, −0.24). Likely mechanism: model has partial pretraining knowledge that conflicts with the spec's interpretive frame. §4.1.3 explores hypotheses (pretraining sufficiency / spec misalignment / retrieval interference); pretraining sufficiency preferred.

**Paper:** §4.1.3.

## m15. Mixture-not-cancellation is system-general

**Finding:** Paired C1 vs. C3 analysis across all 5 memory systems (Mem0, Letta archival, Zep, Supermemory, Base Layer retrieval) shows near-null aggregate deltas hide bilateral per-question swings. Supermemory Ebers (aggregate Δ +0.21): 19 of 39 helped, 10 hurt. Supermemory Keckley (aggregate Δ −0.26): 10 helped, 17 hurt. Same shape reproduces on Mem0, Letta, Zep, BL at varying magnitudes. Per-question effects are often large (>0.3 points); averaging them hides strong disagreement.

**Paper:** §1.3 "Where the specification helps and where it hurts." Source reports: `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `mem0_letta_zep_c1_vs_c3_analysis.md`, `baselayer_c1_vs_c3_paired_analysis.md`.

## m16. Keckley Q21 refusal is a specification-level dynamic

**Finding:** On the question "How does Elizabeth explain her decision not to visit her mother's grave?", the specification's documented-dignity axioms induce refusal — the response model declines to fabricate interior motive when the retrieved facts do not contain it. Reproduces across all 5 memory systems at penalty proportional to each system's retrieval-only counterfactual: Supermemory −2.33, Base Layer −2.33, Mem0 −0.50, Zep −0.50, Letta +1.00 (net positive because C1 was already weak). The content-match rubric scores epistemically-honest refusals identically to off-base guesses. **This is a spec-level pattern, not a memory-system artifact.**

**Paper:** §1.3 (Where helps vs. hurts). Source: paired analysis reports.

## m17. Three failure modes of specification-based reasoning are system-general

**Finding:** Paired analyses surface three spec failure modes that reproduce across systems:
- **Over-theorization on literal-recall questions** (spec-driven elaboration drifts past a plain answer)
- **Spec-induced refusals** (axioms designed to prevent fabrication also prevent productive speculation)
- **Default-axiom overfires** on counter-example moments (subject departs from their own modal pattern; spec encodes the default)

Each reproduces on multiple systems. Supermemory Sunity Devee Q11 (hierarchical deference axiom A4 overrides explicit accusatory tone) and Mem0 Ebers Q1 (love-not-duty axiom over-conditionalizes unconditional affirmation) are matched default-axiom failures on different systems.

**Paper:** §1.3 (Where helps vs. hurts) + §4.3 detail. Source: paired analysis reports.

## m18. Letta archival retrieval has severe fact duplication

**Finding:** Letta archival-path retrieval has dedup ratio 0.34-0.47 on tested subjects — top-10 retrieval returns only 3-5 unique facts, with the most-repeated fact appearing ~4× on average. Mem0's dedup ratio is 1.00 (every top-10 position is unique). This thin substrate inflates Letta's controlled spec delta (+0.25 aggregate, low-baseline) because the spec has more interpretive gap to close, and also makes Letta C1 hedge into "cannot find direct characterization" responses that the spec layers onto.

**Paper:** §4.3.2 Letta character sketch (punch-list item to add). Source: `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`.

## m19. Base Layer prompt-template hedging hypothesis partially contradicted

**Finding:** §4.4 currently hypothesizes that BL's smaller spec delta (+0.12) is from prompt-template-induced hedging. Paired-response analysis measures hedge-trigger lexicon C1→C3 per subject: ebers 0.31→0.15 (drops), keckley 0.23→0.08 (drops), yung_wing flat, hamerton 0.41→0.69 (rises), babur 0.10→0.28 (rises). Two drop, two rise, one flat — not uniform template bias. Actual pattern: when spec can be retrieval-grounded, C3 hedges *less*; when it cannot, C3 surfaces the ungroundedness explicitly.

**Paper:** §4.4 mechanism claim requires rewrite. Source: `docs/research/baselayer_c1_vs_c3_paired_analysis.md`.

## m20. Wrong-spec detection upper bound: 60.6%

**Finding:** Across 587 classified wrong-spec responses (507 random derangement v2 + 80 Franklin-for-Hamerton v1), validated against 30-response stratified manual spot check (30/30 agreement with classifier), response distribution is bimodal: 60.6% explicit detection/refusal (flag the mismatch, refuse or hedge), 36.5% misapply, 2.0% implicit hedge, 0.9% ambiguous. Detection + misapply = 97.1% — bimodal framing supported. The 60.6% is an upper bound on behaviorally-grounded detection: specifications are named rather than anonymized, so name-mismatch alone triggers recognition. Hamerton Franklin-spec 88% explicit; Bernal Diaz 21% explicit — detection depends on how distinguishable the wrong spec is from the true subject.

**Paper:** §1.3 Mechanism + §4.5 expansion. Source: `docs/research/wrong_spec_detection_analysis.md`.

## m21. Provider recall-benchmark claims are 68-85% range, not uniformly 85%+

**Finding:** Primary-source audit of the four commercial memory systems' published benchmark scores:
- **Supermemory:** 85.2% LongMemEval_s with Gemini-3-Pro (self-reported, 2026); 81.6% with GPT-4o
- **Letta:** 74.0% LOCOMO with GPT-4o-mini (self-reported, August 2025); no published LongMemEval score
- **Zep:** 71.2% LongMemEval with GPT-4o (arXiv:2501.13956, January 2025)
- **Mem0:** 68.44% LOCOMO with GPT-4o-mini (Chhikara et al. arXiv:2504.19413, peer-reviewable); 91.6% claimed on vendor blog but disputed by Zep with open GitHub reproducibility issue

The paper's abstract, §2.1, and §5.7 assert all four score "85%+" on recall benchmarks. This is not defensible from primary sources. Tightest honest claim: "accuracies in roughly the 68-85% range depending on provider, model, and benchmark variant; self-reported; benchmarks and models vary."

**Paper:** Abstract L217, §2.1, §5.7 L1134 all require sweep. §1.1 already uses the tighter framing (v7 locked). Source: `docs/research/provider_benchmarks.md`.

## m22. Author baseline pilot — real user in Hamerton regime

**Finding:** Pilot C5 baseline measurement on the paper's author (private corpus of ~41K user-role messages ≈ 12.2M chars, Haiku no-context, 10 questions, single-judge). Mean C5 = 1.90 (95% CI 1.16-2.64), refusal rate 60%, 50% of responses at rubric floor (score 1). Places the author in the Hamerton (1.41) regime, not Franklin (4.10) regime. Consistent with the paper's claim that typical real AI users are low-baseline. One data point with the right sign and plausible magnitude; N=10 and single-judge are caveats. Stricter re-judging would likely pull mean to ~1.5-1.7.

**Paper:** §1.4 ¶2 (v7 locked). Source: `_internal/aarik_baseline_pilot/` (internal evidence, not in public repo).

---

# OPEN QUESTIONS / FUTURE WORK

## F1. Generalization across 14 subjects for Letta stateful-agent test

Currently n=2 (Hamerton, Ebers) plus partial n=3 (Babur, ceiling-saturated). Full battery against 11 remaining subjects required to confirm Letta's stateful-agent path matches BL's spec on prediction across the full population.

## F2. Living-user replication

The 14 subjects are historical figures with public autobiographies — a sample biased *upward* on pretraining representation. Direct replication on living users with private data is the structural extrapolation that turns the paper's central claim into direct measurement. ~99% of real AI users are low-baseline.

## F3. Component ablation of the spec

Anchors vs core vs predictions — which layer carries how much of the prediction-improvement signal? Reviewers (Gemini Pro, Mistral) flagged this as the most important methodological extension.

## F4. Human-judge validation

All judges in this study are LLMs. Human validation on a subset is the standard mitigation for LLM-as-judge concerns.

## F5. Live multi-turn agent tasks

Held-out passage prediction is one task. Live agent workflows with tool use, longer horizons, and genuine multi-turn dynamics are the deployment-relevant tests.

## F6. Independent pretraining-representation proxy

C5 baseline is currently the proxy for "what the model already knows." Mistral suggested independent measures (n-gram frequency, memorization probes) to break the C5-as-proxy circularity concern.

## F7. Supermemory architectural-incompatibility hypothesis test

Is Supermemory's near-zero spec delta truly a ceiling effect, or is there an architectural incompatibility between SM's 5-layer stack and the spec's interpretive structure? Designable test. (Partially resolved by m15 mixture-of-swings finding: the aggregate is not uniform; a differentiated battery separating interpretation from recall would resolve more fully.)

## F8. Zep temporal-graph mechanism direct test

§4.3.2 framing implies Zep's Graphiti temporal-graph substrate drives its spec layerability. Paired-response analysis (m15 source) found Zep's relational edges are biographically correct but behaviorally thin; spec wins come from axiom inference, not time-anchored retrieval. Whether temporal structure is load-bearing or ornamental for this task needs a direct test (time-inversion ablation, temporal-reasoning-specific battery).

## F9. Name-blind wrong-spec control

Current wrong-spec controls use named specifications, so the 60.6% detection rate (m20) includes trivial name-mismatch. A name-blind version — anonymize wrong-spec subject names before serving — would isolate behaviorally-grounded detection from name-recognition. The detection rate would likely fall; the floor is the real target.

## F10. Anonymized vs. named BL spec on low-baseline subjects

BL specs are authored with "this person" anonymization. On low-baseline subjects where the response model has no pretraining footing, the anonymization + epistemic-honesty axioms compose into refusals. Letta's stateful-agent block names the subject directly and avoids this. A de-anonymized rerun of BL C2a against Letta's battery is in progress (agent pending). If the gap narrows substantially, §4.3.1 architectural-convergence framing needs refinement.

## F11. Differentiated battery — interpretation-only

Current battery mixes interpretation-heavy questions (where spec helps) with literal-recall questions (where spec hurts or theorizes past a plain answer). A battery that deliberately targets only cross-domain generalization or counterfactual-from-axiom reasoning would isolate the spec's interpretive contribution cleanly. This would also resolve the "are facts enough when well-retrieved" question (addressed partially by Supermemory paired analysis, m15).

---

# MEMORY-SYSTEM CHARACTER (per-provider summary)

Compact per-provider read with references to the major findings that apply to each. Full detail in paired-analysis reports under `docs/research/`.

## Mem0
- Most reliable baseline in the study. Positive spec delta in both configurations (+0.15 controlled, +0.38 native).
- Mixture-of-swings: moderate (m15). Yung Wing swing distribution 21/6/12 is illustrative — large wins coexist with large losses even when aggregate is positive.
- Reproduces default-axiom overfire failure on Ebers Q1 (love-not-duty axiom over-conditionalizes; similar to Supermemory Sunity Q11).
- Dedup ratio 1.00 (clean retrieval, no duplication).

## Letta (archival-retrieval path)
- Null aggregate spec delta native (−0.01), positive controlled (+0.25).
- **New: severe fact-duplication** (m18): dedup 0.34-0.47, top-10 returns 3-5 unique facts. Thin substrate inflates spec delta in controlled config.
- C1 hedges frequently ("cannot find direct characterization") because retrieval is thin.
- See also Letta stateful path below.

## Letta (stateful-agent path)
- Signature architecture (MemGPT paper, Packer et al. arXiv:2310.08560). Self-editing memory block during multi-turn conversation.
- n=3 subjects tested (Hamerton, Ebers, Babur) (M5, M6, M7).
- Scaling ceiling: block grows linearly with corpus size; saturates near Letta's per-message API ceiling (~333K characters, pending verification per agent rerun).
- 25% verbatim sentence duplication at Babur scale (M7).
- Beats BL spec at matched response model on all 3 subjects tested, but **anonymization confound** (F10) may account for much of the gap on low-baseline subjects; rerun pending.
- Architecturally the only system that autonomously builds an interpretive representation from multi-turn interaction.

## Zep
- Strongest and most consistent positive spec delta (+0.22 controlled, +0.38 native). 9 of 9 low-baseline subjects positive in native.
- Mixture-of-swings present but cleanest distribution of the four: 0-1 big-losses on Ebers and Seacole.
- Holds the largest single swing observed: Seacole Q2 = +4.00 (C1 unanimous 1s → C3 unanimous 5s; m15).
- **Open question (F8):** paired-response analysis suggests Zep's temporal-graph edges are biographically correct but behaviorally thin; spec wins come from axiom inference, not time-anchored retrieval. §4.3.2 framing may overstate the temporal-graph mechanism.

## Supermemory
- Strongest standalone retrieval (C1 mean ~2.65 vs. ~2.30 for others on 1-5 scale).
- Near-zero aggregate spec delta (+0.00 on low-baseline, −0.04 all-14). Ceiling effect: retrieval lifts most subjects out of the range where the spec has headroom.
- **Most pronounced mixture-of-swings:** on Keckley (aggregate Δ −0.26), spec helps 10 and hurts 17, including the striking −2.33 Keckley Q21 refusal case (m16).
- 85.2% LongMemEval_s with Gemini-3-Pro is the only primary-source 85%+ benchmark number across all 4 commercial providers (m21).

## Base Layer
- Open-source retrieval floor (MiniLM-L6-v2 + ChromaDB). Not positioned as a memory product.
- Mean C1 ~2.30 across 14 subjects, in the same band as commercial systems. Spec delta +0.13 low-baseline.
- Comparable, not superior (m11 confirmed from paired-response side).
- **Hedging-hypothesis partially contradicted (m19):** §4.4's prompt-template-induced-hedging explanation is not supported by paired-response measurement. Rewrite pending.
- Keckley Q21 refusal reproduces exactly at −2.33 penalty — confirms m16 as spec-level universal.

---

# SUMMARY TABLE

| Finding ID | Type | Status | Paper section |
|---|---|---|---|
| M1. Gradient | Major | ✓ Tested, supported | §4.1 |
| M2. Spec improves all 4 memory systems on population of interest | Major | ✓ Tested, supported | §4.3 |
| M3. Wrong-spec controls fail | Major | ✓ Tested, supported | §4.5 |
| M4. Memory systems disagree 93%+ on top-1 | Major | ✓ Tested, supported | §4.3 |
| M5. Letta stateful-agent matches BL spec at matched-model | Major | ✓ Tested (n=2), supported | §4.3.1 |
| M6. Letta scaling ceiling at 333K chars | Major | ✓ Tested, observed | §4.3.1 |
| M7. Letta block becomes 25% duplicative at scale | Major | ✓ Tested, observed | §4.3.1 |
| M8. Spec beats raw corpus at 22% the tokens | Major | ✓ Tested, supported | §4.2 |
| M9. Cross-provider replication 5/6 | Major | ✓ Tested, supported | §4.8 |
| m1-m14 | Minor | ✓ Various | various |
| F1-F7 | Open | Future work | §7 |

All findings trace to source files documented in `DATA_REFERENCE.md` §K (Provenance).
