"""Inspect Letta stateful test results for Ebers and Babur to:
 - find the final block size
 - determine whether the ceiling is per-turn or cumulative
 - identify at which cumulative size Letta rejected requests
"""
import json
import os

BASE = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"
OUT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"

def inspect(subject: str):
    path = os.path.join(BASE, f"global_{subject}", "letta_stateful_test_result.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n=== {subject} ===")
    print("subject:", data.get("subject"))
    print("chunks_total:", data.get("chunks_total"))
    print("turns:", len(data.get("turns", [])))
    print("final blocks:")
    for b in data.get("final_blocks", []):
        print(f"  label={b.get('label')} size={len(b.get('value',''))}")

    # Turn structure
    turns = data.get("turns", [])
    if turns:
        t0 = turns[0]
        print("turn 0 keys:", list(t0.keys()))
        # Peek at first turn minimally
        sample = {k: (v if not isinstance(v, (dict, list, str)) or (isinstance(v, str) and len(v) < 150) else f"<{type(v).__name__} len={len(v)}>") for k, v in t0.items()}
        print("turn 0 sample:", sample)

    # Progression: reconstruct cumulative block size per turn if possible
    # Look for errors or rejected turns
    errors = []
    sizes = []
    for i, t in enumerate(turns):
        # Likely fields: 'error', 'blocks_after', 'block_size', 'rejected', 'status'
        if isinstance(t, dict):
            if "error" in t and t["error"]:
                errors.append((i, t["error"]))
            # Try to pull cumulative block size from either 'blocks' or 'block_value_after'
            for k in ("block_size_after", "human_block_size", "block_size"):
                if k in t:
                    sizes.append((i, k, t[k]))
                    break
            # blocks field?
            if "blocks" in t and isinstance(t["blocks"], list):
                for b in t["blocks"]:
                    if isinstance(b, dict) and b.get("label") == "human":
                        sizes.append((i, "blocks[human].value len", len(b.get("value", ""))))
                        break

    print(f"errors: {len(errors)}")
    for e in errors[:5]:
        print(" ", e)
    print(f"size observations: {len(sizes)}")
    for s in sizes[:3]:
        print(" first:", s)
    for s in sizes[-3:]:
        print(" last:", s)

    # Save a summary
    summary_path = os.path.join(OUT_DIR, f"{subject}_stateful_summary.json")
    summary = {
        "subject": subject,
        "chunks_total": data.get("chunks_total"),
        "turns": len(turns),
        "final_blocks": [
            {"label": b.get("label"), "size": len(b.get("value", ""))}
            for b in data.get("final_blocks", [])
        ],
        "error_count": len(errors),
        "first_errors": errors[:10],
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved: {summary_path}")

for s in ("ebers", "babur"):
    inspect(s)
