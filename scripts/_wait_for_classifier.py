"""Poll until classifier finishes."""
import json, time, sys
path = "C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_detection_raw.json"
target = 587
while True:
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        n = d.get("total", 0)
        print(f"total={n} counts={d.get('counts')}", flush=True)
        if n >= target:
            print("DONE", flush=True)
            sys.exit(0)
    except Exception as e:
        print(f"read err: {e}", flush=True)
    time.sleep(30)
