"""Test the actual judge prompt with bumped maxOutputTokens."""

import os, sys, json
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from backfill_all_parse_failures import judge_prompt, load_env

load_env()
api_key = os.environ.get('GEMINI_API_KEY')

# Get a real prompt
data = json.load((REPO / 'results' / 'global_keckley' / 'baselayer_results.json').open(encoding='utf-8'))
q = next(x for x in data if x.get('question_id')==1 and 'C1_baselayer' in x.get('responses',{}))
ho = q['held_out_passage']
text = q['responses']['C1_baselayer']['text']
prompt = judge_prompt(ho, text)
print(f'Prompt length: {len(prompt)}')

# Test 1: maxOutputTokens=8 (current)
print('\n=== maxOutputTokens=8 ===')
r = httpx.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}',
    json={'contents': [{'parts': [{'text': prompt}]}],
          'generationConfig': {'temperature': 0, 'maxOutputTokens': 8}},
    timeout=60)
print(f'Status: {r.status_code}')
j = r.json()
print(json.dumps({k:v for k,v in j.items() if k != 'usageMetadata'}, indent=2)[:1500])
print(f'Usage: {j.get("usageMetadata")}')

# Test 2: maxOutputTokens=64
print('\n=== maxOutputTokens=64 ===')
r = httpx.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}',
    json={'contents': [{'parts': [{'text': prompt}]}],
          'generationConfig': {'temperature': 0, 'maxOutputTokens': 64}},
    timeout=60)
j = r.json()
print(json.dumps({k:v for k,v in j.items() if k != 'usageMetadata'}, indent=2)[:1500])
print(f'Usage: {j.get("usageMetadata")}')

# Test 3: Disable thinking
print('\n=== thinkingBudget=0, maxOutputTokens=16 ===')
r = httpx.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}',
    json={'contents': [{'parts': [{'text': prompt}]}],
          'generationConfig': {'temperature': 0, 'maxOutputTokens': 16,
                               'thinkingConfig': {'thinkingBudget': 0}}},
    timeout=60)
j = r.json()
print(json.dumps({k:v for k,v in j.items() if k != 'usageMetadata'}, indent=2)[:1500])
print(f'Usage: {j.get("usageMetadata")}')
