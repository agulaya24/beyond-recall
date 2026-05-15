"""Find the battery used by the Letta stateful test. Compare with BL C2a battery.
Also: locate the BL spec file for ebers and babur.
"""
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# This script also depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
RESULTS_BASE = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results")
STUDY_RESULTS = str(REPO / "results")

def peek_json(path, max_bytes=2000):
    print(f"\n=== {path} ===")
    if not os.path.exists(path):
        print("  MISSING")
        return None
    size = os.path.getsize(path)
    print(f"  size: {size:,} bytes")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        print(f"  top keys: {list(data.keys())}")
        # Print structure
        for k, v in data.items():
            if isinstance(v, list):
                print(f"    {k}: list[{len(v)}]")
                if v and isinstance(v[0], dict):
                    print(f"      item 0 keys: {list(v[0].keys())}")
            elif isinstance(v, dict):
                print(f"    {k}: dict (keys: {list(v.keys())[:10]})")
            elif isinstance(v, str):
                print(f"    {k}: str len={len(v)}")
            else:
                print(f"    {k}: {v!r}"[:200])
    elif isinstance(data, list):
        print(f"  list[{len(data)}]")
        if data:
            print(f"  item 0 keys: {list(data[0].keys()) if isinstance(data[0], dict) else type(data[0]).__name__}")
    return data

# Look for batteries
for s in ("ebers", "babur"):
    print(f"\n####################")
    print(f"### {s.upper()}")
    print(f"####################")
    for candidate in [
        os.path.join(STUDY_RESULTS, f"global_{s}", "battery.json"),
        os.path.join(STUDY_RESULTS, f"global_{s}", "battery_v2.json"),
        os.path.join(STUDY_RESULTS, f"global_{s}", "battery_gpt54.json"),
    ]:
        peek_json(candidate)

    # Letta memory/stateful test result — does it embed the battery question texts?
    for candidate in [
        os.path.join(RESULTS_BASE, f"global_{s}", "letta_memory_haiku_results.json"),
    ]:
        peek_json(candidate)
