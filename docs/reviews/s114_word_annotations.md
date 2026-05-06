# S114 Word-based review annotations

Source: `docs\beyond_recall_v11_1_draft.docx`
Extracted: 47 annotations

---

## 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured. (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** Appendix H

**Comment:** Link

*Paragraph context:* Defined terms used throughout the paper are collected in Appendix H for reference.

---

## 1.2 What we tested (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** Letta

**Comment:** ^x – should include footnote for “additional testing on letta”

*Paragraph context:* Top-k facts retrieved by each memory system (Mem0, Letta, Supermemory, Zep, Base Layer) from the shared fact pool.

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Additional testing for Letta. Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions above, we ran a

**Comment:** Footnote originating from Letta mention in conditions table

*Paragraph context:* Additional testing for Letta. Of the four commercial memory systems, Letta is architecturally distinct: alongside retrieval, it maintains a persistent memory block that its agent self-edits during multi-turn conversation. Because this path is not exercised by the retrieval conditions above, we ran a

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** ; a high-baseline subject is one it does. This is the population of relevance:

**Comment:** This flows weird, you bring up low baseline, then high baseline, then state “this is the population of erelevence. Unclear what this is. This should likely be “Low-baseline subjects are the population of relevance”

*Paragraph context:* The baseline we refer to throughout is the no-context condition (C5): the response model’s score with no external information. A low-baseline subject is one the model has insignificant pretraining understanding of; a high-baseline subject is one it does. This is the population of relevance: living i

---

## 1.3 What we found (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** Category-shift evidence.

**Comment:** May want to point out what cases this happens in, with memory providers, with full raw corpus, with facts, etc? or is that implied?

*Paragraph context:* Category-shift evidence. The spec doesn’t just nudge the score; it changes the kind of answer the model produces. Crossing one rubric anchor moves a response from “wrong prediction” to “right direction with specifics.” Crossing two or more bands is qualitatively bigger: a single question where the A

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Category-shift evidence.

**Comment:** Re-word this section title to get across point clearly. Want to get across the significance of multi anchor level jump

*Paragraph context:* Category-shift evidence. The spec doesn’t just nudge the score; it changes the kind of answer the model produces. Crossing one rubric anchor moves a response from “wrong prediction” to “right direction with specifics.” Crossing two or more bands is qualitatively bigger: a single question where the A

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Mechanism:

**Comment:** From running this, it is somewhat clear from baseline runs that htem odel is doing some kind of inference on it’s own, it’s likely doing with it with a users raw data, but its opque, and looks to be shallow vs an inspectiable behavioral specification.

*Paragraph context:* Mechanism: three patterns of interaction with retrieval (full development in §4.4.2):

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** the compressed specification

**Comment:** The compressed spec or a compressed spec?

*Paragraph context:* Exploratory note: Letta stateful-agent path. Letta’s stateful-agent architecture self-edits a persistent memory block during ingestion. On 3 subjects (post-hoc), it scored above the Base Layer compressed-brief variant at matched response model. At the largest corpus tested, the block grew to ~335K c

---

## 1.4 What this implies (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** personalization remains surface-level (style, voice, preference) without the interpretive substrate that lets an agent act on a specific person’s behalf

**Comment:** But frankly, this would make no sense if it were to happen. Seems unlikely?

*Paragraph context:* The gap the Behavioral Specification fills cannot be closed by training a larger model on more public data. The private record does not exist in a form a training corpus can capture. The structural options are narrow: either each person supplies their own representation to whatever AI system serves 

---

## 2. Prior Work and Industry Benchmarks (style: Heading2)

### comment
**Author:** Aarik Gulaya  
**Anchor:** Prior Work and Industry Benchmarks

**Comment:** May be worth titling something that implies we are evaluating prior work and industry benchmarks in relation to a 5th target. Prior Work, Industry Benchmarks, The Fifth Target. (somewhat of a reference to the fifth element lol)

*Paragraph context:* 2. Prior Work and Industry Benchmarks

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** neural-memory-analogue systems (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings),

**Comment:** Its not just nueral memory analogue, but also providers like mem0, and zep, vector based retrieval, basically recall optimized efforts

*Paragraph context:* Memory systems today optimize for recall. Some efforts build neural-memory-analogue systems (architectures that borrow from human memory engineering: episodic consolidation, working-memory slots, retrieval over embeddings), but their targets remain general rather than individual. A separate body of 

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** hat kind of intentional individual-specificity, not “bias” in any pejorative sense but an explicit design target, is the missing thread in current AI memory and human-AI interaction research.

**Comment:** This should be brought up in closing as well

*Paragraph context:* Language models are trained to produce responses that are helpful on average across a large population of users. That optimization target produces outputs that no single user is the reference point for. Personalization requires the opposite property: a system whose outputs are tuned to a specific in

---

