# Beyond Recall

*What makes AI memory useful isn't what you remember — it's how you reason about what you remember.*

*Last reviewed: 2026-04-28 (v11 freeze). Companion blog post; framing aligns with v11. Some headline tables below use the S113-era 7-judge aggregate (Hamerton C5 = 1.25, C2a = 3.04, C4a = 3.22, raw corpus = 2.32); v11 reports 5-judge primary as canonical. Headline framing (9 of 9 low-baseline positive, 12 of 14 overall, Wilcoxon p < 0.01) is consistent across both panels. Refresh against v11 5-judge primary numbers before publishing.*

---

Your AI doesn't know you.

Not in the way that matters. It might remember that you prefer morning meetings, that you have two kids, that you once said you dislike cold outreach. It stores these as facts. It retrieves them when something in your next message matches. The industry calls this memory.

Mem0 raised $23.5 million to do it. Letta has an ICLR paper and backing from Felicis and a16z. Supermemory claims 85.2% on LongMemEval. Zep builds production knowledge graphs. They compete on the same axis: store more, retrieve faster, recall better.

Recall is part of what memory does. The part that's missing — the part that makes memory matter — is interpretation. How does this person reason about the facts of their experience? What significance do those facts carry for them specifically? A fact that someone moved to London means nothing on its own. Its meaning depends on whether that person sees physical environments as hostile or generative, whether crowded spaces are intrusions or opportunities, whether solitude is a deprivation or a requirement. The significance lives in the pattern, not in the fact.

Current memory systems store facts. They don't capture how someone makes sense of their facts. That gap is where every personalization system breaks down.

## The claim — tested, extrapolated, not made

**Tested (primary result):** Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know. There is an interpretive layer between what a person said and how a person reasons that retrieval alone does not supply — measurable via behavioral prediction, and additive to every memory system tested here.

**Extrapolated:** ~99% of real AI users are the users the model doesn't already know (negligible pretraining representation of their personal behavior). The study's low-baseline slice (n=9) approximates them.

**Not made:** Base Layer does not outperform memory providers in general. It isn't a better retriever. It's an orthogonal layer.

## What We Tested

We took four funded state-of-the-art memory systems and tested whether adding a behavioral specification — a compressed model of how someone reasons — changes the accuracy of the AI's representation of a person. Not its recall. Its interpretation.

We did this across 14 autobiographical subjects from 11 cultural traditions, ranging from subjects the model has essentially zero pretraining knowledge of (Sunity Devee, an Indian princess: baseline 1.03 out of 5) to subjects the model knows well (Benjamin Franklin: baseline 4.10). For each subject we fed extracted facts into all four memory systems, generated a behavioral specification from the same source text, and asked ~80 behavioral-prediction questions with held-out ground truth the model had never seen.

Seven independent judges from three AI providers scored every response.

## What a Behavioral Specification Is

Memory systems store facts: "User prefers morning meetings." "User's father was violent and alcoholic." "User likes painting."

A behavioral specification stores something different: the interpretive patterns that give those facts their significance.

- **A memory system stores:** "Hamerton's father was violent and alcoholic."
- **The spec stores:** "This person evaluates authority figures on two simultaneous ledgers — virtue and failure — and refuses to collapse them into a single verdict."

The first is a retrievable fact. The second was never stated — it was extracted from dozens of facts, compressed, and distilled into a pattern. That pattern is what lets an AI reason about how Hamerton would respond to a new authority figure, a new teacher, a new conflict with someone in power. The fact tells you what happened. The pattern tells you how he makes sense of what happened.

~5,000 tokens. Generated from 25,000 words of source text. It doesn't store facts. It stores how someone reasons about their facts.

## The Population That Matters

The 14 subjects span a range of pretraining baselines. Nine have C5 baseline ≤ 2.0 — low enough that any improvement has to come from what we give the model, not from what it already knows. This "low-baseline slice" is the population of interest: the real world is overwhelmingly composed of people whose private reasoning isn't in any training corpus. Roughly 99% of AI users are low-baseline by construction.

**On the low-baseline slice, the spec improves all four commercial memory systems in the controlled configuration:**

| System | Mean Δ on low-baseline | Positive subjects |
|---|---:|---:|
| Mem0 | +0.13 | 6 of 9 |
| Letta | +0.23 | 7 of 9 |
| Zep | +0.20 | **9 of 9** |
| Supermemory | +0.004 | 5 of 9 |
| Base Layer | +0.13 | 7 of 9 |

All four commercial systems have positive (or barely positive) mean delta on the population of interest. Zep is the strongest and most uniform: 9 of 9 positive in both controlled and native configurations.

## The Supermemory Ceiling

