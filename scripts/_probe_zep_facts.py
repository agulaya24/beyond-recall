"""Dig into Zep's fact structure."""
import json

p = "C:/Users/Aarik/Anthropic/memory-study-repo/results/global_ebers/zep_results.json"
with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)
e = next(x for x in data if x["question_id"] == 3)
r = e["retrieval"]
print("type of facts:", type(r["facts"]))
print("len:", len(r["facts"]))
print("first item:", type(r["facts"][0]), r["facts"][0])
# If it's a dict with list values
if isinstance(r["facts"], dict):
    for k, v in r["facts"].items():
        print(f"{k}: {type(v).__name__} len={len(v) if hasattr(v,'__len__') else '?'}")
elif isinstance(r["facts"], list):
    for i, item in enumerate(r["facts"][:5]):
        print(f"item {i}: {type(item).__name__}")
        if isinstance(item, (list, tuple)):
            print(f"  contents: {item}")
        elif isinstance(item, dict):
            print(f"  keys: {list(item.keys())}")
            print(f"  content: {json.dumps(item, indent=2)[:600]}")
        else:
            print(f"  {str(item)[:300]}")
