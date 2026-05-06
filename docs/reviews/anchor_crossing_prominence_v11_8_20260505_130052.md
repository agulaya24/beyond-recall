# Anchor-crossing prominence audit — v11.8
_Generated: 2026-05-05 13:00:52_

## Headline read

The author's hypothesis is **partly correct, but uneven across sections**. §1.3 already leads with anchor-crossings (the "2.46" number appears only in a footnote, not body prose); the over-indexing is real and concentrated in **§4.1 and §5.2**, with smaller imbalances in §4.2 and §5.1. The headline section (§1.3) is closer to the desired balance than the author may remember; the load is being carried in the wrong direction primarily inside the gradient sections themselves, where "leveler at 2.46" repetitions out-mass the per-question category-shift framing.

A separable subtlety worth surfacing: "ceiling" (the number 2.46) and "leveler" (the conceptual claim that the spec brings everyone toward similar quality) are linked in the current draft but not the same thing. The leveler claim survives a rebalance; the ceiling number can be moved into footnotes or supporting clauses. Reframing "spec brings every subject toward ~2.46" as "spec brings every subject across the same anchor boundaries, regardless of where their baseline started" preserves the structural point while replacing the number-anchor with a category-anchor.

---

## Per-section balance

### §1.3 What we found — KEEP

**Current balance.** The lead sentence (line 106) is already anchor-crossing framing: *"The Behavioral Specification ... changes the rubric category of answer the language model produces."* The first headline bullet ("Gradient") leads with mean lift +0.89 and 9-of-9 improvement, not with the ceiling. The second headline bullet ("Step-changes, not nudges") is fully anchor-crossing: 55% / 18% (1 in 5 ≥ 2 bands) / 6% (1 in 17 ≥ 3 bands) on the spec conditions. The "2.46" number does not appear in §1.3 body prose at all; it appears only in footnote `[^statsig]` (line 120) as supporting statistical detail.

**Recommendation.** KEEP. §1.3 is already anchor-first.

**One small note.** §1.3's "Gradient" bullet (line 112) leads with mean lift, then percentage of questions improving. If the author wants to push anchor-crossing prominence further, the same bullet could be reordered to lead with "every one of the 9 low-baseline subjects crosses upward" or with the 78.6% improvement rate, but this is not necessary to the rebalance.

---

### §4.1 The cross-subject gradient — TILT-TOWARD-ANCHOR

**Current balance.** "2.46" appears in body prose four times across §4.1 (lines 699, 703, 775, plus the footnote `[^statsig]`). The "leveler" framing is repeated three times in succession:

- Line 699 ("What the gradient is actually showing"): *"the specification produces an answer of roughly uniform quality (mean facts + spec score = 2.46 across all 14 subjects), clustering tightly in the 2.0-2.7 band..."*
- Line 703 ("The specification as a leveler"): *"every subject ... ends up at roughly the same place on the rubric (2.46 across all 14 subjects). This is the equity property of the technology... A subject the model knew nothing about and a subject the model knew well both end up near 2.46..."*
- Line 775 ("Reading the gradient"): *"the spec produces a roughly constant facts + spec quality near 2.46 regardless of baseline."*

The anchor-crossing paragraph (line 695, "**Adding a Behavioral Specification changes the category of answer...**") carries the 55% / 18% / 6% rates and the transition table at lines 705-715 (which is excellent — band-1 → band-3, band-1 → band-4 etc., one of the most layman-legible parts of the paper). But the table is sandwiched between two leveler paragraphs (lines 699, 703) and the anchor framing is then dropped for the rest of §4.1, which returns to the regression slope, the −0.96, the worked examples, the per-subject results table, and the band summary — all of which use ceiling/level framing.

The structural problem: anchor-crossing is introduced once (line 695, one paragraph + a table), then the section returns to gradient/ceiling and stays there. By the time the reader hits "Reading the gradient" at line 775, "2.46" is the conceptual anchor, not the categorical anchors.

**Recommendation.** TILT-TOWARD-ANCHOR. Either reorder so the anchor-crossing paragraph + table come **after** the leveler claim and explicitly extend it ("the leveler effect is visible at the per-question grain as well: subjects don't just average toward 2.46, they cross integer rubric anchors..."), or pare the leveler repetition from three appearances to one and let the anchor-crossing paragraph carry more of the section's narrative weight. The transition table at lines 705-715 is one of the strongest layman-legible exhibits in the paper; it deserves more prominence in the surrounding prose.

**Smaller fix.** Footnote `[^statsig]` in §1.3 (line 120) introduces the "leveler-framing" with the ~2.46 number as paper-wide framing. If the author tilts §4.1 toward anchor-crossings, this footnote should be updated to reflect the rebalance — currently it predisposes the reader toward the ceiling reading before §4.1 even starts.

---

### §4.2 Compression: structure vs. raw text — TILT-TOWARD-ANCHOR

**Current balance.** Mean Δ is the section's lead frame. The opening tables (lines 887-893, 910-921) are mean-score tables; the headline-level claim ("the spec recovers most of what the corpus delivers") is a mean-Δ comparison. Anchor-crossings show up in two places:

