"""Move the 'Reading the gradient' paragraph + Figure 4.1 image + caption to
sit immediately after the 'The cross-subject gradient.' opener paragraph in §4.1,
preserving all comments, tracked changes, and other annotations attached to
existing paragraphs.

Strategy:
    Locate four paragraphs by stable text fragments:
      A. Opener   : starts with "The cross-subject gradient." (the §4.1 lede)
      B. Reading  : starts with "Reading the gradient."
      C. Image    : the paragraph immediately preceding the caption (an image
                    paragraph inserted previously by insert_figures_into_docx_*).
      D. Caption  : starts with "Figure 4.1:"

    Move B, C, D as a block to sit immediately after A. lxml's addnext() on an
    existing element first detaches it from its current position, so each move
    is automatic; no deepcopy, no risk of orphaning comment references.

Usage:
    python reorder_figure_4_1_in_docx_20260508.py <input.docx> <output.docx>
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document


OPENER_FRAGMENT = "less the model already knows about a subject from pretraining"
READING_PREFIX = "Reading the gradient"
CAPTION_PREFIX = "Figure 4.1:"


def main(input_path: Path, output_path: Path) -> int:
    print(f"Opening: {input_path}")
    doc = Document(str(input_path))

    opener_p = None
    reading_p = None
    caption_p = None

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        if opener_p is None and OPENER_FRAGMENT in text:
            opener_p = p
        if reading_p is None and text.startswith(READING_PREFIX):
            reading_p = p
        if caption_p is None and text.startswith(CAPTION_PREFIX):
            caption_p = p

    missing = []
    if opener_p is None:
        missing.append(f"opener (containing {OPENER_FRAGMENT!r})")
    if reading_p is None:
        missing.append(f"reading-the-gradient (starting with {READING_PREFIX!r})")
    if caption_p is None:
        missing.append(f"caption (starting with {CAPTION_PREFIX!r})")
    if missing:
        for m in missing:
            print(f"ERROR: paragraph not found: {m}")
        return 1

    print(f"Found opener     : {opener_p.text[:80]!r}")
    print(f"Found reading    : {reading_p.text[:80]!r}")
    print(f"Found caption    : {caption_p.text[:80]!r}")

    caption_el = caption_p._element
    image_el = caption_el.getprevious()
    if image_el is None or image_el.tag != caption_el.tag:
        print(f"ERROR: no preceding paragraph element found before caption")
        return 1
    print(f"Found image-para : <{image_el.tag.split('}')[1]}> immediately before caption")

    reading_el = reading_p._element
    opener_el = opener_p._element

    if reading_el is opener_el or image_el is opener_el or caption_el is opener_el:
        print("ERROR: target/source elements collide; aborting")
        return 1

    opener_el.addnext(reading_el)
    reading_el.addnext(image_el)
    image_el.addnext(caption_el)

    print("\nReorder complete in memory. Saving...")
    doc.save(str(output_path))
    print(f"Saved: {output_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input.docx> <output.docx>")
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
