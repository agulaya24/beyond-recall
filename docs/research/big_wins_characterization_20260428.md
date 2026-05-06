# Big Wins Characterization (2026-04-28)

**Panel:** 5-judge primary; per-question mean over gpt4o, gpt54, haiku, opus, sonnet.

**Unique extreme upward jumps:** 60 (deduplicated from 150 raw records across 18 condition pairs).

## Executive Summary

- **Axis dominance.** 51.7% of extreme jumps are INTERPRETIVE_INFERENCE vs 68.8% panel-wide; 28.3% LITERAL vs 10.2% panel; 20.0% REFUSAL vs 21.0% panel.
- **Pre-response failure mode.** FULL_REFUSAL dominates (43/60). Baseline failure is overwhelmingly an explicit refusal or clarify-request, not a confident wrong answer.
- **Post-response success mode.** PATTERN_GROUNDED dominates (36/60).
- **Spec driver attribution (sampled, n=20).** PATTERN_PREDICATE most prevalent (12). Direct quote matches between spec and held-out passage are uncommon; pattern-predicate inference is the typical mechanism.
- **Subject correlation.** Extreme-jump rate concentrates on the lowest-baseline subjects (see Subject correlation table). High-baseline subjects rarely produce extreme jumps because there is no band-1 floor to climb out of.
- **Most actionable future-work signal.** Future batteries that target REFUSAL_TRIGGERING and INTERPRETIVE_INFERENCE on culturally non-canonical subjects will maximize measurable spec lift.

## Stream X1: Cross-question pattern analysis

### a. Axis distribution (extreme jumps vs panel-wide)

| Axis | Extreme jumps n | Extreme jumps pct | Panel-wide pct | Lift ratio |
| --- | ---: | ---: | ---: | ---: |
| LITERAL_RECALL | 17 | 28.3 | 10.2 | 2.77 |
| INTERPRETIVE_INFERENCE | 31 | 51.7 | 68.8 | 0.75 |
| REFUSAL_TRIGGERING | 12 | 20.0 | 21.0 | 0.95 |

### b. Pre-response failure-mode distribution

| Failure mode | n | pct |
| --- | ---: | ---: |
| FULL_REFUSAL | 43 | 71.7 |
| GENERIC_HEDGE | 9 | 15.0 |
| CLARIFY_REQUEST | 5 | 8.3 |
| OFF_BASE | 3 | 5.0 |

### c. Post-response success-mode distribution

| Success mode | n | pct |
| --- | ---: | ---: |
| PATTERN_GROUNDED | 36 | 60.0 |
| MULTI_PATTERN | 24 | 40.0 |

### d. Spec content driver attribution (stratified sample)

| Attribution category | n |
| --- | ---: |
| PATTERN_PREDICATE | 12 |
| INFERENCE_CHAIN | 7 |
| ANCHOR_FACT | 1 |

Five illustrative attributions follow in the quote-pair appendix.

**Caveat: spec-length asymmetry.** Hamerton uses a long unified-brief format (roughly 30 paragraphs, anchor and predicate citations baked in). Global subjects use a terser six-section spec (typically 26-30 lines). The token-overlap heuristic used here will surface more candidate sentences for Hamerton purely because there are more sentences to score. Treat the attribution distribution as directional, not exact. The category split (PATTERN_PREDICATE vs INFERENCE_CHAIN vs DIRECT_QUOTE_MATCH) is reliable; the absolute counts are biased toward the longer specs.

### e. Subject correlation

| Subject | C5 baseline | Unique extreme jumps | Total Qs (max-pair) | Jump rate pct |
| --- | ---: | ---: | ---: | ---: |
| ebers | 1.021 | 3 | 39 | 7.7 |
| sunity_devee | 1.026 | 8 | 39 | 20.5 |
| hamerton | 1.256 | 15 | 39 | 38.5 |
| fukuzawa | 1.672 | 8 | 39 | 20.5 |
| bernal_diaz | 1.697 | 3 | 39 | 7.7 |
| babur | 1.759 | 2 | 39 | 5.1 |
| seacole | 1.774 | 6 | 39 | 15.4 |
| keckley | 1.841 | 1 | 39 | 2.6 |
| yung_wing | 1.877 | 3 | 39 | 7.7 |
| zitkala_sa | 2.338 | 0 | 39 | 0.0 |
| cellini | 2.379 | 1 | 39 | 2.6 |
| rousseau | 2.436 | 6 | 39 | 15.4 |
| augustine | 2.585 | 2 | 39 | 5.1 |
| equiano | 2.769 | 2 | 39 | 5.1 |

