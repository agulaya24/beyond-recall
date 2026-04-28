# Framing-Implications Report -- Round 1 Draft (2026-04-28)

## Status banner

This is a Round 1 draft, intended for cross-LLM review (Round 2) before any paper edit. The paper's existing structure is the baseline; pivots proposed here are incremental. Three prior framing claims have been wrong: the original "spec lifts low-baseline more" framing was largely a coupling artifact (corrected in v10); Stream X claimed Hamerton's elevated jump rate came from a longer served spec, when in fact Hamerton's served spec is roughly 0.33x the size of globals'; and the deep pattern-activation discriminator analysis (which post-dates both Stream X and the collective review on the predicate-activation claim) shows that the rhetoric-based predicate-mediated heuristic does not discriminate jumps from non-jumping spec-loaded controls. Each pivot in this report includes alternative-hypothesis treatment and a risk profile so the cross-LLM reviewers can stress-test the same evidence the author will see.

---

## Phase 1 + 2 evidence summary

**Phase 1 wins inventory.** Across 18 paired-condition comparisons (8,804 paired-question instances, 4,206 anchor crossings), the headline numbers reproduce the existing v11 §4 framing. C5 to C4a: 43.2% upward crossings, 15.8% downward, 13.0% multi-anchor, 3.7% extreme upward (>=3 anchor jumps). C4 to C4a (low-baseline-9): mean Δ = 0.088. C8 to C9 (low-baseline-8): mean Δ = 0.088. Both the C4a-on-top-of-facts and the C9-on-top-of-corpus deltas round to about +0.09 at the low-baseline-9/8 grain. Both are inside the rubric-band noise floor at the per-subject mean grain but disaggregate into 21-22% question-improvement, 17-19% question-worsening, with median magnitudes near +1.0 and -0.4.

**Phase 2 Stream X (big-wins characterization).** Phase 2a deduplicated 150 raw extreme-upward records into 60 unique (subject, qid) extreme jumps across 14 subjects. Axis distribution: LITERAL_RECALL 28.3% in jumps vs 10.2% panel-wide (2.77x overrepresentation), INTERPRETIVE_INFERENCE 51.7% vs 68.8% (0.75x), REFUSAL_TRIGGERING 20.0% vs 21.0% (0.95x). Pre-response failure mode at C5: FULL_REFUSAL 71.7%, GENERIC_HEDGE 15.0%, CLARIFY_REQUEST 8.3%, OFF_BASE 5.0%. Initial N=20 mechanism audit: PATTERN_PREDICATE 12, INFERENCE_CHAIN 7, ANCHOR_FACT 1, DIRECT_QUOTE_MATCH 0. Subject distribution of the 60 unique jumps: Hamerton 15 (25%), Sunity Devee 8, Fukuzawa 8, Seacole 6, Rousseau 6, Bernal Diaz 3, Ebers 3, Yung Wing 3, Augustine 2, Babur 2, Equiano 2, Cellini 1, Keckley 1, Zitkala-Sa 0.

**Phase 2 Stream Y (within-band shifts and meta-judging).** Pooled missed-signal ratio across 18 pairs: for every 1 anchor crossing the binary metric records, 0.18 additional same-band shifts of +0.5 or larger exist. Direction-agreement curve on C5 to C4a (excluding judge-flat): 74.2% at panel |Δ| 0.1-0.25, 93.3% at 0.25-0.5, 99.9% at >=1.0. Per-judge nonzero per-question Δ rates run 47.2% (GPT-5.4) to 55.7% (Opus). Pairwise Spearman rank correlation between pre and post conditions: C5 to C4a ρ=0.27, C4 to C4a ρ=0.72, C8 to C9 ρ=0.70, C2a to C4a ρ=0.61. Spec-on-baseline (no context) re-orders the question ranking; spec-on-info-rich (facts already there or corpus already there) preserves the order while lifting sub-anchor.

**Phase 2 deep pattern-activation analysis (post-dates the collective review).** Mechanism classification at full N=60 plus a 38-case non-jumping control group, with disconfirmation tests (verdict per case: spec_doing_work, partial_facts_activation, facts_already_activate, mixed, not-grounded, genuine_inference_via_spec). Full-population mechanism distribution: PATTERN_PREDICATE 47 (78.3%), INFERENCE_CHAIN 11 (18.3%), HYBRID 0, ANCHOR_FACT 0, DIRECT_QUOTE_MATCH 0, UNCLEAR 2. Control group: PATTERN_PREDICATE 36 of 38 (94.7%), INFERENCE_CHAIN 2 of 38 (5.3%). The pattern-predicate rhetoric heuristic detects spec-loaded response style, not lift. Fair comparison after excluding the 9 degenerate C5-to-C4 jumps where post equals the disconfirmation reference: spec_doing_work share is 78.9% in jumps (n=38) vs 80.6% in controls (n=36); delta -1.6 percentage points. The author's own conclusion in the deep-analysis report: "the lift mechanism is not pattern activation by itself." INFERENCE_CHAIN is a discriminator at the right grain: 11 of 60 jumps coded genuine_inference_via_spec, vs 2 of 38 controls coded the same. Roughly 1 in 6 extreme jumps shows spec-enabled inference the retrieval cannot ground; that subset is real signal.

**Collective review on the predicate-activation claim (now superseded on the strong reading).** Both reviewers (GPT-5.5 and Gemini Pro) treated the N=20 audit as plausible-but-not-defensible, and both required (a) coding of all 60 cases and (b) predicate-ablation experiments. The deep analysis closes (a) and the answer is negative on the discriminator: pattern-predicate count does not separate jumps from controls. The cautious framing the reviewers proposed pre-discriminator ("evidence favors predicate-mediated, ablations needed") is no longer the right framing because the discriminator test is now in and the rhetoric heuristic does not discriminate.

**Hamerton confound note.** Hamerton accounts for 15 of 60 unique extreme jumps (25%); jump rate 18.75% across the 80-question Hamerton battery vs 8.9% across the 13 globals' 507 questions (2.1x). Stream X attributed this elevation to a longer served spec; the verified spec-length facts invert that attribution. Hamerton served spec 1,918 words (brief only), globals' served spec roughly 5,775 words on average (anchors + core + predictions + brief stack). Hamerton's served spec is roughly 0.33x globals'. The elevated jump rate is real but not from spec length; candidate explanations (legacy battery generator, subject pretraining thinness, predicate density per word, battery question-type composition) have not been disentangled.

