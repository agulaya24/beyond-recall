"""
S114 comprehensive parse-failure backfill.

Strategy:
  - Load s114_parse_failure_manifest.json
  - For each (subject, condition, judge) cell with parse failures, find
    the originating per-judge JSON file and the responses file
  - For each PF row whose response text exists, re-call the judge
  - Write results to _s114 backfill files alongside the originals
  - Skip cells where the response doesn't exist (ingestion failures)
  - Skip merged files (derived; can be regenerated from per-judge files)

Supports all conditions across all subjects. Stops on any individual
failure and moves on. Incremental save every 20 calls.
"""

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
MANIFEST = REPO / 'docs' / 'research' / 's114_parse_failure_manifest.json'

JUDGE_CONFIG = {
    'haiku':        {'provider': 'anthropic', 'model': 'claude-haiku-4-5-20251001'},
    'sonnet':       {'provider': 'anthropic', 'model': 'claude-sonnet-4-6'},
    'opus':         {'provider': 'anthropic', 'model': 'claude-opus-4-6'},
    'gpt4o':        {'provider': 'openai',    'model': 'gpt-4o-2024-08-06'},
    'gpt54':        {'provider': 'openai',    'model': 'gpt-5.4'},
    'gemini_flash': {'provider': 'google',    'model': 'gemini-2.5-flash'},
    'gemini_pro':   {'provider': 'google',    'model': 'gemini-2.5-pro'},
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
                wait = min(60, 2 ** (attempt + 2))
                time.sleep(wait)
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
                wait = min(60, 2 ** (attempt + 2))
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_gemini(api_key, model, prompt):
    for attempt in range(5):
        try:
            r = httpx.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}',
                json={'contents': [{'parts': [{'text': prompt}]}],
                      'generationConfig': {'temperature': 0, 'maxOutputTokens': 8}},
                timeout=60,
            )
            if r.status_code == 429:
                wait = min(60, 2 ** (attempt + 2))
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            cand = data.get('candidates', [])
            if cand and cand[0].get('content', {}).get('parts'):
                return cand[0]['content']['parts'][0].get('text', '')
            return ''
        except Exception:
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def call_judge(judge, prompt, keys):
    cfg = JUDGE_CONFIG[judge]
    if cfg['provider'] == 'anthropic':
        return call_anthropic(keys['ANTHROPIC_API_KEY'], cfg['model'], prompt)
    if cfg['provider'] == 'openai':
        return call_openai(keys['OPENAI_API_KEY'], cfg['model'], prompt)
    if cfg['provider'] == 'google':
        return call_gemini(keys['GEMINI_API_KEY'], cfg['model'], prompt)


