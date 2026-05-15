"""
Base Layer as a memory system condition — uses the same MiniLM-L6-v2 embeddings
and ChromaDB vector store as the production pipeline.

For each subject:
1. Embed all pre-extracted facts into a local ChromaDB collection
2. For each BP question, retrieve top-10 facts by cosine similarity
3. Generate C1_baselayer (retrieval only) and C3_baselayer (spec + retrieval)
4. Judge with 6-judge panel

Usage:
    python run_baselayer_condition.py                    # All 14 subjects
    python run_baselayer_condition.py --subject babur    # Single subject
    python run_baselayer_condition.py --phase judge      # Just judging
"""
import json, os, sys, time, re, argparse, shutil
from datetime import datetime, timezone
from pathlib import Path

import httpx
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
REPO_DIR = os.path.dirname(BASE_DIR)

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'
JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']
TOP_K = 10

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
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path):
    if not os.path.exists(path): return None
    with open(path, encoding='utf-8') as f: return json.load(f)


def get_results_dir(s):
    if s == 'hamerton': return os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(RESULTS_BASE, f'global_{s}')


def load_facts(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'shared_facts.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'facts.json')
    data = json.load(open(path, encoding='utf-8'))
    if isinstance(data, dict): facts = data.get('facts', [])
    else: facts = data
    return [f['text'] if isinstance(f, dict) else f for f in facts]


def load_battery(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'battery', 'questions_80.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'battery_v2.json')
    data = json.load(open(path, encoding='utf-8'))
    return [q for q in data['questions']
            if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


def load_spec(subject):
    if subject == 'hamerton':
        layers_dir = Path(f'{REPO_DIR}/data/hamerton/spec')
        sections = []
        for layer_name, filename in [
            ("ANCHORS", "anchors_v4.md"), ("CORE", "core_v4.md"),
            ("PREDICTIONS", "predictions_v4.md"),
        ]:
            fp = layers_dir / filename
            if not fp.exists(): continue
            content = fp.read_text(encoding='utf-8')
            marker = "## Injectable Block"
            idx = content.find(marker)
            if idx >= 0: block = content[idx + len(marker):].strip()
            else:
                sep = content.find("\n---\n")
                block = content[sep + 5:].strip() if sep >= 0 else content.strip()
            sections.append(f"## {layer_name}\n\n{block}")
        brief_file = layers_dir / "brief_v5_clean.md"
        if brief_file.exists():
            content = brief_file.read_text(encoding='utf-8')
            marker = "## Injectable Block"
            idx = content.find(marker)
            if idx >= 0: block = content[idx + len(marker):].strip()
            else:
                sep = content.find("\n---\n")
                block = content[sep + 5:].strip() if sep >= 0 else content.strip()
            sections.append(f"## UNIFIED BRIEF\n\n{block}")
        return "\n\n".join(sections)
    else:
        return open(f'{REPO_DIR}/data/global_subjects/{subject}/spec_production.md', encoding='utf-8').read()


# ═══════════════════════════════════════════════════════════════
# API HELPERS
# ═══════════════════════════════════════════════════════════════

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=1024, temperature=0, timeout=180):
    for attempt in range(3):
        try:
            kwargs = {'model': model, 'max_tokens': max_tokens, 'temperature': temperature,
                      'messages': [{'role': 'user', 'content': user_message}]}
            if system_prompt: kwargs['system'] = system_prompt
            resp = httpx.post('https://api.anthropic.com/v1/messages', json=kwargs,
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=timeout)
            resp.raise_for_status()
            d = resp.json()
            return {'text': d['content'][0]['text'], 'input_tokens': d['usage']['input_tokens'],
                    'output_tokens': d['usage']['output_tokens'], 'model': model}
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
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-haiku-4-5-20251001', None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'sonnet':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-sonnet-4-6', None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'opus':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-opus-4-6', None, prompt, max_tokens=8, timeout=60)
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


# ═══════════════════════════════════════════════════════════════
# BASE LAYER VECTOR RETRIEVAL
# ═══════════════════════════════════════════════════════════════

def build_collection(subject, facts, embed_model):
    """Build a ChromaDB collection for a subject's facts using MiniLM-L6-v2."""
    db_path = os.path.join(get_results_dir(subject), 'baselayer_vectors')
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    client = chromadb.PersistentClient(path=db_path)
    collection = client.create_collection(
        name=f'{subject}_facts',
        metadata={'hnsw:space': 'cosine'}
    )

    # Embed all facts
    log(f'  Embedding {len(facts)} facts...')
    embeddings = embed_model.encode(facts, show_progress_bar=False).tolist()

    # Add in batches (ChromaDB limit)
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


def retrieve_baselayer(query, collection, embed_model):
    """Retrieve top-10 facts using cosine similarity."""
    query_emb = embed_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_emb,
        n_results=TOP_K
    )
    return results['documents'][0] if results['documents'] else []


# ═══════════════════════════════════════════════════════════════
# PHASES
# ═══════════════════════════════════════════════════════════════

def phase_embed_and_retrieve(subjects, embed_model):
    log('PHASE A+B: EMBED + RETRIEVE')

    for subject in subjects:
        results_dir = get_results_dir(subject)
        retrieval_path = os.path.join(results_dir, 'baselayer_retrieval.json')

        if os.path.exists(retrieval_path):
            cached = load_json(retrieval_path)
            if cached and len(cached) >= 39:
                log(f'  {subject}: already retrieved, skipping')
                continue

        facts = load_facts(subject)
        questions = load_battery(subject)
        log(f'\n  {subject}: {len(facts)} facts, {len(questions)} questions')

        client, collection = build_collection(subject, facts, embed_model)

        retrieval_cache = {}
        for q in questions:
            qid = str(q['id'])
            t0 = time.time()
            retrieved = retrieve_baselayer(q['text'], collection, embed_model)
            latency = round((time.time() - t0) * 1000)

            retrieval_cache[qid] = {
                'question_id': q['id'],
                'system': 'baselayer',
                'facts_returned': len(retrieved),
                'fact_texts': retrieved,
                'latency_ms': latency,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            log(f'    Q{q["id"]}: {len(retrieved)} facts, {latency}ms')

        atomic_write_json(retrieval_path, retrieval_cache)
        # Clean up vectors (we have the retrieval cache now)
        try:
            db_path = os.path.join(results_dir, 'baselayer_vectors')
            if os.path.exists(db_path):
                shutil.rmtree(db_path)
        except Exception:
            pass  # Windows file lock — cleanup is optional


def phase_generate(subjects):
    log('PHASE C: GENERATE')
    api_key = os.environ['ANTHROPIC_API_KEY']

    for subject in subjects:
        results_dir = get_results_dir(subject)
        retrieval_path = os.path.join(results_dir, 'baselayer_retrieval.json')
        results_path = os.path.join(results_dir, 'baselayer_results.json')

        retrieval_cache = load_json(retrieval_path)
        if not retrieval_cache: continue

        questions = load_battery(subject)
        if len(retrieval_cache) < len(questions):
            log(f'  {subject}: retrieval incomplete, skipping')
            continue

        spec = load_spec(subject)
        existing = load_json(results_path) or []
        done_keys = set()
        for r in existing:
            for c in r.get('responses', {}):
                done_keys.add(f"{r['question_id']}_{c}")

        log(f'\n  {subject}: {len(done_keys)} responses done')

        for q in questions:
            qid = str(q['id'])
            cached = retrieval_cache.get(qid, {})
            facts = cached.get('fact_texts', [])

            q_result = None
            for r in existing:
                if r['question_id'] == q['id']:
                    q_result = r
                    break
            if not q_result:
                q_result = {
                    'question_id': q['id'], 'question_text': q['text'],
                    'held_out_passage': q.get('held_out_passage'),
                    'retrieval': {'facts_returned': len(facts), 'facts': facts},
                    'responses': {}, 'timestamp': datetime.now(timezone.utc).isoformat()
                }
                existing.append(q_result)

            if f"{q['id']}_C1_baselayer" not in done_keys and facts:
                ft = '\n'.join(f'- {f}' for f in facts)
                try:
                    resp = api_call_anthropic(api_key, RESPONSE_MODEL,
                        'The following facts were retrieved about this person.\n\n'
                        '=== RETRIEVED FACTS ===\n' + ft, q['text'])
                    q_result['responses']['C1_baselayer'] = resp
                    log(f'    Q{q["id"]} C1: {resp["output_tokens"]}t')
                except Exception as e:
                    q_result['responses']['C1_baselayer'] = {'error': str(e)}

            if f"{q['id']}_C3_baselayer" not in done_keys:
                if facts:
                    ft = '\n'.join(f'- {f}' for f in facts)
                    sys_prompt = ('The following is a behavioral specification describing your user — '
                        'how they think, decide, and act. You also have retrieved facts.\n\n'
                        '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                        '=== RETRIEVED FACTS ===\n' + ft)
                else:
                    sys_prompt = ('The following is a behavioral specification describing your user — '
                        'how they think, decide, and act.\n\n'
                        '=== BEHAVIORAL SPECIFICATION ===\n' + spec)
                try:
                    resp = api_call_anthropic(api_key, RESPONSE_MODEL, sys_prompt, q['text'])
                    q_result['responses']['C3_baselayer'] = resp
                    log(f'    Q{q["id"]} C3: {resp["output_tokens"]}t')
                except Exception as e:
                    q_result['responses']['C3_baselayer'] = {'error': str(e)}

            atomic_write_json(results_path, existing)


def phase_judge(subjects, judge_filter=None):
    log('PHASE D: JUDGE')
    api_keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
        'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY', ''),
    }
    judges_to_run = [judge_filter] if judge_filter else JUDGES
    conditions = ['C1_baselayer', 'C3_baselayer']

    for subject in subjects:
        results_dir = get_results_dir(subject)
        results = load_json(os.path.join(results_dir, 'baselayer_results.json'))
        if not results: continue

        if sum(1 for r in results if r.get('responses')) < 39:
            log(f'  {subject}: results incomplete, skipping')
            continue

        for judge_name in judges_to_run:
            judgments_path = os.path.join(results_dir, f'baselayer_judgments_{judge_name}.json')
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

            log(f'  {subject} / {judge_name}: {new_count} new')

        # Merge
        merged = []
        for jn in JUDGES:
            jp = os.path.join(results_dir, f'baselayer_judgments_{jn}.json')
            jdata = load_json(jp)
            if jdata: merged.extend(jdata)
        if merged:
            atomic_write_json(os.path.join(results_dir, 'baselayer_judgments_merged.json'), merged)


def phase_analyze(subjects):
    log('PHASE E: ANALYSIS')
    summary = {'system': 'baselayer', 'subjects': {}}

    for subject in subjects:
        results_dir = get_results_dir(subject)
        merged = load_json(os.path.join(results_dir, 'baselayer_judgments_merged.json'))
        if not merged: continue
        c1 = [j['score'] for j in merged if j['condition'] == 'C1_baselayer' and j['score'] > 0]
        c3 = [j['score'] for j in merged if j['condition'] == 'C3_baselayer' and j['score'] > 0]
        c1a = sum(c1) / len(c1) if c1 else 0
        c3a = sum(c3) / len(c3) if c3 else 0
        delta = ((c3a - c1a) / c1a * 100) if c1a > 0 else 0
        summary['subjects'][subject] = {
            'c1_avg': round(c1a, 2), 'c3_avg': round(c3a, 2),
            'improvement_pct': round(delta, 1), 'c1_n': len(c1), 'c3_n': len(c3)
        }
        log(f'  {subject:20s}  C1={c1a:.2f}  C3={c3a:.2f}  delta={delta:+.1f}%')

    atomic_write_json(os.path.join(RESULTS_BASE, 'baselayer_analysis.json'), summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', default=None)
    parser.add_argument('--phase', default='all', choices=['embed', 'generate', 'judge', 'analyze', 'all'])
    parser.add_argument('--judge', default=None)
    args = parser.parse_args()

    subjects = [args.subject] if args.subject else ALL_SUBJECTS

    log(f'Base Layer Condition -- {len(subjects)} subjects, phase={args.phase}')

    embed_model = None
    if args.phase in ('embed', 'all'):
        log('Loading embedding model...')
        embed_model = SentenceTransformer(EMBED_MODEL_NAME)
        phase_embed_and_retrieve(subjects, embed_model)

    if args.phase in ('generate', 'all'):
        phase_generate(subjects)

    if args.phase in ('judge', 'all'):
        phase_judge(subjects, judge_filter=args.judge)

    if args.phase in ('analyze', 'all'):
        phase_analyze(subjects)

    log('DONE')


if __name__ == '__main__':
    main()
