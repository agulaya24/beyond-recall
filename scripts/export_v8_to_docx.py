"""Export v8 paper draft to .docx for Aarik's author review.

Differences from export_v7_to_docx.py:
- Targets docs/beyond_recall_v8_draft.md (body complete through §8; abstract
  intentionally not yet written).
- Strips the v7/v6 editorial scaffolding lines at the top (lines 11-12 of source).
- Keeps the final "*Paper body complete. Abstract to be written last.*" line
  because it communicates the draft state to the reviewer.
- FIGURE_MAP updated for v8 section anchors (not v7 bold-label anchors, which
  shifted wording between drafts). Figures are anchored to H3 headings when
  possible for stability; one figure (fig_4_2_1) is already inline in v8 at
  line 835 and is NOT re-inserted.
- Output: docs/beyond_recall_v8_draft.docx
"""

from pathlib import Path
import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v8_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_v8_draft.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v8_draft.docx"

# Each entry: (line-starts-with anchor, png filename, caption).
# Anchored to H3 headings (stable across drafts). Each anchor fires once.
# Note: fig_4_2_1_question_improvement_rates is already inline in the source
# at line ~835, so we do NOT include it here.
FIGURE_MAP = [
    ("### 4.1 The Cross-Subject Gradient", "fig_4_1_gradient_scatter.png",
     "Figure 4.1: Per-subject baseline (C5) vs. facts+spec (C4a) across all 14 subjects with regression line. The gradient result."),
    ("### 4.2 Compression: Structure vs. Raw Text", "fig_4_2_compression.png",
     "Figure 4.2: Log-tokens vs. normalized prediction score (Hamerton). A 7,300-token specification outperforms the 34,168-token raw corpus."),
    ("### 4.3 Mechanism: Content, Not Format", "fig6_wrong_spec_control.png",
     "Figure 6: Correct-spec vs. wrong-spec score per subject. Wrong-spec lands near baseline; a deterministic maximum-distance pairing lands below baseline."),
    ("### 4.3 Mechanism: Content, Not Format", "fig4_hedging_reduction.png",
     "Figure 4: Hedging/refusal rate drops 28.8% → 1.4% → 0.0% across C5 → C2a → C4a under the narrow starts_refusal classifier."),
    ("### 4.4 Memory-System Composition", "fig7_memory_systems.png",
     "Figure 7: Per-system spec delta (C3 − C1) across low-baseline subjects. The specification layers additively on three of four commercial memory systems."),
    ("### 4.4 Memory-System Composition", "fig3_retrieval_disagreement.png",
     "Figure 3: Top-k retrieval disagreement across embedding-based memory systems given an identical fact pool."),
    ("### 4.5.1 Cross-provider response generation", "fig11_tier2_replication.png",
     "Figure 11: Tier 2 cross-provider replication — 5 of 6 (subject × response model) cells reproduce the specification direction."),
    ("### 4.7 Architectural Convergence: Letta Stateful-Agent", "fig10_letta_scaling.png",
     "Figure 10: Letta self-editing memory block size vs. source corpus size vs. Base Layer's flat compose ceiling. Duplication share at scale."),
    ("### 3.7.4 Inter-Judge Agreement", "fig8_judge_agreement.png",
     "Figure 8: Pairwise Spearman agreement across the 7-judge panel; the 5-judge primary aggregate agrees at ρ = 0.89-0.98."),
    ("### 3.2.1 Pretraining-coverage variance", "fig9_cultural_baseline.png",
     "Figure 9: Baseline score (C5) by subject culture and era, motivating the low-baseline slice."),
    ("## 4. Results", "fig5_condition_effects.png",
     "Figure 5: Condition-by-condition mean deltas across subjects (low-baseline slice, 5-judge primary)."),
]


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    # Rewrite the inline relative figure reference (`../figures/foo.png`) that
    # already exists in the source so pandoc can resolve it regardless of CWD.
    # We do NOT edit the source markdown; this rewrite is in-memory only.
    abs_figs = FIGS.resolve().as_posix()
    text = text.replace("../figures/", abs_figs + "/")
    lines = text.split("\n")

    # Strip the editorial v7/v6 scaffolding lines.
    # v8 source lines 11-12 read:
    #   *v7 working draft -- appended section by section as each locks in review.*
    #   *v6 (`beyond_recall_v6_draft.md`) remains the reference source for sections not yet re-locked.*
    # And they are wrapped by `---` horizontal rules on lines 9 and 14.
    cleaned = []
    skip_block = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Drop the "v7 working draft" line and the "v6 remains the reference source" line.
        if stripped.startswith("*v7 working draft"):
            continue
        if stripped.startswith("*v6 (`beyond_recall_v6_draft.md`)"):
            continue
        cleaned.append(line)
    lines = cleaned

    # Collapse three-consecutive-horizontal-rules or empty paragraphs left behind
    # by stripping (best-effort; pandoc handles extra blank lines fine).
    # We do NOT strip the two `---` lines around the removed block -- they just
    # become a single `---` separator, which is harmless and preserves visual structure.

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

    return "\n".join(out_lines), used


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
