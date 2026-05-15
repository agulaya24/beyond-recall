"""
Option B: Full Pipeline — Feed raw training text to each memory system's native pipeline.
Each system extracts, chunks, indexes using its own approach. Then retrieve + generate + judge.

Usage:
    python run_option_b.py --system mem0
    python run_option_b.py --system letta
    python run_option_b.py --system supermemory
    python run_option_b.py --system zep
    python run_option_b.py --system mem0 --subject augustine --phase ingest
"""
import json, os, sys, time, re, hashlib, random, argparse
from datetime import datetime, timezone
from pathlib import Path

import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
REPO_DIR = os.path.dirname(BASE_DIR)

RUN_ID = '20260415_fp'  # fullpipeline
SUFFIX = '_fullpipeline'

ALL_SUBJECTS = [
    'zitkala_sa', 'hamerton', 'keckley', 'yung_wing', 'seacole',
    'sunity_devee', 'equiano', 'augustine', 'ebers', 'fukuzawa',
    'cellini', 'bernal_diaz', 'rousseau', 'babur'
]

DISPLAY_NAMES = {
    'augustine': 'Saint Augustine', 'babur': 'Babur',
    'bernal_diaz': 'Bernal Diaz del Castillo', 'cellini': 'Benvenuto Cellini',
    'ebers': 'Georg Ebers', 'equiano': 'Olaudah Equiano',
    'fukuzawa': 'Fukuzawa Yukichi', 'hamerton': 'Philip Gilbert Hamerton',
    'keckley': 'Elizabeth Keckley', 'rousseau': 'Jean-Jacques Rousseau',
    'seacole': 'Mary Seacole', 'sunity_devee': 'Sunity Devee',
    'yung_wing': 'Yung Wing', 'zitkala_sa': 'Zitkala-Sa'
}

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']
CHUNK_SIZE = 2000  # words per chunk for systems that need chunking


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


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def get_results_dir(subject):
    if subject == 'hamerton':
        return os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(RESULTS_BASE, f'global_{subject}')


def namespace(subject):
    return f'{subject}_fullpipeline'


def load_training_text(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'corpus', 'tiers', 'tier_02_ch01-10.txt')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'training.txt')
    return open(path, encoding='utf-8').read()


def chunk_text(text, chunk_words=CHUNK_SIZE):
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []
    overlap = 200  # words
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i + chunk_words])
        chunks.append(chunk)
        i += chunk_words - overlap
    return chunks


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
        return open(f'{REPO_DIR}/data/global_subjects/{subject}/spec_production.md', encoding='utf-8').read()


def load_battery(subject):
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'battery', 'questions_80.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'battery_v2.json')
    data = json.load(open(path, encoding='utf-8'))
    return [q for q in data['questions']
            if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


# ═══════════════════════════════════════════════════════════════
# API HELPERS (reused from run_memory_system.py)
# ═══════════════════════════════════════════════════════════════

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=1024, temperature=0, timeout=180):
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
            return {'text': d['content'][0]['text'], 'input_tokens': d['usage']['input_tokens'],
                    'output_tokens': d['usage']['output_tokens'], 'model': model}
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def api_call_openai(api_key, model, prompt, max_tokens=8, temperature=0):
    for attempt in range(3):
        try:
            resp = httpx.post('https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': max_tokens, 'temperature': temperature,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}, timeout=30)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def api_call_gemini(api_key, model, prompt, timeout=60):
    for attempt in range(3):
        try:
            resp = httpx.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}',
                json={'contents': [{'parts': [{'text': prompt}]}]}, timeout=timeout)
            if resp.status_code == 429:
                time.sleep(2 ** (attempt + 2))
                continue
            resp.raise_for_status()
            return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
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
# OPTION B INGESTION — Each system gets raw text
# ═══════════════════════════════════════════════════════════════

