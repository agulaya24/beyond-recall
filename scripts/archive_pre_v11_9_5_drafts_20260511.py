"""Archive pre-v11.9.5 draft families per Aarik 2026-05-11 direction.

The final public-repo release will contain only the locked final-version
paper plus its directly-cited supporting artifacts; predecessor drafts
(v11, v11.1, v11.2, v11.8, v11.9, v11.9.1) and their export scripts move
to `docs/_archive_pre_v11_9_5/` so the active `docs/` root is clean.

Pairs each draft file with its matching `export_*_to_docx.py` script (also
archived) so the historical exporter stays bundled with its corresponding
draft. v10.1 release-frozen baseline stays at `docs/` root (preserved
historical reference per existing AGENTS.md convention).

The user noted this should be specified somewhere; this script's docstring
and the README addendum it triggers handle that.

Usage:
    python scripts/archive_pre_v11_9_5_drafts_20260511.py            # dry-run preview
    python scripts/archive_pre_v11_9_5_drafts_20260511.py --apply    # execute
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
ARCHIVE_ROOT = REPO / "docs" / "_archive_pre_v11_9_5"

# Pre-v11.9.5 draft families to archive
DRAFTS = [
    "beyond_recall_v11_draft",
    "beyond_recall_v11_1_draft",
    "beyond_recall_v11_2_draft",
    "beyond_recall_v11_8_draft",
    "beyond_recall_v11_9_draft",
    "beyond_recall_v11_9_1_draft",
]

# Each draft family typically has these extensions
DRAFT_EXTENSIONS = [".md", ".docx", ".clean.md"]

# Sibling artifacts that should travel with the draft
DRAFT_SIBLINGS = {
    "beyond_recall_v11_8_draft": ["beyond_recall_v11_8_draft_with_figures.docx"],
}

# Matching export scripts to archive alongside drafts
EXPORT_SCRIPTS = [
    "export_v11_to_docx.py",
    "export_v11_1_to_docx.py",
    "export_v11_2_to_docx.py",
    "export_v11_8_to_docx.py",
    "export_v11_9_to_docx.py",
    "export_v11_9_1_to_docx.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    moves: list[tuple[Path, Path]] = []

    # Drafts
    for stem in DRAFTS:
        for ext in DRAFT_EXTENSIONS:
            src = REPO / "docs" / f"{stem}{ext}"
            if src.exists():
                dst = ARCHIVE_ROOT / f"{stem}{ext}"
                moves.append((src, dst))
        for sib in DRAFT_SIBLINGS.get(stem, []):
            src = REPO / "docs" / sib
            if src.exists():
                dst = ARCHIVE_ROOT / sib
                moves.append((src, dst))

    # Export scripts
    for name in EXPORT_SCRIPTS:
        src = REPO / "scripts" / name
        if src.exists():
            dst = ARCHIVE_ROOT / "scripts" / name
            moves.append((src, dst))

    print(f"{'APPLY' if args.apply else 'DRY-RUN'} — pre-v11.9.5 archival\n")
    total_bytes = 0
    for src, dst in moves:
        size = src.stat().st_size
        total_bytes += size
        print(f"  {src.relative_to(REPO)}  ({size:,} bytes)")
        print(f"    -> {dst.relative_to(REPO)}")
        if args.apply:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
            except PermissionError as e:
                print(f"      LOCKED — skip: {e}")

    print(f"\n{len(moves)} items, {total_bytes/1024/1024:.1f} MB total")

    if args.apply:
        # Write/update the policy note inside the archive directory
        ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
        readme = ARCHIVE_ROOT / "README.md"
        readme.write_text(
            "# Pre-v11.9.5 draft archive\n\n"
            "This directory contains paper drafts and their matching export scripts from "
            "the v11 through v11.9.1 cycle. They are preserved as historical reference and "
            "are NOT the editing target.\n\n"
            "**Public-repo policy:** Per Aarik's 2026-05-11 direction, only the locked "
            "final-version paper and its directly-cited supporting artifacts will be "
            "included in the public-launch repo. This `_archive_pre_v11_9_5/` directory "
            "is excluded from the public-launch carve-out.\n\n"
            "**v10.1 release-frozen baseline** at `docs/beyond_recall_v10_1_draft.{md,docx}` "
            "stays at `docs/` root as the preserved citable baseline per longstanding "
            "AGENTS.md convention.\n\n"
            "**Current working draft** at `docs/beyond_recall_v11_9_8_draft.{md,docx}` "
            "(or the most recent v11.9.x at the time of read).\n\n"
            "To restore a draft: `git mv docs/_archive_pre_v11_9_5/<file> docs/<file>`. The "
            "matching export script lives at `docs/_archive_pre_v11_9_5/scripts/<file>`.\n",
            encoding="utf-8",
        )
        print(f"\nWrote policy note: {readme.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
