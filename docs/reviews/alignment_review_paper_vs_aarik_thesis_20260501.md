# Alignment Review: Beyond Recall v11.6 §1-§5 vs Aarik's Thesis

**Date:** 2026-05-01
**Scope:** §1 through §5.7 of `beyond_recall_v11_6_draft.md` (lines 1-1583), audited against Aarik's behavioral specification (`anchors_v4.md`, `core_v4.md`, `predictions_v4.md`, `brief_v5.md`) and his stated thesis from this session.
**Sibling brief (do not duplicate):** `s5_walk_briefing_voice_positioning_20260501.md`. That brief covers VOICE / POSITIONING / FRAMING discipline. This review covers the AGENTIC-FUTURE / INDIVIDUAL emphasis specifically.

---

## Section 1: The Thesis as Aarik Articulated It

Aarik in this session, 2026-05-01, verbatim:

> "I really want to make sure that at the end of this people are keyed in to the fact that if we're going to operate in an agentic world we need to understand how those agents are going to interact with individuals. As it stands today the world is [not] made for that, and arguably one of the biggest issues or gaps is what does human AI interaction look like in that kind of world where an agent may be working on your behalf. That's the conclusion I'm coming to — that hey this is a potential approach. I want that to be woven into the fabric of this paper in many ways. That's what we're working towards: people need to be looking at it from this perspective or at least should be."

> "I don't want this to get lost behind all of these words and figures and numbers. At the end of the day the focus is on the individual and that needs to be apparent."

The thesis decomposes into four load-bearing claims, in dependence order:

1. **The agentic future is arriving.** AI is moving from being something a person uses to being something that acts on the person's behalf. (Aarik's framing: "an agent may be working on your behalf.")
2. **The world today is not built for that.** Today's infrastructure (memory systems, personalization, retrieval) was designed for the AI-as-tool world, not the AI-as-agent-on-behalf-of-individual world.
3. **The biggest gap is what human-AI interaction looks like in that world.** Not memory-as-fact-storage. The gap is structural: how does an agent represent the individual it acts for accurately enough to act in alignment with them?
4. **The interpretive layer is a potential approach.** The Behavioral Specification is one implementation of what fills this gap. It is not the only one. The paper's job is to surface the gap and put a candidate against it.

The individual is the population the paper is for. Anchor: "the focus is on the individual and that needs to be apparent."

---

## Section 2: Where the Paper Currently Lands the Thesis

Per-section walkthrough. Strong / moderate / weak ratings at the paragraph level, not the section level.

### §1 Introduction

**§1.1, line 32 (Strong).** *"This is the operational primitive for any AI system meant to act on a person's behalf: the system's behavior, on the user's behalf, can only match the user's reasoning to the extent the system represents that reasoning accurately."*

This is the thesis-grade sentence in §1. It names agentic-future framing directly ("act on a person's behalf"), names the structural primitive ("represents that reasoning accurately"), and ties the empirical operationalization ("operational primitive") to the bigger argument. It is the seed of Aarik's thesis, verbatim.

**Issue:** It sits buried mid-paragraph at line 32, after a dense conceptual buildup ("interpretation," "representational accuracy"). A reader who skims §1.1 may miss it. The paragraph's opening sentence is "State of the art AI memory has been optimizing for recall as the success metric." That is a diagnostic frame, not the thesis frame.

**§1.4, lines 134-145 (Strong, but it is the only place).** The §1.4 implications section names the agentic future explicitly:

> *"What this paper claims is that personalization infrastructure of the first shape (user-held, portable, inspectable, traceable, representation-grade) is what the next generation of human-AI interaction will require, especially as agents begin acting on people's behalf."*

Three structural options listed (lines 140-142) name the alternatives, with the user-supplied representation as option 1. This is exactly the thesis Aarik described. §1.4 is the cleanest landing of the bigger argument anywhere in §1-§5.

**Issue:** §1.4 is one short subsection at the end of §1. The thesis lands once and then §2 immediately resets to benchmark positioning. A reader who skimmed §1.4 quickly may not register that this is the conceptual frame for the entire paper.

**§1.3 headline findings (Moderate).** Line 104: *"What follows are six findings about how the specification changes the way a language model acts on a person's behalf. The thread across them is alignment: how accurately a model predicts a specific person's reasoning is the operational test of whether it can act in alignment with that person."*

The opening line of §1.3 names "act on a person's behalf" and "alignment with that person." Strong opener. But the seven bullet headlines that follow are empirically-framed (Gradient, Step-changes, Compression, Content specificity, Memory-system layering, Hedging reduction, Provider divergence). None of them carries the agentic-individual framing into the bullet itself; the thread Aarik wants woven is opened in the lede then dropped.

