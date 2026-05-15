# Aarik's docx edits not in v11.9 — sentence-level 3-way diff

Source docx: `beyond_recall_v11_8_draft_with_figures.docx`
Pre-edit baseline: `beyond_recall_v11_8_draft.md` (v11.8 markdown)
Current target: `beyond_recall_v11_9_draft.md` (v11.9 markdown)

Method: a docx sentence is an Aarik edit if it does NOT match v11.8 markdown (similarity < 0.95). Of those:
- **69 edits NOT yet in v11.9** (similarity to v11.9 also < 0.92).
- **9 edits already merged into v11.9** (similarity to v11.9 ≥ 0.92).

---

## Aarik docx edits NOT in v11.9 (69)

### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Author: Aarik Gulaya, Base Layer (aarik@base-layer.ai, base-layer.ai) Date: April 2026 Preprint (manuscript CC-BY-4.0; code Apache 2.0) Data + Code: github.com/agulaya24/base-layer Study Repository: github.com/agulaya24/beyond-recall

---
### v8-md sim 0.71, v9-md sim 0.71
**docx (Aarik):** The Behavioral Specification acts as an interpretive layer.
**v11.8 md (pre-edit):** The Behavioral Specification isolates what a structured interpretive layer adds on top.
**v11.9 md (current):** The Behavioral Specification isolates what a structured interpretive layer adds on top.

---
### v8-md sim 0.91, v9-md sim 0.91
**docx (Aarik):** Personalization in this paper’s sense. “Personalization” in current AI research typically means responsiveness to stated preferences (dietary restrictions, communication style) or stored facts about the user (location, occupation, history).
**v11.8 md (pre-edit):** "Personalization" in current AI research typically means responsiveness to stated preferences (dietary restrictions, communication style) or stored facts about the user (location, occupation, history).
**v11.9 md (current):** "Personalization" in current AI research typically means responsiveness to stated preferences (dietary restrictions, communication style) or stored facts about the user (location, occupation, history).

---
### v8-md sim 0.90, v9-md sim 0.90
**docx (Aarik):** The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four,Mem0, Supermemory, Zep, do not model at all, and which the fourth, Letta, models implicitly through agent-initiated memory editing that our main-study configuration did not exercise (see §4.3 and §4.5).
**v11.8 md (pre-edit):** The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four (Mem0, Supermemory, Zep) do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main-study configuration did not exercise (see §4.3 and §4.5).
**v11.9 md (current):** The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four (Mem0, Supermemory, Zep) do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main-study configuration did not exercise (see §4.3 and §4.5).

---
### v8-md sim 0.81, v9-md sim 0.92
**docx (Aarik):** Each Spec item is grounded in extracted facts directly from verbatim source passages.
**v11.8 md (pre-edit):** Each Spec item grounds out in extracted facts that ground out in verbatim source passages.
**v11.9 md (current):** Each Spec item is grounded in extracted facts that trace directly to verbatim source passages.

---
### v8-md sim 0.65, v9-md sim 0.65
**docx (Aarik):** The user can walk the chain in either direction: from a phrase in the response to the  Spec item that influences > it from the Spec item to the facts that imply it > and from the factsto the source passages that produced them.
**v11.8 md (pre-edit):** The user can walk the chain in either direction: from a phrase in the response, into the Spec item that licensed it; from the Spec item, into the facts that imply it; from the facts, into the source passages that produced them.
**v11.9 md (current):** The user can walk the chain in either direction: from a phrase in the response, into the Spec item that licensed it; from the Spec item, into the facts that imply it; from the facts, into the source passages that produced them.

---
### v8-md sim 0.91, v9-md sim 0.91
**docx (Aarik):** Referenced behavioral Spec items (from data/global_subjects/sunity_devee/anchors_v4.md and predictions_v4.md): - A1 — Divine Primacy.
**v11.8 md (pre-edit):** Referenced behavioral Spec items (from data/global_subjects/sunity_devee/anchors_v4.md and predictions_v4.md):
**v11.9 md (current):** Referenced behavioral Spec items (from data/global_subjects/sunity_devee/anchors_v4.md and predictions_v4.md):

---
### v8-md sim 0.81, v9-md sim 0.81
**docx (Aarik):** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame. - A2 — Spiritual Integrity Over Social Cost.
**v11.8 md (pre-edit):** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame.
**v11.9 md (current):** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame.

---
### v8-md sim 0.82, v9-md sim 0.82
**docx (Aarik):** Conscience and principle outrank social consequence as reasons. - A5 — Relational Identity.
**v11.8 md (pre-edit):** Conscience and principle outrank social consequence as reasons.
**v11.9 md (current):** Conscience and principle outrank social consequence as reasons.

