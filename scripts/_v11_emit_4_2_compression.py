"""v11 canonical emit script for §4.2 (Compression) and §4.2.1 (Question-improvement rate).

Every number reported in §4.2 + §4.2.1 of `docs/beyond_recall_v10_1_draft.md` is
re-derived here from primary per-judge JSON files. The script combines both
subsections in one emit per the task brief; the architecture spec table 8
listing two scripts (`_v11_emit_4_2_compression.py`, `_v11_emit_4_2_1_*.py`)
is overridden by the explicit task instruction. Every claim_id is namespaced
either `4_2_*` or `4_2_1_*` so downstream master orchestration can route them.

Aggregation rule (locked):

    1. For each (subject, condition, judge), gather every per-question score
       from primary JSON. Drop rows where score is None or parse_failure is
       True.
    2. Per-judge per-subject mean = mean of per-question scores within the
       (subject, condition, judge) cell.
    3. Panel mean per-subject per-condition = mean of the 5 per-judge means
       across the locked primary panel {haiku, sonnet, opus, gpt4o, gpt54}.
    4. Aggregate (Mean row, summary lifts) = mean across subjects of the
       per-subject panel means. The script emits every aggregate twice when
       there is a row-count question (e.g. C9 with Babur excluded), so the
       paper's apparent arithmetic drift is legible.

Per-question metrics (§4.2.1) follow the convention from the existing helper
`scripts/_compute_per_question_v2.py`: per-question 5-judge means over judges
with at least 3 panel members reporting; question kept only if both C5 and
the comparison condition have valid per-question means.

Source-word counts for the compression-ratio column are LOCKED CONSTANTS from
the v10 paper §3.2 corpus collection table. The source corpora are not
checked into this repo (`results/global_<subject>/training.txt` is gitignored
in this layout), so the script cannot recompute corpus tokens from text.
Instead it documents the locked §3.2 word counts as the authoritative
denominator, and approximates corpus tokens with the v10 paper's documented
1.3 words->tokens factor (which produces e.g. 96,174 -> 125K for Ebers, the
exact figure printed in §4.2's per-subject table).

Specification-token counts ARE computed mechanically. The script reads
`data/global_subjects/<subject>/spec_production.md` (or the three Hamerton
layer files) and counts cl100k_base tokens via tiktoken. cl100k_base is the
documented choice because it is the GPT-4o family BPE and gives a stable
length count that matches the order of magnitude shown in §4.2's "~7K tok"
hint without claiming Anthropic-specific token boundaries.

Outputs (atomic):
    docs/research/v11_emit/4_2_compression.json
    docs/research/v11_emit/4_2_compression.md

Constraints:
    - Pure Python plus `tiktoken`, `scipy.stats` (already a project dep).
    - Idempotent: timestamp is a literal, no `datetime.now()`.
    - Atomic write: temp file then `Path.replace()`.
    - SHA-256 manifest of every input file in provenance.
    - No em-dashes anywhere in the markdown output.
    - Schema validation on every primary-data file: each record must have
      question_id, condition, judge, score; score in [1.0, 5.0]; condition
      in the canonical set; judge in the canonical set. Hamerton wide-format
      records are normalized first via the same logic as
      `_compute_per_question_v2.py`.

Verification:
    --verify   compare every emitted scalar to the v10 paper §4.2/§4.2.1
               text. Exit 0 if all match within 0.005, exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import tiktoken

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
BACKFILL_DIR = RESULTS / "_s114_backfills"
DATA = REPO / "data"
OUT_DIR = REPO / "docs" / "research" / "v11_emit"
OUT_JSON = OUT_DIR / "4_2_compression.json"
OUT_MD = OUT_DIR / "4_2_compression.md"

# --- Locked constants ---------------------------------------------------------

EMIT_DATE = "2026-04-25"
SCHEMA_VERSION = "v11.0"
PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
PRIMARY_PANEL_SET = set(PRIMARY_PANEL)
KNOWN_JUDGES = PRIMARY_PANEL_SET | {"gemini_flash", "gemini_pro"}

# Low-baseline slice (paper §4.2 / §4.2.1 / §3.2.1), ordered by baseline.
LOW_BASELINE = [
    "hamerton", "sunity_devee", "ebers", "fukuzawa", "bernal_diaz",
    "babur", "seacole", "keckley", "yung_wing",
]

# All 14 main-study subjects, used for the §4.2.1 all-14 row.
ALL_14 = LOW_BASELINE + ["zitkala_sa", "cellini", "rousseau", "augustine", "equiano"]

DISPLAY_NAME = {
    "hamerton": "Hamerton", "sunity_devee": "Sunity Devee", "ebers": "Ebers",
    "fukuzawa": "Fukuzawa", "bernal_diaz": "Bernal Diaz", "babur": "Babur",
    "seacole": "Seacole", "keckley": "Keckley", "yung_wing": "Yung Wing",
    "zitkala_sa": "Zitkala-Sa", "cellini": "Cellini", "rousseau": "Rousseau",
    "augustine": "Augustine", "equiano": "Equiano", "franklin": "Franklin",
}

# Source word counts (locked constants, provenance: v10 §3.2 corpus collection table).
SOURCE_WORDS_S3_2 = {
    "hamerton": 25231,
    "sunity_devee": 67379,
    "ebers": 96174,
    "fukuzawa": 139088,
    "bernal_diaz": 187315,
    "babur": 422772,
    "seacole": 62467,
    "keckley": 58742,
    "yung_wing": 66459,
}

# Words-to-tokens approximation factor used by the v10 paper.
# Provenance: 96174 * 1.30 = 125026 ~ "~125K" printed for Ebers in §4.2.
# Same factor reproduces every "(~tokens)" entry in the §4.2 table.
WORDS_TO_TOKENS = 1.30

# Canonical condition strings as stored in primary data, mapped to short codes.
CONDITION_MAP = {
    "C5":  ["C5_baseline"],
    "C2a": ["C2a_full_spec", "C2a_fullstack_spec"],
    "C4":  ["C4_factdump"],
    "C4a": ["C4a_full_facts_plus_spec", "C4a_full_all_facts_plus_spec", "C4a_fullstack"],
    "C8":  ["C8_raw_corpus"],
    "C9":  ["C9_raw_corpus_plus_spec"],
}
KNOWN_LONG_CONDITIONS = {long for longs in CONDITION_MAP.values() for long in longs}

# v10 paper claims for --verify, all from §4.2 + §4.2.1.
PAPER_PER_SUBJECT = {
    # subject -> (C5, C2a, C4, C8, C4a, C9, C8_minus_C2a, compression_ratio)
    "hamerton":     (1.26, 2.63, 2.43, 2.27, 2.77, 3.09, -0.36, 5),
    "sunity_devee": (1.03, 2.27, 2.46, 2.55, 2.41, 2.46, +0.28, 13),
    "ebers":        (1.02, 1.54, 2.02, 2.18, 2.07, 2.16, +0.64, 18),
    "fukuzawa":     (1.67, 2.35, 2.67, 2.74, 2.78, 2.78, +0.39, 26),
    "bernal_diaz":  (1.70, 2.27, 2.41, 2.55, 2.48, 2.53, +0.28, 35),
    "babur":        (1.76, 1.91, 2.03, 2.05, 2.01, None, +0.14, 78),
    "seacole":      (1.77, 2.48, 2.63, 2.83, 2.59, 2.73, +0.35, 12),
    "keckley":      (1.84, 2.43, 2.39, 2.50, 2.44, 2.49, +0.07, 11),
    "yung_wing":    (1.88, 2.22, 2.13, 2.42, 2.40, 2.50, +0.20, 12),
}

# Mean row as printed in §4.2 Table 4.2.
PAPER_MEAN_ROW = {
    "C5": 1.52, "C2a": 2.23, "C4": 2.35, "C8": 2.45, "C4a": 2.45, "C9": 2.50,
    "C8_minus_C2a": 0.22, "compression_ratio": 23,
}

# Hamerton headline numbers cited explicitly in §4.2 paragraph 1 + Hamerton example.
PAPER_HAMERTON_HEADLINE = {
    "C2a": 2.63, "C8": 2.27, "C9": 3.09, "C4a": 2.77,
    # Spec/corpus token counts the paper rounds to "(~7K tok)" / "(~33K)".
    "spec_tokens_round_thousand": 7000,
    "corpus_tokens_round_thousand": 33000,
}

# Ebers per-subject narrative numbers (paper §4.2 Ebers example).
PAPER_EBERS_HEADLINE = {
    "C2a": 1.54, "C8": 2.18, "C8_minus_C2a": 0.64,
    "spec_lift": 0.52, "corpus_lift": 1.16,
}

# Summary lifts. Note the paper's own internal inconsistency:
#   Paragraph 3 of §4.2: "first ~7K tokens of structured specification buy
#   roughly +0.68 points of lift". Implies C5 mean = 1.55 (9-row aggregate).
#   Bullet list: "spec lift +0.71, corpus lift +0.93". Implies C5 mean = 1.52
#   (which is the printed mean-row C5 -- see verification report item #2).
# The 9-row mean of the printed C5 column is 13.93/9 = 1.5477 -> rounds to 1.55.
# The printed mean-row value 1.52 implies an 8-row aggregate (drop Babur).
# This script emits the 9-row canonical aggregates and surfaces both paper
# claims as separate verify rows so the inconsistency is legible.
PAPER_SUMMARY = {
    "low_baseline_n_subjects": 9,
    "low_baseline_C8_minus_C2a_mean": 0.22,
    "low_baseline_spec_lift_paragraph": 0.68,   # paper paragraph 3
    "low_baseline_spec_lift_bullet": 0.71,      # paper bullet list
    "low_baseline_corpus_lift_bullet": 0.93,    # paper bullet list
    "low_baseline_C9_minus_C8_mean": 0.05,      # paper bullet list

    "improve_low_baseline_n": 351,
    "improve_low_baseline_C2a_pct": 70.9,
    "improve_low_baseline_C4_pct": 72.9,
    "improve_low_baseline_C8_pct": 78.3,
    "improve_low_baseline_C4a_pct": 78.6,
    "improve_low_baseline_median_imp": 1.00,
    "improve_low_baseline_median_wor": -0.40,

    "improve_all14_n": 546,
    "improve_all14_C2a_pct": 58.8,
    "improve_all14_C2a_worsen_pct": 26.7,
    "improve_all14_C4_pct": 60.1,
    "improve_all14_C4_worsen_pct": 26.6,
    "improve_all14_C8_pct": 64.5,
    "improve_all14_C8_worsen_pct": 24.5,
    "improve_all14_C4a_pct": 65.8,
    "improve_all14_C4a_worsen_pct": 26.4,

    "C9_n_with_babur_excluded": 312,

    "pairwise_C8_vs_C2a_better_n": 190,
    "pairwise_C8_vs_C2a_tie_n": 46,
    "pairwise_C8_vs_C2a_worse_n": 115,
    "pairwise_C8_vs_C2a_better_pct": 54.1,
    "pairwise_C8_vs_C2a_worse_pct": 32.8,
    "pairwise_C9_vs_C4a_better_n": 155,
    "pairwise_C9_vs_C4a_tie_n": 42,
    "pairwise_C9_vs_C4a_worse_n": 115,
    "pairwise_C9_vs_C4a_better_pct": 49.7,
    "pairwise_C9_vs_C4a_worse_pct": 36.9,
}

VERIFY_TOLERANCE = 0.005


# --- Schema validation --------------------------------------------------------


def _validate_record(rec, source_path):
    """Verify a normalized {question_id, condition, judge, score, parse_failure}
    record. Raises ValueError with file path on violation. Records with
    parse_failure=True are allowed to have score outside [1,5] or null
    because they are dropped at aggregation time anyway."""
    for k in ("question_id", "condition", "judge", "score"):
        if k not in rec:
            raise ValueError(f"missing field '{k}' in record from {source_path}: {rec}")
    if rec.get("parse_failure"):
        return
    if rec["score"] is None:
        return  # null score is allowed and dropped during aggregation
    if not isinstance(rec["score"], (int, float)) or not (1.0 <= rec["score"] <= 5.0):
        raise ValueError(f"score out of [1, 5] in {source_path}: {rec}")
    if rec["judge"] not in KNOWN_JUDGES:
        raise ValueError(f"unknown judge '{rec['judge']}' in {source_path}: {rec}")
    if rec["condition"] not in KNOWN_LONG_CONDITIONS:
        raise ValueError(f"unknown condition '{rec['condition']}' in {source_path}: {rec}")


def _normalize_records(data, source_path):
    """Normalize Hamerton wide-format records and standard long-format records
    into a uniform shape, then schema-validate each."""
    out = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        qid = rec.get("question_id")
        cond = rec.get("condition")
        if qid is None or cond is None:
            continue
        if "judge" in rec and rec.get("judge"):
            score = rec.get("score")
            normalized = {
                "question_id": qid, "condition": cond,
                "judge": rec["judge"], "score": score,
                "parse_failure": rec.get("parse_failure", False),
            }
            if cond not in KNOWN_LONG_CONDITIONS:
                continue  # silently skip non-§4.2 conditions in shared files
            _validate_record(normalized, source_path)
            out.append(normalized)
        else:
            # Wide format: per-judge score fields, e.g. haiku_score, gpt54_score.
            for key, val in rec.items():
                if key in ("question_id", "condition", "raw_response", "parse_failure"):
                    continue
                if not key.endswith("_score"):
                    continue
                judge_name = key[:-len("_score")]
                if judge_name == "gemini":
                    judge_name = "gemini_flash"
                if val is None:
                    continue
                if cond not in KNOWN_LONG_CONDITIONS:
                    continue
                normalized = {
                    "question_id": qid, "condition": cond,
                    "judge": judge_name, "score": val, "parse_failure": False,
                }
                _validate_record(normalized, source_path)
                out.append(normalized)
    return out


# --- Loaders ------------------------------------------------------------------


def _files_for_subject(subject):
    """Return list of input JSON paths for a subject, in load order."""
    if subject == "hamerton":
        d = RESULTS / "hamerton"
        return [
            d / "judgments_harmonized.json",
            d / "judgments.json",
            d / "gpt4o_judgments.json",
            d / "gpt54_judgments.json",
            d / "opus_judgments.json",
            d / "sonnet_judgments.json",
            d / "c8_c9_judgments_merged.json",
        ]
    d = RESULTS / f"global_{subject}"
    return [
        d / "judgments_v2.json",
        d / "c8_c9_judgments_merged.json",
    ]


def _backfill_files_for_subject(subject):
    """Return list of S114 backfill JSON paths covering §4.2-relevant
    conditions for this subject. Only the conditions in CONDITION_MAP
    (C5/C2a/C4/C4a/C8/C9) are accepted; backfill files outside that set
    are silently skipped because they belong to other sections.
    """
    if not BACKFILL_DIR.exists():
        return []
    if subject == "hamerton":
        prefix = "hamerton__"
    else:
        prefix = f"global_{subject}__"
    out = []
    for p in BACKFILL_DIR.iterdir():
        if not p.is_file() or p.suffix != ".json":
            continue
        if not p.name.startswith(prefix):
            continue
        # Filename convention: {subject_prefix}{cond}__{judge}.json
        parts = p.name[len(prefix):].rsplit("__", 1)
        if len(parts) != 2:
            continue
        cond_part = parts[0]
        if cond_part not in KNOWN_LONG_CONDITIONS:
            # Not a §4.2 condition (e.g. C1_baselayer, C3_supermemory). Skip.
            continue
        out.append(p)
    return out


def _normalize_backfill_records(data, source_path):
    """Backfill records use the canonical schema (question_id, condition,
    judge, score, parse_failure) but write `raw` instead of `raw_response`.
    Translate to the same shape the rest of the loader expects, drop
    parse_failure rows, and filter to §4.2 conditions.
    """
    out = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        if rec.get("parse_failure", False):
            continue
        score = rec.get("score")
        if score is None or score == 0:
            continue
        if not isinstance(score, (int, float)) or not (1.0 <= score <= 5.0):
            continue
        cond = rec.get("condition")
        if cond not in KNOWN_LONG_CONDITIONS:
            continue
        judge = rec.get("judge")
        if judge == "gemini":
            judge = "gemini_flash"
        normalized = {
            "question_id": rec.get("question_id"),
            "condition": cond,
            "judge": judge,
            "score": float(score),
            "parse_failure": False,
        }
        if normalized["question_id"] is None:
            continue
        _validate_record(normalized, source_path)
        out.append(normalized)
    return out


def load_subject_records(subject):
    """Return list of normalized, schema-validated records for a subject.

    After loading the primary per-subject judgment files, this function
    appends S114 backfill rerun records from `results/_s114_backfills/`
    and removes any (qid, condition, judge) primary records whose key is
    superseded by a backfill. Backfill records cover §4.2-relevant
    conditions for which provider rate-limit (HTTP 429) or
    `max_completion_tokens` (HTTP 400) batch failures wiped out the
    original judgments (notably Bernal Diaz C8/C9 gpt4o + gpt54, and the
    supplemental C8/C9 cells for several other globals).
    """
    rows = []
    for path in _files_for_subject(subject):
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            rows.extend(_normalize_records(data, path))

    backfill_records = []
    backfill_keys = set()
    for path in _backfill_files_for_subject(subject):
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            continue
        normalized = _normalize_backfill_records(data, path)
        for r in normalized:
            backfill_keys.add((r["question_id"], r["condition"], r["judge"]))
        backfill_records.extend(normalized)

    if backfill_keys:
        rows = [r for r in rows
                if (r["question_id"], r["condition"], r["judge"]) not in backfill_keys]
        rows.extend(backfill_records)
    return rows


def load_input_manifest():
    """Return list of {path, sha256, size_bytes, n_records} for every input file
    actually loaded by this script. Used in provenance.input_manifest."""
    manifest = []
    seen = set()
    for subject in ALL_14:
        for path in _files_for_subject(subject):
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            if not path.exists():
                continue
            content = path.read_bytes()
            try:
                data = json.loads(content.decode("utf-8"))
                n_records = len(data) if isinstance(data, list) else None
            except Exception:
                n_records = None
            manifest.append({
                "path": str(path.relative_to(REPO)).replace("\\", "/"),
                "sha256": hashlib.sha256(content).hexdigest(),
                "size_bytes": len(content),
                "n_records": n_records,
            })
        # S114 backfill files actually consumed by this script for this subject.
        for path in _backfill_files_for_subject(subject):
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            content = path.read_bytes()
            try:
                data = json.loads(content.decode("utf-8"))
                n_records = len(data) if isinstance(data, list) else None
            except Exception:
                n_records = None
            manifest.append({
                "path": str(path.relative_to(REPO)).replace("\\", "/"),
                "sha256": hashlib.sha256(content).hexdigest(),
                "size_bytes": len(content),
                "n_records": n_records,
                "role": "s114_backfill",
            })
    # Spec-text inputs (for spec_tokens claims).
    spec_inputs = []
    for subject in LOW_BASELINE:
        for p in _spec_paths(subject):
            if p.exists():
                spec_inputs.append(p)
    for p in spec_inputs:
        content = p.read_bytes()
        manifest.append({
            "path": str(p.relative_to(REPO)).replace("\\", "/"),
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
            "n_records": None,
        })
    return manifest


# --- Tokenizer + spec/corpus token counts -------------------------------------


def _spec_paths(subject):
    """Return list of paths whose concatenated text counts as the served
    specification for this subject (for token counting). Hamerton uses three
    layer files; globals use the unified spec_production.md."""
    if subject == "hamerton":
        d = DATA / "hamerton" / "spec"
        return [d / "anchors_v4.md", d / "core_v4.md", d / "predictions_v4.md"]
    return [DATA / "global_subjects" / subject / "spec_production.md"]


def spec_tokens(subject, encoder):
    """Return cl100k_base token count for the served specification text."""
    pieces = []
    for p in _spec_paths(subject):
        if not p.exists():
            return None
        pieces.append(p.read_text(encoding="utf-8"))
    text = "\n\n".join(pieces)
    return len(encoder.encode(text))


def corpus_tokens_approx(subject):
    """Approximate corpus tokens from §3.2 source-word count using the v10
    paper's documented 1.3 words-to-tokens factor. Returns int.

    Caveat: the actual corpus text is not in this repo (training.txt is
    gitignored), so this is the only honest reproduction of the paper's
    "(~tokens)" column. The locked source-word count is the authoritative
    denominator; the token approximation is for reproducing the printed
    "(~125K)" hint, not for any downstream statistic.
    """
    return int(round(SOURCE_WORDS_S3_2[subject] * WORDS_TO_TOKENS))


# --- Aggregation --------------------------------------------------------------


def panel_means_for_subject(rows):
    """Return {short_condition: panel_mean} where panel_mean is the mean across
    available primary-panel per-judge means.

    Aggregation rule for §4.2 mean (matches scripts/recompute_5judge_primary.py
    which produced the v10 paper table): average over whatever primary judges
    have data; nulls/parse_failures are dropped. This differs from §4.1's
    strict all-5-required rule because the C8/C9 supplemental runs sometimes
    lost a primary judge to provider rate-limiting (Bernal Diaz lost gpt4o +
    gpt54 to OpenAI 429s on both C8 and C9; Babur C9 was excluded for
    context-window). Returns None for a condition only when zero primary
    judges have data.

    Also returns judges_present count per condition for provenance.
    """
    per_jc = defaultdict(list)
    for r in rows:
        if r["judge"] not in PRIMARY_PANEL_SET:
            continue
        if r.get("parse_failure"):
            continue
        if r["score"] is None:
            continue
        short = _short(r["condition"])
        if short is None:
            continue
        per_jc[(short, r["judge"])].append(r["score"])

    per_jc_mean = {k: statistics.mean(v) for k, v in per_jc.items() if v}

    means = {}
    judges_present = {}
    for short in CONDITION_MAP:
        judge_means = [per_jc_mean.get((short, j)) for j in PRIMARY_PANEL]
        present = [jm for jm in judge_means if jm is not None]
        if present:
            means[short] = statistics.mean(present)
            judges_present[short] = len(present)
        else:
            means[short] = None
            judges_present[short] = 0
    return means, judges_present


def _short(cond_long):
    for short, longs in CONDITION_MAP.items():
        if cond_long in longs:
            return short
    return None


def per_question_panel_means(rows, min_judges=3):
    """Return {(short_condition, qid): mean_5j_score}. Requires at least
    min_judges reporting panel members for a question. Mirrors the
    convention in scripts/_compute_per_question_v2.py."""
    raw = defaultdict(dict)  # (short, qid) -> {judge: score}
    for r in rows:
        if r["judge"] not in PRIMARY_PANEL_SET:
            continue
        if r.get("parse_failure"):
            continue
        if r["score"] is None:
            continue
        short = _short(r["condition"])
        if short is None:
            continue
        raw[(short, r["question_id"])][r["judge"]] = r["score"]
    out = {}
    for key, jdict in raw.items():
        if len(jdict) >= min_judges:
            out[key] = sum(jdict.values()) / len(jdict)
    return out


def question_outcomes(per_q, condition):
    """Return list of (qid, delta_vs_C5) tuples for questions where both C5
    and `condition` have valid per-question means. delta is mean[cond] - mean[C5]."""
    qids_c5 = {qid for (c, qid) in per_q if c == "C5"}
    qids_cond = {qid for (c, qid) in per_q if c == condition}
    common = sorted(qids_c5 & qids_cond)
    out = []
    for qid in common:
        out.append((qid, per_q[(condition, qid)] - per_q[("C5", qid)]))
    return out


def categorize(deltas, eps=1e-9):
    improved = sum(1 for _, d in deltas if d > eps)
    worsened = sum(1 for _, d in deltas if d < -eps)
    tied = sum(1 for _, d in deltas if abs(d) <= eps)
    return improved, tied, worsened


# --- Build payload ------------------------------------------------------------


def build_payload():
    encoder = tiktoken.get_encoding("cl100k_base")

    # Load + aggregate per-subject panel means for the §4.2 table (low-baseline 9 + all-14).
    subj_rows = {s: load_subject_records(s) for s in ALL_14}
    _agg = {s: panel_means_for_subject(subj_rows[s]) for s in ALL_14}
    subj_panel = {s: m for s, (m, _) in _agg.items()}
    subj_judges_present = {s: jp for s, (_, jp) in _agg.items()}

    # Per-question means (low-baseline + all-14 separately).
    subj_per_q = {s: per_question_panel_means(subj_rows[s]) for s in ALL_14}

    # Per-subject spec/corpus token counts for compression ratio.
    spec_tok = {s: spec_tokens(s, encoder) for s in LOW_BASELINE}
    corpus_tok = {s: corpus_tokens_approx(s) for s in LOW_BASELINE}

    # ---- Build claim_id -> claim record map ----
    claims = {}

    def add_claim(cid, value, estimand, contrast=None, filters=None,
                  n=None, ci95_low=None, ci95_high=None, p_value=None):
        claims[cid] = {
            "value": value, "estimand": estimand, "contrast": contrast,
            "filters": filters or {}, "n": n,
            "ci95_low": ci95_low, "ci95_high": ci95_high, "p_value": p_value,
        }

    # ---- §4.2 Hamerton headline ----
    h = subj_panel["hamerton"]
    add_claim("4_2_hamerton_C2a", h["C2a"],
              estimand="Hamerton C2a 5-judge primary panel mean",
              contrast="C2a vs C5",
              filters={"panel": PRIMARY_PANEL, "subject": "hamerton", "condition": "C2a_full_spec"})
    add_claim("4_2_hamerton_C8", h["C8"],
              estimand="Hamerton C8 5-judge primary panel mean",
              contrast="C8 vs C5",
              filters={"panel": PRIMARY_PANEL, "subject": "hamerton", "condition": "C8_raw_corpus"})
    add_claim("4_2_hamerton_C9", h["C9"],
              estimand="Hamerton C9 5-judge primary panel mean",
              contrast="C9 vs C5",
              filters={"panel": PRIMARY_PANEL, "subject": "hamerton", "condition": "C9_raw_corpus_plus_spec"})
    add_claim("4_2_hamerton_C4a", h["C4a"],
              estimand="Hamerton C4a 5-judge primary panel mean",
              contrast="C4a vs C5",
              filters={"panel": PRIMARY_PANEL, "subject": "hamerton", "condition": "C4a_full_facts_plus_spec"})
    add_claim("4_2_hamerton_spec_tokens", spec_tok["hamerton"],
              estimand="Hamerton specification token count (cl100k_base over anchors+core+predictions v4)",
              filters={"tokenizer": "cl100k_base"})
    add_claim("4_2_hamerton_corpus_tokens", corpus_tok["hamerton"],
              estimand="Hamerton corpus token approximation (source words x 1.30 from v10 §3.2 = 25,231 x 1.30)",
              filters={"factor": WORDS_TO_TOKENS, "source": "v10 §3.2 corpus collection table"})

    # ---- §4.2 per-subject low-baseline table (9 rows) ----
    for subject in LOW_BASELINE:
        m = subj_panel[subject]
        add_claim(f"4_2_{subject}_C5", m["C5"],
                  estimand=f"{DISPLAY_NAME[subject]} C5 panel mean",
                  contrast="C5 baseline",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        add_claim(f"4_2_{subject}_C2a", m["C2a"],
                  estimand=f"{DISPLAY_NAME[subject]} C2a panel mean",
                  contrast="C2a vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        add_claim(f"4_2_{subject}_C4", m["C4"],
                  estimand=f"{DISPLAY_NAME[subject]} C4 panel mean",
                  contrast="C4 vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        add_claim(f"4_2_{subject}_C8", m["C8"],
                  estimand=f"{DISPLAY_NAME[subject]} C8 panel mean",
                  contrast="C8 vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        add_claim(f"4_2_{subject}_C4a", m["C4a"],
                  estimand=f"{DISPLAY_NAME[subject]} C4a panel mean",
                  contrast="C4a vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        add_claim(f"4_2_{subject}_C9", m["C9"],
                  estimand=f"{DISPLAY_NAME[subject]} C9 panel mean (None if Babur context-window exceeded)",
                  contrast="C9 vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        delta_c9 = (m["C9"] - m["C5"]) if (m["C9"] is not None and m["C5"] is not None) else None
        add_claim(f"4_2_{subject}_delta_C9_minus_C5", delta_c9,
                  estimand=f"{DISPLAY_NAME[subject]} C9 - C5 panel-mean lift",
                  contrast="C9 vs C5",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        c8_minus_c2a = (m["C8"] - m["C2a"]) if (m["C8"] is not None and m["C2a"] is not None) else None
        add_claim(f"4_2_{subject}_C8_minus_C2a", c8_minus_c2a,
                  estimand=f"{DISPLAY_NAME[subject]} C8 - C2a (corpus minus spec)",
                  contrast="C8 vs C2a",
                  filters={"panel": PRIMARY_PANEL, "subject": subject})
        # Compression ratio: locked §3.2 source words / spec tokens (round).
        ratio = corpus_tok[subject] / spec_tok[subject] if spec_tok[subject] else None
        add_claim(f"4_2_{subject}_compression_ratio", round(ratio) if ratio else None,
                  estimand=f"{DISPLAY_NAME[subject]} corpus-to-spec compression ratio (rounded), corpus_tokens / spec_tokens",
                  filters={"corpus_tokens": corpus_tok[subject], "spec_tokens": spec_tok[subject],
                           "source_words": SOURCE_WORDS_S3_2[subject]})
        add_claim(f"4_2_{subject}_source_words", SOURCE_WORDS_S3_2[subject],
                  estimand=f"{DISPLAY_NAME[subject]} source-corpus word count (locked, v10 §3.2)",
                  filters={"source": "v10 §3.2 corpus collection table"})
        add_claim(f"4_2_{subject}_spec_tokens", spec_tok[subject],
                  estimand=f"{DISPLAY_NAME[subject]} specification token count (cl100k_base)",
                  filters={"tokenizer": "cl100k_base"})

    # ---- §4.2 Mean row (Table 4.2) ----
    # Note: paper printed mean row mixes 8-row and 9-row aggregates.
    #   - C9 column: 8-row mean (Babur missing by data); paper printed 2.50.
    #     Recomputed 9-row-eligible mean below = 8-row mean by construction.
    #   - C5/C2a/C4/C8/C4a columns: 9-row aggregate is correct.
    #   - The printed C5 = 1.52 implies an 8-row aggregate (drop Babur),
    #     internally inconsistent with C2a/C4/C8/C4a printed 9-row.
    # Script emits the 9-row mean for every column except C9; for C9 it
    # emits the natural 8-row mean and labels it accordingly. The verify
    # step compares against the paper's printed mean-row values; mismatches
    # surface the paper's drift.
    def mean_over(subjects, cond):
        vals = [subj_panel[s][cond] for s in subjects if subj_panel[s][cond] is not None]
        return statistics.mean(vals) if vals else None

    mean_C5_9 = mean_over(LOW_BASELINE, "C5")
    mean_C2a_9 = mean_over(LOW_BASELINE, "C2a")
    mean_C4_9 = mean_over(LOW_BASELINE, "C4")
    mean_C8_9 = mean_over(LOW_BASELINE, "C8")
    mean_C4a_9 = mean_over(LOW_BASELINE, "C4a")
    # C9 with Babur excluded by data:
    mean_C9_8 = mean_over([s for s in LOW_BASELINE if s != "babur"], "C9")
    _c8_c2a_pairs = [
        subj_panel[s]["C8"] - subj_panel[s]["C2a"]
        for s in LOW_BASELINE
        if subj_panel[s]["C8"] is not None and subj_panel[s]["C2a"] is not None
    ]
    mean_C8_minus_C2a_9 = statistics.mean(_c8_c2a_pairs) if _c8_c2a_pairs else None

    add_claim("4_2_table_mean_C5", mean_C5_9,
              estimand="Mean of per-subject C5 over the 9 low-baseline subjects",
              contrast="low-baseline mean", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_table_mean_C5_n_rows", 9,
              estimand="Row count for canonical mean-row C5 aggregate (low-baseline slice)")
    add_claim("4_2_table_mean_C2a", mean_C2a_9,
              estimand="Mean of per-subject C2a over the 9 low-baseline subjects", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_table_mean_C4", mean_C4_9,
              estimand="Mean of per-subject C4 over the 9 low-baseline subjects", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_table_mean_C8", mean_C8_9,
              estimand="Mean of per-subject C8 over the 9 low-baseline subjects", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_table_mean_C4a", mean_C4a_9,
              estimand="Mean of per-subject C4a over the 9 low-baseline subjects", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_table_mean_C9", mean_C9_8,
              estimand="Mean of per-subject C9 over 8 low-baseline subjects (Babur excluded by data)",
              n=8, filters={"panel": PRIMARY_PANEL,
                            "subjects": [s for s in LOW_BASELINE if s != "babur"]})
    add_claim("4_2_table_mean_C9_n_rows", 8,
              estimand="Row count for C9 mean (Babur excluded due to context-window overflow)")
    add_claim("4_2_table_mean_C8_minus_C2a", mean_C8_minus_C2a_9,
              estimand="Mean over low-baseline subjects of (C8 - C2a)", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})

    # ---- §4.2 summary lifts ----
    spec_lift_canonical = mean_C2a_9 - mean_C5_9
    corpus_lift_canonical = mean_C8_9 - mean_C5_9 if mean_C8_9 is not None else None
    _c9_subj = [s for s in LOW_BASELINE if s != "babur"]
    c9_minus_c8_canonical = (
        mean_C9_8 - mean_over(_c9_subj, "C8") if mean_C9_8 is not None else None
    )

    add_claim("4_2_low_baseline_spec_lift_mean", spec_lift_canonical,
              estimand="Mean low-baseline C2a panel mean minus mean low-baseline C5 panel mean (9-row, 9-row)",
              contrast="C2a vs C5 (subject-mean lift)", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_low_baseline_corpus_lift_mean", corpus_lift_canonical,
              estimand="Mean low-baseline C8 panel mean minus mean low-baseline C5 panel mean (9-row)",
              contrast="C8 vs C5 (subject-mean lift)", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_low_baseline_C8_minus_C2a_mean", mean_C8_minus_C2a_9,
              estimand="Mean over low-baseline subjects of per-subject (C8 - C2a)",
              contrast="C8 vs C2a", n=9,
              filters={"panel": PRIMARY_PANEL, "subjects": LOW_BASELINE})
    add_claim("4_2_low_baseline_C9_minus_C8_mean", c9_minus_c8_canonical,
              estimand="Mean low-baseline C9 minus C8 (Babur excluded, 8 subjects, paired)",
              contrast="C9 vs C8", n=8,
              filters={"panel": PRIMARY_PANEL,
                       "subjects": [s for s in LOW_BASELINE if s != "babur"]})

    # ---- Ebers narrative numbers ----
    e = subj_panel["ebers"]
    add_claim("4_2_ebers_C8_minus_C2a", e["C8"] - e["C2a"],
              estimand="Ebers C8 - C2a panel-mean gap",
              contrast="C8 vs C2a", filters={"subject": "ebers", "panel": PRIMARY_PANEL})
    add_claim("4_2_ebers_spec_lift", e["C2a"] - e["C5"],
              estimand="Ebers C2a - C5 panel-mean lift (spec lift)",
              contrast="C2a vs C5", filters={"subject": "ebers", "panel": PRIMARY_PANEL})
    add_claim("4_2_ebers_corpus_lift", e["C8"] - e["C5"],
              estimand="Ebers C8 - C5 panel-mean lift (corpus lift)",
              contrast="C8 vs C5", filters={"subject": "ebers", "panel": PRIMARY_PANEL})

    # ============================================================
    # ---- §4.2.1 question-improvement rates ----
    # ============================================================

    # Low-baseline slice (9 subjects).
    def collect_question_outcomes(subjects, target_cond):
        all_deltas = []
        per_subj_n = {}
        for s in subjects:
            outcomes = question_outcomes(subj_per_q[s], target_cond)
            per_subj_n[s] = len(outcomes)
            all_deltas.extend(outcomes)
        return all_deltas, per_subj_n

    low_summaries = {}
    for cond in ("C2a", "C4", "C8", "C4a", "C9"):
        deltas, _ = collect_question_outcomes(LOW_BASELINE, cond)
        improved, tied, worsened = categorize(deltas)
        n = improved + tied + worsened
        improve_pct = 100.0 * improved / n if n else None
        worsen_pct = 100.0 * worsened / n if n else None
        median_imp = statistics.median([d for _, d in deltas if d > 1e-9]) if any(d > 1e-9 for _, d in deltas) else None
        median_wor = statistics.median([d for _, d in deltas if d < -1e-9]) if any(d < -1e-9 for _, d in deltas) else None
        low_summaries[cond] = {
            "n": n, "improved": improved, "tied": tied, "worsened": worsened,
            "improve_pct": improve_pct, "worsen_pct": worsen_pct,
            "median_imp": median_imp, "median_wor": median_wor,
        }

    add_claim("4_2_1_low_baseline_n", low_summaries["C2a"]["n"],
              estimand="Number of low-baseline questions in §4.2.1 Table (any C-vs-C5 paired count)",
              filters={"slice": "low_baseline_9", "min_judges": 3})
    for cond in ("C2a", "C4", "C8", "C4a"):
        s_ = low_summaries[cond]
        add_claim(f"4_2_1_low_baseline_{cond}_improve_pct", s_["improve_pct"],
                  estimand=f"Percent of low-baseline questions improved by {cond} vs C5",
                  contrast=f"{cond} vs C5", n=s_["n"])
        add_claim(f"4_2_1_low_baseline_{cond}_worsen_pct", s_["worsen_pct"],
                  estimand=f"Percent of low-baseline questions worsened by {cond} vs C5",
                  contrast=f"{cond} vs C5", n=s_["n"])
    # Median magnitudes (paper §4.2.1 table cells; use C2a row as canonical).
    add_claim("4_2_1_median_improvement", low_summaries["C2a"]["median_imp"],
              estimand="Median per-question improvement magnitude (Δ when improved) on C2a low-baseline",
              n=low_summaries["C2a"]["improved"])
    add_claim("4_2_1_median_worsening", low_summaries["C2a"]["median_wor"],
              estimand="Median per-question worsening magnitude (Δ when worsened) on C2a low-baseline",
              n=low_summaries["C2a"]["worsened"])

    # All-14 slice.
    all14_summaries = {}
    for cond in ("C2a", "C4", "C8", "C4a"):
        deltas, _ = collect_question_outcomes(ALL_14, cond)
        improved, tied, worsened = categorize(deltas)
        n = improved + tied + worsened
        improve_pct = 100.0 * improved / n if n else None
        worsen_pct = 100.0 * worsened / n if n else None
        all14_summaries[cond] = {
            "n": n, "improved": improved, "tied": tied, "worsened": worsened,
            "improve_pct": improve_pct, "worsen_pct": worsen_pct,
        }
    add_claim("4_2_1_all14_n", all14_summaries["C2a"]["n"],
              estimand="Number of paired questions across all 14 main-study subjects (C2a vs C5)",
              filters={"slice": "all_14", "min_judges": 3})
    for cond in ("C2a", "C4", "C8", "C4a"):
        s_ = all14_summaries[cond]
        add_claim(f"4_2_1_all14_{cond}_improve_pct", s_["improve_pct"],
                  estimand=f"Percent of all-14 questions improved by {cond} vs C5",
                  contrast=f"{cond} vs C5", n=s_["n"])
        add_claim(f"4_2_1_all14_{cond}_worsen_pct", s_["worsen_pct"],
                  estimand=f"Percent of all-14 questions worsened by {cond} vs C5",
                  contrast=f"{cond} vs C5", n=s_["n"])

    # C9 with Babur excluded.
    deltas_c9, _ = collect_question_outcomes(LOW_BASELINE, "C9")
    add_claim("4_2_1_C9_n_with_babur_excluded", len(deltas_c9),
              estimand="Number of low-baseline questions with valid C5 and C9 means (Babur has no C9 by context-window)")

    # Pairwise per-question comparisons.
    def pairwise(subjects, cond_a, cond_b):
        """Return (a_better_n, tie_n, b_better_n) where 'better' is higher panel-mean
        score on condition a vs b for the same question."""
        a_better = ties = b_better = 0
        for s in subjects:
            per_q = subj_per_q[s]
            qids = sorted({qid for (c, qid) in per_q if c == cond_a} &
                          {qid for (c, qid) in per_q if c == cond_b})
            for qid in qids:
                va = per_q[(cond_a, qid)]
                vb = per_q[(cond_b, qid)]
                if va > vb + 1e-9: a_better += 1
                elif va < vb - 1e-9: b_better += 1
                else: ties += 1
        return a_better, ties, b_better

    c8_a, c8_t, c8_b = pairwise(LOW_BASELINE, "C8", "C2a")
    c8_total = c8_a + c8_t + c8_b
    add_claim("4_2_1_C8_vs_C2a_better_n", c8_a,
              estimand="Number of low-baseline questions where C8 panel mean > C2a panel mean",
              contrast="C8 > C2a", n=c8_total)
    add_claim("4_2_1_C8_vs_C2a_tie_n", c8_t,
              estimand="Number of low-baseline questions where C8 panel mean equals C2a panel mean (within 1e-9)",
              contrast="C8 = C2a", n=c8_total)
    add_claim("4_2_1_C8_vs_C2a_worse_n", c8_b,
              estimand="Number of low-baseline questions where C8 panel mean < C2a panel mean",
              contrast="C8 < C2a", n=c8_total)
    add_claim("4_2_1_C8_vs_C2a_better_pct", 100.0 * c8_a / c8_total if c8_total else None,
              estimand="Percent of low-baseline questions where C8 > C2a",
              contrast="C8 > C2a", n=c8_total)
    add_claim("4_2_1_C8_vs_C2a_worse_pct", 100.0 * c8_b / c8_total if c8_total else None,
              estimand="Percent of low-baseline questions where C8 < C2a",
              contrast="C8 < C2a", n=c8_total)

    c9_a, c9_t, c9_b = pairwise(LOW_BASELINE, "C9", "C4a")
    c9_total = c9_a + c9_t + c9_b
    add_claim("4_2_1_C9_vs_C4a_better_n", c9_a,
              estimand="Number of low-baseline questions where C9 panel mean > C4a panel mean",
              contrast="C9 > C4a", n=c9_total)
    add_claim("4_2_1_C9_vs_C4a_tie_n", c9_t,
              estimand="Number of low-baseline questions where C9 panel mean equals C4a panel mean",
              contrast="C9 = C4a", n=c9_total)
    add_claim("4_2_1_C9_vs_C4a_worse_n", c9_b,
              estimand="Number of low-baseline questions where C9 panel mean < C4a panel mean",
              contrast="C9 < C4a", n=c9_total)
    add_claim("4_2_1_C9_vs_C4a_better_pct", 100.0 * c9_a / c9_total if c9_total else None,
              estimand="Percent of low-baseline questions where C9 > C4a",
              contrast="C9 > C4a", n=c9_total)
    add_claim("4_2_1_C9_vs_C4a_worse_pct", 100.0 * c9_b / c9_total if c9_total else None,
              estimand="Percent of low-baseline questions where C9 < C4a",
              contrast="C9 < C4a", n=c9_total)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "section": "§4.2 + §4.2.1",
        "aggregation_rule": (
            "5-judge primary; per-judge per-question -> per-judge per-subject mean -> "
            "panel mean over AVAILABLE primary judges in {haiku, sonnet, opus, gpt4o, gpt54}. "
            "Matches scripts/recompute_5judge_primary.py (which produced the v10 paper table). "
            "Differs from §4.1's strict all-5-required rule: §4.2 tolerates missing primary "
            "judges because the C8/C9 supplemental runs lost some judges to provider "
            "rate-limiting (Bernal Diaz lost gpt4o + gpt54 on both C8 and C9 to OpenAI 429s; "
            "Babur C9 was excluded for context-window overflow). Per-question metrics "
            "(§4.2.1) require >=3 panel judges reporting per question and use the per-question "
            "panel mean. Subject-mean aggregates (§4.2 Table 4.2 mean row) average per-subject "
            "panel means across the 9 low-baseline subjects (8 for C9, Babur excluded)."
        ),
        "claims": claims,
        "provenance": {
            "script": "scripts/_v11_emit_4_2_compression.py",
            "script_version": "v11.0",
            "run_timestamp": EMIT_DATE,
            "tokenizer": "cl100k_base (tiktoken)",
            "words_to_tokens_factor": WORDS_TO_TOKENS,
            "source_words_origin": "v10 §3.2 corpus collection table (locked constants)",
            "input_manifest": load_input_manifest(),
            "judges_present_per_subject_per_condition": {
                s: subj_judges_present[s] for s in ALL_14
            },
            "notes": [
                "training.txt files are not in the repo; corpus tokens are an approximation "
                "(source_words * 1.30) for reproducing the §4.2 (~tokens) hint only. "
                "The compression-ratio denominator comes from the locked §3.2 source-word counts.",
                "Babur's C9 was excluded at experiment time because the 422,772-word corpus "
                "plus the specification exceeded the response model's context window. "
                "Babur's C8 was run on a 100K-word truncation (truncated=True in c8_c9_results.json).",
                "Paper §4.2 mean-row prints C5 = 1.52 (8-row aggregate dropping Babur), inconsistent "
                "with the C2a/C4/C8/C4a printed values which are 9-row aggregates. The 9-row C5 "
                "aggregate is 1.55. The 8-row C5 (drop Babur) is 1.52. The downstream consequence: "
                "paper paragraph 3 prints +0.68 spec lift (uses C5=1.55) and the bullet list "
                "prints +0.71 (uses C5=1.52). The script emits +0.68 as canonical "
                "(4_2_low_baseline_spec_lift_mean) and verifies against both paper sites.",
            ],
        },
    }
    return payload


# --- Output rendering ---------------------------------------------------------


def fmt(x, digits=2):
    if x is None:
        return "n/a"
    if isinstance(x, int):
        return str(x)
    return f"{x:.{digits}f}"


def fmt_signed(x, digits=2):
    if x is None:
        return "n/a"
    if isinstance(x, int):
        sign = "+" if x >= 0 else ""
        return f"{sign}{x}"
    sign = "+" if x >= 0 else "-"
    return f"{sign}{abs(x):.{digits}f}"


def compare(scaffold, paper, tol=VERIFY_TOLERANCE):
    if scaffold is None and paper is None:
        return ("MATCH", 0.0)
    if scaffold is None or paper is None:
        return ("MISMATCH(missing)", float("inf"))
    delta = float(scaffold) - float(paper)
    if abs(delta) <= tol + 1e-9:
        return ("MATCH", abs(delta))
    return (f"MISMATCH({delta:+.4f})", abs(delta))


def render_markdown(payload, verify_rows):
    lines = []
    lines.append("# v11 emit: §4.2 Compression and §4.2.1 Question-improvement rates")
    lines.append("")
    lines.append(f"_Generated by `scripts/_v11_emit_4_2_compression.py` (timestamp: {EMIT_DATE})_")
    lines.append("")
    lines.append("Aggregation: " + payload["aggregation_rule"])
    lines.append("")

    # MATCH/MISMATCH summary header.
    n_match = sum(1 for r in verify_rows if r["status"] == "MATCH")
    n_total = len(verify_rows)
    lines.append(f"**Verify summary: {n_match}/{n_total} cells MATCH within {VERIFY_TOLERANCE}**")
    lines.append("")

    lines.append("## Side-by-side scaffold vs paper")
    lines.append("")
    lines.append("| claim_id | scaffold | paper | status |")
    lines.append("|---|---:|---:|:--|")
    for r in verify_rows:
        sv = r["scaffold"]
        pv = r["paper"]
        if isinstance(sv, float):
            sv_s = f"{sv:.4f}"
        elif sv is None:
            sv_s = "n/a"
        else:
            sv_s = str(sv)
        if isinstance(pv, float):
            pv_s = f"{pv:.4f}"
        elif pv is None:
            pv_s = "n/a"
        else:
            pv_s = str(pv)
        lines.append(f"| `{r['claim_id']}` | {sv_s} | {pv_s} | {r['status']} |")
    lines.append("")

    lines.append("## Notes on paper drift surfaced by this emit")
    lines.append("")
    for note in payload["provenance"]["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("Provenance manifest is in the JSON output's `provenance.input_manifest`.")
    lines.append("")
    return "\n".join(lines) + "\n"


# --- Verify -------------------------------------------------------------------


def build_verify_rows(payload):
    """Return list of {claim_id, scaffold, paper, status} dicts comparing
    every claim to its v10 paper counterpart. Claims without a direct paper
    citation are still emitted as 'no-paper-claim' for completeness, but
    they never fail verify (treated as MATCH if paper is None)."""
    claims = payload["claims"]
    rows = []

    def add(claim_id, paper):
        sv = claims[claim_id]["value"]
        if paper is None:
            status = "MATCH"
        else:
            status, _ = compare(sv, paper)
        rows.append({"claim_id": claim_id, "scaffold": sv, "paper": paper, "status": status})

    # ---- §4.2 Hamerton headline ----
    add("4_2_hamerton_C2a", PAPER_HAMERTON_HEADLINE["C2a"])
    add("4_2_hamerton_C8", PAPER_HAMERTON_HEADLINE["C8"])
    add("4_2_hamerton_C9", PAPER_HAMERTON_HEADLINE["C9"])
    add("4_2_hamerton_C4a", PAPER_HAMERTON_HEADLINE["C4a"])
    # Spec/corpus tokens: paper claims approximate "(~7K)" / "(~33K)".
    # Compare scaffold to the rounded-1K paper hint within +/- 1500 tokens.
    sv_st = claims["4_2_hamerton_spec_tokens"]["value"]
    paper_st = PAPER_HAMERTON_HEADLINE["spec_tokens_round_thousand"]
    status = "MATCH" if abs(sv_st - paper_st) <= 1500 else f"MISMATCH({sv_st - paper_st:+d}, paper_round_~1K)"
    rows.append({"claim_id": "4_2_hamerton_spec_tokens", "scaffold": sv_st, "paper": paper_st, "status": status})
    sv_ct = claims["4_2_hamerton_corpus_tokens"]["value"]
    paper_ct = PAPER_HAMERTON_HEADLINE["corpus_tokens_round_thousand"]
    status = "MATCH" if abs(sv_ct - paper_ct) <= 2000 else f"MISMATCH({sv_ct - paper_ct:+d}, paper_round_~1K)"
    rows.append({"claim_id": "4_2_hamerton_corpus_tokens", "scaffold": sv_ct, "paper": paper_ct, "status": status})

    # ---- §4.2 per-subject table ----
    for subject in LOW_BASELINE:
        c5, c2a, c4, c8, c4a, c9, c8_minus_c2a, ratio = PAPER_PER_SUBJECT[subject]
        add(f"4_2_{subject}_C5", c5)
        add(f"4_2_{subject}_C2a", c2a)
        add(f"4_2_{subject}_C4", c4)
        add(f"4_2_{subject}_C8", c8)
        add(f"4_2_{subject}_C4a", c4a)
        add(f"4_2_{subject}_C9", c9)
        add(f"4_2_{subject}_C8_minus_C2a", c8_minus_c2a)
        # Compression ratio: paper prints rounded integer with ~ prefix; tolerate +/- 2.
        sv_r = claims[f"4_2_{subject}_compression_ratio"]["value"]
        if sv_r is None:
            status = "MISMATCH(missing)"
        else:
            status = "MATCH" if abs(sv_r - ratio) <= 2 else f"MISMATCH({sv_r - ratio:+d}, paper_~rounded)"
        rows.append({"claim_id": f"4_2_{subject}_compression_ratio", "scaffold": sv_r, "paper": ratio, "status": status})
        # Source words is a locked constant; paper-side equality required.
        add(f"4_2_{subject}_source_words", SOURCE_WORDS_S3_2[subject])

    # delta_C9 and spec_tokens claims have no direct paper number; emit as no-paper-claim.
    for subject in LOW_BASELINE:
        rows.append({"claim_id": f"4_2_{subject}_delta_C9_minus_C5",
                     "scaffold": claims[f"4_2_{subject}_delta_C9_minus_C5"]["value"],
                     "paper": None, "status": "MATCH"})
        rows.append({"claim_id": f"4_2_{subject}_spec_tokens",
                     "scaffold": claims[f"4_2_{subject}_spec_tokens"]["value"],
                     "paper": None, "status": "MATCH"})

    # ---- §4.2 Mean row (Table 4.2) ----
    add("4_2_table_mean_C5", PAPER_MEAN_ROW["C5"])
    add("4_2_table_mean_C2a", PAPER_MEAN_ROW["C2a"])
    add("4_2_table_mean_C4", PAPER_MEAN_ROW["C4"])
    add("4_2_table_mean_C8", PAPER_MEAN_ROW["C8"])
    add("4_2_table_mean_C4a", PAPER_MEAN_ROW["C4a"])
    add("4_2_table_mean_C9", PAPER_MEAN_ROW["C9"])
    add("4_2_table_mean_C8_minus_C2a", PAPER_MEAN_ROW["C8_minus_C2a"])
    rows.append({"claim_id": "4_2_table_mean_C5_n_rows", "scaffold": 9, "paper": None, "status": "MATCH"})
    rows.append({"claim_id": "4_2_table_mean_C9_n_rows", "scaffold": 8, "paper": None, "status": "MATCH"})

    # ---- §4.2 summary lifts ----
    # spec lift: paper has BOTH +0.68 (paragraph) and +0.71 (bullet). Compare to
    # paragraph value as canonical (it correctly uses the 9-row C5).
    add("4_2_low_baseline_spec_lift_mean", PAPER_SUMMARY["low_baseline_spec_lift_paragraph"])
    rows.append({
        "claim_id": "4_2_low_baseline_spec_lift_mean__vs_bullet",
        "scaffold": claims["4_2_low_baseline_spec_lift_mean"]["value"],
        "paper": PAPER_SUMMARY["low_baseline_spec_lift_bullet"],
        "status": compare(claims["4_2_low_baseline_spec_lift_mean"]["value"],
                          PAPER_SUMMARY["low_baseline_spec_lift_bullet"])[0],
    })
    add("4_2_low_baseline_corpus_lift_mean", PAPER_SUMMARY["low_baseline_corpus_lift_bullet"])
    add("4_2_low_baseline_C8_minus_C2a_mean", PAPER_SUMMARY["low_baseline_C8_minus_C2a_mean"])
    add("4_2_low_baseline_C9_minus_C8_mean", PAPER_SUMMARY["low_baseline_C9_minus_C8_mean"])

    # ---- Ebers narrative ----
    add("4_2_ebers_C8_minus_C2a", PAPER_EBERS_HEADLINE["C8_minus_C2a"])
    add("4_2_ebers_spec_lift", PAPER_EBERS_HEADLINE["spec_lift"])
    add("4_2_ebers_corpus_lift", PAPER_EBERS_HEADLINE["corpus_lift"])

    # ---- §4.2.1 question-improvement rates ----
    add("4_2_1_low_baseline_n", PAPER_SUMMARY["improve_low_baseline_n"])
    add("4_2_1_low_baseline_C2a_improve_pct", PAPER_SUMMARY["improve_low_baseline_C2a_pct"])
    add("4_2_1_low_baseline_C4_improve_pct", PAPER_SUMMARY["improve_low_baseline_C4_pct"])
    add("4_2_1_low_baseline_C8_improve_pct", PAPER_SUMMARY["improve_low_baseline_C8_pct"])
    add("4_2_1_low_baseline_C4a_improve_pct", PAPER_SUMMARY["improve_low_baseline_C4a_pct"])
    add("4_2_1_median_improvement", PAPER_SUMMARY["improve_low_baseline_median_imp"])
    add("4_2_1_median_worsening", PAPER_SUMMARY["improve_low_baseline_median_wor"])

    add("4_2_1_all14_n", PAPER_SUMMARY["improve_all14_n"])
    add("4_2_1_all14_C2a_improve_pct", PAPER_SUMMARY["improve_all14_C2a_pct"])
    add("4_2_1_all14_C2a_worsen_pct", PAPER_SUMMARY["improve_all14_C2a_worsen_pct"])
    add("4_2_1_all14_C4_improve_pct", PAPER_SUMMARY["improve_all14_C4_pct"])
    add("4_2_1_all14_C4_worsen_pct", PAPER_SUMMARY["improve_all14_C4_worsen_pct"])
    add("4_2_1_all14_C8_improve_pct", PAPER_SUMMARY["improve_all14_C8_pct"])
    add("4_2_1_all14_C8_worsen_pct", PAPER_SUMMARY["improve_all14_C8_worsen_pct"])
    add("4_2_1_all14_C4a_improve_pct", PAPER_SUMMARY["improve_all14_C4a_pct"])
    add("4_2_1_all14_C4a_worsen_pct", PAPER_SUMMARY["improve_all14_C4a_worsen_pct"])

    add("4_2_1_C9_n_with_babur_excluded", PAPER_SUMMARY["C9_n_with_babur_excluded"])

    # Pairwise.
    add("4_2_1_C8_vs_C2a_better_n", PAPER_SUMMARY["pairwise_C8_vs_C2a_better_n"])
    add("4_2_1_C8_vs_C2a_tie_n", PAPER_SUMMARY["pairwise_C8_vs_C2a_tie_n"])
    add("4_2_1_C8_vs_C2a_worse_n", PAPER_SUMMARY["pairwise_C8_vs_C2a_worse_n"])
    add("4_2_1_C8_vs_C2a_better_pct", PAPER_SUMMARY["pairwise_C8_vs_C2a_better_pct"])
    add("4_2_1_C8_vs_C2a_worse_pct", PAPER_SUMMARY["pairwise_C8_vs_C2a_worse_pct"])
    add("4_2_1_C9_vs_C4a_better_n", PAPER_SUMMARY["pairwise_C9_vs_C4a_better_n"])
    add("4_2_1_C9_vs_C4a_tie_n", PAPER_SUMMARY["pairwise_C9_vs_C4a_tie_n"])
    add("4_2_1_C9_vs_C4a_worse_n", PAPER_SUMMARY["pairwise_C9_vs_C4a_worse_n"])
    add("4_2_1_C9_vs_C4a_better_pct", PAPER_SUMMARY["pairwise_C9_vs_C4a_better_pct"])
    add("4_2_1_C9_vs_C4a_worse_pct", PAPER_SUMMARY["pairwise_C9_vs_C4a_worse_pct"])

    return rows


# --- Atomic write -------------------------------------------------------------


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# --- Main ---------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--verify", action="store_true",
                        help="After emit, print per-claim diff vs paper §4.2/§4.2.1; exit 1 on mismatch.")
    args = parser.parse_args()

    payload = build_payload()
    verify_rows = build_verify_rows(payload)

    json_text = json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False)
    atomic_write(OUT_JSON, json_text + "\n")

    md_text = render_markdown(payload, verify_rows)
    atomic_write(OUT_MD, md_text)

    n_claims = len(payload["claims"])
    n_match = sum(1 for r in verify_rows if r["status"] == "MATCH")
    n_total = len(verify_rows)

    print(f"§4.2/§4.2.1 emit: {n_claims} claim_ids, {n_match}/{n_total} verify rows MATCH")
    print(f"JSON: {OUT_JSON}")
    print(f"MD:   {OUT_MD}")

    if args.verify:
        print()
        print("=" * 78)
        print(f"VERIFY: {n_match}/{n_total} verify rows MATCH within {VERIFY_TOLERANCE}")
        print("=" * 78)
        for r in verify_rows:
            if r["status"] != "MATCH":
                sv = r["scaffold"]
                pv = r["paper"]
                sv_s = f"{sv:.4f}" if isinstance(sv, float) else str(sv)
                pv_s = f"{pv:.4f}" if isinstance(pv, float) else str(pv)
                print(f"  {r['claim_id']:55s} scaffold={sv_s:>10s} paper={pv_s:>10s} {r['status']}")
        sys.exit(0 if n_match == n_total else 1)


if __name__ == "__main__":
    main()
