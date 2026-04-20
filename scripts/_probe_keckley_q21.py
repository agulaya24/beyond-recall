"""Ad-hoc probe: check Keckley Q21 refusal pattern across mem0/letta/zep.

Supermemory's C3 refused to answer Q21 and was catastrophically penalized.
This script checks whether the same refusal dynamic occurs with the other systems.
"""
import json
from statistics import mean

REFUSAL_PHRASES = [
    "i need to be direct",
    "do not contain",
    "not grounded",
    "cannot answer",
    "i should not fabricate",
    "facts provided do not",
    "cannot find",
    "i cannot directly",
]

for sys in ["mem0", "letta", "zep"]:
    print(f"\n========== {sys.upper()} Keckley Q21 ==========")
    with open(f"C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley/{sys}_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(f"C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley/{sys}_judgments_merged.json", "r", encoding="utf-8") as f:
        judgments = json.load(f)

    entry = next((e for e in results if e["question_id"] == 21), None)
    if not entry:
        print("  [missing]")
        continue

    c1_text = entry["responses"][f"C1_{sys}"]["text"]
    c3_text = entry["responses"][f"C3_{sys}"]["text"]

    c1_scores = [(j["judge"], j["score"]) for j in judgments
                 if j["question_id"] == 21 and j["condition"] == f"C1_{sys}" and j.get("score") is not None]
    c3_scores = [(j["judge"], j["score"]) for j in judgments
                 if j["question_id"] == 21 and j["condition"] == f"C3_{sys}" and j.get("score") is not None]

    print(f"C1 mean={mean(s for _,s in c1_scores):.2f}  scores={c1_scores}")
    print(f"C3 mean={mean(s for _,s in c3_scores):.2f}  scores={c3_scores}")

    c1_has_refusal = any(p in c1_text.lower() for p in REFUSAL_PHRASES)
    c3_has_refusal = any(p in c3_text.lower() for p in REFUSAL_PHRASES)
    print(f"C1 refusal-phrasing: {c1_has_refusal}")
    print(f"C3 refusal-phrasing: {c3_has_refusal}")
    print(f"C1 len={len(c1_text)}  C3 len={len(c3_text)}")
    print("--- C1 first 500 ---")
    print(c1_text[:500])
    print("--- C3 first 500 ---")
    print(c3_text[:500])