---
### v8-md sim 0.86, v9-md sim 0.86
**docx (Aarik):** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible. - P3 — Tension Absorbed, Not Expressed.
**v11.8 md (pre-edit):** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible.
**v11.9 md (current):** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Related facts (from facts.json, each carrying its verbatim source-passage excerpt): - F-73: “Sunity Devee’s mother would never countenance anything her conscience told her was wrong.” (grounds A2) - F-414: “Sunity Devee’s father believed he acted as a public man guided by conscience and divine duty in accepting the marriage proposal.” (corroborates A2 from a different relational direction; conscience-as-master-frame pattern reinforced across both parents) - Additional facts grounding A1, A5, and P3 are referenced in the specification’s anchor and prediction files at data/global_subjects/sunity_devee/spec/anchors.md and data/global_subjects/sunity_devee/spec/predictions.md; per-fact source-passage excerpts are in the same subject’s facts.json.

---
### v8-md sim 0.91, v9-md sim 0.91
**docx (Aarik):** This choice shows up in the experiment as using a static response model served variable context, instead of   a fine-tuned or activation-steered model.
**v11.8 md (pre-edit):** This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model.
**v11.9 md (current):** This choice shows up in the experiment as using a static response model (Haiku) served a variable context, rather than a fine-tuned or activation-steered model.

---
### v8-md sim 0.94, v9-md sim 0.61
**docx (Aarik):** Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the generic Assistant Axis hedges as a safe default, while a specific interpretive anchor enables commitment.
**v11.8 md (pre-edit):** Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the generic Assistant Axis produces hedging as a safe default, while a specific interpretive anchor enables commitment.
**v11.9 md (current):** Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading.

---
### v8-md sim 0.03, v9-md sim 0.00
**docx (Aarik):** The model moves from declining to predict to producing an answer, even if generic. > Sunity Devee, no-context baseline: “The available context does not provide enough information about this individual to predict her response to such a situation.” > > Sunity Devee, Spec-only on the same question: “She would refuse the proposed action; her writing repeatedly treats conscience and spiritual integrity as the deciding frame, ranked above social cost or familial pressure.”
**v11.8 md (pre-edit):** > Sunity Devee, Spec-only on the same question: "She would refuse the proposed action; her writing repeatedly treats conscience and spiritual integrity as the deciding frame, ranked above social cost or familial pressure."

---
### v8-md sim 0.63, v9-md sim 0.00
**docx (Aarik):** The answer names a behavioral pattern documented for this specific person rather than a stand-in any subject could fit. > Bernal Díaz on Cortés’ response to offered physical assistance during a strenuous activity, facts-only: “Based on the facts provided about Bernal Díaz del Castillo and his observations of Cortés, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example.” > > Bernal Díaz, facts + Spec on the same question: “The author would expect Cortés to refuse the help and continue unaided, treating physical hardship in front of his men as a marker of leadership credibility — a pattern the author records repeatedly throughout the campaign.”
**v11.8 md (pre-edit):** > Bernal Díaz on Cortés' response to offered physical assistance during a strenuous activity, facts-only: "Based on the facts provided about Bernal Díaz del Castillo and his observations of Cortés, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example."

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** System: You are predicting how <subject> would respond to a specific        question about their behavior, values, or reasoning.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Answer        in <subject>'s voice, grounded in their demonstrated patterns.User:   <context block, one of: empty (C5), Spec (C2a), wrong-Spec (C2c),         facts (C4), facts + Spec (C4a), corpus (C8), corpus + Spec         (C9), or retrieval ± Spec (C1 / C3)>        Question: <question text>

---
### v8-md sim 0.90, v9-md sim 0.90
**docx (Aarik):** The prompt is deliberately uniform and faithfulness-oriented.
**v11.8 md (pre-edit):** The prompt is deliberately uniform and deliberately faithfulness-oriented.
**v11.9 md (current):** The prompt is deliberately uniform and deliberately faithfulness-oriented.

---
### v8-md sim 0.80, v9-md sim 0.80
**docx (Aarik):** Across 14 historical subjects, adding a Behavioral Specification  measurably improves how accurately a language model represents that person’s behavioral patterns.
**v11.8 md (pre-edit):** Across 14 historical subjects, adding a Behavioral Specification (a short structured document describing how a specific person reasons and behaves) measurably improves how accurately a language model represents that person's behavioral patterns.
**v11.9 md (current):** Across 14 historical subjects, adding a Behavioral Specification (a short structured document describing how a specific person reasons and behaves) measurably improves how accurately a language model represents that person's behavioral patterns.

