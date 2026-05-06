# Section 4 Results Restructuring — Cross-LLM Formatting Review

_Generated 2026-04-23 during S114. Author: Aarik Gulaya. Reviewers: Mistral Large, Gemini 2.5 Pro._

## Purpose

The author has already locked six structural decisions for the v9 §4 Results restructure (listed under "Non-Negotiables" below). This review solicited focused formatting guidance on five open sub-questions from two frontier reviewers. The raw responses are reproduced verbatim below the synthesis. The goal is a single consensus recommendation the author can accept, amend, or reject.

This report does NOT modify the v9 or v8 paper. It records the reviewers' recommendations and the editor's synthesis for the author to act on.

## Author's Non-Negotiable Decisions (reviewer input not solicited)

1. All memory-provider results (Mem0, Supermemory, Zep, Base Layer) stay in one consolidated §4.4. No per-system top-level headings.
2. Letta is the one exception, pulled out because of its additional stateful-agent path and architecturally distinct memory model.
3. Current §4.6 "Interpretation vs. Recall" content folds into §4.4.
4. Keckley Q21 cross-system refusal remains a named subsection inside §4.4.
5. §4.5 Robustness moves to the end of Results (after consolidated §4.4 and the Letta breakout).
6. §4.8 Scaling and Practical Implications moves out of Results entirely, into Discussion as §5.5.

## Prompt Sent (Identical to Both Reviewers)

Full §4 body from v9 (114,041 chars, 950 lines, unabridged) plus the six non-negotiables above, the five formatting questions below, and a required output format specifying a concrete subsection tree.

Raw prompt text and full reviewer responses saved at `docs/reviews/s114_section4_raw_responses_20260423_194318.md`.

The five formatting questions asked:

1. Flat table vs. table plus per-system micro-paragraphs vs. other format inside consolidated §4.4.
2. Placement of Keckley Q21 within §4.4.
3. Placement of Pattern 1 / Pattern 2 / Pattern 3 cross-system mechanism analysis.
4. Best subsection ordering for the consolidated §4.4.
5. Anything to move to appendix given the tight-body preference.

Both reviewers returned full structured responses with no truncation (Mistral finish_reason=stop, Gemini finishReason=STOP).

---

## Synthesis: Consensus Recommendation

The two reviewers converge on every substantive question. The differences are minor wording and scope of appendix candidates. The editor's recommended path below reflects the consensus and flags the one area of disagreement.

### Q1. Table format within §4.4: **AGREED — option (b)**

Both reviewers: one consolidated per-system comparison table plus per-system micro-paragraphs of 1 to 2 sentences. Table gives scannable quantitative overview, micro-paragraphs carry the nuance (Supermemory's bimodal story, Zep's clean positive, Letta split behavior, Base Layer zero-cost substrate caveat).

Editor agrees. Option (a) collapses too much of the per-system texture the data genuinely has, particularly the Supermemory variance story and the Zep controlled vs. native pattern. Option (c) is not necessary since (b) already accommodates what each system needs.

### Q2. Keckley Q21 placement: **AGREED — dedicated subsection at the END of §4.4**

Both reviewers: Keckley Q21 as a named subsection at the end of §4.4, functioning as the case study that demonstrates the cross-system reproducibility of the specification-induced refusal. Gemini explicitly notes this lets Q21 serve as the concrete instantiation of Pattern 3 after the reader has seen both the quantitative results and the mechanism framework.

Editor agrees. Placing Q21 first would force the reader to carry a specific example before the aggregate; placing it last lets the reader see the quantitative pattern, the three-mechanism framework, and then the clean cross-system example that operationalizes Pattern 3.

### Q3. Pattern 1 / 2 / 3 cross-system mechanism placement: **AGREED — option (a), integrated into §4.4**

Both reviewers: pull Pattern 1 / 2 / 3 into §4.4 as a "common mechanisms across systems" subsection. Rejecting (b) because §4.3 is about wrong-spec content specificity (H3), which is a distinct claim from cross-system mechanism reproduction. Rejecting (c) as its-own standalone subsection (which is what v9 currently does with §4.6) because it fractures narrative flow and makes the reader build the bridge back to per-system results themselves.

Editor agrees. The Pattern 1 / 2 / 3 content is explanatory scaffolding for the per-system quantitative results above it. It belongs in the same section as the data it explains.

### Q4. Subsection ordering within §4.4: **AGREED — quantitative, then mechanism, then case study**

