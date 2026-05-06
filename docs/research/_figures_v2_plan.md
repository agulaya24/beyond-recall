# Beyond Recall — Figures v2 rebuild plan

Session 2026-04-23. Author's v8 Word annotations at
`docs/reviews/s114_word_annotations.md` drove all redesigns.

**Non-destructive:** no existing figures or scripts were modified or deleted. New v2 assets
sit alongside v1 in `figures/` and `scripts/`. Paper draft untouched.

**Shared data input:** for Fig 4.2.1 and Fig 5, a helper script recomputes per-question
outcomes from the raw judgment JSONs (single source of truth):

- `scripts/_compute_per_question_v2.py` → `scripts/_per_question_outcomes_v2.json`
- Matches the paper's §4.2.1 table exactly on the 4 rows it publishes (C2a/C4/C8/C4a totals
  351/351/351/351, improvement counts 249/256/275/276). C9 adds the fifth row the author
  wanted: 312/261/15/36 at 83.7% improved (Babur correctly excluded — 422K-word corpus
  exceeds the response model's context window, already documented in the paper).

---

## Figure 4.1 — gradient scatter

- **Author annotation (§4.1):** "May want to make 0 on the delta axis a different color.
  Likely need to specify >0 means improvement <0 means degradation. Would appreciate a
  better description on the chart, what is the chart/figure saying exactly. Give a guide
  to reading it."
- **Old approach** (`scripts/generate_fig_4_1_gradient_scatter.py`):
  Scatter with gray y=0 axhline in a subtle color, legend listed "Δ=0 (no spec+facts gain)"
  in small text, no on-chart reading guide.
- **New approach** (`scripts/generate_fig_4_1_gradient_scatter_v2.py`):
  1. Δ=0 line drawn in a distinct crimson (`#C44E52`) so the zero reference reads
     immediately, with explicit "Δ = 0 (no gain from spec + facts)" legend entry.
  2. Light-green shaded band above zero, light-red band below zero with inline annotations
     "Δ > 0 improvement" and "Δ < 0 degradation".
  3. Reading-guide box bottom-left: 4 bullets explaining what each axis is, what the point
     positions mean, and what the downward slope means.
  4. Regression and subject labels preserved (author did not contest them).
- **Rendered:** `figures/fig_4_1_gradient_scatter_v2.png`

---

## Figure 4.2 — compression (Hamerton)

- **Author annotation (§4.2):** "This graph is a bit messy... would likely want to see where
  all facts lands, and where just raw corpus lands. May need to rework this figure."
- **Task spec:** "raw corpus alone (C8), facts alone (C4), spec alone (C2a), facts+spec
  (C4a), corpus+spec (C9) on one plot. Per-condition points, log-token x-axis, score
  y-axis."
- **Old approach** (`scripts/generate_fig_4_2_compression.py`):
  9-subject spaghetti plot with per-subject colored traces and a bold median overlay, plus
  floating reference lines for C2a / C4a / C9 token codes — dense and hard to scan.
- **New approach** (`scripts/generate_fig_4_2_compression_v2.py`):
  1. Single-subject (Hamerton) with 6 points (baseline + 5 context strategies) — matches
     task row: "Hamerton results across 5 conditions."
  2. Each point has condition code, token count, and score annotated in a leader-line
     callout. Color + shape redundancy.
  3. Guide arrow + note: "spec alone (7K tok) outscores raw corpus (34K tok) on Hamerton".
  4. C5 baseline drawn as dotted reference line for quick lift comparison.
- **Data source:** `docs/DATA_REFERENCE.md §8` (Table 4.2 Hamerton compression), which is
  already the primary source for the paper's compression claim.
- **Rendered:** `figures/fig_4_2_compression_v2.png`

---

## Figure 4.2.1 — per-question outcome movement

- **Author annotation (§4.2.1):** "I understand the numbers this is showing, but it
  doesn't make it obvious how it's improving. May want to have a line dot plot or something
  moving from condition to condition. Something that shows raw corpus as the first
  condition. Depending if we want to focus on the compression story or something else."
- **Old approach** (`scripts/generate_fig_4_2_1.py`):
  Stacked bars, 4 conditions (C2a/C4/C8/C4a). No C9. No movement cue.
- **New approach** (`scripts/generate_fig_4_2_1_v2.py`):
  1. Line/dot plot with three lines (improved / tied / worsened %) across conditions.
  2. Condition order follows the task spec: **C8 first**, then C2a, C4, C4a, C9.
  3. Trend line on secondary axis shows **mean Δ** across conditions (+0.91 → +0.68 → +0.80
     → +0.89 → +1.07). Makes the compression-vs-stacking story readable in a glance.
  4. In-label tokens per condition (e.g., `C2a / spec alone / ~7K tok`) keep the scale story
     visible without a separate caption.
- **Data gap resolved:** Added C9 (corpus + spec), which the original Fig 4.2.1 did not
  cover. Computed from `results/global_<subject>/c8_c9_judgments_merged.json` + Hamerton
  equivalents via `_compute_per_question_v2.py`. C9: n = 312 (Babur excluded due to context
  window), 261 improved (83.7%).
- **Rendered:** `figures/fig_4_2_1_question_improvement_rates_v2.png`

---

## Figure 5 — condition deltas (aggregate lift / tie / loss)

- **Author annotation (§4 results intro, Figure 5):** "I understand what this is doing, for
  the first figure in the results, [it] should likely be displaying average lift/loss
  metrics across conditions when looking at all questions in aggregate. This doesn't make
  it immediately clear how each condition performs overall."
- **Old approach** (`figures/generate_figures_v3.py:fig5`):
  Two-panel composite: per-subject slope chart on left, score-distribution boxplot on
  right. Both informative but neither shows aggregate lift/loss.
- **New approach** (`scripts/generate_fig5_condition_effects_v2.py`):
  1. Three side-by-side bars per condition: **% improved**, **% tied**, **% worsened** vs.
     C5 baseline.
  2. Mean Δ trend line overlaid on secondary axis (Δ labels in boxed callouts) so the
     magnitude story sits alongside the direction-mix story.
  3. Same 351-question low-baseline-slice dataset as Fig 4.2.1, plus C9 at n=312.
- **Data source:** `scripts/_per_question_outcomes_v2.json`, identical to Fig 4.2.1.
- **Rendered:** `figures/fig5_condition_effects_v2.png`
- **Note:** The existing `fig5_condition_effects.png` (multi-panel slope + boxplot) was
  NOT deleted. This rebuild sits as a sibling.

---

## Figure 7 — memory-system spec delta (grouped bars)

- **Task spec:** "GROUPED BAR CHART: for each of the 4 memory systems (Mem0, Letta
  archival, Supermemory, Zep), show 9 bars (one per low-baseline subject) + a mean bar
  across the 9. Y-axis must extend to both negative and positive (currently Supermemory
  collapses to 0.00 — we need to see the spread)."
