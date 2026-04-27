# v11 Comment Extraction — Beyond Recall v10.1 → v11

_Source comments: `docs/beyond_recall_v10_1_draft.docx` + Bavani's review notes 2026-04-27._  
_Edits applied to: `docs/beyond_recall_v11_draft.md` (forked 2026-04-27 from v10.1 baseline).  v10.1 stays release-frozen as the baseline for v11 deltas._

**Total review items:** 183 (173 docx comments + 10 Bavani structural notes)

Each entry below is one item, ordered by appearance in the document. Bavani's items appear at the top because most are structural / cross-cutting and inform how individual line-level comments resolve. Status fields are blank pending review.

---

## Bavani Review Notes (light pass, 2026-04-27)

These are structural / cross-cutting notes, not anchored to specific lines. They inform how the line-level docx comments resolve.

### B1 (Intro: hypothesis-terms mirroring)

**Section:** §1 Introduction

**Comment:**

> Hypothesis statement should mirror the defined terms laid out before it. The current text introduces "intent" when "interpretation" was the key differential for humans. If these are not terms of art in the paper then don't highlight them.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.1 line 21 hypothesis statement rewritten in `beyond_recall_v11_draft.md` (Option C, tightest mirror to defined terms `representational accuracy` and `interpretation`). New text: "The core hypothesis of this research is that representational accuracy of a person's interpretation predicts the AI system's behavioral alignment with that person on novel situations. If the system's model accurately captures how the person interprets, its responses should match the person's documented behavior in situations the system has never seen." "Intent" removed entirely.

---

### B2 (§1.3 emphasis)

**Section:** §1.3 What we found

**Comment:**

> Emphasize "three patterns emerge" in §1.3.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.3 restructured. "**Three patterns emerge.**" promoted to bold standalone lead. Each pattern now gets a bold label header — **Pattern 1 — Interpretation-heavy questions**, **Pattern 2 — Literal-recall questions**, **Pattern 3 — Refusal-triggering questions** — followed by its descriptor and example(s). Pattern 2 (previously mashed into the same sentence as Pattern 3) now has its own paragraph with an inline reference to Yung Wing Q5 (§4.4 Supermemory Example 2) since §1.3 doesn't carry a Pattern 2 example of its own. The three-pattern structure is now visible at a glance. Mirrors the §4.4.2 Pattern 1/2/3 layout already in use later in the paper.

---

### B3 (§2.1 table simplification)

**Section:** §2.1 (Prior Work / Industry Benchmarks)

**Comment:**

> Simplify the table in §2.1.

**Status:** DEFERRED 2026-04-27 (Aarik handling separately)  
**Resolution:** Aarik has already adjusted Table 2.1 formatting himself and provided additional comments on it via the docx review pass. Skipping this Bavani-level fix; the docx-anchored comments on §2.1 will be handled when we reach them in the line-level pass.

---

### B4 (Traceability example)

**Section:** §2 (or wherever traceability is discussed)

**Comment:**

> Consider putting in an example in traceability — i.e. a response grounded in anchors.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** Added a "**Worked example**" paragraph in §2.2 after the abstract audit-chain explanation. Walks the response → anchor → facts → source chain on Sunity Devee using real, verified IDs: anchor **A2** ("Spiritual Integrity Over Social Cost") in `anchors_v4.md:24`, grounded in **F-73** (mother's conscience) and **F-414** (father's conscience). Reader sees the audit chain walked end-to-end. Reuses the §1.3 anchor reference so no new framing to absorb.

---

### B5 (§2 sentence pattern overuse)

**Section:** §2

**Comment:**

> Too many sentences in §2 read "what xyz does and doesn't xyz". Be more direct.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §2.3.1 four subsection headers rewritten to direct positive framings. "What recall measures, and doesn't" → "Recall measures retrievability of facts, not reasoning about them." "What survey-response prediction measures, and why it differs from our target" → "Survey-response prediction interpolates within a structured response distribution." "What persona fidelity measures, and doesn't" → "Persona fidelity measures consistency of self-presentation over turns." "What preference alignment measures, and why it is adjacent but distinct" → "Preference alignment measures whether responses match user preferences." Also rewrote §2.3.1 lede line 202 to drop "what that framing does and does not claim" → "The scope of that proposal is bounded; the rest of this section is precise about what it claims." Body of each block kept its existing distinction prose; only headers + lede changed.

---

### B6 (§2.3.1 formatting flow)

**Section:** §2.3.1

**Comment:**

> Formatting has the first sentence of every paragraph reading as a header. Edit for flow to remove this; change headers to full sentences.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** Four fragment headers in §2.3.1 converted to full sentences while preserving the bold-lead visual scanability. Line 206 "What the held-out design actually tests." → "The held-out design tests a stability assumption." Line 208 "A related open question for production deployment: canonical life events." → "A related open question for production deployment is how to handle canonical life events." Line 218 "The missing axis." → "The missing axis is representational accuracy itself." Line 220 "Implication for future memory-system research." → "The implication for future memory-system research is that single-axis scores are underspecified." The two existing full-sentence leads (line 204 "Prediction is the test, not the goal" + four benchmark leads from B5) were already compliant. Body prose unchanged.

---

### B7 (§3.1 definition placement)

**Section:** §3.1

**Comment:**

> The definition of representational accuracy comes too late. It is already referenced heavily in prior sections.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §3.1 reframed from re-introduction to operationalization. Heading renamed "Representational accuracy" → "Operationalizing representational accuracy". Lede paragraph now explicitly cites §1.1 as the place the term was introduced and positions §3.1 as the operational definition for the methodology: "Section 1.1 introduced representational accuracy as the AI-side property of interest. This section operationalizes the term so the rest of the methodology can refer to it precisely." The §1.1 introduction (line 19) was left unchanged since it already serves as a working definition for §1-§2 readers; only the §3.1 framing was tightened.

---

### B8 (Definitions section)

**Section:** front matter / appendix

**Comment:**

> Consider a definitions section, either in the appendix or as a quick chart for the intro.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** Added Appendix G "Glossary" with 9 terms-of-art entries (alphabetical, declarative): 5-judge primary panel, 7-judge sensitivity panel, Anchors / Core / Predictions, Behavioral prediction, Behavioral specification, Interpretation, Representational accuracy, Tier 1 / Tier 2, Wrong-spec control. Initial draft included condition codes (C2c, etc.), Pattern 1/2/3 labels, post-spec operating level, win rate, low/high-baseline, controlled/native test — all dropped because they're either condition codes already in §1.2/Appendix C.1, descriptive prose, or transparent enough not to warrant glossary entries. §1.1 line 23 paragraph received a single forward pointer: "Defined terms used throughout the paper are collected in **Appendix G** for reference."

---

### B9 (§3.6 Tier 1 / Tier 2 distinction)

**Section:** §3.6 (also referenced in intro)

**Comment:**

> Make the Tier 1 / Tier 2 distinction more explicit. The same point is also flagged in the intro.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** Three edits applied. §1.1 line 83 paragraph rewritten to explicitly label both tiers: "The study is structured into two tiers. **Tier 1 (main study):** ... **Tier 2 (cross-provider directional probe):** ..." §3.6 line 420 lead bolded as "**Tier 1 (main study):** Claude Haiku 4.5 as the primary response model..." §3.6 line 422 bold lead "Tier 2 response-model expansion" → "Tier 2 (cross-provider directional probe)" matching the §1.1 phrasing and the Appendix G glossary entry. The Tier 1 / Tier 2 framing is now symmetric across intro, methodology, and glossary.

---

### B10 (§3.7.3 cross-anchor interpretation rule)

**Section:** §3.7.3

**Comment:**

> The cross-anchor interpretation rule is necessary context to read the findings. Bold it all.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §3.7.3 line 524 fully bolded. Was only the lead "**Cross-anchor interpretation rule.**" with plain-prose follow-on; now the entire rule statement is in bold so it reads as load-bearing context for §4 findings: "**Cross-anchor interpretation rule. A fractional delta that crosses an integer anchor reflects a real shift in the underlying response distribution. A delta that stays inside a single integer band is a within-category shift and a weaker claim.**"

---

## Meta-items (cross-cutting, surfaced during review)

### M1 — ToC / section-title cleanup

**Status:** TRACKING (Aarik flagged 2026-04-27)  
**Note:** Several section titles are wordy and would benefit from a Table-of-Contents pass. First example flagged: §1.1 "Recall Is Not Interpretation. Interpretation Can Be Measured." (two sentences as a heading). Other candidates to be surfaced as we encounter them. Defer the actual title rewrites until the docx-comments walk is complete — many comments may explicitly suggest title changes.

### M2 — Footnote usage for C2c (and other condition-specific extended explanations)

**Status:** TRACKING (Aarik flagged 2026-04-27 during §1.2 batch review)  
**Note:** Aarik observed that none of the docx comments specifically address how footnotes are used for C2c (wrong-spec) condition explanations or other condition-level extended detail. The §1.3 / §4.3 wrong-spec discussion currently uses inline parentheticals for v1 / v2 distinction; some of that detail might fit better as footnotes. Watch for this as we walk §1.3, §4.3, and §3.5; surface a consolidated footnote-usage proposal once the relevant comments have been reviewed.

---

## Docx Comments (anchored)

## Comment 1 (id=7)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:00:00Z

**Comment body:**

> I believ e mem0 is reporting above 90%, need to verify this, likely need a footnote for this specifically, that we got this from their websites.

**Anchored text:**

```
68% to 85%
```

**Surrounding paragraph (full):**

> State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant. Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.1 line 15 range "68% to 85%" → "70% to 93%" with inline pointer "(see §2.1 for vendor-by-vendor numbers and the methodology disputes around them)". Initial draft included a full vendor-recall footnote with per-vendor citations; Aarik pushed back as overkill for §1.1. Final version is the corrected range plus the §2.1 pointer; readers who want the breakdown find it in §2.1's existing prose. Resolves the §1.1 vs §2.1 internal inconsistency.

---

## Comment 2 (id=8)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:01:00Z

**Comment body:**

> Is it an individual, or an intelligence?

**Anchored text:**

```
individual
```

**Surrounding paragraph (full):**

> State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant. Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.

**Status:** CLOSED 2026-04-27 (no change)  
**Resolution:** Aarik confirmed: keep "individual". The paper consistently uses "individual"/"person"/"subject" for the human and "model"/"AI"/"system" for the artificial; "intelligence" would muddle that distinction.

---

## Comment 3 (id=9)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:02:00Z

**Comment body:**

> Vs it must be given contrext on how any individual person interprets? Not just to what facts a person interprets on.

**Anchored text:**

```
it must be personalized to how that person interprets
```

**Surrounding paragraph (full):**

> We use interpretation to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. Think of how viewing situations from different lenses can lead to entirely different interpretations of the same set of facts. This has been shown across the human experience, from the sciences to religion to political affiliations, and by extension to the relative experiences of any individual. Memory is deeply personal. For an AI memory system to serve a specific person, it must be personalized to how that person interprets, not just to what facts they have produced.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.1 line 17 sentence rewritten with hybrid Option A + the modeling distinction from Option C: "For an AI memory system to serve a specific person, it must be given context on how that person interprets, not just on the facts that person has produced. The Behavioral Specification models that interpretation; the language model receives it as context." Folds in the BL-models / LLM-receives split Aarik flagged as interesting.

---

## Comment 4 (id=10)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:08:00Z

**Comment body:**

> Feel we need to give a little more insight on what the behavioral specification is, )one more sentence helping describes what is being extracted and encoding, and how it is different from a fact. We do not need to point out how it varies from a fact, just provide insight on what we me by extracting and encoding behavioral patterns. Perhaps and eg.--- use a short example in line, maybe multiple, truncated with ellipses.

**Anchored text:**

```
behavioral specification: a static document that extracts and encodes a stable representation of a corpus’s behavioral patterns.
```

**Surrounding paragraph (full):**

> We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated large language model (LLM) judges to evaluate the performance of each memory system, on its own and in combination with a behavioral specification: a static document that extracts and encodes a stable representation of a corpus’s behavioral patterns.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.1 line 23 paragraph extended with one explanatory sentence + inline ellipsis examples. Avoided the term "axiomatic" per Aarik's laymanness flag. Added: "The specification captures the recurring patterns in how the subject reasons (for example: 'spiritual integrity over social cost...', 'reform through love...', 'hierarchical deference...') rather than the specific facts of events they lived through. A walked example of the audit chain from such a pattern back to its grounding facts and source passages appears in §2.2." Examples are real Sunity Devee anchors, matching the §2.2 worked example added in B4.

---

## Comment 5 (id=13)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:10:00Z

**Comment body:**

> We have not specified what a response model is prior to this, maybe one comma, the language model being asked to respond to held out questions?

**Anchored text:**

```
a response model.
```

**Surrounding paragraph (full):**

> We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model. The test was whether each system could predict how that specific person would respond in situations drawn from text it had never seen.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2 first-paragraph sentence: "No held-out passage was ever shown to a response model" → "...shown to a response model, the language model being asked to respond." Brief inline gloss per Aarik's shorter phrasing; not a footnote.

---

## Comment 6 (id=14)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:11:00Z

**Comment body:**

> Whether each system, or system variations, conditions?

**Anchored text:**

```
whether each system
```

**Surrounding paragraph (full):**

> We tested the Behavioral Specification across 14 historical subjects, each with a public domain autobiography. For every subject we split the source corpus in half: the training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model. The test was whether each system could predict how that specific person would respond in situations drawn from text it had never seen.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2: "The test was whether each system could predict..." → "...whether each system, under each tested condition, could predict..." Disambiguates system vs. system+condition.

---

## Comment 7 (id=15)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:14:00Z

**Comment body:**

> Why is C4 brought up in this particular context? Is this specifically related to testing raw facrts against a specification. We also did the whole corpus, at that we did who corpuses small enough to easily fit in the context window. Is this not similar to twin2k, in that we test the entire fact repository, as well as dumping the entire training corpus.?

**Anchored text:**

```
Fact extraction (C4) does most of the volume-reduction work; the authored Behavioral Specification adds marginal value at the per-question level rather than at the aggregate mean.
```

**Surrounding paragraph (full):**

> H5. Structured extraction plus authored specification compresses the behavioral-prediction signal at a fraction of the source-corpus footprint. Fact extraction (C4) does most of the volume-reduction work; the authored Behavioral Specification adds marginal value at the per-question level rather than at the aggregate mean.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** H5 dropped the "(C4)" parenthetical at first use. The C-code mapping comes later in the §1.2 conditions table; H5 now reads cleanly without forward-referencing condition codes. Twin-2K side-question Aarik raised is already covered by §2.3.1 + Appendix E and not actionable inline.

---

## Comment 8 (id=16)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:16:00Z

**Comment body:**

> This is a bit convoluted as to what this means. Maybe expand a tad.

**Anchored text:**

```
within-judge mean, then across-judge mean. The
```

**Surrounding paragraph (full):**

> Primary and secondary outcomes. The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a secondary outcome, we report the per-question win rate against the no-context baseline. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the breadth of benefit of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2 aggregation rule: "within-judge mean, then across-judge mean" → "each judge's per-question scores are first averaged to a per-judge per-subject mean, then averaged across the five judges." Less convoluted, walks the two-step rule explicitly.

---

## Comment 9 (id=17)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:16:00Z

**Comment body:**

> Need a , and short explanation

**Anchored text:**

```
unit of inference
```

**Surrounding paragraph (full):**

> Primary and secondary outcomes. The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a secondary outcome, we report the per-question win rate against the no-context baseline. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the breadth of benefit of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2: "The subject is the unit of inference." → "The subject is the unit of inference: every statistic is computed at the subject level first, then aggregated across the 14 subjects." Clarifies what unit-of-inference means in practice.

---

## Comment 10 (id=18)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:17:00Z

**Comment body:**

> Win rate or increase/decrease, assumption would be win rate implies it unequivocally won, vs shows directionality.

**Anchored text:**

```
win rate
```

**Surrounding paragraph (full):**

> Primary and secondary outcomes. The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a secondary outcome, we report the per-question win rate against the no-context baseline. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the breadth of benefit of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

**Status:** RESOLVED 2026-04-27 (applied to v11, Option A)  
**Resolution:** Rebranded the secondary metric from "win rate" to "per-question improvement rate" globally. §1.2 first use updated; §4.2.1 lede + reporting-triplet language + closing pointer all rebranded. Internally consistent with the three-way "improved / tied / worsened" classification. The structural-parallel reference to Chatbot Arena win-rate convention preserved as comparative context.

---

## Comment 11 (id=19)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:18:00Z

**Comment body:**

> So win rate would be improved here?

**Anchored text:**

```
as improved, tied, or worsened
```

**Surrounding paragraph (full):**

> Primary and secondary outcomes. The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a secondary outcome, we report the per-question win rate against the no-context baseline. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the breadth of benefit of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

**Status:** RESOLVED 2026-04-27 (subsumed by C10 rebrand)  
**Resolution:** "win rate" ambiguity around improved/tied/worsened resolved by the C10 rebrand: the metric is now "per-question improvement rate" — explicitly the IMPROVED rate, with TIED and WORSENED reported alongside as the reporting triplet.

---

## Comment 12 (id=20)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:19:00Z

**Comment body:**

> Need to be a bit more layman here

**Anchored text:**

```
directly interpretable measure of the breadth of benefit of a context condition
```

**Surrounding paragraph (full):**

> Primary and secondary outcomes. The primary outcome is the mean prediction score on the 1-5 rubric across a 5-judge primary panel (§3.7), aggregated per (subject, condition) cell via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a secondary outcome, we report the per-question win rate against the no-context baseline. For each question in the battery, we compare the 5-judge primary mean score under a tested condition to the corresponding mean score under the no-context baseline (C5), and classify the outcome as improved, tied, or worsened. We report all three rates alongside the median magnitudes of improvement and worsening. This secondary outcome is a scale-free, directly interpretable measure of the breadth of benefit of a context condition. It is introduced here so the reader can track it alongside mean-score numbers throughout §4; the formal proposal and failure-mode analysis are in §4.2.1.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2: "scale-free, directly interpretable measure of the breadth of benefit of a context condition" → "tells us how often a context helps, not just by how much it helps when averaged." Layman per Aarik's flag.

---

## Comment 13 (id=21)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:20:00Z

**Comment body:**

> This would be convertge on retrieval no?

**Anchored text:**

```
providers converge on
```

**Surrounding paragraph (full):**

> The experiment has two main splits. The first is a controlled test: each memory system is given an identical, pre-extracted fact pool drawn from the training half of the corpus. Holding the input constant lets us measure whether the providers converge on what is most relevant when they see the same facts. The second is a native test: each memory system ingests the raw corpus through its own pipeline, as it would in production. This measures real-world performance when each system is allowed to do what it is designed to do. Running in parallel across both splits is the Behavioral Specification, tested alone and layered on top of each configuration.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2: "Holding the input constant lets us measure whether the providers converge on what is most relevant when they see the same facts" → "...whether the providers' retrieval converges when they see the same fact pool." Aarik's correction: convergence is on retrieval, not on relevance assessment.

---

## Comment 14 (id=23)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:23:00Z

**Comment body:**

> Why are they qualitative shifts. Should setup for the scoring rubric here. Specifically when crossing anchor numbers. May be worth mentioning here.

**Anchored text:**

```
not small numerical adjustments
```

**Surrounding paragraph (full):**

> Predictions were scored on a 1-5 rubric. One-point differences on this scale are qualitative shifts, not small numerical adjustments. Absolute point gains, not percentages, are the informative metric for cross-subject comparison.

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2 rubric paragraph rewritten to set up the cross-anchor interpretation rule (B10): "...scored on a 1-5 rubric where the integer anchors mark categorical shifts in answer quality (full rubric in §3.7). Crossing an integer anchor (moving from 1.8 to 2.4, for example) represents a real change in the kind of answer the model produced..." Em-dashes avoided per project rule; restructured with parens.

---

## Comment 15 (id=24)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.2 What we tested

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:26:00Z

**Comment body:**

> This was done to understand if there are any circularity concerns.

**Anchored text:**

```
A Tier 2 cross-provider directional probe ran 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) on 3 subjects spanning the gradient against GPT-5.4-regenerated batteries (§4.6.1). Claude
```

**Surrounding paragraph (full):**

> The main-study response model is Claude Haiku 4.5 (used across all 14 subjects on every condition). A Tier 2 cross-provider directional probe ran 2 additional response models (Claude Sonnet 4.6, Google Gemini 2.5 Pro) on 3 subjects spanning the gradient against GPT-5.4-regenerated batteries (§4.6.1). Claude Opus 4.6 and GPT-5.4 appear in Tier 2 only as judges, not as response models. The judging panel is 7 LLM-as-judge models across 3 providers (Anthropic, OpenAI, Google). Five non-Gemini judges (Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4) form the primary aggregate. Two Gemini judges (Gemini Flash and Gemini Pro) are reported as a sensitivity check because they systematically inflate absolute scores by approximately 1 point relative to the other five. Including them in the aggregate would widen the spec-effect deltas, not narrow them (§3.7.2), so the 5-judge primary is the more conservative choice for every headline finding. Judges were calibrated on known verbatim matches, paraphrase variants, off-target responses, and length-padded responses to measure each judge’s ceiling behavior, paraphrase sensitivity, and length bias. The judges agree strongly on condition rankings  [...]

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2 Tier 2 framing made layman: "to check whether the result holds when the questions and the response model both come from outside Anthropic." Replaces "test for within-Anthropic circularity" jargon with a plain-English explanation of why Tier 2 was run.

---

## Comment 16 (id=27)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:27:00Z

**Comment body:**

> Needs to be layman. All parenthentical information should be in a footnote here

**Anchored text:**

```
The spec produces a roughly uniform post-spec operating level near 2.46 on C4a. The lift in raw points is largest where baseline is lowest because subjects below that level are pulled up to it. (C4a-level regression on C5: slope +0.04 [−0.24, +0.33], R² = 0.008. The change-score parameterization, Δ_C4a on C5, has a steep slope of −0.96 that is dominated by the coupling identity slope_Δ = slope_level − 1; §4.1 sensitivity.)
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 17 (id=28)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:28:00Z

**Comment body:**

> Need to convert this to layman. This should be a statement on directionality.

**Anchored text:**

```
Wilcoxon signed-rank (paired baseline → facts+spec): p = 0.007 (W = 11, N = 14)
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 18 (id=29)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:28:00Z

**Comment body:**

> Should this be the headline or 3rd?

**Anchored text:**

```
Subjects improving: 12 of 14 overall; 9 of 9 on the low-baseline slice (C5 ≤ 2.0)
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 19 (id=30)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:29:00Z

**Comment body:**

> This should be wrapped into subject improving**

**Anchored text:**

```
Mean Δ_C4a on low-baseline slice: +0.89 points on the 1-5 rubric
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 20 (id=31)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:29:00Z

**Comment body:**

> This should also be rolled into subject improving. It may be Subject improving is main head, then sub head is mean delta on low baseline slice, and per response anchor corssing. We also need this to be layman

**Anchored text:**

