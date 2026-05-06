# Beyond Recall v9 — Pre-Final Cross-LLM Review Synthesis

_Generated: 20260423, session S114_
_Raw source: `s114_v9_prefinal_raw_20260423_221318.md`_
_Paper: `docs/beyond_recall_v9_draft.md` (335,889 chars, ~84K tokens)_

## Scope

Four reviewers: Gemini 2.5 Pro (full paper), Mistral Large (full paper), Cerebras Qwen3 235B (first 40k chars), Groq Llama 3.3 70B (first 18k chars). The two full-paper reviewers carry the most weight on whole-paper flow; the two truncated reviewers carry weight on abstract / §1 / early §2-§3 material.

**Note on bias trap:** Fukuzawa Q26 4.20-vs-4.33 was pre-disclosed in the review prompt; counting it as a "4-reviewer catch" would be double-counting. Flagging confirmed, not independently discovered. All other consensus items below are clean.

---

## Per-Reviewer Verdict

| Reviewer | Verdict | Tone |
|---|---|---|
| Gemini 2.5 Pro | READY-WITH-MINOR-FIXES | Core claims robust and well-defended; fixes are flow + one numeric. |
| Mistral Large | READY-WITH-MINOR-FIXES | Structurally sound and ready for arXiv; targeted fixes in §4.4 and §5.1. |
| Cerebras Qwen3 235B | READY-WITH-MINOR-FIXES | Methodologically sound and logically consistent; flagged 4 numerical inconsistencies in §1.3. |
| Groq Llama 3.3 70B | READY-WITH-MINOR-FIXES | Well-structured and clear argument; minor flow + Wilcoxon context. |

**Unanimous:** READY-WITH-MINOR-FIXES. Zero CRITICAL issues. Zero NEEDS-REVISION. No reviewer demanded new experiments or structural rewrites.

---

## Issues by Severity

### CRITICAL
**None.** All four reviewers explicitly returned "None" for critical issues.

### NEEDS_FIX (numerical / logical inconsistencies to resolve before arXiv)

1. **[3 reviewers flagged] §1.3 vs body numerical mismatches.** Cerebras flagged the most specific set; Mistral corroborated two; Gemini Pro corroborated one. Author should do a sweep of every number in §1.3 against its source in §4:
    - **Cerebras:** §1.3 wrong-spec Δ = +0.22; §4.3 reports +0.18. Fix §1.3 to match §4.3.
    - **Cerebras + Mistral:** §1.3 Supermemory low-baseline Δ = -0.01; §4.4 subsection value = -0.02. Reconcile to two decimals. Mistral adds: text says "-0.01" but adjacent table says "-0.05" for all-14; verify which configuration (controlled vs. native) §1.3 is citing and clarify.
    - **Gemini Pro:** §1.3 says Supermemory aggregate Δ = -0.05 (full 14) and -0.01 (low-baseline); §4.4.1 confirms. But native configuration shows -0.01 (full) and -0.03 (low-baseline). §1.3 should state which configuration it is quoting.

2. **[pre-disclosed, 4 reviewers confirmed] Fukuzawa Q26 reported as 4.20 in body vs 4.33 from audit recompute.** Cerebras additionally noticed the same pattern may appear for Sunity Devee Q35 (4.33 in §1.3 vs 4.20 in §4.2.1) — please verify this second instance during read-through, as it may indicate a systematic swap between body and summary.

3. **[1 reviewer, Cerebras] §1.3 "5 of 6 cells reproduce the specification direction"** phrasing is self-undermining. The one "non-reproducing" cell (Zitkala-Sa × Gemini Pro) is actually consistent with the gradient mechanism, not a failure. Rephrase to avoid implying a replication failure. Cerebras suggested: "All 6 cells follow the expected pattern, with one (Zitkala-Sa × Gemini Pro) aligning with the gradient mechanism."

4. **[1 reviewer, Mistral] §4.5 Letta block size: body says 335,349 chars; other claims say 333K ceiling.** Clarify the distinction between measured block size and the API ceiling.

### NEEDS_FIX (flow / restructure)

