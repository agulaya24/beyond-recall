"""
Figure 4.2 v2: Hamerton compression — one plot, five conditions.

S114 author annotation (docs/reviews/s114_word_annotations.md §4.2):
- "This graph is a bit messy, I think what im seeing is specification provide major lift,
   facts + spec additional lift — the lift from these two are comparable to giving the raw
   corpus + spec. Would likely want to see where all facts lands, and where just raw corpus
   lands. May need to rework this figure."

Changes from v1:
1. Hamerton only (single subject), not 9-subject spaghetti. Task row:
   "raw corpus alone (C8), facts alone (C4), spec alone (C2a), facts + spec (C4a),
    corpus + spec (C9) on one plot."
2. Per-condition points with direct labels next to each point. Log-token x-axis.
3. Score y-axis. Baseline C5 (no context) shown as a horizontal reference line.
4. Markers color + shape by context type; annotations show token count and condition code.

Data: docs/DATA_REFERENCE.md §8 (Table 4.2 Hamerton compression).
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
    'legend.fontsize': 8.5,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
})
CB = sns.color_palette('colorblind')

# From docs/DATA_REFERENCE.md §8: Hamerton compression table.
# (condition, token count, 5-judge primary score, marker, color, family label)
POINTS = [
    # code,  tokens,  score,  marker, color,  label
    ('C5 (baseline)',     40,    1.25, 'X', '#7A7A7A', 'No context'),
    ('C2a (spec alone)',  7320,  3.04, 'o', CB[0],    'Spec alone'),
    ('C4 (facts alone)',  7723,  2.53, 'D', CB[4],    'Facts alone'),
    ('C4a (facts+spec)',  16874, 3.22, '^', CB[2],    'Facts + spec'),
    ('C8 (raw corpus)',   34168, 2.32, 's', CB[1],    'Raw corpus'),
    ('C9 (corpus+spec)',  41452, 3.22, 'P', CB[3],    'Corpus + spec'),
]


def main():
    fig, ax = plt.subplots(figsize=(9.2, 5.4))

    # Baseline reference line (C5 = 1.25 on Hamerton)
    ax.axhline(1.25, color='#BBBBBB', linestyle=':', linewidth=1.0, zorder=1,
               label='C5 baseline (1.25, no context)')

    # Plot each condition
    for label, toks, score, marker, color, family in POINTS:
        ax.scatter(toks, score, marker=marker, s=200, color=color,
                   edgecolors='black', linewidths=0.8, zorder=5,
                   label=f'{label}  —  {score:.2f}')

    # Per-point annotations: use leader lines + offsets to avoid overlap in the
    # dense 7K-17K region.
    offset_map = {
        # (dx, dy) in points; arrow=True means draw leader line to marker
        'C5 (baseline)':    (  50,  10, True),
        'C2a (spec alone)': ( -90,  40, True),
        'C4 (facts alone)': ( -90, -40, True),
        'C4a (facts+spec)': (   0,  36, False),
        'C8 (raw corpus)':  (   0, -32, False),
        'C9 (corpus+spec)': (  55,  25, True),
    }
    for label, toks, score, marker, color, family in POINTS:
        dx, dy, arrow = offset_map[label]
        tok_str = f'~{toks/1000:.1f}K tok' if toks >= 1000 else f'~{toks} tok'
        ann = f'{label}\n{tok_str}   score {score:.2f}'
        ax.annotate(
            ann, (toks, score), xytext=(dx, dy), textcoords='offset points',
            ha='center', fontsize=8, color='#222',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='white',
                      edgecolor='#BBBBBB', linewidth=0.6, alpha=0.96),
            arrowprops=dict(arrowstyle='-', color='#999', linewidth=0.7) if arrow else None,
        )

    # Guide arrow: spec beats corpus despite ~5x less context
    ax.annotate('',
                xy=(7320, 3.04), xycoords='data',
                xytext=(34168, 2.32), textcoords='data',
                arrowprops=dict(arrowstyle='->', color='#888888', linewidth=1.0,
                                linestyle='--', connectionstyle='arc3,rad=-0.25'),
                zorder=2)
    ax.text(80, 2.90, 'spec alone (7K tok) outscores\nraw corpus (34K tok) on Hamerton',
            fontsize=8.2, color='#555', fontstyle='italic', ha='left',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFEF5',
                      edgecolor='#DDDDDD', linewidth=0.5, alpha=0.92))

    ax.set_xscale('log')
    ax.set_xlabel('Context size served to the response model (tokens, log scale)')
    ax.set_ylabel('5-judge primary score (1-5 rubric)')
    ax.set_title('Figure 4.2 — Hamerton: score vs. context size for 5 context strategies + baseline')
    ax.grid(True, alpha=0.3, linewidth=0.5, which='both')
    ax.set_ylim(0.6, 4.0)
    ax.set_xlim(20, 200000)

    ax.legend(loc='lower right', fontsize=7.8, framealpha=0.94,
              edgecolor='#CCCCCC', ncol=1, title='Condition  —  score')

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_compression_v2.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