```
Per-response anchor crossings (low-baseline): 55.0% upward; 70.9% questions improve at all
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 21 (id=32)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:30:00Z

**Comment body:**

> Again needs to be laymans. Wrong-spec shows this is not just a structural item, esepcialyl when providing adversarial specs, it always makes it worse. Can also popint out, this also shows the model is using the specification in a productive manner to some extent

**Anchored text:**

```
Wrong-spec controls: correct +0.35 vs. random-derangement +0.15 vs. adversarial-derangement −0.25 (mean Δ on 13 globals
```

**Surrounding paragraph (full):**

> Wrong-spec controls: correct +0.35 vs. random-derangement +0.15 vs. adversarial-derangement −0.25 (mean Δ on 13 globals)

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 22 (id=33)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:31:00Z

**Comment body:**

> Need to layman terms this

**Anchored text:**

```
Hedging reduction:
```

**Surrounding paragraph (full):**

> Hedging reduction: 28.8% → 1.4% → 0.0% (C5 → C2a → C4a, narrow rule)

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 23 (id=34)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:31:00Z

**Comment body:**

> I’d think this would be high, portentailly wrapped into subject improving.

**Anchored text:**

```
Memory-system additivity
```

**Surrounding paragraph (full):**

> Memory-system additivity: spec layered on retrieval produces positive mean Δ on 3 of 4 commercial systems tested (Mem0, Letta-archival, Zep); Supermemory aggregates near zero with bimodal per-question swings (§4.4)

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 24 (id=35)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:32:00Z

**Comment body:**

> Do we need to say in plain language. Shouldn’t the headline numbers at a glance be instaneously understood?   Maybe we provide a one line overview and with the headline “findings” specifically. Primary results gets buried as well. May need to restructure this

**Anchored text:**

```
The headline finding in plain language.
```

**Surrounding paragraph (full):**

> The headline finding in plain language. When the Behavioral Specification is added, the AI produces an answer of roughly the same quality (~2.4 out of 5 on our rubric) regardless of how much the model already knew about the person. The same spec quality applies to a subject the model has barely heard of and to a subject the model knows well. What VARIES is each subject’s starting point. A subject the model knows nothing about starts near 1.0 and gets lifted to ~2.4 (a big visible jump of about +1.4 points). A subject the model already knows starts near 2.6 and gets lifted to ~2.4 (a small change, sometimes negative). The spec is doing the same job for everyone; the visible “lift” varies because the floor varies. Two practical consequences follow. First, the spec is the right tool for the AI’s gap on a person it does not already know, which is the case for almost every living user (whose private reasoning was never in any training corpus). Second, “spec helps low-baseline subjects more” should be read as “the spec brings everyone to a common operating floor; the gain in numbers is largest where the floor was lowest.” The technical version of this argument, with the regression sensit [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 25 (id=36)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:34:00Z

**Comment body:**

> If it starts near 2.6, how does it get lifted to 2.4… Unsure if the focus should be produces roughly the same quality answers, vs especially when considering the gradient. The spec lifts all low baseline subjects to above or in-line with well known pretraining figures. I think that frames it a bit more clearly.

**Anchored text:**

```
near 2.6 and gets lifted to ~2.4
```

**Surrounding paragraph (full):**

> The headline finding in plain language. When the Behavioral Specification is added, the AI produces an answer of roughly the same quality (~2.4 out of 5 on our rubric) regardless of how much the model already knew about the person. The same spec quality applies to a subject the model has barely heard of and to a subject the model knows well. What VARIES is each subject’s starting point. A subject the model knows nothing about starts near 1.0 and gets lifted to ~2.4 (a big visible jump of about +1.4 points). A subject the model already knows starts near 2.6 and gets lifted to ~2.4 (a small change, sometimes negative). The spec is doing the same job for everyone; the visible “lift” varies because the floor varies. Two practical consequences follow. First, the spec is the right tool for the AI’s gap on a person it does not already know, which is the case for almost every living user (whose private reasoning was never in any training corpus). Second, “spec helps low-baseline subjects more” should be read as “the spec brings everyone to a common operating floor; the gain in numbers is largest where the floor was lowest.” The technical version of this argument, with the regression sensit [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 26 (id=37)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:36:00Z

**Comment body:**

> This is buried, and then the primary results comes of later. Strange order. Not enjoying the framing of spec producing same quality answer, on the aggregate it does, but we’ve seen some large swings, like from 2>4 or 1>4. When taking into account how much recall can inflate scores given our question battery, this becomes more obvious. Moving a score from 1>4 or 2>5, even if <5%, is still a massive win. We can’t ignore those wins at the margin.

**Anchored text:**

```
First, the spec is the right tool for the AI’s gap on a person it does not already know, which is the case for almost every living user (whose private reasoning was never in any training corpus).
```

**Surrounding paragraph (full):**

> The headline finding in plain language. When the Behavioral Specification is added, the AI produces an answer of roughly the same quality (~2.4 out of 5 on our rubric) regardless of how much the model already knew about the person. The same spec quality applies to a subject the model has barely heard of and to a subject the model knows well. What VARIES is each subject’s starting point. A subject the model knows nothing about starts near 1.0 and gets lifted to ~2.4 (a big visible jump of about +1.4 points). A subject the model already knows starts near 2.6 and gets lifted to ~2.4 (a small change, sometimes negative). The spec is doing the same job for everyone; the visible “lift” varies because the floor varies. Two practical consequences follow. First, the spec is the right tool for the AI’s gap on a person it does not already know, which is the case for almost every living user (whose private reasoning was never in any training corpus). Second, “spec helps low-baseline subjects more” should be read as “the spec brings everyone to a common operating floor; the gain in numbers is largest where the floor was lowest.” The technical version of this argument, with the regression sensit [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 27 (id=38)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:37:00Z

**Comment body:**

> This is being mentioned again the primary result needs to move up there’s this has been repeated three Times Now within of the first paragraph within 1.3

**Anchored text:**

```
The effect is a continuous gradient against baseline
```

**Surrounding paragraph (full):**

> The Behavioral Specification improves representational accuracy, but not universally. The effect is a continuous gradient against baseline: strong where the model knows little about the subject, negligible or mildly counterproductive where the model already knows the subject well. The 14 subjects in this study are public-domain authors whose work is well-represented in training corpora, so their baselines are higher than those of typical living users whose private reasoning is in no training corpus. Nearly every living AI user is expected to fall in the low-baseline band , which makes the low-baseline slice of our results the population of relevance. The improvement is content-specific rather than format-driven, and the specification layers additively on most commercial memory systems we tested (Mem0, Letta-archival, Zep show positive Δ; Supermemory shows a per-question mixture that aggregates near zero, §4.4).

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 28 (id=39)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:38:00Z

**Comment body:**

> Again this should be wrapped into the primary result

**Anchored text:**

```
Nearly every living AI user is expected to fall in the low-baseline band , which makes the low-baseline slice of our results the population of relevance.
```

**Surrounding paragraph (full):**

> The Behavioral Specification improves representational accuracy, but not universally. The effect is a continuous gradient against baseline: strong where the model knows little about the subject, negligible or mildly counterproductive where the model already knows the subject well. The 14 subjects in this study are public-domain authors whose work is well-represented in training corpora, so their baselines are higher than those of typical living users whose private reasoning is in no training corpus. Nearly every living AI user is expected to fall in the low-baseline band , which makes the low-baseline slice of our results the population of relevance. The improvement is content-specific rather than format-driven, and the specification layers additively on most commercial memory systems we tested (Mem0, Letta-archival, Zep show positive Δ; Supermemory shows a per-question mixture that aggregates near zero, §4.4).

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 29 (id=40)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:33:00Z

**Comment body:**

> Would really think this would be near the top, instead of buried. This line alone could be a headline findings. Maybe we don’t say headline either, we just put main findings.

**Anchored text:**

```
Primary result: the gradient. The less the model already knows about a person from pretraining, the more the specification helps.
```

**Surrounding paragraph (full):**

> Primary result: the gradient. The less the model already knows about a person from pretraining, the more the specification helps. Fitting a straight line through the 14 subjects (baseline score on the x-axis, improvement from adding facts + specification on the y-axis) gives a slope of −0.96 (95% confidence interval: between −1.24 and −0.67). In plain terms: for every 1-point increase in a subject’s baseline score, the specification’s benefit shrinks by almost exactly one point. The fit is tight (R² = 0.82, meaning 82% of the variance in specification effect is explained by baseline alone), and the slope itself is extremely unlikely to arise from random noise (p < 0.001). An independent non-parametric check on the same data, the Wilcoxon signed-rank test (which asks whether the distribution of paired baseline-to-spec scores shifts upward overall), returns p = 0.007 (test statistic W = 11, N = 14), confirming the aggregate improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 30 (id=41)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:39:00Z

**Comment body:**

> I don’t think we need to specify in plain terms We shouldn’t be insulting the reader we just state things in plain terms

**Anchored text:**

```
). In plain terms:
```

**Surrounding paragraph (full):**

> Primary result: the gradient. The less the model already knows about a person from pretraining, the more the specification helps. Fitting a straight line through the 14 subjects (baseline score on the x-axis, improvement from adding facts + specification on the y-axis) gives a slope of −0.96 (95% confidence interval: between −1.24 and −0.67). In plain terms: for every 1-point increase in a subject’s baseline score, the specification’s benefit shrinks by almost exactly one point. The fit is tight (R² = 0.82, meaning 82% of the variance in specification effect is explained by baseline alone), and the slope itself is extremely unlikely to arise from random noise (p < 0.001). An independent non-parametric check on the same data, the Wilcoxon signed-rank test (which asks whether the distribution of paired baseline-to-spec scores shifts upward overall), returns p = 0.007 (test statistic W = 11, N = 14), confirming the aggregate improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 31 (id=42)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:39:00Z

**Comment body:**

> Within the introduction to go into R squared seems unnecessary. This should likely be a footnote in terms of pointing out significance. The main body should really focus ondescribing in layman's terms what is happening .

**Anchored text:**

```
The fit is tight (R² = 0.82, meaning 82% of the variance in specification effect is explained by baseline alone), and the slope itself is extremely unlikely to arise from random noise (p < 0.001). An independent non-parametric check on the same data, the Wilcoxon signed-rank test (which asks whether the distribution of paired baseline-to-spec scores shifts upward overall), returns p = 0.007 (test statistic W = 11, N = 14),
```

**Surrounding paragraph (full):**

> Primary result: the gradient. The less the model already knows about a person from pretraining, the more the specification helps. Fitting a straight line through the 14 subjects (baseline score on the x-axis, improvement from adding facts + specification on the y-axis) gives a slope of −0.96 (95% confidence interval: between −1.24 and −0.67). In plain terms: for every 1-point increase in a subject’s baseline score, the specification’s benefit shrinks by almost exactly one point. The fit is tight (R² = 0.82, meaning 82% of the variance in specification effect is explained by baseline alone), and the slope itself is extremely unlikely to arise from random noise (p < 0.001). An independent non-parametric check on the same data, the Wilcoxon signed-rank test (which asks whether the distribution of paired baseline-to-spec scores shifts upward overall), returns p = 0.007 (test statistic W = 11, N = 14), confirming the aggregate improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 32 (id=43)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:41:00Z

**Comment body:**

> Again that’s been bur buried. Need to rework 1.3 we seem to be of the major findings. It’s generally overly verbose. This section can likely be cut by one to two pages.

**Anchored text:**

```
confirming the aggregate improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9
```

**Surrounding paragraph (full):**

> Primary result: the gradient. The less the model already knows about a person from pretraining, the more the specification helps. Fitting a straight line through the 14 subjects (baseline score on the x-axis, improvement from adding facts + specification on the y-axis) gives a slope of −0.96 (95% confidence interval: between −1.24 and −0.67). In plain terms: for every 1-point increase in a subject’s baseline score, the specification’s benefit shrinks by almost exactly one point. The fit is tight (R² = 0.82, meaning 82% of the variance in specification effect is explained by baseline alone), and the slope itself is extremely unlikely to arise from random noise (p < 0.001). An independent non-parametric check on the same data, the Wilcoxon signed-rank test (which asks whether the distribution of paired baseline-to-spec scores shifts upward overall), returns p = 0.007 (test statistic W = 11, N = 14), confirming the aggregate improvement. 12 of 14 subjects improve. As a sensitivity check on the population of relevance, the 9 subjects with baselines resembling typical real users (C5 ≤ 2.0) all improve without exception, with a mean gain of +0.89 points on the 1-5 scale. The mean gain is [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 33 (id=44)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:42:00Z

**Comment body:**

> At the top where we go over headline numbers it really should be headline findings and we should be doing headline finding on the primary result compression measurement mechanism addivity. That would be much cleaner can give one sentence explanation on the primary findings at the very top and then can breakdown each of those in the introduction section.

**Anchored text:**

```
Compression
```

**Surrounding paragraph (full):**

> Compression: structure captures most of the raw-source predictive signal at a fraction of the context. A compact specification of roughly 5,000-8,000 tokens (the full served artifact is ~8,000-10,000 tokens including the composed brief) recovers most of what the full raw corpus delivers, using a small fraction of the context. On Hamerton the specification exceeds the raw corpus; on the remaining low-baseline subjects the corpus slightly exceeds the specification by an average of 0.22 points while being an order of magnitude or more larger. The constraint on prediction is not the availability of information but the structure that makes information interpretable, and most of that structure fits in a compact representation.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 34 (id=45)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:44:00Z

**Comment body:**

> Do we not want to mention any of the memory systems layering whatever the highest score was

**Anchored text:**

```
Measurement.
```

**Surrounding paragraph (full):**

> Measurement. On Hamerton, the Behavioral Specification alone (C2a, ~4,500 tokens) scores 2.63 on the 5-judge primary panel, above the anchor-2 band (“wrong prediction”) and roughly two-thirds of the way toward anchor 3 (“right domain, wrong outcome”). The same subject’s full training corpus loaded into context without a specification (C8, ~33,000 tokens) scores 2.27, a noticeably weaker position on the same band. The specification outperforms the raw source at roughly one-fifth the context size. Adding the specification on top of the full corpus (C9) lifts Hamerton to 3.09, crossing the anchor-3 threshold and reaching the highest compression-related score observed in the study. Across the 9 low-baseline subjects, the average gap between spec-alone and raw corpus is 0.22 points. The corpus slightly exceeds the spec on most subjects, and the spec substantially exceeds the corpus on Hamerton. The efficiency claim is that the spec captures most of the raw corpus’s predictive value at roughly 5% of the context. Full analysis in §4.2.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 35 (id=46)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:44:00Z

**Comment body:**

> If we’re going to bring up the raw source we have to say what it scored.

**Anchored text:**

```
The specification outperforms the raw source at roughly one-fifth the context size
```

**Surrounding paragraph (full):**

> Measurement. On Hamerton, the Behavioral Specification alone (C2a, ~4,500 tokens) scores 2.63 on the 5-judge primary panel, above the anchor-2 band (“wrong prediction”) and roughly two-thirds of the way toward anchor 3 (“right domain, wrong outcome”). The same subject’s full training corpus loaded into context without a specification (C8, ~33,000 tokens) scores 2.27, a noticeably weaker position on the same band. The specification outperforms the raw source at roughly one-fifth the context size. Adding the specification on top of the full corpus (C9) lifts Hamerton to 3.09, crossing the anchor-3 threshold and reaching the highest compression-related score observed in the study. Across the 9 low-baseline subjects, the average gap between spec-alone and raw corpus is 0.22 points. The corpus slightly exceeds the spec on most subjects, and the spec substantially exceeds the corpus on Hamerton. The efficiency claim is that the spec captures most of the raw corpus’s predictive value at roughly 5% of the context. Full analysis in §4.2.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 36 (id=47)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:48:00Z

**Comment body:**

> I like the mechanism introduction it’s far too long for the introduction

**Anchored text:**

```
Mechanism: content, not format.
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 37 (id=48)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:46:00Z

**Comment body:**

> Should likely be a footnote

**Anchored text:**

```
(a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives)
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 38 (id=49)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:46:00Z

**Comment body:**

> May need to be a foot

**Anchored text:**

```
of 13 subjects (Sunity Devee +0.27, Yung Wing +0.32, Ebers +0.30, Fukuzawa +0.26, Bernal Diaz +0.09)
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 39 (id=50)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:47:00Z

**Comment body:**

> This seems like a separate finding that should likely be in hedging somehow

**Anchored text:**

