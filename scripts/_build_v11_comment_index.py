"""Parse v11_comments_extracted_20260427.md into a structured JSON index.

Run:
    python scripts/_build_v11_comment_index.py

Writes:
    docs/reviews/v11_comment_index.json
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Repo-relative paths (resolved from this file's location).
REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "docs" / "reviews" / "v11_comments_extracted_20260427.md"
OUT = REPO_ROOT / "docs" / "reviews" / "v11_comment_index.json"


THEME_RULES = {
    "layman": ["layman", "plain language", "in plain", "more direct"],
    "footnote": ["footnote", "foot note", "should be a foot", "may need to be a foot"],
    "restructure": [
        "rework",
        "restructure",
        "rolled into",
        "wrapped into",
        "should be the headline",
    ],
    "length": [
        "shorten",
        "too long",
        "too many words",
        "exceptionally long",
        "cut by",
    ],
    "figure_walkthrough": [
        "describe this",
        "walk",
        "explain visually",
        "describe the axes",
    ],
    "linking": ["linked", "link to", "needs to be linked"],
    "color_code": ["color cod", "highlight"],
    "anchor_crossing": [
        "anchor",
        "category",
        "movement across",
        "1 to 2",
        "1 to 3",
        "2 to 5",
        "movement across an anchor",
    ],
    "reorder": [
        "should come before",
        "earlier",
        "buried",
        "move",
        "later section",
    ],
    "gradient_emphasis": ["gradient", "uniform quality"],
}


def derive_themes(body: str) -> list[str]:
    if not body:
        return []
    lower = body.lower()
    matched = []
    for theme, keywords in THEME_RULES.items():
        for kw in keywords:
            if kw in lower:
                matched.append(theme)
                break
    return matched


def parse_status(line: str) -> str:
    """Map status line text to a normalized status keyword."""
    text = line.lower()
    # Order matters: check the most specific first.
    if "pending review" in text:
        return "pending"
    if "resolved" in text:
        return "RESOLVED"
    if "deferred" in text:
        return "DEFERRED"
    if "closed" in text:
        return "CLOSED"
    if "tracking" in text:
        return "TRACKING"
    return text.strip() or "unknown"


# Regex helpers -----------------------------------------------------------------

SECTION_RE = re.compile(r"^\*\*Section:\*\*\s*(.+?)\s*$", re.MULTILINE)
AUTHOR_RE = re.compile(r"^\*\*Author:\*\*\s*(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\*\*Date:\*\*\s*(.+?)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)


def extract_block(block_text: str, header: str) -> str | None:
    """Extract the content of a header like `**Comment body:**` or `**Resolution:**`.

    Returns the raw text following that header until the next `**Header:**`-style
    line or the end of the section. Handles both inline form
    (``**Resolution:** Some text on this line``) and block form
    (``**Comment body:**\\n\\n> Some quoted text``). Strips the surrounding
    ``> `` blockquote prefix and outer whitespace, but preserves internal
    newlines and unicode exactly.
    """
    pattern = (
        rf"\*\*{re.escape(header)}\:\*\*[ \t]*(.*?)(?=\n\*\*[A-Za-z][^*]*?\:\*\*|\Z)"
    )
    match = re.search(pattern, block_text, re.DOTALL)
    if not match:
        return None
    raw = match.group(1)
    # Strip leading blockquote markers ("> "), preserving inline content.
    lines = raw.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.strip() == ">":
            cleaned_lines.append("")
        else:
            cleaned_lines.append(line)
    # Trim trailing `---` separator lines that fall through when this is the
    # last block in the file (no following `**Header:**` to terminate on).
    while cleaned_lines and cleaned_lines[-1].strip() in {"", "---"}:
        cleaned_lines.pop()
    cleaned = "\n".join(cleaned_lines).strip()
    # Filter out the placeholder for unfilled resolutions.
    if cleaned == "_(to be filled in during review)_":
        return None
    return cleaned if cleaned else None


def extract_fenced_block(block_text: str, header: str) -> str | None:
    """Extract a triple-backtick fenced block following a `**Header:**` line."""
    pattern = (
        rf"\*\*{re.escape(header)}\:\*\*\s*\n+```\s*\n(.*?)\n```"
    )
    match = re.search(pattern, block_text, re.DOTALL)
    if not match:
        return None
    return match.group(1)


# Section parsing ---------------------------------------------------------------


def parse_section_path(raw_section: str) -> tuple[str, str | None, str | None]:
    """Return (deepest_section, section_top, subsection).

    `raw_section` is the value from the `**Section:**` line. It may be:
      - a deep path like "Beyond Recall: ... > 1. Introduction > 1.1 Recall Is..."
      - a short path like "§3.7.3"
      - a special value like "(top of document)" or "front matter / appendix"

    Strategy: walk path segments left-to-right; pick the deepest segment whose
    leading token is a section number ("1.1 Recall..." or "§3.7.3 ..."). This
    avoids false positives from numerals embedded later in a heading
    (e.g. "C1 4.20 -> C3 1.80").
    """
    deepest = raw_section.strip()
    if " > " in deepest:
        segments = [s.strip() for s in deepest.split(" > ")]
        deepest = segments[-1]
    else:
        segments = [deepest]

    # Strip the document title segment if present.
    segments = [s for s in segments if not s.startswith("Beyond Recall:")]

    # Heading-leading number pattern (number must start the segment).
    leading_re = re.compile(r"^(?:§\s*)?(\d+(?:\.\d+)*)\b")

    last_top: str | None = None
    last_sub: str | None = None
    for seg in segments:
        m = leading_re.match(seg)
        if not m:
            continue
        num = m.group(1)
        last_top = f"§{num.split('.')[0]}"
        last_sub = f"§{num}" if "." in num else None

    # If the raw_section was a bare "§3.7.3"-style string, the segment-walk
    # already picked it up. If raw didn't yield any heading-leading number,
    # fall back to scanning for a §-prefixed number anywhere in the string.
    if last_top is None:
        any_section_re = re.compile(r"§\s*(\d+(?:\.\d+)*)")
        matches = any_section_re.findall(raw_section)
        if matches:
            last = matches[-1]
            last_top = f"§{last.split('.')[0]}"
            last_sub = f"§{last}" if "." in last else None

    return deepest, last_top, last_sub


# Item parsing ------------------------------------------------------------------


def parse_bavani_block(header_line: str, body: str) -> dict:
    """Parse a Bavani structural-note block (B1-B10)."""
    m = re.match(r"^### (B\d+)\s*\((.+?)\)\s*$", header_line.strip())
    if not m:
        raise ValueError(f"Bad Bavani header: {header_line!r}")
    bid = m.group(1)
    title = m.group(2)

    section_match = SECTION_RE.search(body)
    raw_section = section_match.group(1) if section_match else ""
    deepest, section_top, subsection = parse_section_path(raw_section)

    comment_body = extract_block(body, "Comment")
    status_match = STATUS_RE.search(body)
    status_line = status_match.group(1) if status_match else ""
    status = parse_status(status_line)

    resolution = extract_block(body, "Resolution")

    themes = derive_themes(comment_body or "")

    return {
        "id": bid,
        "comment_id": None,
        "title": title,
        "section": deepest,
        "section_top": section_top,
        "subsection": subsection,
        "author": "Bavani (structural review notes)",
        "date": "2026-04-27",
        "comment_body": comment_body,
        "anchor_text": None,
        "surrounding_paragraph": None,
        "status": status,
        "status_line": status_line,
        "resolution": resolution,
        "themes": themes,
    }


def parse_comment_block(header_line: str, body: str, idx: int) -> dict:
    """Parse a docx comment block. `idx` is the 1-based comment index."""
    m = re.match(r"^## Comment (\d+)\s*\(id=(\d+)\)\s*$", header_line.strip())
    if not m:
        raise ValueError(f"Bad Comment header: {header_line!r}")
    comment_num = int(m.group(1))
    docx_id = m.group(2)
    if comment_num != idx:
        # Non-fatal sanity check; the source file numbers Comment 1..173 in
        # order, but be defensive.
        pass

    cid = f"C{comment_num}"

    section_match = SECTION_RE.search(body)
    raw_section = section_match.group(1) if section_match else ""
    deepest, section_top, subsection = parse_section_path(raw_section)

    author_match = AUTHOR_RE.search(body)
    author = author_match.group(1).strip() if author_match else None

    date_match = DATE_RE.search(body)
    date = date_match.group(1).strip() if date_match else None

    comment_body = extract_block(body, "Comment body")
    anchor_text = extract_fenced_block(body, "Anchored text")
    surrounding = extract_block(body, "Surrounding paragraph (full)")

    status_match = STATUS_RE.search(body)
    status_line = status_match.group(1) if status_match else ""
    status = parse_status(status_line)

    resolution = extract_block(body, "Resolution")

    themes = derive_themes(comment_body or "")

    return {
        "id": cid,
        "comment_id": f"id={docx_id}",
        "section": deepest,
        "section_top": section_top,
        "subsection": subsection,
        "author": author,
        "date": date,
        "comment_body": comment_body,
        "anchor_text": anchor_text,
        "surrounding_paragraph": surrounding,
        "status": status,
        "status_line": status_line,
        "resolution": resolution,
        "themes": themes,
    }


# Top-level driver --------------------------------------------------------------


def split_blocks(text: str) -> list[tuple[str, str]]:
    """Split the full source text into (header_line, body) tuples for both
    Bavani and Comment items, in document order. Meta-items (M1, M2) are
    intentionally excluded.
    """
    lines = text.split("\n")
    blocks: list[tuple[str, str]] = []
    current_header: str | None = None
    current_buf: list[str] = []
    in_meta = False

    def flush():
        nonlocal current_header, current_buf
        if current_header is not None:
            blocks.append((current_header, "\n".join(current_buf)))
        current_header = None
        current_buf = []

    for line in lines:
        # Track meta-items section so we can ignore M1/M2 headers.
        if line.startswith("## Meta-items"):
            flush()
            in_meta = True
            continue
        if line.startswith("## Docx Comments"):
            flush()
            in_meta = False
            continue

        if in_meta:
            continue

        # Bavani note headers (### B1..B10) and Comment headers (## Comment N)
        if re.match(r"^### B\d+\s*\(", line):
            flush()
            current_header = line
            current_buf = []
            continue
        if re.match(r"^## Comment \d+\s*\(id=\d+\)", line):
            flush()
            current_header = line
            current_buf = []
            continue

        # End-of-section dividers we don't need to keep, but keep them in the
        # buffer so the regexes that scan the body still find headers cleanly.
        if current_header is not None:
            current_buf.append(line)

    flush()
    return blocks


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"Source not found: {SOURCE}")

    text = SOURCE.read_text(encoding="utf-8")
    blocks = split_blocks(text)

    bavani_items: list[dict] = []
    comment_items: list[dict] = []
    comment_idx = 0
    for header, body in blocks:
        if header.startswith("### B"):
            bavani_items.append(parse_bavani_block(header, body))
        elif header.startswith("## Comment"):
            comment_idx += 1
            comment_items.append(parse_comment_block(header, body, comment_idx))

    items = bavani_items + comment_items

    # Sanity checks --------------------------------------------------------
    assert len(bavani_items) == 10, f"Expected 10 Bavani items, got {len(bavani_items)}"
    assert (
        len(comment_items) == 173
    ), f"Expected 173 docx comment items, got {len(comment_items)}"
    assert len(items) == 183, f"Expected 183 total, got {len(items)}"

    # Summaries ------------------------------------------------------------
    themes_summary: dict[str, list[str]] = {t: [] for t in THEME_RULES.keys()}
    section_summary: dict[str, list[str]] = {}
    section_top_summary: dict[str, list[str]] = {}
    status_summary: dict[str, list[str]] = {}

    for item in items:
        for t in item["themes"]:
            themes_summary[t].append(item["id"])
        sub = item["subsection"]
        if sub:
            section_summary.setdefault(sub, []).append(item["id"])
        elif item["section_top"]:
            section_summary.setdefault(item["section_top"], []).append(item["id"])
        else:
            section_summary.setdefault(item["section"] or "(uncategorized)", []).append(
                item["id"]
            )
        if item["section_top"]:
            section_top_summary.setdefault(item["section_top"], []).append(item["id"])
        status_summary.setdefault(item["status"], []).append(item["id"])

    # Sort section_summary keys for human readability (§-style numerically).
    def section_sort_key(k: str):
        m = re.match(r"^§(\d+(?:\.\d+)*)", k)
        if not m:
            return (1, k)
        parts = tuple(int(p) for p in m.group(1).split("."))
        return (0, parts)

    section_summary_sorted = dict(
        sorted(section_summary.items(), key=lambda kv: section_sort_key(kv[0]))
    )
    section_top_summary_sorted = dict(
        sorted(section_top_summary.items(), key=lambda kv: section_sort_key(kv[0]))
    )

    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "docs/reviews/v11_comments_extracted_20260427.md",
        "total_items": len(items),
        "bavani_count": len(bavani_items),
        "comment_count": len(comment_items),
        "items": items,
        "themes_summary": themes_summary,
        "section_summary": section_summary_sorted,
        "section_top_summary": section_top_summary_sorted,
        "status_summary": status_summary,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Console summary ------------------------------------------------------
    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    print(f"  total items:       {len(items)}")
    print(f"  Bavani items:      {len(bavani_items)}")
    print(f"  Docx comments:     {len(comment_items)}")
    print()
    print("Theme histogram:")
    for theme, ids in themes_summary.items():
        print(f"  {theme:<22s} {len(ids):>4d}")
    print()
    print("Status histogram:")
    for status, ids in sorted(status_summary.items(), key=lambda kv: -len(kv[1])):
        print(f"  {status:<22s} {len(ids):>4d}")
    print()
    print("Top-level section histogram:")
    for sec, ids in section_top_summary_sorted.items():
        print(f"  {sec:<10s} {len(ids):>4d}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