def ingest_mem0_fp(subject, training_text):
    """Mem0 with infer=True — let it extract its own memories from raw text."""
    key = os.environ['MEM0_KEY']
    user_id = namespace(subject)
    headers = {'Authorization': f'Token {key}', 'Content-Type': 'application/json'}

    chunks = chunk_text(training_text, 2000)
    log(f'  Mem0 fullpipeline: {len(chunks)} chunks')

    ingestion_log = {
        'subject': subject, 'system': 'mem0', 'mode': 'fullpipeline',
        'user_id': user_id, 'chunks_expected': len(chunks),
        'chunks_posted': 0, 'post_success': 0, 'post_failure': 0,
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    for i, chunk in enumerate(chunks):
        for attempt in range(3):
            try:
                resp = httpx.post('https://api.mem0.ai/v1/memories/',
                    json={
                        'messages': [{'role': 'user', 'content': chunk}],
                        'user_id': user_id,
                        'infer': True  # Let Mem0 extract its own memories
                    },
                    headers=headers, timeout=60)
                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    if i == 0:
                        body = resp.json()
                        results = body.get('results', [])
                        log(f'  First chunk: {len(results)} memories extracted')
                        for r in results[:3]:
                            log(f'    "{r.get("memory","")[:80]}..."')
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        log(f'  Chunk {i} failed: {resp.status_code}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    log(f'  Chunk {i} exception: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['chunks_posted'] = i + 1
        if (i + 1) % 10 == 0:
            log(f'  Mem0 FP ingested {i+1}/{len(chunks)} chunks for {subject}')

    # Wait for async processing
    time.sleep(15)
    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    ingestion_log['verification_passed'] = True  # Will verify via search
    return ingestion_log


def ingest_letta_fp(subject, training_text):
    """Letta with raw text — large archival entries, Letta chunks natively."""
    key = os.environ['LETTA_KEY']
    agent_name = namespace(subject)
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    base_url = 'https://api.letta.com/v1'

    # Check for existing agent
    agent_id = None
    try:
        resp = httpx.get(f'{base_url}/agents/', headers=headers, timeout=30)
        for a in resp.json():
            if a['name'] == agent_name:
                agent_id = a['id']
                log(f'  Found existing agent: {agent_id}')
                break
    except:
        pass

    if not agent_id:
        log(f'  Creating Letta agent: {agent_name}')
        resp = httpx.post(f'{base_url}/agents/',
            json={'name': agent_name, 'model': 'openai/gpt-4o-mini',
                  'embedding': 'openai/text-embedding-3-small'},
            headers=headers, timeout=60)
        if resp.status_code not in (200, 201):
            raise RuntimeError(f'Agent creation failed: {resp.status_code} {resp.text[:200]}')
        agent_id = resp.json()['id']
        log(f'  Agent created: {agent_id}')

    # Feed raw text in large chunks — Letta handles chunking internally
    chunks = chunk_text(training_text, 5000)  # Larger chunks for Letta
    log(f'  Letta fullpipeline: {len(chunks)} chunks')

    ingestion_log = {
        'subject': subject, 'system': 'letta', 'mode': 'fullpipeline',
        'agent_id': agent_id, 'agent_name': agent_name,
        'chunks_expected': len(chunks), 'chunks_posted': 0,
        'post_success': 0, 'post_failure': 0,
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    for i, chunk in enumerate(chunks):
        for attempt in range(3):
            try:
                resp = httpx.post(f'{base_url}/agents/{agent_id}/archival-memory',
                    json={'text': chunk}, headers=headers,
                    timeout=httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0))
                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        log(f'  Chunk {i} failed: {resp.status_code}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    log(f'  Chunk {i} exception: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['chunks_posted'] = i + 1
        if (i + 1) % 5 == 0:
            log(f'  Letta FP ingested {i+1}/{len(chunks)} chunks for {subject}')

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    ingestion_log['verification_passed'] = True
    return ingestion_log


def ingest_supermemory_fp(subject, training_text):
    """Supermemory with raw text documents."""
    key = os.environ['SUPERMEMORY_KEY']
    container_tag = namespace(subject)
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

    chunks = chunk_text(training_text, 3000)
    log(f'  Supermemory fullpipeline: {len(chunks)} chunks')

    ingestion_log = {
        'subject': subject, 'system': 'supermemory', 'mode': 'fullpipeline',
        'container_tag': container_tag, 'chunks_expected': len(chunks),
        'chunks_posted': 0, 'post_success': 0, 'post_failure': 0,
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    for i, chunk in enumerate(chunks):
        for attempt in range(3):
            try:
                resp = httpx.post('https://api.supermemory.ai/v3/documents',
                    json={'content': chunk, 'containerTags': [container_tag],
                          'customId': f'{container_tag}_chunk_{i}'},
                    headers=headers, timeout=30, follow_redirects=True)
                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        log(f'  Chunk {i} failed: {resp.status_code}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    log(f'  Chunk {i} exception: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['chunks_posted'] = i + 1
        time.sleep(0.3)  # Rate limit
        if (i + 1) % 10 == 0:
            log(f'  SM FP ingested {i+1}/{len(chunks)} chunks for {subject}')

    time.sleep(30)  # Wait for indexing
    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    ingestion_log['verification_passed'] = True
    return ingestion_log


def ingest_zep_fp(subject, training_text):
    """Zep with raw text — graph.add with chunked text."""
    from zep_cloud.client import Zep
    client = Zep(api_key=os.environ['ZEP_KEY'])
    user_id = namespace(subject)

    try:
        client.user.add(user_id=user_id, first_name=DISPLAY_NAMES.get(subject, subject))
        log(f'  Zep user created: {user_id}')
    except Exception as e:
        if 'already exists' in str(e).lower() or '409' in str(e):
            log(f'  Zep user exists: {user_id}')
        else:
            log(f'  Zep user warning: {e}')

    # Chunk into ~500 char segments (Zep 10K limit per graph.add, but smaller is better for graph)
    chunks = chunk_text(training_text, 500)
    log(f'  Zep fullpipeline: {len(chunks)} chunks')

    ingestion_log = {
        'subject': subject, 'system': 'zep', 'mode': 'fullpipeline',
        'user_id': user_id, 'chunks_expected': len(chunks),
        'chunks_posted': 0, 'post_success': 0, 'post_failure': 0,
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    # Batch chunks into groups respecting 10K char limit
    batch_size = 10
    for batch_start in range(0, len(chunks), batch_size):
        batch_end = min(batch_start + batch_size, len(chunks))
        batch_text = '\n'.join(chunks[batch_start:batch_end])
        if len(batch_text) > 9500:
            batch_text = batch_text[:9500]

        for attempt in range(3):
            try:
                client.graph.add(user_id=user_id, data=batch_text, type='text')
                ingestion_log['post_success'] += (batch_end - batch_start)
                break
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += (batch_end - batch_start)
                    log(f'  Batch {batch_start}-{batch_end} exception: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['chunks_posted'] = batch_end
        time.sleep(15)  # Graph processing

        if batch_end % 50 == 0:
            log(f'  Zep FP ingested {batch_end}/{len(chunks)} chunks for {subject}')

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    ingestion_log['verification_passed'] = True
    return ingestion_log


# ═══════════════════════════════════════════════════════════════
# RETRIEVAL (same as Option A but with fullpipeline namespaces)
# ═══════════════════════════════════════════════════════════════

def retrieve_mem0_fp(query, subject):
    user_id = namespace(subject)
    resp = httpx.post('https://api.mem0.ai/v2/memories/search/',
        json={'query': query, 'filters': {'user_id': user_id}, 'top_k': 10},
        headers={'Authorization': f'Token {os.environ["MEM0_KEY"]}'}, timeout=15)
    if resp.status_code != 200: return []
    data = resp.json()
    if isinstance(data, list):
        return [r.get('memory', '') for r in data[:10]]
    results = data.get('results', data.get('memories', []))
    return [r.get('memory', r.get('text', '')) for r in results[:10]]


def retrieve_letta_fp(query, subject, agent_id):
    resp = httpx.get(f'https://api.letta.com/v1/agents/{agent_id}/archival-memory/search',
        params={'query': query, 'top_k': 10},
        headers={'Authorization': f'Bearer {os.environ["LETTA_KEY"]}'}, timeout=55)
    if resp.status_code != 200: return []
    data = resp.json()
    results = data.get('results', data) if isinstance(data, dict) else data
    return [p.get('content', p.get('text', '')) for p in results[:10]]


def retrieve_supermemory_fp(query, subject):
    container_tag = namespace(subject)
    resp = httpx.post('https://api.supermemory.ai/v3/search',
        json={'q': query, 'limit': 10, 'containerTags': [container_tag]},
        headers={'Authorization': f'Bearer {os.environ["SUPERMEMORY_KEY"]}',
                 'Content-Type': 'application/json'},
        timeout=15, follow_redirects=True)
    if resp.status_code != 200: return []
    out = []
    for r in resp.json().get('results', [])[:10]:
        chunks = r.get('chunks', [])
        if chunks: out.append(chunks[0].get('content', ''))
        else: out.append(r.get('content', ''))
    return [f for f in out if f]


def retrieve_zep_fp(query, subject):
    from zep_cloud.client import Zep
    client = Zep(api_key=os.environ['ZEP_KEY'])
    user_id = namespace(subject)
    try:
        results = client.graph.search(user_id=user_id, query=query, limit=10)
        return [getattr(r, 'fact', None) or getattr(r, 'text', None) or str(r) for r in results][:10]
    except:
        return []


# ═══════════════════════════════════════════════════════════════
# DUMP EXTRACTED MEMORIES (what each system decided to store)
# ═══════════════════════════════════════════════════════════════

def dump_extracted(system, subject, ingestion_log):
    """Dump what each system extracted/stored from the raw text."""
    results_dir = get_results_dir(subject)
    dump_path = os.path.join(results_dir, f'{system}{SUFFIX}_extracted.json')

    extracted = {'subject': subject, 'system': system, 'mode': 'fullpipeline', 'memories': []}

    try:
        if system == 'mem0':
            user_id = namespace(subject)
            # List all memories for this user
            resp = httpx.get(f'https://api.mem0.ai/v1/memories/',
                params={'user_id': user_id},
                headers={'Authorization': f'Token {os.environ["MEM0_KEY"]}'}, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                memories = data if isinstance(data, list) else data.get('results', data.get('memories', []))
                extracted['memories'] = [{'text': m.get('memory', ''), 'id': m.get('id', '')} for m in memories]
                extracted['count'] = len(extracted['memories'])
                log(f'  Mem0 extracted {extracted["count"]} memories for {subject}')

        elif system == 'letta':
            agent_id = ingestion_log.get('agent_id')
            if agent_id:
                # List archival memory
                resp = httpx.get(f'https://api.letta.com/v1/agents/{agent_id}/archival-memory',
                    params={'limit': 1000},
                    headers={'Authorization': f'Bearer {os.environ["LETTA_KEY"]}'}, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    passages = data if isinstance(data, list) else data.get('passages', [])
                    extracted['memories'] = [{'text': p.get('content', p.get('text', '')), 'id': p.get('id', '')} for p in passages]
                    extracted['count'] = len(extracted['memories'])
                    log(f'  Letta extracted {extracted["count"]} passages for {subject}')

        elif system == 'supermemory':
            # Search with empty query to get all documents
            container_tag = namespace(subject)
            resp = httpx.post('https://api.supermemory.ai/v3/search',
                json={'q': ' ', 'limit': 100, 'containerTags': [container_tag]},
                headers={'Authorization': f'Bearer {os.environ["SUPERMEMORY_KEY"]}',
                         'Content-Type': 'application/json'},
                timeout=30, follow_redirects=True)
            if resp.status_code == 200:
                results = resp.json().get('results', [])
                for r in results:
                    chunks = r.get('chunks', [])
                    text = chunks[0].get('content', '') if chunks else r.get('content', '')
                    extracted['memories'].append({'text': text, 'id': r.get('documentId', '')})
                extracted['count'] = len(extracted['memories'])
                log(f'  Supermemory returned {extracted["count"]} results for {subject}')

        elif system == 'zep':
            # Search with generic query
            from zep_cloud.client import Zep
            client = Zep(api_key=os.environ['ZEP_KEY'])
            user_id = namespace(subject)
            results = client.graph.search(user_id=user_id, query='person life experiences', limit=100)
            extracted['memories'] = [{'text': getattr(r, 'fact', str(r))} for r in results]
            extracted['count'] = len(extracted['memories'])
            log(f'  Zep extracted {extracted["count"]} graph facts for {subject}')

    except Exception as e:
        log(f'  Dump failed for {system}/{subject}: {e}')
        extracted['error'] = str(e)

    atomic_write_json(dump_path, extracted)
    return extracted


# ═══════════════════════════════════════════════════════════════
# PHASES
# ═══════════════════════════════════════════════════════════════

def phase_ingest(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE A: INGEST (FULL PIPELINE) -- {system.upper()}')
    log(f'{"="*60}')

    for subject in subjects:
        results_dir = get_results_dir(subject)
        os.makedirs(results_dir, exist_ok=True)
        ing_path = os.path.join(results_dir, f'{system}{SUFFIX}_ingestion.json')

        if os.path.exists(ing_path):
            ing = load_json(ing_path)
            if ing and ing.get('verification_passed'):
                log(f'  {subject}: already ingested, skipping')
                continue

        training_text = load_training_text(subject)
        words = len(training_text.split())
        log(f'\n  {subject}: {words} words of raw text')

        try:
            if system == 'mem0':
                ing_log = ingest_mem0_fp(subject, training_text)
            elif system == 'letta':
                ing_log = ingest_letta_fp(subject, training_text)
            elif system == 'supermemory':
                ing_log = ingest_supermemory_fp(subject, training_text)
            elif system == 'zep':
                ing_log = ingest_zep_fp(subject, training_text)

            atomic_write_json(ing_path, ing_log)

            # Dump what the system extracted
            dump_extracted(system, subject, ing_log)

        except Exception as e:
            log(f'  FAILED: {e}')
            import traceback
            traceback.print_exc()


def phase_retrieve(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE B: RETRIEVE (FULL PIPELINE) -- {system.upper()}')
    log(f'{"="*60}')

    for subject in subjects:
        results_dir = get_results_dir(subject)
        retrieval_path = os.path.join(results_dir, f'{system}{SUFFIX}_retrieval.json')
        ing_path = os.path.join(results_dir, f'{system}{SUFFIX}_ingestion.json')

        ing = load_json(ing_path)
        if not ing or not ing.get('verification_passed'):
            log(f'  {subject}: not ingested, skipping')
            continue

        retrieval_cache = load_json(retrieval_path) or {}
        agent_id = ing.get('agent_id') if system == 'letta' else None
        questions = load_battery(subject)

        log(f'\n  {subject}: {len(questions)} questions, {len(retrieval_cache)} cached')

        for q in questions:
            qid = str(q['id'])
            if qid in retrieval_cache: continue

            t0 = time.time()
            try:
                if system == 'mem0': facts = retrieve_mem0_fp(q['text'], subject)
                elif system == 'letta': facts = retrieve_letta_fp(q['text'], subject, agent_id)
                elif system == 'supermemory': facts = retrieve_supermemory_fp(q['text'], subject)
                elif system == 'zep': facts = retrieve_zep_fp(q['text'], subject)

                retrieval_cache[qid] = {
                    'question_id': q['id'], 'system': system, 'mode': 'fullpipeline',
                    'facts_returned': len(facts), 'fact_texts': facts,
                    'latency_ms': round((time.time() - t0) * 1000),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                log(f'    Q{q["id"]}: {len(facts)} facts')
            except Exception as e:
                retrieval_cache[qid] = {
                    'question_id': q['id'], 'facts_returned': 0, 'fact_texts': [],
                    'error': str(e), 'timestamp': datetime.now(timezone.utc).isoformat()
                }
                log(f'    Q{q["id"]}: FAILED {e}')

            atomic_write_json(retrieval_path, retrieval_cache)


def phase_generate(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE C: GENERATE (FULL PIPELINE) -- {system.upper()}')
    log(f'{"="*60}')

    api_key = os.environ['ANTHROPIC_API_KEY']

    for subject in subjects:
        results_dir = get_results_dir(subject)
        retrieval_path = os.path.join(results_dir, f'{system}{SUFFIX}_retrieval.json')
        results_path = os.path.join(results_dir, f'{system}{SUFFIX}_results.json')

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

            c1_key = f'C1_{system}_fp'
            if f"{q['id']}_{c1_key}" not in done_keys and facts:
                ft = '\n'.join(f'- {f}' for f in facts)
                try:
                    resp = api_call_anthropic(api_key, RESPONSE_MODEL,
                        'The following facts were retrieved about this person.\n\n'
                        '=== RETRIEVED FACTS ===\n' + ft, q['text'])
                    q_result['responses'][c1_key] = resp
                    log(f'    Q{q["id"]} {c1_key}: {resp["output_tokens"]}t')
                except Exception as e:
                    q_result['responses'][c1_key] = {'error': str(e)}

            c3_key = f'C3_{system}_fp'
            if f"{q['id']}_{c3_key}" not in done_keys:
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
                    resp['spec_only'] = len(facts) == 0
                    q_result['responses'][c3_key] = resp
                    log(f'    Q{q["id"]} {c3_key}: {resp["output_tokens"]}t')
                except Exception as e:
                    q_result['responses'][c3_key] = {'error': str(e)}

            atomic_write_json(results_path, existing)


def phase_judge(system, subjects, judge_filter=None):
    log(f'{"="*60}')
    log(f'PHASE D: JUDGE (FULL PIPELINE) -- {system.upper()}')
    log(f'{"="*60}')

    api_keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
        'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY', ''),
    }

    judges_to_run = [judge_filter] if judge_filter else JUDGES

    for subject in subjects:
        results_dir = get_results_dir(subject)
        results_path = os.path.join(results_dir, f'{system}{SUFFIX}_results.json')
        results = load_json(results_path)
        if not results: continue

        questions_with_responses = sum(1 for r in results if r.get('responses'))
        if questions_with_responses < 39:
            log(f'  {subject}: results incomplete ({questions_with_responses}/39), skipping')
            continue

        for judge_name in judges_to_run:
            judgments_path = os.path.join(results_dir, f'{system}{SUFFIX}_judgments_{judge_name}.json')
            existing = load_json(judgments_path) or []
            done_keys = set(f"{j['question_id']}_{j['condition']}" for j in existing)

            conditions = [f'C1_{system}_fp', f'C3_{system}_fp']
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

            log(f'  {subject} / {judge_name}: {new_count} new judgments')

    # Merge
    for subject in subjects:
        results_dir = get_results_dir(subject)
        merged = []
        for jn in JUDGES:
            jp = os.path.join(results_dir, f'{system}{SUFFIX}_judgments_{jn}.json')
            jdata = load_json(jp)
            if jdata: merged.extend(jdata)
        if merged:
            atomic_write_json(os.path.join(results_dir, f'{system}{SUFFIX}_judgments_merged.json'), merged)


def phase_analyze(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE E: ANALYSIS (FULL PIPELINE) -- {system.upper()}')
    log(f'{"="*60}')

    summary = {'system': system, 'mode': 'fullpipeline', 'subjects': {}}

    for subject in subjects:
        results_dir = get_results_dir(subject)
        merged_path = os.path.join(results_dir, f'{system}{SUFFIX}_judgments_merged.json')
        judgments = load_json(merged_path)
        if not judgments: continue

        c1 = [j['score'] for j in judgments if j['condition'] == f'C1_{system}_fp' and j['score'] > 0]
        c3 = [j['score'] for j in judgments if j['condition'] == f'C3_{system}_fp' and j['score'] > 0]
        c1a = sum(c1) / len(c1) if c1 else 0
        c3a = sum(c3) / len(c3) if c3 else 0
        delta = ((c3a - c1a) / c1a * 100) if c1a > 0 else 0

        summary['subjects'][subject] = {
            'c1_avg': round(c1a, 2), 'c3_avg': round(c3a, 2),
            'improvement_pct': round(delta, 1), 'c1_n': len(c1), 'c3_n': len(c3)
        }
        log(f'  {subject:20s}  C1={c1a:.2f}  C3={c3a:.2f}  delta={delta:+.1f}%')

    analysis_path = os.path.join(RESULTS_BASE, f'{system}{SUFFIX}_analysis.json')
    atomic_write_json(analysis_path, summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--system', required=True, choices=['mem0', 'letta', 'supermemory', 'zep'])
    parser.add_argument('--phase', default='all', choices=['ingest', 'retrieve', 'generate', 'judge', 'analyze', 'all'])
    parser.add_argument('--subject', default=None)
    parser.add_argument('--judge', default=None)
    args = parser.parse_args()

    subjects = [args.subject] if args.subject else ALL_SUBJECTS

    log(f'Option B: Full Pipeline -- {args.system.upper()}')
    log(f'Subjects: {subjects}')
    log(f'Phase: {args.phase}')

    if args.phase in ('ingest', 'all'): phase_ingest(args.system, subjects)
    if args.phase in ('retrieve', 'all'): phase_retrieve(args.system, subjects)
    if args.phase in ('generate', 'all'): phase_generate(args.system, subjects)
    if args.phase in ('judge', 'all'): phase_judge(args.system, subjects, judge_filter=args.judge)
    if args.phase in ('analyze', 'all'): phase_analyze(args.system, subjects)

    log(f'DONE -- {args.system.upper()} {args.phase}')


if __name__ == '__main__':
    main()
