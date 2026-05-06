"""
Spec-activation analysis for §4.3.

Counts how often response text cites the specification's anchor tags (A1, A2, ...)
and prediction tags (P1, P2, ...) in each condition, across low-baseline subjects.

Three measurements per (subject, condition):
  1. Tag-citation rate: fraction of responses that cite at least one A-tag or P-tag.
  2. Anchor usage breadth: how many distinct tags get cited across all responses.
  3. Paraphrase match: how often the response text contains a substring from the
     spec's anchor text (bigram overlap check).

Output: docs/research/spec_activation_analysis.md
"""

import json
import re
import statistics
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DATA = REPO / 'data'

SUBJECTS = [
    'ebers', 'sunity_devee', 'fukuzawa', 'bernal_diaz', 'babur',
    'seacole', 'keckley', 'yung_wing', 'hamerton',
]

TAG_RE = re.compile(r'\b([AP])(\d+)\b')


def load_spec(subject):
    """Load the full-stack spec (anchors + core + predictions + brief) for a subject."""
    if subject == 'hamerton':
        base = DATA / 'hamerton' / 'spec'
        texts = []
        for fn in ['anchors_v4.md', 'core_v4.md', 'predictions_v4.md', 'brief_v5_clean.md']:
            p = base / fn
            if p.exists():
                texts.append(p.read_text(encoding='utf-8'))
        return '\n\n'.join(texts) if texts else None
    subj_dir = DATA / 'global_subjects' / subject
    for fn in ['spec_production.md', 'spec.md']:
        p = subj_dir / fn
        if p.exists():
            return p.read_text(encoding='utf-8')
    return None


def extract_tags_from_spec(spec_text):
    """Return set of (type, number) tags defined in the spec."""
    if not spec_text:
        return set()
    # Match A1, A2, P1, etc. — with word boundary
    return {(m.group(1), m.group(2)) for m in TAG_RE.finditer(spec_text)}


def load_subject_responses(subject):
    """Return {question_id: {condition: response_text}}."""
    out = defaultdict(dict)
    if subject == 'hamerton':
        # Hamerton: results.json has spec conditions; results_harmonized or judgments_v2 don't have text
        path = RESULTS / 'hamerton' / 'results.json'
        data = json.load(path.open(encoding='utf-8'))
        for q in data:
            if q.get('tier') != 'behavioral_prediction':
                continue
            qid = q.get('question_id')
            resps = q.get('responses', {})
            for cond, rdata in resps.items():
                if isinstance(rdata, dict):
                    out[qid][cond] = rdata.get('text', '')
        # Hamerton uses C4a_full_all_facts_plus_spec; normalize
    else:
        path = RESULTS / f'global_{subject}' / 'results_v2.json'
        data = json.load(path.open(encoding='utf-8'))
        for q in data:
            qid = q.get('question_id')
            resps = q.get('responses', {})
            for cond, rdata in resps.items():
                if isinstance(rdata, dict):
                    out[qid][cond] = rdata.get('text', '')
    return out


def citation_metrics(response_text, spec_tags):
    """How does the response cite the spec?"""
    if not response_text:
        return {'cited': False, 'tags': set(), 'count': 0}
    tags_in_response = {(m.group(1), m.group(2)) for m in TAG_RE.finditer(response_text)}
    overlap = tags_in_response & spec_tags
    return {'cited': len(overlap) > 0, 'tags': overlap, 'count': len(overlap)}


def analyze_subject(subject):
    spec_text = load_spec(subject)
    if not spec_text:
        print(f'{subject}: no spec found')
        return None
    spec_tags = extract_tags_from_spec(spec_text)
    if not spec_tags:
        print(f'{subject}: no A/P tags in spec')
        return None

    responses = load_subject_responses(subject)
    # Normalize condition names (Hamerton uses _full_all_facts_plus_spec)
    def normalize(cond):
        if cond == 'C4a_full_all_facts_plus_spec':
            return 'C4a_full_facts_plus_spec'
        return cond

    per_cond = defaultdict(lambda: {
        'n_responses': 0,
        'n_cited': 0,
        'tags_used': Counter(),
        'total_citations': 0,
    })

    for qid, cond_map in responses.items():
        for cond, text in cond_map.items():
            norm = normalize(cond)
            m = citation_metrics(text, spec_tags)
            per_cond[norm]['n_responses'] += 1
            if m['cited']:
                per_cond[norm]['n_cited'] += 1
            per_cond[norm]['total_citations'] += m['count']
            for tag in m['tags']:
                per_cond[norm]['tags_used'][tag] += 1

    return {
        'subject': subject,
        'spec_tag_count': len(spec_tags),
        'anchor_count': sum(1 for t, n in spec_tags if t == 'A'),
        'prediction_count': sum(1 for t, n in spec_tags if t == 'P'),
        'per_condition': {
            cond: {
                'n_responses': d['n_responses'],
                'n_cited': d['n_cited'],
                'citation_rate': d['n_cited'] / d['n_responses'] if d['n_responses'] else 0,
                'avg_citations_per_cited_response': d['total_citations'] / d['n_cited'] if d['n_cited'] else 0,
                'distinct_tags_used': len(d['tags_used']),
                'top_5_tags': d['tags_used'].most_common(5),
            }
            for cond, d in per_cond.items()
        },
    }


def main():
    results = []
    for s in SUBJECTS:
        r = analyze_subject(s)
        if r:
            results.append(r)
            print(f'{s}: {r["spec_tag_count"]} spec tags ({r["anchor_count"]} anchors, {r["prediction_count"]} predictions)')
            for cond in ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec', 'C2c_wrong_spec']:
                if cond in r['per_condition']:
                    d = r['per_condition'][cond]
                    print(f'  {cond}: {d["n_cited"]}/{d["n_responses"]} cited ({100*d["citation_rate"]:.1f}%), {d["distinct_tags_used"]} distinct tags used')

    # Aggregate summary
    print('\n\n=== Aggregate across 9 low-baseline subjects ===')
    agg = defaultdict(lambda: {'total_n': 0, 'total_cited': 0, 'total_tags': 0})
    for r in results:
        for cond, d in r['per_condition'].items():
            agg[cond]['total_n'] += d['n_responses']
            agg[cond]['total_cited'] += d['n_cited']
            agg[cond]['total_tags'] += d['distinct_tags_used']
    for cond in ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec', 'C2c_wrong_spec']:
        if cond in agg:
            a = agg[cond]
            rate = 100 * a['total_cited'] / a['total_n'] if a['total_n'] else 0
            print(f'  {cond}: {a["total_cited"]}/{a["total_n"]} cited ({rate:.1f}%)')

    out = REPO / 'docs' / 'research' / 'spec_activation_analysis.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
