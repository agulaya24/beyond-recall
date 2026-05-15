# §3.3 V1/V2 Alignment Audit — `beyond_recall_v11_9_draft.md`

**Date:** 2026-05-08
**Scope:** §3.3 (lines 372–575), subsections §3.3.1 through §3.3.6.
**Method:** Each (subject, qid, condition)-level quote was matched against canonical V2 data using `scripts/v2_canonical_cell_extractor_20260508.py` (battery_v2.json + results_v2.json + judgments_v2.json). Where a paper quote did not match V2, V1 (`results.json`) and variance/memory-system runs were also searched.

---

## Summary

| Metric | Count |
|---|---|
| Total cell-level quotes audited | 4 |
| Aligned with V2 | 1 |
| Misaligned with V2 | 3 |
| STRUCTURAL severity | 3 |
| COSMETIC severity | 0 |

All four cell-level quotes live in §3.3.1 (Score interpretation). §3.3.2–§3.3.6 contain no (subject, qid, condition)-level quotes (panel composition, calibration table on synthetic inputs, panel-level agreement statistics, aggregation rule, and rubric-handling audit are subject-cell-agnostic).

---

## Findings

### Finding 1 — §3.3.1 line 429 — Sunity Devee, no-context baseline

**Paper claim (lines 428–429):**
> *Sunity Devee, no-context baseline:* "The available context does not provide enough information about this individual to predict her response to such a situation."

**Inferred mapping:** subject = `sunity_devee`, condition = `C5_baseline`, qid = unknown (no qid is named in the paper).

**V2 lookup:** the verbatim string "does not provide enough information about this individual to predict her response" does NOT appear in `results/global_sunity_devee/results_v2.json`. It also does NOT appear in V1 `results/global_sunity_devee/results.json`, in any `_variance_runs/run_*_responses.json`, or in any memory-system `*_results.json` file. The phrase exists ONLY in the v11.8 / v11.9 paper drafts.

**Verdict:** **MISALIGNED — STRUCTURAL.** The C5 quote is not sourceable from any actual study response. It reads as illustrative paraphrase rather than a verbatim model output.

**Recommended fix:** Either (a) replace with a real C5_baseline response from a Sunity Devee qid that scores 1 in V2 (so the 1/2 boundary illustration is sourced), naming the qid in a footnote; or (b) explicitly mark this quote as "stylized example, not verbatim from the dataset." Option (a) is the cleaner repair — the audit would then mirror the canonical-cell traceability the paper claims for §4 worked examples.

---

### Finding 2 — §3.3.1 line 431 — Sunity Devee, Spec-only on the same question

**Paper claim (lines 430–431):**
> *Sunity Devee, Spec-only on the same question:* "She would refuse the proposed action; her writing repeatedly treats conscience and spiritual integrity as the deciding frame, ranked above social cost or familial pressure."

**Inferred mapping:** subject = `sunity_devee`, condition = `C2a_full_spec`, qid = paired with Finding 1.

**V2 lookup:** "conscience and spiritual integrity" does NOT appear in `results/global_sunity_devee/results_v2.json` (V2 main-study), nor in `results.json` (V1). The bigram "spiritual integrity" appears in 88 files across the repo (mostly older drafts and variance-run spec_production.md files), but does NOT appear in any `results_v2.json` response text for any subject under `C2a_full_spec`. The full phrase "conscience and spiritual integrity" exists ONLY in the v11.8 / v11.9 paper drafts and in three Sunity Devee `_variance_runs/run_*_responses.json` files (variance-probe runs, NOT the canonical V2 main-study run).

**Verdict:** **MISALIGNED — STRUCTURAL.** Paired with Finding 1, this is a fabricated illustrative pair, not a real (qid, C5 → C2a) pairing from V2 or V1. If sourced from a variance run, the paper does not say so and the variance-run cell was not used to score the published mean Δ.

**Recommended fix:** Same as Finding 1 — replace with a real V2 (subject, qid) pairing where C5 = 1 and C2a ≥ 2 (exists in §4 anchor-crossing examples), and footnote the qid.

