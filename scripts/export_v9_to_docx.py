"""Export v9 paper draft to .docx with v2 figures swapped in.

Changes from export_v8_to_docx.py:
- Target: docs/beyond_recall_v9_draft.md (not v8)
- FIGURE_MAP updated for the v9 post-restructure tree:
    * §4.4 → §4.4.1 Aggregate Performance Across Systems
    * §4.5 is now Letta Stateful-Agent (was §4.7)
    * §4.6 is now Robustness and Sensitivity (was §4.5)
    * §4.6.1 is now Cross-provider Tier 2 replication (was §4.5.1)
    * §4.8 removed entirely (content moved to §5.5)
- v3 figures swapped in (publication polish, 2026-04-23):
    * fig_4_1_gradient_scatter_v3.png
    * fig_4_2_compression_v3.png
    * fig_4_2_1_question_improvement_rates_v3.png
    * fig5_condition_effects_v3.png
    * fig7_memory_systems_v3.png
- Figure 9 (cultural baseline) moved to appendix (injected under ## Appendix D)
- Figure 11 (Tier 2) dropped per author decision
- Note: fig_4_2_1_question_improvement_rates.png is already inline in v9 source at ~line 861
- Note: fig_4_2_1_v2 is the rebuild, but since v4_2_1 is inline, keep as-is for now
    (author can swap the inline path manually if desired)

Output: docs/beyond_recall_v9_draft.docx
"""

from pathlib import Path
import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v9_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_v9_draft.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v9_draft.docx"

# Each entry: (line-starts-with anchor, png filename, caption).
FIGURE_MAP = [
    ("### 4.1 The Cross-Subject Gradient", "fig_4_1_gradient_scatter_v3.png",
     "Figure 4.1: Per-subject baseline (C5) vs. facts+spec (C4a) across all 14 subjects with regression line. The gradient result."),
    ("### 4.2 Compression: Structure vs. Raw Text", "fig_4_2_compression_v3.png",
     "Figure 4.2: Hamerton compression story. A 7,300-token specification outperforms the 34,168-token raw corpus; both are lifted further by facts + spec or corpus + spec."),
    ("### 4.3 Mechanism: Content, Not Format", "fig6_wrong_spec_control.png",
     "Figure 6: Correct-spec vs. wrong-spec score per subject. Wrong-spec lands near baseline; a deterministic maximum-distance pairing lands below baseline."),
    ("### 4.3 Mechanism: Content, Not Format", "fig4_hedging_reduction.png",
     "Figure 4: Hedging/refusal rate drops 28.8% -> 1.4% -> 0.0% across C5 -> C2a -> C4a under the narrow starts_refusal classifier."),
    ("### 4.4.1 Aggregate Performance Across Systems", "fig7_memory_systems_v3.png",
     "Figure 7: Per-system spec delta (C3 - C1) across low-baseline subjects, grouped by memory system. Each system's subject-level spread is visible; Supermemory's per-subject spread reveals the mixture behind the near-zero aggregate."),
    ("### 4.4.1 Aggregate Performance Across Systems", "fig3_retrieval_disagreement.png",
     "Figure 3: Top-k retrieval disagreement across embedding-based memory systems given an identical fact pool."),
    ("### 4.5 Exploratory Case Study: Letta Stateful-Agent", "fig10_letta_scaling.png",
     "Figure 10: Letta self-editing memory block size vs. source corpus size vs. Base Layer's flat compose ceiling. Duplication share at scale."),
    ("### 3.7.4 Inter-Judge Agreement", "fig8_judge_agreement.png",
     "Figure 8: Pairwise Spearman agreement across the 7-judge panel; the 5-judge primary aggregate agrees at rho = 0.86-0.93."),
    ("## Appendix D.", "fig9_cultural_baseline.png",
     "Figure D.1 (moved from body): Baseline score (C5) by subject culture and era, motivating the low-baseline slice definition."),
    ("## 4. Results", "fig5_condition_effects_v3.png",
     "Figure 5: Condition-by-condition improvement rate across subjects (low-baseline slice, 5-judge primary). Shows % improved, % tied, % worsened per condition with mean delta overlay."),
]


