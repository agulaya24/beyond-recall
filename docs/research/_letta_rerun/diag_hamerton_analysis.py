"""Inspect Hamerton analysis/judgments.json."""
import json, os
base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237\analysis"

for name in ("judgments.json", "gemini_pro_judgments.json", "gpt54_judgments.json"):
    path = f"{base}\\{name}"
    if not os.path.exists(path):
        print(f"{name}: missing")
        continue
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== {name} ===")
    if isinstance(data, list):
        print(f"list n={len(data)}")
        if data:
            first = data[0]
            print(f"first keys: {list(first.keys()) if isinstance(first, dict) else type(first).__name__}")
            print(f"first item: {json.dumps(first, indent=2)[:500]}")
            # condition x judge breakdown
            from collections import defaultdict
            by = defaultdict(list)
            for e in data:
                key = (e.get("condition", "?"), e.get("judge", "?"))
                if e.get("score", 0) >= 1 and not e.get("parse_failure"):
                    by[key].append(e["score"])
            # print only C2a rows
            for (cond, judge), scores in sorted(by.items()):
                if "C2a" in cond or "2a" in cond:
                    print(f"  {cond} | {judge}: n={len(scores)} mean={sum(scores)/len(scores):.3f}")
    print()
