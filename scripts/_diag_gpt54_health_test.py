"""Single GPT-5.4 health test using the same prompt template wrong_spec_v2 used."""
import os, subprocess, time, httpx, json

# Load API key
r = subprocess.run(['powershell', '-Command',
    "[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')"],
    capture_output=True, text=True)
key = r.stdout.strip()
assert key, "OPENAI_API_KEY not found"

# Load one zitkala_sa response
data = json.load(open(
    'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_zitkala_sa/wrong_spec_v2_results.json',
    encoding='utf-8'))
q = data[0]
qt = q['question_text']
ho = q['held_out_passage']
resp_text = q['response']['text']

JUDGE_PROMPT = """You are evaluating a behavioral prediction against a verbatim ground truth passage.

Question: {question}

Ground truth (what actually happened): {ground_truth}

Response to score: {response}

Score 1-5 based on prediction accuracy:
5 = Predicts the specific outcome or behavior in the ground truth
4 = Predicts the general direction correctly with some specifics
3 = Captures the right domain but not the specific outcome
2 = Addresses the topic but predicts incorrectly
1 = Refuses to answer or is completely off-base

Respond with only the number 1, 2, 3, 4, or 5."""

prompt = JUDGE_PROMPT.format(question=qt, ground_truth=ho, response=resp_text)
print(f"Prompt length: {len(prompt)} chars")

t0 = time.time()
r = httpx.post('https://api.openai.com/v1/chat/completions',
    json={'model': 'gpt-5.4', 'max_completion_tokens': 10, 'temperature': 0,
          'messages': [{'role': 'user', 'content': prompt}]},
    headers={'Authorization': f"Bearer {key}",
             'Content-Type': 'application/json'},
    timeout=60)
dt = time.time() - t0

print(f"Status: {r.status_code}")
print(f"Time: {dt:.2f}s")
print(f"Rate-limit headers: {[(k,v) for k,v in r.headers.items() if 'ratelimit' in k.lower() or 'retry' in k.lower()]}")
if r.status_code == 200:
    body = r.json()
    print(f"Raw: {body['choices'][0]['message']['content']!r}")
    print(f"Usage: {body.get('usage')}")
else:
    print(f"Body: {r.text[:500]}")
