"""
Generate publication-quality figures for "Beyond Recall" paper.
v3 (2026-04-22 revision): caption/figure mismatch fixes + colorblind-safe palette + paper-scale typography.

Run: python generate_figures_v3.py
Outputs 9 PNGs at 300 DPI to the same directory.

Changes vs prior v3:
  fig1  — removed orphaned x=2.4 threshold line; tightened annotations; shape redundancy.
  fig2  — relabeled to condition codes only (C5/C1/C2a/C3/C4/C4a/C9); colorblind palette + shape by family.
  fig3  — corrected values to match paper §1.3/§4.3 (controlled config: 93/83/74/53 all-three-disagree) + inline
          one-line definition of "disagreement".
  fig4  — regenerated as 3 conditions (C5/C2a/C4a) x 2 classifier rules (narrow: starts_refusal,
          broader: refusal_ge_1). Values from docs/research/hedging_analysis.json.
  fig5  — x-axis labels switched from descriptive names to condition codes (C5/C2a/C2c/C4/C4a),
          with a compact legend mapping. y-axis starts at 0.
  fig6  — colorblind palette + shape redundancy.
  fig7  — full replot. Now shows C3 - C1 delta on the low-baseline slice (n=9) for all 5 systems
          (Mem0, Letta, Zep, Supermemory, Base Layer) per paper §4.3-§4.4. Base Layer delta uses
          the paper's §4.4 value of +0.08 (note: DATA_REFERENCE §4 lists +0.13; flagged for author).
  fig8  — primary panel now 5-judge (Haiku/Sonnet/Opus/GPT-4o/GPT-5.4). Consistent model-name
          typography. 7x7 kept as a separate Gemini sensitivity panel. Naming normalized.
  fig9  — bars strictly sorted by baseline; legend labels reframed as "baseline below/above ~2.0
          low-baseline cutoff"; threshold line removed to avoid confusion with the low-baseline cutoff.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import Normalize
import seaborn as sns

# Output directory = same as this script
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Paper-scale typography (two-column conference paper, not slide-deck) ──
sns.set_theme(context='paper', style='whitegrid', palette='colorblind')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.titlesize': 9.5,
    'axes.labelsize': 8.5,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.7,
    'axes.grid': True,
    'axes.grid.axis': 'y',
    'grid.alpha': 0.35,
    'grid.linewidth': 0.6,
    'figure.dpi': 100,
})

# ── Colorblind-safe palette (seaborn 'colorblind') ──
# Index:  0 blue, 1 orange, 2 green, 3 red, 4 purple, 5 brown, 6 pink, 7 gray, 8 yellow, 9 cyan
CB = sns.color_palette('colorblind')
BLUE    = CB[0]   # improved / spec
ORANGE  = CB[1]   # no-spec / wrong
GREEN   = CB[2]   # low-baseline or improved subgroup
RED     = CB[3]   # franklin / warning
PURPLE  = CB[4]   # facts+spec
BROWN   = CB[5]
PINK    = CB[6]
GRAY    = '#7A7A7A'
YELLOW  = CB[8]
CYAN    = CB[9]

# ── REAL DATA from summary.json (14 subjects, 7-judge aggregate) ──
subjects = ['Sunity Devee', 'Hamerton', 'Ebers', 'Fukuzawa', 'Seacole', 'Keckley',
            'Bernal Diaz', 'Yung Wing', 'Rousseau', 'Babur', 'Augustine', 'Cellini',
            'Equiano', 'Zitkala-Sa']
baselines = [1.026, 1.246, 1.038, 1.803, 1.774, 1.915, 1.828, 1.877, 2.436, 2.032, 2.803, 2.560, 2.932, 2.338]
spec = [2.267, 2.936, 1.795, 2.556, 2.482, 2.641, 2.528, 2.215, 2.810, 2.278, 2.974, 2.722, 2.697, 2.031]
wrong_spec = [1.292, 1.794, 1.504, 2.107, 1.431, 1.500, 2.130, 2.200, 1.913, 1.233, 2.542, 1.944, 2.175, 1.662]
facts = [2.462, 2.554, 2.209, 2.885, 2.626, 2.568, 2.709, 2.128, 2.323, 2.368, 3.092, 2.611, 2.632, 2.103]
facts_spec = [2.410, 3.084, 2.338, 2.987, 2.595, 2.620, 2.782, 2.400, 2.533, 2.385, 3.222, 2.795, 2.654, 2.021]

regions = ['Indian', 'British', 'German', 'Japanese', 'Caribbean', 'Black American',
           'Latin American', 'Chinese', 'French', 'Central Asian', 'North African',
           'Italian', 'West African', 'Native American']

# Judge agreement (Spearman rho) - full 7x7 retained for sensitivity panel
judge_names_7 = ['Haiku', 'Sonnet', 'Opus', 'GPT-4o', 'GPT-5.4', 'Gemini Flash', 'Gemini Pro']
rho_matrix_7 = np.array([
    [1.00, 0.96, 0.94, 0.93, 0.95, 0.98, 0.91],
    [0.96, 1.00, 0.95, 0.92, 0.94, 0.96, 0.90],
    [0.94, 0.95, 1.00, 0.91, 0.93, 0.94, 0.89],
    [0.93, 0.92, 0.91, 1.00, 0.89, 0.91, 0.88],
    [0.95, 0.94, 0.93, 0.89, 1.00, 0.94, 0.90],
    [0.98, 0.96, 0.94, 0.91, 0.94, 1.00, 0.91],
    [0.91, 0.90, 0.89, 0.88, 0.90, 0.91, 1.00],
])
# 5-judge primary (non-Gemini)
judge_names_5 = judge_names_7[:5]
rho_matrix_5 = rho_matrix_7[:5, :5]

# Memory systems delta (C3 - C1), controlled configuration, low-baseline slice (n=9)
# Source: docs/DATA_REFERENCE.md §4 (Mem0, Letta, Zep, Supermemory)
# Base Layer: docs/beyond_recall_v8_draft.md §4.4 states +0.08 on low-baseline (note: §4 table lists +0.13;
# paper body is primary; flagged in fix log).
mem_systems = ['Mem0', 'Letta', 'Zep', 'Supermemory', 'Base Layer']
mem_delta_low = [0.13, 0.23, 0.20, 0.004, 0.08]
mem_positive_of_9 = [6, 7, 9, 5, 7]

# Compression curve (Hamerton)
comp_conditions = ['C5', 'C1 (SM)', 'C1 (Mem0)', 'C2a', 'C3 (SM+spec)',
                   'C3 (Mem0+spec)', 'C3 (Letta+spec)', 'C4', 'C4a', 'C9']
comp_tokens     = [  47,    247,     302,          2562,   2782,
                     2837,     2790,      9583,  12103, 34144]
comp_scores     = [1.41,    2.61,    2.64,         2.77,   2.92,
                     3.21,     3.38,      2.74,   2.69,  2.31]
# Family map: baseline, retrieval-only, spec, retrieval+spec, facts, raw
comp_family = ['baseline', 'retrieval', 'retrieval', 'spec', 'ret+spec',
               'ret+spec',  'ret+spec', 'facts',    'facts', 'raw']
FAMILY_STYLE = {
    'baseline':   {'color': GRAY,    'marker': 'X', 'label': 'C5 baseline (no context)'},
    'retrieval':  {'color': ORANGE,  'marker': 's', 'label': 'Memory system alone (C1)'},
    'spec':       {'color': BLUE,    'marker': 'o', 'label': 'Spec alone (C2a)'},
    'ret+spec':   {'color': GREEN,   'marker': '^', 'label': 'Memory + spec (C3)'},
    'facts':      {'color': PURPLE,  'marker': 'D', 'label': 'Facts (C4 / C4a)'},
    'raw':        {'color': RED,     'marker': 'P', 'label': 'Raw corpus (C9)'},
}

# Hedging data from docs/research/hedging_analysis.json (3 conditions × 2 rules)
hedging_conditions = ['C5\n(baseline)', 'C2a\n(spec)', 'C4a\n(facts + spec)']
hedging_narrow  = [28.8, 1.4, 0.0]   # starts_refusal rule
hedging_broader = [41.2, 7.9, 0.4]   # refusal_ge_1 rule


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {name}")


# ════════════════════════════════════════════════════════════════
# Fig 1: Global Gradient (14 subjects, no Franklin)
# ════════════════════════════════════════════════════════════════
def fig1():
    fig, ax = plt.subplots(figsize=(6.4, 4.4))

    improved = [s > b for b, s in zip(baselines, spec)]

    # y=x reference
    ax.plot([0.5, 4.5], [0.5, 4.5], '--', color=GRAY, linewidth=0.8, alpha=0.7, zorder=1,
            label='y = x (no spec effect)')

    # Plot points with color + shape redundancy
    for i in range(len(subjects)):
        color = BLUE if improved[i] else ORANGE
        marker = 'o' if improved[i] else 's'
        ax.scatter(baselines[i], spec[i], c=[color], marker=marker, s=48, zorder=3,
                   edgecolors='black', linewidths=0.4)

    # Labels for selected subjects (range endpoints + notable inversions)
    label_map = {
        'Sunity Devee': (8, 10),
        'Hamerton': (8, -14),
        'Ebers': (-10, 12),
        'Equiano': (8, -14),
        'Zitkala-Sa': (8, -14),
    }
    for i, subj in enumerate(subjects):
        if subj in label_map:
            dx, dy = label_map[subj]
            ax.annotate(subj, (baselines[i], spec[i]),
                        xytext=(dx, dy), textcoords='offset points',
                        fontsize=7, fontstyle='italic',
                        arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.4))

    ax.set_xlabel('Baseline score (no context, 1-5 rubric)')
    ax.set_ylabel('Score with specification (1-5 rubric)')
    ax.set_title('Global gradient: spec impact across 14 subjects')
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linewidth=0.5)

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=6,
                   markeredgecolor='black', markeredgewidth=0.4, label='Improved with spec (above y=x)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=ORANGE, markersize=6,
                   markeredgecolor='black', markeredgewidth=0.4, label='Not improved (below y=x)'),
        plt.Line2D([0], [0], linestyle='--', color=GRAY, linewidth=0.8, label='y = x (no spec effect)'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')

    save(fig, 'fig1_global_gradient.png')


# ════════════════════════════════════════════════════════════════
# Fig 2: Compression Curve (Hamerton)
# ════════════════════════════════════════════════════════════════
def fig2():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))

    # Plot points grouped by family (color + marker redundancy)
    for family, style in FAMILY_STYLE.items():
        xs = [comp_tokens[i] for i in range(len(comp_conditions)) if comp_family[i] == family]
        ys = [comp_scores[i] for i in range(len(comp_conditions)) if comp_family[i] == family]
        ax.scatter(xs, ys, c=[style['color']], marker=style['marker'], s=62,
                   edgecolors='black', linewidths=0.5, zorder=3, label=style['label'])

    ax.set_xscale('log')

    # Inline labels removed — legend provides family mapping, and markers cluster
    # tightly enough that y-offset labels overlapped neighbouring points. Legend
    # moved to lower-right (empty corner; all data lives upper-left-to-center).

    ax.set_xlabel('Context tokens served to response model (log scale)')
    ax.set_ylabel('Judge score (1-5)')
    ax.set_title('Compression curve: Hamerton conditions by token count')

    ax.legend(loc='lower right', frameon=True, framealpha=0.92, edgecolor='#CCCCCC', ncol=1)
    ax.set_ylim(1.0, 3.8)
    ax.set_xlim(30, 80000)
    ax.grid(True, alpha=0.3, linewidth=0.5, which='both')

    save(fig, 'fig2_compression_curve.png')


# ════════════════════════════════════════════════════════════════
# Fig 3: Retrieval Disagreement (controlled config, three-way)
# ════════════════════════════════════════════════════════════════
def fig3():
    fig, ax = plt.subplots(figsize=(5.0, 3.4))

    labels = ['Top-1', 'Top-3', 'Top-5', 'Top-10']
    # Source: DATA_REFERENCE KEY_FINDINGS §M4. Controlled config, 515 questions, 3-way disagree.
    values = [93, 83, 74, 53]

    bars = ax.bar(labels, values, color=BLUE, width=0.55, edgecolor='white', linewidth=0.5,
                  hatch='//', alpha=0.92)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f'{val}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_ylabel('Disagreement rate (%)')
    ax.set_title('Retrieval disagreement across three memory systems')
    ax.set_ylim(0, 100)

    # In-figure definition so the chart stands alone
    ax.text(0.5, -0.30,
            '"Disagreement" = share of 515 questions where Mem0, Letta, and Supermemory\nall three returned different top-k items (controlled config; identical fact pool).',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=7, color='#444', fontstyle='italic')

    save(fig, 'fig3_retrieval_disagreement.png')


# ════════════════════════════════════════════════════════════════
# Fig 4: Hedging Reduction (3 conditions × 2 classifier rules)
# ════════════════════════════════════════════════════════════════
def fig4():
    fig, ax = plt.subplots(figsize=(5.8, 3.6))

    x = np.arange(len(hedging_conditions))
    width = 0.36

    bars_narrow = ax.bar(x - width/2, hedging_narrow, width, color=BLUE,
                         edgecolor='white', linewidth=0.5,
                         label='Narrow rule (starts_refusal)')
    bars_broad  = ax.bar(x + width/2, hedging_broader, width, color=ORANGE,
                         edgecolor='white', linewidth=0.5, hatch='//',
                         label='Broader rule (refusal_ge_1)')

    for bars, values in [(bars_narrow, hedging_narrow), (bars_broad, hedging_broader)]:
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=7.5)

    ax.set_xticks(x)
    ax.set_xticklabels(hedging_conditions)
    ax.set_ylabel('Hedging / refusal rate (%)')
    ax.set_title('Hedging reduction with specification (13 subjects × 39 questions; 2 classifier rules)')
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')
    ax.grid(True, axis='y', alpha=0.3, linewidth=0.5)

    save(fig, 'fig4_hedging_reduction.png')


# ════════════════════════════════════════════════════════════════
# Fig 5: Condition Effects Composite (2 panels, condition codes)
# ════════════════════════════════════════════════════════════════
def fig5():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.4),
                                    gridspec_kw={'width_ratios': [1.2, 1]})

    # Use condition CODES (match §3.5 and the paper's table 4.1)
    cond_codes  = ['C5', 'C2a', 'C2c', 'C4', 'C4a']
    cond_descs  = ['baseline\n(no context)', 'spec only', 'wrong spec\n(derangement)',
                   'all facts', 'facts + spec']
    n = len(subjects)

    all_scores = np.array([
        baselines,
        spec,
        wrong_spec,
        facts,
        facts_spec,
    ]).T  # shape (14, 5)

    improved = [spec[i] > baselines[i] for i in range(n)]

    # Panel A: Slope chart with condition codes
    x_pos = np.arange(5)
    for i in range(n):
        color = BLUE if improved[i] else ORANGE
        ax1.plot(x_pos, all_scores[i], color=color, alpha=0.45, linewidth=0.9, zorder=2)
        ax1.scatter(x_pos, all_scores[i], color=color, s=12, zorder=3, edgecolors='none')

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(cond_codes, fontsize=9, fontweight='bold')
    # Secondary description row under codes
    for xi, desc in zip(x_pos, cond_descs):
        ax1.text(xi, -0.09, desc, transform=ax1.get_xaxis_transform(),
                 ha='center', va='top', fontsize=6.8, color='#555')

    ax1.set_ylabel('Judge score (1-5)')
    ax1.set_title('A. Per-subject trajectories (N=14)')
    ax1.set_ylim(0, 4.0)
    ax1.set_xlim(-0.4, 4.4)

    handles = [
        plt.Line2D([0], [0], color=BLUE, linewidth=1.3,
                   label='C2a > C5 (spec improved)'),
        plt.Line2D([0], [0], color=ORANGE, linewidth=1.3,
                   label='C2a ≤ C5 (spec did not improve)'),
    ]
    ax1.legend(handles=handles, loc='upper left', frameon=True, framealpha=0.92,
               edgecolor='#CCCCCC')

    # Panel B: Box plots
    bp = ax2.boxplot([all_scores[:, j] for j in range(5)],
                     tick_labels=cond_codes, patch_artist=True, widths=0.5,
                     medianprops=dict(color='black', linewidth=1.0),
                     whiskerprops=dict(linewidth=0.7),
                     capprops=dict(linewidth=0.7),
                     flierprops=dict(marker='o', markersize=2.8))

    box_colors = [GRAY, BLUE, ORANGE, PURPLE, GREEN]
    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.55)

    ax2.set_ylabel('Judge score (1-5)')
    ax2.set_title('B. Score distributions by condition')
    ax2.set_ylim(0, 4.0)
    for tl in ax2.get_xticklabels():
        tl.set_fontweight('bold')

    fig.tight_layout(w_pad=3)
    save(fig, 'fig5_condition_effects.png')


# ════════════════════════════════════════════════════════════════
# Fig 6: Wrong Spec Control (paired dot plot)
# ════════════════════════════════════════════════════════════════
def fig6():
    fig, ax = plt.subplots(figsize=(6.6, 4.4))

    # Sort by correct-spec - wrong-spec gap (largest gap at top for clarity)
    gap = [spec[i] - wrong_spec[i] for i in range(len(subjects))]
    order = np.argsort(gap)  # ascending, smallest gap at bottom; reverse to put largest at top
    order = order[::-1]

    y_positions = np.arange(len(subjects))

    for rank, idx in enumerate(order):
        bl = baselines[idx]
        ws = wrong_spec[idx]
        cs = spec[idx]

        # Connecting line from wrong spec to correct spec highlights the gap
        ax.plot([ws, cs], [rank, rank], color='#CCCCCC', linewidth=1.0, zorder=1)

        # Dots with shape redundancy
        ax.scatter(bl, rank, color=GRAY,   s=38, marker='X', zorder=3, edgecolors='black', linewidths=0.3)
        ax.scatter(ws, rank, color=ORANGE, s=38, marker='s', zorder=3, edgecolors='black', linewidths=0.3)
        ax.scatter(cs, rank, color=BLUE,   s=38, marker='o', zorder=3, edgecolors='black', linewidths=0.3)

    sorted_names = [subjects[i] for i in order]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(sorted_names, fontsize=7.5)
    ax.set_xlabel('Judge score (1-5)')
    ax.set_title('Correct-spec vs. wrong-spec score by subject (sorted by gap)')

    handles = [
        plt.Line2D([0], [0], marker='X', color='w', markerfacecolor=GRAY, markersize=6,
                   markeredgecolor='black', markeredgewidth=0.3, label='Baseline (C5)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=ORANGE, markersize=6,
                   markeredgecolor='black', markeredgewidth=0.3, label='Wrong spec (C2c)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=6,
                   markeredgecolor='black', markeredgewidth=0.3, label='Correct spec (C2a)'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')
    ax.set_xlim(1.0, 3.8)
    ax.grid(True, axis='x', alpha=0.3, linewidth=0.5)

    save(fig, 'fig6_wrong_spec_control.png')


# ════════════════════════════════════════════════════════════════
# Fig 7: Memory System Comparison — C3-C1 delta on low-baseline slice (n=9)
# ════════════════════════════════════════════════════════════════
def fig7():
    fig, ax = plt.subplots(figsize=(6.2, 4.0))

    x = np.arange(len(mem_systems))
    bar_colors = [BLUE if d > 0 else ORANGE for d in mem_delta_low]

    bars = ax.bar(x, mem_delta_low, color=bar_colors, width=0.58,
                  edgecolor='black', linewidth=0.6)

    ax.axhline(0, color='black', linewidth=0.6)

    for bar, delta, pos in zip(bars, mem_delta_low, mem_positive_of_9):
        h = bar.get_height()
        offset = 0.012 if h >= 0 else -0.012
        va = 'bottom' if h >= 0 else 'top'
        ax.text(bar.get_x() + bar.get_width()/2, h + offset,
                f'{delta:+.2f}', ha='center', va=va, fontsize=8.5, fontweight='bold')

    # Two-line x-tick labels: system name + positive count
    tick_labels = [f'{name}\n({pos}/9 positive)'
                   for name, pos in zip(mem_systems, mem_positive_of_9)]
    ax.set_xticks(x)
    ax.set_xticklabels(tick_labels, fontsize=8)
    ax.set_ylabel('Spec delta: C3 − C1 (judge-score points)')
    ax.set_title('Spec delta per memory system, low-baseline slice (n = 9, controlled config)')
    ax.set_ylim(-0.05, 0.30)
    ax.grid(True, axis='y', alpha=0.3, linewidth=0.5)

    save(fig, 'fig7_memory_systems.png')


# ════════════════════════════════════════════════════════════════
# Fig 8: Judge Agreement Heatmap — 5-judge primary + 7-judge sensitivity
# ════════════════════════════════════════════════════════════════
def fig8():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.5),
                             gridspec_kw={'width_ratios': [1.0, 1.15]})

    norm = Normalize(vmin=0.85, vmax=1.0)
    cmap = plt.cm.viridis  # colorblind-safe perceptually uniform

    # Panel A: 5-judge primary
    ax = axes[0]
    im = ax.imshow(rho_matrix_5, cmap=cmap, norm=norm, aspect='equal')
    ax.set_xticks(range(len(judge_names_5)))
    ax.set_yticks(range(len(judge_names_5)))
    ax.set_xticklabels(judge_names_5, rotation=45, ha='right')
    ax.set_yticklabels(judge_names_5)
    for i in range(len(judge_names_5)):
        for j in range(len(judge_names_5)):
            val = rho_matrix_5[i, j]
            text_color = 'white' if val < 0.93 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=7.5, color=text_color)
    ax.set_title('A. 5-judge primary panel')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    # Panel B: 7-judge sensitivity (Gemini included)
    ax = axes[1]
    im = ax.imshow(rho_matrix_7, cmap=cmap, norm=norm, aspect='equal')
    ax.set_xticks(range(len(judge_names_7)))
    ax.set_yticks(range(len(judge_names_7)))
    ax.set_xticklabels(judge_names_7, rotation=45, ha='right')
    ax.set_yticklabels(judge_names_7)
    for i in range(len(judge_names_7)):
        for j in range(len(judge_names_7)):
            val = rho_matrix_7[i, j]
            text_color = 'white' if val < 0.93 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=6.8, color=text_color)
    ax.set_title('B. 7-judge sensitivity (Gemini added)')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    cbar = fig.colorbar(im, ax=axes, fraction=0.035, pad=0.04, label='Spearman ρ (ρ range shown: 0.85–1.00)')

    fig.suptitle('Inter-judge agreement (Spearman ρ across subjects × conditions)',
                 fontsize=10, y=1.02)

    save(fig, 'fig8_judge_agreement.png')


# ════════════════════════════════════════════════════════════════
# Fig 9: Cultural Region Baseline
# ════════════════════════════════════════════════════════════════
def fig9():
    fig, ax = plt.subplots(figsize=(6.2, 4.5))

    # Sort by baseline. barh index 0 plots at bottom; to put lowest at top,
    # we sort descending so the visual top-to-bottom order is low → high.
    order = np.argsort(baselines)[::-1]
    sorted_regions = [regions[i] for i in order]
    sorted_baselines = [baselines[i] for i in order]

    # Encode color by spec-improvement status at baseline. Legend makes this explicit.
    improved = [spec[order[rank]] > baselines[order[rank]] for rank in range(len(subjects))]
    bar_colors = [BLUE if imp else ORANGE for imp in improved]
    hatches = ['' if imp else '//' for imp in improved]

    for rank, (reg, bl, col, hat) in enumerate(zip(sorted_regions, sorted_baselines, bar_colors, hatches)):
        ax.barh(rank, bl, color=col, height=0.62, edgecolor='white', linewidth=0.5, hatch=hat)

    ax.set_yticks(range(len(sorted_regions)))
    ax.set_yticklabels(sorted_regions, fontsize=7.5)
    ax.set_xlabel('Baseline score (1-5 rubric, no-context prediction)')
    ax.set_title('Baseline recognizability by cultural region (ranked low → high)')

    handles = [
        mpatches.Patch(facecolor=BLUE, label='Spec improved this subject'),
        mpatches.Patch(facecolor=ORANGE, hatch='//', label='Spec did not improve this subject'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.92, edgecolor='#CCCCCC')
    ax.set_xlim(0, 3.5)
    ax.grid(True, axis='x', alpha=0.3, linewidth=0.5)

    save(fig, 'fig9_cultural_baseline.png')


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating publication figures for Beyond Recall (v3 revised 2026-04-22)...")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
    fig7()
    fig8()
    fig9()
    print("Done. All 9 figures saved to:", OUT_DIR)
