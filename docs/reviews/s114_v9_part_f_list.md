# Part F — Section-by-Section Wording Reference List

Source: `docs/reviews/s114_v9_edit_plan.md` (Part F) and `docs/reviews/s114_word_annotations.md`.
Purpose: a single walkable reference of every Part F (section-scoped wording) annotation from v8, so Aarik can review top-to-bottom.

**Classification key**
- `APPLIED` — already addressed by Part A-E sweep or a specific triage decision (cross-referenced in status)
- `SAFE_MECHANICAL` — can be applied without further author input (Part F batch agent scope)
- `AUTHOR_JUDGMENT` — needs Aarik review before v9 edit
- `DEFERRED` — deliberately skipped for v9 (needs rerun, new data, or scope decision)

**Scope**
Excludes annotations absorbed into Parts A-E (cross-cutting sweeps, structural moves, data reruns, figure rebuilds, headline list). Only section-scoped wording/clarity/phrasing items appear here.

---

## Summary table

| v8 Section | Part F rows | SAFE_MECHANICAL | AUTHOR_JUDGMENT | APPLIED (already absorbed) | DEFERRED |
|---|---|---|---|---|---|
| §1.1 | 2 | 2 | 0 | 0 | 0 |
| §1.2 | 9 | 4 | 1 | 4 | 0 |
| §1.3 | 24 | 10 | 7 | 7 | 0 |
| §1.4 | 2 | 1 | 1 | 0 | 0 |
| §1.5 | 1 | 1 | 0 | 0 | 0 |
| §2 | 5 | 1 | 3 | 1 | 0 |
| §2.1 | 2 | 0 | 0 | 2 | 0 |
| §2.3 | 4 | 2 | 1 | 1 | 0 |
| §2.4 | 1 | 1 | 0 | 0 | 0 |
| §2.5 | 1 | 0 | 0 | 1 | 0 |
| §3 (intro) | 1 | 1 | 0 | 0 | 0 |
| §3.1 | 2 | 1 | 1 | 0 | 0 |
| §3.2 / §3.2.1 | 3 | 0 | 0 | 3 | 0 |
| §3.3 | 5 | 3 | 1 | 1 | 0 |
| §3.4 / §3.4.1 | 5 | 2 | 1 | 2 | 0 |
| §3.5 | 5 | 0 | 0 | 4 | 1 |
| §3.6 | 4 | 0 | 3 | 1 | 0 |
| §3.7 / §3.7.2 / §3.7.3 / §3.7.4 / §3.7.5 / §3.7.6 | 11 | 4 | 4 | 3 | 0 |
| §4 intro + §4.1 / §4.1.1 / §4.1.2 | 10 | 2 | 3 | 5 | 0 |
| §4.2 / §4.2.1 + examples | 13 | 2 | 3 | 4 | 4 |
| §4.3 + wrong-spec examples | 17 | 3 | 5 | 7 | 2 |
| §4.4 + Supermemory subsection | 16 | 3 | 4 | 6 | 3 |
| §4.5 / §4.5.1 / §4.5.2 / §4.5.3 | 8 | 3 | 2 | 3 | 0 |
| §4.6 | 5 | 0 | 1 | 4 | 0 |
| §4.7 / §4.8 | 3 | 0 | 0 | 3 | 0 |
| §5 / §6 / §7 / §8 | 8 | 0 | 3 | 5 | 0 |
| **TOTAL** | **162** | **49** | **44** | **59** | **10** |

Counts are approximate (single rows can map to multiple sweeps); see Part F of the edit plan for the canonical triage.

---

## §1 Introduction

### §1.1 Recall Is Not Interpretation

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F1.1-1 | "used here as a proxy for this alignment." | "Behavioral prediction as a proxy is lightly covered in the introduction, would expect a bit more insights/definitions on this." | SAFE_MECHANICAL | Pairs with A12 (define "behavioral prediction" on first use). Add 2-3 sentences + forward pointer to §3.1. |
| F1.1-2 | "behavioral specification" | "Bolded for emphasis" | SAFE_MECHANICAL | Apply **bold**. |

