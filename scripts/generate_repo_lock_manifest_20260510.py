"""Generate SHA-256 manifest for repo state lock at v11.9.7 cycle (paper not yet locked).

Produces a manifest covering:
  - All files under the repo root EXCEPT the standard exclusions
    (.git, workspace/study_vectors, __pycache__, .pytest_cache, *.pyc,
    .DS_Store, large binary intermediates already in `_archive/` etc.)
  - Stable byte-level hashes per file
  - Total file count, total bytes, manifest SHA-256 of the manifest itself

Output:
  docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.md   (human-readable)
  docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.json (machine-readable)

The manifest's own SHA-256 is appended to both files so the lock state is
self-verifying. To re-verify later:

    python scripts/generate_repo_lock_manifest_20260510.py --verify <prior.json>

This is a state-snapshot, not a tag. Git tagging is deferred per Aarik's
direction ("we are going to do another run through... can we just issue a new
git tag after").
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".vscode",
    ".idea",
    "node_modules",
}

EXCLUDE_PATH_PREFIXES = [
    "workspace/study_vectors",
    "workspace/__pycache__",
]

EXCLUDE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store",
    ".swp",
    ".swo",
}


def should_skip(rel: Path) -> bool:
    parts = rel.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    rel_str = rel.as_posix()
    if any(rel_str.startswith(prefix) for prefix in EXCLUDE_PATH_PREFIXES):
        return True
    if rel.suffix in EXCLUDE_SUFFIXES:
        return True
    if rel.name.startswith("~$"):  # Word lock-files
        return True
    return False


def sha256_of_file(p: Path, buf: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while chunk := f.read(buf):
            h.update(chunk)
    return h.hexdigest()


def collect_manifest() -> dict:
    entries: list[dict] = []
    total_bytes = 0
    for p in sorted(REPO.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO)
        if should_skip(rel):
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        try:
            digest = sha256_of_file(p)
        except (OSError, PermissionError) as e:
            print(f"  SKIP {rel}: {e}", file=sys.stderr)
            continue
        entries.append({
            "path": rel.as_posix(),
            "size_bytes": size,
            "sha256": digest,
        })
        total_bytes += size

    payload = {
        "generated_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "repo_root": str(REPO),
        "lock_label": "v11.9.7 cycle — repo state pre-paper-lock (paper not yet finalized)",
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "total_mb": round(total_bytes / 1024 / 1024, 2),
        "exclusions": {
            "dirs": sorted(EXCLUDE_DIRS),
            "path_prefixes": EXCLUDE_PATH_PREFIXES,
            "suffixes": sorted(EXCLUDE_SUFFIXES),
        },
        "entries": entries,
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload["manifest_sha256"] = hashlib.sha256(body).hexdigest()
    return payload


def write_outputs(manifest: dict) -> tuple[Path, Path]:
    out_dir = REPO / "docs" / "reviews"
    out_dir.mkdir(exist_ok=True)
    json_out = out_dir / "repo_lock_manifest_v11_9_7_cycle_20260510.json"
    md_out = out_dir / "repo_lock_manifest_v11_9_7_cycle_20260510.md"

    json_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "# Repo lock manifest — v11.9.7 cycle (pre-paper-lock)",
        "",
        f"Generated: {manifest['generated_utc']}",
        f"Manifest SHA-256: `{manifest['manifest_sha256']}`",
        f"Files covered: {manifest['file_count']:,}",
        f"Total bytes: {manifest['total_bytes']:,} ({manifest['total_mb']} MB)",
        "",
        "## Scope",
        "",
        "This is a **state snapshot of the repo at the v11.9.7 paper-cycle**, captured before the paper itself is finalized. The repo is being locked now per Aarik's 2026-05-10 instruction; the paper is not. Git tagging is deferred until after one more paper run-through.",
        "",
        "**Excluded paths.** `.git/`, `workspace/study_vectors/`, `__pycache__/`, IDE caches, byte-compiled Python, OS metadata, Word lock-files.",
        "",
        "## Re-verification",
        "",
        "To verify integrity of this snapshot at any later date:",
        "",
        "```",
        "python scripts/generate_repo_lock_manifest_20260510.py --verify docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.json",
        "```",
        "",
        "Returns a per-file diff: PRESENT and matches, CHANGED, MISSING, NEW.",
        "",
        "## Backup",
        "",
        "Pre-lock tarball at `C:\\Users\\Aarik\\Anthropic\\_backups\\memory-study-repo_pre_v11_9_7_lock_20260510.tar.gz`. Tarball excludes `.git/` and `workspace/study_vectors/` (regenerable). Tarball is independent of this manifest; this manifest covers the live repo state at the same snapshot moment.",
        "",
        "## Manifest companion files",
        "",
        f"- Full per-file table: [`repo_lock_manifest_v11_9_7_cycle_20260510.json`]({json_out.name})",
        "",
        "## Top-50 largest tracked files",
        "",
    ]
    large = sorted(manifest["entries"], key=lambda e: -e["size_bytes"])[:50]
    lines.append("| Size (KB) | Path | SHA-256 (first 12) |")
    lines.append("|---|---|---|")
    for e in large:
        lines.append(f"| {e['size_bytes']//1024:,} | `{e['path']}` | `{e['sha256'][:12]}` |")

    md_out.write_text("\n".join(lines), encoding="utf-8")
    return md_out, json_out


def verify_against(prior_path: Path) -> int:
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    prior_by_path = {e["path"]: e for e in prior["entries"]}
    current = collect_manifest()
    cur_by_path = {e["path"]: e for e in current["entries"]}

    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []
    new: list[str] = []

    for path, e in prior_by_path.items():
        if path not in cur_by_path:
            missing.append(path)
            continue
        if cur_by_path[path]["sha256"] != e["sha256"]:
            changed.append((path, e["sha256"], cur_by_path[path]["sha256"]))

    for path in cur_by_path:
        if path not in prior_by_path:
            new.append(path)

    print(f"Prior manifest: {prior['manifest_sha256']}")
    print(f"Current manifest: {current['manifest_sha256']}")
    print(f"  Files: prior={prior['file_count']:,}  current={current['file_count']:,}")
    print(f"  Changed: {len(changed)}")
    print(f"  Missing (deleted since prior): {len(missing)}")
    print(f"  New (added since prior): {len(new)}")
    if changed[:10]:
        print("\nFirst 10 CHANGED:")
        for path, old, new_d in changed[:10]:
            print(f"  {path}: {old[:8]} -> {new_d[:8]}")
    if missing[:10]:
        print("\nFirst 10 MISSING:")
        for path in missing[:10]:
            print(f"  {path}")
    if new[:10]:
        print("\nFirst 10 NEW:")
        for path in new[:10]:
            print(f"  {path}")
    return 0 if (not changed and not missing and not new) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path, help="Path to prior manifest JSON to verify against")
    args = parser.parse_args()

    if args.verify:
        return verify_against(args.verify)

    print("Collecting repo manifest...")
    manifest = collect_manifest()
    md_out, json_out = write_outputs(manifest)
    print(f"\nFiles: {manifest['file_count']:,}")
    print(f"Bytes: {manifest['total_bytes']:,} ({manifest['total_mb']} MB)")
    print(f"Manifest SHA-256: {manifest['manifest_sha256']}")
    print(f"\nWrote:")
    print(f"  {md_out}")
    print(f"  {json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
