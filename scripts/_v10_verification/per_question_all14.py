"""Compute per-question improvement rates for ALL 14 subjects (paper §4.2.1 second table)."""
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'scripts'))
from _compute_per_question_v2 import per_question_means, CONDITION_MAP

ALL_14 = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
          'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa', 'rousseau',
          'augustine', 'equiano']

for cond in ('C2a', 'C4', 'C4a', 'C8', 'C9'):
    improved = tied = worsened = 0
    deltas_imp = []
    deltas_wor = []
    for subj in ALL_14:
        means = per_question_means(subj)
        c5_qids = {q for (c, q) in means if c == 'C5'}
        cond_qids = {q for (c, q) in means if c == cond}
        qids = sorted(c5_qids & cond_qids)
        for qid in qids:
            base = means[('C5', qid)]
            v = means[(cond, qid)]
            d = v - base
            if d > 1e-9:
                improved += 1
                deltas_imp.append(d)
            elif d < -1e-9:
                worsened += 1
                deltas_wor.append(d)
            else:
                tied += 1
    total = improved + tied + worsened
    pct_imp = 100*improved/total
    pct_w = 100*worsened/total
    pct_tied = 100*tied/total
    print(f'{cond}: n={total} improved={improved} ({pct_imp:.1f}%) tied={tied} ({pct_tied:.1f}%) worse={worsened} ({pct_w:.1f}%)')