### §1.2 What We Tested

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F1.2-1 | "aggregated per (subject, condition) cell via the locked rule (within-judge mean, then across-judge mean; subject is the unit of inference)" | "Bit confusing with the paranthesis." | SAFE_MECHANICAL | Break into two sentences. |
| F1.2-2 | "As a secondary outcome, we report the per-question win rate against the no-context baseline" | "Should we not be doing a per question winrate for all sources, then we can display win rate for all conditions" | SAFE_MECHANICAL | Add forward pointer to §4.2.1 (already reports per-condition). |
| F1.2-3 | "classify the outcome as improved / tied / worsened, and report all three rates alongside the median magnitudes" | "Bit confusing, is that how we classify the outcome? Confusing when bringing up median magnitudes specifically" | SAFE_MECHANICAL | Rewrite as two sentences. |
| F1.2-4 | "The experiment has two main splits..." | "Thinking primary and secondary outcomes should come after covering experiment and conditions?" | AUTHOR_JUDGMENT | Reorder within §1.2: (1) subjects, (2) conditions, (3) outcomes. Confirm intent before moving. |
| F1.2-5 | "Top-k facts retrieved by each memory system..." | "Should specify here the sub condition. Maybe a separate column, just listing sub conditions inbetween condition and inputs given to the model" | APPLIED | Covered by B7 (experimental conditions table). |
| F1.2-6 | "v1 is a deterministic fixed pairing..." | "Broke these up a little for readability" | SAFE_MECHANICAL | Accept tracked line break. |
| F1.2-7 | "Fractional scores (e.g., 2.5, 3.4)..." | "Should add a line on significance of moving between anchor numbers" | APPLIED | Covered by A3 (anchor-crossing framing sweep). |
| F1.2-8 | "Each condition was evaluated with 6 response models across 3 providers..." | "Could this be a table instead? Response models, judges, sensitivity judges..." | APPLIED | Covered by B8 (judge/response-model table). |
| F1.2-9 | (§1.2 outcomes-before-experiment ordering) | Meta-note on section flow. | APPLIED | Same as F1.2-4 re-framing. |

### §1.3 What We Found

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F1.3-1 | "real AI user" | "Real ai user is vague here" | SAFE_MECHANICAL | Covered by A14 (define "real AI user"). |
| F1.3-2 | "most strongly on that slice." | "Most strongly on which slice? can likely cut this" | SAFE_MECHANICAL | Cut. |
| F1.3-3 | "specification helps." | "The more the specification helps? Or the more the specification helps increase representational accuracy?" | SAFE_MECHANICAL | Replace with specific outcome language. |
| F1.3-4 | stats-heavy paragraph | "This feels heavy, a lot of random numbers not focused" | APPLIED | Covered by A1 (layman-ize statistics sweep). |
| F1.3-5 | "12 of 14 subjects improve" | "This should likely be moved up maybe? Feels like hiding the lead, maybe first paragraph?" | AUTHOR_JUDGMENT | Move to lead of §1.3. Confirm paragraph restructure direction. |
| F1.3-6 | "category-level change" claim | "Need to make this clear how" | AUTHOR_JUDGMENT | Expand with 1-2 sentences (refusal → engagement; generic → subject-specific). Aarik should sanity-check example choice. |
| F1.3-7 | "exceeds the raw corpus" | "Need to give comparison how large this is compared to the specification. If mentioning compression need to show compression figures" | SAFE_MECHANICAL | Add 7,300 vs 34,000 token comparison inline. |
| F1.3-8 | "2.63" | Score needs explanation. | APPLIED | Covered by A3. |
| F1.3-9 | "3.09" | Same. | APPLIED | Covered by A3. |
| F1.3-10 | "Measurement. … reads like compression story" | Label wrong. | SAFE_MECHANICAL | Retitle paragraph "Compression". |
| F1.3-11 | "efficiency claim at 5% of context" | "Burying the lead" | SAFE_MECHANICAL | Surface as first sentence of compression paragraph. |
| F1.3-12 | "with complete 5-judge primary coverage" | Sentence too long. | SAFE_MECHANICAL | Cut the clause. |
| F1.3-13 | wrong-spec bimodal distribution | Wants a small table. | AUTHOR_JUDGMENT | Add inline 2-row table (content choice needs review). |
| F1.3-14 | narrow-rule vs broad-rule hedging | "Im confused, so it's being evaluated by two rules. This narrow rules seems almost too narrow. Is this necessary, maybe move to main section instead of introduction" | AUTHOR_JUDGMENT | Drop narrow rule from §1 intro; keep broad rule only. Confirm decision. |
| F1.3-15 | "broad rule is the primary one" | Aarik agrees. | APPLIED | Covered by F1.3-14 resolution. |
| F1.3-16 | "stateful-agent path examined separately below" | Include section number. | APPLIED | Covered by A10. |
| F1.3-17 | Supermemory near-zero aggregate | "Should mention what the delta is... may be useful to provide a range. Maybe a min/max." | SAFE_MECHANICAL | Add min/max numerical range. |
| F1.3-18 | Base Layer substrate description | "Should be mentioned as local" | SAFE_MECHANICAL | Add "local" explicitly. |
| F1.3-19 | Supermemory per-question swings | "Still might be worth adding a delta number in super memory additivity entry" | SAFE_MECHANICAL | Add Δ_C3 − Δ_C1 value. |
| F1.3-20 | ">0.3 large" claim | "why is .3 large?" | SAFE_MECHANICAL | Add one line: "> 0.3 is roughly a third of an anchor band." |
| F1.3-21 | Ebers Q3 example | "Makes me wonder if we should have more example earlier that showcase how obvious this difference can be. Maybe when talking about the judging rubric can give direct examples of what is a 1,2,3,4,5..." | AUTHOR_JUDGMENT | Add rubric illustration examples in §3.7.1. Requires example selection. |
| F1.3-22 | "specification's honesty axioms" | "Do all subjects have honesty axioms? Is that consistent?" | AUTHOR_JUDGMENT | Needs small spec audit before answering in one line. |
| F1.3-23 | "§7." | "In 7 and/or 8?" | SAFE_MECHANICAL | Clarify both sections. |
| F1.3-24 | Letta memory-block linear growth | "Might make this is a separate paragraph start" | SAFE_MECHANICAL | Break paragraph. |

