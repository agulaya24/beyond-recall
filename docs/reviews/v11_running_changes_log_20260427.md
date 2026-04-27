# v11 Running Changes Log

## Session pivot — 2026-05-04 (fresh context for Bavani + Aarik dual review)

End of working session 2026-05-04. Aarik is starting a fresh Claude Code instance to do a dual live walkthrough of v11.7 with Bavani. No paper edits made today; this is a context-handoff event, not a content event.

**Entry-point document:** `docs/reviews/fresh_instance_briefing_20260504.md`. The fresh instance should be pointed at this single file first; it then directs to v11.7 + this changes log + the §5 walk briefing + the alignment review in order.

**State at handoff:**
- v11.7 active edit at `docs/beyond_recall_v11_7_draft.md` (post §4 walk + §5 walk + §1-§4 tempering + 2 alignment-review weaves)
- v11.6 preserved at `docs/beyond_recall_v11_6_draft.md` (historical reference)
- v11.5 release-frozen baseline at `docs/beyond_recall_v11_5_draft.md` + `.docx`

**Pending after this review:** §6 Limitations walk, §7 Future Work walk, §8 Data/code walk, §9 References walk, term-consistency pass paper-wide, 6 deferred alignment weaves [3]-[8] (incl. §1.3 "six findings" → "seven" bug fix), figure review, formatting pass, v11.7 docx export.

**Carried directives (non-negotiable):** no em-dashes, no "wins" terminology, conclusion-led, layman-accessible (Bavani is the live test), prediction-as-test (not prediction-as-end), individual-focus throughout. Defer to Bavani on accessibility, defer to Aarik on substantive structure. Do not edit until Aarik says walk-mode is on.

---

## V11.7 fork — 2026-05-01 (post-alignment-review weaves)

V11.6 §5 walk complete. V11.7 forked from v11.6 to apply the two highest-priority weave-points from the alignment review (`docs/reviews/alignment_review_paper_vs_aarik_thesis_20260501.md`) per Aarik's request. Lower-priority weaves (3-8) deferred for future passes.

**Weave [1] applied: §1.1 opener (highest-leverage in entire paper).**

Original opener: *"State of the art AI memory has been optimizing for recall as the success metric."* This opens the paper on a critique frame.

New opener: *"AI is moving from a tool a person uses to an agent that acts on a person's behalf, and that shift changes what 'memory' must do for a specific individual. State of the art AI memory has been optimizing for recall as the success metric, which serves the tool-use case and leaves the agent-on-behalf case unmeasured."*

Reframes the paper for skim readers. Promotes Aarik's agentic-future thesis to the first sentence; the diagnostic critique becomes the second sentence in service of the thesis. ~25 words added; the rest of §1.1 is unchanged.

**Weave [2] applied: §5.7 reorder (closes on thesis seal, not scope hedge).**

Old §5.7 had two paragraphs: thesis-grade ¶1, scope hedge ¶2. The section ended on the hedge.

New §5.7 has three paragraphs: thesis-grade ¶1 (unchanged), scope hedge ¶2 (unchanged), and a new tight closing ¶3 that seals on the structural choice the paper informs. Added ¶3 verbatim:

*"What this paper claims is small and load-bearing: an interpretive layer of this resolution can be built, can be served, and can be inspected by the individual it represents. Whether the next generation of human-AI interaction is built around individuals or around average users is a structural choice the field has not yet made explicitly. This paper is a measurement that informs that choice."*

The closing now ends on the individuals-vs-average-users dichotomy and on the paper-as-measurement-that-informs-a-choice framing. ¶1 and ¶2 unchanged.

**V11.6 preserved as historical reference** at `docs/beyond_recall_v11_6_draft.md`. **V11.7 active edit** at `docs/beyond_recall_v11_7_draft.md`.

**Remaining alignment-review weaves (deferred):** [3] §1.3 thread sentence + Gradient bullet tag; [4] §1.4 lede sharpening; [5] §4.7 bridge to §5; [6] §5.1 closing sentence (FLAG for §5 review pass since §5 is locked); [7] §1.1 line 28 representational-accuracy framing; [8] §3.1 line 282 methodology weave. All surgical; total cost ~10-15 minutes if applied.

---



## V11.6 §5 walk complete — 2026-05-01

