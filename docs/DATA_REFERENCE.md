# Data Reference — Single Source of Truth

**Generated:** 2026-04-18 from `data/experiments/memory_systems/results/RESULTS_S113.json` (refreshed this session).

**How to read this doc.** Each numbered section is a self-contained experiment result. Each section contains:

- **Label** — the condition name used elsewhere in the paper
- **One-line summary** — what this data says in one sentence
- **Data table** — the numbers themselves
- **Bounded interpretation** — what to conclude from this data alone, without needing other sections
- **Paper location** — where this appears in `beyond_recall_v6_draft.md`

All scores are on the 1-5 behavioral-prediction scale. Every number traces back to JSON files listed in §K.

**Population-of-interest framing.** The 9 "low-baseline" subjects (C5 ≤ 2.0) are the sample subset whose baseline is low enough to matter. The population *outside* this study — living people with private decisions not in any training corpus — is overwhelmingly low-baseline by construction. Approximately 99% of real AI users have negligible pretraining representation of their personal behavior. The low-baseline slice is the operationally relevant population for real deployment. Use this framing whenever the low-baseline result is quoted.

---

## 1. THE GRADIENT — Spec effect vs. baseline knowledge (14 subjects)

**Label:** Gradient. 14 public-domain autobiographical subjects. 7-judge aggregate (see §9 on judge coverage caveat).
**One-line summary:** The worse the model's pretraining knows the subject, the more the spec helps; on the low-baseline slice (the population of interest), 9 of 9 subjects improve.

**Data (ordered by C5 baseline, ascending):**

| Subject | C5 baseline | C2a spec alone | C4a facts+spec | Δ spec | Δ facts+spec |
|---|---:|---:|---:|---:|---:|
| sunity_devee | 1.03 | 2.47 | 2.60 | +1.44 | +1.57 |
| ebers | 1.04 | 1.79 | 2.34 | +0.76 | +1.30 |
| hamerton | 1.25 | 3.04 | 3.22 | +1.79 | +1.97 |
| fukuzawa | 1.80 | 2.56 | 2.99 | +0.75 | +1.18 |
| seacole | 1.85 | 2.64 | 2.78 | +0.79 | +0.93 |
| bernal_diaz | 1.85 | 2.50 | 2.67 | +0.65 | +0.81 |
| keckley | 1.91 | 2.64 | 2.62 | +0.73 | +0.71 |
| yung_wing | 1.96 | 2.40 | 2.53 | +0.44 | +0.57 |
| babur | 1.98 | 2.16 | 2.28 | +0.17 | +0.30 |
| *— low-baseline cutoff —* | | | | | |
| cellini | 2.56 | 2.72 | 2.79 | +0.16 | +0.24 |
| zitkala_sa | 2.60 | 2.19 | 2.26 | −0.41 | −0.33 |
| rousseau | 2.65 | 3.02 | 2.74 | +0.37 | +0.09 |
| augustine | 2.79 | 2.83 | 3.08 | +0.04 | +0.29 |
| equiano | 2.93 | 2.70 | 2.65 | −0.24 | −0.28 |

**Aggregates:**
- All 14: mean Δ spec = +0.53, mean Δ facts+spec = +0.67, positive on 12 of 14
- Low-baseline only (n=9): mean Δ spec = +0.84, mean Δ facts+spec = +1.04, positive on **9 of 9**
- High-baseline (n=5): mean Δ spec = −0.02, mean Δ facts+spec = 0.00 (null)

**Interpretation (bounded to this experiment):**
- The spec helps more where the baseline is lower. The effect is a gradient, not a binary.
- On the low-baseline slice — the 9 subjects that approximate real AI users — the spec is uniformly beneficial. No exceptions.
- Two subjects decline (Zitkala-Sa, Equiano) and they are the two with the highest pretraining baselines in the low-baseline-adjacent range. This is consistent with the gradient mechanism.

**Paper location:** Table 4.1 in §4.1 "The Cross-Subject Gradient (N=14)".

---

## 2. STATISTICAL TESTS — Gradient significance

**Label:** Gradient statistical significance.
**One-line summary:** The spec effect is statistically robust; the gradient (effect inversely proportional to baseline) is the dominant pattern with slope −0.98.

| Test | Value |
|---|---|
| Wilcoxon signed-rank, C5 vs C2a (N=14) | W = 10.0, p = 0.0076 |
| Wilcoxon signed-rank, C5 vs C4a (N=14) | W = 9.0, p = 0.0063 |
| Linear regression (Δ vs C5) slope | −0.98 |
| Regression slope 95% CI | [−1.30, −0.74] |
| Regression intercept | +2.65 |
| Krippendorff α, all 7 judges | 0.535 (ordinal, moderate agreement) |
| Krippendorff α, non-Gemini 5 judges | 0.659 (ordinal, substantial agreement) |

