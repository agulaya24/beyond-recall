"""
C8 (raw corpus) and C9 (raw corpus + spec) for all 14 subjects.

C8: Full training text in system prompt, Haiku generates response.
C9: Full training text + behavioral spec in system prompt.

Truncates training text to ~100K words if it exceeds Haiku's context window.

Usage:
    python run_c8_c9.py                    # All 14 subjects
    python run_c8_c9.py --subject babur    # Single subject
"""
import json, os, sys, time, re, argparse
from datetime import datetime, timezone

import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
REPO_DIR = 'C:/Users/Aarik/Anthropic/memory-study-repo'

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
MAX_TRAINING_WORDS = 100000  # Truncate to fit Haiku context

ALL_SUBJECTS = [
    'zitkala_sa', 'hamerton', 'keckley', 'yung_wing', 'seacole',
    'sunity_devee', 'equiano', 'augustine', 'ebers', 'fukuzawa',
    'cellini', 'bernal_diaz', 'rousseau', 'babur'
]


def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)


def atomic_write_json(path, data):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp, path)
    else:
        os.rename(tmp, path)


def get_results_dir(subject):
    if subject == 'hamerton':
        return os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(RESULTS_BASE, f'global_{subject}')


def load_training_text(subject):
    """Load training text, truncate if over MAX_TRAINING_WORDS."""
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'corpus', 'tiers', 'tier_02_ch01-10.txt')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'training.txt')

    text = open(path, encoding='utf-8').read()
    words = text.split()
    truncated = False
    if len(words) > MAX_TRAINING_WORDS:
        text = ' '.join(words[:MAX_TRAINING_WORDS])
        truncated = True
    return text, len(words), truncated


def load_spec(subject):
    if subject == 'hamerton':
        from pathlib import Path
        layers_dir = Path(f'{REPO_DIR}/data/hamerton/spec')
        sections = []
        for layer_name, filename in [
            ("ANCHORS", "anchors_v4.md"), ("CORE", "core_v4.md"),
            ("PREDICTIONS", "predictions_v4.md"),
        ]:
            filepath = layers_dir / filename
            if not filepath.exists(): continue
            content = filepath.read_text(encoding='utf-8')
            marker = "## Injectable Block"
            idx = content.find(marker)
            if idx >= 0:
                block = content[idx + len(marker):].strip()
            else:
                sep = content.find("\n---\n")
                block = content[sep + 5:].strip() if sep >= 0 else content.strip()
            sections.append(f"## {layer_name}\n\n{block}")
        brief_file = layers_dir / "brief_v5_clean.md"
        if brief_file.exists():
            content = brief_file.read_text(encoding='utf-8')
            marker = "## Injectable Block"
            idx = content.find(marker)
            if idx >= 0:
                block = content[idx + len(marker):].strip()
            else:
                sep = content.find("\n---\n")
                block = content[sep + 5:].strip() if sep >= 0 else content.strip()
            sections.append(f"## UNIFIED BRIEF\n\n{block}")
        return "\n\n".join(sections)
    else:
        path = f'{REPO_DIR}/data/global_subjects/{subject}/spec_production.md'
        return open(path, encoding='utf-8').read()


