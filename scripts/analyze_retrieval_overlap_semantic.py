"""Semantic-similarity (soft) Jaccard sensitivity for cross-system retrieval overlap.

Companion to scripts/analyze_retrieval_overlap.py. The exact-set Jaccard at K=10
in the controlled configuration is 0.083 (mean across 10 pairs, 14 subjects, 546
behavioral-prediction questions). This script asks: does that figure rise
meaningfully when matches are scored on cosine similarity rather than literal
string identity, and at what threshold does any "convergence" reading become
defensible?

For each pair (A, B), each question:
  - Embed A's fact_texts and B's fact_texts with sentence-transformers/all-MiniLM-L6-v2
    (L2-normalized for cosine via dot product).
  - For each fact in A, max cosine similarity to any fact in B; if >= T, count
    as a soft-match (A->B direction).
  - Symmetrize: soft_intersection = mean of (A->B count, B->A count).
  - Soft union = |A| + |B| - soft_intersection.
  - Soft Jaccard = soft_intersection / soft_union.
  - Aggregate per-pair-per-config-per-(K, T) cell as mean across questions.

Configurations:
  - controlled (5 systems, 10 pairs)
  - native     (4 systems, 6 pairs)

K values (truncate-then-dedupe):
  - 5  : top-5 of the ordered fact_texts list, then unique
  - 10 : top-10 of the ordered list (== K=all for controlled, where every
         system returns at most 10), then unique
  - all: full list, then unique. Only meaningfully different from K=10 in
         the native config (Supermemory native often returns 1-8, Zep edges
         vary in count).

Thresholds: T in {0.70, 0.80, 0.85, 0.90, 0.95}.
Calibration anchor (from Letta semantic-duplication analysis): >= 0.95 ~
verbatim-paraphrase, >= 0.85 ~ near-duplicate, >= 0.70 = loose topical match.

Outputs:
  - data:  docs/research/retrieval_overlap_semantic_20260501.json
  - prose: docs/research/retrieval_overlap_semantic_section_draft_20260501.md
"""

from __future__ import annotations

import ast
import itertools
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean

import numpy as np
from sentence_transformers import SentenceTransformer


REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
DATA = REPO / "data"
DOCS_RESEARCH = REPO / "docs" / "research"

CONTROLLED_SYSTEMS = ["baselayer", "mem0", "letta", "supermemory", "zep"]
NATIVE_SYSTEMS = ["mem0", "letta", "supermemory", "zep"]

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

K_VALUES = [5, 10, "all"]
THRESHOLDS = [0.70, 0.80, 0.85, 0.90, 0.95]

ZEP_METADATA_KEYS = {"communities", "context", "episodes", "nodes", "sagas", "themes"}
ZEP_FACT_PATTERN = re.compile(
    r"\bfact=('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"
)


def load_json(p: Path):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def battery_path_for(subject: str) -> Path:
    if subject == "hamerton":
        return DATA / "hamerton" / "battery.json"
    return RESULTS / subject / "battery_v2.json"


def extract_zep_facts(fact_texts: list[str]) -> list[str]:
    """Same logic as analyze_retrieval_overlap.py: strip metadata tuples, regex
    fact='...' kwargs from EntityEdge blob. Preserves emission order."""
    facts: list[str] = []
    for ft in fact_texts:
        if not isinstance(ft, str):
            continue
        skip = False
        for key in ZEP_METADATA_KEYS:
            if ft.startswith(f"('{key}',") and "EntityEdge" not in ft:
                skip = True
                break
        if skip:
            continue
        if "EntityEdge" in ft:
            for m in ZEP_FACT_PATTERN.findall(ft):
                try:
                    facts.append(ast.literal_eval(m))
                except (ValueError, SyntaxError):
                    facts.append(m.strip("'\""))
        else:
            facts.append(ft)
    return facts


