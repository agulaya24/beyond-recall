"""Debug gemini empty response - get full HTTP response."""

import os, sys
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))
from backfill_all_parse_failures import load_env

load_env()
api_key = os.environ.get('GEMINI_API_KEY')
print(f'Key set: {bool(api_key)}, prefix: {api_key[:6] if api_key else None}')

# Simple test
prompt = 'Reply with the digit 3.'
r = httpx.post(
    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}',
    json={'contents': [{'parts': [{'text': prompt}]}],
          'generationConfig': {'temperature': 0, 'maxOutputTokens': 8}},
    timeout=60,
)
print(f'Status: {r.status_code}')
import json
try:
    j = r.json()
    print(json.dumps(j, indent=2)[:1500])
except Exception as e:
    print(f'Body: {r.text[:1500]}')