## 2.1 Memory and personalization benchmarks (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** Survey-response prediction interpolates within a structured response distribution

**Comment:** Needs to be layman

*Paragraph context:* Survey-response prediction interpolates within a structured response distribution. Twin-2K (Toubia et al., 2025, arXiv:2505.17479) predicts held-out survey responses from other survey responses for 2,058 participants. The task format matches the persona format: structured responses on a Likert or nu

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** over turns

**Comment:** Over turns is not layman, unless want to include footnote definition of over turns

*Paragraph context:* Persona fidelity measures consistency of self-presentation over turns. PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416) measures whether a model maintains a described persona during conversation: given a one-line persona (“You are a 45-year-old skeptical accountant from Toronto”)

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** over turns

**Comment:** Again with over turns, need to describe what this means if using, explicitly, footnote likely

*Paragraph context:* Persona fidelity measures consistency of self-presentation over turns. PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416) measures whether a model maintains a described persona during conversation: given a one-line persona (“You are a 45-year-old skeptical accountant from Toronto”)

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Twin-2K’s full-text survey persona.

**Comment:** How many tokens?

*Paragraph context:* Persona fidelity measures consistency of self-presentation over turns. PersonaGym (Samuel et al., Findings of EMNLP 2025, arXiv:2407.18416) measures whether a model maintains a described persona during conversation: given a one-line persona (“You are a 45-year-old skeptical accountant from Toronto”)

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** The scope of that proposal is bounded; the rest of this section is precise about what it claims.

**Comment:** Is this statement necessary?, don’t insult the readers

*Paragraph context:* We propose behavioral prediction on held-out reasoning situations as a test of a fifth target: representational accuracy. The scope of that proposal is bounded; the rest of this section is precise about what it claims.

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** §7

**Comment:** Link

*Paragraph context:* The held-out design tests a stability assumption. The methodology assumes that a person’s interpretive patterns are stable enough within their own corpus that patterns captured from one half reference patterns in the other. Without this assumption, held-out behavioral prediction is impossible in pri

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** §7

**Comment:** Link

*Paragraph context:* A related open question for production deployment is how to handle canonical life events. A person can undergo events (a major career change, a religious conversion, a significant loss, a public stance reversal) that fundamentally shift their subsequent reasoning. The main-study autobiographies were

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** 

**Comment:** 

*Paragraph context:* The missing axis is representational accuracy itself. Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to antici

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** §7

**Comment:** link

*Paragraph context:* The missing axis is representational accuracy itself. Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to antici

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** ’s approach

*Paragraph context:* The missing axis is representational accuracy itself. Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to antici

---

### tracked_delete
**Author:** Aarik Gulaya  
**Text:** ’s battery

*Paragraph context:* The missing axis is representational accuracy itself. Each existing benchmark family measures a real property of memory systems, and each is useful for its own target. What is missing is an axis that measures how accurately the memory system represents the person whose behavior it is meant to antici

---

## 2.2 Memory systems for LLM agents (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** (vendor-reported; evaluation harness open-sourced at github.com/mem0ai/memory-benchmarks)

**Comment:** parenthetical likely in footnote

*Paragraph context:* Current algorithm: 91.6 LOCOMO, 93.4 LongMemEval (vendor-reported; evaluation harness open-sourced at github.com/mem0ai/memory-benchmarks). Peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini.

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini.

**Comment:** this should also be footnote, should keep published recall score column for actual scores, not references or pointers

*Paragraph context:* Current algorithm: 91.6 LOCOMO, 93.4 LongMemEval (vendor-reported; evaluation harness open-sourced at github.com/mem0ai/memory-benchmarks). Peer-reviewable paper (Chhikara et al., arXiv:2504.19413) reports 68.44 LOCOMO for the Mem0g variant with GPT-4o-mini.

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** ^architectural distinction worth surfacing

*Paragraph context:* ^architectural distinction worth surfacing

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** (Letta blog, 2025-08-12)

**Comment:** footnote with link**

*Paragraph context:* 74.0% on LOCOMO with GPT-4o-mini (Letta blog, 2025-08-12)

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** (Rasmussen et al., arXiv:2501.13956)

**Comment:** footnote

*Paragraph context:* 71.2% on LongMemEval with GPT-4o (Rasmussen et al., arXiv:2501.13956)

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Appendix

**Comment:** likely this could be a goot note as well, the entire architectural distinction wroth surfacing?

*Paragraph context:* Architectural distinction worth surfacing. Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is the only one whose core architecture treats memory as something an agent synthesizes during conversation rather than stores for later retrieval. The agent’s main context holds structured 

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Architectural distinction worth surfacing. Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is the only one whose core architecture treats memory as something an agent synthesizes during conversation rather than stores for later retrieval. The agent’s main context holds structured 

**Comment:** 

