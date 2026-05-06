"""
S114 Franklin backfill: score Franklin spec-condition responses with
Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4 (the 4 judges never run on Franklin).

Franklin responses live in results/franklin/fullstack_haiku.json
with 5 conditions: C2a_full_spec, C2c_full_wrong_spec, C3_full_mem0,
C3_full_supermemory, C4a_full_all_facts_plus_spec.

40 questions × 5 conditions × 4 judges = 800 judgments.
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
FRANKLIN = REPO / 'results' / 'franklin'
RESPONSE_PATH = FRANKLIN / 'fullstack_haiku.json'

JUDGES = {
    'sonnet': {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':   {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':  {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai',    'model': 'gpt-5.4'},
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
    return (
        'You are evaluating whether a response about a person PREDICTED what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
        '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
        'Rate 1-5:\n'
        '5=Predicts specific outcome\n'
        '4=General direction correct\n'
        '3=Right domain wrong outcome\n'
        '2=Wrong prediction\n'
        '1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def call_anthropic(api_key, model, prompt):
    for attempt in range(5):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={'model': model, 'max_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=60,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            return r.json()['content'][0]['text']
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


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


def call_judge(judge, prompt, ak, ok):
    cfg = JUDGES[judge]
    if cfg['provider'] == 'anthropic':
        return call_anthropic(ak, cfg['model'], prompt)
    return call_openai(ok, cfg['model'], prompt)


def atomic_write(path, data):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    load_env()
    ak = os.environ.get('ANTHROPIC_API_KEY')
    ok = os.environ.get('OPENAI_API_KEY')
    if not ak or not ok:
        log('FATAL: missing API keys')
        sys.exit(1)

    data = json.load(RESPONSE_PATH.open(encoding='utf-8'))
    bp = [q for q in data if q.get('tier') == 'behavioral_prediction' and q.get('held_out_passage')]
    log(f'Loaded {len(bp)} BP questions')

    for judge_name in JUDGES:
        out_path = FRANKLIN / f'{judge_name}_judgments.json'
        rows = []
        if out_path.exists():
            try:
                rows = json.load(out_path.open())
            except Exception:
                rows = []
        done = {(r['question_id'], r['condition']) for r in rows}

        for q in bp:
            qid = q['question_id']
            ho = q['held_out_passage']
            responses = q.get('responses', {})
            for cond in CONDITIONS:
                if (qid, cond) in done:
                    continue
                rdata = responses.get(cond)
                if not rdata or not rdata.get('text'):
                    continue
                prompt = judge_prompt(ho, rdata['text'])
                try:
                    raw = call_judge(judge_name, prompt, ak, ok)
                    score = parse_score(raw)
                except Exception as e:
                    raw = f'ERROR: {e}'
                    score = 0
                rows.append({
                    'question_id': qid,
                    'condition': cond,
                    'judge': judge_name,
                    'score': score if score > 0 else None,
                    'raw': raw[:100] if isinstance(raw, str) else str(raw)[:100],
                    'parse_failure': score == 0,
                })
                if len(rows) % 20 == 0:
                    atomic_write(out_path, rows)

        atomic_write(out_path, rows)
        log(f'[{judge_name}] DONE {len(rows)} rows -> {out_path}')


if __name__ == '__main__':
    main()
