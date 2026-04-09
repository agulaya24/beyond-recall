# LLM Review Fixes -- All Models (S110, 2026-04-14)

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
