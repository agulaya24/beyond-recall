# Beyond Recall — Structural Review Guide

Use this alongside the Word doc. Each section has: what it does, what to evaluate, what to ignore for now.

---

## Abstract (lines 9-30)
**Function:** The pitch. Reader decides in 90 seconds whether to keep reading. Must convey: problem (recall isn't enough), method (behavioral specification), result (works for unknown subjects, doesn't for known), implication (missing primitive).

**Your note:** You said this feels like the Introduction. That instinct is right — the Abstract IS doing double duty. For ArXiv, that's acceptable (no page limit, readers skim). But the thesis ("behavioral specification is the missing primitive") currently lands in paragraph 3. Consider: should sentence 2-3 just say it?

**Evaluate:** Does this make someone want to read the paper? Does it overstate? The 5 numbered findings at the end — are they the right 5, in the right order?

**Leave alone for now:** Exact percentages (will change after rerun).

---

## 1. Introduction (lines 40-62)
**Function:** Frame the problem. Not "here's what we did" but "here's why the current approach fails." The retrieval disagreement finding (68% zero overlap) is the hook — it shows the problem is structural, not incremental.

**Subsections:**
- **1.1 What We Mean by Alignment** — Distinguishes "behavioral alignment" from AI safety alignment. Necessary disambiguation.
- **1.2 What the Specification Captures** — The knowledge distillation analogy. Compression preserves signal, discards noise.

**Evaluate:** Does the Introduction make the reader feel the problem before hearing the solution? Is the retrieval disagreement finding compelling enough as the opening move? Does it flow from problem → gap → our approach?

---

## 2. Related Work (lines 64-80)
**Function:** Position the paper. Who else is working on this, and why their approach is insufficient. Currently covers: memory systems (Mem0/Letta/etc.), retrieval augmentation, knowledge distillation, user modeling.

**Evaluate:** Is anything missing? The reviewers flagged overlap with "cognitive schema" (Bartlett) and "internal model" (cognitive science). Does this section make clear what's NEW about behavioral specification vs. existing approaches? References — are they real? (We fixed 9 in the provenance audit, but verify any that look suspicious.)

---

## 3. Study Design (lines 82-308)
**Function:** The methodology. This is where reviewers will attack hardest. Must be airtight.

**Subsections (in order):**
- **3.1 Subjects** — 14 subjects, 11 cultures, why these. Gender ratio (4F:10M) acknowledged as limitation.
- **3.2 Corpus Split** — 50/50 training/held-out. Why 50/50.
- **3.3 Pipeline Overview** — The 5-step pipeline. Extract → Author → Compose. This is the core technical contribution.
  - **3.3.1 Extraction** — 47 predicates, Haiku, fact counts. The constrained vocabulary is load-bearing.
  - **3.3.2 Authoring** — Three layers (anchors, core, predictions). Sonnet. Blind generation.
  - **3.3.3 Composition** — Unified brief. Opus. Anti-cataloging.
  - **3.3.4 Serving** — MCP integration. How the spec gets used.
  - **3.3.5 Traceability** — Every claim traceable to source facts.
- **3.4 Question Battery** — 80 questions per subject, generated backward from held-out text.
- **3.5 Experimental Conditions** — The 15 conditions. This is the experiment design.
- **3.6 Response Models** — 6 models across 3 providers.
- **3.7 Evaluation: LLM-as-Judge with Calibration** — 7 judges, calibration framework.

**Evaluate:** Is the pipeline explanation clear enough that someone could replicate it? Are the conditions well-motivated — does each one test a specific hypothesis? The question battery section — reviewers flagged circularity (same model generates battery and spec). Does the text address this?

**This is the longest section.** Read for clarity and logic, not prose quality. If something is confusing, flag it — confusion here means a reviewer will attack it.

---

