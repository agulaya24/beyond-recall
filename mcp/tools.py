"""Tool implementations for the Beyond Recall study MCP server.

Plain typed Python functions; no MCP imports. The server module wraps these
in FastMCP tool decorators. Smoke tests import these directly.

All file reads use encoding="utf-8". SQLite is opened read-only via URI mode.
ChromaDB is used in read-only fashion (no add/upsert/delete calls).
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Literal, Optional

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
WORKSPACE = REPO / "workspace"
DB_PATH = WORKSPACE / "study_knowledge.db"
VEC_PATH = WORKSPACE / "study_vectors"
RESULTS_DIR = REPO / "results"
DOCS_DIR = REPO / "docs"

# Canonical paper draft
PAPER_PATH = DOCS_DIR / "beyond_recall_v12_1_draft.md"
# Provenance and reference docs
PROVENANCE_PATH = DOCS_DIR / "PROVENANCE_INDEX.md"
DATA_REFERENCE_PATH = DOCS_DIR / "DATA_REFERENCE.md"

# Anchor crossing data sources
ANCHOR_RATES_PATH = DOCS_DIR / "research" / "multi_anchor_rates_all_pairs_20260430.json"
ANCHOR_S114_EXAMPLES_PATH = DOCS_DIR / "research" / "s114_anchor_crossing_examples.json"
PER_QUESTION_EXTENDED_PATH = (
    DOCS_DIR / "research" / "per_question_anchor_crossing_extended_20260428.json"
)

# 5-judge primary panel and full sensitivity panel
PRIMARY_JUDGES = ("haiku", "sonnet", "opus", "gpt4o", "gpt54")
SENSITIVITY_JUDGES = (
    "haiku", "sonnet", "opus", "gpt4o", "gpt54", "gemini_flash", "gemini_pro",
)

# 14 main-study subjects with v10.1 / v11 canonical 5-judge primary numbers.
# Source: docs/DATA_REFERENCE.md §1 and PROVENANCE_INDEX.md V10.1 table.
# Hardcoded because table changes ~once per release; runtime parsing is brittle.
MAIN_STUDY_SUBJECTS: list[dict[str, Any]] = [
    {"subject": "ebers",        "dir": "global_ebers",        "c5": 1.02, "c4a": 2.07, "delta_spec": 1.05},
    {"subject": "sunity_devee", "dir": "global_sunity_devee", "c5": 1.03, "c4a": 2.41, "delta_spec": 1.38},
    {"subject": "hamerton",     "dir": "hamerton",            "c5": 1.26, "c4a": 2.77, "delta_spec": 1.51},
    {"subject": "fukuzawa",     "dir": "global_fukuzawa",     "c5": 1.67, "c4a": 2.78, "delta_spec": 1.11},
    {"subject": "bernal_diaz",  "dir": "global_bernal_diaz",  "c5": 1.70, "c4a": 2.48, "delta_spec": 0.78},
    {"subject": "babur",        "dir": "global_babur",        "c5": 1.76, "c4a": 2.01, "delta_spec": 0.25},
    {"subject": "seacole",      "dir": "global_seacole",      "c5": 1.77, "c4a": 2.59, "delta_spec": 0.82},
    {"subject": "keckley",      "dir": "global_keckley",      "c5": 1.84, "c4a": 2.44, "delta_spec": 0.59},
    {"subject": "yung_wing",    "dir": "global_yung_wing",    "c5": 1.88, "c4a": 2.40, "delta_spec": 0.52},
    {"subject": "zitkala_sa",   "dir": "global_zitkala_sa",   "c5": 2.34, "c4a": 2.02, "delta_spec": -0.32},
    {"subject": "cellini",      "dir": "global_cellini",      "c5": 2.38, "c4a": 2.53, "delta_spec": 0.15},
    {"subject": "rousseau",     "dir": "global_rousseau",     "c5": 2.44, "c4a": 2.53, "delta_spec": 0.10},
    {"subject": "augustine",    "dir": "global_augustine",    "c5": 2.58, "c4a": 2.70, "delta_spec": 0.11},
    {"subject": "equiano",      "dir": "global_equiano",      "c5": 2.77, "c4a": 2.42, "delta_spec": -0.35},
]

# Condition aliasing. User-facing canonical names map to a list of dataset
# variants seen in judgment files (globals vs. hamerton differ).
CONDITION_VARIANTS: dict[str, tuple[str, ...]] = {
    "C5":  ("C5_baseline",),
    "C2a": ("C2a_full_spec", "C2a_spec"),
    "C2c": ("C2c_wrong_spec", "C2c_full_wrong_spec"),
    "C4":  ("C4_factdump", "C4_full_facts"),
    "C4a": ("C4a_full_facts_plus_spec", "C4a_full_all_facts_plus_spec"),
    "C8":  ("C8_full_corpus", "C8_corpus"),
    "C9":  ("C9_full_corpus_plus_spec", "C9_corpus_plus_spec"),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _connect_ro(path: Path) -> sqlite3.Connection:
    """Open SQLite read-only via URI mode."""
    uri = f"file:{path.as_posix()}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _load_json(path: Path) -> Any:
    """Load a UTF-8 JSON file. Raises FileNotFoundError if missing."""
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_condition(condition: str) -> Optional[str]:
    """Map a user-facing condition string to its canonical short form (C5, C4a, etc.).

    Accepts short forms ("C5"), full long forms ("C5_baseline"), and case variants.
    Returns None if not recognized.
    """
    if not condition:
        return None
    s = condition.strip()
    # Short form match: C\d+[a-z]? at start. Letter suffix stays lowercase.
    m = re.match(r"^(C)(\d+)([a-z])?", s, flags=re.IGNORECASE)
    if not m:
        return None
    short = "C" + m.group(2) + (m.group(3).lower() if m.group(3) else "")
    if short in CONDITION_VARIANTS:
        return short
    return None


def _resolve_subject(subject: str) -> tuple[Optional[str], Optional[str], list[str]]:
    """Resolve a user-supplied subject string to (canonical_name, dir_name, alternatives).

    Accepts both directory names ("global_seacole", "hamerton") and short
    forms ("seacole"). Returns (None, None, alternatives) on miss.
    """
    if not subject:
        return None, None, [s["subject"] for s in MAIN_STUDY_SUBJECTS]
    s = subject.strip().lower()
    by_subject = {row["subject"]: row for row in MAIN_STUDY_SUBJECTS}
    by_dir = {row["dir"]: row for row in MAIN_STUDY_SUBJECTS}
    if s in by_subject:
        row = by_subject[s]
        return row["subject"], row["dir"], []
    if s in by_dir:
        row = by_dir[s]
        return row["subject"], row["dir"], []
    # Strip "global_" prefix if user typed it inconsistently
    if s.startswith("global_") and s[7:] in by_subject:
        row = by_subject[s[7:]]
        return row["subject"], row["dir"], []
    # Fuzzy fallback: substring match
    matches = [row["subject"] for row in MAIN_STUDY_SUBJECTS if s in row["subject"]]
    return None, None, matches or [row["subject"] for row in MAIN_STUDY_SUBJECTS]


# ---------------------------------------------------------------------------
# Per-judge row loaders (handle the schema heterogeneity)
# ---------------------------------------------------------------------------

def _iter_rows_long(records: Iterable[dict], judge: str) -> Iterable[tuple[int, str, float]]:
    """Long-format rows: {qid, condition, judge, score}."""
    for r in records:
        if not isinstance(r, dict):
            continue
        if r.get("judge") != judge:
            continue
        qid = r.get("question_id")
        cond = r.get("condition")
        score = r.get("score")
        if qid is None or cond is None or score is None:
            continue
        if r.get("parse_failure"):
            continue
        yield int(qid), str(cond), float(score)


def _iter_rows_wide(records: Iterable[dict], judge: str) -> Iterable[tuple[int, str, float]]:
    """Wide-format rows: {qid, condition, <judge>_score}.

    Hamerton's judgments.json (haiku + gemini wide), gpt54_judgments.json,
    and similar use this form.
    """
    score_key = f"{judge}_score"
    for r in records:
        if not isinstance(r, dict):
            continue
        if score_key not in r:
            continue
        qid = r.get("question_id")
        cond = r.get("condition")
        score = r.get(score_key)
        if qid is None or cond is None or score is None:
            continue
        yield int(qid), str(cond), float(score)


def _judge_rows_for_subject(
    subject_dir: str, judge: str
) -> list[tuple[int, str, float]]:
    """Return (qid, condition, score) rows for a subject/judge.

    Searches the subject directory for files plausibly containing this judge's
    scores, in long or wide format, and concatenates. De-duplicates on
    (qid, condition).
    """
    subj_path = RESULTS_DIR / subject_dir
    if not subj_path.exists():
        return []

    out: dict[tuple[int, str], float] = {}

    # Candidate files in priority order. judgments_v2.json (globals) is long
    # and contains all judges. Per-judge files supplement. Hamerton's C5/C4
    # rows live in judgments_harmonized.json.
    candidates = [
        subj_path / "judgments_v2.json",
        subj_path / "judgments.json",
        subj_path / "judgments_harmonized.json",
        subj_path / f"{judge}_judgments.json",
    ]
    seen_files: set[Path] = set()
    for p in candidates:
        if p in seen_files or not p.exists():
            continue
        seen_files.add(p)
        try:
            data = _load_json(p)
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, list):
            continue
        # Try long format first, then wide.
        long_rows = list(_iter_rows_long(data, judge))
        wide_rows = list(_iter_rows_wide(data, judge))
        for qid, cond, score in (*long_rows, *wide_rows):
            out[(qid, cond)] = score

    return [(qid, cond, score) for (qid, cond), score in out.items()]


def _aggregate_score(
    rows_by_judge: dict[str, list[tuple[int, str, float]]],
    canonical_condition: str,
) -> dict[str, Any]:
    """Aggregate per-judge per-question rows into a within-judge mean across
    questions, then mean across judges. Honors locked rule from §3.6.5.

    Returns a dict with mean, n_questions, per_judge breakdown, and condition
    variant matched.
    """
    variants = CONDITION_VARIANTS.get(canonical_condition, ())
    matched_variant: Optional[str] = None

    per_judge: dict[str, dict[str, Any]] = {}
    qid_set: set[int] = set()

    for judge, rows in rows_by_judge.items():
        scores: list[float] = []
        for qid, cond, score in rows:
            if cond not in variants:
                continue
            if matched_variant is None:
                matched_variant = cond
            scores.append(score)
            qid_set.add(qid)
        if scores:
            per_judge[judge] = {
                "judge": judge,
                "mean": round(sum(scores) / len(scores), 4),
                "n": len(scores),
            }

    judge_means = [pj["mean"] for pj in per_judge.values()]
    overall_mean = (
        round(sum(judge_means) / len(judge_means), 4) if judge_means else None
    )

    return {
        "mean": overall_mean,
        "n_questions": len(qid_set),
        "n_judges": len(per_judge),
        "per_judge": per_judge,
        "condition_variant": matched_variant,
    }


# ---------------------------------------------------------------------------
# Tool: search_study
# ---------------------------------------------------------------------------

def search_study(
    query: str,
    mode: Literal["fts", "semantic", "both"] = "both",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search the study knowledge index built by scripts/index_study_repo.py.

    mode="fts" runs SQLite FTS5; mode="semantic" runs ChromaDB nearest-neighbor;
    mode="both" runs both and returns interleaved results tagged with their mode.
    """
    if not query or not query.strip():
        return [{"error": "query must not be empty"}]
    limit = max(1, min(int(limit), 50))

    results: list[dict[str, Any]] = []

    if mode in ("fts", "both"):
        results.extend(_fts_search(query, limit))

    if mode in ("semantic", "both"):
        results.extend(_semantic_search(query, limit))

    return results