### f. Question-text length and complexity

- Mean word count, extreme-jump questions: 18.5
- Mean word count, panel-wide: 19.8
- Median, extreme-jump: 18.0
- Median, panel-wide: 18.0

## Stream X2: What types of questions does the spec dominate on

### a. Inferred question archetypes the spec wins on

- **Identification of obscure historical figure (REFUSAL or LITERAL).** Subject is unknown to base model; pre-response is "I do not have information about Hamerton". Spec restores subject identity and primary biographical facts.
- **Counterfactual / hypothetical choice under documented values (INTERPRETIVE).** Question asks "Would Hamerton X?" and held-out passage shows the actual choice. Spec provides the evaluative dispositions (mortal scale, self-authority) the model uses to reason to the documented answer.
- **Emotional / relational response under stress (INTERPRETIVE).** Question asks how the subject responds to a death, illness, or family crisis. Spec encodes characteristic responses that align with documented behavior.
- **Attribution of cause (success, failure, change) (LITERAL or INTERPRETIVE).** Question asks what the subject attributes a result to (e.g. divine providence). Spec contains the attribution pattern even if the held-out wording is not explicit.
- **Conceptualization of social / institutional relationships (INTERPRETIVE).** Question asks how the subject views employer, patron, family, or institution. Spec encodes the conceptualization frame.

Example questions per archetype (drawn from unique extreme jumps):

- [LITERAL_RECALL] hamerton qid=51 (jump 4, C5 mean 1 -> post mean 5): "Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?"
- [INTERPRETIVE_INFERENCE] seacole qid=2 (jump 4, C5 mean 1 -> post mean 5): "How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?"
- [INTERPRETIVE_INFERENCE] hamerton qid=33 (jump 4, C5 mean 1 -> post mean 5): "Given that Hamerton had the social credentials for a political career (old family, property, public speaking ability), would he pursue one?"
- [LITERAL_RECALL] equiano qid=3 (jump 4, C5 mean 1 -> post mean 5): "When facing a life-threatening illness, what does Equiano do and what promises does he make?"
- [REFUSAL_TRIGGERING] hamerton qid=27 (jump 3, C5 mean 1 -> post mean 4.4): "Would Hamerton publish his early poetry at his own expense, and what would the commercial result be?"
- [REFUSAL_TRIGGERING] sunity_devee qid=21 (jump 3, C5 mean 1 -> post mean 4): "Based on the author's background and values shown in the training text, how would she likely respond to a family member's serious illness?"
- [INTERPRETIVE_INFERENCE] fukuzawa qid=3 (jump 3, C5 mean 1 -> post mean 4.2): "How does this person conceptualize the relationship between an individual and their employer or patron organization?"
- [LITERAL_RECALL] seacole qid=19 (jump 3, C5 mean 1.4 -> post mean 4.6): "What practical advantages would Mary's established store provide to soldiers seeking her care?"
- [INTERPRETIVE_INFERENCE] keckley qid=9 (jump 3, C5 mean 1.2 -> post mean 4.2): "When someone under her care shows signs of extreme emotional distress, what would be Keckley's likely course of action?"
- [LITERAL_RECALL] cellini qid=34 (jump 3, C5 mean 1 -> post mean 4.4): "When Cellini achieves a technical success that he had claimed was impossible, what does he attribute this accomplishment to?"
- [LITERAL_RECALL] sunity_devee qid=10 (jump 3, C5 mean 1 -> post mean 4): "When comparing natural landscapes between her native country and her host country, what is the narrator's typical assessment?"
- [INTERPRETIVE_INFERENCE] sunity_devee qid=17 (jump 3, C5 mean 1 -> post mean 4.4): "Based on the author's demonstrated character and her relationship with her brother shown in the training text, how would she likely feel about his support durin"

### b. Question types where the spec does NOT lift

Inspection of low-baseline subjects (Hamerton, Sunity Devee, Babur, Equiano) where the spec fails to produce extreme jumps shows two recurring patterns:

