# Mem0, Letta, Zep, Supermemory: State of the Art Is Missing the Art

*A 3,156-token behavioral specification outpredicts four funded SOTA memory systems on held-out behavioral prediction. Adding it to any of them makes them better.*

---

## The Industry Is Optimizing for the Wrong Thing

Every AI memory system ships the same pitch: "Your AI will remember everything." Mem0 (backed by a16z, $23.5M raised). Letta, formerly MemGPT (backed by Felicis and a16z, ICLR paper). Supermemory (claims state-of-the-art on LongMemEval at 85.2%). Zep (production knowledge graph memory). They compete on the same axis — store more facts, retrieve them faster, score higher on recall benchmarks.

The benchmarks reward this. LongMemEval asks: "What did the user say about X in conversation 47?" The system searches its memory, finds the fact, returns it. Score: correct. All four systems pass. Everyone scores 85%+.

But recall is not understanding. Remembering what someone said is not the same as understanding why they do what they do. When an AI agent needs to act on behalf of a person — make a decision, anticipate a reaction, navigate a tradeoff the person never explicitly discussed — perfect recall of past conversations is necessary but not sufficient. The agent needs a model of how this person reasons.

No existing benchmark tests this. LongMemEval tests whether the system stored and found a fact. We propose that memory for AI agents isn't about recall at all — it's about reasoning. An agent that remembers everything you said but can't reason about what you'd do next isn't personalized. It's a search engine over your transcripts.

If memory is reasoning, then the right primitive isn't a fact store. It's a compressed model of how someone thinks. That's what a behavioral specification is, and that's what we tested.

## What Is a Behavioral Specification?

Memory systems store facts: "User prefers morning meetings." "User mentioned they have two kids." "User said they dislike cold outreach."

A behavioral specification stores patterns: how someone reasons through tradeoffs, what they prioritize under pressure, where they'll compromise and where they won't. How they think instead of what they said.

- **Memory system stores:** "Hamerton's father was violent and alcoholic"
- **Spec stores:** "This person evaluates authority figures on two simultaneous ledgers — virtue and failure — and refuses to collapse them into a single verdict"

The first is a retrievable fact. The second is a behavioral pattern compressed from dozens of facts. You can't retrieve it because it was never stated — it was extracted, compressed, and distilled.

3,156 tokens. Generated from 25,000 words of source text. 8:1 compression ratio. It doesn't store facts. It stores the structure underneath them.

## Why We Ran This Study

If all memory systems ultimately retrieve facts and inject them into context, and they all score 85%+ on recall benchmarks, the question becomes: does the architecture matter, or does it all collapse to the same behavior? And if a compressed behavioral spec changes how the model uses facts, is that a fundamentally different kind of information than what memory systems provide?

We tested this directly. Four funded SOTA memory systems. One behavioral specification. Same source material. Same questions. Held-out ground truth from chapters none of them had seen.

## What We Tested

We fed 462 facts from an obscure Victorian autobiography into all four memory systems and generated a behavioral specification from the same text using Base Layer's compression pipeline. Then we asked 80 questions — including 39 behavioral prediction questions with ground truth from chapters the systems and the spec had never seen.

The subject, Philip Gilbert Hamerton (1834-1894), was chosen specifically because large language models have near-zero knowledge of him. The baseline condition — the model with no facts and no spec — scored 1.41 out of 5. It doesn't know this person. Any performance above baseline comes from the facts or the spec, not the model's pre-training.

Every system received the same 462 facts. Every condition received the same questions. The only variable was what context the model had when answering.

## The Data

Thirteen conditions. Eighty questions. 1,036 total responses. Every response logged with the exact facts retrieved, the full system prompt, the raw model output, and token counts. Nothing summarized, nothing discarded.

| Condition | What the model sees | n |
|---|---|---|
| C1 (×4 systems) | Facts retrieved by Mem0, Letta, Supermemory, or Zep | 80 each |
| C2a — Spec only | Behavioral specification, no facts | 80 |
| C2c — Wrong spec | Benjamin Franklin's spec (mismatched subject) | 80 |
| C3 (×4 systems) | Behavioral specification + each system's retrieved facts | 80 each |
| C4 — Fact dump | All 462 facts loaded into context | 80 |
| C5 — Baseline | Nothing. Just the question. | 80 |
| C6 — Random facts | 10 randomly selected facts per question | 80 |

