"""Build a paper-footnote ↔ docs/research/ traceability matrix.

Per Aarik 2026-05-11: docs/research/ has 30+ paper footnote references by exact
path and was flagged HIGH cascade risk in the repo cleanup audit. Rather than
moving any files, build a separate matrix that records every paper-text path
reference INTO docs/research/ so any future change to those files has a
machine-readable list of inbound refs to update in lock-step.

Output:
    docs/research/TRACEABILITY_MATRIX.md   (human-readable)
    docs/research/TRACEABILITY_MATRIX.json (machine-readable)

Match strategy: scan the current paper draft for any literal mention of
`docs/research/<path>` and aggregate by referenced path. Cross-check against
the file system to verify each referenced path exists.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "docs" / "beyond_recall_v11_9_10_draft.md"
SUPPLEMENTARY_DIR = REPO / "docs" / "supplementary"

OUT_MD = REPO / "docs" / "research" / "TRACEABILITY_MATRIX.md"
OUT_JSON = REPO / "docs" / "research" / "TRACEABILITY_MATRIX.json"

# Match `docs/research/path/to/file.ext` references; capture path part
REF_RE = re.compile(r"docs/research/([A-Za-z0-9_./\-]+\.(?:md|json|txt|csv|tsv|yaml|yml|py))")


def scan_paper(path: Path) -> dict[str, list[int]]:
    refs: dict[str, list[int]] = defaultdict(list)
    if not path.exists():
        return refs
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for match in REF_RE.finditer(line):
            refs[match.group(1)].append(lineno)
    return refs


def scan_supplementary() -> dict[str, dict[str, list[int]]]:
    """Also scan supplementary appendices for inbound refs."""
    out: dict[str, dict[str, list[int]]] = {}
    if not SUPPLEMENTARY_DIR.exists():
        return out
    for p in SUPPLEMENTARY_DIR.rglob("*.md"):
        refs: dict[str, list[int]] = defaultdict(list)
        for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for match in REF_RE.finditer(line):
                refs[match.group(1)].append(lineno)
        if refs:
            out[str(p.relative_to(REPO)).replace("\\", "/")] = dict(refs)
    return out


def main() -> int:
    print(f"Scanning {PAPER.name}...")
    paper_refs = scan_paper(PAPER)
    print(f"  {sum(len(v) for v in paper_refs.values())} reference occurrences across {len(paper_refs)} files\n")

    print("Scanning supplementary appendices...")
    supp_refs = scan_supplementary()
    print(f"  {len(supp_refs)} supplementary docs reference {sum(len(refs) for refs in supp_refs.values())} files\n")

    # Verify each referenced path exists
    matrix: list[dict] = []
    for path, paper_lines in sorted(paper_refs.items()):
        full = REPO / "docs" / "research" / path
        exists = full.exists()
        size = full.stat().st_size if exists else None
        # Find any supplementary references to the same file
        supp_pointers = {}
        for supp_doc, supp_doc_refs in supp_refs.items():
            if path in supp_doc_refs:
                supp_pointers[supp_doc] = supp_doc_refs[path]
        matrix.append({
            "path": f"docs/research/{path}",
            "exists": exists,
            "size_bytes": size,
            "paper_lines": paper_lines,
            "paper_ref_count": len(paper_lines),
            "supplementary_refs": supp_pointers,
        })

    # Files that supplementary docs reference but paper does not
    supp_only: set[str] = set()
    for supp_doc_refs in supp_refs.values():
        supp_only.update(supp_doc_refs.keys())
    supp_only -= set(paper_refs.keys())

    output = {
        "generated": "2026-05-11",
        "paper": str(PAPER.relative_to(REPO)).replace("\\", "/"),
        "paper_referenced_files": matrix,
        "supplementary_only_files": sorted(supp_only),
        "missing": [m["path"] for m in matrix if not m["exists"]],
    }
    OUT_JSON.write_text(json.dumps(output, indent=2), encoding="utf-8")

    # Markdown view
    lines = [
        "# docs/research/ Traceability Matrix",
        "",
        "Generated: 2026-05-11. Source: paper text + all `docs/supplementary/*.md` appendices.",
        "",
        "**Purpose:** Per Aarik 2026-05-11, `docs/research/` was flagged HIGH cascade risk in the repo cleanup audit because the paper has 30+ direct footnote references by exact path. Rather than restructure `docs/research/` (post-launch), this matrix is the canonical machine-readable list of inbound references so any future file move can update referrers in lock-step.",
        "",
        "**Regenerate** after any paper edit that touches a `docs/research/<file>` mention:",
        "",
        "```",
        "python scripts/build_research_traceability_matrix_20260511.py",
        "```",
        "",
        f"**Summary.** Paper references {len(matrix)} distinct files in `docs/research/`. Of those, **{sum(1 for m in matrix if not m['exists'])}** do not exist on disk (broken refs to fix). Supplementary appendices reference {len(supp_only)} additional files not cited from the paper body.",
        "",
        "## Paper-referenced files",
        "",
        "| Path | On disk | Size | Paper lines | Supp refs |",
        "|---|---|---:|---|---|",
    ]
    for m in matrix:
        ok = "OK" if m["exists"] else "**MISSING**"
        size = f"{m['size_bytes']:,}" if m["size_bytes"] is not None else "—"
        paper_lines_str = ", ".join(str(n) for n in m["paper_lines"][:6])
        if len(m["paper_lines"]) > 6:
            paper_lines_str += f", … ({len(m['paper_lines'])} total)"
        supp_summary = ", ".join(
            f"{Path(k).name}:{','.join(str(n) for n in v[:3])}"
            for k, v in m["supplementary_refs"].items()
        ) or "—"
        lines.append(f"| `{m['path']}` | {ok} | {size} | {paper_lines_str} | {supp_summary} |")

    if supp_only:
        lines.extend([
            "",
            "## Supplementary-only references",
            "",
            "These files are referenced by supplementary appendices but not by the paper body. They still matter for `docs/supplementary/*.md` reproducibility.",
            "",
        ])
        for path in sorted(supp_only):
            full = REPO / "docs" / "research" / path
            ok = "OK" if full.exists() else "**MISSING**"
            lines.append(f"- `docs/research/{path}` ({ok})")

    if any(not m["exists"] for m in matrix):
        lines.extend([
            "",
            "## Broken references (action required)",
            "",
        ])
        for m in matrix:
            if not m["exists"]:
                lines.append(f"- `{m['path']}` — referenced at paper lines {m['paper_lines']}")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(REPO)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO)}")
    if any(not m["exists"] for m in matrix):
        print(f"\nWARNING: {sum(1 for m in matrix if not m['exists'])} broken references (see report)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