---

## Proposed iterative refinements

### Refinement 1. §4.2 -- add "What the aggregate numbers hide" subsection with C4-to-C4a and C8-to-C9 per-question breakdown table

**Current paper state.** The closing block of §4.2 (lines 787 to 792) reads:

> What the aggregate numbers say.
>
> - Every context condition lifts the low-baseline mean by at least one full rubric point over the no-context baseline.
> - The specification alone recovers roughly three-quarters of the corpus-alone lift (spec lift +0.71, corpus lift +0.93) at an order of magnitude to two orders of magnitude smaller context depending on subject.
> - Adding facts to the specification (C4a) produces the same mean as raw corpus alone (both 2.45). Two different compression strategies, same performance, different context shapes.
> - Adding the specification on top of the full raw corpus (C9) adds ~0.05 points on average over raw corpus alone. The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

§4.2.1 then introduces the question-improvement-rate triplet but treats only C5-to-context comparisons.

**Proposed change.** Insert a new sub-block immediately after the "What the aggregate numbers say" bullets (before §4.2.1), titled "What the aggregate numbers hide." Verbatim addition:

> What the aggregate numbers hide. The "spec adds little when corpus is already there" claim survives at the per-subject mean grain; it dissolves at the per-question grain. On the C4 to C4a paired comparison restricted to the 9 low-baseline subjects (351 questions), 21.9% of questions improve on adding the specification while 16.8% worsen; 2.6% of questions cross two or more rubric anchors upward and 1.1% cross three or more upward. On the C8 to C9 paired comparison restricted to the 8 low-baseline subjects with full corpus coverage (312 questions, Babur excluded for context-window reasons), 21.8% improve and 18.6% worsen; 3.8% cross two or more anchors upward and 0.6% cross three or more. Both C4-to-C4a and C8-to-C9 mean Δ round to +0.09 at the low-baseline grain. The aggregate is small because two opposite mechanisms are roughly balancing across questions, not because the specification is uniformly inert. The Pattern 1 / Pattern 2 / Pattern 3 mechanism analysis on Supermemory in §4.4.2 generalizes: spec-on-info-rich produces a bimodal per-question distribution centered at zero, not a unimodal small-positive shift. A per-subject mean is a misleading summary of that distribution.

**Evidence supporting the change.** Wins inventory (`docs/research/wins_inventory_20260428.json`): C4-to-C4a low-baseline-9 has upward 21.9%, downward 16.8%, multi-anchor 2.6%, extreme 1.1%, mean Δ 0.088. C8-to-C9 low-baseline-8 has upward 21.8%, downward 18.6%, multi-anchor 3.8%, extreme 0.6%, mean Δ 0.088. These are locked under the wins inventory's `cross_checks` block (expected = actual). Stream Y bucket distribution (`within_band_shifts_20260428.md`): C4-to-C4a anchor_crossing 37.9%, C8-to-C9 anchor_crossing 40.4%, with same-band-half shifts adding 14% and 12% respectively. Spec-on-info-rich pairs on average have anchor_crossing 40.7% vs spec-on-baseline 60.5%; spec-on-info-rich preserves rank ordering (Spearman ρ = 0.61 to 0.72) where spec-on-baseline re-orders (ρ = 0.27).

**Alternative interpretation.** The bimodal-per-question distribution may itself be a judge-noise artifact: with 5 integer-anchor judges, panel_delta moves in 0.2 increments, and a question that one judge moves up while another moves down can produce same-band noise that looks like opposing mechanisms but is just sampling variance. Stream Y partially rules this out: at panel |Δ| 0.5-1.0, judge-direction-agreement is 93.8% on C5-to-C4a (i.e., when the panel disagrees with itself by half a band or more, a single judge agrees with the panel direction 94% of the time). The signal exists below the binary anchor-crossing metric.

**Risk.** Bimodal-distribution framing was first surfaced on Supermemory (the spec-on-retrieval condition where it was cleanest to read). Generalizing it to C4-to-C4a and C8-to-C9 propagates the same framing to non-Supermemory comparisons; cross-LLM reviewers should check that the specification-as-overlay framing transfers from "spec on top of memory-system retrieval" to "spec on top of facts" or "spec on top of full corpus." The Pattern 1 / 2 / 3 typology was characterized on Supermemory; it has not been independently characterized on facts-only or corpus-only post-conditions.

**Recommendation.** APPLY-AS-DRAFTED for the per-question disaggregation numbers and the bimodal framing. The numbers are locked in `cross_checks`. The framing already lives in §4.4.2 on Supermemory and in §5.4 on the three-pattern story; this addition makes it visible in §4.2 where the small mean Δ is currently the only signal the section gives.

---

### Refinement 2. §4.2 -- C9 vs C8 mean Δ numerical reconciliation

**Current paper state.** §4.2 line 792:

> Adding the specification on top of the full raw corpus (C9) adds ~0.05 points on average over raw corpus alone. The signals overlap; once the model has the full source text, the spec adds little at the aggregate level.

§4.2 table (line 783) reports C8 = 2.45, C9 = 2.59, mean of nine low-baseline subjects, Δ = +0.14. §1.3 and elsewhere the corresponding paragraph appears with Δ ~+0.10. The wins inventory cross_checks lock C8-to-C9 mean_delta at 0.088 on the low-baseline-8 slice (Babur excluded for context window, n=312 questions).

**Proposed change.** Reconcile to one canonical number. The author should choose which slice is the headline: the table's row already reports C9 = 2.59 against C8 = 2.45, which gives subject-mean Δ +0.14 on the n=8 subjects with C9 data; the wins inventory's per-question Δ on the same n=8 subjects (n=312 paired questions) is +0.088. These are not the same statistic. Subject-mean Δ averages first within subject and then across subjects (8 subject means). Per-question Δ is computed at the (subject, qid) grain across all 312 paired questions. The two diverge because subjects with more questions in the matched set carry proportionally more weight in the per-question grain.

