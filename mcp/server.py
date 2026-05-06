"""Beyond Recall study MCP server (MVP).

Exposes the study's data and indexes as agent-callable tools and resources.
Transport: stdio (local).

Tools:
    search_study           -- FTS + semantic search over the study knowledge index
    get_subject_score      -- canonical mean score per (subject, condition, panel)
    list_subjects          -- 14 main-study subjects with C5 / C4a / Δ_spec
    get_provenance         -- locate provenance + data-reference citations for a claim
    list_anchor_crossings  -- per-question multi-anchor jumps for a condition pair

Resources:
    paper://section/<id>   -- text of paper section <id> (e.g. '3.6.2')

Run:
    python server.py

Register with Claude Desktop or Claude Code per mcp/README.md.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Literal

# Ensure local module imports work whether invoked as a script or module.
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="[memory-study] %(levelname)s: %(message)s",
)
logger = logging.getLogger("memory-study")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "ERROR: MCP SDK not installed. Install with: pip install 'mcp[cli]'",
        file=sys.stderr,
    )
    sys.exit(1)

import tools as study_tools  # noqa: E402
import resources as study_resources  # noqa: E402


mcp_app = FastMCP("memory-study-repo")


# ---------------------------------------------------------------------------
# Tool wrappers
# ---------------------------------------------------------------------------

@mcp_app.tool()
def search_study(
    query: str,
    mode: Literal["fts", "semantic", "both"] = "both",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search the study knowledge index (paper, results, scripts, reviews).

    Args:
        query: Search query. For FTS mode this is an SQLite FTS5 expression;
               for semantic mode it is natural-language.
        mode:  'fts' (keyword), 'semantic' (vector), or 'both' (default).
        limit: Maximum results to return (1-50).
    """
    return study_tools.search_study(query=query, mode=mode, limit=limit)


@mcp_app.tool()
def get_subject_score(
    subject: str,
    condition: str,
    panel: Literal["5-judge-primary", "7-judge-sensitivity"] = "5-judge-primary",
) -> dict[str, Any]:
    """Recompute the canonical mean score for a subject and condition.

    Args:
        subject:   Short form ('seacole') or directory name ('global_seacole').
        condition: Short form ('C4a') or full variant ('C4a_full_facts_plus_spec').
        panel:     '5-judge-primary' (canonical) or '7-judge-sensitivity'.

    Returns subject, condition, mean, n_questions, and per-judge breakdown.
    """
    return study_tools.get_subject_score(subject=subject, condition=condition, panel=panel)


@mcp_app.tool()
def list_subjects() -> list[dict[str, Any]]:
    """List the 14 main-study subjects with C5 baseline, C4a (facts+spec),
    Δ_spec, low-baseline flag (C5 ≤ 2.0), and on-disk paths.
    """
    return study_tools.list_subjects()


@mcp_app.tool()
def get_provenance(claim: str, limit: int = 8) -> list[dict[str, Any]]:
    """Search PROVENANCE_INDEX.md and DATA_REFERENCE.md for sections relevant
    to a claim. Returns file pointers and section labels.
    """
    return study_tools.get_provenance(claim=claim, limit=limit)


@mcp_app.tool()
def list_anchor_crossings(
    condition_pair: str = "C5_to_C4a",
    min_jump: int = 2,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Return per-question multi-anchor crossings for a condition pair.

    Args:
        condition_pair: One of 'C5_to_C4a', 'C5_to_C4', 'C5_to_C2a',
                        'C2c_to_C2a', 'C4_to_C4a', 'C5_to_C8', 'C5_to_C9',
                        'C8_to_C9'.
        min_jump:       Minimum absolute integer-band jump (default 2).
        limit:          Maximum rows to return.
    """
    return study_tools.list_anchor_crossings(
        condition_pair=condition_pair, min_jump=min_jump, limit=limit
    )


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

# FastMCP exposes a single resource template via @mcp.resource(uri).
# We expose paper sections as a templated URI: paper://section/{section_id}.

@mcp_app.resource("paper://section/{section_id}")
def paper_section_resource(section_id: str) -> str:
    """Return the text of paper section <section_id> (e.g. '3.6.2', '4.1')."""
    return study_resources.read_resource(study_resources.section_uri(section_id))


@mcp_app.resource("paper://index")
def paper_section_index() -> str:
    """Markdown index of every paper section, with paper://section/<id> URIs."""
    rows = study_resources.index_resources()
    if not rows:
        return "Paper draft not found."
    lines = ["# Beyond Recall paper section index", ""]
    for r in rows:
        lines.append(f"- `{r['uri']}` -- {r['name']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server over stdio."""
    logger.info("Starting Beyond Recall study MCP server.")
    logger.info("Index DB: %s", study_tools.DB_PATH)
    logger.info("Vector store: %s", study_tools.VEC_PATH)
    mcp_app.run(transport="stdio")


if __name__ == "__main__":
    main()
