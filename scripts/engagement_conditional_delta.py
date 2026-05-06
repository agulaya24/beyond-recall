"""
Engagement-conditional Δ_spec analysis.

Replaces the (methodologically-flawed) 2.5-recoding approach with a clean
two-metric partition:

  (1) Refusal rate per condition  (proportion of responses flagged as refusals)
  (2) Engagement-conditional mean  (mean judge score over NON-refusal responses)

Motivation. The 1-5 rubric anchors refusals at 1, same score as actively wrong
predictions. Recoding refusals to 2.5 is incorrect — a refusal provides zero
behavioral information about the subject and should not be treated as equivalent
to a partial-correct prediction. The honest sensitivity analysis reports refusal
rate and engagement-conditional mean as two separate quantities.

Classifier: both narrow (response starts with explicit refusal) and broader
(any refusal pattern anywhere in response), from scripts/classify_hedging.py.

Panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54). Same 14 subjects
(Hamerton + 13 globals) as the original recoding analysis.
"""

import json
import os
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESEARCH_DIR = REPO / 'docs' / 'research'
OUT_MD = RESEARCH_DIR / 'engagement_conditional_delta.md'
OUT_JSON = RESEARCH_DIR / 'engagement_conditional_delta.json'

# Reuse the classifier module from rubric_sensitivity_refusals
sys.path.insert(0, str(REPO / 'scripts'))
from rubric_sensitivity_refusals import (  # noqa: E402
    MAIN_STUDY,
    GRADIENT_CONDITIONS,
    PRIMARY_JUDGES,
    load_global_judgments,
    load_hamerton_judgments,
    load_global_responses,
    load_hamerton_responses,
    narrow_classifier,
    broader_classifier,
)

SUBJECTS = MAIN_STUDY
CONDITIONS = GRADIENT_CONDITIONS
JUDGES = PRIMARY_JUDGES


def is_refusal_narrow(text):
    return narrow_classifier(text or '')


def is_refusal_broader(text):
    return broader_classifier(text or '')


def load_per_subject_judgments(subject):
    """Return list of records {question_id, condition, judge, score, response_text}."""
    if subject == 'hamerton':
        rows = load_hamerton_judgments()
        responses = load_hamerton_responses()
    else:
        rows = load_global_judgments(subject)
        responses = load_global_responses(subject)
    if not rows:
        return None
    out = []
    for r in rows:
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        score = r.get('score')
        if score is None or r.get('parse_failure'):
            continue
        key = (r.get('question_id'), r.get('condition'))
        text = responses.get(key, '') or ''
        out.append({
            'question_id': r.get('question_id'),
            'condition': r.get('condition'),
            'judge': r.get('judge'),
            'score': score,
            'response_text': text,
        })
    return out


def compute_per_subject(records_by_subject):
    """For each subject × condition, compute:
       - total responses (per-question aggregate across 5 judges)
       - refusal count (narrow, broader)
       - engagement-only mean score (excluding refusals)
    """
    out = {}
    for subject, records in records_by_subject.items():
        per_cond = {}
        for cond in CONDITIONS:
            narrow_refusals = 0
            broader_refusals = 0
            total = 0
            eng_narrow_scores = []
            eng_broader_scores = []
            for r in records:
                if r['condition'] != cond:
                    continue
                response_text = r.get('response_text', '') or ''
                score = r['score']
                if score is None:
                    continue
                total += 1
                if is_refusal_narrow(response_text):
                    narrow_refusals += 1
                else:
                    eng_narrow_scores.append(score)
                if is_refusal_broader(response_text):
                    broader_refusals += 1
                else:
                    eng_broader_scores.append(score)
            per_cond[cond] = {
                'total_judgments': total,
                'narrow_refusals': narrow_refusals,
                'narrow_refusal_rate': narrow_refusals / total if total else 0,
                'broader_refusals': broader_refusals,
                'broader_refusal_rate': broader_refusals / total if total else 0,
                'engagement_narrow_n': len(eng_narrow_scores),
                'engagement_narrow_mean': statistics.mean(eng_narrow_scores) if eng_narrow_scores else None,
                'engagement_broader_n': len(eng_broader_scores),
                'engagement_broader_mean': statistics.mean(eng_broader_scores) if eng_broader_scores else None,
            }
        out[subject] = per_cond
    return out


