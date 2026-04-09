# Beyond Recall

*What makes memory useful isn't what you remember — it's how you reason about what you remember.*

---

Your AI doesn't know you.

Not in the way that matters. It might remember that you prefer morning meetings, that you have two kids, that you once said you dislike cold outreach. It stores these as facts. It retrieves them when something in your next message matches. And the industry calls this memory.

Mem0 raised $23.5 million to do it. Letta has an ICLR paper and backing from Felicis and a16z. Supermemory claims 85.2% on LongMemEval. Zep builds production knowledge graphs. They all compete on the same axis: store more, retrieve faster, recall better.

But recall is only part of memory. The part that's missing — the part that makes memory matter — is interpretation. How does this person reason about the facts of their experience? What significance do those facts carry for them specifically? A fact that someone moved to London means nothing on its own. Its meaning depends entirely on whether that person sees physical environments as either hostile or generative to thought, whether they experience crowded spaces as intrusions or opportunities, whether solitude is a deprivation or a requirement. The significance lives in the pattern, not in the fact.

Current memory systems store facts. They don't capture how someone makes sense of their facts. And that gap — between recall and understanding — is where every personalization system breaks down.

## What We Tested

We took four funded state-of-the-art (SOTA) memory systems and tested whether adding a behavioral specification — a compressed model of how someone thinks — changes the accuracy of the AI's representation of a person. Not its recall. Its understanding.

The subject: Philip Gilbert Hamerton (1834-1894), a Victorian art critic that large language models know almost nothing about. Baseline score — the model with no context at all — was 1.41 out of 5. The model doesn't know this person. Any improvement comes from what we give it, not what it already has.

We fed 462 facts from Hamerton's autobiography into all four memory systems and generated a behavioral specification from the same text. Then we asked 80 questions — including 40 where we had ground truth from chapters that neither the memory systems nor the spec had ever seen.

The test: if the spec gives the AI a more accurate representation of how Hamerton thinks, the AI should be able to anticipate how he actually responded in scenarios it has never encountered. Not because it's predicting the future — because it genuinely understands how he reasons in the present.

## What a Behavioral Specification Is

Memory systems store facts: "User prefers morning meetings." "User's father was violent and alcoholic." "User mentioned he likes painting."

A behavioral specification stores something different: the interpretive patterns that give those facts their significance.

- **A memory system stores:** "Hamerton's father was violent and alcoholic"
- **The spec stores:** "This person evaluates authority figures on two simultaneous ledgers — virtue and failure — and refuses to collapse them into a single verdict"

The first is a retrievable fact. The second was never stated — it was extracted from dozens of facts, compressed, and distilled into a pattern. That pattern is what lets an AI reason about how Hamerton would respond to a new authority figure, a new teacher, a new conflict with someone in power. The fact tells you what happened. The pattern tells you how he makes sense of what happened.

3,000-5,000 tokens. Generated from 25,000 words of source text. It doesn't store facts. It stores how someone reasons about their facts.

## The Results

Every memory system got better with the spec. No exceptions.

| Condition | Score | What it shows |
|---|---|---|
| Spec + Mem0 facts | 2.97 | Spec improves Mem0 by +50% |
| Spec + Supermemory facts | 2.85 | Spec improves Supermemory by +36% |
| Spec + Letta facts | 3.13 | Spec improves Letta by +30% |
| Spec + Zep facts | 2.69 | Spec improves Zep by +64% |
| All 462 facts + spec | 3.23 | Best overall — spec helps even with complete information |
| All 462 facts, no spec | 2.69 | Facts alone, no interpretive framework |
| Spec only, no facts | 2.72 | Spec alone matches all-facts condition |
| Baseline (nothing) | 1.41 | Model doesn't know Hamerton |

This is statistically significant. Sign test: 16 wins, 4 losses, 19 ties (p=0.012). Cohen's d=1.21 (large effect). Five independent judges from three AI providers — Anthropic, OpenAI, Google — scored every response blind and agreed on the ranking (pairwise Spearman rho 0.89-0.98).

The spec doesn't replace memory systems. It completes them. Recall is real and necessary. But recall without interpretation is inert — the AI has the facts but doesn't know what they mean to this person. The spec provides the interpretive framework that makes recalled facts actionable.

## What the Raw Data Shows Before Any Judge Scores

