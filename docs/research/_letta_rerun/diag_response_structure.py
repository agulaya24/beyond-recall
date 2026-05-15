"""Diagnose the structure of Letta stateful responses."""
import json
import os

# This script depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")

for subj in ("ebers", "babur"):
    path = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results", f"global_{subj}", "letta_memory_haiku_results.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    print(f"=== {subj} ===")
    print(f"n={len(results)}")
    r0 = results[0]
    print("first response type:", type(r0["response"]).__name__)
    print("first response repr[:200]:", repr(r0["response"])[:200])
    print("first response len:", len(r0["response"]) if isinstance(r0["response"], str) else "?")
    ho_lens = [len(r["held_out_passage"] or "") for r in results]
    resp_lens = [len(r["response"]) if isinstance(r["response"], str) else -1 for r in results]
    print(f"held_out: min={min(ho_lens)} max={max(ho_lens)} mean={sum(ho_lens)/len(ho_lens):.0f}")
    print(f"response: min={min(resp_lens)} max={max(resp_lens)} mean={sum(resp_lens)/len(resp_lens):.0f}")
    print()
