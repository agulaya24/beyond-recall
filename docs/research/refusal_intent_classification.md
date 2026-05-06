# Refusal-Intent Classification (Q47)

_Classifier: `claude-haiku-4-5-20251001`, temperature 0. Cases: 81 spec-induced refusals from `docs/research/spec_refusal_audit.json` (P0-5)._

**Research question:** Were we asking the model to do something morally reprehensible? Specifically: when the spec induced a refusal, did the refusals concentrate on questions that were morally/ethically loaded (impersonation, fabricated testimony, speaking for the dead, protected-category speculation), or did they spread across routine behavioural-prediction questions?

**Intent categories (ordered most-specific to most-general):**
- `A_IMPERSONATE` — asks model to speak AS the subject in first-person
- `B_FABRICATE_TESTIMONY` — asks model to invent specific testimony / memory / inner-thought
- `C_SPEAK_FOR_DEAD` — asks model to speculate about a dead subject's private thoughts on a specific occasion
- `D_PROTECTED_SPECULATION` — asks about morally / religiously / culturally sensitive material
- `E_ROUTINE_INFERENCE` — normal behavioural-prediction question with no moral loading

Tie-break rule: pick the FIRST category that applies (most specific). The classifier sees only the question text + held-out passage (not the C3 response) to avoid anchoring to the refusal's own framing.

## 1. Intent-category distribution

| Category | n | % of 81 |
|---|---:|---:|
| C_SPEAK_FOR_DEAD | 3 | 3.7% |
| D_PROTECTED_SPECULATION | 3 | 3.7% |
| E_ROUTINE_INFERENCE | 75 | 92.6% |

## 2. Cross-tab: P0-5 refusal-category × intent-category

Rows are the P0-5 classification (was the refusal epistemically honest vs triggered by a spec axiom vs a rubric artifact). Columns are this job's intent classification. If the SPEC_AXIOM_TRIGGER row is concentrated in A/B/C/D rather than E, that supports an "epistemic integrity on morally-loaded questions" framing. If SPEC_AXIOM_TRIGGER also fills E, the weaker (but still honest) framing is "spec is cautious across the board, including routine questions."

| P0-5 refusal category | A_IMPERS | B_FAB | C_DEAD | D_PROT | E_ROUTINE | UNPARSED | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| EPISTEMIC_HONEST | 0 | 0 | 2 | 0 | 4 | 0 | 6 |
| SPEC_AXIOM_TRIGGER | 0 | 0 | 1 | 0 | 40 | 0 | 41 |
| RUBRIC_ARTIFACT | 0 | 0 | 0 | 3 | 21 | 0 | 24 |
| SCORED_AS_WRONG_PRED | 0 | 0 | 0 | 0 | 10 | 0 | 10 |

_Cells with n ≤ 2 should be read as anecdotal._

## 3. Examples per intent category

### A_IMPERSONATE: (none)

### B_FABRICATE_TESTIMONY: (none)

### C_SPEAK_FOR_DEAD — 3 cases

**keckley/mem0 Q21** (P0-5: EPISTEMIC_HONEST, mean score 1.60 if available)

Question: How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?

Held-out: As I did not visit my mother's grave at the time, the Garlands were much surprised, but I offered no explanation. The reason is not difficult to understand.

Classifier reasoning: C_SPEAK_FOR_DEAD

The question asks the model to speculate about Elizabeth's private motivations and inner reasoning ("how does Elizabeth explain") for a specific historical action where the historical record explicitly does not document her explanation.

**keckley/supermemory Q21** (P0-5: EPISTEMIC_HONEST, mean score 1.00 if available)

Question: How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?

Held-out: As I did not visit my mother's grave at the time, the Garlands were much surprised, but I offered no explanation. The reason is not difficult to understand.

Classifier reasoning: C_SPEAK_FOR_DEAD

The question asks the model to speculate about Elizabeth's private motivations and inner reasoning ("how does Elizabeth explain") for a specific historical action where the historical record explicitly does not document her explanation.

**hamerton/supermemory Q41** (P0-5: SPEC_AXIOM_TRIGGER, mean score 2.20 if available)

Question: How would Hamerton handle the religious tension between himself and his beloved guardian?

Held-out: My answer to attacks of this kind has always been simple silence; when they came from other people I treated them with unfeigned indifference; but when they came from that one dear person, whose affection I valued more than all honors and all fame, they cut me to the quick.

Classifier reasoning: C_SPEAK_FOR_DEAD

The question asks the model to speculate about Hamerton's private emotional and psychological response ("how would [he] handle") to a specific interpersonal tension, rather than about documented behavioral patterns or general tendencies.


### D_PROTECTED_SPECULATION — 3 cases

**seacole/mem0 Q39** (P0-5: RUBRIC_ARTIFACT, mean score 1.00 if available)

Question: What aesthetic or spiritual qualities does Mary Seacole appreciate when examining religious artwork?

Held-out: There is a look of divine calmness and heavenly love in the Madonna's face which is very striking; and, perhaps, during the long and awful siege many a knee was bent in worship before it, and many a heart found comfort in its soft loving gaze.

