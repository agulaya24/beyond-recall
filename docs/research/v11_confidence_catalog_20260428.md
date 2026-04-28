# V11 Confidence Catalog

_Date: 2026-04-28_
_Purpose: Anchor every claim in the Beyond Recall v11 paper at its appropriate confidence level, after the full wins-analysis pipeline._

This catalog is the source of truth for what the paper does and does not assert. Every body-text claim in v11 should map to one of these levels. Claims at HIGH confidence go in body. Claims at MEDIUM go in body with appropriate hedge. Claims at LOW or UNRESOLVED go in future work or are not made.

## HIGH CONFIDENCE — body claim, asserted directly

### H1. The Behavioral Specification changes the model's behavior on subject-prediction questions

**Evidence:**
- C5 (no spec) vs C2a (spec only) on low-baseline subjects: mean +0.71 lift
- C5 vs C4a (facts + spec): mean +0.89 lift
- 55% of low-baseline questions cross at least one rubric integer anchor upward under C4a
- Wilcoxon signed-rank on the 9 low-baseline subjects: W=11, N=14, p=0.007
- Hedging reduction 28.8% → 0.0% on facts + spec

This is the strongest claim in the paper. Spec presence vs absence produces a measurable, statistically significant, and behaviorally-distinct change in model output.

### H2. On the cross-subject mean, the spec's effect is positive on the population of relevance (low-baseline subjects)

**Evidence:**
- 9 of 9 low-baseline subjects improve under facts + spec (mean Δ_C4a = +0.89, all positive)
- 12 of 14 overall subjects improve
- Per-subject anchor-crossing rates range 25.6% (Babur) to 74.4% (Sunity Devee), all above zero

The mean is the appropriate primary metric. Per-subject means are what the paper reports.

### H3. There is real distribution around the mean. Per-question variance is substantial

**Evidence (added in v11):**
- Across all 18 condition pairs: 4,206 anchor crossings + 759 same-band ≥0.5 within-band shifts + 995 same-band 0.25-0.5 shifts (Stream Y)
- C5→C4a low-baseline: 55% upward crossings, 6.8% downward, 38% no movement
- Multi-anchor jumps (≥2 bands): 18% of low-baseline questions; extreme jumps (≥3 bands): 6%
- Direction asymmetry: no transitions from band 2, 3, or 4 into band 5 across the full 14-subject panel; only band-1 → band-5 transitions reach the ceiling
- Per-question anchor-crossing data is in `docs/research/wins_inventory_20260428.json` and §4.4.2 / Appendix D

The aggregate Δ is a residue of substantial per-question variance, not a uniform lift. Large lifts and degradations both occur. The mean is positive because lifts outweigh degradations on the population of relevance.

### H4. The content of the spec specifically matters; structured prompting alone does not produce the lift

**Evidence:**
- Adversarial wrong-spec C2c (paired to maximize cultural and temporal distance): Δ = −0.25, below baseline
- Random-derangement wrong-spec: Δ = +0.15 (small positive)
- Correct spec C2a: Δ = +0.35
- The gap between adversarial and correct is 0.60 anchor points

Wrong content actively degrades performance below baseline; correct content lifts. This is the paper's primary indirect mechanism evidence: content matters, not just structure.

### H5. Compression: a 7K-token spec recovers most of the predictive signal of the full source corpus

**Evidence:**
- C2a (7K-token spec) vs C8 (raw corpus, 80K-400K tokens): C2a captures roughly three-quarters of the corpus-alone lift
- C4a (facts + spec) and C8 produce essentially identical means (~2.45)
- Per-subject compression ratios in §4.2

The behaviorally relevant signal in autobiographical text is sparse and compressible.

### H6. The integer-anchor metric is 18% lossy

**Evidence (added in v11):**
- Stream Y: half-anchor (≥0.5 same-band) shifts add ~18% to recorded movement beyond the binary anchor-crossing metric
- Panel detects sub-anchor signal: 74% direction-agreement at panel |Δ| 0.1-0.25, 93% at 0.25-0.5

This is methodological transparency, not a new finding. The paper acknowledges the metric is a lower bound on movement detectable.

## MEDIUM CONFIDENCE — body claim with hedge

### M1. The spec's measurable effect is concentrated on a subset of question types where the model's pretraining footprint is thin

**Evidence:**
- LITERAL_RECALL questions are 2.77x overrepresented in extreme upward anchor crossings (28.3% vs 10.2% panel-wide)
- 71.7% of pre-responses on extreme-jump cases are FULL_REFUSAL
- Hamerton's elevated jump rate (18.75%) vs other low-baseline subjects (8.9%) suggests subject-thinness correlation

