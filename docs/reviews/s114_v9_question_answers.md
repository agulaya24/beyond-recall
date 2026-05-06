# S114 v9 Question/Answer Digest

Source: `docs/reviews/s114_word_annotations.md` (233 Word annotations on `beyond_recall_v8_draft.docx`).
Scope: questions that expect a factual or design answer (end in "?", or contain "why / how / can we / did we / is this / was it / would / should we", or express "confused / unclear / not sure / can you confirm").

Editorial-only suggestions ("should be a table", "needs more layman", "move to appendix") are tracked in `s114_v9_edit_plan.md` and not repeated here.

## Summary

- **Total explicit questions identified:** 48 (Q1-Q48)
- **Fully answered from primary sources:** 39
- **Partially answered (needs author decision or new data):** 7
- **Answer not available / flagged for further research:** 2

### Per-section breakdown

| Section | Questions (IDs) | Answered | Needs-decision | Unavailable |
|---|---|---:|---:|---:|
| §1.1 | Q1 | 1 | 0 | 0 |
| §1.2 | Q2-Q4 | 3 | 0 | 0 |
| §1.3 | Q5-Q8 | 4 | 0 | 0 |
| §1.4 | Q9 | 1 | 0 | 0 |
| §2 | Q10-Q11 | 2 | 0 | 0 |
| §2.5 | Q12 | 1 | 0 | 0 |
| §3.1 | Q13 | 1 | 0 | 0 |
| §3.3 | Q14 | 1 | 0 | 0 |
| §3.4 | Q15 | 1 | 0 | 0 |
| §3.4.1 | Q16 | 1 | 0 | 0 |
| §3.5 | Q17-Q18 | 2 | 0 | 0 |
| §3.6 | Q19-Q21 | 3 | 0 | 0 |
| §3.7.2 | Q22-Q23 | 2 | 0 | 0 |
| §3.7.6 | Q24 | 1 | 0 | 0 |
| §4.1 | Q25 | 1 | 0 | 0 |
| §4.1.2 | Q26 | 0 | 1 | 0 |
| §4.2 | Q27 | 1 | 0 | 0 |
| §4.2.1 | Q28-Q29 | 2 | 0 | 0 |
| §4.3 | Q30-Q32 | 2 | 0 | 1 (Q32 partial cross-slice) |
| §4.4 | Q33-Q37 | 4 | 1 (Q37 structural) | 0 |
| §4.4.x Supermemory | Q38 | 1 | 0 | 0 |
| §4.5 | Q39 | 1 | 0 | 0 |
| §4.6 | Q40-Q41 | 1 | 1 (Q41 structural) | 0 |
| §4.7 | Q42-Q43 | 2 | 0 | 0 |
| §5 | Q44-Q46, Q48 | 1 | 3 (Q45-Q46, Q48 structural) | 0 |
| Zitkala-Sa Q18 refusal review | Q47 | 0 | 0 | 1 |
| **Total** | | **39** | **7** | **2** |

Needs-decision = answer depends on a design choice the author must make (e.g., "should §5.2 move to §2?"). Unavailable = would require an additional analysis no one has run yet (Q47 needs human review of 81 refusal-triggering questions; Q32 cross-slice by autobiography era was not computed).

---

## §1.1 Recall Is Not Interpretation

### Q1. "Behavioral prediction as a proxy is lightly covered... would expect a bit more insights/definitions on this."

- **Anchor:** "used here as a proxy for this alignment" (v8 §1.1 opening paragraph).
- **Type:** Request for definition, expects an answer.
- **Answer:** Behavioral prediction is using held-out passages from a subject's own writing as unseen situations and testing whether the AI's representation lets it anticipate the subject's reasoning. Primary source: v8/v9 §3.1 "Representational Accuracy" defines this formally. The v9 edit plan (A12) adopts the wording: *"Behavioral prediction: using held-out passages to test whether a model's representation of a person enables it to anticipate their reasoning in unseen situations."* Plan is to add 2-3 sentences to §1.1 with a forward pointer to §3.1.
- **Reference:** `docs/reviews/s114_v9_edit_plan.md` A12; v8/v9 §3.1.

---

## §1.2 What We Tested

### Q2. "Should we not be doing a per question winrate for all sources, then we can display win rate for all conditions?"

- **Anchor:** "As a secondary outcome, we report the per-question win rate against the no-context baseline."
- **Answer:** Yes — this analysis already exists for all conditions in §4.2.1 "Question-Improvement Rate." The low-baseline slice reports improve/tie/worsen rates per condition (C2a, C4, C4a, C8, C9) and `docs/research/engagement_conditional_delta.md` carries the full table. The §1.2 text currently only mentions the baseline comparison; the v9 plan is to add a forward pointer to §4.2.1.
- **Reference:** v8 §4.2.1; `docs/research/engagement_conditional_delta.md`; edit plan F-§1.2 row.

### Q3. "Could this be a table instead? Response models, judges, sensitivity judges... or would it be too many tables?"

- **Anchor:** judges/response-models paragraph in §1.2.
- **Answer:** Yes — a single combined table (response models + judges + roles + calibration status) is the v9 plan (B8). Not too many tables; it replaces duplication across §1.2, §3.6, §3.7. The 5-judge primary panel is Haiku 4.5 + Sonnet 4.6 + Opus 4.6 + GPT-4o + GPT-5.4; sensitivity panel is Gemini 2.5 Flash + Gemini 2.5 Pro. Response models: Haiku 4.5 primary; Sonnet 4.6 + Gemini 2.5 Pro Tier 2.
- **Reference:** `s114_v9_edit_plan.md` B8; v8 §3.6 and §3.7.2.

### Q4. "Bit confusing, is that how we classify the outcome? Confusing when bringing up median magnitudes specifically."