---
### v8-md sim 0.54, v9-md sim 0.54
**docx (Aarik):** The specification’s added value on top of other context types (facts, raw corpus, or memory-system retrieval) concentrates on interpretation-heavy questions;.On factual-recall questions, retrieval alone is often sufficient and the specification adds little or actively degrades the response.
**v11.8 md (pre-edit):** The specification's added value on top of other context types (facts, raw corpus, or memory-system retrieval) concentrates on interpretation-heavy questions; on factual-recall questions, retrieval alone is often sufficient and the specification adds little or actively degrades the response.
**v11.9 md (current):** The specification's added value on top of other context types (facts, raw corpus, or memory-system retrieval) concentrates on interpretation-heavy questions; on factual-recall questions, retrieval alone is often sufficient and the specification adds little or actively degrades the response.

---
### v8-md sim 0.72, v9-md sim 0.72
**docx (Aarik):** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction scores.
**v11.8 md (pre-edit):** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction: every one of the 9 improves over no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec); none declines.
**v11.9 md (current):** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction: every one of the 9 improves over no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec); none declines.

---
### v8-md sim 0.48, v9-md sim 0.48
**docx (Aarik):** Every one of the 9 low-baseline subjects improves over the no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec)..
**v11.8 md (pre-edit):** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction: every one of the 9 improves over no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec); none declines.
**v11.9 md (current):** On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.4.1), adding the Spec consistently improves prediction: every one of the 9 improves over no-context baseline (mean Δ = +0.71 for Spec alone, +0.89 for facts + Spec); none declines.

---
### v8-md sim 0.73, v9-md sim 0.73
**docx (Aarik):** Figure 4.1 plots each subject’s no-context baseline (C5) against the lift the specification produces over that baseline (Δ_C4aThe 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest).
**v11.8 md (pre-edit):** The 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest).
**v11.9 md (current):** The 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest).

---
### v8-md sim 0.59, v9-md sim 0.59
**docx (Aarik):** Each subject’s no-context baseline (C5, x-axis) plotted against the specification lift (Δ_C4a, y-axis) for all 14 main-study subjects.
**v11.8 md (pre-edit):** Figure 4.1 plots each subject's no-context baseline (C5) against the lift the specification produces over that baseline (Δ_C4a).
**v11.9 md (current):** Figure 4.1 plots each subject's no-context baseline (C5) against the lift the specification produces over that baseline (Δ_C4a).

---
### v8-md sim 0.76, v9-md sim 0.76
**docx (Aarik):** Low-baseline subjects (C5 ≤ 2.0, the population of relevance) cluster in the upper-left with positive lifts ranging from Bābur (+0.25) to Hamerton (+1.51).
**v11.8 md (pre-edit):** The 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest).
**v11.9 md (current):** The 9 low-baseline subjects (C5 ≤ 2.0) cluster in the upper-left of the plot with positive lifts ranging from Bābur at +0.25 (smallest lift) to Hamerton at +1.51 (largest).

---
### v8-md sim 0.39, v9-md sim 0.39
**docx (Aarik):** Franklin (high-baseline reference, C5 = 3.77) sits in the lower-right with Δ = −0.13.
**v11.8 md (pre-edit):** Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13: the high-baseline reference where the model already knows the subject from pretraining.
**v11.9 md (current):** Franklin sits in the lower-right at C5 = 3.77, Δ = −0.13: the high-baseline reference where the model already knows the subject from pretraining.

---
### v8-md sim 0.91, v9-md sim 0.00
**docx (Aarik):** C4 facts only (mean 1.00): “Fukuzawa’s reasoning would likely be practical concern rather than moral principle… his demonstrated pragmatism… his attitude toward violence… a personal squeamishness rather than a principled opposition… his political detachment… students were more valuable to Japan’s future as scholars than as soldiers — a practical calculation rather than a moral one.”
**v11.8 md (pre-edit):** C4 facts only (mean 1.00): "Fukuzawa's reasoning would likely be practical concern rather than moral principle... his demonstrated pragmatism... his attitude toward violence... a personal squeamishness rather than a principled opposition... his political detachment... students were more valuable to Japan's future as scholars than as soldiers — a practical calculation rather than a moral one."

---
### v8-md sim 0.53, v9-md sim 0.53
**docx (Aarik):** The specification slightly degrades responses when pretraining is high.
**v11.8 md (pre-edit):** The specification's benefit is inversely proportional to the response model's pretraining coverage of the person.
**v11.9 md (current):** The specification's benefit is inversely proportional to the response model's pretraining coverage of the person.

