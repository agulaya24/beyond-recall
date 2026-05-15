"""Set explicit table column widths for v11.9.11 docx.

Targets the tables flagged in Group H of the panel review:
  - Excerpt-column tables (Seacole/Hamerton worked examples)
  - "What this means in plain terms" tables
  - "What this bin shows" table
  - Wide numeric-heavy tables (compression, gradient, memsys aggregate)

Rule: numeric columns shrink to ~0.55-0.75"; narrative columns absorb the
slack. Total stays at page-content width (6.5" = 9360 twips for 1" margins on
8.5" letter).

The script matches tables by their first-row header signature so that table
re-ordering does not silently mis-target.

Idempotent: re-running with the same input produces the same output. python-
docx is used for the iteration; explicit `<w:tcW>` elements are written via
direct XML so the widths survive Word's auto-fit behavior.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

from docx import Document
from docx.oxml.ns import qn
from lxml import etree

REPO = Path(__file__).resolve().parent.parent
DOCX = REPO / "docs" / "beyond_recall_v12_1_draft.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{" + W_NS + "}"

# Page width = 8.5" * 1440 twips/inch = 12240; minus 2" margins = 9360 twips
PAGE_W = 9360

# Header signature -> list of column widths (twips). Sum should be <= PAGE_W.
TARGETS = {
    # Worked-example tables: narrow Code/Mean, fat Excerpt
    # C178 2026-05-14: Anchor column deleted from both worked-example tables
    # (Seacole Q2, Hamerton Q25) since the Mean column already exists.
    ("Condition", "Code", "Mean", "Excerpt"):
        [1800, 700, 700, 6160],

    # Spearman table REMOVED 2026-05-13: the Spearman ρ table
    # ("Condition pair", "ρ", "What this means in plain terms") was converted
    # to a bulleted list in v12.1 and no longer exists as a table.

    # Wrong-Spec aggregate table
    ("Condition", "Mean Δ vs. C5 (5-judge primary, 13 globals)", "Reading"):
        [2200, 1800, 5360],

    # Bin-share table REMOVED 2026-05-13: the bin-share table
    # ("C5 baseline (X)", "N", "Share", ...) was converted to prose blocks in
    # v12.1 and no longer exists as a table.

    # Transition table
    ("Transition", "% of responses", "Description"):
        [1500, 1200, 6660],

    # Categories table (3 col with example)
    ("Category", "What it probes", "Example question"):
        [1400, 2800, 5160],

    # Conditions group table (4 col)
    ("Group", "Condition", "Inputs given to the model", "Purpose"):
        [1500, 1800, 3200, 2860],

    # Compression table (10 col -- narrow numerics, fat subject)
    # Headers updated 2026-05-13: "C4a facts+Spec" -> "C4a All Facts + Spec",
    # "C9 corpus+Spec" -> "C9 Corpus + Spec".
    ("Subject", "Source words (~tokens)", "Compression ratio (corpus / Spec)",
     "C5 baseline", "C2a Spec (~7K tok)", "C4 facts (~10K tok)",
     "C8 raw corpus", "C4a All Facts + Spec", "C9 Corpus + Spec", "C8 − C2a"):
        [1400, 1100, 900, 800, 800, 800, 800, 800, 800, 1160],

    # §4.1 gradient table (8 col)
    # Headers updated 2026-05-14 (C149): consistent condition labels --
    # "C5 baseline" -> "C5 Baseline", "C4 facts" -> "C4 All Facts",
    # "C2a Spec" -> "C2a Spec Only", matching the canonical §3.2 names.
    # Subject column narrowed to its minimum that keeps names on one line;
    # the freed space goes to the C4a column.
    ("Subject", "C5 Baseline", "C4 All Facts", "C2a Spec Only",
     "C4a All Facts + Spec", "Δ C4a−C5", "Δ C4a−C4", "Anchor"):
        [1600, 950, 950, 950, 1450, 1150, 1150, 1160],

    # Memory-system aggregate table (6 col)
    ("System", "Config", "Δ_spec", "% subjects improved",
     "% questions up ≥1 anchor", "% questions up ≥2 anchors"):
        [1500, 1100, 800, 1900, 2000, 2060],

    # Subjects table (6 col -- Origin column needs space)
    # C117: "Project Gutenberg #NNNN" shortened to "PG #NNNN" in the draft, so
    # the Source column shrinks and the freed space goes to Origin.
    ("#", "Subject", "Source", "Words", "Origin", "Era"):
        [500, 2200, 1500, 1000, 3300, 860],

    # Per-condition improvement table (8 col)
    ("Condition vs. baseline", "Approx. context", "Improved", "Tied", "Worse",
     "Improvement rate", "Median Δ when improved", "Median Δ when worsened"):
        [1800, 1100, 800, 600, 800, 1100, 1480, 1680],

    # Letta letta-rerun table (8 col)
    # Header updated 2026-05-13: "Spec score (brief only)" -> "Spec score (full-stack)".
    ("Subject", "Corpus (words)", "Letta score", "Spec score (full-stack)",
     "Δ (Letta − Spec)", "Letta block (chars)", "Spec (chars)",
     "Letta : Spec size"):
        [1300, 1100, 1000, 1300, 1100, 1300, 900, 1360],

    # --- New width targets 2026-05-13 (Aarik v12 comment pass) ---

    # C088 / C090: §3.2 "All conditions, by group" table (4 col).
    # Narrow ID; give the freed room to Condition and Inputs served.
    ("Group", "ID", "Condition", "Inputs served"):
        [2600, 600, 2400, 3760],

    # C088 / C090: §3.2 "Direct context manipulations" table (4 col).
    # Same ID-narrowing rationale.
    ("ID", "Condition", "Inputs served", "Null / comparison"):
        [600, 2200, 3400, 3160],

    # C167: §4.2 compression "Context improves prediction" table (5 col).
    # Narrow Condition; the context-served column absorbs the slack.
    ("Condition", "Context served (approx. tokens, low-baseline mean)", "n",
     "Mean (low-baseline)", "Δ from C5"):
        [900, 4760, 600, 1700, 1400],

    # C175: §4.2.1 multi-anchor crossings table (6 col).
    # Maximize Comparison; Subject set shrunk to the minimum that still fits
    # its title; remaining numeric columns stay narrow.
    ("Comparison", "Subject set", "n paired", "Multi-anchor (≥2)",
     "Extreme (≥3)", "Mean Δ"):
        [4360, 1100, 900, 1200, 1000, 800],

    # C183: §4.3 "Summary of the three examples" mechanism table (6 col).
    # Maximize the Mechanism and Wrong-Spec pattern narrative columns; the
    # numeric columns stay narrow.
    ("Example", "Mechanism (correct Spec)", "C4a (correct)", "C2c v1 (wrong)",
     "Drop", "Wrong-Spec pattern"):
        [1100, 3000, 900, 900, 660, 2800],

    # C203: §B.13 memory-system Wilcoxon table (7 col).
    # Give more room to the two low-baseline column headings; shrink the
    # short numeric columns.
    ("System", "Config", "N (all)", "W", "p (all-14)",
     "Low-baseline Δ_spec mean", "Low-baseline improved (of 9)"):
        [1400, 1100, 700, 600, 900, 2400, 2260],

    # C204: §B.14 low-baseline pairwise comparison table (4 col).
    # Maximize the Comparison column; shrink the numeric columns.
    ("Comparison", "First better", "Second better", "Tie"):
        [4860, 1500, 1500, 1500],

    # C205: §B.15 abstention audit cell-count table (5 col).
    # Maximize the Cell and Definition columns; shrink the numeric columns.
    ("Cell", "Definition", "N", "Mean", "% ≥ 2.0"):
        [2700, 4060, 700, 800, 1100],

    # C206: §B.15 Welch comparison table (4 col).
    # Maximize the Comparison column; shrink the rest.
    ("Comparison", "Δ", "95% CI", "p (Welch)"):
        [4860, 800, 2300, 1400],
}


def set_table_widths(table, widths: list[int]) -> bool:
    """Set explicit widths on a table's grid and on each cell.

    Returns True if widths were applied, False if column count mismatch.
    """
    if not table.rows:
        return False
    first_row = table.rows[0]
    n_cols = len(first_row.cells)
    if n_cols != len(widths):
        return False

    tbl = table._tbl

    # 1. Set / replace <w:tblGrid> with explicit widths.
    grid = tbl.find(W + "tblGrid")
    if grid is not None:
        tbl.remove(grid)
    grid = etree.SubElement(tbl, W + "tblGrid")
    for w in widths:
        col = etree.SubElement(grid, W + "gridCol")
        col.set(W + "w", str(w))

    # tblGrid must come right after tblPr; move it if not already
    tblPr = tbl.find(W + "tblPr")
    if tblPr is not None and grid is not None:
        tbl.remove(grid)
        tblPr.addnext(grid)

    # 2. Set explicit width on tblPr -> tblW (fixed, sum of grid)
    if tblPr is not None:
        tblW = tblPr.find(W + "tblW")
        if tblW is None:
            tblW = etree.SubElement(tblPr, W + "tblW")
        tblW.set(W + "type", "dxa")
        tblW.set(W + "w", str(sum(widths)))

        # Force tblLayout to fixed so column widths are honored
        layout = tblPr.find(W + "tblLayout")
        if layout is None:
            layout = etree.SubElement(tblPr, W + "tblLayout")
        layout.set(W + "type", "fixed")

    # 3. Set explicit width on each cell in every row.
    for row in table.rows:
        cells = row.cells
        for col_idx, cell in enumerate(cells):
            if col_idx >= len(widths):
                break
            tc = cell._tc
            tcPr = tc.find(W + "tcPr")
            if tcPr is None:
                tcPr = etree.SubElement(tc, W + "tcPr")
                tc.insert(0, tcPr)
            tcW = tcPr.find(W + "tcW")
            if tcW is None:
                tcW = etree.SubElement(tcPr, W + "tcW")
            tcW.set(W + "type", "dxa")
            tcW.set(W + "w", str(widths[col_idx]))

    return True


def header_signature(table) -> tuple[str, ...]:
    if not table.rows:
        return ()
    # Normalize non-breaking spaces produced by Word/pandoc so target dict keys
    # can use plain ASCII spaces. Collapse runs of whitespace conservatively.
    sigs = []
    for c in table.rows[0].cells:
        t = c.text.strip().replace("\xa0", " ").replace(" ", " ")
        sigs.append(t)
    return tuple(sigs)


def main() -> int:
    print(f"Opening {DOCX.name}...")
    doc = Document(str(DOCX))
    applied = 0
    skipped = 0
    for i, table in enumerate(doc.tables):
        sig = header_signature(table)
        widths = TARGETS.get(sig)
        if widths is None:
            continue
        ok = set_table_widths(table, widths)
        if ok:
            applied += 1
            short = sig[0][:30] if sig else "(unknown)"
            print(f"  T{i:3d}: widths set ({len(widths)} cols) | header[0]={short}")
        else:
            skipped += 1
            print(f"  T{i:3d}: SKIP, column count mismatch (table has {len(table.rows[0].cells)}, widths {len(widths)})")

    print(f"\nApplied: {applied}, Skipped: {skipped}, Targets defined: {len(TARGETS)}")
    doc.save(str(DOCX))
    print(f"Saved {DOCX.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
