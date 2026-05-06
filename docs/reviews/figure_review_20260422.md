# Figure Quality Review (2026-04-22)

Vision providers: Claude Opus 4.5, OpenAI GPT-5.4 (with gpt-4o fallback if unavailable). Figures reviewed: 14.

## Summary table

| Figure | Opus grade | GPT-5.4 grade | Consensus priority |
|---|---|---|---|
| fig1_global_gradient | B | B | Low |
| fig2_compression_curve | B | B | Low |
| fig3_retrieval_disagreement | C | B | High |
| fig4_hedging_reduction | D | C | Critical |
| fig5_condition_effects | C | C | High |
| fig6_wrong_spec_control | B | B | Low |
| fig7_memory_systems | B | B | Low |
| fig8_judge_agreement | B | B | Low |
| fig9_cultural_baseline | B | B | Low |
| fig10_letta_scaling | B | B | Low |
| fig11_tier2_replication | B | B | Low |
| fig_4_1_gradient_scatter | B | B | Low |
| fig_4_2_compression | B | B | Low |
| fig_4_2_1_question_improvement_rates | B | B | Low |

## Per-figure details

### fig1_global_gradient.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Inconsistent labeling—only 5 of 14 subjects are labeled, creating visual imbalance -> Label all points or none, or use a systematic criterion (e.g., label only outliers beyond 1 SD)
  2. Y-axis label "Spec Condition Score" is jargon without definition -> Change to "Score with Specification" or define abbreviation in caption
  3. Vertical dashed line at x≈2.4 is unexplained and adds visual clutter -> Remove or explain in caption (e.g., "median baseline")

- STRENGTHS: Clean design with effective y=x reference line, colorblind-safe blue/orange palette, and appropriate axis scaling that avoids misleading truncation.

- IDEAL VERSION: A scatter plot with all 14 points unlabeled (or all labeled in smaller font), a brief annotation showing the regression slope (-0.98) directly on the plot, and axis labels using full descriptive terms rather than abbreviations.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. The figure does not directly show the claimed “gradient” or ordering by baseline, so the main takeaway is weaker than the caption claims -> replace with a delta-vs-baseline plot (improvement = spec−baseline on y-axis) plus fitted slope and CI, or at minimum add a regression line/annotation and sort subjects explicitly if using a dot plot.
  2. Annotation clutter and inconsistent emphasis make the plot busy at print size -> label only pre-specified notable subjects or move names to a companion table, reduce italic callouts, and use smaller consistent typography with cleaner leader lines.
  3. The extra vertical dashed reference line is unexplained visually and competes with the y=x line -> remove it unless essential, or label it directly in-figure with a clear meaning (e.g., mean/median baseline).
- STRENGTHS: The y=x reference makes improvement interpretable, axes are not misleadingly truncated relative to the comparison task, and the blue/orange encoding is simple and broadly readable.
- IDEAL VERSION: A clean scatter or, preferably, a baseline-vs-improvement plot with colorblind-safe blue/orange points, one clearly labeled reference/regression line, minimal or selective annotations, consistent typography, and no unexplained guide lines so the negative gradient is immediately visible without relying on the caption.

---

### fig2_compression_curve.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Inconsistent/cluttered labels → Remove italic condition labels from points; use consistent annotation style or reference table
  2. Color palette not colorblind-safe → Replace green/orange with distinguishable hues (e.g., blue/orange or use shapes as redundant encoding)
  3. Legend categories don't clearly map to visible points → Clarify which conditions map to which legend entries, or label points with condition numbers only

- STRENGTHS: Log scale appropriate for token range; clean gridlines; core finding (spec beats raw corpus) is visually evident from point positions

- IDEAL VERSION: A cleaner scatter plot with consistent point labels (C1-C9 only), shape encoding redundant with color for accessibility, and a companion table mapping condition codes to full descriptions, with the key comparison (C2a vs C9) highlighted via annotation line or callout.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Main claim is not instantly visible because the key comparison points are sparsely annotated and the figure relies on caption/context -> directly label or highlight the ~5K-token spec point and 34K-token raw point with token counts and scores, plus a subtle arrow/callout stating “5K spec > 34K raw”
  2. Visual clutter from oversized title, large markers, heavy grid, and a bulky legend reduces print-readability -> shrink/remove the title, reduce marker size and grid prominence, and replace the legend with direct point labels or a compact top/right legend
  3. Category encoding is somewhat ambiguous and not fully colorblind/greyscale robust -> use a colorblind-safe palette plus distinct marker shapes or outlines for each condition family so categories remain separable in grayscale print