def aggregate(per_subject):
    """Subject-level mean (equal weight per subject)."""
    by_cond = defaultdict(lambda: {
        'subjects': 0,
        'narrow_refusal_rates': [],
        'broader_refusal_rates': [],
        'engagement_narrow_means': [],
        'engagement_broader_means': [],
    })
    for subject, by_cond_dict in per_subject.items():
        for cond, v in by_cond_dict.items():
            agg = by_cond[cond]
            agg['subjects'] += 1
            agg['narrow_refusal_rates'].append(v['narrow_refusal_rate'])
            agg['broader_refusal_rates'].append(v['broader_refusal_rate'])
            if v['engagement_narrow_mean'] is not None:
                agg['engagement_narrow_means'].append(v['engagement_narrow_mean'])
            if v['engagement_broader_mean'] is not None:
                agg['engagement_broader_means'].append(v['engagement_broader_mean'])
    result = {}
    for cond, agg in by_cond.items():
        result[cond] = {
            'subjects': agg['subjects'],
            'mean_narrow_refusal_rate': statistics.mean(agg['narrow_refusal_rates']),
            'mean_broader_refusal_rate': statistics.mean(agg['broader_refusal_rates']),
            'mean_engagement_narrow_score': statistics.mean(agg['engagement_narrow_means']) if agg['engagement_narrow_means'] else None,
            'mean_engagement_broader_score': statistics.mean(agg['engagement_broader_means']) if agg['engagement_broader_means'] else None,
        }
    return result


