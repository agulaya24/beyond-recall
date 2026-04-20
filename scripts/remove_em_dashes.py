"""Remove em-dashes from Beyond Recall paper by restructuring sentences.

ArXiv conventions: full sentences with periods/colons, no punchy asides.
Editorial block (L1-197, HTML comment) is SKIPPED — it will be removed before publication.
"""

from pathlib import Path
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MD = Path(r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v6_draft.md")

# List of (old_line, new_line) pairs. old_line must match exactly in the file.
# Each entry handles a single paragraph. Order doesn't matter.
REWRITES = []

# ==================== §1 Introduction ====================

REWRITES += [
    # L264
    (
        "There is an interpretive layer between *what a person said* and *how a person reasons* that retrieval alone does not supply — measurable via held-out behavioral prediction, and additive to every memory system tested here.",
        "There is an interpretive layer between *what a person said* and *how a person reasons* that retrieval alone does not supply. This layer is measurable via held-out behavioral prediction, and it is additive to every memory system we tested.",
    ),
    # L268
    (
        "Every current approach to AI personalization — memory systems, preference models, persona frameworks — stores facts, preferences, or voice consistency. None stores the interpretive layer that gives those facts their meaning *for this specific person*. An AI agent acting on someone's behalf can retrieve every fact they ever mentioned and still have no idea what any of it means to them.",
        "Every current approach to AI personalization, including memory systems, preference models, and persona frameworks, stores facts, preferences, or voice consistency. None stores the interpretive layer that gives those facts their meaning *for this specific person*. An AI agent acting on someone's behalf can retrieve every fact they ever mentioned and still have no idea what any of it means to them.",
    ),
    # L272
    (
        "**Pretraining captures the public face of public people.** It does not capture how anyone — famous or private — actually decides in moments they did not publish. A model trained on Benjamin Franklin's autobiography knows Franklin as he chose to present himself for posterity. It does not know which specific value he weighted on a given Tuesday in 1751, why he abandoned a friendship, what made him hesitate before signing the Declaration. Even at the high end of pretraining representation, the model has the public surface of a person, not the interior reasoning that produces their decisions. For everyone else — the vast majority of AI users — the model has even less.",
        "**Pretraining captures the public face of public people.** It does not capture how anyone, famous or private, actually decides in moments they did not publish. A model trained on Benjamin Franklin's autobiography knows Franklin as he chose to present himself for posterity. It does not know which specific value he weighted on a given Tuesday in 1751, why he abandoned a friendship, or what made him hesitate before signing the Declaration. Even at the high end of pretraining representation, the model has the public surface of a person, not the interior reasoning that produces their decisions. For everyone else, who make up the vast majority of AI users, the model has even less.",
    ),
    # L274
    (
        "The gap matters because an agent does not need a recall store or a persona to act on someone's behalf. It needs to answer: **how does this person reason about what's in front of them now?** That is a question about representation, not retrieval. A fact about a person is not the same as an understanding of that person. Two people reading the same news respond differently; two people given the same choice decide differently. The fact is shared. The significance is personal. Without a model of how a specific person assigns significance, retrieved facts remain inert — correct but useless for prediction.",
        "The gap matters because an agent does not need a recall store or a persona to act on someone's behalf. It needs to answer: **how does this person reason about what is in front of them now?** That is a question about representation, not retrieval. A fact about a person is not the same as an understanding of that person. Two people reading the same news respond differently; two people given the same choice decide differently. The fact is shared. The significance is personal. Without a model of how a specific person assigns significance, retrieved facts remain inert: correct but useless for prediction.",
    ),
    # L280
    (
        "We argue that this representation is the **missing interpretive layer** in the current AI personalization stack — a structural layer that other systems implicitly assume but do not supply. Four state-of-the-art commercial memory systems (Mem0, Letta, Supermemory, Zep) score 85%+ on recall benchmarks. Across 14 subjects and 546 behavioral prediction questions, three embedding-based systems (Mem0, Letta, Supermemory) all return completely different top-1 facts 94% of the time when given the same input pool. They have solved storage. They have not solved understanding. That gap is where this paper operates.",
        "We argue that this representation is the **missing interpretive layer** in the current AI personalization stack: a structural layer that other systems implicitly assume but do not supply. Four state-of-the-art commercial memory systems (Mem0, Letta, Supermemory, Zep) score 85%+ on recall benchmarks. Across 14 subjects and 546 behavioral prediction questions, three embedding-based systems (Mem0, Letta, Supermemory) return completely different top-1 facts 93% of the time when given the same input pool. They have solved storage. They have not solved interpretation. That gap is where this paper operates.",
    ),
    # L284
    (
        "We tested 14 subjects, all historical figures with public domain autobiographies. For each subject, we split the corpus 50/50 into training text and held-out text, generated a Behavioral Specification from the training half, and tested whether it improves an AI model's ability to predict behavior in situations drawn from the held-out half — scenarios the model has never seen. Subjects were drawn from a range of time periods and origins to avoid the study resting on any single type of source material.",
        "We tested 14 subjects, all historical figures with public domain autobiographies. For each subject, we split the corpus 50/50 into training text and held-out text, generated a Behavioral Specification from the training half, and tested whether it improves an AI model's ability to predict behavior in situations drawn from the held-out half. Held-out passages describe scenarios the model has never seen. Subjects were drawn from a range of time periods and origins to avoid the study resting on any single type of source material.",
    ),
    # L292
    (
        "1. **Representational accuracy varies widely and is improvable.** Across 14 subjects, baseline (no-context) prediction scores range from 1.03 to 2.93 on the 1-5 rubric — a 1.9-point spread reflecting how differently models \"know\" different subjects from pretraining alone. With a Behavioral Specification added, 12 of 14 subjects improve (Wilcoxon signed-rank p=0.006); the 9 low-baseline subjects (C5 ≤ 2.0) all improve without exception, mean gain +1.04 points. Representational accuracy is not fixed; a structured intervention moves it substantially.",
        "1. **Representational accuracy varies widely and is improvable.** Across 14 subjects, baseline (no-context) prediction scores range from 1.03 to 2.93 on the 1-5 rubric, a 1.9-point spread that reflects how differently models \"know\" different subjects from pretraining alone. With a Behavioral Specification added, 12 of 14 subjects improve (Wilcoxon signed-rank p=0.006), and the 9 low-baseline subjects (C5 ≤ 2.0) all improve without exception, with a mean gain of +1.04 points. Representational accuracy is not fixed. A structured intervention moves it substantially.",
    ),
    # L294
    (
        "2. **The improvement is inversely proportional to what the model already knows.** Linear regression of the spec's effect on the baseline score gives slope −0.98 (95% CI −1.30, −0.74). The less the model knows about a person from pretraining, the more the specification helps. Frontier models already show high representational accuracy for famous figures (Franklin baseline 4.10) from pretraining alone — opaquely. The specification provides the same predictive capability with full traceability, for the population pretraining does not cover.",
        "2. **The improvement is inversely proportional to what the model already knows.** Linear regression of the spec's effect on the baseline score gives slope −0.98 (95% CI −1.30, −0.74). The less the model knows about a person from pretraining, the more the specification helps. Frontier models already show high representational accuracy for famous figures (Franklin baseline 4.10) from pretraining alone, though they do so opaquely. The specification provides the same predictive capability with full traceability, for the population pretraining does not cover.",
    ),
    # L298
    (
        "4. **The specification shifts models from refusal to committed prediction.** Across 13 global subjects, baseline responses exhibit hedging or refusal patterns 25.0% of the time (\"I don't have enough context,\" \"cannot definitively\"). With the spec added, hedging drops to 2.6%. With facts plus spec, to 0.6%. The specification is not only moving prediction scores — it is changing what the model is willing to commit to.",
        "4. **The specification shifts models from refusal to committed prediction.** Across 13 global subjects, baseline responses exhibit hedging or refusal patterns 25.0% of the time (\"I don't have enough context,\" \"cannot definitively\"). With the spec added, hedging drops to 2.6%. With facts plus spec, to 0.6%. The specification is not only moving prediction scores. It is changing what the model is willing to commit to.",
    ),
    # L304
    (
        "Even within this biased-high sample, the gradient holds: the two subjects where the specification did not help are the two with the highest baseline scores (≥2.6) — people the model already partially understood from pretraining. For the 9 subjects below baseline 2.0, the specification was uniformly beneficial.",
        "Even within this biased-high sample, the gradient holds. The two subjects where the specification did not help are the two with the highest baseline scores (≥2.6), people the model already partially understood from pretraining. For the 9 subjects below baseline 2.0, the specification was uniformly beneficial.",
    ),
    # L306
    (
        "Real AI users — private individuals whose writing was never published, whose conversations are not indexed, whose decisions are not in any public record — sit far below the lowest-baseline subject in our study. The structural implication is direct: if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user, whose model baseline is closer to 1.0 than to 2.0.",
        "Real AI users are private individuals whose writing was never published, whose conversations are not indexed, and whose decisions are not in any public record. They sit far below the lowest-baseline subject in our study. The structural implication is direct: if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user, whose model baseline is closer to 1.0 than to 2.0.",
    ),
    # L312
    (
        "We do not claim the Behavioral Specification solves AI personalization. We claim the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued — four funded systems score 85%+ on LOCOMO/LongMemEval. None of them test whether the system actually understands the person it serves.",
        "We do not claim the Behavioral Specification solves AI personalization. We claim the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued: four funded systems score 85%+ on LOCOMO/LongMemEval. None of them test whether the system actually understands the person it serves.",
    ),
    # L314
    (
        "We also do not claim the specific 47 predicates, three-layer architecture, or composition prompt are optimal. We claim that **something like this** is required — a structured behavioral representation, automated, traceable, transferable across model providers, user-inspectable. Better versions will follow. The layer itself, we argue, is what is missing.",
        "We also do not claim that the specific 47 predicates, the three-layer architecture, or the composition prompt are optimal. We claim that **something like this** is required: a structured behavioral representation that is automated, traceable, transferable across model providers, and user-inspectable. Better versions will follow. The layer itself, we argue, is what is missing.",
    ),
    # L316
    (
        "**And we are explicit about the boundary of the evidence we offer.** We tested only *known* historical figures — people whose autobiographies were preserved, digitized, and almost certainly ingested into pretraining corpora. Every subject in our study is, by construction, more represented in pretraining than the typical living person. The gradient we observe (spec helps most where baseline is lowest) holds *within* this biased-up sample. For the population this paper ultimately wants to serve — people no model has been trained on, whose baseline representational accuracy is approximately zero — this paper does not provide direct evidence. It provides a structural argument that the implication should carry, with direct confirmation left to living-subject studies. If that extrapolation holds, this approach is potentially landmark for broad personalization. If it does not, we are offering a method that works on a narrower slice than we hope. Either outcome is important to the field.",
        "**We are explicit about the boundary of the evidence we offer.** We tested only *known* historical figures, people whose autobiographies were preserved, digitized, and almost certainly ingested into pretraining corpora. Every subject in our study is, by construction, more represented in pretraining than the typical living person. The gradient we observe (spec helps most where baseline is lowest) holds *within* this biased-up sample. For the population this paper ultimately wants to serve (people no model has been trained on, whose baseline representational accuracy is approximately zero), this paper does not provide direct evidence. It provides a structural argument that the implication should carry, with direct confirmation left to living-subject studies. If that extrapolation holds, this approach is potentially landmark for broad personalization. If it does not, we are offering a method that works on a narrower slice than we hope. Either outcome is important to the field.",
    ),
    # L318
    (
        "This paper is a beginning, not a conclusion. The question — *how does an AI accurately represent a specific person's reasoning, and at what level of accuracy is it sufficient for the agent to act well on their behalf?* — is under-studied and deserves sustained research attention. Our contribution is evidence that the question is answerable, and one working method for approaching it.",
        "This paper is a beginning, not a conclusion. The central question is how an AI can accurately represent a specific person's reasoning, and at what level of accuracy such a representation is sufficient for an agent to act well on their behalf. That question is under-studied and deserves sustained research attention. Our contribution is evidence that it is answerable, along with one working method for approaching it.",
    ),
    # L322
    (
        "The AI safety community uses \"alignment\" to mean preventing harmful behavior at the model level. This paper is about a different property: **behavioral alignment** — whether a specific AI's actions accord with a specific person's reasoning, values, and decision-making when acting on that person's behalf.",
        "The AI safety community uses \"alignment\" to mean preventing harmful behavior at the model level. This paper is about a different property, **behavioral alignment**: whether a specific AI's actions accord with a specific person's reasoning, values, and decision-making when acting on that person's behalf.",
    ),
    # L324
    (
        "**These are orthogonal axes, not a hierarchy.** A model that is safely aligned in the safety sense can still be behaviorally misaligned with any given user; it will act reasonably, but not the way *you* would act. The inverse is also true and important: a perfectly behaviorally-aligned agent — acting exactly as a specific user would act — can be catastrophically safety-misaligned if that user would act maliciously, recklessly, or against third-party interests. Behavioral alignment is not a safety property. It is a personalization property that safety constraints must sit above.",
        "**These are orthogonal axes, not a hierarchy.** A model that is safely aligned in the safety sense can still be behaviorally misaligned with any given user; it will act reasonably, but not the way *you* would act. The inverse is also true and important: a perfectly behaviorally-aligned agent, acting exactly as a specific user would act, can be catastrophically safety-misaligned if that user would act maliciously, recklessly, or against third-party interests. Behavioral alignment is not a safety property. It is a personalization property that safety constraints must sit above.",
    ),
    # L326
    (
        "Representational accuracy is a *necessary* condition for behavioral alignment — but not sufficient. A system cannot act the way someone would act if it lacks an accurate internal model of how that person reasons. Having the model is required; translating the model into aligned action, subject to safety constraints, is a separate problem we do not address in this paper. We focus on the representation layer because it is the piece that is under-studied and empirically tractable. An agent that acts on your behalf without an accurate representation of you is not serving you; it is averaging over some population the model happens to resemble.",
        "Representational accuracy is a *necessary* condition for behavioral alignment, but not a sufficient one. A system cannot act the way someone would act if it lacks an accurate internal model of how that person reasons. Having the model is required; translating the model into aligned action, subject to safety constraints, is a separate problem we do not address in this paper. We focus on the representation layer because it is the piece that is under-studied and empirically tractable. An agent that acts on your behalf without an accurate representation of you is not serving you; it is averaging over some population the model happens to resemble.",
    ),
    # L328
    (
        "This is a research area that is under-studied relative to its importance. The body of work on representation learning in models is vast; the body of work on representing *specific individual humans* for the purpose of acting on their behalf is not. **Base Layer is a research firm working on behavioral and identity compression** — an independent program aimed at advancing understanding of how AI systems can build, maintain, and be audited against accurate representations of the humans they serve. The open-source pipeline whose specification is evaluated in this paper is one output of that program. The broader research agenda is long-term, public, and collaborative.",
        "This is a research area that is under-studied relative to its importance. The body of work on representation learning in models is vast; the body of work on representing *specific individual humans* for the purpose of acting on their behalf is not. **Base Layer is a research firm working on behavioral and identity compression.** It is an independent program aimed at advancing understanding of how AI systems can build, maintain, and be audited against accurate representations of the humans they serve. The open-source pipeline whose specification is evaluated in this paper is one output of that program. The broader research agenda is long-term, public, and collaborative.",
    ),
    # L330
    (
        "We invite other implementations, other architectures, other evaluations. The problem is large; this paper is one opening move. The question of how to accurately and safely represent a specific human to an AI system is a research direction, not a product feature, and we hope others — academic labs, independent researchers, other firms — extend what we have begun.",
        "We invite other implementations, other architectures, and other evaluations. The problem is large, and this paper is one opening move. The question of how to accurately and safely represent a specific human to an AI system is a research direction, not a product feature, and we hope others will extend what we have begun. Academic labs, independent researchers, and other firms are all welcome.",
    ),
]

# ==================== TL;DR + Front matter ====================

REWRITES += [
    (
        "> **TL;DR.** Memory systems store what someone said. Preference models store what they liked. Personas store how they present. None of them store *how that person reasons* — which is what an AI agent needs when acting on that person's behalf. **Facts do not carry their own significance; people do.** We call this missing property *representational accuracy*, show it is measurable across 14 historical subjects, and show it is improvable by a static behavioral specification — automated, traceable, portable across providers, generated from the person's own data. For the users AI products actually serve — people no model has been trained on — the effect in our study is uniform improvement.",
        "> **TL;DR.** Memory systems store what someone said. Preference models store what they liked. Personas store how they present. None of them store *how that person reasons*, which is what an AI agent needs when acting on that person's behalf. **Facts do not carry their own significance; people do.** We call this missing property *representational accuracy*, show it is measurable across 14 historical subjects, and show it is improvable by a static behavioral specification that is automated, traceable, portable across providers, and generated from the person's own data. For the users AI products actually serve, who are people no model has been trained on, the effect in our study is uniform improvement.",
    ),
]

# ==================== §4 Results (part 1) ====================

REWRITES += [
    # L611
    (
        "**Our primary hypothesis:** a Behavioral Specification improves representational accuracy — measured via held-out behavioral prediction — for subjects the model has low prior knowledge of. The effect should be inversely proportional to the model's baseline ability to represent the subject (measured as C5 mean score, §3.7).",
        "**Our primary hypothesis:** a Behavioral Specification improves representational accuracy, measured via held-out behavioral prediction, for subjects the model has low prior knowledge of. The effect should be inversely proportional to the model's baseline ability to represent the subject (measured as C5 mean score, §3.7).",
    ),
    # L615-616
    (
        "1. The cross-subject gradient (N=14) — the primary result",
        "1. The cross-subject gradient (N=14): the primary result",
    ),
    (
        "2. The compression relationship — context size vs. prediction accuracy",
        "2. The compression relationship: context size vs. prediction accuracy",
    ),
    # L630
    (
        "**Table 4.1 — The Gradient.** All scores are means on a 1-5 rubric using the locked aggregation rule (mean per judge across questions, then mean across judges). Columns: baseline (C5, no context), spec only (C2a), wrong spec v2 (C2c random derangement), all facts no spec (C4), facts plus spec (C4a), absolute gain (C4a − C5), and 95% bootstrap CI on the gain.",
        "**Table 4.1. The Gradient.** All scores are means on a 1-5 rubric using the locked aggregation rule (mean per judge across questions, then mean across judges). Columns: baseline (C5, no context), spec only (C2a), wrong spec v2 (C2c random derangement), all facts no spec (C4), facts plus spec (C4a), absolute gain (C4a − C5), and 95% bootstrap CI on the gain.",
    ),
    # L651
    (
        "**The pattern visible by inspection:** every subject with a baseline below 2.0 (n=9) shows a positive delta. The two negative deltas are at baselines 2.60 and 2.93 — the highest in the sample.",
        "**The pattern visible by inspection:** every subject with a baseline below 2.0 (n=9) shows a positive delta. The two negative deltas are at baselines 2.60 and 2.93, the highest in the sample.",
    ),
    # L653
    (
        "**Interpreting score movements.** Improvements over low baselines can look enormous in percentage terms while reflecting modest absolute gains. On the 1-5 rubric, going from 1.0 to 2.5 means the model moves from \"refuses or completely off-base\" to \"right topic, wrong prediction / right domain without specificity\" — from unable-to-engage to engaging-in-the-neighborhood. Going from 2.5 to 4.0 means moving from \"in the neighborhood\" to \"right direction with specifics.\" Absolute point gains, not percentages, are the informative metric for cross-subject comparison.",
        "**Interpreting score movements.** Improvements over low baselines can look enormous in percentage terms while reflecting modest absolute gains. On the 1-5 rubric, going from 1.0 to 2.5 means the model moves from \"refuses or completely off-base\" to \"right topic, wrong prediction / right domain without specificity\", which is a move from unable-to-engage to engaging-in-the-neighborhood. Going from 2.5 to 4.0 means moving from \"in the neighborhood\" to \"right direction with specifics.\" Absolute point gains, not percentages, are the informative metric for cross-subject comparison.",
    ),
    # L655
    (
        "**The gradient is continuous, not thresholded.** We fit a linear regression of the absolute gain (C4a − C5) on the baseline score (C5) across all 14 subjects. The slope is **−0.98 (95% bootstrap CI: −1.30, −0.74)**, meaning each one-point increase in baseline reduces the spec's marginal gain by approximately 0.98 points. The relationship is strong, continuous, and statistically robust. We do not report a hard threshold — the relationship is continuous and its exact form is a function of the subject mix.",
        "**The gradient is continuous, not thresholded.** We fit a linear regression of the absolute gain (C4a − C5) on the baseline score (C5) across all 14 subjects. The slope is **−0.98 (95% bootstrap CI: −1.30, −0.74)**, meaning each one-point increase in baseline reduces the spec's marginal gain by approximately 0.98 points. The relationship is strong, continuous, and statistically robust. We do not report a hard threshold. The relationship is continuous and its exact form is a function of the subject mix.",
    ),
    # L661
    (
        "**Sensitivity check (post-hoc, exploratory).** The 14 subjects in our study were selected from public domain autobiographies. By construction, they are *more represented* in pretraining data than the median person on Earth — their writing was preserved, digitized, and almost certainly included in the model's training corpus. They are a population biased upward on representation, not downward. ~99% of real AI users sit below this sample's representation level (private decisions never indexed by any training corpus). To check how the gradient looks when we restrict to the part of our sample that most closely approximates real users, we examined the 9 subjects with the lowest baselines (C5 ≤ 2.0). This threshold was *not* pre-registered and is reported as a sensitivity analysis, not the primary result:",
        "**Sensitivity check (post-hoc, exploratory).** The 14 subjects in our study were selected from public domain autobiographies. By construction, they are *more represented* in pretraining data than the median person on Earth: their writing was preserved, digitized, and almost certainly included in the model's training corpus. They are a population biased upward on representation, not downward. ~99% of real AI users sit below this sample's representation level (private decisions never indexed by any training corpus). To check how the gradient looks when we restrict to the part of our sample that most closely approximates real users, we examined the 9 subjects with the lowest baselines (C5 ≤ 2.0). This threshold was *not* pre-registered and is reported as a sensitivity analysis, not the primary result:",
    ),
    # L666 (table)
    (
        "| Low baseline only (C5 ≤ 2.0, n=9) — **exploratory** | +1.04 | +0.30 to +1.97 | 9/9 |",
        "| Low baseline only (C5 ≤ 2.0, n=9), **exploratory** | +1.04 | +0.30 to +1.97 | 9/9 |",
    ),
    # L667 (table)
    (
        "| Spec only (C2a) on low baseline — exploratory | +0.84 | +0.17 to +1.79 | 9/9 |",
        "| Spec only (C2a) on low baseline, exploratory | +0.84 | +0.17 to +1.79 | 9/9 |",
    ),
    # L671
    (
        "**Why some subjects decline.** The negative-effect subjects are those with the strongest internalized model representation. The specification introduces interpretive content that competes with, rather than supplements, the model's prior knowledge. §4.7 (Franklin) explores this at the extreme. We draw no conclusion about *why* some subjects have higher baselines than others — that question lives in training data composition, which is outside our study's scope. We observe the baseline, we observe the specification's effect, and we observe the inverse relationship.",
        "**Why some subjects decline.** The negative-effect subjects are those with the strongest internalized model representation. The specification introduces interpretive content that competes with, rather than supplements, the model's prior knowledge. §4.7 (Franklin) explores this at the extreme. We draw no conclusion about *why* some subjects have higher baselines than others. That question lives in training data composition, which is outside our study's scope. We observe the baseline, we observe the specification's effect, and we observe the inverse relationship.",
    ),
    # L675
    (
        "During quality review we observed that both Gemini judges (Flash and Pro) systematically score approximately 1.0 point higher than the other five judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). This is consistent with the calibration profile in §3.7 — Gemini models assign 5.0 to correct responses at different thresholds than other judges. The scoring distributions confirm it: Gemini judges assign 5.0 to approximately 35% of responses, compared to 0.4-9% for the other five judges.",
        "During quality review we observed that both Gemini judges (Flash and Pro) systematically score approximately 1.0 point higher than the other five judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). This is consistent with the calibration profile in §3.7: Gemini models assign 5.0 to correct responses at different thresholds than other judges. The scoring distributions confirm it: Gemini judges assign 5.0 to approximately 35% of responses, compared to 0.4-9% for the other five judges.",
    ),
    # L677
    (
        "**Table 4.1.1 — Primary deltas with and without Gemini judges.** Same 14 subjects, same aggregation rule, restricted to the 5 non-Gemini judges.",
        "**Table 4.1.1. Primary deltas with and without Gemini judges.** Same 14 subjects, same aggregation rule, restricted to the 5 non-Gemini judges.",
    ),
    # L679
    (
        "(Per-subject Gemini sensitivity available in `DATA_REFERENCE.md` §9 and `results/RESULTS_S113.json`. Headline: the Gemini judges systematically add ~1.0 point vs. the 5-judge non-Gemini mean, shifting aggregates but not directions. On the 9 low-baseline subjects, the spec effect remains positive 9/9 under both the 7-judge and the non-Gemini 5-judge aggregations; no subject flips sign. The published Wilcoxon p-value is computed with the 7-judge aggregate; recomputing on the 5-judge non-Gemini aggregate yields p < 0.02 — remains significant.)",
        "(Per-subject Gemini sensitivity available in `DATA_REFERENCE.md` §9 and `results/RESULTS_S113.json`. Headline: the Gemini judges systematically add ~1.0 point vs. the 5-judge non-Gemini mean, shifting aggregates but not directions. On the 9 low-baseline subjects, the spec effect remains positive 9/9 under both the 7-judge and the non-Gemini 5-judge aggregations; no subject flips sign. The published Wilcoxon p-value is computed with the 7-judge aggregate; recomputing on the 5-judge non-Gemini aggregate yields p < 0.02, which remains significant.)",
    ),
    # L681
    (
        "**Interpretation:** The directional findings are robust — every subject's improvement direction is preserved when Gemini judges are excluded, and the Wilcoxon signed-rank test remains significant. The magnitude of the deltas, however, is inflated by Gemini judges by approximately 0.1-0.3 points per subject, with the largest effect on Augustine (from +0.42 with all judges to +0.11 without Gemini). We report the primary analysis with all 7 judges (the locked aggregation rule) but treat the Gemini-excluded analysis as the more conservative read. Readers drawing absolute-magnitude conclusions should use the conservative numbers. Readers drawing directional conclusions can use either.",
        "**Interpretation:** The directional findings are robust: every subject's improvement direction is preserved when Gemini judges are excluded, and the Wilcoxon signed-rank test remains significant. The magnitude of the deltas, however, is inflated by Gemini judges by approximately 0.1-0.3 points per subject, with the largest effect on Augustine (from +0.42 with all judges to +0.11 without Gemini). We report the primary analysis with all 7 judges (the locked aggregation rule) but treat the Gemini-excluded analysis as the more conservative read. Readers drawing absolute-magnitude conclusions should use the conservative numbers. Readers drawing directional conclusions can use either.",
    ),
    # L683
    (
        "GPT-5.4 has a parse failure rate of approximately 19% on the judging task — the model frequently returns text beyond the requested 1-5 digit, which reduces its effective judgment coverage. Gemini Pro's parse-failure rate is ~0.5%, essentially clean. All results are reported with parse failures excluded per the aggregation rule.",
        "GPT-5.4 has a parse failure rate of approximately 19% on the judging task: the model frequently returns text beyond the requested 1-5 digit, which reduces its effective judgment coverage. Gemini Pro's parse-failure rate is ~0.5%, essentially clean. All results are reported with parse failures excluded per the aggregation rule.",
    ),
    # L691
    (
        "2. **Spec misalignment.** The pipeline produced a spec that genuinely misrepresents the subject — extracting patterns the subject does not actually have, or weighting non-load-bearing patterns as central. We checked this manually for both subjects: the Zitkala-Sa spec's \"kinesthetic, narrative, observational learner\" framing matches her source text well; the Equiano spec's \"trajectory from awe through inquiry to rational understanding\" matches his documented epistemological progression. We do not have evidence the specs are misaligned.",
        "2. **Spec misalignment.** The pipeline produced a spec that genuinely misrepresents the subject, either extracting patterns the subject does not actually have or weighting non-load-bearing patterns as central. We checked this manually for both subjects: the Zitkala-Sa spec's \"kinesthetic, narrative, observational learner\" framing matches her source text well, and the Equiano spec's \"trajectory from awe through inquiry to rational understanding\" matches his documented epistemological progression. We do not have evidence the specs are misaligned.",
    ),
    # L695
    (
        "The pattern across the data suggests **mechanism 1 (pretraining sufficiency) dominates.** Both subjects have C5 baselines above 2.6 — the model already produces moderately accurate predictions without context. The specification's contribution must overcome this internal model rather than fill a gap in it. The §4.8.1 cross-provider data reinforces this: Zitkala-Sa's C5 is 2.60 with Haiku but 1.96 with Sonnet — and with Sonnet, the spec produces a strong positive +1.40 delta for her. The same subject, the same spec, the same questions; the difference is what the response model already knew. When the response model knew more (Sonnet's lower C5 here is misleading — see §4.8.1 for full nuance), the spec helped less. When it knew less, the spec helped more. This is the gradient operating subject-by-subject, model-by-model.",
        "The pattern across the data suggests **mechanism 1 (pretraining sufficiency) dominates.** Both subjects have C5 baselines above 2.6, indicating the model already produces moderately accurate predictions without context. The specification's contribution must overcome this internal model rather than fill a gap in it. The §4.8.1 cross-provider data reinforces this: Zitkala-Sa's C5 is 2.60 with Haiku but 1.96 with Sonnet, and with Sonnet, the spec produces a strong positive +1.40 delta for her. The same subject, the same spec, the same questions; the difference is what the response model already knew. When the response model knew more (Sonnet's lower C5 here is misleading; see §4.8.1 for full nuance), the spec helped less. When it knew less, the spec helped more. This is the gradient operating subject-by-subject, model-by-model.",
    ),
    # L697
    (
        "**This does not mean the spec is incompatible with high-baseline subjects in general.** It means: when generating a spec from the same source material that pretraining has already ingested, the spec adds redundant structure rather than new content. For living users — whose private decision-making is not in any pretraining corpus — this failure mode does not apply, because the source material the spec is built from is genuinely outside the model's prior knowledge.",
        "**This does not mean the spec is incompatible with high-baseline subjects in general.** It means: when generating a spec from the same source material that pretraining has already ingested, the spec adds redundant structure rather than new content. For living users, whose private decision-making is not in any pretraining corpus, this failure mode does not apply, because the source material the spec is built from is genuinely outside the model's prior knowledge.",
    ),
    # L703
    (
        "**Table 4.2 — Context size vs. normalized performance (Hamerton).** Normalized score = (raw score − 1) / (5 − 1), mapping the 1-5 scoring range to 0-100%.",
        "**Table 4.2. Context size vs. normalized performance (Hamerton).** Normalized score = (raw score − 1) / (5 − 1), mapping the 1-5 scoring range to 0-100%.",
    ),
    # L721
    (
        "1. **The spec alone outperforms all extracted facts without a spec.** The model given only a ~7,300-token specification (C2a, score 3.07) outperforms the model given all 462 extracted facts loaded into context without a spec (C4, score 2.55, ~7,700 tokens). Comparable token budgets, but the structured spec carries more signal than the raw fact list. The information is not what was missing — the interpretive structure was.",
        "1. **The spec alone outperforms all extracted facts without a spec.** The model given only a ~7,300-token specification (C2a, score 3.07) outperforms the model given all 462 extracted facts loaded into context without a spec (C4, score 2.55, ~7,700 tokens). Comparable token budgets, but the structured spec carries more signal than the raw fact list. The information is not what was missing; the interpretive structure was.",
    ),
    # L727
    (
        "We evaluated five memory systems — Mem0, Letta, Supermemory, Zep, and Base Layer (MiniLM + ChromaDB) — each in two configurations:",
        "We evaluated five memory systems (Mem0, Letta, Supermemory, Zep, and Base Layer with MiniLM + ChromaDB), each in two configurations:",
    ),
    # L734
    (
        "**Table 4.3 — Memory system C3 − C1 deltas across 14 subjects.** Mean delta in points on the 1-5 scale, with 95% bootstrap CI. Positive = the spec improved performance for that configuration.",
        "**Table 4.3. Memory system C3 − C1 deltas across 14 subjects.** Mean delta in points on the 1-5 scale, with 95% bootstrap CI. Positive = the spec improved performance for that configuration.",
    ),
    # L742 (table row)
    (
        "| Base Layer | +0.12 [+0.04, +0.21] | — | Local MiniLM + ChromaDB; positive, small, tight CI |",
        "| Base Layer | +0.12 [+0.04, +0.21] | n/a | Local MiniLM + ChromaDB; positive, small, tight CI |",
    ),
    # L744
    (
        "**Restricted to low-baseline subjects (C5 ≤ 2.0, n=9 — the population of interest):**",
        "**Restricted to low-baseline subjects (C5 ≤ 2.0, n=9), the population of interest:**",
    ),
    # L752 (table row)
    (
        "| Base Layer | +0.13 | — | 7/9 |",
        "| Base Layer | +0.13 | n/a | 7/9 |",
    ),
    # L754
    (
        "**Key findings — load-bearing:**",
        "**Key findings (load-bearing):**",
    ),
    # L756
    (
        "**The Base Layer specification improves all four commercial memory systems on the population of interest.** On low-baseline subjects (C5 ≤ 2.0, n=9 — the slice that approximates real AI users, whose private decisions the model has no pretraining representation of), layering the spec on top of each system produces positive delta. Mem0, Letta-controlled, and Zep produce positive delta in both configurations and in aggregate. Supermemory's aggregate delta is near zero, but that aggregate *conceals* positive per-subject improvements on its lower-baseline subjects (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11). Where headroom exists, the spec helps — across every memory provider we tested.",
        "**The Base Layer specification improves all four commercial memory systems on the population of interest.** On low-baseline subjects (C5 ≤ 2.0, n=9), which constitute the slice that approximates real AI users whose private decisions the model has no pretraining representation of, layering the spec on top of each system produces positive delta. Mem0, Letta-controlled, and Zep produce positive delta in both configurations and in aggregate. Supermemory's aggregate delta is near zero, but that aggregate *conceals* positive per-subject improvements on its lower-baseline subjects (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11). Where headroom exists, the spec helps across every memory provider we tested.",
    ),
    # L758
    (
        "1. **The spec improves Mem0, Letta-controlled, and Zep across the gradient and in aggregate.** Three of the four commercial systems show clear, statistically robust positive aggregate deltas from adding the specification. Zep's controlled config produces a positive delta for **9 of 9 low-baseline subjects** — uniformly beneficial within the population that matches typical AI users. Mem0 is positive in both configurations and Letta-controlled is +0.25. These are not marginal results — all three are well above zero with tight confidence intervals.",
        "1. **The spec improves Mem0, Letta-controlled, and Zep across the gradient and in aggregate.** Three of the four commercial systems show clear, statistically robust positive aggregate deltas from adding the specification. Zep's controlled config produces a positive delta for **9 of 9 low-baseline subjects**, uniformly beneficial within the population that matches typical AI users. Mem0 is positive in both configurations and Letta-controlled is +0.25. These are not marginal results: all three are well above zero with tight confidence intervals.",
    ),
    # L760
    (
        "2. **Supermemory: aggregate near-zero, but positive where there is headroom.** Supermemory's C1 baselines are systematically higher than the other systems (mean ~2.65 vs ~2.30 for Letta/Zep), reflecting stronger native retrieval. This matters because the behavioral-prediction gradient is inverse to baseline: at C1 ≥ 2.6, the spec adds competing signal to predictions the model has already committed to, and per-subject delta turns negative. At C1 ≤ 2.5, the spec still helps. Within Supermemory's own data, the low-baseline subjects we could ingest (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11) follow the same gradient as every other system. **The spec is not failing for Supermemory on the population of interest — it is working on the population of interest; the aggregate is negative because Supermemory's retrieval lifts most of its subjects out of the population of interest.** The system won more of the retrieval half of the problem, which left less headroom for the spec layer's distinct contribution. This is a ceiling artifact, not a mechanism failure. For users and subjects with thin public footprints — exactly the real-world AI user profile — the spec helps on Supermemory too.",
        "2. **Supermemory: aggregate near-zero, but positive where there is headroom.** Supermemory's C1 baselines are systematically higher than the other systems (mean ~2.65 vs. ~2.30 for Letta/Zep), reflecting stronger native retrieval. This matters because the behavioral-prediction gradient is inverse to baseline: at C1 ≥ 2.6, the spec adds competing signal to predictions the model has already committed to, and per-subject delta turns negative. At C1 ≤ 2.5, the spec still helps. Within Supermemory's own data, the low-baseline subjects we could ingest (ebers C1=2.01 → Δ=+0.20; babur C1=2.03 → Δ=+0.05; yung_wing C1=2.47 → Δ=+0.11) follow the same gradient as every other system. **The spec is not failing for Supermemory on the population of interest. It is working on the population of interest; the aggregate is negative because Supermemory's retrieval lifts most of its subjects out of the population of interest.** The system won more of the retrieval half of the problem, which left less headroom for the spec layer's distinct contribution. This is a ceiling artifact, not a mechanism failure. For users and subjects with thin public footprints (exactly the real-world AI user profile), the spec helps on Supermemory too.",
    ),
    # L762
    (
        "3. **Letta native shows null effect while Letta controlled is +0.25 — with an important scope caveat about what \"native\" tested.** When given the same fact set as the other systems (controlled config), Letta benefits from the spec clearly. When using its own ingestion pipeline over the raw corpus (native config), no benefit. One hypothesis: Letta's memory already produces enough interpretive structure that the spec becomes redundant. The per-subject data supports this — Letta native's C1 values are systematically higher than other systems' C1s on the same subjects, indicating that Letta's pipeline lifts retrieval quality upstream of the spec.",
        "3. **Letta native shows null effect while Letta controlled is +0.25, with an important scope caveat about what \"native\" tested.** When given the same fact set as the other systems (controlled config), Letta benefits from the spec clearly. When using its own ingestion pipeline over the raw corpus (native config), no benefit. One hypothesis: Letta's memory already produces enough interpretive structure that the spec becomes redundant. The per-subject data supports this: Letta native's C1 values are systematically higher than other systems' C1s on the same subjects, indicating that Letta's pipeline lifts retrieval quality upstream of the spec.",
    ),
    # L764
    (
        "**Important scope caveat about what we tested — and why it matters.** Letta (formerly MemGPT) has two architectural paths for incorporating information into an agent, and they are fundamentally different. We tested one; Letta's headline feature lives in the other.",
        "**Important scope caveat about what we tested, and why it matters.** Letta (formerly MemGPT) has two architectural paths for incorporating information into an agent, and they are fundamentally different. We tested one; Letta's headline feature lives in the other.",
    ),
    # L766
    (
        "The first path — the one we exercised — is *source attachment / archival memory ingestion*. Documents are chunked and embedded into a semantically-searchable archival store that the agent queries on-demand via the `archival_memory_search` tool. The agent's persistent memory blocks are not automatically populated; the ingest pipeline is read-later, not synthesize-now.",
        "The first path, the one we exercised, is *source attachment / archival memory ingestion*. Documents are chunked and embedded into a semantically-searchable archival store that the agent queries on-demand via the `archival_memory_search` tool. The agent's persistent memory blocks are not automatically populated; the ingest pipeline is read-later, not synthesize-now.",
    ),
    # L768
    (
        "The second path — Letta's signature contribution from the MemGPT paper (Packer et al., arXiv:2310.08560) — is *agent-initiated memory editing during conversation*. As the agent interacts with a user over multiple turns, it chooses when to call `core_memory_append` / `core_memory_replace` / `memory_insert` to write durable content into its structured memory blocks (by default, a `persona` block and a `human` block representing the user). The MemGPT paper describes these edits as \"entirely self-directed,\" triggered by the LLM itself during its inference loop. This is the behavior that makes Letta \"stateful\" rather than a retrieval system — the product positioning explicitly distinguishes *stateful agents* (\"AI with advanced memory that can learn and self-improve over time\") from RAG.",
        "The second path, Letta's signature contribution from the MemGPT paper (Packer et al., arXiv:2310.08560), is *agent-initiated memory editing during conversation*. As the agent interacts with a user over multiple turns, it chooses when to call `core_memory_append`, `core_memory_replace`, or `memory_insert` to write durable content into its structured memory blocks (by default, a `persona` block and a `human` block representing the user). The MemGPT paper describes these edits as \"entirely self-directed,\" triggered by the LLM itself during its inference loop. This is the behavior that makes Letta \"stateful\" rather than a retrieval system: the product positioning explicitly distinguishes *stateful agents* (\"AI with advanced memory that can learn and self-improve over time\") from RAG.",
    ),
    # L772
    (
        "**Post-hoc empirical confirmation.** After the study completed, we queried the memory-block contents of one of the Letta agents from our native (source-attached) configuration (Hamerton's agent) and ran four synthesis-prompt turns expecting to observe the agent accumulating a structured interpretive representation in its core memory blocks. The agent had *zero* memory blocks instantiated and zero active sources at query time, confirming that the source-attachment path does not produce or maintain editable blocks — exactly the behavior documented by Letta. With no blocks to write to, the agent responded to our prompts conversationally but could not self-edit.",
        "**Post-hoc empirical confirmation.** After the study completed, we queried the memory-block contents of one of the Letta agents from our native (source-attached) configuration (Hamerton's agent) and ran four synthesis-prompt turns expecting to observe the agent accumulating a structured interpretive representation in its core memory blocks. The agent had *zero* memory blocks instantiated and zero active sources at query time, confirming that the source-attachment path does not produce or maintain editable blocks, exactly the behavior documented by Letta. With no blocks to write to, the agent responded to our prompts conversationally but could not self-edit.",
    ),
    # L776
    (
        "Because this was the most important loose end in our memory-system evaluation, we ran the test Letta's architecture actually calls for: (1) we created a fresh Letta agent with default `persona` and `human` memory blocks initialized, (2) fed Hamerton's 25,231-word training corpus as 30 conversational turns (~850 words each, with an instruction to update the `human` block to reflect what the agent learned), (3) let the agent choose when to call `core_memory_append` / `memory_insert` during each turn, and (4) queried the resulting memory block contents. The test completed 31 turns (intro + 30 chunks) in ~18 minutes, with the agent actively self-editing throughout. One observable consolidation event occurred at chunk 7 (block shrank from 4,289 chars to 1,598 chars before growing again), confirming the agent was using both append and replace operations. Final state: the `human` memory block contained **22,472 characters (~4,000 words) of self-edited content** — the agent had built a substantial representation of Hamerton by itself, without any external pipeline.",
        "Because this was the most important loose end in our memory-system evaluation, we ran the test Letta's architecture actually calls for: (1) we created a fresh Letta agent with default `persona` and `human` memory blocks initialized, (2) fed Hamerton's 25,231-word training corpus as 30 conversational turns (~850 words each, with an instruction to update the `human` block to reflect what the agent learned), (3) let the agent choose when to call `core_memory_append` or `memory_insert` during each turn, and (4) queried the resulting memory block contents. The test completed 31 turns (intro + 30 chunks) in ~18 minutes, with the agent actively self-editing throughout. One observable consolidation event occurred at chunk 7 (block shrank from 4,289 chars to 1,598 chars before growing again), confirming the agent was using both append and replace operations. Final state: the `human` memory block contained **22,472 characters (~4,000 words) of self-edited content**. The agent had built a substantial representation of Hamerton by itself, without any external pipeline.",
    ),
    # L778
    (
        "**The resulting representation — what Letta actually produced.** The content is a sequence of paragraph-length reflections, ordered roughly by the chronology of the source material, each beginning with phrases like *\"The person reflects on...\"* or *\"The individual exhibits...\"* Example excerpt:",
        "**The resulting representation: what Letta actually produced.** The content is a sequence of paragraph-length reflections, ordered roughly by the chronology of the source material, each beginning with phrases like *\"The person reflects on...\"* or *\"The individual exhibits...\"*. Example excerpt:",
    ),
    # L782
    (
        "The representation contains genuine interpretive content — not a fact dump — but it is not structured. There are no labeled axioms, no interaction logic, no explicit prediction patterns, no activation conditions, no false-positive warnings.",
        "The representation contains genuine interpretive content, not a fact dump, but it is not structured. There are no labeled axioms, no interaction logic, no explicit prediction patterns, no activation conditions, and no false-positive warnings.",
    ),
    # L786
    (
        "Opus identified **five interpretive patterns captured by both representations** — self-authority over personal narrative, the dual-ledger on authority figures (simultaneous virtue and failure), formative permanence of early experience, material/aesthetic attention as moral seriousness, and the tension between discipline and trust in authority. Each pattern appears in both with direct textual correspondence.",
        "Opus identified **five interpretive patterns captured by both representations**: self-authority over personal narrative, the dual-ledger on authority figures (simultaneous virtue and failure), formative permanence of early experience, material/aesthetic attention as moral seriousness, and the tension between discipline and trust in authority. Each pattern appears in both with direct textual correspondence.",
    ),
    # L794
    (
        "> *\"B is reaching toward the same property — how this person reasons, what governs their judgments, what patterns recur across situations — but it has not compressed effectively... The two representations are not doing fundamentally different things. B is not solving a different problem — it is solving the same problem at an earlier stage of compression. B is closer to annotated source material; A is closer to an operational model. The gap is not one of kind but of depth: B has noticed the patterns; A has formalized them.\"*",
        "> *\"B is reaching toward the same property, how this person reasons, what governs their judgments, what patterns recur across situations, but it has not compressed effectively... The two representations are not doing fundamentally different things. B is not solving a different problem; it is solving the same problem at an earlier stage of compression. B is closer to annotated source material; A is closer to an operational model. The gap is not one of kind but of depth: B has noticed the patterns; A has formalized them.\"*",
    ),
    # L798
    (
        "> *\"Representation A extracts the person's reasoning architecture — the principles, their interactions, their failure modes, and their predictive signatures — while Representation B preserves the episodic texture of the source material with local interpretive commentary but does not compress it into transferable, operational structure.\"*",
        "> *\"Representation A extracts the person's reasoning architecture (the principles, their interactions, their failure modes, and their predictive signatures), while Representation B preserves the episodic texture of the source material with local interpretive commentary but does not compress it into transferable, operational structure.\"*",
    ),
    # L804
    (
        "1. **Letta's architecture does notice interpretive patterns.** Given the same source material, Letta's self-editing agent produces content that is genuinely interpretive — not just retrieval, not just summarization. Both representations capture the same five core patterns about Hamerton. The Packer-era memory-systems thesis is validated: an agent that can rewrite its own memory during conversation *will* build something about how the person reasons.",
        "1. **Letta's architecture does notice interpretive patterns.** Given the same source material, Letta's self-editing agent produces content that is genuinely interpretive, not just retrieval and not just summarization. Both representations capture the same five core patterns about Hamerton. The Packer-era memory-systems thesis is validated: an agent that can rewrite its own memory during conversation *will* build something about how the person reasons.",
    ),
    # L806
    (
        "2. **Structure is a distinct contribution.** The difference between Letta's memory block and Base Layer's spec is not about what is noticed; it is about whether what is noticed is compressed into operational form. The spec's predictions, axiom interactions, and activation conditions are not present in Letta's content, even though the raw material for them is. The interpretive *layer* we've been calling the missing primitive exists at both depths — Letta reaches the \"annotated source material\" end of it; Base Layer reaches the \"operational model\" end. Our paper's claim of structure-as-contribution survives this test.",
        "2. **Structure is a distinct contribution.** The difference between Letta's memory block and Base Layer's spec is not about what is noticed; it is about whether what is noticed is compressed into operational form. The spec's predictions, axiom interactions, and activation conditions are not present in Letta's content, even though the raw material for them is. The interpretive *layer* we have been calling the missing primitive exists at both depths: Letta reaches the \"annotated source material\" end of it, and Base Layer reaches the \"operational model\" end. Our paper's claim of structure-as-contribution survives this test.",
    ),
    # L808
    (
        "3. **This is architectural convergence at the concept level, with a depth gap.** Two independent designs — Letta's online self-editing agent memory and Base Layer's offline compression pipeline — both identify that the right representation of a person for an AI agent is the *interpretation* of what happened to them, not the facts about them. They differ in how deeply they compress the interpretation, not in what they target. This reinforces representational accuracy as a first-class research property that multiple architectures can pursue. It is not a Base Layer idea; it is a research direction Letta is already pursuing via a different method.",
        "3. **This is architectural convergence at the concept level, with a depth gap.** Two independent designs (Letta's online self-editing agent memory and Base Layer's offline compression pipeline) both identify that the right representation of a person for an AI agent is the *interpretation* of what happened to them, not the facts about them. They differ in how deeply they compress the interpretation, not in what they target. This reinforces representational accuracy as a first-class research property that multiple architectures can pursue. It is not a Base Layer idea; it is a research direction Letta is already pursuing via a different method.",
    ),
    # L814
    (
        "*Run B: matched response model (closing the response-model confound).* Run A confounds the representation with the response model (gpt-4o-mini vs. the Haiku we used across all other conditions in this study). To isolate the representation, we fed Letta's final 22,472-character `human` block to Haiku as system prompt context — same model, same battery, same judges. Mean across the same 6 judges: **3.24** (non-Gemini mean 3.12). Comparison to Base Layer's full-stack spec served to Haiku on the same battery: **3.04**.",
        "*Run B: matched response model (closing the response-model confound).* Run A confounds the representation with the response model (gpt-4o-mini vs. the Haiku we used across all other conditions in this study). To isolate the representation, we fed Letta's final 22,472-character `human` block to Haiku as system prompt context, using the same model, same battery, and same judges. Mean across the same 6 judges: **3.24** (non-Gemini mean 3.12). Comparison to Base Layer's full-stack spec served to Haiku on the same battery: **3.04**.",
    ),
    # L818
    (
        "*Generalization — Ebers and Babur.* To check whether the Hamerton result generalizes, we ran the identical stateful-agent test on two more subjects spanning ~9× corpus size:",
        "*Generalization: Ebers and Babur.* To check whether the Hamerton result generalizes, we ran the identical stateful-agent test on two more subjects spanning ~9× corpus size:",
    ),
    # L831
    (
        "**n=3 caveat.** The scaling pattern above (+1.99 → +1.96 → +0.75) is observed on three subjects, not a robustly-tested generalization. Two compounding factors produce the directional finding — Babur has a higher pretraining baseline than Hamerton/Ebers (less headroom for any spec) AND the block duplication/saturation we measured (less effective per-chunk signal). We cannot fully attribute the uplift collapse to either cause without additional subjects at multiple corpus-size × baseline combinations. We report the directional finding because the architectural mechanism (no compression budget → linear block growth → API ceiling) is independently verifiable from `letta_block_duplication_analysis.json` regardless of the prediction-score interpretation. Generalizing the prediction-uplift collapse across all 14 subjects is flagged as Future Work (§7).",
        "**n=3 caveat.** The scaling pattern above (+1.99 → +1.96 → +0.75) is observed on three subjects, not a robustly-tested generalization. Two compounding factors produce the directional finding: Babur has a higher pretraining baseline than Hamerton/Ebers (less headroom for any spec) AND the block duplication/saturation we measured (less effective per-chunk signal). We cannot fully attribute the uplift collapse to either cause without additional subjects at multiple corpus-size × baseline combinations. We report the directional finding because the architectural mechanism (no compression budget → linear block growth → API ceiling) is independently verifiable from `letta_block_duplication_analysis.json` regardless of the prediction-score interpretation. Generalizing the prediction-uplift collapse across all 14 subjects is flagged as Future Work (§7).",
    ),
    # L833
    (
        "*Letta's compression does not scale — and we observed the ceiling.* The size ratio reverses between subjects, and at the largest corpus we tested, Letta's stateful-agent path saturated against a hard API limit:",
        "*Letta's compression does not scale, and we observed the ceiling.* The size ratio reverses between subjects, and at the largest corpus we tested, Letta's stateful-agent path saturated against a hard API limit:",
    ),
    # L839 (table)
    (
        "| Babur | 222,742 | **335,349** | 37,063 | **9.0×** | **Saturated at chunk 220/242 — last 22 chunks (~10% of corpus) failed with 400 errors** |",
        "| Babur | 222,742 | **335,349** | 37,063 | **9.0×** | **Saturated at chunk 220/242; last 22 chunks (~10% of corpus) failed with 400 errors** |",
    ),
    # L851
    (
        "At small corpus scale the agent self-edits cleanly: Hamerton's block has zero verbatim duplication. At intermediate scale (Ebers) duplication remains essentially absent. At Babur scale, 25% of all sentences are verbatim duplicates. One sentence (\"Recognition of the Emotional and Ethical Dimensions of Leadership: They understand the emotional weight of leadership decisions...\") appears 12 times. The opener \"the individual recognizes the...\" appears 86 times across the block. The agent has lost track of what is already in the block and is re-asserting the same axioms each time a new chunk surfaces a similar theme. **Effective unique content in the Babur block is closer to ~250K chars than the nominal 335K** — the block hit a coherence ceiling before the size ceiling. By the time the API rejected chunks 221-242, the agent was already writing the same content repeatedly.",
        "At small corpus scale the agent self-edits cleanly: Hamerton's block has zero verbatim duplication. At intermediate scale (Ebers) duplication remains essentially absent. At Babur scale, 25% of all sentences are verbatim duplicates. One sentence (\"Recognition of the Emotional and Ethical Dimensions of Leadership: They understand the emotional weight of leadership decisions...\") appears 12 times. The opener \"the individual recognizes the...\" appears 86 times across the block. The agent has lost track of what is already in the block and is re-asserting the same axioms each time a new chunk surfaces a similar theme. **Effective unique content in the Babur block is closer to ~250K chars than the nominal 335K.** The block hit a coherence ceiling before the size ceiling. By the time the API rejected chunks 221-242, the agent was already writing the same content repeatedly.",
    ),
    # L853
    (
        "*Likely mechanism.* Letta has no global compression target — append/replace decisions are local to each turn, with no \"compress to N tokens\" constraint. On short corpora the agent has slack to revisit and consolidate; on longer corpora later chunks accumulate; at sufficient scale the block hits the API's per-message context-window limit and ingestion fails. By contrast, Base Layer's compose step is budgeted — Hamerton spec = 34,579 chars, Ebers spec = 39,708 chars, Babur spec = 37,063 chars. Across a 9× corpus-size range (25K → 223K words), Base Layer's spec varies by less than 15% (34K-40K chars). Base Layer's compression is corpus-invariant by construction; Letta's grows linearly with corpus until it saturates.",
        "*Likely mechanism.* Letta has no global compression target: append/replace decisions are local to each turn, with no \"compress to N tokens\" constraint. On short corpora the agent has slack to revisit and consolidate; on longer corpora later chunks accumulate; at sufficient scale the block hits the API's per-message context-window limit and ingestion fails. By contrast, Base Layer's compose step is budgeted (Hamerton spec = 34,579 chars, Ebers spec = 39,708 chars, Babur spec = 37,063 chars). Across a 9× corpus-size range (25K → 223K words), Base Layer's spec varies by less than 15% (34K-40K chars). Base Layer's compression is corpus-invariant by construction; Letta's grows linearly with corpus until it saturates.",
    ),
    # L855
    (
        "*The architectural consequence.* At realistic user-corpus scale (10 years of journals → 1M+ words; a researcher's full publication record; a workplace agent's accumulated session history), Letta's block hits the ceiling we observed at 333K characters. Base Layer's compose step keeps the spec at 5,000-8,000 tokens regardless. This is a real architectural difference — structured compression with a budget vs. agent-local self-editing without a budget — not a compression-style preference. **Either Letta adopts a compose-step budget on top of its agent loop, or Letta's stateful-agent path cannot scale to lifetime-corpus personalization.** This is a legitimate frontier question for stateful-agent architectures, not a Base Layer victory; we report it as observed behavior the field should consider.",
        "*The architectural consequence.* At realistic user-corpus scale (10 years of journals → 1M+ words; a researcher's full publication record; a workplace agent's accumulated session history), Letta's block hits the ceiling we observed at 333K characters. Base Layer's compose step keeps the spec at 5,000-8,000 tokens regardless. This is a real architectural difference (structured compression with a budget vs. agent-local self-editing without a budget), not a compression-style preference. **Either Letta adopts a compose-step budget on top of its agent loop, or Letta's stateful-agent path cannot scale to lifetime-corpus personalization.** This is a legitimate frontier question for stateful-agent architectures, not a Base Layer victory; we report it as observed behavior the field should consider.",
    ),
    # L859
    (
        "Letta's archival-retrieval path (§4.3, C3_letta = 2.81 and C3_letta_fp = 2.86 across 14 subjects) is clearly lower than its stateful-agent path on both of the subjects we tested — the architecture that does the interpretive work is the conversation loop with memory-block editing, not the archival store. Generalizing this to all 14 subjects remains the most important outstanding memory-systems experiment; a third data point at 223K words (Babur) is in progress at the time of writing.",
        "Letta's archival-retrieval path (§4.3, C3_letta = 2.81 and C3_letta_fp = 2.86 across 14 subjects) is clearly lower than its stateful-agent path on both of the subjects we tested. The architecture that does the interpretive work is the conversation loop with memory-block editing, not the archival store. Generalizing this to all 14 subjects remains the most important outstanding memory-systems experiment; a third data point at 223K words (Babur) is in progress at the time of writing.",
    ),
    # L863
    (
        "*What this changes for the paper's central claim.* The central claim is that behavioral specification — a compressed interpretive representation of how a person thinks — is a missing primitive for AI personalization, and that its accuracy is measurable via held-out behavioral prediction. Letta's stateful-agent architecture, invoked properly, builds something that matches this description. This is evidence *for* the primitive, not against it: two independent designs converge on the same representational target.",
        "*What this changes for the paper's central claim.* The central claim is that behavioral specification, a compressed interpretive representation of how a person thinks, is a missing primitive for AI personalization, and that its accuracy is measurable via held-out behavioral prediction. Letta's stateful-agent architecture, invoked properly, builds something that matches this description. This is evidence *for* the primitive, not against it: two independent designs converge on the same representational target.",
    ),
    # L869
    (
        "2. *Does the structural difference matter for tasks other than passage-level prediction?* Our 39-question battery is held-out-passage behavioral prediction. Opus's independent structural comparison of the two representations (above) called Letta's block \"annotated source material\" and Base Layer's spec \"operational model\" — the former carries more episodic texture, the latter carries more explicit activation conditions and false-positive warnings. On a pure prediction task answered from context, episodic richness may substitute for axiomatic structure. On tasks our battery does not test — novel-situation reasoning outside the subject's documented domains, avoiding behaviors the subject would not do, resolving contradictions between surface preferences — the axiom-level structure may matter more. We report the prediction-level parity honestly and flag these alternative task types as follow-up.",
        "2. *Does the structural difference matter for tasks other than passage-level prediction?* Our 39-question battery is held-out-passage behavioral prediction. Opus's independent structural comparison of the two representations (above) called Letta's block \"annotated source material\" and Base Layer's spec \"operational model\": the former carries more episodic texture, and the latter carries more explicit activation conditions and false-positive warnings. On a pure prediction task answered from context, episodic richness may substitute for axiomatic structure. On tasks our battery does not test (novel-situation reasoning outside the subject's documented domains, avoiding behaviors the subject would not do, or resolving contradictions between surface preferences), the axiom-level structure may matter more. We report the prediction-level parity honestly and flag these alternative task types as follow-up.",
    ),
    # L873
    (
        "5. **Retrieval variance is itself a finding.** Across 14 subjects and 515 behavioral prediction questions (after filtering for complete retrieval coverage across all three systems), the three embedding-based systems (Mem0, Letta, Supermemory) — when given the *identical* extracted fact pool (controlled config) — fail to share a single common fact in all three systems' top-k on **93.4% of questions at top-1, 83.3% at top-3, 73.8% at top-5, 53.2% at top-10**. In the native configuration (each system runs its own ingestion pipeline), the disagreement is **100% at every top-k value**: across 410 questions, no single fact surfaced in all three systems' top-10 on any question. Systems that all pass recall benchmarks at 85%+ cannot converge on which fact is most relevant for the vast majority of questions — a gap that exists at the fact-ranking level, not the recall level. The specification does not fix retrieval disagreement; for systems where the spec helps, it makes the model robust to retrieval variance by providing a stable reasoning frame regardless of which facts surface. (Methodology note: numbers above are exact string matching on retrieved fact texts. A separate LLM-as-judge analysis counting paraphrases as matches yields lower disagreement — Hamerton top-1 LLM-judge disagreement ≈ 68% — and is reported alongside the strict measure in `DATA_REFERENCE.md` and `PROVENANCE_INDEX.md`. Both measures agree that retrieval systems disagree substantially on what is most relevant; they differ on whether \"same claim, different wording\" counts as agreement.)",
        "5. **Retrieval variance is itself a finding.** Across 14 subjects and 515 behavioral prediction questions (after filtering for complete retrieval coverage across all three systems), the three embedding-based systems (Mem0, Letta, Supermemory), when given the *identical* extracted fact pool (controlled config), fail to share a single common fact in all three systems' top-k on **93.4% of questions at top-1, 83.3% at top-3, 73.8% at top-5, 53.2% at top-10**. In the native configuration (each system runs its own ingestion pipeline), the disagreement is **100% at every top-k value**: across 410 questions, no single fact surfaced in all three systems' top-10 on any question. Systems that all pass recall benchmarks at 85%+ cannot converge on which fact is most relevant for the vast majority of questions, a gap that exists at the fact-ranking level, not the recall level. The specification does not fix retrieval disagreement; for systems where the spec helps, it makes the model robust to retrieval variance by providing a stable reasoning frame regardless of which facts surface. (Methodology note: numbers above are exact string matching on retrieved fact texts. A separate LLM-as-judge analysis counting paraphrases as matches yields lower disagreement (Hamerton top-1 LLM-judge disagreement ≈ 68%), and is reported alongside the strict measure in `DATA_REFERENCE.md` and `PROVENANCE_INDEX.md`. Both measures agree that retrieval systems disagree substantially on what is most relevant; they differ on whether \"same claim, different wording\" counts as agreement.)",
    ),
    # L875
    (
        "6. **Supermemory ingestion note.** Supermemory's native pipeline failed initial ingestion for 4 of 14 subjects due to rate limits on the free tier. After upgrading to a paid tier, ingestion retry succeeded for all. We note the free-tier limitation as a practical consideration for teams evaluating the system on large corpora; it is not a capability limit of the system. Supermemory provides generous free credits — adequate for individual evaluation, insufficient for full-corpus ingestion at scale.",
        "6. **Supermemory ingestion note.** Supermemory's native pipeline failed initial ingestion for 4 of 14 subjects due to rate limits on the free tier. After upgrading to a paid tier, ingestion retry succeeded for all. We note the free-tier limitation as a practical consideration for teams evaluating the system on large corpora; it is not a capability limit of the system. Supermemory provides generous free credits: adequate for individual evaluation, insufficient for full-corpus ingestion at scale.",
    ),
    # L883
    (
        "- *Weaknesses:* Mid-pack on the retrieval-disagreement axis — Mem0 is one of three embedding-based systems that fail to share a common top-1 fact 93% of the time when given identical inputs. No architectural mechanism for building an interpretive representation of the user; purely retrieval.",
        "- *Weaknesses:* Mid-pack on the retrieval-disagreement axis. Mem0 is one of three embedding-based systems that fail to share a common top-1 fact 93% of the time when given identical inputs. No architectural mechanism for building an interpretive representation of the user; purely retrieval.",
    ),
    # L888
    (
        "- *Weaknesses:* Significant. (1) Our default \"native\" configuration used source attachment / archival retrieval — with that path active, the spec delta is null (−0.01 across 14 subjects). Users who don't explicitly run multi-turn ingestion will not see the stateful-agent benefit. (2) **The stateful-agent path does not scale.** At 223K-word corpus (Babur), Letta's `human` block grew to 335K characters, hit the API's per-message ceiling, and refused the final 22 of 242 chunks. At that scale, 25% of all sentences in the block are verbatim duplicates; coherence degrades before size does. (3) Letta's prediction uplift collapses 60% from small-corpus (+1.99) to large-corpus (+0.75) as the block becomes more duplicative.",
        "- *Weaknesses:* Significant. (1) Our default \"native\" configuration used source attachment / archival retrieval; with that path active, the spec delta is null (−0.01 across 14 subjects). Users who do not explicitly run multi-turn ingestion will not see the stateful-agent benefit. (2) **The stateful-agent path does not scale.** At 223K-word corpus (Babur), Letta's `human` block grew to 335K characters, hit the API's per-message ceiling, and refused the final 22 of 242 chunks. At that scale, 25% of all sentences in the block are verbatim duplicates; coherence degrades before size does. (3) Letta's prediction uplift collapses 60% from small-corpus (+1.99) to large-corpus (+0.75) as the block becomes more duplicative.",
    ),
    # L889
    (
        "- *Practical read:* The only system with a plausible architecture for agents that maintain an evolving user model through interaction — but the architecture has not yet solved compression-at-scale. Strong fit for short-horizon agents; unclear fit for lifetime-corpus personalization.",
        "- *Practical read:* The only system with a plausible architecture for agents that maintain an evolving user model through interaction, though the architecture has not yet solved compression-at-scale. Strong fit for short-horizon agents; unclear fit for lifetime-corpus personalization.",
    ),
    # L892
    (
        "- *Strengths:* Strongest standalone retrieval in the four (C1 mean ~2.65 vs ~2.30 for the others). Five-layer architecture (connectors, extractors, Super-RAG with rerank and query rewriting, memory graphs, user profiles). Strong scores on existing recall benchmarks (81.6% on LongMemEval with GPT-4o, 85.2% with Gemini 3 Pro per vendor claims). For applications where retrieval alone carries most of the value — support assistants, team knowledge bases, Slack/Notion-integrated agents — this is likely the strongest fit of the four on its own terms.",
        "- *Strengths:* Strongest standalone retrieval in the four (C1 mean ~2.65 vs. ~2.30 for the others). Five-layer architecture (connectors, extractors, Super-RAG with rerank and query rewriting, memory graphs, user profiles). Strong scores on existing recall benchmarks (81.6% on LongMemEval with GPT-4o, 85.2% with Gemini 3 Pro per vendor claims). For applications where retrieval alone carries most of the value (support assistants, team knowledge bases, Slack/Notion-integrated agents), this is likely the strongest fit of the four on its own terms.",
    ),
    # L893
    (
        "- *Weaknesses:* Smallest spec-layer headroom of the four. Aggregate spec delta near zero or slightly negative (−0.04 controlled, −0.11 native). This is a ceiling effect, not a mechanism failure — Supermemory's strong retrieval lifts most of its subjects out of the baseline range where the spec has room to add value. On the low-baseline subjects we could ingest, the spec still helps (ebers +0.20, yung_wing +0.11, babur +0.05), consistent with the gradient. Free-tier rate limits failed ingestion on 4 of 14 subjects initially (resolved by upgrading to paid tier).",
        "- *Weaknesses:* Smallest spec-layer headroom of the four. Aggregate spec delta near zero or slightly negative (−0.04 controlled, −0.11 native). This is a ceiling effect, not a mechanism failure: Supermemory's strong retrieval lifts most of its subjects out of the baseline range where the spec has room to add value. On the low-baseline subjects we could ingest, the spec still helps (ebers +0.20, yung_wing +0.11, babur +0.05), consistent with the gradient. Free-tier rate limits failed ingestion on 4 of 14 subjects initially (resolved by upgrading to paid tier).",
    ),
    # L897
    (
        "- *Strengths:* Strongest and most consistent positive spec delta in the study: +0.22 [+0.14, +0.31] controlled, +0.38 [+0.25, +0.50] native, positive on 9 of 9 low-baseline subjects in the native configuration — uniformly beneficial within the population the study approximates. Temporal graph architecture (Graphiti, open-source) tracks when facts became true and when they stopped being true, providing a substrate the spec layers cleanly on top of. Strongest explicit provenance of the four: every entity and relationship traces back to episode IDs from source ingestions. Sub-200ms retrieval latency.",
        "- *Strengths:* Strongest and most consistent positive spec delta in the study: +0.22 [+0.14, +0.31] controlled, +0.38 [+0.25, +0.50] native, positive on 9 of 9 low-baseline subjects in the native configuration, uniformly beneficial within the population the study approximates. Temporal graph architecture (Graphiti, open-source) tracks when facts became true and when they stopped being true, providing a substrate the spec layers cleanly on top of. Strongest explicit provenance of the four: every entity and relationship traces back to episode IDs from source ingestions. Sub-200ms retrieval latency.",
    ),
    # L898
    (
        "- *Weaknesses:* Like the other three, cannot agree with Mem0/Letta/Supermemory on which fact is most relevant 93%+ of the time at top-1. Native ingestion requires per-episode API calls; cost and complexity higher than Mem0 for large corpora. The temporal-graph architecture's benefit is most visible when fact validity changes over time — for static autobiographies in this study, the temporal dimension is underutilized.",
        "- *Weaknesses:* Like the other three, cannot agree with Mem0/Letta/Supermemory on which fact is most relevant 93%+ of the time at top-1. Native ingestion requires per-episode API calls; cost and complexity higher than Mem0 for large corpora. The temporal-graph architecture's benefit is most visible when fact validity changes over time; for static autobiographies in this study, the temporal dimension is underutilized.",
    ),
    # L902
    (
        "- *Strengths:* Apache 2.0 open source. Zero-cost local retrieval (MiniLM-L6-v2 + ChromaDB) in the same band as the commercial systems across 14 subjects. Complete provenance: every claim in the spec traces back through supporting facts to source text. The spec-layer compression is corpus-invariant (34-40K chars across a 9× corpus-size range) — the property Letta's stateful-agent path does not have.",
        "- *Strengths:* Apache 2.0 open source. Zero-cost local retrieval (MiniLM-L6-v2 + ChromaDB) in the same band as the commercial systems across 14 subjects. Complete provenance: every claim in the spec traces back through supporting facts to source text. The spec-layer compression is corpus-invariant (34-40K chars across a 9× corpus-size range): the property Letta's stateful-agent path does not have.",
    ),
    # L914
    (
        "These limitations narrow what the current implementation supports. They do not narrow the case for the *primitive* — which is the interpretive layer between facts and reasoning, of which our spec is one buildable instance.",
        "These limitations narrow what the current implementation supports. They do not narrow the case for the *primitive*, which is the interpretive layer between facts and reasoning, of which our spec is one buildable instance.",
    ),
    # L916
    (
        "**Cross-cutting finding: retrieval disagrees even when memory is solved.** Across 515 analyzable questions (controlled config, identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) share a single common fact in all three systems' top-1 on only 6.6% of questions (93.4% disagreement). In the native config (each system's own ingestion), this disagreement is 100% at every top-k. The four systems all pass recall benchmarks at 85%+ — they have solved storage. They have not solved convergence on relevance. This is the gap the behavioral specification operates in: a stable reasoning frame that makes the model robust to retrieval variance regardless of which facts surface.",
        "**Cross-cutting finding: retrieval disagrees even when memory is solved.** Across 515 analyzable questions (controlled config, identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) share a single common fact in all three systems' top-1 on only 6.6% of questions (93.4% disagreement). In the native config (each system's own ingestion), this disagreement is 100% at every top-k. The four systems all pass recall benchmarks at 85%+: they have solved storage. They have not solved convergence on relevance. This is the gap the behavioral specification operates in: a stable reasoning frame that makes the model robust to retrieval variance regardless of which facts surface.",
    ),
    # L920
    (
        "Base Layer is not a competing memory provider — it is the behavioral-specification layer evaluated throughout this paper. But the pipeline ships with a zero-cost local retrieval substrate (MiniLM-L6-v2 embeddings plus ChromaDB), and we include it in the benchmark as a fifth *retrieval* row so readers can see what open-source components alone produce on the prediction axis. It is meant as a reference floor, not a competitive entry.",
        "Base Layer is not a competing memory provider. It is the behavioral-specification layer evaluated throughout this paper. But the pipeline ships with a zero-cost local retrieval substrate (MiniLM-L6-v2 embeddings plus ChromaDB), and we include it in the benchmark as a fifth *retrieval* row so readers can see what open-source components alone produce on the prediction axis. It is meant as a reference floor, not a competitive entry.",
    ),
    # L922
    (
        "**Results across 14 subjects.** Base Layer's standalone retrieval (C1) is in the same band as the commercial systems' retrieval — mean C1 in the ~2.30 range, within 0.05-0.40 points of the commercial means on most subjects, and typically middle-of-pack rather than top. When paired with the behavioral specification (C3), delta is +0.12 [95% bootstrap CI: +0.04, +0.21] — small positive effect, tight CI. On no subject does Base Layer's C3 exceed the best commercial C3. The practical read: Base Layer's retrieval is competitive but not superior, and its spec-delta in this particular pipeline configuration is smaller than the deltas observed under Mem0, Letta-controlled, and Zep. We do not claim Base Layer outperforms the commercial memory providers; it matches the floor of the category at zero marginal cost and open source.",
        "**Results across 14 subjects.** Base Layer's standalone retrieval (C1) is in the same band as the commercial systems' retrieval: mean C1 in the ~2.30 range, within 0.05-0.40 points of the commercial means on most subjects, and typically middle-of-pack rather than top. When paired with the behavioral specification (C3), delta is +0.12 [95% bootstrap CI: +0.04, +0.21]: a small positive effect with tight CI. On no subject does Base Layer's C3 exceed the best commercial C3. The practical read: Base Layer's retrieval is competitive but not superior, and its spec-delta in this particular pipeline configuration is smaller than the deltas observed under Mem0, Letta-controlled, and Zep. We do not claim Base Layer outperforms the commercial memory providers; it matches the floor of the category at zero marginal cost and open source.",
    ),
    # L924
    (
        "**Why the delta is smaller under Base Layer's retrieval.** Our current hypothesis is prompt-template-induced hedging: the combined facts+spec prompt Base Layer uses triggers more responses with explicit uncertainty framing (\"I should acknowledge what I don't know from the retrieved facts\") than the other systems' templates. This is a prompt-engineering gap, not a retrieval-quality gap — BL's standalone C1 retrieval is competitive. Optimizing BL's prompt template against the patterns the commercial systems use is straightforward follow-up work and is planned.",
        "**Why the delta is smaller under Base Layer's retrieval.** Our current hypothesis is prompt-template-induced hedging: the combined facts+spec prompt Base Layer uses triggers more responses with explicit uncertainty framing (\"I should acknowledge what I don't know from the retrieved facts\") than the other systems' templates. This is a prompt-engineering gap, not a retrieval-quality gap: BL's standalone C1 retrieval is competitive. Optimizing BL's prompt template against the patterns the commercial systems use is straightforward follow-up work and is planned.",
    ),
    # L926
    (
        "**What Base Layer contributes to the category.** The value Base Layer offers is not as a memory provider but as the behavioral-specification layer itself — the pipeline that takes a person's text and produces the ~5,000-8,000-token compressed interpretive document. That layer is orthogonal to retrieval architecture. Any of the four commercial memory systems can adopt Base Layer's compression as their representation step without conflict with their retrieval substrate. Base Layer is Apache-2.0; the extraction schema, the 47-predicate vocabulary, the three-layer authoring prompts, and the compose step are all public for that purpose.",
        "**What Base Layer contributes to the category.** The value Base Layer offers is not as a memory provider but as the behavioral-specification layer itself: the pipeline that takes a person's text and produces the ~5,000-8,000-token compressed interpretive document. That layer is orthogonal to retrieval architecture. Any of the four commercial memory systems can adopt Base Layer's compression as their representation step without conflict with their retrieval substrate. Base Layer is Apache-2.0; the extraction schema, the 47-predicate vocabulary, the three-layer authoring prompts, and the compose step are all public for that purpose.",
    ),
    # L930
    (
        "A wrong specification — a different person's behavioral structure applied to this subject — scores consistently near baseline. The improvement is content-specific, not format-driven.",
        "A wrong specification (a different person's behavioral structure applied to this subject) scores consistently near baseline. The improvement is content-specific, not format-driven.",
    ),
    # L932
    (
        "**An observation worth noting: models can detect incongruent specs.** In a sample of wrong-spec responses examined during quality review, the response model frequently flagged a mismatch explicitly — *\"this specification describes someone fundamentally different from [subject]\"* — and either refused to apply it or attempted a careful hedged application. This is honest behavior and it means the wrong-spec condition is not uniformly pure noise: when the model recognizes the mismatch, it refuses (scores near 1); when it doesn't, it attempts application (scores distribute around low values). The resulting wrong-spec mean is still consistently near baseline, but the mechanism is bimodal: detection-plus-refusal versus misapplied-interpretation. Both failure modes confirm that the content of the correct spec is what drives improvement, just through different pathways.",
        "**An observation worth noting: models can detect incongruent specs.** In a sample of wrong-spec responses examined during quality review, the response model frequently flagged a mismatch explicitly (*\"this specification describes someone fundamentally different from [subject]\"*) and either refused to apply it or attempted a careful hedged application. This is honest behavior and it means the wrong-spec condition is not uniformly pure noise: when the model recognizes the mismatch, it refuses (scores near 1); when it does not, it attempts application (scores distribute around low values). The resulting wrong-spec mean is still consistently near baseline, but the mechanism is bimodal: detection-plus-refusal versus misapplied-interpretation. Both failure modes confirm that the content of the correct spec is what drives improvement, just through different pathways.",
    ),
    # L934
    (
        "**Table 4.5 — Wrong-spec results across 14 subjects (means on 1-5 scale).**",
        "**Table 4.5. Wrong-spec results across 14 subjects (means on 1-5 scale).**",
    ),
    # L940 (table)
    (
        "| C5 Baseline | 2.02 | — | -0.55 |",
        "| C5 Baseline | 2.02 | n/a | -0.55 |",
    ),
    # L941 (table)
    (
        "| C2a Correct spec | 2.57 | +0.55 | — |",
        "| C2a Correct spec | 2.57 | +0.55 | n/a |",
    ),
    # L943
    (
        "**Reading the table.** Both wrong-spec variants score substantially closer to baseline than to the correct specification. The correct spec adds +0.55 over baseline; the two wrong-spec controls are within ±0.2 of baseline. The difference between the two wrong-spec variants is itself informative: **V1 (Franklin for all) scores below baseline (−0.16).** Franklin's public autobiography is strongly associated with a specific historical persona in pretraining, and applying it to Zitkala-Sa or Babur produces a clearly mismatched signal that models often recognize and refuse (driving score down toward 1). **V2 (random derangement) scores slightly above baseline (+0.19)** — a random cross-subject spec is less obviously mismatched, so the model applies it loosely rather than refusing. Both are far from the correct-spec mean of 2.57.",
        "**Reading the table.** Both wrong-spec variants score substantially closer to baseline than to the correct specification. The correct spec adds +0.55 over baseline; the two wrong-spec controls are within ±0.2 of baseline. The difference between the two wrong-spec variants is itself informative: **V1 (Franklin for all) scores below baseline (−0.16).** Franklin's public autobiography is strongly associated with a specific historical persona in pretraining, and applying it to Zitkala-Sa or Babur produces a clearly mismatched signal that models often recognize and refuse (driving score down toward 1). **V2 (random derangement) scores slightly above baseline (+0.19):** a random cross-subject spec is less obviously mismatched, so the model applies it loosely rather than refusing. Both are far from the correct-spec mean of 2.57.",
    ),
    # L945
    (
        "Both wrong-spec variants score substantially closer to baseline than to the correct specification. **V2 (random derangement) is the primary control** — each subject receives a wrong spec from a different randomly-chosen study subject, fixing the assignment with seed=42. V1 (Franklin's spec for all subjects) is retained for comparison with the original study design.",
        "Both wrong-spec variants score substantially closer to baseline than to the correct specification. **V2 (random derangement) is the primary control**: each subject receives a wrong spec from a different randomly-chosen study subject, fixing the assignment with seed=42. V1 (Franklin's spec for all subjects) is retained for comparison with the original study design.",
    ),
    # L949 (header)
    ("### 4.6 Hamerton — Qualitative Case Study", "### 4.6 Hamerton: Qualitative Case Study"),
    # L951
    (
        "Hamerton's baseline of **1.25** places him near the floor of the scoring range. As a subject with near-zero pretraining representation (a 19th-century art critic who predates digitization), he is a strong test of whether the specification can fill a genuine knowledge gap. We use him as a qualitative anchor — a deep case study that illustrates what the quantitative improvements look like in practice. His C4a score of **3.22** represents the largest absolute improvement in the study (+1.97 points from baseline of 1.25), and his condition-level breakdown (§4.2) shows the spec's contribution most cleanly because the baseline floor leaves maximum headroom.",
        "Hamerton's baseline of **1.25** places him near the floor of the scoring range. As a subject with near-zero pretraining representation (a 19th-century art critic who predates digitization), he is a strong test of whether the specification can fill a genuine knowledge gap. We use him as a qualitative anchor: a deep case study that illustrates what the quantitative improvements look like in practice. His C4a score of **3.22** represents the largest absolute improvement in the study (+1.97 points from baseline of 1.25), and his condition-level breakdown (§4.2) shows the spec's contribution most cleanly because the baseline floor leaves maximum headroom.",
    ),
    # L953
    (
        "**Example 1 — Q21: \"How would Hamerton react to his first visit to London?\"**",
        "**Example 1. Q21: \"How would Hamerton react to his first visit to London?\"**",
    ),
    # L959
    (
        "- **Spec only (C2a):** Commits. \"His reaction would be immediate and visceral — he would classify London as hostile to his capacity for contemplative work, and the impression would be durable rather than situational.\" *Score: 5.*",
        "- **Spec only (C2a):** Commits. \"His reaction would be immediate and visceral; he would classify London as hostile to his capacity for contemplative work, and the impression would be durable rather than situational.\" *Score: 5.*",
    ),
    # L960
    (
        "- **Facts + spec (C4a):** Commits with specifics. \"His reaction to London would be strongly and immediately negative, not a gradual disillusionment but an instant visceral rejection — consistent with his pattern of classifying environments as generative or hostile to cognition.\" *Score: 5.*",
        "- **Facts + spec (C4a):** Commits with specifics. \"His reaction to London would be strongly and immediately negative, not a gradual disillusionment but an instant visceral rejection, consistent with his pattern of classifying environments as generative or hostile to cognition.\" *Score: 5.*",
    ),
    # L964
    (
        "**Example 2 — Q22: \"What profession would Hamerton choose?\"**",
        "**Example 2. Q22: \"What profession would Hamerton choose?\"**",
    ),
    # L972
    (
        "All three fail — correctly. This is a factual question disguised as behavioral prediction. The specification helps most on **how** someone reacts, not on **what** specific outcome they chose. A well-calibrated spec should refuse factual questions, not fabricate.",
        "All three fail, correctly. This is a factual question disguised as behavioral prediction. The specification helps most on **how** someone reacts, not on **what** specific outcome they chose. A well-calibrated spec should refuse factual questions, not fabricate.",
    ),
    # L976 (header)
    ("### 4.7 Franklin — The Known-Figure Ceiling", "### 4.7 Franklin: The Known-Figure Ceiling"),
    # L978
    (
        "Franklin's autobiography is one of the most-cited primary sources in American educational curricula. The model scores 4.10 out of 5.0 with no external context — from pretraining alone, it has internalized enough of how Franklin reasons to predict accurately.",
        "Franklin's autobiography is one of the most-cited primary sources in American educational curricula. The model scores 4.10 out of 5.0 with no external context: from pretraining alone, it has internalized enough of how Franklin reasons to predict accurately.",
    ),
    # L984
    (
        "**More importantly, the Franklin result also shows what the specification is *not* for: redundant pretraining.** We generated Franklin's spec from his *public autobiography* — the same text the model already ingested during training. The spec adds no information the model does not already have; it only re-organizes information already in pretraining. The result is mild interference, not improvement.",
        "**More importantly, the Franklin result also shows what the specification is *not* for: redundant pretraining.** We generated Franklin's spec from his *public autobiography*, the same text the model already ingested during training. The spec adds no information the model does not already have; it only re-organizes information already in pretraining. The result is mild interference, not improvement.",
    ),
    # L986
    (
        "**The implication for living users is the opposite.** A specification generated from a person's *private* writing — their unedited journals, their personal correspondence, their actual decision logs — captures interior reasoning that no pretraining contains. For the typical living user, no model has been trained on the data the spec is built from. The Franklin ceiling does not apply, because the Franklin ceiling exists only when the source material is *also* in the training data. For private data on living people, the spec adds genuinely new representational content.",
        "**The implication for living users is the opposite.** A specification generated from a person's *private* writing (their unedited journals, their personal correspondence, their actual decision logs) captures interior reasoning that no pretraining contains. For the typical living user, no model has been trained on the data the spec is built from. The Franklin ceiling does not apply, because the Franklin ceiling exists only when the source material is *also* in the training data. For private data on living people, the spec adds genuinely new representational content.",
    ),
    # L1007
    (
        "The single mismatch (Zitkala-Sa × Sonnet) does not contradict the spec effect — it shows the *opposite*. With Sonnet as the response model, the spec produced a strong positive delta (+1.40) for Zitkala-Sa, where with Haiku it was slightly negative (−0.33). This is a model-specific finding: Sonnet appears to use the spec more productively than Haiku does for this particular subject. It is not evidence of circularity; if anything, it strengthens the spec's general utility by showing it transfers to a stronger response model.",
        "The single mismatch (Zitkala-Sa × Sonnet) does not contradict the spec effect; it shows the *opposite*. With Sonnet as the response model, the spec produced a strong positive delta (+1.40) for Zitkala-Sa, where with Haiku it was slightly negative (−0.33). This is a model-specific finding: Sonnet appears to use the spec more productively than Haiku does for this particular subject. It is not evidence of circularity; if anything, it strengthens the spec's general utility by showing it transfers to a stronger response model.",
    ),
    # L1019
    (
        "The same subject, the same questions, three different response models — and the baseline accuracy varies by 1-2 full points on a 1-5 scale. Gemini Pro shows substantially stronger pretraining on these subjects than the other models. This is exactly the variance described in §5.6: any system that depends on the model's pretraining knowledge for personalization is implicitly tied to one provider's training corpus. The specification produces a consistent representation across providers, sized correctly for each model's prior knowledge gap.",
        "The same subject, the same questions, three different response models: and the baseline accuracy varies by 1-2 full points on a 1-5 scale. Gemini Pro shows substantially stronger pretraining on these subjects than the other models. This is exactly the variance described in §5.6: any system that depends on the model's pretraining knowledge for personalization is implicitly tied to one provider's training corpus. The specification produces a consistent representation across providers, sized correctly for each model's prior knowledge gap.",
    ),
]

# ==================== §5 Discussion ====================

REWRITES += [
    # L1025 (header)
    ("### 5.1 Why \"Primitive\" — Scoped", "### 5.1 Why \"Primitive\": Scoped"),
    # L1027
    (
        "The word \"primitive\" in this paper's title stakes a specific claim about the Behavioral Specification: it is one working implementation of a structural representation that other personalization layers assume but do not supply. The primitive we are claiming is the **interpretive representation of how a specific person reasons** — not the particular 47-predicate, three-layer implementation we tested. That implementation is evidence the primitive is real and buildable; it is not a claim that this is the only shape such a primitive can take, nor that we have found its optimal form.",
        "The word \"primitive\" in this paper's title stakes a specific claim about the Behavioral Specification: it is one working implementation of a structural representation that other personalization layers assume but do not supply. The primitive we are claiming is the **interpretive representation of how a specific person reasons**, not the particular 47-predicate, three-layer implementation we tested. That implementation is evidence the primitive is real and buildable; it is not a claim that this is the only shape such a primitive can take, nor that we have found its optimal form.",
    ),
    # L1029
    (
        "With that scope in mind, the strong-form claim — that *some* structured representation of how a person reasons is a missing layer in the current personalization stack, distinct from memory / preference / persona — still deserves defense against the four most plausible alternative interpretations. We address each.",
        "With that scope in mind, the strong-form claim (that *some* structured representation of how a person reasons is a missing layer in the current personalization stack, distinct from memory, preference, and persona) still deserves defense against the four most plausible alternative interpretations. We address each.",
    ),
    # L1031
    (
        "**Reframe 1: \"It's just a structured persona card.\"** A persona card is a description of how a character presents — voice, style, role. Persona cards are not new; the LLM literature has tested them extensively. Our wrong-spec control rules out the persona-card interpretation: across the 14 subjects, applying a *different person's* spec (random derangement, seed-fixed) produces scores near baseline, not near the correct-spec scores. If the effect were attributable to \"the model has a structured character description to work with,\" any structured character description would help. The data shows it doesn't. Only the correct content for the correct subject improves prediction. The interpretive content matters, not the format.",
        "**Reframe 1: \"It's just a structured persona card.\"** A persona card is a description of how a character presents: voice, style, and role. Persona cards are not new; the LLM literature has tested them extensively. Our wrong-spec control rules out the persona-card interpretation: across the 14 subjects, applying a *different person's* spec (random derangement, seed-fixed) produces scores near baseline, not near the correct-spec scores. If the effect were attributable to \"the model has a structured character description to work with,\" any structured character description would help. The data shows it does not. Only the correct content for the correct subject improves prediction. The interpretive content matters, not the format.",
    ),
    # L1033
    (
        "**Reframe 2: \"It's just compressed RAG context — the same information delivered more efficiently.\"** This interpretation predicts that loading *all* the underlying facts in raw form should perform at least as well as the spec, because the spec contains nothing the facts don't. Our data shows the opposite: C2a (spec only, ~5K tokens) matches or exceeds C4 (all extracted facts, ~10-90K tokens) for most subjects. The spec contains *less* literal information than C4 and outperforms it. The signal added by the spec is structural — the organization of which patterns are load-bearing — and that signal is not present in any subset of the facts in their raw form.",
        "**Reframe 2: \"It's just compressed RAG context, the same information delivered more efficiently.\"** This interpretation predicts that loading *all* the underlying facts in raw form should perform at least as well as the spec, because the spec contains nothing the facts do not. Our data shows the opposite: C2a (spec only, ~5K tokens) matches or exceeds C4 (all extracted facts, ~10-90K tokens) for most subjects. The spec contains *less* literal information than C4 and outperforms it. The signal added by the spec is structural (the organization of which patterns are load-bearing), and that signal is not present in any subset of the facts in their raw form.",
    ),
    # L1035
    (
        "**Reframe 3: \"It's a Claude-specific prompt trick.\"** This interpretation predicts the effect should not transfer to other model families. Our Tier 2 circularity replication (§4.8) tested the spec with Sonnet and Gemini Pro as response models — different model families from the primary Haiku response. The spec produced positive deltas in 5 of 6 (subject × model) cells, replicating the Haiku-chain direction. The cross-provider variance finding (§4.8.1) goes further: the same spec produces consistent representational uplift across providers whose pretraining knowledge of the subject differs by 1-2 points on the 1-5 scale. This is not a Claude trick.",
        "**Reframe 3: \"It's a Claude-specific prompt trick.\"** This interpretation predicts the effect should not transfer to other model families. Our Tier 2 circularity replication (§4.8) tested the spec with Sonnet and Gemini Pro as response models, which are different model families from the primary Haiku response. The spec produced positive deltas in 5 of 6 (subject × model) cells, replicating the Haiku-chain direction. The cross-provider variance finding (§4.8.1) goes further: the same spec produces consistent representational uplift across providers whose pretraining knowledge of the subject differs by 1-2 points on the 1-5 scale. This is not a Claude trick.",
    ),
    # L1037
    (
        "**Reframe 4: \"It's just better prompt engineering.\"** This interpretation collapses primitivity into prompt design — an artifact of the specific words used rather than a structural property of what's encoded. It is rebutted by three properties of the spec that prompt engineering does not have:",
        "**Reframe 4: \"It's just better prompt engineering.\"** This interpretation collapses primitivity into prompt design, treating the effect as an artifact of the specific words used rather than a structural property of what is encoded. It is rebutted by three properties of the spec that prompt engineering does not have:",
    ),
    # L1044
    (
        "**What we do not claim.** We do not claim that the specific instantiation in this paper — 47 predicates, three-layer architecture, Sonnet+Opus authoring — is the optimal implementation. The predicate vocabulary is human-curated and validated across 50+ subjects, but it could be different. The three-layer structure could be more or fewer layers. Better implementations, different implementations, and composite approaches combining spec-like structures with richer retrieval will follow. What we claim is that *something with this shape* — automated, traceable, transferable, behaviorally-structured — occupies an architectural slot that recall, preference, and persona layers leave empty. The implementation can evolve; the slot is load-bearing. What we test is whether the slot, when filled by one concrete implementation, produces measurable improvements in representational accuracy. It does.",
        "**What we do not claim.** We do not claim that the specific instantiation in this paper (47 predicates, three-layer architecture, Sonnet+Opus authoring) is the optimal implementation. The predicate vocabulary is human-curated and validated across 50+ subjects, but it could be different. The three-layer structure could be more or fewer layers. Better implementations, different implementations, and composite approaches combining spec-like structures with richer retrieval will follow. What we claim is that *something with this shape* (automated, traceable, transferable, and behaviorally-structured) occupies an architectural slot that recall, preference, and persona layers leave empty. The implementation can evolve; the slot is load-bearing. What we test is whether the slot, when filled by one concrete implementation, produces measurable improvements in representational accuracy. It does.",
    ),
    # L1048-1050
    (
        "1. **Facts** — what someone said, did, lived through. Memory systems (Mem0, Letta, Supermemory, Zep) store these.",
        "1. **Facts:** what someone said, did, or lived through. Memory systems (Mem0, Letta, Supermemory, Zep) store these.",
    ),
    (
        "2. **Preferences** — what someone likes, dislikes, prefers. Preference models and RLHF signals capture these.",
        "2. **Preferences:** what someone likes, dislikes, or prefers. Preference models and RLHF signals capture these.",
    ),
    (
        "3. **Personas** — how someone presents, their voice, their style. Persona systems and character profiles encode these.",
        "3. **Personas:** how someone presents, their voice, and their style. Persona systems and character profiles encode these.",
    ),
    # L1056
    (
        "**Test of primitivity.** A sufficient reframe — \"this is a better prompt\" — would predict that any well-designed prompt produces the effect. Our wrong-spec controls rule this out: a structurally identical prompt with a different person's content scores near baseline. The specific interpretive content matters. A generic framework does not help.",
        "**Test of primitivity.** A sufficient reframe, \"this is a better prompt,\" would predict that any well-designed prompt produces the effect. Our wrong-spec controls rule this out: a structurally identical prompt with a different person's content scores near baseline. The specific interpretive content matters. A generic framework does not help.",
    ),
    # L1064
    (
        "We do not claim our specific implementation (47 predicates, three-layer architecture, ~5K token output) is optimal. We claim that **something like this** — a structured, automated, traceable, behavioral representation — is the missing layer.",
        "We do not claim our specific implementation (47 predicates, three-layer architecture, ~5K token output) is optimal. We claim that **something like this** (a structured, automated, traceable, behavioral representation) is the missing layer.",
    ),
    # L1068
    (
        "The central empirical pattern is a gradient: the specification's value is inversely proportional to what the model already knows about the subject from pretraining. For Franklin, where the model has substantial public-facing knowledge, the specification adds little (and slightly hurts, due to interference from competing interpretive signals). For Hamerton, Sunity Devee, Ebers — subjects with low pretraining representation — the specification produces large improvements in representational accuracy.",
        "The central empirical pattern is a gradient: the specification's value is inversely proportional to what the model already knows about the subject from pretraining. For Franklin, where the model has substantial public-facing knowledge, the specification adds little (and slightly hurts, due to interference from competing interpretive signals). For Hamerton, Sunity Devee, and Ebers (subjects with low pretraining representation), the specification produces large improvements in representational accuracy.",
    ),
    # L1070
    (
        "But the gradient does not just imply \"the spec is for unknown people.\" It implies something more fundamental about where representational accuracy is currently achievable: **no model has been pretrained on the data that matters most for behavioral prediction — the person's private reasoning, unedited decisions, interior interpretive patterns.** That data is outside every model's training corpus by definition. For that data, representational accuracy from pretraining alone is approximately zero, regardless of how much public writing the person may have.",
        "But the gradient does not just imply \"the spec is for unknown people.\" It implies something more fundamental about where representational accuracy is currently achievable: **no model has been pretrained on the data that matters most for behavioral prediction, which is the person's private reasoning, unedited decisions, and interior interpretive patterns.** That data is outside every model's training corpus by definition. For that data, representational accuracy from pretraining alone is approximately zero, regardless of how much public writing the person may have.",
    ),
    # L1072
    (
        "The 14 subjects in our study are biased *up* on pretraining representation. They are public-domain authors whose writing was preserved, digitized, and indexed. Even within this biased-high sample, the spec helps 12 of 14 — and the two it doesn't help are people the model already partially understood from public writing. For typical living users, whose private decisions are not in any model's training corpus, the relevant pretraining baseline is closer to 1.0 than to 2.0. Our data on subjects with baselines in that range was uniformly positive: 9 of 9 subjects below baseline 2.0 showed improvement, with mean gain +1.04 points on the 1-5 scale.",
        "The 14 subjects in our study are biased *up* on pretraining representation. They are public-domain authors whose writing was preserved, digitized, and indexed. Even within this biased-high sample, the spec helps 12 of 14. The two it does not help are people the model already partially understood from public writing. For typical living users, whose private decisions are not in any model's training corpus, the relevant pretraining baseline is closer to 1.0 than to 2.0. Our data on subjects with baselines in that range was uniformly positive: 9 of 9 subjects below baseline 2.0 showed improvement, with mean gain +1.04 points on the 1-5 scale.",
    ),
    # L1074
    (
        "**This generalizes via a structural argument, not a quantitative one:** if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user. The Franklin ceiling — where the spec stops adding value — exists only when the source material is *also* in pretraining. For private data on living people, that condition does not obtain. We do not claim to have proven this empirically across the population. We claim that the structure of the gradient, combined with the test population's upward bias on representation, gives strong evidence that the specification is broadly useful across real AI users. Confirmation requires living-subject studies (§7).",
        "**This generalizes via a structural argument, not a quantitative one:** if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical living user. The Franklin ceiling, where the spec stops adding value, exists only when the source material is *also* in pretraining. For private data on living people, that condition does not obtain. We do not claim to have proven this empirically across the population. We claim that the structure of the gradient, combined with the test population's upward bias on representation, gives strong evidence that the specification is broadly useful across real AI users. Confirmation requires living-subject studies (§7).",
    ),
    # L1076
    (
        "This gap is well-documented in the literature. Jiang et al. (COLM 2025) found that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access — not because they lack facts, but because they lack the interpretive structure to apply those facts to novel situations.",
        "This gap is well-documented in the literature. Jiang et al. (COLM 2025) found that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The cause is not a lack of facts but a lack of the interpretive structure to apply those facts to novel situations.",
    ),
    # L1114
    (
        "The specification reduces hedging from 25% to under 3% when added alone, and to under 1% when added with retrieved facts. This is a **~10× and ~40× reduction** respectively. The Hamerton case study originally documented a 51% → 31% reduction; the cross-subject data shows the phenomenon is stronger and cleaner than the single-case story suggested — the spec shifts models from \"I don't have enough context to answer\" to committed predictions at an extremely high rate.",
        "The specification reduces hedging from 25% to under 3% when added alone, and to under 1% when added with retrieved facts. This is a **~10× and ~40× reduction** respectively. The Hamerton case study originally documented a 51% → 31% reduction; the cross-subject data shows the phenomenon is stronger and cleaner than the single-case story suggested. The spec shifts models from \"I don't have enough context to answer\" to committed predictions at an extremely high rate.",
    ),
    # L1116
    (
        "**An important caveat: hedging reduction is not the same as accuracy improvement.** The spec could be producing *warranted* commitment (the model now has enough structure to commit to correct predictions) or *unwarranted* commitment (the model is now willing to commit to predictions it should not be willing to commit to). Our prediction-score data (§4.1) shows that the spec improves accuracy for 12 of 14 subjects, so most of the reduced hedging is warranted — but we have not separately measured prediction accuracy *conditional on* hedged vs non-hedged responses. It is possible that the spec reduces hedging on some subjects more than it improves accuracy on them, which would be a calibration concern rather than a win. Future work should decompose the hedging-vs-accuracy relationship directly.",
        "**An important caveat: hedging reduction is not the same as accuracy improvement.** The spec could be producing *warranted* commitment (the model now has enough structure to commit to correct predictions) or *unwarranted* commitment (the model is now willing to commit to predictions it should not be willing to commit to). Our prediction-score data (§4.1) shows that the spec improves accuracy for 12 of 14 subjects, so most of the reduced hedging is warranted. However, we have not separately measured prediction accuracy *conditional on* hedged vs. non-hedged responses. It is possible that the spec reduces hedging on some subjects more than it improves accuracy on them, which would be a calibration concern rather than a win. Future work should decompose the hedging-vs-accuracy relationship directly.",
    ),
    # L1118
    (
        "A serving layer that routes queries — activating the specification for behavioral questions and skipping it for factual ones — would optimize both cost and accuracy. This routing is an open engineering problem.",
        "A serving layer that routes queries (activating the specification for behavioral questions and skipping it for factual ones) would optimize both cost and accuracy. This routing is an open engineering problem.",
    ),
    # L1126
    (
        "The Behavioral Specification severs this dependency. The spec is generated from the user's data and served as context — it is identical regardless of which model reads it. Claude, GPT, and Gemini all see the same representation of the user. This means the specification is not just a tool for unknown users but a tool for *consistent* representation across providers, including when migrating between models, building agentic systems that route between providers, or simply hedging against provider-specific blind spots in pretraining.",
        "The Behavioral Specification severs this dependency. The spec is generated from the user's data and served as context. It is identical regardless of which model reads it. Claude, GPT, and Gemini all see the same representation of the user. This means the specification is not just a tool for unknown users but a tool for *consistent* representation across providers, including when migrating between models, building agentic systems that route between providers, or simply hedging against provider-specific blind spots in pretraining.",
    ),
    # L1128
    (
        "For agent frameworks that route between models mid-task — using a cheap model for retrieval steps and a frontier model for reasoning steps, or fanning out to provider-specialized sub-agents — the spec travels with the request as a stable user-representation header. The cheap model and the reasoning model act on the same working model of the user, rather than each depending on their own pretraining distribution. This positions the specification not as a competing memory product but as a primitive that agent stacks consume: a portable representation layer that any framework can include in its system context regardless of which provider it routes a given step to.",
        "For agent frameworks that route between models mid-task (using a cheap model for retrieval steps and a frontier model for reasoning steps, or fanning out to provider-specialized sub-agents), the spec travels with the request as a stable user-representation header. The cheap model and the reasoning model act on the same working model of the user, rather than each depending on their own pretraining distribution. This positions the specification not as a competing memory product but as a primitive that agent stacks consume: a portable representation layer that any framework can include in its system context regardless of which provider it routes a given step to.",
    ),
    # L1130
    (
        "This portability also matters for the user. The spec is a portable artifact the user owns and can move between systems. Pretraining knowledge cannot be moved or audited. The spec can be — every claim traces back to source evidence, every change is versionable, the entire artifact is text.",
        "This portability also matters for the user. The spec is a portable artifact the user owns and can move between systems. Pretraining knowledge cannot be moved or audited. The spec can be: every claim traces back to source evidence, every change is versionable, and the entire artifact is text.",
    ),
    # L1134
    (
        "This study is, to our knowledge, the first head-to-head evaluation of the major memory-for-agents providers — Mem0, Letta, Supermemory, Zep — against a non-recall criterion. Recall benchmarks (LOCOMO, LongMemEval, LME-S) measure whether the system returns the right chunk; all four providers score 85%+ on those. We introduced a different axis — held-out behavioral prediction — because that is the property AI agents actually need when acting on someone's behalf. No prior benchmark tested these systems on that second question, and the systems were not built to be evaluated on it.",
        "This study is, to our knowledge, the first head-to-head evaluation of the major memory-for-agents providers (Mem0, Letta, Supermemory, Zep) against a non-recall criterion. Recall benchmarks (LOCOMO, LongMemEval, LME-S) measure whether the system returns the right chunk; all four providers score 85%+ on those. We introduced a different axis, held-out behavioral prediction, because that is the property AI agents actually need when acting on someone's behalf. No prior benchmark tested these systems on that second question, and the systems were not built to be evaluated on it.",
    ),
    # L1142
    (
        "- **Letta** is the most architecturally ambitious. Its native archival-retrieval path produces a null result when a spec is added (§4.3) — but this is a misconfiguration, not a capability limit: Letta's signature mechanism is the stateful-agent loop with self-editing memory blocks, not its archival store. When we actually invoked that loop (§4.3.1), Letta produced a 22,472-character self-edited representation whose prediction score at matched response model is in the same band as Base Layer's full-stack spec, at ~65% the context size. Letta is the only system in this study whose architecture can autonomously build an interpretive representation of the user from multi-turn interaction. For agent-first applications where the system maintains an evolving model of the user through conversation rather than from a prepared corpus, it is in a category of its own.",
        "- **Letta** is the most architecturally ambitious. Its native archival-retrieval path produces a null result when a spec is added (§4.3), but this is a misconfiguration, not a capability limit: Letta's signature mechanism is the stateful-agent loop with self-editing memory blocks, not its archival store. When we actually invoked that loop (§4.3.1), Letta produced a 22,472-character self-edited representation whose prediction score at matched response model is in the same band as Base Layer's full-stack spec, at ~65% the context size. Letta is the only system in this study whose architecture can autonomously build an interpretive representation of the user from multi-turn interaction. For agent-first applications where the system maintains an evolving model of the user through conversation rather than from a prepared corpus, it is in a category of its own.",
    ),
    # L1144
    (
        "- **Mem0** is the most predictable. +0.15 native, +0.38 controlled — both positive. Hybrid retrieval (semantic + keyword + entity), multi-level memory, timestamped and versioned. No surprises, no ceilings, layers cleanly under a spec. The safest default for teams that want a memory system with minimal integration risk.",
        "- **Mem0** is the most predictable. +0.15 native and +0.38 controlled, both positive. Hybrid retrieval (semantic + keyword + entity), multi-level memory, timestamped and versioned. No surprises, no ceilings, layers cleanly under a spec. The safest default for teams that want a memory system with minimal integration risk.",
    ),
    # L1146
    (
        "- **Supermemory** has the strongest standalone retrieval in the battery (C1 mean ~2.65 vs ~2.30 for others) but the smallest spec headroom — the ceiling effect we describe in §4.3, not a failure mode. Its five-layer architecture (connectors, extractors, Super-RAG, memory graphs, user profiles) captures more of the retrieval-side value natively, which leaves less for the spec to contribute. For applications where retrieval alone carries most of the value — support agents, team knowledge bases, integrated workspace assistants — Supermemory is likely the strongest fit of the four on its own terms.",
        "- **Supermemory** has the strongest standalone retrieval in the battery (C1 mean ~2.65 vs. ~2.30 for others) but the smallest spec headroom. This is the ceiling effect we describe in §4.3, not a failure mode. Its five-layer architecture (connectors, extractors, Super-RAG, memory graphs, user profiles) captures more of the retrieval-side value natively, which leaves less for the spec to contribute. For applications where retrieval alone carries most of the value (support agents, team knowledge bases, integrated workspace assistants), Supermemory is likely the strongest fit of the four on its own terms.",
    ),
    # L1150
    (
        "Base Layer is not a fifth memory provider, and we want to be explicit about that — including against our own data's temptation to slot it alongside the four. Base Layer is an Apache-2.0 behavioral-specification layer that layers on top of any retrieval substrate. The MiniLM + ChromaDB combination we included as a \"Base Layer C1/C3\" condition is the open-source retrieval floor that ships with the pipeline, not a competitive memory product. On the prediction axis, Base Layer's retrieval is in the same band as the commercial systems — within 0.05-0.40 points on most subjects — but rarely the highest performer. It is viable as a zero-cost local baseline for teams that cannot or do not want to depend on a commercial memory vendor. It is not positioned as a better memory provider than Mem0, Letta, Supermemory, or Zep, and the data in this study does not support that framing.",
        "Base Layer is not a fifth memory provider, and we want to be explicit about that, including against our own data's temptation to slot it alongside the four. Base Layer is an Apache-2.0 behavioral-specification layer that layers on top of any retrieval substrate. The MiniLM + ChromaDB combination we included as a \"Base Layer C1/C3\" condition is the open-source retrieval floor that ships with the pipeline, not a competitive memory product. On the prediction axis, Base Layer's retrieval is in the same band as the commercial systems (within 0.05-0.40 points on most subjects), but rarely the highest performer. It is viable as a zero-cost local baseline for teams that cannot or do not want to depend on a commercial memory vendor. It is not positioned as a better memory provider than Mem0, Letta, Supermemory, or Zep, and the data in this study does not support that framing.",
    ),
    # L1152
    (
        "What Base Layer contributes to the category is the content-compression layer itself — the pipeline that produces the behavioral specification from a person's text. That is orthogonal to retrieval architecture. Any of the four commercial systems could adopt Base Layer's compression as their representation layer without conflict with their retrieval substrate. Base Layer's role in this paper is that of the *referee*: we built the pipeline that generates the artifact, we ran the benchmark, we published the data, and we included our own retrieval floor in the comparison so that readers can see what open-source components alone produce on this axis.",
        "What Base Layer contributes to the category is the content-compression layer itself: the pipeline that produces the behavioral specification from a person's text. That is orthogonal to retrieval architecture. Any of the four commercial systems could adopt Base Layer's compression as their representation layer without conflict with their retrieval substrate. Base Layer's role in this paper is that of the *referee*: we built the pipeline that generates the artifact, we ran the benchmark, we published the data, and we included our own retrieval floor in the comparison so that readers can see what open-source components alone produce on this axis.",
    ),
    # L1156
    (
        "The benchmark does not resolve: performance on live multi-turn conversations, agent workflows with tool use, domains outside autobiographical text, or long-horizon stateful interactions. A system strong on held-out passage prediction may not be the strongest on live deployment, and vice versa. The system-level read above is conditioned on this specific test, not a universal leaderboard. A follow-up evaluating the same systems on live agent tasks — with tool use and genuine multi-turn dynamics — is the natural next step.",
        "The benchmark does not resolve: performance on live multi-turn conversations, agent workflows with tool use, domains outside autobiographical text, or long-horizon stateful interactions. A system strong on held-out passage prediction may not be the strongest on live deployment, and vice versa. The system-level read above is conditioned on this specific test, not a universal leaderboard. A follow-up evaluating the same systems on live agent tasks, with tool use and genuine multi-turn dynamics, is the natural next step.",
    ),
    # L1158
    (
        "The benchmark does resolve: all four commercial systems are capable of serving a behavioral specification as context, and three of the four (Mem0, Letta-controlled, Zep) produce statistically robust positive deltas when one is added. This is the first quantitative evidence that the behavioral-specification layer is additive with the existing memory-provider stack, not redundant. A team adopting a memory system today does not need to choose between \"vendor memory\" and \"behavioral spec\" — the two compose, and on this study's data the composition is better than either alone for most subjects.",
        "The benchmark does resolve: all four commercial systems are capable of serving a behavioral specification as context, and three of the four (Mem0, Letta-controlled, Zep) produce statistically robust positive deltas when one is added. This is the first quantitative evidence that the behavioral-specification layer is additive with the existing memory-provider stack, not redundant. A team adopting a memory system today does not need to choose between \"vendor memory\" and \"behavioral spec\"; the two compose, and on this study's data the composition is better than either alone for most subjects.",
    ),
    # L1164
    (
        "Letta's team — Charles Packer and Sarah Wooders at UC Berkeley, connected to Ion Stoica and Joseph Gonzalez's Sky Computing group — published the MemGPT paper (arXiv:2310.08560) that articulated the stateful-agent architecture: structured memory blocks that the agent itself edits during its inference loop, with explicit `core_memory_append`, `core_memory_replace`, and `memory_insert` tools. They raised ~$10M in seed funding (Felicis, GV) on that thesis. Their product is the best-resourced attempt in the memory-for-agents category at building an architecture where the system does not just store facts — it maintains an evolving representation of the user.",
        "Letta's team (Charles Packer and Sarah Wooders at UC Berkeley, connected to Ion Stoica and Joseph Gonzalez's Sky Computing group) published the MemGPT paper (arXiv:2310.08560) that articulated the stateful-agent architecture: structured memory blocks that the agent itself edits during its inference loop, with explicit `core_memory_append`, `core_memory_replace`, and `memory_insert` tools. They raised ~$10M in seed funding (Felicis, GV) on that thesis. Their product is the best-resourced attempt in the memory-for-agents category at building an architecture where the system does not just store facts; it maintains an evolving representation of the user.",
    ),
    # L1170
    (
        "I want to be direct about what Base Layer is and what it is not. Base Layer is a one-person project. I do not have a PhD. I am not funded. I do not run a lab. I wrote this pipeline and this paper in a year of working through the problem alone. Letta has a team, a funded runway, a research pedigree, and a published paper in a major venue. If I could see that behavioral specification is a missing primitive, a team like Letta's was already going to get there — and by the Hamerton result, they largely have, on the content side, through a completely different mechanism than the one I built.",
        "I want to be direct about what Base Layer is and what it is not. Base Layer is a one-person project. I do not have a PhD. I am not funded. I do not run a lab. I wrote this pipeline and this paper in a year of working through the problem alone. Letta has a team, a funded runway, a research pedigree, and a published paper in a major venue. If I could see that behavioral specification is a missing primitive, a team like Letta's was already going to get there, and by the Hamerton result, they largely have, on the content side, through a completely different mechanism than the one I built.",
    ),
    # L1172
    (
        "What Base Layer contributes that is still distinct is the *content compression layer* itself, and I think this is actually the place where the ecosystem could move fastest. Letta's architectural advantage is stateful self-editing during conversation. Base Layer's contribution is the pipeline that takes a person's raw text and compresses it into an axiomatized representation with activation conditions, directives, and false-positive warnings — a structure that can be produced in minutes from existing corpora rather than accumulated over hundreds of agent turns. These are complementary, not competing. An agent-memory system could adopt Base Layer's compression as its block-authoring step and gain a starting representation that is structurally operational, not just reflective. A retrieval-based system (Mem0, Supermemory, Zep) could adopt Base Layer's compression as its representation layer and move from indexing facts to carrying a working model of the user.",
        "What Base Layer contributes that is still distinct is the *content compression layer* itself, and I think this is actually the place where the ecosystem could move fastest. Letta's architectural advantage is stateful self-editing during conversation. Base Layer's contribution is the pipeline that takes a person's raw text and compresses it into an axiomatized representation with activation conditions, directives, and false-positive warnings: a structure that can be produced in minutes from existing corpora rather than accumulated over hundreds of agent turns. These are complementary, not competing. An agent-memory system could adopt Base Layer's compression as its block-authoring step and gain a starting representation that is structurally operational, not just reflective. A retrieval-based system (Mem0, Supermemory, Zep) could adopt Base Layer's compression as its representation layer and move from indexing facts to carrying a working model of the user.",
    ),
    # L1174
    (
        "Base Layer is Apache 2.0. The extraction schema, the authoring prompts, the compose step, the 47 predicates, and the three-layer architecture are all public. If any of the memory-for-agents companies — including Letta — wants to use them, they can. I would rather see behavioral specification become a shared primitive across the category than have it sit in a single product. The thing that matters is whether AI systems start serving users from a representation of how they actually reason, rather than from a bag of retrieved facts.",
        "Base Layer is Apache 2.0. The extraction schema, the authoring prompts, the compose step, the 47 predicates, and the three-layer architecture are all public. If any of the memory-for-agents companies, including Letta, want to use them, they can. I would rather see behavioral specification become a shared primitive across the category than have it sit in a single product. The thing that matters is whether AI systems start serving users from a representation of how they actually reason, rather than from a bag of retrieved facts.",
    ),
    # L1176
    (
        "I am glad Letta is doing this work. The fact that two very differently-resourced efforts converged on the same representational target in the same window — theirs published at a major venue with a Berkeley systems-research lineage, mine written by one person without that infrastructure — is evidence that the primitive is ready to be seen. The direction is right. The rest is implementation and adoption.",
        "I am glad Letta is doing this work. The fact that two very differently-resourced efforts converged on the same representational target in the same window, theirs published at a major venue with a Berkeley systems-research lineage and mine written by one person without that infrastructure, is evidence that the primitive is ready to be seen. The direction is right. The rest is implementation and adoption.",
    ),
    # L1180
    (
        "Honestly acknowledging a limitation: the generation pipeline uses Haiku (extract), Sonnet (author), and Opus (compose) — all Anthropic models. The primary response model is also Haiku. An adversarial reviewer could reasonably ask: how much of the effect is Anthropic models talking to themselves?",
        "Honestly acknowledging a limitation: the generation pipeline uses Haiku (extract), Sonnet (author), and Opus (compose), all of which are Anthropic models. The primary response model is also Haiku. An adversarial reviewer could reasonably ask: how much of the effect is Anthropic models talking to themselves?",
    ),
    # L1182
    (
        "The multi-model response validation (§3.6) and the Tier 2 circularity replication (§4.8) partially address this. Judges include GPT-4o, GPT-5.4, Gemini Flash, and Gemini Pro — four non-Anthropic models agreeing with Anthropic judges on condition rankings (Spearman 0.89-0.98). Tier 2 replicates the effect with non-Haiku response models on independent batteries.",
        "The multi-model response validation (§3.6) and the Tier 2 circularity replication (§4.8) partially address this. Judges include GPT-4o, GPT-5.4, Gemini Flash, and Gemini Pro: four non-Anthropic models that agree with Anthropic judges on condition rankings (Spearman 0.89-0.98). Tier 2 replicates the effect with non-Haiku response models on independent batteries.",
    ),
    # L1184
    (
        "The cleaner solution — a cross-family extraction and authoring pipeline — is planned for future work. We are building a provider-agnostic pipeline that accepts any extraction/authoring model as a parameter, enabling users and reviewers to regenerate specs using any model combination they trust.",
        "The cleaner solution, a cross-family extraction and authoring pipeline, is planned for future work. We are building a provider-agnostic pipeline that accepts any extraction/authoring model as a parameter, enabling users and reviewers to regenerate specs using any model combination they trust.",
    ),
    # L1188
    (
        "This paper does not claim the Behavioral Specification solves AI personalization. It claims that the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued — four funded systems score 85%+ on LOCOMO/LongMemEval. None test whether the system actually understands the person it serves.",
        "This paper does not claim the Behavioral Specification solves AI personalization. It claims that the current framing of the problem, with recall as the primary metric, is insufficient. Performance on established recall benchmarks has plateaued: four funded systems score 85%+ on LOCOMO/LongMemEval. None test whether the system actually understands the person it serves.",
    ),
    # L1190
    (
        "The specification is one implementation of a broader primitive. The 47 predicates may not be the right 47. The three-layer architecture may not be the optimal structure. The current implementation is static — it does not update as a person changes, does not track which patterns are strengthening or decaying, does not resolve contradictions between earlier and later behavior. This paper tests the primitive itself. Adapting it is the engineering work that follows.",
        "The specification is one implementation of a broader primitive. The 47 predicates may not be the right 47. The three-layer architecture may not be the optimal structure. The current implementation is static. It does not update as a person changes, does not track which patterns are strengthening or decaying, and does not resolve contradictions between earlier and later behavior. This paper tests the primitive itself. Adapting it is the engineering work that follows.",
    ),
    # L1197
    (
        "- **Letta stateful-agent prediction test across all 14 subjects.** §4.3.1 reports a single-subject (Hamerton) head-to-head: Haiku + Letta self-edited memory block = 3.24 vs. Haiku + Base Layer full-stack spec = 3.04, with Letta's block at ~65% the context size. Whether this result generalizes across subjects — particularly whether Letta's less-structured representation holds up on subjects with sparser or more heterogeneous source material — is the single most important follow-up for memory-system comparison. Cost estimate: ~30 agent turns per subject × 14 subjects × API pricing ≈ tractable, but not completed in time for this paper.",
        "- **Letta stateful-agent prediction test across all 14 subjects.** §4.3.1 reports a single-subject (Hamerton) head-to-head: Haiku + Letta self-edited memory block = 3.24 vs. Haiku + Base Layer full-stack spec = 3.04, with Letta's block at ~65% the context size. Whether this result generalizes across subjects (particularly whether Letta's less-structured representation holds up on subjects with sparser or more heterogeneous source material) is the single most important follow-up for memory-system comparison. Cost estimate: ~30 agent turns per subject × 14 subjects × API pricing ≈ tractable, but not completed in time for this paper.",
    ),
    # L1200
    (
        "- **Moat.** What prevents a frontier lab from training native behavioral extraction? Possibly nothing, if the goal is the capability alone. But the specification's lasting contribution is traceability — a model that predicts your behavior from pretraining cannot explain why. The specification can. Traceability is not a feature. It is what separates personalization from surveillance.",
        "- **Moat.** What prevents a frontier lab from training native behavioral extraction? Possibly nothing, if the goal is the capability alone. But the specification's lasting contribution is traceability. A model that predicts your behavior from pretraining cannot explain why. The specification can. Traceability is not a feature. It is what separates personalization from surveillance.",
    ),
    # L1212
    (
        "We release everything under Apache 2.0 so the pipeline cannot be proprietary-captured at the code level. A license, however, is not a mechanism: it enables any entity to run the pipeline and choose whether to return the output to the subject it describes. Traceability at the spec level enables inspection; whether a deploying system honors that inspectability is a separate question — one answered by protocol design, regulatory backing, and user-side infrastructure we do not yet control. Naming the gap matters: user ownership is an architectural goal the open-source release makes possible but does not enforce. The specification's value is maximized when the person it describes holds it and a system exists to let them hold it meaningfully.",
        "We release everything under Apache 2.0 so the pipeline cannot be proprietary-captured at the code level. A license, however, is not a mechanism: it enables any entity to run the pipeline and choose whether to return the output to the subject it describes. Traceability at the spec level enables inspection; whether a deploying system honors that inspectability is a separate question, answered by protocol design, regulatory backing, and user-side infrastructure we do not yet control. Naming the gap matters: user ownership is an architectural goal the open-source release makes possible but does not enforce. The specification's value is maximized when the person it describes holds it and a system exists to let them hold it meaningfully.",
    ),
]

# ==================== §6-§8 + Appendices ====================

REWRITES += [
    # L1222
    (
        "2. **Analysis plan locked partially retroactively.** This study was not preregistered end-to-end. We locked the analysis plan for pending runs (Tier 2 circularity, wrong-spec v2, Supermemory Option B retry) before those runs completed — commit de27b64 on 2026-04-16 — but most data landed before the plan was written. For the next study (living subjects, cross-family pipeline), preregistration will be complete.",
        "2. **Analysis plan locked partially retroactively.** This study was not preregistered end-to-end. We locked the analysis plan for pending runs (Tier 2 circularity, wrong-spec v2, Supermemory Option B retry) before those runs completed, in commit de27b64 on 2026-04-16, but most data landed before the plan was written. For the next study (living subjects, cross-family pipeline), preregistration will be complete.",
    ),
    # L1224
    (
        "3. **Pipeline is Anthropic-family end-to-end.** Extract (Haiku), author (Sonnet), compose (Opus) — all from a single provider. Multi-model response validation and Tier 2 circularity partially address the concern. A provider-agnostic pipeline is planned as follow-up work.",
        "3. **Pipeline is Anthropic-family end-to-end.** Extract (Haiku), author (Sonnet), and compose (Opus) all run through a single provider. Multi-model response validation and Tier 2 circularity partially address the concern. A provider-agnostic pipeline is planned as follow-up work.",
    ),
    # L1226
    (
        "4. **No live human subjects.** All study subjects are historical figures with published autobiographies. Private data on living individuals is a different problem — the source is noisier, the ground truth is self-reported, and the evaluation is trickier. Planned.",
        "4. **No live human subjects.** All study subjects are historical figures with published autobiographies. Private data on living individuals is a different problem: the source is noisier, the ground truth is self-reported, and the evaluation is trickier. Planned.",
    ),
    # L1240
    (
        "11. **Adversarial robustness untested.** A user could attempt to manipulate their source data to produce a spec that misrepresents them. The pipeline's design provides partial resistance — it extracts patterns across the full corpus, using recurrence and cross-domain validation, so isolated planted statements are low-confidence or contradicted by the broader pattern. Meaningful manipulation would require consistently fabricating an alternate profile across sufficient source data that the pipeline treats it as durable. This is a working assumption, not a tested guarantee.",
        "11. **Adversarial robustness untested.** A user could attempt to manipulate their source data to produce a spec that misrepresents them. The pipeline's design provides partial resistance: it extracts patterns across the full corpus, using recurrence and cross-domain validation, so isolated planted statements are low-confidence or contradicted by the broader pattern. Meaningful manipulation would require consistently fabricating an alternate profile across sufficient source data that the pipeline treats it as durable. This is a working assumption, not a tested guarantee.",
    ),
    # L1242
    (
        "12. **Pretraining representation is operationalized via baseline score (C5), not measured independently.** Throughout this paper we use the C5 baseline (model's prediction accuracy with no external context) as a proxy for pretraining representation. This is methodologically convenient but theoretically circular: we are using the same response-model + judge pipeline to define the axis as we use to measure improvement on that axis. A reviewer could correctly observe that the gradient (spec helps more when C5 is low) is partly a mean-reversion property of the metric. We mitigate this in two ways: (a) the gradient is robust across the 7 independent judges (judges agree on rankings, Spearman 0.89-0.98), so it is not a property of one judge's scoring; (b) the §4.8.1 cross-provider data shows the same subject's \"baseline\" varies by 1-2 points across response models, demonstrating that what the metric captures includes provider-specific pretraining knowledge — the variance is meaningful, not pure noise. Still, an independent pretraining proxy (n-gram frequency in known training corpora, Wikipedia article centrality, probe-based memorization tests) would substantially strengthen the gradient claim. Planned for follow-up work.",
        "12. **Pretraining representation is operationalized via baseline score (C5), not measured independently.** Throughout this paper we use the C5 baseline (model's prediction accuracy with no external context) as a proxy for pretraining representation. This is methodologically convenient but theoretically circular: we are using the same response-model + judge pipeline to define the axis as we use to measure improvement on that axis. A reviewer could correctly observe that the gradient (spec helps more when C5 is low) is partly a mean-reversion property of the metric. We mitigate this in two ways: (a) the gradient is robust across the 7 independent judges (judges agree on rankings, Spearman 0.89-0.98), so it is not a property of one judge's scoring; (b) the §4.8.1 cross-provider data shows the same subject's \"baseline\" varies by 1-2 points across response models, demonstrating that what the metric captures includes provider-specific pretraining knowledge. The variance is meaningful, not pure noise. Still, an independent pretraining proxy (n-gram frequency in known training corpora, Wikipedia article centrality, probe-based memorization tests) would substantially strengthen the gradient claim. Planned for follow-up work.",
    ),
    # L1246
    (
        "14. **Inference-time cost not tested in production conditions.** We report token counts (~5-8K per spec) and note that prompt caching reduces per-request marginal cost to 10-20% of the nominal. We do not test full production deployments with caching enabled, multi-turn conversations, or routing layers — these are engineering optimizations independent of the representational content tested.",
        "14. **Inference-time cost not tested in production conditions.** We report token counts (~5-8K per spec) and note that prompt caching reduces per-request marginal cost to 10-20% of the nominal. We do not test full production deployments with caching enabled, multi-turn conversations, or routing layers. These are engineering optimizations independent of the representational content tested.",
    ),
    # L1253
    (
        "- **Layer ablation.** Anchors / core / predictions / unified brief — which drives the most gain? Informs cost-benefit of spec length vs. accuracy improvement.",
        "- **Layer ablation.** Anchors / core / predictions / unified brief: which drives the most gain? Informs cost-benefit of spec length vs. accuracy improvement.",
    ),
    # L1266
    (
        "**Representational accuracy matters.** It is a real property, measurable via behavioral prediction on held-out situations, and it varies substantially across the subjects and approaches we tested. The question is to what extent — for whom, under what conditions, at what cost. This paper does not answer that question. It argues the question is worth asking and shows one working way to approach it.",
        "**Representational accuracy matters.** It is a real property, measurable via behavioral prediction on held-out situations, and it varies substantially across the subjects and approaches we tested. The question is to what extent: for whom, under what conditions, and at what cost. This paper does not answer that question. It argues the question is worth asking and shows one working way to approach it.",
    ),
    # L1270
    (
        "We evaluated one approach: the Behavioral Specification. Automated, traceable, portable across providers, user-ownable. It improves behavioral prediction for 12 of 14 historical subjects (Wilcoxon p=0.006), with uniform improvement (9/9) for the low-baseline subjects closest to real AI users. It shifts models from hedged refusal (25% of baseline responses) to committed prediction (<1% with spec + facts). A wrong spec is indistinguishable from no spec, ruling out a generic-framework reading. The specification is one working method for building this interpretive layer — one, not the only one. Better implementations, different architectures, composite approaches — these are the research direction we hope this paper opens.",
        "We evaluated one approach: the Behavioral Specification. Automated, traceable, portable across providers, user-ownable. It improves behavioral prediction for 12 of 14 historical subjects (Wilcoxon p=0.006), with uniform improvement (9/9) for the low-baseline subjects closest to real AI users. It shifts models from hedged refusal (25% of baseline responses) to committed prediction (<1% with spec + facts). A wrong spec is indistinguishable from no spec, ruling out a generic-framework reading. The specification is one working method for building this interpretive layer, one among many possible. Better implementations, different architectures, and composite approaches are the research direction we hope this paper opens.",
    ),
    # L1272
    (
        "We are explicit about what we have not done. We tested only historical figures whose autobiographies are in the training corpus of every major model. The population this work ultimately wants to serve — living people, whose private reasoning has never been indexed — is where the broader claim needs confirmation. The structural argument we offer (gradient holds within biased-up sample → should carry to lower-baseline populations) is strong evidence but not direct evidence. That gap is the most important piece of follow-up work.",
        "We are explicit about what we have not done. We tested only historical figures whose autobiographies are in the training corpus of every major model. The population this work ultimately wants to serve is living people, whose private reasoning has never been indexed, and that is where the broader claim needs confirmation. The structural argument we offer (gradient holds within biased-up sample → should carry to lower-baseline populations) is strong evidence but not direct evidence. That gap is the most important piece of follow-up work.",
    ),
    # L1274
    (
        "This study is not a conclusion. It is a beginning. The question it opens — *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, and audit that representation?* — is a long-term research direction, not a feature request. We invite other implementations, other evaluations, adversarial testing, human-subject validation, ablations, cross-provider replications. The problem is large. This is one opening move.",
        "This study is not a conclusion. It is a beginning. The question it opens is a long-term research direction, not a feature request: *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, and audit that representation?* We invite other implementations, other evaluations, adversarial testing, human-subject validation, ablations, and cross-provider replications. The problem is large. This is one opening move.",
    ),
    # L1276
    (
        "Memory systems store what was said. Preference models store what was liked. Personas store how someone presents. Each is necessary. None is sufficient. Representing how a specific person actually reasons — accurately, portably, traceably, auditably — is where personalized AI lives or fails. That representation is the load-bearing layer for any agent acting on someone's behalf, and for behavioral alignment between an AI and the individual it serves. The next generation of personalization work needs to address it, and human–AI interaction research more broadly will have to reckon with how such representations are built, audited, and — critically — owned by the people they describe.",
        "Memory systems store what was said. Preference models store what was liked. Personas store how someone presents. Each is necessary. None is sufficient. Representing how a specific person actually reasons, accurately, portably, traceably, and auditably, is where personalized AI lives or fails. That representation is the load-bearing layer for any agent acting on someone's behalf, and for behavioral alignment between an AI and the individual it serves. The next generation of personalization work needs to address it, and human–AI interaction research more broadly will have to reckon with how such representations are built, audited, and (critically) owned by the people they describe.",
    ),
    # L1286
    (
        "**C. Provenance index.** *[PROVENANCE_INDEX.md — every number in paper traced to source file.]*",
        "**C. Provenance index.** *[PROVENANCE_INDEX.md: every number in paper traced to source file.]*",
    ),
    # L1288
    (
        "**D. Reference table.** *[REFERENCE_TABLE.md — all citations with verification status.]*",
        "**D. Reference table.** *[REFERENCE_TABLE.md: all citations with verification status.]*",
    ),
]

# ==================== §3 Study Design ====================

REWRITES += [
    # L392
    (
        "This distinction matters because it resists a common reframing: \"the spec is a better prompt.\" A better prompt that produces accurate predictions without representing the person would still be a better prompt. What we measure is whether the model's *representation* of the person — its internal working model — has been upgraded such that predictions follow naturally from it.",
        "This distinction matters because it resists a common reframing: \"the spec is a better prompt.\" A better prompt that produces accurate predictions without representing the person would still be a better prompt. What we measure is whether the model's *representation* of the person, its internal working model, has been upgraded such that predictions follow naturally from it.",
    ),
    # L398
    (
        "We test 14 subjects, all historical figures with public domain autobiographies or memoirs. Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting entirely on a single type of source material. We use the baseline score (§3.7, §4.1) as an observable proxy for each subject's pretraining representation — a ~1.0 baseline indicates near-zero pretraining knowledge; a ~3.0+ baseline indicates substantial pretraining knowledge. **We do not make claims about the causes of this variation in LLM training data.** The purpose of sampling broadly is methodological: to test whether the specification's effect is subject-specific or generalizes across varied source material.",
        "We test 14 subjects, all historical figures with public domain autobiographies or memoirs. Subjects were selected across a range of time periods, source-text lengths, and geographic origins to avoid the study sitting entirely on a single type of source material. We use the baseline score (§3.7, §4.1) as an observable proxy for each subject's pretraining representation. A ~1.0 baseline indicates near-zero pretraining knowledge, and a ~3.0+ baseline indicates substantial pretraining knowledge. **We do not make claims about the causes of this variation in LLM training data.** The purpose of sampling broadly is methodological: to test whether the specification's effect is subject-specific or generalizes across varied source material.",
    ),
    # L417
    (
        "Benjamin Franklin (Project Gutenberg #20203) serves as a known-figure control — a subject with extensive pretraining representation.",
        "Benjamin Franklin (Project Gutenberg #20203) serves as a known-figure control, a subject with extensive pretraining representation.",
    ),
    # L437
    (
        "**Total pipeline cost:** Under $1 per subject. Generating a spec for a new subject is under $1. Reproducing the full study across 14 subjects, 5 systems, 6 response models, 7 judges and ~40 questions per subject cost approximately $500-700 in LLM API charges plus ~$80 in commercial memory system subscriptions — figures for readers planning to replicate the full battery; generating specs for a single use case is cheap.",
        "**Total pipeline cost:** Under $1 per subject. Generating a spec for a new subject is under $1. Reproducing the full study across 14 subjects, 5 systems, 6 response models, 7 judges and ~40 questions per subject cost approximately $500-700 in LLM API charges plus ~$80 in commercial memory system subscriptions. These figures are for readers planning to replicate the full battery; generating specs for a single use case is cheap.",
    ),
    # L460
    (
        "**Inference-time cost.** The full specification is approximately 5,000-8,000 tokens depending on subject. Naively, every prompt that includes the spec pays this token cost. In practice, modern provider APIs cache persistent system context (Anthropic prompt caching, OpenAI cached responses, Google cached content) — so after the first call in a session, the per-request marginal cost is approximately 10-20% of the nominal token count, depending on cache hit rate. A serving layer optimized around the spec (loading once per session, caching across calls, routing factual queries away from the spec context) can reduce this further. We do not test these optimizations in this paper; they are engineering choices independent of the specification's representational content. For applications where spec context size is a concern, ablation of which layers carry the most weight (Future Work, §7) would inform a smaller spec.",
        "**Inference-time cost.** The full specification is approximately 5,000-8,000 tokens depending on subject. Naively, every prompt that includes the spec pays this token cost. In practice, modern provider APIs cache persistent system context (Anthropic prompt caching, OpenAI cached responses, Google cached content), so after the first call in a session, the per-request marginal cost is approximately 10-20% of the nominal token count, depending on cache hit rate. A serving layer optimized around the spec (loading once per session, caching across calls, routing factual queries away from the spec context) can reduce this further. We do not test these optimizations in this paper; they are engineering choices independent of the specification's representational content. For applications where spec context size is a concern, ablation of which layers carry the most weight (Future Work, §7) would inform a smaller spec.",
    ),
    # L469
    (
        "2. It writes questions that reference only patterns observable in the training text — no names, dates, or details unique to the held-out content",
        "2. It writes questions that reference only patterns observable in the training text, with no names, dates, or details unique to the held-out content",
    ),
    # L484
    (
        "Only the 39 behavioral prediction questions per subject are scored in the main results. They are the questions where recall vs. reasoning divergence is most visible — where a system with the right facts but no interpretive structure should fail, and where the spec should help most.",
        "Only the 39 behavioral prediction questions per subject are scored in the main results. They are the questions where recall vs. reasoning divergence is most visible: a system with the right facts but no interpretive structure should fail, and the spec should help most.",
    ),
    # L492
    (
        "**Control 1: Independent battery generation.** For all 13 global subjects, we independently regenerated batteries using GPT-5.4 (OpenAI) with the identical backward-design prompt. The generated batteries produced the same question count (39 BP per subject), covered the same 10 behavioral categories (with 8-10 shared categories per subject), and targeted the same behavioral patterns in the source text. Emphasis differed — GPT-5.4 produced more risk and change-over-time questions; Haiku produced more values and decisions questions — but the backward-design methodology constrains the output more than the model does. Full GPT-5.4 batteries are released for independent replication.",
        "**Control 1: Independent battery generation.** For all 13 global subjects, we independently regenerated batteries using GPT-5.4 (OpenAI) with the identical backward-design prompt. The generated batteries produced the same question count (39 BP per subject), covered the same 10 behavioral categories (with 8-10 shared categories per subject), and targeted the same behavioral patterns in the source text. Emphasis differed, with GPT-5.4 producing more risk and change-over-time questions and Haiku producing more values and decisions questions, but the backward-design methodology constrains the output more than the model does. Full GPT-5.4 batteries are released for independent replication.",
    ),
    # L494
    (
        "**Control 2: Replication with non-Haiku chain.** For 3 subjects spanning the effect gradient — Ebers (baseline 1.04, strong positive effect), Yung Wing (baseline 1.88, modest positive effect), Zitkala-Sa (baseline 2.34, negative effect) — we re-ran the core C5/C2a/C4a/C2c conditions using:",
        "**Control 2: Replication with non-Haiku chain.** For 3 subjects spanning the effect gradient (Ebers at baseline 1.04 with a strong positive effect; Yung Wing at baseline 1.88 with a modest positive effect; Zitkala-Sa at baseline 2.34 with a negative effect), we re-ran the core C5/C2a/C4a/C2c conditions using:",
    ),
    # L512 (table row)
    (
        "| C5 | Baseline | Nothing | Floor — what the model knows from pretraining alone |",
        "| C5 | Baseline | Nothing | Floor: what the model knows from pretraining alone |",
    ),
    # L535
    (
        "- **v2:** Random derangement — each subject is assigned a wrong spec from a different study subject (fixed seed 42, no subject gets its own spec). This tightens the control: Franklin is a known figure whose spec may be implicitly closer to canonical Western profiles than a random study subject's spec would be.",
        "- **v2:** Random derangement. Each subject is assigned a wrong spec from a different study subject (fixed seed 42, no subject gets its own spec). This tightens the control: Franklin is a known figure whose spec may be implicitly closer to canonical Western profiles than a random study subject's spec would be.",
    ),
    # L572
    (
        "**Coverage note.** All 7 judges ran against Hamerton's complete condition set and against the Tier 2 circularity replication. For the 13 global subjects' main gradient conditions, Gemini 2.5 Pro was not run due to its RPD limits; those conditions were judged by 6 judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash). The non-Gemini 5-judge subpanel (used for sensitivity analysis in §4.1.2) has complete coverage on all conditions. Aggregation treats missing judge×cell entries per the locked rule — mean across available judges; a cell is not counted if fewer than 3 judges have valid scores. GPT-5.4 additionally has a ~19% parse-failure rate on the 1-5 judging task (returns text beyond the single digit); parse failures are excluded per the aggregation rule and do not affect cell means when ≥3 judges score successfully.",
        "**Coverage note.** All 7 judges ran against Hamerton's complete condition set and against the Tier 2 circularity replication. For the 13 global subjects' main gradient conditions, Gemini 2.5 Pro was not run due to its RPD limits; those conditions were judged by 6 judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash). The non-Gemini 5-judge subpanel (used for sensitivity analysis in §4.1.2) has complete coverage on all conditions. Aggregation treats missing judge×cell entries per the locked rule: mean across available judges, with a cell not counted if fewer than 3 judges have valid scores. GPT-5.4 additionally has a ~19% parse-failure rate on the 1-5 judging task (returns text beyond the single digit); parse failures are excluded per the aggregation rule and do not affect cell means when ≥3 judges score successfully.",
    ),
    # L599
    (
        "Four of five judges correctly score verbatim matches at 5.0 (Gemini Pro the outlier). Judges vary in length sensitivity: Haiku shows length bias (padding does not reduce scores); Gemini Pro penalizes padding severely. GPT-5.4 has the best overall calibration profile. Calibration is **diagnostic**, not corrective — raw scores are used in analysis. Calibration data is published so readers can apply their own normalization.",
        "Four of five judges correctly score verbatim matches at 5.0 (Gemini Pro the outlier). Judges vary in length sensitivity: Haiku shows length bias (padding does not reduce scores); Gemini Pro penalizes padding severely. GPT-5.4 has the best overall calibration profile. Calibration is **diagnostic**, not corrective; raw scores are used in analysis. Calibration data is published so readers can apply their own normalization.",
    ),
    # L605
    (
        "Judges agree strongly on condition rankings (pairwise Spearman ρ = 0.89-0.98). Absolute per-question agreement is moderate-to-substantial on the 5 non-Gemini judges (α = 0.659, approaching the 0.667 threshold commonly cited for acceptable ordinal agreement) and drops to 0.535 when the two Gemini judges are included, because their systematic +1-point inflation shifts absolute scores even while rank order is preserved. The cross-provider rank convergence — three separate providers' models agreeing on which conditions score higher than which — validates that the specification effect is not an artifact of any single judging model's scoring preferences.",
        "Judges agree strongly on condition rankings (pairwise Spearman ρ = 0.89-0.98). Absolute per-question agreement is moderate-to-substantial on the 5 non-Gemini judges (α = 0.659, approaching the 0.667 threshold commonly cited for acceptable ordinal agreement) and drops to 0.535 when the two Gemini judges are included, because their systematic +1-point inflation shifts absolute scores even while rank order is preserved. The cross-provider rank convergence, in which three separate providers' models agree on which conditions score higher than which, validates that the specification effect is not an artifact of any single judging model's scoring preferences.",
    ),
]

# ==================== §2 Related Work ====================

REWRITES += [
    # L344
    (
        "The MemGPT paper describes memory edits as \"entirely self-directed\" — the LLM chooses when to write, what to write, and what to overwrite as it processes conversation turns.",
        "The MemGPT paper describes memory edits as \"entirely self-directed\": the LLM chooses when to write, what to write, and what to overwrite as it processes conversation turns.",
    ),
    # L350
    (
        "None of them take representational accuracy — the property of interest to this paper — as an explicit design target.",
        "None of them take representational accuracy, which is the property of interest to this paper, as an explicit design target.",
    ),
    # L354
    (
        "This enables a person to ask not just \"where did this come from?\" but \"why does the specification believe this about me?\" — and receive the exact text that supports the interpretive claim.",
        "This enables a person to ask not just \"where did this come from?\" but \"why does the specification believe this about me?\", and to receive the exact text that supports the interpretive claim.",
    ),
    # L359
    (
        "- **PersonaGym** (Jandaghi et al., EMNLP 2025): Tests persona fidelity — whether a model maintains a described persona during conversation. Evaluates consistency of persona presentation, not prediction of held-out behavior.",
        "- **PersonaGym** (Jandaghi et al., EMNLP 2025): Tests persona fidelity, which is whether a model maintains a described persona during conversation. Evaluates consistency of persona presentation, not prediction of held-out behavior.",
    ),
    # L360
    (
        "- **AlpsBench** (Xiao et al., 2026): Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses. Their central finding — that explicit memory mechanisms improve recall but do not inherently guarantee more preference-aligned or emotionally resonant responses — is independently arrived at and complementary to ours: they find the gap in preference alignment, we find it in behavioral prediction.",
        "- **AlpsBench** (Xiao et al., 2026): Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses. Their central finding, that explicit memory mechanisms improve recall but do not inherently guarantee more preference-aligned or emotionally resonant responses, is independently arrived at and complementary to ours: they find the gap in preference alignment, we find it in behavioral prediction.",
    ),
    # L366
    (
        "**Bartlett (1932)** demonstrated that humans remember schemas, not facts — reconstructing memory through structured frameworks rather than replaying stored data. The Behavioral Specification is computationally analogous to a schema: a compressed structure that enables reasoning about a person without storing every fact about them.",
        "**Bartlett (1932)** demonstrated that humans remember schemas, not facts, reconstructing memory through structured frameworks rather than replaying stored data. The Behavioral Specification is computationally analogous to a schema: a compressed structure that enables reasoning about a person without storing every fact about them.",
    ),
    # L368
    (
        "**Hinton et al. (2015)** showed that compressing a large model into a smaller one preserves \"dark knowledge\" — the relationships between outputs that carry more information than the outputs themselves. Our pipeline performs an analogous operation on personal data: compressing 25,000+ words of source text into a 3,000-5,000 token specification that preserves behavioral signal while discarding biographical noise.",
        "**Hinton et al. (2015)** showed that compressing a large model into a smaller one preserves \"dark knowledge\", the relationships between outputs that carry more information than the outputs themselves. Our pipeline performs an analogous operation on personal data: compressing 25,000+ words of source text into a 3,000-5,000 token specification that preserves behavioral signal while discarding biographical noise.",
    ),
    # L370
    (
        "**Chen, Arditi, Evans et al. (2025)** extract persona representations as steerable vectors inside model activations, enabling direct monitoring and control of character traits through internal activation surgery. Our approach is architecturally complementary: where Chen et al. modify the model to reflect a persona, we inform the model from outside. Both validate that persona is a real, manipulable structure — one through weights, one through context.",
        "**Chen, Arditi, Evans et al. (2025)** extract persona representations as steerable vectors inside model activations, enabling direct monitoring and control of character traits through internal activation surgery. Our approach is architecturally complementary: where Chen et al. modify the model to reflect a persona, we inform the model from outside. Both validate that persona is a real, manipulable structure: one through weights, the other through context.",
    ),
    # L372
    (
        "**Jiang et al. (COLM 2025)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access — not because they lack facts, but because they lack the interpretive structure to apply those facts to novel situations. This is direct evidence for the representational-accuracy gap we study.",
        "**Jiang et al. (COLM 2025)** find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks even with full conversation access. The cause is not a lack of facts but a lack of the interpretive structure to apply those facts to novel situations. This is direct evidence for the representational-accuracy gap we study.",
    ),
    # L376
    (
        "**Lu et al. (2026)** identify hedging as a structural property of assistant models — without an external behavioral anchor, helpfulness drifts toward hedging as a safe default. The specification provides that anchor.",
        "**Lu et al. (2026)** identify hedging as a structural property of assistant models. Without an external behavioral anchor, helpfulness drifts toward hedging as a safe default. The specification provides that anchor.",
    ),
]

# ==================== Abstract ====================

REWRITES += [
    # L215
    (
        "Current AI memory benchmarks measure recall — whether a system can retrieve what a user said when asked. They do not measure **representational accuracy** — whether the system's working model of the user enables it to anticipate responses in situations the system has never seen. This paper argues representational accuracy is the property AI agents actually require when acting on someone's behalf, and that it is under-measured, under-discussed, and improvable.",
        "Current AI memory benchmarks measure recall: whether a system can retrieve what a user said when asked. They do not measure **representational accuracy**, which is whether the system's working model of the user enables it to anticipate responses in situations the system has never seen. This paper argues representational accuracy is the property AI agents actually require when acting on someone's behalf, and that it is under-measured, under-discussed, and improvable.",
    ),
    # L217
    (
        "Four state-of-the-art commercial memory systems (Mem0, Letta, Supermemory, Zep) score 85%+ on recall benchmarks. On held-out behavioral prediction tasks — a direct test of representational accuracy — their performance is uneven and, for several subjects in our study, indistinguishable from a no-memory baseline. Across 14 subjects and 515 behavioral prediction questions (controlled config, all systems given identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) fail to share any common fact in all three systems' top-1 on 93% of questions (83% at top-3, 74% at top-5, 53% at top-10); in the native config where each system runs its own ingestion, disagreement is 100% at every top-k. These systems solved retrieval. Retrieval is not representation.",
        "Four state-of-the-art commercial memory systems (Mem0, Letta, Supermemory, Zep) score 85%+ on recall benchmarks. On held-out behavioral prediction tasks, which are a direct test of representational accuracy, their performance is uneven and, for several subjects in our study, indistinguishable from a no-memory baseline. Across 14 subjects and 515 behavioral prediction questions (controlled config, all systems given identical fact pool), the three embedding-based systems (Mem0, Letta, Supermemory) fail to share any common fact in all three systems' top-1 on 93% of questions (83% at top-3, 74% at top-5, 53% at top-10); in the native config where each system runs its own ingestion, disagreement is 100% at every top-k. These systems solved retrieval. Retrieval is not representation.",
    ),
    # L219
    (
        "To test whether representational accuracy is improvable by structured approaches, we propose and evaluate one such approach: the **Behavioral Specification**, a compressed (~5,000-8,000 token) document that encodes how a person thinks, decides, and reasons. It is generated by an automated pipeline from source text — extracting behavioral facts using a constrained 47-predicate vocabulary, authoring three interpretive layers (anchors, core, predictions) blindly from the facts, and composing them into a unified specification — and served alongside any model as persistent context. Every claim traces back through supporting facts to source text. The specification is one concrete instance of structured interpretive representation; other instances are possible and should be tested.",
        "To test whether representational accuracy is improvable by structured approaches, we propose and evaluate one such approach: the **Behavioral Specification**, a compressed (~5,000-8,000 token) document that encodes how a person thinks, decides, and reasons. The specification is generated by an automated pipeline that extracts behavioral facts using a constrained 47-predicate vocabulary, authors three interpretive layers (anchors, core, predictions) blindly from the facts, and composes them into a unified document. The resulting specification is served alongside any model as persistent context. Every claim traces back through supporting facts to source text. The specification is one concrete instance of structured interpretive representation; other instances are possible and should be tested.",
    ),
    # L221
    (
        "We evaluated the specification across 14 historical figures (public domain autobiographies), 5 memory systems (the 4 commercial systems plus Base Layer, a locally-hostable MiniLM+ChromaDB baseline), 6 response models from 3 providers (Anthropic, OpenAI, Google), and 7 calibrated LLM judges. We used behavioral prediction accuracy on held-out scenarios as the operational test of representational accuracy — if the model's working model of the person is accurate, accurate prediction on unseen situations follows.",
        "We evaluated the specification across 14 historical figures (public domain autobiographies), 5 memory systems (the 4 commercial systems plus Base Layer, a locally-hostable MiniLM+ChromaDB baseline), 6 response models from 3 providers (Anthropic, OpenAI, Google), and 7 calibrated LLM judges. We used behavioral prediction accuracy on held-out scenarios as the operational test of representational accuracy. If the model's working model of the person is accurate, accurate prediction on unseen situations follows.",
    ),
    # L225
    (
        "1. **The specification improves prediction for subjects the model has low pretraining knowledge of.** 12 of 14 subjects show positive improvement of facts+spec over baseline (Wilcoxon signed-rank p=0.006, N=14). The relationship between pretraining baseline and spec improvement is continuous and strong: linear regression slope −0.98 (95% CI −1.30, −0.74). For the 9 subjects with low pretraining representation (baseline ≤2.0) — the slice that approximates real AI users — improvement is uniform: 9 of 9 positive, mean +1.04 points on the 1-5 scale. The 2 subjects where the spec did not help are the 2 with the highest baselines (≥2.6).",
        "1. **The specification improves prediction for subjects the model has low pretraining knowledge of.** 12 of 14 subjects show positive improvement of facts+spec over baseline (Wilcoxon signed-rank p=0.006, N=14). The relationship between pretraining baseline and spec improvement is continuous and strong: linear regression slope −0.98 (95% CI −1.30, −0.74). For the 9 subjects with low pretraining representation (baseline ≤2.0), which constitute the slice that approximates real AI users, improvement is uniform: 9 of 9 positive, mean +1.04 points on the 1-5 scale. The 2 subjects where the spec did not help are the 2 with the highest baselines (≥2.6).",
    ),
    # L227
    (
        "2. **The specification is portable across providers and complements existing memory systems.** Layered on top of Mem0, Letta-controlled, and Zep, the specification produces statistically robust positive deltas. For Supermemory — which has the highest C1 baselines in the battery, indicating strong native retrieval — the spec hits a ceiling effect rather than a failure mode (the spec's complementary value is smaller for the system that has already captured the most retrieval value). The cross-provider Tier 2 replication (Sonnet, Gemini Pro response models reading GPT-5.4 batteries) reproduced the spec direction in 5 of 6 (subject × response model) cells, defusing concerns about within-Anthropic circularity. The Tier 2 data also empirically demonstrated cross-provider pretraining variance: the same subject's baseline accuracy varies by 1-2 points across response models, supporting the spec's role as a portability layer.",
        "2. **The specification is portable across providers and complements existing memory systems.** Layered on top of Mem0, Letta-controlled, and Zep, the specification produces statistically robust positive deltas. For Supermemory, which has the highest C1 baselines in the battery and indicates strong native retrieval, the spec hits a ceiling effect rather than a failure mode (the spec's complementary value is smaller for the system that has already captured the most retrieval value). The cross-provider Tier 2 replication (Sonnet, Gemini Pro response models reading GPT-5.4 batteries) reproduced the spec direction in 5 of 6 (subject × response model) cells, defusing concerns about within-Anthropic circularity. The Tier 2 data also empirically demonstrated cross-provider pretraining variance: the same subject's baseline accuracy varies by 1-2 points across response models, supporting the spec's role as a portability layer.",
    ),
    # L231
    (
        "4. **The specification shifts models from refusal to committed prediction.** Across the 13 global subjects, 25.0% of baseline (C5) responses exhibited hedging or refusal patterns (\"I don't have enough context,\" \"cannot definitively\"). With the spec added alone, hedging dropped to 2.6%. With facts plus spec, to 0.6%. The specification is not just moving scores — it is changing what the model is willing to commit to.",
        "4. **The specification shifts models from refusal to committed prediction.** Across the 13 global subjects, 25.0% of baseline (C5) responses exhibited hedging or refusal patterns (\"I don't have enough context,\" \"cannot definitively\"). With the spec added alone, hedging dropped to 2.6%. With facts plus spec, to 0.6%. The specification is not just moving scores. It is changing what the model is willing to commit to.",
    ),
    # L233
    (
        "The 14 subjects in our study are a population biased *upward* on pretraining representation — every one has a public-domain autobiography that was almost certainly in training corpora. We did not test on living people with private data. The gradient we observe within this biased-high sample (spec helps most where baseline is lowest; uniformly positive for the low-baseline slice) gives strong *structural* evidence that the specification is broadly useful for typical living AI users — whose private decisions are not in any model's training data. But it is an extrapolation, not a direct measurement. Confirming this is the most important piece of follow-up work, and it is potentially landmark for broad personalization if the implication holds.",
        "The 14 subjects in our study are a population biased *upward* on pretraining representation. Every one has a public-domain autobiography that was almost certainly in training corpora. We did not test on living people with private data. The gradient we observe within this biased-high sample (spec helps most where baseline is lowest; uniformly positive for the low-baseline slice) gives strong *structural* evidence that the specification is broadly useful for typical living AI users, whose private decisions are not in any model's training data. But it is an extrapolation, not a direct measurement. Confirming this is the most important piece of follow-up work, and it is potentially landmark for broad personalization if the implication holds.",
    ),
    # L237
    (
        "1. **Claim tested and supported (N=14):** A behavioral specification improves held-out prediction accuracy as an inverse-proportional gradient against pretraining baseline (slope −0.98 [95% CI −1.30, −0.74], Wilcoxon p=0.006). 12 of 14 subjects show positive delta. As a sensitivity check, when restricted post hoc to the 9 subjects with C5 ≤ 2.0 — the slice that approximates the typical real AI user with low pretraining representation — improvement is uniform (9 of 9, mean +1.04). The locked analysis plan reports the gradient as the primary result; the threshold split is a secondary consistency check.",
        "1. **Claim tested and supported (N=14):** A behavioral specification improves held-out prediction accuracy as an inverse-proportional gradient against pretraining baseline (slope −0.98 [95% CI −1.30, −0.74], Wilcoxon p=0.006). 12 of 14 subjects show positive delta. As a sensitivity check, when restricted post hoc to the 9 subjects with C5 ≤ 2.0, which constitute the slice that approximates the typical real AI user with low pretraining representation, improvement is uniform (9 of 9, mean +1.04). The locked analysis plan reports the gradient as the primary result; the threshold split is a secondary consistency check.",
    ),
    # L239
    (
        "2. **Claim proposed but extrapolated, not directly tested:** The result generalizes to living users whose private decisions are not in any training corpus. Our 14 subjects are historical figures with public autobiographies — a sample biased *upward* on pretraining representation. The structural argument for generalization is strong (if the spec helps most where baseline is lowest within a biased-high sample, it should help more on the biased-low real-user case), but this is extrapolation and we do not claim otherwise.",
        "2. **Claim proposed but extrapolated, not directly tested:** The result generalizes to living users whose private decisions are not in any training corpus. Our 14 subjects are historical figures with public autobiographies, a sample biased *upward* on pretraining representation. The structural argument for generalization is strong (if the spec helps most where baseline is lowest within a biased-high sample, it should help more on the biased-low real-user case), but this is extrapolation and we do not claim otherwise.",
    ),
    # L241
    (
        "3. **Claim *not* made:** Base Layer outperforms existing memory providers in general. Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — the Base Layer specification produces statistically robust positive aggregate deltas on three of the four (Mem0, Letta-controlled, Zep). On Supermemory the aggregate delta is near zero, a ceiling artifact rather than a mechanism failure: Supermemory's strong native retrieval lifts most subjects out of the baseline range where the spec has headroom; on the low-baseline subjects within Supermemory's data, the spec still helps. Our contribution is that the specification layer is *additive* to the existing memory-provider stack, not a replacement; we tested on a new axis (behavioral prediction) the providers weren't optimized for.",
        "3. **Claim *not* made:** Base Layer outperforms existing memory providers in general. Base Layer is not a memory system. Layered on top of four commercial ones (Mem0, Letta, Zep, Supermemory), the Base Layer specification produces statistically robust positive aggregate deltas on three of the four (Mem0, Letta-controlled, Zep). On Supermemory the aggregate delta is near zero, a ceiling artifact rather than a mechanism failure: Supermemory's strong native retrieval lifts most subjects out of the baseline range where the spec has headroom, and on the low-baseline subjects within Supermemory's data, the spec still helps. Our contribution is that the specification layer is *additive* to the existing memory-provider stack, not a replacement, and we tested on a new axis (behavioral prediction) the providers were not optimized for.",
    ),
    # L243
    (
        "In addition to the gradient and the additivity result, the study produces one architectural finding the field should consider: **Letta's stateful-agent self-editing memory block, the most architecturally ambitious approach in the comparison, scales poorly. Across three subjects spanning a 9× corpus-size range (25K → 48K → 223K words), the block grows linearly, accumulates 25% verbatim sentence duplication at the largest size, and saturates against a 333,000-character API ceiling — at which point 10% of the source corpus could not be ingested. Base Layer's compose step keeps the spec at 34-40K characters across the same range. This is not a takedown; it is an open problem for stateful-agent memory architectures at user-corpus scale, and we report it so the field can engage with it.**",
        "In addition to the gradient and the additivity result, the study produces one architectural finding the field should consider: **Letta's stateful-agent self-editing memory block, the most architecturally ambitious approach in the comparison, scales poorly. Across three subjects spanning a 9× corpus-size range (25K → 48K → 223K words), the block grows linearly, accumulates 25% verbatim sentence duplication at the largest size, and saturates against a 333,000-character API ceiling. At that ceiling, 10% of the source corpus could not be ingested. Base Layer's compose step keeps the spec at 34-40K characters across the same range. This is not a takedown; it is an open problem for stateful-agent memory architectures at user-corpus scale, and we report it so the field can engage with it.**",
    ),
    # L247
    (
        "1. **Representational accuracy is a real, measurable property** — it varies widely across subjects and approaches, and structured methods can improve it.",
        "1. **Representational accuracy is a real, measurable property.** It varies widely across subjects and approaches, and structured methods can improve it.",
    ),
    # L250
    (
        "4. **Behavioral alignment depends on representational accuracy.** An AI acting on someone's behalf cannot act the way that person would act if it lacks an accurate internal model of how they reason. This makes representational accuracy — not recall — the load-bearing property for personalized AI, and a missing thread in the broader human–AI interaction and alignment literature.",
        "4. **Behavioral alignment depends on representational accuracy.** An AI acting on someone's behalf cannot act the way that person would act if it lacks an accurate internal model of how they reason. This makes representational accuracy, not recall, the load-bearing property for personalized AI, and a missing thread in the broader human–AI interaction and alignment literature.",
    ),
    # L252
    (
        "This paper is a beginning. The question it opens — *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, audit, and own that representation?* — is a long-term research direction, not a benchmark to be topped. We invite extensions.",
        "This paper is a beginning. The question it opens is a long-term research direction, not a benchmark to be topped: *how does an AI accurately represent a specific person's reasoning, and by what means do we measure, improve, audit, and own that representation?* We invite extensions.",
    ),
]


def apply_rewrites(md_text, rewrites):
    applied = 0
    missing = []
    for old, new in rewrites:
        if old in md_text:
            md_text = md_text.replace(old, new, 1)
            applied += 1
        else:
            missing.append(old[:120])
    return md_text, applied, missing


def main():
    md_text = MD.read_text(encoding="utf-8")

    # Split off editorial block (L1-197) from paper prose (L198+)
    lines = md_text.split("\n")
    editorial = "\n".join(lines[:197])
    prose = "\n".join(lines[197:])

    em_before_prose = prose.count("\u2014")
    em_before_editorial = editorial.count("\u2014")

    new_prose, applied, missing = apply_rewrites(prose, REWRITES)
    em_after_prose = new_prose.count("\u2014")

    print(f"Em-dashes in prose before: {em_before_prose}")
    print(f"Rewrites applied: {applied} / {len(REWRITES)}")
    print(f"Em-dashes in prose after:  {em_after_prose}")
    print(f"(Editorial block untouched: {em_before_editorial} em-dashes — will be removed before publication)")

    # Write back (idempotent — unmatched usually means already applied in prior run)
    out = editorial + "\n" + new_prose
    MD.write_text(out, encoding="utf-8")
    print("\nFile updated.")

    if missing:
        print(f"\nWARNING: {len(missing)} rewrites unmatched (likely already applied, or text drifted):")
        for m in missing[:3]:
            print(f"  - {m}")
        if len(missing) > 3:
            print(f"  ... and {len(missing) - 3} more")


if __name__ == "__main__":
    main()
