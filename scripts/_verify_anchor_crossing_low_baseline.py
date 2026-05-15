"""Verify paper §1.3 / §4.1 low-baseline anchor crossing claims exactly.

Paper §1.3 line 122 says:
- 55% one anchor upward
- 18% cross two or more anchors
- 5.9% cross three or more anchors
- 351 paired questions
- 9 low-baseline subjects, C5 -> C4a

Recompute from per-question 5-judge primary means.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from compute_anchor_crossing import load_subject_rows, integer_band, PRIMARY_JUDGES, LOW_BASELINE


def main():
    total = 0
    upward = 0  # crossings >= 1
    multi_anchor = 0  # >= 2
    extreme = 0  # >= 3
    downward = 0
    no_crossing = 0
    boundary = defaultdict(int)

    for subject in LOW_BASELINE:
        rows = load_subject_rows(subject)
        if not rows:
            continue
        per_q = defaultdict(lambda: defaultdict(list))
        for r in rows:
            if r.get('judge') not in PRIMARY_JUDGES:
                continue
            if r.get('score') is None:
                continue
            if r.get('parse_failure'):
                continue
            per_q[r.get('question_id')][r.get('condition')].append(r['score'])

        for qid, by_cond in per_q.items():
            c5 = by_cond.get('C5_baseline', [])
            c4a = by_cond.get('C4a_full_facts_plus_spec', [])
            if len(c5) < 3 or len(c4a) < 3:
                continue
            c5_mean = sum(c5) / len(c5)
            c4a_mean = sum(c4a) / len(c4a)
            c5_band = integer_band(c5_mean)
            c4a_band = integer_band(c4a_mean)
            diff = c4a_band - c5_band
            total += 1
            if diff >= 1:
                upward += 1
                boundary[f"{c5_band}->{c4a_band}"] += 1
            if diff >= 2:
                multi_anchor += 1
            if diff >= 3:
                extreme += 1
            if diff < 0:
                downward += 1
            if diff == 0:
                no_crossing += 1

    print(f"Total low-baseline paired questions: {total}")
    print(f"Upward (>=1 anchor up):  {upward} ({100*upward/total:.2f}%)")
    print(f"Multi-anchor (>=2):      {multi_anchor} ({100*multi_anchor/total:.2f}%)")
    print(f"Extreme (>=3):           {extreme} ({100*extreme/total:.2f}%)")
    print(f"Downward (<0):           {downward} ({100*downward/total:.2f}%)")
    print(f"No crossing (=0):        {no_crossing} ({100*no_crossing/total:.2f}%)")
    print()
    print("Upward boundary breakdown:")
    for k, v in sorted(boundary.items()):
        print(f"  {k}: {v} ({100*v/total:.2f}%)")


if __name__ == '__main__':
    main()
