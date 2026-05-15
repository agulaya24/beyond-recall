"""Inspect the actual C2a response data to see if spec was named or anonymized."""
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

for subject in ("ebers", "babur"):
    print(f"\n========== {subject} ==========")
    # results_v2.json — this is the v2 39-question run used in the paper for low-baseline subjects
    path = os.path.join(str(REPO / "results"), f"global_{subject}", "results_v2.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # data is a list of 39 questions
    print(f"  type: {type(data).__name__}, len: {len(data)}")
    print(f"  item 0 keys:", list(data[0].keys()))
    # Condition keys
    first = data[0]
    print(f"  item 0 condition keys:")
    for k, v in first.items():
        if isinstance(v, dict):
            print(f"    {k} (dict) keys: {list(v.keys())}")
        elif isinstance(v, str):
            print(f"    {k}: str len={len(v)}")
        else:
            print(f"    {k}: {type(v).__name__}")
    # Find C2a
    if "C2a" in first:
        c2a = first["C2a"]
        print(f"\n  C2a keys:", list(c2a.keys()) if isinstance(c2a, dict) else type(c2a).__name__)
        if isinstance(c2a, dict):
            for k, v in c2a.items():
                if isinstance(v, str):
                    print(f"    C2a.{k}: str len={len(v)}")
                    if len(v) > 500:
                        print(f"    C2a.{k} preview (first 400):", v[:400].replace("\n", " | ")[:400])

    # Peek at item 0's full content
    print(f"\n  Sample response text (first 300 chars of each string field):")
    for k, v in first.items():
        if isinstance(v, str) and len(v) > 100:
            print(f"    [{k}] ({len(v)} chars): {v[:200]}")
        elif isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, str) and len(vv) > 100:
                    print(f"    [{k}.{kk}] ({len(vv)} chars): {vv[:200]}")
