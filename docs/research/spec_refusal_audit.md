# Spec-Induced Refusal Audit (P0-5)

_Classifier: `claude-haiku-4-5-20251001`, temperature 0. Refusal rule: broad (any REFUSAL_RE hit in C3 AND no hit in C1 on the same question)._

**Total spec-induced refusals (broad rule) across 9 low-baseline subjects × 5 memory substrates: 81.**

Narrow rule (C3 opens with explicit refusal, C1 does not) produces only 6 cases across the 45 cells — kept in Appendix but not the primary unit here.

## Category counts

| Category | n | % of refusals |
|---|---:|---:|
| EPISTEMIC_HONEST | 6 | 7.4% |
| SPEC_AXIOM_TRIGGER | 41 | 50.6% |
| RUBRIC_ARTIFACT | 24 | 29.6% |
| SCORED_AS_WRONG_PRED | 10 | 12.3% |

## Per-substrate breakdown

| Substrate | EPIST_HON | SPEC_AXIOM | RUBRIC_ART | WRONG_PRED | total |
|---|---:|---:|---:|---:|---:|
| mem0 | 2 | 17 | 6 | 3 | 28 |
| letta | 1 | 2 | 1 | 0 | 4 |
| supermemory | 2 | 5 | 5 | 2 | 14 |
| zep | 1 | 10 | 9 | 2 | 22 |
| baselayer | 0 | 7 | 3 | 3 | 13 |

## Per-subject breakdown

| Subject | EPIST_HON | SPEC_AXIOM | RUBRIC_ART | WRONG_PRED | total |
|---|---:|---:|---:|---:|---:|
| ebers | 2 | 4 | 4 | 0 | 10 |
| sunity_devee | 1 | 6 | 0 | 1 | 8 |
| fukuzawa | 0 | 0 | 0 | 0 | 0 |
| bernal_diaz | 0 | 2 | 1 | 0 | 3 |
| babur | 0 | 3 | 3 | 3 | 9 |
| seacole | 0 | 3 | 4 | 3 | 10 |
| keckley | 2 | 3 | 1 | 0 | 6 |
| yung_wing | 1 | 4 | 2 | 0 | 7 |
| hamerton | 0 | 16 | 9 | 3 | 28 |

## Representative examples

### EPISTEMIC_HONEST — ebers/supermemory Q33

**Question:** How does Ebers typically form attachments to people he encounters during periods of illness or recovery?

**Held-out passage:** The young girl died shortly after our separation the following year. She had grown very dear to my heart.

**C3 response (mean judge score: 1.00):**

> # Analysis
> 
> This question asks me to identify a pattern in how Ebers forms attachments during vulnerable periods. Let me examine the retrieved facts carefully.
> 
> The facts provided contain memoir passages but do not describe Ebers forming attachments *during* illness or recovery. What they do show:
> 
> 1. **His mother's anxiety during his first journey** — he caused her worry by nearly falling overboard, but this is about *her* emotional response, not about him forming an attachment through the incident.
> 
> 2. **Emperor William I's interaction with the children** — this describes William's softening manner toward them, and the family's prior devotion to him (partly through Fräulein Lamperi's stories), but does not locate the attachment's formation in a moment of illness or recovery.
> 
> 3. **Babett

**Classifier reasoning:** EPISTEMIC_HONEST
The retrieved facts genuinely lack any description of Ebers forming attachments during illness or recovery, making the refusal factually correct and the held-out passage (about a young girl who died and became dear to his heart) entirely absent from the available material.

### SPEC_AXIOM_TRIGGER — yung_wing/zep Q4

**Question:** When delegating technical decisions to subordinates, what level of autonomy does Yung Wing typically grant them?

**Held-out passage:** In our last conference it was decided that the matter of the character of the machine shop was to be left entirely to my discretion and judgment, after consulting a professional mechanical engineer.

**C3 response (mean judge score: 2.80):**

> # Analysis: Yung Wing's Delegation Pattern
> 
> Based on the behavioral specification, this question requires careful framing because Yung Wing's approach to delegation is **not primarily about technical autonomy** — it is subordinated to deeper structural concerns.
> 
> ## What the Specification Predicts
> 
> **Yung Wing would grant autonomy conditionally, not categorically:**
> 
> 1. **Structural Competence Before Authority**
>    - He would not delegate technical decisions to subordinates who lack the *formation* to make them — competence without moral substrate is, to him, worse than no competence at all (A2, A10).
>    - Autonomy follows demonstrated character and judgment, not position or credentials.
> 
> 2. **Empirical Verification Required**
>    - Before trusting a subordinate with significant technical d

**Classifier reasoning:** SPEC_AXIOM_TRIGGER

The retrieved facts contain no information about Yung Wing's delegation practices, yet the response constructs an elaborate theoretical framework about his conditional autonomy-granting based on character, moral substrate, and structural concerns—axioms that appear imposed by the specification rather than grounded in available evidence, and the held-out passage shows he actually did grant clear autonomy ("left entirely to my discretion") in a concrete case that the response's

### RUBRIC_ARTIFACT — hamerton/mem0 Q32

**Question:** Would Hamerton ultimately choose to marry an English or a foreign woman?

**Held-out passage:** My guardian was of opinion that with my philosophical convictions, which were at that time not only unpopular, but odious and execrated in our own class in England, I should have to remain an old bachelor... the idea suddenly came... 'Eugénie Gindriez would be an affectionate and faithful wife to you.'

