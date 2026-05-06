# V9 Triage — Cross-LLM Consensus Synthesis

**Reviewers:** Gemini 2.5 Pro, Gemini 2.5 Flash (truncated), Cerebras Qwen3 235B, Mistral Large, Groq Llama 3.3 70B.
**Source reviews:** `s114_v9_triage_review_20260423_171730.md`, `s114_v9_triage_review_groq_retry.md`
**Triage under review:** `s114_v9_edit_plan.md`

---

## Bottom line

**4 of 5 substantive reviewers say: NOT SAFE TO GREENLIGHT AS-IS, needs minor modifications first.**
**1 of 5 (Cerebras) disagrees with structural decisions B1/B3 — but Cerebras is overriding explicit author requests, so these objections are flagged but do not change the plan.**

The triage is fundamentally sound. Every reviewer agrees on P0-1 through P0-6 (the core rerun queue). The required changes before launch are:

1. **Upgrade P0-6 (derangement control) to Tier 0** — needed before H6 can survive as a headline.
2. **Add 2 new Part 0 items lifted out of Part F** — flagged as scientific-integrity issues, not wording fixes.
3. **Add 2 new Part 0 items from Mistral's reviewer-critique reading** — question-battery category audit + rubric sensitivity on refusals.
4. **H6 caveat plan** — explicit action item to guard the n=1 claim.
5. **Minor additions to Parts A/B** for cross-cutting definitions Mistral identified.

Nothing else needs to change before reruns start.

---

## Consensus matrix — Part 0 Ultra-High-Priority Queue

| Item | Gemini Pro | Cerebras | Mistral | Groq | Consensus |
|------|------------|----------|---------|------|-----------|
| P0-1 Letta full-stack rerun | AGREE | N/A (misread triage) | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-2 Supermemory paid tier | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-3 §4.5 Sonnet/Haiku fact check | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-4 Spec-activation trace | AGREE | N/A | MODIFY (expand to per-tag viz) | AGREE | **AGREE — GREENLIT with Mistral's expand scope** |
| P0-5 Refusal audit | AGREE | N/A | AGREE (add "judge-rubric artifact" category) | AGREE | **AGREE — GREENLIT with 4th category** |
| P0-6 Author derangement | AGREE | N/A | AGREE + UPGRADE to Tier 0 | AGREE | **AGREE — UPGRADE TO TIER 0** |
| P0-7 Spec similarity | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-8 Question × Mechanism | AGREE | N/A | MODIFY (narrow to 9 low-baseline) | AGREE | **AGREE — NARROW SCOPE** |
| P0-9 Baseline-band figure | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-10 Multi-anchor-jump | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |
| P0-11 Repo traceability | AGREE | N/A | DISAGREE (defer post-submission) | AGREE | **DEFER to post-submission** (Mistral rationale accepted — not a v9 blocker) |
| P0-12 Appendix ref audit | AGREE | N/A | AGREE | AGREE | **AGREE — GREENLIT** |

Cerebras produced its own invented P0-1 through P0-12 that didn't match the actual triage — its consensus column is omitted. The valid points Cerebras raised are captured below under "new additions."

---

## New additions required (consensus-driven)

### P0-13 (NEW, Tier 0) — Battery-leakage verification

**Source:** Gemini Pro flagged this as a scientific-integrity issue, not a wording fix.
**Annotation:** §3.4 — *"Can we verify this please"* on the claim that the question-generation prompt "forbids named-entity or specific-date leakage."
**Scope:** Manual audit of 20+ questions, cross-check against held-out windows. Document findings.
**Cost:** ~30 min.
**Blocks:** §3.4 paragraph integrity + the whole backward-design methodology claim.
**Rationale:** If leakage is found, it affects interpretation of all results, not just §3.4 prose. This is not a wording fix — it's a data-integrity check.

### P0-14 (NEW, Tier 1) — Living-user baseline methodology decision

