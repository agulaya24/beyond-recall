"""Dump full text of top paired examples for each of the three systems."""
import json
from statistics import mean
from pathlib import Path

EXAMPLES = [
    # (system, subject, qid, label)
    ("mem0", "ebers", 11, "spec-wins (Ebers Q11 +1.67)"),
    ("mem0", "yung_wing", 3, "spec-wins (Yung Q3 +1.67)"),
    ("mem0", "ebers", 1, "spec-loses (Ebers Q1 -1.33)"),
    ("mem0", "yung_wing", 11, "spec-loses (Yung Q11 -1.17)"),

    ("letta", "ebers", 38, "spec-wins (Ebers Q38 +2.17)"),
    ("letta", "hamerton", 33, "spec-wins (Hamerton Q33 +2.67)"),
    ("letta", "ebers", 17, "spec-loses (Ebers Q17 -1.67)"),
    ("letta", "hamerton", 59, "spec-loses (Hamerton Q59 -1.50)"),

    ("zep", "ebers", 35, "spec-wins (Ebers Q35 +2.17)"),
    ("zep", "seacole", 2, "spec-wins (Seacole Q2 +4.00)"),
    ("zep", "ebers", 18, "spec-loses (Ebers Q18 -1.33)"),
    ("zep", "seacole", 18, "spec-loses (Seacole Q18 -1.00)"),
]

ROOT = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results")
for system, subject, qid, label in EXAMPLES:
    print(f"\n\n####### {label} #######")
    cand_dirs = [ROOT / f"global_{subject}", ROOT / subject]
    sdir = next((d for d in cand_dirs if (d / f"{system}_results.json").exists()), None)
    if sdir is None:
        print(f"[missing dir for {system}/{subject}]")
        continue
    rp = sdir / f"{system}_results.json"
    jp = sdir / f"{system}_judgments_merged.json"
    with open(rp, "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(jp, "r", encoding="utf-8") as f:
        judgments = json.load(f)
    e = next((x for x in results if x["question_id"] == qid), None)
    if not e:
        print("[missing]")
        continue
    print(f"QUESTION: {e['question_text']}")
    print(f"\nHELD-OUT PASSAGE: {e['held_out_passage']}")
    c1_text = e["responses"][f"C1_{system}"]["text"]
    c3_text = e["responses"][f"C3_{system}"]["text"]
    c1_scores = [(j["judge"], j["score"]) for j in judgments if j["question_id"] == qid and j["condition"] == f"C1_{system}" and j.get("score") is not None]
    c3_scores = [(j["judge"], j["score"]) for j in judgments if j["question_id"] == qid and j["condition"] == f"C3_{system}" and j.get("score") is not None]
    print(f"\nC1 mean={mean(s for _,s in c1_scores):.2f}  scores={c1_scores}")
    print(f"C3 mean={mean(s for _,s in c3_scores):.2f}  scores={c3_scores}")
    # Retrieval facts
    facts = e.get("retrieval", {}).get("facts", [])
    fact_sample = facts[:6] if facts else []
    print(f"\nRETRIEVED FACTS (top 6): {fact_sample}")
    print(f"\n--- C1 TEXT ({len(c1_text)} ch) ---\n{c1_text[:2200]}")
    print(f"\n--- C3 TEXT ({len(c3_text)} ch) ---\n{c3_text[:2200]}")