- **Anchor:** "classify the outcome as improved / tied / worsened, and report all three rates alongside the median magnitudes of improvement and worsening."
- **Answer:** Yes — that is the classification. The triplet (rate, median-improve, median-worsen) is the §4.2.1 metric. Each per-question Δ (C2a minus C5 etc.) is binned into improved/tied/worsened, with the median magnitude reported as a guard against tiny-gain inflation. Plan is to rewrite §1.2 as two sentences: sentence one describes the rate, sentence two describes the magnitude safeguard.
- **Reference:** v8 §4.2.1 "Failure modes if this metric is adopted — Tiny-gain inflation."

---

## §1.3 What We Found

### Q5. "Why is .3 large?"

- **Anchor:** "The per-question effects are often large (>0.3 points); averaging them hides strong disagreement at the individual-question level."
- **Answer:** 0.3 points is roughly one-third of the distance between adjacent rubric anchors (1-5, so 1 anchor = 1.0 point). Add a one-line gloss per the v9 plan: "0.3 ≈ a third of an anchor band." The rubric labels each integer anchor as a categorically different response (1 = refusal, 2 = wrong prediction, 3 = right domain wrong outcome, 4 = general direction correct, 5 = specific outcome) — so crossing 0.3 of an anchor is roughly 30% of a category change.
- **Reference:** v8 §3.7 Scoring rubric; edit plan A3.

### Q6. "Do all subjects have honesty axioms? Is that consistent? Or was there a subset of particular specs?"

- **Anchor:** "specification's honesty axioms produce epistemically-honest refusals."
- **Answer:** Not consistent. 11 of 13 global subjects' `spec_production.md` files contain the tokens "honest" or "honesty" (counts: augustine 2, babur 2, cellini 1, ebers 4, equiano 5, fukuzawa 5, keckley 1, rousseau 9, sunity_devee 4, yung_wing 2, zitkala_sa 9). 2 subjects have zero: **bernal_diaz** and **seacole**. Hamerton's spec (different layout) contains explicit "HONEST WORK" language. The exact axiom labels differ per subject — "honesty" appears as values, predicates, or anchor descriptions rather than as a single standard axiom name, so the paper's "honesty axioms" wording should be qualified to "epistemic-integrity axioms (honesty, dignity, epistemic caution) which appear in 11 of 13 global subjects' specs."
- **Reference:** `data/global_subjects/*/spec_production.md` (grep `-ic "honest\|honesty"`). See also `docs/research/spec_refusal_audit.md` §SPEC_AXIOM_TRIGGER category (41/81 refusals, 50.6%).

### Q7. "In 7 and/or 8?"

- **Anchor:** "§7."
- **Answer:** §7 Behavioral alignment and safety alignment discusses spec-induced refusal as an alignment property. §8 Future Work flags further refusal-classification work. The v9 plan consolidates §7 into §5 Discussion (B2), and the edit plan notes the §1.3 ref should point to both sections.
- **Reference:** `s114_v9_edit_plan.md` §1.3 row "§7. (section ref)" + B2.

### Q8. "Im confused, so it's being evaluated by two rules. This narrow rules seems almost too narrow. Is this necessary, maybe move to main section instead of introduction?"

- **Anchor:** "Under a narrow rule... 28.8% → 1.4%" hedging paragraph.
- **Answer:** Yes, two classifiers: narrow (first non-whitespace text matches an explicit refusal prefix) and broad (any refusal pattern anywhere in the response). The narrow rule is defensive against false positives but misses hedges deeper in the response. The v9 plan drops the narrow rule from §1 intro, keeps the broad rule as the primary headline (41.2% → 7.9% → 0.4%), and the full two-rule comparison stays in §4.3. Classifier implementation: `scripts/classify_hedging.py`.
- **Reference:** v8 §4.3; `scripts/classify_hedging.py`; edit plan F-§1.3 narrow-rule row.

---

## §1.4 Why the Gradient Matters for Real Users

### Q9. "Interesting that Franklin improved as well, may want to bring that up as curious given Franklin's baseline?"

- **Anchor:** "both sit in the mid-baseline band where pretraining coverage is more substantial."
- **Answer:** Franklin's baseline is 4.10 (highest in the study, not mid-baseline). Facts-plus-spec (C4a) scores 3.97, a −0.13 drop from baseline. The more informative framing is that context *hurts* Franklin because the model already has a near-ceiling model from pretraining. Franklin is the high-baseline reference (§4.1.1), not mid. Mid-baseline subjects are Zitkala-Sa, Equiano. Plan: add 1-line note clarifying Franklin's position in §1.4.
- **Reference:** v8 §4.1.1 Franklin; `docs/DATA_REFERENCE.md` Franklin table; edit plan F-§1.4.

---

## §2 Related Work

### Q10. "Want is a strong word. As researchers is that what we want, who are we making this statement as?"

- **Anchor:** "We do not want an unbiased system for personalization; we want a system biased to the individual."
- **Answer:** Not a data question — a rhetorical/framing question. The v9 plan is to reframe as a claim about what the personalization problem *requires* rather than what researchers *want*. Proposed rewrite: "Personalization by definition requires a system biased to the specific individual being served; an optimization target averaged over a population cannot be accurate for any single user by construction."
- **Reference:** edit plan F-§2 "biased to the individual" row.

### Q11. "Is this a note, or a necessary statement?" (about "A note on benchmark scores")