**Source:** Gemini Pro surfaced this from Aarik's §4.1.2 comment.
**Annotation:** *"Really the more interesting baseline is with full facts vs spec w/facts, or memory systems fact vs spec."*
**Scope:** Discussion with Aarik on whether §4.1.2 living-user replication should be reported against a fuller baseline (facts only, memory-system only). If yes, small rerun needed.
**Cost:** ~$5 if rerun needed.
**Blocks:** §4.1.2 final write-up + H6 scope.
**Rationale:** Methodological critique of the baseline used for the living-user experiment. May require a new small rerun to strengthen the n=1 claim.

### P0-15 (NEW, Tier 1) — Question-category audit across batteries

**Source:** Mistral surfaced from Aarik's §4.4 Supermemory limitation comment.
**Annotation:** *"Some subjects' batteries may over-represent literal-recall items"* + Aarik's *"We should do some post hoc analysis on this, may reveal a lot, could enable post hoc data and judging analysis as well."*
**Scope:** Classify each of 586 questions by category (literal-recall, interpretive-inference, refusal-triggering). Cross-tab with spec effect per subject. Haiku classification ~$1.
**Cost:** ~$1, ~1 hr analysis.
**Blocks:** §4.4 Supermemory interpretation + §4.6 recall/interpretation framing + §8 future work shape.
**Rationale:** Addresses concern that the gradient result could be partly an artifact of battery composition. Currently flagged as future work (P0-8) — upgrading to Part 0 because it can be run cheaply and tightens H3/H5 claims.

### P0-16 (NEW, Tier 1) — Rubric sensitivity analysis on refusals

**Source:** Mistral lifted from Aarik's §3.7.6 validity-audit comment.
**Scope:** Recode all spec-induced refusals as neutral (score = 1.0 midway or equivalent) rather than floor anchor (1.0 = "refused or off-base"). Recompute Δ_spec. Report as sensitivity check.
**Cost:** ~0 — pure post-hoc on existing judge scores.
**Blocks:** §3.7.6 validity-audit + §4.4 Pattern 3 interpretation.
**Rationale:** Current rubric lumps honest refusal with wrong prediction. Any conclusion about "spec hurts on refusal-triggering questions" may be rubric artifact rather than real effect. Sensitivity analysis tests this.

### P0-17 (NEW, Tier 1) — Judge floor-testing diagnostic

**Source:** Cerebras + Groq flagged. From Aarik's §2.5 annotation: *"We didn't do any floor testing as well?"*
**Scope:** Add a floor-testing diagnostic (verbatim-wrong response scored against held-out) to the judge calibration suite. Currently have ceiling, paraphrase-sensitivity, length-bias. Floor is missing.
**Cost:** ~$2, ~20 min.
**Blocks:** §2.5 completeness + judge-calibration credibility.
**Rationale:** Methodological gap in calibration. Author flagged it explicitly. Fixes a latent reviewer objection to the judge panel.

---

## Headline findings — consensus on the E list

| Finding | Action |
|---------|--------|
| H1 Hedging collapses | GREENLIT. Mistral suggests adding robustness note ("robust to judge panel composition, §4.5.2"). |
| H2 The gradient | GREENLIT. Mistral suggests scoping to "historical subjects" until P0-6 confirms for living user. |
| H3 70.9% of questions improve | GREENLIT. Mistral suggests footnote with median magnitude. |
| H4 Compression wins | GREENLIT. Mistral suggests surfacing the 10× token ratio explicitly. |
| H5 Spec composes additively | MODIFY. Clarify Supermemory masking; Mistral's phrasing accepted. |
| H6 None of 40 responses worse | **MAJOR CAVEAT REQUIRED.** 3/4 reviewers flagged as dangerous over-claim. Add explicit n=1 caveat and pair with P0-6 derangement result before it can appear in abstract/blog/outreach. |
| H7 Spec is traceable (audit trail) | GREENLIT. P0-4 deepens this. |
| H8 Spec-induced refusal = epistemic integrity | GREENLIT. Mistral suggests scoping to "epistemically honest refusals." |
| H9 Content, not format | GREENLIT. Mistral suggests adding the derangement Δ = −0.25. |

### Proposed new headline from consensus:

**H10 (Mistral) — Detection asymmetry.** *"The model detects mismatches between named subjects and anonymized specs, revealing an ability to compare interpretive content to biographical context."* (From §4.3 wrong-spec where model said "This is a behavioral model of a 16th-century Central Asian military ruler, almost certainly Babur.")

