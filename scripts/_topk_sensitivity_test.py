"""
Top-K retrieval sensitivity test (Yung Wing only).

Tests the hypothesis that the C2a (spec) vs C1 (retrieval-only) gap reported in
the paper might be partly attributable to context-size differences (~500 tokens
of retrieved facts at K=10 vs ~9000 tokens of spec).

This script forks `run_baselayer_condition.py` to:
- Fix to a single subject (yung_wing)
- Take K as a CLI argument (--k 10/50/140)
- Build ChromaDB ONCE per run, then retrieve at the chosen K
- Generate C1' (retrieval only) and C3' (spec + retrieval) at the given K
- Run a 5-judge primary panel (no gemini_flash)
- Write outputs to `data/topk_test_20260428/yung_wing_K<K>_*.json`

No paper edits. Research-only output.

Usage:
    python _topk_sensitivity_test.py --k 10 --phase all
    python _topk_sensitivity_test.py --k 50 --phase generate
    python _topk_sensitivity_test.py --k 140 --phase judge
"""
import json
import os
import sys
import time
import re
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import httpx
import chromadb
from sentence_transformers import SentenceTransformer

try:
    import tiktoken
    _ENC = tiktoken.get_encoding('cl100k_base')
except Exception:
    _ENC = None

# Paths
REPO_DIR = 'C:/Users/Aarik/Anthropic/memory-study-repo'
SUBJECT = 'yung_wing'
SUBJECT_RESULTS_DIR = f'{REPO_DIR}/results/global_{SUBJECT}'
SUBJECT_SPEC_PATH = f'{REPO_DIR}/data/global_subjects/{SUBJECT}/spec_production.md'
OUT_DIR = f'{REPO_DIR}/data/topk_test_20260428'

# Models
RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'

# 5-judge primary panel (no gemini_flash, per task spec)
PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def atomic_write_json(path, data):
    tmp = path + '.tmp'
    for attempt in range(3):
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(path):
                os.replace(tmp, path)
            else:
                os.rename(tmp, path)
            return
        except PermissionError:
            if attempt < 2:
                time.sleep(2)
                try: os.remove(tmp)
                except: pass
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def count_tokens(text):
    """Count tokens using cl100k_base. Falls back to char/4 if tiktoken missing."""
    if _ENC is not None:
        try:
            return len(_ENC.encode(text))
        except Exception:
            pass
    return len(text) // 4


def load_facts():
    path = os.path.join(SUBJECT_RESULTS_DIR, 'facts.json')
    data = json.load(open(path, encoding='utf-8'))
    if isinstance(data, dict):
        facts = data.get('facts', [])
    else:
        facts = data
    return [f['text'] if isinstance(f, dict) else f for f in facts]


def load_battery():
    path = os.path.join(SUBJECT_RESULTS_DIR, 'battery_v2.json')
    data = json.load(open(path, encoding='utf-8'))
    return [q for q in data['questions']
            if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


def load_spec():
    return open(SUBJECT_SPEC_PATH, encoding='utf-8').read()


# API helpers (lifted from run_baselayer_condition.py)

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=1024,
                       temperature=0, timeout=180):
    for attempt in range(3):
        try:
            kwargs = {'model': model, 'max_tokens': max_tokens, 'temperature': temperature,
                      'messages': [{'role': 'user', 'content': user_message}]}
            if system_prompt:
                kwargs['system'] = system_prompt
            resp = httpx.post('https://api.anthropic.com/v1/messages', json=kwargs,
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=timeout)
            resp.raise_for_status()
            d = resp.json()
            return {'text': d['content'][0]['text'],
                    'input_tokens': d['usage']['input_tokens'],
                    'output_tokens': d['usage']['output_tokens'],
                    'model': model}
        except Exception:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def api_call_openai(api_key, model, prompt, max_tokens=8):
    for attempt in range(3):
        try:
            resp = httpx.post('https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': max_tokens, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                timeout=30)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def judge_prompt(held_out, response_text):
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
            '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
            'Rate 1-5:\n5=Predicts specific outcome\n4=General direction correct\n'
            '3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')


def parse_score(text):
    if not text:
        return 0
    match = re.search(r'[1-5]', text.strip())
    return int(match.group()) if match else 0


def run_judge(judge_name, prompt, api_keys):
    raw = ''
    try:
        if judge_name == 'haiku':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'],
                'claude-haiku-4-5-20251001', None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'sonnet':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'],
                'claude-sonnet-4-6', None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'opus':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'],
                'claude-opus-4-6', None, prompt, max_tokens=8, timeout=60)
            raw = r['text']
        elif judge_name == 'gpt4o':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-4o', prompt)
        elif judge_name == 'gpt54':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-5.4', prompt)
        else:
            return 0, f'unknown judge {judge_name}', True
    except Exception as e:
        return 0, str(e), True
    score = parse_score(raw)
    return score, raw, (score == 0)


