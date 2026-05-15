"""Build v11.9 docx from the v11.9 markdown source.

Differs from `export_v11_8_to_docx.py` in two ways:

  1. Source markdown is `docs/beyond_recall_v11_9_5_draft.md`. The v11.9 source
     contains figures as inline `![caption](path)` embeds at their canonical
     positions (Figure 4.1 already moved into §4.1 above the gradient claim,
     etc.), so this script does NOT use a FIGURE_MAP injection pass — pandoc
     resolves the inline references directly via the resource path.

  2. After pandoc conversion, the docx is post-processed by
     `post_process_v11_8_docx_20260508.py` to apply per-subject row shading
     (band-by-C5-baseline-value, since v11.9 dropped the explicit Band column).

The pre-pandoc passes still applied here, carried over from the v11.8 builder:

  - Numbered headings receive explicit `{#sec-x-y}` anchor ids.
  - In-prose `§X.Y` cross-refs are rewritten to clickable markdown links.
  - Long parentheticals (>15 words, non-citation, non-statistic) are rewritten
    to pandoc footnote syntax.
  - The Appendix D.4 per-judge score-matrix range is wrapped in landscape
    sectPr paragraphs.

Output: `docs/beyond_recall_v11_9_5_draft.docx`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pypandoc

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "docs" / "beyond_recall_v11_9_5_draft.md"
FIGS = REPO / "figures"
OUT_MD = REPO / "docs" / "beyond_recall_v11_9_5_draft.clean.md"
OUT_DOCX = REPO / "docs" / "beyond_recall_v11_9_5_draft.docx"
POST_PROCESS = REPO / "scripts" / "post_process_v11_8_docx_20260508.py"


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

LANDSCAPE_SECTIONS = [
    ("### D.4 Per-judge score matrices", "### D.5 "),
]


HEADING_LINE_RE = re.compile(
    r"^(?P<hashes>#{2,4})\s+(?P<num>(?:[A-E]|\d+)(?:\.\d+){0,3})\s+(?P<title>.+?)\s*$"
)
SECTION_REF_RE = re.compile(r"§(?P<ref>(?:[A-E]|\d+)(?:\.\d+)+)")
PAREN_RE = re.compile(r"\(([^()\n]+)\)")


def section_anchor_id(section_num: str) -> str:
    return "sec-" + section_num.replace(".", "-").lower()


def build_heading_anchor_map(lines):
    anchors = {}
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_LINE_RE.match(line)
        if not match:
            continue
        anchors[match.group("num")] = section_anchor_id(match.group("num"))
    return anchors


def inject_heading_anchors(lines, anchors):
    out = []
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line); continue
        if in_code:
            out.append(line); continue
        match = HEADING_LINE_RE.match(line)
        if not match:
            out.append(line); continue
        num = match.group("num")
        if num not in anchors:
            out.append(line); continue
        if re.search(r"\{#[^}]+\}\s*$", line):
            out.append(line); continue
        out.append(f"{line.rstrip()} {{#{anchors[num]}}}")
    return out


def iter_outside_code_and_links(line):
    pattern = re.compile(
        r"(`[^`\n]*`|!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*\)|<[^>]+>)"
    )
    pos = 0
    for match in pattern.finditer(line):
        if match.start() > pos:
            yield line[pos:match.start()], True
        yield match.group(0), False
        pos = match.end()
    if pos < len(line):
        yield line[pos:], True


def rewrite_section_refs(lines, anchors):
    out = []
    n_links = 0
    unresolved = set()
    in_code = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line); continue
        if in_code:
            out.append(line); continue
        if HEADING_LINE_RE.match(line):
            out.append(line); continue
        if stripped.startswith("|"):
            out.append(line); continue
        if stripped.startswith("!["):
            out.append(line); continue
        rebuilt = []
        for chunk, replaceable in iter_outside_code_and_links(line):
            if not replaceable:
                rebuilt.append(chunk); continue

            def _sub(match):
                nonlocal n_links
                ref = match.group("ref")
                if ref in anchors:
                    n_links += 1
                    return f"[§{ref}](#{anchors[ref]})"
                unresolved.add(ref)
                return match.group(0)
            rebuilt.append(SECTION_REF_RE.sub(_sub, chunk))
        out.append("".join(rebuilt))
    return out, n_links, unresolved


_FOOTNOTE_EXCLUDE_SUBSTRINGS = (
    "arXiv:", " et al.", "et al.,", "et seq.",
    "Fig.", "Fig ", "Figure ", "Table ", "p. ", "pp. ",
    "R²", "R^2", "Δ", "δ", "e.g.,", "i.e.,", "cf.",
    ".py", ".md", ".json", ".ipynb",
    "scripts/", "docs/", "results/", "figures/", "data/", "memory-study-repo/",
)
_FOOTNOTE_EXCLUDE_PATTERNS = (
    re.compile(r"^\s*\d{4}(?:-\d{2}-\d{2})?\s*$"),
    re.compile(r"\b\d{4}\b[,;\s]"),
    re.compile(r"\br\s*=\s*[-−]?\d"),
    re.compile(r"\bp\s*[<=]\s*\d"),
    re.compile(r"\bn\s*=\s*\d"),
    re.compile(r"\bN\s*=\s*\d"),
    re.compile(r"\bmean\s+[A-Za-z0-9]+\s*="),
    re.compile(r"\b[a-zA-Z]+\s*=\s*[-−]?\d"),
    re.compile(r"\bC\d+[a-z]?\b"),
    re.compile(r"^[\s-]*[-−]?\d+\.\d+"),
    re.compile(r"\$[^$]*\$"),
    re.compile(r"§"),
    re.compile(r"\\\\"),
)
_FOOTNOTE_MIN_WORDS = 16


def _paren_excluded(content):
    for marker in _FOOTNOTE_EXCLUDE_SUBSTRINGS:
        if marker in content:
            return True
    for pat in _FOOTNOTE_EXCLUDE_PATTERNS:
        if pat.search(content):
            return True
    return False


def rewrite_footnotes(lines):
    out = []
    footnote_defs = []
    previews = []
    in_code = False
    counter = 0
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code = not in_code
            out.append(line); continue
        if in_code:
            out.append(line); continue
        if HEADING_LINE_RE.match(line):
            out.append(line); continue
        if stripped.startswith("|"):
            out.append(line); continue
        if stripped.startswith("!["):
            out.append(line); continue
        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 300:
            out.append(line); continue

        rebuilt_parts = []
        for chunk, replaceable in iter_outside_code_and_links(line):
            if not replaceable:
                rebuilt_parts.append(chunk); continue
            new_chunk_parts = []
            pos = 0
            for match in PAREN_RE.finditer(chunk):
                new_chunk_parts.append(chunk[pos:match.start()])
                content = match.group(1).strip()
                wc = len(content.split())
                if wc < _FOOTNOTE_MIN_WORDS or _paren_excluded(content):
                    new_chunk_parts.append(match.group(0))
                else:
                    counter += 1
                    marker = f"[^fn{counter}]"
                    new_chunk_parts.append(marker)
                    footnote_defs.append(f"[^fn{counter}]: {content}")
                    previews.append(content[:160])
                pos = match.end()
            new_chunk_parts.append(chunk[pos:])
            rebuilt_parts.append("".join(new_chunk_parts))
        out.append("".join(rebuilt_parts))
    return out, footnote_defs, previews


def build_clean_markdown():
    text = MD.read_text(encoding="utf-8")
    abs_figs = FIGS.resolve().as_posix()
    text = text.replace("../figures/", abs_figs + "/")
    lines = text.split("\n")
    while lines and lines[0].strip() == "":
        lines = lines[1:]

    anchors = build_heading_anchor_map(lines)
    lines = inject_heading_anchors(lines, anchors)
    lines, n_section_links, unresolved_refs = rewrite_section_refs(lines, anchors)
    lines, footnote_defs, footnote_previews = rewrite_footnotes(lines)

    if footnote_defs:
        if lines and lines[-1].strip() != "":
            lines.append("")
        for fdef in footnote_defs:
            lines.append(fdef)
            lines.append("")

    # Landscape wrapping for D.4 per-judge score matrices.
    final_lines = []
    k = 0
    landscape_pairs = list(LANDSCAPE_SECTIONS)
    injected = []
    while k < len(lines):
        line = lines[k]
        start_match = next(
            (pair for pair in landscape_pairs if line.startswith(pair[0])), None
        )
        if start_match:
            final_lines.append("")
            final_lines.append(PORTRAIT_SECTPR)
            final_lines.append("")
            final_lines.append(line)
            k += 1
            end_prefix = start_match[1]
            while k < len(lines) and not lines[k].startswith(end_prefix):
                final_lines.append(lines[k])
                k += 1
            final_lines.append("")
            final_lines.append(LANDSCAPE_SECTPR)
            final_lines.append("")
            injected.append(start_match[0])
            continue
        final_lines.append(line)
        k += 1

    stats = {
        "section_links": n_section_links,
        "unresolved_refs": sorted(unresolved_refs),
        "footnote_count": len(footnote_defs),
        "anchors_built": len(anchors),
        "landscape_wrappers": injected,
    }
    return "\n".join(final_lines), stats


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
        help="Build cleaned markdown only; skip pandoc + post-process.")
    parser.add_argument("--skip-post-process", action="store_true",
        help="Skip the table-row-shading post-process step.")
    args = parser.parse_args()

    cleaned, stats = build_clean_markdown()
    OUT_MD.write_text(cleaned, encoding="utf-8")
    print(f"Intermediate markdown: {OUT_MD}")
    print(f"  anchors indexed: {stats['anchors_built']}")
    print(f"  section hyperlinks: {stats['section_links']}")
    print(f"  footnotes created from parentheticals: {stats['footnote_count']}")
    if stats["unresolved_refs"]:
        print(f"  unresolved §refs: {len(stats['unresolved_refs'])} (first 10: {stats['unresolved_refs'][:10]})")
    if stats["landscape_wrappers"]:
        for s in stats["landscape_wrappers"]:
            print(f"  landscape wrapper around: {s[:70]}")

    if args.dry_run:
        print("\n(dry-run) skipping pandoc and post-process.")
        return 0

    if OUT_DOCX.exists():
        try:
            OUT_DOCX.unlink()
            print(f"Removed prior docx: {OUT_DOCX}")
        except PermissionError:
            print(f"WARNING: {OUT_DOCX} is locked (Word open?). Will write to .NEW path.")

    reference_docx = REPO / "docs" / "_reference_arxiv_11pt.docx"
    target = OUT_DOCX if not OUT_DOCX.exists() else OUT_DOCX.with_suffix(".docx.NEW")

    pypandoc.convert_file(
        str(OUT_MD),
        "docx",
        outputfile=str(target),
        extra_args=[
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--resource-path=" + str(REPO),
            "--reference-doc=" + str(reference_docx) if reference_docx.exists() else "--standalone",
        ] if reference_docx.exists() else [
            "--standalone", "--toc", "--toc-depth=3",
            "--resource-path=" + str(REPO),
        ],
    )
    size_kb = target.stat().st_size / 1024
    print(f"Wrote: {target}  ({size_kb:.0f} KB)")

    if args.skip_post_process:
        print("(--skip-post-process) skipping table shading.")
        return 0

    if not POST_PROCESS.exists():
        print(f"NOTE: post-process script not found at {POST_PROCESS}; skipping.")
        return 0

    print("\nRunning post-process (figure reorder no-op + table shading)...")
    rc = subprocess.call([sys.executable, str(POST_PROCESS), str(target), str(target)])
    print(f"post-process exit: {rc}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