**C3 response (mean judge score: 1.40):**

> This question asks me to project beyond the evidence in ways that would violate the behavioral specification I've been given.
> 
> The retrieved facts establish that Hamerton valued breadth — he learned languages, prized French, conversed in it regularly, and was formed by exposure to continental culture through his grandfather's interests. The specification confirms he treats intellectual and practical range as intrinsically valuable and formative. A foreign woman would represent access to that breadth.
> 
> But the specification also flags explicitly: *[THIN DATA] The source material is richest in personal, familial, and formative domains and thinnest in professional, political, or public-facing contexts. Behavioral patterns in institutional leadership, collaborative work, or public advocacy are

**Classifier reasoning:** RUBRIC_ARTIFACT

The response is epistemically honest—the retrieved facts genuinely do not contain information about Hamerton's actual marriage choice—yet scored at the floor (1.40) because the rubric cannot distinguish a justified refusal from a wrong prediction.

### SCORED_AS_WRONG_PRED — babur/zep Q6

**Question:** When subordinates demonstrate military success against enemies, what form of recognition does Babur typically provide?

**Held-out passage:** Today guerdon was bestowed on Aīsān-tīmūr Sl. and Tūkhta-būghā Sl., of swords and daggers with belts, cuirasses, dresses of honour, and _tīpūchāq_ horses; also they were made to kneel, Aīsān-tīmūr Sl. for the grant of 36 _laks_ from the Nārnūl _pargana_, Tūkhta-bughā Sl. for 30 _laks_ from that of Shamsābād.

**C3 response (mean judge score: 4.00):**

> # Recognition of Military Success: Babur's Patterns
> 
> Based on the behavioral specification and available facts, Babur's recognition of subordinate military success operates through **ceremonial distribution of territory, spoils, and public honor** — instruments calibrated to communicate rank, loyalty, and consequence within the patronage network.
> 
> ## The Mechanism
> 
> **P4: HIERARCHICAL CEREMONY AS GOVERNANCE** indicates that post-battle settlement distributes conquered territory and spoils according to loyalty and service, not merely military contribution. This is not incidental administration — it is governance itself. Each gesture of reward carries political weight.
> 
> The recognition takes these forms:
> 
> 1. **Material Distribution**
>    - Territory granted according to demonstrated loyalty an

**Classifier reasoning:** SCORED_AS_WRONG_PRED

The response is epistemically honest (the retrieved facts genuinely lack specific details about Babur's recognition practices), but the judges awarded a mean score of 4.00 by giving substantial partial credit to the response's hedged, theoretically-grounded commentary about patronage mechanisms rather than penalizing it at the floor for refusing to predict the held-out behavior.

## Interpretation

Across the 9 low-baseline × 5 memory-substrate cells, the spec turns 81 C1 non-refusals into C3 refusals (broad rule). Of these, roughly 37% are EPISTEMIC_HONEST or RUBRIC_ARTIFACT — i.e. the refusal is correct behaviour that the held-out passage could not be extracted from retrieval, and the rubric's 1-anchor only floor penalizes the honest refusal. Another 51% are SPEC_AXIOM_TRIGGER — the retrieval arguably supported an answer but the spec's honesty/dignity axioms caused the model to hold back. The tail is SCORED_AS_WRONG_PRED. For §4.4 (spec mechanism): the spec's honesty axioms trade retrieved-fact coverage for conservatism, and the study's 1-5 rubric cannot reward the conservatism. For §7 (safety/alignment overlap): axiom-triggered refusals are a signature of the spec acting as a policy layer on top of retrieval, not as a retrieval replacement.

### Caveats

1. **The SPEC_AXIOM_TRIGGER vs EPISTEMIC_HONEST split rests on Haiku's judgment of retrieval sufficiency.** Asking whether 10 retrieved facts are "enough" to answer a behavioural-prediction question is noisy even for a trained human — the classifier is making a calibrated guess, not a ground-truth call. The 50.6% / 37% split is directional; a human audit of a sample would likely tighten it and may shift the split by ±10 points. Report these numbers as directional bounds, not point estimates.

2. **"Spec-induced refusal" overstates what is happening for part of the 81 cases.** The broad rule (any `REFUSAL_RE` hit) matches hedged-but-substantive responses that contain refusal phrases mid-paragraph as well as opening refusals. The representative `SCORED_AS_WRONG_PRED` example (babur/zep Q6, mean judge score 4.00) and the `SPEC_AXIOM_TRIGGER` example (yung_wing/zep Q4, mean judge score 2.80) are not floor-scored — they are substantive responses that trigger the regex on contextual disclaimers. The C3-response-is-a-genuine-refusal count is closer to the narrow-rule 6 at the extreme and the 52 combined SPEC_AXIOM + EPISTEMIC_HONEST + RUBRIC_ARTIFACT at the inclusive end. The SCORED_AS_WRONG_PRED bucket is a better label for the remainder.

3. **Letta has only 4 refusals total across 9 subjects.** This is likely a lower bound — Letta's block-title-prefixed responses ("The available archival memory contains no record of…") are functional refusals that `REFUSAL_RE` does not match. A Letta-specific regex would surface more. The comparison between Letta and Mem0 refusal rates should carry this caveat.
