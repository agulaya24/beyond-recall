"""
Figure 4.1: Cross-Subject Gradient scatter.

Δ_C4a (facts+spec vs C5) on y-axis, C5 baseline on x-axis.
Points colored by band (low-baseline, mid-baseline, Franklin control).
Regression line + 95% CI band.

Data: 5-judge primary per-subject aggregates (computed in recompute_5judge_primary.py).

2026-04-22 revision: colorblind-safe palette, selective point labels with repel offsets,
explicit y=0 "no spec+facts gain" reference annotation, paper-scale typography,
Franklin control distinguished by marker shape (diamond) in addition to color.
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
GRAY    = '#7A7A7A'
CRIMSON = CB[3]   # Franklin (control)

# 5-judge primary gradient data (from recompute output)
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

# Label only notable/endpoint subjects to reduce overlap.
# Per-label (dx, dy) offsets in points, chosen so text clears its marker and neighbours.
LABEL_OFFSETS = {
    'Ebers':              (10,  6),    # push right of marker (was clipping left edge)
    'Hamerton':           (10,  6),    # push right, clear of marker
    'Babur':              (10, -4),    # right + slight down
    'Zitkala-Sa':         (-8, -14),   # below-left, clears the mid-band cluster
    'Equiano':            (8, -14),    # below-right, clears Zitkala-Sa
    'Franklin (control)': (-8,  10),   # above-left of marker
}
LABELED = set(LABEL_OFFSETS.keys())


def main():
    fig, ax = plt.subplots(figsize=(9, 5.8))

    # Regression on main-gradient N=14 (excluding Franklin for the study's reported slope)
    slope = -0.96
    intercept = 2.36
    x_line = np.linspace(0.8, 4.2, 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color='gray', linestyle='--', linewidth=1.3,
            label=f'Regression (N=14): slope −0.96, R² = 0.82')

    # Approximate 95% CI band
    slope_lo, slope_hi = -1.24, -0.67
    y_lo = slope_lo * x_line + intercept + 0.2
    y_hi = slope_hi * x_line + intercept - 0.2
    ax.fill_between(x_line, y_lo, y_hi, color='gray', alpha=0.10,
                    label='Approximate 95% CI band')

    # Plot points by band (color + marker redundancy)
    for band in ['low', 'mid', 'franklin']:
        xs = [c5 for (_, c5, d, b) in SUBJECTS if b == band]
        ys = [d  for (_, c5, d, b) in SUBJECTS if b == band]
        ax.scatter(xs, ys, c=[COLORS[band]], marker=MARKERS[band], s=105,
                   edgecolors='black', linewidths=0.7, label=LABELS[band], zorder=10)

    # Selective labels with per-subject offsets (points) to clear markers and neighbours.
    for name, c5, d, band in SUBJECTS:
        if name in LABELED:
            dx, dy = LABEL_OFFSETS[name]
            ax.annotate(name, (c5, d), xytext=(dx, dy), textcoords='offset points',
                        fontsize=7.5, color='#333')

    # y=0 reference with inline explanation (replaces orphaned x=2.4 line from earlier draft)
    ax.axhline(0, color='black', linewidth=0.5, alpha=0.6)
    ax.text(4.15, 0.03, 'Δ = 0 (no spec+facts gain)', fontsize=7, color='#555',
            ha='right', va='bottom', fontstyle='italic')

    # Formatting
    ax.set_xlabel('C5 baseline (pretraining-only prediction score, 1-5 rubric)')
    ax.set_ylabel('Δ from baseline: C4a (facts + spec) − C5 (points on 1-5 rubric)')
    ax.set_title('Figure 4.1 — The cross-subject gradient  (5-judge primary, N = 14 main + Franklin control)')
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.95, edgecolor='#CCCCCC')
    # Extra left padding so "Ebers" label (C5=1.02, leftmost point) no longer clips
    # against the plot edge. Right edge also extended slightly to keep Franklin annotation in-bounds.
    ax.set_xlim(0.6, 4.4)
    ax.set_ylim(-0.6, 1.8)

    # Shaded band at C5 ≤ 2.0 (low-baseline region) — labeled
    ax.axvspan(0.7, 2.0, alpha=0.05, color=BLUE)
    ax.text(1.35, 1.72, 'Low-baseline slice\n(C5 ≤ 2.0)', fontsize=7.5, color='#333',
            ha='center', va='top', fontstyle='italic')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_1_gradient_scatter.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')
    out_pdf = FIG_DIR / 'fig_4_1_gradient_scatter.pdf'
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_pdf}')


if __name__ == '__main__':
    main()
