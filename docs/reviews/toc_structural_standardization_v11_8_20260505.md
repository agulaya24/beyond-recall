# TOC + structural standardization review — Beyond Recall v11.8 (2026-05-05)

Source: `docs/beyond_recall_v11_8_draft.md` (3,222 lines).

## Summary

- Sections: 9 main + 8 appendices (A-H).
- Numbering scheme: numeric `1.1.1` for body; `Appendix X.Y` for appendices. Maximum nesting in body is 3 levels (e.g., 4.4.3); appendices reach 3 levels (e.g., B.9.3 inside an appendix subsection but only as bold inline labels, not as `####` headers).
- Heading depth: max `### ` (level-3). No `#### ` headers anywhere — confirmed clean.
- Convention deviations flagged: 6 substantive + 4 cosmetic.
- Hard placeholders / publish blockers: 2 ("Appendix B.X" at lines 1210 / 1214, missing Abstract).
- Cosmetic-only items: 4.

## Full TOC (with line numbers)

```
L1     # Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
        (lines 3-9: byline, date, license, code/repo URLs)

L11    ## 1. Introduction
L13      <!-- HTML comment: future-work note for §1 worked example -->
L24    ### 1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.
L40    ### 1.2 What we tested
L104   ### 1.3 What we found
L136   ### 1.4 What this implies

L150   ## 2. Prior Work, Industry Benchmarks, The Fifth Target
L160   ### 2.1 Memory and personalization benchmarks
L186   ### 2.2 Memory systems for LLM agents
L213   ### 2.3 Traceability and Reasoning Traces
L254   ### 2.4 Cognitive and representational foundations

L270   ## 3. Study Design
L276   ### 3.1 Operationalizing representational accuracy
L292   ### 3.2 Subjects
L325   ### 3.2.1 Pretraining-coverage variance
L339   ### 3.3 Question Battery Formation
L359   ### 3.3.1 Circularity controls
L375   ### 3.4 Experimental conditions
L414   ### 3.5 Response models
L448   ### 3.6 Evaluation: LLM-as-judge with calibration
L470   ### 3.6.1 Judge panel
L488   ### 3.6.2 Score interpretation
L523   ### 3.6.3 Calibration
L557   ### 3.6.4 Inter-judge agreement
L577   ### 3.6.5 Aggregation
L587   ### 3.6.6 Rubric-handling limitations (validity audit)
L631   ### 3.7 Base Layer Pipeline for the Behavioral Specification

L667   ## 4. Results
L683   ### 4.1 The cross-subject gradient
L819   ### 4.1.1 Per-question baseline engagement and the worked rubric example
L865   ### 4.1.2 The gradient at the high-baseline end (Franklin reference)
L877   ### 4.2 Compression: structure vs. raw text
L951   ### 4.2.1 Per-question improvement rate
L998   ### 4.3 Mechanism: Content, Not Format
L1125  ### 4.4 Memory-system composition
L1133  ### 4.4.1 Aggregate performance across systems
L1200  ### 4.4.2 Where the spec helps, where it hurts, and which question types route to each
L1295  ### 4.4.3 Case study: cross-system refusal on Keckley Q21
L1327  ### 4.4.4 Two statistical signatures
L1350  ### 4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc)
L1368  ### 4.6 Robustness and sensitivity
L1374  ### 4.6.1 Cross-provider response generation (Tier 2 replication)
L1398  ### 4.6.2 Judge panel sensitivity (5-judge primary vs 7-judge)
L1414  ### 4.6.3 Battery composition sensitivity
L1428  ### 4.6.4 Wrong-spec derangement protocol sensitivity
L1463  ### 4.6.5 Retrieval-overlap sensitivity (semantic-similarity matching, K variation)
L1482  ### 4.6.6 What these robustness checks do not address
L1490  ### 4.7 Summary of §4 and bridge to discussion

L1513  ## 5. Discussion
L1517  ### 5.1 Synthesis: what the seven findings together establish
L1529  ### 5.2 Why the gradient is the load-bearing finding
L1541  ### 5.3 Retrieval is not interpretation
L1551  ### 5.4 Composition with retrieval
L1565  ### 5.5 Wrong-spec mechanism and hedging elimination
L1577  ### 5.6 Compression and what makes personalization operationally tractable
L1587  ### 5.7 Privacy and the case for user-held representation
L1601  ### 5.8 Closing argument

L1611  ## 6. Limitations
L1615  ### 6.1 Subject sample
L1631  ### 6.2 Measurement apparatus
L1645  ### 6.3 Pipeline and specification stability
L1672  ### 6.4 Scope of exploration

L1684  ## 7. Future Work
L1688  ### 7.1 Measurement methodology
L1698  ### 7.2 Subject and corpus expansion
L1702  ### 7.3 Specification design and composition
L1712  ### 7.4 Production serving and infrastructure
L1716  ### 7.5 Stateful-agent implementations and temporal drift tracking
L1734  ### 7.6 Safety-alignment integration
L1742    *Paper body complete. Abstract to be written last.*  <-- italic placeholder

L1746  ## 8. Data, code, and reproducibility
L1768  ## 9. References

L1814  ## Appendix A. Predicate Vocabulary
L1816  ### A.1 The 46 Constrained Predicates
L1903  ### A.2 Provenance and design choices
L1909  ### A.3 Not in the vocabulary
L1917  ### A.4 Live deployment

L1923  ## Appendix B. Question Batteries
L1925  ### B.1 The 10 fixed behavioral-prediction categories
L1944  ### B.2 Per-subject battery composition (10-category by 15-subject matrix)
L1969  ### B.3 Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING)
L2001  ### B.4 Category-level effect size on Δ_spec
L2013  ### B.5 Per-subject by axis Δ_spec
L2017  ### B.6 Battery-composition sensitivity
L2048  ### B.7 Coupling-free reframing of the gradient
L2068  ### B.8 Per-predicate ablation (Phase 2c)
L2084  ### B.9 Footnote-redirect technical detail
L2100  ### B.10 Pre-registered hypotheses and post-hoc analyses

L2129  ## Appendix C. Conditions, Models, and Memory-System Configurations
L2131  ### C.1 Condition identifiers (summary card)
L2151  ### C.2 Shared response-model invocation
L2165  ### C.3 Response models
L2175  ### C.4 Pipeline models (specification generation)
L2188  ### C.5 Judge panel
L2202  ### C.6 Memory-system ingestion and retrieval parameters
L2217  ### C.7 Ingestion exclusions and failure cases
L2226  ### C.8 Analysis plan lock

L2232  ## Appendix D. Validity Audit and Score Distributions
L2234  ### D.1 Per-subject 5-judge primary aggregate (main gradient)
L2258  ### D.2 Per-subject anchor-crossing on the low-baseline slice
L2286  ### D.3 Rubric-handling validity audit (full report)
L2354  ### D.4 Per-judge score matrices
L2441  ### D.5 Example verbatim responses at each rubric anchor

L2447  ## Appendix E. Selected per-subject excerpts
L2451  ### E.1 Hamerton ... L2932 ### E.14 Zitkala-Sa  (14 sub-headers)

L2970  ## Appendix F. Benchmark Scope Analysis
L2974  ### F.1 LongMemEval ... L3086 ### F.7 What no prior benchmark measures

L3099  ## Appendix G. Letta Stateful-Agent: Exploratory Case Study (full)
        (no subsections; single long appendix block to L3190)

L3191  ## Appendix H. Glossary
        (no subsections; alphabetical glossary entries to L3222)
```