The cleanest fix: in §4.2 line 792, replace "~0.05 points" with "+0.09 points (per-question grain on the 8 low-baseline subjects with C9 data; see Stream Y bucket distribution and the C8-to-C9 row in `docs/research/wins_inventory_20260428.json`)." Keep the table's subject-mean of +0.14 as the row delta; add a footnote that subject-mean and per-question grain diverge because of unequal Q counts post-Babur-exclusion. Verbatim replacement for line 792:

> Adding the specification on top of the full raw corpus (C9) adds +0.14 points on the subject-mean low-baseline grain (8 subjects, Babur excluded for context-window reasons) and +0.09 points on the per-question grain over the same 8 subjects (312 paired questions). Both are inside the rubric-band noise floor at the aggregate grain. The signals overlap on average; once the model has the full source text, the spec adds little at the aggregate level. The per-question disaggregation in the next subsection shows the aggregate small Δ resolves into 21.8% improving questions and 18.6% worsening questions, not a uniform small positive shift.

**Evidence supporting the change.** `wins_inventory_20260428.json` `cross_checks` block locks the per-question grain values. The subject-mean +0.14 is computed directly off the Table at line 783.

**Alternative interpretation.** The current ~0.05 number may have been computed against C8 raw corpus on the all-14 grain or under a different judge aggregate. Without provenance for the ~0.05, the reconciliation should either trace where it came from or replace it. The current text makes a quantitative claim that is not pinned to a specific grain.

**Risk.** Pinning the C8-to-C9 number means removing wiggle room. If a reviewer asks "which slice is canonical?" the answer is now in writing. Recommend reporting both grains side by side with explicit slice labels rather than picking one.

**Recommendation.** APPLY-AS-DRAFTED. The `cross_checks` block is the source of truth for the per-question grain; the subject-mean +0.14 sits in the existing Table 4.2 row.

---

### Refinement 3. §4.4.2 -- strengthen Pattern 1, 2, 3 with Spearman ρ split

**Current paper state.** §4.4.2 line 1117 to 1119, the subsection lede:

> 4.4.2 Where the spec helps, where it hurts, and which question types route to each
>
> This subsection is the mechanism deep-dive for §4.4. It does three things. First, it quantifies the bimodal per-question distribution on Supermemory (the system where the aggregate Δ is closest to zero and the per-question signal is therefore cleanest to read). Second, it walks through four paired Supermemory examples that anchor Pattern 1, Pattern 2, and Pattern 3. Third, it shows the same three patterns reproducing across every memory system in the study, with the relative frequency of each pattern shifting by retrieval architecture in a way that tracks how much of the plain answer the retrieval already supplies.

The Pattern 1 / 2 / 3 description rests on per-question paired-Δ counts and on four worked examples; no rank-correlation statistic supports it.

**Proposed change.** Insert a paragraph immediately after line 1119, before "Why Supermemory carries the mechanism walkthrough":

> A rank-correlation lens on the same paired data. Stream Y (`docs/research/within_band_shifts_20260428.md`) computes Spearman ρ between pre and post conditions across the questions in each pair. Spec-on-baseline pairs (C5 to C2a, C5 to C4, C5 to C4a, C5 to C8, C5 to C9): mean ρ near 0.27 on the C5-to-C4a flagship pair; spec on baseline re-ranks the question pool, and the question that scored highest in C5 is not necessarily the question that scores highest in C4a. Spec-on-info-rich pairs (C4 to C4a, C8 to C9, C2a to C4a): ρ = 0.61, 0.70, 0.72; spec on top of an information-rich condition preserves the order of question difficulty while shifting magnitudes. The Pattern 1 / 2 / 3 mixture is the per-question level at which order is preserved but magnitude swings: about a fifth of questions move up by one rubric anchor or more, about a fifth move down, and the rank order across questions stays roughly intact. This is a different mechanism signature from spec-on-baseline, where the spec is doing first-pass identity and pattern supply work and the question-level ranking flips because previously-tied refusal responses get differentiated.

**Evidence supporting the change.** Stream Y rank-correlation table (within-band-shifts §Y1 paragraph 4): C5-to-C4a ρ=0.27, C4-to-C4a ρ=0.72, C8-to-C9 ρ=0.70, C2a-to-C4a ρ=0.61. Direction-agreement on small panel-Δ bins (74.2% at 0.1-0.25 on C5-to-C4a) confirms the rank-correlation signal is not noise.

**Alternative interpretation.** The Spearman ρ split may reflect the floor-and-ceiling of the rubric rather than a substantive mechanism difference. If C5 contains many tied band-1 refusals, the rank correlation is mechanically suppressed (ties on one side and not on the other reduce ρ). The C4 and C8 conditions have far fewer band-1 ties because retrieval-given answers are differentiated, so the post pre-condition's distribution is already spread out and the spec's effect can preserve that spread.

**Risk.** Adding rank correlation as evidence for Pattern 1 / 2 / 3 expands the §4.4.2 mechanism story onto a new statistical primitive. The existing per-question bimodal counts already do the work qualitatively; the rank-correlation primitive is a redundant but not contradictory check. Cross-LLM reviewers may flag the addition as gold-plating if they read it as a separate claim rather than a corroborating one.

**Recommendation.** APPLY-AS-DRAFTED, scoped narrowly. Frame the rank-correlation paragraph as a corroborating check on the existing Pattern 1 / 2 / 3 framing, not as a new claim. Keep the four worked examples as the primary evidence; the Spearman ρ paragraph is one paragraph and does not displace them.

---

### Refinement 4. §3.6 -- add half-anchor metric note

**Current paper state.** §3.6.2 (lines 413 to 432) introduces fractional score interpretation and the cross-anchor rule:

> Cross-anchor interpretation rule. A fractional delta that crosses an integer anchor reflects a real shift in the underlying response distribution. A delta that stays inside a single integer band is a within-category shift and a weaker claim.

The section makes the integer-anchor metric the primary unit for §4 reporting. No explicit acknowledgment that within-band shifts carry detectable signal that the binary anchor-crossing metric ignores.

**Proposed change.** Add a paragraph after the "Examples from the data" bullets (after line 430), before §3.6.3:

