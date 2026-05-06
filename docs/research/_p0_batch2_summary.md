# P0 Batch 2 — Summary

_Generated 2026-04-23. Three post-hoc analyses for the "Beyond Recall" v8 → v9 paper revision. Companion to the P0 batch 1 summary (`_p0_parallel_batch_summary.md`)._

## Status

| Job | Status | Report | Data |
|---|---|---|---|
| P0-5  Spec-induced refusal audit | DONE | [`spec_refusal_audit.md`](spec_refusal_audit.md)     | [`spec_refusal_audit.json`](spec_refusal_audit.json) |
| P0-15 Question-category audit    | DONE | [`question_category_audit.md`](question_category_audit.md) | [`question_category_audit.json`](question_category_audit.json) |
| P0-17 Judge floor-test           | DONE | [`judge_floor_test.md`](judge_floor_test.md)         | [`judge_floor_test.json`](judge_floor_test.json) |

## Scripts (all repo-root runnable)

```bash
python scripts/_p0b_inventory.py                  # Pre-flight counts (no API)
python scripts/audit_spec_refusals.py             # Job 1 — Haiku classifier
python scripts/classify_question_categories.py    # Job 2 — Haiku classifier
python scripts/judge_floor_test.py                # Job 3 — 5-judge floor test
```

## Pre-flight inventory (Job 1 specifically)

The P0-5 audit needed to know how many spec-induced refusals existed before spending classification budget. Broad-rule recount (the canonical `REFUSAL_RE` from `scripts/classify_hedging.py`, triggered anywhere in C3 but not C1 on the same question) across 9 low-baseline subjects × 5 memory-system substrates = 45 cells:

| Count | Rule |
|---|---|
| 81  | Broad (C3 has any refusal hit AND C1 does not) — **used as audit scope** |
| 6   | Narrow (C3 *opens* with explicit refusal, C1 does not) — reported as addendum, too sparse to tabulate |