def write_report(per_subject, agg):
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        '# Engagement-conditional Δ_spec analysis',
        '',
        '_Generated by `scripts/engagement_conditional_delta.py`. Supplementary data: `engagement_conditional_delta.json`._',
        '',
        '## Question',
        '',
        'The 1-5 rubric anchors refusals at 1 (same as actively wrong predictions).',
        'The honest partition of the aggregate Δ_spec is:',
        '',
        '- **Refusal rate** — what fraction of responses are refusals per condition?',
        '- **Engagement-conditional mean** — given the model engages (non-refusal), what is the mean judge score?',
        '',
        'Recoding refusals to 2.5 is methodologically wrong: a refusal carries zero behavioral',
        'information about the subject, while a 2.5 score claims partial capture of the subject\'s',
        'behavioral pattern. The two failure modes are not equivalent.',
        '',
        '## Aggregate (mean across 14 subjects)',
        '',
        '### Refusal rates by condition',
        '',
        '| Condition | Narrow rate | Broader rate |',
        '|---|---:|---:|',
    ]
    order = ['C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
             'C4_factdump', 'C4a_full_facts_plus_spec']
    for cond in order:
        if cond not in agg:
            continue
        v = agg[cond]
        lines.append(
            f'| {cond} | {v["mean_narrow_refusal_rate"]*100:.1f}% | '
            f'{v["mean_broader_refusal_rate"]*100:.1f}% |'
        )
    lines += [
        '',
        '### Engagement-conditional mean score (non-refusal responses only)',
        '',
        '| Condition | Mean (narrow-exclude) | Mean (broader-exclude) |',
        '|---|---:|---:|',
    ]
    for cond in order:
        if cond not in agg:
            continue
        v = agg[cond]
        n = v['mean_engagement_narrow_score']
        b = v['mean_engagement_broader_score']
        lines.append(
            f'| {cond} | {n:.3f} | {b:.3f} |'
        )

    # Δ vs C5
    c5 = agg.get('C5_baseline', {})
    if c5:
        lines += [
            '',
            '### Δ (condition − C5_baseline) on the engagement-conditional means',
            '',
            '| Condition | Δ (narrow) | Δ (broader) |',
            '|---|---:|---:|',
        ]
        for cond in order:
            if cond == 'C5_baseline' or cond not in agg:
                continue
            v = agg[cond]
            n_delta = v['mean_engagement_narrow_score'] - c5['mean_engagement_narrow_score']
            b_delta = v['mean_engagement_broader_score'] - c5['mean_engagement_broader_score']
            lines.append(
                f'| {cond} | {n_delta:+.3f} | {b_delta:+.3f} |'
            )

    lines += [
        '',
        '## Per-subject — narrow classifier',
        '',
        '| Subject | C5 rate / eng-mean | C2a rate / eng-mean | Δ eng | C4a rate / eng-mean | Δ eng facts+spec |',
        '|---|---|---|---:|---|---:|',
    ]
    for subject in sorted(per_subject, key=lambda s: per_subject[s]['C5_baseline']['engagement_narrow_mean'] or 0):
        v = per_subject[subject]
        c5v = v['C5_baseline']
        c2av = v['C2a_full_spec']
        c4av = v['C4a_full_facts_plus_spec']
        c5_eng = c5v['engagement_narrow_mean']
        c2a_eng = c2av['engagement_narrow_mean']
        c4a_eng = c4av['engagement_narrow_mean']
        if c5_eng is None or c2a_eng is None:
            continue
        d_spec = c2a_eng - c5_eng
        d_all = (c4a_eng - c5_eng) if c4a_eng is not None else None
        d_all_str = f'{d_all:+.2f}' if d_all is not None else 'n/a'
        c4a_rate = c4av['narrow_refusal_rate']*100
        c4a_mean = c4a_eng if c4a_eng is not None else float('nan')
        lines.append(
            f'| {subject} | {c5v["narrow_refusal_rate"]*100:.0f}% / {c5_eng:.2f} | '
            f'{c2av["narrow_refusal_rate"]*100:.0f}% / {c2a_eng:.2f} | {d_spec:+.2f} | '
            f'{c4a_rate:.0f}% / {c4a_mean:.2f} | {d_all_str} |'
        )
    lines += [
        '',
        '## Per-subject — broader classifier',
        '',
        '| Subject | C5 rate / eng-mean | C2a rate / eng-mean | Δ eng | C4a rate / eng-mean | Δ eng facts+spec |',
        '|---|---|---|---:|---|---:|',
    ]
    for subject in sorted(per_subject, key=lambda s: per_subject[s]['C5_baseline']['engagement_broader_mean'] or 0):
        v = per_subject[subject]
        c5v = v['C5_baseline']
        c2av = v['C2a_full_spec']
        c4av = v['C4a_full_facts_plus_spec']
        c5_eng = c5v['engagement_broader_mean']
        c2a_eng = c2av['engagement_broader_mean']
        c4a_eng = c4av['engagement_broader_mean']
        if c5_eng is None or c2a_eng is None:
            continue
        d_spec = c2a_eng - c5_eng
        d_all = (c4a_eng - c5_eng) if c4a_eng is not None else None
        d_all_str = f'{d_all:+.2f}' if d_all is not None else 'n/a'
        c4a_rate = c4av['broader_refusal_rate']*100
        c4a_mean = c4a_eng if c4a_eng is not None else float('nan')
        lines.append(
            f'| {subject} | {c5v["broader_refusal_rate"]*100:.0f}% / {c5_eng:.2f} | '
            f'{c2av["broader_refusal_rate"]*100:.0f}% / {c2a_eng:.2f} | {d_spec:+.2f} | '
            f'{c4a_rate:.0f}% / {c4a_mean:.2f} | {d_all_str} |'
        )

    lines += [
        '',
        '## Interpretation',
        '',
        'The two-metric partition separates the spec\'s refusal-reducing effect from its',
        'engagement-conditional prediction improvement. Paper should report both:',
        '',
        '- **Refusal-rate drop** (this is already H1, preserved and strengthened).',
        '- **Engagement-conditional Δ_spec** (new — the prediction-accuracy claim, tested on responses where the model actually engaged).',
        '',
        'If the engagement-conditional Δ is near zero, the paper\'s aggregate Δ_spec is',
        'almost entirely refusal-rate reduction — valuable in itself but a narrower claim than',
        '"the spec produces more accurate predictions." If the engagement-conditional Δ is',
        'substantial, both claims hold independently.',
    ]
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')


def main():
    print('Loading per-subject judgments...', flush=True)
    records_by_subject = {}
    missing = []
    for subject in SUBJECTS:
        records = load_per_subject_judgments(subject)
        if records is None:
            missing.append(subject)
            continue
        records_by_subject[subject] = records

    if missing:
        print(f'WARNING: missing judgments for {missing}', flush=True)

    print(f'Computing per-subject stats for {len(records_by_subject)} subjects...', flush=True)
    per_subject = compute_per_subject(records_by_subject)

    print('Aggregating...', flush=True)
    agg = aggregate(per_subject)

    print('Writing report...', flush=True)
    write_report(per_subject, agg)

    OUT_JSON.write_text(json.dumps({
        'per_subject': per_subject,
        'aggregate': agg,
    }, indent=2), encoding='utf-8')

    print(f'Wrote: {OUT_MD}', flush=True)
    print(f'Wrote: {OUT_JSON}', flush=True)


if __name__ == '__main__':
    main()
