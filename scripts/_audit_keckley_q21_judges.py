"""Inspect which judges scored Q21 across all 5 systems."""
import json
from pathlib import Path

RESULTS = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley")

for sys in ["supermemory", "baselayer", "letta", "mem0", "zep"]:
    fpath = RESULTS / f"{sys}_judgments_merged.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    cnt_parse = 0
    judges = set()
    for j in data:
        if j.get("question_id") == 21:
            judges.add(j.get("judge"))
            if j.get("parse_failure"):
                cnt_parse += 1
    print(f"{sys}: judges={sorted(judges)}, parse_fail_count={cnt_parse}")
