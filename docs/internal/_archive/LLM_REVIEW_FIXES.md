# LLM Review Fixes -- All Models (S110, 2026-04-14 → S113, 2026-04-18)

Consolidated tracker for all feedback from LLM reviewers across all rounds.

---

## Review Sources

| Model | Round | Verdict | Key Concern |
|---|---|---|---|
| DeepSeek (adversarial) | S110 | v3 product launch doc | Repos 404, undeclared COI, synthetic-only evaluation, historical subjects only |
| Gemini Flash | R1 (S109) | A- | No human evaluation, circular LLM-judging-LLM |
| Cerebras Qwen3 235B | R1 (S109) | Major revision | % calculation misleading, Cohen's d misuse, no aggregate stats |
| Mistral Large | R1 (S109) | Not ready | Historical texts != real users, post-hoc not prediction, statistical overreach |
| Groq Llama 3.3 | R1 (S109) | FAILED | 413 payload too large (needs truncation to ~30k chars) |
| Gemini Pro | R1 (S109) | FAILED | 503 service unavailable |
| DeepSeek | S110 | Solid paper, real contribution | "Unknown" framing, effect size honesty, spec stability, hedging precision |
| GPT-5.4 | S110 (plan review) | Ready to execute | Prompt harmonization, aggregation rule, battery methodology |
| Gemini Flash | S110 (plan review) | Exceptionally robust | -- |
| Mistral Large | S110 (plan review) | Ready to execute | -- |
| Gemini 2.5 Flash | R2 (S113) | Substantially improved (truncated ~1.2K chars) | Repositioning lands honestly |
| Gemini 2.5 Pro | R2 (S113) | Strong; requires substantial revision | Circularity of C5 baseline; Letta comparison incomplete (n=1 vs 14-subject archival) |
| Cerebras Qwen3 235B | R2 (S113, focused payload) | Honest, transparent — no critical issues in focus sections | §5.7 "Zep is the most consistent performer" overclaims without "in this study" |
| Mistral Large | R2 (S113) | Ready with revisions | Circularity; Letta scope; Supermemory ceiling vs. architectural-incompat; extrapolation to living users |
| Groq Llama 3.3 70B | R2 (S113, minimal payload) | Well-argued; needs generalization tests | Framing honest; needs more testing beyond historical figures |

---

## FIXES APPLIED (S110)

### From Cerebras Qwen3 (R1)
- [x] Percentage calculation clarified -- added absolute gains + normalized baseline column to Table 4.4
- [x] Cohen's d caveat added (ordinal/bounded data, directional indicator only)
- [x] Calibration language fixed ("normalized scoring" → "calibrated cross-provider comparison")
- [x] Score interpretation paragraph added explaining what 1→2.7 means qualitatively

