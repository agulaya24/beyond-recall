"""Check BL-side judge coverage in _letta_rerun for ebers, babur."""
import json, os
from pathlib import Path

base = str(Path(__file__).resolve().parents[3] / "docs" / "research" / "_letta_rerun")

for subj in ("ebers", "babur"):
    print(f"=== {subj} BL-C2a-named (rerun) ===")
    for j in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
        p = f"{base}\\{subj}_judgments_{j}.json"
        if not os.path.exists(p):
            print(f"  {j}: MISSING")
            continue
        with open(p, encoding="utf-8") as f:
            dd = json.load(f)
        valid = [e["score"] for e in dd if e.get("score", 0) >= 1 and not e.get("parse_failure")]
        print(f"  {j}: n={len(dd)}, valid={len(valid)}, mean={sum(valid)/len(valid):.3f}" if valid else f"  {j}: n={len(dd)} NO VALID")
