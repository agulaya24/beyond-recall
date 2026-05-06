"""
v11.8 §5.8 closing argument review by GPT-5.4 (OpenAI) and Claude Opus 4.7
(Anthropic). Sends the entire §1 Introduction and §5 Discussion as context with
a focused review prompt on the closing argument.

Output: docs/reviews/v11_8_closing_5_4_opus_<ts>.md
"""
import os
import sys
import json
import time
import subprocess
import datetime
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_8_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)


def get_win_env(key: str) -> str:
    r = subprocess.run(
        ['powershell', '-Command',
         f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_sections():
    text = PAPER_PATH.read_text(encoding='utf-8')
    lines = text.splitlines()
    s1 = '\n'.join(lines[10:149]).strip()
    s5 = '\n'.join(lines[1504:1600]).strip()
    return s1, s5


REVIEW_PROMPT = """You are reviewing the closing argument of a research paper for arXiv submission.

The paper is "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization." Section 1 (Introduction) and Section 5 (Discussion) are below. Section 5.8 (the last subsection of Section 5) is the closing argument.

The author has gone through several drafts of §5.8 and is asking for guidance on whether the current draft works as the paper's closing statement. Specific concerns:
1. The close should not "announce" or be elitist — let the results speak.
2. The close should be about MEMORY (recall vs interpretation), not personalization.
3. The close should not duplicate §1.4 ("What this implies") which already laid out the structural options.
4. Vision-document echoes ("Loading facts into context is not knowing someone") and a "What is settled / What is not" frame are present in the current draft.
5. The close partitions findings (settled) from open questions (open) and points to §7 for safety/deployment implications.

Read §1 INTRODUCTION and §5 DISCUSSION below, and provide structured feedback in this format:

## CLOSING — DOES IT WORK?
Direct evaluation of whether the current §5.8 closes the paper effectively. Address:
- Does it land the central claim of the paper without re-litigating §1.4?
- Does it avoid announcing/posturing language?
- Does it earn its conclusions or assert them?
- Does it bookend §1.1 and §1.4 cleanly?

## SPECIFIC LANGUAGE FIXES
Cite the offending text and propose alternatives. Be precise.

## STRUCTURAL ISSUES
Anything in the close that risks being read as advocacy, manifesto, or off-topic.

## WHAT THE CLOSE IS MISSING
Anything important from §5.1-§5.7 that the close doesn't carry.

## VERDICT
One paragraph: ready to lock, or what to change before locking.

Be direct. The author wants critical guidance. Do not be diplomatic.

---

§1 INTRODUCTION:

{s1}

---

§5 DISCUSSION:

{s5}
"""


def call_openai(api_key: str, model_id: str, prompt: str,
                max_tokens: int = 6144, timeout: int = 600):
    url = 'https://api.openai.com/v1/chat/completions'
    body = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': max_tokens,
    }
    if model_id.startswith('gpt-4'):
        body['temperature'] = 0.3
        body.pop('max_completion_tokens')
        body['max_tokens'] = max_tokens
    payload = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            return text, data.get('model')
    except urllib.error.HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode()[:500]
        except Exception:
            pass
        return None, f'HTTP {e.code}: {body_text}'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def call_anthropic(api_key: str, model_id: str, prompt: str,
                   max_tokens: int = 6144, timeout: int = 600):
    url = 'https://api.anthropic.com/v1/messages'
    body = {
        'model': model_id,
        'max_tokens': max_tokens,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    payload = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.31.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data['content'][0]['text']
            return text, data.get('model')
    except urllib.error.HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode()[:500]
        except Exception:
            pass
        return None, f'HTTP {e.code}: {body_text}'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def main():
    print('Loading API keys...')
    openai_key = get_win_env('OPENAI_API_KEY')
    anthropic_key = get_win_env('ANTHROPIC_API_KEY')
    if not openai_key:
        print('ERROR: OPENAI_API_KEY not found')
        sys.exit(1)
    if not anthropic_key:
        print('ERROR: ANTHROPIC_API_KEY not found')
        sys.exit(1)

    print('Loading sections...')
    s1, s5 = load_sections()
    print(f'  §1: {len(s1)} chars (~{len(s1)//4} tokens)')
    print(f'  §5: {len(s5)} chars (~{len(s5)//4} tokens)')
    prompt = REVIEW_PROMPT.format(s1=s1, s5=s5)
    print(f'  prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)\n')

    results = {}

    # GPT-5.4 (with fallbacks)
    print('Calling OpenAI GPT-5.4...')
    for model_id in ['gpt-5.4', 'gpt-5', 'gpt-4o']:
        print(f'  trying {model_id}...')
        t0 = time.time()
        text, label = call_openai(openai_key, model_id, prompt)
        elapsed = time.time() - t0
        if text:
            wc = len(text.split())
            print(f'  SUCCESS in {elapsed:.1f}s ({wc} words) [{label}]')
            results[f'OpenAI {label or model_id}'] = text
            break
        else:
            print(f'  FAIL ({elapsed:.1f}s): {label}')
            time.sleep(5)
    else:
        results['OpenAI (all models failed)'] = f'ERROR: all OpenAI candidates failed'

    # Claude Opus 4.7
    print('\nCalling Anthropic Opus 4.7...')
    t0 = time.time()
    text, label = call_anthropic(anthropic_key, 'claude-opus-4-7', prompt)
    elapsed = time.time() - t0
    if text:
        wc = len(text.split())
        print(f'  SUCCESS in {elapsed:.1f}s ({wc} words) [{label}]')
        results[f'Anthropic {label or "claude-opus-4-7"}'] = text
    else:
        print(f'  FAIL ({elapsed:.1f}s): {label}')
        results['Anthropic claude-opus-4-7'] = f'ERROR: {label}'

    # Save
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'v11_8_closing_5_4_opus_{ts}.md'
    lines = [
        f'# v11.8 §5.8 Closing Argument Review — GPT-5.4 + Opus 4.7',
        f'_Generated: {ts}_',
        f'_§1: {len(s1)} chars; §5: {len(s5)} chars_\n'
    ]
    for model, review in results.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')


if __name__ == '__main__':
    main()