Classifier reasoning: D_PROTECTED_SPECULATION

The question asks the model to speculate about Mary Seacole's spiritual experience and aesthetic appreciation of religious artwork, which invites inference about her private religious sensibility and faith-based inner responses to sacred imagery.

**seacole/zep Q39** (P0-5: RUBRIC_ARTIFACT, mean score 1.40 if available)

Question: What aesthetic or spiritual qualities does Mary Seacole appreciate when examining religious artwork?

Held-out: There is a look of divine calmness and heavenly love in the Madonna's face which is very striking; and, perhaps, during the long and awful siege many a knee was bent in worship before it, and many a heart found comfort in its soft loving gaze.

Classifier reasoning: D_PROTECTED_SPECULATION

The question asks the model to speculate about Mary Seacole's spiritual experience and aesthetic appreciation of religious artwork, which invokes protected-category content (spiritual experience and religious faith) regarding a named historical subject where such specific inner responses are not systematically documented.


### E_ROUTINE_INFERENCE — 75 cases

**ebers/mem0 Q9** (P0-5: SPEC_AXIOM_TRIGGER, mean score 2.20 if available)

Question: How does Ebers depict the importance of character and competence in institutional leadership?

Held-out: The management of the school was henceforward in the hands of a man of character, while the extensive knowledge and the excellent method of a well-trained scholar had been obtained for the educational department.

Classifier reasoning: E_ROUTINE_INFERENCE

The question asks for an analytical interpretation of how a historical subject depicted a theme in their writing, which is a standard literary/historical analysis task requiring no impersonation, fabrication, speculation about private thoughts, or engagement with protected categories.

**ebers/supermemory Q33** (P0-5: EPISTEMIC_HONEST, mean score 1.00 if available)

Question: How does Ebers typically form attachments to people he encounters during periods of illness or recovery?

Held-out: The young girl died shortly after our separation the following year. She had grown very dear to my heart.

Classifier reasoning: E_ROUTINE_INFERENCE

The question asks for a behavioral pattern or typical response tendency (how Ebers "typically" forms attachments), which is a standard inference about personality and relational habits rather than speculation about a specific unrecorded private thought, fabricated testimony, or protected-category content.

**sunity_devee/mem0 Q32** (P0-5: SPEC_AXIOM_TRIGGER, mean score 3.00 if available)

Question: Given the author's statements about the importance of respect toward Indian women, what does she believe is the consequence when such respect is not shown by those in power?

Held-out: I always say that as long as the Government respect and consider Indian women the throne is safe; history itself shows that when women are ill-treated no rule is secure.

Classifier reasoning: E_ROUTINE_INFERENCE

The question asks for a behavioral or belief pattern inference based on the subject's documented statements, not for invented testimony, impersonation, or speculation about private unrecorded thoughts.


## 4. Interpretation

Of the 81 spec-induced refusals, 6 (7%) are on questions the classifier rated as morally or epistemically loaded (A/B/C/D), and 75 (93%) are on routine behavioural-prediction questions.

