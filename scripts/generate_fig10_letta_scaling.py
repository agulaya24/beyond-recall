"""Figure 10: Letta stateful-agent block size growth vs. Base Layer spec size,
plus duplication percentage at scale.

Data sources: DATA_REFERENCE.md §7, KEY_FINDINGS.md M6 and M7.

2026-04-22 revision: colorblind-safe palette, clearer axis labels,
paper-scale typography.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parents[1] / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Paper-scale typography + colorblind palette
sns.set_theme(context='paper', style='whitegrid', palette='colorblind')
plt.rcParams.update({
    'font.size': 8.5,
    'axes.titlesize': 9.5,
    'axes.labelsize': 8.5,
    'legend.fontsize': 7.5,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
})

CB = sns.color_palette('colorblind')
BLUE = CB[0]
ORANGE = CB[1]
GREEN = CB[2]
GRAY = '#7A7A7A'

subjects = ["Hamerton", "Ebers", "Babur"]
corpus_words = [25231, 48161, 222742]
letta_block_chars = [22472, 68413, 335349]
bl_spec_chars = [34579, 39708, 37063]
api_ceiling = 333000
duplication_pct = [0.0, 0.0, 25.4]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))

# Panel 1: block size vs corpus size (colorblind-safe, shape + color redundancy)
ax1.plot(
    corpus_words, letta_block_chars, marker="o", linewidth=1.6,
    label="Letta stateful-agent block", color=ORANGE, markersize=8,
    markeredgecolor='black', markeredgewidth=0.5,
)
ax1.plot(
    corpus_words, bl_spec_chars, marker="s", linewidth=1.6,
    label="Base Layer specification", color=BLUE, markersize=8,
    markeredgecolor='black', markeredgewidth=0.5,
)
ax1.axhline(
    y=api_ceiling, color=GRAY, linestyle="--", linewidth=1.2,
    label=f"Letta API ceiling ({api_ceiling:,} chars)",
)

# Label Letta-block points (upper curve); offsets avoid overlap with the BL curve.
label_offsets = {'Hamerton': (-8, -22), 'Ebers': (12, 12), 'Babur': (-60, -16)}
for i, subj in enumerate(subjects):
    dx, dy = label_offsets[subj]
    ax1.annotate(
        subj, xy=(corpus_words[i], letta_block_chars[i]),
        xytext=(dx, dy), textcoords="offset points", fontsize=8.5, fontweight="bold",
    )

ax1.set_xlabel("Source corpus size (words)")
ax1.set_ylabel("Memory block / specification size (characters)")
ax1.set_title("Letta block grows with source; Base Layer spec stays bounded")
ax1.legend(loc="upper left", frameon=True, framealpha=0.92, edgecolor='#CCCCCC')
ax1.grid(True, alpha=0.3, linewidth=0.5)
ax1.set_xlim(0, 260000)
ax1.set_ylim(0, 380000)

# Panel 2: duplication % — hatch redundancy on the high-duplication bar
colors = [BLUE if d < 5 else ORANGE for d in duplication_pct]
hatches = ['' if d < 5 else '//' for d in duplication_pct]
bars = ax2.bar(
    subjects, duplication_pct, color=colors, edgecolor="black", linewidth=0.8, width=0.55,
)
for bar, hat in zip(bars, hatches):
    bar.set_hatch(hat)

ax2.set_ylabel("Verbatim sentence duplication (%)")
ax2.set_title("Letta block coherence degrades before size ceiling")
ax2.set_ylim(0, 30)
ax2.grid(True, axis="y", alpha=0.3, linewidth=0.5)

for bar, val in zip(bars, duplication_pct):
    ax2.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.6, f"{val:.1f}%",
        ha="center", va="bottom", fontsize=9, fontweight="bold",
    )

# Subject+size on x-axis in two lines
labels_with_size = [f"{s}\n{c:,} chars" for s, c in zip(subjects, letta_block_chars)]
ax2.set_xticks(range(len(subjects)))
ax2.set_xticklabels(labels_with_size, fontsize=7.5)

plt.tight_layout()
outfile = FIG_DIR / "fig10_letta_scaling.png"
plt.savefig(outfile, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Wrote: {outfile}")