> A note on within-band shifts. The integer-anchor metric is the conservative reporting unit; it does not capture sub-anchor signal. A post-hoc audit of all 18 paired condition comparisons (Stream Y, `docs/research/within_band_shifts_20260428.md`) finds that for every 1 anchor crossing the binary metric records, an additional 0.18 same-band shifts of half a rubric anchor or larger exist that the binary metric records as zero movement. Direction-agreement among the 5 primary judges on these sub-anchor shifts is 74.2% at panel |Δ| 0.1-0.25 and 93.3% at 0.25-0.5, well above chance. The decision to use the binary integer-anchor metric throughout §4 is conservative: it under-counts spec effects that move responses inside a single rubric band rather than across one. Numbers reported as "the spec moves X% of responses" are accordingly interpreted as a lower bound on movement; the half-anchor and quarter-anchor distributions are reported in the within-band shifts companion document for readers who want a finer-grain view.

**Evidence supporting the change.** Stream Y pooled missed-signal ratio: 759 same-band |Δ| >= 0.5 instances exist alongside 4,206 anchor crossings across 8,804 paired comparisons; ratio 0.18. Direction-agreement at small panel-Δ confirms the sub-anchor signal is detected by the panel rather than being judge noise.

**Alternative interpretation.** The 18% missed-signal rate may reflect rubric-handling artifacts that the existing §3.6.6 validity audit covers (length inflation in C5, abstention partial-credit). If those artifacts are responsible for half-anchor movements that look like real signal but are actually rubric quirks, then the integer-anchor metric is correctly conservative and the within-band note overstates the missed signal.

**Risk.** Acknowledging within-band signal opens the question of why §4 doesn't report on it. The paper's discipline of using the binary metric is defensible (Krippendorff α = 0.659 across the 5-judge primary panel justifies caution about absolute magnitudes). The within-band paragraph should state explicitly that §4 will continue to report integer-anchor crossings as primary, and the within-band view is a sensitivity check.

**Recommendation.** APPLY-AS-DRAFTED. The paragraph is methodological transparency; it does not change any §4 number. The decision to keep integer-anchor crossings as primary is preserved; the within-band view becomes available to readers who want it.

---

### Refinement 5. Appendix B -- Hamerton-leverage at per-question grain

**Current paper state.** §4.1 paragraph 731:

> Hamerton leverage. Hamerton has both the highest Δ_C4a and the largest battery (80 questions), and a natural concern is that it alone drives the slope. Dropping Hamerton and refitting on the 13 globals attenuates the slope by about 7%, with overlapping confidence intervals. The gradient is not Hamerton-driven. Subset-regression detail also appears in Appendix B.6.

The Hamerton-leverage check is at the per-subject mean grain (drop one of 14 subject means, refit). It does not test the wins-population or the per-question grain.

**Proposed change.** Add a new subsection to Appendix B (after B.6, before B.7), titled "B.6.1 Hamerton-leverage at the per-question wins grain." Verbatim addition:

> B.6.1 Hamerton-leverage at the per-question wins grain. The B.6 sensitivity check drops Hamerton's per-subject mean and refits the gradient regression. A complementary check at the per-question wins grain: drop Hamerton's 15 unique extreme upward jumps from the 60-case wins inventory and recompute the headline numbers on the 13 globals only. Hamerton's 15 jumps span 80 battery questions (jump rate 18.75%); the 13 globals' 45 jumps span 13 x 39 = 507 questions (jump rate 8.9%). Removing Hamerton drops the wins-population from 60 to 45, the 13-global jump rate stays at 8.9% (10.4% relative concentration drop), and the axis distribution shifts: LITERAL_RECALL share among the remaining 45 jumps falls from 28.3% (17 of 60) to 24.4% (11 of 45), within the 95% binomial CI of the full-population rate. The mechanism distribution from the deep pattern-activation analysis (`docs/research/pattern_activation_deep_20260428.md`): on the 45 globals' jumps, PATTERN_PREDICATE = 36 (80.0%), INFERENCE_CHAIN = 8 (17.8%), UNCLEAR = 1 (2.2%); on Hamerton's 15 jumps, PATTERN_PREDICATE = 11 (73.3%), INFERENCE_CHAIN = 3 (20.0%), UNCLEAR = 1 (6.7%). The mechanism distribution is invariant to dropping Hamerton; the elevated jump rate is the leverage. Candidate explanations for the rate elevation that have not been disentangled (legacy battery generator, subject pretraining thinness, predicate density per word in the brief-only spec format, battery question-type composition) are flagged as future work in §7.

**Evidence supporting the change.** Hamerton confound note (`docs/research/hamerton_confound_note_20260428.md`) derives the 15 of 60, 18.75%, and 2.1x figures and explicitly recommends a per-question-grain Hamerton-leverage check. Deep pattern-activation analysis (`docs/research/pattern_activation_deep_20260428.md`) provides the per-subject mechanism counts: Hamerton 15 (PATTERN_PREDICATE 11, INFERENCE_CHAIN 3, UNCLEAR 1), globals 45 (PATTERN_PREDICATE 36, INFERENCE_CHAIN 8, UNCLEAR 1).

**Alternative interpretation.** The mechanism-distribution invariance under Hamerton drop may be illusory because the same heuristic is doing the labeling in both groups. The deep analysis shows that PATTERN_PREDICATE rhetoric is dominant across both jumps and controls; the Hamerton-vs-globals invariance is a property of the labeling heuristic, not of the underlying lift mechanism.

**Risk.** Adding a per-question-grain Hamerton-leverage check propagates Hamerton's status as a leverage point. The existing §4.1 per-subject-mean check shows the gradient is not Hamerton-driven; the per-question wins-grain check shows the wins population is heavily Hamerton-loaded (25% of unique extreme jumps). These two facts are not contradictory but they do require different interpretations: the gradient slope is robust to Hamerton, but any wins-as-headline framing would be Hamerton-dependent.

**Recommendation.** APPLY-AS-DRAFTED. The check is cheap, the data is on disk, and the appendix is the right home for it. The existing §4.1 paragraph 731 should add a sentence pointing readers to the new B.6.1 for the per-question wins-grain leverage check. Verbatim addition to §4.1 paragraph 731 (final sentence): "A complementary leverage check at the per-question wins grain (drop Hamerton's 15 extreme jumps, recompute the wins population on 13 globals only) is in Appendix B.6.1; the mechanism distribution is invariant to dropping Hamerton, but the elevated jump rate is itself Hamerton-concentrated and the cause has not been disentangled."

