"""
Compute 5-judge primary (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) and 7-judge
aggregate deltas for wrong-spec controls across the 13 global subjects.

- C2a full spec (correct)
- C2c_wrong_spec (v1, fixed derangement; see scripts/run_global_rerun.py WRONG_SPEC_PAIRING)  -> lives in global_<subj>/judgments_v2.json
- C2c_wrong_spec_v2 (random derangement, seed=42) -> lives in _wrong_spec_v2/global_<subj>/

Aggregation (matches recompute_5judge_primary.py):
  per-judge-condition mean across questions, then mean across judges in panel.
Subject-level Δ computed, then mean across 13 subjects.
"""

import json
import os
import statistics
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), '..', 'results')
BASE = os.path.normpath(BASE)

GLOBALS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
    'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee',
    'yung_wing', 'zitkala_sa',
]
PRIMARY = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
ALL = PRIMARY | {'gemini_flash', 'gemini_pro'}


def subject_cond_mean(rows, panel):
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in panel:
            continue
        if r.get('score') is None:
            continue
        if r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])
    per_c = defaultdict(list)
    for (c, j), scores in per_jc.items():
        if scores:
            per_c[c].append(statistics.mean(scores))
    return {c: statistics.mean(ms) for c, ms in per_c.items() if ms}


def load_v2_backfills(subject):
    overrides = {}
    bd = os.path.join(BASE, '_s114_backfills')
    if os.path.isdir(bd):
        prefix = f'global_{subject}__'
        for f in os.listdir(bd):
            if not f.startswith(prefix) or not f.endswith('.json'):
                continue
            try:
                data = json.load(open(os.path.join(bd, f), encoding='utf-8'))
            except Exception:
                continue
            for r in data:
                if r.get('score') is None:
                    continue
                overrides[(r['question_id'], r['condition'], r['judge'])] = (
                    r['score'], r.get('parse_failure', False)
                )
    return overrides


def main():
    results_5j = {}
    results_7j = {}

    for subj in GLOBALS:
        main_path = os.path.join(BASE, f'global_{subj}', 'judgments_v2.json')
        rows = json.load(open(main_path, encoding='utf-8'))
        overrides = load_v2_backfills(subj)
        for r in rows:
            key = (r.get('question_id'), r.get('condition'), r.get('judge'))
            if key in overrides:
                s, pf = overrides[key]
                r['score'] = s
                r['parse_failure'] = pf

        v2_rows = []
        for judge in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']:
            p = os.path.join(BASE, '_wrong_spec_v2', f'global_{subj}',
                             f'wrong_spec_v2_judgments_{judge}.json')
            if os.path.exists(p):
                v2_rows.extend(json.load(open(p, encoding='utf-8')))

        combined = rows + v2_rows
        results_5j[subj] = subject_cond_mean(combined, PRIMARY)
        results_7j[subj] = subject_cond_mean(combined, ALL)

    def summarize(results, label):
        d_c2a, d_v1, d_v2 = [], [], []
        print(f'\n=== {label} ===')
        hdr = f'{"subj":<15} {"C5":>6} {"C2a":>6} {"v1":>6} {"v2":>6} {"dC2a":>7} {"dV1":>7} {"dV2":>7}'
        print(hdr)
        for subj in GLOBALS:
            m = results[subj]
            c5 = m.get('C5_baseline')
            c2a = m.get('C2a_full_spec')
            v1 = m.get('C2c_wrong_spec')
            v2 = m.get('C2c_wrong_spec_v2')

            def f(x):
                return f'{x:.2f}' if x is not None else '  -- '

            def ff(a, b):
                if a is None or b is None:
                    return '  -- '
                return f'{a - b:+.2f}'

            print(f'{subj:<15} {f(c5):>6} {f(c2a):>6} {f(v1):>6} {f(v2):>6} '
                  f'{ff(c2a, c5):>7} {ff(v1, c5):>7} {ff(v2, c5):>7}')
            if c2a is not None and c5 is not None:
                d_c2a.append(c2a - c5)
            if v1 is not None and c5 is not None:
                d_v1.append(v1 - c5)
            if v2 is not None and c5 is not None:
                d_v2.append(v2 - c5)

        print(f'Mean d C2a vs C5:                      {statistics.mean(d_c2a):+.3f} (N={len(d_c2a)})')
        print(f'Mean d C2c v1 (fixed derangement) vs C5: {statistics.mean(d_v1):+.3f} (N={len(d_v1)})')
        print(f'Mean d C2c v2 (random derange) vs C5:   {statistics.mean(d_v2):+.3f} (N={len(d_v2)})')

        def grand(key):
            vals = [results[s].get(key) for s in GLOBALS if results[s].get(key) is not None]
            return statistics.mean(vals), len(vals)

        gc5 = grand('C5_baseline')
        gc2a = grand('C2a_full_spec')
        gv1 = grand('C2c_wrong_spec')
        gv2 = grand('C2c_wrong_spec_v2')
        print(f'Grand means: C5={gc5[0]:.3f}  C2a={gc2a[0]:.3f}  v1={gv1[0]:.3f}  v2={gv2[0]:.3f}')
        return {
            'mean_delta_c2a': statistics.mean(d_c2a),
            'mean_delta_v1': statistics.mean(d_v1),
            'mean_delta_v2': statistics.mean(d_v2),
            'grand_c5': gc5[0], 'grand_c2a': gc2a[0], 'grand_v1': gv1[0], 'grand_v2': gv2[0],
            'n_c2a': len(d_c2a), 'n_v1': len(d_v1), 'n_v2': len(d_v2),
        }

    s5 = summarize(results_5j, '5-judge primary (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4)')
    s7 = summarize(results_7j, '7-judge (primary + Gemini Flash + Gemini Pro where available)')

    print('\n=== Gemini inclusion effect (5-judge - 7-judge) ===')
    print(f'd C2a: {s5["mean_delta_c2a"] - s7["mean_delta_c2a"]:+.3f}')
    print(f'd v1:  {s5["mean_delta_v1"]  - s7["mean_delta_v1"]:+.3f}')
    print(f'd v2:  {s5["mean_delta_v2"]  - s7["mean_delta_v2"]:+.3f}')


if __name__ == '__main__':
    main()
