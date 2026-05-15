# v11.9.1 — appendix word counts + table formatting audit

## Appendix word counts (cut candidates)

Sorted by word count descending. Anything > 600 words is a cut candidate (redirect to repo).

| § | Level | Title | Words | Cut candidate? |
|---|---|---|---:|---|
| A | H2 | Appendix G. Letta Stateful-Agent: Exploratory Case Study (full) | 2722 | **STRONG cut candidate** |
| A11 | H3 | D.4 Per-judge score matrices | 1742 | **STRONG cut candidate** |
| A11 | H3 | A.1 The 46 Constrained Predicates | 894 | cut candidate |
| A11 | H3 | D.3 Rubric-handling validity audit (full report) | 869 | cut candidate |
| A11 | H3 | B.6 Battery-composition sensitivity | 714 | cut candidate |
| A | H2 | Appendix H. Glossary | 710 | cut candidate |
| A11 | H3 | F.8 Persona-input depth comparison across benchmarks | 623 | cut candidate |
| A11 | H3 | F.4 Twin-2K | 539 | consider trim |
| A11 | H3 | B.10 Pre-registered hypotheses and post-hoc analyses | 500 | consider trim |
| A11 | H3 | B.9 Footnote-redirect technical detail | 497 | consider trim |
| A11 | H3 | B.7 Coupling-free reframing of the gradient | 474 | consider trim |
| A11 | H3 | B.11 Per-system per-subject paired-delta distributions | 412 | consider trim |
| A11 | H3 | B.8 Per-predicate ablation (Phase 2c) | 380 | consider trim |
| A11 | H3 | F.2 PersonaGym | 335 | consider trim |
| A11 | H3 | B.1 The 10 fixed behavioral-prediction categories | 323 | consider trim |
| A11 | H3 | F.1 LongMemEval | 300 | consider trim |
| A11 | H3 | C.6 Memory-system ingestion and retrieval parameters | 277 | consider trim |
| A11 | H3 | D.1 Per-subject 5-judge primary aggregate (main gradient) | 269 | consider trim |
| A11 | H3 | D.2 Per-subject anchor-crossing on the low-baseline slice | 254 | consider trim |
| A11 | H3 | F.5 LoCoMo | 254 | consider trim |
| A11 | H3 | F.3 AlpsBench | 250 |  |
| A11 | H3 | C.1 Condition identifiers (summary card) | 202 |  |
| A11 | H3 | F.7 What no prior benchmark measures | 178 |  |
| A11 | H3 | B.5 Per-subject by axis Δ_spec | 165 |  |
| A11 | H3 | F.6 MemOS and related systems-level benchmarks | 158 |  |
| A11 | H3 | B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING) | 154 |  |
| A11 | H3 | A.2 Provenance and design choices | 141 |  |
| A | H2 | Appendix E. Per-subject worked examples | 131 |  |
| A11 | H3 | B.4 Category-level effect size on Δ_spec | 127 |  |
| A11 | H3 | B.2 Per-subject battery composition (10-category by 15-subject matrix) | 124 |  |
| A11 | H3 | C.5 Judge panel | 121 |  |
| A11 | H3 | C.2 Shared response-model invocation | 120 |  |
| A11 | H3 | C.7 Ingestion exclusions and failure cases | 116 |  |
| A11 | H3 | C.4 Pipeline models (specification generation) | 103 |  |
| A11 | H3 | A.3 Not in the vocabulary | 99 |  |
| A11 | H3 | D.5 Example verbatim responses at each rubric anchor | 82 |  |
| A | H2 | Appendix F. Benchmark Scope Analysis | 74 |  |
| A11 | H3 | C.3 Response models | 71 |  |
| A11 | H3 | A.4 Live deployment | 41 |  |
| A11 | H3 | C.8 Analysis plan lock | 36 |  |
| A | H2 | Appendix A. Predicate Vocabulary | 0 |  |
| A | H2 | Appendix B. Question Batteries | 0 |  |
| A | H2 | Appendix C. Conditions, Models, and Memory-System Configurations | 0 |  |
| A | H2 | Appendix D. Validity Audit and Score Distributions | 0 |  |

---
## Tables with very long cells (formatting issues)

`max_cell_chars > 400` = a single cell that becomes a 10-line block in Word.

`max_cell_chars > 200` = wraps awkwardly, fixable by widening that column or shortening the cell text.


| L | Section | n_rows | n_cols | max_cell | long_cells | very_long | header preview |
|---:|---|---:|---:|---:|---:|---:|---|
| L1079 | 4.2.1 Per-question improvement rate | 7 | 5 | 409 | 4 | 1 | `| Condition (natural-language) | Code | Mean | Band | Excerpt (verbatim) |` |
| L953 | 4.1.1 Per-question baseline engagement a | 6 | 5 | 397 | 5 | 0 | `| Condition (natural-language) | Code | Mean | Anchor | Excerpt (verbatim from `` |
| L721 | 3.7 Pipeline for the Behavioral Specific | 6 | 4 | 290 | 2 | 0 | `| Step | Input | Tool / model | Output |` |
| L2854 | F.8 Persona-input depth comparison acros | 7 | 4 | 208 | 1 | 0 | `| Benchmark | Persona-input form | Approximate input depth (tokens) | Notes |` |

---
## Long heading titles (likely to wrap awkwardly)

Titles > 65 chars often run onto two lines in Word.


- L1 (H1, 87 chars): Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
- L176 (H3, 73 chars): 2.1 Prior measurement targets and the gap representational accuracy fills
- L292 (H3, 79 chars): 3.1 Operationalizing representational accuracy via the Behavioral Specification
- L911 (H3, 68 chars): 4.1.1 Per-question baseline engagement and the worked rubric example
- L1317 (H3, 71 chars): 4.4.2 Layering the Spec: aggregate Δ across systems and ingestion paths
- L1357 (H3, 82 chars): 4.4.3 Where the Spec helps, where it hurts, and which question types route to each
- L1688 (H3, 79 chars): 4.6.6 Retrieval-overlap sensitivity (semantic-similarity matching, K variation)
- L1854 (H3, 70 chars): 5.6 Compression and what makes personalization operationally tractable
- L2237 (H3, 70 chars): B.2 Per-subject battery composition (10-category by 15-subject matrix)
- L2241 (H3, 78 chars): B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING)