#!/usr/bin/env python3
"""Wrap wide longtables in landscape mode for the appendix sections that
need it: Appendix B per-subject tables (B.2 onwards). Appendix D.4 was
landscape-wrapped through v11.8 but is redirected in v12.1 (no inline table).

Strategy: identify each appendix subsection's range in the body, find every
longtable inside that range, and wrap each one in landscape. Idempotent.
"""
import re
from pathlib import Path

BODY = Path(__file__).resolve().parents[1] / "build" / "beyond_recall_body.tex"

text = BODY.read_text(encoding="utf-8")

# --- Helpers ---
def is_already_wrapped(t, lt_open):
    """Return True if longtable at lt_open is immediately preceded by an
    unmatched \\begin{landscape}."""
    pre = t[max(0, lt_open - 200):lt_open]
    last_open = pre.rfind("\\begin{landscape}")
    last_close = pre.rfind("\\end{landscape}")
    return last_open >= 0 and last_open > last_close


def find_longtables_in_range(t, start, end):
    """Return list of (open_idx, close_idx_end) of longtables fully contained
    in [start, end)."""
    results = []
    pos = start
    while True:
        lt_open = t.find("\\begin{longtable}", pos)
        if lt_open < 0 or lt_open >= end:
            break
        lt_close = t.find("\\end{longtable}", lt_open)
        if lt_close < 0 or lt_close >= end:
            break
        results.append((lt_open, lt_close + len("\\end{longtable}")))
        pos = lt_close + len("\\end{longtable}")
    return results


def wrap_longtables_in_section(anchor_pat, label, t):
    """Wrap every longtable in a section. Section span = [anchor_end, next_subsection_or_section_anchor)."""
    anchor_m = re.search(anchor_pat, t)
    if not anchor_m:
        print(f"  WARN: anchor {label} not found")
        return t, 0
    # Skip past anchor's "{%\n\subsection{...}\label{slug}}" closing — find
    # the first newline AFTER the anchor's content. The anchor is on its own
    # line; \subsection{...}\label{...}} ends at the second } closing the
    # \hypertarget. Easiest: skip past the next "\\label{" + closing "}}".
    after_anchor = anchor_m.end()
    label_close = t.find("}}", after_anchor)
    start = label_close + 2 if label_close > 0 else after_anchor
    # End of this section: next \hypertarget after start.
    # Slugs include _, hyphen, period, alphanumeric.
    next_anchor = re.search(r"\\hypertarget\{[a-z0-9._\-]+\}", t[start:])
    end = (start + next_anchor.start()) if next_anchor else len(t)
    tables = find_longtables_in_range(t, start, end)
    n_wrapped = 0
    # Walk in REVERSE so insertions don't shift earlier indices.
    for lt_open, lt_close_end in reversed(tables):
        if is_already_wrapped(t, lt_open):
            continue
        t = (
            t[:lt_open]
            + "\\begin{landscape}\n"
            + t[lt_open:lt_close_end]
            + "\n\\end{landscape}"
            + t[lt_close_end:]
        )
        n_wrapped += 1
    if n_wrapped:
        print(f"  WRAPPED {n_wrapped} longtable(s) in {label}")
    else:
        print(f"  SKIP: {label} (no unwrapped longtable in section)")
    return t, n_wrapped


# D.4 wrap removed 2026-05-14: in v12.1 Appendix D.4 ("Per-judge score
# matrices") is redirected (the wide 11-column matrix moved out of the body),
# so there is no longtable to landscape-wrap. Re-add a wrap block here if a
# future revision puts the matrix back inline.

# Wrap B.2 onwards (appendix B per-subject tables)
for n in range(2, 12):  # B.2 .. B.11
    text, _ = wrap_longtables_in_section(
        rf"\\hypertarget\{{b\.{n}-[^}}]+\}}",
        f"Appendix B.{n}",
        text,
    )

BODY.write_text(text, encoding="utf-8")
print("Table landscape wrapping complete.")
