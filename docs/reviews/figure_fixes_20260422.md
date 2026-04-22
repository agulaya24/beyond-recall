# Figure Fix Log — 2026-04-22

Applied in response to [`figure_review_20260422.md`](figure_review_20260422.md). Every figure in `figures/` was regenerated from its script; PNGs were replaced in place at 300 DPI. No file renames; no underlying-data changes; no paper-draft edits.

## Global changes (applied to every script)

- **Unified colorblind-safe palette.** All scripts now import `seaborn` and set `seaborn.set_theme(context='paper', style='whitegrid', palette='colorblind')`. Red/green and some orange/blue pairings are replaced with the seaborn `colorblind` palette (accessible-by-default for deuteranopia / protanopia / tritanopia).
- **Shape / hatch redundancy.** Wherever a single color previously carried a categorical comparison, a second channel (marker shape, hatch pattern) now carries it redundantly, so the figures are grayscale- and print-robust.
- **Paper-scale typography.** `rcParams` adjusted from slide-deck sizes (font.size 9-12, titlesize 12-14) to conference two-column sizes (font.size 8.5-9.5, titlesize 9.5-11). Gridlines thinned to alpha 0.3-0.5.
- **Interpretive text moved out of figures.** Where titles carried a claim ("holds in 5 of 6 cells", "39% reduction"), titles were rewritten as neutral descriptions and the interpretation was moved to the caption (which lives in the paper, not here). Median-Δ statistics on `fig_4_2_1` were moved from the title block to a compact bottom note.

## Per-figure changes

### fig3_retrieval_disagreement — CRITICAL MISMATCH RESOLVED

- **Mismatch.** Figure showed 68% / 39% / 22% / 11% at Top-1/3/5/10; paper §1 abstract and §4.3 state 93% / 83% / 74% / 53% (controlled config, all-three-disagree, 515 questions).
- **Resolution.** Corrected the `values` array in `figures/generate_figures_v3.py::fig3()` to `[93, 83, 74, 53]` per `docs/KEY_FINDINGS.md` §M4 (source: `data/experiments/memory_systems/string_match_disagreement.py` → `results/string_match_disagreement.json`, §3-way controlled).
- **Additional.** Added an inline one-line definition of "disagreement" under the x-axis so the figure stands alone: *"Disagreement" = share of 515 questions where Mem0, Letta, and Supermemory all three returned different top-k items (controlled config; identical fact pool).*
- **Palette.** Single blue color + diagonal hatch for grayscale legibility.

### fig4_hedging_reduction — CRITICAL MISMATCH RESOLVED

- **Mismatch.** Figure showed two bars ("Without Spec" 51%, "With Spec" 31%) with a "39% reduction" arrow callout. Paper §1.3 and §5 describe three conditions (C5 / C2a / C4a) under two classifier rules (narrow `starts_refusal` and broader `refusal_ge_1`). Prior figure's 51/31 numbers could not be reconciled to any replay of `hedging_analysis.json`.
- **Resolution.** Regenerated as a 3×2 grouped bar chart:
  - x = C5 (baseline) / C2a (spec) / C4a (facts + spec)
  - series = Narrow rule (starts_refusal): 28.8% / 1.4% / 0.0%
  - series = Broader rule (refusal_ge_1): 41.2% / 7.9% / 0.4%
  - All six values taken verbatim from `docs/research/hedging_analysis.json`.
- **Palette.** Blue (narrow) + orange with diagonal hatch (broader).
- **Decorative arrow removed.** "39% reduction" callout dropped; the magnitude is visible from the bars themselves.

### fig5_condition_effects — CRITICAL MISMATCH RESOLVED (with residual flag)

- **Mismatch.** Figure showed 5 named conditions ("Baseline", "Spec", "Wrong Spec", "Facts", "Facts+Spec"); the review flagged that the caption references "C1-C9 condition-by-condition mean deltas". Y-axis also truncated at ~1.0.
- **Resolution — labels.** X-axis tick labels changed to the paper's canonical condition codes (C5 / C2a / C2c / C4 / C4a per §3.5), with a small descriptive second-row caption under each tick. Legend on Panel A reworded to reference C2a > C5 and C2a ≤ C5 explicitly.
- **Resolution — y-axis.** Both panels' y-axes now start at 0 (was ~1.0 in the prior figure). Box-plot medians remain centered visually; bias from truncation removed.
- **Caption discrepancy flag (author decision).** The v6-draft caption as quoted in the review references "C1-C9", which would require an 11-condition multi-panel that is not producible from the data currently inlined in `generate_figures_v3.py` (which carries only the five direct-context conditions C5 / C2a / C2c / C4 / C4a). Adding C1, C3, C6, C7, C8, C9 series would require re-aggregating `results/<subject>/*_results.json` and is outside the scope of a figure-quality pass. **Recommend the caption be rewritten** (in `docs/beyond_recall_v8_draft.md`) to describe what is actually plotted: "Per-subject trajectories and score distributions across the five direct-context conditions (C5 / C2a / C2c / C4 / C4a)". Flagged for author.