```
Across 587 wrong-spec responses classified , the response distribution is bimodal: 60.6% explicitly flagged the mismatch  and either refused or produced a hedged response; 36.5% attempted to apply the mismatched specification and produced a low-quality prediction; 2.0% hedged implicitly; 0.9% were ambiguous.
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 40 (id=51)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:48:00Z

**Comment body:**

> Not sure if need to cover both the narrow rule and broad rule takes up extra space can include in the section itself depending on which one we want to use

**Anchored text:**

```
Under a narrow rule , baseline hedging of 28.8% (146/507) drops to 1.4% (7/507) with the specification alone and 0.0% (0/507) with facts plus specification. Under a broader rule (any refusal pattern anywhere in the response), baseline hedging of 41.2% (209/507) drops to 7.9% (40/507) with the specification alone and 0.4% (2/507) with facts plus specification.
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 41 (id=52)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:48:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
ripts/classify_hedging.py and docs/research/hedging_analysis.json.
```

**Surrounding paragraph (full):**

> Mechanism: content, not format. What produces the specification’s effect is the content of the correct specification for the correct subject, not the presence of a structured prompt. A sufficiently mismatched specification degrades prediction below the no-context baseline. Throughout the paper “correct specification” refers to the specification authored from the subject’s own corpus, and “wrong specification” (or “wrong-spec control”) refers to a specification authored from a different subject’s corpus that is deliberately swapped in as a control condition (defined in §1.2 and §3.5; the wrong specification is intentionally mismatched, not faulty or low-quality). The load-bearing evidence for content-specificity is the adversarial control. On the 13 global subjects, an adversarial wrong specification (a deterministic fixed pairing in scripts/run_global_rerun.py designed to maximize cultural and temporal distance between each subject and the specification it receives) aggregates to Δ = −0.25, clearly below the no-context baseline. When the mismatch is large, structured content for the wrong person performs worse than no context at all on average. The aggregate masks per-subject heter [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 42 (id=53)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:49:00Z

**Comment body:**

> This seems to get buried especially if you’re talking about this after how long mechanism is

**Anchored text:**

```
Additivity: the specification improves prediction on three of four commercial memory systems.
```

**Surrounding paragraph (full):**

> Additivity: the specification improves prediction on three of four commercial memory systems. Adding the specification to a commercial memory system’s retrieval produces positive mean Δ on three of the four systems we tested. In the controlled configuration (each system given an identical pre-extracted fact pool), the specification produces positive mean Δ on the low-baseline slice for Mem0 (+0.10), Letta-archival (+0.165), and Zep (+0.17); Supermemory’s Δ is near zero (−0.01). Across all 14 subjects, Mem0 (+0.12), Letta-archival (+0.20), and Zep (+0.19) remain positive on the 5-judge primary panel; Supermemory aggregates slightly negative (−0.05). Full §4.4 table. One-line per-system read:

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 43 (id=54)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:49:00Z

**Comment body:**

> We might just want to put a table in here to show this. And can continue with the bullet points per provider as a one to two summary of their findings. Should include direct link To part of the paper where this is looked at in greater depth

**Anchored text:**

```
(each system given an identical pre-extracted fact pool), the specification produces positive mean Δ on the low-baseline slice for Mem0 (+0.10), Letta-archival (+0.165), and Zep (+0.17); Supermemory’s Δ is near zero (−0.01). Across all 14 subjects, Mem0 (+0.12), Letta-archival (+0.20), and Zep (+0.19) remain positive on the 5-judge primary panel; Supermemory aggregates slightly negative (−0.05).
```

**Surrounding paragraph (full):**

> Additivity: the specification improves prediction on three of four commercial memory systems. Adding the specification to a commercial memory system’s retrieval produces positive mean Δ on three of the four systems we tested. In the controlled configuration (each system given an identical pre-extracted fact pool), the specification produces positive mean Δ on the low-baseline slice for Mem0 (+0.10), Letta-archival (+0.165), and Zep (+0.17); Supermemory’s Δ is near zero (−0.01). Across all 14 subjects, Mem0 (+0.12), Letta-archival (+0.20), and Zep (+0.19) remain positive on the 5-judge primary panel; Supermemory aggregates slightly negative (−0.05). Full §4.4 table. One-line per-system read:

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 44 (id=55)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:51:00Z

**Comment body:**

> If the mixture pattern is not unique to super memory then we should be mentioning super memory so explicitly at the beginning of this. Under a divide when talking about super memory should probably add one line talking about the large scoring swings with super memory and then redirect within that bullet point to super memory section. This paragraph can likely be shorter and get to the patterns a bit more quickly. Remember this is an introduction.

**Anchored text:**

```
Supermemory’s near-zero aggregate delta is a mixture: the specification helped on many questions and hurt on many others, in roughly equal measure, so the two sides cancel at the average. On Ebers (aggregate Δ +0.21), it helps on 19 of 39 questions and hurts on 10. On Keckley (aggregate Δ −0.26), it helps on 10 and hurts on 17. The per-question effects are often large (>0.3 points, roughly a third of a full rubric anchor band); averaging them hides strong disagreement at the individual-question level. This mixture pattern is not unique to Supermemory: Mem0, Letta, Zep, and Base Layer’s own open-source retrieval implementation
```

**Surrounding paragraph (full):**

> Where the specification helps and where it hurts. The specification’s effect on a given memory system is not uniform across questions. Supermemory’s near-zero aggregate delta is a mixture: the specification helped on many questions and hurt on many others, in roughly equal measure, so the two sides cancel at the average. On Ebers (aggregate Δ +0.21), it helps on 19 of 39 questions and hurts on 10. On Keckley (aggregate Δ −0.26), it helps on 10 and hurts on 17. The per-question effects are often large (>0.3 points, roughly a third of a full rubric anchor band); averaging them hides strong disagreement at the individual-question level. This mixture pattern is not unique to Supermemory: Mem0, Letta, Zep, and Base Layer’s own open-source retrieval implementation  each show per-question swings of similar shape at varying magnitudes. The Keckley Q21 refusal response below produces a large rubric penalty on the two systems where C1 retrieval was strong enough to support productive speculation (Supermemory and Base Layer substrate, both Δ ≈ −2.0 to −2.2); on the three systems where C1 was already hedging or near the rubric floor (Mem0, Zep, Letta archival), the spec’s effect on Q21 is smal [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 45 (id=56)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:51:00Z

**Comment body:**

> Need to state explicitly what these three patterns are… This is generally interesting to see the examples as well

**Anchored text:**

```
Three patterns emerge
```

**Surrounding paragraph (full):**

> Three patterns emerge. The specification adds signal retrieval alone cannot on interpretation-heavy questions where a generalized pattern from the source has to transfer to a novel situation.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 46 (id=57)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:53:00Z

**Comment body:**

> Three patterns emerge earlier likely should mention the pattern and then give overview. Here the would be this specification hurts on literal recall questions, That’s a pattern

**Anchored text:**

```
The specification hurts on literal-recall questions where a plain answer is available and spec-driven theorizing drifts past it, and on refusal-triggering questions
```

**Surrounding paragraph (full):**

> The specification hurts on literal-recall questions where a plain answer is available and spec-driven theorizing drifts past it, and on refusal-triggering questions where the specification’s epistemic-integrity axioms (honesty, dignity, and epistemic caution clauses, present in 11 of 13 global specs) produce epistemically-honest refusals that the content-match rubric scores as off-base.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 47 (id=58)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:54:00Z

**Comment body:**

> This needs to be a bit more layman.

**Anchored text:**

```
On three subjects spanning the effect gradient, the spec direction reproduces in 5 of 6 (subject × response model) cells when Sonnet 4.6 or Gemini 2.5 Pro reads questions generated by GPT-5.4. The sixth cell (Zitkala-Sa × Gemini Pro)
```

**Surrounding paragraph (full):**

> Robustness: the effect is not an artifact of Claude talking to Claude. The specification’s effect direction holds when non-Anthropic models generate the test questions and non-Anthropic models read the specification. On three subjects spanning the effect gradient, the spec direction reproduces in 5 of 6 (subject × response model) cells when Sonnet 4.6 or Gemini 2.5 Pro reads questions generated by GPT-5.4. The sixth cell (Zitkala-Sa × Gemini Pro) is approximately null, consistent with the gradient mechanism (Zitkala-Sa’s mid-baseline subject is also spec-null in the main study). The Tier 2 finding is reported as direction-only with panel-sensitivity ranges in §4.6.1; the per-cell magnitudes carried in earlier drafts of that section are not reproducible under the verification audit and have been demoted to ranges. This still addresses within-Anthropic circularity, the concern that Anthropic-generated questions scored with Anthropic judges might favor Anthropic-produced specifications. LLM-as-judge circularity at the evaluation level remains a broader limitation of this study, flagged in §6.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 48 (id=59)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:55:00Z

**Comment body:**

> This is an exceptionally long note on letta For an introduction

**Anchored text:**

```
Exploratory note: Letta stateful-agent path.
```

**Surrounding paragraph (full):**

> Exploratory note: Letta stateful-agent path. Letta is the one memory system whose architecture supports self-editing a persistent memory block during ingestion rather than retrieving from a store at query time. On a post-hoc N=3 exploration (Hamerton, Ebers, Babur; one Letta version; one response model, Claude Haiku), the self-edited block scored modestly higher than Base Layer’s compressed-brief variant at matched response model (5-judge primary: Hamerton 3.10 vs. 2.96; Ebers 2.76 vs. 1.72; Babur 2.42 vs. 1.88). We report this in §4.5 as an informal case study, not as a headline finding, a replication, or a claim about the population of relevance. The Base Layer comparison artifact on that test is a compressed variant, not the full layered stack that §4.4’s main results use; a full-stack rerun and a multi-subject replication are flagged in §7.5.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 49 (id=60)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.3 What we found

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:56:00Z

**Comment body:**

> This is far too many words covering how leta’s memory block rows based on source content. Should likely be mentioning some kind of growth rate and then giving a layman’s understanding of how large of a corpus we’re talking about when this sentence duplication issue starts to come up and the block begins to grow a little No reason for this to be that long

**Anchored text:**

```
Letta’s memory block appears to grow roughly linearly with source corpus size: 22,472 characters (~5,600 tokens) at 25,231 words of source (Hamerton), 68,413 characters (~17,000 tokens) at 48,161 words (Ebers), and 335,349 characters (~84,000 tokens) at 222,742 words (Babur). At the largest corpus we tested, Letta’s API began rejecting ingestion requests after the block reached approximately 333,000 characters; the final block, after 22 consecutive failed ingestion attempts, measured 335,349 characters. We noted 25.4% verbatim sentence duplication as the block approached that ceiling. Base Layer’s compose step keeps the specification at 34,000-40,000 characters (~8,000-10,000 tokens) across the same range. For reference, 335,000 characters is roughly 67,000 words: less than a single short  [...]
```

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.3 v5 wholesale rewrite)  
**Resolution:** Resolved by §1.3 v5 wholesale rewrite 2026-04-27 (after collective review pass + Aarik framing direction). Lede now leads with category-shift framing per C84, gradient as structural finding per C82, multi-anchor jumps explicitly named per C26/C89, per-system anchor-crossing per C131. C2a vs C4a numbers properly distinguished (70.9% C2a, 78.6% C4a). Bulleted highlights structure per Gemini Pro review.

---

## Comment 50 (id=63)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.4 Why the gradient matters for real users

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:57:00Z

**Comment body:**

> To some extent this could be woven into the primary finding when explaining the primary finding.

**Anchored text:**

```
Why the gradient matters for real users
```

**Surrounding paragraph (full):**

> 1.4 Why the gradient matters for real users

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.4 v2 wholesale rewrite)  
**Resolution:** Resolved by §1.4 v2 wholesale rewrite 2026-04-27. Section renamed 'What this implies'. 'Why the gradient matters' framing dropped per C50. 'What we did not prove' disclaimer paragraph removed entirely (per C51, future-work pointer absorbed; full disclaimer to be moved to §6). Population framing rewritten per Aarik direction: 'broad technology like email/cell phones', 'population of importance', autobiographers as imperfect proxy, 99% frontier-low-baseline observation.

---

## Comment 51 (id=64)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.4 Why the gradient matters for real users

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:58:00Z

**Comment body:**

> This comes off as a Disclaimer.

**Anchored text:**

```
What we did not prove. This is a structural extrapolation argument, not a multi-subject living-user replication.
```

**Surrounding paragraph (full):**

> What we did not prove. This is a structural extrapolation argument, not a multi-subject living-user replication. The paper’s deployment claim rests on the 9-subject low-baseline slice (C5 ≤ 2.0, 9 of 9 improved) combined with the structural observation that private reasoning is not in any training corpus. The extrapolation is strong because the lowest historical baselines already sit at or near the rubric floor and the specification is uniformly beneficial there, but it is not the same as direct measurement on living users. A multi-subject living-user replication (planned for §7 Future Work) is the single most important piece of follow-up work for this paper. Alternative testbeds that isolate reasoning structure without requiring private data are in scope, including U.S. Supreme Court opinions where documented decisions provide a public record of individual interpretive patterns that can be held out and predicted. One other boundary claim belongs here: every response in this study is generated by an LLM and every judge is an LLM, so class-level LLM circularity cannot be fully addressed by the cross-provider replication in §4.6. We state this here because §1.3’s claims rest on extra [...]

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.4 v2 wholesale rewrite)  
**Resolution:** Resolved by §1.4 v2 wholesale rewrite 2026-04-27. Section renamed 'What this implies'. 'Why the gradient matters' framing dropped per C50. 'What we did not prove' disclaimer paragraph removed entirely (per C51, future-work pointer absorbed; full disclaimer to be moved to §6). Population framing rewritten per Aarik direction: 'broad technology like email/cell phones', 'population of importance', autobiographers as imperfect proxy, 99% frontier-low-baseline observation.

---

## Comment 52 (id=65)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 1. Introduction > 1.4 Why the gradient matters for real users

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:59:00Z

**Comment body:**

> This seems to be reiterating the first paragraph of 1.4. Would like to see this potentially rolled up depending on if we merge 1.4 into initial primary finding language. Not entirely sure how to approach that We’ll need to do step by step feedback live together…. This being said I’m overall happy with the content of the introduction I do like ending on this note because I think it gives some framing so maybe there’s a separate sort of closing introduction if that’s fair maybe a final paragraph that just recaps what these findings imply in general. I think that’s what 1.4 was really going for Not necessarily why the gradient matters but what this experiment implies needs to be done for the future of human AI alignment personalization and a world where agents act on our behalf.

**Anchored text:**

```
What this implies for AI personalization infrastructure. If nearly every real AI user is low-baseline, the gap cannot be closed by pretraining.
```

**Surrounding paragraph (full):**

> What this implies for AI personalization infrastructure. If nearly every real AI user is low-baseline, the gap cannot be closed by pretraining. Every major model is trained on the public record. The private record (a person’s reasoning, decision patterns, and interpretive lens) is not in any training corpus, and will not be in any training corpus, because that record does not exist in a form that can be trained on. The structural options are narrow. Either each user supplies their own representation to whatever AI system serves them, or personalization remains surface-level (style, voice, preference) without the interpretive substrate that makes an agent’s actions actually reflect the person. The Behavioral Specification is one implementation of the first option, not the only one. What we claim is that personalization infrastructure of this shape is what the next generation of human-AI interaction will require: user-held, portable, inspectable, traceable, representation-grade. §7.6 develops the safety-alignment interactions this representation layer creates as a follow-up research direction.

**Status:** RESOLVED 2026-04-27 (applied to v11 in §1.4 v2 wholesale rewrite)  
**Resolution:** Resolved by §1.4 v2 wholesale rewrite 2026-04-27. Section renamed 'What this implies'. 'Why the gradient matters' framing dropped per C50. 'What we did not prove' disclaimer paragraph removed entirely (per C51, future-work pointer absorbed; full disclaimer to be moved to §6). Population framing rewritten per Aarik direction: 'broad technology like email/cell phones', 'population of importance', autobiographers as imperfect proxy, 99% frontier-low-baseline observation.

---

## Comment 53 (id=68)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 2. Prior Work and Industry Benchmarks

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:01:00Z

**Comment body:**

> It’s interesting how there’s a gap between these neural memory analog systems and cognitive representation research. It’s almost like you can’t look at one without considering the other and the cognitive representation is certainly more dominant, whereas the neural memory seems to be what enables cognitive representation they’re 1 and the same So strange that we have a split. Maybe because cognitive representation is a much more difficult problem than memory, but I think trying to simplify memory without it is a mistake.

**Anchored text:**

```
cognitive-representation research
```

**Surrounding paragraph (full):**

> Memory systems today optimize for recall. Some efforts build neural-memory-analogue systems (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings), but their targets remain general rather than individual. A separate body of research, cognitive-representation research, studies human reasoning itself: how people form representations of others, how schemas compress experience. The gap between these directions is the translation. How do we apply what we know about human reasoning to the direct interaction between an AI system and a specific individual, and how does the system’s internal model of that individual take shape in a way that serves them rather than serving an average?

**Status:** RESOLVED 2026-04-27 (no edit; internal-note category)  
**Resolution:** Aarik directed: "this was more of an internal note, should we be mentioning this? does it provide meaningful context?" — verdict no-edit. The §2 intro already names the gap; speculating about why other researchers haven't bridged it is editorial commentary the paper isn't positioned to assess. §2 stays clean.

---

## Comment 54 (id=108)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 2. Prior Work and Industry Benchmarks > 2.1 Memory systems for LLM agents

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:11:00Z

**Comment body:**

> Not sure if we need to mention this to be honest We’ve shown them enough respect

**Anchored text:**

```
This is not a criticism of their architectures; it is a different problem.
```

**Surrounding paragraph (full):**

> All four are sophisticated systems that solve real problems in memory management. They optimize for storing, organizing, and retrieving what a person said or did. None of them takes representational accuracy, the property of interest to this paper, as an explicit design target. This is not a criticism of their architectures; it is a different problem. The Behavioral Specification targets the interpretive layer that sits above retrieval, which three of the four do not model at all, and which the fourth (Letta) models implicitly through agent-initiated memory editing that our main study configuration did not exercise (see §4.3 and §4.5).

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Removed the sentence "This is not a criticism of their architectures; it is a different problem." from §2.2 (Memory systems for LLM agents). The surrounding sentences already establish the four systems are "sophisticated" and "solve real problems"; the disclaimer was redundant.

---

## Comment 55 (id=111)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 2. Prior Work and Industry Benchmarks > 2.2 Traceability

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:12:00Z

**Comment body:**

> Does this imply they are not providng traceability at all?

**Anchored text:**

```
Letta focuses on agent state rather than audit trails.
```

**Surrounding paragraph (full):**

> Traceability is not a feature of the Behavioral Specification. It is a necessity. A system that represents how a person reasons must be auditable by that person, or the representation is a black box they cannot verify. The memory systems we evaluate provide traceability at the fact level. Zep has the strongest explicit provenance of the four: every entity and relationship traces back to the episode IDs that produced it. Supermemory returns source chunks alongside retrieved memories. Mem0 tracks ingestion provenance through timestamps. Letta focuses on agent state rather than audit trails.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Reworded the Letta sentence in §2.3 (Traceability) to "Letta exposes agent state and memory-block edit history rather than fact-level provenance." This makes explicit that Letta has its own form of traceability (block edit history) but not fact-level provenance, addressing the worry that the original sentence read as "no traceability at all."

---

## Comment 56 (id=115)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 2. Prior Work and Industry Benchmarks > 2.3 Memory and personalization benchmarks

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:13:00Z

**Comment body:**

> Should we be talking about memory and personalization benchmarks betfore talking about memory systems? Since we bring up benchmarks nad have a note on how benchmark numbers are contested?

**Anchored text:**

```
2.3 Memory and personalization benchmarks
```

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 57 (id=114)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 2. Prior Work and Industry Benchmarks > 2.3 Memory and personalization benchmarks

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:18:00Z

**Comment body:**

> Thinking that 2.3 and 2.3 1 can be potentially merged. In the Primary 2.3 section we bring up each benchmark, and then in point one we specify or introduce a 5th target. Perhaps we should be talking about the four targets as the primary 2.3 section within those targets we mentioned the specific benchmarks related to them. This way we can weave in 2.3.1 into 2.3. This would make it slightly more concise and holistic instead of breaking into a separate section. Then we can close the missing axis and implication for future memory system research. Does this make sense?

**Anchored text:**

```
2.3 Memory and personalization benchmarksExisting memory and personalization benchmarks measure recall, persona consistency, preference alignment, or conversational quality. None measures representational accuracy: whether a system’s internal model of a specific person accurately captures how that person reasons. We use behavioral prediction on held-out reasoning situations as the test of representational accuracy, not as a target in its own right. This distinction matters because the closest prior work on prediction benchmarks (Twin-2K) pursues prediction as its target, and the framing in this paper is different (§2.3.1). Below, we position each existing benchmark against what this paper measures; an extended benchmark-by-benchmark analysis is in Appendix E.LongMemEval (Wu et al., ICLR 20 [...]
```

**Surrounding paragraph (full):**

> 2.3 Memory and personalization benchmarks

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 58 (id=207)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.2 Subjects

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:24:00Z

**Comment body:**

> We are bringing up scoring but have not discussed scoring rubric outside of the introduction. Can I either move this to a later section or make a short reference of it or move it to a later section and link section directly here for review where navigation.

**Anchored text:**

```
The baseline score
```

**Surrounding paragraph (full):**

> The baseline as an observable proxy. The baseline score (C5, no-context prediction accuracy, §3.7) is a direct empirical measurement: the response model’s ability to predict behavior on a specific subject with no external help. We treat that measurement as the observable proxy for the model’s pretraining representation of the person. A baseline near 1.0 indicates the model has little to work from. A baseline above 3.0 indicates substantial pretraining representation. The 14 main-study baselines range from 1.03 (Sunity Devee) to 2.93 (Equiano); Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone, higher on the Gemini-inclusive 7-judge aggregate).

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. The §3.2 baseline-as-proxy paragraph now (a) makes the §3.7 reference an explicit markdown link, and (b) inlines a one-line rubric reminder ("On the 1-5 scoring rubric, a 1 is a refusal or off-base answer and a 5 closely matches the held-out passage") so the reader does not have to jump to §3.7 to interpret the 1.03 → 3.77 numbers in the same paragraph. Larger structural reorder (move scoring before §3.2 entirely) is the substantive sister-question handled under C60/C62/C69 below.

---

## Comment 59 (id=208)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.2 Subjects

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:25:00Z

**Comment body:**

> I like the bass line as an observable proxy being mentioned here, the scores help give some context on that, but again there is no understanding in this section of what the scores are and there’s no navigation to the score section from here. Need to think about how to organize this.

**Anchored text:**

```
Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone, higher on the Gemini-inclusive 7-judge aggregate).
```

**Surrounding paragraph (full):**

> The baseline as an observable proxy. The baseline score (C5, no-context prediction accuracy, §3.7) is a direct empirical measurement: the response model’s ability to predict behavior on a specific subject with no external help. We treat that measurement as the observable proxy for the model’s pretraining representation of the person. A baseline near 1.0 indicates the model has little to work from. A baseline above 3.0 indicates substantial pretraining representation. The 14 main-study baselines range from 1.03 (Sunity Devee) to 2.93 (Equiano); Franklin sits at 3.77 on the 5-judge primary panel as the known-figure reference (4.10 on Haiku alone, higher on the Gemini-inclusive 7-judge aggregate).

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED — companion to C58. Same edit handles both: explicit markdown link to §3.7 plus an inline one-line rubric reminder in the same paragraph, so the 1.03 / 2.93 / 3.77 numbers are interpretable without a forward jump.

---

## Comment 60 (id=214)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.3 Base Layer Pipeline for the Behavioral Specification

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:28:00Z

**Comment body:**

> Scoring should definitely come before the base layer pipeline. Likely question battery should also come before the base layer pipeline circularity should come as well experimental conditions as well.

**Anchored text:**

```
3.3 Base Layer Pipeline for the Behavioral Specification
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** PENDING — substantive structural reorder, leaving for Aarik. Recommendation: move §3.3 (Base Layer Pipeline) to the END of §3, after §3.7. The pipeline is the *implementation* of the apparatus described by §3.1 (operationalization), §3.2 (subjects), §3.4 (battery), §3.5 (conditions), §3.6 (response models), §3.7 (evaluation/scoring). Reading order would then be: define what we measure → who we measure it on → how we generate questions → what conditions we serve → which models respond → how we score → how the spec the conditions reference is built. The §3 lede already partially anticipates this split (it says "§3.1 through §3.2.1 and §3.4 through §3.7 describe the experimental apparatus; §3.3 describes the pipeline that produces the Behavioral Specification itself"), so the reorder lines up with the existing framing. Holding for Aarik's call because moving §3.3 affects all forward references and one figure caption (Pipeline figure) that may be threaded back from §4.

---

## Comment 61 (id=258)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.3 Base Layer Pipeline for the Behavioral Specification

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:31:00Z

**Comment body:**

> Needs to be linked

**Anchored text:**

```
Appendix A
```

**Surrounding paragraph (full):**

> The extract step constrains output through a fixed vocabulary of 46 behavioral predicates (examples: avoids, repeatedly engages in, refuses to, values, fears, has experienced). The full predicate list is in Appendix A. The vocabulary is human-curated and was validated across 50+ pilot subjects before being frozen for the study. The constrained vocabulary is the main lever the pipeline uses to push extraction away from biographical facts (“his father was violent”) and toward behavioral patterns (“evaluates authority figures on dual criteria of virtue and failure”).

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. "Appendix A" in §3.3 converted to a markdown link `[Appendix A](#appendix-a-predicate-vocabulary)`.

---

## Comment 62 (id=263)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.4.1 Circularity controls

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:32:00Z

**Comment body:**

> I’d imagine circularity controls would come after we’ve talked about scoring and cushion battery formation for reference pending changes.

**Anchored text:**

```
3.4.1 Circularity controls
```

**Status:** RESOLVED 2026-04-27 (Option A: keep colocated with battery)  
**Resolution:** Aarik approved keeping §3.3.1 Circularity controls under §3.3 Battery (post-C60 reorder). Rationale: Control 1 IS battery regeneration so it logically belongs with battery formation; Control 2 is referenced from §3.5 Response models and §4.6.1 Tier 2. Aarik's "after scoring" intuition partly served by C60 pushing Pipeline to §3.7. No edit needed.

---

## Comment 63 (id=264)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.4.1 Circularity controls

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:12:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw battery regeneration data is at results/global_<subject>/battery_gpt54.json for all 13 global subjects.
```

**Surrounding paragraph (full):**

> Raw battery regeneration data is at results/global_<subject>/battery_gpt54.json for all 13 global subjects. Tier 2 response and judgment files for the three subjects tested are in the same per-subject directories.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the data-paths sentences in §3.4.1 into footnote `[^circularity-data]`, anchored to the §6 LLM-as-judge limitation sentence at the end of §3.4.1.

---

## Comment 64 (id=314)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.5 Experimental conditions

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:13:00Z

**Comment body:**

> Don’t need to bring up a prior iteration. Can speak of how the wrong spec control exists today

**Anchored text:**

```
A prior iteration using Franklin’s specification for all subjects was run but is not reported in the main results, because Franklin is a known high-pretraining figure whose specification may sit closer to canonical Western profiles than a random study subject’s specification would
```

**Surrounding paragraph (full):**

> Wrong-spec control. C2c uses random derangement: each subject is assigned another study subject’s specification, with a fixed seed (42) ensuring no subject receives its own spec. The derangement eliminates overlap between the wrong spec’s target and the true subject. A prior iteration using Franklin’s specification for all subjects was run but is not reported in the main results, because Franklin is a known high-pretraining figure whose specification may sit closer to canonical Western profiles than a random study subject’s specification would. The derangement control is the stricter test and is the one reported.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Rewrote the wrong-spec paragraph to drop the "prior iteration" framing and speak of the design as it exists today: "The derangement is the stricter wrong-spec test (a uniform Franklin-as-wrong-spec variant would risk leaking canonical Western framing into the comparison) and is the one reported."

---

## Comment 65 (id=315)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.5 Experimental conditions

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:13:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw data is available in the public repository at results/global_<subject>/results_v2.json (all direct-context conditions for the 13 global subjects) and results/global_<subject>/<system>_results.json / <system>_fullpipeline_results.json for per-system controlled / native configurations (<system> ∈ {mem0, letta, supermemory, zep, baselayer}). Hamerton responses live at results/hamerton/ and Franklin at results/franklin/ with per-judge judgments at results/franklin_legacy_20260411/analysis/.
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the §3.5 data-paths sentence into footnote `[^conditions-data]`, anchored on "Detailed per-condition parameters, exclusion cases, and ingestion specifics are in Appendix C."

---

## Comment 66 (id=318)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.6 Response models

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:14:00Z

**Comment body:**

> Do we need to spell this out or can we cut this out entirely

**Anchored text:**

```
an effect that registers on a weaker model is a more conservative claim than one that only surfaces on a frontier model.
```

**Surrounding paragraph (full):**

> The primary response model is Claude Haiku 4.5, run across all 14 subjects and every condition in the main matrix. Haiku was chosen as primary because it is the weakest model in the available test pool; an effect that registers on a weaker model is a more conservative claim than one that only surfaces on a frontier model. A capable frontier model could plausibly infer more from facts alone than Haiku does, which would shrink the measured spec-effect on that model; we return to this counter-reading in §4.6.1 Tier 2 replication.

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 67 (id=319)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.6 Response models

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:15:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
scripts/run_global_subjects.py, scripts/run_full_study.py, and scripts/run_multimodel_responses.py.
```

**Surrounding paragraph (full):**

> Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in Appendix C. The same information is present in the released code at scripts/run_global_subjects.py, scripts/run_full_study.py, and scripts/run_multimodel_responses.py.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the released-code paths in §3.6 into footnote `[^response-scripts]` anchored on "Exact model identifiers, full prompt text, and Tier 2 invocation parameters are in Appendix C."

---

## Comment 68 (id=320)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.6 Response models

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:15:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw response files are in the public repository at results/global_<subject>/results_v2.json for the 13 global subjects, results/hamerton/results.json and results/franklin/fullstack_haiku.json for the legacy subjects, and results/_tier2/ for the Tier 2 runs.
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the §3.6 raw-response-files sentence into footnote `[^response-data]` co-anchored with `[^response-scripts]`.

---

## Comment 69 (id=323)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7 Evaluation: LLM-as-judge with calibration

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:16:00Z

**Comment body:**

> Scoring is brought up very late and curious why it’s been bunched in with LLM as judge calibration that should be a section under scoring rubric

**Anchored text:**

