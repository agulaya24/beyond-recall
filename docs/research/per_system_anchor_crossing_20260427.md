# Per-Memory-System Anchor-Crossing Analysis (C1 -> C3)

**Generated:** 2026-04-27 by `scripts/compute_per_system_anchor_crossing.py`

## What this measures

For each memory system (Mem0, Letta archival, Zep, Supermemory, BaseLayer), under both controlled (C1_<sys> / C3_<sys>) and native (C1_<sys>_fp / C3_<sys>_fp) configurations, this script asks: when the spec is added on top of retrieval, how often does a question move across an integer rubric anchor (the [1,2), [2,3), [3,4), [4,5] bands) upward?

Aggregation locked to the §3.7.2 rule: per-judge per-question score -> simple mean across the 5 primary judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) per (subject, question, condition). BaseLayer has no native (`_fp`) configuration — it IS the full pipeline — so only the controlled row is reported. Letta stateful path is out of scope; Letta controlled is the archival path.

---

## Plain-language summary

- **mem0 controlled:** 23.4% of 351 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **mem0 native:** 36.1% of 349 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **letta controlled:** 26.9% of 350 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **letta native:** 19.9% of 351 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **zep controlled:** 27.9% of 351 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **zep native:** 32.5% of 351 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **supermemory controlled:** 20.2% of 351 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).
- **supermemory native:** 23.4% of 154 low-baseline paired questions crossed an anchor upward; 6 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 7 subjects).
- **baselayer controlled:** 29.0% of 348 low-baseline paired questions crossed an anchor upward; 9 of 9 low-baseline subjects had at least one upward anchor crossing (data complete on 9 subjects).

---

## Mem0

### mem0 — controlled (C1_mem0 -> C3_mem0)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 546 | 131 | 24.0% | 98 | 17.9% | 317 | 58.1% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 351 | 82 | 23.4% | 66 | 18.8% | 203 | 57.8% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 42 | 12.0% |
| 1->3 | 3 | 0.9% |
| 1->4 | 2 | 0.6% |
| 2->3 | 28 | 8.0% |
| 2->4 | 2 | 0.6% |
| 2->5 | 2 | 0.6% |
| 3->4 | 3 | 0.9% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 12 | 10 | 17 |
| sunity_devee | 39 | 7 | 9 | 23 |
| ebers | 39 | 5 | 5 | 29 |
| fukuzawa | 39 | 9 | 9 | 21 |
| seacole | 39 | 11 | 7 | 21 |
| bernal_diaz | 39 | 8 | 11 | 20 |
| keckley | 39 | 6 | 7 | 26 |
| yung_wing | 39 | 16 | 6 | 17 |
| babur | 39 | 8 | 2 | 29 |

### mem0 — native (C1_mem0_fp -> C3_mem0_fp)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 544 | 202 | 37.1% | 74 | 13.6% | 268 | 49.3% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 349 | 126 | 36.1% | 52 | 14.9% | 171 | 49.0% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 79 | 22.6% |
| 1->3 | 18 | 5.2% |
| 1->4 | 5 | 1.4% |
| 1->5 | 1 | 0.3% |
| 2->3 | 17 | 4.9% |
| 2->4 | 2 | 0.6% |
| 3->4 | 4 | 1.1% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 22 | 3 | 14 |
| sunity_devee | 39 | 19 | 8 | 12 |
| ebers | 37 | 14 | 2 | 21 |
| fukuzawa | 39 | 12 | 7 | 20 |
| seacole | 39 | 18 | 6 | 15 |
| bernal_diaz | 39 | 8 | 9 | 22 |
| keckley | 39 | 9 | 11 | 19 |
| yung_wing | 39 | 16 | 5 | 18 |
| babur | 39 | 8 | 1 | 30 |

## Letta

