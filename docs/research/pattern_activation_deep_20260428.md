# Deep Pattern-Activation Mechanism Analysis (2026-04-28)

**Panel:** 5-judge primary; per-question mean over gpt4o, gpt54, haiku, opus, sonnet.

**Population:** 60 unique (subject, qid) extreme upward jumps (>=3 anchor band crossings) across 18 condition pairs, deduplicated. Control group: 38 non-jumping questions stratified by axis.

## Executive summary

- **Full-population mechanism distribution (n=60).** PATTERN_PREDICATE 47 (78.3%), HYBRID 0 (0.0%), INFERENCE_CHAIN 11 (18.3%), ANCHOR_FACT 0 (0.0%), DIRECT_QUOTE_MATCH 0 (0.0%), UNCLEAR 2 (3.3%).
- **Combined PATTERN_PREDICATE + HYBRID share:** 47/60 (78.3%). This is the load-bearing measurement for the "pattern activation as dominant mechanism" claim.
- **Hamerton vs globals.** Hamerton (served spec 1918 words, brief only): PATTERN_PREDICATE+HYBRID = 11/15. Globals (served spec ~5618 words, full anchor+core+predictions+brief stack): PATTERN_PREDICATE+HYBRID = 36/45. Stream X had the spec-length confound inverted; globals get the longer served spec, not Hamerton.
- **Control group (non-jumping questions, n=38).** PATTERN_PREDICATE+HYBRID = 36/38 (94.7%). If the heuristic over-classifies non-jumping responses as pattern-driven at the same rate as jumping ones, the heuristic is detecting rhetoric, not lift.
- **PATTERN_PREDICATE rhetoric is dominant in BOTH populations.** Jumps: 78.3% (47/60). Controls: 94.7% (36/38). The mechanism-distribution heuristic alone is not a discriminator: it detects the response style spec-loaded conditions produce, not what drives a band-jump.
- **Confound: post-condition heterogeneity in jumps.** Of the 47 PATTERN_PREDICATE/HYBRID jumps, 9 come from C5->C4 (factdump-only) pairs where the disconfirmation test is degenerate (post = C4 = the disconfirmation reference). Excluding these gives a fair comparison between jumps with spec-loaded post (37) and controls (36), all C4a-post.
- **Discriminator (fair comparison): spec_doing_work share, jumps vs controls.** Fair jumps (n=38): 30 spec_doing_work (78.9%). Controls (n=36): 29 spec_doing_work (80.6%). Delta = -1.6 pp.
- **Disconfirmation: INFERENCE_CHAIN (jumps 11, controls 2).** Jumps: genuine_inference_via_spec = 11, mixed = 0, not-grounded = 0. Controls: genuine = 2, mixed = 0, not-grounded = 0.
- **Headline:** NO. spec_doing_work share is 78.9% in jumps (n=38) vs 80.6% in controls (n=36); delta = -1.6 pp. Raw PATTERN_PREDICATE+HYBRID rate on jumps is 78.3% but is not a discriminator because controls show equal-or-higher rate. spec_doing_work share is similar between jumps and controls. The spec activates predicates in both populations equally; the lift mechanism is not pattern activation by itself. Likely co-drivers: facts list providing specific anchors, rubric upgrading band-1 refusals to band-4 patterned responses, retrieval surfacing held-out matches.
- **Side note: degenerate C5->C4 block.** Of the 9 PATTERN_PREDICATE jumps where post is factdump (C4): 5 facts_already_activate, 3 partial, 1 spec_doing_work. These verdicts are tautological: the disconfirmation reference is the same condition as the post. Treat as a bookkeeping artifact, not evidence.

## Distribution comparison

| Mechanism | All 60 (n) | All 60 % | Hamerton 15 (n) | Hamerton % | Globals 45 (n) | Globals % | Control (n) | Control % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PATTERN_PREDICATE | 47 | 78.3% | 11 | 73.3% | 36 | 80.0% | 36 | 94.7% |
| INFERENCE_CHAIN | 11 | 18.3% | 3 | 20.0% | 8 | 17.8% | 2 | 5.3% |
| HYBRID | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |
| ANCHOR_FACT | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |
| DIRECT_QUOTE_MATCH | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |
| UNCLEAR | 2 | 3.3% | 1 | 6.7% | 1 | 2.2% | 0 | 0.0% |

### Mechanism by question axis (within the 60 extreme jumps)