def get_facts_for_question(record: dict, system: str) -> list[str]:
    raw = record.get("fact_texts") or []
    if system == "zep":
        return extract_zep_facts(raw)
    return [x for x in raw if isinstance(x, str)]


def truncate_then_dedupe(texts: list[str], k) -> list[str]:
    """Apply top-K truncation in original order, then dedupe preserving order.

    k may be int or 'all'. Empty/whitespace strings dropped.
    """
    if k == "all":
        head = texts
    else:
        head = texts[: int(k)]
    seen = set()
    out: list[str] = []
    for t in head:
        if not isinstance(t, str):
            continue
        s = t.strip()
        if not s:
            continue
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def load_payloads():
    """Returns:
      payloads[subject][config][system][qid] = list[str]  (raw ordered fact_texts)
      file_status[subject][config][system] = "ok" | "MISSING"
    """
    payloads: dict = {s: {"controlled": {}, "native": {}} for s in SUBJECTS}
    file_status: dict = defaultdict(lambda: defaultdict(dict))

    for subject in SUBJECTS:
        rdir = RESULTS / subject
        for system in CONTROLLED_SYSTEMS:
            fp = rdir / f"{system}_retrieval.json"
            if not fp.exists():
                file_status[subject]["controlled"][system] = "MISSING"
                continue
            d = load_json(fp)
            payloads[subject]["controlled"][system] = {
                int(qid): get_facts_for_question(rec, system)
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
                int(qid): get_facts_for_question(rec, system)
                for qid, rec in d.items()
            }
            file_status[subject]["native"][system] = "ok"

    return payloads, file_status


def collect_unique_strings(payloads) -> dict[str, dict[str, set[str]]]:
    """Per (subject, config), the union of all unique fact strings across
    systems and questions. We embed once per (subject, config) batch.
    """
    out: dict[str, dict[str, set[str]]] = {}
    for subject, cfgs in payloads.items():
        out[subject] = {}
        for cfg, sysmap in cfgs.items():
            uniq: set[str] = set()
            for system, qmap in sysmap.items():
                for qid, lst in qmap.items():
                    for t in lst:
                        if isinstance(t, str):
                            s = t.strip()
                            if s:
                                uniq.add(s)
            out[subject][cfg] = uniq
    return out


def soft_jaccard(
    a_texts: list[str], b_texts: list[str], embed_lookup: dict, threshold: float
) -> tuple[float, int, float, float]:
    """Soft Jaccard with symmetrized intersection.

    Returns (jaccard, |A|, |B|, soft_intersection). |A|, |B| are unique set sizes.
    NaN if both empty.
    """
    if not a_texts and not b_texts:
        return float("nan"), 0, 0, 0.0
    if not a_texts or not b_texts:
        return 0.0, len(a_texts), len(b_texts), 0.0

    A = np.stack([embed_lookup[t] for t in a_texts])  # (n_a, d)
    B = np.stack([embed_lookup[t] for t in b_texts])  # (n_b, d)
    sim = A @ B.T  # cosine since L2-normalized

    a_max = sim.max(axis=1)  # for each fact in A, best match in B
    b_max = sim.max(axis=0)  # for each fact in B, best match in A

    a_to_b = int((a_max >= threshold).sum())
    b_to_a = int((b_max >= threshold).sum())

    soft_intersect = (a_to_b + b_to_a) / 2.0
    soft_union = len(a_texts) + len(b_texts) - soft_intersect
    if soft_union <= 0:
        return float("nan"), len(a_texts), len(b_texts), soft_intersect
    return soft_intersect / soft_union, len(a_texts), len(b_texts), soft_intersect


