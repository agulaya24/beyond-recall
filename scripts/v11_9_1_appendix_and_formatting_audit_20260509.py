"""Appendix word-count + table-formatting audit for v11.9.1.

Outputs:
  1. Appendix subsection word counts — sorted descending — to identify cut candidates
  2. Tables with cells longer than CELL_LONG_THRESHOLD characters — these wrap badly
     in narrow columns and produce 10-line cells
  3. Heading-level sanity check — flag titles that are very long (likely to wrap)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "docs" / "beyond_recall_v11_9_1_draft.md"
OUT = REPO / "docs" / "research" / "v11_9_1_appendix_and_formatting_audit_20260509.md"

CELL_LONG_THRESHOLD = 200      # any single cell > 200 chars wraps to many lines
CELL_VERY_LONG_THRESHOLD = 400 # > 400 chars is a 10-line cell

text = SRC.read_text(encoding="utf-8")
lines = text.splitlines()

heading_re = re.compile(r"^(#{1,6})\s+(.*)$")

# Walk: collect sections w/ word counts
sections = []
current = None
for i, ln in enumerate(lines, 1):
    m = heading_re.match(ln)
    if m:
        if current is not None:
            current["end"] = i - 1
            sections.append(current)
        level = len(m.group(1))
        title = m.group(2).strip()
        current = {"level": level, "title": title, "start": i, "end": len(lines), "body": []}
        continue
    if current is not None:
        current["body"].append(ln)
if current is not None:
    sections.append(current)

def word_count(blob: str) -> int:
    return len(re.findall(r"\b\w+\b", blob))

# Tables: find every line that's a table row, group consecutive rows into tables,
# track section ownership, and count long-cell rows.
tables = []
i = 0
while i < len(lines):
    ln = lines[i].strip()
    if ln.startswith("|") and ln.count("|") >= 2 and not re.match(r"^\|[\s\-:|]+\|$", ln):
        # Start of table; first line is header
        start_line = i + 1
        rows = [lines[i]]
        i += 1
        # Skip separator
        if i < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i].strip()):
            rows.append(lines[i])
            i += 1
        # Body rows
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(lines[i])
            i += 1
        # Find owning section
        section_title = "(unknown)"
        for s in sections:
            if s["start"] <= start_line <= s["end"]:
                section_title = s["title"]
                break
        # Compute longest cell across all rows
        max_cell = 0
        long_cells = 0
        very_long_cells = 0
        for r in rows:
            cells = [c.strip() for c in r.strip("|").split("|")]
            for c in cells:
                cl = len(c)
                if cl > max_cell:
                    max_cell = cl
                if cl > CELL_LONG_THRESHOLD:
                    long_cells += 1
                if cl > CELL_VERY_LONG_THRESHOLD:
                    very_long_cells += 1
        tables.append({
            "start_line": start_line,
            "section": section_title,
            "n_rows": len(rows) - 1,  # exclude separator
            "n_cols": len(rows[0].strip("|").split("|")),
            "max_cell_chars": max_cell,
            "long_cells": long_cells,
            "very_long_cells": very_long_cells,
            "header": rows[0].strip()[:200],
        })
    else:
        i += 1

# Long titles
long_titles = [s for s in sections if len(s["title"]) > 65]

# Build output
out = []
out.append("# v11.9.1 — appendix word counts + table formatting audit\n")

# === Appendix word counts ===
out.append("## Appendix word counts (cut candidates)\n")
out.append("Sorted by word count descending. Anything > 600 words is a cut candidate (redirect to repo).\n")
out.append("| § | Level | Title | Words | Cut candidate? |")
out.append("|---|---|---|---:|---|")
appendix_secs = [s for s in sections if s["level"] in (2, 3) and re.match(r"Appendix [A-Z]", s["title"])]
# Include subsections of Appendices too
appendix_subsecs = []
in_appendix = False
for s in sections:
    if s["level"] == 2 and re.match(r"Appendix [A-Z]", s["title"]):
        in_appendix = True
        appendix_subsecs.append(s)
    elif s["level"] == 2:
        in_appendix = False
    elif in_appendix and s["level"] == 3:
        appendix_subsecs.append(s)

for s in sorted(appendix_subsecs, key=lambda x: -word_count("\n".join(x["body"]))):
    wc = word_count("\n".join(s["body"]))
    cut_flag = ""
    if wc > 1500:
        cut_flag = "**STRONG cut candidate**"
    elif wc > 600:
        cut_flag = "cut candidate"
    elif wc > 250:
        cut_flag = "consider trim"
    out.append(f"| {('A' + str(s['level'] - 2) * 2) if s['level'] == 3 else 'A'} | H{s['level']} | {s['title']} | {wc} | {cut_flag} |")

# === Formatting: long-cell tables ===
out.append("\n---\n## Tables with very long cells (formatting issues)\n")
out.append(f"`max_cell_chars > {CELL_VERY_LONG_THRESHOLD}` = a single cell that becomes a 10-line block in Word.\n")
out.append(f"`max_cell_chars > {CELL_LONG_THRESHOLD}` = wraps awkwardly, fixable by widening that column or shortening the cell text.\n\n")
out.append("| L | Section | n_rows | n_cols | max_cell | long_cells | very_long | header preview |")
out.append("|---:|---|---:|---:|---:|---:|---:|---|")
for t in sorted(tables, key=lambda x: -x["max_cell_chars"]):
    if t["max_cell_chars"] < CELL_LONG_THRESHOLD:
        continue
    out.append(f"| L{t['start_line']} | {t['section'][:40]} | {t['n_rows']} | {t['n_cols']} | {t['max_cell_chars']} | {t['long_cells']} | {t['very_long_cells']} | `{t['header'][:80]}` |")

# === Long titles ===
out.append("\n---\n## Long heading titles (likely to wrap awkwardly)\n")
out.append(f"Titles > 65 chars often run onto two lines in Word.\n\n")
for s in long_titles:
    out.append(f"- L{s['start']} (H{s['level']}, {len(s['title'])} chars): {s['title']}")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"\nAppendix subsections (≥ 600 words): {sum(1 for s in appendix_subsecs if word_count(chr(10).join(s['body'])) > 600)}")
print(f"Tables with very long cells (> {CELL_VERY_LONG_THRESHOLD} chars): {sum(1 for t in tables if t['max_cell_chars'] > CELL_VERY_LONG_THRESHOLD)}")
print(f"Tables with long cells (> {CELL_LONG_THRESHOLD} chars): {sum(1 for t in tables if t['max_cell_chars'] > CELL_LONG_THRESHOLD)}")
print(f"Long titles (> 65 chars): {len(long_titles)}")
