"""Analyze score bands: per-band statistics including judge disagreement, response length,
subject distribution, and response-form features (hedging, refusal, specificity).
"""
import json
import re
from collections import Counter, defaultdict
from statistics import mean, stdev

POOL = "C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/_score_band_pool.json"
with open(POOL, "r", encoding="utf-8") as f:
    pool = json.load(f)

REFUSAL_PATTERNS = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

HEDGE_PATTERNS = [
    r"\b(?:likely|probably|perhaps|possibly|might|could|may|would likely|seems?|appears?|suggest)\b",
    r"\bgenerally speaking\b",
    r"\bit is reasonable to\b",
    r"\bwe might (?:imagine|infer|conjecture)\b",
]
HEDGE_RE = re.compile("|".join(HEDGE_PATTERNS), re.IGNORECASE)

SPECIFIC_PATTERNS = [
    r"\bspecifically\b",
    r"\bnamely\b",
    r"\bthe .* would be\b",
    r"\bwill\b",
    r'"[^"]{10,}"',  # direct quotes >= 10 chars
]
SPECIFIC_RE = re.compile("|".join(SPECIFIC_PATTERNS), re.IGNORECASE)


def analyze_response(text):
    return {
        "len_chars": len(text),
        "len_words": len(text.split()),
        "refusal_hits": len(REFUSAL_RE.findall(text)),
        "hedge_hits": len(HEDGE_RE.findall(text)),
        "specific_hits": len(SPECIFIC_RE.findall(text)),
        "has_quote": '"' in text,
        "starts_refusal": bool(re.match(r"^\s*(?:I (?:cannot|can't|don't)|The retrieved facts (?:do not|don't))", text, re.IGNORECASE)),
    }


# For each band, compute aggregate stats + sample records
print("# Score band analysis\n")
band_report = {}
for band_name, records in pool["bands"].items():
    if not records:
        continue
    stats = {
        "n_in_sample": len(records),
        "subjects_represented": sorted(set(r["subject"] for r in records)),
        "conditions_represented": Counter(r["condition"] for r in records),
        "mean_of_means": round(mean(r["mean_score"] for r in records), 3),
        "mean_judge_stdev": round(mean(stdev(r["scores"]) if len(r["scores"]) > 1 else 0 for r in records), 3),
        "mean_judge_range": round(mean(max(r["scores"]) - min(r["scores"]) for r in records), 3),
        "mean_resp_words": round(mean(len(r["response"].split()) for r in records), 1),
        "median_resp_words": sorted(len(r["response"].split()) for r in records)[len(records) // 2],
        "mean_refusal_hits": round(mean(analyze_response(r["response"])["refusal_hits"] for r in records), 2),
        "mean_hedge_hits": round(mean(analyze_response(r["response"])["hedge_hits"] for r in records), 2),
        "mean_specific_hits": round(mean(analyze_response(r["response"])["specific_hits"] for r in records), 2),
        "n_starts_refusal": sum(1 for r in records if analyze_response(r["response"])["starts_refusal"]),
    }
    # Judge vector diversity: how often do scores span >= 2 points?
    stats["n_judge_range_ge_2"] = sum(1 for r in records if max(r["scores"]) - min(r["scores"]) >= 2)
    stats["n_judge_range_ge_3"] = sum(1 for r in records if max(r["scores"]) - min(r["scores"]) >= 3)
    band_report[band_name] = stats
    print(f"## {band_name}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()

# Save band report
with open("C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/_score_band_stats.json", "w", encoding="utf-8") as f:
    json.dump(band_report, f, indent=2)

# Also: histogram of judge score vectors across ALL records (from pool, not just sample)
# Use the full pool by reloading the records file? we only saved sample. Good enough for now.
