"""
Generate all 9 publication-quality figures for "Beyond Recall" paper.
v3: Uses REAL data from summary.json (harmonized rerun).
Run: python generate_figures_v3.py
Outputs 9 PNGs at 300 DPI to the same directory.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import Normalize

# Output directory = same as this script
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Global style ──
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.grid': True, 'axes.grid.axis': 'both',
    'grid.alpha': 0.5,
    'grid.linewidth': 0.8,
})

# ── Color palette ──
BLUE = '#1F77B4'
RED_ORANGE = '#D55E00'
GREEN = '#2CA02C'
PURPLE = '#9467BD'
GRAY = '#7A7A7A'
GOLD = '#E6AB02'

# ── REAL DATA from summary.json ──
subjects = ['Sunity Devee', 'Hamerton', 'Ebers', 'Fukuzawa', 'Seacole', 'Keckley',
            'Bernal Diaz', 'Yung Wing', 'Rousseau', 'Babur', 'Augustine', 'Cellini',
            'Equiano', 'Zitkala-Sa']
baselines = [1.026, 1.246, 1.038, 1.803, 1.774, 1.915, 1.828, 1.877, 2.436, 2.032, 2.803, 2.560, 2.932, 2.338]
spec = [2.267, 2.936, 1.795, 2.556, 2.482, 2.641, 2.528, 2.215, 2.810, 2.278, 2.974, 2.722, 2.697, 2.031]
wrong_spec = [1.292, 1.794, 1.504, 2.107, 1.431, 1.500, 2.130, 2.200, 1.913, 1.233, 2.542, 1.944, 2.175, 1.662]
facts = [2.462, 2.554, 2.209, 2.885, 2.626, 2.568, 2.709, 2.128, 2.323, 2.368, 3.092, 2.611, 2.632, 2.103]
facts_spec = [2.410, 3.084, 2.338, 2.987, 2.595, 2.620, 2.782, 2.400, 2.533, 2.385, 3.222, 2.795, 2.654, 2.021]
effects = [121.0, 135.5, 72.8, 41.7, 39.9, 37.9, 38.3, 18.0, 15.4, 12.1, 6.1, 6.3, -8.0, -13.2]

regions = ['Indian', 'British', 'German', 'Japanese', 'Caribbean', 'Black American',
           'Latin American', 'Chinese', 'French', 'Central Asian', 'North African',
           'Italian', 'West African', 'Native American']

# Judge agreement (Spearman rho)
judge_names = ['Haiku', 'Sonnet', 'Opus', 'GPT-4o', 'GPT-5.4', 'Gem Flash', 'Gem Pro']
rho_matrix = np.array([
    [1.00, 0.96, 0.94, 0.93, 0.95, 0.98, 0.91],
    [0.96, 1.00, 0.95, 0.92, 0.94, 0.96, 0.90],
    [0.94, 0.95, 1.00, 0.91, 0.93, 0.94, 0.89],
    [0.93, 0.92, 0.91, 1.00, 0.89, 0.91, 0.88],
    [0.95, 0.94, 0.93, 0.89, 1.00, 0.94, 0.90],
    [0.98, 0.96, 0.94, 0.91, 0.94, 1.00, 0.91],
    [0.91, 0.90, 0.89, 0.88, 0.90, 0.91, 1.00],
])

# Memory systems (Hamerton brief-only - original study)
mem_systems = ['Letta', 'Mem0', 'Supermemory', 'Zep']
mem_without = [2.33, 2.64, 2.61, 1.62]
mem_with = [3.38, 3.21, 2.92, 2.69]

# Compression curve (Hamerton - original merged results)
comp_conditions = ['C5 Baseline', 'C1 SM', 'C1 Mem0', 'C2a Spec', 'C3 SM+Spec',
                   'C3 Mem0+Spec', 'C3 Letta+Spec', 'C4 All Facts', 'C4a Facts+Spec', 'C9 Raw']
comp_tokens = [47, 247, 302, 2562, 2782, 2837, 2790, 9583, 12103, 34144]
comp_scores = [1.41, 2.61, 2.64, 2.77, 2.92, 3.21, 3.38, 2.74, 2.69, 2.31]
comp_colors_map = {
    'C5 Baseline': GRAY, 'C1 SM': GOLD, 'C1 Mem0': GOLD,
    'C2a Spec': BLUE, 'C3 SM+Spec': GREEN, 'C3 Mem0+Spec': GREEN,
    'C3 Letta+Spec': GREEN, 'C4 All Facts': PURPLE,
    'C4a Facts+Spec': PURPLE, 'C9 Raw': RED_ORANGE
}


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {name}")


# ════════════════════════════════════════════════════════════════
# Fig 1: Global Gradient (14 subjects, no Franklin)
# ════════════════════════════════════════════════════════════════
def fig1():
    fig, ax = plt.subplots(figsize=(6.8, 4.8))

    improved = [s > b for b, s in zip(baselines, spec)]

    # y=x reference
    ax.plot([0.5, 4.5], [0.5, 4.5], '--', color=GRAY, linewidth=0.8, alpha=0.6, zorder=1)

    # Threshold line
    ax.axvline(x=2.4, linestyle='--', color=GRAY, linewidth=0.8, alpha=0.5)
    ax.text(2.43, 0.75, 'threshold ~2.4', fontsize=7, color=GRAY, fontstyle='italic')

    # Plot points
    for i in range(len(subjects)):
        color = BLUE if improved[i] else RED_ORANGE
        ax.scatter(baselines[i], spec[i], c=color, s=50, zorder=3,
                   edgecolors='black', linewidths=0.4)

    # Labels for selected subjects
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
                        fontsize=7.5, fontstyle='italic',
                        arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.5))

    ax.set_xlabel('Baseline Score (no context)')
    ax.set_ylabel('Spec Condition Score')
    ax.set_title('Global Gradient: Spec Impact Across 14 Subjects')
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_aspect('equal')

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.4, label='Improved with spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=RED_ORANGE, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.4, label='Not improved'),
        plt.Line2D([0], [0], linestyle='--', color=GRAY, linewidth=0.8, label='y = x (no change)'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')

    save(fig, 'fig1_global_gradient.png')


# ════════════════════════════════════════════════════════════════
# Fig 2: Compression Curve (Hamerton)
# ════════════════════════════════════════════════════════════════
def fig2():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))

    colors = [comp_colors_map[c] for c in comp_conditions]
    ax.scatter(comp_tokens, comp_scores, c=colors, s=80, zorder=3, edgecolors='black', linewidths=0.5)
    ax.set_xscale('log')

    label_set = {'C5 Baseline', 'C2a Spec', 'C3 Letta+Spec', 'C9 Raw', 'C4 All Facts'}
    offsets = {
        'C5 Baseline': (-6, -14),
        'C2a Spec': (-10, 10),
        'C3 Letta+Spec': (8, 8),
        'C9 Raw': (8, -10),
        'C4 All Facts': (8, -12),
    }
    for i, cond in enumerate(comp_conditions):
        if cond in label_set:
            dx, dy = offsets[cond]
            ax.annotate(cond, (comp_tokens[i], comp_scores[i]),
                        xytext=(dx, dy), textcoords='offset points',
                        fontsize=7.5, fontstyle='italic',
                        arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.5))

    ax.set_xlabel('Context Tokens (log scale)')
    ax.set_ylabel('Judge Score (1-5)')
    ax.set_title('Compression Curve: Hamerton Conditions by Token Count')

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GRAY, markersize=7, label='Baseline'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GOLD, markersize=7, label='Memory system alone'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=7, label='Spec alone'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GREEN, markersize=7, label='Memory + Spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=PURPLE, markersize=7, label='All facts / Facts+Spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=RED_ORANGE, markersize=7, label='Raw corpus'),
    ]
    ax.legend(handles=handles, loc='lower left', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')
    ax.set_ylim(1.0, 3.8)

    save(fig, 'fig2_compression_curve.png')


# ════════════════════════════════════════════════════════════════
# Fig 3: Retrieval Disagreement
# ════════════════════════════════════════════════════════════════
def fig3():
    fig, ax = plt.subplots(figsize=(5, 3.5))

    labels = ['Top-1', 'Top-3', 'Top-5', 'Top-10']
    values = [68, 39, 22, 11]

    bars = ax.bar(labels, values, color=BLUE, width=0.55, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f'{val}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylabel('Disagreement Rate (%)')
    ax.set_title('Retrieval Disagreement Across Memory Systems')
    ax.set_ylim(0, 82)

    save(fig, 'fig3_retrieval_disagreement.png')


# ════════════════════════════════════════════════════════════════
# Fig 4: Hedging Reduction
# ════════════════════════════════════════════════════════════════
def fig4():
    fig, ax = plt.subplots(figsize=(5, 3.5))

    labels = ['Without Spec', 'With Spec']
    values = [51, 31]
    colors = [RED_ORANGE, BLUE]

    bars = ax.bar(labels, values, color=colors, width=0.45, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{val}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Arrow annotation
    ax.annotate('', xy=(1, 35), xytext=(0, 47),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(0.5, 43, '39% reduction', ha='center', fontsize=8.5, fontweight='bold')

    ax.set_ylabel('Hedging Language (%)')
    ax.set_title('Hedging Reduction with Behavioral Specification')
    ax.set_ylim(0, 65)

    save(fig, 'fig4_hedging_reduction.png')


# ════════════════════════════════════════════════════════════════
# Fig 5: Condition Effects Composite (2 panels)
# ════════════════════════════════════════════════════════════════
def fig5():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), gridspec_kw={'width_ratios': [1.2, 1]})

    conditions = ['Baseline', 'Spec', 'Wrong\nSpec', 'Facts', 'Facts+\nSpec']
    n = len(subjects)

    # Build per-condition arrays (14 subjects, REAL data)
    all_scores = np.array([
        baselines,
        spec,
        wrong_spec,
        facts,
        facts_spec,
    ]).T  # shape (14, 5)

    improved = [spec[i] > baselines[i] for i in range(n)]

    # Panel A: Slope chart
    x_pos = np.arange(5)
    for i in range(n):
        color = BLUE if improved[i] else RED_ORANGE
        ax1.plot(x_pos, all_scores[i], color=color, alpha=0.5, linewidth=1.0, zorder=2)
        ax1.scatter(x_pos, all_scores[i], color=color, s=12, zorder=3, edgecolors='none')

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(conditions)
    ax1.set_ylabel('Judge Score (1-5)')
    ax1.set_title('A. Per-Subject Trajectories (N=14)')
    handles = [
        plt.Line2D([0], [0], color=BLUE, linewidth=1.2, label='Improved'),
        plt.Line2D([0], [0], color=RED_ORANGE, linewidth=1.2, label='Not improved'),
    ]
    ax1.legend(handles=handles, loc='upper left', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')

    # Panel B: Box plots
    bp = ax2.boxplot([all_scores[:, j] for j in range(5)],
                     tick_labels=conditions, patch_artist=True, widths=0.5,
                     medianprops=dict(color='black', linewidth=1.2),
                     whiskerprops=dict(linewidth=0.8),
                     capprops=dict(linewidth=0.8),
                     flierprops=dict(marker='o', markersize=3))

    box_colors = [GRAY, BLUE, RED_ORANGE, PURPLE, GREEN]
    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax2.set_ylabel('Judge Score (1-5)')
    ax2.set_title('B. Score Distributions by Condition')

    fig.tight_layout(w_pad=3)
    save(fig, 'fig5_condition_effects.png')


# ════════════════════════════════════════════════════════════════
# Fig 6: Wrong Spec Control (paired dot plot)
# ════════════════════════════════════════════════════════════════
def fig6():
    fig, ax = plt.subplots(figsize=(6.8, 4.5))

    # Sort by baseline (lowest at top)
    order = np.argsort(baselines)
    y_positions = np.arange(len(subjects))

    for rank, idx in enumerate(order):
        bl = baselines[idx]
        ws = wrong_spec[idx]
        cs = spec[idx]

        # Connecting line from baseline to correct spec
        ax.plot([bl, cs], [rank, rank], color='#CCCCCC', linewidth=0.8, zorder=1)

        # Dots
        ax.scatter(bl, rank, color=GRAY, s=40, zorder=3, edgecolors='black', linewidths=0.3)
        ax.scatter(ws, rank, color=RED_ORANGE, s=40, zorder=3, edgecolors='black', linewidths=0.3)
        ax.scatter(cs, rank, color=BLUE, s=40, zorder=3, edgecolors='black', linewidths=0.3)

    sorted_names = [subjects[i] for i in order]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(sorted_names, fontsize=7.5)
    ax.set_xlabel('Judge Score (1-5)')
    ax.set_title('Wrong Spec Control: Baseline vs. Wrong Spec vs. Correct Spec')

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GRAY, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.3, label='Baseline'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=RED_ORANGE, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.3, label='Wrong spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.3, label='Correct spec'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')
    ax.set_xlim(0.5, 3.8)

    save(fig, 'fig6_wrong_spec_control.png')


# ════════════════════════════════════════════════════════════════
# Fig 7: Memory System Comparison
# ════════════════════════════════════════════════════════════════
def fig7():
    fig, ax = plt.subplots(figsize=(6, 4))

    x = np.arange(len(mem_systems))
    width = 0.32

    bars1 = ax.bar(x - width / 2, mem_without, width, color=GRAY, label='Without spec',
                   edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width / 2, mem_with, width, color=BLUE, label='With spec',
                   edgecolor='white', linewidth=0.5)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=7.5)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=7.5)

    for i in range(len(mem_systems)):
        pct = (mem_with[i] - mem_without[i]) / mem_without[i] * 100
        mid_x = x[i]
        top_y = max(mem_with[i], mem_without[i]) + 0.18
        ax.text(mid_x, top_y, f'+{pct:.0f}%', ha='center', va='bottom',
                fontsize=7.5, fontweight='bold', color=BLUE)

    ax.set_xticks(x)
    ax.set_xticklabels(mem_systems)
    ax.set_ylabel('Judge Score (1-5)')
    ax.set_title('Memory Systems: With vs. Without Behavioral Specification')
    ax.set_ylim(0, 4.0)
    ax.legend(frameon=True, framealpha=0.9, edgecolor='#CCCCCC')

    save(fig, 'fig7_memory_systems.png')


# ════════════════════════════════════════════════════════════════
# Fig 8: Judge Agreement Heatmap
# ════════════════════════════════════════════════════════════════
def fig8():
    fig, ax = plt.subplots(figsize=(5.5, 5))

    norm = Normalize(vmin=0.85, vmax=1.0)
    cmap = plt.cm.Blues

    im = ax.imshow(rho_matrix, cmap=cmap, norm=norm, aspect='equal')

    ax.set_xticks(range(len(judge_names)))
    ax.set_yticks(range(len(judge_names)))
    ax.set_xticklabels(judge_names, rotation=45, ha='right')
    ax.set_yticklabels(judge_names)

    for i in range(len(judge_names)):
        for j in range(len(judge_names)):
            val = rho_matrix[i, j]
            text_color = 'white' if val > 0.95 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=7.5, color=text_color)

    ax.set_title('Inter-Judge Agreement (Spearman rho)')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Spearman rho')

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    fig.tight_layout()
    save(fig, 'fig8_judge_agreement.png')


# ════════════════════════════════════════════════════════════════
# Fig 9: Cultural Region Baseline
# ════════════════════════════════════════════════════════════════
def fig9():
    fig, ax = plt.subplots(figsize=(6, 4.5))

    # Sort by baseline (lowest at top)
    order = np.argsort(baselines)

    sorted_regions = [regions[i] for i in order]
    sorted_baselines = [baselines[i] for i in order]
    improved = [spec[order[rank]] > baselines[order[rank]] for rank in range(len(subjects))]

    colors = [BLUE if imp else RED_ORANGE for imp in improved]

    ax.barh(range(len(sorted_regions)), sorted_baselines, color=colors, height=0.6,
            edgecolor='white', linewidth=0.5)

    ax.axvline(x=2.4, linestyle='--', color=GRAY, linewidth=0.8, alpha=0.6)
    ax.text(2.43, len(sorted_regions) - 0.5, 'threshold\n~2.4', fontsize=7, color=GRAY,
            fontstyle='italic', va='top')

    ax.set_yticks(range(len(sorted_regions)))
    ax.set_yticklabels(sorted_regions, fontsize=7.5)
    ax.set_xlabel('Baseline Score (1-5)')
    ax.set_title('Baseline Recognizability by Cultural Region')

    handles = [
        mpatches.Patch(color=BLUE, label='Spec improved score'),
        mpatches.Patch(color=RED_ORANGE, label='Spec did not improve'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')
    ax.set_xlim(0, 3.5)

    save(fig, 'fig9_cultural_baseline.png')


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating 9 figures for Beyond Recall (v3 - real data)...")
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
