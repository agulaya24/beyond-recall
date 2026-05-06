# Supermemory §4.4.1 Update Block — Ready to Apply

_Generated 2026-04-23 by `scripts/compute_supermemory_paid_tier_aggregate.py`._
_Replaces the existing Supermemory paragraph + table rows in v9 §4.4.1._

---

## Replacement paragraph for v9 §4.4.1 (Supermemory micro-paragraph)

> **Supermemory (native).** Across all 14 subjects with native Supermemory data (Hamerton + 13 globals), mean Δ_spec = -0.013 on the 5-judge primary panel (6 subjects positive, 8 negative; Wilcoxon W = 48.0, p = 0.8077). On the low-baseline slice (C5 ≤ 2.0, n = 9), mean Δ_spec = -0.027 (4/9 positive; Wilcoxon W = 21.0, p = 0.9102). Per-subject Δ_spec ranges from -0.447 (fukuzawa) to +0.426 (rousseau). At the per-question level, across the 377 paired (C1, C3) questions with valid 5-judge scores (of 546 nominal, with the remainder excluded due to per-question parse failures on the C1_supermemory_fp judge runs), the spec helped by ≥ 0.5 on 82 questions (22%), hurt by ≥ 0.5 on 60 questions (16%), and was within ±0.5 on 235 (62%). The aggregate near-zero is a mixture of positive and negative per-question effects that cancel on average — see §4.4.2 and the paired-response analysis in `docs/research/supermemory_c1_vs_c3_paired_analysis.md` for qualitative characterization.

## Updated table rows for v9 §4.4.1 "Aggregate results, native configuration"

### Current (v9 line ~1081) — REMOVE:

```
| Supermemory* | −0.07 | 3/10 | −0.03 | 3/7 |
```

### Replacement — INSERT:

```
| Supermemory | −0.01 | 6/14 | −0.03 | 4/9 |
```

(Note: asterisk and free-tier-failure footnote on the Supermemory row are removed, since all 14 subjects are now included.)

### Also update (v9 line 1086 — Wilcoxon sentence):

**Was:**

> Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant.

**Replacement:**

> Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant (Supermemory native W = 48.0, p = 0.8077 on the paid-tier-complete n = 14 sample).

### Alternate detailed table row (if v9 wants Wilcoxon inline):

| System | Config | Δ_spec (5-judge, full) | + / total | Δ_spec low-baseline | Low + / total | Wilcoxon |
|---|---|---:|---:|---:|---:|---:|
| supermemory | native | -0.013 | 6/14 | -0.027 | 4/9 | W = 48.0, p = 0.8077 |

Prior row for diff-comparison (n = 10 free-tier partial):

| supermemory | native | -0.073 | 3/10 | -0.026 | 3/7 | W = 18.0, p = 0.3750 |

## Updated footnote on Supermemory ingestion (v9 line 1084)

**Was (to be replaced):**

> \* Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau), so the native n drops to 10 full / 7 low-baseline. Base Layer has no separate "native" condition because Base Layer's authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

**Now (replacement) — keep the Base Layer sentence; replace the Supermemory sentence:**

> Supermemory native data: four subjects (Bernal Diaz, Babur, Cellini, Rousseau) initially encountered ingestion failures on the free-tier Supermemory API. A paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures) and retrieved 4.3–5.0 facts per question across these four subjects, with the 5-judge primary panel re-run on the resulting responses; the native Supermemory aggregate reported above reflects the paid-tier rerun, with all 14 main-study subjects (Hamerton + 13 globals) included. Base Layer has no separate "native" condition because Base Layer's authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

(Alternatively, if the asterisk is dropped from the Supermemory row in the table, this footnote can be reduced to just the Base Layer sentence; the Supermemory methodology goes into §3.3.)

## Notes for paper author

- Aggregate sign is unchanged from the prior published number: Δ_spec stayed negative. Magnitude shifted +0.060 toward zero.
- Low-baseline mean shifted -0.001 (-0.026 → -0.027). Essentially unchanged.
- Paired Wilcoxon (5-judge, n = 14): p = 0.8077 (was p = 0.3750 at n = 10). More data, weaker test — reflects mixture-cancellation rather than the prior 4-subject gap.

### Per-question mixture — reconciliation note (important)

- The task asked for "14 × 39 = 546 questions"; actual valid-paired count is **377/546**. Shortfall is not a bug; it is the product of `parse_failure=True` rows on `C1_supermemory_fp` (score=0) being excluded per existing study convention (matches `recompute_5judge_primary.py` and `compute_memory_systems_5judge.py`).
- Shortfall concentrates in 6 subjects where all 5 primary judges emitted parse failures on the same C1 question-ids: sunity_devee (34 q), fukuzawa (34), augustine (33), ebers (30), seacole (21), equiano (17). These are upstream C1 response-generation issues on `supermemory_fullpipeline` (empty or malformed responses the judges could not score), not 5-judge-panel failures. C3 had 0 parse failures across the study.
- **§4.4.2 vs §4.4.1 reconciliation:** §4.4.2 already reports "516 paired main-study questions" — that number is on the **controlled** Supermemory condition (`C1_supermemory` / `C3_supermemory`), not the **native** condition (`_fp`). The two numbers measure different data; they are not in conflict. If §4.4.1 adds the native 377/546 figure, consider a one-liner distinguishing it from the §4.4.2 controlled 516 figure.
- Per-question mixture proportions (22% help / 16% hurt / 62% tied) are dominated by the 8 subjects with full-coverage pairs (Hamerton + 4 paid-tier + keckley + yung_wing + zitkala_sa = 312 pairs, 83% of the 377 valid). Proportions are not skewed by any single subject.

### Paragraph-length note

- The replacement paragraph above runs ~150 words with the full mixture breakdown. The existing §4.4.1 Supermemory content is shorter (one sentence at v9 line 1090 + footnote). If the author wants to keep §4.4.1 tight, mean + range + Wilcoxon go in §4.4.1, and the per-question mixture count moves to §4.4.2 (or stays as a supplementary table). The modular pieces above (table row, Wilcoxon sentence, footnote) support that split.

### Other housekeeping

- Blog post should not need changes — it references the qualitative paired-analysis story, not the aggregate number. Verify by reading `docs/blog_post_v2.md` for any "-0.07" or "n = 10" references (none expected).
- `docs/research/memory_systems_5judge_primary.md` is now stale for Supermemory native rows; rerun `scripts/compute_memory_systems_5judge.py` (or point it at canonical results path for the 4 paid-tier subjects) to resync that reference file.
- `docs/KEY_FINDINGS.md` line 71 still says "Supermemory −0.11 (ceiling)" — update to "−0.01" for the 7-judge or "−0.01" for the 5-judge (both round to −0.01 / −0.02 depending on panel and precision).
- `docs/DATA_REFERENCE.md` line 110 says "Supermemory slightly negative" — still accurate.
- `docs/PROVENANCE_INDEX.md` line 394 points at "n=10 shown for native SM" — this entry needs updating to reflect n=14 paid-tier.
