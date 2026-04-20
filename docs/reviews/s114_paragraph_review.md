# S114 Paragraph Review — Beyond Recall v6

**Session:** 114
**Date started:** 2026-04-20
**Target launch:** Tuesday 2026-04-21
**Draft:** `docs/beyond_recall_v6_draft.md`
**Protocol:**
- Paragraph by paragraph, top-to-bottom (Abstract is last)
- Aarik's live notes captured **verbatim** (no paraphrase, no summarization)
- Assistant verifies claims/numbers against `docs/DATA_REFERENCE.md` and `docs/KEY_FINDINGS.md`
- Status tags: `clean` / `edit` / `recompose` / `flag`
- After full pass → recomposition pass → re-review → iterate

---

## §1. Introduction

### §1.1 — Recall Is Not Interpretation. Interpretation Can Be Measured.

#### Word review (round 1) — 8 comments on current live §1.1

1. (anchor: "Memory systems have solved storage") — "Should we be specifying AI memory systems specifically in this case. I should be mentioning what the current state of affairs is around benchmarking."
2. (anchor: "That is the distinction this paper makes rigorous") — "This opening sentence is what it should be. Stating up front that is the distinction this paper makes rigorous is feels off to me."
3. (anchor: "This layer is measurable via held-out behavioral prediction...") — "The second paragraph feels a bit disjointed here."
4. (anchor: "His father was violent...") — "This is an exceptionally heavy opening example of this."
5. (anchor: "Same fact, opposite behavioral predictions") — "I don't know if we should be talking about behavioral predictions this quickly in this fashion."
6. (anchor: "None stores the interpretive layer that gives those facts their meaning for this specific person") — "Is it this specific person or for people in general are individuals rather."
7. (anchor: "An AI agent acting on someone's behalf...") — "Making a logical jump here. When reading this out loud versus reading this in my head I seem to have two different interpretations. It seems I'm struggling with what voice this should be taking. Please provide feedback."

Diagnosis applied: intro was claim-dense and connection-poor. Every sentence was a thesis, nothing was setup. Voice oscillated across four registers (formal academic / provocative / technical CS / direct declaratives). Structural, not sentence-level.

#### Draft 1 (assistant, delivered inline in chat) — REJECTED by Aarik

Structure attempted: setup → gap → claim → email example → pretraining ceiling → what paper does. 6 paragraphs.

#### Aarik feedback on Draft 1 — verbatim

- "In the second paragraph none of these benchmarks measure whether the system has any working model of the person it serves storage is not interpretation. We should be framing this within the lens of benchmarks that benchmarks are measuring recall but recall is not the same thing as interpretation We should avoid switching between recall and storage."
- "Bringing up that three of the four providers returned completely different top one facts does not suggest that storage has been solved not sure where the sentence came from."
- "Should we be introducing behavioral specifications or missing property of representational accuracy."
- "I don't like the email example."
- "Throwing pre training in makes this feel unfocused."
- "Generally not happy with this I did prefer the first archive drafts we had worked on Can you analyze the first one and give feedback on"

Assistant actions from this feedback:
- [pending] Analyze the first / archive drafts of §1.1 and report what was working
- Durable: keep recall vs interpretation as the single pivot. Do not introduce storage as a third term.
- Durable: 93% retrieval-disagreement stat does not support "storage solved" claim. Sequencing error — move or cut.
- Open question: does §1.1 need to introduce Behavioral Specification at all, or defer to §1.2/§1.3?
- Cut: email example
- Cut or defer: pretraining paragraph (belongs in §1.4 territory, pulls focus in §1.1)

#### Assistant: single-point distillation proposed

"There is a property that determines whether an AI agent can act accurately on a specific person's behalf. It is not recall. It is how well the system models how that person reasons. Call it representational accuracy. No current benchmark measures it."

#### Aarik draft (his voice, dictated) — verbatim

