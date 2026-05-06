"""
Figure 5 v3: Per-condition lift / tie / loss rates — publication polish.

Changes from v2:
1. Shared typography (14/12/10) + palette via _figure_style.py.
2. COLOR SEMANTICS FIX: % improved is GREEN, % worsened is RED, tied is gray, Mean Delta
   is distinct BLUE. Same encoding as Fig 4.2.1, matches Fig 4.1 direction colors.
3. GN-style bar-value labels at the top of each bar (no change from v2, reinforced).
4. In-chart n= strip under xticks (GN style).
5. Vertical orientation preserved: 5 conditions with a left-to-right compression narrative.
6. Mean Delta bbox styling tightened so it does not occlude bars.
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

CONDITION_ORDER = ['C2a', 'C4', 'C8', 'C4a', 'C9']
CONDITION_LABELS = {
    'C2a': 'spec alone\n(C2a)\n~7K tok',
    'C4':  'facts alone\n(C4)\n~10K tok',
    'C8':  'raw corpus\n(C8)\n~34-550K tok',
    'C4a': 'facts + spec\n(C4a)\n~17K tok',
    'C9':  'corpus + spec\n(C9)\n~40-550K tok',
}


def main():
    data = json.load(open(DATA_PATH))

    imp = np.array([data[c]['improved_pct'] for c in CONDITION_ORDER])
    tie = np.array([data[c]['tied_pct']     for c in CONDITION_ORDER])
    wor = np.array([data[c]['worsened_pct'] for c in CONDITION_ORDER])
    mean_d = np.array([data[c]['mean_delta'] for c in CONDITION_ORDER])
    totals = [data[c]['total'] for c in CONDITION_ORDER]

    x = np.arange(len(CONDITION_ORDER))
    w = 0.26

    fig, ax = plt.subplots(figsize=(13, 6.8))

    b_imp = ax.bar(x - w, imp, w, color=COLOR_IMPROVED, edgecolor='black', linewidth=0.6,
                   label='% improved (Delta > 0)')
    b_tie = ax.bar(x,     tie, w, color=COLOR_TIE, edgecolor='black', linewidth=0.6,
                   hatch='..', label='% tied (Delta = 0)')
    b_wor = ax.bar(x + w, wor, w, color=COLOR_WORSENED, edgecolor='black', linewidth=0.6,
                   hatch='//', label='% worsened (Delta < 0)')

    def _label(bars, color='#222'):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + 1.2, f'{h:.1f}%',
                    ha='center', va='bottom', fontsize=SIZE_ANNOTATION_SMALL,
                    fontweight='bold', color=color)
    _label(b_imp); _label(b_tie); _label(b_wor)

    # Mean Delta trend on secondary axis (BLUE — does not collide with RED worsened)
    ax2 = ax.twinx()
    ax2.plot(x, mean_d, marker='D', linestyle='-', color=COLOR_MEAN_DELTA, linewidth=1.8,
             markersize=10, markeredgecolor='white', markeredgewidth=1.2,
             label='Mean Delta vs. C5 (right axis)', zorder=10)
    for xi, v in zip(x, mean_d):
        ax2.annotate(f'Delta = +{v:.2f}', (xi, v), xytext=(0, 12),
                     textcoords='offset points',
                     ha='center', fontsize=SIZE_ANNOTATION_SMALL, fontweight='bold',
                     color=COLOR_MEAN_DELTA,
                     bbox=dict(boxstyle='round,pad=0.22', facecolor='white',
                               edgecolor=COLOR_MEAN_DELTA, linewidth=0.7, alpha=0.95))
    ax2.set_ylabel('Mean Delta score vs. C5 baseline  (1-5 rubric)',
                   color=COLOR_MEAN_DELTA)
    ax2.tick_params(axis='y', labelcolor=COLOR_MEAN_DELTA)
    ax2.set_ylim(0, 1.5)
    ax2.grid(False)
    ax2.spines['top'].set_visible(False)

    ax.set_xticks(x)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER])
    ax.set_ylabel('Share of low-baseline questions  (%)')
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_title('Figure 5: Aggregate lift, tie, and loss per condition vs. C5 baseline  (low-baseline slice, 5-judge primary)',
                 pad=18)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)

    # In-chart n= strip
    for xi, c in zip(x, CONDITION_ORDER):
        ax.annotate(f'n = {totals[CONDITION_ORDER.index(c)]}',
                    (xi, -0.05), xytext=(0, -60), textcoords='offset points',
                    ha='center', fontsize=SIZE_FOOTER, color='#444',
                    xycoords=('data', 'axes fraction'))

    # Combine legends
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='upper left', framealpha=0.95,
              edgecolor='#CCCCCC', ncol=1)

    footer = ('Low-baseline slice (n = 9 subjects). 5-judge primary, per-question means. '
              'Baseline = C5 (no context). '
              'Babur excluded from C9 (422,772-word corpus exceeds context window).')
    fig.text(0.5, 0.005, footer, ha='center', fontsize=SIZE_FOOTER, color='#444',
             fontstyle='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig5_condition_effects_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
