"""Try Base Layer aggregation including parse-failure scores as 0 (i.e. counted)
to see if that produces paper's -2.2 / 3.6."""
import json
from pathlib import Path
from statistics import mean

RESULTS = Path("C:/Users/Aarik/Anthropic/memory-study-repo/results/global_keckley")
TARGET_QID = 21

PANELS = {
    "5judge_primary": {"haiku", "sonnet", "opus", "gpt4o", "gpt54"},
    "7judge_with_pro": {"haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"},
    "6judge_with_flash": {"haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash"},
    "3judge_anthropic_only": {"haiku", "sonnet", "opus"},
}

# Base Layer C1: haiku=5, sonnet=2, opus=3, gpt4o=PARSE, gpt54=PARSE, gemini_flash=PARSE
# Base Layer C3: haiku=1, sonnet=1, opus=1, gpt4o=PARSE, gpt54=PARSE, gemini_flash=PARSE

def compute_with_zeros(data, panel, c1_label, c3_label):
    """Include parse failures as score=0."""
    c1, c3 = [], []
    for j in data:
        if j.get("question_id") != TARGET_QID:
            continue
        score = j.get("score")
        if score is None:
            score = 0
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


for panel_name, panel in PANELS.items():
    fpath = RESULTS / "baselayer_judgments_merged.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    r = compute_with_zeros(data, panel, "C1_baselayer", "C3_baselayer")
    if r is None:
        print(f"{panel_name}: no match")
        continue
    c1m, c3m, d, n1, n2 = r
    print(f"BL {panel_name:<22} (zeros included): C1={c1m:.3f} C3={c3m:.3f} delta={d:+.3f} n={n1}/{n2}")

# What if paper averaged baseline 3.6 / 3.333 across the 9 low-baseline subjects' Q21 baselines for ALL
# those subjects and used that as some "typical" baseline? No, paper says specifically Q21 cell.
# Maybe the paper means to round 3.333 -> 3.3 not 3.6. Let me check if the column says ~3.6 or ~3.3 for both.
