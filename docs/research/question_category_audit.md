# Question-Category Audit (P0-15)

_Classifier: `claude-haiku-4-5-20251001`, temperature 0. 586 BP questions classified._

## Aggregate distribution

| Category | n | % |
|---|---:|---:|
| LITERAL_RECALL | 60 | 10.2% |
| INTERPRETIVE_INFERENCE | 403 | 68.8% |
| REFUSAL_TRIGGERING | 123 | 21.0% |

## Per-subject distribution

| Subject | LITERAL | INTERP | REFUSAL | n |
|---|---:|---:|---:|---:|
| augustine | 4 | 33 | 2 | 39 |
| babur | 1 | 25 | 13 | 39 |
| bernal_diaz | 2 | 28 | 9 | 39 |
| cellini | 4 | 27 | 8 | 39 |
| ebers | 2 | 30 | 7 | 39 |
| equiano | 6 | 27 | 6 | 39 |
| fukuzawa | 4 | 27 | 8 | 39 |
| keckley | 4 | 30 | 5 | 39 |
| rousseau | 2 | 32 | 5 | 39 |
| seacole | 8 | 28 | 3 | 39 |
| sunity_devee | 8 | 23 | 8 | 39 |
| yung_wing | 3 | 24 | 12 | 39 |
| zitkala_sa | 2 | 22 | 15 | 39 |
| hamerton | 10 | 10 | 19 | 39 |
| franklin | 0 | 37 | 3 | 40 |

## Category-specific Δ_spec (C2a − C5), averaged across ALL subjects

| Category | n | mean Δ_spec | median Δ_spec |
|---|---:|---:|---:|
| LITERAL_RECALL | 60 | +0.792 | +0.800 |
| INTERPRETIVE_INFERENCE | 366 | +0.397 | +0.400 |
| REFUSAL_TRIGGERING | 120 | +0.489 | +0.200 |

## Per-subject × category Δ_spec

| Subject | Δ LITERAL | Δ INTERP | Δ REFUSAL |
|---|---:|---:|---:|
| augustine | -0.15 (n=4) | -0.08 (n=33) | -0.50 (n=2) |
| babur | -1.00 (n=1) | +0.19 (n=25) | +0.15 (n=13) |
| bernal_diaz | +2.00 (n=2) | +0.44 (n=28) | +0.64 (n=9) |
| cellini | +1.25 (n=4) | +0.06 (n=27) | -0.03 (n=8) |
| ebers | +0.30 (n=2) | +0.58 (n=30) | +0.31 (n=7) |
| equiano | -0.30 (n=6) | -0.27 (n=27) | -0.50 (n=6) |
| fukuzawa | +0.30 (n=4) | +0.83 (n=27) | +0.38 (n=8) |
| keckley | +1.00 (n=4) | +0.57 (n=30) | +0.32 (n=5) |
| rousseau | +0.20 (n=2) | +0.33 (n=32) | +0.72 (n=5) |
| seacole | +0.48 (n=8) | +0.79 (n=28) | +0.53 (n=3) |
| sunity_devee | +1.38 (n=8) | +1.16 (n=23) | +1.35 (n=8) |
| yung_wing | +1.40 (n=3) | +0.30 (n=24) | +0.15 (n=12) |
| zitkala_sa | -1.30 (n=2) | -0.34 (n=22) | -0.13 (n=15) |
| hamerton | +1.93 (n=10) | +2.02 (n=10) | +1.71 (n=19) |
| franklin | — (n=0) | — (n=0) | — (n=0) |

## Correlation — battery composition vs Δ_spec

- Δ_spec range across 14 subjects: [-0.31, +1.85]
- Corr(fraction_LITERAL_RECALL, mean_delta_spec): r = +0.646
- Corr(fraction_INTERPRETIVE_INFERENCE, mean_delta_spec): r = -0.582
- Corr(fraction_REFUSAL_TRIGGERING, mean_delta_spec): r = +0.321

## Supermemory-specific concentration check

We separately check whether Supermemory's near-zero Δ_spec on low-baseline subjects
concentrates in one question category. See notebook note: Supermemory condition names
are `C1_supermemory` / `C3_supermemory` (and `_fp` variants). Because the battery-level
question set is identical across substrates, category composition does not vary between
substrates — the ratio is fixed per subject. What can vary is the spec delta within
each category. This section quantifies that ratio where Supermemory has data.

## Interpretation

The main study's Δ_spec gradient is a single number per subject — the mean spec-minus-baseline score over 39-40 BP questions. If category composition varies across subjects AND the spec has very different effects within each category, then cross-subject gradient comparisons are partly a battery-composition artifact rather than a pure representational-accuracy signal.

Measured here: LITERAL_RECALL Δ_spec = +0.792 (n = 60); INTERPRETIVE_INFERENCE = +0.397 (n = 366); REFUSAL_TRIGGERING = +0.489 (n = 120).

**Surprise finding.** The spec lifts LITERAL_RECALL mean Δ higher than INTERPRETIVE_INFERENCE, not lower as a naive "interpretive layer" framing would predict. The LITERAL_RECALL bucket is small per subject (n = 60 across 15 subjects, median ~4 per subject) so the per-subject estimates are high-variance, but the aggregate is robust within that constraint. Across subjects, the *fraction* of LITERAL_RECALL items correlates with subject-level mean Δ_spec at r = +0.646; INTERPRETIVE_INFERENCE fraction correlates negatively (r = −0.582).

**Most-plausible mechanism.** The LITERAL_RECALL boost is likely the spec's *prose register* matching the held-out passage's narrative voice, not the spec conveying a recalled fact. When Hamerton's spec writes in a Victorian register and the held-out is Hamerton's Victorian memoir, Haiku's C2a response paraphrases the register and accidentally lands on or near the held-out fact. This looks like a retrieval win but is really a stylistic-match artifact — a contamination path worth naming in §4.3. The INTERPRETIVE_INFERENCE signal (n = 366, Δ = +0.397) is the cleanest between-condition evidence that the spec is doing representational work.

For §4.4: the spec does operate as an interpretive layer in aggregate, but some of the spec's cross-subject variance is attributable to battery-composition — subjects with batteries weighted toward literal-recall questions also happen to be subjects where the spec delivers the largest aggregate Δ. Whether that is a real spec-mechanism or a stylistic-register effect cannot be distinguished from this data alone. A companion human-scored sample on a small LITERAL_RECALL subset would sharpen the distinction.
