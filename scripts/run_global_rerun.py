"""
Global Subjects Full Rerun — Overnight Pipeline

Reruns all 13 global subjects with identical methodology to Hamerton:
- Production specs (47 predicates → Sonnet → Opus)
- 80-question batteries (Haiku backward-design, 5 tiers, 10 categories)
- 5 conditions (C5, C2a, C2c, C4, C4a)
- 7-judge panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro)

Usage:
    python run_global_rerun.py --step harmonize     # Phase 0: Hamerton prompt harmonization
    python run_global_rerun.py --step battery        # Phase 1: Generate 80-question batteries
    python run_global_rerun.py --step responses      # Phase 2: Generate responses (5 conditions)
    python run_global_rerun.py --step judge          # Phase 3: 7-judge panel
    python run_global_rerun.py --step analyze        # Phase 4: Stats + gradient table
    python run_global_rerun.py --step all            # All phases with gate checks
    python run_global_rerun.py --step <name> --subject augustine   # Single subject
    python run_global_rerun.py --step judge --judge gpt54          # Single judge
    python run_global_rerun.py --step <name> --force               # Redo completed work
"""
import json, os, sys, time, re, hashlib, subprocess, argparse, shutil
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_BASE = os.path.join(BASE_DIR, 'results')
REPO_DIR = os.path.dirname(BASE_DIR)
HAMERTON_FS_DIR = os.path.join(RESULTS_BASE, 'run_fullstack_hamerton_20260411_231237')

SUBJECTS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers',
    'equiano', 'fukuzawa', 'keckley', 'rousseau', 'seacole',
    'sunity_devee', 'yung_wing', 'zitkala_sa'
]

DISPLAY_NAMES = {
    'augustine': 'Saint Augustine', 'babur': 'Babur',
    'bernal_diaz': 'Bernal Diaz del Castillo', 'cellini': 'Benvenuto Cellini',
    'ebers': 'Georg Ebers', 'equiano': 'Olaudah Equiano',
    'fukuzawa': 'Fukuzawa Yukichi', 'keckley': 'Elizabeth Keckley',
    'rousseau': 'Jean-Jacques Rousseau', 'seacole': 'Mary Seacole',
    'sunity_devee': 'Sunity Devee', 'yung_wing': 'Yung Wing',
    'zitkala_sa': 'Zitkala-Sa'
}

# C2c wrong-spec pairings (deterministic fixed mismatched pairing)
WRONG_SPEC_PAIRING = {
    'augustine': 'fukuzawa', 'babur': 'keckley',
    'bernal_diaz': 'sunity_devee', 'cellini': 'zitkala_sa',
    'ebers': 'equiano', 'equiano': 'ebers',
    'fukuzawa': 'augustine', 'keckley': 'babur',
    'rousseau': 'yung_wing', 'seacole': 'bernal_diaz',
    'sunity_devee': 'cellini', 'yung_wing': 'rousseau',
    'zitkala_sa': 'seacole'
}

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
BATTERY_MODEL = 'claude-haiku-4-5-20251001'  # Same as Hamerton — carbon copy

# Target battery structure (matching Hamerton exactly)
TARGET_BP = 39
TARGET_RECALL = 10
TARGET_INFERENTIAL = 11
TARGET_ADVERSARIAL = 10
TARGET_BOUNDARY = 10
TARGET_TOTAL = TARGET_BP + TARGET_RECALL + TARGET_INFERENTIAL + TARGET_ADVERSARIAL + TARGET_BOUNDARY  # 80

BP_CATEGORIES = [
    'decisions', 'values', 'relationships', 'conflict', 'learning',
    'risk', 'creativity', 'stress', 'career', 'change_over_time'
]

LOG_FILE = os.path.join(BASE_DIR, f'rerun_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

# ═══════════════════════════════════════════════════════════════
# API SETUP
# ═══════════════════════════════════════════════════════════════

def load_api_keys():
    """Load all API keys from Windows user environment."""
    keys = {}
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY']:
        r = subprocess.run(['powershell', '-Command',
            f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True)
        val = r.stdout.strip()
        if val:
            os.environ[k] = val
            keys[k] = val
    return keys


# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


# ═══════════════════════════════════════════════════════════════
# ATOMIC FILE I/O
# ═══════════════════════════════════════════════════════════════

def atomic_write_json(path, data):
    """Write JSON atomically: write to .tmp, then rename."""
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(path):
        os.replace(tmp_path, path)
    else:
        os.rename(tmp_path, path)


def load_json(path):
    """Load JSON file, return None if missing."""
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════
# API CALL HELPERS (with retry + backoff)
# ═══════════════════════════════════════════════════════════════

import httpx

def api_call_anthropic(api_key, model, system_prompt, user_message, max_tokens=1024, temperature=0, timeout=180):
    """Call Anthropic API with exponential backoff."""
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
    """Call OpenAI API with exponential backoff."""
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
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
            else:
                raise


def api_call_gemini(api_key, model, prompt, timeout=60):
    """Call Gemini API with exponential backoff."""
    for attempt in range(3):
        try:
            resp = httpx.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}',
                json={'contents': [{'parts': [{'text': prompt}]}]},
                timeout=timeout)
            if resp.status_code == 429:
                wait = 2 ** (attempt + 2)  # Longer waits for rate limit
                log(f'    Gemini 429, waiting {wait}s')
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
            else:
                raise


# ═══════════════════════════════════════════════════════════════
# JUDGE INFRASTRUCTURE
# ═══════════════════════════════════════════════════════════════

def judge_prompt(held_out, response_text):
    """Build judge prompt — identical to Hamerton, character-for-character."""
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
    """Parse judge score. Returns 1-5 or 0 (parse failure)."""
    if not text:
        return 0
    text = text.strip()
    match = re.search(r'[1-5]', text)
    if match:
        return int(match.group())
    return 0


def run_judge(judge_name, prompt, api_keys):
    """Run a single judge call. Returns (score, raw_response, parse_failure)."""
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
            time.sleep(5)  # Pro has tighter rate limits than Flash
    except Exception as e:
        return 0, str(e), True

    score = parse_score(raw)
    return score, raw, (score == 0)


ALL_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']


# ═══════════════════════════════════════════════════════════════
# DATA LOADERS
# ═══════════════════════════════════════════════════════════════

def load_spec(subject):
    """Load production spec for a subject."""
    path = f'{REPO_DIR}/data/global_subjects/{subject}/spec_production.md'
    return open(path, encoding='utf-8').read()


def load_facts(subject):
    """Load facts from results directory (same as original run)."""
    path = f'{RESULTS_BASE}/global_{subject}/facts.json'
    data = json.load(open(path, encoding='utf-8'))
    if isinstance(data, dict):
        facts = data.get('facts', [])
    else:
        facts = data
    return [f['text'] if isinstance(f, dict) else f for f in facts]