- STRENGTHS: The log-scaled x-axis is appropriate, the overall trend is understandable, and the plot does support the compression story that mid-sized specs outperform the much longer raw corpus.
- IDEAL VERSION: A clean log-scale scatter with smaller markers, direct labels on only the key conditions (especially C2a/C3/C4/C9), a colorblind-safe shape+color encoding, minimal gridlines, no oversized title, and an explicit visual annotation showing that the ~5K-token spec condition scores above the 34K-token raw corpus point.

---

### fig3_retrieval_disagreement.png

**Claude Opus:**

- GRADE: C

- TOP 3 ISSUES (priority order, each one line):
  1. Data mismatch: Figure shows 68%/11% but caption claims 93%/53% disagreement rates -> Verify and correct values to match the text in §1 and §4
  2. Missing context: No indication this aggregates three systems or how disagreement is defined -> Add subtitle or caption note explaining aggregation method across Mem0, Letta, Supermemory
  3. Non-standard x-axis intervals: Top-1, 3, 5, 10 are uneven but bars are equally spaced -> Either use proportional spacing or add note that axis is categorical

- STRENGTHS: Clean minimal design with direct data labels, appropriate y-axis starting at zero, legible typography and professional single-hue color choice

- IDEAL VERSION: A bar chart with corrected data values matching the paper text, a brief annotation explaining the three-system aggregation methodology, and either grouped bars showing each system separately or error bars indicating variance across the three memory systems.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Main values do not match the paper claim/caption support (figure shows 68% top-1 and 11% top-10 vs stated 93% and 53%) -> correct the underlying data or replace the plot so the displayed numbers exactly match the text and caption.
  2. Title is oversized and the chart uses heavy gridlines / large typography that feel presentation-like rather than conference-paper-like -> reduce title size, lighten or remove minor visual clutter, and standardize fonts to paper-sized readability.
  3. The figure lacks enough context to stand alone because “disagreement” is undefined and no denominator/sample context is visible -> add a concise subtitle or axis note such as “% queries with non-identical retrieved sets across Mem0/Letta/Supermemory” and include n in caption.
- STRENGTHS: Simple single-series bar chart with clear category ordering, zero baseline, and direct value labels makes the trend easy to read quickly.
- IDEAL VERSION: A compact NeurIPS-style bar chart with corrected values, a y-axis from 0–100%, subtle gray gridlines, smaller consistent typography, direct labels on bars, and a concise in-figure note clarifying that disagreement means the percentage of queries whose top-k retrieved sets differ across Mem0, Letta, and Supermemory.

---

### fig4_hedging_reduction.png

**Claude Opus:**

- GRADE: D

- TOP 3 ISSUES (priority order, each one line):
  1. Caption-figure mismatch: Caption describes three conditions (C5→C2a→C4a) with specific percentages, but figure shows only two bars ("Without Spec" vs "With Spec") with different values (51%/31%) → Regenerate figure to match caption data or correct caption
  2. Misleading annotation: "39% reduction" is ambiguous (could be absolute or relative; 51→31 is 20 percentage points absolute, ~39% relative) → Clarify as "39% relative reduction" or show absolute difference
  3. Orange/blue palette may fail red-green colorblind readers and orange prints poorly in grayscale → Use colorblind-safe palette (e.g., blue/orange from ColorBrewer with sufficient luminance contrast)

- STRENGTHS: Clean minimal design with clear axis labels, appropriate y-axis starting at zero, and readable typography

- IDEAL VERSION: A grouped or multi-bar chart showing all three conditions (C5, C2a, C4a) with both classifier rules (narrow/broader) as separate series, using a colorblind-safe palette and annotations that clearly indicate the metric type (absolute vs. relative change).

**GPT-5.4:**

- GRADE: C
- TOP 3 ISSUES (priority order, each one line):
  1. Figure does not match the stated result (shows 2 bars and 51%→31%, while caption describes C5→C2a→C4a with narrow/broader rules: 28.8→1.4→0.0 and 41.2→7.9→0.4) -> Redesign as a 3-condition plot with both classifier-rule series and exact reported values.
  2. Annotation-heavy presentation (“39% reduction” arrow, oversized title/value labels) adds chart junk and is not publication-standard -> Remove the arrow/callout, shrink typography, and let the data/legend convey the comparison.
  3. Labels are underspecified for standalone reading (“Without Spec/With Spec” is too vague; no legend for rules; x-axis omits condition names) -> Use x-axis labels C5, C2a, C4a, add a concise legend for Narrow vs Broader rule, and title/y-axis text aligned with caption terminology (“Hedging/refusal rate (%)”).