LANDSCAPE_SECTPR = (
    '```{=openxml}\n'
    '<w:p><w:pPr><w:sectPr>'
    '<w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
    '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr></w:pPr></w:p>\n'
    '```'
)

PORTRAIT_SECTPR = (
    '```{=openxml}\n'
    '<w:p><w:pPr><w:sectPr>'
    '<w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="720" w:footer="720" w:gutter="0"/>'
    '<w:cols w:space="720"/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr></w:pPr></w:p>\n'
    '```'
)

# Sections to render in landscape orientation. Each entry is a (start_header,
# end_header) pair — the section starting at start_header renders in landscape;
# the paragraph at end_header reverts to portrait. Matching is exact-prefix.
LANDSCAPE_SECTIONS = [
    ("### D.4 Per-judge score matrices", "### D.5 "),
]


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    # Rewrite inline relative figure refs (`../figures/foo.png`) so pandoc can resolve.
    abs_figs = FIGS.resolve().as_posix()
    text = text.replace("../figures/", abs_figs + "/")
    # Swap Fig 4.2.1 inline reference to the v3 polished rendering without touching
    # the v9 paper body source.
    text = text.replace(
        "fig_4_2_1_question_improvement_rates.png",
        "fig_4_2_1_question_improvement_rates_v3.png",
    )
    lines = text.split("\n")

    # Drop leading blank lines
    while lines and lines[0].strip() == "":
        lines = lines[1:]

    # Insert figures at mapped anchors
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
            # Walk forward to the next blank line so the figure drops in
            # after the heading's lead paragraph, not cramming the heading.
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

    # Inject landscape section-break paragraphs around LANDSCAPE_SECTIONS.
    # Pandoc honors `{=openxml}` raw blocks in docx output; a sectPr paragraph
    # closes the section ending there with the specified page properties.
    # Pattern: portrait sectPr immediately BEFORE the landscape start (closes
    # prior portrait section), landscape sectPr immediately AFTER the last
    # paragraph of the landscape region (closes the landscape section).
    final_lines = []
    k = 0
    injected = []
    landscape_pairs = list(LANDSCAPE_SECTIONS)
    while k < len(out_lines):
        line = out_lines[k]
        # Check if this line starts a landscape section.
        start_match = next(
            (pair for pair in landscape_pairs if line.startswith(pair[0])), None
        )
        if start_match:
            # Close previous portrait section BEFORE the landscape heading.
            final_lines.append("")
            final_lines.append(PORTRAIT_SECTPR)
            final_lines.append("")
            final_lines.append(line)
            k += 1
            end_prefix = start_match[1]
            # Consume lines until we hit the end prefix.
            while k < len(out_lines) and not out_lines[k].startswith(end_prefix):
                final_lines.append(out_lines[k])
                k += 1
            # Close the landscape section BEFORE the end heading (so the
            # landscape section ends with its own sectPr paragraph).
            final_lines.append("")
            final_lines.append(LANDSCAPE_SECTPR)
            final_lines.append("")
            injected.append(start_match[0])
            continue
        final_lines.append(line)
        k += 1

    if injected:
        for start in injected:
            print(f"  + landscape wrapper around: {start[:70]}")

    return "\n".join(final_lines), used


def main():
    cleaned, used = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")
    print(f"Figures inserted: {len(used)} / {len(FIGURE_MAP)}")
    for prefix, png in sorted(used):
        print(f"  + {png}  @  {prefix[:70]}")
    unmatched = [(p, f) for (p, f, _) in FIGURE_MAP if (p, f) not in used]
    if unmatched:
        print("Unmatched anchors (no figure inserted):")
        for prefix, png in unmatched:
            print(f"  - {png}  @  {prefix[:70]}")

    if OUT_DOCX.exists():
        OUT_DOCX.unlink()
        print(f"Removed prior docx: {OUT_DOCX}")

    reference_docx = REPO / "docs" / "_reference_arxiv_11pt.docx"
    pypandoc.convert_file(
        str(OUT_MD),
        "docx",
        outputfile=str(OUT_DOCX),
        extra_args=[
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--resource-path=" + str(REPO),
            "--reference-doc=" + str(reference_docx),
        ],
    )
    size_kb = OUT_DOCX.stat().st_size / 1024
    print(f"Wrote: {OUT_DOCX}  ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