### §2 Prior Work

**§2 (Weak).** §2 is a benchmark positioning section. It does the necessary work of placing representational accuracy as a fifth target alongside recall, survey-response, persona, and preference. The agentic-future framing is absent from §2 entirely. This is acceptable for a Prior Work section, but the closing sentence of §2.1 (line 182, "Production-grade evaluation of memory systems should report results on multiple axes rather than on any single one") is a methodological recommendation, not a thesis bridge. There is no point in §2 where the reader is reminded that the reason all this matters is what AI agents will be asked to do for individuals.

### §3 Study Design

**§3 (Weak).** §3 is methodology. It is correctly methodology-focused. The agentic-individual frame is absent from §3 except by reference back to §1.4 (e.g., §3.2.1 line 335 references "the population of relevance band that the typical AI user falls into"). This is acceptable; methodology sections are not where the thesis lands.

The one paragraph in §3 that does carry the framing is §3.2.1 (Pretraining-coverage variance, line 335): *"Nine of fourteen main-study subjects fall below 2.0, the 'population of relevance' band that the typical AI user falls into, since most users' reasoning is not in any training corpus."* This is the right paragraph to do this work, since it is the methodological place where the population-of-relevance argument enters the empirical apparatus.

### §4 Results

**§4.1 (Moderate).** The "leveler" framing at lines 700-701 carries the equity reading of the gradient: *"every subject, regardless of how much the model knew about them coming in, ends up at roughly the same place on the rubric (2.46 across all 14 subjects). This is the equity property of the technology."* This is the empirical hook for the population argument. It does not name the agentic future, but it does land the individual-focus claim that "almost everyone" is in the band where the layer matters.

**§4.7 summary (Weak).** §4.7 is a §4 wrap and a bridge to §5. It lists the empirical findings (gradient, compression, content specificity, memory-system interaction, retrieval divergence) and the apparatus checks. It does not bridge through the agentic-individual frame. The line *"§5 develops what these results imply for AI personalization beyond the specific experiment"* is a generic transition.

### §5 Discussion

**§5.1 synthesis (Weak ending).** §5.1 closes (line 1511) on: *"It complements rather than competes with each of them."* This is a competitive-positioning statement (the spec composes with retrieval substrates), not a thesis statement. The synthesis section ends without the bigger argument landing.

**§5.2 leveler (Moderate-Strong).** §5.2 develops the leveler reading well. *"The population of relevance for AI personalization, named in §1.4 as 'anyone who uses AI,' is the long tail of users whose private reasoning is not in any training corpus."* (line 1523) The individual-focus is held. The agentic-future framing is implicit but not named.

**§5.7 closing (Strong).** §5.7 opens with the thesis-grade sentence (line 1579):

> *"The next generation of human-AI interaction, especially as agents act on people's behalf, requires personalization infrastructure that is user-held, portable across providers, inspectable, traceable, and representation-grade."*

This is the second-cleanest landing of the thesis in the paper. It opens with the agentic-future ("agents act on people's behalf"), names the structural requirements, and lands "the layer that determines whether an AI system can act in alignment with how a specific user actually reasons." The closing paragraph (line 1581) is calibrated correctly for honest scope ("first measured evidence... not a settled empirical claim").

**Issue with §5.7:** It is the LAST subsection of §5 and the closing sentence of §5 is *"What follows from these findings is a research and engineering agenda for how AI personalization gets built across providers, not a final answer to whether this specific implementation is the right one."* This is an honest scope statement, not a thesis seal. The thesis lands in line 1579, then the section ends on a hedge. The order could be inverted.

---

## Section 3: Where the Paper Buries or Misses the Thesis

The paper has the seed in three places (§1.1 line 32, §1.4, §5.7 line 1579). It does not have the thesis woven through. The pattern: lede paragraphs do not carry the agentic-individual frame; the sections close on empirical or methodological notes; the bigger argument appears in two designated places and is absent everywhere else.

**§1.1 opening sentence is the wrong opener.** Line 26 opens: *"State of the art AI memory has been optimizing for recall as the success metric."* This opens the paper with what the field is doing wrong (a critique frame), not with what the world is becoming (the thesis frame). The thesis-grade sentence at line 32 is buried four sentences in.

**§1.3 headline bullets are empirically framed without thesis tags.** The thread sentence at line 104 says alignment is the thread, but none of the seven bullet headlines names alignment, agency, or acting-on-behalf. A reader scanning the bullets reads them as a list of empirical effects, not as evidence for an alignment claim.