1. The "Multi-anchor (≥2 bands) / Extreme (≥3 bands)" table at lines 938-948 (line 938 onward, "What the aggregate numbers hide"). This table is excellent. It carries the most defensible version of the §1 thesis at the per-question grain: 13.0% / 12.5% / 9.0% / 14.5% multi-anchor rates, and the punchline at line 949 ("Adding context to a no-context baseline shifts categorical bands on roughly 1 in 7 questions; layering the specification on top of all facts or raw corpus shifts categorical bands on roughly 1 in 45").
2. The §4.2.1 per-question improvement rate (lines 953-974) — improvement-rate framing rather than anchor-crossing framing per se, but compatible.

The structural issue: the multi-anchor table is filed under "**What the aggregate numbers hide**" (line 934). That heading is defensible but subordinates anchor-crossings to mean-Δ as the canonical metric. The line 949 sentence ("the specification produces the most categorical moves where prior context is sparsest") is one of the cleanest thesis-aligned sentences in the entire paper, and it reads as a table-caption afterthought rather than a load-bearing claim.

**Recommendation.** TILT-TOWARD-ANCHOR. Promote the multi-anchor analysis from "what the aggregate numbers hide" into a peer-level subsection alongside the mean-Δ analysis. Concretely: split §4.2 into "compression at the mean-Δ grain" and "compression at the per-question categorical-shift grain," rather than the current structure where the latter is a hidden-detail subsection. The line 949 sentence belongs in the section's bridge prose, not as a table caption.

---

### §5.1 Synthesis — KEEP, light TILT

**Current balance.** The single-paragraph synthesis at line 1517 leads with mean lift first, anchor-crossings second:

> *"...mean lift +0.89 on the 9 low-baseline subjects; 9 of 9 subjects improved; 78.6% of individual questions improve under the matched layer). 55% of low-baseline questions cross at least one rubric anchor upward, and roughly 1 in 5 cross two or more anchors, meaning the model goes from refusal to a grounded subject-specific prediction in qualitative steps rather than incremental score nudges."*

The order signals priority. Mean Δ → improvement rate → anchor-crossings, with the anchor-crossing claim explicitly framed as "rather than incremental score nudges" — anchor-crossing is doing the qualitative-jump work, mean Δ is doing the headline-statistic work. This is defensible for a synthesis paragraph (the most-cited statistic of the paper is mean Δ +0.89, and the synthesis should foreground it), but the order does signal what the paper wants the reader to walk away with.

**Recommendation.** KEEP, but consider a light reorder. If the author wants to commit fully to anchor-first framing, the second clause could be promoted to first ("55% of low-baseline questions cross at least one rubric anchor upward, ... mean lift +0.89, ..."). This is a one-sentence change, low-cost.

---

### §5.2 Why the gradient is the load-bearing finding — ANCHOR-FIRST-CEILING-SECOND

**Current balance.** This is the strongest case for rebalance in the paper. Two structural observations:

1. The section **title itself** commits to gradient-as-headline. If the paper is rebalancing toward anchor-crossings, "Why the gradient is the load-bearing finding" is the wrong frame for the section that develops the load-bearing claim.
2. The body (lines 1529-1535) mentions **zero anchor-crossings**. The section is built entirely around the "leveler" / "equity property" framing: *"the layer brings every user toward consistent representational accuracy, regardless of how thoroughly the pretrained model already knew them"* (line 1529). The slope footnote `[^treatment-het-fn]` (line 1535) uses the −0.96 / coupling argument. Anchor-crossings — the 55%, the 18%, the qualitative-step finding from §1.3 and §4.1 — do not appear here at all.

The section's argument is strong but its evidence base is one-sided: the gradient is load-bearing because it shows the spec works for the population of relevance, but the *nature* of how the spec works for that population (qualitative category shifts, not score nudges) is exactly what's missing.

**Recommendation.** ANCHOR-FIRST-CEILING-SECOND. This requires a structural rewrite of the section. Two options:

- **Option A (lighter).** Keep the title and the leveler claim, but add anchor-crossing as the primary mechanism: *"The spec is load-bearing for the population of relevance not because it raises an average score by some amount, but because it crosses categorical thresholds: 55% of low-baseline questions move across at least one rubric anchor upward, and 18% cross two or more. The shift is qualitative — refusal becomes grounded prediction — not incremental."*
- **Option B (full rebalance).** Retitle the section ("Why the gradient is load-bearing" → "Why the gradient and the category-shifts together are load-bearing," or similar) and rewrite the body to lead with anchor-crossings as the layman-legible finding, with the −0.96 slope and ceiling as the quantitative backing.

This is the highest-leverage section for the rebalance. Changes here propagate to readers most.

---

### Abstract — TBD

The abstract has not been written yet (write-last rule). Skip and decide framing now.

---

## Suggested rebalance edits

### §4.1 (TILT-TOWARD-ANCHOR)