### From Mistral Large (R1)
- [x] "Every real user is unknown" scoped to "vast majority" 
- [x] Hedging metric made prominent (Section 5.5)
- [x] Historical texts acknowledged as proxy, not equivalent to real user data (Limitation #7)

### From Gemini Flash (R1)
- [x] "Facts themselves never mattered" → "facts alone are insufficient" (Abstract)
- [x] "Presumably due to pre-training" → "consistent with stronger representation" (Abstract)

### From DeepSeek (S110)
- [x] "Unknown" → "low pretraining representation" (6 locations throughout paper)
- [x] Sign test condition pairing clarified (C3 = spec+Mem0 vs C1 = Mem0 alone)
- [x] Wrong spec subject specified (Franklin's spec applied to Hamerton)
- [x] Franklin framing: "provides for private individuals what pretraining provides for public figures"

### From GPT-5.4 (S110 plan review)
- [x] Hamerton C5/C4 prompt harmonization (Phase 0 -- rerun with generic prompts)
- [x] Aggregation rule locked (mean per judge across questions, then mean across judges, N=14)
- [x] Battery generation methodology matched to Hamerton exactly (Haiku, same prompt template)

### From Aarik's Review (80 comments, S110)
- [x] Thesis moved to sentence 1 of Introduction
- [x] Full conditions table added (Section 3.5)
- [x] Battery generation methodology explained (backward design)
- [x] Pipeline overview replaced with structured table
- [x] Judge calibration moved to Study Design (Section 3.7)
- [x] Response models as structured table
- [x] Results intro with hypothesis statement
- [x] AlpsBench given proper treatment
- [x] Memory system improvements as table
- [x] Prediction example with full fields (false positive, directive)
- [x] Em dashes removed (27 instances)
- [x] Spec failure analysis added (Section 5.4)
- [x] Threshold analysis explained
- [x] Future work expanded (layer ablation, diff daemon, private tests)
- [x] Specification stability tested (45% exact, semantically stable)

---

## REMAINING -- IMPLEMENT NOW (no input needed)

### From R1 reviewers (all three flagged)
- [ ] No human evaluation -- acknowledged in limitations, calibration mitigates. Add: "Human validation of a subset of judgments is planned." **STATUS: Added to limitation #5.**
- [ ] Spec component ablation -- which layer drives the gain? **STATUS: Added to Future Work.**

### From DeepSeek
- [ ] Hedging claim: distinguish refusals (score=1 "refuses") from incorrect predictions (score=1 "off-base"). Re-examine score=1 data to separate these.
- [ ] Per-question variance analysis by category (decisions, values, etc.). Add to Phase 4 analysis code.
- [ ] Spec stability downstream: run extraction twice, compose both, diff the resulting specs.
- [ ] Abstract too long (350+ words). Trim after numbers finalize.
- [ ] Consider Cliff's delta instead of Cohen's d (ordinal-appropriate effect size).

### From Cerebras (R1)
- [ ] No statistical testing across 14 subjects. **STATUS: Wilcoxon in Phase 4 analysis code, runs after rerun.**
- [ ] Missing cultural bias discussion in predicate design. Add note that predicates were developed across 50+ subjects.

### From Mistral (R1)
- [ ] Question battery circularity (same model generates battery and spec). Acknowledge as limitation.
- [ ] "Prediction" framing -- technically post-hoc pattern matching. Add explicit acknowledgment.

---

## REMAINING -- NEEDS AARIK INPUT

| Item | Source | Question |
|---|---|---|
| Title uniqueness | DeepSeek | "Beyond Recall" already used by other papers. Alternatives? |
| C4 -- behavioral models in intro | Aarik | How early to introduce? (Decided: not needed) |
| C10 -- durability claim | Aarik | Hedge or remove? |
| C11 -- "thrown in" passage | Aarik | Can't identify without re-reading |
| C21 -- subsections 1.1/1.2 | Aarik | Keep, merge, or cut? |
| C41 -- confidence weights | Aarik | Justify or flag heuristic? (Decided: weighted combination, no %) |
| C79 -- percentage display | Aarik | Lead with absolute gains? (Partially addressed with interpretation paragraph) |

---

## APPLIED (reference audit, S110 late)

- [x] REF-18 (PersonaX, Shi et al.) removed -- was in references but never cited in body
- [x] Citation style standardized to author-year throughout (removed bracket [1]-[5] from Related Work)
- [x] Acknowledgments + funding statement added ("self-funded, no external support")
- [x] Disclosure statement added at top of paper
- [x] Study repo pushed to GitHub (private, public on launch day)

## NOTED FOR WEDNESDAY (from reference audit + adversarial review + Baordy feedback)

### From Baordy (external advisor)
- [ ] Generate GPT-5.4 batteries for ALL 13 subjects (cheap, fast). Compare qualitatively against Haiku batteries (difficulty, framing, category coverage). Report in paper as robustness check. Full rerun with GPT-5.4 batteries available for v2 if reviewers insist.
- [ ] Move hedging reduction finding (51%→31%) into abstract
- [ ] Verify 68% overlap stat is prominent in intro (already moved, check placement)
- [ ] Prep answers for three likely questions: cold start threshold, real-time updates, moat vs frontier labs
- [ ] Blog + README should lead with results, not methodology (different order than paper)

- [ ] REF-14 author verification -- body says "Du et al." but REFERENCE_TABLE noted original lead author may differ. Verify arXiv:2510.05381.
- [ ] Embed figures 5-9 in paper (generated but only 1-4 are in markdown)
- [ ] Abstract still has old numbers -- update after rerun Phase 4
- [ ] 37 markdown tables -- consider converting some to figures for readability
- [ ] 68% retrieval disagreement is single-subject (Hamerton) -- scope the claim or replicate
- [ ] "Missing primitive" rhetoric -- consider "a missing primitive" (DeepSeek + adversarial both flagged)
- [ ] Question battery circularity (same model generates battery and spec) -- acknowledge as limitation
- [ ] "Prediction" framing -- technically post-hoc pattern matching -- add acknowledgment
- [ ] Main BaseLayer repo needs updates for launch (see docs/MAIN_REPO_UPDATES_NEEDED.md)
- [ ] Add Apache 2.0 LICENSE file to study repo before going public

---

## REMAINING -- WAIT FOR DATA

| Item | Source | Depends On |
|---|---|---|
| All Table 4.4 numbers | Rerun | Phase 2-4 completion |
| Wilcoxon signed-rank p-value | Rerun | Phase 4 analysis |
| Krippendorff's alpha | Rerun | Phase 4 analysis |
| Abstract percentages | Rerun | Final numbers |
| C31 -- corpus split verification | Aarik | Check Hamerton chapter structure |
| C57 -- Franklin still relevant | Rerun | Confirm after updated experiment |
| C99 -- cost re-evaluation | Rerun | Final API costs |

---

## REQUIRES EXPANDED EXPERIMENT (Future Work)

| Item | Source | What's Needed |
|---|---|---|
| Human evaluation | All R1 reviewers + DeepSeek | Human annotators scoring a subset |
| Spec component ablation | Cerebras + Mistral | Anchors-only, core-only, predictions-only conditions |
| Alternative compression baseline | Mistral | Compare spec to 5K-token summary (non-behavioral) |
| Multiple comparisons correction | Mistral | Bonferroni or FDR on 14 subjects x 5 conditions |
| Temporal/novel scenario test | Mistral | Held-out chapters = same autobiography; truly novel scenarios untested |
| Question battery independence | Mistral | Use different LLM to generate battery |
| Adversarial robustness | DeepSeek + Cerebras | Insert fake behavioral pattern, test if spec picks it up |

---

## LAUNCH-DAY REQUIREMENTS (from adversarial DeepSeek review)

### 1. Make repos public
- `agulaya24/BaseLayer` -- currently public, confirm all study scripts included
- `agulaya24/memory-study-repo` -- NOT YET A GIT REPO. Must: git init, push, make public
- Both must be live before paper goes out. Every "public repository" claim in the paper depends on this.

### 2. Add conflict of interest disclosure to paper
- Aarik is founder of BaseLayer.ai. The paper validates the product's pipeline.
- Add to paper: "Disclosure: The first author is the founder of Base Layer, which provides an open-source implementation of the pipeline described in this paper. All data, code, and evaluation artifacts are released under Apache 2.0 to enable independent verification."
- This is standard for applied ML research. Not disclosing looks worse than disclosing.

### 3. Hedging: 68% retrieval disagreement is single-subject
- Currently presented as a general finding but comes from Hamerton only (462 facts)
- Either: replicate on global subjects in the rerun, or clearly scope the claim to Hamerton

---

## Adversarial Review Triage (DeepSeek harsh review)

**Already addressed:**
- "Unknown" framing → changed to "low pretraining representation"
- Effect size inflation → score interpretation paragraph added
- Cohen's d caveat → noted as directional indicator
- Spec stability → tested (45% exact, semantically stable)
- Wrong spec subject → specified (Franklin's spec on Hamerton)
- Pipeline contamination → multi-model validation (6 models, 3 providers)

**Valid but acknowledged in limitations:**
- No human evaluation (limitation #5)
- Historical figures only (limitation #7)
- Single primary response model (limitation #3, reworded)
- LLM-only evaluation circularity (limitation #5)

**Valid and needs action:**
- COI disclosure (add before launch)
- Repos public (launch-day task)
- 68% retrieval disagreement scoping (single-subject caveat needed)
- "Missing primitive" rhetoric (consider softening to "a missing primitive")

**Rejected / disagree:**
- "Product whitepaper" characterization -- the study has negative controls, calibration framework, multi-provider validation, and 14 subjects. That's more rigorous than most applied ML papers. The commercial connection is real but doesn't invalidate the methodology.
- "Context rot may be prompt engineering" -- we cite two independent papers (Hong 2025, Du 2025) confirming this is a real phenomenon across 18 frontier models.

---

## Venue Recommendations (from DeepSeek)
- **CHI** (human-AI interaction)
- **IUI** (personalization)
- **EMNLP** (memory systems)
- "Too applied for ICML/NeurIPS, too narrowly focused for ACL"

---

## ROUND 2 (S113, 2026-04-18) — against v6 draft

Four substantive reviews returned. Primary file: `docs/reviews/round_02_20260418_150505.md`. See `docs/reviews/README.md` for the full review index.

### Round 2 focus questions
1. Does §4.4 (Base Layer open-source retrieval floor) land honestly, or read as defensive / COI-motivated?
2. Does §5.7 ("First Benchmark on an Axis the Category Wasn't Optimized For") come across as a fair referee or biased?
3. Is the abstract's 3-claim disaggregation (tested / extrapolated / NOT claimed) clear?
4. Is §4.3.1 Letta stateful-agent parity result (n=1) handled with appropriate humility?
5. Any overclaiming elsewhere?

### Consensus across reviewers
- **§4.4, §5.7, abstract disaggregation:** All four reviewers (Pro, Mistral, Cerebras, Groq) judge the repositioning as honest/fair/clear. No fixes needed on these three focus questions.
- **§4.3.1 Letta n=1:** All four agree the result is handled with humility. No fixes.

### Critical issues flagged (Round 2)

| Reviewer | Issue | Category | Action |
|---|---|---|---|
| Gemini Pro, Mistral Large | **C5-as-pretraining-proxy circularity.** The gradient (spec helps most when C5 is low) uses the same response-model + judge pipeline to measure both the independent and dependent variable. Could be partially regression-to-the-mean. | (b) requires expanded experiment — independent pretraining proxy (n-gram frequency, memorization probes) | **Honest acknowledgment in Limitation #12 added; deferred to Future Work §7. Paper already flags this.** |
| Gemini Pro, Mistral Large | **Letta stateful-agent test is n=1 (Hamerton only); main Table 4.3 uses misconfigured archival path.** Conclusion of "architectural convergence" rests on single subject. | (b) requires expanded experiment — 14-subject stateful-agent replication | **Flagged in §5.10 Open Questions + §7 Future Work as "the single most important follow-up for memory-system comparison." Paper is explicit.** |
| Gemini Pro | **Missing: proper ablation of spec components** (anchors / core / predictions / unified brief). | (b) requires expanded experiment | **Flagged in Limitations #13 + §7 Future Work.** |
| Gemini Pro, Mistral Large | **Missing: human-in-the-loop validation** of LLM-judge scores. | (b) requires expanded experiment | **Flagged in Limitation #1 + §7 Future Work. Calibration framework partially mitigates.** |
| Gemini Pro | **Methodology: Gemini judges should be sensitivity analysis, not primary.** 7-judge panel includes known inflators. | (a) fixable now — or (c) stylistic | **PARTIALLY APPLIED.** §4.1.2 now presents both 7-judge and non-Gemini 5-judge; Wilcoxon on both. Locked aggregation rule keeps 7-judge as primary for transparency (disclosed in §3.7). Not changed because changing the primary mid-audit would break the locked analysis plan. |

### (a) Fixable items applied to v6

| Item | Reviewer | Status |
|---|---|---|
| §5.7 "Zep is the most consistent performer in our data" — hedge with "in this study / on this task" | Cerebras, Mistral | **TO-DO** — small hedge, apply before launch |
| §1.4 title "Why the Gradient Implies Universal Utility" — "Universal" overclaims | Gemini Pro | **TO-DO** — retitle to "Why the Gradient Implies Broad Utility for Real Users" (already done in v6? verify) — **confirmed done at line 298** |
| §8 conclusion "recall is solved" — oversimplifies | Gemini Pro | **TO-DO** — soften to "performance on established recall benchmarks has plateaued" |
| §5.2 / §1.4 extrapolation framing — "should generalize" reads too confidently | Mistral | **LARGELY DONE** — v6 already has 3-claim abstract disaggregation and §1.5 hedge. Check §5.2 language. |
| §5.8 personal tone ("I am glad Letta is doing this work") — unconventional for research paper | Gemini Pro, Cerebras, Mistral | **DEFERRED** — Aarik explicit editorial choice (voice bank). Not changed. |
| Future-date "April 2026" | Gemini Pro | **NO-OP** — paper is dated April 2026 because submission is April 2026 (S113 clock). Not a bug. |
| §4.3 "ebers" lowercase / "Letta is the most architecturally ambitious" subjective phrasing / §4.3.1 "Run A native" unclear | Cerebras (minor) | **TO-DO** — one-pass copyedit before launch |
| §4.3 "native vs. controlled" confusing; add table summarizing the two | Mistral (minor) | **ALREADY IN §3.5** — verify cross-ref |
| §4.1.3 + §4.5 quantify bimodal wrong-spec mechanism with histogram | Mistral (minor) | (b) requires expanded experiment — deferred |

### (b) Requires expanded experiment — logged in Future Work

All logged to paper §7 Future Work and/or Limitations §6:
- Independent pretraining proxy (n-gram frequency, memorization probes)
- 14-subject Letta stateful-agent replication
- Spec component ablation (anchors / core / predictions / brief)
- Human judge validation
- Temporal drift testing
- Adversarial robustness testing
- Cross-family extraction/authoring pipeline
- Cold-start minimum corpus scaling
- Integration with provider-native memory (ChatGPT/Claude/Gemini)
- Hedging-vs-accuracy decomposition
- Cross-provider pretraining variance explanation
- Supermemory architectural-overlap hypothesis test

### (c) Stylistic-only — not applied

- §5.8 first-person narrative (Aarik editorial choice)
- Paper length / density (will consider for v2 / camera-ready)
- Terminology conflation "representational accuracy" ↔ "behavioral prediction accuracy" (paper defines the former as operationalized by the latter — minor clarification pass acceptable but not load-bearing)

### Round 2 exit criteria

All four substantive reviewers judge the paper as either ready-with-revisions or substantively revised-and-strong on the primary positioning questions. No (a) items remain that block launch. All (b) items are category "requires expanded experiment" and are logged in Future Work per protocol. Recursive review loop exits per protocol.

**Paper is ready for Tuesday 2026-04-21 launch pending:** Aarik's voice pass + the three (a) to-do items above (S5.7 Zep hedge, §8 "recall is solved" softening, §4.3 copyedit).
