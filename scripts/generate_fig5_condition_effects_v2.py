"""
Figure 5 v2: Per-condition aggregate lift / tie / loss rates with mean Δ overlay.

S114 author annotation (docs/reviews/s114_word_annotations.md §4 intro / Figure 5):
- "I understand what this is doing, for the first figure in the results, [it] should likely
   be displaying average lift/loss metrics across conditions when looking at all questions
   in aggregate. This doesn't make it immediately clear how each condition performs overall."

Changes from v1:
1. Figure now shows three side-by-side bars per condition (% improved, % tied, % worsened vs.
   C5 baseline), making per-condition performance immediately visible in aggregate.
2. A mean Δ line on a secondary axis gives the magnitude, not just the direction mix.
3. Uses the same 351-question low-baseline-slice dataset as Fig 4.2.1 (plus 312 for C9 due
   to Babur's oversized corpus), so the two figures share an anchored metric.

Data source: scripts/_per_question_outcomes_v2.json (computed from raw judgment JSONs in
results/global_<subject>/ and results/hamerton/).
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
DATA_PATH = REPO / 'scripts' / '_per_question_outcomes_v2.json'

sns.set_theme(context='paper', style='whitegrid', palette='colorblind')
plt.rcParams.update({
    'font.size': 9.5,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

CB = sns.color_palette('colorblind')
COLOR_IMPROVED = CB[0]
COLOR_TIE      = '#9E9E9E'
COLOR_WORSE    = CB[1]
COLOR_MEAN     = CB[3]

CONDITION_ORDER = ['C2a', 'C4', 'C8', 'C4a', 'C9']
CONDITION_LABELS = {
    'C2a': 'C2a\nspec alone\n(~7K tok)',
    'C4':  'C4\nfacts alone\n(~10K tok)',
    'C8':  'C8\nraw corpus\n(~34-550K tok)',
    'C4a': 'C4a\nfacts + spec\n(~17K tok)',
    'C9':  'C9\ncorpus + spec\n(~40-550K tok)',
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

    fig, ax = plt.subplots(figsize=(12, 6.4))

    b_imp = ax.bar(x - w, imp, w, color=COLOR_IMPROVED, edgecolor='black', linewidth=0.5,
                   label='% improved (Δ > 0)')
    b_tie = ax.bar(x,     tie, w, color=COLOR_TIE,      edgecolor='black', linewidth=0.5,
                   hatch='..', label='% tied (Δ = 0)')
    b_wor = ax.bar(x + w, wor, w, color=COLOR_WORSE,    edgecolor='black', linewidth=0.5,
                   hatch='//', label='% worsened (Δ < 0)')

    def _label(bars):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + 1.0, f'{h:.1f}%',
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold',
                    color='#222')
    _label(b_imp); _label(b_tie); _label(b_wor)

    # Mean Δ on secondary axis
    ax2 = ax.twinx()
    ax2.plot(x, mean_d, marker='D', linestyle='-', color=COLOR_MEAN, linewidth=1.6,
             markersize=9, markeredgecolor='white', markeredgewidth=1.1,
             label='Mean Δ vs. C5 (right axis)', zorder=10)
    for xi, v in zip(x, mean_d):
        ax2.annotate(f'Δ = +{v:.2f}', (xi, v), xytext=(0, 10), textcoords='offset points',
                     ha='center', fontsize=8.2, fontweight='bold', color=COLOR_MEAN,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                               edgecolor=COLOR_MEAN, linewidth=0.6, alpha=0.92))
    ax2.set_ylabel('Mean Δ score vs. C5 baseline  (1-5 rubric)',
                   color=COLOR_MEAN, fontsize=9.5)
    ax2.tick_params(axis='y', labelcolor=COLOR_MEAN, labelsize=8.5)
    ax2.set_ylim(0, 1.5)
    ax2.grid(False)

    # Main axis formatting
    ax.set_xticks(x)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER], fontsize=9)
    ax.set_ylabel('Share of low-baseline questions  (%)')
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_title('Figure 5 — Aggregate lift / tie / loss per condition vs. C5 baseline  (low-baseline slice, 5-judge primary)',
                 pad=14)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # Combine legends
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=9, framealpha=0.94,
              edgecolor='#CCCCCC', ncol=1)

    # Footer with n per condition
    n_note = ' · '.join(f'{c}: n={t}' for c, t in zip(CONDITION_ORDER, totals))
    footer = (f'Low-baseline slice (n = 9 subjects). 5-judge primary, per-question means. '
              f'Baseline = C5 (no context). Counts per condition — {n_note}. '
              f'Babur excluded from C9 (422,772-word corpus exceeds context window).')
    fig.text(0.5, 0.005, footer, ha='center', fontsize=7.5, color='#444', fontstyle='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig5_condition_effects_v2.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
