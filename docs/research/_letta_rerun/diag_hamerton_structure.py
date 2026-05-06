"""Examine Hamerton's Letta stateful and memory_haiku result structures."""
import json

base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237"

for name in ("letta_memory_haiku_results.json", "letta_stateful_predict_results.json"):
    path = f"{base}\\{name}"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== {name} ===")
    if isinstance(data, list):
        print(f"list len={len(data)}")
        if data:
            print(f"first keys: {list(data[0].keys())}")
            first = data[0]
            for k, v in first.items():
                if isinstance(v, str):
                    print(f"  {k}: str len={len(v)} [{v[:80]!r}]")
                elif isinstance(v, dict):
                    print(f"  {k}: dict keys={list(v.keys())}")
                    if "text" in v:
                        print(f"    text len={len(v['text'])} [{v['text'][:80]!r}]")
                else:
                    print(f"  {k}: {type(v).__name__} = {v}")
    elif isinstance(data, dict):
        print(f"dict keys: {list(data.keys())}")
        if "results" in data:
            res = data["results"]
            print(f"results list len={len(res)}")
            if res:
                print(f"first keys: {list(res[0].keys())}")
                first = res[0]
                for k, v in first.items():
                    if isinstance(v, str):
                        print(f"  {k}: str len={len(v)} [{v[:80]!r}]")
                    elif isinstance(v, dict):
                        print(f"  {k}: dict keys={list(v.keys())}")
                        if "text" in v:
                            print(f"    text len={len(v['text'])}")
                    else:
                        print(f"  {k}: {type(v).__name__} = {v}")
    print()

# Now check existing gpt54 judgments
for name in ("letta_memory_haiku_judgments_gpt54.json", "letta_stateful_judgments_gpt54.json"):
    path = f"{base}\\{name}"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== {name} ===")
    print(f"n={len(data)}")
    if data:
        print(f"first: {json.dumps(data[0], indent=2)[:400]}")
        # count parse failures / scores
        pf = sum(1 for e in data if e.get("parse_failure"))
        valid = sum(1 for e in data if e.get("score", 0) >= 1 and not e.get("parse_failure"))
        print(f"parse_failure: {pf}, valid: {valid}")
    print()
