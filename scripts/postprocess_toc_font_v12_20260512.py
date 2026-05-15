"""Shrink + restyle the table-of-contents in the v12 docx with level hierarchy.

Aarik wants the TOC dramatically smaller than body, with a visual hierarchy:

  - Top-level sections (TOC1 — "1. Introduction", "2. Methods", ...): BOLD
  - Second-level (TOC2 — "4.1", "4.2", ...): normal weight
  - Third-level+ (TOC3, TOC4 — "4.1.1", examples): ITALIC

Base font: 7pt (was 8pt). Times New Roman for consistency with body.

Approach: find the TOC SDT structured-document-tag in word/document.xml,
walk every paragraph, read its pStyle val to determine level, then walk
every <w:r> inside that paragraph and force the appropriate rPr.

Idempotent.

Run after `font_fix_v12_20260511.py` (which would otherwise set everything
to 11pt) and before any further docx post-processing.
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

TOC_FONT = "Times New Roman"
TOC_PT_HALF = 18   # 9pt expressed as half-points
TOC_PT_DISPLAY = 9


def detect_toc_level(p) -> int:
    """Return the TOC level (1, 2, 3, ...) for a paragraph based on pStyle.

    Pandoc emits pStyle val like "TOC1", "TOC2", "TOC3" (no space). Some
    reference docx variants use "TOC 1" with a space; handle both.
    Default to 2 (normal) if no recognizable TOC style is found.
    """
    pPr = p.find(W + "pPr")
    if pPr is None:
        return 2
    pStyle = pPr.find(W + "pStyle")
    if pStyle is None:
        return 2
    val = pStyle.get(W + "val") or ""
    val_clean = val.replace(" ", "").lower()
    if val_clean.startswith("toc"):
        suffix = val_clean[3:]
        if suffix.isdigit():
            return int(suffix)
    return 2


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

    # Step 1: locate the TOC SDT (docPartGallery val="Table of Contents")
    toc_sdt = None
    for child in body.iter(W + "sdt"):
        sdt_pr = child.find(W + "sdtPr")
        if sdt_pr is None:
            continue
        doc_part = sdt_pr.find(W + "docPartObj")
        if doc_part is None:
            continue
        gallery = doc_part.find(W + "docPartGallery")
        if gallery is not None and gallery.get(W + "val") == "Table of Contents":
            toc_sdt = child
            break

    if toc_sdt is None:
        print("No TOC SDT found — skipping.")
        return 0

    # Step 2: walk every TOC paragraph, determine its level, apply hierarchy.
    runs_set = 0
    paras_set = 0
    level_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    for p in toc_sdt.iter(W + "p"):
        level = detect_toc_level(p)
        level_counts[level] = level_counts.get(level, 0) + 1

        # Determine styling for this level
        bold = (level == 1)
        italic = (level >= 3)

        # Walk every run in this paragraph
        for r in p.iter(W + "r"):
            rPr = r.find(W + "rPr")
            if rPr is None:
                rPr = etree.SubElement(r, W + "rPr")
                r.remove(rPr)
                r.insert(0, rPr)

            # Font family
            rFonts = rPr.find(W + "rFonts")
            if rFonts is None:
                rFonts = etree.SubElement(rPr, W + "rFonts")
            rFonts.set(W + "ascii", TOC_FONT)
            rFonts.set(W + "hAnsi", TOC_FONT)
            rFonts.set(W + "cs", TOC_FONT)
            rFonts.set(W + "eastAsia", TOC_FONT)

            # Size
            sz = rPr.find(W + "sz")
            if sz is None:
                sz = etree.SubElement(rPr, W + "sz")
            sz.set(W + "val", str(TOC_PT_HALF))

            szCs = rPr.find(W + "szCs")
            if szCs is None:
                szCs = etree.SubElement(rPr, W + "szCs")
            szCs.set(W + "val", str(TOC_PT_HALF))

            # Bold (TOC1 only)
            existing_b = rPr.find(W + "b")
            existing_bCs = rPr.find(W + "bCs")
            if bold:
                if existing_b is None:
                    etree.SubElement(rPr, W + "b")
                if existing_bCs is None:
                    etree.SubElement(rPr, W + "bCs")
            else:
                if existing_b is not None:
                    rPr.remove(existing_b)
                if existing_bCs is not None:
                    rPr.remove(existing_bCs)

            # Italic (TOC3+)
            existing_i = rPr.find(W + "i")
            existing_iCs = rPr.find(W + "iCs")
            if italic:
                if existing_i is None:
                    etree.SubElement(rPr, W + "i")
                if existing_iCs is None:
                    etree.SubElement(rPr, W + "iCs")
            else:
                if existing_i is not None:
                    rPr.remove(existing_i)
                if existing_iCs is not None:
                    rPr.remove(existing_iCs)

            runs_set += 1

        # Paragraph-level rPr default (so future inserted runs inherit)
        pPr = p.find(W + "pPr")
        if pPr is None:
            pPr = etree.SubElement(p, W + "pPr")
            p.remove(pPr)
            p.insert(0, pPr)

        p_rPr = pPr.find(W + "rPr")
        if p_rPr is None:
            p_rPr = etree.SubElement(pPr, W + "rPr")

        sz = p_rPr.find(W + "sz")
        if sz is None:
            sz = etree.SubElement(p_rPr, W + "sz")
        sz.set(W + "val", str(TOC_PT_HALF))

        szCs = p_rPr.find(W + "szCs")
        if szCs is None:
            szCs = etree.SubElement(p_rPr, W + "szCs")
        szCs.set(W + "val", str(TOC_PT_HALF))

        # Mirror bold/italic at paragraph-default level too
        existing_b = p_rPr.find(W + "b")
        if bold and existing_b is None:
            etree.SubElement(p_rPr, W + "b")
        elif not bold and existing_b is not None:
            p_rPr.remove(existing_b)

        existing_i = p_rPr.find(W + "i")
        if italic and existing_i is None:
            etree.SubElement(p_rPr, W + "i")
        elif not italic and existing_i is not None:
            p_rPr.remove(existing_i)

        paras_set += 1

    print(f"  TOC paragraphs styled: {paras_set}")
    print(f"    TOC1 (bold):    {level_counts.get(1, 0)}")
    print(f"    TOC2 (normal):  {level_counts.get(2, 0)}")
    print(f"    TOC3 (italic):  {level_counts.get(3, 0)}")
    print(f"    TOC4 (italic):  {level_counts.get(4, 0)}")
    print(f"  TOC runs sized to {TOC_PT_DISPLAY}pt: {runs_set}")

    # Step 3: inject TOC1/TOC2/TOC3+ style definitions into styles.xml.
    # The TOC SDT contains only a placeholder; Word renders entries at
    # view-time using these style defs. Hierarchy: TOC1 bold, TOC2 normal,
    # TOC3+ italic; all 7pt Times New Roman.
    styles_xml = files["word/styles.xml"].decode("utf-8")
    styles_tree = etree.fromstring(files["word/styles.xml"])

    def make_toc_style(level: int) -> "etree._Element":
        bold = (level == 1)
        italic = (level >= 3)
        style_id = f"TOC{level}"
        style = etree.SubElement(styles_tree, W + "style")
        style.set(W + "type", "paragraph")
        style.set(W + "styleId", style_id)
        name = etree.SubElement(style, W + "name")
        name.set(W + "val", f"toc {level}")
        based = etree.SubElement(style, W + "basedOn")
        based.set(W + "val", "Normal")
        nxt = etree.SubElement(style, W + "next")
        nxt.set(W + "val", "Normal")
        etree.SubElement(style, W + "autoRedefine")
        ui = etree.SubElement(style, W + "uiPriority")
        ui.set(W + "val", "39")
        etree.SubElement(style, W + "unhideWhenUsed")

        pPr = etree.SubElement(style, W + "pPr")
        spacing = etree.SubElement(pPr, W + "spacing")
        spacing.set(W + "after", "60")
        # Indent third-level+ slightly to reinforce hierarchy
        if level >= 2:
            ind = etree.SubElement(pPr, W + "ind")
            ind.set(W + "left", str(220 * (level - 1)))

        rPr = etree.SubElement(style, W + "rPr")
        rFonts = etree.SubElement(rPr, W + "rFonts")
        rFonts.set(W + "ascii", TOC_FONT)
        rFonts.set(W + "hAnsi", TOC_FONT)
        rFonts.set(W + "cs", TOC_FONT)
        rFonts.set(W + "eastAsia", TOC_FONT)
        if bold:
            etree.SubElement(rPr, W + "b")
            etree.SubElement(rPr, W + "bCs")
        if italic:
            etree.SubElement(rPr, W + "i")
            etree.SubElement(rPr, W + "iCs")
        sz = etree.SubElement(rPr, W + "sz")
        sz.set(W + "val", str(TOC_PT_HALF))
        szCs = etree.SubElement(rPr, W + "szCs")
        szCs.set(W + "val", str(TOC_PT_HALF))
        return style

    # Remove any existing TOC1..TOC5 styles before adding fresh ones (idempotent)
    for existing in styles_tree.findall(W + "style"):
        sid = existing.get(W + "styleId") or ""
        if sid in ("TOC1", "TOC2", "TOC3", "TOC4", "TOC5"):
            styles_tree.remove(existing)

    for lvl in (1, 2, 3, 4, 5):
        make_toc_style(lvl)
    print(f"  Injected TOC1..TOC5 style definitions into styles.xml")

    files["word/styles.xml"] = etree.tostring(
        styles_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )

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
