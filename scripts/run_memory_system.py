"""
Memory Systems Expansion — Run 4 memory systems x 14 subjects.

Each system runs independently with own checkpoints. Launch one per terminal:
    python run_memory_system.py --system mem0
    python run_memory_system.py --system letta
    python run_memory_system.py --system supermemory
    python run_memory_system.py --system zep

Phases: ingest → retrieve → generate → judge
    python run_memory_system.py --system mem0 --phase ingest
    python run_memory_system.py --system mem0 --phase retrieve
    python run_memory_system.py --system mem0 --phase generate
    python run_memory_system.py --system mem0 --phase judge
    python run_memory_system.py --system mem0 --phase judge --judge opus
    python run_memory_system.py --system mem0 --phase all          # default

Test on one subject first:
    python run_memory_system.py --system mem0 --subject augustine --phase ingest
"""
import json, os, sys, time, re, hashlib, subprocess, argparse, random
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
REPO_DIR = 'C:/Users/Aarik/Anthropic/memory-study-repo'

RUN_ID = '20260415'  # Run-scoped namespace prefix

# All 14 subjects sorted by fact count ascending (small first for early verification)
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

# Judge models
JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']

LOG_FILE = None  # Set in main()


# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    if LOG_FILE:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


# ═══════════════════════════════════════════════════════════════
# ATOMIC FILE I/O
# ═══════════════════════════════════════════════════════════════

def atomic_write_json(path, data):
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp_path, path)
    else:
        os.rename(tmp_path, path)


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════
# DATA LOADERS
# ═══════════════════════════════════════════════════════════════

def get_results_dir(subject):
    """Get results directory for a subject."""
    if subject == 'hamerton':
        return os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(RESULTS_BASE, f'global_{subject}')


def load_facts(subject):
    """Load pre-extracted facts for a subject."""
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'shared_facts.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'facts.json')
    data = json.load(open(path, encoding='utf-8'))
    if isinstance(data, dict):
        facts = data.get('facts', [])
    else:
        facts = data
    return [f['text'] if isinstance(f, dict) else f for f in facts]


def load_battery(subject):
    """Load BP questions (39 with held_out_passage) for a subject."""
    if subject == 'hamerton':
        path = os.path.join(BASE_DIR, 'battery', 'questions_80.json')
    else:
        path = os.path.join(RESULTS_BASE, f'global_{subject}', 'battery_v2.json')
    data = json.load(open(path, encoding='utf-8'))
    questions = data['questions']
    # Filter to BP with held_out_passage only
    bp = [q for q in questions if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]
    return bp


def load_spec(subject):
    """Load production spec for a subject."""
    if subject == 'hamerton':
        # Hamerton uses full layer stack
        layers_dir = Path(f'{REPO_DIR}/data/hamerton/spec')
        sections = []
        for layer_name, filename in [
            ("ANCHORS", "anchors_v4.md"),
            ("CORE", "core_v4.md"),
            ("PREDICTIONS", "predictions_v4.md"),
        ]:
            filepath = layers_dir / filename
            if not filepath.exists():
                continue
            content = filepath.read_text(encoding='utf-8')
            marker = "## Injectable Block"
            idx = content.find(marker)
            if idx >= 0:
                block = content[idx + len(marker):].strip()
            else:
                sep = content.find("\n---\n")
                block = content[sep + 5:].strip() if sep >= 0 else content.strip()
            sections.append(f"## {layer_name}\n\n{block}")
        # Add brief
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


# ═══════════════════════════════════════════════════════════════
# API CALL HELPERS
# ═══════════════════════════════════════════════════════════════

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=1024, temperature=0, timeout=180):
    for attempt in range(3):
        try:
            kwargs = {
                'model': model, 'max_tokens': max_tokens, 'temperature': temperature,
                'messages': [{'role': 'user', 'content': user_message}]
            }
            if system_prompt:
                kwargs['system'] = system_prompt
            resp = httpx.post('https://api.anthropic.com/v1/messages',
                json=kwargs,
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=timeout)
            resp.raise_for_status()
            d = resp.json()
            return {
                'text': d['content'][0]['text'],
                'input_tokens': d['usage']['input_tokens'],
                'output_tokens': d['usage']['output_tokens'],
                'model': model
            }
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                log(f'    Retry {attempt+1}/3 after {wait}s: {e}')
                time.sleep(wait)
            else:
                raise


def api_call_openai(api_key, model, prompt, max_tokens=8, temperature=0):
    for attempt in range(3):
        try:
            resp = httpx.post('https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': max_tokens, 'temperature': temperature,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                timeout=30)
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
                json={'contents': [{'parts': [{'text': prompt}]}]},
                timeout=timeout)
            if resp.status_code == 429:
                wait = 2 ** (attempt + 2)
                log(f'    Gemini 429, waiting {wait}s')
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


# ═══════════════════════════════════════════════════════════════
# JUDGE INFRASTRUCTURE
# ═══════════════════════════════════════════════════════════════

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
    match = re.search(r'[1-5]', text.strip())
    return int(match.group()) if match else 0