def load_hamerton_facts():
    """Load Hamerton's original facts."""
    path = os.path.join(BASE_DIR, 'shared_facts.json')
    data = json.load(open(path, encoding='utf-8'))
    return [f['text'] for f in data['facts']]


def load_hamerton_battery():
    """Load Hamerton's 80-question battery."""
    path = os.path.join(BASE_DIR, 'battery', 'questions_80.json')
    return json.load(open(path, encoding='utf-8'))


# ═══════════════════════════════════════════════════════════════
# PHASE 0: HAMERTON PROMPT HARMONIZATION
# ═══════════════════════════════════════════════════════════════

def phase_harmonize(api_keys, force=False):
    """Rerun Hamerton C5_baseline and C4_factdump with generic prompts."""
    log('=' * 60)
    log('PHASE 0: HAMERTON PROMPT HARMONIZATION')
    log('=' * 60)

    output_path = os.path.join(HAMERTON_FS_DIR, 'results_harmonized.json')
    checkpoint_path = os.path.join(HAMERTON_FS_DIR, 'harmonize_checkpoint.json')

    if os.path.exists(output_path) and not force:
        log('  results_harmonized.json already exists. Use --force to redo.')
        return True

    # Load battery and facts
    battery = load_hamerton_battery()
    bp_questions = [q for q in battery['questions']
                    if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]
    facts = load_hamerton_facts()
    ft_all = '\n'.join(f'- {f}' for f in facts)

    log(f'  BP questions: {len(bp_questions)}')
    log(f'  Facts: {len(facts)}')

    # Load checkpoint
    if os.path.exists(checkpoint_path) and not force:
        checkpoint = json.load(open(checkpoint_path, encoding='utf-8'))
    else:
        checkpoint = {'completed': {}, 'results': []}

    completed_ids = set(checkpoint['completed'].keys())

    for q_idx, q in enumerate(bp_questions):
        qid = str(q['id'])
        if qid in completed_ids:
            continue

        q_text = q['text']
        q_result = {
            'question_id': q['id'], 'question_text': q_text,
            'held_out_passage': q['held_out_passage'],
            'responses': {}
        }

        # C5_baseline — generic prompt
        try:
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], RESPONSE_MODEL,
                                   'Answer the following question.', q_text)
            q_result['responses']['C5_baseline'] = r
            log(f'  Q{q["id"]} C5: {r["output_tokens"]}t, {r["input_tokens"]} in')
        except Exception as e:
            q_result['responses']['C5_baseline'] = {'error': str(e)}
            log(f'  Q{q["id"]} C5 FAILED: {e}')

        # C4_factdump — generic prompt
        try:
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], RESPONSE_MODEL,
                'The following is a complete set of known facts about the person '
                'this question concerns.\n\n=== FACTS ===\n' + ft_all,
                q_text)
            q_result['responses']['C4_factdump'] = r
            log(f'  Q{q["id"]} C4: {r["output_tokens"]}t, {r["input_tokens"]} in')
        except Exception as e:
            q_result['responses']['C4_factdump'] = {'error': str(e)}
            log(f'  Q{q["id"]} C4 FAILED: {e}')

        checkpoint['results'].append(q_result)
        checkpoint['completed'][qid] = True
        atomic_write_json(checkpoint_path, checkpoint)

    # Write final results
    atomic_write_json(output_path, checkpoint['results'])
    log(f'  Saved {len(checkpoint["results"])} questions to results_harmonized.json')

    # Clean up checkpoint
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)

    # Gate check
    return gate_check_harmonize(output_path)


def gate_check_harmonize(output_path):
    """Verify Phase 0 output."""
    log('\n  GATE CHECK — Phase 0:')
    data = load_json(output_path)
    if not data:
        log('  FAIL: results_harmonized.json missing')
        return False

    # Check count
    if len(data) != 39:
        log(f'  FAIL: Expected 39 questions, got {len(data)}')
        return False
    log(f'  OK: {len(data)} questions')

    # Check no errors
    errors = 0
    for q in data:
        for cond, resp in q.get('responses', {}).items():
            if isinstance(resp, dict) and 'error' in resp:
                errors += 1
    if errors > 0:
        log(f'  FAIL: {errors} error responses')
        return False
    log(f'  OK: No error responses')

    # Check token sanity
    c5_tokens = [q['responses']['C5_baseline']['input_tokens'] for q in data
                 if 'input_tokens' in q['responses'].get('C5_baseline', {})]
    c4_tokens = [q['responses']['C4_factdump']['input_tokens'] for q in data
                 if 'input_tokens' in q['responses'].get('C4_factdump', {})]

    if c5_tokens and max(c5_tokens) > 100:
        log(f'  WARN: C5 max input tokens = {max(c5_tokens)} (expected < 100)')
    else:
        log(f'  OK: C5 input tokens avg={sum(c5_tokens)//len(c5_tokens) if c5_tokens else 0}')

    if c4_tokens and min(c4_tokens) < 5000:
        log(f'  WARN: C4 min input tokens = {min(c4_tokens)} (expected > 5000)')
    else:
        log(f'  OK: C4 input tokens avg={sum(c4_tokens)//len(c4_tokens) if c4_tokens else 0}')

    log('  PHASE 0 GATE: PASS')
    return True


# ═══════════════════════════════════════════════════════════════
# PHASE 0b: JUDGE HAMERTON HARMONIZED RESPONSES
# ═══════════════════════════════════════════════════════════════

def phase_harmonize_judge(api_keys, judges_to_run=None, force=False):
    """Judge Hamerton harmonized responses with 7-judge panel."""
    log('\n  JUDGING HAMERTON HARMONIZED RESPONSES')

    output_path = os.path.join(HAMERTON_FS_DIR, 'results_harmonized.json')
    judgments_path = os.path.join(HAMERTON_FS_DIR, 'judgments_harmonized.json')

    results = load_json(output_path)
    if not results:
        log('  ERROR: results_harmonized.json not found. Run --step harmonize first.')
        return False

    # Load existing judgments
    judgments = load_json(judgments_path) or []
    judged = set()
    for j in judgments:
        judged.add((j['question_id'], j['condition'], j['judge']))

    judges = judges_to_run or ALL_JUDGES
    consecutive_failures = defaultdict(int)

    for judge_name in judges:
        judge_scores = []
        for q in results:
            ho = q.get('held_out_passage', '')
            if not ho:
                continue
            for cond, resp in q.get('responses', {}).items():
                if not isinstance(resp, dict) or 'text' not in resp or 'error' in resp:
                    continue

                key = (q['question_id'], cond, judge_name)
                if key in judged and not force:
                    continue

                # FM-6: Stop after 5 consecutive failures
                if consecutive_failures[judge_name] >= 5:
                    log(f'  {judge_name} STOPPED: 5 consecutive failures')
                    break

                prompt = judge_prompt(ho, resp['text'])
                score, raw, failed = run_judge(judge_name, prompt, api_keys)

                if failed:
                    consecutive_failures[judge_name] += 1
                else:
                    consecutive_failures[judge_name] = 0

                judgments.append({
                    'question_id': q['question_id'], 'condition': cond,
                    'judge': judge_name, 'score': score,
                    'raw_response': raw[:100] if failed else '',
                    'parse_failure': failed
                })
                judged.add(key)
                judge_scores.append(score)

            if consecutive_failures[judge_name] >= 5:
                break

        valid = [s for s in judge_scores if s > 0]
        if valid:
            log(f'  {judge_name}: avg={sum(valid)/len(valid):.2f} (n={len(valid)}, failures={len(judge_scores)-len(valid)})')

        atomic_write_json(judgments_path, judgments)

    log(f'  Total judgments: {len(judgments)}')
    return True