def load_battery(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'battery', 'questions_80.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'battery_v2.json')
    data = json.load(open(path, encoding='utf-8'))
    return [q for q in data['questions']
            if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


def gen(api_key, question, system_prompt):
    for attempt in range(3):
        try:
            resp = httpx.post('https://api.anthropic.com/v1/messages',
                json={'model': RESPONSE_MODEL, 'max_tokens': 1024, 'temperature': 0,
                      'system': system_prompt,
                      'messages': [{'role': 'user', 'content': question}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=180)
            resp.raise_for_status()
            d = resp.json()
            return {
                'text': d['content'][0]['text'],
                'input_tokens': d['usage']['input_tokens'],
                'output_tokens': d['usage']['output_tokens'],
                'model': RESPONSE_MODEL
            }
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                log(f'  Retry {attempt+1}/3 after {wait}s: {e}')
                time.sleep(wait)
            else:
                raise


def run_subject(subject, api_key):
    results_dir = get_results_dir(subject)
    results_path = os.path.join(results_dir, 'c8_c9_results.json')

    # Load existing results for checkpoint
    existing = {}
    if os.path.exists(results_path):
        for r in json.load(open(results_path, encoding='utf-8')):
            existing[r['question_id']] = r

    # Load data
    training_text, total_words, truncated = load_training_text(subject)
    spec = load_spec(subject)
    questions = load_battery(subject)

    log(f'{subject}: {total_words} words {"(truncated to 100K)" if truncated else ""}, {len(questions)} questions')

    total_in = 0
    total_out = 0

    for q in questions:
        qid = q['id']

        # Check if already done
        if qid in existing:
            r = existing[qid]
            if 'C8_raw_corpus' in r.get('responses', {}) and 'C9_raw_corpus_plus_spec' in r.get('responses', {}):
                continue

        q_result = existing.get(qid, {
            'question_id': qid,
            'question_text': q['text'],
            'held_out_passage': q.get('held_out_passage'),
            'responses': {},
            'training_words': total_words,
            'truncated': truncated,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

        # C8: raw corpus only
        if 'C8_raw_corpus' not in q_result.get('responses', {}):
            try:
                t0 = time.time()
                resp = gen(api_key, q['text'],
                    'The following is the full text of an autobiography. Use it to '
                    'answer the question.\n\n'
                    f'=== AUTOBIOGRAPHY TEXT ===\n{training_text}')
                resp['latency_ms'] = round((time.time() - t0) * 1000)
                q_result.setdefault('responses', {})['C8_raw_corpus'] = resp
                total_in += resp['input_tokens']
                total_out += resp['output_tokens']
                log(f'  Q{qid} C8: {resp["output_tokens"]}t ({resp["input_tokens"]} in)')
            except Exception as e:
                q_result.setdefault('responses', {})['C8_raw_corpus'] = {'error': str(e)}
                log(f'  Q{qid} C8: FAILED {e}')

        # C9: raw corpus + spec
        if 'C9_raw_corpus_plus_spec' not in q_result.get('responses', {}):
            try:
                t0 = time.time()
                resp = gen(api_key, q['text'],
                    'The following is a behavioral specification describing your user — '
                    'how they think, decide, and act. You also have the full text of '
                    'their autobiography.\n\n'
                    f'=== BEHAVIORAL SPECIFICATION ===\n{spec}\n\n'
                    f'=== AUTOBIOGRAPHY TEXT ===\n{training_text}')
                resp['latency_ms'] = round((time.time() - t0) * 1000)
                q_result.setdefault('responses', {})['C9_raw_corpus_plus_spec'] = resp
                total_in += resp['input_tokens']
                total_out += resp['output_tokens']
                log(f'  Q{qid} C9: {resp["output_tokens"]}t ({resp["input_tokens"]} in)')
            except Exception as e:
                q_result.setdefault('responses', {})['C9_raw_corpus_plus_spec'] = {'error': str(e)}
                log(f'  Q{qid} C9: FAILED {e}')

        existing[qid] = q_result

        # Save after each question
        atomic_write_json(results_path, list(existing.values()))

    cost = (total_in * 0.80 + total_out * 4.00) / 1_000_000
    log(f'  {subject} complete: ${cost:.2f}')
    return cost


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', default=None)
    args = parser.parse_args()

    api_key = os.environ['ANTHROPIC_API_KEY']
    subjects = [args.subject] if args.subject else ALL_SUBJECTS

    log(f'C8/C9 Generation — {len(subjects)} subjects')
    total_cost = 0

    for subject in subjects:
        try:
            cost = run_subject(subject, api_key)
            total_cost += cost
        except Exception as e:
            log(f'  {subject} FAILED: {e}')
            import traceback
            traceback.print_exc()

    log(f'Total cost: ${total_cost:.2f}')


if __name__ == '__main__':
    main()
