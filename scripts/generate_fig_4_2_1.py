"""
Figure 4.2.1: Per-question outcome distribution by condition.

Low-baseline slice (9 subjects, 351 questions, 5-judge primary per-question means).
Stacked-bar: Improved / Tied / Worsened percentages per condition.
Source: §4.2.1 of docs/beyond_recall_v8_draft.md (counts table, 249/49/53 etc.).

Median Δ when improved = +1.00, median Δ when worsened = −0.40 (annotated as figure note).

2026-04-22 revision: colorblind-safe palette (blue/gray/orange instead of green/gray/red),
condition labels expanded inline to reduce dependence on caption, median Δ moved to a
compact bottom note rather than the figure title.
"""

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
    'font.size': 9.5,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})

CB = sns.color_palette('colorblind')
COLOR_IMPROVED = CB[0]   # blue
COLOR_TIE      = '#BDBDBD'
COLOR_WORSE    = CB[1]   # orange

# Counts from §4.2.1 of the v8 draft, 351-question low-baseline slice.
# (condition label, improved, tied, worsened)
COUNTS = [
    ('C2a\nspec only',         249, 49, 53),
    ('C4\nfacts only',         256, 44, 51),
    ('C8\nraw corpus',         275, 31, 45),
    ('C4a\nfacts + spec',      276, 22, 53),
]

N_TOTAL = 351  # 9 subjects x 39 questions


def main():
    conds = [row[0] for row in COUNTS]
    improved_pct = [100.0 * row[1] / N_TOTAL for row in COUNTS]
    tie_pct      = [100.0 * row[2] / N_TOTAL for row in COUNTS]
    worse_pct    = [100.0 * row[3] / N_TOTAL for row in COUNTS]

    fig, ax = plt.subplots(figsize=(10.5, 6.0))

    x = np.arange(len(conds))
    bar_width = 0.62

    # Hatch redundancy on tie + worsened (grayscale-safe)
    ax.bar(x, improved_pct, bar_width,
           label='Improved (Δ > 0)', color=COLOR_IMPROVED,
           edgecolor='black', linewidth=0.5)
    ax.bar(x, tie_pct, bar_width, bottom=improved_pct,
           label='Tied (Δ = 0)', color=COLOR_TIE, hatch='..',
           edgecolor='black', linewidth=0.5)
    bottom_worse = [i + t for i, t in zip(improved_pct, tie_pct)]
    ax.bar(x, worse_pct, bar_width, bottom=bottom_worse,
           label='Worsened (Δ < 0)', color=COLOR_WORSE, hatch='//',
           edgecolor='black', linewidth=0.5)

    # In-bar value labels
    for i, (imp, tie, wor) in enumerate(zip(improved_pct, tie_pct, worse_pct)):
        ax.text(i, imp / 2, f'{imp:.1f}%', ha='center', va='center',
                color='white', fontsize=11, fontweight='bold')
        ax.text(i, imp + tie / 2, f'{tie:.1f}%', ha='center', va='center',
                color='black', fontsize=9)
        ax.text(i, imp + tie + wor / 2, f'{wor:.1f}%', ha='center', va='center',
                color='white', fontsize=10, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(conds, fontsize=10)
    ax.set_ylabel('Share of 351 low-baseline questions (%)')
    ax.set_ylim(0, 115)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_title('Figure 4.2.1 — Per-question outcome vs. C5 baseline (low-baseline slice, n = 351)',
                 pad=38)

    ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)

    ax.legend(loc='upper center', fontsize=9, framealpha=0.92,
              edgecolor='#CCCCCC', ncol=3, bbox_to_anchor=(0.5, 1.08))

    # Compact figure note (moved out of title)
    note = ('n = 9 subjects × 39 questions · 5-judge primary per-question means · baseline = C5 (no-context)  '
            '|  median Δ when improved: +1.00    median Δ when worsened: −0.40')
    fig.text(0.5, 0.02, note, ha='center', fontsize=8, color='#444', fontstyle='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out_png = FIG_DIR / 'fig_4_2_1_question_improvement_rates.png'
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    print(f'Saved: {out_png}')
    out_pdf = FIG_DIR / 'fig_4_2_1_question_improvement_rates.pdf'
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_pdf}')


if __name__ == '__main__':
    main()