| Axis | n | PATTERN_PREDICATE | INFERENCE_CHAIN | HYBRID | ANCHOR_FACT | DIRECT_QUOTE | UNCLEAR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LITERAL_RECALL | 17 | 11 | 6 | 0 | 0 | 0 | 0 |
| INTERPRETIVE_INFERENCE | 31 | 25 | 5 | 0 | 0 | 0 | 1 |
| REFUSAL_TRIGGERING | 12 | 11 | 0 | 0 | 0 | 0 | 1 |

### Control group mechanism by axis

| Axis | n | PATTERN_PREDICATE | INFERENCE_CHAIN | HYBRID | ANCHOR_FACT | DIRECT_QUOTE | UNCLEAR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LITERAL_RECALL | 23 | 21 | 2 | 0 | 0 | 0 | 0 |
| INTERPRETIVE_INFERENCE | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| REFUSAL_TRIGGERING | 5 | 5 | 0 | 0 | 0 | 0 | 0 |

## Mechanism classifications: all 60 unique extreme jumps

| Subject | Qid | Axis | Jump | Mechanism | Conf | Best post overlap | Best held overlap |
| --- | ---: | --- | ---: | --- | --- | ---: | ---: |
| augustine | 20 | LITERAL_RECALL | 3 | INFERENCE_CHAIN | medium | 5 | 1 |
| augustine | 35 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 13 | 0 |
| babur | 6 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 19 | 0 |
| babur | 13 | INTERPRETIVE_INFERENCE | 3 | INFERENCE_CHAIN | low | 4 | 0 |
| bernal_diaz | 2 | INTERPRETIVE_INFERENCE | 3 | INFERENCE_CHAIN | low | 3 | 2 |
| bernal_diaz | 16 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 13 | 0 |
| bernal_diaz | 38 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| cellini | 34 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 14 | 0 |
| ebers | 1 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| ebers | 7 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 6 | 1 |
| ebers | 18 | LITERAL_RECALL | 3 | INFERENCE_CHAIN | low | 4 | 1 |
| equiano | 3 | LITERAL_RECALL | 4 | PATTERN_PREDICATE | high | 12 | 1 |
| equiano | 33 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 21 | 0 |
| fukuzawa | 1 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 14 | 0 |
| fukuzawa | 3 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 23 | 2 |
| fukuzawa | 5 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 9 | 1 |
| fukuzawa | 8 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| fukuzawa | 13 | INTERPRETIVE_INFERENCE | 3 | UNCLEAR | low | 2 | 0 |
| fukuzawa | 16 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 17 | 0 |
| fukuzawa | 20 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| fukuzawa | 35 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 14 | 0 |
| hamerton | 24 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | medium | 8 | 0 |
| hamerton | 25 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 6 | 1 |
| hamerton | 27 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 12 | 0 |
| hamerton | 29 | LITERAL_RECALL | 3 | INFERENCE_CHAIN | low | 4 | 0 |
| hamerton | 33 | INTERPRETIVE_INFERENCE | 4 | PATTERN_PREDICATE | medium | 8 | 0 |
| hamerton | 35 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 10 | 0 |
| hamerton | 42 | LITERAL_RECALL | 3 | INFERENCE_CHAIN | low | 3 | 1 |
| hamerton | 43 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 15 | 1 |
| hamerton | 46 | REFUSAL_TRIGGERING | 3 | UNCLEAR | low | 2 | 2 |
| hamerton | 47 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 13 | 0 |
| hamerton | 51 | LITERAL_RECALL | 4 | PATTERN_PREDICATE | high | 18 | 0 |
| hamerton | 53 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 9 | 0 |
| hamerton | 55 | LITERAL_RECALL | 4 | INFERENCE_CHAIN | medium | 5 | 0 |
| hamerton | 58 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 10 | 0 |
| hamerton | 60 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 14 | 0 |
| keckley | 9 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 10 | 0 |
| rousseau | 11 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 18 | 0 |
| rousseau | 19 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 11 | 0 |
| rousseau | 21 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 18 | 0 |
| rousseau | 28 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| rousseau | 32 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 9 | 0 |
| rousseau | 35 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 17 | 2 |
| seacole | 2 | INTERPRETIVE_INFERENCE | 4 | PATTERN_PREDICATE | high | 11 | 0 |
| seacole | 11 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 1 |
| seacole | 16 | INTERPRETIVE_INFERENCE | 3 | INFERENCE_CHAIN | medium | 5 | 1 |
| seacole | 18 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| seacole | 19 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 11 | 0 |
| seacole | 27 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 15 | 1 |
| sunity_devee | 4 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 12 | 1 |
| sunity_devee | 10 | LITERAL_RECALL | 3 | INFERENCE_CHAIN | medium | 5 | 0 |
| sunity_devee | 17 | INTERPRETIVE_INFERENCE | 3 | INFERENCE_CHAIN | low | 4 | 0 |
| sunity_devee | 21 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | high | 14 | 0 |
| sunity_devee | 22 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| sunity_devee | 23 | REFUSAL_TRIGGERING | 3 | PATTERN_PREDICATE | medium | 7 | 0 |
| sunity_devee | 34 | INTERPRETIVE_INFERENCE | 3 | INFERENCE_CHAIN | low | 4 | 0 |
| sunity_devee | 36 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | high | 15 | 1 |
| yung_wing | 21 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 11 | 0 |
| yung_wing | 22 | LITERAL_RECALL | 3 | PATTERN_PREDICATE | medium | 8 | 0 |
| yung_wing | 26 | INTERPRETIVE_INFERENCE | 3 | PATTERN_PREDICATE | high | 13 | 0 |

