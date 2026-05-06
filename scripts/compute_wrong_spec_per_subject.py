"""
Per-subject 5-judge and 7-judge C2c_wrong_spec (v1) deltas vs C5_baseline.

For the 13 global subjects, v1 is a deterministic fixed cross-subject pairing
defined in scripts/run_global_rerun.py (WRONG_SPEC_PAIRING, lines 51-60),
designed to maximize cultural and temporal distance. Hamerton's v1 is
separately Franklin's specification, loaded via run_full_study.py.

Extends compute_wrong_spec_5judge.py to include Hamerton, whose data layout
differs from the 13 globals (judgments fragmented across multiple files).

Uses recompute_5judge_primary.load_hamerton_judgments() for Hamerton so that
the C2c_full_wrong_spec condition (Franklin-for-Hamerton variant) is properly
normalized to 'C2c_wrong_spec'.

Focus: Sunity Devee, Ebers, Hamerton — the three subjects with baselines
within the author pilot's range (~1.0-1.3).
"""

import json
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

sys.path.insert(0, str(Path(__file__).parent))
from recompute_5judge_primary import (  # noqa: E402
    load_hamerton_judgments, load_global_judgments,
    PRIMARY_JUDGES, ALL_JUDGES,
)

GLOBALS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
    'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee',
    'yung_wing', 'zitkala_sa',
]
SUBJECTS = ['hamerton'] + GLOBALS
FOCUS = ['sunity_devee', 'ebers', 'hamerton']


def aggregate(rows, panel):
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in panel:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])
    per_c = defaultdict(list)
    for (c, j), scores in per_jc.items():
        if scores:
            per_c[c].append(statistics.mean(scores))
    return {c: statistics.mean(ms) for c, ms in per_c.items() if ms}


def load(subject):
    if subject == 'hamerton':
        return load_hamerton_judgments()
    return load_global_judgments(subject)


def main():
    results_5j = {}
    results_7j = {}

    for subj in SUBJECTS:
        rows = load(subj)
        results_5j[subj] = aggregate(rows, PRIMARY_JUDGES)
        results_7j[subj] = aggregate(rows, ALL_JUDGES)

    for label, panel in [('5-judge primary (Haiku/Sonnet/Opus/GPT-4o/GPT-5.4)', results_5j),
                         ('7-judge (primary + Gemini Flash + Gemini Pro where available)', results_7j)]:
        print(f'\n=== {label} ===')
        print(f'{"subj":<15} {"C5":>6} {"C2c_v1":>7} {"dV1":>7}')
        for subj in SUBJECTS:
            m = panel[subj]
            c5 = m.get('C5_baseline')
            v1 = m.get('C2c_wrong_spec')
            def f(x): return f'{x:.3f}' if x is not None else '  --  '
            def ff(a, b): return f'{a-b:+.3f}' if (a is not None and b is not None) else '  --  '
            marker = '  <--' if subj in FOCUS else ''
            print(f'{subj:<15} {f(c5):>6} {f(v1):>7} {ff(v1, c5):>7}{marker}')

        # Focus subset summary
        deltas = []
        for subj in FOCUS:
            m = panel[subj]
            c5 = m.get('C5_baseline')
            v1 = m.get('C2c_wrong_spec')
            if c5 is not None and v1 is not None:
                deltas.append((subj, c5, v1, v1 - c5))
        if deltas:
            print(f'\nFocus subset (matched-baseline, N={len(deltas)}):')
            for subj, c5, v1, d in deltas:
                print(f'  {subj:<15} C5={c5:.3f}  C2c_v1={v1:.3f}  d={d:+.3f}')
            mean_d = statistics.mean(d for *_, d in deltas)
            print(f'  Mean d (wrong-spec v1 - C5): {mean_d:+.3f}')  # Hamerton=Franklin, globals=fixed derangement


if __name__ == '__main__':
    main()
