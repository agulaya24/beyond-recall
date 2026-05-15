"""List all <w:del> content in v11.8 docx — paragraph-by-paragraph.

For each paragraph that contains any <w:del>, emit:
  - paragraph index
  - the deleted text spans (joined)
  - surrounding context (the surviving text in that paragraph)

Use this to verify all stricken content is removed from v11.9.1.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v11_8_draft_with_figures.docx"
OUT = REPO / "docs" / "research" / "v11_8_tracked_deletions_20260509.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def collect_text(el, suppress_del: bool) -> str:
    parts = []
    for child in el.iter():
        if child.tag != W + "t":
            continue
        # Walk ancestors to check if inside w:del
        in_del = False
        a = child
        # ElementTree has no parent map; build one once if needed.
        # Cheap approach: check tag chain via the parent_map
        ancestor = parent_map.get(child)
        while ancestor is not None:
            if ancestor.tag == W + "del":
                in_del = True
                break
            ancestor = parent_map.get(ancestor)
        if suppress_del and in_del:
            continue
        if (not suppress_del) and not in_del:
            continue
        parts.append(child.text or "")
    return "".join(parts)


with zipfile.ZipFile(DOCX) as z:
    with z.open("word/document.xml") as f:
        root = ET.parse(f).getroot()

parent_map = {c: p for p in root.iter() for c in p}

body = root.find(W + "body")
paragraphs = body.findall(W + "p")
print(f"Total paragraphs: {len(paragraphs)}")

records = []
for idx, p in enumerate(paragraphs):
    deletions = list(p.iter(W + "del"))
    if not deletions:
        continue
    # Collect deleted text from all w:del subtrees (uses w:delText)
    deleted_pieces = []
    for d in deletions:
        for t in d.iter(W + "delText"):
            deleted_pieces.append(t.text or "")
        for t in d.iter(W + "t"):
            deleted_pieces.append(t.text or "")
    deleted_text = "".join(deleted_pieces).strip()
    if not deleted_text:
        continue
    # Surviving text in this paragraph (skip w:del subtrees)
    surviving_pieces = []
    def walk(el):
        for child in el:
            if child.tag == W + "del":
                continue
            if child.tag == W + "t":
                surviving_pieces.append(child.text or "")
            else:
                walk(child)
    walk(p)
    surviving_text = "".join(surviving_pieces).strip()
    records.append({
        "idx": idx,
        "deleted": deleted_text,
        "surviving": surviving_text,
    })

print(f"Paragraphs with deletions: {len(records)}")

lines = [f"# v11.8 docx tracked deletions\n"]
lines.append(f"Total paragraphs with `<w:del>` content: **{len(records)}**\n")
lines.append("Each entry shows the deleted text span and the surviving text of that paragraph.\n")
lines.append("---\n")

for r in records:
    lines.append(f"## Paragraph {r['idx']}\n")
    lines.append(f"**Deleted:** {r['deleted']}\n")
    if r['surviving']:
        lines.append(f"**Surviving:** {r['surviving']}\n")
    else:
        lines.append(f"**Surviving:** *(empty — entire paragraph deleted)*\n")
    lines.append("---\n")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}")