- STRENGTHS: Simple bar design, zero-baseline y-axis, and high-contrast colors make the current comparison easy to read at a glance.
- IDEAL VERSION: A clean, print-friendly grouped bar chart or two-line plot with x-axis C5/C2a/C4a, y-axis hedging/refusal rate (%) from 0–45 or 0–50, two colorblind-safe series for Narrow and Broader classifier rules, small direct value labels, minimal gridlines, and no decorative arrow.

---

### fig5_condition_effects.png

**Claude Opus:**

- GRADE: C

- TOP 3 ISSUES (priority order, each one line):
  1. Caption mentions conditions C1-C9 but figure shows "Baseline, Spec, Wrong Spec, Facts, Facts+Spec" — reconcile labeling or add condition code annotations to x-axis
  2. Panel A legend "Improved/Not improved" undefined — specify improved relative to what (baseline? previous condition?) and how threshold was determined
  3. Y-axis truncated at ~1.0 instead of 0, potentially exaggerating effect sizes — either start at 0 or add axis break notation

- STRENGTHS: Clean two-panel layout effectively pairs individual trajectories with aggregate distributions; minimal chartjunk and professional typography

- IDEAL VERSION: Unified figure with x-axis labels matching condition codes from the paper (C1-C9), a legend explicitly defining the improvement criterion, y-axis starting at 0 or with clear break notation, and a colorblind-safe palette (e.g., blue/orange replaced with blue/vermillion from ColorBrewer) with pattern fills for print compatibility.

**GPT-5.4:**

- GRADE: C
- TOP 3 ISSUES (priority order, each one line):
  1. Figure content does not match the stated caption/claim ("condition-by-condition mean deltas across subjects" and core conditions C1–C9) -> either replace with the actual delta-by-condition summary figure or retitle/reframe this as an illustrative pilot/example trajectory + distribution figure.
  2. Panel A is visually busy and the blue/orange improvement coding is underdefined and potentially misleading -> de-emphasize individual trajectories with thin gray lines, overlay condition means ± CI, and define "Improved" explicitly in-panel or remove that categorization.
  3. Labels and panel organization are not self-sufficient for a scanning reader -> add a concise shared x-axis descriptor, clarify what score means and relative to what baseline/delta, and use consistent panel lettering/typography sized for two-column print.
- STRENGTHS: Clean overall layout, readable axes, sensible y-scale without deceptive truncation, and the boxplot panel is close to publication-ready.
- IDEAL VERSION: A two-panel, print-safe figure where the left panel shows condition-wise mean deltas (with 95% CIs and subject-level jitter or faint paired lines) across the actual core conditions C1–C9 and the right panel gives compact distributions on the same scale, using a restrained colorblind-safe palette, explicit labels, and minimal visual clutter.

---

### fig6_wrong_spec_control.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Color palette not colorblind-safe (orange/gray distinction problematic for deuteranopia) -> Use blue/orange/gray with higher saturation contrast or switch to blue/vermillion/black with distinct shapes
  2. Y-axis labels are cryptic historical names without context -> Add brief descriptor or group by category, or reference a table explaining subject selection
  3. Title is informal ("Wrong Spec Control") -> Use formal title like "Judge Scores Across Specification Conditions by Subject"

- STRENGTHS: Clean dot plot design effectively shows three-way comparison per subject with minimal chart junk; gridlines aid score reading without overwhelming.

- IDEAL VERSION: A horizontal dot plot with colorblind-safe palette (e.g., viridis-derived), subjects ordered by effect size (correct-spec minus wrong-spec), formal axis titles, and marker shapes redundantly encoding condition alongside color.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Main takeaway is not immediately visible because the title is long and the comparison structure is visually flat -> retitle to “Correct-spec vs. wrong-spec score by subject” and directly encode pairing with faint within-row connectors or sort rows by (correct − wrong) gap.
  2. X-axis is labeled “Judge Score (1-5)” but the plotted range starts near 0.5, which can feel inconsistent and slightly misleading -> set the axis cleanly to 1–5 (or explicitly mark observed range while noting the score scale in caption).
  3. Baseline/wrong/correct colors are acceptable but the orange-blue-gray trio is only marginally print-robust without shape redundancy -> use a colorblind-safe palette with stronger luminance separation and/or distinct marker shapes, especially if printed in grayscale.