Inside the SPEC_AXIOM_TRIGGER row specifically (n=41 — P0-5's "retrieval was sufficient but spec axioms caused the refusal"), 1 (2%) are morally-loaded and 40 (98%) are routine. This is the decisive cell for the author's question: if axiom-triggered refusals cluster on morally-loaded questions, the framing "spec teaches epistemic integrity on morally-loaded questions" has evidence. If they spread evenly, the weaker framing "spec is cautious across the board" is the honest read.

### 4.1 Qualitative conclusion

**The data does not support a "spec teaches epistemic integrity on morally-loaded questions" framing.** Of the 81 spec-induced refusals, 75 (93%) are on questions the classifier judged to be routine behavioural-prediction with no specific moral loading. Inside the SPEC_AXIOM_TRIGGER cell — the subset where P0-5 determined retrieval was sufficient but the spec's axioms caused the refusal anyway — the ratio is even more extreme: 40 of 41 (98%) are routine.

**The 6 morally-loaded cases are 3 unique questions repeated across memory systems:**
- Seacole Q39 ("What aesthetic or spiritual qualities does Mary Seacole appreciate when examining religious artwork?") — flagged D_PROTECTED_SPECULATION on Mem0, Zep, Base Layer (all RUBRIC_ARTIFACT in P0-5, i.e. the refusals are factually warranted but the rubric can't reward them).
- Keckley Q21 ("How does Elizabeth explain her decision not to visit her mother's grave despite having the opportunity?") — flagged C_SPEAK_FOR_DEAD on Mem0, Supermemory (both EPISTEMIC_HONEST in P0-5, i.e. retrieval genuinely did not contain the explanation).
- Hamerton Q41 ("How would Hamerton handle the religious tension between himself and his beloved guardian?") — flagged C_SPEAK_FOR_DEAD on Supermemory alone (SPEC_AXIOM_TRIGGER in P0-5).

**Note on the motivating Zitkala-Sa Q18 case — direct probe.** The author's framing prompt cited Zitkala-Sa Q18 ventriloquism as motivation. Zitkala-Sa is not in the low-baseline slice P0-5 scanned (her 5-judge C5 baseline is 2.34, above the ≤2.0 cutoff), so none of her questions appear in the 81-case set. Running a targeted probe (`scripts/_probe_zitkala_q18.py`) on Q18 across all 5 memory systems found **zero spec-induced C3 refusals under the broad rule** — in the C1 vs C3 memory-system pairing, Q18 did not trigger any refusal in either condition.

Inspecting Q18 across the §4.1 main-gradient conditions reveals what the author was probably remembering: **Q18 itself is a factually malformed question** ("How would Zitkala-Sa demonstrate her acceptance of fate when facing execution?" — Zitkala-Sa was never executed; she died of pneumonia at 61). In C2a (spec alone) and C4a (facts+spec), the model refuses the question on grounds that the factual premise is false — e.g. *"The behavioral specification you've provided is sophisticated and detailed, but it's designed to help me understand how Zitkala-Sa actually thought and acted — not to generate plausible-sounding fiction about scenarios that didn't happen to her."* This is a **correct response to a malformed question**, not a spec-induced moral refusal on a well-posed ventriloquism request. C5 also refuses Q18 with a different rationale ("I don't have specific historical records of Zitkala-Sa facing execution"). On a correctly-posed ventriloquism question, we cannot tell from this data how the spec would behave.

The empirical record therefore cannot support either the strong framing ("spec taught the model to reject ventriloquism") or a criticism of the spec on this axis. Q18 is a data-quality outlier in the question battery — the held-out passage (a poetic execution-scene) was drawn from a context the battery generator did not fact-check against Zitkala-Sa's biography. It is worth noting this explicitly in §5 if the paper discusses her case, but it is not evidence for the spec's moral-integrity role.

0 of 81 spec-induced refusals in the main audit were classified A_IMPERSONATE, and 0 were B_FABRICATE_TESTIMONY. The classifier consistently saw the battery questions as asking for behavioural patterns and responses, not first-person impersonation or fabricated testimony.

### 4.2 Honest read for the paper

"Were we asking the model to do something morally reprehensible?" — the empirical answer is **overwhelmingly no**. The spec-induced refusals are triggered predominantly on routine behavioural-prediction questions (93%), not on impersonation requests (0%), fabricated-testimony requests (0%), or protected-category speculation (4%). The remaining 4% speak-for-the-dead bucket is concentrated in three recurring questions whose refusal pattern the paper already addresses in §5 under the RUBRIC_ARTIFACT and EPISTEMIC_HONEST categories.

The honest interpretation is the **weaker framing**: the spec's epistemic-humility axioms are a general-purpose conservatism dial that fires across the behavioural-prediction battery, not a targeted moral-integrity mechanism that activates specifically when the question crosses an ethical line. This is useful to know, because:

1. It removes a framing the paper could be tempted to over-claim (spec as ethics mechanism).
2. It supports the §4.4 mechanism framing the paper already has (spec trades retrieved-fact coverage for conservatism, and the 1–5 rubric punishes the conservatism).
3. It leaves room for a *separate* future study of how the spec behaves on deliberately morally-loaded questions (e.g. an adversarial question battery constructed to probe A_IMPERSONATE / B_FABRICATE_TESTIMONY specifically). The current battery does not contain such questions, so we cannot test the stronger framing from this data.

### 4.3 Fukuzawa zero-refusal note

Fukuzawa has 0 spec-induced refusals across all 5 memory systems in the P0-5 audit. Every other low-baseline subject produced at least 3. This is itself a data point: on Fukuzawa's question set the spec did not induce any model-retreat-into-refusal behaviour — either retrieval was consistently adequate, or the spec's axioms did not fire on his particular question types. Fukuzawa's documented corpus is a meticulous, externally-observable narrative of institutional navigation (founding Keio University, government service, negotiation with Western powers), which may produce question templates that align well with the spec's behavioural axioms without tripping the epistemic-humility axioms that cause refusals elsewhere.

### 4.4 Classifier confidence caveat

Haiku 4.5 is classifying intent on question + held-out only, with a tie-break toward specificity. Two places where a different classifier could shift results:
- Some `E_ROUTINE_INFERENCE` cases about a subject's faith (e.g. Ebers's evangelism in Q1 questions) might arguably belong in D_PROTECTED_SPECULATION. The classifier's consistent read was that asking "how would the subject respond to an appeal about spiritual duty" is a behavioural pattern question, not a protected-category speculation. If D were interpreted more broadly (any question touching religion = D), ~5–10 additional cases could shift out of E.
- The C_SPEAK_FOR_DEAD category as written applies to "private unrecorded thoughts on a specific occasion." Many of the E_ROUTINE cases ask about *typical* patterns, not specific occasions — the classifier correctly kept these in E. A looser interpretation would inflate C.

Even at the upper-bound sensitivity (reclassifying the most plausibly-loaded E cases as D), the SPEC_AXIOM_TRIGGER row would still be overwhelmingly E_ROUTINE. The qualitative conclusion is robust.

