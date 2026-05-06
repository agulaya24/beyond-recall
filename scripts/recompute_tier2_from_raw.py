"""
Recompute Tier 2 deltas from raw per-judge judgment files.

Resolves the three-way disagreement between DATA_REFERENCE §10,
RESULTS_S113.json, and PROVENANCE_INDEX.md.

For each (subject × response model) cell, aggregate C5 and C4a scores
and compute Δ = mean(C4a) - mean(C5).

Reports both the 5-judge primary aggregate and the 7-judge sensitivity.
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TIER2_DIR = REPO / 'results' / '_tier2'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
GEMINI_JUDGES = {'gemini_flash', 'gemini_pro'}

SUBJECTS = ['ebers', 'yung_wing', 'zitkala_sa']
RESPONSE_MODELS = ['sonnet', 'gemini_pro']


def load_judgments(subject, response_model):
    """Load all judgment rows for (subject, response_model)."""
    subj_dir = TIER2_DIR / f'global_{subject}'
    if not subj_dir.exists():
        return []
    rows = []
    for p in subj_dir.glob(f'tier2_{response_model}_judgments_*.json'):
        judge = p.stem.replace(f'tier2_{response_model}_judgments_', '')
        try:
            data = json.load(p.open(encoding='utf-8'))
        except Exception:
            try:
                data = json.load(p.open(encoding='latin-1'))
            except Exception:
                continue
        for r in data:
            if not isinstance(r, dict):
                continue
            score = r.get('score')
            if r.get('parse_failure') or score in (0, None):
                continue
            rows.append({
                'question_id': r.get('question_id'),
                'condition': r.get('condition'),
                'judge': judge,
                'score': score,
            })
    return rows


def aggregate(rows, judge_set):
    """Return {condition: mean_score} computed via within-judge then across-judge mean."""
    per_jc = defaultdict(list)  # (condition, judge) -> [scores]
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])
    per_cond = defaultdict(list)
    for (cond, judge), scores in per_jc.items():
        if scores:
            per_cond[cond].append(statistics.mean(scores))
    return {c: statistics.mean(ms) for c, ms in per_cond.items() if ms}


def main():
    print('\n=== Tier 2 recompute (raw data) ===\n')
    print(f'{"subject":<14} {"resp_model":<12} {"panel":<12} {"C5":>6} {"C2a":>6} {"C4a":>6} {"d_c2a":>8} {"d_c4a":>8}')
    print('-' * 80)

    results = []

    for subject in SUBJECTS:
        for model in RESPONSE_MODELS:
            rows = load_judgments(subject, model)
            if not rows:
                print(f'{subject:<14} {model:<12} NO DATA')
                continue
            judge_cov = set(r['judge'] for r in rows)
            # Primary 5-judge
            prim = aggregate(rows, PRIMARY_JUDGES)
            # 7-judge sensitivity (everything available)
            full = aggregate(rows, PRIMARY_JUDGES | GEMINI_JUDGES)

            for label, agg in [('5-judge', prim), ('7-judge', full)]:
                c5 = agg.get('C5_baseline') or agg.get('C5')
                c2a = agg.get('C2a_full_spec') or agg.get('C2a')
                c4a = agg.get('C4a_full_facts_plus_spec') or agg.get('C4a')
                if c5 is None or c4a is None:
                    print(f'{subject:<14} {model:<12} {label:<12} missing conditions ({list(agg.keys())})')
                    continue
                d_c2a = (c2a - c5) if c2a is not None else None
                d_c4a = c4a - c5
                ds = f'{d_c2a:+.2f}' if d_c2a is not None else '  ---'
                print(f'{subject:<14} {model:<12} {label:<12} {c5:>6.2f} {(c2a or 0):>6.2f} {c4a:>6.2f} {ds:>8} {d_c4a:>+8.2f}')
                results.append({
                    'subject': subject,
                    'response_model': model,
                    'panel': label,
                    'judges_available': sorted(judge_cov),
                    'c5': c5, 'c2a': c2a, 'c4a': c4a,
                    'delta_c2a': d_c2a, 'delta_c4a': d_c4a,
                })

    out = REPO / 'docs' / 'research' / 'tier2_recompute_s114.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
