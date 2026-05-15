#!/usr/bin/env python3
"""carve_public_launch_branch_20260511.py

Carve out files that should NOT live in the public arXiv-launch repo and
produce a `public-launch` git branch whose tree is the publishable subset.

Modes
-----
(default)        dry-run -- print a summary of what WOULD be excluded
--inventory      write a markdown inventory report under docs/reviews/
--apply          actually create the `public-launch` branch and `git rm` excluded paths

Hard rules
----------
* DEFAULT is dry-run. Nothing destructive runs without --apply.
* --apply REQUIRES a clean working tree; aborts otherwise.
* Script NEVER pushes. User pushes manually after review.
* Anything paper-cited (per docs/research/TRACEABILITY_MATRIX.json) MUST NOT be excluded.
  If the rule set would exclude such a file, the script flags it and refuses to apply.
* docs/research/ is KEPT WHOLESALE by default (cascade risk: HIGH).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent  # memory-study-repo/
TRACEABILITY_MATRIX = REPO_ROOT / "docs" / "research" / "TRACEABILITY_MATRIX.json"
INVENTORY_PATH = REPO_ROOT / "docs" / "reviews" / "public_launch_carveout_inventory_20260511.md"
BRANCH_NAME = "public-launch"

# Directories excluded outright (recursively). Stored as forward-slash POSIX
# paths relative to REPO_ROOT; trailing slash optional. Matched as path
# prefixes against forward-slash repo-relative paths.
EXCLUDE_DIRS = [
    "docs/reviews/",
    "docs/_archive_pre_v11_9_5/",
    "_archive/",                       # top-level _light_clean archive
    "scripts/_archive/",
    "scripts/_v10_verification/",
    "scripts/_v11_validation/",
    "scripts/_judge_invocation/__pycache__/",
    "logs/",
    "build/",                          # latex intermediates
    "charts/",                         # pre-v8 era
    "docs/internal/",
    "docs/archive/",
    "docs/versions/",
]

# Glob patterns matched against forward-slash repo-relative paths.
EXCLUDE_PATTERNS = [
    "scripts/_audit_*.py",
    "scripts/_dryrun_*.py",
    "scripts/_v11_emit_*.py",
    "scripts/_v11_audit_paper_numbers*.py",
    "scripts/_v11_paper_numbers*.py",
    "scripts/_v10_battery_sensitivity*.py",
    "scripts/_v10_coupling_sensitivity*.py",
    "scripts/_v10_pipeline_variance*.py",
    "scripts/_calibration_*.py",
    "scripts/_retry_*.py",
    "scripts/_groq_*.py",
    "scripts/_inspect_*.py",
    "scripts/_check_*.py",
    "scripts/_compute_*.py",
    "scripts/_build_v11_comment_index*.py",
    "scripts/_build_reference_docx*.py",
    "scripts/_emit_*.py",
    "scripts/_figure_style*.py",
    "scripts/_table_4_6_5judge_recompute*.py",
    "scripts/_topk_*.py",
    "scripts/_robustness_*.py",
    "scripts/_verify_n100_*.py",
    "scripts/_rerun_*.py",
    "scripts/panel_review_*.py",
    "scripts/light_cleanup_*.py",
    "scripts/archive_pre_v11_9_5_*.py",
    "scripts/build_research_traceability_*.py",
    "scripts/generate_repo_lock_manifest_*.py",
    "scripts/diff_*.py",
    "scripts/list_v11_*.py",
    "scripts/index_study_repo.py",
    "**/__pycache__/**",
    "**/__pycache__",
    "**/*.pyc",
    "~$*.docx",
    "**/~$*.docx",
    "~WRL*.tmp",
    "**/~WRL*.tmp",
    "**/.DS_Store",
]

# Files that MUST be kept regardless of pattern matches above. Paths are
# repo-relative POSIX strings. Override applies to exact files; for trees
# we use the KEEP_PREFIX list below.
KEEP_OVERRIDES = {
    "scripts/export_v11_9_8_to_docx.py",
    "scripts/build_arxiv_pdf.sh",
    "scripts/install_amscls.sh",
    "scripts/install_tex_packages.sh",
    "scripts/tlmgr_self_update.sh",
}

# Whole-tree keeps: any path under these prefixes is force-kept.
KEEP_PREFIXES = [
    "docs/supplementary/",
    # docs/research/ kept wholesale -- cascade risk on exclusion is HIGH.
    # Per spec: default to keeping until Aarik says otherwise.
    "docs/research/",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_git(args: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in the repo root."""
    cmd = ["git", "-C", str(REPO_ROOT), *args]
    return subprocess.run(
        cmd,
        check=check,
        text=True,
        capture_output=capture,
    )


def posix(p: Path) -> str:
    """Repo-relative POSIX path."""
    return p.relative_to(REPO_ROOT).as_posix()


