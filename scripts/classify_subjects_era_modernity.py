"""
classify_subjects_era_modernity.py
==================================

JOB 1 (Q32): Cross-slice spec-delta by era / language-modernity / content-exoticism.

For each of the 14 main-study subjects, pull:
  - C5 baseline, C2a spec-alone, C4a facts+spec, and the derived Δ_spec = C2a - C5
    (re-aggregated on the 5-judge primary panel: haiku, sonnet, opus, gpt4o, gpt54)
  - Per-system controlled Δ_spec (C3 - C1) for mem0, letta, supermemory, zep, baselayer
    (pulled from `docs/research/memory_systems_5judge_primary.md` per-subject table
     for consistency with the same 5-judge panel)

Classify each subject by:
  - era bucket: pre_1700 / 1700-1900 / post_1900
  - language modernity: modern / archaic (all corpora English; "archaic" = pre-modern
    English or pre-modern translation voice)
  - content exoticism: familiar (Western bourgeois autobiography) /
    marginal-familiar / non-Western

Then cross-tabulate era × Δ_spec (mean, std, n) for each memory system AND for §4.1 C2a/C4a.
Also report Δ_spec residualized on C5 baseline to separate era-effect from collinear-baseline-effect.

Outputs:
  docs/research/era_modernity_cross_slice.md
  docs/research/era_modernity_cross_slice.json
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
OUT_MD = REPO / "docs" / "research" / "era_modernity_cross_slice.md"
OUT_JSON = REPO / "docs" / "research" / "era_modernity_cross_slice.json"

PRIMARY_JUDGES = {"haiku", "sonnet", "opus", "gpt4o", "gpt54"}

# Subject classification. Era bucket = primary life/writing period.
# Modernity = language voice of the source text as the experiment saw it (English).
# Exoticism = content familiarity to a Western-modern baseline reader.
# Hamerton is bucketed `familiar` (per advisor note; Victorian English art-writer).
SUBJECT_CLASS = {
    # name            era_bucket     modernity  exoticism             life/work dates
    # Hamerton: default bucket = familiar (Victorian English art-writer, Western-bourgeois).
    # Sensitivity analysis below rebuckets him as marginal-familiar to test fragility of n=3 familiar cell.
    "hamerton":      ("1700-1900",  "modern",  "familiar"),           # 1834-1894 Eng
    "franklin":      ("1700-1900",  "modern",  "familiar"),           # 1706-1790 Amer
    "augustine":     ("pre_1700",   "archaic", "non-Western"),        # 354-430 CE N. Afr
    "babur":         ("pre_1700",   "archaic", "non-Western"),        # 1483-1530 Tim/Mughal
    "bernal_diaz":   ("pre_1700",   "archaic", "non-Western"),        # 1496-1584 Spain/Mex
    "cellini":       ("pre_1700",   "archaic", "marginal-familiar"),  # 1500-1571 Italy
    "ebers":         ("1700-1900",  "modern",  "familiar"),           # 1837-1898 Germ
    "equiano":       ("1700-1900",  "modern",  "non-Western"),        # 1745-1797 African-Brit
    "fukuzawa":      ("1700-1900",  "modern",  "non-Western"),        # 1835-1901 Japan
    "keckley":       ("1700-1900",  "modern",  "non-Western"),        # 1818-1907 Black Amer
    "rousseau":      ("1700-1900",  "modern",  "familiar"),           # 1712-1778 Fr/Swiss
    "seacole":       ("1700-1900",  "modern",  "non-Western"),        # 1805-1881 Jamaican-Brit
    "sunity_devee":  ("1700-1900",  "modern",  "non-Western"),        # 1864-1932 Indian
    "yung_wing":     ("1700-1900",  "modern",  "non-Western"),        # 1828-1912 Chin-Amer
    "zitkala_sa":    ("post_1900",  "modern",  "non-Western"),        # 1876-1938 Yankton Dak
}

# 14 main-study subjects (Franklin is known-figure replication, NOT part of main gradient —
# so we will classify it but keep it flagged. Section 4.1 main gradient has 14 = hamerton + 13.)
MAIN_STUDY = [
    "hamerton", "augustine", "babur", "bernal_diaz", "cellini", "ebers",
    "equiano", "fukuzawa", "keckley", "rousseau", "seacole", "sunity_devee",
    "yung_wing", "zitkala_sa",
]
# Note: Franklin is the known-figure replication; excluded from the 14-subject main study.


# Per-subject spec-delta on the 5-judge panel for each memory system.
# Source: docs/research/memory_systems_5judge_primary.md (controlled config), verified
# above as the 5-judge recompute, identical panel we use for §4.1 below.
MEMSYS_5J_CONTROLLED = {
    "hamerton":      {"mem0": +0.103, "letta": +0.387, "zep": +0.333, "supermemory": +0.144, "baselayer": -0.010},
    "sunity_devee":  {"mem0": -0.082, "letta": +0.026, "zep": +0.087, "supermemory": -0.113, "baselayer": +0.043},
    "ebers":         {"mem0": +0.149, "letta": +0.138, "zep": +0.272, "supermemory": +0.138, "baselayer": +0.077},
    "fukuzawa":      {"mem0": +0.046, "letta": +0.044, "zep": +0.026, "supermemory": -0.205, "baselayer": +0.051},
    "seacole":       {"mem0": +0.154, "letta": +0.400, "zep": +0.472, "supermemory": +0.082, "baselayer": +0.197},
    "bernal_diaz":   {"mem0": -0.026, "letta": +0.036, "zep": +0.097, "supermemory": -0.031, "baselayer": -0.077},
    "keckley":       {"mem0": -0.021, "letta": -0.021, "zep": +0.041, "supermemory": -0.267, "baselayer": -0.009},
    "yung_wing":     {"mem0": +0.328, "letta": +0.308, "zep": +0.123, "supermemory": +0.108, "baselayer": +0.333},
    "babur":         {"mem0": +0.256, "letta": +0.164, "zep": +0.041, "supermemory": +0.051, "baselayer": +0.140},
    "cellini":       {"mem0": +0.364, "letta": +0.413, "zep": +0.405, "supermemory": -0.036, "baselayer": +0.274},
    "zitkala_sa":    {"mem0": -0.123, "letta": -0.051, "zep": -0.031, "supermemory": -0.246, "baselayer": -0.272},
    "rousseau":      {"mem0": +0.108, "letta": +0.587, "zep": +0.467, "supermemory": -0.026, "baselayer": +0.333},
    "augustine":     {"mem0": +0.349, "letta": +0.223, "zep": +0.205, "supermemory": -0.040, "baselayer": +0.111},
    "equiano":       {"mem0": +0.092, "letta": +0.123, "zep": +0.072, "supermemory": -0.319, "baselayer": -0.103},
}

# -----------------------------------------------------------------------------
# Load 5-judge §4.1 C5/C2a/C4a from raw judgments (re-aggregate for consistency).
# -----------------------------------------------------------------------------


def load_global_judgments(subject):
    path = RESULTS / f"global_{subject}" / "judgments_v2.json"
    rows = []
    if path.exists():
        rows = json.load(path.open(encoding="utf-8"))
    # Normalize score to int where possible
    cleaned = []
    for r in rows:
        s = r.get("score")
        try:
            s = int(s) if s is not None and s != "" else None
        except (TypeError, ValueError):
            s = None
        pf = r.get("parse_failure")
        if isinstance(pf, str):
            pf = pf.lower() == "true"
        cleaned.append({
            "question_id": str(r.get("question_id")),
            "condition": r.get("condition"),
            "judge": r.get("judge"),
            "score": s,
            "parse_failure": bool(pf),
        })
    return cleaned


def load_hamerton_judgments():
    """Aggregated Hamerton rows (borrowed logic from scripts/recompute_5judge_primary.py)."""
    base = RESULTS / "hamerton"
    rows = []

    def normalize(cond):
        if cond == "C2c_full_wrong_spec":
            return "C2c_wrong_spec"
        if cond == "C4a_full_all_facts_plus_spec":
            return "C4a_full_facts_plus_spec"
        return cond

    harm = base / "judgments_harmonized.json"
    if harm.exists():
        for r in json.load(harm.open(encoding="utf-8")):
            try:
                s = int(r.get("score")) if r.get("score") not in (None, "") else None
            except (TypeError, ValueError):
                s = None
            pf = r.get("parse_failure")
            if isinstance(pf, str):
                pf = pf.lower() == "true"
            rows.append({
                "question_id": str(r.get("question_id")),
                "condition": normalize(r.get("condition")),
                "judge": r.get("judge"),
                "score": s,
                "parse_failure": bool(pf),
            })

    wide = base / "judgments.json"
    if wide.exists():
        for r in json.load(wide.open(encoding="utf-8")):
            cond = normalize(r.get("condition"))
            if "haiku_score" in r and r["haiku_score"] not in (None, ""):
                try:
                    rows.append({
                        "question_id": str(r["question_id"]),
                        "condition": cond,
                        "judge": "haiku",
                        "score": int(r["haiku_score"]),
                        "parse_failure": False,
                    })
                except (TypeError, ValueError):
                    pass
            if "gemini_score" in r and r["gemini_score"] not in (None, ""):
                try:
                    rows.append({
                        "question_id": str(r["question_id"]),
                        "condition": cond,
                        "judge": "gemini_flash",
                        "score": int(r["gemini_score"]),
                        "parse_failure": False,
                    })
                except (TypeError, ValueError):
                    pass

    for judge, field in [
        ("gpt54", "gpt54_score"),
        ("gemini_pro", "gemini_pro_score"),
    ]:
        p = base / f"{judge}_judgments.json"
        if p.exists():
            for r in json.load(p.open(encoding="utf-8")):
                v = r.get(field)
                if v in (None, ""):
                    continue
                try:
                    rows.append({
                        "question_id": str(r["question_id"]),
                        "condition": normalize(r.get("condition")),
                        "judge": judge,
                        "score": int(v),
                        "parse_failure": False,
                    })
                except (TypeError, ValueError):
                    pass

    for judge in ["sonnet", "opus", "gpt4o"]:
        p = base / f"{judge}_judgments.json"
        if p.exists():
            for r in json.load(p.open(encoding="utf-8")):
                try:
                    s = int(r.get("score")) if r.get("score") not in (None, "") else None
                except (TypeError, ValueError):
                    s = None
                pf = r.get("parse_failure")
                if isinstance(pf, str):
                    pf = pf.lower() == "true"
                rows.append({
                    "question_id": str(r["question_id"]),
                    "condition": normalize(r.get("condition")),
                    "judge": judge,
                    "score": s,
                    "parse_failure": bool(pf),
                })
    return rows


def aggregate_5j(rows, condition):
    """Mean over (judge means over questions) on 5-judge panel."""
    per_judge = defaultdict(list)
    for r in rows:
        if r["condition"] != condition:
            continue
        if r["judge"] not in PRIMARY_JUDGES:
            continue
        if r["score"] is None or r["parse_failure"]:
            continue
        per_judge[r["judge"]].append(r["score"])
    judge_means = [statistics.mean(s) for s in per_judge.values() if s]
    return statistics.mean(judge_means) if judge_means else None


# -----------------------------------------------------------------------------
# Cross-tab helpers
# -----------------------------------------------------------------------------


def bucket_stats(values):
    values = [v for v in values if v is not None]
    if not values:
        return {"n": 0, "mean": None, "std": None}
    return {
        "n": len(values),
        "mean": statistics.mean(values),
        "std": statistics.pstdev(values) if len(values) > 1 else 0.0,
    }


def cross_tab(subjects, class_idx, key):
    """For each class bucket, collect `key` (a function subject -> Δ) and summarize."""
    buckets = defaultdict(list)
    for s in subjects:
        bucket_label = SUBJECT_CLASS[s][class_idx]
        v = key(s)
        buckets[bucket_label].append(v)
    return {b: bucket_stats(vs) for b, vs in buckets.items()}


def ols_residuals(xs, ys):
    """Return the residuals of ys ~ xs (simple linear regression)."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return [None] * len(xs)
    mx = statistics.mean(p[0] for p in pairs)
    my = statistics.mean(p[1] for p in pairs)
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    slope = sxy / sxx if sxx else 0.0
    intercept = my - slope * mx
    return [None if (x is None or y is None) else (y - (intercept + slope * x)) for x, y in zip(xs, ys)]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    per_subject = {}

    # Load §4.1 C5/C2a/C4a per subject on 5-judge panel
    for s in MAIN_STUDY:
        if s == "hamerton":
            rows = load_hamerton_judgments()
        else:
            rows = load_global_judgments(s)
        c5 = aggregate_5j(rows, "C5_baseline")
        c2a = aggregate_5j(rows, "C2a_full_spec")
        c4a = aggregate_5j(rows, "C4a_full_facts_plus_spec")
        per_subject[s] = {
            "c5_5j": c5,
            "c2a_5j": c2a,
            "c4a_5j": c4a,
            "delta_c2a_5j": (c2a - c5) if (c2a is not None and c5 is not None) else None,
            "delta_c4a_5j": (c4a - c5) if (c4a is not None and c5 is not None) else None,
            "era": SUBJECT_CLASS[s][0],
            "modernity": SUBJECT_CLASS[s][1],
            "exoticism": SUBJECT_CLASS[s][2],
            "memsys": MEMSYS_5J_CONTROLLED.get(s, {}),
        }

    # Compute residualized deltas (Δ ~ C5 baseline) for §4.1 C2a/C4a and for each memsys
    xs_c5 = [per_subject[s]["c5_5j"] for s in MAIN_STUDY]
    for key in ["delta_c2a_5j", "delta_c4a_5j"]:
        ys = [per_subject[s][key] for s in MAIN_STUDY]
        res = ols_residuals(xs_c5, ys)
        for s, r in zip(MAIN_STUDY, res):
            per_subject[s][f"{key}_resid"] = r

    for sys_ in ["mem0", "letta", "zep", "supermemory", "baselayer"]:
        ys = [per_subject[s]["memsys"].get(sys_) for s in MAIN_STUDY]
        res = ols_residuals(xs_c5, ys)
        for s, r in zip(MAIN_STUDY, res):
            per_subject[s][f"delta_{sys_}_5j_resid"] = r

    # Build cross-tabs for each dimension, for each delta source
    CROSS_DIMS = [("era", 0), ("modernity", 1), ("exoticism", 2)]
    DELTA_SOURCES = {
        "§4.1 C2a spec-alone (C2a-C5)": lambda s: per_subject[s]["delta_c2a_5j"],
        "§4.1 facts+spec (C4a-C5)":     lambda s: per_subject[s]["delta_c4a_5j"],
        "Mem0 controlled (C3-C1)":      lambda s: per_subject[s]["memsys"].get("mem0"),
        "Letta controlled (C3-C1)":     lambda s: per_subject[s]["memsys"].get("letta"),
        "Zep controlled (C3-C1)":       lambda s: per_subject[s]["memsys"].get("zep"),
        "Supermemory controlled":       lambda s: per_subject[s]["memsys"].get("supermemory"),
        "Base Layer controlled":        lambda s: per_subject[s]["memsys"].get("baselayer"),
    }
    RESID_SOURCES = {
        "§4.1 C2a residualized on C5":  lambda s: per_subject[s].get("delta_c2a_5j_resid"),
        "§4.1 C4a residualized on C5":  lambda s: per_subject[s].get("delta_c4a_5j_resid"),
        "Mem0 residualized on C5":      lambda s: per_subject[s].get("delta_mem0_5j_resid"),
        "Letta residualized on C5":     lambda s: per_subject[s].get("delta_letta_5j_resid"),
        "Zep residualized on C5":       lambda s: per_subject[s].get("delta_zep_5j_resid"),
        "Supermemory residualized on C5": lambda s: per_subject[s].get("delta_supermemory_5j_resid"),
        "Base Layer residualized on C5": lambda s: per_subject[s].get("delta_baselayer_5j_resid"),
    }

    cross_tables = {}
    for dim_name, idx in CROSS_DIMS:
        for label, fn in DELTA_SOURCES.items():
            cross_tables[(dim_name, label)] = cross_tab(MAIN_STUDY, idx, fn)
        for label, fn in RESID_SOURCES.items():
            cross_tables[(dim_name, label)] = cross_tab(MAIN_STUDY, idx, fn)

    # JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump({
            "subject_class": {s: dict(zip(["era", "modernity", "exoticism"], c)) for s, c in SUBJECT_CLASS.items()},
            "main_study_subjects": MAIN_STUDY,
            "per_subject": per_subject,
            "cross_tables": {
                f"{d}|{lbl}": tbl for (d, lbl), tbl in cross_tables.items()
            },
            "notes": {
                "panel": "5-judge primary: haiku, sonnet, opus, gpt4o, gpt54",
                "delta_definition_41": "mean(condition) - mean(C5_baseline) per subject",
                "delta_definition_memsys": "mean(C3) - mean(C1) per subject (controlled config)",
                "residualized_delta": "residual of Δ ~ C5_baseline (simple OLS) across all 14 subjects",
                "hamerton_bucket": "familiar (Victorian English art-writer, Western-bourgeois)",
            },
        }, f, indent=2, ensure_ascii=False)

    # Markdown report
    md = []
    md.append("# Era / Modernity / Exoticism Cross-Slice of Spec Deltas (Q32)")
    md.append("")
    md.append("_Panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54). All 14 main-study subjects._")
    md.append("")
    md.append("**Question:** Do certain eras / modernity registers / content-exoticism buckets show systematically different spec deltas?")
    md.append("")
    md.append("**Method:** Each subject bucketed on three dimensions. For each bucket, report mean, std, n of Δ_spec across two data sources: (a) §4.1 controlled gradient conditions C2a (spec alone) and C4a (facts+spec), re-aggregated on the 5-judge panel; (b) five memory-system C3−C1 deltas on the controlled config (5-judge panel, from `docs/research/memory_systems_5judge_primary.md`).")
    md.append("")
    md.append("**Collinearity control:** because era correlates with C5 baseline (pre-1700 = lower pretraining knowledge = lower baseline), we also report Δ residualized on C5 via simple OLS across all 14 subjects. If residual cross-tabs still differ by bucket, the era/modernity/exoticism axis adds variance beyond baseline. If not, the effect is collinear with baseline.")
    md.append("")

    md.append("## 1. Per-subject classification + raw deltas")
    md.append("")
    md.append("| Subject | Era | Modernity | Exoticism | C5 (5j) | Δ C2a (5j) | Δ C4a (5j) | Mem0 | Letta | Zep | SM | BL |")
    md.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for s in MAIN_STUDY:
        d = per_subject[s]
        era, mod, exo = SUBJECT_CLASS[s]
        c5 = d["c5_5j"]; dc2a = d["delta_c2a_5j"]; dc4a = d["delta_c4a_5j"]
        ms = d["memsys"]
        def f(v, sign=True):
            if v is None:
                return "—"
            return f"{v:+.3f}" if sign else f"{v:.2f}"
        md.append(
            f"| {s} | {era} | {mod} | {exo} | "
            f"{f(c5, sign=False)} | {f(dc2a)} | {f(dc4a)} | "
            f"{f(ms.get('mem0'))} | {f(ms.get('letta'))} | {f(ms.get('zep'))} | "
            f"{f(ms.get('supermemory'))} | {f(ms.get('baselayer'))} |"
        )
    md.append("")

    def format_cross_table(title, tbl):
        md.append(f"### {title}")
        md.append("")
        md.append("| Bucket | n | mean Δ | std |")
        md.append("|---|---:|---:|---:|")
        for bucket, stats in sorted(tbl.items()):
            if stats["n"] == 0:
                md.append(f"| {bucket} | 0 | — | — |")
                continue
            md.append(f"| {bucket} | {stats['n']} | {stats['mean']:+.3f} | {stats['std']:.3f} |")
        md.append("")

    md.append("## 2. Raw cross-tabs — Era")
    md.append("")
    md.append("Bucket ordering: `pre_1700` (n=4), `1700-1900` (n=9), `post_1900` (n=1). post_1900 is Zitkala-Sa alone — do not treat as its own effect, but report for completeness.")
    md.append("")
    for label, fn in DELTA_SOURCES.items():
        format_cross_table(label, cross_tables[("era", label)])

    md.append("## 3. Raw cross-tabs — Modernity")
    md.append("")
    md.append("Bucket ordering: `archaic` (n=4: Augustine, Babur, Bernal Diaz, Cellini), `modern` (n=10). All corpora are in English; archaic = pre-modern English/translation voice.")
    md.append("")
    for label, fn in DELTA_SOURCES.items():
        format_cross_table(label, cross_tables[("modernity", label)])

    md.append("## 4. Raw cross-tabs — Exoticism")
    md.append("")
    md.append("Bucket ordering: `familiar` (n=4: Hamerton, Ebers, Rousseau, Franklin if included — here Rousseau, Ebers, Hamerton = n=3, since Franklin is not in the 14), `marginal-familiar` (n=1: Cellini), `non-Western` (n=10). Small-cell noise warning: `marginal-familiar` has n=1. Reported for transparency only.")
    md.append("")
    for label, fn in DELTA_SOURCES.items():
        format_cross_table(label, cross_tables[("exoticism", label)])

    md.append("## 5. Residualized cross-tabs — does the axis add variance beyond C5 baseline?")
    md.append("")
    md.append("Residualized Δ = Δ − OLS-predicted(Δ | C5 baseline), computed across all 14 subjects. A bucket mean near zero on the residualized table means the raw bucket-level effect was explained by baseline. A bucket mean still clearly nonzero means the axis adds genuine variance beyond baseline.")
    md.append("")
    for axis in ["era", "modernity", "exoticism"]:
        md.append(f"### 5.{'123'[['era','modernity','exoticism'].index(axis)]} {axis.title()} — residualized")
        md.append("")
        for label, fn in RESID_SOURCES.items():
            format_cross_table(f"{label} — by {axis}", cross_tables[(axis, label)])

    md.append("## 6. Interpretation")
    md.append("")
    md.append(
        "With n=14 split 3 ways on any axis, cell sizes are 1–10. These numbers are "
        "descriptive — no significance tests are attempted on cells with n<3. The headline "
        "check is: does any axis still show a bucket separation on the **residualized** "
        "tables (§5), i.e. after removing the baseline-collinear component?"
    )
    md.append("")
    md.append(
        "Write the qualitative read below after inspecting the tables. The file is "
        "regenerable; this report is the descriptive companion to the author's Q32."
    )
    md.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with OUT_MD.open("w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
