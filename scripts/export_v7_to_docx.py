"""Export v7 paper draft (partial) to .docx for Aarik's review.

Differences from export_to_docx.py:
- Targets docs/beyond_recall_v7_draft.md (partially complete: §1 + §2 locked)
- Anchors figures under §1.3 bold-label paragraphs so figures show up in
  the review doc even though §3, §4, §5 sections are not yet drafted.
- No editorial HTML comment block to strip (v7 doesn't have one).
- Output: docs/beyond_recall_v7_review.docx
"""

from pathlib import Path
import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v7_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_v7_review.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v7_review.docx"

# Each entry: (line-starts-with anchor, png filename, caption)
# §1.3 bold-label anchors and §4/§5 anchors both supported. Whichever matches first in the file wins.
FIGURE_MAP = [
    # §1.3 finding anchors (for v7 review)
    ("**Primary result: the gradient.**", "fig1_global_gradient.png",
     "Figure 1: Per-subject C5 baseline vs. C4a (facts+spec) across all 14 subjects. The gradient result."),
    ("**Compression: structure beats raw source at a fraction of the context.**", "fig2_compression_curve.png",
     "Figure 2: Log-tokens vs. normalized prediction score (Hamerton). 7,300-token spec beats 34,168-token corpus."),
    ("**Mechanism: content, not format.**", "fig6_wrong_spec_control.png",
     "Figure 6: Correct-spec vs. wrong-spec score per subject. Wrong-spec lands near baseline."),
    ("**Mechanism: content, not format.**", "fig4_hedging_reduction.png",
     "Figure 4: Hedging/refusal rate drops 28.8% → 1.4% → 0.0% across C5 → C2a → C4a (starts_refusal classifier)."),
    ("**Additivity: the specification layers on three of four commercial memory systems.**", "fig7_memory_systems.png",
     "Figure 7: Per-system spec delta (C3 − C1) across low-baseline subjects."),
    ("**Robustness: the effect is not an artifact of Claude talking to Claude.**", "fig11_tier2_replication.png",
     "Figure 11: Tier 2 cross-provider replication — 5 of 6 (subject × response model) cells positive."),
    ("**Architectural observation: Letta's stateful-agent path.**", "fig10_letta_scaling.png",
     "Figure 10: Letta block size vs. corpus size (vs. Base Layer flat line); duplication % at scale."),
    # §4/§5 anchors kept in case v7 grows; harmless if those sections absent
    ("### 4.1 The Cross-Subject Gradient", "fig1_global_gradient.png",
     "Figure 1 (duplicate in §4.1 if present)."),
    ("### 4.2 Compression", "fig2_compression_curve.png",
     "Figure 2 (duplicate in §4.2 if present)."),
    ("### 4.3 Memory Systems", "fig7_memory_systems.png",
     "Figure 7 (duplicate in §4.3 if present)."),
]


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    lines = text.split("\n")

    # v7 does not have an editorial HTML comment block. No strip needed.
    # Drop leading blank lines.
    while lines and lines[0].strip() == "":
        lines = lines[1:]

    out_lines = []
    used = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        out_lines.append(line)
        matches = []
        for prefix, png, caption in FIGURE_MAP:
            key = (prefix, png)
            if key in used:
                continue
            if line.startswith(prefix):
                matches.append((prefix, png, caption))
        if matches:
            for prefix, png, caption in matches:
                used.add((prefix, png))
            # Walk forward to a blank line, then insert figures.
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                out_lines.append(lines[j])
                j += 1
            out_lines.append("")
            for prefix, png, caption in matches:
                img_path = (FIGS / png).resolve().as_posix()
                out_lines.append(f"![{caption}]({img_path})")
                out_lines.append("")
                out_lines.append(f"*{caption}*")
                out_lines.append("")
            i = j
        i += 1

    return "\n".join(out_lines), used


def main():
    cleaned, used = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")
    print(f"Figures inserted: {len(used)}")
    for prefix, png in used:
        print(f"  - {png} under anchor: {prefix[:60]}")

    pypandoc.convert_file(
        str(OUT_MD),
        "docx",
        outputfile=str(OUT_DOCX),
        extra_args=[
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--resource-path=" + str(REPO),
        ],
    )
    size_kb = OUT_DOCX.stat().st_size / 1024
    print(f"Wrote: {OUT_DOCX}  ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
