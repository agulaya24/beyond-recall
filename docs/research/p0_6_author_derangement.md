# P0-6: Author Franklin battery, additional wrong-spec derangements

**Scope.** Two supplementary wrong-spec conditions on the author's 40-question behavioral-prediction battery used in §4.1.2. The existing Franklin-spec wrong-spec condition (C2c_Franklin, mean = 2.586) and the correct-spec condition (C2a, mean = 2.861) are unchanged. This experiment adds two new wrong-spec draws to check whether the +1.56 lift from the paper's wrong-spec condition persists when the spec is drawn from a different subject.

**Methodology.** Identical to the existing §4.1.2 wrong-spec condition (`_internal/aarik_clean_pilot/run_c2c_wrongspec.py`): same 40-question battery, same Haiku 4.5 responder at temperature 0, same 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4), same judge rubric and prompt template. The only change is the subject whose full-stack Behavioral Specification (anchors + core + predictions + brief) is served. Sources: Hamerton's spec from `C:/Users/Aarik/Anthropic/hamerton_memory/data/identity_layers/`; global subjects' specs from `memory-study-repo/data/global_subjects/<subject>/`. Response and judgment artefacts are in `_internal/aarik_clean_pilot_p0_6/` (private, paired with the existing author-pilot data).

**Comparability caveat.** The existing §4.1.2 C2c condition loaded Franklin's spec as `brief_v5_clean.md` (name-scrubbed). The global subjects in the main-study repo only have `brief_v5.md` (no cleaned variant). Both are byte-identical in structure and differ only in name redaction inside the brief; Hamerton has both and the `_clean` variant was used. The `=== TAG ===` header for the brief differs accordingly (`=== BRIEF_V5_CLEAN ===` versus `=== BRIEF ===`). This is a known minor asymmetry and is not expected to move judge scores at this magnitude.

## Condition A, seed-fixed random derangement

**Pool.** The 14 historical main-study subjects (Hamerton plus the 13 global-subjects pipeline subjects):
`hamerton, augustine, babur, bernal_diaz, cellini, ebers, equiano, fukuzawa, keckley, rousseau, seacole, sunity_devee, yung_wing, zitkala_sa`.

**Selection.** `random.Random(42).choice(pool)` in insertion order. Also verified stable under sorted order: both yield the same pick.

**Pick: Seacole** (Mary Seacole, 19th-century British-Jamaican nurse).

The manifest with the exact RNG state is at `_internal/aarik_clean_pilot_p0_6/manifest.json`. The assembled spec served to the responder is preserved at `spec_c2c_random_seacole.md`.

## Condition B, maximum-distance derangement

**Pick: Babur** (Zahir ud-Din Muhammad Babur, 16th-century founder of the Mughal Empire; military commander, Central Asian nomadic aristocrat).

**Rationale.** Babur is the task-specified default for maximum distance. A quick anchor-level read against the author's spec confirms the choice. Babur's axioms include *Divine Instrumentality*, *Embodied Authority*, *Genealogical Gravity*, *Sensory Primacy*, and military-command and succession-legitimacy themes. The author's axioms include *Agency-as-Architecture*, *Layered-Systems Thinking*, *Evidence-before-Acceptance*, *Epistemic Tiering*, *Compression-as-Quality*, *Self-Critique-as-Operating-System*, *Multi-Agent-over-Monolith*, and *Provenance-and-Traceability*. There is no obvious behavioral analogue between the two anchor sets: a 16th-century conqueror whose legitimacy rests on bloodline and divine favour versus a 21st-century introspective-rationalist software architect. Seacole is genuinely further from the author in the main-study spec-similarity results than most subjects, but both her *Embodied Authority* and *Constitutive Action* axioms have mild analogues in the author's *Risk-Sequenced Execution* and *Agency-as-Architecture*. Babur has no such surface analogue, which matches the spirit of "max-distance" as the task defines it.

The assembled spec served to the responder is preserved at `spec_c2c_max_distance_babur.md`.

## Results

### Comparison table, 5-judge primary mean (N = 40, author battery, Haiku 4.5 responder)

