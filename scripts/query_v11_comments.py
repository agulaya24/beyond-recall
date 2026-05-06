"""Query helper for the v11 comment index.

Reads `docs/reviews/v11_comment_index.json` and exposes a small set of
filter functions plus a CLI. Filters compose: `--section §1.3 --status
pending --theme footnote`.

Examples:
    python scripts/query_v11_comments.py --section §1.3
    python scripts/query_v11_comments.py --theme footnote
    python scripts/query_v11_comments.py --status pending --section §4
    python scripts/query_v11_comments.py --search "color cod"
    python scripts/query_v11_comments.py --id C42

Default output: one item per line, "<id>  <status>  <section_top/subsection>
<comment_body first 120 chars>". Use `--full` to print everything.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "docs" / "reviews" / "v11_comment_index.json"


def load_index(path: Path = INDEX_PATH) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(
            f"Index not found at {path}. "
            f"Build it with: python scripts/_build_v11_comment_index.py"
        )
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ filters


def by_section(items: list[dict], pattern: str) -> list[dict]:
    """Match items whose section_top or subsection matches `pattern`.

    Matching is forgiving: `§1.3` matches the exact subsection `§1.3`, and
    `§1` matches all of `§1`, `§1.1`, `§1.2`, ... A bare number (no `§`)
    is treated identically to its `§`-prefixed form.
    """
    needle = pattern.strip()
    if not needle.startswith("§"):
        needle = f"§{needle}"

    def matches(item: dict) -> bool:
        sub = item.get("subsection") or ""
        top = item.get("section_top") or ""
        # Exact match on either field.
        if needle == sub or needle == top:
            return True
        # Prefix match on subsection (§1 should match §1.3, §1.3.4).
        if sub and (sub == needle or sub.startswith(needle + ".")):
            return True
        # If user asked for a top-level (e.g. §1) and that's the item's top,
        # the equality check above already handled it.
        return False

    return [i for i in items if matches(i)]


def by_theme(items: list[dict], theme: str) -> list[dict]:
    """Match items tagged with `theme`."""
    needle = theme.strip().lower()
    return [i for i in items if needle in [t.lower() for t in i.get("themes", [])]]


def by_status(items: list[dict], status: str) -> list[dict]:
    """Match items by status. Case-insensitive; accepts `pending`, `resolved`,
    `deferred`, `closed`, `tracking`."""
    needle = status.strip().lower()
    return [i for i in items if (i.get("status") or "").lower() == needle]


def search(items: list[dict], keyword: str) -> list[dict]:
    """Substring (case-insensitive) match across comment_body, anchor_text,
    surrounding_paragraph, and resolution."""
    needle = keyword.lower()

    def hit(item: dict) -> bool:
        for field in (
            "comment_body",
            "anchor_text",
            "surrounding_paragraph",
            "resolution",
        ):
            v = item.get(field) or ""
            if needle in v.lower():
                return True
        return False

    return [i for i in items if hit(i)]


def by_id(items: list[dict], item_id: str) -> list[dict]:
    needle = item_id.strip().upper()
    return [i for i in items if i.get("id", "").upper() == needle]


# ------------------------------------------------------------------ rendering


def render_brief(item: dict) -> str:
    sec = item.get("subsection") or item.get("section_top") or "(no §)"
    body = (item.get("comment_body") or "").replace("\n", " ").strip()
    if len(body) > 120:
        body = body[:117] + "..."
    return f"{item['id']:<6s} {item['status']:<10s} {sec:<10s} {body}"


def render_full(item: dict) -> str:
    out = []
    out.append("=" * 78)
    out.append(f"ID: {item['id']}  ({item.get('comment_id') or 'Bavani'})")
    if item.get("title"):
        out.append(f"Title: {item['title']}")
    out.append(f"Section: {item.get('section')}")
    out.append(
        f"  section_top={item.get('section_top')}  subsection={item.get('subsection')}"
    )
    out.append(f"Author: {item.get('author')}")
    out.append(f"Date:   {item.get('date')}")
    out.append(f"Status: {item.get('status')}  ({item.get('status_line')})")
    if item.get("themes"):
        out.append(f"Themes: {', '.join(item['themes'])}")
    out.append("")
    out.append("Comment body:")
    out.append(item.get("comment_body") or "(empty)")
    if item.get("anchor_text"):
        out.append("")
        out.append("Anchored text:")
        out.append(item["anchor_text"])
    if item.get("surrounding_paragraph"):
        out.append("")
        out.append("Surrounding paragraph:")
        out.append(item["surrounding_paragraph"])
    if item.get("resolution"):
        out.append("")
        out.append("Resolution:")
        out.append(item["resolution"])
    return "\n".join(out)


# ------------------------------------------------------------------ CLI


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Query the v11 paper-review comment index.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--section", help="Section filter, e.g. §1.3 or §4 or 4.1.1")
    p.add_argument("--theme", help="Theme filter, e.g. footnote, layman, reorder")
    p.add_argument(
        "--status",
        help="Status filter: pending / resolved / deferred / closed / tracking",
    )
    p.add_argument("--search", help="Substring keyword search across body/anchor/resolution")
    p.add_argument("--id", help="Exact id lookup, e.g. C42 or B3")
    p.add_argument(
        "--full",
        action="store_true",
        help="Print full content of each matching item.",
    )
    p.add_argument(
        "--count-only",
        action="store_true",
        help="Print only the count of matches (no per-item lines).",
    )
    p.add_argument(
        "--ids-only",
        action="store_true",
        help="Print only the ids, one per line.",
    )
    p.add_argument(
        "--list-themes",
        action="store_true",
        help="Print available themes and their counts, then exit.",
    )
    p.add_argument(
        "--list-sections",
        action="store_true",
        help="Print available sections and their counts, then exit.",
    )
    args = p.parse_args(argv)

    # On Windows the default cp1252 stdout chokes on em-dashes / §; force utf-8.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    data = load_index()
    items: list[dict] = list(data["items"])

    if args.list_themes:
        for theme, ids in data.get("themes_summary", {}).items():
            print(f"{theme:<22s} {len(ids):>4d}")
        return 0

    if args.list_sections:
        for sec, ids in data.get("section_summary", {}).items():
            print(f"{sec:<14s} {len(ids):>4d}")
        return 0

    if args.id:
        items = by_id(items, args.id)
    if args.section:
        items = by_section(items, args.section)
    if args.theme:
        items = by_theme(items, args.theme)
    if args.status:
        items = by_status(items, args.status)
    if args.search:
        items = search(items, args.search)

    if args.count_only:
        print(len(items))
        return 0

    if args.ids_only:
        for it in items:
            print(it["id"])
        return 0

    if args.full:
        for it in items:
            print(render_full(it))
            print()
    else:
        for it in items:
            print(render_brief(it))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