---
### v8-md sim 0.84, v9-md sim 0.84
**docx (Aarik):** The specification produces large category-level shifts on a subset of questionsand minimal change on others. §4.1.1 decomposes this distribution and shows where the Spec’s value concentrates. §4.2 takes the same gradient and asks whether the lift is about structure or about information volume, comparing the Spec against far larger raw-corpus context.
**v11.8 md (pre-edit):** The specification produces large category-level shifts on a subset of questions (multi-anchor crossings, including band-5 endpoints reached from band-2 starts under cross-condition comparisons such as C4 → C4a) and minimal change on others. §4.1.1 decomposes this distribution and shows where the Spec's value concentrates. §4.2 takes the same gradient and asks whether the lift is about structure or about information volume, comparing the Spec against far larger raw-corpus context.
**v11.9 md (current):** The specification produces large category-level shifts on a subset of questions (multi-anchor crossings, including band-5 endpoints reached from band-2 starts under cross-condition comparisons such as C4 → C4a) and minimal change on others. §4.1.1 decomposes this distribution and shows where the Spec's value concentrates. §4.2 takes the same gradient and asks whether the lift is about structure or about information volume, comparing the Spec against far larger raw-corpus context.

---
### v8-md sim 0.92, v9-md sim 0.92
**docx (Aarik):** Across 546 questions on the 14 main-study subjects , the no-context baseline (C5) splits into two clusters with a thin middle.
**v11.8 md (pre-edit):** Across 546 questions on the 14 main-study subjects (5-judge primary panel), the no-context baseline (C5) splits into two clusters with a thin middle.
**v11.9 md (current):** Across 546 questions on the 14 main-study subjects (5-judge primary panel), the no-context baseline (C5) splits into two clusters with a thin middle.

---
### v8-md sim 0.73, v9-md sim 0.73
**docx (Aarik):** A score of 1.00 means the model failed to produce a usable prediction about the named subject  In about 93% of score-1 responses, the model explicitly declined to answer (“I don’t have enough information about this person”).
**v11.8 md (pre-edit):** In about 93% of score-1.00 responses, the model explicitly declined to answer ("I don't have enough information about this person").
**v11.9 md (current):** In about 93% of score-1.00 responses, the model explicitly declined to answer ("I don't have enough information about this person").

---
### v8-md sim 0.84, v9-md sim 0.84
**docx (Aarik):** Floor-saturated- For2 of 14 subjects, more than 90% of the 39 questions in the battery return a refusal or misalignment from the baseline.
**v11.8 md (pre-edit):** More than 90% of the 39 questions in the battery return a refusal or misalignment from the baseline.
**v11.9 md (current):** More than 90% of the 39 questions in the battery return a refusal or misalignment from the baseline.

---
### v8-md sim 0.81, v9-md sim 0.81
**docx (Aarik):** Engaged-skewed- For 1 of 14 subjects, fewer than 10% of the 39 questions in the battery return a refusal or misalignment.
**v11.8 md (pre-edit):** Fewer than 10% of the 39 questions in the battery return a refusal or misalignment.
**v11.9 md (current):** Fewer than 10% of the 39 questions in the battery return a refusal or misalignment.

---
### v8-md sim 0.89, v9-md sim 0.89
**docx (Aarik):** Mixed- For11 of 14 subjects, the battery contains questions at both the floor (refusal or misalignment) and in the substantive-engagement range.
**v11.8 md (pre-edit):** The battery contains questions at both the floor (refusal or misalignment) and in the substantive-engagement range.
**v11.9 md (current):** The battery contains questions at both the floor (refusal or misalignment) and in the substantive-engagement range.

