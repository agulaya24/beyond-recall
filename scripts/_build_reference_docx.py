"""Build a pandoc reference.docx styled for arXiv-standard body:
Times New Roman 11pt Normal, retaining heading hierarchy.

Output: docs/_reference_arxiv_11pt.docx

Used by export_v9_to_docx.py via --reference-doc.
"""
import subprocess
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "_reference_arxiv_11pt.docx"

# Start from pandoc's default reference.docx (via pypandoc-bundled pandoc).
tmp = REPO / "docs" / "_pandoc_default_reference.docx"
import pypandoc
pandoc_exe = pypandoc.get_pandoc_path()
subprocess.run(
    [pandoc_exe, "-o", str(tmp), "--print-default-data-file", "reference.docx"],
    check=True,
)

doc = Document(str(tmp))

# Body font: Times New Roman 11pt
BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(11)

# Heading scale (relative): H1 14pt bold, H2 13pt bold, H3 12pt bold, rest 11pt
HEADING_SCALE = {
    "Heading 1": (Pt(14), True),
    "Heading 2": (Pt(13), True),
    "Heading 3": (Pt(12), True),
    "Heading 4": (Pt(11), True),
    "Heading 5": (Pt(11), True),
    "Heading 6": (Pt(11), True),
    "Heading 7": (Pt(11), True),
    "Heading 8": (Pt(11), True),
    "Heading 9": (Pt(11), True),
    "Title":     (Pt(20), True),
    "Subtitle":  (Pt(14), False),
}


def set_rpr_font(style, font_name, size, bold=None):
    """Set the font/size on a style's default run properties."""
    rPr = style.element.get_or_add_rPr()

    # Remove existing rFonts and rFonts-related tags to start clean
    for tag in ("rFonts", "sz", "szCs"):
        for e in rPr.findall(qn(f"w:{tag}")):
            rPr.remove(e)

    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    rFonts.set(qn("w:cs"), font_name)
    rFonts.set(qn("w:eastAsia"), font_name)
    rPr.append(rFonts)

    sz = OxmlElement("w:sz")
    # docx sz is in half-points
    sz.set(qn("w:val"), str(int(size.pt * 2)))
    rPr.append(sz)

    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), str(int(size.pt * 2)))
    rPr.append(szCs)

    if bold is True:
        b = OxmlElement("w:b")
        rPr.append(b)
        bCs = OxmlElement("w:bCs")
        rPr.append(bCs)


# Apply to Normal style (body text default)
normal = doc.styles["Normal"]
set_rpr_font(normal, BODY_FONT, BODY_SIZE)

# Apply to heading styles (retain bold)
for style_name, (size, bold) in HEADING_SCALE.items():
    if style_name in [s.name for s in doc.styles]:
        try:
            style = doc.styles[style_name]
            set_rpr_font(style, BODY_FONT, size, bold=bold)
        except Exception as e:
            print(f"  WARN: {style_name}: {e}")

# Save
doc.save(str(OUT))
print(f"Wrote: {OUT}")

# Verify
import zipfile
with zipfile.ZipFile(str(OUT)) as z:
    xml = z.read("word/styles.xml").decode("utf-8", errors="replace")
    if 'Times New Roman' in xml:
        print("Verified: Times New Roman in styles.xml")
    if 'w:val="22"' in xml:  # 22 half-points = 11pt
        print("Verified: 11pt (sz val=22) present")
