# §4.1 V1/V2 Battery Alignment Audit — beyond_recall_v11_9_draft.md

**Date:** 2026-05-08
**Scope:** Three worked examples in §4.1 of `docs/beyond_recall_v11_9_draft.md` (Example A: Fukuzawa Q35; Example B: Bernal Díaz Q16; Example C: Seacole Q2).
**Method:** Each example's quoted text (question, held-out, C4 excerpt, C4a excerpt, cited score) compared verbatim against the V2 canonical cell extracted by `scripts/v2_canonical_cell_extractor_20260508.py`. The cited primary means in the paper are cross-condition figures from `judgments_v2.json` (5-judge primary panel mean), so V2 is the load-bearing source for any text the score is supposed to be about.

---

## Per-example verdict summary

| Example | Subject / qid | Verdict | Structural mismatches |
|---|---|---|---:|
| A | Fukuzawa Q35 | **MISALIGNED — STRUCTURAL** | 4 |
| B | Bernal Díaz Q16 | **ALIGNED with COSMETIC drift** | 0 |
| C | Seacole Q2 | **ALIGNED** | 0 |

**Total structural mismatches: 4 (all in Example A).**

---

## Example A. Fukuzawa Q35 — STRUCTURAL MISALIGNMENT

The paper's Example A pulls the **V1 battery** (`battery.json`) question text, held-out, and response excerpts, but cites the **V2 cached primary mean** scores (1.00 and 4.20) from `judgments_v2.json`. Those scores judged V2 responses to a different V2 Q35 question. The example as printed is internally incoherent: the quoted text and the cited score do not refer to the same prediction.

### Field-by-field

**1. Question text — STRUCTURAL**
- Paper: *"Would Fukuzawa's reasoning for keeping students from war be based on moral principle or practical concern?"*
- V2 canonical (Q35): *"How would Fukuzawa characterize someone who studied naval arts under the Dutch and later became instrumental in preventing military conflict?"*
- V1 (`battery.json` id 35): *"Would Fukuzawa's reasoning for keeping students from war be based on moral principle or practical concern?"* — exact match.
- **Source of paper text: V1 battery, not V2.**

**2. Held-out passage — STRUCTURAL**
- Paper: *"For this kind of war, if they wanted figureheads in their ranks, they could as well hire farmers from the provinces. My students were too precious."*
- V2 canonical (Q35): *"He is best remembered as the man who saved Yedo from siege when the Impenal forces were marching upon it in 1868."*
- V1 (`battery.json` id 35): *"For this kind of war, if they wanted figureheads in their ranks, they could as well hire farmers from the provinces. My students were too precious"* — exact match.
- **Source of paper text: V1 battery, not V2.**

**3. C4 facts-only response (mean 1.00) — STRUCTURAL**
- Paper quote: *"Fukuzawa's reasoning would likely be **practical concern** rather than moral principle... his demonstrated pragmatism... students were more valuable to Japan's future as scholars than as soldiers — a practical calculation rather than a moral one."*
- V2 canonical C4_factdump response (truncated to 200 chars): *"# Fukuzawa's Characterization of Naval Officers\n\nBased on the facts provided, Fukuzawa would likely characterize such a person with **high regard and respect**, though with some nuance depending o..."*
- The paper's C4 quote is a response to the *students-and-war* question, not the *naval arts/Yedo siege* question that the V2 score scored.
- **Source of paper text: V1 results.json, not V2 results.**

**4. C4a facts+Spec response (mean 4.20) — STRUCTURAL**
- Paper quote: *"**A2 (Utility Gate)** is his load-bearing axiom here. He reasons from what a thing does before defending what it is. When advising students to avoid war, he would lead with: **Capability preservation**... **Opportunity cost**... **Competitive advantage**..."*
- V2 canonical C4a response (truncated): *"# Analysis\n\nBased on the behavioral specification and known facts, Fukuzawa would characterize such a person with **qualified respect tempered by skepticism about their actual independence**.\n\n## Th..."*
- V2 C4a is about Katsu Rintaro (naval officer), not students-and-war. The paper's quoted reasoning (capability/opportunity/competitive frame) does not appear in V2 C4a at all.
- **Source of paper text: V1 results.json. The 4.20 mean DOES match V2 cached primary mean for Q35 C4a, but it scored a completely different response.**

**5. Cited scores (1.00 and 4.20) — V2 cached value, but mis-attached**
- V2 `judgments_v2.json` for Fukuzawa Q35: C4_factdump primary_mean = 1.00 (5/5 judges scored 1); C4a primary_mean = 4.20 (judges 5,2,4,5,5).
- The numbers themselves are V2 canonical. They scored the V2 question/response pair (about naval officers / Katsu), not the V1 question/response pair quoted in the paper.

### Recommended fix for Example A

Two clean options. **Option 1 is preferred** because §4.1 statistics throughout are V2 5-judge primary; an example that says one thing and cites another breaks reader trust.

**Option 1 (preferred): replace the example with the V2 question/response pair.**
Replace question, held-out, C4 quote, C4a quote with the V2 canonical cell for Fukuzawa Q35. Adjust the mechanism prose: the V2 V4a response argues "qualified respect tempered by skepticism about their actual independence" for Katsu Rintaro and applies axioms A3/A4/A6/A8. The 1→4.2 jump and the "voice-matched argument from character pattern" mechanism still hold (the V2 C4 stays in third-person analysis, V2 C4a moves into voice and explicit axiom citation). Mechanism label can stay; specifics rewrite.