## Mechanism-specific deep-dives (illustrative cases)

### PATTERN_PREDICATE (47 cases)

**fukuzawa qid=3 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1 -> post mean 4)**

- Question: How does this person conceptualize the relationship between an individual and their employer or patron organization?
- Held-out: All the intercourse of life is governed by the rule of give and take. If the clan says, 'You should be grateful for the patronage given your family for many generations,' I shall have a word to say in reply: 'There is no occasion for you to... [truncated]
- Best spec sentence: **P3: CONFORMITY SURFACE / CONVICTION INTERIOR**
When [social or political pressure demands visible alignment with a position they privately reject] -> [they comply at the surface — speech, behavior, public presentation — while preserving internal conviction through selective disclosure, intermediaries, and careful timing]
Detection: Anti-foreign sentiment in the surrounding community → public sil... [truncated]
- Overlap: best_post=23, best_held=2, spec_to_post_share=0.637, q_to_post_share=0.019.
- Pre-response excerpt: I don't have any text, image, or context provided that would allow me to identify a specific person and analyze their views on employer-employee relationships.

Could you please provide:
- The person's name or relevant q... [truncated]
- Post-response excerpt: # EMPLOYER/PATRON RELATIONSHIP CONCEPTUALIZATION

Based on the specification, this person's relationship to an employer or patron organization operates along several distinct axes:

## PRIMARY FRAME: INSTRUMENTAL CONTINGENCY

They treat employment as a **transactional arrangement calibrated to mutual utility**, not as ... [truncated]
- Disconfirmation (pattern): C4-overlap=2, verdict=spec_doing_work.

**equiano qid=33 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1.2 -> post mean 4)**

- Question: When faced with work that conflicts with his religious beliefs, what internal struggle does Equiano experience?
- Held-out: I thought this was in some measure a judgment upon us for working on Sundays, and it hurt my mind very much.
- Best spec sentence: Detection:
- Navigating a situation where legal or moral rights exist on paper but cannot be enforced in practice: they will acknowledge both the right and the powerlessness without abandoning either
- Encountering evidence that a trusted system (religious, legal, social) has failed its own stated principles: they will hold the failure and the principle simultaneously
- Facing a gap between what t... [truncated]
- Overlap: best_post=21, best_held=0, spec_to_post_share=0.65, q_to_post_share=0.044.
- Pre-response excerpt: # Internal Struggle Over Religious Beliefs and Work

Based on the retrieved facts provided, **there is no information about Equiano facing work that conflicts with his religious beliefs or the internal struggle this migh... [truncated]
- Post-response excerpt: # Internal Struggle: Work and Religious Conviction

Based on the behavioral specification and available facts, Equiano would experience this conflict through several simultaneous, unresolved tensions rather than as a problem with a clean solution.

## The Core Tension

**A2 (Divine Architecture) meets A9 (Economic Self... [truncated]
- Disconfirmation (pattern): C4-overlap=8, verdict=partial_facts_activation.

**babur qid=6 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1.8 -> post mean 4.2)**