# Vector retrieval (per-K)

def build_collection(facts, embed_model, k):
    """Build a ChromaDB collection. One per K to avoid lock conflicts on Windows."""
    db_path = os.path.join(OUT_DIR, f'_chroma_K{k}')
    if os.path.exists(db_path):
        try:
            shutil.rmtree(db_path)
        except Exception:
            pass

    client = chromadb.PersistentClient(path=db_path)
    collection = client.create_collection(
        name=f'{SUBJECT}_facts_k{k}',
        metadata={'hnsw:space': 'cosine'}
    )

    log(f'  Embedding {len(facts)} facts (one-time per run)...')
    embeddings = embed_model.encode(facts, show_progress_bar=False).tolist()

    batch_size = 500
    for i in range(0, len(facts), batch_size):
        batch_end = min(i + batch_size, len(facts))
        collection.add(
            ids=[f'fact_{j}' for j in range(i, batch_end)],
            embeddings=embeddings[i:batch_end],
            documents=facts[i:batch_end]
        )

    log(f'  Collection built: {collection.count()} facts')
    return client, collection


def retrieve(query, collection, embed_model, k):
    """Retrieve top-k facts using cosine similarity."""
    query_emb = embed_model.encode([query]).tolist()
    n = min(k, collection.count())
    results = collection.query(query_embeddings=query_emb, n_results=n)
    return results['documents'][0] if results['documents'] else []


# Phases

def phase_retrieve(k, embed_model):
    log(f'PHASE A+B: EMBED + RETRIEVE (K={k})')
    facts = load_facts()
    questions = load_battery()
    log(f'  {SUBJECT}: {len(facts)} facts in pool, {len(questions)} BP questions')

    actual_k = min(k, len(facts))
    if actual_k < k:
        log(f'  WARNING: requested K={k} > pool size {len(facts)}, using K={actual_k}')

    client, collection = build_collection(facts, embed_model, k)

    retrieval = {}
    for q in questions:
        qid = str(q['id'])
        t0 = time.time()
        retrieved = retrieve(q['text'], collection, embed_model, actual_k)
        latency = round((time.time() - t0) * 1000)

        # Measure actual context payload tokens (joined as it would be sent)
        payload = '\n'.join(f'- {f}' for f in retrieved)
        n_tokens = count_tokens(payload)

        retrieval[qid] = {
            'question_id': q['id'],
            'k_requested': k,
            'k_actual': actual_k,
            'fact_pool_size': len(facts),
            'facts_returned': len(retrieved),
            'fact_texts': retrieved,
            'context_tokens_cl100k': n_tokens,
            'context_chars': len(payload),
            'latency_ms': latency,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }

    out_path = os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_retrieval.json')
    atomic_write_json(out_path, retrieval)

    # Cleanup chroma db
    try:
        db_path = os.path.join(OUT_DIR, f'_chroma_K{k}')
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
    except Exception:
        pass

    return retrieval, actual_k


