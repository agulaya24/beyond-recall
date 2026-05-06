"""Drill into RESULTS_S113 gradient for hamerton."""
import json
with open(r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\RESULTS_S113.json", encoding="utf-8") as f:
    data = json.load(f)
grad = data["gradient"]
print(f"gradient top-type: {type(grad).__name__}")
if isinstance(grad, dict):
    print(f"gradient keys: {list(grad.keys())[:20]}")
    if "hamerton" in grad:
        h = grad["hamerton"]
        print(f"hamerton: {json.dumps(h, indent=2)[:1500]}")
    elif "subjects" in grad:
        subs = grad["subjects"]
        print(f"subjects keys: {list(subs.keys())[:5] if isinstance(subs, dict) else type(subs).__name__}")
        if isinstance(subs, dict) and "hamerton" in subs:
            print(json.dumps(subs["hamerton"], indent=2)[:2000])
elif isinstance(grad, list):
    print(f"gradient list n={len(grad)}")
    if grad:
        print(f"first item keys: {list(grad[0].keys()) if isinstance(grad[0], dict) else type(grad[0]).__name__}")
        for item in grad:
            if isinstance(item, dict) and item.get("subject", "").lower() == "hamerton":
                print(json.dumps(item, indent=2)[:2000])
                break
