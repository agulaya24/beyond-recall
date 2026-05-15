"""Regenerate SHA-256 manifest for repo state lock at v12.1 cycle.

Sibling of `generate_repo_lock_manifest_20260510.py`. Reuses that module's
`collect_manifest()` helper so exclusion rules and hashing logic stay
identical to the prior lock, then writes outputs under the new dated paths
the v12.1 audit pass calls for.

Outputs:
  docs/repo_lock_manifest_20260513.md     (human-readable)
  docs/repo_lock_manifest_20260513.json   (machine-readable)

Re-verify later:

    python scripts/generate_repo_lock_manifest_20260510.py --verify docs/repo_lock_manifest_20260513.json
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "scripts" / "generate_repo_lock_manifest_20260510.py"

spec = importlib.util.spec_from_file_location("repo_lock_20260510", SRC)
mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
assert spec and spec.loader
spec.loader.exec_module(mod)  # type: ignore[union-attr]

LOCK_LABEL = "v12.1 cycle — repo state post-v12.1 draft (paper still active edit)"


def main() -> int:
    print("Collecting repo manifest...")
    manifest = mod.collect_manifest()
    manifest["lock_label"] = LOCK_LABEL

    # Recompute manifest_sha256 because we mutated lock_label after collect_manifest
    # built it. Strip the prior manifest_sha256 first so the body matches what a
    # fresh collect would produce with this label.
    manifest.pop("manifest_sha256", None)
    import hashlib
    body = json.dumps(manifest, separators=(",", ":"), sort_keys=True).encode("utf-8")
    manifest["manifest_sha256"] = hashlib.sha256(body).hexdigest()

    out_dir = REPO / "docs"
    out_dir.mkdir(exist_ok=True)
    json_out = out_dir / "repo_lock_manifest_20260513.json"
    md_out = out_dir / "repo_lock_manifest_20260513.md"

    json_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "# Repo lock manifest — v12.1 cycle (post-v12.1 draft)",
        "",
        f"Generated: {manifest['generated_utc']}",
        f"Manifest SHA-256: `{manifest['manifest_sha256']}`",
        f"Files covered: {manifest['file_count']:,}",
        f"Total bytes: {manifest['total_bytes']:,} ({manifest['total_mb']} MB)",
        "",
        "## Scope",
        "",
        "State snapshot of the repo at the v12.1 paper-draft cycle. Captured after v12 and v12.1 paper artifacts landed; paper itself is still under active edit. Prior lock at `docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.{md,json}` is preserved unchanged.",
        "",
        "**Excluded paths.** `.git/`, `workspace/study_vectors/`, `__pycache__/`, IDE caches, byte-compiled Python, OS metadata, Word lock-files. Exclusion rules are inherited verbatim from `scripts/generate_repo_lock_manifest_20260510.py` so the two manifests are directly comparable.",
        "",
        "## Re-verification",
        "",
        "To verify integrity of this snapshot at any later date:",
        "",
        "```",
        "python scripts/generate_repo_lock_manifest_20260510.py --verify docs/repo_lock_manifest_20260513.json",
        "```",
        "",
        "Returns a per-file diff: PRESENT and matches, CHANGED, MISSING, NEW.",
        "",
        "## Companion files",
        "",
        f"- Full per-file JSON table: `repo_lock_manifest_20260513.json`",
        f"- Prior lock (v11.9.7 cycle, 2026-05-10): `docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.{{md,json}}`",
        f"- v12.1 diff + integrity report: `docs/reviews/v12_1_repo_lock_report_20260513.md`",
        "",
        "## Top-50 largest tracked files",
        "",
        "| Size (KB) | Path | SHA-256 (first 12) |",
        "|---|---|---|",
    ]
    large = sorted(manifest["entries"], key=lambda e: -e["size_bytes"])[:50]
    for e in large:
        lines.append(f"| {e['size_bytes']//1024:,} | `{e['path']}` | `{e['sha256'][:12]}` |")

    md_out.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nFiles: {manifest['file_count']:,}")
    print(f"Bytes: {manifest['total_bytes']:,} ({manifest['total_mb']} MB)")
    print(f"Manifest SHA-256: {manifest['manifest_sha256']}")
    print(f"\nWrote:")
    print(f"  {md_out}")
    print(f"  {json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