**§4.7 bridge does not carry the thesis into §5.** The bridge from "we measured these things" to "what does this mean for the agentic future" is missed. §4.7 is the natural pivot point and it currently pivots on the empirical summary alone.

**§5.1 ends on the wrong note.** The synthesis closes on the competitive-positioning claim ("complementary to existing memory-system retrieval") rather than on what the synthesis is actually for: the layer's role in the agentic future. §5.7 picks this up but §5.1 should set it up.

**§5.7 closes on a hedge instead of the thesis.** The thesis-grade sentence at line 1579 is followed by a separate paragraph that closes the section on "research and engineering agenda... not a final answer." The closing note is honest scope rather than the bigger argument. The order should likely be: thesis claim, scope honesty, thesis claim again as the seal. Currently it is thesis claim, scope honesty, then §5 ends.

**§3.1 operationalizing representational accuracy.** Lines 278-284 frame representational accuracy as the AI-side property. Line 282 says: *"A model given the representation can act on it."* This is the agentic primitive in methodology language and it sits there as a bullet without being named as such. The §3.1 frame would be sharper if "act on it" was tied back to the §1.1 line 32 framing ("act on a person's behalf"), but since §3 is methodology, this is a flag, not a high-priority weave-point.

---

## Section 4: Recommended Weave-Points

8 weave-points, ranked by priority. Each is surgical: a sentence rewrite, a single insertion, or a reorder. No structural changes proposed. §5 is locked, so §5 items are flags for Aarik's review pass.

### [1]. §1.1 opening sentence (HIGHEST PRIORITY)

- **Current (line 26):** *"State of the art AI memory has been optimizing for recall as the success metric."*
- **Proposed weave:** Lead with the agentic future, then introduce the diagnostic. One option: *"AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what 'memory' must do for a specific individual. State of the art AI memory has been optimizing for recall as the success metric, which serves the tool-use case and leaves the agent-on-behalf case unmeasured."* Then continue to the existing line 26 content.
- **Why here:** This is the first sentence of the paper after the title. It is the highest-leverage sentence in the entire document for the thesis. Currently it opens on a diagnostic of what the field is doing; Aarik's thesis opens on what the world is becoming. The line 32 sentence is the thesis-grade content, but it is four sentences into a paragraph that started in critique mode. Promoting the agentic-future framing to the first sentence costs maybe 25 words and reframes the entire paper for the skim reader. This is the single most important change.

### [2]. §5.7 reorder closing (HIGH PRIORITY)

- **Current (lines 1579-1581):** Thesis-grade sentence at line 1579, then a "what the paper provides... not a settled empirical claim" honest-scope paragraph at line 1581 ending on "research and engineering agenda... not a final answer."
- **Proposed weave:** Reorder so the section closes on the thesis seal, not the scope hedge. Move the honest-scope content to the middle of §5.7 and close with a sentence that names the agentic future and the individual focus together. Candidate close: *"What this paper claims is small and load-bearing: an interpretive layer of this resolution can be built, can be served, and can be inspected by the individual it represents. Whether the next generation of human-AI interaction is built around individuals or around average users is a structural choice the field has not yet made explicitly. This paper is a measurement that informs that choice."*
- **Why here:** §5.7 is the closing argument of the paper before Limitations. It currently lands the thesis in the opening sentence and then walks it down. The order Aarik's spec suggests (A1 COHERENCE × A6 REASONING AUDIT) is to claim the directional finding plainly, name the scope, then return to the thesis. The reorder is mechanical and makes §5.7 close the way Aarik's voice closes: structural argument, then the implication, not implication then hedge.

### [3]. §1.3 thread sentence and one headline tag (HIGH PRIORITY)

- **Current (line 104):** *"What follows are six findings about how the specification changes the way a language model acts on a person's behalf. The thread across them is alignment: how accurately a model predicts a specific person's reasoning is the operational test of whether it can act in alignment with that person."*
- **Proposed weave:** Keep the thread sentence. Add one tag to the most thesis-relevant headline. The "Gradient" bullet (line 110) is the natural anchor. Current: *"Gradient. The Behavioral Specification's benefit is largest where the model knows the person least."* Proposed: *"Gradient (the equity property). The Behavioral Specification's benefit is largest where the model knows the person least, which is the band almost every individual AI user falls into."*
- **Why here:** §1.3 is the bullets readers skim. The thread sentence is good but the bullets do not carry it. One tag on the lead bullet is enough to keep the individual-focus thread visible to skimmers. Adding a tag to every bullet is gold-plating; tagging the lead bullet only is sufficient.