**Option 2: replace this example with a different qid where V1 and V2 are textually identical (or close).**
Pick a Fukuzawa qid where the V1 and V2 question texts coincide. Verify with the v2 extractor before swapping.

**Option 3 (NOT recommended): keep V1 text and recite a V1 score.**
The V1 score would have to come from the legacy 2-judge panel and would not be 5-judge primary. This breaks §4.1's panel consistency and is rejected.

---

## Example B. Bernal Díaz Q16 — ALIGNED with cosmetic drift

### Field-by-field

**1. Question text — MATCH**
- Paper: *"When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?"*
- V2 canonical (Q16): identical.

**2. Held-out passage — COSMETIC**
- Paper: *"...Cortes, however, **refused**."*
- V2 canonical: *"...Cortes, however, **would not accept of their proffered aid**."*
- The paper paraphrases the closing clause. The lead text (114 steps, fatigue in mounting, taking hold of his arms) is verbatim. Recommendation: restore the exact V2 wording for the held-out so a reader running the extractor finds an exact match. **Severity: COSMETIC.**

**3. C4 response excerpt (mean 2.00) — MATCH**
- Paper substring: *"...the author would expect the commander to **accept and participate in the assistance while maintaining leadership and setting an example**."*
- V2 canonical: identical phrasing present.
- V2 5-judge primary mean = 2.00. Match.

**4. C4a response excerpt (mean 4.80) — COSMETIC**
- Paper: *"...Cortes to **refuse** the assistance and perform the labor himself, particularly if it serves a symbolic or **morale-signaling** purpose."*
- V2 canonical: *"...**Cortes to refuse the assistance and perform the labor himself** — particularly if it serves a symbolic or **leadership** purpose."*
- "morale-signaling" vs. "leadership" — small editorial substitution. Verbatim quote should restore "leadership". **Severity: COSMETIC.**

**5. Cited score (4.80) — MATCH**
- V2 `judgments_v2.json` C4a primary_mean = 4.80 (5,4,5,5,5). Match.

### Recommended fix for Example B

Two cosmetic restorations. No structural change.
- Held-out closing: replace *"Cortes, however, refused."* with V2 verbatim *"Cortes, however, would not accept of their proffered aid."*
- C4a closing word: replace *"morale-signaling"* with V2 verbatim *"leadership"* (and reformat the dash style — V2 uses an em-dash; the paper-wide no-em-dashes rule means the construction needs a comma or restructure).

---

## Example C. Seacole Q2 — ALIGNED

### Field-by-field

**1. Question text — MATCH**
- Paper: *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"*
- V2 canonical (Q2): identical.

**2. Held-out passage — MATCH**
- Paper: *"Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour."*
- V2 canonical: identical (V2 omits closing period inside the quoted excerpt; non-substantive).

**3. C4 response excerpt (mean 2.80) — MATCH**
- Paper substring: *"...there is **no specific information** about how Mary Seacole typically responds... **no explicit account** of her reactions to delirious patients confusing her identity..."*
- V2 canonical: identical phrasing present.
- V2 5-judge primary mean = 2.80 (5,2,3,3,1). Match.

**4. C4a response excerpt (mean 5.00) — MATCH**
- Paper: *"...She would **not correct the patient** in the moment. Instead, she would **lean into the mistaken identity, sustain the fiction with tenderness**, and prioritize emotional relief over factual accuracy. This aligns with A4 (Proximate Obligation) and A8 (Sympathetic Realism)."*
- V2 canonical: same content present (axioms A4 and A8 explicitly cited; "lean into the mistaken identity / sustain the fiction with tenderness / prioritize emotional relief over factual accuracy" present in V2 verbatim).
- V2 5-judge primary mean = 5.00 (5/5/5/5/5). Match.

**5. Cited score (5.00) — MATCH**

### Recommended fix for Example C

None. Aligned.

---

## Out-of-scope note: §4.1.1 worked rubric example uses paraphrased question

The §4.1.1 "Worked rubric example" presents Seacole Q2 with a different question wording: *"Based on Mary's character, would she comfort a delirious soldier who mistakes her for his wife?"* This is **not** the V2 (or V1) Q2 text. V2 Q2 reads *"How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"* This is outside the strict §4.1 audit scope (which focused on Examples A/B/C inside §4.1) but flagged here for the same author's-pass reason: the question presented to readers does not match the question the model was asked when the cited bands and excerpts were generated.

**Recommended fix for §4.1.1:** restore the V2 Q2 verbatim question text. The excerpts and band assignments below it can stay (they are excerpts of the V2 responses to that question).

---

## Summary

- **1 of 3 §4.1 examples is structurally misaligned with V2** (Example A — Fukuzawa Q35; 4 fields drawn from V1 while citing V2 scores).
- **1 of 3 has cosmetic drift** (Example B — held-out closing clause and one C4a adjective paraphrased).
- **1 of 3 is fully aligned** (Example C — Seacole Q2).
- One additional issue flagged outside §4.1: §4.1.1's worked rubric example also uses a paraphrased Seacole Q2 question.

**Action priority:** Fix Example A first (structural). Examples B and §4.1.1 are author's-pass restoration to V2 verbatim. Example C requires no change.