## Comparison vs. arXiv ML/AI conventions

| Convention | Standard | Beyond Recall v11.8 | Verdict |
|---|---|---|---|
| Section ordering: Abstract → Intro → Related Work → Methods → Results → Discussion → Limitations → Future Work → Conclusion → References → Appendix | Standard | Intro → Prior Work → Study Design → Results → Discussion → Limitations → Future Work → Data/Code → References → Appendices A-H | **Conforms** with two notable variations: (a) no Conclusion section (§5.8 "Closing argument" subsumes it inside Discussion), (b) Data/Code/Repro block as its own §8 between Future Work and References. Both are common variants in arXiv ML papers; not blocking. |
| Abstract before §1 | Required for arXiv submission | **Missing.** Italic placeholder at L1742 says "Abstract to be written last." | **P0 — must be filled before arXiv submission.** Already tracked in project notes (write-last rule); flagging here for completeness. |
| Author block: byline, affiliation, contact, date | Standard | Lines 3-9: `Author: Aarik Gulaya, Base Layer; Date: April 2026; Preprint (Apache 2.0); Data + Code: github.com/agulaya24/base-layer; Study Repository: github.com/agulaya24/memory-study-repo`. **No email contact, no ORCID.** | **P1.** ArXiv accepts no-email submissions but contact is conventional. Affiliation present. Recommend adding email. |
| Section depth ≤ 3 levels | Convention | Max depth 3 (e.g., §4.4.3, §B.9 → B.9.3 inline-bold only, not `#### ` heading). No `#### ` anywhere. | **Conforms.** |
| Heading labels — Related Work | "Related Work" or "Background" most common; "Prior Work" acceptable | "Prior Work, Industry Benchmarks, The Fifth Target" | **P2 cosmetic.** Three-clause heading is unusual for a §2. Most arXiv papers have a single-noun-phrase title here. Suggest renaming to "Related Work" or "Background" with the Fifth Target framing handled in the section body. |
| Heading labels — Conclusion | "Conclusion" expected | §5.8 "Closing argument" inside §5 Discussion | **P2 cosmetic.** Acceptable variant; some reviewers will look for an explicit "Conclusion" header. Either rename §5.8 → "Conclusion" and pull it out of §5 to its own top-level section, or leave as-is and rely on §5.8 to do the work. Recommend leaving as-is given §5.8 already functions as conclusion. |
| References format | Alphabetical by first author; full surname; arXiv IDs durable identifiers | §9 conforms (Bartlett, Chen, Chhikara, Hinton, Jain, ...). Conventions header at L1770 explains "et al." rule. Already passed independent verification. | **Conforms.** |
| Appendix labeling | "Appendix X. Title" with `### X.Y` subsections | All 8 appendices labeled `## Appendix [A-H]. Title` with `### [A-H].N` subsections | **Conforms.** |
| Cross-references resolve to actual headings | Required | Most do. **§4.4.4 has a heading (L1327) but is never cross-referenced from §5 or earlier despite being load-bearing per project notes.** §3.6.5 has a heading but is never cross-referenced (informational only). | **P1 (§4.4.4 missing referent in §5.4 or §5.5)** — see "Section pointer audit" below. Project memory `project_v11_8_section_pointer_audit.md` flags this class. |
| Numbered figures + tables | Required for arXiv | Tables exist (e.g., conditions table at L65). Figure-numbering convention not audited here (separate review at `figures_signoff_v11_8_20260505_122548.md`). | **Out of scope; treated by figure review.** |

