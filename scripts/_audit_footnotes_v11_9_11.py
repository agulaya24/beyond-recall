"""Audit footnote lengths in v11.9.11."""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "docs" / "beyond_recall_v11_9_11_draft.md"

text = PAPER.read_text(encoding="utf-8")
defs = re.findall(r"^\[\^([a-z0-9-]+)\]:\s+(.+?)(?=\n\n|\n\[\^|\Z)", text, re.MULTILINE | re.DOTALL)
print(f"Total footnote definitions: {len(defs)}")
sorted_defs = sorted(defs, key=lambda d: -len(d[1]))
print("Top 30 longest footnotes:")
for name, body in sorted_defs[:30]:
    body_one_line = body.replace("\n", " ").replace("\r", " ")[:120]
    print(f"  [{name}] {len(body)}c: {body_one_line}")
