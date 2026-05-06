# Section 2.4 Reference Verification — "Beyond Recall" v6 draft

**Audited:** 2026-04-17 (S113 pre-launch)
**Section:** §2.4 "Cognitive and representational foundations"
**Source draft:** `docs/beyond_recall_v6_draft.md` lines 380-392
**Cross-ref:** `docs/REFERENCE_TABLE.md` (REF-01, REF-02, REF-08, REF-15, REF-16, REF-17)

Each reference verified independently via web search + direct fetch against arXiv / canonical venue.

---

## Summary table

| # | Reference (v6 citation form) | Actual authors | Venue + year | arXiv / ID | Characterization accurate? | Status |
|---|------------------------------|----------------|--------------|------------|----------------------------|--------|
| 1 | Bartlett (1932) | Frederic C. Bartlett | Cambridge University Press, 1932 | ISBN 978-0521483568 | Yes — schema + reconstruction is the canonical reading | **VERIFIED** |
| 2 | Hinton et al. (2015) | Geoffrey Hinton, Oriol Vinyals, Jeff Dean | NeurIPS 2014 Deep Learning Workshop (2015 arXiv) | arXiv:1503.02531 | Yes — "dark knowledge" is Hinton's own term for inter-class similarity structure preserved through soft targets | **VERIFIED** |
| 3 | Chen, Arditi, Evans et al. (2025) | Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey | arXiv 2025 (Anthropic / safety-research) | arXiv:2507.21509 | Yes — paper extracts activation-space directions ("persona vectors") for monitoring + steering traits such as evil, sycophancy, hallucination | **VERIFIED** (author short-form issue below) |
| 4 | Jiang et al. (COLM 2025) | Bowen Jiang, Zhuoqun Hao, Young-Min Cho, Bryan Li, Yuan Yuan, Sihao Chen, Lyle Ungar, Camillo J. Taylor, Dan Roth | COLM 2025 (PersonaMem benchmark) | arXiv:2504.14225 | Yes — paper reports frontier models (GPT-4.1, o4-mini, GPT-4.5, o1, Gemini-2.0) at ~50% overall accuracy on dynamic user-profile tasks. Our "lack of interpretive structure" framing is our interpretation layered on their empirical finding, which is acceptable as long as it is read as interpretation, not as their own claim. | **VERIFIED — mild overreach in gloss** |
| 5 | Jain et al. (2026) | Shomik Jain, Charlotte Park, Matt Viana, Ashia Wilson, Dana Calacci | arXiv, Sep 2025 (related CHI 2026 extended abstract exists separately) | arXiv:2509.12517 | **NO** — paper is about **sycophancy**, not **hedging**. v6 misattributes a hedging claim to this paper. Only use of "hedge" in the paper is a footnote citing Cheng et al. 2025 for a form of sycophancy the authors explicitly place outside their scope. | **NEEDS CORRECTION** |
| 6 | Lu et al. (2026) | Christina Lu, Jack Gallagher, Jonathan Michala, Kyle Fish, Jack Lindsey | arXiv, Jan 2026 (safety-research) | arXiv:2601.10387 | **NO** — paper identifies the "Assistant Axis" as the dominant direction in persona activation space and shows steering toward it reinforces "helpful and harmless" behavior. The paper does **not** identify **hedging** as a structural property, and does not use the phrase "safe default." One incidental occurrence of "hedging" in §6.2 is descriptive of an unsteered Qwen example, not a structural claim. | **NEEDS CORRECTION** |

---

## Detail — references that need correction

### REF-15 Jain et al. (2026) — misattributed claim

**v6 current text (§2.4):**
> "Jain et al. (2026) find that adding interaction context to LLMs increases rather than reduces hedging when the context lacks interpretive framing. Our hedging-reduction finding (§5.5) is consistent: context without structure amplifies uncertainty; context with interpretive structure anchors commitment."

**What the paper actually finds (arXiv:2509.12517 abstract, verbatim):**
> "Agreement sycophancy tends to increase with the presence of user context […] User memory profiles are associated with the largest increases in agreement sycophancy (e.g. +45% for Gemini 2.5 Pro) […] Perspective sycophancy increases only when models can accurately infer user viewpoints from interaction context."

