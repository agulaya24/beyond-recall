"""Verify Q21 question_id alignment across battery, results, and judgment files."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# 1. battery_v2.json
b = REPO / 'results' / 'global_keckley' / 'battery_v2.json'
b_data = json.load(b.open(encoding='utf-8')) if b.exists() else None

# 2. baselayer_results.json
r = REPO / 'results' / 'global_keckley' / 'baselayer_results.json'
r_data = json.load(r.open(encoding='utf-8'))

print('=== Q21 alignment check ===')

# battery_v2
if b_data:
    if isinstance(b_data, list):
        b_q21 = next((q for q in b_data if (q.get('question_id') == 21 or q.get('id') == 21)), None)
    elif isinstance(b_data, dict):
        b_q21 = b_data.get('21') or b_data.get(21)
    else:
        b_q21 = None
    if b_q21:
        text = b_q21.get('question_text') or b_q21.get('question') or b_q21.get('text', '')
        text_safe = (text or '').encode('ascii', 'replace').decode('ascii')[:200]
        print(f'battery_v2 Q21: {text_safe!r}')

# baselayer_results
r_q21 = next((q for q in r_data if q.get('question_id') == 21), None)
if r_q21:
    text = r_q21.get('question_text', '')
    text_safe = (text or '').encode('ascii', 'replace').decode('ascii')[:200]
    print(f'baselayer_results Q21 question_text: {text_safe!r}')
    held = r_q21.get('held_out_passage', '')
    held_safe = (held or '').encode('ascii', 'replace').decode('ascii')[:200]
    print(f'baselayer_results Q21 held_out_passage: {held_safe!r}')

# Paper text reference
paper_q21_question = "How does Elizabeth explain her decision not to visit her mother's grave"
print(f'\nPaper line 1423 expects: {paper_q21_question!r}')
if r_q21:
    qt = r_q21.get('question_text', '')
    match = paper_q21_question.lower() in qt.lower() if qt else False
    print(f'Match: {match}')
