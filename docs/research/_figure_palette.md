# Beyond Recall — Figure Palette and Typography (v3)

Shared rules for the five v3 main-body figures. Every v3 figure script imports these constants
from `scripts/_figure_style.py`.

Non-destructive: v2 scripts and images are left in place. v3 sits alongside.

---

## Typography

One font family across all figures: **DejaVu Sans** (matplotlib default, no install). If
Helvetica / Arial is preferred for arXiv, swap `FONT_FAMILY` in `_figure_style.py`.

| Element | Size | Weight |
|---|---|---|
| Figure title | 14 pt | bold |
| Axis labels | 12 pt | regular |
| Tick labels | 10 pt | regular |
| Annotations / in-chart text | 10-11 pt | regular |
| Legend | 10 pt | regular |
| Footer / footnote | 9 pt | italic |

Titles are the only bold element. All other text is regular weight. Em-dashes are not used;
commas, colons, or parens instead.

---

## Color palette (semantic, not categorical)

A single mapping for identical concepts across figures.

| Constant | Hex | Used for |
|---|---|---|
| `COLOR_IMPROVED` | `#2F9E44` | Δ > 0 bars, lines, and regions |
| `COLOR_WORSENED` | `#C44E52` | Δ < 0 bars, lines, and regions |
| `COLOR_TIE` | `#8A8A8A` | Δ = 0 bars and regions |
| `COLOR_ZERO_LINE` | `#C44E52` | Δ = 0 reference line (matches WORSENED) |
| `COLOR_MEAN_DELTA` | `#2E86AB` | Mean Δ trend / overlay (not semantically positive or negative) |
| `COLOR_BASELINE` | `#7A7A7A` | C5 baseline markers, reference lines |
| `COLOR_NEUTRAL_BAND` | `#FAFAFA` | How-to-read callout box fill |

### Baseline-band colors (Fig 4.1 only)

| Constant | Hex | Used for |
|---|---|---|
| `BAND_LOW` | `#2E86AB` | Low-baseline subjects (C5 <= 2.0) |
| `BAND_MID` | `#F18F01` | Mid-baseline subjects (2.0 < C5 < 3.0) |
| `BAND_FRANKLIN` | `#A23B72` | Franklin high-baseline control |

### Per-memory-system colors (Fig 7 only)

Each memory system has one color, used as the positive-bar fill. Negative bars in every
panel use `COLOR_WORSENED` (`#C44E52`) so direction reads at a glance.

| System | Hex |
|---|---|
| Mem0 | `#2E86AB` (blue) |
| Letta (archival) | `#2F9E44` (green) |
| Supermemory | `#6A4C93` (purple — deliberately non-orange to avoid collision with COLOR_WORSENED in the Supermemory panel) |
| Zep | `#F18F01` (orange) |

---

## Reserved collisions avoided

1. `% worsened` and `Mean Δ` are now different hues (`#C44E52` red vs. `#2E86AB` blue).
   In v2 both were reddish-orange and blurred on screen.
2. Fig 7 Supermemory positive bars (purple) vs negative bars (red) are now distinct;
   in v2 they were both in the orange-red band.
3. The Δ > 0 = green / Δ < 0 = red rule from Fig 4.1 now applies in Fig 4.2.1 and Fig 5
   (`% improved` = green, `% worsened` = red, `tied` = gray). `Mean Δ` overlay uses the
   distinct blue `COLOR_MEAN_DELTA`.

---

## Style rules (Gamers-Nexus-benchmark inspired, low-chrome)

- Bar-value labels render **at the end of each bar**, not floating inside. For very short
  negative bars, labels sit just past the bar tip.
- Sample size `n=` prints in the chart body (e.g., as a small data box next to the title
  row), not only in the caption or footer.
- Gridlines only on the value axis, dashed `--`, 30% alpha. No box frame — top / right
  spines removed.
- Baseline / zero line is always drawn. Always same color (`COLOR_ZERO_LINE`) across
  figures.
- Mean / aggregate bar gets a darker variant of the group color, solid fill (no hatch),
  and a 2 pt black outline to distinguish it from the per-subject bars.

---

## File convention

- Rendered images: `figures/<name>_v3.png` at `dpi=300`.
- Scripts: `scripts/generate_<name>_v3.py`, one per figure, importing from
  `scripts/_figure_style.py`.
- v2 assets left untouched for side-by-side comparison.
