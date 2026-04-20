# Aarik's Paper Review — S110 (2026-04-14)

80 comments extracted from Word doc. Organized by section with action items.

## Overall Reaction
"Overall really good, really happy with it."

---

## ABSTRACT / INTRODUCTION (C2-C17)

**C2 — Thesis placement:** "Fine with moving this up to the first paragraph, but not sure how to integrate it with the memory integration"
- ACTION: Restructure intro paragraph to lead with thesis, then ground in memory systems context

**C4 — Behavioral models framing:** "Like the idea of bringing up memory systems and preference models. Would think to mention behavioral models here. Not sure if we should be that upfront in the introduction"
- ACTION: Discuss — how early do we introduce "behavioral specification" as a concept?

**C5 — Recall examples:** "Maybe give 2-3 examples of recall test questions"
- ACTION: Add concrete examples of what recall benchmarks test

**C6 — Floating comment:** "This comment is randomly dropped in here, no context given"
- ACTION: Identify which text this refers to, fix or remove

**C7 — Scaling examples:** "This is quite a heavy comparison, may want to scale how advanced the examples are. 'Classified environment as hostile or generative' is heavy wording, start with simple example, move to more complex"
- ACTION: Reorder examples from simple to complex

**C9 — Core proposition:** "Not sure if this is what we are proposing. We are really proposing that in order to have aligned AI memory and actions, AI requires a representation of how its user thinks."
- ACTION: CRITICAL FRAMING — Aarik's restatement is cleaner than what's in the paper. Use this.

**C10 — Inspectable claim:** "Based on inspectable and structured pattern extraction that is shown to be durable over time?"
- ACTION: Clarify what makes the spec inspectable

**C11 — Integration:** "Feel like this is being thrown in, need to be integrated"
- ACTION: Better transitions

**C12 — Source clarity:** "Confusing, need to specify we are using autobiographies for this specifically"
- ACTION: State upfront: source text = public domain autobiographies

**C13 — Cross-references:** "Should probably link or mention which section goes over how the specification is generated"
- ACTION: Add section references throughout

**C14 — SOTA qualifier:** "Four state of the art COMMERCIAL memory systems"
- ACTION: Add "commercial"

**C15 — SOTA usage:** "First time using SOTA following the abstract"
- ACTION: Define on first use in main body

**C16 — Overlap metric:** "This is misleading, if this top 1, top 3, top 5, what?"
- ACTION: Specify which overlap metric (top-1 = 68%, already in abstract but needs clarity)

**C17 — Disjointed sentences:** "These two sentences are disjointed"
- ACTION: Fix flow

---

## RELATED WORK / ALIGNMENT (C19-C27)

**C19 — Alignment introduction:** "This is the first time we're using alignment in the paper. Not sure if this needs to be here or if we should be mentioning alignment somewhere earlier"
- ACTION: Either introduce alignment in intro or move this section up

**C21 — Subsection necessity:** "We partially specify this within the introduction. Not sure if we need an additional subsection for this"
- ACTION: Consider merging 1.1/1.2 with intro

**C23 — Paragraph to bullets:** "Would prefer if this was covered in bullet points instead of one paragraph"
- ACTION: Convert to structured list

**C24 — Verify provider claims:** "Please backtrack this with existing documentation from each provider"
- ACTION: Verify all provider memory claims against their actual docs

**C25 — Complementing:** "I like the mention of complementing here"
- NO ACTION — positive feedback

**C26 — AlpsBench treatment:** "I would expect each of these benchmarks should have their own paragraph dedicated to them in bullet form. For AlpsBench the reason it was created was not to demonstrate recall ≠ alignment. They were testing an entirely different thesis that should be laid out with respect"
- ACTION: Expand AlpsBench treatment, honor their actual thesis

**C27 — Reference indexing:** "Every time another research paper is referenced there should be an index number that can be referred to within the appendix or references"
- ACTION: Add proper citation numbering throughout

---

## STUDY DESIGN (C31-C55)

**C31 — Verify 50/50 split:** "Can you verify that this was actually a 50/50 split? From my understanding for Hamerton we only did the first 10 chapters. Please verify"
- ACTION: CRITICAL — verify corpus split. Hamerton may be chapter-based, not word-count-based.

**C32 — Question composition:** "Be mention that prediction questions reference these behaviors but we don't actually go over how those prediction questions are composed. Likely should be mentioned somewhere here"
- ACTION: Add battery generation methodology section

**C34 — Subject identification:** "Clearly this source text is referencing a specific subject. Mention which subject and works"
- ACTION: Be explicit about which autobiography each example comes from

**C38 — Predicate spec:** "We also created a predicate spec. Might be worth mentioning here and checking if that's still accurate on the research page"
- ACTION: Reference predicate vocabulary table, verify website accuracy

**C39 — Predicate completeness:** "Are these all of the predicate types or did we leave some of these out? This is very good though"
- ACTION: Verify full 47 predicates listed or reference complete list

