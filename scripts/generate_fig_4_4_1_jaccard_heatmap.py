"""Generate the §4.4.1 cross-system retrieval-overlap heatmap.

A 5x5 symmetric heatmap showing mean pairwise Jaccard similarity between every
pair of memory systems on the controlled retrieval configuration (n=5,460 =
all 14 subjects × 39 questions × 10 pairs).

Output: figures/fig_4_4_1_jaccard_heatmap_v1.{png,pdf}.
Data:   docs/research/retrieval_overlap_analysis_20260501.json (per_pair_per_config).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

REPO = Path("C:/Users/Aarik/Anthropic/memory-study-repo")
DATA = REPO / "docs" / "research" / "retrieval_overlap_analysis_20260501.json"
FIGS = REPO / "figures"

# Display order: Base Layer | Mem0 | Letta | Supermemory | Zep
SYSTEMS = ["baselayer", "mem0", "letta", "supermemory", "zep"]
LABELS = ["Base Layer", "Mem0", "Letta", "Supermemory", "Zep"]


def main() -> None:
    sns.set_theme(style="white", palette="colorblind")
    d = json.loads(DATA.read_text(encoding="utf-8"))
    pairs = [r for r in d["per_pair_per_config"] if r["config"] == "controlled"]

    # Build symmetric 5x5 matrix; diagonal = 1.0 (self-overlap)
    n = len(SYSTEMS)
    M = np.full((n, n), np.nan)
    for i in range(n):
        M[i, i] = 1.0
    for r in pairs:
        a, b = r["sys_a"], r["sys_b"]
        if a in SYSTEMS and b in SYSTEMS:
            i, j = SYSTEMS.index(a), SYSTEMS.index(b)
            v = r["mean_jaccard_raw"]
            M[i, j] = v
            M[j, i] = v

    # Annotate cells: numeric for off-diagonal pairs, hyphen for diagonal
    annot = np.empty_like(M, dtype=object)
    for i in range(n):
        for j in range(n):
            if i == j:
                annot[i, j] = "—"
            else:
                annot[i, j] = f"{M[i, j]:.3f}"

    fig, ax = plt.subplots(figsize=(7.0, 6.0), dpi=300)

    # Mask diagonal so the colorbar reflects only pairwise data
    mask = np.eye(n, dtype=bool)

    sns.heatmap(
        M,
        mask=mask,
        annot=annot,
        fmt="",
        cmap="viridis",
        vmin=0.0,
        vmax=0.16,
        cbar_kws={"label": "Mean pairwise Jaccard"},
        linewidths=0.6,
        linecolor="white",
        xticklabels=LABELS,
        yticklabels=LABELS,
        ax=ax,
        annot_kws={"fontsize": 11, "fontweight": "bold"},
    )

    # Color the diagonal cells gray
    for i in range(n):
        ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=True, facecolor="#dddddd",
                                   edgecolor="white", lw=0.6, zorder=2))
        ax.text(i + 0.5, i + 0.5, "—", ha="center", va="center",
                fontsize=11, color="#666666", zorder=3)

    ax.set_title(
        "Cross-system retrieval overlap (controlled config, K=10)\n"
        "Mean pairwise Jaccard across n=5,460 (system pair, question) instances",
        fontsize=11,
        pad=14,
    )
    ax.tick_params(axis="x", labelrotation=0)
    ax.tick_params(axis="y", labelrotation=0)
    plt.setp(ax.get_xticklabels(), fontsize=10)
    plt.setp(ax.get_yticklabels(), fontsize=10)

    # Footer note
    fig.text(
        0.02, 0.02,
        "Mean Jaccard 0.083 across 10 system pairs; lowest pair Supermemory–Zep 0.025; "
        "highest Base Layer–Supermemory 0.146.\n"
        "Source: scripts/analyze_retrieval_overlap.py.",
        fontsize=7.5,
        color="#444444",
    )
    plt.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)

    out_png = FIGS / "fig_4_4_1_jaccard_heatmap_v1.png"
    out_pdf = FIGS / "fig_4_4_1_jaccard_heatmap_v1.pdf"
    fig.savefig(out_png, bbox_inches="tight", dpi=300)
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"WROTE {out_png}")
    print(f"WROTE {out_pdf}")


if __name__ == "__main__":
    main()