---

### Refinement 6. Discussion / §4.6 -- cautious mechanism description

**Current paper state.** §4.4.2 paragraph 1264:

> This per-system characterization is qualitative. A quantitative frequency breakdown of Pattern 1 / 2 / 3 across all 507 questions x 5 systems would require mechanism classification per response, which is flagged as a follow-up in §7. The observation that the paired analyses reproduce the three mechanisms on every system is empirical; the specific relative frequency per system is not yet quantified.

§5.4 paragraph 1454:

> The specification interacts with retrieval at the question level, not uniformly. The mechanism is structured: the spec helps a particular class of question (interpretation-heavy, where retrieved facts underdetermine the answer) and hurts a different class (literal-recall, where retrieval already supplied the plain answer; or refusal-triggering, where retrieved facts cannot ground a prediction at all). §4.3 and §4.4 identified three patterns that together generate the correct-spec effect; aggregate Δ_spec is the per-question balance of these three patterns.

§5.4 paragraph 1468:

> What the mechanism reading leaves open. We did not run component ablation (anchors-only, core-only, predictions-only, brief-only, and combinations). Which layer of the specification carries Pattern 1 (pattern supply) improvements, which contributes to Pattern 2 (over-theorization) regressions, and which triggers Pattern 3 (structural refusal) is not measured. §7 flags this as the priority authoring-pipeline follow-up.

**Proposed change.** Add a paragraph at the end of §5.4 (after paragraph 1468), before §5.5:

> What the mechanism heuristic does not establish. A post-hoc deep audit of the wins population (`docs/research/pattern_activation_deep_20260428.md`) classified the mechanism behind all 60 unique extreme upward jumps and a 38-case non-jumping control group of stratified spec-loaded responses. PATTERN_PREDICATE was the dominant code on both populations: 47 of 60 jumps (78.3%) and 36 of 38 controls (94.7%), with the control rate slightly higher. After excluding 9 degenerate C5-to-C4 jumps where the post-condition equals the disconfirmation reference, the spec_doing_work share is 78.9% in jumps (n=38) vs 80.6% in controls (n=36); delta -1.6 percentage points. The pattern-predicate-rhetoric heuristic detects the response style that spec-loaded conditions produce; it does not discriminate jumps from non-jumping spec-loaded responses. We therefore frame the §4.4.2 Pattern 1 / 2 / 3 typology as a description of the per-question signal in the data, not as an attribution of the lift to predicate activation per se. The narrower mechanism claim that does survive the discriminator test: 11 of 60 extreme upward jumps (18.3%) coded INFERENCE_CHAIN with disconfirmation verdict genuine_inference_via_spec, vs 2 of 38 controls (5.3%) with the same code. About 1 in 6 extreme upward jumps shows specification-enabled inference of an answer the retrieval cannot ground; that subset is real and is the strongest mechanism signal in the wins data. Causal attribution of the broader Pattern 1 lift to specific predicates would require predicate ablation, which is flagged as the priority authoring-pipeline follow-up in §7.

**Evidence supporting the change.** Deep pattern-activation analysis full numbers: PATTERN_PREDICATE 47 of 60 jumps and 36 of 38 controls; spec_doing_work 78.9% jumps vs 80.6% controls (fair comparison after C5-to-C4 exclusion); INFERENCE_CHAIN with genuine_inference_via_spec verdict 11 of 60 jumps vs 2 of 38 controls.

**Alternative interpretation.** The discriminator test may be itself undermined by the disconfirmation reference choice. The "fair comparison" excludes 9 cases where post equals C4 (the disconfirmation reference), so the discriminator is computed on 38 jumps (post = C4a) vs 36 controls (post = C4a). Both groups are facts+spec post-condition responses; the only difference is whether the question landed an extreme jump or not. Under that lens, the heuristic's failure to discriminate is expected: it is measuring response style, and both groups are in the same response style. This may be the cleanest reading: the rhetoric heuristic is a measurement of style, not of mechanism, and the fact that it does not separate jumps from non-jumps is because both populations are stylistically comparable. The lift mechanism then has to be sought elsewhere (anchor frequency vs facts coverage at the per-question level, predicate-ablation experiments, or human-coded mechanism judgments).

**Risk.** Stating that the mechanism heuristic does not discriminate is a public retreat from a claim that lived in v10 and earlier drafts. Cross-LLM reviewers will read it as a self-correction. The honest framing makes the eventual predicate-ablation experiment results carry more weight, but it does cost the paper a clean mechanism story in the meantime. The risk of overcorrection: the deep analysis is N=60 + N=38 with a single LLM-coded mechanism heuristic; running a second independent classifier or a human-coded subset before declaring the heuristic non-discriminating would be a stronger move. The author may want to flag the discriminator test itself as a sensitivity check, not as the final word.

**Recommendation.** REFINE-FIRST. The proposed paragraph as drafted is the honest framing given the deep analysis. But before applying, the author should consider adding a stratified human-coded subsample (or a second independent classifier) to corroborate that the heuristic is non-discriminating, and only commit to the §5.4 paragraph if that corroboration holds. If the corroboration is not feasible before the v11 freeze, applying the paragraph as drafted with a footnote acknowledging "single-classifier limitation" is acceptable.

---

## Higher-stakes pivots

### Pivot 7. Strong mechanism description: "the mechanism is predicate activation, not retrieval"

**Current paper state.** No version of this strong claim appears verbatim in v11. §5.4 paragraph 1452 takes the careful position that "content specificity is a necessary condition, not an optional property"; §5.4 paragraph 1454 attributes Pattern 1 to "pattern supply" without claiming predicates are the causal driver. The §1.4 implications block (paragraph 119 onward) frames the spec as a representational tool, not as a predicate-activation tool. The collective review (`docs/reviews/pattern_activation_claim_review_20260428.md`) was reading a candidate sentence the author had on the table for §5.4: "The specification's primary mechanism is behavioral-predicate activation; it enables the model to reconstruct answers to factual questions by applying documented patterns, rather than by retrieving verbatim facts from the context." Neither reviewer endorsed the strong reading without ablation experiments.

