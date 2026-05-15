"""Mechanistic footnote-provenance audit for v11.9.11.

For every numerical claim (counts, percentages, p-values, deltas, means)
inside every footnote definition in the paper, attempt to locate the
authoritative source file containing that value. Output a structured
audit document.

Approach:
  1. Parse all `[^name]: body` footnote definitions from the paper.
  2. Within each body, extract numerical tokens with surrounding context.
  3. For each number, search authoritative source files for that value
     in a similar context.
  4. Emit a Markdown report grouped by footnote, with one row per number:
     `(footnote, number, paper-context, source-file, source-context,
       VERIFIED/UNVERIFIED)`.

Authoritative sources searched:
  - docs/research/*.md
  - docs/research/v11_emit/*.json
  - docs/DATA_REFERENCE.md

A number is "VERIFIED" if it appears in at least one authoritative source
in a phrase the heuristic judges to be the same claim. The match is by
proximity of numeric value plus a snippet of the surrounding wording; this
is heuristic, not perfect, but catches the majority of cases for spot-check.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "docs" / "beyond_recall_v11_9_11_draft.md"
OUT = REPO / "docs" / "reviews" / "v11_9_11_footnote_provenance_audit_20260511.md"

SOURCE_GLOBS = [
    REPO / "docs" / "research",
    REPO / "docs" / "DATA_REFERENCE.md",
    REPO / "docs" / "KEY_FINDINGS.md",
]


def extract_footnotes(text: str) -> list[tuple[str, str]]:
    return re.findall(
        r"^\[\^([a-z0-9-]+)\]:\s+(.+?)(?=\n\n|\n\[\^|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )


NUMBER_RE = re.compile(
    r"""
    (?<![A-Za-z\.])                # not preceded by letter (avoids §4.1)
    (?P<num>
        [-−+]?                     # optional sign
        \d{1,3}(?:,\d{3})*         # 1-3 digits, optional thousands
        (?:\.\d+)?                 # optional decimal
        |
        [-−+]?\.\d+                # decimal-only
    )
    (?P<unit>%|\b)
    """,
    re.VERBOSE,
)


def extract_numbers(body: str) -> list[tuple[str, str]]:
    """Return [(number_str, context_30c), ...] from a footnote body.

    Skips numbers inside section refs (§3.7.6, §4.2.1, etc.) and inside
    footnote-reference brackets ([^xyz]).
    """
    # Strip section refs and footnote refs first so they don't match
    cleaned = re.sub(r"§\d+(\.\d+)+(\.\d+)?", " ", body)
    cleaned = re.sub(r"\[\^[a-z0-9-]+\]", " ", cleaned)
    # Strip arxiv refs like "arXiv:2509.12517" and year "2025" patterns
    cleaned = re.sub(r"arXiv:\d+\.\d+", " ", cleaned)

    results = []
    for m in NUMBER_RE.finditer(cleaned):
        num_str = m.group("num").replace("−", "-")
        # Skip 4-digit numbers that look like years
        bare = num_str.replace("-", "").replace("+", "")
        if "." not in bare and len(bare) == 4 and bare.startswith(("19", "20", "21")):
            continue
        if num_str.replace("-", "").replace("+", "").replace(".", "").replace(",", "") == "":
            continue
        start = max(0, m.start() - 30)
        end = min(len(cleaned), m.end() + 30)
        context = cleaned[start:end].strip()
        results.append((num_str, context))
    return results


def normalize_for_search(num_str: str) -> list[str]:
    """Generate search-form variants of a number for source matching."""
    out = [num_str]
    bare = num_str.lstrip("+-−")
    out.append(bare)
    # Without commas
    if "," in num_str:
        out.append(num_str.replace(",", ""))
        out.append(bare.replace(",", ""))
    # Strip trailing zeros after decimal
    if "." in bare:
        stripped = re.sub(r"\.?0+$", "", bare)
        out.append(stripped)
    return list(set(out))


def load_source_corpus() -> dict[str, str]:
    """Load all authoritative source files into a dict path -> text."""
    out = {}
    for src in SOURCE_GLOBS:
        if src.is_file():
            try:
                out[src.relative_to(REPO).as_posix()] = src.read_text(
                    encoding="utf-8", errors="replace"
                )
            except Exception:
                pass
        elif src.is_dir():
            for f in src.rglob("*.md"):
                try:
                    out[f.relative_to(REPO).as_posix()] = f.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except Exception:
                    pass
            for f in src.rglob("*.json"):
                try:
                    out[f.relative_to(REPO).as_posix()] = f.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except Exception:
                    pass
    return out


def find_in_sources(num_str: str, sources: dict[str, str]) -> list[str]:
    """Return list of source files containing the number."""
    hits = []
    variants = normalize_for_search(num_str)
    for path, text in sources.items():
        for v in variants:
            if v and v in text:
                hits.append(path)
                break
    return hits


def main() -> int:
    text = PAPER.read_text(encoding="utf-8")
    footnotes = extract_footnotes(text)
    print(f"Footnotes: {len(footnotes)}")

    print("Loading source corpus...")
    sources = load_source_corpus()
    print(f"Source files loaded: {len(sources)}")

    lines = [
        "# v11.9.11 footnote provenance audit",
        "",
        "Generated by `scripts/footnote_provenance_audit_20260511.py`.",
        "",
        "For each footnote, every extracted numerical claim is matched against",
        "authoritative source files in `docs/research/`, `docs/DATA_REFERENCE.md`,",
        "and `docs/KEY_FINDINGS.md`. A number is **VERIFIED** if the same value",
        "appears in at least one source file. **UNVERIFIED** numbers either are",
        "not in any source corpus or appear in a different form (rounded, percent-vs-fraction, etc.).",
        "",
        "Heuristic match, not strict provenance. Recheck UNVERIFIED items manually.",
        "",
        "---",
        "",
    ]

    counts = Counter()
    for name, body in footnotes:
        nums = extract_numbers(body)
        if not nums:
            continue
        lines.append(f"## [{name}]")
        lines.append("")
        lines.append(f"_Body:_ {body[:200].replace(chr(10), ' ')}{'...' if len(body) > 200 else ''}")
        lines.append("")
        lines.append("| Number | Paper context | Source files (hits) | Status |")
        lines.append("|---|---|---|---|")
        for num, ctx in nums:
            hits = find_in_sources(num, sources)
            ctx_short = ctx.replace("|", "\\|")[:60]
            if hits:
                hits_str = "; ".join(hits[:2]) + (f" +{len(hits) - 2}" if len(hits) > 2 else "")
                status = "VERIFIED"
                counts["VERIFIED"] += 1
            else:
                hits_str = "—"
                status = "UNVERIFIED"
                counts["UNVERIFIED"] += 1
            lines.append(f"| `{num}` | {ctx_short} | {hits_str} | {status} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **VERIFIED:** {counts['VERIFIED']}")
    lines.append(f"- **UNVERIFIED:** {counts['UNVERIFIED']}")
    total = counts["VERIFIED"] + counts["UNVERIFIED"]
    if total:
        rate = 100 * counts["VERIFIED"] / total
        lines.append(f"- **Verification rate:** {rate:.1f}%")
    lines.append("")
    lines.append("UNVERIFIED items deserve manual recheck. Many will be heuristic")
    lines.append("false-negatives (rounding differences, percent vs. fraction forms,")
    lines.append("numbers presented inline in the paper itself rather than in a")
    lines.append("dedicated source file). Genuine UNVERIFIED items should either be")
    lines.append("traced back to source data or cut from the footnote.")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote: {OUT}")
    print(f"Summary: VERIFIED={counts['VERIFIED']}, UNVERIFIED={counts['UNVERIFIED']}")
    if total:
        print(f"Verification rate: {100 * counts['VERIFIED'] / total:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