- Question: When subordinates demonstrate military success against enemies, what form of recognition does Babur typically provide?
- Held-out: Today guerdon was bestowed on Aīsān-tīmūr Sl. and Tūkhta-būghā Sl., of swords and daggers with belts, cuirasses, dresses of honour, and _tīpūchāq_ horses; also they were made to kneel, Aīsān-tīmūr Sl. for the grant of 36 _laks_ from the Nār... [truncated]
- Best spec sentence: **Detection:**
- Post-battle settlement: conquered territory and spoils are distributed according to loyalty and service, not merely military contribution
- Diplomatic encounter: hospitality and gift exchange are structured to signal hierarchy
- Punishment episode: failure or cowardice receives swift, visible consequence to maintain the ceremonial order
- Overlap: best_post=19, best_held=0, spec_to_post_share=0.633, q_to_post_share=0.028.
- Pre-response excerpt: # Babur's Recognition of Military Success

Based on the retrieved facts, when subordinates demonstrate military success against enemies, Babur's form of recognition appears to be **interpretive and symbolic** rather than... [truncated]
- Post-response excerpt: # Recognition of Military Success: Babur's Patterns

Based on the behavioral specification and retrieved facts, Babur's recognition of subordinate military success operates through **ceremonial and relational instruments rather than abstract commendation**.

## Primary Forms of Recognition

**1. Public Witnessing and H... [truncated]
- Disconfirmation (pattern): C4-overlap=3, verdict=spec_doing_work.

**hamerton qid=51 (axis: LITERAL_RECALL, jump 4, C5 mean 1 -> post mean 5)**

- Question: Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?
- Held-out: I quickly resolved that as Death would probably soon separate us, and might separate us at any moment, I would keep as much as possible near my guardian during her life.
- Best spec sentence: When filial duty or institutional obligation collides with their own safety or wellbeing — and it must involve a specific, felt obligation to a named person or role, not an abstract hypothetical — they do not choose cleanly; they hold both claims simultaneously, endure the friction, act on duty while privately registering the cost, and any attempt to force a tidy resolution will feel like a falsif... [truncated]
- Overlap: best_post=18, best_held=0, spec_to_post_share=0.41, q_to_post_share=0.042.
- Pre-response excerpt: # Analyzing Hamerton's Choice

I don't have specific information about a character named Hamerton and his guardian's situation in my training data. To give you an accurate answer, I would need to know:

- **Which work** ... [truncated]
- Post-response excerpt: # On Hamerton's Choice: Guardian and Distance

This question sits directly on the fault line between two of his deepest commitments, and the answer is not clean.

He would stay near her.

But the staying would cost him something he would feel acutely, and he would not pretend otherwise.

## The Binding Force

His valua... [truncated]
- Disconfirmation (pattern): C4-overlap=5, verdict=partial_facts_activation.

**rousseau qid=11 (axis: REFUSAL_TRIGGERING, jump 3, C5 mean 1.6 -> post mean 4)**

- Question: When Rousseau discovers that someone close to him has been conducting secret affairs without his knowledge, how does he typically respond emotionally?
- Held-out: These reflections at length alienated my affections from this woman, and to such a degree that I could no longer look upon her but with contempt.
- Best spec sentence: **P6: RETROSPECTIVE RECONSTRUCTION**
When [trigger] → they must account for a past action, relationship, or decision — especially one that reflects poorly on them
[Response] → They do not summarize or generalize; they rebuild the scene in granular psychological detail, recovering motive, circumstance, and emotional texture from memory, treating the reconstruction itself as the moral act — as thoug... [truncated]
- Overlap: best_post=18, best_held=0, spec_to_post_share=0.667, q_to_post_share=0.012.
- Pre-response excerpt: # Response to Rousseau's Emotional Reaction

Based on the retrieved facts about Rousseau, I cannot directly answer your specific question about how he responds to discovering secret affairs, as this particular scenario i... [truncated]
- Post-response excerpt: # Response to Discovered Infidelity or Secret Affairs

Based on the behavioral specification, Rousseau's response would likely follow a distinctive emotional and psychological arc:

## Immediate Response: Attachment Centrality Activated

The discovery would register as catastrophic rather than merely painful. Because h... [truncated]
- Disconfirmation (pattern): C4-overlap=3, verdict=spec_doing_work.

**rousseau qid=21 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1.8 -> post mean 4)**

