"""Compute per-question outcome distribution for low-baseline slice across C2a, C4, C8, C4a, C9.

Used as input data for Fig 4.2.1 v2 and Fig 5 v2.
Output: scripts/_per_question_outcomes_v2.json
"""
import json
import os
import statistics
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

# 9 low-baseline subjects (5-judge primary C5 <= 2.0)
SUBJECTS = ['sunity_devee', 'ebers', 'hamerton', 'fukuzawa', 'bernal_diaz',
            'babur', 'seacole', 'keckley', 'yung_wing']

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

# Condition codes as they appear in data files (varies between hamerton and globals)
CONDITION_MAP = {
    'C5':  ['C5_baseline'],
    'C2a': ['C2a_full_spec', 'C2a_fullstack_spec'],
    'C4':  ['C4_factdump'],
    'C4a': ['C4a_full_facts_plus_spec', 'C4a_full_all_facts_plus_spec', 'C4a_fullstack'],
    'C8':  ['C8_raw_corpus'],
    'C9':  ['C9_raw_corpus_plus_spec'],
}


def find_subject_dir(subj):
    if subj == 'hamerton':
        return RESULTS / 'hamerton'
    return RESULTS / f'global_{subj}'


def _normalize_records(data, implicit_judge=None):
    """Normalize various Hamerton judgment schemas into {question_id, condition, judge, score, parse_failure}."""
    out = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        qid = rec.get('question_id')
        cond = rec.get('condition')
        if qid is None or cond is None:
            continue
        if 'judge' in rec and rec['judge']:
            # Standard schema
            out.append({
                'question_id': qid, 'condition': cond,
                'judge': rec['judge'], 'score': rec.get('score'),
                'parse_failure': rec.get('parse_failure', False),
            })
        else:
            # Per-judge-score-field schema (Hamerton judgments.json, gpt54_judgments.json, etc.)
            for key, val in rec.items():
                if key in ('question_id', 'condition', 'raw_response', 'parse_failure'):
                    continue
                if not key.endswith('_score'):
                    continue
                judge_name = key[:-len('_score')]
                # gemini_pro_score -> gemini_pro, haiku_score -> haiku, gemini_score -> gemini_flash
                if judge_name == 'gemini':
                    judge_name = 'gemini_flash'
                if val is None:
                    continue
                out.append({
                    'question_id': qid, 'condition': cond,
                    'judge': judge_name, 'score': val, 'parse_failure': False,
                })
    return out


def load_records(subj):
    """Yield judgment records for a subject across all relevant files."""
    d = find_subject_dir(subj)
    if subj == 'hamerton':
        files = [
            d / 'judgments_harmonized.json',   # C4, C5 (all 7 judges)
            d / 'judgments.json',              # C2a/C2c/C3/C4a (haiku+gemini_flash per-field)
            d / 'gpt4o_judgments.json',        # standard
            d / 'gpt54_judgments.json',        # per-field gpt54_score
            d / 'gemini_pro_judgments.json',   # per-field gemini_pro_score
            d / 'opus_judgments.json',         # standard
            d / 'sonnet_judgments.json',       # standard
            d / 'c8_c9_judgments_merged.json', # C8, C9 standard
        ]
    else:
        files = [
            d / 'judgments_v2.json',
            d / 'c8_c9_judgments_merged.json',
        ]
    for fp in files:
        if not fp.exists():
            continue
        with open(fp) as f:
            data = json.load(f)
        if isinstance(data, list):
            yield from _normalize_records(data)


def per_question_means(subj):
    """Return {(cond_short, qid): mean_5j} for primary panel; judges>=3 required."""
    raw = {}
    for rec in load_records(subj):
        j = rec.get('judge')
        if j not in PRIMARY_JUDGES:
            continue
        if rec.get('parse_failure'):
            continue
        c = rec.get('condition')
        short = None
        for sc, labels in CONDITION_MAP.items():
            if c in labels:
                short = sc
                break
        if short is None:
            continue
        qid = rec.get('question_id')
        score = rec.get('score')
        if score is None:
            continue
        raw.setdefault((short, qid), {})[j] = score
    out = {}
    for (short, qid), jdict in raw.items():
        if len(jdict) >= 3:
            out[(short, qid)] = sum(jdict.values()) / len(jdict)
    return out


def main():
    result = {}
    for cond in ('C2a', 'C4', 'C4a', 'C8', 'C9'):
        improved = tied = worsened = 0
        deltas_improved = []
        deltas_worsened = []
        all_deltas = []
        per_subj_counts = {}
        for subj in SUBJECTS:
            means = per_question_means(subj)
            qids = sorted({q for (c, q) in means if c == 'C5'} &
                          {q for (c, q) in means if c == cond})
            per_subj_counts[subj] = len(qids)
            for qid in qids:
                base = means[('C5', qid)]
                v = means[(cond, qid)]
                d = v - base
                all_deltas.append(d)
                if d > 1e-9:
                    improved += 1
                    deltas_improved.append(d)
                elif d < -1e-9:
                    worsened += 1
                    deltas_worsened.append(d)
                else:
                    tied += 1
        total = improved + tied + worsened
        result[cond] = {
            'total': total,
            'improved': improved,
            'tied': tied,
            'worsened': worsened,
            'improved_pct': 100 * improved / total if total else 0,
            'tied_pct': 100 * tied / total if total else 0,
            'worsened_pct': 100 * worsened / total if total else 0,
            'median_imp': statistics.median(deltas_improved) if deltas_improved else None,
            'median_wor': statistics.median(deltas_worsened) if deltas_worsened else None,
            'mean_delta': statistics.mean(all_deltas) if all_deltas else None,
            'per_subject_qcount': per_subj_counts,
        }
    for c in ('C8', 'C2a', 'C4', 'C4a', 'C9'):
        r = result[c]
        print(f"{c}: total={r['total']:3d}  "
              f"improved={r['improved']:3d} ({r['improved_pct']:.1f}%)  "
              f"tied={r['tied']:3d} ({r['tied_pct']:.1f}%)  "
              f"worsened={r['worsened']:3d} ({r['worsened_pct']:.1f}%)  "
              f"median_imp={r['median_imp']}  median_wor={r['median_wor']}  "
              f"mean_delta={r['mean_delta']:+.3f}")
    out = REPO / 'scripts' / '_per_question_outcomes_v2.json'
    with open(out, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out}")


if __name__ == '__main__':
    main()