- STRENGTHS: Clean dot plot, readable subject labels, minimal clutter, and the per-subject triplet design does communicate that wrong-spec is generally much closer to baseline than to correct-spec.
- IDEAL VERSION: A sorted horizontal triplet dot plot with x-axis spanning 1–5, concise title, colorblind-safe markers (optionally with distinct shapes), subtle within-row connectors or highlighted correct–wrong gaps, and a compact legend placed unobtrusively so the “wrong-spec ≈ baseline, correct-spec higher” message is instantly legible.

---

### fig7_memory_systems.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Caption-figure mismatch: Caption mentions "C3 minus C1 delta" and "Base Layer" but figure shows absolute scores with percentage improvements and no Base Layer → Revise caption to match actual content or update figure to show deltas
  2. Percentage labels inconsistent with visual encoding: +66% for Zep appears largest but represents smallest absolute gain (1.07) vs Letta's +45% (1.05) → Add absolute delta values alongside percentages or clarify metric in title
  3. Gray-blue palette may lack sufficient contrast for grayscale printing → Use hatching patterns or increase luminance difference between conditions

- STRENGTHS: Clean design with minimal chart junk, clear direct labeling of values, appropriate y-axis starting at 0 avoiding truncation bias

- IDEAL VERSION: A grouped bar chart showing both absolute scores and delta values with consistent labeling, matched caption describing actual content, and pattern fills for print accessibility, with all five systems mentioned in caption included.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Figure does not match the stated scope/caption (caption says 5 systems incl. Base Layer, figure shows 4 and uses a different title framing) -> align title/caption/content exactly and include Base Layer or revise the claim/caption.
  2. Main quantity of interest is the delta, but the chart emphasizes absolute scores with decorative percent callouts -> plot C3−C1 directly (or add explicit delta labels in score units, with optional percent secondary annotation).
  3. Styling is too presentation-like for NeurIPS/ICML (oversized title/legend, heavy gridlines, large annotations) -> reduce title size, lighten grid, shrink legend, standardize typography, and simplify annotations for print-size readability.
- STRENGTHS: Grouped bars make the direction of improvement immediately visible, the zero baseline is honest, and the gray/blue pairing is broadly colorblind-safe and print-tolerable.
- IDEAL VERSION: A compact grouped bar chart or dot-and-whisker plot with all five systems including Base Layer, x-axis = system, y-axis = spec delta (C3−C1) in judge-score units on a zero-centered scale with optional error bars, minimal gridlines, consistent small typography, and subdued colorblind-safe accents.

---

### fig8_judge_agreement.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Caption mentions "6-judge panel" but figure shows 7 judges (includes Gem Pro) -> Correct caption or clarify if Gem Pro is separate
  2. Color scale truncated at 0.86 exaggerates visual differences in a high-agreement matrix -> Start scale at 0.80 or 0.0 with diverging colormap, or note truncation explicitly
  3. "Gem Flash" and "Gem Pro" abbreviations inconsistent with "GPT-4o/GPT-5.4" naming convention -> Use full names (Gemini Flash, Gemini Pro) or consistent abbreviation style throughout

- STRENGTHS: Clean heatmap with readable annotations, symmetric matrix correctly displayed, professional typography and adequate cell contrast for value legibility.

- IDEAL VERSION: A correlation heatmap with a clearly labeled non-truncated or explicitly noted color scale (0.80–1.00), consistent model naming conventions, corrected caption matching the actual judge count, and a colorblind-safe sequential palette (e.g., viridis) replacing the current blue scheme.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Caption/title mismatch with stated 6-judge panel and caption mention of “correlations / alpha across subjects” while figure shows a 7×7 pairwise rho matrix -> align the figure to the actual panel and metric(s), or split into separate panels for pairwise Spearman rho and panel-level alpha.
  2. Axis labels are inconsistent/abbreviated (“Gem Flash”, “Gem Pro”) and title is oversized relative to publication norms -> use the exact model names consistently on both axes/caption and reduce title/font size to match paper typography.
  3. Color scale is overly compressed near 1.0 and the full symmetric matrix duplicates information -> either show only one triangle with annotations or justify the truncated colorbar clearly and consider a more print-robust grayscale-safe palette with subtle cell borders.
- STRENGTHS: Easy-to-read heatmap with direct in-cell values, clear ordering, and overall high agreement pattern visible at a glance.
- IDEAL VERSION: A compact upper-triangular annotated heatmap with consistent judge names, a smaller publication-style title, a clearly justified and labeled rho color scale (or separate alpha panel), and colorblind/print-safe styling that remains legible at single-column size.

---

