"""
7-judge panel on Supermemory paid-tier rerun responses for the 4 previously-failed subjects.

Subjects: bernal_diaz, babur, cellini, rousseau.
Conditions: C1_supermemory_fp (retrieval only), C3_supermemory_fp (retrieval + BL spec).
Judges: haiku, sonnet, opus, gpt4o, gpt54 (5-primary) + gemini_flash, gemini_pro (sensitivity).

Reads responses from:
  memory_system/data/experiments/memory_systems/results/global_<subject>/supermemory_fullpipeline_results.json

Writes judgments to (matching existing 10-subject format for downstream aggregation):
  memory_system/data/experiments/memory_systems/results/global_<subject>/supermemory_fullpipeline_judgments_<judge>.json

Checkpoints every 10 calls. Resume-safe.
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

MS_RESULTS = Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results')
SUBJECTS = ['bernal_diaz', 'babur', 'cellini', 'rousseau']
CONDITIONS = ['C1_supermemory_fp', 'C3_supermemory_fp']

JUDGES = {
    'haiku':         {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet':        {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':          {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':         {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':         {'provider': 'openai',    'model': 'gpt-5-chat-latest'},
    'gemini_flash':  {'provider': 'google',    'model': 'gemini-2.5-flash'},
    'gemini_pro':    {'provider': 'google',    'model': 'gemini-2.5-pro'},
}


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY']:
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
            '=== RESPONSE ===\n' + (response_text or '')[:1500] + '\n\n'
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


def call_anthropic(api_key, model, prompt):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': model,
                    'max_tokens': 8,
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
            return r.json()['content'][0]['text']
        except Exception as e:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_openai(api_key, model, prompt):
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={
                    'model': model,
                    'max_completion_tokens': 8,
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


def call_gemini(api_key, model, prompt):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    for attempt in range(4):
        try:
            r = httpx.post(
                url,
                json={
                    'contents': [{'parts': [{'text': prompt}]}],
                    'generationConfig': {'temperature': 0, 'maxOutputTokens': 16},
                },
                headers={'Content-Type': 'application/json'},
                timeout=60,
            )
            r.raise_for_status()
            d = r.json()
            cands = d.get('candidates', [])
            if not cands:
                return ''
            parts = cands[0].get('content', {}).get('parts', [])
            for p in parts:
                if 'text' in p:
                    return p['text']
            return ''
        except Exception as e:
            if attempt < 3:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge_name, prompt, keys):
    spec = JUDGES[judge_name]
    if spec['provider'] == 'anthropic':
        return call_anthropic(keys['anthropic'], spec['model'], prompt)
    elif spec['provider'] == 'openai':
        return call_openai(keys['openai'], spec['model'], prompt)
    elif spec['provider'] == 'google':
        return call_gemini(keys['gemini'], spec['model'], prompt)


def atomic_write(path, data):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_responses(subject):
    """Return list of {question_id, condition, response_text, held_out_passage}."""
    p = MS_RESULTS / f'global_{subject}' / 'supermemory_fullpipeline_results.json'
    data = json.load(p.open(encoding='utf-8'))
    out = []
    for item in data:
        qid = item.get('question_id')
        ho = item.get('held_out_passage') or ''
        responses = item.get('responses', {})
        for cond in CONDITIONS:
            r = responses.get(cond)
            if not r:
                continue
            text = r.get('text') if isinstance(r, dict) else str(r)
            if not text:
                continue
            out.append({
                'question_id': qid,
                'condition': cond,
                'response_text': text,
                'held_out_passage': ho,
            })
    return out


def main():
    load_env()
    keys = {
        'anthropic': os.environ.get('ANTHROPIC_API_KEY'),
        'openai': os.environ.get('OPENAI_API_KEY'),
        'gemini': os.environ.get('GEMINI_API_KEY'),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        log(f'FATAL: missing keys: {missing}')
        sys.exit(1)

    # Load responses for each subject
    all_responses = {}
    for subj in SUBJECTS:
        rs = load_responses(subj)
        all_responses[subj] = rs
        log(f'{subj}: {len(rs)} response records')

    total_calls_needed = sum(len(rs) for rs in all_responses.values()) * len(JUDGES)
    log(f'Total calls across all subjects/judges: {total_calls_needed}')

    # Process judge by judge, subject by subject (lets us resume per-judge if interrupted)
    for judge_name in JUDGES:
        for subj in SUBJECTS:
            out_path = MS_RESULTS / f'global_{subj}' / f'supermemory_fullpipeline_judgments_{judge_name}.json'
            rows = []
            # If the file exists and was from the prior free-tier run, archive-rename it first
            # so we start fresh (prior judgments were all parse_failure against empty responses)
            if out_path.exists():
                try:
                    existing = json.load(out_path.open(encoding='utf-8'))
                    # Check: do existing rows reference non-empty responses? If they're all parse_failure,
                    # they're the stale free-tier artifacts; overwrite.
                    non_failure_count = sum(1 for r in existing if r.get('score') and r.get('score') > 0)
                    if non_failure_count == 0:
                        log(f'[{judge_name}/{subj}] overwriting {len(existing)} stale rows (all parse_failure)')
                        rows = []
                    else:
                        rows = existing
                        log(f'[{judge_name}/{subj}] resuming from {len(rows)} existing rows '
                            f'({non_failure_count} with score > 0)')
                except Exception:
                    rows = []
            done = {(r['question_id'], r['condition']) for r in rows
                    if r.get('score') and r['score'] > 0}

            rs = all_responses[subj]
            to_do = [r for r in rs if (r['question_id'], r['condition']) not in done]
            if not to_do:
                log(f'[{judge_name}/{subj}] nothing to do')
                continue

            log(f'[{judge_name}/{subj}] starting {len(to_do)} calls')
            calls_this_run = 0
            for r in to_do:
                prompt = judge_prompt(r['held_out_passage'], r['response_text'])
                try:
                    raw = call_judge(judge_name, prompt, keys)
                    score = parse_score(raw)
                except Exception as e:
                    log(f'[{judge_name}/{subj}] ERROR q={r["question_id"]} c={r["condition"]}: {e}')
                    raw = f'ERROR: {e}'
                    score = 0
                # Remove any prior failure row for this (qid, cond) so we don't duplicate
                rows = [x for x in rows if not (x.get('question_id') == r['question_id']
                                                and x.get('condition') == r['condition'])]
                rows.append({
                    'question_id': r['question_id'],
                    'condition': r['condition'],
                    'judge': judge_name,
                    'score': score if score > 0 else 0,
                    'parse_failure': score == 0,
                })
                calls_this_run += 1
                if calls_this_run % 10 == 0:
                    atomic_write(out_path, rows)
                    log(f'[{judge_name}/{subj}] {calls_this_run}/{len(to_do)} done, saved checkpoint')
            atomic_write(out_path, rows)
            log(f'[{judge_name}/{subj}] DONE {calls_this_run} calls; file: {out_path}')

    log('ALL JUDGES COMPLETE')


if __name__ == '__main__':
    main()
