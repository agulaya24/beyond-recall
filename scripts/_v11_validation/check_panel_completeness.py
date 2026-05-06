"""Mechanical panel-completeness audit.

Scans every ``results/**/*judgments*.json`` file under the repo and computes
per-(file, condition, judge) parse-failure rates. Flags any cell where the
parse-failure rate exceeds 5% as SUSPECT, and any cell that is fully failed
as FULL_FAIL.

Outputs a CSV at ``docs/research/v11_panel_completeness_audit.csv`` with one
row per (file, condition, judge) cell.

Exit code:
    0 if every cell is CLEAN, OR every non-CLEAN cell is in the waiver list.
    1 otherwise.

Waiver file: ``docs/research/v11_panel_completeness_waivers.json``. Format::

    {
      "waivers": [
        {"file": "results/...", "condition": "...", "judge": "...",
         "status": "FULL_FAIL", "reason": "...", "tracked_in": "..."}
      ]
    }

Anything matching by (file, condition, judge) in the waivers list is treated
as expected and does not fail CI.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent.parent
RESULTS = REPO / "results"
LETTA_RERUN = REPO / "docs" / "research" / "_letta_rerun"
OUT_CSV = REPO / "docs" / "research" / "v11_panel_completeness_audit.csv"
WAIVER_PATH = REPO / "docs" / "research" / "v11_panel_completeness_waivers.json"

SUSPECT_THRESHOLD = 0.05  # cells with > 5% parse-failure rate are SUSPECT
FULL_FAIL_THRESHOLD = 0.99  # cells with >= 99% parse-failure rate are FULL_FAIL

KNOWN_JUDGES = {
    "haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro",
}


def is_parse_failure(row: dict[str, Any]) -> bool:
    """Mirror the rule in ``scripts/scan_parse_failures.py``."""
    if row.get("parse_failure") is True:
        return True
    score = row.get("score")
    if score in (0, None):
        return True
    if isinstance(score, (int, float)) and score < 1:
        return True
    return False


def _load_judgments(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        data = json.loads(path.read_text(encoding="latin-1"))
    if isinstance(data, dict) and "judgments" in data:
        data = data["judgments"]
    if not isinstance(data, list):
        return []
    return data


def _scan_file(path: Path) -> list[tuple[str, str, int, int]]:
    """Return list of (condition, judge, n_failed, n_total) for a single file.

    Handles both the long-format (one row per question x judge) and the
    legacy wide-format (one row with ``haiku_score``, ``gemini_score``, etc).
    """
    records = _load_judgments(path)
    if not records:
        return []

    agg: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])

    if all(k in records[0] for k in ("question_id", "condition", "judge", "score")):
        # Long format.
        for r in records:
            cond = r.get("condition") or "?"
            judge = r.get("judge") or "?"
            agg[(cond, judge)][1] += 1
            if is_parse_failure(r):
                agg[(cond, judge)][0] += 1
    elif "haiku_score" in records[0] or "gemini_score" in records[0]:
        # Legacy wide format.
        col_map = [
            ("haiku_score", "haiku"),
            ("sonnet_score", "sonnet"),
            ("opus_score", "opus"),
            ("gpt4o_score", "gpt4o"),
            ("gpt54_score", "gpt54"),
            ("gemini_score", "gemini_flash"),
            ("gemini_pro_score", "gemini_pro"),
        ]
        for r in records:
            cond = r.get("condition") or "?"
            for col, judge in col_map:
                if col not in r:
                    continue
                agg[(cond, judge)][1] += 1
                v = r.get(col)
                if v in (0, None):
                    agg[(cond, judge)][0] += 1
    else:
        return []

    return [(c, j, pf, tot) for (c, j), (pf, tot) in agg.items()]


def _classify(n_failed: int, n_total: int) -> str:
    if n_total == 0:
        return "EMPTY"
    rate = n_failed / n_total
    if rate >= FULL_FAIL_THRESHOLD:
        return "FULL_FAIL"
    if rate > SUSPECT_THRESHOLD:
        return "SUSPECT"
    return "CLEAN"


def _load_waivers() -> set[tuple[str, str, str]]:
    if not WAIVER_PATH.exists():
        return set()
    try:
        data = json.loads(WAIVER_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return set()
    out: set[tuple[str, str, str]] = set()
    for w in data.get("waivers", []):
        f = w.get("file", "").replace("\\", "/")
        c = w.get("condition", "")
        j = w.get("judge", "")
        if f and c and j:
            out.add((f, c, j))
    return out


def _iter_judgment_files() -> list[Path]:
    files: list[Path] = []
    if RESULTS.exists():
        files.extend(p for p in RESULTS.rglob("*judgments*.json") if p.is_file())
    if LETTA_RERUN.exists():
        files.extend(p for p in LETTA_RERUN.rglob("*judgments*.json") if p.is_file())
    # Skip ``.rl_backup`` and ``.brief_only_backup`` siblings; these are
    # intentionally preserved evidence. Also skip merged aggregates whose
    # cell-level breakdown is already covered by the per-judge files.
    return [p for p in files if not p.suffix in {".rl_backup", ".backup"}
            and not p.name.endswith(".brief_only_backup")]


def main() -> int:
    waivers = _load_waivers()
    rows: list[dict[str, Any]] = []
    suspect = 0
    full_fail = 0
    waived = 0
    cells = 0

    for path in sorted(_iter_judgment_files()):
        # Use a repo-relative path with forward slashes for stable CSV output.
        try:
            rel = path.resolve().relative_to(REPO).as_posix()
        except ValueError:
            rel = path.as_posix()

        for cond, judge, n_failed, n_total in _scan_file(path):
            cells += 1
            status = _classify(n_failed, n_total)
            rate = (n_failed / n_total) if n_total else 0.0
            waived_here = (rel, cond, judge) in waivers
            if status == "FULL_FAIL":
                full_fail += 1
            elif status == "SUSPECT":
                suspect += 1
            if waived_here and status != "CLEAN":
                waived += 1
            rows.append({
                "file": rel,
                "condition": cond,
                "judge": judge,
                "n_total": n_total,
                "n_failed": n_failed,
                "fail_rate": round(rate, 4),
                "status": status,
                "waived": "Y" if waived_here else "N",
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["file", "condition", "judge", "n_total", "n_failed",
                           "fail_rate", "status", "waived"],
        )
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["status"] != "FULL_FAIL",
                                             x["status"] != "SUSPECT",
                                             x["file"], x["condition"], x["judge"])):
            w.writerow(r)

    print(f"Scanned {cells} cells across {len(_iter_judgment_files())} files.")
    print(f"  CLEAN     : {cells - full_fail - suspect}")
    print(f"  SUSPECT   : {suspect}  (>{int(SUSPECT_THRESHOLD * 100)}% parse-failure)")
    print(f"  FULL_FAIL : {full_fail}")
    print(f"  Waived    : {waived}")
    print(f"CSV written: {OUT_CSV.relative_to(REPO).as_posix()}")

    unwaived_bad = [
        r for r in rows
        if r["status"] in {"FULL_FAIL", "SUSPECT"} and r["waived"] == "N"
    ]
    if unwaived_bad:
        print()
        print(f"FAIL: {len(unwaived_bad)} unwaived non-CLEAN cells.")
        for r in unwaived_bad[:25]:
            print(f"  {r['status']:<10} {r['file']}  cond={r['condition']}  judge={r['judge']}  "
                  f"{r['n_failed']}/{r['n_total']}")
        if len(unwaived_bad) > 25:
            print(f"  ... ({len(unwaived_bad) - 25} more in CSV)")
        return 1
    print("PASS: every non-CLEAN cell is waived.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