This is the "spec is the tool for the unknown" framing. The hedge: we cannot fully disentangle subject thinness from battery-generator effects (Hamerton's battery used a legacy generator). This belongs in the paper but framed as observational not causal.

### M2. Two distinct statistical signatures exist for spec-on-baseline vs spec-on-info-rich-context

**Evidence:**
- Stream Y: spec-on-baseline (C5→C4a) Spearman ρ between pre and post per-question scores = 0.27 (re-ranks)
- Spec-on-info-rich (C4→C4a, C8→C9) Spearman ρ ≈ 0.71 (uniformly lifts)
- Different per-question dynamics under different contexts

The hedge: floor-effect alternative is not ruled out. Spec-on-baseline could have lower ρ partly because baseline scores cluster at the rubric floor (1-2 range) where re-ranking is structurally easier. This belongs as a small section in §4.4 + future-work bullet, framed as "two statistical signatures" not "two mechanisms."

## LOW CONFIDENCE — future work, not asserted in body

### L1. Specific within-spec content (which behavioral predicate, which spec section) drives the lift

**Evidence (Phase 2c, appendix only):**
- Predicate ablation on 16 cases: removal of single rater-identified predicate produced Δ_removal = +0.05 (CI95 [-0.35, +0.45]); reversal produced Δ_reversal = -0.24 (CI95 [-0.45, -0.02])
- Single-predicate removal does not measurably reduce response quality
- Consistent with redundant spec construction: multiple sentences reinforce the same behavioral patterns

This does NOT contradict H1 or H4. It says we cannot identify a uniquely load-bearing predicate via per-sentence ablation. The high-level mechanism question (does the spec cause the lift?) is settled by H1+H4. The internal mechanism question (which part) remains open. Future work: human-rated predicate identification, larger N, irrelevant-predicate control, multi-predicate cluster ablation.

### L2. The wins distribution suggests question-battery weaknesses

**Evidence:**
- LITERAL_RECALL overrepresented in extreme jumps (M1)
- Battery-question-type confound: subjects whose batteries lean LITERAL_RECALL also produce larger Δ_spec (Appendix B.6)
- Hamerton's elevated jump rate may be partly battery-generator artifact

The hedge: future work needs a category-balanced battery designed specifically for spec evaluation. The current battery wasn't designed with spec-evaluation in mind; it was designed for the broader prediction task. This is an honest methodological limitation and belongs in §6 + §7.

### L3. Generalization from autobiographers to "anyone who uses AI"

**Evidence:**
- 14 historical autobiographers as subjects
- Constructive argument: subjects with thin pretraining footprint are the closest available proxy for the population of typical AI users (whose reasoning is not in any training corpus)

This is a constructive leap, not an empirical generalization. The paper has language acknowledging this. Multi-subject living-user replication is flagged as the leading follow-up in §7.

## UNRESOLVED — explicitly acknowledged as open

### U1. The internal mechanism by which the spec produces lift

H1 and H4 establish that the spec causes the lift and that content matters. But which structural feature of the spec (anchors / core / predictions / brief; specific predicate types; spec length; predicate density per word) is the active ingredient — UNRESOLVED. Phase 2c ruled out single-predicate uniqueness; the broader question is open.

### U2. Whether Hamerton's elevated rate is from spec format, battery generator, or subject thinness

Stream X erroneously claimed Hamerton has a "long unified-brief vs globals' six-section spec"; deeper analysis verified the inverse (Hamerton served spec is 1918 words; globals' served spec is ~5775 words). Hamerton's 2.1x extreme-jump rate vs other subjects is real but cause is not isolated.

### U3. Whether the LLM-as-judge panel measures behavioral pattern capture or grounded-feeling response style

The control group anomaly in deeper analysis (94.7% PATTERN_PREDICATE+HYBRID rate on non-jumping spec-loaded controls) suggests the LLM rater attributes pattern-grounding to ANY successful spec-loaded response. This is the rater-confabulation alternative the collective review flagged. Future work: human annotation on a calibration subset.

## What the paper SHOULD NOT claim

- "The mechanism is behavioral-predicate activation." Not supported by Phase 2c.
- "The spec uniquely lifts low-baseline subjects more than high-baseline ones." This is partly a coupling artifact; the data supports the opportunity-distribution reframing already in §4.1.
- "Wins" or "big wins" as paper-prose terminology. Replaced with "increases in representational accuracy" / "extreme upward anchor crossings" / "multi-anchor jumps."
- Headline claims based on the 60-case wins population. The wins population is illustrative, not headline.

## What the paper SHOULD claim

- The spec changes behavior (H1, asserted)
- The mean effect is positive on the population of relevance (H2, asserted)
- There is substantial per-question variance around the mean (H3, asserted with explicit table / subsection in §4.2)
- Content matters; wrong specs degrade (H4, asserted via existing §4.3)
- Compression: 7K-token spec captures most of the corpus signal (H5, asserted)
- Metric is a lower bound on movement (H6, methodological note in §3.6)
- Spec is most useful where pretraining footprint is thinnest (M1, asserted with hedge)
- Two statistical signatures, spec-on-baseline vs spec-on-info-rich (M2, small section in §4.4 with floor-effect caveat)
- Internal mechanism, battery weaknesses, generalization, and rater methodology questions: all in Future Work (L1, L2, L3, U1-U3)
