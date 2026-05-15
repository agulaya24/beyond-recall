"""10-call gemini_flash pilot rerun on the Keckley C1_baselayer cell to test
whether the empty_response failure pattern is rescuable.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from backfill_all_parse_failures import judge_prompt, parse_score, load_env, call_gemini

# Pilot: Keckley C1_baselayer first 10 PFs
SUBJECT = 'global_keckley'
CONDITION = 'C1_baselayer'
JUDGE = 'gemini_flash'

response_path = REPO / 'results' / 'global_keckley' / 'baselayer_results.json'
data = json.load(response_path.open(encoding='utf-8'))

# First 10 questions with C1_baselayer responses
qids = []
qmap = {}
for q in data:
    if 'C1_baselayer' not in q.get('responses', {}):
        continue
    text = q['responses']['C1_baselayer'].get('text', '')
    ho = q.get('held_out_passage', '')
    if text and ho:
        qids.append(q['question_id'])
        qmap[q['question_id']] = (ho, text)
    if len(qids) >= 10:
        break

print(f'Pilot QIDs: {qids}')

load_env()
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print('ERROR: GEMINI_API_KEY not set')
    sys.exit(1)

results = []
for qid in qids:
    ho, text = qmap[qid]
    prompt = judge_prompt(ho, text)
    try:
        raw = call_gemini(api_key, 'gemini-2.5-flash', prompt)
        score = parse_score(raw)
        rescued = score in (1, 2, 3, 4, 5)
        # In ASCII safe form
        raw_excerpt = (raw or '').encode('ascii', 'replace').decode('ascii')[:120]
        results.append({'qid': qid, 'raw_excerpt': raw_excerpt, 'score': score, 'rescued': rescued})
        print(f'  Q{qid}: score={score}, raw={raw_excerpt!r}')
    except Exception as e:
        msg = str(e).encode('ascii', 'replace').decode('ascii')[:200]
        results.append({'qid': qid, 'raw_excerpt': '', 'score': 0, 'rescued': False, 'error': msg})
        print(f'  Q{qid}: ERROR: {msg}')
    time.sleep(0.5)  # Tiny delay

n_rescued = sum(1 for r in results if r['rescued'])
print(f'\nRescued {n_rescued}/{len(results)}')

out = REPO / 'docs' / 'research' / '_audit_20260507_gemini_pilot.json'
out.write_text(json.dumps(results, indent=2), encoding='utf-8')
print(f'Wrote {out}')