### §1.4 Why the Gradient Matters

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F1.4-1 | "both sit in the mid-baseline band where pretraining coverage is more substantial" | "Interesting that franklin improved as well, may want to bring that up as curious given franklins's baseline?" | SAFE_MECHANICAL | Add 1-line note. |
| F1.4-2 | "because that record does not exist in a form that can be trained on." | "Its not necessarily that the record does not exist, but that it needs to be inferred by the system itself. Human's don't recognize their own patterns much of the time..." | AUTHOR_JUDGMENT | Rewrite with inference framing — philosophical precision, confirm wording. |

### §1.5 Behavioral Alignment section heading

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F1.5-1 | "1.5 Behavioral Alignment and the Human-AI Interaction Problem" | "Should bring up which section this is discussed in" | SAFE_MECHANICAL | Add section pointer in heading or opening line (§7). |

---

## §2 Related Work

### §2 intro

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F2-1 | "2. Related Work" section position | "Seems we are opting to put related work as 2nd, a lot of paper seem to put it last for some reason" | APPLIED | Keep 2nd — Aarik commented, did not push for move. |
| F2-2 | "Some efforts build memory architectures modeled on human memory..." | "Should name these categories a bit more specifically, seems to be brain based memory systems, vs cognitive sciences." | AUTHOR_JUDGMENT | Covered by A13 (define neural-memory-analogue) but category naming needs Aarik confirmation. |
| F2-3 | "We do not want an unbiased system for personalization; we want a system biased to the individual." | "Want is a strong word. As researchers is that what we want, who are we making this statement as?... Enter syncopathy arguments" | AUTHOR_JUDGMENT | Reframe as requirement of personalization problem, not researcher preference. Wording needs review. |

### §2.1 Memory systems

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F2.1-1 | "Mem0 (Chhikara et al., 2025): An extract-consolidate-retrieve pipeline..." | "Redundant list alongside table it seems. Pick one." | APPLIED | Covered by B6 (pick list or table). |
| F2.1-2 | "A note on benchmark scores in this field" | "Is this a note, or a necessary statement?... Likely should leave 2.1 as memory provider overview, add this note to benchmark 2.3, and then move 2.3 to 2.2." | APPLIED | Covered by B4 (move to §2.3 head). |

### §2.3 Benchmarks

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F2.3-1 | "PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416)" | "All of these should have examples of what exactly is being tested" | APPLIED | Covered by A11 (cited-work examples sweep). |
| F2.3-2 | "produced positive results" | "Should mention what positive results, and this is where initial hypothesis around compression beating raw corpus or raw facts came from" | AUTHOR_JUDGMENT | Expand: state the Twin-2K 71.83% accuracy result and compression-ratio origin story. |
| F2.3-3 | "LoCoMo" | "Should also state what the industry standard benchmarks are. Likely should have longmemeval and locomo as the first two, as today's major memory benchmarks" | SAFE_MECHANICAL | Reorder §2.3 to put LongMemEval + LoCoMo first. |
| F2.3-4 | (general §2.3 ordering) | Part of B4 move. | SAFE_MECHANICAL | Covered by B4. |

### §2.4 Cognitive foundations

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F2.4-1 | "extract persona representations as steerable vectors inside model activations..." | "Needs to be more layman explanation" | SAFE_MECHANICAL | Plain-English rewrite. |

### §2.5 LLM-as-judge

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F2.5-1 | judge-biases paragraph | "We didn't do any floor testing as well?" | APPLIED | Covered by P0-17 (judge floor-testing diagnostic — not wording). |

---

## §3 Study Design

### §3 intro

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3-1 | "two intertwined but separable halves" | Vague / filler. | SAFE_MECHANICAL | Cut. |

