"""Step 5: Aggregate 5-judge primary means for
  - Letta stateful block -> Haiku  (letta_memory_haiku)
  - BL full-stack named spec -> Haiku  (this rerun)
for Hamerton, Ebers, Babur.

Mirrors the aggregation method in 70_compute_5judge_primary.py:
  Method A: per-question mean across available judges, then mean over questions.  [paper default]
  Method B: per-judge mean, then mean over judges.

Emits:
  - 5judge_fullstack_results.json
  - RESULTS.md: side-by-side comparison vs the old unified-brief Δ.
"""
import json
import os

RERUN_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) if False else os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(RERUN_DIR)  # _letta_rerun
# This script also depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
MS_RESULTS = os.path.join(MEMORY_SYSTEM_ROOT, "data", "experiments", "memory_systems", "results")

PRIMARY_JUDGES = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]


def load_judgments(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def aggregate(judgments_by_judge):
    """Return (cell_A, cell_B, per_judge_mean, n_qids, per_q_mean_dict)."""
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
    per_q_means = {}
    for qid in sorted(all_qids):
        vals = [scores_by_judge[j][qid] for j in scores_by_judge if qid in scores_by_judge[j]]
        if vals:
            per_q_means[qid] = sum(vals) / len(vals)
    cell_A = sum(per_q_means.values()) / len(per_q_means) if per_q_means else 0.0
    per_judge_mean = {}
    for j, per_qid in scores_by_judge.items():
        vals = list(per_qid.values())
        if vals:
            per_judge_mean[j] = sum(vals) / len(vals)
    cell_B = sum(per_judge_mean.values()) / len(per_judge_mean) if per_judge_mean else 0.0
    return cell_A, cell_B, per_judge_mean, len(all_qids), per_q_means


# ===== Letta stateful block -> Haiku (from main-study) =====
LETTA_PATHS = {
    "hamerton": os.path.join(MS_RESULTS, "run_fullstack_hamerton_20260411_231237"),
    "ebers":    os.path.join(MS_RESULTS, "global_ebers"),
    "babur":    os.path.join(MS_RESULTS, "global_babur"),
}

letta_results = {}
for subj, base in LETTA_PATHS.items():
    judgments = {}
    for j in PRIMARY_JUDGES:
        judgments[j] = load_judgments(fr"{base}\letta_memory_haiku_judgments_{j}.json")
    letta_results[subj] = aggregate(judgments)


# ===== BL unified-brief named (old rerun, for transparent comparison) =====
#   Ebers/Babur: _letta_rerun/{subj}_judgments_{j}.json
#   Hamerton: haiku from analysis/judgments.json (C2a_full_spec) + the rest from _letta_rerun/hamerton_bl_c2a_judgments_{j}.json

old_bl_results = {}

for subj in ("ebers", "babur"):
    judgments = {}
    for j in PRIMARY_JUDGES:
        judgments[j] = load_judgments(fr"{PARENT_DIR}\{subj}_judgments_{j}.json")
    old_bl_results[subj] = aggregate(judgments)

ham_base = LETTA_PATHS["hamerton"]
judgments = {}
with open(fr"{ham_base}\analysis\judgments.json", encoding="utf-8") as f:
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
for j in ("sonnet", "opus", "gpt4o", "gpt54"):
    judgments[j] = load_judgments(fr"{PARENT_DIR}\hamerton_bl_c2a_judgments_{j}.json")
old_bl_results["hamerton"] = aggregate(judgments)


# ===== BL FULL-STACK NAMED (this rerun) =====
new_bl_results = {}
for subj in ("hamerton", "ebers", "babur"):
    judgments = {}
    for j in PRIMARY_JUDGES:
        judgments[j] = load_judgments(os.path.join(RERUN_DIR, f"{subj}_fullstack_judgments_{j}.json"))
    new_bl_results[subj] = aggregate(judgments)


# ===== Report =====
def fmt(n):
    return f"{n:.3f}" if n is not None else "  -  "


rows = []
md_lines = []
md_lines.append("# BL Full-Stack Named vs Letta Stateful - Matched Comparison")
md_lines.append("")
md_lines.append("**Response model:** Claude Haiku 4.5 (temperature 0)  ")
md_lines.append("**Judge panel (5-judge primary):** Haiku, Sonnet, Opus, GPT-4o, GPT-5.4  ")
md_lines.append("**Aggregation:** per-question mean across available judges, then mean over questions (Method A; paper default).  ")
md_lines.append("")
md_lines.append("This rerun replaces the BL side's compressed ~7K-char unified brief with the full layered spec (~35-40K chars), with \"this person\" replaced by the subject's surname in the anonymized global specs and a named header prepended to Hamerton's concatenated layers.")
md_lines.append("")
md_lines.append("## Headline table")
md_lines.append("")
md_lines.append("| Subject | Letta block -> Haiku | BL full-stack named -> Haiku | Δ (Letta - BL full) | BL unified-brief (old) | Δ (Letta - BL unified, old) |")
md_lines.append("|---|---:|---:|---:|---:|---:|")

for subj in ("hamerton", "ebers", "babur"):
    lA, lB, lpj, ln, lq = letta_results[subj]
    nA, nB, npj, nn, nq = new_bl_results[subj]
    oA, oB, opj, on, oq = old_bl_results[subj]
    delta_new = lA - nA
    delta_old = lA - oA
    md_lines.append(
        f"| {subj.capitalize()} | {lA:.3f} (n={ln}) | {nA:.3f} (n={nn}) | {delta_new:+.3f} | {oA:.3f} (n={on}) | {delta_old:+.3f} |"
    )
    rows.append({
        "subject": subj,
        "letta": {"mean_A": round(lA, 4), "mean_B": round(lB, 4), "per_judge": {k: round(v, 4) for k, v in lpj.items()}, "n": ln},
        "bl_fullstack_named": {"mean_A": round(nA, 4), "mean_B": round(nB, 4), "per_judge": {k: round(v, 4) for k, v in npj.items()}, "n": nn},
        "bl_unified_brief_named": {"mean_A": round(oA, 4), "mean_B": round(oB, 4), "per_judge": {k: round(v, 4) for k, v in opj.items()}, "n": on},
        "delta_fullstack": round(delta_new, 4),
        "delta_unified": round(delta_old, 4),
    })

md_lines.append("")
md_lines.append("### Per-judge breakdown (primary 5, Method A components)")
md_lines.append("")
md_lines.append("Format: Letta / BL_full_stack / BL_unified.")
md_lines.append("")
md_lines.append("| Subject | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 |")
md_lines.append("|---|---|---|---|---|---|")
for subj in ("hamerton", "ebers", "babur"):
    _, _, lpj, _, _ = letta_results[subj]
    _, _, npj, _, _ = new_bl_results[subj]
    _, _, opj, _, _ = old_bl_results[subj]
    cells = []
    for j in PRIMARY_JUDGES:
        lv = lpj.get(j); nv = npj.get(j); ov = opj.get(j)
        cells.append(f"{fmt(lv)} / {fmt(nv)} / {fmt(ov)}")
    md_lines.append(f"| {subj.capitalize()} | " + " | ".join(cells) + " |")
md_lines.append("")

# Shift magnitudes
md_lines.append("### Shift from unified brief -> full stack (same judges, same questions)")
md_lines.append("")
md_lines.append("| Subject | BL unified (old) | BL full-stack (new) | Shift | Δ vs Letta (old) | Δ vs Letta (new) | Gap closed |")
md_lines.append("|---|---:|---:|---:|---:|---:|---:|")
for subj in ("hamerton", "ebers", "babur"):
    lA, *_ = letta_results[subj]
    nA, *_ = new_bl_results[subj]
    oA, *_ = old_bl_results[subj]
    shift = nA - oA
    delta_old = lA - oA
    delta_new = lA - nA
    gap_closed = delta_old - delta_new   # how much the Letta advantage shrank (positive = gap shrank)
    md_lines.append(
        f"| {subj.capitalize()} | {oA:.3f} | {nA:.3f} | {shift:+.3f} | {delta_old:+.3f} | {delta_new:+.3f} | {gap_closed:+.3f} |"
    )
md_lines.append("")

# Honest interpretation
md_lines.append("## Interpretation")
md_lines.append("")

# Build interpretation programmatically from the numbers.
interp_lines = []
for subj in ("hamerton", "ebers", "babur"):
    lA, *_ = letta_results[subj]
    nA, *_ = new_bl_results[subj]
    oA, *_ = old_bl_results[subj]
    shift = nA - oA
    delta_new = lA - nA
    delta_old = lA - oA
    if delta_new > 0.05:
        dir_new = f"Letta still ahead by {delta_new:+.3f}"
    elif delta_new < -0.05:
        dir_new = f"BL full-stack ahead by {-delta_new:+.3f}"
    else:
        dir_new = f"parity ({delta_new:+.3f})"
    interp_lines.append(
        f"- **{subj.capitalize()}**: unified-brief BL {oA:.3f} -> full-stack BL {nA:.3f} (shift {shift:+.3f}). "
        f"Letta {lA:.3f}. {dir_new}. Old Δ was {delta_old:+.3f}, new Δ is {delta_new:+.3f}."
    )
md_lines.extend(interp_lines)
md_lines.append("")

md_lines.append("See `5judge_fullstack_results.json` for the raw numbers used to build this table.")
md_lines.append("")

# Write outputs
results_json = {
    "response_model": "claude-haiku-4-5-20251001",
    "primary_judges": PRIMARY_JUDGES,
    "method": {"A": "per-question mean across judges, then mean over questions", "B": "per-judge mean, then mean over judges"},
    "letta_side": "letta_memory_haiku main-study judgments (unchanged)",
    "bl_fullstack_named": "full-layered spec (~35-40K chars) with named surname substitution; pronouns preserved",
    "bl_unified_brief_named": "compressed unified brief (~7K chars) from prior rerun (for comparison only)",
    "rows": rows,
}
with open(os.path.join(RERUN_DIR, "5judge_fullstack_results.json"), "w", encoding="utf-8") as f:
    json.dump(results_json, f, indent=2)

with open(os.path.join(RERUN_DIR, "RESULTS.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Also print a plain table to stdout
print("5-judge primary (Method A)")
print(f"{'subject':<12} {'Letta':>8} {'BL_full':>8} {'d_full':>8} {'BL_unif':>8} {'d_unif':>8} {'shift':>8}")
for subj in ("hamerton", "ebers", "babur"):
    lA, *_ = letta_results[subj]
    nA, *_ = new_bl_results[subj]
    oA, *_ = old_bl_results[subj]
    print(f"{subj:<12} {lA:>8.3f} {nA:>8.3f} {lA-nA:>+8.3f} {oA:>8.3f} {lA-oA:>+8.3f} {nA-oA:>+8.3f}")

print("\nWrote:")
print("  " + os.path.join(RERUN_DIR, "5judge_fullstack_results.json"))
print("  " + os.path.join(RERUN_DIR, "RESULTS.md"))
