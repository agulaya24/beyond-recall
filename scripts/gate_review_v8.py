"""
Beyond Recall v8 — Full-Paper Gate Review.

Final gate review before publication. Runs across all available non-Gemini
providers: Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B,
OpenAI GPT-5.4, Anthropic Claude Opus (external-instance review).

Usage: python gate_review_v8.py
"""

import os
import sys
import json
import subprocess
import datetime
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v8_draft.md'
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
    # Strip HTML comments (internal editorial notes)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


GATE_PROMPT = """You are doing a gate review of a completed research paper draft before publication. The author wants a final check for factual errors, unsupported claims, internal contradictions, logical gaps, and residual voice issues. The paper has already been through multiple rounds of review; this is the final pass.

Paper title: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

Your review should focus ONLY on:
1. Load-bearing claims not supported by the data shown (cite section + quote)
2. Factual errors or internal contradictions across sections
3. Logical gaps in the argument
4. Remaining voice or marketing-register issues (the paper has had voice sweeps; focus on residual only)
5. Missing cross-references
6. Structural integrity — any section that feels out of place or redundant

Do NOT recommend:
- Stylistic preferences or word choices where the current phrasing is defensible
- Full rewrites
- Expansions of topics already covered elsewhere in the paper
- Section 8 Future Work completeness (it is a deliberate research agenda)

Respond with these EXACT sections:

## (a) OVERALL GATE VERDICT
One of: "READY TO PUBLISH" | "READY WITH MINOR FIXES LISTED BELOW" | "NEEDS SUBSTANTIVE WORK BEFORE PUBLISH"
Then a 1-2 sentence justification.

## (b) CRITICAL ISSUES (gate publication)
List by priority. For each:
- Section + quoted text
- Why it gates publication
- Specific fix

## (c) MINOR ISSUES (fix quickly or leave)
Brief bullets. Each with section reference.

## (d) STRUCTURAL CONCERNS
Any section that feels out of place, redundant, or broken in flow. If none, say "None."

Be specific. Cite sections. Quote. Do not be diplomatic — if the paper is ready, say so. If it is not, be explicit about what gates it.

Paper text follows:

---

{paper}
"""


def review_mistral(paper, api_key):
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}],
        'temperature': 0.2,
        'max_tokens': 6000
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=360) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Mistral Large] done ({len(text)} chars)')
            return {'Mistral Large': text}
    except Exception as e:
        body = ''
        if isinstance(e, urllib.error.HTTPError):
            try: body = e.read().decode()[:300]
            except Exception: pass
        print(f'  [Mistral] ERROR: {e} | {body}')
        return {'Mistral Large': f'ERROR: {e} | {body}'}


def review_cerebras(paper, api_key):
    # Cerebras qwen3 235B has ~128k context; full paper should fit.
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}],
        'temperature': 0.2,
        'max_tokens': 6000
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=360) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:400]
            except Exception: pass
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                print(f'  [Cerebras Qwen3 235B] ERROR: {e.code}: {body}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras Qwen3 235B] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}
    return {'Cerebras Qwen3 235B': 'ERROR: all attempts failed'}


def review_groq(paper, api_key):
    # Groq free tier has payload/context limits. Use head + tail strategy:
    # opening (intro/methods/headline results) + later sections (discussion/limits).
    if len(paper) > 25000:
        head = paper[:14000]
        tail = paper[-10000:]
        paper_trunc = (
            head
            + '\n\n[...middle sections truncated for Groq payload limit — review what is visible...]\n\n'
            + tail
        )
    else:
        paper_trunc = paper

    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.2,
        'max_tokens': 4000
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Groq Llama 3.3 70B] done ({len(text)} chars)')
            return {'Groq Llama 3.3 70B (head+tail subset)': text}
    except Exception as e:
        body = ''
        if isinstance(e, urllib.error.HTTPError):
            try: body = e.read().decode()[:300]
            except Exception: pass
        print(f'  [Groq] ERROR: {e} | {body}')
        return {'Groq Llama 3.3 70B (head+tail subset)': f'ERROR: {e} | {body}'}