**Current line 695 paragraph head:**
> *"Adding a Behavioral Specification changes the category of answer the response model produces, not just the number attached to it."*

**Keep this lead. Add a closing sentence that ties anchor-crossings to the leveler claim before the leveler paragraph at line 703:**
> *"The 2.46 cross-subject mean (line 699) is the average of these categorical shifts, not a smooth gradient: subjects don't level toward a number, they cross the same set of integer rubric anchors regardless of where their baseline started."*

**Pare the "leveler" repetition.** Currently three appearances (lines 699, 703, 775) say the same thing. Cut to one. The strongest version is the line 703 paragraph (it has the equity-property framing); cut lines 699 and 775 down to single-sentence references rather than full leveler restatements.

### §4.2 (TILT-TOWARD-ANCHOR)

**Current line 934 heading:**
> *"What the aggregate numbers hide."*

**Replace with a peer-level heading:**
> *"Compression at the per-question categorical-shift grain."*

**Promote line 949 from table-caption position to lead sentence of the subsection:**
> *"At the per-question grain, the categorical-shift pattern is what the §1 thesis predicts: the specification produces the most categorical moves where prior context is sparsest. Adding context to a no-context baseline shifts categorical bands on roughly 1 in 7 questions (mean across paired conditions); layering the specification on top of all facts or raw corpus shifts bands on roughly 1 in 45."*

### §5.2 (ANCHOR-FIRST-CEILING-SECOND)

**Option A (lighter rewrite, keeps title).** Insert as new second paragraph, after line 1529 ("Every living user of AI..."):

> *"What the gradient delivers is not a smooth elevation of a score. The spec moves the model across categorical rubric thresholds: 55% of low-baseline questions cross at least one integer anchor upward when the spec is added, and roughly 1 in 5 cross two or more anchors. These are qualitative shifts in the kind of answer the model produces — refusal becomes grounded prediction; generic engagement becomes subject-specific reasoning — not score nudges. The leveler effect named above operates at the per-question grain: subjects whose baseline sat at the rubric floor cross the same set of anchors as subjects whose baseline sat near the middle, ending in roughly the same category of response."*

**Option B (full rewrite).** Retitle the section. Lead with the categorical-shift finding, fold the equity-property and slope into supporting paragraphs. Highest cost, highest payoff if the author commits to anchor-first as the paper's primary frame.

---

## Abstract framing recommendation

**Anchor-first.** Two reasons:

1. **Layman legibility.** "55% of low-baseline questions cross a rubric anchor upward" is concrete in a way "spec produces a 2.46 ceiling" is not. The latter requires the reader to know what the 1-5 rubric is, what 2.46 means relative to it, and to trust that 2.46 is meaningfully different from a baseline mean of 1.52. The former requires only that the reader understands "moves the answer into a different category." Abstract readers will be field generalists, journalists, and skim-readers; concrete-categorical framing is the lower-friction frame.

2. **Numerical fragility.** "2.46" is a 5-judge primary panel mean on a specific battery of 39 questions. Any future reproduction or extension of the study will produce a slightly different number, which weakens the headline claim if the number is the headline. Anchor-crossings (55%, 18%, 6%) are also empirical and will also vary, but they are presented as proportional thresholds rather than as a single ceiling number, and they survive minor numerical drift better.

**Suggested abstract lead structure:**

> *"A Behavioral Specification ... a structured ~7K-token representation of how a specific person reasons ... changes the kind of answer a language model produces about that person. On 9 historical subjects whose pretraining baseline sits at or below 2.0 on a 1-5 rubric (the population of relevance for AI personalization, where the typical user sits even deeper), 55% of held-out behavioral questions cross at least one integer rubric anchor upward when the specification is added; roughly 1 in 5 cross two or more anchors. The shift is qualitative: refusal becomes grounded prediction. Mean lift +0.89 [statistical detail]. The effect is largest where the model knows the person least; on a high-baseline reference subject the model already knows, the specification has nothing to add."*

The mean Δ stays (it's the canonical statistic for the field), but it's no longer the lead. The lead is what the paper actually shows: a category of answer changes.

**Reasoning to reject ceiling-first.** Ceiling framing leads with "spec produces a uniform quality near 2.46." This is a coupling-derived claim (per the §4.6.4 / §5.2 footnote, the slope of −0.96 is the mathematical consequence of the post-spec mean being roughly constant, not independent treatment-heterogeneity evidence). Leading with the ceiling implicitly leads with the coupled framing the paper itself flagged as needing softening in v10. Anchor-first is honest to the underlying claim; ceiling-first is a near-restatement of a coupling artifact.

---

## Closing note

The rebalance is achievable without disturbing any of the paper's empirical claims. The numbers don't change; only which numbers and which sentences carry the headline weight. §1.3 already does the right thing; §4.1, §4.2, and especially §5.2 are where the editing work concentrates. The §5.2 retitle is the most consequential single decision the author has to make: keeping it as "Why the gradient is the load-bearing finding" commits the section to ceiling-framing as load-bearing, regardless of body edits. If anchor-first is the call, §5.2's title needs to change with it.