### letta — controlled (C1_letta -> C3_letta)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 545 | 153 | 28.1% | 93 | 17.1% | 299 | 54.9% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 350 | 94 | 26.9% | 68 | 19.4% | 188 | 53.7% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 51 | 14.6% |
| 1->3 | 16 | 4.6% |
| 2->3 | 17 | 4.9% |
| 2->4 | 4 | 1.1% |
| 3->4 | 6 | 1.7% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 38 | 15 | 6 | 17 |
| sunity_devee | 39 | 8 | 10 | 21 |
| ebers | 39 | 8 | 5 | 26 |
| fukuzawa | 39 | 9 | 6 | 24 |
| seacole | 39 | 14 | 2 | 23 |
| bernal_diaz | 39 | 11 | 14 | 14 |
| keckley | 39 | 5 | 11 | 23 |
| yung_wing | 39 | 15 | 9 | 15 |
| babur | 39 | 9 | 5 | 25 |

### letta — native (C1_letta_fp -> C3_letta_fp)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 546 | 112 | 20.5% | 101 | 18.5% | 333 | 61.0% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 351 | 70 | 19.9% | 70 | 19.9% | 211 | 60.1% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 39 | 11.1% |
| 1->3 | 1 | 0.3% |
| 1->4 | 1 | 0.3% |
| 2->3 | 19 | 5.4% |
| 2->4 | 2 | 0.6% |
| 3->4 | 8 | 2.3% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 13 | 7 | 19 |
| sunity_devee | 39 | 7 | 12 | 20 |
| ebers | 39 | 4 | 6 | 29 |
| fukuzawa | 39 | 6 | 12 | 21 |
| seacole | 39 | 8 | 8 | 23 |
| bernal_diaz | 39 | 10 | 8 | 21 |
| keckley | 39 | 7 | 6 | 26 |
| yung_wing | 39 | 9 | 4 | 26 |
| babur | 39 | 6 | 7 | 26 |

## Zep

### zep — controlled (C1_zep -> C3_zep)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 546 | 160 | 29.3% | 96 | 17.6% | 290 | 53.1% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 351 | 98 | 27.9% | 69 | 19.7% | 184 | 52.4% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 57 | 16.2% |
| 1->3 | 9 | 2.6% |
| 1->4 | 2 | 0.6% |
| 1->5 | 1 | 0.3% |
| 2->3 | 19 | 5.4% |
| 2->4 | 9 | 2.6% |
| 3->4 | 1 | 0.3% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 13 | 7 | 19 |
| sunity_devee | 39 | 13 | 10 | 16 |
| ebers | 39 | 9 | 4 | 26 |
| fukuzawa | 39 | 8 | 9 | 22 |
| seacole | 39 | 18 | 4 | 17 |
| bernal_diaz | 39 | 11 | 8 | 20 |
| keckley | 39 | 9 | 11 | 19 |
| yung_wing | 39 | 12 | 9 | 18 |
| babur | 39 | 5 | 7 | 27 |

### zep — native (C1_zep_fp -> C3_zep_fp)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 546 | 193 | 35.3% | 74 | 13.6% | 279 | 51.1% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 351 | 114 | 32.5% | 48 | 13.7% | 189 | 53.8% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 70 | 19.9% |
| 1->3 | 16 | 4.6% |
| 1->4 | 5 | 1.4% |
| 2->3 | 15 | 4.3% |
| 2->4 | 3 | 0.9% |
| 3->4 | 5 | 1.4% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 21 | 6 | 12 |
| sunity_devee | 39 | 13 | 8 | 18 |
| ebers | 39 | 8 | 3 | 28 |
| fukuzawa | 39 | 14 | 7 | 18 |
| seacole | 39 | 14 | 5 | 20 |
| bernal_diaz | 39 | 12 | 6 | 21 |
| keckley | 39 | 11 | 5 | 23 |
| yung_wing | 39 | 14 | 4 | 21 |
| babur | 39 | 7 | 4 | 28 |

## Supermemory

