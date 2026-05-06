"""
Per-question anchor-crossing analysis across all relevant condition pairs for §4.2.

Extends `compute_anchor_crossing_c4a_c4_and_c9_c8.py` to the full set of pairs:

  Same-source-file (judgments_v2.json):
    C5_baseline               -> C4a_full_facts_plus_spec       (full pipeline from baseline)
    C5_baseline               -> C4_factdump                    (facts from baseline, no spec)
    C5_baseline               -> C2a_full_spec                  (spec from baseline)
    C2c_wrong_spec            -> C2a_full_spec                  (correct spec vs wrong spec)
    C4_factdump               -> C4a_full_facts_plus_spec       (spec on top of facts)

  Cross-source-file (judgments_v2.json + c8_c9_judgments_merged.json):
    C5_baseline               -> C8_raw_corpus                  (raw corpus from baseline)
    C5_baseline               -> C9_raw_corpus_plus_spec        (corpus+spec from baseline)
    C8_raw_corpus             -> C9_raw_corpus_plus_spec        (spec on top of corpus)

Subject set: all 14 main-study subjects. Babur is excluded *only* for any pair
involving C8 or C9 (context overflow at corpus length).

Output: docs/research/multi_anchor_rates_all_pairs_20260430.json
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_PATH = REPO / 'docs' / 'research' / 'multi_anchor_rates_all_pairs_20260430.json'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

ALL_14 = [
    'hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
    'bernal_diaz', 'keckley', 'yung_wing', 'babur',
    'augustine', 'equiano', 'cellini', 'rousseau', 'zitkala_sa',
]
# Babur excluded from C8/C9 (context overflow)
ALL_14_NO_BABUR = [s for s in ALL_14 if s != 'babur']


def integer_band(m):
    if m is None:
        return None
    if m < 1.0:
        return 0
    if m >= 5.0:
        return 5
    return int(m)


def subject_results_dir(subject):
    return RESULTS / 'hamerton' if subject == 'hamerton' else RESULTS / f'global_{subject}'


def load_judgments_v2(subject):
    """Load main judgments_v2.json (for C5/C2a/C2c/C4/C4a)."""
    if subject == 'hamerton':
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from recompute_5judge_primary import load_hamerton_judgments
        return load_hamerton_judgments()
    p = subject_results_dir(subject) / 'judgments_v2.json'
    return json.load(p.open(encoding='utf-8')) if p.exists() else []


def load_c8_c9(subject):
    """Load c8_c9_judgments_merged.json (for C8/C9)."""
    p = subject_results_dir(subject) / 'c8_c9_judgments_merged.json'
    return json.load(p.open(encoding='utf-8')) if p.exists() else []


def load_combined(subject):
    """Combined rows from both files. Used for cross-file pairs (C5 vs C8/C9)."""
    return load_judgments_v2(subject) + load_c8_c9(subject)


def per_question_means(rows, target_conditions):
    bucket = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('parse_failure'):
            continue
        if r.get('score') is None:
            continue
        if r.get('condition') not in target_conditions:
            continue
        bucket[r['question_id']][r['condition']].append(r['score'])
    out = {}
    for qid, conds in bucket.items():
        per_q = {}
        for cond, scores in conds.items():
            if len(scores) >= 3:
                per_q[cond] = statistics.mean(scores)
        out[qid] = per_q
    return out


def analyze_pair(subjects, pre_cond, post_cond, source_loader, label):
    """Compute paired anchor-crossings for one (pre, post) condition pair."""
    boundary_counts = defaultdict(int)
    multi_anchor_examples = []
    per_subject = []
    total = up = down = none = 0
    sum_pre = sum_post = 0.0

    for subj in subjects:
        rows = source_loader(subj)
        if not rows:
            per_subject.append({'subject': subj, 'total': 0, 'note': 'no rows loaded'})
            continue
        per_q = per_question_means(rows, {pre_cond, post_cond})
        s_total = s_up = s_down = s_none = 0
        s_sum_pre = s_sum_post = 0.0
        for qid, conds in per_q.items():
            if pre_cond not in conds or post_cond not in conds:
                continue
            pre_m, post_m = conds[pre_cond], conds[post_cond]
            pre_b, post_b = integer_band(pre_m), integer_band(post_m)
            total += 1
            s_total += 1
            sum_pre += pre_m
            sum_post += post_m
            s_sum_pre += pre_m
            s_sum_post += post_m
            if post_b > pre_b:
                up += 1
                s_up += 1
                jump = post_b - pre_b
                boundary_counts[f'{pre_b}->{post_b}'] += 1
                if jump >= 2:
                    multi_anchor_examples.append({
                        'subject': subj, 'qid': qid, 'pre_band': pre_b, 'post_band': post_b,
                        'jump': jump, 'pre_mean': round(pre_m, 3),
                        'post_mean': round(post_m, 3),
                    })
            elif post_b < pre_b:
                down += 1
                s_down += 1
                boundary_counts[f'{pre_b}->{post_b} DOWN'] += 1
            else:
                none += 1
                s_none += 1
        per_subject.append({
            'subject': subj, 'total': s_total, 'upward': s_up,
            'downward': s_down, 'no_crossing': s_none,
            'upward_pct': round(100 * s_up / s_total, 1) if s_total else None,
            'mean_pre': round(s_sum_pre / s_total, 3) if s_total else None,
            'mean_post': round(s_sum_post / s_total, 3) if s_total else None,
            'mean_delta': round((s_sum_post - s_sum_pre) / s_total, 3) if s_total else None,
        })

    multi_anchor = sum(
        c for b, c in boundary_counts.items()
        if not b.endswith('DOWN')
        and (int(b.split('->')[1]) - int(b.split('->')[0])) >= 2
    )
    extreme = sum(
        c for b, c in boundary_counts.items()
        if not b.endswith('DOWN')
        and (int(b.split('->')[1]) - int(b.split('->')[0])) >= 3
    )

    if total == 0:
        return {
            'label': label, 'pre_cond': pre_cond, 'post_cond': post_cond,
            'subjects': subjects, 'n_paired_questions': 0,
            'note': 'No paired questions found',
        }

    return {
        'label': label,
        'pre_cond': pre_cond,
        'post_cond': post_cond,
        'subjects': subjects,
        'n_subjects': len(subjects),
        'n_paired_questions': total,
        'upward': up,
        'downward': down,
        'no_crossing': none,
        'upward_pct': round(100 * up / total, 1),
        'downward_pct': round(100 * down / total, 1),
        'no_crossing_pct': round(100 * none / total, 1),
        'net_upward': up - down,
        'net_upward_pct': round(100 * (up - down) / total, 1),
        'multi_anchor_count': multi_anchor,
        'multi_anchor_pct': round(100 * multi_anchor / total, 1),
        'extreme_count': extreme,
        'extreme_pct': round(100 * extreme / total, 1),
        'mean_pre': round(sum_pre / total, 3),
        'mean_post': round(sum_post / total, 3),
        'mean_delta': round((sum_post - sum_pre) / total, 3),
        'boundary_breakdown': dict(sorted(boundary_counts.items())),
        'per_subject': per_subject,
        'multi_anchor_examples': multi_anchor_examples,
    }


def main():
    pairs = [
        # Same-source-file pairs (judgments_v2.json), all 14 subjects
        ('C5_to_C4a', ALL_14, 'C5_baseline', 'C4a_full_facts_plus_spec',
         load_judgments_v2, 'C5 (baseline) -> C4a (facts + spec, full pipeline)'),
        ('C5_to_C4', ALL_14, 'C5_baseline', 'C4_factdump',
         load_judgments_v2, 'C5 (baseline) -> C4 (facts only)'),
        ('C5_to_C2a', ALL_14, 'C5_baseline', 'C2a_full_spec',
         load_judgments_v2, 'C5 (baseline) -> C2a (spec only)'),
        ('C2c_to_C2a', ALL_14, 'C2c_wrong_spec', 'C2a_full_spec',
         load_judgments_v2, 'C2c (wrong spec) -> C2a (correct spec)'),
        ('C4_to_C4a', ALL_14, 'C4_factdump', 'C4a_full_facts_plus_spec',
         load_judgments_v2, 'C4 (facts) -> C4a (facts + spec)'),
        # Cross-source-file pairs (need both files), Babur excluded
        ('C5_to_C8', ALL_14_NO_BABUR, 'C5_baseline', 'C8_raw_corpus',
         load_combined, 'C5 (baseline) -> C8 (raw corpus)'),
        ('C5_to_C9', ALL_14_NO_BABUR, 'C5_baseline', 'C9_raw_corpus_plus_spec',
         load_combined, 'C5 (baseline) -> C9 (raw corpus + spec)'),
        ('C8_to_C9', ALL_14_NO_BABUR, 'C8_raw_corpus', 'C9_raw_corpus_plus_spec',
         load_c8_c9, 'C8 (corpus) -> C9 (corpus + spec)'),
    ]

    results = {}
    for key, subjects, pre, post, loader, label in pairs:
        results[key] = analyze_pair(subjects, pre, post, loader, label)

    out = {
        'date': '2026-04-30',
        'aggregation': '5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54), per-question 5-judge mean',
        'integer_band_definition': 'floor(mean) clipped to [1, 5]; bands [1,2), [2,3), [3,4), [4,5]',
        'subject_set_notes': {
            'all_14_subjects_used_for': [
                'C5_to_C4a', 'C5_to_C4', 'C5_to_C2a', 'C2c_to_C2a', 'C4_to_C4a',
            ],
            'babur_excluded_for': ['C5_to_C8', 'C5_to_C9', 'C8_to_C9'],
            'rationale_babur_exclude': 'Context overflow at raw-corpus length',
        },
        'pairs': results,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'Wrote {OUT_PATH}\n')
    print(f'{"pair":<14} {"n":>5} {"up%":>6} {"multi%":>7} {"extreme%":>9} {"meanD":>7}')
    for key, r in results.items():
        if r.get('n_paired_questions', 0) == 0:
            print(f'{key:<14} EMPTY')
            continue
        print(f'{key:<14} {r["n_paired_questions"]:>5} '
              f'{r["upward_pct"]:>6.1f} {r["multi_anchor_pct"]:>7.1f} '
              f'{r["extreme_pct"]:>9.1f} {r["mean_delta"]:>+7.3f}')


if __name__ == '__main__':
    main()
