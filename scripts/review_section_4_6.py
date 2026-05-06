"""
Ad-hoc: cross-LLM review of §4.6 Interpretation vs. Recall.
Focused review prompt — understandability, logic, table readability.
Writes raw responses to docs/reviews/section_4_6_review_<timestamp>.md.
"""

import os
import sys
import json
import subprocess
import datetime
import urllib.request
import urllib.error
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAYLOAD_PATH = REPO_ROOT / 'docs' / 'reviews' / '_section_4_6_payload.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_payload():
    return PAYLOAD_PATH.read_text(encoding='utf-8').strip()


REVIEW_PROMPT = """You are reviewing §4.6 of a research paper titled "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization." The section is included below. The paper studies whether a compact behavioral specification can improve AI prediction of how a specific person would respond in novel situations, on top of commercial memory systems (Mem0, Letta, Zep, Supermemory) and an open-source retrieval substrate (Base Layer).

§4.6 Interpretation vs. Recall is the per-question analysis section. Prior sections §4.4 and §4.5 established aggregate numbers per memory system and confirmed robustness across judges and response models. §4.6 is where the paper looks inside the aggregates and explains what's producing them at the per-question level.

Please review §4.6 for:

1. **Understandability.** Is the opening paragraph clear to a reader who has read §1 through §4.5? Does the plain-language explanation of the per-question distribution land, or does it still read as jargon?
2. **Logic.** Are the three mechanisms (pattern supply, over-theorization, structural refusal) clearly distinguished? Does the cross-system reproduction claim hold up given the evidence presented?
3. **Keckley Q21 framing.** Is the "single cleanest cross-substrate replication" claim well-supported by the table? Is the interpretation (property of the specification, not the memory system) defensible?
4. **Table readability.** Does the per-subject paired-delta table communicate "every row is a mixture" effectively? Any columns that should be reordered or dropped?
5. **Logical gaps or claims not supported.** Any sentence in §4.6 that a skeptical reader would flag as unsupported by the data shown?
6. **Voice issues.** Any remaining jargon, GTM-style verbs ("beats", "crushes", "dominates"), em-dashes in prose, or sentences that sound like marketing rather than research.
7. **What's missing.** Any per-question framing question that a reader would expect §4.6 to address but doesn't.

Respond with (a) overall grade A/B/C/D/F for intelligibility and logic, (b) top 3 fixable issues in priority order, (c) anything that would require an expanded experiment to resolve (these go to §8 Future Work; not in scope for §4.6 rewrite).

§4.6 text follows:

{payload}
"""


def review_gemini(payload, api_key):
    results = {}
    for model_id, label in [
        ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
        ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload_body = json.dumps({
            'contents': [{'parts': [{'text': REVIEW_PROMPT.format(payload=payload)}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 2048}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload_body, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/2.31.0'
        })
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['candidates'][0]['content']['parts'][0]['text']
                results[label] = text
                print(f'  [{label}] done ({len(text)} chars)')
        except Exception as e:
            results[label] = f'ERROR: {e}'
            print(f'  [{label}] ERROR: {e}')
    return results


def review_groq(payload, api_key):
    url = 'https://api.groq.com/openai/v1/chat/completions'
    body = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(payload=payload)}],
        'temperature': 0.3,
        'max_tokens': 2048
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Groq Llama 3.3 70B] done ({len(text)} chars)')
            return {'Groq Llama 3.3 70B': text}
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B': f'ERROR: {e}'}


def review_cerebras(payload, api_key):
    url = 'https://api.cerebras.ai/v1/chat/completions'
    body = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(payload=payload)}],
        'temperature': 0.3,
        'max_tokens': 2048
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                body_txt = ''
                try:
                    body_txt = e.read().decode()[:300]
                except Exception:
                    pass
                print(f'  [Cerebras] ERROR: {e.code}: {body_txt}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body_txt}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_mistral(payload, api_key):
    url = 'https://api.mistral.ai/v1/chat/completions'
    body = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(payload=payload)}],
        'temperature': 0.3,
        'max_tokens': 2048
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Mistral Large] done ({len(text)} chars)')
            return {'Mistral Large': text}
    except Exception as e:
        print(f'  [Mistral] ERROR: {e}')
        return {'Mistral Large': f'ERROR: {e}'}


def save_results(all_reviews):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'section_4_6_review_{ts}.md'
    lines = [
        f'# §4.6 Interpretation vs. Recall — Cross-LLM Review',
        f'_Generated: {ts}_',
        f'',
        f'Providers queried: Mistral Large, Gemini 2.5 Pro, Gemini 2.5 Flash, Cerebras Qwen3 235B, Groq Llama 3.3 70B',
        f'',
        f'Payload: `docs/reviews/_section_4_6_payload.md`',
        f'',
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}\n')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    missing = [k for k, v in [
        ('GEMINI', gemini_key),
        ('GROQ', groq_key),
        ('CEREBRAS', cerebras_key),
        ('MISTRAL', mistral_key)
    ] if not v]
    if missing:
        print(f'Missing keys: {missing} (will skip those providers)')

    print('Loading §4.6 payload...')
    payload = load_payload()
    print(f'Payload: {len(payload)} chars, ~{len(payload)//4} tokens\n')

    all_reviews = {}

    if mistral_key:
        print('Sending to Mistral Large (REQUIRED)...')
        all_reviews.update(review_mistral(payload, mistral_key))
    else:
        all_reviews['Mistral Large'] = 'SKIPPED: no MISTRAL_API_KEY'

    if gemini_key:
        print('Sending to Gemini...')
        all_reviews.update(review_gemini(payload, gemini_key))
    else:
        all_reviews['Gemini 2.5 Pro'] = 'SKIPPED: no GEMINI_API_KEY'
        all_reviews['Gemini 2.5 Flash'] = 'SKIPPED: no GEMINI_API_KEY'

    if cerebras_key:
        print('Sending to Cerebras...')
        all_reviews.update(review_cerebras(payload, cerebras_key))
    else:
        all_reviews['Cerebras Qwen3 235B'] = 'SKIPPED: no CEREBRAS_API_KEY'

    if groq_key:
        print('Sending to Groq...')
        all_reviews.update(review_groq(payload, groq_key))
    else:
        all_reviews['Groq Llama 3.3 70B'] = 'SKIPPED: no GROQ_API_KEY'

    out_path = save_results(all_reviews)
    print(f'\nDone. {len(all_reviews)} providers.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
