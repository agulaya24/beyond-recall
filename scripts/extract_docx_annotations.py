"""Extract comments, highlights, and tracked changes from the reviewed .docx.

Usage:
    python extract_docx_annotations.py [path_to_docx]
    (defaults to docs/beyond_recall_review.docx)

Output: docs/reviews/s114_word_annotations.md
  - every comment with its anchored text and author
  - every highlight with its text
  - every tracked insertion and deletion
  - all grouped by approximate paragraph / section
"""

from pathlib import Path
import sys
import zipfile
import re
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DOCX = REPO / "docs" / "beyond_recall_review.docx"
OUT = REPO / "docs" / "reviews" / "s114_word_annotations.md"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def text_of(elem):
    """Gather visible text from a <w:p> or <w:r>, ignoring deletions (<w:del>)."""
    parts = []
    for t in elem.iter(f"{{{NS['w']}}}t"):
        # Skip if inside a <w:del> (deleted text)
        parent = t
        is_deleted = False
        # Walk up to see if any ancestor is w:del
        for anc in elem.iter():
            if t in list(anc):
                if anc.tag == f"{{{NS['w']}}}del":
                    is_deleted = True
                break
        if not is_deleted:
            parts.append(t.text or "")
    return "".join(parts)


def simple_text(elem):
    """All <w:t> text concatenated, including from <w:ins> and <w:del>."""
    return "".join((t.text or "") for t in elem.iter(f"{{{NS['w']}}}t"))


def iter_paragraphs(doc_root):
    """Yield every <w:p> in document order."""
    body = doc_root.find(f"{{{NS['w']}}}body")
    if body is None:
        return
    for p in body.iter(f"{{{NS['w']}}}p"):
        yield p


def extract_comments(zf):
    """Return dict: comment_id -> {author, date, text}."""
    try:
        data = zf.read("word/comments.xml").decode("utf-8")
    except KeyError:
        return {}
    root = ET.fromstring(data)
    out = {}
    for c in root.findall(f"{{{NS['w']}}}comment"):
        cid = c.get(f"{{{NS['w']}}}id")
        author = c.get(f"{{{NS['w']}}}author", "")
        date = c.get(f"{{{NS['w']}}}date", "")
        text = "".join((t.text or "") for t in c.iter(f"{{{NS['w']}}}t"))
        out[cid] = {"author": author, "date": date, "text": text.strip()}
    return out


def extract_annotations(docx_path: Path):
    with zipfile.ZipFile(docx_path, "r") as zf:
        doc_xml = zf.read("word/document.xml").decode("utf-8")
        comments = extract_comments(zf)

    root = ET.fromstring(doc_xml)

    # Walk paragraphs, collecting annotations with their paragraph text for context.
    current_section = "(before first heading)"
    section_counter = 0
    paragraph_counter = 0
    results = []

    for p in iter_paragraphs(root):
        paragraph_counter += 1

        # Heading detection via pStyle
        pPr = p.find(f"{{{NS['w']}}}pPr")
        style_name = None
        if pPr is not None:
            pStyle = pPr.find(f"{{{NS['w']}}}pStyle")
            if pStyle is not None:
                style_name = pStyle.get(f"{{{NS['w']}}}val", "")
        full_text = simple_text(p).strip()
        if style_name and style_name.startswith("Heading") and full_text:
            section_counter += 1
            current_section = f"{full_text} (style: {style_name})"

        para_text = full_text[:300]

        # Comment references — each <w:commentRangeStart>/<w:commentReference>
        for cref in p.iter(f"{{{NS['w']}}}commentReference"):
            cid = cref.get(f"{{{NS['w']}}}id")
            if cid and cid in comments:
                c = comments[cid]
                # Find the anchor text: everything between commentRangeStart and commentRangeEnd in the body
                anchor = anchor_text_for_comment(root, cid)
                results.append({
                    "kind": "comment",
                    "section": current_section,
                    "paragraph_context": para_text,
                    "anchor": anchor[:300],
                    "author": c["author"],
                    "date": c["date"],
                    "text": c["text"],
                })

        # Highlights — runs with <w:highlight> in rPr
        for r in p.iter(f"{{{NS['w']}}}r"):
            rPr = r.find(f"{{{NS['w']}}}rPr")
            if rPr is None:
                continue
            hl = rPr.find(f"{{{NS['w']}}}highlight")
            if hl is None:
                continue
            color = hl.get(f"{{{NS['w']}}}val", "yellow")
            run_text = "".join((t.text or "") for t in r.iter(f"{{{NS['w']}}}t"))
            if run_text.strip():
                results.append({
                    "kind": "highlight",
                    "section": current_section,
                    "paragraph_context": para_text,
                    "color": color,
                    "text": run_text.strip(),
                })

        # Tracked insertions
        for ins in p.iter(f"{{{NS['w']}}}ins"):
            author = ins.get(f"{{{NS['w']}}}author", "")
            date = ins.get(f"{{{NS['w']}}}date", "")
            ins_text = "".join((t.text or "") for t in ins.iter(f"{{{NS['w']}}}t"))
            if ins_text.strip():
                results.append({
                    "kind": "tracked_insert",
                    "section": current_section,
                    "paragraph_context": para_text,
                    "author": author,
                    "date": date,
                    "text": ins_text.strip(),
                })

        # Tracked deletions
        for dele in p.iter(f"{{{NS['w']}}}del"):
            author = dele.get(f"{{{NS['w']}}}author", "")
            date = dele.get(f"{{{NS['w']}}}date", "")
            del_text = "".join((t.text or "") for t in dele.iter(f"{{{NS['w']}}}delText"))
            if del_text.strip():
                results.append({
                    "kind": "tracked_delete",
                    "section": current_section,
                    "paragraph_context": para_text,
                    "author": author,
                    "date": date,
                    "text": del_text.strip(),
                })

    return results


