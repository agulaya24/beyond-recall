# Analysis Plan Lock — Beyond Recall

**Locked:** 2026-04-16 (Session 113)
**Purpose:** Pre-commitment document for analyses of data that has not yet landed at time of writing, plus locked methodology for analyses of existing data. Written before Tier 2 circularity runs, Supermemory Option B retry, and wrong-spec v2 runs complete.

**What this is:** A prospective analysis plan that applies to:
1. All currently existing run data (Core C1-C5, memory systems Option A/B, Base Layer, C8/C9)
2. Pending runs: Supermemory Option B retry (4 subjects), Tier 2 circularity (3 subjects), wrong-spec v2 (14 subjects)

**What this is NOT:** A preregistration of the full study. Most data landed before this document was written. We lock what is lockable going forward, and report existing data per the same locked methodology.

---

## Primary Outcome

**Representational accuracy**, operationalized as mean predicted-behavior score (1-5 scale) across 39 behavioral prediction questions per subject, averaged across judges per the aggregation rule below.

**Scoring rubric (fixed):**
- 1 = refuses or wholly wrong
- 2 = right topic, wrong prediction
- 3 = right domain, no specifics
- 4 = right direction with specifics
- 5 = specific outcome predicted

---

## Aggregation Rule

For each (subject, condition) cell:
1. Mean score across all questions within each judge
2. Mean across judges

Unit of inference: subject. This is the locked rule and will not change.

---

## Primary Statistical Tests

1. **Wilcoxon signed-rank, paired:** baseline (C5) vs spec (C2a) subject-level means, N=14. Two-sided, alpha=0.05.
2. **Wilcoxon signed-rank, paired:** baseline (C5) vs spec+facts (C4a) subject-level means, N=14. Two-sided.
3. **Krippendorff's alpha (ordinal):** inter-judge agreement on all prediction accuracy judgments. Computed across all 7 judges using pairwise question-level scores.

Multiple-comparison correction: Bonferroni across the two primary Wilcoxon tests (adjusted alpha 0.025).

---

## Secondary Metrics

- **Per-subject improvement:** (C2a - C5), (C4a - C5) in raw score points.
- **Confidence intervals:** 95% bootstrap CI over 1000 resamples of (question × judge) combinations within each (subject, condition) cell. Reported alongside every headline delta.
- **Gradient regression:** Linear regression of (C4a - C5) raw delta on C5 baseline score, with 95% CI on slope. Replaces the dropped "~2.4 threshold" language.
- **Effect size (Cohen's d):** computed on subject-level means between paired conditions. Reported with ordinal-data caveat.

---

## Memory System Analysis

For each of 5 systems (Mem0, Letta, Supermemory, Zep, Base Layer):
- **C1 (retrieval only):** subject-level mean score, 95% CI
- **C3 (retrieval + spec):** subject-level mean score, 95% CI
- **Delta (C3 - C1):** absolute points gained per subject, bootstrap CI

Systems are tested in two configurations:
- **Controlled:** each system given identical 462-fact set (or equivalent per-subject extracted set)
- **Native:** each system processes raw training corpus through its own ingestion pipeline

Paper reports both configurations as one unified memory-system evaluation.

**Supermemory Option B retry (pending):** If ingestion retry succeeds for cellini, bernal_diaz, rousseau, babur, augustine, their data is merged into the primary analysis. If retry fails, they are reported as "Supermemory native pipeline failed ingestion" in limitations. No cherry-picking.

---

## Base Layer (5th System)

Base Layer uses MiniLM-L6-v2 embeddings + ChromaDB retrieval. Analyzed identically to the 4 commercial systems. Same C1 / C3 / Delta structure. No special treatment in reporting.

---

## Wrong-Spec Control (C2c)

**V1 (existing):** Each subject evaluated with Franklin's specification. Risk: Franklin is a known figure; his spec may be implicitly closer to a Victorian British man (Hamerton) than a randomly chosen alternative.

**V2 (pending):** Each subject assigned a wrong spec from a randomly chosen OTHER study subject (not Franklin). Random assignment fixed via seed=42. Reported alongside V1 as a robustness check.

Both V1 and V2 numbers reported in paper. Primary interpretation is V2 (closer to true random control).

---

## Tier 2 Circularity Replication

**Purpose:** Defuse the circularity concern that Haiku generates both questions and responses.

**Design:**
- 3 subjects: ebers (low baseline, strong effect), yung_wing (mid baseline), zitkala_sa (high baseline, negative effect)
- 5 conditions: C1 through C5 (core set only)
- Battery: GPT-5.4-generated (`battery_gpt54.json`, already exists)
- Response models: GPT-5.4 and Sonnet 4.6 (two non-Haiku models, different providers)
- Judge panel: same 7 judges

**Pre-committed test:** For each of the 3 subjects, the direction of the (C4a - C5) delta under GPT-5.4 battery + GPT-5.4 response must match the direction under Haiku battery + Haiku response. Same for Sonnet.

If 5 or 6 of the 6 (3 subjects × 2 response models) replicate direction, circularity is considered defused. If fewer, we report the failure honestly and discuss.

---

## Hedging Reduction

Report per-subject hedging rate: proportion of responses scored as 1 (refusal) + responses flagged as hedged in content. Compare C5 vs C2a and C5 vs C4a.

Existing paper claim (51% → 31%) is Hamerton-only. New analysis computes across all 14 subjects.

---

## Retrieval Overlap

Methodology frozen: LLM-as-judge pairwise comparison using the prompt in `EXPERIMENT_LOG.md` line 79-89. Metrics: top-1, top-3, top-5, top-10 overlap rates across the 3 embedding-based systems (Mem0, Letta, Supermemory).

Existing numbers in paper abstract (68% / 39% / 22% / 11%) are from this methodology. If new data alters, numbers update in paper; methodology does not change.

---

## Reporting

- All raw scores reported as mean ± 95% CI (bootstrap)
- Percentages (improvement over baseline) reported alongside absolute point gains
- Percentages are defined as: `(C_new - C5) / C5 × 100` — relative to raw baseline score
- Effect size interpretation: Cohen's d with ordinal caveat
- No use of the "~2.4 threshold" language. Gradient is reported as continuous relationship.

---

## Deviations

Any deviation from this plan will be reported explicitly in the paper methods section. Examples: additional stat tests, alternative effect metrics, post-hoc subgroup analysis. The plan is a pre-commitment, not a straitjacket, but deviations must be transparent.

---

## Commit Record

This file committed to `agulaya24/memory-study-repo` before the following runs:
- Tier 2 circularity (3 subjects × 2 response models × 5 conditions × 7 judges)
- Wrong-spec v2 (14 subjects × C2c condition × 7 judges)
- Supermemory Option B retry (5 subjects)

Any data landing after this commit is analyzed per this plan.