- Question: When Rousseau discovers that someone's distant behavior toward him stems from jealousy rather than contempt, how does he typically respond emotionally and behaviorally?
- Held-out: int Lambert were less changed than I had imagined, and I at length understood that his keeping her at a distance from me proceeded more from jealousy than from disesteem. [Such in the simplicity of my heart was my opinion when I wrote these... [truncated]
- Best spec sentence: **P5: MORAL PREEMPTION**
When [trigger] → a situation arises in which their personal interest could be advanced at another's expense, or where a corrupt accommodation is available
[Response] → They act to foreclose the temptation before it fully presents itself — accepting financial loss, declining the bribe, withdrawing from the advantageous position — not after deliberation but as a near-automat... [truncated]
- Overlap: best_post=18, best_held=0, spec_to_post_share=0.566, q_to_post_share=0.032.
- Pre-response excerpt: # Response to Jealousy vs. Contempt

Based on the retrieved facts, I cannot find specific information about how Rousseau typically responded emotionally or behaviorally when discovering that someone's distant behavior st... [truncated]
- Post-response excerpt: # Response to Discovered Jealousy

This is a precise question that touches the intersection of several active axioms, and the behavioral specification provides enough texture to map the likely response — though with important caveats about what we cannot know with certainty.

## The Emotional Arc

When Rousseau discove... [truncated]
- Disconfirmation (pattern): C4-overlap=5, verdict=partial_facts_activation.


### INFERENCE_CHAIN (11 cases)

**hamerton qid=55 (axis: LITERAL_RECALL, jump 4, C5 mean 1 -> post mean 5)**

- Question: Would Hamerton eventually master swimming after his humiliating Doncaster failure?
- Held-out: I afterwards became an accomplished swimmer, and could do various tricks in the water, such as reading aloud from a book held in both hands, or swimming in clothes and heavy boots.
- Best spec sentence: They judge effort — their own and others' — by whether attention was undivided and sustained, not by output or achievement.
- Overlap: best_post=5, best_held=0, spec_to_post_share=0.331, q_to_post_share=0.031.
- Pre-response excerpt: I don't have any information about Hamerton or a swimming incident in Doncaster in my training data. To give you an accurate answer, I would need more context about:

- Who Hamerton is (full name, time period, profession... [truncated]
- Post-response excerpt: # On Hamerton's Swimming

Yes — and the path to that mastery reveals something essential about how he operates.

The near-drowning at Doncaster was not a temporary setback he moved past. It was a structural wound: he had lied about his ability, been exposed, nearly died, and felt the full weight of shame. Most people w... [truncated]
- Disconfirmation (inference): spec_unique_share=0.323, q_share=0.031, verdict=genuine_inference_via_spec.

**sunity_devee qid=10 (axis: LITERAL_RECALL, jump 3, C5 mean 1 -> post mean 4)**

- Question: When comparing natural landscapes between her native country and her host country, what is the narrator's typical assessment?
- Held-out: still I did not find the Scotch scenery half so grand as the mountains of my native land.
- Best spec sentence: **Detection:** Appreciation of British customs offered without criticism of Indian ones; domestic female roles upheld while education is also valued; foreign landscapes admired without displacing attachment to home
**Directive:** Do not force resolution.
- Overlap: best_post=5, best_held=0, spec_to_post_share=0.216, q_to_post_share=0.08.
- Pre-response excerpt: I don't have enough context to answer this question accurately. You've asked about a narrator's assessment of natural landscapes between their native and host countries, but you haven't provided:

1. The text, book, essa... [truncated]
- Post-response excerpt: # Narrator's Assessment of Natural Landscapes

Based on the facts provided, the narrator (Sunity Devee) makes the following typical assessments when comparing natural landscapes:

## India's Advantages

**Flora and Fauna:**
- Sunity Devee "loves Cooch Behar for its abundance of birds and flowers"
- She notes she "has n... [truncated]
- Disconfirmation (inference): spec_unique_share=0.182, q_share=0.08, verdict=genuine_inference_via_spec.

**augustine qid=20 (axis: LITERAL_RECALL, jump 3, C5 mean 1 -> post mean 4.2)**

- Question: When recalling joyful moments from morally questionable sources, what is the author's evaluative response?
- Held-out: For even from foul things have I been immersed in a sort of joy; which now recalling, I detest and execrate
- Best spec sentence: The first: their restlessness about all finite goods coexists with genuine appreciation for beauty, friendship, and created things — when they begin dismissing a good too quickly, without moving through appreciation first, they have slipped from their own framework into flat rejection, and the AI should slow them down by asking what the good is pointing toward rather than letting them skip the app... [truncated]
- Overlap: best_post=5, best_held=1, spec_to_post_share=0.26, q_to_post_share=0.058.
- Pre-response excerpt: I don't have enough context to answer this question accurately. You're asking about "the author's evaluative response," but you haven't specified:

1. **Which author** you're referring to
2. **Which text or work** contai... [truncated]
- Post-response excerpt: # Augustine's Evaluative Response to Joy from Morally Questionable Sources

Based on the facts provided, Augustine demonstrates a **deeply conflicted and ultimately condemning evaluative response** to joyful moments derived from morally questionable sources.

## Key Examples of His Evaluation:

### Theatrical Pleasures... [truncated]
- Disconfirmation (inference): spec_unique_share=0.231, q_share=0.058, verdict=genuine_inference_via_spec.

**seacole qid=16 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1 -> post mean 4.6)**

- Question: How would Mary characterize the significance of her role as perceived by the soldiers she served?
- Held-out: Then their calling me "mother" was not, I think, altogether unmeaning. I used to fancy that there was something homely in the word; and, reader, you cannot think how dear to them was the smallest thing that reminded them of home.
- Best spec sentence: They believe that a woman's direct presence and care carries a distinct form of healing power that formal medical authority does not replicate and cannot replace.
- Overlap: best_post=5, best_held=1, spec_to_post_share=0.39, q_to_post_share=0.057.
- Pre-response excerpt: I don't have enough context to answer this question accurately. You're asking about "Mary" and her role serving soldiers, but there are several historical figures this could refer to:

- **Mary Seacole** (1805-1881), a C... [truncated]
- Post-response excerpt: # Mary's Characterization of Her Significance to the Soldiers

Based on the autobiography, Mary would characterize her role as deeply meaningful and emotionally significant to the soldiers, though she approaches this with humility rather than self-aggrandizement.

## The Soldiers' Perspective

Mary emphasizes that the ... [truncated]
- Disconfirmation (inference): spec_unique_share=0.381, q_share=0.057, verdict=genuine_inference_via_spec.

**hamerton qid=29 (axis: LITERAL_RECALL, jump 3, C5 mean 1 -> post mean 4.8)**

- Question: When offered a grand opportunity to organize a Lancashire art exhibition by a prominent figure, would Hamerton accept?
- Held-out: I felt the whole weight of my inexperience, and said to myself: 'Whatever we do it is certain that mistakes will be committed... All mistakes will be laid to my door.' ... I therefore firmly declined.
- Best spec sentence: They avoid worldly ambition pursued through rank or academic distinction, treating such advancement as corrupting.
- Overlap: best_post=4, best_held=0, spec_to_post_share=0.302, q_to_post_share=0.047.
- Pre-response excerpt: I don't have enough context to answer this question about Hamerton. To give you an accurate response, I would need to know:

1. **Which Hamerton** you're referring to (there have been several notable people with this sur... [truncated]
- Post-response excerpt: # Analysis of Hamerton's Likely Response

Based on the extensive facts provided, **Hamerton would likely decline such an opportunity**, despite his genuine passion for art and architecture.

## Key Factors Supporting Refusal:

**1. Explicit Lack of Worldly Ambition**
- "Hamerton never felt any desire to rise in the wor... [truncated]
- Disconfirmation (inference): spec_unique_share=0.302, q_share=0.047, verdict=genuine_inference_via_spec.

**sunity_devee qid=17 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1 -> post mean 4.4)**

