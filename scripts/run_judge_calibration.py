"""
Judge Calibration Test — give the model the held-out answer as a fact.
If judges don't score 5.0, we have measurement error to quantify.
Tests: answer-as-fact (no spec) and answer-as-fact + spec.
"""
import json, httpx, subprocess, os, time, pathlib
from collections import defaultdict

for k in ['ANTHROPIC_API_KEY', 'GEMINI_API_KEY']:
    r = subprocess.run(['powershell', '-Command',
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val: os.environ[k] = val

api_key = os.environ['ANTHROPIC_API_KEY']
gemini_key = os.environ['GEMINI_API_KEY']

battery = json.load(open('data/experiments/memory_systems/battery/questions_80.json'))

# Load full spec
# NOTE: the hamerton_memory subject environment lives outside this repo. Set
# ANTHROPIC_ROOT to the directory that contains it; defaults to empty so a
# missing path is obvious.
layers_dir = pathlib.Path(os.environ.get("ANTHROPIC_ROOT", "")) / 'hamerton_memory' / 'data' / 'identity_layers'
sections = []
for ln, fn in [('ANCHORS', 'anchors_v4.md'), ('CORE', 'core_v4.md'), ('PREDICTIONS', 'predictions_v4.md')]:
    fp = layers_dir / fn
    if not fp.exists(): continue
    c = fp.read_text(encoding='utf-8')
    m = '## Injectable Block'
    idx = c.find(m)
    block = c[idx + len(m):].strip() if idx >= 0 else c.strip()
    sections.append(f'## {ln}\n\n{block}')
bf = layers_dir / 'brief_v5_clean.md'
c = bf.read_text(encoding='utf-8')
m = '## Injectable Block'
idx = c.find(m)
block = c[idx + len(m):].strip() if idx >= 0 else c.strip()
sections.append(f'## UNIFIED BRIEF\n\n{block}')
spec = '\n\n'.join(sections)

bp_questions = [q for q in battery['questions']
                if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]

print(f'JUDGE CALIBRATION TEST', flush=True)
print(f'{len(bp_questions)} questions x 2 conditions', flush=True)

results = []
for q_idx, q in enumerate(bp_questions):
    qid = q['id']
    q_text = q['text']
    held_out = q['held_out_passage']

    q_result = {'question_id': qid, 'question_text': q_text,
                'held_out_passage': held_out, 'responses': {}}

    # Condition 1: answer-as-fact, no spec
    try:
        resp = httpx.post('https://api.anthropic.com/v1/messages',
            json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 1024, 'temperature': 0,
                  'system': ('The following fact is available about the person '
                             'this question concerns.\n\n=== FACT ===\n- ' + held_out),
                  'messages': [{'role': 'user', 'content': q_text}]},
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'}, timeout=60)
        d = resp.json()
        q_result['responses']['answer_as_fact'] = {
            'text': d['content'][0]['text'],
            'output_tokens': d['usage']['output_tokens']}
    except Exception as e:
        q_result['responses']['answer_as_fact'] = {'error': str(e)}

    # Condition 2: answer-as-fact + spec
    try:
        resp = httpx.post('https://api.anthropic.com/v1/messages',
            json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 1024, 'temperature': 0,
                  'system': ('The following is a behavioral specification describing your user. '
                             'You also have a retrieved fact.\n\n'
                             '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                             '=== RETRIEVED FACT ===\n- ' + held_out),
                  'messages': [{'role': 'user', 'content': q_text}]},
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'}, timeout=60)
        d = resp.json()
        q_result['responses']['answer_as_fact_plus_spec'] = {
            'text': d['content'][0]['text'],
            'output_tokens': d['usage']['output_tokens']}
    except Exception as e:
        q_result['responses']['answer_as_fact_plus_spec'] = {'error': str(e)}

    results.append(q_result)
    if (q_idx + 1) % 10 == 0:
        print(f'  {q_idx + 1}/{len(bp_questions)} generated', flush=True)

print(f'\nGeneration done. Now judging with Haiku + Gemini...', flush=True)


def jp(ho, txt):
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + ho + '\n\n'
            '=== RESPONSE ===\n' + txt[:1500] + '\n\n'
            'Rate 1-5:\n'
            '5=Predicts specific outcome\n'
            '4=General direction correct\n'
            '3=Right domain wrong outcome\n'
            '2=Wrong prediction\n'
            '1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')


judgments = []
errors = 0
for r in results:
    ho = r['held_out_passage']
    for cond in ['answer_as_fact', 'answer_as_fact_plus_spec']:
        resp = r['responses'].get(cond, {})
        txt = resp.get('text', '')
        if not txt:
            continue

        prompt = jp(ho, txt)
        h = g = 0
        try:
            resp_h = httpx.post('https://api.anthropic.com/v1/messages',
                json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=30)
            t = resp_h.json()['content'][0]['text'].strip()
            h = int(t[0]) if t and t[0].isdigit() else 0
        except:
            pass
        try:
            resp_g = httpx.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}',
                json={'contents': [{'parts': [{'text': prompt}]}]}, timeout=30)
            if resp_g.status_code == 200:
                t = resp_g.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                g = int(t[0]) if t and t[0].isdigit() else 0
            elif resp_g.status_code == 429:
                time.sleep(10)
                errors += 1
        except:
            errors += 1

        judgments.append({'question_id': r['question_id'], 'condition': cond,
                         'haiku_score': h, 'gemini_score': g})
        time.sleep(0.3)

# Save
outdir = 'data/experiments/memory_systems/results/judge_calibration'
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, 'results.json'), 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
with open(os.path.join(outdir, 'judgments.json'), 'w') as f:
    json.dump(judgments, f, indent=2)

# Report
h_scores = defaultdict(list)
g_scores = defaultdict(list)
for j in judgments:
    if j['haiku_score'] > 0:
        h_scores[j['condition']].append(j['haiku_score'])
    if j['gemini_score'] > 0:
        g_scores[j['condition']].append(j['gemini_score'])

print(f'\n=== JUDGE CALIBRATION RESULTS ===', flush=True)
print(f'Expected: 5.0 (model given the literal answer)\n', flush=True)
for cond in ['answer_as_fact', 'answer_as_fact_plus_spec']:
    h = h_scores.get(cond, [])
    g = g_scores.get(cond, [])
    h_avg = sum(h) / len(h) if h else 0
    g_avg = sum(g) / len(g) if g else 0
    h_dist = [h.count(i) for i in range(1, 6)]
    g_dist = [g.count(i) for i in range(1, 6)]
    print(f'{cond}:', flush=True)
    print(f'  Haiku:  {h_avg:.2f} (n={len(h)}) dist={h_dist}', flush=True)
    print(f'  Gemini: {g_avg:.2f} (n={len(g)}) dist={g_dist}', flush=True)

print(f'\nIf < 5.0: judges penalize style/length, not content accuracy.', flush=True)
print(f'Gap between 5.0 and actual = measurement error in rubric.', flush=True)
print(f'Errors: {errors}', flush=True)