def review_openai(paper, api_key):
    # GPT-5.4. Full context should fit.
    url = 'https://api.openai.com/v1/chat/completions'
    for model_id in ['gpt-5.4', 'gpt-5-4', 'gpt-5']:
        payload = json.dumps({
            'model': model_id,
            'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}],
            'temperature': 0.2,
            'max_tokens': 6000
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0'
        })
        try:
            with urllib.request.urlopen(req, timeout=360) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [OpenAI {model_id}] done ({len(text)} chars)')
                return {f'OpenAI {model_id}': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:400]
            except Exception: pass
            print(f'  [OpenAI {model_id}] ERROR: {e.code}: {body}')
            # fall through to next model
        except Exception as e:
            print(f'  [OpenAI {model_id}] ERROR: {e}')
    return {'OpenAI GPT-5.4': 'ERROR: all model IDs failed'}


def review_anthropic(paper, api_key):
    # External-instance Claude Opus review. Different session / no conversation
    # continuity with the drafting instance = legitimate external review.
    url = 'https://api.anthropic.com/v1/messages'
    for model_id in ['claude-opus-4-6', 'claude-opus-4-5', 'claude-opus-4-7']:
        payload = json.dumps({
            'model': model_id,
            'max_tokens': 6000,
            'temperature': 0.2,
            'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}]
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'User-Agent': 'python-requests/2.31.0'
        })
        try:
            with urllib.request.urlopen(req, timeout=360) as resp:
                data = json.loads(resp.read())
                text = data['content'][0]['text']
                print(f'  [Anthropic {model_id}] done ({len(text)} chars)')
                return {f'Anthropic {model_id}': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:400]
            except Exception: pass
            print(f'  [Anthropic {model_id}] ERROR: {e.code}: {body}')
        except Exception as e:
            print(f'  [Anthropic {model_id}] ERROR: {e}')
    return {'Anthropic Claude Opus': 'ERROR: all model IDs failed'}


def save_raw(all_reviews, ts):
    out_path = REVIEWS_DIR / f'full_paper_gate_review_{ts}.md'
    lines = [
        '# Beyond Recall v8 — Full Paper Gate Review (Raw)',
        f'_Generated: {ts}_',
        f'_Paper: {PAPER_PATH.name} ({PAPER_PATH.stat().st_size} bytes)_',
        '',
        'Providers: Mistral Large, Cerebras Qwen3 235B, Groq Llama 3.3 70B, OpenAI GPT-5.4, Anthropic Claude Opus (external-instance).',
        'Gemini excluded per author policy.',
        '',
        'Review focus: factual errors, unsupported claims, internal contradictions, logical gaps, residual voice issues, missing cross-references, structural integrity.',
        '',
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}\n')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved raw reviews: {out_path}')
    return out_path


def main():
    print('Loading API keys from Windows env...')
    mistral_key = get_win_env('MISTRAL_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    groq_key = get_win_env('GROQ_API_KEY')
    openai_key = get_win_env('OPENAI_API_KEY')
    anthropic_key = get_win_env('ANTHROPIC_API_KEY')

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper path: {PAPER_PATH}')
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    all_reviews = {}

    if mistral_key:
        print('Sending to Mistral Large...')
        all_reviews.update(review_mistral(paper, mistral_key))
    else:
        print('Skipping Mistral - no key')

    if cerebras_key:
        print('Sending to Cerebras Qwen3 235B...')
        all_reviews.update(review_cerebras(paper, cerebras_key))
    else:
        print('Skipping Cerebras - no key')

    if groq_key:
        print('Sending to Groq Llama 3.3 70B (head+tail subset)...')
        all_reviews.update(review_groq(paper, groq_key))
    else:
        print('Skipping Groq - no key')

    if openai_key:
        print('Sending to OpenAI GPT-5.4...')
        all_reviews.update(review_openai(paper, openai_key))
    else:
        print('Skipping OpenAI - no key')

    if anthropic_key:
        print('Sending to Anthropic Claude Opus (external-instance)...')
        all_reviews.update(review_anthropic(paper, anthropic_key))
    else:
        print('Skipping Anthropic - no key')

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = save_raw(all_reviews, ts)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Raw review file: {out_path}')
    print(f'Timestamp: {ts}')


if __name__ == '__main__':
    main()
