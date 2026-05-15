"""Canonical extractor for v2-grade worked-example content.

For a given (subject, qid, condition) tuple, returns:
    - question text from battery_v2.json
    - held_out passage from battery_v2.json
    - response from results_v2.json under that question_id and condition
    - per-judge scores from judgments_v2.json filtered to that (qid, condition)
    - 5-judge primary mean and per-judge listing

This is the *single source of truth* used to verify worked examples in §4 of
the paper. Any worked example that references a (subject, qid, condition) MUST
be sourceable from this extractor; if not, the example is misaligned.

Use as a library:
    from v2_canonical_cell_extractor_20260508 import extract
    cell = extract('fukuzawa', 35, 'C4_factdump')
    print(cell['question'], cell['response'][:200], cell['primary_mean'])

Or as a CLI:
    python v2_canonical_cell_extractor_20260508.py fukuzawa 35 C4_factdump
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import mean


PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']
REPO = Path(__file__).resolve().parent.parent


def _subject_dir(subject: str) -> Path:
    """Map subject name to its results directory. global_X for globals,
    'hamerton' for the original Hamerton subject."""
    if subject == 'hamerton':
        return REPO / 'results' / 'hamerton'
    return REPO / 'results' / f'global_{subject}'


def extract(subject: str, qid: int, condition: str) -> dict:
    """Pull canonical v2 cell content. Returns a dict with question, held_out,
    response, judge_scores (per-judge), primary_mean, plus integrity flags.
    """
    base = _subject_dir(subject)
    if not base.exists():
        raise FileNotFoundError(f"Subject directory not found: {base}")

    # Battery (v2)
    battery_path = base / 'battery_v2.json'
    if not battery_path.exists():
        raise FileNotFoundError(f"battery_v2.json not found for {subject} at {battery_path}")
    battery = json.loads(battery_path.read_text(encoding='utf-8'))
    questions = battery.get('questions', battery)
    q = next((x for x in questions if x.get('id') == qid), None)
    if q is None:
        raise KeyError(f"Q{qid} not found in {battery_path}")

    question_text = q.get('text', '')
    held_out = q.get('held_out_passage', '')

    # Results (v2)
    results_path = base / 'results_v2.json'
    if not results_path.exists():
        raise FileNotFoundError(f"results_v2.json not found for {subject}")
    results = json.loads(results_path.read_text(encoding='utf-8'))
    qresult = next((r for r in results if r.get('question_id') == qid), None)
    if qresult is None:
        raise KeyError(f"Q{qid} not found in {results_path}")

    responses = qresult.get('responses', {})
    if condition not in responses:
        # Try common aliases
        aliases = {
            'C4': 'C4_factdump', 'C4_factdump': 'C4_factdump',
            'C5': 'C5_baseline', 'C5_baseline': 'C5_baseline',
            'C2a': 'C2a_full_spec', 'C2a_full_spec': 'C2a_full_spec', 'C2a_spec': 'C2a_full_spec',
            'C4a': 'C4a_full_facts_plus_spec', 'C4a_full_facts_plus_spec': 'C4a_full_facts_plus_spec',
            'C4a_facts_plus_spec': 'C4a_full_facts_plus_spec',
            'C2c': 'C2c_wrong_spec', 'C2c_wrong_spec': 'C2c_wrong_spec',
        }
        canon = aliases.get(condition, condition)
        if canon in responses:
            condition = canon
        else:
            raise KeyError(
                f"Condition {condition!r} not found in responses; "
                f"available: {list(responses.keys())}"
            )

    response_obj = responses[condition]
    if isinstance(response_obj, dict):
        response_text = response_obj.get('text') or response_obj.get('response_text') or ''
    else:
        response_text = str(response_obj)

    # Judgments
    judg_path = base / 'judgments_v2.json'
    if not judg_path.exists():
        raise FileNotFoundError(f"judgments_v2.json not found for {subject}")
    judgments = json.loads(judg_path.read_text(encoding='utf-8'))
    cell_judgments = [
        r for r in judgments
        if r.get('question_id') == qid and r.get('condition') == condition
    ]
    judge_scores = {}
    for r in cell_judgments:
        if r.get('parse_failure'):
            continue
        judge_scores[r['judge']] = r['score']

    primary = [judge_scores[j] for j in PRIMARY_JUDGES if j in judge_scores]
    primary_mean = round(mean(primary), 3) if primary else None
    primary_min = min(primary) if primary else None
    primary_max = max(primary) if primary else None
    primary_range = primary_max - primary_min if primary else None

    return {
        'subject': subject,
        'qid': qid,
        'condition': condition,
        'question': question_text,
        'held_out': held_out,
        'response': response_text,
        'judge_scores': judge_scores,
        'primary_judges': {j: judge_scores.get(j) for j in PRIMARY_JUDGES},
        'primary_mean': primary_mean,
        'primary_range': primary_range,
        'primary_n': len(primary),
        'source_files': {
            'battery': str(battery_path.relative_to(REPO)),
            'results': str(results_path.relative_to(REPO)),
            'judgments': str(judg_path.relative_to(REPO)),
        },
    }


def format_cell(cell: dict, response_chars: int = 1500) -> str:
    """Pretty-print a cell for human inspection."""
    lines = [
        f"=== {cell['subject']} Q{cell['qid']} {cell['condition']} ===",
        f"  Source: {cell['source_files']['battery']} + {cell['source_files']['results']} + {cell['source_files']['judgments']}",
        f"  Question: {cell['question']}",
        f"  Held-out: {cell['held_out'][:300]}{'...' if len(cell['held_out']) > 300 else ''}",
        f"  Per-judge primary scores: {cell['primary_judges']}",
        f"  Primary 5-judge mean: {cell['primary_mean']} (range {cell['primary_range']}, n={cell['primary_n']})",
        f"  Response (len {len(cell['response'])}):",
        f"  {cell['response'][:response_chars]}{'...' if len(cell['response']) > response_chars else ''}",
    ]
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <subject> <qid> <condition>")
        print(f"Example: python {sys.argv[0]} fukuzawa 35 C4_factdump")
        sys.exit(2)
    subj, qid, cond = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    cell = extract(subj, qid, cond)
    print(format_cell(cell))