# ═══════════════════════════════════════════════════════════════
# PHASE 1: BATTERY GENERATION
# ═══════════════════════════════════════════════════════════════

BP_PROMPT_TEMPLATE = """You are designing a behavioral prediction test for {subject_name}.

TRAINING TEXT (what the model will know):
{training_excerpt}

HELD-OUT TEXT (ground truth the model has NOT seen):
{heldout_excerpt}

Generate {count} behavioral prediction questions. For each question:
1. Find a specific decision/behavior/reaction in the HELD-OUT text
2. Write a question that can be answered from TRAINING patterns (not from memorizing the held-out text)
3. Extract the exact held-out passage as ground truth (verbatim quote, not paraphrased)

IMPORTANT: The question text must NOT contain names, dates, or specific details that only appear in the held-out text. The question should reference patterns visible in the training text.

Return a JSON array of objects with fields:
"text" (the question), "held_out_passage" (exact verbatim quote from held-out text),
"category" (one of: {categories})

Return ONLY the JSON array. No explanation."""

RECALL_PROMPT = """Generate {count} factual recall questions about {subject_name} based on this text.
Each question should have a clear factual answer found in the text.

TEXT:
{text_excerpt}

Return a JSON array of objects with fields: "text" (the question)
Return ONLY the JSON array."""

INFERENTIAL_PROMPT = """Generate {count} inferential questions about {subject_name} that require reasoning across multiple facts from this text. These questions should NOT be answerable from a single sentence — they require connecting multiple pieces of information.

TEXT:
{text_excerpt}

Return a JSON array of objects with fields: "text" (the question)
Return ONLY the JSON array."""

ADVERSARIAL_PROMPT = """Generate {count} adversarial abstention questions about {subject_name}. These are questions that CANNOT be answered from ANY available biographical data — they ask about topics the subject never discussed, events after their lifetime, or hypothetical modern scenarios.

Subject: {subject_name}

Return a JSON array of objects with fields: "text" (the question)
Return ONLY the JSON array."""

BOUNDARY_PROMPT = """Generate {count} boundary-probing questions about {subject_name} that test the edge cases of the subject's known behavioral patterns. These questions should push into areas where the subject's values or patterns might conflict or where the answer is genuinely uncertain.

TEXT (for context on their patterns):
{text_excerpt}

Return a JSON array of objects with fields: "text" (the question)
Return ONLY the JSON array."""


def parse_json_response(text):
    """Parse JSON from LLM response, handling markdown code blocks."""
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    return json.loads(text)


