"""Generate figures for the Beyond Recall paper."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Global style
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
})

FIGDIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Figure 1 — Global Gradient: Baseline vs. Best Condition
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

subjects = ['Sunity Devee', 'Ebers', 'Hamerton', 'Cellini', 'Rousseau', 'Seacole',
            'Yung Wing', 'Babur', 'Fukuzawa', 'Keckley', 'Bernal Diaz', 'Equiano',
            'Augustine', 'Zitkala-Sa', 'Franklin']
baselines = [1.00, 1.07, 1.41, 1.43, 1.55, 2.00, 2.00, 2.02, 2.08, 2.35, 2.38, 2.42, 2.98, 3.20, 4.10]
best = [2.68, 2.40, 2.97, 2.30, 2.23, 2.52, 2.55, 2.45, 2.90, 2.65, 2.70, 2.38, 2.80, 2.83, 3.85]

improved = [b > bl for bl, b in zip(baselines, best)]
colors = ['#2166ac' if imp else '#b2182b' for imp in improved]

# y=x line
ax.plot([0.5, 4.5], [0.5, 4.5], color='#999999', linewidth=1, linestyle='-', zorder=1, label='No improvement')

# Threshold line
ax.axvline(x=2.4, color='#666666', linewidth=1, linestyle='--', zorder=1, alpha=0.7)
ax.text(2.43, 1.05, 'threshold\n(baseline ≈ 2.4)', fontsize=9, color='#666666', va='bottom')

# Points
for i, (bl, bt, subj, col) in enumerate(zip(baselines, best, subjects, colors)):
    ax.scatter(bl, bt, c=col, s=60, zorder=3, edgecolors='white', linewidth=0.5)
    label = subj
    if subj == 'Franklin':
        label = 'Franklin\n(known-figure control)'
    # Offset labels to avoid overlap
    offset_x, offset_y = 0.06, 0.06
    ha = 'left'
    if subj == 'Sunity Devee':
        offset_x = 0.06
        offset_y = 0.08
        va = 'bottom'
    elif subj == 'Ebers':
        offset_x = -0.06
        ha = 'right'
        va = 'bottom'
    elif subj == 'Hamerton':
        offset_x = -0.06
        ha = 'right'
        va = 'bottom'
    elif subj == 'Cellini':
        offset_x = 0.06
        offset_y = -0.15
        va = 'top'
    elif subj == 'Rousseau':
        offset_x = 0.06
        offset_y = -0.15
        va = 'top'
    elif subj == 'Seacole':
        offset_x = -0.06
        ha = 'right'
        offset_y = 0.08
        va = 'bottom'
    elif subj == 'Yung Wing':
        offset_x = -0.06
        ha = 'right'
        offset_y = -0.12
        va = 'top'
    elif subj == 'Babur':
        offset_x = 0.06
        offset_y = -0.15
        va = 'top'
    elif subj == 'Fukuzawa':
        offset_x = 0.06
        offset_y = 0.08
        va = 'bottom'
    elif subj == 'Keckley':
        offset_x = 0.06
        offset_y = -0.12
        va = 'top'
    elif subj == 'Bernal Diaz':
        offset_x = -0.06
        ha = 'right'
        va = 'bottom'
    elif subj == 'Equiano':
        offset_x = -0.06
        ha = 'right'
        offset_y = -0.10
        va = 'top'
    elif subj == 'Augustine':
        offset_x = 0.06
        offset_y = -0.15
        va = 'top'
    elif subj == 'Franklin':
        offset_x = -0.06
        ha = 'right'
        va = 'center'
        offset_y = 0.0
    elif subj == 'Zitkala-Sa':
        offset_x = 0.06
        offset_y = 0.08
        va = 'bottom'
    else:
        va = 'bottom'
    ax.annotate(label, (bl, bt), xytext=(bl + offset_x, bt + offset_y),
                fontsize=8, color=col, ha=ha, va=va, zorder=4)

ax.set_xlabel('Baseline Score (no specification)', fontsize=12)
ax.set_ylabel('Best Condition Score', fontsize=12)
ax.set_title('Global Gradient: Specification Impact Across 15 Subjects', fontsize=13, fontweight='bold')
ax.set_xlim(0.5, 4.5)
ax.set_ylim(0.8, 4.5)
ax.set_aspect('equal')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2166ac', markersize=8, label='Improved'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#b2182b', markersize=8, label='No improvement'),
    Line2D([0], [0], color='#999999', linewidth=1, label='y = x (no change)'),
]
ax.legend(handles=legend_elements, loc='upper left', frameon=False, fontsize=10)

plt.tight_layout()
fig.savefig(f'{FIGDIR}/fig1_global_gradient.png', dpi=300, bbox_inches='tight')
plt.close()
print('Figure 1 saved.')

# ============================================================
# Figure 2 — Compression Curve: Context Size vs. Score
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

conditions = ['C5\nBaseline', 'C1\nMem0', 'C1\nSM', 'C2a\nSpec', 'C3\nMem0+Spec',
              'C3\nSM+Spec', 'C3\nLetta+Spec', 'C4\nAll Facts', 'C4a\nFacts+Spec', 'C9\nRaw Corpus']
tokens = [47, 302, 247, 2562, 2837, 2782, 2790, 9583, 12103, 34144]
scores = [1.41, 2.64, 2.61, 2.77, 3.21, 2.92, 3.38, 2.74, 2.69, 2.31]

# Color by category
cat_colors = {
    'baseline': '#999999',
    'memory': '#fc8d62',
    'spec': '#2166ac',
    'combined': '#66c2a5',
    'raw': '#e78ac3',
}
point_colors = [
    cat_colors['baseline'],  # C5
    cat_colors['memory'],    # C1 Mem0
    cat_colors['memory'],    # C1 SM
    cat_colors['spec'],      # C2a
    cat_colors['combined'],  # C3 Mem0+Spec
    cat_colors['combined'],  # C3 SM+Spec
    cat_colors['combined'],  # C3 Letta+Spec
    cat_colors['raw'],       # C4
    cat_colors['combined'],  # C4a
    cat_colors['raw'],       # C9
]

for i, (t, s, c, col) in enumerate(zip(tokens, scores, conditions, point_colors)):
    ax.scatter(t, s, c=col, s=80, zorder=3, edgecolors='white', linewidth=0.5)
    # Label positioning - manual offsets to avoid overlaps
    ox_pts, oy_pts = 0, 10
    ha, va = 'center', 'bottom'
    clabel = c.replace('\n', ' ')
    if 'Letta' in c:
        ox_pts, oy_pts = 5, 10
        ha = 'left'
    elif 'SM+Spec' in c:
        ox_pts, oy_pts = 0, -10
        va = 'top'
    elif 'Mem0+Spec' in c:
        ox_pts, oy_pts = -5, 10
        ha = 'right'
    elif c.startswith('C1\nSM'):
        ox_pts, oy_pts = -5, -10
        ha, va = 'right', 'top'
    elif c.startswith('C1\nMem0'):
        ox_pts, oy_pts = 5, 10
        ha = 'left'
    elif 'C2a' in c:
        ox_pts, oy_pts = 0, 10
    elif 'Facts+Spec' in c:
        ox_pts, oy_pts = 0, -10
        va = 'top'
    elif 'All Facts' in c:
        ox_pts, oy_pts = 5, 10
        ha = 'left'
    elif 'Raw' in c:
        ox_pts, oy_pts = 0, -10
        va = 'top'
    elif 'Baseline' in c:
        ox_pts, oy_pts = 5, -8
        ha, va = 'left', 'top'
    ax.annotate(clabel, (t, s), xytext=(ox_pts, oy_pts),
                textcoords='offset points', fontsize=8, color=col, ha=ha, va=va, zorder=4)

ax.set_xscale('log')
ax.set_xlabel('Average Input Tokens (log scale)', fontsize=12)
ax.set_ylabel('Mean Judge Score (1–5)', fontsize=12)
ax.set_title('Compression Curve: Context Size vs. Prediction Accuracy (Hamerton)', fontsize=13, fontweight='bold')
ax.set_ylim(1.0, 4.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_colors['baseline'], markersize=8, label='Baseline'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_colors['memory'], markersize=8, label='Memory system only'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_colors['spec'], markersize=8, label='Specification only'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_colors['combined'], markersize=8, label='Combined'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=cat_colors['raw'], markersize=8, label='Raw/all facts'),
]
ax.legend(handles=legend_elements, loc='upper left', frameon=False, fontsize=9)

plt.tight_layout()
fig.savefig(f'{FIGDIR}/fig2_compression_curve.png', dpi=300, bbox_inches='tight')
plt.close()
print('Figure 2 saved.')

# ============================================================
# Figure 3 — Retrieval Disagreement Across Memory Systems
# ============================================================
fig, ax = plt.subplots(figsize=(6, 4))

topk_labels = ['Top-1', 'Top-3', 'Top-5', 'Top-10']
zero_overlap = [68, 39, 22, 11]

bars = ax.bar(topk_labels, zero_overlap, color='#2166ac', width=0.55, edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, zero_overlap):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
            f'{val}%', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2166ac')

ax.set_xlabel('Retrieval Depth (top-K)', fontsize=12)
ax.set_ylabel('Zero Overlap Between Systems (%)', fontsize=12)
ax.set_title('Retrieval Disagreement Across Memory Systems', fontsize=13, fontweight='bold')
ax.set_ylim(0, 85)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
fig.savefig(f'{FIGDIR}/fig3_retrieval_disagreement.png', dpi=300, bbox_inches='tight')
plt.close()
print('Figure 3 saved.')

# ============================================================
# Figure 4 — Hedging Reduction
# ============================================================
fig, ax = plt.subplots(figsize=(6, 4))

labels = ['Without\nSpecification', 'With\nSpecification']
values = [51, 31]
bar_colors = ['#b2182b', '#2166ac']

bars = ax.bar(labels, values, color=bar_colors, width=0.5, edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f'{val}%', ha='center', va='bottom', fontsize=13, fontweight='bold', color=bar.get_facecolor())

# Annotation arrow showing reduction
ax.annotate('39% reduction',
            xy=(1, 31), xytext=(0.5, 65),
            fontsize=11, fontweight='bold', color='#333333', ha='center',
            arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))

ax.set_ylabel('Responses Containing Hedging Language (%)', fontsize=12)
ax.set_title('Hedging Reduction With Behavioral Specification', fontsize=13, fontweight='bold')
ax.set_ylim(0, 75)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
fig.savefig(f'{FIGDIR}/fig4_hedging_reduction.png', dpi=300, bbox_inches='tight')
plt.close()
print('Figure 4 saved.')

print('\nAll 4 figures generated successfully.')
