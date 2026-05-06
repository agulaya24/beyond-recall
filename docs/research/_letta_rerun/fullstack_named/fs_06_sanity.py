"""Sanity check: confirm qid overlap between Letta main-study judgments and the
new full-stack BL judgments."""
import json


def check(subject, letta_base, bl_path):
    with open(fr"{letta_base}\letta_memory_haiku_judgments_haiku.json", encoding="utf-8") as f:
        letta_h = json.load(f)
    with open(bl_path, encoding="utf-8") as f:
        bl_h = json.load(f)
    letta_qids = set(e["question_id"] for e in letta_h if e.get("score", 0) >= 1)
    bl_qids = set(e["question_id"] for e in bl_h if e.get("score", 0) >= 1)
    print(f"{subject}: Letta qids={len(letta_qids)}, BL qids={len(bl_qids)}, overlap={len(letta_qids & bl_qids)}")
    letta_only = sorted(letta_qids - bl_qids)
    bl_only = sorted(bl_qids - letta_qids)
    if letta_only:
        print(f"  letta-only: {letta_only[:5]} (total {len(letta_only)})")
    if bl_only:
        print(f"  bl-only:    {bl_only[:5]} (total {len(bl_only)})")


check(
    "HAMERTON",
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237",
    r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\hamerton_fullstack_judgments_haiku.json",
)
check(
    "EBERS",
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers",
    r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\ebers_fullstack_judgments_haiku.json",
)
check(
    "BABUR",
    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur",
    r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun\fullstack_named\babur_fullstack_judgments_haiku.json",
)
