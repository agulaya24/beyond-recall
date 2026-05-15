"""Verify Babur C9 has response data and identify the action class."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Check if Babur C9 has response data
results_path = REPO / 'results' / 'global_babur' / 'c8_c9_results.json'
print(f'C9 results file exists: {results_path.exists()}')
if results_path.exists():
    data = json.load(results_path.open(encoding='utf-8'))
    print(f'Total questions: {len(data)}')
    has_c9 = 0
    has_c9_text = 0
    sample_qid = None
    for q in data:
        responses = q.get('responses', {})
        if 'C9_raw_corpus_plus_spec' in responses:
            has_c9 += 1
            r = responses['C9_raw_corpus_plus_spec']
            t = r.get('text', '') if isinstance(r, dict) else r
            if t and len(str(t)) > 100:
                has_c9_text += 1
                if sample_qid is None:
                    sample_qid = q.get('question_id')
    print(f'Questions with C9 response: {has_c9}')
    print(f'Questions with C9 response text >100 chars: {has_c9_text}')
    print(f'Sample QID: {sample_qid}')

# Check the per-judge file for C9 to see exactly what's failing
print('\nPer-judge files for Babur C8/C9:')
for judge in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']:
    p = REPO / 'results' / 'global_babur' / f'c8_c9_judgments_{judge}.json'
    if not p.exists():
        print(f'  {judge}: FILE MISSING')
        continue
    rows = json.load(p.open(encoding='utf-8'))
    c9_rows = [r for r in rows if r.get('condition') == 'C9_raw_corpus_plus_spec']
    valid = [r for r in c9_rows if not r.get('parse_failure') and r.get('score') in (1, 2, 3, 4, 5)]
    pf = [r for r in c9_rows if r.get('parse_failure') or r.get('score') in (0, None)]
    print(f'  {judge}: total={len(c9_rows)}, valid={len(valid)}, failed={len(pf)}')

# Check what's in backfills for Babur C9
print('\nBackfills for Babur C9:')
bf_dir = REPO / 'results' / '_s114_backfills'
for f in bf_dir.glob('global_babur__C9_raw_corpus_plus_spec__*.json'):
    rows = json.load(f.open(encoding='utf-8'))
    valid = [r for r in rows if not r.get('parse_failure') and r.get('score') in (1, 2, 3, 4, 5)]
    pf = [r for r in rows if r.get('parse_failure') or r.get('score') in (0, None)]
    print(f'  {f.name}: total={len(rows)}, valid={len(valid)}, failed={len(pf)}')