def compute_battery_checksum(battery):
    """Compute checksum for battery integrity verification (FM-3)."""
    content = json.dumps(battery['questions'], sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()


def generate_bp_questions(api_key, subject_name, training_text, heldout_text, target_count=39):
    """Generate behavioral prediction questions using backward design."""
    categories = ', '.join(BP_CATEGORIES)
    all_questions = []
    heldout_len = len(heldout_text)

    # 4 batches with different held-out windows
    batch_size = 10
    num_batches = 4
    for batch_idx in range(num_batches):
        # Slide window across held-out text
        window_start = (heldout_len * batch_idx) // num_batches
        window_end = min(window_start + 5000, heldout_len)
        heldout_excerpt = heldout_text[window_start:window_end]

        prompt = BP_PROMPT_TEMPLATE.format(
            subject_name=subject_name,
            training_excerpt=training_text[:3000],
            heldout_excerpt=heldout_excerpt,
            count=batch_size,
            categories=categories
        )

        try:
            r = api_call_anthropic(api_key, BATTERY_MODEL, None, prompt,
                                   max_tokens=4096, timeout=120)
            questions = parse_json_response(r['text'])
            all_questions.extend(questions)
            log(f'    Batch {batch_idx+1}/{num_batches}: {len(questions)} questions')
        except Exception as e:
            log(f'    Batch {batch_idx+1}/{num_batches} FAILED: {e}')

    # Deduplicate by question text
    seen = set()
    unique = []
    for q in all_questions:
        q_text = q.get('text', '').strip().lower()
        if q_text and q_text not in seen:
            seen.add(q_text)
            unique.append(q)

    # Trim to target count
    if len(unique) > target_count:
        unique = unique[:target_count]

    return unique


def generate_tier_questions(api_key, subject_name, text_excerpt, tier, prompt_template, count):
    """Generate questions for non-BP tiers."""
    prompt = prompt_template.format(
        subject_name=subject_name,
        text_excerpt=text_excerpt[:5000],
        count=count
    )
    try:
        r = api_call_anthropic(api_key, BATTERY_MODEL, None, prompt,
                               max_tokens=2048, timeout=60)
        questions = parse_json_response(r['text'])
        log(f'    {tier}: {len(questions)} questions')
        return questions[:count]
    except Exception as e:
        log(f'    {tier} FAILED: {e}')
        return []


def phase_battery(api_keys, subjects_to_run, force=False):
    """Generate 80-question batteries for all subjects."""
    log('\n' + '=' * 60)
    log('PHASE 1: BATTERY GENERATION')
    log('=' * 60)

    api_key = api_keys['ANTHROPIC_API_KEY']

    for subj in subjects_to_run:
        display = DISPLAY_NAMES.get(subj, subj)
        output_path = f'{RESULTS_BASE}/global_{subj}/battery_v2.json'

        if os.path.exists(output_path) and not force:
            # Verify existing battery
            existing = load_json(output_path)
            if existing and len(existing.get('questions', [])) == TARGET_TOTAL:
                log(f'  {subj}: battery_v2.json exists with {TARGET_TOTAL} questions. Skipping.')
                continue
            else:
                log(f'  {subj}: battery_v2.json exists but incomplete. Regenerating.')

        # FM-3: If regenerating, wipe downstream data
        if force or os.path.exists(output_path):
            for downstream in ['results_v2.json', 'judgments_v2.json', 'responses_checkpoint.json']:
                dp = f'{RESULTS_BASE}/global_{subj}/{downstream}'
                if os.path.exists(dp):
                    os.remove(dp)
                    log(f'  {subj}: Wiped {downstream} (FM-3: battery changed)')

        log(f'\n  {display} ({subj}):')

        # Load texts
        training_path = f'{RESULTS_BASE}/global_{subj}/training.txt'
        heldout_path = f'{RESULTS_BASE}/global_{subj}/heldout.txt'

        if not os.path.exists(training_path) or not os.path.exists(heldout_path):
            log(f'  {subj}: MISSING training.txt or heldout.txt — skipping')
            continue

        training = open(training_path, encoding='utf-8').read()
        heldout = open(heldout_path, encoding='utf-8').read()
        log(f'    Training: {len(training.split())} words, Held-out: {len(heldout.split())} words')

        # Generate BP questions
        log(f'    Generating {TARGET_BP} behavioral prediction questions...')
        bp_questions = generate_bp_questions(api_key, display, training, heldout, TARGET_BP)

        # Generate other tiers
        log(f'    Generating supplementary tiers...')
        recall_qs = generate_tier_questions(api_key, display, training, 'recall',
                                            RECALL_PROMPT, TARGET_RECALL)
        inferential_qs = generate_tier_questions(api_key, display, training, 'inferential',
                                                 INFERENTIAL_PROMPT, TARGET_INFERENTIAL)
        adversarial_qs = generate_tier_questions(api_key, display, training, 'adversarial_abstention',
                                                 ADVERSARIAL_PROMPT, TARGET_ADVERSARIAL)
        boundary_qs = generate_tier_questions(api_key, display, training, 'boundary_probing',
                                             BOUNDARY_PROMPT, TARGET_BOUNDARY)

        # Assemble battery
        battery = {
            'metadata': {
                'subject': display,
                'subject_key': subj,
                'generated': datetime.now(timezone.utc).isoformat(),
                'model': BATTERY_MODEL,
                'method': 'backward_design_from_heldout',
                'total': 0,
                'tiers': {}
            },
            'questions': []
        }

        qid = 1
        # BP tier
        for q in bp_questions:
            battery['questions'].append({
                'id': qid, 'tier': 'behavioral_prediction',
                'category': q.get('category', 'decisions'),
                'text': q['text'],
                'held_out_passage': q.get('held_out_passage', ''),
            })
            qid += 1
        # Recall tier
        for q in recall_qs:
            battery['questions'].append({
                'id': qid, 'tier': 'recall',
                'category': 'recall',
                'text': q['text'],
                'held_out_passage': None,
            })
            qid += 1
        # Inferential tier
        for q in inferential_qs:
            battery['questions'].append({
                'id': qid, 'tier': 'inferential',
                'category': 'inferential',
                'text': q['text'],
                'held_out_passage': None,
            })
            qid += 1
        # Adversarial tier
        for q in adversarial_qs:
            battery['questions'].append({
                'id': qid, 'tier': 'adversarial_abstention',
                'category': 'adversarial',
                'text': q['text'],
                'held_out_passage': None,
            })
            qid += 1
        # Boundary tier
        for q in boundary_qs:
            battery['questions'].append({
                'id': qid, 'tier': 'boundary_probing',
                'category': 'boundary',
                'text': q['text'],
                'held_out_passage': None,
            })
            qid += 1

        battery['metadata']['total'] = len(battery['questions'])
        battery['metadata']['tiers'] = {
            'behavioral_prediction': len(bp_questions),
            'recall': len(recall_qs),
            'inferential': len(inferential_qs),
            'adversarial_abstention': len(adversarial_qs),
            'boundary_probing': len(boundary_qs),
        }
        battery['metadata']['checksum'] = compute_battery_checksum(battery)

        atomic_write_json(output_path, battery)
        log(f'    SAVED: {len(battery["questions"])} questions (BP={len(bp_questions)}, '
            f'recall={len(recall_qs)}, inf={len(inferential_qs)}, '
            f'adv={len(adversarial_qs)}, bound={len(boundary_qs)})')

    return gate_check_battery(subjects_to_run)


def gate_check_battery(subjects_to_run):
    """Verify Phase 1 output."""
    log('\n  GATE CHECK — Phase 1:')
    all_pass = True

    for subj in subjects_to_run:
        path = f'{RESULTS_BASE}/global_{subj}/battery_v2.json'
        data = load_json(path)

        if not data:
            log(f'  FAIL: {subj} — battery_v2.json missing')
            all_pass = False
            continue

        total = len(data.get('questions', []))
        tiers = defaultdict(int)
        bp_with_ho = 0
        empty_ho = 0

        for q in data.get('questions', []):
            tiers[q['tier']] += 1
            if q['tier'] == 'behavioral_prediction':
                if q.get('held_out_passage'):
                    bp_with_ho += 1
                else:
                    empty_ho += 1

        # Check counts
        if total != TARGET_TOTAL:
            log(f'  WARN: {subj} — {total} questions (target {TARGET_TOTAL})')
            if total < TARGET_TOTAL - 5:
                all_pass = False

        if bp_with_ho < TARGET_BP - 5:
            log(f'  FAIL: {subj} — only {bp_with_ho} BP questions with held_out_passage')
            all_pass = False

        if empty_ho > 0:
            log(f'  WARN: {subj} — {empty_ho} BP questions with empty held_out_passage')

        log(f'  {subj}: {total} questions (BP={tiers["behavioral_prediction"]}[{bp_with_ho} w/passage], '
            f'recall={tiers["recall"]}, inf={tiers["inferential"]}, '
            f'adv={tiers["adversarial_abstention"]}, bound={tiers["boundary_probing"]})')

    if all_pass:
        log('  PHASE 1 GATE: PASS')
    else:
        log('  PHASE 1 GATE: FAIL — review warnings above')
    return all_pass


# ═══════════════════════════════════════════════════════════════
# PHASE 2: RESPONSE GENERATION
# ═══════════════════════════════════════════════════════════════

CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec', 'C4_factdump', 'C4a_full_facts_plus_spec']


def build_system_prompt(condition, spec, wrong_spec, facts_bullets):
    """Build system prompt for each condition — identical to Hamerton format."""
    if condition == 'C5_baseline':
        return 'Answer the following question.'
    elif condition == 'C2a_full_spec':
        return ('The following is a behavioral specification describing your user \u2014 '
                'how they think, decide, and act.\n\n'
                '=== BEHAVIORAL SPECIFICATION ===\n' + spec)
    elif condition == 'C2c_wrong_spec':
        return ('The following is a behavioral specification describing your user \u2014 '
                'how they think, decide, and act.\n\n'
                '=== BEHAVIORAL SPECIFICATION ===\n' + wrong_spec)
    elif condition == 'C4_factdump':
        return ('The following is a complete set of known facts about the person '
                'this question concerns.\n\n=== FACTS ===\n' + facts_bullets)
    elif condition == 'C4a_full_facts_plus_spec':
        return ('The following is a behavioral specification describing your user \u2014 '
                'how they think, decide, and act. You also have the complete set of '
                'known facts about this person.\n\n'
                '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                '=== ALL KNOWN FACTS ===\n' + facts_bullets)
    else:
        raise ValueError(f'Unknown condition: {condition}')


def preflight_token_audit(subjects_to_run):
    """FM-7: Check prompt sizes before spending money."""
    log('\n  PRE-FLIGHT TOKEN AUDIT:')
    warnings = []
    for subj in subjects_to_run:
        spec = load_spec(subj)
        facts = load_facts(subj)
        ft_all = '\n'.join(f'- {f}' for f in facts)

        # Estimate tokens (~4 chars per token)
        c2a_est = len(spec) // 4
        c4_est = len(ft_all) // 4
        c4a_est = (len(spec) + len(ft_all)) // 4

        log(f'  {subj}: C2a~{c2a_est//1000}K, C4~{c4_est//1000}K, C4a~{c4a_est//1000}K tokens, facts={len(facts)}')

        if c4a_est > 150000:
            warnings.append(f'{subj}: C4a estimated {c4a_est//1000}K tokens — may need fact capping')

    if warnings:
        log('  WARNINGS:')
        for w in warnings:
            log(f'    {w}')
    else:
        log('  All subjects within token limits.')
    return warnings


def phase_responses(api_keys, subjects_to_run, force=False):
    """Generate responses for 5 conditions across all subjects."""
    log('\n' + '=' * 60)
    log('PHASE 2: RESPONSE GENERATION')
    log('=' * 60)

    api_key = api_keys['ANTHROPIC_API_KEY']

    # Pre-flight audit
    warnings = preflight_token_audit(subjects_to_run)

    total_in = total_out = total_errors = 0

    for subj in subjects_to_run:
        display = DISPLAY_NAMES.get(subj, subj)
        battery_path = f'{RESULTS_BASE}/global_{subj}/battery_v2.json'
        results_path = f'{RESULTS_BASE}/global_{subj}/results_v2.json'
        checkpoint_path = f'{RESULTS_BASE}/global_{subj}/responses_checkpoint.json'

        # FM-2: Verify battery exists and passes gate
        battery = load_json(battery_path)
        if not battery or len(battery.get('questions', [])) != TARGET_TOTAL:
            log(f'  {subj}: SKIP — battery_v2.json missing or incomplete')
            continue

        # FM-3: Verify battery checksum if results exist
        if os.path.exists(results_path) and not force:
            existing = load_json(results_path)
            bp_count = sum(1 for q in battery['questions']
                          if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage'))
            expected = bp_count * len(CONDITIONS)
            actual = sum(len(q.get('responses', {})) for q in (existing or []))
            if actual >= expected:
                log(f'  {subj}: results_v2.json complete ({actual} responses). Skipping.')
                continue

        # Load data
        spec = load_spec(subj)
        wrong_subj = WRONG_SPEC_PAIRING[subj]
        wrong_spec = load_spec(wrong_subj)
        facts = load_facts(subj)
        ft_all = '\n'.join(f'- {f}' for f in facts)

        # FM-7: Cap facts if needed
        max_fact_chars = 600000  # ~150K tokens
        if len(ft_all) > max_fact_chars:
            original_count = len(facts)
            while len(ft_all) > max_fact_chars and facts:
                facts = facts[:-100]
                ft_all = '\n'.join(f'- {f}' for f in facts)
            log(f'  {subj}: Capped facts from {original_count} to {len(facts)} (FM-7)')

        bp_questions = [q for q in battery['questions']
                       if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]

        log(f'\n  {display} ({subj}): {len(bp_questions)} BP questions, '
            f'{len(facts)} facts, spec {len(spec.split())}w, wrong_spec={wrong_subj}')

        # Load checkpoint
        if os.path.exists(checkpoint_path) and not force:
            checkpoint = load_json(checkpoint_path)
        else:
            checkpoint = {'completed': {}, 'results': {}}

        for q in bp_questions:
            qid = str(q['id'])
            if qid not in checkpoint['results']:
                checkpoint['results'][qid] = {
                    'question_id': q['id'], 'question_text': q['text'],
                    'held_out_passage': q['held_out_passage'],
                    'responses': {}
                }

            for cond in CONDITIONS:
                key = f'{qid}_{cond}'
                if key in checkpoint['completed'] and not force:
                    continue

                sys_prompt = build_system_prompt(cond, spec, wrong_spec, ft_all)

                try:
                    r = api_call_anthropic(api_key, RESPONSE_MODEL, sys_prompt, q['text'])
                    checkpoint['results'][qid]['responses'][cond] = r
                    total_in += r['input_tokens']
                    total_out += r['output_tokens']
                except Exception as e:
                    checkpoint['results'][qid]['responses'][cond] = {'error': str(e)}
                    total_errors += 1
                    log(f'    Q{q["id"]} {cond} ERROR: {e}')

                checkpoint['completed'][key] = True

            # Checkpoint after each question (all conditions)
            if int(qid) % 10 == 0:
                atomic_write_json(checkpoint_path, checkpoint)
                cost = (total_in * 0.80 + total_out * 4.00) / 1_000_000
                log(f'    {subj} Q{qid}: {len(checkpoint["completed"])} done, ${cost:.2f}')

        # Save final results
        results_list = [checkpoint['results'][str(q['id'])] for q in bp_questions
                       if str(q['id']) in checkpoint['results']]
        atomic_write_json(results_path, results_list)
        atomic_write_json(checkpoint_path, checkpoint)

        subj_responses = sum(len(r.get('responses', {})) for r in results_list)
        log(f'  {subj} DONE: {subj_responses} responses, {total_errors} errors')

    cost = (total_in * 0.80 + total_out * 4.00) / 1_000_000
    log(f'\nRESPONSE GENERATION COMPLETE — ${cost:.2f}, {total_errors} errors')

    return gate_check_responses(subjects_to_run)


def gate_check_responses(subjects_to_run):
    """Verify Phase 2 output."""
    log('\n  GATE CHECK — Phase 2:')
    all_pass = True

    for subj in subjects_to_run:
        results_path = f'{RESULTS_BASE}/global_{subj}/results_v2.json'
        battery_path = f'{RESULTS_BASE}/global_{subj}/battery_v2.json'

        results = load_json(results_path)
        battery = load_json(battery_path)

        if not results:
            log(f'  FAIL: {subj} — results_v2.json missing')
            all_pass = False
            continue

        bp_count = sum(1 for q in battery['questions']
                      if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage'))
        expected_responses = bp_count * len(CONDITIONS)

        actual = 0
        errors = 0
        token_sums = defaultdict(list)
        for q in results:
            for cond, resp in q.get('responses', {}).items():
                if isinstance(resp, dict) and 'error' in resp:
                    errors += 1
                elif isinstance(resp, dict) and 'input_tokens' in resp:
                    actual += 1
                    token_sums[cond].append(resp['input_tokens'])

        error_rate = errors / max(expected_responses, 1)

        # Token sanity
        token_report = []
        for cond in CONDITIONS:
            toks = token_sums.get(cond, [])
            if toks:
                avg = sum(toks) // len(toks)
                token_report.append(f'{cond}={avg}')

        log(f'  {subj}: {actual}/{expected_responses} responses, {errors} errors ({error_rate:.1%}), '
            f'tokens: {", ".join(token_report)}')

        if error_rate > 0.05:
            log(f'  FAIL: {subj} — error rate {error_rate:.1%} > 5%')
            all_pass = False

    if all_pass:
        log('  PHASE 2 GATE: PASS')
    else:
        log('  PHASE 2 GATE: FAIL')
    return all_pass


# ═══════════════════════════════════════════════════════════════
# PHASE 4: ANALYSIS
# ═══════════════════════════════════════════════════════════════

def phase_analyze():
    """Compute gradient table, Wilcoxon, Krippendorff's alpha."""
    log('\n' + '=' * 60)
    log('PHASE 4: ANALYSIS')
    log('=' * 60)

    analysis_dir = os.path.join(RESULTS_BASE, 'global_rerun_analysis')
    os.makedirs(analysis_dir, exist_ok=True)

    # Aggregation rule (locked): mean per judge across questions, then mean across judges
    # Unit of inference: subject (N=14)

    all_subject_scores = {}  # subject -> {condition -> score}

    # ── Global subjects ──
    for subj in SUBJECTS:
        judgments_path = f'{RESULTS_BASE}/global_{subj}/judgments_v2.json'
        judgments = load_json(judgments_path)
        if not judgments:
            log(f'  {subj}: SKIP — no judgments')
            continue

        # Step 1: Mean per judge per condition (excluding score=0)
        judge_cond_scores = defaultdict(lambda: defaultdict(list))
        for j in judgments:
            if j['score'] > 0 and not j.get('parse_failure'):
                judge_cond_scores[j['judge']][j['condition']].append(j['score'])

        # Step 2: Mean across judges per condition
        cond_means = {}
        for cond in CONDITIONS:
            judge_means = []
            for judge_name in ALL_JUDGES:
                scores = judge_cond_scores.get(judge_name, {}).get(cond, [])
                if scores:
                    judge_means.append(sum(scores) / len(scores))
            if judge_means:
                cond_means[cond] = sum(judge_means) / len(judge_means)

        all_subject_scores[subj] = cond_means

    # ── Hamerton harmonized ──
    hamerton_judgments_path = os.path.join(HAMERTON_FS_DIR, 'judgments_harmonized.json')
    hamerton_judgments = load_json(hamerton_judgments_path)

    # Also load Hamerton full-stack judgments for spec conditions
    hamerton_fs_analysis = os.path.join(HAMERTON_FS_DIR, 'analysis')
    hamerton_spec_judgments = []
    for jfile in ['judgments.json', 'gpt54_judgments.json', 'gemini_pro_judgments.json']:
        jpath = os.path.join(hamerton_fs_analysis, jfile)
        if os.path.exists(jpath):
            hamerton_spec_judgments.extend(load_json(jpath) or [])

    if hamerton_judgments:
        # Harmonized C5 and C4
        h_judge_cond = defaultdict(lambda: defaultdict(list))
        for j in hamerton_judgments:
            if j['score'] > 0 and not j.get('parse_failure'):
                h_judge_cond[j['judge']][j['condition']].append(j['score'])

        hamerton_cond_means = {}
        for cond in ['C5_baseline', 'C4_factdump']:
            judge_means = []
            for judge_name in ALL_JUDGES:
                scores = h_judge_cond.get(judge_name, {}).get(cond, [])
                if scores:
                    judge_means.append(sum(scores) / len(scores))
            if judge_means:
                hamerton_cond_means[cond] = sum(judge_means) / len(judge_means)

        # Full-stack spec conditions from existing Hamerton data
        # Map judge names from existing files
        h_spec_judge_cond = defaultdict(lambda: defaultdict(list))
        for j in hamerton_spec_judgments:
            score = j.get('score') or j.get('haiku_score') or j.get('gpt54_score', 0)
            judge = j.get('judge', 'haiku')
            if 'gpt54_score' in j:
                judge = 'gpt54'
                score = j['gpt54_score']
            elif 'gemini_pro_score' in j:
                judge = 'gemini_pro'
                score = j['gemini_pro_score']
            if score > 0:
                h_spec_judge_cond[judge][j['condition']].append(score)

        for cond in ['C2a_full_spec', 'C2c_full_wrong_spec', 'C4a_full_all_facts_plus_spec']:
            judge_means = []
            for judge_name in ALL_JUDGES:
                # Map condition names
                lookup_cond = cond
                scores = h_spec_judge_cond.get(judge_name, {}).get(lookup_cond, [])
                if scores:
                    judge_means.append(sum(scores) / len(scores))
            if judge_means:
                hamerton_cond_means[lookup_cond] = sum(judge_means) / len(judge_means)

        all_subject_scores['hamerton'] = hamerton_cond_means

    # ── Print gradient table ──
    log('\n  GRADIENT TABLE (Table 4.4):')
    log(f'  {"Subject":<20} {"Baseline":>8} {"Spec":>8} {"Wrong":>8} {"Facts":>8} {"F+Spec":>8} {"Effect":>8}')
    log(f'  {"-"*20} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8}')

    gradient_data = []
    for subj in ['hamerton'] + SUBJECTS:
        scores = all_subject_scores.get(subj, {})
        baseline = scores.get('C5_baseline', 0)
        spec = scores.get('C2a_full_spec', 0)
        wrong = scores.get('C2c_wrong_spec', scores.get('C2c_full_wrong_spec', 0))
        facts = scores.get('C4_factdump', 0)
        f_spec = scores.get('C4a_full_facts_plus_spec', scores.get('C4a_full_all_facts_plus_spec', 0))

        effect = ((spec - baseline) / baseline * 100) if baseline > 0 else 0
        effect_str = f'{effect:+.0f}%'

        display = DISPLAY_NAMES.get(subj, subj.title())
        log(f'  {display:<20} {baseline:>8.2f} {spec:>8.2f} {wrong:>8.2f} {facts:>8.2f} {f_spec:>8.2f} {effect_str:>8}')

        gradient_data.append({
            'subject': subj, 'display': display,
            'C5_baseline': round(baseline, 3),
            'C2a_full_spec': round(spec, 3),
            'C2c_wrong_spec': round(wrong, 3),
            'C4_factdump': round(facts, 3),
            'C4a_full_facts_plus_spec': round(f_spec, 3),
            'effect_pct': round(effect, 1)
        })

    # ── Wilcoxon signed-rank test ──
    log('\n  WILCOXON SIGNED-RANK TEST:')
    baselines = []
    specs = []
    for d in gradient_data:
        if d['C5_baseline'] > 0 and d['C2a_full_spec'] > 0:
            baselines.append(d['C5_baseline'])
            specs.append(d['C2a_full_spec'])

    wilcoxon_result = None
    try:
        from scipy.stats import wilcoxon
        stat, p_value = wilcoxon(specs, baselines, alternative='greater')
        log(f'  N={len(baselines)}, statistic={stat:.2f}, p={p_value:.4f}')
        log(f'  {"SIGNIFICANT" if p_value < 0.05 else "NOT significant"} at alpha=0.05')
        wilcoxon_result = {'n': len(baselines), 'statistic': round(float(stat), 3),
                          'p_value': round(float(p_value), 4)}
    except ImportError:
        log('  scipy not available — install with: pip install scipy')
    except Exception as e:
        log(f'  Error: {e}')

    # ── Krippendorff's alpha ──
    log('\n  KRIPPENDORFF\'S ALPHA:')
    try:
        # Build reliability matrix: judges × items
        # Collect all (question_id, condition) pairs across subjects
        import numpy as np

        all_judgments = []
        for subj in SUBJECTS:
            judgments = load_json(f'{RESULTS_BASE}/global_{subj}/judgments_v2.json') or []
            for j in judgments:
                j['subject'] = subj
            all_judgments.extend(judgments)

        if all_judgments:
            # Build item keys
            items = sorted(set((j['subject'], j['question_id'], j['condition']) for j in all_judgments))
            item_idx = {k: i for i, k in enumerate(items)}

            # Build matrix
            matrix = np.full((len(ALL_JUDGES), len(items)), np.nan)
            for j in all_judgments:
                if j['score'] > 0:
                    judge_idx = ALL_JUDGES.index(j['judge']) if j['judge'] in ALL_JUDGES else -1
                    if judge_idx >= 0:
                        item_key = (j['subject'], j['question_id'], j['condition'])
                        if item_key in item_idx:
                            matrix[judge_idx, item_idx[item_key]] = j['score']

            # Simple Krippendorff's alpha (ordinal)
            # Using bootstrap approximation
            valid_cols = ~np.all(np.isnan(matrix), axis=0)
            matrix = matrix[:, valid_cols]

            # Compute observed disagreement
            n_items = matrix.shape[1]
            Do = 0  # observed disagreement
            De = 0  # expected disagreement
            n_pairs = 0

            for col in range(n_items):
                vals = matrix[:, col]
                vals = vals[~np.isnan(vals)]
                m = len(vals)
                if m < 2:
                    continue
                for i in range(m):
                    for j in range(i + 1, m):
                        Do += (vals[i] - vals[j]) ** 2
                        n_pairs += 1

            # Expected disagreement from marginal distribution
            all_vals = matrix[~np.isnan(matrix)]
            n_total = len(all_vals)
            for i in range(n_total):
                for j in range(i + 1, min(i + 1000, n_total)):  # sample for speed
                    De += (all_vals[i] - all_vals[j]) ** 2

            De_pairs = min(n_total * (n_total - 1) // 2, n_total * 500)

            if De_pairs > 0 and n_pairs > 0:
                Do_avg = Do / n_pairs
                De_avg = De / De_pairs
                alpha = 1 - (Do_avg / De_avg) if De_avg > 0 else 0
                log(f'  Alpha = {alpha:.3f} (items={n_items}, judges={len(ALL_JUDGES)})')
                log(f'  Interpretation: {"Good" if alpha > 0.67 else "Moderate" if alpha > 0.33 else "Low"} agreement')
            else:
                alpha = None
                log('  Insufficient data for alpha calculation')
        else:
            alpha = None
            log('  No judgment data available')
    except ImportError:
        alpha = None
        log('  numpy not available')
    except Exception as e:
        alpha = None
        log(f'  Error: {e}')

    # ── Save summary ──
    summary = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'subjects': len(gradient_data),
        'gradient': gradient_data,
        'wilcoxon': wilcoxon_result,
        'krippendorff_alpha': round(float(alpha), 3) if alpha is not None else None,
        'aggregation_rule': 'mean_per_judge_then_mean_across_judges',
        'unit_of_inference': 'subject',
        'conditions': CONDITIONS,
        'judges': ALL_JUDGES
    }
    atomic_write_json(os.path.join(analysis_dir, 'summary.json'), summary)
    log(f'\n  Summary saved to {analysis_dir}/summary.json')

    log('\n  PHASE 4: COMPLETE')


# ═══════════════════════════════════════════════════════════════
# PHASE 3: JUDGING (7-JUDGE PANEL)
# ═══════════════════════════════════════════════════════════════

def phase_judge(api_keys, subjects_to_run, judges_to_run=None, force=False):
    """Judge all responses with 7-judge panel."""
    log('\n' + '=' * 60)
    log('PHASE 3: JUDGING (7-JUDGE PANEL)')
    log('=' * 60)

    judges = judges_to_run or ALL_JUDGES
    log(f'  Judges: {judges}')

    for subj in subjects_to_run:
        display = DISPLAY_NAMES.get(subj, subj)
        results_path = f'{RESULTS_BASE}/global_{subj}/results_v2.json'
        judgments_path = f'{RESULTS_BASE}/global_{subj}/judgments_v2.json'

        results = load_json(results_path)
        if not results:
            log(f'  {subj}: SKIP — results_v2.json missing. Run --step responses first.')
            continue

        log(f'\n  {display} ({subj}):')

        # Load existing judgments (FM-1: track at tuple level)
        judgments = load_json(judgments_path) or []
        judged = set()
        for j in judgments:
            judged.add((j['question_id'], j['condition'], j['judge']))

        # Build items to judge (BP with held_out_passage only, response truncated to 1500 chars)
        items = []
        for q in results:
            ho = q.get('held_out_passage', '')
            if not ho:
                continue
            for cond, resp in q.get('responses', {}).items():
                if isinstance(resp, dict) and 'text' in resp and 'error' not in resp:
                    items.append((q['question_id'], cond, ho, resp['text']))

        log(f'    {len(items)} items × {len(judges)} judges = {len(items) * len(judges)} judgments needed')

        consecutive_failures = defaultdict(int)

        for judge_name in judges:
            judge_count = 0
            judge_scores = []
            judge_failures = 0

            for qid, cond, ho, txt in items:
                key = (qid, cond, judge_name)

                # FM-1: Never duplicate
                if key in judged and not force:
                    continue

                # FM-6: Stop after 5 consecutive failures
                if consecutive_failures[judge_name] >= 5:
                    log(f'    {judge_name} STOPPED at Q{qid} {cond}: 5 consecutive failures')
                    break

                prompt = judge_prompt(ho, txt)
                score, raw, failed = run_judge(judge_name, prompt, api_keys)

                if failed:
                    consecutive_failures[judge_name] += 1
                    judge_failures += 1
                else:
                    consecutive_failures[judge_name] = 0

                judgment = {
                    'question_id': qid, 'condition': cond,
                    'judge': judge_name, 'score': score,
                    'parse_failure': failed
                }
                if failed:
                    judgment['raw_response'] = raw[:200]

                judgments.append(judgment)
                judged.add(key)
                judge_scores.append(score)
                judge_count += 1

                # Checkpoint every 50 judgments per judge
                if judge_count % 50 == 0:
                    atomic_write_json(judgments_path, judgments)

            # Reset consecutive failures for next subject
            consecutive_failures[judge_name] = 0

            valid = [s for s in judge_scores if s > 0]
            if valid:
                log(f'    {judge_name}: avg={sum(valid)/len(valid):.2f} '
                    f'(n={len(valid)}, new={judge_count}, failures={judge_failures})')
            elif judge_count > 0:
                log(f'    {judge_name}: {judge_count} scored, ALL parse failures')

            atomic_write_json(judgments_path, judgments)

        log(f'  {subj}: {len(judgments)} total judgments')

    return gate_check_judge(subjects_to_run)


def gate_check_judge(subjects_to_run):
    """Verify Phase 3 output."""
    log('\n  GATE CHECK — Phase 3:')
    all_pass = True

    for subj in subjects_to_run:
        judgments_path = f'{RESULTS_BASE}/global_{subj}/judgments_v2.json'
        battery_path = f'{RESULTS_BASE}/global_{subj}/battery_v2.json'

        judgments = load_json(judgments_path)
        battery = load_json(battery_path)

        if not judgments:
            log(f'  FAIL: {subj} — judgments_v2.json missing')
            all_pass = False
            continue

        bp_count = sum(1 for q in battery['questions']
                      if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage'))
        expected = bp_count * len(CONDITIONS) * len(ALL_JUDGES)

        # Check for duplicates (FM-1)
        seen = set()
        duplicates = 0
        for j in judgments:
            key = (j['question_id'], j['condition'], j['judge'])
            if key in seen:
                duplicates += 1
            seen.add(key)

        if duplicates > 0:
            log(f'  FAIL: {subj} — {duplicates} duplicate judgments (FM-1 violation)')
            all_pass = False

        # Check per-judge completeness and parse failures
        judge_stats = defaultdict(lambda: {'total': 0, 'valid': 0, 'failures': 0, 'scores': []})
        for j in judgments:
            jn = j['judge']
            judge_stats[jn]['total'] += 1
            if j.get('parse_failure'):
                judge_stats[jn]['failures'] += 1
            if j['score'] > 0:
                judge_stats[jn]['valid'] += 1
                judge_stats[jn]['scores'].append(j['score'])

        judge_summary = []
        for jn in ALL_JUDGES:
            s = judge_stats.get(jn, {'total': 0, 'valid': 0, 'failures': 0, 'scores': []})
            avg = sum(s['scores']) / len(s['scores']) if s['scores'] else 0
            fail_rate = s['failures'] / max(s['total'], 1)
            judge_summary.append(f'{jn}={avg:.2f}({s["valid"]})')

            if fail_rate > 0.10 and s['total'] > 0:
                log(f'  WARN: {subj} {jn} parse failure rate {fail_rate:.0%}')

        log(f'  {subj}: {len(judgments)}/{expected} judgments, '
            f'dupes={duplicates}, judges: {", ".join(judge_summary)}')

    if all_pass:
        log('  PHASE 3 GATE: PASS')
    else:
        log('  PHASE 3 GATE: FAIL')
    return all_pass


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Global Subjects Full Rerun')
    parser.add_argument('--step', required=True,
                        choices=['harmonize', 'battery', 'responses', 'judge', 'analyze', 'all'])
    parser.add_argument('--subject', default='all')
    parser.add_argument('--judge', default=None, help='Run specific judge only')
    parser.add_argument('--force', action='store_true', help='Redo completed work')
    args = parser.parse_args()

    log(f'=== Global Subjects Full Rerun ===')
    log(f'Step: {args.step}, Subject: {args.subject}, Force: {args.force}')
    log(f'Started: {datetime.now(timezone.utc).isoformat()}')
    log(f'Log: {LOG_FILE}')

    api_keys = load_api_keys()
    log(f'API keys loaded: {", ".join(k for k, v in api_keys.items() if v)}')

    if args.step in ('harmonize', 'all'):
        success = phase_harmonize(api_keys, force=args.force)
        if not success:
            log('PHASE 0 FAILED — stopping.')
            sys.exit(1)
        # Judge harmonized responses
        judges = [args.judge] if args.judge else None
        phase_harmonize_judge(api_keys, judges_to_run=judges, force=args.force)

    if args.step in ('battery', 'all'):
        subjects = SUBJECTS if args.subject == 'all' else [s.strip() for s in args.subject.split(',')]
        success = phase_battery(api_keys, subjects, force=args.force)
        if not success:
            log('PHASE 1 FAILED — stopping. Review warnings, fix batteries, rerun.')
            if args.step == 'all':
                sys.exit(1)

    if args.step in ('responses', 'all'):
        subjects = SUBJECTS if args.subject == 'all' else [s.strip() for s in args.subject.split(',')]
        success = phase_responses(api_keys, subjects, force=args.force)
        if not success:
            log('PHASE 2 FAILED — stopping. Review errors, rerun failed subjects.')
            if args.step == 'all':
                sys.exit(1)

    if args.step in ('judge', 'all'):
        subjects = SUBJECTS if args.subject == 'all' else [s.strip() for s in args.subject.split(',')]
        judges = [args.judge] if args.judge else None
        success = phase_judge(api_keys, subjects, judges_to_run=judges, force=args.force)
        if not success:
            log('PHASE 3 FAILED — stopping. Review parse failures, rerun failed judges.')
            if args.step == 'all':
                sys.exit(1)

    if args.step in ('analyze', 'all'):
        phase_analyze()

    log(f'\nCompleted: {datetime.now(timezone.utc).isoformat()}')


if __name__ == '__main__':
    main()
