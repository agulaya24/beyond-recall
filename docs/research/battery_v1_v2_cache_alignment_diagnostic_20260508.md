# Diagnostic: judgments_v2.json scored v2 responses; paper displays v1 responses

**Date:** 2026-05-08
**Trigger:** Aarik flagged unstable per-cell scores in §4.1 worked examples; investigation surfaced a structural battery/judgment misalignment.

---

## Headline finding

**`judgments_v2.json` (the cache used to compute the paper's headline numbers) scored *v2* responses against *v2* questions. The paper's §4.1 worked examples quote *v1* responses against *v1* questions but cite scores from `judgments_v2.json` — which means the displayed response and the cited score correspond to *different question/response pairs*.**

The aggregate Mean Δ_C4a = +0.89 is internally consistent (v2 measurement of v2 responses). The paper's *qualitative* content (worked examples, quoted responses, question framings) is partly misaligned with the v2 measurement the aggregate is built on.

---

## Evidence chain

### 1. Two complete batteries exist

| File | Created | Description |
|---|---|---|
| `battery.json` | 2026-04-12 01:39 | v1 batteries (40 questions per subject, against v1 corpus split) |
| `battery_v2.json` | 2026-04-14 15:46 | v2 batteries (different questions at the same `question_id` slots) |
| `results.json` | 2026-04-14 15:03 | v1 responses (one per (qid, condition) pair) — generated *before* `battery_v2` was created, so against `battery.json` |
| `results_v2.json` | 2026-04-14 20:44 | v2 responses — generated against `battery_v2.json` |
| `judgments.json` | 2026-04-12 01:57 | v1 judgments |
| `judgments_v2.json` | 2026-04-15 12:35 | v2 judgments — what the paper's aggregate uses |

### 2. v1 and v2 batteries have *completely* different questions at the same `question_id`

Sample across 13 subjects, 4 question_ids each (1, 16, 22, 35) — **52/52 question_ids have different question text in v1 vs v2.**

Examples:
- Fukuzawa Q35 v1: *"Would Fukuzawa's reasoning for keeping students from war be based on moral principle or practical concern?"*
- Fukuzawa Q35 v2: *"How would Fukuzawa characterize someone who studied naval arts under the Dutch and later became instrumental in preventing military conflict?"*
- Bernal Díaz Q16 v1: *"How would Diaz characterize the strategic thinking behind X?"*
- Bernal Díaz Q16 v2: *"When the commander is offered physical assistance during a strenuous activity..."*

These are not paraphrases. They probe different behaviors, different held-out passages, different correct answers.

### 3. Cached judgments have no link to which battery they scored

Every cached judgment record is exactly: `{question_id, condition, judge, score, parse_failure}`. No response_text, no response_hash, no battery_version. We cannot determine programmatically which battery a cached judgment scored.

### 4. Empirical re-judge resolves which battery the cache scored

**Test cell: Fukuzawa Q35 C4 (factdump). Cached score: 1.00 unanimous (haiku/sonnet/opus/gpt4o/gpt54 all = 1).**

| Re-judge run | Question + response | Fresh 5-judge mean |
|---|---|---|
| v1 | "Students from war" Q + v1 C4 response (students-as-precious framing) | **4.20** (5/4/4/4/4) |
| v2 | "Naval officers" Q + v2 C4 response (Captain Kimura framing) | **1.60** (2/1/1/2/2) |

**Cached 1.00 is far from v1 fresh (4.20) but close to v2 fresh (1.60).** The judges that scored `judgments_v2.json` were scoring the v2 response, not the v1 response. The remaining gap (1.00 cached vs 1.60 fresh on v2) is plausibly within run-to-run noise; the v1 gap (1.00 cached vs 4.20 fresh) is far outside that noise.

### 5. Bernal Díaz Q16 stability (Example B in the paper)

Cached score: 2.00 unanimous (2/2/2/2/2). Question text (v1): *"How would Diaz characterize the strategic thinking..."*; v2: *"When the commander is offered physical assistance..."* The Example B response in the paper is the "physical assistance" response with the "Cortés refuses help" held-out — this is the **v2** content. Same picture: paper quotes v2 framing, cites cached score (which came from scoring v2 in this case). Example B is internally consistent (v2 quoted, v2 score). Example A (Fukuzawa) is *not* — it quotes v1 but cites a v2 score.

(Diagnostic for Example C still owed; cached Seacole Q2 score 2.80 / 5/2/3/3/1 is wide-variance and a fresh re-judge of v1 gave 4.00 — same pattern as Fukuzawa: v1 fresh diverges from cached. To confirm v2 origin of Seacole cached, run the v2 cell.)

---

## Implications

### Aggregate measurement (Mean Δ_C4a = +0.89, Wilcoxon p = 0.007, R² = 0.82)

**Internally consistent.** All cached scores in `judgments_v2.json` are scoring v2 responses against v2 questions, end to end. The number "+0.89 mean Spec lift across 14 subjects on the v2 batteries" is what the aggregate actually measures. Headline survives.

### Paper qualitative content

**Mixed alignment.** Spot-checks suggest:
- Example B (Bernal Díaz Q16): v2 question + v2 response + v2 score. **Aligned.**
- Example A (Fukuzawa Q35): v1 question + v1 response + v2 score. **Misaligned** — the displayed response was scored differently from what the cited number indicates.
- Example C (Seacole Q2): pending v2 confirmation, but v1 fresh diverges from cached, suggesting same misalignment as Example A.

The §3.5 prose ("Each main-study subject receives 39 behavioral prediction questions; the 14 main-study batteries total 546 questions") and the question battery framings in §3.5 / §4 may also reflect v1 conventions while the aggregate measures v2.

### Per-question phenomena (§4.1.1, §4.2)

Statistics like "55.0% of low-baseline responses cross at least one rubric anchor" or "18% multi-anchor crossings" are computed from `judgments_v2.json` joined to v2 batteries. These are valid v2 measurements. Verbatim worked examples that quote v1 responses inside these stats *would* be misaligned, but the aggregate stats themselves are not.

### Per-judge files for memory systems

`baselayer_judgments_*`, `letta_judgments_*`, `mem0_judgments_*`, `supermemory_judgments_*`, `zep_judgments_*` (and their `_fullpipeline_*` variants) and `c8_c9_judgments_*` — each scored against whichever results file was current at their generation time. These need their own diagnostic, but the same pattern (only `question_id` linkage, no battery version metadata) applies.

---

## Paths forward

### Option 0 — Confirm the pattern systematically (cheap)

Re-judge **5–8 cells across multiple subjects/conditions**, both v1 and v2 each, to confirm "cached matches v2 fresh, not v1 fresh" is a systematic pattern, not just two cells. Cost: ~$2–5, ~50–80 calls. **Recommend running this first before committing to A or B below.**

### Option A — Reconcile paper qualitative content to v2 (lighter)

If Option 0 confirms the systematic pattern:

- Switch all worked examples in §4.1 to v2 question + v2 response + cached v2 score. (Example A gets a new question/response from v2 Fukuzawa; current "students from war" content gets dropped.)
- Update §3.5 question-battery framings to reflect v2 batteries.
- Verify §3.7 / §4.4 references against v2 content.
- Aggregate numbers (Mean Δ_C4a, gradient slope, anchor-crossing rates, Wilcoxon, etc.) **stay unchanged** — they were always v2 measurements.

**Cost:** rewriting ~3 worked examples + audit pass on qualitative §3.5 framings. No re-running of any pipeline step.

### Option B — Re-judge v1 responses and use v1 throughout (heavier)

If you'd rather the paper's qualitative content (the v1 questions/responses Aarik already worked on) be load-bearing:

- Re-judge `results.json` content (v1 responses, v1 questions) fresh with the current 5-judge primary panel + verbatim rubric. ~10,000 calls × all subjects/conditions. ~$30–50, ~1 day.
- Use that as the new aggregate. Mean Δ_C4a, gradient, anchor-crossing rates, Wilcoxon p — all need to be recomputed from the v1 re-judge.
- Worked examples stay as currently written.

**Cost:** full re-judge + recompute of all §4 numbers. Risk: aggregate may shift; cannot predict direction without running it.

### Option C — Acknowledge and report both (heaviest, most defensive)

Run Option B as a robustness check, report both v1-aggregate and v2-aggregate alongside each other in §4.6 sensitivity. Maximally transparent, maximally heavy.

---

## Recommendation

1. **Run Option 0 immediately** — 5–8 cell systematic pattern check. Cheap, fast, decisive.
2. **If Option 0 confirms cached = v2 across cells, do Option A.** It's the smallest change that gets the paper internally consistent. Aggregate stays; qualitative content gets reconciled to what was actually measured.
3. **Do NOT do Option B or C unless Option 0 surfaces an unexpected finding** — e.g., that some subjects' cached judgments scored v1, or that v1 fresh re-judge produces meaningfully different aggregates from v2.

The minimum-change rule applies: the headline measurement (+0.89) survives; the qualitative paper text needs to catch up to what the aggregate actually represents.

---

## Files
- This memo: `docs/research/battery_v1_v2_cache_alignment_diagnostic_20260508.md`
- Today's earlier related memos: `docs/research/example_a_c4_score_meta_analysis_20260508.md`, `docs/research/example_a_c_fresh_rejudge_20260508.md`, `docs/research/published_rubric_per_judge_ablation_20260508.md`, `docs/research/rubric_rejudge_reconciliation_20260508.md`
- Raw v1/v2 fresh re-judge data: `results/_example_a_c_fresh_rejudge_20260508/` (v1 only); v2 Fukuzawa Q35 C4 result captured inline above.
