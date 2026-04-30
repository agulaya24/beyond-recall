"""Export v11.5 locked-sections draft to .docx for Aarik's review.

Includes only sections walked and locked through 2026-04-29:
- Title block + frontmatter
- §1 Introduction (full)
- §2 Prior Work, Industry Benchmarks, The Fifth Target (full)
- §3 Study Design (full, including §3.1 through §3.7)
- §8 Data, code, and reproducibility (kept so §3.7 cross-ref resolves)
- §9 References (kept so all citations resolve)
- All Appendices (A through H)

Excludes §4-§7, which are still in active edit.
"""

from pathlib import Path
import pypandoc
import re

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v11_5_draft.md"
OUT_MD = REPO / "docs" / "beyond_recall_v11_5_locked_draft.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v11_5_locked_draft.docx"

# Section anchors. Lines are 1-indexed in the source markdown.
# Use heading-line patterns to locate boundaries dynamically (more robust than
# hardcoded line numbers in case the source shifts).
SECTION_PATTERNS = {
    "section_1_start": re.compile(r"^## 1\. Introduction"),
    "section_4_start": re.compile(r"^## 4\. Results"),
    "section_8_start": re.compile(r"^## 8\. Data, code"),
    "appendix_a_start": re.compile(r"^## Appendix A\."),
}


def find_line(lines, pattern):
    """Return 0-indexed line number of first match, or -1."""
    for i, line in enumerate(lines):
        if pattern.match(line):
            return i
    return -1


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    lines = text.split("\n")

    s1 = find_line(lines, SECTION_PATTERNS["section_1_start"])
    s4 = find_line(lines, SECTION_PATTERNS["section_4_start"])
    s8 = find_line(lines, SECTION_PATTERNS["section_8_start"])
    sA = find_line(lines, SECTION_PATTERNS["appendix_a_start"])

    if -1 in (s1, s4, s8, sA):
        raise RuntimeError(
            f"Missing section anchor: §1={s1}, §4={s4}, §8={s8}, AppA={sA}"
        )

    # Build the locked draft.
    # 1. Title + frontmatter (lines 0 to s1, exclusive of s1)
    # 2. Banner indicating locked-sections-only state
    # 3. §1 + §2 + §3 (lines s1 to s4, exclusive of s4)
    # 4. §8 + §9 (lines s8 to sA, exclusive of sA)
    # 5. Appendix A through end (lines sA to end)

    banner = [
        "",
        "> **v11.5 LOCKED-SECTIONS DRAFT.** This document contains only the "
        "sections walked and locked as of 2026-04-29. §1 through §3 are body "
        "sections; §8 (data and code) and §9 (references) are kept so cross-"
        "references resolve; Appendices A through H are included. §4 through "
        "§7 are in active edit and intentionally not included in this draft.",
        "",
    ]

    parts = []
    parts.extend(lines[:s1])
    parts.extend(banner)
    parts.extend(lines[s1:s4])
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("> **Note.** §4 (Results), §5 (Discussion), §6 (Limitations), "
                 "and §7 (Future Work) are omitted from this locked-sections "
                 "draft. Some cross-references in §1-§3 point into those "
                 "sections and will not resolve here; those are intentional "
                 "stand-ins until §4-§7 are walked and locked.")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.extend(lines[s8:sA])
    parts.extend(lines[sA:])

    return "\n".join(parts)


def main():
    cleaned = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")
    print(f"  line count: {len(cleaned.splitlines())}")

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
