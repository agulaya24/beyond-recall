"""Pull the error progression for Babur to identify the ceiling event precisely."""
import json
import os

# This script depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
path = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results", "global_babur", "letta_stateful_test_result.json")
with open(path, encoding="utf-8") as f:
    data = json.load(f)

turns = data["turns"]
# Print a chronological list of turns with error or kind != 'ingest'/'intro'
print("All turn 'kind' values:")
kinds = {}
for t in turns:
    k = t.get("kind")
    kinds[k] = kinds.get(k, 0) + 1
print(kinds)

print("\nAll errors with full message:")
error_turns = []
for i, t in enumerate(turns):
    if "error" in t and t["error"]:
        print(f"Turn {i}: kind={t.get('kind')} | error: {t['error'][:300]}")
        error_turns.append(i)

print(f"\nError turns indices: {error_turns}")
print(f"First 400-series error appears at turn index:", next((i for i, t in enumerate(turns) if t.get('error') and '400' in t['error']), None))

# Show context of turn 220-225 non-error info
print("\nContext around first 400 error:")
for i in range(218, min(228, len(turns))):
    t = turns[i]
    err = t.get("error", "")
    has_err = "ERROR" if err else ""
    rp = t.get("response_preview", "")
    if isinstance(rp, str):
        rp_preview = rp[:150].replace("\n", " ")
    else:
        rp_preview = str(rp)[:150]
    print(f"  T{i}: kind={t.get('kind')} {has_err} | resp_preview: {rp_preview}")

# Also detect the per-turn chunk sizes if available
print("\nLooking for chunk size fields per turn...")
if turns:
    key_sample = set()
    for t in turns[:3]:
        key_sample.update(t.keys())
    print("Union of keys in first 3 turns:", key_sample)
    # Print all keys from all turns (union)
    all_keys = set()
    for t in turns:
        all_keys.update(t.keys())
    print("Union of keys across all turns:", all_keys)