def _fts_search(query: str, limit: int) -> list[dict[str, Any]]:
    """SQLite FTS5 search over chunks_fts."""
    if not DB_PATH.exists():
        return [{"error": f"index not found at {DB_PATH}", "mode": "fts"}]
    out: list[dict[str, Any]] = []
    try:
        with _connect_ro(DB_PATH) as c:
            rows = c.execute(
                """
                SELECT
                    chunks.id,
                    chunks.scope,
                    chunks.label,
                    files.filename,
                    files.path,
                    snippet(chunks_fts, 0, '[', ']', '...', 32),
                    rank
                FROM chunks_fts
                JOIN chunks ON chunks.id = chunks_fts.rowid
                JOIN files ON chunks.file_id = files.id
                WHERE chunks_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()
        for chunk_id, scope, label, fname, fpath, snip, rank in rows:
            out.append({
                "mode": "fts",
                "chunk_id": chunk_id,
                "scope": scope,
                "label": label,
                "file_path": fpath,
                "filename": fname,
                "content_preview": (snip or "")[:400],
                "score": float(rank) if rank is not None else None,
            })
    except sqlite3.OperationalError as e:
        # Likely an FTS5 query syntax error from user input.
        out.append({"mode": "fts", "error": f"FTS query error: {e}"})
    return out


def _semantic_search(query: str, limit: int) -> list[dict[str, Any]]:
    """ChromaDB semantic search over the 'study' collection."""
    if not VEC_PATH.exists():
        return [{"error": f"vector index not found at {VEC_PATH}", "mode": "semantic"}]
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
    except ImportError as e:
        return [{"mode": "semantic", "error": f"semantic deps missing: {e}"}]

    try:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        client = chromadb.PersistentClient(path=str(VEC_PATH))
        col = client.get_collection("study")
    except Exception as e:
        return [{"mode": "semantic", "error": f"vector store unavailable: {e}"}]

    emb = model.encode([query]).tolist()
    res = col.query(query_embeddings=emb, n_results=limit)
    out: list[dict[str, Any]] = []
    for i in range(len(res.get("ids", [[]])[0])):
        meta = res["metadatas"][0][i] or {}
        doc = res["documents"][0][i] or ""
        dist = (
            res["distances"][0][i]
            if res.get("distances") and res["distances"][0]
            else None
        )
        out.append({
            "mode": "semantic",
            "chunk_id": int(res["ids"][0][i]) if res["ids"][0][i].isdigit() else res["ids"][0][i],
            "scope": meta.get("scope"),
            "label": meta.get("label"),
            "file_path": None,
            "filename": None,
            "content_preview": doc[:400],
            "score": float(dist) if dist is not None else None,
        })
    return out


# ---------------------------------------------------------------------------
# Tool: get_subject_score
# ---------------------------------------------------------------------------

def get_subject_score(
    subject: str,
    condition: str,
    panel: Literal["5-judge-primary", "7-judge-sensitivity"] = "5-judge-primary",
) -> dict[str, Any]:
    """Recompute the per-judge mean score for a subject and condition.

    Aggregation: within-judge mean across questions, then mean across panel
    judges (locked rule from paper §3.6.5).
    """
    canonical_subject, subj_dir, alternatives = _resolve_subject(subject)
    if not canonical_subject:
        return {
            "error": f"subject not found: {subject!r}",
            "alternatives": alternatives,
        }

    canonical_cond = _normalize_condition(condition)
    if not canonical_cond:
        return {
            "error": f"unrecognized condition: {condition!r}",
            "supported": list(CONDITION_VARIANTS.keys()),
        }

    judges = (
        PRIMARY_JUDGES if panel == "5-judge-primary"
        else SENSITIVITY_JUDGES if panel == "7-judge-sensitivity"
        else PRIMARY_JUDGES
    )

    rows_by_judge: dict[str, list[tuple[int, str, float]]] = {}
    for j in judges:
        rs = _judge_rows_for_subject(subj_dir, j)
        if rs:
            rows_by_judge[j] = rs

    agg = _aggregate_score(rows_by_judge, canonical_cond)
    if agg["n_judges"] == 0:
        return {
            "subject": canonical_subject,
            "subject_dir": subj_dir,
            "condition": canonical_cond,
            "panel": panel,
            "error": "no judgment rows found for this (subject, condition, panel)",
        }

    return {
        "subject": canonical_subject,
        "subject_dir": subj_dir,
        "condition": canonical_cond,
        "condition_variant_used": agg["condition_variant"],
        "panel": panel,
        "panel_judges_expected": list(judges),
        "panel_judges_found": list(agg["per_judge"].keys()),
        "mean": agg["mean"],
        "n_questions": agg["n_questions"],
        "per_judge": agg["per_judge"],
        "source_dir": str(RESULTS_DIR / subj_dir),
        "aggregation_rule": "within-judge mean across questions, then mean across panel judges (paper §3.6.5)",
    }


# ---------------------------------------------------------------------------
# Tool: list_subjects
# ---------------------------------------------------------------------------

def list_subjects() -> list[dict[str, Any]]:
    """Return the 14 main-study subjects with C5 baseline, Δ_spec (C4a-C5),
    canonical C4a, and the data directory path.

    Source values are 5-judge primary canonical from DATA_REFERENCE.md §1.
    Hardcoded because the table changes ~once per release.
    """
    out: list[dict[str, Any]] = []
    for row in MAIN_STUDY_SUBJECTS:
        if row["dir"] == "hamerton":
            data_dir = REPO / "data" / "hamerton"
        else:
            data_dir = REPO / "data" / "global_subjects" / row["subject"]
        out.append({
            "subject": row["subject"],
            "results_dir": str(RESULTS_DIR / row["dir"]),
            "data_dir": str(data_dir),
            "c5_baseline": row["c5"],
            "c4a_facts_plus_spec": row["c4a"],
            "delta_spec": row["delta_spec"],
            "low_baseline": row["c5"] <= 2.0,
        })
    return out


# ---------------------------------------------------------------------------
# Tool: get_provenance
# ---------------------------------------------------------------------------

def get_provenance(claim: str, limit: int = 8) -> list[dict[str, Any]]:
    """Search PROVENANCE_INDEX.md and DATA_REFERENCE.md for sections matching
    the supplied claim. Returns file pointers and section labels.
    """
    if not claim or not claim.strip():
        return [{"error": "claim must not be empty"}]
    limit = max(1, min(int(limit), 25))

    target_filenames = {"PROVENANCE_INDEX.md", "DATA_REFERENCE.md"}
    out: list[dict[str, Any]] = []

    # Try semantic search first, filter by filename.
    if VEC_PATH.exists():
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb

            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            client = chromadb.PersistentClient(path=str(VEC_PATH))
            col = client.get_collection("study")
            emb = model.encode([claim]).tolist()
            # Pull more than limit to allow filename post-filter
            res = col.query(query_embeddings=emb, n_results=limit * 6)
            ids = res.get("ids", [[]])[0]
            for i, chunk_id in enumerate(ids):
                meta = res["metadatas"][0][i] or {}
                # Resolve filename + path via SQLite
                fname, fpath = _filename_for_chunk(chunk_id)
                if fname in target_filenames:
                    doc = res["documents"][0][i] or ""
                    out.append({
                        "mode": "semantic",
                        "filename": fname,
                        "file_path": fpath,
                        "section_label": meta.get("label"),
                        "content_preview": doc[:500],
                    })
                if len(out) >= limit:
                    break
        except Exception as e:
            out.append({"mode": "semantic", "error": f"semantic unavailable: {e}"})

    # FTS fallback / supplement, scoped to the two target files.
    if len(out) < limit and DB_PATH.exists():
        try:
            with _connect_ro(DB_PATH) as c:
                placeholders = ",".join("?" * len(target_filenames))
                rows = c.execute(
                    f"""
                    SELECT chunks.id, chunks.label, files.filename, files.path,
                           snippet(chunks_fts, 0, '[', ']', '...', 32)
                    FROM chunks_fts
                    JOIN chunks ON chunks.id = chunks_fts.rowid
                    JOIN files  ON chunks.file_id = files.id
                    WHERE chunks_fts MATCH ?
                      AND files.filename IN ({placeholders})
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (claim, *target_filenames, limit),
                ).fetchall()
            for chunk_id, label, fname, fpath, snip in rows:
                out.append({
                    "mode": "fts",
                    "filename": fname,
                    "file_path": fpath,
                    "section_label": label,
                    "content_preview": (snip or "")[:500],
                })
        except sqlite3.OperationalError as e:
            out.append({"mode": "fts", "error": f"FTS query error: {e}"})

    return out[:limit]


