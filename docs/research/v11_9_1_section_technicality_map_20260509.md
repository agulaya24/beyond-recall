# v11.9.1 — section technicality map

Sections ranked on a 0-5 technical-density scale (higher = denser jargon/stats/codes per 1000 words). Higher scores = more aggressive laymanization opportunity in audience-facing prose; appendix-style scores ≥ 4 are usually appropriate as-is.

**Components (0-5 each, capped):**
- `stats` = Wilcoxon/Spearman/Krippendorff/R²/p=/regression/permutation density
- `greek` = ρ α β Δ π σ μ density
- `var` = Δ_C4a, n=, k=, α=, ρ=, p= variable density
- `code` = backticked file paths (.py / .json / scripts/ / results/)
- `cond` = condition-code (C1, C2a, C4a, ...) density
- `method` = anchor / rubric / panel / judge / abstention / derangement / cosine / jaccard density

**Score-5 → laymanization band:**
- 0.0–1.0 — already layman; touch only if a specific term lands wrong
- 1.0–2.0 — mostly layman; a few terms need parenthetical glosses or a 1-line setup
- 2.0–3.0 — mixed; needs a layman opener + technical body OK to follow
- 3.0–4.0 — technical-by-design; appropriate if it's a methods/sensitivity section, but the section opener should be a layman summary if it's audience-facing
- 4.0–5.0 — fully technical; appropriate for §3.3 internals, §4.6, appendices; not appropriate for §1, §5, abstract

---