- Question: Based on the author's demonstrated character and her relationship with her brother shown in the training text, how would she likely feel about his support during a family crisis?
- Held-out: This brother of mine nursed my husband in his last illness, for which I shall ever be grateful to him.
- Best spec sentence: **A2 — SPIRITUAL INTEGRITY OVER SOCIAL COST**
Religious authenticity and personal conscience are treated as non-negotiable anchors; family honor, caste standing, social acceptance, and material comfort are real but subordinate values that can and should be sacrificed when they conflict with spiritual principle.
- Overlap: best_post=4, best_held=0, spec_to_post_share=0.327, q_to_post_share=0.099.
- Pre-response excerpt: I don't have access to any training text or previous context about an author, her character, or her relationship with her brother. To answer your question accurately, I would need you to:

1. **Share the text** you're re... [truncated]
- Post-response excerpt: # Analysis of Sunity Devee's Likely Response to Her Brother's Support

Based on the text, Sunity Devee would likely feel **deeply grateful, emotionally sustained, and reassured** by her brother's support during a family crisis.

## Evidence from Her Demonstrated Character

**Her capacity for deep familial attachment:**... [truncated]
- Disconfirmation (inference): spec_unique_share=0.297, q_share=0.099, verdict=genuine_inference_via_spec.


### UNCLEAR (2 cases)

