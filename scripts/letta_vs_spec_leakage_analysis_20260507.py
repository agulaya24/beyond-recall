"""Per-question texture-leakage analysis: Letta block vs Base Layer Spec.

Companion analysis to §4.5 / Appendix G of beyond_recall_v11_8_draft.md.

For each (subject, question_id) in the §4.5 case study (Hamerton qid 21-60,
Ebers qid 1-40, Babur qid 1-40), compute:

  - 5-judge primary panel mean for Letta-block-direct condition
  - 5-judge primary panel mean for BL-Spec-unified-brief condition
  - Score delta (Letta − Spec)
  - Cosine similarity (MiniLM-L6-v2, mean-pooled-by-sentence) between:
      cos_letta_heldout : Letta response vs held-out ground-truth passage
      cos_spec_heldout  : BL Spec response vs held-out ground-truth passage
      cos_letta_spec    : Letta response vs BL Spec response

Drop rule: keep a (subject, qid) only if at least one of the 5 primary judges
returned a valid (parse_failure=False) score on BOTH conditions.

Outputs:
  docs/research/letta_vs_spec_per_question_scores_20260507.csv
  docs/research/letta_vs_spec_leakage_analysis_20260507.md
"""
from __future__ import annotations

import csv
import json
import os
import re
import statistics
import sys
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

# ---------- Paths (mirrors _v11_emit_4_5_letta.py path resolution) ----------

REPO = Path(__file__).resolve().parents[1]
RERUN = REPO / "docs" / "research" / "_letta_rerun"
OUT_DIR = REPO / "docs" / "research"
CSV_OUT = OUT_DIR / "letta_vs_spec_per_question_scores_20260507.csv"
MD_OUT = OUT_DIR / "letta_vs_spec_leakage_analysis_20260507.md"

# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MEMORY_RESULTS = Path(os.environ.get("MEMORY_SYSTEM_ROOT", "")) / "data" / "experiments" / "memory_systems" / "results"
MEMORY_PATH_BY_SUBJECT = {
    "hamerton": MEMORY_RESULTS / "run_fullstack_hamerton_20260411_231237",
    "ebers": MEMORY_RESULTS / "global_ebers",
    "babur": MEMORY_RESULTS / "global_babur",
}

PRIMARY_PANEL = ["haiku", "sonnet", "opus", "gpt4o", "gpt54"]
SUBJECTS = ["hamerton", "ebers", "babur"]
SUBJECT_DISPLAY = {"hamerton": "Hamerton", "ebers": "Ebers", "babur": "Babur"}

LETTA_CONDITION_BY_SUBJECT = {
    "hamerton": "C_letta_memory_haiku",
    "ebers": "C_letta_memory_haiku_ebers",
    "babur": "C_letta_memory_haiku_babur",
}
BL_UNIFIED_CONDITION_BY_SUBJECT = {
    "hamerton": "C2a_full_spec",
    "ebers": "BL_C2a_named_ebers",
    "babur": "BL_C2a_named_babur",
}

# ---------- Loaders ----------


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def letta_block_judgment_path(subject: str, judge: str) -> Path:
    base = MEMORY_PATH_BY_SUBJECT[subject]
    return base / f"letta_memory_haiku_judgments_{judge}.json"


def bl_unified_judgment_path(subject: str, judge: str) -> Path:
    """Schema-variant path resolution; matches _v11_emit_4_5_letta.py."""
    if subject == "hamerton":
        if judge == "haiku":
            # Wide-format legacy file under run_fullstack/analysis/judgments.json
            return MEMORY_PATH_BY_SUBJECT[subject] / "analysis" / "judgments.json"
        # sonnet, opus, gpt4o, gpt54: long-format in _letta_rerun
        return RERUN / f"hamerton_bl_c2a_judgments_{judge}.json"
    return RERUN / f"{subject}_judgments_{judge}.json"