### fig7_memory_systems — CRITICAL MISMATCH RESOLVED (with data-source flag)

- **Mismatch.** Figure plotted Hamerton-specific absolute C1 and C3 scores for 4 systems (Letta, Mem0, Supermemory, Zep); README and §4.4 describe a per-system C3 − C1 delta on the 9 low-baseline subjects across 5 systems *including Base Layer*.
- **Resolution.** Full replot. x = system, y = mean (C3 − C1) on the low-baseline slice. Bars use the controlled-config values from `DATA_REFERENCE.md §4` for the four commercial systems (Mem0 +0.13, Letta +0.23, Zep +0.20, Supermemory +0.004). Base Layer bar uses **+0.08**, taken from the paper's own §4.4 body-text claim ("Mean C1 ~2.30 across 14 subjects, in the same band as the commercial systems. Spec Δ +0.08 on the low-baseline slice"). Positive-subject counts (6/9, 7/9, 9/9, 5/9, 7/9) now appear as a second x-tick line under each system name.
- **Data-source reconciliation FLAG.** `DATA_REFERENCE.md §4` (controlled config, low-baseline slice) lists **Base Layer +0.13, 7 of 9 positive** — not +0.08. The paper body (§4.4) says +0.08. The discrepancy is not a figure defect; it is a source-of-truth mismatch between the data table and the paper prose. **Flagged for author to reconcile**: either update the §4.4 prose to +0.13 or update DATA_REFERENCE to match the +0.08 figure derivation. The figure currently tracks §4.4 prose.
- **Palette.** Blue bars for positive deltas; orange would have appeared if any system went negative.

### fig8_judge_agreement — CRITICAL MISMATCH RESOLVED

- **Mismatch.** Figure showed a 7×7 correlation heatmap; paper's primary panel is 5 judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) with the two Gemini judges reported as a sensitivity check.
- **Resolution.** Two-panel layout: Panel A = 5-judge primary matrix (sliced from the 7×7 ρ matrix), Panel B = 7-judge sensitivity with both Gemini judges labeled as "Gemini Flash" and "Gemini Pro" (normalized from the previous "Gem Flash" / "Gem Pro").
- **Colormap.** Switched from single-hue `plt.cm.Blues` to perceptually uniform `plt.cm.viridis`. The 0.85–1.00 range is now disclosed in the colorbar label.
- **Typography.** Title shrunk from slide-deck size to paper size; suptitle added above the two panels with exactly the claim the figure supports.

### fig1_global_gradient (high-priority)

- Removed the unlabeled dashed line at x=2.4. It was orphaned — no other figure in the set referenced a 2.4 threshold, and both reviewers independently flagged it.
- Marker shape added: circle for improved, square for not-improved; color-encoded the same way. Improves grayscale legibility.
- Legend clarified ("Improved with spec (above y=x)" / "Not improved (below y=x)" / "y = x (no spec effect)").
- Axis labels spelled out ("Baseline score (no context, 1-5 rubric)", "Score with specification (1-5 rubric)").

### fig2_compression_curve (high-priority)

- Color + marker shape redundancy: each condition family now has a dedicated marker (X for baseline, square for retrieval-only, circle for spec, triangle for memory+spec, diamond for facts, plus for raw corpus).
- Condition labels in the plot are the paper's canonical codes (C5, C2a, C3, C4, C9) rather than descriptive strings.
- Legend moved to avoid obscuring the C5 baseline point at the low-token end.

### fig6_wrong_spec_control (high-priority)

- Rows sorted by (correct − wrong) gap rather than baseline, so the "wrong-spec ≈ baseline" pattern is immediately legible.
- Markers made shape-redundant (X for baseline, square for wrong spec, circle for correct spec).
- Axis limits tightened to the observed data range.

### fig9_cultural_baseline (high-priority)

- Orange/blue legend relabeled to its actual semantic: "Spec improved this subject" / "Spec did not improve this subject". Redundant diagonal hatch on the "not improved" bars.
- Unlabeled 2.4 threshold line removed — it was orphaned and neither reviewer could figure out what it referenced.
- Bars strictly sorted by baseline with lowest at top (reading direction low → high from title).