def phase_generate(k):
    log(f'PHASE C: GENERATE (K={k})')
    api_key = os.environ['ANTHROPIC_API_KEY']

    retrieval = load_json(os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_retrieval.json'))
    if not retrieval:
        log('  ERROR: no retrieval cache found, run --phase retrieve first')
        return

    questions = load_battery()
    spec = load_spec()
    spec_tokens = count_tokens(spec)
    log(f'  Spec size: {len(spec)} chars / {spec_tokens} tokens (cl100k)')

    results_path = os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_results.json')
    existing = load_json(results_path) or []
    done_keys = set()
    for r in existing:
        for c in r.get('responses', {}):
            done_keys.add(f"{r['question_id']}_{c}")

    log(f'  {len(done_keys)} responses already done')

    for q in questions:
        qid = str(q['id'])
        cached = retrieval.get(qid, {})
        facts = cached.get('fact_texts', [])

        q_result = None
        for r in existing:
            if r['question_id'] == q['id']:
                q_result = r
                break
        if not q_result:
            q_result = {
                'question_id': q['id'],
                'question_text': q['text'],
                'held_out_passage': q.get('held_out_passage'),
                'k_requested': k,
                'k_actual': cached.get('k_actual', k),
                'retrieval': {
                    'facts_returned': len(facts),
                    'context_tokens_cl100k': cached.get('context_tokens_cl100k'),
                },
                'responses': {},
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
            existing.append(q_result)

        # C1': retrieval only
        if f"{q['id']}_C1_prime" not in done_keys and facts:
            ft = '\n'.join(f'- {f}' for f in facts)
            try:
                resp = api_call_anthropic(api_key, RESPONSE_MODEL,
                    'The following facts were retrieved about this person.\n\n'
                    '=== RETRIEVED FACTS ===\n' + ft, q['text'])
                q_result['responses']['C1_prime'] = resp
                log(f'    Q{q["id"]} C1: {resp["output_tokens"]}t out, {resp["input_tokens"]}t in')
            except Exception as e:
                q_result['responses']['C1_prime'] = {'error': str(e)}

        # C3': spec + retrieval
        if f"{q['id']}_C3_prime" not in done_keys:
            if facts:
                ft = '\n'.join(f'- {f}' for f in facts)
                sys_prompt = ('The following is a behavioral specification describing your user, '
                    'how they think, decide, and act. You also have retrieved facts.\n\n'
                    '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                    '=== RETRIEVED FACTS ===\n' + ft)
            else:
                sys_prompt = ('The following is a behavioral specification describing your user, '
                    'how they think, decide, and act.\n\n'
                    '=== BEHAVIORAL SPECIFICATION ===\n' + spec)
            try:
                resp = api_call_anthropic(api_key, RESPONSE_MODEL, sys_prompt, q['text'])
                q_result['responses']['C3_prime'] = resp
                log(f'    Q{q["id"]} C3: {resp["output_tokens"]}t out, {resp["input_tokens"]}t in')
            except Exception as e:
                q_result['responses']['C3_prime'] = {'error': str(e)}

        atomic_write_json(results_path, existing)


def phase_judge(k):
    log(f'PHASE D: JUDGE (K={k}, 5-judge primary)')
    api_keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
    }

    results = load_json(os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_results.json'))
    if not results:
        log('  ERROR: no results found, run --phase generate first')
        return

    judgments_path = os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_judgments.json')
    existing = load_json(judgments_path) or []
    done_keys = set(f"{j['question_id']}_{j['condition']}_{j['judge']}"
                    for j in existing)

    conditions = ['C1_prime', 'C3_prime']

    for q_result in results:
        qid = q_result['question_id']
        held_out = q_result.get('held_out_passage', '')
        if not held_out:
            continue

        for cond in conditions:
            resp = q_result.get('responses', {}).get(cond, {})
            resp_text = resp.get('text', '')
            for judge_name in PRIMARY_JUDGES:
                key = f'{qid}_{cond}_{judge_name}'
                if key in done_keys:
                    continue
                if not resp_text or 'error' in resp:
                    existing.append({
                        'question_id': qid, 'condition': cond, 'judge': judge_name,
                        'score': 0, 'parse_failure': True,
                        'note': 'no response',
                    })
                    done_keys.add(key)
                    continue
                score, raw, pf = run_judge(judge_name,
                                           judge_prompt(held_out, resp_text),
                                           api_keys)
                existing.append({
                    'question_id': qid, 'condition': cond, 'judge': judge_name,
                    'score': score,
                    'raw_response': raw if pf else '',
                    'parse_failure': pf,
                })
                done_keys.add(key)
                atomic_write_json(judgments_path, existing)
        log(f'    Q{qid}: judged')


def phase_summary(k):
    """Quick on-screen aggregate so we can sanity-check before report."""
    judgments = load_json(os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_judgments.json'))
    if not judgments:
        log(f'  K={k}: no judgments file')
        return
    c1 = [j['score'] for j in judgments
          if j['condition'] == 'C1_prime' and j['score'] > 0]
    c3 = [j['score'] for j in judgments
          if j['condition'] == 'C3_prime' and j['score'] > 0]
    c1m = sum(c1)/len(c1) if c1 else 0
    c3m = sum(c3)/len(c3) if c3 else 0
    log(f'  K={k}: C1\' n={len(c1)} mean={c1m:.3f}  C3\' n={len(c3)} mean={c3m:.3f}  '
        f'delta={c3m - c1m:+.3f}')

    # Also show context-payload token stats
    retrieval = load_json(os.path.join(OUT_DIR, f'{SUBJECT}_K{k}_retrieval.json'))
    if retrieval:
        toks = [r['context_tokens_cl100k'] for r in retrieval.values()
                if r.get('context_tokens_cl100k')]
        if toks:
            log(f'    avg context tokens: {sum(toks)/len(toks):.0f}  '
                f'min={min(toks)}  max={max(toks)}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=int, required=True,
                        help='Top-K for retrieval (10 / 50 / 140 etc.)')
    parser.add_argument('--phase', default='all',
                        choices=['retrieve', 'generate', 'judge', 'summary', 'all'])
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    log(f'TopK Sensitivity -- subject={SUBJECT}, K={args.k}, phase={args.phase}')

    if args.phase in ('retrieve', 'all'):
        log('Loading embedding model...')
        embed_model = SentenceTransformer(EMBED_MODEL_NAME)
        phase_retrieve(args.k, embed_model)

    if args.phase in ('generate', 'all'):
        phase_generate(args.k)

    if args.phase in ('judge', 'all'):
        phase_judge(args.k)

    phase_summary(args.k)
    log('DONE')


if __name__ == '__main__':
    main()