## 4. Results (lines 310-424)
**Function:** What happened. Numbers, tables, findings. No interpretation yet (that's Discussion).

**Subsections:**
- **4.1 Primary Subject: Hamerton** — The deep dive. Full-stack spec results. This is where Cohen's d appears.
- **4.2 The Compression Story** — 5K tokens outperforms 33K tokens. The headline finding.
- **4.3 The Known-Figure Test (Franklin)** — Context hurts for known subjects. The negative result that strengthens the paper.
- **4.4 The Global Gradient** — N=14 table. The breadth finding. **NUMBERS WILL CHANGE** after the rerun currently running.
- **4.5 Pretraining Representation Bias** — Why the gradient exists.
- **4.6 Judge Calibration** — The calibration framework results.

**Evaluate:** Are the results presented honestly? Does each subsection have a clear finding, or is it just data? The Franklin result is the most interesting to a skeptic — does it get enough space? Table 4.4 (gradient) — is it readable? Does the ordering make sense?

**Flag but don't fix:** Any number you question — we'll update all numbers after the rerun.

---

## 5. Discussion (lines 426-501)
**Function:** What it means. This is where YOUR voice matters most. The Discussion is where the paper goes from "here's data" to "here's what this changes."

**Subsections:**
- **5.1 The Specification Is a Tool for the Unknown** — Core thesis. The spec matters when the model doesn't already know.
- **5.2 Frontier Models Already Do This for Famous People** — The Franklin finding inverted: pretraining IS a behavioral specification.
- **5.3 Facts Do Not Carry Their Own Significance. People Do.** — The framing you care about most. Facts + spec > spec alone > facts alone.
- **5.4 The Specification Is a Multiplier, Not a Substitute** — Positioning against "replace memory with spec."
- **5.5 When to Use a Specification (and When Not To) — The Hedging Problem** — Hedging metric. Spec reduces hedging from 51% to 31%.
- **5.6 Scope and Open Questions** — What we don't know yet.
- **5.7 Ethical Considerations** — Privacy, consent, manipulation risk.

**Evaluate:** This is where you should be hardest. Does each subsection earn its space? Is the framing YOUR framing or generic academic framing? "Facts do not carry their own significance" is your core insight — does the section do it justice, or does it read like a summary? The hedging analysis (5.5) — is this compelling or does it feel tacked on?

---

## 6. Limitations (lines 503-516)
**Function:** Honest accounting of what the study can't claim.

**Evaluate:** Are the limitations real or defensive? Reviewers flagged: no human evaluation, historical texts != real users, LLM-judging-LLM circularity. Are these addressed directly and honestly, or hedged?

---

## 7. Future Work (lines 518-530)
**Function:** What comes next. Should feel like a research agenda, not a to-do list.

**Evaluate:** Does this excite you? Would a reviewer read this and think "I want to see that study"? The SCOTUS study, the temporal prediction study, live human subjects — are these the right next steps?

---

## 8. Conclusion (lines 532-546)
**Function:** 3-5 sentences that a reader remembers. The takeaway.

**Evaluate:** If someone only reads the Abstract and the Conclusion, do they get the paper? Is the last sentence something you'd say out loud?

---

## Appendices (A-F)
- **A:** Example spec (Hamerton). Skim for quality.
- **B:** Qualitative examples. Do these land?
- **C:** Score calculation. Technical reference.
- **D:** Figure specs. NOT YET PRODUCED — just descriptions.
- **E:** Provider issues. Reference.
- **F:** Agent navigation + reproducibility.

---

## How to Review

1. **First pass: Read the Abstract and Conclusion only.** Do they tell the same story? Is the Conclusion stronger or weaker than the Abstract?

2. **Second pass: Read linearly, flag reactions.** Use Word comments. Mark anything that:
   - Confused you
   - Felt like it overstated
   - Felt like it understated (you know it's stronger than this)
   - Bored you (section too long, point already made)
   - Made you want to argue back

3. **Third pass: Voice.** Read sentences out loud. Mark anything you wouldn't say. Mark anything that sounds like a different person wrote it.

4. **Don't fix prose.** Flag it. We'll fix together.

---

## What the reviewers attacked (for context)
Three free-model reviews came back. Common themes:
- No human evaluation (all 3 flagged)
- Percentage calculations misleading (Cerebras)
- Historical texts != real users (Mistral)
- Question battery circularity (Mistral)
- No aggregate statistical test like Wilcoxon (Cerebras)
- No spec component ablation (all 3)
- "Prediction" vs "post-hoc pattern matching" (Mistral)

You don't need to address these in your review. But knowing what they flagged might sharpen your eye.
