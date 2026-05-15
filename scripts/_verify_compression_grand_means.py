"""Verify paper §4.2 grand-mean compression lifts (+0.71 Spec alone, +0.93 corpus alone).

Per `[^compression-grain]` footnote: these are grand-means across all responses,
not per-subject means. Per-subject-mean equivalents are +0.69 and +0.89 (delta_C2a/delta_C4a).

This script pools per-(subject, qid) 5-judge primary means across the 9 low-baseline
subjects, then takes the grand mean of (C2a - C5) and (C8 - C5) at the per-question grain.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from compute_anchor_crossing import LOW_BASELINE, PRIMARY_JUDGES, load_subject_rows
from _verify_c9_improvement_rate import load_c8_c9_judgments


def main():
    per_subject_qid_cond_mean = defaultdict(dict)
    for subject in LOW_BASELINE:
        rows_main = load_subject_rows(subject)
        rows_c89 = load_c8_c9_judgments(subject)
        per_q = defaultdict(lambda: defaultdict(list))
        for r in (rows_main + rows_c89):
            if r.get('judge') not in PRIMARY_JUDGES:
                continue
            if r.get('score') is None or r.get('parse_failure'):
                continue
            per_q[r.get('question_id')][r.get('condition')].append(r['score'])
        for qid, by_cond in per_q.items():
            for cond, vals in by_cond.items():
                if len(vals) < 3:
                    continue
                per_subject_qid_cond_mean[(subject, qid)][cond] = sum(vals) / len(vals)

    # Grand-mean: pool all per-(subject, qid) means then take overall mean
    c5_vals = []
    c2a_vals = []
    c8_vals = []
    c4a_vals = []
    for key, by_cond in per_subject_qid_cond_mean.items():
        c5 = by_cond.get('C5_baseline')
        c2a = by_cond.get('C2a_full_spec')
        c8 = by_cond.get('C8_raw_corpus')
        c4a = by_cond.get('C4a_full_facts_plus_spec')
        if c5 is not None and c2a is not None:
            c5_vals.append(c5)
            c2a_vals.append(c2a)
        if c5 is not None and c8 is not None:
            c8_vals.append(c8)
        if c5 is not None and c4a is not None:
            c4a_vals.append(c4a)

    def mean(xs):
        return sum(xs) / len(xs) if xs else float('nan')

    # For C2a vs C5, the n is the paired count
    paired_c2a_c5 = []
    paired_c8_c5 = []
    paired_c4a_c5 = []
    for key, by_cond in per_subject_qid_cond_mean.items():
        c5 = by_cond.get('C5_baseline')
        if c5 is None:
            continue
        c2a = by_cond.get('C2a_full_spec')
        c8 = by_cond.get('C8_raw_corpus')
        c4a = by_cond.get('C4a_full_facts_plus_spec')
        if c2a is not None:
            paired_c2a_c5.append((c5, c2a))
        if c8 is not None:
            paired_c8_c5.append((c5, c8))
        if c4a is not None:
            paired_c4a_c5.append((c5, c4a))

    print(f"Paired (C2a, C5) n = {len(paired_c2a_c5)}")
    print(f"  Mean C5 = {mean([p[0] for p in paired_c2a_c5]):.4f}")
    print(f"  Mean C2a = {mean([p[1] for p in paired_c2a_c5]):.4f}")
    print(f"  Grand-mean delta (C2a - C5) = {mean([p[1] - p[0] for p in paired_c2a_c5]):+.4f}")
    print()
    print(f"Paired (C8, C5) n = {len(paired_c8_c5)}")
    print(f"  Mean C5 = {mean([p[0] for p in paired_c8_c5]):.4f}")
    print(f"  Mean C8 = {mean([p[1] for p in paired_c8_c5]):.4f}")
    print(f"  Grand-mean delta (C8 - C5) = {mean([p[1] - p[0] for p in paired_c8_c5]):+.4f}")
    print()
    print(f"Paired (C4a, C5) n = {len(paired_c4a_c5)}")
    print(f"  Mean C5 = {mean([p[0] for p in paired_c4a_c5]):.4f}")
    print(f"  Mean C4a = {mean([p[1] for p in paired_c4a_c5]):.4f}")
    print(f"  Grand-mean delta (C4a - C5) = {mean([p[1] - p[0] for p in paired_c4a_c5]):+.4f}")


if __name__ == '__main__':
    main()
