"""Add centered page numbers to footer + hard-set 1" margins for v11.9.11.

Page numbers: arabic, centered, starting at 1 from cover page.
Margins: 1" all sides (US Letter), hard-set in sectPr.
Footer/header distance: 0.5".

Idempotent: detects existing page-number field code in the footer and skips
re-insertion. Margin values are always set explicitly even if already correct.
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
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from lxml import etree

    print(f"Opening {DOCX.name}...")
    doc = Document(str(DOCX))
    section = doc.sections[0]

    # ---- HARD-SET MARGINS (1") ----
    section.page_height = Inches(11)
    section.page_width = Inches(8.5)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)
    print("Margins set: 1\" all sides, US Letter (8.5x11), header/footer 0.5\".")

    # ---- ADD PAGE NUMBERS TO FOOTER ----
    footer = section.footer
    footer_para = footer.paragraphs[0]

    # Check idempotency: is there already a PAGE field code?
    existing_xml = etree.tostring(footer_para._p, encoding="unicode")
    if "PAGE" in existing_xml and "fldChar" in existing_xml:
        print("Page number field already in footer; skipping insert.")
    else:
        # Clear any existing content in the footer paragraph
        for child in list(footer_para._p):
            if child.tag in (W + "r", W + "hyperlink"):
                footer_para._p.remove(child)

        # Set alignment to center
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Set paragraph font (9pt Times New Roman, matching footnotes)
        pPr = footer_para._p.find(W + "pPr")
        if pPr is None:
            pPr = etree.SubElement(footer_para._p, W + "pPr")
            footer_para._p.insert(0, pPr)

        # Build the PAGE field code via three runs:
        # 1) <w:fldChar fldCharType="begin"/>
        # 2) <w:instrText>PAGE</w:instrText>
        # 3) <w:fldChar fldCharType="end"/>
        # All with 9pt Times New Roman.

        def make_run(elements_xml: str) -> "etree._Element":
            rpr = (
                '<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
                'w:cs="Times New Roman" w:eastAsia="Times New Roman"/>'
                '<w:sz w:val="18"/><w:szCs w:val="18"/>'
                '</w:rPr>'
            )
            run_xml = (
                '<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                + rpr + elements_xml + '</w:r>'
            )
            return etree.fromstring(run_xml)

        r_begin = make_run('<w:fldChar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fldCharType="begin"/>')
        r_instr = make_run('<w:instrText xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xml:space="preserve">PAGE   \\* MERGEFORMAT</w:instrText>')
        r_separate = make_run('<w:fldChar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fldCharType="separate"/>')
        r_value = make_run('<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">1</w:t>')
        r_end = make_run('<w:fldChar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fldCharType="end"/>')

        for el in (r_begin, r_instr, r_separate, r_value, r_end):
            footer_para._p.append(el)

        print("Inserted centered PAGE field in footer (9pt Times New Roman).")

    doc.save(str(DOCX))
    print(f"Saved {DOCX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
