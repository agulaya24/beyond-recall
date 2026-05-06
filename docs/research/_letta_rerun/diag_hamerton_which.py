"""Figure out which judgments give 3.24 for Hamerton Letta."""
import json, os

base = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237"

for prefix in ("letta_memory_haiku", "letta_stateful"):
    print(f"=== {prefix} judgments ===")
    judges = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]
    per_judge_mean = {}
    for j in judges:
        path = f"{base}\\{prefix}_judgments_{j}.json"
        if not os.path.exists(path):
            print(f"  {j}: MISSING")
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        valid_scores = [e["score"] for e in data if e.get("score", 0) >= 1 and not e.get("parse_failure")]
        if valid_scores:
            per_judge_mean[j] = sum(valid_scores) / len(valid_scores)
            print(f"  {j}: n_valid={len(valid_scores)}/{len(data)}, mean={per_judge_mean[j]:.3f}")
        else:
            print(f"  {j}: n={len(data)}, ALL INVALID")
    # overall
    if per_judge_mean:
        vals = list(per_judge_mean.values())
        print(f"  OVERALL ({len(vals)}-judge) mean: {sum(vals)/len(vals):.3f}")
        non_gem = {k: v for k, v in per_judge_mean.items() if "gemini" not in k}
        if non_gem:
            vv = list(non_gem.values())
            print(f"  non-Gemini ({len(vv)}-judge) mean: {sum(vv)/len(vv):.3f}")
    print()
