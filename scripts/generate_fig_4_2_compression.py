"""
Figure 4.2: Score vs. context size across conditions, per subject.

X-axis (log scale): approximate tokens served as context.
Y-axis: 5-judge primary score.
One line per subject (faint), connecting its (C5, C2a, C4, C8, C4a, C9) points.
Bold aggregate curve (median across subjects per condition) makes the compression
story readable without decoding individual traces.

2026-04-22 revision: colorblind palette + aggregate overlay to de-emphasize individual
trajectories; condition-code annotations above x-axis replace cryptic floating labels;
paper-scale typography.
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
    'axes.titlesize': 10.5,
    'axes.labelsize': 9.5,
    'legend.fontsize': 7.5,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
})

# Approx token counts (1.3 tokens/word) for C8/C9
WORD_COUNTS = {
    'Hamerton': 25231, 'Sunity Devee': 67379, 'Ebers': 96174,
    'Fukuzawa': 139088, 'Bernal Diaz': 187315, 'Babur': 422772,
    'Seacole': 62467, 'Keckley': 58742, 'Yung Wing': 66459,
}

# 5-judge primary scores per subject per condition
SCORES = {
    'Hamerton':     {'C5': 1.26, 'C2a': 2.63, 'C4': 2.43, 'C8': 2.27, 'C4a': 2.77, 'C9': 3.09},
    'Sunity Devee': {'C5': 1.03, 'C2a': 2.27, 'C4': 2.46, 'C8': 2.55, 'C4a': 2.41, 'C9': 2.46},
    'Ebers':        {'C5': 1.02, 'C2a': 1.54, 'C4': 2.02, 'C8': 2.18, 'C4a': 2.07, 'C9': 2.16},
    'Fukuzawa':     {'C5': 1.67, 'C2a': 2.35, 'C4': 2.67, 'C8': 2.74, 'C4a': 2.78, 'C9': 2.78},
    'Bernal Diaz':  {'C5': 1.70, 'C2a': 2.27, 'C4': 2.41, 'C8': 2.55, 'C4a': 2.48, 'C9': 2.53},
    'Babur':        {'C5': 1.76, 'C2a': 1.91, 'C4': 2.03, 'C8': 2.05, 'C4a': 2.01, 'C9': None},
    'Seacole':      {'C5': 1.77, 'C2a': 2.48, 'C4': 2.63, 'C8': 2.83, 'C4a': 2.59, 'C9': 2.73},
    'Keckley':      {'C5': 1.84, 'C2a': 2.43, 'C4': 2.39, 'C8': 2.50, 'C4a': 2.44, 'C9': 2.49},
    'Yung Wing':    {'C5': 1.88, 'C2a': 2.22, 'C4': 2.13, 'C8': 2.42, 'C4a': 2.40, 'C9': 2.50},
}


def tokens(cond, subject):
    wc = WORD_COUNTS[subject]
    corpus_tokens = int(wc * 1.3)
    if cond == 'C5': return 100
    if cond == 'C2a': return 7000
    if cond == 'C4':  return 10000
    if cond == 'C8':  return corpus_tokens
    if cond == 'C4a': return 17000
    if cond == 'C9':  return corpus_tokens + 7000
    return None


def main():
    fig, ax = plt.subplots(figsize=(10, 6.0))

    # Thin-trace per-subject lines (colorblind palette, cycled)
    subjects_ordered = sorted(SCORES.keys(), key=lambda s: SCORES[s]['C5'])
    palette = sns.color_palette('colorblind', n_colors=len(subjects_ordered))

    # Aggregate summary: median score per condition across subjects
    cond_order = ['C5', 'C2a', 'C4', 'C4a', 'C8', 'C9']
    agg_x = []
    agg_y = []
    for cond in cond_order:
        # Use first subject's WORD_COUNTS-independent token estimate for non-C8/C9
        # For C8/C9, take median across subjects
        if cond in ('C8', 'C9'):
            ts = [tokens(cond, s) for s in subjects_ordered if SCORES[s][cond] is not None]
            agg_x.append(float(np.median(ts)))
        else:
            agg_x.append(tokens(cond, subjects_ordered[0]))
        ys = [SCORES[s][cond] for s in subjects_ordered if SCORES[s][cond] is not None]
        agg_y.append(float(np.median(ys)))

    # Order by x
    order = np.argsort(agg_x)
    agg_x = [agg_x[i] for i in order]
    agg_y = [agg_y[i] for i in order]

    # Per-subject traces (faint)
    for i, subject in enumerate(subjects_ordered):
        scores = SCORES[subject]
        xs, ys = [], []
        for cond in ['C5', 'C2a', 'C4', 'C8', 'C4a', 'C9']:
            if scores[cond] is None:
                continue
            xs.append(tokens(cond, subject))
            ys.append(scores[cond])
        sort = np.argsort(xs)
        xs = [xs[j] for j in sort]
        ys = [ys[j] for j in sort]
        ax.plot(xs, ys, 'o-', color=palette[i], alpha=0.35,
                linewidth=0.9, markersize=3.5, label=subject)

    # Bold aggregate median curve on top
    ax.plot(agg_x, agg_y, 'o-', color='black', linewidth=2.2, markersize=7.5,
            markeredgecolor='white', markeredgewidth=0.8, label='Median across subjects',
            zorder=10)

    ax.set_xscale('log')
    ax.set_xlabel('Context size served to response model (approximate tokens, log scale)')
    ax.set_ylabel('5-judge primary score (1-5 rubric)')
    ax.set_title('Figure 4.2 — Compression: score vs. context size across low-baseline subjects')
    ax.grid(True, alpha=0.3, linewidth=0.5, which='both')
    ax.set_ylim(0.8, 3.3)
    ax.set_xlim(50, 700000)

    # Condition-code reference markers at actual x-locations (replace floating top labels)
    # Reference points: C5 at ~100, C2a at 7k, C4a at 17k, C9 representative at ~300k median
    ref_conds = [
        ('C5',  100,    'minimum context'),
        ('C2a', 7000,   'spec ~7K'),
        ('C4a', 17000,  'facts+spec ~17K'),
        ('C9',  300000, 'raw corpus +spec ~300K'),
    ]
    for label, x_loc, desc in ref_conds:
        ax.axvline(x_loc, color='#BBBBBB', linewidth=0.6, linestyle=':', alpha=0.8, zorder=1)
        ax.text(x_loc, 3.24, f'{label}\n{desc}', fontsize=7, ha='center', va='top',
                color='#444',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                          edgecolor='#DDDDDD', linewidth=0.5, alpha=0.9))

    # Legend: aggregate first, subjects in 2 compact columns
    handles, labels = ax.get_legend_handles_labels()
    # Reorder: 'Median across subjects' first
    try:
        idx = labels.index('Median across subjects')
        handles = [handles[idx]] + handles[:idx] + handles[idx+1:]
        labels  = [labels[idx]]  + labels[:idx]  + labels[idx+1:]
    except ValueError:
        pass
    ax.legend(handles, labels, loc='lower right', fontsize=7, framealpha=0.92,
              edgecolor='#CCCCCC', ncol=2)

    plt.tight_layout()
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / 'fig_4_2_compression.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    print(f'Saved: {out}')
    out_pdf = FIG_DIR / 'fig_4_2_compression.pdf'
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_pdf}')


if __name__ == '__main__':
    main()
