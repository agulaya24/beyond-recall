# v11.8 Section-Pointer Audit -- mechanical
_Generated: 20260505_094736_
_Paper: `beyond_recall_v11_8_draft.md`_

- Total headings parsed: **71**
- Total §X refs found: **502**
- OK (target exists): **502**
- MISSING (target does not exist): **0**

## Heading map

| § | Title | Line |
|---|---|---:|
| §1 | Introduction | 11 |
| §1.1 | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 |
| §1.2 | What we tested | 40 |
| §1.3 | What we found | 104 |
| §1.4 | What this implies | 136 |
| §2 | Prior Work, Industry Benchmarks, The Fifth Target | 150 |
| §2.1 | Memory and personalization benchmarks | 158 |
| §2.2 | Memory systems for LLM agents | 186 |
| §2.3 | Traceability and Reasoning Traces | 213 |
| §2.4 | Cognitive and representational foundations | 252 |
| §2.5 | LLM-as-judge | 268 |
| §3 | Study Design | 272 |
| §3.1 | Operationalizing representational accuracy | 278 |
| §3.2 | Subjects | 294 |
| §3.2.1 | Pretraining-coverage variance | 327 |
| §3.3 | Question Battery Formation | 341 |
| §3.3.1 | Circularity controls | 361 |
| §3.4 | Experimental conditions | 377 |
| §3.5 | Response models | 416 |
| §3.6 | Evaluation: LLM-as-judge with calibration | 450 |
| §3.6.1 | Judge panel | 472 |
| §3.6.2 | Score interpretation | 490 |
| §3.6.3 | Calibration | 525 |
| §3.6.4 | Inter-judge agreement | 559 |
| §3.6.5 | Aggregation | 579 |
| §3.6.6 | Rubric-handling limitations (validity audit) | 589 |
| §3.7 | Base Layer Pipeline for the Behavioral Specification | 633 |
| §4 | Results | 669 |
| §4.1 | The cross-subject gradient | 685 |
| §4.1.1 | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 |
| §4.1.2 | The gradient at the high-baseline end (Franklin reference) | 865 |
| §4.2 | Compression: structure vs. raw text | 877 |
| §4.2.1 | Per-question improvement rate | 949 |
| §4.3 | Mechanism: Content, Not Format | 996 |
| §4.4 | Memory-system composition | 1123 |
| §4.4.1 | Aggregate performance across systems | 1131 |
| §4.4.2 | Where the spec helps, where it hurts, and which question types route to each | 1194 |
| §4.4.3 | Case study: cross-system refusal on Keckley Q21 | 1289 |
| §4.4.4 | Two statistical signatures | 1321 |
| §4.5 | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 |
| §4.6 | Robustness and sensitivity | 1360 |
| §4.6.1 | Cross-provider response generation (Tier 2 replication) | 1366 |
| §4.6.2 | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 |
| §4.6.3 | Battery composition sensitivity | 1406 |
| §4.6.4 | Wrong-spec derangement protocol sensitivity | 1420 |
| §4.6.5 | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 |
| §4.6.6 | What these robustness checks do not address | 1474 |
| §4.7 | Summary of §4 and bridge to discussion | 1482 |
| §5 | Discussion | 1505 |
| §5.1 | Synthesis: what the seven findings together establish | 1509 |
| §5.2 | Why the gradient is the load-bearing finding | 1521 |
| §5.3 | Retrieval is not interpretation | 1533 |
| §5.4 | Composition with retrieval | 1543 |
| §5.5 | Wrong-spec mechanism and hedging elimination | 1557 |
| §5.6 | Compression and what makes personalization operationally tractable | 1569 |
| §5.7 | Privacy and the case for user-held representation | 1579 |
| §5.8 | Closing argument | 1591 |
| §6 | Limitations | 1601 |
| §6.1 | Subject sample | 1605 |
| §6.2 | Measurement apparatus | 1621 |
| §6.3 | Pipeline and specification stability | 1635 |
| §6.4 | Scope of exploration | 1662 |
| §7 | Future Work | 1674 |
| §7.1 | Measurement methodology | 1678 |
| §7.2 | Subject and corpus expansion | 1688 |
| §7.3 | Specification design and composition | 1694 |
| §7.4 | Production serving and infrastructure | 1700 |
| §7.5 | Stateful-agent implementations and temporal drift tracking | 1704 |
| §7.6 | Safety-alignment integration | 1720 |
| §8 | Data, code, and reproducibility | 1736 |
| §9 | References | 1758 |

## MISSING references (target section does not exist)

_None._

## All references with current target