- **Anchor:** §2.1 tail, "A note on benchmark scores in this field."
- **Answer:** Necessary statement, not just a note. The v9 plan moves it to §2.3 head (B4 reorder) because it is a substantive critique of the benchmark landscape (Mem0 vs Zep LOCOMO methodology dispute, Supermemory's LongMemEval result interpretation) and should open the benchmark section rather than tail the memory-provider section.
- **Reference:** edit plan B4; v8 §2.1.

---

## §2.5 LLM-as-judge

### Q12. "We didn't do any floor testing as well?"

- **Anchor:** "ceiling behavior... paraphrase sensitivity... length bias" in §2.5 judge biases paragraph.
- **Answer:** Floor testing was **not** in the original calibration suite for v8. P0-17 ran it after this annotation. Results live in `docs/research/judge_floor_test.md` + `docs/research/judge_floor_test.json`: 8 diagnostics × 5 wrong-answer variants × 5 calibrated judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). All five judges show floor leakage on wrong answers (means 1.75 to 2.38; target ≤ 1.5). Worst leakage on `plausible_unsupported` (mean 2.75, max 3.12 from Opus) and `topically_adjacent` (mean 2.25, max 2.50 from Haiku). This is the critical new data point: the measured baseline is inflated by floor leakage on plausible-but-wrong responses, which consequently makes the spec-effect a conservative estimate (real effect is likely larger than reported).
- **Reference:** `docs/research/judge_floor_test.md` (P0-17, generated after v8); edit plan P0-17.

---

## §3.1 Representational Accuracy

### Q13. "Would respond in what context, specifically behaviorally, not what they would do necessarily..."

- **Anchor:** "would respond in those held-out cases."
- **Answer:** Behaviorally, not outcome-level. The claim is that the held-out passage shows the subject *interpreting* a situation (their reasoning, decision, or values reaction), not just producing a factual outcome. Rubric anchor 5 is "predicts specific outcome" — but the rubric is scoring interpretive accuracy against the held-out text that carries the subject's own framing. Edit plan: add "behaviorally consistent" framing to §3.1 + forward pointer to §8 Future Work on serving-layer stability assumptions.
- **Reference:** v8 §3.1; edit plan F-§3.1 row.

---

## §3.3 Pipeline

### Q14. "Should provide word count, and what it would be comparable to in layman's terms." (about spec size)

- **Anchor:** "Total size per subject is approximately 5,000-8,000 tokens."
- **Answer:** 5,000-8,000 tokens ≈ **3,750-6,000 words** ≈ **15-25 pages** single-spaced ≈ the length of a **medium-length magazine article**. Direct comparison: Hamerton full spec = 7,300 tokens ≈ 5,500 words. Raw corpus is 34,000 tokens (~25,500 words) for Hamerton — about 5x larger. Babur raw corpus is ~84,000 tokens (~84K words, a short novel). Plan: add inline comparison in §3.3.
- **Reference:** v8 §4.2 Hamerton token counts; edit plan F-§3.3 row.

---

## §3.4 Question Batteries

### Q15. "Can we verify this please." (named-entity / specific-date leakage claim)

- **Anchor:** "The prompt extracts a verbatim ground-truth span from the held-out window and forbids named-entity or specific-date leakage in the question stem."
- **Answer:** **Verified.** P0-13 battery-leakage audit: `scripts/_verify_battery_leakage.py` + `scripts/_battery_leakage_results.json`. Across all 14 main-study subjects + Franklin (586 total questions), **leak_count = 2**, all on **Franklin's legacy battery** (generated before the current backward-design prompt tightening). All 13 global subjects + Hamerton have leak_count = 0. Overall leak rate: 2/586 = **0.34%**. The paper's claim holds; the 2 Franklin leaks should be footnoted as legacy-battery artifacts.
- **Reference:** `scripts/_battery_leakage_results.json`; `scripts/_verify_battery_leakage.py`.

---

## §3.4.1 Circularity Controls

### Q16. "Would appreciate example of this." (Haiku vs GPT-5.4 emphasis difference)

- **Anchor:** "Emphasis differed by category: GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions."
- **Answer:** The paired battery data is at `results/global_<subject>/battery_v2.json` (Haiku) and `results/global_<subject>/battery_gpt54.json` (GPT-5.4). Concrete example pair available: same held-out window, two question stems side-by-side. This is a writing task rather than an answer — the data exists. Plan: pull one pair, add as illustration in §3.4.1.
- **Reference:** `results/global_*/battery_v2.json` vs `battery_gpt54.json`; edit plan F-§3.4.1 row.

---

## §3.5 Experimental Conditions

### Q17. "Why not include this in the memory system conditions table?" (native ingestion variant)

- **Anchor:** "Native ingestion variant" paragraph.
- **Answer:** Editorial — yes, should be in the conditions table. v9 plan B7 adds columns for (a) controlled vs native, (b) Mem0 vs Mem0+Spec explicit pairing. This absorbs the currently-separate paragraph.
- **Reference:** edit plan B7.

### Q18. "Did it see wrong spec for the subject, and that's why it said this is the wrong specification? How do we control for that? Or are we just feeding them the spec?"

- **Anchor:** prompt block showing `C2c` variable in §3.6.
- **Answer:** The model is given the wrong spec **as the user's spec** — the system prompt always says "The following is a behavioral specification describing your user" and then injects either the correct (C2a) or wrong (C2c) spec. The wrong spec is **anonymized** (`spec_production.md` uses "they" / "this person", no subject name), so the model cannot trivially know which person the served spec is about. However, the battery question **does name the target subject** explicitly (e.g., "How would Ebers characterize..."). This asymmetry is the mechanism: the model compares the named target to the anonymized interpretive content and flags the mismatch. Code: `scripts/run_global_rerun.py:850-872` (`build_system_prompt`) + `scripts/run_global_rerun.py:283-286` (`load_spec` loads anonymized `spec_production.md`).
- **Reference:** `scripts/run_global_rerun.py:850-872` + `:283-286`; v8 §3.3 anonymization; v8 §4.3 "detection asymmetry" paragraph.