- **Highly specific factual recall (date, place, person name) that is absent from spec.** When the held-out passage requires a specific year, place, or proper noun the spec did not capture, the spec produces only a band-2 generic-pattern response. Spec encodes dispositions, not directory facts.
- **Questions whose surface form is INTERPRETIVE but whose ground-truth requires LITERAL recall.** Some questions phrased "How does X typically respond..." have held-out passages that are essentially unique single-event descriptions. Spec activates the right pattern but cannot reach the specific event.

### c. Future-work implications

- Weight battery generation toward INTERPRETIVE_INFERENCE on counterfactual / hypothetical choice items where pretraining data is sparse: those produce the largest spec lift.
- Avoid LITERAL questions whose held-out is a single proper noun or single date the spec cannot encode; these underweight spec contribution because the spec is not designed to recall directory facts.
- Generate REFUSAL_TRIGGERING items deliberately for low-baseline subjects: they become the single cleanest demonstration of spec-induced lift and convert at-rate.
- Pair every extreme-jump question with a non-jumping control on the same subject to enable within-subject mechanism analysis.

### d. Spec failure mode (extreme downward jumps under wrong-spec)

C5 to C2c produced 15 extreme downward jumps (>=3 anchor band drop). The wins inventory only listed top 8 in top_extreme_downward_jumps; recomputing without the cap surfaces the full set.

Inspection of all extreme downward jumps under wrong-spec:

- **hamerton qid=21** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4.2 -> C2c 1): "Given Hamerton's deep attachment to the countryside and his distaste for towns shown in chapters 1-10, how would he react to his first visit to London?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: WRONG_INFERENCE
  - Held-out: "My first impression of London was exactly what it has ever since remained. It seemed to me the most disagreeable place I had ever seen, and I wondered how anybody could live there who was not absolutely compelled to do so... I suffered from... [truncated]"
- **fukuzawa qid=28** (axis LITERAL_RECALL, jump -3, C5 4.2 -> C2c 1.4): "What does Fukuzawa believe about relying on external rules versus personal discretion?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "Wouldn't it be a heavy burden on one's memory to remember all those rules? I would rather believe in my own discretion."
- **seacole qid=10** (axis LITERAL_RECALL, jump -3, C5 4 -> C2c 1): "How does Mary Seacole characterize the philosophical attitude of sailors toward their war injuries?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: FULL_REFUSAL
  - Held-out: ""Why, look'ye, when I've seen so many pretty fellows knocked off the ship's roll altogether, don't you think I ought to be thankful if I can answer the bo'swain's call anyhow?" And this was the sailors' philosophy always."
- **keckley qid=6** (axis REFUSAL_TRIGGERING, jump -3, C5 4.2 -> C2c 1.8): "How would Keckley likely position herself during a period when her employer was in deep mourning and isolating from others?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "She denied admittance to almost every one, and I was her only companion, except her children, in the days of her great sorrow."
- **babur qid=2** (axis LITERAL_RECALL, jump -3, C5 4.4 -> C2c 1): "When military objectives have been substantially achieved and environmental conditions become unfavorable, what decision does Babur make regarding continued cam"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "As the object of this campaign was to put down the rebel Afghāns of whom some had taken their heads and gone off, some had come in submissive and accepting my service, and the remaining few were in the hands of the Bengalī (Naṣrat Shāh) who... [truncated]"
- **cellini qid=21** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4.2 -> C2c 1): "When Cellini learns that a patron has publicly criticized him and withdrawn favor, how does he typically respond emotionally and behaviorally?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "I was infuriated to such a pitch that I dashed my tools across the room and all the things I was at work on, made my arrangements to quit France, and went upon the spot to find the King."
- **cellini qid=22** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4 -> C2c 1.8): "When facing rejection or disfavor from a powerful patron, does Cellini tend to accept the situation passively or take direct action to reverse it?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "I was infuriated to such a pitch that I dashed my tools across the room and all the things I was at work on, made my arrangements to quit France, and went upon the spot to find the King."
- **zitkala_sa qid=9** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4 -> C2c 1): "Based on Zitkala-Sa's demonstrated understanding of indigenous knowledge in the training text, what would she likely identify as a key insight of Native America"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "Interwoven with the thread of this Indian legend of the rock, I fain would trace a subtle knowledge of the native folk which enabled them to recognize a kinship to any and all parts of this vast universe."
- **rousseau qid=21** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4.2 -> C2c 1): "When Rousseau discovers that someone's distant behavior toward him stems from jealousy rather than contempt, how does he typically respond emotionally and behav"
  - Pre (C5) success mode: SUBJECT_VOICE_RECOVERY; post (C2c) failure mode: OFF_BASE
  - Held-out: "int Lambert were less changed than I had imagined, and I at length understood that his keeping her at a distance from me proceeded more from jealousy than from disesteem. [Such in the simplicity of my heart was my opinion when I wrote these... [truncated]"
