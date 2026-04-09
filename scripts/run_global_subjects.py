"""
Global Subjects Pipeline — Process 8 new subjects overnight.
For each: split corpus → extract facts → generate battery → run full-stack conditions → judge.
"""
import json, os, sys, time, subprocess, random, hashlib, httpx, pathlib
from datetime import datetime, timezone
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env
for k in ['ANTHROPIC_API_KEY', 'GEMINI_API_KEY']:
    r = subprocess.run(['powershell', '-Command',
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val: os.environ[k] = val

api_key = os.environ['ANTHROPIC_API_KEY']
gemini_key = os.environ['GEMINI_API_KEY']

SUBJECTS = [
    {'name': 'keckley', 'display': 'Elizabeth Keckley', 'region': 'Black American',
     'corpus': 'data/corpora/keckley/raw.txt'},
    {'name': 'sunity_devee', 'display': 'Sunity Devee', 'region': 'Indian',
     'corpus': 'data/corpora/sunity_devee/raw.txt'},
    {'name': 'zitkala_sa', 'display': 'Zitkala-Sa', 'region': 'Native American',
     'corpus': 'data/corpora/zitkala_sa/raw.txt'},
    {'name': 'equiano', 'display': 'Olaudah Equiano', 'region': 'West African',
     'corpus': 'data/corpora/equiano/raw.txt'},
    {'name': 'seacole', 'display': 'Mary Seacole', 'region': 'Caribbean',
     'corpus': 'data/corpora/seacole/raw.txt'},
    {'name': 'fukuzawa', 'display': 'Fukuzawa Yukichi', 'region': 'Japanese',
     'corpus': 'data/corpora/fukuzawa/raw.txt'},
    {'name': 'babur', 'display': 'Babur', 'region': 'Central Asian/Muslim',
     'corpus': 'data/corpora/babur/raw.txt'},
    {'name': 'yung_wing', 'display': 'Yung Wing', 'region': 'Chinese',
     'corpus': 'data/corpora/yung_wing/raw.txt'},
    {'name': 'cellini', 'display': 'Benvenuto Cellini', 'region': 'Italian/Renaissance',
     'corpus': 'data/corpora/cellini/raw.txt'},
    {'name': 'bernal_diaz', 'display': 'Bernal Diaz del Castillo', 'region': 'Latin American/Spanish',
     'corpus': 'data/corpora/bernal_diaz/raw.txt'},
    {'name': 'ebers', 'display': 'Georg Ebers', 'region': 'German',
     'corpus': 'data/corpora/ebers/raw.txt'},
    {'name': 'rousseau', 'display': 'Jean-Jacques Rousseau', 'region': 'French',
     'corpus': 'data/corpora/rousseau/raw.txt'},
    {'name': 'augustine', 'display': 'Saint Augustine', 'region': 'North African/Roman',
     'corpus': 'data/corpora/augustine/raw.txt'},
]


def chunk_text(text, max_words=3000, overlap=200):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(' '.join(words[start:end]))
        start = end - overlap if end < len(words) else end
    return chunks


def extract_facts(corpus_text, subject_name):
    """Extract facts using Haiku."""
    chunks = chunk_text(corpus_text)
    all_facts = []
    for i, chunk in enumerate(chunks):
        prompt = (f'Extract factual assertions from this autobiography text about {subject_name}. '
                  'Each fact should be a single, self-contained declarative sentence. '
                  'Include facts about values, decisions, relationships, habits, beliefs, '
                  'events, personality traits, skills, preferences. '
                  'Return ONLY a JSON array of strings.')
        try:
            resp = httpx.post('https://api.anthropic.com/v1/messages',
                json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 4096, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt + '\n\nText:\n' + chunk}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=60)
            text = resp.json()['content'][0]['text'].strip()
            if text.startswith('```'): text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
            facts = json.loads(text)
            all_facts.extend(facts)
        except Exception as e:
            print(f'    Chunk {i} error: {e}', flush=True)
        if (i + 1) % 5 == 0:
            print(f'    {i + 1}/{len(chunks)} chunks ({len(all_facts)} facts)', flush=True)

    # Dedup
    seen = set()
    unique = []
    for f in all_facts:
        n = f.strip().lower()
        if n not in seen:
            seen.add(n)
            unique.append(f.strip())
    return unique


def generate_battery(training_text, heldout_text, subject_name):
    """Generate 40 behavioral prediction questions using Opus-like Haiku calls."""
    # Ask Haiku to generate questions backward from held-out text
    prompt = (f'You are designing a behavioral prediction test for {subject_name}.\n\n'
              f'TRAINING TEXT (what the model will know):\n{training_text[:3000]}\n\n'
              f'HELD-OUT TEXT (ground truth the model has NOT seen):\n{heldout_text[:5000]}\n\n'
              'Generate 20 behavioral prediction questions. For each question:\n'
              '1. Find a specific decision/behavior/reaction in the HELD-OUT text\n'
              '2. Write a question that can be answered from TRAINING patterns\n'
              '3. Extract the exact held-out passage as ground truth\n\n'
              'Return a JSON array of objects with fields: '
              '"text" (the question), "held_out_passage" (exact quote from held-out), '
              '"category" (one of: decisions, values, relationships, conflict, learning, risk)\n\n'
              'Return ONLY the JSON array.')

    questions = []
    # Two batches of 20 to get 40
    for batch in range(2):
        offset = batch * 2000
        try:
            resp = httpx.post('https://api.anthropic.com/v1/messages',
                json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 4096, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': prompt.replace(
                          heldout_text[:5000], heldout_text[offset:offset + 5000])}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'}, timeout=120)
            text = resp.json()['content'][0]['text'].strip()
            if text.startswith('```'): text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
            batch_qs = json.loads(text)
            questions.extend(batch_qs)
        except Exception as e:
            print(f'    Battery batch {batch} error: {e}', flush=True)

    # Build full battery
    battery = {'metadata': {'subject': subject_name, 'total': len(questions) + 20,
                            'tiers': {'behavioral_prediction': len(questions),
                                      'recall': 10, 'adversarial_abstention': 10}},
               'questions': []}

    for i, q in enumerate(questions):
        battery['questions'].append({
            'id': i + 1, 'tier': 'behavioral_prediction',
            'category': q.get('category', 'decisions'),
            'text': q['text'], 'held_out_passage': q.get('held_out_passage', ''),
        })

    # Add 10 baseline/adversarial questions
    for i in range(10):
        battery['questions'].append({
            'id': len(questions) + i + 1, 'tier': 'adversarial_abstention',
            'category': 'adversarial',
            'text': f'What was {subject_name}\'s opinion on modern technology?',
            'held_out_passage': None,
        })

    return battery


