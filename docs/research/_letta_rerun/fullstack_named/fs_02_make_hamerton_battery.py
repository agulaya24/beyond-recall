"""Step 2: Extract Hamerton's 39-question Letta battery from the main-study
letta_memory_haiku_results.json file and save it in the standard battery shape
(matching ebers/babur battery JSON format).

Output: _letta_rerun/fullstack_named/hamerton_letta_battery.json
"""
import json
import os

SRC = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237\letta_memory_haiku_results.json"
OUT = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\hamerton_letta_battery.json"


def main():
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    results = d.get("results", [])
    battery_qs = []
    for r in results:
        battery_qs.append({
            "question_id": r["question_id"],
            "question_text": r["question_text"],
            "held_out_passage": r.get("held_out_passage", ""),
        })
    payload = {
        "subject": "hamerton",
        "source": os.path.basename(SRC),
        "total": len(battery_qs),
        "questions": battery_qs,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    qids = sorted(q["question_id"] for q in battery_qs)
    print(f"hamerton: {len(battery_qs)} qs, qid range {qids[0]}-{qids[-1]} -> {OUT}")


if __name__ == "__main__":
    main()
