"""
Figure 4.2 v3: Hamerton compression — publication polish.

Changes from v2:
1. Shared typography (14/12/10 via _figure_style.py).
2. Shared palette (baseline gray, spec blue, facts orange, facts+spec green, corpus red,
   corpus+spec purple). No color-concept collisions with other figures.
3. Guide callout "spec alone (7K tok) outscores raw corpus (34K tok)" now rides the
   arc arrow between the two points it references, not floating far to the left.
4. Leader-line offsets tuned so callouts no longer cross.
5. Wider figsize (10.5 x 5.8) to accommodate 14pt fonts without crowding.
6. dpi=300.
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import (
    apply_style,
    COLOR_BASELINE, COLOR_MEAN_DELTA,
    SIZE_ANNOTATION_SMALL, SIZE_LEGEND,
)

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'

apply_style()

# Per-condition markers + colors (paper's per-condition encoding; distinct within figure)
POINTS = [
    # code,  tokens,  score,  marker, color,  family
    ('C5 (baseline)',     40,    1.25, 'X', COLOR_BASELINE, 'No context'),
    ('C2a (spec alone)',  7320,  3.04, 'o', '#2E86AB',      'Spec alone'),
    ('C4 (facts alone)',  7723,  2.53, 'D', '#F18F01',      'Facts alone'),
    ('C4a (facts+spec)',  16874, 3.22, '^', '#2F9E44',      'Facts + spec'),
    ('C8 (raw corpus)',   34168, 2.32, 's', '#C44E52',      'Raw corpus'),
    ('C9 (corpus+spec)',  41452, 3.22, 'P', '#6A4C93',      'Corpus + spec'),
]


def main():
    fig, ax = plt.subplots(figsize=(10.5, 6.4))

    ax.axhline(1.25, color='#BBBBBB', linestyle=':', linewidth=1.1, zorder=1,
               label='C5 baseline (1.25, no context)')

    for label, toks, score, marker, color, family in POINTS:
        ax.scatter(toks, score, marker=marker, s=230, color=color,
                   edgecolors='black', linewidths=0.9, zorder=5,
                   label=f'{label} = {score:.2f}')

    # Leader-line offsets. Arrow-less labels placed closer to points; arrowed ones
    # pulled further to avoid overlap in the dense 7-17K token band.
    offset_map = {
        # (dx, dy, arrow)
        'C5 (baseline)':    (  60,  16, True),
        'C2a (spec alone)': ( -95,  48, True),
        'C4 (facts alone)': ( -90, -46, True),
        'C4a (facts+spec)': (   0,  42, False),
        'C8 (raw corpus)':  (   0, -38, False),
        'C9 (corpus+spec)': (  50,  30, True),
    }
    for label, toks, score, marker, color, family in POINTS:
        dx, dy, arrow = offset_map[label]
        tok_str = f'~{toks/1000:.1f}K tok' if toks >= 1000 else f'~{toks} tok'
        ann = f'{label}\n{tok_str}, score {score:.2f}'
        ax.annotate(
            ann, (toks, score), xytext=(dx, dy), textcoords='offset points',
            ha='center', fontsize=SIZE_ANNOTATION_SMALL, color='#222',
            bbox=dict(boxstyle='round,pad=0.32', facecolor='white',
                      edgecolor='#BBBBBB', linewidth=0.7, alpha=0.97),
            arrowprops=dict(arrowstyle='-', color='#999', linewidth=0.8) if arrow else None,
        )

    # Guide arrow + callout: spec alone outscores raw corpus despite ~5x less context.
    # Arc arrow above points (rad positive) from C8 point to C2a point.
    ax.annotate('',
                xy=(7320, 3.04), xycoords='data',
                xytext=(34168, 2.32), textcoords='data',
                arrowprops=dict(arrowstyle='->', color='#777777', linewidth=1.2,
                                linestyle='--', connectionstyle='arc3,rad=0.45'),
                zorder=2)
    # Callout text placed above the arc, between C2a and C8 horizontally.
    ax.text(15500, 3.92,
            'spec alone (~7K tok) outscores raw corpus (~34K tok)',
            fontsize=SIZE_ANNOTATION_SMALL, color='#444', fontstyle='italic', ha='center',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='#FFFEF5',
                      edgecolor='#D8C88A', linewidth=0.7, alpha=0.96))

    ax.set_xscale('log')
    ax.set_xlabel('Context size served to the response model (tokens, log scale)')
    ax.set_ylabel('5-judge primary score (1-5 rubric)')
    ax.set_title('Figure 4.2: Hamerton score vs. context size across 5 context strategies + baseline')
    ax.grid(True, alpha=0.3, linewidth=0.5, which='both')
    ax.set_ylim(0.5, 4.3)
    ax.set_xlim(20, 200000)

    ax.legend(loc='lower right', fontsize=SIZE_LEGEND - 1, framealpha=0.96,
              edgecolor='#CCCCCC', ncol=1, title='Condition (score)')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_compression_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
