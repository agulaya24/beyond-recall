"""Sanity check: confirm qid overlap between Letta main-study judgments and the
new full-stack BL judgments."""
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
# This script also depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
MS_RESULTS = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results")
FULLSTACK_DIR = REPO / "docs" / "research" / "_letta_rerun" / "fullstack_named"


def check(subject, letta_base, bl_path):
    with open(os.path.join(letta_base, "letta_memory_haiku_judgments_haiku.json"), encoding="utf-8") as f:
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
    os.path.join(MS_RESULTS, "run_fullstack_hamerton_20260411_231237"),
    str(FULLSTACK_DIR / "hamerton_fullstack_judgments_haiku.json"),
)
check(
    "EBERS",
    os.path.join(MS_RESULTS, "global_ebers"),
    str(FULLSTACK_DIR / "ebers_fullstack_judgments_haiku.json"),
)
check(
    "BABUR",
    os.path.join(MS_RESULTS, "global_babur"),
    str(FULLSTACK_DIR / "babur_fullstack_judgments_haiku.json"),
)
