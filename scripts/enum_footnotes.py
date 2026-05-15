#!/usr/bin/env python3
"""Enumerate every footnote in body.tex with index, line number, length, preview."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

BODY = Path(__file__).resolve().parents[1] / "build" / "beyond_recall_body.tex"
text = BODY.read_text(encoding="utf-8")

# Confirm backslashes exist
print(f"file size: {len(text)} chars")
print(f"backslash count: {text.count(chr(92))}")
print(f"chars 0-200: {text[:200]!r}")
print()

# Find every \footnote{ and \footnotetext{ via literal substring search
markers = []
i = 0
needle1 = chr(92) + "footnote{"
needle2 = chr(92) + "footnotetext{"
while True:
    p1 = text.find(needle1, i)
    p2 = text.find(needle2, i)
    candidates = [(p1, False, needle1), (p2, True, needle2)]
    candidates = [c for c in candidates if c[0] != -1]
    if not candidates:
        break
    candidates.sort()
    pos, is_ft, needle = candidates[0]
    open_pos = pos + len(needle)
    depth = 1
    j = open_pos
    while j < len(text) and depth > 0:
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        j += 1
    body = text[open_pos:j-1]
    markers.append((pos, len(body), body, is_ft))
    i = j

print(f"Found {len(markers)} footnotes (incl. footnotetext)")
print()

# Print all in order
for idx, (off, ln, body, ft_only) in enumerate(markers, 1):
    line_no = text[:off].count("\n") + 1
    one = " ".join(body.split())[:100]
    marker = "FT" if ft_only else "  "
    print(f"#{idx:3d}  L{line_no:5d}  {ln:5d}  {marker}  {one}")
