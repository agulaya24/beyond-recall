#!/usr/bin/env python3
"""Fix broken \hyperlink{...} references in beyond_recall_body.tex.

Pandoc generated link slugs prefixed with section numbers stripped of dots,
but the matching \hypertarget{...} slugs preserve dots and lack prefixes.
We rewrite the \hyperlink{...} side to match the existing \hypertarget side.
"""
import re
from pathlib import Path

BODY = Path(__file__).resolve().parents[1] / "build" / "beyond_recall_body.tex"

# Map: broken slug -> actual hypertarget slug.
RENAMES = {
    "13-what-we-found": "what-we-found",
    "7-future-work": "future-work",
    "73-specification-design-and-composition": "specification-design-and-composition",
    "8-data-code-and-reproducibility": "data-code-and-reproducibility",
    "appendix-a-predicate-vocabulary": "appendix-a.-predicate-vocabulary",
    "appendix-h-glossary": "appendix-h.-glossary",
}

text = BODY.read_text(encoding="utf-8")
total = 0
for old, new in RENAMES.items():
    pattern = r"\\hyperlink\{" + re.escape(old) + r"\}"
    repl = r"\\hyperlink{" + new + r"}"
    matches = len(re.findall(pattern, text))
    if matches:
        text = re.sub(pattern, repl, text)
        print(f"  {old} -> {new}: {matches} replacements")
        total += matches
    else:
        print(f"  {old}: not found (already fixed?)")

BODY.write_text(text, encoding="utf-8")
print(f"\nTotal replacements: {total}")