- **Old approach** (`figures/generate_figures_v3.py:fig7`):
  5 bars, one per system, each showing aggregate Δ_spec across the low-baseline slice.
  Supermemory collapsed to -0.01, visually invisible.
- **New approach** (`scripts/generate_fig7_memory_systems_v2.py`):
  1. Four panels (one per memory system) side-by-side, sharing y-axis (−0.35 to +0.55).
  2. Each panel: 9 per-subject bars + a highlighted MEAN bar (hatched, outlined, system
     color). Mean also printed in the panel subtitle.
  3. Negative bars tinted red-orange so direction is visible at a glance.
  4. Supermemory spread now clearly visible: ranges from Keckley −0.267 to Hamerton +0.144;
     the aggregate mean −0.010 is bar is correctly shown as a small near-zero bar, not
     "invisible" in the old plot's aggregate-only framing.
- **Base Layer excluded** from this figure per the original paper Fig 7 scope (the
  memory-system comparison figure); Base Layer results are reported alongside in §4.4 and
  in earlier figures.
- **Data source:** `docs/research/memory_systems_5judge_primary.md` — per-subject detail,
  controlled configuration, 5-judge primary.
- **Rendered:** `figures/fig7_memory_systems_v2.png`

---

## Figure 9 — cultural baseline (move to appendix, no rebuild)

- **Author annotation (§3.2 / §3.2.1):**
  - §3.2: "Should likely be a figure including all of the subjects and their baseline score"
  - §3.2.1: "This should be collapsed into a figure for 3.2. likely can drop 3.2.1"
    and a `tracked_delete` on the Figure 9 anchor line.
- **Decision: move to appendix, no script change.**
  - Rationale: The author's delete marker on the §3.2.1 Figure 9 anchor paired with
    "likely can drop 3.2.1" signals the pretraining-coverage figure is not needed in the
    main body once the baseline distribution is summarized inline (per the §3.2 comment).
    The existing `fig9_cultural_baseline.png` in `figures/` is adequate for an appendix
    reference; rebuilding it for the main body would be working against explicit feedback.
