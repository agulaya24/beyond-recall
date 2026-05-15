"""
Cross-system top-K retrieval overlap analysis for Beyond Recall v11.5 §4.4.1.

Answers §1.2's promise: do memory-system providers converge on which facts are
most relevant given identical input?

Two configurations:
  - controlled: same all-facts pool ingested into all systems; each retrieves top-K
                files: <system>_retrieval.json
  - native:     each system runs its own native pipeline (chunking, extraction)
                files: <system>_fullpipeline_retrieval.json

For controlled, all five systems are comparable string-set objects (atomic facts
each ~one sentence). For native, the four memory systems return raw chunks /
provider-internal payloads of heterogeneous shape; baselayer has no native config
because baselayer's controlled output IS its native output. We therefore report
controlled as the primary deliverable and native as a secondary, caveated check.

Per question, per system pair: Jaccard = |A ∩ B| / |A ∪ B|.
Aggregates: per-pair-per-config, overall-per-config, per-subject, per-tier.
Sanity: normalized (lowercase, stripped, whitespace-collapsed) vs. raw.

Outputs:
  - data:  docs/research/retrieval_overlap_analysis_20260501.json
  - prose: docs/research/retrieval_overlap_section_draft_20260501.md
"""

from __future__ import annotations

import ast
import itertools
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev


REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
DATA = REPO / "data"
DOCS_RESEARCH = REPO / "docs" / "research"

CONTROLLED_SYSTEMS = ["baselayer", "mem0", "letta", "supermemory", "zep"]
NATIVE_SYSTEMS = ["mem0", "letta", "supermemory", "zep"]  # baselayer has no _fullpipeline_retrieval

SUBJECTS = [
    "hamerton",
    "global_augustine",
    "global_babur",
    "global_bernal_diaz",
    "global_cellini",
    "global_ebers",
    "global_equiano",
    "global_fukuzawa",
    "global_keckley",
    "global_rousseau",
    "global_seacole",
    "global_sunity_devee",
    "global_yung_wing",
    "global_zitkala_sa",
]

# Zep returns serialization tuples, not facts. Ignore these top-level keys.
ZEP_METADATA_KEYS = {"communities", "context", "episodes", "nodes", "sagas", "themes"}

# Pattern to extract fact='...' or fact="..." (top-level kwarg on EntityEdge)
ZEP_FACT_PATTERN = re.compile(
    r"\bfact=('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"
)


def load_json(p: Path):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def battery_path_for(subject: str) -> Path:
    """Resolve the battery file with question tier metadata.

    Globals: battery_v2.json in results/global_<name>/ has 80 questions with
             behavioral_prediction tier as ids 1-39.
    Hamerton: data/hamerton/battery.json has 80 questions; behavioral_prediction
              tier is ids 21-49 plus 51-60 (id 50 absent in retrieval files).
    """
    if subject == "hamerton":
        return DATA / "hamerton" / "battery.json"
    return RESULTS / subject / "battery_v2.json"


def load_battery_tiers(subject: str) -> dict[int, dict]:
    """Return {question_id: {tier, category, text}}."""
    bp = battery_path_for(subject)
    if not bp.exists():
        return {}
    bat = load_json(bp)
    qs = bat.get("questions", []) if isinstance(bat, dict) else bat
    return {
        int(q["id"]): {
            "tier": q.get("tier", "unknown"),
            "category": q.get("category", "unknown"),
            "text": q.get("text", ""),
        }
        for q in qs
    }


def normalize_fact(s: str) -> str:
    """Lowercase, strip, collapse internal whitespace, drop trailing punctuation
    that varies between systems (period, semicolon)."""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[\.;]+$", "", s)
    return s


def extract_zep_facts(fact_texts: list[str]) -> list[str]:
    """Zep dumps a serialized search-result object as 7 entries. Six are tuples
    like ('communities', None) — pure metadata. The seventh contains an `edges`
    list of EntityEdge(...) repr strings, each with a top-level fact='...' kwarg.
    Extract the top-level fact strings and return as a flat list."""
    facts: list[str] = []
    for ft in fact_texts:
        if not isinstance(ft, str):
            continue
        # Strip ('key', value) metadata wrappers
        skip = False
        for key in ZEP_METADATA_KEYS:
            if ft.startswith(f"('{key}',") and "EntityEdge" not in ft:
                skip = True
                break
        if skip:
            continue
        # Edges blob: extract top-level fact=... kwargs
        if "EntityEdge" in ft:
            for m in ZEP_FACT_PATTERN.findall(ft):
                try:
                    facts.append(ast.literal_eval(m))
                except (ValueError, SyntaxError):
                    facts.append(m.strip("'\""))
        else:
            # Plain string fact (unlikely for Zep but just in case)
            facts.append(ft)
    return facts


