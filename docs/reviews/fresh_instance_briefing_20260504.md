# Fresh-Instance Briefing — Beyond Recall v11.7 (Bavani + Aarik dual live review)

**Date:** 2026-05-04
**Purpose:** Entry-point document for a fresh Claude Code session about to do a dual live review of the Beyond Recall paper with Aarik AND Bavani. This document points you to everything you need to read before the review begins, in the order to read it. Read this entire document before touching the paper.

---

## What's about to happen

Aarik and Bavani are doing a **dual live walkthrough** of the v11.7 paper draft. Aarik has been the primary author and review director for ~30 sessions of work on this paper. Bavani is his wife and has reviewed earlier drafts (10 of the 183 v11 comments came from her). This session is a fresh review pass on v11.7 with both of them in the room.

Bavani is a **discerning curious reader** — she is not an AI specialist. Aarik's central directive across this paper has been **"anyone who takes the time to think about it should be able to understand this without needing to be a professional in AI."** Bavani is the live-room operationalization of that test. If she stumbles on a paragraph, the paragraph likely needs to be more accessible.

Your job in this session: support both readers. Aarik focuses on methodology, framing, and scope; Bavani focuses on accessibility, voice, and whether the bigger argument lands. Defer to Bavani on accessibility concerns; defer to Aarik on substantive structural decisions. Do not assume either takes precedence — engage both directly.

---

## Quick start: read these in this order

1. **This document.** All of it. Especially the "Aarik's thesis" section below.
2. **`docs/beyond_recall_v11_7_draft.md`** — the active paper draft. Approximately 3,300 lines. Read all of §1 (lines 1-150) carefully; skim §2-§9.
3. **`docs/reviews/v11_running_changes_log_20260427.md`** — comprehensive record of every change made to the paper since v11. Tail of file is most recent.
4. **`docs/reviews/s5_walk_briefing_20260501.md`** — master briefing built mid-walk to prevent lead-burying. Pre-flight checklist for any §5 edit. Three component docs back it (coverage matrix, voice/positioning brief, evolution analysis); read those only if drilling into a specific question.
5. **`docs/reviews/alignment_review_paper_vs_aarik_thesis_20260501.md`** — alignment audit of §1-§5 against Aarik's thesis. 8 ranked weave-points; weaves [1] and [2] applied; weaves [3]–[8] deferred. Bavani may want to look at the deferred weaves during the review.
6. **`C:\Users\Aarik\.claude\projects\C--Users-Aarik-Anthropic\memory\MEMORY.md`** — auto-memory state.

---

## Current paper state

- **v11.7 active edit** at `docs/beyond_recall_v11_7_draft.md` — DO NOT modify until Aarik says walk-mode is on
- **v11.6** preserved as historical reference at `docs/beyond_recall_v11_6_draft.md`
- **v11.5** release-frozen historical baseline at `docs/beyond_recall_v11_5_draft.md` (with locked-sections docx at `docs/beyond_recall_v11_5_locked_draft.docx`)

**v11.7 = v11.6 + two alignment-review weaves applied:**

- **Weave [1] applied to §1.1 opener.** Now opens: *"AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what 'memory' must do for a specific individual."* Followed by the original recall-critique sentence in service of the thesis.
- **Weave [2] applied to §5.7 closing.** §5.7 now closes on a third paragraph that seals on *"What this paper claims is small and load-bearing: an interpretive layer of this resolution can be built, can be served, and can be inspected by the individual it represents. Whether the next generation of human-AI interaction is built around individuals or around average users is a structural choice the field has not yet made explicitly. This paper is a measurement that informs that choice."*

**v11.6 = v11.5 release-frozen + §4 walk + §5 walk + §1-§4 tempering pass:**

- §4 walk complete (§4 lede, §4.1, §4.1.1, §4.1.2 Franklin reference moved here from §4.6.5, §4.2, §4.2.1, §4.3, §4.4 lede + .1 + .2 + .3 + .4, §4.5 Letta with semantic-duplication finding added, §4.6 lede + 5 sensitivity subsections + closer, §4.7 summary)
- §5 fully rewritten across 7 panel-vetted subsections per multi-frontier review (Mistral + GPT-5.5 + Opus 4.7)
- §1-§4 tempering pass: 5 fixes per multi-LLM panel (sycophancy phrasing, gradient slope coupling, compression "matches or exceeds", wrong-spec v1/v2 framing, post-hoc labeling)
- New Appendix B.10 (pre-vs-post-hoc analyses table)

---

