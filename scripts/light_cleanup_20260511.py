"""Light-clean pass per docs/reviews/repo_cleanup_audit_20260510.md Section 5.

Safe-to-move items only; zero refs from the active v11.9.8 build pipeline. Moves
go to `_archive/_light_clean_20260511/` so they're recoverable. Office lock
turds are deleted (recoverable via tarball backup at
`C:\\Users\\Aarik\\Anthropic\\_backups\\memory-study-repo_pre_v11_9_7_lock_20260510.tar.gz`).

Usage:
    python scripts/light_cleanup_20260511.py            # dry-run preview
    python scripts/light_cleanup_20260511.py --apply    # execute moves
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO / "_archive" / "_light_clean_20260511"

# (path relative to repo, action) where action is "delete" or "archive"
ITEMS: list[tuple[str, str]] = [
    # Office lock / temp turds — DELETE (recoverable via tarball)
    ("docs/~$yond_recall_v11_9_6_draft.docx", "delete"),
    ("docs/~WRL0003.tmp", "delete"),
    # Explicit _backup_ files — ARCHIVE (still v11.8-era; SHA manifest references them)
    ("docs/_v11_8_walking_backup_20260508.docx", "archive"),
    ("docs/_v11_8_walk_frozen_backup_20260508.md", "archive"),
    ("docs/_v11_8_post_section3_edits_backup_20260508.md", "archive"),
    ("docs/_v11_8_pre_figure_insertion_backup_20260508.docx", "archive"),
    # Duplicate reference docx (canonical lives in docs/_pandoc_styles/)
    ("docs/_reference_arxiv_11pt.docx", "delete"),
    # Intermediate v11.8 figure-ordering docx
    ("docs/archive/beyond_recall_v11_8_draft_with_figures_reordered.docx", "archive"),
    ("docs/archive/beyond_recall_v11_8_draft_with_figures_v2.docx", "archive"),
    # LaTeX test artifacts (rebuildable)
    ("docs/versions/_latex_test_artifacts/beyond_recall_test.aux", "delete"),
    ("docs/versions/_latex_test_artifacts/beyond_recall_test.log", "delete"),
    ("docs/versions/_latex_test_artifacts/beyond_recall_test.out", "delete"),
    ("docs/versions/_latex_test_artifacts/beyond_recall_test.pdf", "delete"),
    ("docs/versions/_latex_test_artifacts/beyond_recall_test.tex", "delete"),
    # v10.1 / v11 freeze-cycle log archival (logs/_archive/)
    ("logs/v10_1_review_gpt55_postfix_run.log", "archive"),
    ("logs/v11_scaffolding_review_run.log", "archive"),
]

# __pycache__ dirs are handled separately (recursive remove)
PYCACHE_DIRS = [
    "scripts/__pycache__",
    "scripts/_v10_verification/__pycache__",
    "scripts/_archive/scratch_v9_v10/__pycache__",
]


def archive_path(repo_rel: Path) -> Path:
    return ARCHIVE_ROOT / repo_rel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Execute moves (default: dry-run preview)")
    args = parser.parse_args()

    moved = 0
    deleted = 0
    missing = 0
    pycache_dirs_cleared = 0

    print(f"{'APPLY' if args.apply else 'DRY-RUN'} — light cleanup\n")

    for rel, action in ITEMS:
        src = REPO / rel
        if not src.exists():
            print(f"  [missing] {rel}")
            missing += 1
            continue
        size = src.stat().st_size

        if action == "delete":
            print(f"  [delete ] {rel}  ({size:,} bytes)")
            if args.apply:
                try:
                    src.unlink()
                    deleted += 1
                except PermissionError as e:
                    print(f"      LOCKED — skip: {e}")
        else:  # archive
            dst = archive_path(Path(rel))
            print(f"  [archive] {rel}  ({size:,} bytes)  ->  _archive/_light_clean_20260511/{rel}")
            if args.apply:
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    moved += 1
                except PermissionError as e:
                    print(f"      LOCKED — skip: {e}")

    print()
    for d in PYCACHE_DIRS:
        p = REPO / d
        if not p.exists():
            print(f"  [missing] {d}/")
            continue
        n_files = sum(1 for _ in p.rglob("*") if _.is_file())
        print(f"  [pycache] {d}/  ({n_files} files)")
        if args.apply:
            try:
                shutil.rmtree(p)
                pycache_dirs_cleared += 1
            except PermissionError as e:
                print(f"      LOCKED — skip: {e}")

    print(f"\nSummary: {moved} archived, {deleted} deleted, {pycache_dirs_cleared} __pycache__ cleared, {missing} missing")
    if not args.apply:
        print("(Dry-run only. Pass --apply to execute.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
