"""Sensitivity probe for Q32: recompute the exoticism cross-tab with Hamerton
reclassified from `familiar` to `marginal-familiar`. The original `familiar`
bucket has n=3 (Hamerton, Ebers, Rousseau). Moving Hamerton gives familiar=2,
marginal-familiar=2 (Cellini + Hamerton). Does the residualized exoticism effect
survive the swap?
"""
import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_JSON = REPO / "docs" / "research" / "era_modernity_cross_slice.json"

# Load the previously-computed per-subject data (already 5-judge residualized)
data = json.load(DATA_JSON.open(encoding="utf-8"))
per_subject = data["per_subject"]
MAIN_STUDY = data["main_study_subjects"]

# Reclassify Hamerton
SUBJECT_EXO_ALT = {
    "hamerton": "marginal-familiar",  # swapped
    "augustine": "non-Western",
    "babur": "non-Western",
    "bernal_diaz": "non-Western",
    "cellini": "marginal-familiar",
    "ebers": "familiar",
    "equiano": "non-Western",
    "fukuzawa": "non-Western",
    "keckley": "non-Western",
    "rousseau": "familiar",
    "seacole": "non-Western",
    "sunity_devee": "non-Western",
    "yung_wing": "non-Western",
    "zitkala_sa": "non-Western",
}


def bucket_stats(values):
    values = [v for v in values if v is not None]
    if not values:
        return (0, None, None)
    return (
        len(values),
        statistics.mean(values),
        statistics.pstdev(values) if len(values) > 1 else 0.0,
    )


def run(delta_key, label):
    print(f"\n### {label} (Hamerton reclassified)")
    buckets = defaultdict(list)
    for s in MAIN_STUDY:
        v = per_subject[s].get(delta_key)
        buckets[SUBJECT_EXO_ALT[s]].append(v)
    print("| Bucket | n | mean | std |")
    print("|---|---:|---:|---:|")
    for b in ["familiar", "marginal-familiar", "non-Western"]:
        n, m, sd = bucket_stats(buckets[b])
        if n == 0:
            print(f"| {b} | 0 | — | — |")
        else:
            print(f"| {b} | {n} | {m:+.3f} | {sd:.3f} |")


print("# Hamerton sensitivity: exoticism cross-tab with Hamerton = marginal-familiar\n")
print("Compare against §4 and §5.3 of era_modernity_cross_slice.md.")
print("\nThe relevant question is whether the residualized `familiar` signal "
      "(+0.17–0.20 on Letta/Zep/Mem0/BL) survives removing Hamerton from that bucket.")

for key, lbl in [
    ("delta_c2a_5j_resid", "§4.1 C2a residualized"),
    ("delta_c4a_5j_resid", "§4.1 C4a residualized"),
    ("delta_mem0_5j_resid", "Mem0 residualized"),
    ("delta_letta_5j_resid", "Letta residualized"),
    ("delta_zep_5j_resid", "Zep residualized"),
    ("delta_supermemory_5j_resid", "Supermemory residualized"),
    ("delta_baselayer_5j_resid", "Base Layer residualized"),
]:
    run(key, lbl)

print("\n---")
print("Compare to the original (Hamerton = familiar) residualized exoticism numbers:")
print("  Letta: familiar +0.195 / marginal-familiar +0.179 / non-Western -0.077")
print("  Zep:   familiar +0.174 / marginal-familiar +0.214 / non-Western -0.074")
print("  Mem0:  familiar +0.024 / marginal-familiar +0.203 / non-Western -0.028")
print("  BL:    familiar +0.059 / marginal-familiar +0.191 / non-Western -0.037")
print()
print("If the `familiar` bucket collapses to near-zero after removing Hamerton, the `familiar` story is Hamerton-carried — a pipeline-tuning-bias artifact in disguise. If `familiar` stays above zero, the cross-cultural hypothesis is robust.")