Questions span five tiers: factual recall (10), inferential synthesis (10), behavioral prediction (40), adversarial abstention (10), and boundary probing (10). The battery is deliberately bottom-heavy on behavioral prediction — that's where divergence between recall and reasoning lives.

All prompts are identical across conditions except for the injected context. No condition was told "say so if you don't know." No condition was given the subject's name in the system prompt. The spec conditions say "your user" — the model doesn't know whose spec it has.

## What the Raw Data Shows (No Judge Required)

Before any LLM scores a response, the data already tells a story.

**Response volume.** The spec changes how much the model has to say. Conditions with the spec (C3) produce 2.07-2.25x the output tokens of the same memory system without the spec (C1). Consistent across all four systems. The model isn't padding — it's reasoning through a framework that gives it more to work with.

| Condition | Avg output tokens |
|---|---|
| C3 (spec + facts) | 494-565 |
| C2a (spec only) | 341 |
| C4 (all facts) | 311 |
| C2c (wrong spec) | 274 |
| C1 (facts only) | 244-253 |
| C6 (random) | 192 |
| C5 (baseline) | 163 |

**Refusal rate.** On the 39 behavioral prediction questions, memory systems alone refuse to answer — hedging with "insufficient information" — 51% of the time. Add the spec, and refusal drops to 31%. The spec gives the model enough structure to attempt a prediction where raw facts leave it stuck.

When C1 does answer, it scores well (avg 3.7). The problem isn't that memory systems give bad answers. It's that they give no answer half the time. The spec unlocks the other half.

**Retrieval disagreement.** Four systems, same 462 facts, same question. How often do they agree on the most important fact?

- All 3 embedding systems agree on top-1: **8%**
- 2 of 3 agree: **27%**
- All 3 disagree: **65%**
- Zep matches any embedding system: **8%**

This is mechanical. No judge, no threshold, just: did they return the same top fact? Two-thirds of the time, three SOTA systems looking at identical data retrieve entirely different facts for the same question.

**Adversarial calibration.** Ten unanswerable questions — facts the corpus simply doesn't contain. Every condition correctly abstained except one: C4 (all 462 facts dumped into context) fabricated answers on 2 out of 10. More facts produced more overconfidence. The spec, despite being a compressed interpretation of those same facts, abstained correctly on all 10.

**Fact diversity.** Across 80 questions, how many unique top-1 facts does each system surface?

| System | Unique top-1 facts |
|---|---|
| Supermemory | 67 |
| Letta | 59 |
| Mem0 | 57 |
| Zep | 41 |

Zep's knowledge graph retrieves the same father-property-settlement fact for 39% of all questions — a graph traversal bias toward high-connectivity nodes regardless of query relevance.

## How We Measured Prediction Accuracy

Each behavioral prediction question was designed backward from a specific passage in the held-out chapters — chapters the model, the memory systems, and the spec never saw. We extracted the passage describing what Hamerton actually did, then wrote a question that could only be answered using information from the training chapters.

For example: the training chapters establish Hamerton's love of wild Scottish moors, his comfort with solitude, and his indifference to social convention. The held-out chapter reveals he chose to encamp alone on remote Highland hills for a month, despite everyone considering him "extremely eccentric." The question asks whether he would make that choice. The held-out passage is the ground truth.

Each condition's response was scored 1-5 by independent LLM judges against the held-out passage:

- **5** — Predicts the specific outcome or behavior described in the ground truth
- **4** — Predicts the general direction correctly with some specifics
- **3** — Captures the right domain but not the specific outcome
- **2** — Addresses the topic but predicts incorrectly
- **1** — Refuses to answer or is completely off-base

The judges never see each other's scores. They see only the held-out passage and the response. Multiple judges scored every response independently — their agreement validates that the scores are measuring something real, not artifacts of one model's preferences.

[CHART 1: Horizontal bar chart — all 13 conditions ranked by prediction accuracy]

## The Spec Doesn't Replace Memory. It Completes It.

The strongest condition wasn't the spec alone. It was the spec combined with each memory system's retrieved facts. Adding the behavioral specification to Letta's retrieval improved prediction accuracy from 2.40 to 3.13 (4-judge average). Adding it to Mem0 improved it from 2.63 to 3.01. Adding it to Zep — the weakest retriever — improved it from 1.64 to 2.69. A 64% improvement.

Every memory system got better with the spec. No exceptions.

