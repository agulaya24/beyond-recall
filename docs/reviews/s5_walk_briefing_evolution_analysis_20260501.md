# §5 Walk Briefing: Framing Evolution Analysis

**Purpose:** Reference document for the §5 (Discussion) walk of Beyond Recall v11.6. Tracks how Aarik's framing of the paper has evolved across drafts (v8 through v11.6) so that when drafting each §5 subsection, the writer can consult this doc to see WHY certain framings were locked, what was rejected and why, and what the trajectory of refinement says about where Aarik wants §5 to land. Companion to the voice/positioning brief (`s5_walk_briefing_voice_positioning_20260501.md`) and the coverage matrix (parallel agent). Voice brief covers static rules; coverage matrix covers stats; this brief covers trajectory.

**Primary sources consulted:**
- `docs/reviews/v11_running_changes_log_20260427.md` (v11 walk-level decision log, 812 lines)
- `docs/reviews/s5_drift_diff_20260501.md` (cold-read drift diff)
- `docs/reviews/s5_independent_outline_20260501.md` (cold-read §5 outline)
- `docs/reviews/round_v11_6_section5_structure_20260501_152904.md` (multi-LLM §5 structure verdict)
- `memory/MEMORY.md` (current state + V11 paper draft section)
- `memory/project_v11_paper_active_editing.md` (V11/V11.5 walk progress)
- Paper drafts: v8 (`docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.clean.md`), v9 (same path), v10.1 (`docs/beyond_recall_v10_1_draft.clean.md`), v11.6 (`docs/beyond_recall_v11_6_draft.md`)

---

## Section 1: The arc of framing evolution

The headline claim has refined across versions. What was framed as "the specification helps where the model knows little" in v8 has narrowed to "the specification produces a uniform post-spec answer quality near 2.46; the lift in raw points is largest where the baseline is lowest" in v11.6. Same data, sharper claim. The trajectory below names every walk-level decision behind that refinement.

### 1.1 v8 → v9 (Apr 23-24)

