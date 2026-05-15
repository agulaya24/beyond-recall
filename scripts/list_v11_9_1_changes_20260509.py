"""List all w:ins / w:del tracked changes in v11.9.1 docx with surrounding context."""
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
DOCX = REPO / "docs" / "beyond_recall_v11_9_1_draft.docx"
OUT = REPO / "docs" / "research" / "v11_9_1_tracked_changes_20260509.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

with zipfile.ZipFile(DOCX) as z:
    with z.open("word/document.xml") as f:
        root = ET.parse(f).getroot()

body = root.find(W + "body")
paragraphs = body.findall(W + "p")

records = []
for idx, p in enumerate(paragraphs):
    insertions = list(p.iter(W + "ins"))
    deletions = list(p.iter(W + "del"))
    if not insertions and not deletions:
        continue

    ins_texts = []
    for ins in insertions:
        for t in ins.iter(W + "t"):
            ins_texts.append(t.text or "")
    inserted = "".join(ins_texts).strip()

    del_texts = []
    for d in deletions:
        for t in d.iter(W + "delText"):
            del_texts.append(t.text or "")
        for t in d.iter(W + "t"):
            del_texts.append(t.text or "")
    deleted = "".join(del_texts).strip()

    pieces = []
    def walk(el):
        for child in el:
            if child.tag == W + "del":
                continue
            if child.tag == W + "t":
                pieces.append(child.text or "")
            else:
                walk(child)
    walk(p)
    surviving = "".join(pieces).strip()

    records.append({
        "idx": idx,
        "inserted": inserted,
        "deleted": deleted,
        "surviving": surviving,
    })

print(f"Paragraphs with tracked changes: {len(records)}")

lines = [f"# v11.9.1 docx tracked changes\n"]
lines.append(f"Total paragraphs with tracked changes: **{len(records)}**\n")
lines.append("---\n")

for i, r in enumerate(records, 1):
    lines.append(f"## Change {i} (paragraph {r['idx']})")
    if r['inserted']:
        lines.append(f"**Inserted:** {r['inserted']}")
    if r['deleted']:
        lines.append(f"**Deleted:** {r['deleted']}")
    lines.append(f"**Paragraph (post-accept):** {r['surviving']}")
    lines.append("")
    lines.append("---")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}")