def main() -> int:
    DOCS_RESEARCH.mkdir(parents=True, exist_ok=True)

    print("Loading retrieval payloads ...")
    payloads, file_status = load_payloads()

    # Validate that the controlled config has 14 subjects with all 5 systems
    ok_controlled = sum(
        1 for s in SUBJECTS
        if all(file_status[s]["controlled"].get(sys_) == "ok" for sys_ in CONTROLLED_SYSTEMS)
    )
    ok_native = sum(
        1 for s in SUBJECTS
        if all(file_status[s]["native"].get(sys_) == "ok" for sys_ in NATIVE_SYSTEMS)
    )
    print(f"  controlled: {ok_controlled}/{len(SUBJECTS)} subjects with all systems ok")
    print(f"  native:     {ok_native}/{len(SUBJECTS)} subjects with all systems ok")

    print("Collecting unique fact strings per (subject, config) ...")
    uniq_by_subject_cfg = collect_unique_strings(payloads)
    total_strings = sum(len(s) for sub in uniq_by_subject_cfg.values() for s in sub.values())
    print(f"  total unique strings to embed: {total_strings:,}")

    print("Loading sentence-transformers model (all-MiniLM-L6-v2) ...")
    t0 = time.time()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"  loaded in {time.time() - t0:.1f}s")

    # Embed per (subject, config) batch — keeps memory modest, allows progress logging.
    print("Embedding ...")
    embed_lookup: dict[tuple[str, str], dict[str, np.ndarray]] = {}
    for subject, cfgs in uniq_by_subject_cfg.items():
        for cfg, uniq in cfgs.items():
            if not uniq:
                embed_lookup[(subject, cfg)] = {}
                continue
            texts = sorted(uniq)
            t0 = time.time()
            embs = model.encode(
                texts,
                batch_size=64,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            embed_lookup[(subject, cfg)] = {
                t: e for t, e in zip(texts, embs)
            }
            print(f"  [{subject}/{cfg}] {len(texts):,} strings in {time.time() - t0:.1f}s")

    # ==========================================================================
    # Compute soft Jaccard per (config, K, T, pair, subject, qid)
    # We aggregate to (config, pair, K, T) with per-subject as a side aggregate.
    # ==========================================================================
    # records: list of per-question records
    records: list[dict] = []
    print("Computing soft Jaccard across configs / pairs / K / T ...")

    for config, systems in (
        ("controlled", CONTROLLED_SYSTEMS),
        ("native", NATIVE_SYSTEMS),
    ):
        pairs = list(itertools.combinations(systems, 2))
        n_pairs = len(pairs)
        print(f"  [{config}] {n_pairs} pairs")
        for subject in SUBJECTS:
            sys_data = payloads[subject][config]
            if not sys_data:
                continue
            qid_sets = [set(sys_data[s].keys()) for s in systems if s in sys_data]
            if len(qid_sets) < 2:
                continue
            common_qids = sorted(set.intersection(*qid_sets))
            if not common_qids:
                continue
            lookup = embed_lookup[(subject, config)]

            for sys_a, sys_b in pairs:
                if sys_a not in sys_data or sys_b not in sys_data:
                    continue
                for qid in common_qids:
                    raw_a = sys_data[sys_a][qid]
                    raw_b = sys_data[sys_b][qid]
                    for k in K_VALUES:
                        a_texts = truncate_then_dedupe(raw_a, k)
                        b_texts = truncate_then_dedupe(raw_b, k)
                        for T in THRESHOLDS:
                            j, na, nb, inter = soft_jaccard(
                                a_texts, b_texts, lookup, T
                            )
                            records.append({
                                "config": config,
                                "subject": subject,
                                "qid": qid,
                                "sys_a": sys_a,
                                "sys_b": sys_b,
                                "K": k,
                                "T": T,
                                "size_a": na,
                                "size_b": nb,
                                "soft_intersect": inter,
                                "soft_jaccard": j,
                            })

    print(f"  total per-question records: {len(records):,}")

    # ==========================================================================
    # Aggregations
    # ==========================================================================
    def safe_mean(xs):
        xs = [x for x in xs if x is not None and not (isinstance(x, float) and x != x)]
        return float(mean(xs)) if xs else None

    # Per-pair × config × K × T
    bins_pair: dict[tuple, list[float]] = defaultdict(list)
    for r in records:
        key = (r["config"], r["sys_a"], r["sys_b"], r["K"], r["T"])
        if r["soft_jaccard"] is not None and not (
            isinstance(r["soft_jaccard"], float) and r["soft_jaccard"] != r["soft_jaccard"]
        ):
            bins_pair[key].append(r["soft_jaccard"])

    per_pair = []
    for (config, sa, sb, k, t), vals in bins_pair.items():
        per_pair.append({
            "config": config,
            "sys_a": sa,
            "sys_b": sb,
            "K": k,
            "T": t,
            "n_questions": len(vals),
            "mean_soft_jaccard": safe_mean(vals),
        })
    per_pair.sort(key=lambda r: (r["config"], r["sys_a"], r["sys_b"],
                                 0 if r["K"] == "all" else r["K"], r["T"]))

    # Aggregate across pairs: config × K × T
    bins_cell: dict[tuple, list[float]] = defaultdict(list)
    for r in per_pair:
        if r["mean_soft_jaccard"] is not None:
            bins_cell[(r["config"], r["K"], r["T"])].append(r["mean_soft_jaccard"])

    per_cell = []
    for (config, k, t), vals in bins_cell.items():
        per_cell.append({
            "config": config,
            "K": k,
            "T": t,
            "n_pairs": len(vals),
            "mean_soft_jaccard_across_pairs": safe_mean(vals),
            "min_pair": min(vals) if vals else None,
            "max_pair": max(vals) if vals else None,
        })
    per_cell.sort(key=lambda r: (r["config"],
                                 0 if r["K"] == "all" else r["K"], r["T"]))

    # Per-subject × config × K × T
    bins_subj: dict[tuple, list[float]] = defaultdict(list)
    for r in records:
        if r["soft_jaccard"] is not None and not (
            isinstance(r["soft_jaccard"], float) and r["soft_jaccard"] != r["soft_jaccard"]
        ):
            bins_subj[(r["subject"], r["config"], r["K"], r["T"])].append(r["soft_jaccard"])
    per_subject = []
    for (subj, config, k, t), vals in bins_subj.items():
        per_subject.append({
            "subject": subj,
            "config": config,
            "K": k,
            "T": t,
            "n_pair_questions": len(vals),
            "mean_soft_jaccard": safe_mean(vals),
        })
    per_subject.sort(key=lambda r: (r["subject"], r["config"],
                                    0 if r["K"] == "all" else r["K"], r["T"]))

    # ==========================================================================
    # Sanity checks
    # ==========================================================================
    sanity = {}
    # 1. Monotonicity per (config, pair, K): soft Jaccard should be non-decreasing
    #    as T drops. Allow a tiny epsilon for floating arithmetic.
    monotonic_violations = []
    by_pair_K: dict[tuple, list[tuple[float, float]]] = defaultdict(list)
    for r in per_pair:
        if r["mean_soft_jaccard"] is None:
            continue
        by_pair_K[(r["config"], r["sys_a"], r["sys_b"], r["K"])].append(
            (r["T"], r["mean_soft_jaccard"])
        )
    for key, ts in by_pair_K.items():
        ts.sort(key=lambda x: x[0], reverse=True)  # descending T
        for i in range(len(ts) - 1):
            if ts[i + 1][1] < ts[i][1] - 1e-9:
                monotonic_violations.append({
                    "key": list(key),
                    "T_high": ts[i][0],
                    "v_high": ts[i][1],
                    "T_low": ts[i + 1][0],
                    "v_low": ts[i + 1][1],
                })
    sanity["monotonicity_violations"] = monotonic_violations
    sanity["monotonicity_violations_count"] = len(monotonic_violations)

    # 2. T=0.95 controlled K=10 mean across pairs: should be >= exact 0.083 and modest.
    cell_095_ctrl_10 = next(
        (r for r in per_cell if r["config"] == "controlled" and r["K"] == 10 and r["T"] == 0.95),
        None,
    )
    sanity["controlled_K10_T095_cell"] = cell_095_ctrl_10

    # 3. T=0.70 vs T=0.95 spread (controlled, K=10) — should rise as T falls
    cell_070_ctrl_10 = next(
        (r for r in per_cell if r["config"] == "controlled" and r["K"] == 10 and r["T"] == 0.70),
        None,
    )
    sanity["controlled_K10_T070_cell"] = cell_070_ctrl_10

    # ==========================================================================
    # Save data
    # ==========================================================================
    out_data = {
        "metadata": {
            "generated": "2026-05-01",
            "script": "scripts/analyze_retrieval_overlap_semantic.py",
            "subjects": SUBJECTS,
            "n_subjects": len(SUBJECTS),
            "controlled_systems": CONTROLLED_SYSTEMS,
            "native_systems": NATIVE_SYSTEMS,
            "n_controlled_pairs": len(list(itertools.combinations(CONTROLLED_SYSTEMS, 2))),
            "n_native_pairs": len(list(itertools.combinations(NATIVE_SYSTEMS, 2))),
            "K_values": K_VALUES,
            "thresholds": THRESHOLDS,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "metric": (
                "Soft Jaccard with symmetrized intersection. For each fact in A, "
                "max cosine similarity to any fact in B; if >= T, count as match. "
                "Soft intersection = mean of (A->B count, B->A count). "
                "Soft union = |A| + |B| - soft_intersection. "
                "Soft Jaccard = soft_intersection / soft_union."
            ),
            "k_truncation_order": (
                "Truncate ordered fact_texts list to top-K, then deduplicate. "
                "K=all means no truncation. Empty/whitespace strings dropped."
            ),
            "k_all_note": (
                "K=all is identical to K=10 for controlled (every system returns "
                "<=10). Distinct values appear only in native, where Supermemory "
                "and Zep often return fewer than 10."
            ),
            "calibration": (
                "Threshold semantics from Letta semantic-duplication study: "
                ">= 0.95 ~ verbatim-paraphrase, >= 0.85 ~ near-duplicate, "
                ">= 0.70 = loose topical match. Reading Jaccard at T=0.70 as "
                "convergence is vulnerable to topical-density confound; "
                "T=0.85 and T=0.95 are the discriminating cells."
            ),
            "exact_baseline_reference": (
                "From scripts/analyze_retrieval_overlap.py: controlled mean "
                "exact-set Jaccard = 0.083 raw / 0.088 normalized; native = ~0.000."
            ),
        },
        "file_status_per_subject": {k: dict(v) for k, v in file_status.items()},
        "sanity_checks": sanity,
        "per_cell_across_pairs": per_cell,
        "per_pair_per_config_per_K_per_T": per_pair,
        "per_subject_per_config_per_K_per_T": per_subject,
    }

    out_path = DOCS_RESEARCH / "retrieval_overlap_semantic_20260501.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"\nWROTE {out_path}")

    # ==========================================================================
    # Console summary
    # ==========================================================================
    print("\n=== HEADLINE GRID — mean soft Jaccard across pairs ===")
    for cfg in ("controlled", "native"):
        print(f"\n[{cfg}]")
        # Sort thresholds descending for readability (verbatim -> loose)
        for k in K_VALUES:
            line = f"  K={str(k):>3s}  "
            for T in sorted(THRESHOLDS, reverse=True):
                cell = next(
                    (r for r in per_cell
                     if r["config"] == cfg and r["K"] == k and r["T"] == T),
                    None,
                )
                v = cell["mean_soft_jaccard_across_pairs"] if cell else None
                line += f" T={T:.2f}: {v:.3f}" if v is not None else f" T={T:.2f}:  N/A "
            print(line)

    print(f"\nMonotonicity violations: {sanity['monotonicity_violations_count']}")
    if monotonic_violations[:3]:
        for v in monotonic_violations[:3]:
            print(f"  WARN: {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
