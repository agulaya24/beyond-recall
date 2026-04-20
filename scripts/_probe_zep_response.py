"""Look at the actual C1_zep response text to see what facts made it into generation."""
import json

p = "C:/Users/Aarik/Anthropic/memory-study-repo/results/global_ebers/zep_results.json"
with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

for qid in [3, 11, 35]:
    e = next(x for x in data if x["question_id"] == qid)
    print(f"\n===== Q{qid} =====")
    print("QUESTION:", e["question_text"])
    print("\n--- C1_zep TEXT ---")
    print(e["responses"]["C1_zep"]["text"][:1500])
    print("\n--- C1_zep prompt keys (if any) ---")
    print(list(e["responses"]["C1_zep"].keys()))