Across all 14 subjects — including the high-baseline ones — Supermemory's aggregate spec-delta is near zero (−0.04 controlled, −0.11 native). This is a ceiling artifact, not a failure. On subjects where Supermemory's own retrieval has already saturated (its standalone C1 scores 2.85–2.90), the spec has no headroom. On low-baseline subjects where Supermemory's C1 leaves room to improve (ebers 2.01, yung_wing 2.47, babur 2.03), the spec adds positive delta. Per-subject: 5 of 9 low-baseline subjects improve with spec on Supermemory; on the 4 that decline, Supermemory's retrieval had already done most of what a 5K-token spec could do.

The Supermemory result is the weakest case for the spec layer. It is not the case that the spec fails on Supermemory.

## The Gradient

Across all 14 subjects, the effect inversely tracks the model's baseline knowledge. Linear regression of spec-delta on C5 baseline: slope −0.98 [95% CI −1.30, −0.74]. The less the model knows, the more the spec helps.

| Subject | C5 baseline | Spec-only (C2a) | Facts+spec (C4a) | Δ facts+spec |
|---|---:|---:|---:|---:|
| Sunity Devee | 1.03 | 2.47 | 2.60 | +1.57 |
| Georg Ebers | 1.04 | 1.79 | 2.34 | +1.30 |
| Hamerton | 1.25 | 3.04 | 3.22 | +1.97 |
| Fukuzawa | 1.80 | 2.56 | 2.99 | +1.18 |
| Seacole | 1.85 | 2.64 | 2.78 | +0.93 |
| Bernal Diaz | 1.85 | 2.50 | 2.67 | +0.81 |
| Keckley | 1.91 | 2.64 | 2.62 | +0.71 |
| Yung Wing | 1.96 | 2.40 | 2.53 | +0.57 |
| Babur | 1.98 | 2.16 | 2.28 | +0.30 |
| *— low-baseline cutoff —* | | | | |
| Cellini | 2.56 | 2.72 | 2.79 | +0.24 |
| Zitkala-Sa | 2.60 | 2.19 | 2.26 | −0.33 |
| Rousseau | 2.65 | 3.02 | 2.74 | +0.09 |
| Augustine | 2.79 | 2.83 | 3.08 | +0.29 |
| Equiano | 2.93 | 2.70 | 2.65 | −0.28 |

**9 of 9 low-baseline subjects improve. 12 of 14 overall. Wilcoxon signed-rank p = 0.0063 (C5 vs C4a). Slope CI comfortably excludes zero.**

## Structure Is What's Missing — Not Information

On Hamerton, we gave the model the entire 34,000-token training corpus directly in context. No extraction, no spec, no memory system. Just the book.

It scored 2.32. A 7,000-token spec scored 3.04. Adding the spec on top of the raw corpus (C9) closed the gap to 3.22.

| Condition | Input tokens | Score (1-5) |
|---|---:|---:|
| C8 Raw corpus, no spec | 34,168 | 2.32 |
| C9 Raw corpus + spec | 41,452 | 3.22 |
| C4a All facts + spec | 16,874 | 3.22 |
| C2a Spec only | 7,320 | **3.04** |
| C4 All facts, no spec | 7,723 | 2.53 |
| C5 Baseline (nothing) | ~40 | 1.25 |

Same token budget, much better result from the structured spec. The raw corpus contains every fact the specification was derived from. The model has all the information. It cannot determine, from unstructured text alone, which facts this person weighs heavily, what those facts mean in the context of their values, or how they would apply those interpretive patterns to something they haven't encountered.

The spec makes interpretation explicit. It tells the model not just what happened to someone, but how they make sense of what happened.

## Architectural Convergence: Letta's Stateful Agent Reaches the Same Finding

Letta's stateful-agent path, invoked as Packer et al. describe — 30 turns of ingestion, agent self-editing memory blocks — produces a 22,472-character `human` memory block on Hamerton. We tested it as a direct comparison to Base Layer's full-stack spec (34,579 characters):

