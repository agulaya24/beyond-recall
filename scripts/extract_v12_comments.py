"""Extract every comment Aarik left on beyond_recall_v12_draft.docx, paired
with the anchored text and the surrounding paragraph for context.

Output: docs/reviews/v12_aarik_comments_20260513.md

Each comment is recorded independently with:
  - Comment ID (Word's internal id)
  - Order of appearance in the document (#N)
  - Section anchor (best-guess: nearest preceding Heading 1/2/3)
  - Anchored text (between commentRangeStart and commentRangeEnd)
  - Surrounding paragraph (the paragraph containing the anchor)
  - Comment text (verbatim, no truncation)
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v12_draft.docx"
OUT = REPO / "docs" / "reviews" / "v12_aarik_comments_20260513.md"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{" + W_NS + "}"


def main() -> int:
    from lxml import etree

    with zipfile.ZipFile(str(DOCX)) as z:
        comments_xml = z.read("word/comments.xml")
        doc_xml = z.read("word/document.xml")

    # --- Parse comments.xml into a dict by id ---
    ctree = etree.fromstring(comments_xml)
    comments_by_id: dict[str, dict] = {}
    for c in ctree.findall(W + "comment"):
        cid = c.get(W + "id")
        author = c.get(W + "author") or ""
        date = c.get(W + "date") or ""
        paras = []
        for p in c.iter(W + "p"):
            ptext = "".join((tt.text or "") for tt in p.iter(W + "t"))
            paras.append(ptext)
        full = "\n".join(paras).strip()
        comments_by_id[cid] = {
            "id": cid,
            "author": author,
            "date": date,
            "text": full,
        }

    # --- Walk document.xml: maintain doc-order list of comments, anchor text,
    #     surrounding paragraph, and nearest preceding heading. ---
    dtree = etree.fromstring(doc_xml)
    body = dtree.find(W + "body")

    def para_text(p) -> str:
        return "".join((t.text or "") for t in p.iter(W + "t")).strip()

    def heading_level(p) -> tuple[int, str] | None:
        pPr = p.find(W + "pPr")
        if pPr is None:
            return None
        pStyle = pPr.find(W + "pStyle")
        if pStyle is None:
            return None
        val = pStyle.get(W + "val") or ""
        if val == "Heading1":
            return (1, para_text(p))
        if val == "Heading2":
            return (2, para_text(p))
        if val == "Heading3":
            return (3, para_text(p))
        if val == "AppendixSubhead":
            return (3, para_text(p))
        return None

    # Build flat list of paragraphs with their text + heading info.
    # We also remember, for each <w:commentRangeStart>, the index of its
    # containing paragraph and the surrounding heading chain.
    all_paras = list(body.iter(W + "p"))

    # Index map: w:commentRangeStart id -> (para_idx, start_node)
    starts: dict[str, tuple[int, object]] = {}
    ends: dict[str, tuple[int, object]] = {}
    for i, p in enumerate(all_paras):
        for el in p.iter(W + "commentRangeStart"):
            cid = el.get(W + "id")
            starts.setdefault(cid, (i, el))
        for el in p.iter(W + "commentRangeEnd"):
            cid = el.get(W + "id")
            ends.setdefault(cid, (i, el))

    # Compute nearest preceding H1/H2/H3 for each paragraph index.
    heading_chain_at: list[tuple[str, str, str]] = []
    cur_h1 = cur_h2 = cur_h3 = ""
    for p in all_paras:
        hd = heading_level(p)
        if hd is not None:
            lvl, txt = hd
            if lvl == 1:
                cur_h1, cur_h2, cur_h3 = txt, "", ""
            elif lvl == 2:
                cur_h2, cur_h3 = txt, ""
            elif lvl == 3:
                cur_h3 = txt
        heading_chain_at.append((cur_h1, cur_h2, cur_h3))

    # For each commentReference in document order, build the record.
    # commentReference (not commentRangeStart) is what marks the anchor point;
    # commentRangeStart/End delimit the anchored text. Aarik's comments mostly
    # use the range markers (selection-anchored). We use the range for the
    # anchored-text excerpt; commentReference's containing paragraph is the
    # surrounding context.
    refs: list[tuple[str, int]] = []  # (cid, para_idx)
    for i, p in enumerate(all_paras):
        for el in p.iter(W + "commentReference"):
            cid = el.get(W + "id")
            refs.append((cid, i))

    def extract_anchored_text(cid: str) -> str:
        if cid not in starts or cid not in ends:
            return ""
        start_para_idx, start_node = starts[cid]
        end_para_idx, end_node = ends[cid]
        # Walk all <w:t> elements between start_node and end_node (across paragraphs).
        capture = False
        out_chunks: list[str] = []
        all_descendants = list(body.iter())
        for el in all_descendants:
            if el is start_node:
                capture = True
                continue
            if el is end_node:
                break
            if capture and el.tag == W + "t" and el.text:
                out_chunks.append(el.text)
        return "".join(out_chunks).strip()

    # --- Write the markdown report ---
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# v12 Aarik comments — verbatim extraction")
    lines.append("")
    lines.append(f"Source: `{DOCX.name}`. Total comments: {len(refs)}.")
    lines.append("")
    lines.append("Each entry is a single comment recorded independently. Entries are")
    lines.append("listed in document order. Tags can be applied per entry after review.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for n, (cid, p_idx) in enumerate(refs, 1):
        c = comments_by_id.get(cid)
        if c is None:
            continue
        h1, h2, h3 = heading_chain_at[p_idx]
        surrounding = para_text(all_paras[p_idx])
        anchored = extract_anchored_text(cid)

        lines.append(f"## C{n:03d}  (comment-id {cid})")
        lines.append("")
        chain = " › ".join([x for x in (h1, h2, h3) if x]) or "(top of document)"
        lines.append(f"**Section:** {chain}")
        lines.append("")
        if anchored:
            short = anchored if len(anchored) <= 600 else anchored[:600] + " […]"
            lines.append(f"**Anchored text:** {short}")
            lines.append("")
        if surrounding and surrounding != anchored:
            short_s = surrounding if len(surrounding) <= 800 else surrounding[:800] + " […]"
            lines.append(f"**Surrounding paragraph:** {short_s}")
            lines.append("")
        lines.append(f"**Comment:** {c['text']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(refs)} comments to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
