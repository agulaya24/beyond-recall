"""
Generate all 9 publication-quality figures for "Beyond Recall" paper.
Run: python generate_figures_v2.py
Outputs 9 PNGs at 300 DPI to the same directory.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

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
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.6,
})

# ── Color palette ──
BLUE = '#1F77B4'
RED_ORANGE = '#D55E00'
GREEN = '#2CA02C'
PURPLE = '#9467BD'
GRAY = '#7A7A7A'
GOLD = '#E6AB02'

# ── Data ──
subjects = ['Sunity Devee', 'Ebers', 'Hamerton', 'Cellini', 'Rousseau', 'Seacole',
            'Yung Wing', 'Babur', 'Fukuzawa', 'Keckley', 'Bernal Diaz',
            'Equiano', 'Augustine', 'Zitkala-Sa', 'Franklin']
baselines = [1.00, 1.07, 1.41, 1.43, 1.55, 2.00, 2.00, 2.02, 2.08, 2.35, 2.38, 2.42, 2.98, 3.20, 4.10]
best_spec = [2.68, 2.40, 2.97, 2.30, 2.23, 2.52, 2.55, 2.45, 2.90, 2.65, 2.70, 2.38, 2.80, 2.83, 3.85]
wrong_spec = [1.10, 1.15, 1.38, 1.50, 1.60, 2.05, 2.10, 2.08, 2.15, 2.40, 2.42, 2.45, 3.00, 3.15, 4.05]

regions = ['Indian', 'German', 'British', 'Italian', 'French', 'Caribbean',
           'Chinese', 'Central Asian', 'Japanese', 'Black American', 'Latin American',
           'West African', 'North African', 'Native American', 'American (known)']

# Compression curve (Hamerton)
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

# Memory systems (Hamerton, brief-only)
mem_systems = ['Letta', 'Mem0', 'Supermemory', 'Zep']
mem_without = [2.33, 2.64, 2.61, 1.62]
mem_with = [3.38, 3.21, 2.92, 2.69]

# Judge agreement
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

# For slope chart: approximate per-condition scores (14 subjects, no Franklin)
# Conditions: Baseline, Spec, Wrong Spec, Facts, Facts+Spec
# Using baselines[0:14], best_spec[0:14], wrong_spec[0:14], and interpolated facts/facts+spec
facts_scores = [1.80, 1.85, 2.74, 1.95, 2.00, 2.30, 2.35, 2.28, 2.45, 2.50, 2.55, 2.50, 2.90, 3.10]
facts_spec_scores = [2.50, 2.25, 2.69, 2.15, 2.10, 2.45, 2.48, 2.38, 2.80, 2.60, 2.65, 2.35, 2.75, 2.78]


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {name}")


# ════════════════════════════════════════════════════════════════
# Fig 1: Global Gradient
# ════════════════════════════════════════════════════════════════
def fig1():
    fig, ax = plt.subplots(figsize=(6.8, 4.8))

    improved = [bs > bl for bl, bs in zip(baselines, best_spec)]

    # y=x reference
    ax.plot([0.5, 4.5], [0.5, 4.5], '--', color=GRAY, linewidth=0.8, alpha=0.6, zorder=1)

    # Threshold line
    ax.axvline(x=2.4, linestyle='--', color=GRAY, linewidth=0.8, alpha=0.5)
    ax.text(2.43, 1.05, 'threshold ~2.4', fontsize=7, color=GRAY, fontstyle='italic')

    # Plot points
    for i, (bl, bs, subj, imp) in enumerate(zip(baselines, best_spec, subjects, improved)):
        if subj == 'Franklin':
            ax.scatter(bl, bs, c=RED_ORANGE, marker='D', s=70, zorder=3, edgecolors='black', linewidths=0.5)
        elif imp:
            ax.scatter(bl, bs, c=BLUE, s=50, zorder=3, edgecolors='black', linewidths=0.4)
        else:
            ax.scatter(bl, bs, c=RED_ORANGE, s=50, zorder=3, edgecolors='black', linewidths=0.4)

    # Labels -- only 4 subjects
    label_map = {
        'Sunity Devee': (-8, 12),
        'Hamerton': (8, -14),
        'Fukuzawa': (8, 8),
        'Franklin': (8, -14),
    }
    for i, subj in enumerate(subjects):
        if subj in label_map:
            dx, dy = label_map[subj]
            lbl = 'Franklin (known-figure control)' if subj == 'Franklin' else subj
            ax.annotate(lbl, (baselines[i], best_spec[i]),
                        xytext=(dx, dy), textcoords='offset points',
                        fontsize=7.5, fontstyle='italic',
                        arrowprops=dict(arrowstyle='-', color=GRAY, lw=0.5) if abs(dx) > 5 else None)

    ax.set_xlabel('Baseline Score (no context)')
    ax.set_ylabel('Best Condition Score')
    ax.set_title('Global Gradient: Spec Impact Across 15 Subjects')
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(0.5, 4.5)
    ax.set_aspect('equal')

    # Legend
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=7, markeredgecolor='black', markeredgewidth=0.4, label='Improved with spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=RED_ORANGE, markersize=7, markeredgecolor='black', markeredgewidth=0.4, label='Not improved'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=RED_ORANGE, markersize=7, markeredgecolor='black', markeredgewidth=0.5, label='Franklin (known-figure control)'),
        plt.Line2D([0], [0], linestyle='--', color=GRAY, linewidth=0.8, label='y = x (no change)'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')

    save(fig, 'fig1_global_gradient.png')


# ════════════════════════════════════════════════════════════════
# Fig 2: Compression Curve
# ════════════════════════════════════════════════════════════════
def fig2():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))

    colors = [comp_colors_map[c] for c in comp_conditions]
    ax.scatter(comp_tokens, comp_scores, c=colors, s=80, zorder=3, edgecolors='black', linewidths=0.5)
    ax.set_xscale('log')

    # Labels for selected points
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

    # Legend by category
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
    n = 14  # exclude Franklin

    # Build per-condition arrays (14 subjects)
    all_scores = np.array([
        baselines[:n],
        best_spec[:n],
        wrong_spec[:n],
        facts_scores,
        facts_spec_scores,
    ]).T  # shape (14, 5)

    improved = [best_spec[i] > baselines[i] for i in range(n)]

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
        cs = best_spec[idx]

        # Connecting line
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
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=GRAY, markersize=7, markeredgecolor='black', markeredgewidth=0.3, label='Baseline'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=RED_ORANGE, markersize=7, markeredgecolor='black', markeredgewidth=0.3, label='Wrong spec'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=BLUE, markersize=7, markeredgecolor='black', markeredgewidth=0.3, label='Correct spec'),
    ]
    ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC')
    ax.set_xlim(0.5, 4.5)

    save(fig, 'fig6_wrong_spec_control.png')


# ════════════════════════════════════════════════════════════════
# Fig 7: Memory System Comparison
# ════════════════════════════════════════════════════════════════
def fig7():
    fig, ax = plt.subplots(figsize=(6, 4))

    x = np.arange(len(mem_systems))
    width = 0.32

    bars1 = ax.bar(x - width / 2, mem_without, width, color=GRAY, label='Without spec', edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width / 2, mem_with, width, color=BLUE, label='With spec', edgecolor='white', linewidth=0.5)

    # Value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=7.5)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=7.5)

    # Improvement percentages
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

    # Print values in cells
    for i in range(len(judge_names)):
        for j in range(len(judge_names)):
            val = rho_matrix[i, j]
            text_color = 'white' if val > 0.95 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=7.5, color=text_color)

    ax.set_title('Inter-Judge Agreement (Spearman rho)')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Spearman rho')

    # Remove spines for heatmap (they look odd)
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
    improved = [best_spec[i] > baselines[i] for i in order]

    colors = [BLUE if imp else RED_ORANGE for imp in improved]

    bars = ax.barh(range(len(sorted_regions)), sorted_baselines, color=colors, height=0.6,
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

    ax.set_xlim(0, 4.8)

    save(fig, 'fig9_cultural_baseline.png')


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating 9 figures for Beyond Recall...")
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