**Recommendation:** Promote to H10. Aarik's own annotation on this was *"major finding IMO"*, consistent with headline status.

---

## Structural decisions — consensus on Part B

| Decision | Gemini Pro | Cerebras | Mistral | Groq | Verdict |
|----------|------------|----------|---------|------|---------|
| B1 Results reorg (§4.5 end, §4.6/§4.7 fold, §4.8 out) | AGREE | DISAGREE | MODIFY | (not reviewed) | **APPLY WITH MISTRAL MODIFICATION:** keep §4.5 Robustness as a standalone section (not buried at end); move §4.8 Scaling to new §5.5 Practical Implications (not Future Work). Cerebras' disagreement overrides Aarik's explicit requests — discarded. |
| B2 §7 Safety → §5 Discussion | AGREE | (not reviewed) | AGREE (fold as §5.4) | (not reviewed) | **APPLY** |
| B3 §2 vs §5 split | AGREE | DISAGREE | MODIFY | (not reviewed) | **APPLY WITH MISTRAL MODIFICATION:** move benchmark comparisons (Twin-2K, LoCoMo) to §2 but KEEP anti-pattern framing and open questions in §5 as forward-looking content. |
| B4 §2 internal order | AGREE | (not reviewed) | AGREE | (not reviewed) | **APPLY** |
| B5 §3.2 ↔ §3.2.1 collapse | AGREE | (not reviewed) | AGREE | (not reviewed) | **APPLY** |
| B6 §2.1 list vs table | AGREE | (not reviewed) | AGREE (keep table) | (not reviewed) | **APPLY — keep table, drop prose** |
| B7 §3.5 conditions table | AGREE | (not reviewed) | AGREE | (not reviewed) | **APPLY** |
| B8 Judge/response-model table | AGREE | (not reviewed) | AGREE | (not reviewed) | **APPLY** |

### New B-items consensus wants added:

- **B9 (Mistral) — §4.3 new Hedging Behavior subsection.** *"Add new subsection §4.3.x: Hedging Behavior: An Open Question to discuss detection asymmetry and refusal mechanisms."* Consolidates scattered hedging observations into one dedicated treatment. **ADOPT.**
- **B10 (Mistral) — §5.1 The Anti-Pattern: What Behavioral Specification Is Not.** Explicitly define the anti-pattern (not recall, not persona fidelity, not preference alignment). Addresses Aarik's §5 request: *"define the anti-pattern that is the spec."* **ADOPT.**

### Cerebras' B1/B3 disagreements — rejected, noted

Cerebras argues §4.5 should stay before performance results (causal logic) and §1.5 should stay in intro (framing, not discussion). Both objections contradict Aarik's explicit Word comments that requested these moves. Cerebras is overriding author intent based on theoretical priors. **Rejected.** Documented here in case Aarik wants to reconsider.

---

## Cross-cutting additions to Part A

Mistral identified 3 definition sweeps that weren't in Part A:

- **A12 — Define "behavioral prediction"** on first use. Aarik §1.1 comment: *"Behavioral prediction as a proxy is lightly covered... would expect a bit more insights/definitions."*
- **A13 — Define "neural-memory-analogue systems"** on first use in §2.1. Aarik: *"brain-based memory systems, vs cognitive sciences."*
- **A14 — Define "real AI user"** on first use in §1.3/§1.4. Currently vague per Aarik. Replace with "a living person whose private reasoning is not in any LLM training corpus."

**All three adopted.**

---

## Missing annotations (final check)

Gemini Pro: *"The editor has successfully captured every one of the 233 annotations."*

Mistral claimed 5 missed annotations. On audit:
- §1.1 behavioral prediction proxy — captured in Part F §1 as "§1.1 'used here as a proxy for this alignment'" → promoted to A12 (addressed).
- §1.3 category-level change — captured in Part F §1 as "§1.3 'category-level change' claim" (addressed).
- §2.1 brain-based — captured partially in Part F §2 "memory-like / cognitive categories" → promoted to A13 (addressed).
- §3.3 brief composition — captured in Part F §4 at "§4.3 'almost certainly Babur' example" → already scheduled as §3.3 paragraph addition.
- §4.3 Hedging Behavior subsection — NEW, adopted as B9.

