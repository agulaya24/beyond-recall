"""One-shot diff analysis between v11.9.7 lock (2026-05-10) and v12.1 lock (2026-05-13).

Buckets MISSING / NEW / CHANGED by top-level directory and prints a summary plus
the explicit v12 / v12.1 paper artifact list. Output is the body of the diff
section in `docs/reviews/v12_1_repo_lock_report_20260513.md`.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

REPO = Path(__file__).resolve().parent.parent
PRIOR = REPO / "docs" / "reviews" / "repo_lock_manifest_v11_9_7_cycle_20260510.json"
CURR = REPO / "docs" / "repo_lock_manifest_20260513.json"


def top_dir(path: str) -> str:
    parts = path.split("/", 1)
    return parts[0] if len(parts) > 1 else "(root)"


def main() -> int:
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    curr = json.loads(CURR.read_text(encoding="utf-8"))

    prior_by_path = {e["path"]: e for e in prior["entries"]}
    curr_by_path = {e["path"]: e for e in curr["entries"]}

    missing: list[dict] = []   # in prior, not in current
    new: list[dict] = []       # in current, not in prior
    changed: list[tuple[dict, dict]] = []   # in both, sha differs

    for path, e in prior_by_path.items():
        if path not in curr_by_path:
            missing.append(e)
            continue
        ce = curr_by_path[path]
        if ce["sha256"] != e["sha256"]:
            changed.append((e, ce))

    for path, e in curr_by_path.items():
        if path not in prior_by_path:
            new.append(e)

    # Bucket by top-level dir
    bucket_missing: dict[str, list[dict]] = defaultdict(list)
    bucket_new: dict[str, list[dict]] = defaultdict(list)
    bucket_changed: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for e in missing:
        bucket_missing[top_dir(e["path"])].append(e)
    for e in new:
        bucket_new[top_dir(e["path"])].append(e)
    for pair in changed:
        bucket_changed[top_dir(pair[0]["path"])].append(pair)

    all_dirs = sorted(set(bucket_missing) | set(bucket_new) | set(bucket_changed))

    print(f"PRIOR manifest sha: {prior['manifest_sha256']}")
    print(f"CURR  manifest sha: {curr['manifest_sha256']}")
    print(f"Files: prior={prior['file_count']:,}  current={curr['file_count']:,}")
    print(f"Bytes: prior={prior['total_bytes']:,}  current={curr['total_bytes']:,}  delta={curr['total_bytes']-prior['total_bytes']:+,}")
    print(f"Totals: MISSING={len(missing)}  NEW={len(new)}  CHANGED={len(changed)}")
    print()

    print(f"{'directory':<40} {'changed':>8} {'new':>8} {'missing':>8} {'net Δ bytes':>14}")
    print("-" * 80)
    for d in all_dirs:
        c = len(bucket_changed[d])
        n = len(bucket_new[d])
        m = len(bucket_missing[d])
        delta = sum(e["size_bytes"] for e in bucket_new[d]) - sum(e["size_bytes"] for e in bucket_missing[d])
        for pre, post in bucket_changed[d]:
            delta += post["size_bytes"] - pre["size_bytes"]
        print(f"{d:<40} {c:>8} {n:>8} {m:>8} {delta:>+14,}")

    # v12 / v12.1 paper artifacts highlight
    print("\n--- v12 / v12.1 paper artifacts present in current lock ---")
    for e in curr["entries"]:
        if "v12" in e["path"]:
            tag = "NEW" if e["path"] in {x["path"] for x in new} else ("CHG" if any(p["path"] == e["path"] for p, _ in changed) else "SAME")
            print(f"  {tag:<4} {e['size_bytes']/1024:>8.1f} KB  {e['path']}  {e['sha256'][:12]}")

    # Notable CHANGED highlights
    print("\n--- Top 20 CHANGED by absolute byte delta ---")
    sorted_changed = sorted(changed, key=lambda p: -abs(p[1]["size_bytes"] - p[0]["size_bytes"]))[:20]
    for pre, post in sorted_changed:
        d = post["size_bytes"] - pre["size_bytes"]
        print(f"  {d:>+14,} bytes  {post['path']}  {pre['sha256'][:8]} -> {post['sha256'][:8]}")

    # All MISSING (so user can audit)
    print("\n--- All MISSING (deleted since prior) ---")
    for e in sorted(missing, key=lambda x: x["path"]):
        print(f"  {e['size_bytes']:>10,}  {e['path']}")

    # All NEW
    print("\n--- All NEW (added since prior) ---")
    for e in sorted(new, key=lambda x: x["path"]):
        print(f"  {e['size_bytes']:>10,}  {e['path']}")

    # All CHANGED
    print("\n--- All CHANGED ---")
    for pre, post in sorted(changed, key=lambda p: p[1]["path"]):
        d = post["size_bytes"] - pre["size_bytes"]
        print(f"  {d:>+12,}  {post['path']}  {pre['sha256'][:8]} -> {post['sha256'][:8]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
