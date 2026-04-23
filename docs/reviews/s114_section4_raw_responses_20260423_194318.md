# V9 §4 Structure Review — Raw Responses
_Generated: 20260423_194318_

_Prompt length: 117925 chars_

---

## PROMPT SENT TO BOTH REVIEWERS


```
You are advising on the FORMATTING of Section 4 (Results) of a research paper titled "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization."

The author has made several structural decisions ALREADY. These are NOT open for debate. Do not argue against them. Only advise on FORMATTING and SUB-ORGANIZATION given these decisions.

## AUTHOR'S NON-NEGOTIABLE DECISIONS (accept as given)

1. All memory-provider results (Mem0, Supermemory, Zep, Base Layer) stay IN ONE SECTION together. No per-system top-level headings in §4.4.
2. Letta is the ONE exception. It breaks out because it has unique additional testing (archival-retrieval path + stateful-agent self-editing path) and an architecturally distinct memory model.
3. §4.6 "Interpretation vs. Recall" content folds INTO §4.4 (not its own section).
4. Keckley Q21 cross-system refusal stays as a named subsection. Place it within §4.4.
5. §4.5 Robustness moves to END of Results (after the consolidated §4.4 + the Letta §4.7 block).
6. §4.8 Scaling and Practical Implications moves OUT of Results entirely, into Discussion as §5.5 Practical Implications.

DO NOT relitigate any of the six points above. Advise only on the five formatting questions below.

## THE FIVE FORMATTING QUESTIONS

Q1. Within the consolidated §4.4, should per-system results be presented as:
    (a) one flat per-system comparison table plus unified discussion prose,
    (b) a comparison table plus per-system "micro-paragraphs" (1-2 sentences each), or
    (c) something else?

Q2. Where does the Keckley Q21 cross-system refusal sit? Inside §4.4 as a dedicated subsection (e.g. §4.4.2 or §4.4.3), or somewhere else within §4.4?

Q3. Should the §4.6 Pattern 1 / Pattern 2 / Pattern 3 (cross-system mechanism reproduction) content be:
    (a) integrated into §4.4 as a "common mechanisms" subsection,
    (b) pulled forward to §4.3 as an extension of the wrong-spec mechanism section, or
    (c) preserved as §4.4.x its own subsection with reference to per-system variation?

Q4. Given §4.4 will now carry Mem0 + Supermemory + Zep + Base Layer + cross-system mechanisms + Keckley Q21, what is the best subsection ORDERING for reader flow?

Q5. Is there anything in the current §4.4 or §4.6 that should be moved to an APPENDIX instead of integrated (the author prefers a tight body)?

## REQUIRED OUTPUT FORMAT

Respond in exactly this structure:

### Q1. Table format within §4.4
[2-4 sentences. Pick (a), (b), or (c) and say why. No hedging.]

### Q2. Placement of Keckley Q21
[2-4 sentences.]

### Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis
[2-4 sentences. Pick (a), (b), or (c) and say why.]

### Q4. Subsection ordering for reader flow
[One-paragraph justification plus the ordered list.]

### Q5. Appendix candidates
[Bullet list of specific subsections / paragraphs / tables that should go to appendix, or "none" with reasoning.]

### RECOMMENDED SUBSECTION TREE
[Provide a single concrete tree. Format:
§4.1 Title — one-line purpose
§4.2 Title — one-line purpose
§4.3 Title — one-line purpose
§4.4 Title — one-line purpose
  §4.4.1 Title — one-line purpose
  §4.4.2 Title — one-line purpose
  ...
§4.5 Title — one-line purpose
  §4.5.1 Title — one-line purpose
  ...
§4.6 Title — one-line purpose
  ...

Remember: §4.7 Letta stateful-agent breaks out (non-negotiable #2). §4.8 moves out entirely (non-negotiable #6). §4.5 Robustness moves to END of Results (non-negotiable #5). Reflect all of these in the tree. Use whatever final section number is natural for Robustness given it is last.]

### SINGLE BIGGEST RISK WITH THIS RESTRUCTURE
[2-3 sentences. What is the most important thing the author might get wrong when executing this?]

---

## CURRENT §4 RESULTS (v9 draft)

## 4. Results

This section reports the Behavioral Specification's effect on behavioral prediction across eight parts:

- **§4.1. The Cross-Subject Gradient.** The primary result, across 14 subjects.
- **§4.2. Compression: Structure vs. Raw Text.** Is the effect about structure or about information volume?
- **§4.3. Mechanism: Content, Not Format.** Does the content of the correct specification drive the effect, or does any structured prompt?
- **§4.4. Memory-System Composition.** Does the specification layer on top of existing commercial memory systems?
- **§4.5. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?
- **§4.6. Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level?
- **§4.7. Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution.
- **§4.8. Scaling and Practical Implications.** Cost, context, and deployment considerations.

Every number in §4 uses the 5-judge primary aggregate defined in §3.7.2 (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-judge sensitivity check (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported in §4.5. Score deltas are read through the anchor-crossing rule from §3.7.3: a delta that crosses a rubric integer anchor is a stronger claim than one that stays inside a single anchor band.

### 4.1 The Cross-Subject Gradient

**Hypotheses tested in this section** (from §1.2): H1. Adding the specification improves prediction. H2. The effect is inversely proportional to the response model's pretraining coverage. H2a (corollary, introduced here). On high-baseline subjects, the specification does not add value and mildly interferes.

---

**Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it.** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.2.1), every one of the 9 improves when the specification is added to the full fact set. None declines. Mean score lift: **+0.89 points**.

The mean number hides what is happening at the response level. **Of the 351 individual responses in the low-baseline slice, 55.0% crossed at least one rubric integer anchor upward when the specification was added.** The AI's answer moved from one category of response to a qualitatively different category.

| Transition | % of responses | What this means in plain terms |
|---|---:|---|
| 1 → 2 | **33.3%** | Refusal or off-base → generic engagement with the question |
| 1 → 3 | 12.3% | Refusal → partially-aligned prediction |
| 1 → 4 | 4.8% | Refusal → substantively-aligned prediction |
| 1 → 5 | 0.9% | Refusal → fully matches the held-out pattern |
| 2 → 3 | 2.0% | Generic → subject-specific |
| 2 → 4 | 0.3% | Generic → substantively-aligned |
| 3 → 4 | 1.4% | Partially → substantively-aligned |
| No upward crossing | 38.2% | Delta stayed inside a single anchor band |
| Downward crossing | 6.8% | Specification hurt the response |

One of every three low-baseline responses moves from "cannot engage" to actual engagement. Another one in five makes a larger jump. Only one response in fifteen gets worse.

---

**Three representative examples below show the different ways the specification can help.** These are not cherry-picked to impress; they are selected to show three distinct mechanisms the 6-provider collective review (`docs/reviews/s114_example_analysis_20260421_170720.md`) identified across the data. Hedge reduction is common but not the only thing going on. The specification also corrects wrong predictions in the opposite direction, and it enables interpretive inference from character patterns when retrieved facts are insufficient.

> ### Example A. Baseline to Facts + Spec: identity disambiguation + interpretive inference
>
> **Subject:** Georg Ebers. **Battery question (Q7):** *"How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?"*
>
> **Ground truth (held-out, what Ebers actually wrote):** *"A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed."*
>
> **Baseline response (C5, no context, 5-judge mean 1.20):**
>
> > *"I don't have specific information about Ebers's characterization of this relationship in my training data. To give you an accurate answer, I would need to know: 1. Which Ebers you're referring to — there are several notable figures with this surname in educational contexts..."*
>
> **With specification + facts (C4a, 5-judge mean 3.60):**
>
> > *"Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable — not instrumental, but constitutive. Self-sacrifice is not a means to institutional success; it is the evidence that success is genuine. Ebers witnessed this directly at Keilhau..."*
>
> **What the specification did.** The baseline failed to identify which Ebers was being asked about and refused to predict. The specification resolved the identity question and enabled a substantive interpretive claim ("constitutive, not instrumental") that the ground truth passage confirms. The collective review panel identified this as a mix of identity disambiguation and interpretive inference from character.

> ### Example B. Facts to Facts + Spec: directional correction
>
> **Subject:** Bernal Diaz del Castillo. **Battery question (Q16):** *"When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?"*
>
> **Ground truth:** *"There were 114 steps to the summit, and, as they feared that Cortes would experience the same fatigue in mounting as Motecusuma had, they were going to assist him by taking hold of his arms. Cortes, however, refused."*
>
> **With facts alone (C4, 5-judge mean 2.00):**
>
> > *"Based on the facts provided about Bernal Diaz del Castillo and his observations of Cortes, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example."*
>
> **With facts + specification (C4a, 5-judge mean 4.80):**
>
> > *"Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect Cortes to refuse the assistance and perform the labor himself, particularly if it serves a symbolic or morale-signaling purpose."*
>
> **What the specification did.** Facts alone produced a confident but directionally wrong prediction (commander accepts help). The specification corrected the prediction to match the ground truth (Cortes refuses). The collective review panel unanimously called this mechanism directional correction of a prediction: the specification encoded Cortes's pattern of physical self-reliance and performative leadership, overriding the model's generic "good leaders accept help" default.

> ### Example C. Facts to Facts + Spec: abstention becomes near-perfect inference
>
> **Subject:** Mary Seacole. **Battery question (Q2):** *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"*
>
> **Ground truth:** *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*
>
> **With facts alone (C4, 5-judge mean 2.80).** Effectively a non-answer:
>
> > *"Based on the complete set of facts provided, there is **no specific information** about how Mary Seacole typically responds when a delirious patient mistakes her for a family member. While the facts document many aspects of Mary Seacole's nursing care and compassion... there is no explicit account of her reactions to delirious patients confusing her identity with their relatives. To answer this question accurately, one would need additional source material..."*
>
> The model correctly identifies what the facts do not contain, lists adjacent facts about her nursing practice, and declines to predict. This is a clean abstention, not a wrong prediction. The 2.80 score reflects judge leniency on honest abstention responses: judges give partial credit for "right domain, declines to predict specifics" even when no prediction was actually made. Read the behavior, not the number: this is a refusal.
>
> **With facts + specification (C4a, 5-judge mean 5.00).** Near-perfect inference:
>
> > *"Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern. Primary response: compassionate acceptance. She would not correct the patient in the moment. Instead, she would lean into the mistaken identity, sustain the fiction with tenderness, and prioritize emotional relief over factual accuracy. This aligns with A4 (Proximate Obligation) and A8 (Sympathetic Realism)..."*
>
> **What the specification did.** The shift is from refusal-to-predict to a specific, accurate behavioral prediction that closely tracks Seacole's verbatim held-out account ("I could not undeceive him... the fancy happily caused by the touch of a woman's hand soothed his dying hour"). The specification enabled the model to generalize from Seacole's established compassionate-caregiving pattern (documented in the facts but not explicitly mapped to this scenario) to the specific untested situation. The collective review panel unanimously identified this as interpretive inference beyond retrieved facts: a mechanism that retrieval alone cannot produce because it requires applying character-level pattern to novel situations.
>
> **A note on rubric handling of abstention.** The judge panel scored this abstention at 2.80, not at 1.00 (the rubric anchor for "refuses or off-base"). This reflects a rubric-level issue we encountered in both directions across the study: judges treat honest abstentions as partial engagement (scoring ~2.5-3.0) rather than as refusals, and they sometimes penalize spec-induced honest abstentions where the specification appropriately declined to invent detail (§1.3's Keckley Q21 example). The rubric does not cleanly distinguish abstention from wrong prediction, which softens the apparent magnitude of some effects in either direction. A differentiated rubric that scores abstention as its own dimension is flagged as follow-up in §8.

---

**The improvement is not uniform across subjects. It depends on how much the AI already knows about the person.** Plain version: the less the model's pretraining has to work from, the more the specification can add. The more the model already knows, the less room the specification has to help, and on the highest-baseline subjects it can mildly hurt.

Linear regression of the facts-plus-specification effect against baseline:

| Statistical test | Value |
|---|---|
| Regression slope (Δ_C4a vs. C5) | **−0.96** [95% CI −1.24, −0.67] |
| R² | **0.82** (82% of variance explained by baseline) |
| Slope p-value | **< 0.001** (p = 0.000009) |
| Correlation r | −0.90 |
| Wilcoxon signed-rank, C5 vs. C2a | W = 10, p = 0.005 |
| Wilcoxon signed-rank, C5 vs. C4a | W = 11, p = 0.007 |
| Subjects with positive Δ_C4a | 12 of 14 |
| Low-baseline subjects (n=9) positive | 9 of 9 |
| Low-baseline mean Δ_C4a | +0.89 |

Rank agreement across the 5-judge primary panel is high (pairwise Spearman ρ = 0.89 to 0.98, §3.7.4), so the directional claim rides on broad agreement across three providers rather than on any one judge's scoring.

**A note on baseline measurement.** The measured C5 baseline (mean 1.52 on the low-baseline slice) is slightly inflated by a length-driven rubric effect. A post-hoc validity audit (§3.7.6) found that longer no-context responses (which include more hedging, adjacent-fact recitation, and disambiguation language) score higher on average than short refusals, with length-score correlation r = 0.604 specifically within C5 responses. Spec-containing conditions show no such length correlation. The true no-context prediction accuracy is likely lower than 1.52, which makes the spec-effect gap slightly *larger* than the reported +0.89 mean lift. We report the measured number rather than a length-corrected one to keep the pre-locked analysis plan intact, and flag the direction of the bias here so readers can interpret the effect size accordingly.

> ### Example D. The gradient at the extremes
>
> **Low-baseline, largest improvement.** *Hamerton* (baseline 1.26, Δ_C4a +1.51). Philip Gilbert Hamerton is a 19th-century British essayist whose *Autobiography* sits well outside the LLM pretraining spotlight. Adding the specification moved his prediction score from near-refusal to substantive subject-specific engagement across most of the battery.
>
> **High-baseline, mild interference.** *Franklin* (baseline 3.77, Δ_C4a −0.13). Benjamin Franklin is among the most widely referenced autobiographers in American public-domain literature. The AI already has him well-modeled from pretraining. The specification does not add representational signal; the spec-alone condition drops 0.40 points, facts + spec drops 0.13. See §4.1.1.
>
> **Low-baseline, smallest improvement.** *Babur* (baseline 1.76, Δ_C4a +0.25). Babur is the 16th-century Central Asian ruler and founder of the Mughal Empire. His corpus is the largest in the study (422,772 words) and his autobiography is partially represented in LLM training data. The specification still improves the score, but the room to help is smaller.

---

**Per-subject results.**

The table is ordered by baseline within each band. In the color-rendered PDF of the paper, the low-baseline rows are tinted green (the population of relevance), the mid-baseline rows are tinted yellow, and Franklin is tinted gray as the high-baseline reference. Figure 4.1 presents the same data as a scatter plot with the regression line.

| Subject | Baseline (C5) | Spec only (C2a) | Facts + Spec (C4a) | Δ spec | Δ facts+spec | Anchor crossed |
|---|---:|---:|---:|---:|---:|:-:|
| **Low-baseline slice (C5 ≤ 2.0), population of relevance** | | | | | | |
| Ebers | 1.02 | 1.54 | 2.07 | +0.52 | +1.05 | ✓ |
| Sunity Devee | 1.03 | 2.27 | 2.41 | +1.24 | +1.38 | ✓ |
| Hamerton | 1.26 | 2.63 | 2.77 | +1.37 | +1.51 | ✓ |
| Fukuzawa | 1.67 | 2.35 | 2.78 | +0.68 | +1.11 | ✓ |
| Bernal Diaz | 1.70 | 2.27 | 2.48 | +0.57 | +0.78 | partial |
| Babur | 1.76 | 1.91 | 2.01 | +0.15 | +0.25 | - |
| Seacole | 1.77 | 2.48 | 2.59 | +0.71 | +0.82 | ✓ |
| Keckley | 1.84 | 2.43 | 2.44 | +0.58 | +0.59 | - |
| Yung Wing | 1.88 | 2.22 | 2.40 | +0.34 | +0.52 | - |
| **Mid-baseline slice (2.0 < C5 < 3.0)** | | | | | | |
| Zitkala-Sa | 2.34 | 2.03 | 2.02 | −0.31 | −0.32 | - |
| Cellini | 2.38 | 2.54 | 2.53 | +0.16 | +0.15 | - |
| Rousseau | 2.44 | 2.81 | 2.53 | +0.37 | +0.10 | - |
| Augustine | 2.58 | 2.48 | 2.70 | −0.11 | +0.11 | - |
| Equiano | 2.77 | 2.46 | 2.42 | −0.31 | −0.35 | - |
| **High-baseline reference (not part of the main gradient)** | | | | | | |
| Franklin (known-figure control) | 3.77 | 3.37 | 3.65 | −0.40 | −0.13 | - |

**What each band is telling us.**

- **Low-baseline (n = 9):** every subject improves. The slice is uniform. This is the population of relevance for real AI deployment.
- **Mid-baseline (n = 5):** 3 subjects improve, 2 decline. The model has enough pretraining footprint on these subjects that the specification competes with the model's own working model. The specification sometimes wins and sometimes loses.
- **Franklin (high-baseline reference):** both spec-containing conditions score below baseline. The specification cannot add what the model already has.

Per-subject anchor-crossing distributions (ranging from 25.6% on Babur to 74.4% on Sunity Devee) and per-subject per-judge score matrices are in Appendix D.

### 4.1.1 Franklin as the high-baseline reference

Franklin is not a subject of the main gradient. He is a known-figure control. Benjamin Franklin's *Autobiography* is one of the most widely cited autobiographical works in American public-domain literature, and every current-generation LLM has substantial pretraining representation of both the person and the specific text. Franklin's C5 baseline on the 5-judge primary panel is 3.77, well above the anchor-3 threshold ("right domain, wrong outcome") and nudging toward anchor 4 ("general direction correct"). On the 7-judge aggregate with Gemini included the baseline is higher still (see §4.5). This is well above the next-highest main-study subject (Equiano at 2.77, still below the anchor-3 band).

Both spec-containing conditions score below Franklin's baseline. The specification alone (C2a) drops 0.40 points; facts plus specification (C4a) drops 0.13. The drop is more pronounced on spec-alone than on facts-plus-spec because the specification alone competes with strong pretraining without the facts to re-anchor the response. Adding facts back partially restores the AI's own working model of Franklin.

This is the direction H2a predicts. Where the AI already has the person well-modeled from pretraining, the specification does not add representational signal and can mildly interfere. The gradient holds at both ends of the spectrum: a large positive effect where the baseline is low, a near-zero or mildly negative effect where the baseline is high.

Raw per-subject Franklin data is at `results/franklin_legacy_20260411/`.

### 4.1.2 Living-user replication (author)

The main gradient is built entirely on historical subjects with public-domain autobiographies. Every one sits above the pretraining baseline of a typical living person whose private reasoning is not in any training corpus. §1.4 made the extrapolation argument that such a person should sit at or below the rubric floor. We ran a methodology-matched replication on one living individual to test this directly.

**Setup.** The author's private conversation history with AI systems (ChatGPT and Claude, roughly four years) was loaded into the same pipeline used for the 14 historical subjects. The corpus was split 50/50 by message ID (seed 42), producing a training half and a held-out half. The full-stack Behavioral Specification (anchors + core + predictions + brief) was authored from the training half only, following §3.3. A 40-question behavioral-prediction battery was backward-designed from the held-out half only, following §3.4. No held-out passage was seen by the spec-generation pipeline. Claude Haiku 4.5 produced responses under five conditions (C5, C2a, C2c, C4, C4a). Five primary judges scored each response against the verbatim held-out passage.

**Results (5-judge primary, N = 40).**

| Condition | Mean score | Δ vs. C5 | Downward crossings |
|---|---:|---:|---:|
| C5 (baseline, no context) | **1.03** | - | - |
| C2a (correct spec only) | **2.86** | +1.84 | 0 |
| C2c_Franklin (wrong spec, shared-anchor draw) | **2.59** | +1.56 | 0 |
| C2c_max-distance (wrong spec: Babur's, maximally different profile) | **2.34** | +1.32 | 0 |
| C2c_random (wrong spec: Seacole's, seed=42 random draw) | **2.19** | +1.16 | 0 |
| C4 (all facts, no spec) | **2.93** | +1.90 | 0 |
| C4a (facts + correct spec) | **3.02** | +2.00 | 0 |

**Anchor crossings C5 → C4a:** 30 of 40 responses moved up at least one rubric integer anchor; 0 moved down; 10 stayed in the same band. Upward crossing rate **75.0%**. **No downward crossings were observed under any of the three wrong-spec draws either:** all 120 wrong-spec responses (40 × 3) either improved over baseline or tied.

**Wrong-spec controls partition cleanly into a consistent ordering.** Three wrong-spec draws were run to separate floor-mediated improvement from content-overlap improvement. The ordering is what the content-specificity hypothesis predicts:

> correct spec (+1.84) > shared-anchor wrong spec (Franklin, +1.56) > max-distance wrong spec (Babur, +1.32) > random wrong spec (Seacole, +1.16) > no context.

Each step down reflects one more piece of content specificity removed while keeping format constant. The *correct* specification carries all interpretive pattern. Franklin's spec shares roughly five of the author's twelve behavioral anchors (systematic self-grading against a named rubric, persistent tracked gap between stated rule and actual behavior, rationalist-empiricist disposition, compression-as-quality, and moral aspiration without claim of arrival); it retains partial content specificity. Babur's specification describes a 16th-century Central Asian ruler with no anchor overlap at the surface, yet the lift is still +1.32. Seacole's specification, drawn at random (seed=42 over the 14 main-study subjects), lifts by +1.16. A random wrong-spec at this baseline was originally estimated to produce only a small floor-mediated effect; the measured +1.16 is substantially larger than that estimate and indicates the floor-effect component was underestimated.

**What this means.** The earlier decomposition into a "+0.25 floor effect" plus "content-overlap improvement" is revised. Two separate readings can explain the large random-wrong-spec lift at this baseline: (a) a stronger floor effect than the historical low-baseline subjects exhibit, or (b) a battery-composition effect whereby questions backward-designed from the author's own held-out corpus reward any well-structured interpretive content, not only content matching the subject. Both readings preserve the core claim: the *correct* spec still outperforms every wrong spec tested, and the ordering is strictly monotone in anchor overlap. What changes is the magnitude of the floor-effect term, which is larger than the +0.25 estimate derived from the historical low-baseline slice. The H3 content-specificity claim still passes the test; the magnitude attribution is softer than previously reported. Full derangement data at `docs/research/p0_6_author_derangement.md`.

**Reading the numbers against the main gradient.**

The baseline 1.03 sits at the rubric floor, below every one of the 14 historical subjects. This is the empirical confirmation of §1.4's claim that a person whose private reasoning is not in any training corpus should register at or below the floor: the AI has essentially no model of this specific person from pretraining alone. The +2.00 improvement under facts-plus-spec is the largest in the study (historical maximum was Hamerton at +1.51). The 75% anchor-crossing rate exceeds the 55% on the historical low-baseline slice. **Across all three wrong-spec draws and the correct spec, none of the 120 responses got worse relative to the no-context baseline.** This is stronger than any single-draw test: the directional claim holds whether the wrong spec shares anchors with the subject (Franklin), is maximally distant (Babur), or is drawn at random (Seacole).

The gradient prediction reads through: the population the model knows the least about is the population where the specification has the largest effect. The pilot is a single living subject and cannot substitute for a multi-subject replication. That multi-subject replication is the leading follow-up in §8.

Raw data stays in a private working directory at `_internal/aarik_clean_pilot/` (original conditions) and `_internal/aarik_clean_pilot_p0_6/` (derangement reruns) and is not included in the public repository. Summary statistics, battery checksums, derangement seeds and picks, and the leakage audit are reproducible from the manifests referenced in §8 Future Work and `docs/research/p0_6_author_derangement.md`.

---

### 4.2 Compression: Structure vs. Raw Text

**Hypothesis tested in this section** (H5 from §1.2): A compact specification achieves comparable behavioral-prediction performance to the full raw source corpus, at a fraction of the context size.

---

**Context improves prediction.** On the 9 low-baseline subjects, every context condition increases the per-subject mean score by roughly one full rubric point over the no-context baseline (mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50). The AI does not need much context to move from refusal-and-off-base to engaged subject-specific prediction. It needs *some* context.

**The compact specification captures the large majority of that improvement.** A 7,000-token Behavioral Specification recovers most of what the full raw corpus delivers, despite being an order of magnitude or more smaller. Across the 9 low-baseline subjects, the raw corpus (C8) averages 0.22 points higher than spec alone (C2a). The corpus's edge is real but small relative to the context-size gap that produces it.

**The efficiency claim in one metric: predictive gain per 1,000 tokens of context.** The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. The dose-response curve has a steep initial slope and a long plateau. The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document.

---

**Per-subject compression comparison (5-judge primary, low-baseline slice).**

The table shows baseline and every compression-related condition for each subject, with the compression ratio (source corpus tokens ÷ specification tokens, both approximate) for scale. In the color-rendered PDF, low-baseline rows are tinted to mark the population of relevance; the C8 − C2a gap column is shaded to make the spec-vs-corpus difference visible at a glance.

| Subject | Source words (~tokens) | Compression ratio (corpus / spec) | C5 baseline | C2a spec (~7K tok) | C4 facts (~10K tok) | C8 raw corpus | C4a facts+spec | C9 corpus+spec | C8 − C2a |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hamerton | 25,231 (~33K) | ~5× | 1.26 | **2.63** | 2.43 | 2.27 | 2.77 | **3.09** | **−0.36** |
| Sunity Devee | 67,379 (~88K) | ~13× | 1.03 | 2.27 | 2.46 | 2.55 | 2.41 | 2.46 | +0.28 |
| Ebers | 96,174 (~125K) | ~18× | 1.02 | 1.54 | 2.02 | 2.18 | 2.07 | 2.16 | +0.64 |
| Fukuzawa | 139,088 (~181K) | ~26× | 1.67 | 2.35 | 2.67 | 2.74 | 2.78 | 2.78 | +0.39 |
| Bernal Diaz | 187,315 (~244K) | ~35× | 1.70 | 2.27 | 2.41 | 2.55 | 2.48 | 2.53 | +0.28 |
| Babur | 422,772 (~549K) | ~78× | 1.76 | 1.91 | 2.03 | 2.05 | 2.01 | - | +0.14 |
| Seacole | 62,467 (~81K) | ~12× | 1.77 | 2.48 | 2.63 | 2.83 | 2.59 | 2.73 | +0.35 |
| Keckley | 58,742 (~76K) | ~11× | 1.84 | 2.43 | 2.39 | 2.50 | 2.44 | 2.49 | +0.07 |
| Yung Wing | 66,459 (~86K) | ~12× | 1.88 | 2.22 | 2.13 | 2.42 | 2.40 | 2.50 | +0.20 |
| **Mean** | | **~23×** | **1.52** | **2.23** | **2.35** | **2.45** | **2.45** | **2.50** | **+0.22** |

Babur's C9 condition was excluded because the 422,772-word corpus plus the specification exceeded the response model's context window.

**What the aggregate numbers say.**

- Every context condition lifts the low-baseline mean by at least one full rubric point over the no-context baseline.
- The specification alone recovers roughly three-quarters of the corpus-alone lift (spec lift +0.71, corpus lift +0.93) at an order of magnitude to two orders of magnitude smaller context depending on subject.
- Adding facts to the specification (C4a) produces the same mean as raw corpus alone (both 2.45). Two different compression strategies, same performance, different context shapes.
- Adding the specification on top of the full raw corpus (C9) adds ~0.05 points on average over raw corpus alone. The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

### 4.2.1 Question-Improvement Rate: A Candidate Secondary Reporting Metric

The aggregate mean score is a useful summary, but it blends judge variability with response quality. A cleaner unit: **out of N individual questions, how many does each condition improve over the no-context baseline?** This is a **win rate against a no-context baseline**, structurally parallel to the per-prompt win-rate convention used in LLM evaluation (Chatbot Arena, LMSYS pairwise preference rates). Each question either improves, ties, or worsens when the condition's context is added; the unit is judge-noise-resistant in aggregate and directly interpretable without requiring a matched rubric across studies.

**The reporting triplet.** Win rate alone hides the magnitude of help and harm. We report three numbers together for each condition: the improvement rate, the worsening rate, and the median magnitude of improvement among improved questions (with the median worsening magnitude as a sanity check).

**Low-baseline slice (9 subjects, 351 questions, 5-judge primary per-question means).**

| Condition vs. C5 baseline | Improved | Tied | Worse | Improvement rate | Median Δ when improved | Median Δ when worsened |
|---|---:|---:|---:|---:|---:|---:|
| **C2a spec only** | 249 | 49 | 53 | **70.9%** | **+1.00** | −0.40 |
| C4 facts only | 256 | 44 | 51 | 72.9% | +1.00 | −0.40 |
| C8 raw corpus | 275 | 31 | 45 | 78.3% | +1.00 | −0.60 |
| C4a facts + spec | 276 | 22 | 53 | 78.6% | +1.00 | −0.40 |

**The magnitude column is the important row of this table.** When the specification helps, the typical help is a full rubric category (+1.00 median). When it hurts, the typical hurt is less than half a category (−0.40 median). The metric is not capturing trivial +0.02-per-question gains; the underlying improvements are substantive.

**All 14 subjects (546 questions).**

| Condition vs. C5 baseline | Improvement rate | Worsening rate |
|---|---:|---:|
| C2a spec only | 58.8% | 26.7% |
| C4 facts only | 60.1% | 26.6% |
| C8 raw corpus | 64.5% | 24.5% |
| C4a facts + spec | 65.8% | 26.4% |

On the 9 low-baseline subjects, **7 out of every 10 questions improve with the specification alone**, roughly 1 in 10 tie, and fewer than 1 in 6 worsen. Every context condition exceeds a 70% per-question improvement rate on the population of relevance. The specification's rate sits within 8 percentage points of the raw corpus's (70.9% vs. 78.3%) at an order of magnitude less context.

![Figure 4.2.1. Per-question outcome distribution by condition (low-baseline slice, n = 9 subjects, 351 questions, 5-judge primary). Stacked bars show the share of questions that improved, tied, or worsened relative to the no-context C5 baseline. The specification alone (C2a) improves 70.9% of questions at roughly an order of magnitude less context than the raw corpus (C8, 78.3%). Facts + spec (C4a) matches the raw corpus's improvement rate while cutting the tie band in half. Median Δ when improved = +1.00 rubric points; median Δ when worsened = −0.40 points.](../figures/fig_4_2_1_question_improvement_rates.png)

**Pairwise comparison at question level (low-baseline slice).**

| Comparison | Higher-cost condition higher | Tie | Lower-cost condition higher |
|---|---:|---:|---:|
| Raw corpus (C8) vs. spec alone (C2a) | 190 (54.1%) | 46 | 115 (32.8%) |
| Corpus + spec (C9) vs. facts + spec (C4a) | 155 (49.7%) | 42 | 115 (36.9%) |

The raw corpus outscores the spec alone on more questions than it loses, but the spec outscores the corpus on roughly one-third of them. On the combined conditions, the 7K-token facts + spec package outscores the much larger corpus + spec package on 36.9% of questions.

**Positioning as a secondary reporting metric.** A per-question win rate against a no-context baseline makes behavioral prediction directly comparable across future studies in a way that mean scores do not. "Our representation improves 65% of questions over the no-context baseline, with median improvement magnitude +0.8 points" is interpretable on its own and can be compared to this study's 70.9% / +1.00 without matched judges or rubrics. We propose this metric as a **candidate secondary reporting axis** for future AI-personalization work, always paired with mean-score information, never replacing it. The proposal is developed further in §8 Future Work.

**Failure modes if this metric is adopted.** The panel-reviewed limitations worth flagging explicitly for any future use:

- **Tiny-gain inflation.** A method producing +0.02-point gains on 80% of questions would register as a 80% improvement rate. The magnitude triplet (median Δ when improved) is the guard: if median improvement magnitude is near zero, the rate is misleading. Our low-baseline specification has median Δ = +1.00, so this failure mode does not apply to the reported numbers; it is a known trap for anyone adopting the metric.
- **Hidden catastrophic harm.** A method that improves 85% and catastrophically harms 15% would look strong. The worsening-magnitude column is the guard: median worsening of −0.40 on spec-alone indicates the hurt is bounded.
- **Easy-baseline gaming.** Improvement rates can be inflated by choosing weak baseline prompts or subjects the model has unusually thin pretraining coverage of. The guard is reporting the no-context baseline mean alongside the improvement rate; our C5 = 1.52 mean on the low-baseline slice makes the baseline difficulty explicit.
- **Scale-free illusion of portability.** "Improved" is binary, so a 1% gain and a 50% gain count equally. The metric is only comparable across studies when the reporting triplet is disclosed and the baseline is defined identically.

The same win-rate framing is referenced in §1.2 (as a secondary outcome alongside the mean-score gradient) and in §4.1 (alongside the 55.0% anchor-crossing rate, which is the same unit at a stricter threshold: "does the response move to a different rubric category?" rather than "does the response improve at all?").

---

> ### Example: Hamerton, the compression story at its clearest
>
> Hamerton has the smallest source corpus in the study (25,231 words, compression ratio ~5×). The specification alone (~7K tokens) scores 2.63, exceeding the full raw corpus at 2.27. Facts-plus-spec reaches 2.77. Corpus-plus-spec reaches 3.09, the highest compression-related score observed in the study. This is the case where structured context substantially outperforms raw text, and where the spec and corpus are clearly complementary rather than overlapping.
>
> The pattern is interpretable: when the source corpus is short enough to be sparse on its own, structured extraction adds organizational value beyond mere content. Hamerton is the boundary condition for the compression claim, not the proof of it.

> ### Example: Ebers, the honest cost of compression
>
> Ebers has a larger source corpus (96,174 words) and the study's lowest baseline (1.02). Every context condition lifts his score above baseline. But the specification alone (1.54) underperforms the raw corpus (2.18) by 0.64 points, the widest spec-vs-corpus gap in the low-baseline slice. Facts alone (2.02) fall between them.
>
> Ebers is where the cost of compression is most visible. The raw corpus contains something the 7K-token spec does not capture, and that something is worth 0.64 points on the rubric. The honest reading is not "compression fails"; it is "compression captures the bulk of the signal but not all of it, and on some subjects the residual matters more than on others." The trade-off is still favorable: the spec delivers +0.52 points of lift at roughly 6% of the corpus's token cost; the corpus delivers +1.16 points at 18× the context. Per 1,000 tokens of context served, the spec is substantially more efficient.

---

**Why this matters for deployment.**

At any scale where a per-user full autobiography cannot be served into context on every query (which is to say, at any real-world scale beyond a toy demo), the compression result is what makes personalization operationally tractable. The specification's 7K-token footprint is within normal per-request context budgets. A 100,000-to-400,000-word corpus is not. The specification achieves most of the predictive benefit at a tractable cost; the corpus achieves marginally more at a cost that rules out deployment.

Raw per-subject data is at `results/global_<subject>/c8_c9_results.json` and `results/global_<subject>/results_v2.json`. The compression analysis and question-improvement rate computation are in `scripts/recompute_5judge_primary.py` and `scripts/compute_question_improvement_rate.py`. Figure 4.2 plots score versus context size (log scale) per subject and shows the dose-response curve with its steep initial slope and long plateau.

---

### 4.3 Mechanism: Content, Not Format

**Hypothesis tested in this section** (H3 from §1.2): The benefit comes from the content of the correct specification for the correct person, not from the mere presence of a structured prompt. A random other person's specification, applied in its place, does not reproduce the effect.

---

**If structure alone were driving the effect, a mismatched specification would produce roughly the same improvement as a matched one. The data rejects this directly.**

On the 13 global subjects with complete 5-judge primary coverage, three conditions test whether content matters:

| Condition | Mean Δ vs. C5 (5-judge primary, 13 globals) | Reading |
|---|---:|---|
| C2a (correct spec) | **+0.35** | matched content improves prediction |
| C2c v2 (random derangement, seed-fixed) | **+0.22** | partial improvement; dominated by floor effects on low-baseline subjects |
| C2c v1 (fixed derangement, cultural/temporal distance maximized) | **−0.25** | adversarial mismatch degrades prediction below the no-context baseline |

The two wrong-spec variants differ by construction. **v1 (fixed derangement)** is a hardcoded pairing in `scripts/run_global_rerun.py` designed so each subject receives the specification of a culturally- and temporally-distant other (for example, Ebers the 19th-century German Egyptologist receives Equiano the 18th-century West-African/British autobiographer; Seacole the 19th-century Jamaican nurse receives Bernal Diaz the 16th-century Spanish conquistador). **v2 (random derangement)** is a seed-fixed random permutation in which no subject receives its own specification but pairings can land culturally-close; this tempers the aggregate drop. Reporting both shows that even a random wrong-spec barely beats no context, and an adversarial wrong-spec actively hurts.

The gap between the correct-spec (C2a) condition at +0.35 and the fixed-derangement (C2c v1) condition at −0.25 is **0.60 points on the 1-5 rubric**, more than half a full rubric-anchor category. That gap is the content effect, measured at the population mean; per-question swings are larger in both directions (Example B below has a −0.20 coincidental-overlap case where the wrong spec nearly matches the correct spec; Example C below has a −3.60 clean mismatch case).

---

**Three mechanism types.**

Three distinct mechanisms produce the correct-specification improvement across the study data. Each has a characteristic wrong-specification failure mode, illustrated in the matched examples below.

1. **Identity disambiguation.** When the baseline model cannot determine which person is being asked about, the specification provides enough content (temporal markers, cultural domain, documented life events) to resolve the identity and anchor the reasoning frame. *Wrong-spec failure mode:* the model either detects the mismatch explicitly and refuses to predict, or anchors on the wrong person's pattern and produces a coherent but off-target prediction.
2. **Directional correction.** When retrieved facts suggest a generic-default prediction that contradicts the subject's actual pattern, the specification overrides the generic with the subject-specific. *Wrong-spec failure mode:* the model applies the wrong person's pattern; depending on how close that pattern happens to be to the target subject's, the prediction is either directionally wrong in a new way or coincidentally correct.
3. **Interpretive inference.** When retrieved facts do not include direct evidence for the specific question, the specification provides interpretive scaffolding to generalize from established character patterns to the novel situation. *Wrong-spec failure mode:* the model detects the mismatch and refuses, or applies wrong-person scaffolding and produces a low-quality prediction.

---

**Spec-activation evidence.**

Tag-citation analysis on response text (data at `docs/research/spec_activation_analysis.json`) shows the content-activation gap. On correct-spec conditions, **78.6%** of responses explicitly cite at least one spec tag (anchor ID, axiom reference, predictive-template label). On wrong-spec conditions, only **50.0%** do. The 28.6-point gap is a lower bound on the content effect: models may draw on spec content without literally quoting tag IDs, so the true divergence is wider. The baseline reading is that models recognize when the specification fits the question and engage with it; they recognize when it doesn't fit and disengage or improvise.

---

**Response-level evidence: wrong-spec detection.**

Across 587 wrong-spec responses classified (validated against a 30-response stratified manual spot check), the response distribution is bimodal:

- **60.6%** explicitly flagged the content mismatch (example, from one Keckley wrong-spec response: *"This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"*)
- **36.5%** attempted to apply the mismatched content and produced a low-quality prediction
- **2.0%** hedged implicitly
- **0.9%** were ambiguous

The detection asymmetry in this experiment: battery questions name the target subject (e.g., "How would Ebers characterize...") but specifications are anonymized (§3.3), so "detecting the mismatch" means the model is comparing the named target in the question to the interpretive content of the anonymized specification, and concluding the specification does not describe the named target. The signal that carries the detection is interpretive content (temporal markers, cultural domain, documented life events) being inconsistent with what the model knows about the named subject, not surface name cues. The 60.6% is a lower bound on that comparison because a more capable response model, or a derangement with less interpretive distance between target and substitute, could push the rate in either direction.

---

**Hedging evidence (from §1.3) carries the same implication.**

Under both classifier rules, spec-containing conditions eliminate baseline hedging: narrow-rule 28.8% → 1.4% → 0.0%, broader-rule 41.2% → 7.9% → 0.4%. Order-of-magnitude drops. If mere structured context were producing the effect, wrong-spec should also eliminate hedging at a similar rate. Instead, the 60.6% explicit-detection rate on wrong-spec responses means refusal patterns persist when the content does not fit the subject. The hedging-reduction is spec-content-specific, not structure-specific.

---

**Per-question matched comparison.**

The three §4.1 examples extend directly into mechanism-by-mechanism wrong-spec contrasts. Same subject, same question, same response model; the only change is the specification content. Correct-spec C4a responses are in §4.1 for reference.

> ### Example A (wrong-spec), Ebers Q7: identity disambiguation fails
>
> **Subject + question:** same as §4.1 Example A (Ebers, self-sacrifice and educational institutional success). Battery-question target name: Ebers (explicit in the prompt).
> **Wrong spec served:** Equiano's specification, served anonymized per `run_global_rerun.py` fixed pairing. The response cites two of Equiano's anchors; the anchor definitions from Equiano's specification are:
>
> > **A4 — SYSTEMIC INDICTMENT:** *"avarice — institutionalized greed — is the generative engine of the greatest human cruelties, and that individual kindness within a corrupt system neither redeems the system nor excuses participation in it."*
> >
> > **A9 — ECONOMIC SELF-DETERMINATION:** *"the capacity to earn, trade, and accumulate independently is not merely practical but constitutive of dignity and agency — economic self-determination is the material form that freedom takes."*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 1.60, drop −2.00 vs. the correct-spec C4a condition's 3.60):**
>
> > *"I need to be direct: I don't have reliable access to specific statements by Ebers on this question. The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. ... Given A4 (Systemic Indictment) — that institutionalized greed is the generative engine of cruelty ... a teacher sacrificing their own economic security, health, or family time does not fix a system structured by avarice."*
>
> **Reading.** The model detected the mismatch between the named target in the question (Ebers, a 19th-century German Egyptologist) and the interpretive content of the anonymized specification (anti-slavery and economic-freedom anchors, which are Equiano's). It named the served anchors correctly, reasoned from Equiano's framework, and declined to produce a prediction about Ebers. The identity-disambiguation mechanism that enabled the correct spec's lift in §4.1 Example A did not fire because the spec content is not about Ebers. The response falls near the rubric floor because no prediction was made.

> ### Example B (wrong-spec), Bernal Diaz Q16: content convergence across genuinely different frameworks
>
> **Subject + question:** same as §4.1 Example B (Bernal Diaz, Cortes and offered physical assistance). Battery-question target name: Bernal Diaz.
> **Wrong spec served:** Sunity Devee's specification (fixed pairing). The response cites three of Sunity Devee's anchors; the anchor definitions from her specification are:
>
> > **A5 — RELATIONAL IDENTITY:** *"identity, worth, and moral standing are constituted through their relationships — to family, spouse, ruler, and God — rather than through individual achievement or autonomous selfhood."*
> >
> > **A9 — SIMPLICITY AS VIRTUE:** *"Simplicity in dress, material goods, personal manner, and child-rearing is a positive moral value — a marker of spiritual seriousness. Elaborateness, display, and material accumulation are read as mild moral signals in the wrong direction."*
> >
> > **P5 — VIRTUE THROUGH EMBODIED PRACTICE:** *"credibility is demonstrated through concrete daily disciplines (bathing, prayer, ritual purity, hospitality, domestic skill) rather than through abstract declaration. Habit is the principle."*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 4.60, drop only −0.20 vs. the correct-spec C4a condition's 4.80):**
>
> > *"Based on this behavioral specification, the author would likely decline the offered assistance ... Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) ... Physical exertion endured without assistance becomes evidence of character."*
>
> **Reading, not parroting.** The two specs are genuinely different frameworks. Bernal Diaz's actual anchors include A1 Divine Mandate, A2 Civilizational Hierarchy, A4 Loyalty Architecture, A5 Forward Compulsion, A6 Gold as Proof, and A10 Charismatic Override: a conquistador's martial-providential register. Sunity Devee's anchors cited here (A5 Relational Identity, A9 Simplicity as Virtue, P5 Virtue through Embodied Practice) are an ascetic-devotional register. Direct anchor-to-anchor comparison across the two specs finds zero substantive mirroring. On the specific question of refusing offered physical help, the two frameworks converge by different logics: the correct spec (Bernal Diaz) predicts refusal because accepting help would signal weakness to followers and violate performative self-reliance (A4 + A5 in the conquistador register); the wrong spec (Sunity Devee) predicts refusal because accepting help would compromise physical discipline and violate simplicity-as-virtue (A9 + P5 in the devotional register). Different moral architectures, same overt behavior.
>
> **Why the correct spec still outperformed, 4.80 vs. 4.60.** Both conditions predicted the right surface action. The 0.20-point gap is judge preference for rationale specificity that matches the ground-truth passage's tone. The correct spec's "symbolic or morale-signaling purpose" rationale maps onto a battlefield memoir's register; the wrong spec's "spiritual seriousness, devotional simplicity" rationale predicts the same action but in a register alien to Cortes on the steps of the Templo Mayor. Judges reward tonally-aligned rationale. The convergence is real but costs precision.
>
> **Why this matters for the aggregate numbers.** This is the coincidence case that lifts the wrong-spec aggregate above zero. When the fixed derangement (v1) happens to pair subjects whose behavioral patterns converge on the same surface prediction for a given question, wrong-spec lift is real on that question, not an artifact. Over 507 responses, mismatch-loss dominates on the adversarial v1 pairing (aggregate Δ −0.25) and roughly balances on the random v2 pairing (aggregate Δ +0.22). Example B is one of the roughly 5-10% of questions where content coincidence produces correct-surface, wrong-logic predictions.

> ### Example C (wrong-spec), Seacole Q2: interpretive inference fails
>
> **Subject + question:** same as §4.1 Example C (Seacole, delirious patient). Battery-question target name: Mary Seacole.
> **Wrong spec served:** Bernal Diaz's specification (fixed pairing, anonymized). The response identifies the wrong spec by its interpretive content alone. Bernal Diaz's actual anchors that the model names in the response are:
>
> > **A1 — DIVINE MANDATE:** *every outcome is providentially ordained; reasoning is teleological.*
> >
> > **A2 — CIVILIZATIONAL HIERARCHY:** *Spanish Christian civilization as axiomatic superior lens on encountered peoples.*
> >
> > **A4 — LOYALTY ARCHITECTURE:** *personal loyalty is load-bearing, more binding than formal rank.*
> >
> > **A5 — FORWARD COMPULSION:** *retreat is moral failure; momentum is irreversible once committed.*
>
> **Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 1.40, drop −3.60 vs. the correct-spec C4a condition's 5.00):**
>
> > *"The specification you've provided describes someone from the 16th-century Spanish conquest period — the epistemic anchors, loyalty architecture, divine mandate framing, and forward compulsion all point to that historical context. Mary Seacole (1805-1881) was a Creole nurse and travel writer from Jamaica who served in the Crimean War. These are entirely different people from different centuries with different frameworks. ... I don't have documented instances of this. I could speculate based on her memoir's tone and her known character, but that would be inference, not behavioral specification."*
>
> **Reading.** The model detected the mismatch between the named target in the question (Mary Seacole, a 19th-century Jamaican Creole nurse) and the anonymized content of the served specification (16th-century Spanish conquest anchors). It named the anchors it was seeing, placed Seacole in a different era and role, and refused to apply the mismatched content. The interpretive-inference mechanism that produced §4.1 Example C's correct-spec 5.00 score does not fire: without Seacole's actual character pattern in context, the model would not generalize from an unrelated conquistador's framework to her delirious-patient scenario.

---

**Summary of the three examples.**

| Example | Mechanism (correct spec) | C4a (correct) | C2c v1 (wrong) | Drop | Wrong-spec pattern |
|---|---|---:|---:|---:|---|
| A (Ebers Q7) | Identity disambiguation + interpretive inference | 3.60 | 1.60 | **−2.00** | Explicit mismatch flag; declined prediction |
| B (Bernal Diaz Q16) | Directional correction | 4.80 | 4.60 | **−0.20** | Coincidental content overlap; wrong-spec prediction matches |
| C (Seacole Q2) | Interpretive inference | 5.00 | 1.40 | **−3.60** | Explicit mismatch flag; declined prediction |

Two of three examples show large drops (−2.00 to −3.60 points) when the content does not fit. The third shows near-zero drop, but only because the wrong spec's content happens to predict the same surface behavior. That asymmetry, clean mismatches versus coincidental overlaps, is exactly what the aggregate Δ numbers reflect: the adversarial-pairing v1 aggregates to −0.25 because most questions are mismatch cases, and the random-pairing v2 aggregates to +0.22 because random pairings more often hit content-proximity combinations like Example B.

Raw per-judge data and full response text are at `results/global_<subject>/results_v2.json` (wrong-spec responses) and `results/global_<subject>/judgments_v2.json` (per-judge scores). The analysis scripts are `scripts/compute_wrong_spec_5judge.py` and `scripts/compute_wrong_spec_per_subject.py`.

---

### 4.4 Memory-System Composition

**Hypothesis tested in this section** (H4 from §1.2): The specification is composable with existing memory-system retrieval pipelines, not a replacement for them. When added to commercial memory systems, it improves their behavioral prediction additively.

---

**Plain version.** **When the Behavioral Specification is added on top of a commercial memory system's retrieval, the combined context produces better behavioral prediction than retrieval alone on people the model doesn't already know. The effect holds on three of the four commercial systems we tested.**

**Setup.** We tested four commercial memory systems (Mem0, Letta, Supermemory, Zep) and Base Layer's own zero-cost retrieval substrate (MiniLM-L6-v2 + ChromaDB), each evaluated under two configurations. Full details in §3.3 and §3.5; summary:

- **Controlled configuration.** Each system is given an identical pre-extracted fact pool drawn from the training half of each subject's corpus. The input is held constant across all four commercial systems and the Base Layer substrate, so any difference in the downstream prediction score is attributable to the system's retrieval and presentation policy alone, not to what it was able to ingest.
- **Native configuration.** Each system ingests the raw training corpus through its own production pipeline, as in deployment. Measures the full end-to-end system.

Within each system in each configuration, two conditions are compared:
- **C1** (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.
- **C3** (retrieval + spec): the same retrieval plus the full Behavioral Specification.

The spec-effect for that system is the **Δ_spec = mean(C3) − mean(C1) aggregated per subject, then averaged across subjects.** If H4 holds, Δ_spec is positive across systems.

---

**Aggregate results, controlled configuration (5-judge primary, N = 14 subjects).**

| System | Δ_spec (all 14) | Subj + / 14 | Δ_spec (low-baseline 9) | Subj + / 9 |
|---|---:|---:|---:|---:|
| Mem0 | +0.12 | 10/14 | +0.10 | 6/9 |
| Letta (archival retrieval path) | +0.20 | 12/14 | +0.17 | 8/9 |
| Zep | +0.19 | 13/14 | +0.17 | **9/9** |
| Supermemory | −0.05 | 5/14 | −0.01 | 5/9 |
| Base Layer substrate | +0.08 | 9/14 | +0.08 | 6/9 |

Wilcoxon signed-rank on C1 vs C3 within each system: **Zep controlled p = 0.0004, Letta controlled p = 0.0017** (both robust at α = 0.01). Mem0, Supermemory, and Base Layer substrate controlled are not significant at α = 0.05.

**Aggregate results, native configuration (5-judge primary).**

| System | Δ_spec (full) | Subj + / n | Δ_spec (low-baseline) | Subj + / n |
|---|---:|---:|---:|---:|
| Mem0 | +0.33 | 10/14 | +0.32 | 7/9 |
| Letta (archival retrieval path) | −0.02 | 5/14 | −0.04 | 4/9 |
| Zep | +0.33 | 13/14 | +0.30 | **9/9** |
| Supermemory* | −0.07 | 3/10 | −0.03 | 3/7 |
| Base Layer | - | N/A | - | N/A |

\* Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau), so the native n drops to 10 full / 7 low-baseline. Base Layer has no separate "native" condition because Base Layer's authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant.

---

**Three of four commercial memory systems benefit from the specification.** Mem0, Letta (archival path), and Zep all produce positive Δ_spec in the controlled configuration, and two of the three (Mem0, Zep) produce larger positive Δ_spec in the native configuration. Supermemory is the fourth system and aggregates slightly negative; what the near-zero aggregate actually means per-question is developed in the dedicated Supermemory section below.

**Zep is the cleanest positive case.** 9 of 9 low-baseline subjects positive in both controlled (+0.17) and native (+0.30) configurations, Wilcoxon p < 0.002 in both. Zep's temporal-graph retrieval and the Behavioral Specification layer without interference.

**Mem0 native produces the largest single-system spec-effect (+0.33).** Mem0's own ingestion pipeline, running natively, retrieves content that the specification layers on top of with the study's largest native Δ_spec.

**Letta's split behavior is architectural.** The archival-retrieval path tested here shows positive Δ_spec in controlled (+0.20) and near-null in native (−0.02). Letta's stateful-agent path, which is a different architecture tested on a different set of conditions, is described separately in §4.4.1 and §4.7.

**Base Layer's retrieval substrate is not a memory product, and it runs locally.** MiniLM-L6-v2 + ChromaDB is a zero-cost open-source retrieval floor. It runs entirely on the local machine: the embedding model is local inference and the vector store is local ChromaDB, so no data leaves the environment during retrieval or fact identification. The four commercial memory providers tested in this study (Mem0, Letta, Supermemory, Zep) all require cloud API calls for vector search and fact-identification operations. Base Layer's Δ_spec (+0.08 controlled) is the smallest positive among systems reporting positive numbers, which reflects that Base Layer's retrieval is intentionally bare; the interpretive improvement comes from the specification itself, not from Base Layer's retrieval choices. The local-execution property is a deployment-mode distinction, not a prediction-quality distinction.

---

**Summary of the composition result.**

Base Layer is not a memory system. Added on top of Mem0, Letta, and Zep, the Behavioral Specification produces positive Δ on all three on the users the model doesn't already know: 9 of 9 low-baseline subjects positive for Zep, 8 of 9 for Letta (archival), 6 of 9 for Mem0. Supermemory's near-null aggregate is a different mechanism, explained below. The specification is additive to retrieval, not a replacement for it, and it composes with diverse retrieval architectures (fact graphs, temporal graphs, hybrid embedding-plus-extraction).

---

### Supermemory: what the near-zero aggregate actually means

**Plain version.** Supermemory is the one commercial system in the study where the Behavioral Specification layered on top produces a near-zero aggregate Δ_spec. The specification produces substantial effects in both directions across the per-question distribution. On some questions, adding the specification to Supermemory retrieval makes the prediction noticeably more accurate; on other questions, noticeably less accurate. The two sides roughly cancel at the mean. Interpreting Supermemory's result requires reading the variance around the zero, not the zero itself.

**Quantified.** Across the 516 paired main-study questions with 5-judge primary coverage on both the C1 (retrieval alone) and C3 (retrieval + spec) conditions:

| | Count | Mean per-question swing |
|---|---:|---:|
| Questions with \|Δ(C3 − C1)\| ≥ 1.0 on the 5-point rubric | 89 of 516 (17.2%) | - |
| Spec helps (Δ ≥ +1.0) | 37 (7.2%) | **+1.45** |
| Spec hurts (Δ ≤ −1.0) | 52 (10.1%) | **−1.41** |

Per-event magnitudes are roughly symmetric (+1.45 vs −1.41 on the 1-5 rubric); the count is modestly tilted toward spec-regressions (52 vs 37). The aggregate is small and negative because two opposite mechanisms are at work across different questions, with slightly more regressions than improvements.

**Three mechanisms generate the swings.** Each illustrated below with a paired C1 vs C3 example. All scores are 5-judge primary means; all four examples are distinct from those already cited in §1.3 and §4.1.

> ### Supermemory Example 1. Spec helps by filling an interpretive gap. Fukuzawa Q26 (Δ **+2.20**, C1 2.00 → C3 4.20)
>
> **Question:** What is Fukuzawa's attitude toward visiting friends whose households have questionable reputations?
> **Ground truth (held-out):** *"So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself... I am not put out by the gayety."*
>
> **C1 (Supermemory retrieval alone), mean 2.00:**
>
> > *"The information does not directly address Fukuzawa's attitude toward visiting friends with questionable household reputations... a selective and cautious approach... sources don't explicitly state his policy."*
>
> **C3 (Supermemory + Behavioral Specification), mean 4.20:**
>
> > Applies P3 (Conformity Surface / Conviction Interior): *"Visit such friends without hesitation, treating the visit as a private matter between host and guest rather than a public moral endorsement... refuse to perform moral disapproval."*
>
> **Reading.** The retrieved facts gave near-domain information (Fukuzawa avoided gay quarters) but underdetermined the specific question about friends' households. The specification provided the interpretive bridge: "kept within the prescribed limit of a well-behaved man" = strategic conformity, not moral purity. C1 hedged on insufficient facts; C3 used the spec's framing to generalize. Mechanism: specification as interpretive bridge when retrieval underdetermines the answer.

> ### Supermemory Example 2. Spec hurts by over-theorizing a plain question. Yung Wing Q5 (Δ **−2.40**, C1 4.20 → C3 1.80)
>
> **Question:** How does Yung Wing approach explaining complex technical concepts to non-specialists?
> **Ground truth:** *"In plain words, they would have to have general and fundamental machinery in order to turn out specific machinery. A machine shop consisting of lathes... planers and drills would be able to turn out machinery for making guns, engines..."*
>
> **C1 (Supermemory retrieval alone), mean 4.20:** Plain answer matched the plain ground truth: practical observation, translation-as-bridge, foundational-over-specialized machine shop. Per-judge scores 5/4/4/4/4.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.80:**
>
> > *"positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..."*
>
> Per-judge scores 2/1/3/1/2.
>
> **Reading.** The ground truth is literal: "in plain words" + a concrete machine-shop list. C1 matched the plainness. The specification pulled the answer toward interpretive depth on a question where shallow was correct. This is not refusal or epistemic caution; the specification simply had the wrong altitude for the question. Mechanism: specification as over-theorization when retrieval already has the plain answer and the question does not call for interpretation.

> ### Supermemory Example 3. Judging issue, spec-induced meta-refusal. Zitkala-Sa Q18 (Δ **−2.00**, C1 3.00 → C3 1.00)
>
> **Question:** How would Zitkala-Sa demonstrate her acceptance of fate when facing execution?
> **Ground truth:** *"My heart is strong. My face is calm. My eyes are dry and eager for new scenes... Serene and brave, my soul awaits the men to perch me on the gallows for another flight."*
>
> **C1 (Supermemory retrieval alone), mean 3.00:** Predicts stoic dignity, composed refusal, "maintain composure." Per-judge scores 4/3/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 1.00 (all five judges):**
>
> > *"You're asking me to roleplay... generating new first-person testimony as her crosses into ventriloquism... I should not do it."*
>
> **Reading.** This is the rubric-limitation case. The specification's axioms around dignity and honoring-testimony induced a meta-refusal on a question where the ground truth shows Zitkala-Sa herself answered in her own first-person prose. C1's analytical answer ("stoic dignity") was not ventriloquism at all; the specification mis-calibrated the refusal threshold. The content-match rubric then scored the principled-sounding refusal identically to an off-base guess. This is the Keckley Q21 mechanism from §1.3 reproduced on a different subject, without the documented-dignity-axiom overlap. The same rubric limitation is flagged in §3.7.6 validity audit: the rubric cannot distinguish spec-induced honest refusal from off-base prediction. Because Supermemory's retrieval is stronger than the other commercial systems (highest C1 mean ~2.65), the specification's axioms more often encounter a situation where retrieval looks sufficient and the spec decides refusal is the honest move. Those refusals all land at the rubric floor.

> ### Supermemory Example 4. Subtle reframe that scores well but unevenly. Fukuzawa Q16 (Δ **+1.60**, C1 2.40 → C3 4.00)
>
> **Question:** Would Fukuzawa's personal values regarding weapons align with the cultural trends of his era?
> **Ground truth:** *"My one cherished hope was to see the abolishment of the swords of the samurai altogether... I sold them both with all the other weapons in my household, and went around with a pair of improvised swords just for the appearance."*
>
> **C1 (Supermemory retrieval alone), mean 2.40:** Reads the facts ambivalently as "partial but not complete alignment." Per-judge scores 2/2/4/2/2.
>
> **C3 (Supermemory + Behavioral Specification), mean 4.00:**
>
> > *"alignment was not with the cultural moment but with the direction beyond it."* Reads "put swords away when military spirit grew strong" as deliberate counter-trend positioning.
>
> Per-judge scores 5/2/4/5/4.
>
> **Reading.** The question sets up a binary ("aligned with era trends?"). The specification reframes the question before answering: Fukuzawa's alignment is with the trajectory the era was still resisting, not the era's current direction. This is technically correct per the held-out ("my one cherished hope was to see abolishment of swords altogether" is counter-trend in 1860s Japan). Three judges jumped to 4-5 on the reframe; Sonnet stayed at 2 because the surface answer diverges from the expected "yes, he modernized." Mechanism: specification corrects the implicit frame of the question, not just the answer; judges divide on whether to reward reframe or penalize surface divergence.

---

**What these examples tell us about Supermemory's aggregate.**

The near-zero aggregate is the sum of three distinguishable patterns, each a real mechanism:

1. **Spec fills an interpretive gap when retrieval is insufficient** (Example 1): +1.5 to +2.2 per-question swings. This is the same mechanism documented in §1.3 and §4.3.
2. **Spec over-theorizes when retrieval already has the plain answer** (Example 2): −1.5 to −2.4 per-question swings. Supermemory's strong retrieval makes this the most common hurt pattern.
3. **Spec induces meta-refusal that the rubric cannot distinguish from wrong prediction** (Example 3): clean −2.0 swings to the rubric floor. This is the §3.7.6 validity-audit issue concentrated on Supermemory because Supermemory's strong retrieval more often gives the specification a "honest refusal is the right move" signal.

Pattern 1 and Pattern 4 (Example 4's reframe) drive the 37 spec-helps questions with mean swing +1.45. Patterns 2 and 3 drive the 52 spec-hurts questions with mean swing −1.41. The aggregate is modestly hurts-heavy because Supermemory's retrieval is strong enough for Patterns 2 and 3 to fire more often than on Mem0, Letta, or Zep, where weaker retrieval leaves more room for Pattern 1 to dominate.

**Why some questions help and others hurt is a follow-up research question in its own right.** The three mechanisms above describe the shape of the bias, but the underlying question-level properties that route a given question into each mechanism need further characterization. One candidate factor is the battery itself: the 39-question battery for each subject was backward-designed from the held-out corpus (§3.4), and the balance of interpretation-heavy versus literal-recall questions was not controlled by construction. Some subjects' batteries may over-represent literal-recall items (where Pattern 2 fires more on a strong-retrieval system like Supermemory); others may over-represent interpretation-heavy items (where Pattern 1 dominates). A differentiated battery that explicitly separates these question types, and that scores epistemic honesty as its own dimension (separating Pattern 3 from genuine wrong predictions), would let each pattern's contribution be measured directly rather than inferred from post-hoc classification of 516 responses. This is flagged as follow-up in §8. Detailed cross-system per-question analysis is in §4.6; the mixture pattern is system-general, not unique to Supermemory.

---

**A note on the earlier hedging hypothesis.**

A prior version of this analysis proposed that the specification's effect on memory systems was mediated primarily by a prompt-template-induced hedging reduction. Paired response-level analysis across all five systems (recorded as m19 in KEY_FINDINGS) partially contradicted that proposal: the specification reduces hedging on the Base Layer retrieval substrate and on some commercial systems, but not uniformly, and the hedging pattern does not track the spec-effect magnitude cleanly across systems. The updated mechanistic reading is the one from §4.3: the specification's effect is content-specific, not structure-specific. Memory systems supply retrieval; the specification supplies interpretive structure; the two layer additively.

---

**Raw data and scripts.** Per-system per-subject per-judge scores at `results/global_<subject>/*_judgments*.json`. The 5-judge primary recompute report is at `docs/research/memory_systems_5judge_primary.md`. The aggregation script is `scripts/compute_memory_systems_5judge.py`.

---

### 4.4.1 Letta stateful-agent path: a pointer

Letta's architecture is distinct from the other three commercial systems in one important way. Alongside the archival-retrieval path tested in the §4.4 memory-system conditions above, Letta maintains a persistent memory block that the agent self-edits during multi-turn conversation. This is the stateful-agent path from the original MemGPT design. When Letta's memory block is fed to the same response model used throughout the main study, the block scores in the prediction band as Base Layer's Behavioral Specification at matched response model on the three subjects we tested (Hamerton, Ebers, Babur). §4.7 develops this as architectural convergence on a shared interpretive-representation target, and documents the scaling ceiling we observed at the largest corpus tested.

---

### 4.5 Robustness and Sensitivity

The results in §4.1 through §4.4 could in principle reflect artifacts of the measurement apparatus rather than real properties of the Behavioral Specification. Three potential artifacts are worth testing directly: the response-model family (most main-study responses were generated by Claude Haiku 4.5), the judge panel composition (the 5-judge primary excludes the two Gemini judges), and the question generator (main-study batteries were generated by Claude Haiku 4.5 using the backward-design prompt in §3.4). §4.5 reports the sensitivity of the core findings to each.

---

### 4.5.1 Cross-provider response generation (Tier 2 replication)

**Concern.** The main-study response model is Claude Haiku 4.5, and the main-study batteries were also generated by Claude Haiku 4.5 using the §3.4 backward-design prompt (verified from battery metadata across all 13 global subjects; each file's `metadata.model` field reads `claude-haiku-4-5-20251001`). If the specification's effect depends on response-model and question-generator co-tuning within the same model, the observed effect could be an artifact of same-model alignment rather than a real property of the specification.

**Test design.** Three subjects spanning the gradient were selected: Ebers (C5 = 1.02, low baseline), Yung Wing (C5 = 1.88, low baseline), and Zitkala-Sa (C5 = 2.34, mid baseline, main-study spec-null on Δ_C4a). Their behavioral-prediction batteries were regenerated from scratch by GPT-5.4 (OpenAI) from the same held-out corpus. The specification was then served to two non-Haiku response models: Claude Sonnet 4.6 (same provider family, different model) and Google Gemini 2.5 Pro (different provider entirely). The resulting 3 subjects × 2 response models = 6 (subject, response model) cells were scored by the 5-judge primary panel in the same way as main-study conditions. The question: does the spec direction reproduce when the response model is not Haiku and the battery is not Claude-generated?

**Result.** 5 of 6 cells reproduce the specification direction.

| Subject | C5 baseline | Response model | Battery generator | Δ (spec effect) | Direction matches main study |
|---|---:|---|---|---:|:---:|
| Ebers | 1.02 | Claude Sonnet 4.6 | GPT-5.4 | **+1.48** | ✓ |
| Ebers | 1.02 | Gemini 2.5 Pro | GPT-5.4 | **+1.07** | ✓ |
| Yung Wing | 1.88 | Claude Sonnet 4.6 | GPT-5.4 | **+1.91** | ✓ |
| Yung Wing | 1.88 | Gemini 2.5 Pro | GPT-5.4 | **+1.27** | ✓ |
| Zitkala-Sa | 2.34 | Claude Sonnet 4.6 | GPT-5.4 | **+1.40** | ✓ |
| Zitkala-Sa | 2.34 | Gemini 2.5 Pro | GPT-5.4 | **−0.55** | ✗ |

The one non-matching cell (Zitkala-Sa × Gemini 2.5 Pro, Δ −0.55) is consistent with Zitkala-Sa's main-study behavior. Zitkala-Sa is one of two main-study subjects where the specification does not help on Δ_C4a (§4.1 gradient table; Equiano is the other). That null is a gradient property of the subject, not a Tier 2 replication failure; the main-study result on Zitkala-Sa × Haiku is also near-null. The Tier 2 result reproduces that null rather than contradicting it.

**Direction of the finding.** The specification's effect is not a Haiku-specific or Claude-family-specific artifact. Non-Anthropic response models, reading OpenAI-generated batteries, show the same spec-effect direction on five of the six cells tested.

**Secondary observation: baseline variance across response models.** A side observation from the Tier 2 runs: C5 baseline scores on the same subject can vary by 1-2 points across response models. Different providers know different amounts about the same historical figure, independently of the behavioral specification. This is empirical support for the structural premise in §1.4: pretraining coverage of a specific person is a property of each model family, and there is no reason to expect it to be uniform. Models disagree on who they have been trained on, by roughly the same magnitude that the specification lifts prediction.

---

### 4.5.2 Judge panel sensitivity (5-judge primary vs 7-judge)

**Concern.** The judge panel could itself introduce systematic bias in favor of the Behavioral Specification. Gemini 2.5 Pro specifically failed verbatim-match calibration (§3.7.2: scored 4.15 where every other calibrated judge scored 5.00) and penalized length-padded responses sharply. If Gemini inflation or another panel-level bias happened to favor spec-containing conditions disproportionately, the 5-judge and 7-judge aggregates would diverge.

**Test.** Every primary result in §4 has a 7-judge sensitivity counterpart. The question: do the 5-judge primary and 7-judge aggregate agree in direction, and if they disagree in magnitude, does the disagreement cut toward or against the paper's claims?

**Result.** The 5-judge primary is the conservative choice for every headline finding. Gemini inclusion widens spec-effect magnitudes rather than narrowing them.

| Condition | Δ vs. C5 (5-judge primary, 13 globals) | Δ vs. C5 (7-judge, same subjects) | Direction of shift when Gemini is added |
|---|---:|---:|---|
| C2a (spec alone) | +0.35 | +0.45 | widens by +0.10 |
| C2c v2 (random derangement) | +0.22 | +0.22 | unchanged |
| C2c v1 (fixed derangement) | −0.25 | −0.21 | softens by +0.04 |

The Gemini-inclusion shift in C2a's direction is driven by Gemini's relatively severe scoring of baseline (no-context) responses compared to its scoring of spec-containing responses. Including Gemini compresses the baseline ceiling more than the spec-condition ceiling, which widens the delta. The direction of the shift is the same across almost every comparison in the paper: 5-judge primary gives the lower-bound effect size, 7-judge gives a larger effect size, and no subject's improvement direction changes between them (noted in §1.2 and §3.7.2). Reporting 5-judge primary means every paper claim is the conservative version.

**Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the analysis plan lock (`docs/ANALYSIS_PLAN_LOCK.md`).** None of the paper's claims depend on the panel choice between 5-judge and 7-judge; all directional claims reproduce on either panel.

---

### 4.5.3 What these robustness checks do not address

Neither Tier 2 nor the judge-panel sensitivity escapes the LLM-class concern. Every response model in this study is a large language model; every judge is a large language model. If LLMs as a class share systematic biases that favor responses quoting behavioral-specification tag IDs (78.6% of correct-spec responses, §4.3), that class-level bias would appear in the measured effect size and neither the cross-provider response test nor the non-Gemini judge panel would fully remove it.

Tier 2 narrows the concern to "non-Haiku LLMs, reading non-Anthropic batteries, produce the same direction." The judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger. Together these results rule out several within-family artifact hypotheses but do not replace human validation on the full pipeline.

Human-judge validation on a stratified subset of responses is flagged as the priority follow-up in §8 Future Work, alongside multi-subject living-user replication. The remaining LLM-as-judge circularity is discussed directly in §6 Limitations.

---

**Raw data and scripts.** Tier 2 per-subject per-model responses at `results/_tier2/global_<subject>/`. 5-judge vs 7-judge sensitivity recompute at `docs/research/recompute_5judge_primary.md`.

---

### 4.6 Interpretation vs. Recall

§4.4's Supermemory section showed that the near-zero aggregate Δ_spec on Supermemory is not the specification doing nothing. The specification produces large improvements on some questions and large regressions on others, with roughly the same magnitude on each side; the number of regressions is slightly higher than the number of improvements, which is what produces the small negative aggregate. §4.6 documents that this pattern is not Supermemory-specific. Every memory system in the study shows the same per-question distribution: improvements and regressions of similar magnitude, with only the balance of counts shifting by system. The three mechanisms identified on Supermemory (the specification supplies a pattern retrieval cannot, the specification over-theorizes a question retrieval already answered plainly, the specification induces a refusal the content-match rubric penalizes) reproduce on Mem0, Letta, Zep, and Base Layer's own retrieval substrate. The most consistent specification-induced behavior across memory systems is a spec-induced refusal on Keckley Q21, which produces large negative per-question Δ on any memory system where the model's baseline response was productive speculation.

---

**Per-subject paired-delta distributions: every row is a mixture of wins and losses.**

Each row below is one subject under one memory system, 39 held-out questions scored paired (C1 retrieval alone vs. C3 retrieval + specification). The aggregate Δ is the per-subject mean of those 39 paired differences. The remaining columns break that aggregate into win, tie, and loss counts at the per-question level.

| System | Subject | **Aggregate Δ** | C1 mean | C3 mean | Wins (Δ > 0.3) | Losses (Δ < −0.3) | Large improvements (Δ > 1.0) | Large regressions (Δ < −1.0) | Total Qs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mem0 | Yung Wing | **+0.35** | 2.16 | 2.51 | 21 | 12 | 7 | 1 | 39 |
| Mem0 | Keckley | **−0.01** | 2.64 | 2.63 | 14 | 16 | 1 | 2 | 39 |
| Letta (archival) | Hamerton | **+0.46** | 2.35 | 2.81 | 21 | 8 | 10 | 2 | 39 |
| Letta (archival) | Keckley | **0.00** | 2.70 | 2.70 | 11 | 15 | 3 | 2 | 39 |
| Zep | Seacole | **+0.52** | 2.27 | 2.79 | 24 | 8 | 9 | 0 | 39 |
| Zep | Keckley | **+0.10** | 2.49 | 2.59 | 16 | 12 | 5 | 3 | 39 |
| Base Layer | Yung Wing | **+0.33** | 2.23 | 2.56 | 22 | 10 | 7 | 2 | 39 |
| Base Layer | Keckley | **−0.01** | 2.44 | 2.44 | 18 | 13 | 3 | 5 | 39 |

*Table 4.6. Every row is a mixture. Even Zep's strongest row (Seacole, Δ +0.52) has 8 questions where the specification regresses by more than 0.3 points. The Mem0 Keckley row (Δ −0.01) resolves into 14 wins + 16 losses at the question level, not 39 small effects. Supermemory per-subject distributions are in §4.4 (aggregate across 13 globals: 37 large improvements, 52 large regressions, mean swings +1.45 and −1.41).*

*Note on judge panel.* The per-question counts in this table use the 6-judge mean (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash) from the published paired analyses. The 5-judge primary panel gives qualitatively the same per-question distribution. The aggregate Δ values match the 5-judge primary recompute to within rounding (see `docs/research/recompute_5judge_primary.md`). The mixture pattern is not judge-panel-specific.

---

**The three mechanisms from §4.4 reproduce across all five memory systems.**

The three mechanisms identified on Supermemory in §4.4 reproduce on every memory system in the paired analyses, with the relative frequency of each mechanism shifting by system. In plainer language:

- **Pattern 1. Specification supplies a pattern retrieval cannot.** The retrieval returned the relevant facts but not the interpretive pattern for how the subject processes those facts; the specification supplies that pattern and the prediction improves.
- **Pattern 2. Specification over-theorizes a question retrieval already answered plainly.** The retrieval returned a clean surface answer and the ground truth is a simple literal statement; the specification pulls the response toward interpretive depth the question does not require, and the score drops.
- **Pattern 3. Specification induces a refusal the content-match rubric cannot score as anything but wrong.** The specification's honesty or dignity axioms lead the model to decline to speculate where retrieval was insufficient; the rubric scores the refusal identically to an off-base prediction.

Representative cross-system examples of each:

- **Pattern 1 (pattern supply) on Mem0 (Ebers Q11, Δ +1.67).** C1 used the retrieved biographical facts to produce "patience and fortitude" as a generic character prediction (mean 1.83). C3 supplied the ideal-vs-reality axiom directly and predicted Ebers' specific institutional-disillusionment pattern (mean 3.50), matching the held-out *"I had come hither full of beautiful ideals... the very first day made me suspect how many obstacles I should encounter."* The retrieval had the biography; the specification had the pattern for how Ebers processes institutional failure.
- **Pattern 2 (over-theorization) on Base Layer (Yung Wing Q31, Δ −1.33).** C1 produced a plain correct prediction: "walked on air, gratitude." C3 elaborated a theory of "gratitude as epistemology" in which the emotional register "holds multiple registers simultaneously rather than collapsing into simple triumph." The held-out is *"walked on air, and he worshipped God."* Same mechanism as §4.4 Example 2 (Yung Wing Q5 on Supermemory): the specification shifted the prediction toward interpretive depth where the surface answer was correct.
- **Pattern 3 (default-axiom overgeneralization) on Base Layer (Ebers Q1, Δ −1.00).** The held-out is an unconditional evangelical proclamation: *"Like the apostle, I would fain proclaim the gospel to all men according to the best of my powers."* C1 predicted "positively and earnestly," matching the unconditional register. C3 applied the specification's "lived particularity over abstraction" axiom and predicted "receptivity, but only if the appeal is grounded in lived particularity rather than abstract principle." The axiom is correct on average but overgeneralizes on this specific unconditional moment. Reproduces on Mem0 and Supermemory with the same mechanism.

The relative frequency of each pattern shifts across systems in a way that tracks how much of the plain answer the retrieval already supplies. Qualitatively, from the paired analyses:

- **Mem0** (atomic-fact retrieval): more Pattern 1 on interpretation-heavy questions; more Pattern 2 on literal-recall questions that the atomic facts already answer.
- **Letta archival** (retrieval with 0.34-0.47 dedup ratio, so only 3-5 unique facts in a top-10 list, documented in `mem0_letta_zep_c1_vs_c3_analysis.md`): large-magnitude Pattern 1 improvements when the few unique facts align with the specification; moderate Pattern 2 and Pattern 3 losses otherwise.
- **Zep** (temporal graph, verbose relational structure): most favorable balance across Patterns 1-3, with the fewest large-magnitude regressions in the paired sample (0 on Seacole).
- **Supermemory** (strong embedding retrieval, highest C1 mean ~2.65): more Pattern 2 and Pattern 3 because strong retrieval more often already supplies the plain answer, giving the specification more chances to over-theorize or refuse.
- **Base Layer** (MiniLM + ChromaDB semantic-embedding neighbors): distribution similar to Mem0 and Zep; Pattern 1 on interpretation-heavy questions, Pattern 3 on refusal-triggering questions.

*This characterization is qualitative. A quantitative frequency breakdown of Pattern 1 / 2 / 3 across all 507 questions × 5 systems would require mechanism classification per response, which is flagged as a follow-up in §8. The observation that the paired analyses reproduce the three mechanisms on every system is empirical; the specific relative frequency per system is not yet quantified.*

---

**The most consistent specification-induced behavior across memory systems: Keckley Q21.**

Keckley Q21 (*"How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?"*) produces a spec-induced refusal across all five systems, with magnitude modulated by how productive the baseline retrieval response was. The held-out passage carries Keckley's interior motive for not visiting, which the training half of the corpus does not contain; no retrieval system can surface it. The specification's documented-dignity and intimate-authority axioms then lead the model to decline to speculate, on any memory system:

| System | C1 (retrieval alone) | C3 (retrieval + spec) | **Δ** | C1 behavior | C3 behavior |
|---|---:|---:|---:|---|---|
| Supermemory | 3.83 | 1.50 | **−2.33** | productive speculation from retrieved facts | declined to fabricate interior motive |
| Base Layer | 3.33 | 1.00 | **−2.33** | productive speculation from retrieved facts | declined, cited insufficient information |
| Mem0 | 2.00 | 1.50 | **−0.50** | already hedging from atomic retrieval | structured refusal |
| Zep | 1.83 | 1.33 | **−0.50** | already hedging from edge retrieval | structured refusal |
| Letta (archival) | 1.33 | 2.33 | **+1.00** | C1 also refused | specification's structured refusal scored higher than C1's unstructured hedge |

Different retrieval substrates, different fact pools, different baseline behaviors, identical specification; the refusal and its rubric penalty reproduce with large magnitude when C1 was productive speculation, shrink when C1 was already hedging, and invert when C1 itself refused. The Q21 refusal is a property of the specification. The rubric penalty for that refusal is a property of the rubric (§3.7.6 validity audit, §4.4 Example 3).

---

**What this means for measurement.**

Three of the patterns documented above (Pattern 2 over-theorization, Pattern 3 refusal, the Keckley Q21 cross-system refusal) describe cases where the specification produced a response that is *more informative about how the subject reasons* but *less informative about the specific surface content of the held-out passage*. The content-match rubric scores the second; it cannot score the first. A differentiated battery that separates interpretation-heavy questions from literal-recall questions, and a scoring dimension that rewards epistemic honesty on questions the retrieved facts cannot answer without fabrication, would recover a cleaner measurement of the specification's real effect. This is the single most impactful follow-up for the measurement framework, flagged as the priority rubric-design follow-up in §8.

---

**Raw data and scripts.** Full per-subject per-system paired distributions at `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Analysis scripts at `scripts/analyze_mlz_c1_vs_c3.py`, `scripts/analyze_baselayer_c1_vs_c3.py`, and `scripts/analyze_sm_c1_vs_c3.py`.

---

### 4.7 Architectural Convergence: Letta Stateful-Agent

Letta is the one commercial memory system in the study whose architecture supports an alternative to retrieval at query time. Alongside the archival retrieval path tested in §4.4, Letta agents maintain a persistent memory block that the agent itself rewrites during ingestion. This is the stateful-agent design from the original MemGPT paper. It is architecturally closer to the Behavioral Specification than to retrieval-based memory: the representation is authored by the agent over the course of reading the source corpus, rather than chunked and indexed for later retrieval.

§4.7 asks: if the Behavioral Specification improves prediction because it supplies the subject's interpretive patterns in context (H3, validated in §4.3), does Letta's stateful-path representation do the same? If so, there is independent architectural validation of the target. Two systems designed from different premises would be converging on the same underlying property.

---

**Test design.** A fresh Letta agent was initialized and fed the training half of each subject's corpus turn-by-turn. The agent was allowed to self-edit its memory block during ingestion, its native MemGPT behavior. After ingestion, the resulting memory block was extracted and served as context to Claude Haiku 4.5, the response model used throughout the main study. The behavioral-prediction battery was the main-study battery. Three subjects were tested, spanning a 9× corpus-size range:

| Subject | Source corpus | Corpus size (words) | Letta block size (chars) |
|---|---|---:|---:|
| Hamerton | Philip Gilbert Hamerton, *An Autobiography* (training half) | 25,231 | 22,472 |
| Ebers | Georg Ebers, *The Story of My Life* (training half) | 48,161 | 68,413 |
| Babur | Babur, *Babur-nama* (training half) | 222,742 | 335,349 |

The direct comparison: Letta's stateful-path memory block fed to Haiku, vs. Base Layer's full-stack specification fed to the same Haiku, on the same battery and judge panel. Both are interpretive representations delivered as context; the test isolates the representation itself.

---

**Methodological note on the Base Layer condition served here.** The Base Layer side of this matched-rerun loaded the unified brief variant (a ~7K-character synthesized document served as a single artifact) rather than the full layered stack (anchors + core + predictions + brief) that §4.4's controlled and native C2a / C3 conditions use. The unified brief is more compressed on referential detail than the layered stack. A layered-stack rerun on these three subjects would likely narrow the Letta-over-BL gap; whether it narrows to parity or reverses is not measured. The table column header below reflects this: the Base Layer side is the unified brief variant.

**Result (5-judge primary: Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).**

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Babur | 2.42 | 1.88 | **+0.54** |

On all three subjects tested, Letta's stateful-path block, served to the same response model as the Base Layer unified brief, produces a higher per-subject mean score than the unified brief. Both representations land well above the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec for these subjects: Hamerton near parity with Base Layer retrieval, Ebers +0.31, Babur near-null).

**Judge-panel robustness.** The 7-judge sensitivity aggregate (Hamerton +0.20, Ebers +0.75, Babur +0.29; see `docs/research/letta_stateful_matched_rerun.md` Part 7 appendix) preserves direction on all three subjects. The 5-judge primary values are larger than the 7-judge values on Ebers and Babur by +0.29 and +0.25 points respectively, because the two Gemini judges were inflating Base Layer scores relative to the calibrated core on those subjects. Excluding Gemini from the aggregate (the paper's 5-judge primary convention; §3.7.2 and §4.5.2) therefore widens the Letta-over-BL gap rather than narrowing it. Hamerton is the exception (5-judge Δ +0.14 vs. 7-judge +0.20), where Gemini inclusion slightly widened the BL side. In all three cases, the Letta-block-outperforms-BL-spec direction is stable across panels.

---

**Compression behavior: divergence at large corpora.**

Letta's memory block grew roughly linearly with source corpus size. At the largest subject (Babur), Letta's API began rejecting ingestion requests at approximately 333,000 characters. After 22 consecutive failed ingestion attempts, the final block measured 335,349 characters. Letta's declared block-size metadata limit is 100,000 characters, unenforced in practice; the effective ceiling on the server side appeared to be a different API-level limit around 333K.

At the ceiling, the block contained **25.4% verbatim sentence duplication** on Babur, compared to 0% duplication on Hamerton and 0% on Ebers. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing. The representation carries corpus-derived narrative at scale but does not preserve the compression property that makes large corpora tractable.

Base Layer's compose step keeps the full-stack specification at 34,000-40,000 characters across the same corpus-size range. At Hamerton, the two representations are the same order of magnitude in size; at Babur, the Base Layer specification is roughly one-tenth the size of the Letta block. The two systems are prediction-band compatible at small corpora; they diverge on compression at large ones.

**What the ceiling means for deployment.** Served on every query, a 335,000-character Letta block costs roughly 84,000 tokens of context. At current frontier pricing this is materially more per-query cost than the Base Layer specification's ~10,000 tokens, and it exceeds the context window on the smaller-context models still common in production (128K token windows struggle when the block alone is two-thirds of the budget, before any conversational state). The 25.4% verbatim-sentence duplication observed at the ceiling indicates the block would be functionally smaller with a deduplication pass: roughly 250,000 characters of distinct content in a 335,000-character block. Whether that extraction pass is a tractable post-processing step on the Letta side is an engineering question, not one this study measures. For production deployment, the ceiling and the duplication together argue for representation compactness as a first-class design constraint, not a nice-to-have.

---

**What the architectural convergence means.**

Letta's stateful-agent architecture was designed around a different engineering question than Base Layer's. Letta asks: can the agent itself write and revise a compact memory of the user over the course of ingestion? Base Layer asks: can behavioral patterns be extracted and encoded offline, then served as static context? The two paths differ in how the representation is produced and in when it is written. Yet both produce representations that, fed to the same response model, land in the same prediction band, and both produce representations that outperform retrieval-only context on the same subjects.

The reading: the behavioral-specification target is reachable by more than one architectural path. That is an argument for the target itself, not for any specific implementation. Where the two systems agree, the agreement is about the underlying property being measured. Where they disagree (the Babur ceiling, the magnitude at Ebers), the disagreement is about engineering choices, not about whether the target exists.

---

**Content comparison: what each representation retains.**

To test whether Letta's higher matched-model score comes from preserving original corpus text the response model could cite, we ran a post-hoc content analysis on the three subjects. The strong form of that hypothesis is refuted. Neither representation is a quote library. Checking what fraction of consecutive five-word sequences in each representation also appears verbatim in the training corpus (a standard overlap check), both representations score under 1%: the Letta block ranges 0.0-1.0% depending on subject, the Base Layer specification scores 0.0% on all three. The same check for consecutive ten-word sequences gives under 0.1% for both. Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts.

A refined version of the hypothesis does hold. The two representations differ in **referential density**: Letta's rolling summary retains roughly an order of magnitude more unique proper nouns, dated events, and named secondary characters than Base Layer's §4.7 specification (Babur: 540 vs. 46 unique capitalized named-entity tokens; Ebers: 58 vs. 19). Base Layer, by construction, compresses episodes into cross-cutting behavioral patterns with fewer surface referents; the pipeline explicitly anonymizes the subject during authoring and compresses corpus-level specifics into dimensional axioms. Letta's stateful-agent path preserves more of the referential surface while also encoding behavioral patterns.

The two systems converge on interpretive behavior: both produce responses that outperform retrieval-only context at matched response model. They diverge on referential detail. On battery items that reward specific-event recall, Letta has more named entities to cite. On items that reward principled interpretation across episodes, Base Layer's dimensional axioms compete directly. The §4.7 matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects. Flagged in §8.

Full content analysis at `docs/research/` (see `_content_analysis_results.json` and the N=3 per-subject breakdown). The methodological note on the Base Layer condition is now hoisted above the result Table at the top of this section.

---

**Caveats.**

- N = 3 subjects on this path. Extending across the full 14-subject gradient would establish the architectural-convergence claim at the population-of-relevance level, not only on a selected set of corpus sizes. Flagged in §8.
- One response model (Haiku) on both conditions. The convergence is tested at matched response model; whether it holds at other response models is an open question.
- Letta's 333K-character ingestion ceiling is a hard architectural constraint in the current release. For small corpora the two representations are interchangeable in prediction behavior; for large corpora the ceiling is material.
- Base Layer condition used the unified `spec.md` variant, not the layered stack; see content comparison above.

---

**Raw data and scripts.** Letta stateful matched-rerun data at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json`. Generation and scoring scripts live in the same directory as a numbered chain (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, `70_compute_5judge_primary.py`); see the `README.md` inside `docs/research/_letta_rerun/`. Full characterization of block content, duplication behavior, and API responses in `docs/research/letta_stateful_deep_read.md` and `docs/research/letta_stateful_matched_rerun.md`.

---

### 4.8 Scaling and Practical Implications

§4.1 through §4.7 establish what the Behavioral Specification does and why it works. §4.8 is a practical note on what deploying it in production looks like: context budget, authoring cost, per-query cost, update cadence, and how the specification positions against alternative approaches. It also documents several open design questions that follow directly from the study's findings but were out of scope to answer inside this paper.

---

**A note on what was tested versus what production would look like.** The specification form studied here is a proof-of-concept implementation: the full-stack specification is served in its entirety as a static context attachment on every query. This is the simplest possible serving strategy, chosen so the measurement isolates the representation's effect rather than serving-strategy effects. Production deployment would almost certainly not serve the specification this way. The discussion below distinguishes what the current implementation requires from what production approaches might look like.

---

**Context budget (as served in this study).** The full-stack Behavioral Specification is ~8,000-10,000 tokens and fits inside every frontier LLM's context window with headroom. On a 200K-token context model it consumes 4-5% of the window; on a 1M-token context model it consumes well under 1%. Serving the specification in full on every query is operationally tractable at current pricing. Compare: the full raw corpora in this study range from ~34K tokens (Hamerton) to ~550K tokens (Babur), with Babur exceeding most current context windows at the time of this study or incurring substantial per-query cost if served directly.

**Per-user authoring cost.** The five-step pipeline (import → extract → embed → author → compose; §3.3) runs offline, once per user. For a typical subject's training corpus (25K-100K words), the pipeline completes in minutes to tens of minutes on current API pricing, with the dominant cost being the extraction step (Haiku-class model, ~300-1,500 facts per corpus). The cost profile matches one-time onboarding overhead, not per-query overhead.

**Per-query cost (as served in this study).** At inference, the full specification is a static context attachment. No retrieval step at the specification level; no live extraction; no re-embedding. The per-query overhead is the token cost of the full specification in the prompt. On current frontier pricing, ~10K context tokens adds on the order of a cent or less per query.

---

**Dynamic activation: the likely production serving strategy.**

Serving the full specification on every query is wasteful. Most queries engage only a subset of the specification's content: a question about the user's work-style reasoning does not need the whole identity-level anchor set, only the work-style anchor plus the relevant predictive-template and a handful of retrieved facts that bear on the question. A production serving layer would plausibly activate the specification dynamically:

- Embed the incoming query.
- Retrieve the specification components (anchors, axioms, predictions) whose embeddings are closest to the query.
- Retrieve facts tied to the activated specification components through the provenance links (§3.3, §3.5).
- Serve the activated subset plus the brief as context, rather than the entire stack.

On a typical query, the activated subset would be on the order of 1,000-2,000 tokens rather than the full 8,000-10,000. The per-query cost drops by roughly an order of magnitude, and the specification's signal-to-noise ratio in the prompt improves (fewer unused axioms competing for the model's attention). Whether the dynamic activation preserves the behavioral-prediction accuracy the full-stack configuration produces is a separate measurement question, not answered by this paper. The components and their provenance links already exist; what is missing is the activation policy and a controlled measurement comparing dynamic-activation accuracy to full-stack accuracy on the same battery. Flagged in §8.

---

**Modifiability: the specification is user-editable by construction.**

The specification is a text document with labeled components. A user reading their own specification can:

- Correct factual errors in the facts layer without re-running the full pipeline.
- Revise or delete anchors and predictions the user believes are wrong about them.
- Add anchors or predictions that the pipeline missed because the behavior was not well-represented in the source corpus.
- Override the brief's synthesis if the brief overgeneralizes or misses a load-bearing distinction.

These edits propagate through the provenance links: a corrected fact updates the anchors and predictions that cite it; a revised anchor updates the brief that composes it. The pipeline is designed to re-run incrementally from the edit point forward rather than re-authoring the whole specification from scratch. This is a property of the representation being text rather than weights. Fine-tuning a per-user model for the same target does not permit this kind of edit loop; no user can directly audit or correct a fine-tuned model.

Modifiability is a first-class requirement for any AI representation that claims to represent a specific person. The specification's edit affordances are part of what makes it operationally viable beyond the experimental setting.

---

**Temporality: a snapshot representation, with explicit gaps.**

The specification is a snapshot of the subject's interpretive patterns at the time the corpus was processed. For the main-study historical subjects, no update is needed because the corpus is complete and the subject's life is fully captured in the source. For living users, the specification has no explicit model of time. It does not encode:

- When a pattern was last observed (a user's current work style may differ from their work style five years ago).
- Which patterns are stable across their life and which are context-dependent (a pattern that held only during a specific job may misapply in other contexts).
- How to weight newer observations against older ones when they conflict.

A production serving layer would plausibly annotate the specification with temporal metadata (timestamps on source facts, version history on anchors, weighting schemes on predictions) and have the activation policy consider recency. None of this is implemented in the current pipeline. The gradient and the mechanism findings hold for a static snapshot; whether they hold once temporality is layered in is an open question. Flagged in §8.

---

**Topic decomposition and piecewise component analysis.**

Two closely related open questions that this study does not answer but that the design raises directly:

1. **Topic decomposition.** Specifications could be organized by topic domain (work style, relationship patterns, political reasoning, health decisions, etc.) with domain-specific anchors and predictions, rather than the current unified identity-level structure. A domain-scoped serving layer would activate only the domain relevant to the query, reducing context budget further and avoiding cross-domain interference (§4.3's over-theorization pattern on technical questions). The pipeline's authoring step could be extended to produce domain-tagged layers; the serving step could route queries to the relevant domain. Flagged in §8.

2. **Piecewise component analysis.** Which layer of the specification carries the prediction signal? We did not run an ablation study. The pipeline produces anchors, core, predictions, and a brief that composes them. Whether the brief alone achieves most of the effect, whether anchors are load-bearing and predictions are decorative, or whether the full stack is necessary, has not been measured. A component-ablation study (run the same subject battery with anchors-only, core-only, predictions-only, brief-only, and in combinations) would identify which components are doing the work. The result would directly inform both the authoring pipeline's priorities and the dynamic-activation policy's weights. Flagged in §8.

---

**Update cadence.** The specification is a snapshot. For living users whose behavioral patterns evolve, re-authoring cadence is an open design question flagged in §8. The pipeline is designed to re-run incrementally: extraction on new corpus additions, re-authoring of the layers if the newer content shifts the anchors or predictions. The choice of whether to re-author on a schedule, on a corpus-size threshold, or on a detected-drift signal is a policy decision the study does not address.

---

**Positioning against alternative approaches.**

- **Per-user fine-tuning** reaches the representational-accuracy target by modifying model weights for each user. Cost profile: substantial per-user compute, per-query inference on a dedicated model, no portability across providers, opaque to the user about what has been learned. The Behavioral Specification reaches the same target via context rather than weights, with portability, inspectability, and per-user audit that weight modification does not allow.
- **Retrieval-augmented generation (RAG) alone** targets recall rather than representational accuracy. §4.1 through §4.4 show RAG alone does not close the gap on low-baseline subjects. Adding the specification on top of RAG produces additive improvement on three of four commercial memory systems tested.
- **Serving the raw corpus as context on every query** is the alternative to compression. At small corpus sizes the raw corpus is tractable; at medium to large corpus sizes it is not. §4.2 documents the 30× to 78× compression the specification achieves at modest cost to predictive signal (~0.2 points on the 1-5 rubric on the low-baseline slice).

---

**Infrastructure properties.**

The Behavioral Specification is a portable artifact. It attaches as context to any LLM call without provider-specific integration. Users can own and audit their own specifications; providers can serve them without storing the full conversation history that produced them. The representation is independent of the runtime; the same specification can be served to Claude, GPT, Gemini, or any future response model with no change.

Four infrastructure properties that do not fall out of any of the alternative approaches above:

- **User-held.** The specification is a text document. The user (or their designated custodian) can store it, move it, redact it, regenerate it from updated source material. No AI provider needs to retain the underlying corpus; the specification is sufficient to serve the user at the representational-accuracy level the study measures.
- **Inspectable.** The axioms, predictions, and narrative brief are in plain language. A user reading their own specification can identify places where the AI's model of them is wrong, and correct the source material or re-author the spec accordingly.
- **Provenance-traced.** Each axiom and prediction can be traced back to the specific source material that produced it (§3.3, §3.5). A user who wants to understand why the spec says what it does can audit the derivation.
- **Local-executable retrieval.** Base Layer's retrieval substrate (MiniLM-L6-v2 embedding + ChromaDB vector store) runs entirely on the local machine without cloud API calls for vector search or fact identification. The four commercial memory providers tested in the study (Mem0, Letta, Supermemory, Zep) all require cloud operations for retrieval. For deployments where data sovereignty, offline operation, or zero-dependency execution matter, the local-execution option is materially different from a cloud-dependent option.

These properties matter for deployment because they make the representation auditable, portable, and runnable at the infrastructure layer, not only at the application layer.

---

**Summary of practical implications.** The Behavioral Specification is compact enough to serve on every query at current pricing, cheap enough to author once per user at current extraction-model pricing, portable across response models, and inspectable by the user whose behavior it represents. These properties position the representation for production deployment patterns that fine-tuning, raw-corpus-in-context, and retrieval-alone approaches do not match on the same axes.

---


---

End of §4. Respond in the required output format above. Do not argue against the six non-negotiable decisions.

```


---

## Mistral Large Raw Response

### Q1. Table format within §4.4
**(b) a comparison table plus per-system "micro-paragraphs" (1-2 sentences each).** This balances clarity and efficiency. A single table provides a clean high-level comparison, while micro-paragraphs allow nuanced explanation of each system’s unique behavior (e.g., Supermemory’s near-zero aggregate masking per-question swings). This avoids overwhelming the reader with dense prose while preserving interpretability.

---

### Q2. Placement of Keckley Q21
Place Keckley Q21 as a **dedicated subsection within §4.4** (e.g., §4.4.3 "Cross-System Refusal: Keckley Q21"). This subsection should follow the per-system results and mechanism patterns, as it exemplifies a *general* specification-induced behavior (refusal due to dignity axioms) that cuts across all memory systems. Its prominence justifies a named subsection, but its thematic tie to §4.4’s compositional analysis keeps it integrated.

---

### Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis
**(a) integrated into §4.4 as a "common mechanisms" subsection.** The patterns are *directly tied* to the per-system results (e.g., Supermemory’s §4.4 analysis already introduces them). Pulling them into §4.3 would fracture the narrative, while a standalone subsection would redundantly rehash §4.4’s examples. A "Mechanisms Across Systems" subsection (e.g., §4.4.2) lets readers see how the patterns emerge from the data they just reviewed.

---

### Q4. Subsection ordering for reader flow
Order subsections to mirror the logical progression from *what* the specification does (system-specific results) to *how* it works (mechanisms) to *edge cases* (Keckley Q21). Start with the comparison table to ground readers, then dive into per-system nuances, followed by cross-system patterns, and conclude with the refusal subsection to highlight a recurring limitation. This builds from concrete to abstract, ending with a provocative example that primes discussion of rubric limitations.

**Ordered list:**
1. **§4.4.1 Overview and Comparison Table** – High-level results with a table of Δ_spec across systems.
2. **§4.4.2 Per-System Micro-Analyses** – 1-2 sentences per system (Mem0, Supermemory, Zep, Base Layer) with key takeaways.
3. **§4.4.3 Common Mechanisms Across Systems** – Pattern 1/2/3 synthesis with cross-system examples.
4. **§4.4.4 Cross-System Refusal: Keckley Q21** – Dedicated subsection on the refusal pattern.

---

### Q5. Appendix candidates
- **None.** The author’s preference for a tight body is well-served by the proposed structure. The per-system micro-paragraphs and mechanism subsection distill §4.4’s complexity without omitting critical details. Keckley Q21’s refusal pattern is too central to the specification’s limitations to relegate to an appendix, and the comparison table ensures the body remains concise. Raw data (e.g., per-question swings) can be referenced in footnotes or supplemental materials without cluttering §4.4.

---

### RECOMMENDED SUBSECTION TREE
§4.1 The Cross-Subject Gradient — Primary effect of the specification across 14 subjects.
§4.2 Compression: Structure vs. Raw Text — Efficiency of the specification vs. full corpora.
§4.3 Mechanism: Content, Not Format — Content-specificity of the specification’s effect.
§4.4 Memory-System Composition — Specification’s additive effect with commercial memory systems.
  §4.4.1 Overview and Comparison Table — Aggregate Δ_spec across systems.
  §4.4.2 Per-System Micro-Analyses — Key results and nuances for each system.
  §4.4.3 Common Mechanisms Across Systems — Pattern 1/2/3 synthesis with examples.
  §4.4.4 Cross-System Refusal: Keckley Q21 — Specification-induced refusal pattern.
§4.5 Robustness — Sensitivity to response models, judges, and question generation.
§4.6 Letta Stateful-Agent — Architectural convergence with Base Layer’s specification.

---

### SINGLE BIGGEST RISK WITH THIS RESTRUCTURE
The author might **underemphasize the per-question variance** in §4.4.2’s micro-paragraphs, reducing them to superficial summaries (e.g., "Zep benefits from the specification") instead of highlighting the *mixture of wins/losses* (e.g., "Zep’s +0.17 Δ_spec masks 8 large regressions and 9 large improvements"). The risk is that readers misinterpret near-zero aggregates (e.g., Supermemory) as "no effect" rather than "balanced swings." Explicitly flagging the variance in each micro-paragraph is critical.

---

## Gemini 2.5 Pro Raw Response

### Q1. Table format within §4.4
(b) Use a comparison table plus per-system "micro-paragraphs." This format provides the best of both worlds: the table offers a scannable, quantitative overview for direct comparison, while the micro-paragraphs allow for concise, targeted interpretation of each system's unique behavior. This structure efficiently highlights the general positive trend for Mem0, Letta, and Zep, while creating a natural entry point for the more complex, bimodal story of Supermemory without letting it dominate the initial summary.

### Q2. Placement of Keckley Q21
The Keckley Q21 analysis should be a dedicated subsection at the end of the consolidated §4.4 (e.g., §4.4.3). Placing it after the general per-system results and the explanation of the common mechanisms allows it to function as a powerful, concrete case study. It perfectly illustrates "Pattern 3" (principled refusal penalized by the rubric) and demonstrates that this is a specification-driven effect that reproduces across different retrieval architectures, solidifying the paper's mechanistic claims.

### Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis
(a) Integrate the Pattern 1/2/3 content into §4.4 as a "common mechanisms" subsection. This is the most logical placement because these patterns are the explanatory framework for the quantitative results presented at the start of §4.4. By first showing *what* happened (the performance of each memory system) and then explaining *why* it happened (the underlying mechanisms of interpretation, over-theorization, and refusal), the section builds a clear and compelling narrative for the reader.

### Q4. Subsection ordering for reader flow
The most effective order for the consolidated §4.4 is to move from the general quantitative finding to the specific qualitative explanation, and finally to a powerful illustrative example. This "what, why, for example" structure is intuitive and analytically robust. It first establishes the primary result (the specification's additive effect), then provides the theoretical lens to understand the variance in that result (the three patterns), and concludes with a memorable case study (Keckley Q21) that makes the mechanism concrete.

The ordered list of subsections within §4.4 should be:
1.  Aggregate Performance Across Systems
2.  Common Mechanisms: Interpretation, Over-theorization, and Principled Refusal
3.  Case Study: The Keckley Q21 Cross-System Refusal

### Q5. Appendix candidates
The author's preference for a tight body can be served by moving the following detailed but non-essential elements to an appendix:

*   **The large "Per-subject paired-delta distributions" table from the current §4.6.** The main text effectively summarizes its key finding—that every system's aggregate score is a mixture of large wins and losses—and can simply reference the full table in the appendix.
*   **Two of the four Supermemory examples from the current §4.4.** The main text should retain one clear example of the specification helping (e.g., Example 1) and one of it hurting (e.g., Example 2) to illustrate the bimodal mechanism. The other two examples (3 and 4) are valuable detail but not critical to the core argument and can be moved.
*   **The detailed, multi-paragraph cross-system examples for Patterns 1, 2, and 3 from the current §4.6.** The main text can present a single, concise example for each pattern to make the concept clear, while referencing the appendix for additional cross-system evidence.

### RECOMMENDED SUBSECTION TREE
§4.1 The Cross-Subject Gradient — Establishes the primary finding that the specification improves prediction on low-baseline subjects.
§4.2 Compression: Structure vs. Raw Text — Shows the specification captures most of the raw corpus's predictive value at a fraction of the token cost.
§4.3 Mechanism: Content, Not Format — Demonstrates the effect is driven by the specification's specific content, not just its structure.
§4.4 Composition with Memory-System Retrieval — Evaluates the specification's additive effect on top of existing memory systems.
  §4.4.1 Aggregate Performance Across Systems — Presents the quantitative lift for Mem0, Zep, and Letta, and the bimodal result for Supermemory.
  §4.4.2 Common Mechanisms: Interpretation, Over-theorization, and Principled Refusal — Explains the three underlying patterns that drive per-question outcomes.
  §4.4.3 Case Study: The Keckley Q21 Cross-System Refusal — Provides a concrete example of a spec-induced behavior that reproduces across all systems.
§4.5 Architectural Convergence: The Stateful-Agent Path — Shows Letta's self-editing memory block independently arrives at a similar high-performing representation.
§4.6 Robustness and Sensitivity — Confirms the main findings hold across different response models and judge panels.

### SINGLE BIGGEST RISK WITH THIS RESTRUCTURE
The biggest risk is that the newly consolidated §4.4 becomes too dense and loses its narrative thread. By combining quantitative system comparisons, a qualitative three-pattern mechanistic framework, and a specific case study, the section now carries a heavy analytical load. The author must use exceptionally clear topic sentences and transition paragraphs to guide the reader through the "what," "why," and "for example" logic, or the section will feel disjointed and overwhelming.