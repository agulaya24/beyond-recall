"""
Figure 7 v3: Per-memory-system spec delta by subject — publication polish.

Changes from v2:
1. Shared typography (14/12/10) + palette via _figure_style.py.
2. COLOR COLLISION FIX: positive bars use each system's distinct color from the shared
   palette; negative bars use the clean RED (COLOR_WORSENED, #C44E52) in every panel.
   Supermemory is now PURPLE (not orange-red), so positive vs. negative reads clearly
   where v2 had ambiguous red-orange tones.
3. MEAN bar distinction: darker system-color fill (no hatch), 2 pt black outline.
   In v2 the MEAN was same-color with dotted hatch, which read as "just another bar".
4. In-chart per-panel n= printed in subtitle; mean also shown in subtitle.
5. dpi=300.

Data source: docs/research/memory_systems_5judge_primary.md (controlled config, 5-judge
primary).
"""

from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _figure_style import (
    apply_style, darker,
    SYSTEM_COLOR, COLOR_WORSENED,
    SIZE_ANNOTATION_SMALL, SIZE_FOOTER,
)

REPO = Path(__file__).resolve().parent.parent
FIG_DIR = REPO / 'figures'

apply_style()

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


def main():
    fig, axes = plt.subplots(1, 4, figsize=(17.5, 5.8), sharey=True)
    fig.suptitle('Figure 7: Per-subject spec delta (C3 - C1) by memory system  '
                 '(low-baseline slice, controlled config, 5-judge primary)',
                 fontsize=14, fontweight='bold', y=1.01)

    n = len(SUBJECTS) + 1
    x = np.arange(n)
    x_labels = [SUBJECT_LABELS[s] for s in SUBJECTS] + ['MEAN']

    y_min, y_max = -0.35, 0.55

    for ax, system in zip(axes, SYSTEMS):
        sys_data = DATA[system]
        vals = [sys_data[s] for s in SUBJECTS]
        mean_v = float(np.mean(vals))
        all_vals = vals + [mean_v]
        pos_color = SYSTEM_COLOR[system]

        bar_colors = [pos_color if v >= 0 else COLOR_WORSENED for v in vals]
        bars = ax.bar(x[:-1], vals, width=0.75, color=bar_colors, alpha=0.85,
                      edgecolor='black', linewidth=0.5)

        # MEAN bar: darker system color fill, solid (no hatch), 2 pt black outline
        mean_fill = darker(pos_color, 0.25) if mean_v >= 0 else darker(COLOR_WORSENED, 0.15)
        ax.bar(x[-1], mean_v, width=0.85, color=mean_fill, alpha=1.0,
               edgecolor='black', linewidth=2.0, zorder=5)

        # Bar value labels at bar tip (GN style)
        for xi, v in zip(x, all_vals):
            offset = 0.012 if v >= 0 else -0.012
            va = 'bottom' if v >= 0 else 'top'
            ax.text(xi, v + offset, f'{v:+.2f}', ha='center', va=va,
                    fontsize=8, fontweight='bold', color='#222')

        # Zero reference line
        ax.axhline(0, color='black', linewidth=0.9, zorder=2)
        # MEAN divider
        ax.axvline((len(SUBJECTS) - 1) + 0.5, color='#888', linewidth=0.8,
                   linestyle=':', alpha=0.7, zorder=1)

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8.5)
        ax.get_xticklabels()[-1].set_fontweight('bold')

        # In-panel title: name + mean + n (GN style "n=" in chart body, not only caption)
        ax.set_title(f'{system}\nmean = {mean_v:+.3f}  (n = {len(SUBJECTS)} subjects)',
                     fontsize=11)
        ax.set_ylim(y_min, y_max)
        ax.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)

    axes[0].set_ylabel('Delta_spec = C3 - C1  (points on 1-5 rubric)')

    footer = ('Low-baseline slice (n = 9 subjects, C5 <= 2.0). '
              'Controlled configuration: identical fact pool loaded into each memory system. '
              'Delta_spec = mean(C3) - mean(C1) per subject, 5-judge primary. '
              'Source: docs/research/memory_systems_5judge_primary.md. '
              'Positive bars in each system color; negative bars in red; MEAN bar outlined.')
    fig.text(0.5, -0.04, footer, ha='center', fontsize=SIZE_FOOTER, color='#444',
             fontstyle='italic')

    plt.tight_layout(rect=[0, 0.02, 1, 1])

    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig7_memory_systems_v3.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')


if __name__ == '__main__':
    main()