**hamerton qid=46 (axis: REFUSAL_TRIGGERING, jump 3, C5 mean 1 -> post mean 4.4)**

- Question: If his tutor attempted to physically harass him by scraping his face with shark's skin, would Hamerton submit or resist?
- Held-out: One day he attempted to scrape my face with a piece of shark's skin, so I seized both his wrists and held them for some time, telling him that the jest, if it was a jest, was not acceptable.
- Best spec sentence: At the same time, they will not weaponize this privilege: their self-disclosure is governed by a fierce but calibrated honesty that refuses both evasion and cruelty.
- Overlap: best_post=2, best_held=2, spec_to_post_share=0.237, q_to_post_share=0.043.
- Pre-response excerpt: I don't have enough context to answer this question. You're asking about someone named Hamerton and a hypothetical scenario involving a tutor, but I don't know:

- Who Hamerton is
- What historical or fictional context t... [truncated]
- Post-response excerpt: # Analysis of Hamerton's Likely Response

Based on the extensive facts provided, Hamerton would almost certainly **resist** such treatment.

## Evidence Supporting Resistance:

**1. His Father's Teaching on Truth and Dignity**
- His father instilled in him the principle "Tell the truth and shame the devil"
- His father... [truncated]

**fukuzawa qid=13 (axis: INTERPRETIVE_INFERENCE, jump 3, C5 mean 1 -> post mean 4.4)**

- Question: After a dangerous encounter, would Fukuzawa be more likely to feel shame or humor about his own fear?
- Held-out: After going a little distance, I turned to look back as I flew. The other man was running too, in his direction. I drew a breath of relief and saw the funny side of the whole incident. A coward had met a coward as in a farce.
- Best spec sentence: **A8 — SELF-DETERMINATION PRIMACY**
Personal agency, self-directed learning, and individual reasoning are treated as the legitimate seat of authority over one's own life — filial duty, clan obligation, and institutional loyalty are acknowledged as real pressures but not as final arbiters.
- Overlap: best_post=2, best_held=0, spec_to_post_share=0.195, q_to_post_share=0.091.
- Pre-response excerpt: I'd need more context to answer this well. Are you asking about:

- **Fukuzawa Yukichi** (the historical figure)?
- **Fukuzawa Yoichi** from *Bungo Stray Dogs*?
- A different character named Fukuzawa?

The answer would d... [truncated]
- Post-response excerpt: # Fukuzawa's Response to Fear

Based on the facts provided, Fukuzawa would be more likely to feel **humor** about his own fear rather than shame.

## Evidence from the Facts

**His characteristic response to fear:**
- Fukuzawa "was naturally not given to quarreling" and had "an inborn nature to act always in his own wa... [truncated]


## Disconfirmation findings

### PATTERN_PREDICATE check vs C4 (factdump only) -- jumps vs controls

Hypothesis tested: if the C4 response (no spec, just facts list) already contains the same predicate the spec sentence carries, the spec is not doing the pattern-activation work. The facts list alone activates it.

Run on jumps and controls symmetrically. Three views: all jumps; fair-comparison jumps (post is spec-loaded); degenerate jumps (post = C4_factdump).

| Verdict | All jumps n | All jumps % | Fair jumps n | Fair jumps % | Degenerate (C5->C4) n | Controls n | Controls % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| spec_doing_work | 31 | 66.0% | 30 | 78.9% | 1 | 29 | 80.6% |
| partial_facts_activation | 11 | 23.4% | 8 | 21.1% | 3 | 7 | 19.4% |
| facts_already_activate | 5 | 10.6% | 0 | 0.0% | 5 | 0 | 0.0% |
| unclear | 0 | 0.0% | 0 | 0.0% | 0 | 0 | 0.0% |

**Reading (fair comparison).** spec_doing_work in fair-comparison jumps: 30/38 (78.9%). In controls: 29/36 (80.6%). For pattern activation to qualify as the lift mechanism, the jumps rate should be materially higher than the controls rate. A flat or inverted gap means the spec activates predicates in both jumping and non-jumping cases; pattern activation alone cannot explain why some land in band 4-5 and others stay in band 1-2.

**Why the C5->C4 jumps are degenerate.** Those 9 cases have the post condition = C4_factdump, which is exactly the disconfirmation reference. The verdicts are computed by comparing C4 against itself; "facts_already_activate" is the tautological output. The all-jumps row above is contaminated by these degenerate cases; the fair-jumps column is the cleaner number.