def run_judge(judge_name, prompt, api_keys):
    raw = ''
    try:
        if judge_name == 'haiku':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-haiku-4-5-20251001',
                                   None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'sonnet':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-sonnet-4-6',
                                   None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'opus':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], 'claude-opus-4-6',
                                   None, prompt, max_tokens=8, timeout=60)
            raw = r['text']
        elif judge_name == 'gpt4o':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-4o', prompt)
        elif judge_name == 'gpt54':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], 'gpt-5.4', prompt)
        elif judge_name == 'gemini_flash':
            raw = api_call_gemini(api_keys['GEMINI_API_KEY'], 'gemini-2.5-flash', prompt)
        elif judge_name == 'gemini_pro':
            raw = api_call_gemini(api_keys['GEMINI_API_KEY'], 'gemini-2.5-pro', prompt)
            time.sleep(5)
    except Exception as e:
        return 0, str(e), True
    score = parse_score(raw)
    return score, raw, (score == 0)


# ═══════════════════════════════════════════════════════════════
# MEMORY SYSTEM ADAPTERS — INGESTION
# ═══════════════════════════════════════════════════════════════

def namespace(subject, system):
    """Run-scoped namespace to prevent stale data contamination."""
    return f'{subject}_run_{RUN_ID}'


def ingest_mem0(subject, facts):
    """Ingest facts into Mem0 via raw HTTP. infer=False to store as-is."""
    key = os.environ['MEM0_KEY']
    user_id = namespace(subject, 'mem0')
    headers = {'Authorization': f'Token {key}', 'Content-Type': 'application/json'}

    ingestion_log = {
        'subject': subject, 'system': 'mem0', 'user_id': user_id,
        'facts_expected': len(facts), 'facts_posted': 0,
        'post_success': 0, 'post_failure': 0, 'failed_fact_indices': [],
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    # Check for checkpoint (resume from where we left off)
    cp_path = os.path.join(get_results_dir(subject), 'mem0_ingestion_checkpoint.json')
    start_idx = 0
    if os.path.exists(cp_path):
        cp = load_json(cp_path)
        start_idx = cp.get('last_successful_index', 0) + 1
        ingestion_log = cp
        log(f'  Resuming from fact {start_idx}')

    for i, fact in enumerate(facts):
        if i < start_idx:
            continue

        for attempt in range(3):
            try:
                resp = httpx.post('https://api.mem0.ai/v1/memories/',
                    json={
                        'messages': [{'role': 'user', 'content': fact}],
                        'user_id': user_id,
                        'infer': False  # Store as-is, matching Hamerton methodology
                    },
                    headers=headers, timeout=30)

                # Log first response to verify infer=False is working
                if i == start_idx:
                    log(f'  First ingestion response status: {resp.status_code}')
                    try:
                        body = resp.json()
                        # Check if Mem0 reformulated the fact
                        if 'results' in body and body['results']:
                            stored = body['results'][0].get('memory', '')
                            if stored and stored != fact:
                                log(f'  WARNING: Mem0 may have reformulated fact!')
                                log(f'    Sent:   {fact[:80]}...')
                                log(f'    Stored: {stored[:80]}...')
                            else:
                                log(f'  Verified: fact stored as-is')
                    except:
                        pass

                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        ingestion_log['failed_fact_indices'].append(i)
                        log(f'  Fact {i} failed after 3 attempts: {resp.status_code} {resp.text[:200]}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    ingestion_log['failed_fact_indices'].append(i)
                    log(f'  Fact {i} exception after 3 attempts: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['facts_posted'] = i + 1
        ingestion_log['last_successful_index'] = i

        # Checkpoint every 100 facts
        if (i + 1) % 100 == 0:
            atomic_write_json(cp_path, ingestion_log)
            log(f'  Mem0 ingested {i+1}/{len(facts)} for {subject}')

    # Clean up checkpoint
    if os.path.exists(cp_path):
        os.remove(cp_path)

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    return ingestion_log


def ingest_letta(subject, facts):
    """Ingest facts into Letta via passages endpoint."""
    key = os.environ['LETTA_KEY']
    agent_name = namespace(subject, 'letta')
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    base_url = 'https://api.letta.com/v1'

    ingestion_log = {
        'subject': subject, 'system': 'letta', 'agent_name': agent_name,
        'facts_expected': len(facts), 'facts_posted': 0,
        'post_success': 0, 'post_failure': 0, 'failed_fact_indices': [],
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    # Check for existing agent or checkpoint
    cp_path = os.path.join(get_results_dir(subject), 'letta_ingestion_checkpoint.json')
    agent_id = None
    start_idx = 0

    if os.path.exists(cp_path):
        cp = load_json(cp_path)
        agent_id = cp.get('agent_id')
        start_idx = cp.get('last_successful_index', 0) + 1
        ingestion_log = cp
        log(f'  Resuming from fact {start_idx}, agent {agent_id}')

    if not agent_id:
        # Check for existing agent with this name first
        try:
            resp = httpx.get(f'{base_url}/agents/', headers=headers, timeout=30)
            if resp.status_code == 200:
                for a in resp.json():
                    if a['name'] == agent_name:
                        agent_id = a['id']
                        ingestion_log['agent_id'] = agent_id
                        log(f'  Found existing Letta agent: {agent_id}')
                        break
        except:
            pass

        if not agent_id:
            # Create agent
            log(f'  Creating Letta agent: {agent_name}')
            resp = httpx.post(f'{base_url}/agents/',
                json={
                    'name': agent_name,
                    'model': 'openai/gpt-4o-mini',
                    'embedding': 'openai/text-embedding-3-small'
                },
                headers=headers, timeout=60)
            if resp.status_code not in (200, 201):
                log(f'  Agent creation failed: {resp.status_code} {resp.text[:300]}')
                raise RuntimeError(f'Letta agent creation failed: {resp.status_code}')
            agent_id = resp.json()['id']
            ingestion_log['agent_id'] = agent_id
            log(f'  Agent created: {agent_id}')

    # Individual fact ingestion (matches Hamerton methodology — 1 fact = 1 passage)
    # NOTE: Batch ingestion (newline-joined) tested at 135x faster BUT changes chunking
    # behavior (Letta merges adjacent facts). This produces different retrieval results.
    # Individual ingestion preserves 1:1 fact-to-passage mapping for methodological consistency.

    for i, fact in enumerate(facts):
        if i < start_idx:
            continue

        for attempt in range(3):
            try:
                resp = httpx.post(f'{base_url}/agents/{agent_id}/archival-memory',
                    json={'text': fact},
                    headers=headers,
                    timeout=httpx.Timeout(connect=10.0, read=45.0, write=10.0, pool=10.0))

                if i == start_idx:
                    log(f'  First archival-memory response: {resp.status_code}')

                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        ingestion_log['failed_fact_indices'].append(i)
                        log(f'  Fact {i} failed: {resp.status_code} {resp.text[:200]}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    ingestion_log['failed_fact_indices'].append(i)
                    log(f'  Fact {i} exception: {e}')
                else:
                    wait = 2 ** (attempt + 1)
                    log(f'  Fact {i} retry {attempt+1} after {wait}s: {e}')
                    time.sleep(wait)

        ingestion_log['facts_posted'] = i + 1
        ingestion_log['last_successful_index'] = i

        if (i + 1) % 100 == 0:
            atomic_write_json(cp_path, ingestion_log)
            log(f'  Letta ingested {i+1}/{len(facts)} for {subject}')

    if os.path.exists(cp_path):
        os.remove(cp_path)

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    return ingestion_log


def ingest_supermemory(subject, facts):
    """Ingest facts into Supermemory via /v3/documents. follow_redirects=True is critical."""
    key = os.environ['SUPERMEMORY_KEY']
    container_tag = namespace(subject, 'supermemory')
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

    ingestion_log = {
        'subject': subject, 'system': 'supermemory', 'container_tag': container_tag,
        'facts_expected': len(facts), 'facts_posted': 0,
        'post_success': 0, 'post_failure': 0, 'failed_fact_indices': [],
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    cp_path = os.path.join(get_results_dir(subject), 'supermemory_ingestion_checkpoint.json')
    start_idx = 0
    if os.path.exists(cp_path):
        cp = load_json(cp_path)
        start_idx = cp.get('last_successful_index', 0) + 1
        ingestion_log = cp
        log(f'  Resuming from fact {start_idx}')

    for i, fact in enumerate(facts):
        if i < start_idx:
            continue

        for attempt in range(3):
            try:
                resp = httpx.post('https://api.supermemory.ai/v3/documents',
                    json={
                        'content': fact,
                        'containerTags': [container_tag],
                        'customId': f'{container_tag}_fact_{i}'  # Dedup key
                    },
                    headers=headers, timeout=30,
                    follow_redirects=True)  # CRITICAL: 308 redirect issue

                if i == start_idx:
                    log(f'  First document response: {resp.status_code} {resp.text[:200]}')

                if resp.status_code in (200, 201):
                    ingestion_log['post_success'] += 1
                    break
                else:
                    if attempt == 2:
                        ingestion_log['post_failure'] += 1
                        ingestion_log['failed_fact_indices'].append(i)
                        log(f'  Fact {i} failed: {resp.status_code} {resp.text[:200]}')
            except Exception as e:
                if attempt == 2:
                    ingestion_log['post_failure'] += 1
                    ingestion_log['failed_fact_indices'].append(i)
                    log(f'  Fact {i} exception: {e}')
                else:
                    time.sleep(2 ** (attempt + 1))

        ingestion_log['facts_posted'] = i + 1
        ingestion_log['last_successful_index'] = i

        # Rate limit — conservative to avoid 429s but faster than original 0.5s
        time.sleep(0.3)

        if (i + 1) % 100 == 0:
            atomic_write_json(cp_path, ingestion_log)
            log(f'  Supermemory ingested {i+1}/{len(facts)} for {subject}')

    if os.path.exists(cp_path):
        os.remove(cp_path)

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    return ingestion_log


def ingest_zep(subject, facts):
    """Ingest facts into Zep via SDK graph.add with batching."""
    from zep_cloud.client import Zep

    key = os.environ['ZEP_KEY']
    user_id = namespace(subject, 'zep')
    client = Zep(api_key=key)

    ingestion_log = {
        'subject': subject, 'system': 'zep', 'user_id': user_id,
        'facts_expected': len(facts), 'facts_posted': 0,
        'post_success': 0, 'post_failure': 0, 'failed_fact_indices': [],
        'start_time': datetime.now(timezone.utc).isoformat()
    }

    cp_path = os.path.join(get_results_dir(subject), 'zep_ingestion_checkpoint.json')
    start_idx = 0
    if os.path.exists(cp_path):
        cp = load_json(cp_path)
        start_idx = cp.get('last_successful_index', 0) + 1
        ingestion_log = cp
        log(f'  Resuming from fact {start_idx}')

    # Create user
    try:
        client.user.add(user_id=user_id, first_name=DISPLAY_NAMES.get(subject, subject))
        log(f'  Zep user created: {user_id}')
    except Exception as e:
        if 'already exists' in str(e).lower() or '409' in str(e):
            log(f'  Zep user already exists: {user_id}')
        else:
            log(f'  Zep user creation warning: {e}')

    # Ingest in batches of 20 (500-char chunks per graph.add call)
    batch_size = 20
    for batch_start in range(start_idx, len(facts), batch_size):
        batch_end = min(batch_start + batch_size, len(facts))
        batch = facts[batch_start:batch_end]

        # Concatenate batch into single text (respect 10K char limit)
        batch_text = '\n'.join(batch)
        if len(batch_text) > 9500:
            # Split into smaller sub-batches
            for i, fact in enumerate(batch):
                idx = batch_start + i
                for attempt in range(3):
                    try:
                        client.graph.add(user_id=user_id, data=fact, type='text')
                        ingestion_log['post_success'] += 1
                        break
                    except Exception as e:
                        if attempt == 2:
                            ingestion_log['post_failure'] += 1
                            ingestion_log['failed_fact_indices'].append(idx)
                            log(f'  Fact {idx} exception: {e}')
                        else:
                            time.sleep(2 ** (attempt + 1))
        else:
            for attempt in range(3):
                try:
                    client.graph.add(user_id=user_id, data=batch_text, type='text')
                    ingestion_log['post_success'] += len(batch)
                    break
                except Exception as e:
                    if attempt == 2:
                        ingestion_log['post_failure'] += len(batch)
                        for i in range(batch_start, batch_end):
                            ingestion_log['failed_fact_indices'].append(i)
                        log(f'  Batch {batch_start}-{batch_end} exception: {e}')
                    else:
                        time.sleep(2 ** (attempt + 1))

        ingestion_log['facts_posted'] = batch_end
        ingestion_log['last_successful_index'] = batch_end - 1

        # 15s wait for graph processing
        time.sleep(15)

        atomic_write_json(cp_path, ingestion_log)
        log(f'  Zep ingested {batch_end}/{len(facts)} for {subject}')

    if os.path.exists(cp_path):
        os.remove(cp_path)

    ingestion_log['end_time'] = datetime.now(timezone.utc).isoformat()
    return ingestion_log


# ═══════════════════════════════════════════════════════════════
# MEMORY SYSTEM ADAPTERS — RETRIEVAL
# ═══════════════════════════════════════════════════════════════

def retrieve_mem0(query, subject):
    user_id = namespace(subject, 'mem0')
    resp = httpx.post('https://api.mem0.ai/v2/memories/search/',
        json={'query': query, 'filters': {'user_id': user_id}, 'top_k': 10},
        headers={'Authorization': f'Token {os.environ["MEM0_KEY"]}'},
        timeout=15)
    if resp.status_code != 200:
        return [], resp.status_code
    data = resp.json()
    if isinstance(data, list):
        facts = [r.get('memory', '') for r in data[:10]]
    else:
        results = data.get('results', data.get('memories', []))
        facts = [r.get('memory', r.get('text', '')) for r in results[:10]]
    return [f for f in facts if f], resp.status_code


def retrieve_letta(query, subject, agent_id):
    headers = {'Authorization': f'Bearer {os.environ["LETTA_KEY"]}'}
    # Use archival-memory/search endpoint (confirmed working)
    resp = httpx.get(
        f'https://api.letta.com/v1/agents/{agent_id}/archival-memory/search',
        params={'query': query, 'top_k': 10},
        headers=headers, timeout=55)
    if resp.status_code != 200:
        return [], resp.status_code
    data = resp.json()
    # Response is {"results": [{"content": "...", ...}]} or list of passages
    if isinstance(data, dict):
        results = data.get('results', [])
    else:
        results = data
    facts = [p.get('content', p.get('text', '')) for p in results[:10]]
    return [f for f in facts if f], resp.status_code


def retrieve_supermemory(query, subject):
    container_tag = namespace(subject, 'supermemory')
    resp = httpx.post('https://api.supermemory.ai/v3/search',
        json={'q': query, 'limit': 10, 'containerTags': [container_tag]},
        headers={'Authorization': f'Bearer {os.environ["SUPERMEMORY_KEY"]}',
                 'Content-Type': 'application/json'},
        timeout=15, follow_redirects=True)
    if resp.status_code != 200:
        return [], resp.status_code
    results = resp.json().get('results', [])
    out = []
    for r in results[:10]:
        chunks = r.get('chunks', [])
        if chunks:
            out.append(chunks[0].get('content', ''))
        else:
            out.append(r.get('memory', r.get('content', '')))
    return [f for f in out if f], resp.status_code


def retrieve_zep(query, subject):
    from zep_cloud.client import Zep
    client = Zep(api_key=os.environ['ZEP_KEY'])
    user_id = namespace(subject, 'zep')
    try:
        results = client.graph.search(user_id=user_id, query=query, limit=10)
        facts = []
        for r in results:
            text = getattr(r, 'fact', None) or getattr(r, 'text', None) or str(r)
            if text:
                facts.append(text)
        return facts[:10], 200
    except Exception as e:
        return [], str(e)


# ═══════════════════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════════════════

def verify_ingestion(system, subject, facts, agent_id=None):
    """Verify ingestion by searching for 10 random facts. Need 8/10 to pass."""
    random.seed(42 + hash(subject))
    sample = random.sample(facts, min(10, len(facts)))

    # Need agent_id for Letta — prefer passed arg, fallback to file
    if system == 'letta' and not agent_id:
        ing_path = os.path.join(get_results_dir(subject), f'{system}_ingestion.json')
        ing = load_json(ing_path)
        if ing:
            agent_id = ing.get('agent_id')

    hits = 0
    for fact in sample:
        # Use first 50 chars as query
        query = fact[:80]
        try:
            if system == 'mem0':
                results, _ = retrieve_mem0(query, subject)
            elif system == 'letta':
                if not agent_id:
                    log(f'  No agent_id for Letta verification')
                    return False, 0, len(sample)
                results, _ = retrieve_letta(query, subject, agent_id)
            elif system == 'supermemory':
                results, _ = retrieve_supermemory(query, subject)
            elif system == 'zep':
                results, _ = retrieve_zep(query, subject)
            else:
                results = []

            if results:
                hits += 1
        except Exception as e:
            log(f'  Verification query failed: {e}')

    passed = hits >= (len(sample) * 0.8)  # 80% threshold
    return passed, hits, len(sample)


# ═══════════════════════════════════════════════════════════════
# PHASE A: INGEST
# ═══════════════════════════════════════════════════════════════

def phase_ingest(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE A: INGEST — {system.upper()}')
    log(f'{"="*60}')

    manifest = {
        'system': system, 'run_id': RUN_ID,
        'subjects_attempted': 0, 'subjects_completed': 0,
        'subjects_failed': [], 'ingestion_verified': 0,
        'phase': 'ingest'
    }

    for subject in subjects:
        results_dir = get_results_dir(subject)
        os.makedirs(results_dir, exist_ok=True)

        ing_path = os.path.join(results_dir, f'{system}_ingestion.json')

        # Skip if already done
        if os.path.exists(ing_path):
            ing = load_json(ing_path)
            if ing and ing.get('verification_passed'):
                log(f'  {subject}: already ingested and verified, skipping')
                manifest['subjects_completed'] += 1
                manifest['ingestion_verified'] += 1
                manifest['subjects_attempted'] += 1
                continue

        manifest['subjects_attempted'] += 1
        facts = load_facts(subject)
        log(f'\n  {subject}: {len(facts)} facts')

        try:
            if system == 'mem0':
                ing_log = ingest_mem0(subject, facts)
            elif system == 'letta':
                ing_log = ingest_letta(subject, facts)
            elif system == 'supermemory':
                ing_log = ingest_supermemory(subject, facts)
            elif system == 'zep':
                ing_log = ingest_zep(subject, facts)
            else:
                raise ValueError(f'Unknown system: {system}')

            # Verification
            log(f'  Verifying {subject}...')
            # Wait for indexing (especially Supermemory and Zep)
            if system in ('supermemory', 'zep'):
                time.sleep(30)
            elif system == 'mem0':
                time.sleep(10)

            # Pass agent_id for Letta (not yet written to file)
            letta_agent_id = ing_log.get('agent_id') if system == 'letta' else None
            passed, hits, total = verify_ingestion(system, subject, facts, agent_id=letta_agent_id)
            ing_log['verification_passed'] = passed
            ing_log['verification_hits'] = hits
            ing_log['verification_total'] = total

            if passed:
                log(f'  VERIFIED: {hits}/{total} search hits')
                manifest['subjects_completed'] += 1
                manifest['ingestion_verified'] += 1
            else:
                log(f'  VERIFICATION FAILED: {hits}/{total} — retrying in 60s...')
                time.sleep(60)
                passed2, hits2, total2 = verify_ingestion(system, subject, facts, agent_id=letta_agent_id)
                ing_log['verification_passed'] = passed2
                ing_log['verification_hits'] = hits2
                if passed2:
                    log(f'  VERIFIED on retry: {hits2}/{total2}')
                    manifest['subjects_completed'] += 1
                    manifest['ingestion_verified'] += 1
                else:
                    log(f'  FAILED after retry: {hits2}/{total2}')
                    manifest['subjects_failed'].append(subject)

            atomic_write_json(ing_path, ing_log)

        except Exception as e:
            log(f'  INGEST FAILED for {subject}: {e}')
            manifest['subjects_failed'].append(subject)
            import traceback
            traceback.print_exc()

    # Save manifest
    manifest_path = os.path.join(RESULTS_BASE, f'{system}_manifest.json')
    atomic_write_json(manifest_path, manifest)
    log(f'\nIngestion complete: {manifest["subjects_completed"]}/{manifest["subjects_attempted"]} subjects')
    log(f'Failed: {manifest["subjects_failed"]}')
    return manifest


# ═══════════════════════════════════════════════════════════════
# PHASE B: RETRIEVE (cached per question)
# ═══════════════════════════════════════════════════════════════

def phase_retrieve(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE B: RETRIEVE — {system.upper()}')
    log(f'{"="*60}')

    for subject in subjects:
        results_dir = get_results_dir(subject)
        retrieval_path = os.path.join(results_dir, f'{system}_retrieval.json')

        # Check ingestion passed
        ing_path = os.path.join(results_dir, f'{system}_ingestion.json')
        ing = load_json(ing_path)
        if not ing or not ing.get('verification_passed'):
            log(f'  {subject}: ingestion not verified, skipping')
            continue

        # Load existing retrieval cache
        retrieval_cache = load_json(retrieval_path) or {}

        # Get agent_id for Letta
        agent_id = ing.get('agent_id') if system == 'letta' else None

        questions = load_battery(subject)

        log(f'\n  {subject}: {len(questions)} BP questions, {len(retrieval_cache)} already cached')

        for q in questions:
            qid = str(q['id'])
            if qid in retrieval_cache:
                continue

            q_text = q['text']
            t0 = time.time()

            try:
                if system == 'mem0':
                    facts, status = retrieve_mem0(q_text, subject)
                elif system == 'letta':
                    facts, status = retrieve_letta(q_text, subject, agent_id)
                elif system == 'supermemory':
                    facts, status = retrieve_supermemory(q_text, subject)
                elif system == 'zep':
                    facts, status = retrieve_zep(q_text, subject)

                latency_ms = round((time.time() - t0) * 1000)

                retrieval_cache[qid] = {
                    'question_id': q['id'],
                    'question_text': q_text,
                    'system': system,
                    'facts_returned': len(facts),
                    'fact_texts': facts,
                    'latency_ms': latency_ms,
                    'status': status,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }

                log(f'    Q{q["id"]}: {len(facts)} facts, {latency_ms}ms')

            except Exception as e:
                retrieval_cache[qid] = {
                    'question_id': q['id'],
                    'question_text': q_text,
                    'system': system,
                    'facts_returned': 0,
                    'fact_texts': [],
                    'latency_ms': 0,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                log(f'    Q{q["id"]}: FAILED — {e}')

            # Save after each question
            atomic_write_json(retrieval_path, retrieval_cache)

        log(f'  {subject}: {len(retrieval_cache)} questions retrieved')


# ═══════════════════════════════════════════════════════════════
# PHASE C: GENERATE (C1 + C3 from cached retrieval)
# ═══════════════════════════════════════════════════════════════

def phase_generate(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE C: GENERATE — {system.upper()}')
    log(f'{"="*60}')

    api_key = os.environ['ANTHROPIC_API_KEY']
    total_in = 0
    total_out = 0

    for subject in subjects:
        results_dir = get_results_dir(subject)

        # Load retrieval cache
        retrieval_path = os.path.join(results_dir, f'{system}_retrieval.json')
        retrieval_cache = load_json(retrieval_path)
        if not retrieval_cache:
            log(f'  {subject}: no retrieval cache, skipping')
            continue

        # Completeness gate: need all 39 BP questions retrieved
        questions_check = load_battery(subject)
        if len(retrieval_cache) < len(questions_check):
            log(f'  {subject}: retrieval incomplete ({len(retrieval_cache)}/{len(questions_check)}), skipping generate')
            continue

        # Load spec
        spec = load_spec(subject)

        # Load existing results + checkpoint
        results_path = os.path.join(results_dir, f'{system}_results.json')
        existing_results = load_json(results_path) or []
        completed_keys = set()
        for r in existing_results:
            for cond in r.get('responses', {}):
                completed_keys.add(f"{r['question_id']}_{cond}")

        questions = load_battery(subject)
        log(f'\n  {subject}: {len(questions)} questions, {len(completed_keys)} responses done')

        for q in questions:
            qid = str(q['id'])
            q_text = q['text']

            # Get cached retrieval
            cached = retrieval_cache.get(qid, {})
            retrieved_facts = cached.get('fact_texts', [])

            # Find or create result entry for this question
            q_result = None
            for r in existing_results:
                if r['question_id'] == q['id']:
                    q_result = r
                    break
            if not q_result:
                q_result = {
                    'question_id': q['id'],
                    'question_text': q_text,
                    'held_out_passage': q.get('held_out_passage'),
                    'retrieval': {
                        'facts_returned': len(retrieved_facts),
                        'facts': retrieved_facts,
                        'latency_ms': cached.get('latency_ms', 0)
                    },
                    'responses': {},
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                existing_results.append(q_result)

            # C1: retrieval only (skip if 0 facts retrieved)
            c1_key = f'C1_{system}'
            if f"{q['id']}_{c1_key}" not in completed_keys:
                if retrieved_facts:
                    ft = '\n'.join(f'- {f}' for f in retrieved_facts)
                    try:
                        t0 = time.time()
                        resp = api_call_anthropic(api_key, RESPONSE_MODEL,
                            'The following facts were retrieved about this person.\n\n'
                            '=== RETRIEVED FACTS ===\n' + ft,
                            q_text)
                        resp['latency_ms'] = round((time.time() - t0) * 1000)
                        q_result['responses'][c1_key] = resp
                        total_in += resp['input_tokens']
                        total_out += resp['output_tokens']
                        log(f'    Q{q["id"]} {c1_key}: {resp["output_tokens"]}t')
                    except Exception as e:
                        q_result['responses'][c1_key] = {'error': str(e)}
                        log(f'    Q{q["id"]} {c1_key}: FAILED {e}')
                else:
                    q_result['responses'][c1_key] = {'text': 'NO_RETRIEVAL', 'no_facts': True}
                    log(f'    Q{q["id"]} {c1_key}: no facts retrieved')

            # C3: spec + retrieval
            c3_key = f'C3_{system}'
            if f"{q['id']}_{c3_key}" not in completed_keys:
                if retrieved_facts:
                    ft = '\n'.join(f'- {f}' for f in retrieved_facts)
                    system_prompt = (
                        'The following is a behavioral specification describing your user — '
                        'how they think, decide, and act. You also have retrieved facts.\n\n'
                        '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                        '=== RETRIEVED FACTS ===\n' + ft)
                else:
                    # Spec only (no retrieval) — still tests spec utility
                    system_prompt = (
                        'The following is a behavioral specification describing your user — '
                        'how they think, decide, and act.\n\n'
                        '=== BEHAVIORAL SPECIFICATION ===\n' + spec)

                try:
                    t0 = time.time()
                    resp = api_call_anthropic(api_key, RESPONSE_MODEL, system_prompt, q_text)
                    resp['latency_ms'] = round((time.time() - t0) * 1000)
                    resp['spec_only'] = len(retrieved_facts) == 0
                    q_result['responses'][c3_key] = resp
                    total_in += resp['input_tokens']
                    total_out += resp['output_tokens']
                    log(f'    Q{q["id"]} {c3_key}: {resp["output_tokens"]}t' +
                        (' (spec-only)' if not retrieved_facts else ''))
                except Exception as e:
                    q_result['responses'][c3_key] = {'error': str(e)}
                    log(f'    Q{q["id"]} {c3_key}: FAILED {e}')

            # Save after each question
            atomic_write_json(results_path, existing_results)

        log(f'  {subject}: complete')

    cost = (total_in * 0.80 + total_out * 4.00) / 1_000_000
    log(f'\nGeneration cost: ${cost:.2f}')


# ═══════════════════════════════════════════════════════════════
# PHASE D: JUDGE
# ═══════════════════════════════════════════════════════════════

def phase_judge(system, subjects, judge_filter=None):
    log(f'{"="*60}')
    log(f'PHASE D: JUDGE — {system.upper()}')
    log(f'{"="*60}')

    api_keys = {
        'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
        'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
        'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY', ''),
    }

    judges_to_run = [judge_filter] if judge_filter else JUDGES

    for subject in subjects:
        results_dir = get_results_dir(subject)
        results_path = os.path.join(results_dir, f'{system}_results.json')
        results = load_json(results_path)
        if not results:
            log(f'  {subject}: no results, skipping')
            continue

        # Completeness gate: need 39 questions with responses
        questions_with_responses = sum(1 for r in results if r.get('responses'))
        if questions_with_responses < 39:
            log(f'  {subject}: results incomplete ({questions_with_responses}/39), skipping judge')
            continue

        for judge_name in judges_to_run:
            judgments_path = os.path.join(results_dir, f'{system}_judgments_{judge_name}.json')
            existing = load_json(judgments_path) or []
            done_keys = set(f"{j['question_id']}_{j['condition']}" for j in existing)

            conditions = [f'C1_{system}', f'C3_{system}']
            new_count = 0
            parse_failures = 0

            for q_result in results:
                qid = q_result['question_id']
                held_out = q_result.get('held_out_passage', '')
                if not held_out:
                    continue

                for cond in conditions:
                    key = f'{qid}_{cond}'
                    if key in done_keys:
                        continue

                    resp = q_result.get('responses', {}).get(cond, {})
                    resp_text = resp.get('text', '')
                    if not resp_text or resp_text == 'NO_RETRIEVAL' or 'error' in resp:
                        # Skip unjudgeable responses
                        existing.append({
                            'question_id': qid, 'condition': cond,
                            'judge': judge_name, 'score': 0,
                            'raw_response': 'skipped_no_response',
                            'parse_failure': True
                        })
                        continue

                    prompt = judge_prompt(held_out, resp_text)
                    score, raw, pf = run_judge(judge_name, prompt, api_keys)

                    existing.append({
                        'question_id': qid, 'condition': cond,
                        'judge': judge_name, 'score': score,
                        'raw_response': raw if pf else '',
                        'parse_failure': pf
                    })

                    if pf:
                        parse_failures += 1
                    new_count += 1

                    # Save after each judgment
                    atomic_write_json(judgments_path, existing)

            log(f'  {subject} / {judge_name}: {new_count} new judgments, {parse_failures} parse failures')

    # Merge all judge files per subject
    for subject in subjects:
        results_dir = get_results_dir(subject)
        merged = []
        for jn in JUDGES:
            jp = os.path.join(results_dir, f'{system}_judgments_{jn}.json')
            jdata = load_json(jp)
            if jdata:
                merged.extend(jdata)
        if merged:
            atomic_write_json(os.path.join(results_dir, f'{system}_judgments_merged.json'), merged)


# ═══════════════════════════════════════════════════════════════
# PHASE E: ANALYSIS (per system)
# ═══════════════════════════════════════════════════════════════

def phase_analyze(system, subjects):
    log(f'{"="*60}')
    log(f'PHASE E: ANALYSIS — {system.upper()}')
    log(f'{"="*60}')

    summary = {
        'system': system, 'run_id': RUN_ID,
        'subjects': {}, 'overall': {}
    }

    all_c1 = []
    all_c3 = []

    for subject in subjects:
        results_dir = get_results_dir(subject)
        merged_path = os.path.join(results_dir, f'{system}_judgments_merged.json')
        judgments = load_json(merged_path)
        if not judgments:
            continue

        c1_scores = [j['score'] for j in judgments
                     if j['condition'] == f'C1_{system}' and j['score'] > 0]
        c3_scores = [j['score'] for j in judgments
                     if j['condition'] == f'C3_{system}' and j['score'] > 0]

        c1_avg = sum(c1_scores) / len(c1_scores) if c1_scores else 0
        c3_avg = sum(c3_scores) / len(c3_scores) if c3_scores else 0
        improvement = ((c3_avg - c1_avg) / c1_avg * 100) if c1_avg > 0 else 0

        summary['subjects'][subject] = {
            'c1_avg': round(c1_avg, 2),
            'c3_avg': round(c3_avg, 2),
            'improvement_pct': round(improvement, 1),
            'c1_n': len(c1_scores),
            'c3_n': len(c3_scores),
            'display_name': DISPLAY_NAMES.get(subject, subject)
        }

        all_c1.extend(c1_scores)
        all_c3.extend(c3_scores)

        log(f'  {subject:20s}  C1={c1_avg:.2f}  C3={c3_avg:.2f}  delta={improvement:+.1f}%')

    if all_c1 and all_c3:
        summary['overall'] = {
            'c1_avg': round(sum(all_c1) / len(all_c1), 2),
            'c3_avg': round(sum(all_c3) / len(all_c3), 2),
            'c1_n': len(all_c1),
            'c3_n': len(all_c3),
        }
        log(f'\n  OVERALL: C1={summary["overall"]["c1_avg"]:.2f}  C3={summary["overall"]["c3_avg"]:.2f}')

    analysis_path = os.path.join(RESULTS_BASE, f'{system}_analysis.json')
    atomic_write_json(analysis_path, summary)
    log(f'  Saved to {analysis_path}')


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    global LOG_FILE

    parser = argparse.ArgumentParser(description='Memory Systems Expansion')
    parser.add_argument('--system', required=True, choices=['mem0', 'letta', 'supermemory', 'zep'])
    parser.add_argument('--phase', default='all', choices=['ingest', 'retrieve', 'generate', 'judge', 'analyze', 'all'])
    parser.add_argument('--subject', default=None, help='Single subject to run (default: all)')
    parser.add_argument('--judge', default=None, help='Single judge to run (for --phase judge)')
    args = parser.parse_args()

    LOG_FILE = os.path.join(BASE_DIR, f'{args.system}_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    subjects = [args.subject] if args.subject else ALL_SUBJECTS

    log(f'Memory Systems Expansion — {args.system.upper()}')
    log(f'Subjects: {subjects}')
    log(f'Phase: {args.phase}')
    log(f'Run ID: {RUN_ID}')
    log(f'Log: {LOG_FILE}')

    # Zep credit pre-check
    if args.system == 'zep' and args.phase in ('ingest', 'all'):
        try:
            from zep_cloud.client import Zep
            client = Zep(api_key=os.environ['ZEP_KEY'])
            # Try to get account info
            log('  Zep SDK initialized successfully')
        except Exception as e:
            log(f'  WARNING: Zep SDK init failed: {e}')
            log(f'  Install with: pip install zep-cloud')

    if args.phase in ('ingest', 'all'):
        phase_ingest(args.system, subjects)

    if args.phase in ('retrieve', 'all'):
        phase_retrieve(args.system, subjects)

    if args.phase in ('generate', 'all'):
        phase_generate(args.system, subjects)

    if args.phase in ('judge', 'all'):
        phase_judge(args.system, subjects, judge_filter=args.judge)

    if args.phase in ('analyze', 'all'):
        phase_analyze(args.system, subjects)

    log(f'\n{"="*60}')
    log(f'DONE — {args.system.upper()} {args.phase}')
    log(f'{"="*60}')


if __name__ == '__main__':
    main()
