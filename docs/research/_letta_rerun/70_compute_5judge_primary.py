"""Compute 5-judge primary means (haiku, sonnet, opus, gpt4o, gpt54) for:
  - Letta stateful block -> Haiku (letta_memory_haiku)
  - BL full-stack spec  -> Haiku (C2a)
for Hamerton, Ebers, Babur.

Two aggregation methods reported:
 (A) per-question mean across judges, then mean over questions   [paper default]
 (B) per-judge mean, then mean over judges                         [judge-level]

Both should yield near-identical results when coverage is balanced, but (A) is
the canonical paper method (see letta_stateful_matched_rerun.md Part 6).
"""
import json, os
from collections import defaultdict

RERUN_DIR = os.path.dirname(os.path.abspath(__file__))

PRIMARY_JUDGES = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]


def load_judgments(path):
    """Return list of {question_id, score, parse_failure}."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def aggregate(judgments_by_judge):
    """judgments_by_judge: {judge: [{'question_id', 'score', ...}, ...]}
    Returns (cell_mean_A, cell_mean_B, per_judge_mean, n_qids).
    """
    # Per judge, qid -> score (valid only)
    scores_by_judge = {}
    all_qids = set()
    for j, entries in judgments_by_judge.items():
        if entries is None:
            continue
        per_qid = {}
        for e in entries:
            qid = e["question_id"]
            if e.get("score", 0) >= 1 and not e.get("parse_failure"):
                per_qid[qid] = e["score"]
                all_qids.add(qid)
        scores_by_judge[j] = per_qid
    # Method A: per-question mean across available judges, then mean over qids
    per_q_means = []
    for qid in sorted(all_qids):
        vals = [scores_by_judge[j][qid] for j in scores_by_judge if qid in scores_by_judge[j]]
        if vals:
            per_q_means.append(sum(vals) / len(vals))
    cell_A = sum(per_q_means) / len(per_q_means) if per_q_means else 0
    # Method B: per-judge mean, then mean over judges
    per_judge_mean = {}
    for j, per_qid in scores_by_judge.items():
        vals = list(per_qid.values())
        if vals:
            per_judge_mean[j] = sum(vals) / len(vals)
    cell_B = sum(per_judge_mean.values()) / len(per_judge_mean) if per_judge_mean else 0
    return cell_A, cell_B, per_judge_mean, len(all_qids)


# ========= LETTA STATEFUL (letta_memory_haiku) =========
LETTA_PATHS = {
    "hamerton": r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\run_fullstack_hamerton_20260411_231237",
    "ebers":    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_ebers",
    "babur":    r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results\global_babur",
}

letta_results = {}
for subj, p in LETTA_PATHS.items():
    judgments = {}
    for j in PRIMARY_JUDGES:
        judgments[j] = load_judgments(f"{p}\\letta_memory_haiku_judgments_{j}.json")
    letta_results[subj] = aggregate(judgments)

# ========= BL FULL-STACK (C2a_full_spec) =========
# Ebers, Babur: use _letta_rerun/{subj}_judgments_{judge}.json (rerun files)
# Hamerton: haiku from analysis/judgments.json; sonnet/opus/gpt4o/gpt54 from _letta_rerun/hamerton_bl_c2a_judgments_{judge}.json

bl_results = {}

# Ebers / Babur
for subj in ("ebers", "babur"):
    judgments = {}
    for j in PRIMARY_JUDGES:
        judgments[j] = load_judgments(f"{RERUN_DIR}\\{subj}_judgments_{j}.json")
    bl_results[subj] = aggregate(judgments)

# Hamerton: build judgments dict
ham_base = LETTA_PATHS["hamerton"]
judgments = {}

# Haiku: extract from analysis/judgments.json rows with condition=C2a_full_spec
with open(f"{ham_base}\\analysis\\judgments.json", encoding="utf-8") as f:
    main = json.load(f)
haiku_entries = []
for e in main:
    if e.get("condition") == "C2a_full_spec":
        haiku_entries.append({
            "question_id": e["question_id"],
            "score": e.get("haiku_score", 0),
            "parse_failure": e.get("haiku_score", 0) == 0,
        })
judgments["haiku"] = haiku_entries

# gpt54 from analysis/gpt54_judgments.json is ALL 400-error -- ignore. Use our new file.
for j in ("sonnet", "opus", "gpt4o", "gpt54"):
    judgments[j] = load_judgments(f"{RERUN_DIR}\\hamerton_bl_c2a_judgments_{j}.json")

bl_results["hamerton"] = aggregate(judgments)

# ========= REPORT =========
print("5-JUDGE PRIMARY (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4)")
print("=" * 70)

out_rows = []

for subj in ("hamerton", "ebers", "babur"):
    lA, lB, lpj, ln = letta_results[subj]
    bA, bB, bpj, bn = bl_results[subj]
    print(f"\n--- {subj} ---")
    print(f"  Letta block -> Haiku | 5-judge primary")
    for j in PRIMARY_JUDGES:
        val = lpj.get(j, None)
        print(f"    {j:>12}: {val:.3f}" if val is not None else f"    {j:>12}: --")
    print(f"    cell mean (A per-q): {lA:.3f}  (B per-judge): {lB:.3f}  n_qids={ln}")
    print(f"  BL spec -> Haiku     | 5-judge primary")
    for j in PRIMARY_JUDGES:
        val = bpj.get(j, None)
        print(f"    {j:>12}: {val:.3f}" if val is not None else f"    {j:>12}: --")
    print(f"    cell mean (A per-q): {bA:.3f}  (B per-judge): {bB:.3f}  n_qids={bn}")
    delta_A = lA - bA
    delta_B = lB - bB
    print(f"  d (Letta - BL)  A: {delta_A:+.3f}   B: {delta_B:+.3f}")
    out_rows.append({
        "subject": subj,
        "letta_5judge_A": round(lA, 3),
        "bl_5judge_A": round(bA, 3),
        "delta_A": round(delta_A, 3),
        "letta_5judge_B": round(lB, 3),
        "bl_5judge_B": round(bB, 3),
        "delta_B": round(delta_B, 3),
        "letta_per_judge": {k: round(v, 3) for k, v in lpj.items()},
        "bl_per_judge": {k: round(v, 3) for k, v in bpj.items()},
        "n_letta": ln,
        "n_bl": bn,
    })

# Save
with open(os.path.join(RERUN_DIR, "5judge_primary_results.json"), "w", encoding="utf-8") as f:
    json.dump({"rows": out_rows, "method_A": "per-question mean across judges, then mean over questions",
               "method_B": "per-judge mean, then mean over judges"}, f, indent=2)

print("\n\n=== 7-judge vs 5-judge primary d comparison ===")
# Paper 7-judge Δ values (from letta_stateful_matched_rerun.md Table in §4.7 paper draft)
paper_7j = {
    "hamerton": {"letta": 3.24, "bl": 3.04, "delta": 0.20},  # paper §4.7 line 1346
    "ebers":    {"letta": 3.004, "bl": 2.254, "delta": 0.751},  # letta_stateful_matched_rerun.md Part 6 headline
    "babur":    {"letta": 2.725, "bl": 2.436, "delta": 0.289},
}
print(f"{'subject':<12} {'7j d':>8} {'5j-A d':>8} {'5j-B d':>8} {'shift A':>8} {'shift B':>8}")
for row in out_rows:
    s = row["subject"]
    d7 = paper_7j[s]["delta"]
    dA = row["delta_A"]
    dB = row["delta_B"]
    print(f"{s:<12} {d7:>+8.3f} {dA:>+8.3f} {dB:>+8.3f} {dA-d7:>+8.3f} {dB-d7:>+8.3f}")

print("\nWrote: _letta_rerun/5judge_primary_results.json")
