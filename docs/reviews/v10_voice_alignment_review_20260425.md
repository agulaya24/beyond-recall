# v10 Voice and Alignment Review

**Date:** 2026-04-25
**Reviewer:** Claude (Opus 4.7)
**Reference:** `_internal/aarik_clean_pilot/spec.md` (Aarik Gulaya behavioral specification, v10 vintage)
**Subject:** `docs/beyond_recall_v10_draft.md` and `memory-study-repo` public release artifacts.

This document is read-only. No paper or repo file was modified. Verdicts are ALIGNED / DRIFTING / MISALIGNED with the spec's anchors (A1-A12) and behavioral predictions (P1-P15) as the alignment reference. Where a passage is misaligned the citation is to the specific anchor or prediction the passage violates.

---

## 1. Executive Summary

**Top-level verdict: DRIFTING.** The v10 paper holds the paper's load-bearing argument (recall is not interpretation; the spec is the tool for the unknown; per-user representation is a structural requirement) cleanly enough that the central claims read as aligned with Aarik's own framing. The drift sits at three layers: **length** (the paper body is ~1,670 lines plus appendices, which violates A6 COMPRESSION AS QUALITY at the document level), **register** (multiple sections fall into generic ML-paper voice that an outside reader would not identify as Aarik), and **repo metadata drift** (numerical inconsistencies between README / KEY_FINDINGS / DATA_REFERENCE / paper that would not survive Aarik's own A10 PROVENANCE check if he opened the repo cold). No section is structurally misaligned with the anchor set; several sections are voice-misaligned in ways that read as a stronger writer's prose, not Aarik's.

### Top 5 alignment items (paper)
1. **§5.5 Practical implications has no per-user calibration framing.** A6, A1, P1: the section discusses dynamic activation, modifiability, temporality, topic decomposition. It never names "per-user calibration" as the load-bearing property. This is the framing Aarik has explicitly told the project to surface; it is absent where it would land best.
2. **§5.3 The population of relevance underclaims, then overclaims.** A3 EVIDENCE BEFORE ACCEPTANCE: the section is careful about the structural argument, but the abstract framing in README ("approximately 99% of real AI users") is not in the paper at all. The README's number is unsupported and not what the paper itself says. The paper's hedge is correct; the README's confidence is misaligned.
3. **§4.1 coupling-free reframing is a self-critique landed honestly, but buried.** A7 SELF-CRITIQUE AS OPERATING SYSTEM: the reframing ("the steep negative slope is largely a coupling artifact") is the paper's strongest A7 moment. It sits 60+ lines into §4.1 after the headline number is already imprinted. Aarik would surface this in §1.3.
4. **§6 Limitations §6.3 pipeline-stability admission is voice-aligned, but §6.2 LLM-as-judge ends with a sentence that softens the limitation.** A7: "The paper as a whole is best understood as a methodological prototype with LLM-judge-only evidence on the headline directional claims, awaiting human-validation triangulation as the highest-priority single follow-up" is honest and voice-aligned; the surrounding paragraph builds toward it correctly.
5. **§5.5 dynamic activation framed as nice-to-have, then upgraded mid-paragraph to "requirement."** P6: this is one of the strongest substantive moments in §5; the reframe lands. Worth preserving exactly as-is.

### Top 3 voice items (paper)
1. **§2 Prior Work and Industry Benchmarks reads like a literature-review for a journal.** P9: the register is generic-ML-paper, not Aarik. Five subsections, each with the same internal structure ("X (citation): the paper does Y. We measure Z"). Compresses badly and loses load-bearing force.
2. **§3.7 Evaluation runs to ~700 lines across §3.7 to §3.7.6.** A6: the section is correct in detail and earns its length on §3.7.6 (validity audit) but the prose-style on §3.7.1 to §3.7.5 reads as defensive over-explanation rather than direct. P6 violation at the subsection level.
3. **§7 Future Work uses the construction "is a follow-up flagged in §X" 12+ times across the section.** Mechanical filler that adds words without adding signal. P6 violation.

### Top 2 repo items
1. **Numerical drift between repo orientation docs and the paper.** Hamerton C5 baseline: README §2 says 1.25; paper §4.1 table says 1.26; DATA_REFERENCE §1 says 1.26; KEY_FINDINGS M5 cites a "Hamerton +1.99" uplift number that uses a different metric ("Letta block fed to Haiku vs C5") than the paper §4.5 number (+0.14 from Letta vs Base Layer). DATA_REFERENCE was synced 2026-04-24 in the v10 freeze pass; README and KEY_FINDINGS retain stale numbers. A10 violation.
2. **README has no link to the paper's actual abstract because the paper has no abstract yet.** The README opens with marketing prose ("The Flagship Claim") rather than with what the paper actually says about itself. A reader landing cold on the GitHub page reads Aarik's framing of his own work before reading the paper. P3: the README leads with conclusion, not evidence. The paper itself does the right thing (no abstract by design); the repo metadata around it drifts the framing back to GTM.

---

## 2. Spec Reference

The 12 anchors and 15 predictions used as the alignment reference, abbreviated to the load-bearing line each:

| Tag | Name | Used as alignment test for |
|---|---|---|
| A1 | AGENCY-AS-ARCHITECTURE | Whether the paper / repo treats user-held representation as a structural design constraint, not a feature. |
| A2 | LAYERED-SYSTEMS THINKING | Whether sections decompose before reassembling, rather than presenting monolithic claims. |
| A3 | EVIDENCE BEFORE ACCEPTANCE | Whether claims are presented as hypotheses with citation, or as conclusions. |
| A4 | EPISTEMIC TIERING | Whether confidence levels are differentiated across tiers (durable / situational / context-dependent). |
| A5 | STRUCTURED PATIENCE WITH KNOWN VIOLATION | Whether stated rules are violated under pressure, and whether the violation is named. |
| A6 | COMPRESSION AS QUALITY | Whether outputs grow past their load-bearing point; whether reduction is treated as a quality move. |
| A7 | SELF-CRITIQUE AS OPERATING SYSTEM | Whether failures are graded against named rubrics; whether contradictions are surfaced rather than smoothed. |
| A8 | MULTI-AGENT OVER MONOLITH | Whether validation comes from multiple independent sources; whether blind evaluation is preferred. |
| A9 | REGISTER FLUENCY WITHOUT FRICTION | Whether shifts in technical / philosophical / casual register read as smooth context-switching. |
| A10 | PROVENANCE AND TRACEABILITY | Whether outputs can be traced to source; whether black-box conclusions are flagged. |
| A11 | RISK-SEQUENCED EXECUTION | Whether work is ordered to contain instabilities before they propagate. |
| A12 | DOUBT AS LOAD-BEARING STRUCTURE | Whether self-doubt coexists with strong opinions, rather than being resolved or hidden. |
| P1 | AGENCY-VETO REFLEX | First question is who controls what; centralized solutions never the default. |
| P2 | DECOMPOSITION BEFORE SOLUTION | Map components before proposing solutions. |
| P3 | HYPOTHESIS-FIRST SKEPTICISM | Lead with evidence and methodology; not with conclusions. |
| P6 | COMPRESSION AS EDITORIAL STANDARD | Default to shorter outputs; reductions are quality moves. |
| P7 | SYSTEMATIC SELF-GRADING | Failures graded against named rubrics; carry the analysis forward. |
| P10 | PROVENANCE DEMAND ON CONCLUSIONS | Conclusions linked to source facts; black-box judgments flagged as incomplete. |
| P11 | RISK-SEQUENCED TASK ORDERING | Reorder to surface known instabilities first; accept upfront cost to prevent downstream cleanup. |
| P12 | DOUBT COEXISTING WITH CONVICTION | Doubt is not resolved by reassurance; it operates in parallel with strong opinions. |

Plus the auto-memory voice rules: no em-dashes, no GTM-language, "AI never knew, not AI forgot," "prediction is the test, not the product," "individual-first is load-bearing," "model bias is good as long as it is biased for you," "per-user calibration to interact with data and decisions on their behalf."

---

## 3. Per-Section Paper Review

### §1.1 Recall Is Not Interpretation. Interpretation Can Be Measured.

**Alignment: ALIGNED.** The section establishes the load-bearing distinction (recall vs interpretation) and frames it correctly: prior systems "compete on standard recall benchmarks," the function of memory is dictated by how an individual processes facts, AI systems must be personalized to how that person interprets. This is the framing Aarik has stated repeatedly in `feedback_prediction_framing.md` and the auto-memory ("prediction is the test, not the product"). The introduction of "representational accuracy" as the AI-side property and "interpretation" as the human-side property reads as Aarik's own decomposition (A2). The H1-H5 hypothesis list (§1.2) is exactly the LAYERED-SYSTEMS THINKING decomposition the spec predicts.

**Voice: ALIGNED.** Direct declaratives. The sentence "Optimizing further on recall leaves something more fundamental unmeasured" lands in Aarik's voice. The phrase "Memory is deeply personal" is one declarative beat that earns its place. No em-dashes, no GTM language.

**Highest-impact change:** The phrase "by extension to the relative experiences of any individual" in paragraph 2 is the one piece of soft prose in this section. Tighten to "across individuals." A6.

---

### §1.2 What we tested

**Alignment: ALIGNED.** The five hypotheses are properly hypotheses (A3, P3): "A response model given a Behavioral Specification ... produces responses that align with that person's documented behavior more closely than the same model given no context." Falsifiable, structured, A2-style decomposition. The condition table (C1-C9 plus C2c) is the most compressed possible reading of the experiment matrix; it is the kind of artifact Aarik's spec predicts (P2 DECOMPOSITION BEFORE SOLUTION).

**Voice: ALIGNED.** The phrase "every meaningful combination of inputs was evaluated as its own condition" is direct. The sentence "The five hypotheses map directly to §4: H1 and H2 to §4.1 The Gradient; H3 to §4.3 Mechanism; H4 to §4.4 Memory-System Composition; H5 to §4.2 Compression" is exactly the structural-mapping move A2 predicts. Reads as Aarik.

**Highest-impact change:** None at the section level. The "Additional testing for Letta" paragraph could be 2 lines shorter without losing content. Trivial.

---

### §1.3 What we found

**Alignment: DRIFTING.** The section is correct on substance. The drift is in **placement**. The headline-numbers callout box is sound. The "primary result: the gradient" paragraph is sound. The compression result and the mechanism result land cleanly. **Then** at line 116 the paper pivots into "Where the specification helps and where it hurts" and runs through Ebers Q3, Sunity Devee Q35, Keckley Q21 with detailed score reporting. This is the right material. It belongs here. But the section runs 90+ lines without a structural break, and the per-question examples ride past the load-bearing claim ("the gradient") rather than buttressing it. A6 violation at the subsection level. The "infrastructure-implication" paragraph at the end of §1.4 is exactly where Aarik's voice should be loudest, and it lands well; its weight is diluted by the volume of §1.3 above it.

**Voice: DRIFTING.** The mechanism prose at lines 102-108 is solid. The hedging-rate sentence ("Under a narrow rule (a response counts as hedged only if its first non-whitespace text matches an explicit refusal prefix: 'I cannot,' 'I can't,' 'I don't,' 'I do not,' 'The retrieved facts do not,' 'The retrieved facts don't'), baseline hedging of 28.8% (146/507) drops to 1.4% (7/507) with the specification alone and 0.0% (0/507) with facts plus specification") is one sentence carrying ~80 words including 12 percentages and 6 fractions. P6 violation. Aarik would break this. The "additivity" paragraph at lines 108-115 lands well; the per-system bullets are A2-aligned.

**Highest-impact change:** Move the §4.1 coupling-free reframing finding (currently buried in §4.1 line ~755) up into §1.3's headline. The paper's strongest A7 moment ("the steep negative slope is largely a coupling artifact of the change-score parameterization") should appear before the headline number is read 60+ times. Aarik's spec predicts he would surface the self-critique upstream of the conclusion it qualifies, not downstream.

---

### §1.4 Why the gradient matters for real users

**Alignment: ALIGNED.** This is one of the paper's strongest sections for matching Aarik's spec. The structural-extrapolation argument is hedged exactly right (A3, A12): "if the specification is uniformly beneficial for the lowest-baseline historical figures we could test, and if a typical living user whose private decisions were never indexed is expected by construction to sit at or below that same floor, the specification should be at least as beneficial for typical real AI users as it is for the historical subjects measured here." The "what we did not prove" paragraph is the A7 self-critique landed correctly. The infrastructure-implication paragraph closes with "Either each user supplies their own representation to whatever AI system serves them, or personalization remains surface-level (style, voice, preference) without the interpretive substrate that makes an agent's actions actually reflect the person." This is A1 AGENCY-AS-ARCHITECTURE in the paper's own voice.

**Voice: ALIGNED.** The phrasing "user-held, portable, inspectable, traceable, representation-grade" is Aarik's voice. The phrasing "Either each user supplies their own representation, or personalization remains surface-level" reads as the binary-architectural framing P2 predicts.

**Highest-impact change:** None. Possibly hold this section verbatim. The repo's README claim that "approximately 99% of real AI users have negligible pretraining representation" should be removed from the README and replaced with §1.4's hedged structural-extrapolation language. The paper itself is correct; the README overshoots. (This is a repo finding, recorded in §5 below.)

---

### §2 Prior Work and Industry Benchmarks (subsections §2.1-§2.5)

**Alignment: DRIFTING.** The substance is right (P3 HYPOTHESIS-FIRST SKEPTICISM applied to other people's claims: the dispute over Mem0 vs Zep LOCOMO methodology, the noted methodological immaturity of conversational memory benchmarks, the explicit statement that "this paper does not attempt that adjudication"). The §2.3.1 "What Existing Benchmarks Measure vs What Representational Accuracy Tests" subsection is a strong A2 decomposition: prediction-is-test-not-goal, what-the-held-out-design-tests, what-recall-measures-and-doesnt, what-survey-prediction-measures, what-persona-fidelity-measures, what-preference-alignment-measures, the missing axis. Each subsection lands.

**Voice: DRIFTING.** The §2.1 to §2.4 register drifts into generic-literature-review prose. Five paragraph blocks per benchmark, each beginning "X (citation): an extract-consolidate-retrieve pipeline..." reads like a section a graduate student would write, not Aarik. The §2.5 LLM-as-judge subsection is two paragraphs and reads correctly. P9 says register-shifts should be smooth; here the shift into journal-conventional prose is jarring.

**Highest-impact change:** §2.1 to §2.4 could compress by ~30%. The Table 2.1 carries most of the comparison; the prose under each provider largely repeats the table's content. P6 says lists that grow too long become taxonomies. §2.1 currently is a taxonomy.

---

### §3 Study Design (focus on §3.1, §3.3, §3.7, §3.7.6 validity audit)

**§3.1 Representational Accuracy: ALIGNED.** Three-component decomposition (the person has consistent patterns, the representation carries the signal, a model can act on it) is A2 textbook. The sentence "We do not claim to modify the model's internal parameters. The Behavioral Specification is served as context: a lens through which the model can reason about a specific person" is direct in Aarik's voice. ALIGNED on voice as well.

**§3.3 Pipeline: ALIGNED.** The five-step table (Import / Extract / Embed / Author / Compose) plus the Anchors / Core / Predictions / Brief structure is the most compressed possible description of the pipeline. P2 DECOMPOSITION BEFORE SOLUTION: the section maps the architecture before claiming results. The Hamerton example anchors / core / predictions paragraphs are concrete enough that a reader can audit the artifact (A10). ALIGNED on voice.

**§3.7 Evaluation: DRIFTING.** Substance is correct. **Length is the problem.** §3.7 through §3.7.6 occupies roughly 200 lines. The §3.7.1 judge panel table, §3.7.2 calibration, §3.7.3 fractional-score interpretation, §3.7.4 inter-judge agreement, §3.7.5 aggregation, and §3.7.6 rubric-handling validity audit each have legitimate content. The drift is that §3.7.2 to §3.7.5 cover ground that could collapse to 30 lines without losing argument. The §3.7.6 validity audit is the section that earns its length and is exactly Aarik's A7 voice ("Both rubric-handling effects pull the measured C5 baseline upward. This shrinks the measured spec-vs-baseline gap. The true effect size for the population of relevance is likely somewhat larger than the +0.89 mean lift we report; we elect to report the measured number and flag the direction of the bias rather than recompute under a modified rubric, to keep the analysis plan lock intact").

**§3.7.6 validity audit: ALIGNED.** This is one of the most aligned sections in the paper. The audit explicitly names two rubric-handling limitations, classifies their direction (paper-favorable: the measured effect is a lower bound on the true effect), and elects not to recompute. This is exactly A5 STRUCTURED PATIENCE WITH KNOWN VIOLATION applied to a measurement: the analysis plan is locked, the violation is named, the direction is graded, the inference is carried forward. ALIGNED on voice. Hold verbatim.

**Highest-impact change for §3.7:** Compress §3.7.1 to §3.7.5 by half. §3.7.6 stays verbatim. The Krippendorff α paragraph in §3.7.4 is one example: it could be three lines. It is twelve.

---

### §4.1 The cross-subject gradient

**Alignment: DRIFTING.** The headline result is sound. The sensitivity checks (battery composition, GPT-5.4-battery subset, coupling-free reframing) are correct A8 multi-source-validation moves and represent the strongest empirical-rigor work in the paper. The drift is the **placement** of the coupling reframing. The reader sees ~100 lines of headline result, per-subject table, anchor-crossing distributions, and three illustrative examples (A, B, C, D) before reaching "Coupling-free reframing of the gradient" at line 755. By that point the −0.96 slope and the R² = 0.82 are already imprinted. The reframing then says "the steep negative slope is largely a coupling artifact" and the framing has to be backed out of after the fact. Aarik's spec predicts he would surface this self-critique upstream of the result it qualifies (A7).

**Voice: ALIGNED on most paragraphs, DRIFTING on the example boxes.** The Example A / B / C boxes carry the right content but the prose register inside them ("With specification + facts (C4a, 5-judge mean 3.60): Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable") is generic-evaluation-text rather than Aarik. The "What the specification did" sub-summaries are direct and land. The "A note on rubric handling of abstention" callout in Example C is in Aarik's voice (A7).

**Highest-impact change:** Move "Honest reframing" (the ~5-line block at line 759) into §1.3's headline numbers callout, with a forward-pointer to the full sensitivity treatment in §4.1. Aarik's spec predicts the self-critical reframing should appear at the moment the headline is first stated, not after.

---

### §4.2 Compression

**Alignment: ALIGNED.** The substance is direct. The H5 statement (compact specification recovers most of raw corpus's signal at a fraction of the context) is supported by the per-subject compression table. The "honest cost of compression" Ebers example explicitly names where compression loses signal (0.64 points on the rubric). This is A7 self-critique applied at the per-subject level. The §4.2.1 question-improvement-rate proposal is A8 multi-source-validation logic ("A cleaner unit: out of N individual questions, how many does each condition improve over the no-context baseline?") and the failure-mode analysis at the end ("Tiny-gain inflation," "Hidden catastrophic harm," "Easy-baseline gaming," "Scale-free illusion of portability") is exactly the kind of multi-mode failure-decomposition Aarik's spec predicts.

**Voice: ALIGNED.** The phrasing "the dose-response curve has a steep initial slope and a long plateau" is direct. The "behaviorally relevant signal in autobiographical text is sparse and compressible" sentence is Aarik's voice.

**Highest-impact change:** None at the section level. The "Per-1,000-tokens-of-context efficiency" framing in §4.2 paragraph 3 could be tightened to one line; currently runs three.

---

### §4.3 Mechanism: Content, Not Format

**Alignment: ALIGNED.** The two-variant wrong-spec design (v1 fixed adversarial derangement and v2 random derangement) is exactly the A8 multi-source-validation move. The two together "bracket the question": adversarial mismatch hurts, random mismatch barely helps. The 60.6% / 36.5% bimodal classification of wrong-spec responses is supported by a 30-response stratified manual spot check (A10 PROVENANCE). The three mechanism types (identity disambiguation, directional correction, interpretive inference) are A2 decomposition. The matched per-question examples (A wrong-spec, B wrong-spec, C wrong-spec) directly mirror §4.1's correct-spec examples; the parallelism is the right structural choice.

**Voice: ALIGNED.** The Example B "content convergence across genuinely different frameworks" reading is exactly the kind of subtle-mechanism-reading Aarik's spec predicts. The sentence "The two specs are genuinely different frameworks ... Direct anchor-to-anchor comparison across the two specs finds zero substantive mirroring. On the specific question of refusing offered physical help, the two frameworks converge by different logics" is in Aarik's voice (P9 register-fluency, A2 decomposition).

**Highest-impact change:** The "Spec-activation evidence" subsection (~lines 916-918) repeats the 78.6% / 50.0% citation rate without adding mechanistic claim. Could compress to one sentence; currently three.

---

### §4.4 Memory-system composition

**§4.4.1 Aggregate: ALIGNED.** The two-configuration design (controlled vs native) is A8. The "three of four commercial systems benefit from the specification" headline is the right framing, not "four of four." The Supermemory near-zero is reported honestly. Reads ALIGNED on voice. The "Zep is the cleanest positive case" paragraph is direct.

**§4.4.2 Common Mechanisms: ALIGNED.** The per-subject paired-delta distribution table (Table 4.6) is the right artifact. The sentence "Every row is a mixture. Even Zep's strongest row (Seacole, Δ +0.52) has 8 questions where the specification regresses by more than 0.3 points" is exactly Aarik's voice and an A7 self-critique applied at the per-row level.

**§4.4.3 Keckley Q21: ALIGNED.** The five-system reproduction of the same spec-induced refusal, with magnitude proportional to baseline-retrieval productivity, is the cleanest possible mechanism-isolation. The sentence "The Q21 refusal is a property of the specification. The rubric penalty for that refusal is a property of the rubric (§3.7.6 validity audit, §4.4 Example 3)" is the paper's strongest decomposition (A2 + A7 + A10).

**Voice: ALIGNED on all three subsections.**

**Highest-impact change:** None. The Supermemory deep-dive in §4.4.1 could be shortened by one example (Example 4 Fukuzawa Q16 partly duplicates Example 1's mechanism), but the section earns its length on the cross-system Pattern 1/2/3 reproduction.

---

### §4.5 Exploratory case study (Letta)

**Alignment: ALIGNED.** The section is correctly framed as exploratory and post-hoc. "Headline result on the small sample tested" is hedged correctly. "What this does and does not show" is A7 self-critique. The architectural-ceiling observation (~333K characters, 25.4% verbatim duplication on Babur) is the right empirical observation for the framing. Pointer to Appendix F for the full case study is the right A6 move (compress the body, expand the appendix).

**Voice: ALIGNED.** The phrasing "The two systems are prediction-band compatible at small corpora and diverge on compression at large ones" is direct, evidence-based. The flag for §7.5 follow-up is A11 RISK-SEQUENCED.

**Highest-impact change:** The §4.5 Letta-block-size-versus-compose-step character-count paragraph could be removed from the body and live entirely in Appendix F. The body summary already contains the architectural ceiling observation in one sentence.

---

### §4.6 Robustness and sensitivity

**Alignment: ALIGNED.** The §4.6.1 Tier 2 cross-provider replication is A8 multi-source-validation done correctly: 5 of 6 cells reproduce the direction, the one non-matching cell (Zitkala-Sa × Gemini Pro) is consistent with Zitkala-Sa's main-study null rather than a contradiction. This is exactly the failure-mode-classification Aarik's spec predicts (P7 SYSTEMATIC SELF-GRADING). The §4.6.2 5-judge-vs-7-judge sensitivity is presented honestly: "Gemini inclusion widens spec-effect magnitudes rather than narrowing them. The 5-judge primary is the conservative choice." The §4.6.3 explicit acknowledgment that "Neither Tier 2 nor the judge-panel sensitivity escapes the class-level LLM concern" is the right A7 boundary statement.

**Voice: ALIGNED.** The sentence "Reporting 5-judge primary means every paper claim is the conservative version" lands as Aarik. The sentence in §4.6.3 "Tier 2 narrows the within-provider concern to 'non-Haiku LLMs reading non-Anthropic batteries produce the same direction'; the judge-panel sensitivity shows that removing the most-inflationary judges makes the effect smaller, not larger. Together these checks rule out several within-family artifact hypotheses but do not replace human validation on the full pipeline" is exactly the kind of boundary-defining sentence the spec predicts.

**Highest-impact change:** None. The section earns its length on the rigor.

---

### §5.1 The Anti-Pattern: What Behavioral Specification Is Not

**Alignment: ALIGNED.** Five-paragraph negation (it is not memory recall, not persona fidelity, not preference alignment, not survey-response interpolation, not a psychometric profile) is A2 DECOMPOSITION applied negatively. Naming the anti-pattern before stating the positive target is exactly the move Aarik's spec predicts (P2 DECOMPOSITION BEFORE SOLUTION).

**Voice: ALIGNED.** The phrasing "The Behavioral Specification's anchors are surfaced from the subject's corpus rather than projected onto a fixed axis set" is in Aarik's voice. The closing "the positive target is narrower than any of the above. We want a representation that lets a response model act as this specific person would, on situations the model has never seen" is direct.

**Highest-impact change:** None. Hold verbatim.

---

### §5.2 What the study demonstrates

**Alignment: ALIGNED.** Four-bullet summary maps directly to H1+H2 / H3 / H4 / H5 (which §1.2 promised). The §4.5 exploratory note is hedged correctly. The closing pointer to §5.3-§5.6 is A11 RISK-SEQUENCED structure.

**Voice: ALIGNED.** Direct.

**Highest-impact change:** None.

---

### §5.3 The population of relevance

**Alignment: ALIGNED on the paper text; the README's "99% of real AI users" framing is MISALIGNED with this section and is a repo-level finding, not a paper-level one.** The paper section reads "every such user sits in the low-baseline band because their private reasoning is structurally absent from training data, then representational accuracy is not an enhancement for edge cases. It is a structural requirement for personalization at all," which is correct. The structural argument is hedged correctly: "rests on a structural argument: private reasoning is not in any training corpus, so pretraining cannot close the gap, so a user-supplied representation is required. The structural argument is strong but not a substitute for the empirical replication."

**Voice: ALIGNED on the section.** Direct.

**Highest-impact change:** Add one sentence acknowledging that the percentage figure ("99%") that appears in the README and other repo orientation docs is a heuristic rather than measured. Currently the paper does not source any percentage; it argues structurally. The repo's percentage claim should either be removed from the repo or grounded in the paper here.

---

### §5.4 Content specificity and mechanism

**Alignment: ALIGNED.** This is one of the paper's strongest sections for A7 SELF-CRITIQUE. "The three patterns together imply dynamic spec activation is a requirement for production response quality. Pattern 1 (pattern supply) helps when retrieval is thin on interpretive structure. Pattern 2 (over-theorization) hurts when retrieval already has the plain answer. Pattern 3 (structural refusal) hurts when the specification's honesty axioms fire on questions where retrieval was insufficient. Serving the full specification on every query, as this study did, subjects every question to all three mechanisms regardless of which one is appropriate for the query." This is the paper acknowledging that the experimental serving strategy is suboptimal in production, while presenting the result on its actual experimental conditions. A5 STRUCTURED PATIENCE WITH KNOWN VIOLATION applied to engineering.

**Voice: ALIGNED.** "Specification design is a multi-objective problem" is direct.

**Highest-impact change:** None. Hold verbatim.

---

### §5.5 Practical implications

**Alignment: DRIFTING.** Substance is right: context budget, authoring cost, per-query cost, dynamic activation, modifiability, temporality, topic decomposition, update cadence, positioning against alternatives, infrastructure properties. Each subsection is correctly hedged ("as served in this study"; "would plausibly activate"; "is a separate measurement question, not answered by this paper"). **The drift:** the section never names "per-user calibration" as the load-bearing property the implementation is implementing. The auto-memory rule "per-user calibration to interact with data and decisions on their behalf" should be the framing-claim that ties dynamic activation, modifiability, and topic decomposition together. Currently each is presented as a separate engineering proposal. Aarik's spec predicts he would frame these as four implementations of the same underlying property: the user's calibration applied to their own behalf.

**Voice: DRIFTING.** The section is technically correct but reads as a "future work" subsection one would find in any ML paper. The "user-held," "inspectable," "provenance-traced," "local-executable retrieval" four-bullet list at the bottom is the most aligned moment of the section (A1 + A10). The dynamic-activation paragraph reads like generic engineering-handwave: "Embed the incoming query / Retrieve the specification components / Retrieve facts tied to the activated specification components / Serve the activated subset plus the brief as context, rather than the entire stack."

**Highest-impact change:** Add a one-line frame at the top of §5.5: "The implementation choices below are different ways of letting per-user calibration interact with data and decisions on the user's behalf." Then introduce dynamic activation, modifiability, temporality, topic decomposition as concrete realizations of that property. This makes A1 visible at the structural level rather than only in the "Infrastructure properties" four-bullet list at the bottom.

---

### §5.6 What the study does not settle

**Alignment: ALIGNED.** The "Framing: read for directionality, not precision" opening paragraph is exactly the A4 EPISTEMIC TIERING the spec predicts: directional results vs precision results are at different tiers, treated with different standards. The five-item list (multi-subject living-user replication, rubric validity, component ablation, production deployment gap, LLM-as-judge circularity) is decomposed correctly.

**Voice: ALIGNED.** "A reader should take a +0.89 mean improvement on the low-baseline slice as strong evidence that the specification helps more where baseline is lower, not as a claim that the effect size is exactly 0.89 points" is exactly Aarik's voice.

**Highest-impact change:** None. Possibly the strongest A7 section in the paper.

---

### §6 Limitations (focus on §6.2 LLM-as-judge, §6.3 pipeline variance)

**§6.1 Subject sample: ALIGNED.** Public-domain selection bias, self-presentation bias, translation artifacts, era; each named, each direction-of-bias graded. A7.

**§6.2 Measurement apparatus / LLM-as-judge: ALIGNED.** "The 5-judge primary panel can answer the directional question (does the specification move representational accuracy in the right direction) but not the absolute-quality question (is any specific numeric value the right score). A stratified human-validation subset is the leading measurement follow-up flagged in §7.1; until that exists, the paper's claims should be read as directional rather than precise." The bolded sentence "**The paper as a whole is best understood as a methodological prototype with LLM-judge-only evidence on the headline directional claims, awaiting human-validation triangulation as the highest-priority single follow-up**" is the most A7-aligned paragraph in the paper. ALIGNED on voice.

**§6.3 Pipeline and specification stability: ALIGNED.** The per-subject pipeline-variance probe (n=3 reruns each on Sunity Devee, Yung Wing, Augustine) is A8 multi-source-validation applied to the pipeline itself. The "Read of the precision question" paragraph names the magnitude (run-to-run SD = 0.10 vs cross-subject SD = 0.59) and concludes "directional finding survives across reruns; per-subject Δ_C4a numbers should be read with a soft uncertainty bar of roughly ±0.10 around them." Augustine's sign flips on 2 of 3 reruns is named, not hidden. A7.

**Voice: ALIGNED on both subsections.**

**Highest-impact change:** §6.2's "Response-model coverage" paragraph reads as procedural list; the section is otherwise voice-aligned. Possibly tighten by 30%, no structural change.

---

### §7 Future Work (focus on §7.5 stateful-agent + drift, §7.6 safety)

**Alignment: DRIFTING.** Substance is reasonable. Each follow-up maps to a §6 limitation or §5.6 open item. The drift is **mechanical filler.** The phrase "is a follow-up flagged in §X" or "flagged in §7" appears 12+ times across the section. The construction "is a/the [adjective] follow-up" appears another 8+ times. Each individual flag is reasonable; in aggregate the prose carries low information density. P6 violation.

**§7.5 Stateful-agent + drift: ALIGNED on substance, DRIFTING on prose density.** The "stateful-agent variant of the Behavioral Specification" / "cleaner §4.5 rerun with naming and scaling controls" / "temporal drift tracking" / "continuous-representation infrastructure" four-part decomposition is A2 done correctly. The SCOTUS sequential-checkpoint design as a portable methodology is the right A11 forward-pointer to a corpus that doesn't share the autobiography-bias problem.

**§7.6 Safety integration: DRIFTING on substance.** The post-hoc classifier audit (75 of 81 spec-induced refusals are routine behavioral-prediction, not morally loaded) is the right A7 self-critique applied to the H8 reframing ("conservatism dial" not "moral-integrity mechanism," per the v9 update notes). The section then frames safety-alignment integration as "collaboration space with AI safety researchers," which is honest about scope but reads as a deferral. This section may be where Aarik's auto-memory rule "model bias is good, as long as it is biased for you" should appear. It does not. The framing here is "behavioral-spec authoring on a malicious user," a defensive posture. The "biased for you" framing is offensive: the spec is intentionally biased toward the specific person it represents, and that bias is the desired property. The framing should appear here.

**Voice: DRIFTING.** Multiple paragraphs read as bibliography-summary. The "additional architectural paths worth testing" paragraph at the end of §7.5 is generic.

**Highest-impact change:** Compress §7 by ~30% by removing the mechanical "flagged in §X" filler. Add the "model bias is good, as long as it is biased for you" framing into §7.6 as the affirmative version of the safety-alignment question.

---

### §8 Data, code, and reproducibility

**Alignment: ALIGNED.** Apache 2.0 + CC-BY 4.0, all raw response files in the repo, source autobiographies from Project Gutenberg / Internet Archive, pointer to PROVENANCE_INDEX, pointer to DATA_REFERENCE, total study cost USD 350, runs on a standard developer laptop. A1 (user-held, transparent), A10 (PROVENANCE), A11 (RISK-SEQUENCED). The "Conflicts of interest" disclosure is the kind of A3 epistemic-hygiene disclosure the spec predicts.

**Voice: ALIGNED.** Direct, factual.

**Highest-impact change:** None.

---

### §9 References

**Alignment: ALIGNED.** Bartlett, Chen, Chhikara, Hinton, Jain, Jiang, Lu, Maharana, Packer, Rasmussen, Samuel, Toubia, Verga, Wu, Xiao, Zheng. Each cited reference appears in the body with a specific claim attached. A10 PROVENANCE done correctly. The Gulaya 2026 self-cite is the correct artifact-pointer.

**Voice: ALIGNED.** No comment needed.

**Highest-impact change:** None.

---

### Appendix F (Letta full case study)

**Alignment: ALIGNED.** N=3 case study explicitly framed as "post-hoc exploration, not a replication or a headline finding." The "Methodological note on the Base Layer condition served here" paragraph is the right A7 self-critique: the §4.5 main result table compared Letta's named, self-edited block against Base Layer's unified-brief variant rather than the full layered stack. The robustness rerun against the full layered stack preserves direction. The naming asymmetry (Letta ingests named corpus; Base Layer authors anonymized then restores name at serving) is named as a methodological gap. The content-comparison ("referential density: Letta's rolling summary retains roughly an order of magnitude more unique proper nouns, dated events, and named secondary characters than Base Layer's specification") is the right per-subject decomposition (A2 + A7).

**Voice: ALIGNED.** "Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts" is direct. "The §4.5 matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects" is A8 follow-up logic.

**Highest-impact change:** None. Hold verbatim.

---

## 4. Cross-cutting Paper Findings

### 4.1 Where does the paper still hold a generic ML-paper voice?

§2.1 to §2.4 (per-provider blocks). §3.7.1 to §3.7.5 (judge-panel mechanics). §7 Future Work (mechanical "flagged in §X" filler). The Example A / B / C boxes within §4.1 carry their content well but the prose-style inside the boxes ("Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable") reads as evaluation-text, not Aarik. These four sections together constitute roughly 25-30% of the paper body. P9 says register-shifts should be smooth; in the paper as it stands the shifts are jarring at the boundary between Aarik's voice and the journal-conventional-voice that has crept into these subsections.

### 4.2 Where does the paper overclaim past the evidence?

The paper itself is hedged correctly almost everywhere. The two places where the prose comes closest to overclaiming are: (a) the §1.3 "additivity: the specification improves prediction on three of four commercial memory systems" headline. Supermemory's near-zero is technically a "fourth system aggregating slightly negative" rather than a clean fourth-system success, and the headline framing soft-pedals this. The paper does treat Supermemory honestly later (§4.4 deep-dive with the bimodal distribution), but the §1.3 headline is one half-step ahead of where the evidence sits. (b) The §1.4 "the structural implication is direct" sentence is the strongest forward-projection in the paper. The hedging in the surrounding paragraphs (and §5.3 / §5.6) is correct, but this single sentence reads with more confidence than the structural-extrapolation argument supports. A3 violation, mild.

The README's "approximately 99% of real AI users have negligible pretraining representation" is the genuine overclaim in the public artifact. The number is not in the paper, not in DATA_REFERENCE, not anywhere with a citation. It is a heuristic, not a measurement. A3 + A10 violations at the repo level.

### 4.3 Where does the paper bury a self-critical observation that Aarik would normally surface?

The §4.1 coupling-free reframing. This is the paper's strongest A7 moment ("the steep negative slope is largely a coupling artifact of the change-score parameterization") and it sits 60+ lines into §4.1 after the headline number is already imprinted. Aarik's spec predicts he would surface this in §1.3 (or in the headline-numbers callout box) with a forward-pointer to the full sensitivity treatment. As currently placed, the reader reads "−0.96 [95% CI −1.24, −0.67]" multiple times before being told that this slope is dominated by the coupling identity and that the substantive finding is "roughly constant C4a ceiling, lift larger where floor lower." This is the difference between A7 self-critique-up-front and self-critique-after-the-fact. The paper does the second; the spec predicts Aarik would do the first.

### 4.4 Where could the paper compress further without losing argument?

§2.1 to §2.4 by ~30%. §3.7.1 to §3.7.5 by ~50%. §7 Future Work by ~30%. Appendix B and Appendix D have the right level of detail for an appendix and should not be compressed (different rule: A6 governs communication, not archival).

The full-paper test: the body (§1 through §8) plus appendices runs ~1,670 + ~810 = ~2,480 lines. A6 says "outputs that are too dense fail their audience." The paper's audience is researchers, founders, and AI-personalization practitioners; the body alone is at the upper end of what a focused reader will work through. The version that holds at the body level is roughly: §1 hold, §2 compress 30%, §3 compress 30%, §4 hold (earns its length), §5 compress 10%, §6 hold, §7 compress 30%, §8 hold. Result: a paper body roughly 1,200-1,300 lines. That fits the spec's prediction (P6 default-to-shorter) without losing the load-bearing argument.

### 4.5 Where does the paper read as if it values the system over the individual?

The paper as a whole respects A1 AGENCY-AS-ARCHITECTURE. The infrastructure-properties bullet list in §5.5 (user-held, inspectable, provenance-traced, local-executable retrieval) is the strongest A1 artifact in the paper. The §1.4 closing argument ("either each user supplies their own representation, or personalization remains surface-level") is exactly A1 in the paper's own voice.

The one drift: §5.5 dynamic activation is presented as an engineering optimization ("on a typical query, the activated subset would be on the order of 1,000-2,000 tokens rather than the full 8,000-10,000. The per-query cost drops by roughly an order of magnitude"). The user-agency framing is absent here. The paper-favorable phrasing would be: dynamic activation is what makes the user's calibration runnable at production scale on the user's behalf. Currently it reads as "the system selects the components"; the A1 framing would be "the system loads the components on the user's calibration so the user's representation runs efficiently."

### 4.6 Em-dashes, GTM puffery, hype words

The paper passes the em-dash check at the body level. (KEY_FINDINGS line 157 contains an em-dash inside a quoted sentence; that is a repo-orientation file, not the paper.)

The paper passes the GTM-puffery check. No "crushes," no "beats" in the paper body. ("Beats" appears in KEY_FINDINGS line 157 and line 210; both are repo-orientation file violations, not paper violations.) The paper does use "outperforms" (e.g., §4.2 "the specification outperforms the raw source at roughly one-fifth the context size"); this is on the acceptable side of the rule per AGENTS.md ("prefer 'exceeds', 'outperforms'").

The paper passes the hype-word check. "Novel" appears once in §5.1 ("the Behavioral Specification's anchors are surfaced from the subject's corpus"); acceptable. "Groundbreaking" does not appear. "We are excited" does not appear.

### 4.7 Per-user calibration framing

Absent in §5.5 where it would land best. Absent in §7.6 safety where "biased for you" framing would land. Absent in the §1.4 infrastructure-implication paragraph (which is otherwise the strongest A1 paragraph in the paper). The framing "per-user calibration to interact with data and decisions on their behalf" should appear in at least these three places. Currently the paper relies on "user-held," "inspectable," "portable" as the A1-aligned vocabulary; "calibration" is the load-bearing word that does not appear.

The §3.1 "representational accuracy" definition is the technical place where calibration could be named without changing the substance: "representational accuracy is the property of an AI system whose internal model is calibrated to a specific person's interpretive patterns." Currently the section says "how faithfully a model can act in line with a specific person when given a representation of that person," which is correct but does not surface the calibration framing.

---

## 5. Repo Review

### 5.1 README.md

**Story consistency: DRIFTING.** README states Hamerton C5 = 1.25 in the subjects table (line 172). Paper §4.1 table says 1.26. DATA_REFERENCE §1 says 1.26. KEY_FINDINGS M5 cites "Hamerton +1.99 / Ebers +1.96 / Babur +0.75" as the Letta-stateful uplift, while the paper §4.5 table gives +0.14 / +1.05 / +0.54. The two are different metrics (Letta-vs-no-context vs Letta-minus-BL-spec); KEY_FINDINGS labels neither cleanly. README does not reference KEY_FINDINGS' framing of these numbers, so the README internal-only check passes; the cross-doc consistency check does not. A10 violation.

**Framing drift: DRIFTING.** "The Flagship Claim" header is GTM-language by section title alone. The first sentence ("Base Layer is not a memory system. Layered on top of four commercial ones — Mem0, Letta, Zep, Supermemory — it improves all four on the users the model doesn't already know") is the framing-discipline sentence STUDY_MEMORY.md has locked. It is correct as far as it goes but contains an em-dash inside the dash-style sentence ("commercial ones — Mem0, Letta, Zep, Supermemory — it improves"). Em-dash violation at the load-bearing sentence in the public-facing repo entry-point.

**99% claim: MISALIGNED.** README §"The Population That Matters" states "Approximately 99% of real AI users have negligible pretraining representation of their personal behavior." This number is not in the paper. The paper makes a structural-extrapolation argument in §1.4 and §5.3 that is correctly hedged. The README's "99%" is a heuristic, presented as a measurement. A3 + A10 violation.

**Third-party reader test: PARTIAL.** A reader landing cold on the GitHub page reads "The Flagship Claim," "The Claim — Tested, Extrapolated, Not Made," "What This Study Is — And Is Not," "The Population That Matters," and only then "Study Scale" and "Key Findings." The first four blocks are framing claims. P3 says lead with evidence, not conclusions. The README leads with conclusions. A reader who wants to evaluate the work has to scroll past four self-framing sections to get to the data.

**Recommendation:** Tighten README to ~150 lines. Lead with the abstract (or, in v10's case, lead with the three-sentence paper-summary the paper opens with). Move "The Flagship Claim" / "Tested, Extrapolated, Not Made" into a section titled "What this study claims" rather than "The Flagship Claim."

---

### 5.2 ISSUES.md

**Story consistency: ALIGNED.** ISSUES.md is the kind of artifact A7 SYSTEMATIC SELF-GRADING produces. Open P0 / P1 / P2 buckets, each closed item dated and explained. The "P0 — Resolved this session" tables are exactly the per-session log Aarik's spec predicts. Reads as Aarik. The "How this file is maintained" section at the bottom is a small but important piece of process documentation.

**Voice: ALIGNED.** Direct, declarative. No GTM language.

**Recommendation:** None. This file is the strongest public-release artifact in the repo for matching Aarik's voice.

---

### 5.3 AGENTS.md

**Story consistency: ALIGNED.** Lists v10 as canonical, points at DATA_REFERENCE as source of truth, lists the locked decisions (5-judge primary, 7-judge sensitivity, condition-identifier gloss convention, framework for reading raw scores, voice rules). The "What NOT to do" list is the kind of A1 + A7 artifact the spec predicts.

**Voice: ALIGNED.** Direct.

**Recommendation:** None.

---

### 5.4 agents/STUDY_MEMORY.md

**Story consistency: ALIGNED.** Locked constants, primary judge panel decision, analysis plan lock, condition naming, data-integrity verified checks, architectural framing, key numbers (5-judge primary canonical), legacy 7-judge values for sensitivity, memory-system character one-liners, methodology gotchas, known open items, voice-framing-discipline rules. This is the A7 + A10 + A11 artifact.

**Voice: ALIGNED.** "Mistake made + recovered" subsection is the strongest A7 voice in the file: "Early in the session, the editor (Claude) propagated a flawed prior-session research-doc claim that §4.1 used a simpler Haiku-generated spec... Built a 'Hamerton unified rerun' on this premise. When the author pushed back, verified against `run_global_rerun.py:283-285` and confirmed all 14 §4.1 subjects use the full 4-layer spec. The rerun artifacts were wiped from the repo. Lesson captured." This is exactly Aarik's framing: failure named, type identified, fix logged, lesson carried forward.

**Recommendation:** None. The "Hamerton data note (S114)" closing section is the kind of provenance-trail entry that should remain.

---

### 5.5 agents/study-guide.md

**Story consistency: DRIFTING.** Says "9 of 9 on 7-judge; recount on 5-judge primary pending" in the verification table, even though the v10 release-freeze pass closed the recount and DATA_REFERENCE / paper now cite the 5-judge primary 9 of 9 directly. Stale pointer. A10 violation at minor magnitude.

The verification table at lines 134-145 references "DATA_REFERENCE §1" / "§4" / "§7" / "§8" / "§10" / "§12"; these are correct anchor IDs for DATA_REFERENCE.

**Voice: ALIGNED.**

**Recommendation:** Refresh the verification table's "Primary vs sensitivity" column to the v10 5-judge primary numbers (9 of 9 confirmed, slope −0.96, etc.). Currently mixes the pre-recount and post-recount language.

---

### 5.6 docs/DATA_REFERENCE.md

**Story consistency: ALIGNED.** Most authoritative numerical artifact in the repo. Synced 2026-04-24 to v10's 5-judge primary panel. Each section: label, one-line summary, data table, bounded interpretation, paper location. A2 DECOMPOSITION + A10 PROVENANCE + A11 RISK-SEQUENCED. The legacy 7-judge values are kept as sensitivity, not deleted, which is the right A4 EPISTEMIC TIERING move.

**Voice: ALIGNED.** "Bounded interpretation" labels for each section is the kind of self-discipline Aarik's spec predicts.

**Recommendation:** None at the section level.

---

### 5.7 docs/KEY_FINDINGS.md

**Story consistency: DRIFTING.** Hamerton C5 baseline appears as 1.26 in some places (correctly synced to v10) and as 1.25 in M5 (Letta stateful comparison). The M5 "Letta block fed to Haiku: **3.24** (matched response model) / Base Layer full-stack spec fed to Haiku: 3.04 / **Uplift summary across n=3:** Hamerton +1.99 (small, clean), Ebers +1.96 (medium, clean), Babur **+0.75**" cites Letta-vs-baseline numbers (3.24 for Letta, 3.04 for BL, neither of which is the 5-judge primary number; the 5-judge primary in the paper §4.5 is 3.10 vs 2.96).

The "uplift" framing in M5 is also a metric Aarik's spec predicts he would call out. "Letta's uplift" against what baseline? The line uses both "+1.99 vs C5" and "+0.20 vs BL C2a" framings without disambiguating. A10 violation.

**Voice: DRIFTING.** Line 157: "Letta beats Base Layer's spec on all three at matched response model — and Letta's uplift collapses 60% at large corpus scale" contains both "beats" (GTM language flagged in `feedback_no_gtm_language.md`) and an em-dash (flagged in `feedback_no_em_dashes.md`). Voice rule violations on a specific line in a public-release file.

**Recommendation:** Refresh M5 to use the v10 5-judge primary numbers (Letta block 3.10 vs BL spec 2.96 on Hamerton, etc.) consistent with the paper §4.5 table. Replace "beats" with "exceeds" or "outperforms." Remove the em-dash. Disambiguate the "uplift" framing: pick one baseline (vs C5 or vs BL C2a) and stick to it across all three subjects.

---

### 5.8 docs/PROVENANCE_INDEX.md

**Story consistency: DRIFTING.** Header dates: "Generated 2026-04-13. Updated 2026-04-18 (Session 113 — full-stack refresh)." The S113 corrections summary table lists "§4.1.1 Lift (spec − baseline) | +0.55 → +0.67 (all-14 mean Δ facts+spec)"; this is the legacy 7-judge value. The 5-judge primary value (per DATA_REFERENCE and paper) is +0.55. PROVENANCE_INDEX has not been refreshed for v10. A10 violation: the provenance index itself drifts from the source-of-truth numbers it claims to anchor.

The §S115 addendum (referenced in the v10 release-freeze pass) does not appear in the file body in the lines visible. The file does state "see PAPER_CORRECTIONS.md for the full S113 changelog," but the S113 changelog is now superseded by the v10 release-freeze pass numbers.

**Voice: ALIGNED on the file's existing prose.**

**Recommendation:** Refresh PROVENANCE_INDEX to v10 numbers, or add an explicit "this index is anchored to S113 7-judge values; v10 5-judge primary lives in DATA_REFERENCE.md" header at the top. Currently the file silently drifts.

---

### 5.9 REPRODUCE.md

**Story consistency: ALIGNED.** Section 1 (Environment), Section 2 (sensitivity scripts, no API calls required), Section 3 (higher-cost recomputes), Section 4 (Letta rerun), Section 5 (hardcoded-path inventory), Section 6 (number-to-source mapping), Section 7 (what is NOT reproducible offline). Section 5's hardcoded-path-inventory subsection is exactly the A7 + A10 honesty the spec predicts: "approximately 42 scripts under `scripts/` reference `C:/Users/Aarik/Anthropic/...` paths. Most are one-off probes... The exceptions worth flagging: scripts/run_multimodel_responses.py..."

**Voice: ALIGNED.** Direct. The phrase "If you are reproducing the v10 §4.1 result from a fresh clone for a paper-review reason, sections 1, 2, and 5 of this document are sufficient. The rest is provenance" is exactly Aarik's voice.

**Recommendation:** None.

---

### 5.10 requirements.txt

**Story consistency: ALIGNED.** The header comment ("Captured by import-statement audit of scripts/ and docs/research/_letta_rerun/") is the kind of A10 PROVENANCE statement the spec predicts. The note that "provider SDKs that the paper text mentions ... are not directly imported by any committed script in this repository" is honest scope-statement.

**Voice: ALIGNED.** Direct.

**Recommendation:** None.

---

### 5.11 Single highest-impact repo improvement

The numerical drift between README, KEY_FINDINGS, PROVENANCE_INDEX, and the paper itself. README says Hamerton 1.25 where DATA_REFERENCE says 1.26. KEY_FINDINGS M5 cites Letta numbers that don't match the v10 paper §4.5 table. PROVENANCE_INDEX still anchors to S113 7-judge values. A10 PROVENANCE AND TRACEABILITY is the anchor that says outputs must be traceable to their sources, and where the index disagrees with the source-of-truth, the index drifts. A reader auditing the paper's claims by following the repo's traceability chain would hit each of these inconsistencies and lose confidence.

The fix is one focused pass: for each public-facing repo file (README, KEY_FINDINGS, PROVENANCE_INDEX, agents/study-guide.md), grep for every numerical claim, verify against DATA_REFERENCE, update or footnote-as-legacy-value. Roughly 90 minutes of work.

### 5.12 Where do repo docs read as ML-research jargon rather than the user's voice?

KEY_FINDINGS' major-finding entries (M1 through M9) use "Evidence:" / "Paper:" / "Statistical robustness" / "Cross-provider replication" labels that read as a methods-paper extract. The minor findings (m1 through m26) read more in Aarik's voice (e.g., "Information is not what's missing — structure is"), though that example itself contains an em-dash and is a voice-rule violation. The MAJOR / MINOR / OPEN-QUESTIONS structure is correct (A4 EPISTEMIC TIERING). The prose inside each entry reads as more journal-conventional than Aarik would naturally write.

PROVENANCE_INDEX is an index, so prose voice does not apply. The status legend (VERIFIED / APPROXIMATE / NOT FOUND / DERIVED / S113) is the right tiering.

The four agents/-prefixed files (AGENTS.md, STUDY_MEMORY.md, study-guide.md, plus the v10 release-freeze pass report) read closest to Aarik's voice. These are the artifacts where his voice is loudest.

---

## 6. Recommended Sequence

If Aarik adopts every alignment fix in this review, the sequence below groups by effort.

### Trivial (under 30 minutes total)

1. README §"The Population That Matters": remove or hedge the "approximately 99%" claim. Replace with the §1.4 / §5.3 structural-extrapolation language.
2. README §"The Flagship Claim" sentence: replace the em-dashes with commas or restructure into two sentences.
3. KEY_FINDINGS line 157: replace "beats" with "exceeds" and remove the em-dash.
4. agents/study-guide.md verification table: refresh the "Primary vs sensitivity" column to v10 5-judge primary numbers.
5. Hamerton C5 baseline mismatch: README 1.25 → 1.26 (sync to DATA_REFERENCE / paper).

### 30 minutes (single section work)

6. §1.3 Move the §4.1 coupling-free reframing finding into the headline-numbers callout box, with a forward-pointer to the full sensitivity treatment in §4.1. (Currently the strongest A7 self-critique sits 60+ lines into §4.1.)
7. §5.5 Practical implications: add one-line frame at the top introducing "per-user calibration" as the property the implementation choices below realize. Then thread the term into the dynamic-activation, modifiability, temporality, and topic-decomposition subsections.
8. §7.6 Safety: add the "model bias is good, as long as it is biased for you" framing as the affirmative version of the safety question.
9. KEY_FINDINGS M5: refresh to v10 5-judge primary numbers (Letta block 3.10 vs BL spec 2.96 on Hamerton). Disambiguate the "uplift" framing: pick one baseline.
10. PROVENANCE_INDEX header: add explicit note that the file's S113 numbers are legacy, the v10 5-judge primary lives in DATA_REFERENCE.

### Multi-hour (compression and rewriting passes)

11. §2.1 to §2.4: compress per-provider blocks by ~30%. Most of the prose under each provider repeats the table content.
12. §3.7.1 to §3.7.5: compress to ~50% of current length. The §3.7.6 validity audit holds verbatim (it is the section that earns its length).
13. §7 Future Work: compress by ~30% by removing the mechanical "flagged in §X" / "is the [adjective] follow-up" filler.
14. §1.3 / §4.1 Example A / B / C boxes: rewrite the score-explanation prose ("Based on the behavioral specification...") in a more direct register. Currently reads as evaluation-text; should read as Aarik's analysis.
15. Repo numerical-drift sweep: for each public-facing repo file (README, KEY_FINDINGS, PROVENANCE_INDEX, agents/study-guide.md), grep every numerical claim, verify against DATA_REFERENCE, update or footnote-as-legacy.

The trivial fixes plus item 6 (coupling reframing placement) plus item 7 (per-user calibration framing in §5.5) are the highest-yield-per-minute changes. If only one section is rewritten, §5.5 is the section where the biggest framing gain sits.

---

*End of review.*
