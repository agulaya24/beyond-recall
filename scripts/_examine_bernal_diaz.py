import json
d = json.load(open("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/wrong_spec_detection_raw.json", encoding="utf-8"))
for r in d["rows"]:
    if r["subject_key"] == "global_bernal_diaz" and r["category"] == "explicit":
        print("EXPLICIT:")
        print(r["evidence_quote"])
        print("RESPONSE FIRST 300:", r["response_full"][:300].replace("\n", " | "))
        break
print()
for r in d["rows"]:
    if r["subject_key"] == "global_bernal_diaz" and r["category"] == "misapply":
        print("MISAPPLY:")
        print(r["response_full"][:500].replace("\n", " | "))
        break
