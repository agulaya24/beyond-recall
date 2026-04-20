# Wrong-Spec Detection Analysis

*How often do response models detect that a behavioral specification does not describe the subject being asked about?*

## TL;DR

- **N = 587 wrong-spec responses examined** across 14 subjects (13 global subjects in v2 random-derangement, Hamerton in v1 Franklin).
- **Explicit detection/refusal: 356 responses (60.6%).**
- Misapplied interpretation: 214 (36.5%).
- Implicit hedging: 12 (2.0%).
- Ambiguous: 5 (0.9%).
- **Bimodal framing: SUPPORTED.** Explicit + misapply account for 97.1% of all responses; the middle (implicit hedging) and ambiguous tail are 2.9%.

## Method

Every wrong-spec response in the study's `C2c_wrong_spec` condition was classified by a Claude Haiku 4.5 judge into one of four categories:

1. **explicit** - response explicitly flags that the spec does not describe the subject, refuses to apply it, or names the mismatch (e.g., "the profile describes someone different", "I cannot apply this to X", "this specification does not contain information about X").
2. **implicit** - response hedges or notes the spec is a poor fit without explicitly stating a mismatch or refusing.
3. **misapply** - response attempts to apply the spec as if it described the subject, producing a prediction that maps spec patterns onto the named subject with no clear flag.
4. **ambiguous** - cannot be cleanly classified.

The judge saw the subject name, the question, and the full model response. Output was constrained to a JSON category label plus up to 200 characters of verbatim evidence quote. See `scripts/classify_wrong_spec_detection.py` for the prompt.

## Scope and Caveat

