"""
Pull real response examples from low-baseline subjects where the specification
produced a large anchor crossing (e.g., C5 = 1 refusal, C4a = 4 substantively
aligned). These are the callout-box examples for §4.1.

For each low-baseline subject, finds question instances where:
  - 5-judge primary mean C5 <= 1.5 (refusal-like)
  - AND 5-judge primary mean C4a >= 3.5 (substantive)

Prints the question text, ground truth passage (short), both response texts.
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

PRIMARY = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

# Low-baseline subjects in 5-judge primary ordering
LOW_BASELINE = ['ebers', 'sunity_devee', 'hamerton', 'fukuzawa', 'bernal_diaz',
                'babur', 'seacole', 'keckley', 'yung_wing']


def load_subject(subject):
    if subject == 'hamerton':
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from recompute_5judge_primary import load_hamerton_judgments
        judgments = load_hamerton_judgments()
        responses_path = RESULTS / 'hamerton' / 'results.json'
    else:
        sdir = RESULTS / f'global_{subject}'
        judgments = json.load((sdir / 'judgments_v2.json').open())
        responses_path = sdir / 'results_v2.json'

    responses = json.load(responses_path.open())
    return judgments, responses


def score_mean(rows, qid, condition, judges):
    scores = []
    for r in rows:
        if r.get('question_id') != qid:
            continue
        if r.get('condition') != condition:
            continue
        if r.get('judge') not in judges:
            continue
        s = r.get('score')
        if s and s > 0 and not r.get('parse_failure'):
            scores.append(s)
    return statistics.mean(scores) if scores else None


def find_crossings(subject):
    judgments, responses = load_subject(subject)

    # For every BP question, get C5 and C4a means on 5-judge primary
    candidates = []
    for q in responses:
        if q.get('tier') != 'behavioral_prediction':
            continue
        qid = q.get('question_id')
        if qid is None:
            continue

        c5_name = 'C5_baseline'
        c4a_name = 'C4a_full_facts_plus_spec'
        c5 = score_mean(judgments, qid, c5_name, PRIMARY)
        c4a = score_mean(judgments, qid, c4a_name, PRIMARY)

        if c5 is None or c4a is None:
            continue
        jump = c4a - c5
        if c5 <= 1.8 and c4a >= 3.0:  # broad net
            resps = q.get('responses', {})
            c5_resp = resps.get(c5_name, {}).get('text', '') if isinstance(resps.get(c5_name), dict) else ''
            c4a_resp = resps.get(c4a_name, {}).get('text', '') if isinstance(resps.get(c4a_name), dict) else ''
            candidates.append({
                'subject': subject,
                'question_id': qid,
                'question_text': q.get('question_text', ''),
                'held_out': (q.get('held_out_passage', '') or '')[:500],
                'c5_mean': c5,
                'c4a_mean': c4a,
                'jump': jump,
                'c5_response': c5_resp[:800],
                'c4a_response': c4a_resp[:800],
            })
    return candidates


def main():
    all_candidates = []
    for s in LOW_BASELINE:
        try:
            all_candidates.extend(find_crossings(s))
        except Exception as e:
            print(f'{s}: ERROR {e}')

    # Sort by jump magnitude
    all_candidates.sort(key=lambda x: -x['jump'])
    print(f'\nFound {len(all_candidates)} anchor-crossing candidates (C5<=1.8, C4a>=3.0)\n')

    # Print top 5
    print('=' * 80)
    for i, c in enumerate(all_candidates[:8]):
        print(f'\n--- Example {i+1}: {c["subject"]} Q{c["question_id"]} ---')
        print(f'Jump: {c["c5_mean"]:.2f} -> {c["c4a_mean"]:.2f} (Δ +{c["jump"]:.2f})')
        print(f'Question: {c["question_text"][:200]}')
        print(f'Held-out: {c["held_out"][:250]}')
        print(f'\nC5 response (baseline): {c["c5_response"][:400]}')
        print(f'\nC4a response (spec + facts): {c["c4a_response"][:400]}')
        print()

    out = REPO / 'docs' / 'research' / 's114_anchor_crossing_examples.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_candidates, f, indent=2, ensure_ascii=False)
    print(f'Saved: {out} ({len(all_candidates)} examples)')


if __name__ == '__main__':
    main()
