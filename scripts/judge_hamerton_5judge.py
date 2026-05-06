"""
Run Sonnet 4.6, Opus 4.6, and GPT-4o as judges on Hamerton's spec-condition
responses (C2a, C2c, C3_mem0, C3_supermemory, C4a). Brings Hamerton's primary-judge
coverage up to 5 (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) for the main gradient.

Responses live in: results/hamerton/results.json (39 behavioral_prediction questions).

Output: results/hamerton/{sonnet,opus,gpt4o}_judgments.json  (long format)
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
HAMERTON = REPO / 'results' / 'hamerton'
RESULTS_PATH = HAMERTON / 'results.json'

JUDGES = {
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
}

CONDITIONS = [
    'C2a_full_spec',
    'C2c_full_wrong_spec',
    'C3_full_mem0',
    'C3_full_supermemory',
    'C4a_full_all_facts_plus_spec',
]


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY']:
        r = subprocess.run(
            ['powershell', '-Command',
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


def judge_prompt(held_out, response_text):
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
            '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
            'Rate 1-5:\n'
            '5=Predicts specific outcome\n'
            '4=General direction correct\n'
            '3=Right domain wrong outcome\n'
            '2=Wrong prediction\n'
            '1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def call_anthropic(api_key, model, prompt, max_tokens=8):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': model,
                    'max_tokens': max_tokens,
                    'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                timeout=60,
            )
            r.raise_for_status()
            d = r.json()
            return d['content'][0]['text']
        except Exception as e:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_openai(api_key, model, prompt, max_tokens=8):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={
                    'model': model,
                    'max_completion_tokens': max_tokens,
                    'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge_name, prompt, anthropic_key, openai_key):
    spec = JUDGES[judge_name]
    if spec['provider'] == 'anthropic':
        return call_anthropic(anthropic_key, spec['model'], prompt)
    else:
        return call_openai(openai_key, spec['model'], prompt)


def atomic_write(path, data):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    load_env()
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    if not anthropic_key:
        log('FATAL: missing ANTHROPIC_API_KEY')
        sys.exit(1)
    if not openai_key:
        log('FATAL: missing OPENAI_API_KEY')
        sys.exit(1)

    data = json.load(RESULTS_PATH.open(encoding='utf-8'))
    bp = [r for r in data if r.get('tier') == 'behavioral_prediction' and r.get('held_out_passage')]
    log(f'Loaded {len(bp)} behavioral-prediction questions with held-out passages')

    for judge_name in JUDGES:
        out_path = HAMERTON / f'{judge_name}_judgments.json'
        rows = []
        if out_path.exists():
            try:
                existing = json.load(out_path.open())
                rows = existing
                log(f'[{judge_name}] Resuming from {len(rows)} existing rows')
            except Exception:
                rows = []
        done = {(r['question_id'], r['condition']) for r in rows}

        log(f'[{judge_name}] Starting judging. {len(bp)*len(CONDITIONS) - len(done)} calls remaining.')
        calls_this_run = 0
        for q in bp:
            qid = q['question_id']
            ho = q['held_out_passage']
            for cond in CONDITIONS:
                if (qid, cond) in done:
                    continue
                resp = q.get('responses', {}).get(cond)
                if not resp or not resp.get('text'):
                    log(f'[{judge_name}] Missing response q={qid} cond={cond}; skipping')
                    continue
                prompt = judge_prompt(ho, resp['text'])
                try:
                    raw = call_judge(judge_name, prompt, anthropic_key, openai_key)
                    score = parse_score(raw)
                except Exception as e:
                    log(f'[{judge_name}] API error q={qid} cond={cond}: {e}')
                    score = 0
                    raw = f'ERROR: {e}'
                row = {
                    'question_id': qid,
                    'condition': cond,
                    'judge': judge_name,
                    'score': score if score > 0 else None,
                    'raw_response': raw[:200] if isinstance(raw, str) else str(raw)[:200],
                    'parse_failure': score == 0,
                }
                rows.append(row)
                calls_this_run += 1
                if calls_this_run % 10 == 0:
                    atomic_write(out_path, rows)
                    log(f'[{judge_name}] Progress: {calls_this_run} new calls, total {len(rows)} rows')

        atomic_write(out_path, rows)
        log(f'[{judge_name}] DONE. {len(rows)} total rows, {calls_this_run} new calls this run. Output: {out_path}')


if __name__ == '__main__':
    main()