## Recommended fixes

### P0 (publish-day blocking)

1. **Abstract.** Currently a literal placeholder at L1742: "*Paper body complete. Abstract to be written last.*". Must be replaced with a 250-300-word abstract before §1, not after §7. Already tracked in `project_v11_paper_active_editing.md`.
2. **"Appendix B.X" placeholders at L1210 and L1214.** Two literal "B.X" string references in §4.4.2 body and footnote `[^memsys-pattern-appendix]`. The footnote even says "(forthcoming, to be moved during appendix walk)". Resolve to a concrete appendix subsection number (likely B.11 since B.10 is the last existing) and create the corresponding appendix block, OR fold the table into B.5 and update both references.

### P1 (strongly recommended)

3. **Author email/contact line.** Add `Contact: <email>` after `Author:` line (L3). ArXiv submission tools often warn on missing contact even though they accept the upload.
4. **§4.4.4 cross-reference orphan.** §4.4.4 "Two statistical signatures" has a heading but is referenced by no §5 subsection. Either add a §5.4 reference to §4.4.4 (the natural fit per project notes — §5.4 currently references §4.4.2 and §4.4.3 but not §4.4.4), or absorb §4.4.4 into §4.4.2 as a subsection-style block under bold heading.
5. **Section pointer audit (already flagged in project memory).** Project notes flag systematic §X.Y drift carried forward from earlier drafts where §5.6 / §5.7 swapped. Recommend running an automated audit during the final pass (a script that for each §X.Y reference confirms the heading exists at the same depth and label). The sections that are *defined but never cross-referenced* are §3.6.5 (informational, fine) and §4.4.4 (load-bearing, fix per item 4).
6. **HTML comment block at L13-22.** A multi-line `<!-- FUTURE-WORK NOTE -->` block sits between §1 heading and §1.1. Comments do not render in markdown but will appear in any LaTeX/PDF pipeline that converts the source verbatim and in the published `.docx` if not stripped. Decision deferred to production-release pass per the comment itself; flag here so it is removed before LaTeX/arXiv conversion. Either remove or move to a separate `paper_notes.md` file.