---

### Finding 3 — §3.3.1 line 434 — Bernal Díaz, facts-only on Cortés' physical assistance

**Paper claim (lines 433–434):**
> *Bernal Díaz on Cortés' response to offered physical assistance during a strenuous activity, facts-only:* "Based on the facts provided about Bernal Díaz del Castillo and his observations of Cortés, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example."

**Canonical V2 cell** — `extract('bernal_diaz', 16, 'C4_factdump')`:
- **Question:** "When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?" — matches paper paraphrase.
- **Held-out:** "There were 114 steps to the summit, and, as they feared that Cortes would experience the same fatigue in mounting as Motecusuma had, they were going to assist him by taking hold of his arms. Cortes, however, would not accept of their proffered aid." — consistent with paper's framing.
- **Response (verbatim, V2):** "...the author would expect the commander to **accept and participate in the assistance while maintaining leadership and setting an example**..." — **matches paper quote verbatim.**
- **Per-judge primary scores (haiku, sonnet, opus, gpt4o, gpt54):** 2, 2, 2, 2, 2 → **primary mean = 2.0.**

**Verdict:** **ALIGNED.** Quote is verbatim from V2; mapping is `bernal_diaz` qid=16 C4_factdump; primary mean 2.0 (rubric anchor 2 — "wrong prediction"). The held-out shows Cortés *refusing* assistance, so the C4 response is genuinely off — score 2 is consistent.

---

### Finding 4 — §3.3.1 line 436 — Bernal Díaz, facts + Spec on the same question

**Paper claim (lines 435–436):**
> *Bernal Díaz, facts + Spec on the same question:* "The author would expect Cortés to refuse the help and continue unaided, treating physical hardship in front of his men as a marker of leadership credibility — a pattern the author records repeatedly throughout the campaign."

**Inferred mapping:** subject = `bernal_diaz`, qid = 16, condition = `C4a_full_facts_plus_spec`.

**Canonical V2 cell** — `extract('bernal_diaz', 16, 'C4a_full_facts_plus_spec')`:
- **Response (verbatim, V2 head):** "Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect **Cortes to refuse the assistance and perform the labor himself** — particularly if it serves a symbolic or leadership purpose. ## Evidence from the Text The clearest example occurs during the construction of Villa Rica de la Vera Cruz: > 'Cortes himself carried a basket filled with stones and earth on his shoulders while working on the fortress foundations...'"
- **Per-judge primary scores:** 5, 4, 5, 5, 5 → **primary mean = 4.8.**

**Paper-quoted vs V2 actual:**

| | Paper version | V2 actual |
|---|---|---|
| Verb phrase | "refuse the help and **continue unaided**" | "refuse the assistance and **perform the labor himself**" |
| Justification | "physical hardship in front of his men as a marker of leadership credibility" | "particularly if it serves a symbolic or leadership purpose" |
| Pattern claim | "a pattern the author records repeatedly throughout the campaign" | Cites a specific incident (basket of stones at Villa Rica fortress foundations) and frames Cortés' physical labor as the pattern |

The string "refuse the help and continue unaided" does NOT exist in `results_v2.json` for Bernal Díaz, nor anywhere in the `results/` tree. It exists ONLY in the v11.8 / v11.9 paper drafts.

**Verdict:** **MISALIGNED — STRUCTURAL.** The paper paraphrases the model's actual answer in a direction that flatters the §3.3.1 illustration. The V2 C4a response actually argues Cortés would *participate in physical labor* (the basket-of-stones incident), which is a different behavioral prediction from "refuse and continue unaided." Both predictions happen to score well against the held-out (which shows Cortés refusing arm-support on the temple steps), but the paraphrase distorts the model's reasoning.