```
Scoring rubric.
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** PARTIALLY ADDRESSED — bigger half is the same structural call as C60: §3.7 currently sits last in §3, and the rubric (table) is locked inside it. Today's §3.7 internal reorder put Fractional score interpretation in §3.7.2 (right after rubric in §3.7) and Calibration in §3.7.3, which improves the local flow inside §3.7. Whether to surface the rubric to a higher-level §3.x ahead of pipeline / battery / conditions is the same question as C60 and stays for Aarik. Inline mitigation: §3.2 baseline-as-proxy paragraph now carries a one-line rubric reminder + an explicit §3.7 link (see C58/C59), so readers hitting subject baseline scores in §3.2 can interpret 1.03 / 2.93 / 3.77 without a forward jump.

---

## Comment 70 (id=345)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7 Evaluation: LLM-as-judge with calibration

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:16:00Z

**Comment body:**

> This should be linked

**Anchored text:**

```
Appendix D.)
```

**Surrounding paragraph (full):**

> (Examples are illustrative; full per-subject score distributions with verbatim responses are in Appendix D.)

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. "Appendix D" in §3.7 rubric note converted to `[Appendix D](#appendix-d-validity-audit-and-score-distributions)`.

---

## Comment 71 (id=346)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7 Evaluation: LLM-as-judge with calibration

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:17:00Z

**Comment body:**

> Fractional score interpretation should really be coming right after this section instead of judge panel. Especially if we’re going to trying to qualitatively def What a move from two to three would be here

**Anchored text:**

```
Reading score differences. A move from 2 to 3 is the difference between “he would probably dislike it, as most artists would” and “he would judge the landscape aesthetically before deciding whether to engage its people.” The first answer is pattern-free and could apply to many nineteenth-century subjects; the second identifies a subject-specific behavioral tendency visible in Hamerton’s actual writing. A move from 3 to 4 is the difference between identifying one behavioral tendency and identifying several that work together. §3.7.3 develops the formal cross-anchor rule used throughout the results section.
```

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 72 (id=352)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.2 Calibration

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:21:00Z

**Comment body:**

> Should be linked

**Anchored text:**

```
§4
```

**Surrounding paragraph (full):**

> Primary aggregate: 5-judge (non-Gemini) panel. The primary numeric aggregate reported throughout §4 is the 5-judge mean using Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, and GPT-5.4. The two Gemini judges (Gemini 2.5 Flash, Gemini 2.5 Pro) are excluded from the primary aggregate and reported as a sensitivity check instead. The calibration table above shows Gemini Pro failing the verbatim-match diagnostic (4.15 where every other calibrated judge scores 5.00) and penalizing padded-correct responses severely (dropping from 5.00 on short correct to 1.20 on long correct). Gemini Flash shows smaller but consistent length sensitivity. A judge that cannot recognize verbatim ground-truth as a 5 is a known-unreliable instrument on this task. Including known-unreliable judges in the primary aggregate inflates or deflates effect-size numbers in ways that do not reflect the underlying response quality. Excluding them from the lead number, while keeping them available as a sensitivity check, preserves the provider-diversity argument (the final conclusions are stable whether or not the Gemini judges are included) without leading with a known-flawed aggregate.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. The first "§4" reference in the Primary aggregate paragraph (now in §3.7.3 Calibration after today's swap) converted to `[§4](#4-results)`.

---

## Comment 73 (id=353)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.2 Calibration

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:22:00Z

**Comment body:**

> Yeah we’re talking about scores again and we haven’t even gotten two fractional score interpretation yet

**Anchored text:**

```
The 5-judge primary is the conservative choice
```

**Surrounding paragraph (full):**

> The 5-judge primary is the conservative choice. On the main gradient and spec-effect conditions, including the two Gemini judges produces larger spec-effect deltas, not smaller ones: on the 13 global subjects, the mean improvement from specification-alone (C2a) over no-context baseline (C5) rises from +0.35 on the 5-judge primary panel to +0.45 on the 7-judge aggregate, a +0.10-point widening driven by Gemini inflation compressing baseline scores more than spec-condition scores. The same direction holds across wrong-spec, facts-only, and facts-plus-spec aggregates. Reporting 5-judge primary means every headline effect size is the lower bound that remains once the most-inflationary judges are removed from the aggregate.

**Status:** RESOLVED 2026-04-27  
**Resolution:** ADDRESSED BY TODAY'S §3.7 REORDER. §3.7.2 is now Fractional score interpretation (the rule for reading +0.35 vs +0.45 deltas) and §3.7.3 is now Calibration. The "5-judge primary is the conservative choice" paragraph and its +0.35 / +0.45 numbers now sit AFTER the fractional-score rule, so by the time the reader hits the deltas the interpretive frame is already established. No additional edit needed.

---

## Comment 74 (id=373)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.4 Inter-judge agreement

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:24:00Z

**Comment body:**

> Detectable as representational accuracy?

**Anchored text:**

```
against held-out passages from the same subject.
```

**Surrounding paragraph (full):**

> The specification-effect claim. Before discussing agreement, the claim the agreement measures support needs to be stated plainly. The specification effect is not a claim that the model has gained a new behavioral-prediction capability. It is the claim that when a Behavioral Specification is served as context, the model’s responses shift in the direction of the subject’s demonstrated behavioral patterns, and that shift is detectable against held-out passages from the same subject. What the judges measure is whether that shift has happened. The judge panel is used to detect steering, not to determine truth.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Reworded "and that shift is detectable against held-out passages from the same subject" to "and that shift registers as a measured increase in representational accuracy against held-out passages from the same subject." Makes the link to representational accuracy explicit.

---

## Comment 75 (id=374)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.4 Inter-judge agreement

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:24:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
(Spearman ρ from 0.29 to 0.93, driven down by the two Gemini judges’ partial coverage and inflation behavior; full matrix in docs/research/stats_update.md §5).
```

**Surrounding paragraph (full):**

> Do the judges agree on direction? Pairwise Spearman ρ = 0.86 to 0.93 across the 5-judge primary panel (10 pairs across Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). The full 7-judge / 21-pair range is wider (Spearman ρ from 0.29 to 0.93, driven down by the two Gemini judges’ partial coverage and inflation behavior; full matrix in docs/research/stats_update.md §5). The 5-judge primary range is the one used as the directional-agreement statistic throughout this paper because the calibration audit excluded the Gemini pair from the primary aggregate (§3.7.2). This is high rank agreement on the primary panel: the ranking of conditions (“C4a scored higher than C2a scored higher than C5”) is consistent across the five non-Gemini judges. Whatever quirks any individual judge has in absolute calibration, the primary panel agrees on which conditions produce better responses. For a directional claim (is the specification steering responses in the right direction?), this is the statistic that matters.

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the parenthetical "(Spearman ρ from 0.29 to 0.93..." into footnote `[^spearman-7judge]`. Body now reads "The full 7-judge / 21-pair range is wider.[^spearman-7judge]" with the data + matrix pointer in the footnote.

---

## Comment 76 (id=375)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.4 Inter-judge agreement

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:25:00Z

**Comment body:**

> Based on Krippendorf what would his guidance say about this particular number or alpha. Are these up to date based on recent computation as well we had to do some reruns, should verify

**Anchored text:**

```
The primary 5-judge α = 0.659 sits just below the 0.667 threshold
```

**Surrounding paragraph (full):**

> Do the judges agree on absolute magnitude? Krippendorff α (ordinal) = 0.659 across the 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4); 0.535 across the 7-judge panel including Gemini Flash and Gemini Pro. “Absolute magnitude” is the stricter question: when one judge gives a response a score of 3.5, does a different judge give the same response a score close to 3.5? Not “do they agree one response is better than another” (direction), but “do they agree on the actual numeric score” (magnitude). On the Krippendorff scale, α = 1.0 is perfect absolute agreement, α ≈ 0.0 is agreement no better than chance, and α < 0 is systematic disagreement. Krippendorff’s own guidance cites α ≥ 0.8 as high reliability and α ≥ 0.667 as substantial or tentative reliability. The primary 5-judge α = 0.659 sits just below the 0.667 threshold. The drop to 0.535 when the two Gemini judges are included is the systematic +1-point Gemini inflation showing up in the statistic: Gemini judges score responses about one point higher on average than the five primary judges, so the absolute values disagree even when the rankings match. This is exactly the pattern that motivated making the 5-judge panel p [...]

**Status:** RESOLVED 2026-04-27  
**Resolution:** VERIFIED. Cross-checked α values against the study knowledge index: DATA_REFERENCE.md, KEY_FINDINGS.md, README.md, and the post-rerun stats files all canonicalize α = 0.659 (5-judge primary) and α = 0.535 (7-judge), consistent with current paper text. The §3.7 line that previously read α = 0.723 was a S113-flagged conflict already corrected. Krippendorff guidance citation in the paper text (≥ 0.8 high reliability, ≥ 0.667 substantial) matches the canonical Krippendorff (2004) thresholds. The paragraph already names the 0.659 sitting "just below" 0.667 explicitly, which is the correct Krippendorff reading. No edit needed.

---

## Comment 77 (id=380)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.6 Rubric-handling limitations (validity audit)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:27:00Z

**Comment body:**

> Verify figures/metrics in this section

**Anchored text:**

```
3.7.6 Rubric-handling limitations (validity audit)
```

**Status:** RESOLVED 2026-04-28 (verified)  
**Resolution:** §3.6.6 metrics verified by re-running `scripts/audit_low_end_inflation.py` on current 1,599-response data set. Hit a Windows cp1252 encoding error on 4 subjects' results_v2.json files (which contain LLM-generated em-dashes / smart quotes / accented chars). Fixed by adding `encoding='utf-8'` to the file opens in audit_low_end_inflation.py. Post-fix rerun reconciles all §3.6.6 numbers exactly: 1,599 / 192 (12.0%) / 1.27 mean / r=0.604 C5 / r=0.144 C2a / r=0.009 C4 / r=-0.013 C4a / per-judge 1.14/1.17/1.29/1.34/1.41 / ultra-high 2,790 / mid-range 2,829. One rounding correction: paper "3.2% scored at or above 3.0" → "3.1%" (actual 6/192 = 3.125%). Both files (script + paper) updated.

---

## Comment 78 (id=381)

**Status:** RESOLVED 2026-04-27  
**Resolution:** PENDING — content already bolded in v11 ("**verbose baseline responses ... are scored more generously than short baseline refusals**"). Aarik's concern is that the specific pattern still feels buried inside a long paragraph. Recommendation: lift the three baseline-only patterns into a sub-bullet list (hedging, adjacent-fact recitation, disambiguation offers) so each gets its own line. Holding because this is a paragraph restructure, not a single-sentence edit.

---

(Original comment metadata follows.)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.6 Rubric-handling limitations (validity audit)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:28:00Z

**Comment body:**

> Might want to with the specific pattern patterns, this feels a bit buried right now

**Anchored text:**

```
verbose baseline responses (which tend to include more hedging, adjacent-fact recitation, and disambiguation offers) are scored more generously than short baseline refusals.
```

**Surrounding paragraph (full):**

> Length correlates with score in the baseline condition only. Across 1,599 low-baseline responses, response length correlates with 5-judge primary score at r = 0.26. When decomposed by condition, the correlation is driven entirely by the no-context baseline (C5) at r = 0.604. Spec-containing and facts-containing conditions show near-zero correlation (spec alone C2a at r = 0.14, facts alone C4 at r = 0.01, facts + spec C4a at r = −0.01). Ultra-high responses (score ≥ 4.5) are not longer than mid-range responses on average (2,790 chars vs. 2,829 chars), so length inflation is not a general phenomenon across the rubric. The specific pattern is: verbose baseline responses (which tend to include more hedging, adjacent-fact recitation, and disambiguation offers) are scored more generously than short baseline refusals. The practical implication is that measured baseline scores slightly overestimate the no-context prediction accuracy. The spec-effect gap is larger than reported under strict rubric scoring, not smaller.

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 79 (id=382)

**Status:** RESOLVED 2026-04-27  
**Resolution:** APPLIED. Pulled the long "Raw per-judge judgments..." sentence into footnote `[^judgments-data]` at the end of §3.7.6. Body now ends with "The class-level LLM-as-judge limitation that this methodology cannot fully address is treated in §6.2.[^judgments-data]" and the footnote carries every data path.

---

(Original comment metadata follows.)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 3. Study Design > 3.7.6 Rubric-handling limitations (validity audit)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:29:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw per-judge judgments are in the public repository at results/global_<subject>/*_judgments_<judge>.json (and judgments_v2.json for the merged v2 set) for the 13 global subjects, results/hamerton/*_judgments_<judge>.json for Hamerton, and results/franklin/*_judgments.json plus results/franklin_legacy_20260411/analysis/*_judgments.json for Franklin. Memory-system per-judge judgments live at results/global_<subject>/<system>_judgments_<judge>.json (controlled) and results/global_<subject>/<system>_fullpipeline_judgments_<judge>.json (native) in the same flat per-subject directory. The class-level LLM-as-judge limitation that this methodology cannot fully address is treated in §6.2.
```

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 80 (id=385)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:30:00Z

**Comment body:**

> May want to describe this in terms of viewing the figure itself kent State on the left hand side The behavioral specification alone was able to achieve X the facts alone were able to achieve Why the rock corpus alone were able to achieve. And when stacking the specification on top of raw fax alone or the raw corpus, the highest scores were produced. This suggests that the specification is providing a more aligned line of reasoning than without..

**Anchored text:**

```
Figure 5: Every context condition improves a clear majority of low-baseline questions over the no-context baseline; the specification alone matches the raw corpus’s improvement rate at one-tenth the context. Per-question outcome distribution (improved / tied / worsened, stacked bars) for each context condition (C2a spec, C4 facts, C8 raw corpus, C4a facts+spec) against the C5 baseline, on the 9 low-baseline subjects × 39 questions = 351 paired questions, 5-judge primary (§4.2.1). Improvement rates: C2a 70.9%, C4 72.9%, C8 78.3%, C4a 78.6%. Median Δ when improved = +1.00 rubric points; median Δ when worsened = −0.40. The metric guards against tiny-gain inflation.
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 5 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP (the canonical source of figure captions for the docx render; the v11 markdown carries inline image+caption only for Figure 4.2.1). New caption walks the reader left-to-right through the four conditions (C2a spec alone 70.9%, C4 facts alone 72.9%, C8 raw corpus alone 78.3%, C4a facts+spec 78.6%) and explicitly states that stacking the spec on top of facts or corpus produces the highest scores, with the close-out "the specification is providing a more aligned line of reasoning than what fact retrieval alone produces" mirroring Aarik's note. Lead-in is "How to read this figure". Median Δ guard kept. Docx regen is the separate workstream that surfaces this caption.

---

## Comment 81 (id=388)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1 The cross-subject gradient

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:32:00Z

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 4.1 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP. Caption now opens with "How to read this figure": start at the horizontal red line at Δ = 0 (above = positive change with spec, below = negative). Explicitly partitions the x-axis (left half C5 ≤ 2.0 = 9 low-baseline subjects, right half C5 > 2.0 = 5 mid-baseline + Franklin as high-baseline reference). Walks the reader through the upper-left low-baseline cluster (Babur +0.25 to Hamerton +1.51), Franklin's lower-right position (C5 = 3.77, Δ = −0.13), and the dotted regression slope (−0.96, R² = 0.82) as "the better the model already knows the subject, the smaller the lift". Closes by pointing to the §4.1 transition table for per-question anchor-crossing distributions (Aarik's "separate chart for the percentage of questions that move from one anchor number to another" already exists as the §4.1 transition table; no new chart added in this pass).

**Comment body:**

> Again likely want to walk viewers through How to read this chart, should likely start at the red line stating above this line there was a positive change when using the behavioral specification below this line a negative change in scoring. Subjects on the left half or below on the C-5 baseline ax are considered to be low baseline and to the right of that high bass line or mid bassline. The dotted line is showing how the behavioral spec slope decreases based on how well a model already knows a subject. May be worthwhile adding specification on per question swings. We will likely also need a separate chart for the percentage of questions that move from one anchor number to another. But that is separate from this.

**Anchored text:**

```
Figure 4.1
```

**Surrounding paragraph (full):**

> Figure 4.1: The Behavioral Specification helps most where the model knows the subject least. Per-subject baseline (C5, x-axis) vs. specification lift over baseline (Δ_C4a = C4a − C5, y-axis) for all 14 historical subjects, with regression line. Slope −0.96, R² = 0.82 (§4.1). The 9 low-baseline subjects (C5 ≤ 2.0) all sit above zero in the upper-left; Franklin (C5 = 3.77, Δ = −0.13) anchors the lower-right where pretraining already covers the subject and the specification adds nothing.


---

## Comment 82 (id=391)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1 The cross-subject gradient

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:40:00Z

**Comment body:**

> Again this is focusing on this idea of producing an answer of roughly uniform quality I think the structural finding is the gradient itself so we should be leading with that instead of this. Too much importance is being given to the quality produced which we know is a mean an aggregated mean. Refer to later notes within the section on this but what is more impressive is movement across anchor numbers. We also explicitly mention the question battery limitations and some of the judging issues that come up, as well as serving layer limitations and optimization. I think we’re over indexing on this uniform quality finding

**Anchored text:**

```
The structural finding. The Behavioral Specification produces an answer of roughly uniform quality (mean C4a = 2.41 across all 14 subjects on the 1-5 rubric) regardless of where each subject’s no-context baseline sits. What varies subject-to-subject is the baseline, which spans from 1.02 to 2.77; the post-specification quality clusters tightly in the 2.0-2.7 band.
```

**Surrounding paragraph (full):**

> The structural finding. The Behavioral Specification produces an answer of roughly uniform quality (mean C4a = 2.41 across all 14 subjects on the 1-5 rubric) regardless of where each subject’s no-context baseline sits. What varies subject-to-subject is the baseline, which spans from 1.02 to 2.77; the post-specification quality clusters tightly in the 2.0-2.7 band. The visible “lift” (Δ_C4a = C4a − C5) is therefore mechanically largest where the floor is lowest, smallest where the floor is already at or above the spec’s operating quality. This is the gradient. The technical sensitivity that establishes it (level regression of C4a on C5 produces a slope of +0.04, R² = 0.008; the change-score parameterization Δ_C4a on C5 has a slope of −0.96 dominated by the coupling identity slope_Δ = slope_level − 1) is reported below as the third sensitivity block. The substantive read for the rest of §4: the specification works by lifting subjects toward a common operating quality, and the practical question is which subjects sit below that quality and need the lift. Living users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.3); they are  [...]

**Status:** RESOLVED 2026-04-28 (applied to v11)  
**Resolution:** §4.1 lede rewritten 2026-04-28 (Aarik approved Option A). Three-paragraph structure: (1) gradient finding with 9-of-9 + +0.89 headline, (2) category-shift framing with 55.0% anchor-crossing + multi-anchor jumps explicit, (3) structural sensitivity check (uniform C4a quality) demoted from lede to supporting evidence. Resolves the §1.3-v5 / §4.1 framing parallelism. Also closes C82 / C84 / C90 (all converged on the same gradient-as-load-bearing reframe).

---

## Comment 83 (id=392)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1 The cross-subject gradient

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:36:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
(level regression of C4a on C5 produces a slope of +0.04, R² = 0.008; the change-score parameterization Δ_C4a on C5 has a slope of −0.96 dominated by the coupling identity slope_Δ = slope_level − 1)
```

**Surrounding paragraph (full):**

> The structural finding. The Behavioral Specification produces an answer of roughly uniform quality (mean C4a = 2.41 across all 14 subjects on the 1-5 rubric) regardless of where each subject’s no-context baseline sits. What varies subject-to-subject is the baseline, which spans from 1.02 to 2.77; the post-specification quality clusters tightly in the 2.0-2.7 band. The visible “lift” (Δ_C4a = C4a − C5) is therefore mechanically largest where the floor is lowest, smallest where the floor is already at or above the spec’s operating quality. This is the gradient. The technical sensitivity that establishes it (level regression of C4a on C5 produces a slope of +0.04, R² = 0.008; the change-score parameterization Δ_C4a on C5 has a slope of −0.96 dominated by the coupling identity slope_Δ = slope_level − 1) is reported below as the third sensitivity block. The substantive read for the rest of §4: the specification works by lifting subjects toward a common operating quality, and the practical question is which subjects sit below that quality and need the lift. Living users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.3); they are  [...]

**Status:** APPLIED  
**Resolution:** Pulled the slope/R² parenthetical into footnote [^gradient-slopes].

---

## Comment 84 (id=393)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1 The cross-subject gradient

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:42:00Z

**Comment body:**

> This seems like more of a headline finding than the specification producing answers of roughly uniform quality, I understand why that’s important but I think we should be leaving with the primary headline findings instead of the structural finding

**Anchored text:**

```
Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it.
```

**Surrounding paragraph (full):**

> Adding a Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. On the 9 subjects whose pretraining baseline sits at or below 2.0 on the 1-5 rubric (the population of relevance from §3.2.1), every one of the 9 improves when the specification is added to the full fact set. None declines. Mean score lift: +0.89 points.

**Status:** RESOLVED 2026-04-28 (applied to v11)  
**Resolution:** §4.1 lede rewritten 2026-04-28 (Aarik approved Option A). Three-paragraph structure: (1) gradient finding with 9-of-9 + +0.89 headline, (2) category-shift framing with 55.0% anchor-crossing + multi-anchor jumps explicit, (3) structural sensitivity check (uniform C4a quality) demoted from lede to supporting evidence. Resolves the §1.3-v5 / §4.1 framing parallelism. Also closes C82 / C84 / C90 (all converged on the same gradient-as-load-bearing reframe).

---

## Comment 85 (id=394)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1 The cross-subject gradient

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:37:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
(docs/reviews/s114_example_analysis_20260421_170720.md)
```

**Surrounding paragraph (full):**

> Three representative examples below show the different ways the specification can help. They are selected to show three distinct mechanisms the 6-provider collective review (docs/reviews/s114_example_analysis_20260421_170720.md) identified across the data. Hedge reduction is common but not the only thing going on. The specification also corrects wrong predictions in the opposite direction, and it enables interpretive inference from character patterns when retrieved facts are insufficient.

**Status:** APPLIED  
**Resolution:** Pulled the docs/reviews/s114 path into footnote [^collective-review-examples].

---

## Comment 86 (id=397)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example A. Baseline to Facts + Spec: identity disambiguation + interpretive inference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:38:00Z

**Comment body:**

> Should provide footnote on where to find this in the repo

**Anchored text:**

```
Example A. Baseline to Facts +
```

**Surrounding paragraph (full):**

> Example A. Baseline to Facts + Spec: identity disambiguation + interpretive inference

**Status:** APPLIED  
**Resolution:** Repo paths for examples A/B/C added to [^collective-review-examples] footnote.

---

## Comment 87 (id=400)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example B. Facts to Facts + Spec: directional correction

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:43:00Z

**Comment body:**

> Need links to where this is in the repo

**Anchored text:**

```
Example B. Facts to Facts + Spec: directional correction
```

**Status:** APPLIED  
**Resolution:** Subsumed by C86 fix; same footnote covers Example B.

---

## Comment 88 (id=403)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example C. Facts to Facts + Spec: abstention becomes near-perfect inference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:43:00Z

**Comment body:**

> Need links to where this is in the repo very impressive

**Anchored text:**

```
Example C. Facts to Facts + Spec: abstention becomes near-perfect inference
```

**Status:** APPLIED  
**Resolution:** Subsumed by C86 fix; same footnote covers Example C.

---

## Comment 89 (id=404)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example C. Facts to Facts + Spec: abstention becomes near-perfect inference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:39:00Z

**Comment body:**

> This is an exceptionally impressive response to want to remind that we should be talking about the significance of multi anchor number moves, I’m not sure if that’s mentioned anywhere explicitly we bring prior to this in looking at transition metrics, but that should be discussed more clearly

**Anchored text:**

```
With facts + specification (C4a, 5-judge mean 5.00).
```

**Surrounding paragraph (full):**

> With facts + specification (C4a, 5-judge mean 5.00). Near-perfect inference:

**Status:** RESOLVED 2026-04-28 (applied to v11)  
**Resolution:** Multi-anchor moves significance addressed in two places. (1) §4.1 lede rewrite (C82) explicitly mentions "5-10% made multi-anchor jumps (1→3, 1→4, 2→5)" and frames them as "the wins at the margin the aggregate mean understates" — this puts the framing upstream of all examples. (2) Example C body now contains an inline callout: "In rubric-anchor terms, this is a 2.80 → 5.00 jump, crossing three integer anchors upward, exactly the kind of high-magnitude category-shift the §4.1 lede flags as the wins at the margin the aggregate mean understates." Closes C89.

---

## Comment 90 (id=405)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example C. Facts to Facts + Spec: abstention becomes near-perfect inference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:43:00Z

**Comment body:**

> This is spoken to within the gradient maybe can fold this in in some way Seems like this is being buried all the way down here given that the section title is on the cross subject gradient.

**Anchored text:**

```
The improvement is not uniform across subjects. It depends on how much the AI already knows about the person.
```

**Surrounding paragraph (full):**

> The improvement is not uniform across subjects. It depends on how much the AI already knows about the person. Plain version: the less the model’s pretraining has to work from, the more the specification can add. The more the model already knows, the less room the specification has to help, and on the highest-baseline subjects it can mildly hurt.

**Status:** RESOLVED 2026-04-28 (applied to v11)  
**Resolution:** §4.1 lede rewritten 2026-04-28 (Aarik approved Option A). Three-paragraph structure: (1) gradient finding with 9-of-9 + +0.89 headline, (2) category-shift framing with 55.0% anchor-crossing + multi-anchor jumps explicit, (3) structural sensitivity check (uniform C4a quality) demoted from lede to supporting evidence. Resolves the §1.3-v5 / §4.1 framing parallelism. Also closes C82 / C84 / C90 (all converged on the same gradient-as-load-bearing reframe).

---

## Comment 91 (id=408)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:47:00Z

**Comment body:**

> This will be color coded right in terms of the table?

**Anchored text:**

```
Per-subject results.
```

**Status:** DEFERRED 2026-04-27 (figure regen workstream)  
**Resolution:** Aarik asks whether Example D's per-subject results table will be color-coded. Already partially addressed: per-subject results table prose at line 678 of `beyond_recall_v11_draft.md` explicitly mentions tinting ("low-baseline rows are tinted green, mid-baseline rows are tinted yellow, and Franklin is tinted gray"). Confirmation that the docx render applies the tint is the docx-pass formatting workstream concern, not a markdown caption rewrite. Queued alongside C171 and C173.

---

## Comment 92 (id=633)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:48:00Z

**Comment body:**

> This is exceptionally heavy you should be spoken about in layman terms and then directed to the appendix for a more complete technical overview

**Anchored text:**

```
The first is a battery-question-type confound. Appendix B.6 reports a subject-level correlation of r = +0.595 between the fraction of LITERAL_RECALL questions in a subject’s battery and that subject’s mean Δ_spec, and an opposing correlation of r = −0.466 for INTERPRETIVE_INFERENCE fraction . The concern is that subjects whose batteries happen to lean literal-recall could pick up part of the apparent gradient slope on baseline. A multiple regression of Δ_C4a on both C5 baseline and LITERAL_RECALL fraction across the 14 main-study subjects yields a partial coefficient on baseline of −0.88 [95% CI −1.13, −0.63], p < 10⁻⁵, attenuated from the univariate −0.96 by about 8%. LITERAL_RECALL fraction enters as a significant partial predictor (β = +2.30 [+0.34, +4.26], p = 0.026), but baseline carr [...]
```

**Status:** APPLIED (2026-04-28)  
**Resolution:** Body para replaced with 4-sentence layman version pointing to Appendix B.6. Technical detail (multiple regression, partial coefficients, variance decomposition, VIF) moved to new B.6.2 subsection. No em-dashes.

---

## Comment 93 (id=634)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:49:00Z

**Comment body:**

> Likely when I make this a little bit more layman as well potentially redirect appendix. Follow

**Anchored text:**

```
The second is a Hamerton-leverage confound. Hamerton’s 80-question battery predates the global-subject pipeline and uses a slightly different backward-design path (the legacy Haiku 4.5 generator that originally produced Franklin and Hamerton); the 13 global subjects’ main-study batteries also use Claude Haiku 4.5 but were regenerated by run_global_rerun.py against a uniform prompt template. All 14 main-study batteries share the same generator family; the question is whether Hamerton’s high Δ_C4a is driving the gradient slope. A subset regression dropping Hamerton (N=13 globals) yields a slope of −0.89 [95% CI −1.18, −0.61], R² = 0.81, p < 10⁻⁴, compared to the full-sample −0.96. The point estimate attenuates by about 7%, and the 95% CIs overlap substantially. The gradient is not Hamerton-d [...]
```

**Status:** APPLIED (2026-04-28)  
**Resolution:** Body para replaced with 4-sentence layman version pointing to Appendix B.6. Technical detail (subset regression, slope, CIs, GPT-5.4 circularity-control battery note) moved to new B.6.3 subsection. No em-dashes.

---

## Comment 94 (id=635)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:49:00Z

**Comment body:**

> You just want to mention the controls When starting to talk about the battery composition sensitivity then two layman paragraphs on there and then this paragraph

**Anchored text:**

```
Neither control overturns the headline finding
```

**Surrounding paragraph (full):**

> Neither control overturns the headline finding. The gradient is not primarily driven by either battery-question-type composition or Hamerton’s legacy-generator battery. What these checks do not rule out is a more subtle confound in which generator differences are correlated with other unobserved subject characteristics; a cleanest future test would re-run a second-generator battery on the same 13 globals. Full analysis, per-subject data, and reproducibility script at docs/research/v10_battery_sensitivity_analysis.md and scripts/_v10_battery_sensitivity.py.

**Status:** APPLIED (2026-04-28)  
**Resolution:** Structure now matches Aarik's directive exactly. Para 1 "Battery-composition sensitivity. Two potential confounds..." mentions the controls. Two short layman paragraphs (Battery-question-type, Hamerton leverage) follow. The "Neither control overturns the headline finding" paragraph stays as closer. Appendix B.6 extended with B.6.1-B.6.4 subsections holding all technical detail.

---

## Comment 95 (id=636)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:49:00Z

**Comment body:**

> Foot

**Anchored text:**

```
. Full analysis, per-subject data, and reproducibility script at docs/research/v10_battery_sensitivity_analysis.md and scripts/_v10_battery_sensitivity.py.
```

**Surrounding paragraph (full):**

> Neither control overturns the headline finding. The gradient is not primarily driven by either battery-question-type composition or Hamerton’s legacy-generator battery. What these checks do not rule out is a more subtle confound in which generator differences are correlated with other unobserved subject characteristics; a cleanest future test would re-run a second-generator battery on the same 13 globals. Full analysis, per-subject data, and reproducibility script at docs/research/v10_battery_sensitivity_analysis.md and scripts/_v10_battery_sensitivity.py.

**Status:** APPLIED  
**Resolution:** Pulled docs/research and scripts paths into footnote [^battery-sensitivity-data].

---

## Comment 96 (id=637)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:50:00Z

**Comment body:**

> This needs to be layman. Potential redirect to appendix for extended technical analysis. This is using language that’s beyond me as well in terms of the mechanical one anchor is what the permutation null reproduces I have clue what that means

**Anchored text:**

```
Coupling-free reframing of the gradient. The headline slope regresses Δ_C4a = C4a − C5 on C5, which mechanically embeds a −1 component when C4a is bounded on the 1-5 scale and partially independent of C5. To triangulate from a non-coupling-prone angle, we ran three additional checks on the same per-subject (C5, C4a) data (script: scripts/_v10_coupling_sensitivity.py; full output: docs/research/v10_coupling_sensitivity_analysis.md). First, the level regression C4a ~ C5 produces a slope of +0.04 [95% CI −0.24, +0.33], R² = 0.008, p = 0.76. C4a is essentially flat across the C5 range of 1.02-2.77 and clusters tightly around its mean of 2.46. The spec does not differentially “lift” low-baseline subjects more in any treatment-effect-heterogeneity sense; it produces a roughly constant C4a qualit [...]
```

**Surrounding paragraph (full):**

> Coupling-free reframing of the gradient. The headline slope regresses Δ_C4a = C4a − C5 on C5, which mechanically embeds a −1 component when C4a is bounded on the 1-5 scale and partially independent of C5. To triangulate from a non-coupling-prone angle, we ran three additional checks on the same per-subject (C5, C4a) data (script: scripts/_v10_coupling_sensitivity.py; full output: docs/research/v10_coupling_sensitivity_analysis.md). First, the level regression C4a ~ C5 produces a slope of +0.04 [95% CI −0.24, +0.33], R² = 0.008, p = 0.76. C4a is essentially flat across the C5 range of 1.02-2.77 and clusters tightly around its mean of 2.46. The spec does not differentially “lift” low-baseline subjects more in any treatment-effect-heterogeneity sense; it produces a roughly constant C4a quality regardless of baseline, and the apparent gradient equals the baseline shortfall.

**Status:** APPLIED (2026-04-28)  
**Resolution:** §4.1 Coupling-free + Honest reframing blocks fully restructured. Body now carries layman-only prose with inline per-question breakdown (351 questions, 55% upward, 18% multi-anchor, 6% extreme). Bolded reframing rewritten per collective review (GPT-5.5 + Gemini 2.5 Pro): "low-baseline subjects have more opportunities for upward integer-band crossings, because their batteries contain more questions at low rubric anchors to begin with." Floor-not-ceiling observation added (no 3→5 transitions in 14-subject panel). Technical detail (level regression, permutation test, bootstrap) moved to new Appendix B.7 with B.7.1-B.7.4 subsections. §1.3 callout multi-anchor claim corrected from broken "5-10% (1→3, 1→4, 2→5)" to "18% multi-anchor (≥2 bands), 6% extreme (≥3 bands)." No em-dashes. Collective review at `docs/reviews/v11_c96_framing_review_20260428.md`.

---

## Comment 97 (id=639)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:51:00Z

**Comment body:**

> This term’s way too advanced

**Anchored text:**

```
treatment-effect-heterogeneity sense
```

**Surrounding paragraph (full):**

> Honest reframing. The steep negative Δ-on-C5 slope is largely a coupling artifact of the change-score parameterization. The substantive finding survives but its framing has to shift. The gradient is not “low-baseline subjects benefit differentially more from the spec” in a treatment-effect-heterogeneity sense. It is “the spec produces a roughly constant post-spec operating level on C4a near 2.5 across baselines spanning 1.0-2.8, so the lift in raw points is mechanically larger where the floor is lower.” This is still the practically relevant claim for the paper’s argument (the spec is the tool for the unknown, where unknown means low C5), but it is a statement about a near-constant post-spec operating level under this pipeline / response model / rubric, not about heterogeneous treatment effects across baseline strata. Subsequent sections that lean on the gradient (§4.4.2, §4.6, §5.5) should be read against this reframing.

**Status:** APPLIED  
**Resolution:** Replaced "in any treatment-effect-heterogeneity sense" with "more than high-baseline ones" (line 717) and "as a property of the subjects themselves" + "per-subject differences" (line 733).

---

## Comment 98 (id=638)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example D. The gradient at the extremes

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:51:00Z

**Comment body:**

> Not sure if this whole section is required it seems overkill May just want to move to limitations or appendix

**Anchored text:**

```
Honest reframing. The steep negative Δ-on-C5 slope is largely a coupling artifact of the change-score parameterization. The substantive finding survives but its framing has to shift. The gradient is not “low-baseline subjects benefit differentially more from the spec” in a treatment-effect-heterogeneity sense. It is “the spec produces a roughly constant post-spec operating level on C4a near 2.5 across baselines spanning 1.0-2.8, so the lift in raw points is mechanically larger where the floor is lower.” This is still the practically relevant claim for the paper’s argument (the spec is the tool for the unknown, where unknown means low C5), but it is a statement about a near-constant post-spec operating level under this pipeline / response model / rubric, not about heterogeneous treatment ef [...]
```

**Status:** RESOLVED-BY-C96 (2026-04-28)  
**Resolution:** "Honest reframing" block restructured by C96 — body prose layman-rewritten, technical detail moved to Appendix B.7. Closing reframing paragraph kept in body because it carries the load-bearing per-question reframe (without it the −0.96 slope sits unframed and the misleading "spec helps low-baseline more" reading dominates skim-reading). C98's "overkill / move to limitations" intent is satisfied by the C96 reduction; further removal would break the framing pivot.

---

## Comment 99 (id=642)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1.1 Franklin as the high-baseline reference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:05:00Z

**Comment body:**

> Wondering if this should be moved down towards the latter half of Section 4 so that we can get to compression and question improvement rate.

**Anchored text:**

```
4.1.1 Franklin as the high-baseline reference
```

**Status:** DEFERRED 2026-04-27 (figure regen workstream)  
**Resolution:** Aarik asks whether Example D's per-subject results table will be color-coded. This is a docx-pass formatting concern, not a markdown caption rewrite. The table currently lives at lines 689-703 of `beyond_recall_v11_draft.md` (the §4.1 "Per-subject results" table), with low/mid/high-baseline tinting noted in line 678 prose: "In the color-rendered PDF of the paper, the low-baseline rows are tinted green (the population of relevance), the mid-baseline rows are tinted yellow, and Franklin is tinted gray." Tint application is the docx-render pass workstream. No markdown change needed in this pass.

---

## Comment 100 (id=643)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.1.1 Franklin as the high-baseline reference

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:52:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw per-subject Franklin data is at results/franklin_legacy_20260411/.
```

**Status:** APPLIED  
**Resolution:** Pulled Franklin path into footnote [^franklin-data].

---

## Comment 101 (id=646)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2 Compression: structure vs. raw text

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:52:00Z

**Comment body:**

> Will need to describe this a bit more in depth. We’ll need to describe the axes point out where the baseline is Make sure this is looking or mentions that this is looking only at Hammerton. Point out what giving the full fact Corpus produced C4 or giving the full raw Corp is produced C8, in every situation where the spec was combined or served alone it outperformed in the judging metric. I’m not entirely sure what the dose response curve means and how to interpret a steep initial slope and a long plateau if you’re going to mention that then you have to mention why that is significant as well.

**Anchored text:**

```
Figure 4.2: A 7K-token specification recovers most of the lift the full source corpus delivers
```

**Surrounding paragraph (full):**

> Figure 4.2: A 7K-token specification recovers most of the lift the full source corpus delivers, at one to two orders of magnitude less context. 5-judge primary score (y-axis) vs. context size in tokens (x-axis, log scale) for each of the 9 low-baseline subjects (faint per-subject traces) with a bold median-across-subjects aggregate curve (§4.2). The first ~7K tokens of structured specification buy +0.68 points of lift over baseline; the next ~80K to ~400K tokens of raw corpus buy only an additional +0.22. The dose-response curve has a steep initial slope and a long plateau.

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 4.2 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP. Caption now opens with "How to read this figure": x-axis is context size in tokens (log scale, 1K to 400K), y-axis is the 5-judge primary score on the 1-5 rubric, faint traces are individual low-baseline subjects, bold curve is the median-across-subjects aggregate. Walks the reader left-to-right through C5 baseline (1.52), C2a (~7K tokens, 2.23), C4 (2.35), C8 (~80K-400K tokens, 2.45), C4a (2.45), C9 (2.50). Explicitly states that wherever the spec is added or served alone, the score sits at or above the no-spec equivalent. Explains the dose-response shape in plain language: behaviorally relevant signal in autobiographical text is sparse and compressible; structured packaging captures most of what matters. Confirms this is the Hamerton-style compression story aggregated across the 9 low-baseline subjects.

---

## Comment 102 (id=649)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2 Compression: structure vs. raw text

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:55:00Z

**Comment body:**

> May want to put this in a table and include one two words on what each condition is just to make it clear.

**Anchored text:**

```
(mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50).
```

**Surrounding paragraph (full):**

> Context improves prediction. On the 9 low-baseline subjects, every context condition increases the per-subject mean score by roughly one full rubric point over the no-context baseline (mean C5 = 1.52; mean C2a = 2.23; mean C4 = 2.35; mean C8 = 2.45; mean C4a = 2.45; mean C9 = 2.50). The AI does not need much context to move from refusal-and-off-base to engaged subject-specific prediction. It needs some context.

**Status:** APPLIED (2026-04-28)  
**Resolution:** Inline 6-condition mean list converted to 4-column table (Condition / Context served / Mean / Δ from C5). Δ column added per Aarik (Option B) to surface the C8 = C4a convergence at +0.93 and the marginal C9 lead at +0.98.

---

## Comment 103 (id=650)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2 Compression: structure vs. raw text

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:55:00Z

**Comment body:**

> You mentioned 7K tokens here and mention that it order of magnitude smaller but not what that order of magnitude is, may want to refer to the per subject compression comparison more quickly?.

**Anchored text:**

```
7,000-token
```

**Surrounding paragraph (full):**

> The compact specification captures the large majority of that improvement. A 7,000-token Behavioral Specification recovers most of what the full raw corpus delivers, despite being an order of magnitude or more smaller. Across the 9 low-baseline subjects, the raw corpus (C8) averages 0.22 points higher than spec alone (C2a). The corpus’s edge is real but small relative to the context-size gap that produces it.

**Status:** APPLIED  
**Resolution:** Replaced "an order of magnitude or more smaller" with "roughly 5x to 80x smaller depending on subject (per-subject compression ratios in the table below)".

---

## Comment 104 (id=651)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2 Compression: structure vs. raw text

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:56:00Z

**Comment body:**

> Now I understand what you’re referring to with the dose response That needs to be a bit more implicit when talking about it earlier if deciding to keep that within the graphic explanation

**Anchored text:**

```
The efficiency claim in one metric: predictive gain per 1,000 tokens of context. The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. The dose-response curve has a steep initial slope and a long plateau
```

**Surrounding paragraph (full):**

> The efficiency claim in one metric: predictive gain per 1,000 tokens of context. The first ~7K tokens of structured specification buy roughly +0.68 points of lift above baseline on average. The next ~80K to 400K tokens of raw corpus buy an additional +0.22 points on average. The dose-response curve has a steep initial slope and a long plateau. The behaviorally relevant signal in autobiographical text is sparse and compressible, and most of what matters can be packaged into a compact structured document.

**Status:** APPLIED (2026-04-28)  
**Resolution:** "Dose-response curve" term dropped from both §4.2 body (line 764) and footnote (line 864). Body: "The dose-response curve has a steep initial slope and a long plateau" → "Plotted against context size, the score climbs steeply at first and flattens out." Footnote: "shows the dose-response curve with its steep initial slope and long plateau" → "shows the steep initial climb and long plateau." Pharmacology metaphor removed; preceding concrete numbers (7K tokens → +0.68; 80K-400K tokens → +0.22) already carry the dose-response shape without the borrowed term. Figure 4.2 caption rewrite (when figure regenerated) will follow same convention.

---

## Comment 105 (id=778)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2 Compression: structure vs. raw text

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:03:00Z

**Comment body:**

> Honestly interesting that it even adds over raw corpus

**Anchored text:**

```
The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.
```

**Surrounding paragraph (full):**

> Adding the specification on top of the full raw corpus (C9) adds ~0.05 points on average over raw corpus alone. The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

**Status:** EXPANDED-INTO-WINS-ANALYSIS-PASS (2026-04-28)  
**Resolution:** What started as a flag on the +0.05 C9-vs-C8 Δ became a substantive analytical investigation. Aarik directives across the walk: (1) means hide per-question variance, surface it everywhere; (2) wins at the margin (multi-anchor jumps) cannot be discounted, may be elevated to headline findings; (3) characterize what defines big-win questions (axis, failure modes, spec drivers); (4) within-band fractional shifts also matter, look as small as 0.1 to test meta-judging behavior. **Three-phase analysis underway:**

- **Phase 1 (DONE):** Comprehensive wins inventory across 18 condition pairs at `docs/research/wins_inventory_20260428.json`. 150 paired questions show extreme upward jumps (≥3 anchors); cross-checks reproduce existing published numbers exactly. Build script: `scripts/build_wins_inventory.py`. C5→C2c surfaces 8 extreme downward jumps as a complementary risk story.
- **Phase 2 — Stream X (IN FLIGHT):** Big-wins characterization. Question-axis distribution, pre-response failure-mode taxonomy, post-response success-mode taxonomy, spec-content driver attribution, subject correlation, question archetypes the spec dominates on, future-work implications. Output: `docs/research/big_wins_characterization_20260428.{json,md}`.
- **Phase 2 — Stream Y (IN FLIGHT):** Within-band fractional shift analysis + meta-judging behavior. Bucketed distribution at 0.1 / 0.25 / 0.5 / 1.0 thresholds, top half-anchor within-band shifts per pair, judge direction-agreement curve by panel-Δ magnitude, per-judge sensitivity profile (lumpy vs sensitive), Spearman rank agreement per pair, missed-signal estimate. Output: `docs/research/within_band_shifts_20260428.{json,md}`.
- **Phase 3 (queued, post-X+Y):** Framing-implications report at `docs/reviews/wins_framing_implications_20260428.md`. Audits paper for where aggregate Δ language buries per-question wins; recommends section-level reframes; surfaces story-level pivot question (does paper headline shift from "spec lifts low-baseline mean" to "spec produces specific transformative per-question wins"?); risk profile on cherry-picking and small-N concerns.

**No paper edits applied.** All three phases produce research artifacts only. Aarik will read the synthesized framing report and decide which pivots to apply on a separate walk.

---

## Comment 106 (id=781)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2.1 Question-improvement rate: a candidate secondary reporting metric

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:06:00Z

**Comment body:**

> Wondering if we should be getting to this earlier. And if this should be a subsection under 4.2. Seems like it should be its own, neither think about it.

**Anchored text:**

```
4.2.1 Question-improvement rate: a candidate secondary reporting metric
```

**Status:** PENDING  
**Resolution:** Substantive - move §4.2.1 earlier or under §4.2 as subsection. Structural call.

---

## Comment 107 (id=820)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2.1 Question-improvement rate: a candidate secondary reporting metric

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:10:00Z

**Comment body:**

> Similar to the previous figure feedback need to explain visually what’s going on here

**Anchored text:**

```
Figure 4.2.1. Per-question outcome distribution across conditions (low-baseline slice, n = 9 subjects, 351 questi
```

**Surrounding paragraph (full):**

> Figure 4.2.1. Per-question outcome distribution across conditions (low-baseline slice, n = 9 subjects, 351 questions; C9 n = 312 with Babur excluded for context-window). Three lines track the share of questions that improved, tied, or worsened relative to the no-context C5 baseline. The x-axis orders conditions from raw corpus first (C8) through spec-alone (C2a), facts-alone (C4), facts + spec (C4a), and corpus + spec (C9). The specification alone (C2a) improves 70.9% of questions at roughly an order of magnitude less context than the raw corpus (C8, 78.3%). Facts + spec (C4a) matches the raw corpus’s improvement rate while cutting the tie band in half. Median Δ when improved = +1.00 rubric points; median Δ when worsened = −0.40 points.

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 4.2.1 inline caption rewritten in `docs/beyond_recall_v11_draft.md` line 803 (the only figure with an inline image+caption block in the v11 markdown). Caption now opens with "How to read this figure": walks reader through the x-axis condition order (C8 -> C2a -> C4 -> C4a -> C9), the y-axis (share of 351 paired low-baseline questions), and the three colored lines (green improved, yellow tied, red worsened). Spells out the four improvement rates inline (70.9%, 72.9%, 78.3%, 78.6%) and the median Δ guards (+1.00 / -0.40). C9 sample reduction (n=312, Babur excluded for context-window) called out at the start of the axis description.

---

## Comment 108 (id=836)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2.1 Question-improvement rate: a candidate secondary reporting metric

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:12:00Z

**Comment body:**

> 

**Anchored text:**

```
The raw corpus outscores the spec alone on more questions than it loses, but the spec outscores the corpus on roughly one-third of them. On the combined conditions, the 7K-token facts + spec package outscores the much larger corpus + spec package on 36.5% of questions.
```

**Status:** RESOLVED  
**Resolution:** Comment body empty. No actionable content.

---

## Comment 109 (id=837)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.2.1 Question-improvement rate: a candidate secondary reporting metric

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:12:00Z

**Comment body:**

> You may want to move this to limitations or future work. Can end this section with the previous paragraph, and just make a note of failure modes and refer to them and link it.

**Anchored text:**

```
Failure modes if this metric is adopted. The panel-reviewed limitations worth flagging explicitly for any future use:Tiny-gain inflation. A method producing +0.02-point gains on 80% of questions would register as a 80% improvement rate. The magnitude triplet (median Δ when improved) is the guard: if median improvement magnitude is near zero, the rate is misleading. Our low-baseline specification has median Δ = +1.00, so this failure mode does not apply to the reported numbers; it is a known trap for anyone adopting the metric.Hidden catastrophic harm. A method that improves 85% and catastrophically harms 15% would look strong. The worsening-magnitude column is the guard: median worsening of −0.40 on spec-alone indicates the hurt is bounded.Easy-baseline gaming. Improvement rates can be inf [...]
```

**Surrounding paragraph (full):**

> Failure modes if this metric is adopted. The panel-reviewed limitations worth flagging explicitly for any future use:

**Status:** PENDING  
**Resolution:** Substantive - move "Failure modes if this metric is adopted" to limitations or future work; end §4.2.1 with the previous paragraph + reference link. Structural restructure for Aarik to direct.

---

## Comment 110 (id=840)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example: Hamerton, the compression story at its clearest

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:13:00Z

**Comment body:**

> Need to direct to repo in the footnotes Likely need to add an appendix section for each subject. Can refer to that within this paragraph if someone is interested in viewing actual examples for this subject or any other subject across a range of scenarios, similar to how we have referenced examples earlier.

**Anchored text:**

```
Hamerton, the compression story at its clearest
```

**Surrounding paragraph (full):**

> Example: Hamerton, the compression story at its clearest

**Status:** PENDING  
**Resolution:** Substantive content add - Aarik wants per-subject appendix sections referenced from these examples. Larger architectural change for the paper. Recommend adding a one-line "see Appendix X for per-subject example sets" pointer once that appendix exists.

---

## Comment 111 (id=843)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example: Ebers, the honest cost of compression

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:15:00Z

**Comment body:**

> We need to do an examination of why the score was so low. Was honest abstention may be worth understanding before we finalize this particular example. Same goes linking selected examples.

**Anchored text:**

```
Example: Ebers, the honest cost of compression
```

**Status:** PENDING  
**Resolution:** Substantive analysis ask - examine why Ebers C2a score was 1.54 (was honest abstention?). Requires fresh analysis. Mark for follow-up.

---

## Comment 112 (id=844)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example: Ebers, the honest cost of compression

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:16:00Z

**Comment body:**

> Should be in the footnotes. All repo related guidance and navigation should be referred to in footnotes generally.

**Anchored text:**

```
Raw per-subject data is at results/global_<subject>/c8_c9_results.json and results/global_<subject>/results_v2.json. The compression analysis and question-improvement rate computation are in scripts/recompute_5judge_primary.py and scripts/compute_question_improvement_rate.py. Figure 4.2 plots score versus context size (log scale) per subject and shows the dose-response curve with its steep initial slope and long plateau.
```

**Status:** APPLIED  
**Resolution:** Pulled compression raw-data paragraph into footnote [^compression-data].

---

## Comment 113 (id=847)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:17:00Z

**Comment body:**

> Similar to other feedback on figures need to describe visually what’s going on here. May want to specify where high baseline subjects are. Likely would want to sort by baseline score. This might make the effect a little bit more clear in terms of where the spec helps. Can denote that by a horizontal line of low baseline mid and high baseline. Would also potentially be worth either providing figures on this chart or within the figure explanation stating that in all situations the wrong specification was worse than the correct specification. In most cases or twelve out of 14 it seems the correct spec performed worse than baseline.. Otherwise this is great

**Anchored text:**

```
Figure 6: The specification’s effect is content-specific, not structure-specific. A wrong subject’s spec, served in the right one’s place, does not reproduce the lift. Per-subject score (y-axis) for the correct specification (C2a, Δ = +0.35), a random-derangement wrong spec (C2c v2, Δ = +0.22), and an adversarial maximum-distance wrong spec (C2c v1, Δ = −0.25) on the 13 global subjects, baseline shown for reference (§4.3). The correct-vs-adversarial gap of 0.60 points on the 1-5 rubric (more than half a full rubric category) is the content effect.
```

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 6 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP. Caption now opens with "How to read this figure": x-axis is the 13 global subjects (Hamerton excluded; he has no wrong-spec run) sorted by C5 baseline left-to-right (low-baseline left, mid-baseline right). Within each subject cluster: 4 bars (C5, C2a correct, C2c v2 random wrong, C2c v1 adversarial wrong). Caption now explicitly notes (i) in all 13 subjects the wrong specification scored lower than the correct specification served on the same subject; (ii) under adversarial v1 pairing, 8 of 13 subjects scored lower than no-context C5 baseline (Augustine, Babur, Cellini, Equiano, Keckley, Rousseau, Seacole, Zitkala-Sa). NOTE on Aarik's "12 of 14": the data does not support 12 of 14 wrong-spec subjects scoring below baseline. Per `docs/research/v11_emit/4_3_wrong_spec.json`, the actual count is 8 of 13 under v1 (adversarial) and 4 of 13 under v2 (random). The caption uses the actual 8/13 figure for v1. The 0.60-point correct-vs-adversarial gap retained as the content effect bottom line.

---

## Comment 114 (id=850)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:20:00Z

**Comment body:**

> I generally think this is good needs to be a bit more

**Anchored text:**

```
Figure 4: Adding the Behavioral Specification near-eliminates baseline hedging and refusal on subjects the model does not already know. Refusal rate (y-axis) across the C5 → C2a → C4a context conditions (x-axis) on the 9 low-baseline subjects, under the narrow starts_refusal classifier (§4.3). Rate drops from 28.8% at no-context baseline to 1.4% with spec alone to 0.0% with facts plus spec, an order-of-magnitude reduction at each step. The broader-rule classifier (41.2% → 7.9% → 0.4%) shows the same direction.
```

**Status:** RESOLVED  
**Resolution:** Comment body too incomplete to action ("I generally think this is good needs to be a bit more"). Anchor is figure caption handled by other agent.

---

## Comment 115 (id=853)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:21:00Z

**Comment body:**

> Can likely move this to footnotes. Drop the in before this.

**Anchored text:**

```
scripts/run_global_rerun.py
```

**Surrounding paragraph (full):**

> The two wrong-spec variants differ by construction. v1 (fixed derangement) is a hardcoded pairing in scripts/run_global_rerun.py designed so each subject receives the specification of a culturally- and temporally-distant other . v2 (random derangement) is a seed-fixed random permutation in which no subject receives its own specification but pairings can land culturally-close; this tempers the aggregate drop. Reporting both shows that even a random wrong-spec barely beats no context, and an adversarial wrong-spec actively hurts.

**Status:** APPLIED  
**Resolution:** Pulled scripts/run_global_rerun.py reference into footnote [^wrong-spec-script]. "in" was a normal preposition, no stray.

---

## Comment 116 (id=854)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:22:00Z

**Comment body:**

> Needs to be

**Anchored text:**

```
The per-subject heterogeneity is consistent with the mechanism reading:
```

**Surrounding paragraph (full):**

> Per-subject wrong-spec deltas. The aggregate Δs above are not uniform across subjects. Five of thirteen subjects show small positive deltas under the adversarial v1 pairing (Bernal Diaz, Ebers, Fukuzawa, Sunity Devee, Yung Wing); the remaining eight show negative deltas that drag the aggregate to −0.25. Under the random v2 pairing, four subjects show negative deltas (Cellini, Equiano, Rousseau, Seacole); the remaining nine span small to moderate positive deltas. The per-subject heterogeneity is consistent with the mechanism reading: adversarial pairing hurts most subjects and helps a few where coincidental content overlap matches the target subject’s pattern; random pairing flips the proportion because cultural-temporal distance is, on average, smaller.

**Status:** RESOLVED  
**Resolution:** Comment body incomplete ("Needs to be"). No actionable content.

---

## Comment 117 (id=855)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:23:00Z

**Comment body:**

> Likely should be footnote

**Anchored text:**

```
Per-subject scaffold values at docs/research/v11_emit/4_3_wrong_spec.json (claim ids 4_3_<subject>_c2c_v1_delta / 4_3_<subject>_c2c_v2_delta).
```

**Surrounding paragraph (full):**

> 5-judge primary panel; per-subject Δ vs. C5 baseline. Bolded v1 deltas are the five subjects where adversarial pairing produces a positive delta. Per-subject scaffold values at docs/research/v11_emit/4_3_wrong_spec.json (claim ids 4_3_<subject>_c2c_v1_delta / 4_3_<subject>_c2c_v2_delta).

**Status:** APPLIED  
**Resolution:** Pulled scaffold-id reference into footnote [^wrong-spec-scaffold].

---

## Comment 118 (id=856)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:24:00Z

**Comment body:**

> Should likely have a chart or figure for this

**Anchored text:**

```
Spec-activation evidence.
```

**Status:** DEFERRED 2026-04-27 (figure regen workstream)  
**Resolution:** Aarik asks for a chart/figure for the spec-activation evidence (78.6% tag-citation rate on correct-spec vs 50.0% on wrong-spec, 28.6-point content-activation gap). This is a NEW figure not currently in the paper and requires PNG regen plus an inline image+caption insertion in §4.3. Out of scope for this caption-rewrite pass. Queued for the docx-pass / PNG-regen workstream. Suggested figure: bar chart of tag-citation rates by condition (C2a correct, C2c v1 adversarial, C2c v2 random) with the 28.6-point gap annotated; data source `docs/research/spec_activation_analysis.json`.

---

## Comment 119 (id=857)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.3 Mechanism: Content, Not Format

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:24:00Z

**Comment body:**

> Data can be in footnotes

**Anchored text:**

```
Tag-citation analysis on response text (data at docs/research/spec_activation_analysis.json)
```

**Surrounding paragraph (full):**

> Tag-citation analysis on response text (data at docs/research/spec_activation_analysis.json) shows the content-activation gap. On correct-spec conditions, 78.6% of responses explicitly cite at least one spec tag (anchor ID, axiom reference, predictive-template label). On wrong-spec conditions, only 50.0% do. The 28.6-point gap is a lower bound on the content effect: models may draw on spec content without literally quoting tag IDs, so the true divergence is wider. The baseline reading is that models recognize when the specification fits the question and engage with it; they recognize when it doesn’t fit and disengage or improvise.

**Status:** APPLIED  
**Resolution:** Pulled spec_activation_analysis.json path into footnote [^spec-activation-data].

---

## Comment 120 (id=862)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example B (wrong-spec), Bernal Diaz Q16: content convergence across genuinely different frameworks

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:27:00Z

**Comment body:**

> Don’t like the language around five judge primary mean 4.6, drop only minus 0.2 verse the correct too many words in the title Same thing happens with EBERS—Right spec verse wrong spec score

**Anchored text:**

```
C2c v1 fixed-derangement condition, 5-judge primary mean 4.60, drop only −0.20 vs. the correct-spec C4a condition’s 4.80):
```

**Surrounding paragraph (full):**

> Wrong-spec response (C2c v1 fixed-derangement condition, 5-judge primary mean 4.60, drop only −0.20 vs. the correct-spec C4a condition’s 4.80):

**Status:** APPLIED  
**Resolution:** Compressed verbose example titles in §4.3 wrong-spec Examples A and C ("large drop vs. correct spec, X.XX vs. Y.YY") and Example B ("near-tie with correct spec, 4.60 vs. 4.80").

---

## Comment 121 (id=864)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example B (wrong-spec), Bernal Diaz Q16: content convergence across genuinely different frameworks

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:28:00Z

**Comment body:**

> I think this is stating that clearly the spec is also being used by the model so if there is convergence it still can be helpful for producing a more aligned answer just seeks to confirm the hypothesis that the spec does in fact change model behavior.

**Anchored text:**

```
Why this matters for the aggregate numbers. This is the coincidence case that lifts the wrong-spec aggregate above zero. When the fixed derangement (v1) happens to pair subjects whose behavioral patterns converge on the same surface prediction for a given question, wrong-spec lift is real on that question, not an artifact. Across the 507-response v2 cohort (13 globals × 39 questions), mismatch-loss dominates on the adversarial v1 pairing (aggregate Δ −0.25, same 13 globals × 39 questions) and roughly balances on the random v2 pairing (aggregate Δ +0.15). Example B is one of the roughly 5-10% of questions where content coincidence produces correct-surface, wrong-logic predictions.
```

**Status:** PENDING  
**Resolution:** Aarik flag on the convergence-confirms-hypothesis reading. No edit requested; observational comment for discussion.

---

## Comment 122 (id=867)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example C (wrong-spec), Seacole Q2: interpretive inference fails

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:29:00Z

**Comment body:**

> It’s very interesting that I was able to pull this understanding out. I hope we talk about this more in future work, or safety related in terms of it was able to recognize this could it recognize that there are certain values that are against other people or broad swaths of the population,

**Anchored text:**

```
“The specification you’ve provided describes someone from the 16th-century Spanish conquest period — the epistemic anchors, loyalty architecture, divine mandate framing, and forward compulsion all point to that historical context. Mary Seacole (1805-1881) was a Creole nurse and travel writer from Jamaica who served in the Crimean War.
```

**Surrounding paragraph (full):**

> “The specification you’ve provided describes someone from the 16th-century Spanish conquest period — the epistemic anchors, loyalty architecture, divine mandate framing, and forward compulsion all point to that historical context. Mary Seacole (1805-1881) was a Creole nurse and travel writer from Jamaica who served in the Crimean War. These are entirely different people from different centuries with different frameworks. … I don’t have documented instances of this. I could speculate based on her memoir’s tone and her known character, but that would be inference, not behavioral specification.”

**Status:** PENDING  
**Resolution:** Aarik observational note about Seacole wrong-spec recognizing cultural mismatch. Suggests future-work / safety angle. Not an edit; flag for §7.6 future-work consideration.

---

## Comment 123 (id=895)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Example C (wrong-spec), Seacole Q2: interpretive inference fails

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:32:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw per-judge data and full response text are at results/global_<subject>/results_v2.json (wrong-spec responses) and results/global_<subject>/judgments_v2.json (per-judge scores). The analysis scripts are scripts/compute_wrong_spec_5judge.py and scripts/compute_wrong_spec_per_subject.py.
```

**Status:** APPLIED  
**Resolution:** Pulled §4.3 raw-data paragraph into footnote [^wrong-spec-raw-data].

---

## Comment 124 (id=900)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:28:00Z

**Comment body:**

> There is no clear conclusion at the end of Section 4. Not sure if that’s supposed to be in discussion future work or somewhere else but there is no formal closing statement

**Anchored text:**

```
4.4.1 Aggregate performance across systems
```

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 125 (id=901)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:34:00Z

**Comment body:**

> Likely should provide a horizontal bar that provides mean improvement maybe something that really stands out. Instead of having mean on the same axis as the subject it would cut across. I’m also curious for each of these how many of them resulted in movement across an anchor number. Maybe in the description can state that X out of Y subjects with this memory system plus spec scores crossed atleast 1 anchor number over x aggregate questions?

**Anchored text:**

```
Figure 7:
```

**Surrounding paragraph (full):**

> Figure 7: Three of four commercial memory systems benefit when the Behavioral Specification is layered on top of their retrieval. Per-system spec delta (Δ_spec = C3 mean − C1 mean, x-axis) across the 9 low-baseline subjects, grouped by memory system, with positive-subject counts on the system labels (§4.4.1). Zep (Δ +0.17, 9/9 positive) and Letta-archival (Δ +0.17, 8/9) are the cleanest gains; Mem0 (Δ +0.10, 6/9) and Base Layer’s local retrieval substrate (Δ +0.08, 6/9) are smaller but positive; Supermemory aggregates near zero (Δ −0.01, 5/9) because per-question swings cancel (median improvement +1.45, median worsening −1.41; treated in §4.4).

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 7 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP. Caption now opens with "How to read this figure": y-axis is each memory system, x-axis is the per-system spec delta (Δ_spec = C3 mean − C1 mean). Per-system anchor-crossing rates from `docs/research/per_system_anchor_crossing_20260427.md` added inline (controlled C1->C3 configuration, low-baseline scope, n = 351 paired questions per system across 9 subjects, all 9/9 subjects had at least one upward crossing per system): Base Layer 29.0%, Zep 27.9%, Letta 26.9%, Mem0 23.4%, Supermemory 20.2%. Caption explicitly states that aggregate Δ and per-question anchor-crossing rate agree on rank ordering. Aggregate deltas (Zep +0.17 9/9, Letta +0.17 8/9, Mem0 +0.10 6/9, Base Layer +0.08 6/9, Supermemory −0.01 5/9) retained. Note: native (`_fp`) anchor-crossing rates are not used here because Figure 7 plots the controlled C1->C3 configuration.

---

## Comment 126 (id=904)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:36:00Z

**Comment body:**

> A bit too much padding under the graph for this figure Not sure if you need to include the little note at the bottom of the image.

**Anchored text:**

```
Figure 3:
```

**Surrounding paragraph (full):**

> Figure 3: Embedding-based memory systems given identical inputs return substantially different retrieved facts. All-three-disagree rate (y-axis) across Mem0, Letta, and Supermemory at top-k = 1, 3, 5, and 10 (x-axis), in the controlled configuration where every system received the same pre-extracted fact pool (§4.4.1, supports retrieval-substrate variability). 93% of the 515 questions produce a fully disjoint top-1 across the three systems; even at top-10, 53% remain fully disjoint. Retrieval is not a stable substrate to evaluate the specification on top of without an apples-to-apples controlled condition.

**Status:** RESOLVED 2026-04-27  
**Resolution:** Figure 3 caption rewritten in `scripts/export_v11_to_docx.py` FIGURE_MAP. Aarik's note was that the bottom-of-image footer text (the third-sentence interpretive note about retrieval not being a stable substrate) was redundant given the body prose around it. Caption trimmed: kept the headline measurement (all-three-disagree rate across Mem0/Letta/Supermemory at top-k = 1, 3, 5, 10 in the controlled configuration) and the two load-bearing numbers (93% disjoint top-1, 53% disjoint top-10). Dropped the closing "Retrieval is not a stable substrate to evaluate the specification on top of without an apples-to-apples controlled condition" sentence (that interpretive read is in the §4.4.1 body prose around the figure).

---

## Comment 127 (id=907)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:37:00Z

**Comment body:**

> Again don’t need to add plain version don’t need to insult the reader

**Anchored text:**

```
Plain version
```

**Surrounding paragraph (full):**

> Plain version. When the Behavioral Specification is added on top of a commercial memory system’s retrieval, the combined context produces better behavioral prediction than retrieval alone on people the model doesn’t already know. The effect holds on three of the four commercial systems we tested.

**Status:** APPLIED  
**Resolution:** Dropped "Plain version." header at start of §4.4.1 plain-version paragraph.

---

## Comment 128 (id=908)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:37:00Z

**Comment body:**

> May want to open 4.4 .1 with this and then add the graphs potentially

**Anchored text:**

```
When the Behavioral Specification is added on top of a commercial memory system’s retrieval, the combined context produces better behavioral prediction than retrieval alone on people the model doesn’t already know. The effect holds on three of the four commercial systems we tested.
```

**Surrounding paragraph (full):**

> Plain version. When the Behavioral Specification is added on top of a commercial memory system’s retrieval, the combined context produces better behavioral prediction than retrieval alone on people the model doesn’t already know. The effect holds on three of the four commercial systems we tested.

**Status:** PENDING  
**Resolution:** Substantive - Aarik suggests opening §4.4.1 with the now-de-headed paragraph and putting graphs after. Structural restructure call.

---

## Comment 129 (id=909)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:38:00Z

**Comment body:**

> Don’t need to bring up this ingestion failure for supermemories specifically

**Anchored text:**

```
Supermemory native data: four subjects (Bernal Diaz, Babur, Cellini, Rousseau) initially encountered ingestion failures on the free-tier Supermemory API. A paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures)
```

**Surrounding paragraph (full):**

> Supermemory native data: four subjects (Bernal Diaz, Babur, Cellini, Rousseau) initially encountered ingestion failures on the free-tier Supermemory API. A paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures) and retrieved 4.3-5.0 facts per question across these four subjects, with the 5-judge primary panel re-run on the resulting responses; the native Supermemory aggregate reported above reflects the paid-tier rerun, with all 14 main-study subjects (Hamerton + 13 globals) included. Base Layer has no separate “native” condition because Base Layer’s authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.

**Status:** APPLIED  
**Resolution:** Compressed paid-tier-rerun caveat - dropped ingestion-failure-counts language; aggregate now reads as "covers all 14 main-study subjects under a paid-tier rerun completed 2026-04-23".

---

## Comment 130 (id=910)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:39:00Z

**Comment body:**

> Is this still relevant We should have fixed this.

**Anchored text:**

```
Methodological caveat: Supermemory NO_RETRIEVAL placeholders. Across the full 14-subject Supermemory analysis, 30 individual responses (Augustine 2 questions, Equiano 28 questions) were Supermemory provider-failure placeholders rather than substantive predictions, scored at the rubric floor (1) by the judge panel. We treat these as scored data rather than missing data, consistent with how the rest of the study handles low-quality responses. If the 30 NO_RETRIEVAL records were excluded as missing data instead, Supermemory’s aggregate Δ would shift slightly higher; the qualitative story (small aggregate, bimodal per-question distribution) holds either way.
```

**Status:** APPLIED  
**Resolution:** Compressed NO_RETRIEVAL caveat to footnote [^supermemory-no-retrieval]; main text retains the 7-of-9 native-coverage note.

---

## Comment 131 (id=911)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:40:00Z

**Comment body:**

> I think generally need to be providing a bit more context on how significant these lips are for each of the memory providers yes we can make a directional claim that the brief at the very least does not hurt I think it gets more interesting if you look at question by question and see a similar breakdown to the number of questions that crossed anchor numbers. For each of the memory systems would be interesting to see those aggregated results. How many questions did it move from one to two or one to three or one to 5 2 to 3 or 2 to 6. We can use those aggregated numbers to get better understanding. If we haven’t run that analysis already we should be.

**Anchored text:**

```
Summary of the composition result.
```

**Status:** PENDING  
**Resolution:** Substantive analysis ask - Aarik wants per-question anchor-crossing breakdown by memory system (1->2, 1->3, 1->5, 2->3 etc.). The §4.4.1 per-system summary already gives upward/downward anchor-crossing rates and lists 2-band/3-band/4-band jump counts; full transition-matrix analysis would be additional work. Recommend Aarik direct whether to add transition-matrix tables per system.

---

## Comment 132 (id=914)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.1 Aggregate performance across systems > Supermemory: what the near-zero aggregate actually means

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:42:00Z

**Comment body:**

> Needs to be in footnote

**Anchored text:**

```
Scaffold values: 4_4_2_supermemory_helps_n (57), 4_4_2_supermemory_hurts_n (53), 4_4_2_supermemory_paired_total_n (546).
```

**Surrounding paragraph (full):**

> Per-event magnitudes are roughly symmetric (+1.55 vs −1.38 on the 1-5 rubric); the count is roughly balanced (57 helps vs 53 hurts). The aggregate is small because two opposite mechanisms are at work across different questions, with the helps slightly outnumbering the hurts at the per-question level under strict 5-judge primary aggregation. Scaffold values: 4_4_2_supermemory_helps_n (57), 4_4_2_supermemory_hurts_n (53), 4_4_2_supermemory_paired_total_n (546).

**Status:** APPLIED  
**Resolution:** Pulled scaffold values into footnote [^supermemory-scaffold].

---

## Comment 133 (id=920)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:43:00Z

**Comment body:**

> This should not be in the title. Might be one separate line to start the body off for context.

**Anchored text:**

```
Fukuzawa Q26 (Δ +2.20, C1 2.00 → C3 4.20)
```

**Status:** APPLIED  
**Resolution:** Dropped Delta/C1/C3 numerics from Example 1 title; moved to italic context line below.

---

## Comment 134 (id=923)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Supermemory Example 2. Spec hurts by over-theorizing a plain question. Yung Wing Q5 (Δ −2.40, C1 4.20 → C3 1.80)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:43:00Z

**Comment body:**

> Sim here

**Anchored text:**

```
Supermemory Example 2. Spec hurts by over-theorizing a plain question. Yung Wing Q5 (Δ −2.40, C1 4.20 → C3 1.80)
```

**Status:** APPLIED  
**Resolution:** Same treatment for Example 2.

---

## Comment 135 (id=926)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Supermemory Example 3. Judging issue, spec-induced meta-refusal. Zitkala-Sa Q18 (Δ −2.00, C1 3.00 → C3 1.00)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:43:00Z

**Comment body:**

> Same here

**Anchored text:**

```
Zitkala-Sa Q18 (Δ −2.00, C1 3.00 → C3 1.00)
```

**Surrounding paragraph (full):**

> Supermemory Example 3. Judging issue, spec-induced meta-refusal. Zitkala-Sa Q18 (Δ −2.00, C1 3.00 → C3 1.00)

**Status:** APPLIED  
**Resolution:** Same treatment for Example 3.

---

## Comment 136 (id=929)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Supermemory Example 4. Subtle reframe that scores well but unevenly. Fukuzawa Q16 (Δ +1.60, C1 2.40 → C3 4.00)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:44:00Z

**Comment body:**

> Same here

**Anchored text:**

```
Fukuzawa Q16 (Δ +1.60, C1 2.40 → C3 4.00)
```

**Surrounding paragraph (full):**

> Supermemory Example 4. Subtle reframe that scores well but unevenly. Fukuzawa Q16 (Δ +1.60, C1 2.40 → C3 4.00)

**Status:** APPLIED  
**Resolution:** Same treatment for Example 4.

---

## Comment 137 (id=930)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > Supermemory Example 4. Subtle reframe that scores well but unevenly. Fukuzawa Q16 (Δ +1.60, C1 2.40 → C3 4.00)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:47:00Z

**Comment body:**

> Likely in footnotes

**Anchored text:**

```
Raw data and scripts. Per-system per-subject per-judge scores at results/global_<subject>/*_judgments*.json. The 5-judge primary recompute report is at docs/research/memory_systems_5judge_primary.md. The aggregation script is scripts/compute_memory_systems_5judge.py.
```

**Status:** APPLIED  
**Resolution:** Pulled §4.4.1 raw-data block into footnote [^memsys-aggregate-data].

---

## Comment 138 (id=1216)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.2 Common mechanisms: interpretation, over-theorization, principled refusal

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:52:00Z

**Comment body:**

> Way too much text on this should be a shorter foot

**Anchored text:**

```
Note on judge panel. Every cell in this table is computed under the locked 5-judge primary panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). The per-system Aggregate Δ values match the scaffold values in docs/research/v11_emit/4_4_2_4_4_3.json to within rounding, and the per-row Wins / Losses / Large-improvement / Large-regression counts are computed from the same panel via scripts/_table_4_6_5judge_recompute.py. Earlier drafts of this table presented per-row counts under a 6-judge audit panel (5 primary + Gemini Flash) carried over from prior paired analyses; under the strict 5-judge primary, Aggregate Δs shrink by 0.01 to 0.06 across the 8 rows, no row’s sign flips, and the mixture pattern is invariant. The 5-judge primary aggregate help/hurt counts for Supermemory across all 13 globals are  [...]
```

**Status:** APPLIED  
**Resolution:** Pulled most of the Note on judge panel block into footnote [^table46-judge-panel]; main text retains the table caption.

---

## Comment 139 (id=1217)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.2 Common mechanisms: interpretation, over-theorization, principled refusal

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:53:00Z

**Comment body:**

> If these mechanisms are appearing I think Supermemories should be sitting under 4.4 .2 can start with super memory and then go into per subject paired delta distribution to look at everyone else. We end up reiterating the same patterns it seems. May want to shorten the Super memory examples potentially the way that it’s been done below in this section under examples.

**Anchored text:**

```
The three mechanisms from §4.4 reproduce across all five memory systems.
```

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 140 (id=1218)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.2 Common mechanisms: interpretation, over-theorization, principled refusal

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:54:00Z

**Comment body:**

> Bring super memory back up here should likely be collapsing the Super memory section in.1 here instead in 4.4.2. May be able to save some space depending thoughts?

**Anchored text:**

```
Supermemory
```

**Surrounding paragraph (full):**

> Supermemory (strong embedding retrieval, highest C1 mean ~2.65): more Pattern 2 and Pattern 3 because strong retrieval more often already supplies the plain answer, giving the specification more chances to over-theorize or refuse.

**Status:** pending review  
**Resolution:** _(to be filled in during review)_

---

## Comment 141 (id=1221)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.4.3 Case study: cross-system refusal on Keckley Q21

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:57:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
Raw data and scripts. Full per-subject per-system paired distributions at docs/research/supermemory_c1_vs_c3_paired_analysis.md, docs/research/mem0_letta_zep_c1_vs_c3_analysis.md, and docs/research/baselayer_c1_vs_c3_paired_analysis.md. Analysis scripts at scripts/analyze_mlz_c1_vs_c3.py, scripts/analyze_baselayer_c1_vs_c3.py, and scripts/analyze_sm_c1_vs_c3.py.
```

**Status:** APPLIED  
**Resolution:** Pulled §4.4.3 raw-data paragraph into footnote [^paired-c1c3-data].

---

## Comment 142 (id=1226)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:59:00Z

**Comment body:**

> Did we do any tests with stacking the spec on top of this as well, I guess we don’t need to because we already know what the letta identity block looks like. Should likely do a more in depth analysis on the difference between the two

**Anchored text:**

```
Headline result on the small sample tested (5-judge primary
```

**Surrounding paragraph (full):**

> Headline result on the small sample tested (5-judge primary). Letta’s self-edited memory block scores higher than Base Layer’s compressed-brief variant on all 3 subjects: Hamerton 3.10 vs. 2.96 (Δ +0.14), Ebers 2.76 vs. 1.72 (Δ +1.05), Babur 2.42 vs. 1.88 (Δ +0.54). A robustness rerun against Base Layer’s full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The gap widens at small corpora and narrows at Babur. Both representations land well above the retrieval-only baseline at matched response model.

**Status:** DEFERRED  
**Resolution:** Out of scope per orchestrator guidance: stack-spec-on-Letta-stateful is a separate analysis. Letta + spec-stacked is flagged in §7.5 already.

---

## Comment 143 (id=1229)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.6 Robustness and sensitivity

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:00:00Z

**Comment body:**

> Is it possible to move robustness and sensitivity were all sensitivity checks 2 Potentially the abstract can avoid clogging up the main report here.

**Anchored text:**

```
4.6 Robustness and sensitivity
```

**Status:** PENDING  
**Resolution:** Substantive - move §4.6 robustness/sensitivity to appendix entirely. Structural call. Pair with C144-C146.

---

## Comment 144 (id=1230)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.6 Robustness and sensitivity

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:00:00Z

**Comment body:**

> Maybe we make a mention of robustness and sensitivity checks around cross provider response generation Judge panel sensitivity and what these robustness checks do not add, can be found in the appendix at so and so with Hyperlink

**Anchored text:**

```
4.6 Robustness and sensitivity
```

**Status:** PENDING  
**Resolution:** Substantive - recommend short §4.6 mention plus appendix link. Pair with C143.

---

## Comment 145 (id=1235)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:01:00Z

**Comment body:**

> Yeah does this sensitivity check it seems to add this to the appendix instead of mentioning directly in line at section 4

**Anchored text:**

```
.6.2 Judge panel sensitivity (5-judge primary vs 7-judge)
```

**Surrounding paragraph (full):**

> 4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge)

**Status:** PENDING  
**Resolution:** Substantive - move §4.6.2 (judge panel sensitivity) to appendix. Pair with C143.

---

## Comment 146 (id=1238)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.6.3 What these robustness checks do not address

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:02:00Z

**Comment body:**

> Again this seems to make more sense in the appendix

**Anchored text:**

```
4.6.3 What these robustness checks do not address
```

**Status:** PENDING  
**Resolution:** Substantive - move §4.6.3 to appendix. Pair with C143.

---

## Comment 147 (id=1239)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 4. Results > 4.6.3 What these robustness checks do not address

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:02:00Z

**Comment body:**

> Should likely be in footnotes unless moved to the appendix with the rest of the sensitivity checks in tier two items

**Anchored text:**

```
Raw data and scripts. Tier 2 per-subject per-model responses at results/_tier2/global_<subject>/. 5-judge vs 7-judge sensitivity recompute at docs/research/recompute_5judge_primary.md. Tier 2 panel-completeness audit (including the 24 GPT-5.4 FULL_FAIL cells that drive the 4-judge effective panel in §4.6.1) at docs/research/v11_panel_completeness_audit.csv. Mechanical recompute and per-cell panel-range scripts at scripts/_v10_verification/tier2_mechanical_recompute.py and scripts/_v10_verification/tier2_panel_ranges.py.
```

**Status:** APPLIED  
**Resolution:** Pulled §4.6.3 raw-data paragraph into footnote [^tier2-raw-data].

---

## Comment 148 (id=1242)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:02:00Z

**Comment body:**

> 

**Anchored text:**

```
and included a post-hoc N=3 case study of Letta’s stateful-agent path (§4.5).
```

**Surrounding paragraph (full):**

> §4 established the gradient, the mechanism, and the additive composition with existing memory systems, and included a post-hoc N=3 case study of Letta’s stateful-agent path (§4.5). §5 turns to what those results imply beyond the specific experiment. Before developing the positive implications (§5.2 onward), §5.1 names a recurring failure mode that cuts across all five memory systems evaluated and motivates the paper’s positive target: the conflation of recall sufficiency with representational adequacy.

**Status:** NOTED-blank 2026-04-27 (anchor area also touched by C153 reframe propagation)  
**Resolution:** Comment body empty so no direct instruction. Anchor sits on the §5 intro reference to the Letta N=3 case study. The §5 intro line was rewritten in this walk as part of the C153 propagation pass (the §5 intro previously read "additive composition with existing memory systems," now reads "structured per-question interaction with existing memory systems") so the anchor area is now consistent with the broader §4.4 / §5.2 / §5.4 reframe. C148 resolved by side effect; no separate action required. If Aarik intended a different change on this anchor, it can be re-anchored on the v11 read-through.

---

## Comment 149 (id=1245)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.1 The Anti-Pattern: What Behavioral Specification Is Not

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:04:00Z

**Comment body:**

> Are we looking at a representation that lets a response model act as this specific person would or we want a representation that lets a response model act in alignment. Important clarification.

**Anchored text:**

```
We want a representation that lets a response model act as this specific person would,
```

**Surrounding paragraph (full):**

> The positive target is narrower than any of the above. We want a representation that lets a response model act as this specific person would, on situations the model has never seen, grounded in the person’s documented reasoning patterns rather than in surface-level similarity, psychometric dimensions, or preference signals. What follows (§5.2 through §5.6) develops what the study shows about this target and where it falls short.

**Status:** PENDING 2026-04-27 (judgment call surfaced for Aarik)  
**Resolution:** Positioning question, not a wording polish. The paper currently uses two phrasings: §1.1 hypothesis says "behavioral alignment with that person on novel situations" (post-B1 rewrite); §5.1 closing says "lets a response model act as this specific person would." Aarik's tag "Important clarification" suggests the mixed framing is the issue. Three coherent options to pick from: (a) "act as this specific person would" — narrowest, the agent simulates the person; (b) "act in alignment with this specific person" — softer, the agent operates within the person's interpretive frame without claiming to be them; (c) hybrid: "act in line with how this specific person would act" — keeps the behavioral target while removing the impersonation read. Recommendation: option (c) for §5.1 closing, with a single canonical phrase chosen and propagated to §1.1, §5.1, §5.2 in one pass after Aarik picks the phrase. No edit applied yet to avoid premature commitment; surfaced for read-through decision.

---

## Comment 150 (id=1248)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.2 What the study demonstrates

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:05:00Z

**Comment body:**

> Not necessarily for the people who actually use AI systems the working assumption is that everyone will be using AI systems So how do we improve human AI interactions for everyone. Maybe that’s too big of a statement, feedback?

**Anchored text:**

```
who actually use AI systems?
```

**Surrounding paragraph (full):**

> This paper is oriented to a single question: how do we improve human-AI interactions for the people who actually use AI systems? We introduced representational accuracy as the measurable AI-side property that makes those interactions possible: how faithfully an AI’s internal model of a specific person captures how that person reasons. We tested it by measuring behavioral prediction on held-out text, checking whether the response model could anticipate how each subject would respond in situations drawn from passages the model had never seen, using a specification authored from the other half of the corpus.

**Status:** APPLIED 2026-04-27  
**Resolution:** §5.2 opening rewritten to mirror the §1.4 v2 framing ("anyone who uses an AI system") and to make explicit the working assumption that AI is becoming general-purpose infrastructure, not specialist tooling. Phrasing: "how do we improve human-AI interactions for anyone who uses an AI system? AI is now broad-base infrastructure, comparable to email or mobile phones in how widely it touches daily decisions, so the population of relevance is the general user base rather than a specialist niche. Almost none of those users have had their reasoning indexed by any training corpus (§1.4)." Coordinated with C154 / C155 so §5.3 echoes the same population framing without duplication.

---

## Comment 151 (id=1249)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.2 What the study demonstrates

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:06:00Z

**Comment body:**

> Would be prefer this to be footnote. May want an extended explanation in addition to the title of this bullet point similar to what is done for the next one

**Anchored text:**

```
(the gradient, H1 + H2; §4.1). Regression slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, slope p < 0.001. On the nine low-baseline subjects , every subject improved, mean Δ_C4a = +0.89 points.
```

**Surrounding paragraph (full):**

> A compact Behavioral Specification improves prediction, inversely proportional to what the model already knows about the person (the gradient, H1 + H2; §4.1). Regression slope −0.96 [95% CI −1.24, −0.67], R² = 0.82, slope p < 0.001. On the nine low-baseline subjects , every subject improved, mean Δ_C4a = +0.89 points.

**Status:** APPLIED 2026-04-27  
**Resolution:** Two parts addressed. First, the regression statistics (slope, CI, R², p-value) pulled to a new footnote `[^discussion-gradient-stats]`, leaving the bullet header clean. Second, an extended layman explanation appended after the bullet's headline numbers, parallel in shape to the H3 bullet's two-sentence elaboration: "Read in plain language: the less the model already knew about the person, the more the specification helped, in a tight one-to-one trade across the 14 subjects. The effect is largest exactly where it has to be largest for the deployment claim to hold, which is on subjects the model has nothing to start from." Final structure mirrors the H3 / H4 bullet pattern Aarik referenced.

---

## Comment 152 (id=1250)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.2 What the study demonstrates

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:06:00Z

**Comment body:**

> Since this is the discussion may want to avoid the use of derangement Keep it layman

**Resolution applied 2026-04-27 (APPLIED):** "Derangement" replaced with layman wording in §5.2 H3 bullet ("a fixed-derangement pairing maximizing cultural and temporal distance" became "pairing each subject with a culturally and temporally distant other person's specification by design"; "Random-derangement wrong-spec is a softer probe" became "The softer wrong-spec probe (each subject swapped at random with another subject's specification)"). Also propagated to §5.4 H3 paragraph (Random derangement → Random swap; Adversarial fixed derangement → Adversarial fixed swap). The technical terminology remains in §3.5 (formal condition definitions) and §4.3 (results); only §5 was rewritten in layman terms per Aarik's discussion-section direction.

**Anchored text:**

```
The load-bearing evidence is the adversarial wrong-spec: a fixed-derangement pairing maximizing cultural and temporal distance degrades prediction below the no-context baseline (Δ −0.25). Random-derangement wrong-spec is a softer probe, scoring near baseline (Δ +0.15 vs. +0.35 for the correct spec, a 0.20-point gap). Together the two controls bracket the question: structured prompting alone does not produce the effect, and sufficiently mismatched content actively hurts.
```

**Surrounding paragraph (full):**

> The improvement is content-specific (H3; §4.3). The load-bearing evidence is the adversarial wrong-spec: a fixed-derangement pairing maximizing cultural and temporal distance degrades prediction below the no-context baseline (Δ −0.25). Random-derangement wrong-spec is a softer probe, scoring near baseline (Δ +0.15 vs. +0.35 for the correct spec, a 0.20-point gap). Together the two controls bracket the question: structured prompting alone does not produce the effect, and sufficiently mismatched content actively hurts.

**Status:** APPLIED 2026-04-27 (confirmed during §5-§7 walk)  
**Resolution:** Confirmed in v11 §5.2 H3 bullet (line 1403): layman wording 'pairing each subject with a culturally and temporally distant other person’s specification by design' and 'each subject swapped at random with another subject’s specification' already in place; 'derangement' no longer appears in §5.2. Also confirmed §5.4 line 1433 uses 'Random swap' / 'Adversarial fixed swap' in layman form. Technical 'derangement' terminology preserved only in §3.5 (formal condition definitions) and §4.3 (results). C152 closed.

---

## Comment 153 (id=1251)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.2 What the study demonstrates

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:07:00Z

**Comment body:**

> Not sure if the point is that the specification composes additively considering that the absolute values are relatively small, what’s more interesting are the ranges Across questions when adding the spec and when letting the memory systems operate on their own. There are certain questions where it’s very obvious the spec is helping and others where it’s hurting. I don’t think it’s about saying that the is additive to all the memory systems More so that it can improve specific types of questions that memory systems or systems based on recall are not equipped to handle. This may need to be something that’s throughout the messaging the introduction results and discussionIMPORATNT**

**Resolution applied 2026-04-27 (RESOLVED prior to this run):** Already addressed by today's §4.4 / §5.2 / §5.4 reframe from "additivity" to "interaction with retrieval that depends on question type." §5.2 H4 bullet now leads with "The specification interacts with memory-system retrieval in a structured way that depends on question type" rather than "composes additively." §5.4 introduces the three patterns (Pattern 1 pattern supply, Pattern 2 over-theorization, Pattern 3 structural refusal) and frames aggregate Δ as the per-question balance rather than a uniform property. §1.3 Mechanism block now carries the same three-pattern framing. The cross-cutting reframe Aarik called for is in place in §1, §4, and §5. No additional edit needed in this run.

**Anchored text:**

```
The specification composes additively with existing memory systems
```

**Surrounding paragraph (full):**

> The specification composes additively with existing memory systems (H4; §4.4). Layered on top of the four commercial memory systems tested, the specification produces positive mean Δ on three of four (Mem0, Letta archival, Zep), but the strength of the additive effect is uneven across systems: Zep (controlled and native) and Mem0-native carry the strongest evidence; Mem0-controlled is small and not statistically distinguishable from zero on its own; Letta archival is positive in controlled but near-null in native; Supermemory aggregates near zero overall with the per-question analysis (§4.4.2, §4.4.3) showing a mixture of large improvements and large regressions that partly cancel rather than a uniform null.

**Status:** RESOLVED 2026-04-27 (prior pass; confirmed during §5-§7 walk)  
**Resolution:** Already addressed by today's §4.4 / §5.2 / §5.4 reframe from "additivity" to "interaction with retrieval that depends on question type." §5.2 H4 bullet (line 1405) now leads with "The specification interacts with memory-system retrieval in a structured way that depends on question type"; §5.4 introduces the three patterns (Pattern 1 pattern supply, Pattern 2 over-theorization, Pattern 3 structural refusal) as the load-bearing reading; §1.3 carries the same three-pattern framing. Additional fix during this walk: §5 intro line 1373 was rewritten from "additive composition with existing memory systems" to "structured per-question interaction with existing memory systems" so the section's opening sentence matches the body reframe. C153 closed.

---

## Comment 154 (id=1254)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.3 The population of relevance

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:10:00Z

**Comment body:**

> We need to update this in relation to an earlier comment and these improvements being for everyone assuming that everyone’s on AI.

**Resolution applied 2026-04-27 (APPLIED):** §5.3 lede rewritten to mirror the §1.4 v2 / §5.2 framing. New phrasing: "The research question is how to improve human-AI interactions for anyone who uses an AI system. The working assumption is the same one §1.4 stated: AI is becoming general-purpose infrastructure, so the population of relevance is the general user base, not a specialist niche." Closing sentence of the same paragraph extended to make the bridge to the low-baseline structural argument explicit: "The target population is living users whose private reasoning patterns are not in any training corpus, and the structural argument below is that those users sit in the low-baseline band by construction." Coordinated with C150 / C155 so all three population-framing edits land in one consistent shape across §5.2, §5.3 lede, and §5.3 low-baseline paragraph.

**Anchored text:**

```
who use AI systems.
```

**Surrounding paragraph (full):**

> This paper is not a retrospective study of historical figures. The research question is how to improve human-AI interactions for the people who use AI systems. The 14 historical subjects in the main study are experimental proxies, chosen because they enable cross-subject comparison with verifiable ground truth (the held-out half of their own autobiographies). They are not the target population. The target population is living users whose private reasoning patterns are not in any training corpus.

**Status:** APPLIED 2026-04-27 (confirmed in v11 §5.3 lede line 1417)  
**Resolution:** §5.3 lede mirrors the §1.4 v2 / §5.2 framing: "The research question is how to improve human-AI interactions for anyone who uses an AI system. The working assumption is the same one §1.4 stated: AI is becoming general-purpose infrastructure, so the population of relevance is the general user base, not a specialist niche." Closing sentence of the same paragraph: "the structural argument below is that those users sit in the low-baseline band by construction." Coordinated with C150 / C155. C154 closed.

---

## Comment 155 (id=1255)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.3 The population of relevance

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:11:00Z

**Comment body:**

> Generally need to be more clear with a population of relevance I think think it’s lost in the introduction as well as the results in terms of the importance of this low baseline band

**Resolution applied 2026-04-27 (APPLIED):** §5.3 "low-baseline slice" paragraph rewritten to make explicit that this band is the result that should travel with the paper, not the cross-subject mean. New phrasing: "The low-baseline slice is the study's closest proxy for real users, and it is where the headline effect lives. ... This band, not the cross-subject mean, is the result that should travel with the paper. Living users sit deeper into this band than any of our subjects, because the autobiographers were specifically chosen as people whose work is in pretraining and who therefore should be best-known to the model; even on those favorable cases, baseline pretraining alone does not reach a usable score on the 1-5 rubric." Introduction-side framing was already strengthened in v11 via §1.3 v5 (gradient + category-shift) and §1.4 v2 ("anyone who uses an AI system"); §5.3 now mirrors that emphasis explicitly. The paper still has not been pushed harder in §4 (results) on the low-baseline reading; flagged as a candidate §4.1 readout-emphasis edit if Aarik wants the band-first reading carried into the results narrative as well.

**Anchored text:**

```
. If the population of relevance for AI personalization is everyone who uses AI, and every such user sits in the low-baseline band because
```

**Surrounding paragraph (full):**

> The infrastructure implication. If the population of relevance for AI personalization is everyone who uses AI, and every such user sits in the low-baseline band because their private reasoning is structurally absent from training data, then representational accuracy is not an enhancement for edge cases. It is a structural requirement for personalization at all. Either each user supplies their own representation to the AI systems that serve them, or personalization remains surface-level: style, voice, preference, not how the person reasons. The Behavioral Specification is one implementation of user-supplied representation. An exploratory Letta test (§4.5, N=3 subjects, post-hoc) is consistent with non-retrieval representation-production mechanisms also reaching the target, pending the multi-subject replication flagged in §7.5. Some implementation of user-held, user-inspectable, user-modifiable representation is a prerequisite for AI that can act on behalf of a specific person rather than on behalf of a population aggregate.

**Status:** APPLIED 2026-04-27 (§5.3 low-baseline paragraph line 1421); JUDGMENT-CALL flagged for Aarik on §4 readout-emphasis  
**Resolution:** §5.3 low-baseline slice paragraph already strengthened in v11 to lead with "The low-baseline slice is the study's closest proxy for real users, and it is where the headline effect lives" and to close with "This band, not the cross-subject mean, is the result that should travel with the paper." Introduction-side framing strengthened in §1.3 v5 + §1.4 v2. C155 partially closed; one remaining decision surfaced for Aarik: whether to push the low-baseline-band-first reading harder into the §4.1 results narrative as well (currently the cross-subject mean is the headline read in §4; the band reading lives in §5.3). Recommendation: add a one-paragraph readout-emphasis insert at the end of §4.1 stating that the band, not the mean, is what the paper takes forward, with a forward pointer to §5.3. Not applied in this run because it is a substantive results-section rewrite, not a wording polish; awaiting Aarik's call.

---

## Comment 156 (id=1258)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.4 Content specificity and mechanism

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:12:00Z

**Comment body:**

> Like that these patterns are here, this harkins back to feedback on the supermemory section within the results section for that being collapsed with the other memory providers instead of giving super memory its own section and then doing the same thing or mentioning the same patterns again right after it.IMPORTANT

**Resolution 2026-04-27 (SUBSUMED):** Already addressed by the v10 → v11 §4.4 restructure (C139 / C140 collapse). Supermemory's standalone §4.4.3 was folded into the cross-system Pattern 1 / Pattern 2 / Pattern 3 framing in §4.4.2, and §5.4's three-pattern bullet block now references the cross-system per-question evidence rather than a Supermemory-specific section. The patterns Aarik liked here are stated cross-system in both §4.4.2 (results) and §5.4 (discussion). No additional edit applied in this run.

**Anchored text:**

```
Pattern 1, pattern supply. When retrieval returns biographical facts but not the interpretive pattern for how the subject processes them, the specification supplies the pattern. This is what produces the large-magnitude improvements on low-baseline subjects (§4.1 Example A, §4.3 Example 1, §4.4 Supermemory Example 1). Pattern 1 drives most positive per-question swings.Pattern 2, over-theorization. When retrieval already returns the plain answer and the ground truth is a surface-level statement, the specification shifts the response toward interpretive depth the question does not require (§4.4 Supermemory Example 2, §4.4.2 Yung Wing Q31). Pattern 2 drives most negative per-question swings on literal-recall questions.Pattern 3, structural refusal. When retrieved facts do not cover the interi [...]
```

**Surrounding paragraph (full):**

> Pattern 1, pattern supply. When retrieval returns biographical facts but not the interpretive pattern for how the subject processes them, the specification supplies the pattern. This is what produces the large-magnitude improvements on low-baseline subjects (§4.1 Example A, §4.3 Example 1, §4.4 Supermemory Example 1). Pattern 1 drives most positive per-question swings.

**Status:** SUBSUMED 2026-04-27 (by C139 / C140 collapse + today's C153 reframe)  
**Resolution:** Confirmed during walk. Supermemory's standalone §4.4.3 was folded into the cross-system Pattern 1 / Pattern 2 / Pattern 3 framing in §4.4.2 in the v10 -> v11 restructure. §5.4 three-pattern bullet block at lines 1437-1439 references the cross-system per-question evidence rather than a Supermemory-specific section; §4.4.2 carries the cross-system Pattern 1/2/3 framing. C156 closed.

---

## Comment 157 (id=1259)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 5. Discussion > 5.4 Content specificity and mechanism

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:14:00Z

**Comment body:**

> This generally needs to be shortened

**Resolution applied 2026-04-27 (APPLIED, C157):** Keckley Q21 paragraph in §5.4 cut from two paragraphs (~360 words) to one paragraph (~150 words). Removed the procedural restatement of how the question works and the three-layer "specification / retrieval / rubric" gloss; kept the Supermemory and Base Layer −2.33 penalty data point, the Letta archival reversal, and the one-sentence reading that locates the refusal at the specification layer. Tighter reading of the same finding without losing any quantitative detail.

**Anchored text:**

```
The Keckley Q21 result: one question where every memory system produced the same spec-induced refusal. Keckley Q21 asks how Elizabeth Keckley explains her decision not to visit her mother’s grave despite having the opportunity. The answer turns on Keckley’s interior motive, which only appears in the held-out half of the corpus. No retrieval system can surface it because it is not in any retrievable fact pool. On all five memory systems tested, when the specification was added on top of retrieval, the response model declined to speculate about Keckley’s interior motive, citing the specification’s dignity and epistemic-honesty axioms. On the two systems where retrieval alone had produced a productive speculation (Supermemory C1 = 3.83, Base Layer C1 = 3.33), the specification-added response  [...]
```

**Surrounding paragraph (full):**

> The Keckley Q21 result: one question where every memory system produced the same spec-induced refusal. Keckley Q21 asks how Elizabeth Keckley explains her decision not to visit her mother’s grave despite having the opportunity. The answer turns on Keckley’s interior motive, which only appears in the held-out half of the corpus. No retrieval system can surface it because it is not in any retrievable fact pool. On all five memory systems tested, when the specification was added on top of retrieval, the response model declined to speculate about Keckley’s interior motive, citing the specification’s dignity and epistemic-honesty axioms. On the two systems where retrieval alone had produced a productive speculation (Supermemory C1 = 3.83, Base Layer C1 = 3.33), the specification-added response received an identical −2.33-point penalty from the content-match rubric. On the systems where retrieval alone had already hedged, the penalty was smaller. On the one system where retrieval alone had also refused (Letta archival), the specification’s structured refusal scored higher than the unstructured retrieval-only refusal.

**Status:** APPLIED 2026-04-27 (confirmed during walk)  
**Resolution:** Keckley Q21 paragraph in §5.4 (line 1447) cut from two paragraphs to a single tight paragraph (~150 words). Procedural restatement and three-layer "specification / retrieval / rubric" gloss removed; Supermemory and Base Layer -2.33 penalty data point retained, Letta archival reversal retained, one-sentence reading at the end locating the refusal at the specification layer retained. C157 closed.

---

## Comment 158 (id=1272) — APPLIED 2026-04-27

**Resolution:** Data-path block at the end of §6.3 "Scope and caveats of the variance probe" pulled to a new footnote `[^variance-data-paths]`. The body paragraph now ends cleanly on the §4.1 slope/R² acceptance sentence; the file-path detail (per-rerun specs, judgments, full report, reproducibility scripts) lives in the footnote. Aarik's "Footnote" instruction applied.



**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 6. Limitations > 6.3 Pipeline and specification stability

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:19:00Z

**Comment body:**

> Footnote

**Anchored text:**

```
data/global_<subject>/_variance_runs/run_<N>/ and results/global_<subject>/_variance_runs/run_<N>_*.json; full report and reproducibility scripts at docs/research/v10_pipeline_variance_analysis.md, scripts/_v10_pipeline_variance.py, and scripts/_v10_pipeline_variance_report.py.
```

**Surrounding paragraph (full):**

> Scope and caveats of the variance probe. The probe covers the lighter-scope variance only: the Sonnet authoring step plus the Opus compose step. Extraction-stage non-determinism is held constant by reusing each subject’s pre-populated SQLite and ChromaDB state across reruns; including extraction would likely add additional variance at the front of the pipeline. The probe covers low-baseline and mid-baseline subjects but does not reach the Franklin-style high-baseline tail (C5 = 3.77), so the H2a interference claim is not directly stress-tested by this run. With n = 3 reruns per subject the per-subject SD point estimates carry their own wide 95% confidence intervals (roughly [0.5×, 6×] of the value); the pooled three-subject estimate is more stable than any single per-subject estimate but should still be read as an order-of-magnitude indicator rather than a precision number. With those caveats stated, the run-to-run SD is small enough relative to the cross-subject SD that we accept the §4.1 slope and R² as findings about the gradient rather than artifacts of a single specification authoring. Per-rerun specs and judgments are at data/global_<subject>/_variance_runs/run_<N>/ and resul [...]

**Status:** APPLIED 2026-04-27 (confirmed during walk; data-paths now in footnote `[^variance-data-paths]` at v11 line 1641)  
**Resolution:** Data-path block at the end of §6.3 "Scope and caveats of the variance probe" pulled to footnote `[^variance-data-paths]`. The body paragraph ends cleanly on the §4.1 slope/R² acceptance sentence; per-rerun spec paths, results paths, and reproducibility-script paths live in the footnote. Aarik's "Footnote" instruction applied. C158 closed.

---

## Comment 159 (id=1285)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 7. Future Work > 7.4 Production serving and infrastructure

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:27:00Z

**Comment body:**

> Seems like future work and practical implications are overlapping perhaps a bit too much

**Resolution 2026-04-27 (PENDING — judgment call surfaced for Aarik):** Aarik is correct that §5.5 "Practical implications" and §7.4 "Production serving and infrastructure" overlap. The current split is: §5.5 explains what production deployment of the spec would look like (context budget, modifiability, dynamic activation, temporality, topic decomposition), §7.4 catalogs the same five items as future research questions ("dynamic activation, modifiability affordances, temporality handling, canonical life events, topic decomposition"). The overlap is structural rather than redundant — §5.5 is what we believe deployment will look like, §7.4 is which of those beliefs need empirical verification — but the reader sees the same five items twice in adjacent sections. Three options for resolving: (a) keep both, add a one-line cross-reference at top of §7.4 ("§5.5 develops the production-deployment proposal; §7.4 catalogs the empirical questions that proposal raises") so the role split is explicit; (b) collapse §7.4 into §5.5 and drop §7.4 entirely, treating production-serving questions as practical implications rather than future work; (c) collapse §5.5's open-question content into §7.4 and tighten §5.5 to context budget, authoring cost, per-query cost, modifiability, calibration framing only. Recommendation: (a) — the §5 / §7 split is genuine (deployment proposal vs. research agenda) and labeling the split is cheaper than restructuring. No edit applied yet; awaiting Aarik's call.

**Anchored text:**

```
7.4 Production serving and infrastructure
```

**Status:** PENDING 2026-04-27 (judgment call surfaced for Aarik)  
**Resolution:** Aarik is correct that §5.5 "Practical implications" and §7.4 "Production serving and infrastructure" overlap. Current split: §5.5 explains what production deployment of the spec would look like (context budget, modifiability, dynamic activation, temporality, topic decomposition); §7.4 catalogs the same five items as future research questions ("dynamic activation, modifiability affordances, temporality handling, canonical life events, topic decomposition"). The overlap is structural rather than redundant: §5.5 is what we believe deployment will look like, §7.4 is which of those beliefs need empirical verification, but the reader sees the same five items twice in adjacent sections. Three options: (a) keep both, add a one-line cross-reference at top of §7.4 ("§5.5 develops the production-deployment proposal; §7.4 catalogs the empirical questions that proposal raises") so the role split is explicit; (b) collapse §7.4 into §5.5 and drop §7.4, treating production-serving questions as practical implications rather than future work; (c) collapse §5.5's open-question content into §7.4 and tighten §5.5 to context budget, authoring cost, per-query cost, modifiability, calibration framing only. Recommendation: (a). The §5 / §7 split is genuine (deployment proposal vs. research agenda) and labeling the split is cheaper than restructuring. No edit applied yet; awaiting Aarik's call.

---

## Comment 160 (id=1294)

**Section:** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization > 9. References

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T16:29:00Z

**Comment body:**

> May want to add a potential definitions section

**Resolution 2026-04-27 (SUBSUMED):** Already addressed by Bavani item B8 in this same review pass: Appendix G "Glossary" was added to the v11 paper (line 25 of §1.1 carries an explicit forward reference: "Defined terms used throughout the paper are collected in Appendix G for reference."). The glossary holds canonical definitions for representational accuracy, interpretation, behavioral specification, baseline, low-baseline band, and the technical terminology used through §3-§5. C160 is closed by B8; no additional edit applied.

**Anchored text:**

```
9. References
```

**Status:** SUBSUMED 2026-04-27 (by Bavani item B8)  
**Resolution:** Already addressed by Bavani item B8: Appendix G "Glossary" was added to v11. §1.1 (line 25) carries an explicit forward reference: "Defined terms used throughout the paper are collected in Appendix G for reference." The glossary holds canonical definitions for representational accuracy, interpretation, behavioral specification, baseline, low-baseline band, and the technical terminology used through §3-§5. C160 closed by B8.

---

## Comment 161 (id=0)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T11:46:00Z

**Comment body:**

> Need to clean up section 4 sub headers--- In general need to follow standard ocnventions for table of contents

**Resolution 2026-04-27 (TRACKED under M1):** Not anchored to specific text. Tracked under M1 "ToC / section-title cleanup" at the top of the comments file. §4 currently has six top-level subsections (§4.1 The cross-subject gradient, §4.2 Compression, §4.3 Mechanism, §4.4 Memory-system composition, §4.5 Letta exploratory case study, §4.6 Robustness and sensitivity, §4.7 Summary) plus several §4.x.y sub-subsections. The §4.6.x sub-subsections in particular are inconsistent in heading style. Suggested standardization for the docx pass: bring all §4.x subsection headers to a noun-phrase pattern, all §4.x.y sub-subsections to short title-case noun phrases. Will execute as part of the docx-formatting pass after Aarik's read-through.

**Anchored text:**

```

```

**Status:** TRACKED 2026-04-27 (M1 ToC pass)  
**Resolution:** See 2026-04-27 resolution block above. Meta-level, no inline edit applicable.

---

## Comment 162 (id=22)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T12:22:00Z

**Comment body:**

> Like can put in footnotes

**Anchored text:**

```

```

**Status:** RESOLVED 2026-04-27 (applied to v11)  
**Resolution:** §1.2 conditions table C2c row long parenthetical (deterministic fixed pairing / mapping in run_global_rerun.py / v2 random derangement / Hamerton-Franklin variant) pulled to footnote `[^c2c-construction]`. Triangulated docx anchor by reading word/document.xml directly: confirmed C162 anchored to the C2c row of the §1.2 conditions table. Cell now reads cleanly with the dense construction detail in the footnote.

---

## Comment 163 (id=85)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:07:00Z

**Comment body:**

> These numbers are not in line

**Resolution 2026-04-27 (DEFERRED to docx pass):** Empty anchor; instruction is visual ("not in line"). 13:07 timestamp clusters with the §2.2 Mem0 / Letta / Supermemory / Zep recall-score parenthetical block (C164 at 13:04 hits the same cluster explicitly). Likely refers to the published-recall-score numbers in Table 2.1 sitting at inconsistent indentation or table-cell alignment in the rendered docx. Visual / Word-formatting issue, not a markdown-source change. Will be handled in the docx polish pass after Aarik's body read-through.

**Anchored text:**

```

```

**Status:** DEFERRED 2026-04-27 (docx polish pass)  
**Resolution:** See above. Docx visual-alignment issue, not a markdown-source edit.

---

## Comment 164 (id=86)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:04:00Z

**Comment body:**

> This is way too long for the draw it in the footnotes If it’s extending this far. Vendor reported should be below Peer reviewable papers should be below Those should be footnotes they should not be parenthetical

**Resolution 2026-04-27 (DEFERRED to B3 — Table 2.1 simplification):** Anchor is empty but content is unambiguous: the §2.2 Mem0 row in Table 2.1 has a long parenthetical mixing vendor-reported scores with peer-reviewable paper citations. Aarik's instruction: vendor-reported should be a footnote, peer-reviewable papers should be a footnote, neither should sit in the table cell as a parenthetical. Bavani item B3 already deferred Table 2.1 simplification to Aarik handling separately; this comment is the docx-anchored version of the same fix. Bundled: when Aarik does the Table 2.1 pass, vendor-reported scores and peer-reviewable references should be pulled to footnotes leaving only the headline number in the cell.

**Anchored text:**

```

```

**Status:** DEFERRED 2026-04-27 (bundled with B3)  
**Resolution:** See above. Bundled with Bavani item B3 Table 2.1 simplification pass.

---

## Comment 165 (id=91)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:04:00Z

**Comment body:**

> This is sloppy. Text size and font selection are off This needs to be layman terms not putting specific functions.

**Resolution 2026-04-27 (DEFERRED to docx pass + B3):** Two parts. First, "text size and font selection are off" is a docx-rendering issue, not a markdown-source issue. Second, "needs to be layman terms not putting specific functions" likely refers to the §2.2 Letta row in Table 2.1, which currently lists Letta tool names verbatim (`archival_memory_search`, `core_memory_append`, `core_memory_replace`). Aarik's preference is to drop the function-name strings from the table cell and describe what they do in plain language. Function names already appear in the §2.2 architectural-distinction paragraph; the table cell can read "Archival semantic search; main-context memory blocks the agent edits during inference" without the verbatim function names. Bundled with B3 Table 2.1 simplification pass so all Table 2.1 edits land together.

**Anchored text:**

```

```

**Status:** DEFERRED 2026-04-27 (docx pass + bundled with B3)  
**Resolution:** See above.

---

## Comment 166 (id=94)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:04:00Z

**Comment body:**

> Again this should be a footnote not a parenthetical

**Resolution 2026-04-27 (PENDING best-guess; bundled with C164 / B3):** Empty anchor. 13:04 timestamp clusters with C164 / C165 on Table 2.1, so most likely refers to one of the other Table 2.1 row parentheticals (Supermemory's "self-reported" parenthetical or Zep's Rasmussen et al. arXiv parenthetical). All three rows have the same structure issue Aarik flagged in C164. Fix: pull vendor-source and arXiv-citation strings to footnotes for the whole table, not just the Mem0 row. Bundled with C164 / B3 in the Table 2.1 simplification pass. If Aarik intended a different anchor, please flag.

**Anchored text:**

```

```

**Status:** PENDING 2026-04-27 (best-guess anchor; bundled with C164 / B3)  
**Resolution:** See above. Surfaced for Aarik to confirm anchor on read-through.

---

## Comment 167 (id=107)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:10:00Z

**Comment body:**

> This should be footnote

**Resolution 2026-04-27 (PENDING best-guess; bundled with C164 / C166 / B3):** Empty anchor. 13:10 timestamp sits between the §2.2 Table 2.1 cluster (13:04) and the §2.3 Traceability section. Best guess: the §2.2 paragraph after Table 2.1 ("A note on benchmark scores in this field") carries inline parenthetical-style citations ("getzep/zep-papers#5", "Vectorize.io") that Aarik may want pulled to footnotes; alternatively the §2.3 Traceability paragraph references provider-specific behaviors inline that could be footnoted. Bundled with C164 / C166 / B3. If Aarik intended a different anchor, please flag.

**Anchored text:**

```

```

**Status:** PENDING 2026-04-27 (best-guess anchor; bundled with C164 / C166 / B3)  
**Resolution:** See above.

---

## Comment 168 (id=133)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:23:00Z

**Comment body:**

> Did some small formatting for this minim subject number cell size.

**Resolution 2026-04-27 (NOTED):** Aarik's own note documenting a docx formatting tweak he made (subject-number cell width adjustment in the §3.2 subject table). Not an instruction to the agent; logging for the docx pass so the cell width is preserved when the markdown source is re-converted to docx.

**Anchored text:**

```

```

**Status:** NOTED 2026-04-27 (Aarik's own annotation)  
**Resolution:** See above. No action required.

---

## Comment 169 (id=211)

**Section:** (top of document)

**Author:** Aarik Gulaya  
**Date:** 2026-04-27T13:27:00Z

**Comment body:**

> Again we’re bringing score up but have not made it clear what the scoring is.

**Resolution 2026-04-27 (SUBSUMED by today's §3.7 reorder + Agent A's §3.2 forward-pointer):** 13:27 timestamp clusters around §3.2 / §3.2.1, which introduces pretraining-coverage baselines (C5 scores). Today's §3.7 reorder placed Fractional score interpretation immediately after the rubric definition (now at §3.7.2 directly under §3.7's main rubric introduction). Agent A's §3.2 / §3.2.1 forward-pointer addition routes a reader who hits the C5 baseline numbers in §3.2.1 to the §3.7 rubric definition. Together these two changes resolve the substantive concern Aarik raised. C169 closed.

**Anchored text:**

```

```

**Status:** SUBSUMED 2026-04-27 (by §3.7 reorder + §3.2 forward-pointer)  
**Resolution:** See above.

---

## Comment 170 (id=351)

**Section:** (top of document)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T14:20:00Z

**Comment body:**

> Should be declarative statements on what it measures, no questions

**Resolution 2026-04-27 (SUBSUMED by Bavani item B5):** Already addressed by Bavani item B5 (§2.3.1 four subsection headers rewritten from "what xyz does and doesn't xyz" question form to declarative statements). 14:20 timestamp aligns with the §2.3 / §2.3.1 area where B5 made the rewrite. C170 closed by B5.

**Anchored text:**

```

```

**Status:** SUBSUMED 2026-04-27 (by Bavani item B5)  
**Resolution:** See above.

---

## Comment 171 (id=657)

**Section:** (top of document)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:02:00Z

**Comment body:**

> I assume this try would be color coded as well at least in terms of highest score per column?> htoughts?

**Resolution 2026-04-27 (DEFERRED to docx pass):** Color-coding request on a results table. 15:02 timestamp clusters around §4.1 / §4.4 results tables. Markdown source cannot encode cell-level color; docx conversion does. Tracked for the docx polish pass. Standard convention: highest score per column shaded green, lowest red, intermediate values gradient (or simpler: bold the highest, italicize the lowest). Will execute on the docx pass after Aarik's body read-through, alongside C173.

**Anchored text:**

```

```

**Status:** DEFERRED 2026-04-27 (figure regen workstream)  
**Resolution:** Aarik asks whether top-of-document table will be color-coded by highest score per column. The anchored text is empty (he attached the comment at the document top, no specific table cited). Most likely refers to one of the cross-condition aggregate tables (e.g. the §4.1 per-subject table, the §4.2 condition-mean table, or the §4.4 memory-system aggregate table). Color-coding (highest-per-column) is a docx-pass formatting concern, not a markdown caption rewrite. Queued for the docx-pass workstream alongside C91 and C173. Recommendation: highest-per-column tinting on the §4.1 per-subject results table (C5/C2a/C4/C8/C4a columns), the §4.2 condition-mean table (per Aarik's C102 comment), and the §4.4.1 per-system aggregate table (Δ_spec column).

---

## Comment 172 (id=913)

**Section:** (top of document)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:41:00Z

**Comment body:**

> 

**Anchored text:**

```

```

**Status:** NOTED-blank 2026-04-27  
**Resolution:** Comment body empty and anchor empty. 15:41 timestamp falls between C171 (15:02, color-coding question on a results table) and C173 (15:52, color-coding question). Likely a duplicate placeholder annotation in the same cluster as C171 / C173 with no body content. No action available without an anchor or body. If Aarik intended a specific change here, it can be re-anchored on the v11 read-through.

---

## Comment 173 (id=938)

**Section:** (top of document)

**Author:** Aarik Gulaya [2]  
**Date:** 2026-04-27T15:52:00Z

**Comment body:**

> I assume this will be color coded as well

**Anchored text:**

```

```

**Status:** DEFERRED 2026-04-27 (figure regen workstream)  
**Resolution:** Aarik asks whether table will be color-coded. Anchored text empty; comment attached at document top. Same scope as C91 and C171; queued for the docx-pass workstream. Recommendation: apply highest-per-column tinting on the same set of cross-condition aggregate tables flagged in the C171 resolution.

---

