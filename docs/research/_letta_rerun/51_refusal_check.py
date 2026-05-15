"""Check: do BL-C2a-named responses still show refusals?
If yes, this indicates the spec-alone (no facts, no narrative) can't rescue Haiku on low-baseline subjects,
even when named. That means the gap is primarily ANCHORED CONTENT (Letta's block contains corpus-derived narrative) vs.
behavioral SPEC (which doesn't contain corpus content). Not an anonymization issue."""
import json
import os
import sys
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO = Path(__file__).resolve().parents[3]
# This script also depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
DIR = str(REPO / "docs" / "research" / "_letta_rerun")

REFUSAL_MARKERS = [
    "i don't have",
    "i do not have",
    "i don't know",
    "i cannot",
    "i can't",
    "i'm not able",
    "need to flag",
    "need to be direct",
    "don't have reliable",
    "without more information",
    "cannot provide",
    "no access to",
    "unable to",
]

for subject in ("ebers", "babur"):
    path = os.path.join(DIR, f"{subject}_bl_c2a_named_responses.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    responses = data["results"]
    print(f"\n=== {subject} — BL-C2a-named refusal analysis ({len(responses)} responses) ===")
    refuses = 0
    for r in responses:
        txt = (r.get("response") or "").lower()[:500]
        hit = any(m in txt for m in REFUSAL_MARKERS)
        if hit:
            refuses += 1
    print(f"  Refusal pattern hits: {refuses}/{len(responses)} ({100*refuses/len(responses):.0f}%)")

    # Also load Letta stateful responses for comparison
    letta_path = os.path.join(
        MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results",
        f"global_{subject}", "letta_memory_haiku_results.json")
    with open(letta_path, encoding="utf-8") as f:
        ldata = json.load(f)
    lrefuses = 0
    for r in ldata["results"]:
        rv = r.get("response")
        if isinstance(rv, dict):
            rv = rv.get("text", "")
        txt = (rv or "").lower()[:500]
        if any(m in txt for m in REFUSAL_MARKERS):
            lrefuses += 1
    print(f"  Letta stateful refusal hits: {lrefuses}/{len(ldata['results'])} ({100*lrefuses/len(ldata['results']):.0f}%)")

    # Show 2 sample comparisons on SAME qid
    print(f"\n  Sample comparisons (first 3 questions):")
    for i, (bl_r, l_r) in enumerate(zip(responses, ldata["results"])):
        if i >= 3:
            break
        bl_score_avg = None
        # Aggregate BL 7-judge score for this qid
        qid = bl_r["question_id"]
        js = []
        for j in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
            jp = os.path.join(DIR, f"{subject}_judgments_{j}.json")
            if not os.path.exists(jp):
                continue
            with open(jp, encoding="utf-8") as f:
                jd = json.load(f)
            for item in jd:
                if item.get("question_id") == qid and isinstance(item.get("score"), (int, float)) and item["score"] >= 1:
                    js.append(item["score"])
        bl_score_avg = sum(js)/len(js) if js else None

        # Letta 7-judge
        lsc = []
        LBASE = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results")
        for j in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
            jp = os.path.join(LBASE, f"global_{subject}", f"letta_memory_haiku_judgments_{j}.json")
            if not os.path.exists(jp):
                continue
            with open(jp, encoding="utf-8") as f:
                jd = json.load(f)
            for item in jd:
                if item.get("question_id") == qid and isinstance(item.get("score"), (int, float)) and item["score"] >= 1:
                    lsc.append(item["score"])
        l_score_avg = sum(lsc)/len(lsc) if lsc else None

        qt = bl_r["question_text"][:120]
        ho = (bl_r["held_out_passage"] or "")[:100]
        bl_preview = (bl_r["response"] or "")[:200].replace("\n", " ")
        lrv = l_r.get("response")
        if isinstance(lrv, dict):
            lrv = lrv.get("text", "")
        l_preview = (lrv or "")[:200].replace("\n", " ")
        print(f"\n  Q{qid}: {qt}")
        print(f"    held-out: {ho}...")
        print(f"    Letta stateful (score={l_score_avg:.2f} if l_score_avg else '?'): {l_preview}")
        print(f"    BL-C2a-named  (score={bl_score_avg:.2f} if bl_score_avg else '?'): {bl_preview}")