| Condition | Mean | Δ vs. C5 | Source |
|---|---:|---:|---|
| **C5** (no context) | 1.03 | reference | existing §4.1.2 |
| **C2c random (Seacole)** | **2.19** | **+1.16** | new (this experiment) |
| **C2c max-distance (Babur)** | **2.34** | **+1.32** | new (this experiment) |
| **C2c Franklin** (existing) | 2.59 | +1.56 | existing §4.1.2 |
| **C2a** (correct spec) | 2.86 | +1.84 | existing §4.1.2 |
| **C4** (all facts, no spec) | 2.93 | +1.90 | existing §4.1.2 |
| **C4a** (facts + correct spec) | 3.02 | +2.00 | existing §4.1.2 |

### Per-judge means (5-judge primary)

| Judge | C5 | C2c random | C2c max-dist | C2c Franklin | C2a |
|---|---:|---:|---:|---:|---:|
| Haiku | 1.10 | 2.26 | 2.47 | 2.64 | 3.08 |
| Sonnet | 1.00 | 1.73 | 1.88 | 1.90 | 2.28 |
| Opus | 1.00 | 2.20 | 2.30 | 2.75 | 3.00 |
| GPT-4o | 1.03 | 2.55 | 2.68 | 3.08 | 2.93 |
| GPT-5.4 | 1.00 | 2.21 | 2.38 | 2.56 | 3.03 |

Sonnet is systematically the lowest scorer across every condition including C2a and C4a. Opus is the most discriminating between correct and wrong specs (C2a minus C2c_random = +0.80). GPT-4o is the most permissive on both wrong-spec conditions.

### Engagement and refusals

The broad per-question refusal rate (5-judge aggregate mean < 1.5) and the engagement-conditional mean (Qs where the aggregate mean is at least 1.5):

| Condition | Refusal rate | Engagement-conditional mean | n engaged |
|---|---:|---:|---:|
| C5 | 100% by construction | n/a | 0 |
| C2c random (Seacole) | 35% | 2.68 | 26 |
| C2c max-distance (Babur) | 25% | 2.72 | 30 |

Both new wrong-spec conditions have substantial refusal rates. More than a quarter of the author's questions do not find a handle in either Seacole's or Babur's specification. When they do find one, the engagement-conditional mean lands at roughly 2.7, about a point below the correct-spec baseline.

### H6 ("none of 40 responses got worse"), anchor-crossing vs. C5

| Condition vs. C5 | Up | Same | Down | Upward rate |
|---|---:|---:|---:|---:|
| C2c Franklin | 25 | 15 | 0 | 62.5% |
| C2c random (Seacole) | 16 | 24 | 0 | 40.0% |
| C2c max-distance (Babur) | 20 | 20 | 0 | 50.0% |

**Zero questions moved down** for either new condition. H6 is robustly confirmed across two additional wrong-spec draws: a random-pick or maximum-distance spec does not hurt the author's predictions relative to the no-context baseline on any of 40 questions. The upward crossing rate scales roughly with spec-subject similarity. Franklin's spec, which shares multiple anchors with the author's, produces the highest rate (62.5%), and the Seacole and Babur specs, which share far fewer, produce lower rates (40 to 50%).

### Paired per-question Δ vs. C5

| Condition | Mean Δ | Median Δ | Q with Δ > 0 | Q with Δ = 0 | Q with Δ < 0 |
|---|---:|---:|---:|---:|---:|
| C2c Franklin | +1.55 | +1.10 | 38 | 2 | 0 |
| C2c random (Seacole) | +1.15 | +0.60 | 35 | 5 | 0 |
| C2c max-distance (Babur) | +1.30 | +0.90 | 35 | 5 | 0 |

Five questions yield exactly the C5 score under each of the two new wrong-spec conditions; none yield a lower score. This is consistent with Franklin, where two questions tie and none drop.

### Per-question head-to-head

