# Beyond Recall — Figures v3 publication polish report

Session 2026-04-23. Final polish pass on the five v2 figures for the arXiv release.
Non-destructive: v2 assets preserved. v3 sits alongside.

---

## Shared changes applied to all five figures

1. **Typography unified via `scripts/_figure_style.py`:**
   - Title 14 pt bold
   - Axis labels 12 pt
   - Tick labels 10 pt
   - Annotations 10-11 pt
   - Legend 10 pt
   - Footer 9 pt italic
   - Font family: DejaVu Sans (matplotlib default, free, arXiv-safe)
2. **Palette unified via `docs/research/_figure_palette.md` + `scripts/_figure_style.py`:**
   - `COLOR_IMPROVED` = `#2F9E44` (green) — same semantic across all figures
   - `COLOR_WORSENED` = `#C44E52` (red) — Δ < 0 in every figure
   - `COLOR_TIE` = `#8A8A8A` (gray)
   - `COLOR_MEAN_DELTA` = `#2E86AB` (blue) — distinct from green/red direction colors
   - `COLOR_BASELINE` = `#7A7A7A` (dark gray)
   - Per-system colors (Fig 7): Mem0 blue `#2E86AB`, Letta green `#2F9E44`,
     Supermemory purple `#6A4C93`, Zep orange `#F18F01`
3. **Low-chrome style** (Gamers Nexus aggregate-benchmark reference):
   - Top + right spines removed
   - Dashed gridlines at 30% alpha, value axis only
   - Bar-value labels at the end of each bar (not floating inside)
   - In-chart `n=` counts (moved from footer to chart body) on Fig 4.2.1, Fig 5, Fig 7
4. **300 dpi confirmed on every save** via `plt.savefig(..., dpi=300, bbox_inches='tight')`.

---

## Three color-semantic bugs found in v2 and fixed in v3

Per an advisory review of v2 before polish, three collisions were identified:

### Bug 1. `% worsened` and `Mean Δ` shared a reddish hue in v2 Fig 4.2.1 / Fig 5

v2 used `CB[1]` orange for worsened and `CB[3]` red-magenta for mean Δ. At typical viewing
distance on a projector or PDF renderer they blurred together even though they encode
different concepts.

