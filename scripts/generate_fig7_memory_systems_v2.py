"""
Figure 7 v2: Per-memory-system spec delta, broken out by subject.

S114 task specification:
- GROUPED BAR CHART: for each of the 4 memory systems (Mem0, Letta archival,
  Supermemory, Zep), show 9 bars (one per low-baseline subject) + a mean bar across
  the 9.
- Y-axis must extend to both negative and positive (currently Supermemory collapses to 0.00
  — we need to see the spread).

Data source: docs/research/memory_systems_5judge_primary.md (Per-subject detail, controlled
configuration). Controlled configuration is used per the paper body (§4.4, §4.3) — it is the
configuration that holds the fact pool constant across systems.

Base Layer is intentionally excluded here: Fig 7 in the paper is the memory-system
comparison, and Base Layer appears in §4.4.1 and earlier figures separately.
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
    'font.size': 9,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'legend.fontsize': 8.5,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
})

# Per-subject Δ_spec (C3 − C1), controlled configuration, 5-judge primary.
# Source: docs/research/memory_systems_5judge_primary.md, "Per-subject detail, Controlled" table.
SUBJECTS = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
            'bernal_diaz', 'keckley', 'yung_wing', 'babur']
SUBJECT_LABELS = {
    'hamerton':     'Hamerton',
    'sunity_devee': 'Sunity Devee',
    'ebers':        'Ebers',
    'fukuzawa':     'Fukuzawa',
    'seacole':      'Seacole',
    'bernal_diaz':  'Bernal Diaz',
    'keckley':      'Keckley',
    'yung_wing':    'Yung Wing',
    'babur':        'Babur',
}

# system -> {subject -> delta}  (controlled configuration, 5-judge primary)
DATA = {
    'Mem0': {
        'hamerton': +0.103, 'sunity_devee': -0.082, 'ebers': +0.149,
        'fukuzawa': +0.046, 'seacole': +0.154, 'bernal_diaz': -0.026,
        'keckley': -0.021, 'yung_wing': +0.328, 'babur': +0.256,
    },
    'Letta (archival)': {
        'hamerton': +0.387, 'sunity_devee': +0.026, 'ebers': +0.138,
        'fukuzawa': +0.044, 'seacole': +0.400, 'bernal_diaz': +0.036,
        'keckley': -0.021, 'yung_wing': +0.308, 'babur': +0.164,
    },
    'Supermemory': {
        'hamerton': +0.144, 'sunity_devee': -0.113, 'ebers': +0.138,
        'fukuzawa': -0.205, 'seacole': +0.082, 'bernal_diaz': -0.031,
        'keckley': -0.267, 'yung_wing': +0.108, 'babur': +0.051,
    },
    'Zep': {
        'hamerton': +0.333, 'sunity_devee': +0.087, 'ebers': +0.272,
        'fukuzawa': +0.026, 'seacole': +0.472, 'bernal_diaz': +0.097,
        'keckley': +0.041, 'yung_wing': +0.123, 'babur': +0.041,
    },
}

SYSTEMS = ['Mem0', 'Letta (archival)', 'Supermemory', 'Zep']

CB = sns.color_palette('colorblind')
SYSTEM_COLORS = {
    'Mem0':             CB[0],
    'Letta (archival)': CB[2],
    'Supermemory':      CB[1],
    'Zep':              CB[4],
}


def main():
    fig, axes = plt.subplots(1, 4, figsize=(16, 5.2), sharey=True)
    fig.suptitle('Figure 7 — Per-subject spec delta (C3 − C1) by memory system  (low-baseline slice, controlled config, 5-judge primary)',
                 fontsize=11.5, y=1.02)

    n = len(SUBJECTS) + 1  # 9 subjects + mean
    x = np.arange(n)
    x_labels = [SUBJECT_LABELS[s] for s in SUBJECTS] + ['MEAN']

    y_min, y_max = -0.35, 0.55

    for ax, system in zip(axes, SYSTEMS):
        sys_data = DATA[system]
        vals = [sys_data[s] for s in SUBJECTS]
        mean_v = float(np.mean(vals))
        all_vals = vals + [mean_v]
        color = SYSTEM_COLORS[system]

        # Two color shades: subject bars lighter, MEAN bar same color darker
        bar_colors = [color if v >= 0 else '#E06666' for v in vals]
        mean_color = color
        mean_edge = 'black'

        bars = ax.bar(x[:-1], vals, width=0.75, color=bar_colors, alpha=0.75,
                      edgecolor='black', linewidth=0.5)
        # Tag negative bars with a distinct orange-red fill so direction is visible at a glance
        for bar, v in zip(bars, vals):
            if v < 0:
                bar.set_facecolor('#E07A5F')
                bar.set_alpha(0.9)

        # MEAN bar — bold, outlined, system color. Tint red if negative.
        mean_fill = mean_color if mean_v >= 0 else '#E07A5F'
        ax.bar(x[-1], mean_v, width=0.85, color=mean_fill, alpha=0.98,
               edgecolor='black', linewidth=1.4, hatch='..', zorder=5)

        # Value labels
        for xi, v in zip(x, all_vals):
            offset = 0.012 if v >= 0 else -0.012
            va = 'bottom' if v >= 0 else 'top'
            ax.text(xi, v + offset, f'{v:+.2f}', ha='center', va=va,
                    fontsize=7.4, fontweight='bold', color='#222')

        # Zero reference line
        ax.axhline(0, color='black', linewidth=0.8, zorder=2)

        # MEAN divider line
        ax.axvline((len(SUBJECTS) - 1) + 0.5, color='#888', linewidth=0.7,
                   linestyle=':', alpha=0.7, zorder=1)

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=7.8)
        # Bold the MEAN tick
        ax.get_xticklabels()[-1].set_fontweight('bold')

        ax.set_title(f'{system}    mean = {mean_v:+.3f}', fontsize=10)
        ax.set_ylim(y_min, y_max)
        ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)

    axes[0].set_ylabel('Δ_spec = C3 − C1  (points on 1-5 rubric)', fontsize=10)

    # Footer
    footer = ('Low-baseline slice (n = 9 subjects, C5 ≤ 2.0). '
              'Controlled configuration: identical fact pool loaded into each memory system. '
              'Δ_spec = mean(C3) − mean(C1) per subject, 5-judge primary. '
              'Source: docs/research/memory_systems_5judge_primary.md.')
    fig.text(0.5, -0.02, footer, ha='center', fontsize=7.8, color='#444', fontstyle='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig7_memory_systems_v2.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
