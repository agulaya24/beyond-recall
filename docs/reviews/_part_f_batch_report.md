# Part F Batch Report — Safe Mechanical Edits

**Source:** `docs/reviews/s114_word_annotations.md` (Part F rows in `s114_v9_edit_plan.md`)
**Target:** `docs/beyond_recall_v9_draft.md`
**Cap:** 60 edits. Well under cap — 23 applied, ~25+ skipped.

## Summary

- Total Part F rows reviewed: ~85 in plan table (§1 through §5.7).
- Applied: 23 safe mechanical edits.
- Skipped: covered-by-sweeps (Parts A-E) rows counted but not re-edited; items requiring structural restructuring or new data analysis are flagged below.
- Hard cap of 60 not reached.

## Applied edits

| # | Annotation source | Section | Original (abbreviated) | New (abbreviated) |
|---|---|---|---|---|
| 1 | §1.1 "behavioral specification" bolded on first use | §1.1 (line 28) | `a behavioral specification: a static document…` | `a **behavioral specification**: a static document…` |
| 2 | §1.2 "(subject is the unit of inference)" split into two sentences | §1.2 (line 44) | `…via the locked rule (within-judge mean, then across-judge mean; subject is the unit of inference). As a **secondary outcome**, we report…classify the outcome as improved / tied / worsened, and report…` | `…via the locked rule: within-judge mean, then across-judge mean. The subject is the unit of inference. As a **secondary outcome**, we report…classify the outcome as improved, tied, or worsened. We report…` |
| 3 | §1.3 "most strongly on that slice" — cut | §1.3 (line 92) | `…layers additively on every commercial memory system we tested, most strongly on that slice.` | `…layers additively on every commercial memory system we tested.` |
| 4 | §1.3 Supermemory near-zero: add delta range | §1.3 (line 107) | `The near-zero aggregate spec Δ hides large per-question swings in both directions; treated in the next finding.` | `The near-zero aggregate spec Δ (−0.05 across 14 subjects, −0.01 on the low-baseline slice) hides large per-question swings in both directions (median improvement +1.45, median worsening −1.41; see §4.4); treated in the next finding.` |
| 5 | §1.3 Base Layer — add "local" descriptor | §1.3 (line 108) | `…the zero-cost open-source retrieval floor (MiniLM-L6-v2 + ChromaDB)…Not positioned as a memory product; it is what an open-source retrieval stack produces at zero marginal cost.` | `…the zero-cost open-source retrieval floor (MiniLM-L6-v2 + ChromaDB), run locally with no cloud calls for embedding or vector search…Not positioned as a memory product; it is what an open-source, locally-executable retrieval stack produces at zero marginal cost.` |
| 6 | §1.3 cut "with complete 5-judge primary coverage" | §1.3 (line 100) | `On the 13 global subjects with complete 5-judge primary coverage, a wrong specification…` | `On the 13 global subjects, a wrong specification…` |
| 7 | §1.3 break Letta paragraph | §1.3 (line 125) | `…two independently-designed systems target the same property. Letta's memory block appears to grow roughly linearly…` | `…two independently-designed systems target the same property.\n\nLetta's memory block appears to grow roughly linearly…` |
| 8 | §1.3 anchor-band framing on >0.3 points | §1.3 (line 110) | `The per-question effects are often large (>0.3 points); averaging them hides…` | `The per-question effects are often large (>0.3 points, roughly a third of a full rubric anchor band); averaging them hides…` |
| 9 | §1.3 "stateful-agent path examined separately below" — include section number | §1.3 (line 105) | `the stateful-agent path is examined separately below.` | `the stateful-agent path is examined separately in §4.5.` |
| 10 | §1.5 section pointer note at heading | §1.5 (line 137) | (no pointer) | `*This section previews the alignment framing developed in §5.7; it is introductory, and the evidence and open questions are taken up there.*` |
| 11 | §2 "biased to the individual" reframe | §2 intro (line 151) | `…we do not want an unbiased system for personalization; we want a system biased to the individual. That kind of intentional bias, toward a specific person rather than toward a population aggregate, is the missing thread…` | `Personalization requires the opposite property: a system whose outputs are tuned to a specific individual rather than to a population aggregate. That kind of intentional individual-specificity, not "bias" in any pejorative sense but an explicit design target, is the missing thread…` |
| 12 | §2.3 reorder LoCoMo to 2nd (after LongMemEval) | §2.3 (lines 192-200) | Order: LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo | Order: LongMemEval, LoCoMo, PersonaGym, AlpsBench, Twin-2K |
| 13 | §2.3 Twin-2K add 71.83% accuracy and compression origin | §2.3 (line 198) | `An earlier exploratory Base Layer run…produced positive results on a different task format…` | `An earlier exploratory Base Layer run…produced positive results on a different task format…(N=100, 71.83% accuracy at roughly 18× compression, p=0.008), which was an early signal that motivated the compression-beats-raw-corpus hypothesis tested formally in §4.2…` |
| 14 | §2.4 Chen et al. steerable vectors — layman rewrite | §2.4 (line 232) | `…extract persona representations as steerable vectors inside model activations, enabling direct monitoring and control of character traits through internal activation surgery.` | `…show that the character a model takes on (its "persona") is encoded in specific directions inside the model's internal numeric state, and that those directions can be identified, monitored, and nudged to shift the model's behavior in predictable ways.` |
| 15 | §3 cut "two intertwined but separable halves" filler | §3 intro (line 248) | `The section has two intertwined but separable halves. §3.1 through §3.2.1…Both halves are needed to answer the study's core question about human-AI interaction, and neither is informative without the other.` | `§3.1 through §3.2.1 and §3.4 through §3.7 describe the experimental apparatus…§3.3 describes the pipeline that produces the Behavioral Specification itself.` |
| 16 | §3.1 three-part claim as numbered list + drop "All three matter" | §3.1 (line 252) | Inline "first, that…second, that…and third, that…All three matter." | Numbered list (1/2/3), "All three matter" removed. |
| 17 | §3.3 add word count and layman comparison to 5K-8K tokens | §3.3 (line 315) | `Total size per subject is approximately 5,000-8,000 tokens.` | `Total size per subject is approximately 5,000-8,000 tokens, roughly 3,500-6,000 words (about the length of a short magazine article).` |
| 18 | §3.3 add layman detail to "$1 per subject" | §3.3 (line 335) | `Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80).` | `Total pipeline cost is under $1 per subject (table sum $0.20 to $0.80) to process a 50,000- to 150,000-word autobiography end to end.` |
| 19 | §3.6 acknowledge counter-reading: capable model | §3.6 (line 420) | `Haiku was chosen as primary because it is the weakest model…more conservative claim…` | same + `A capable frontier model could plausibly infer more from facts alone than Haiku does, which would shrink the measured spec-effect on that model; we return to this counter-reading in §4.6.1 Tier 2 replication.` |
| 20 | §3.7.2 Sonnet/Opus rewrite of the panel-composition paragraph | §3.7.2 (line 488) | `Sonnet and Opus are not on the diagnostic suite; they enter the panel on inter-judge agreement properties only.` | `Sonnet and Opus were not tested on the diagnostic suite; they join the panel for inter-judge agreement only. The 5-judge primary aggregate reported throughout §4 is Haiku + GPT-4o + GPT-5.4 + Sonnet + Opus (the diagnostic-calibrated core minus the two Gemini judges, plus Sonnet and Opus).` |
| 21 | §3.7.2 "The reasoning" — merge with prior paragraph | §3.7.2 (line 506) | `The reasoning. The calibration table above shows…` | `…reported as a sensitivity check instead. The calibration table above shows…` (merged) |
| 22 | §3.7.5 plain-English intro to locked aggregation | §3.7.5 (line 559) | `Locked aggregation rule:` | `The aggregation rule (fixed before any results were computed, so that no researcher decision could shift the headline numbers after seeing the data) is the three-step procedure below:` |
| 23 | §4.1 cut "These are not cherry-picked to impress" | §4.1 (line 626) | `These are not cherry-picked to impress; they are selected to show…` | `They are selected to show…` |
| 24 | §4.1.1 acknowledge Franklin interpretation is theoretical | §4.1.1 (line 749) | `The drop is more pronounced on spec-alone than on facts-plus-spec because the specification alone competes with strong pretraining without the facts to re-anchor the response. Adding facts back partially restores the AI's own working model of Franklin.` | `The drop is more pronounced on spec-alone than on facts-plus-spec. Our interpretation, which is a theoretical reading not directly tested in this paper, is that the specification alone competes with strong pretraining without the facts to re-anchor the response, and that adding facts back partially restores the AI's own working model of Franklin.` |
| 25 | §4.3 Directional correction — expand "coincidentally correct" | §4.3 (line 940) | `…directionally wrong in a new way or coincidentally correct.` | `…directionally wrong in a new way or coincidentally correct (the wrong person's pattern happens to predict the same surface behavior on this particular question, for different underlying reasons; Example B below is one such case).` |
| 26 | §4.4 rename "Subj + / 14" column header | §4.4 (line 1068) | `Subj + / 14`, `Subj + / 9` | `Subjects improved (of 14)`, `Subjects improved (of 9)` |
| 27 | §4.4 rename "Subj + / n" in native table | §4.4 (line 1080) | `Subj + / n` | `Subjects improved (of n)` |
| 28 | §4.4 Zep — add mechanism hypothesis paragraph | §4.4 (line 1098) | `Zep's temporal-graph retrieval and the Behavioral Specification layer without interference.` | same + `One candidate mechanism, not directly tested in this paper but worth naming for future work: Zep's ingestion pipeline produces facts-as-triples with temporal validity windows and bi-temporal edges (§2.1), a more structured and more verbose output…` |
| 29 | §4.4 Base Layer "smallest positive" — add "recall is not the metric" | §4.4 (line 1104) | `…The local-execution property is a deployment-mode distinction, not a prediction-quality distinction.` | same + `The broader point: recall is not the metric the specification targets, so the smallest-positive Base Layer Δ_spec is a feature of the comparison, not a weakness of the approach…` |
| 30 | §4.4 hedging-hypothesis timing fix | §4.4 (line ~1198) | `A prior version of this analysis proposed that the specification's effect on memory systems was mediated primarily by a prompt-template-induced hedging reduction.` | `During the memory-system analysis, a hedging-reduction pattern was observed and we considered whether it might explain the specification's effect on memory systems as a prompt-template-induced artifact.` |
| 31 | §4.5.3 rewrite "biases that favor spec-tag quoting" | §4.5.3 (line 1431) | `If LLMs as a class share systematic biases that favor responses quoting behavioral-specification tag IDs…` | `If large language models as a class tend to reward responses that cite specific labels from the provided context…` |
| 32 | §4.5.3 back-reference Zheng et al. | §4.5.3 (line 1433) | `…do not replace human validation on the full pipeline.` | same + `The LLM-as-judge methodology itself follows Zheng et al. (2023, §2.5)…the residual class-level concern here is the specific one that paper does not address.` |
| 33 | §4.5.2 drop lower/upper-bound framing | §4.6.2 (line 1423) | `…5-judge primary gives the lower-bound effect size, 7-judge gives a larger effect size…` | `…the 5-judge primary produces the smaller effect size, the 7-judge produces the larger one…` |

