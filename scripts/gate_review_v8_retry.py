"""
Retry the missing gate reviews: OpenAI (fix max_tokens param) + Cerebras (after rate-limit cooldown).
Appends to the same raw review file from the first run.
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
RAW_PATH = REVIEWS_DIR / 'full_paper_gate_review_20260422_173703.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
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


def review_openai_fixed(paper, api_key):
    url = 'https://api.openai.com/v1/chat/completions'
    for model_id in ['gpt-5.4', 'gpt-5', 'gpt-5-turbo', 'o1']:
        payload = json.dumps({
            'model': model_id,
            'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}],
            'temperature': 0.2,
            'max_completion_tokens': 6000
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0'
        })
        try:
            with urllib.request.urlopen(req, timeout=420) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [OpenAI {model_id}] done ({len(text)} chars)')
                return {f'OpenAI {model_id}': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:500]
            except Exception: pass
            print(f'  [OpenAI {model_id}] ERROR: {e.code}: {body}')
            # If the error is about temperature, retry without it
            if 'temperature' in body.lower():
                payload2 = json.dumps({
                    'model': model_id,
                    'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper)}],
                    'max_completion_tokens': 6000
                }).encode('utf-8')
                req2 = urllib.request.Request(url, data=payload2, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                    'User-Agent': 'python-requests/2.31.0'
                })
                try:
                    with urllib.request.urlopen(req2, timeout=420) as resp:
                        data = json.loads(resp.read())
                        text = data['choices'][0]['message']['content']
                        print(f'  [OpenAI {model_id} (no-temp retry)] done ({len(text)} chars)')
                        return {f'OpenAI {model_id}': text}
                except Exception as e2:
                    body2 = ''
                    if isinstance(e2, urllib.error.HTTPError):
                        try: body2 = e2.read().decode()[:500]
                        except Exception: pass
                    print(f'  [OpenAI {model_id} (no-temp retry)] ERROR: {e2} | {body2}')
        except Exception as e:
            print(f'  [OpenAI {model_id}] ERROR: {e}')
    return {'OpenAI GPT-5': 'ERROR: all model IDs failed'}


def review_cerebras(paper, api_key):
    url = 'https://api.cerebras.ai/v1/chat/completions'
    # Try smaller payload truncation to stay under TPM limit this attempt
    paper_trunc = paper
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.2,
        'max_tokens': 6000
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=420) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:500]
            except Exception: pass
            if e.code == 429 and attempt < 3:
                wait = 60
                print(f'  [Cerebras] rate limited, waiting {wait}s... (attempt {attempt+1}/4)')
                time.sleep(wait)
            else:
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}
    return {'Cerebras Qwen3 235B': 'ERROR: all retries rate-limited'}


def append_to_raw(new_reviews):
    if not RAW_PATH.exists():
        print(f'Raw file missing: {RAW_PATH}')
        return
    existing = RAW_PATH.read_text(encoding='utf-8')
    additions = ['\n\n---\n\n# RETRY PASS\n']
    for model, review in new_reviews.items():
        additions.append(f'\n---\n\n## {model}\n\n{review}\n')
    RAW_PATH.write_text(existing + '\n'.join(additions), encoding='utf-8')
    print(f'Appended {len(new_reviews)} reviews to {RAW_PATH}')


def main():
    openai_key = get_win_env('OPENAI_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')

    paper = load_paper()
    print(f'Paper: {len(paper)} chars\n')

    new_reviews = {}
    if openai_key:
        print('Retrying OpenAI with max_completion_tokens...')
        new_reviews.update(review_openai_fixed(paper, openai_key))

    if cerebras_key:
        print('Retrying Cerebras Qwen3 235B after cooldown...')
        new_reviews.update(review_cerebras(paper, cerebras_key))

    append_to_raw(new_reviews)


if __name__ == '__main__':
    main()