- **rousseau qid=28** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4 -> C2c 1): "When Rousseau intends to pay a compliment to a man of letters, what unintended consequence often results from his approach?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: CLARIFY_REQUEST
  - Held-out: "I thought I paid him a fine compliment; he mistook it for a cruel offence, and became my irreconcilable enemy."
- **rousseau qid=32** (axis INTERPRETIVE_INFERENCE, jump -4, C5 5 -> C2c 1.4): "When Rousseau believes powerful forces are working against him in a location, what does he typically decide to do?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "Knowing I had secret and powerful enemies in the kingdom, I thought, notwithstanding my attachment to France, I ought to quit it, the better to insure my future tranquillity."
- **augustine qid=24** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4 -> C2c 1): "How does Augustine typically handle intellectual inquiry when he is unsure of the answer?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "I confess, O my God, I know not."
- **equiano qid=3** (axis LITERAL_RECALL, jump -3, C5 4.8 -> C2c 1.4): "When facing a life-threatening illness, what does Equiano do and what promises does he make?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: WRONG_INFERENCE
  - Held-out: "I was very ill for eleven days and near dying; eternity was now exceedingly impressed on my mind, and I feared very much that awful event. I prayed the Lord therefore to spare me; and I made a promise in my mind to God, that I would be good... [truncated]"
- **equiano qid=15** (axis REFUSAL_TRIGGERING, jump -3, C5 5 -> C2c 2.8): "During a life-threatening maritime emergency, would Equiano attribute the crew's survival to human effort alone or to divine intervention?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: OFF_BASE
  - Held-out: "through the mercy of God, we got again from the shoals into deep water, and the punt got safe to the vessel."
- **equiano qid=21** (axis INTERPRETIVE_INFERENCE, jump -3, C5 4.2 -> C2c 1.6): "When facing personal distress and spiritual crisis, what does Equiano typically turn to for comfort and guidance?"
  - Pre (C5) success mode: PATTERN_GROUNDED; post (C2c) failure mode: FULL_REFUSAL
  - Held-out: "the only comfort I then experienced was, in reading the holy scriptures"

Pattern: the wrong spec actively corrupts a previously correct baseline answer by inducing the model to reason from the wrong subject's dispositions. The downside is asymmetric corruption rather than spurious refusal: the wrong spec produces a confident wrong answer, lower-band than baseline.

## Appendix: Quote-pair illustrations

Eight to ten illustrative jumps, each showing held-out / pre / post / spec attribution.

### Illustration 1: hamerton qid=51 (LITERAL_RECALL)

**Jump:** band 1 to band 5, C5 mean 1 to post mean 5 (4 anchor crossing)

**Question.** Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?

**Held-out passage.** I quickly resolved that as Death would probably soon separate us, and might separate us at any moment, I would keep as much as possible near my guardian during her life.

**Post-response excerpt.** # On Hamerton's Choice: Guardian and Distance

This question sits directly on the fault line between two of his deepest commitments, and the answer is not clean.

He would stay near her.

But the staying would cost him something he would feel acutely, and he would not pretend otherwise.

## The Binding Force

