"""Export Beyond Recall paper draft to .docx for Word-based review.

- Strips the editorial HTML comment block (L1-197) that will not be published.
- Inserts figure references at section anchors per figures/README.md.
- Converts via bundled pandoc (pypandoc_binary).
- Output: docs/beyond_recall_review.docx
"""

from pathlib import Path
import re
import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v6_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_review.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_review.docx"

FIGURE_MAP = [
    ("### 3.7", "fig8_judge_agreement.png",
     "Figure 8: Inter-judge agreement across the non-Gemini judge panel."),
    ("## 4. Results", "fig5_condition_effects.png",
     "Figure 5: Condition-by-condition mean deltas across subjects."),
    ("### 4.1 The Cross-Subject Gradient", "fig1_global_gradient.png",
     "Figure 1: Per-subject C5 baseline vs. C4a (facts+spec) across all 14 subjects."),
    ("### 4.1.3", "fig9_cultural_baseline.png",
     "Figure 9: Baseline score by subject culture."),
    ("### 4.2 Compression", "fig2_compression_curve.png",
     "Figure 2: Log-tokens vs. normalized prediction score (Hamerton)."),
    ("### 4.3 Memory Systems", "fig7_memory_systems.png",
     "Figure 7: Per-system spec delta (C3 − C1) on 9 low-baseline subjects."),
    ("### 4.3 Memory Systems", "fig3_retrieval_disagreement.png",
     "Figure 3: Top-k retrieval disagreement across embedding-based memory systems."),
    ("### 4.5 The Wrong-Spec", "fig6_wrong_spec_control.png",
     "Figure 6: Correct-spec vs. wrong-spec score per subject."),
    ("### 5.5 When to Use", "fig4_hedging_reduction.png",
     "Figure 4: Hedging/refusal rate across C5 → C2a → C4a."),
]


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    lines = text.split("\n")
    # Drop the editorial HTML comment block
    start = None
    end = None
    for i, l in enumerate(lines):
        if start is None and l.strip().startswith("<!--"):
            start = i
        if start is not None and l.strip() == "-->":
            end = i
            break
    if start is not None and end is not None:
        lines = lines[end + 1:]
    # Drop leading blank lines
    while lines and lines[0].strip() == "":
        lines = lines[1:]

    # Insert figure markdown after mapped headings
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

    return "\n".join(out_lines)


def main():
    cleaned = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")

    # Convert to .docx
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
