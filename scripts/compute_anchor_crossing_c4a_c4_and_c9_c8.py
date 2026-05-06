"""
Per-question anchor-crossing analysis for C4a vs C4 and C9 vs C8 paired pairs.

Extends `compute_anchor_crossing.py` (which only handles C5 -> C4a) to the two
spec-on-top-of-info-rich-context comparisons:
  - C4 (facts) -> C4a (facts + spec)
  - C8 (corpus) -> C9 (corpus + spec; Babur excluded due to context overflow)

Reads from per-subject judgment files, computes per-question 5-judge primary
means under each condition, classifies each question as upward / downward / no
anchor crossing, breaks down upward crossings by jump size and band-pair.

Output: docs/research/per_question_anchor_crossing_extended_20260428.json
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_PATH = REPO / 'docs' / 'research' / 'per_question_anchor_crossing_extended_20260428.json'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

LOW_BASELINE_FULL = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
                     'bernal_diaz', 'keckley', 'yung_wing', 'babur']
LOW_BASELINE_C9 = [s for s in LOW_BASELINE_FULL if s != 'babur']  # Babur excludes for C9


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
    """Load main judgments_v2.json (for C5/C2a/C4/C4a/C2c)."""
    if subject == 'hamerton':
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from recompute_5judge_primary import load_hamerton_judgments
        return load_hamerton_judgments()
    p = subject_results_dir(subject) / 'judgments_v2.json'
    return json.load(p.open(encoding='utf-8')) if p.exists() else []


def load_c8_c9_judgments(subject):
    """Load c8_c9_judgments_merged.json (for C8/C9)."""
    p = subject_results_dir(subject) / 'c8_c9_judgments_merged.json'
    return json.load(p.open(encoding='utf-8')) if p.exists() else []


def per_question_means(rows, target_conditions):
    """Build {question_id: {condition: mean_score}} for the 5-judge primary panel."""
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
    delta_count = 0

    for subj in subjects:
        rows = source_loader(subj)
        if not rows:
            continue
        per_q = per_question_means(rows, {pre_cond, post_cond})
        s_total = s_up = s_down = s_none = 0
        for qid, conds in per_q.items():
            if pre_cond not in conds or post_cond not in conds:
                continue
            pre_m, post_m = conds[pre_cond], conds[post_cond]
            pre_b, post_b = integer_band(pre_m), integer_band(post_m)
            total += 1
            s_total += 1
            sum_pre += pre_m
            sum_post += post_m
            delta_count += 1
            if post_b > pre_b:
                up += 1
                s_up += 1
                jump = post_b - pre_b
                boundary_counts[f'{pre_b}->{post_b}'] += 1
                if jump >= 2:
                    multi_anchor_examples.append({
                        'subject': subj, 'qid': qid, 'pre_band': pre_b, 'post_band': post_b,
                        'jump': jump, 'pre_mean': round(pre_m, 3), 'post_mean': round(post_m, 3),
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
        })

    multi_anchor = sum(c for b, c in boundary_counts.items()
                       if not b.endswith('DOWN') and (int(b.split('->')[1]) - int(b.split('->')[0])) >= 2)
    extreme = sum(c for b, c in boundary_counts.items()
                  if not b.endswith('DOWN') and (int(b.split('->')[1]) - int(b.split('->')[0])) >= 3)

    return {
        'label': label,
        'pre_cond': pre_cond,
        'post_cond': post_cond,
        'subjects': subjects,
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
        'mean_pre': round(sum_pre / delta_count, 3),
        'mean_post': round(sum_post / delta_count, 3),
        'mean_delta': round((sum_post - sum_pre) / delta_count, 3),
        'boundary_breakdown': dict(sorted(boundary_counts.items())),
        'per_subject': per_subject,
        'multi_anchor_examples': multi_anchor_examples,
    }


def main():
    c4a_vs_c4 = analyze_pair(
        LOW_BASELINE_FULL,
        pre_cond='C4_factdump',
        post_cond='C4a_full_facts_plus_spec',
        source_loader=load_judgments_v2,
        label='C4 (facts) -> C4a (facts + spec)',
    )
    c9_vs_c8 = analyze_pair(
        LOW_BASELINE_C9,
        pre_cond='C8_raw_corpus',
        post_cond='C9_raw_corpus_plus_spec',
        source_loader=load_c8_c9_judgments,
        label='C8 (corpus) -> C9 (corpus + spec)',
    )

    out = {
        'date': '2026-04-28',
        'aggregation': '5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54), per-question 5-judge mean',
        'integer_band_definition': 'floor(mean) clipped to [1, 5]; bands [1,2), [2,3), [3,4), [4,5]',
        'pairs': {
            'C4a_vs_C4': c4a_vs_c4,
            'C9_vs_C8': c9_vs_c8,
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'Wrote {OUT_PATH}')
    for label, pair in [('C4a vs C4', c4a_vs_c4), ('C9 vs C8', c9_vs_c8)]:
        print(f'\n{label}:  n={pair["n_paired_questions"]}  '
              f'up={pair["upward_pct"]}%  down={pair["downward_pct"]}%  '
              f'none={pair["no_crossing_pct"]}%  '
              f'multi-anchor={pair["multi_anchor_pct"]}%  '
              f'extreme={pair["extreme_pct"]}%  '
              f'mean Δ={pair["mean_delta"]:+.3f}')


if __name__ == '__main__':
    main()
