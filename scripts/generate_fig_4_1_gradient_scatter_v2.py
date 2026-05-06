"""
Figure 4.1 v2: Cross-Subject Gradient scatter.

S114 author annotations (docs/reviews/s114_word_annotations.md §4.1):
- "May want to make 0 on the delta axis a different color."
- "Likely need to specify >0 means improvement <0 means degradation."
- "Would appreciate a better description on the chart, what is the chart/figure saying exactly.
   Give a guide to reading it."

Changes from v1:
1. Δ=0 reference line now drawn in a distinct color (red-ish) instead of black; clearly labeled
   "Δ = 0 (no gain from spec + facts)" with explicit ">0 = improvement / <0 = degradation".
2. Added a small on-chart "how to read this" box that states the question, the axes, and the
   takeaway in one glance.
3. Legend entries reworded to make direction of Δ explicit.
4. Underlying data, regression line, and per-subject colors unchanged (author did NOT ask to
   rescale or relabel the scatter itself).

Do NOT replace fig_4_1_gradient_scatter.png. Saves as fig_4_1_gradient_scatter_v2.png.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'

sns.set_theme(context='paper', style='whitegrid', palette='colorblind')
plt.rcParams.update({
    'font.size': 9,
    'axes.titlesize': 10.5,
    'axes.labelsize': 9.5,
    'legend.fontsize': 8,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
})
CB = sns.color_palette('colorblind')
BLUE    = CB[0]   # low-baseline
ORANGE  = CB[1]   # mid-baseline
CRIMSON = CB[3]   # Franklin (high-baseline control)
ZERO_COLOR = '#C44E52'  # distinct red for Δ=0 reference (author request)

# Same 5-judge primary gradient data as v1 (author did not contest the values).
SUBJECTS = [
    ('Ebers', 1.02, 1.05, 'low'),
    ('Sunity Devee', 1.03, 1.38, 'low'),
    ('Hamerton', 1.26, 1.51, 'low'),
    ('Fukuzawa', 1.67, 1.11, 'low'),
    ('Bernal Diaz', 1.70, 0.78, 'low'),
    ('Babur', 1.76, 0.25, 'low'),
    ('Seacole', 1.77, 0.82, 'low'),
    ('Keckley', 1.84, 0.59, 'low'),
    ('Yung Wing', 1.88, 0.52, 'low'),
    ('Zitkala-Sa', 2.34, -0.32, 'mid'),
    ('Cellini', 2.38, 0.15, 'mid'),
    ('Rousseau', 2.44, 0.10, 'mid'),
    ('Augustine', 2.58, 0.11, 'mid'),
    ('Equiano', 2.77, -0.35, 'mid'),
    ('Franklin (control)', 3.77, -0.13, 'franklin'),
]

COLORS  = {'low': BLUE,    'mid': ORANGE, 'franklin': CRIMSON}
MARKERS = {'low': 'o',     'mid': 's',    'franklin': 'D'}
LABELS  = {
    'low':      'Low-baseline (C5 ≤ 2.0)',
    'mid':      'Mid-baseline (2.0 < C5 < 3.0)',
    'franklin': 'Franklin (high-baseline control)',
}

# Labels for selected subjects (endpoints + anomalies)
LABEL_OFFSETS = {
    'Ebers':              (10,  6),
    'Hamerton':           (10,  6),
    'Babur':              (10, -4),
    'Zitkala-Sa':         (-8, -14),
    'Equiano':            (8, -14),
    'Franklin (control)': (-8,  10),
}
LABELED = set(LABEL_OFFSETS.keys())


def main():
    fig, ax = plt.subplots(figsize=(9.4, 6.0))

    # Regression on main-gradient N=14 (excluding Franklin)
    slope = -0.96
    intercept = 2.36
    x_line = np.linspace(0.8, 4.2, 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color='gray', linestyle='--', linewidth=1.3,
            label='Regression (N=14): slope −0.96, R² = 0.82, p < 0.001', zorder=4)

    # Approximate 95% CI band
    slope_lo, slope_hi = -1.24, -0.67
    y_lo = slope_lo * x_line + intercept + 0.2
    y_hi = slope_hi * x_line + intercept - 0.2
    ax.fill_between(x_line, y_lo, y_hi, color='gray', alpha=0.10,
                    label='Approximate 95% CI band', zorder=3)

    # Δ=0 reference (distinct color + explicit label)
    ax.axhline(0, color=ZERO_COLOR, linewidth=1.6, linestyle='-', alpha=0.85, zorder=5,
               label='Δ = 0 (no gain from spec + facts)')

    # Shaded direction annotations: light green above 0, light red below 0
    ax.axhspan(0.0, 1.9, facecolor='#2CA02C', alpha=0.04, zorder=1)
    ax.axhspan(-0.7, 0.0, facecolor=ZERO_COLOR, alpha=0.04, zorder=1)
    ax.text(4.30, 1.55, 'Δ > 0\nimprovement', fontsize=8, color='#2F7A2F',
            ha='right', va='top', fontstyle='italic', alpha=0.85)
    ax.text(4.30, -0.50, 'Δ < 0\ndegradation', fontsize=8, color='#9A3B3B',
            ha='right', va='top', fontstyle='italic', alpha=0.85)

    # Plot points by band
    for band in ['low', 'mid', 'franklin']:
        xs = [c5 for (_, c5, d, b) in SUBJECTS if b == band]
        ys = [d  for (_, c5, d, b) in SUBJECTS if b == band]
        ax.scatter(xs, ys, c=[COLORS[band]], marker=MARKERS[band], s=110,
                   edgecolors='black', linewidths=0.7, label=LABELS[band], zorder=10)

    # Subject labels
    for name, c5, d, band in SUBJECTS:
        if name in LABELED:
            dx, dy = LABEL_OFFSETS[name]
            ax.annotate(name, (c5, d), xytext=(dx, dy), textcoords='offset points',
                        fontsize=7.5, color='#333')

    # How-to-read box (author: "give a guide to reading it")
    guide = (
        'How to read this figure\n'
        '—————————————\n'
        '• Each point = one subject.\n'
        '• X-axis: pretraining-only baseline score (C5). Lower = model knows the\n'
        '  person less.\n'
        '• Y-axis: change in score when the Behavioral Spec + facts are added (C4a − C5).\n'
        '  Above the red line = spec helped. Below = spec hurt.\n'
        '• The downward slope means: the less the model already knows about a subject,\n'
        '  the more the spec helps.'
    )
    ax.text(
        0.02, 0.02, guide, transform=ax.transAxes,
        fontsize=7.2, color='#222', va='bottom', ha='left',
        bbox=dict(boxstyle='round,pad=0.45', facecolor='#FAFAFA',
                  edgecolor='#BBBBBB', linewidth=0.6, alpha=0.96),
    )

    # Formatting
    ax.set_xlabel('C5 baseline (pretraining-only prediction score, 1-5 rubric)')
    ax.set_ylabel('Δ from baseline: C4a (facts + spec) − C5  (points on 1-5 rubric)')
    ax.set_title('Figure 4.1 — The cross-subject gradient  (5-judge primary, N = 14 main + Franklin control)')
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.95, edgecolor='#CCCCCC')
    ax.set_xlim(0.6, 4.4)
    ax.set_ylim(-0.7, 1.9)

    # Low-baseline band shading (kept from v1)
    ax.axvspan(0.7, 2.0, alpha=0.06, color=BLUE)
    ax.text(1.35, 1.84, 'Low-baseline slice\n(C5 ≤ 2.0)', fontsize=7.5, color='#333',
            ha='center', va='top', fontstyle='italic')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_1_gradient_scatter_v2.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