def atomic_write(path, data):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def infer_cell_prefix(subject, condition):
    """
    Return (response_file_path, prefix_for_judgment_file) for a given subject/condition.

    subject is e.g. 'global_ebers' or 'hamerton'
    condition is e.g. 'C1_baselayer', 'C5_baseline', etc.
    """
    sdir = RESULTS / subject

    # Direct conditions (main gradient, globals): use results_v2.json
    direct_conds = {'C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                    'C4_factdump', 'C4a_full_facts_plus_spec'}
    if condition in direct_conds:
        if subject == 'hamerton':
            # Hamerton uses results.json with _full conditions for C2a/C2c/C4a
            return sdir / 'results.json', None
        return sdir / 'results_v2.json', None

    # C8/C9
    if condition in {'C8_raw_corpus', 'C9_raw_corpus_plus_spec'}:
        return sdir / 'c8_c9_results.json', 'c8_c9'

    # Memory system conditions
    for system in ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']:
        if condition == f'C1_{system}' or condition == f'C3_{system}':
            return sdir / f'{system}_results.json', system
        if condition == f'C1_{system}_fp' or condition == f'C3_{system}_fp':
            return sdir / f'{system}_fullpipeline_results.json', f'{system}_fullpipeline'

    return None, None


def load_response_for_cell(response_path, condition):
    """Return {question_id: (held_out_passage, response_text)} for a given condition."""
    if not response_path or not response_path.exists():
        return {}
    data = json.load(response_path.open(encoding='utf-8'))
    out = {}
    for q in data:
        if not isinstance(q, dict):
            continue
        qid = q.get('question_id')
        ho = q.get('held_out_passage')
        if not ho or qid is None:
            continue
        responses = q.get('responses', {})
        rdata = responses.get(condition)
        if rdata is None:
            continue
        text = rdata.get('text', '') if isinstance(rdata, dict) else str(rdata)
        if not text:
            continue
        out[qid] = (ho, text)
    return out


def find_existing_scores(subject, condition, judge):
    """
    Returns {question_id: existing_score_or_None} from original per-judge file.
    Also returns the path to that file so we know where to write backfill.
    """
    sdir = RESULTS / subject
    # Map condition to the per-judge filename prefix
    _, prefix = infer_cell_prefix(subject, condition)

    # For direct conditions (no prefix), look at judgments_v2.json which is long-format
    if prefix is None:
        jf = sdir / 'judgments_v2.json'
        if not jf.exists():
            return None, {}
        data = json.load(jf.open(encoding='utf-8'))
        scores = {}
        for r in data:
            if r.get('condition') == condition and r.get('judge') == judge:
                scores[r['question_id']] = r.get('score')
        return jf, scores

    # For prefixed conditions, there's a per-judge file
    jf = sdir / f'{prefix}_judgments_{judge}.json'
    if not jf.exists():
        return None, {}
    data = json.load(jf.open(encoding='utf-8'))
    scores = {}
    for r in data:
        if r.get('condition') == condition:
            scores[r['question_id']] = r.get('score')
    return jf, scores


def needs_rerun(score):
    return score in (0, None)


def run_backfill():
    load_env()
    keys = {k: os.environ.get(k) for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY']}

    manifest = json.load(MANIFEST.open(encoding='utf-8'))

    # Deduplicate: one cell per (subject, condition, judge)
    seen = {}
    for entry in manifest:
        key = (entry['subject'], entry['condition'], entry['judge'])
        if key not in seen or entry['parse_failures'] > seen[key]['parse_failures']:
            seen[key] = entry

    cells = sorted(seen.values(), key=lambda e: -e['parse_failures'])
    log(f'Found {len(cells)} unique cells with parse failures')

    total_new_calls = 0
    backfill_dir = REPO / 'results' / '_s114_backfills'
    backfill_dir.mkdir(parents=True, exist_ok=True)

    for cell in cells:
        subject, condition, judge = cell['subject'], cell['condition'], cell['judge']

        # Skip gemini_pro - coverage is intentionally partial and the few PFs aren't material
        if judge == 'gemini_pro':
            continue
        if judge not in JUDGE_CONFIG:
            continue

        response_path, _ = infer_cell_prefix(subject, condition)
        if not response_path or not response_path.exists():
            log(f'[{subject} / {condition} / {judge}] no response file; skip')
            continue

        responses = load_response_for_cell(response_path, condition)
        if not responses:
            log(f'[{subject} / {condition} / {judge}] no matching responses for condition; skip')
            continue

        jfile, existing_scores = find_existing_scores(subject, condition, judge)

        # Backfill target file
        out_path = backfill_dir / f'{subject}__{condition}__{judge}.json'
        existing = []
        if out_path.exists():
            try:
                existing = json.load(out_path.open())
            except Exception:
                existing = []
        done = {r['question_id'] for r in existing}

        to_run = []
        for qid, (ho, resp_text) in responses.items():
            if qid in done:
                continue
            # Only re-run if original was a parse failure
            original = existing_scores.get(qid)
            if not needs_rerun(original):
                continue
            to_run.append((qid, ho, resp_text))

        if not to_run:
            continue

        log(f'[{subject} / {condition} / {judge}] {len(to_run)} to rerun')

        for qid, ho, resp_text in to_run:
            prompt = judge_prompt(ho, resp_text)
            try:
                raw = call_judge(judge, prompt, keys)
                score = parse_score(raw)
            except Exception as e:
                raw = f'ERROR: {e}'
                score = 0
                log(f'  [{subject}/{condition}/{judge} Q{qid}] ERROR: {e}')
            existing.append({
                'question_id': qid,
                'condition': condition,
                'judge': judge,
                'score': score if score > 0 else None,
                'raw': raw[:100] if isinstance(raw, str) else str(raw)[:100],
                'parse_failure': score == 0,
            })
            total_new_calls += 1
            if len(existing) % 20 == 0:
                atomic_write(out_path, existing)

        atomic_write(out_path, existing)
        # Count successful rescues
        rescued = sum(1 for r in existing if not r.get('parse_failure'))
        log(f'[{subject} / {condition} / {judge}] done — {rescued}/{len(existing)} rescued, total new calls {total_new_calls}')

    log(f'\nBackfill complete. Total new API calls: {total_new_calls}')


if __name__ == '__main__':
    run_backfill()
