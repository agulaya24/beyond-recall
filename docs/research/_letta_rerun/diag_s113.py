"""Check RESULTS_S113.json for Hamerton C2a per-judge."""
import json
with open(r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\RESULTS_S113.json", encoding="utf-8") as f:
    data = json.load(f)
print("top keys:", list(data.keys()))
# Look for hamerton
if "memory_systems" in data:
    ms = data["memory_systems"]
    print(f"memory_systems keys (sample): {list(ms.keys())[:10]}")
# Look for hamerton specifically
import json as _j
def find(obj, target, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            np = f"{path}/{k}"
            if isinstance(k, str) and target.lower() in k.lower():
                print(f"HIT: {np}")
                if isinstance(v, dict):
                    print(f"  keys: {list(v.keys())[:20]}")
                elif isinstance(v, (int, float, str)):
                    print(f"  val: {v}")
                else:
                    print(f"  type: {type(v).__name__}")
            find(v, target, np)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:5]):
            find(v, target, f"{path}[{i}]")
find(data, "hamerton")
