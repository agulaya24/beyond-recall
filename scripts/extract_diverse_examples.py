"""
Extract a diverse set of response examples for §4.1 callouts.

Three kinds of comparisons per subject:
  (A) C5 baseline vs. C4a (facts + spec) — the big jump story.
  (B) C4 (facts alone) vs. C4a (facts + spec) — what does the spec ADD on top of raw facts?
  (C) C2a (spec alone) vs. C4a (facts + spec) — what do facts add on top of spec?

Selects the examples with the cleanest separation on each comparison.
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

PRIMARY = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

LOW_BASELINE = ['ebers', 'sunity_devee', 'fukuzawa', 'bernal_diaz',
                'babur', 'seacole', 'keckley', 'yung_wing']


def per_q_score(judgments, qid, condition):
    scores = []
    for r in judgments:
        if r.get('judge') not in PRIMARY:
            continue
        if r.get('question_id') != qid:
            continue
        if r.get('condition') != condition:
            continue
        s = r.get('score')
        if s and s > 0 and not r.get('parse_failure'):
            scores.append(s)
    return statistics.mean(scores) if scores else None


def extract_for_subject(subject):
    sdir = RESULTS / f'global_{subject}'
    try:
        judgments = json.load((sdir / 'judgments_v2.json').open())
        responses = json.load((sdir / 'results_v2.json').open())
    except Exception:
        return []

    # Collect per-question means per condition (globals' results_v2.json is BP-only by construction)
    per_q = defaultdict(dict)
    for q in responses:
        qid = q['question_id']
        for cond in ['C5_baseline', 'C2a_full_spec', 'C4_factdump', 'C4a_full_facts_plus_spec']:
            m = per_q_score(judgments, qid, cond)
            if m is not None:
                per_q[qid][cond] = m

    comparisons = []
    for q in responses:
        qid = q.get('question_id')
        if qid not in per_q:
            continue
        scores = per_q[qid]
        resps = q.get('responses', {})

        def safe_resp(cond):
            r = resps.get(cond, {})
            return r.get('text', '')[:900] if isinstance(r, dict) else ''

        def entry(kind, low, high):
            return {
                'kind': kind,
                'subject': subject,
                'question_id': qid,
                'question_text': q.get('question_text', '')[:400],
                'held_out': (q.get('held_out_passage') or '')[:400],
                'low_cond': low,
                'high_cond': high,
                'low_score': scores.get(low),
                'high_score': scores.get(high),
                'jump': scores.get(high) - scores.get(low) if scores.get(low) and scores.get(high) else 0,
                'low_text': safe_resp(low),
                'high_text': safe_resp(high),
            }

        # (A) C5 vs C4a
        if 'C5_baseline' in scores and 'C4a_full_facts_plus_spec' in scores:
            comparisons.append(entry('A_baseline_vs_factsspec', 'C5_baseline', 'C4a_full_facts_plus_spec'))
        # (B) C4 vs C4a
        if 'C4_factdump' in scores and 'C4a_full_facts_plus_spec' in scores:
            comparisons.append(entry('B_facts_vs_factsspec', 'C4_factdump', 'C4a_full_facts_plus_spec'))
        # (C) C2a vs C4a
        if 'C2a_full_spec' in scores and 'C4a_full_facts_plus_spec' in scores:
            comparisons.append(entry('C_speconly_vs_factsspec', 'C2a_full_spec', 'C4a_full_facts_plus_spec'))

    return comparisons


def main():
    all_cmp = []
    for s in LOW_BASELINE:
        all_cmp.extend(extract_for_subject(s))

    by_kind = defaultdict(list)
    for c in all_cmp:
        by_kind[c['kind']].append(c)

    for kind in ['A_baseline_vs_factsspec', 'B_facts_vs_factsspec', 'C_speconly_vs_factsspec']:
        rows = by_kind[kind]
        rows.sort(key=lambda x: -x['jump'])
        print(f'\n===== {kind} =====')
        for r in rows[:5]:
            if r['jump'] < 0.5:
                break
            print(f'\n--- {r["subject"]} Q{r["question_id"]}: {r["low_cond"]}={r["low_score"]:.2f} -> {r["high_cond"]}={r["high_score"]:.2f} (Δ +{r["jump"]:.2f}) ---')
            print(f'Q: {r["question_text"][:160]}')
            print(f'Held-out: {r["held_out"][:200]}')
            print(f'LOW ({r["low_cond"]}): {r["low_text"][:300]}')
            print(f'HIGH ({r["high_cond"]}): {r["high_text"][:300]}')

    out = REPO / 'docs' / 'research' / 's114_diverse_examples.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(by_kind, f, indent=2, ensure_ascii=False)
    print(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
