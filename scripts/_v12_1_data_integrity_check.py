"""Data integrity check for the 14 main-study subjects, used by the v12.1 repo lock pass.

Per paper §3.4 Table 3.1, the 14 main-study subjects are:
  13 globals (under data/global_subjects/<s>/ and results/global_<s>/)
    augustine, babur, bernal_diaz, cellini, ebers, equiano, fukuzawa,
    keckley, rousseau, seacole, sunity_devee, yung_wing, zitkala_sa
  Hamerton (under data/hamerton/ and results/hamerton/)
  Franklin  (under data/franklin/ and results/franklin/ + results/franklin_legacy_20260411/)

The task brief asked to confirm `battery_v2.json` / `results_v2.json` / `judgments_v2.json`
exist per subject. The repo's actual canonical layout is:
  - globals: v2 canonical lives in results/global_<s>/{battery_v2,results_v2,judgments_v2}.json
             unsuffixed v1 cache stays in data/global_subjects/<s>/{battery,results,judgments}.json
  - Hamerton: results.json + judgments.json + battery.json (no _v2 suffix); plus the
             memory-systems matrix of {provider}_judgments_*.json files.
  - Franklin: data/franklin/battery.json; responses at results/franklin/fullstack_haiku.json;
             judgments at results/franklin/{haiku|sonnet|opus|gpt4o|gpt54|gemini_pro}_judgments.json
             plus the C4 backfill in results/franklin_legacy_20260411/analysis/.
Specs live at:
  - globals: data/global_subjects/<s>/{anchors_v4,core_v4,predictions_v4,brief_v5}.md (flat layout)
  - Hamerton: data/hamerton/spec/{anchors_v4,core_v4,predictions_v4,brief_v5_clean}.md
  - Franklin: baselayer/examples/franklin/{anchors_v4,core_v4,predictions_v4,brief_v4}.md

This script prints a status line for each subject across all expected files.
Anything missing or zero-byte is flagged as FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent

GLOBAL_SUBJECTS = [
    "augustine", "babur", "bernal_diaz", "cellini", "ebers", "equiano",
    "fukuzawa", "keckley", "rousseau", "seacole", "sunity_devee", "yung_wing",
    "zitkala_sa",
]


def check(path: Path) -> tuple[bool, int]:
    if not path.exists():
        return False, 0
    try:
        sz = path.stat().st_size
    except OSError:
        return False, 0
    return sz > 0, sz


def report_subject(name: str, files: list[tuple[str, Path]]) -> list[str]:
    rows = []
    for label, p in files:
        ok, sz = check(p)
        status = "OK" if ok else "MISSING/EMPTY"
        rel = p.relative_to(REPO).as_posix()
        rows.append(f"  {status:<14}  {label:<24}  {sz:>10,} B  {rel}")
    return rows


def main() -> int:
    print("=" * 100)
    print("DATA INTEGRITY — 14 main-study subjects (v12.1 lock pass, 2026-05-13)")
    print("=" * 100)

    pass_count = 0
    fail_lines: list[str] = []

    # 13 globals
    for s in GLOBAL_SUBJECTS:
        print(f"\n--- {s} (global) ---")
        files = [
            # v2 canonical (results tree)
            ("battery_v2.json",      REPO / "results" / f"global_{s}" / "battery_v2.json"),
            ("results_v2.json",      REPO / "results" / f"global_{s}" / "results_v2.json"),
            ("judgments_v2.json",    REPO / "results" / f"global_{s}" / "judgments_v2.json"),
            # v1 cache (data tree)
            ("battery.json (v1)",    REPO / "data" / "global_subjects" / s / "battery.json"),
            ("results.json (v1)",    REPO / "data" / "global_subjects" / s / "results.json"),
            ("judgments.json (v1)",  REPO / "data" / "global_subjects" / s / "judgments.json"),
            # spec (flat layout in data tree)
            ("anchors_v4.md",        REPO / "data" / "global_subjects" / s / "anchors_v4.md"),
            ("core_v4.md",           REPO / "data" / "global_subjects" / s / "core_v4.md"),
            ("predictions_v4.md",    REPO / "data" / "global_subjects" / s / "predictions_v4.md"),
            ("brief_v5.md",          REPO / "data" / "global_subjects" / s / "brief_v5.md"),
        ]
        rows = report_subject(s, files)
        for r in rows:
            print(r)
            if "MISSING" in r:
                fail_lines.append(f"{s}: {r.strip()}")
            else:
                pass_count += 1

    # Hamerton
    print("\n--- hamerton ---")
    files_h = [
        ("battery.json",            REPO / "data" / "hamerton" / "battery.json"),
        ("results.json",            REPO / "results" / "hamerton" / "results.json"),
        ("judgments.json",          REPO / "results" / "hamerton" / "judgments.json"),
        ("facts.json",              REPO / "data" / "hamerton" / "facts.json"),
        ("spec/anchors_v4.md",      REPO / "data" / "hamerton" / "spec" / "anchors_v4.md"),
        ("spec/core_v4.md",         REPO / "data" / "hamerton" / "spec" / "core_v4.md"),
        ("spec/predictions_v4.md",  REPO / "data" / "hamerton" / "spec" / "predictions_v4.md"),
        ("spec/brief_v5_clean.md",  REPO / "data" / "hamerton" / "spec" / "brief_v5_clean.md"),
    ]
    rows = report_subject("hamerton", files_h)
    for r in rows:
        print(r)
        if "MISSING" in r:
            fail_lines.append(f"hamerton: {r.strip()}")
        else:
            pass_count += 1

    # Franklin
    print("\n--- franklin ---")
    files_f = [
        ("battery.json",                       REPO / "data" / "franklin" / "battery.json"),
        ("facts.json",                         REPO / "data" / "franklin" / "facts.json"),
        ("fullstack_haiku.json (responses)",   REPO / "results" / "franklin" / "fullstack_haiku.json"),
        ("judgments.json (legacy 2-judge)",    REPO / "results" / "franklin" / "judgments.json"),
        ("gpt4o_judgments.json (C4 backfill)", REPO / "results" / "franklin" / "gpt4o_judgments.json"),
        ("gpt54_judgments.json (C4 backfill)", REPO / "results" / "franklin" / "gpt54_judgments.json"),
        ("opus_judgments.json",                REPO / "results" / "franklin" / "opus_judgments.json"),
        ("sonnet_judgments.json",              REPO / "results" / "franklin" / "sonnet_judgments.json"),
        ("gemini_pro_judgments.json",          REPO / "results" / "franklin" / "gemini_pro_judgments.json"),
        ("baselayer/anchors_v4.md",            REPO / "baselayer" / "examples" / "franklin" / "anchors_v4.md"),
        ("baselayer/core_v4.md",               REPO / "baselayer" / "examples" / "franklin" / "core_v4.md"),
        ("baselayer/predictions_v4.md",        REPO / "baselayer" / "examples" / "franklin" / "predictions_v4.md"),
        ("baselayer/brief_v4.md",              REPO / "baselayer" / "examples" / "franklin" / "brief_v4.md"),
    ]
    rows = report_subject("franklin", files_f)
    for r in rows:
        print(r)
        if "MISSING" in r:
            fail_lines.append(f"franklin: {r.strip()}")
        else:
            pass_count += 1

    print()
    print("=" * 100)
    print(f"Pass: {pass_count}")
    print(f"Fail: {len(fail_lines)}")
    if fail_lines:
        print("\nFails:")
        for f in fail_lines:
            print(f"  {f}")
    return 0 if not fail_lines else 1


if __name__ == "__main__":
    raise SystemExit(main())
