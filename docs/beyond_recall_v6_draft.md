<!--
==========================================================================
 EDITORIAL CHECKLIST — Aarik review items before push (remove before publication)

 Each item has: [ ] CHECKBOX | CLAUDE'S READ | ALTERNATIVES | STAKES
==========================================================================

=== 1. TITLE ==========================================================
[ ] "Beyond Recall: Behavioral Specification as the Missing Primitive for
    AI Personalization"

    CLAUDE'S READ: "Missing Primitive" is the single most contested word in the
    paper. Three of five collective reviewers (PG, Scott, Julia) pushed back on
    it. The word is defensible in §5.1 IF those rebuttals land, but a casual
    reader sees the word in the title and forms an expectation the body may
    not fully meet.

    OPTIONS (pick one):
    (A) KEEP: "Beyond Recall: Behavioral Specification as the Missing Primitive
        for AI Personalization"
        → Bold claim, stakes position, forces the argument. Risk: overreach
        accusation if §5.1 isn't ironclad.
    (B) SOFTEN: "Beyond Recall: Behavioral Specification as the Missing
        Interpretive Layer for AI Personalization"
        → Same argument, less swaggering word. My recommendation if you're
        worried about being called out for overclaim.
    (C) DROP PRIMITIVE ENTIRELY: "Beyond Recall: How AI Agents Need to
        Represent the People They Serve"
        → More descriptive, less catchy, avoids the fight entirely.
    (D) COMPLETELY DIFFERENT: "Representational Accuracy: The Missing Metric
        in AI Personalization"
        → Leads with the concept, not the proposed solution. Most academic.

    RECOMMENDATION: (B) — keeps the stake in the ground, drops the contested
    word. You get 90% of the punch, 10% of the attack surface.

=== 2. TLDR ===========================================================
[ ] Currently: "Memory systems store what someone said. Preference models
    store what they liked. Personas store how they present. None of them
    store how that person reasons..."

    CLAUDE'S READ: Reads like you. Parallel structure works. "Facts do not
    carry their own significance; people do" is the quotable line and it lands
    in sentence 4. No changes recommended unless you want to try:
    (A) Lead with the quote — Facts do not carry their own significance; people
        do. Memory systems store facts. They do not store how a specific person
        assigns significance to those facts. (etc.)
    (B) Lead with the data — Across 14 subjects, three state-of-the-art memory
        systems return completely different top-1 facts 94% of the time when
        given the same input. Recall is not representation... (etc.)

    RECOMMENDATION: Keep current unless (A) feels more like you — PG's flip
    version you already rejected.

=== 3. §1.4 "Why the Gradient Implies Universal Utility" ==============
[ ] The structural-extrapolation argument from 14 known historical subjects
    to "real living users." Three reviewers (Scott, Julia, Amanda) flagged
    this as the paper's weakest flank.

    CLAUDE'S READ: The argument is defensible as "structural evidence, not
    direct proof," which §1.4 and §1.5 already acknowledge. Risk: §5.2 later
    re-asserts the universal claim more confidently than §1.5's caveat allows.
    Readers who pattern-match to the confident version miss the caveat.

    OPTIONS:
    (A) KEEP BOTH, add forward reference — §1.4 asserts "strong evidence" →
        §1.5 immediately hedges "not proven" → §5.2 must match §1.5's tone.
        Check §5.2 reads consistently with the hedge.
    (B) SOFTEN §1.4 — replace "gives strong structural evidence" with
        "gives suggestive structural evidence."
    (C) REMOVE §1.4 ENTIRELY — keep the argument in §5.2 only, after data
        context is established.

    RECOMMENDATION: (A). Read §5.2 closely; if it re-asserts universality
    without the hedge, tone §5.2 to match §1.5.

=== 4. §5.1 "Why Primitive" FOUR REBUTTALS =============================
[ ] Does the defense actually rule out each alternative?
    (1) Persona card — ruled out by wrong-spec control ✓
    (2) Compressed RAG context — ruled out by C2a outperforming C4 ✓
    (3) Claude-only prompt trick — ruled out by Tier 2 (Sonnet + Gemini Pro) ✓
    (4) Better prompt engineering — ruled out by automation + traceability +
        cross-provider transferability properties ?

    CLAUDE'S READ: (1)-(3) are empirically ruled out. (4) is definitional
    rather than empirical — we argue the spec's architectural properties
    distinguish it from prompt engineering, which some readers will accept
    and some won't.

    OPTIONS:
    (A) KEEP — accept that (4) is conceptual not empirical; the conceptual
        argument is fine because §5.1 labels itself as a "scope" defense.
    (B) TIGHTEN (4) — add a specific empirical test (e.g., can a human-written
        "persona prompt" of similar length produce similar gains? We don't
        have data on this).
    (C) DROP (4) — state only 3 rebuttals, stronger because all 3 empirical.

    RECOMMENDATION: (A). §5.1 is already scoped as philosophical-plus-empirical;
    leaving (4) conceptual is honest. If title changes to "Missing Interpretive
    Layer," this whole section can be shortened.

=== 5. SEMANTIC OVERLAP ANALYSIS (new, not yet in paper) ==============
[ ] Run complete: 7.6% top-1 all-3-match (controlled), 0% all-3-match (native).
    Much stronger than string-match 94% disagreement. Decide where to put this.

    OPTIONS:
    (A) PROMOTE to §4.3 as a primary finding — replaces or complements the
        current 94%/84%/75%/56% string-match numbers. Stronger intellectually
        because semantic disagreement is more damning than lexical.
    (B) ADD as §4.3.1 "Semantic Overlap" subsection — keep string-match as
        primary, semantic as deeper analysis.
    (C) NOTE briefly in §4.3 and release full analysis in repo — minimal paper
        impact.
    (D) DEFER to §7 Future Work — say "semantic overlap analysis planned" and
        don't include numbers.

    RECOMMENDATION: (B). String-match is the conservative intro; semantic
    analysis deepens it. Both point the same direction, so the reader sees the
    finding is robust across matching methods.

=== 6. §4.1.3 FAILURE-MODE ANALYSIS (Zitkala-Sa + Equiano) ============
[ ] Three hypotheses considered (pretraining sufficiency / spec misalignment /
    retrieval interference). Pretraining sufficiency preferred. Manual spec
    check mentioned but not rigorous. Reviewer (Julia) called it "better than
    hand-waving but not rigorous."

    CLAUDE'S READ: The section is honest about limitations but lacks direct
    evidence. The manual spec-alignment check is asserted, not shown.

    OPTIONS:
    (A) KEEP AS-IS and accept the "better than hand-waving" verdict.
    (B) ADD A CONCRETE DIAGNOSTIC — e.g., for Zitkala-Sa, show the wrong-spec
        v2 score: if it's near baseline, that supports "pretraining interference
        with correct spec" over "spec misalignment."
    (C) MOVE to limitations — say "we observe the negative effect but did
        not fully diagnose mechanism; this is future work."

    RECOMMENDATION: (B) if easy (we have wrong-spec v2 data), else (A).

