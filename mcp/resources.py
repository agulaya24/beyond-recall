"""MCP Resource helpers for the Beyond Recall study server.

Exposes paper sections via paper://section/<id> URIs. The canonical paper
source is the v11.5 draft at docs/beyond_recall_v11_5_draft.md.

Section IDs come from the leading numeric token of each heading (e.g. '3.6.2').
Headings without a numeric prefix get a slug derived from the title.
"""
from __future__ import annotations

from typing import Any

from tools import (
    PAPER_PATH,
    get_paper_section,
    list_paper_sections,
)


PAPER_URI_PREFIX = "paper://section/"


def section_uri(section_id: str) -> str:
    """Build the MCP resource URI for a paper section."""
    return f"{PAPER_URI_PREFIX}{section_id}"


def index_resources() -> list[dict[str, Any]]:
    """Return MCP-style resource descriptors for every paper section."""
    descs: list[dict[str, Any]] = []
    for sec in list_paper_sections():
        descs.append({
            "uri": section_uri(sec["id"]),
            "name": f"{sec['id']} {sec['title']}",
            "description": (
                f"Paper section {sec['id']} ('{sec['title']}'), lines "
                f"{sec['line_start']}-{sec['line_end']} of {PAPER_PATH.name}."
            ),
            "mimeType": "text/markdown",
        })
    return descs


def read_resource(uri: str) -> str:
    """Resolve a paper://section/<id> URI to the section's markdown text."""
    if not uri.startswith(PAPER_URI_PREFIX):
        return f"Error: unknown resource URI {uri!r}"
    section_id = uri[len(PAPER_URI_PREFIX):]
    res = get_paper_section(section_id)
    if "error" in res:
        return f"Error: {res['error']}"
    title_line = f"# {res['title']} (paper §{res['id']})"
    return f"{title_line}\n\n{res['text']}"
