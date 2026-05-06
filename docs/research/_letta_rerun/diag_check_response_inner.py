"""Check inner structure of responses."""
import json

for subj in ("ebers", "babur"):
    path = rf"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_{subj}\letta_memory_haiku_results.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]
    print(f"=== {subj} ===")
    # Check all response shapes
    dict_keys_seen = set()
    text_lens = []
    for r in results:
        resp = r["response"]
        if isinstance(resp, dict):
            for k in resp.keys():
                dict_keys_seen.add(k)
            if "text" in resp:
                text_lens.append(len(resp["text"] or ""))
    print(f"dict keys seen: {dict_keys_seen}")
    print(f"text len: min={min(text_lens)} max={max(text_lens)} mean={sum(text_lens)/len(text_lens):.0f}")
    # Simulate what str(response) would look like
    simulated_str = str(results[0]["response"])
    print(f"str(resp)[:300]: {simulated_str[:300]}")
    print(f"str(resp) len: {len(simulated_str)}")
    print()