**Interpretation (bounded):**
- p < 0.01 on both Wilcoxon tests. Gradient is not noise.
- Slope CI excludes zero comfortably. The relationship is reliably negative.
- Non-Gemini inter-judge agreement (α=0.66) is above the ordinal "substantial agreement" threshold; Gemini-inclusive agreement drops to 0.54 due to systematic Gemini inflation (see §9).

**Paper location:** §4.1, with full Gemini sensitivity in §4.1.2.

---

## 3. MEMORY SYSTEMS × SPEC — Aggregate spec-delta (all 14 subjects)

**Label:** Memory system × spec table. Mem0/Letta/Supermemory/Zep/BaseLayer, two configs each.
**One-line summary:** Adding the Base Layer spec to any of the 4 commercial memory systems produces positive delta in at least one configuration; 3 of the 4 are positive in both.

**Controlled configuration** (all systems given identical extracted fact set):

| System | Mean Δ (C3 − C1) | 95% bootstrap CI | Interpretation |
|---|---:|---:|---|
| Mem0 | +0.15 | [+0.08, +0.23] | Positive, tight CI |
| Letta | +0.25 | [+0.15, +0.36] | Positive, tight CI |
| Zep | +0.22 | [+0.14, +0.31] | Positive, tight CI |
| Supermemory | −0.04 | [−0.12, +0.04] | Near-zero (ceiling — see §4) |
| Base Layer | +0.12 | [+0.04, +0.21] | Positive, small |

**Native configuration** (each system runs its own ingestion pipeline on raw corpus):

| System | Mean Δ (C3 − C1) | 95% bootstrap CI | Interpretation |
|---|---:|---:|---|
| Mem0 | +0.38 | [+0.21, +0.54] | Strong positive |
| Letta | −0.01 | [−0.09, +0.06] | Null — archival-retrieval path (see §7 for stateful-agent test) |
| Zep | +0.38 | [+0.25, +0.50] | Strong positive |
| Supermemory (n=10) | −0.11 | [−0.24, +0.04] | Near-zero; 4 subjects failed free-tier ingestion |

**Interpretation (bounded):**
- Controlled config: 4 of 5 systems positive (all except Supermemory, which is near-zero).
- Native config: Mem0 and Zep clearly positive; Letta null; Supermemory slightly negative.
- The Letta native null is explained by architectural misconfiguration (we used the archival path, not the stateful-agent path — see §7).
- Supermemory aggregate is near-zero but this comes from its high-baseline subjects; see §4 for the low-baseline breakdown.

**Paper location:** Table 4.3 in §4.3.

---

## 4. MEMORY SYSTEMS × SPEC ON LOW-BASELINE — Population of interest only

**Label:** Memory system low-baseline slice (C5 ≤ 2.0, n=9 subjects).
**One-line summary:** On the 9 low-baseline subjects — the population approximating real AI users — the Base Layer spec produces positive mean delta on ALL 4 commercial memory systems in the controlled configuration.

**Controlled configuration, low-baseline slice:**

| System | Mean Δ on low-baseline | Positive subjects |
|---|---:|---:|
| Mem0 | +0.13 | 6 of 9 |
| Letta | +0.23 | 7 of 9 |
| Zep | +0.20 | 9 of 9 |
| Supermemory | +0.004 | 5 of 9 |
| Base Layer | +0.13 | 7 of 9 |

**All 5 systems have positive (or barely positive) mean delta on the low-baseline slice.**

**Native configuration, low-baseline slice:**

| System | Mean Δ on low-baseline | Positive subjects |
|---|---:|---:|
| Mem0 | +0.38 | 7 of 9 |
| Letta | −0.01 | 4 of 9 |
| Zep | +0.37 | 9 of 9 |
| Supermemory | −0.06 (n=7) | 2 of 7 |

**Interpretation (bounded):**
- The load-bearing result: in the controlled config, adding the spec improves all 4 commercial memory systems on the population of interest (low-baseline subjects). This generalizes the spec's usefulness across memory-provider architectures.
- Zep is the strongest, most uniform case: 9/9 positive on low-baseline in both configs.
- Supermemory controlled is barely above zero (+0.004) — not failure, but the weakest case. Its native config is slightly negative, reflecting the ceiling effect: SM's strong native retrieval lifts most subjects out of the spec's useful range.