Both reviewers converge on the same "what, why, for example" ordering:

1. Aggregate per-system quantitative results (table + micro-paragraphs)
2. Common mechanisms across systems (Pattern 1 / 2 / 3)
3. Keckley Q21 cross-system refusal case study

Mistral's ordering is identical in effect but numbered 4.4.1 through 4.4.4 rather than 4.4.1 through 4.4.3. Mistral splits "Overview and Comparison Table" (4.4.1) from "Per-System Micro-Analyses" (4.4.2) into two subsections; Gemini treats the table plus micro-paragraphs as a single 4.4.1 "Aggregate Performance Across Systems" unit.

Editor's recommendation: **follow Gemini's three-subsection structure.** The table and micro-paragraphs are tightly coupled and do not need a heading boundary between them. One fewer heading produces a cleaner §4.4.

### Q5. Appendix candidates: **PARTIAL DISAGREEMENT**

Mistral recommends **no appendix moves**. Argues the proposed (b)-format + mechanism subsection + Keckley subsection already keeps §4.4 tight.

Gemini recommends three specific appendix moves:

1. The large "Per-subject paired-delta distributions" table from current §4.6 (the 8-row table showing per-subject wins / losses / large improvements / large regressions). Main text summarizes; appendix holds the full table.
2. Two of the four Supermemory examples from current §4.4. Keep one "spec helps" and one "spec hurts"; appendix takes the other two.
3. Detailed multi-paragraph cross-system Pattern 1 / 2 / 3 examples from current §4.6. Main text presents one concise example per pattern; appendix holds additional cross-system evidence.

Editor's default given the disagreement: **split the difference, leaning Gemini.** Of Gemini's three suggestions, (1) the per-subject paired-delta table and (3) the multi-paragraph cross-system examples are strong candidates because they do carry a lot of body length without substantively advancing the core argument (they provide evidence that the asserted patterns reproduce, which can be validated by a reader who chooses to go to appendix). Suggestion (2) is weaker: the four Supermemory examples are each doing distinct work. Example 1 (Pattern 1), Example 2 (Pattern 2), Example 3 (Pattern 3 plus rubric-limitation), Example 4 (judge-divergence reframe). Dropping Examples 3 or 4 would cost the reader either the rubric-limitation anchor (which feeds §6 Limitations) or the judge-divergence observation. Recommend keeping all four Supermemory examples in body.

Concrete appendix-move recommendation:

- **Move to appendix:** The current §4.6 Table 4.6 (per-subject paired-delta distributions, 8 rows). Keep the summary claim in body; reference appendix for the table.
- **Move to appendix:** The three detailed cross-system Pattern exemplars (Mem0 Ebers Q11, Base Layer Yung Wing Q31, Base Layer Ebers Q1) currently in §4.6 paragraph form. Keep a one-sentence-per-pattern summary in body; move the multi-paragraph examples to appendix.
- **Keep in body:** All four Supermemory examples inside the consolidated §4.4. Each illustrates a distinct mechanism the reader needs.
- **Keep in body:** The Keckley Q21 cross-system table (5 systems by C1 / C3 / Δ). It IS the case study, not supporting detail.

### Recommended §4 Subsection Tree (Consensus + Editor)

```
§4.1  The Cross-Subject Gradient
        — Primary finding: spec improves prediction on low-baseline subjects;
          inversely proportional to pretraining coverage.
        §4.1.1  Franklin as the high-baseline reference
        §4.1.2  Living-user replication (author)

§4.2  Compression: Structure vs. Raw Text
        — 7K-token spec recovers most of the raw corpus lift at 10x to 100x
          smaller context.
        §4.2.1  Question-Improvement Rate: candidate secondary reporting metric

§4.3  Mechanism: Content, Not Format
        — Wrong-spec controls: the effect is content-specific, not
          structure-specific.

§4.4  Composition with Memory-System Retrieval
        — Specification is additive on top of commercial memory systems;
          three of four show positive Delta_spec.
        §4.4.1  Aggregate Performance Across Systems
                — Controlled + native tables, per-system micro-paragraphs
                  (Mem0, Supermemory, Zep, Base Layer). Includes the full
                  Supermemory mixture analysis with the four examples.
        §4.4.2  Common Mechanisms: Interpretation, Over-theorization,
                Principled Refusal
                — Pattern 1 / 2 / 3 framework. One concise exemplar per
                  pattern in body; additional cross-system exemplars in
                  Appendix E.
        §4.4.3  Case Study: Cross-System Refusal on Keckley Q21
                — 5-system table + interpretive reading. Operationalizes
                  Pattern 3 across retrieval substrates.

§4.5  Architectural Convergence: Letta Stateful-Agent Path
        — Independent architecture reaches the same prediction band.
          Compression ceiling documented at Babur.

§4.6  Robustness and Sensitivity
        — Cross-provider response generation, judge-panel sensitivity,
          scope of what the robustness checks do not address.
        §4.6.1  Cross-provider response generation (Tier 2 replication)
        §4.6.2  Judge panel sensitivity (5-judge primary vs 7-judge)
        §4.6.3  What these robustness checks do not address
```

