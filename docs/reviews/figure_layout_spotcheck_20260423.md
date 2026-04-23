# Figure Layout Spot-Check (2026-04-23)

- Run: 2026-04-23 17:32 UTC
- Model: claude-opus-4-5
- Scope: layout/collision only (no content/color/style critique)
- Figures checked: 14
- CLEAN: 12
- FLAGGED: 2

## Per-figure verdicts

- **fig1_global_gradient**: CLEAN
- **fig2_compression_curve**: ISSUES: - Label "C2a" overlaps with data point (blue circle and green triangle cluster) - Label "C4" overlaps with/crowds the pink diamond data points - Legend box partially obscures the orange square data point (C1)
- **fig3_retrieval_disagreement**: CLEAN
- **fig4_hedging_reduction**: CLEAN
- **fig5_condition_effects**: CLEAN
- **fig6_wrong_spec_control**: CLEAN
- **fig7_memory_systems**: CLEAN
- **fig8_judge_agreement**: CLEAN
- **fig9_cultural_baseline**: CLEAN
- **fig10_letta_scaling**: CLEAN
- **fig11_tier2_replication**: CLEAN
- **fig_4_1_gradient_scatter**: ISSUES: - Overlapping text labels on data points: "Ebers" partially cut off at left edge, "Zitkala-Sa" and "Equiano" labels overlap with their data points - Y-axis label text is dense and may be difficult to read at smaller print sizes - Some data point labels (e.g., "Cabur", "Hamerton") overlap or crowd near their markers
- **fig_4_2_compression**: CLEAN
- **fig_4_2_1_question_improvement_rates**: CLEAN

## Flagged figures

### fig2_compression_curve

ISSUES: - Label "C2a" overlaps with data point (blue circle and green triangle cluster) - Label "C4" overlaps with/crowds the pink diamond data points - Legend box partially obscures the orange square data point (C1)

### fig_4_1_gradient_scatter

ISSUES: - Overlapping text labels on data points: "Ebers" partially cut off at left edge, "Zitkala-Sa" and "Equiano" labels overlap with their data points - Y-axis label text is dense and may be difficult to read at smaller print sizes - Some data point labels (e.g., "Cabur", "Hamerton") overlap or crowd near their markers