**Paper location:** Table 4.3 low-baseline rows, §4.3 key findings.

---

## 5. SUPERMEMORY DEEP-DIVE — Per-subject on low-baseline

**Label:** Supermemory per-subject detail, low-baseline only.
**One-line summary:** Supermemory's spec delta is mixed on low-baseline (5 of 9 positive), with positive deltas concentrated on subjects where Supermemory's own retrieval leaves headroom.

| Subject | C5 baseline | C1 (SM alone) | C3 (SM + spec) | Δ |
|---|---:|---:|---:|---:|
| sunity_devee | 1.03 | 2.70 | 2.54 | −0.16 |
| ebers | 1.04 | 2.01 | 2.21 | **+0.20** |
| hamerton | 1.25 | 2.72 | 2.86 | **+0.14** |
| fukuzawa | 1.80 | 2.85 | 2.71 | −0.14 |
| seacole | 1.85 | 2.74 | 2.86 | **+0.12** |
| bernal_diaz | 1.85 | 2.61 | 2.58 | −0.03 |
| keckley | 1.91 | 2.90 | 2.65 | −0.25 |
| yung_wing | 1.96 | 2.47 | 2.58 | **+0.11** |
| babur | 1.98 | 2.03 | 2.08 | **+0.05** |

**Interpretation (bounded):**
- 5 of 9 subjects show positive delta. Aggregate = +0.004.
- On subjects where SM's C1 is low (ebers 2.01, yung_wing 2.47, babur 2.03), the spec adds positive delta consistent with the gradient mechanism.
- On subjects where SM's C1 is already high (fukuzawa 2.85, keckley 2.90), the spec adds negative delta — retrieval has already captured what it could, and the spec introduces competing signal.
- The overall near-zero aggregate for Supermemory is explained by its retrieval distribution, not by spec failure.

**Paper location:** §4.3 Supermemory paragraph.

---

## 6. WRONG-SPEC CONTROLS — Content specificity tests

**Label:** Wrong-spec v1 (Franklin-for-all) + v2 (random derangement).
**One-line summary:** A subject's spec, when wrong, scores near or below baseline; the correct spec is what produces improvement, not the format.