Notes on this tree:

- §4.7 and §4.8 from v9 do not exist anymore. Letta becomes §4.5, Robustness becomes §4.6. §4.8 Scaling and Practical Implications moves out entirely to Discussion §5.5.
- §4.4.1 is a single subsection in the Gemini three-subsection structure. The author can split it into §4.4.1 Aggregate (table only) + §4.4.2 Per-System Micro-Paragraphs (Mem0, Supermemory, Zep, Base Layer) if the Aggregate subsection runs too long, at a cost of one extra heading.
- Letta archival-retrieval path results must remain inside §4.4.1's table as the fourth commercial system. The new §4.5 is the stateful-agent path only. v9 already handles this with a pointer in current §4.4.1; the new tree preserves that pointer.

### Single Biggest Risk (both reviewers flagged similar concern)

Gemini: §4.4 becomes too dense and loses its narrative thread when quantitative results, three-pattern mechanism framework, and Keckley case study all live under one heading. Mitigation: exceptionally clear topic sentences plus transition paragraphs at each subsection boundary.

Mistral: the per-system micro-paragraphs understate the mixture of wins and losses, letting readers misread near-zero aggregates as "no effect" rather than "balanced swings." Mitigation: each micro-paragraph must explicitly carry the mixture signal, not just the aggregate delta.

Both concerns are real. The editor's recommendation is that the author treat the §4.4.1 micro-paragraphs as load-bearing and write each one to carry both (a) the aggregate Δ_spec number and (b) an explicit pointer to the underlying mixture (example: "Supermemory's near-zero aggregate resolves into 37 large improvements and 52 large regressions at the per-question level; the mechanisms for both directions are developed in §4.4.2.").

---

## Reviewer Raw Responses

### Mistral Large

**Q1. Table format within §4.4.** (b) a comparison table plus per-system "micro-paragraphs" (1-2 sentences each). This balances clarity and efficiency. A single table provides a clean high-level comparison, while micro-paragraphs allow nuanced explanation of each system's unique behavior (e.g., Supermemory's near-zero aggregate masking per-question swings). This avoids overwhelming the reader with dense prose while preserving interpretability.

**Q2. Placement of Keckley Q21.** Place Keckley Q21 as a dedicated subsection within §4.4 (e.g., §4.4.3 "Cross-System Refusal: Keckley Q21"). This subsection should follow the per-system results and mechanism patterns, as it exemplifies a general specification-induced behavior (refusal due to dignity axioms) that cuts across all memory systems. Its prominence justifies a named subsection, but its thematic tie to §4.4's compositional analysis keeps it integrated.

**Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis.** (a) integrated into §4.4 as a "common mechanisms" subsection. The patterns are directly tied to the per-system results (e.g., Supermemory's §4.4 analysis already introduces them). Pulling them into §4.3 would fracture the narrative, while a standalone subsection would redundantly rehash §4.4's examples. A "Mechanisms Across Systems" subsection (e.g., §4.4.2) lets readers see how the patterns emerge from the data they just reviewed.

**Q4. Subsection ordering for reader flow.** Order subsections to mirror the logical progression from what the specification does (system-specific results) to how it works (mechanisms) to edge cases (Keckley Q21). Start with the comparison table to ground readers, then dive into per-system nuances, followed by cross-system patterns, and conclude with the refusal subsection to highlight a recurring limitation. This builds from concrete to abstract, ending with a provocative example that primes discussion of rubric limitations.

Ordered list:
1. §4.4.1 Overview and Comparison Table: High-level results with a table of Δ_spec across systems.
2. §4.4.2 Per-System Micro-Analyses: 1-2 sentences per system (Mem0, Supermemory, Zep, Base Layer) with key takeaways.
3. §4.4.3 Common Mechanisms Across Systems: Pattern 1/2/3 synthesis with cross-system examples.
4. §4.4.4 Cross-System Refusal: Keckley Q21: Dedicated subsection on the refusal pattern.

**Q5. Appendix candidates.** None. The author's preference for a tight body is well-served by the proposed structure. The per-system micro-paragraphs and mechanism subsection distill §4.4's complexity without omitting critical details. Keckley Q21's refusal pattern is too central to the specification's limitations to relegate to an appendix, and the comparison table ensures the body remains concise. Raw data (e.g., per-question swings) can be referenced in footnotes or supplemental materials without cluttering §4.4.

**Recommended subsection tree.**
- §4.1 The Cross-Subject Gradient: Primary effect of the specification across 14 subjects.
- §4.2 Compression: Structure vs. Raw Text: Efficiency of the specification vs. full corpora.
- §4.3 Mechanism: Content, Not Format: Content-specificity of the specification's effect.
- §4.4 Memory-System Composition: Specification's additive effect with commercial memory systems.
  - §4.4.1 Overview and Comparison Table: Aggregate Δ_spec across systems.
  - §4.4.2 Per-System Micro-Analyses: Key results and nuances for each system.
  - §4.4.3 Common Mechanisms Across Systems: Pattern 1/2/3 synthesis with examples.
  - §4.4.4 Cross-System Refusal: Keckley Q21: Specification-induced refusal pattern.
- §4.5 Robustness: Sensitivity to response models, judges, and question generation.
- §4.6 Letta Stateful-Agent: Architectural convergence with Base Layer's specification.

(Note from editor: Mistral placed Letta after Robustness. Gemini placed Letta before Robustness. The author's non-negotiable #5 states Robustness moves to the END of Results, which places it AFTER Letta. Gemini's ordering is the one that matches the non-negotiables; Mistral's Letta-after-Robustness ordering contradicts non-negotiable #5 and should be disregarded on this point.)

**Single biggest risk.** The author might underemphasize the per-question variance in §4.4.2's micro-paragraphs, reducing them to superficial summaries (e.g., "Zep benefits from the specification") instead of highlighting the mixture of wins/losses (e.g., "Zep's +0.17 Δ_spec masks 8 large regressions and 9 large improvements"). The risk is that readers misinterpret near-zero aggregates (e.g., Supermemory) as "no effect" rather than "balanced swings." Explicitly flagging the variance in each micro-paragraph is critical.

### Gemini 2.5 Pro

**Q1. Table format within §4.4.** (b) Use a comparison table plus per-system "micro-paragraphs." This format provides the best of both worlds: the table offers a scannable, quantitative overview for direct comparison, while the micro-paragraphs allow for concise, targeted interpretation of each system's unique behavior. This structure efficiently highlights the general positive trend for Mem0, Letta, and Zep, while creating a natural entry point for the more complex, bimodal story of Supermemory without letting it dominate the initial summary.

**Q2. Placement of Keckley Q21.** The Keckley Q21 analysis should be a dedicated subsection at the end of the consolidated §4.4 (e.g., §4.4.3). Placing it after the general per-system results and the explanation of the common mechanisms allows it to function as a powerful, concrete case study. It perfectly illustrates "Pattern 3" (principled refusal penalized by the rubric) and demonstrates that this is a specification-driven effect that reproduces across different retrieval architectures, solidifying the paper's mechanistic claims.

**Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis.** (a) Integrate the Pattern 1/2/3 content into §4.4 as a "common mechanisms" subsection. This is the most logical placement because these patterns are the explanatory framework for the quantitative results presented at the start of §4.4. By first showing what happened (the performance of each memory system) and then explaining why it happened (the underlying mechanisms of interpretation, over-theorization, and refusal), the section builds a clear and compelling narrative for the reader.

**Q4. Subsection ordering for reader flow.** The most effective order for the consolidated §4.4 is to move from the general quantitative finding to the specific qualitative explanation, and finally to a powerful illustrative example. This "what, why, for example" structure is intuitive and analytically robust. It first establishes the primary result (the specification's additive effect), then provides the theoretical lens to understand the variance in that result (the three patterns), and concludes with a memorable case study (Keckley Q21) that makes the mechanism concrete.

Ordered list of subsections within §4.4:
1. Aggregate Performance Across Systems
2. Common Mechanisms: Interpretation, Over-theorization, and Principled Refusal
3. Case Study: The Keckley Q21 Cross-System Refusal

**Q5. Appendix candidates.** The author's preference for a tight body can be served by moving the following detailed but non-essential elements to an appendix:

- The large "Per-subject paired-delta distributions" table from the current §4.6. The main text effectively summarizes its key finding (that every system's aggregate score is a mixture of large wins and losses) and can simply reference the full table in the appendix.
- Two of the four Supermemory examples from the current §4.4. The main text should retain one clear example of the specification helping (e.g., Example 1) and one of it hurting (e.g., Example 2) to illustrate the bimodal mechanism. The other two examples (3 and 4) are valuable detail but not critical to the core argument and can be moved.
- The detailed, multi-paragraph cross-system examples for Patterns 1, 2, and 3 from the current §4.6. The main text can present a single, concise example for each pattern to make the concept clear, while referencing the appendix for additional cross-system evidence.

**Recommended subsection tree.**
- §4.1 The Cross-Subject Gradient: Establishes the primary finding that the specification improves prediction on low-baseline subjects.
- §4.2 Compression: Structure vs. Raw Text: Shows the specification captures most of the raw corpus's predictive value at a fraction of the token cost.
- §4.3 Mechanism: Content, Not Format: Demonstrates the effect is driven by the specification's specific content, not just its structure.
- §4.4 Composition with Memory-System Retrieval: Evaluates the specification's additive effect on top of existing memory systems.
  - §4.4.1 Aggregate Performance Across Systems: Presents the quantitative lift for Mem0, Zep, and Letta, and the bimodal result for Supermemory.
  - §4.4.2 Common Mechanisms: Interpretation, Over-theorization, and Principled Refusal: Explains the three underlying patterns that drive per-question outcomes.
  - §4.4.3 Case Study: The Keckley Q21 Cross-System Refusal: Provides a concrete example of a spec-induced behavior that reproduces across all systems.
- §4.5 Architectural Convergence: The Stateful-Agent Path: Shows Letta's self-editing memory block independently arrives at a similar high-performing representation.
- §4.6 Robustness and Sensitivity: Confirms the main findings hold across different response models and judge panels.

**Single biggest risk.** The biggest risk is that the newly consolidated §4.4 becomes too dense and loses its narrative thread. By combining quantitative system comparisons, a qualitative three-pattern mechanistic framework, and a specific case study, the section now carries a heavy analytical load. The author must use exceptionally clear topic sentences and transition paragraphs to guide the reader through the "what," "why," and "for example" logic, or the section will feel disjointed and overwhelming.

---

## Where Reviewers Disagree (and Editor's Default Path)

1. **Number of §4.4 subsections (3 vs 4).** Mistral splits Aggregate Table and Per-System Micro-Paragraphs into two separate subsections (§4.4.1 and §4.4.2); Gemini treats both as one §4.4.1. Editor default: **follow Gemini's three-subsection structure** unless the combined §4.4.1 runs long in draft (over 3 pages). One fewer heading reads cleaner.

2. **Ordering of Letta (§4.5) vs Robustness (§4.6 in Gemini's tree / §4.5 in Mistral's tree).** Mistral places Letta AFTER Robustness; Gemini places Letta BEFORE Robustness. The author's non-negotiable #5 states Robustness moves to the END of Results. Gemini's order matches. Editor default: **Letta first, Robustness last, per the author's non-negotiable.** Mistral's ordering on this point violates a non-negotiable and is disregarded.

3. **Appendix moves (none vs three).** Mistral recommends no appendix moves; Gemini recommends three. Editor default given the tight-body preference the author stated: **take two of Gemini's three moves.** Move the per-subject paired-delta table (current §4.6 Table 4.6) to appendix. Move the three detailed cross-system Pattern 1 / 2 / 3 exemplars to appendix, keeping one concise exemplar per pattern in body. DO NOT move the Supermemory examples; all four earn their place.

## Summary

The two reviewers converge strongly on the core formatting: (b)-format table with per-system micro-paragraphs, Keckley Q21 as last subsection of §4.4, Pattern 1 / 2 / 3 integrated as mid-subsection of §4.4, "what-why-for-example" ordering. They also converge on the main risk: §4.4 density. They diverge only on (a) whether to use three or four subsections inside §4.4 and (b) how aggressively to move material to appendix. The editor's recommended tree, flagged disagreements with defaults, and the specific per-system micro-paragraph guardrail (each micro-paragraph carries both aggregate Δ and an explicit mixture-signal pointer) are above.

Author decides from here.
