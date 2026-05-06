"""
S114 backfill: re-judge Base Layer C1/C3 responses with GPT-4o + GPT-5.4
for the 12 globals whose original runs hit sustained 429 rate limits
(all parse_failures in baselayer_judgments_{gpt4o,gpt54,gemini_flash}.json).

Brings Base Layer to full 5-judge primary coverage.

Excludes:
  - zitkala_sa (full 6-judge coverage already)
  - hamerton (Base Layer not in main gradient for Hamerton)
  - franklin (Base Layer not tested on Franklin)
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
RESULTS = REPO / 'results'

JUDGES = {
    'gpt4o':  {'provider': 'openai', 'model': 'gpt-4o-2024-08-06'},
    'gpt54':  {'provider': 'openai', 'model': 'gpt-5.4'},
}

CONDITIONS = ['C1_baselayer', 'C3_baselayer']

# 12 globals that need backfill (everyone except zitkala_sa which has full coverage)
SUBJECTS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
    'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee', 'yung_wing',
]


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    for k in ['OPENAI_API_KEY']:
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


def call_openai(api_key, model, prompt, max_tokens=8):
    for attempt in range(5):
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
            if r.status_code == 429:
                wait = 2 ** (attempt + 2)
                log(f'  429 rate limit, waiting {wait}s...')
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
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

    total_calls = 0
    for subject in SUBJECTS:
        subj_dir = RESULTS / f'global_{subject}'
        results_path = subj_dir / 'baselayer_results.json'
        if not results_path.exists():
            log(f'[{subject}] no baselayer_results.json; skipping')
            continue
        data = json.load(results_path.open(encoding='utf-8'))

        for judge_name in JUDGES:
            out_path = subj_dir / f'baselayer_judgments_{judge_name}_s114.json'
            rows = []
            if out_path.exists():
                try:
                    rows = json.load(out_path.open())
                except Exception:
                    rows = []
            done = {(r['question_id'], r['condition']) for r in rows}

            for q in data:
                qid = q['question_id']
                ho = q.get('held_out_passage')
                responses = q.get('responses', {})
                if not ho:
                    continue
                for cond in CONDITIONS:
                    if (qid, cond) in done:
                        continue
                    resp_data = responses.get(cond)
                    if not resp_data or not resp_data.get('text'):
                        log(f'[{subject}] Missing {cond} response for Q{qid}')
                        continue
                    prompt = judge_prompt(ho, resp_data['text'])
                    try:
                        raw = call_openai(ok, JUDGES[judge_name]['model'], prompt)
                        score = parse_score(raw)
                    except Exception as e:
                        log(f'[{subject}] [{judge_name}] Q{qid} {cond}: {e}')
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
                    total_calls += 1
                    if len(rows) % 10 == 0:
                        atomic_write(out_path, rows)

            atomic_write(out_path, rows)
            log(f'[{subject}] [{judge_name}] DONE {len(rows)} rows written to {out_path.name}')

    log(f'\nALL DONE. Total new calls: {total_calls}')


if __name__ == '__main__':
    main()
