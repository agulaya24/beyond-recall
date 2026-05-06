"""
Validity audit for the low-end of the rubric.

Questions:
  1. Are abstention-like responses being scored 1 (refusal) or 2-3 (partial)?
  2. Does response length correlate with score independent of content?
  3. Which judges are most lenient on low-end responses?
  4. Are ultra-high scores (4.5-5.0) substantive or inflated?

Method: scan all low-baseline responses + scores. Classify abstention-like
responses by phrase patterns. Compare score distribution for abstention-like
vs substantive responses. Correlate length with score.
"""

import json
import re
import statistics
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
PRIMARY = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
ALL_JUDGES = PRIMARY | {'gemini_flash', 'gemini_pro'}

LOW_BASELINE = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'bernal_diaz',
                'babur', 'seacole', 'keckley', 'yung_wing']

ABSTENTION_PATTERNS = [
    r"i don['\u2019]t have (specific|enough|detailed|direct)",
    r"there is no (specific|explicit|direct|documented)",
    r"i cannot (point to|confirm|verify|provide|determine)",
    r"i am (not|unable) (able|certain|sure)",
    r"would need (additional|more|further|specific)",
    r"no (specific|explicit|direct) (information|account|passage|reference)",
    r"i['\u2019]m not (aware|familiar)",
    r"without (more|additional|specific) (context|information|details)",
    r"i (do not|don['\u2019]t) (recall|know)",
    r"(cannot|unable to) (accurately|reliably) (answer|predict|characterize)",
    r"my training data does not",
    r"no specific documented",
]


def is_abstention(text):
    if not text:
        return False
    t = text.lower()
    for pattern in ABSTENTION_PATTERNS:
        if re.search(pattern, t):
            return True
    return False


def load_global(subject):
    if subject == 'hamerton':
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from recompute_5judge_primary import load_hamerton_judgments
        j = load_hamerton_judgments()
        responses_path = RESULTS / 'hamerton' / 'results.json'
    else:
        sdir = RESULTS / f'global_{subject}'
        j = json.load((sdir / 'judgments_v2.json').open(encoding='utf-8'))
        responses_path = sdir / 'results_v2.json'
    responses = json.load(responses_path.open(encoding='utf-8'))
    return j, responses


def per_q_score(judgments, qid, condition, judge_set):
    scores_by_judge = defaultdict(list)
    for r in judgments:
        if r.get('judge') not in judge_set:
            continue
        if r.get('question_id') != qid:
            continue
        if r.get('condition') != condition:
            continue
        s = r.get('score')
        if s and s > 0 and not r.get('parse_failure'):
            scores_by_judge[r['judge']].append(s)
    judge_means = [statistics.mean(ss) for ss in scores_by_judge.values()]
    return statistics.mean(judge_means) if judge_means else None, scores_by_judge