def load_letta_block_per_qid_score(subject: str, judge: str) -> dict[int, float]:
    """Return {qid: score} for Letta-block-direct condition, dropping parse_failure."""
    path = letta_block_judgment_path(subject, judge)
    rows = load_json(path)
    cond = LETTA_CONDITION_BY_SUBJECT[subject]
    out = {}
    for r in rows:
        if r.get("condition") != cond:
            continue
        if r.get("judge") != judge:
            continue
        if r.get("parse_failure"):
            continue
        score = r.get("score")
        if score is None:
            continue
        try:
            sf = float(score)
        except (TypeError, ValueError):
            continue
        if not (1.0 <= sf <= 5.0):
            continue
        out[int(r["question_id"])] = sf
    return out


def load_bl_unified_per_qid_score(subject: str, judge: str) -> dict[int, float]:
    """Return {qid: score} for BL unified-brief condition, dropping parse_failure."""
    path = bl_unified_judgment_path(subject, judge)
    if subject == "hamerton" and judge == "haiku":
        # Wide-format: rows have haiku_score directly; condition key C2a_full_spec.
        rows = load_json(path)
        out = {}
        for r in rows:
            if r.get("condition") != "C2a_full_spec":
                continue
            score = r.get("haiku_score")
            if score is None or score == 0:
                continue
            try:
                sf = float(score)
            except (TypeError, ValueError):
                continue
            if not (1.0 <= sf <= 5.0):
                continue
            out[int(r["question_id"])] = sf
        return out
    # Long-format
    rows = load_json(path)
    cond = BL_UNIFIED_CONDITION_BY_SUBJECT[subject]
    out = {}
    for r in rows:
        if r.get("condition") != cond:
            continue
        if r.get("judge") != judge:
            continue
        if r.get("parse_failure"):
            continue
        score = r.get("score")
        if score is None:
            continue
        try:
            sf = float(score)
        except (TypeError, ValueError):
            continue
        if not (1.0 <= sf <= 5.0):
            continue
        out[int(r["question_id"])] = sf
    return out


# ---------- Response-text loaders ----------


def load_letta_response_text(subject: str) -> dict[int, dict[str, str]]:
    """Return {qid: {response_text, question_text, held_out_passage}} for the
    Letta-block-direct condition."""
    base = MEMORY_PATH_BY_SUBJECT[subject]
    path = base / "letta_memory_haiku_results.json"
    d = load_json(path)
    res = d["results"]
    out = {}
    for r in res:
        qid = int(r["question_id"])
        rsp = r.get("response", {})
        if isinstance(rsp, dict):
            text = rsp.get("text", "")
        else:
            text = str(rsp)
        out[qid] = {
            "response_text": text,
            "question_text": r.get("question_text", ""),
            "held_out_passage": r.get("held_out_passage", ""),
        }
    return out


def load_bl_response_text(subject: str) -> dict[int, dict[str, str]]:
    """Return {qid: {response_text, question_text, held_out_passage}} for the
    BL unified-brief condition."""
    if subject == "hamerton":
        # Hamerton: results.json filtered to C2a_full_spec (80 rows total, 39 used)
        path = MEMORY_PATH_BY_SUBJECT[subject] / "results.json"
        d = load_json(path)
        out = {}
        for r in d:
            qid = int(r["question_id"])
            rsp = r.get("responses", {})
            if not isinstance(rsp, dict):
                continue
            c2a = rsp.get("C2a_full_spec")
            if not c2a:
                continue
            text = c2a.get("text") if isinstance(c2a, dict) else str(c2a)
            out[qid] = {
                "response_text": text,
                "question_text": r.get("question_text", ""),
                "held_out_passage": r.get("held_out_passage", ""),
            }
        return out
    # Ebers / Babur: _letta_rerun/<subject>_bl_c2a_named_responses.json
    path = RERUN / f"{subject}_bl_c2a_named_responses.json"
    d = load_json(path)
    res = d["results"]
    out = {}
    for r in res:
        qid = int(r["question_id"])
        rsp = r.get("response")
        if isinstance(rsp, dict):
            text = rsp.get("text", "")
        else:
            text = str(rsp) if rsp is not None else ""
        out[qid] = {
            "response_text": text,
            "question_text": r.get("question_text", ""),
            "held_out_passage": r.get("held_out_passage", ""),
        }
    return out