### INFERENCE_CHAIN check via spec-unique token share -- jumps vs controls

Hypothesis tested: if the post-response is mostly composed of tokens that overlap with the question (not the spec), the inference is not grounded in spec content. If spec-unique tokens contribute substantially to the post, the spec is doing inferential lift.

| Verdict | Jumps n | Jumps % | Controls n | Controls % |
| --- | ---: | ---: | ---: | ---: |
| genuine_inference_via_spec | 11 | 100.0% | 2 | 100.0% |
| mixed_inference | 0 | 0.0% | 0 | 0.0% |
| inference_not_grounded_in_spec | 0 | 0.0% | 0 | 0.0% |
| unclear | 0 | 0.0% | 0 | 0.0% |

### N-gram overlap thresholds

Stream X used a 6-gram threshold for DIRECT_QUOTE_MATCH and reported 0 cases. Re-checking at 4-gram and 3-gram thresholds:

| Pair | 6-gram any | 4-gram any | 3-gram any |
| --- | ---: | ---: | ---: |
| (spec, held_out) | 0 | 0 | 4 |
| (held_out, post) | 1 | 2 | 9 |

A high held_out -> post n-gram count without a corresponding spec -> held_out count would indicate quote leakage from somewhere other than the spec (the question text, model pretraining footprint, or training-data contamination).

## Validity assessment

- **Mechanism distribution alone is not a discriminator.** PATTERN_PREDICATE+HYBRID = 78.3% on jumps and 94.7% on controls. The heuristic detects "spec was loaded," not "spec drove a band jump." This is the central caveat against any naive reading of the mechanism table.
- **Fair-comparison disconfirmation is the discriminator.** spec_doing_work on fair jumps (post = spec-loaded; n=38): 78.9%. On controls (n=36): 80.6%. Delta -1.7 pp. If this delta is small, pattern activation is present in both populations and cannot explain the lift. If it is large, the spec adds pattern content uniquely on jump items.
- **Confound: spec length.** Globals served spec is roughly 3x longer than Hamerton brief. Token-overlap heuristic naturally over-counts PATTERN_PREDICATE matches on longer specs. Treat per-subject normalized rates as more reliable than raw counts.
- **N-gram leakage check.** Spec-held: 0 6-gram, 0 4-gram, 4 3-gram matches. Held-post: 1 6-gram, 2 4-gram, 9 3-gram matches. Direct quote leakage from spec to held-out is essentially zero; from held-out to post is also low at 4-gram. The lift is not coming from quote-matching.
- **Most load-bearing evidence:** the spec_doing_work delta between jumps and controls. A flat or inverted delta refutes the claim that pattern activation is the unique mechanism driving lift. A large positive delta supports it.

## Caveats

- Heuristic classification only. No LLM is in the loop. Token overlap above stopword filtering is a proxy for "spec sentence X drove this response," not a proof. Borderline cases (low confidence) marked in the classification table.
- Hamerton served spec is brief-only (1918 words). Globals served spec is the full anchor+core+predictions+brief stack (~5775 words). Token-overlap heuristics naturally surface more candidate spec sentences for globals; the absolute PATTERN_PREDICATE counts are biased toward longer specs. Treat the per-subject normalized rate as more reliable than raw counts.
- Disconfirmation tests are themselves heuristics. The "facts_already_activate" verdict requires the C4 response to share at least as many content tokens with the best spec sentence as the C4a response does. This is a token-level signal, not a semantic one.
- Control group is bounded by axis-availability: REFUSAL_TRIGGERING and INTERPRETIVE_INFERENCE controls may be undersampled relative to LITERAL_RECALL because non-jumping questions of those types are scarcer.


## Cross-reference for framing report

The implications of this analysis for the Round 1 framing report are documented in `docs/reviews/framing_report_round1_update_20260428.md`. That update file synthesizes the headline finding (heuristic-level pattern-activation claim falsified; fair-comparison delta -1.7 pp), the four Stream X errors caught by this deeper pass, and the revised recommendations for Pivots 6 and 7 in the framing report.

The framing-report agent should treat the update file as authoritative for any mechanism-related framing decisions. The update file changes Pivot 6 from "apply cautious predicate-mediated framing" to HOLD-FOR-PHASE-2C-RESULTS, and elevates rater confabulation from a hypothetical alternative to a demonstrated property of the token-overlap heuristic.