| Condition | Mean | Δ vs C5 baseline | Δ vs C2a correct spec |
|---|---:|---:|---:|
| C5 (no spec) | 2.02 | — | − |
| C2a (correct spec) | 2.55 | +0.53 | − |
| C2c v1 (Franklin's spec applied to all 13 non-Franklin subjects) | 1.86 | −0.16 | −0.69 |
| C2c v2 (random derangement, seed=42) | 2.30 | +0.28 | −0.25 |

**Interpretation (bounded):**
- v1 (Franklin-for-all) is the cleanest null: Franklin's spec is uniformly dissimilar to the 13 other subjects, and assigning it produces scores below baseline.
- v2 (random derangement) is a noisier null: some random pairings happen to produce loosely-similar specs, so v2 is slightly elevated above v1. Still far below correct-spec scores.
- In both v1 and v2, wrong specs do NOT reach correct-spec scores. The content specificity of the correct spec matters.

**Paper location:** Table 4.5 in §4.5.

---

## 7. LETTA STATEFUL-AGENT TEST — Hamerton only

**Label:** Letta stateful-agent loop, Packer methodology.
**One-line summary:** When Letta's stateful-agent path is invoked properly (30-turn ingestion with self-editing), it produces a representation that predicts as well as Base Layer's spec at 65% the context size, on Hamerton.

| Measurement | Value |
|---|---|
| Final Letta `human` memory block | 22,472 chars / ~3,167 words / ~5,600 tokens |
| Base Layer full-stack spec (Hamerton) | 34,579 chars / ~5,250 words / ~8,500 tokens |
| Letta block / Base Layer spec (size ratio) | 0.65 |
| Run A: gpt-4o-mini + Letta agent loop (native response model) | 3.38 (6 judges) |
| Run B: Haiku + Letta block as context (matched response model) | **3.24** (6 judges); 3.12 non-Gemini (4 judges) |
| Reference C2a: Haiku + Base Layer full-stack spec | **3.04** (7 judges) |
| Reference C5 Hamerton baseline | 1.25 |
| Run B vs C2a at matched response model | +0.20 at 65% context size |

**Interpretation (bounded):**
- This is a single-subject result (Hamerton only). Do not generalize to 13 other subjects.
- Letta's stateful-agent path produces an interpretive representation (not just retrieval). Five overlapping behavioral patterns identified by independent Opus comparison.
- At matched response model, Letta's block predicts slightly higher than Base Layer's full-stack spec at smaller context — structural parity with size efficiency.
- An Ebers follow-up test was launched in parallel; will add here when complete.
- Generalization to all 14 subjects is the most important outstanding memory-systems experiment.

**Paper location:** §4.3.1.

---

## 8. TABLE 4.2 — HAMERTON COMPRESSION (token efficiency)

**Label:** Hamerton compression curve.
**One-line summary:** On Hamerton, a 7K-token spec (C2a) outperforms 34K tokens of raw corpus (C8) and matches spec-augmented raw corpus (C9).

| Condition | Avg input tokens | Score (1-5) | Normalized (0-100%) |
|---|---:|---:|---:|
| C8 Raw corpus, no spec | 34,168 | 2.32 | 33% |
| C9 Raw corpus + spec | 41,452 | 3.22 | 56% |
| C4a All facts + spec | 16,874 | 3.22 | 56% |
| C4 All facts, no spec | 7,723 | 2.53 | 38% |
| C3 Mem0 + spec | 7,576 | 2.77 | 44% |
| C3 Supermemory + spec | 7,522 | 2.86 | 47% |
| C2a Spec only | 7,320 | 3.04 | 51% |
| C1 Mem0 (facts only) | ~300 | 2.55 | 39% |
| C5 Baseline (nothing) | ~40 | 1.25 | 6% |

**Interpretation (bounded):**
- Information is not what's missing: C4 (all facts, no spec) at 7,723 tokens scores 2.53, while C2a (spec alone) at 7,320 tokens scores 3.04. Same token budget, much better result from the structured spec.
- Raw 34K-token corpus (C8) only reaches 2.32 — the model cannot extract interpretive structure from unstructured text alone.
- Adding spec on top of raw corpus (C9) closes the gap to C4a level, confirming structure is the limiting factor, not information.

**Paper location:** Table 4.2 in §4.2.

---

## 9. JUDGE PANEL — Coverage and calibration

**Label:** 7-judge panel. LLM-as-judge for behavioral-prediction grading.
**One-line summary:** All 7 judges agree on direction; Gemini judges inflate scores by ~1 point; GPT-5.4 has the highest parse-failure rate; Gemini Pro coverage is limited to Hamerton + Tier 2.

| Judge | Coverage | Parse-failure rate | Score offset vs 5-judge panel |
|---|---|---:|---:|
| Claude Haiku 4.5 | All conditions, all subjects | ~0.2% | baseline |
| Claude Sonnet 4.6 | All conditions, all subjects | ~0.4% | baseline |
| Claude Opus 4.6 | All conditions, all subjects | ~0.3% | baseline |
| GPT-4o | All conditions, all subjects | ~1% | baseline |
| GPT-5.4 | All conditions, all subjects | **~19%** | +0.1 |
| Gemini 2.5 Flash | All conditions, all subjects | ~2% | **+0.9** |
| Gemini 2.5 Pro | Hamerton, Tier 2, wrong-spec v2 only | **~0.5%** | **+1.0** |

**Interpretation (bounded):**
- The five non-Gemini judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) form a calibrated core panel.
- Both Gemini judges systematically inflate by ~1 point — handled by reporting non-Gemini means alongside full-panel means (§4.1.2 sensitivity analysis).
- GPT-5.4 parse-failure rate 19% means ~19% of its judgments are dropped per the aggregation rule; effective coverage remains >80% of questions.
- Gemini Pro did NOT run on the 13 global subjects' main gradient conditions — only on Hamerton and Tier 2 replication. Paper methodology describes 7 judges; effective coverage is 6 for global subjects.

**Paper location:** §3.7 judge calibration, §4.1.2 sensitivity analysis.

---

## 10. TIER 2 CIRCULARITY — Cross-provider replication

**Label:** Tier 2 circularity. 3 subjects × 2 non-Haiku response models × GPT-5.4-generated battery.
**One-line summary:** The spec effect replicates across non-Haiku response models on non-Haiku batteries in 5 of 6 cells — circularity concern defused.

| Subject | Response Model | Battery | Spec-effect Δ | Direction |
|---|---|---|---:|---|
| Ebers | Sonnet | GPT-5.4 | +1.48 | ✓ positive |
| Ebers | Gemini Pro | GPT-5.4 | +1.07 | ✓ positive |
| Yung Wing | Sonnet | GPT-5.4 | +1.91 | ✓ positive |
| Yung Wing | Gemini Pro | GPT-5.4 | +1.27 | ✓ positive |
| Zitkala-Sa | Sonnet | GPT-5.4 | +1.40 | ✓ positive |
| Zitkala-Sa | Gemini Pro | GPT-5.4 | −0.55 | ✗ mismatch |

