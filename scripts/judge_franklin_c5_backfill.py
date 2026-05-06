"""
Franklin C5 backfill — run gpt4o + gpt5.4 on the legacy Franklin run's
C5_baseline responses so Franklin enters the 5-judge primary panel.

Source responses: results/franklin_legacy_20260411/results.json (condition: C5_baseline in responses dict).
Output: results/franklin_legacy_20260411/analysis/{gpt4o,gpt54}_judgments.json
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
FRANKLIN_DIR = REPO / 'results' / 'franklin_legacy_20260411'
RESULTS = FRANKLIN_DIR / 'results.json'
ANALYSIS = FRANKLIN_DIR / 'analysis'

JUDGES = {
    'gpt4o': 'gpt-4o-2024-08-06',
    'gpt54': 'gpt-5.4',
}


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    r = subprocess.run(
        ['powershell', '-Command',
         "[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')"],
        capture_output=True, text=True
    )
    v = r.stdout.strip()
    if v:
        os.environ['OPENAI_API_KEY'] = v


def judge_prompt(held_out, response_text):
    return (
        'You are evaluating whether a response about a person PREDICTED what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
        '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
        'Rate 1-5:\n5=Predicts specific outcome\n4=General direction correct\n'
        '3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def call_openai(api_key, model, prompt):
    for attempt in range(5):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                timeout=60,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def atomic_write(path, data):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    load_env()
    ok = os.environ.get('OPENAI_API_KEY')
    if not ok:
        log('FATAL: missing OPENAI_API_KEY')
        sys.exit(1)

    data = json.load(RESULTS.open(encoding='utf-8'))
    # Franklin legacy results: responses is a string; need to parse with literal_eval
    import ast
    bp = []
    for q in data:
        if q.get('tier') != 'behavioral_prediction':
            continue
        if not q.get('held_out_passage'):
            continue
        resps = q.get('responses')
        if isinstance(resps, str):
            try:
                resps = ast.literal_eval(resps)
            except Exception:
                continue
        if not isinstance(resps, dict):
            continue
        for cond in ['C5_baseline', 'C2a_spec_only', 'C4a_factdump_plus_spec']:
            cdata = resps.get(cond)
            if not cdata:
                continue
            text = cdata.get('text') if isinstance(cdata, dict) else str(cdata)
            if text:
                bp.append({'question_id': q['question_id'],
                           'condition': cond,
                           'held_out_passage': q['held_out_passage'],
                           'response_text': text})

    log(f'Loaded {len(bp)} Franklin BP questions with C5 responses')

    for judge_name, model in JUDGES.items():
        out_path = ANALYSIS / f'{judge_name}_judgments.json'
        rows = []
        if out_path.exists():
            try:
                rows = json.load(out_path.open())
            except Exception:
                rows = []
        done = {(r['question_id'], r['condition']) for r in rows}

        for q in bp:
            key = (q['question_id'], q['condition'])
            if key in done:
                continue
            prompt = judge_prompt(q['held_out_passage'], q['response_text'])
            try:
                raw = call_openai(ok, model, prompt)
                score = parse_score(raw)
            except Exception as e:
                raw = f'ERROR: {e}'
                score = 0
            rows.append({
                'question_id': q['question_id'],
                'condition': q['condition'],
                f'{judge_name}_score': score if score > 0 else 0,
            })
            if len(rows) % 10 == 0:
                atomic_write(out_path, rows)

        atomic_write(out_path, rows)
        valid = [r[f'{judge_name}_score'] for r in rows if r.get(f'{judge_name}_score', 0) > 0]
        import statistics
        mean = statistics.mean(valid) if valid else 0
        log(f'[{judge_name}] DONE {len(rows)} rows, C5 mean = {mean:.3f}, saved to {out_path}')


if __name__ == '__main__':
    main()
