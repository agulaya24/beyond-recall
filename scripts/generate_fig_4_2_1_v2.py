"""
Figure 4.2.1 v2: Per-question outcome distribution — movement across conditions.

S114 author annotation (docs/reviews/s114_word_annotations.md §4.2.1):
- "I understand the numbers this is [showing], but it doesn't make it obvious how it's
   improving. May want to have a line dot plot or something moving from condition to
   condition. Something that shows raw corpus as the first condition. Depending if we want
   to focus on the compression story or something else."

Changes from v1:
1. Layout is now a line/dot plot with condition on x-axis, showing MOVEMENT of the three
   outcome percentages (improved, tied, worsened) as we move across conditions.
2. Condition order on x-axis: C8 (raw corpus), C2a (spec), C4 (facts), C4a (facts+spec),
   C9 (corpus+spec). Per task: "raw corpus (C8) should appear as the first condition on the
   x-axis, then C2a, then C4, then C4a, then C9."
3. A mean Δ trend line plotted on a secondary axis makes the compression story readable:
   spec alone (C2a) is within 7 pp of raw corpus on improvement rate at 1/5 the context,
   and corpus+spec stacks additively.
4. Small inline value labels retained so individual percentages stay readable.

Data source: scripts/_per_question_outcomes_v2.json (computed by
_compute_per_question_v2.py from the same raw judgment JSON the paper's §4.2.1 table uses).
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
COLOR_IMPROVED = CB[0]   # blue
COLOR_TIE      = '#8F8F8F'
COLOR_WORSE    = CB[1]   # orange
COLOR_MEAN     = CB[3]   # red/purple for mean Δ trend line

CONDITION_ORDER = ['C8', 'C2a', 'C4', 'C4a', 'C9']
CONDITION_LABELS = {
    'C8':  'C8\nraw corpus\n(~34-550K tok)',
    'C2a': 'C2a\nspec alone\n(~7K tok)',
    'C4':  'C4\nfacts alone\n(~10K tok)',
    'C4a': 'C4a\nfacts + spec\n(~17K tok)',
    'C9':  'C9\ncorpus + spec\n(~40-550K tok)',
}


def main():
    data = json.load(open(DATA_PATH))

    imp = [data[c]['improved_pct'] for c in CONDITION_ORDER]
    tie = [data[c]['tied_pct']     for c in CONDITION_ORDER]
    wor = [data[c]['worsened_pct'] for c in CONDITION_ORDER]
    mean_d = [data[c]['mean_delta'] for c in CONDITION_ORDER]
    totals = [data[c]['total'] for c in CONDITION_ORDER]

    x = np.arange(len(CONDITION_ORDER))

    fig, ax = plt.subplots(figsize=(11, 6.2))

    # --- Three lines: improved / tied / worsened percentages ---
    ax.plot(x, imp, marker='o', color=COLOR_IMPROVED, linewidth=2.2, markersize=11,
            markeredgecolor='white', markeredgewidth=1.2,
            label='Improved (Δ > 0 vs. C5 baseline)', zorder=6)
    ax.plot(x, tie, marker='s', color=COLOR_TIE, linewidth=1.8, markersize=9,
            markeredgecolor='white', markeredgewidth=1.0,
            label='Tied (Δ = 0)', zorder=5)
    ax.plot(x, wor, marker='v', color=COLOR_WORSE, linewidth=2.0, markersize=11,
            markeredgecolor='white', markeredgewidth=1.2,
            label='Worsened (Δ < 0)', zorder=6)

    # Value labels
    for xi, v in zip(x, imp):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, 12), textcoords='offset points',
                    ha='center', fontsize=9, fontweight='bold', color=COLOR_IMPROVED)
    for xi, v in zip(x, tie):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, -14), textcoords='offset points',
                    ha='center', fontsize=8.2, color='#555')
    for xi, v in zip(x, wor):
        ax.annotate(f'{v:.1f}%', (xi, v), xytext=(0, -14), textcoords='offset points',
                    ha='center', fontsize=9, fontweight='bold', color=COLOR_WORSE)

    # --- Trend line for mean Δ on secondary axis ---
    ax2 = ax.twinx()
    ax2.plot(x, mean_d, marker='D', linestyle='--', color=COLOR_MEAN, linewidth=1.4,
             markersize=7, alpha=0.85, zorder=4,
             label='Mean Δ vs. C5 (points on 1-5 rubric, right axis)')
    for xi, v in zip(x, mean_d):
        ax2.annotate(f'+{v:.2f}', (xi, v), xytext=(12, -4), textcoords='offset points',
                     fontsize=7.8, color=COLOR_MEAN, fontstyle='italic')
    ax2.set_ylabel('Mean Δ score vs. C5 baseline', color=COLOR_MEAN, fontsize=9.5)
    ax2.tick_params(axis='y', labelcolor=COLOR_MEAN, labelsize=8.5)
    ax2.set_ylim(0, 1.4)
    ax2.grid(False)

    # Main axis formatting
    ax.set_xticks(x)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITION_ORDER], fontsize=8.8)
    ax.set_ylabel('Share of low-baseline questions  (%)')
    ax.set_ylim(-4, 100)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_title('Figure 4.2.1 — Per-question outcome vs. C5 baseline: movement across five context strategies',
                 pad=12)
    ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    for spine in ('top',):
        ax.spines[spine].set_visible(False)
    for spine in ('top',):
        ax2.spines[spine].set_visible(False)

    # Combine legends
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='center right', fontsize=8.8, framealpha=0.94,
              edgecolor='#CCCCCC', ncol=1, bbox_to_anchor=(1.0, 0.48))

    # Footnote: totals per condition (C9 is n=312 because Babur's corpus exceeded context window)
    n_note = ' · '.join(f'{c}: n={t}' for c, t in zip(CONDITION_ORDER, totals))
    footer = (f'Low-baseline slice (n = 9 subjects). 5-judge primary, per-question means.  '
              f'Baseline = C5 (no context).  Counts per condition — {n_note}.  '
              f'Babur excluded from C9 (422,772-word corpus exceeds context window).')
    fig.text(0.5, 0.005, footer, ha='center', fontsize=7.5, color='#444', fontstyle='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_1_question_improvement_rates_v2.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
