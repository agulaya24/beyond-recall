"""Judge C8/C9 responses. Uses same 6-judge panel as Option A."""
import json, os, sys, time, re, argparse
from datetime import datetime, timezone
import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']
ALL_SUBJECTS = [
    'zitkala_sa', 'hamerton', 'keckley', 'yung_wing', 'seacole',
    'sunity_devee', 'equiano', 'augustine', 'ebers', 'fukuzawa',
    'cellini', 'bernal_diaz', 'rousseau', 'babur'
]

def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)

def atomic_write_json(path, data):
    tmp = path + '.tmp'
    for attempt in range(3):
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(path): os.replace(tmp, path)
            else: os.rename(tmp, path)
            return
        except PermissionError:
            if attempt < 2:
                time.sleep(2)
                try: os.remove(tmp)
                except: pass
            else:
                # Last resort: write directly
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path):
    if not os.path.exists(path): return None
    with open(path, encoding='utf-8') as f: return json.load(f)

def get_results_dir(s):
    if s == 'hamerton': return os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(RESULTS_BASE, f'global_{s}')

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=8, timeout=60):
    for attempt in range(3):
        try:
            kwargs = {'model': model, 'max_tokens': max_tokens, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': user_message}]}
            if system_prompt: kwargs['system'] = system_prompt
            resp = httpx.post('https://api.anthropic.com/v1/messages', json=kwargs,
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=timeout)
            resp.raise_for_status()
            d = resp.json()
            return {'text': d['content'][0]['text']}
        except Exception as e:
            if attempt < 2: time.sleep(2 ** (attempt + 1))
            else: raise

def api_call_openai(api_key, model, prompt, max_tokens=8):
    for attempt in range(3):
        try:
            resp = httpx.post('https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': max_tokens, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}, timeout=30)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            if attempt < 2: time.sleep(2 ** (attempt + 1))
            else: raise

def api_call_gemini(api_key, model, prompt):
    for attempt in range(3):
        try:
            resp = httpx.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}',
                json={'contents': [{'parts': [{'text': prompt}]}]}, timeout=60)
            if resp.status_code == 429: time.sleep(2 ** (attempt + 2)); continue
            resp.raise_for_status()
            return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            if attempt < 2: time.sleep(2 ** (attempt + 1))
            else: raise

def judge_prompt(held_out, response_text):
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
            '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
            'Rate 1-5:\n5=Predicts specific outcome\n4=General direction correct\n'
            '3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')

def parse_score(text):
    if not text: return 0
    match = re.search(r'[1-5]', text.strip())
    return int(match.group()) if match else 0

def run_judge(judge_name, prompt, api_keys):
    raw = ''
    try:
        if judge_name == 'haiku':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-haiku-4-5-20251001', None, prompt)
            raw = r['text']
        elif judge_name == 'sonnet':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-sonnet-4-6', None, prompt)
            raw = r['text']
        elif judge_name == 'opus':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-opus-4-6', None, prompt, timeout=120)
            raw = r['text']
        elif judge_name == 'gpt4o':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-4o', prompt)
        elif judge_name == 'gpt54':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-5.4', prompt)
        elif judge_name == 'gemini_flash':
            raw = api_call_gemini(api_keys['GEMINI_API_KEY'], 'gemini-2.5-flash', prompt)
    except Exception as e:
        return 0, str(e), True
    score = parse_score(raw)
    return score, raw, (score == 0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', default=None)
    parser.add_argument('--judge', default=None)
    args = parser.parse_args()

    api_keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
        'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY', ''),
    }

    subjects = [args.subject] if args.subject else ALL_SUBJECTS
    judges_to_run = [args.judge] if args.judge else JUDGES
    conditions = ['C8_raw_corpus', 'C9_raw_corpus_plus_spec']

    for subject in subjects:
        results_dir = get_results_dir(subject)
        results_path = os.path.join(results_dir, 'c8_c9_results.json')
        results = load_json(results_path)
        if not results:
            log(f'{subject}: no C8/C9 results')
            continue

        for judge_name in judges_to_run:
            judgments_path = os.path.join(results_dir, f'c8_c9_judgments_{judge_name}.json')
            existing = load_json(judgments_path) or []
            done_keys = set(f"{j['question_id']}_{j['condition']}" for j in existing)
            new_count = 0

            for q_result in results:
                qid = q_result['question_id']
                held_out = q_result.get('held_out_passage', '')
                if not held_out: continue

                for cond in conditions:
                    if f'{qid}_{cond}' in done_keys: continue
                    resp = q_result.get('responses', {}).get(cond, {})
                    resp_text = resp.get('text', '')
                    if not resp_text or 'error' in resp:
                        existing.append({'question_id': qid, 'condition': cond,
                            'judge': judge_name, 'score': 0, 'parse_failure': True})
                        continue

                    score, raw, pf = run_judge(judge_name, judge_prompt(held_out, resp_text), api_keys)
                    existing.append({'question_id': qid, 'condition': cond,
                        'judge': judge_name, 'score': score,
                        'raw_response': raw if pf else '', 'parse_failure': pf})
                    new_count += 1
                    atomic_write_json(judgments_path, existing)

            log(f'{subject} / {judge_name}: {new_count} new')

        # Merge
        merged = []
        for jn in JUDGES:
            jp = os.path.join(results_dir, f'c8_c9_judgments_{jn}.json')
            jdata = load_json(jp)
            if jdata: merged.extend(jdata)
        if merged:
            atomic_write_json(os.path.join(results_dir, 'c8_c9_judgments_merged.json'), merged)

    log('DONE')

if __name__ == '__main__':
    main()