# ---------- Embedding helpers ----------

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def ngram_overlap_pct(text: str, ref_text: str, n: int = 5) -> float | None:
    """Fraction of n-word sequences in `text` that appear verbatim in `ref_text`.

    Lowercased word tokens, punctuation stripped. Mirrors the helper in
    `_v11_emit_4_5_letta.py`. Returns 0.0 if either side has fewer than n
    tokens.
    """
    def toks(s: str) -> list[str]:
        return re.findall(r"[a-z]+", s.lower())

    text_tokens = toks(text)
    ref_tokens = toks(ref_text)
    if len(text_tokens) < n or len(ref_tokens) < n:
        return 0.0
    ref_grams = set()
    for i in range(len(ref_tokens) - n + 1):
        ref_grams.add(tuple(ref_tokens[i : i + n]))
    text_grams_total = 0
    text_grams_hit = 0
    for i in range(len(text_tokens) - n + 1):
        g = tuple(text_tokens[i : i + n])
        text_grams_total += 1
        if g in ref_grams:
            text_grams_hit += 1
    if text_grams_total == 0:
        return 0.0
    return 100.0 * text_grams_hit / text_grams_total


def split_sentences(text: str, min_chars: int = 15) -> list[str]:
    if not text:
        return []
    raw = SENT_SPLIT.split(text)
    out = []
    for s in raw:
        s = re.sub(r"\s+", " ", s.strip())
        if len(s) >= min_chars:
            out.append(s)
    if not out and text.strip():
        # Fallback: text with no sentence break
        out = [re.sub(r"\s+", " ", text.strip())[:1000]]
    return out