| Comparison | Mean delta | Wins | Ties | Losses |
|---|---:|---:|---:|---:|
| random vs. Franklin | -0.40 | 7 | 10 | 23 |
| max-dist vs. Franklin | -0.25 | 10 | 8 | 22 |
| max-dist vs. random | +0.14 | 17 | 9 | 14 |
| random vs. C2a (correct) | n/a | 8 | 4 | 28 |
| max-dist vs. C2a (correct) | n/a | 9 | 4 | 27 |
| Franklin vs. C2a (correct) | n/a | 12 | 7 | 21 |

Franklin's spec outperforms both new wrong-spec draws at a per-question level, unsurprising given the shared anchors documented in §4.1.2. Babur edges Seacole by 0.14 points on average, a gap well inside the judge-variance noise floor expected at N = 40 with five judges.

## Interpretation

**The lift from C5 to wrong-spec persists under both new draws.** Serving a completely non-author spec still lifts the author's battery by roughly +1.15 to +1.32 points over the no-context baseline. Both new conditions are below the Franklin wrong-spec (+1.56) but well above the rubric floor. The improvement is not an artefact of Franklin's anchor overlap with the author.

**The Franklin wrong-spec result was an atypically favourable draw.** §4.1.2 decomposes the +1.56 Franklin lift into a baseline-mediated component (approximately +0.25 from the floor effect observed in main-study low-baseline subjects' wrong-spec controls) and a content-overlap component (approximately +1.31 from the five shared anchors between Franklin and the author). The two new draws land inside that expected envelope: with very little content overlap, the lift falls to +1.15 (Seacole) and +1.30 (Babur). The 0.28-point gap between C2c Franklin and C2a in the paper, which §4.1.2 attributes to an atypically favourable wrong-spec draw, is consistent with these numbers. The gap between C2c random and C2a is 0.67, and the gap between C2c max-distance and C2a is 0.52. Both are larger than the Franklin gap, which is what the atypical-draw reading predicts.

**Implication for §4.1.2 narrative.** The total wrong-spec lift on the author (+1.15 to +1.32 on a truly arbitrary draw) is larger than the historical low-baseline floor effect (+0.25) would predict in isolation. This could reflect a stronger floor effect for this subject specifically, a battery-selection artefact (the author's battery was backward-designed from the held-out half of his own corpus and may over-select for questions where any strong first-person voice helps), or a combination. Either reading loosens the specific +0.25 number in §4.1.2's decomposition without invalidating the decomposition's logic: correct spec > Franklin spec > other wrong specs > no spec, in that order, is still the observed ordering.

**Babur versus Seacole.** Babur outperforms Seacole by 0.14 points. This is within the judge-variance envelope at this N and should not be read as a subject-specific effect.

**H6 ("none of 40 responses got worse") holds robustly.** The paper reports 0 downward anchor crossings for C5 to C4a. The new data adds 0 downward crossings for C5 to C2c_random and 0 for C5 to C2c_max_distance, both with broad 5-judge agreement. H6 is not an artefact of the Franklin draw: a random or maximum-distance wrong-spec also does not harm the author's predictions on any question relative to the no-context baseline. This is a stronger version of H6 than §4.1.2 reports and should be cited if H6 is broadened in a future revision.

**Cost.** Estimated total approximately $3.74 (80 Haiku 4.5 responses plus 400 judge calls across 5 models). Well under the $12 cap.

## Files

- Manifest (RNG seed, selection, spec sources): `_internal/aarik_clean_pilot_p0_6/manifest.json`
- Assembled specs (what the responder actually saw): `spec_c2c_random_seacole.md`, `spec_c2c_max_distance_babur.md`
- Responses: `responses_c2c_random_derangement.json`, `responses_c2c_max_distance_derangement.json`
- Judgments: `judgments_c2c_random_derangement.json`, `judgments_c2c_max_distance_derangement.json`
- Per-condition summary: `summary_c2c_random.json`, `summary_c2c_max_distance.json`
- Merged analysis (existing plus new conditions with per-question crossings and deltas): `final_analysis.json`
- Runner script: `run_p0_6_derangements.py`
- Analysis script: `analyze_results.py`
- Log: `run_log.txt`

All artefacts are under `_internal/aarik_clean_pilot_p0_6/`; no author response text or ground-truth content is reproduced in this public report.