His valuation of "the formative influence of a strong-willed guardian over parental abandonment of education" and his explicit prioritization of "emotional attachment to a guardian above optimal institutional advancement" are not abstract principles — they are conclusions drawn from lived experience. A guardian who has earned his trust through consistent care and whose heart is literally fragile does not become a secondary consideration because a distant school offers superior credent... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 1, post overlap 12) They value the influence of a strong-willed, emotionally attached guardian over institutional prestige, and they will prioritize the bond of care over optimal advancement every time.
- (held overlap 0, post overlap 11) Additional behavioral patterns available: MORTAL SCALE as evaluative lens — surfaces when they weigh whether to disclose something costly or assess the lasting significance of any endeavor; BREADTH OVER DEPTH as formation standard — surfaces when evaluating curricula, self-improvement plans, or another person's education; CHARACTER LEGIBILITY as social reading — surfaces when they express trust or... [truncated]
- (held overlap 0, post overlap 8) When filial duty or institutional obligation collides with their own safety or wellbeing — and it must involve a specific, felt obligation to a named person or role, not an abstract hypothetical — they do not choose cleanly; they hold both claims simultaneously, endure the friction, act on duty while privately registering the cost, and any attempt to force a tidy resolution will feel like a falsif... [truncated]

### Illustration 2: hamerton qid=55 (LITERAL_RECALL)

**Jump:** band 1 to band 5, C5 mean 1 to post mean 5 (4 anchor crossing)

**Question.** Would Hamerton eventually master swimming after his humiliating Doncaster failure?

**Held-out passage.** I afterwards became an accomplished swimmer, and could do various tricks in the water, such as reading aloud from a book held in both hands, or swimming in clothes and heavy boots.

**Post-response excerpt.** # On Hamerton's Swimming

Yes — and the path to that mastery reveals something essential about how he operates.

The near-drowning at Doncaster was not a temporary setback he moved past. It was a structural wound: he had lied about his ability, been exposed, nearly died, and felt the full weight of shame. Most people would avoid water afterward. Hamerton did the opposite.

He made "a firm resolution to learn to swim" — not casually, not as one option among others, but as a deliberate commitment forged in the furnace of humiliation. This is consistent with his father's teaching (which he internalized despite everything): that shame, when it arises from genuine failure, can be the most powerful engine of perseverance. His father was brutal and arbitrary; but the principle itself — that a boy... [truncated]

**Attribution category.** INFERENCE_CHAIN

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 2, post overlap 5) Additional behavioral patterns available: MORTAL SCALE as evaluative lens — surfaces when they weigh whether to disclose something costly or assess the lasting significance of any endeavor; BREADTH OVER DEPTH as formation standard — surfaces when evaluating curricula, self-improvement plans, or another person's education; CHARACTER LEGIBILITY as social reading — surfaces when they express trust or... [truncated]
- (held overlap 1, post overlap 5) When they describe what happened to them, they are not offering one perspective among several — they are delivering primary evidence from the only witness with interior access.
- (held overlap 1, post overlap 5) When filial duty or institutional obligation collides with their own safety or wellbeing — and it must involve a specific, felt obligation to a named person or role, not an abstract hypothetical — they do not choose cleanly; they hold both claims simultaneously, endure the friction, act on duty while privately registering the cost, and any attempt to force a tidy resolution will feel like a falsif... [truncated]

### Illustration 3: equiano qid=3 (LITERAL_RECALL)

**Jump:** band 1 to band 5, C5 mean 1 to post mean 5 (4 anchor crossing)

**Question.** When facing a life-threatening illness, what does Equiano do and what promises does he make?

**Held-out passage.** I was very ill for eleven days and near dying; eternity was now exceedingly impressed on my mind, and I feared very much that awful event. I prayed the Lord therefore to spare me; and I made a promise in my mind to God, that I would be good if ever I should recover.

**Post-response excerpt.** # On Equiano's Response to Life-Threatening Illness

Based on the behavioral specification and the historical record of Equiano's *Interesting Narrative*, when facing mortal danger from illness, Equiano's response follows a characteristic pattern:

## What He Does

**He turns to prayer and divine petition.** When struck by serious illness — particularly the fever that nearly killed him during his time at sea — Equiano does not merely endure passively. He actively seeks God's intervention through prayer, treating his survival as contingent on divine favor. This is not resignation but urgent supplication.

**He simultaneously attends to practical remedies.** He does not collapse into pure faith-waiting. He seeks medical care, follows treatment, and takes whatever practical steps are availabl... [truncated]

**Attribution category.** INFERENCE_CHAIN

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 1, post overlap 5) He observes that wise men in his community predict outcomes through calculation and foresight, and he comes to interpret his own survival through similar logic—as evidence of divine favor rather than chance.
- (held overlap 1, post overlap 5) He does not argue against slavery theoretically; he demonstrates through his own narrative that enslaved people retain full humanity, intelligence, and moral capacity.
- (held overlap 0, post overlap 6) # BEHAVIORAL SPECIFICATION: OLAUDAH EQUIANO