### fig9_cultural_baseline.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Threshold line unlabeled and unexplained—what does 2.4 represent? -> Add clear annotation or define in caption what threshold signifies and why it determines improvement classification
  2. Orange/blue color scheme may conflate "did not improve" with negative connotation for cultures scoring above threshold -> Reframe legend to neutral terms (e.g., "Above threshold" / "Below threshold") or clarify the spec improvement logic
  3. Y-axis ordering unclear (neither alphabetical nor strictly by score) -> Sort all bars by baseline score descending for cleaner visual hierarchy

- STRENGTHS: Clean minimal design, appropriate scale starting at zero, legible typography, and effective horizontal bar orientation for categorical comparisons.

- IDEAL VERSION: A horizontal bar chart sorted strictly by baseline score with a clearly annotated threshold line, neutral color coding explained in terms of the threshold criterion, and a subtitle clarifying the Western-canon exposure hypothesis being tested.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Color encoding is semantically opaque and potentially misleading (orange bars are among the highest baselines, but legend refers to downstream improvement) -> relabel colors to reflect the actual grouping shown or replace color with direct bar annotations / side markers for “spec improved” vs “not improved.”
  2. The main claim (“correlated with Western-canon pretraining exposure, not subject quality”) is not visually explicit from the category ordering alone -> rename categories to a clearer construct (e.g., “subject cultural origin”), add a short subtitle or axis-side note indicating bars are sorted by baseline, and optionally group/shade likely high- vs low-exposure regions.
  3. Figure is somewhat busy for print (heavy gridlines, large title, oversized legend, handwritten-style threshold note) -> reduce gridline contrast, shrink title, move threshold label to a clean printed annotation, and simplify the legend or replace it with direct labeling.
- STRENGTHS: Easy-to-scan horizontal ranking, sensible zero baseline, and the threshold line helps connect the plot to the §4 gradient discussion.
- IDEAL VERSION: A clean horizontal bar chart sorted by baseline with direct, publication-style annotation of the threshold, a corrected/clarified grouping cue tied to the actual hypothesis (pretraining exposure or improvement status), lighter gridlines, and consistent typography that remains legible in grayscale and at single-column print size.

---

### fig10_letta_scaling.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Red/blue color scheme fails common colorblind tests (deuteranopia) -> Switch to blue/orange or use distinct markers with patterns
  2. Left panel y-axis label "Block / spec size (characters)" is ambiguous -> Clarify to "Memory block size (characters)" or separate into two labeled series
  3. Right panel x-axis labels mix dataset names with character counts in inconsistent typography -> Standardize font size and move character counts to a table or parenthetical in legend

- STRENGTHS: Clear visual narrative showing linear growth vs. bounded behavior with well-marked API ceiling; dual-panel layout effectively links scaling to quality degradation.

- IDEAL VERSION: A two-panel figure using colorblind-safe palette (blue/orange) with simplified axis labels, consistent typography across both panels, and the right panel's character counts moved to a unified legend or caption to reduce axis clutter.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Left panel overlays two different relationships on one y-axis and uses source size on x-axis without making the subject-wise pairing immediately obvious -> switch to a dumbbell/slope chart by subject or small multiples, with each subject on the x-axis and separate marks for Letta block, Base Layer spec, and ceiling.
  2. Titles and in-plot text are too sentence-like and oversized for paper style, with heavy bold annotations competing with data -> shorten titles, reduce font sizes, and move subject labels to axis ticks or unobtrusive point labels.
  3. The right panel’s zero bars are visually weak and the added character-count text under categories is cramped/redundant -> use direct x-axis labels with subject + chars on two lines and annotate all bars consistently with compact labels.
- STRENGTHS: The main takeaway is visible: Letta memory grows sharply toward/above the API ceiling while the base specification remains comparatively flat, and the coherence problem is highlighted with a simple bar chart.
- IDEAL VERSION: A two-panel figure with subject names on the x-axis, a clean left-panel subject-wise comparison of Letta block vs Base Layer vs API ceiling using colorblind-safe lines/markers and concise labels, and a right-panel bar chart with consistent direct annotations showing duplication rising sharply only for Babur.

---

### fig11_tier2_replication.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Title contains result interpretation ("holds in 5 of 6 cells") which belongs in caption, not figure -> Move to caption; use neutral descriptive title like "Tier 2 Cross-Provider Replication Results"
  2. X-axis labels (Ebers, Yung Wing, Zitkala-Sa) are undefined without context -> Add subtitle or axis label clarifying these are "Subject/Topic" categories
  3. Blue/green palette may fail deuteranopia colorblind tests -> Use blue/orange or add pattern fills for accessibility

