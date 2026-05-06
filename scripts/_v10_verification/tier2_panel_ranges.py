"""Compute per-cell Δ_C4a_internal under three panel choices.

Panels:
  - 4-judge effective (drops GPT-5.4 since Tier 2 GPT-5.4 judge files are
    100% parse_failures with score=0 — see
    docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md).
  - 5-judge legacy (includes GPT-5.4 zeros; corrupts the aggregate).
  - 7-judge sensitivity (5-judge + Gemini Flash + Gemini Pro).

Reports min/max range per cell so §4.6.1 can publish direction-only with
sensitivity ranges.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tier2_mechanical_recompute import (  # type: ignore
    per_subject_per_condition_mean,
    TIER2_DIR,
)

PANEL_4 = {"haiku", "sonnet", "opus", "gpt4o"}
PANEL_5 = PANEL_4 | {"gpt54"}
PANEL_7 = PANEL_5 | {"gemini_flash", "gemini_pro"}

CELLS = [
    ("ebers", "sonnet"),
    ("ebers", "gemini_pro"),
    ("yung_wing", "sonnet"),
    ("yung_wing", "gemini_pro"),
    ("zitkala_sa", "sonnet"),
    ("zitkala_sa", "gemini_pro"),
]


def tier2(subj: str, resp: str, panel: set[str]) -> dict[str, float]:
    pat = TIER2_DIR / f"global_{subj}" / f"tier2_{resp}_judgments_*.json"
    files = [
        Path(p)
        for p in glob.glob(str(pat))
        if not p.endswith(".rl_backup") and "merged" not in p
    ]
    return per_subject_per_condition_mean(files, panel)


def main() -> None:
    print("Per-cell C4a delta under three panels (range = sensitivity to panel choice)")
    print()
    header = (
        f"{'subject':12} {'resp':12} "
        f"{'4j_dC4a':>9} {'5j_dC4a':>9} {'7j_dC4a':>9} "
        f"{'min':>8} {'max':>8} {'sign':>6}"
    )
    print(header)
    rows = []
    for subj, resp in CELLS:
        deltas = []
        for panel in (PANEL_4, PANEL_5, PANEL_7):
            m = tier2(subj, resp, panel)
            c5 = m.get("C5_baseline")
            c4a = m.get("C4a_full_facts_plus_spec")
            d = (c4a - c5) if (c5 is not None and c4a is not None) else None
            deltas.append(d)
        valid = [d for d in deltas if d is not None]
        lo = min(valid) if valid else None
        hi = max(valid) if valid else None
        if lo is None or hi is None:
            sign = "?"
        elif lo > 0:
            sign = "+"
        elif hi < 0:
            sign = "-"
        elif lo <= 0 <= hi:
            sign = "~0"
        else:
            sign = "?"

        def f(x):
            return f"{x:+9.3f}" if x is not None else "       na"

        print(
            f"{subj:12} {resp:12} "
            f"{f(deltas[0])} {f(deltas[1])} {f(deltas[2])} "
            f"{f(lo)} {f(hi)} {sign:>6}"
        )
        rows.append((subj, resp, deltas, lo, hi, sign))


if __name__ == "__main__":
    main()