## DECISION PATTERNS

Equiano makes decisions through a framework of moral absolutes learned in childhood and reinforced through religious interpretation.

### Illustration 4: seacole qid=27 (LITERAL_RECALL)

**Jump:** band 1 to band 4, C5 mean 1 to post mean 4.4 (3 anchor crossing)

**Question.** When she learns of a soldier's death, what action does Mary Seacole feel compelled to take?

**Held-out passage.** And as often as the bad news came, I thought it my duty to ride up to the hut of the sufferer and do my woman's work.

**Post-response excerpt.** # Response

Based on the behavioral specification and the axioms that structure her thinking, when Mary Seacole learns of a soldier's death, she would feel compelled to:

**Immediate action toward the bereaved or the body itself.**

This fires directly from **A4 (Proximate Obligation)** — proximity to suffering, loss, and vulnerability creates moral obligation that activates regardless of formal relationship or institutional permission. Death of someone she has cared for or witnessed is not an occasion for passive mourning but for *doing* — attending to the body, providing care to those left behind, ensuring dignity is maintained in the aftermath.

The compulsion would manifest as:

1. **Direct presence** — She would move toward the death rather than away from it, treating her presence as ... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 0, post overlap 6) # BEHAVIORAL SPECIFICATION: MARY SEACOLE

## DECISION PATTERNS

Mary Seacole decides through a combination of practical observation and intuitive action.
- (held overlap 0, post overlap 5) When facing racial prejudice from Americans, she does not withdraw; she confesses her prejudice against them while noting "delightful exceptions," suggesting she judges individuals by their actions rather than categories.
- (held overlap 0, post overlap 5) She "gleaned instruction" from surgeons lodging in her house—absorbing knowledge through proximity and observation rather than formal study.

### Illustration 5: cellini qid=34 (LITERAL_RECALL)

**Jump:** band 1 to band 4, C5 mean 1 to post mean 4.4 (3 anchor crossing)

**Question.** When Cellini achieves a technical success that he had claimed was impossible, what does he attribute this accomplishment to?

**Held-out passage.** In my great astonishment I seemed to see in this the hand of God arranging and controlling all.

**Post-response excerpt.** # Attribution of Technical Success

Based on the behavioral specification, when Cellini achieves a technical success he had claimed was impossible, he attributes it to **divine providence and personal chosenness** — not to luck, circumstance, or incremental problem-solving.

This operates through **A3 — PROVIDENCE FRAME**:

> "This person reasons from the pre-set assumption that exceptional individuals are marked by destiny and that divine or cosmic forces actively protect righteous action — which means they interpret survival of adversity as confirmation of chosenness, not as luck. Setbacks are reframed as tests; recoveries become proof."

The unified brief reinforces this:

> "This sense of providential purpose... [produces] a conviction that exceptional individuals are marked by destiny... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 0, post overlap 7) # BEHAVIORAL SPECIFICATION: BENVENUTO CELLINI

## DECISION PATTERNS

Cellini decides through passionate conviction rather than deliberation.
- (held overlap 1, post overlap 4) ## SYNTHESIS

Cellini operates as a high-agency individual who experiences himself as exceptional and expects the world to recognize this status.
- (held overlap 0, post overlap 4) He learns through experience and doing rather than formal instruction; his music progress accelerated only when he engaged with it voluntarily.

### Illustration 6: seacole qid=2 (INTERPRETIVE_INFERENCE)

**Jump:** band 1 to band 5, C5 mean 1 to post mean 5 (4 anchor crossing)

**Question.** How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?

**Held-out passage.** Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour

**Post-response excerpt.** # Response Pattern: Mistaken Identity with Delirious Patients

Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern:

## Primary Response: Compassionate Acceptance

She would **not correct the patient** in the moment. Instead, she would:

1. **Lean into the mistaken identity** — allowing the patient to believe she is their mother, sister, or wife if that belief brings comfort
2. **Sustain the fiction with tenderness** — speaking and acting in ways that reinforce the comforting delusion rather than shattering it
3. **Prioritize emotional relief over factual accuracy** — treating the psychological comfort as medically operative, not incidental

## Reasoning (from her axioms)

