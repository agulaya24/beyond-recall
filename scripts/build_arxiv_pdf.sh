#!/bin/bash
# Build script for Beyond Recall arXiv PDF.
# Phase 2 deliverable: pandoc body regeneration -> pdflatex compile cycle.
# Body-only approach preserves the customized arXiv preamble in beyond_recall.tex
# (master). Body content lives in beyond_recall_body.tex (regenerable).

set -e

REPO="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$REPO/build"
SRC="$REPO/docs/beyond_recall_v12_1_draft.md"
PANDOC="${PANDOC:-pandoc}"

cd "$BUILD"

echo "[0/5] Pre-processing markdown (strip front matter + walk-progress block) ..."
TMP_MD="$BUILD/_beyond_recall_clean.md"
# (1) Strip front matter: H1 title, author block, body Abstract section,
#     "For AI agents:" line, and the openxml page-break fence. The preamble
#     in build/beyond_recall.tex carries the canonical title, author, date,
#     and abstract; emitting them twice produces a broken cover page. Drop
#     everything from line 1 through (but not including) the first
#     "## 1. Introduction" line.
# (2) Strip the v11-era walk-progress block if present (no-op on v12).
# (3) Strip single-line HTML comments.
awk '
  BEGIN { in_front=1; skip=0 }
  in_front==1 && /^## 1\. Introduction/ { in_front=0; print; next }
  in_front==1 { next }
  /^<!-- WALK PROGRESS/ { skip=1; next }
  skip==1 && /^---$/ { skip=0; next }
  skip==1 { next }
  /^<!--/ && /-->$/ { next }   # single-line HTML comments
  { print }
' "$SRC" > "$TMP_MD"

echo "[1/5] Regenerating body from cleaned markdown ..."
"$PANDOC" "$TMP_MD" \
  -o beyond_recall_body.tex \
  --from markdown+yaml_metadata_block+pipe_tables+grid_tables \
  --to latex \
  --top-level-division=section \
  --shift-heading-level-by=-1

echo "[1.5/5] Post-processing body (anchor fixes, citation conversion) ..."
python "$REPO/scripts/fix_body_anchors.py"
if [ -f "$REPO/scripts/convert_citations.py" ]; then
  python "$REPO/scripts/convert_citations.py"
fi
if [ -f "$REPO/scripts/fix_body_tables.py" ]; then
  python "$REPO/scripts/fix_body_tables.py"
fi

echo "[2/5] pdflatex pass 1 ..."
pdflatex -interaction=nonstopmode beyond_recall.tex > /dev/null 2>&1 || true

if [ -f "beyond_recall.bib" ]; then
  echo "[3/5] bibtex ..."
  bibtex beyond_recall > /dev/null 2>&1 || true
fi

echo "[4/5] pdflatex pass 2 ..."
pdflatex -interaction=nonstopmode beyond_recall.tex > /dev/null 2>&1 || true

echo "[5/5] pdflatex pass 3 ..."
pdflatex -interaction=nonstopmode beyond_recall.tex > /dev/null 2>&1 || true

# Clean up temp markdown.
rm -f "$TMP_MD"

echo "Done. PDF at $BUILD/beyond_recall.pdf"
ls -la beyond_recall.pdf beyond_recall.log
