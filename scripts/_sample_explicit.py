import json
d = json.load(open("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_detection_raw.json", encoding="utf-8"))
explicit = [r for r in d["rows"] if r["category"] == "explicit"]
print(f"total explicit: {len(explicit)}")
for r in explicit[:12]:
    print(f"[{r['subject_key']} Q{r['question_id']}]")
    print(f"  quote: {r['evidence_quote'][:200]}")
    print(f"  response first 300: {r['response_full'][:300].replace(chr(10),' | ')}")
    print("---")