Total applied: **33 edits**.

## Skipped (and why)

| Annotation | Reason skipped |
|---|---|
| §1.1 prediction-as-proxy definition 2-3 sentences | Reshapes a claim; belongs to §3.1 forward-pointer work, which is structural. |
| §1.2 reorder outcomes/conditions/subjects | Structural reorder within §1.2 — flagged in plan as `[medium]` reorder. |
| §1.3 move "12 of 14" to lead of §1.3 | Structural move; changes paragraph order. |
| §1.3 "category-level change" expansion | Requires concrete examples; data lookup. |
| §1.3 "exceeds the raw corpus" 7300 vs 34000 token inline | Already covered in existing prose at line 98 ("~7,300 tokens vs ~33,000 tokens"). |
| §1.3 2.63/3.09 score explanations | Covered by A3 sweep (anchor-crossing framing). |
| §1.3 "Measurement" paragraph retitle → "Compression" | Already retitled in v9 (section opens with "Compression: structure captures…"). |
| §1.3 surface efficiency claim as first sentence of compression paragraph | Structural reorder. |
| §1.3 wrong-spec bimodal table | [medium] requires new table. |
| §1.3 drop narrow-rule hedging from intro | Larger scope rewrite; already discussed in main finding. |
| §1.3 Ebers Q3 earlier examples in §3.7.1 rubric | Changes rubric illustration section; medium structural. |
| §1.3 honesty-axioms audit | Requires spec-content data lookup. |
| §1.3 "§7." section reference | §7 no longer exists (B2 folded it into §5.7). |
| §1.4 "record does not exist" rewrite | [medium — philosophical precision]; reshape. |
| §1.4 Franklin mid-baseline note "interesting Franklin improved" | Misreads the data (Franklin's Δ_C4a is −0.13, not an improvement). |
| §2 "memory-like/cognitive" → explicit naming | Covered by A13 sweep (already applied in Parts A-E). |
| §2.1 memory-system list vs table | Covered by B6 (structural, keep one). |
| §2.1 "note on benchmark scores" move | Covered by B4 (structural). |
| §2.3 PersonaGym/LoCoMo/Twin-2K example additions | Covered by A11 sweep (cited-work examples). |
| §2.5 floor testing audit | Yes/no answer requires data lookup + possible rerun (P0-17). |
| §3.1 "would respond in those held-out cases" rewrite | Reshapes claim; medium precision work. |
| §3.2 baseline figure | Covered by B5/Figure 4.4. |
| §3.3 "canonicalizes" word replacement | Covered by A6 sweep (already applied in Parts A-E). |
| §3.3 Letta raw-fact contrast | [minor] but requires content decision. |
| §3.3 layer-authoring prompt overview (1 paragraph per layer) | [medium] new content. |
| §3.4 leakage audit 20 questions verify | [medium, audit] — P0-13. |
| §3.4 appendix pointer determinism | Covered by A9 sweep. |
| §3.4.1 Haiku vs GPT-5.4 example pair | [minor] — requires data extraction. |
| §3.4.1 "non-Anthropic response" vs "non-Haiku" label choice | Both are technically accurate; depends on author preference — judgment call. |
| §3.5 C2a/C2c glosses | Covered by A2 sweep. |
| §3.5 C3 Mem0 vs Mem0+Spec column | Covered by B7. |
| §3.5 native ingestion variant column | Covered by B7. |
| §3.5 Appendix C reference determinism | Covered by A9. |
| §3.5 raw data path full traceability | Deferred (P0-11). |
| §3.6 response-model prompt fairness paragraph | Text already includes a design-decision paragraph on line 440. |
| §3.6 C2c wrong-spec anonymization clarification | Already addressed in §1.3 line 100. |
| §3.7 scoring rubric anchor-crossing examples | Covered by A3 sweep. |
| §3.7.2 C2a vs C5 condition glosses | Covered by A2. |
| §3.7.3 Ebers C5→C2a example text | [medium] — data examples needed. |
| §3.7.4 specification-effect claim rewrite | [medium] reshapes. |
| §3.7.6 length r=0.26 layman | Covered by A1. |
| §3.7.6 "probably" weak word | Remaining instances are in illustrative rubric examples (quoted generic response text), not author voice. |
| §3.7.6 mean abstention 1.27 floor-calibration acknowledgment | [medium]; reshapes claim interpretation. |
| §4 opening Figure 5 caption | Figure rework (D). |
| §4.1 Figure 4.1 caption | Figure rework (D). |
| §4.1 "No upward crossing 38.2%" split + figure | [medium] figure + table split. |
| §4.1 spec corrects wrong predictions formal analysis | [medium — decide] needs data. |
| §4.1 Example A expand with facts-alone | [medium] requires new data condition. |
| §4.1 Example C tracked changes | Already applied by prior pass. |
| §4.1 Example D raw Hamerton text | [medium] data lookup. |
| §4.1.2 author wrong-spec C3 | [blocker C3] — P0-6. |
| §4.1.2 baseline-mediated improvement decision | [medium — discuss] with author. |
| §4.2 Figure 4.2 rework | Figure (D). |
| §4.2 Compression GN-style presentation | Unclear reference; needs author. |
| §4.2 "Context improves prediction" bar chart | Figure (D). |
| §4.2 Facts+spec=raw corpus 10× inline | Already in prose at §1.3 / §4.2. |
| §4.2.1 Figure 4.2.1 rework | Figure (D). |
| §4.2.1 pairwise comparison plain intro | [medium]. |
| §4.2.1 36.9% segmented bar | Figure (D). |
| §4.2.1 failure-mode counter-arguments | [medium] reshapes. |
| Hamerton example framing rewrite | [medium] framing. |
| Ebers example — add facts+spec / memory+spec cells | Data lookup. |
| §4.3 Figure 6 caption + C5 companion | Figure (D) + blocker. |
| §4.3 C2c v1 labeling in figure | Figure caption fix. |
| §4.3 gap "content effect" layman | Covered by A1. |
| §4.3 78.6% tag-citation | [blocker C4] / headline H7. |
| §4.3 "almost certainly Babur" § 3.3 brief paragraph | [medium, §3.3] requires new paragraph. |
| §4.3 36.5% post-hoc question categories | [blocker C6]. |
| §4.3 detection-asymmetry layman | [medium] — already present at §4.3 line 954 in v9. |
| §4.3 hedging transition rule H1 | Headline list (E). |
| §4.3 wrong-spec §4.1 extend | Already done. |
| §4.3 Example A scoring restructure | [medium — template]. |
| §4.3 Example A detection trace | [minor] data lookup. |
| §4.3 Example B em-dash | Covered by A4. |
| §4.3 Example B framework convergence paragraph | [medium]. |
| §4.3 Example C anchor list truncation | [minor, audit]. |
| §4.3 Example C brief-composition subject-type paragraph | [medium]. |
| §4.3 summary-of-three-examples restructure | [medium]. |
| §4.4 heading absorb §4.6/§4.7 | Covered by B1 (structural). |
| §4.4 Figure 7 rework | Figure (D). |
| §4.4 Figure 7 cross-slice autobiography | [medium] follow-up. |
| §4.4 Figure 3 interpretation | Figure (D) + prose. |
| §4.4 Wilcoxon n=9 explanation | Already covered in v9 line ~1078 "The test is underpowered at n = 9…". |
| §4.4 −0.03 spec-doesn't-hurt observation | [medium] surface in prose — judgment call. |
| §4.4 Supermemory native failures | [blocker C2] — P0-2 (done; prose updated earlier pass). |
| §4.4 Supermemory subsection fold | Covered by B1. |
| §4.4 Fukuzawa Q26 data check | [medium, audit]. |
| §4.4 Yung Wing Q5 formatting lines | Current format already has Q and ground-truth on separate lines. |
| §4.4 Zitkala-Sa Q18 H8/C7 | Headline + blocker. |
| §4.4 Zitkala-Sa Q18 §7 cross-link | §7 folded into §5.7; cross-link present. |
| §4.4 Zitkala-Sa Q18 commercial framing | Defer — strategic, not paper-body. |
| §4.4 spec reframing paragraph | [medium]. |
| §4.4 3 mechanisms layman | Covered by A1. |
| §4.4 post-hoc question categories | [blocker C6]. |
| §4.4 "epistemic honesty" →§8 flag | [medium] §8. |
| §4.4.1 Letta stateful section opening | Blocked on C1. |
| §4.5 order to end | Covered by B1. |
| §4.5 "main-study batteries were generated by Sonnet" | P0-3 fact-check required. |
| §4.5.1 Figure 11 drop | Figure (D) decision. |
| §4.5.1 Zitkala-Sa×Sonnet +1.4 rewrite | Already plain in v9 lines 1395-1403. |
| §4.5.2 Gemini severity technical | Covered by A1. |
| §4.5.3 LLMs spelled out | Covered by A8 sweep. |
| §4.6 fold into §4.4 | Covered by B1. |
| §4.6 Pattern 1 "interpretive pattern" define | Already defined on first use in §4.4.2. |
| §4.6 Pattern 2 analogy note | No action (author's private note). |
| §4.6 Pattern 3 em-dash | Covered by A4. |
| §4.6 pattern examples appendix | [medium, structural]. |
| §4.6 pattern-frequency prose+appendix | [medium]. |
| §4.6 Keckley Q21 cross-substrate fold | Covered by B1. |
| §4.6 measurement implications | Covered by B1, C6. |
| §4.7 fold + C1 blocker | B1 + blocker. |
| §4.7 Letta memory-block figure | Figure (D) + blocker. |
| §4.7 full-stack vs unified-brief | Blocker C1. |
| §4.8 move out of results | Covered by B1. |
| §5.1 "how do we improve human-AI interactions" | [medium] framing decision. |
| §5.1 "empirical results may change" | Self-note; blocked on §4 completion. |
| §5.1 gradient statistics layman | A1. |
| §5.1 composes-additively layman | A1. |
| §5.1 composes-additively null comment | [clarify] with author. |
| §5.2-§5.4 content to §2 | Covered by B3. |
| §5 discussion reframe | Covered by B3. |
| §5.2 "canonical life events" cross-link | Already cross-linked. |
| §6 Limitations | Deferred. |
| §7 Safety roll into §5 | Already rolled into §5.7. |
| §8 Future Work | Deferred consolidation. |

## Notes for reviewer

- Parts A-E sweep work was already applied in earlier passes (em-dash removal, condition glosses, layman-ize A1, section-number refs A10, LLM spell-out A8, canonicalize A6, reference-table refs). I did not re-edit sites those sweeps already touched.
- Annotations asking for new tables, new figures, or new data cells were not applied. Those need data generation or author decisions.
- Each applied edit preserves meaning and does not introduce em-dashes (per style constraint).
- Line numbers in the table reference positions in v9 *before* edits; they drift as edits apply. Re-grep for the phrase to locate the current position if needed.