### §3.1 Representational Accuracy

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.1-1 | three-part claim about representational accuracy | "Should likely be a list, and don't need to state all three matter" | SAFE_MECHANICAL | Convert to numbered list, drop "all three matter." |
| F3.1-2 | "would respond in those held-out cases" | "Would respond in what context, specifically behaviorally... working assumption is they are stable to some extent... refers to this being an incomplete implementation." | AUTHOR_JUDGMENT | Rewrite with behavioral-prediction precision + forward pointer to future-work serving-layer. Needs Aarik's framing. |

### §3.2 Subjects + §3.2.1 Pretraining coverage

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.2-1 | "baseline as an observable proxy" | "Should likely be a figure including all of the subjects and their baseline score" | APPLIED | Covered by B5 + Figure 4.4. |
| F3.2.1-1 | cultural figure (Figure 9) | Move to appendix. | APPLIED | Covered by Part D. |
| F3.2.1-2 | baseline-band table | Collapse into §3.2. | APPLIED | Covered by B5. |

### §3.3 Pipeline

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.3-1 | "canonicalizes" | "Hate this word." | APPLIED | Covered by A6 (global replacement). |
| F3.3-2 | "5,000-8,000 tokens" | "Should provide word count, and what it would be comparable to in layman's terms" | SAFE_MECHANICAL | Add "≈1,500-2,500 words — about the length of a short magazine article." |
| F3.3-3 | "46 predicates constrained vocab" | "Interesting note on this. Letta takes a raw fact approach... Interesting." | SAFE_MECHANICAL | Add 1-sentence compare/contrast to Letta's raw-fact approach. |
| F3.3-4 | "three authored layers have distinct jobs" | "May want to give some insight on the prompting and how it's directed to pull this kind of information out" | AUTHOR_JUDGMENT | 1 paragraph per layer on prompting strategy. Level-of-detail needs review. |
| F3.3-5 | "$1 per subject" | "Need to give example of how much source text/token/characters/layman comparison and cost under $1" | SAFE_MECHANICAL | One comparison line ("~$1 per subject for ~50K words..."). |

### §3.4 Question Batteries + §3.4.1 Circularity Controls

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.4-1 | "forbids named-entity leakage" | "Can we verify this please" | APPLIED | Covered by P0-13 (audit, not wording). |
| F3.4-2 | "appendix" | Direct to specific appendix section. | APPLIED | Covered by A9. |
| F3.4.1-1 | Haiku vs GPT-5.4 question emphasis | "Would appreciate example of this" | AUTHOR_JUDGMENT | Add 1 example pair — example selection needs review. |
| F3.4.1-2 | "non-Anthropic response" vs "non-Haiku" | Inconsistent labeling. | SAFE_MECHANICAL | Pick one, apply globally. |
| F3.4.1-3 | (general appendix pointer) | Part of A9 sweep. | SAFE_MECHANICAL | Covered by A9. |

### §3.5 Experimental Conditions

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.5-1 | "C2a / C2c" labels | Need "no facts" / "static spec" specifier. | APPLIED | Covered by A2. |
| F3.5-2 | "C3 Retrieval + spec" | Table column addition for "Mem0 vs Mem0 + Spec" clarity. | APPLIED | Covered by B7. |
| F3.5-3 | "Native ingestion variant" | Fold into conditions table. | APPLIED | Covered by B7. |
| F3.5-4 | "Appendix C" | Reference determinism. | APPLIED | Covered by A9. |
| F3.5-5 | raw data path | "Need to go through a full organization run for the memory study repo... full traceability matrix" | DEFERRED | Repo work beyond v9; logged in TECH_DEBT. |

### §3.6 Response Models

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.6-1 | Haiku primary response model | "Is this fair to say, one could say a more capable model would be able to infer better from facts alone." | AUTHOR_JUDGMENT | Acknowledge counter-reading in 1 sentence w/ pointer to §4.5 Tier 2 replication. Wording needs review. |
| F3.6-2 | Tier 2 Sonnet + Gemini | Replaces earlier feedback request. | APPLIED | Already covered by Tier 2 replication write-up. |
| F3.6-3 | response-model prompt | "Is this prompt fair, should it not just be the straight up question" | AUTHOR_JUDGMENT | Short justifying paragraph; constant across conditions (no bias). Wording needs review. |
| F3.6-4 | "wrong spec (C2c)" in prompt variable | "Did it see wrong spec for the subject, and that's why it said this is the wrong specification?" | AUTHOR_JUDGMENT | Clarify anonymization from §3.3 — model sees no subject name attached. |