| § | Title | wc | Score | Top driver | stats / greek / var / code / cond / method |
|---|---|---:|---:|---|---|
| H2 | 1. Introduction | 1 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;1.1 Recall is not interpretation. Interpretation can be measured. | 813 | 0.0 | method | 0 / 0 / 0 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;1.2 What we tested | 1863 | 0.4 | method | 0 / 0 / 1 / 1 / 14 / 23 |
| H3 | &nbsp;&nbsp;1.3 What we found | 1245 | 0.6 | method | 5 / 4 / 6 / 0 / 4 / 16 |
| H3 | &nbsp;&nbsp;1.4 What this implies | 328 | 0.0 | method | 0 / 0 / 0 / 0 / 0 / 1 |
| H2 | 2. Prior Work, Industry Benchmarks, The Fifth Target | 485 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;2.1 Prior measurement targets and the gap representational accuracy fills | 1175 | 0.0 | method | 0 / 0 / 0 / 0 / 0 / 3 |
| H3 | &nbsp;&nbsp;2.2 Memory systems for LLM agents | 664 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;2.3 Traceability and reasoning traces | 898 | 0.4 | code | 0 / 0 / 0 / 6 / 2 / 2 |
| H3 | &nbsp;&nbsp;2.4 Cognitive and representational foundations | 793 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 3 |
| H2 | 3. Study Design | 152 | 0.3 | method | 0 / 0 / 0 / 0 / 0 / 3 |
| H3 | &nbsp;&nbsp;3.1 Operationalizing representational accuracy via the Behavioral Specification | 434 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;3.2 Experimental conditions | 896 | 1.0 | cond | 0 / 0 / 0 / 2 / 35 / 1 |
| H3 | &nbsp;&nbsp;3.3 Scoring rubric with calibrated LLM judge panel | 555 | 0.9 | method | 0 / 0 / 0 / 1 / 4 / 25 |
| H3 | &nbsp;&nbsp;3.3.1 Score interpretation | 930 | 1.1 | method | 1 / 3 / 2 / 6 / 0 / 37 |
| H3 | &nbsp;&nbsp;3.3.2 Judge panel | 338 | 0.6 | method | 0 / 0 / 0 / 0 / 0 / 14 |
| H3 | &nbsp;&nbsp;3.3.3 Calibration | 754 | 0.8 | method | 0 / 0 / 0 / 2 / 0 / 33 |
| H3 | &nbsp;&nbsp;3.3.4 Inter-judge agreement | 778 | 2.3 | greek | 14 / 25 / 9 / 3 / 0 / 27 |
| H3 | &nbsp;&nbsp;3.3.5 Aggregation and statistical analysis plan | 648 | 1.8 | method | 9 / 7 / 7 / 2 / 2 / 25 |
| H3 | &nbsp;&nbsp;3.3.6 Rubric-handling limitations (post-hoc validity audit) | 299 | 1.7 | code | 0 / 0 / 0 / 7 / 3 / 15 |
| H3 | &nbsp;&nbsp;3.4 Subjects | 290 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;3.4.1 Pretraining-coverage variance | 410 | 0.4 | method | 0 / 0 / 0 / 0 / 1 / 10 |
| H3 | &nbsp;&nbsp;3.5 Question battery formation | 655 | 0.4 | code | 0 / 0 / 0 / 4 / 0 / 1 |
| H3 | &nbsp;&nbsp;3.5.1 Circularity controls | 299 | 0.7 | cond | 0 / 0 / 0 / 1 / 4 / 4 |
| H3 | &nbsp;&nbsp;3.6 Response models | 689 | 1.2 | cond | 0 / 0 / 0 / 7 / 20 / 1 |
| H3 | &nbsp;&nbsp;3.7 Pipeline for the Behavioral Specification | 925 | 0.4 | code | 0 / 0 / 0 / 5 / 3 / 0 |
| H2 | 4. Results | 403 | 0.5 | method | 0 / 0 / 1 / 0 / 0 / 12 |
| H3 | &nbsp;&nbsp;4.1 The cross-subject gradient and its per-question mechanism | 3291 | 1.2 | stats | 30 / 15 / 14 / 10 / 43 / 59 |
| H3 | &nbsp;&nbsp;4.1.1 Per-question baseline engagement and the worked rubric example | 1518 | 0.7 | cond | 2 / 2 / 1 / 5 / 19 / 20 |
| H3 | &nbsp;&nbsp;4.1.2 The gradient at the high-baseline end (Franklin reference) | 492 | 1.0 | code | 0 / 0 / 1 / 3 / 7 / 12 |
| H3 | &nbsp;&nbsp;4.2 Compression: structure vs. raw text | 815 | 0.6 | cond | 0 / 1 / 2 / 0 / 17 / 2 |
| H3 | &nbsp;&nbsp;4.2.1 Per-question improvement rate | 1990 | 0.6 | code | 0 / 7 / 7 / 6 / 15 / 18 |
| H3 | &nbsp;&nbsp;4.2.2 Three statistical signatures | 279 | 1.0 | greek | 1 / 7 / 3 / 0 / 0 / 1 |
| H3 | &nbsp;&nbsp;4.3 Mechanism: Correct Content, Not Format | 2386 | 0.5 | code | 1 / 6 / 6 / 7 / 7 / 22 |
| H3 | &nbsp;&nbsp;4.4 Memory-system composition | 47 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;4.4.1 Cross-system retrieval: providers do not converge | 1229 | 0.5 | method | 0 / 1 / 3 / 4 / 0 / 17 |
| H3 | &nbsp;&nbsp;4.4.2 Layering the Spec: aggregate Δ across systems and ingestion paths | 922 | 1.6 | var | 3 / 19 / 20 / 3 / 6 / 11 |
| H3 | &nbsp;&nbsp;4.4.3 Where the Spec helps, where it hurts, and which question types route to each | 2038 | 0.8 | cond | 0 / 15 / 15 / 2 / 26 / 21 |
| H3 | &nbsp;&nbsp;4.4.4 Case study: cross-system refusal on Keckley Q21 | 914 | 1.0 | code | 0 / 1 / 1 / 10 / 10 / 9 |
| H3 | &nbsp;&nbsp;4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc) | 1765 | 0.4 | code | 1 / 4 / 5 / 5 / 0 / 16 |
| H3 | &nbsp;&nbsp;4.6 Robustness and sensitivity | 173 | 1.1 | stats | 3 / 0 / 0 / 0 / 0 / 7 |
| H3 | &nbsp;&nbsp;4.6.1 Cross-provider response generation (Tier 2 replication) | 705 | 0.7 | method | 0 / 4 / 4 / 2 / 1 / 12 |
| H3 | &nbsp;&nbsp;4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge) | 419 | 1.5 | method | 1 / 3 / 3 / 2 / 0 / 23 |
| H3 | &nbsp;&nbsp;4.6.3 Battery composition sensitivity | 304 | 1.5 | stats | 9 / 1 / 3 / 2 / 0 / 0 |
| H3 | &nbsp;&nbsp;4.6.4 Statistical-rigor checks on the headline gradient | 599 | 2.2 | stats | 47 / 3 / 12 / 6 / 4 / 1 |
| H3 | &nbsp;&nbsp;4.6.5 Wrong-Spec derangement protocol sensitivity | 515 | 0.7 | var | 0 / 5 / 5 / 1 / 0 / 5 |
| H3 | &nbsp;&nbsp;4.6.6 Retrieval-overlap sensitivity (semantic-similarity matching, K variation) | 441 | 1.0 | var | 0 / 0 / 9 / 2 / 0 / 7 |
| H3 | &nbsp;&nbsp;4.6.7 Rubric-handling limitations (post-hoc validity audit) | 1137 | 1.0 | method | 1 / 4 / 10 / 2 / 7 / 31 |
| H3 | &nbsp;&nbsp;4.6.8 What these robustness checks do not address | 261 | 1.4 | code | 0 / 0 / 0 / 5 / 0 / 11 |
| H3 | &nbsp;&nbsp;4.7 Summary of §4 and bridge to discussion | 650 | 0.8 | stats | 8 / 1 / 4 / 0 / 2 / 8 |
| H2 | 5. Discussion | 87 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;5.1 Synthesis: what the seven findings together establish | 448 | 0.2 | method | 0 / 0 / 0 / 0 / 0 / 6 |
| H3 | &nbsp;&nbsp;5.2 Why the gradient is the load-bearing finding | 309 | 0.3 | stats | 3 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;5.3 Retrieval is not interpretation | 243 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;5.4 Composition with retrieval | 385 | 0.4 | var | 1 / 2 / 2 / 0 / 0 / 1 |
| H3 | &nbsp;&nbsp;5.5 Wrong-Spec mechanism and hedging elimination | 478 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;5.6 Compression and what makes personalization operationally tractable | 343 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;5.7 Privacy and the case for user-held representation | 565 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;5.8 Closing argument | 251 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H2 | 6. Limitations | 62 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;6.1 Subject sample | 506 | 0.0 | method | 0 / 0 / 0 / 0 / 0 / 1 |
| H3 | &nbsp;&nbsp;6.2 Measurement apparatus | 731 | 0.6 | method | 1 / 2 / 1 / 0 / 0 / 24 |
| H3 | &nbsp;&nbsp;6.3 Pipeline and specification stability | 1076 | 1.2 | stats | 13 / 7 / 9 / 4 / 6 / 5 |
| H3 | &nbsp;&nbsp;6.4 Scope of exploration | 284 | 0.3 | cond | 0 / 0 / 0 / 0 / 2 / 3 |
| H2 | 7. Future Work | 22 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;7.1 Measurement methodology | 706 | 1.0 | method | 2 / 3 / 9 / 0 / 1 / 20 |
| H3 | &nbsp;&nbsp;7.2 Subject and corpus expansion | 135 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;7.3 Specification design and composition | 623 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 3 |
| H3 | &nbsp;&nbsp;7.4 Production serving and infrastructure | 199 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;7.5 Stateful-agent implementations and temporal drift tracking | 832 | 0.1 | var | 0 / 0 / 1 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;7.6 Safety-alignment integration | 227 | 0.2 | code | 0 / 0 / 0 / 1 / 0 / 0 |
| H2 | 8. Data, code, and reproducibility | 615 | 0.9 | code | 0 / 0 / 0 / 12 / 0 / 3 |
| H2 | 9. References | 575 | 0.2 | method | 0 / 0 / 0 / 0 / 2 / 6 |
| H2 | Appendix A. Predicate Vocabulary | 1 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;A.1 The 46 Constrained Predicates | 894 | 0.1 | code | 0 / 0 / 0 / 1 / 0 / 0 |
| H3 | &nbsp;&nbsp;A.2 Provenance and design choices | 141 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;A.3 Not in the vocabulary | 99 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;A.4 Live deployment | 41 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H2 | Appendix B. Question Batteries | 1 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;B.1 The 10 fixed behavioral-prediction categories | 323 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;B.2 Per-subject battery composition (10-category by 15-subject matrix) | 124 | 0.8 | code | 0 / 0 / 0 / 4 / 0 / 0 |
| H3 | &nbsp;&nbsp;B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING) | 154 | 0.8 | code | 0 / 0 / 0 / 3 / 0 / 0 |
| H3 | &nbsp;&nbsp;B.4 Category-level effect size on Δ_spec | 127 | 2.4 | greek | 0 / 6 / 8 / 1 / 2 / 0 |
| H3 | &nbsp;&nbsp;B.5 Per-subject by axis Δ_spec | 165 | 1.1 | code | 0 / 1 / 1 / 2 / 0 / 2 |
| H3 | &nbsp;&nbsp;B.6 Battery-composition sensitivity | 714 | 1.6 | stats | 12 / 7 / 8 / 4 / 4 / 3 |
| H3 | &nbsp;&nbsp;B.7 Coupling-free reframing of the gradient | 474 | 2.6 | stats | 21 / 5 / 7 / 2 / 23 / 2 |
| H3 | &nbsp;&nbsp;B.8 Per-predicate ablation (Phase 2c) | 380 | 1.5 | code | 2 / 5 / 5 / 3 / 0 / 6 |
| H3 | &nbsp;&nbsp;B.9 Footnote-redirect technical detail | 497 | 1.1 | cond | 0 / 5 / 5 / 1 / 8 / 6 |
| H3 | &nbsp;&nbsp;B.10 Pre-registered hypotheses and post-hoc analyses | 500 | 0.5 | method | 1 / 0 / 1 / 1 / 0 / 9 |
| H3 | &nbsp;&nbsp;B.11 Per-system per-subject paired-delta distributions | 412 | 1.0 | var | 0 / 4 / 4 / 2 / 2 / 4 |
| H2 | Appendix C. Conditions, Models, and Memory-System Configurations | 1 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;C.1 Condition identifiers (summary card) | 202 | 0.9 | cond | 0 / 0 / 0 / 0 / 9 / 1 |
| H3 | &nbsp;&nbsp;C.2 Shared response-model invocation | 120 | 0.8 | cond | 0 / 0 / 0 / 0 / 9 / 0 |
| H3 | &nbsp;&nbsp;C.3 Response models | 71 | 1.7 | code | 0 / 0 / 0 / 3 / 4 / 0 |
| H3 | &nbsp;&nbsp;C.4 Pipeline models (specification generation) | 103 | 0.5 | code | 0 / 0 / 0 / 1 / 0 / 0 |
| H3 | &nbsp;&nbsp;C.5 Judge panel | 121 | 0.7 | method | 0 / 0 / 0 / 0 / 0 / 6 |
| H3 | &nbsp;&nbsp;C.6 Memory-system ingestion and retrieval parameters | 277 | 0.8 | code | 0 / 0 / 0 / 2 / 4 / 1 |
| H3 | &nbsp;&nbsp;C.7 Ingestion exclusions and failure cases | 116 | 1.0 | cond | 0 / 0 / 0 / 1 / 3 / 0 |
| H3 | &nbsp;&nbsp;C.8 Analysis plan lock | 36 | 1.2 | code | 0 / 0 / 0 / 1 / 0 / 1 |
| H2 | Appendix D. Validity Audit and Score Distributions | 1 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;D.1 Per-subject 5-judge primary aggregate (main gradient) | 269 | 1.7 | code | 0 / 2 / 2 / 4 / 3 / 6 |
| H3 | &nbsp;&nbsp;D.2 Per-subject anchor-crossing on the low-baseline slice | 254 | 1.7 | code | 0 / 0 / 1 / 4 / 7 / 4 |
| H3 | &nbsp;&nbsp;D.3 Rubric-handling validity audit (full report) | 869 | 1.5 | cond | 2 / 0 / 1 / 4 / 26 / 29 |
| H3 | &nbsp;&nbsp;D.4 Per-judge score matrices | 1742 | 1.4 | cond | 2 / 2 / 0 / 9 / 85 / 22 |
| H3 | &nbsp;&nbsp;D.5 Example verbatim responses at each rubric anchor | 82 | 1.9 | code | 0 / 0 / 0 / 1 / 2 / 4 |
| H2 | Appendix E. Per-subject worked examples | 131 | 2.8 | code | 0 / 2 / 2 / 3 / 5 / 4 |
| H2 | Appendix F. Benchmark Scope Analysis | 74 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;F.1 LongMemEval | 300 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;F.2 PersonaGym | 335 | 0.2 | method | 0 / 0 / 0 / 0 / 0 / 4 |
| H3 | &nbsp;&nbsp;F.3 AlpsBench | 250 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;F.4 Twin-2K | 539 | 0.1 | method | 0 / 0 / 0 / 0 / 0 / 2 |
| H3 | &nbsp;&nbsp;F.5 LoCoMo | 254 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;F.6 MemOS and related systems-level benchmarks | 158 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;F.7 What no prior benchmark measures | 178 | 0.0 | stats | 0 / 0 / 0 / 0 / 0 / 0 |
| H3 | &nbsp;&nbsp;F.8 Persona-input depth comparison across benchmarks | 623 | 0.1 | code | 0 / 0 / 0 / 1 / 0 / 0 |
| H2 | Appendix G. Letta Stateful-Agent: Exploratory Case Study (full) | 2722 | 0.7 | code | 0 / 8 / 12 / 18 / 2 / 20 |
| H2 | Appendix H. Glossary | 710 | 0.6 | method | 0 / 2 / 2 / 0 / 0 / 24 |