def get_facts_for_question(
    record: dict, system: str, config: str
) -> list[str]:
    """Pull the comparable fact-text list for one (system, config, question)."""
    raw = record.get("fact_texts") or []
    if system == "zep":
        return extract_zep_facts(raw)
    return [x for x in raw if isinstance(x, str)]


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return float("nan")
    u = a | b
    if not u:
        return float("nan")
    return len(a & b) / len(u)


def safe_mean(xs: list[float]) -> float | None:
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and x != x)]
    return mean(xs) if xs else None


def sanity_self_check():
    """Hand-verify Jaccard math on a known case."""
    A = {"x", "y", "z", "w"}
    B = {"x", "y", "p", "q"}
    j = jaccard(A, B)
    expected = 2 / 6  # |intersect|=2, |union|=6
    assert abs(j - expected) < 1e-9, f"Jaccard self-check failed: {j} vs {expected}"


def main() -> int:
    sanity_self_check()

    DOCS_RESEARCH.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # Load all retrieval payloads
    # =========================================================================
    # struct[subject][config][system] = {qid: list[str]}
    # struct[subject][config + '_norm'][system] = {qid: list[str]}
    payloads: dict[str, dict[str, dict[str, dict[int, list[str]]]]] = {}
    file_status: dict[str, dict[str, dict[str, str]]] = defaultdict(lambda: defaultdict(dict))

    for subject in SUBJECTS:
        rdir = RESULTS / subject
        payloads[subject] = {"controlled": {}, "native": {}}

        for system in CONTROLLED_SYSTEMS:
            fp = rdir / f"{system}_retrieval.json"
            if not fp.exists():
                file_status[subject]["controlled"][system] = "MISSING"
                continue
            d = load_json(fp)
            payloads[subject]["controlled"][system] = {
                int(qid): get_facts_for_question(rec, system, "controlled")
                for qid, rec in d.items()
            }
            file_status[subject]["controlled"][system] = "ok"

        for system in NATIVE_SYSTEMS:
            fp = rdir / f"{system}_fullpipeline_retrieval.json"
            if not fp.exists():
                file_status[subject]["native"][system] = "MISSING"
                continue
            d = load_json(fp)
            payloads[subject]["native"][system] = {
                int(qid): get_facts_for_question(rec, system, "native")
                for qid, rec in d.items()
            }
            file_status[subject]["native"][system] = "ok"

    # =========================================================================
    # Compute pairwise overlap per question
    # =========================================================================
    # records: list of dict per (subject, config, qid, sys_a, sys_b)
    overlap_records: list[dict] = []
    cap_records: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )  # cap_records[config][system] = list of unique-set sizes per question
    list_len_records: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )  # list_len_records[config][system] = list of raw list lengths per question

    tier_lookup: dict[str, dict[int, dict]] = {
        s: load_battery_tiers(s) for s in SUBJECTS
    }

    for subject in SUBJECTS:
        for config in ("controlled", "native"):
            systems_in_cfg = (
                CONTROLLED_SYSTEMS if config == "controlled" else NATIVE_SYSTEMS
            )
            sys_data = payloads[subject][config]
            # Common qids = intersection of qids present across all systems for this config
            qid_sets = [set(sys_data[s].keys()) for s in systems_in_cfg if s in sys_data]
            if not qid_sets:
                continue
            common_qids = sorted(set.intersection(*qid_sets))
            tiers = tier_lookup.get(subject, {})
            # Track caps using unique-set sizes (consistent with Jaccard math).
            # Note: list-length and unique-set-length can differ — Letta controlled
            # frequently returns 10 duplicates of 2-7 unique facts (graph-traversal
            # retrieval). We report unique-set for compatibility with overlap stats.
            for s in systems_in_cfg:
                if s in sys_data:
                    for qid in common_qids:
                        lst = sys_data[s][qid]
                        cap_records[config][s].append(len(set(lst)))
                        list_len_records[config][s].append(len(lst))

            for qid in common_qids:
                tier_info = tiers.get(qid, {})
                for sys_a, sys_b in itertools.combinations(systems_in_cfg, 2):
                    if sys_a not in sys_data or sys_b not in sys_data:
                        continue
                    raw_a = sys_data[sys_a][qid]
                    raw_b = sys_data[sys_b][qid]
                    set_a_raw = set(raw_a)
                    set_b_raw = set(raw_b)
                    set_a_norm = {normalize_fact(x) for x in raw_a if x.strip()}
                    set_b_norm = {normalize_fact(x) for x in raw_b if x.strip()}
                    rec = {
                        "subject": subject,
                        "config": config,
                        "qid": qid,
                        "tier": tier_info.get("tier", "unknown"),
                        "category": tier_info.get("category", "unknown"),
                        "sys_a": sys_a,
                        "sys_b": sys_b,
                        "size_a": len(set_a_raw),
                        "size_b": len(set_b_raw),
                        "intersect_raw": len(set_a_raw & set_b_raw),
                        "union_raw": len(set_a_raw | set_b_raw),
                        "jaccard_raw": jaccard(set_a_raw, set_b_raw),
                        "intersect_norm": len(set_a_norm & set_b_norm),
                        "union_norm": len(set_a_norm | set_b_norm),
                        "jaccard_norm": jaccard(set_a_norm, set_b_norm),
                    }
                    overlap_records.append(rec)

    # =========================================================================
    # Aggregations
    # =========================================================================
    def aggregate(records: list[dict], group_keys: tuple[str, ...]) -> list[dict]:
        bins: dict[tuple, list[dict]] = defaultdict(list)
        for r in records:
            key = tuple(r[k] for k in group_keys)
            bins[key].append(r)
        out = []
        for key, recs in bins.items():
            j_raw = [r["jaccard_raw"] for r in recs if r["jaccard_raw"] is not None and r["jaccard_raw"] == r["jaccard_raw"]]
            j_norm = [r["jaccard_norm"] for r in recs if r["jaccard_norm"] is not None and r["jaccard_norm"] == r["jaccard_norm"]]
            intersects_raw = [r["intersect_raw"] for r in recs]
            row = {k: v for k, v in zip(group_keys, key)}
            row["n_questions"] = len(recs)
            row["mean_jaccard_raw"] = safe_mean(j_raw)
            row["mean_jaccard_norm"] = safe_mean(j_norm)
            row["mean_intersect_raw"] = safe_mean(intersects_raw)
            row["mean_intersect_norm"] = safe_mean([r["intersect_norm"] for r in recs])
            row["mean_union_raw"] = safe_mean([r["union_raw"] for r in recs])
            row["mean_size_a"] = safe_mean([r["size_a"] for r in recs])
            row["mean_size_b"] = safe_mean([r["size_b"] for r in recs])
            row["share_zero_intersect"] = (
                sum(1 for x in intersects_raw if x == 0) / len(intersects_raw)
                if intersects_raw else None
            )
            row["share_le_one_intersect"] = (
                sum(1 for x in intersects_raw if x <= 1) / len(intersects_raw)
                if intersects_raw else None
            )
            out.append(row)
        return out

    # Per-pair-per-config aggregate
    per_pair = aggregate(overlap_records, ("config", "sys_a", "sys_b"))
    per_pair.sort(key=lambda r: (r["config"], r["sys_a"], r["sys_b"]))

    # Overall per config
    per_config = aggregate(overlap_records, ("config",))
    per_config.sort(key=lambda r: r["config"])

    # Per-subject per-config
    per_subject = aggregate(overlap_records, ("subject", "config"))
    per_subject.sort(key=lambda r: (r["subject"], r["config"]))

    # Per-tier per-config (using tier metadata)
    per_tier = aggregate(overlap_records, ("config", "tier"))
    per_tier.sort(key=lambda r: (r["config"], r["tier"]))

    # Per-category per-config (battery category, e.g. relationships, learning)
    per_category = aggregate(overlap_records, ("config", "category"))
    per_category.sort(key=lambda r: (r["config"], r["category"]))

    # Cap behavior summary — unique-set sizes (used by Jaccard) AND raw list
    # lengths (the literal size each provider reports as facts_returned).
    cap_summary = {}
    for config, sys_caps in cap_records.items():
        cap_summary[config] = {}
        for system, caps in sys_caps.items():
            list_lens = list_len_records[config][system]
            cap_summary[config][system] = {
                "n_q": len(caps),
                "min_unique": min(caps) if caps else None,
                "max_unique": max(caps) if caps else None,
                "mean_unique": safe_mean(caps) if caps else None,
                "min_list_len": min(list_lens) if list_lens else None,
                "max_list_len": max(list_lens) if list_lens else None,
                "mean_list_len": safe_mean(list_lens) if list_lens else None,
                "frac_unique_at_or_above_10": (
                    sum(1 for c in caps if c >= 10) / len(caps) if caps else None
                ),
                "duplication_ratio": (
                    safe_mean(list_lens) / safe_mean(caps)
                    if caps and list_lens and safe_mean(caps) and safe_mean(caps) > 0
                    else None
                ),
                "note": (
                    "Letta controlled returns 10 entries per question but mean unique "
                    "is far lower (graph-traversal retrieval emits the same fact "
                    "multiple times). Supermemory native returns 0-8 atomic facts "
                    "(often 1) due to ingestion-tier limits. Zep returns 7 entries of "
                    "which 6 are tuple metadata wrappers; effective fact count comes "
                    "from regex-extracted top-level fact='...' kwargs in the edges blob."
                ) if system in ("letta", "supermemory", "zep") else None,
            }

    # Normalization sensitivity: per-pair-per-config delta
    norm_sensitivity = []
    for r in per_pair:
        norm_sensitivity.append(
            {
                "config": r["config"],
                "sys_a": r["sys_a"],
                "sys_b": r["sys_b"],
                "raw": r["mean_jaccard_raw"],
                "norm": r["mean_jaccard_norm"],
                "delta_norm_minus_raw": (
                    (r["mean_jaccard_norm"] - r["mean_jaccard_raw"])
                    if r["mean_jaccard_norm"] is not None and r["mean_jaccard_raw"] is not None
                    else None
                ),
            }
        )

    # =========================================================================
    # Headline numbers + identify high/low pairs
    # =========================================================================
    headline = {}
    for cfg in ("controlled", "native"):
        rows = [r for r in per_pair if r["config"] == cfg]
        if not rows:
            continue
        rows_sorted = sorted(
            rows,
            key=lambda r: (
                r["mean_jaccard_raw"] if r["mean_jaccard_raw"] is not None else -1
            ),
        )
        headline[cfg] = {
            "n_pairs": len(rows),
            "mean_jaccard_raw_overall": safe_mean(
                [r["mean_jaccard_raw"] for r in rows]
            ),
            "mean_jaccard_norm_overall": safe_mean(
                [r["mean_jaccard_norm"] for r in rows]
            ),
            "lowest_pair": {
                "sys_a": rows_sorted[0]["sys_a"],
                "sys_b": rows_sorted[0]["sys_b"],
                "mean_jaccard_raw": rows_sorted[0]["mean_jaccard_raw"],
                "mean_jaccard_norm": rows_sorted[0]["mean_jaccard_norm"],
            },
            "highest_pair": {
                "sys_a": rows_sorted[-1]["sys_a"],
                "sys_b": rows_sorted[-1]["sys_b"],
                "mean_jaccard_raw": rows_sorted[-1]["mean_jaccard_raw"],
                "mean_jaccard_norm": rows_sorted[-1]["mean_jaccard_norm"],
            },
        }

    # =========================================================================
    # Save data deliverable
    # =========================================================================
    out_data = {
        "metadata": {
            "generated": "2026-05-01",
            "script": "scripts/analyze_retrieval_overlap.py",
            "subjects": SUBJECTS,
            "controlled_systems": CONTROLLED_SYSTEMS,
            "native_systems": NATIVE_SYSTEMS,
            "n_subjects": len(SUBJECTS),
            "n_controlled_pairs": len(list(itertools.combinations(CONTROLLED_SYSTEMS, 2))),
            "n_native_pairs": len(list(itertools.combinations(NATIVE_SYSTEMS, 2))),
            "metric": "Jaccard = |A ∩ B| / |A ∪ B| over fact-text sets",
            "normalization": "lowercase, strip, collapse whitespace, drop trailing . or ;",
            "zep_handling": (
                "Zep returns 7 entries: 6 tuple metadata wrappers (communities/context/"
                "episodes/nodes/sagas/themes) and 1 'edges' blob containing serialized "
                "EntityEdge reprs. We strip metadata tuples and regex-extract top-level "
                "fact='...' kwargs. Effective Zep retrieval is variable per question."
            ),
            "baselayer_native_note": (
                "BaseLayer has no separate _fullpipeline_retrieval.json — its "
                "controlled-config retrieval IS its native pipeline output (the "
                "all-facts pool was produced by the BaseLayer extraction pipeline). "
                "Native-config Jaccard therefore covers four memory systems / six pairs."
            ),
            "native_caveat": (
                "Native-config retrievals are heterogeneous in shape: Letta returns "
                "raw multi-sentence book passages; Mem0 returns third-person summary "
                "sentences; Supermemory returns 0-8 atomic facts (often 1); Zep returns "
                "EntityEdge graph rows. Surface-string Jaccard between heterogeneous "
                "shapes is structurally low. Controlled config is the cleanest test of "
                "the §1.2 convergence question because all systems index the same "
                "all-facts pool."
            ),
            "behavioral_prediction_tier_only": (
                "All retrieval files cover behavioral_prediction tier only "
                "(13 globals × 39q from battery_v2.json + Hamerton 39q from battery.json "
                "tier='behavioral_prediction'). Adversarial/recall/inferential/boundary "
                "tiers are not represented in retrieval payloads."
            ),
        },
        "headline": headline,
        "file_status_per_subject": {k: dict(v) for k, v in file_status.items()},
        "cap_behavior": cap_summary,
        "per_config_overall": per_config,
        "per_pair_per_config": per_pair,
        "per_subject_per_config": per_subject,
        "per_tier_per_config": per_tier,
        "per_category_per_config": per_category,
        "normalization_sensitivity_per_pair": norm_sensitivity,
    }

    out_path = DOCS_RESEARCH / "retrieval_overlap_analysis_20260501.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"WROTE {out_path}")

    # =========================================================================
    # Console summary
    # =========================================================================
    print("\n=== HEADLINE ===")
    for cfg, h in headline.items():
        print(f"\n{cfg}: {h['n_pairs']} pairs, "
              f"mean Jaccard raw = {h['mean_jaccard_raw_overall']:.3f}, "
              f"norm = {h['mean_jaccard_norm_overall']:.3f}")
        print(f"  lowest:  {h['lowest_pair']['sys_a']:12s} vs {h['lowest_pair']['sys_b']:12s} "
              f"raw={h['lowest_pair']['mean_jaccard_raw']:.3f}")
        print(f"  highest: {h['highest_pair']['sys_a']:12s} vs {h['highest_pair']['sys_b']:12s} "
              f"raw={h['highest_pair']['mean_jaccard_raw']:.3f}")

    print("\n=== PER-PAIR (controlled) ===")
    for r in [r for r in per_pair if r["config"] == "controlled"]:
        print(f"  {r['sys_a']:12s} vs {r['sys_b']:12s} "
              f"n={r['n_questions']:4d} "
              f"|A|={r['mean_size_a']:.1f} |B|={r['mean_size_b']:.1f} "
              f"intersect={r['mean_intersect_raw']:.2f} union={r['mean_union_raw']:.2f} "
              f"J_raw={r['mean_jaccard_raw']:.3f} J_norm={r['mean_jaccard_norm']:.3f}")

    print("\n=== PER-PAIR (native) ===")
    for r in [r for r in per_pair if r["config"] == "native"]:
        print(f"  {r['sys_a']:12s} vs {r['sys_b']:12s} "
              f"n={r['n_questions']:4d} "
              f"|A|={r['mean_size_a']:.1f} |B|={r['mean_size_b']:.1f} "
              f"intersect={r['mean_intersect_raw']:.2f} "
              f"J_raw={r['mean_jaccard_raw']:.3f} J_norm={r['mean_jaccard_norm']:.3f}")

    print("\n=== CAPS ===")
    for cfg, sysmap in cap_summary.items():
        print(f"  [{cfg}]")
        for s, c in sysmap.items():
            print(f"    {s:12s} n_q={c['n_q']:4d} min={c['min_unique']} max={c['max_unique']} "
                  f"mean_unique={c['mean_unique']:.2f} frac>=10={c['frac_unique_at_or_above_10']:.3f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