This is statistically significant (p=0.012, sign test). Not a trend. Not a suggestion. Sixteen questions improved, four degraded, nineteen unchanged. Five independent judges — Haiku, Sonnet 4.6, Opus, GPT-4o, and Gemini 2.5 Flash — scored every response blind and agreed on the ranking (pairwise Spearman rho 0.89-0.98 across all judge pairs). Three AI providers (Anthropic, OpenAI, Google) independently confirmed the same result.

The spec alone, with zero retrieved facts, scored 2.48 (4-judge average). That's higher than most memory systems operating alone. But this comparison is not statistically significant at our sample size (p=0.83) — the spec needs facts to reason on. It's a multiplier, not a substitute. What it changes is how those facts get used.

To be precise about what the data supports and what it doesn't:
- **Significant (p=0.012):** Spec + facts beats facts alone across all four memory systems
- **Suggestive but not significant:** Spec alone beats memory systems alone
- **Confirmed by all judges:** The ranking is stable across five models from three providers
- **Not tested:** Whether the spec's effect generalizes across response models (all responses generated by Haiku)

## Memory Systems Either Hit or Miss. The Spec Creates a Gradient.

This is the most important finding in the study, and the averages hide it.

[CHART 2: Side-by-side histograms — C1_mem0 bimodal vs C3_mem0 gradient]

When Mem0 retrieves facts without the spec, it scores a 1 (complete failure) on 16 out of 39 behavioral questions. It scores a 5 (accurate prediction) on 11. Almost nothing in between. It either retrieves the right facts and succeeds, or retrieves the wrong facts and fails completely. No graceful degradation.

Add the spec, and the ones collapse from 16 to 3. The fives stay at 11. The spec didn't make the good predictions better — it rescued the bad ones. Thirteen questions moved from catastrophic failure to partial or full prediction.

This is not an incremental quality improvement. It is a categorical shift in the failure mode. Without the spec, memory systems produce a bimodal distribution — they either work or they completely fail. With the spec, the failure mode changes from total miss to partial hit. The spec provides a reasoning framework that lets the model do something productive even when the retrieved facts aren't ideal. Without it, wrong facts produce wrong answers. With it, wrong facts still get interpreted through a behavioral lens that constrains the response toward plausibility.

## They Don't Even Agree With Each Other

Here is what four state-of-the-art memory systems retrieve when asked the same question about the same person from the same 462 facts:

[CHART 3: Heatmap — pairwise top-1 agreement]

65% of the time, all three embedding-based systems (Mem0, Letta, Supermemory) retrieve different top-1 facts. They agree on the most relevant fact only 8% of the time. Zep's knowledge graph diverges even further — it matches any embedding system's top-1 on just 8% of questions, and retrieves the same father-property-settlement fact for 39% of the entire battery.

These systems score 85%+ on LongMemEval. They all pass the recall benchmark. But "retrieve the right fact" and "retrieve the most relevant fact for this question" are different problems. LongMemEval tests the first. Our study tests the second. On the second, they can't even agree.

## Compression Beats Volume

[CHART 4: Size comparison — 462 facts vs 3,156-token spec, equal prediction scores]

All 462 facts loaded into context (C4) scored 2.74. The 3,156-token spec scored 2.77. Equal predictive power, roughly 10x size difference.

More facts did not produce better predictions. In fact, more facts produced worse calibration — the fact-dump condition was the only one that fabricated answers on unanswerable questions (2 out of 10 adversarial questions). Every other condition, including the spec, correctly abstained.

More information created more overconfidence. The spec, despite containing less information, produced better calibration.

## A Wrong Map Is Better Than No Map

[CHART 5: Three bars — no spec, wrong spec, right spec]

We ran a control condition: Benjamin Franklin's behavioral specification applied to Hamerton's questions. The model was told "this is a behavioral specification describing your user" — it couldn't detect the mismatch.

The wrong spec scored 2.21. The correct spec scored 2.77. The baseline with no spec scored 1.41.

A wrong behavioral framework still outperforms no framework by 57%. But the right framework outperforms the wrong one by 25%. The cost of having no spec is catastrophic. The cost of having the wrong spec is moderate. The value of having the right spec is clear.

## What This Means

Every major AI memory system optimizes for the same objective: recall. Store more, retrieve faster, rank better. They compete on LongMemEval scores and ingestion speed and token limits.

None of them optimize for what actually matters when an AI agent needs to act on behalf of a person: behavioral prediction. Can the agent anticipate what you would do, not just remember what you said? Can it reason about your values when the specific scenario was never discussed? Can it degrade gracefully when the retrieved facts aren't sufficient?