### §3.7 Evaluation suite

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F3.7-1 | Scoring rubric | "Good example here, not sure if should be adding something similar when I mentioned in earlier comments." | APPLIED | Covered by A3 — rubric becomes anchor-crossing illustration centerpiece. |
| F3.7.2-1 | Sonnet/Opus not on diagnostic suite | Confusing relationship to 5-judge primary. | AUTHOR_JUDGMENT | Rewrite explicitly: "Sonnet and Opus not tested on diagnostic suite; they join panel for inter-judge agreement only. 5-judge primary = Haiku + GPT-4o + GPT-5.4 + Sonnet + Opus." Confirm phrasing. |
| F3.7.2-2 | "The reasoning" paragraph start | Awkward. | SAFE_MECHANICAL | Merge with prior paragraph. |
| F3.7.2-3 | "C2a's mean Δ vs. C5 rises from" | Condition labels unclear. | APPLIED | Covered by A2. |
| F3.7.3-1 | "Ebers C5 → C2a" examples | "Should provide the actual examples for these" | AUTHOR_JUDGMENT | Add 1 example response per anchor crossing — example selection. |
| F3.7.4-1 | Specification-effect claim | "Need to be very explicit what the specification claim is exactly." | AUTHOR_JUDGMENT | Rewrite opening paragraph with formal claim. Needs wording review. |
| F3.7.5-1 | "Locked aggregation rule" | "Personally I don't know what a locked aggregation rule is" | SAFE_MECHANICAL | Open with one-sentence plain-English definition. |
| F3.7.6-1 | Mean abstention 1.27 | "This sounds like a floor calibration" | AUTHOR_JUDGMENT | Covered by P0-16 post-hoc. Acknowledge framing; needs Aarik's call on integration. |
| F3.7.6-2 | length correlation r = 0.26 | Too technical. | APPLIED | Covered by A1. |
| F3.7.6-3 | "probably" | Weak word. | APPLIED | Covered by A7. |
| F3.7-2 | (general) | Meta. | SAFE_MECHANICAL | Sequence ordering within §3.7; no action required. |

---

## §4 Results

### §4 opening + §4.1

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4-1 | Figure 5 caption | Condition deltas not clear at aggregate. | APPLIED | Covered by Part D. |
| F4.1-1 | Figure 4.1 caption | Need reader guide + 0-line. | APPLIED | Covered by Part D. |
| F4.1-2 | "No upward crossing 38.2%" | "Most interesting ones are multi jumps like 1-3,1-4,1-5 which make up >15% of responses" | APPLIED | Covered by P0-10 (multi-anchor-jump figure). |
| F4.1-3 | "These are not cherry-picked" | "Don't need to bring this up" | SAFE_MECHANICAL | Cut. |
| F4.1-4 | "specification corrects wrong predictions" | Not formally explored. | AUTHOR_JUDGMENT | Add short formal analysis OR flag as §8 future work — decision needed. |
| F4.1-5 | Example A | "This may be more interesting if just facts are provided vs specification + facts" | AUTHOR_JUDGMENT | Expand with intermediate facts-alone condition. Needs data pull + review. |
| F4.1-6 | Example C | Tracked inserts: "baseline" capitalization, plain version tracked delete. | SAFE_MECHANICAL | Accept tracked changes. |
| F4.1-7 | Example D (Hamerton) | "Need the raw example here" | AUTHOR_JUDGMENT | Add held-out passage + C5 and C4a responses. Selection needs review. |
| F4.1.1-1 | Franklin "because specification alone competes with strong pretraining" | "This is a theory" | SAFE_MECHANICAL | Acknowledge explicitly as interpretive claim; mark for future testing. |
| F4.1.2-1 | author wrong-spec gap | C3 rerun blocker. | APPLIED | Covered by P0-6 (derangement). |
| F4.1.2-2 | baseline-mediated improvement | Prefers fuller-facts baseline. | APPLIED | Covered by P0-14. |
| F4.1.2-3 | "None of the 40 responses got worse" | Headline finding. | APPLIED | Covered by Part E H6. |