Hamerton carries 28 of 81 refusals on its own (the paper's flagship low-baseline subject). The remaining 53 are spread across the other 8 subjects.

## Top findings to escalate

### 1. JOB 1 — roughly half of "spec-induced refusals" are spec-axiom artifacts, not epistemic caution

_Directional. Caveats in [`spec_refusal_audit.md`](spec_refusal_audit.md) — Haiku's retrieval-sufficiency judgment is noisy, and the broad REFUSAL_RE regex catches hedged-but-substantive responses in addition to outright refusals._

Across the 81 refusals:

| Category | n | % |
|---|---:|---:|
| SPEC_AXIOM_TRIGGER (retrieval was sufficient but spec made the model hold back) | 41 | 50.6% |
| RUBRIC_ARTIFACT (honest refusal scored at the 1-anchor floor) | 24 | 29.6% |
| SCORED_AS_WRONG_PRED (judges gave partial credit to a refusal) | 10 | 12.3% |
| EPISTEMIC_HONEST (retrieval genuinely insufficient, score > 1.5) | 6 | 7.4% |

**Per-substrate concentration.** Mem0 (28 refusals) and Zep (22) are where spec-axiom triggering is most visible. Letta has only 4 refusals total — the stateful agent rarely produces spec-induced refusals. Baselayer sits in the middle at 13, entirely split between SPEC_AXIOM and the tail categories. **Reading:** the honesty/dignity axioms in the behavioural spec produce measurable conservatism that the current rubric penalises as a wrong prediction.

**For §4.4 / §7 paper prose:** about half of the spec's low-baseline refusals are the model *applying the spec's honesty axioms*, not the model failing to know. This is the same mechanism the paper discusses in §7 (behavioural alignment as a conservatism axis) but quantified.

### 2. JOB 2 — the gradient does NOT map neatly to "interpretive" vs "recall" questions

586 BP questions classified into three category buckets. Aggregate mean Δ_spec (C2a − C5) per category:

| Category | n | mean Δ_spec | median Δ_spec |
|---|---:|---:|---:|
| LITERAL_RECALL         | 60  | **+0.792** | +0.800 |
| INTERPRETIVE_INFERENCE | 366 | +0.397 | +0.400 |
| REFUSAL_TRIGGERING     | 120 | +0.489 | +0.200 |

**Surprise.** The spec lifts LITERAL_RECALL questions the most in absolute mean, not INTERPRETIVE_INFERENCE. Across subjects, the *fraction* of LITERAL_RECALL questions correlates with subject-level Δ_spec at **r = +0.646**. Interpretive fraction negatively correlates (r = −0.582).

**Caveats.** The LITERAL_RECALL bucket is small per subject (median ~4 questions) so these per-subject Δ are high-variance. Mean is dominated by Hamerton (+1.93 on n=10 literal-recall items) and Sunity Devee (+1.38 on n=8). The INTERPRETIVE_INFERENCE bucket is the scale-setter (n=366) and its Δ = +0.397 is the cleanest between-condition signal.

**Mechanism read.** The LITERAL_RECALL boost is likely the spec's *prose style* matching the held-out passage's narrative register — not retrieval correctness. When Hamerton's spec writes in a Victorian register and the held-out is Hamerton's Victorian memoir, Haiku's C2a output paraphrases the register and accidentally lands on or near the held-out fact. This is worth naming explicitly in §4.3: some of the gradient is **stylistic-match contamination on short recall questions**, not mechanism.

**Franklin excluded:** no C5_baseline condition in the data, so all 40 BP entries have null Δ_spec.

### 3. JOB 3 — ALL 5 primary judges leak at the floor; worst variant is "plausible_unsupported"

Wrong-answer variants scored by the 5-judge primary panel:

| Judge | mean score on wrong answers | pct ≤ 1.5 |
|---|---:|---:|
| sonnet | **1.75** | 38% |
| gpt54  | 2.12 | 12% |
| opus   | 2.15 | 22% |
| haiku  | 2.17 | 20% |
| gpt4o  | **2.38** | 5% |

No judge in the 5-panel is tight-at-floor (mean ≤ 1.5). Sonnet is the tightest; GPT-4o is the leakiest.

**Per-variant:** `plausible_unsupported` leaks hardest (mean 2.75 across judges, Opus 3.12). `wrong_direction` is the most reliably scored low (1.62). `off_topic_generic` is surprisingly high on GPT-4o (2.88) — the judge is crediting "humans commonly feel torn…" generic waffle as partial-match.

**Reading for §3.7.6 / §6.2:**
- The primary 5-judge mean is **systematically optimistic** on wrong answers, by ~0.5–0.7 score points at the floor. That is a non-trivial fraction of the observed aggregate Δ_spec (~+0.4 per job-1 refusal-displacement framing).
- The directional gradient still holds — a response that invents plausible but unsupported claims gets ~2.75; a response that recovers the actual held-out behaviour gets 4–5 — but there is real floor compression.
- **Recommendation:** either (a) add a rubric clarification that score 1 is correct for any response that does not identify a held-out-consistent outcome, and re-judge a subset to measure the correction, or (b) down-weight the leakier judges (GPT-4o, Haiku) in the 5-judge aggregate, or (c) report Sonnet-only as a more conservative secondary estimate. Option (a) is the cleanest.

## Cost per job

| Job | API calls | Approx. cost |
|---|---:|---:|
| P0-5 (81 × Haiku classifications) | 81 | ~$0.25 |
| P0-15 (586 × Haiku classifications) | 586 | ~$1.20 |
| P0-17 (8 × Haiku variant gen + 200 × 5-judge scores) | 208 | ~$2.20 |
| **Total** | | **~$3.65** |

Within the ~$5 hard cap. Under-projection for Job 3 because the final scope was 8 diagnostics (Hamerton IDs 3 and 11 are recall-tier, not BP — auto-filtered by the BP-tier gate in `collect_diagnostics`).

## Method caveats

1. **REFUSAL_RE is a regex**, not an LLM classifier. It under-counts Letta's structured non-refusals (e.g. "the available archival memory contains no record of…") that are functionally refusals but phrased more formally. Job 1's per-substrate count is therefore likely a lower bound for Letta and a faithful count for the others.

2. **The question-category taxonomy has an implicit ordering.** REFUSAL_TRIGGERING questions are a subset of questions that *should* refuse — but Haiku-classifier calls are binary per item, so the counts are mutually exclusive. A question that looks interpretive but is unanswerable gets categorised as REFUSAL_TRIGGERING here. See the per-subject table for cases where REFUSAL_TRIGGERING is high (Babur 13/39, Yung Wing 12/39, Zitkala-Sa 15/39, Hamerton 19/39) — these are subjects where the battery itself pushes on the refusal floor more than the spec does.

3. **Job 3's variants are Haiku-generated.** A stronger variant generator (e.g. Opus) could make `plausible_unsupported` variants even more convincing, which would *increase* floor leakage. The 8 × 5 floor-test results are a lower bound.

4. **Hamerton and Franklin's Δ_spec** come from different judgment-file formats than the globals. Hamerton's C5_baseline lives in `judgments_harmonized.json`; its C2a/C2c/C3/C4a live in `judgments.json` as per-question row objects with `haiku_score`/`gemini_score` columns. The Job 2 script merges both — see `scripts/classify_question_categories.py::load_per_question_scores`. Franklin has no C5 and is reported as `— (n=0)` rows.
