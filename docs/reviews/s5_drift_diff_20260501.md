# §5 Drift Diff — Independent Outline vs Current §5

**Date:** 2026-05-01
**Method:** Diff between `s5_independent_outline_20260501.md` and current §5 in `beyond_recall_v11_5_draft.md` lines 1497–1710.
**Scope:** §5.1 through §5.6 (current). Does NOT cover §6, which begins at line 1714.

---

## Current §5 structure (as written)

| Subsection | Lines | Title |
|---|---|---|
| §5 lede | 1497–1499 | Discussion intro |
| §5.1 | 1501–1517 | The Anti-Pattern: What Behavioral Specification Is Not |
| §5.2 | 1521–1539 | What the study demonstrates |
| §5.3 | 1543–1553 | The population of relevance |
| §5.4 | 1557–1577 | Content specificity and mechanism |
| §5.5 | 1581–1684 | Practical implications (longest by far, ~100 lines) |
| §5.6 | 1688–1708 | What the study does not settle |

---

## Highest-priority drift items (top of list = most actionable)

### MISSING-1: §4.4.1 retrieval-divergence finding is absent from §5

**Status:** CRITICAL MISSING.
**Where in §1–§4:** §1.3 7th headline ("Provider divergence on retrieval relevance"); §4.4.1 full subsection (lines 1158–1183 of paper); §4.6.5 semantic-similarity sensitivity check (lines 1449–1462); §4.7 fifth-finding bullet (line 1483).
**What current §5 says about it:** Nothing. A single phrase at line 1533 mentions "three of four commercial memory systems show net-positive aggregate Δ" without addressing the convergence-failure finding. The 52.3% / 8.3% Jaccard finding does not appear anywhere in §5.
**Action:** Add a new subsection (proposed §5.3 in the independent outline: "Retrieval is not interpretation: what the cross-system divergence means"). This subsection should state the finding (52.3% of system-pair × question instances share zero top-10 facts, mean Jaccard 8.3%, confirmed under semantic similarity at every threshold tested in §4.6.5), connect it to the §2.1 fifth-target argument, and draw the implication that recall accuracy and interpretive relevance are different properties. This is the single most important addition to §5; it is a HIGH-confidence empirical finding (catalog-grade) elevated to headline status during the §4 walk.

### MISSING-2: Letta semantic-duplication observation absent from §5

**Status:** CRITICAL MISSING.
**Where in §1–§4:** §1.3 exploratory note; §4.5 body lines 1336–1348 including the new semantic-similarity duplication paragraph; Appendix G full case study.
**What current §5 says about it:** Line 1537 mentions §4.5 in one sentence ("an informal post-hoc exploration... consistent with non-retrieval representation-production mechanisms also reaching a similar prediction band"). Line 1553 has a similar one-line gesture. Neither §5 mention engages the architectural-ceiling reading: 25.4% verbatim sentence duplication at Babur, 35.2% near-paraphrase at strict ≥0.95 cosine threshold (56.1% at ≥0.85), block growing to 335K characters against the 333K-character ingestion ceiling, monotonic scaling with corpus size, while Base Layer's unified brief holds at 34K-40K characters across the same range.
**Action:** Add a short subsection (proposed §5.5 in the independent outline: "Architectural ceilings under scale"). Two paragraphs. First: the convergence finding (two architectures, retrieval-based static spec and self-editing memory block, converge on the same interpretive target at matched response model on N=3) as positive evidence for the validity of the interpretive-layer target. Second: the scaling-ceiling finding as a specific cost the unified-brief specification does not share, with explicit "N=3, post-hoc, exploratory" hedging consistent with confidence catalog. The current §5 does not carry either thread.

### STALE-1: §5.4 references to specific §4 sections need re-checking

**Status:** Minor, mechanical.
**Where:** §5.4 line 1563 references "§4.3 and §4.4" for the three patterns. The three patterns now live in §4.4.2 (mechanism subsection) with anchor examples and cross-system reproduction. §4.3 carries the wrong-spec mechanism, not the three-pattern memory-system mechanism.
**Action:** Change "§4.3 and §4.4" on line 1563 to "§4.4.2." Similarly check §5.4 line 1565 reference to "§4.4.2 Example 1" (should be either "§4.4.2 Pattern 1" or specifically the Fukuzawa Q26 anchor example).

### STALE-2: §5.4 line 1575 Keckley reference

**Status:** Light. The Keckley Q21 paragraph in §5.4 (lines 1575) is detailed but redundant with §4.4.3 (the Keckley Q21 case study is now its own subsection with a cross-system table). §5 should compress this into a one-paragraph implication, not re-narrate the case study.
**Action:** Trim §5.4 line 1575 to a single paragraph that references §4.4.3 for the case study and uses the cross-system penalty distribution to argue for differentiated rubrics. The current paragraph reads as a re-telling, not an interpretation.

