"""
LLM-as-Judge Evaluation Framework
Test 2: Judge given a PERFECT verbatim response (held-out passage = response)
Test 3: Judge given correct but paraphrased response vs verbatim
Test 4: Judge given long correct vs short correct response

Isolates judge failure modes from model failure modes.
"""
import json, httpx, subprocess, os, time
from collections import defaultdict

for k in ['ANTHROPIC_API_KEY', 'GEMINI_API_KEY']:
    r = subprocess.run(['powershell', '-Command',
        f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val: os.environ[k] = val

api_key = os.environ['ANTHROPIC_API_KEY']
gemini_key = os.environ['GEMINI_API_KEY']

battery = json.load(open('data/experiments/memory_systems/battery/questions_80.json'))
bp_questions = [q for q in battery['questions']
                if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


def judge_haiku(prompt):
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


def judge_gemini(prompt):
    try:
        resp = httpx.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}',
            json={'contents': [{'parts': [{'text': prompt}]}]}, timeout=30)
        if resp.status_code == 200:
            t = resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return int(t[0]) if t and t[0].isdigit() else 0
        elif resp.status_code == 429:
            time.sleep(10)
        return 0
    except:
        return 0


def jp(ho, response):
    return ('You are evaluating whether a response about a person PREDICTED '
            'what actually happened.\n\n'
            '=== HELD-OUT GROUND TRUTH ===\n' + ho + '\n\n'
            '=== RESPONSE ===\n' + response + '\n\n'
            'Rate 1-5:\n'
            '5=Predicts specific outcome\n'
            '4=General direction correct\n'
            '3=Right domain wrong outcome\n'
            '2=Wrong prediction\n'
            '1=Refuses or off-base\n\n'
            'Respond with ONLY a single digit (1-5).')


def paraphrase(text):
    """Generate a paraphrased version via Haiku."""
    try:
        resp = httpx.post('https://api.anthropic.com/v1/messages',
            json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 512, 'temperature': 0,
                  'messages': [{'role': 'user',
                                'content': f'Paraphrase this passage in your own words. '
                                           f'Keep all the facts but change the wording completely. '
                                           f'Do NOT use any of the original phrases.\n\n{text}'}]},
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'}, timeout=30)
        return resp.json()['content'][0]['text']
    except:
        return text


print('=== LLM-AS-JUDGE EVALUATION FRAMEWORK ===\n', flush=True)

# Use first 20 questions for speed
test_qs = bp_questions[:20]
print(f'Using {len(test_qs)} questions\n', flush=True)

all_judgments = []

# TEST 2: Judge given PERFECT verbatim response
# The response IS the held-out passage. Judge should score 5.
print('--- TEST 2: Verbatim response (response = held-out passage) ---', flush=True)
for q in test_qs:
    prompt = jp(q['held_out_passage'], q['held_out_passage'])
    h = judge_haiku(prompt)
    g = judge_gemini(prompt)
    all_judgments.append({'test': 'verbatim', 'qid': q['id'], 'haiku': h, 'gemini': g})
    time.sleep(0.3)
h_scores = [j['haiku'] for j in all_judgments if j['test'] == 'verbatim' and j['haiku'] > 0]
g_scores = [j['gemini'] for j in all_judgments if j['test'] == 'verbatim' and j['gemini'] > 0]
print(f'  Haiku: {sum(h_scores)/len(h_scores):.2f} (n={len(h_scores)}) '
      f'dist={[h_scores.count(i) for i in range(1,6)]}', flush=True)
print(f'  Gemini: {sum(g_scores)/len(g_scores):.2f} (n={len(g_scores)}) '
      f'dist={[g_scores.count(i) for i in range(1,6)]}', flush=True)
print(f'  Expected: 5.0 (identical text)\n', flush=True)

# TEST 3: Paraphrased correct response vs verbatim
# Generate paraphrases, then judge both
print('--- TEST 3: Paraphrased correct vs verbatim ---', flush=True)
print('  Generating paraphrases...', flush=True)
for q in test_qs:
    para = paraphrase(q['held_out_passage'])
    prompt = jp(q['held_out_passage'], para)
    h = judge_haiku(prompt)
    g = judge_gemini(prompt)
    all_judgments.append({'test': 'paraphrased', 'qid': q['id'], 'haiku': h, 'gemini': g})
    time.sleep(0.3)
h_scores = [j['haiku'] for j in all_judgments if j['test'] == 'paraphrased' and j['haiku'] > 0]
g_scores = [j['gemini'] for j in all_judgments if j['test'] == 'paraphrased' and j['gemini'] > 0]
print(f'  Haiku: {sum(h_scores)/len(h_scores):.2f} (n={len(h_scores)}) '
      f'dist={[h_scores.count(i) for i in range(1,6)]}', flush=True)
print(f'  Gemini: {sum(g_scores)/len(g_scores):.2f} (n={len(g_scores)}) '
      f'dist={[g_scores.count(i) for i in range(1,6)]}', flush=True)
print(f'  Expected: ~5.0 (same content, different words)\n', flush=True)

# TEST 4: Long correct vs short correct
# Short: first sentence of held-out. Long: held-out + extra elaboration
print('--- TEST 4: Short correct vs long correct ---', flush=True)

# Short version: first sentence only
for q in test_qs:
    first_sentence = q['held_out_passage'].split('.')[0] + '.'
    prompt = jp(q['held_out_passage'], first_sentence)
    h = judge_haiku(prompt)
    g = judge_gemini(prompt)
    all_judgments.append({'test': 'short_correct', 'qid': q['id'], 'haiku': h, 'gemini': g})
    time.sleep(0.3)

# Long version: held-out + elaboration
for q in test_qs:
    long_response = (q['held_out_passage'] +
                     '\n\nThis behavior is consistent with the subject\'s established patterns '
                     'of careful deliberation, preference for direct experience over abstract '
                     'instruction, and willingness to make unconventional choices when they '
                     'align with deeply held values. The decision reflects both practical '
                     'reasoning and emotional conviction, as the subject weighs immediate '
                     'circumstances against long-term aspirations.')
    prompt = jp(q['held_out_passage'], long_response)
    h = judge_haiku(prompt)
    g = judge_gemini(prompt)
    all_judgments.append({'test': 'long_correct', 'qid': q['id'], 'haiku': h, 'gemini': g})
    time.sleep(0.3)

h_short = [j['haiku'] for j in all_judgments if j['test'] == 'short_correct' and j['haiku'] > 0]
g_short = [j['gemini'] for j in all_judgments if j['test'] == 'short_correct' and j['gemini'] > 0]
h_long = [j['haiku'] for j in all_judgments if j['test'] == 'long_correct' and j['haiku'] > 0]
g_long = [j['gemini'] for j in all_judgments if j['test'] == 'long_correct' and j['gemini'] > 0]

print(f'  Short correct (first sentence only):', flush=True)
print(f'    Haiku: {sum(h_short)/len(h_short):.2f} (n={len(h_short)}) '
      f'dist={[h_short.count(i) for i in range(1,6)]}', flush=True)
print(f'    Gemini: {sum(g_short)/len(g_short):.2f} (n={len(g_short)}) '
      f'dist={[g_short.count(i) for i in range(1,6)]}', flush=True)
print(f'  Long correct (verbatim + elaboration):', flush=True)
print(f'    Haiku: {sum(h_long)/len(h_long):.2f} (n={len(h_long)}) '
      f'dist={[h_long.count(i) for i in range(1,6)]}', flush=True)
print(f'    Gemini: {sum(g_long)/len(g_long):.2f} (n={len(g_long)}) '
      f'dist={[g_long.count(i) for i in range(1,6)]}', flush=True)
print(f'  Length bias = long - short. >0 means length inflates scores.\n', flush=True)

# SUMMARY
print('=== SUMMARY ===\n', flush=True)
tests = {
    'verbatim': 'Identical text (pure judge test)',
    'paraphrased': 'Correct content, different words',
    'short_correct': 'First sentence only',
    'long_correct': 'Verbatim + elaboration padding',
}
print(f'{"Test":<25} {"Haiku":>7} {"Gemini":>7} {"What it measures"}', flush=True)
print('=' * 75, flush=True)
for test_name, description in tests.items():
    h = [j['haiku'] for j in all_judgments if j['test'] == test_name and j['haiku'] > 0]
    g = [j['gemini'] for j in all_judgments if j['test'] == test_name and j['gemini'] > 0]
    h_avg = sum(h) / len(h) if h else 0
    g_avg = sum(g) / len(g) if g else 0
    print(f'  {test_name:<23} {h_avg:>7.2f} {g_avg:>7.2f}   {description}', flush=True)

print(f'\nIf verbatim < 5.0: judge has a problem (can\'t recognize identical text)', flush=True)
print(f'If paraphrased < verbatim: judge penalizes rewording', flush=True)
print(f'If long > short: judge has length bias', flush=True)
print(f'If long > verbatim: judge rewards padding', flush=True)

# Save
outdir = 'data/experiments/memory_systems/results/judge_evaluation'
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, 'judgments.json'), 'w') as f:
    json.dump(all_judgments, f, indent=2)
print(f'\nSaved to {outdir}', flush=True)
