"""
DEPRECATED — superseded by scripts/classify_hedging.py.

This script uses a broader "any REFUSAL_PATTERNS hit anywhere in the
response" rule that produces 209/40/2 out of 507 (41.2% / 7.9% / 0.4%).
The paper's canonical hedging metric is now the narrower `starts_refusal`
rule defined in scripts/classify_hedging.py, which produces
146/7/0 out of 507 (28.8% / 1.4% / 0.0%). See docs/research/hedging_analysis.json
for the full provenance note.

Historical context: this script was written to try to reproduce the
v6/v7 paper numbers (127/13/3 = 25.0%/2.6%/0.6%), which could not be
reproduced from any threshold of the patterns in
docs/research/_analyze_score_bands.py. The variant sweep is in
scripts/_probe_hedge_variants.py. Kept here for historical record; do not
use for new paper figures — use classify_hedging.py.

Source responses live in:
  results/global_<subject>/results_v2.json
(39 questions each x 13 subjects = 507 per condition.)
"""

import json
import os
import re
from datetime import date

BASE = os.path.join(os.path.dirname(__file__), '..', 'results')
BASE = os.path.normpath(BASE)
OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'research', 'hedging_analysis.json')
OUT = os.path.normpath(OUT)

GLOBALS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
    'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee',
    'yung_wing', 'zitkala_sa',
]

REFUSAL_PATTERNS = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

HEDGE_PATTERNS = [
    r"\b(?:likely|probably|perhaps|possibly|might|could|may|would likely|seems?|appears?|suggest)\b",
    r"\bgenerally speaking\b",
    r"\bit is reasonable to\b",
    r"\bwe might (?:imagine|infer|conjecture)\b",
]
HEDGE_RE = re.compile("|".join(HEDGE_PATTERNS), re.IGNORECASE)

CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec']


def get_response_text(rec, condition):
    resp = rec.get('responses', {}).get(condition)
    if resp is None:
        return None
    if isinstance(resp, dict):
        return resp.get('text') or resp.get('response') or ''
    return str(resp)


def classify(text):
    return {
        'refusal_hits': len(REFUSAL_RE.findall(text)),
        'hedge_hits': len(HEDGE_RE.findall(text)),
        'starts_refusal': bool(re.match(
            r"^\s*(?:I (?:cannot|can't|don't)|The retrieved facts (?:do not|don't))",
            text, re.IGNORECASE
        )),
    }


def main():
    by_condition = {c: {'hedged': 0, 'total': 0, 'hedge_only': 0,
                        'starts_refusal': 0} for c in CONDITIONS}
    per_subject = {}

    for subj in GLOBALS:
        path = os.path.join(BASE, f'global_{subj}', 'results_v2.json')
        recs = json.load(open(path, encoding='utf-8'))
        per_subject[subj] = {c: {'hedged': 0, 'total': 0} for c in CONDITIONS}
        for rec in recs:
            for cond in CONDITIONS:
                text = get_response_text(rec, cond)
                if text is None:
                    continue
                by_condition[cond]['total'] += 1
                per_subject[subj][cond]['total'] += 1
                feats = classify(text)
                if feats['refusal_hits'] >= 1:
                    by_condition[cond]['hedged'] += 1
                    per_subject[subj][cond]['hedged'] += 1
                if feats['hedge_hits'] >= 1:
                    by_condition[cond]['hedge_only'] += 1
                if feats['starts_refusal']:
                    by_condition[cond]['starts_refusal'] += 1

    print(f'{"condition":<32} {"hedged":>8} {"total":>8} {"rate":>8}  | hedge_loose starts_refusal')
    for c in CONDITIONS:
        b = by_condition[c]
        rate = b['hedged'] / b['total'] if b['total'] else 0.0
        print(f'{c:<32} {b["hedged"]:>8} {b["total"]:>8} {rate:>8.3f}  | '
              f'{b["hedge_only"]:>11} {b["starts_refusal"]:>13}')

    # Write artifact
    out = {
        'C5': {'hedged': by_condition['C5_baseline']['hedged'],
               'total': by_condition['C5_baseline']['total'],
               'rate': round(by_condition['C5_baseline']['hedged']
                             / by_condition['C5_baseline']['total'], 4)},
        'C2a': {'hedged': by_condition['C2a_full_spec']['hedged'],
                'total': by_condition['C2a_full_spec']['total'],
                'rate': round(by_condition['C2a_full_spec']['hedged']
                              / by_condition['C2a_full_spec']['total'], 4)},
        'C4a': {'hedged': by_condition['C4a_full_facts_plus_spec']['hedged'],
                'total': by_condition['C4a_full_facts_plus_spec']['total'],
                'rate': round(by_condition['C4a_full_facts_plus_spec']['hedged']
                              / by_condition['C4a_full_facts_plus_spec']['total'], 4)},
        'classifier': {
            'flagging_rule': 'refusal_hits >= 1 from REFUSAL_RE',
            'patterns_used': REFUSAL_PATTERNS,
            'hedge_patterns_secondary': HEDGE_PATTERNS,
        },
        'classifier_script': '_analyze_score_bands.py (patterns) '
                             'and scripts/compute_hedging_rates.py (counter)',
        'source_data': 'results/global_<subject>/results_v2.json, '
                       '13 subjects x 39 questions = 507 per condition',
        'subjects': GLOBALS,
        'conditions': CONDITIONS,
        'per_subject': per_subject,
        'computed_at': date.today().isoformat(),
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f'\nWrote {OUT}')


if __name__ == '__main__':
    main()
