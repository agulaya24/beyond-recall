"""Sanity check: confirm 5j vs 7j actually differ when Geminis are present and GPT-5.4 is dropped."""
from __future__ import annotations

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tier2_mechanical_recompute import per_subject_per_condition_mean, TIER2_DIR  # type: ignore

CELLS = [
    ("ebers", "sonnet"), ("ebers", "gemini_pro"),
    ("yung_wing", "sonnet"), ("yung_wing", "gemini_pro"),
    ("zitkala_sa", "sonnet"), ("zitkala_sa", "gemini_pro"),
]

PANELS = {
    "4j_no_gpt54": {"haiku", "sonnet", "opus", "gpt4o"},
    "5j_with_zeros": {"haiku", "sonnet", "opus", "gpt4o", "gpt54"},
    "6j_geminis_only": {"haiku", "sonnet", "opus", "gpt4o", "gemini_flash", "gemini_pro"},
    "7j": {"haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"},
}


def tier2(subj, resp, panel):
    pat = TIER2_DIR / f"global_{subj}" / f"tier2_{resp}_judgments_*.json"
    files = [Path(p) for p in glob.glob(str(pat)) if not p.endswith(".rl_backup") and "merged" not in p]
    return per_subject_per_condition_mean(files, panel)


print(f"{'cell':28} " + " ".join(f"{name:>14}" for name in PANELS))
for subj, resp in CELLS:
    cell = f"{subj}/{resp}"
    deltas = []
    for name, panel in PANELS.items():
        m = tier2(subj, resp, panel)
        c5 = m.get("C5_baseline")
        c4a = m.get("C4a_full_facts_plus_spec")
        d = (c4a - c5) if (c5 is not None and c4a is not None) else None
        deltas.append(f"{d:+14.3f}" if d is not None else "            na")
    print(f"{cell:28} " + " ".join(deltas))