### P2 (cosmetic / stylistic)

7. **§2 title rename.** "Prior Work, Industry Benchmarks, The Fifth Target" is unusual. ML convention is a single-noun-phrase header. Suggest "Related Work" (most common) or "Background and Related Work." The "Fifth Target" framing belongs in the section body; the heading does not need to encode the rhetorical structure. This is the single biggest stylistic deviation a reviewer will flag.
8. **§5.8 "Closing argument" → optional rename to "Conclusion" and promote to top-level §6.** Reviewers and arXiv toolchains sometimes look for an explicit Conclusion. Either acceptable; current structure works.
9. **§7 placeholder italic at L1742.** Italic line "*Paper body complete. Abstract to be written last.*" is editorial scaffolding, not paper content. Remove on final pass (will be removed when the abstract is written).
10. **Section title capitalization inconsistency.** §2.3 uses Title Case ("Traceability and Reasoning Traces") while neighbors use Sentence case ("§2.1 Memory and personalization benchmarks", "§2.2 Memory systems for LLM agents", "§2.4 Cognitive and representational foundations"). Pick one convention paper-wide. Same drift in §1.1 ("Recall Is Not Interpretation. Interpretation Can Be Measured." Title Case + double-sentence) versus §1.2 / §1.3 / §1.4 ("What we tested", "What we found", "What this implies" — Sentence case). Sentence case is more common in arXiv ML; recommend converting §1.1 and §2.3 to Sentence case for consistency. Note: §3.3 / §4.3 also use Title Case ("Question Battery Formation", "Mechanism: Content, Not Format"). The §4.3 "Content, Not Format" stylistic choice is a deliberate emphasis; the §3.3 case is drift.

## Appendix labeling consistency check

All 8 appendices verified. Each `## Appendix [A-H]. <Title>` heading is present, and each appendix subsection uses `### <letter>.<number> <title>`:

- A: A.1 - A.4 (4 subsections) — OK
- B: B.1 - B.10 (10 subsections) — OK. Note B.10 is "Pre-registered hypotheses and post-hoc analyses" not "B.10 Pre-registered..." (header text fine; fixed).
- C: C.1 - C.8 (8 subsections) — OK
- D: D.1 - D.5 (5 subsections) — OK
- E: E.1 - E.14 (14 per-subject excerpts, one per main-study subject) — OK
- F: F.1 - F.7 (7 benchmark scope subsections) — OK
- G: no subsections, single appendix block (Letta exploratory case study — full text). **This is a long block (~1200 lines) with no subsection structure**, while every other appendix uses subsections. P2 cosmetic: consider adding 3-4 subsection breaks (G.1 Method, G.2 Results, G.3 Robustness, G.4 Naming-asymmetry caveat / data pointers) to match the rest. Optional, not blocking.
- H: no subsections, alphabetical glossary entries. Standard for glossary appendices; conforms.

## Things that look fine

- Author block, date, license line at L3-9 — present and well-formed.
- §9 References — alphabetical-by-first-author, full surnames, arXiv IDs, venue years where applicable. Already independently verified (`references_independent_verification_v11_8_20260505.md`).
- Body section ordering (Intro → Prior Work → Methods → Results → Discussion → Limitations → Future Work → Data/Code → References → Appendix) — conforms to ML conventions, with two acceptable variants (no separate Conclusion, Data/Code as its own §8).
- Appendix structure A-H labeling — uniform.
- §1.3 enumerates "seven findings" with seven bullets — count matches. (Earlier-draft "six findings" bug already fixed in v11.8.)
- §3 "Study Design" header used in place of "Methods" — common and acceptable variant; reviewer will not flag.
- §4 "Results" header — standard.
- Footnote labels `[^name]` — consistent format throughout.
- No `#### ` (level-4) headers — depth cap respected.
- §6 Limitations as separate top-level section (not buried in Discussion) — preferred ML convention; conforms.
- §7 Future Work organized by theme rather than chronology — clear and conforms.
- §8 Data/code/reproducibility as separate section — increasingly standard for arXiv submissions; conforms.
- Glossary as Appendix H — recommended for papers that introduce defined terms; conforms.