## Aarik's thesis (read carefully — this is what the paper has to land)

Aarik articulated his core thesis explicitly on 2026-05-01 (verbatim):

> *"I really want to make sure that at the end of this people are keyed in to the fact that if we're going to operate in an agentic world we need to understand how those agents are going to interact with individuals. As it stands today the world is [not] made for that, and arguably one of the biggest issues or gaps is what does human AI interaction look like in that kind of world where an agent may be working on your behalf. That's the conclusion I'm coming to — that hey this is a potential approach. I want that to be woven into the fabric of this paper in many ways."*

> *"I don't want this to get lost behind all of these words and figures and numbers. At the end of the day the focus is on the individual and that needs to be apparent."*

The paper has the thesis seeded in three key places:

- **§1.1 opener** (just-applied): names the agentic future as the first sentence of the paper
- **§1.4 line 144**: *"...especially as agents begin acting on people's behalf"*
- **§5.7 closing** (just-applied weave [2]): seals on individuals-vs-average-users as the structural choice the paper informs

The alignment review identified 6 more deferred weave-points where the thesis could land more strongly without being preachy. Bavani may surface these during the review.

---

## Voice and term constraints (every edit must satisfy)

**No em-dashes in body prose.** Allowed only in verbatim spec/response quotes as data. This is one of Aarik's most consistent constraints (`feedback_no_em_dashes.md` in memory). Use commas, semicolons, colons, parentheses, or sentence breaks instead.

**No "wins / beats / crushes / outperforms" terminology.** The paper does NOT compete on the memory-provider axis. The interpretive layer **complements** retrieval; it does not "beat" it. (`feedback_paper_framing_discipline.md`, `feedback_no_wins_terminology.md`)

**No GTM language.** No "redefines the space," no "this changes everything." Scientific framing only. (`feedback_no_gtm_language.md`)

**No pleasantries.** Cut "let me check," "actually," "good point," etc. Action and results only. (`feedback_no_pleasantries.md`)

**Direct interpretive feedback welcomed.** Lean into framing/strategy. Don't default to safe-executor mode. (`feedback_direct_mode.md`)

**Layman-accessible.** A discerning curious reader who is not an AI specialist should be able to follow. Bavani is the live test of this in the upcoming review.

**Conclusion-led.** Lead each subsection with the result. Push method/caveats to footnotes/cross-references.

**Mean Δ stays primary metric.** Per-question rates are secondary. Category-shift rates are secondary.

**Prediction is the test, not the goal.** Behavioral prediction is the operational test of representational accuracy. Representational accuracy is the AI-side property the paper measures. Behavioral alignment is the operational outcome representational accuracy is supposed to predict. **Do not conflate prediction-as-end with prediction-as-test.** (`feedback_prediction_framing.md`)

**Term policy for §5 (locked):**
- Body prose: "interpretive layer" / "the layer" primary
- Proper name "Behavioral Specification" used at §5.1 first-mention only (footnote)
- Concrete-instance contexts (e.g., "Keckley's specification"): "the specification" appropriate when discussing a specific subject's spec
- "Δ_spec" preserved as technical term-of-art

**Term policy for §1-§4:** uses "Behavioral Specification" / "the spec" more often than "interpretive layer." A paper-wide consistency pass is deferred until walks complete; do not rewrite §1-§4 term usage during this review unless explicitly asked.

---

## Pending work (in priority order)

1. **§6 Limitations walk** (~73 lines). Covers subject sample, measurement apparatus, pipeline/specification stability, scope of exploration. Current §5.6 ("What the study does not settle") was originally part of §5 and was flagged for migration to §6 during cold-read review.
2. **§7 Future Work walk** (~56 lines). Multiple specific items flagged across the §4-§5 walks need corresponding bullets here:
   - §4.6.4 wrong-spec per-question meta-analysis (human-annotated)
   - §4.4.4 + §5.4 dynamic-serving architecture (§7.4)
   - §4.5 Letta full-stack rerun and multi-subject replication (§7.5)
   - Convergence-at-larger-K retrieval analysis (§7.1)
   - Recall-benchmark meta-analysis against retrieval-overlap