5. **[3 reviewers flagged — consensus] §4.4 internal ordering feels disjointed.** Gemini Pro, Cerebras, and Mistral independently flagged that the Aggregate → Mechanisms → Keckley subsection structure reads as "aggregate stats, then deep-dive one system, then generalize, then another case study." Three specific suggestions converged:
    - Move Supermemory deep-dive into §4.4.2 (Mechanisms) so it *introduces* the three mechanisms rather than standing alone.
    - Add a bridge sentence into §4.4.2 linking Patterns 1-3 back to the §4.4.1 examples (Mistral: "These three mechanisms — pattern supply, over-theorization, and principled refusal — generate the per-question swings that cancel at the aggregate.")
    - Consider whether §4.4.3 Keckley should fold into §4.4.2 as the capstone example for Pattern 3 (Principled Refusal), rather than standing as its own subsection (Gemini Pro).

    Recommendation for author read-through: read §4.4 end-to-end and decide if the Supermemory analysis should be restructured as the lead example inside §4.4.2 rather than between the aggregate and the mechanisms sections.

6. **[2 reviewers flagged] §4.4 → §4.5 transition is abrupt.** Gemini Pro and Groq both flagged. One-sentence bridge recommended. Gemini Pro offered: "While the Keckley case demonstrates a specification-level dynamic common across retrieval-based systems, one system in our study offers a fundamentally different architectural path..."

7. **[2 reviewers flagged] §5.1 Anti-Pattern opens abruptly.** Cerebras and Mistral flagged. One-sentence lead-in recommended. Cerebras offered: "Before turning to implications, we pause to name a recurring failure mode observed across conditions: the conflation of recall sufficiency with representational adequacy."

8. **[1 reviewer, Mistral] §5.1 "It is not survey-response prediction" bullet misstates Twin-2K's task.** Mistral suggests revising to: "It is not survey-response interpolation. Twin-2K predicts held-out Likert responses from other survey responses; our battery predicts open-ended behavior on unseen autobiographical passages."

9. **[1 reviewer, Cerebras] §5.5 Practical Implications overlaps with §1.4.** Reframe §5.5 around infrastructure (portable specs, versioning, audit trails, API contracts), leaving §1.4 as the user-benefit extrapolation. This preserves both without redundancy.

10. **[1 reviewer, Cerebras] §5.7 Safety transition from §5.6 is missing a connective sentence.** Suggested: "While behavioral alignment is not a safety property, it interacts critically with safety, especially when personalization amplifies user intent."

### NICE_TO_HAVE

- **[Gemini Pro] Add explicit figure reference for the gradient plot in §4.1** — the regression is described in prose but no "(Figure 4.1)" call-out appears.
- **[Gemini Pro] Add a small table for the N=1 author-derangement result in §4.1.2** to make the C5 / three wrong-spec / correct-spec comparison scannable.
- **[Mistral] Add forward pointer from §4.4.3 (Keckley) to §5.7 (Safety)** — the refusal pattern is penalized by the rubric but aligns with safety-relevant epistemic restraint.
- **[Mistral] Add a single-line cost estimate for dynamic activation in §5.5** — "Per-query cost drops to ~$0.001 at current frontier pricing."
- **[Mistral] Footnote on LITERAL_RECALL bucket's small size (n=60) in Appendix B.4** for variance caveat.
- **[Cerebras] Consider adding a §4.4 per-system Δ summary table** (controlled and native, side by side) for reader scannability.
- **[Cerebras] Note in §5.5 that specs could be version-controlled like code** (rollback, audit) — direct infrastructure framing.
- **[Cerebras] §1.2 clarify "Base Layer" in C1** refers to the open-source retrieval stack, not the full spec system.
- **[Groq] Expand Wilcoxon signed-rank explanation in §1.3** for statistical-non-specialist readers.

### STYLE

