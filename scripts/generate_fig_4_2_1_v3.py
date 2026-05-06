"""
Figure 4.2.1 v3: Per-question outcome movement across conditions — publication polish.

Changes from v2:
1. Shared typography (14/12/10) + palette via _figure_style.py.
2. COLOR SEMANTICS FIX: % improved is now GREEN (was blue), % worsened is RED (was orange),
   tied is gray. Mean Delta trend uses distinct BLUE. Matches Fig 4.1 green/red convention;
   eliminates prior visual collision between % worsened and Mean Delta.
3. Xtick labels re-ordered: name first, then code, then token band. "raw corpus\n(C8)\n
   ~34-550K tok" instead of "C8\nraw corpus\n(~34-550K tok)".
4. In-chart n= data strip: small text near title shows per-condition n counts, replacing
   the crowded footer footnote.
5. dpi=300.
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
    COLOR_IMPROVED, COLOR_WORSENED, COLOR_TIE, COLOR_MEAN_DELTA,
    SIZE_ANNOTATION, SIZE_ANNOTATION_SMALL, SIZE_LEGEND, SIZE_FOOTER,
)

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'
DATA_PATH = REPO / 'scripts' / '_per_question_outcomes_v2.json'

apply_style()

CONDITION_ORDER = ['C8', 'C2a', 'C4', 'C4a', 'C9']
CONDITION_LABELS = {
    'C8':  'raw corpus\n(C8)\n~34-550K tok',
    'C2a': 'spec alone\n(C2a)\n~7K tok',
    'C4':  'facts alone\n(C4)\n~10K tok',
    'C4a': 'facts + spec\n(C4a)\n~17K tok',
    'C9':  'corpus + spec\n(C9)\n~40-550K tok',
}


def main():
    data = json.load(open(DATA_PATH))

    imp = [data[c]['improved_pct'] for c in CONDITION_ORDER]
    tie = [data[c]['tied_pct']     for c in CONDITION_ORDER]
    wor = [data[c]['worsened_pct'] for c in CONDITION_ORDER]
    mean_d = [data[c]['mean_delta'] for c in CONDITION_ORDER]
    totals = [data[c]['total'] for c in CONDITION_ORDER]

    x = np.arange(len(CONDITION_ORDER))

    fig, ax = plt.subplots(figsize=(12, 6.6))

    # Three lines with semantic colors
    ax.plot(x, imp, marker='o', color=COLOR_IMPROVED, linewidth=2.4, markersize=12,
            markeredgecolor='white', markeredgewidth=1.3,
            label='Improved (Delta > 0 vs. C5 baseline)', zorder=6)
    ax.plot(x, tie, marker='s', color=COLOR_TIE, linewidth=1.8, markersize=9,
            markeredgecolor='white', markeredgewidth=1.0,
            label='Tied (Delta = 0)', zorder=5)
    ax.plot(x, wor, marker='v', color=COLOR_WORSENED, linewidth=2.2, markersize=12,
            markeredgecolor='white', markeredgewidth=1.3,
            label='Worsened (Delta < 0)', zorder=6)

    # Value labels on each line
    for xi, v in zip(x, imp):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, 13), textcoords='offset points',
                    ha='center', fontsize=SIZE_ANNOTATION, fontweight='bold',
                    color=COLOR_IMPROVED)
    for xi, v in zip(x, tie):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, -16), textcoords='offset points',
                    ha='center', fontsize=SIZE_ANNOTATION_SMALL, color='#555')
    for xi, v in zip(x, wor):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, -16), textcoords='offset points',
                    ha='center', fontsize=SIZE_ANNOTATION, fontweight='bold',
                    color=COLOR_WORSENED)

    # Mean Delta trend line on secondary axis (blue, distinct from the three semantic colors)
    ax2 = ax.twinx()
    ax2.plot(x, mean_d, marker='D', linestyle='--', color=COLOR_MEAN_DELTA, linewidth=1.6,
             markersize=8, alpha=0.9, zorder=4,
             label='Mean Delta vs. C5 (right axis)')
    for xi, v in zip(x, mean_d):
        ax2.annotate(f'+{v:.2f}', (xi, v), xytext=(12, -4), textcoords='offset points',
                     fontsize=SIZE_ANNOTATION_SMALL, color=COLOR_MEAN_DELTA,
                     fontstyle='italic')
    ax2.set_ylabel('Mean Delta score vs. C5 baseline', color=COLOR_MEAN_DELTA)
    ax2.tick_params(axis='y', labelcolor=COLOR_MEAN_DELTA)
    ax2.set_ylim(0, 1.4)
    ax2.grid(False)
    ax2.spines['top'].set_visible(False)

    # Main axis formatting
    ax.set_xticks(x)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER])
    ax.set_ylabel('Share of low-baseline questions  (%)')
    ax.set_ylim(-4, 100)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_title('Figure 4.2.1: Per-question outcome vs. C5 baseline across five context strategies',
                 pad=16)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)

    # In-chart n= strip (GN-style): per-condition counts placed under each xtick
    for xi, c in zip(x, CONDITION_ORDER):
        ax.annotate(f'n = {totals[CONDITION_ORDER.index(c)]}',
                    (xi, -0.05), xytext=(0, -52), textcoords='offset points',
                    ha='center', fontsize=SIZE_FOOTER, color='#444',
                    xycoords=('data', 'axes fraction'))

    # Combine legends
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='center right', framealpha=0.95,
              edgecolor='#CCCCCC', ncol=1, bbox_to_anchor=(1.0, 0.48))

    # Concise footer: only the excluded-subject caveat remains
    footer = ('Low-baseline slice (n = 9 subjects). 5-judge primary, per-question means. '
              'Baseline = C5 (no context). '
              'Babur excluded from C9 (422,772-word corpus exceeds context window).')
    fig.text(0.5, 0.005, footer, ha='center', fontsize=SIZE_FOOTER, color='#444',
             fontstyle='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_1_question_improvement_rates_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