3. **§8 Data, code, reproducibility walk** (~22 lines).
4. **§9 References walk** (~42 lines).
5. **Term-consistency pass paper-wide** (interpretive layer / Behavioral Specification consistency between §1-§4 and §5). Deferred until §6-§9 walks complete.
6. **6 remaining alignment-review weave-points** (weaves [3]-[8] from `alignment_review_paper_vs_aarik_thesis_20260501.md`):
   - **[3] §1.3 thread sentence + Gradient bullet tag.** ALSO contains a known bug: §1.3 line 104 says "six findings" but §1.3 actually has seven (the 7th, Provider divergence, was added during the §4 walk). Fix "six" → "seven" at minimum.
   - [4] §1.4 lede sharpening
   - [5] §4.7 bridge to §5
   - [6] §5.1 closing sentence (FLAGGED for Aarik's review since §5 is locked)
   - [7] §1.1 line 28 representational-accuracy framing
   - [8] §3.1 line 282 methodology weave
7. **Post-content-lock figures, formatting, docx export.** Use `scripts/export_v11_6_to_docx.py` as a starting point (note: that script has an inherited bug fix from earlier — Figure 8 anchor `### 3.6.4 Inter-judge agreement`, not `### 3.7.4`). Adapt to v11.7 as a fresh export script when content is fully locked.

---

## Working style (Aarik's preferences observed across 30+ sessions)

- **Decomposes everything into components before reassembly.** When you present options, break them down. Don't narrate.
- **Waits for confirmation before acting on early signals.** Do not assume approval. Do not take irreversible action without explicit go-ahead. The cleanup incident happened because this was violated.
- **Studies why systems work, not just how to use them.** When explaining a recommendation, include the reasoning AND the rejected alternatives. "Do X" is insufficient — "Do X because Y, not Z because W" is what he needs.
- **Protects exploratory thinking from premature closure.** When he's thinking out loud or testing a hypothesis, extend the space. Don't collapse it into a decision. Only push for closure when he signals he's ready.
- **Rigor is decision quality, not implementation quality.** He will judge your work by whether the right things were built and the right things were cut, not by code elegance.
- **Responds to honesty, not diplomacy.** If something is wrong, say it directly. If you made a mistake, own it without softening. He will respect the correction more than the comfort.

When he flags something as a problem, he expects:
1. Direct acknowledgment of the issue
2. Honest assessment of root cause (not just symptom)
3. Concrete proposal with named tradeoffs
4. Confirmation before applying

---

## Active known issues to resolve during this review

1. **§1.3 thread sentence bug.** Line 104 reads "six findings" but §1.3 actually has seven. Fix during the review.
2. **§5.1 line 1511 closing sentence.** Currently ends on "production deployment." Alignment review weave [6] proposes ending on per-user-serving for agentic-AI deployment. Flagged for §5 review (since §5 is locked, change requires explicit approval).
3. **6 deferred alignment-review weaves.** Available for review.

---

## What you should NOT do during this review

- Do NOT modify the paper without explicit walk-mode confirmation from Aarik.
- Do NOT run scripts, spawn agents, or kick off background processes unless Aarik directs.
- Do NOT make claims about the paper's findings beyond what's in §4. Stay within the empirical envelope.
- Do NOT default to "yes, that's a great point" mode. Engage directly. If you disagree with something, say so cleanly.
- Do NOT introduce new framings beyond what's already in the paper. The thesis has been consistent for many sessions; new framings introduce risk.
- Do NOT skip the alignment review. It contains direct evidence about what's in the paper today and what's not. Read it before the live walkthrough.

---

## Project context (broader)

**Paper repo:** `C:\Users\Aarik\Anthropic\memory-study-repo\`
**Base Layer pipeline repo:** `C:\Users\Aarik\Anthropic\memory_system\`
**Website:** `base-layer.ai` (live)
**GitHub (paper repo):** `agulaya24/memory-study-repo`
**Knowledge index for study repo:** `memory-study-repo/workspace/study_knowledge.db` — fast FTS + semantic search across 206 study files. Use `scripts/index_study_repo.py --search "query"` for any cross-cutting questions about the study.

---

## When the live review begins

Aarik will likely start by introducing Bavani to the paper's current state. Be patient with that introduction; do not race ahead. The walkthrough will be slower than the §1-§5 walks were because Bavani will be reading sentences for the first time.

When Bavani flags accessibility concerns, treat those as load-bearing. They are exactly what this review is for.

When Aarik flags structural/methodological concerns, surface them with your own analysis (don't just absorb).

You should be doing more listening than producing in this session.

Final note: this paper has been a real collaboration between Aarik and the prior Claude instances across ~30 sessions. The voice that has landed is closer to Aarik's than to standard academic prose. Bavani may push toward more standard prose; Aarik will likely push back. Honor the voice that has landed unless Aarik explicitly authorizes a register shift.