*Paragraph context:* Architectural distinction worth surfacing. Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is the only one whose core architecture treats memory as something an agent synthesizes during conversation rather than stores for later retrieval. The agent’s main context holds structured 

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Table 2.1; their per-vendor research pages and the Mem0 / Zep / Supermemory papers cited above hold the architectural details that did not carry into the body here.

**Comment:** can be a footnote**

*Paragraph context:* Architectural distinction worth surfacing. Of the four systems, Letta (Packer et al., 2023, arXiv:2310.08560) is the only one whose core architecture treats memory as something an agent synthesizes during conversation rather than stores for later retrieval. The agent’s main context holds structured 

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** A note on benchmark scores in this field.

**Comment:** also all of them are getting very high scores, you could say that recall is effectively solved, or may a mention, head nod to it

*Paragraph context:* A note on benchmark scores in this field. The recall-benchmark landscape for memory-for-agents is contested. Mem0 and Zep have publicly disputed each other’s LOCOMO methodology in a GitHub issue (getzep/zep-papers#5), with Mem0 alleging that Zep’s 84% claim included adversarial question categories t

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** A note on benchmark scores in this field. The recall-benchmark landscape for memory-for-agents is contested. Mem0 and Zep have publicly disputed each other’s LOCOMO methodology in a GitHub issue (getzep/zep-papers#5), with Mem0 alleging that Zep’s 84% claim included adversarial question categories t

**Comment:** This note should likely be in the appendix. Would rather immedietly get to the “all four are sophisticated systems” Maybe want to “^note on benchmark scores” somewhere earlier, or with the table?

*Paragraph context:* A note on benchmark scores in this field. The recall-benchmark landscape for memory-for-agents is contested. Mem0 and Zep have publicly disputed each other’s LOCOMO methodology in a GitHub issue (getzep/zep-papers#5), with Mem0 alleging that Zep’s 84% claim included adversarial question categories t

---

## 2.3 Traceability (style: Heading3)

### comment
**Author:** Aarik Gulaya  
**Anchor:** 3 Traceability

**Comment:** This section seems to cover more explicitly how traceability is a key factor for the behavioral spec, most importantly, that pure fact level traceability does not provide a reasoning trace. That reasoning trace is what we are explicitly after. Maybe should be using the term reasoning trace here.

*Paragraph context:* 2.3 Traceability

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** Traceability is not a feature of the Behavioral Specification. It is a necessity.

**Comment:** This feels a bit salesly, GTM

*Paragraph context:* Traceability is not a feature of the Behavioral Specification. It is a necessity. A system that represents how a person reasons must be auditable by that person, or the representation is a black box they cannot verify. The memory systems we evaluate provide traceability at the fact level. Zep has th

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** reasons.

**Comment:** Reasoning traces would work perfecetly with how we are already deifning it, it would be a term of art as well.

*Paragraph context:* Fact-level traceability answers where a retrieved claim came from. That is necessary but not sufficient for a representation of how a person reasons. What is also required is traceability at the reasoning level: why the system believes this about this person, not just which fact it pulled. The Behav

---

### comment
**Author:** Aarik Gulaya  
**Anchor:** The phrase is the title of anchor A2 in data/global_subjects/sunity_devee/anchors_v4.md. A2 is grounded in extracted facts including F-73 (“Sunity Devee’s mother would never countenance anything her conscience told her was wrong”) and F-414 . Each fact in facts.json carries the verbatim source-passa

**Comment:** This examples needs to be a bit more clear and structured We should have an example response, show how parts of the response are tagged to a particular part of the behavioral spec, then can see the facts related to that behavioral spec, to see what the inference is. Should likely be separate lines/paragraphs, similar to how we show example responses. As it is currently presented it is a bit convoluted and not very layman.

*Paragraph context:* Worked example. When the response model generates a prediction on Sunity Devee citing “spiritual integrity over social cost” as the reason a character would refuse familial pressure, that interpretive frame traces back through three layers. The phrase is the title of anchor A2 in data/global_subject

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Worked Example

*Paragraph context:* Worked Example

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Sunity Devee

*Paragraph context:* Sunity Devee

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Question:

*Paragraph context:* Question:

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Response: Lorem Ipsum, trfigio^C4, autditore legume^P1, a mia.

*Paragraph context:* Response: Lorem Ipsum, trfigio^C4, autditore legume^P1, a mia.

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Reasoning

*Paragraph context:* Reasoning Trace/Context Explanation:

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Trace/Context Explanation:

*Paragraph context:* Reasoning Trace/Context Explanation:

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Ref

*Paragraph context:* Referenced Behavioral Spec Items:

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** erenced Behavioral Spec Items:

*Paragraph context:* Referenced Behavioral Spec Items:

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** -P1- Analysis under authority

*Paragraph context:* -P1- Analysis under authority

---

### tracked_insert
**Author:** Aarik Gulaya  
**Text:** Related Facts

*Paragraph context:* Related Facts

---