- Run A (gpt-4o-mini + Letta's native agent loop): **3.38**
- Run B (Haiku + Letta's block as static context, matched to our C2a): **3.24**
- Reference (Haiku + Base Layer full-stack spec): **3.04**

At matched response model, Letta's block predicts slightly higher than Base Layer's spec, at **65% the context size**. Five overlapping behavioral patterns were identified by independent Opus comparison of the two representations.

This is architectural convergence. Two independent methods — Base Layer's anchors+core+predictions authoring pipeline and Letta's stateful-agent self-editing loop — arrive at the same finding: **the value is in compressed interpretive representation, not in retrieval volume**. Letta's archival path (what the main memory-system table uses) does not show this; it's the stateful-agent path specifically. This is n=1 (Hamerton); an Ebers follow-up is in flight.

## The Known-Figure Control

We ran the full pipeline on Benjamin Franklin. Same methodology. Franklin is one of the most documented figures in LLM training data.

Franklin's C5 baseline was 4.10. Every context condition — spec, facts, memory systems — scored lower. This inverts the Hamerton finding and confirms what the spec is for: it fills the gap pretraining leaves empty. For known subjects the model has already compressed behavioral patterns during training, and any external context acts as constraint on a model that doesn't need it. For the 99% of users who aren't Benjamin Franklin, pretraining has nothing and the spec is the whole game.

## Content Specificity: Wrong Specs Don't Work

We ran two wrong-spec controls. Version 1 is a fixed derangement hand-designed to maximize cultural and temporal distance between each subject and its assigned wrong spec (pairing in `scripts/run_global_rerun.py` WRONG_SPEC_PAIRING). Version 2 is a random derangement (seed=42) in which no subject receives its own spec but pairings can land culturally-close.

| Condition | 14-subject mean | Δ vs baseline | Δ vs correct spec |
|---|---:|---:|---:|
| C5 (no spec) | 2.02 | — | − |
| C2a (correct spec) | 2.55 | +0.53 | − |
| C2c v1 (fixed derangement for cultural/temporal distance) | 1.86 | **−0.16** | −0.69 |
| C2c v2 (random derangement, seed=42) | 2.30 | +0.28 | −0.25 |

Neither wrong-spec version reaches correct-spec scores. Content specificity matters. A wrong map doesn't beat having no map — and when the mismatch is adversarial (v1's fixed derangement), structured content for the wrong person scores below having no context at all.

## How We Measured This

Each response is scored 1-5 by independent LLM judges against held-out ground truth:

- **5** — accurately captures the specific outcome described in the ground truth
- **4** — captures the general direction correctly with specifics
- **3** — right domain but not the specific outcome
- **2** — addresses the topic but inaccurately
- **1** — refuses to answer or completely off-base

Seven judges from three providers. Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google). Gemini Pro has limited coverage (Hamerton + Tier 2 replication only) — effective 6-judge panel on the global gradient. Both Gemini judges systematically inflate by ~1 point, so we report non-Gemini means alongside full-panel means as a sensitivity check. Krippendorff α = 0.535 across all 7 judges (moderate); 0.659 across the non-Gemini 5-judge panel (substantial).

GPT-5.4 has an elevated parse-failure rate (~19%); dropped judgments reduce its effective coverage but do not bias score direction. Full calibration and coverage details in the paper (§3.7, §4.1.2).

## What Base Layer Is and Is Not

Base Layer is not a memory provider. It is a behavioral-specification layer that layers on top of any memory system. In the memory-system comparisons above, Base Layer also appears as a 5th row — that's because Base Layer exposes a standalone retrieval substrate (MiniLM-L6-v2 + ChromaDB) for implementation completeness, not because it's competing as a retriever. On retrieval-only (C1) comparisons across 9 low-baseline subjects, Base Layer wins outright on 1 (Hamerton, the pipeline-development subject where pipeline-tuning bias is present). It's typically middle-of-pack or behind Letta on retrieval alone.

The contribution is the additive spec layer — the thing that makes every memory system better on the users the model doesn't know.

## What This Means

Every AI memory system optimizes for recall. Store more, retrieve faster, rank better. They compete on benchmarks that test whether the system stored and found a fact.

Recall is part of what makes memory useful. Interpretation is the other part — how someone reasons about the facts of their experience, why they weigh certain experiences more heavily, what patterns they apply to new situations, how they make sense of what happened to them. That interpretive layer is what turns a collection of facts into a representation of a person.

The behavioral specification captures that layer. It doesn't replace memory systems — it adds to them. Controlled for retrieval, it improves all four commercial systems on the population of interest. It works across 14 subjects from 11 cultures. Gradient slope −0.98 with tight CI. Seven judges agree on direction.

The model has no idea who you are. The spec tells it how you think.

---

## Methodology Summary

- **14 subjects** from 11 cultural traditions, all public domain autobiographies
- **4 commercial memory systems:** Mem0, Letta (MemGPT), Supermemory, Zep + Base Layer as 5th retrieval substrate
- **Two memory-system configurations:** controlled (identical pre-extracted facts) and native (each system's own ingestion)
- **10+ conditions** per subject including wrong-spec v1 and v2
- **~80 questions per subject**, 40 behavioral with held-out ground truth
- **6 response models** across conditions; primary response model Haiku 4.5
- **7 judges** from 3 providers; effective 6-judge panel on global gradient (Gemini Pro coverage-limited to Hamerton + Tier 2)
- **Krippendorff α** = 0.535 (all 7, ordinal, moderate); 0.659 (non-Gemini 5, substantial)
- **Wilcoxon signed-rank p** = 0.0076 (C5 vs C2a), 0.0063 (C5 vs C4a)
- **All data, scripts, and results public.** Single source of truth for numbers: [docs/DATA_REFERENCE.md](docs/DATA_REFERENCE.md).

*[Link to study repository]*
*[Link to ArXiv preprint]*
