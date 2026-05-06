"""Re-read Letta stateful judges treating gpt54 failures correctly + test structural variance."""
import json
import os
from collections import defaultdict

BASE = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"

def load_scores(path):
    """Return dict qid -> score (1-5) or None. Drops 0/failed entries."""
    if not os.path.exists(path):
        return {}, 'missing'
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    scores = {}
    struct = None
    if isinstance(d, list):
        struct = 'list'
        for item in d:
            if isinstance(item, dict):
                qid = item.get('question_id')
                s = item.get('score') or item.get('judgment')
                if isinstance(s, (int, float)) and 1 <= s <= 5:
                    scores[qid] = s
    elif isinstance(d, dict):
        # If has judgments key
        if 'judgments' in d:
            struct = 'dict.judgments'
            for item in d['judgments']:
                qid = item.get('question_id')
                s = item.get('score')
                if isinstance(s, (int, float)) and 1 <= s <= 5:
                    scores[qid] = s
        else:
            struct = 'dict'
            for k, v in d.items():
                try:
                    qid = int(k)
                    if isinstance(v, (int, float)) and 1 <= v <= 5:
                        scores[qid] = v
                    elif isinstance(v, dict) and 'score' in v:
                        s = v['score']
                        if isinstance(s, (int, float)) and 1 <= s <= 5:
                            scores[qid] = s
                except (ValueError, TypeError):
                    pass
    return scores, struct


for subject in ("ebers", "babur"):
    print(f"\n===== {subject} =====")
    sub_dir = os.path.join(BASE, f"global_{subject}")
    judges = {}
    for j in ("haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"):
        sc, struct = load_scores(os.path.join(sub_dir, f"letta_memory_haiku_judgments_{j}.json"))
        n = len(sc)
        m = sum(sc.values())/n if n else 0.0
        print(f"  {j}: n={n:3d} struct={struct} mean={m:.3f}")
        judges[j] = sc

    # Paper-style aggregation: per-question mean of valid judges (drop 0s), then mean over questions
    # Paper says 6 judges for Letta stateful. But gpt54 failed. Let's see what 5-judge (no gpt54) gives vs 6-judge.
    print("\n  Per-question-mean aggregation:")
    for label, names in [
        ("5-judge no-gpt54 no-geminiPro", ["haiku", "sonnet", "opus", "gpt4o", "gemini_flash"]),
        ("5-judge (haiku/sonnet/opus/gpt4o/gpt54)", ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]),
        ("6-judge (+ gpt54 + gemini_flash)", ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash"]),
        ("6-judge no-gpt54 + gemini_pro", ["haiku", "sonnet", "opus", "gpt4o", "gemini_flash", "gemini_pro"]),
        ("7-judge all", ["haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro"]),
        ("non-Gemini 4-judge (haiku/sonnet/opus/gpt4o)", ["haiku", "sonnet", "opus", "gpt4o"]),
    ]:
        qs = set()
        for n in names:
            qs.update(judges.get(n, {}).keys())
        pq = []
        for qid in qs:
            js = []
            for n in names:
                if qid in judges.get(n, {}):
                    js.append(judges[n][qid])
            if js:
                pq.append(sum(js)/len(js))
        if pq:
            print(f"    {label}: {sum(pq)/len(pq):.3f} (n_q={len(pq)})")
