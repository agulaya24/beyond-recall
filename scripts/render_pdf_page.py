#!/usr/bin/env python3
"""Render specific PDF pages to PNG so the Read tool can view them.

Usage:
    python scripts/render_pdf_page.py <page> [<page> ...]
    python scripts/render_pdf_page.py 13 50 64

Defaults to build/beyond_recall.pdf; pass --pdf for a different file.
Output PNGs go to build/page_NNN.png at 144 DPI.
"""
import argparse
import sys
from pathlib import Path

import pymupdf  # type: ignore

DEFAULT_PDF = Path(__file__).resolve().parents[1] / "build" / "beyond_recall.pdf"


def render(pdf_path: Path, pages: list[int], dpi: int = 144, out_dir: Path | None = None) -> list[Path]:
    out_dir = out_dir or pdf_path.parent
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    written: list[Path] = []
    zoom = dpi / 72.0  # default page DPI is 72
    mat = pymupdf.Matrix(zoom, zoom)
    for p in pages:
        if p < 1 or p > n:
            print(f"  page {p}: out of range (PDF has {n} pages)", file=sys.stderr)
            continue
        page = doc[p - 1]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = out_dir / f"page_{p:03d}.png"
        pix.save(out)
        print(f"  rendered page {p:>3} -> {out} ({pix.width}x{pix.height})")
        written.append(out)
    doc.close()
    return written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="+", type=int, help="1-indexed page numbers")
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--dpi", type=int, default=144)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    if not args.pdf.exists():
        print(f"PDF not found: {args.pdf}", file=sys.stderr)
        return 1
    render(args.pdf, args.pages, dpi=args.dpi, out_dir=args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