> State of the art memory today has been optimizing for recall as the success metric. What base layer has been trying to explore, Is that recall is one part of memory and that in many ways The function of memory is dictated by how an individual processes the facts and experiences of their life.
>
> Think of how viewing situations from different lenses can lead to entirely different understandings and interpretations of the same set of facts this has been showed shown Across the human experience in the sciences to religion to political affiliations and by extension relative experiences of all or any individual.
>
> 4 State of the art AI Memory Systems zip letter Mem 0 and super memory have all scored 85% plus on memory benchmarks. This suggests that the benchmark must evolve past what it is currently optimized for.
>
> We introduce the concept of a benchmark based on representational accuracy. In proposing representational accuracy as the next optimization for AI memory it also requires the application of behavioral prediction unheld out behavioral situations as a proxy for how well an AI agent knows its user in the present.
>
> We test this framework on the leading state of the art AI memory systems as well as a diverse set of 14 autobiographies from authors all across the world. For our initial examination we will be leveraging baselined and calibrated LLM judges to evaluate the performance of these memory systems in comparison to and with a behavioral specification, a static document that extracts and encodes a Stable representation of a corpus's behavioral patterns.

#### Aarik feedback on assistant's cleanup — verbatim

> Yeah may want to move the statement on the forest state of the art a memory systems scoring 85% or higher plus suggesting that the benchmark must evolve somehow merge that into the first paragraph Little confused with representational accuracy and or verses interpretation