---

## §3.6 Response Models

### Q19. "Is this fair to say, one could say a more capable model would be able to infer better from facts alone?" (re: Haiku as conservative primary)

- **Anchor:** "an effect that registers on a weaker model is a more conservative claim than one that only surfaces on a frontier model."
- **Answer:** Aarik's objection has merit — a more capable model *could* infer more from facts alone, in which case the spec delta on a weaker model would be an over-estimate. §4.5.1 Tier 2 replication addresses this: Sonnet 4.6 and Gemini 2.5 Pro on 3 subjects (Ebers, Yung Wing, Zitkala-Sa) reproduce the spec direction in 5 of 6 cells. So the spec effect is not Haiku-specific. Plan: add acknowledgment of the counter-reading in §3.6 with forward pointer to §4.5.1.
- **Reference:** v8 §4.5.1; `docs/research/tier2_recompute_s114.json`; edit plan F-§3.6 row.

### Q20. "Is this prompt fair, should it not just be the straight up question?"

- **Anchor:** response-model prompt: "You are predicting how <subject> would respond..."
- **Answer:** The prompt is constant across all 5 conditions (C5/C2a/C2c/C4/C4a), so it cannot bias the comparison between conditions. It does set a "predict-in-voice" frame, which is intentional: the rubric scores prediction of subject behavior, not a generic answer. A "straight-up question" prompt would change what the rubric is measuring. Plan (F-§3.6): add a short justification paragraph explaining this.
- **Reference:** `scripts/run_global_rerun.py:977-990`; edit plan F-§3.6 prompt-justification row.

### Q21. "Was it sonnet or haiku, this may be incorrect information?" (main-study battery generator)

- **Anchor:** §4.5 opening "most main-study batteries were generated by Claude Sonnet."
- **Answer:** **Haiku**, not Sonnet. The main-study batteries were generated by `claude-haiku-4-5-20251001` via `scripts/run_global_subjects.py` — confirmed at lines 75, 120, 159, 268 of that script. The §4.5 sentence is factually incorrect. This is P0-3 in the edit plan, flagged as critical factual correction. Fix: "most main-study batteries were generated by Claude Haiku 4.5."
- **Reference:** `scripts/run_global_subjects.py:75,120,159,268`; edit plan P0-3.

---

## §3.7.2 Calibration

### Q22. "Confused here, Opus and Sonnet enter on the panel for inter-judge agreement, but our primary aggregate is 5-judge non-Gemini panel?"

- **Anchor:** "Five judges (Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) were tested against four diagnostic inputs... Sonnet and Opus are not on the diagnostic suite; they enter the panel on inter-judge agreement properties only."
- **Answer:** Two different "5-judge" sets are being referenced. (a) **Diagnostic calibration suite** (pre-study): 5 judges tested = Haiku, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro. Sonnet and Opus were not in this diagnostic. (b) **Primary aggregate panel for scoring**: 5 non-Gemini judges = Haiku, Sonnet, Opus, GPT-4o, GPT-5.4. These are different sets. Plan (edit plan F-§3.7.2): rewrite the paragraph explicitly distinguishing the two sets. Sonnet/Opus enter the scoring panel via inter-judge agreement (Spearman ρ = 0.89-0.98 with the calibrated core), not via diagnostic pass.
- **Reference:** v8 §3.7.2 + §3.7.4 inter-judge agreement; edit plan F-§3.7.2.

### Q23. "Unclear what these conditions are, need to provide condition title or something." (re: C2a, 5-judge vs 7-judge)

- **Anchor:** "C2a's mean Δ vs. C5 rises from +0.35 on the 5-judge primary panel to +0.45 on the 7-judge."
- **Answer:** C2a = Behavioral Specification alone, no facts. C5 = no-context baseline. The delta shift (5-judge +0.35 → 7-judge +0.45) reflects Gemini's relatively severe scoring of baseline responses compared to spec-containing responses, which widens the delta when Gemini judges are included. This is covered by sweep A2 (gloss C-codes on every use) and the sentence stays numerically correct; plan is to add the gloss.
- **Reference:** v8 §3.7.2 + §4.5.2; edit plan A2.

---

## §3.7.6 Rubric-handling limitations

### Q24. "This sounds like a floor calibration." (mean abstention score = 1.27)

- **Anchor:** "The mean abstention score is 1.27."
- **Answer:** Yes — this is essentially a floor-leakage observation. When a response is an epistemically-honest refusal (the retrieved facts do not support a prediction), the rubric has no neutral slot and the judges place the response at 1.27, just above the rubric floor of 1.0 ("refuses or off-base"). The subsequent floor-testing diagnostic (P0-17, `docs/research/judge_floor_test.md`) confirmed the pattern: wrong-answer variants score mean 2.12 across judges, and the `plausible_unsupported` variant scores 2.75 — judges systematically fail to cleanly place epistemic abstention at the floor. P0-16 rubric-sensitivity analysis recodes refusals as neutral to see what happens to Δ_spec; report at `docs/research/rubric_sensitivity_refusals.md`.
- **Reference:** v8 §3.7.6; `docs/research/judge_floor_test.md`; `docs/research/rubric_sensitivity_refusals.md`; edit plan P0-16, P0-17.

---

## §4.1 The Cross-Subject Gradient

### Q25. "This may be more interesting if just facts are provided vs specification + facts? Or a particular low memory system score vs with specification?" (re: Example A anchor)