### OVERWEIGHTED-1: §5.5 Practical Implications is ~100 lines, scope-creeps into §7

**Status:** Major. §5.5 currently runs lines 1581–1684 and contains: context budget, authoring cost, per-query cost, dynamic activation (full architecture), modifiability, temporality, topic decomposition, piecewise component analysis, update cadence, positioning against alternatives, infrastructure properties (4 named), per-user calibration framing (3 paragraphs).
**Catalog grounding:** Most of these are flagged in confidence catalog as future work or deployment proposals, not findings the data settle.
**Action:** Cut §5.5 by roughly 50%. Keep: a tight production-deployment-tractability paragraph anchored to §4.2 compression (the 7K-token spec fits inside every frontier context; Babur's 550K-token corpus does not). Cut to §7 future-work: the full dynamic-activation architecture (it should be referenced not specified), modifiability bullets, temporality bullets, topic decomposition bullets, piecewise component analysis (this is L1 in catalog, future work only), update-cadence bullet. Move the "calibration" framing if it survives Aarik's voice pass, but recognize it is not anchored to a §4 finding; it is a deployment frame that may belong elsewhere.

### OVERWEIGHTED-2: §5.4 "dynamic spec activation is a requirement" is too strong a claim

**Status:** Major. Line 1569 reads: "The three patterns together imply dynamic spec activation is a requirement for production response quality... it is a requirement for ensuring that the specification's effect on any given response is net positive."
**Catalog grounding:** Catalog M1 says "spec is most useful where pretraining footprint is thinnest" with a hedge. The three-patterns finding is HIGH-confidence on existence; the production-architecture implication ("requirement") is not data-settled.
**Action:** Soften "is a requirement" to language like "the data point toward dynamic serving as the next architectural step" or "the three patterns together suggest production response quality could be improved by dynamic activation, which §7.4 develops." Do not assert requirement status; this is a future-work direction.

### UNDERWEIGHTED-1: §5.2 four-result summary skips the 7th headline

**Status:** Major. §5.2 lines 1525–1535 summarize four empirical results. They are H1+H2 (gradient), H3 (content specificity), H4 (memory-system interaction), H5 (compression). The 7th headline (provider divergence) is not in the four-result summary.
**Action:** Either expand to five empirical results adding the divergence finding, or add a separate sentence calling it out. The §4.7 summary (line 1482) already lists five findings. §5.2 should mirror that structure.

### UNDERWEIGHTED-2: §5.2 hedging-reduction (6th headline) absence

**Status:** Light-to-moderate. §1.3 lists hedging reduction (28.8% → 0.0%) as the 6th headline; it is described as "the same mechanism behind the gradient operating at its floor." §5.2's content-specificity bullet (line 1531) does not pick up the hedging thread; §5.4's mechanism subsection touches it implicitly but does not name it.
**Action:** In whichever §5 subsection picks up content effect / mechanism (proposed §5.6 in the independent outline, or current §5.4), add a sentence connecting the wrong-spec content effect to the hedging-elimination finding. The connection is in §4.3 (correct-spec eliminates baseline hedging; wrong-spec preserves it). One sentence is sufficient.

### REORDERABLE-1: §5.1 Anti-Pattern subsection should move

**Status:** Moderate. Current §5.1 (lines 1501–1517) lists what the spec is NOT (memory recall, persona fidelity, preference alignment, survey-response interpolation, psychometric profile). This content is largely a re-statement of §2.1 (Memory and personalization benchmarks). It functions as a recap of prior work, not as discussion of the paper's own findings.
**Catalog grounding:** This material is HIGH-confidence (it is ground positioning) but it is not a discussion of §4. It is positioning §2 already established.
**Action:** Either trim aggressively (one paragraph naming the four anti-patterns by reference to §2.1) or move out of §5 entirely. The independent outline does not carry this subsection. Discussion sections in this paper class typically synthesize findings, not re-state positioning. If retained, it should be a brief framing paragraph at the top of §5, not a five-paragraph subsection.

### REORDERABLE-2: §5.3 (population of relevance) sits between §5.2 and §5.4

**Status:** Moderate. §5.3's content (population of relevance, low-baseline subjects as proxy for living users, structural argument) is the discussion of the gradient's high-stakes implication. The independent outline folds this into the gradient subsection (proposed §5.2: "Why the gradient is the load-bearing finding") because the population-of-relevance claim is the implication of the gradient, not a distinct topic.
**Action:** Consider folding §5.3 into the gradient discussion. If retained as a separate subsection, ensure it sits immediately after the gradient discussion and that the connective tissue is explicit (the gradient implies the low-baseline band is where the spec lives, and the typical AI user sits deep in that band).

### REORDERABLE-3: §5.4 mechanism placement

**Status:** Moderate. Current §5.4 covers "Content specificity and mechanism" together. The independent outline splits these: a content-specificity discussion (proposed §5.6) sits separately from a memory-system-composition discussion (proposed §5.4). The reason to split: content specificity is about the wrong-spec finding (§4.3); memory-system composition is about the three patterns (§4.4.2). They are distinct findings with distinct §4 anchors.
**Action:** Consider splitting current §5.4 into two subsections, one on §4.3 (content effect, sycophancy bracketing, transfer of patterns observed) and one on §4.4.2 + §4.4.3 (three patterns, dynamic-serving implication). Current §5.4 mixes them.

### OUT-OF-SCOPE-1: §5.5 calibration framing without §4 anchor

**Status:** Light-to-moderate. §5.5 closing (lines 1680–1684) introduces "per-user calibration" as a deployment frame. This frame is consistent with §4.1's uniform-quality finding, but it is not a finding §4 establishes. It is a positioning-and-naming choice.
**Catalog grounding:** Not in confidence catalog. This is closer to GTM language than to discussion of findings.
**Action:** Consider whether the calibration framing belongs in §5 at all. If it does, anchor it explicitly to a §4 finding and keep it short (one paragraph). If the goal is positioning-language rather than discussion, it may belong in §1.4 (where the "structural options" argument lives) or in §7 (future work and deployment). The current placement is positioning material in a discussion section without a §4 anchor.

### OUT-OF-SCOPE-2: §5.5 "infrastructure properties" four-bullet block

**Status:** Light. Lines 1665–1670 list four infrastructure properties (user-held, inspectable, provenance-traced, local-executable retrieval). These are properties of the artifact, not findings of the experiment. §2.3 (traceability and reasoning traces) is the canonical home for the inspectability and provenance arguments; §1.4 carries the user-held argument.
**Action:** Either trim to a single sentence pointing back to §1.4 / §2.3 / §3.7, or move out of §5. The discussion section's job is to interpret findings, not to enumerate artifact properties.

---

## Minor items

### MINOR-1: §5.3 line 1551 "What we did not prove" framing

The phrase "What we did not prove" appears mid-subsection and does not match the current §5.6 ("What the study does not settle"). Suggest aligning the language between the two so the reader does not parse them as overlapping.

### MINOR-2: §5.6 line 1696 reference to §3.6.6 length-score correlation

Line 1696 cites "length-score correlation r = 0.604 within C5 baseline only." Current §3.6.6 (line 595) reports r = 0.60 within C5. The published version should match exactly or use the §3.6.6 number consistently.

### MINOR-3: §5.4 line 1567 Keckley Q21 reference resolution

Line 1567 references "§1.3 Keckley Q21." §1.3 in v11.5 does not directly include a Keckley Q21 callout (the Keckley case study lives at §4.4.3). Update reference.

### MINOR-4: §5.4 line 1565 "§4.1 Example A, §4.3 Example 1, §4.4.2 Example 1"

These cross-references are mixed: §4.1 has Examples A/B/C (Ebers Q7, Bernal Diaz Q16, Seacole Q2). §4.3 carries wrong-spec Examples A/B/C on the same questions. §4.4.2 Pattern 1 anchor example is Fukuzawa Q26. The triple-citation across §4.1 / §4.3 / §4.4.2 in §5.4 should resolve to the right examples.

---

## Summary of high-level drift

The current §5 was written before three §4 changes landed: (1) the §4.4.1 retrieval-divergence finding was elevated to a 7th headline finding in §1.3 with full subsection in §4.4.1 and sensitivity check in §4.6.5; (2) the §4.5 / Appendix G Letta case study acquired a semantic-duplication observation that bears on architectural ceilings; (3) Franklin moved from §4.6.5 to §4.1.2 as the high-baseline end of the gradient.

§5 currently has four primary issues. First, the retrieval-divergence finding is absent. Second, the Letta architectural-ceiling reading is absent. Third, §5.5 (Practical Implications) is overweighted relative to what §4 establishes and contains substantial content that belongs in §7. Fourth, §5.1 (Anti-Pattern) is positioning material that re-states §2.1 rather than interpreting §4.

Recommended structural action: rebuild §5 with seven subsections (§5.1 synthesis lede; §5.2 gradient + population of relevance combined; §5.3 retrieval-divergence as new subsection; §5.4 memory-system composition with three patterns; §5.5 architectural ceilings via Letta; §5.6 content effect + hedging; §5.7 compression and deployment tractability; §5.8 closing argument). Cut current §5.1 (Anti-Pattern) to a paragraph at the top of §5.2 or remove. Cut current §5.5 (Practical Implications) by half, moving production-architecture proposals to §7. Move current §5.6 (What the study does not settle) to either bridge into §6 or be folded into §6.1.

The single most important addition is the retrieval-divergence subsection. The single most important cut is §5.5 Practical Implications.
