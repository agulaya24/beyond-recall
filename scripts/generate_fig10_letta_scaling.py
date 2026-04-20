"""Figure 10: Letta stateful-agent block size growth vs. Base Layer spec size,
plus duplication percentage at scale.

Data sources: DATA_REFERENCE.md §7, KEY_FINDINGS.md M6 and M7.
"""

import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(r"C:\Users\Aarik\Anthropic\memory-study-repo\figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

subjects = ["Hamerton", "Ebers", "Babur"]
corpus_words = [25231, 48161, 222742]
letta_block_chars = [22472, 68413, 335349]
bl_spec_chars = [34579, 39708, 37063]
api_ceiling = 333000
duplication_pct = [0.0, 0.0, 25.4]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

# Panel 1: block size vs corpus size
ax1.plot(
    corpus_words,
    letta_block_chars,
    marker="o",
    linewidth=2,
    label="Letta stateful-agent block",
    color="#c0392b",
    markersize=9,
)
ax1.plot(
    corpus_words,
    bl_spec_chars,
    marker="s",
    linewidth=2,
    label="Base Layer specification",
    color="#2980b9",
    markersize=9,
)
ax1.axhline(
    y=api_ceiling,
    color="gray",
    linestyle="--",
    linewidth=1.5,
    label=f"Letta API ceiling ({api_ceiling:,} chars)",
)

for i, subj in enumerate(subjects):
    ax1.annotate(
        subj,
        xy=(corpus_words[i], letta_block_chars[i]),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
    )

ax1.set_xlabel("Source corpus size (words)", fontsize=11)
ax1.set_ylabel("Block / spec size (characters)", fontsize=11)
ax1.set_title(
    "Letta block grows with source; Base Layer spec stays bounded",
    fontsize=12,
)
ax1.legend(loc="upper left", fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 260000)
ax1.set_ylim(0, 380000)

# Panel 2: duplication %
colors = ["#2980b9" if d < 5 else "#c0392b" for d in duplication_pct]
bars = ax2.bar(
    subjects,
    duplication_pct,
    color=colors,
    edgecolor="black",
    linewidth=1.2,
    width=0.55,
)
ax2.set_ylabel("Verbatim sentence duplication (%)", fontsize=11)
ax2.set_title(
    "Letta block coherence degrades before size ceiling",
    fontsize=12,
)
ax2.set_ylim(0, 30)
ax2.grid(True, axis="y", alpha=0.3)

for bar, val in zip(bars, duplication_pct):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.6,
        f"{val:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
    )

# Annotate block sizes under each bar
for i, (bar, chars) in enumerate(zip(bars, letta_block_chars)):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        -1.5,
        f"{chars:,} chars",
        ha="center",
        va="top",
        fontsize=9,
        color="#555",
    )

plt.tight_layout()
outfile = FIG_DIR / "fig10_letta_scaling.png"
plt.savefig(outfile, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Wrote: {outfile}")