**v3 fix.** Worsened is now `#C44E52` (clean red, matching Fig 4.1's zero-line color).
Mean Δ is `#2E86AB` blue. Unambiguous and colorblind-safe.

### Bug 2. Fig 7 Supermemory panel had ambiguous positive vs negative bars

v2 Supermemory used `CB[1]` orange for positive bars and `#E07A5F` red-orange for negative
bars. Direction was visually hard to read in the Supermemory panel specifically (v2's
original issue — "Supermemory collapses to 0.00, need to see spread").

**v3 fix.** Supermemory positive bars are now purple `#6A4C93`; all negative bars in every
panel are red `#C44E52` (COLOR_WORSENED). Clear directional contrast in every panel.

### Bug 3. Fig 4.1's Δ > 0 = green rule was not applied in Fig 4.2.1 / Fig 5

v2 Fig 4.2.1 and Fig 5 used blue for improved. That's a within-figure encoding choice,
but it means the visual convention from Fig 4.1 ("green = up, red = down") did not
carry across.

**v3 fix.** Improved is now green on Fig 4.2.1 and Fig 5, matching Fig 4.1. Cross-figure
visual grammar is consistent.

---

## Per-figure polish notes

### Figure 4.1 — cross-subject gradient

- **Before:** 10/11 pt type, Zitkala-Sa and Equiano labels overlapping mid-baseline square
  cluster at x = 2.3 - 2.8, y = -0.35.
- **After:** 14/12/10 pt type. Label offsets adjusted — Zitkala-Sa pushed up+right,
  Equiano pushed down+right, both readable without overlap. How-to-read guide box tightened
  (6-line -> 6-line but shorter strings) to stay within ~7% of figure area (advisor
  budget: 8-10% max). Figsize grown to 10.5 x 6.4 in to absorb larger fonts.
- **Rendered:** `figures/fig_4_1_gradient_scatter_v3.png` (3149 x 1884 px @ 300 dpi)

### Figure 4.2 — Hamerton compression

- **Before:** Callout "spec alone (7K tok) outscores raw corpus (34K tok) on Hamerton"
  floating in top-left of plot at x=80, far from the two points (x=7300 and x=34168) it
  referenced.
- **After:** Callout placed above the arc arrow between C2a and C8, centered on the
  horizontal midpoint. The arc arrow (rad=+0.45) does the point-to-point gesture; the
  callout sits above it at y=3.92. Figsize grown to 10.5 x 6.4 in.
- **Rendered:** `figures/fig_4_2_compression_v3.png` (3107 x 1870 px @ 300 dpi)

### Figure 4.2.1 — per-question outcome movement

- **Before:** xtick labels led with the code (`C8\nraw corpus\n(~34-550K tok)`). Footer
  carried the full per-condition n-count list.
- **After:** xtick labels name-first (`raw corpus\n(C8)\n~34-550K tok`). In-chart `n =`
  strip prints under each xtick, matching GN-style benchmark charts. Improved line is
  green, worsened is red, tied is gray, Mean Δ is distinct blue.
- **Rendered:** `figures/fig_4_2_1_question_improvement_rates_v3.png` (3558 x 1993 px @ 300 dpi)

### Figure 5 — aggregate lift / tie / loss

- **Before:** Bars were blue/gray/orange. Mean Δ line used red-magenta that blurred with
  the orange worsened bars. Footer carried n-counts.
- **After:** Green improved bars, gray tied (dotted hatch), red worsened (diagonal hatch),
  blue Mean Δ line on secondary axis. Bar value labels at bar end (GN style). In-chart
  n= strip. Vertical orientation kept (5 ordered conditions, left-to-right compression
  narrative; horizontal would obscure the order story, per advisor).
- **Rendered:** `figures/fig5_condition_effects_v3.png` (3858 x 2052 px @ 300 dpi)

### Figure 7 — memory-system per-subject deltas

- **Before:** MEAN bar used dotted hatch with 1.4 pt outline — read as "just another
  bar with dots". Supermemory panel had ambiguous positive vs. negative coloring.
- **After:** MEAN bar uses a darker shade of each system color (22% darker via `darker()`
  helper), solid fill with 2.0 pt black outline — visually distinct from the per-subject
  bars. Each system has its own palette color; all negative bars are red. Per-panel
  subtitle now includes `n = 9 subjects` alongside the mean, so per-panel sample size is
  on-chart (not only in caption).
- **Rendered:** `figures/fig7_memory_systems_v3.png` (6264 x 1896 px @ 300 dpi)

---

## Gamers-Nexus style references applied

GN aggregate-benchmark charts (public examples: GN's GPU and CPU roundups) exhibit:

1. **Bar labels at the end of each bar, not inside.** Applied on Fig 5 (improved/tied/worsened
   percentages labeled above bar tips) and Fig 7 (delta values labeled at bar tips for
   both positive and negative).
2. **Sample size `n=` printed in-chart, not only in caption.** Applied on Fig 4.2.1 (per
   condition, under xticks), Fig 5 (per condition, under xticks), Fig 7 (per panel, in
   subtitle).
3. **Low-chrome layout.** Top + right spines removed across all five figures. Gridlines
   dashed at 30% alpha on value axis only.
4. **Clear zero / baseline reference.** Fig 4.1 zero line in red; Fig 4.2 C5 baseline as
   dotted line; Fig 7 zero line per panel.
5. **Mean / aggregate bar distinguished.** Fig 7 MEAN bar uses darker color + thick
   outline (GN's "average" column analog).

GN's horizontal-bar convention was considered for Fig 5 and rejected — for 5 conditions
with a left-to-right compression narrative, vertical reads cleaner. Horizontal works when
the categorical axis is unordered; here the order itself carries the story.

---

## Deliverables

| Figure | New script | Rendered image | Dimensions | File size |
|---|---|---|---|---|
| 4.1 | `scripts/generate_fig_4_1_gradient_scatter_v3.py` | `figures/fig_4_1_gradient_scatter_v3.png` | 3149 x 1884 | 461 KB |
| 4.2 | `scripts/generate_fig_4_2_compression_v3.py` | `figures/fig_4_2_compression_v3.png` | 3107 x 1870 | 381 KB |
| 4.2.1 | `scripts/generate_fig_4_2_1_v3.py` | `figures/fig_4_2_1_question_improvement_rates_v3.png` | 3558 x 1993 | 401 KB |
| 5 | `scripts/generate_fig5_condition_effects_v3.py` | `figures/fig5_condition_effects_v3.png` | 3858 x 2052 | 388 KB |
| 7 | `scripts/generate_fig7_memory_systems_v3.py` | `figures/fig7_memory_systems_v3.png` | 6264 x 1896 | 444 KB |

Plus:

- `scripts/_figure_style.py` — shared typography + palette helper
- `docs/research/_figure_palette.md` — human-readable palette + typography documentation
- `scripts/export_v9_to_docx.py` — FIGURE_MAP updated to v3 filenames;
  inline Fig 4.2.1 path rewritten in-pipeline so v9 paper body source stays untouched
- `docs/beyond_recall_v9_draft.docx` — re-rendered, 2798 KB, 10/10 figures inserted

---

## Requires author action (caption-figure mismatch, pre-existing)

The v9 paper body at line 869 has an inline caption for Fig 4.2.1 that says:

> "Stacked bars show the share of questions that improved, tied, or worsened relative
> to the no-context C5 baseline."

**This caption is stale** — the v2 rebuild (and now v3) is a line/dot plot with three
semantic lines (improved / tied / worsened) plus a Mean Δ trend on a secondary axis,
not stacked bars. It was never updated when the v2 layout changed.

The caption update is a **content claim, not cosmetic**, so it is not auto-rewritten by
the export pipeline. Recommended author edit to `docs/beyond_recall_v9_draft.md` line 869:

- Replace `Stacked bars show the share of questions` with something like `Three
  lines track the share of questions`.
- Consider mentioning the right-axis Mean Δ trend line, since it is a substantive
  element of the figure.

---

## What was considered and rejected

1. **Horizontalize Fig 5 (GN style).** Rejected — the 5 conditions carry a left-to-right
   compression narrative; horizontal would obscure that ordering. GN horizontal is for
   unordered benchmark aggregates (different GPUs side-by-side).
2. **Shared condition-color encoding across all figures.** Rejected — different figures use
   the x-axis for different encodings (subject on Fig 4.1, tokens on Fig 4.2, conditions on
   4.2.1/5, subjects on 7). Color rules apply within-encoding (Δ direction semantics), not
   cross-figure.
3. **In-figure captions.** Rejected — task spec: "Captions stay in the paper body."
4. **Deleting v2 files.** Rejected — task spec: "v3 sits alongside the v2 versions."