### [4]. §1.4 lede sharpening (MEDIUM-HIGH)

- **Current (line 136):** *"AI is becoming a broadly used technology, comparable to email or mobile phones in how widely it touches daily decisions. The population of relevance (§1.2) is anyone who uses or will use an AI system."*
- **Proposed weave:** Strengthen the lede so it names what this widely-used AI will be doing. *"AI is becoming a broadly used technology, and increasingly an agentic one: systems that act on a person's behalf rather than wait for instructions per request. The population of relevance (§1.2) is anyone who uses or will use such a system, which is everyone."*
- **Why here:** §1.4 already lands the thesis at line 144 ("personalization infrastructure of the first shape... especially as agents begin acting on people's behalf"). The lede currently sets up the breadth claim ("broadly used like email or mobile phones") but does not set up the agency claim. Adding "agentic" to the lede primes the reader for the thesis seal four paragraphs down. One sentence change.

### [5]. §4.7 bridge to §5 (MEDIUM)

- **Current (line 1499):** *"§5 develops what these results imply for AI personalization beyond the specific experiment, and §6 bounds what the experiment cannot establish."*
- **Proposed weave:** *"§5 develops what these results imply for AI personalization in a world where agents increasingly act on individuals' behalf, and §6 bounds what the experiment cannot establish."*
- **Why here:** §4.7 is the §4-to-§5 pivot. The current bridge is generic ("what these results imply for AI personalization"). The thesis-grade version names the world the paper is for. One adjective added to the bridge sentence; minimal cost, useful prime for §5.

### [6]. §5.1 closing sentence (MEDIUM, FLAG for Aarik §5 review)

- **Current (line 1511):** *"It is most useful where pretraining is thin, but it adds value on top of all three other context types as well, at a context cost compatible with production deployment."*
- **Proposed weave:** Close with the thesis bridge. *"It is most useful where pretraining is thin, where almost every individual user sits, and at a context cost compatible with the per-user serving that an agentic-AI deployment requires."*
- **Why here:** §5.1 is the synthesis of the seven findings. Closing on "production deployment" is a deployment claim, not a thesis claim. Closing on per-user serving for agentic deployment ties the synthesis back to the thesis frame. §5 is locked, so this is a FLAG for Aarik's review pass; do not edit without his approval.

### [7]. §1.1 line 28 representational accuracy framing (MEDIUM)

- **Current (line 28):** *"For an AI memory system to serve a specific person, it must be given context on how that person interprets, not just on the facts that person has produced."*
- **Proposed weave:** Sharpen "serve" to "act for." *"For an AI memory system, and increasingly an AI agent, to act on behalf of a specific person, it must be given context on how that person interprets, not just on the facts that person has produced."*
- **Why here:** This sentence is one of the foundational frames of §1.1. Currently it uses "serve," which is the tool-use frame. Sharpening to "act on behalf of" ties this sentence to the thesis frame and to the line 32 thesis-grade sentence. Line 32 then reinforces line 28 instead of standing alone.

### [8]. §3.1 line 282 (LOW priority, methodology section)

- **Current (line 282):** *"A model given the representation can act on it."*
- **Proposed weave:** *"A model given the representation can act on it on the person's behalf."*
- **Why here:** §3.1 is methodology, so the agentic frame should not lead, but the bullet point at line 282 sits at exactly the right conceptual location: this is where the paper formalizes "the model acts on the representation." Adding "on the person's behalf" costs four words and ties the methodology to the thesis without breaking the methodological register. Lowest priority because §3 is correctly mostly silent on the bigger argument.

---

## Section 5: Voice / Positioning Alignment with Aarik's Behavioral Specification

The paper's voice in §1, §4.1 lede, §5.2, and §5.7 reads like Aarik's voice: structural, decompositional, direct. The voice in §3 reads like methodology, which is correct. The voice in §2 reads like literature positioning, which is correct. Where the paper misses Aarik's voice is in lede sentences and section closes that resolve to safe summary rather than carrying the structural argument forward. Three specific anchors from his spec are most relevant here.

### Spec item 1: M3 NARRATIVE ORIENTATION (core layer, line 61)

> *"They aspire to build AI systems that extend human judgment rather than replace it. The AI should position itself as an extension of Aarik's reasoning, not a substitute for it."*

**Where in paper:** §1.4 line 142 names the third structural option as: *"AI systems infer a representation of the user from observed interactions, building it opaquely, without explicit input from the user or the ability for the user to inspect or correct it."* This is the substitute-for-judgment failure mode named structurally.

