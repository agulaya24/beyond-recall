"""Find Hamerton C2a_full_spec response texts."""
import json, os

base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237"

# Top-level results.json has all conditions
with open(f"{base}\\results.json", encoding="utf-8") as f:
    data = json.load(f)
print(f"type: {type(data).__name__}")
if isinstance(data, list):
    print(f"n={len(data)}")
    if data:
        print(f"first keys: {list(data[0].keys())}")
        # Inspect responses structure
        if "responses" in data[0]:
            r0 = data[0]
            print(f"qid: {r0.get('question_id')}")
            print(f"responses keys: {list(r0['responses'].keys())}")
            # pick C2a
            for cond, resp in r0["responses"].items():
                if "C2a" in cond:
                    print(f"  {cond}: {type(resp).__name__}, keys={list(resp.keys()) if isinstance(resp, dict) else '?'}")
                    if isinstance(resp, dict) and "text" in resp:
                        print(f"    text len: {len(resp['text'])}")

# Compare against 39 behavioral-prediction qids from Letta battery
with open(f"{base}\\letta_memory_haiku_results.json", encoding="utf-8") as f:
    letta = json.load(f)
letta_qids = set(r["question_id"] for r in letta["results"])
print(f"Letta qids: {len(letta_qids)}")

# Find overlap
if isinstance(data, list):
    top_qids = set(r["question_id"] for r in data if "question_id" in r)
    print(f"top results qids: {len(top_qids)}")
    print(f"intersection with letta: {len(top_qids & letta_qids)}")
    # does each intersection result have a C2a response?
    c2a_found = 0
    for r in data:
        if r.get("question_id") in letta_qids:
            resps = r.get("responses", {})
            if any("C2a" in k for k in resps):
                c2a_found += 1
    print(f"C2a responses on letta-qid intersection: {c2a_found}")