Cerebras claimed 5 missing:
- §3.0 "two intertwined but separable halves" — captured in Part F §3 "§3 'two intertwined but separable halves'".
- §3.3 "canonicalizes" — captured in Part A as A6.
- §3.3 word count — captured in Part F §3 "§3.3 '5,000-8,000 tokens'".
- §2.5 floor testing — promoted to P0-17.
- §1.1 proxy — A12.

**Net result:** All 233 annotations captured. 3 definitions promoted to A12-A14, 1 subsection added as B9, 1 discussion-tone section added as B10, 1 floor-test promoted to P0-17.

---

## Revised priority order (consensus-approved)

### Tier 0 — Greenlight immediately on Aarik's approval:

1. **P0-1 Letta stateful-agent full-stack rerun** ($10-20, 1-2 hrs) — Critical path. §4.7 unwritable without this.
2. **P0-2 Supermemory paid-tier ingestion for 4 failures** ($5-10, 30-60 min) — Data completeness.
3. **P0-3 §4.5 Sonnet/Haiku fact check** (~10 min) — Trivial, high impact.
4. **P0-6 Author derangement control** ($5, ~20 min + judge) — **Upgraded from Tier 1.** Guards H6.
5. **P0-13 Battery-leakage verification** (~30 min) — Scientific integrity.

### Tier 1 — Parallel once Tier 0 launches:

6. **P0-4 Spec-activation / tag-citation per-response trace** (~1 hr, no API) — H7 + §4.3.
7. **P0-5 Spec-induced refusal audit across 5 substrates** (~$2, 1-2 hrs) — H8 + §7.
8. **P0-7 Pairwise spec-similarity across 14 subjects** (~30 min, no API) — §4.3 + §4.1.2.
9. **P0-8 Question × Mechanism cross-tab** (scope-narrowed to 9 low-baseline subjects; ~$1, 1-2 hrs).
10. **P0-14 Living-user baseline discussion** — decide with Aarik before committing.
11. **P0-15 Question-category audit across all batteries** (~$1, 1 hr).
12. **P0-16 Rubric sensitivity on refusals** (~0, ~30 min analysis).
13. **P0-17 Judge floor-testing diagnostic** (~$2, ~20 min).

### Tier 2 — After Tier 0/1 data lands:

14. **P0-9 Baseline-band figure** for §3.2.
15. **P0-10 Multi-anchor-jump figure** for §4.1.
16. **P0-12 Appendix reference audit** — reviewer usability.

### Deferred (post-submission):

- **P0-11 Repo traceability matrix.** Mistral: defer. Agreed.

### Total: ~$25-45, ~6-8 hrs compute, ~8-10 hrs analysis.

---

## H6 guarding plan (required before launch)

Both Gemini Pro and Mistral flagged H6 as the single biggest over-claim risk. Plan:

1. Before running P0-6 (derangement), update abstract/blog drafts to strip or heavily caveat "none of the 40 responses got worse."
2. After P0-6 lands, rewrite H6 as: *"In the single living-user replication (n=1), the specification improved 40/40 responses relative to no-context baseline. A random-derangement control [P0-6 result] suggests the effect [is/is not] explained primarily by baseline-mediated improvement alone."*
3. Living-user replication should be framed as **pilot**, not as confirmation of the universal-coverage claim.
4. Any external use (blog, outreach, social) must include the n=1 caveat in the same breath as the finding.

---

## What changes in the triage file

All of the above will be merged into `s114_v9_edit_plan.md` now so the master plan reflects consensus. Specifically:

- Part 0 gets P0-13 through P0-17 appended.
- P0-6 moves up to Tier 0.
- P0-11 moves to a "Deferred" tier.
- Part A gets A12/A13/A14 appended.
- Part B gets B1/B3 "applied-with-modification" notes and B9/B10 appended.
- Part E gets H6 guarding plan + H10 proposed.

Once done, Aarik can greenlight Tier 0 runs.
