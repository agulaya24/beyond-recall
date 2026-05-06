"""Quick progress check on judgment files."""
import json
import os

DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"
for s in ("ebers", "babur"):
    print(f"\n=== {s} ===")
    for j in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
        p = os.path.join(DIR, f"{s}_judgments_{j}.json")
        if not os.path.exists(p):
            print(f"  {j}: missing")
            continue
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        valid = [x["score"] for x in d if x.get("score", 0) >= 1]
        err_samples = [x.get("error", "")[:80] for x in d if x.get("error")]
        m = sum(valid)/len(valid) if valid else 0.0
        print(f"  {j}: n={len(d)} valid={len(valid)} mean={m:.3f}")
        if err_samples and not valid:
            print(f"    sample error: {err_samples[0]}")
