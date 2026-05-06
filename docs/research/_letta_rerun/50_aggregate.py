"""Part 6: aggregate BL-C2a-named results and compare to Letta stateful.
Paper-style per-question mean-across-judges then average over questions."""
import json
import os
import sys
from statistics import mean
from collections import defaultdict

# Force UTF-8 stdout on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

RERUN_DIR = r"C:\Users\Aarik\Anthropic\memory-study-repo\docs\research\_letta_rerun"
LETTA_BASE = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"

JUDGES_7 = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]
JUDGES_6_no_gp = ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash"]
JUDGES_non_gemini_4 = ["haiku", "sonnet", "opus", "gpt4o"]  # gpt54 excluded: failed on Letta stateful
JUDGES_non_gemini_5 = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]


def load_scores(path):
    """Return dict qid -> score (1-5) or {} on missing."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, list):
        out = {}
        for item in d:
            if isinstance(item, dict):
                s = item.get("score")
                if isinstance(s, (int, float)) and 1 <= s <= 5:
                    out[item.get("question_id")] = s
        return out
    return {}


def aggregate(judges_dict, judge_names):
    """Per-question mean of valid judges; then mean over questions. Returns (mean, n_q, per_question_list)."""
    qs = set()
    for n in judge_names:
        qs.update(judges_dict.get(n, {}).keys())
    pq = []
    for qid in sorted(qs):
        js = [judges_dict[n][qid] for n in judge_names if qid in judges_dict.get(n, {})]
        if js:
            pq.append(mean(js))
    if pq:
        return mean(pq), len(pq), pq
    return None, 0, []


print("\n" + "=" * 80)
print("LETTA STATEFUL vs BL-C2a-NAMED (same battery, same response model, same judges)")
print("=" * 80)

rows = []
for subject in ("ebers", "babur"):
    # Load Letta stateful judgments
    letta_judges = {}
    for j in JUDGES_7:
        p = os.path.join(LETTA_BASE, f"global_{subject}", f"letta_memory_haiku_judgments_{j}.json")
        letta_judges[j] = load_scores(p)

    # Load our BL-C2a-named judgments
    bl_judges = {}
    for j in JUDGES_7:
        p = os.path.join(RERUN_DIR, f"{subject}_judgments_{j}.json")
        bl_judges[j] = load_scores(p)

    print(f"\n----- {subject.upper()} -----")
    print(f"  Letta judgments valid counts: {{{', '.join(f'{j}:{len(letta_judges[j])}' for j in JUDGES_7)}}}")
    print(f"  BL    judgments valid counts: {{{', '.join(f'{j}:{len(bl_judges[j])}' for j in JUDGES_7)}}}")

    for label, names in [
        ("7-judge (all)", JUDGES_7),
        ("6-judge (no gemini_pro)", JUDGES_6_no_gp),
        ("non-Gemini 5-judge", JUDGES_non_gemini_5),
        ("non-Gemini 4-judge (no gpt54)", JUDGES_non_gemini_4),
    ]:
        letta_m, letta_n, letta_pq = aggregate(letta_judges, names)
        bl_m, bl_n, bl_pq = aggregate(bl_judges, names)
        letta_s = f"{letta_m:.3f}" if letta_m is not None else "—"
        bl_s = f"{bl_m:.3f}" if bl_m is not None else "—"
        if letta_m is not None and bl_m is not None:
            delta = letta_m - bl_m
            delta_s = f"{delta:+.3f}"
        else:
            delta_s = "—"
        print(f"  {label:40s} Letta={letta_s} (n_q={letta_n})  BL-C2a-named={bl_s} (n_q={bl_n})  Δ(Letta-BL)={delta_s}")
        if label == "7-judge (all)":
            rows.append((subject, letta_m, bl_m, delta))

# Final summary table
print("\n" + "=" * 80)
print("SUMMARY TABLE (7-judge per-question mean)")
print("=" * 80)
print(f"{'Subject':<10} {'Letta stateful (paper)':>25} {'BL-C2a-named (rerun)':>25} {'Δ (Letta − BL)':>20}")
print("-" * 80)
for subject, letta_m, bl_m, delta in rows:
    print(f"{subject:<10} {letta_m:>25.2f} {bl_m:>25.2f} {delta:>+20.2f}")

# Compare with the original paper comparison (anonymized + different battery): Letta stateful − BL C2a
# Per §7: Ebers Letta 3.00 vs BL C2a 1.79 => +1.21; Babur Letta 2.73 vs BL C2a 2.16 => +0.57
# Now re-compute:
print("\n" + "=" * 80)
print("ORIGINAL (different battery, same spec) vs RERUN (matched battery, same spec)")
print("=" * 80)
print(f"{'Subject':<10} {'Original Δ (paper)':>25} {'Rerun Δ (matched)':>25}")
print("-" * 80)
orig = {"ebers": ("Letta 3.00 - BL 1.79 = +1.21", 1.21),
        "babur": ("Letta 2.73 - BL 2.16 = +0.57", 0.57)}
for subject, letta_m, bl_m, delta in rows:
    orig_desc, orig_d = orig[subject]
    print(f"{subject:<10} {orig_desc:>25}   {delta:+.2f} (matched)")
    # Does the gap shrink, stay, or grow?
    change = delta - orig_d
    print(f"           {'':>25}   Δ change from original: {change:+.3f}")