The behavioral specification is the missing layer. It doesn't replace memory systems. It makes every one of them better. It provides the reasoning framework that transforms fact retrieval into behavioral prediction.

State of the art in recall is not state of the art in alignment. The art is missing.

## Raw Text Doesn't Work Either

We ran one more condition: dump the entire training corpus — 25,000 words of raw autobiography — directly into the model's context window. No extraction, no spec, no memory system. Just the book.

The raw corpus scored 2.31. The spec plus 10 retrieved facts scored 3.01. A 3,000-token spec with 10 facts beats 25,000 words of raw text by 30%. That's an 18:1 compression ratio producing superior predictive performance.

This is not just a quality finding. It's an economics finding. Every deployment of AI agents with memory has a context window budget. The spec delivers better predictions in a fraction of the token cost. 3,000 tokens instead of 25,000. That difference compounds across millions of users.

The problem isn't information availability. The model has everything it needs in the raw text. The problem is extractability — the model cannot use 25,000 words of unstructured autobiography to predict behavior. The spec tells it what to look for and how to reason. Compression isn't about saving tokens. It's about structuring information into a usable form.

And when we gave the model all 462 facts plus the spec (C4a), it scored 3.23 — the highest of any condition. The spec helps even with complete information. It's not fixing bad retrieval. It's providing the reasoning framework that transforms facts into predictions.

## The Known-Figure Test

Does any of this matter if the model already knows the person?

We ran the entire study again on Benjamin Franklin. Same methodology, same memory systems, same question design. Franklin is one of the most famous people in LLM training data. His autobiography is almost certainly memorized by every major model.

The result: the model with no context at all — no facts, no spec, not even told who the subject is — scored 4.10 out of 5. It recognized Franklin from the behavioral patterns in the questions alone. Every condition we gave it — spec, facts, memory systems — scored lower than the bare baseline.

The spec hurts when the model already knows.

| Subject | Model's Prior Knowledge | Baseline | Spec + Facts | Effect |
|---|---|---|---|---|
| Hamerton (unknown) | None | 1.37 | 3.13 | **+128%** |
| Franklin (known) | Deep | 3.99 | 3.83 | **-4%** |

This isn't a failure. It's the use case definition. Every real user is Hamerton, not Franklin. Your AI agent doesn't know your customers, your team, your users. It has baseline 1.37 for all of them. The spec exists for the 99.99% of people who aren't famous enough to be in the training data — which is everyone.

The model has no idea who you are. And that's the problem the behavioral specification solves.

## Methodology

- **Corpus:** Philip Gilbert Hamerton, *An Autobiography* (1834-1858), Project Gutenberg. Chapters 1-10 as training, 11-32 as held-out validation.
- **Systems:** Mem0 (mem0ai 1.0.11), Letta (letta-client 1.10.2), Supermemory (supermemory 3.32.0), Zep (zep-cloud 3.20.0)
- **Conditions (Hamerton):** 15 total — 4 memory systems alone (C1), spec alone (C2a), wrong spec (C2c), spec + each memory system (C3), all facts (C4), all facts + spec (C4a), baseline (C5), random facts (C6), raw corpus in context (C9).
- **Conditions (Franklin):** 12 total — same as above minus Letta/Zep, plus named baseline (C7: model told "this is Benjamin Franklin").
- **Questions:** 80 per subject across 5 tiers. 39/40 behavioral prediction questions designed backward from held-out chapters with extracted ground truth passages.
- **Judges:** 5 independent LLM judges from 3 providers: Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o (OpenAI), Gemini 2.5 Flash (Google). Pairwise Spearman rho 0.89-0.98. All judges agree on condition rankings.
- **Prompt parity:** All conditions received identical prompts. No condition was coached to abstain or answer. No condition revealed the subject's name (except C7).
- **All data, scripts, and results are public.** [Link to repo]. [Link to interactive explorer]. Every claim in this post traces to raw data you can verify.

---

*We propose Base Layer — Behavioral Alignment Infrastructure for AI. Base Layer builds behavioral specifications — compressed documents that encode how a person thinks, decides, and acts. The pipeline extracts behavioral patterns from text, compresses them into a portable spec, and serves them to any AI system. This study is the first empirical comparison of behavioral compression against SOTA memory retrieval.*

*[Link to interactive data explorer]*
*[Link to study repository]*
*[Link to ArXiv preprint]*