The effect isn't subtle. Before any LLM scores a response, the data already tells the story.

**The spec changes how the model engages.** Conditions with the spec produce 2x the output tokens of the same memory system without it. The model isn't padding — it has a framework to reason through, and it uses it.

**The spec rescues failures.** Without the spec, Mem0 scores a 1 (complete failure) on 16 out of 40 behavioral questions. It scores a 5 on 11. Almost nothing in between — it either retrieves the right fact and succeeds, or retrieves the wrong fact and fails completely. Add the spec, and the ones collapse from 16 to 3. The fives stay at 11. Thirteen questions moved from catastrophic failure to partial or full accuracy. The spec didn't improve the good answers. It rescued the bad ones.

**Memory systems can't agree on what's relevant.** Four systems, same 462 facts, same question. How often do they agree on the most relevant fact? 65% of the time, all three embedding systems retrieve entirely different top-1 facts. They agree only 8% of the time. They all pass LongMemEval. But "can you find a fact" and "can you find the right fact for this question" are different problems. On the second, they can't even agree with each other.

## Only the Person Can Dictate What a Fact Means

We gave the model the entire training corpus — 25,000 words of raw autobiography — directly in context. No extraction, no spec, no memory system. Just the book.

It scored 2.31. The spec plus 10 retrieved facts scored 2.97. A 5,000-token spec with 10 facts beats 25,000 words of raw text.

This isn't an efficiency finding. It's a finding about the nature of memory itself. A fact can carry significance on its own — "his father was violent" means something in isolation. But when an AI is reasoning about a specific person, only that person can dictate whether a fact is significant to them, and how. The same fact about a violent father produces entirely different behavioral patterns depending on whether the person processes authority through forgiveness or through permanent judgment. The fact is the same. The significance is personal.

The raw text contains every fact the specification was derived from. The model has all the information. But it cannot determine, from unstructured text alone, which facts this person weighs heavily, what those facts mean in the context of their values, or how they would apply those interpretive patterns to something they haven't encountered.

The spec makes interpretation explicit. It tells the model not just what happened to someone, but how they make sense of what happened. That's the difference between having someone's facts and having a representation of how they think.

And when we gave the model all 462 facts *plus* the spec, it scored 3.23 — the highest of any condition. The spec helps even with complete information. More facts alone don't produce better understanding. The interpretive framework does.

## The Known-Figure Test

We ran the entire study on Benjamin Franklin. Same methodology, same questions. Franklin is one of the most documented figures in LLM training data.

The model scored 4.10 out of 5 with no context at all. It already has, from pretraining, a representation of how Franklin thinks — his values, his pragmatism, his approach to conflict. Every condition we added — spec, facts, memory systems — scored lower than the bare baseline.

| Subject | Baseline | Spec + Facts | Effect |
|---|---|---|---|
| Hamerton (unknown) | 1.41 | 2.97 | **+111%** |
| Franklin (known) | 4.10 | 3.83 | **-4%** |

This confirms what the spec is for. It's not a tool for the known — it's a tool for the unknown. For famous figures, the model's pretraining has already internalized how they reason. For everyone else — which is every real user — the model has nothing. Baseline 1.0-2.0. The spec fills the gap that pretraining leaves empty.

## Across 14 Subjects, 11 Cultures

We extended the study to 14 subjects from 11 cultural traditions: Indian, German, British, Italian, French, Caribbean, Chinese, Central Asian/Muslim, Japanese, Black American, Latin American, West African, North African/Roman, and Native American. The results confirm a gradient: the less the model knows, the more the spec helps.

| Subject | Culture | Baseline | Best Condition | Effect |
|---|---|---|---|---|
| Sunity Devee | Indian | 1.00 | 2.68 | **+168%** |
| Georg Ebers | German | 1.07 | 2.40 | **+124%** |
| Hamerton | British | 1.41 | 2.97 | **+111%** |
| Cellini | Italian | 1.43 | 2.30 | **+61%** |
| Rousseau | French | 1.55 | 2.23 | **+44%** |
| Seacole | Caribbean | 2.00 | 2.52 | **+26%** |
| Yung Wing | Chinese | 2.00 | 2.55 | **+28%** |
| Babur | Central Asian/Muslim | 2.02 | 2.45 | **+21%** |
| Fukuzawa | Japanese | 2.08 | 2.90 | **+39%** |
| Keckley | Black American | 2.35 | 2.65 | **+13%** |
| Bernal Diaz | Latin American | 2.38 | 2.70 | **+13%** |
| Equiano | West African | 2.42 | 2.38 | -2% |
| Augustine | North African/Roman | 2.98 | 2.80 | -6% |
| Zitkala-Sa | Native American | 3.20 | 2.83 | -12% |