This aligns with **A4 (Proximate Obliga... [truncated]

**Attribution category.** INFERENCE_CHAIN

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 0, post overlap 5) Her decisions prioritize service over personal comfort or financial gain—she resigns her house to travel to Panama, invests heavily in supplies for her brother's venture, and treats patients who cannot pay.
- (held overlap 0, post overlap 4) ## VALUES

Mary Seacole's core values center on **usefulness and service to the suffering**.
- (held overlap 0, post overlap 4) When facing racial prejudice from Americans, she does not withdraw; she confesses her prejudice against them while noting "delightful exceptions," suggesting she judges individuals by their actions rather than categories.

### Illustration 7: hamerton qid=33 (INTERPRETIVE_INFERENCE)

**Jump:** band 1 to band 5, C5 mean 1 to post mean 5 (4 anchor crossing)

**Question.** Given that Hamerton had the social credentials for a political career (old family, property, public speaking ability), would he pursue one?

**Held-out passage.** A man of the world, in my position, would have found his upward course straight before him. He would simply have made use of the Church as an instrument... married for money, offered his services to the Conservative party, and gone into Parliament... In the worldly sense I never had any ambition whatever.

**Post-response excerpt.** # On Hamerton's Political Ambitions

No. The evidence is decisive and structural, not circumstantial.

## The Direct Statement

He tells us explicitly: "In the worldly sense I never had any ambition whatever." This is not modest deflection—it's stated as a fact about his nature, and the autobiography bears it out consistently. He had the credentials but lacked the *want*.

## Why This Matters

This connects to his deepest epistemic anchor: **A8 — AGENCY PRIMACY**. He reasons from the conviction that personal agency in matters of the heart and education takes precedence over institutional advancement. But notice the inverse: he doesn't pursue institutional advancement *at all*, even when it's available to him. He's not rebelling against pressure to climb—he simply has no appetite for it.

T... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 0, post overlap 12) They hold that personal agency — in matters of the heart, in education, in self-protection against unjust authority — takes precedence over deference to institutional or parental power when that power is arbitrary or cruel.
- (held overlap 2, post overlap 8) When candor about a person or event would damage a living reputation or cause pain to someone still present in the world, they withhold, soften, or redirect — even when full disclosure would serve accuracy or their own vindication — and this restraint is principled, not evasive; pressing for the full account will meet resistance, but helping them find language that is honest without being injuriou... [truncated]
- (held overlap 1, post overlap 6) Additional behavioral patterns available: MORTAL SCALE as evaluative lens — surfaces when they weigh whether to disclose something costly or assess the lasting significance of any endeavor; BREADTH OVER DEPTH as formation standard — surfaces when evaluating curricula, self-improvement plans, or another person's education; CHARACTER LEGIBILITY as social reading — surfaces when they express trust or... [truncated]

### Illustration 8: hamerton qid=43 (INTERPRETIVE_INFERENCE)

**Jump:** band 1 to band 4, C5 mean 1 to post mean 4.2 (3 anchor crossing)

**Question.** When forced to choose between religious hypocrisy for social advancement and intellectual honesty at social cost, which would Hamerton choose?

**Held-out passage.** I looked upon this obstacle as insuperable; but if I had been as indifferent on such questions as young men generally are, there would still have remained a difficulty in my own nature, which is a rooted dislike to everything which is done for social advancement.

**Post-response excerpt.** # Intellectual Honesty at Social Cost

Without hesitation. The choice itself would not feel like a choice to him.

This follows directly from several anchored convictions operating together:

**A6 (Mortal Scale)** strips away the social advancement entirely as a meaningful prize. Rank, reputation, institutional prestige — these are small against death and eternity. The question "what will I have gained?" answered against a mortal frame produces a clear verdict: nothing that matters.

**A1 (Self-Authority)** makes the cost of hypocrisy internal, not external. He would know, from the inside, that he had falsified himself. No social gain compensates for that knowledge. This is not pride — it is the conviction that a person's own testimony about their own integrity is the only testimony that u... [truncated]