| Ref line | §Ref | Status | Target title | Target line | Context |
|---:|---|---|---|---:|---|
| 14 | §4.1 | OK | The cross-subject gradient | 685 | FUTURE-WORK NOTE (Aarik 2026-04-30, during §4.1 walk): |
| 15 | §1 | OK | Introduction | 11 | Consider adding a worked example to §1 (Introduction) for the production release. |
| 16 | §3 | OK | Study Design | 272 | we're working with (responses, judging, transitions) before §3." |
| 17 | §1 | OK | Introduction | 11 | Likely candidates for the worked example to mirror in §1: |
| 18 | §3.6.2 | OK | Score interpretation | 490 | - §3.6.2 multi-anchor crossings (Seacole Q2, Hamerton Q25, Bernal Dí |
| 19 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | - §3.7 Hamerton specification examples (Anchors A1, Core, Predicti |
| 20 | §4.1.1 | OK | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 | - §4.1.1 Seacole Q2 worked rubric example across condition bands |
| 26 | §2.2 | OK | Memory systems for LLM agents | 186 | range depending on provider, model, and benchmark variant (§2.2). Optimizing further on recall leaves something more fundam |
| 28 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | al patterns; the operational definition is developed across §3.7. The Behavioral Specification is the artifact that captures |
| 30 | §2.1 | OK | Memory and personalization benchmarks | 158 | etive patterns to new situations the system has never seen. §2.1 positions each benchmark against what this paper measures, |
| 32 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | response in the held-out text on a 1-5 interpretive rubric (§3.6). Accurate prediction on held-out text is evidence that the |
| 34 | §2.4 | OK | Cognitive and representational foundations | 252 | tering them. See Sharma et al. 2023, Perez et al. 2022, and §2.4 (Jain et al. 2025). Whether an accurate representation also |
| 34 | §7 | OK | Future Work | 1674 | ehalf), are open questions of the broader research program (§7). |
| 36 | §2.3 | OK | Traceability and Reasoning Traces | 213 | back to its grounding facts and source passages appears in §2.3. |
| 42 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | e **question battery** (size and composition per subject in §3.6). The test was whether each system, under each tested condi |
| 44 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | g-half corpus through an extraction-and-authoring pipeline (§3.7). The pipeline distills the recurring patterns of how the s |
| 48 | §4.1 | OK | The cross-subject gradient | 685 | em, the full extracted fact list, or the raw source corpus (§4.1). |
| 49 | §4.1 | OK | The cross-subject gradient | 685 | ffect is largest on people the model does not already know (§4.1). |
| 50 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ation, applied in its place, does not reproduce the effect (§4.3). |
| 51 | §4.4 | OK | Memory-system composition | 1123 | er-question patterns and shift with retrieval architecture (§4.4). |
| 52 | §4.2 | OK | Compression: structure vs. raw text | 877 | ve accuracy of an 80-400K-token (~60-300K-word) raw corpus (§4.2). |
| 56 | §4.4.1 | OK | Aggregate performance across systems | 1131 | –H5 results: the cross-system retrieval-overlap divergence (§4.4.1, with sensitivity in §4.6.5), the Letta stateful-agent case |
| 56 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | m retrieval-overlap divergence (§4.4.1, with sensitivity in §4.6.5), the Letta stateful-agent case study (§4.5; Appendix G), t |
| 56 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ensitivity in §4.6.5), the Letta stateful-agent case study (§4.5; Appendix G), the abstention-credit validity audit (§3.6.6) |
| 56 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | y (§4.5; Appendix G), the abstention-credit validity audit (§3.6.6), and the per-subject wrong-spec heterogeneity table (§4.6. |
| 56 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | 3.6.6), and the per-subject wrong-spec heterogeneity table (§4.6.4). These are labeled where they appear and are reported as e |
| 58 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | ion score on the 1-5 rubric across a 5-judge primary panel (§3.6).[^primary-aggregation] Cross-subject claims are calculated |
| 58 | §4.2.1 | OK | Per-question improvement rate | 949 | ontext condition helps relative to the comparison baseline (§4.2.1), not just by how much it helps when averaged. The formal p |
| 58 | §4.2.1 | OK | Per-question improvement rate | 949 | and failure-mode analysis for the secondary outcome are in §4.2.1; full operational details for both outcomes are in §3.6. |
| 58 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | n §4.2.1; full operational details for both outcomes are in §3.6. |
| 60 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | ns are aggregated across the 14 subjects. Full mechanics in §3.6. |
| 62 | §3.4 | OK | Experimental conditions | 377 | n (the provider's own ingestion pipeline); design detail in §3.4 and §3.5. Running in parallel across both is the Behavioral |
| 62 | §3.5 | OK | Response models | 416 | ovider's own ingestion pipeline); design detail in §3.4 and §3.5. Running in parallel across both is the Behavioral Specific |
| 78 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | l variant (Franklin's specification) reported separately in §4.1.2. |
| 80 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | e Behavioral Specification. Full methodology and results in §4.5. |
| 82 | §3.2 | OK | Subjects | 294 | on) to 422,772 words (Babur). Full source references are in §3.2. |
| 84 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | s mark categorical shifts in answer quality (full rubric in §3.6, summarized in the table below). Crossing an integer anchor |
| 94 | §3.6.2 | OK | Score interpretation | 490 | s-anchor rule for fractional scores (e.g., 2.5, 3.4), is in §3.6.2. Example questions per subject and panel composition are in |
| 94 | §3.6.1 | OK | Judge panel | 472 | Example questions per subject and panel composition are in §3.6.1. |
| 98 | §3.2.1 | OK | Pretraining-coverage variance | 327 | aseline C5 > 3.0. Full distribution and band assignments in §3.2.1. |
| 100 | §3.5 | OK | Response models | 416 | tion. Tier 2 is a smaller cross-provider directional probe (§3.5, §4.6.1). The 7-judge panel spans three providers; the 5 no |
| 100 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | Tier 2 is a smaller cross-provider directional probe (§3.5, §4.6.1). The 7-judge panel spans three providers; the 5 non-Gemini |
| 100 | §3.6.3 | OK | Calibration | 525 | nd the 2 Gemini judges are reported as a sensitivity check (§3.6.3). |
| 108 | §1.4 | OK | What this implies | 136 | his is the population of importance for AI personalization (§1.4, §5.3): on a frontier model serving general AI users, almos |
| 108 | §5.3 | OK | Retrieval is not interpretation | 1533 | the population of importance for AI personalization (§1.4, §5.3): on a frontier model serving general AI users, almost ever |
| 112 | §4.1 | OK | The cross-subject gradient | 685 | questions improve.*[^statsig][^delta-aggregation] Detail in §4.1. |
| 113 | §4.1 | OK | The cross-subject gradient | 685 | spec conditions across the low-baseline subjects. Detail in §4.1. |
| 114 | §4.2 | OK | Compression: structure vs. raw text | 877 | x smaller context length (per-subject compression ratios in §4.2). The spec is not summarizing; it is selecting and structur |
| 114 | §4.2 | OK | Compression: structure vs. raw text | 877 | c actually beats the raw corpus (2.63 vs. 2.27).* Detail in §4.2. |
| 115 | §4.3 | OK | Mechanism: Content, Not Format | 996 | m-derangement Δ = +0.15; correct spec Δ = +0.35.* Detail in §4.3. |
| 116 | §4.4 | OK | Memory-system composition | 1123 | crossings range from 20% to 36% across systems.* Detail in §4.4. |
| 117 | §4.3 | OK | Mechanism: Content, Not Format | 996 | spec converts refusal into substantive response. Detail in §4.3. |
| 118 | §4.4.1 | OK | Aggregate performance across systems | 1131 | irwise overlap 8.3% across the ten system pairs.* Detail in §4.4.1. |
| 120 | §4.1 | OK | The cross-subject gradient | 685 | he same prediction quality, ~2.46 on the 1-5 rubric) are in §4.1. |
| 122 | §1.2 | OK | What we tested | 40 | C4a (per-subject grain is the locked unit of inference; see §1.2 aggregation rule). The grand-mean alternative (C4a grand me |
| 126 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | tterns of interaction with retrieval** (full development in §4.4.2). Baseline runs suggest the model already attempts shallow |
| 132 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | across providers; the spec direction reproduces. Detail in §4.6.1. |
| 134 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | not apply to the unified-brief specification. Case study in §4.5 / Appendix G. |
| 138 | §1.2 | OK | What we tested | 40 | ly it touches daily decisions. The population of relevance (§1.2) is anyone who uses or will use an AI system. Even the auto |
| 146 | §5 | OK | Discussion | 1505 | uire, especially as agents begin acting on people's behalf. §5 is an extended discussion of these implications; §7 develop |
| 146 | §7 | OK | Future Work | 1674 | behalf. §5 is an extended discussion of these implications; §7 develops the safety, alignment, and deployment implications |
| 152 | §2 | OK | Prior Work, Industry Benchmarks, The Fifth Target | 150 | soning situations as its operational test. The remainder of §2 walks the four existing targets, names the benchmarks attac |
| 178 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | on, which is one reason temporality is a flagged follow-up (§5.5, [§7](#7-future-work)). We state the assumption explicitly |
| 178 | §7 | OK | Future Work | 1674 | ch is one reason temporality is a flagged follow-up (§5.5, [§7](#7-future-work)). We state the assumption explicitly so th |
| 180 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | e above and adjacent to it, and sits alongside temporality (§5.5) as a follow-up in [§7](#7-future-work). |
| 180 | §7 | OK | Future Work | 1674 | t, and sits alongside temporality (§5.5) as a follow-up in [§7](#7-future-work). |
| 182 | §7 | OK | Future Work | 1674 | a prototype answer on that axis, not a finished benchmark. [§7](#7-future-work) flags a differentiated rubric (one that se |
| 207 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | t design is examined separately as a post-hoc case study in §4.5 (full case study in Appendix G), distinct from the archival |
| 207 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ing that our main-study configuration did not exercise (see §4.3 and §4.5). |
| 207 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | our main-study configuration did not exercise (see §4.3 and §4.5). |
| 211 | §4.4 | OK | Memory-system composition | 1123 | retrieval and interacts with it at the per-question level (§4.4), regardless of where each memory system lands on recall. |
| 258 | §4.2 | OK | Compression: structure vs. raw text | 877 | raw content it was derived from? The Hamerton condition in §4.2 (4,500-token spec vs. 33,000-token training corpus at 2.63 |
| 264 | §1.3 | OK | What we found | 104 | . This is why our experiment includes a wrong-spec control (§1.3 Mechanism): we hand the model a structured interpretive con |
| 264 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ), and content matters too (Base Layer's wrong-spec result, §4.3). |
| 266 | §1.3 | OK | What we found | 104 | it is willing to commit to. Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the gener |
| 266 | §4.3 | OK | Mechanism: Content, Not Format | 996 | o commit to. Our hedging-reduction finding (§1.3 Mechanism, §4.3) is consistent with this reading: the generic Assistant Axi |
| 270 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | as a sensitivity check. Full calibration methodology is in §3.6. |
| 274 | §4 | OK | Results | 669 | asurement choice ties back to a specific number reported in §4, and the statistical commitments were pre-locked before fin |
| 276 | §3.1 | OK | Operationalizing representational accuracy | 278 | §3.1 through §3.6 describe the experimental apparatus: the prope |
| 276 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | §3.1 through §3.6 describe the experimental apparatus: the property being mea |
| 276 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | nditions, the response models, and the evaluation protocol. §3.7 describes the pipeline that produces the Behavioral Specifi |
| 292 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | Pro) are reported as a sensitivity check. The rubric is in §3.6. A guide to interpreting fractional scores at different ran |
| 292 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | 9 vs. 3.2 indicates, what 1.5 vs. 2.0 indicates) is also in §3.6. |
| 315 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | for what the high-baseline end of the spectrum looks like (§4.6.4), not as a subject whose representation is a design target |
| 319 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | ne-rubric-pointer]: Rubric and aggregation rule defined in [§3.6](#36-evaluation-llm-as-judge-with-calibration). |
| 323 | §4 | OK | Results | 669 | e specification adds on top of the baseline is the question §4 tests. |
| 337 | §4.1 | OK | The cross-subject gradient | 685 | ive performance deltas when the specification is added (see §4.1 Table 4.1 and §4.6). Franklin at 3.77 (5-judge primary) anc |
| 337 | §4.6 | OK | Robustness and sensitivity | 1360 | tas when the specification is added (see §4.1 Table 4.1 and §4.6). Franklin at 3.77 (5-judge primary) anchors the high-basel |
| 339 | §4 | OK | Results | 669 | This distribution matters for reading §4's results: the variance is not flat, and the specification' |
| 339 | §4.1 | OK | The cross-subject gradient | 685 | ly affect representational accuracy rather than improve it. §4.1 develops this gradient explicitly. |
| 357 | §6 | OK | Limitations | 1601 | in the paper, and flags a broader limitation we carry into §6: automated backward-design batteries are not a substitute f |
| 359 | §3.3.1 | OK | Circularity controls | 361 | 5.4-regenerated batteries (used in the circularity control, §3.3.1) are at `results/global_<subject>/battery_gpt54.json`. The |
| 367 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | model are outside the Anthropic family. Full results are in §4.6.1. |
| 369 | §1.2 | OK | What we tested | 40 | wrong-specification control. Full condition definitions in §1.2. |
| 373 | §6 | OK | Limitations | 1601 | by these controls. It is discussed as an open limitation in §6.[^circularity-data] |
| 408 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | cess and is evaluated as a separate comparison, reported in §4.5 alongside other Letta findings rather than as a top-line co |
| 410 | §4.3 | OK | Mechanism: Content, Not Format | 996 | the wrong-spec effect by construction. Both are reported in §4.3, with v1 headlined for the stronger evidence of content eff |
| 410 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | tent effect; sensitivity analysis on the protocol choice in §4.6.4. We do not use a uniform Franklin-as-wrong-spec variant, wh |
| 418 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | the most conservative estimate of the spec's contribution; §4.6.1 Tier 2 cross-provider probe checks whether the direction ho |
| 420 | §3.3.1 | OK | Circularity controls | 361 | ol 1. Tier 2 results and subject-selection rationale are in §3.3.1 and §4.6.1. |
| 420 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | 2 results and subject-selection rationale are in §3.3.1 and §4.6.1. |
| 424 | §3.4 | OK | Experimental conditions | 377 | tion plus whichever context inputs the condition specifies (§3.4). Nothing about the prompt changes per condition beyond the |
| 438 | §4.3 | OK | Mechanism: Content, Not Format | 996 | c context is itself part of the phenomenon the study tests. §4.3 reports the hedging-rate shift across conditions and treats |
| 442 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | of forward behavior, and a unified brief synthesizing them (§3.7). The C2a vs C8 / C4 comparison is a direct test of whether |
| 454 | §3.6.1 | OK | Judge panel | 472 | ately recursive.** Response models are evaluated by judges (§3.6.1). Judges are evaluated by calibration diagnostics (§3.6.3), |
| 454 | §3.6.3 | OK | Calibration | 525 | (§3.6.1). Judges are evaluated by calibration diagnostics (§3.6.3), inter-judge agreement metrics (§3.6.4), and post-hoc rubr |
| 454 | §3.6.4 | OK | Inter-judge agreement | 559 | ration diagnostics (§3.6.3), inter-judge agreement metrics (§3.6.4), and post-hoc rubric-handling audits (§3.6.6). No single l |
| 454 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | ment metrics (§3.6.4), and post-hoc rubric-handling audits (§3.6.6). No single layer is treated as ground truth; each layer's |
| 466 | §3.4 | OK | Experimental conditions | 377 | fiers (C5, C2a, C4a, C3) refer to the conditions defined in §3.4 and summarized in Appendix C; rubric anchor numbers 1 throu |
| 466 | §4.1.1 | OK | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 | of when the no-context baseline engages versus abstains in [§4.1.1 Per-question baseline engagement and the worked rubric exam |
| 468 | §3.6.2 | OK | Score interpretation | 490 | ignment with the specific behavior in the held-out passage. §3.6.2 develops the formal cross-anchor rule used throughout the r |
| 488 | §3.6.3 | OK | Calibration | 525 | s is the directional question the panel is built to answer; §3.6.3 (calibration) and §3.6.4 (inter-judge agreement) measure ho |
| 488 | §3.6.4 | OK | Inter-judge agreement | 559 | tion the panel is built to answer; §3.6.3 (calibration) and §3.6.4 (inter-judge agreement) measure how reliably it does. |
| 515 | §4.2 | OK | Compression: structure vs. raw text | 877 | §4.2 reports the rate at which these crossings appear in each co |
| 517 | §4 | OK | Results | 669 | applies this rule consistently.** Score deltas reported in §4 are read through this lens. A +0.50 delta that crosses a ru |
| 521 | §4 | OK | Results | 669 | addition to the integer-band crossings reported throughout §4, an additional ~18% of paired questions across the 18 condi |
| 527 | §4 | OK | Results | 669 | ent only. The 5-judge primary aggregate reported throughout §4 is Haiku + GPT-4o + GPT-5.4 + Sonnet + Opus (the diagnostic |
| 551 | §4 | OK | Results | 669 | panel.** The primary numeric aggregate reported throughout [§4](#4-results) is the 5-judge mean using Haiku 4.5, Sonnet 4. |
| 553 | §4 | OK | Results | 669 | given and the delta is discussed. Every primary finding in §4 is stable across both aggregates (robustness confirmed in § |
| 553 | §4.6 | OK | Robustness and sensitivity | 1360 | 4 is stable across both aggregates (robustness confirmed in §4.6). |
| 557 | §4 | OK | Results | 669 | **How raw scores are read in §4.** Raw scores are treated as directional rather than absolu |
| 557 | §3.6.2 | OK | Score interpretation | 490 | ion than levels; deltas that cross a rubric integer anchor (§3.6.2) are treated as stronger claims than deltas staying inside |
| 567 | §5 | OK | Discussion | 1505 | on behavior. Full matrix in `docs/research/stats_update.md` §5. |
| 571 | §3.6.3 | OK | Calibration | 525 | ven when rankings match. This is why the calibration audit (§3.6.3) excluded the Gemini judges from the primary aggregate. |
| 591 | §4 | OK | Results | 669 | aced two rubric-handling limitations that any reader of the §4 numbers should keep in mind.[^validity-audit-script] |
| 627 | §7 | OK | Future Work | 1674 | r a modified rubric, to keep the analysis plan lock intact. §7 Future Work proposes a differentiated rubric that scores re |
| 629 | §6.2 | OK | Measurement apparatus | 1621 | on that this methodology cannot fully address is treated in §6.2.[^judgments-data] |
| 663 | §7.3 | OK | Specification design and composition | 1694 | isolating brief-with-layers vs. layers-only is flagged in [§7.3 Specification design and composition](#73-specification-des |
| 665 | §8 | OK | Data, code, and reproducibility | 1736 | study subjects are available in the public repository (see [§8 Data and code availability](#8-data-and-code-availability)) |
| 673 | §4 | OK | Results | 669 | The seven parts of §4 establish this picture in detail: |
| 675 | §4.1 | OK | The cross-subject gradient | 685 | - **§4.1. The cross-subject gradient.** The primary result, across 1 |
| 676 | §4.2 | OK | Compression: structure vs. raw text | 877 | - **§4.2. Compression: structure vs. raw text.** Is the effect about |
| 677 | §4.3 | OK | Mechanism: Content, Not Format | 996 | - **§4.3. Mechanism: Content, Not Format.** Does the content of the |
| 678 | §4.4 | OK | Memory-system composition | 1123 | - **§4.4. Memory-system composition.** Does the specification layer |
| 678 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | tems? Where does it help or hurt at the per-question level (§4.4.2 common mechanisms, §4.4.3 cross-system Keckley case)? |
| 678 | §4.4.3 | OK | Case study: cross-system refusal on Keckley Q21 | 1289 | r hurt at the per-question level (§4.4.2 common mechanisms, §4.4.3 cross-system Keckley case)? |
| 679 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | - **§4.5. Exploratory case study (Letta stateful-agent).** Brief sum |
| 680 | §4.6 | OK | Robustness and sensitivity | 1360 | - **§4.6. Robustness and sensitivity.** Cross-provider response gene |
| 680 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | ne end of the gradient through the Franklin reference is in §4.1.2.) |
| 681 | §4.7 | OK | Summary of §4 and bridge to discussion | 1482 | - **§4.7. Summary and bridge to discussion.** A one-paragraph synthe |
| 681 | §4 | OK | Results | 669 | d bridge to discussion.** A one-paragraph synthesis of what §4 established, framing the transition into §5. |
| 681 | §5 | OK | Discussion | 1505 | nthesis of what §4 established, framing the transition into §5. |
| 683 | §4 | OK | Results | 669 | Every number in §4 uses the 5-judge primary aggregate defined in §3.6.3 (Haiku |
| 683 | §3.6.3 | OK | Calibration | 525 | number in §4 uses the 5-judge primary aggregate defined in §3.6.3 (Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4). The 7-j |
| 683 | §4.6 | OK | Robustness and sensitivity | 1360 | (adding Gemini 2.5 Flash and Gemini 2.5 Pro) is reported in §4.6. Score deltas are read through the anchor-crossing rule fro |
| 683 | §3.6.2 | OK | Score interpretation | 490 | Score deltas are read through the anchor-crossing rule from §3.6.2: a delta that crosses a rubric integer anchor is a stronger |
| 687 | §1.2 | OK | What we tested | 40 | **Hypotheses tested in this section** (from §1.2): H1. Adding the specification improves prediction. H2. The |
| 691 | §3.2.1 | OK | Pretraining-coverage variance | 327 | low 2.0 on the 1-5 rubric (the population of relevance from §3.2.1), adding the specification consistently improves prediction |
| 691 | §4.2 | OK | Compression: structure vs. raw text | 877 | ller in magnitude than the spec-vs-baseline lift (detail in §4.2 and §4.4). Spec alone does not outperform facts alone or ra |
| 691 | §4.4 | OK | Memory-system composition | 1123 | agnitude than the spec-vs-baseline lift (detail in §4.2 and §4.4). Spec alone does not outperform facts alone or raw corpus |
| 699 | §5.3 | OK | Retrieval is not interpretation | 1533 | ing corpus sit at or near the rubric floor by construction (§5.3), and they are the subjects for whom the lift is largest an |
| 703 | §1.4 | OK | What this implies | 136 | hich is the population of relevance for AI personalization (§1.4, §5.3). |
| 703 | §5.3 | OK | Retrieval is not interpretation | 1533 | s the population of relevance for AI personalization (§1.4, §5.3). |
| 717 | §3.6.2 | OK | Score interpretation | 490 | hese transitions appear below (Examples A through D) and in §3.6.2 (multi-anchor crossings) and §4.1.1 (Seacole Q2 across cond |
| 717 | §4.1.1 | OK | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 | les A through D) and in §3.6.2 (multi-anchor crossings) and §4.1.1 (Seacole Q2 across condition bands). |
| 761 | §4.4.3 | OK | Case study: cross-system refusal on Keckley Q21 | 1289 | ons where the spec appropriately declined to invent detail (§4.4.3's Keckley Q21). The rubric does not cleanly distinguish abs |
| 761 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | s not cleanly distinguish abstention from wrong prediction (§3.6.6); a differentiated rubric is flagged in §7. |
| 761 | §7 | OK | Future Work | 1674 | prediction (§3.6.6); a differentiated rubric is flagged in §7. |
| 767 | §3.6.4 | OK | Inter-judge agreement | 559 | ] **Pairwise Spearman ρ** across the 5-judge primary panel (§3.6.4) confirms that the lift's direction is consistent across ju |
| 803 | §4.2 | OK | Compression: structure vs. raw text | 877 | only) was run on the 9 low-baseline subjects as part of the §4.2 compression analysis; mid-baseline subjects and Franklin we |
| 813 | §4.6.3 | OK | Battery composition sensitivity | 1406 | n and Hamerton-leverage subset regression) are addressed in §4.6.3 as robustness checks; both leave the baseline gradient effe |
| 815 | §4.1.1 | OK | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 | comparisons such as C4 → C4a) and minimal change on others. §4.1.1 decomposes this distribution and shows where the spec's val |
| 823 | §4.1 | OK | The cross-subject gradient | 685 | es.[^bimodal-stats] This is the per-question shape that the §4.1 gradient summarizes at the subject level. |
| 845 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | \| Band \| Definition (from §3.6) \| |
| 861 | §3.6.2 | OK | Score interpretation | 490 | he example traces the *cross-anchor interpretation rule* of §3.6.2 on a single question. C5 declines for lack of referent; C2c |
| 861 | §4.1 | OK | The cross-subject gradient | 685 | and 5 on a single question is what the per-subject means in §4.1 aggregate. |
| 863 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | abstention at roughly twice Haiku's rate) is decomposed in §3.6.6; memory-system retrieval inflates refusal scores at the con |
| 863 | §4.4 | OK | Memory-system composition | 1123 | evel rather than via visible fact recitation, decomposed in §4.4; further limitations on the abstention reading (REFUSE-bin |
| 863 | §6.2 | OK | Measurement apparatus | 1621 | ntion* with *spec corrects confident error*) are flagged in §6.2. |
| 879 | §1.2 | OK | What we tested | 40 | **Hypothesis tested in this section** (H5 from §1.2): A compact specification achieves comparable behavioral-pr |
| 932 | §3.6.2 | OK | Score interpretation | 490 | iformly small effects. *Multi-anchor crossings* (defined in §3.6.2) occur much more often when context is added to a no-contex |
| 945 | §1 | OK | Introduction | 11 | ands on roughly 1 in 45. The pattern is consistent with the §1 thesis: the specification produces the most categorical mov |
| 947 | §3.4 | OK | Experimental conditions | 377 | natural language; cross-reference to condition codes is in §3.4 and Appendix C. The 9-subject low-baseline slice gives some |
| 947 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | gregate Δ on the spec-on-info-rich pairs, are decomposed in §4.4.2 alongside memory-system layering. Multi-anchor examples: Ha |
| 970 | §4.2.1 | OK | Per-question improvement rate | 949 | points, so the metric guards against tiny-gain inflation. (§4.2.1).](../figures/fig_4_2_1_question_improvement_rates_v3.png) |
| 998 | §1.2 | OK | What we tested | 40 | **Hypothesis tested in this section** (H3 from §1.2): The benefit comes from the content of the correct specifi |
| 1018 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | l, and the adversarial-vs-random pairing sensitivity are in §4.6.4. |
| 1040 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | ws about the named subject — specifications are anonymized (§3.7), so the model has no surface name cue to compare against; |
| 1044 | §1.3 | OK | What we found | 104 | under the broader-pattern classifier (rule definitions in [§1.3](#13-the-core-finding) footnote). On wrong-spec, refusal pa |
| 1050 | §4.1 | OK | The cross-subject gradient | 685 | The three §4.1 examples extend directly into mechanism-by-mechanism wrong- |
| 1050 | §4.1 | OK | The cross-subject gradient | 685 | he specification content. Correct-spec C4a responses are in §4.1 for reference. |
| 1054 | §4.1 | OK | The cross-subject gradient | 685 | > **Subject + question:** same as §4.1 Example A (Ebers, self-sacrifice and educational institutio |
| 1065 | §4.1 | OK | The cross-subject gradient | 685 | biguation mechanism that enabled the correct spec's lift in §4.1 Example A did not fire because the spec content is not abou |
| 1069 | §4.1 | OK | The cross-subject gradient | 685 | > **Subject + question:** same as §4.1 Example B (Bernal Diaz, Cortes and offered physical assista |
| 1090 | §4.1 | OK | The cross-subject gradient | 685 | > **Subject + question:** same as §4.1 Example C (Seacole, delirious patient). Battery-question ta |
| 1105 | §4.1 | OK | The cross-subject gradient | 685 | content. The interpretive-inference mechanism that produced §4.1 Example C's correct-spec 5.00 score does not fire: without |
| 1125 | §1.2 | OK | What we tested | 40 | **Hypothesis tested in this section** (H4 from §1.2): The Behavioral Specification interacts with memory-system |
| 1127 | §4.4.1 | OK | Aggregate performance across systems | 1131 | **Surfaced finding (not pre-registered).** §4.4.1 also reports a finding that did not feature in our pre-regi |
| 1127 | §4.4.1 | OK | Aggregate performance across systems | 1131 | ch facts matter for a specific interpretive task. Detail in §4.4.1; meta-analysis follow-ups in §7.1. |
| 1127 | §7.1 | OK | Measurement methodology | 1678 | pretive task. Detail in §4.4.1; meta-analysis follow-ups in §7.1. |
| 1133 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | balance of per-question patterns; that decomposition is in §4.4.2 (where Supermemory's near-zero aggregate Δ is also unpacked |
| 1137 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | rally unlike a retrieval path and is reported separately in §4.5. |
| 1162 | §4.3 | OK | Mechanism: Content, Not Format | 996 | e cleanly across systems; the content-specific reading from §4.3 holds. |
| 1164 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | tion varies by system. The mechanism for these splits is in §4.4.2: the spec helps retrieval-based systems on interpretation-h |
| 1166 | §1.2 | OK | What we tested | 40 | tem retrieval overlap: providers do not converge.** For the §1.2 convergence question, the controlled answer is no: the prov |
| 1188 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | This ties to the §4.4.2 patterns. The three downstream patterns that distinguish me |
| 1190 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | also leaves the divergence intact; full sensitivity grid in §4.6.5. |
| 1202 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | not distinguish principled refusal from a wrong prediction (§3.6.6). *Lowers the measured rubric score; whether it lowers actu |
| 1265 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | incipled-sounding refusal identically to an off-base guess (§3.6.6). |
| 1267 | §4.4.3 | OK | Case study: cross-system refusal on Keckley Q21 | 1289 | ditional moment. The Keckley Q21 cross-system case study in §4.4.3 is the cleanest demonstration that Pattern 3 only registers |
| 1279 | §7 | OK | Future Work | 1674 | lassification per response and is flagged as future work in §7. |
| 1283 | §7 | OK | Future Work | 1674 | scores epistemic honesty as its own dimension is flagged in §7. |
| 1285 | §7.4 | OK | Production serving and infrastructure | 1700 | ion subsets is flagged as production-serving future work in §7.4. |
| 1313 | §7 | OK | Future Work | 1674 | on. This is the priority rubric-design follow-up flagged in §7. |
| 1315 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | subject reasons. On Keckley Q21 (and Pattern 3 examples in §4.4.2), the specification produces a response that captures the s |
| 1342 | §4.4 | OK | Memory-system composition | 1123 | The four commercial systems analyzed in §4.4 all share a retrieval-based architecture: facts are chunked |
| 1342 | §4.4 | OK | Memory-system composition | 1123 | eparate from the archival retrieval path evaluated above in §4.4, in which the agent writes and revises a persistent memory |
| 1342 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | uring ingestion rather than returning chunks at query time. §4.5 evaluates that path directly, to test whether an architectu |
| 1356 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ointers are in **Appendix G**. The methodological note: the §4.5 main result table compares Letta's named, self-edited block |
| 1356 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | are documented in Appendix G and flagged as future work in §7.5. |
| 1362 | §4.1 | OK | The cross-subject gradient | 685 | The results in §4.1 through §4.4 could in principle reflect artifacts of the me |
| 1362 | §4.4 | OK | Memory-system composition | 1123 | The results in §4.1 through §4.4 could in principle reflect artifacts of the measurement app |
| 1362 | §4.6 | OK | Robustness and sensitivity | 1360 | ather than real properties of the Behavioral Specification. §4.6 reports five sensitivity checks: cross-provider response ge |
| 1362 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | different model family and a different question generator (§4.6.1), the judge panel composition between the conservative 5-ju |
| 1362 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | ge sensitivity panel that adds Gemini Flash and Gemini Pro (§4.6.2), battery composition by question type (§4.6.3), the wrong- |
| 1362 | §4.6.3 | OK | Battery composition sensitivity | 1406 | Gemini Pro (§4.6.2), battery composition by question type (§4.6.3), the wrong-spec derangement protocol comparing adversarial |
| 1362 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | ent protocol comparing adversarial against random pairings (§4.6.4), and semantic-similarity sensitivity on the retrieval-over |
| 1362 | §4.4.1 | OK | Aggregate performance across systems | 1131 | imilarity sensitivity on the retrieval-overlap finding from §4.4.1 (§4.6.5). §4.6.6 names what these checks do not address. (T |
| 1362 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | y sensitivity on the retrieval-overlap finding from §4.4.1 (§4.6.5). §4.6.6 names what these checks do not address. (The high- |
| 1362 | §4.6.6 | OK | What these robustness checks do not address | 1474 | vity on the retrieval-overlap finding from §4.4.1 (§4.6.5). §4.6.6 names what these checks do not address. (The high-baseline |
| 1362 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | f the gradient through the Franklin reference is treated in §4.1.2 as part of the gradient finding, not as an apparatus check. |
| 1370 | §3.3 | OK | Question Battery Formation | 341 | tudy batteries were generated by Claude Haiku 4.5 using the §3.3 backward-design prompt (verified from the `metadata.model` |
| 1370 | §4.1 | OK | The cross-subject gradient | 685 | re the specification did not measurably improve prediction (§4.1 gradient table; Equiano is the other), so the Tier 2 result |
| 1372 | §3.3.1 | OK | Circularity controls | 361 | out corpus, following the Control 1 procedure introduced in §3.3.1. The specification was then served to two non-Haiku respons |
| 1384 | §7 | OK | Future Work | 1674 | families and direction outside this subset are future work (§7). |
| 1386 | §1.4 | OK | What this implies | 136 | on. This is empirical support for the structural premise in §1.4: pretraining coverage of a specific person is a property of |
| 1402 | §3.6.3 | OK | Calibration | 525 | judges. Gemini 2.5 Pro failed verbatim-match calibration in §3.6.3 (scored 4.15 where every other calibrated judge scored 5.00 |
| 1402 | §4.1 | OK | The cross-subject gradient | 685 | comparable to the calibrated core. Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as p |
| 1402 | §4.4 | OK | Memory-system composition | 1123 | the calibrated core. Every primary finding in §4.1 through §4.4 was checked against the 7-judge aggregate as part of the an |
| 1408 | §4.1 | OK | The cross-subject gradient | 685 | **Result.** The gradient slope from §4.1 survives both confounds tested. Neither battery-question-ty |
| 1412 | §3.3 | OK | Question Battery Formation | 341 | version of the backward-design protocol, distinct from the §3.3 protocol used to generate the 13 globals' batteries, which |
| 1422 | §4.3 | OK | Mechanism: Content, Not Format | 996 | incidental content alignment with the target's pattern; see §4.3 Example B for a worked overlap case). |
| 1424 | §1.2 | OK | What we tested | 40 | angement-detail]: Derangement protocol mechanics defined in §1.2 (conditions table footnote) and §3.4. v1 is a deterministic |
| 1424 | §3.4 | OK | Experimental conditions | 377 | l mechanics defined in §1.2 (conditions table footnote) and §3.4. v1 is a deterministic fixed pairing maximizing cultural an |
| 1445 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ct's pattern, not a structural property of mismatch itself; §4.3 Example B (Bernal Diaz Q16) walks through one such case in |
| 1449 | §4.3 | OK | Mechanism: Content, Not Format | 996 | te separation, per-predicate ablation null) is developed in §4.3 and not rebuilt here. |
| 1451 | §7 | OK | Future Work | 1674 | These questions are not answered by this study; flagged in §7. |
| 1457 | §4.4.1 | OK | Aggregate performance across systems | 1131 | dentity to semantic-similarity matching does not change the §4.4.1 retrieval-divergence finding. Across 240 (config × pair × K |
| 1468 | §4.4.1 | OK | Aggregate performance across systems | 1131 | **What this establishes.** The §4.4.1 retrieval-divergence finding survives under semantic-simila |
| 1468 | §7.1 | OK | Measurement methodology | 1678 | lling each system at higher K) is flagged as future work in §7.1.[^retrieval-overlap-semantic] |
| 1476 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | the effect smaller, not larger. The wrong-spec sensitivity (§4.6.4) brackets the content-vs-template question from two protoco |
| 1476 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | s the active ingredient. The retrieval-overlap sensitivity (§4.6.5) confirms the §4.4.1 divergence finding under semantic-simi |
| 1476 | §4.4.1 | OK | Aggregate performance across systems | 1131 | nt. The retrieval-overlap sensitivity (§4.6.5) confirms the §4.4.1 divergence finding under semantic-similarity matching but d |
| 1476 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | oes not test convergence at K > 10. The Franklin reference (§4.1.2) shows the gradient holds at the high-baseline end on one s |
| 1476 | §6.2 | OK | Measurement apparatus | 1621 | n and the human-validation follow-up are treated in full in §6.2.[^tier2-raw-data] |
| 1478 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | `FULL_FAIL` cells that drive the 4-judge effective panel in §4.6.1) at `docs/research/v11_panel_completeness_audit.csv`. Mecha |
| 1482 | §4 | OK | Results | 669 | ### 4.7 Summary of §4 and bridge to discussion |
| 1484 | §4 | OK | Results | 669 | §4 established four findings: |
| 1486 | §4.1 | OK | The cross-subject gradient | 685 | - **The gradient (§4.1, §4.1.2).** The specification produces a roughly uniform po |
| 1486 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | - **The gradient (§4.1, §4.1.2).** The specification produces a roughly uniform post-spec |
| 1487 | §4.2 | OK | Compression: structure vs. raw text | 877 | - **Compression (§4.2).** The structured representation compresses the predictive |
| 1488 | §4.3 | OK | Mechanism: Content, Not Format | 996 | - **Content specificity (§4.3).** The effect is content-specific rather than structural; |
| 1489 | §4.4 | OK | Memory-system composition | 1123 | - **Memory-system interaction (§4.4).** The specification interacts with memory-system retrieva |
| 1490 | §4.4.1 | OK | Aggregate performance across systems | 1131 | - **Retrieval divergence (§4.4.1, surfaced post-hoc).** Given an identical fact pool, the fo |
| 1494 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | - **Cross-provider response generation (§4.6.1).** Direction reproduces on Sonnet 4.6 and Gemini 2.5 Pro a |
| 1495 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | - **Judge panel (§4.6.2).** No directional claim flips between the conservative 5-j |
| 1496 | §4.6.3 | OK | Battery composition sensitivity | 1406 | - **Battery composition (§4.6.3).** Neither battery-question-type composition nor Hamerton' |
| 1496 | §4.1 | OK | The cross-subject gradient | 685 | -type composition nor Hamerton's leverage explains away the §4.1 gradient slope. |
| 1497 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | - **Wrong-spec derangement protocol (§4.6.4).** The wrong-spec result holds across both protocols teste |
| 1498 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | - **Retrieval-overlap sensitivity (§4.6.5).** The §4.4.1 retrieval-divergence finding survives semant |
| 1498 | §4.4.1 | OK | Aggregate performance across systems | 1131 | - **Retrieval-overlap sensitivity (§4.6.5).** The §4.4.1 retrieval-divergence finding survives semantic-similarity m |
| 1499 | §4.6.6 | OK | What these robustness checks do not address | 1474 | - **What these checks do not address (§4.6.6).** The class-level LLM-as-judge concern remains and is tre |
| 1499 | §6.2 | OK | Measurement apparatus | 1621 | class-level LLM-as-judge concern remains and is treated in §6.2. |
| 1501 | §5 | OK | Discussion | 1505 | §5 develops what these results imply for AI personalization be |
| 1501 | §6 | OK | Limitations | 1601 | for AI personalization beyond the specific experiment, and §6 bounds what the experiment cannot establish. |
| 1507 | §4 | OK | Results | 669 | §4 produced the empirical results; this section discusses thei |
| 1515 | §7 | OK | Future Work | 1674 | man-validation follow-up is the highest-priority next step (§7). Robustness checks against cross-provider response models, |
| 1515 | §4.6 | OK | Robustness and sensitivity | 1360 | odels, judge-panel composition, and protocol choices are in §4.6. |
| 1517 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | fic person reasons. Full pipeline and operational detail in §3.7. |
| 1529 | §4.1 | OK | The cross-subject gradient | 685 | ment-heterogeneity readings were considered and rejected in §4.1 on this basis. |
| 1539 | §5.4 | OK | Composition with retrieval | 1543 | puts. Behavioral alignment requires the deeper calibration. §5.4 picks up what happens when the interpretive layer is compos |
| 1545 | §5.3 | OK | Retrieval is not interpretation | 1533 | The implication of §5.3 is not that retrieval is unnecessary, but that retrieval an |
| 1545 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | ive layer's calibration signal needs to be conditional. The §4.4.2 three composition patterns[^composition-patterns] argue aga |
| 1547 | §4.4.3 | OK | Case study: cross-system refusal on Keckley Q21 | 1289 | eorization, and principled refusal. The Keckley Q21 case in §4.4.3 walks through the third. |
| 1553 | §7.4 | OK | Production serving and infrastructure | 1700 | tectural answer requires beginning to draw the distinction. §7.4 develops dynamic serving as a production-architecture follo |
| 1559 | §4.3 | OK | Mechanism: Content, Not Format | 996 | The wrong-spec controls in §4.3 establish that the matched layer's content does the work, n |
| 1559 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | d content makes the model worse than no context at all. The §4.6.4 sensitivity check confirms the finding holds across both de |
| 1561 | §2.4 | OK | Cognitive and representational foundations | 252 | les out the simplest sycophancy reading: Jain et al. (2025; §2.4) showed that context without the right structure pushes mod |
| 1563 | §4.3 | OK | Mechanism: Content, Not Format | 996 | The Bernal Diaz Q16 case from §4.3 (Example B) shows that some behavioral patterns transfer ac |
| 1563 | §5.3 | OK | Retrieval is not interpretation | 1533 | onvergence at the interpretive layer is informative against §5.3's retrieval-divergence finding. Providers do not converge o |
| 1563 | §7 | OK | Future Work | 1674 | ontrolled component ablation is flagged as the next test in §7. |
| 1565 | §5.6 | OK | Compression and what makes personalization operationally tractable | 1569 | n how it can be compressed to fit production-scale serving (§5.6) and who holds and inspects it (§5.7) become the structural |
| 1565 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | duction-scale serving (§5.6) and who holds and inspects it (§5.7) become the structural questions. |
| 1571 | §4.2 | OK | Compression: structure vs. raw text | 877 | its source corpus recovers most of the predictive accuracy (§4.2) is the property that makes per-user personalization feasib |
| 1573 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ompression is the open question. The wrong-spec controls in §4.3 partially address it: derangements and adversarial mismatch |
| 1581 | §1.4 | OK | What this implies | 136 | The inspectability requirement of §1.4 is also an argument about privacy and ownership. Behavioral |
| 1583 | §3 | OK | Study Design | 272 | is incremental but growing. As the operations described in §3 become cheaper and more capable, the asymmetry between what |
| 1585 | §1.4 | OK | What this implies | 136 | A specific risk frames the inspectability claim from §1.4. A spec built from publicly available data alone may not ca |
| 1585 | §4.3 | OK | Mechanism: Content, Not Format | 996 | n drive the spec into the adversarial regime established in §4.3. Inspectability and modifiability allow the person to detec |
| 1587 | §7 | OK | Future Work | 1674 | one else is a structural choice the field has not yet made. §7 develops the safety and deployment implications. |
| 1597 | §7 | OK | Future Work | 1674 | ation, and generalization beyond this protocol remain open. §7 develops the implications for safety, alignment, and deploy |
| 1603 | §6.1 | OK | Subject sample | 1605 | f constraint on the experimental setup: the subject sample (§6.1), the measurement apparatus (§6.2), the pipeline and specif |
| 1603 | §6.2 | OK | Measurement apparatus | 1621 | etup: the subject sample (§6.1), the measurement apparatus (§6.2), the pipeline and specification stability (§6.3), and the |
| 1603 | §6.3 | OK | Pipeline and specification stability | 1635 | apparatus (§6.2), the pipeline and specification stability (§6.3), and the scope of exploration (§6.4). Each is a permanent |
| 1603 | §6.4 | OK | Scope of exploration | 1662 | ecification stability (§6.3), and the scope of exploration (§6.4). Each is a permanent caveat on how the paper's results sho |
| 1603 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | ad, distinct from the open research questions catalogued in §5.7 and the follow-up experiments proposed in §7. |
| 1603 | §7 | OK | Future Work | 1674 | atalogued in §5.7 and the follow-up experiments proposed in §7. |
| 1607 | §5.3 | OK | Retrieval is not interpretation | 1533 | e load-bearing for the paper's framing and are developed in §5.3; this subsection covers four remaining external-validity ca |
| 1607 | §5 | OK | Discussion | 1505 | ection covers four remaining external-validity caveats that §5 does not address. |
| 1623 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | per's numbers should be read. The rubric limitations are in §5.7; the LLM-as-judge limitation is the canonical one and is tr |
| 1625 | §3.3 | OK | Question Battery Formation | 341 | an LLM, and the question batteries are also LLM-generated (§3.3). The 5-judge primary panel and the 7-judge sensitivity che |
| 1625 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | itivity check together address within-provider circularity (§4.6.1, §4.6.2): the specification effect reproduces when non-Anth |
| 1625 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | check together address within-provider circularity (§4.6.1, §4.6.2): the specification effect reproduces when non-Anthropic re |
| 1625 | §7.1 | OK | Measurement methodology | 1678 | tion subset is the leading measurement follow-up flagged in §7.1; until that exists, the paper's claims should be read as di |
| 1627 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | e.** The main-study response model is Claude Haiku 4.5. The §4.6.1 Tier 2 cross-provider directional probe ran 2 additional re |
| 1627 | §4.1 | OK | The cross-subject gradient | 685 | ain-study response model is Haiku across all 14 subjects in §4.1; Tier 2 establishes direction across response-model familie |
| 1631 | §3.6.4 | OK | Inter-judge agreement | 559 | iance.** Pairwise Spearman ρ across judges is 0.86 to 0.93 (§3.6.4), so the rank order of conditions is stable across the pane |
| 1631 | §3.6.3 | OK | Calibration | 525 | stable across the panel. Absolute-score calibration varies (§3.6.3): Gemini Pro fails verbatim-match calibration (4.15 where c |
| 1631 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | eserving the direction of every claim, which is part of why §5.7 frames the paper as directional rather than precise. |
| 1637 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | hment versus production-realistic dynamic activation) is in §5.5 and §5.7. What follows covers pipeline-internal constraints |
| 1637 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | sus production-realistic dynamic activation) is in §5.5 and §5.7. What follows covers pipeline-internal constraints on how t |
| 1643 | §4.1 | OK | The cross-subject gradient | 685 | is reported below, alongside the cross-subject SD that the §4.1 gradient slope is fit to. |
| 1645 | §4.1 | OK | The cross-subject gradient | 685 | \| Subject \| Canonical Δ_C4a (§4.1) \| Per-rerun Δ_C4a SD (n=3) \| % of cross-subject SD \| |
| 1652 | §4.1 | OK | The cross-subject gradient | 685 | er-subject point estimate. The per-subject Δ_C4a numbers in §4.1 should be read with a soft uncertainty bar of roughly ±0.10 |
| 1654 | §4.1 | OK | The cross-subject gradient | 685 | enough relative to the cross-subject SD that we accept the §4.1 slope and R² as findings about the gradient rather than art |
| 1658 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | for layer authoring, and Claude Opus for the compose step (§3.7). These model choices were not varied across the study. Dif |
| 1658 | §7 | OK | Future Work | 1674 | nthropic authoring model), is a direct follow-up flagged in §7. |
| 1664 | §4.1 | OK | The cross-subject gradient | 685 | tizes the conditions and subjects central to H1 through H5 (§4.1 through §4.4). Robustness and ablation conditions were adde |
| 1664 | §4.4 | OK | Memory-system composition | 1123 | ditions and subjects central to H1 through H5 (§4.1 through §4.4). Robustness and ablation conditions were added selectively |
| 1666 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | itional response models (Sonnet 4.6, Gemini 2.5 Pro) in the §4.6.1 Tier 2 cross-provider directional probe on 3 subjects. The |
| 1668 | §4.4 | OK | Memory-system composition | 1123 | ival retrieval path the other three commercial systems use (§4.4, §4.5). Testing the stateful path required a different eval |
| 1668 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | etrieval path the other three commercial systems use (§4.4, §4.5). Testing the stateful path required a different evaluation |
| 1668 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | the stateful path required a different evaluation harness (§4.5 test design), and that work pulled us partially outside the |
| 1668 | §7 | OK | Future Work | 1674 | against future Letta releases is flagged as a follow-up in §7. |
| 1670 | §2.1 | OK | Memory and personalization benchmarks | 158 | 2K is prior work, not a condition of this study.** Twin-2K (§2.1) appears in this paper as prior work that measures a relate |
| 1680 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | uestions and scores epistemic honesty as its own dimension (§3.6.6, §5.7). Alongside this: a curated question set with explici |
| 1680 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | and scores epistemic honesty as its own dimension (§3.6.6, §5.7). Alongside this: a curated question set with explicit qual |
| 1680 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | th explicit quality control on the backward-design process (§5.7), a human-validated subset of rubric applications to test w |
| 1680 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | est whether the rubric was reasonably applied per-response (§5.7), and human-judge validation on a stratified subset of resp |
| 1680 | §4.6.3 | OK | Battery composition sensitivity | 1406 | responses to address class-level LLM-as-judge circularity (§4.6.3, §5.7). Prompt-sensitivity testing across the authoring, re |
| 1680 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | es to address class-level LLM-as-judge circularity (§4.6.3, §5.7). Prompt-sensitivity testing across the authoring, response |
| 1680 | §6.2 | OK | Measurement apparatus | 1621 | oss the authoring, response-generation, and judging stages (§6.2) is a separate measurement-stability follow-up that becomes |
| 1682 | §4.4.1 | OK | Aggregate performance across systems | 1131 | **Retrieval-overlap follow-ups (from the surfaced §4.4.1 finding).** Two measurement studies remain open after the § |
| 1682 | §4.4.1 | OK | Aggregate performance across systems | 1131 | 1 finding).** Two measurement studies remain open after the §4.4.1 sensitivity check that already covers K=5 and semantic-simi |
| 1684 | §4.4.1 | OK | Aggregate performance across systems | 1131 | ly 1-2 of an average union of 17 facts (mean Jaccard 0.083, §4.4.1). The K=5 truncation tested in §4.4.1 lowers overlap rather |
| 1684 | §4.4.1 | OK | Aggregate performance across systems | 1131 | (mean Jaccard 0.083, §4.4.1). The K=5 truncation tested in §4.4.1 lowers overlap rather than raising it. Whether convergence |
| 1686 | §4.4.1 | OK | Aggregate performance across systems | 1131 | facts when given identical fact pools and fixed questions (§4.4.1). Recall benchmarks measure recall, which is what they shou |
| 1686 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | terpretive task. The wrong-spec per-question meta-analysis (§4.6.4) belongs to the same class of follow-up: a deeper read of w |
| 1690 | §5.3 | OK | Retrieval is not interpretation | 1533 | replication is the leading follow-up for the entire paper (§5.3, §5.7). The paper's findings depend structurally on an extr |
| 1690 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | cation is the leading follow-up for the entire paper (§5.3, §5.7). The paper's findings depend structurally on an extrapolat |
| 1690 | §6.1 | OK | Subject sample | 1605 | mporary writing rather than pre-20th-century autobiography, §6.1), non-English original sources (to remove translation artif |
| 1690 | §6.1 | OK | Subject sample | 1605 | -English original sources (to remove translation artifacts, §6.1), and alternative testbeds that isolate reasoning structure |
| 1690 | §5.3 | OK | Retrieval is not interpretation | 1533 | l interpretive patterns that can be held out and predicted (§5.3). |
| 1692 | §4 | OK | Results | 669 | mall (n=4 vs 10) and the result is not load-bearing for any §4 claim, but the direction suggests the authoring pipeline ma |
| 1696 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | tions, brief) is the priority authoring-pipeline follow-up (§5.5, §5.4, §5.7). Serving each layer alone and in combinations, |
| 1696 | §5.4 | OK | Composition with retrieval | 1543 | brief) is the priority authoring-pipeline follow-up (§5.5, §5.4, §5.7). Serving each layer alone and in combinations, measu |
| 1696 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | ) is the priority authoring-pipeline follow-up (§5.5, §5.4, §5.7). Serving each layer alone and in combinations, measuring P |
| 1698 | §6.3 | OK | Pipeline and specification stability | 1635 | sensitivity to specific LLM choices at each pipeline step (§6.3); a Base Layer referent-variant that retains named entities |
| 1698 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | nside the same dimensional scaffold, to isolate whether the §4.5 Letta-over-Base-Layer gap is driven by referential vocabula |
| 1698 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ferential vocabulary or by the self-editing process itself (§4.5, §5.5); and a layered-stack Letta rerun on the matched-reru |
| 1698 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | ial vocabulary or by the self-editing process itself (§4.5, §5.5); and a layered-stack Letta rerun on the matched-rerun subj |
| 1698 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | n the matched-rerun subjects, which would likely narrow the §4.5 gap (§4.5, §5.7). |
| 1698 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | hed-rerun subjects, which would likely narrow the §4.5 gap (§4.5, §5.7). |
| 1698 | §5.7 | OK | Privacy and the case for user-held representation | 1579 | run subjects, which would likely narrow the §4.5 gap (§4.5, §5.7). |
| 1702 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | These five items appear in §5.5 as deployment design considerations; this section flags whi |
| 1702 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | ion-realistic serving-layer follow-ups follow directly from §5.5: dynamic activation, modifiability affordances, temporality |
| 1702 | §2.1 | OK | Memory and personalization benchmarks | 158 | y affordances, temporality handling, canonical life events (§2.1), and topic decomposition (see §5.5 for the description of |
| 1702 | §5.5 | OK | Wrong-spec mechanism and hedging elimination | 1557 | canonical life events (§2.1), and topic decomposition (see §5.5 for the description of each). Each is a measurement questio |
| 1708 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ry with provenance across edits is a natural next step. The §4.5 Letta exploration (N=3, post-hoc) is one data point on an a |
| 1708 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | comparison within a single architectural family and extend §4.5 to a layered-stack rerun against Letta at full scope. |
| 1710 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | **Cleaner §4.5 rerun with naming and scaling controls.** Two specific exte |
| 1710 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ming and scaling controls.** Two specific extensions of the §4.5 exploration are worth running as a unit. First, anonymize t |
| 1710 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ng Base Layer's anonymized-during-authoring convention; the §4.5 naming asymmetry (Letta ingests named corpus, Base Layer st |
| 1710 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | owing trend between Letta and Base Layer observed at Babur (§4.5 caveats, full-stack rerun) continues, inverts, or stalls as |
| 1710 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | easing verbatim-duplication rates. Both together would turn §4.5's case study into a controlled comparison. |
| 1714 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | 10-year baseline on anchor Y") as a first-class output. The §4.5 exploration and the SCOTUS-style sequential-checkpoint desi |
| 1718 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | ectory is interpretable and the per-update cost matches the §3.7 pipeline cost. Two design questions matter. First, drift an |
| 1726 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ps follow from this. First, the spec-induced refusal cases (§4.3, §4.6.3) showed the response model declining to speculate a |
| 1726 | §4.6.3 | OK | Battery composition sensitivity | 1406 | low from this. First, the spec-induced refusal cases (§4.3, §4.6.3) showed the response model declining to speculate about int |
| 1728 | §4.3 | OK | Mechanism: Content, Not Format | 996 | cifications.** The wrong-spec adversarial control (Examples §4.3) demonstrates that the response model can recognize spec co |
| 1738 | §3.2 | OK | Subjects | 294 | t Archive). Per-subject Project Gutenberg IDs are listed in §3.2 Table 3.2. Memory-system raw retrieval and ingestion logs a |
| 1740 | §4.1 | OK | The cross-subject gradient | 685 | docs/PROVENANCE_INDEX.md` and `docs/DATA_REFERENCE.md`. The §4.1 battery-composition sensitivity analysis is reproducible vi |
| 1740 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | reproducible via `scripts/_v10_battery_sensitivity.py`. The §3.6.6 rubric-handling validity audit is reproducible via `scripts |
| 1740 | §4.3 | OK | Mechanism: Content, Not Format | 996 | reproducible via `scripts/audit_low_end_inflation.py`. The §4.3 hedging classifier is at `scripts/classify_hedging.py`. |
| 1750 | §2.2 | OK | Memory systems for LLM agents | 186 | ot adjudicate disputes between providers' published claims (§2.2). |
| 1796 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | l Letta stateful-agent exploratory case study summarized in §4.5. Appendix H is the glossary. |
| 1804 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | The extraction step (Step 2 of the pipeline, §3.7) instructs the extraction model to emit triples of the form |
| 1808 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | refuses to do, which is what anchors the authored layers in §3.7. |
| 1822 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | s, beliefs, and self-view.** These populate the core layer (§3.7) and describe the stable commitments a subject carries acro |
| 1905 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | A live web deployment of the pipeline described in §3.7, with served briefs across additional subjects beyond the 1 |
| 2001 | §4.1 | OK | The cross-subject gradient | 685 | onsistent with their status as mid-baseline subjects on the §4.1 gradient. Fukuzawa and Seacole show their largest positive |
| 2005 | §4.1 | OK | The cross-subject gradient | 685 | This appendix provides the technical detail behind the §4.1 battery-sensitivity controls. |
| 2024 | §3.3.1 | OK | Circularity controls | 361 | lobal as a circularity control; its results are reported in §3.3.1 and §4.6.1, not folded back into the §4.1 gradient itself. |
| 2024 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | circularity control; its results are reported in §3.3.1 and §4.6.1, not folded back into the §4.1 gradient itself. |
| 2024 | §4.1 | OK | The cross-subject gradient | 685 | are reported in §3.3.1 and §4.6.1, not folded back into the §4.1 gradient itself. |
| 2028 | §5.3 | OK | Retrieval is not interpretation | 1533 | nt per subject, not about mean score movement per category. §5.3 and §7 flag a follow-up study with a category-balanced batt |
| 2028 | §7 | OK | Future Work | 1674 | bject, not about mean score movement per category. §5.3 and §7 flag a follow-up study with a category-balanced battery as |
| 2052 | §4.1 | OK | The cross-subject gradient | 685 | low-baseline subjects" toward the per-question reframing in §4.1: low-baseline subjects have a larger pool of questions at l |
| 2052 | §4.2 | OK | Compression: structure vs. raw text | 877 | endpoints reached come from band 1) is consistent with the §4.2 finding that even the full source corpus C8 plateaus at a s |
| 2064 | §4.3 | OK | Mechanism: Content, Not Format | 996 | dence from the wrong-spec adversarial control (Appendix C / §4.3) shows the spec as a whole is doing causal work. The null r |
| 2066 | §6.3 | OK | Pipeline and specification stability | 1635 | line variance than the per-subject mean grain documented in §6.3. |
| 2076 | §1.2 | OK | What we tested | 40 | ubject level first, then aggregated across the 14 subjects (§1.2 aggregation rule). |
| 2088 | §4 | OK | Results | 669 | e catalogues every load-bearing analysis result reported in §4 and identifies its status. Post-hoc items are reported as e |
| 2092 | §4.1 | OK | The cross-subject gradient | 685 | H1** Spec-context outperforms no-context \| Pre-registered \| §4.1, §1.3 1st bullet \| Headline gradient \| |
| 2092 | §1.3 | OK | What we found | 104 | pec-context outperforms no-context \| Pre-registered \| §4.1, §1.3 1st bullet \| Headline gradient \| |
| 2093 | §4.1 | OK | The cross-subject gradient | 685 | ely proportional to pretraining coverage \| Pre-registered \| §4.1, §4.1.2, §1.3 1st bullet \| Gradient at both ends; Franklin |
| 2093 | §4.1.2 | OK | The gradient at the high-baseline end (Franklin reference) | 865 | oportional to pretraining coverage \| Pre-registered \| §4.1, §4.1.2, §1.3 1st bullet \| Gradient at both ends; Franklin referenc |
| 2093 | §1.3 | OK | What we found | 104 | al to pretraining coverage \| Pre-registered \| §4.1, §4.1.2, §1.3 1st bullet \| Gradient at both ends; Franklin reference \| |
| 2094 | §4.3 | OK | Mechanism: Content, Not Format | 996 | ent-specificity (correct vs. wrong spec) \| Pre-registered \| §4.3, §1.3 4th bullet \| Wrong-spec controls v1 + v2 \| |
| 2094 | §1.3 | OK | What we found | 104 | ecificity (correct vs. wrong spec) \| Pre-registered \| §4.3, §1.3 4th bullet \| Wrong-spec controls v1 + v2 \| |
| 2095 | §4.4 | OK | Memory-system composition | 1123 | ts with retrieval through three patterns \| Pre-registered \| §4.4, §4.4.2, §1.3 5th bullet \| Memory-system composition \| |
| 2095 | §4.4.2 | OK | Where the spec helps, where it hurts, and which question types route to each | 1194 | h retrieval through three patterns \| Pre-registered \| §4.4, §4.4.2, §1.3 5th bullet \| Memory-system composition \| |
| 2095 | §1.3 | OK | What we found | 104 | val through three patterns \| Pre-registered \| §4.4, §4.4.2, §1.3 5th bullet \| Memory-system composition \| |
| 2096 | §4.2 | OK | Compression: structure vs. raw text | 877 | oken spec recovers most of corpus signal \| Pre-registered \| §4.2, §1.3 3rd bullet \| At 5x to 80x smaller context \| |
| 2096 | §1.3 | OK | What we found | 104 | pec recovers most of corpus signal \| Pre-registered \| §4.2, §1.3 3rd bullet \| At 5x to 80x smaller context \| |
| 2097 | §4.4.1 | OK | Aggregate performance across systems | 1131 | \| Cross-system retrieval-overlap divergence \| Post-hoc \| §4.4.1; sensitivity in §4.6.5; §1.3 7th bullet \| Surfaced during m |
| 2097 | §4.6.5 | OK | Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 1455 | eval-overlap divergence \| Post-hoc \| §4.4.1; sensitivity in §4.6.5; §1.3 7th bullet \| Surfaced during memory-system analysis; |
| 2097 | §1.3 | OK | What we found | 104 | rlap divergence \| Post-hoc \| §4.4.1; sensitivity in §4.6.5; §1.3 7th bullet \| Surfaced during memory-system analysis; mean J |
| 2098 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | \| Letta stateful-agent case study \| Post-hoc \| §4.5; full in Appendix G \| N=3, exploratory \| |
| 2099 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | \| Letta semantic-duplication scaling \| Post-hoc \| §4.5; Appendix G \| Surfaced in this paper's analysis; cosine ≥ 0 |
| 2100 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | \| Abstention-credit validity audit \| Post-hoc \| §3.6.6 \| 9.4% of refusals score ≥ 2.0; bias direction makes the sp |
| 2101 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | \| Per-subject wrong-spec heterogeneity \| Post-hoc \| §4.6.4 \| 5/13 subjects show small positive v1 deltas (coincidental |
| 2102 | §4.3 | OK | Mechanism: Content, Not Format | 996 | \| Hedging-elimination (28.8% → 0.0%) \| Post-hoc \| §4.3, §1.3 6th bullet \| Surfaced from response-level audit \| |
| 2102 | §1.3 | OK | What we found | 104 | \| Hedging-elimination (28.8% → 0.0%) \| Post-hoc \| §4.3, §1.3 6th bullet \| Surfaced from response-level audit \| |
| 2103 | §4.6.3 | OK | Battery composition sensitivity | 1406 | sensitivity (literal-recall fraction) \| Post-hoc reactive \| §4.6.3, Appendix B.6 \| Added in response to v9/v10 reviewer concer |
| 2104 | §4.6.3 | OK | Battery composition sensitivity | 1406 | on leverage check (subset regression) \| Post-hoc reactive \| §4.6.3, Appendix B.6 \| Added in response to v9/v10 reviewer concer |
| 2105 | §4.1.1 | OK | Per-question baseline engagement and the worked rubric example[^companion-data-411] | 819 | upling-free reframing of the gradient \| Post-hoc reactive \| §4.1.1 leveler callout, Appendix B.7 \| Added in response to GPT-5. |
| 2106 | §3.5 | OK | Response models | 416 | der response generation (Tier 2) \| Pre-registered control \| §3.5, §3.3.1, §4.6.1 \| Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects |
| 2106 | §3.3.1 | OK | Circularity controls | 361 | sponse generation (Tier 2) \| Pre-registered control \| §3.5, §3.3.1, §4.6.1 \| Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects \| |
| 2106 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | eneration (Tier 2) \| Pre-registered control \| §3.5, §3.3.1, §4.6.1 \| Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects \| |
| 2107 | §3.3.1 | OK | Circularity controls | 361 | battery regeneration (Control 1) \| Pre-registered control \| §3.3.1, §4.6.1 \| Battery generator circularity \| |
| 2107 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | regeneration (Control 1) \| Pre-registered control \| §3.3.1, §4.6.1 \| Battery generator circularity \| |
| 2108 | §3.6.3 | OK | Calibration | 525 | ge primary, 7-judge sensitivity) \| Pre-registered control \| §3.6.3, §4.6.2 \| Locked panel before scoring \| |
| 2108 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | ry, 7-judge sensitivity) \| Pre-registered control \| §3.6.3, §4.6.2 \| Locked panel before scoring \| |
| 2109 | §4.6.4 | OK | Wrong-spec derangement protocol sensitivity | 1420 | ec derangement protocol sensitivity (v1 vs v2) \| Reactive \| §4.6.4 \| v2 is the standard randomization control; v1 is the adver |
| 2111 | §4 | OK | Results | 669 | scripts and raw data for each row are pointed to throughout §4 and consolidated in §8 Data, Code, and Reproducibility. |
| 2111 | §8 | OK | Data, code, and reproducibility | 1736 | r each row are pointed to throughout §4 and consolidated in §8 Data, Code, and Reproducibility. |
| 2119 | §4 | OK | Results | 669 | A consolidated lookup for the condition IDs used throughout §4. Defined in §3.4; summarized here. |
| 2119 | §3.4 | OK | Experimental conditions | 377 | lookup for the condition IDs used throughout §4. Defined in §3.4; summarized here. |
| 2149 | §3.5 | OK | Response models | 416 | specific context is part of the phenomenon being measured (§3.5, §4.3). |
| 2149 | §4.3 | OK | Mechanism: Content, Not Format | 996 | fic context is part of the phenomenon being measured (§3.5, §4.3). |
| 2186 | §3.6.3 | OK | Calibration | 525 | free-text justification. Calibration diagnostic results in §3.6.3. |
| 2196 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | s \| n/a (read from block) \| Evaluated as a separate path in §4.5, not as a row in the C1 / C3 conditions. \| |
| 2208 | §4.4 | OK | Memory-system composition | 1123 | 0 list often contains 3-5 unique facts. \| Reported as-is in §4.4. Not excluded. \| |
| 2222 | §4.1 | OK | The cross-subject gradient | 685 | This table reproduces the §4.1 cross-subject gradient for reference. Every number is the 5 |
| 2246 | §3.6.2 | OK | Score interpretation | 490 | fferent integer rubric band than the C5 mean. Definition in §3.6.2 and `scripts/compute_anchor_crossing.py`. |
| 2270 | §4.1 | OK | The cross-subject gradient | 685 | sistent with her unusually low C5 baseline of 1.03 noted in §4.1. Per-subject downward-crossing rates stay at or below 15% f |
| 2274 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | This audit is the formal report that §3.6.6 summarizes. It was produced by `scripts/audit_low_end_infla |
| 2338 | §4.1 | OK | The cross-subject gradient | 685 | likely somewhat larger than the +0.89 mean lift reported in §4.1. The paper reports the measured number rather than a length |
| 2338 | §7 | OK | Future Work | 1674 | ntrolled scoring protocol, are both flagged as follow-up in §7. |
| 2342 | §3.6.3 | OK | Calibration | 525 | r Hamerton). The slice-level picture is already reported in §3.6.3 (calibration) and §4.6.2 (5-judge vs 7-judge sensitivity), |
| 2342 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | vel picture is already reported in §3.6.3 (calibration) and §4.6.2 (5-judge vs 7-judge sensitivity), which together establish |
| 2348 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | : Gemini judges not run on C2c or C4 for some subjects; see §4.6.2 on 5-judge vs 7-judge coverage). |
| 2425 | §4.1 | OK | The cross-subject gradient | 685 | cells. Subject rows follow the C5-baseline ordering used in §4.1 (lowest baseline first). Empty Subject cells continue the p |
| 2425 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | as run as a sensitivity judge only on a subset of subjects (§4.6.2); those cells were never populated. Franklin is not include |
| 2425 | §4.2 | OK | Compression: structure vs. raw text | 877 | he global-subject run; Franklin's judgments are reported in §4.2 and are stored under `results/franklin_legacy_20260411/anal |
| 2429 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | nchors 1-5 for one representative subject (Hamerton) are in §3.6 as part of the rubric definition. Examples at anchor crossi |
| 2429 | §4.1 | OK | The cross-subject gradient | 685 | c definition. Examples at anchor crossings are developed in §4.1 (Examples A, B, C on Ebers, Bernal Diaz, Seacole). Three il |
| 2958 | §2.1 | OK | Memory and personalization benchmarks | 158 | benchmark by benchmark, the scope differences summarized in §2.1 between prior work on memory and personalization benchmarks |
| 2974 | §1.1 | OK | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 | pending on provider, model, and benchmark variant (cited in §1.1 and §2.2). Specific numbers per system are in the papers an |
| 2974 | §2.2 | OK | Memory systems for LLM agents | 186 | n provider, model, and benchmark variant (cited in §1.1 and §2.2). Specific numbers per system are in the papers and vendor |
| 3036 | §2.1 | OK | Memory and personalization benchmarks | 158 | line, and the task targets are substantively different (see §2.1). |
| 3054 | §2.2 | OK | Memory systems for LLM agents | 186 | formance 87.9%. Memory-system claims on LoCoMo, detailed in §2.2: Mem0g variant 68.44 with GPT-4o-mini (peer-reviewed, Chhik |
| 3054 | §2.2 | OK | Memory systems for LLM agents | 186 | ini; earlier Zep claim of 84 publicly disputed by Mem0 (see §2.2 dispute note). The methodology disagreement between vendors |
| 3054 | §2.2 | OK | Memory systems for LLM agents | 186 | ethodology disagreement between vendors remains unresolved; §2.2 treats these single-number comparisons with explicit cautio |
| 3056 | §2.2 | OK | Memory systems for LLM agents | 186 | memory systems (Zep, Letta, Mem0, Supermemory) compete on. §2.2 uses these results as context for the memory-system landsca |
| 3060 | §2.2 | OK | Memory systems for LLM agents | 186 | g literature, including MemOS and adjacent evaluations. See §2.2 for the memory-systems landscape. |
| 3070 | §4.4 | OK | Memory-system composition | 1123 | cification and the memory-layer infrastructure compose: our §4.4 Mem0 / Letta / Zep / Supermemory / Base Layer results show |
| 3087 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | *Body summary in §4.5. This appendix retains the full method, per-subject results |
| 3087 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ess checks, content analysis, and caveats from the original §4.5 in v9 / earlier drafts of v10.* |
| 3092 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | is flagged as the highest-priority external falsification (§7.5). |
| 3094 | §4.4 | OK | Memory-system composition | 1123 | query time. Alongside the archival retrieval path tested in §4.4, Letta agents maintain a persistent memory block that the a |
| 3094 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | orpus, rather than chunked and indexed for later retrieval. §4.5 examines what that produces on a small set of subjects, wit |
| 3094 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | compressed variant used here) are flagged as follow-ups in §7.5. |
| 3110 | §4.4 | OK | Memory-system composition | 1123 | l layered stack (anchors + core + predictions + brief) that §4.4's controlled and native C2a / C3 conditions use. The unifie |
| 3120 | §4.4 | OK | Memory-system composition | 1123 | bove the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec for these subjects: Hamerton near par |
| 3122 | §3.6.3 | OK | Calibration | 525 | from the aggregate (the paper's 5-judge primary convention; §3.6.3 and §4.6.2) therefore widens the Letta-over-BL gap rather t |
| 3122 | §4.6.2 | OK | Judge panel sensitivity (5-judge primary vs 7-judge) | 1390 | gregate (the paper's 5-judge primary convention; §3.6.3 and §4.6.2) therefore widens the Letta-over-BL gap rather than narrowi |
| 3142 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | unified-brief variant tested here. All three are flagged in §7.5. |
| 3152 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ed events, and named secondary characters than Base Layer's §4.5 specification, and the gap scales with corpus size. On Babu |
| 3154 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | odes, Base Layer's dimensional axioms compete directly. The §4.5 matched-model gap may be attributable in part to the refere |
| 3154 | §7 | OK | Future Work | 1674 | nsional scaffold would separate the two effects. Flagged in §7. |
| 3156 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | s the highest-priority external falsification we can run on §4.5, and is flagged as such in §7.5. If that replication closes |
| 3156 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | falsification we can run on §4.5, and is flagged as such in §7.5. If that replication closes the gap at parity, §4.5's direc |
| 3156 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | such in §7.5. If that replication closes the gap at parity, §4.5's direction holds on a wider sample. If it reverses, §4.5's |
| 3156 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | , §4.5's direction holds on a wider sample. If it reverses, §4.5's direction was corpus-specific. |
| 3164 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | level, not only a selected set of corpus sizes. Flagged in §7.5. |
| 3167 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | r condition used the unified `spec.md` variant for the main §4.5 table. A robustness rerun with the full layered stack (anch |
| 3167 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | rs + core + predictions + brief, name-restored to match the §4.5 naming convention) preserves direction on all three subject |
| 3168 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | e strips the subject's name during specification authoring (§3.7 anonymization step); the §4.5 comparison restores the name |
| 3168 | §4.5 | OK | Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1344 | ring specification authoring (§3.7 anonymization step); the §4.5 comparison restores the name at the surface level only (str |
| 3168 | §7.5 | OK | Stateful-agent implementations and temporal drift tracking | 1704 | s. only at serving time. Flagged as a methodological gap in §7.5. |
| 3181 | §3.6.3 | OK | Calibration | 525 | oss {Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4}. See §3.6.3. |
| 3183 | §3.6.3 | OK | Calibration | 525 | sh and Gemini 2.5 Pro, reported as a sensitivity check. See §3.6.3. |
| 3185 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | s from the core. A composed brief sits above all three. See §3.7. |
| 3187 | §1.1 | OK | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 | t's own verbatim response on a 1-5 interpretive rubric. See §1.1, §3.6. |
| 3187 | §3.6 | OK | Evaluation: LLM-as-judge with calibration | 450 | n verbatim response on a 1-5 interpretive rubric. See §1.1, §3.6. |
| 3189 | §1.1 | OK | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 | e memory-system retrieval as an interpretive structure. See §1.1, §3.7. |
| 3189 | §3.7 | OK | Base Layer Pipeline for the Behavioral Specification | 633 | ry-system retrieval as an interpretive structure. See §1.1, §3.7. |
| 3191 | §3.6.2 | OK | Score interpretation | 490 | ger band is a within-category shift and a weaker claim. See §3.6.2. |
| 3193 | §1.1 | OK | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 | rty the Behavioral Specification is designed to mirror. See §1.1. |
| 3195 | §3.6.2 | OK | Score interpretation | 490 | ). The strongest categorical signal the rubric detects. See §3.6.2, §4.2. |
| 3195 | §4.2 | OK | Compression: structure vs. raw text | 877 | trongest categorical signal the rubric detects. See §3.6.2, §4.2. |
| 3197 | §3.6.6 | OK | Rubric-handling limitations (validity audit) | 589 | " "I cannot confirm," "would need additional context"). See §3.6.6. |
| 3199 | §1.1 | OK | Recall Is Not Interpretation. Interpretation Can Be Measured. | 24 | behavioral prediction on held-out reasoning situations. See §1.1, §3.1. |
| 3199 | §3.1 | OK | Operationalizing representational accuracy | 278 | oral prediction on held-out reasoning situations. See §1.1, §3.1. |
| 3201 | §3.6.4 | OK | Inter-judge agreement | 559 | claim of new model capability or absolute correctness. See §3.6.4. |
| 3203 | §3.5 | OK | Response models | 416 | g Wing, Zitkala-Sa) with GPT-5.4-regenerated batteries. See §3.5, §4.6.1. |
| 3203 | §4.6.1 | OK | Cross-provider response generation (Tier 2 replication) | 1366 | , Zitkala-Sa) with GPT-5.4-regenerated batteries. See §3.5, §4.6.1. |
| 3205 | §1.3 | OK | What we found | 104 | 2** (seed-fixed random derangement; aggregate Δ +0.15). See §1.3, §3.4, §4.3. |
| 3205 | §3.4 | OK | Experimental conditions | 377 | eed-fixed random derangement; aggregate Δ +0.15). See §1.3, §3.4, §4.3. |
| 3205 | §4.3 | OK | Mechanism: Content, Not Format | 996 | xed random derangement; aggregate Δ +0.15). See §1.3, §3.4, §4.3. |
