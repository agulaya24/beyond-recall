"""
Beyond Recall — Cross-LLM Paper Review Script
Sends the paper to all free API providers, collects structured feedback.
Usage: python review_paper.py [--round N]
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_arxiv_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
    # Strip HTML comments (internal review notes)
    import re
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


REVIEW_PROMPT = """You are reviewing a research paper for arXiv submission. Be a rigorous, honest peer reviewer.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

Read the full paper below, then provide structured feedback in exactly this format:

## CRITICAL ISSUES
Issues that would cause rejection or significantly undermine the claims. Be specific — cite section and claim.

## MISSING
Important content, analysis, or discussion that is absent and should be present.

## NEEDS EXPANSION
Areas that are present but underdeveloped given the claims being made.

## METHODOLOGY CONCERNS
Any issues with experimental design, statistical analysis, or evaluation validity.

## MINOR ISSUES
Small fixes: clarity, framing, wording, flow.

## VERDICT
One sentence: overall assessment and readiness for submission.

Be direct. Do not be diplomatic. If something is wrong, say so clearly. If the paper is strong, say that too.

---

PAPER:

{paper}
"""


def review_gemini(paper, api_key):
    import urllib.request
    import urllib.error

    results = {}
    for model_id, label in [
        ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
        ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': REVIEW_PROMPT.format(paper=paper)}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 4096}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                text = data['candidates'][0]['content']['parts'][0]['text']
                results[label] = text
                print(f'  [{label}] done ({len(text)} chars)')
        except Exception as e:
            results[label] = f'ERROR: {e}'
            print(f'  [{label}] ERROR: {e}')
    return results


def review_groq(paper, api_key):
    import urllib.request
    # Groq free tier has HTTP payload limit — truncate paper to ~40k chars
    paper_trunc = paper[:40000] + ('\n\n[Paper truncated for API limit — first 40k chars]' if len(paper) > 40000 else '')
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
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


def review_cerebras(paper, api_key):
    import urllib.request, urllib.error, time
    # Truncate for rate limit safety
    paper_trunc = paper[:40000] + ('\n\n[Paper truncated — first 40k chars]' if len(paper) > 40000 else '')
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                print(f'  [Cerebras] ERROR: {e.code}: {e.read().decode()[:100]}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_mistral(paper, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Mistral Large] done ({len(text)} chars)')
            return {'Mistral Large': text}
    except Exception as e:
        print(f'  [Mistral] ERROR: {e}')
        return {'Mistral Large': f'ERROR: {e}'}


def save_results(all_reviews, round_num):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'round_{round_num:02d}_{ts}.md'
    lines = [f'# Paper Review — Round {round_num}', f'_Generated: {ts}_\n']
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    round_num = 1
    for arg in sys.argv[1:]:
        if arg.startswith('--round'):
            round_num = int(arg.split('=')[-1]) if '=' in arg else int(sys.argv[sys.argv.index(arg)+1])

    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    missing = [k for k, v in [('GEMINI', gemini_key), ('GROQ', groq_key), ('CEREBRAS', cerebras_key), ('MISTRAL', mistral_key)] if not v]
    if missing:
        print(f'Missing keys: {missing}')
        sys.exit(1)

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    all_reviews = {}

    print('Sending to Gemini...')
    all_reviews.update(review_gemini(paper, gemini_key))

    print('Sending to Groq...')
    all_reviews.update(review_groq(paper, groq_key))

    print('Sending to Cerebras...')
    all_reviews.update(review_cerebras(paper, cerebras_key))

    print('Sending to Mistral...')
    all_reviews.update(review_mistral(paper, mistral_key))

    out_path = save_results(all_reviews, round_num)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
