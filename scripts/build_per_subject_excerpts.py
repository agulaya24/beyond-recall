"""
Per-subject excerpts builder for Beyond Recall v11 Appendix E.

For each of the 14 main-study subjects, picks the 3 paired (C5, C4a) questions
with the largest C4a - C5 panel-mean Delta, where both C5 and C4a responses are
present and non-empty. Renders a markdown appendix and saves the underlying raw
data to a JSON file for reproducibility.

Aggregation: 5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54).
Per-question score = simple mean across the 5 primary judges (require >=3
valid). Subject baseline = mean over questions of the per-question C5 5-judge
primary mean (matches the §4.1 baseline column).

Outputs:
  docs/research/per_subject_excerpts_20260428.json    (raw data)
  prints the markdown body (Appendix E content) to stdout

The caller (this script's __main__) writes the markdown body to a temporary
file `docs/research/_per_subject_excerpts_appendix_body.md` and the appendix
is then inserted into the paper by a separate edit step.
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_JSON = REPO / 'docs' / 'research' / 'per_subject_excerpts_20260428.json'
OUT_MD = REPO / 'docs' / 'research' / '_per_subject_excerpts_appendix_body.md'

sys.path.insert(0, str(REPO / 'scripts'))
from recompute_5judge_primary import load_hamerton_judgments  # noqa: E402

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

# Subject order (low-baseline first, then mid-baseline) per spec.
SUBJECT_ORDER = [
    'hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
    'bernal_diaz', 'keckley', 'yung_wing', 'babur',
    'augustine', 'cellini', 'equiano', 'rousseau', 'zitkala_sa',
]

DISPLAY_NAME = {
    'hamerton': 'Hamerton',
    'sunity_devee': 'Sunity Devee',
    'ebers': 'Ebers',
    'fukuzawa': 'Fukuzawa',
    'seacole': 'Seacole',
    'bernal_diaz': 'Bernal Diaz',
    'keckley': 'Keckley',
    'yung_wing': 'Yung Wing',
    'babur': 'Babur',
    'augustine': 'Augustine',
    'cellini': 'Cellini',
    'equiano': 'Equiano',
    'rousseau': 'Rousseau',
    'zitkala_sa': 'Zitkala-Sa',
}

HAMERTON_CANONICAL_TO_INTERNAL = {
    'C2c_wrong_spec': 'C2c_full_wrong_spec',
    'C4a_full_facts_plus_spec': 'C4a_full_all_facts_plus_spec',
}


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def subject_dir(subject: str) -> Path:
    return RESULTS / 'hamerton' if subject == 'hamerton' else RESULTS / f'global_{subject}'


def safe_load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.load(path.open('r', encoding='utf-8'))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Judgment + response loaders
# ---------------------------------------------------------------------------

def load_judgments_v2(subject: str):
    if subject == 'hamerton':
        return load_hamerton_judgments()
    return safe_load_json(subject_dir(subject) / 'judgments_v2.json') or []


def _load_responses_to_index(path: Path):
    data = safe_load_json(path)
    if not isinstance(data, list):
        return {}
    return {e['question_id']: e for e in data}


def get_response_payload(subject: str, qid: int, canonical_condition: str):
    """Return (text, question_text, held_out_passage) for one (qid, condition)."""
    sd = subject_dir(subject)
    if subject == 'hamerton':
        if canonical_condition in ('C5_baseline', 'C4_factdump'):
            idx = _load_responses_to_index(sd / 'results_harmonized.json')
            key_in_file = canonical_condition
        else:
            idx = _load_responses_to_index(sd / 'results.json')
            key_in_file = HAMERTON_CANONICAL_TO_INTERNAL.get(
                canonical_condition, canonical_condition)
    else:
        idx = _load_responses_to_index(sd / 'results_v2.json')
        key_in_file = canonical_condition

    entry = idx.get(qid)
    if not entry:
        return None, None, None
    resp_dict = entry.get('responses', {})
    cond_entry = resp_dict.get(key_in_file)
    text = None
    if isinstance(cond_entry, dict):
        text = cond_entry.get('text')
    return text, entry.get('question_text'), entry.get('held_out_passage')


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------

def per_question_means(rows, target_conditions):
    """Build {qid: {cond: mean}} for primary-panel mean, requiring >=3 valid."""
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
        if per_q:
            out[qid] = per_q
    return out


def integer_band(mean_score):
    if mean_score is None:
        return None
    if mean_score < 1.0:
        return 0
    if mean_score >= 5.0:
        return 5
    return int(mean_score)


# ---------------------------------------------------------------------------
# Sanitization + truncation
# ---------------------------------------------------------------------------

EM_DASH = '—'
EN_DASH = '–'


def sanitize(text):
    """Remove em-dashes / en-dashes, collapse whitespace, strip newlines."""
    if text is None:
        return None
    # Replace em-dash with " - " (with surrounding spaces) and en-dash with "-".
    text = text.replace(EM_DASH, ' - ').replace(EN_DASH, '-')
    # Collapse runs of whitespace (incl. newlines) into single spaces.
    text = re.sub(r'\s+', ' ', text).strip()
    return text


_SENTENCE_END = re.compile(r'[.!?](?=\s|$|["\'\)\]])')


def truncate_at_sentence(text, n):
    """Truncate to <= n chars, preferring a sentence boundary at or before n.

    If no sentence boundary is found in the first n chars, hard-cuts at n and
    appends '... [truncated]'.
    """
    if text is None:
        return None
    if len(text) <= n:
        return text
    # Find the latest sentence-end at or before index n.
    best = -1
    for m in _SENTENCE_END.finditer(text[:n + 1]):
        end = m.end()
        if end <= n:
            best = end
    if best > 0 and best >= n // 2:  # require at least half the budget
        return text[:best].rstrip() + ' [truncated]'
    return text[:n].rstrip() + '... [truncated]'


# ---------------------------------------------------------------------------
# Pick top-3 cases per subject
# ---------------------------------------------------------------------------

def pick_cases_for_subject(subject: str):
    """Return (baseline_C5_mean, list of case dicts in delta-desc order, anomaly)."""
    rows = load_judgments_v2(subject)
    if not rows:
        return None, [], f'no judgment rows for {subject}'

    per_q = per_question_means(rows, {'C5_baseline', 'C4a_full_facts_plus_spec'})

    # Subject baseline = mean across all questions of C5 per-question mean.
    c5_per_q_means = [v['C5_baseline'] for v in per_q.values()
                      if 'C5_baseline' in v]
    baseline = statistics.mean(c5_per_q_means) if c5_per_q_means else None

    # Build paired records.
    candidates = []
    for qid, conds in per_q.items():
        if 'C5_baseline' not in conds or 'C4a_full_facts_plus_spec' not in conds:
            continue
        c5 = conds['C5_baseline']
        c4a = conds['C4a_full_facts_plus_spec']
        delta = c4a - c5

        c5_text, q_text_a, hop_a = get_response_payload(subject, qid, 'C5_baseline')
        c4a_text, q_text_b, hop_b = get_response_payload(
            subject, qid, 'C4a_full_facts_plus_spec')
        question_text = q_text_a or q_text_b
        held_out = hop_a or hop_b

        if not c5_text or not c5_text.strip():
            continue
        if not c4a_text or not c4a_text.strip():
            continue

        candidates.append({
            'qid': qid,
            'question_text_raw': question_text,
            'held_out_raw': held_out,
            'c5_text_raw': c5_text,
            'c4a_text_raw': c4a_text,
            'c5_mean': c5,
            'c4a_mean': c4a,
            'delta': delta,
            'c5_band': integer_band(c5),
            'c4a_band': integer_band(c4a),
        })

    # Sort by Δ desc, then qid asc for stability.
    candidates.sort(key=lambda c: (-c['delta'], c['qid']))

    picked = candidates[:3]
    anomaly = None
    if len(picked) < 3:
        anomaly = (f'only {len(picked)} paired (C5,C4a) cases with non-empty '
                   f'responses (target: 3)')
    return baseline, picked, anomaly


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_appendix(subject_data):
    """Render the full Appendix E markdown body."""
    out = []
    out.append('## Appendix E. Selected per-subject excerpts')
    out.append('')
    out.append(
        'This appendix provides three illustrative paired (C5, C4a) cases per '
        'subject for readers wanting concrete examples of the specification\'s '
        'effect at the per-question grain. Cases are selected by largest C4a '
        'minus C5 panel-mean Δ within each subject, requiring both responses '
        'to be present and non-empty. Excerpts are truncated for readability; '
        'full responses are at `results/<subject>/results_v2.json` (or '
        '`results/hamerton/results.json` for Hamerton). Per-question scores '
        'are 5-judge primary means (haiku, sonnet, opus, gpt4o, gpt54).'
    )
    out.append('')

    for i, subj in enumerate(SUBJECT_ORDER, 1):
        info = subject_data[subj]
        baseline = info['baseline_c5']
        cases = info['cases']
        anomaly = info.get('anomaly')

        baseline_str = f'{baseline:.2f}' if baseline is not None else 'N/A'
        out.append(f'### E.{i} {DISPLAY_NAME[subj]} (baseline C5 = {baseline_str})')
        out.append('')
        if anomaly:
            out.append(f'*Note: {anomaly}.*')
            out.append('')

        for j, c in enumerate(cases, 1):
            qid = c['qid']
            delta = c['delta']
            c5 = c['c5_mean']
            c4a = c['c4a_mean']
            pre_b = c['c5_band']
            post_b = c['c4a_band']

            out.append(
                f'**Case {j}: q{qid}** '
                f'(Δ_C4a = {delta:+.2f}; C5 = {c5:.2f} to C4a = {c4a:.2f}; '
                f'band {pre_b} to {post_b})'
            )
            out.append('')
            out.append(f'*Question:* {c["question_text"]}')
            out.append('')
            if c['held_out']:
                out.append(f'*Held-out passage:* {c["held_out"]}')
                out.append('')
            out.append(f'*C5 response (no context):* {c["c5_text"]}')
            out.append('')
            out.append(f'*C4a response (facts + spec):* {c["c4a_text"]}')
            out.append('')
            if j < len(cases):
                out.append('---')
                out.append('')

        # Empty line between subjects (except after last).
        if i < len(SUBJECT_ORDER):
            out.append('')

    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    subject_data = {}
    print('Pulling cases for 14 subjects...')
    for subj in SUBJECT_ORDER:
        baseline, picked, anomaly = pick_cases_for_subject(subj)
        if baseline is None:
            print(f'  [WARN] {subj}: no baseline computed')
        else:
            if picked:
                print(f'  {subj}: baseline {baseline:.3f}, {len(picked)} cases, '
                      f'top delta = {picked[0]["delta"]:+.3f}')
            else:
                print(f'  {subj}: baseline {baseline:.3f}, 0 cases')

        # Sanitize + truncate fields for rendering and the JSON record.
        rendered_cases = []
        for c in picked:
            q_text = sanitize(c['question_text_raw']) or '(question text missing)'
            held_out = sanitize(c['held_out_raw'])
            held_out_short = truncate_at_sentence(held_out, 600) if held_out else None
            c5_text = truncate_at_sentence(sanitize(c['c5_text_raw']), 500)
            c4a_text = truncate_at_sentence(sanitize(c['c4a_text_raw']), 500)

            rendered_cases.append({
                'qid': c['qid'],
                'question_text': q_text,
                'held_out': held_out_short,
                'c5_text': c5_text,
                'c4a_text': c4a_text,
                'c5_mean': round(c['c5_mean'], 3),
                'c4a_mean': round(c['c4a_mean'], 3),
                'delta': round(c['delta'], 3),
                'c5_band': c['c5_band'],
                'c4a_band': c['c4a_band'],
                # Preserve full raw response in JSON for reproducibility.
                'c5_text_raw': c['c5_text_raw'],
                'c4a_text_raw': c['c4a_text_raw'],
                'question_text_raw': c['question_text_raw'],
                'held_out_raw': c['held_out_raw'],
            })

        subject_data[subj] = {
            'baseline_c5': round(baseline, 3) if baseline is not None else None,
            'cases': rendered_cases,
            'anomaly': anomaly,
        }

    # Write JSON.
    out = {
        'date': '2026-04-28',
        'aggregation': '5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54). Per-question score = mean across the 5 primary judges, requiring >=3 valid (non-null, non-parse-failure) primary-judge scores. Subject baseline = mean over questions of the per-question C5 mean.',
        'panel_judges': sorted(PRIMARY_JUDGES),
        'selection_rule': 'Within each subject, sort paired (C5, C4a) questions by Δ = C4a_mean - C5_mean descending; take top 3 where both C5 and C4a responses are present and non-empty. Tiebreak by qid ascending.',
        'truncation': 'Held-out passage truncated at sentence boundary at <=600 chars; C5/C4a response texts at <=500 chars. Em-dashes (U+2014) and en-dashes (U+2013) removed during sanitization.',
        'subject_order': SUBJECT_ORDER,
        'subjects': subject_data,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f'\nWrote {OUT_JSON}')

    # Render markdown.
    md = render_appendix(subject_data)
    with OUT_MD.open('w', encoding='utf-8') as f:
        f.write(md + '\n')
    print(f'Wrote {OUT_MD}')

    # Summary stats.
    total_cases = sum(len(s['cases']) for s in subject_data.values())
    print(f'\nTotal cases: {total_cases} (target: 42)')
    anomalies = [(s, d['anomaly']) for s, d in subject_data.items() if d['anomaly']]
    if anomalies:
        print('\nAnomalies:')
        for s, a in anomalies:
            print(f'  {s}: {a}')
    else:
        print('\nNo anomalies.')

    # Sanity check: print baselines vs. published §4.1.
    PUBLISHED = {
        'hamerton': 1.26, 'sunity_devee': 1.03, 'ebers': 1.02, 'fukuzawa': 1.67,
        'seacole': 1.77, 'bernal_diaz': 1.70, 'keckley': 1.84, 'yung_wing': 1.88,
        'babur': 1.76, 'augustine': 2.58, 'cellini': 2.38, 'equiano': 2.77,
        'rousseau': 2.44, 'zitkala_sa': 2.34,
    }
    print('\nBaseline cross-check vs. §4.1:')
    print(f'{"subject":<16} {"computed":>10} {"published":>10} {"diff":>7}')
    for subj in SUBJECT_ORDER:
        b = subject_data[subj]['baseline_c5']
        p = PUBLISHED.get(subj)
        diff = abs(b - p) if (b is not None and p is not None) else None
        marker = '' if (diff is not None and diff <= 0.02) else '  CHECK'
        print(f'{subj:<16} {b:>10.3f} {p:>10.2f} {diff:>7.3f}{marker}')


if __name__ == '__main__':
    main()
