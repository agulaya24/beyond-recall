"""Audit Q21 deltas using multiple panel definitions to find which one matches paper."""
import json
from pathlib import Path
from statistics import mean

RESULTS = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley")
TARGET_QID = 21

PANELS = {
    "5judge_primary": {"haiku", "sonnet", "opus", "gpt4o", "gpt54"},
    "7judge_with_pro": {"haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"},
    "6judge_no_pro": {"haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash"},
    "3judge_anthropic_only": {"haiku", "sonnet", "opus"},
    "4judge_no_gpt54": {"haiku", "sonnet", "opus", "gpt4o"},
}

SYSTEMS = [
    ("Supermemory",  "supermemory_judgments_merged.json",  "C1_supermemory", "C3_supermemory"),
    ("Base Layer",   "baselayer_judgments_merged.json",    "C1_baselayer",   "C3_baselayer"),
    ("Letta",        "letta_judgments_merged.json",        "C1_letta",       "C3_letta"),
    ("Mem0",         "mem0_judgments_merged.json",         "C1_mem0",        "C3_mem0"),
    ("Zep",          "zep_judgments_merged.json",          "C1_zep",         "C3_zep"),
]

def compute(data, panel, c1_label, c3_label, drop_parse_fail=True):
    c1, c3 = [], []
    for j in data:
        if j.get("question_id") != TARGET_QID:
            continue
        if drop_parse_fail and j.get("parse_failure"):
            continue
        score = j.get("score")
        if score is None:
            continue
        judge = j.get("judge", "?")
        if judge not in panel:
            continue
        cond = j.get("condition")
        if cond == c1_label:
            c1.append(score)
        elif cond == c3_label:
            c3.append(score)
    if not c1 or not c3:
        return None
    return (mean(c1), mean(c3), mean(c3) - mean(c1), len(c1), len(c3))

print(f"{'System':<14} {'Panel':<22} {'C1':>8} {'C3':>8} {'Delta':>8} {'n1/n2':>10}")
print("-" * 75)
for sys_name, fname, c1_label, c3_label in SYSTEMS:
    fpath = RESULTS / fname
    data = json.loads(fpath.read_text(encoding="utf-8"))
    for panel_name, panel in PANELS.items():
        r = compute(data, panel, c1_label, c3_label)
        if r is None:
            print(f"{sys_name:<14} {panel_name:<22} (no match)")
            continue
        c1m, c3m, d, n1, n2 = r
        print(f"{sys_name:<14} {panel_name:<22} {c1m:>8.3f} {c3m:>8.3f} {d:>+8.3f} {n1:>4}/{n2:<4}")
    print()