**C40 — Better example:** "Is there perhaps a better example of this?"
- ACTION: Find a more compelling example

**C41 — Weight justification:** "Worthwhile bringing up why these particular signals have related weight. Frankly I'm not entirely sure why we gave those weights"
- ACTION: Either justify weights or acknowledge they're heuristic

**C43 — Full prediction example:** "Would really appreciate if a prediction with false positive and directives were provided to give a complete understanding"
- ACTION: Add complete prediction example with all fields

**C45 — Open research area:** "Should likely bring up this as an open research area"
- ACTION: Flag as active research

**C46 — "Faithful" wording:** "Is this a mechanical variation? Should probably specify because we're using a word like faithful"
- ACTION: Clarify or replace "faithful"

**C47 — Layer ablation:** "Likely worth mentioning that we are still doing research on if all four of these artifacts produced the best results or not but we do have some initial testing"
- ACTION: Add note about layer ablation as future work with initial signals

**C49 — Serving layer:** "Not sure if it's worth bringing up here that we are currently working on optimizing this serving layer. This is open or active research"
- ACTION: Mention briefly as active research

**C51 — Provenance via embedding:** "Should likely specify somewhere within this traceability section that it's the embedding that allows us to provide provenance throughout all the generations"
- ACTION: Clarify the mechanism (embedding-based provenance)

**C53 — Memory provider fact comparison:** "Would be curious about the difference when we provide the fact set and when the memory system is allowed to create its own fact set from the corpus"
- ACTION: Interesting future analysis. Note for future work.

**C54 — Adversarial tier rationale:** "Adversarial abstention is a very interesting category. I personally do not understand how this is supposed to operate. Maybe worth pointing out why we decided to add each of these tiers separately"
- ACTION: Add rationale for each tier's purpose

**C55 — Question generation methodology:** "We still have not laid out our approach/theory for creating held out passages, specifically the questions that come from these passages"
- ACTION: CRITICAL — add backward design methodology explanation

---

## RESULTS (C57-C80)

**C57 — Franklin still relevant?:** "We also have Benjamin Franklin. I'm not sure if this is still true after we run the updated global subjects experiment"
- ACTION: Review after rerun data — Franklin section stays (known-figure control)

**C58 — List vs paragraph:** "Not sure if this is relevant considering we are re-running the global subjects. Should also be in list form versus paragraph"
- ACTION: Convert to structured list, update after rerun

**C61 — Response model listing:** "Not sure if we have to mention Claude Haiku 4.5 as the primary response model. Can just start with multi-model validation and list all of them. Should be structured list"
- ACTION: Restructure as list, lead with multi-model

**C63 — Why 1-5 scale:** "Should specify why we picked 1 through 5. It's enough to begin seeing convergence between models but leaves something to be desired"
- ACTION: Justify the scale choice

**C66 — Results table upfront:** "When bringing up results didn't expect to focus specifically on Hamerton beginning. Expected to see a table of all results or at least a statement about what the results were"
- ACTION: STRUCTURAL — consider leading with aggregate results table, then deep-dive into Hamerton

**C67 — Why Hamerton is primary:** "We say 'for the primary subject.' We never specify why Hamerton is the primary subject. Should be some introductory paragraph stating our primary hypothesis and whether it is true or not"
- ACTION: Add results intro paragraph with hypothesis + why Hamerton is primary

**C68 — Cohen's d explanation:** "For any metrics generally not known to the layman like Cohen's d we'll need a short explanation"
- ACTION: Add parenthetical explanation for all technical metrics

**C69 — Baseline figure:** "Should mention the baseline figure here"
- ACTION: Include baseline number

**C70 — Conditions table:** "I don't see any sections actually laying out explicitly what all of the conditions are. We need a separate table that goes over the conditions specifically as well as the sub-conditions"
- ACTION: CRITICAL — add full conditions table (this is a major gap)

**C71 — Percentage table:** "When talking about how much the specification improved every system this should be in table format. Should be explaining how we came to those percentages. Are those on average across all subjects or something else?"
- ACTION: Add table, clarify calculation methodology

**C72 — Formal structure for examples:** "Would appreciate if this is more formally structured. Maybe include notable examples within the appendix"
- ACTION: Move detailed examples to appendix, reference from main text

**C74 — Positive:** "This is great"
- NO ACTION

**C76 — Specify baseline source:** "Specify this is from baseline evaluation"
- ACTION: Clarify which evaluation produced the baseline

**C77 — Model predictive capabilities:** "Maybe worth mentioning that frontier models and/or language models in general may already have some kind of predictive capabilities but those are very opaque"
- ACTION: Good point — add note about implicit behavioral modeling in pretraining

**C79 — Percentage interpretation:** "I think we need to reassess how this effect is calculated or displayed. 168% of the baseline may not be the best way to portray this. Need to think about how to put this into perspective since we are only using a 1-5 scoring scale. Maybe apply some kind of interpretation for what it means to move from 1 to 2, 2 to 3, so on"
- ACTION: CRITICAL — add interpretive framework for score movements (what does going from 1.0 to 2.7 actually mean in terms of prediction quality?)

