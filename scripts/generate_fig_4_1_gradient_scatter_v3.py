"""
Figure 4.1 v3: Cross-Subject Gradient scatter — publication polish.

Changes from v2 (2026-04-23 final polish pass):
1. Shared typography (14pt title bold, 12pt labels, 10pt ticks, 10pt annotations) via
   scripts/_figure_style.py.
2. Shared palette: BAND_LOW (blue), BAND_MID (orange), BAND_FRANKLIN (magenta),
   COLOR_ZERO_LINE (red) match the Beyond Recall figure palette doc.
3. Zitkala-Sa and Equiano label offsets adjusted so they do not overlap the mid-baseline
   square cluster at x=2.3-2.8, y=-0.35.
4. How-to-read box kept but shrunk to stay within ~8% of figure area.
5. dpi=300 confirmed on savefig.

Mechanical link (2026-05-13): the scatter values and regression parameters are now
loaded from docs/research/v11_emit/4_1_gradient.json (produced by
scripts/_v11_emit_4_1_gradient.py from primary results/ judgment data) instead of
hardcoded Python literals. Plotted values are unchanged: the emit JSON carries the
same C5 and delta_C4a values that were previously hand-transcribed, at full
precision; this script rounds them to the 2-decimal display precision used before.

Output: figures/fig_4_1_gradient_scatter_v3.png
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import (
    apply_style,
    BAND_LOW, BAND_MID, BAND_FRANKLIN,
    COLOR_ZERO_LINE, COLOR_IMPROVED, COLOR_WORSENED,
    COLOR_NEUTRAL_BAND,
    SIZE_ANNOTATION, SIZE_ANNOTATION_SMALL, SIZE_LEGEND, SIZE_FOOTER,
)

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'
DATA_PATH = REPO / 'docs' / 'research' / 'v11_emit' / '4_1_gradient.json'

apply_style()

# Display-name overrides where the figure's label text differs from the emit
# JSON's display_name (the JSON has no accent on Diaz; Franklin carries the
# "(control)" tag only in the figure).
DISPLAY_OVERRIDE = {
    'franklin': 'Franklin (control)',
}


def load_subjects():
    """Load the per-subject scatter rows and regression block from the emit JSON.

    Returns (subjects, regression) where subjects is a list of
    (display_name, C5, delta_C4a, band) tuples in the JSON's order, and
    regression is the regression_delta_on_C5 dict.
    """
    data = json.load(open(DATA_PATH, encoding='utf-8'))
    low_ids = set(data['summary']['low_baseline_subjects'])
    rows = []
    for s in data['subjects']:
        sid = s['id']
        if sid == 'franklin':
            band = 'franklin'
        elif sid in low_ids:
            band = 'low'
        else:
            band = 'mid'
        name = DISPLAY_OVERRIDE.get(sid, s['display_name'])
        rows.append((name, round(s['C5'], 2), round(s['delta_C4a'], 2), band))
    return rows, data['summary']['regression_delta_on_C5']


SUBJECTS, REGRESSION = load_subjects()

COLORS  = {'low': BAND_LOW,  'mid': BAND_MID,  'franklin': BAND_FRANKLIN}
MARKERS = {'low': 'o',       'mid': 's',       'franklin': 'D'}
LABELS  = {
    'low':      'Low-baseline (C5 <= 2.0)',
    'mid':      'Mid-baseline (2.0 < C5 < 3.0)',
    'franklin': 'Franklin (high-baseline control)',
}

# Label offsets tuned to avoid the mid-baseline cluster at x=2.3-2.8, y=-0.35
LABEL_OFFSETS = {
    'Ebers':              (10,   6),
    'Hamerton':           (10,   6),
    'Babur':              (12,  -2),
    'Zitkala-Sa':         (8,   8),
    'Equiano':            (10, -14),
    'Franklin (control)': (-8,  12),
}
LABELED = set(LABEL_OFFSETS.keys())


def main():
    fig, ax = plt.subplots(figsize=(10.5, 6.4))

    slope = round(REGRESSION['slope'], 2)
    intercept = round(REGRESSION['intercept'], 2)
    r_squared = round(REGRESSION['r_squared'], 2)
    x_line = np.linspace(0.8, 4.2, 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color='#555555', linestyle='--', linewidth=1.5,
            label=f'Regression (N=14): slope {slope:.2f}, R^2 = {r_squared:.2f}, p < 0.001',
            zorder=4)

    slope_lo = round(REGRESSION['ci95_low'], 2)
    slope_hi = round(REGRESSION['ci95_high'], 2)
    y_lo = slope_lo * x_line + intercept + 0.2
    y_hi = slope_hi * x_line + intercept - 0.2
    ax.fill_between(x_line, y_lo, y_hi, color='gray', alpha=0.10,
                    label='Approximate 95% CI band', zorder=3)

    # Zero-reference and direction bands
    ax.axhline(0, color=COLOR_ZERO_LINE, linewidth=1.8, linestyle='-', alpha=0.9, zorder=5,
               label='Delta = 0 (no gain from spec + facts)')
    ax.axhspan(0.0, 1.9, facecolor=COLOR_IMPROVED, alpha=0.05, zorder=1)
    ax.axhspan(-0.7, 0.0, facecolor=COLOR_WORSENED, alpha=0.05, zorder=1)
    ax.text(4.30, 1.55, 'Delta > 0\nimprovement', fontsize=SIZE_ANNOTATION_SMALL,
            color='#2F7A2F', ha='right', va='top', fontstyle='italic', alpha=0.9)
    ax.text(4.30, -0.50, 'Delta < 0\ndegradation', fontsize=SIZE_ANNOTATION_SMALL,
            color='#9A3B3B', ha='right', va='top', fontstyle='italic', alpha=0.9)

    for band in ['low', 'mid', 'franklin']:
        xs = [c5 for (_, c5, d, b) in SUBJECTS if b == band]
        ys = [d  for (_, c5, d, b) in SUBJECTS if b == band]
        ax.scatter(xs, ys, c=[COLORS[band]], marker=MARKERS[band], s=130,
                   edgecolors='black', linewidths=0.8, label=LABELS[band], zorder=10)

    for name, c5, d, band in SUBJECTS:
        if name in LABELED:
            dx, dy = LABEL_OFFSETS[name]
            ax.annotate(name, (c5, d), xytext=(dx, dy), textcoords='offset points',
                        fontsize=SIZE_ANNOTATION_SMALL, color='#333')

    guide = (
        'How to read this figure\n'
        '- Each point = one subject.\n'
        '- X: C5 baseline (pretraining-only, 1-5).\n'
        '- Y: change from C5 to C4a (facts + spec).\n'
        '- Above red line: spec helped. Below: spec hurt.\n'
        '- Downward slope: less known, more spec lift.'
    )
    ax.text(
        0.015, 0.025, guide, transform=ax.transAxes,
        fontsize=8.5, color='#222', va='bottom', ha='left',
        bbox=dict(boxstyle='round,pad=0.38', facecolor=COLOR_NEUTRAL_BAND,
                  edgecolor='#BBBBBB', linewidth=0.7, alpha=0.97),
    )

    ax.set_xlabel('C5 baseline (pretraining-only prediction score, 1-5 rubric)')
    ax.set_ylabel('Delta from baseline: C4a (facts + spec) - C5  (points on 1-5 rubric)')
    ax.set_title('Figure 4.1: The cross-subject gradient  (5-judge primary, N = 14 main + Franklin control)')
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.legend(loc='upper right', fontsize=SIZE_LEGEND - 1, framealpha=0.95,
              edgecolor='#CCCCCC')
    ax.set_xlim(0.6, 4.4)
    ax.set_ylim(-0.7, 1.9)

    ax.axvspan(0.7, 2.0, alpha=0.06, color=BAND_LOW)
    ax.text(1.35, 1.84, 'Low-baseline slice\n(C5 <= 2.0)', fontsize=SIZE_ANNOTATION_SMALL,
            color='#333', ha='center', va='top', fontstyle='italic')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_1_gradient_scatter_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