### §4.2 Compression + §4.2.1 Question-Improvement Rate

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.2-1 | Figure 4.2 | Rework. | APPLIED | Covered by Part D. |
| F4.2-2 | "Compression: Structure vs. Raw Text" | "Please refer to benchmark examples from gamers nexus" | DEFERRED | Needs clarification from Aarik on GN-style presentation — what does this mean specifically? |
| F4.2-3 | "Context improves prediction" | "This should be a simple figure" | APPLIED | Part D — new bar chart (C5 → C2a → C4 → C8 → C4a → C9). |
| F4.2-4 | "compact specification captures" | "This should again be a simple figure" | APPLIED | Same as F4.2-3. |
| F4.2-5 | per-1K-tokens efficiency line | "This is interesting" — positive flag. | SAFE_MECHANICAL | Surface as bullet finding. |
| F4.2-6 | "Facts+spec = raw corpus at 2.45" | "This is pretty big" + "This needs to be more clear, raw corpus is usually 10x larger... huge compression win" | AUTHOR_JUDGMENT | Surface explicit 10× token ratio inline. Part of H4 headline. Wording to confirm. |
| F4.2.1-1 | §4.2.1 headline | "This is a headline finding" | APPLIED | Covered by Part E H3. |
| F4.2.1-2 | condition vs C5 baseline label | A2 gloss. | APPLIED | Covered by A2. |
| F4.2.1-3 | Figure 4.2.1 | Rework. | APPLIED | Covered by Part D. |
| F4.2.1-4 | pairwise comparison | "Needs to be explained" | SAFE_MECHANICAL | Plain-English intro paragraph. |
| F4.2.1-5 | spec vs corpus on 36.9% | "Maybe a segmented bar chart would make this easier" | DEFERRED | Bar chart addition — figure task, not wording. |
| F4.2.1-6 | failure modes for rate metric | "Can we counter any of these failure modes now?" | AUTHOR_JUDGMENT | Add counterarguments where possible. Needs content decision. |
| F4.2.1-7 | tiny-gain inflation | "We should include some controls around this" | SAFE_MECHANICAL | Surface median magnitude more prominently. |
| F4.2.1-8 | Hamerton example framing | "This is a huge finding, need to frame this as, compressing source corpus, pulls out information that the model itself does not seem to infer" | AUTHOR_JUDGMENT | Rewrite framing paragraph — needs Aarik's exact phrasing. |
| F4.2.1-9 | Ebers example | "Would want to see facts + spec, and memory system + spec as well" | DEFERRED | Requires additional comparison data pulls. |
| F4.2.1-10 | (general) Gamers Nexus reference | Clarify with Aarik. | DEFERRED | Same as F4.2-2. |

### §4.3 Mechanism + wrong-spec examples

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.3-1 | Figure 6 caption | Need spec-similarity analysis (C5). | APPLIED | Covered by Part D + P0-7. |
| F4.3-2 | Figure 4 | Explicit approval. | APPLIED | Keep. Part E H1 already covers. |
| F4.3-3 | C2c v1 labeling in figure | Not visible in figure. | SAFE_MECHANICAL | Fix caption. |
| F4.3-4 | "gap is the content effect" | Layman. | APPLIED | Covered by A1. |
| F4.3-5 | "coincidentally correct" | Term needs expansion. | SAFE_MECHANICAL | Add 1-2 sentences defining. |
| F4.3-6 | tag-citation 78.6% vs 50.0% | Headline (H7) + C4 rerun. | APPLIED | Covered by Part E H7 + P0-4. |
| F4.3-7 | "almost certainly Babur" example | "We don't talk too much about the brief itself" | AUTHOR_JUDGMENT | Add 1 paragraph in §3.3 on composed-brief step. Content decision. |
| F4.3-8 | "36.5% attempted to apply mismatched" | Post-hoc by question category. | APPLIED | Covered by P0-8 / C6. |
| F4.3-9 | "detection asymmetry" paragraph | Needs layman version + possible Hedging Behavior section. | APPLIED | Covered by B9 (new §4.3.x Hedging Behavior). |
| F4.3-10 | hedging transition rule | Headline (H1). | APPLIED | Part E H1. |
| F4.3-11 | per-question matched comparison | Approved. | APPLIED | Keep. |
| F4.3-12 | wrong-spec §4.1 extend | Approved. | APPLIED | Keep. |
| F4.3-13 | Example A wrong-spec (Ebers Q7) tracked insert | Tracked insert. | SAFE_MECHANICAL | Accept. |
| F4.3-14 | Example A scoring text | "Should be at the top... simplified... correct/wrong/baseline" | AUTHOR_JUDGMENT | Restructure template: (1) headline scores, (2) anchors, (3) response, (4) reading. Template needs review. |
| F4.3-15 | Example A "detected the mismatch" | "How, what was it detecting, from the question?" | SAFE_MECHANICAL | Add detection trace in Reading section. |
| F4.3-16 | Example B em-dash | A4 sweep. | APPLIED | Covered by A4. |
| F4.3-17 | Example B framework convergence | Interesting interpretation. | AUTHOR_JUDGMENT | Add 1 paragraph on convergence finding. Content decision. |
| F4.3-18 | Example B "the convergence" | Repeat. | APPLIED | Same as F4.3-17. |
| F4.3-19 | Example C anchor list truncation | "Have these been truncated, they seem very short" | SAFE_MECHANICAL | Verify raw anchors — restore if truncated. |
| F4.3-20 | Example C "16th-century Spanish conquest" | Interesting brief-detail finding. | AUTHOR_JUDGMENT | Add paragraph on brief providing implicit subject-type guards. |
| F4.3-21 | Example C "major finding" flag | Same. | APPLIED | Same as F4.3-20. |
| F4.3-22 | Example C "longer notes = substantial edits" | Meta-instruction for Aarik's comments. | APPLIED | Honored in this triage; no paper action. |
| F4.3-23 | summary-of-three-examples table | "Split per-example + keep summary" | DEFERRED | Restructure — needs structural review. |
| F4.3-24 | (general) per-example template | Same as F4.3-14. | DEFERRED | Template decision. |