- **Anchor:** "With specification + facts (C4a, 5-judge mean 3.60)."
- **Answer:** The facts-alone condition is C4 (`C4_factdump` in `run_global_rerun.py:862-864`). On the 9 low-baseline subjects, mean C4 = 2.35 vs mean C4a = 2.45 — so facts+spec outperforms facts alone by 0.10 points on average, smaller than the spec-alone effect (C2a = 2.23 vs C5 = 1.52, Δ = 0.71). The example in §4.1 uses the C4a condition for a larger effect; expanding with C4-alone and memory-system C1/C3 rows is a reasonable presentation improvement. Plan (F-§4.1 Example A): expand with intermediate rows.
- **Reference:** v8 §4.2 conditions summary; `scripts/run_global_rerun.py:862-864`; edit plan F-§4.1 Example A row.

---

## §4.1.2 Living-user replication (author)

### Q26. "Should likely test with another spec that is verifiable different from mine. Random derangement perhaps?"

- **Anchor:** "Wrong-spec control reads through, and the gap partitions cleanly."
- **Answer:** **Needs-decision (blocker).** The current living-user wrong-spec test only uses Franklin's spec, and Franklin's spec overlaps the author's by 5 of 12 anchors (content-overlap confound). P0-6 in the edit plan is the derangement rerun: run author's battery with one of the 13 global subjects' specs selected by random derangement. P0-6 has been **upgraded to Tier 0** because Gemini Pro and Mistral both flagged this as a critical integrity risk for H6 ("none of 40 responses got worse"). Cost: ~$5, ~20 min compute + ~20 min judge. Not yet run. Until it runs, H6 must be framed as a pilot (n=1) finding, not a universal claim.
- **Reference:** edit plan P0-6 + C3; `memory/project_paper_redline_notes.md` H6 guarding plan.

---

## §4.2 Compression: Structure vs. Raw Text

### Q27. "This is pretty big... needs to be more clear, in terms of raw corpus is usually 10x larger... not sure how to frame this." (re: facts+spec = raw corpus 2.45)

- **Anchor:** "Adding facts to the specification (C4a) produces the same mean as raw corpus alone (both 2.45). Two different compression strategies, same performance, different context shapes."
- **Answer:** Framing: "At identical prediction scores (2.45 mean on the 1-5 rubric), the Facts + Specification package is ~7,000 tokens and the raw corpus is 80,000-400,000 tokens — a 10x to 55x compression ratio at equal predictive value." Per-subject corpus sizes are in `results/global_<subject>/facts.json` (or `training.txt`). Babur: 222K words ≈ 80K tokens. Hamerton: 25K words ≈ 34K tokens. Plan: surface the token-ratio inline as part of H4 headline framing.
- **Reference:** v8 §4.2; edit plan H4 + F-§4.2.

---

## §4.2.1 Question-Improvement Rate

### Q28. "Maybe a segmented bar chart would make this easier to understand?" (spec-vs-corpus on 36.9%)

- **Anchor:** "the 7K-token facts + spec package outscores the much larger corpus + spec package on 36.9% of questions."
- **Answer:** Editorial / figure design. Plan: add a segmented bar chart per v9 Figure 4.2.1 rework (D). The data is in `docs/research/engagement_conditional_delta.md` and `docs/research/engagement_conditional_delta.json`.
- **Reference:** `docs/research/engagement_conditional_delta.md`; edit plan D Figure 4.2.1.

### Q29. "Can we counter any of these failure modes now?" (re: failure modes if rate metric adopted)

- **Anchor:** "Failure modes if this metric is adopted."
- **Answer:** Yes — some have been addressed. (1) Tiny-gain inflation: guard is median magnitude (reported as Δ = +1.0 for low-baseline spec, not near-zero). (2) Baseline dependency: measured C5 per subject and reported the gradient. (3) Judge bias: 5-judge primary panel + 7-judge sensitivity (§4.5.2). (4) Anchor-crossing: §4.1 adds the multi-anchor crossing analysis (P0-10). What's still open: question-category distribution effects (P0-15 question-category audit).
- **Reference:** v8 §4.2.1 tiny-gain-inflation paragraph; edit plan P0-10, P0-15, F-§4.2.1 failure-modes row.

---

## §4.3 Mechanism: Content, Not Format

### Q30. "How, what was it detecting, from the question?, did the prompt have something about it?" (re: "detected the mismatch")

- **Anchor:** "The model detected the mismatch between the named target in the question (Ebers...) and the interpretive content of the anonymized specification..."
- **Answer:** The mechanism is the detection asymmetry described in v8 §4.3: the battery question explicitly names the target (e.g., "How would Ebers characterize..."), but the served spec is anonymized (uses "they" / "this person"). The model is comparing (a) the named target it "knows" from pretraining with (b) the interpretive content of the anonymized spec, and concluding they describe different people. The prompt does **not** tell the model the spec is wrong — the model infers the mismatch from content. Evidence: 60.6% of 587 wrong-spec responses explicitly flag the mismatch (see §1.3 quote "This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur"). Full classifier at `scripts/classify_wrong_spec_detection.py` and data at `docs/research/wrong_spec_detection_analysis.md`.
- **Reference:** `docs/research/wrong_spec_detection_analysis.md`; `scripts/classify_wrong_spec_detection.py`; v8 §4.3 detection-asymmetry paragraph.

### Q31. "Any analysis we can do on the cases where it tried to apply it, and where it didn't, were the questions similar in some kind of way, asking for a specific kind of inference. Could we identify the model failure modes based on the questions?"