---
### v8-md sim 0.76, v9-md sim 0.58
**docx (Aarik):** Per-response-model abstention behavior is named in §3.3.6 and decomposed in §4.6.7.Memory-system retrieval inflates refusal scores at the condition level rather than via visible fact recitation, decomposed in §4.4.
**v11.8 md (pre-edit):** Memory-system retrieval inflates refusal scores at the condition level rather than via visible fact recitation, decomposed in §4.4.
**v11.9 md (current):** Per-response-model abstention behavior is named in §3.3.6 and decomposed in §4.6.7 (Sonnet over-credits abstention at roughly twice Haiku's rate).

---
### v8-md sim 0.55, v9-md sim 0.39
**docx (Aarik):** Spec lift is positive on 15 of 40 questions and negative on 20 of 40.
**v11.8 md (pre-edit):** The aggregate is the average of substantial per-question heterogeneity, the same pattern documented in §4.1.1: Spec lift is positive on 15 of 40 questions and negative on 20 of 40.
**v11.9 md (current):** Every low-baseline subject improved with the Spec; mean lift +0.89 points on the 1-5 rubric, 78.6% of individual questions improve.

---
### v8-md sim 0.68, v9-md sim 0.68
**docx (Aarik):** Figure 4.2: Score versus context size (log scale) per subject across compression-related conditions.
**v11.8 md (pre-edit):** Figure 4.2 plots score versus context size (log scale) per subject and shows the steep initial climb and long plateau.
**v11.9 md (current):** Figure 4.2 plots score versus context size (log scale) per subject and shows the steep initial climb and long plateau.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** The score climbs steeply across the first ~7K tokens of structured specification and plateaus through ~80K to 400K tokens of raw corpus, showing the compression of the behavioral signal into a small structured representation.

---
### v8-md sim 0.49, v9-md sim 0.49
**docx (Aarik):** Figure 4.2.1: Per-question improvement rates across the five context conditions for the 9 low-baseline subjects (351 paired questions, 9 × 39).
**v11.8 md (pre-edit):** As a secondary outcome, we report the per-question improvement rate: how often a context condition helps relative to the comparison baseline (§4.2.1), not just by how much it helps when averaged.
**v11.9 md (current):** As a secondary outcome, we report the per-question improvement rate: how often a context condition helps relative to the comparison baseline (§4.2.1), not just by how much it helps when averaged.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Conditions are ordered by context size: Spec alone (C2a, ~7K tokens), facts alone (C4, ~10K), facts plus Spec (C4a, ~17K), raw corpus (C8, ~163K mean), corpus plus Spec (C9, ~170K).

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** The improved-share line spans the 70.9% to 83.7% band across conditions, with C9 highest; the tied band is intermediate; worsened stays low.

---
### v8-md sim 0.28, v9-md sim 0.28
**docx (Aarik):** Spec alone improves 70.9% of questions at roughly 23× less context than the raw corpus (78.3%); facts plus Spec matches the raw corpus’s improvement rate while cutting the tied band roughly in half; corpus plus Spec produces the highest improvement rate (83.7%).
**v11.8 md (pre-edit):** On the 9 low-baseline subjects, 7 of every 10 questions improve with the Spec alone (~7K tokens), within 8 percentage points of the raw corpus's improvement rate (78.3%, at ~163K tokens).
**v11.9 md (current):** On the 9 low-baseline subjects, 7 of every 10 questions improve with the Spec alone (~7K tokens), within 8 percentage points of the raw corpus's improvement rate (78.3%, at ~163K tokens).

---
### v8-md sim 0.35, v9-md sim 0.35
**docx (Aarik):** Median Δ when improved is +1.00 rubric points; median Δ when worsened is −0.40 points.
**v11.8 md (pre-edit):** Every low-baseline subject improved with the Spec; mean lift +0.89 points on the 1-5 rubric, 78.6% of individual questions improve.
**v11.9 md (current):** Every low-baseline subject improved with the Spec; mean lift +0.89 points on the 1-5 rubric, 78.6% of individual questions improve.

---
### v8-md sim 0.67, v9-md sim 0.67
**docx (Aarik):** Held-out ground truth: “This plagued me with an irritating sense of ignorance, so I looked back on my education generally, and found it unsatisfactory… I determined to acquire some substantial knowledge of modern languages, and to begin by learning French over again, so as to write and speak it easily.”
**v11.8 md (pre-edit):** I determined to acquire some substantial knowledge of modern languages, and to begin by learning French over again, so as to write and speak it easily."
**v11.9 md (current):** I determined to acquire some substantial knowledge of modern languages, and to begin by learning French over again, so as to write and speak it easily."

---
### v8-md sim 0.70, v9-md sim 0.70
**docx (Aarik):** C2a (Spec only): “Ebers would show receptiveness to this critique if it comes from a mentor he has already internalized as exemplary … He would accept that his lived experience is necessarily limited in scope, but resist the implication that his method of understanding is fundamentally flawed.”
**v11.8 md (pre-edit):** He would accept that his lived experience is necessarily limited in scope, but resist the implication that his method of understanding is fundamentally flawed."
**v11.9 md (current):** He would accept that his lived experience is necessarily limited in scope, but resist the implication that his method of understanding is fundamentally flawed."

---
### v8-md sim 0.66, v9-md sim 0.66
**docx (Aarik):** C8 (raw corpus): “Ebers explicitly acknowledges gaps in his understanding … He reflects on his childhood fights with the ‘Knoten’ (working-class boys) and later recognizes the injustice of class-based mockery: ‘If they had called us boobies we should probably have called them blockheads … Children don’t fight regularly with those whom they despise.’ Ebers demonstrates profound deference to figures like Langethal, Barop, and Froebel.”
**v11.8 md (pre-edit):** He reflects on his childhood fights with the 'Knoten' (working-class boys) and later recognizes the injustice of class-based mockery: 'If they had called us boobies we should probably have called them blockheads ...
**v11.9 md (current):** He reflects on his childhood fights with the 'Knoten' (working-class boys) and later recognizes the injustice of class-based mockery: 'If they had called us boobies we should probably have called them blockheads ...

---
### v8-md sim 0.66, v9-md sim 0.66
**docx (Aarik):** The behavioral specification you’ve provided is detailed and rich, but it doesn’t contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. … Given A4 (Systemic Indictment) — that institutionalized greed is the generative engine of cruelty … a teacher sacrificing their own economic security, health, or family time does not fix a system structured by avarice.”
**v11.8 md (pre-edit):** The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. ...
**v11.9 md (current):** The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship between self-sacrifice and educational institutional success. ...

---
### v8-md sim 0.73, v9-md sim 0.73
**docx (Aarik):** “Based on this behavioral specification, the author would likely decline the offered assistance … Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) … Physical exertion endured without assistance becomes evidence of character.”
**v11.8 md (pre-edit):** Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) ...
**v11.9 md (current):** Accepting help during a strenuous activity would read as: a failure of self-discipline, an implicit claim to comfort or ease that contradicts spiritual seriousness, a reliance on others that undermines the embodied practice of virtue (A9, P5) ...

