"""Build side-by-side HTML of Beyond Recall paper with figures embedded at section anchors.

Output: docs/beyond_recall_review.html (open in any browser; print to PDF if desired).
"""

from pathlib import Path
import re
import markdown

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v6_draft.md"
FIGS = REPO / "figures"
OUT = REPO / "docs" / "beyond_recall_review.html"

FIGURE_MAP = [
    ("### 3.7", "fig8_judge_agreement.png",
     "Figure 8: Inter-judge agreement across the non-Gemini judge panel."),
    ("## 4. Results", "fig5_condition_effects.png",
     "Figure 5: Condition-by-condition mean deltas across subjects. Orientation view."),
    ("### 4.1 The Cross-Subject Gradient", "fig1_global_gradient.png",
     "Figure 1: Per-subject C5 baseline vs. C4a (facts+spec) across all 14 subjects, ordered by baseline. The gradient result."),
    ("### 4.1.3", "fig9_cultural_baseline.png",
     "Figure 9: Baseline score by subject culture. Addresses whether the gradient is confounded by corpus difficulty vs. pretraining density."),
    ("### 4.2 Compression", "fig2_compression_curve.png",
     "Figure 2: Log-tokens vs. normalized prediction score (Hamerton). ~5K-token spec outperforms 34K-token raw corpus."),
    ("### 4.3 Memory Systems", "fig7_memory_systems.png",
     "Figure 7: Per-system spec delta (C3 − C1) for Mem0, Letta, Supermemory, Zep, and Base Layer on the 9 low-baseline subjects."),
    ("### 4.3 Memory Systems", "fig3_retrieval_disagreement.png",
     "Figure 3: Top-k retrieval disagreement across the three embedding-based memory systems. 93% at top-1, 53% at top-10."),
    ("### 4.5 The Wrong-Spec", "fig6_wrong_spec_control.png",
     "Figure 6: Correct-spec vs. wrong-spec (random derangement) score per subject. Wrong-spec lands near baseline."),
    ("### 5.5 When to Use", "fig4_hedging_reduction.png",
     "Figure 4: Hedging/refusal rate across C5 → C2a → C4a. 25.0% baseline → 2.6% spec → 0.6% facts+spec."),
]

def build():
    md_text = MD.read_text(encoding="utf-8")

    # Insert figure markers after the first heading-match for each figure.
    # A heading line is "### X ..." or "## X ...".
    # Strategy: walk line-by-line; on first line starting with the heading prefix, queue a figure insertion
    # to appear after the first blank line that follows (i.e., after the heading text line itself).

    lines = md_text.split("\n")
    used_prefixes = set()
    out_lines = []
    pending = []  # list of (figpath, caption) to insert at next blank line

    def figure_for(line):
        hits = []
        for prefix, png, caption in FIGURE_MAP:
            key = (prefix, png)
            if key in used_prefixes:
                continue
            if line.startswith(prefix):
                hits.append((prefix, png, caption))
        return hits

    for line in lines:
        out_lines.append(line)
        matches = figure_for(line)
        for prefix, png, caption in matches:
            used_prefixes.add((prefix, png))
            pending.append((png, caption))
        # insert pending figures after a blank line following the heading
        if pending and line.strip() == "" and len(out_lines) > 1 and out_lines[-2].startswith(("#", "|", "-", "*", ">")) is False:
            # simple rule: after any blank line that follows at least one non-heading paragraph since the heading
            # but for simplicity just flush on first blank line
            pass

    # Simpler: rewrite — walk and insert figure block immediately after heading line + one blank
    out_lines = []
    used_prefixes = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        out_lines.append(line)
        matches = []
        for prefix, png, caption in FIGURE_MAP:
            key = (prefix, png)
            if key in used_prefixes:
                continue
            if line.startswith(prefix):
                matches.append((prefix, png, caption))
        if matches:
            for prefix, png, caption in matches:
                used_prefixes.add((prefix, png))
            # walk forward to one blank line, then insert figure block
            j = i + 1
            while j < len(lines) and lines[j].strip() != "":
                out_lines.append(lines[j])
                j += 1
            out_lines.append("")  # keep the blank
            for prefix, png, caption in matches:
                rel = (FIGS / png).resolve().as_posix()
                out_lines.append(f'<figure class="paperfig">')
                out_lines.append(f'  <img src="file:///{rel}" alt="{png}" />')
                out_lines.append(f'  <figcaption>{caption}</figcaption>')
                out_lines.append(f'</figure>')
                out_lines.append("")
            i = j
        i += 1

    md_with_figs = "\n".join(out_lines)

    html_body = markdown.markdown(
        md_with_figs,
        extensions=["tables", "fenced_code", "toc"],
    )

    css = """
    body { font-family: Georgia, 'Times New Roman', serif; max-width: 980px; margin: 2em auto; padding: 0 2em;
           line-height: 1.55; color: #1a1a1a; background: #fafaf7; }
    h1, h2, h3, h4 { font-family: -apple-system, 'Segoe UI', sans-serif; color: #111; line-height: 1.2; }
    h1 { border-bottom: 2px solid #333; padding-bottom: 0.3em; }
    h2 { margin-top: 2em; border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
    h3 { margin-top: 1.8em; color: #333; }
    h4 { margin-top: 1.4em; color: #444; }
    p { margin: 0.8em 0; }
    blockquote { border-left: 3px solid #888; margin: 1em 0; padding: 0.2em 1em; background: #f0eee8; color: #333; }
    code { background: #eee; padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.92em; }
    pre { background: #222; color: #eee; padding: 1em; overflow-x: auto; border-radius: 4px; }
    pre code { background: transparent; color: inherit; padding: 0; }
    table { border-collapse: collapse; margin: 1em 0; font-size: 0.92em; }
    th, td { border: 1px solid #bbb; padding: 0.4em 0.7em; text-align: left; }
    th { background: #e8e6de; }
    tr:nth-child(even) td { background: #f5f3ec; }
    figure.paperfig { margin: 1.6em 0; padding: 1em; background: #fff; border: 1px solid #ccc; border-radius: 4px;
                      box-shadow: 0 1px 3px rgba(0,0,0,0.08); text-align: center; }
    figure.paperfig img { max-width: 100%; height: auto; border: 1px solid #eee; }
    figure.paperfig figcaption { font-family: -apple-system, 'Segoe UI', sans-serif; font-size: 0.9em;
                                 color: #555; margin-top: 0.6em; font-style: italic; }
    a { color: #1a5490; }
    hr { border: none; border-top: 1px solid #ccc; margin: 2em 0; }
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Beyond Recall — v6 draft with figures (review build)</title>
  <style>{css}</style>
</head>
<body>
<p style="background:#fff3d9; padding:0.8em 1em; border:1px solid #d4b886; border-radius:4px; font-family:-apple-system,'Segoe UI',sans-serif; font-size:0.9em;">
<strong>S114 review build.</strong> Figures embedded at mapped sections per <code>figures/README.md</code>.
Source: <code>docs/beyond_recall_v6_draft.md</code>. To export as PDF, print from your browser (Ctrl-P → Save as PDF).
</p>
{html_body}
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote: {OUT}")
    print(f"Figures inserted: {len(used_prefixes)} / {len(FIGURE_MAP)}")
    if len(used_prefixes) < len(FIGURE_MAP):
        missing = [(p, f) for p, f, _ in FIGURE_MAP if (p, f) not in used_prefixes]
        print(f"Missing: {missing}")

if __name__ == "__main__":
    build()