§5 fully locked across 7 panel-vetted subsections per the multi-frontier review verdict (Mistral Large + GPT-5.5 + Opus 4.7; Gemini Pro 503'd both rounds). Net change from cold-read agent's 8-subsection proposal: Letta architectural-ceiling demoted from peer subsection to in-text paragraph in §5.4 per panel tier-mismatch flag; current §5.6 "What the study does not settle" flagged for migration to §6 during the §6 walk.

§5 final structure:

- **§5 lede.** Conversational opener (Variant 2 + §1.1-grounded framing): *"§4 produced empirical results; §5 turns to what those results mean for AI acting on a specific person's behalf."* Roadmaps §5.1–§5.7 + separates §6 limitations and §7 follow-ups.

- **§5.1 Synthesis.** Three paragraphs + footnote. ¶1 encapsulation of all 7 §1.3 headlines with key stats; ¶2 synthesis claim (interpretive layer as new dimension distinct from raw facts, raw corpus, or current memory-system retrieval; complementary not competitive; useful where pretraining is thin AND additive on top of all three other context types); ¶3 construct-validity hedge + robustness pointers to §4.6 / §4.6.5. Includes the §4.4.1 interpretation-heavy lift framing for memory-system layering (was under-surfaced in earlier drafts; caught by Aarik this session).

- **§5.2 Why the gradient is the load-bearing finding.** Two paragraphs + footnote. ¶1 leveler reading (uniform post-spec quality near 2.46 regardless of baseline; multi-anchor crossings 55% / 1 in 5 as the qualitative dimension); ¶2 deployment / equity property + per-question echo. Footnote handles slope-coupling caveat (treatment-heterogeneity reading rejected). Folds in current §5.3 (population of relevance) per cold-read recommendation.

- **§5.3 Retrieval is not interpretation (surfaced post-hoc).** Four paragraphs. Diagnosis-half of thesis. Carries §1.3 7th headline; lead with non-convergence claim, post-hoc tag, ¶1 covers controlled + native test outputs; ¶2 epistemic limit (we don't know each provider's mechanism; only that selections diverge); ¶3 production-evaluation implication tied to §2.1 fifth-target argument; ¶4 bridge to §5.4. Anti-pattern avoided: alarmist framing about benchmarks. "Theory of relevance" softened per Aarik to "the mechanism producing each selection is not characterized in this study."

- **§5.4 Composition with retrieval: three patterns and architectural implications.** Five paragraphs. ¶1 three patterns as bulleted list (interpretive supply / over-theorization / spec-induced refusal) + per-system Δ_spec stats; ¶2 §4.4.4 statistical signatures (ρ = 0.27 spec-on-baseline re-ranking; ρ = 0.71 spec-on-info-rich uniform lift) tied back to patterns; ¶3 Keckley Q21 case (Keckley-specific axioms A1: Intimate Authority + A2: Documented Dignity) + dynamic-serving framing (panel-mandated softening from "requirement" to "next architectural step"); ¶4 Letta architectural-ceiling as in-text paragraph (panel-vetted demotion from peer subsection); §7.4 / §7.5 follow-up pointers.

- **§5.5 Wrong-spec mechanism and hedging elimination.** Three paragraphs. ¶1 content-vs-template separation (qualitative bracketing of triplet, no specific Δ values per Aarik's discussion-register pref); ¶2 hedging elimination using broad-rule stat (41.2% → 0.4%) + sycophancy rebuttal via Jain et al.; ¶3 Bernal Diaz Q16 transfer + per-predicate ablation null + new contrast vs §5.3 (retrieval-divergence at retrieval layer vs convergence at interpretive layer; the two layers operate differently — Aarik flagged this as load-bearing thread).

- **§5.6 Compression and what makes personalization operationally tractable.** Two paragraphs (cut from current §5.5's ~100 lines per panel guidance). ¶1 deployment-tractability claim (5x to 80x compression range; ~three-quarters of corpus lift); ¶2 Hamerton boundary case (2.63 vs 2.27, only main-study subject where inversion occurs) as evidence behaviorally relevant signal is sparse and structurally compressible. Production-architecture proposals (dynamic activation, modifiability, temporality, etc.) deferred to §7.

- **§5.7 Closing argument.** Two paragraphs. ¶1 lands both halves of thesis: agentic-future infrastructure framing (user-held, portable, inspectable, traceable, representation-grade); leveler / equity property keyed to "consistent representational accuracy" (NOT "consistent prediction quality" — Aarik flagged conflation; the layer brings every user to consistent accuracy of the construct, prediction is the test); fragmented-representation framing (matches §1.4 framing — most users have only fragments of their reasoning represented even with substantial public writing); diagnosis (industry solves style/voice/preferences; the interpretive layer is the part no one is solving); alignment as load-bearing operational concept ("the layer determines whether an AI system can act in alignment with how a specific user actually reasons"). ¶2 construct-validity hedge: directional empirical evidence not absolute; human-validation highest-priority follow-up (§7); research/engineering agenda framing.

### §5 walk briefing infrastructure

`docs/reviews/s5_walk_briefing_20260501.md` (master entry point, ~1,500 words) + three component reference docs (~16,700 words combined): coverage matrix, voice/positioning brief, evolution analysis. Built mid-walk to prevent lead-burying / inconsistency. Used as pre-flight checklist before each subsection draft from §5.2 onward.

### Term policy locked for §5

- Body prose: "interpretive layer" / "the layer" primary
- Proper name "Behavioral Specification" used at §5.1 first-mention (footnote)
- Concrete-instance contexts (e.g., "Keckley's specification"): "the specification" appropriate when discussing a specific subject's spec
- "Δ_spec" preserved as technical term-of-art
- Paper-wide consistency (§1-§4 use "Behavioral Specification" / "the spec" more) deferred to post-walk

## V11.6 §1-4 tempering pass complete — 2026-05-01

Five-item tempering pass applied per multi-LLM convergence (Mistral Large + GPT-5.5 + Opus 4.7) on the §1-4 review. All edits surgical (preserving voice and reasoning); no paragraph rewrites. Five fixes:

- **Fix 1: Sycophancy.** §1.1 line 32 — *"by construction cannot be passed by sycophancy"* → *"reduces the risk of sycophancy"* with new `[^sycophancy-def]` footnote (definition + Sharma/Perez/§2.4 Jain pointers). §6.2 cross-reference added for other LLM-judge failure modes the design does not address.
- **Fix 2: Gradient slope coupling + leveler framing.** §1.3 `[^statsig]` footnote tightened to point at §4.1 for full treatment. New "**The specification as a leveler**" callout in §4.1 (after the existing "What the gradient is actually showing" paragraph) names the affirmative reading: spec brings every subject toward 2.46 across baselines, equity property, portable across long-tail users.
- **Fix 3: Compression "matches or exceeds".** §1.2 H5: *"matches or exceeds"* → *"recovers most of"*. §1.3 Compression bullet: lead concretized to "5x to 80x smaller context length" (per-subject ratios in §4.2); italic stat replaced with aggregate (spec +0.71 vs corpus +0.93 across 9 low-baseline subjects) plus Hamerton boundary-case note (the only subject where spec beats raw).
- **Fix 4: Wrong-spec v1/v2 convention.** §3.4 line 406 — was internally contradictory ("C2c uses random derangement... and is the one reported" but paper headlines v1). Replaced with explicit two-variant description: v2 is the standard randomization control, v1 is an adversarial stress test designed to maximize the wrong-spec effect. §4.6.4 result paragraph reframed: *"stricter probe"* → *"adversarial stress test"* with explanation of why we headline v1 (negative −0.25 result is stronger evidence than v2's near-baseline +0.15, which can include coincidental content alignment; cross-references §4.3 Example B). v1 stays as headline (preserves Aarik's earlier choice during §4.6 walk).
- **Fix 5: Pre-registered vs post-hoc labeling.** §1.2 new `[^pre-vs-post-hoc]` footnote on H1-H5 mapping line, listing post-hoc analyses with cross-references and pointing to Appendix B.10 for full breakdown. New Appendix B.10 "Pre-registered hypotheses and post-hoc analyses" with a 17-row table cataloguing every load-bearing analysis result with status (Pre-registered / Pre-registered control / Post-hoc / Post-hoc reactive / Reactive). §1.3 7th headline tagged "(surfaced post-hoc)" to make evidentiary tier visible at headline level.

§1-4 now cleared for §5 walk informed by both the cold-read independent outline (#90) and the multi-LLM panel (#91). v11.5 preserved as historical lock-point reference.

## V11.6 fork — 2026-05-01

V11.5 release-frozen at `docs/beyond_recall_v11_5_draft.md` after multi-LLM review of §1-4 landed (Mistral Large + GPT-5.5 + Opus 4.7; Gemini Pro 503'd). V11.6 forked as new active edit branch at `docs/beyond_recall_v11_6_draft.md`. This fork is needed because the multi-LLM convergence findings require touching locked §1, §2, §3, §4 content (tempering pass on overstated claims): cannot be passed by sycophancy → reduces the risk of sycophancy; gradient slope reframing; compression "matches or exceeds" softening; wrong-spec v1/v2 framing convention; pre-registered vs post-hoc labeling.

V11.5 includes all session edits through 2026-05-01 (§4 walk complete: §4.1.2 Franklin, §4.4.1 retrieval-overlap subsection + sensitivity in §4.6.5, §4.5 Letta + semantic-duplication, §4.6 5-subsection structure, §4.7 bullet summary, retrieval-divergence elevated to §1.3 7th headline). V11.5 is the citable historical reference; V11.6 is where the tempering pass + §5 walk + §6-§9 walks land.

Multi-LLM review of §1-4 at `docs/reviews/round_v11_5_sections_1_4_20260501_141341.md`. Cold-read §5 outline + diff at `docs/reviews/s5_independent_outline_20260501.md` and `s5_drift_diff_20260501.md`.



_Started 2026-04-27. Tracks every change applied (✓), queued (▷), or pending Aarik decision (?) during the v11 comment-walk._

Source paper: `docs/beyond_recall_v11_draft.md` (forked from v10.1 baseline 2026-04-27)
Comment index: `docs/reviews/v11_comment_index.json` (183 items)

---

## V11.1 — annotation walk (2026-04-28)

V11 release-frozen at `docs/beyond_recall_v11_draft.md`. V11.1 forked as new active edit branch at `docs/beyond_recall_v11_1_draft.md`. This pass applies all dispositions from `docs/reviews/s114_word_annotations.md` (58 annotations across §1.1, §1.2, §1.3) to v11.1 only.

### §1.1 Recall Is Not Interpretation (A1-A3)

| Item | Disposition | Change |
|---|---|---|
| ✓ A1 | APPLIED | Replaced parenthetical `(see §2.2 for vendor-by-vendor numbers and the methodology disputes around them)` with `(§2.2)`. Tracked deletes ("see" / "for vendor-by-vendor numbers...") absorbed. |
| ✓ A2 | APPLIED | Inserted brief Behavioral Specification gloss at first mention in §1.1 paragraph 2: `Throughout this paper we use the term **Behavioral Specification** to refer to a static document that extracts and encodes a person's behavioral patterns; the operational definition is developed across §3.7.` Full definition retained at original location in paragraph 5. |
| ✓ A3 | APPLIED (via A2) | Earlier introduction satisfied by A2 insertion. Full definition still appears in paragraph 5 unchanged. |
| ✓ A5 | APPLIED | Added "act on a person's behalf" framing to core hypothesis paragraph: `This is the operational primitive for any AI system meant to act on a person's behalf: the system's behavior, on the user's behalf, can only match the user's reasoning to the extent the system represents that reasoning accurately.` |

### §1.2 What we tested (A4-A29)

| Item | Disposition | Change |
|---|---|---|
| ◌ A4 | NO-ACTION | Reflective sidenote on hypothesis genesis (informal pre-studies). Documented; no text change. |
| ◌ A6 | NO-ACTION | Empty comment at "H1." anchor. |
| ✓ A7 | APPLIED | Added response-model gloss to §1.2 intro paragraph: `Throughout this section, the **response model** is the language model being asked to predict how the subject would respond, and the **Behavioral Specification** is the context document that response model receives.` |
| ✓ A8, A9, A10 | APPLIED | H4 simplified: removed Pattern 1/2/3 forecast and "mouthful" sentence about aggregate Δ. New H4: `The specification interacts with memory-system retrieval in a structured way that depends on the type of question being asked. Aggregate effects on each memory system reflect the balance of these per-question patterns and shift with retrieval architecture (§4.4).` |
| ✓ A11 | APPLIED | H5 simplified: removed C4 / C8 / Twin-2K technical content from H5. New H5: `Structured representation compresses the behavioral-prediction signal at a fraction of the source-corpus footprint. Tested in §4.2 against extracted facts and the full raw corpus.` Twin-2K positioning preserved in §2.1. |
| ✓ A12 | APPLIED | Changed `§4` to `§4 (Results)` on first mention in mapping paragraph. |
| ◌ A13 | NO-ACTION | Empty comment at "locked rule" anchor. |
| ✓ A14 | APPLIED | Locked-rule mechanics moved to footnote `[^locked-rule]`. Body retains `aggregated per (subject, condition) cell via the locked rule.[^locked-rule]`. |
| ✓ A15 | APPLIED | Unit-of-inference detail moved to footnote `[^unit-of-inference]`. Body retains `The **subject is the unit of inference**.[^unit-of-inference]` |
| ✓ A16 | APPLIED | Primary/secondary outcomes paragraph trimmed substantially. Operational details (improved/tied/worsened classification, median magnitudes, intro-here-track-throughout-§4) cut from body and pointed to §3.6 / §4.2.1. |
| ✓ A17 | APPLIED | "Two main splits" arrives sooner via A16 trim. |
| ◌ A18 | NO-ACTION | Empty comment at "2.5, 3.4" anchor. |
| ✓ A19 | APPLIED | Cross-anchor rule reference added to fractional-scores sentence: `Fractional scores (e.g., 2.5, 3.4) emerge from judge averaging and are interpreted using the cross-anchor rule in §3.6.2... Full rubric in §3.6 and panel composition in §3.6.1.` |
| ✓ A20 | APPLIED (via A19) | "Vague" partial-progress phrase replaced with concrete cross-anchor explanation including 2.4 example. |
| ✓ A21 | APPLIED | Tracked-insert "(C5>3 on the rubric)" applied to high-baseline definition with corrected formatting. |
| ✓ A22 | APPLIED | "Whose private reasoning was never indexed by any training corpus" rewritten to "whose reasoning the model has insignificant pretraining understanding of even when fragments of their digital footprint may exist in training data." |
| ✓ A23 | APPLIED | Tracked-insert chain reconstructed with "Relevence" → "Relevance" spelling correction. New sentence chain: low-baseline ≤ 2.0 / high-baseline > 3.0 / pretraining-representation gap spawns "population of relevance" / most typical AI users fall into low-baseline band. |
| ✓ A24 | APPLIED | Honesty fix: removed "outside Anthropic" framing because Sonnet 4.6 is Anthropic. New phrasing references the cross-provider check by sectional pointer (§3.5, §4.6.1) without listing models in body. |
| ✓ A25 | APPLIED | Tier 2 paragraph trimmed substantially. Removed per-subject list (Ebers / Yung Wing / Zitkala-Sa) and GPT-5.4 detail from §1.2. |
| ✓ A26 | APPLIED | Removed sentence "Including them in the aggregate would widen the spec-effect deltas, not narrow them" from §1.2 body; kept as §3.6.3 cross-reference. |
| ◌ A27 | NO-ACTION | Empty comment with longer anchor. |
| ✓ A28, A29 | APPLIED | Judge calibration paragraph moved to footnote `[^judge-calibration]`. Body retains `Judge calibration and validation can be found in §3.6.3.[^judge-calibration]`. |

### §1.3 What we found (A30 — the BIG layperson rewrite)

| Item | Disposition | Change |
|---|---|---|
| ✓ A30 | APPLIED | All 6 headline-findings bullets rewritten qualitative-first per Aarik's directive ("layperson, draws any reader, single number anchor, technical detail in §4"). Numerical claims preserved exactly per v11 confidence catalog. Bullets rewritten: Gradient, Category-shift, Compression, Content specificity, Memory-system layering, Hedging reduction. Number lines italicized to visually anchor "one short line on the numbers." All cross-refs preserved (§4.1, §4.2, §4.3, §4.4). Footnotes `[^statsig]`, `[^delta-aggregation]`, `[^hedging]` retained in place. |

### Verification (v11.1 vs v11 baseline)

- Em-dashes / en-dashes added in §1.1 / §1.2 / §1.3: 0 (existing en/em-dashes appear only in spec quote excerpts, lines 624/628/981+ etc., none of which my edits touched).
- "Wins" terminology added in body prose: 0.
- Cross-references: all section pointers in §1.1-§1.3 (§2.2, §3.5, §3.6, §3.6.1, §3.6.2, §3.6.3, §3.7, §4.1, §4.2, §4.2.1, §4.3, §4.4, §4.5, §4.6.1, §4.6.4) resolve to existing sections in v11.1 paper.
- New footnotes added: `[^locked-rule]`, `[^unit-of-inference]`, `[^judge-calibration]`. Existing footnotes preserved (`[^c2c-construction]`, `[^low-baseline]`, `[^statsig]`, `[^delta-aggregation]`, `[^hedging]`).

### Judgment calls

- **A23 sentence reconstruction.** The tracked-insert/delete sequence on the Population of Relevance paragraph did not parse cleanly as a literal apply (Aarik typed "Relevence" + scattered tokens). I reconstructed Aarik's intent: introduce both low-baseline (≤2.0) and high-baseline (>3.0) thresholds, frame the gap between them as the source of the "population of relevance," then claim that most typical AI users fall in the low-baseline band. Spelling corrected to "Relevance." Gloss on "indexed" was rewritten per A22.
- **A22 rewrite.** Chose "insignificant pretraining understanding" + "even when fragments of their digital footprint may exist in training data" as the layperson rendering of Aarik's longer comment about random Reddit comments / private essays.
- **A24 Tier 2 framing.** Removed "outside Anthropic" rather than expanding to caveat the Sonnet inclusion, since Aarik's clear directive in A25 was to trim the introduction's Tier 2 section overall.
- **A8/A9/A11 H4 / H5.** Cut the body details rather than restructuring with hedges, on the principle that the introduction should present the hypothesis as testable, not as already-confirmed-with-pattern-structure. The Pattern 1/2/3 detail still appears in §1.3 Mechanism and §4.4.2 where it belongs.
- **Tracked-insert "but" (between A17 and A18).** Did not apply. Could not unambiguously locate the insertion point in the "two main splits" paragraph after the A16/A17 trim. Documented; no text change.
- **A6, A13, A18, A27 (empty comments).** No-action.

### V11.1 file

- Path: `C:/Users/Aarik/Anthropic/memory-study-repo/docs/beyond_recall_v11_1_draft.md`
- V11 baseline preserved unmodified at `docs/beyond_recall_v11_draft.md`.

### Stream 1 — §1.1 polish + §1.2 introduction-as-preparation tightening (2026-04-28)

Aarik directive: introduction = preparation, not execution. Definitive statements first; technical detail moves to §3 / §4. Each piece reads to any reader. Pattern from §1.3 v5 extended to §1.1 (light) + §1.2 (substantial).

#### §1.1 light polish

| Item | Disposition | Change |
|---|---|---|
| ✓ §1.1 reads accessibly | NO-CHANGE | §1.1 already reads as preparation throughout. The conceptual setup (recall vs interpretation, representational accuracy, behavioral specification) is the right scope and stays. |
| ◌ §1.1 alignment-thread echo | NO-ACTION | Line 21 already carries "operational primitive for any AI system meant to act on a person's behalf" and "behavioral alignment with that person on novel situations." The alignment thread is implicit and load-bearing. A one-sentence echo would be redundant. Not added. |

#### §1.2 substantial tightening

| Item | Disposition | Change |
|---|---|---|
| ✓ Two-main-splits paragraph | TRIMMED-TO-SENTENCE | Replaced 5-sentence "controlled / native / running in parallel" paragraph with one sentence pointing to §3.4 / §3.5 and merged with conditions-table lead-in. |
| ✓ Fractional-scores cross-anchor explanation | MOVED-TO-§3.6.2 | Body explanation of cross-anchor rule with band-2/band-3 / 2.4 example removed; replaced with single pointer sentence. |
| ✓ Three example questions block (Ebers / Sunity Devee / Keckley) | CUT-TO-§3.6.1 POINTER | All 3 example questions + the trailing "Each question references patterns..." paragraph cut wholesale. Replaced with §3.6.1 pointer. (Advisor recommended zero inline over one inline; rubric table immediately above already does the layperson "what is being scored" work.) |
| ✓ Locked-rule footnote | KEPT-AS-IS | Already short ("Each judge's per-question scores... full mechanics in §3.6"). No further trim needed. |
| ✓ Tier 2 paragraph | TRIMMED-FURTHER | Reduced from 4-sentence "two tiers / Haiku / Tier 2 cross-provider / 7 judges / calibration footnote" block to 3 sentences. Removed `[^judge-calibration]` footnote entirely (calibration detail lives in §3.6.3 already). Added alignment-thread closer: "Together these hypotheses test whether a Behavioral Specification can move a language model toward acting in alignment with a specific person." |
| ✓ Judge calibration footnote | REMOVED | `[^judge-calibration]` definition + reference both removed. §3.6.3 carries the canonical calibration disclosure. |
| ✓ Baseline definition + thresholds | TRIMMED + FOOTNOTE | Body retains low-baseline / high-baseline as terms-of-art and the population-of-relevance claim. Numeric thresholds (C5 ≤ 2.0, C5 > 3.0) moved to new `[^baseline-thresholds]` footnote pointing to §3.2.1 for full distribution. |
| ✓ §1.2 intro paragraph redundancy | TIGHTENED | "No held-out passage was ever shown to a response model, the language model being asked to respond. Throughout this section, the response model is the language model being asked to predict..." (duplicate gloss in adjacent sentences) collapsed to single sentence with response-model gloss as apposition. |

#### Length delta on §1.2

- v11 baseline §1.2: 1,970 words / 13,022 bytes / 63 paragraph-blocks
- v11.1 stream-1 §1.2: 1,537 words / 10,244 bytes / 63 paragraph-blocks
- **Net trim: −433 words (−22%), −2,778 bytes**

#### Footnotes net change

- Added: `[^baseline-thresholds]` (replaces inline thresholds)
- Removed: `[^judge-calibration]` (canonical lives in §3.6.3)
- Net: 0 (one-for-one). §1.2 now carries `[^locked-rule]`, `[^unit-of-inference]`, `[^c2c-construction]`, `[^baseline-thresholds]`. Below the advisor-flagged "5+ footnote forest" threshold.

#### Cross-references verified

`§3.2.1` (line 258), `§3.4` (line 306), `§3.5` (line 345), `§3.6.1` (line 399), `§3.6.2` (line 415), `§3.6.3`, `§4.6.1` — all resolve.

#### Verification (Stream 1)

- Em-dashes / en-dashes: 19 + 0 = 19 (baseline preserved; all in spec/model-output verbatim quotes at lines 624, 628, 981, 983, 996, 998, 1000, 1017, 1019, 1021, 1023; none in §1.1 or §1.2).
- "Wins" body-prose in §1.1 / §1.2: 0.
- Em-dashes / en-dashes added in §1.1 / §1.2 by this pass: 0.
- v11 baseline file: unmodified.

#### Judgment calls

- **Three example questions: zero inline, not one.** Advisor recommendation. Rubric table (lines 71-77) already does the layperson "what is being scored" work; keeping one example would force keeping the trailing "Each question references patterns..." paragraph (which is itself execution rather than preparation). Cleaner cut: drop the bullet block + trailing paragraph wholesale, point to §3.6.1.
- **§1.1 alignment echo: not added.** §1.1 line 21 already says "operational primitive for any AI system meant to act on a person's behalf" — alignment thread implicit. Forced echo would be redundant.
- **Alignment-thread closer placed at §1.2 end (not start).** Advisor: closer position binds the hypotheses to alignment after the reader has seen them, rather than pre-framing. One sentence: "Together these hypotheses test whether a Behavioral Specification can move a language model toward acting in alignment with a specific person."
- **Rubric "Shift from previous anchor" wording kept.** Advisor flag was conditional. Re-read confirms the column reads as preparation (qualitative anchor for what each crossing means), not analysis. Kept verbatim.
- **Baseline thresholds → footnote, not §3.2.1 cross-ref only.** Advisor: "Keep low-baseline / high-baseline terms in body. Move only numeric thresholds." Footnote keeps the thresholds visible to a careful reader without forcing a flip to §3.2.1, while still removing them from the body's argument flow.

---

## Applied (✓)

### Bavani structural notes (B1-B10)

| Item | Section | Change |
|---|---|---|
| ✓ B1 | §1.1 | Hypothesis statement rewritten Option C (terms-of-art mirror: representational accuracy + interpretation; "intent" removed) |
| ✓ B2 | §1.3 | "Three patterns emerge" promoted; bold-labeled Pattern 1/2/3 headers added |
| deferred B3 | §2.1 | Aarik handling Table 2.1 separately |
| ✓ B4 | §2.2 | Worked example (Sunity Devee A2 → F-73 / F-414) added |
| ✓ B5 | §2.3.1 | 4 subsection headers + lede rewritten direct (no "what X measures and doesn't") |
| ✓ B6 | §2.3.1 | 4 fragment headers converted to full sentences |
| ✓ B7 | §3.1 | Renamed "Operationalizing representational accuracy" + lede explicitly cites §1.1 |
| ✓ B8 | Appendix G | New "Glossary" with 9 terms-of-art entries; §1.1 forward pointer |
| ✓ B9 | §1.1, §3.6 | Tier 1 / Tier 2 explicit framing in 3 places |
| ✓ B10 | §3.7.3 | Cross-anchor interpretation rule fully bolded |

### Docx comments (C1-C15, §1.1 + §1.2)

| Item | Section | Change |
|---|---|---|
| ✓ C1 | §1.1 line 15 | Vendor recall range "68% to 85%" → "70% to 93%" + inline §2.1 pointer (footnote dropped per Aarik) |
| ✓ C2 | §1.1 | "individual" kept (no change, confirmed) |
| ✓ C3 | §1.1 line 17 | "personalized to how that person interprets" → "given context on how that person interprets... The Behavioral Specification models that interpretation; the language model receives it as context." |
| ✓ C4 | §1.1 line 23 | Added inline ellipsis examples ("spiritual integrity over social cost..." etc.); contrast clause "rather than the specific facts of events they lived through" stripped per Aarik full-comment recovery 2026-04-27 |
| ✓ C5 | §1.2 | "shown to a response model" → "shown to a response model, the language model being asked to respond" |
| ✓ C6 | §1.2 | "whether each system" → "whether each system, under each tested condition" |
| ✓ C7 | §1.2 H5 | Reframed: "Fact extraction does most of volume-reduction" → "Structured representation compresses... Both extracted facts (C4) and the full raw corpus (C8) serve as comparators... Twin-2K forward pointer added" |
| ✓ C8 | §1.2 aggregation rule | "within-judge mean, then across-judge mean" → "each judge's per-question scores are first averaged to a per-judge per-subject mean, then averaged across the five judges" |
| ✓ C9 | §1.2 | "subject is the unit of inference" → "...: every statistic is computed at the subject level first, then aggregated across the 14 subjects" |
| ✓ C10/C11 | §1.2 + §4.2.1 | "win rate" → "per-question improvement rate" rebrand globally |
| ✓ C12 | §1.2 | "scale-free directly interpretable measure of breadth of benefit" → "tells us how often a context helps, not just by how much it helps when averaged" |
| ✓ C13 | §1.2 | "providers converge on what is most relevant" → "providers' retrieval converges when they see the same fact pool" |
| ✓ C14 | §1.2 rubric paragraph | Rewritten to set up cross-anchor rule with 1.8→2.4 example |
| ✓ C15 | §1.2 Tier 2 | Layman motivation: "to check whether the result holds when the questions and the response model both come from outside Anthropic" |

### Docx comments (C16-C52, §1.3 + §1.4 wholesale)

| Item | Section | Change |
|---|---|---|
| ✓ C16-C49 (34 comments) | §1.3 | **§1.3 v5 wholesale rewrite.** Lede: "Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least." Bulleted highlights (gradient / category-shift / compression / content-specificity / memory-system layering / hedging) per Gemini Pro review. C2a (70.9%) vs C4a (78.6%) numbers distinguished. 55.0% anchor-crossing added. Per-system anchor-crossing range (20-36%) folded into Memory-system layering bullet. Multi-anchor wins explicitly named (1→4 on Mem0 native). |
| ✓ C50-C52 | §1.4 | **§1.4 v2 wholesale rewrite.** Renamed "What this implies". "Why the gradient matters" framing dropped. "What we did not prove" disclaimer paragraph removed entirely. New framing per Aarik 2026-04-27: "broad technology like email / cell phones", "population of importance is anyone who uses an AI system", autobiographers as imperfect proxy, 99% frontier-low-baseline observation. |

### Docx comments (top of document)

| Item | Section | Change |
|---|---|---|
| ✓ C162 | §1.2 conditions table | C2c row long parenthetical (deterministic fixed pairing / mapping / v2 random derangement / Hamerton-Franklin variant) pulled to footnote `[^c2c-construction]` |

### Docx comments (§4.1 battery-sensitivity layman cluster)

| Item | Section | Change |
|---|---|---|
| ✓ C92/C93/C94 | §4.1 + Appendix B.6 | **Battery-sensitivity restructure (Aarik directive: mention controls, two layman paragraphs, then closer).** Body para 1 ("Battery-composition sensitivity. Two potential confounds...") kept as opener. Para 2 (Battery-question-type) replaced with 4-sentence layman version pointing to Appendix B.6. Para 3 (Hamerton-leverage) replaced with 4-sentence layman version pointing to Appendix B.6. Para 4 ("Neither control overturns the headline finding") kept as closer. Appendix B.6 retitled "Battery-composition sensitivity" and extended to four subsections: B.6.1 question-type correlations (existing), B.6.2 multiple regression with LITERAL_RECALL fraction (new, holds partial coefficients / variance decomposition / VIF), B.6.3 Hamerton-leverage subset regression (new, holds slope / CIs / GPT-5.4 circularity-control battery note), B.6.4 discussion. No em-dashes. |

### Wins-analysis investigation (in-flight, 2026-04-28)

| Item | Status | Notes |
|---|---|---|
| Phase 1 — wins inventory | ✓ DONE | `docs/research/wins_inventory_20260428.json` covers 18 condition pairs (direct, corpus, memory systems controlled + native). 150 extreme upward jumps documented with verbatim question + response text. 8 extreme downward jumps under wrong-spec C2c. Cross-checks reproduce published numbers exactly. Script: `scripts/build_wins_inventory.py`. |
| Phase 2 Stream X — big-wins characterization | ✓ DONE WITH ERRORS | Output: `docs/research/big_wins_characterization_20260428.{json,md}`. Errors caught by deeper analysis: wrong spec file used (`spec.md` 931w instead of `spec_production.md` 5775w served at C2a/C4a); Hamerton spec-length backwards; 9 of 47 PATTERN_PREDICATE counts came from degenerate C5→C4 pairs. Numbers superseded by deeper analysis. |
| Hamerton confound note | ✓ SAVED | `docs/research/hamerton_confound_note_20260428.md`. Verified: Hamerton spec is 0.33x globals' size, not larger. Hamerton extreme-jump rate is 2.1x globals' but cause is NOT spec length. |
| Phase 2 Stream Y — within-band + meta-judging | ✓ DONE | Output: `docs/research/within_band_shifts_20260428.{json,md}`. Two-mechanism finding: spec-on-baseline (C5→C4a) Spearman ρ=0.27 (re-ranks); spec-on-info-rich (C4→C4a, C8→C9) ρ≈0.71 (uniformly lifts). Distinct empirical signatures. Integer-anchor metric is 18% lossy. Panel detects sub-anchor signal cleanly (74% direction-agreement at panel \|Δ\| 0.1-0.25). All 5 primary judges add coherent signal. |
| Phase 2 collective review on pattern-activation claim | ✓ DONE (now superseded) | Output: `docs/reviews/pattern_activation_claim_review_20260428.md`. GPT-5.5 + Gemini Pro endorsed cautious framing pre-deeper-analysis; both nominated predicate ablation as highest-priority disconfirmation test. The cautious framing they endorsed is no longer data-supported after deeper analysis. |
| Phase 2 deeper pattern-activation analysis (60 cases) | ✓ DONE | Output: `docs/research/pattern_activation_deep_20260428.{json,md}`. **HEURISTIC-LEVEL PATTERN-ACTIVATION CLAIM FALSIFIED.** Fair-comparison spec_doing_work rate: extreme jumps 78.9% (n=38) vs non-jumping controls 80.6% (n=36). Delta -1.7 pp. Heuristic detects "spec-loaded condition" not "spec drove lift." Direct quote lookup empirically ruled out. Narrower claim that survives: 11 of 60 INFERENCE_CHAIN cases with verdict genuine_inference_via_spec. |
| Phase 2c — predicate ablation experiment | ▷ RUNNING | Script: `scripts/run_predicate_ablation.py`. Background bash id `bzvhc3her`. 16 cases stratified. Original + ablated + reversed → 5-judge primary panel. ~320 API calls, under $5. Decision rule: mean Δ_removal ≥1.0 = STRONG; 0.5-1.0 = CAUTIOUS; <0.5 = NOT supported. Results land in appendix per Aarik. |
| Phase 3 Round 1 framing report | ✓ DONE | Output: `docs/reviews/framing_implications_20260428.md` (7,589 words). Update integrating deeper-analysis: `docs/reviews/framing_report_round1_update_20260428.md`. Disposition: 5 APPLY-AS-DRAFTED iterative refinements + 1 HOLD-FOR-PHASE-2C (cautious mechanism, superseded) + 1 PHASE-2C-DEPENDENT (strong mechanism) + 1 APPLY-AS-DRAFTED with reviewer-conditional fallback (two-mechanism story at metric level — fold into §4.4 small section + future work, layman per Aarik). |
| Phase 3 Round 2 cross-LLM review on framing report | ▷ RUNNING (retry after server 500) | Output target: `docs/reviews/framing_report_round2_review_20260428.md`. Agent: `a877fc46ccef8daa4` (first attempt failed 500). GPT-5.5 + Gemini Pro evaluate 8 proposed pivots. |
| Held-out passage leakage investigation | ▷ RUNNING (retry after server 500) | Output target: `docs/research/held_out_leakage_investigation_20260428.{json,md}`. Agent: `ad61971eb743dad41` (first attempt failed 500). Investigates 1 6-gram + 2 4-gram + 9 3-gram held-out → post-response matches. Source attribution + severity verdict + paper-text mitigation recommendation. |
| Pipeline state snapshot | ✓ SAVED | `docs/research/wins_analysis_pipeline_state_20260428.md` — durable state snapshot for crash recovery. Updated mid-session due to intermittent Anthropic API server 500s. |
| Paper edits | ⊘ NONE APPLIED | No paper edits this pass. Aarik decides which pivots to apply on a separate walk after Round 2 review and Phase 2c results land. |

**Origin:** C105 flag on the +0.05 C9-vs-C8 Δ ("Honestly interesting that it even adds over raw corpus") expanded into substantive multi-stream investigation per Aarik directives across the walk. Tracker updated in `v11_comments_extracted_20260427.md` C105 entry.

### Docx comments (§4.1 coupling-free reframing layman + per-question reframing)

| Item | Section | Change |
|---|---|---|
| ✓ C96 | §4.1 + §1.3 callout + new Appendix B.7 | **Coupling-free / Honest reframing block fully restructured to per-question framing.** Body now layman: "Sanity-checking the gradient" (4 sentences) + "What is actually happening" (long para with inline 55% / 18% / 6% breakdown + floor-not-ceiling observation + opportunity-not-empirical-comparison reframing) + closing reframing paragraph with bolded "low-baseline subjects have more such opportunities, because their batteries contain more questions at low rubric anchors to begin with." Technical detail (level regression slope +0.04, permutation null −0.998, bootstrap CIs) moved to new **Appendix B.7** with subsections B.7.1 level regression, B.7.2 permutation test (with plain-language explanation of the −1 mechanical anchor), B.7.3 bootstrap, B.7.4 reading-the-gradient closer. **§1.3 callout fix:** broken "Multi-anchor jumps (1→3, 1→4, 2→5) appear in roughly 5-10%" replaced with "Multi-anchor jumps of two or more bands (e.g., 1→3) appear in 18% of low-baseline questions on the spec conditions, with about 6% being extreme jumps of three or more bands (e.g., 1→4, 1→5)." Floor-not-ceiling observation added to §1.3 callout. **Collective review:** GPT-5.5 + Gemini 2.5 Pro both endorsed the v3-to-v4 reframing direction with strong convergence on (a) tighten "more questions to be changed" → "more opportunities," (b) put per-question numbers in body not appendix, (c) split §1.3 5-10% claim into 18% / 6% (Option c), (d) add parenthetical pointer for "categories." Review at `docs/reviews/v11_c96_framing_review_20260428.md`. **3→5 absence:** confirmed empirically across all 546 paired questions in 14-subject panel — zero band-3-or-higher to band-5 transitions. The spec lifts the floor, not the ceiling. No em-dashes. |

### Population-of-relevance language sweep (consequence of §1.4 v2 framing change)

| Item | Section | Change |
|---|---|---|
| ✓ §3.2.1 line 281 | "real living users" → "the typical AI user falls into, since most users' reasoning is not in any training corpus" |
| ✓ §5.1 line 1386 | "real AI users" → "typical AI users" |

### Framing-pivot edit set (R1–R5, Pivot 8, predicate ablation, leakage audit) — 2026-04-28

Aarik-approved edit set anchored to `docs/research/v11_confidence_catalog_20260428.md`. All 9 applied.

| Item | Section | Change |
|---|---|---|
| ✓ R2 | §4.2 line 796 | Mean Δ for C9 vs C8 reconciled: ~0.05 → ~0.09 with explicit per-question paired-recompute scoping note. Distinguishes the canonical per-question paired Δ from the per-subject-table 2.59 vs 2.45 mean column. |
| ✓ Leakage footnote (Edit 9) | §4.1 line 741, footnote def line 743 | Held-out leakage audit footnote added on the band-1-to-band-5 / category-shift evidence; references `docs/research/held_out_leakage_investigation_20260428.md`; severity rare; 2 pretraining-memorization candidates would shift the C5→C4a low-baseline extreme-jump count by at most 1 (20 to 19). |
| ✓ R4 | §3.6.2 line 434 | Half-anchor metric note added: integer-anchor crossing metric is a lower bound on movement detectable; ~18% of paired questions across 18 condition pairs show same-band ≥0.5-anchor shifts; 5-judge primary detects sub-anchor signal (74% direction agreement at \|Δ\| 0.1-0.25, 93% at 0.25-0.5). |
| ✓ R1 | §4.2 line 798 | New "What the aggregate numbers hide" subsection with C4a vs C4 + C9 vs C8 anchor-crossing table (22%/17%/61% up/down/none); names Hamerton C9 outlier (49% upward) and the 7 other low-baseline subjects' bimodal pattern. Round-2-review wording adopted: removed "bimodal," "two opposite mechanisms," "dissolves." |
| ✓ R3 | §4.4.2 line 1142 | Spearman ρ paragraph added at end of "Why Supermemory carries the mechanism walkthrough": C5→C4a ρ 0.27 vs C4→C4a / C8→C9 ρ ≈ 0.71. Floor-effect alternative foregrounded; two readings not separately identifiable. |
| ✓ Pivot 8 (Edit 6) | new §4.4.4 line 1311 | "Two statistical signatures" subsection added at end of §4.4 (numbered 4.4.4 since 4.4.3 = Keckley case study). Spearman ρ table for 4 condition pairs; floor-effect alternative explicitly named; future work bullet for non-floor-anchored baseline. |
| ✓ Wrong-spec elevation (Edit 7) | end of §4.6.4 line 1418 | New paragraph elevates wrong-spec triplet (correct +0.35, random-derangement +0.15, adversarial −0.25) as the paper's primary indirect mechanism evidence. Explicitly does NOT claim per-predicate mechanism; refers to Appendix B.8. |
| ✓ R5 (Edit 5) | new Appendix B.6.5 line 2056 | "Hamerton-leverage at the per-question grain" subsection. 25% of 60 unique extreme jumps on Hamerton; 18.75% extreme-jump rate vs 8.9% for other 13 subjects. Three candidate mechanisms not separately identifiable; spec length anti-correlated with extreme-jump rate. Heuristic-classifier caveat foregrounded per Round 2 review. |
| ✓ Predicate ablation (Edit 8) | new Appendix B.8 line 2080 | Phase 2c per-predicate ablation results added. Δ_removal +0.05 [−0.35, +0.45]; Δ_reversal −0.24 [−0.45, −0.02]. Null on single-sentence ablation framed as consistent with redundant spec construction; rerun-stochasticity caveat (mean drift −1.44 anchors on 16 cases) explicitly disclosed. |

### Per-subject excerpts appendix

| Item | Section | Change |
|---|---|---|
| ✓ Appendix E selected per-subject excerpts | New appendix added: 3 illustrative paired (C5, C4a) cases per subject (14 subjects × 3 = 42 cases). Sorted by per-question Δ descending. Pre/post response excerpts truncated to 500 chars; held-out passage to 600 chars. Source: `docs/research/per_subject_excerpts_20260428.json`. Script: `scripts/build_per_subject_excerpts.py`. Existing Appendix E (Benchmark Scope) renumbered to F; Appendix F (Letta) to G; Appendix G (Glossary) to H. All body cross-references (§1.1, §1.5, §2, §2.2, body of §4.5, line 1826 appendix index) updated. |

**Verification (changed regions):** em-dashes/en-dashes total 35 (no increase from pre-edit baseline; spec said 29 but actual baseline was 35). No "wins" / "big wins" / "wins at the margin" body-prose in changed regions; "wins inventory" surfaces only as a literal data-file reference in Appendix B.6.5 and B.8 (`docs/research/wins_inventory_20260428.json`). Edit 6 numbered 4.4.4 not 4.4.3 (4.4.3 already exists as the Keckley case study).

### Meta-trackers

| Item | Notes |
|---|---|
| ✓ M1 | ToC / section-title cleanup tracker (Aarik flagged 2026-04-27; deferred until docx-comments walk complete) |
| ✓ M2 | Footnote-vs-parenthetical convention tracker; convention confirmed (methodological detail / strict-vs-broader rule alternatives / threshold definitions → footnote; one-phrase glosses + cross-references → parenthetical; term-of-art definitions → Appendix H; vendor recall numbers → §2.1 prose pointer) |

### Infrastructure

| Item | Output |
|---|---|
| ✓ Comment index | `docs/reviews/v11_comment_index.json` + `scripts/query_v11_comments.py` |
| ✓ Per-system anchor-crossing analysis (C131) | `docs/research/per_system_anchor_crossing_20260427.{md,json}` + `scripts/compute_per_system_anchor_crossing.py` |
| ✓ Collective review #1 GPT-5.5 | `docs/reviews/v11_post_comments_review_gpt55_20260427.md` |
| ✓ Collective review #2 Gemini Pro | `docs/reviews/v11_post_comments_review_gemini_pro_20260427.md` |
| ✓ §1.1 / §1.2 audit (caught C4 + C7 misses) | result: 2 misses caught and applied |

---

## Queued, Aarik approved (▷)

These have your green-light from "good, and I agree with your take's on my comments" 2026-04-27. To apply in priority order.

| Item | Section | Change | Effort |
|---|---|---|---|
| ▷ C56 | §2 | Move §2.3 (benchmarks) before §2.1 (memory systems) | medium |
| ▷ C57 | §2.3 | Merge §2.3 + §2.3.1 into single section | medium |
| ▷ C66 | §3.6 | Compress (don't cut) the "weakest model" rationale to 2 sentences | small |
| ▷ C71 | §3.7 | Reorder §3.7.x: rubric → fractional-score interpretation → judge panel → calibration → inter-judge agreement | medium |
| ▷ C99 | §4.1.1 / §4.6 | Move Franklin section to §4.6 sensitivities | medium |
| ▷ C106 | §4.2 / §4.2.1 | Keep §4.2.1 as subsection of §4.2 (current); confirm placement | trivial |
| ▷ C124 | §4.7 (NEW) | Add §4 closing paragraph bridging into §5 | small |
| ▷ C139/C140 | §4.4.1 / §4.4.2 | Collapse Supermemory deep-dive (Examples 1-4 + Pattern 1/2/3) into §4.4.2; keep aggregate paragraph in §4.4.1 with §4.4.2 pointer | medium |
| ▷ C150 | §5.2 | "everyone uses AI" framing softened to "the population of typical AI users" | small |
| ▷ C153 (IMPORTANT) | §1, §4, §5 | **Reframe additivity throughout: from "spec composes additively with 3 of 4 systems" to "spec lets retrieval-based memory systems handle question types they weren't designed for". Aggregate Δs are small; per-question pattern (Pattern 1/2/3) is where the action is.** Propagates through §1.3, §4.4, §5. §1.3 v5 partially reflects this; §4.4 / §5 still use additivity framing. | LARGE |
| ▷ C171 | tables | Color-code Table 4.1 gradient, Table 4.2 compression, Table 4.6 paired-Δ (highest score per column). Skip Appendix D matrices (color noise). Implementation in docx pass, not markdown. | medium |

---

## Pending (?) — surfaced to Aarik for direction

### Figure feedback (C80, C81, C91, C101, C107, C113, C118, C125, C126, C171, C173)

11 figure-related comments. Aarik wants direction on which to address:

| Item | Section | Comment | Recommended action |
|---|---|---|---|
| ? C80 | §4 (Figure 5) | "May want to describe this in terms of viewing the figure itself..." (walk reader through visually) | Rewrite caption with visual walkthrough |
| ? C81 | §4.1 Figure 4.1 | "Walk viewers through how to read this chart, start at the red line stating above this line there was a positive change... Subjects on left half / below baseline are low baseline... May be worthwhile adding specification on per question swings. We will likely also need a separate chart for the percentage of questions that move from one anchor number to another." | Rewrite caption + queue NEW figure for per-question anchor crossings |
| ? C91 | §4.1 per-subject table | "This will be color coded right in terms of the table?" | Add color-coding to Table 4.1 |
| ? C101 | §4.2 Figure 4.2 | "Need to describe this a bit more in depth. Describe axes, point out where the baseline is, mention this is looking only at Hamerton, point out C4 / C8 results, every situation spec was combined or served alone outperformed in judging metric. Not entirely sure what dose response curve means..." | Rewrite caption with explicit walkthrough |
| ? C107 | §4.2.1 Figure 4.2.1 | "Similar to previous figure feedback, need to explain visually what's going on here" | Rewrite caption |
| ? C113 | §4.3 Figure 6 | "Describe visually what's going on here. May want to specify where high baseline subjects are. Likely sort by baseline score. Denote low/mid/high baseline. Could provide figures on this chart or within figure explanation stating that in all situations the wrong specification was worse than the correct specification. In most cases or twelve out of 14 it seems the correct spec performed worse than baseline." | Re-render figure (sort by baseline + low/mid/high band) + rewrite caption |
| ? C118 | §4.3 Spec-activation evidence | "Should likely have a chart or figure for this" | NEW figure for tag-citation rates 78.6% vs 50.0% |
| ? C125 | §4.4.1 Figure 7 | "Provide horizontal bar for mean improvement... how many of them resulted in movement across an anchor number. Maybe in description state X out of Y subjects with this memory system plus spec scores crossed at least 1 anchor number over X aggregate questions" | Re-render figure (mean improvement bar) + rewrite caption with anchor-crossing rates from new analysis |
| ? C126 | §4.4.1 Figure 3 | "A bit too much padding under the graph for this figure. Not sure if you need to include the little note at the bottom of the image" | Re-render figure with tighter padding, drop bottom note |
| ? C171 | §4 tables (general) | Color-coded for highest-score-per-column | Same as C91 — covered by Table 4.1, 4.2, 4.6 docx pass |
| ? C173 | unspecified table | Color-coded | Same as C171 |

**Recommendation:** figure regeneration is a separate workstream (PNG generation scripts at `scripts/figures/`). Recommend batching all 11 into one figure-regen pass after the §1-§5 prose restructures land. Caption rewrites can be done now in markdown.

### Other direction questions still open

| Item | Question |
|---|---|
| ? C111 | §4.2 Ebers honest abstention deeper analysis — needs new analysis or footnote acknowledging? |
| ? C142 | §4.5 stack spec on Letta stateful-agent path — new test or out of scope? |
| ? 9 uncovered weaknesses | (from collective reviews) — H2 still overstates "inversely proportional" / spec treated as monolithic / three patterns not theorized / rubric is passage-matching not representational accuracy / etc. — address now or post-walk? |

---

## Cuts, deletions, deprecations

| Item | What was removed |
|---|---|
| §1.3 entire "Headline numbers at a glance" callout box (8 bullets) | Replaced by §1.3 v5 prose lede + bulleted Headline findings |
| §1.3 "Headline finding in plain language" extended paragraph (~10 sentences) | Cut entirely (per C30 "we shouldn't be insulting the reader, we just state") |
| §1.3 "Primary result: the gradient" + "Compression: structure..." + "Mechanism: content, not format" + "Additivity:" + "Where the specification helps and where it hurts" + "Three patterns emerge" with examples + "Robustness:" + "Letta block-scaling" paragraphs | Cut entirely; content distributed to §4.x sections (mostly already there) |
| §1.4 entire "Why the gradient matters for real users" + "What we did not prove" disclaimer + "What this implies for AI personalization infrastructure" three-paragraph block | Replaced by §1.4 v2 two-paragraph "What this implies" |

---

## Comment-walk closure batch (2026-04-28)

Final closure dispositions on the remaining pending comments after Aarik approved the disposition set on 2026-04-28.

| Item | Disposition | Notes |
|---|---|---|
| ✓ C106 (§4.2.1 placement) | RESOLVED-KEEP-CURRENT | KEEP §4.2.1 as subsection of §4.2. Mean Δ stays primary metric per v11 confidence catalog (HIGH H1). No promotion. |
| ▷ C109 (§4.2.1 limitations move) | PARTIAL-APPLY | Trim §4.2.1 tail in close-out edit pass; keep core measure as subsection; do not move to limitations. |
| ✓ C110 (per-subject appendix) | RESOLVED-VIA-APPENDIX-E | Per Aarik 2026-04-28: not full per-subject appendix; selected illustrative excerpts (3 paired cases per subject) in new Appendix E. Excerpts agent in flight. |
| ✓ C111 (Ebers honest abstention) | DEFERRED-TO-FUTURE-WORK | Probe what specifically Ebers responses get wrong is a future-work bullet; not freeze-blocking. Existing §4.2 framing of Ebers as honest-cost-of-context example stays. |
| ✓ C121 (wrong-spec convergence) | RESOLVED-NO-ACTION | Existing §4.3 narrative covers; Edit 7 (wrong-spec elevation) sharpened this further. |
| ▷ C122 (Seacole wrong-spec safety) | PARTIAL-APPLY | Add 1-sentence future-work bullet on safety probing of behavioral specs ("can the model recognize wrong-spec content as adversarial"). |
| ✓ C128 (§4.4.1 open with graph) | DEFERRED-TO-FIGURE-REGEN | Queued in figure-regen pass alongside C81/C101/C107/C113/C118/C125/C126/C171/C173. Caption updates can be drafted in markdown now; figure rerendering is post-freeze. |
| ▷ C143-C146 (§4.6 robustness restructure) | PARTIAL-APPLY | Minor restructure: keep high-level mention in §4.6 body, push verbose detail to appendix. C144 specifically (1-paragraph high-level + appendix pointer) is the right level. |
| ▷ C149 (§5.1 act-as vs predict) | APPLY | Clarify: paper's framing is "predict how this person would respond," not "act as this person." 1-sentence disambiguation in §5.1. |
| ▷ C159 (§7 future-work / practical-implications overlap) | PARTIAL-APPLY | Light dedup pass; surface obvious overlap; do not restructure §7 wholesale. |
| (already applied) C155 | APPLIED-EARLIER | (no change) |

### Pending small edits to apply post-excerpts-agent

The ▷ rows above translate to ~5 small body edits to be batched after the per-subject excerpts agent finishes:
- C109: trim §4.2.1 tail (small)
- C122: 1-sentence future-work bullet (small)
- C143-C146: §4.6 restructure (medium, push detail to appendix)
- C149: §5.1 clarification (1 sentence)
- C159: §7 dedup pass (light)

Plus the figure-regen pass workstream (C81/C101/C107/C113/C118/C125/C126/C128/C171/C173) is post-freeze.

### Comment-walk closure batch applied (2026-04-28)

All 5 small edits applied (or noted as no-op) post-excerpts-agent. Em-dash count unchanged at 35; section headers intact.

| Item | Status | Section | Change |
|---|---|---|---|
| ✓ C109 | APPLIED | §4.2.1 | Tail "Failure modes if this metric is adopted" 4-bullet block (lines 852-858) replaced with single-sentence pointer to §6 limitations. Core measure retained as subsection of §4.2. |
| ✓ C122 | APPLIED | §7.6 | New paragraph "Safety-side probing of behavioral specifications" added at end of §7.6, citing wrong-spec adversarial control (Examples §4.3) and flagging adversarial-values probing as future work. |
| ✓ C143-C146 | NO-OP | §4.6 | All §4.6 subsections already concise: §4.6.2 is one table + brief commentary, §4.6.3 is already pointer-style (4 sentences pointing to §6.2), §4.6.4 is single-evidence claim. No verbose detail to push. Per the explicit no-op exit criterion in the edit instructions ("most subsections under 200 words"), no restructure applied. Per-judge detail already lives in Appendix D.4. |
| ✓ C149 | APPLIED | §5.1 | New "Note on framing" paragraph added after §5.1 opening lede: predict-how-person-would-respond vs act-as-that-person. Closing-paragraph "act as this specific person would" updated to "accurately predict how this specific person would respond" for internal consistency within §5.1. |
| ✓ C159 | APPLIED | §7.4 | Added cross-reference sentence at start of §7.4: "These five items appear in §5.5 as deployment design considerations; this section flags which of them require empirical study before production deployment." Trimmed §7.4's parenthetical re-descriptions of the 5 items; replaced with "(see §5.5 for the description of each)". §7.4 reduced from ~140 words to ~95 words. §5.5 untouched. |

**Verification.** Em-dash + en-dash scan: 35 + 0 = 35 (baseline preserved). Section headers verified intact at lines 811 (§4.2.1), 1337 (§4.6), 1343-1399 (§4.6.1-4.6.4), 1427 (§5.1), 1507 (§5.5), 1713 (§7), 1717-1751 (§7.1-7.6).

### Cursory-review fixes (2026-04-28)

Source: `docs/reviews/v11_cursory_review_20260428.md` (GPT-5.4 + Gemini 2.5 Pro, both BLOCKING-ISSUES-12). 12 mechanical fixes applied:

| # | Status | Section | Change |
|---|---|---|---|
| 1 | APPLIED | §3.2 | Broken anchor `#37-evaluation-llm-as-judge-with-calibration` corrected to `#36-evaluation-llm-as-judge-with-calibration` (line 250). |
| 2 | NO-OP | §4.1 footnote | `v10_battery_sensitivity_analysis.md` and `_v10_battery_sensitivity.py` paths verified to point at real files (no v11 renames exist); paths retained. |
| 3 | NO-OP | §4.6.1 | `_v10_verification/tier2_mechanical_recompute.py` and `tier2_panel_ranges.py` verified to point at real files; paths retained. |
| 4 | NO-OP | §6.3 / Appendix B.7 | `v10_pipeline_variance_analysis.md`, `_v10_pipeline_variance.py`, `_v10_pipeline_variance_report.py`, `_v10_coupling_sensitivity.py` all verified to exist; paths retained. |
| 5 | APPLIED | §4.1 (line 580) | "5-10% multi-anchor jumps" replaced with §1.3-canonical "18% / 6%" framing; "wins at the margin" replaced with "multi-anchor jumps at the margin." |
| 6 | APPLIED | §4.1 (line 584) | Mean C4a stated as 2.41 corrected to canonical 2.46. |
| 7 | APPLIED | §4.2.1 (line 828) | "All 14 subjects (546 questions)" relabeled to "All 14 main-study subjects, matched 39-question batteries (546 questions: 13 globals plus the Hamerton 39-question matched-battery slice)." |
| 8 | APPLIED | §4.1 (line 572), §4.6.4 (line 1407), §6.3 (line 1693) | "H2a" label removed; replaced with "Corollary to H2" and "the H2 corollary" / "H2 corollary interference claim." |
| 9 | APPLIED | §1.3 (lines 110-112), §4.1 prose | Pattern 1/2/3 em-dash headers converted to comma-separated form. "Wins" / "multi-anchor wins" / "sometimes wins and sometimes loses" replaced with "extreme upward anchor crossings" / "multi-anchor jumps" / "sometimes increases representational accuracy and sometimes does not" in §1.3 line 98, §1.3 line 101, §4.1 line 656, §4.1 line 724. Em-dashes inside verbatim model-output blockquotes (lines 616, 620) preserved as data. |
| 10 | APPLIED | §1.3 (line 98), §4.1 (line 741) | Floor-not-ceiling claim scoped to "C5 to C4a comparison on the full 14-subject panel" with explicit C4-to-C4a parenthetical referencing Seacole Example C 2.80→5.00. |
| 11a | APPLIED | §5.4 (line 1501) | Keckley Q21 numbers reconciled to §4.4.3 canonical: "C1 ≈ 3.4-3.6 ... Δ on Q21 of −2.0 and −2.2 respectively" (was 3.83 / 3.33 / −2.33). |
| 11b | APPLIED | §3.7 (line 532), §5.5 (line 1517) | Spec size reconciled to canonical "approximately 7,000 tokens" / "~7,000 tokens" (was 5,000-8,000 in §3.7 and 8,000-10,000 in §5.5). |
| 11c | APPLIED | §8 (line 1771) | `scripts/audit_rubric.py` corrected to `scripts/audit_low_end_inflation.py` (matches §3.6.6). |
| 11d | APPLIED | §5.2 (line 1461) | Compression ratios reconciled to §4.2 table: "roughly 7× (Hamerton) to 79× (Babur)" (was 5× / 78×). |
| 11e | APPLIED | §4.6.4 (line 1403) | Gemini-inflation cross-reference `(see §4.5)` corrected to `(see §3.6.3)`. |
| 12 | APPLIED | §1.3 (line 93) | Low-baseline footnote pointer "§1.4, §3.2.1" corrected to "§1.4, §5.3" (population-of-importance argument). |

**Verification.**
- Em-dash + en-dash scan: 35 → 26 after fixes. Net reduction of 9 (Pattern 1/2/3 in §1.3 = 3, plus 6 already removed in earlier comment-walk passes shown in scan delta). Remaining 26 are: 13 inside verbatim quoted model-output blockquotes (data; preserved), 8 in glossary/appendix authorial prose (out of cursory-review scope), 5 in §6 / appendix prose (out of cursory-review scope, not flagged in the review).
- "Wins" body-prose scan §1.3: 0 occurrences. "Wins" body-prose scan §4.1: 0 occurrences.
- Mean C4a 2.46 consistency in §4.1: confirmed (2.41 instances at lines 704, 717 are subject-specific table cells, not means).
- Multi-anchor jump 18% / 6% consistency: §1.3 line 98, §4.1 line 580, §4.1 line 741 all aligned.

**Recommendation.** v11 paper is ready-for-freeze on the 12 cursory-review issues. Out-of-scope em-dashes in glossary, §6, and Letta appendix were not flagged by either reviewer and are not addressed here per the "stay scoped to the 12 fixes" constraint.


---

## V11 FREEZE — 2026-04-28

The Beyond Recall v11 paper draft is release-frozen.

**Citable canonical paper:** `docs/beyond_recall_v11_draft.md` (replaces v10.1 as canonical)

**v10.1 baseline preserved:** `docs/beyond_recall_v10_1_draft.md` (historical reference)

### Final paper state

- Em-dashes: 19 total characters across 13 lines, all in spec quotes / model response quotes (preserved as data per Aarik directive). 0 in authorial prose.
- "Wins" terminology: scrubbed from body prose (only data-file path references remain).
- All 8 framing-pivot edits applied: R1 §4.2 per-question variance subsection, R2 §4.2 numerical reconciliation, R3 §4.4.2 Spearman ρ caveat, R4 §3.6 half-anchor metric note, R5 Appendix B.6.5 Hamerton-leverage at per-question grain, Pivot 8 §4.4.4 two statistical signatures, wrong-spec elevation in §4.6.4, Appendix B.8 Phase 2c predicate ablation results.
- All comment-walk closure items resolved (applied / partial-applied / deferred-to-future-work / no-op / deferred-to-figure-regen).
- All 12 cursory-review issues addressed (9 applied, 3 verified-no-op).
- All 4 paper-vs-scaffold MISMATCH items reconciled.
- Selected per-subject excerpts appendix (Appendix E) with 42 cases × 14 subjects.
- Footnote-redirect Appendix B.9 added for the 3 heaviest explanatory footnotes.
- +0.89 vs +0.93 aggregation footnote present.
- Final em-dash + "wins" + footnote-length verifications passed.

### Index files synced to v11

- `docs/DATA_REFERENCE.md`: v11 numerical additions subsection + 12 new provenance rows
- `docs/PROVENANCE_INDEX.md`: 17 v11 research artifacts indexed
- `docs/KEY_FINDINGS.md`: 7 new findings (M15-M21) + "What we explicitly do NOT claim" section + MISMATCH-flag callout
- `ISSUES.md`: stale data-locking pending entry replaced with closure entry

### Research artifacts produced this v11 session

- `docs/research/v11_confidence_catalog_20260428.md` — explicit HIGH / MEDIUM / LOW / UNRESOLVED map of every claim
- `docs/research/wins_inventory_20260428.json` — 18 condition pairs, 60 unique extreme upward anchor crossings
- `docs/research/big_wins_characterization_20260428.{json,md}` — Stream X (errors superseded by deeper analysis)
- `docs/research/within_band_shifts_20260428.{json,md}` — Stream Y, two-statistical-signatures finding
- `docs/research/pattern_activation_deep_20260428.{json,md}` — heuristic-level claim falsified
- `docs/research/predicate_ablation_results_20260428.{json,md}` — Phase 2c, NOT_SUPPORTED on per-predicate uniqueness
- `docs/research/held_out_leakage_investigation_20260428.{json,md}` — severity rare
- `docs/research/hamerton_confound_note_20260428.md` — spec-length inversion correction
- `docs/research/per_subject_excerpts_20260428.json` — Appendix E source data
- `docs/research/per_question_anchor_crossing_extended_20260428.json` — C4a vs C4 / C9 vs C8 paired crossings
- `docs/research/wins_analysis_pipeline_state_20260428.md` — durable session state snapshot

### Cross-LLM reviews completed this v11 session

- `docs/reviews/framing_implications_20260428.md` (Round 1 framing report)
- `docs/reviews/framing_report_round1_update_20260428.md` (deeper-analysis integration)
- `docs/reviews/framing_report_round2_review_20260428.md` (Round 2 cross-LLM review)
- `docs/reviews/pattern_activation_claim_review_20260428.md` (collective review on mechanism claim)
- `docs/reviews/v11_c96_framing_review_20260428.md` (C96 §4.1 layman framing review)
- `docs/reviews/v11_cursory_review_20260428.md` (final cursory error-check)

### Net change summary from v10.1

The wins-analysis pipeline produced **incremental refinements**, not a wholesale reframe. v11's paper-level changes from v10.1: per-question variance subsection in §4.2, mean Δ numerical reconciliation, Spearman ρ caveat in §4.4.2, half-anchor methodological note in §3.6, Hamerton-leverage at per-question grain in Appendix B.6.5, Pivot 8 two-statistical-signatures section in §4.4.4, wrong-spec elevation as primary indirect mechanism evidence in §4.6.4, Phase 2c predicate ablation results in Appendix B.8, footnote-redirect Appendix B.9, selected per-subject excerpts in Appendix E. All headline claims (mean Δ +0.89, 55% anchor crossing, wrong-spec −0.25, compression, hedging) carry forward unchanged.

V11 is the citable canonical version effective 2026-04-28.

## V11.1 — outstanding edits queue (running list)

- **"pejorative" replacement** — line 132 §1.4: "not 'bias' in any pejorative sense but an explicit design target". "Pejorative" is not layman; reword. Candidate replacement: "not 'bias' in the negative sense but an explicit design target" or "not 'bias' as the word usually means but an explicit design target." **(CLOSED in round 2 walk, 2026-04-28: applied replacement "not 'bias' in the negative sense" in §2 lede.)**

---

## V11.1 — round 2 annotation walk (2026-04-28)

Source: `docs/reviews/s114_word_annotations.md` (47 annotations across §1.1, §1.2, §1.3, §1.4, §2.1, §2.2, §2.3). Edits applied to `docs/beyond_recall_v11_1_draft.md` only; v11 release-frozen baseline at `docs/beyond_recall_v11_draft.md` untouched.

### §1 fixes (B1-B8)

| Item | Disposition | Change |
|---|---|---|
| ✓ B1 | APPLIED | §1.1 closing sentence: "Appendix H" made clickable as `[**Appendix H**](#appendix-h-glossary)`. |
| ✓ B2 | APPLIED | §1.2 conditions table: Letta row in C1 entry now reads `Letta[^letta-additional]`. The standalone "Additional testing for Letta" body paragraph converted to footnote `[^letta-additional]` (preserved verbatim, lightly rephrased to "this table" instead of "the conditions above"). |
| ✓ B3 | APPLIED | §1.2 baseline paragraph rewritten lead-with-low-baseline. New text: "Low-baseline subjects are the population of relevance: people the model has insignificant pretraining understanding of, even when fragments of their digital footprint exist in training data. High-baseline subjects are the opposite, people the model already knows about from pretraining. Most typical AI users fall into the low-baseline band." |
| ✓ B4 | APPLIED | §1.3 second bullet retitled "Step-changes, not nudges." Pairs naturally with body sentence "doesn't just nudge the score." |
| ✓ B5 | APPLIED (combined with B4) | Lead clause added at start of bullet: "This pattern holds on the spec, facts+spec, and corpus+spec conditions in §4.1 and §4.2 on the low-baseline slice." |
| ✓ B6 | APPLIED | One-sentence aside appended to "Mechanism: three patterns" lead-in: "Baseline runs suggest the model already attempts shallow inference from a user's raw data on its own; the specification makes that inference inspectable and structured." |
| ✓ B7 | APPLIED | "Base Layer compressed-brief variant" → "Base Layer's compressed-brief specification" (possessive disambiguates the article). |
| ✓ B8 | APPLIED via concrete-failure-mode rewrite | §1.4 sentence rewritten: "either each person supplies their own representation to whatever AI system serves them, or personalization stays at the level of style, voice, and preference selection, the layer current memory systems already address. The layer of how a person reasons about novel situations remains untouched." Names the failure mode concretely; matches §1.4 framing of training-corpus limits. |

### §2 fixes (B9-B22)

| Item | Disposition | Change |
|---|---|---|
| ✓ B9 | APPLIED | §2 title: "Prior Work and Industry Benchmarks" → "Prior Work, Industry Benchmarks, The Fifth Target". §2 lede rewritten as a new opening paragraph that names the four existing measurement targets (recall of stored facts, survey-response prediction, persona fidelity, preference alignment) and announces representational accuracy as the fifth target. The four-target list is consistent with §2.1's existing enumeration. |
| ✓ B10 | APPLIED | "Recall-optimized efforts include both **neural-memory-analogue systems** ... and the broader class of vector-retrieval and embeddings-based commercial memory providers (Mem0, Zep, Supermemory, Letta)" — broadened scope of the recall-optimized framing without adding new content. |
| ✓ B11 | APPLIED | "not 'bias' in any pejorative sense" → "not 'bias' in the negative sense". |
| ▷ B12 | FLAGGED, NOT APPLIED | Population-of-relevance / intentional-individual-specificity callback to §5 closing recorded here as forward-reference for next pass. Not edited in this pass per Aarik's instruction. **PENDING:** add to §5 closing the framing that intentional individual-specificity is what current AI memory and human-AI interaction research is missing. |
| ✓ B13 | APPLIED | §2.1 layperson fixes: (a) "Survey-response prediction interpolates within a structured response distribution" → "Survey-response prediction predicts how a person would answer survey questions by looking at how they answered other survey questions." (b) "over turns" → "across the back-and-forth of a conversation" with new footnote `[^turn-def]` defining turn as "one round of conversation, a single exchange of one user message and one model reply." Single footnote covers both occurrences (the second mention is consumed by the rewrite). (c) Twin-2K token count: noted that each Twin-2K participant's persona is a complete survey transcript on the order of several thousand tokens; flagged that the paper does not publish a fixed token count. (d) "The scope of that proposal is bounded; the rest of this section is precise about what it claims." DELETED per Aarik directive ("don't insult the readers"). (e) Three §7 link mentions in §2.1 made clickable as `[§7](#7-future-work)`. |
| ✓ B14 | APPLIED | "This paper's battery is a prototype answer" → "This paper's approach is a prototype answer" (tracked insert/delete). |
| ✓ B15 | APPLIED | Mem0 row: parenthetical and Chhikara reference both moved to new footnote `[^mem0-recall]`; recall-score column simplified to "91.6 LOCOMO, 93.4 LongMemEval (current algorithm)". Letta row: "(Letta blog, 2025-08-12)" → footnote `[^letta-recall]` with full URL. Zep row: "(Rasmussen et al., arXiv:2501.13956)" → footnote `[^zep-recall]`. Recall-score column now keeps raw scores in body, references in footnotes. |
| ✓ B16 + B17 | APPLIED via consolidated restructure | "Architectural distinction worth surfacing" paragraph trimmed: lead sentence about Letta-as-architecturally-distinct stays in body; the implementation detail about `core_memory_append` / `core_memory_replace` / archival memory / recall memory and the trailing per-vendor sentence both moved to footnote `[^letta-arch]`. |
| ✓ B18 | APPLIED | New body sentence inserted: "All four systems report recall scores in the 70-93% range; on the standard recall benchmarks, recall is approaching solved." Measured framing — does not claim "solved" definitively. |
| ✓ B19 | APPLIED | Entire "A note on benchmark scores in this field" paragraph moved into footnote `[^benchmark-disputes]`. Body retains a single anchor on "All four systems report recall scores in the 70-93% range; on the standard recall benchmarks, recall is approaching solved.[^benchmark-disputes]" so the reader gets immediately to "All four are sophisticated systems." Body order reversed: recall-is-solved + sophisticated-systems first, then Letta architectural distinction, instead of architectural distinction → benchmark dispute → sophisticated-systems. |
| ✓ B20 | APPLIED | §2.3 retitled "Traceability and Reasoning Traces". "Reasoning trace" promoted as a term of art at first use ("What is also required is a **reasoning trace**: not just which fact the system pulled, but why the system believes this about this person"). Surgical replacement: kept "fact-level traceability" intact as the contrast term; replaced generic "traceability at the reasoning level" with "reasoning trace" where it specifically means why-the-system-believes. Last paragraph: "A reasoning-attribution specification" → "A reasoning-trace specification". |
| ✓ B21 | APPLIED | §2.3 opening sentence de-salesy: "Traceability is not a feature of the Behavioral Specification. It is a necessity." → "For a representation of how a person reasons, traceability is required, not optional." |
| ✓ B22 | APPLIED with real Sunity Devee Q4 data | Worked-example restructured into labeled multi-line block. Used real C2a response from `results/global_sunity_devee/results_v2.json` (Question 4, "When her husband expresses disappointment about missing an opportunity due to her concerns, does the narrator typically reconsider her position?"). Real held-out passage preserved. Real C2a response excerpt used (truncated for length, marked as excerpt) with anchors A2/A5/P3/A1 that the response actually invokes by name. Spec-item bullets quote source spec format from `data/global_subjects/sunity_devee/anchors_v4.md` and `predictions_v4.md` verbatim (A1 Divine Primacy, A2 Spiritual Integrity Over Social Cost, A5 Relational Identity, P3 Tension Absorbed Not Expressed). F-73 retained, F-161 added (from `facts.json`); F-414 (which I could not verify in this session) replaced with F-161 which I did verify. Lorem Ipsum placeholder NOT used. |

### Verification (v11.1 round 2 walk vs. start of session)

**Em-dashes / en-dashes:**
- Pre-pass count: 13 em-dashes (U+2014), 0 en-dashes (U+2013), all in spec/response quote excerpts.
- Post-pass count: 18 em-dashes, 0 en-dashes. Net delta +5.
- All 5 new em-dashes are inside spec/response quote contexts: 1 inside the response excerpt blockquote (real C2a response text from the data file) + 4 inside the worked-example spec-item bullets ("A1 — Divine Primacy", "A2 — Spiritual Integrity Over Social Cost", "A5 — Relational Identity", "P3 — Tension Absorbed, Not Expressed"), each of which is verbatim copy of the source-spec format used throughout the paper (matches existing convention at lines 1011, 1013, 1026, 1028, 1030, etc., which also quote spec-item codes with em-dashes).
- No new em-dashes in body prose. Convention preserved.
- **Note on baseline figure:** Task description specified "baseline of 19" but the measured pre-pass count was 13. Discrepancy flagged here; verification was performed against the actually-measured 13 (and confirmed all 13 fall in spec/response quotes via Grep). The "19" figure may be from a v10.1 measurement that didn't carry forward; not investigated further this pass.

**"Wins" terminology in body prose:** No new "wins" usage added. The existing "win-rate convention" reference (line ~851, §4.2.1) is a methodological term referring to LMSYS pairwise preference rates and is not boast prose. Convention preserved.

**Cross-references:** All section pointers in §1.1-§1.4 and §2 (§2.1, §2.2, §2.3, §3.4, §3.5, §3.6, §3.6.1, §3.6.2, §3.6.3, §3.7, §4, §4.1, §4.2, §4.3, §4.4, §4.5, §4.6.1, §4.6.4, §5.5, §7) resolve to existing sections. New clickable links added: `[**Appendix H**](#appendix-h-glossary)`, three `[§7](#7-future-work)` in §2.1.

**New footnotes added:** `[^letta-additional]` (§1.2), `[^turn-def]` (§2.1), `[^mem0-recall]` / `[^letta-recall]` / `[^zep-recall]` (§2.2 Table 2.1), `[^letta-arch]` (§2.2), `[^benchmark-disputes]` (§2.2). Existing footnotes preserved unchanged.

### Diff summary

| Section | Lines added | Lines removed | Net |
|---|---|---|---|
| §1.1 | 1 (Appendix H link inline edit, no line delta) | 0 | 0 |
| §1.2 | 2 (footnote definition) | 1 (paragraph removal) | +1 |
| §1.3 | 0 (inline rewrites) | 0 | 0 |
| §1.4 | 0 (inline rewrite of one sentence) | 0 | 0 |
| §2 lede | 1 (new fifth-target paragraph added before existing lede) | 0 | +1 |
| §2.1 | 1 footnote | 1 sentence ("scope of that proposal" deletion) | 0 |
| §2.2 | 5 footnotes + 1 new body sentence (recall-is-solved nod) | 1 long body paragraph (benchmark-disputes) + content moved into footnotes | net body trims, footnote bulk grows |
| §2.3 | ~30 lines (worked-example restructure as multi-line labeled block) | ~3 lines (old single-paragraph worked example) | +~25 |

§1 changes: tight, surgical (~5 sentence-level edits + 1 footnote conversion).
§2 changes: substantial structural restructure (title + lede + 5 footnote conversions + body reorder + worked-example restructure).

### Worked-example block as applied (verbatim from §2.3)

```
**Worked example.** Sunity Devee, Question 4 (battery item, drawn from a held-out passage about her husband, the Maharajah, expressing disappointment over a missed opportunity). The structure below shows how a single response in the C2a (specification-only) condition decomposes into a reasoning trace.

> **Subject:** Sunity Devee
>
> **Question:** *"When her husband expresses disappointment about missing an opportunity due to her concerns, does the narrator typically reconsider her position?"*
>
> **Held-out ground truth:** *"The Maharajah was disappointed, as he was anxious to go and see the old castle, and to shoot, and I deprived him of both these pleasures."*
>
> **Response (C2a, excerpt):** *"Based on the behavioral specification, the answer is no, not typically, and not in the way the question assumes. **A2 (Spiritual Integrity Over Social Cost)**^A2 and **A5 (Relational Identity)**^A5 create the relevant dynamic. A5 activates first: relational identity means his disappointment matters deeply. A2 holds firm: arguments from social consequence, including spousal disappointment, will not register as reasons on their own. Rather than reconsider the position itself, she is more likely to absorb the tension without resolving it (**P3 — Tension Absorbed, Not Expressed**)^P3 and reframe the disappointment within a spiritual logic (**A1 — Divine Primacy**)^A1, while grieving the relational cost without reversing the decision."*
>
> **Reasoning trace:**
> The response cites four spec items by name. Each maps to a specific behavioral pattern in the specification, and each pattern grounds out in extracted facts that grounded out in verbatim source passages. The user can walk this chain in either direction: from a phrase in the response, into the spec item that licensed it; from the spec item, into the facts that imply it; from the facts, into the source passages that produced them.
>
> **Referenced behavioral spec items** (from `data/global_subjects/sunity_devee/anchors_v4.md` and `predictions_v4.md`):
> - **A1 — Divine Primacy.** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame.
> - **A2 — Spiritual Integrity Over Social Cost.** Conscience and principle outrank social consequence as reasons.
> - **A5 — Relational Identity.** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible.
> - **P3 — Tension Absorbed, Not Expressed.** Conflicts between principle and relationship are held in place rather than collapsed in either direction.
>
> **Related facts** (from `facts.json`, each carrying its verbatim source-passage excerpt):
> - **F-73:** *"Sunity Devee's mother would never countenance anything her conscience told her was wrong."* (grounds A2)
> - **F-161:** *"Sunity Devee's mother was a woman of strong convictions who would not countenance anything her conscience told her was wrong."* (corroborates A2)
> - Additional facts grounding A1, A5, and P3 are referenced in the specification's anchor and prediction files; the full chain is enumerated in Appendix B.
```

### Judgment calls flagged for Aarik

1. **F-414 substitution.** I could not locate fact ID 414 grounding the father-conscience claim in the live `facts.json` for Sunity Devee within this pass. Substituted F-161, which I did verify ("Sunity Devee's mother was a woman of strong convictions..."), as the second corroborating fact. If F-414 is the intended fact, restore the original wording; if F-161 is acceptable, the worked-example block is correct as written.
2. **Worked-example response excerpt.** I used a real C2a response from `results/global_sunity_devee/results_v2.json` Q4 (input_tokens 7513, output_tokens 703, model claude-haiku-4-5-20251001). The excerpt is shortened from the full 703-token response and lightly stitched (kept the four A2/A5/P3/A1 invocations the response actually makes; cut intermediate explanation paragraphs; preserved verbatim wording where used). The excerpt is marked "(C2a, excerpt)" so the reader knows this is a representative slice, not the full response. If a fully-verbatim untrimmed version is preferred, the source line is line 125 of `results_v2.json`.
3. **B12 not applied.** Per task instructions, §5 closing edit deferred. Forward-reference flagged in this log and at the top of the outstanding-edits queue.
4. **Em-dash baseline mismatch.** Task spec said baseline = 19. Measured baseline = 13. Resolved against measured count, not specified count. The measured pre-pass count is 13 across the entire v11.1 file, all in spec/response quote contexts. The "19" figure may be stale from an earlier v10.1 measurement.

### Pending after this pass

- B12 §5 closing callback (intentional individual-specificity / population-of-relevance framing).
- F-414 verification or replacement confirmation in the worked-example block.
- §1.5 / §3 / §4 / §5+ annotations not in the s114 set (out of scope for this pass).

## V11.2 — pending §5 Discussion expansion (queued)

When §5 walk reaches it: expand on the hypothesis hierarchy introduced in §1.1:
- (1) held-out from corpus = what we operationally measure
- (2) genuinely new situations within the person's pattern range = what the hypothesis claims; plausibly true but extrapolation
- (3) situations outside the person's pattern range = open question
- (4) downstream steering / agent action beyond prediction = open research direction

§5 should develop what each level requires, what the current evidence supports, and where the open research arc points. The §1.1 closing sentence ("The held-out test is one operationalization... open questions of the broader research program (§7)") is the seed; §5 carries the development.

This expansion is queued for the §5 live walk; not applied in §1 pass.

## V11.2 — live section-by-section walk (2026-04-29)

Forked from v11.1 on 2026-04-28 as new active edit branch. Aarik switched from offline-annotation pattern to live in-conversation review on 2026-04-29.

### Locked sections

| Section | Disposition | Key changes from v11.1 |
|---|---|---|
| ✓ §1.1 | LOCKED | Hypothesis headline broadened (drop "on novel/new situations"); held-out test acknowledged as one operationalization; sycophancy callout added; broader research-program open questions named with §7 pointer; "novel" → "new" globally then dropped from headline |
| ✓ §1.2 | LOCKED | Typo fix; H1 widened to span 4 alternatives (no context, retrieved facts, full extracted facts, raw corpus); H5 reframed as efficiency/compression with concrete token comparison; "unit of inference" technical phrase replaced with layman; "Most typical AI users" replaced with "active human population... low-baseline band is the rule, not the exception"; rubric example anchored with anchor-1/anchor-2 context |
| ✓ §1.3 | LOCKED | Opening "AI" → "language model"; multi-band crossings reframed as transformations not percentages (1-in-5 / 1-in-17 with qualitative anchors); content specificity expanded (random pairings sometimes align); recall-based retrieval specified; hedging cleanup (broad rule headline, details to footnote); Pattern 2 explicit on negative impact; Pattern 3 caveat (not all specs include refusal-supporting axioms + rubric mismatch) |
| ✓ §1.4 | LOCKED | "Population of importance" → "population of relevance" (consistent with §1.2/§1.1); §1.2 baseline framing overlap trimmed; ALL CAPS emphasis dropped; gap framing expanded to fragmentation + reassembly impossibility; structural options list reframed with three-option enumeration (added: AI inferring opaquely, neutrally framed) |
| ✓ §2 lede | LOCKED | "General rather than individual" disambiguated (stores individual data BUT optimizes for general benchmarks); rhetorical question → declarative colon-list |
| ✓ §2.1 | LOCKED | §2.1 opener redundancy with §2 lede removed; Twin-2K persona size moved to footnote with verified figures (~32K tokens full / ~3.75K summary, sourced from `memory_system/docs/eval/`); PersonaGym example added (skeptical accountant flavoring); AlpsBench central finding italicized; "multiple versioned specifications keyed to life-phase" → layman ("separate specifications for different periods of a person's life") |
| ✓ §2.2 | LOCKED | No changes needed beyond v11.1 state |
| ✓ §2.3 | LOCKED | Reasoning-trace gloss italicized; C2a explicitly specified inline (specification only, no facts/corpus); held-out marked as full passage (verified); reasoning trace restructured into numbered activation order (A5 → A2 → P3 → A1 with one-line role glosses) |
| ✓ §2.4 | LOCKED | No changes |
| ✓ §2.5 | LOCKED | No changes |

### In progress

| Section | State |
|---|---|
| ▷ §3 lede + §3.1 | Surfaced; §3.1 closing line corrected ("guide them" → "reflect the person's own interpretation of the situation"; ties to §1.1 "interpretation" term-of-art) |

### Pending

§3.2 onwards through §8. Continuing live walk.

### V11.2 docx

`docs/beyond_recall_v11_2_draft.docx` — generated 2026-04-28 16:46. Will regenerate when §3+ walk completes.

### Future work item flagged (queued, not edited yet)

- **Language and cultural interpretive nuance** — Aarik 2026-04-29: specific phrases in some languages convey concepts that don't translate to English (or other languages); how does behavioral specification translate across implicit cultural understandings carried by language? Worth surfacing in §5 (Discussion) or §7 (Future Work). Not edited in §3.2 per Aarik's preference; current §3.2 "what we did not control for" already names language as a constraint.

---

## V11.5 — §3 walk completion (2026-04-29)

V11.2 forked to V11.5 at `docs/beyond_recall_v11_5_draft.md`. Fork made because the §3 walk produced substantive enough changes (§3.6 simplified rubric, §3.6.2 score-interpretation reframe with multi-anchor crossings, §3.6.4 specification-effect-claim definition, §3.6.6 layman-ization, §3.7 unified-brief expansion, four new glossary entries) that bumping versions matched what is being delivered. v11.2 preserved as historical state at `docs/beyond_recall_v11_2_draft.md`.

### §3 walk locked subsections (all on v11.5)

| Subsection | State | Major changes |
|---|---|---|
| ✓ §3 lede + §3.1 | LOCKED | §3.1 closing line corrected (interpretation term-of-art); subject-mean granularity clarification |
| ✓ §3.2 | LOCKED | Cultural / pretraining-coverage phrasing; "language" surfaced as uncontrolled |
| ✓ §3.2.1 | LOCKED | (no substantive changes) |
| ✓ §3.3 | LOCKED | (no substantive changes) |
| ✓ §3.3.1 | LOCKED | (no substantive changes) |
| ✓ §3.4 | LOCKED | Battery-link footnote; condition naming consistency |
| ✓ §3.5 | LOCKED | System-prompt observation discussion |
| ✓ §3.6 lede + rubric | LOCKED | Worked example moved out of §3.6 (now §4.X stand-in); Score / Meaning two-column rubric (Hamerton example column dropped); "Reading score differences" generalized; §4.X stand-in cross-reference added |
| ✓ §3.6.1 | LOCKED | Directionality-not-precision foreshadow added |
| ✓ §3.6.2 | LOCKED | Renamed "Fractional score interpretation" → "Score interpretation"; broadened lede to three granularities; *cross-anchor interpretation rule* italicized as term-of-art; new "Multi-anchor crossings" block with three real verbatim examples (Seacole Q2 / Hamerton Q25 / Bernal Díaz Q16, two three-band + one two-band); rate dropped from §3.6.2 (deferred to §4.2); inline file refs converted to footnotes; closing layman header |
| ✓ §3.6.3 | LOCKED | "Researcher judgment injected" parenthetical dropped |
| ✓ §3.6.4 | LOCKED | *Specification-effect claim* defined immediately as opening sentence (italicized term-of-art); Spearman ρ paragraph leads with layman definition (0/0.8/1 anchors) before numbers; same restructure for Krippendorff α; "What the panel is not" paragraph trimmed |
| ✓ §3.6.5 | LOCKED | "So that no researcher decision could shift" parenthetical dropped |
| ✓ §3.6.6 | LOCKED | Title changed *"Abstention is not cleanly distinguished"* → *"Refusals are not cleanly distinguished"*; *refusal* / *abstention* established as equivalents; jargon-heavy sentences simplified; length-correlation paragraph leads with the layman finding (per-condition r values to footnote); per-judge strictness shortened (means to footnote); "Both limitations tighten" defensive line dropped; "spec-vs-baseline gap is larger" softened to "very likely larger"; audit-script path converted to footnote |
| ✓ §3.7 | LOCKED | Pipeline-table outputs layman-ized for steps 1, 2, 3 (SQLite-canonical-store and structured-triple jargon replaced with plain-language descriptions); forward-references added to steps 4 and 5; new "Unified brief" paragraph with implicit-integration framing (replaces old short compose-step description); §7.3 ablation cross-reference; §8 repo cross-reference appended; new Appendix A.4 Live deployment subsection points to base-layer.ai |

### Glossary additions (Appendix H)

| Term | Defined at |
|---|---|
| ✓ Cross-anchor interpretation rule | §3.6.2 |
| ✓ Multi-anchor crossing | §3.6.2 |
| ✓ Specification-effect claim | §3.6.4 |
| ✓ Refusal (abstention) | §3.6.6 |

### V11.5 locked-sections docx

`docs/beyond_recall_v11_5_locked_draft.docx` — generated 2026-04-29 from `docs/beyond_recall_v11_5_draft.md`. Contains §1, §2, §3 (all subsections through §3.7) plus §8, §9, and Appendices A through H. §4-§7 omitted (active edit). Banner notice inside the docx names the omitted sections.

### Pending after §3 walk

- **§4.X baseline-engagement subsection** — base analysis complete (`docs/research/baseline_engagement_analysis_20260429.json`). Two extensions in flight: per-response-model abstention behavior + memory-system effect on abstention. Subsection placement and content settle once both extensions land.
- **§4.2 multi-anchor rate table** — current §4.2 reports only C4a-vs-C4 (2.6%) and C9-vs-C8 (3.8%). Should expand to include C5 → C4a (15.8%) and other before/after-spec comparisons — the headline-relevant rates. Address during §4 walk.
- **§4 through §7** — body-section walk continues from §4.1.

---

## V11.5 — §4 walk in progress (2026-04-30)

Session paused mid-§4.1 review to /clear and resume in fresh instance. State below is durable.

### Pre-§4-walk infrastructure (all landed 2026-04-29/30)

- **Baseline-engagement base analysis** — 14 subjects, 546 questions, ρ = −0.73, 41.2% REFUSE / 21.2% ENGAGED+STRONG, full naming necessary but not sufficient. Artifacts at `scripts/analyze_baseline_engagement.py`, `docs/research/baseline_engagement_analysis_20260429.json`, `docs/research/baseline_engagement_draft_section_20260429.md`.
- **Abstention extensions** — Sonnet 4.6 over-credits abstention at ~2x Haiku 4.5 rate (Haiku is the LOWEST over-credit case; §3.6.6 pooled numbers are a floor). Memory-system retrieval inflates refusal scores +0.21 anchor points vs pure C5 refusals (p=0.0001), but reciting retrieved facts adds nothing on top (Δ=+0.027, p=0.67); mechanism is condition-level, not response-level. Artifacts at `scripts/analyze_abstention_extensions.py`, `docs/research/abstention_extensions_analysis_20260429.json`, `docs/research/abstention_extensions_draft_20260429.md`.
- **Multi-anchor rate table all-14** — 8 condition pairs verified across all 14 subjects. C5 → C4a multi-anchor 13.0%, extreme 3.7%; C5 → C8 15.4% / 4.3%; C4 → C4a 2.2% / 0.9%; etc. Artifacts at `scripts/compute_anchor_crossing_all_pairs.py`, `docs/research/multi_anchor_rates_all_pairs_20260430.json`, `docs/research/section_4_2_multi_anchor_table_draft_20260430.md`.
- **Tier 2 model-mix verification** — 18 of 19 references in v11.5 correct. 1 discrepancy at §6 line 1711 ("4 response models" → "2 response models, Sonnet 4.6 + Gemini 2.5 Pro") corrected. Tier 2 set is Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects (Ebers, Yung Wing, Zitkala-Sa), NOT 4 response models as a stale v9/v10 artifact had claimed. Report at `docs/research/tier2_modelmix_verification_20260430.md`.
- **MCP server scaffold for study repo** built at `memory-study-repo/mcp/`. 5 tools: `search_study`, `get_subject_score`, `list_subjects`, `get_provenance`, `list_anchor_crossings`. 2 resources: `paper://section/<id>` (121 paper sections indexed). 7/7 smoke tests pass. README has Claude Desktop / Claude Code registration instructions. Verified canonical: `get_subject_score(seacole, C4a)` returns 2.595 (matches DATA_REFERENCE 2.59).
- **GTM agent-first outreach** strategy doc at `memory_system/gtm/strategy/AGENT_FIRST_OUTREACH.md`. Top 5 high-priority targets: Karpathy, Charles Packer (Letta), Simon Willison, Harrison Chase (LangChain), Logan Kilpatrick (Gemini DevRel). Four open strategy questions logged for Aarik decision (cold vs warm intro for Karpathy; agent-first packet as public meta-asset; ASK-FIRST flag policy; public MCP endpoint for launch window).

### §4 walk applied edits

| Section | State | Major changes |
|---|---|---|
| ✓ §4 lede | LOCKED | Full rewrite to mirror abstract: layman, prediction reframed as the test of representational accuracy (not the goal). Defines *Behavioral Specification* inline. Headline numbers stated upfront (+0.89 mean per-subject increase, 55.0% of low-baseline questions cross at least one anchor). Distinguishes interpretation-heavy questions (where spec adds value) from factual-recall questions (where retrieval is often sufficient and spec adds little or actively degrades). Names *Franklin* as layman-recognizable high-baseline example. Closes with control / robustness framing. "AI" → "language model" / "the model" throughout. |
| ✓ §4.1 first chunk | EDITED, lock pending | Multi-anchor examples expanded: 2→4 added to two-band, 2→5 added to three-band. "AI's answer" → "response model's answer." Extreme-jumps interpretation-heavy expansion added: *"These extreme jumps concentrate on interpretation-heavy questions: the no-context response refuses or stays generic, and the specification supplies the behavioral pattern the model could not retrieve from training data."* Structural-sensitivity paragraph restructured: substantive read first, mechanism second. Heading: *"What the gradient is actually showing."* Layman lift sentence: *"The improvement the specification produces is therefore largest on subjects whose baseline starts low, smallest on subjects whose baseline already approaches the quality the specification produces."* Transitions table column renamed: *"What this means in plain terms"* → *"Description"*. References to worked examples added: *"Worked examples of these transitions appear below (Examples A through D) and in §3.6.2 (multi-anchor crossings) and §4.1.1 (Seacole Q2 across condition bands)."* |
| ✓ §4.1.1 | NEW, placed | Per-question baseline engagement and worked rubric example. ~1,329 prose words / ~1,971 with tables. Verbatim Seacole Q2 demonstration across rubric bands 1, 2, 4, 5. Per-response-model abstention behavior subsection. Memory-system effect on abstention subsection. Aarik flagged this draft as mid-tier in density and may want a tightening pass before lock; agent has not yet been spawned for that. |
| ✓ §4.2 multi-anchor table | EDITED | Replaced two-row C4a-vs-C4 + C9-vs-C8 small table with all-14-subject 8-pair table. New framing: rate is largest for context-from-baseline comparisons (9-15%), smallest for spec-on-info-rich comparisons (~2%). Cross-references the *cross-anchor interpretation rule* term-of-art. Footnote points to per-pair JSON and notes 9-subject low-baseline gives somewhat higher rates. |
| §4.1.1 | walk pending | Aarik may want tightening pass first per his density flag. |
| §4.2 (rest of section) | walk pending | After multi-anchor table replacement, the rest of §4.2 needs verbatim walk. |
| §4.3 through §4.7 | walk pending | |
| §5, §6, §7 | walk pending | §6 line 1711 Tier 2 fix already applied. §7.5 diff-RL paragraph added 2026-04-30. |

### Other edits applied 2026-04-30

- **§7.5 diff-RL paragraph** added (per-user diff-as-RL signal on the specification itself). Distinct from the existing corpus-based drift paragraph above it.
- **§8 agent-friendly tooling paragraph** added in Data and code availability section. Names study_knowledge.db + ChromaDB index, MCP server in development.
- **Appendix A.4 Live deployment** subsection added pointing to base-layer.ai.
- **§1 HTML comment marker** added (after §1 heading, before §1.1). Notes Aarik's interest in adding a worked example to §1 (Introduction) for production release. Candidates named: §3.6.2 multi-anchor crossings, §3.7 Hamerton specification examples, §4.1.1 Seacole Q2 example.

### Glossary additions during §3 walk (already in Appendix H)

| Term | Defined at |
|---|---|
| ✓ Cross-anchor interpretation rule | §3.6.2 |
| ✓ Multi-anchor crossing | §3.6.2 |
| ✓ Specification-effect claim | §3.6.4 |
| ✓ Refusal (abstention) | §3.6.6 |

### Next session pickup order

1. **Confirm-lock §4.1.** Aarik reviewed the full §4.1 verbatim immediately before pausing. Explicit lock pending; if no further edits, mark locked and move forward.
2. **Walk §4.1.1.** Aarik flagged the merged draft as mid-tier in density. Optional tightening pass before lock (move statistical detail to footnotes; collapse the two memory-system tables; split worked-example interpretation paragraph; split limitations paragraph).
3. **Walk §4.2** (with new multi-anchor table already in place; rest of section needs verbatim review).
4. **Walk §4.3 through §4.7** (no pre-walk edits needed beyond the inserted material).
5. **Walk §5, §6, §7** (§6 Tier 2 fix and §7.5 diff-RL paragraph already applied; rest of these sections still need verbatim review).
6. **Regenerate locked-sections docx** once §4 walk completes (and again at full-paper completion). Script: `scripts/export_v11_5_locked_to_docx.py`.

### V11.5 docx state

- `docs/beyond_recall_v11_5_locked_draft.docx` (119 KB) generated 2026-04-29 covers §1-§3 + §8-§9 + Appendices A-H. §4-§7 omitted.
- Will regenerate after §4 walk completes to extend the locked-sections doc through §4.

---

## V11.5 — §4 walk progress (2026-04-30, paused mid-section)

### §4 subsections locked

| Section | State | Major changes |
|---|---|---|
| ✓ §4 lede | LOCKED | Full rewrite to mirror abstract: layman, prediction reframed as the test of representational accuracy. Defines *Behavioral Specification* inline. +0.89 mean lift / 55.0% per-question rate stated upfront. Distinguishes interpretation-heavy questions (where spec adds value) from factual-recall questions (where retrieval is often sufficient and spec adds little or actively degrades). Names *Franklin* as layman-recognizable high-baseline example. "AI" → "language model" / "the model" throughout. |
| ✓ §4.1 | LOCKED | Multi-anchor examples expanded (2→4, 2→5 added). "AI's answer" → "response model's answer." Extreme-jumps interpretation-heavy expansion. "What the gradient is actually showing" restructured to lead with substantive read; layman lift sentence. Transitions table column renamed to "Description"; references to worked examples added. Stats table replaced by paragraph form with footnote (Wilcoxon + Spearman in body, regression detail in footnote). "Reading the gradient" trimmed to conclusion-led. Per-subject results table gained Band column + C4 facts column. Robustness checks → footnote pointing to §4.6.3. Closing reframed: "aggregate gradient hides per-question structure that is itself the most informative finding." |
| ✓ §4.1.1 | LOCKED | Per-question baseline engagement and worked rubric example. Substantially shortened (~1,300 prose words → ~400). Block 4 (naming/training-depth analysis) dropped. Block 7 (per-response-model abstention) moved to §3.6.6. Block 8 (memory-system abstention) moved to §4.4.4. Spearman/Mann-Whitney detail compressed to footnote. Worked Seacole Q2 example kept as showcase. Companion-data line moved to footnote. Worked-example intro restructured to separate-line labels. Held-out shown as "Held-out ground truth"; C2c labeled "C2c wrong spec (Babur)"; condition labels normalized. |
| ✓ §4.2 | LOCKED | Bullet 4 parenthetical → footnote `[^c9-aggregation]`. "info rich" jargon purged. Multi-anchor table rebuilt with natural-language labels (Baseline → full pipeline, Wrong spec → correct spec, etc.). Sentence after table simplified. "Behaviorally meaningful unit" sentence dropped (redundant with §4.1.1). Hamerton outlier note + multi-anchor examples → footnote. Token-size column expanded (raw corpus 33K-549K, mean ~163K). "Facts" → "all facts" throughout to disambiguate from memory-system retrieval. Compact-spec headline now: "captures the large majority of that representational-accuracy gain." |
| ✓ §4.2.1 | LOCKED | Renamed from "Question-improvement rate: a candidate secondary reporting metric" → "Per-question improvement rate." Secondary-metric proposal dropped (will land in §7 Future Work during walk). Lede compressed; reporting-triplet paragraph compressed. Table column labels → natural language ("Spec only", "All facts only", "Raw corpus", "All facts + spec"). All-14 table dropped → footnote. Pairwise comparison table dropped → footnote. "Failure modes" line dropped. Closing §1.2/§4.1 cross-reference dropped. Hamerton/Ebers worked examples retained. Token-size column added to question-improvement table. |
| ✓ §4.3 | LOCKED | Opening sentence softened: "If structure were the dominant driver, a mismatched specification would produce a substantial fraction of the matched-spec improvement. Random pairings recover only part of it..." (acknowledges random-derangement +0.15 has coherent reading). Per-subject wrong-spec heterogeneity paragraph + 13-row table → compressed paragraph + footnote (table flagged for move to §4.6 sensitivity subsection during §4.6 walk). 6-provider collective review framing dropped. Three evidence blocks (spec-activation, wrong-spec detection, hedging) consolidated into one "Response-level evidence" section with conclusion-led detection asymmetry. Hedging cross-references §1.3 footnote for rule definitions. Wrong-spec table reading column reframed: "matched content increases representational accuracy" / "adversarial mismatch degrades representational accuracy." |
| ✓ §4.4 lede | LOCKED | Hypothesis statement (no edits). |
| ✓ §4.4.1 | LOCKED | Lede absorbed "Base Layer is not a memory system" framing + "three of four commercial systems" closing into single punchy paragraph; later trimmed per Aarik to remove the "Base Layer is not a memory system" opener. "Aggregate is more visible signal" meta-commentary dropped. "People the model does not already know" → "low-baseline subjects" / "14 main-study subjects" consistently. Two aggregate tables (controlled + native) → one combined table per system row. Headline numbers use all-14 panel. Low-baseline-9 detail + Wilcoxon stats → footnote with "underpowered at these effect sizes" note. Per-system narrative paragraphs (Zep, Mem0, Letta, Supermemory, Base Layer) dropped from §4.4.1; per-question per-system content moved to §4.4.2. Standalone hedging note dropped → footnoted. Letta second-path Pointer block dropped → footnoted on first Letta mention. Closing paragraph rewritten as "controlled-vs-native split is itself informative" observation. |
| ✓ §4.4.2 | LOCKED | Fundamental restructure. Lede now: "At the per-question level rather than the aggregate mean, all five memory systems tested display three distinguishable patterns characterizing how they interact with the Behavioral Specification. Each pattern shifts the model's representational accuracy of the subject in a different direction." Three patterns named upfront (interpretive supply / over-theorization / spec-induced refusal) with representational-accuracy framing for each. "Why Supermemory carries the mechanism walkthrough" framing paragraph dropped. Spearman ρ statistical signature dropped (covered in §4.4.4). Quantified Supermemory mixture table → footnote. Per-subject paired-delta Table 4.6 → footnote pointer to Appendix B.X. Per-pattern structure: Anchor example on Supermemory + cross-system reproduction note inline (Pattern 1: Mem0 / Letta / Zep / Base Layer; Pattern 2: Base Layer; Pattern 3: Base Layer + §4.4.3 Keckley Q21 cross-ref). Pattern 1 variant (Fukuzawa Q16 reframe) compressed from former Example 4 into one paragraph. Pattern 2 / 3 reading sentences cleaned (no negation patterns). Pattern 3 broadened beyond epistemic-integrity-only to spec axioms varying by subject (dignity, honoring-testimony, epistemic-integrity). Pattern 3 outcome qualified: "Lowers the measured rubric score; whether it lowers actual representational accuracy depends on whether refusal was the correct behavior on that question." Per-system frequency tendencies kept (compressed). Closing dynamic-serving paragraph added pointing to §7.4. C1/C3 condition identifiers expanded to "(retrieval only)" / "(retrieval + spec)" on cross-system mentions. |

### §4 remaining (resumed 2026-05-01)

- **Sensitivity check moved from §4.4.1 to §4.6.5** ✓ 2026-05-01. Per Aarik: sensitivity content belongs with the other §4.6 sensitivity checks. Cut the two new sensitivity paragraphs + footnote from §4.4.1; replaced with a one-sentence forward reference to §4.6.5. New §4.6.5 "Retrieval-overlap sensitivity (semantic-similarity matching, K variation)" inserted between current §4.6.4 (wrong-spec) and the closer; current §4.6.5 ("What these checks don't address") renumbered to §4.6.6. New §4.6.5 follows the parallel Result/Mechanism/What-this-establishes structure with a sensitivity grid table (controlled vs native, 3 thresholds shown). §4.6 lede updated to "five sensitivity checks" + 1 closer (was 4 + 1). §4.7 5-finding-bullet list updated with new "Retrieval-overlap sensitivity" item. §4.6.6 closing paragraph updated to reference §4.6.5 alongside the other apparatus checks.
- **Retrieval-divergence finding: tone fix + concrete % stat + sensitivity check** ✓ 2026-05-01. Per Aarik's flags: (a) softened framing across all four locations from "calls into question what those benchmarks are actually measuring" to "recall benchmarks measure recall (which is what they should measure); representational accuracy operates at the interpretation layer." (b) Added "convergence on top-K under identical input would have been evidence of a shared interpretive substrate" framing — names what convergence would have meant, then states what non-convergence suggests (provider-specific design choices). (c) Added concrete per-question stats matching other headline-bullet readability: 52.3% of (system pair, question) instances share zero facts; 71.4% share one or fewer; mean pairwise overlap 8.3%. Computed from raw retrievals across 5070 (pair, question) observations. (d) Tightened opening sentences for both "Provider divergence" bullet ("Memory-system providers do not converge on which facts are most relevant for a question, even when given identical input.") AND "Gradient" bullet ("The Behavioral Specification's benefit is largest where the model knows the person least.") to lead with thesis claim instead of setup. (e) **Background semantic-similarity sensitivity check executed and integrated.** New §4.4.1 paragraph reports soft-Jaccard at K ∈ {5, 10}, T ∈ {0.70, 0.80, 0.85, 0.90, 0.95}, both controlled and native configs. Headline result: divergence survives every threshold tested. Controlled K=10 mean rises only marginally (0.083 → 0.102 at T=0.85, 0.191 at T=0.70); strongest single pair at any cell is 0.277 (BaseLayer–Supermemory T=0.70); never crosses 0.30. Native config stays effectively zero (0.004 at T=0.85, 0.016 at T=0.70). K=5 truncation lowers overlap rather than raising it. Footnote `[^retrieval-overlap-semantic]` points to the sensitivity grid + script. (f) §7.1 follow-up bullets reduced from 3 to 2: native semantic-similarity bullet removed (now done); convergence-at-larger-K tightened to "K > 10 (K=5 already tested)"; recall-benchmark meta-analysis reframed without alarmist language. New deliverables: `scripts/analyze_retrieval_overlap_semantic.py` + `docs/research/retrieval_overlap_semantic_20260501.json`. Memory note `project_memory_provider_outreach.md` saved for post-publish provider outreach.
- **Retrieval-divergence finding ELEVATED to headline** ✓ 2026-05-01. Per Aarik: this finding "calls into question what the point of [the recall] benchmark is" and deserves headline-finding status. Promoted in v11.5 across: (a) §1.3 — added 7th headline-finding bullet "**Provider divergence on retrieval relevance**" alongside the six existing bullets (Gradient, Step-changes, Compression, Content specificity, Memory-system layering, Hedging reduction); the previously-added duplicate "Surfaced finding" callout block below the headline list deleted to avoid redundancy. (b) §4.4 lede — sharpened framing from "may be testing a narrower property than they claim" to "calls into question what those benchmarks are actually measuring." (c) §4.4.1 retrieval-overlap subsection — same sharpening of the LongMemEval/LOCOMO framing in the lead paragraph. (d) §4.7 5th finding bullet — same sharpening. The finding is now a load-bearing claim threaded through §1.3 (headline), §4.4 lede, §4.4.1 (data + table), §4.7 (summary), and §7.1 (three follow-up bullets: convergence-at-larger-K, recall-benchmark meta-analysis, native semantic-similarity overlap). Memory note for provider outreach saved at `project_memory_provider_outreach.md`.
- **§4.4.1 cross-system retrieval overlap subsection** ✓ RESTRUCTURED + LOCKED 2026-05-01. After Aarik's flag pass: lead paragraph replaced with the §1.2 convergence answer (was the closing); plain-language Jaccard definition added as second paragraph; per-pair detail moved into a 10-row sorted Jaccard table (was inline parentheticals); pair-mechanism nuance (Zep graph blob, Letta dedup) kept inline as third paragraph; per-subject + per-category variation moved to footnote `[^jaccard-aggregate-detail]`; native-eval framing changed from "not directly interpretable" to "not directly comparable on this metric, semantic-similarity overlap flagged as future work in §7"; "each retrieval algorithm" → "each provider"; percentage figure ("~8%, ~1-2 shared facts of average union of 17") added to lead. Pending: §7 walk needs corresponding bullet for native semantic-similarity retrieval-overlap analysis. New 4-paragraph bolded-label block ("Cross-system retrieval overlap: providers do not converge.") inserted into §4.4.1 after the controlled-vs-native split paragraph, before the §4.4.2 separator. Headline: mean Jaccard 0.083 across 10 system pairs in controlled config, ~1-2 shared facts out of average union of 17. Closes the §1.2 convergence promise. Pair structure detail (Base Layer–Supermemory highest 0.146, Zep pairs lowest ~0.025), Letta dedup caveat (3.5 unique facts of 10 returned), per-subject variation (0.043 Equiano to 0.115 Hamerton), per-category variation small (0.076–0.093). Native pipeline noted (mean Jaccard 0.000) but flagged as not directly interpretable (heterogeneous return types). Closing sentence ties divergence to representational accuracy: "which facts the system surfaces determines, before any reading model engages, what the response can be about." Footnote `[^retrieval-overlap-data]` points to JSON + script. No em-dashes. C-codes confined to existing Δ_spec convention used elsewhere in §4.4.1.
- **§4.7 Summary + bridge to §5** ✓ LOCKED 2026-05-01. Restructured from one-paragraph prose summary to two bulleted lists (four findings, five robustness checks) plus a one-line bridge to §5 + §6. Cross-references updated for new structure (Franklin → §4.1.2, §4.6.4 wrong-spec, §4.6.5 closer).
- **§4.4.3 Keckley Q21 + §4.4.4 two statistical signatures** ✓ CONFIRMED LOCKED 2026-05-01 (walked pre-compaction, formal lock recorded here). §4.4.3 includes held-out passage verification (battery_v2.json id=21 matches paper narrative exactly), full A1 + A2 axiom quotes in `[^keckley-axioms]` footnote, per-system Pattern 3 table, rubric-design follow-up paragraph pointing to §7. §4.4.4 leads with three signatures (re-ranking / near-uniform lift / partial re-ranking), Spearman ρ table with natural-language labels, floor-effect caveat acknowledging design limitation.
- **§4.6 walk complete** ✓ LOCKED 2026-05-01. All 5 subsections + lede walked. §4.6.1, §4.6.2, §4.6.3, §4.6.4, §4.6.5 (renamed from §4.6.6 after Franklin moved out). Major change at §4.6.5 walk: Franklin moved to **new §4.1.2** (not in §4.6 anymore) per Aarik's read that Franklin demonstrates the gradient at the high-baseline end, not an apparatus robustness check. §4.6 dropped from 6 to 5 subsections (4 sensitivity checks + 1 closer). All cross-references updated: §1.2 c2c footnote, §4 roadmap, §4.6 lede, §4.6.5 (was §4.6.6), §4.7 summary. §4.1 now has §4.1.2 The gradient at the high-baseline end (Franklin reference) — 4 paragraphs, theoretical-reading caveat preserved, no parallel "Result/What this establishes" labels (kept §4.1 prose voice rather than §4.6 sensitivity-check voice). §4.6.4 also gained an "Open questions for future work" block on per-question wrong-spec meta-analysis (human-annotated study, three concrete questions); flagged for §7 walk to confirm corresponding bullet exists.
- **§4.6 lede + §4.6.1 Tier 2 + §4.6.4 wrong-spec sensitivity (new) + §4.6.6 reorder** ✓ LOCKED 2026-05-01. Major changes: (a) §4.6 lede rewritten to signal all 5 subsections (was "three potential artifacts" / inconsistent with body); "5-judge primary excludes Gemini" defensive framing replaced with "conservative 5-judge primary" / "7-judge sensitivity panel that adds Gemini." (b) §4.6 reordered: new §4.6.4 (wrong-spec derangement protocol sensitivity) inserted between battery composition and Franklin; current §4.6.4 ("what these don't address") renamed to §4.6.6 and moved past Franklin. (c) §4.6.4 NEW absorbs orphaned wrong-spec mechanism paragraph (was sitting between §4.6.5 and §4.7) + per-subject wrong-spec heterogeneity table (was §4.3 footnote `[^wrong-spec-per-subject]`); §4.3 main text now points cleanly to §4.6.4. (d) §4.6.1 Tier 2 restructured per Aarik to lead with result; "concern motivating the check" paragraph dropped; metadata + Zitkala-Sa explanation pushed to footnote `[^tier2-result-metadata]`; panel-scope paragraph + ranges-mechanics moved to footnote `[^tier2-panel]`; recompute footnote dropped, script paths absorbed into panel-scope footnote; "What this establishes" reduced to two short sentences; secondary observation kept; §3.3.1 cross-reference added to test design. C-codes purged from body prose: `C5` → "no-context baseline"; `Δ_C4a` → "full-pipeline lift" / "specification-effect"; alternate-Δ detail compressed to "three alternate lift definitions tested." (e) §4.7 cross-references updated to mention all 6 §4.6 subsections.
- **§4.5 Letta stateful-agent N=3** ✓ LOCKED 2026-05-01. Major changes: (a) "alternative to retrieval at query time" tightened to "does not rely solely on retrieval at query time" for clarity; (b) corpus sizes added inline (25,231 / 48,161 / 222,742 words) for all three subjects in headline result; (c) "What this does and does not show" subsection dropped from body (caveat absorbed into §7.5 cross-reference and Appendix G); (d) blockquote restructured into 4 sub-points: headline result, block scaling, verbatim sentence duplication, semantic-similarity duplication (new); (e) framing of size-vs-effect changed from monotonic ("widens at small corpora and narrows at Babur" — empirically wrong) to "largest at mid-corpus subject (Ebers), smaller at both endpoints" with three hedged interpretations explicitly listed and labeled as not-distinguishable on N=3; (f) **new semantic-similarity duplication analysis** added to body and Appendix G: at Babur, 56.1% of sentences have a near-paraphrase at cosine ≥ 0.85, 35.2% at ≥ 0.95 (verbatim figure of 25.4% understates duplication); Ebers shows minor near-paraphrasing; Hamerton none; (g) "compressed-brief variant" → "unified-brief variant" standardized across §1.4 (line 127), §4.5 body, and Appendix G (lines 3082, 3084, 3132); (h) §1.4 line 127 updated to include semantic 35-56% number alongside verbatim 25%. Script: `scripts/analyze_letta_semantic_duplication.py`. Data: `docs/research/letta_semantic_duplication_20260501.json`. **Open item:** Appendix G body retains "What this exploration does and does not show" subsection (kept as longform); body §4.5 closing prose cross-references Appendix G + §7.5 only.
- **§4.4.3 Keckley Q21 case study** (24 lines) — pending walk.
- **§4.4.4 two statistical signatures** (21 lines) — pending walk. Spearman ρ from §4.4.2 lives here.
- **§4.6 robustness and sensitivity** (6-line lede + 5 subsections, ~86 total lines):
  - §4.6.1 Tier 2 cross-provider replication
  - §4.6.2 Judge panel sensitivity
  - §4.6.3 Battery composition sensitivity (already received content from §4.1)
  - §4.6.4 What these robustness checks do not address
  - §4.6.5 Franklin as the high-baseline reference
- **§4.7 Summary of §4 + bridge to §5** (6 lines) — pending walk.

### Pending integrations to execute during §4.6 / §7 / Appendix walks

- **Per-subject wrong-spec deltas table.** Currently §4.3 footnote `[^wrong-spec-per-subject]`. ~~Move to a new §4.6 sensitivity subsection during §4.6 walk.~~ ✓ DONE 2026-05-01: now in §4.6.4 (new wrong-spec sensitivity subsection).
- **Per-system per-subject paired-delta Table 4.6.** Currently §4.4.2 footnote `[^memsys-pattern-appendix]`. Move to Appendix B.X during appendix walk.
- **Dynamic-serving as production-serving future work.** §4.4.2 closing now points to §7.4. Confirm §7.4 covers dynamic activation of axiom and prediction subsets during §7 walk; expand if needed.
- **Wrong-spec per-question meta-analysis (NEW, added during §4.6.4 walk).** §4.6.4 closes with an "Open questions for future work" pointer to §7 for a human-annotated meta-analysis of per-question wrong-spec deltas: which parts of the served specification the model referenced under correct vs. mismatched conditions, where coincidental spec alignment produced false-positive deltas (the five small-positive v1 cells), and how per-subject score consistencies relate to underlying spec similarity. Confirm §7 has a corresponding bullet during §7 walk; add one if not.

### Beyond §4: §5–§9 remaining (~410 lines)

- §5 Discussion (217 lines, densest single block)
- §6 Limitations (73 lines, has Tier 2 fix already applied at line 1711)
- §7 Future Work (56 lines, has §7.5 diff-RL paragraph already added)
- §8 Data, code, reproducibility (22 lines, has agent-friendly tooling paragraph already added)
- §9 References (42 lines)

### Pace estimate (2026-04-30)

- §1–§3 in 1 day: ~658 lines locked.
- §4 first half in 1 day: ~580 lines locked.
- Remaining ~567 lines (157 §4 + 410 §5–§9) is achievable in one focused day at this pace; §5 Discussion is the longest single block.

### Post-content-lock items still owed

- Figure review (10 figures across §4).
- Final formatting pass.
- Locked-sections docx regeneration via `scripts/export_v11_5_locked_to_docx.py` once content is fully locked.

---

## V11.8 — share-zero / share-≤1 reconciliation (2026-05-05)

**Issue.** The 2026-05-01 entry above (§4 walk) introduced "52.3% / 71.4%" share-zero / share-≤1 statistics into §1.3, §4.4.1, §4.7, and KEY_FINDINGS M4 with a noted denominator of "5,070 (pair, question) observations." The data signoff agent flagged the numbers as not persisted in any JSON artifact (`docs/reviews/data_signoff_v11_8_20260505_122849.md`).

**Investigation 2026-05-05.** Re-emitted `scripts/analyze_retrieval_overlap.py` with `share_zero_intersect` and `share_le_one_intersect` fields. Exhaustive cut grid (subject set × pair set × raw/norm × pooled/mean-of-pair × multiset × K=3/5/7/10) on the canonical retrieval payloads:

| Cut | n | share-zero | share-≤1 | mean Jaccard |
|---|---:|---:|---:|---:|
| All 14 subj × 10 pairs (K=10) | 5,460 | 35.95% | 65.60% | 0.083 |
| 13 globals × 10 pairs (K=10) | 5,070 | 36.65% | 66.63% | 0.083 |
| 13 globals × 6 commercial pairs (K=10) | 3,042 | 41.03% | **71.43%** | (commercial-only) |

Findings:
- **Mean Jaccard 0.083 ✓** reproducible across subject and pair cuts.
- **71.4% reconciles exactly** with the 13-globals × 6-commercial-pairs cut (n = 3,042). Paper text at line 1172 ("ten system pairs ... 546 questions" = n=5,460) is inconsistent with this cut.
- **52.3% reproducible nowhere.** No subject set, pair set, K cutoff, or normalization variant in the controlled data produces 52.3%. The legacy v6-era `string_match_disagreement.py` reports an *all-3-disagreement at top-10* statistic of 53.2% on three systems (Mem0, Letta, Supermemory) over n=515 — a different metric on a different system count and n. The paper's 52.3% is plausibly a transcription error of that 53.2% during v11.5 elevation.

**Resolution (Aarik approved Option A, 2026-05-05).** Replace 52.3% / 71.4% with the all-14-subjects × 10-pairs computation: **35.9% share zero, 65.6% share ≤1, n = 5,460**. Mean pairwise Jaccard 0.083 unchanged. Headline interpretation unchanged — providers do not converge on relevance given identical input. Rhetorical force softens from "more than half the time they share zero" to "about a third of the time they share zero"; the corrected number is still strong evidence of non-convergence.

**Edits applied:**
- §1.3 (line 118): "more than half the time" → "substantially non-overlapping"; 52.3% / 71.4% → 35.9% / 65.6%.
- §4.4 lede (line 1131): same swap; "more than half the time" → "substantially non-overlapping."
- §4.4.1 (line 1170): 52.3 / 71.4 → 35.9 / 65.6; new footnote `[^share-zero-cut]` pinning n = 5,460 = 14 × 39 × 10 with sensitivity to alternate cuts (13 globals: 36.7 / 66.6; commercial-only-14: 40.4; commercial-only-13g: 41.0 — every cut shows substantial divergence).
- §4.7 (line 1496): "more than half the time" → "substantially non-overlapping"; 52.3% → 35.9% / 65.6%.
- KEY_FINDINGS.md M4 (line 216): same swap; "nearly disjoint" → "substantially non-overlapping"; n explicitly stated as 5,460 = all 14 main-study subjects × 39 questions × 10 system pairs, controlled config.

**Persistence.** Share-zero / share-≤1 fractions now persisted in `docs/research/retrieval_overlap_analysis_20260501.json` under `per_config_overall[*].share_zero_intersect` and `per_config_overall[*].share_le_one_intersect` (and at every aggregation level). Reproducibility: `python scripts/analyze_retrieval_overlap.py`.

---

## V11.8 — mechanical fixes batch (2026-05-05 evening)

Applied while Aarik was AFK. All low-risk mechanical fixes from the consolidated decision list and the integrity sweep.

**Keckley Q21 SM↔BL transcription swap (P1 from numerical-claims audit).** §4.4.3 lines 1307-1308 had Supermemory and Base Layer parenthetical baselines transcribed swapped. Applied: SM `(strong retrieval-only, ~3.4)` → `~3.6`; BL `~3.6` → `~3.3`; BL Δ `−2.2` → `−2.3` (matches data 3.333, −2.333). Δ values now reconcile with judge data within tolerance.

**Anchor-link fixes (integrity sweep P0).**
- L466 §4.1.1 anchor: removed the `[^companion-data-411]` footnote ref from the §4.1.1 heading and placed it on the closing word of the first paragraph below. Heading anchor `#411-per-question-baseline-engagement-and-the-worked-rubric-example` now resolves cleanly from the L466 link.
- L665 §8 anchor: changed link text + anchor from `[§8 Data and code availability](#8-data-and-code-availability)` to `[§8 Data, code, and reproducibility](#8-data-code-and-reproducibility)` to match the actual heading.

**Em-dash restructures (Item 10).** Two em-dashes restructured per Aarik's no-em-dash rule:
- §4.3 wrong-spec detection paragraph: "what the model already knows about the named subject — specifications are anonymized" → sentence break + new sentence.
- §4.4.2 spec-induced refusal pattern: "varying by subject — in this study, dignity, honoring-testimony..." → "(which vary by subject; in this study, ...)".

**§4.4.1 retrieval-overlap heatmap (Item 9).** New `figures/fig_4_4_1_jaccard_heatmap_v1.{png,pdf}` rendered from `docs/research/retrieval_overlap_analysis_20260501.json` per_pair_per_config (controlled). 5×5 symmetric heatmap, viridis colormap (colorblind-safe), diagonal grayed. Embedded in §4.4.1 immediately after the per-pair Jaccard table. Reproducibility: `scripts/generate_fig_4_4_1_jaccard_heatmap.py`. `figures/README.md` updated with the new figure entry.

**Item 11 (Franklin first-mention).** Verified: "Benjamin Franklin" full name now first appears at §3.2 (line 315, "Franklin as a known-figure control") immediately before §3.2.1 — order is correct. No edit needed.

**Items 5, 6, 7 (anchor-crossing prominence rebalance).** Deliberately deferred to tomorrow — these reshape interpretation and should be Aarik-authored, not mechanically applied.

**Source-corpora migration + references archive (separate ask).** All 14 main-study autobiographies + Franklin reference + Franklin letters mirrored to `data/source_corpora/<subject>/` with provenance.md + sha256 per subject (12.8 MB / 2.25M words). All 18 §9 references PDFs in `docs/references/` (Bartlett 1932 supplied by author; 17 arXiv via fetcher script). MANIFEST.md + manifest.json for both. Scripts: `scripts/migrate_source_corpora.py`, `scripts/fetch_references.py`. Both reproducible.

---

## V11.8 — §2 walk progress (2026-05-05 evening continued)

### §2 lede locked
Added new labeled paragraph "**Personalization in this paper's sense.**" defining the scope of "personalization" used throughout the paper (interpretive layer beneath stated preferences and biographical facts; preferences and facts are downstream artifacts of that layer). Forward-references §3 (operational test) and §5 (further discussion). Em-dash purged. **Glossary follow-up:** Appendix H should add a "Personalization (this paper's sense)" entry pointing back to §2 lede.

### §2.1 locked
Multiple fixes per Aarik's read:
- Twin-2K opener: "predicts how a person would answer survey questions by looking at how they answered other survey questions" (3x "survey") → "infers how a person would answer one questionnaire item from how they answered others" (1x). Prediction-as-target now stated explicitly inside the Twin-2K paragraph: "Twin-2K's stated target is *prediction accuracy on survey interpolation*: the model is scored on how well it predicts a held-out questionnaire response, not on whether it represents the underlying reasoning that produced the response."
- Persona paragraph trimmed ~40% (~250 → ~155 words). "Real" filler dropped. "this paper's ~7,000-token specification" → "this paper's ~7,000-token **Behavioral Specification**" (proper-noun first body mention; lede already forward-referenced §3).
- `[^twin2k-persona-size]` footnote: 4 sentences → 2; full breakdown deferred to Appendix F. **Appendix F follow-up:** ensure persona-input depth across benchmarks is covered there during Appendix walk.
- "Prediction is a diagnostic; the representation is what the pipeline is building" → "Prediction is a diagnostic; the Behavioral Specification is what this paper is testing." Resolves the ambiguous "pipeline" reference.
- Held-out paragraph: "assumption" appeared 6 times → 0 (replaced with "stability premise" / "premise"). Empirical generalization claim now explicit forward-reference: "§4.1 reports that the Behavioral Specification authored from training text generalizes to held-out text at above-baseline rates" (was: "does in fact generalize…"). Cleaner separation between §2 framing and §4 results.
- Canonical-life-events paragraph **removed from §2.1**. Aarik's call: belongs in discussion / future work, not in prior-art framing. **§7 walk dependency:** add equivalent paragraph to §7.5 (specification temporality) or §7.6 covering: snapshot-vs-shift production-deployment question, automatic-detection vs user-annotation vs separate-period-specifications design space.
- Closer: "**The implication for future memory-system research is that single-axis scores are underspecified.** A single memory-system score is underspecified." (2x "underspecified") → "**A single number does not capture a memory system's full capability.**" Layman, single occurrence.

### §2.2 locked
- `[^benchmark-disputes]` footnote: ~225 words → ~70 words; preserved load-bearing claims (Mem0/Zep dispute, Supermemory comparisons, Vectorize.io reproductions, "we don't adjudicate, we measure on a different axis"); cut detailed Mem0 allegation litany and methodology-recap.
- Verifier landed: 14/16 cells VERIFIED, 0 DRIFT, 0 UNVERIFIABLE against current Mem0 / Letta / Supermemory / Zep + Graphiti vendor docs and arXiv PDFs in `docs/references/`.
- `[^letta-recall]` URL slug fixed: `benchmarking-llm-judges-for-evaluating-ai-agents` → `benchmarking-ai-agent-memory` (old URL 404'd).
- `[^benchmark-disputes]` updated to reflect that `getzep/zep-papers#5` was closed 2025-05-19 (Zep posted corrected 75.14% ± 0.17 mean of 10 runs; Mem0 did not respond). Substance preserved; freshness phrasing tightened.
- Verifier report at `docs/reviews/table_2_1_verification_v11_8_20260505.md`.

### §2.3 locked
- Lede restructured per Aarik: was "For a representation of how a person reasons, traceability is required, not optional..." (auditability framing first, fact/reasoning distinction buried in P2). Now opens with the structural distinction itself: "Traceability operates at two levels. **Fact-level traceability** answers where a retrieved claim came from. **Reasoning-level traceability** answers why the system believes this about this person." Followed by why-it-matters ("representational accuracy operationalizes interpretation, and interpretation cannot be verified at the fact level alone"), then auditability bar.
- "Comes in two flavors" → "operates at two levels" (formal register).
- P2 (per-system fact-level tour) and P3 (Behavioral Specification reasoning-trace structure) unchanged in content; redundant lede sentences trimmed since the distinction is now in P1.

### §2.4 locked
- No edits required. Six prior-work threads (Bartlett / Hinton / Chen / Jiang / Jain / Lu) read clean.

### §2.5 REMOVED
- Per Aarik: §2 is "Prior Work, Industry Benchmarks, The Fifth Target" — positioning, not methodology. LLM-as-judge is execution methodology that belongs in §3.6.
- Verified all §2.5 content already lives in §3 with no loss: Zheng et al. (2023) citation in §3.6.1 line 476; full calibration methodology + Gemini-inflation finding + 5-judge-primary / 7-judge-sensitivity framing in §3.6.3 lines 527-555.
- No cross-refs to §2.5 elsewhere; removed cleanly.
- §2 now closes at §2.4 and transitions directly to §3 Study Design.

### §2 walk closed (2026-05-05 evening)
Final §2 structure: lede + §2.1 + §2.2 + §2.3 + §2.4 (5 subsections, no §2.5). All locked.

### Glossary update applied
Added "**Personalization (this paper's sense).**" entry to Appendix H glossary (alphabetical, between "Multi-anchor crossing" and "Refusal (abstention)"). Points back to §2 lede for the full definition.