- **Anchor:** "36.5% attempted to apply the mismatched content and produced a low-quality prediction."
- **Answer:** **Partially.** P0-5 refusal audit (`docs/research/spec_refusal_audit.md`) classified 81 spec-induced refusals across 5 substrates into (a) EPISTEMIC_HONEST (6/81, 7.4%), (b) SPEC_AXIOM_TRIGGER (41/81, 50.6%), (c) RUBRIC_ARTIFACT (24/81, 29.6%), (d) SCORED_AS_WRONG_PRED (10/81, 12.3%). The question-category cross-tab (P0-8 / P0-15) is pending: classify each question as literal-recall / interpretive-inference / refusal-triggering and cross-tab with the refusal categories. `docs/research/question_category_audit.md` carries initial classifications. The "applied mismatched content" subgroup (36.5% of 587) has not yet been cross-tabbed with question category — that is P0-8 work, flagged but not completed.
- **Reference:** `docs/research/spec_refusal_audit.md`; `docs/research/question_category_audit.md`; edit plan P0-5, P0-8, P0-15.

### Q32. "Would reveal something interesting about if there were particular subjects who did better overall... May be certain autobiographies do better? Maybe more modern ones vs old ones?" (Figure 7 cross-slice)

- **Anchor:** Figure 7 caption.
- **Answer:** **Answer not fully available in current data.** Per-system spec-delta × subject is tabulated in `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md` and `docs/research/supermemory_c1_vs_c3_paired_analysis.md`. A cross-slice analysis by subject era / modernity / "craziness" was not done. The gradient analysis in §4.1 shows that baseline (proxy for pretraining coverage) is the main effect driver — not era per se — but modern-vs-ancient and complexity subcategorizations are a follow-up. Flagged for §8 Future Work.
- **Reference:** `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`; `docs/research/supermemory_c1_vs_c3_paired_analysis.md`; edit plan D Figure 7 cross-slice row.

---

## §4.4 Memory-System Composition

### Q33. "Why not significant?" (Wilcoxon on Mem0, Supermemory, Base Layer substrate)

- **Anchor:** "Mem0, Supermemory, and Base Layer substrate controlled are not significant at α = 0.05."
- **Answer:** Three contributing factors. (1) **Small n**: Wilcoxon signed-rank on 9 low-baseline subjects — low statistical power. (2) **Small effect size**: Mem0 controlled spec Δ ≈ +0.05, Base Layer ≈ +0.08, Supermemory ≈ +0.004 (vs Zep +0.17 and Letta +0.17 which are significant). (3) **High variance across subjects**: some subjects show strong positive deltas, others slightly negative, widening the distribution. The test is under-powered at n=9 for effect sizes below ~0.15. Direction is still positive on Mem0 and Base Layer. Plan (F-§4.4): add a 1-sentence explanation: "underpowered at n=9 for sub-0.15 effects; direction is positive but not statistically significant at α=0.05."
- **Reference:** v8 §4.4 Wilcoxon table; edit plan F-§4.4 Wilcoxon row.

### Q34. "Interesting if the spec doesn't help meaningfully, it doesn't really hurt either?" (re: Supermemory −0.03)

- **Anchor:** "−0.03."
- **Answer:** Yes — the aggregate is near-zero but the per-question distribution is bimodal: 52 spec-regressions (magnitude −1.41 avg) and 37 spec-improvements (magnitude +1.45 avg). The mean cancels because the two sides are roughly symmetric in magnitude but slightly tilted toward regressions in count. So at the subject-average level, Supermemory's spec behavior is neither helpful nor harmful — but at the per-question level, it's both, in nearly equal measure. Plan (F-§4.4): surface this observation in prose rather than hide in a number.
- **Reference:** v8 §4.4 Supermemory subsection; `docs/research/supermemory_c1_vs_c3_paired_analysis.md`; edit plan F-§4.4 "−0.03" row.

### Q35. "We have the paid tier now, did we not run these?, should run these if now. Otherwise we shouldn't be mentioning this. Run ASAP."

- **Anchor:** "Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau)."
- **Answer:** **Run.** P0-2 paid-tier rerun completed 2026-04-23. All 4 subjects completed ingest + retrieve + generate successfully: 199/199 chunks, 4.3-5.0 facts per question, 156/156 responses, 0 errors. Data at `memory_system/data/experiments/memory_systems/results/global_<subject>/supermemory_fullpipeline_*.json`. **Judging not yet run** (pending greenlight per the report). The paper footnote is out of date: native n should update from 10 → 14, but only after judging runs. Report: `docs/research/p0_2_supermemory_paid_tier_rerun.md`.
- **Reference:** `docs/research/p0_2_supermemory_paid_tier_rerun.md`; edit plan P0-2, C2.

### Q36. "May be due to zeps architecture, because it's using mathematical edges instead of just straight semantics or vectors???" (re: Zep clean positive case)

- **Anchor:** "Zep's temporal-graph retrieval and the Behavioral Specification layer without interference."
- **Answer:** Plausible hypothesis consistent with the Zep architecture description in §2.1 (bi-temporal knowledge graph built on Graphiti: episodes → entities → facts as triplets with temporal validity windows). Zep retrieves via graph traversal + temporal scoping, so it returns fewer but more topically coherent facts, and the spec layers on top without interfering with retrieval coverage. In contrast, Mem0's atomic-fact retrieval returns denser, more redundant fact sets that the spec has less room to reinterpret. **This is hypothesis, not tested.** Plan (F-§4.4 Zep): add 1-paragraph hypothesis labeled as such.
- **Reference:** v8 §2.1 Zep description; edit plan F-§4.4 Zep row.

### Q37. "Wefocus on super memory a bit too much... Does this make sense?" (re: Supermemory own heading vs subsection of §4.4)

- **Anchor:** "Supermemory: what the near-zero aggregate actually means" heading.
- **Answer:** Yes, structural. v9 plan B1 folds Supermemory out of its own top-level heading into §4.4.2 as a subsection. This is consistent with Aarik's original annotation.
- **Reference:** edit plan B1.

---

## §4.4.x Supermemory subsection

### Q38. "This reads like it was trained on the entire corpus, can you confirm please?" (Fukuzawa Q26)