The paper studies **agreement sycophancy** and **perspective sycophancy**, not hedging. "Hedging" appears once in the paper, in a footnote describing *indirectness sycophancy* (Cheng et al.) which they explicitly exclude from scope.

**Recommended correction (options):**

1. **Reframe our claim around sycophancy, not hedging.** If our §5.5 finding is about reduced hedging, cite Jain in reference to a *distinct* but analogous failure mode: "context without interpretive structure amplifies failure modes — Jain et al. (2026) show it increases sycophancy; we observe it increases hedging." This keeps the citation but is honest about what they measured vs. what we measured.

2. **Drop Jain from the hedging-specific claim and move to a different paragraph.** Keep Jain as support for the general "raw context without structure degrades behavior" point, not the specific hedging mechanism.

Option 1 is the cleaner fix and also applies to the §5.4 re-use of this citation (v6 line 1108), which has the same misattribution.

### REF-16 Lu et al. (2026) — misattributed claim

**v6 current text (§2.4):**
> "Lu et al. (2026) identify hedging as a structural property of assistant models. Without an external behavioral anchor, helpfulness drifts toward hedging as a safe default. The specification provides that anchor."

**What the paper actually finds (arXiv:2601.10387):**
The leading direction in persona activation space is an "Assistant Axis." Steering toward it reinforces **helpful and harmless** behavior; steering away produces mystical / theatrical / non-assistant personas. Pre-trained models also carry this axis, where it promotes consultant/coach archetypes and inhibits spiritual ones.

Nothing in the paper identifies hedging as structural. The paper uses "hedging" once (§6.2) to describe a Qwen example before steering. The "safe default" language is ours, not theirs.

**Recommended correction:**

Reframe to what Lu et al. actually show, then bridge to our claim:

> "Lu et al. (2026) identify an 'Assistant Axis' — a dominant direction in activation space that anchors the helpful-and-harmless default persona. Their finding that this default is a *structural* property of post-training (not a surface stylistic choice) is consistent with our reading that assistant behavior in the absence of a specific user model defaults to a generic, cautious posture. The specification provides an external user model that displaces that generic default."

This keeps Lu as support but attributes only the claim the paper actually makes (structural default persona), and moves our hedging argument to a separate sentence with the framing made explicit as interpretation.

---

## Minor issues (not corrections, but flag)

- **Chen author short form (REF-08):** v6 cites as "Chen, Arditi, Evans et al." — canonical author order is "Chen, Arditi, Sleight, Evans, Lindsey." Dropping Sleight and Lindsey is acceptable short form but inconsistent with alphabetical or contribution-weighted conventions. Either use "Chen et al. (2025)" first-mention-with-full-list or keep the current short form consistently across all three occurrences in the paper body.
- **Jiang interpretive gloss:** v6 says "The cause is not a lack of facts but a lack of the interpretive structure to apply those facts to novel situations." The Jiang paper documents the 50% accuracy number; the "interpretive structure" diagnosis is ours. This is defensible as commentary but should read as our interpretation, not as Jiang's finding. Consider: "We read this as evidence for the representational-accuracy gap: the facts are present in the conversation log, but models lack the interpretive structure to apply them."
- **Jain year (2026 vs 2025):** arXiv posting is Sep 2025. If the associated CHI extended abstract (dl.acm.org/doi/10.1145/3772363.3798575, "When Flattery Backfires") is the intended venue anchor, 2026 is defensible. REFERENCE_TABLE already flags this. Pick one convention paper-wide.

---

## Red flags — none

All six references exist and are retrievable. No fabricated citations in §2.4. The issues are **mischaracterization**, not non-existence, and they are fixable with a short edit before launch.

## Recommended pre-launch edit summary

1. Rewrite the Jain sentence in §2.4 and §5.4 to say "sycophancy" rather than "hedging" (or reframe around a general "context-without-structure" claim).
2. Rewrite the Lu sentence in §2.4 to attribute only the Assistant Axis / helpful-and-harmless default claim; keep our hedging-default bridge but mark it as our inference.
3. Optionally soften the Jiang gloss to mark the "interpretive structure" diagnosis as ours.

Everything else in §2.4 is fine to ship as written.