**Proposed pivot.** Replace the existing soft framing in §5.4 with: "The specification's primary mechanism is behavioral-predicate activation; it enables the model to reconstruct answers to factual questions by applying documented patterns, rather than by retrieving verbatim facts from the context." This pivot makes predicate activation the named mechanism throughout §5.4 and §5.5 and would require recasting the §4.4.2 Pattern 1 / 2 / 3 typology around predicates (Pattern 1 = predicate activation; Pattern 2 = predicate over-application; Pattern 3 = predicate-induced refusal).

**Evidence supporting the pivot.** Pre-discriminator: 12 of 20 stratified-sample cases coded PATTERN_PREDICATE; 0 of 20 coded DIRECT_QUOTE_MATCH; 1 of 20 coded ANCHOR_FACT. Stream X axis-distribution: LITERAL_RECALL overrepresented at 2.77x panel rate among extreme jumps, and on those LITERAL_RECALL jumps the spec rarely contains the answer text (held-overlap typically 0-2 tokens), so the model is reconstructing rather than retrieving. The 60.6% wrong-spec content-mismatch detection rate on C2c (§4.3 paragraph 935) shows the model engages with spec content as a comparable signal to question content.

**Alternative hypothesis still unrefuted.** The deep pattern-activation analysis shows the predicate-rhetoric heuristic does not discriminate jumps from non-jumping spec-loaded responses. That alone does not rule out predicate activation as the causal mechanism, but it removes the only quantitative evidence for it that the study currently has. The two unrefuted alternatives (both flagged in the collective review): (a) rater-induced confabulation, where the rhetoric heuristic systematically labels coherent spec-loaded responses as "predicate-driven" because the spec is full of predicates; (b) generic persona enrichment, where the spec provides any rich subject-specific context (predicates, biographical facts in disguise, narrative framing) and the model uses it diffusely without the predicates being individually causal.

**Risk profile.** Cherry-picking risk: high if the strong claim survives only because of the 78.3% PATTERN_PREDICATE rate on the 60-jump population, which is matched by 94.7% on controls. Small-N risk: the 60-case population is small in absolute terms even at full census; a strong mechanism claim should ride on a much larger population or on causal experiments. Rater confabulation risk: very high, given the deep analysis result and the collective review's central concern. Hamerton concentration risk: 15 of 60 cases (25%) are Hamerton-driven; the strong claim would inherit that concentration.

**Phase 2c dependency.** Predicate ablation must show that removing the heuristic-identified causal predicate disproportionately drops the lift on the implicated questions. Specifically: (a) for the 12 PATTERN_PREDICATE cases in the original N=20 sample, regenerate responses with the implicated predicate removed (other content preserved) and show that the lift collapses by at least one rubric anchor on average; (b) for the same 12 cases, regenerate with the implicated predicate replaced by a plausible-but-irrelevant predicate and show that lift collapses similarly; (c) inter-rater reliability check on the heuristic, ideally with at least two independent classifiers (LLM or human) on the full 60-case population, with Cohen's κ above 0.5 on the PATTERN_PREDICATE vs INFERENCE_CHAIN distinction. If (a), (b), and (c) succeed, the strong claim is defensible. If any one fails, the claim retreats to the cautious INFERENCE_CHAIN-only framing in Refinement 6.

**Recommendation.** PHASE-2C-DEPENDENT. The current evidence is negative on the discriminator we have. The phase-2c bar is restoring positive discrimination through ablation; the bar is no longer "wait for confirmation" but "wait for a positive signal where the current signal is null."

---

### Pivot 8. Two-mechanism story explicit: spec-on-baseline re-ranks; spec-on-info-rich uniformly lifts

**Current paper state.** §4.1 (the cross-subject gradient) treats the C5-to-C4a paired comparison as the headline statistic; §4.2 (compression) treats spec-on-baseline (C5-to-C2a) as the compression headline; §4.4 (memory-system composition) treats spec-on-retrieval (C1-to-C3) as a separate per-system effect. The paper currently does not articulate a generalized two-mechanism story across the full condition matrix. The closest existing framing is §4.4.2's Pattern 1 / 2 / 3, which describes per-question heterogeneity within a single (Supermemory) post-condition. The Stream Y rank-correlation result (spec-on-baseline ρ ≈ 0.27 vs spec-on-info-rich ρ ≈ 0.61-0.72) is a new statistical primitive that has not been propagated into the paper.

**Proposed pivot.** Add a new subsection at the end of §4 (after §4.7), or fold a substantive paragraph into §4.4 introduction, that frames the spec's effect as different in kind on baseline-empty conditions than on information-rich conditions. Verbatim candidate text for the new subsection lede:

> A two-mechanism reading of the spec's behavior across conditions. The spec's per-question signal differs in kind depending on whether the pre-condition has any subject-specific information at all. On spec-on-baseline pairs (C5 to C2a, C5 to C4, C5 to C4a, C5 to C8, C5 to C9), the question-level rank correlation between pre and post is low (Spearman ρ ≈ 0.27 on the C5-to-C4a flagship), and 60.5% of questions cross at least one rubric integer anchor. The spec is doing first-pass identity and pattern-supply work, and the question-level ranking flips because previously-tied band-1 refusals get differentiated. On spec-on-info-rich pairs (C4 to C4a, C8 to C9, C2a to C4a), the rank correlation is high (Spearman ρ = 0.61, 0.70, 0.72), and only 40.7% of questions cross an anchor. The spec is acting as a per-question modulator: it preserves the relative ordering of question difficulty while shifting magnitudes (Pattern 1 / 2 / 3 in §4.4.2), with about a fifth of questions improving and a fifth worsening at the per-question grain. The aggregate small Δ on info-rich pairs masks substantial bidirectional per-question movement (§4.2.1, §4.4.2). The two mechanisms are not exclusive: the same Pattern 1 mechanism (specification supplies the interpretive pattern when retrieval underdetermines the answer) drives both the spec-on-baseline lift and the spec-on-info-rich modulation; what changes is the proportion of questions on which Pattern 1 versus Pattern 2 versus Pattern 3 fires, which itself tracks how much of the plain answer the pre-condition already supplies.

