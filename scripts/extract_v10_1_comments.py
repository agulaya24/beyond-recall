"""
Extract every comment from beyond_recall_v10_1_draft.docx with its anchored text
and surrounding section context, for mechanical side-by-side review.

Output: docs/reviews/v11_comments_extracted_<date>.md (numbered list, one entry per
comment with author, date, comment body, anchored excerpt, nearest section heading).
"""
import re
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v10_1_draft.docx"
OUT = REPO / "docs" / "reviews" / f"v11_comments_extracted_{datetime.now():%Y%m%d}.md"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def text_of(elem):
    """Concatenate w:t descendants. Preserve order; ignore tracked-change deletions."""
    parts = []
    for t in elem.iter(f"{{{W}}}t"):
        parts.append(t.text or "")
    return "".join(parts)


def is_heading(p):
    """Return heading text + level if paragraph is a heading, else None."""
    pStyle = p.find(f"{{{W}}}pPr/{{{W}}}pStyle")
    if pStyle is None:
        return None
    val = pStyle.get(f"{{{W}}}val", "")
    m = re.match(r"Heading(\d)", val)
    if not m:
        return None
    level = int(m.group(1))
    return level, text_of(p)


def main():
    with zipfile.ZipFile(DOCX, "r") as z:
        comments_xml = z.read("word/comments.xml")
        document_xml = z.read("word/document.xml")

    # Comments: id -> (author, date, body)
    comments = {}
    croot = ET.fromstring(comments_xml)
    for c in croot.iter(f"{{{W}}}comment"):
        cid = c.get(f"{{{W}}}id")
        author = c.get(f"{{{W}}}author", "?")
        date = c.get(f"{{{W}}}date", "")
        body = "\n".join(text_of(p) for p in c.iter(f"{{{W}}}p")).strip()
        comments[cid] = {"author": author, "date": date, "body": body}

    # Walk body paragraphs, track section heading + commentRange anchors.
    droot = ET.fromstring(document_xml)
    body = droot.find(f"{{{W}}}body")
    if body is None:
        raise SystemExit("no body found")

    paragraphs = list(body.findall(f"{{{W}}}p"))

    # Build per-comment: anchor_text (concat of runs between RangeStart/End across paragraphs),
    # section path (last seen H1/H2/H3/H4), paragraph index of start.
    anchors = {cid: {"text_runs": [], "section": [None, None, None, None],
                     "para_idx": None, "para_text": ""}
               for cid in comments}
    open_ids = set()
    section = [None, None, None, None]  # H1..H4

    for idx, p in enumerate(paragraphs):
        h = is_heading(p)
        if h is not None:
            level, htxt = h
            if 1 <= level <= 4:
                section[level - 1] = htxt
                # clear deeper levels
                for j in range(level, 4):
                    section[j] = None

        para_text = text_of(p)
        # Walk children in order to capture commentRangeStart / End and runs.
        # We use iter to find anchor markers within this paragraph.
        for elem in p.iter():
            tag = elem.tag.split("}", 1)[-1]
            if tag == "commentRangeStart":
                cid = elem.get(f"{{{W}}}id")
                if cid in anchors:
                    open_ids.add(cid)
                    if anchors[cid]["para_idx"] is None:
                        anchors[cid]["para_idx"] = idx
                        anchors[cid]["section"] = list(section)
                        anchors[cid]["para_text"] = para_text
            elif tag == "commentRangeEnd":
                cid = elem.get(f"{{{W}}}id")
                if cid in open_ids:
                    open_ids.discard(cid)
            elif tag == "commentReference":
                # Word stores the inline reference marker; sometimes a comment is
                # a "point" comment with no Range Start/End. Treat as anchored at
                # this paragraph if not already anchored.
                cid = elem.get(f"{{{W}}}id")
                if cid in anchors and anchors[cid]["para_idx"] is None:
                    anchors[cid]["para_idx"] = idx
                    anchors[cid]["section"] = list(section)
                    anchors[cid]["para_text"] = para_text
            elif tag == "t" and open_ids:
                t = elem.text or ""
                for cid in open_ids:
                    anchors[cid]["text_runs"].append(t)

    # Compose Markdown report.
    rows = []
    for cid, c in comments.items():
        a = anchors[cid]
        anchor_text = "".join(a["text_runs"]).strip()
        if not anchor_text:
            anchor_text = a["para_text"].strip()
        section_path = " > ".join([s for s in a["section"] if s]) or "(top of document)"
        rows.append({
            "cid": cid,
            "para_idx": a["para_idx"] if a["para_idx"] is not None else 10**9,
            "section": section_path,
            "author": c["author"],
            "date": c["date"],
            "body": c["body"],
            "anchor": anchor_text,
            "para_text": a["para_text"].strip(),
        })

    rows.sort(key=lambda r: r["para_idx"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        f.write(f"# v11 Comment Extraction — Beyond Recall v10.1\n\n")
        f.write(f"_Source: `docs/beyond_recall_v10_1_draft.docx`. "
                f"Generated {datetime.now():%Y-%m-%d %H:%M}._\n\n")
        f.write(f"**Total comments:** {len(rows)}\n\n")
        f.write("Each entry below is one comment, ordered by appearance in the document. "
                "Status fields are blank pending review.\n\n")
        f.write("---\n\n")
        for n, r in enumerate(rows, start=1):
            f.write(f"## Comment {n} (id={r['cid']})\n\n")
            f.write(f"**Section:** {r['section']}\n\n")
            f.write(f"**Author:** {r['author']}  \n")
            f.write(f"**Date:** {r['date']}\n\n")
            f.write(f"**Comment body:**\n\n")
            for line in r["body"].splitlines() or [""]:
                f.write(f"> {line}\n")
            f.write("\n")
            f.write(f"**Anchored text:**\n\n")
            anchor = r["anchor"]
            if len(anchor) > 800:
                anchor = anchor[:800] + " [...]"
            f.write(f"```\n{anchor}\n```\n\n")
            if r["anchor"] != r["para_text"] and r["para_text"]:
                ptx = r["para_text"]
                if len(ptx) > 1200:
                    ptx = ptx[:1200] + " [...]"
                f.write(f"**Surrounding paragraph (full):**\n\n")
                f.write(f"> {ptx}\n\n")
            f.write(f"**Status:** pending review  \n")
            f.write(f"**Resolution:** _(to be filled in during review)_\n\n")
            f.write("---\n\n")

    print(f"Extracted {len(rows)} comments to {OUT}")


if __name__ == "__main__":
    main()
