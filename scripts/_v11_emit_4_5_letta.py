"""v11 canonical emit script for §4.5 (and Appendix F) Letta stateful-agent comparison.

Every number reported in §4.5 / Appendix F of `docs/beyond_recall_v10_1_draft.md` for
the Letta stateful-agent vs Base Layer matched-rerun is re-derived from primary
per-judge JSON files by this script. There are no hardcoded per-cell means.

Aggregation rule (locked across the v10/v11 paper, §1 of v11_emit/_ARCHITECTURE.md):

    1. For each (subject, condition, judge), gather every per-question score from
       primary JSON. Drop rows where parse_failure is True or score is missing.
    2. Per-judge per-subject mean = mean of per-question scores within that
       (subject, condition, judge) cell.
    3. Panel mean per-subject per-condition = mean of the per-judge means across
       the 5 panel members {haiku, sonnet, opus, gpt4o, gpt54}.

When per-cell question coverage is balanced across judges (as it is here:
n=39 for Hamerton, n=40 for Ebers and Babur on every judge), Method A
(per-question mean across judges then mean over questions) and Method B
(per-judge mean then mean over judges) produce identical scalars within FP
tolerance. The locked rule is Method B; both are recorded in the JSON for
audit.

The 7-judge panel (adding gemini_flash and gemini_pro) is reported as a
sensitivity check only.

Schema variance is handled in three named branches:

    A. Letta block -> Haiku, 5-judge primary panel
       Source files (per-judge):
         Hamerton: results/run_fullstack_hamerton_20260411_231237/
                   letta_memory_haiku_judgments_<judge>.json
         Ebers:    results/global_ebers/letta_memory_haiku_judgments_<judge>.json
         Babur:    results/global_babur/letta_memory_haiku_judgments_<judge>.json
       (results/ here means C:\\Users\\Aarik\\Anthropic\\memory_system\\data\\
        experiments\\memory_systems\\results\\)
       Schema: list of {question_id, condition, judge, score, parse_failure}
       Conditions: 'C_letta_memory_haiku' (Hamerton) or
                   'C_letta_memory_haiku_<subject>' (Ebers, Babur)

    B. BL unified-brief -> Haiku, 5-judge primary panel
       Source files (per-judge):
         Hamerton: hamerton_bl_c2a_judgments_<judge>.json (sonnet/opus/gpt4o/gpt54)
                   AND analysis/judgments.json -> haiku_score wide field for haiku
         Ebers:    _letta_rerun/ebers_judgments_<judge>.json
         Babur:    _letta_rerun/babur_judgments_<judge>.json
       Schema: list of {question_id, condition, judge, score, parse_failure}
       Conditions: 'BL_C2a_named_<subject>' (Ebers, Babur);
                   'C2a_full_spec' wide-format on Hamerton legacy haiku.

    C. BL full-stack named -> Haiku, 5-judge primary panel
       Source files (per-judge):
         _letta_rerun/fullstack_named/<subject>_fullstack_judgments_<judge>.json
       Schema: list of {question_id, condition, judge, score, parse_failure}
       Conditions: 'BL_C2a_fullstack_named_<subject>'

The 7-judge sensitivity adds gemini_flash and gemini_pro:
    - Letta side: same per-judge file pattern as branch A.
    - BL side (Hamerton): analysis/judgments.json -> gemini_score wide field
                          AND analysis/gemini_pro_judgments.json -> gemini_pro_score
    - BL side (Ebers/Babur): _letta_rerun/<subject>_judgments_<judge>.json
                              for gemini_flash and gemini_pro.

Block sizes (chars) come from the primary stateful_summary / stateful_test_result
JSON `final_blocks[label='human'].size` field, NOT from the .txt mirrors which
have CRLF line endings on Windows.

Corpus word counts are recorded as paper-stated values; no canonical primary-data
script for these exists in the repo. Flagged in summary.data_gaps.

Babur block duplication rate is recomputed from
`docs/research/_letta_blocks/babur_human_block.txt` by splitting into sentences
on `[.!?]` and counting (total - unique_sentences) / total_sentences. Algorithm
documented inline.

Named-entity counts (paper Appendix F: Babur 540 vs 46, Ebers 58 vs 19) and
5-gram corpus-overlap rates have no canonical source script. They are computed
here from the Letta block text and the BL spec_production.md text using
deterministic algorithms documented inline. If the scaffold values disagree
with the paper's quoted values, that is the architecture working as designed:
the scaffold becomes the truth and the paper text is reconciled to match.

Outputs (atomic-written):
    docs/research/v11_emit/4_5_letta.json
    docs/research/v11_emit/4_5_letta.md

Verification:
    --verify   Compare every emitted scalar against §4.5 / Appendix F paper
               claims; exit 0 on full match within 0.005 tolerance, 1 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------- Paths ----------

REPO = Path(__file__).resolve().parents[1]
RERUN = REPO / "docs" / "research" / "_letta_rerun"
FULLSTACK = RERUN / "fullstack_named"
BLOCKS_DIR = REPO / "docs" / "research" / "_letta_blocks"
GLOBAL_DATA = REPO / "data" / "global_subjects"

# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MEMORY_RESULTS = Path(os.environ.get("MEMORY_SYSTEM_ROOT", "")) / "data" / "experiments" / "memory_systems" / "results"
MEMORY_PATH_BY_SUBJECT = {
    "hamerton": MEMORY_RESULTS / "run_fullstack_hamerton_20260411_231237",
    "ebers": MEMORY_RESULTS / "global_ebers",
    "babur": MEMORY_RESULTS / "global_babur",
}

OUT_DIR = REPO / "docs" / "research" / "v11_emit"
OUT_JSON = OUT_DIR / "4_5_letta.json"
OUT_MD = OUT_DIR / "4_5_letta.md"

# ---------- Locked constants ----------

EMIT_DATE = "2026-04-25"
SCHEMA_VERSION = "v11.0"
SCRIPT_VERSION = "1.0.0"
PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
SENSITIVITY_PANEL = PRIMARY_PANEL + ["gemini_flash", "gemini_pro"]
ALL_JUDGES_KNOWN = set(SENSITIVITY_PANEL)

VERIFY_TOLERANCE = 0.005

SUBJECTS = ["hamerton", "ebers", "babur"]
SUBJECT_DISPLAY = {"hamerton": "Hamerton", "ebers": "Ebers", "babur": "Babur"}

# Per-subject question-id ranges (Hamerton uses qids 21-60; Ebers/Babur use 1-40).
EXPECTED_N_BY_SUBJECT = {"hamerton": 39, "ebers": 40, "babur": 40}

# Canonical condition strings expected in each branch; used to assert schema.
LETTA_CONDITION_BY_SUBJECT = {
    "hamerton": "C_letta_memory_haiku",
    "ebers": "C_letta_memory_haiku_ebers",
    "babur": "C_letta_memory_haiku_babur",
}
BL_UNIFIED_CONDITION_BY_SUBJECT = {
    # Hamerton legacy haiku rows live in analysis/judgments.json under
    # 'C2a_full_spec'; the rerun sonnet/opus/gpt4o/gpt54 files use 'C2a_full_spec'
    # too (verified with diag_check_response_inner.py historically). Ebers and
    # Babur use the named condition 'BL_C2a_named_<subject>'.
    "hamerton": "C2a_full_spec",
    "ebers": "BL_C2a_named_ebers",
    "babur": "BL_C2a_named_babur",
}
BL_FULLSTACK_CONDITION_BY_SUBJECT = {
    "hamerton": "BL_C2a_fullstack_named_hamerton",
    "ebers": "BL_C2a_fullstack_named_ebers",
    "babur": "BL_C2a_fullstack_named_babur",
}

# Paper-claimed per-subject means and deltas, for --verify (read from
# docs/beyond_recall_v10_1_draft.md §4.5 lines 1269 and 2432-2434, and
# Appendix F lines 2408 and 2481).
PAPER_CLAIMS = {
    "hamerton": {
        "letta_block_score_haiku": 3.10,
        "bl_unified_brief_score_haiku": 2.96,
        "delta_letta_minus_bl": 0.14,
        # 7-judge sensitivity (line 2438 of paper).
        "letta_block_score_haiku_7judge": None,  # paper reports only delta
        "bl_unified_brief_score_haiku_7judge": None,
        "delta_letta_minus_bl_7judge": 0.20,
        # Full-stack named (line 2481 of paper, §4.5 line 1269).
        "fullstack_bl_score_haiku": None,  # paper reports only delta
        "fullstack_delta_letta_minus_bl": 0.27,
        "letta_block_chars": 22472,
        "corpus_words": 25231,
        "letta_unique_named_entities": None,  # not stated for Hamerton in paper
        "bl_unique_named_entities": None,
        "letta_5gram_overlap_pct": None,
        "bl_5gram_overlap_pct": None,
    },
    "ebers": {
        "letta_block_score_haiku": 2.76,
        "bl_unified_brief_score_haiku": 1.72,
        "delta_letta_minus_bl": 1.05,
        "letta_block_score_haiku_7judge": None,
        "bl_unified_brief_score_haiku_7judge": None,
        "delta_letta_minus_bl_7judge": 0.75,
        "fullstack_bl_score_haiku": None,
        "fullstack_delta_letta_minus_bl": 1.21,
        "letta_block_chars": 68413,
        "corpus_words": 48161,
        "letta_unique_named_entities": 58,
        "bl_unique_named_entities": 19,
        "letta_5gram_overlap_pct": None,
        "bl_5gram_overlap_pct": None,
    },
    "babur": {
        "letta_block_score_haiku": 2.42,
        "bl_unified_brief_score_haiku": 1.88,
        "delta_letta_minus_bl": 0.54,
        "letta_block_score_haiku_7judge": None,
        "bl_unified_brief_score_haiku_7judge": None,
        "delta_letta_minus_bl_7judge": 0.29,
        "fullstack_bl_score_haiku": None,
        "fullstack_delta_letta_minus_bl": 0.38,
        "letta_block_chars": 335349,
        "corpus_words": 222742,
        "letta_unique_named_entities": 540,
        "bl_unique_named_entities": 46,
        "letta_5gram_overlap_pct": None,
        "bl_5gram_overlap_pct": None,
    },
}
PAPER_CLAIMS_GLOBAL = {
    "babur_block_duplication_rate": 0.254,  # paper line 2446 says 25.4%
    "letta_api_ceiling_approx_chars": 333000,  # paper line 2444
}


# ---------- Helpers: schema validation, file I/O ----------


class SchemaError(RuntimeError):
    """Raised when a primary-data file fails the locked schema check."""


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_entry(path: Path, n_records: int | None = None) -> dict:
    return {
        "path": str(path).replace("\\", "/"),
        "sha256": sha256_of(path),
        "size_bytes": path.stat().st_size,
        "n_records": n_records,
    }


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing primary-data file: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def assert_long_format_judgment_record(record: dict, source: Path) -> None:
    """Validate a long-format judgment record per architecture §5."""
    for k in ("question_id", "condition", "judge", "score"):
        if k not in record:
            raise SchemaError(
                f"Schema violation in {source}: record missing key {k!r}: {record!r}"
            )
    judge = record["judge"]
    if judge not in ALL_JUDGES_KNOWN:
        raise SchemaError(
            f"Schema violation in {source}: unknown judge {judge!r} not in {ALL_JUDGES_KNOWN}"
        )
    score = record["score"]
    if score is not None:
        try:
            sf = float(score)
        except (TypeError, ValueError):
            raise SchemaError(
                f"Schema violation in {source}: non-numeric score {score!r} on record {record!r}"
            )
        if not (1.0 <= sf <= 5.0) and not record.get("parse_failure"):
            # Score 0 with parse_failure True is allowed; otherwise out-of-range.
            raise SchemaError(
                f"Schema violation in {source}: score {sf} out of [1,5] on record {record!r}"
            )


def load_long_format_judgments(
    path: Path, expected_judge: str, expected_condition: str, expected_n: int
) -> list[dict]:
    """Load a long-format per-judge JSON; return the kept rows (parse_failure False).

    Asserts every record has the expected judge and one of the expected
    conditions. Asserts at least `expected_n` records present (exact match
    with parse_failure rows allowed). Raises SchemaError on violation.
    """
    raw = load_json(path)
    if not isinstance(raw, list):
        raise SchemaError(f"Expected list at {path}, got {type(raw).__name__}")
    rows = []
    for r in raw:
        assert_long_format_judgment_record(r, path)
        if r["judge"] != expected_judge:
            raise SchemaError(
                f"{path}: expected judge {expected_judge!r}, got {r['judge']!r}"
            )
        if r["condition"] != expected_condition:
            raise SchemaError(
                f"{path}: expected condition {expected_condition!r}, "
                f"got {r['condition']!r}"
            )
        rows.append(r)
    if len(rows) < expected_n:
        raise SchemaError(
            f"{path}: expected at least {expected_n} records, got {len(rows)}"
        )
    return rows


def per_judge_mean_from_long(rows: list[dict]) -> tuple[float | None, int]:
    """Per-judge per-subject mean (Method B inner step). Drops parse_failure."""
    valid = [
        float(r["score"])
        for r in rows
        if not r.get("parse_failure") and r.get("score") is not None
    ]
    if not valid:
        return None, 0
    return statistics.mean(valid), len(valid)


def per_judge_per_question_from_long(rows: list[dict]) -> dict[int, float]:
    """Return {qid: score} for valid (parse_failure=False) records."""
    out = {}
    for r in rows:
        if r.get("parse_failure") or r.get("score") is None:
            continue
        out[int(r["question_id"])] = float(r["score"])
    return out


# ---------- Hamerton legacy haiku loader (wide format) ----------


def load_hamerton_legacy_haiku_for_condition(
    analysis_judgments_path: Path, condition: str, expected_n: int
) -> dict[int, float]:
    """Hamerton's haiku side of the BL unified-brief comparison lives in
    `analysis/judgments.json` as wide-format rows with `haiku_score`. Validate
    that the file has rows for the requested condition and return {qid: score}.
    """
    raw = load_json(analysis_judgments_path)
    if not isinstance(raw, list):
        raise SchemaError(
            f"Expected list at {analysis_judgments_path}, got {type(raw).__name__}"
        )
    rows = [r for r in raw if r.get("condition") == condition]
    if len(rows) < expected_n:
        raise SchemaError(
            f"{analysis_judgments_path}: expected >= {expected_n} rows for "
            f"condition {condition!r}, got {len(rows)}"
        )
    out = {}
    for r in rows:
        score = r.get("haiku_score")
        if score is None or score == 0:
            continue
        try:
            sf = float(score)
        except (TypeError, ValueError):
            raise SchemaError(
                f"{analysis_judgments_path}: non-numeric haiku_score on {r!r}"
            )
        if not (1.0 <= sf <= 5.0):
            raise SchemaError(
                f"{analysis_judgments_path}: haiku_score {sf} out of [1,5] on {r!r}"
            )
        out[int(r["question_id"])] = sf
    return out


def load_hamerton_legacy_wide_for_condition(
    analysis_judgments_path: Path,
    condition: str,
    score_field: str,
    expected_n: int,
) -> dict[int, float]:
    """Generic wide-format loader for `analysis/judgments.json` (gemini_score)
    and `analysis/gemini_pro_judgments.json` (gemini_pro_score).
    """
    raw = load_json(analysis_judgments_path)
    if not isinstance(raw, list):
        raise SchemaError(
            f"Expected list at {analysis_judgments_path}, got {type(raw).__name__}"
        )
    rows = [r for r in raw if r.get("condition") == condition]
    if len(rows) < expected_n:
        raise SchemaError(
            f"{analysis_judgments_path}: expected >= {expected_n} rows for "
            f"condition {condition!r}, got {len(rows)}"
        )
    out = {}
    for r in rows:
        score = r.get(score_field)
        if score is None or score == 0:
            continue
        sf = float(score)
        if not (1.0 <= sf <= 5.0):
            raise SchemaError(
                f"{analysis_judgments_path}: {score_field} {sf} out of [1,5]"
            )
        out[int(r["question_id"])] = sf
    return out


# ---------- Path resolution per branch ----------


def letta_block_judgment_path(subject: str, judge: str) -> Path:
    base = MEMORY_PATH_BY_SUBJECT[subject]
    return base / f"letta_memory_haiku_judgments_{judge}.json"


def bl_unified_judgment_path(subject: str, judge: str) -> Path:
    """Resolve where BL unified-brief per-judge rows live for this subject.

    Returns the path. The schema branch is determined by caller via the
    return-path's location.
    """
    if subject == "hamerton":
        if judge == "haiku":
            # Wide-format legacy file.
            return MEMORY_PATH_BY_SUBJECT[subject] / "analysis" / "judgments.json"
        if judge == "gemini_flash":
            # Wide-format under `gemini_score`.
            return MEMORY_PATH_BY_SUBJECT[subject] / "analysis" / "judgments.json"
        if judge == "gemini_pro":
            return (
                MEMORY_PATH_BY_SUBJECT[subject]
                / "analysis"
                / "gemini_pro_judgments.json"
            )
        # sonnet, opus, gpt4o, gpt54 in long format under _letta_rerun.
        return RERUN / f"hamerton_bl_c2a_judgments_{judge}.json"
    return RERUN / f"{subject}_judgments_{judge}.json"


def bl_fullstack_judgment_path(subject: str, judge: str) -> Path:
    return FULLSTACK / f"{subject}_fullstack_judgments_{judge}.json"


# ---------- Cell-mean computation ----------


def cell_mean_methodB_panel(
    per_judge_qid_scores: dict[str, dict[int, float]], panel: list[str]
) -> tuple[float | None, list[str], dict[str, float]]:
    """Method B: per-judge mean over the judge's per-question scores, then mean
    of the per-judge means across the panel members. Returns
    (panel_mean, missing_judges, per_judge_means).
    """
    per_judge_means = {}
    missing = []
    for j in panel:
        scores = per_judge_qid_scores.get(j) or {}
        if not scores:
            missing.append(j)
            continue
        per_judge_means[j] = statistics.mean(scores.values())
    if missing:
        return None, missing, per_judge_means
    return statistics.mean(per_judge_means.values()), [], per_judge_means


def cell_mean_methodA(
    per_judge_qid_scores: dict[str, dict[int, float]],
) -> tuple[float | None, int]:
    """Method A: per-question mean across available judges, then mean over the
    questions. Returns (mean, n_qids_used).
    """
    all_qids = sorted(set().union(*[set(d.keys()) for d in per_judge_qid_scores.values()]))
    per_q = []
    for qid in all_qids:
        vals = [
            per_judge_qid_scores[j][qid]
            for j in per_judge_qid_scores
            if qid in per_judge_qid_scores[j]
        ]
        if vals:
            per_q.append(statistics.mean(vals))
    if not per_q:
        return None, 0
    return statistics.mean(per_q), len(per_q)


def gather_per_judge_qid_scores(
    subject: str, branch: str, panel: list[str], manifest: list[dict]
) -> dict[str, dict[int, float]]:
    """branch in {'letta', 'bl_unified', 'bl_fullstack'}.

    Returns {judge: {qid: score}} after schema validation. Adds every consumed
    file to the manifest.
    """
    out: dict[str, dict[int, float]] = {}
    expected_n = EXPECTED_N_BY_SUBJECT[subject]
    for j in panel:
        if branch == "letta":
            path = letta_block_judgment_path(subject, j)
            cond = LETTA_CONDITION_BY_SUBJECT[subject]
            rows = load_long_format_judgments(path, j, cond, expected_n)
            manifest.append(manifest_entry(path, n_records=len(rows)))
            out[j] = per_judge_per_question_from_long(rows)
        elif branch == "bl_unified":
            path = bl_unified_judgment_path(subject, j)
            if subject == "hamerton" and j == "haiku":
                qid_scores = load_hamerton_legacy_haiku_for_condition(
                    path, "C2a_full_spec", expected_n
                )
                # Manifest entry deduped by hash regardless of repeat-resolve path.
                manifest.append(manifest_entry(path, n_records=len(qid_scores)))
                out[j] = qid_scores
            elif subject == "hamerton" and j == "gemini_flash":
                qid_scores = load_hamerton_legacy_wide_for_condition(
                    path, "C2a_full_spec", "gemini_score", expected_n
                )
                manifest.append(manifest_entry(path, n_records=len(qid_scores)))
                out[j] = qid_scores
            elif subject == "hamerton" and j == "gemini_pro":
                qid_scores = load_hamerton_legacy_wide_for_condition(
                    path, "C2a_full_spec", "gemini_pro_score", expected_n
                )
                manifest.append(manifest_entry(path, n_records=len(qid_scores)))
                out[j] = qid_scores
            else:
                cond = BL_UNIFIED_CONDITION_BY_SUBJECT[subject]
                # Hamerton sonnet/opus/gpt4o/gpt54 use 'C2a_full_spec' too.
                rows = load_long_format_judgments(path, j, cond, expected_n)
                manifest.append(manifest_entry(path, n_records=len(rows)))
                out[j] = per_judge_per_question_from_long(rows)
        elif branch == "bl_fullstack":
            path = bl_fullstack_judgment_path(subject, j)
            cond = BL_FULLSTACK_CONDITION_BY_SUBJECT[subject]
            rows = load_long_format_judgments(path, j, cond, expected_n)
            manifest.append(manifest_entry(path, n_records=len(rows)))
            out[j] = per_judge_per_question_from_long(rows)
        else:
            raise ValueError(f"Unknown branch {branch!r}")
    return out


# ---------- Block-size + corpus loaders ----------


def load_letta_block_size(subject: str, manifest: list[dict]) -> int:
    """Return the canonical char size of the human memory block for this subject.

    Source priority:
        1. `final_blocks[label='human'].size` from stateful_summary JSON
           (Ebers, Babur).
        2. `final_blocks[].value` length from letta_stateful_test_result.json
           (Hamerton).
    """
    if subject == "hamerton":
        path = MEMORY_PATH_BY_SUBJECT[subject] / "letta_stateful_test_result.json"
        d = load_json(path)
        manifest.append(manifest_entry(path))
        for b in d.get("final_blocks", []):
            if b.get("label") == "human":
                return len(b["value"])
        raise SchemaError(f"No human block found in {path}")
    # Ebers, Babur: use the stateful_summary mirror in _letta_rerun.
    path = RERUN / f"{subject}_stateful_summary.json"
    d = load_json(path)
    manifest.append(manifest_entry(path))
    for b in d.get("final_blocks", []):
        if b.get("label") == "human":
            return int(b["size"])
    raise SchemaError(f"No human block size found in {path}")


def load_letta_block_text(subject: str, manifest: list[dict]) -> str:
    """Return the canonical block text. For Hamerton this comes from
    letta_stateful_test_result.json; for Ebers/Babur from the .txt mirror in
    `_letta_blocks/` (LF-normalized for char-count consistency).
    """
    if subject == "hamerton":
        path = MEMORY_PATH_BY_SUBJECT[subject] / "letta_stateful_test_result.json"
        d = load_json(path)
        for b in d.get("final_blocks", []):
            if b.get("label") == "human":
                return b["value"]
        raise SchemaError(f"No human block found in {path}")
    path = BLOCKS_DIR / f"{subject}_human_block.txt"
    if not path.exists():
        raise FileNotFoundError(f"Missing block text file: {path}")
    manifest.append(manifest_entry(path))
    # Read with universal newlines so CRLF -> LF for portable counts.
    return path.read_text(encoding="utf-8")


def load_bl_spec_text(subject: str, manifest: list[dict]) -> str:
    """The §4.5 BL side served the unified-brief spec.

    For Ebers/Babur, `data/global_subjects/<subject>/spec_production.md` is
    the artifact the matched-rerun used (per `letta_stateful_matched_rerun.md`
    Part 4). For Hamerton, the unified-brief variant is `spec.md` /
    `brief_v5.md` in the same path, which the rerun does not store separately;
    we use `_letta_rerun/hamerton_spec_named.md` if present, else fall back to
    `data/global_subjects/hamerton/spec.md`.
    """
    candidates = []
    if subject == "hamerton":
        candidates = [
            RERUN / "hamerton_spec_named.md",
            REPO / "data" / "hamerton" / "spec" / "brief_v5_clean.md",
            GLOBAL_DATA / subject / "spec.md",
            GLOBAL_DATA / subject / "brief_v5.md",
        ]
    else:
        candidates = [
            RERUN / f"{subject}_spec_named.md",
            GLOBAL_DATA / subject / "spec_production.md",
            GLOBAL_DATA / subject / "spec.md",
        ]
    for p in candidates:
        if p.exists():
            manifest.append(manifest_entry(p))
            return p.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"No BL spec found for {subject}; tried {[str(c) for c in candidates]}"
    )


# ---------- Text analytics: duplication, named entities, n-gram overlap ----------


_SENT_SPLIT_RE = re.compile(r"[.!?]+\s+")


def sentence_duplication_rate(text: str) -> tuple[float, int, int]:
    """Split text into sentences on `[.!?]+\\s+`, lowercase + strip whitespace,
    drop empties shorter than 10 chars, and return (duplication_rate,
    total_sentences, unique_sentences).

    duplication_rate := (total - unique) / total. This matches the paper's
    "25.4% verbatim sentence duplication" claim on Babur. The 10-char floor
    drops fragments like '1' or 'OK'.
    """
    parts = _SENT_SPLIT_RE.split(text)
    sents = [s.strip().lower() for s in parts]
    sents = [s for s in sents if len(s) >= 10]
    total = len(sents)
    if total == 0:
        return 0.0, 0, 0
    unique = len(set(sents))
    return (total - unique) / total, total, unique


_TOKEN_RE = re.compile(r"\b[A-Z][a-zA-Z]+\b")
_STOP_CAP_TOKENS = {
    # Sentence-initial words don't count as named entities. Drop a small
    # whitelist of common English sentence-starts and pronouns capitalized at
    # sentence-initial position. This is a deterministic approximation; the
    # paper's number was computed by hand on the deep-read; we recompute from
    # the block text and document the rule here.
    "The", "This", "That", "These", "Those", "They", "Their", "Them",
    "He", "She", "His", "Her", "Hers", "It", "Its", "We", "Our", "Ours",
    "You", "Your", "Yours", "I", "Me", "My", "Mine",
    "A", "An", "And", "But", "Or", "If", "When", "Where", "Why", "How",
    "What", "Who", "Whom", "Whose", "While", "Although", "Though",
    "After", "Before", "During", "Despite", "Through", "Across",
    "Both", "Either", "Neither", "Each", "Every", "Some", "Any", "No",
    "Not", "So", "Such", "Even", "Only", "Just", "Then", "Now", "Here",
    "There", "Yes", "Also", "However", "Therefore", "Thus", "Hence",
    "First", "Second", "Third", "Last", "Next", "Other", "Another",
    "Despite", "Because", "Since", "Until", "Whether", "As", "By", "For",
    "From", "In", "Into", "On", "Onto", "Out", "Over", "Per", "To", "Up",
    "With", "Within", "Without", "Upon",
    "Recognition", "Understanding", "Acknowledgment",  # markdown bullet labels
    "Person", "Individual",  # paper says BL strips these as anonymizers
}


def unique_named_entities(text: str) -> tuple[int, list[str]]:
    """Count unique capitalized tokens that look like named entities.

    Algorithm:
        - Tokenize on `\\b[A-Z][a-zA-Z]+\\b`.
        - Drop the stop list above (common sentence-initial caps).
        - Drop tokens of length <= 2.
        - Return (unique count, sample of the first 50 sorted entities for
          audit).

    This is deterministic but lossy; it overcounts non-name proper nouns
    (place names, dated months) and undercounts hyphenated entities. The
    paper's Appendix F number was computed by hand; the scaffold value is
    the reproducible reference.
    """
    matches = set()
    for m in _TOKEN_RE.findall(text):
        if len(m) <= 2:
            continue
        if m in _STOP_CAP_TOKENS:
            continue
        matches.add(m)
    sample = sorted(matches)[:50]
    return len(matches), sample


def ngram_overlap_pct(text: str, corpus_text: str, n: int = 5) -> float:
    """Fraction of n-word sequences in `text` that appear verbatim in
    `corpus_text`. Lowercased word tokens; punctuation stripped.
    """
    def toks(s):
        return re.findall(r"[a-z]+", s.lower())

    text_tokens = toks(text)
    corpus_tokens = toks(corpus_text)
    if len(text_tokens) < n or len(corpus_tokens) < n:
        return 0.0
    corpus_grams = set()
    for i in range(len(corpus_tokens) - n + 1):
        corpus_grams.add(tuple(corpus_tokens[i : i + n]))
    text_grams_total = 0
    text_grams_hit = 0
    for i in range(len(text_tokens) - n + 1):
        g = tuple(text_tokens[i : i + n])
        text_grams_total += 1
        if g in corpus_grams:
            text_grams_hit += 1
    if text_grams_total == 0:
        return 0.0
    return 100.0 * text_grams_hit / text_grams_total


# ---------- Build payload ----------


def build_per_subject_block(
    subject: str, manifest: list[dict], data_gaps: list[str]
) -> dict:
    """Compute every claim_id for one subject; return the per-subject block."""
    expected_n = EXPECTED_N_BY_SUBJECT[subject]

    # Branch A: Letta block, 5-judge primary
    letta_qid_scores = gather_per_judge_qid_scores(
        subject, "letta", PRIMARY_PANEL, manifest
    )
    letta_panel_mean, letta_missing, letta_pj_means = cell_mean_methodB_panel(
        letta_qid_scores, PRIMARY_PANEL
    )
    if letta_missing:
        raise RuntimeError(
            f"§4.5 panel coverage gap: subject={subject} branch=letta "
            f"missing judges={letta_missing}"
        )
    letta_methodA, letta_qids = cell_mean_methodA(letta_qid_scores)

    # Branch B: BL unified-brief, 5-judge primary
    blu_qid_scores = gather_per_judge_qid_scores(
        subject, "bl_unified", PRIMARY_PANEL, manifest
    )
    blu_panel_mean, blu_missing, blu_pj_means = cell_mean_methodB_panel(
        blu_qid_scores, PRIMARY_PANEL
    )
    if blu_missing:
        raise RuntimeError(
            f"§4.5 panel coverage gap: subject={subject} branch=bl_unified "
            f"missing judges={blu_missing}"
        )
    blu_methodA, blu_qids = cell_mean_methodA(blu_qid_scores)

    delta_5j = letta_panel_mean - blu_panel_mean

    # 7-judge sensitivity
    letta_qid_scores_7 = gather_per_judge_qid_scores(
        subject, "letta", SENSITIVITY_PANEL, manifest
    )
    letta_7_mean, letta_7_missing, letta_pj7 = cell_mean_methodB_panel(
        letta_qid_scores_7, SENSITIVITY_PANEL
    )
    if letta_7_missing:
        raise RuntimeError(
            f"§4.5 7-judge gap: subject={subject} branch=letta missing={letta_7_missing}"
        )
    blu_qid_scores_7 = gather_per_judge_qid_scores(
        subject, "bl_unified", SENSITIVITY_PANEL, manifest
    )
    blu_7_mean, blu_7_missing, blu_pj7 = cell_mean_methodB_panel(
        blu_qid_scores_7, SENSITIVITY_PANEL
    )
    if blu_7_missing:
        raise RuntimeError(
            f"§4.5 7-judge gap: subject={subject} branch=bl_unified "
            f"missing={blu_7_missing}"
        )
    delta_7j = letta_7_mean - blu_7_mean

    # Branch C: BL full-stack named, 5-judge primary (Letta side reused)
    fs_qid_scores = gather_per_judge_qid_scores(
        subject, "bl_fullstack", PRIMARY_PANEL, manifest
    )
    fs_panel_mean, fs_missing, fs_pj = cell_mean_methodB_panel(
        fs_qid_scores, PRIMARY_PANEL
    )
    if fs_missing:
        raise RuntimeError(
            f"§4.5 fullstack gap: subject={subject} missing={fs_missing}"
        )
    delta_fullstack = letta_panel_mean - fs_panel_mean

    # Block size
    block_chars = load_letta_block_size(subject, manifest)

    # Block text + spec text for content analysis
    block_text = load_letta_block_text(subject, manifest)
    spec_text = load_bl_spec_text(subject, manifest)

    # Named-entity counts
    letta_ne, letta_ne_sample = unique_named_entities(block_text)
    bl_ne, bl_ne_sample = unique_named_entities(spec_text)

    # 5-gram overlap: requires the source corpus, which is not in this repo.
    # Flag as data gap; emit None for these claims.
    letta_5gram_pct = None
    bl_5gram_pct = None
    data_gaps.append(
        f"{subject}: 5-gram corpus overlap not computed; source corpus file "
        f"not present in repo. Would need data/global_subjects/{subject}/"
        f"corpus.txt or equivalent training-half text. Paper claims both "
        f"sides under 1%."
    )

    # Babur duplication rate
    duplication_rate = None
    duplication_total = None
    duplication_unique = None
    if subject == "babur":
        duplication_rate, duplication_total, duplication_unique = (
            sentence_duplication_rate(block_text)
        )

    # Corpus word counts: paper-stated; flagged as data gap.
    corpus_words = PAPER_CLAIMS[subject]["corpus_words"]
    data_gaps.append(
        f"{subject}: corpus word count {corpus_words} is paper-stated only; no "
        f"canonical corpus.txt in this repo. Source: docs/research/"
        f"letta_stateful_matched_rerun.md and inventory CSV row 15. "
        f"Marked NEEDS-corpus-source."
    )

    return {
        "subject": subject,
        "display_name": SUBJECT_DISPLAY[subject],
        "claims": {
            f"4_5_{subject}_letta_block_score_haiku": {
                "value": round(letta_panel_mean, 4),
                "method_A": round(letta_methodA, 4) if letta_methodA is not None else None,
                "method_B": round(letta_panel_mean, 4),
                "estimand": "Mean per-question score for Letta self-edited memory block served to Claude Haiku 4.5, aggregated across 5-judge primary panel",
                "contrast": "Letta block -> Haiku, 5-judge primary panel",
                "filters": {
                    "panel": PRIMARY_PANEL,
                    "condition": [LETTA_CONDITION_BY_SUBJECT[subject]],
                    "subjects": [subject],
                },
                "n": letta_qids,
                "per_judge_means": {k: round(v, 4) for k, v in letta_pj_means.items()},
            },
            f"4_5_{subject}_bl_unified_brief_score_haiku": {
                "value": round(blu_panel_mean, 4),
                "method_A": round(blu_methodA, 4) if blu_methodA is not None else None,
                "method_B": round(blu_panel_mean, 4),
                "estimand": "Mean per-question score for Base Layer unified-brief spec served to Claude Haiku 4.5, aggregated across 5-judge primary panel",
                "contrast": "BL unified brief -> Haiku, 5-judge primary panel",
                "filters": {
                    "panel": PRIMARY_PANEL,
                    "condition": [BL_UNIFIED_CONDITION_BY_SUBJECT[subject]],
                    "subjects": [subject],
                },
                "n": blu_qids,
                "per_judge_means": {k: round(v, 4) for k, v in blu_pj_means.items()},
            },
            f"4_5_{subject}_delta_letta_minus_bl": {
                "value": round(delta_5j, 4),
                "estimand": "Letta panel mean minus BL unified-brief panel mean (5-judge primary)",
                "contrast": "Letta - BL unified, 5-judge primary",
                "filters": {"panel": PRIMARY_PANEL, "subjects": [subject]},
                "n": min(letta_qids, blu_qids),
            },
            f"4_5_{subject}_letta_block_score_haiku_7judge": {
                "value": round(letta_7_mean, 4),
                "estimand": "Letta block panel mean across 7-judge sensitivity panel",
                "contrast": "Letta block -> Haiku, 7-judge sensitivity",
                "filters": {"panel": SENSITIVITY_PANEL, "subjects": [subject]},
                "n": expected_n,
                "per_judge_means": {k: round(v, 4) for k, v in letta_pj7.items()},
            },
            f"4_5_{subject}_bl_unified_brief_score_haiku_7judge": {
                "value": round(blu_7_mean, 4),
                "estimand": "BL unified-brief panel mean across 7-judge sensitivity panel",
                "contrast": "BL unified -> Haiku, 7-judge sensitivity",
                "filters": {"panel": SENSITIVITY_PANEL, "subjects": [subject]},
                "n": expected_n,
                "per_judge_means": {k: round(v, 4) for k, v in blu_pj7.items()},
            },
            f"4_5_{subject}_delta_letta_minus_bl_7judge": {
                "value": round(delta_7j, 4),
                "estimand": "Letta - BL unified delta, 7-judge sensitivity",
                "contrast": "Letta - BL unified, 7-judge sensitivity",
                "filters": {"panel": SENSITIVITY_PANEL, "subjects": [subject]},
                "n": expected_n,
            },
            f"4_5_{subject}_fullstack_bl_score_haiku": {
                "value": round(fs_panel_mean, 4),
                "estimand": "Mean per-question score for BL full-stack named spec, 5-judge primary",
                "contrast": "BL full-stack named -> Haiku, 5-judge primary",
                "filters": {
                    "panel": PRIMARY_PANEL,
                    "condition": [BL_FULLSTACK_CONDITION_BY_SUBJECT[subject]],
                    "subjects": [subject],
                },
                "n": expected_n,
                "per_judge_means": {k: round(v, 4) for k, v in fs_pj.items()},
            },
            f"4_5_{subject}_fullstack_delta_letta_minus_bl": {
                "value": round(delta_fullstack, 4),
                "estimand": "Letta panel mean minus BL full-stack panel mean (5-judge primary)",
                "contrast": "Letta - BL full-stack, 5-judge primary",
                "filters": {"panel": PRIMARY_PANEL, "subjects": [subject]},
                "n": expected_n,
            },
            f"4_5_{subject}_letta_block_chars": {
                "value": int(block_chars),
                "estimand": "Length in characters of the final Letta human memory block",
                "contrast": "Letta block size at end of ingestion",
                "filters": {"subjects": [subject]},
                "n": 1,
            },
            f"4_5_{subject}_corpus_words": {
                "value": int(corpus_words),
                "estimand": "Word count of the training-half source corpus (paper-stated)",
                "contrast": "Source corpus size",
                "filters": {"subjects": [subject]},
                "n": 1,
                "data_gap": "paper-stated; no canonical corpus.txt in repo",
            },
            f"4_5_{subject}_letta_unique_named_entities": {
                "value": int(letta_ne),
                "estimand": "Unique capitalized tokens (excluding sentence-initial stop list) in the Letta block",
                "contrast": "Referential density: Letta block",
                "filters": {"subjects": [subject]},
                "n": 1,
                "algorithm": "regex `\\b[A-Z][a-zA-Z]+\\b`, drop length<=2 and stop list",
                "sample": letta_ne_sample,
            },
            f"4_5_{subject}_bl_unique_named_entities": {
                "value": int(bl_ne),
                "estimand": "Unique capitalized tokens in the BL spec",
                "contrast": "Referential density: BL spec",
                "filters": {"subjects": [subject]},
                "n": 1,
                "algorithm": "regex `\\b[A-Z][a-zA-Z]+\\b`, drop length<=2 and stop list",
                "sample": bl_ne_sample,
            },
            f"4_5_{subject}_letta_5gram_overlap_pct": {
                "value": letta_5gram_pct,
                "estimand": "Percent of 5-word sequences in Letta block found verbatim in source corpus",
                "contrast": "Verbatim corpus overlap: Letta",
                "filters": {"subjects": [subject]},
                "n": 1,
                "data_gap": "Source corpus not in repo; paper claims under 1%",
            },
            f"4_5_{subject}_bl_5gram_overlap_pct": {
                "value": bl_5gram_pct,
                "estimand": "Percent of 5-word sequences in BL spec found verbatim in source corpus",
                "contrast": "Verbatim corpus overlap: BL",
                "filters": {"subjects": [subject]},
                "n": 1,
                "data_gap": "Source corpus not in repo; paper claims 0% on all three",
            },
        },
        "duplication_rate": duplication_rate,
        "duplication_total_sentences": duplication_total,
        "duplication_unique_sentences": duplication_unique,
    }


def build_payload() -> dict:
    manifest: list[dict] = []
    data_gaps: list[str] = []
    subject_blocks = []
    for subject in SUBJECTS:
        subject_blocks.append(build_per_subject_block(subject, manifest, data_gaps))

    # Global claims: Babur duplication, Letta API ceiling
    babur_block = next(b for b in subject_blocks if b["subject"] == "babur")
    duplication = babur_block["duplication_rate"]
    global_claims = {
        "4_5_babur_block_duplication_rate": {
            "value": round(duplication, 4) if duplication is not None else None,
            "estimand": "Fraction of sentences in Babur Letta block that are verbatim duplicates of another sentence in the same block",
            "contrast": "Babur block duplication rate",
            "filters": {"subjects": ["babur"]},
            "n": babur_block["duplication_total_sentences"],
            "algorithm": "split on `[.!?]+\\s+`, lowercase+strip, drop sentences <10 chars; rate = (total - unique) / total",
        },
        "4_5_letta_api_ceiling_approx_chars": {
            "value": 333000,
            "estimand": "Approximate effective character ceiling on Letta API per-message ingestion observed during Babur run (paper-stated; from letta_stateful_matched_rerun.md Part 1)",
            "contrast": "API ingestion ceiling",
            "filters": {"subjects": ["babur"]},
            "n": 1,
            "data_gap": "paper-stated; the empirical observation in matched_rerun.md is 332,585 chars at last successful turn (T220) and 400 errors thereafter; 333,000 is the paper's rounded value.",
        },
    }

    # Aggregate every per-subject claim into a flat top-level dict, plus globals.
    flat_claims: dict[str, dict] = {}
    for block in subject_blocks:
        for cid, cd in block["claims"].items():
            flat_claims[cid] = cd
    flat_claims.update(global_claims)

    # Dedupe manifest by sha256.
    seen = set()
    deduped_manifest = []
    for entry in manifest:
        if entry["sha256"] in seen:
            continue
        seen.add(entry["sha256"])
        deduped_manifest.append(entry)
    deduped_manifest.sort(key=lambda e: e["path"])

    payload = {
        "schema_version": SCHEMA_VERSION,
        "section": "§4.5 + Appendix F",
        "aggregation_rule": "5-judge primary; Method B (per-judge mean -> mean of judge means across {haiku, sonnet, opus, gpt4o, gpt54}). Method A reported as audit; balanced coverage means A==B within FP tolerance.",
        "claims": flat_claims,
        "summary": {
            "subjects": SUBJECTS,
            "n_claims": len(flat_claims),
            "data_gaps": data_gaps,
            "panel_primary": PRIMARY_PANEL,
            "panel_sensitivity": SENSITIVITY_PANEL,
        },
        "provenance": {
            "script": "scripts/_v11_emit_4_5_letta.py",
            "script_version": SCRIPT_VERSION,
            "run_timestamp": EMIT_DATE,
            "input_manifest": deduped_manifest,
        },
    }
    return payload


# ---------- Markdown rendering ----------


def fmt_value(v, digits=3):
    if v is None:
        return "n/a"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v:.{digits}f}"
    if isinstance(v, list):
        if not v:
            return "[]"
        return f"[{len(v)} entries]"
    return str(v)


def compare(scaffold, paper, tol=VERIFY_TOLERANCE):
    if scaffold is None and paper is None:
        return ("MATCH", 0.0)
    if scaffold is None or paper is None:
        return ("MISMATCH(missing)", float("inf"))
    try:
        d = float(scaffold) - float(paper)
    except (TypeError, ValueError):
        return ("MISMATCH(typed)", float("inf"))
    # For integer claims (block sizes, word counts), use absolute tolerance of 1.
    if isinstance(scaffold, int) and isinstance(paper, int):
        if abs(scaffold - paper) <= 1:
            return ("MATCH", abs(scaffold - paper))
        return (f"MISMATCH({d:+})", abs(d))
    if abs(d) <= tol + 1e-9:
        return ("MATCH", abs(d))
    return (f"MISMATCH({d:+.4f})", abs(d))


def paper_value_for(claim_id: str):
    """Return the paper-claimed value for `claim_id`, or None if not asserted."""
    # Per-subject claims
    for subject in SUBJECTS:
        prefix = f"4_5_{subject}_"
        if claim_id.startswith(prefix):
            tail = claim_id[len(prefix):]
            return PAPER_CLAIMS[subject].get(tail)
    if claim_id == "4_5_babur_block_duplication_rate":
        return PAPER_CLAIMS_GLOBAL["babur_block_duplication_rate"]
    if claim_id == "4_5_letta_api_ceiling_approx_chars":
        return PAPER_CLAIMS_GLOBAL["letta_api_ceiling_approx_chars"]
    return None


def render_markdown(payload: dict) -> str:
    lines = []
    lines.append("# v11 emit: §4.5 + Appendix F (Letta stateful-agent comparison)")
    lines.append("")
    lines.append(f"_Generated by `scripts/_v11_emit_4_5_letta.py` (timestamp: {EMIT_DATE})_")
    lines.append("")
    lines.append("Aggregation: " + payload["aggregation_rule"])
    lines.append("")
    lines.append("Panels:")
    lines.append("- 5-judge primary: " + ", ".join(PRIMARY_PANEL))
    lines.append("- 7-judge sensitivity: " + ", ".join(SENSITIVITY_PANEL))
    lines.append("")
    lines.append("## Side-by-side scaffold vs paper §4.5 / Appendix F")
    lines.append("")
    lines.append("| claim_id | scaffold | paper | verify |")
    lines.append("|---|---:|---:|:--|")

    n_match = 0
    n_total = 0
    for cid, cdata in payload["claims"].items():
        scaffold = cdata.get("value")
        paper = paper_value_for(cid)
        if paper is None:
            verify = "N/A (paper-silent)"
        else:
            status, _ = compare(scaffold, paper)
            verify = status
            if status == "MATCH":
                n_match += 1
            n_total += 1
        lines.append(
            f"| `{cid}` | {fmt_value(scaffold)} | {fmt_value(paper)} | {verify} |"
        )

    lines.append("")
    lines.append(
        f"**Verify roll-up:** {n_match}/{n_total} paper-asserted claims MATCH "
        f"within tolerance ({VERIFY_TOLERANCE} for floats, integer-equal for "
        f"counts)."
    )

    sm = payload["summary"]
    if sm["data_gaps"]:
        lines.append("")
        lines.append("## Data gaps")
        lines.append("")
        for g in sm["data_gaps"]:
            lines.append(f"- {g}")

    lines.append("")
    lines.append("## Provenance manifest")
    lines.append("")
    lines.append("| path | sha256 (12) | size_bytes | n_records |")
    lines.append("|---|---|---:|---:|")
    for e in payload["provenance"]["input_manifest"]:
        sh = e["sha256"][:12]
        nr = e.get("n_records")
        lines.append(
            f"| `{e['path']}` | `{sh}` | {e['size_bytes']} | {nr if nr is not None else '-'} |"
        )
    lines.append("")
    lines.append(f"Script: `{payload['provenance']['script']}` v{SCRIPT_VERSION}")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------- Atomic write ----------


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# ---------- Verify ----------


def run_verify(payload: dict, verbose: bool = True) -> bool:
    diffs = []
    for cid, cdata in payload["claims"].items():
        scaffold = cdata.get("value")
        paper = paper_value_for(cid)
        if paper is None:
            continue
        status, _ = compare(scaffold, paper)
        diffs.append((cid, scaffold, paper, status))

    n_match = sum(1 for d in diffs if d[3] == "MATCH")
    n_total = len(diffs)

    if verbose:
        print()
        print("=" * 78)
        print(
            f"VERIFY (§4.5 + Appendix F): {n_match}/{n_total} claims MATCH "
            f"within tolerance"
        )
        print("=" * 78)
        for cid, scaffold, paper, status in diffs:
            if status != "MATCH":
                print(
                    f"  {cid:50s} scaffold={fmt_value(scaffold):>10} "
                    f"paper={fmt_value(paper):>10} -> {status}"
                )
    return n_match == n_total


# ---------- Main ----------


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--verify",
        action="store_true",
        help="After emit, compare every value against §4.5 / Appendix F paper claims; exit 1 on mismatch.",
    )
    args = parser.parse_args()

    payload = build_payload()

    json_text = json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False)
    atomic_write(OUT_JSON, json_text + "\n")

    md_text = render_markdown(payload)
    atomic_write(OUT_MD, md_text)

    print("Section 4.5 + Appendix F Letta emit (5-judge primary panel)")
    print("-" * 78)
    for subject in SUBJECTS:
        letta_id = f"4_5_{subject}_letta_block_score_haiku"
        bl_id = f"4_5_{subject}_bl_unified_brief_score_haiku"
        d_id = f"4_5_{subject}_delta_letta_minus_bl"
        d7_id = f"4_5_{subject}_delta_letta_minus_bl_7judge"
        fs_id = f"4_5_{subject}_fullstack_delta_letta_minus_bl"
        sz_id = f"4_5_{subject}_letta_block_chars"
        ne_l = f"4_5_{subject}_letta_unique_named_entities"
        ne_b = f"4_5_{subject}_bl_unique_named_entities"

        def cv(cid):
            return payload["claims"][cid]["value"]

        print(
            f"  {SUBJECT_DISPLAY[subject]:9s}  "
            f"Letta={cv(letta_id):.3f}  BL={cv(bl_id):.3f}  d5={cv(d_id):+.3f}  "
            f"d7={cv(d7_id):+.3f}  d_fullstack={cv(fs_id):+.3f}  "
            f"block={cv(sz_id):>7d}  ne(L/B)={cv(ne_l)}/{cv(ne_b)}"
        )

    babur_dup = payload["claims"]["4_5_babur_block_duplication_rate"]["value"]
    print(f"\n  Babur duplication rate: {babur_dup:.4f} (paper says 0.254)")

    print()
    print(f"JSON: {OUT_JSON}")
    print(f"MD:   {OUT_MD}")

    if args.verify:
        ok = run_verify(payload, verbose=True)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