**Evidence supporting the pivot.** Stream Y rank-correlation primitive (`within_band_shifts_20260428.md`, paragraph 4 of executive summary): C5-to-C4a ρ=0.27, C4-to-C4a ρ=0.72, C8-to-C9 ρ=0.70, C2a-to-C4a ρ=0.61. Wins inventory anchor-crossing rates: spec-on-baseline mean 60.5%, spec-on-info-rich mean 40.7%. §4.4.2 Pattern 1 / 2 / 3 typology already documented per-question heterogeneity on Supermemory; this pivot generalizes the mechanism description to the full condition matrix.

**Alternative hypothesis still unrefuted.** The Spearman ρ split may be a floor-effect artifact, not a genuine two-mechanism signal. Spec-on-baseline starts with many tied band-1 refusal responses; once the specification differentiates them, the rank correlation between baseline and post is mechanically suppressed because the baseline distribution is heavily tied. Spec-on-info-rich starts with already-differentiated questions (retrieved facts vary in coverage), so the rank correlation between pre and post is mechanically higher because both distributions are spread out. Under this alternative, the "two mechanisms" are one mechanism (spec produces a lift) operating on two different baseline distributions, and the Spearman ρ is a property of the input distribution rather than of the spec's behavior. To refute this alternative, one would compute Spearman ρ between condition pairs that have similarly-spread input distributions but different post conditions, which the existing data does not directly support.

**Risk profile.** Cherry-picking risk: low; the rank-correlation primitive is computed across all questions in each pair and is not a small-N sample. Small-N risk: low at the question grain (n=312 to 546 per pair). Rater confabulation risk: not applicable; this is a direct statistical signal across panel scores, not a mechanism heuristic. Hamerton concentration risk: medium; Hamerton's high battery-level Spearman correlation may pull the spec-on-info-rich aggregate up. Multi-anchor crossing artifact risk: the rubric is bounded 1-5; high-baseline subjects whose pre-condition responses cluster near 4-5 may have rank correlations dominated by ceiling effects. A robustness check could compute Spearman ρ on the low-baseline-9 slice only, where ceiling effects are minimized.

**Phase 2c dependency.** None. The two-mechanism reframing is at the metric level (rank correlation, anchor-crossing rate) and does not depend on predicate-ablation experiments. It is fully derivable from existing data.

**Recommendation.** Strongest pivot in the set. Substantive enough to merit a new claim, with the caveat that it should ride on the rank-correlation primitive (statistical, panel-judge agnostic) rather than on the predicate-mediated mechanism story. Frame as "two-mechanism at the metric level," not "two-mechanism at the predicate level." Recommendation status: APPLY-AS-DRAFTED for the proposed verbatim text, with a robustness footnote on the low-baseline-9 slice rank correlations to address the ceiling-effect alternative. If the cross-LLM reviewers in Round 2 raise the floor-effect alternative as a substantive concern, demote to a §4 subsection (rather than a major restructure) and frame as a "candidate reading" pending further work.

---

## Cross-cutting risks the report flags

**Cherry-picking risk on the 60-case wins population.** Hamerton accounts for 15 of 60 unique extreme upward jumps (25% of the wins population) on a battery of 80 questions; the 13 globals account for the remaining 45 jumps on 13 x 39 = 507 questions. Hamerton's per-question extreme-jump rate is 2.1x the globals' average. Any wins-as-headline framing inherits this concentration. The Refinement 5 leverage check at the per-question grain is the appropriate mitigation; the elevated Hamerton rate is real, not a spec-length effect, and its cause is not yet disentangled.

**Small-N risk.** 60 unique extreme jumps is a small finite population. Statistical claims about mechanism distribution should hedge: the deep analysis result that PATTERN_PREDICATE is 78.3% of jumps and 94.7% of controls has wide implicit confidence intervals at this N. Any pivot that rides on absolute rates from the 60-case population should report rates with their binomial CIs.

**Rater confabulation risk.** The collective review's central concern about mechanism attribution applies to any claim that the spec works through predicate activation. The deep pattern-activation analysis result that the heuristic does not discriminate jumps from non-jumping spec-loaded controls is consistent with the rater confabulation hypothesis: the heuristic detects spec-loaded response style, not the causal pathway from spec to lift. Predicate ablation experiments are the only direct test. Pre-ablation, the cautious framing in Refinement 6 is the honest position.