def mean_pooled_embedding(text: str, model: SentenceTransformer) -> np.ndarray | None:
    """Mean-pool sentence embeddings; returns L2-normalized vector or None."""
    sents = split_sentences(text)
    if not sents:
        return None
    embs = model.encode(
        sents,
        batch_size=32,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    mean = embs.mean(axis=0)
    norm = np.linalg.norm(mean)
    if norm == 0:
        return None
    return mean / norm


def cosine(a: np.ndarray | None, b: np.ndarray | None) -> float | None:
    if a is None or b is None:
        return None
    return float(np.dot(a, b))


# ---------- Per-question pipeline ----------


def collect_per_question_scores(subject: str) -> dict[int, dict[str, Any]]:
    """For one subject, gather per-judge scores across the primary panel for
    both conditions. Apply drop rule: keep qid only if at least one judge
    on each condition has a valid score.

    Returns {qid: {letta_score, spec_score, letta_per_judge, spec_per_judge}}.
    """
    letta_per_judge: dict[str, dict[int, float]] = {}
    spec_per_judge: dict[str, dict[int, float]] = {}
    for j in PRIMARY_PANEL:
        letta_per_judge[j] = load_letta_block_per_qid_score(subject, j)
        spec_per_judge[j] = load_bl_unified_per_qid_score(subject, j)

    # Union of qids across both sides
    all_qids = set()
    for j in PRIMARY_PANEL:
        all_qids |= set(letta_per_judge[j].keys()) | set(spec_per_judge[j].keys())

    out = {}
    for qid in sorted(all_qids):
        letta_scores = [
            letta_per_judge[j][qid] for j in PRIMARY_PANEL if qid in letta_per_judge[j]
        ]
        spec_scores = [
            spec_per_judge[j][qid] for j in PRIMARY_PANEL if qid in spec_per_judge[j]
        ]
        if not letta_scores or not spec_scores:
            continue
        out[qid] = {
            "letta_score": statistics.mean(letta_scores),
            "spec_score": statistics.mean(spec_scores),
            "letta_per_judge": {
                j: letta_per_judge[j].get(qid) for j in PRIMARY_PANEL
            },
            "spec_per_judge": {
                j: spec_per_judge[j].get(qid) for j in PRIMARY_PANEL
            },
        }
    return out


# ---------- Aggregate stats ----------


def pearson_corr(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = sum((x - mx) ** 2 for x in xs)
    den_y = sum((y - my) ** 2 for y in ys)
    if den_x == 0 or den_y == 0:
        return None
    return num / ((den_x * den_y) ** 0.5)


def spearman_corr(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None

    def rank(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        ranks = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[order[k]] = avg_rank
            i = j + 1
        return ranks

    rx = rank(xs)
    ry = rank(ys)
    return pearson_corr(rx, ry)


# ---------- Main ----------


def main():
    print(f"[{__file__}] starting analysis ...")
    print("Loading sentence-transformer all-MiniLM-L6-v2 ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    csv_rows: list[dict[str, Any]] = []
    per_subject_summary: dict[str, dict[str, Any]] = {}

    for subject in SUBJECTS:
        print(f"\n=== {SUBJECT_DISPLAY[subject]} ===")
        scores_by_qid = collect_per_question_scores(subject)
        letta_texts = load_letta_response_text(subject)
        bl_texts = load_bl_response_text(subject)

        kept = sorted(
            qid
            for qid in scores_by_qid
            if qid in letta_texts and qid in bl_texts
        )
        dropped = sorted(set(scores_by_qid) - set(kept))
        print(
            f"  paired qids with valid scores+responses: {len(kept)}; "
            f"dropped: {dropped if dropped else 'none'}"
        )

        for qid in kept:
            sd = scores_by_qid[qid]
            letta_text = letta_texts[qid]["response_text"] or ""
            spec_text = bl_texts[qid]["response_text"] or ""
            heldout = letta_texts[qid]["held_out_passage"] or bl_texts[qid].get(
                "held_out_passage", ""
            )
            qtext = letta_texts[qid]["question_text"] or bl_texts[qid].get(
                "question_text", ""
            )

            letta_emb = mean_pooled_embedding(letta_text, model)
            spec_emb = mean_pooled_embedding(spec_text, model)
            heldout_emb = mean_pooled_embedding(heldout, model)

            cos_letta_heldout = cosine(letta_emb, heldout_emb)
            cos_spec_heldout = cosine(spec_emb, heldout_emb)
            cos_letta_spec = cosine(letta_emb, spec_emb)

            # Surface-syntactic n-gram overlap (verbatim phrase echo)
            # 5-gram is the canonical verbatim-phrase test from
            # _v11_emit_4_5_letta.py.
            ngram5_letta_heldout = (
                ngram_overlap_pct(letta_text, heldout, n=5)
                if (letta_text and heldout)
                else None
            )
            ngram5_spec_heldout = (
                ngram_overlap_pct(spec_text, heldout, n=5)
                if (spec_text and heldout)
                else None
            )
            ngram5_gap = (
                ngram5_letta_heldout - ngram5_spec_heldout
                if (
                    ngram5_letta_heldout is not None
                    and ngram5_spec_heldout is not None
                )
                else None
            )
            # 3-gram is a sensitivity measure — short phrases / proper-name
            # bigrams + a connective token. Picks up named-entity grounding.
            ngram3_letta_heldout = (
                ngram_overlap_pct(letta_text, heldout, n=3)
                if (letta_text and heldout)
                else None
            )
            ngram3_spec_heldout = (
                ngram_overlap_pct(spec_text, heldout, n=3)
                if (spec_text and heldout)
                else None
            )
            ngram3_gap = (
                ngram3_letta_heldout - ngram3_spec_heldout
                if (
                    ngram3_letta_heldout is not None
                    and ngram3_spec_heldout is not None
                )
                else None
            )

            csv_rows.append(
                {
                    "subject": subject,
                    "question_id": qid,
                    "question_text": qtext,
                    "letta_score": round(sd["letta_score"], 4),
                    "spec_score": round(sd["spec_score"], 4),
                    "score_delta": round(sd["letta_score"] - sd["spec_score"], 4),
                    "cos_letta_heldout": round(cos_letta_heldout, 4)
                    if cos_letta_heldout is not None
                    else "",
                    "cos_spec_heldout": round(cos_spec_heldout, 4)
                    if cos_spec_heldout is not None
                    else "",
                    "cos_letta_spec": round(cos_letta_spec, 4)
                    if cos_letta_spec is not None
                    else "",
                    "texture_gap": round(
                        cos_letta_heldout - cos_spec_heldout, 4
                    )
                    if (cos_letta_heldout is not None and cos_spec_heldout is not None)
                    else "",
                    "ngram5_letta_heldout": round(ngram5_letta_heldout, 4)
                    if ngram5_letta_heldout is not None
                    else "",
                    "ngram5_spec_heldout": round(ngram5_spec_heldout, 4)
                    if ngram5_spec_heldout is not None
                    else "",
                    "ngram5_gap": round(ngram5_gap, 4)
                    if ngram5_gap is not None
                    else "",
                    "ngram3_letta_heldout": round(ngram3_letta_heldout, 4)
                    if ngram3_letta_heldout is not None
                    else "",
                    "ngram3_spec_heldout": round(ngram3_spec_heldout, 4)
                    if ngram3_spec_heldout is not None
                    else "",
                    "ngram3_gap": round(ngram3_gap, 4)
                    if ngram3_gap is not None
                    else "",
                    "heldout_passage_excerpt": heldout[:200].replace("\n", " ").strip()
                    if heldout
                    else "",
                    "letta_response_excerpt": letta_text[:200]
                    .replace("\n", " ")
                    .strip(),
                    "spec_response_excerpt": spec_text[:200]
                    .replace("\n", " ")
                    .strip(),
                    "letta_haiku": sd["letta_per_judge"].get("haiku"),
                    "letta_sonnet": sd["letta_per_judge"].get("sonnet"),
                    "letta_opus": sd["letta_per_judge"].get("opus"),
                    "letta_gpt4o": sd["letta_per_judge"].get("gpt4o"),
                    "letta_gpt54": sd["letta_per_judge"].get("gpt54"),
                    "spec_haiku": sd["spec_per_judge"].get("haiku"),
                    "spec_sonnet": sd["spec_per_judge"].get("sonnet"),
                    "spec_opus": sd["spec_per_judge"].get("opus"),
                    "spec_gpt4o": sd["spec_per_judge"].get("gpt4o"),
                    "spec_gpt54": sd["spec_per_judge"].get("gpt54"),
                }
            )

        per_subject_summary[subject] = {
            "n_kept": len(kept),
            "n_dropped": len(dropped),
            "dropped_qids": dropped,
        }

    # Write CSV
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "subject",
        "question_id",
        "question_text",
        "letta_score",
        "spec_score",
        "score_delta",
        "cos_letta_heldout",
        "cos_spec_heldout",
        "cos_letta_spec",
        "texture_gap",
        "ngram5_letta_heldout",
        "ngram5_spec_heldout",
        "ngram5_gap",
        "ngram3_letta_heldout",
        "ngram3_spec_heldout",
        "ngram3_gap",
        "heldout_passage_excerpt",
        "letta_response_excerpt",
        "spec_response_excerpt",
        "letta_haiku",
        "letta_sonnet",
        "letta_opus",
        "letta_gpt4o",
        "letta_gpt54",
        "spec_haiku",
        "spec_sonnet",
        "spec_opus",
        "spec_gpt4o",
        "spec_gpt54",
    ]
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in csv_rows:
            w.writerow(row)
    print(f"\nWrote CSV: {CSV_OUT} ({len(csv_rows)} rows)")

    # ---------- Aggregate stats ----------

    n_total = len(csv_rows)

    # Class A — Content-equivalent, score-divergent
    class_a = [
        r
        for r in csv_rows
        if r["cos_letta_spec"] != ""
        and r["cos_letta_spec"] > 0.75
        and abs(r["score_delta"]) > 1.0
    ]
    # Class B — Spec excels (Spec scored ≥ 0.5 higher; i.e. delta < -0.5)
    class_b = [r for r in csv_rows if r["score_delta"] < -0.5]
    # Class C — Both high, different paths
    class_c = [
        r
        for r in csv_rows
        if r["letta_score"] >= 3.0
        and r["spec_score"] >= 3.0
        and r["cos_letta_spec"] != ""
        and r["cos_letta_spec"] < 0.5
    ]

    # Texture-leakage Pearson r (pooled)
    pool_xs = [
        r["score_delta"]
        for r in csv_rows
        if r["texture_gap"] != ""
    ]
    pool_ys = [
        r["texture_gap"]
        for r in csv_rows
        if r["texture_gap"] != ""
    ]
    pool_pearson = pearson_corr(pool_xs, pool_ys)
    pool_spearman = spearman_corr(pool_xs, pool_ys)

    # Within-subject correlations (semantic / texture_gap)
    within_subject_corr = {}
    for subject in SUBJECTS:
        rows_s = [r for r in csv_rows if r["subject"] == subject and r["texture_gap"] != ""]
        xs = [r["score_delta"] for r in rows_s]
        ys = [r["texture_gap"] for r in rows_s]
        within_subject_corr[subject] = {
            "n": len(rows_s),
            "pearson_r": pearson_corr(xs, ys),
            "spearman_rho": spearman_corr(xs, ys),
            "mean_score_delta": statistics.mean(xs) if xs else None,
            "mean_texture_gap": statistics.mean(ys) if ys else None,
        }

    # ---- N-gram (surface-syntactic) correlations ----
    def ngram_block(gap_field, l_field, s_field):
        pool_xs_ng = [r["score_delta"] for r in csv_rows if r[gap_field] != ""]
        pool_ys_ng = [r[gap_field] for r in csv_rows if r[gap_field] != ""]
        pool_p = pearson_corr(pool_xs_ng, pool_ys_ng)
        pool_s = spearman_corr(pool_xs_ng, pool_ys_ng)
        per_subject = {}
        for subject in SUBJECTS:
            rows_s = [
                r for r in csv_rows
                if r["subject"] == subject and r[gap_field] != ""
            ]
            xs = [r["score_delta"] for r in rows_s]
            ys = [r[gap_field] for r in rows_s]
            ngL = [r[l_field] for r in rows_s if r[l_field] != ""]
            ngS = [r[s_field] for r in rows_s if r[s_field] != ""]
            per_subject[subject] = {
                "n": len(rows_s),
                "pearson_r": pearson_corr(xs, ys),
                "spearman_rho": spearman_corr(xs, ys),
                "mean_score_delta": statistics.mean(xs) if xs else None,
                "mean_gap": statistics.mean(ys) if ys else None,
                "mean_letta_heldout": statistics.mean(ngL) if ngL else None,
                "mean_spec_heldout": statistics.mean(ngS) if ngS else None,
                "max_letta_heldout": max(ngL) if ngL else None,
                "max_spec_heldout": max(ngS) if ngS else None,
            }
        return pool_p, pool_s, per_subject

    pool_pearson_ng5, pool_spearman_ng5, within_subject_corr_ngram5 = ngram_block(
        "ngram5_gap", "ngram5_letta_heldout", "ngram5_spec_heldout"
    )
    pool_pearson_ng3, pool_spearman_ng3, within_subject_corr_ngram3 = ngram_block(
        "ngram3_gap", "ngram3_letta_heldout", "ngram3_spec_heldout"
    )
    # alias for back-compat with existing code below
    within_subject_corr_ngram = within_subject_corr_ngram5
    pool_pearson_ng = pool_pearson_ng5
    pool_spearman_ng = pool_spearman_ng5

    # Sort Class A by |texture_gap| descending
    class_a_sorted = sorted(
        class_a,
        key=lambda r: abs(r["texture_gap"]) if r["texture_gap"] != "" else 0,
        reverse=True,
    )

    # Class A mean texture gap
    class_a_mean_gap = (
        statistics.mean(r["texture_gap"] for r in class_a if r["texture_gap"] != "")
        if class_a
        else None
    )

    summary = {
        "n_total": n_total,
        "per_subject": per_subject_summary,
        "class_a_count": len(class_a),
        "class_a_pct": round(100 * len(class_a) / n_total, 2) if n_total else 0,
        "class_a_mean_texture_gap": round(class_a_mean_gap, 4)
        if class_a_mean_gap is not None
        else None,
        "class_b_count": len(class_b),
        "class_b_pct": round(100 * len(class_b) / n_total, 2) if n_total else 0,
        "class_c_count": len(class_c),
        "class_c_pct": round(100 * len(class_c) / n_total, 2) if n_total else 0,
        "pooled_pearson_r": round(pool_pearson, 4) if pool_pearson is not None else None,
        "pooled_spearman_rho": round(pool_spearman, 4)
        if pool_spearman is not None
        else None,
        "pooled_pearson_r_ngram5": round(pool_pearson_ng5, 4)
        if pool_pearson_ng5 is not None
        else None,
        "pooled_spearman_rho_ngram5": round(pool_spearman_ng5, 4)
        if pool_spearman_ng5 is not None
        else None,
        "pooled_pearson_r_ngram3": round(pool_pearson_ng3, 4)
        if pool_pearson_ng3 is not None
        else None,
        "pooled_spearman_rho_ngram3": round(pool_spearman_ng3, 4)
        if pool_spearman_ng3 is not None
        else None,
        "within_subject_ngram5": {
            s: {
                "n": v["n"],
                "pearson_r": (round(v["pearson_r"], 4) if v["pearson_r"] is not None else None),
                "spearman_rho": (round(v["spearman_rho"], 4) if v["spearman_rho"] is not None else None),
                "mean_score_delta": (round(v["mean_score_delta"], 4) if v["mean_score_delta"] is not None else None),
                "mean_gap": (round(v["mean_gap"], 4) if v["mean_gap"] is not None else None),
                "mean_letta_heldout": (round(v["mean_letta_heldout"], 4) if v["mean_letta_heldout"] is not None else None),
                "mean_spec_heldout": (round(v["mean_spec_heldout"], 4) if v["mean_spec_heldout"] is not None else None),
                "max_letta_heldout": (round(v["max_letta_heldout"], 4) if v["max_letta_heldout"] is not None else None),
                "max_spec_heldout": (round(v["max_spec_heldout"], 4) if v["max_spec_heldout"] is not None else None),
            }
            for s, v in within_subject_corr_ngram5.items()
        },
        "within_subject_ngram3": {
            s: {
                "n": v["n"],
                "pearson_r": (round(v["pearson_r"], 4) if v["pearson_r"] is not None else None),
                "spearman_rho": (round(v["spearman_rho"], 4) if v["spearman_rho"] is not None else None),
                "mean_score_delta": (round(v["mean_score_delta"], 4) if v["mean_score_delta"] is not None else None),
                "mean_gap": (round(v["mean_gap"], 4) if v["mean_gap"] is not None else None),
                "mean_letta_heldout": (round(v["mean_letta_heldout"], 4) if v["mean_letta_heldout"] is not None else None),
                "mean_spec_heldout": (round(v["mean_spec_heldout"], 4) if v["mean_spec_heldout"] is not None else None),
                "max_letta_heldout": (round(v["max_letta_heldout"], 4) if v["max_letta_heldout"] is not None else None),
                "max_spec_heldout": (round(v["max_spec_heldout"], 4) if v["max_spec_heldout"] is not None else None),
            }
            for s, v in within_subject_corr_ngram3.items()
        },
        "within_subject": {
            s: {
                "n": v["n"],
                "pearson_r": round(v["pearson_r"], 4)
                if v["pearson_r"] is not None
                else None,
                "spearman_rho": round(v["spearman_rho"], 4)
                if v["spearman_rho"] is not None
                else None,
                "mean_score_delta": round(v["mean_score_delta"], 4)
                if v["mean_score_delta"] is not None
                else None,
                "mean_texture_gap": round(v["mean_texture_gap"], 4)
                if v["mean_texture_gap"] is not None
                else None,
            }
            for s, v in within_subject_corr.items()
        },
        "class_a_top": class_a_sorted[:6],
        "class_b_top": sorted(class_b, key=lambda r: r["score_delta"])[:6],
        "class_c_top": sorted(
            class_c, key=lambda r: r["letta_score"] + r["spec_score"], reverse=True
        )[:6],
    }

    # Persist summary as JSON for downstream use
    SUMMARY_OUT = OUT_DIR / "letta_vs_spec_leakage_summary_20260507.json"
    with SUMMARY_OUT.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"Wrote summary JSON: {SUMMARY_OUT}")

    # ---------- Print to console ----------
    print("\n" + "=" * 78)
    print("AGGREGATE TEXTURE-LEAKAGE ANALYSIS")
    print("=" * 78)
    print(f"N_total kept: {n_total}")
    for s, v in per_subject_summary.items():
        print(f"  {SUBJECT_DISPLAY[s]}: kept={v['n_kept']} dropped={v['n_dropped']} {v['dropped_qids']}")

    print(f"\nClass A (cos_letta_spec>0.75 AND |score_delta|>1.0): "
          f"{len(class_a)} ({summary['class_a_pct']}%)")
    print(f"  mean texture_gap (cos_letta_heldout - cos_spec_heldout): {class_a_mean_gap}")
    print(f"Class B (Spec excels, score_delta<-0.5): "
          f"{len(class_b)} ({summary['class_b_pct']}%)")
    print(f"Class C (both >=3.0 AND cos_letta_spec<0.5): "
          f"{len(class_c)} ({summary['class_c_pct']}%)")

    print(f"\nPooled correlation (score_delta, texture_gap):")
    print(f"  Pearson r: {pool_pearson}")
    print(f"  Spearman rho: {pool_spearman}")

    print(f"\nWithin-subject correlation (score_delta, texture_gap):")
    for s, v in within_subject_corr.items():
        print(f"  {SUBJECT_DISPLAY[s]} (n={v['n']}): "
              f"Pearson r={v['pearson_r']}, Spearman rho={v['spearman_rho']}, "
              f"mean d={v['mean_score_delta']}, mean gap={v['mean_texture_gap']}")

    print(f"\n--- 5-gram (verbatim phrase) overlap ---")
    print(f"Pooled Pearson r={pool_pearson_ng5}, Spearman rho={pool_spearman_ng5}")
    for s, v in within_subject_corr_ngram5.items():
        print(f"  {SUBJECT_DISPLAY[s]} (n={v['n']}): "
              f"Pearson r={v['pearson_r']}, "
              f"mean gap={v['mean_gap']}, "
              f"mean L_h={v['mean_letta_heldout']} (max {v['max_letta_heldout']}), "
              f"mean S_h={v['mean_spec_heldout']} (max {v['max_spec_heldout']})")
    print(f"\n--- 3-gram (named-entity / short-phrase) overlap ---")
    print(f"Pooled Pearson r={pool_pearson_ng3}, Spearman rho={pool_spearman_ng3}")
    for s, v in within_subject_corr_ngram3.items():
        print(f"  {SUBJECT_DISPLAY[s]} (n={v['n']}): "
              f"Pearson r={v['pearson_r']}, "
              f"mean gap={v['mean_gap']}, "
              f"mean L_h={v['mean_letta_heldout']} (max {v['max_letta_heldout']}), "
              f"mean S_h={v['mean_spec_heldout']} (max {v['max_spec_heldout']})")

    print()
    print("Top Class A cases (sorted by |texture_gap|):")
    for r in class_a_sorted[:6]:
        print(
            f"  {r['subject']:9s} q{r['question_id']:>2}  d={r['score_delta']:+.2f}  "
            f"cos_letta_heldout={r['cos_letta_heldout']:.3f}  "
            f"cos_spec_heldout={r['cos_spec_heldout']:.3f}  "
            f"gap={r['texture_gap']:+.3f}  cos_letta_spec={r['cos_letta_spec']:.3f}"
        )


if __name__ == "__main__":
    main()