def _filename_for_chunk(chunk_id: Any) -> tuple[Optional[str], Optional[str]]:
    """Return (filename, path) for a chunk_id from the SQLite index, or (None, None)."""
    if not DB_PATH.exists():
        return None, None
    try:
        cid = int(chunk_id)
    except (ValueError, TypeError):
        return None, None
    try:
        with _connect_ro(DB_PATH) as c:
            row = c.execute(
                """
                SELECT files.filename, files.path
                FROM chunks JOIN files ON chunks.file_id = files.id
                WHERE chunks.id = ?
                """,
                (cid,),
            ).fetchone()
    except sqlite3.OperationalError:
        return None, None
    return (row[0], row[1]) if row else (None, None)


# ---------------------------------------------------------------------------
# Tool: list_anchor_crossings
# ---------------------------------------------------------------------------

def list_anchor_crossings(
    condition_pair: str = "C5_to_C4a",
    min_jump: int = 2,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Return per-question multi-anchor crossings for a condition pair.

    Reads from multi_anchor_rates_all_pairs_20260430.json (8 pairs with
    multi_anchor_examples) and supplements with s114_anchor_crossing_examples.json
    for C5_to_C4a (extreme jumps with held-out passage text).

    Returns rows with subject, qid, pre_band, post_band, pre_mean, post_mean, jump.
    For C5_to_C4a, also includes question_text and held_out where available.
    """
    if not condition_pair:
        return [{"error": "condition_pair required (e.g. 'C5_to_C4a')"}]
    limit = max(1, min(int(limit), 200))

    data: dict[str, Any] = {}
    if ANCHOR_RATES_PATH.exists():
        try:
            data = _load_json(ANCHOR_RATES_PATH)
        except (json.JSONDecodeError, OSError) as e:
            return [{"error": f"failed to load {ANCHOR_RATES_PATH.name}: {e}"}]

    pairs = data.get("pairs", {})
    if condition_pair not in pairs:
        return [{
            "error": f"condition_pair {condition_pair!r} not found",
            "available": list(pairs.keys()),
        }]

    examples = pairs[condition_pair].get("multi_anchor_examples") or []
    out: list[dict[str, Any]] = []
    for ex in examples:
        jump = ex.get("jump")
        if jump is None or abs(jump) < min_jump:
            continue
        out.append({
            "condition_pair": condition_pair,
            "subject": ex.get("subject"),
            "qid": ex.get("qid"),
            "pre_band": ex.get("pre_band"),
            "post_band": ex.get("post_band"),
            "pre_mean": ex.get("pre_mean"),
            "post_mean": ex.get("post_mean"),
            "jump": jump,
            "source_file": str(ANCHOR_RATES_PATH),
        })

    # Enrich C5_to_C4a rows with question_text + held_out where present.
    if condition_pair == "C5_to_C4a" and ANCHOR_S114_EXAMPLES_PATH.exists():
        try:
            s114 = _load_json(ANCHOR_S114_EXAMPLES_PATH)
        except (json.JSONDecodeError, OSError):
            s114 = []
        if isinstance(s114, list):
            keyed = {(r.get("subject"), r.get("question_id")): r for r in s114 if isinstance(r, dict)}
            for row in out:
                k = (row["subject"], row["qid"])
                if k in keyed:
                    row["question_text"] = keyed[k].get("question_text")
                    row["held_out"] = keyed[k].get("held_out")
                    row["s114_jump"] = keyed[k].get("jump")

    out.sort(key=lambda r: (-(r.get("jump") or 0), r.get("subject") or ""))
    return out[:limit]


# ---------------------------------------------------------------------------
# Paper section index (used by resources.py)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")


def list_paper_sections() -> list[dict[str, Any]]:
    """Parse the canonical paper draft for section index entries.

    Returns rows: {id, level, title, line_start, line_end}. Section IDs are the
    leading numeric token of the title where present (e.g. '3.6.2'); otherwise
    a slug derived from the title.
    """
    if not PAPER_PATH.exists():
        return []
    text = PAPER_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections: list[dict[str, Any]] = []
    for i, line in enumerate(lines, start=1):
        m = _HEADING_RE.match(line)
        if not m:
            continue
        hashes, title = m.group(1), m.group(2)
        sec_id = _extract_section_id(title)
        sections.append({
            "id": sec_id,
            "level": len(hashes),
            "title": title.strip(),
            "line_start": i,
            "line_end": None,
        })
    # Set line_end as the line before the next heading at <= level
    for idx, sec in enumerate(sections):
        end_line = len(lines)
        for nxt in sections[idx + 1:]:
            if nxt["level"] <= sec["level"]:
                end_line = nxt["line_start"] - 1
                break
        sec["line_end"] = end_line
    return sections


def _extract_section_id(title: str) -> str:
    m = re.match(r"^(\d+(?:\.\d+){0,3})\s+", title)
    if m:
        return m.group(1)
    # Fallback to slug
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "section"


def get_paper_section(section_id: str) -> dict[str, Any]:
    """Return the text of a paper section identified by its numeric id (e.g. '3.6.2')
    or its slug.
    """
    sections = list_paper_sections()
    if not sections:
        return {"error": f"paper draft not found at {PAPER_PATH}"}
    target = section_id.strip()
    sec = next((s for s in sections if s["id"] == target), None)
    if sec is None:
        # Try case-insensitive match on slug
        sec = next((s for s in sections if s["id"].lower() == target.lower()), None)
    if sec is None:
        return {
            "error": f"section {section_id!r} not found",
            "available_ids": [s["id"] for s in sections][:50],
        }
    text = PAPER_PATH.read_text(encoding="utf-8").splitlines()
    body = "\n".join(text[sec["line_start"] - 1: sec["line_end"]])
    return {
        "id": sec["id"],
        "title": sec["title"],
        "level": sec["level"],
        "line_start": sec["line_start"],
        "line_end": sec["line_end"],
        "file_path": str(PAPER_PATH),
        "text": body,
    }