- STRENGTHS: Clean layout with minimal chart junk, clear value annotations on bars, appropriate baseline at zero, and legible typography at standard print sizes.

- IDEAL VERSION: A grouped bar chart with a neutral descriptive title, clearly labeled subject categories on x-axis, colorblind-safe palette (blue/orange), and the interpretive "5 of 6 cells" finding moved to the caption where methodological context can be provided.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. X-axis categories are under-explained, so the figure is not self-contained without paper context -> add an x-axis label or short subtitle clarifying what “Ebers / Yung Wing / Zitkala-Sa” are (e.g., subject personas/authors/cells) and what each grouped pair represents
  2. The title is too long and carries interpretation rather than just description -> shorten to a neutral descriptive title and move “spec direction holds in 5 of 6 cells” to caption or a small annotation
  3. No uncertainty or sample-size information makes replication strength hard to assess -> add error bars or CIs and optionally n per bar/group
- STRENGTHS: Clean grouped-bar layout, readable value labels, sensible zero baseline, and generally professional color/legend treatment.
- IDEAL VERSION: A compact grouped bar chart with a short neutral title, explicit x-axis/context labels, colorblind-safe fills plus optional hatching, and confidence intervals/error bars around each estimate while keeping the zero reference line and direct value annotations.

---

### fig_4_1_gradient_scatter.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Y-axis label uses cryptic notation "Δ_C4a (facts + spec vs baseline)" -> Spell out fully: "Change in C4a Score (facts + specification vs. baseline)"
  2. Color scheme not fully colorblind-safe (red-green distinction problematic for deuteranopia) -> Use blue/orange/purple palette instead of green/orange/red
  3. Overlapping labels (Seacole/Bernal Diaz, Keckley/Yung Wing, Cellini/Rousseau/Augustine) reduce legibility -> Use repel/offset positioning or leader lines

- STRENGTHS: Strong regression annotation with R² and slope, clear visual separation of baseline groups, appropriate confidence band shading, and clean axis formatting.

- IDEAL VERSION: A scatter plot with fully spelled-out axis labels, colorblind-safe palette (e.g., viridis-derived), non-overlapping point labels using smart repulsion, and the Franklin control point visually distinguished by marker shape rather than just color.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Figure is over-annotated and hard to parse quickly (long title, long legend, every point labeled) -> shorten title, move slope/R² and cohort definitions to caption, and label only notable/outlier points or use repel labels with smaller text.
  2. Background category shading and CI band add visual clutter and overlap ambiguously -> remove the vertical shaded regions (or replace with thin threshold lines at C5=2 and 3) and lighten/thin the CI band.
  3. Axes and reference structure are not fully self-explanatory for the intended comparison -> add a y=0 reference label (“no spec+facts gain”), consider an x=y-style conceptual note in caption if needed, and tighten axis limits to the data range with consistent tick spacing.
- STRENGTHS: Clear negative trend is visible, axes are mostly clean and interpretable, and the green/orange/red grouping is reasonably intuitive and colorblind-tolerant.
- IDEAL VERSION: A clean scatter with concise axis labels, thin dashed regression line plus subtle CI band, threshold markers at baseline cutoffs instead of full background shading, selective non-overlapping point labels, a small unobtrusive legend for cohort colors, and a short title while statistical details live in the caption.

---

### fig_4_2_compression.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Color palette not colorblind-safe (10 similar hues, pink/red and olive/green pairs problematic) -> Reduce to 5-6 distinct colors with varied line styles (solid, dashed, dotted) or use shape markers more prominently
  2. Legend overcrowded and competes with data -> Move legend outside plot area or use direct line labels at endpoints; "Spec / Facts region" annotation belongs in caption, not legend
  3. Shaded region labels ("C5", "Spec / Facts", "Raw Corpus") at top lack explanation -> Define these regions in caption or add brief axis annotations explaining the compression stages

- STRENGTHS: Log-scale x-axis appropriate for token ranges; clear overall trend visible showing steep initial gains then plateau; professional gridlines and axis formatting.

- IDEAL VERSION: A cleaner figure with 3-4 grouped line styles (by subject category) using a colorblind-safe palette, legend moved outside the plot or replaced with direct labels, and region annotations integrated into a descriptive caption rather than cluttering the plot area.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Too many overlapping subject trajectories and points make the main takeaway hard to parse -> emphasize the aggregate trend with a bold summary curve and de-emphasize per-subject lines using thinner, lighter strokes or move subject detail to appendix/small multiples.
  2. Title/subtitle and in-plot callouts are verbose and compete with the data -> shorten the title, move interpretation (“steep initial slope, long plateau”) to the caption, and replace floating labels (“C5”, “Spec / Facts”, “Raw Corpus”) with cleaner top annotations or subtle axis-region markers.
  3. Color/legend load is high for nine series and may not print well -> use a colorblind-safe palette with fewer saturated hues, add direct endpoint labels where possible, and simplify/remove the large legend box.
