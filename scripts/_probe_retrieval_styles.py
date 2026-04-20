"""Probe retrieval style per system.

For a handful of low-baseline questions, show what each system retrieves.
Looking for whether Zep produces time-anchored graph walks, Mem0 produces
hybrid/categorized facts, Letta produces archival paragraph chunks.
"""
import json
from pathlib import Path

SUBJECT = "ebers"
QIDS = [3, 11, 21, 34]  # mix: a spec-wins case, a spec-loses case, refusal case, neutral

for sys in ["mem0", "letta", "zep"]:
    print(f"\n====== {sys.upper()} / {SUBJECT} ======")
    p = Path(f"C:/Users/Aarik/Anthropic/memory-study-repo/results/global_{SUBJECT}/{sys}_results.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for qid in QIDS:
        entry = next((e for e in data if e["question_id"] == qid), None)
        if not entry:
            continue
        retrieval = entry.get("retrieval", {})
        print(f"\n--- Q{qid}: {entry['question_text'][:120]}")
        print(f"retrieval keys: {list(retrieval.keys())}")
        # pretty print what we got
        for k, v in retrieval.items():
            if isinstance(v, list):
                print(f"  [{k}] list of {len(v)}")
                for item in v[:4]:
                    if isinstance(item, dict):
                        summary = {kk: (str(vv)[:200] if not isinstance(vv, (list, dict)) else f"<{type(vv).__name__} len={len(vv)}>") for kk, vv in item.items()}
                        print(f"    {summary}")
                    else:
                        print(f"    {type(item).__name__}: {str(item)[:260]}")
            elif isinstance(v, dict):
                print(f"  [{k}] dict keys={list(v.keys())[:8]}")
            else:
                print(f"  [{k}] = {str(v)[:160]}")