def main():
    all_rows = []  # (subject, qid, condition, text, length, primary_mean, per-judge scores, is_abstention)

    for subject in LOW_BASELINE:
        try:
            j, responses = load_global(subject)
        except Exception as e:
            print(f'{subject}: load error {e}')
            continue

        for q in responses:
            qid = q.get('question_id')
            if qid is None:
                continue
            resps = q.get('responses', {})
            for cond in ['C5_baseline', 'C2a_full_spec', 'C4_factdump',
                         'C4a_full_facts_plus_spec', 'C2c_wrong_spec']:
                rdata = resps.get(cond, {})
                text = rdata.get('text', '') if isinstance(rdata, dict) else ''
                if not text:
                    continue
                primary_mean, per_judge = per_q_score(j, qid, cond, PRIMARY)
                if primary_mean is None:
                    continue
                all_rows.append({
                    'subject': subject,
                    'qid': qid,
                    'condition': cond,
                    'length': len(text),
                    'primary_mean': primary_mean,
                    'per_judge': {k: statistics.mean(v) for k, v in per_judge.items()},
                    'is_abstention': is_abstention(text),
                    'text_head': text[:200],
                })

    print(f'\nTotal responses analyzed: {len(all_rows)}\n')

    # 1. Abstention frequency + score distribution
    abs_rows = [r for r in all_rows if r['is_abstention']]
    non_abs = [r for r in all_rows if not r['is_abstention']]
    print(f'Abstention-pattern matches: {len(abs_rows)} / {len(all_rows)} ({100*len(abs_rows)/len(all_rows):.1f}%)')
    print(f'Mean 5-judge primary score:')
    print(f'  Abstention-like: {statistics.mean(r["primary_mean"] for r in abs_rows):.2f} (expected: close to 1.0)')
    print(f'  Non-abstention:  {statistics.mean(r["primary_mean"] for r in non_abs):.2f}')

    # Distribution of abstention scores
    print(f'\nScore distribution for abstention-like responses:')
    bands = {'1.0-1.5': 0, '1.5-2.0': 0, '2.0-2.5': 0, '2.5-3.0': 0, '3.0-3.5': 0, '3.5+': 0}
    for r in abs_rows:
        s = r['primary_mean']
        if s < 1.5: bands['1.0-1.5'] += 1
        elif s < 2.0: bands['1.5-2.0'] += 1
        elif s < 2.5: bands['2.0-2.5'] += 1
        elif s < 3.0: bands['2.5-3.0'] += 1
        elif s < 3.5: bands['3.0-3.5'] += 1
        else: bands['3.5+'] += 1
    for b, n in bands.items():
        pct = 100*n/len(abs_rows) if abs_rows else 0
        print(f'  {b}: {n} ({pct:.1f}%)')

    # Flagged: abstention responses scoring above 2.0 (should be <= 1.5 if rubric is clean)
    flagged = [r for r in abs_rows if r['primary_mean'] >= 2.0]
    print(f'\nFlagged: {len(flagged)} abstention responses scoring >= 2.0 on 5-judge primary')
    print(f'(Expected: 0 if rubric cleanly distinguishes refusal from prediction)')

    # 2. Length correlation
    try:
        from scipy import stats as sp
        lengths = [r['length'] for r in all_rows]
        scores = [r['primary_mean'] for r in all_rows]
        corr, p = sp.pearsonr(lengths, scores)
        print(f'\nLength-score correlation (all {len(all_rows)} responses): r = {corr:.3f}, p = {p:.3e}')
        # Per condition
        print('\nPer-condition length-score correlation:')
        for cond in ['C5_baseline', 'C2a_full_spec', 'C4_factdump', 'C4a_full_facts_plus_spec']:
            cond_rows = [r for r in all_rows if r['condition'] == cond]
            if len(cond_rows) >= 10:
                corr, p = sp.pearsonr([r['length'] for r in cond_rows], [r['primary_mean'] for r in cond_rows])
                print(f'  {cond}: r = {corr:.3f} (n={len(cond_rows)})')
    except ImportError:
        print('scipy not available; skipping correlation')

    # 3. Per-judge inflation on abstention-like responses
    print('\nPer-judge means on abstention-like responses (should be near 1.0 if judges are strict):')
    per_judge_on_abs = defaultdict(list)
    for r in abs_rows:
        for judge, score in r['per_judge'].items():
            per_judge_on_abs[judge].append(score)
    for judge in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']:
        if judge in per_judge_on_abs:
            m = statistics.mean(per_judge_on_abs[judge])
            print(f'  {judge}: {m:.2f} (n={len(per_judge_on_abs[judge])})')

    # 4. Ultra-high scores (>= 4.5). Sample and check if substantive
    ultra_high = [r for r in all_rows if r['primary_mean'] >= 4.5]
    print(f'\nUltra-high responses (primary mean >= 4.5): {len(ultra_high)}')
    print(f'Mean length of ultra-high: {statistics.mean(r["length"] for r in ultra_high):.0f} chars')
    print(f'Mean length of mid-range (2.5-3.5): {statistics.mean(r["length"] for r in all_rows if 2.5 <= r["primary_mean"] < 3.5):.0f} chars')
    print(f'Mean length of low-range (<2.0): {statistics.mean(r["length"] for r in all_rows if r["primary_mean"] < 2.0):.0f} chars')

    # Save full audit
    out = REPO / 'docs' / 'research' / 's114_low_end_inflation_audit.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({
            'flagged_abstention_above_2': [{k: v for k, v in r.items() if k != 'per_judge'} for r in flagged],
            'total_responses': len(all_rows),
            'abstention_count': len(abs_rows),
            'abstention_mean_score': statistics.mean(r['primary_mean'] for r in abs_rows),
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f'\nSaved: {out}')

    # Show a few flagged examples
    print(f'\n--- Sample of 5 most-inflated abstentions ---')
    flagged_sorted = sorted(flagged, key=lambda r: -r['primary_mean'])[:5]
    for r in flagged_sorted:
        print(f'\n{r["subject"]} Q{r["qid"]} {r["condition"]}: primary={r["primary_mean"]:.2f}, len={r["length"]}')
        print(f'  per-judge: {r["per_judge"]}')
        print(f'  text: {r["text_head"][:300]}')


if __name__ == '__main__':
    main()
