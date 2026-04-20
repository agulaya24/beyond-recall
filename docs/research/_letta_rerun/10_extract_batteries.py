"""Extract the 40-question battery used by Letta stateful test for Ebers and Babur.
Source: letta_memory_haiku_results.json — which embeds question_id, question_text, held_out_passage."""
import json
import os

RESULTS_BASE = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"
OUT_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"

for s in ("ebers", "babur"):
    in_path = os.path.join(RESULTS_BASE, f"global_{s}", "letta_memory_haiku_results.json")
    with open(in_path, encoding="utf-8") as f:
        data = json.load(f)
    questions = []
    for r in data["results"]:
        questions.append({
            "question_id": r["question_id"],
            "question_text": r["question_text"],
            "held_out_passage": r["held_out_passage"],
        })
    print(f"\n{s}: {len(questions)} questions extracted")
    # sample
    print(f"  Q1: {questions[0]['question_text'][:100].encode('ascii', errors='replace').decode()}")
    print(f"  Q40: {questions[-1]['question_text'][:100].encode('ascii', errors='replace').decode()}")
    out_path = os.path.join(OUT_DIR, f"{s}_letta_battery.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "subject": s,
            "source": "letta_memory_haiku_results.json (embedded battery from Letta stateful test)",
            "count": len(questions),
            "questions": questions,
        }, f, indent=2, ensure_ascii=False)
    print(f"  Written: {out_path}")
