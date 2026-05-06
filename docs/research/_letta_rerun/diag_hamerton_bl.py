"""Hamerton BL C2a per-judge means."""
import json, os
base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237"

# baselayer_results has C2a responses
with open(f"{base}\\baselayer_results.json", encoding="utf-8") as f:
    data = json.load(f)
print("results keys:", list(data.keys()) if isinstance(data, dict) else "list")
if isinstance(data, dict):
    for k, v in data.items():
        if isinstance(v, list):
            print(f"  {k}: list n={len(v)}")
            if v:
                print(f"    first keys: {list(v[0].keys())}")
        else:
            print(f"  {k}: {type(v).__name__}")
elif isinstance(data, list):
    print(f"list n={len(data)}")
    if data:
        print(f"first keys: {list(data[0].keys())}")

print()
# Per-judge on baselayer_judgments
judges = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]
per_judge = {}
conditions_seen = set()
for j in judges:
    path = f"{base}\\baselayer_judgments_{j}.json"
    if not os.path.exists(path):
        print(f"  {j}: MISSING")
        continue
    with open(path, encoding="utf-8") as f:
        dd = json.load(f)
    # condition breakdown
    cond_scores = {}
    for e in dd:
        cond = e.get("condition", "?")
        conditions_seen.add(cond)
        if e.get("score", 0) >= 1 and not e.get("parse_failure"):
            cond_scores.setdefault(cond, []).append(e["score"])
    print(f"  {j}: conditions={list(cond_scores.keys())}")
    for c, vs in cond_scores.items():
        print(f"      {c}: n={len(vs)} mean={sum(vs)/len(vs):.3f}")

print()
print("All conditions seen:", conditions_seen)