Actions:
- Merge the 85%+ statistic + "benchmark must evolve" into opening paragraph so the state of the art has teeth immediately.
- Clarify the semantic relationship between "interpretation" (human-side: how an individual processes facts) and "representational accuracy" (AI-side: the system's capacity to model that). They are not synonymous and the current draft leaves the bridge implicit.

#### Aarik feedback (round 3) — verbatim

> the goal is to understand the core of what im trying to get at and drafting from there. I think we need to define representational accuracy as its been shared here being a property of the AI system. Interpretation should also be defined within this introduction. I like the relationship maybe we should be stating that as the core hypothesis of what we are researching here.

Actions:
- Define "interpretation" explicitly in §1.1 (human-side property)
- Define "representational accuracy" explicitly in §1.1 (AI-side property)
- State the relationship between them as the CORE HYPOTHESIS of the research
- Draft from understood core, not from surface iteration

#### Aarik feedback (round 4) — verbatim

> Can you confirm that those four leading systems are all scoring 85% or higher on recall benchmarks. Should likely change what base layer has been trying into base layer is exploring how recall is one part of memory. I like the second paragraph I think we need to make it very clear why interpretation as a human side property is required for AI memory systems. Maybe can bring up memory is a very personal topic Therefore it should be personalized for each individual Something along those lines. For representational accuracy paragraph instead of using separate sentences should just be one continuous sentence of what representational accuracy is not. It is not recall preference matching or persona consistency, it is a distinct property of an AI system and no current benchmark is built to measure it. I like that 4th paragraph.

Actions:
- VERIFY the 85%+ claim for all four systems (or hedge)
- Rewrite ¶1: "Base Layer is exploring how recall is one part of memory..." (not "has been trying to explore")
- Rewrite ¶2: add the "memory is personal → must be personalized → interpretation required" logic
- Rewrite ¶3: collapse "is not recall / is not preference / is not persona" into one continuous sentence
- ¶4 locked

#### Aarik feedback (round 5) — verbatim

> If you can do research on each of the providers and confirm any benchmarks that they have provided should include those in the repo as well as source documents Based on that will take an approach to how we should talk about the Spirit saying all report and then per their own publish results is redundant. In many ways this filler language. The second paragraph starting with think of how viewing situations S2 direct first person need to make it more declarative. By extension to the relative experiences of an individual feels like a throw away sentence need to make it something slightly more concrete. Between person persons and corpus should likely pick one but not sure how to think about that. The core hypothesis isn't as much focused on acting on a specific person's behalf as it is being aligned with the user's intent and behavior.

Actions:
- Research each provider's benchmark claims (Mem0, Letta, Supermemory, Zep) with sources, save to repo (pending, agent dispatched)
- Cut filler: "all report X per their own published results" reads as redundant hedging. Wait for research findings before rewriting ¶1.
- Rewrite ¶2 "Think of how..." as declarative third-person statement
- Rewrite "by extension to the relative experiences of an individual" with something concrete
- Pick consistent term across §1.1: "person" throughout conceptual framing, "corpus" only in methods ¶5
- **Major reframe on core hypothesis:** pivot from "acting on a specific person's behalf" (agency framing) to "aligned with the user's intent and behavior" (alignment framing). Connects to §1.6 Behavioral Alignment.

#### Benchmark research finding — MATERIAL FOR PAPER-WIDE CLEANUP

Written to `docs/research/provider_benchmarks.md` with sources.

**The "all four score 85%+ on recall benchmarks" claim is NOT defensible from primary sources.**

| Provider | Best published number | Source | Hits 85%+? |
|---|---|---|---|
| Mem0 | 68.44 LOCOMO (paper, Chhikara et al. 2025); 91.6 / 93.4 (vendor blog, disputed + unreproducible) | arXiv:2504.19413 | No in paper; disputed in blog |
| Letta | 74.0% LOCOMO (GPT-4o-mini) | letta.com/blog/benchmarking-ai-agent-memory (2025-08-12) | No |
| Supermemory | 85.2% LongMemEval_s (Gemini-3-Pro); 81.6% (GPT-4o) | supermemory.ai/research | Narrowly yes, model-specific |
| Zep | 71.2% LongMemEval (GPT-4o) | arXiv:2501.13956 (Jan 2025) | No |

**Implications:**
- Paper's abstract and §5.7 both assert "85%+" — those claims need to be softened too
- §2.1 Supermemory citation (81.6% / 85.2%) is fine as-is
- §1.1 must not assert 85%+ for all four
- Tightest honest claim: "vendors report LOCOMO/LongMemEval accuracies in the 68–85% range; scores are self-reported, benchmarks and models vary, independent replications are limited"

#### Aarik feedback (round 6) — verbatim

> remove "in many ways" in paragraph 1. I'm good with using a for paragraph one

Actions:
- Pick Option A for ¶1 (range-specific, honest, 68%–85%)
- Cut "in many ways" filler from ¶1 Base Layer sentence
- §1.1 ready for lock pending final read

#### Aarik feedback (round 7) — verbatim

> instead of base layer is exploring, it should likely be this research paper explores?
> otherwise lock this

Actions:
- Apply "This research paper explores" in ¶1 (paper as agent, not organization)
- §1.1 **LOCKED** — applied to `docs/beyond_recall_v6_draft.md` (replaced L260-280)
- `beyond_recall_review.docx` regenerated
- `beyond_recall_review.html` regenerated

#### §1.1 LOCKED VERSION (source of truth)

> State of the art AI memory has been optimizing for recall as the success metric. The four leading systems (Zep, Letta, Mem0, and Supermemory) compete on standard recall benchmarks such as LOCOMO and LongMemEval, reporting accuracies in roughly the 68% to 85% range depending on provider, model, and benchmark variant. Optimizing further on recall leaves something more fundamental unmeasured. This research paper explores how recall is one part of memory, and how the function of memory is dictated by how an individual processes the facts and experiences of their life.
>
> We use **interpretation** to refer to this human-side property: the way a specific person processes facts and experiences into judgments, decisions, and reactions. A single set of facts, processed through different interpretive lenses, produces different judgments. This pattern is well-documented across the sciences, religion, and political affiliation. It also operates at the individual level: two people facing the same decision can reach opposite conclusions from identical information. Memory is deeply personal. For an AI memory system to serve a specific person, it must be personalized to how that person interprets, not just to what facts they have produced.
>
> We introduce **representational accuracy** as the corresponding AI-side property: how well a system's internal model of a specific person captures that person's interpretive patterns. It is not recall, preference matching, or persona consistency; it is a distinct property of the AI system, and no current benchmark is built to measure it.
>
> **The core hypothesis of this research is that representational accuracy predicts alignment between an AI system's behavior and the intent and behavior of the person it serves.** If an AI system's model of a person accurately captures how they interpret situations, its responses should align with that person's intent and behavior in situations the system has never seen. The operational test is behavioral prediction on held-out situations, used here as a proxy for this alignment.
>
> We test this hypothesis on the leading state-of-the-art AI memory systems and on a diverse set of 14 autobiographies from authors across the world. For this initial examination we use baselined and calibrated LLM judges to evaluate the performance of each memory system, on its own and in combination with a behavioral specification: a static document that extracts and encodes a stable representation of a corpus's behavioral patterns.

#### Calibrated voice signals captured from §1.1 work (carry forward to §1.2+)

- Open with plain declarative state of the art, not with thesis
- Use `benchmark / evaluation` framing to set up gaps, not emotion
- Third-person "this research paper" as the agent (not "Base Layer" in body text)
- Pair concept definitions explicitly when they have human-side and AI-side analogues
- State hypothesis explicitly, bolded, not hedged
- No em-dashes
- No "in many ways" / "per their own published results" / filler hedging
- Use "person" in conceptual framing; "corpus" only in methods; avoid "user" for now
- Use ordinary concrete examples (two people facing the same decision), not emotional ones
- Parallel-list "It is not X, Y, or Z; it is W" single-sentence form, not three bullets
- Alignment framing over agency framing (alignment between AI behavior and person's intent/behavior)

#### Paper-wide punch-list items created during §1.1 work

- Sweep abstract L217 and §5.7 L1134 for "85%+" claim; apply same softening as §1.1 ¶1
- Consider renaming/retitling §1.1 since "makes rigorous" language was cut from the body

---

## §1.2 What We Tested

#### Aarik pre-draft commentary — verbatim

> I think 1.2 should name all control conditions if we're labeling it what we tested that should be in a table format most likely or some type of matrix. We may want to include a dot plot as well color coded for each condition. But I guess that would be getting into results so that may be something we want to put in the blog post or abstract. AH 1.3 is what we found since this is the paper it feels like this first section is an in many ways am I thinking about this correctly. Feel free to collapse or expand I agree with your single point that you'd like to bring up at one point 2 Let me see a draft.

Actions:
- §1.2 must name all control conditions, table/matrix form
- Dot plot belongs in results (§4) or blog, not §1.2
- Confirm §1 structure is an "extended guided tour" style intro (§1.1 problem → §1.2 tested → §1.3 found → §1.4 scope → §1.5 not-claim → §1.6 alignment). Defensible on arXiv but worth naming so Aarik can see the spine.
- Single point agreed, draft §1.2

#### Aarik feedback on draft 1 of §1.2 — verbatim

> In this paragraph you do not bring up our controls I think we should preface by what the high level split is. First is a fixed set of facts and to see the performance of each of these memory systems across these autobiographies this lets us measure if there's any kind of fact convergence between the providers if given the same set of facts. The Second is giving the raw corpus to each of these providers as a real world test and seeing how they perform. As part of all of these we are also in parallel testing the specification alone and in addition to. Remember no one is going to be familiar with the conditions are running so when you have all the condition numbers out of order on the left that can be very confusing so the descriptions need to be very very clear Should be using a reasonable amount of space to describe each of these.

Actions:
- Preface with high-level split before the condition table:
  - First split: fixed fact pool (controlled test) → measures fact-convergence across providers on identical input
  - Second split: raw corpus (native test) → real-world measurement of each provider's own pipeline
  - Parallel to both splits: specification alone and in combination
- Condition table: description-first, not number-first; numbers in parens for reference; descriptions given reasonable space; ordered by logic, not by numeric code
- Wrong-spec explicitly describes v1 and v2

#### Aarik feedback on draft 2 of §1.2 — verbatim

> I think this is fine for now A fine to use top kfax as well. We should make a note on additional testing around LETTA Due to its unique operation compared to the other memory systems. On the 4th point fine to repeat

Actions:
- Add note about Letta-specific additional testing (stateful-agent path, §4.3.1, n=3 subjects)
- Top-k phrasing kept as-is
- Final evaluation paragraph kept (4th point)
- Ready for lock pending Letta note review

#### §1.2 LOCKED — applied to source

Aarik: "lock"

- Applied to `docs/beyond_recall_v6_draft.md` (replaced L272-276)
- `beyond_recall_review.docx` regenerated
- `beyond_recall_review.html` regenerated

#### Voice signals captured from §1.2 work (carry forward to §1.3+)

- High-level structural splits (controlled vs native) named explicitly before diving into matrix
- Table rows lead with plain-language names, condition codes parenthetical; ordered by experimental logic, not numeric code
- Give each row reasonable space for purpose/interpretation, do not compress unfamiliar jargon
- Separate paragraph for architecturally distinct subtests (e.g., Letta stateful) with scope caveat (n=3, 9× corpus range)
- Pointer to §3 for full methodology rather than duplicating detail in §1
- Keep final "how it was evaluated" paragraph even if §1.1 touched the same ground; reinforcement at paragraph end is fine in an extended-guided-tour intro

---

## §1.3 What We Found + §1.2 additions

#### Aarik pre-draft feedback — verbatim

> for what we tested would it be good to include some insight on the Llm judging and baselining. We also need to introduce the concept of what it means to have a low baseline with the model I think the calibration needs to be mentioned within that 1.2 as well. We should be covering all major findings within 1.3. It should open with a single sentence maybe it can be a paragraph It should be the major finding of the paper but it should not be idolizing the result This is where we also need to bring a baseline It does improve with the behavioral specification as long as the baseline is below a particular gradient We need to be very honest with how we are presenting the behavioral specifications additive nature

Actions:
- **Reopen §1.2** to add:
  - Definition of baseline (C5, low-baseline = ≤2.0, population relevance)
  - LLM judge calibration detail (what was calibrated, how, Gemini offset, 7 vs 5 non-Gemini)
- §1.3 draft must cover ALL major findings
- Open with single sentence or short paragraph stating the major finding
- Must NOT idolize the result — honest framing
- The honesty lever: spec improves ONLY when baseline is below a particular level; effect is a gradient, not universal
- Frame additive nature carefully — spec is additive to memory systems, not a replacement, and effect is population-dependent

#### Aarik feedback on draft 1 of §1.3 + §1.2 additions — verbatim

> We need to describe the one through 5 scale. We also need to give some understanding of what it means to increase by one point on that scale. In 1.2 we should likely be providing a list of the 14 subject autobiographies we used unless you think that should be in a later section. The 7300 token specification performing higher than the raw training corpus is a great finding it feels a bit buried. For robustness circularity concerns are still an issue because judging was done with language models Not sure if it's fair to say they are diffused. We should make it clear for Letta on how the block grows from 22K to 335K specifically that it seems to increase linearly based on the size of the source. Should note that as it grows in size we have noted a 25% duplication issue Not fair to say at the largest scale because we didn't test larger than this. Also worthwhile pointing out the significance of 335,000 characters We do have references from existing examples as well as personal data to help describe the significance of that size in the grand scheme of how large a corpus can be. We may also want to include token count alongside character count.

Actions:
- §1.2: Add 1-5 rubric with anchors (the paper's §3.7 rubric) + what a 1-point gain means qualitatively
- §1.2: Add a compact list of the 14 subjects (chronological, spans 4 continents + 2 millennia); defer full table to §3.2
- §1.3: Split out a dedicated "Compression" finding highlighting 7,300-token spec > 34,168-token raw corpus
- §1.3 Robustness: soften "defused"; say Tier 2 addresses within-Anthropic circularity but LLM-as-judge circularity is a broader study limitation flagged in §6
- §1.3 Letta: state linear block growth explicitly with per-subject chars + tokens; avoid "at the largest scale" generalization, use "on the largest corpus we tested"; contextualize 335,000-char ceiling against real-world corpora
- §1.3 Letta: include token counts alongside character counts for all three subjects

#### Aarik feedback on draft 2 of §1.3 — verbatim

> On the spec scoring near baseline I believe some of the data had shown the wrong spec can actually negatively affect a model's ability and in some cases there were outright refusals to answer or acknowledgement that this was completely different than the person at hand might be worth mentioning that within mechanism. For additivity Not sure what to make of the Super memory plus 0 I think with fixed facts it was a different metric compared to feeding the whole corpus to super memory. If supermemories retrieval leaves less headroom for the specification then the question becomes are facts enough versus the specification. The way it's presented here it brings into a large question whether or not a behavioral specification matters if you have the right facts based on super memories performance

Actions:
- §1.3 Mechanism: add wrong-spec negative effect (V1 Franklin-for-all scores below baseline at −0.16), add the detection/refusal behavior
- §1.3 Additivity: address the "facts enough vs specification" question head-on. Supermemory's near-zero is a retrieval-distribution effect, not evidence facts replace spec. Reference the compression finding (C2a > C4 at same tokens) to close the loop.

#### Aarik feedback on draft 3 of §1.3 — verbatim

> we need to run that analysis if we have the raw numbers as well.
> for 2. if both of those are possible, then we need to bring this up. may be worth doing some direct analysis of those responses to see how super memory was different from supermemory + spec. May provide some insights. Share examples here we can examine together.
> If super memory is at 0, then we need to udnerstand whats the difference. Is something different being brought up in the spec version, or a different tone.

Actions (analyses authorized, running in background):
- Agent 1: quantify wrong-spec detection/refusal rate from C2c response data. Produce rate numbers + example quotes.
- Agent 2: paired analysis of Supermemory C1 responses vs Supermemory C3 (C1 + spec) responses on same questions. Identify qualitative differences even where quantitative score delta is ~0. Surface 3-5 example pairs.
- Both agents write to `docs/research/` for later review.

#### Aarik feedback (round — while agents run) — verbatim

> yeah lock 1.2, are there any graphs we can add for each of these in results. Reading all the figures in word form is very heavy. We should be plotting below every paragraph honestly, unless that would be highly unusual

Actions:
- §1.2 LOCKED (additions applied to source)
- For §1.3 figure-density: existing 9 figures cover 5 of 7 findings. Gaps: Tier 2 replication (robustness), Letta scaling + duplication (architectural).
- For review readability: inline figures per finding in §1.3 is reasonable. For arXiv final, a mid-path (one summary figure in §1, detail in §4) is most conventional.
- After §1.3 content locks: update `export_to_docx.py` and `build_review_html.py` to place figures under each finding's bold-label anchor for review doc

#### Figures 10 and 11 generated

- `figures/fig10_letta_scaling.png` — two-panel: block size vs corpus size (Letta vs BL), plus duplication % bar chart
- `figures/fig11_tier2_replication.png` — grouped bar chart of spec-Δ per subject × response model (Sonnet vs Gemini Pro)

#### Supermemory analysis findings approved for integration

Aarik: "wonderful findings, please integrate as appropriate. please make this very clear. Would it be worth providing results overviews per memory system as part of this section as well?"

Actions:
- Expand Additivity with compact per-system bullet summary (matches §4.3.2 character sketches in condensed form)
- Add new finding "Where the specification helps and where it hurts" with Keckley Q21 anchor and three-failure-mode framing
- Flag differentiated-battery follow-up (§7)

#### Aarik feedback on §1.3 draft with findings integrated — verbatim

> for addivity for supermemroy need to specify like you did for me, there were really wild delta swings. That needs to be brought up. That is not clear, more research will need to be done there. --- you also need to provide performance of base layer's memory implementation, as an open source alternative. imporatnt to see what can be "hacked" together. ---- For where the specification helps and where it hurts this needs to be explained better the last sentence in particular I do not understand what redistribution of large per question effects that cancel at the mean means. If we're going to reference specific questions as examples then we need to provide the actual text in line That can be a separate call out or graphic within the report itself but we need to be able to see those. The first sentence for each of these findings needs to be layman understandable the definitions as they stand now immediately start as technical.

Actions:
- Additivity: mention Supermemory's "wild delta swings" in the per-system bullet, cross-reference the next finding
- Additivity: add Base Layer's actual numbers (C1 mean ~2.30, spec delta +0.13 on low-baseline) so readers see what the open-source retrieval floor produces
- "Where helps vs. hurts": rewrite the "redistribution of large per-question effects" sentence in plain English (helped on many, hurt on many, cancel at the mean)
- "Where helps vs. hurts": inline the actual question text for every referenced example (Ebers Q3, Sunity Devee Q35, Keckley Q21)
- Every finding's FIRST SENTENCE must be layman-understandable. Technical numbers come after.
- Wrong-spec Mechanism: use a verbatim example quote (from the agent's classification output) not a paraphrase

#### Workflow change + §1.3 LOCKED

Aarik: "please bold the first layman sentence, each of those is great! lock. ... dont bother replace the current 1.3, you should be drafting this as a new document to keep credit usage low. Can refer to previous document, but not need to regenerate, can just append to a new document as we get through each section."

Actions:
- v7 draft at `docs/beyond_recall_v7_draft.md` — new document, appended section by section as each locks
- v6 (`beyond_recall_v6_draft.md`) untouched going forward; stays as reference for unreviewed sections
- Layman sentences bolded in §1.3 (alongside the section labels)
- `.docx` / `.html` regeneration paused; will regenerate only when Aarik asks
- §1.1, §1.2, §1.3 all present in v7 as locked content

## §1.4 Why the Gradient Matters for Real Users

### Aarik pre-draft commentary — verbatim

> 1.5 should likely be collapsed into 1.4. I agree with the single point to land the reason that's what we're shooting for it's because this is really showing the need for deeper personalization or per user configuration or synchronization when it comes to human AI interaction. This is interesting because I am using it personally it's in the cloud file here it's in my cloud app I already use it when I tell you produce something or to change something I point you to my behavioral specification. The whole point of this study is to understand how to improve the interactions of all individ not just the ones that the happens to have been trained on. You should likely run a baseline on my personal data actually and see where that number comes to... But yes the working assumption would be if most of the world is on this either all of the models are trained not individuals or we need to ensure there is some kind of human AI interaction platform to facilitate this kind of human AI understanding

### Aarik lock feedback — verbatim

> Go with the proposed title. Say we have run initial pilots with two real users on their private. May also want to mention that we're looking into alternative ways to test reasoning structure such as Supreme Court opinions. If possible for these results would appreciate if you go through select examples for each of the condition runs to ensure we are not missing any specific details like we were with super memory for any of the other providers. Letta in particular with its full stateful agent conditions would be interesting to look at the direct results of.
> this 1.4 draft is generally really great though

### §1.4 LOCKED — appended to v7

Structural changes:
- §1.5 (What This Paper Does Not Claim) collapsed into §1.4 ¶2
- §1.6 (Behavioral Alignment) renumbered to §1.5
- Five subsections now: §1.1, §1.2, §1.3, §1.4, §1.5

Content changes from draft:
- Title: "Why the Gradient Matters for Real Users"
- "two real users on their private corpora" (was "one to two")
- Added SCOTUS opinions mention as alternative testbed
- Em-dash fixed in ¶3 (colon + string as payoff: "...user-held, portable, inspectable, traceable, representation-grade.")

### Three analysis agents launched (running in background)

1. **Aarik baseline pilot** — C5 measurement on Aarik's own private data. Writes to `C:\Users\Aarik\Anthropic\_internal\aarik_baseline_pilot\` (outside repo; internal evidence only per Aarik's instruction).
2. **Letta stateful deep-read** — full analysis of Letta stateful-agent memory block content + matched-model paired comparison vs. BL spec + brief archival-path check. Writes to `docs/research/letta_stateful_deep_read.md`.
3. **Mem0 / Letta-archival / Zep paired analysis** — mirror of the Supermemory methodology on the other three commercial memory systems to check for hidden per-question swings. Writes to `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`.

Findings will surface for possible integration into §1.3 or §4.3 if they materially change the story.

---

## §1.5 Behavioral Alignment and the Human-AI Interaction Problem (formerly §1.6)

(pending — next to draft)
