"""Reorder cover + TOC + body in the v11.9.11 docx.

Default pandoc --toc places the Table of Contents at the very start of the
document, before the title. The intended ordering for the preprint is:

  Page 1: Cover (Title, masthead, abstract)
  Page 2: Table of Contents
  Page 3+: §1 onwards

This script moves the TOC SDT element from the start of the body to a
position after the existing abstract→§1 page break, and adds another page
break after the TOC so §1 starts on its own page.

Idempotent: detects whether the TOC is already in the desired position by
checking whether the first body element is the cover title heading.
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v12_1_draft.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{" + W_NS + "}"


def main() -> int:
    from lxml import etree

    print(f"Opening {DOCX.name}...")
    with zipfile.ZipFile(str(DOCX)) as zin:
        names = zin.namelist()
        files = {n: zin.read(n) for n in names}

    doc_xml = files["word/document.xml"]
    tree = etree.fromstring(doc_xml)
    body = tree.find(W + "body")
    if body is None:
        print("ERROR: no <w:body> found")
        return 1

    # Step 1: locate the TOC SDT (table of contents structured document tag)
    toc_sdt = None
    for child in body:
        if child.tag == W + "sdt":
            # Check if this SDT contains a TOC docPartGallery
            sdt_pr = child.find(W + "sdtPr")
            if sdt_pr is not None:
                doc_part = sdt_pr.find(W + "docPartObj")
                if doc_part is not None:
                    gallery = doc_part.find(W + "docPartGallery")
                    if gallery is not None and gallery.get(W + "val") == "Table of Contents":
                        toc_sdt = child
                        break

    if toc_sdt is None:
        print("No TOC SDT found — assuming already reordered or never present.")
        return 0

    # Idempotency check: if the TOC SDT is NOT at the start of the body,
    # assume reorder has already been applied.
    body_children = list(body)
    first_non_sdt = next((c for c in body_children if c.tag != W + "sdt"), None)
    first_idx_of_sdt = body_children.index(toc_sdt)
    first_meaningful_idx = 0
    if first_idx_of_sdt > 2:
        # TOC is not at start; reordered already
        print(f"TOC SDT at index {first_idx_of_sdt} — already reordered. No action.")
        return 0

    # Step 2: locate the existing abstract-end page break.
    # We look for a <w:p> that contains a <w:br w:type="page"/> as its first
    # meaningful child after pPr. This is the raw-OOXML page break we added
    # in the markdown source.
    existing_pagebreak_p = None
    for i, child in enumerate(body_children):
        if child.tag != W + "p":
            continue
        # Look for a w:br with w:type="page" anywhere in this paragraph
        for br in child.iter(W + "br"):
            if br.get(W + "type") == "page":
                existing_pagebreak_p = child
                existing_pagebreak_idx = i
                break
        if existing_pagebreak_p is not None:
            break

    if existing_pagebreak_p is None:
        print("ERROR: no existing page break found. Cannot determine TOC insertion point.")
        return 1

    print(f"Found TOC SDT at body[{first_idx_of_sdt}]; existing page break at body[{existing_pagebreak_idx}].")

    # Step 3: detach TOC SDT from its current position
    body.remove(toc_sdt)

    # Step 4: re-locate the page break (index may have shifted now)
    body_children = list(body)
    existing_pagebreak_idx = body_children.index(existing_pagebreak_p)

    # Step 5: Insert TOC immediately AFTER the existing page break.
    # The existing page break separates abstract from §1.
    # Resulting order:
    #   ... abstract ...
    #   [existing page break]   ← Page 1 ends, Page 2 starts
    #   [TOC SDT]
    #   [NEW page break]        ← Page 2 ends, Page 3 starts
    #   §1. Introduction
    insert_pos = existing_pagebreak_idx + 1
    body.insert(insert_pos, toc_sdt)

    # Step 6: Build a new page break paragraph and insert after the TOC
    pagebreak_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:r><w:br w:type="page"/></w:r></w:p>'
    )
    new_pagebreak = etree.fromstring(pagebreak_xml)
    body.insert(insert_pos + 1, new_pagebreak)

    print(f"Moved TOC to body[{insert_pos}]; inserted new page break at body[{insert_pos + 1}].")

    # Serialize and repack
    new_doc_xml = etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    files["word/document.xml"] = new_doc_xml

    tmp_path = DOCX.with_suffix(".docx.tmp")
    with zipfile.ZipFile(str(tmp_path), "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, files[n])
    shutil.move(str(tmp_path), str(DOCX))
    print(f"Saved {DOCX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