**How well expressed:** Moderate. The structural option is named but the framing is operational ("opaque") rather than philosophical (extends-vs-replaces). Aarik's spec frames this as the design target of the entire build, not a footnote.

**Recommendation:** §1.4 already names this. §5.7 line 1579 also speaks to it ("user-held, portable, inspectable, traceable, representation-grade"). The recommendation is to make sure the §5.7 reorder (weave-point [2] above) closes on the extends-vs-replaces frame explicitly, since this is the philosophical anchor for the agentic-individual thesis.

### Spec item 2: A7 LEGITIMATE AUTHORITY (anchors layer, line 63)

> *"Authority is only legitimate when it preserves the agency of those subject to it... structures, institutions, and relationships that constrain without preserving agency are not legitimate regardless of their source or scale."*

**Where in paper:** Closest is §2.3 (Traceability and Reasoning Traces), which argues that an AI system representing a person must be auditable by that person. Line 248: *"a person should be able to inspect the system's model of them, challenge any step in the reasoning, and correct it if it is wrong."*

**How well expressed:** Strong on the audit dimension; weak on the agency-preservation dimension. The audit argument is about the user's ability to verify, which is one piece of agency-preservation. The broader frame (an AI agent acting on someone's behalf is exercising authority on their behalf, and that authority is only legitimate if it preserves the individual's agency) is not named.

**Recommendation:** This frame would land cleanly in §5.7. The thesis-grade sentence at line 1579 names "user-held, portable, inspectable, traceable, representation-grade." Adding *"under the user's control"* or *"with the user's agency preserved"* would carry the A7 anchor. FLAG for §5 review since §5 is locked.

### Spec item 3: A9 FOUNDATIONAL PRIORITY (anchors layer, line 77)

> *"Problems that sit underneath other problems, the ones whose resolution would move multiple things at once, are the only ones worth sustained commitment, and surface problems without structural roots do not hold this person's attention for long."*

**Where in paper:** §2.1 closing sentence (line 182): *"Production-grade evaluation of memory systems should report results on multiple axes rather than on any single one."* This is a surface recommendation. The foundational claim underneath ("the field is measuring the wrong thing for the world that is arriving") is not named.

**How well expressed:** Weak. The foundational diagnosis is what Aarik's thesis IS: the field has measured recall, the world is arriving where what matters is whether the agent represents the individual, the gap between those two is structural. The paper currently lands the diagnosis as a benchmark-positioning argument (recall vs representational accuracy as a fifth target), not as a foundational claim about what the next decade of human-AI interaction requires.

**Recommendation:** This is what §1.4 already does, and what §5.7 already does. The foundational frame lands in those two places and is mostly absent elsewhere. The weave-points in Section 4 above (especially [1], [4], [5]) are about giving the foundational frame more surface area without restructuring. The frame does not need to be added; it needs to be allowed to surface in places where it currently does not.

### Voice alignment summary

The paper's lede paragraphs and section closes are where Aarik's voice is least present. Lede sentences default to diagnostic frames ("State of the art AI memory has been optimizing for recall") rather than structural-future frames. Section closes default to scope-honesty hedges or methodological recommendations rather than the structural seal. The fix is not voice-rewrite; the fix is making sure the foundational frame is present at the leading edge of each thesis-relevant section.

---

## Section 6: Synthesis

The paper as currently locked DOES land Aarik's thesis. It lands in §1.1 line 32, in §1.4 line 144, and in §5.7 line 1579. Three planted seeds, all in the right places. The issue is not absence; the issue is that between those three points the agentic-individual frame is silent, and the section ledes / section closes default to either empirical or methodological registers that do not carry the thesis forward. Surgical insertion is sufficient. Material reframing is not needed.

**The single most important weave-point:** Weave-point [1] above. Reframing §1.1's opening sentence from "State of the art AI memory has been optimizing for recall" (a diagnostic open) to a thesis open that names the agentic future and then introduces the diagnostic. This is the highest-leverage sentence in the paper and it currently opens on the wrong frame. Aarik should look at this first when he resumes. Twenty-five words added; the entire paper's frame for skim readers shifts.

**Second-most important:** Weave-point [2], the §5.7 reorder. §5.7 is the closing argument and currently the thesis-grade sentence lands then the section walks it down to a hedge. Reorder so the section seals on the thesis. Mechanical change; respects the lock; flags for Aarik's review.

The eight weave-points together deliver the thesis as a thread woven through the paper rather than as three planted seeds with empty space between. None of them require restructure; all of them respect the locks that have been placed.