- [Gemini Pro] §1.4 "clean-methodology pilot" -> "methodology-matched pilot" (more neutral).
- [Gemini Pro] §4.4.1 "One-line per-system read" — informal; reword.
- [Mistral] §4.1 Example D "The structural implication is direct" -> "The structural implication is straightforward."
- [Mistral] §4.4.1 "Plain version" -> "Plain-language summary" (consistency with other "Plain version" headers).
- [Mistral] §5.7 "Two separate priorities" -> "Two orthogonal priorities" (sharper phrasing).
- [Cerebras] "Armed with the spec's documented-dignity axioms" -> "Guided by the spec's epistemic-integrity clauses" (too metaphorical).
- [Cerebras] "This is architectural convergence" -> "This suggests architectural convergence" (soften).
- [Cerebras] Replace "tells us" with "indicates" / "suggests" in analytical passages.
- [Cerebras] Prefer "we interpret this as" over "we read this as" for analytical consistency.
- [Groq] Break up some long, convoluted sentences for readability.

---

## Appendix Citation Check — Consensus

Gemini Pro audited all 9 identifiable body -> appendix citations and found **no misaimed or vague citations**. Mistral agreed. Cerebras flagged two low-priority improvements:

- §2.3 could add "(see Appendix E, Table E.1)" for pin-point reference.
- §4.3 cites `scripts/classify_hedging.py` and `docs/research/hedging_analysis.json` — these are repo paths, not appendices. Add a footnote: "Analysis scripts and raw outputs are available in the study repository."

No appendix claim was flagged as unsupported by the body. Self-consistency check: PASS.

---

## Consensus Recommendations for Author Read-Through

Ranked by consensus strength (number of reviewers) and severity:

1. **Sweep every number in §1.3 against its source in §4.** Cerebras alone flagged 3 mismatches, Mistral corroborated 2, Gemini Pro 1. This is the single highest-leverage fix. Build a small list: every Δ, p-value, and example score in §1.3, confirm each against the body.
2. **Resolve Fukuzawa Q26 4.20 vs 4.33 (plus the possible mirror for Sunity Devee Q35).** Pre-disclosed. Cerebras caught a second potential instance; verify.
3. **Read §4.4 end-to-end and make a decision on ordering.** The Aggregate -> Mechanisms -> Keckley structure was independently flagged as non-ideal by 3 reviewers. Either (a) restructure so Supermemory deep-dive leads §4.4.2 Mechanisms, or (b) add strong bridge sentences at §4.4.1 -> §4.4.2 -> §4.4.3 to make the logic explicit. Do not leave as-is.
4. **Add transition sentences:** §4.4 -> §4.5 (2 reviewers), §5.0 -> §5.1 (2 reviewers), §5.6 -> §5.7 (1 reviewer).
5. **Fix §5.1 Twin-2K characterization** (Mistral): "survey-response interpolation," not "prediction."
6. **Reframe §5.5 around infrastructure** to remove overlap with §1.4.
7. **Restate "5 of 6 cells reproduce"** in §1.3 to avoid implying a replication failure.
8. **Clarify §4.5 Letta block size** (335,349 measured vs 333K ceiling).

Items 1, 2, 3, 7, 8 are numerical / semantic correctness. Items 4, 5, 6 are flow. Together these constitute the pre-final fix set.

---

## Items Flagged by 3+ Reviewers (Highlighted)

1. **Fukuzawa Q26 numerical inconsistency** — 4 reviewers (pre-disclosed, not counted as independent).
2. **§1.3 numerical mismatches against body numbers** — 3 reviewers (Cerebras primary, Mistral and Gemini Pro corroborated). **Independent.**
3. **§4.4 internal subsection ordering feels disjointed** — 3 reviewers (Gemini Pro, Cerebras, Mistral). **Independent.**

Only three items cleared the 3-reviewer threshold, and one was pre-disclosed. The §1.3 numerical sweep and the §4.4 reordering decision are the two clean consensus items the author should treat as non-optional before submission.

---

## Verdict for the Author

All four reviewers independently arrived at **READY-WITH-MINOR-FIXES**. No reviewer asked for a new experiment, a structural rewrite, or a scope change. The paper is substantively locked. The remaining work is a numerical sweep of §1.3, a flow decision on §4.4, and roughly a dozen one-sentence bridges and wording tweaks. Expected author time: 60-90 min of focused read-through. No blockers for arXiv.