### supermemory — controlled (C1_supermemory -> C3_supermemory)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 516 | 96 | 18.6% | 113 | 21.9% | 307 | 59.5% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 351 | 71 | 20.2% | 79 | 22.5% | 201 | 57.3% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 31 | 8.8% |
| 1->3 | 3 | 0.9% |
| 2->3 | 21 | 6.0% |
| 2->4 | 5 | 1.4% |
| 2->5 | 1 | 0.3% |
| 3->4 | 9 | 2.6% |
| 3->5 | 1 | 0.3% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 14 | 8 | 17 |
| sunity_devee | 39 | 3 | 10 | 26 |
| ebers | 39 | 7 | 5 | 27 |
| fukuzawa | 39 | 5 | 12 | 22 |
| seacole | 39 | 9 | 6 | 24 |
| bernal_diaz | 39 | 7 | 14 | 18 |
| keckley | 39 | 7 | 14 | 18 |
| yung_wing | 39 | 12 | 7 | 20 |
| babur | 39 | 7 | 3 | 29 |

### supermemory — native (C1_supermemory_fp -> C3_supermemory_fp)

**Missing data for subjects:** babur, bernal_diaz, cellini, rousseau

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 10 / 14 | 221 | 42 | 19.0% | 50 | 22.6% | 129 | 58.4% | 9 / 14 |
| Low-baseline (9) | 7 / 9 | 154 | 36 | 23.4% | 30 | 19.5% | 88 | 57.1% | 6 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 24 | 15.6% |
| 1->3 | 3 | 1.9% |
| 2->3 | 4 | 2.6% |
| 3->4 | 4 | 2.6% |
| 4->5 | 1 | 0.6% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 13 | 3 | 23 |
| sunity_devee | 5 | 0 | 1 | 4 |
| ebers | 9 | 3 | 1 | 5 |
| fukuzawa | 5 | 1 | 2 | 2 |
| seacole | 18 | 3 | 4 | 11 |
| keckley | 39 | 6 | 10 | 23 |
| yung_wing | 39 | 10 | 9 | 20 |

## Baselayer

### baselayer — controlled (C1_baselayer -> C3_baselayer)

| Scope | N subjects (with data / scope) | N questions | Upward | % up | Downward | % down | No crossing | % none | Subjects with >=1 upward / N |
|---|---|---|---|---|---|---|---|---|---|
| All 14 subjects | 14 / 14 | 543 | 145 | 26.7% | 117 | 21.5% | 281 | 51.7% | 14 / 14 |
| Low-baseline (9) | 9 / 9 | 348 | 101 | 29.0% | 75 | 21.6% | 172 | 49.4% | 9 / 9 |

**Upward boundary breakdown (low-baseline scope):**

| Boundary | Count | % of low-baseline questions |
|---|---|---|
| 1->2 | 58 | 16.7% |
| 1->3 | 6 | 1.7% |
| 1->4 | 2 | 0.6% |
| 2->3 | 23 | 6.6% |
| 2->4 | 5 | 1.4% |
| 3->4 | 6 | 1.7% |
| 4->5 | 1 | 0.3% |

**Per-subject (low-baseline scope):**

| Subject | N questions | Upward | Downward | No crossing |
|---|---|---|---|---|
| hamerton | 39 | 13 | 10 | 16 |
| sunity_devee | 39 | 10 | 7 | 22 |
| ebers | 39 | 10 | 5 | 24 |
| fukuzawa | 39 | 13 | 11 | 15 |
| seacole | 39 | 12 | 8 | 19 |
| bernal_diaz | 39 | 9 | 13 | 17 |
| keckley | 39 | 10 | 7 | 22 |
| yung_wing | 39 | 18 | 8 | 13 |
| babur | 36 | 6 | 6 | 24 |

---

## Multi-anchor-jump distribution per system

Counts of upward jumps by jump size (number of integer bands crossed). Low-baseline scope.
A 2-band jump is e.g. 1.x -> 3.x, a 3-band jump is e.g. 1.x -> 4.x.

