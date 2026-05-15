"""Verify C9 (corpus + spec) per-question improvement rate against paper §4.2.1 Fig caption (83.7%)."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from compute_anchor_crossing import LOW_BASELINE, PRIMARY_JUDGES, load_subject_rows

# C9 / C8 lives in c8_c9_judgments_merged.json
RESULTS = REPO / 'results'


def load_c8_c9_judgments(subject):
    """Load C8 / C9 judgments for a subject."""
    if subject == 'hamerton':
        p = RESULTS / 'hamerton' / 'c8_c9_judgments_merged.json'
    else:
        p = RESULTS / f'global_{subject}' / 'c8_c9_judgments_merged.json'
    if not p.exists():
        return []
    return json.loads(p.read_text())


def main():
    # Build per-(subject, qid) C5, C8, C9 5-judge means
    by_subject_qid = {}
    for subject in LOW_BASELINE:
        # C5 from main judgments
        rows_main = load_subject_rows(subject)
        rows_c89 = load_c8_c9_judgments(subject)
        per_q = defaultdict(lambda: defaultdict(list))
        for r in rows_main:
            if r.get('judge') not in PRIMARY_JUDGES:
                continue
            if r.get('score') is None or r.get('parse_failure'):
                continue
            per_q[r.get('question_id')][r.get('condition')].append(r['score'])
        for r in rows_c89:
            if r.get('judge') not in PRIMARY_JUDGES:
                continue
            if r.get('score') is None or r.get('parse_failure'):
                continue
            per_q[r.get('question_id')][r.get('condition')].append(r['score'])
        by_subject_qid[subject] = per_q

    # Compute improvement rate for C8/C9 vs C5
    for cond in ('C8_raw_corpus', 'C9_raw_corpus_plus_spec'):
        total = 0
        improved = 0
        tied = 0
        worse = 0
        for subject, per_q in by_subject_qid.items():
            if subject == 'babur':  # C9 excluded
                if cond == 'C9_raw_corpus_plus_spec':
                    continue
            for qid, by_cond in per_q.items():
                c5 = by_cond.get('C5_baseline', [])
                c89 = by_cond.get(cond, [])
                if len(c5) < 3 or len(c89) < 3:
                    continue
                c5_mean = sum(c5) / len(c5)
                c89_mean = sum(c89) / len(c89)
                diff = c89_mean - c5_mean
                total += 1
                if diff > 0:
                    improved += 1
                elif diff < 0:
                    worse += 1
                else:
                    tied += 1
        pct = 100 * improved / total if total else 0
        print(f"{cond}: improved={improved}/{total} = {pct:.2f}%  (tied={tied}, worse={worse})")


if __name__ == '__main__':
    main()
