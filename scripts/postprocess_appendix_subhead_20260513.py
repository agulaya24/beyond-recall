"""Strip appendix subsections (A.1, B.2, ..., G.6) from the main TOC.

Approach
--------
1. Add a new paragraph style `AppendixSubhead` to `word/styles.xml`. It is
   `basedOn` Heading 3 (inherits all visual properties), but overrides the
   outline level to 9 ("body text"). Word's TOC field at `\\o "1-3"` skips
   paragraphs with outline level outside 1–3, so these paragraphs no longer
   appear in the main TOC.

2. In `word/document.xml`, find every paragraph styled Heading 3 whose
   visible text begins with the appendix-subsection pattern (letter-dot-digit,
   e.g. "A.1", "B.15", "F.7"). Rewrite its `pStyle` to `AppendixSubhead`.

The body still renders the heading the same way (same fonts, same weight,
same spacing). The TOC no longer lists them. Idempotent — running twice
produces the same output.
"""
from __future__ import annotations

import re
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

APPENDIX_SUBHEAD_STYLE_ID = "AppendixSubhead"
APPENDIX_SUBHEAD_NAME = "Appendix Subhead"

# Appendix subsection text pattern: starts with letter-dot-digit
# (A.1, B.15, C.8, D.5, F.7, G.6, etc.)
SUB_RE = re.compile(r"^[A-H]\.\d+(?:\.\d+)?\s")


def ensure_appendix_subhead_style(styles_tree, etree):
    """Inject the AppendixSubhead style (idempotent)."""
    # Remove existing if present (idempotent re-injection)
    for existing in styles_tree.findall(W + "style"):
        if existing.get(W + "styleId") == APPENDIX_SUBHEAD_STYLE_ID:
            styles_tree.remove(existing)

    style = etree.SubElement(styles_tree, W + "style")
    style.set(W + "type", "paragraph")
    style.set(W + "styleId", APPENDIX_SUBHEAD_STYLE_ID)

    name = etree.SubElement(style, W + "name")
    name.set(W + "val", APPENDIX_SUBHEAD_NAME)

    based = etree.SubElement(style, W + "basedOn")
    based.set(W + "val", "Heading3")

    nxt = etree.SubElement(style, W + "next")
    nxt.set(W + "val", "BodyText")

    etree.SubElement(style, W + "qFormat")

    pPr = etree.SubElement(style, W + "pPr")
    outline = etree.SubElement(pPr, W + "outlineLvl")
    outline.set(W + "val", "9")


def paragraph_text(p) -> str:
    return "".join((t.text or "") for t in p.iter(W + "t"))


def main() -> int:
    from lxml import etree

    print(f"Opening {DOCX.name}...")
    with zipfile.ZipFile(str(DOCX)) as zin:
        names = zin.namelist()
        files = {n: zin.read(n) for n in names}

    # ---- Add AppendixSubhead style to styles.xml ----
    styles_tree = etree.fromstring(files["word/styles.xml"])
    ensure_appendix_subhead_style(styles_tree, etree)
    print(f"  Injected style: {APPENDIX_SUBHEAD_STYLE_ID}")

    # ---- Add left-indent to the Definition style so glossary entries hang ----
    for style in styles_tree.findall(W + "style"):
        if style.get(W + "styleId") == "Definition":
            pPr = style.find(W + "pPr")
            if pPr is None:
                pPr = etree.SubElement(style, W + "pPr")
            # Remove any existing ind override and replace
            for old in pPr.findall(W + "ind"):
                pPr.remove(old)
            ind = etree.SubElement(pPr, W + "ind")
            ind.set(W + "left", "360")
            # Tighten spacing after definition for vertical rhythm
            for old in pPr.findall(W + "spacing"):
                pPr.remove(old)
            spacing = etree.SubElement(pPr, W + "spacing")
            spacing.set(W + "after", "120")
            print(f"  Updated Definition style: left indent 360 twips")
            break

    files["word/styles.xml"] = etree.tostring(
        styles_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    # ---- Rewrite pStyle on matching Heading3 paragraphs in document.xml ----
    doc_tree = etree.fromstring(files["word/document.xml"])
    body = doc_tree.find(W + "body")
    if body is None:
        print("ERROR: no <w:body> in document.xml")
        return 1

    rewrote = 0
    samples = []
    for p in body.iter(W + "p"):
        pPr = p.find(W + "pPr")
        if pPr is None:
            continue
        pStyle = pPr.find(W + "pStyle")
        if pStyle is None:
            continue
        if pStyle.get(W + "val") != "Heading3":
            continue
        text = paragraph_text(p).strip()
        if not SUB_RE.match(text):
            continue
        pStyle.set(W + "val", APPENDIX_SUBHEAD_STYLE_ID)
        rewrote += 1
        if len(samples) < 6:
            samples.append(text[:80])

    print(f"  Heading3 paragraphs restyled to AppendixSubhead: {rewrote}")
    for s in samples:
        print(f"    - {s}")

    files["word/document.xml"] = etree.tostring(
        doc_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    # ---- Repack ----
    tmp_path = DOCX.with_suffix(".docx.tmp")
    with zipfile.ZipFile(str(tmp_path), "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, files[n])
    shutil.move(str(tmp_path), str(DOCX))
    print(f"Saved {DOCX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
