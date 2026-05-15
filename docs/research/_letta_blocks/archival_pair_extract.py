import json, sys
from collections import defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parents[3]

# Pull responses for specific archival Ebers Q31, Q3, and a Hamerton archival pair
def load_results(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_resp(results, qid, cond):
    for r in results:
        if r.get('question_id') == qid:
            if 'responses' in r:
                resp = r['responses'].get(cond)
                if resp:
                    return r, resp
    return None, None

# Ebers archival results
ep = str(REPO / 'results/global_ebers/letta_fullpipeline_results.json')
e_results = load_results(ep)
if isinstance(e_results, dict) and 'results' in e_results:
    e_results = e_results['results']
# Check schema
print('Ebers archival sample keys:', list(e_results[0].keys()) if e_results else 'empty')
print('Ebers sample responses keys:', list(e_results[0].get('responses', {}).keys()) if e_results else 'empty')

# Pull Q31 for Ebers archival
for qid in [31, 14, 3]:
    for r in e_results:
        if r.get('question_id') == qid:
            print(f'\n=== EBERS archival Q{qid} ===')
            print(f'Q: {r.get("question_text", "")}')
            print(f'Held-out: {r.get("held_out_passage", "")[:300]}')
            for cond_key, resp in r.get('responses', {}).items():
                text = resp.get('text', '') if isinstance(resp, dict) else str(resp)
                print(f'\n{cond_key} [model={resp.get("model", "?") if isinstance(resp, dict) else "?"}]:')
                print(text[:1800])
            break

# Pull Hamerton Q25 and Q46 archival
hp = str(REPO / 'results/hamerton/letta_fullpipeline_results.json')
h_results = load_results(hp)
if isinstance(h_results, dict) and 'results' in h_results:
    h_results = h_results['results']
for qid in [25, 46]:
    for r in h_results:
        if r.get('question_id') == qid:
            print(f'\n=== HAMERTON archival Q{qid} ===')
            print(f'Q: {r.get("question_text", "")}')
            print(f'Held-out: {r.get("held_out_passage", "")[:300]}')
            for cond_key, resp in r.get('responses', {}).items():
                text = resp.get('text', '') if isinstance(resp, dict) else str(resp)
                print(f'\n{cond_key} [model={resp.get("model", "?") if isinstance(resp, dict) else "?"}]:')
                print(text[:1800])
            break