def gen_response(question, system_prompt):
    resp = httpx.post('https://api.anthropic.com/v1/messages',
        json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 1024, 'temperature': 0,
              'system': system_prompt,
              'messages': [{'role': 'user', 'content': question}]},
        headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                 'content-type': 'application/json'}, timeout=60)
    resp.raise_for_status()
    d = resp.json()
    return {'text': d['content'][0]['text'],
            'input_tokens': d['usage']['input_tokens'],
            'output_tokens': d['usage']['output_tokens']}


def judge_haiku(held_out, response_text):
    prompt = ('You are evaluating whether a response about a person PREDICTED what actually happened.'
              '\n\n=== HELD-OUT GROUND TRUTH ===\n' + held_out +
              '\n\n=== RESPONSE ===\n' + response_text[:1500] +
              '\n\nRate 1-5:\n5=Predicts specific outcome\n4=General direction correct'
              '\n3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base'
              '\n\nRespond with ONLY a single digit (1-5).')
    try:
        resp = httpx.post('https://api.anthropic.com/v1/messages',
            json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 8, 'temperature': 0,
                  'messages': [{'role': 'user', 'content': prompt}]},
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'}, timeout=30)
        t = resp.json()['content'][0]['text'].strip()
        return int(t[0]) if t and t[0].isdigit() else 0
    except:
        return 0