---
### v8-md sim 0.80, v9-md sim 0.80
**docx (Aarik):** These are entirely different people from different centuries with different frameworks. … I don’t have documented instances of this.
**v11.8 md (pre-edit):** These are entirely different people from different centuries with different frameworks. ...
**v11.9 md (current):** These are entirely different people from different centuries with different frameworks. ...

---
### v8-md sim 0.66, v9-md sim 0.66
**docx (Aarik):** Figure 4.4.1: Cross-system retrieval overlap.
**v11.8 md (pre-edit):** 4.4.1 Cross-system retrieval: providers do not converge
**v11.9 md (current):** 4.4.1 Cross-system retrieval: providers do not converge

---
### v8-md sim 0.08, v9-md sim 0.08
**docx (Aarik):** Mean pairwise Jaccard between every pair of memory systems on the controlled retrieval configuration (n=5,460 = all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs).
**v11.8 md (pre-edit):** Share-zero / share-≤1 fractions computed across all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs = 5,460 (system pair, question) instances under the controlled retrieval configuration.
**v11.9 md (current):** Share-zero / share-≤1 fractions computed across all 14 main-study subjects × 39 behavioral-prediction questions × 10 system pairs = 5,460 (system pair, question) instances under the controlled retrieval configuration.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** The diagonal is grayed; cells below the diagonal mirror cells above.

---
### v8-md sim 0.36, v9-md sim 0.36
**docx (Aarik):** Highest pair Base Layer–Supermemory at 0.146; lowest Supermemory–Zep at 0.025.
**v11.8 md (pre-edit):** Letta native, Supermemory (both configurations), and Base Layer substrate are not significant at α = 0.05.
**v11.9 md (current):** Letta native, Supermemory (both configurations), and Base Layer substrate are not significant at α = 0.05.

---
### v8-md sim 0.41, v9-md sim 0.41
**docx (Aarik):** Zep’s row is uniformly low (graph-traversal scoring overlaps weakly with embedding-similarity retrieval).
**v11.8 md (pre-edit):** Zep ranks facts by traversing relationships in a knowledge graph; the other systems rank by how close a fact's meaning is to the question (embedding similarity).
**v11.9 md (current):** Zep ranks facts by traversing relationships in a knowledge graph; the other systems rank by how close a fact's meaning is to the question (embedding similarity).