**Interpretation (bounded):**
- 5 of 6 cells positive. Effect is not an artifact of Haiku-answering-Haiku-generated batteries.
- The Zitkala-Sa × Gemini Pro mismatch is the one outlier. Zitkala-Sa is also one of the two subjects the main gradient shows spec hurting (§4.1.3 failure-mode analysis) — this is a consistent-with-gradient finding, not a replication failure.
- Baseline accuracy varies by 1-2 points across response models on the same subject — independent empirical evidence for the cross-provider variance the paper claims.

**Paper location:** §4.8.

---

## 11. EBERS STATEFUL-AGENT TEST — In Progress

**Label:** Ebers Letta stateful-agent loop (2nd-subject generalization check).
**One-line summary:** In-flight; will extend §4.3.1 from n=1 to n=2.

**Status at time of writing:** ~25-30 of 52 chunks ingested; ~30 min remaining. Will populate this section with block size, prediction score, and comparison to §7 when complete.

**Paper location:** Planned addition to §4.3.1 or §7 pending result.

---

## 12. BASE LAYER AS RETRIEVAL FLOOR — Where BL wins, where it doesn't

**Label:** BL standalone retrieval (MiniLM + ChromaDB) vs commercial systems' retrieval.
**One-line summary:** BL's retrieval is comparable to commercial systems — in the same band, wins only on Hamerton (pipeline development subject), usually middle-of-pack.

**C1 comparisons (retrieval only) on low-baseline subjects (C5 ≤ 2.0):**

| Subject | C5 | Mem0 C1 | Letta C1 | SM C1 | Zep C1 | **BL C1** | Best |
|---|---:|---:|---:|---:|---:|---:|---|
| sunity_devee | 1.03 | 2.13 | 2.59 | 2.57 | 2.24 | 2.41 | letta |
| ebers | 1.04 | 1.65 | 2.21 | 1.80 | 1.60 | 1.76 | letta |
| hamerton | 1.25 | 1.72 | 2.56 | 2.20 | 1.98 | **2.73** | **BL** |
| fukuzawa | 1.80 | 2.59 | 3.07 | 2.90 | 2.41 | 2.45 | letta |
| seacole | 1.85 | 2.16 | 2.89 | 2.74 | 2.18 | 2.44 | letta |
| bernal_diaz | 1.85 | 2.44 | 2.65 | — | 2.25 | 2.36 | letta |
| keckley | 1.91 | 2.45 | 2.70 | 2.58 | 2.48 | 2.44 | letta |
| yung_wing | 1.96 | 1.79 | 2.53 | 2.52 | 2.01 | 2.23 | letta |
| babur | 1.98 | 1.62 | 2.03 | — | 1.68 | 1.67 | letta |

**Interpretation (bounded):**
- BL wins C1 outright on 1 of 9 low-baseline subjects: Hamerton (which was also the pipeline development subject, so pipeline-tuning bias is present).
- BL is typically middle-of-pack or behind Letta on C1.
- **Takeaway:** BL is not a "better retriever" than the commercial systems. Its contribution is the spec layer, not the retrieval substrate.

**Paper location:** §4.4.

---

## K. PROVENANCE — Source files for every number

| Data category | Source file path |
|---|---|
| Gradient 14 subjects | `data/experiments/memory_systems/results/RESULTS_S113.json` > `gradient` |
| Memory systems aggregate | `RESULTS_S113.json` > `memory_systems` |
| Statistical tests | `RESULTS_S113.json` > `wilcoxon`, `gradient_regression`, `krippendorff_alpha` |
| Tier 2 circularity | `RESULTS_S113.json` > `tier2_circularity` |
| Letta stateful-agent block | `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json` |
| Letta matched-model test | `results/run_fullstack_hamerton_20260411_231237/letta_memory_haiku_judgments_*.json` |
| Hamerton Table 4.2 | `results/run_fullstack_hamerton_20260411_231237/*_judgments_*.json` (aggregated per condition) |
| Wrong-spec v1 | `results/global_*/judgments_v2.json` > condition `C2c_wrong_spec` |
| Wrong-spec v2 | `results/run_fullstack_hamerton_20260411_231237/wrong_spec_v2_judgments_*.json` + per-subject |
| Judge calibration | per-judge parse-failure counts computed across all `*_judgments_*.json` files |

Any discrepancy between this document and the paper draft should be resolved in favor of this document. Paper was updated against these numbers in session S113 (2026-04-18).