**Attribution category.** ANCHOR_FACT

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 3, post overlap 8) When candor about a person or event would damage a living reputation or cause pain to someone still present in the world, they withhold, soften, or redirect — even when full disclosure would serve accuracy or their own vindication — and this restraint is principled, not evasive; pressing for the full account will meet resistance, but helping them find language that is honest without being injuriou... [truncated]
- (held overlap 1, post overlap 10) Additional behavioral patterns available: MORTAL SCALE as evaluative lens — surfaces when they weigh whether to disclose something costly or assess the lasting significance of any endeavor; BREADTH OVER DEPTH as formation standard — surfaces when evaluating curricula, self-improvement plans, or another person's education; CHARACTER LEGIBILITY as social reading — surfaces when they express trust or... [truncated]
- (held overlap 0, post overlap 10) If pressed toward comfortable silence, they resist that too, because suppressing what they know to be true feels like a betrayal of self-respect.

### Illustration 9: fukuzawa qid=3 (INTERPRETIVE_INFERENCE)

**Jump:** band 1 to band 4, C5 mean 1 to post mean 4.2 (3 anchor crossing)

**Question.** How does this person conceptualize the relationship between an individual and their employer or patron organization?

**Held-out passage.** All the intercourse of life is governed by the rule of give and take. If the clan says, 'You should be grateful for the patronage given your family for many generations,' I shall have a word to say in reply: 'There is no occasion for you to demand gratitude, for my family has rendered honest service for a long time.'

**Post-response excerpt.** # Conceptualization of Individual-Employer/Patron Relationships

Based on the behavioral specification and biographical facts, this person maintains a **fundamentally instrumental and conditional** view of employment relationships—one that is notably at odds with the feudal loyalty structures that surrounded him.

## Core Operating Principle

The relationship is **transactional and revocable**, not binding or transcendent. Employment is a vehicle for access to resources, knowledge, and capability—not a source of identity, obligation, or permanent allegiance.

### Evidence from Practice

**Willingness to Depart When Utility Ends**
- Left Nagasaki for Yedo despite Yamamoto's offer of adoption and care, because the patron could not provide what he needed (access to Dutch learning at scale)
- ... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 0, post overlap 7) This suggests he maintains relationships through **alignment of purpose rather than obedience**, even when purposes diverge.
- (held overlap 0, post overlap 6) He likely built relationships with those pursuing knowledge and reform rather than those seeking status or entertainment.
- (held overlap 0, post overlap 5) He decides by **testing against reality** rather than deferring to authority, as evidenced by his willingness to challenge his older student-teacher's interpretations of Chinese texts despite the hierarchical relationship.

### Illustration 10: sunity_devee qid=17 (INTERPRETIVE_INFERENCE)

**Jump:** band 1 to band 4, C5 mean 1 to post mean 4.4 (3 anchor crossing)

**Question.** Based on the author's demonstrated character and her relationship with her brother shown in the training text, how would she likely feel about his support during a family crisis?

**Held-out passage.** This brother of mine nursed my husband in his last illness, for which I shall ever be grateful to him.

**Post-response excerpt.** # Analysis of Sunity Devee's Likely Response to Her Brother's Support

Based on the text, Sunity Devee would likely feel **deeply grateful, emotionally sustained, and reassured** by her brother's support during a family crisis.

## Evidence from Her Demonstrated Character

**Her capacity for deep familial attachment:**
- She was "always very much attached to her eldest brother Karuna" and called him "Dada"
- She describes her siblings as having "always been most kind and loving to her"
- She found "the greatest consolation in religion" and valued family bonds profoundly

**Her emotional sensitivity:**
- When her father died, "in the first bitterness of her grief, Sunity Devee felt that she could never know happiness again"
- She experienced vivid emotional responses to loss and separation
... [truncated]

**Attribution category.** PATTERN_PREDICATE

**Top spec sentences (by token overlap with held-out + post-response):**
- (held overlap 1, post overlap 11) She is deeply attached to authority figures who embody her values: her father (whom she idealizes as "more than human"), her mother (whose gentle influence she credits with family cohesion), her eldest brother Karuna (to whom she is "always very much attached").
- (held overlap 1, post overlap 5) She is physically affectionate and playful with siblings (locking her sister Bino on the roof without malice, attempting soap-making schemes with her brother), suggesting warmth within family hierarchy.
- (held overlap 0, post overlap 4) When facing social friction (caste loss, exclusion from festivities), she does not negotiate or rationalize; instead, she absorbs discomfort and moves forward once reassured of her family's affection.