def iter_repo_files() -> Iterable[Path]:
    """Yield every tracked file under REPO_ROOT according to git ls-files.

    Falls back to a filesystem walk if git ls-files fails (unlikely; the
    --apply path also needs git). We use the git inventory because that
    is what `git rm` operates on.
    """
    try:
        result = run_git(["ls-files"], check=True)
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            yield REPO_ROOT / line
    except subprocess.CalledProcessError:
        for p in REPO_ROOT.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                yield p


def match_dir_rule(rel: str) -> str | None:
    """Return the matching EXCLUDE_DIRS prefix, or None."""
    for d in EXCLUDE_DIRS:
        prefix = d if d.endswith("/") else d + "/"
        if rel.startswith(prefix):
            return d
    return None


def match_pattern_rule(rel: str) -> str | None:
    """Return the first matching EXCLUDE_PATTERNS glob, or None."""
    for pat in EXCLUDE_PATTERNS:
        # fnmatch handles ** via recursive glob when used with PurePath.match,
        # but fnmatch.fnmatch itself does NOT understand **. We translate by
        # checking via pathlib.PurePosixPath.match for patterns containing **,
        # and fall back to fnmatch otherwise.
        if "**" in pat:
            try:
                if Path(rel).match(pat) or fnmatch.fnmatch(rel, pat.replace("**/", "*").replace("/**", "")):
                    return pat
            except ValueError:
                pass
            # secondary check: substring-based, e.g. "__pycache__"
            if "__pycache__" in pat and "__pycache__" in rel.split("/"):
                return pat
            if pat == "**/*.pyc" and rel.endswith(".pyc"):
                return pat
            if pat == "**/.DS_Store" and rel.endswith(".DS_Store"):
                return pat
            if pat in ("**/~$*.docx",) and Path(rel).name.startswith("~$") and rel.endswith(".docx"):
                return pat
            if pat in ("**/~WRL*.tmp",) and Path(rel).name.startswith("~WRL") and rel.endswith(".tmp"):
                return pat
        else:
            if fnmatch.fnmatch(rel, pat):
                return pat
    return None


def is_force_kept(rel: str) -> str | None:
    """Return a description of the keep-rule that protects this file, or None."""
    if rel in KEEP_OVERRIDES:
        return f"KEEP_OVERRIDES exact: {rel}"
    for prefix in KEEP_PREFIXES:
        if rel.startswith(prefix):
            return f"KEEP_PREFIX: {prefix}"
    return None


def classify_file(rel: str) -> tuple[str, str | None, str | None]:
    """Return (decision, rule, keep_reason).

    decision in {"keep", "exclude"}.
    rule is the matching exclude rule when excluded, else None.
    keep_reason is set when an override saved an otherwise-excluded file.
    """
    dir_rule = match_dir_rule(rel)
    pat_rule = match_pattern_rule(rel)
    if dir_rule is None and pat_rule is None:
        return "keep", None, None

    keep_reason = is_force_kept(rel)
    if keep_reason:
        return "keep", None, keep_reason

    return "exclude", dir_rule or pat_rule, None


def load_traceability() -> set[str]:
    """Return the set of repo-relative POSIX paths the paper cites."""
    if not TRACEABILITY_MATRIX.exists():
        return set()
    try:
        data = json.loads(TRACEABILITY_MATRIX.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"WARN: could not parse traceability matrix: {exc}", file=sys.stderr)
        return set()
    cited: set[str] = set()
    for entry in data.get("paper_referenced_files", []):
        path = entry.get("path")
        if path:
            cited.add(path)
        for supp_path in (entry.get("supplementary_refs") or {}):
            cited.add(supp_path)
    return cited


# ---------------------------------------------------------------------------
# Classification pass
# ---------------------------------------------------------------------------