| System | Config | 1-band | 2-band | 3-band | 4-band | Total upward |
|---|---|---|---|---|---|---|
| mem0 | controlled | 73 | 5 | 4 | 0 | 82 |
| mem0 | native | 100 | 20 | 5 | 1 | 126 |
| letta | controlled | 74 | 20 | 0 | 0 | 94 |
| letta | native | 66 | 3 | 1 | 0 | 70 |
| zep | controlled | 77 | 18 | 2 | 1 | 98 |
| zep | native | 90 | 19 | 5 | 0 | 114 |
| supermemory | controlled | 61 | 9 | 1 | 0 | 71 |
| supermemory | native | 33 | 3 | 0 | 0 | 36 |
| baselayer | controlled | 88 | 11 | 2 | 0 | 101 |

### Same, all-14-subjects scope

| System | Config | 1-band | 2-band | 3-band | 4-band | Total upward |
|---|---|---|---|---|---|---|
| mem0 | controlled | 114 | 13 | 4 | 0 | 131 |
| mem0 | native | 158 | 32 | 11 | 1 | 202 |
| letta | controlled | 120 | 28 | 4 | 1 | 153 |
| letta | native | 107 | 4 | 1 | 0 | 112 |
| zep | controlled | 131 | 26 | 2 | 1 | 160 |
| zep | native | 152 | 33 | 8 | 0 | 193 |
| supermemory | controlled | 83 | 12 | 1 | 0 | 96 |
| supermemory | native | 39 | 3 | 0 | 0 | 42 |
| baselayer | controlled | 124 | 17 | 4 | 0 | 145 |

---

## Sanity check vs §4.4 wins/losses

§4.4 wins/losses uses Δ ≥ +0.3 (or ≤ −0.3) thresholds at the subject mean level. Anchor-crossing here uses integer-band crossing at the question level. The two metrics are not identical (a Δ of +0.4 may not cross an integer band, and a within-question swing of e.g. 1.9 -> 2.1 crosses an anchor without producing a +0.3 subject-level delta) but should agree in direction.

Direction-of-effect check on low-baseline scope (upward % vs downward %):

| System | Config | Up % | Down % | Net | KEY_FINDINGS Δ_spec |
|---|---|---|---|---|---|
| mem0 | controlled | 23.4% | 18.8% | +4.6 pp | +0.12 |
| mem0 | native | 36.1% | 14.9% | +21.2 pp | +0.33 |
| letta | controlled | 26.9% | 19.4% | +7.4 pp | n/a |
| letta | native | 19.9% | 19.9% | +0.0 pp | n/a |
| zep | controlled | 27.9% | 19.7% | +8.3 pp | +0.19 |
| zep | native | 32.5% | 13.7% | +18.8 pp | +0.33 |
| supermemory | controlled | 20.2% | 22.5% | -2.3 pp | n/a |
| supermemory | native | 23.4% | 19.5% | +3.9 pp | n/a |
| baselayer | controlled | 29.0% | 21.6% | +7.5 pp | spec is the primary arm |

Direction-of-effect read:

- **Mem0, Zep, BaseLayer, Letta controlled:** all show positive net upward (up % > down %), agreeing with §4.4 / KEY_FINDINGS positive Δ_spec deltas.
- **Letta native:** net 0.0 pp (19.9% up, 19.9% down) — the bilateral per-question swings (m15 mixture-of-swings) cancel at the integer-band level, consistent with §4.4 reporting Letta archival as near-null in the native config.
- **Supermemory controlled:** small net negative (20.2% up, 22.5% down) — agrees with KEY_FINDINGS §4.4.2 ("Supermemory mixture", aggregate near-zero on low-baseline slice; 57 helps / 53 hurts at the Δ ≥ 0.3 threshold).
- **Supermemory native:** missing 4 of 9 low-baseline subjects (data on 5 subjects only — see per-system table) so this row is partial.

No system shows a contradictory direction relative to its §4.4 wins/losses delta. Magnitudes differ (anchor-crossing requires moving across an integer line, which is a stricter / lossier signal than a +0.3 mean delta), but the rank ordering across systems matches.
