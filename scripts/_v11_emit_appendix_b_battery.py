"""v11 canonical emit script for Appendix B of the Beyond Recall v10 paper.

Appendix B reports the question battery composition (B.1 through B.6):

  B.1  10 fixed behavioral-prediction categories (definition only, no numbers)
  B.2  Per-subject battery composition (15 subjects x 10 categories)
  B.3  Behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL_TRIGGERING)
  B.4  Category-level effect size on Delta_spec
  B.5  Per-subject by axis Delta_spec
  B.6  Battery-composition correlation with subject-level Delta_spec

Aggregation rule (locked v11):
  Per-judge per-question score -> per-judge per-(subject, condition, question)
  mean -> 5-judge primary panel mean = mean across {haiku, sonnet, opus, gpt4o, gpt54}.
  A panel mean is None when any panel judge is missing for that cell.

Per-question Delta_spec under v11 = panel_mean(C2a_full_spec) - panel_mean(C5_baseline).

Inputs (primary):
  results/global_<subject>/battery_v2.json    13 global subjects (39 BP qs each)
  data/hamerton/battery.json                   39 BP questions
  data/franklin/battery.json                   40 BP questions
  results/global_<subject>/judgments_v2.json   13 global subjects (judgments)
  results/_s114_backfills/global_<subject>__*.json   judgment overlays
  results/hamerton/{judgments_harmonized,judgments,sonnet_judgments,
                     opus_judgments,gpt4o_judgments,gpt54_judgments}.json
  results/franklin_legacy_20260411/analysis/{haiku,sonnet,opus,gpt4o,gpt54}_judgments.json
  docs/research/question_category_audit.json   Haiku-classifier categorical labels
                                                (PRIMARY for category labels; the labels
                                                 are produced by an LLM classifier and
                                                 cannot be re-derived without rerunning it)

Outputs (atomic-written):
  docs/research/v11_emit/appendix_b_battery.json
  docs/research/v11_emit/appendix_b_battery.md

Constraints:
  - Schema-validate every input file. Abort with a named error if a battery
    JSON question is missing `category` or `tier`, or if an audit record is
    missing `category_rubric`.
  - Idempotent: timestamp is a literal; running twice on unchanged inputs
    produces byte-identical output.
  - Atomic write: tmp file + rename.
  - SHA-256 manifest of every input file.
  - No em-dashes in markdown output.

Verification:
  --verify  Run emit, compare emitted scalars to v10 paper Appendix B claims.
            Exit 0 if all match within 0.005 tolerance, exit 1 otherwise.

Note on the locked condition set: per-question Delta_spec uses the C2a vs C5
contrast. This is the "subject-level Delta_spec" used in B.4, B.5, B.6 and is
consistent with the audit doc's definition (NOT the gradient table's Delta_C4a
in section 4.1).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Make sibling scripts importable.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from recompute_5judge_primary import (  # noqa: E402
    load_global_judgments,
    load_hamerton_judgments,
)

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
DATA = REPO / "data"
OUT_DIR = REPO / "docs" / "research" / "v11_emit"
OUT_JSON = OUT_DIR / "appendix_b_battery.json"
OUT_MD = OUT_DIR / "appendix_b_battery.md"

# --- Locked constants -------------------------------------------------------

EMIT_DATE = "2026-04-25"
SCHEMA_VERSION = "v11.0"
SCRIPT_VERSION = "v11.0-appendix-b"
PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
VERIFY_TOLERANCE = 0.005

# Subject ordering for B.2 (matches paper Appendix B table order).
SUBJECT_ORDER = [
    "augustine", "babur", "bernal_diaz", "cellini", "ebers", "equiano",
    "fukuzawa", "keckley", "rousseau", "seacole", "sunity_devee",
    "yung_wing", "zitkala_sa", "hamerton", "franklin",
]
GLOBAL_SUBJECTS = {
    "augustine", "babur", "bernal_diaz", "cellini", "ebers", "equiano",
    "fukuzawa", "keckley", "rousseau", "seacole", "sunity_devee",
    "yung_wing", "zitkala_sa",
}
MAIN_STUDY = [s for s in SUBJECT_ORDER if s != "franklin"]  # 14 subjects

# 10 fixed behavioral-prediction category columns (paper B.2 order).
CATEGORY_ORDER = [
    "decisions", "values", "relationships", "conflict", "learning",
    "risk", "creativity", "stress", "career", "change_over_time",
]

# 3 behavioral-axis labels (B.3-B.6).
AXIS_ORDER = ["LITERAL_RECALL", "INTERPRETIVE_INFERENCE", "REFUSAL_TRIGGERING"]

# --- Paper claims for --verify ---------------------------------------------

PAPER_B2 = {
    "augustine":    [6, 7, 4, 5, 9, 0, 3, 3, 0, 2],
    "babur":        [9, 6, 8, 4, 3, 1, 2, 3, 2, 1],
    "bernal_diaz":  [8, 8, 4, 5, 5, 3, 0, 5, 0, 1],
    "cellini":      [5, 6, 5, 4, 3, 1, 4, 5, 4, 2],
    "ebers":        [4, 8, 3, 4, 6, 0, 6, 3, 1, 4],
    "equiano":      [5, 8, 4, 5, 5, 1, 0, 8, 0, 3],
    "fukuzawa":     [8, 11, 5, 5, 3, 1, 1, 2, 0, 3],
    "keckley":      [6, 7, 9, 6, 4, 1, 0, 3, 2, 1],
    "rousseau":     [5, 6, 9, 6, 5, 1, 1, 4, 1, 1],
    "seacole":      [7, 10, 7, 1, 3, 1, 2, 6, 2, 0],
    "sunity_devee": [4, 9, 6, 5, 5, 1, 1, 6, 0, 2],
    "yung_wing":    [10, 8, 3, 3, 3, 1, 3, 2, 5, 1],
    "zitkala_sa":   [4, 11, 6, 5, 4, 0, 3, 4, 0, 2],
    "hamerton":     [6, 4, 6, 4, 4, 3, 4, 3, 3, 2],
    "franklin":     [6, 6, 5, 4, 3, 4, 4, 3, 3, 2],
}
PAPER_B2_COLUMN_TOTALS = [93, 115, 84, 66, 65, 19, 34, 60, 23, 27]
PAPER_B2_GRAND_TOTAL = 586

PAPER_B3 = {
    "LITERAL_RECALL": (60, 10.2),
    "INTERPRETIVE_INFERENCE": (403, 68.8),
    "REFUSAL_TRIGGERING": (123, 21.0),
    "TOTAL": (586, 100.0),
}

PAPER_B4 = {
    "LITERAL_RECALL":         {"n": 60,  "mean_delta_spec": 0.792},
    "INTERPRETIVE_INFERENCE": {"n": 366, "mean_delta_spec": 0.397},
    "REFUSAL_TRIGGERING":     {"n": 120, "mean_delta_spec": 0.489},
}

# B.5 per-subject axis deltas (Hamerton triplet noted in paper text).
PAPER_B5_HAMERTON = {
    "LITERAL_RECALL": 1.93,
    "INTERPRETIVE_INFERENCE": 2.02,
    "REFUSAL_TRIGGERING": 1.71,
}

PAPER_B6 = {
    "LITERAL_RECALL_corr_with_delta":         0.646,
    "INTERPRETIVE_INFERENCE_corr_with_delta": -0.582,
    "REFUSAL_TRIGGERING_corr_with_delta":     0.321,
    "delta_min": -0.31,
    "delta_max":  1.85,
}

# --- File helpers -----------------------------------------------------------


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def file_manifest_entry(path: Path, n_records: int | None = None) -> dict:
    return {
        "path": str(path.relative_to(REPO)).replace("\\", "/"),
        "sha256": sha256_of(path),
        "size_bytes": path.stat().st_size,
        "n_records": n_records,
    }


# --- Battery loading + schema validation ------------------------------------


class BatterySchemaError(ValueError):
    """Raised when a battery JSON does not satisfy the v11 schema contract."""


def battery_path(subject: str) -> Path:
    if subject == "hamerton":
        return DATA / "hamerton" / "battery.json"
    if subject == "franklin":
        return DATA / "franklin" / "battery.json"
    if subject in GLOBAL_SUBJECTS:
        # canonical: results/global_<subject>/battery_v2.json
        p = RESULTS / f"global_{subject}" / "battery_v2.json"
        if not p.exists():
            raise BatterySchemaError(
                f"battery_v2.json missing for global subject '{subject}' at {p}"
            )
        return p
    raise BatterySchemaError(f"unknown subject '{subject}'")


def load_battery_bp(subject: str) -> tuple[list[dict], Path]:
    """Return (behavioral_prediction_questions, source_path) for a subject.

    Aborts with BatterySchemaError if any expected field is missing.
    """
    path = battery_path(subject)
    raw = json.load(path.open(encoding="utf-8"))
    if not isinstance(raw, dict) or "questions" not in raw:
        raise BatterySchemaError(
            f"battery JSON {path} is not a dict with 'questions' key"
        )
    questions = raw["questions"]
    if not isinstance(questions, list):
        raise BatterySchemaError(
            f"battery JSON {path}: 'questions' is not a list"
        )
    bp = []
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            raise BatterySchemaError(
                f"{path}: question index {i} is not a dict"
            )
        if "tier" not in q:
            raise BatterySchemaError(
                f"{path}: question id={q.get('id')} missing 'tier' field"
            )
        if q["tier"] != "behavioral_prediction":
            continue
        if "category" not in q or q["category"] is None:
            raise BatterySchemaError(
                f"{path}: BP question id={q.get('id')} missing 'category' "
                f"field; cannot proceed without explicit category-per-question"
            )
        if q["category"] not in CATEGORY_ORDER:
            raise BatterySchemaError(
                f"{path}: BP question id={q.get('id')} has unexpected "
                f"category '{q['category']}'; allowed = {CATEGORY_ORDER}"
            )
        if "id" not in q:
            raise BatterySchemaError(
                f"{path}: BP question missing 'id' field"
            )
        bp.append(q)
    return bp, path


# --- Audit JSON loading + schema validation ---------------------------------


class AuditSchemaError(ValueError):
    """Raised when the question_category_audit.json does not satisfy v11."""


def load_audit() -> tuple[dict, Path]:
    path = REPO / "docs" / "research" / "question_category_audit.json"
    if not path.exists():
        raise AuditSchemaError(f"audit JSON missing at {path}")
    data = json.load(path.open(encoding="utf-8"))
    if not isinstance(data, dict) or "questions" not in data:
        raise AuditSchemaError(f"{path}: missing 'questions' key")
    by_key = {}
    for q in data["questions"]:
        for f in ("subject", "question_id", "category_rubric"):
            if f not in q:
                raise AuditSchemaError(
                    f"{path}: audit record missing '{f}': {q}"
                )
        if q["category_rubric"] not in AXIS_ORDER:
            raise AuditSchemaError(
                f"{path}: unexpected category_rubric '{q['category_rubric']}' "
                f"on (subject={q['subject']}, qid={q['question_id']})"
            )
        by_key[(q["subject"], q["question_id"])] = q["category_rubric"]
    return {"records": data["questions"], "by_key": by_key}, path


# --- Judgment loading (5-judge primary panel, per-question deltas) ----------


def load_subject_judgments(subject: str) -> list[dict]:
    """Return canonical-shape judgment rows for any subject."""
    if subject == "hamerton":
        return load_hamerton_judgments()
    if subject == "franklin":
        # Franklin judgments are loaded from the legacy directory; we use the
        # same loader as 4_1_gradient.py inlined here for clarity.
        return load_franklin_judgments()
    return load_global_judgments(subject)


# Franklin has its legacy condition names; this mirrors _v11_emit_4_1_gradient.
FRANKLIN_COND_MAP = {
    "C5_baseline": "C5_baseline",
    "C2a_spec_only": "C2a_full_spec",
    "C4_factdump": "C4_factdump",
    "C2c_wrong_spec": "C2c_wrong_spec",
    "C4a_factdump_plus_spec": "C4a_full_facts_plus_spec",
}


def load_franklin_judgments() -> list[dict]:
    base = RESULTS / "franklin_legacy_20260411" / "analysis"
    rows = []
    file_map = {
        "haiku": "haiku_judgments.json",
        "sonnet": "sonnet_judgments.json",
        "opus": "opus_judgments.json",
        "gpt4o": "gpt4o_judgments.json",
        "gpt54": "gpt54_judgments.json",
    }
    for judge, fname in file_map.items():
        p = base / fname
        if not p.exists():
            continue
        score_field = f"{judge}_score"
        for r in json.load(p.open(encoding="utf-8")):
            cond = FRANKLIN_COND_MAP.get(r.get("condition"))
            if cond is None:
                continue
            score = r.get(score_field)
            if score is None:
                continue
            rows.append({
                "question_id": r.get("question_id"),
                "condition": cond,
                "judge": judge,
                "score": score,
                "parse_failure": False,
            })
    return rows


def per_question_panel_delta(rows: list[dict]) -> dict:
    """For a subject's rows, return {qid: C2a_full_spec - C5_baseline}.

    Both panel means must be present (all 5 panel judges) for the qid to have
    a non-None delta. The per-judge per-question mean is the mean of all
    (judge, question, condition) scores (typically 1 score per cell, but the
    loader may have multiple if both pre- and post-backfill records exist; we
    average defensively).
    """
    buckets = defaultdict(list)
    for r in rows:
        if r.get("judge") not in PRIMARY_PANEL:
            continue
        if r.get("parse_failure"):
            continue
        score = r.get("score")
        if score is None:
            continue
        buckets[(r["question_id"], r["condition"], r["judge"])].append(score)

    per_jq = {k: statistics.mean(v) for k, v in buckets.items() if v}

    qcond = defaultdict(list)
    for (qid, cond, judge), m in per_jq.items():
        qcond[(qid, cond)].append((judge, m))

    panel_mean = {}
    for (qid, cond), pairs in qcond.items():
        present = {j for j, _ in pairs}
        if present == set(PRIMARY_PANEL):
            panel_mean[(qid, cond)] = statistics.mean(m for _, m in pairs)
        else:
            panel_mean[(qid, cond)] = None

    qids_seen = {qid for (qid, _) in panel_mean}
    deltas = {}
    for qid in qids_seen:
        c2a = panel_mean.get((qid, "C2a_full_spec"))
        c5 = panel_mean.get((qid, "C5_baseline"))
        if c2a is None or c5 is None:
            deltas[qid] = None
        else:
            deltas[qid] = c2a - c5
    return deltas


# --- Stats utilities --------------------------------------------------------


def pearson_r(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n != len(ys) or n < 2:
        return float("nan")
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return float("nan")
    return num / (sx * sy)


def median(xs: list[float]) -> float:
    return statistics.median(xs) if xs else float("nan")


# --- Build payload ----------------------------------------------------------


def build_payload() -> dict:
    """Top-level orchestrator. Returns the canonical JSON dict."""
    input_manifest: list[dict] = []
    claims: dict[str, dict] = {}

    # ---- 1. Load batteries (B.2 source data) -------------------------------
    battery_bp = {}  # subject -> [BP question dict]
    battery_paths = {}
    for subject in SUBJECT_ORDER:
        bp, path = load_battery_bp(subject)
        battery_bp[subject] = bp
        battery_paths[subject] = path
        input_manifest.append(file_manifest_entry(path, n_records=len(bp)))

    # ---- 2. Load audit (B.3-B.6 categorical labels) ------------------------
    audit, audit_path = load_audit()
    input_manifest.append(file_manifest_entry(audit_path, n_records=len(audit["records"])))

    # ---- 3. Load judgments + compute per-question Delta_spec ---------------
    judgment_paths_added: set[str] = set()
    per_question_delta = {}  # subject -> {qid: delta or None}
    for subject in SUBJECT_ORDER:
        rows = load_subject_judgments(subject)
        per_question_delta[subject] = per_question_panel_delta(rows)
        # Manifest input judgment files. (We list canonical paths; per-file
        # content is resolved inside the loaders, so we record canonical paths
        # only.)
        if subject == "hamerton":
            cands = [
                RESULTS / "hamerton" / "judgments_harmonized.json",
                RESULTS / "hamerton" / "judgments.json",
                RESULTS / "hamerton" / "sonnet_judgments.json",
                RESULTS / "hamerton" / "opus_judgments.json",
                RESULTS / "hamerton" / "gpt4o_judgments.json",
                RESULTS / "hamerton" / "gpt54_judgments.json",
            ]
        elif subject == "franklin":
            cands = [
                RESULTS / "franklin_legacy_20260411" / "analysis" / "haiku_judgments.json",
                RESULTS / "franklin_legacy_20260411" / "analysis" / "sonnet_judgments.json",
                RESULTS / "franklin_legacy_20260411" / "analysis" / "opus_judgments.json",
                RESULTS / "franklin_legacy_20260411" / "analysis" / "gpt4o_judgments.json",
                RESULTS / "franklin_legacy_20260411" / "analysis" / "gpt54_judgments.json",
            ]
        else:
            cands = [RESULTS / f"global_{subject}" / "judgments_v2.json"]
            backfill_dir = RESULTS / "_s114_backfills"
            if backfill_dir.exists():
                cands.extend(sorted(backfill_dir.glob(f"global_{subject}__*.json")))
        for p in cands:
            if not p.exists():
                continue
            key = str(p.resolve())
            if key in judgment_paths_added:
                continue
            judgment_paths_added.add(key)
            input_manifest.append(file_manifest_entry(p))

    # ---- 4. B.2 emit -------------------------------------------------------
    b2_matrix = {}  # subject -> {category: count}
    column_totals = {c: 0 for c in CATEGORY_ORDER}
    grand_total = 0
    for subject in SUBJECT_ORDER:
        cats = Counter(q["category"] for q in battery_bp[subject])
        row = {c: int(cats.get(c, 0)) for c in CATEGORY_ORDER}
        b2_matrix[subject] = row
        row_total = sum(row.values())
        for c in CATEGORY_ORDER:
            column_totals[c] += row[c]
        grand_total += row_total
        # claim_ids: per (subject, category) cell + per-subject total
        for c in CATEGORY_ORDER:
            claims[f"appB_2_{subject}_{c}_count"] = {
                "value": row[c],
                "estimand": f"count of behavioral-prediction questions in category '{c}' for subject '{subject}'",
                "contrast": None,
                "filters": {"subject": subject, "tier": "behavioral_prediction", "category": c},
                "n": int(row_total),
                "ci95_low": None, "ci95_high": None, "p_value": None,
            }
        claims[f"appB_2_{subject}_total"] = {
            "value": int(row_total),
            "estimand": f"total behavioral-prediction questions for subject '{subject}'",
            "contrast": None,
            "filters": {"subject": subject, "tier": "behavioral_prediction"},
            "n": int(row_total),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
    for c in CATEGORY_ORDER:
        claims[f"appB_2_column_total_{c}"] = {
            "value": int(column_totals[c]),
            "estimand": f"total questions across all 15 subjects in category '{c}'",
            "contrast": None,
            "filters": {"tier": "behavioral_prediction", "category": c, "subjects": SUBJECT_ORDER},
            "n": int(column_totals[c]),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
    claims["appB_2_grand_total"] = {
        "value": int(grand_total),
        "estimand": "total behavioral-prediction questions across all 15 subjects",
        "contrast": None,
        "filters": {"tier": "behavioral_prediction", "subjects": SUBJECT_ORDER},
        "n": int(grand_total),
        "ci95_low": None, "ci95_high": None, "p_value": None,
    }

    # ---- 5. B.3 emit (axis distribution) -----------------------------------
    # Apply audit labels to the BP questions in each battery. Cross-check that
    # every BP question has an audit label; abort with a named error if not.
    axis_counter = Counter()
    per_subject_axis_count = {}
    missing_audit = []
    for subject in SUBJECT_ORDER:
        per_subject_axis_count[subject] = Counter()
        for q in battery_bp[subject]:
            qid = q["id"]
            axis = audit["by_key"].get((subject, qid))
            if axis is None:
                missing_audit.append((subject, qid))
                continue
            axis_counter[axis] += 1
            per_subject_axis_count[subject][axis] += 1
    if missing_audit:
        raise AuditSchemaError(
            f"audit labels missing for {len(missing_audit)} (subject, qid) pairs; "
            f"first 5: {missing_audit[:5]}"
        )

    total_n = sum(axis_counter.values())
    for axis in AXIS_ORDER:
        n = int(axis_counter[axis])
        pct = round(100.0 * n / total_n, 1) if total_n else 0.0
        key_axis = axis.lower()
        claims[f"appB_3_{key_axis}_n"] = {
            "value": n,
            "estimand": f"count of behavioral-prediction questions classified as '{axis}'",
            "contrast": None,
            "filters": {"axis": axis, "tier": "behavioral_prediction", "subjects": SUBJECT_ORDER},
            "n": n,
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
        claims[f"appB_3_{key_axis}_pct"] = {
            "value": pct,
            "estimand": f"percentage of behavioral-prediction questions classified as '{axis}'",
            "contrast": None,
            "filters": {"axis": axis, "tier": "behavioral_prediction", "subjects": SUBJECT_ORDER},
            "n": total_n,
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
    claims["appB_3_total_n"] = {
        "value": int(total_n),
        "estimand": "total behavioral-prediction questions across the 15 subjects (sum across axis labels)",
        "contrast": None,
        "filters": {"tier": "behavioral_prediction", "subjects": SUBJECT_ORDER},
        "n": int(total_n),
        "ci95_low": None, "ci95_high": None, "p_value": None,
    }

    # ---- 6. B.4 emit (axis-level mean Delta_spec) --------------------------
    # B.4 is computed across the 14 main-study subjects (Franklin excluded
    # because its legacy condition coverage produces no panel-mean delta on
    # the spec contrast under the locked rule). The question count per axis
    # therefore drops from B.3's totals.
    axis_pool = defaultdict(list)
    for subject in MAIN_STUDY:
        for q in battery_bp[subject]:
            qid = q["id"]
            axis = audit["by_key"].get((subject, qid))
            d = per_question_delta[subject].get(qid)
            if axis is None or d is None:
                continue
            axis_pool[axis].append(d)
    for axis in AXIS_ORDER:
        vals = axis_pool[axis]
        n = len(vals)
        m = statistics.mean(vals) if vals else None
        med = median(vals) if vals else None
        key_axis = axis.lower()
        claims[f"appB_4_{key_axis}_mean_delta_spec"] = {
            "value": m,
            "estimand": (
                f"mean per-question Delta_spec (C2a_full_spec - C5_baseline) "
                f"across all '{axis}' questions in the 14 main-study subjects"
            ),
            "contrast": "C2a_full_spec vs C5_baseline",
            "filters": {"axis": axis, "subjects": MAIN_STUDY},
            "n": int(n),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
        claims[f"appB_4_{key_axis}_n"] = {
            "value": int(n),
            "estimand": f"number of '{axis}' questions with a panel-mean Delta_spec across the 14 main-study subjects",
            "contrast": "C2a_full_spec vs C5_baseline",
            "filters": {"axis": axis, "subjects": MAIN_STUDY},
            "n": int(n),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
        claims[f"appB_4_{key_axis}_median_delta_spec"] = {
            "value": med,
            "estimand": f"median per-question Delta_spec across '{axis}' questions in main-study",
            "contrast": "C2a_full_spec vs C5_baseline",
            "filters": {"axis": axis, "subjects": MAIN_STUDY},
            "n": int(n),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }

    # ---- 7. B.5 emit (per-subject by axis Delta_spec) ----------------------
    # For each (subject, axis), mean of per-question deltas where both panel
    # means exist. Franklin will mostly be None.
    per_subject_axis_delta = {}  # subject -> {axis: float or None}
    for subject in SUBJECT_ORDER:
        per_subject_axis_delta[subject] = {}
        bucket = defaultdict(list)
        for q in battery_bp[subject]:
            qid = q["id"]
            axis = audit["by_key"].get((subject, qid))
            d = per_question_delta[subject].get(qid)
            if axis is None or d is None:
                continue
            bucket[axis].append(d)
        for axis in AXIS_ORDER:
            vals = bucket[axis]
            v = statistics.mean(vals) if vals else None
            per_subject_axis_delta[subject][axis] = v
            key_axis = axis.lower()
            claims[f"appB_5_{subject}_{key_axis}_delta"] = {
                "value": v,
                "estimand": (
                    f"per-question mean Delta_spec for axis '{axis}' on subject '{subject}'"
                ),
                "contrast": "C2a_full_spec vs C5_baseline",
                "filters": {"subject": subject, "axis": axis},
                "n": int(len(vals)),
                "ci95_low": None, "ci95_high": None, "p_value": None,
            }

    # ---- 8. B.6 emit (battery-composition correlations) -------------------
    # x = fraction of subject's BP questions with axis A
    # y = subject-level mean Delta_spec (C2a - C5) across all BP qs with a
    #     valid panel delta
    # Across the 14 main-study subjects.
    subj_mean_delta = {}
    subj_axis_frac = {s: {} for s in MAIN_STUDY}
    for subject in MAIN_STUDY:
        per_q = []
        cats_for_valid = []
        for q in battery_bp[subject]:
            qid = q["id"]
            axis = audit["by_key"].get((subject, qid))
            d = per_question_delta[subject].get(qid)
            if d is None:
                continue
            per_q.append(d)
            cats_for_valid.append(axis)
        n = len(per_q)
        subj_mean_delta[subject] = statistics.mean(per_q) if per_q else None
        for axis in AXIS_ORDER:
            subj_axis_frac[subject][axis] = (
                sum(1 for c in cats_for_valid if c == axis) / n if n else 0.0
            )

    ys = [subj_mean_delta[s] for s in MAIN_STUDY]
    if any(y is None for y in ys):
        # Fall back: drop subjects with no valid delta
        valid_subj = [s for s in MAIN_STUDY if subj_mean_delta[s] is not None]
        ys = [subj_mean_delta[s] for s in valid_subj]
    else:
        valid_subj = list(MAIN_STUDY)
    for axis in AXIS_ORDER:
        xs = [subj_axis_frac[s][axis] for s in valid_subj]
        r = pearson_r(xs, ys)
        key_axis = axis.lower()
        claims[f"appB_6_{key_axis}_corr_with_delta"] = {
            "value": r,
            "estimand": (
                f"Pearson r across the {len(valid_subj)} main-study subjects between "
                f"the fraction of subject's BP questions classified as '{axis}' and "
                f"the subject's mean Delta_spec (C2a - C5)"
            ),
            "contrast": "C2a_full_spec vs C5_baseline",
            "filters": {"subjects": valid_subj, "axis": axis},
            "n": int(len(valid_subj)),
            "ci95_low": None, "ci95_high": None, "p_value": None,
        }
    # Also expose the cross-subject Delta_spec range used in B.6 narrative.
    claims["appB_6_delta_min"] = {
        "value": min(ys) if ys else None,
        "estimand": "minimum per-subject mean Delta_spec across the main-study subjects",
        "contrast": "C2a_full_spec vs C5_baseline",
        "filters": {"subjects": valid_subj},
        "n": int(len(valid_subj)),
        "ci95_low": None, "ci95_high": None, "p_value": None,
    }
    claims["appB_6_delta_max"] = {
        "value": max(ys) if ys else None,
        "estimand": "maximum per-subject mean Delta_spec across the main-study subjects",
        "contrast": "C2a_full_spec vs C5_baseline",
        "filters": {"subjects": valid_subj},
        "n": int(len(valid_subj)),
        "ci95_low": None, "ci95_high": None, "p_value": None,
    }

    # ---- Sort manifest deterministically (idempotency) ---------------------
    input_manifest = sorted(input_manifest, key=lambda e: e["path"])

    # ---- Final payload -----------------------------------------------------
    payload = {
        "schema_version": SCHEMA_VERSION,
        "section": "Appendix B",
        "aggregation_rule": (
            "5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54). "
            "Per-judge per-question score -> per-judge per-(subject, condition, "
            "question) mean -> panel mean. Per-question Delta_spec = "
            "panel(C2a_full_spec) - panel(C5_baseline) when all 5 panel judges "
            "have data on both conditions for that question."
        ),
        "panel": list(PRIMARY_PANEL),
        "claims": claims,
        "tables": {
            "B2_matrix": {
                "columns": list(CATEGORY_ORDER),
                "subjects": list(SUBJECT_ORDER),
                "rows": [
                    {
                        "subject": s,
                        **{c: b2_matrix[s][c] for c in CATEGORY_ORDER},
                        "total": sum(b2_matrix[s][c] for c in CATEGORY_ORDER),
                    }
                    for s in SUBJECT_ORDER
                ],
                "column_totals": {c: column_totals[c] for c in CATEGORY_ORDER},
                "grand_total": grand_total,
            },
            "B3_axis_distribution": {
                axis: {
                    "n": int(axis_counter[axis]),
                    "pct": round(100.0 * axis_counter[axis] / total_n, 1),
                }
                for axis in AXIS_ORDER
            },
            "B3_per_subject": {
                s: {a: int(per_subject_axis_count[s][a]) for a in AXIS_ORDER}
                for s in SUBJECT_ORDER
            },
            "B4_axis_mean_delta_spec": {
                axis: {
                    "n": int(len(axis_pool[axis])),
                    "mean": statistics.mean(axis_pool[axis]) if axis_pool[axis] else None,
                    "median": median(axis_pool[axis]) if axis_pool[axis] else None,
                }
                for axis in AXIS_ORDER
            },
            "B5_per_subject_axis_delta": per_subject_axis_delta,
            "B6_correlations": {
                axis: pearson_r(
                    [subj_axis_frac[s][axis] for s in valid_subj],
                    [subj_mean_delta[s] for s in valid_subj],
                )
                for axis in AXIS_ORDER
            },
            "B6_subject_mean_delta": {s: subj_mean_delta[s] for s in valid_subj},
            "B6_subject_axis_frac": {s: subj_axis_frac[s] for s in valid_subj},
            "B6_n_valid_subjects": int(len(valid_subj)),
        },
        "provenance": {
            "script": "scripts/_v11_emit_appendix_b_battery.py",
            "script_version": SCRIPT_VERSION,
            "run_timestamp": EMIT_DATE,
            "input_manifest": input_manifest,
            "notes": [
                "B.2 counts come directly from each subject's battery JSON; "
                "no judgment data is involved in B.2.",
                "B.3 axis labels come from docs/research/question_category_audit.json; "
                "the Haiku-classifier output is the primary source. Re-deriving "
                "would require rerunning that classifier.",
                "B.4, B.5, B.6 per-question Delta_spec values are recomputed "
                "from per-judge JSON files under the v11 5-judge primary rule.",
                "Franklin's per-question deltas under the spec contrast are "
                "fully populated only on (C5_baseline, C2a_full_spec) which both "
                "have 5-judge coverage in the legacy data; if any are missing the "
                "subject contributes only valid cells.",
            ],
        },
    }
    return payload


# --- Output rendering -------------------------------------------------------


def fmt(x, digits=2, signed=False):
    if x is None:
        return "n/a"
    if signed:
        sign = "+" if x >= 0 else "-"
        return f"{sign}{abs(x):.{digits}f}"
    return f"{x:.{digits}f}"


def compare(scaffold, paper, tol=VERIFY_TOLERANCE):
    if scaffold is None and paper is None:
        return ("MATCH", 0.0)
    if scaffold is None or paper is None:
        return ("MISMATCH(missing)", float("inf"))
    delta = scaffold - paper
    if abs(delta) <= tol + 1e-9:
        return ("MATCH", abs(delta))
    return (f"MISMATCH({delta:+.4f})", abs(delta))


def render_markdown(payload: dict) -> str:
    lines = []
    lines.append("# v11 emit: Appendix B (Question Batteries)")
    lines.append("")
    lines.append(
        f"_Generated by `scripts/_v11_emit_appendix_b_battery.py` "
        f"(timestamp: {EMIT_DATE}, script version: {SCRIPT_VERSION})_"
    )
    lines.append("")
    lines.append("Aggregation: " + payload["aggregation_rule"])
    lines.append("")
    lines.append("Panel: " + ", ".join(payload["panel"]))
    lines.append("")

    # ---- B.2 table ---------------------------------------------------------
    lines.append("## B.2 Per-subject battery composition (15 x 10)")
    lines.append("")
    lines.append("Compared cell-by-cell to v10 paper Table B.2.")
    lines.append("")
    short_cols = ["decis", "val", "rel", "conf", "learn", "risk", "creat",
                  "stress", "career", "ch_o_t"]
    header = (
        "| Subject | "
        + " | ".join(short_cols)
        + " | Total | verify |"
    )
    sep = "|---|" + "---:|" * (len(short_cols) + 1) + ":--|"
    lines.append(header)
    lines.append(sep)
    b2 = payload["tables"]["B2_matrix"]
    for row in b2["rows"]:
        sid = row["subject"]
        row_vals = [row[c] for c in CATEGORY_ORDER]
        paper_vals = PAPER_B2[sid]
        ok = (row_vals == paper_vals)
        verify = "MATCH" if ok else f"MISMATCH({[a-b for a,b in zip(row_vals, paper_vals)]})"
        lines.append(
            f"| {sid} | "
            + " | ".join(str(v) for v in row_vals)
            + f" | {row['total']} | {verify} |"
        )
    # Column totals row
    col_total_vals = [b2["column_totals"][c] for c in CATEGORY_ORDER]
    paper_col_totals = PAPER_B2_COLUMN_TOTALS
    col_ok = col_total_vals == paper_col_totals
    col_verify = "MATCH" if col_ok else f"MISMATCH({[a-b for a,b in zip(col_total_vals, paper_col_totals)]})"
    lines.append(
        f"| **Column total** | "
        + " | ".join(f"**{v}**" for v in col_total_vals)
        + f" | **{b2['grand_total']}** | {col_verify} |"
    )
    paper_grand = PAPER_B2_GRAND_TOTAL
    grand_verify = "MATCH" if b2["grand_total"] == paper_grand else f"MISMATCH({b2['grand_total'] - paper_grand:+d})"
    lines.append("")
    lines.append(f"Grand total: scaffold = {b2['grand_total']}, paper = {paper_grand}, verify = {grand_verify}")
    lines.append("")

    # ---- B.3 ---------------------------------------------------------------
    lines.append("## B.3 Behavioral-axis distribution")
    lines.append("")
    lines.append("| Axis | n (scaffold) | n (paper) | n verify | pct (scaffold) | pct (paper) | pct verify |")
    lines.append("|---|---:|---:|:--|---:|---:|:--|")
    b3 = payload["tables"]["B3_axis_distribution"]
    for axis in AXIS_ORDER:
        sc_n = b3[axis]["n"]
        sc_pct = b3[axis]["pct"]
        p_n, p_pct = PAPER_B3[axis]
        n_status, _ = compare(float(sc_n), float(p_n))
        pct_status, _ = compare(float(sc_pct), float(p_pct), tol=0.05)  # paper rounds to 0.1
        lines.append(
            f"| {axis} | {sc_n} | {p_n} | {n_status} | "
            f"{sc_pct:.1f}% | {p_pct:.1f}% | {pct_status} |"
        )
    lines.append("")

    # ---- B.4 ---------------------------------------------------------------
    lines.append("## B.4 Axis-level mean Delta_spec (C2a vs C5)")
    lines.append("")
    lines.append("| Axis | n (scaffold) | n (paper) | mean Δ (scaffold) | mean Δ (paper) | verify |")
    lines.append("|---|---:|---:|---:|---:|:--|")
    b4 = payload["tables"]["B4_axis_mean_delta_spec"]
    for axis in AXIS_ORDER:
        sc_n = b4[axis]["n"]
        sc_m = b4[axis]["mean"]
        p_n = PAPER_B4[axis]["n"]
        p_m = PAPER_B4[axis]["mean_delta_spec"]
        m_status, _ = compare(sc_m, p_m)
        n_status, _ = compare(float(sc_n), float(p_n))
        joint = "MATCH" if (m_status == "MATCH" and n_status == "MATCH") else f"n:{n_status}; mean:{m_status}"
        lines.append(
            f"| {axis} | {sc_n} | {p_n} | "
            f"{fmt(sc_m, 4, signed=True)} | {fmt(p_m, 4, signed=True)} | {joint} |"
        )
    lines.append("")

    # ---- B.5 ---------------------------------------------------------------
    lines.append("## B.5 Per-subject by axis Delta_spec")
    lines.append("")
    lines.append("Hamerton triplet stated in paper as LITERAL +1.93, INTERP +2.02, REFUSAL +1.71.")
    lines.append("")
    lines.append("| Subject | LITERAL Δ | INTERP Δ | REFUSAL Δ | LIT verify | INTERP verify | REF verify |")
    lines.append("|---|---:|---:|---:|:--|:--|:--|")
    b5 = payload["tables"]["B5_per_subject_axis_delta"]
    for s in SUBJECT_ORDER:
        triplet = b5[s]
        if s == "hamerton":
            paper_axis = PAPER_B5_HAMERTON
            stat_lit, _ = compare(triplet["LITERAL_RECALL"], paper_axis["LITERAL_RECALL"])
            stat_int, _ = compare(triplet["INTERPRETIVE_INFERENCE"], paper_axis["INTERPRETIVE_INFERENCE"])
            stat_ref, _ = compare(triplet["REFUSAL_TRIGGERING"], paper_axis["REFUSAL_TRIGGERING"])
        else:
            stat_lit = stat_int = stat_ref = "(no paper claim)"
        lines.append(
            f"| {s} | "
            f"{fmt(triplet['LITERAL_RECALL'], 2, signed=True)} | "
            f"{fmt(triplet['INTERPRETIVE_INFERENCE'], 2, signed=True)} | "
            f"{fmt(triplet['REFUSAL_TRIGGERING'], 2, signed=True)} | "
            f"{stat_lit} | {stat_int} | {stat_ref} |"
        )
    lines.append("")

    # ---- B.6 ---------------------------------------------------------------
    lines.append("## B.6 Battery-composition correlations with subject-level Delta_spec")
    lines.append("")
    lines.append("| Axis | r (scaffold) | r (paper) | verify |")
    lines.append("|---|---:|---:|:--|")
    b6 = payload["tables"]["B6_correlations"]
    for axis in AXIS_ORDER:
        sc_r = b6[axis]
        p_r = PAPER_B6[f"{axis}_corr_with_delta"]
        status, _ = compare(sc_r, p_r)
        lines.append(f"| {axis} | {fmt(sc_r, 4, signed=True)} | {fmt(p_r, 4, signed=True)} | {status} |")
    rng_lo = payload["claims"]["appB_6_delta_min"]["value"]
    rng_hi = payload["claims"]["appB_6_delta_max"]["value"]
    lo_status, _ = compare(rng_lo, PAPER_B6["delta_min"])
    hi_status, _ = compare(rng_hi, PAPER_B6["delta_max"])
    lines.append("")
    lines.append(
        f"Cross-subject Delta_spec range: scaffold "
        f"[{fmt(rng_lo, 4, signed=True)}, {fmt(rng_hi, 4, signed=True)}]; "
        f"paper [{PAPER_B6['delta_min']:+.2f}, {PAPER_B6['delta_max']:+.2f}]. "
        f"min: {lo_status}; max: {hi_status}."
    )
    lines.append("")

    # ---- Provenance --------------------------------------------------------
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Script: `{payload['provenance']['script']}` (version {payload['provenance']['script_version']})")
    lines.append("")
    lines.append("Input manifest (SHA-256, size, n_records):")
    lines.append("")
    for entry in payload["provenance"]["input_manifest"]:
        nrec = "" if entry["n_records"] is None else f" n={entry['n_records']}"
        lines.append(f"- `{entry['path']}` {entry['sha256'][:12]}... {entry['size_bytes']}B{nrec}")
    lines.append("")
    lines.append("Notes:")
    for n in payload["provenance"]["notes"]:
        lines.append(f"- {n}")
    lines.append("")

    return "\n".join(lines) + "\n"


# --- Atomic write -----------------------------------------------------------


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# --- Verify -----------------------------------------------------------------


def collect_verify_pairs(payload: dict) -> list[tuple[str, object, object, str]]:
    """Return (label, scaffold, paper, status) tuples for every paper claim."""
    pairs: list[tuple[str, object, object, str]] = []

    # B.2 cells
    b2 = payload["tables"]["B2_matrix"]
    for row in b2["rows"]:
        sid = row["subject"]
        for ci, c in enumerate(CATEGORY_ORDER):
            sc = row[c]
            p = PAPER_B2[sid][ci]
            status, _ = compare(float(sc), float(p))
            pairs.append((f"B2.{sid}.{c}", sc, p, status))
        # Per-subject total: globals + Hamerton = 39, Franklin = 40.
        expected_total = 40 if sid == "franklin" else 39
        status, _ = compare(float(row["total"]), float(expected_total))
        pairs.append((f"B2.{sid}.total", row["total"], expected_total, status))
    for ci, c in enumerate(CATEGORY_ORDER):
        sc = b2["column_totals"][c]
        p = PAPER_B2_COLUMN_TOTALS[ci]
        status, _ = compare(float(sc), float(p))
        pairs.append((f"B2.column_total.{c}", sc, p, status))
    status, _ = compare(float(b2["grand_total"]), float(PAPER_B2_GRAND_TOTAL))
    pairs.append(("B2.grand_total", b2["grand_total"], PAPER_B2_GRAND_TOTAL, status))

    # B.3
    b3 = payload["tables"]["B3_axis_distribution"]
    for axis in AXIS_ORDER:
        p_n, p_pct = PAPER_B3[axis]
        status, _ = compare(float(b3[axis]["n"]), float(p_n))
        pairs.append((f"B3.{axis}.n", b3[axis]["n"], p_n, status))
        status, _ = compare(float(b3[axis]["pct"]), float(p_pct), tol=0.05)
        pairs.append((f"B3.{axis}.pct", b3[axis]["pct"], p_pct, status))
    status, _ = compare(float(payload["claims"]["appB_3_total_n"]["value"]), float(PAPER_B3["TOTAL"][0]))
    pairs.append(("B3.total_n", payload["claims"]["appB_3_total_n"]["value"], PAPER_B3["TOTAL"][0], status))

    # B.4
    b4 = payload["tables"]["B4_axis_mean_delta_spec"]
    for axis in AXIS_ORDER:
        sc_m = b4[axis]["mean"]
        p_m = PAPER_B4[axis]["mean_delta_spec"]
        status, _ = compare(sc_m, p_m)
        pairs.append((f"B4.{axis}.mean_delta_spec", sc_m, p_m, status))
        sc_n = b4[axis]["n"]
        p_n = PAPER_B4[axis]["n"]
        status, _ = compare(float(sc_n), float(p_n))
        pairs.append((f"B4.{axis}.n", sc_n, p_n, status))

    # B.5: Hamerton triplet only (paper text states this)
    hb = payload["tables"]["B5_per_subject_axis_delta"]["hamerton"]
    for axis, paper_val in PAPER_B5_HAMERTON.items():
        sc = hb[axis]
        status, _ = compare(sc, paper_val)
        pairs.append((f"B5.hamerton.{axis}", sc, paper_val, status))

    # B.6
    b6 = payload["tables"]["B6_correlations"]
    for axis in AXIS_ORDER:
        sc = b6[axis]
        p = PAPER_B6[f"{axis}_corr_with_delta"]
        status, _ = compare(sc, p)
        pairs.append((f"B6.{axis}.corr", sc, p, status))
    rng_lo = payload["claims"]["appB_6_delta_min"]["value"]
    rng_hi = payload["claims"]["appB_6_delta_max"]["value"]
    status, _ = compare(rng_lo, PAPER_B6["delta_min"])
    pairs.append(("B6.delta_min", rng_lo, PAPER_B6["delta_min"], status))
    status, _ = compare(rng_hi, PAPER_B6["delta_max"])
    pairs.append(("B6.delta_max", rng_hi, PAPER_B6["delta_max"], status))

    return pairs


def run_verify(payload: dict) -> bool:
    pairs = collect_verify_pairs(payload)
    n_match = sum(1 for _, _, _, s in pairs if s == "MATCH")
    n_total = len(pairs)
    print()
    print("=" * 78)
    print(f"VERIFY: {n_match}/{n_total} cells MATCH within {VERIFY_TOLERANCE}")
    print("=" * 78)
    for label, sc, p, status in pairs:
        if status == "MATCH":
            continue
        sc_disp = f"{sc:.4f}" if isinstance(sc, float) else str(sc)
        p_disp = f"{p:.4f}" if isinstance(p, float) else str(p)
        print(f"  {label:60s} scaffold={sc_disp} paper={p_disp} -> {status}")
    if n_match < n_total:
        print()
        print("(MATCH cells suppressed; see emit markdown for full table.)")
    return n_match == n_total


# --- Main -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--verify", action="store_true",
        help="After emit, compare every value against v10 paper Appendix B claims; exit 1 on mismatch.",
    )
    args = parser.parse_args()

    payload = build_payload()

    json_text = json.dumps(payload, indent=2, sort_keys=False)
    atomic_write(OUT_JSON, json_text + "\n")

    md_text = render_markdown(payload)
    atomic_write(OUT_MD, md_text)

    n_claims = len(payload["claims"])
    print(f"Appendix B emit complete: {n_claims} claim_ids emitted.")
    print(f"  JSON: {OUT_JSON}")
    print(f"  MD:   {OUT_MD}")

    if args.verify:
        ok = run_verify(payload)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