- STRENGTHS: Log-scaled x-axis is appropriate for the compression story, the shaded spec/facts region is useful, and axes are generally labeled clearly with readable typography.
- IDEAL VERSION: A clean log-x plot with one prominent aggregate compression curve plus faint subject-level traces, a subtle shaded 7–10K token band, minimal top annotations, and a compact colorblind-safe styling that remains legible in grayscale and print.

---

### fig_4_2_1_question_improvement_rates.png

**Claude Opus:**

- GRADE: B

- TOP 3 ISSUES (priority order, each one line):
  1. Color scheme not colorblind-safe (red-green combination) -> Use blue/orange/gray or another deuteranopia-friendly palette
  2. Condition labels (C2a, C4, C8, C4a) are cryptic without referring to legend/text -> Add descriptive labels or parenthetical clarifications directly on x-axis
  3. Footer metadata clutters the figure and duplicates caption content -> Move median Δ statistics to caption or results text

- STRENGTHS: Clean stacked-bar design with clear percentage annotations, appropriate 0-100% scale, and informative subtitle providing essential experimental context.

- IDEAL VERSION: A stacked horizontal or vertical bar chart using a colorblind-safe palette (e.g., blue/gray/orange), with fully descriptive x-axis condition labels, percentage annotations retained, and supplementary statistics moved to the caption.

**GPT-5.4:**

- GRADE: B
- TOP 3 ISSUES (priority order, each one line):
  1. Title/caption information is overloaded inside the plot area, making the main message harder to scan -> move sample details and rubric/baseline notes to the caption, keep a short title such as “Per-question outcome vs. C5 baseline”.
  2. Stacked bars make cross-condition comparison of Tied/Worsened segments less precise and the key claim (improvement rate) is visually diluted -> sort bars by Improved share and directly emphasize the green percentages, or use a horizontal 100% stacked layout with the Improved segment first and the headline comparison called out.
  3. Red–green encoding is not fully colorblind-safe and may reproduce poorly in grayscale -> switch to a colorblind-safe palette (e.g., blue/gray/orange) and/or add subtle hatching for one non-improved category.
- STRENGTHS: Clear 0–100% axis, direct in-bar percentages, and clean overall construction make the figure understandable without much caption support.
- IDEAL VERSION: A compact 100% stacked bar chart with bars ordered by improvement rate, a short title, colorblind-safe blue/gray/orange fills with direct percentage labels, a small unobtrusive legend, and all methodological details moved to the caption or figure note.

---

## Cross-cutting observations

Patterns that repeat across the set:

- **Colorblind / print safety.** Flagged on 9 of 14 figures (fig2, fig4, fig5, fig6, fig8, fig9, fig10, fig11, fig_4_1, fig_4_2, fig_4_2_1). The recurring concern is orange+blue or red+green pairs without redundant shape/pattern encoding, and scales like viridis are recommended where >2 series exist.
- **Caption / figure mismatch.** Flagged on 4 figures and is the most serious class of issue: fig3 shows 68%/11% while the caption (and paper text) claims 93%/53%; fig4 shows a two-bar "With/Without Spec" 51/31 chart while the caption describes three conditions (C5/C2a/C4a) under two classifier rules; fig5 labels conditions "Baseline, Spec, Wrong Spec..." instead of the caption's C1-C9; fig7 caption names 5 systems including Base Layer, figure shows 4 with no Base Layer; fig8 caption says 6-judge panel, figure shows 7 (includes Gem Pro).
- **Oversized titles and presentation-style typography.** Flagged on fig2, fig3, fig4, fig7, fig8, fig9, fig_4_1, fig_4_2, fig_4_2_1. The set reads as slide-deck rather than two-column conference paper in several places: long sentence titles, heavy gridlines, large markers, large legends.
- **Unexplained reference lines / shaded regions.** fig1 and fig_4_1 have a vertical dashed line at x=2.4 with no in-plot explanation; fig9 has an unlabeled threshold line; fig_4_2 has "C5 / Spec / Facts / Raw Corpus" top labels without defined regions.
- **Annotation / label clutter.** fig1 labels only 5 of 14 points inconsistently; fig_4_1 labels every point with visible overlap; fig2 has inconsistent italic callouts; fig_4_2 has 10-line legend competing with data; fig4 has an "39% reduction" arrow callout.
- **Axis-scale concerns.** fig5 y-axis starts at ~1.0 instead of 0 (potential effect-size exaggeration); fig6 x-axis is labeled 1-5 but plots from ~0.5; fig8 colorbar is truncated near 1.0 so cell-to-cell variation is visually amplified.
- **Condition-code legibility.** fig2, fig5, fig_4_2_1 use bare condition codes (C2a, C4, C8, C4a) with no in-figure mapping; readers must flip to the paper text.