- **Action for caller:** in the Part B restructure, move Figure 9 to Appendix and remove
  the inline reference from §3.2.1 (or fold §3.2.1 back into §3.2 with baseline table).
- **No script change required.**

---

## Figure 11 — Tier 2 replication (dropped)

- **Author annotation (§4.5.1):** "Not entirely clear what this figure is doing. May want
  to drop. Table seems to cover it better, even after reading the concern and test design."
- **Decision: drop. Table in §4.5 is authoritative, per the author's stated preference.**
  - Rationale: The author was explicit — rebuilding a figure he's flagged as unclear,
    against his stated preference for the table, works against the feedback. The Tier 2
    data is 6 data points (3 subjects × 2 response models); a table shows them tighter than
    any figure.
- **Action for caller:** drop the `![Figure 11: ...]` image include in §4.5.1; leave the
  §4.5 table in place.
- **No script change required.** Existing `fig11_tier2_replication.png` and its script
  remain on disk for reference.

---

## Figure 3 — retrieval disagreement (keep figure, revise caption)

- **Author annotation (§4.4):** figure is kept; interpretation should be more explicit.
- **Decision: no script change.** Fig 3 stays as is.
- **Action for caller:** when the caption is next revised, add a reading guide that
  states: (a) "disagreement" = share of questions on which Mem0 / Letta / Supermemory all
  three returned different top-k items; (b) the controlled fact-pool context; (c) why this
  matters for the paper's claim that retrieval-only memory systems do not converge on what
  is relevant from identical source material.
- **No script change required.**

---

## Data-audit artifacts (produced during rebuild)

- `scripts/_compute_per_question_v2.py` — recomputes per-question outcomes from raw
  judgment JSONs. Inputs: `results/global_<subject>/judgments_v2.json`,
  `results/global_<subject>/c8_c9_judgments_merged.json`, plus Hamerton's mixed-schema files
  (`judgments.json`, `gpt4o_judgments.json`, `gpt54_judgments.json`,
  `gemini_pro_judgments.json`, `opus_judgments.json`, `sonnet_judgments.json`,
  `judgments_harmonized.json`, `c8_c9_judgments_merged.json`).
- `scripts/_per_question_outcomes_v2.json` — cached outputs, consumed by Fig 4.2.1 v2
  and Fig 5 v2. Includes per-subject question-count breakdown for audit.
- `scripts/_probe_hamerton.py`, `_probe_hamerton2.py`, `_probe_hamerton3.py`,
  `_probe_c4a.py`, `_probe_hamerton_c4a.py` — transient schema-probe scripts used to
  diagnose Hamerton's mixed judgment-file schemas. Can be deleted once author approves
  v2 figures; retained for reproducibility.

---

## Deliverable inventory

| Figure | New script | Rendered image |
|---|---|---|
| 4.1  | `scripts/generate_fig_4_1_gradient_scatter_v2.py` | `figures/fig_4_1_gradient_scatter_v2.png` |
| 4.2  | `scripts/generate_fig_4_2_compression_v2.py` | `figures/fig_4_2_compression_v2.png` |
| 4.2.1| `scripts/generate_fig_4_2_1_v2.py` | `figures/fig_4_2_1_question_improvement_rates_v2.png` |
| 5    | `scripts/generate_fig5_condition_effects_v2.py` | `figures/fig5_condition_effects_v2.png` |
| 7    | `scripts/generate_fig7_memory_systems_v2.py` | `figures/fig7_memory_systems_v2.png` |
| 9    | (no rebuild — move to appendix) | N/A |
| 11   | (no rebuild — drop, table covers it) | N/A |
| 3    | (no script change — caption revision only) | N/A |

All v2 scripts use `matplotlib`, `seaborn`, `numpy` only. No additional dependencies. Each
script can be re-run standalone:

```bash
python scripts/generate_fig_4_1_gradient_scatter_v2.py
python scripts/generate_fig_4_2_compression_v2.py
python scripts/_compute_per_question_v2.py  # prerequisite for 4.2.1 and 5
python scripts/generate_fig_4_2_1_v2.py
python scripts/generate_fig5_condition_effects_v2.py
python scripts/generate_fig7_memory_systems_v2.py
```