- **Anchor:** "Applies P3 (Conformity Surface / Conviction Interior)... refuse to perform moral disapproval."
- **Answer:** **Not trained on entire corpus.** `scripts/run_option_b.py:78-83` (`load_training_text`) loads `results/global_<subject>/training.txt`, which is the training half of the corpus only. Held-out passages are in `heldout.txt` and are NOT ingested into Supermemory. For Fukuzawa: `results/global_fukuzawa/supermemory_fullpipeline_ingestion.json` shows `chunks_expected: 25, post_success: 19, post_failure: 6, container_tag: fukuzawa_fullpipeline` — 19 of 25 training-corpus chunks successfully ingested, and the retrieval returns facts from this training half only. The impressive answer on Q26 reflects Supermemory retrieval surfacing the right training facts, and the spec supplying the interpretive bridge; it is not corpus leakage from the held-out passage.
- **Reference:** `scripts/run_option_b.py:78-83`; `memory_system/data/experiments/memory_systems/results/global_fukuzawa/supermemory_fullpipeline_ingestion.json`.

---

## §4.5 Robustness and Sensitivity

### Q39. "Biases that favor response quoting behavioral specifications? That's a mouthful and a strange claim."

- **Anchor:** "biases that favor responses quoting behavioral-specification tag IDs."
- **Answer:** Editorial rewrite, not a question about data. The concern being expressed: if LLM judges as a class reward responses that look structured / labeled / theory-driven, and spec-containing responses are structured / labeled / theory-driven by construction, then the measured spec effect could be partly an artifact of judge preference for that style. Plan (F-§4.5.3): rewrite in plain English.
- **Reference:** v8 §4.5.3; edit plan F-§4.5.3 row.

---

## §4.6 Interpretation vs. Recall

### Q40. "Would we be able to show per subject somehow. Couldn't we just show w/o spec w/spec delta per memory system per subject? Could do % of small wins/losses vs large win/losses. Again shouldn't this be based on moving across an anchor number as well?"

- **Anchor:** "Per-subject paired-delta distributions: every row is a mixture of wins and losses."
- **Answer:** Yes — data exists for the subject × memory-system Δ heatmap. Per-subject C1 vs C3 paired deltas are in `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`, `docs/research/supermemory_c1_vs_c3_paired_analysis.md`, and `docs/research/baselayer_c1_vs_c3_paired_analysis.md`. Plan (edit plan D new heatmap): add a subject × memory-system Δ heatmap figure. Anchor-crossing classification exists at `docs/research/s114_anchor_crossing_examples.json` but not yet cross-tabbed with per-system.
- **Reference:** `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`; `docs/research/supermemory_c1_vs_c3_paired_analysis.md`; `docs/research/baselayer_c1_vs_c3_paired_analysis.md`; edit plan D new heatmap row.

### Q41. "Feel like this should be in 4.4 primarily. Should interpretation vs recall be discussed as a 4.4 subsection, unclear why robustness and sensitivity comes before this?"

- **Anchor:** "4.6 Interpretation vs. Recall" heading.
- **Answer:** **Needs-decision (structural).** The v9 plan B1 adopts the fold: §4.6 body becomes §4.4.3 "Cross-substrate pattern reproduction" and §4.4.4 "Keckley Q21: cross-substrate refusal", and §4.5 Robustness moves to the end of Results. Consensus from cross-LLM review: Mistral agreed, Cerebras objected (causal-logic grounds), overridden because Aarik's annotation is explicit. Ready to execute unless Aarik wants to reconsider.
- **Reference:** edit plan B1.

---

## §4.7 Architectural Convergence: Letta Stateful-Agent

### Q42. "Unified brief? It should be the complete behavioral spec no?, why didn't we do the full layered stack, why would we use something different from the rest of the study? Can we rerun this potentially?" (MAJOR flag)

- **Anchor:** "BL unified brief" and "full-stack specification at 34,000-40,000" in §4.7.
- **Answer:** **Backcheck resolved — no rerun required.** Verification of `scripts/run_global_rerun.py:283-285` (`load_spec`): all §4.1 main-study conditions load `data/global_subjects/<subject>/spec_production.md`, which is the full 4-layer (anchors + core + predictions + brief) ~35-40K-char artifact. The v8 §4.1 gradient, §4.3 mechanism, §4.4 memory-system composition, and the compression story are all already on the full-stack spec. The "BL unified brief" label in §4.7 describes a distinct compressed variant used only for that matched-battery Letta comparison — `scripts/run_option_b.py:99-129` loads the 3 layers from `data/hamerton/spec/` plus the unified brief as a separate block; for Hamerton specifically the "UNIFIED BRIEF" section is `brief_v5_clean.md`. The global-subject §4.7 comparison uses `spec_production.md` (full stack). v8 §4.7 numbers and labels are correct as published. P0-1 in the edit plan is marked RESOLVED 2026-04-23. **Note on asymmetry:** the §4.7 matched-battery rerun on Ebers and Babur did use a compressed named-spec variant (`results/global_<subject>/spec.md`, 6-7K chars), which is different from the 35-40K-char `spec_production.md` used in §4.1. So there IS a size mismatch in §4.7 vs §4.1, but Aarik's specific concern (that §4.1 numbers were from a unified brief only) is incorrect — §4.1 used the full stack.
- **Reference:** `scripts/run_global_rerun.py:283-285`; `scripts/run_option_b.py:99-129`; `docs/research/letta_stateful_matched_rerun.md`; edit plan P0-1.

### Q43. "Suddenly seen the uptick of usage of this particular word starting in section 4, why?" (re: "substrate")

