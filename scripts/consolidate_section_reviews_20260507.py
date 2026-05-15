"""Consolidate the 8 (or 9) v11.8 section walkthrough review markdown files
into a single combined markdown with TOC, then convert to .docx via pypandoc.

Output:
  docs/reviews/v11_8_consolidated_section_reviews_20260507.md
  docs/reviews/v11_8_consolidated_section_reviews_20260507.docx

If pypandoc fails, the consolidated .md is still written.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pypandoc

REPO = Path(__file__).resolve().parent.parent
REVIEWS_DIR = REPO / "docs" / "reviews"

# Order matches paper structure: §1-2, §3, §4, §5, §6-7, App AB, App CDE,
# App FGH, then figures (if generated in time).
INPUT_FILES = [
    ("Sections 1 & 2 (Introduction, Prior Work)",
     "section1_2_walkthrough_review_20260507.md"),
    ("Section 3 (Methods)",
     "section3_walkthrough_review_20260507.md"),
    ("Section 4 (Results)",
     "section4_walkthrough_review_20260507.md"),
    ("Section 5 (Discussion)",
     "section5_walkthrough_review_20260507.md"),
    ("Sections 6 & 7 (Limitations, Future Work)",
     "section6_7_walkthrough_review_20260507.md"),
    ("Appendices A & B",
     "appendices_AB_walkthrough_review_20260507.md"),
    ("Appendices C, D, E",
     "appendices_CDE_walkthrough_review_20260507.md"),
    ("Appendices F, G, H",
     "appendices_FGH_walkthrough_review_20260507.md"),
    ("Figures",
     "figures_walkthrough_review_20260507.md"),
]

OUT_MD = REVIEWS_DIR / "v11_8_consolidated_section_reviews_20260507.md"
OUT_DOCX = REVIEWS_DIR / "v11_8_consolidated_section_reviews_20260507.docx"


def main() -> int:
    present: list[tuple[str, Path]] = []
    missing: list[str] = []
    for label, fname in INPUT_FILES:
        p = REVIEWS_DIR / fname
        if p.exists():
            present.append((label, p))
        else:
            missing.append(fname)

    print(f"Found {len(present)} review files; missing {len(missing)}.")
    for label, p in present:
        size_kb = p.stat().st_size / 1024
        print(f"  + {label}: {p.name} ({size_kb:.1f} KB)")
    for fname in missing:
        print(f"  - MISSING: {fname}")

    # Build slug-style anchor ids per review so the TOC links resolve.
    def slug(label: str) -> str:
        out_chars = []
        for ch in label.lower():
            if ch.isalnum():
                out_chars.append(ch)
            elif ch in (" ", "-", "_", "&", ",", "(", ")"):
                out_chars.append("-")
        s = "".join(out_chars)
        while "--" in s:
            s = s.replace("--", "-")
        return s.strip("-")

    parts: list[str] = []

    parts.append("# v11.8 Consolidated Section Walkthrough Reviews")
    parts.append("")
    parts.append("**Date:** 2026-05-07  ")
    parts.append("**Paper:** Beyond Recall v11.8 draft  ")
    parts.append(f"**Reviews included:** {len(present)} of {len(INPUT_FILES)}")
    if missing:
        parts.append("")
        parts.append("**Not yet generated:**")
        for fname in missing:
            parts.append(f"- `{fname}`")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Table of Contents")
    parts.append("")
    for label, _p in present:
        anchor = slug(label)
        parts.append(f"- [{label}](#{anchor})")
    parts.append("")
    parts.append("---")
    parts.append("")

    for label, p in present:
        anchor = slug(label)
        parts.append("")
        parts.append("\\newpage")
        parts.append("")
        # Top-level review header. Uses an explicit anchor id so the TOC
        # links resolve even if pandoc's auto-slug differs from our slug().
        parts.append(f"# {label} {{#{anchor}}}")
        parts.append("")
        parts.append(f"*Source file: `{p.name}`*")
        parts.append("")
        # Read the file, demote its existing top-level H1 to H2 so we don't
        # have two competing H1s per review section.
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        demoted: list[str] = []
        first_h1_seen = False
        for line in lines:
            if not first_h1_seen and line.startswith("# ") and not line.startswith("## "):
                # The very first H1 in each file becomes a subordinate H2,
                # since the section label above already serves as the H1.
                demoted.append("## " + line[2:])
                first_h1_seen = True
            else:
                demoted.append(line)
        parts.append("\n".join(demoted))
        parts.append("")
        parts.append("---")
        parts.append("")

    combined = "\n".join(parts)
    OUT_MD.write_text(combined, encoding="utf-8")
    size_kb = OUT_MD.stat().st_size / 1024
    print(f"\nWrote consolidated markdown: {OUT_MD} ({size_kb:.1f} KB)")

    # Convert to docx. Use pandoc's own TOC on top of our manual one (the
    # manual one is for the markdown; pandoc's --toc produces the Word TOC
    # field). Tables in GFM markdown render natively in docx.
    try:
        if OUT_DOCX.exists():
            OUT_DOCX.unlink()
        pypandoc.convert_file(
            str(OUT_MD),
            "docx",
            outputfile=str(OUT_DOCX),
            extra_args=[
                "--standalone",
                "--toc",
                "--toc-depth=2",
                "--from=markdown+pipe_tables+tex_math_dollars",
            ],
        )
        size_kb = OUT_DOCX.stat().st_size / 1024
        print(f"Wrote docx: {OUT_DOCX} ({size_kb:.1f} KB)")
        return 0
    except Exception as exc:
        print(f"\npypandoc conversion FAILED: {exc}", file=sys.stderr)
        print(f"Markdown fallback is at: {OUT_MD}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