**Stream X arithmetic and attribution errors risk.** Stream X's claim that Hamerton's elevated extreme-jump rate came from a longer served spec is empirically wrong (Hamerton served spec is 0.33x globals'). One verified error suggests the possibility of others. Where Stream X numbers feed downstream claims, those claims should be re-checked against `wins_inventory_20260428.json` (which has explicit `cross_checks` locking the headline counts). The mechanism counts from Stream X's N=20 audit are superseded by the deep analysis's N=60 + control-group census; do not propagate the N=20 numbers as if they are the canonical figures.

**Spec-loaded response style is itself a confound for any rhetoric-based mechanism heuristic.** The deep analysis result (jumps 78.3% PATTERN_PREDICATE, controls 94.7%) is the cleanest evidence: the heuristic detects the response style spec-loaded conditions produce, not what drives a band-jump. This risk is not specific to the deep analysis; any future rhetoric-based mechanism characterization (per-system Pattern 1 / 2 / 3 frequencies, mechanism-by-axis breakdowns) will face the same confound. Predicate ablation, blinded attribution, or per-component spec ablation are the structural fixes; rhetorical post-hoc classification is not.

**Multi-anchor crossings might still be artifacts of bounded-rubric ceilings rather than real shifts.** The 1-5 rubric is bounded; a multi-anchor jump from band 1 to band 4 is mechanically larger than the same magnitude shift in unbounded space. The existing §3.6.6 validity audit documents one rubric-handling artifact (length inflation in C5 lifting baseline scores; abstention partial-credit similarly inflating baseline). Both effects shrink the measured spec-effect gap; the corrected effect is larger, not smaller. But ceiling effects on the high-baseline reference (Franklin C5 = 3.77, no upward room above 5.0) and on the high-band questions across all subjects could be suppressing the upper tail of multi-anchor jumps. None of the proposed pivots ride on the upper-tail multi-anchor distribution, so this risk is contained for Round 1 but should be flagged if any future framing leans on the magnitude-of-largest-jump statistic.

---

## Sections of the paper that DO NOT need framing change

The wins inventory and Phase 2 streams characterize spec behavior at the per-question grain on existing condition pairs. They do not implicate the following sections:

- **§4.3 wrong-spec adversarial control.** The adversarial v1 derangement aggregate Δ_C2c_v1 = -0.25 (13 globals); the random v2 derangement aggregate Δ_C2c_v2 = +0.15. Neither is touched by the wins-inventory analysis, which is about correct-spec extreme upward jumps. The §4.3 mechanism description (identity disambiguation, directional correction, interpretive inference; three mechanism types with characteristic wrong-spec failure modes) is independent of the predicate-mediated framing in §5.4 and is not destabilized by the deep analysis result.
- **§3.6.3 Calibration.** The diagnostic-test calibration of the 5-judge primary panel is independent of any wins-population analysis. The 5-judge primary aggregate is the conservative choice (excludes the two Gemini judges; effect sizes get larger if the Gemini judges are added).
- **§3.6.1 Judge panel composition.** Seven judges across three providers; primary aggregate is 5-judge non-Gemini. Wins inventory and Phase 2 streams use the same 5-judge primary aggregate.
- **§4.6.1 Cross-provider response generation (Tier 2 replication).** Three subjects across four response models; not affected by mechanism-attribution framing.
- **§4.6.4 Franklin as the high-baseline reference.** Franklin baseline 3.77, Δ_C4a -0.13. The high-baseline reference does not appear in the wins population (no extreme upward jumps because there is no band-1 floor to climb out of). §4.6.4 is unaffected.
- **§3.6.6 Rubric-handling validity audit.** Abstention partial-credit and length-inflation in C5 are independent of mechanism attribution; the audit's conclusion that both effects shrink the measured spec-effect gap remains valid.
- **§4.5 Letta exploratory case study (and Appendix F full version).** N=3 post-hoc case study; not implicated.
- **§4.4.1 Aggregate performance across systems.** The per-system aggregate Δ_spec table is unaffected; the Pattern 1 / 2 / 3 typology in §4.4.2 is the place where mechanism framing tightens.

---

## Open questions for the author

**1. Numerical reconciliation for C9 vs C8.** The wins inventory `cross_checks` block locks the per-question grain at +0.088 on the low-baseline-8 slice; the existing §4.2 table reports the subject-mean grain at +0.14 on the same 8 subjects. Which slice is the canonical headline? Recommend reporting both grains side by side with explicit slice labels (Refinement 2). Open question: does the author want one canonical number in the prose with the other in a footnote, or both prominently?

**2. Hamerton-confound elevation: body-text or appendix-only?** The Hamerton confound note recommends documenting the spec-length inversion explicitly. The Refinement 5 proposal places the per-question wins-grain leverage check in Appendix B.6.1 with a one-sentence pointer in §4.1 paragraph 731. Open question: should the Hamerton confound get a body-text paragraph in §4.1 or §6 (limitations), or is the appendix sufficient?

**3. Two-mechanism story (Pivot 8): substantive enough to be its own §4 subsection?** The rank-correlation split (ρ=0.27 spec-on-baseline vs ρ=0.61-0.72 spec-on-info-rich) is a clean statistical primitive that generalizes the §4.4.2 Pattern 1 / 2 / 3 framing across the full condition matrix. Open question: should this become a new §4.7 (or §4.5, depending on numbering), or fold into §4.4 introduction as a paragraph?

**4. Mechanism heuristic non-discrimination disclosure: §5.4 paragraph or §6.2 limitations?** Refinement 6 proposes the cautious-framing addition at the end of §5.4. Open question: does the author want the disclosure in §5.4 (where the mechanism story is the substance) or in §6.2 measurement-apparatus limitations (where it is framed as a measurement instrument issue)?

**5. Round 2 review timing.** The cross-LLM review (GPT-5.5 + Gemini Pro) on this report should run before any of Refinements 1-5 are applied to the v11 draft, to catch overcorrection or framing drift. Open question: does the author want the cross-LLM review to run on this report directly, or on a v11 draft with Refinements 1-5 already proposed inline as candidate edits?

---

## Round 2 reviewer brief

The cross-LLM reviewers (GPT-5.5 + Gemini Pro) should answer the following questions on Round 2 review of this report:

**1. Are Refinements 1-5 justified by the evidence?** Convergence required: both reviewers should independently agree that each refinement's evidence (cited verbatim from `wins_inventory_20260428.json`, `within_band_shifts_20260428.md`, `pattern_activation_deep_20260428.md`, `hamerton_confound_note_20260428.md`) supports the proposed change. Where reviewers disagree, the report should HOLD that refinement pending a third review or author judgment.

**2. Is Refinement 6's cautious framing the right framing given the deep pattern-activation discriminator result?** Specifically: does the §5.4 paragraph addition correctly attribute the heuristic's non-discrimination to "rhetoric, not mechanism," or does it overstate the discriminator's strength? Is the narrower INFERENCE_CHAIN-only claim (11 of 60 jumps coded genuine_inference_via_spec, vs 2 of 38 controls) defensible at this N, or should it also retreat?

**3. Is Pivot 7 (strong mechanism description) defensible only if Phase 2c succeeds?** Is the Phase 2c bar correctly framed as "restoring positive discrimination" rather than "confirming an absent signal"? Are the three Phase 2c criteria (predicate ablation, predicate reversal, inter-rater reliability) the right minimum bar, or should the bar be raised or lowered?

**4. Is Pivot 8 (two-mechanism story) substantive enough to merit a new claim, and is the rank-correlation primitive (Spearman ρ=0.27 vs ρ=0.61-0.72) the right load-bearing evidence?** Is the floor-effect alternative hypothesis correctly characterized? What additional robustness check would convert it from "candidate reading" to "established result" (low-baseline-9 slice rank correlation, ceiling-effect controls, or something else)?

**5. What is the strongest objection to the report's overall stance?** The report's stance is: paper structure preserved, six iterative refinements proposed (one REFINE-FIRST, five APPLY-AS-DRAFTED), one strong mechanism pivot deferred to Phase 2c, one two-mechanism pivot recommended at the metric level. What objection should the author take most seriously, and from which evidence?

**6. Anything missing or overclaimed?** Specifically: any wins-inventory or Stream Y or deep-analysis numbers that could be cited but were not; any framing the report could have proposed but did not; any pivot the report applied that should be downgraded; any pivot the report deferred that should be applied.

---