### §4.4 Memory-System Composition + Supermemory subsection

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.4-1 | heading | Absorb §4.6, §4.7, Supermemory subsection. | APPLIED | Covered by B1. |
| F4.4-2 | Figure 7 | Rework. | APPLIED | Part D. |
| F4.4-3 | Figure 7 cross-slice analysis | "May be certain autobiographies do better?" | AUTHOR_JUDGMENT | Flag as follow-up / short post-hoc. |
| F4.4-4 | Figure 3 | Keep + interpretation. | APPLIED | Part D (KEEP + paragraph). |
| F4.4-5 | "Subj + / 14" column | Rename column. | SAFE_MECHANICAL | Rename. |
| F4.4-6 | Wilcoxon on Mem0/Supermemory/BL | "Why not significant?" | SAFE_MECHANICAL | Add 1 sentence: underpowered at n=9. |
| F4.4-7 | "−0.03" | "Interesting if the spec doesn't help meaningfully, it doesn't really hurt either?" | SAFE_MECHANICAL | Surface observation in prose. |
| F4.4-8 | Supermemory native failures | C2 rerun. | APPLIED | Covered by P0-2. |
| F4.4-9 | Zep temporal graph | "May be due to zeps architecture" | AUTHOR_JUDGMENT | Add 1 paragraph hypothesizing mechanism. Content needs Aarik's architectural take. |
| F4.4-10 | BL "smallest positive" | "Point is local memory capabilities... recall is a horrible metric" | AUTHOR_JUDGMENT | Reframe Base Layer substrate paragraph. Strategic framing — Aarik review. |
| F4.4-11 | Supermemory subsection (fold) | Cover Examples 1-4. | APPLIED | Covered by B1. |
| F4.4-12 | Fukuzawa Q26 "gay quarters" | "This reads like it was trained on the entire corpus, can you confirm" | DEFERRED | Data audit (train-half vs full corpus ingestion) — not wording. |
| F4.4-13 | Yung Wing Q5 formatting | Question/ground truth each need own line. | SAFE_MECHANICAL | Fix formatting. |
| F4.4-14 | Zitkala-Sa Q18 "I should not do it" | H8 + C7. | APPLIED | Covered by Part E H8 + P0-5. |
| F4.4-15 | Zitkala-Sa Q18 section 7 link | Cross-link. | APPLIED | Covered by B2. |
| F4.4-16 | Zitkala-Sa Q18 safety-layer commercial framing | "Can literally pass unsafe liability to them" | DEFERRED | Not paper-body content — strategic/commercial. |
| F4.4-17 | spec reframing behavior | Interesting. | SAFE_MECHANICAL | Add 1 paragraph. |
| F4.4-18 | 3 mechanisms layman | A1 sweep. | APPLIED | Covered by A1. |
| F4.4-19 | post-hoc question categories | P0-8. | APPLIED | Covered by C6/P0-8. |
| F4.4-20 | "epistemic honesty" → §8 | Flag in §8. | AUTHOR_JUDGMENT | §8 future-work addition. |
| F4.4-21 | "A note on the earlier hedging hypothesis" | "Hedging was found during, not before" | SAFE_MECHANICAL | Rewrite with accurate timing. |
| F4.4.1-1 | Letta stateful section opening | Heavy; needs layman. | DEFERRED | Blocked on P0-1 (Letta full-stack rerun). |

### §4.5 Robustness + §4.5.1 / §4.5.2 / §4.5.3

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.5-1 | §4.5 order (move to end) | B1 restructure. | APPLIED | Covered by B1. |
| F4.5-2 | "main-study batteries were generated by Claude Sonnet" | "Was it sonnet or haiku, this may be incorrect information" | APPLIED | Covered by P0-3 (fact check). |
| F4.5.1-1 | Figure 11 | Consider drop. | APPLIED | Part D. |
| F4.5.1-2 | Zitkala-Sa × Sonnet +1.4 paragraph | "I don't understand. Needs to be more layman" | AUTHOR_JUDGMENT | Rewrite one-non-matching-cell paragraph in plain English. |
| F4.5.2-1 | Gemini severity technical | A1 sweep. | APPLIED | Covered by A1. |
| F4.5.2-2 | lower-bound effect size framing | "Not a fan of this technicality" | SAFE_MECHANICAL | Drop upper/lower-bound framing. |
| F4.5.3-1 | not-addressed section back-ref | "We talk about LLM as judge concerns in intro, and design, at that we reference the specific paper... But then it's not referenced here" | SAFE_MECHANICAL | Back-reference Zheng et al. explicitly. |
| F4.5.3-2 | "biases that favor spec-tag quoting" | "That's a mouthful and a strange claim" | AUTHOR_JUDGMENT | Rewrite more plainly. |
| F4.5.3-3 | "LLMs" spelled out | A8 sweep. | APPLIED | Covered by A8. |

