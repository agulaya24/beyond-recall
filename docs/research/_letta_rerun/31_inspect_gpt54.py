"""Inspect the gpt54 judgment file structure."""
import json
import os

# This script depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
path = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results", "global_ebers", "letta_memory_haiku_judgments_gpt54.json")
with open(path, encoding="utf-8") as f:
    d = json.load(f)

if isinstance(d, list):
    print(f"list len={len(d)}")
    if d:
        print(f"item 0 keys: {list(d[0].keys()) if isinstance(d[0], dict) else type(d[0]).__name__}")
        print(f"item 0: {d[0]}")
        print(f"item 1: {d[1]}")