**Pattern of changes:** post-survey corrections, references redline, structural compression. v9 docx comments file (22 comments) shows mostly mechanical Aarik feedback: rename §2 "SOTA and Industry Benchmarks" (#8), put repetitive content in footnotes (#9, #14, #15, #17, #18, #20), question rubric column phrasing (#16). Three substantive framing items:
- **#1, #2, #3 §1.2 "correct" vs "accurate" language.** Aarik flagging that "correct specification for the correct person" should be reconsidered, possibly "accurate specification for the specified individual." This becomes a thread that resolves in v11 through "specification-effect claim" terminology in §3.6.4.
- **#7 §1.5 alignment section "feels very high level from the previous sections which are more specific and grounded."** The first concrete signal that §1.5 has structural problems — flagged for keeping in discussion, not for removal.
- **#21 §4. Results: "specify the number of facts. Likely need to state conclusion in picture reference."** Headline-numbers-up-front directive that propagates through every subsequent walk.

The §1 introduction structure in v8/v9 carried §1.1 (Recall Is Not Interpretation), §1.2 (What We Tested), §1.3 (What We Found), §1.4 (Why the Gradient Matters for Real Users), §1.5 (Behavioral Alignment and the Human-AI Interaction Problem). v8 §1.4 contained an author N=1 pilot that becomes the load-bearing argument for "structural extrapolation from the historical sample to typical living users." This will be cut in v10.

### 1.2 v9 → v10 (Apr 24)

This is the largest single-version reframe in the project. From `MEMORY.md` "v10 changes from v9 in this session":

**Removed:**
- **§4.1.2 author N=1 pilot REMOVED entirely.** Aarik's call: "don't want to overweight personal data point." Downstream refs in §1.3, §5.3, §5.6, §7 rewritten to rely on 9-of-9 low-baseline + structural extrapolation only. This removes the strongest single-subject living-user data point in the paper. The implication for §5 is that the population-of-relevance argument has to rest on (a) low-baseline 9-of-9, and (b) structural extrapolation from autobiographers being above typical users. No direct living-user evidence in the paper.
- **§1.5 + §5.7 alignment-framing sections REMOVED for circular-reasoning flag.** The alignment framing in v8/v9 §1.5 made the claim that "behavioral alignment is a different property from safety alignment, and the two axes are orthogonal." A reviewer flagged circularity (the paper introduces a benchmark, finds an effect, then claims that effect is what alignment means). Safety content folded into §7.6 as future work. The thesis that "representational accuracy is necessary for behavioral alignment" no longer appears as a §1 claim. **Implication for §5:** the alignment framing is OFF the table for §5.7 closing argument. The §1.4 framing ("anyone who uses AI") is the substitute, and it is positioning, not philosophical.
- **§3.7.7 LLM-as-judge disclosure REMOVED.** Canonical limitation now lives in §6.2 only (down from 6 places of redundancy to 4 distinct purposes).

**Moved:**
- **§4.5 Letta MOVED to Appendix F.** Body trimmed 14,347 → 2,567 chars; brief summary + headline-result blockquote remain in §4.5 body. v11.5 walk later restores §4.5 as a longer body subsection with the new semantic-duplication finding.

**Added (sensitivity scaffolding):**
- **§4.1 Battery-composition sensitivity.** Multiple regression with LITERAL_RECALL fraction (partial slope = −0.88); subset regression GPT-5.4-only: −0.89; baseline survives both controls. This is defensive scaffolding against "is the gradient an artifact of question-type composition?"
- **§4.1 Coupling-free reframing.** **The single most important framing decision in v10.** GPT-5.5 caught Δ-on-baseline coupling. C4a-level slope = +0.04 [−0.25, +0.33], R² = 0.008. Permutation test p = 0.77. Honest reframing per running-changes log: *"spec produces uniform C4a ceiling near 2.46, not differential treatment heterogeneity."* Substantive finding survives; framing changed. The pre-coupling reading was "the spec helps low-baseline subjects more than high-baseline" (treatment heterogeneity). The post-coupling reading is "the spec brings every subject to roughly the same post-spec quality, and the lift in raw points is largest where the baseline is lowest." Same data, different mechanism. **Implication for §5:** §5.2 must lead with the leveler/uniform-quality reading, not with the heterogeneity reading. The treatment-heterogeneity phrasing is rejected for being a coupling artifact, not just out of style.
- **§6.3 Pipeline variance QUANTIFIED.** 3-subject probe (Sunity Devee, Yung Wing, Augustine), 3 reruns each. Pooled SD = 0.10 = 17% of cross-subject SD. Augustine sign flips on 2/3 reruns (mid-baseline within uncertainty band).

**Reframed:**
- **§1.3 callout box, §4.1 visual walkthrough, all 10 figure captions REWRITTEN conclusion-led with grounded numbers.** v9 had narrative figure captions; v10 has lead-with-conclusion captions.
- **Wrong-spec gap softened.** Lead with adversarial −0.25 control; random-derangement +0.22 vs. correct +0.35 framed as "softer probe" rather than as the headline mechanism finding. The hardest evidence for content-vs-template separation is the adversarial wrong-spec, not the random derangement.
- **Six-model coverage scoping HONESTY.** Main study Haiku-only across 14 subjects; 4 additional response models in Tier 2 cross-provider replication on 3 subjects only. v9 had implied broader coverage.
- **Memory-system additivity:** "3 of 4 commercial systems" propagated everywhere (was inconsistent at "all 4").

**Added (standard practices):** §8 Data/code/repro + §9 References + Author affiliation + Funding + Conflicts + License + Acknowledgments.

### 1.3 v10 → v10.1 (Apr 25-27)

Incremental refinements, not a wholesale reframe. From `MEMORY.md` "Net change from v10.1 to v11":
- HIGH/MEDIUM/LOW/UNRESOLVED claims cataloged at `docs/research/v11_confidence_catalog_20260428.md`. This becomes the source of truth for every paper claim's evidentiary tier from v11 forward.
- All v10 headline claims carry forward unchanged.

### 1.4 v10.1 → v11 (Apr 27-28)

The major framing reframes table from `project_v11_paper_active_editing.md`:

| From | To | Why |
|---|---|---|
| Spec as additive on top of memory systems | Spec interacts with retrieval | Additivity framing collapsed under review pressure; interaction model is more honest about what spec does |
| Gradient as supporting evidence | Gradient as load-bearing structural finding | Cross-subject baseline gradient elevated to primary structural claim |
| Magnitude-of-lift as headline | Category-shift as headline | Low-baseline subjects crossing the 2.4 threshold is the more defensible and load-bearing result |
| Population framed as research subjects | Population as "anyone who uses AI" / "broad technology" | Widens implications; positions spec as a broad technology rather than a narrow tool |

**Other v11 changes:**
- §1.3 v5 wholesale rewrite (C16-C49). Lede: "Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least."
- §1.4 v2 wholesale rewrite (C50-C52). Renamed "What this implies." "Why the gradient matters" framing dropped. "What we did not prove" disclaimer paragraph removed entirely. New framing: "broad technology like email / cell phones," "population of importance is anyone who uses an AI system," autobiographers as imperfect proxy, 99% frontier-low-baseline observation.
- §2 restructured (renamed "Prior Work, Industry Benchmarks, The Fifth Target"). New §2 lede names the four existing measurement targets and announces representational accuracy as the fifth.
- §4.1.1 → §4.6.4 moved/renumbered (Franklin moved from main results to robustness/sensitivities).
- §4.7 new section added (closing paragraph bridging into §5).
- "Win rate" → "per-question improvement rate" rebrand globally (C10/C11).
- §1.4 "everyone uses AI" → "the population of typical AI users" / later "population of relevance" softening.

**Phase 2c predicate ablation, Wins-analysis pipeline, held-out leakage investigation** all landed in v11. Heuristic-level pattern-activation claim FALSIFIED. Eight framing-pivot edits applied (R1-R5 + Pivot 8 + wrong-spec elevation + Appendix B.8 predicate ablation).

### 1.5 v11 → v11.1/v11.2 (Apr 28-29)

Annotation walks (Word-doc comments). Locked §1.1, §1.2 light polish, §1.3 v5 rewrite to "Step-changes, not nudges" frame, §2 restructure to "Prior Work, Industry Benchmarks, The Fifth Target" with §2 lede announcing representational accuracy as the fifth target. **B12 forward-reference flagged:** add to §5 closing the framing that intentional individual-specificity is what current AI memory and human-AI interaction research is missing. (This is queued for §5.7 / §5.8.)

### 1.6 v11.2 → v11.5 (Apr 29-30)

Live walk through §3 and substantially all of §4. Major locks:
- **§3.6 simplified rubric.** Hamerton example column dropped from rubric table.
- **§3.6.2 cross-anchor interpretation rule** named as term-of-art. Multi-anchor crossings block with three real verbatim examples.
- **§3.6.4 specification-effect claim** defined as opening sentence (italicized term-of-art).
- **§3.6.6 Refusals are not cleanly distinguished** (renamed from "Abstention is not cleanly distinguished"). Refusal/abstention established as equivalents.
- **§3.7 unified-brief expansion** with implicit-integration framing.
- **§4 lede full rewrite** to mirror abstract: prediction reframed as the test of representational accuracy (not the goal). Names Franklin as layman-recognizable high-baseline example.
- **§4.1.1 NEW** per-question baseline engagement and worked rubric example. Verbatim Seacole Q2 demonstration across rubric bands 1, 2, 4, 5.
- **§4.1.2 Franklin moved here** (from §4.6.5). Aarik's read: "Franklin demonstrates the gradient at the high-baseline end, not an apparatus robustness check."
- **§4.4.1 cross-system retrieval overlap subsection.** Headline: providers do NOT converge on which facts are most relevant given identical input. Mean Jaccard 0.083 across 5 systems on shared 10-fact pool; ~1-2 of 17 union facts shared per pair. Confirmed under semantic similarity at every threshold tested in §4.6.5.
- **§4.4.2 Three patterns** (interpretive supply, over-theorization, spec-induced refusal) named upfront.
- **§4.5 Letta** restored to longer body subsection (previously trimmed to ~3 paragraphs in v10) with new semantic-similarity duplication analysis: at Babur, 56.1% of sentences have a near-paraphrase at cosine ≥ 0.85, 35.2% at ≥ 0.95.
- **§4.6 5-subsection structure** + closer (Franklin moved out to §4.1.2).
- **§4.7 Summary** restructured from prose to two bulleted lists (four findings, five robustness checks).
- **Retrieval-divergence finding ELEVATED to §1.3 7th headline.** Per Aarik: this finding "calls into question what the point of [the recall] benchmark is" and deserves headline-finding status. Originally framed alarmist ("calls into question what those benchmarks are actually measuring"), softened on the same walk to "recall benchmarks measure recall (which is what they should measure); representational accuracy operates at the interpretation layer."
- **New Appendix B.10** for pre-vs-post-hoc tagging.

### 1.7 v11.5 → v11.6 (May 1, this session)

**§1-4 tempering pass** (5 surgical fixes per multi-LLM convergence):
1. Sycophancy: "by construction cannot be passed by sycophancy" → "reduces the risk of sycophancy."
2. Gradient slope coupling + leveler framing: §4.1 "**The specification as a leveler**" callout NAMED. The affirmative reading: spec brings every subject toward 2.46 across baselines, equity property, portable across long-tail users.
3. Compression "matches or exceeds" → "recovers most of." §1.3 lead concretized to "5x to 80x smaller context length." Hamerton boundary-case note (only subject where spec beats raw).
4. Wrong-spec v1/v2 convention. v2 = standard randomization control, v1 = adversarial stress test designed to maximize the wrong-spec effect. Negative −0.25 result is stronger evidence than v2's near-baseline +0.15.
5. Pre-registered vs post-hoc labeling. Appendix B.10 with 17-row table cataloguing every load-bearing analysis result.

**Then the §5 cold-read pass** (this session) produced the structural verdict that drives the rest of this brief.

---

## Section 2: What Aarik has consistently rejected

Patterns of cuts across multiple versions. Each row names what was rejected, when it was first cut, and what replaced it.

### 2.1 "Wins" / "beats" / "crushes" / "outperforms" terminology

**First cut:** v9/v10 redline pass, scrubbed in v10. Re-flagged at v11 cursory-review (`v11_cursory_review_20260428.md` issue #9): "wins" / "multi-anchor wins" / "sometimes wins and sometimes loses" replaced with "extreme upward anchor crossings" / "multi-anchor jumps" / "sometimes increases representational accuracy and sometimes does not."

**Replaced with:** "increases in representational accuracy," "extreme upward anchor crossings," "multi-anchor jumps," "produces a larger delta than."

**Aarik's exact words (2026-04-28, wins-analysis pivot):** "we committed to evaluating on the mean, we dont use the term WIN remember? should be using increase representational accuracy or another term."

### 2.2 Em-dashes in body prose

**First cut:** v6 → v7 (v6 had 341 em-dashes; v7 baseline). Continuously enforced.

**Replaced with:** Period, colon, comma + conjunction, parentheses. Sentence structure changes, not punctuation.

**Standing rule** from `feedback_no_em_dashes.md`: "almost sickeningly... LLM tell."

### 2.3 The §1.5 alignment fold (behavioral alignment as orthogonal axis)

**First cut:** v9 → v10. Removed for circular-reasoning flag.

**Replaced with:** §7.6 future-work pointer (safety probing of behavioral specifications). The alignment framing is OFF the table for §5.7 closing argument. The substitute is the §1.4 "anyone who uses AI" / "broad technology" framing — positioning, not philosophical.

**Implication for §5:** Do not resurrect the safety-vs-personalization-axis framing in §5.7. The closing argument runs on population of relevance + new-layer claim, not on alignment-axis orthogonality.

### 2.4 §4.1.2 author N=1 pilot

**First cut:** v9 → v10. Aarik's call: "don't want to overweight personal data point."

**Replaced with:** Structural extrapolation only. 9-of-9 low-baseline data + autobiographers-are-above-typical-users argument. No direct living-user data in the paper.

**Implication for §5:** §5.2 (gradient + population) cannot lean on direct N=1 living-user evidence. The argument is structural: low-baseline 9-of-9 + autobiographer-baselines-are-the-floor + AI deployment population is "anyone who uses AI."

### 2.5 Differential treatment heterogeneity reading of the gradient

**First cut:** v10. GPT-5.5 review of v10 caught Δ-on-baseline coupling. C4a-level slope = +0.04 [−0.25, +0.33], R² = 0.008. Permutation test p = 0.77.

**Replaced with:** "spec produces uniform C4a ceiling near 2.46; lift in raw points is largest where baseline is lowest." Reframed as "**the specification as a leveler**" in v11.5/v11.6 §4.1 callout.

**Implication for §5 (this is critical):** §5.2 must lead with the leveler/uniform-quality reading. The treatment-heterogeneity reading ("the spec helps low-baseline more than high-baseline") was rejected for being a coupling artifact, not just for stylistic reasons. A §5 paragraph that reaches for the "spec helps low-baseline more" phrasing is reaching for an explicitly-rejected framing. The post-spec mechanism is uniform-quality + opportunity-distribution, not differential treatment.

### 2.6 Additivity framing for memory-system composition

**First cut:** v10.1 → v11. Per `project_v11_paper_active_editing.md`: "additivity framing collapsed under review pressure; interaction model is more honest about what spec does."

**Replaced with:** "Spec interacts with retrieval." Three patterns (interpretive supply, over-theorization, spec-induced refusal). Aggregate Δs are small; per-question pattern is where the action is.

**Implication for §5:** §5.4 must use the three-patterns framing, not the "additive on top of retrieval" framing. The aggregate Δ on each system is a balance of patterns, not a clean additive boost. C153 in the running-changes log: "spec lets retrieval-based memory systems handle question types they weren't designed for."

### 2.7 Magnitude-of-lift as headline

**First cut:** v10.1 → v11. Per `project_v11_paper_active_editing.md`: "low-baseline subjects crossing the 2.4 threshold is the more defensible and load-bearing result."

**Replaced with:** Category-shift as headline. The 2.4 threshold (between rubric anchor 2 = "right topic, wrong prediction" and anchor 3 = "right domain, no specifics") is the qualitative gate. 55.0% of low-baseline questions cross at least one anchor upward. **In v11.6, multi-anchor crossings reframed as transformations not percentages** (1-in-5 / 1-in-17 with qualitative anchors).

**Implication for §5:** §5.2 should foreground category-shift (1-in-5 questions cross two-or-more bands; 1-in-17 cross three-or-more) over magnitude (Δ +0.89). Mean Δ stays primary evaluation metric, but category-shift is the "what does this look like to a reader" framing.

### 2.8 "Population of importance" → "Population of relevance"

**First cut:** v11.2 → v11.5 (per `v11_running_changes_log` line 619). "Population of importance" → "population of relevance" (consistent with §1.2/§1.1).

**Replaced with:** "population of relevance" everywhere. C150 in queue: "everyone uses AI" framing softened to "the population of typical AI users."

### 2.9 Lead-burying under methodology

**First cut:** §1.3 v5 wholesale rewrite (C16-C49) in v11. Continuously enforced.

**Aarik's directive (running-changes log line 76):** "layperson, draws any reader, single number anchor, technical detail in §4." All numerical claims preserved exactly per v11 confidence catalog; bullets rewritten qualitative-first; numbers italicized to visually anchor "one short line on the numbers."

**Implication for §5:** Every §5 subsection lede should lead with the interpretive claim, not with the number that supports it. Numbers go in italicized stat lines or footnotes.

### 2.10 GTM language in body prose

**First cut:** Continuous. Reinforced at every review.

**Replaced with:** Plain declarative scientific framing. From `feedback_no_gtm_language.md`: "Promotional verbs undercut the credibility of the empirical claim."

### 2.11 Inflated-scope claims

**First cut:** v11 cursory-review (issue #10): "floor-not-ceiling claim scoped to 'C5 to C4a comparison on the full 14-subject panel' with explicit C4-to-C4a parenthetical." Continuously: every claim must be scoped to the data that supports it.

**Implication for §5:** Cross-anchor improvements scoped to specific condition pairs. Compression ratios scoped to specific subject (Hamerton boundary case is the only subject where spec beats raw corpus). Multi-subject living-user replication named in §7 as the highest-priority follow-up, not asserted as already done.

### 2.12 Re-stating positioning in Discussion (current §5.1 Anti-Pattern)

**Flagged this session (2026-05-01):** §5 drift diff identifies current §5.1 (Anti-Pattern) as redundant with §2.1. Multi-LLM panel verdict (Mistral, GPT-5.5, Opus 4.7): "The Anti-Pattern subsection is redundant with §2.1 and does not interpret §4 findings." Recommendation: "Either trim aggressively (one paragraph naming the four anti-patterns by reference to §2.1) or move out of §5 entirely."

**Implication for §5:** §5.1 in v11.6 will become a synthesis lede that integrates the seven headlines into one positive claim, NOT a re-statement of §2.1. The Anti-Pattern material either becomes one paragraph at the top of §5.1 or moves out entirely.

### 2.13 Practical-Implications scope-creep into §7 territory

**Flagged this session (2026-05-01):** §5 drift diff: "§5.5 currently runs lines 1581–1684 and contains: context budget, authoring cost, per-query cost, dynamic activation (full architecture), modifiability, temporality, topic decomposition, piecewise component analysis, update cadence, positioning against alternatives, infrastructure properties (4 named), per-user calibration framing (3 paragraphs)." Most flagged as future work or deployment proposals, not findings the data settle.

**Implication for §5:** Cut current §5.5 by ~50%. Keep tight production-deployment-tractability paragraph anchored to §4.2 compression. Move full dynamic-activation architecture, modifiability bullets, temporality bullets, topic decomposition bullets, piecewise component analysis (catalog L1 — future work only), update-cadence bullet to §7.

### 2.14 "Dynamic spec activation is a requirement" language

**Flagged this session (2026-05-01):** §5 drift diff OVERWEIGHTED-2: line 1569 "The three patterns together imply dynamic spec activation is a requirement for production response quality... it is a requirement for ensuring that the specification's effect on any given response is net positive." Catalog grounding: not data-settled. Three-patterns finding is HIGH-confidence on existence; the production-architecture implication ("requirement") is not.

**Replaced with:** "the data point toward dynamic serving as the next architectural step" or "the three patterns together suggest production response quality could be improved by dynamic activation, which §7.4 develops."

---

## Section 3: What Aarik has consistently elevated

Patterns of pushes across multiple versions. Each row names what was elevated, when it became load-bearing, and why.

### 3.1 "AI never knew, not AI forgot" framing

**Became load-bearing:** Pre-paper (in `feedback_core_problem.md`, MEMORY.md). Carried forward into every paper version.

**Why:** This is the structural diagnosis half of the thesis. Memory systems solve forgetting. The behavioral specification solves never knowing. The two are different problems with different solutions; the field has been building solutions to the first while assuming they address the second.

**Implication for §5:** §5.3 (Retrieval is not interpretation) should surface this distinction explicitly. From `feedback_core_problem.md`: "AI never knew in the first place / No AI agent has a model of how the person it serves actually thinks, decides, and communicates / Not preferences, not history — behavioral patterns that determine whether the AI's actions align with what the person would actually do."

### 3.2 Representational accuracy as the through-line term

**Became load-bearing:** v8/v9. Stable since.

**Why:** Names the AI-side property the paper measures. Distinct from recall, preference matching, persona consistency. The fifth target.

**Reinforced in v11:** §2 retitled "Prior Work, Industry Benchmarks, The Fifth Target." §2 lede announces representational accuracy as the fifth target. §3.1 (Methods) renamed "Operationalizing representational accuracy."

### 3.3 Prediction is the test of representational accuracy, not the goal

**Became load-bearing:** Pre-v8 (in `feedback_prediction_framing.md` and CLAUDE.md line 30). Reinforced in v11.5 §4 lede rewrite ("prediction reframed as the test of representational accuracy, not the goal").

**Why:** The product is accurate representation of how someone reasons. Prediction is how we measure that accuracy. If the representation is accurate, prediction follows. Never frame prediction as the end goal.

**Implication for §5:** §5.1 synthesis lede should keep the through-line: representational accuracy is what the spec produces; prediction is how we check; the seven findings together establish a property of the layer, not a property of the prediction task.

### 3.4 Gradient as load-bearing structural finding

**Became load-bearing:** v10.1 → v11 (per `project_v11_paper_active_editing.md`: "Gradient as supporting evidence → Gradient as load-bearing structural finding").

**Why:** The gradient is where the paper's strongest empirical signal lives. Reframed in v10 from "differential treatment heterogeneity" (rejected as coupling artifact) to "uniform post-spec quality + opportunity distribution" (the leveler framing).

**Implication for §5:** §5.2 (gradient + population of relevance) is the load-bearing subsection of §5. Read both ends of the gradient (low-baseline 9 of 9 with mean Δ +0.89, and Franklin's high-baseline reversal) as evidence for the same mechanism: spec produces a fixed quality of answer, and the room it has to help is governed by where the baseline sits.

### 3.5 Category-shift / multi-anchor crossings as the headline

**Became load-bearing:** v11. Per `project_v11_paper_active_editing.md`: "Magnitude-of-lift as headline → Category-shift as headline."

**Why:** Crossing the 2.4 threshold is qualitative, not numerical. "Right domain" vs "wrong prediction" is what a reader can picture. Mean Δ +0.89 is what a reviewer can compute.

**Reinforced in v11.5/v11.6:** Multi-anchor crossings reframed as "transformations not percentages" (1-in-5 / 1-in-17 with qualitative anchors). 18% of low-baseline questions cross two or more bands; 6% cross three or more.

**Implication for §5:** §5.2 should foreground category-shift over magnitude. Each multi-band crossing is "one question the AI was unable to engage with at all, transformed into a grounded answer."

### 3.6 Provider divergence on retrieval relevance (7th headline)

**Became load-bearing:** v11.5 (Apr 30 - May 1). Originally surfaced post-hoc; elevated to headline status mid-§4 walk.

**Why:** Aarik in S118: this finding "calls into question what the point of [the recall] benchmark is." Mean Jaccard 0.083 across 10 system pairs on shared 10-fact pool; 52.3% of (system pair, question) instances share zero top-10 facts; 71.4% share one or fewer; mean pairwise overlap 8.3%. Confirmed under semantic similarity at every threshold tested in §4.6.5.

**Tone calibration this session:** Original framing "calls into question what those benchmarks are actually measuring" softened to "recall benchmarks measure recall (which is what they should measure); representational accuracy operates at the interpretation layer." Aarik's instruction: don't be alarmist; recall is a legitimate measurement of recall. The argument is not that recall benchmarks are wrong; the argument is that recall is one property and representational accuracy is a different property.

**Implication for §5 (CRITICAL — this is the new subsection):** §5 must carry retrieval-divergence as a load-bearing discussion thread, not a footnote. Per cold-read drift diff: "the single most important addition is the retrieval-divergence subsection." The implication §5 should draw out: recall accuracy and interpretive relevance are different properties. A system can saturate recall and still pick a different fact than another system from the same pool when asked which fact matters for a specific interpretive question.

### 3.7 The "leveler" affirmative reading of the gradient

**Became load-bearing:** v11.5/v11.6 §4.1 walk. Named explicitly in v11.6 §1-4 tempering pass (Fix 2): "**The specification as a leveler**" callout in §4.1 after the existing "What the gradient is actually showing" paragraph.

**Why:** The affirmative reading: spec brings every subject toward 2.46 across baselines, equity property, portable across long-tail users.

**Implication for §5:** §5.2 should lead with this affirmative reading. From the voice/positioning brief Section 2.6: "the leveler reading should be surfaced as an equity property, not a market expansion claim. The argument: post-spec, prediction quality is uniform across baselines. Pre-spec, prediction quality tracks how well-known the subject is. The interpretive layer collapses the famous-vs-obscure gradient."

### 3.8 Letta architectural-ceiling observation (semantic-duplication finding)

**Became load-bearing:** v11.5 (Apr 30 - May 1). New analysis: at Babur, 56.1% of sentences have a near-paraphrase at cosine ≥ 0.85, 35.2% at ≥ 0.95.

**Why:** The verbatim figure of 25.4% understates duplication. Semantic-similarity captures the architectural ceiling more honestly: an architecture that produces its representation by self-editing rather than by retrieval converges on the same interpretive target as the Behavioral Specification on a small N=3 sample, but has a scaling ceiling that the unified-brief specification does not share. Block grows ten-fold; spec holds at 34K-40K characters.

**Implication for §5:** New §5.5 subsection (Architectural ceilings). Two paragraphs. First: convergence finding as positive evidence for the validity of the interpretive-layer target (two architectures converge on it independently). Second: scaling-ceiling finding as a specific cost of the self-editing path that the static-specification path avoids. Explicit "N=3, exploratory, future work" hedging consistent with confidence catalog. The current §5 carries neither thread.

### 3.9 Layman-accessibility threshold

**Became load-bearing:** Continuously, but most explicitly during §1 walks (C16-C49 §1.3 v5; C50-C52 §1.4 v2; A30 §1.3 layperson rewrite). Reinforced during §3 walk (§3.6.6 layman-ization, §3.7.3 cross-anchor rule layman-ization).

**Aarik's directive:** "layperson, draws any reader, single number anchor, technical detail in §4." A reader who reads only §1 should be able to follow the paper's argument without flipping to §4.

**Reinforced this session for §5:** Aarik's instructions for §5 include "Need to be conversational, formal" register and "§5 needs to stand alone — someone who reads only §1 should follow §5."

**Implication for §5:** Conversational, formal register. Each subsection should make sense to a reader who has not yet flipped to §4. Cross-references to §4 are pointers, not load-bearing prerequisites.

### 3.10 Population-of-relevance argument widened

**Became load-bearing:** v10.1 → v11. Per `project_v11_paper_active_editing.md`: "Population framed as research subjects → Population as 'anyone who uses AI' / 'broad technology'."

**Why:** AI is becoming a broadly used technology, comparable to email or mobile phones in how widely it touches daily decisions. The population of relevance is anyone who uses or will use an AI system.

**Reinforced in v11.5:** The C5 baseline distribution (41% refusals at C5=1.00, 21% strong) shows the bimodal per-question echo of the cross-subject gradient. From `s5_independent_outline_20260501.md` §5.2: "Even people whose work is in pretraining sit near the rubric floor."

**Implication for §5:** §5.2 third paragraph should connect the cross-subject gradient to the per-question bimodal C5 baseline as the deployment story.

---

## Section 4: The §5 trajectory specifically

This is the section that gets consulted most. The §5 drift-diff and the v11.6 multi-LLM panel verdict are the most actionable inputs for the §5 walk itself.

### 4.1 §5 was largely written before recent §4 elevations

Per `s5_drift_diff_20260501.md` summary: "The current §5 was written before three §4 changes landed: (1) the §4.4.1 retrieval-divergence finding was elevated to a 7th headline finding in §1.3 with full subsection in §4.4.1 and sensitivity check in §4.6.5; (2) the §4.5 / Appendix G Letta case study acquired a semantic-duplication observation that bears on architectural ceilings; (3) Franklin moved from §4.6.5 to §4.1.2 as the high-baseline end of the gradient."

Current §5 has four primary issues:
1. The retrieval-divergence finding is absent.
2. The Letta architectural-ceiling reading is absent.
3. §5.5 (Practical Implications) is overweighted relative to what §4 establishes and contains substantial content that belongs in §7.
4. §5.1 (Anti-Pattern) is positioning material that re-states §2.1 rather than interpreting §4.

### 4.2 Current §5 structure (v11.5/v11.6 baseline before walk)

| Subsection | Lines (v11.5) | Title |
|---|---|---|
| §5 lede | 1497–1499 | Discussion intro |
| §5.1 | 1501–1517 | The Anti-Pattern: What Behavioral Specification Is Not |
| §5.2 | 1521–1539 | What the study demonstrates |
| §5.3 | 1543–1553 | The population of relevance |
| §5.4 | 1557–1577 | Content specificity and mechanism |
| §5.5 | 1581–1684 | Practical implications (longest by far, ~100 lines) |
| §5.6 | 1688–1708 | What the study does not settle |

### 4.3 Multi-frontier panel verdict on §5 structure (2026-05-01)

From `round_v11_6_section5_structure_20260501_152904.md`. Three reviewers (Mistral Large, GPT-5.5, Claude Opus 4.7). Convergence: rebuild §5 with **7 subsections**.

| Subsection | Title | Drives | Notes |
|---|---|---|---|
| §5.1 | Synthesis lede | §1.3 (seven headlines), §4.7 | Replaces current Anti-Pattern. Integrates seven headlines into one positive claim. 3-4 paragraphs. |
| §5.2 | Gradient + population of relevance combined | §4.1, §4.1.2, §4.1.1, §1.4 | Folds current §5.3 (population) into §5.2 (gradient). Lead with leveler reading. |
| §5.3 | Retrieval is not interpretation (NEW) | §1.3 7th headline, §4.4.1, §4.6.5, §2.1 | The single most important addition. HIGH-confidence empirical evidence. |
| §5.4 | Composition with retrieval (three patterns) | §4.4.1, §4.4.2, §4.4.3 | Soften "is a requirement" to "data point toward dynamic serving as the next step." |
| §5.5 | Architectural ceilings via Letta (NEW, short) | §4.5, Appendix G | Two paragraphs. Explicit "N=3, exploratory" hedging. |
| §5.6 | Wrong-spec mechanism + hedging | §1.3 4th headline, §4.3, §4.6.4, §2.4 Jain | Content effect rules out sycophancy; transfer of patterns observed; honest unresolved (which structural feature is active ingredient). |
| §5.7 | Compression and deployment tractability | §1.3 3rd headline, §4.2, §1.4 | Tight. Hamerton boundary case. Deployment proposals to §7. |
| §5.8 | Closing argument | §1.1 / §1.4 (positioning), §4 in toto, §7.4 / §7 | One to two short paragraphs. Conclusion-led. |

(Mistral Large proposed 8 subsections including §5.8 closing as separate; GPT-5.5 had 7 subsections combining closing into §5.7. Final structure pending Aarik decision; likely 7 subsections with closing as §5.7 lede paragraph or as separate §5.8.)

### 4.4 Demoted from current §5 (multi-LLM convergence)

- **Letta** demoted to in-text paragraph in current §5.5 (or absent); elevated to its own §5.5 subsection in proposed structure.
- **Current §5.6 ("What the study does not settle")** → moves to §6 Limitations or folds into §6.1.
- **Current §5.5 (Practical Implications)** cut by ~50%. Production-architecture proposals (dynamic activation full architecture, modifiability bullets, temporality bullets, topic decomposition bullets, piecewise component analysis, update cadence) to §7.

### 4.5 What §5 needs to inherit from v11.5/v11.6 evolution

**The leveler framing (§5.2 should lead with this affirmative reading).** From v11.6 §1-4 tempering pass Fix 2: spec brings every subject toward 2.46 across baselines, equity property, portable across long-tail users. NOT "the spec helps low-baseline more than high-baseline" — that is the rejected coupling-artifact reading.

**The multi-context-lens framing (§5.1 already has this in ¶2).** The behavioral-specification layer is distinct from facts/corpus/retrieval and complements all three. Not a competitor; an additional dimension.

**Honest construct-validity hedge (§5.1 ¶3 has this; §5.7/§5.8 closing also flags it).** From `feedback_outreach_honesty.md` and CLAUDE.md anchors: claim the directional empirical finding plainly. Name the scope (subjects modeled from biography/letters; LLM-graded predictions; single primary response model). Name the highest-priority follow-up (human validation, multi-subject living-user replication) as the next step, not as a hedge that softens what was found.

**Pre-registered vs post-hoc distinction (§1.3 provider-divergence tagged; §5 inherits).** From v11.6 §1-4 tempering pass Fix 5. §5.3 retrieval-divergence subsection should be honest that this finding surfaced post-hoc and survives pre-registered semantic-similarity sensitivity check. §5.5 Letta should be honest that this is N=3 exploratory.

**Three-patterns framing for memory-system composition (NOT additivity).** From C153 in v11 walk: "spec lets retrieval-based memory systems handle question types they weren't designed for. Aggregate Δs are small; per-question pattern (Pattern 1/2/3) is where the action is."

**Category-shift over magnitude.** §5.2 should foreground 1-in-5 / 1-in-17 multi-band crossings over Δ +0.89.

### 4.6 What §5 must NOT do (from cold-read outline)

- Do not assert per-predicate or per-anchor mechanism (catalog U1, L1; Phase 2c predicate ablation falsified the heuristic-level claim).
- Do not claim the spec uniquely lifts low-baseline more than high-baseline as a treatment-heterogeneity finding (catalog "should not claim"; the coupling is real and the §4.1 framing is "uniform post-spec answer quality + opportunity distribution," which §5 should preserve).
- Do not use "wins" or "big wins" terminology.
- Do not assert generalization from autobiographers to all AI users as empirical (catalog L3); it is constructive and must be framed that way.
- Do not introduce new findings or new analyses; §5 is interpretation of §4, not extension of it.
- Do not anticipate §6 (limitations) or §7 (future work) at length; pointers are fine, redoing them is scope creep.

---

## Section 5: How Aarik's session-level feedback has evolved (this session, May 1)

Calibration data points for the §5 walk, from Aarik's comments during this session:

- **Lead-burying frustration (multiple times).** Per the user's framing instruction in this task: "We've been inconsistent about surfacing key findings; this brief is the calibration reference."
- **Term consistency issues.** "subject vs person" and "layer vs Behavioral Specification" need declared equivalents and consistent use within and across paragraphs.
- **"Don't be alarmist" tone calibration on retrieval-divergence.** Original framing "calls into question what those benchmarks are actually measuring" softened to "recall benchmarks measure recall (which is what they should measure); representational accuracy operates at the interpretation layer." Aarik's instruction: recall is a legitimate measurement of recall.
- **"Conversational, formal" register for §5 lede.** Direct interpretive judgment, not safe summary; but formal academic register, not GTM voice.
- **"§5 needs to stand alone."** Someone who reads only §1 should follow §5. Cross-references to §4 are pointers, not load-bearing prerequisites.
- **"Don't bury anchor improvement rate."** The 55% / 78.6% / 1-in-5 / 1-in-17 numbers should not get hidden behind methodology recap.
- **"Add interpretation-heavy lens for memory-system layering" (caught by Aarik this session).** The three-patterns framing in §4.4.2 should be honored in §5.4 — not just "the spec helps on retrieval" but "the spec lets retrieval-based memory systems handle question types they weren't designed for." Interpretation-heavy is the lens.

---

## Section 6: The implicit thesis Aarik wants §5 to land

Direct quote from this session:

> "I believe this study is pointing out a critical issue in how the industry is operating today and that this interpretive framing can fundamentally change how we approach memory. I don't want that to be undersold by this paper."

Two halves of this thesis:

1. **Diagnosis:** the industry today optimizes for recall and treats memory as fact retrieval. That measures one thing; it does not measure whether the AI has a model of how the person thinks. The result is that personalization quality varies by how well-known the person is, not by how well the AI represents them.
2. **Constructive:** the interpretive layer (the behavioral specification) is a fundamentally distinct dimension of personalization. It is not a competitor to retrieval. It sits on top of any retrieval substrate and changes what the retrieved facts mean for the user.

What this implies for §5.7/§5.8 closing argument:

- **The paper's bigger claim is industry-positional, not just empirical.** The closing should make the structural argument visible: this is not a "we found a small effect" paper; it is a "we identified a layer the field has not been measuring" paper.
- **Interpretive framing as a fundamental shift, not an incremental improvement.** The closing should land that this is a different axis of personalization, not a better point on the existing axis.
- **Without overselling.** Directional empirical evidence of a layer that exists, can be built, and matters. The data establish that the layer is measurable, content-specific, structurally compressible, and complementary to retrieval. Multi-subject living-user replication, differentiated rubrics, dynamic-serving architectures are what the next phase looks like.
- **§5.7/§5.8 should land that big claim while honoring the construct-validity hedge.** From the v11 confidence catalog: this is HIGH-confidence on H1-H6 (existence, gradient, compression, content-specificity, three-patterns, hedging-reduction), MEDIUM on M1-M2 (spec-most-useful-where-pretraining-thinnest, three-patterns-by-system), LOW on L1-L3 (which structural feature is active ingredient, dynamic-serving-as-requirement, generalization to all users), UNRESOLVED on U1-U3.

The §5.7/§5.8 closing should not announce that the paper has settled this question. It should state that the paper provides the first measured evidence that the layer exists, can be built, can be served, and matters for behavior, and that everything from differentiated rubrics to dynamic-serving architectures to multi-subject living-user replication is what the next phase looks like.

---

## Closing note

This brief exists to give the §5 walk a concrete handle on the trajectory. Each subsection of §5 inherits something from the evolution captured here. The single most important inheritance is the leveler reframing from v10 (Section 2.5 / Section 3.7): §5.2 must lead with the affirmative uniform-quality reading because the alternative reading was rejected as a coupling artifact, not because the brief preferred it stylistically. A §5 paragraph that reaches for "the spec helps low-baseline more than high-baseline" phrasing is reaching for an explicitly-rejected framing.

The second most important inheritance is the §5 cold-read structural verdict (Section 4.3): §5 needs the retrieval-divergence subsection added, the Letta architectural-ceiling subsection added, the Anti-Pattern collapsed into a paragraph or removed, and Practical Implications cut by ~50% with deployment proposals moved to §7. Multi-LLM convergence is on a 7-subsection structure. The drift between v11.5's §5 and what §1-§4 now establish is real and load-bearing.

The third most important inheritance is the implicit thesis (Section 6): the paper is making an industry-positional claim that recall and representational accuracy are different properties, and that the field has been measuring one and assuming it predicts the other. §5.7/§5.8 must land that claim without overselling. Directional empirical evidence on a controlled benchmark; multi-subject living-user replication is the next step; the field's next move (differentiated rubrics, dynamic serving, living-user data) follows naturally from the finding.