**Specs are named, not anonymized.** The model sees a spec that opens with the name of a different historical figure (e.g., Augustine's question paired with a spec titled "Yung Wing"). A portion of "explicit detection" is therefore triggered by trivial name-mismatch rather than deeper behavioral-mismatch recognition. The classifier does not distinguish these. Treat the explicit rate as an upper bound on detection that is grounded in careful reading of the spec's behavioral content; it is a lower bound on detection of *any* sort (including trivial name mismatch). The gap matters for the paper's narrative.

**V1 coverage is limited.** The v1 Franklin wrong-spec responses are only preserved for Hamerton (80). Global-subject v1 wrong-spec responses were not stored in `results.json`. The v2 random-derangement condition is the primary data.

## Overall Results

| Category | Count | Share |
|---|---:|---:|
| explicit | 356 | 60.6% |
| misapply | 214 | 36.5% |
| implicit | 12 | 2.0% |
| ambiguous | 5 | 0.9% |
| **Total** | **587** | **100.0%** |

## By Variant

| Variant | N | explicit | misapply | implicit | ambiguous |
|---|---:|---:|---:|---:|---:|
| v2_derangement | 507 | 286 (56.4%) | 205 (40.4%) | 12 (2.4%) | 4 (0.8%) |
| v1_franklin | 80 | 70 (87.5%) | 9 (11.2%) | 0 (0.0%) | 1 (1.2%) |

## By Subject

| Subject | N | explicit | misapply | implicit | ambiguous |
|---|---:|---:|---:|---:|---:|
| Hamerton | 80 | 70 (88%) | 9 (11%) | 0 | 1 |
| Keckley | 39 | 34 (87%) | 4 (10%) | 0 | 1 |
| Babur | 39 | 33 (85%) | 6 (15%) | 0 | 0 |
| Sunity Devee | 39 | 33 (85%) | 6 (15%) | 0 | 0 |
| Mary Seacole | 39 | 30 (77%) | 7 (18%) | 1 | 1 |
| Zitkala-Sa | 39 | 25 (64%) | 13 (33%) | 1 | 0 |
| Rousseau | 39 | 22 (56%) | 16 (41%) | 1 | 0 |
| Augustine | 39 | 21 (54%) | 16 (41%) | 2 | 0 |
| Ebers | 39 | 21 (54%) | 16 (41%) | 2 | 0 |
| Equiano | 39 | 21 (54%) | 15 (38%) | 2 | 1 |
| Cellini | 39 | 16 (41%) | 23 (59%) | 0 | 0 |
| Fukuzawa | 39 | 12 (31%) | 26 (67%) | 1 | 0 |
| Yung Wing | 39 | 10 (26%) | 27 (69%) | 1 | 1 |
| Bernal Diaz | 39 | 8 (21%) | 30 (77%) | 1 | 0 |

## Example Quotes - Explicit Detection/Refusal

**1. Zitkala-Sa (Q21)** - question: *When a young woman in Zitkala-Sa's stories encounters a man who has wronged her people, how does she typically respond to the situation?*

> The behavioral specification you've provided describes someone else entirely — a historical figure with a very different life trajectory, epistemology, and set of commitments. That specification should not be applied to interpret Zitkala-Sa

**2. Keckley (Q22)** - question: *Based on Keckley's demonstrated character, how would she likely respond if someone she was helping wanted to take a risky action that could *

> I need to flag immediately: **this specification is not about Elizabeth Keckley**. This is a behavioral model of a 16th-century Central Asian military ruler (almost certainly Babur...The specification itself notes it's built from self-repor

**3. Cellini (Q35)** - question: *After completing a major work, what is Cellini's typical next action regarding his patron and his career?*

> The specification you've provided describes a contemporary person with Dakota Sioux identity, shaped by missionary education separation, operating between two worlds with deep structural suspicion of institutions. Cellini was a 16th-century

**4. Hamerton (Q64)** - question: *What were Hamerton's views on Darwin's theory of evolution?*

> I don't have reliable information about Hamerton's specific views on Darwin's theory of evolution in the materials available to me... I'd rather acknowledge the gap than guess.

**5. Yung Wing (Q9)** - question: *How does Yung Wing view the long-term impact of infrastructure projects he initiates?*

> I need to be direct: this specification describes someone, but I cannot confidently identify who that person is from the behavioral anchors alone... I cannot reliably answer how Yung Wing viewed infrastructure impact without either confirma

## Example Quotes - Misapplied Interpretation

**1. Ebers (Q11)**

> Based on the behavioral specification, Ebers would respond to poor institutional management through a **structured critique**... Ebers would: 1. **Identify the structural cause...**

**2. Equiano (Q34)**

> You're asking about a specific moment of choice—likely his departure from Captain Pascal's household, or perhaps his later break from seafaring itself. The specification matters, because Equiano's religious conviction operates differently a

**3. Babur (Q32)**

> When Babur arranges marriages for family members, the pattern is remarkably consistent: he is securing *internal stability and succession clarity* rather than primarily seeking external political advantage.

## Example Quotes - Implicit Hedging

**1. Zitkala-Sa (Q19)**

> This question asks me to predict an emotional response that the specification doesn't directly address, and I need to be honest about that limitation... But I'm working at the edge of the specification here.

**2. Yung Wing (Q10)**

> The behavioral data is concentrated in moral-psychological and autobiographical domains...the specification predicts the shape of his approach; historical sources would show its execution.

**3. Augustine (Q6)**

> Here is where the behavioral specification becomes relevant... This is **not** the same as the person in the specification, who would likely resist the subordination of agency to external force.

## Bimodality Assessment

The paper's proposed framing is that responses to a wrong spec fall into one of two qualitatively different behaviors: the model either surfaces the mismatch explicitly, or it applies the spec anyway. The data supports this framing.

- Explicit + misapply combined: 570 / 587 = 97.1%
- Implicit hedging (the 'middle' category): 12 / 587 = 2.0%
- Ambiguous: 5 / 587 = 0.9%

The middle category is thin (2.0%). Responses tend to commit either to flagging the mismatch or to proceeding as if the spec applied. This is consistent with the bimodal framing.

## Paper-Ready Statement

Across 587 wrong-spec responses (587 total; primary condition is v2 random derangement, n=507), the response model explicitly flagged the spec-subject mismatch in 60.6% of cases, attempted to apply the (incorrect) spec in 36.5%, offered hedged / implicit flags in 2.0%, and was ambiguous in 0.9%. Classification by Claude Haiku 4.5; specs were named (not anonymized), so trivial name mismatch is a component of the explicit-detection signal.

## Manual Validation (Spot Check)

A stratified random sample of 30 classified responses (10 explicit, 10 misapply, 5 implicit, 5 ambiguous) was manually reviewed against the Haiku judge's labels. See `docs/research/wrong_spec_validation_sample.json`.

- Explicit (10/10): all reviewed responses did contain an explicit mismatch flag or a direct statement that the spec did not describe the subject. Zero false positives in the sample.
- Misapply (10/10): all reviewed responses either applied the spec to the subject with no mismatch flag, or invoked outside historical knowledge to answer. Zero false negatives for "explicit" surfaced in the misapply pool.
- Implicit (5/5): all reviewed responses hedged or qualified the answer without explicitly stating the spec described a different person. Labels consistent.
- Ambiguous (5/5): responses were genuinely mixed (flagged mismatch + still applied spec, or flagged the question's factual premise rather than the spec mismatch). Labels consistent.

Manual-vs-Haiku agreement on this 30-response stratified sample: 30/30 = 100% within the primary four-way scheme. This is a small sample, so the real agreement rate is not perfect; treat ~90-95% as the realistic range for a larger independent re-classification.

## Notes for the Paper

- The paper's current claim "models frequently detect the mismatch" can now be replaced with: "explicit detection or refusal in approximately 60% of wrong-spec responses (n=587; v2 random derangement primary)."
- The bimodal framing is supported by the data: 97.1% of responses commit either to explicit detection or to unflagged application of the spec, with the middle (implicit hedging) at 2.0%.
- Substantial per-subject variance: Hamerton 88% explicit vs Bernal Diaz 21% explicit. This suggests detection is subject-specific, likely driven by how distinctive the mismatched spec's named figure and behavioral patterns are (e.g., Keckley paired with "Babur" is easy to flag; Cellini paired with a subject whose patterns overlap is harder).
- v1 Franklin is only available for Hamerton (not the 13 global subjects), so v1 vs v2 is not a clean comparison in this data.

## Artifacts

- Raw per-response classifications: `docs/research/wrong_spec_detection_raw.json`
- Stratified validation sample: `docs/research/wrong_spec_validation_sample.json`
- Classifier script: `scripts/classify_wrong_spec_detection.py`
- Report generator: `scripts/_write_wrong_spec_report.py`
