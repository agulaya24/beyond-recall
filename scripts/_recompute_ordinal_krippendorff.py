"""Ordinal Krippendorff alpha recompute for the v12.1 mechanistic figure check.

Paper §3.3.3 cites ordinal alpha = 0.659 (5-judge) and 0.535 (7-judge).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import krippendorff

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from recompute_5judge_primary import (  # noqa: E402
    load_global_judgments,
    load_hamerton_judgments,
    GLOBAL_SUBJECTS,
)

PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']
SENS_JUDGES = ['gemini_flash', 'gemini_pro']
SEVEN_JUDGES = PRIMARY_JUDGES + SENS_JUDGES

CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec']


def gather_all_scores():
    """Return list of (subject, condition, qid, judge, score)."""
    rows = []
    for subj in GLOBAL_SUBJECTS:
        try:
            records = load_global_judgments(subj)
        except Exception as e:
            print(f"  warn: {subj}: {e}")
            continue
        for rec in records:
            if rec.get('parse_failure'):
                continue
            score = rec.get('score')
            if score is None:
                continue
            cond = rec.get('condition')
            qid = rec.get('question_id')
            j = rec.get('judge')
            if cond is None or qid is None or j is None:
                continue
            rows.append((subj, cond, qid, j, float(score)))

    try:
        records = load_hamerton_judgments()
    except Exception as e:
        print(f"  warn: hamerton: {e}")
        records = []
    for rec in records:
        if rec.get('parse_failure'):
            continue
        score = rec.get('score')
        if score is None:
            continue
        cond = rec.get('condition')
        qid = rec.get('question_id')
        j = rec.get('judge')
        if cond is None or qid is None or j is None:
            continue
        rows.append(('hamerton', cond, qid, j, float(score)))

    return rows


def build_matrix(rows, judges, conditions):
    """Build a J x N matrix of scores; np.nan for missing."""
    cell = {}
    for subj, cond, qid, j, score in rows:
        if cond not in conditions or j not in judges:
            continue
        key = (subj, cond, qid)
        cell.setdefault(key, {}).setdefault(j, []).append(score)
    units = sorted(cell.keys())
    matrix = np.full((len(judges), len(units)), np.nan, dtype=float)
    for ci, key in enumerate(units):
        per_judge = cell[key]
        for ji, j in enumerate(judges):
            if j in per_judge:
                matrix[ji, ci] = sum(per_judge[j]) / len(per_judge[j])
    return matrix, units


def compute_alpha(matrix, level='ordinal'):
    # Filter columns to those with at least 2 non-NaN values; otherwise the
    # third-party `krippendorff` package warns/errors.
    valid_cols = np.sum(~np.isnan(matrix), axis=0) >= 2
    sub = matrix[:, valid_cols]
    if sub.size == 0:
        return None, 0
    alpha = krippendorff.alpha(reliability_data=sub, level_of_measurement=level)
    return alpha, sub.shape[1]


def main():
    print("Loading judgments...")
    rows = gather_all_scores()
    print(f"  Loaded {len(rows)} rows total")
    if not rows:
        print("  No rows loaded; aborting.")
        return

    for panel_name, judges in [('5-judge primary', PRIMARY_JUDGES),
                                ('7-judge sensitivity', SEVEN_JUDGES)]:
        print(f"\n== {panel_name} ==")
        # Pooled across CONDITIONS
        mat, units = build_matrix(rows, judges, CONDITIONS)
        a, n = compute_alpha(mat, 'ordinal')
        a_int, _ = compute_alpha(mat, 'interval')
        print(f"  pooled across {CONDITIONS}: ordinal alpha = {a:.4f} | interval alpha = {a_int:.4f} | n={n}")
        # Per-condition
        for cond in CONDITIONS:
            mat, _ = build_matrix(rows, judges, [cond])
            a, n = compute_alpha(mat, 'ordinal')
            print(f"    {cond}: ordinal alpha = {a:.4f} | n={n}")


if __name__ == '__main__':
    main()