### fig10_letta_scaling (high-priority)

- Colors switched from crimson/cobalt (fails some colorblind tests) to the seaborn `colorblind` blue/orange pair.
- Babur bar in the right panel now carries a diagonal hatch so the high-duplication state is grayscale-robust.
- Subject + character-count are now a single two-line x-tick label (prior version had the character count floated under the axis in cramped typography).
- Subject labels on the left-panel points offset to avoid collision with the Base Layer line.

### fig11_tier2_replication (high-priority)

- Title rewritten as a neutral description; the "holds in 5 of 6 cells" interpretation moved to where captions live (in the paper prose).
- Gemini Pro bars carry a diagonal hatch so the two response models are distinguishable in grayscale.
- Small in-figure note on battery source (GPT-5.4) + baseline definition keeps the figure readable standalone.

### fig_4_1_gradient_scatter (high-priority)

- Point markers now vary by band (circle low-baseline, square mid, diamond Franklin-control) so the grouping survives grayscale.
- Annotation clutter reduced: only the six notable subjects are labeled (Ebers / Hamerton / Babur / Zitkala-Sa / Equiano / Franklin control); the other eight are left unlabeled to let the trend read cleanly.
- Y=0 reference line now carries an inline label ("Δ = 0 (no spec+facts gain)") so there is no unexplained horizontal line.
- The low-baseline shaded region is explicitly labeled inline.

### fig_4_2_compression (high-priority)

- 10-color overload replaced with faint per-subject lines + one bold black aggregate median curve. The compression shape is now readable in ~5 seconds rather than requiring legend decoding.
- Condition-code vertical reference lines at C5 / C2a / C4a / C9 replace the prior floating top labels; each line carries an inline token-band annotation.

### fig_4_2_1_question_improvement_rates (high-priority)

- Green/red stacked-bar coloring replaced with the `colorblind` palette's blue (improved), light gray (tie), orange (worsened). The two non-improved categories also carry hatching for grayscale.
- Median-Δ statistics moved from the in-figure footer-over-bars into a compact note under the plot.
- Legend moved above the plot area so it does not obscure the tops of the 78% bars.

## Files changed

```
figures/generate_figures_v3.py
figures/README.md
scripts/generate_fig10_letta_scaling.py
scripts/generate_fig11_tier2_replication.py
scripts/generate_fig_4_1_gradient_scatter.py
scripts/generate_fig_4_2_compression.py
scripts/generate_fig_4_2_1.py
figures/fig1_global_gradient.png             (regenerated)
figures/fig2_compression_curve.png           (regenerated)
figures/fig3_retrieval_disagreement.png      (regenerated)
figures/fig4_hedging_reduction.png           (regenerated)
figures/fig5_condition_effects.png           (regenerated)
figures/fig6_wrong_spec_control.png          (regenerated)
figures/fig7_memory_systems.png              (regenerated)
figures/fig8_judge_agreement.png             (regenerated)
figures/fig9_cultural_baseline.png           (regenerated)
figures/fig10_letta_scaling.png              (regenerated)
figures/fig11_tier2_replication.png          (regenerated)
figures/fig_4_1_gradient_scatter.{png,pdf}   (regenerated)
figures/fig_4_2_compression.{png,pdf}        (regenerated)
figures/fig_4_2_1_question_improvement_rates.{png,pdf}  (regenerated)
docs/reviews/figure_fixes_20260422.md        (this file)
```

## Residual items flagged for author

1. **fig5 caption update.** The v6-draft caption says "C1-C9 condition-by-condition mean deltas". The figure now plots the five direct-context conditions (C5 / C2a / C2c / C4 / C4a) with explicit condition codes. Recommend rewriting the caption in `docs/beyond_recall_v8_draft.md` to describe what is actually plotted rather than restoring the promise of 11 conditions, unless the author intends to build the full 11-condition panel.

2. **fig7 Base Layer data-source reconciliation.** Paper §4.4 prose says Base Layer spec Δ on low-baseline = +0.08. DATA_REFERENCE.md §4 controlled-config table says +0.13. The figure follows the paper prose. The author should decide which is authoritative and align the other.

3. **Archive candidate.** `fig1` through `fig11` are v6-era figures retained as prior-draft artifacts; the v8 draft only directly references `fig_4_1_*`, `fig_4_2_*`, and `fig_4_2_1_*`. Consider moving `fig1`–`fig11` into `figures/_archive/` so a reader opening the folder sees only the paper-bound set.