**Secondary issue — anchor-crossing miscategorization:** The paper frames this Bernal Díaz example as a **2/3 boundary** illustration ("generic becomes subject-specific"). V2 primary means: C4 = 2.0, C4a = 4.8. The actual delta is **a 2 → 5 multi-anchor crossing across three anchor boundaries (2/3, 3/4, 4/5)**, not a 2/3 boundary case. By the paper's own §3.3.1 multi-anchor-crossing definition (line 442), this example illustrates the "strongest categorical signal the rubric detects" — the headline phenomenon, not the boundary the paper places it at.

**Recommended fix:** Three options, ordered by preference.
1. **Keep the example, recategorize and requote.** Replace the C4a paraphrase with a verbatim 1–2-sentence excerpt from V2's actual C4a response (the basket-of-stones reasoning), footnote qid=16, and move the example to a multi-anchor-crossing illustration in §3.3.1 paragraph on multi-anchor crossings (line 442) rather than the 2/3 boundary list.
2. **Pick a real 2/3 example from V2.** Find a Bernal Díaz qid (or any subject) where 5-judge C4 mean is in [1.6, 2.4] and 5-judge C4a mean is in [2.6, 3.4], use the verbatim responses, and footnote the qid.
3. **Mark as stylized illustration.** Explicitly note in §3.3.1 that the worked excerpts are "stylized to illustrate the boundary; verbatim worked examples appear in §4.1.1 and Appendix E," then drop the quotation marks.

---

## §3.3.2–§3.3.6 audit

No (subject, qid, condition)-level quotes were found in §3.3.2 through §3.3.6.

- **§3.3.2 (Judge panel)** — describes the 7-judge panel composition, blinding, and verbatim judge prompt. No subject-cell content.
- **§3.3.3 (Calibration)** — diagnostic table uses synthetic inputs (verbatim, paraphrased, short correct, long correct) constructed independently of subject responses. The seven judges' calibration scores (e.g., Gemini Pro at 4.15 / 3.55 / 2.85 / 1.20) are sourced from `results/judge_calibration/`, not from any subject's V2 cell. Out of audit scope.
- **§3.3.4 (Inter-judge agreement)** — reports Spearman ρ 0.86–0.93 (5-judge primary), Krippendorff α 0.659 (5-judge) and 0.535 (7-judge). These are panel-level statistics aggregated over all (subject, qid, condition) cells; no individual cell is named. Out of audit scope.
- **§3.3.5 (Aggregation and statistical analysis plan)** — pre-registered aggregation rule, Wilcoxon signed-rank test on Δ_C4a, *N* = 14, two-sided α = 0.05. No cell-level quotes.
- **§3.3.6 (Rubric-handling limitations)** — refusal anchor ambiguity, length-score correlation r = 0.60 in C5, mean lift +0.89. These are repo-level summary statistics; no individual cell is named. Out of audit scope.

---

## Bottom line

§3.3 contains four (subject, qid, condition)-level worked-example quotes, all in §3.3.1. **Three of the four are misaligned with V2.** The Sunity Devee pair (Findings 1 and 2) is fabricated illustrative text not sourceable from any V1, V2, variance-run, or memory-system results file. The Bernal Díaz C4 quote (Finding 3) is verbatim and aligned. The Bernal Díaz C4a quote (Finding 4) paraphrases the V2 response in a direction that distorts the model's reasoning, AND the C4 → C4a anchor-crossing this example illustrates is a multi-anchor (2 → 5) crossing, not the 2/3 boundary the paper places it at.

The §3.3.1 fix burden is structural rather than cosmetic because §3.3.1 is the section that *defines* the cross-anchor interpretation rule. Worked examples in the section that defines the interpretive frame need to be canonical-cell-sourceable for the same reason §4.1.1 worked examples need to be — readers will trace them back. Recommended fix is to replace the four §3.3.1 quotes with V2-canonical (subject, qid, condition) excerpts and footnote the qids, or convert §3.3.1 to a stylized-illustration register and drop the quotation marks. The §4 / §5 worked examples (which are canonical-cell-sourced) should be cross-referenced from §3.3.1 so the rubric-interpretation argument lands on real responses rather than illustrative paraphrase.