def anchor_text_for_comment(root, cid):
    """Gather the text between <w:commentRangeStart w:id=cid> and <w:commentRangeEnd w:id=cid>."""
    collecting = False
    parts = []
    body = root.find(f"{{{NS['w']}}}body")
    if body is None:
        return ""
    for elem in body.iter():
        tag = elem.tag
        if tag == f"{{{NS['w']}}}commentRangeStart" and elem.get(f"{{{NS['w']}}}id") == cid:
            collecting = True
            continue
        if tag == f"{{{NS['w']}}}commentRangeEnd" and elem.get(f"{{{NS['w']}}}id") == cid:
            collecting = False
            break
        if collecting and tag == f"{{{NS['w']}}}t":
            parts.append(elem.text or "")
    return "".join(parts).strip()


def write_report(results, docx_path):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S114 Word-based review annotations",
        "",
        f"Source: `{docx_path}`",
        f"Extracted: {len(results)} annotations",
        "",
        "---",
        "",
    ]
    by_section = {}
    for r in results:
        by_section.setdefault(r["section"], []).append(r)

    for section, items in by_section.items():
        lines.append(f"## {section}")
        lines.append("")
        for r in items:
            kind = r["kind"]
            lines.append(f"### {kind}")
            if kind == "comment":
                lines.append(f"**Author:** {r['author']}  ")
                lines.append(f"**Anchor:** {r['anchor']}")
                lines.append("")
                lines.append(f"**Comment:** {r['text']}")
            elif kind == "highlight":
                lines.append(f"**Color:** {r['color']}  ")
                lines.append(f"**Highlighted text:** {r['text']}")
            elif kind in ("tracked_insert", "tracked_delete"):
                lines.append(f"**Author:** {r['author']}  ")
                lines.append(f"**Text:** {r['text']}")
            lines.append("")
            lines.append(f"*Paragraph context:* {r['paragraph_context']}")
            lines.append("")
            lines.append("---")
            lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    return OUT


def main():
    docx = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DOCX
    if not docx.exists():
        print(f"Not found: {docx}")
        sys.exit(1)
    results = extract_annotations(docx)
    out = write_report(results, docx)
    print(f"Annotations: {len(results)}")
    print(f"Wrote: {out}")

    # Summary counts
    kinds = {}
    for r in results:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    for k, n in sorted(kinds.items()):
        print(f"  {k}: {n}")


if __name__ == "__main__":
    main()