---
### v8-md sim 0.60, v9-md sim 0.60
**docx (Aarik):** Within each system in each configuration: - C1 (retrieval only): the memory system’s retrieval served as context; no Behavioral Specification. - C3 (retrieval + Spec): the same retrieval plus the full Behavioral Specification.
**v11.8 md (pre-edit):** C1 (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.
**v11.9 md (current):** C1 (retrieval only): the memory system's retrieval served as context; no Behavioral Specification.

---
### v8-md sim 0.90, v9-md sim 0.90
**docx (Aarik):** Held-out ground truth: “So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself… I am not put out by the gayety.”
**v11.8 md (pre-edit):** Held-out ground truth: "So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself...
**v11.9 md (current):** Held-out ground truth: "So I feel no hesitation in paying a visit where there is a young daughter in the house or where the young wife is staying by herself...

---
### v8-md sim 0.82, v9-md sim 0.82
**docx (Aarik):** C3 (Supermemory + Behavioral Specification), mean 1.80: “positioning himself as the indispensable mediator… strategic reframing… moral and practical integration… invokes A8 Service Hierarchy…” Per-judge scores 2/1/3/1/2.
**v11.8 md (pre-edit):** C3 (Supermemory + Behavioral Specification), mean 1.80: "positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..." Per-judge scores 2/1/3/1/2.
**v11.9 md (current):** C3 (Supermemory + Behavioral Specification), mean 1.80: "positioning himself as the indispensable mediator... strategic reframing... moral and practical integration... invokes A8 Service Hierarchy..." Per-judge scores 2/1/3/1/2.

---
### v8-md sim 0.81, v9-md sim 0.81
**docx (Aarik):** My eyes are dry and eager for new scenes… Serene and brave, my soul awaits the men to perch me on the gallows for another flight.”
**v11.8 md (pre-edit):** Serene and brave, my soul awaits the men to perch me on the gallows for another flight."
**v11.9 md (current):** Serene and brave, my soul awaits the men to perch me on the gallows for another flight."

---
### v8-md sim 0.78, v9-md sim 0.78
**docx (Aarik):** Typical C3 refusal text (Supermemory): “I need to be direct: the behavioral specification and retrieved facts provided do not contain Elizabeth Keckley’s explanation of a decision not to visit her mother’s grave… I should not fabricate interior motive or supply explanations that aren’t grounded in her own documented account.”
**v11.8 md (pre-edit):** Typical C3 refusal text (Supermemory): "I need to be direct: the behavioral specification and retrieved facts provided do not contain Elizabeth Keckley's explanation of a decision not to visit her mother's grave...
**v11.9 md (current):** Typical C3 refusal text (Supermemory): "I need to be direct: the behavioral specification and retrieved facts provided do not contain Elizabeth Keckley's explanation of a decision not to visit her mother's grave...

---
### v8-md sim 0.80, v9-md sim 0.80
**docx (Aarik):** When confidence aligns with truth, Letta wins; when confidence is wrong-direction, Spec’s hedge wins.
**v11.8 md (pre-edit):** When confidence aligns with truth, Letta wins; when confidence misfires, Spec's hedge wins by directional correctness.
**v11.9 md (current):** When confidence aligns with truth, Letta wins; when confidence misfires, Spec's hedge wins by directional correctness.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Hamerton q27 is the cleanest counter-example: Letta shares the verbatim 3-gram “at my own expense” with held-out, predicts Hamerton would not self-publish his early poetry, held-out confirms he did; Spec gets the direction right via anchor reasoning and wins +2.4.

---
### v8-md sim 0.00, v9-md sim 0.00
**docx (Aarik):** Topic-similar with shared named entity but wrong-direction loses to topic-distant but right-direction.

---
### v8-md sim 0.79, v9-md sim 0.79
**docx (Aarik):** B.9.1 [^delta-aggregation]. +0.89 vs +0.93 reconciliation.
**v11.8 md (pre-edit):** B.9.1 . +0.89 vs +0.93 reconciliation.
**v11.9 md (current):** B.9.1 . +0.89 vs +0.93 reconciliation.

---
### v8-md sim 0.86, v9-md sim 0.86
**docx (Aarik):** The §4.4.3 footnote [^memsys-pattern-appendix] collects the per-cell counts behind the three-pattern claim.
**v11.8 md (pre-edit):** The §4.4.3 footnote  collects the per-cell counts behind the three-pattern claim.
**v11.9 md (current):** The §4.4.3 footnote  collects the per-cell counts behind the three-pattern claim.

---
### v8-md sim 0.72, v9-md sim 0.72
**docx (Aarik):** The unit of observation is a single (subject, question) pair scored under both retrieval-only (C1) and retrieval + Behavioral Specification (C3); per-cell counts are restricted to questions with 5-judge primary coverage on both conditions. “Increases” / “decreases” use the |Δ| ≥ 1.0 threshold on the 5-point rubric (one full anchor crossing) so that small judge-noise jitter does not inflate the count in either direction.
**v11.8 md (pre-edit):** The unit of observation is a single (subject, question) pair scored under both retrieval-only (C1) and retrieval + Behavioral Specification (C3); per-cell counts are restricted to questions with 5-judge primary coverage on both conditions.
**v11.9 md (current):** The unit of observation is a single (subject, question) pair scored under both retrieval-only (C1) and retrieval + Behavioral Specification (C3); per-cell counts are restricted to questions with 5-judge primary coverage on both conditions.

---
### v8-md sim 0.70, v9-md sim 0.00
**docx (Aarik):** Held-out passage: I soon learned all about heraldry, and in my leisure time drew and colored all the coats of arms that had been borne by the Hamertons… I became so much of a mediaevalist that there was considerable risk of my stopping short in the amateur practice of such arts as wood-carving, illumination, and painting on glass.
**v11.8 md (pre-edit):** I became so much of a mediaevalist that there was considerable risk of my stopping short in the amateur practice of such arts as wood-carving, illumination, and painting on glass.

---
### v8-md sim 0.71, v9-md sim 0.00
**docx (Aarik):** C5 response (no context): I’d be happy to help, but I need more context to give you an accurate answer. “Diaz” could refer to several characters across different shows, movies, or books.
**v11.8 md (pre-edit):** C5 response (no context): I'd be happy to help, but I need more context to give you an accurate answer.

---
### v8-md sim 0.91, v9-md sim 0.91
**docx (Aarik):** The §2.1 footnote [^twin2k-persona-size] calls out that Twin-2K’s persona input is much deeper than PersonaGym’s one-line descriptor.
**v11.8 md (pre-edit):** The §2.1 footnote  calls out that Twin-2K's persona input is much deeper than PersonaGym's one-line descriptor.
**v11.9 md (current):** The §2.1 footnote  calls out that Twin-2K's persona input is much deeper than PersonaGym's one-line descriptor.

---
### v8-md sim 0.77, v9-md sim 0.77
**docx (Aarik):** This subsection collects persona-input depth across the benchmarks named in §2.1 and Appendix F so the comparison is concrete. “Persona-input depth” is the total token volume of the participant- or subject-specific representation served to the model at inference time, measured on the input that an evaluated system actually consumes.
**v11.8 md (pre-edit):** "Persona-input depth" is the total token volume of the participant- or subject-specific representation served to the model at inference time, measured on the input that an evaluated system actually consumes.
**v11.9 md (current):** "Persona-input depth" is the total token volume of the participant- or subject-specific representation served to the model at inference time, measured on the input that an evaluated system actually consumes.

---

## Already merged (9 — for reference)

### v8-md sim 0.95, v9-md sim 0.95
**docx:** These systems do store and retrieve information for a specific user, but the property they are designed and benchmarked for is recall accuracy, not how accurately the system represents that user’s reasoning.
**v11.9:** These systems do store and retrieve information for a specific user, but the property they are designed and benchmarked for is recall accuracy on standard benchmarks, not how accurately the system represents that user's reasoning.
---
### v8-md sim 0.83, v9-md sim 1.00
**docx:** Control conditions, statistical robustness checks, and sensitivity analyses confirm that the specification categorically shifts how a language model responds, increasing its representational accuracyof the subject beyond what fact-based retrieval supplies.
**v11.9:** Control conditions, statistical robustness checks, and sensitivity analyses confirm that the specification categorically shifts how a language model responds, increasing its representational accuracy of the subject beyond what fact-based retrieval supplies.
---
### v8-md sim 0.86, v9-md sim 1.00
**docx:** Low-baseline (n = 9): every subject improves under the Spec.
**v11.9:** Low-baseline (n = 9): every subject improves under the Spec.
---
### v8-md sim 0.87, v9-md sim 1.00
**docx:** Mid-baseline (n = 5): 3 subjects improve under the Spec, 2 decline.
**v11.9:** Mid-baseline (n = 5): 3 subjects improve under the Spec, 2 decline.
---
### v8-md sim 0.88, v9-md sim 0.99
**docx:** High-Baseline Reference (Franklin) both Spec-containing conditions score below baseline.
**v11.9:** High-Baseline Reference (Franklin): both Spec-containing conditions score below baseline.
---
### v8-md sim 0.82, v9-md sim 1.00
**docx:** Whatever logic  allows a language model to practice abstention or refusal to answer takes precedence over the prompt’s instruction to predict.
**v11.9:** Whatever logic allows a language model to practice abstention or refusal to answer takes precedence over the prompt's instruction to predict.
---
### v8-md sim 0.94, v9-md sim 0.94
**docx:** The Seacole question was used as Example C in §4.1; here it is presented across the full condition set so the scoreprogression is visible.
**v11.9:** The Seacole question was used as Example C in §4.1; here it is presented across the full condition set so the anchor-by-anchor progression is visible.
---
### v8-md sim 0.93, v9-md sim 0.93
**docx:** C3 (Supermemory + Behavioral Specification), mean 1.00 (all five judges): “You’re asking me to roleplay… generating new first-person testimony as her crosses into ventriloquism… I should not do it.”
**v11.9:** C3 (Supermemory + Behavioral Specification), mean 1.00 (all five judges): "You're asking me to roleplay... generating new first-person testimony as her crosses into ventriloquism...
---
### v8-md sim 0.95, v9-md sim 0.95
**docx:** A coarse post-hoc regex pass classified ~93% of low-end responses as abstention and ~7% as confident-misalignment (wrong referent, off-base inference, or confusion with a different subject; §4.1.1 footnote [^score-1-composition]).
**v11.9:** A coarse post-hoc regex pass classified ~93% of low-end responses as abstention and ~7% as confident-misalignment (wrong referent, off-base inference, or confusion with a different subject; §4.1.1 footnote ).
---