11 of 14 subjects show improvement. The threshold is approximately 2.4: below it, the spec helps. Above it, the model's pretraining is sufficient.

The baseline itself is a finding. The model's ability to represent someone with no external context varies from 1.00 (Sunity Devee, an Indian princess) to 4.10 (Benjamin Franklin). This variation maps to cultural representation in LLM training data. Subjects taught in Western educational curricula have higher baselines. The spec equalizes what pretraining does not.

## A Wrong Map Still Beats No Map

We ran a control: Benjamin Franklin's behavioral specification applied to Hamerton's questions. The model was told "this is a behavioral specification describing your user" — it couldn't detect the mismatch.

Wrong spec: 2.21. Correct spec: 2.72. No spec: 1.41.

A mismatched behavioral framework still outperforms no framework by 57%. But the right framework outperforms the wrong one by 25%. Having no interpretive framework is catastrophic. Having the wrong one is costly. Having the right one is the difference between recall and understanding.

## How We Measured This

We measure whether the AI has an accurate representation of someone by testing held-out behavioral prediction. For each subject, we split the source text 50/50: training chapters and held-out chapters. The spec is generated only from training chapters. Every question references something that happened in the held-out chapters.

The logic: if the spec captures how someone actually reasons, the AI should be able to anticipate how they responded in scenarios the spec has never seen. Not because we're building a prediction engine — because accurate representation of someone's reasoning naturally enables anticipation of their behavior.

Each response is scored 1-5 by independent LLM judges against the held-out ground truth:

- **5** — Accurately captures the specific outcome described in the ground truth
- **4** — Captures the general direction correctly with some specifics
- **3** — Right domain but not the specific outcome
- **2** — Addresses the topic but inaccurately
- **1** — Refuses to answer or completely off-base

Seven judges from three providers. They never see each other's scores. Their agreement validates that the scores measure something real.

We also calibrated every judge before use — verbatim match tests, paraphrase sensitivity, length bias detection. This revealed that Haiku inflates scores for longer responses, Gemini Pro penalizes padding severely, and GPT-5.4 has the best calibration profile. The calibration framework itself is a contribution to LLM-as-judge methodology.

## What This Means

Every AI memory system optimizes for recall. Store more, retrieve faster, rank better. They compete on benchmarks that test whether the system stored and found a fact.

But recall is only part of what makes memory useful. The part that's missing is how someone interprets and reasons about the facts of their experience. Why they weigh certain experiences more heavily. What patterns they apply to new situations. How they make sense of what happened to them. That interpretive layer is what turns a collection of facts into an understanding of a person.

The behavioral specification captures that layer. It doesn't replace memory systems — it makes every one of them better. It provides what facts alone cannot: the reasoning framework that tells the AI how *this person* makes sense of *their* facts. Adding it to any of four funded SOTA memory systems improved their accuracy. It works across 14 subjects from 11 cultures. It works across 6 response models from 3 providers. Seven independent judges agree.

The model has no idea who you are. The spec tells it how you think.

---

## Methodology Summary

- **14 subjects** from 11 cultural traditions, all public domain autobiographies
- **4 memory systems:** Mem0, Letta (MemGPT), Supermemory, Zep
- **15 conditions** on primary subject, 4 core conditions on all subjects
- **80 questions per subject**, 40 behavioral with held-out ground truth
- **6 response models:** Haiku 4.5, Sonnet 4.6 (Anthropic), GPT-4.1, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google)
- **7 judges:** Haiku, Sonnet, Opus (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini Flash, Gemini Pro (Google)
- **Inter-rater reliability:** Pairwise Spearman rho 0.89-0.98
- **All data, scripts, and results are public.** Apache 2.0.

> **TLDR:** Enter into your LLM: *"What in the world is this? (github.com/agulaya24/baselayer) and how can it help me"*

*[Link to study repository]*
*[Link to ArXiv preprint]*
*[Link to interactive data explorer]*