### §4.6 Interpretation vs. Recall

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.6-1 | §4.6 fold into §4.4 | B1 restructure. | APPLIED | Covered by B1. |
| F4.6-2 | Pattern 1 "interpretive pattern" | Key word. | SAFE_MECHANICAL | Keep + define clearly on first use. |
| F4.6-3 | Pattern 2 "over-theorizing = anxiety for humans" | Analogy note — do not add to paper. | APPLIED | No action. |
| F4.6-4 | Pattern 3 em-dash | A4 sweep. | APPLIED | Covered by A4. |
| F4.6-5 | pattern examples | "Likely should put this in the appendix" + roll into §4.4. | APPLIED | Covered by B1 + appendix move. |
| F4.6-6 | pattern-frequency shifts | Prose form + appendix breakdown. | AUTHOR_JUDGMENT | Prose rewrite, detail to appendix. Structure decision. |
| F4.6-7 | Keckley Q21 cross-substrate | Fold into §4.4. | APPLIED | Covered by B1. |
| F4.6-8 | measurement implications | Roll into §4.4 + question analysis. | APPLIED | Covered by B1 + C6. |

### §4.7 Architectural Convergence + §4.8 Scaling

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F4.7-1 | §4.7 fold + C1 rerun blocker | B1 + P0-1. | APPLIED | Covered by B1 + P0-1. |
| F4.7-2 | Letta memory-block growth figure | Part D + C1. | APPLIED | Part D + P0-1. |
| F4.7-3 | full-stack vs unified-brief | C1. | APPLIED | Resolved (P0-1 confirmed paper was already correct). |
| F4.8-1 | move out of results | B1. | APPLIED | Covered by B1 (→ §5.5 Practical Implications per Mistral modification). |

---

## §5 Discussion / §6 Limitations / §7 Safety / §8 Future Work

(Aarik deferred detailed review, but scattered comments are here.)

| # | Line quote | Author's annotation | Classification | Status note |
|---|---|---|---|---|
| F5.1-1 | "how do we improve human-AI interactions" | First mention. | AUTHOR_JUDGMENT | Weave framing through §1-§4 OR open §5 with it explicitly as unifying thread. Structural decision needed. |
| F5.1-2 | "empirical results may change" | Self-note. | APPLIED | Blocked on §4 completion — rerun all §5.1 bullets then. |
| F5.1-3 | gradient statistics | A1 sweep. | APPLIED | Covered by A1. |
| F5.1-4 | "composes additively" | Layman. | APPLIED | Covered by A1. |
| F5.1-5 | composes-additively null comment | Empty comment — likely content expansion. | AUTHOR_JUDGMENT | Flag for walk-through — needs Aarik clarification. |
| F5.2-F5.4-1 | §5.2-§5.4 content | "Most content belongs in §2." | APPLIED | Covered by B3. |
| F5-reframe | §5 discussion reframe as extension | B3 + B10. | APPLIED | Covered by B3 + B10 (Anti-Pattern definition). |
| F5.2-1 | "canonical life events" | Relates to prior paragraph. | SAFE_MECHANICAL | Cross-link in v9. |
| F6-1 | §6 Limitations | Deferred. | DEFERRED | Not touching until structural decisions land. |
| F7-1 | §7 Safety | Roll into §5. | APPLIED | Covered by B2. |
| F8-1 | §8 Future Work | Deferred. | AUTHOR_JUDGMENT | Consolidate items flagged throughout (C6, C7, A11, Zep hypothesis, hedging-behavior question, question-category post-hoc). Scope decision. |

---

## Walking guide for Aarik

**Priority order when walking this list with Aarik:**

1. **AUTHOR_JUDGMENT items (~44 rows)** — the critical-path walk. Each needs a call on content or framing. Recommend §-by-§ top-to-bottom.
2. **DEFERRED items (~10 rows)** — for each, decide: post-v9, drop, or promote to AUTHOR_JUDGMENT. Most are waiting on data/structural decisions; a few (Gamers Nexus reference, Fukuzawa Q26 ingestion audit) are one-answer resolutions.
3. **SAFE_MECHANICAL items (~49 rows)** — Part F batch agent applies these tonight. Aarik doesn't need to walk these individually; spot-check post-hoc against `_part_f_batch_report.md`.
4. **APPLIED items (~59 rows)** — already absorbed by A-E sweeps. No action needed. Listed here only so the accounting is complete and nothing appears "dropped."

**Estimated walk time:** 15-20 minutes if focusing on AUTHOR_JUDGMENT + DEFERRED rows. Full top-to-bottom walk: ~40 minutes.
