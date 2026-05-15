"""Move heading bold from direct run formatting onto the heading STYLE.

C001 (2026-05-14): the table of contents renders the section numbers ("x.x")
and entry text in bold. Root cause: pandoc emits every Heading1/2/3 paragraph
with bold applied as *direct run formatting* (`<w:b>` on each run's rPr), while
the Heading styles themselves carry no bold. When Word builds the TOC field, it
copies the heading text's *direct* character formatting into each TOC entry, so
the bold rides along even though the TOC2 / TOC3 styles are normal weight.

Fix: relocate the bold. Add `<w:b>` + `<w:bCs>` to the Heading1/2/3 style
definitions in styles.xml, then strip the direct `<w:b>` / `<w:bCs>` from the
runs inside Heading1/2/3 paragraphs in document.xml. Net effect:

  - Body headings stay bold (now via the paragraph style, not direct runs).
  - The TOC field, copying only direct character formatting (none now), renders
    each entry at its TOC-level style weight: TOC1 bold, TOC2 / TOC3+ normal.

Idempotent. Run after `font_fix_v12_20260511.py` (which sweeps run sizes) and
before `postprocess_toc_font_v12_20260512.py`.
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

HEADING_STYLES = {"Heading1", "Heading2", "Heading3"}


def main() -> int:
    from lxml import etree

    if not DOCX.exists():
        print(f"ERROR: {DOCX} not found")
        return 1

    print(f"Opening {DOCX.name}...")
    with zipfile.ZipFile(str(DOCX)) as zin:
        names = zin.namelist()
        files = {n: zin.read(n) for n in names}

    # --- Step 1: add bold to the Heading1/2/3 style definitions -------------
    styles_tree = etree.fromstring(files["word/styles.xml"])
    styles_bolded = 0
    for style in styles_tree.findall(W + "style"):
        sid = style.get(W + "styleId") or ""
        if sid not in HEADING_STYLES:
            continue
        rPr = style.find(W + "rPr")
        if rPr is None:
            rPr = etree.SubElement(style, W + "rPr")
        if rPr.find(W + "b") is None:
            etree.SubElement(rPr, W + "b")
        if rPr.find(W + "bCs") is None:
            etree.SubElement(rPr, W + "bCs")
        styles_bolded += 1
    print(f"  Heading styles given bold: {styles_bolded}")

    # --- Step 2: strip direct bold from runs inside heading paragraphs ------
    doc_tree = etree.fromstring(files["word/document.xml"])
    body = doc_tree.find(W + "body")
    if body is None:
        print("ERROR: no <w:body> found")
        return 1

    runs_stripped = 0
    headings_seen = 0
    for p in body.iter(W + "p"):
        pPr = p.find(W + "pPr")
        if pPr is None:
            continue
        pStyle = pPr.find(W + "pStyle")
        if pStyle is None:
            continue
        if (pStyle.get(W + "val") or "") not in HEADING_STYLES:
            continue
        headings_seen += 1
        for r in p.findall(W + "r"):
            rPr = r.find(W + "rPr")
            if rPr is None:
                continue
            b = rPr.find(W + "b")
            if b is not None:
                rPr.remove(b)
                runs_stripped += 1
            bCs = rPr.find(W + "bCs")
            if bCs is not None:
                rPr.remove(bCs)

    print(f"  Heading paragraphs processed: {headings_seen}")
    print(f"  Direct <w:b> runs stripped:   {runs_stripped}")

    files["word/styles.xml"] = etree.tostring(
        styles_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    files["word/document.xml"] = etree.tostring(
        doc_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    tmp_path = DOCX.with_suffix(".docx.tmp")
    with zipfile.ZipFile(str(tmp_path), "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, files[n])
    shutil.move(str(tmp_path), str(DOCX))
    print(f"Saved {DOCX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
