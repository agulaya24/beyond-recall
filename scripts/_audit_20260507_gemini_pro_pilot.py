"""5-call gemini_pro pilot."""

import json, os, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from backfill_all_parse_failures import judge_prompt, parse_score, load_env, call_gemini

response_path = REPO / 'results' / 'global_augustine' / 'baselayer_results.json'
data = json.load(response_path.open(encoding='utf-8'))

qmap = {}
for q in data:
    if 'C1_baselayer' not in q.get('responses', {}):
        continue
    text = q['responses']['C1_baselayer'].get('text', '')
    ho = q.get('held_out_passage', '')
    if text and ho:
        qmap[q['question_id']] = (ho, text)
        if len(qmap) >= 5:
            break

load_env()
api_key = os.environ.get('GEMINI_API_KEY')
results = []
for qid, (ho, text) in qmap.items():
    prompt = judge_prompt(ho, text)
    try:
        raw = call_gemini(api_key, 'gemini-2.5-pro', prompt)
        score = parse_score(raw)
        raw_ex = (raw or '').encode('ascii', 'replace').decode('ascii')[:120]
        results.append({'qid': qid, 'score': score, 'raw': raw_ex})
        print(f'Q{qid}: score={score}, raw={raw_ex!r}')
    except Exception as e:
        msg = str(e).encode('ascii', 'replace').decode('ascii')[:200]
        results.append({'qid': qid, 'error': msg})
        print(f'Q{qid}: ERROR: {msg}')
    time.sleep(1)

n_ok = sum(1 for r in results if r.get('score') in (1,2,3,4,5))
print(f'\nRescued {n_ok}/{len(results)}')

out = REPO / 'docs' / 'research' / '_audit_20260507_gemini_pro_pilot.json'
out.write_text(json.dumps(results, indent=2), encoding='utf-8')