**C80 — Threshold discussion:** "It seems there's a threshold here. Once you cross the 2.4 baseline is when the effect starts to become negative. I don't remember reading on how the baseline was established. May need to cover that more explicitly earlier"
- ACTION: Add threshold analysis and baseline methodology explanation

---

## DISCUSSION (C83-C110)

**C83 — Judge calibration placement:** "I'm surprised Judge Calibration is showing up so late. This should likely be discussed when talking about the judges the first time instead of within the results section since it's a methodological approach issue"
- ACTION: STRUCTURAL — move judge calibration to Study Design (Section 3.7)

**C84 — Spearman claims:** "If there was a change that needed to be made to the pairwise Spearman row claims, something that had to do with judging significance for the group"
- ACTION: Verify Spearman calculations, consider adding Krippendorff's alpha

**C87 — Section title:** "Should likely be 'the behavioral specification as a tool for the unknown.' Let me know your thoughts"
- ACTION: Update title

**C88 — "Model's ignorance":** "This statement is a little abstract"
- ACTION: Make more concrete

**C89 — Em dashes:** "Will likely need to remove em dashes"
- ACTION: Replace em dashes with standard dashes or restructure sentences

**C91 — Frontier model prediction:** "Earlier mentioned how frontier models may be predicting on well-known public figures. Might be worth mentioning that we provide full traceability whereas the model may not"
- ACTION: Add traceability as differentiator from implicit pretraining

**C94 — Positive:** "This is an exceptionally powerful statement"
- NO ACTION — flag for preservation

**C96 — Spec alone vs serving:** "The working assumption is you would never use the specification alone, ideally it would be paired with some kind of serving layer. The fact that the specification alone can perform better than baseline or even with facts is saying something about how models deal with reasoning guidance"
- ACTION: This is a KEY INSIGHT from Aarik. Work this framing into the discussion.

**C99 — Price update:** "We'll need to re-evaluate the actual price after everything runs"
- ACTION: Update cost numbers after rerun

**C102 — Reorder:** "Generally I think this should be moved down the list"
- ACTION: Reorder in limitations

**C103 — Single model label:** "I don't understand why this is labeled 'single primary response model' when we used multiple models"
- ACTION: Fix label — we used 6 response models

**C104 — Testable now:** "This is something we could potentially test right now before we release"
- ACTION: Evaluate feasibility

**C105 — Human judges:** "Should mention that the judge calibration seeks to mitigate some of this but there's no replacement for human judges on tasks like this"
- ACTION: Add calibration acknowledgment + human judge future work

**C106 — Private tests:** "We have done private tests. It's worth mentioning we may release research on it, we would like to do further study"
- ACTION: Add note about private testing on living subjects

**C107 — Fixed by new run:** "I believe this should be fixed with our new run"
- ACTION: Verify after rerun

**C108 — Diff daemon:** "We didn't bring up anything around how we'd be looking at the creation of a diff daemon. I think it is worth bringing up that this is an open research area"
- ACTION: Add temporal drift / diff daemon to future work

**C110 — Predicate ablation + cost-benefit:** "We did do some predicate ablation, it'd be interesting to test it within this particular context. There's also no mention of cost-benefit analysis. We did not explicitly look at if the trade-off is worth it. Maybe we shouldn't even bring that up"
- ACTION: Discuss with Aarik — cost-benefit as limitation or separate analysis?

---

## APPENDIX / STRUCTURE (C113-C122)

**C113 — Repo link:** "We need to include a link to the repo below this. We also need a link to the repo likely at the beginning. Maybe we should have a cover page"
- ACTION: Add repo link at top, consider cover page

**C117 — Undiscussed finding:** "This is a really interesting finding. It is not discussed anywhere in the main report"
- ACTION: CRITICAL — identify which finding and add to discussion

**C118 — Spec failure modes:** "Would be worth bringing up where the specification fails as well alongside facts. Can also help us describe what it's able to do and what it's not able to do"
- ACTION: Add failure analysis section or expand qualitative examples

**C122 — Figures:** "Would really like to integrate these figures into the report and across the report if possible"
- ACTION: Generate figures from data (4 specs already written in Appendix D). Integrate throughout.

---

## PRIORITY ACTIONS (Critical Items)

1. **C70** — Full conditions table (major gap)
2. **C55/C32** — Battery generation methodology (backward design explanation)
3. **C79** — Score interpretation framework (what does 1→2.7 mean?)
4. **C9** — Core proposition reframing (use Aarik's cleaner version)
5. **C66/C67** — Results section structure (lead with aggregate, justify Hamerton as primary)
6. **C83** — Move judge calibration to methodology
7. **C31** — Verify corpus split methodology
8. **C122** — Generate and integrate figures
9. **C27** — Reference numbering throughout
10. **C117** — Find and discuss the undiscussed appendix finding