def process_subject(subject):
    name = subject['name']
    display = subject['display']
    region = subject['region']

    print(f'\n{"="*60}', flush=True)
    print(f'PROCESSING: {display} ({region})', flush=True)
    print(f'{"="*60}', flush=True)

    # Read corpus
    corpus = open(subject['corpus'], encoding='utf-8', errors='ignore').read()
    words = corpus.split()
    total_words = len(words)
    print(f'  Corpus: {total_words} words', flush=True)

    # Strip Gutenberg header/footer
    start_markers = ['*** START OF', '***START OF']
    end_markers = ['*** END OF', '***END OF', 'End of the Project Gutenberg', 'End of Project Gutenberg']
    for m in start_markers:
        idx = corpus.find(m)
        if idx >= 0:
            corpus = corpus[corpus.find('\n', idx) + 1:]
            break
    for m in end_markers:
        idx = corpus.find(m)
        if idx >= 0:
            corpus = corpus[:idx]
            break

    words = corpus.split()
    total_words = len(words)
    print(f'  After stripping: {total_words} words', flush=True)

    # Split 50/50 training/held-out
    mid = total_words // 2
    training = ' '.join(words[:mid])
    heldout = ' '.join(words[mid:])
    print(f'  Training: {len(training.split())} words, Held-out: {len(heldout.split())} words', flush=True)

    # Save training corpus
    outdir = os.path.join(BASE_DIR, 'results', f'global_{name}')
    os.makedirs(outdir, exist_ok=True)

    with open(os.path.join(outdir, 'training.txt'), 'w', encoding='utf-8') as f:
        f.write(training)
    with open(os.path.join(outdir, 'heldout.txt'), 'w', encoding='utf-8') as f:
        f.write(heldout)

    # Step 1: Extract facts from training text
    print(f'  Step 1: Extracting facts...', flush=True)
    facts = extract_facts(training, display)
    print(f'  Extracted {len(facts)} facts', flush=True)

    facts_data = {'metadata': {'subject': display, 'total_facts': len(facts)},
                  'facts': [{'id': i + 1, 'text': f} for i, f in enumerate(facts)]}
    with open(os.path.join(outdir, 'facts.json'), 'w', encoding='utf-8') as f:
        json.dump(facts_data, f, indent=2, ensure_ascii=False)

    # Step 2: Generate question battery
    print(f'  Step 2: Generating battery...', flush=True)
    battery = generate_battery(training, heldout, display)
    bp_count = sum(1 for q in battery['questions'] if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage'))
    print(f'  Generated {len(battery["questions"])} questions ({bp_count} behavioral prediction)', flush=True)

    with open(os.path.join(outdir, 'battery.json'), 'w', encoding='utf-8') as f:
        json.dump(battery, f, indent=2, ensure_ascii=False)

    # Step 3: Generate spec (use facts as input to Haiku for a lightweight spec)
    print(f'  Step 3: Generating spec...', flush=True)
    facts_text = '\n'.join(f'- {f}' for f in facts[:200])  # Cap at 200 for prompt size
    spec_prompt = (f'You are creating a behavioral specification for {display}. '
                   'Based on these facts, write a compressed document describing how this person '
                   'thinks, decides, and acts. Focus on: decision patterns, values, '
                   'conflict resolution, learning style, risk tolerance, relationship dynamics. '
                   'Write in third person. Be specific and behavioral, not biographical.\n\n'
                   f'Facts:\n{facts_text}')
    try:
        resp = httpx.post('https://api.anthropic.com/v1/messages',
            json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 4096, 'temperature': 0,
                  'messages': [{'role': 'user', 'content': spec_prompt}]},
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'}, timeout=120)
        spec = resp.json()['content'][0]['text']
    except Exception as e:
        spec = ''
        print(f'    Spec generation failed: {e}', flush=True)

    print(f'  Spec: {len(spec.split())} words', flush=True)
    with open(os.path.join(outdir, 'spec.md'), 'w', encoding='utf-8') as f:
        f.write(spec)

    # Step 4: Run conditions on behavioral prediction questions
    print(f'  Step 4: Running conditions...', flush=True)
    bp_questions = [q for q in battery['questions']
                    if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]

    ft_all = '\n'.join(f'- {f}' for f in facts)
    random.seed(42)
    results = []

    for q_idx, q in enumerate(bp_questions):
        q_text = q['text']
        q_result = {'question_id': q['id'], 'question_text': q_text,
                    'held_out_passage': q['held_out_passage'],
                    'responses': {}}

        # C5: Baseline
        try:
            r = gen_response(q_text, 'Answer the following question.')
            q_result['responses']['C5_baseline'] = r
        except:
            pass

        # C2a: Spec only
        if spec:
            try:
                r = gen_response(q_text,
                    'The following is a behavioral specification describing your user.\n\n'
                    '=== BEHAVIORAL SPECIFICATION ===\n' + spec)
                q_result['responses']['C2a_spec'] = r
            except:
                pass

        # C4: All facts
        try:
            r = gen_response(q_text,
                'The following is a complete set of known facts about the person '
                'this question concerns.\n\n=== FACTS ===\n' + ft_all)
            q_result['responses']['C4_factdump'] = r
        except:
            pass

        # C4a: All facts + spec
        if spec:
            try:
                r = gen_response(q_text,
                    'The following is a behavioral specification describing your user. '
                    'You also have the complete set of known facts.\n\n'
                    '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                    '=== ALL KNOWN FACTS ===\n' + ft_all)
                q_result['responses']['C4a_facts_plus_spec'] = r
            except:
                pass

        results.append(q_result)
        if (q_idx + 1) % 10 == 0:
            print(f'    {q_idx + 1}/{len(bp_questions)} questions', flush=True)

    with open(os.path.join(outdir, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Step 5: Judge with Haiku
    print(f'  Step 5: Judging...', flush=True)
    judgments = []
    for r in results:
        ho = r.get('held_out_passage', '')
        if not ho:
            continue
        for cond, resp in r['responses'].items():
            txt = resp.get('text', '')
            if not txt:
                continue
            score = judge_haiku(ho, txt)
            judgments.append({'question_id': r['question_id'], 'condition': cond,
                             'haiku_score': score})

    with open(os.path.join(outdir, 'judgments.json'), 'w', encoding='utf-8') as f:
        json.dump(judgments, f, indent=2)

    # Report
    scores = defaultdict(list)
    for j in judgments:
        if j['haiku_score'] > 0:
            scores[j['condition']].append(j['haiku_score'])

    print(f'\n  RESULTS: {display} ({region})', flush=True)
    print(f'  {"Condition":<25} {"Haiku":>7} {"n":>4}', flush=True)
    for c in sorted(scores, key=lambda c: -sum(scores[c]) / len(scores[c])):
        avg = sum(scores[c]) / len(scores[c])
        print(f'  {c:<25} {avg:>7.2f} {len(scores[c]):>4}', flush=True)

    return {'name': name, 'display': display, 'region': region,
            'corpus_words': total_words, 'facts': len(facts),
            'questions': len(bp_questions), 'spec_words': len(spec.split()),
            'scores': {c: sum(s) / len(s) for c, s in scores.items()}}


def main():
    print('=== GLOBAL SUBJECTS PIPELINE ===', flush=True)
    print(f'{len(SUBJECTS)} subjects to process', flush=True)
    print(f'Started: {datetime.now(timezone.utc).isoformat()}', flush=True)

    all_results = []
    for subject in SUBJECTS:
        try:
            result = process_subject(subject)
            all_results.append(result)
        except Exception as e:
            print(f'\n  FAILED: {subject["display"]} — {e}', flush=True)
            all_results.append({'name': subject['name'], 'display': subject['display'],
                               'error': str(e)})

    # Final summary
    print(f'\n\n{"="*60}', flush=True)
    print(f'GLOBAL SUBJECTS — FINAL SUMMARY', flush=True)
    print(f'{"="*60}', flush=True)
    print(f'{"Subject":<25} {"Region":<20} {"Words":>8} {"Facts":>6} {"C5":>6} {"C2a":>6} {"C4a":>6}', flush=True)
    for r in all_results:
        if 'error' in r:
            print(f'  {r["display"]:<23} FAILED: {r["error"][:40]}', flush=True)
        else:
            c5 = r['scores'].get('C5_baseline', 0)
            c2a = r['scores'].get('C2a_spec', 0)
            c4a = r['scores'].get('C4a_facts_plus_spec', 0)
            print(f'  {r["display"]:<23} {r["region"]:<18} {r["corpus_words"]:>8} {r["facts"]:>6} '
                  f'{c5:>6.2f} {c2a:>6.2f} {c4a:>6.2f}', flush=True)

    with open(os.path.join(BASE_DIR, 'results', 'global_summary.json'), 'w') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f'\nCompleted: {datetime.now(timezone.utc).isoformat()}', flush=True)


if __name__ == '__main__':
    main()