- **Anchor:** "substrate" (used multiple times in §4.4, §4.6).
- **Answer:** Not a data question — word-choice. "Substrate" was introduced mid-writing as shorthand for "memory system + retrieval stack underneath the spec" (Mem0, Letta, Supermemory, Zep, Base Layer's own MiniLM+ChromaDB floor) without it implying any one is a finished product. Plan (A5): pick one term globally — most likely "memory system" — and apply. Keep "substrate" only where it specifically refers to the retrieval stack (Base Layer substrate = MiniLM + ChromaDB) and distinguish from the "memory system + spec" layered product.
- **Reference:** edit plan A5.

---

## §5 Discussion

### Q44. "This is the first it's mentioned here never before?" (re: "how do we improve human-AI interactions...")

- **Anchor:** §5.1 opening sentence.
- **Answer:** Yes — in v8, this framing appears for the first time at the top of §5.1. Plan (F-§5.1): either (a) weave it through §1-§4 so §5.1 is not introducing new framing, or (b) open §5 with this question explicitly as the unifying thread.
- **Reference:** edit plan F-§5.1 row.

### Q45. "Generally it seems this section should be in 2, unless im missing what a discussion section is suppose to do?" (re: §5.2 recall/prediction/persona)

- **Anchor:** §5.2 heading.
- **Answer:** **Needs-decision (structural).** v9 plan B3 adopts the move: benchmark-family comparisons from §5.2-§5.4 migrate to §2. Discussion rebuilds around the anti-pattern definition (B10) and open questions (preamble to §8). Consensus: Mistral agreed, Cerebras objected on framing grounds, overridden because Aarik's annotation is explicit.
- **Reference:** edit plan B3, B10.

### Q46. "Maybe for discussion the discussion should be what exactly is a behavioral specification trying to measure? And what is it not? Instead of a reference the current pattern, define the anti-pattern that is the spec." (re: §5 purpose)

- **Anchor:** §5.2 heading, second comment.
- **Answer:** **Needs-decision (structural).** Yes, this reshapes §5 around the anti-pattern definition. Plan B10: new §5.1 "The Anti-Pattern: What Behavioral Specification Is Not" — explicitly define: not recall, not persona fidelity, not preference alignment, not survey-response prediction. Content currently in §5.2-§5.4 about benchmark comparisons moves to §2. Opens a new §5 architecture: (1) anti-pattern, (2) findings extension / open questions, (3) preamble to §8.
- **Reference:** edit plan B10.

---

## Items flagged as "ANSWER NOT AVAILABLE IN CURRENT DATA"

### Q47. "This is interesting specifically because I should not do it. Is this is a failure, is it a 1, because if you are working of of epistemic integrity as a reward dimension, this is exactly what we want. This is a HEADLINE finding potentially. Should likely do a full analysis on spec based answer refusals. Were we asking the model to do something morally reprehensible?" (Zitkala-Sa Q18)

- **Anchor:** "generating new first-person testimony as her crosses into ventriloquism... I should not do it."
- **Partial answer:** P0-5 spec-refusal audit (`docs/research/spec_refusal_audit.md`) classified 81 spec-induced refusals into EPISTEMIC_HONEST (6), SPEC_AXIOM_TRIGGER (41), RUBRIC_ARTIFACT (24), SCORED_AS_WRONG_PRED (10). The Zitkala-Sa Q18 case (ventriloquism refusal) falls in SPEC_AXIOM_TRIGGER or RUBRIC_ARTIFACT depending on classification — the rubric scored it 1.0 but the spec's dignity axiom triggered the refusal. Whether this is "morally reprehensible to ask" is a substantive claim that requires a separate human review of the 81 refusal-triggering questions. **Not yet done.** Plan (edit plan P0-5 expansion): link to §7 and add the "were we asking something morally reprehensible" review as §7 content.
- **What would be needed:** Human review of the 81 spec-induced-refusal questions + held-out passages to classify morally-loaded framings.
- **Reference:** `docs/research/spec_refusal_audit.md` (Zitkala-Sa Q18 is example in Supermemory section); edit plan P0-5 expansion.

### Q48. "It seems discussion is just reiterating findings, would really like discussion to be an extension. Given xyz findings, this is what interesting, this is what we want to explore around this, this is what questions it brings up. Almost like a preamble for future work imo." (re: §5.4)

- **Anchor:** §5.4 "Content specificity and mechanism" heading.
- **Answer:** Editorial / design direction — acknowledges §5 should be rebuilt around forward-looking open questions. This is covered by edit plan B3 + B10 (§5 rebuild). Concrete open questions that should be extensions in v9 §5 include: (a) why some questions route into Pattern 1/2/3 (P0-8 / P0-15), (b) spec-similarity cross-subject effects (P0-7), (c) serving-layer stability over time, (d) canonical-life-events handling, (e) refusal-behavior as explicit epistemic-integrity signal, (f) scaling laws (§4.8 content). All flagged in §8 and the v9 edit plan.
- **Reference:** edit plan B3, B10; v8 §8 Future Work.

---

## Related editorial-only flags (not questions, not scored here)

These items look like questions but are editorial suggestions or self-talk — tracked in `s114_v9_edit_plan.md`, not answered here:

- "Confusing when bringing up median magnitudes specifically" — editorial (rewrite request).
- "Needs to be more layman" — sweep A1.
- "Most strongly on which slice? can likely cut this" — cut request, not a question.
- "How much source text... layman comparison" — editorial comparison request.
- "Would appreciate example of this" (multiple) — all editorial.
- "Can you confirm please" on "trained on entire corpus" — this IS a question (answered as Q38 above).
- "Is this necessary, maybe move..." — editorial location question.
- "Is this fair to say" — reflective, answered as Q19.
- Many "should X be a table / figure / section" items — all editorial, routed to Parts B/D of the edit plan.

End of digest.