## Prioritized fix list

**Critical (fix before publication):**
- **fig3_retrieval_disagreement** — values (68%/11%) do not match the paper's stated 93%/53%. Either the figure or the text is wrong; resolve before submission. Also add a one-line definition of "disagreement" in-figure.
- **fig4_hedging_reduction** — figure does not show what the caption describes (two bars vs three conditions × two classifier rules). Regenerate as a grouped bar chart with x=C5/C2a/C4a and two series (narrow/broader rule) matching the paper numbers exactly.
- **fig5_condition_effects** — caption describes "condition-by-condition mean deltas across C1-C9" but figure shows 5 named conditions. Either relabel x-axis to C1-C9 codes with a mapping legend or rewrite the caption to describe what is actually plotted. Also fix the y-axis starting at ~1.0.
- **fig7_memory_systems** — caption promises 5 systems including Base Layer; figure has 4 and no Base Layer. Either add Base Layer or correct the caption. Also switch from "absolute scores + percent callout" to a direct C3-C1 delta plot matching the paper's framing.
- **fig8_judge_agreement** — caption says 6-judge panel; heatmap shows 7 (includes Gem Pro). Reconcile, and normalize naming ("Gem Flash" / "Gem Pro" vs "GPT-4o" / "GPT-5.4").

**High (noticeably improves the paper):**
- **fig1_global_gradient** / **fig_4_1_gradient_scatter** — explain or remove the unlabeled dashed line at x=2.4; move per-point labels to a consistent repel/selective scheme; consider a direct delta-vs-baseline view so the negative gradient reads without caption support.
- **All figures** — swap orange/blue or red/green pairs for a colorblind-safe palette (blue/orange with shape redundancy, or viridis where >2 series). Ensure grayscale legibility; add hatch patterns where color alone carries the signal.
- **fig_4_2_compression** — 10-subject palette is too dense; emphasize an aggregate trend line and fade per-subject traces, or move per-subject detail to an appendix small-multiples panel.
- **fig10_letta_scaling** — left panel overlays two relationships on one y-axis; a dumbbell/slope view per subject reads more cleanly.
- **fig11_tier2_replication** — add error bars or CIs; the replication story is weaker without any uncertainty visible.
- **fig6_wrong_spec_control** — sort rows by correct-wrong gap and add within-row connectors so the "wrong-spec ≈ baseline" pattern is immediately legible.
- **fig9_cultural_baseline** — sort bars strictly by baseline score; relabel the orange/blue legend so it matches the threshold criterion it encodes.

**Low (polish only, can defer):**
- Shrink oversized titles across the set to conference-paper scale; reduce heavy gridlines to light gray.
- Move interpretive text ("holds in 5 of 6 cells", "39% reduction", median Δ statistics on fig_4_2_1) out of the plot area and into captions.
- Replace cryptic axis labels ("Δ_C4a (facts + spec vs baseline)", "Spec Condition Score", "Block / spec size") with fully spelled-out descriptions.
- Normalize model-name typography across all figures ("Gemini Flash" vs "Gem Flash", consistent GPT/Claude casing).

## Overall verdict

The figure set is **not publication-ready**. The core problem is not aesthetics — it is that five figures (fig3, fig4, fig5, fig7, fig8) disagree with their own captions or with numbers stated in the paper text, which is a correctness-level issue rather than a polish issue. Grades cluster at B with two C's and one D, and both vision models independently flag the same mismatches, so this is not a single-reviewer quirk. Minimum fix list to reach publication-ready: (1) reconcile the five caption/figure mismatches by regenerating or rewriting, (2) swap the remaining orange/blue or red/green palettes for a colorblind- and grayscale-safe set with redundant shape/pattern encoding, (3) explain or remove the unlabeled reference lines on fig1 and fig_4_1. The High-priority list would raise the set from "acceptable" to "strong", but the Critical list is non-negotiable — reviewers will flag the caption mismatches on first read.