def classify_all() -> dict:
    """Walk the repo and bucket every file."""
    excluded: list[tuple[str, str, int]] = []         # (rel, rule, size)
    kept: list[tuple[str, int]] = []                  # (rel, size)
    overrides_fired: list[tuple[str, str]] = []       # (rel, keep_reason)
    research_excluded: list[str] = []                 # should be empty

    for path in iter_repo_files():
        rel = posix(path)
        # `git ls-files` can list paths that are deleted in the working tree
        # but still in the index. We still want to classify them so the
        # inventory reflects the full tracked set; size falls back to 0.
        try:
            size = path.stat().st_size if path.exists() else 0
        except OSError:
            size = 0

        decision, rule, keep_reason = classify_file(rel)
        if decision == "exclude":
            excluded.append((rel, rule or "<unknown>", size))
            if rel.startswith("docs/research/"):
                research_excluded.append(rel)
        else:
            kept.append((rel, size))
            if keep_reason:
                overrides_fired.append((rel, keep_reason))

    cited = load_traceability()
    excluded_paths = {e[0] for e in excluded}
    cited_violations = sorted(cited & excluded_paths)

    return {
        "excluded": excluded,
        "kept": kept,
        "overrides_fired": overrides_fired,
        "research_excluded": research_excluded,
        "cited_violations": cited_violations,
        "cited_total": len(cited),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def group_by_rule(excluded: list[tuple[str, str, int]]) -> dict[str, list[tuple[str, int]]]:
    buckets: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for rel, rule, size in excluded:
        buckets[rule].append((rel, size))
    for rule in buckets:
        buckets[rule].sort()
    return dict(buckets)


def group_by_top_dir(kept: list[tuple[str, int]]) -> dict[str, list[tuple[str, int]]]:
    buckets: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for rel, size in kept:
        top = rel.split("/", 1)[0] if "/" in rel else "(repo root)"
        buckets[top].append((rel, size))
    for top in buckets:
        buckets[top].sort()
    return dict(buckets)


def print_dry_run(report: dict) -> None:
    excluded = report["excluded"]
    kept = report["kept"]

    print("=" * 72)
    print("Public-launch carveout -- DRY RUN")
    print("=" * 72)
    print(f"Repo root:           {REPO_ROOT}")
    print(f"Total files (git):   {len(excluded) + len(kept)}")
    print(f"Files to EXCLUDE:    {len(excluded)}")
    print(f"Files to KEEP:       {len(kept)}")
    print(f"Size to EXCLUDE:     {fmt_size(sum(s for _, _, s in excluded))}")
    print(f"Size to KEEP:        {fmt_size(sum(s for _, s in kept))}")
    print()
    print(f"docs/research/ excluded count: {len(report['research_excluded'])} (must be 0)")
    print(f"Paper-cited violations:        {len(report['cited_violations'])} (must be 0)")
    if report["cited_violations"]:
        print("!!! CITED FILES THAT WOULD BE REMOVED:")
        for v in report["cited_violations"]:
            print(f"    - {v}")
    print()
    print("Excluded by rule (top rules):")
    buckets = group_by_rule(excluded)
    for rule, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        sz = sum(s for _, s in items)
        print(f"  {len(items):>4} files  {fmt_size(sz):>10}  {rule}")
    print()
    print("Run with --inventory to write the full markdown inventory.")
    print("Run with --apply to create the public-launch branch.")


def write_inventory(report: dict) -> None:
    excluded = report["excluded"]
    kept = report["kept"]
    INVENTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    excl_size = sum(s for _, _, s in excluded)
    keep_size = sum(s for _, s in kept)

    lines: list[str] = []
    lines.append("# Public-launch carveout inventory -- 2026-05-11")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Repo root: `{REPO_ROOT.as_posix()}`")
    lines.append(f"Branch target: `{BRANCH_NAME}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Before | After (public-launch) |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Tracked files | {len(excluded) + len(kept)} | {len(kept)} |")
    lines.append(f"| Total size | {fmt_size(excl_size + keep_size)} | {fmt_size(keep_size)} |")
    lines.append(f"| Files removed | -- | {len(excluded)} |")
    lines.append(f"| Size removed | -- | {fmt_size(excl_size)} |")
    lines.append("")
    lines.append("## Safety checks")
    lines.append("")
    lines.append(f"- docs/research/ files in exclusion set: **{len(report['research_excluded'])}** (must be 0)")
    lines.append(f"- TRACEABILITY_MATRIX paper-cited files in exclusion set: **{len(report['cited_violations'])}** (must be 0)")
    lines.append(f"- TRACEABILITY_MATRIX total paper-cited files: {report['cited_total']}")
    if report["cited_violations"]:
        lines.append("")
        lines.append("### CITED VIOLATIONS (rule set must be adjusted)")
        for v in report["cited_violations"]:
            lines.append(f"- `{v}`")
    if report["research_excluded"]:
        lines.append("")
        lines.append("### docs/research/ violations")
        for v in report["research_excluded"]:
            lines.append(f"- `{v}`")
    lines.append("")
    lines.append("## Excluded files grouped by rule")
    lines.append("")
    buckets = group_by_rule(excluded)
    for rule, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        sz = sum(s for _, s in items)
        lines.append(f"### `{rule}` -- {len(items)} files, {fmt_size(sz)}")
        lines.append("")
        for rel, s in items:
            lines.append(f"- `{rel}` ({fmt_size(s)})")
        lines.append("")
    lines.append("## Kept files grouped by top-level directory")
    lines.append("")
    kbuckets = group_by_top_dir(kept)
    for top, items in sorted(kbuckets.items(), key=lambda kv: -len(kv[1])):
        sz = sum(s for _, s in items)
        lines.append(f"### `{top}/` -- {len(items)} files, {fmt_size(sz)}")
        lines.append("")
        # cap detail to keep inventory readable but always show counts
        if len(items) <= 200:
            for rel, s in items:
                lines.append(f"- `{rel}` ({fmt_size(s)})")
        else:
            lines.append(f"_({len(items)} files; first 50 shown for brevity)_")
            lines.append("")
            for rel, s in items[:50]:
                lines.append(f"- `{rel}` ({fmt_size(s)})")
            lines.append("- ...")
        lines.append("")
    if report["overrides_fired"]:
        lines.append("## KEEP overrides that protected files from exclusion rules")
        lines.append("")
        for rel, reason in sorted(report["overrides_fired"]):
            lines.append(f"- `{rel}` -- {reason}")
        lines.append("")
    lines.append("---")
    lines.append("Generated by `scripts/carve_public_launch_branch_20260511.py --inventory`.")
    lines.append("")
    INVENTORY_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote inventory: {INVENTORY_PATH}")


# ---------------------------------------------------------------------------
# Apply mode
# ---------------------------------------------------------------------------

def assert_clean_worktree() -> None:
    result = run_git(["status", "--porcelain"], check=True)
    if result.stdout.strip():
        print(
            "ERROR: working tree is not clean. Commit or stash before running --apply.\n"
            "Offending paths:",
            file=sys.stderr,
        )
        print(result.stdout, file=sys.stderr)
        sys.exit(2)


def assert_branch_does_not_exist() -> None:
    result = run_git(["branch", "--list", BRANCH_NAME], check=True)
    if result.stdout.strip():
        print(
            f"ERROR: branch `{BRANCH_NAME}` already exists. Delete it or pick a different name.",
            file=sys.stderr,
        )
        sys.exit(2)


def current_branch() -> str:
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=True).stdout.strip()


