"""
Compute per-response anchor-crossing rate on low-baseline subjects (5-judge primary).

Definition: for each question on each low-baseline subject, compute the 5-judge mean
score under C5 (baseline) and under C4a (facts + spec). If the C4a mean lands in a
different integer band than the C5 mean, the question crossed an integer anchor.

Anchor bands: [1,2), [2,3), [3,4), [4,5], and the rubric floor [<1].

Reports:
  - Total low-baseline (C5 ≤ 2.0 on 5-judge primary) questions
  - Count and % that crossed an anchor upward (C4a band > C5 band)
  - Count and % that crossed an anchor downward (C4a band < C5 band)
  - Breakdown by anchor boundary crossed
"""

import json
from collections import defaultdict
from pathlib import Path
import statistics

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

# 5-judge primary low-baseline subjects (C5 ≤ 2.0)
LOW_BASELINE = [
    'hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
    'bernal_diaz', 'keckley', 'yung_wing', 'babur',
]


def load_subject_rows(subject):
    """Load all (question_id, condition, judge, score) rows for a subject,
    using the same normalization as recompute_5judge_primary.py."""
    if subject == 'hamerton':
        # Re-use the Hamerton loader from the recompute script
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from recompute_5judge_primary import load_hamerton_judgments
        return load_hamerton_judgments()
    path = RESULTS / f'global_{subject}' / 'judgments_v2.json'
    if not path.exists():
        return []
    return json.load(path.open())


def integer_band(mean_score):
    """Return which integer band a mean score falls into. A mean of exactly 3.0
    lands in the [3, 4) band (i.e., at the anchor itself)."""
    if mean_score is None:
        return None
    if mean_score < 1.0:
        return 0  # below rubric floor — shouldn't happen
    if mean_score >= 5.0:
        return 5
    return int(mean_score)


def main():
    total_questions = 0
    upward_crossings = 0
    downward_crossings = 0
    no_crossing = 0
    boundary_counts = defaultdict(int)
    per_subject_summary = {}

    for subject in LOW_BASELINE:
        rows = load_subject_rows(subject)
        if not rows:
            continue

        # Per-question per-condition collect primary judge scores
        per_q = defaultdict(lambda: defaultdict(list))
        for r in rows:
            if r['judge'] not in PRIMARY_JUDGES:
                continue
            if r.get('score') is None:
                continue
            if r.get('parse_failure'):
                continue
            per_q[r['question_id']][r['condition']].append(r['score'])

        # Compute per-question 5-judge means for C5 and C4a
        subj_up = 0
        subj_down = 0
        subj_none = 0
        subj_total = 0
        for qid, conds in per_q.items():
            c5_scores = conds.get('C5_baseline', [])
            c4a_scores = conds.get('C4a_full_facts_plus_spec', [])
            if not c5_scores or not c4a_scores:
                continue
            if len(c5_scores) < 3 or len(c4a_scores) < 3:
                continue
            c5_mean = statistics.mean(c5_scores)
            c4a_mean = statistics.mean(c4a_scores)
            c5_band = integer_band(c5_mean)
            c4a_band = integer_band(c4a_mean)

            subj_total += 1
            total_questions += 1

            if c4a_band > c5_band:
                subj_up += 1
                upward_crossings += 1
                boundary_counts[f'{c5_band}-{c4a_band}'] += 1
            elif c4a_band < c5_band:
                subj_down += 1
                downward_crossings += 1
            else:
                subj_none += 1
                no_crossing += 1

        per_subject_summary[subject] = {
            'total': subj_total,
            'upward': subj_up,
            'downward': subj_down,
            'no_crossing': subj_none,
        }

    print('\n=== Anchor-crossing rate (5-judge primary, low-baseline subjects, N=9) ===\n')
    print(f'Total questions analyzed:   {total_questions}')
    print(f'Upward crossings:            {upward_crossings} ({100*upward_crossings/total_questions:.1f}%)')
    print(f'Downward crossings:          {downward_crossings} ({100*downward_crossings/total_questions:.1f}%)')
    print(f'No anchor crossed:           {no_crossing} ({100*no_crossing/total_questions:.1f}%)')
    print(f'Net upward:                  {upward_crossings - downward_crossings} ({100*(upward_crossings-downward_crossings)/total_questions:.1f}%)')
    print()
    print('Upward crossing by band transition:')
    for boundary, count in sorted(boundary_counts.items()):
        print(f'  {boundary}: {count} ({100*count/total_questions:.1f}% of low-baseline questions)')
    print()
    print('Per-subject breakdown:')
    print(f'{"subject":<15} {"n":>5} {"up":>5} {"up%":>6} {"down":>5} {"none":>5}')
    for subj, s in per_subject_summary.items():
        up_pct = 100 * s["upward"] / s["total"] if s["total"] else 0
        print(f'{subj:<15} {s["total"]:>5} {s["upward"]:>5} {up_pct:>6.1f} {s["downward"]:>5} {s["no_crossing"]:>5}')


if __name__ == '__main__':
    main()