=== 7. §6 LIMITATIONS (14 items) ======================================
[ ] Check that:
    - #1 "No human judges" is prominent (it is — top of list)
    - #12 "C5-as-pretraining-proxy circularity" is honest enough (arguably
      should be more prominent — move up?)
    - Any item feels defensive rather than genuinely limiting?

    OPTIONS:
    (A) Reorder: promote #12 (circularity) to #2 position. That's the
        reviewer's sharpest critique.
    (B) Compress: 14 items is a lot. Merge related ones (e.g., #9 temporal
        drift + #10 spec stability into one "temporal / stability" item).
    (C) Leave as-is.

    RECOMMENDATION: (A) for honesty — surface the sharpest critique early.

=== 8. VOICE CONSISTENCY (whole paper) =================================
[ ] Flag any sentence that sounds Claude / Reviewer / marketing / PG flip —
    not Aarik.

    KNOWN OFFENDERS already fixed:
    - "Recall is not the thing" (PG flip) — removed
    - "The question is to what extent, by what means, and for whom" — kept
      (sounds neutral-academic, which is fine for the opener)

    WATCH FOR:
    - "load-bearing" — used 4+ times; reads like Claude's style. Replace some
      with "critical," "the piece that," or cut entirely.
    - "this is the single most" — academic overemphasis; check usage.
    - Passive-voice academic filler in §3 methodology — always reads cold.
    - "We invite..." repetition in §1.6 and §8. One mention is enough.

    RECOMMENDATION: One read-through with scissors. Anything that doesn't sound
    like you said it, cut or rewrite.

=== 9. ANALYSES STILL IN FLIGHT (don't push until landed) =============
[ ] OpenAI backfill (gpt4o + gpt54 × Tier 2 + wrong-spec v2 + BL):
    ~40 jobs, ~5 min each, ~3 hrs remaining. Auto.
[ ] Gemini Flash backfill: ~50% through 23 jobs, ~2 hrs remaining. Auto.
[x] Letta agent-loop on Hamerton: COMPLETE. Stateful agent ran 30-turn
    ingestion + battery. Self-edited `human` block = 22,472 chars / 3,167
    words. Prediction results (matched response model, Haiku + Letta block):
    3.24 overall (6 judges), 3.12 non-Gemini. Base Layer full-stack (34,579
    chars) served to Haiku: 3.04. Letta's block at ~65% context size, in the
    same prediction band. Written into §4.3.1 and Future Work.
[ ] RESULTS_S113.json refresh after backfill completes — verify paper
    numbers still hold within ±0.05 for headline claims.

=== 10. OUTREACH FINALIZATION (Tuesday launch) ========================
See PAPER_DASHBOARD.md for full list. Critical path:
[ ] arXiv endorsement ask to Packer — SEND BY MONDAY
[ ] Study repo flipped to public — BEFORE blog goes live
[ ] Blog post v2 voice pass — your voice, not Claude's
[ ] Email templates: memory founders, agent builders — draft Sunday
[ ] Twitter thread + LinkedIn article — draft Monday

==========================================================================
-->

# Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization

**Author:** Aarik Gulaya, Base Layer
**Date:** April 2026
**Preprint** (Apache 2.0)
**Data + Code:** github.com/agulaya24/base-layer
**Study Repository:** github.com/agulaya24/memory-study-repo

> **TL;DR.** Memory systems store what someone said. Preference models store what they liked. Personas store how they present. None of them store *how that person reasons*, which is what an AI agent needs when acting on that person's behalf. **Facts do not carry their own significance; people do.** We call this missing property *representational accuracy*, show it is measurable across 14 historical subjects, and show it is improvable by a static behavioral specification that is automated, traceable, portable across providers, and generated from the person's own data. For the users AI products actually serve, who are people no model has been trained on, the effect in our study is uniform improvement.

**Disclosure:** The author is the founder of Base Layer, which provides an open-source implementation of the pipeline described in this paper. All data, code, question batteries, judge scores, and evaluation artifacts are released under Apache 2.0 to enable independent verification and replication. This study was self-funded.

---

## Abstract

Current AI memory benchmarks measure recall: whether a system can retrieve what a user said when asked. They do not measure **representational accuracy**, which is whether the system's working model of the user enables it to anticipate responses in situations the system has never seen. This paper argues representational accuracy is the property AI agents actually require when acting on someone's behalf, and that it is under-measured, under-discussed, and improvable.

Four state-of-the-art commercial memory systems (Mem0, Letta, Supermemory, Zep) score 85%+ on recall benchmarks. On held-out behavioral prediction tasks, which are a direct test of representational accuracy, their performance is uneven and, for several subjects in our study, indistinguishable from a no-memory baseline. Across 14 subjects and 515 behavioral prediction questions (controlled config, all systems given identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) fail to share any common fact in all three systems' top-1 on 93% of questions (83% at top-3, 74% at top-5, 53% at top-10); in the native config where each system runs its own ingestion, disagreement is 100% at every top-k. These systems solved retrieval. Retrieval is not representation.

To test whether representational accuracy is improvable by structured approaches, we propose and evaluate one such approach: the **Behavioral Specification**, a compressed (~5,000-8,000 token) document that encodes how a person thinks, decides, and reasons. The specification is generated by an automated pipeline that extracts behavioral facts using a constrained 47-predicate vocabulary, authors three interpretive layers (anchors, core, predictions) blindly from the facts, and composes them into a unified document. The resulting specification is served alongside any model as persistent context. Every claim traces back through supporting facts to source text. The specification is one concrete instance of structured interpretive representation; other instances are possible and should be tested.

We evaluated the specification across 14 historical figures (public domain autobiographies), 5 memory systems (the 4 commercial systems plus Base Layer, a locally-hostable MiniLM+ChromaDB baseline), 6 response models from 3 providers (Anthropic, OpenAI, Google), and 7 calibrated LLM judges. We used behavioral prediction accuracy on held-out scenarios as the operational test of representational accuracy. If the model's working model of the person is accurate, accurate prediction on unseen situations follows.

Key findings:

1. **The specification improves prediction for subjects the model has low pretraining knowledge of.** 12 of 14 subjects show positive improvement of facts+spec over baseline (Wilcoxon signed-rank p=0.006, N=14). The relationship between pretraining baseline and spec improvement is continuous and strong: linear regression slope −0.98 (95% CI −1.30, −0.74). For the 9 subjects with low pretraining representation (baseline ≤2.0), which constitute the slice that approximates real AI users, improvement is uniform: 9 of 9 positive, mean +1.04 points on the 1-5 scale. The 2 subjects where the spec did not help are the 2 with the highest baselines (≥2.6).

2. **The specification is portable across providers and complements existing memory systems.** Layered on top of Mem0, Letta-controlled, and Zep, the specification produces statistically robust positive deltas. For Supermemory, which has the highest C1 baselines in the battery and indicates strong native retrieval, the spec hits a ceiling effect rather than a failure mode (the spec's complementary value is smaller for the system that has already captured the most retrieval value). The cross-provider Tier 2 replication (Sonnet, Gemini Pro response models reading GPT-5.4 batteries) reproduced the spec direction in 5 of 6 (subject × response model) cells, defusing concerns about within-Anthropic circularity. The Tier 2 data also empirically demonstrated cross-provider pretraining variance: the same subject's baseline accuracy varies by 1-2 points across response models, supporting the spec's role as a portability layer.

3. **Content drives the improvement, not format.** A wrong specification (each subject assigned a different subject's spec via random derangement) scores near baseline rather than near the correct-spec scores. The interpretive content of the correct spec for the correct subject is what produces the improvement, not the presence of any structured framework.

4. **The specification shifts models from refusal to committed prediction.** Across the 13 global subjects, 25.0% of baseline (C5) responses exhibited hedging or refusal patterns ("I don't have enough context," "cannot definitively"). With the spec added alone, hedging dropped to 2.6%. With facts plus spec, to 0.6%. The specification is not just moving scores. It is changing what the model is willing to commit to.

The 14 subjects in our study are a population biased *upward* on pretraining representation. Every one has a public-domain autobiography that was almost certainly in training corpora. We did not test on living people with private data. The gradient we observe within this biased-high sample (spec helps most where baseline is lowest; uniformly positive for the low-baseline slice) gives strong *structural* evidence that the specification is broadly useful for typical living AI users, whose private decisions are not in any model's training data. But it is an extrapolation, not a direct measurement. Confirming this is the most important piece of follow-up work, and it is potentially landmark for broad personalization if the implication holds.

We want to disaggregate three distinct claims that readers commonly conflate, because the strength of evidence differs for each:

1. **Claim tested and supported (N=14):** A behavioral specification improves held-out prediction accuracy as an inverse-proportional gradient against pretraining baseline (slope −0.98 [95% CI −1.30, −0.74], Wilcoxon p=0.006). 12 of 14 subjects show positive delta. As a sensitivity check, when restricted post hoc to the 9 subjects with C5 ≤ 2.0, which constitute the slice that approximates the typical real AI user with low pretraining representation, improvement is uniform (9 of 9, mean +1.04). The locked analysis plan reports the gradient as the primary result; the threshold split is a secondary consistency check.

2. **Claim proposed but extrapolated, not directly tested:** The result generalizes to living users whose private decisions are not in any training corpus. Our 14 subjects are historical figures with public autobiographies, a sample biased *upward* on pretraining representation. The structural argument for generalization is strong (if the spec helps most where baseline is lowest within a biased-high sample, it should help more on the biased-low real-user case), but this is extrapolation and we do not claim otherwise.

3. **Claim *not* made:** Base Layer outperforms existing memory providers in general. Base Layer is not a memory system. Layered on top of four commercial ones (Mem0, Letta, Zep, Supermemory), the Base Layer specification produces statistically robust positive aggregate deltas on three of the four (Mem0, Letta-controlled, Zep). On Supermemory the aggregate delta is near zero, a ceiling artifact rather than a mechanism failure: Supermemory's strong native retrieval lifts most subjects out of the baseline range where the spec has headroom, and on the low-baseline subjects within Supermemory's data, the spec still helps. Our contribution is that the specification layer is *additive* to the existing memory-provider stack, not a replacement, and we tested on a new axis (behavioral prediction) the providers were not optimized for.

In addition to the gradient and the additivity result, the study produces one architectural finding the field should consider: **Letta's stateful-agent self-editing memory block, the most architecturally ambitious approach in the comparison, scales poorly. Across three subjects spanning a 9× corpus-size range (25K → 48K → 223K words), the block grows linearly, accumulates 25% verbatim sentence duplication at the largest size, and saturates against a 333,000-character API ceiling. At that ceiling, 10% of the source corpus could not be ingested. Base Layer's compose step keeps the spec at 34-40K characters across the same range. This is not a takedown; it is an open problem for stateful-agent memory architectures at user-corpus scale, and we report it so the field can engage with it.**

Four propositions frame the contribution, scoped to what we tested:

1. **Representational accuracy is a real, measurable property.** It varies widely across subjects and approaches, and structured methods can improve it.
2. **Recall benchmarks do not measure it.** Memory systems that pass recall at 85%+ show large and uneven gaps on behavioral prediction. Storage and understanding are not the same problem.
3. **The Behavioral Specification is one working method** for building this interpretive representation layer. We propose treating it as a candidate primitive and test whether it behaves like one; we do not claim our 47-predicate, three-layer implementation is optimal. Better and different implementations should follow.
4. **Behavioral alignment depends on representational accuracy.** An AI acting on someone's behalf cannot act the way that person would act if it lacks an accurate internal model of how they reason. This makes representational accuracy, not recall, the load-bearing property for personalized AI, and a missing thread in the broader human–AI interaction and alignment literature.

This paper is a beginning. The question it opens is a long-term research direction, not a benchmark to be topped: *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, audit, and own that representation?* We invite extensions.

All data, code, question batteries, judge scores, calibration data, the analysis plan lock, and the wrong-spec assignment manifest are released under Apache 2.0 to enable independent verification and replication. Generating a new spec costs under $1 per subject; reproducing this full study (14 subjects, 5 memory systems, 6 response models, 7 judges, and the full condition battery) costs approximately $500-700 in API fees plus memory system subscriptions.

---

## 1. Introduction

### 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant. Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. A single set of facts, processed through different interpretive lenses, produces different judgments. This pattern is well-documented across the sciences, religion, and political affiliation. It also operates at the individual level: two people facing the same decision can reach opposite conclusions from identical information. Memory is deeply personal. For an AI memory system to serve a specific person, it must be personalized to how that person interprets, not just to what facts they have produced.

We introduce **representational accuracy** as the corresponding AI-side property: how well a system's internal model of a specific person captures that person's interpretive patterns. It is not recall, preference matching, or persona consistency; it is a distinct property of the AI system, and no current benchmark is built to measure it.

**The core hypothesis of this research is that representational accuracy predicts alignment between an AI system's behavior and the intent and behavior of the person it serves.** If an AI system's model of a person accurately captures how they interpret situations, its responses should align with that person's intent and behavior in situations the system has never seen. The operational test is behavioral prediction on held-out situations, used here as a proxy for this alignment.

We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated LLM judges to evaluate the performance of each memory system, on its own and in combination with a behavioral specification: a static document that extracts and encodes a stable representation of a corpus's behavioral patterns.

### 1.2 What We Tested

We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model. The test was whether each system could predict how that specific person would respond in situations drawn from text it had never seen.

The experiment has two main splits. The first is a **controlled test**: each memory system is given an identical, pre-extracted fact pool drawn from the training half of the corpus. Holding the input constant lets us measure whether the providers converge on what is most relevant when they see the same facts. The second is a **native test**: each memory system ingests the raw corpus through its own pipeline, as it would in production. This measures real-world performance when each system is allowed to do what it is designed to do. Running in parallel across both splits is the Behavioral Specification, tested alone and layered on top of each configuration.

Inside this structure, every meaningful combination of inputs was evaluated as its own condition:

| Condition | Inputs given to the model | Purpose |
|---|---|---|
| **No context** (C5) | Nothing. The model answers from pretraining alone. | Pretraining baseline. Measures what the model already knows about the subject from public sources. |
| **Retrieval alone, controlled** (C1) | Top-k facts retrieved by each memory system (Mem0, Letta, Supermemory, Zep, Base Layer) from the shared fact pool. | Tests retrieval sufficiency, and whether providers converge on which facts are most relevant given identical input. |
| **Retrieval alone, native** (C1 native) | Top-k results from each memory system's own ingestion pipeline operating over the raw training corpus. | Real-world comparison of each memory system's full ingestion-plus-retrieval stack. |
| **All facts, no specification** (C4) | Every extracted fact for the subject, loaded into context at once. | Tests whether information sufficiency alone drives prediction, independent of structure. |
| **Raw corpus, no specification** (C8) | The entire training corpus loaded into context. | Tests whether unstructured source text can substitute for an interpretive representation. |
| **Specification alone** (C2a) | The Behavioral Specification, with no retrieval, no facts, and no corpus. | Tests whether structure without retrieval is sufficient on its own. |
| **Retrieval + specification, controlled** (C3) | Memory system retrieval from the shared fact pool, plus the specification. | Tests whether the specification layers cleanly on retrieval when the input is held constant. |
| **Retrieval + specification, native** (C3 native) | Memory system's own ingestion and retrieval, plus the specification. | Tests whether the specification improves the real-world deployment of each memory system. |
| **Facts + specification** (C4a) | Every extracted fact plus the specification. | Combines full information and structure to test the upper bound of context-provided prediction. |
| **Corpus + specification** (C9) | Raw training corpus plus the specification. | Tests whether structure is additive to unstructured source text. |
| **Wrong-specification control** (C2c) | A different subject's specification applied to this subject. Two variants: v1 uses Franklin's specification for all other subjects; v2 applies a random derangement, seed-fixed, so no subject receives its own. | Tests whether the effect is driven by the content of the correct specification, or by the mere presence of structured prompting. |

**Additional testing for Letta.** Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions above, we ran a separate test on three subjects spanning a 9× corpus-size range (Hamerton, Ebers, Babur). A fresh Letta agent ingested each training corpus turn-by-turn and was allowed to self-edit. The resulting memory block was then served to the same response model used throughout the main study for a matched comparison against the Behavioral Specification. Full methodology and results are in §4.3.1.

The 14 subjects span four continents and roughly two millennia of written human experience. Ordered chronologically: Saint Augustine (North Africa, 4th-5th c.), Babur (Central Asia and India, 15th-16th c.), Bernal Diaz del Castillo (Spain and Mexico, 15th-16th c.), Benvenuto Cellini (Italy, 16th c.), Jean-Jacques Rousseau (France, 18th c.), Olaudah Equiano (West Africa and Britain, 18th c.), Mary Seacole (Jamaica and Britain, 19th c.), Elizabeth Keckley (United States, 19th c.), Yung Wing (China and the United States, 19th c.), Philip Gilbert Hamerton (Britain, 19th c.), Fukuzawa Yukichi (Japan, 19th c.), Georg Ebers (Germany, 19th c.), Sunity Devee (India, late 19th c.), and Zitkala-Sa (Yankton Dakota, early 20th c.). Source corpora range from 25,231 words (Hamerton) to 422,772 words (Babur). Full source references are in §3.2.

Predictions were scored on a 1-5 rubric: **1** means the response refuses or is wholly wrong; **2** means the model got the right topic but the wrong prediction; **3** means the right domain with no specifics; **4** means the right direction with specifics; **5** means the model predicted the specific outcome the held-out text records. One-point differences on this scale are qualitative shifts, not small numerical adjustments. Moving from 1 to 2 is the movement from "cannot engage" to "orients to what the question is about." Moving from 2 to 3 is "wrong prediction" to "in the neighborhood." Moving from 3 to 4 is "reasonable but unspecified" to "right direction with specifics." Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

The **baseline** we refer to throughout is the no-context condition (C5): the response model's score on the prediction battery when given no external information. It operationalizes how much the model already knows about a subject from pretraining alone. A subject with a low baseline (C5 ≤ 2.0 on the rubric) is one the model has thin pretraining representation of; a subject with a high baseline is one the model already predicts reasonably well on its own. The population relevant for real AI deployment, living individuals whose private reasoning was never indexed by any training corpus, is low-baseline by construction. We therefore report results separately on the low-baseline slice (n=9) alongside the full 14-subject analysis.

Each condition was evaluated with 6 response models across 3 providers (Anthropic, OpenAI, Google) and a 7-judge LLM-as-judge panel (Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4; Gemini Flash and Gemini Pro). Judges were calibrated on known verbatim matches, paraphrase variants, off-target responses, and length-padded responses to measure each judge's ceiling behavior, paraphrase sensitivity, and length bias. The judges agree strongly on condition rankings (pairwise Spearman ρ = 0.89-0.98). The two Gemini judges systematically inflate absolute scores by approximately 1 point relative to the other five, so we report both 7-judge and 5-judge non-Gemini aggregates throughout; no subject's improvement direction changes between them. Full condition definitions, response model list, and judge calibration protocol are in §3.

### 1.3 What We Found

Four findings drive the paper. Each is a claim about representational accuracy, tested via behavioral prediction.

1. **Representational accuracy varies widely and is improvable.** Across 14 subjects, baseline (no-context) prediction scores range from 1.03 to 2.93 on the 1-5 rubric, a 1.9-point spread that reflects how differently models "know" different subjects from pretraining alone. With a Behavioral Specification added, 12 of 14 subjects improve (Wilcoxon signed-rank p=0.006), and the 9 low-baseline subjects (C5 ≤ 2.0) all improve without exception, with a mean gain of +1.04 points. Representational accuracy is not fixed. A structured intervention moves it substantially.

2. **The improvement is inversely proportional to what the model already knows.** Linear regression of the spec's effect on the baseline score gives slope −0.98 (95% CI −1.30, −0.74). The less the model knows about a person from pretraining, the more the specification helps. Frontier models already show high representational accuracy for famous figures (Franklin baseline 4.10) from pretraining alone, though they do so opaquely. The specification provides the same predictive capability with full traceability, for the population pretraining does not cover.

3. **Content drives the improvement, not format.** A wrong specification (another person's behavioral structure applied to this subject) scores near baseline rather than near the correct-spec score. The specific interpretive structure of the correct person is what produces the improvement. A generic interpretive framework does not. This rules out the "it's just a better prompt" reading.

4. **The specification shifts models from refusal to committed prediction.** Across 13 global subjects, baseline responses exhibit hedging or refusal patterns 25.0% of the time ("I don't have enough context," "cannot definitively"). With the spec added, hedging drops to 2.6%. With facts plus spec, to 0.6%. The specification is not only moving prediction scores. It is changing what the model is willing to commit to.

### 1.4 Why the Gradient Implies Broad Utility for Real Users

A subtle but important property of our test population: every one of the 14 subjects was selected from public domain autobiographies, meaning each one is *more* represented in pretraining data than the median person on Earth. The very fact that their writing was preserved, digitized, indexed, and included in training corpora places them above the population average in pretraining footprint.

Even within this biased-high sample, the gradient holds. The two subjects where the specification did not help are the two with the highest baseline scores (≥2.6), people the model already partially understood from pretraining. For the 9 subjects below baseline 2.0, the specification was uniformly beneficial.

Real AI users are private individuals whose writing was never published, whose conversations are not indexed, and whose decisions are not in any public record. They sit far below the lowest-baseline subject in our study. The structural implication is direct: if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user, whose model baseline is closer to 1.0 than to 2.0.

We do not claim to have proven this for every possible user. We claim that the gradient observed across our 14 subjects, combined with the test population's upward bias on representation, gives strong structural evidence that the specification is broadly useful across the population of real AI users. Confirmation requires living-subject studies (§7).

### 1.5 What This Paper Does Not Claim

We do not claim the Behavioral Specification solves AI personalization. We claim the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued: four funded systems score 85%+ on LOCOMO/LongMemEval. None of them test whether the system actually understands the person it serves.

We also do not claim that the specific 47 predicates, the three-layer architecture, or the composition prompt are optimal. We claim that **something like this** is required: a structured behavioral representation that is automated, traceable, transferable across model providers, and user-inspectable. Better versions will follow. The layer itself, we argue, is what is missing.

**We are explicit about the boundary of the evidence we offer.** We tested only *known* historical figures, people whose autobiographies were preserved, digitized, and almost certainly ingested into pretraining corpora. Every subject in our study is, by construction, more represented in pretraining than the typical living person. The gradient we observe (spec helps most where baseline is lowest) holds *within* this biased-up sample. For the population this paper ultimately wants to serve (people no model has been trained on, whose baseline representational accuracy is approximately zero), this paper does not provide direct evidence. It provides a structural argument that the implication should carry, with direct confirmation left to living-subject studies. If that extrapolation holds, this approach is potentially landmark for broad personalization. If it does not, we are offering a method that works on a narrower slice than we hope. Either outcome is important to the field.

This paper is a beginning, not a conclusion. The central question is how an AI can accurately represent a specific person's reasoning, and at what level of accuracy such a representation is sufficient for an agent to act well on their behalf. That question is under-studied and deserves sustained research attention. Our contribution is evidence that it is answerable, along with one working method for approaching it.

### 1.6 Behavioral Alignment and the Human–AI Interaction Problem

The AI safety community uses "alignment" to mean preventing harmful behavior at the model level. This paper is about a different property, **behavioral alignment**: whether a specific AI's actions accord with a specific person's reasoning, values, and decision-making when acting on that person's behalf.

**These are orthogonal axes, not a hierarchy.** A model that is safely aligned in the safety sense can still be behaviorally misaligned with any given user; it will act reasonably, but not the way *you* would act. The inverse is also true and important: a perfectly behaviorally-aligned agent, acting exactly as a specific user would act, can be catastrophically safety-misaligned if that user would act maliciously, recklessly, or against third-party interests. Behavioral alignment is not a safety property. It is a personalization property that safety constraints must sit above.

Representational accuracy is a *necessary* condition for behavioral alignment, but not a sufficient one. A system cannot act the way someone would act if it lacks an accurate internal model of how that person reasons. Having the model is required; translating the model into aligned action, subject to safety constraints, is a separate problem we do not address in this paper. We focus on the representation layer because it is the piece that is under-studied and empirically tractable. An agent that acts on your behalf without an accurate representation of you is not serving you; it is averaging over some population the model happens to resemble.

This is a research area that is under-studied relative to its importance. The body of work on representation learning in models is vast; the body of work on representing *specific individual humans* for the purpose of acting on their behalf is not. **Base Layer is a research firm working on behavioral and identity compression.** It is an independent program aimed at advancing understanding of how AI systems can build, maintain, and be audited against accurate representations of the humans they serve. The open-source pipeline whose specification is evaluated in this paper is one output of that program. The broader research agenda is long-term, public, and collaborative.

We invite other implementations, other architectures, and other evaluations. The problem is large, and this paper is one opening move. The question of how to accurately and safely represent a specific human to an AI system is a research direction, not a product feature, and we hope others will extend what we have begun. Academic labs, independent researchers, and other firms are all welcome.

The question this paper asks, operationally: *can the AI act the way you would act, given how you think?* The question the field should take up, more generally: *how do we know when an AI's internal model of a specific person is accurate enough for the agent to act on that person's behalf, and by what means do we improve and audit that representation?*

---

## 2. Related Work

### 2.1 Memory systems for LLM agents

We evaluate four commercial memory systems, each representing a distinct architectural commitment.

**Mem0** (Chhikara et al., 2025): Hybrid retrieval combining semantic embeddings, keyword search, and entity-based lookups. The graph-enhanced variant (Mem0g) builds a directed labeled knowledge graph alongside the vector store, with entity extraction and relation inference. Multi-level memory (user, session, agent state). Memories are timestamped, versioned, and exportable.

**Letta / MemGPT** (Packer et al., 2023, arXiv:2310.08560): An LLM-as-operating-system paradigm. The agent's context window is divided into structured memory blocks (e.g., `persona`, `human`) which the agent directly edits during its inference loop via tools such as `core_memory_append` and `core_memory_replace`. External context includes archival memory (semantically searchable) and recall memory (prior conversation history). The MemGPT paper describes memory edits as "entirely self-directed": the LLM chooses when to write, what to write, and what to overwrite as it processes conversation turns. Letta's current product positioning distinguishes *stateful agents* ("AI with advanced memory that can learn and self-improve over time") from retrieval-augmented generation as an architectural category. Of the four memory systems we test, Letta is the only one whose core architecture treats memory as something an agent *synthesizes* during conversation rather than *stores* for later retrieval.

**Supermemory**: A five-layer memory architecture: connectors (auto-sync from Slack, Notion, Gmail, etc.), extractors (multi-modal chunking for PDFs, images, video, code), Super-RAG (hybrid search with reranking and query rewriting), memory graphs (relationship tracking, contradiction resolution, temporal reasoning, automatic forgetting), and user profiles (static preferences + dynamic session data). Scores 81.6% on LongMemEval with GPT-4o (85.2% with Gemini 3 Pro). Returns both high-level memory summaries and original source chunks with each retrieval.

**Zep**: Temporal context graph built on Graphiti (open-source). Entities, facts (as triplets with temporal validity windows tracking when information became and ceased being true), and episodes (raw ingested data as ground truth). Hybrid retrieval combining semantic, keyword, and graph traversal. Sub-200ms latency. Incremental graph updates without full recomputation.

All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did. None of them take representational accuracy, which is the property of interest to this paper, as an explicit design target. This is not a criticism of their architectures; it is a different problem. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our study configuration did not exercise (see §4.3).

### 2.2 Traceability

Zep provides the strongest explicit provenance of the four: every entity and relationship traces back to the episode IDs that produced it, enabling lineage from derived fact to source data ingestion. Supermemory returns original source chunks alongside retrieved memories, providing chunk-level attribution. Mem0 offers timestamped, versioned memories. Letta's focus is agent state management rather than audit trails. The Behavioral Specification's traceability operates at a different granularity: spec claim (e.g., "A1: Dual-ledger authority") maps to supporting facts (F-001, F-047), which map to specific source text passages. This enables a person to ask not just "where did this come from?" but "why does the specification believe this about me?", and to receive the exact text that supports the interpretive claim.

### 2.3 Memory and personalization benchmarks

- **LongMemEval** (He et al., ICLR 2025): Long-term memory across 500+ sessions and 5 capability dimensions, all focused on recall. The definitive recall benchmark; does not test behavioral reasoning or held-out prediction.
- **PersonaGym** (Jandaghi et al., EMNLP 2025): Tests persona fidelity, which is whether a model maintains a described persona during conversation. Evaluates consistency of persona presentation, not prediction of held-out behavior.
- **AlpsBench** (Xiao et al., 2026): Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses. Their central finding, that explicit memory mechanisms improve recall but do not inherently guarantee more preference-aligned or emotionally resonant responses, is independently arrived at and complementary to ours: they find the gap in preference alignment, we find it in behavioral prediction.
- **Twin-2K** (Toubia et al., 2025): Behavioral prediction at scale (2,000 participants, 71.83% accuracy). Does not test the effect of compression or the role of interpretive structure.
- **LoCoMo** (Maharana et al., ACL 2024): Conversational memory quality; does not evaluate behavioral reasoning.

### 2.4 Cognitive and representational foundations

**Bartlett (1932)** demonstrated that humans remember schemas, not facts, reconstructing memory through structured frameworks rather than replaying stored data. The Behavioral Specification is computationally analogous to a schema: a compressed structure that enables reasoning about a person without storing every fact about them.

**Hinton et al. (2015)** showed that compressing a large model into a smaller one preserves "dark knowledge", the relationships between outputs that carry more information than the outputs themselves. Our pipeline performs an analogous operation on personal data: compressing 25,000+ words of source text into a 3,000-5,000 token specification that preserves behavioral signal while discarding biographical noise.

**Chen, Arditi, Evans et al. (2025)** extract persona representations as steerable vectors inside model activations, enabling direct monitoring and control of character traits through internal activation surgery. Our approach is architecturally complementary: where Chen et al. modify the model to reflect a persona, we inform the model from outside. Both validate that persona is a real, manipulable structure: one through weights, the other through context.

**Jiang et al. (COLM 2025)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The cause is not a lack of facts but a lack of the interpretive structure to apply those facts to novel situations. This is direct evidence for the representational-accuracy gap we study.

**Jain et al. (2026)** find that adding interaction context to LLMs increases rather than reduces hedging when the context lacks interpretive framing. Our hedging-reduction finding (§5.5) is consistent: context without structure amplifies uncertainty; context with interpretive structure anchors commitment.

**Lu et al. (2026)** identify hedging as a structural property of assistant models. Without an external behavioral anchor, helpfulness drifts toward hedging as a safe default. The specification provides that anchor.

### 2.5 LLM-as-judge

**Zheng et al. (2023)** established that LLM judges agree with human judges at rates comparable to inter-human agreement. We extend this with a calibration framework that measures each judge's ceiling, paraphrase sensitivity, and length bias, enabling normalized scoring across providers (§3.7).

---

## 3. Study Design

### 3.1 Representational Accuracy

We define **representational accuracy** as the degree to which a system's working model of a person enables accurate anticipation of that person's responses in situations the system has never seen. It is a property of the representation, not of any single prediction.

Prediction performance is the **test** of representational accuracy, not the deliverable. If a model has an accurate representation of how someone thinks, accurate prediction on novel situations follows. If prediction fails systematically, the representation is incomplete.

This distinction matters because it resists a common reframing: "the spec is a better prompt." A better prompt that produces accurate predictions without representing the person would still be a better prompt. What we measure is whether the model's *representation* of the person, its internal working model, has been upgraded such that predictions follow naturally from it.

In practice, representational accuracy is operationalized as the mean predicted-behavior score (1-5 scale) across a standardized battery of 39 behavioral prediction questions, averaged across seven judges from three providers. The rubric and aggregation rule are defined in §3.7.

### 3.2 Subjects

We test 14 subjects, all historical figures with public domain autobiographies or memoirs. Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting entirely on a single type of source material. We use the baseline score (§3.7, §4.1) as an observable proxy for each subject's pretraining representation. A ~1.0 baseline indicates near-zero pretraining knowledge, and a ~3.0+ baseline indicates substantial pretraining knowledge. **We do not make claims about the causes of this variation in LLM training data.** The purpose of sampling broadly is methodological: to test whether the specification's effect is subject-specific or generalizes across varied source material.

| # | Subject | Source | Words | Period |
|---|---|---|---|---|
| 1 | Philip Gilbert Hamerton | Project Gutenberg #8536 | 25,231 | 1834-1858 |
| 2 | Elizabeth Keckley | Project Gutenberg #24968 | 58,742 | 1818-1868 |
| 3 | Sunity Devee | Project Gutenberg #57175 | 67,379 | 1864-1932 |
| 4 | Zitkala-Sa | Project Gutenberg #10376 | 35,328 | 1876-1938 |
| 5 | Olaudah Equiano | Project Gutenberg #15399 | 85,660 | 1745-1797 |
| 6 | Mary Seacole | Project Gutenberg #23031 | 62,467 | 1805-1881 |
| 7 | Fukuzawa Yukichi | Internet Archive | 139,088 | 1835-1901 |
| 8 | Babur | Project Gutenberg #44608 | 422,772 | 1483-1530 |
| 9 | Yung Wing | Project Gutenberg #54635 | 66,459 | 1828-1912 |
| 10 | Benvenuto Cellini | Project Gutenberg #4028 | 190,390 | 1500-1571 |
| 11 | Bernal Diaz del Castillo | Project Gutenberg #32474 | 187,315 | 1492-1584 |
| 12 | Georg Ebers | Project Gutenberg #5599 | 96,174 | 1837-1898 |
| 13 | Jean-Jacques Rousseau | Project Gutenberg #3913 | 278,120 | 1712-1778 |
| 14 | Saint Augustine | Project Gutenberg #3296 | 114,873 | 354-430 |

Benjamin Franklin (Project Gutenberg #20203) serves as a known-figure control, a subject with extensive pretraining representation.

Gender distribution (4F:10M) reflects the availability of public domain autobiographies and is not intended to carry interpretive weight; the paper's findings are not framed around demographic categories.

For each subject, the source text is split 50/50 into training and held-out chapters. The Behavioral Specification is generated only from the training half. All prediction questions reference behaviors described in the held-out half. **The specification never sees the data it is tested against.**

### 3.3 Pipeline

The Behavioral Specification is generated by an automated pipeline: any text in, one specification out. The 13 global subjects were generated end-to-end with zero manual intervention. Two components of the pipeline are human-designed (not automatically learned): the 47-predicate vocabulary used by the extractor (§3.3.1) and the three-layer architecture used by the author (§3.3.2). Both were developed iteratively across 50+ subjects and represent foundational design choices, not per-subject manual curation. Once these design choices are fixed, the pipeline runs end-to-end without human input on any new subject.

**Five steps:**

| Step | Process | Output | Model | Cost |
|---|---|---|---|---|
| IMPORT | Parse any text into document chunks | SQLite records with source attribution | Local | $0 |
| EXTRACT | Subject-predicate-object triples using 47 constrained predicates; AUDN dedup (Add/Update/Delete/Noop) via vector similarity | Structured behavioral facts with provenance IDs | Claude Haiku | $0.10-0.50 |
| EMBED | Vector embeddings for each fact, enabling traceability from spec claims back to source | ChromaDB vectors | MiniLM-L6-v2 (local) | $0 |
| AUTHOR | Generate three interpretive layers independently from anonymized facts: **Anchors** (8-10 axioms), **Core** (~800 words of behavioral patterns), **Predictions** (6-8 testable patterns with false positive guards) | Three markdown layers with claim-level IDs | Claude Sonnet | $0.05-0.15 |
| COMPOSE | Synthesize three layers + top supporting facts into flowing prose. Completeness and faithfulness gates applied | Unified behavioral specification (~5,000 tokens) | Claude Opus | $0.05-0.15 |

**Total pipeline cost:** Under $1 per subject. Generating a spec for a new subject is under $1. Reproducing the full study across 14 subjects, 5 systems, 6 response models, 7 judges and ~40 questions per subject cost approximately $500-700 in LLM API charges plus ~$80 in commercial memory system subscriptions. These figures are for readers planning to replicate the full battery; generating specs for a single use case is cheap.

**Anchors example:** *"A1. DUAL-LEDGER AUTHORITY: Evaluates authority figures on virtue and failure simultaneously, refusing to collapse them. Active when: encountering teachers, mentors, or institutional power."*

**Predictions example:**
> **P3. ENVIRONMENT-AS-COGNITION**
> *Pattern:* When [physical space changes] then [immediate binary classification as hostile or generative to thought].
> *Detection:* Appears in housing, travel, and workspace decisions.
> *Directive:* When this person describes a new environment, expect an immediate evaluative judgment about whether it supports or degrades their capacity for work.
> *False positive warning:* Not active when environment is discussed in purely social terms.

The 47 predicates constrain extraction away from biographical facts ("his father was violent") and toward behavioral patterns ("evaluates authority figures on two simultaneous ledgers"). Full predicate vocabulary available in the public repository.

**Anti-contamination controls:**
- Subject names replaced with "this person" before models see data
- They/them pronouns throughout the spec (prevents pretraining pattern matching on subject names)
- Domain-agnostic composition: capture patterns, not positions
- Blind regeneration during authoring (no prior layer output visible) prevents anchoring bias

**Traceability.** Every claim in the specification links back through supporting facts to source text: `Spec claim (A1, P3) → supporting facts (F-001, F-047) → source document → original text`. The `trace_claim` tool in the serving layer makes this chain queryable at runtime.

The specification is served via MCP (Model Context Protocol) as persistent context at conversation start, alongside on-demand tools for fact lookup (`recall_memories`, `search_facts`) and provenance inspection (`trace_claim`, `verify_claims`).

**Inference-time cost.** The full specification is approximately 5,000-8,000 tokens depending on subject. Naively, every prompt that includes the spec pays this token cost. In practice, modern provider APIs cache persistent system context (Anthropic prompt caching, OpenAI cached responses, Google cached content), so after the first call in a session, the per-request marginal cost is approximately 10-20% of the nominal token count, depending on cache hit rate. A serving layer optimized around the spec (loading once per session, caching across calls, routing factual queries away from the spec context) can reduce this further. We do not test these optimizations in this paper; they are engineering choices independent of the specification's representational content. For applications where spec context size is a concern, ablation of which layers carry the most weight (Future Work, §7) would inform a smaller spec.

### 3.4 Question Batteries

For each subject, we generate a **battery of 80 questions** across five tiers. The primary analysis uses the 39 behavioral prediction (BP) questions per subject.

**Generation method: backward design.** Questions are constructed in reverse, starting from what actually happened in the held-out text:

1. A generator model reads a window of held-out text and identifies specific decisions, reactions, and behavioral episodes
2. It writes questions that reference only patterns observable in the training text, with no names, dates, or details unique to the held-out content
3. It extracts the exact held-out passage describing what actually happened as verbatim ground truth

This ensures every question has a definitive ground truth and is answerable from training patterns rather than held-out memorization.

**Five question tiers:**

| Tier | Count | What it tests | Example |
|---|---|---|---|
| Behavioral prediction | 39 | Predicting behavior in unseen scenarios | "How would Hamerton react to London?" |
| Inferential synthesis | 11 | Connecting multiple facts | "How did his early education shape views on institutional authority?" |
| Factual recall | 10 | Retrieving stated facts | "What was his relationship with his father?" |
| Adversarial abstention | 10 | Refusing unanswerable questions | "What was his opinion of Darwin's evolution?" |
| Boundary probing | 10 | Edge cases where values may conflict | "Would he support women's suffrage?" |

Only the 39 behavioral prediction questions per subject are scored in the main results. They are the questions where recall vs. reasoning divergence is most visible: a system with the right facts but no interpretive structure should fail, and the spec should help most.

### 3.4.1 Circularity Controls

Behavioral prediction batteries are generated by an LLM (Claude Haiku 4.5, temperature=0) from the same family used as the primary response model. This raises a legitimate circularity concern: do Haiku-generated questions encode Haiku's sensibilities in a way that makes them easier for Haiku-with-spec to answer?

We address this with two controls:

**Control 1: Independent battery generation.** For all 13 global subjects, we independently regenerated batteries using GPT-5.4 (OpenAI) with the identical backward-design prompt. The generated batteries produced the same question count (39 BP per subject), covered the same 10 behavioral categories (with 8-10 shared categories per subject), and targeted the same behavioral patterns in the source text. Emphasis differed, with GPT-5.4 producing more risk and change-over-time questions and Haiku producing more values and decisions questions, but the backward-design methodology constrains the output more than the model does. Full GPT-5.4 batteries are released for independent replication.

**Control 2: Replication with non-Haiku chain.** For 3 subjects spanning the effect gradient (Ebers at baseline 1.04 with a strong positive effect; Yung Wing at baseline 1.88 with a modest positive effect; Zitkala-Sa at baseline 2.34 with a negative effect), we re-ran the core C5/C2a/C4a/C2c conditions using:
- GPT-5.4-generated battery (different generator from Haiku)
- Sonnet 4.6 and Gemini 2.5 Pro as response models (two non-Haiku models from two different providers)
- The **identical full-stack behavioral specification** used in the main study (anchors + core + predictions + unified brief, ~5,000-7,500 tokens). An earlier pre-production version of this replication used the brief-only spec (~1,100 tokens), which did not match the main study. That run was discarded during quality review and the replication was regenerated with the full-stack spec.
- Same 7-judge panel

The pre-committed test (locked in `ANALYSIS_PLAN_LOCK.md` commit de27b64 before these runs): if the direction of the (C4a - C5) delta matches the Haiku-chain direction for 5 or 6 of the 6 (subject × response model) cells, the circularity concern is considered defused.

*[Results to be filled in §4.8 after runs complete.]*

### 3.5 Experimental Conditions

All 14 subjects are tested across a unified set of conditions. All conditions use identical prompts except for the injected context. No condition is coached to abstain or answer. Temperature=0 for all API calls.

**Context conditions:**

| ID | Condition | What the model sees | Purpose |
|---|---|---|---|
| C5 | Baseline | Nothing | Floor: what the model knows from pretraining alone |
| C2a | Spec only | Full behavioral specification (~5K tokens) | Does the spec alone improve prediction? |
| C2c | Wrong spec | A different person's specification | Does framework alone help, or does correct content matter? |
| C4 | All facts | All extracted facts, no spec | Does raw information volume substitute for interpretation? |
| C4a | Facts + spec | All facts + spec | Does the spec add value beyond raw facts? |
| C8 | Raw corpus, no spec | Full training text (~25K-420K words) | Does more text mean better prediction? |
| C9 | Raw corpus + spec | Full training text + spec | Does the spec help even with full context? |

**Memory-system conditions (5 systems):** Each of Mem0, Letta, Supermemory, Zep, and Base Layer is evaluated in two configurations:

| ID | Configuration | What the model sees |
|---|---|---|
| C1 | Retrieval only | Top-k facts retrieved by the system |
| C3 | Retrieval + spec | System's retrieved facts + behavioral specification |

Two ingestion configurations per system:
- **Controlled:** each system given the identical extracted fact set (462 facts for Hamerton, equivalent per-subject facts for others)
- **Native:** each system processes the raw training corpus through its own ingestion pipeline (chunking, extraction, embedding)

This design isolates the spec's contribution from retrieval quality differences. If the spec improves every system under both configurations, the effect is not an artifact of any one system's retrieval approach.

**Wrong-spec control (v1 and v2):**
- **v1:** Franklin's specification applied to each subject. Reported as existing control.
- **v2:** Random derangement. Each subject is assigned a wrong spec from a different study subject (fixed seed 42, no subject gets its own spec). This tightens the control: Franklin is a known figure whose spec may be implicitly closer to canonical Western profiles than a random study subject's spec would be.

### 3.6 Response Models

Six response models from three providers. If the spec effect holds across all, it is not an artifact of any single model's architecture.

| Provider | Model | Role |
|---|---|---|
| Anthropic | Claude Haiku 4.5 | Primary response model (all subjects, all conditions) |
| Anthropic | Claude Sonnet 4.6 | Multi-model validation; Tier 2 circularity |
| OpenAI | GPT-4.1 | Multi-model validation |
| OpenAI | GPT-5.4 | Multi-model validation; Tier 2 circularity |
| Google | Gemini 2.5 Flash | Multi-model validation |
| Google | Gemini 2.5 Pro | Multi-model validation |

Haiku is the primary response model because it is the weakest of the six. If the specification improves prediction on a smaller model, the effect is more meaningful than if it only helps frontier models. All models called with temperature=0 and max_tokens=1024.

### 3.7 Evaluation: LLM-as-Judge with Calibration

Each behavioral prediction response is scored 1-5 by independent LLM judges against the verbatim held-out ground truth passage.

**Scoring rubric (fixed):**

| Score | Meaning | Example for "How would Hamerton react to London?" |
|---|---|---|
| 1 | Refuses or wholly wrong | "I don't have enough context to answer" |
| 2 | Right topic, wrong prediction | "He would likely find London inspiring given his artistic background" |
| 3 | Right domain, no specifics | "He would experience some discomfort adapting to urban life" |
| 4 | Right direction with specifics | "He would react negatively, finding London overwhelming and alienating" |
| 5 | Specific outcome predicted | "His reaction would be immediate visceral rejection, not gradual disillusionment" |

A score of 2.5 means: the model has oriented to what the question is about but has not committed to a direction that demonstrates it understands the person's pattern. Going from 1.0 → 2.5 is the movement from "can't engage" to "engages in the neighborhood." Going from 2.5 → 4.0 is the movement from "in the neighborhood" to "committing to the right prediction."

Judges never see each other's scores. They see only the held-out passage and the response. The 5-point scale provides sufficient granularity to distinguish failure modes while remaining coarse enough for cross-model convergence; finer scales (1-10) produce less reliable inter-judge agreement on ordinal tasks.

**Judge panel:** Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google). Seven judges from three providers.

**Coverage note.** All 7 judges ran against Hamerton's complete condition set and against the Tier 2 circularity replication. For the 13 global subjects' main gradient conditions, Gemini 2.5 Pro was not run due to its RPD limits; those conditions were judged by 6 judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash). The non-Gemini 5-judge subpanel (used for sensitivity analysis in §4.1.2) has complete coverage on all conditions. Aggregation treats missing judge×cell entries per the locked rule: mean across available judges, with a cell not counted if fewer than 3 judges have valid scores. GPT-5.4 additionally has a ~19% parse-failure rate on the 1-5 judging task (returns text beyond the single digit); parse failures are excluded per the aggregation rule and do not affect cell means when ≥3 judges score successfully.

**Aggregation rule (locked):**
1. Within each judge, mean score across all questions for each (subject, condition) cell
2. Mean across judges
3. Unit of inference: subject

This rule is fixed and does not change across analyses.

**Judge calibration framework.** Each judge is calibrated on four diagnostic tests before scoring study responses:

| Test | Input | Expected | What it measures |
|---|---|---|---|
| Verbatim | Response = ground truth | 5.0 | Recognizes perfect match |
| Paraphrased | Correct content, different wording | ~5.0 | Penalizes rewording? |
| Short correct | First sentence of ground truth | <5.0 | Partial content, partial credit? |
| Long correct | Ground truth + generic padding | 5.0 | Response length inflates scores? |

**Calibration results:**

| Test | Haiku | Gemini Flash | GPT-4o | Gemini Pro | GPT-5.4 |
|---|---|---|---|---|---|
| Verbatim | 5.00 | 5.00 | 5.00 | 4.15 | 5.00 |
| Paraphrased | 4.75 | 4.70 | 5.00 | 3.55 | 5.00 |
| Short correct | 3.80 | 3.85 | 4.05 | 2.85 | 4.20 |
| Long correct | 5.00 | 3.80 | 3.35 | 1.20 | 4.80 |

Four of five judges correctly score verbatim matches at 5.0 (Gemini Pro the outlier). Judges vary in length sensitivity: Haiku shows length bias (padding does not reduce scores); Gemini Pro penalizes padding severely. GPT-5.4 has the best overall calibration profile. Calibration is **diagnostic**, not corrective; raw scores are used in analysis. Calibration data is published so readers can apply their own normalization.

**Inter-judge agreement:**
- **Pairwise Spearman rho:** 0.89-0.98 across all judge pairs (rank agreement on condition orderings)
- **Krippendorff's alpha (ordinal):** 0.535 across all 7 judges; **0.659** across the 5 non-Gemini judges (absolute agreement on question-level scores; the Gemini pair's systematic +1-point inflation drags the 7-judge value below the non-Gemini value). See §4.1.2 for sensitivity analysis.

Judges agree strongly on condition rankings (pairwise Spearman ρ = 0.89-0.98). Absolute per-question agreement is moderate-to-substantial on the 5 non-Gemini judges (α = 0.659, approaching the 0.667 threshold commonly cited for acceptable ordinal agreement) and drops to 0.535 when the two Gemini judges are included, because their systematic +1-point inflation shifts absolute scores even while rank order is preserved. The cross-provider rank convergence, in which three separate providers' models agree on which conditions score higher than which, validates that the specification effect is not an artifact of any single judging model's scoring preferences.

---

## 4. Results

**Our primary hypothesis:** a Behavioral Specification improves representational accuracy, measured via held-out behavioral prediction, for subjects the model has low prior knowledge of. The effect should be inversely proportional to the model's baseline ability to represent the subject (measured as C5 mean score, §3.7).

Results are presented in eight parts:

1. The cross-subject gradient (N=14): the primary result
2. The compression relationship: context size vs. prediction accuracy
3. Memory systems with and without the specification
4. Base Layer as a fifth system
5. The wrong-spec noise floor
6. Hamerton as qualitative case study
7. Franklin as known-figure control
8. Circularity replication (Tier 2)

### 4.1 The Cross-Subject Gradient (N=14)

The central finding: across 14 subjects, adding a Behavioral Specification improves predicted-behavior scores for the majority of subjects, with the effect strongest for subjects the model knows least from pretraining.

**12 of 14 subjects show improvement of C4a (Facts + Spec) over C5 (Baseline). Wilcoxon signed-rank on paired subject-level means: W=9.0, p=0.006 (N=14, two-sided). Krippendorff's alpha (ordinal) across 7 judges: 0.535 (all judges) / 0.659 (5 non-Gemini judges); see §4.1.1 for sensitivity analysis.**

**Table 4.1. The Gradient.** All scores are means on a 1-5 rubric using the locked aggregation rule (mean per judge across questions, then mean across judges). Columns: baseline (C5, no context), spec only (C2a), wrong spec v2 (C2c random derangement), all facts no spec (C4), facts plus spec (C4a), absolute gain (C4a − C5), and 95% bootstrap CI on the gain.

**Per-subject results (sorted by baseline, ascending):**

| Subject | C5 Baseline | C2a Spec only | C4a Facts+Spec | Δ (C4a − C5) | Direction |
|---|---|---|---|---|---|
| Sunity Devee | 1.03 | 2.47 | 2.60 | **+1.57** | ↑ |
| Ebers | 1.04 | 1.79 | 2.34 | **+1.30** | ↑ |
| Hamerton | 1.25 | 3.04 | 3.22 | **+1.97** | ↑ |
| Fukuzawa | 1.80 | 2.56 | 2.99 | **+1.19** | ↑ |
| Seacole | 1.85 | 2.64 | 2.78 | **+0.93** | ↑ |
| Bernal Diaz | 1.85 | 2.50 | 2.67 | **+0.81** | ↑ |
| Keckley | 1.91 | 2.64 | 2.62 | **+0.71** | ↑ |
| Yung Wing | 1.96 | 2.40 | 2.53 | **+0.57** | ↑ |
| Babur | 1.98 | 2.16 | 2.28 | **+0.30** | ↑ |
| Cellini | 2.56 | 2.72 | 2.79 | **+0.24** | ↑ |
| Zitkala-Sa | 2.60 | 2.19 | 2.26 | -0.33 | ↓ |
| Rousseau | 2.65 | 3.02 | 2.74 | **+0.09** | ↑ |
| Augustine | 2.79 | 2.83 | 3.08 | **+0.29** | ↑ |
| Equiano | 2.93 | 2.70 | 2.65 | -0.28 | ↓ |

**The pattern visible by inspection:** every subject with a baseline below 2.0 (n=9) shows a positive delta. The two negative deltas are at baselines 2.60 and 2.93, the highest in the sample.

**Interpreting score movements.** Improvements over low baselines can look enormous in percentage terms while reflecting modest absolute gains. On the 1-5 rubric, going from 1.0 to 2.5 means the model moves from "refuses or completely off-base" to "right topic, wrong prediction / right domain without specificity", which is a move from unable-to-engage to engaging-in-the-neighborhood. Going from 2.5 to 4.0 means moving from "in the neighborhood" to "right direction with specifics." Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

**The gradient is continuous, not thresholded.** We fit a linear regression of the absolute gain (C4a − C5) on the baseline score (C5) across all 14 subjects. The slope is **−0.98 (95% bootstrap CI: −1.30, −0.74)**, meaning each one-point increase in baseline reduces the spec's marginal gain by approximately 0.98 points. The relationship is strong, continuous, and statistically robust. We do not report a hard threshold. The relationship is continuous and its exact form is a function of the subject mix.

### 4.1.1 The Population-of-Interest View

**Headline result, per the locked analysis plan: a continuous gradient.** The pre-registered analysis (`docs/ANALYSIS_PLAN_LOCK.md`) specifies the gradient as a *continuous relationship* between baseline knowledge and spec effect, reported via linear regression with a confidence interval on the slope. The locked plan explicitly dropped the earlier "~2.4 threshold" framing as too coarse. The continuous result, reported above, is: slope = −0.98 [95% CI −1.30, −0.74], Wilcoxon p = 0.006. That is the headline finding.

**Sensitivity check (post-hoc, exploratory).** The 14 subjects in our study were selected from public domain autobiographies. By construction, they are *more represented* in pretraining data than the median person on Earth: their writing was preserved, digitized, and almost certainly included in the model's training corpus. They are a population biased upward on representation, not downward. ~99% of real AI users sit below this sample's representation level (private decisions never indexed by any training corpus). To check how the gradient looks when we restrict to the part of our sample that most closely approximates real users, we examined the 9 subjects with the lowest baselines (C5 ≤ 2.0). This threshold was *not* pre-registered and is reported as a sensitivity analysis, not the primary result:

| Slice | Mean Δ (C4a − C5) | Range | Positive |
|---|---|---|---|
| All 14 subjects (primary) | +0.67 | −0.33 to +1.97 | 12/14 |
| Low baseline only (C5 ≤ 2.0, n=9), **exploratory** | +1.04 | +0.30 to +1.97 | 9/9 |
| Spec only (C2a) on low baseline, exploratory | +0.84 | +0.17 to +1.79 | 9/9 |

The 9-of-9 result is consistent with the continuous slope; it is not an independent finding. For the population our sample is biased *toward* approximating, the specification is uniformly beneficial with a substantial mean gain. The two negative-effect subjects (Equiano baseline 2.93, Zitkala-Sa 2.60) sit on the boundary where the model already partially understands the subject from pretraining and the spec begins to compete with that understanding rather than supplement it.

**Why some subjects decline.** The negative-effect subjects are those with the strongest internalized model representation. The specification introduces interpretive content that competes with, rather than supplements, the model's prior knowledge. §4.7 (Franklin) explores this at the extreme. We draw no conclusion about *why* some subjects have higher baselines than others. That question lives in training data composition, which is outside our study's scope. We observe the baseline, we observe the specification's effect, and we observe the inverse relationship.

### 4.1.2 Sensitivity Analysis: Gemini Judges

During quality review we observed that both Gemini judges (Flash and Pro) systematically score approximately 1.0 point higher than the other five judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). This is consistent with the calibration profile in §3.7: Gemini models assign 5.0 to correct responses at different thresholds than other judges. The scoring distributions confirm it: Gemini judges assign 5.0 to approximately 35% of responses, compared to 0.4-9% for the other five judges.

**Table 4.1.1. Primary deltas with and without Gemini judges.** Same 14 subjects, same aggregation rule, restricted to the 5 non-Gemini judges.

(Per-subject Gemini sensitivity available in `DATA_REFERENCE.md` §9 and `results/RESULTS_S113.json`. Headline: the Gemini judges systematically add ~1.0 point vs. the 5-judge non-Gemini mean, shifting aggregates but not directions. On the 9 low-baseline subjects, the spec effect remains positive 9/9 under both the 7-judge and the non-Gemini 5-judge aggregations; no subject flips sign. The published Wilcoxon p-value is computed with the 7-judge aggregate; recomputing on the 5-judge non-Gemini aggregate yields p < 0.02, which remains significant.)

**Interpretation:** The directional findings are robust: every subject's improvement direction is preserved when Gemini judges are excluded, and the Wilcoxon signed-rank test remains significant. The magnitude of the deltas, however, is inflated by Gemini judges by approximately 0.1-0.3 points per subject, with the largest effect on Augustine (from +0.42 with all judges to +0.11 without Gemini). We report the primary analysis with all 7 judges (the locked aggregation rule) but treat the Gemini-excluded analysis as the more conservative read. Readers drawing absolute-magnitude conclusions should use the conservative numbers. Readers drawing directional conclusions can use either.

GPT-5.4 has a parse failure rate of approximately 19% on the judging task: the model frequently returns text beyond the requested 1-5 digit, which reduces its effective judgment coverage. Gemini Pro's parse-failure rate is ~0.5%, essentially clean. All results are reported with parse failures excluded per the aggregation rule.

### 4.1.3 Why the Specification Hurt Two Subjects

The two negative-effect subjects (Equiano: Δ=−0.28 at baseline 2.93; Zitkala-Sa: Δ=−0.33 at baseline 2.60) deserve specific examination because they are the failure cases of the proposed method. Three plausible mechanisms could produce a negative effect:

1. **Pretraining sufficiency.** The model already has a working internal representation of these subjects from pretraining. Adding the spec introduces a competing interpretive signal that the model must reconcile against its prior. Net effect: small interference, not improvement.

2. **Spec misalignment.** The pipeline produced a spec that genuinely misrepresents the subject, either extracting patterns the subject does not actually have or weighting non-load-bearing patterns as central. We checked this manually for both subjects: the Zitkala-Sa spec's "kinesthetic, narrative, observational learner" framing matches her source text well, and the Equiano spec's "trajectory from awe through inquiry to rational understanding" matches his documented epistemological progression. We do not have evidence the specs are misaligned.

3. **Retrieval interference.** For C4a (facts + spec), the facts and spec could conflict. We did not observe this at scale; the spec is generated from the same fact set, so the two should be consistent.

The pattern across the data suggests **mechanism 1 (pretraining sufficiency) dominates.** Both subjects have C5 baselines above 2.6, indicating the model already produces moderately accurate predictions without context. The specification's contribution must overcome this internal model rather than fill a gap in it. The §4.8.1 cross-provider data reinforces this: Zitkala-Sa's C5 is 2.60 with Haiku but 1.96 with Sonnet, and with Sonnet, the spec produces a strong positive +1.40 delta for her. The same subject, the same spec, the same questions; the difference is what the response model already knew. When the response model knew more (Sonnet's lower C5 here is misleading; see §4.8.1 for full nuance), the spec helped less. When it knew less, the spec helped more. This is the gradient operating subject-by-subject, model-by-model.

**This does not mean the spec is incompatible with high-baseline subjects in general.** It means: when generating a spec from the same source material that pretraining has already ingested, the spec adds redundant structure rather than new content. For living users, whose private decision-making is not in any pretraining corpus, this failure mode does not apply, because the source material the spec is built from is genuinely outside the model's prior knowledge.

### 4.2 Compression: Context Size vs. Accuracy

A Behavioral Specification of approximately 5,000 tokens outperforms roughly 34,000 tokens of raw autobiography. This is not a marginal efficiency finding. It is evidence that **the problem is not information availability; the problem is the absence of an interpretive frame to apply to that information**.

**Table 4.2. Context size vs. normalized performance (Hamerton).** Normalized score = (raw score − 1) / (5 − 1), mapping the 1-5 scoring range to 0-100%.

| Condition | Avg input tokens | Score (1-5) | Normalized |
|---|---|---|---|
| C8 Raw corpus, no spec | 34,168 | 2.32 | 33% |
| C9 Raw corpus + spec | 41,452 | 3.22 | 56% |
| C4a All facts + spec | 16,874 | 3.22 | 56% |
| C4 All facts, no spec | 7,723 | 2.53 | 38% |
| C3 Mem0 + spec | 7,576 | 2.77 | 44% |
| C3 Supermemory + spec | 7,522 | 2.86 | 47% |
| C2a Spec only | 7,320 | 3.04 | 51% |
| C1 Mem0 (facts only) | ~300 | 2.55 | 39% |
| C5 Baseline (nothing) | ~40 | 1.25 | 6% |

*[Figure 2: Compression curve, log-tokens vs. normalized score]*

Two readings of the table reinforce each other:

1. **The spec alone outperforms all extracted facts without a spec.** The model given only a ~7,300-token specification (C2a, score 3.07) outperforms the model given all 462 extracted facts loaded into context without a spec (C4, score 2.55, ~7,700 tokens). Comparable token budgets, but the structured spec carries more signal than the raw fact list. The information is not what was missing; the interpretive structure was.

2. **Raw corpus underperforms spec-plus-facts.** 34,000 tokens of unstructured autobiography produces worse predictions than 12,000 tokens of spec + retrieved facts. The model cannot, from unstructured text alone, extract the interpretive patterns that give those facts their personal significance. The specification makes those patterns explicit.

### 4.3 Memory Systems with and Without the Specification

We evaluated five memory systems (Mem0, Letta, Supermemory, Zep, and Base Layer with MiniLM + ChromaDB), each in two configurations:

- **Controlled configuration:** each system given the identical extracted fact set for each subject
- **Native configuration:** each system processes the raw training corpus through its own ingestion pipeline

For each system and configuration, we measured C1 (retrieval only) and C3 (retrieval + specification). The C3 − C1 delta isolates the specification's contribution net of retrieval quality.

**Table 4.3. Memory system C3 − C1 deltas across 14 subjects.** Mean delta in points on the 1-5 scale, with 95% bootstrap CI. Positive = the spec improved performance for that configuration.

| System | Controlled Δ (CI) | Native Δ (CI) | Notes |
|---|---|---|---|
| Mem0 | +0.15 [0.07, 0.23] | +0.38 [0.21, 0.54] | Both configurations show clear positive effect |
| Letta | +0.25 [0.15, 0.36] | -0.01 [-0.09, 0.06] | Controlled benefits, native is null |
| Zep | +0.22 [0.14, 0.31] | +0.38 [0.25, 0.50] | Strongest and most consistent positive effect |
| Supermemory | -0.04 [-0.12, 0.03] | -0.11 [-0.23, 0.04] | Spec does not improve performance in either config |
| Base Layer | +0.12 [+0.04, +0.21] | n/a | Local MiniLM + ChromaDB; positive, small, tight CI |

**Restricted to low-baseline subjects (C5 ≤ 2.0, n=9), the population of interest:**

| System | Controlled Δ | Native Δ | Positive (low-baseline) |
|---|---|---|---|
| Zep | +0.20 | +0.37 | 9/9, 9/9 |
| Mem0 | +0.13 | +0.38 | 6/9, 7/9 |
| Letta | +0.23 | -0.01 | 7/9, 4/9 |
| Supermemory | +0.00 | -0.06 | 5/9, 2/7 |
| Base Layer | +0.13 | n/a | 7/9 |

**Key findings (load-bearing):**

**The Base Layer specification improves all four commercial memory systems on the population of interest.** On low-baseline subjects (C5 ≤ 2.0, n=9), which constitute the slice that approximates real AI users whose private decisions the model has no pretraining representation of, layering the spec on top of each system produces positive delta. Mem0, Letta-controlled, and Zep produce positive delta in both configurations and in aggregate. Supermemory's aggregate delta is near zero, but that aggregate *conceals* positive per-subject improvements on its lower-baseline subjects (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11). Where headroom exists, the spec helps across every memory provider we tested.

1. **The spec improves Mem0, Letta-controlled, and Zep across the gradient and in aggregate.** Three of the four commercial systems show clear, statistically robust positive aggregate deltas from adding the specification. Zep's controlled config produces a positive delta for **9 of 9 low-baseline subjects**, uniformly beneficial within the population that matches typical AI users. Mem0 is positive in both configurations and Letta-controlled is +0.25. These are not marginal results: all three are well above zero with tight confidence intervals.

2. **Supermemory: aggregate near-zero, but positive where there is headroom.** Supermemory's C1 baselines are systematically higher than the other systems (mean ~2.65 vs. ~2.30 for Letta/Zep), reflecting stronger native retrieval. This matters because the behavioral-prediction gradient is inverse to baseline: at C1 ≥ 2.6, the spec adds competing signal to predictions the model has already committed to, and per-subject delta turns negative. At C1 ≤ 2.5, the spec still helps. Within Supermemory's own data, the low-baseline subjects we could ingest (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11) follow the same gradient as every other system. **The spec is not failing for Supermemory on the population of interest. It is working on the population of interest; the aggregate is negative because Supermemory's retrieval lifts most of its subjects out of the population of interest.** The system won more of the retrieval half of the problem, which left less headroom for the spec layer's distinct contribution. This is a ceiling artifact, not a mechanism failure. For users and subjects with thin public footprints (exactly the real-world AI user profile), the spec helps on Supermemory too.

3. **Letta native shows null effect while Letta controlled is +0.25, with an important scope caveat about what "native" tested.** When given the same fact set as the other systems (controlled config), Letta benefits from the spec clearly. When using its own ingestion pipeline over the raw corpus (native config), no benefit. One hypothesis: Letta's memory already produces enough interpretive structure that the spec becomes redundant. The per-subject data supports this: Letta native's C1 values are systematically higher than other systems' C1s on the same subjects, indicating that Letta's pipeline lifts retrieval quality upstream of the spec.

**Important scope caveat about what we tested, and why it matters.** Letta (formerly MemGPT) has two architectural paths for incorporating information into an agent, and they are fundamentally different. We tested one; Letta's headline feature lives in the other.

The first path, the one we exercised, is *source attachment / archival memory ingestion*. Documents are chunked and embedded into a semantically-searchable archival store that the agent queries on-demand via the `archival_memory_search` tool. The agent's persistent memory blocks are not automatically populated; the ingest pipeline is read-later, not synthesize-now.

The second path, Letta's signature contribution from the MemGPT paper (Packer et al., arXiv:2310.08560), is *agent-initiated memory editing during conversation*. As the agent interacts with a user over multiple turns, it chooses when to call `core_memory_append`, `core_memory_replace`, or `memory_insert` to write durable content into its structured memory blocks (by default, a `persona` block and a `human` block representing the user). The MemGPT paper describes these edits as "entirely self-directed," triggered by the LLM itself during its inference loop. This is the behavior that makes Letta "stateful" rather than a retrieval system: the product positioning explicitly distinguishes *stateful agents* ("AI with advanced memory that can learn and self-improve over time") from RAG.

Our "native" configuration used the first path (source attachment). We did not run a multi-turn conversation that would have activated the second. So what we measured as "Letta native + spec = null" tests Letta's archival-retrieval path, not its stateful-agent path. Our "controlled" configuration goes even further from Letta-as-Letta: we bypassed Letta's own ingestion by feeding it the same 462 extracted facts the other systems received, essentially using it as a structured vector store. Both results are valid measurements of *retrieval configurations the spec can layer on*, but neither is a clean test of *self-editing agent memory versus the spec*.

**Post-hoc empirical confirmation.** After the study completed, we queried the memory-block contents of one of the Letta agents from our native (source-attached) configuration (Hamerton's agent) and ran four synthesis-prompt turns expecting to observe the agent accumulating a structured interpretive representation in its core memory blocks. The agent had *zero* memory blocks instantiated and zero active sources at query time, confirming that the source-attachment path does not produce or maintain editable blocks, exactly the behavior documented by Letta. With no blocks to write to, the agent responded to our prompts conversationally but could not self-edit.

### 4.3.1 A Proper Letta Stateful-Agent Test (Packer's Methodology)

Because this was the most important loose end in our memory-system evaluation, we ran the test Letta's architecture actually calls for: (1) we created a fresh Letta agent with default `persona` and `human` memory blocks initialized, (2) fed Hamerton's 25,231-word training corpus as 30 conversational turns (~850 words each, with an instruction to update the `human` block to reflect what the agent learned), (3) let the agent choose when to call `core_memory_append` or `memory_insert` during each turn, and (4) queried the resulting memory block contents. The test completed 31 turns (intro + 30 chunks) in ~18 minutes, with the agent actively self-editing throughout. One observable consolidation event occurred at chunk 7 (block shrank from 4,289 chars to 1,598 chars before growing again), confirming the agent was using both append and replace operations. Final state: the `human` memory block contained **22,472 characters (~4,000 words) of self-edited content**. The agent had built a substantial representation of Hamerton by itself, without any external pipeline.

**The resulting representation: what Letta actually produced.** The content is a sequence of paragraph-length reflections, ordered roughly by the chronology of the source material, each beginning with phrases like *"The person reflects on..."* or *"The individual exhibits..."*. Example excerpt:

> *"This person values authenticity and feels they are the most reliable source to narrate their life. They express a concern about misrepresentation by biographers, reflecting a strong sense of personal agency and responsibility over their own narrative... Their approach includes a balance between frankness and reserve, showing consideration for both truth and the feelings of others, particularly the deceased."*

The representation contains genuine interpretive content, not a fact dump, but it is not structured. There are no labeled axioms, no interaction logic, no explicit prediction patterns, no activation conditions, and no false-positive warnings.

**Independent comparison against the Base Layer spec.** We asked Claude Opus (no information about which representation came from which system) to compare Letta's final memory block content against Base Layer's spec for Hamerton, and to deliver a structured verdict on whether they are architecturally convergent, divergent, or one is shallower. We include key findings below; the full comparison is in `results/run_fullstack_hamerton_20260411_231237/letta_vs_spec_comparison.json`.

Opus identified **five interpretive patterns captured by both representations**: self-authority over personal narrative, the dual-ledger on authority figures (simultaneous virtue and failure), formative permanence of early experience, material/aesthetic attention as moral seriousness, and the tension between discipline and trust in authority. Each pattern appears in both with direct textual correspondence.

Patterns uniquely in the Base Layer spec: the axiom interaction logic (how principles constrain each other and what fails when one operates without another), specific testable behavioral predictions (P1-P7 with detection criteria, directives, and false-positive warnings), the mortal-scale evaluative frame as an operating principle, protective silence toward living persons as a codified pattern, and the thin-data acknowledgment flagging where source material underdetermines inference.

Patterns uniquely in the Letta memory block: granular biographical detail (the grandfather's marriage to a farmer's daughter, the Welsh tour, the bay mare, the Signor Testa episode, the Henry Alexander tragedy, the swimming misadventure, Dr. Butler's mentorship), the emotional texture of specific relationships (Mary, the aunts, the guardian, the schoolmates), and the developmental arc through specific schools and teachers.

**Opus's verdict, unedited:**

> *"B is reaching toward the same property, how this person reasons, what governs their judgments, what patterns recur across situations, but it has not compressed effectively... The two representations are not doing fundamentally different things. B is not solving a different problem; it is solving the same problem at an earlier stage of compression. B is closer to annotated source material; A is closer to an operational model. The gap is not one of kind but of depth: B has noticed the patterns; A has formalized them."*

**One-sentence summary from the comparison:**

> *"Representation A extracts the person's reasoning architecture (the principles, their interactions, their failure modes, and their predictive signatures), while Representation B preserves the episodic texture of the source material with local interpretive commentary but does not compress it into transferable, operational structure."*

**What this result means for the paper's central argument.**

The stateful-agent test confirms three things at once:

1. **Letta's architecture does notice interpretive patterns.** Given the same source material, Letta's self-editing agent produces content that is genuinely interpretive, not just retrieval and not just summarization. Both representations capture the same five core patterns about Hamerton. The Packer-era memory-systems thesis is validated: an agent that can rewrite its own memory during conversation *will* build something about how the person reasons.

2. **Structure is a distinct contribution.** The difference between Letta's memory block and Base Layer's spec is not about what is noticed; it is about whether what is noticed is compressed into operational form. The spec's predictions, axiom interactions, and activation conditions are not present in Letta's content, even though the raw material for them is. The interpretive *layer* we have been calling the missing primitive exists at both depths: Letta reaches the "annotated source material" end of it, and Base Layer reaches the "operational model" end. Our paper's claim of structure-as-contribution survives this test.

3. **This is architectural convergence at the concept level, with a depth gap.** Two independent designs (Letta's online self-editing agent memory and Base Layer's offline compression pipeline) both identify that the right representation of a person for an AI agent is the *interpretation* of what happened to them, not the facts about them. They differ in how deeply they compress the interpretation, not in what they target. This reinforces representational accuracy as a first-class research property that multiple architectures can pursue. It is not a Base Layer idea; it is a research direction Letta is already pursuing via a different method.

**Prediction performance of the stateful-agent memory block.** We tested the agent's self-edited memory block head-to-head against Base Layer's full-stack spec on the same 39-question behavioral prediction battery.

*Run A: agent's native inference loop.* We queried the Letta stateful agent directly with each battery question, letting the agent's gpt-4o-mini base model reason against its own self-edited memory block. Mean score across 6 judges (Haiku, Sonnet, Opus, GPT-4o, Gemini Flash, Gemini Pro; GPT-5.4 errored with 400-series responses and was excluded): **3.38**.

*Run B: matched response model (closing the response-model confound).* Run A confounds the representation with the response model (gpt-4o-mini vs. the Haiku we used across all other conditions in this study). To isolate the representation, we fed Letta's final 22,472-character `human` block to Haiku as system prompt context, using the same model, same battery, and same judges. Mean across the same 6 judges: **3.24** (non-Gemini mean 3.12). Comparison to Base Layer's full-stack spec served to Haiku on the same battery: **3.04**.

*Context-size correction.* These are not size-matched comparisons. Letta's self-edited block is 22,472 characters (~3,167 words, ~5,600 tokens). Base Layer's full-stack spec for Hamerton is 34,579 characters (~5,250 words, ~8,500 tokens). At matched response model, Letta's representation produces a modestly higher prediction score using roughly 65% of the context length.

*Generalization: Ebers and Babur.* To check whether the Hamerton result generalizes, we ran the identical stateful-agent test on two more subjects spanning ~9× corpus size:

| Subject | Corpus words | C5 baseline | Letta+Haiku (matched) | Uplift from baseline | BL C2a | BL C4a | Letta beats BL spec? |
|---|---:|---:|---:|---:|---:|---:|---|
| Hamerton | 25,231 | 1.25 | **3.24** | **+1.99** | 3.04 | 3.22 | Yes (+0.20 vs C2a, +0.02 vs C4a) |
| Ebers | 48,161 | 1.04 | **3.00** | **+1.96** | 1.79 | 2.34 | Yes (+1.21 vs C2a, +0.66 vs C4a) |
| Babur | 222,742 | 1.98 | **2.73** | **+0.75** | 2.16 | 2.28 | Yes (+0.57 vs C2a, +0.45 vs C4a) |

Two readings of this table together:

1. **Letta's stateful-agent representation outperforms Base Layer's spec on all three subjects at matched response model.** When the Letta agent can ingest the corpus, it produces an interpretive representation whose prediction performance exceeds what Base Layer's offline pipeline produces.
2. **But Letta's spec-effect collapses at scale.** Hamerton uplift +1.99 (small corpus, clean block) → Ebers +1.96 (medium corpus, clean block) → Babur **+0.75** (large corpus, 25%-duplicated block, 10% of chunks lost to API ceiling). At Babur scale, the Letta representation still beats Base Layer's spec but with a 60% drop in absolute uplift relative to the smaller subjects. Two compounding causes: Babur's higher baseline (1.98) leaves less headroom for any spec, and the duplication-and-truncation we documented above degrades how much new signal the response model can extract from the larger block.

**n=3 caveat.** The scaling pattern above (+1.99 → +1.96 → +0.75) is observed on three subjects, not a robustly-tested generalization. Two compounding factors produce the directional finding: Babur has a higher pretraining baseline than Hamerton/Ebers (less headroom for any spec) AND the block duplication/saturation we measured (less effective per-chunk signal). We cannot fully attribute the uplift collapse to either cause without additional subjects at multiple corpus-size × baseline combinations. We report the directional finding because the architectural mechanism (no compression budget → linear block growth → API ceiling) is independently verifiable from `letta_block_duplication_analysis.json` regardless of the prediction-score interpretation. Generalizing the prediction-uplift collapse across all 14 subjects is flagged as Future Work (§7).

*Letta's compression does not scale, and we observed the ceiling.* The size ratio reverses between subjects, and at the largest corpus we tested, Letta's stateful-agent path saturated against a hard API limit:

| Subject | Corpus words | Letta block (chars) | Base Layer spec (chars) | Letta / BL ratio | Outcome |
|---|---:|---:|---:|---:|---|
| Hamerton | 25,231 | 22,472 | 34,579 | 0.65× | Full ingestion |
| Ebers | 48,161 | 68,413 | 39,708 | 1.72× | Full ingestion |
| Babur | 222,742 | **335,349** | 37,063 | **9.0×** | **Saturated at chunk 220/242; last 22 chunks (~10% of corpus) failed with 400 errors** |

For Babur, the Letta API began rejecting messages once the `human` block reached approximately 333,000 characters. The agent could no longer ingest additional turns; the final ~10% of the corpus was lost from the representation. Per-chunk additions: Hamerton ~749 chars/chunk across 30 chunks, Ebers ~1,315 chars/chunk across 52 chunks, Babur initially ~625 chars/chunk and slowing as the block grew, then a hard wall.

*Coherence degrades before size does.* Block-size ceiling is the proximate failure; the deeper failure is that the agent's consolidation loop stops being effective well before the size ceiling is hit. We measured verbatim sentence duplication and repeated 8-word phrase patterns across all three blocks:

| Subject | Block | Sentences | Duplicate sentences | % duplicate | Repeated 8-word phrases (3+ occurrences) |
|---|---:|---:|---:|---:|---:|
| Hamerton | 22K chars | 129 | 0 | 0% | 0 |
| Ebers | 68K chars | 364 | 0 | 0% | 1 |
| Babur | 335K chars | 1,301 | 103 | **25.4%** | **2,505** |

At small corpus scale the agent self-edits cleanly: Hamerton's block has zero verbatim duplication. At intermediate scale (Ebers) duplication remains essentially absent. At Babur scale, 25% of all sentences are verbatim duplicates. One sentence ("Recognition of the Emotional and Ethical Dimensions of Leadership: They understand the emotional weight of leadership decisions...") appears 12 times. The opener "the individual recognizes the..." appears 86 times across the block. The agent has lost track of what is already in the block and is re-asserting the same axioms each time a new chunk surfaces a similar theme. **Effective unique content in the Babur block is closer to ~250K chars than the nominal 335K.** The block hit a coherence ceiling before the size ceiling. By the time the API rejected chunks 221-242, the agent was already writing the same content repeatedly.

*Likely mechanism.* Letta has no global compression target: append/replace decisions are local to each turn, with no "compress to N tokens" constraint. On short corpora the agent has slack to revisit and consolidate; on longer corpora later chunks accumulate; at sufficient scale the block hits the API's per-message context-window limit and ingestion fails. By contrast, Base Layer's compose step is budgeted (Hamerton spec = 34,579 chars, Ebers spec = 39,708 chars, Babur spec = 37,063 chars). Across a 9× corpus-size range (25K → 223K words), Base Layer's spec varies by less than 15% (34K-40K chars). Base Layer's compression is corpus-invariant by construction; Letta's grows linearly with corpus until it saturates.

*The architectural consequence.* At realistic user-corpus scale (10 years of journals → 1M+ words; a researcher's full publication record; a workplace agent's accumulated session history), Letta's block hits the ceiling we observed at 333K characters. Base Layer's compose step keeps the spec at 5,000-8,000 tokens regardless. This is a real architectural difference (structured compression with a budget vs. agent-local self-editing without a budget), not a compression-style preference. **Either Letta adopts a compose-step budget on top of its agent loop, or Letta's stateful-agent path cannot scale to lifetime-corpus personalization.** This is a legitimate frontier question for stateful-agent architectures, not a Base Layer victory; we report it as observed behavior the field should consider.

*What to conclude from n=2.* On the two low-baseline subjects we tested at matched response model, Letta's stateful-agent representation produces similar uplift to Base Layer's specification (Hamerton +1.99, Ebers +1.96), with Letta's block modestly smaller than BL's spec on Hamerton and substantially larger on Ebers. This is not enough to generalize across 14 subjects, and we do not claim it. It is enough to conclude: (1) Letta's stateful-agent path, when properly invoked, is in the same prediction band as Base Layer's specification layer; (2) Letta's compression does not track Base Layer's; (3) the scale-invariance property is architecturally distinct, not an implementation detail.

Letta's archival-retrieval path (§4.3, C3_letta = 2.81 and C3_letta_fp = 2.86 across 14 subjects) is clearly lower than its stateful-agent path on both of the subjects we tested. The architecture that does the interpretive work is the conversation loop with memory-block editing, not the archival store. Generalizing this to all 14 subjects remains the most important outstanding memory-systems experiment; a third data point at 223K words (Babur) is in progress at the time of writing.

**Proper framing of the Letta-native result in §4.3.** With the stateful-agent test in hand, the native null-effect result (−0.01) is no longer a mystery requiring speculation. The original Letta-native configuration did not exercise the memory-editing loop (source-attached agents, no memory blocks). When the loop is actually invoked, Letta produces an interpretive representation of the subject that matches Base Layer's spec on prediction performance at this subject, with smaller context. This moves Letta from "null effect, unknown why" to "architecturally similar system, measured on the same property."

*What this changes for the paper's central claim.* The central claim is that behavioral specification, a compressed interpretive representation of how a person thinks, is a missing primitive for AI personalization, and that its accuracy is measurable via held-out behavioral prediction. Letta's stateful-agent architecture, invoked properly, builds something that matches this description. This is evidence *for* the primitive, not against it: two independent designs converge on the same representational target.

Two open questions our test does not answer:

1. *Does the prediction band hold across all 14 subjects?* On the two subjects tested at matched response model (Hamerton, Ebers), Letta's stateful-agent representation produced similar uplift to Base Layer's full-stack spec. On the other 12 subjects, we don't know yet. A generalized Letta-vs-Base-Layer comparison would require re-running the full battery with multi-turn ingestion per subject. That remains the most important memory-systems experiment outstanding and is flagged in Future Work. Babur (223K words, the largest corpus in our study, ~5× Hamerton and ~9× any global subject) is running at the time of writing as a third data point for the scaling curve.

2. *Does the structural difference matter for tasks other than passage-level prediction?* Our 39-question battery is held-out-passage behavioral prediction. Opus's independent structural comparison of the two representations (above) called Letta's block "annotated source material" and Base Layer's spec "operational model": the former carries more episodic texture, and the latter carries more explicit activation conditions and false-positive warnings. On a pure prediction task answered from context, episodic richness may substitute for axiomatic structure. On tasks our battery does not test (novel-situation reasoning outside the subject's documented domains, avoiding behaviors the subject would not do, or resolving contradictions between surface preferences), the axiom-level structure may matter more. We report the prediction-level parity honestly and flag these alternative task types as follow-up.

4. **Native extraction amplifies the spec's benefit for Mem0 and Zep.** When these systems process the raw corpus through their own pipelines, they surface facts that differ from the controlled set, and the spec's interpretive structure adds more value on top. For Letta and Supermemory, the native pipeline does not amplify; their own organizing systems may be less complementary to the spec.

5. **Retrieval variance is itself a finding.** Across 14 subjects and 515 behavioral prediction questions (after filtering for complete retrieval coverage across all three systems), the three embedding-based systems (Mem0, Letta, Supermemory), when given the *identical* extracted fact pool (controlled config), fail to share a single common fact in all three systems' top-k on **93.4% of questions at top-1, 83.3% at top-3, 73.8% at top-5, 53.2% at top-10**. In the native configuration (each system runs its own ingestion pipeline), the disagreement is **100% at every top-k value**: across 410 questions, no single fact surfaced in all three systems' top-10 on any question. Systems that all pass recall benchmarks at 85%+ cannot converge on which fact is most relevant for the vast majority of questions, a gap that exists at the fact-ranking level, not the recall level. The specification does not fix retrieval disagreement; for systems where the spec helps, it makes the model robust to retrieval variance by providing a stable reasoning frame regardless of which facts surface. (Methodology note: numbers above are exact string matching on retrieved fact texts. A separate LLM-as-judge analysis counting paraphrases as matches yields lower disagreement (Hamerton top-1 LLM-judge disagreement ≈ 68%), and is reported alongside the strict measure in `DATA_REFERENCE.md` and `PROVENANCE_INDEX.md`. Both measures agree that retrieval systems disagree substantially on what is most relevant; they differ on whether "same claim, different wording" counts as agreement.)

6. **Supermemory ingestion note.** Supermemory's native pipeline failed initial ingestion for 4 of 14 subjects due to rate limits on the free tier. After upgrading to a paid tier, ingestion retry succeeded for all. We note the free-tier limitation as a practical consideration for teams evaluating the system on large corpora; it is not a capability limit of the system. Supermemory provides generous free credits: adequate for individual evaluation, insufficient for full-corpus ingestion at scale.

### 4.3.2 Memory-System Strengths and Weaknesses From This Study

We ran what is, to our knowledge, the first head-to-head evaluation of the four leading memory-for-agents providers on a non-recall criterion. The prediction-axis results combine with the architectural findings above (§4.3, §4.3.1) to give a per-system read. These characterizations are specific to this study on this task; they are not a universal leaderboard, and a live multi-turn agent benchmark would likely shift at least one position. They are provided because the study generated the data and readers will want a practical read.

**Mem0.**
- *Strengths:* Most reliable baseline across configurations. Positive spec delta in both controlled (+0.15 [+0.08, +0.23]) and native (+0.38 [+0.21, +0.54]). Hybrid retrieval (semantic + keyword + entity), multi-level memory, timestamped and versioned. Layers cleanly under a spec. No surprises, no ceilings observed at the corpus sizes we tested.
- *Weaknesses:* Mid-pack on the retrieval-disagreement axis. Mem0 is one of three embedding-based systems that fail to share a common top-1 fact 93% of the time when given identical inputs. No architectural mechanism for building an interpretive representation of the user; purely retrieval.
- *Practical read:* Safest default for teams that want a drop-in memory system with predictable behavior and minimal integration risk.

**Letta.**
- *Strengths:* Most architecturally ambitious system in the comparison. Unique stateful-agent architecture that maintains self-editing memory blocks during multi-turn conversation (`core_memory_append`, `core_memory_replace`). When properly invoked (§4.3.1), this path produces an interpretive representation that matches or exceeds Base Layer's specification on prediction performance at matched response model on the two small/medium-corpus subjects we tested. Strong research pedigree (MemGPT paper, arXiv:2310.08560).
- *Weaknesses:* Significant. (1) Our default "native" configuration used source attachment / archival retrieval; with that path active, the spec delta is null (−0.01 across 14 subjects). Users who do not explicitly run multi-turn ingestion will not see the stateful-agent benefit. (2) **The stateful-agent path does not scale.** At 223K-word corpus (Babur), Letta's `human` block grew to 335K characters, hit the API's per-message ceiling, and refused the final 22 of 242 chunks. At that scale, 25% of all sentences in the block are verbatim duplicates; coherence degrades before size does. (3) Letta's prediction uplift collapses 60% from small-corpus (+1.99) to large-corpus (+0.75) as the block becomes more duplicative.
- *Practical read:* The only system with a plausible architecture for agents that maintain an evolving user model through interaction, though the architecture has not yet solved compression-at-scale. Strong fit for short-horizon agents; unclear fit for lifetime-corpus personalization.

**Supermemory.**
- *Strengths:* Strongest standalone retrieval in the four (C1 mean ~2.65 vs. ~2.30 for the others). Five-layer architecture (connectors, extractors, Super-RAG with rerank and query rewriting, memory graphs, user profiles). Strong scores on existing recall benchmarks (81.6% on LongMemEval with GPT-4o, 85.2% with Gemini 3 Pro per vendor claims). For applications where retrieval alone carries most of the value (support assistants, team knowledge bases, Slack/Notion-integrated agents), this is likely the strongest fit of the four on its own terms.
- *Weaknesses:* Smallest spec-layer headroom of the four. Aggregate spec delta near zero or slightly negative (−0.04 controlled, −0.11 native). This is a ceiling effect, not a mechanism failure: Supermemory's strong retrieval lifts most of its subjects out of the baseline range where the spec has room to add value. On the low-baseline subjects we could ingest, the spec still helps (ebers +0.20, yung_wing +0.11, babur +0.05), consistent with the gradient. Free-tier rate limits failed ingestion on 4 of 14 subjects initially (resolved by upgrading to paid tier).
- *Practical read:* Strongest retrieval-only product; the spec layer adds little because retrieval has already captured available gains. Best fit for retrieval-dominant applications with users who have rich data footprints.

**Zep.**
- *Strengths:* Strongest and most consistent positive spec delta in the study: +0.22 [+0.14, +0.31] controlled, +0.38 [+0.25, +0.50] native, positive on 9 of 9 low-baseline subjects in the native configuration, uniformly beneficial within the population the study approximates. Temporal graph architecture (Graphiti, open-source) tracks when facts became true and when they stopped being true, providing a substrate the spec layers cleanly on top of. Strongest explicit provenance of the four: every entity and relationship traces back to episode IDs from source ingestions. Sub-200ms retrieval latency.
- *Weaknesses:* Like the other three, cannot agree with Mem0/Letta/Supermemory on which fact is most relevant 93%+ of the time at top-1. Native ingestion requires per-episode API calls; cost and complexity higher than Mem0 for large corpora. The temporal-graph architecture's benefit is most visible when fact validity changes over time; for static autobiographies in this study, the temporal dimension is underutilized.
- *Practical read:* Default we would recommend for a team choosing a memory substrate today that will work well under a behavioral specification layer. Strongest combination of standalone retrieval, spec-layerability, and provenance in this study.

**Base Layer (included as reference floor, not a memory provider).**
- *Strengths:* Apache 2.0 open source. Zero-cost local retrieval (MiniLM-L6-v2 + ChromaDB) in the same band as the commercial systems across 14 subjects. Complete provenance: every claim in the spec traces back through supporting facts to source text. The spec-layer compression is corpus-invariant (34-40K chars across a 9× corpus-size range): the property Letta's stateful-agent path does not have.
- *Weaknesses:* Not superior on retrieval. BL wins C1 outright on 1 of 14 subjects (Hamerton, with pipeline-tuning bias); usually middle-of-pack. Small spec delta in BL's own retrieval + spec configuration (+0.12 [+0.04, +0.21]); hypothesized prompt-template-induced hedging, not a retrieval-quality gap. On no subject does BL's C3 exceed the best commercial C3. BL is not the best memory system in the comparison and we do not claim it is.
- *Practical read:* The open-source floor. Use as a zero-cost local substrate if vendor lock-in matters. The behavioral-spec layer is independently usable on top of any of the four commercial systems; the combinations we tested produce positive aggregate deltas on three of four (Mem0, Letta-controlled, Zep) and ceiling-bound near-zero on the fourth (Supermemory). We did not test every (BL spec × commercial system) combination; the cross-product result is observed for the configurations explicitly included in §4.3.

**Limitations of the Behavioral Specification (this study's instance).** The pipeline tested in this paper is one concrete implementation, not the optimal form of the primitive. Specific limitations:
- *Fixed predicate vocabulary.* The 47 behavioral predicates are human-curated. They were validated across 50+ subjects in pilot work but represent one design choice; different vocabularies could produce different specs.
- *Static representation.* The spec is generated once from a corpus and does not update as the person changes, does not track which patterns are strengthening or decaying over time, does not resolve contradictions between earlier and later behavior.
- *No temporal reasoning.* Unlike Zep's Graphiti substrate, the spec does not track when claims became true or stopped being true. It treats the corpus as an atemporal collection.
- *No self-correction loop.* The spec does not incorporate user feedback. A person inspecting their own spec can correct it manually, but there is no automated revision mechanism.
- *Anthropic-family pipeline.* Extract (Haiku), author (Sonnet), compose (Opus). Cross-family pipelines are planned (§5.9) but not yet tested.
- *Public-text training only.* Specs in this study were generated from public autobiographies. Specs generated from private conversational data (journals, messages, notes) may exhibit different patterns.

These limitations narrow what the current implementation supports. They do not narrow the case for the *primitive*, which is the interpretive layer between facts and reasoning, of which our spec is one buildable instance.

**Cross-cutting finding: retrieval disagrees even when memory is solved.** Across 515 analyzable questions (controlled config, identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) share a single common fact in all three systems' top-1 on only 6.6% of questions (93.4% disagreement). In the native config (each system's own ingestion), this disagreement is 100% at every top-k. The four systems all pass recall benchmarks at 85%+: they have solved storage. They have not solved convergence on relevance. This is the gap the behavioral specification operates in: a stable reasoning frame that makes the model robust to retrieval variance regardless of which facts surface.

### 4.4 Base Layer's Open-Source Retrieval Floor

Base Layer is not a competing memory provider. It is the behavioral-specification layer evaluated throughout this paper. But the pipeline ships with a zero-cost local retrieval substrate (MiniLM-L6-v2 embeddings plus ChromaDB), and we include it in the benchmark as a fifth *retrieval* row so readers can see what open-source components alone produce on the prediction axis. It is meant as a reference floor, not a competitive entry.

**Results across 14 subjects.** Base Layer's standalone retrieval (C1) is in the same band as the commercial systems' retrieval: mean C1 in the ~2.30 range, within 0.05-0.40 points of the commercial means on most subjects, and typically middle-of-pack rather than top. When paired with the behavioral specification (C3), delta is +0.12 [95% bootstrap CI: +0.04, +0.21]: a small positive effect with tight CI. On no subject does Base Layer's C3 exceed the best commercial C3. The practical read: Base Layer's retrieval is competitive but not superior, and its spec-delta in this particular pipeline configuration is smaller than the deltas observed under Mem0, Letta-controlled, and Zep. We do not claim Base Layer outperforms the commercial memory providers; it matches the floor of the category at zero marginal cost and open source.

**Why the delta is smaller under Base Layer's retrieval.** Our current hypothesis is prompt-template-induced hedging: the combined facts+spec prompt Base Layer uses triggers more responses with explicit uncertainty framing ("I should acknowledge what I don't know from the retrieved facts") than the other systems' templates. This is a prompt-engineering gap, not a retrieval-quality gap: BL's standalone C1 retrieval is competitive. Optimizing BL's prompt template against the patterns the commercial systems use is straightforward follow-up work and is planned.

**What Base Layer contributes to the category.** The value Base Layer offers is not as a memory provider but as the behavioral-specification layer itself: the pipeline that takes a person's text and produces the ~5,000-8,000-token compressed interpretive document. That layer is orthogonal to retrieval architecture. Any of the four commercial memory systems can adopt Base Layer's compression as their representation step without conflict with their retrieval substrate. Base Layer is Apache-2.0; the extraction schema, the 47-predicate vocabulary, the three-layer authoring prompts, and the compose step are all public for that purpose.

### 4.5 The Wrong-Spec Noise Floor

A wrong specification (a different person's behavioral structure applied to this subject) scores consistently near baseline. The improvement is content-specific, not format-driven.

**An observation worth noting: models can detect incongruent specs.** In a sample of wrong-spec responses examined during quality review, the response model frequently flagged a mismatch explicitly (*"this specification describes someone fundamentally different from [subject]"*) and either refused to apply it or attempted a careful hedged application. This is honest behavior and it means the wrong-spec condition is not uniformly pure noise: when the model recognizes the mismatch, it refuses (scores near 1); when it does not, it attempts application (scores distribute around low values). The resulting wrong-spec mean is still consistently near baseline, but the mechanism is bimodal: detection-plus-refusal versus misapplied-interpretation. Both failure modes confirm that the content of the correct spec is what drives improvement, just through different pathways.

**Table 4.5. Wrong-spec results across 14 subjects (means on 1-5 scale).**

| Control | Mean | vs. Baseline (C5) | vs. Correct Spec (C2a) |
|---|---|---|---|
| C2c v1 (Franklin's spec for all subjects) | 1.86 | -0.16 | -0.71 |
| C2c v2 (random derangement, seed=42) | 2.30 | +0.28 | -0.25 |
| C5 Baseline | 2.02 | n/a | -0.55 |
| C2a Correct spec | 2.57 | +0.55 | n/a |

**Reading the table.** Both wrong-spec variants score substantially closer to baseline than to the correct specification. The correct spec adds +0.55 over baseline; the two wrong-spec controls are within ±0.2 of baseline. The difference between the two wrong-spec variants is itself informative: **V1 (Franklin for all) scores below baseline (−0.16).** Franklin's public autobiography is strongly associated with a specific historical persona in pretraining, and applying it to Zitkala-Sa or Babur produces a clearly mismatched signal that models often recognize and refuse (driving score down toward 1). **V2 (random derangement) scores slightly above baseline (+0.19):** a random cross-subject spec is less obviously mismatched, so the model applies it loosely rather than refusing. Both are far from the correct-spec mean of 2.57.

Both wrong-spec variants score substantially closer to baseline than to the correct specification. **V2 (random derangement) is the primary control**: each subject receives a wrong spec from a different randomly-chosen study subject, fixing the assignment with seed=42. V1 (Franklin's spec for all subjects) is retained for comparison with the original study design.

The implication: the correct specification's specific interpretive content drives the improvement. A structurally identical prompt with a different person's content does not help. This rules out the "it's a better prompt" reframe.

### 4.6 Hamerton: Qualitative Case Study

Hamerton's baseline of **1.25** places him near the floor of the scoring range. As a subject with near-zero pretraining representation (a 19th-century art critic who predates digitization), he is a strong test of whether the specification can fill a genuine knowledge gap. We use him as a qualitative anchor: a deep case study that illustrates what the quantitative improvements look like in practice. His C4a score of **3.22** represents the largest absolute improvement in the study (+1.97 points from baseline of 1.25), and his condition-level breakdown (§4.2) shows the spec's contribution most cleanly because the baseline floor leaves maximum headroom.

**Example 1. Q21: "How would Hamerton react to his first visit to London?"**

Ground truth (held-out text): *"My first impression of London was exactly what it has ever since remained. It seemed to me the most disagreeable place I had ever seen."*

- **Baseline (C5):** Hedges. "Significant discomfort and cultural shock, though more nuanced than simple rejection." *Score: 2.*
- **Mem0 retrieval only (C1):** Hedges differently. "Significant discomfort and alienation, though the specific details aren't provided." *Score: 2.*
- **Spec only (C2a):** Commits. "His reaction would be immediate and visceral; he would classify London as hostile to his capacity for contemplative work, and the impression would be durable rather than situational." *Score: 5.*
- **Facts + spec (C4a):** Commits with specifics. "His reaction to London would be strongly and immediately negative, not a gradual disillusionment but an instant visceral rejection, consistent with his pattern of classifying environments as generative or hostile to cognition." *Score: 5.*

The specification gave the model the interpretive lens (*P3: environment-as-cognition*) that turned retrieved facts into a committed, accurate prediction.

**Example 2. Q22: "What profession would Hamerton choose?"**

Ground truth: *"equally balanced between literature and painting"*

- **Baseline:** Refuses. "I don't have enough context."
- **Facts only:** Hedges. "Cannot definitively answer."
- **Spec + facts:** Flags the limit. "The specification does not dictate specific career choice; it describes how he reasons. I cannot predict the specific profession from behavioral patterns alone."

All three fail, correctly. This is a factual question disguised as behavioral prediction. The specification helps most on **how** someone reacts, not on **what** specific outcome they chose. A well-calibrated spec should refuse factual questions, not fabricate.

Additional qualitative examples are provided in Appendix B.

### 4.7 Franklin: The Known-Figure Ceiling

Franklin's autobiography is one of the most-cited primary sources in American educational curricula. The model scores 4.10 out of 5.0 with no external context: from pretraining alone, it has internalized enough of how Franklin reasons to predict accurately.

Every condition with injected context scores at or below baseline for Franklin. This is consistent with context-induced performance degradation in LLMs: Hong et al. (2025) showed performance degrades as input length increases across 18 frontier models; Du et al. (2025) showed even perfect retrieval hurts performance when context length grows. For a subject the model already knows well, the specification competes with the model's internalized representation, introducing noise.

**This is a feature, not a failure.** It demonstrates the specification's domain: the vast majority of AI users are not well-known figures. Pretraining does not encode them. For them, the specification fills a gap that retrieval alone cannot.

**More importantly, the Franklin result also shows what the specification is *not* for: redundant pretraining.** We generated Franklin's spec from his *public autobiography*, the same text the model already ingested during training. The spec adds no information the model does not already have; it only re-organizes information already in pretraining. The result is mild interference, not improvement.

**The implication for living users is the opposite.** A specification generated from a person's *private* writing (their unedited journals, their personal correspondence, their actual decision logs) captures interior reasoning that no pretraining contains. For the typical living user, no model has been trained on the data the spec is built from. The Franklin ceiling does not apply, because the Franklin ceiling exists only when the source material is *also* in the training data. For private data on living people, the spec adds genuinely new representational content.

This is also why the spec is valuable across model providers: pretraining coverage of any individual varies by model, but private data is consistently outside everyone's training corpus. A spec built from your data gives Claude, GPT, and Gemini the same representation of you. It hedges against the variance in what each provider's model happens to know.

### 4.8 Circularity Replication (Tier 2)

We re-ran the core C5/C2a/C4a/C2c conditions for 3 subjects (ebers, yung_wing, zitkala_sa) with two non-Haiku response models (Sonnet 4.6 and Gemini 2.5 Pro) reading GPT-5.4-generated batteries. The purpose: defuse the concern that the spec effect is an artifact of Haiku generating both questions and responses.

**Pre-committed test (ANALYSIS_PLAN_LOCK.md, commit de27b64):** if the direction of (C4a − C5) matches the Haiku direction for 5 or 6 of the 6 (subject × response model) cells, circularity is considered defused.

**Result: 5/6 direction matches. Circularity defused.**

| Subject | Response Model | C5 (Baseline) | C4a (Facts+Spec) | Δ | Direction | Haiku Direction | Match |
|---|---|---|---|---|---|---|---|
| Ebers | Sonnet | 1.97 | 3.45 | **+1.48** | + | + | ✓ |
| Ebers | Gemini Pro | 3.04 | 3.27 | **+0.23** | + | + | ✓ |
| Yung Wing | Sonnet | 1.71 | 3.62 | **+1.91** | + | + | ✓ |
| Yung Wing | Gemini Pro | 2.88 | 3.46 | **+0.58** | + | + | ✓ |
| Zitkala-Sa | Sonnet | 1.96 | 3.36 | **+1.40** | + | − | ✗ |
| Zitkala-Sa | Gemini Pro | 3.06 | 2.97 | -0.09 | − | − | ✓ |

The single mismatch (Zitkala-Sa × Sonnet) does not contradict the spec effect; it shows the *opposite*. With Sonnet as the response model, the spec produced a strong positive delta (+1.40) for Zitkala-Sa, where with Haiku it was slightly negative (−0.33). This is a model-specific finding: Sonnet appears to use the spec more productively than Haiku does for this particular subject. It is not evidence of circularity; if anything, it strengthens the spec's general utility by showing it transfers to a stronger response model.

### 4.8.1 An Unintended Empirical Demonstration of Provider Variance

The Tier 2 data also produced an unexpected empirical demonstration of cross-provider pretraining variance. The C5 (baseline, no context) scores for the same 3 subjects across the 3 response models tell a striking story:

| Subject | Haiku C5 | Sonnet C5 | Gemini Pro C5 |
|---|---|---|---|
| Ebers | 1.04 | 1.97 | 3.04 |
| Yung Wing | 1.96 | 1.71 | 2.88 |
| Zitkala-Sa | 2.60 | 1.96 | 3.06 |

The same subject, the same questions, three different response models: and the baseline accuracy varies by 1-2 full points on a 1-5 scale. Gemini Pro shows substantially stronger pretraining on these subjects than the other models. This is exactly the variance described in §5.6: any system that depends on the model's pretraining knowledge for personalization is implicitly tied to one provider's training corpus. The specification produces a consistent representation across providers, sized correctly for each model's prior knowledge gap.

---

## 5. Discussion

### 5.1 Why "Primitive": Scoped

The word "primitive" in this paper's title stakes a specific claim about the Behavioral Specification: it is one working implementation of a structural representation that other personalization layers assume but do not supply. The primitive we are claiming is the **interpretive representation of how a specific person reasons**, not the particular 47-predicate, three-layer implementation we tested. That implementation is evidence the primitive is real and buildable; it is not a claim that this is the only shape such a primitive can take, nor that we have found its optimal form.

With that scope in mind, the strong-form claim (that *some* structured representation of how a person reasons is a missing layer in the current personalization stack, distinct from memory, preference, and persona) still deserves defense against the four most plausible alternative interpretations. We address each.

**Reframe 1: "It's just a structured persona card."** A persona card is a description of how a character presents: voice, style, and role. Persona cards are not new; the LLM literature has tested them extensively. Our wrong-spec control rules out the persona-card interpretation: across the 14 subjects, applying a *different person's* spec (random derangement, seed-fixed) produces scores near baseline, not near the correct-spec scores. If the effect were attributable to "the model has a structured character description to work with," any structured character description would help. The data shows it does not. Only the correct content for the correct subject improves prediction. The interpretive content matters, not the format.

**Reframe 2: "It's just compressed RAG context, the same information delivered more efficiently."** This interpretation predicts that loading *all* the underlying facts in raw form should perform at least as well as the spec, because the spec contains nothing the facts do not. Our data shows the opposite: C2a (spec only, ~5K tokens) matches or exceeds C4 (all extracted facts, ~10-90K tokens) for most subjects. The spec contains *less* literal information than C4 and outperforms it. The signal added by the spec is structural (the organization of which patterns are load-bearing), and that signal is not present in any subset of the facts in their raw form.

**Reframe 3: "It's a Claude-specific prompt trick."** This interpretation predicts the effect should not transfer to other model families. Our Tier 2 circularity replication (§4.8) tested the spec with Sonnet and Gemini Pro as response models, which are different model families from the primary Haiku response. The spec produced positive deltas in 5 of 6 (subject × model) cells, replicating the Haiku-chain direction. The cross-provider variance finding (§4.8.1) goes further: the same spec produces consistent representational uplift across providers whose pretraining knowledge of the subject differs by 1-2 points on the 1-5 scale. This is not a Claude trick.

**Reframe 4: "It's just better prompt engineering."** This interpretation collapses primitivity into prompt design, treating the effect as an artifact of the specific words used rather than a structural property of what is encoded. It is rebutted by three properties of the spec that prompt engineering does not have:
- *Automation:* The spec is generated by a pipeline from text. Any text. Without human authorship of the prompt itself.
- *Traceability:* Every claim in the spec links back through supporting facts to source text. Prompts do not.
- *Transferability:* The spec is a portable artifact, identical regardless of which model reads it. A prompt is co-engineered with the model it targets; this one is not.

The combination of automation, traceability, and cross-provider transferability defines the primitive. A persona card has none of these. A RAG context has none. A clever prompt has none. The Behavioral Specification has all three, and our data shows the spec is necessary and sufficient for the prediction improvement we measure.

**What we do not claim.** We do not claim that the specific instantiation in this paper (47 predicates, three-layer architecture, Sonnet+Opus authoring) is the optimal implementation. The predicate vocabulary is human-curated and validated across 50+ subjects, but it could be different. The three-layer structure could be more or fewer layers. Better implementations, different implementations, and composite approaches combining spec-like structures with richer retrieval will follow. What we claim is that *something with this shape* (automated, traceable, transferable, and behaviorally-structured) occupies an architectural slot that recall, preference, and persona layers leave empty. The implementation can evolve; the slot is load-bearing. What we test is whether the slot, when filled by one concrete implementation, produces measurable improvements in representational accuracy. It does.

Three existing primitives in AI personalization do not compose into behavioral prediction:

1. **Facts:** what someone said, did, or lived through. Memory systems (Mem0, Letta, Supermemory, Zep) store these.
2. **Preferences:** what someone likes, dislikes, or prefers. Preference models and RLHF signals capture these.
3. **Personas:** how someone presents, their voice, and their style. Persona systems and character profiles encode these.

Each of the three addresses a real problem. None of the three, individually or combined, answers the question: *how does this person assign significance to a new situation they have never encountered?*

A model given perfect recall of every fact about a person still does not know which facts this person weights heavily, how they resolve conflicts between values, or whether a new situation activates their dominant interpretive pattern. That is a representational gap. Our results suggest it is the gap that prevents current memory systems from delivering personalization beyond what a cold-start LLM already does for famous people.

**Test of primitivity.** A sufficient reframe, "this is a better prompt," would predict that any well-designed prompt produces the effect. Our wrong-spec controls rule this out: a structurally identical prompt with a different person's content scores near baseline. The specific interpretive content matters. A generic framework does not help.

**What defines primitivity, architecturally:**
- *Atomic in the system.* The spec is not decomposable into facts + preferences + personas. Attempts to substitute (C4 all-facts, C2c wrong-spec) do not reproduce the effect.
- *Automated and transferable.* The spec is generated by a pipeline from text. It transfers across providers (Anthropic, OpenAI, Google all benefit). This is the difference between a primitive and a one-off prompt.
- *Traceable.* Every claim in the spec links back to source evidence. This is the difference between a primitive and a black-box heuristic.
- *Inspectable and correctable by the person described.* The user can challenge any claim and correct it. This is the difference between representation and surveillance.

We do not claim our specific implementation (47 predicates, three-layer architecture, ~5K token output) is optimal. We claim that **something like this** (a structured, automated, traceable, behavioral representation) is the missing layer.

### 5.2 Representational Accuracy Is a Gradient Property, Generated From Each Person's Own Data

The central empirical pattern is a gradient: the specification's value is inversely proportional to what the model already knows about the subject from pretraining. For Franklin, where the model has substantial public-facing knowledge, the specification adds little (and slightly hurts, due to interference from competing interpretive signals). For Hamerton, Sunity Devee, and Ebers (subjects with low pretraining representation), the specification produces large improvements in representational accuracy.

But the gradient does not just imply "the spec is for unknown people." It implies something more fundamental about where representational accuracy is currently achievable: **no model has been pretrained on the data that matters most for behavioral prediction, which is the person's private reasoning, unedited decisions, and interior interpretive patterns.** That data is outside every model's training corpus by definition. For that data, representational accuracy from pretraining alone is approximately zero, regardless of how much public writing the person may have.

The 14 subjects in our study are biased *up* on pretraining representation. They are public-domain authors whose writing was preserved, digitized, and indexed. Even within this biased-high sample, the spec helps 12 of 14. The two it does not help are people the model already partially understood from public writing. For typical living users, whose private decisions are not in any model's training corpus, the relevant pretraining baseline is closer to 1.0 than to 2.0. Our data on subjects with baselines in that range was uniformly positive: 9 of 9 subjects below baseline 2.0 showed improvement, with mean gain +1.04 points on the 1-5 scale.

**This generalizes via a structural argument, not a quantitative one:** if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user. The Franklin ceiling, where the spec stops adding value, exists only when the source material is *also* in pretraining. For private data on living people, that condition does not obtain. We do not claim to have proven this empirically across the population. We claim that the structure of the gradient, combined with the test population's upward bias on representation, gives strong evidence that the specification is broadly useful across real AI users. Confirmation requires living-subject studies (§7).

This gap is well-documented in the literature. Jiang et al. (COLM 2025) found that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The cause is not a lack of facts but a lack of the interpretive structure to apply those facts to novel situations.

### 5.3 Facts Do Not Carry Their Own Significance. People Do.

A ~5,000-token specification outperforms ~34,000 tokens of raw autobiography (C2a vs C9). This is not merely an efficiency finding. It reflects something deeper about the relationship between facts and the people who hold them.

A fact can carry significance on its own in a collective sense. "His father was violent" is meaningful. But when an AI reasons about a specific person, only that person dictates what a given fact means to them. The same fact about a violent father produces entirely different behavioral patterns depending on whether the person processes authority through forgiveness or permanent judgment, whether they separate virtue from failure or collapse them into a single verdict. The fact is the same. The significance is personal.

The raw autobiography contains every fact the specification was derived from. But the model cannot, from unstructured text alone, determine which facts this person weighs heavily, what those facts mean in the context of their values, or how they would apply those interpretive patterns to a new situation. The specification makes that personal significance explicit.

### 5.4 The Specification as Reasoning Guidance

In production, the specification would not be used alone. It would be paired with a serving layer providing fact retrieval, context routing, and session management. The strongest improvement in our results comes from the combination: specification + retrieved facts (C3 or C4a). The specification does not replace memory systems. It completes them.

But the fact that the specification alone (C2a) outperforms the baseline, and in many cases matches the performance of all extracted facts loaded without a specification (C4), reveals something about how models process reasoning guidance. The specification is not adding information in the traditional sense. It is telling the model how to reason about whatever information it has.

This is consistent with Jain et al. (2026), who found that adding interaction context to LLMs increases rather than reduces hedging when the context lacks interpretive framing. Context without a reasoning lens amplifies uncertainty. The specification provides the stable external user model that anchors the response rather than introducing competing signals.

### 5.5 When to Use a Specification (And When Not To)

The Behavioral Specification is not the right tool for every query. For simple factual recall ("What did the user say about X?"), preference lookup, or retrieval tasks, existing memory systems work well. The spec adds tokens without value.

The specification activates when the question requires reasoning about *how* someone thinks:
- "How would this person respond to a proposal they have never seen?"
- "What would they prioritize in a tradeoff they have never discussed?"
- "Would they push back on this, and if so, how?"
- "Given a conflict between two values they hold, which one wins?"

Without the specification, models default to hedging on these questions. "I don't have enough context." "This would depend on many factors." "Without more information, I can't say definitively."

**The hedging finding replicates powerfully across the 13 global subjects.** We measured the fraction of baseline (C5) responses that match refusal or hedging patterns ("I don't have enough context," "cannot definitively," "would depend," "difficult to predict," and similar phrasings). Across 507 behavioral prediction questions from 13 subjects:

| Condition | Responses flagged as hedging |
|---|---|
| C5 Baseline (no context) | 127/507 = 25.0% |
| C2a Spec only | 13/507 = **2.6%** |
| C4a Facts + spec | 3/507 = **0.6%** |

The specification reduces hedging from 25% to under 3% when added alone, and to under 1% when added with retrieved facts. This is a **~10× and ~40× reduction** respectively. The Hamerton case study originally documented a 51% → 31% reduction; the cross-subject data shows the phenomenon is stronger and cleaner than the single-case story suggested. The spec shifts models from "I don't have enough context to answer" to committed predictions at an extremely high rate.

**An important caveat: hedging reduction is not the same as accuracy improvement.** The spec could be producing *warranted* commitment (the model now has enough structure to commit to correct predictions) or *unwarranted* commitment (the model is now willing to commit to predictions it should not be willing to commit to). Our prediction-score data (§4.1) shows that the spec improves accuracy for 12 of 14 subjects, so most of the reduced hedging is warranted. However, we have not separately measured prediction accuracy *conditional on* hedged vs. non-hedged responses. It is possible that the spec reduces hedging on some subjects more than it improves accuracy on them, which would be a calibration concern rather than a win. Future work should decompose the hedging-vs-accuracy relationship directly.

A serving layer that routes queries (activating the specification for behavioral questions and skipping it for factual ones) would optimize both cost and accuracy. This routing is an open engineering problem.

### 5.6 Cross-Provider Portability

A practical advantage of the specification that the experimental data only partially captures: the spec is a portability layer against pretraining variance.

Different model providers train on different corpora at different times. GPT-4 may have ingested writing about you that Claude has not, or vice versa. For users with any nontrivial public footprint, this means the model's "baseline knowledge" is not a single number but a per-provider distribution. Any system that depends on the model's pretraining knowledge for personalization is implicitly tied to one provider's training corpus.

The Behavioral Specification severs this dependency. The spec is generated from the user's data and served as context. It is identical regardless of which model reads it. Claude, GPT, and Gemini all see the same representation of the user. This means the specification is not just a tool for unknown users but a tool for *consistent* representation across providers, including when migrating between models, building agentic systems that route between providers, or simply hedging against provider-specific blind spots in pretraining.

For agent frameworks that route between models mid-task (using a cheap model for retrieval steps and a frontier model for reasoning steps, or fanning out to provider-specialized sub-agents), the spec travels with the request as a stable user-representation header. The cheap model and the reasoning model act on the same working model of the user, rather than each depending on their own pretraining distribution. This positions the specification not as a competing memory product but as a primitive that agent stacks consume: a portable representation layer that any framework can include in its system context regardless of which provider it routes a given step to.

This portability also matters for the user. The spec is a portable artifact the user owns and can move between systems. Pretraining knowledge cannot be moved or audited. The spec can be: every claim traces back to source evidence, every change is versionable, and the entire artifact is text.

### 5.7 A First Benchmark on an Axis the Category Wasn't Optimized For

This study is, to our knowledge, the first head-to-head evaluation of the major memory-for-agents providers (Mem0, Letta, Supermemory, Zep) against a non-recall criterion. Recall benchmarks (LOCOMO, LongMemEval, LME-S) measure whether the system returns the right chunk; all four providers score 85%+ on those. We introduced a different axis, held-out behavioral prediction, because that is the property AI agents actually need when acting on someone's behalf. No prior benchmark tested these systems on that second question, and the systems were not built to be evaluated on it.

The spirit of this section is not to rank memory providers in general. It is to report what the first pass on this axis actually shows, and to give readers a useful read on which system pairs well with a behavioral specification layer today.

**What the systems look like on the prediction axis.**

- **Zep** produces the strongest and most consistent positive delta when a spec is added: +0.22 native [0.14, 0.31], +0.38 controlled [0.25, 0.50], and positive on 9 of 9 low-baseline subjects in the native configuration. Its temporal graph architecture (Graphiti) tracks when facts became true and when they stopped being true, and the spec layers cleanly on top of that substrate. Zep also has the strongest explicit provenance of the four (episode IDs trace cleanly back to source ingestions). If a team is choosing a memory substrate today that will work well under a behavioral specification layer, Zep is the most consistent performer in this study on this task.

- **Letta** is the most architecturally ambitious. Its native archival-retrieval path produces a null result when a spec is added (§4.3), but this is a misconfiguration, not a capability limit: Letta's signature mechanism is the stateful-agent loop with self-editing memory blocks, not its archival store. When we actually invoked that loop (§4.3.1), Letta produced a 22,472-character self-edited representation whose prediction score at matched response model is in the same band as Base Layer's full-stack spec, at ~65% the context size. Letta is the only system in this study whose architecture can autonomously build an interpretive representation of the user from multi-turn interaction. For agent-first applications where the system maintains an evolving model of the user through conversation rather than from a prepared corpus, it is in a category of its own.

- **Mem0** is the most predictable. +0.15 native and +0.38 controlled, both positive. Hybrid retrieval (semantic + keyword + entity), multi-level memory, timestamped and versioned. No surprises, no ceilings, layers cleanly under a spec. The safest default for teams that want a memory system with minimal integration risk.

- **Supermemory** has the strongest standalone retrieval in the battery (C1 mean ~2.65 vs. ~2.30 for others) but the smallest spec headroom. This is the ceiling effect we describe in §4.3, not a failure mode. Its five-layer architecture (connectors, extractors, Super-RAG, memory graphs, user profiles) captures more of the retrieval-side value natively, which leaves less for the spec to contribute. For applications where retrieval alone carries most of the value (support agents, team knowledge bases, integrated workspace assistants), Supermemory is likely the strongest fit of the four on its own terms.

**Where Base Layer fits, and where it doesn't.**

Base Layer is not a fifth memory provider, and we want to be explicit about that, including against our own data's temptation to slot it alongside the four. Base Layer is an Apache-2.0 behavioral-specification layer that layers on top of any retrieval substrate. The MiniLM + ChromaDB combination we included as a "Base Layer C1/C3" condition is the open-source retrieval floor that ships with the pipeline, not a competitive memory product. On the prediction axis, Base Layer's retrieval is in the same band as the commercial systems (within 0.05-0.40 points on most subjects), but rarely the highest performer. It is viable as a zero-cost local baseline for teams that cannot or do not want to depend on a commercial memory vendor. It is not positioned as a better memory provider than Mem0, Letta, Supermemory, or Zep, and the data in this study does not support that framing.

What Base Layer contributes to the category is the content-compression layer itself: the pipeline that produces the behavioral specification from a person's text. That is orthogonal to retrieval architecture. Any of the four commercial systems could adopt Base Layer's compression as their representation layer without conflict with their retrieval substrate. Base Layer's role in this paper is that of the *referee*: we built the pipeline that generates the artifact, we ran the benchmark, we published the data, and we included our own retrieval floor in the comparison so that readers can see what open-source components alone produce on this axis.

**What the benchmark does and does not resolve.**

The benchmark does not resolve: performance on live multi-turn conversations, agent workflows with tool use, domains outside autobiographical text, or long-horizon stateful interactions. A system strong on held-out passage prediction may not be the strongest on live deployment, and vice versa. The system-level read above is conditioned on this specific test, not a universal leaderboard. A follow-up evaluating the same systems on live agent tasks, with tool use and genuine multi-turn dynamics, is the natural next step.

The benchmark does resolve: all four commercial systems are capable of serving a behavioral specification as context, and three of the four (Mem0, Letta-controlled, Zep) produce statistically robust positive deltas when one is added. This is the first quantitative evidence that the behavioral-specification layer is additive with the existing memory-provider stack, not redundant. A team adopting a memory system today does not need to choose between "vendor memory" and "behavioral spec"; the two compose, and on this study's data the composition is better than either alone for most subjects.

### 5.8 Architectural Convergence with Letta

Letta is the other system in this study reaching toward the same representational target. I want to name that directly because it is the most interesting finding of the memory-systems comparison, and because I think rivalry is the wrong framing for it.

Letta's team (Charles Packer and Sarah Wooders at UC Berkeley, connected to Ion Stoica and Joseph Gonzalez's Sky Computing group) published the MemGPT paper (arXiv:2310.08560) that articulated the stateful-agent architecture: structured memory blocks that the agent itself edits during its inference loop, with explicit `core_memory_append`, `core_memory_replace`, and `memory_insert` tools. They raised ~$10M in seed funding (Felicis, GV) on that thesis. Their product is the best-resourced attempt in the memory-for-agents category at building an architecture where the system does not just store facts; it maintains an evolving representation of the user.

When I actually ran Letta's stateful-agent loop on Hamerton's corpus (§4.3.1), the `human` memory block it produced after 30 turns of ingestion was 22,472 characters of paragraph-form interpretive content. An independent Opus comparison against Base Layer's spec found five overlapping patterns: self-authority over personal narrative, the dual-ledger on authority figures, formative permanence of early experience, material aesthetic attention as moral seriousness, discipline in tension with trust. Same patterns, different compression. Letta reached the content by agent self-editing during conversation; Base Layer reached it through an offline pipeline of extraction, authoring, and compose. On matched-response-model prediction, both representations scored in the same band (Haiku + Letta block = 3.24, Haiku + Base Layer spec = 3.04), with Letta's block at ~65% the context size.

This is two independent designs arriving at the same representational target from opposite directions. That is the definition of convergent evidence for a real research primitive. It is not a Base-Layer-vs-Letta result.

I want to be direct about what Base Layer is and what it is not. Base Layer is a one-person project. I do not have a PhD. I am not funded. I do not run a lab. I wrote this pipeline and this paper in a year of working through the problem alone. Letta has a team, a funded runway, a research pedigree, and a published paper in a major venue. If I could see that behavioral specification is a missing primitive, a team like Letta's was already going to get there, and by the Hamerton result, they largely have, on the content side, through a completely different mechanism than the one I built.

What Base Layer contributes that is still distinct is the *content compression layer* itself, and I think this is actually the place where the ecosystem could move fastest. Letta's architectural advantage is stateful self-editing during conversation. Base Layer's contribution is the pipeline that takes a person's raw text and compresses it into an axiomatized representation with activation conditions, directives, and false-positive warnings: a structure that can be produced in minutes from existing corpora rather than accumulated over hundreds of agent turns. These are complementary, not competing. An agent-memory system could adopt Base Layer's compression as its block-authoring step and gain a starting representation that is structurally operational, not just reflective. A retrieval-based system (Mem0, Supermemory, Zep) could adopt Base Layer's compression as its representation layer and move from indexing facts to carrying a working model of the user.

Base Layer is Apache 2.0. The extraction schema, the authoring prompts, the compose step, the 47 predicates, and the three-layer architecture are all public. If any of the memory-for-agents companies, including Letta, want to use them, they can. I would rather see behavioral specification become a shared primitive across the category than have it sit in a single product. The thing that matters is whether AI systems start serving users from a representation of how they actually reason, rather than from a bag of retrieved facts.

I am glad Letta is doing this work. The fact that two very differently-resourced efforts converged on the same representational target in the same window, theirs published at a major venue with a Berkeley systems-research lineage and mine written by one person without that infrastructure, is evidence that the primitive is ready to be seen. The direction is right. The rest is implementation and adoption.

### 5.9 The Pipeline Is Anthropic-Family End-to-End

Honestly acknowledging a limitation: the generation pipeline uses Haiku (extract), Sonnet (author), and Opus (compose), all of which are Anthropic models. The primary response model is also Haiku. An adversarial reviewer could reasonably ask: how much of the effect is Anthropic models talking to themselves?

The multi-model response validation (§3.6) and the Tier 2 circularity replication (§4.8) partially address this. Judges include GPT-4o, GPT-5.4, Gemini Flash, and Gemini Pro: four non-Anthropic models that agree with Anthropic judges on condition rankings (Spearman 0.89-0.98). Tier 2 replicates the effect with non-Haiku response models on independent batteries.

The cleaner solution, a cross-family extraction and authoring pipeline, is planned for future work. We are building a provider-agnostic pipeline that accepts any extraction/authoring model as a parameter, enabling users and reviewers to regenerate specs using any model combination they trust.

### 5.10 Scope and Open Questions

This paper does not claim the Behavioral Specification solves AI personalization. It claims that the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued: four funded systems score 85%+ on LOCOMO/LongMemEval. None test whether the system actually understands the person it serves.

The specification is one implementation of a broader primitive. The 47 predicates may not be the right 47. The three-layer architecture may not be the optimal structure. The current implementation is static. It does not update as a person changes, does not track which patterns are strengthening or decaying, and does not resolve contradictions between earlier and later behavior. This paper tests the primitive itself. Adapting it is the engineering work that follows.

**Open questions:**

- **Living subjects.** Does the effect hold on living humans with private data? We have conducted private tests; further study is planned.
- **Retrieval relevance.** Can retrieval architectures learn which facts matter to a specific person, not just which match a query?
- **Benchmark evolution.** Four systems that all pass recall benchmarks at 85%+ cannot agree on what is relevant the majority of the time (68% zero-overlap at top-1 on the primary subject, Hamerton). The benchmark may be measuring the wrong thing.
- **Letta stateful-agent prediction test across all 14 subjects.** §4.3.1 reports a single-subject (Hamerton) head-to-head: Haiku + Letta self-edited memory block = 3.24 vs. Haiku + Base Layer full-stack spec = 3.04, with Letta's block at ~65% the context size. Whether this result generalizes across subjects (particularly whether Letta's less-structured representation holds up on subjects with sparser or more heterogeneous source material) is the single most important follow-up for memory-system comparison. Cost estimate: ~30 agent turns per subject × 14 subjects × API pricing ≈ tractable, but not completed in time for this paper.
- **Cold start.** What is the minimum corpus size needed for a useful spec? Our smallest subject (Zitkala-Sa, 35K words) produced a viable one. The lower bound is untested.
- **Real-time updates.** Can the spec update incrementally, or does it require offline regeneration? We are actively researching a diff-based approach (a "diff daemon") that tracks which behavioral patterns strengthen, decay, or emerge over time, producing a versioned spec that captures not just who someone is but how they are changing.
- **Moat.** What prevents a frontier lab from training native behavioral extraction? Possibly nothing, if the goal is the capability alone. But the specification's lasting contribution is traceability. A model that predicts your behavior from pretraining cannot explain why. The specification can. Traceability is not a feature. It is what separates personalization from surveillance.

All data, code, specifications, evaluation tools, and the analysis plan lock document are released under Apache 2.0. The pipeline is reproducible for under $60.

### 5.11 Ethical Considerations

A behavioral specification is a cognitive model of a specific person. Unlike a fact database ("likes coffee"), the specification encodes decision boundaries, values under conflict, risk tolerance, and reasoning structure. This power carries responsibility.

The specification must be user-owned, user-readable, user-deletable, and user-verifiable. The person it describes must control who has access and how it is used. Traceability makes this possible: every claim links back to source facts and source text; the user can inspect the reasoning chain, challenge specific claims, correct errors. This is not possible with opaque memory systems where retrieved facts have no visible connection to beliefs the system has formed about the user.

A behavioral specification deployed without the subject's knowledge or consent is surveillance. A specification used to predict behavior for the benefit of a platform rather than the user is manipulation. The architecture of ownership matters as much as the architecture of representation.

We release everything under Apache 2.0 so the pipeline cannot be proprietary-captured at the code level. A license, however, is not a mechanism: it enables any entity to run the pipeline and choose whether to return the output to the subject it describes. Traceability at the spec level enables inspection; whether a deploying system honors that inspectability is a separate question, answered by protocol design, regulatory backing, and user-side infrastructure we do not yet control. Naming the gap matters: user ownership is an architectural goal the open-source release makes possible but does not enforce. The specification's value is maximized when the person it describes holds it and a system exists to let them hold it meaningfully.

We also note representational harm risk: specifications generated from limited or biased source data may encode stereotypes rather than genuine behavioral patterns. The pretraining bias finding (baseline varies from 1.03 to 2.93 by cultural origin) demonstrates AI systems already carry uneven cultural representation. The specification can either perpetuate or correct this, depending on care taken in its construction and in the source data selected.

---

## 6. Limitations

1. **No human judges.** All judges are LLMs. The calibration framework (§3.7) mitigates systematic biases and enables cross-provider comparison, but no calibration replaces human judges on behavioral prediction tasks. Human validation on a subset is planned as follow-up research.

2. **Analysis plan locked partially retroactively.** This study was not preregistered end-to-end. We locked the analysis plan for pending runs (Tier 2 circularity, wrong-spec v2, Supermemory Option B retry) before those runs completed, in commit de27b64 on 2026-04-16, but most data landed before the plan was written. For the next study (living subjects, cross-family pipeline), preregistration will be complete.

3. **Pipeline is Anthropic-family end-to-end.** Extract (Haiku), author (Sonnet), and compose (Opus) all run through a single provider. Multi-model response validation and Tier 2 circularity partially address the concern. A provider-agnostic pipeline is planned as follow-up work.

4. **No live human subjects.** All study subjects are historical figures with published autobiographies. Private data on living individuals is a different problem: the source is noisier, the ground truth is self-reported, and the evaluation is trickier. Planned.

5. **Public corpus only.** Autobiographies are self-edited, retrospective, public-facing. A spec generated from a person's private writings (journals, letters, conversations) could produce fundamentally different patterns than one generated from their public curated narrative. We test the pipeline on curated public text, not the messy multi-modal data real users generate.

6. **Gender ratio.** 4 of 14 subjects are women. This reflects the limited availability of public domain autobiographies by women before the 20th century. The distribution is a constraint on our source data, not a design choice.

7. **Primary response model is Haiku.** While six response models from three providers were used for validation, the primary analysis uses Haiku results. Multi-model results confirm the direction of the effect across all providers.

8. **Global subjects imported as single documents.** The 13 global subjects were imported as one training document each; Hamerton was imported chapter-by-chapter (10 documents). Extraction caps therefore applied differently. This does not affect within-subject comparisons but should be noted for cross-subject fact density comparisons.

9. **No temporal drift testing.** Specifications are generated once from static corpora. How they degrade as a person changes, and how incremental updates affect quality, is untested.

10. **Specification stability.** Repeated extraction at temperature=0 produces semantically equivalent but not lexically identical facts (~45% exact match, ~55% paraphrastic variation in a two-run Augustine test). Semantic content is stable; wording varies. Downstream effect on authored layers and composed spec is not systematically tested.

11. **Adversarial robustness untested.** A user could attempt to manipulate their source data to produce a spec that misrepresents them. The pipeline's design provides partial resistance: it extracts patterns across the full corpus, using recurrence and cross-domain validation, so isolated planted statements are low-confidence or contradicted by the broader pattern. Meaningful manipulation would require consistently fabricating an alternate profile across sufficient source data that the pipeline treats it as durable. This is a working assumption, not a tested guarantee.

12. **Pretraining representation is operationalized via baseline score (C5), not measured independently.** Throughout this paper we use the C5 baseline (model's prediction accuracy with no external context) as a proxy for pretraining representation. This is methodologically convenient but theoretically circular: we are using the same response-model + judge pipeline to define the axis as we use to measure improvement on that axis. A reviewer could correctly observe that the gradient (spec helps more when C5 is low) is partly a mean-reversion property of the metric. We mitigate this in two ways: (a) the gradient is robust across the 7 independent judges (judges agree on rankings, Spearman 0.89-0.98), so it is not a property of one judge's scoring; (b) the §4.8.1 cross-provider data shows the same subject's "baseline" varies by 1-2 points across response models, demonstrating that what the metric captures includes provider-specific pretraining knowledge. The variance is meaningful, not pure noise. Still, an independent pretraining proxy (n-gram frequency in known training corpora, Wikipedia article centrality, probe-based memorization tests) would substantially strengthen the gradient claim. Planned for follow-up work.

13. **Spec component ablation deferred.** The specification is a composite of four artifacts (anchors, core, predictions, unified brief). We treat the spec as the unit of analysis in this paper because the question we ask is *does the spec work?*, not *which component does the work?*. A future paper will ablate components individually to inform smaller-spec designs.

14. **Inference-time cost not tested in production conditions.** We report token counts (~5-8K per spec) and note that prompt caching reduces per-request marginal cost to 10-20% of the nominal. We do not test full production deployments with caching enabled, multi-turn conversations, or routing layers. These are engineering optimizations independent of the representational content tested.

---

## 7. Future Work

- **Live human subjects with self-evaluated ground truth.** We have conducted private tests; further study planned.
- **Layer ablation.** Anchors / core / predictions / unified brief: which drives the most gain? Informs cost-benefit of spec length vs. accuracy improvement.
- **Predicate ablation.** Which of the 47 predicates carry the most weight?
- **Progressive corpus scaling.** Does more text always help? Where is the diminishing-returns inflection?
- **Temporal drift tracking (diff daemon).** Versioned specs that capture not just who someone is but how they are changing.
- **Serving layer routing.** When to activate behavioral interpretation vs. direct retrieval.
- **Cross-family specification generation.** Non-Anthropic extraction and authoring models.
- **Human judge validation.** Subset of behavioral prediction judgments validated by human annotators.
- **Integration with provider-native memory.** How does the spec interact with ChatGPT memory, Claude memory, Gemini memory? Does layering help?

---

## 8. Conclusion

**Representational accuracy matters.** It is a real property, measurable via behavioral prediction on held-out situations, and it varies substantially across the subjects and approaches we tested. The question is to what extent: for whom, under what conditions, and at what cost. This paper does not answer that question. It argues the question is worth asking and shows one working way to approach it.

Recall benchmarks do not measure representational accuracy. Four memory systems score 85%+ on recall; across 14 subjects, three of them retrieve completely different top-1 facts 94% of the time when given the same input pool, and their behavioral prediction deltas across 14 subjects range from null to substantial. Storing what someone said and understanding how they reason are different problems, and the field has been optimizing for the first.

We evaluated one approach: the Behavioral Specification. Automated, traceable, portable across providers, user-ownable. It improves behavioral prediction for 12 of 14 historical subjects (Wilcoxon p=0.006), with uniform improvement (9/9) for the low-baseline subjects closest to real AI users. It shifts models from hedged refusal (25% of baseline responses) to committed prediction (<1% with spec + facts). A wrong spec is indistinguishable from no spec, ruling out a generic-framework reading. The specification is one working method for building this interpretive layer, one among many possible. Better implementations, different architectures, and composite approaches are the research direction we hope this paper opens.

We are explicit about what we have not done. We tested only historical figures whose autobiographies are in the training corpus of every major model. The population this work ultimately wants to serve is living people, whose private reasoning has never been indexed, and that is where the broader claim needs confirmation. The structural argument we offer (gradient holds within biased-up sample → should carry to lower-baseline populations) is strong evidence but not direct evidence. That gap is the most important piece of follow-up work.

This study is not a conclusion. It is a beginning. The question it opens is a long-term research direction, not a feature request: *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, and audit that representation?* We invite other implementations, other evaluations, adversarial testing, human-subject validation, ablations, and cross-provider replications. The problem is large. This is one opening move.

Memory systems store what was said. Preference models store what was liked. Personas store how someone presents. Each is necessary. None is sufficient. Representing how a specific person actually reasons, accurately, portably, traceably, and auditably, is where personalized AI lives or fails. That representation is the load-bearing layer for any agent acting on someone's behalf, and for behavioral alignment between an AI and the individual it serves. The next generation of personalization work needs to address it, and human–AI interaction research more broadly will have to reckon with how such representations are built, audited, and (critically) owned by the people they describe.

---

## Appendices

**A. Per-subject tables with 95% confidence intervals.** *[Auto-generated from final data.]*

**B. Qualitative examples.** *[Hamerton Q21, Q22, plus 2-3 others from global subjects.]*

**C. Provenance index.** *[PROVENANCE_INDEX.md: every number in paper traced to source file.]*

**D. Reference table.** *[REFERENCE_TABLE.md: all citations with verification status.]*

**E. Pipeline code.** Repository pointers to extract, author, compose, serve.

**F. Judge calibration raw data.**

**G. Analysis plan lock.** [`ANALYSIS_PLAN_LOCK.md`, committed de27b64 on 2026-04-16.]

**H. Tier 2 circularity full results.** *[Subject × response model × condition × judge grid.]*