def apply_carveout(report: dict) -> None:
    if report["cited_violations"]:
        print("ERROR: cited-file violations exist; refusing to apply. See inventory.", file=sys.stderr)
        sys.exit(2)
    if report["research_excluded"]:
        print("ERROR: docs/research/ files in exclusion set; refusing to apply.", file=sys.stderr)
        sys.exit(2)

    assert_clean_worktree()
    assert_branch_does_not_exist()

    original_branch = current_branch()
    print(f"Current branch: {original_branch}")
    print(f"Creating branch: {BRANCH_NAME}")
    run_git(["checkout", "-b", BRANCH_NAME], capture=False)

    excluded = report["excluded"]
    print(f"Removing {len(excluded)} files via `git rm`...")

    # Batch in chunks to keep the command line manageable on Windows.
    CHUNK = 200
    paths = [rel for rel, _, _ in excluded]
    for i in range(0, len(paths), CHUNK):
        chunk = paths[i : i + CHUNK]
        try:
            run_git(["rm", "-r", "--quiet", "--", *chunk], capture=False)
        except subprocess.CalledProcessError as exc:
            print(f"git rm failed on chunk starting at {chunk[0]}: {exc}", file=sys.stderr)
            print("Aborting; switching back to original branch.", file=sys.stderr)
            run_git(["checkout", original_branch], capture=False, check=False)
            run_git(["branch", "-D", BRANCH_NAME], capture=False, check=False)
            sys.exit(3)

    commit_msg = (
        "carve: exclude private/historical artifacts from public-launch branch "
        "(per docs/reviews/public_launch_carveout_inventory_20260511.md)"
    )
    print("Committing...")
    run_git(["commit", "-m", commit_msg], capture=False)

    print()
    print("Diff summary against original branch:")
    run_git(["diff", f"{original_branch}..{BRANCH_NAME}", "--stat"], capture=False)

    print()
    print(f"Switching back to {original_branch}.")
    run_git(["checkout", original_branch], capture=False)

    print()
    print("=" * 72)
    print(f"DONE. Branch `{BRANCH_NAME}` created from `{original_branch}`.")
    print("Did NOT push. Inspect with:")
    print(f"    git diff {original_branch}..{BRANCH_NAME} --stat")
    print("Push manually when ready.")
    print("=" * 72)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--inventory", action="store_true", help="Write markdown inventory and exit.")
    g.add_argument("--apply", action="store_true", help="Create the public-launch branch.")
    args = parser.parse_args(argv)

    print(f"Stage: classify  ({REPO_ROOT})")
    report = classify_all()
    print(
        f"  -> excluded={len(report['excluded'])}  "
        f"kept={len(report['kept'])}  "
        f"cited_violations={len(report['cited_violations'])}"
    )

    if args.apply:
        print("Stage: apply")
        apply_carveout(report)
        return 0

    if args.inventory:
        print("Stage: inventory")
        write_inventory(report)
        # Also print dry-run summary for convenience.
        print()
        print_dry_run(report)
        return 0

    print("Stage: dry-run report")
    print_dry_run(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
