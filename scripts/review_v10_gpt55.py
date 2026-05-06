"""
Beyond Recall v10 — GPT-5.5 Review
Sends the v10 paper to OpenAI's latest GPT-5.x model with structured review prompt.
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
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v10_1_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
OUT_PATH = REVIEWS_DIR / 'v10_review_gpt55_20260424.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
    import re
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


REVIEW_PROMPT = """You are an experienced reviewer for a top empirical ML / HCI venue. Read the full Beyond Recall v10 paper below. Produce a structured review.

This paper has been through extensive revision based on 4 prior cross-LLM reviews. Notable v10 changes from v9:
- Author N=1 pilot removed entirely (now relies on 9-of-9 low-baseline subjects + structural extrapolation for the deployment claim)
- Alignment-framing sections (sec 1.5, 5.7) removed for circular reasoning; safety content moved to sec 7.6 future work
- Sec 4.1 added a battery-composition sensitivity block (multiple regression + subset regression). Headline slope = -0.96 [-1.24, -0.67]; under multiple regression controlling for LITERAL_RECALL fraction, partial coefficient on baseline = -0.88 [-1.13, -0.63]; under subset regression dropping Hamerton, slope = -0.89 [-1.18, -0.61]
- Sec 4.5 Letta demoted to exploratory N=3 case study with naming-asymmetry caveat
- LLM-class circularity caveat hoisted to sec 1.3
- Twin-2K demoted to related work only
- Sec 5.5 deployment claims scoped to what was tested

Your review:

## Verdict
One of: CRITICAL_FIXES_REQUIRED / NEEDS_REVISION / READY_WITH_MINOR_FIXES / READY_FOR_ARXIV. One-sentence justification.

## Highest-impact single improvement
What is the ONE thing the author should do next to maximize this paper's impact? Be specific.

## Critical issues (must fix before submission)
Cite section, current claim, suggested fix.

## Needs revision (overclaim, buried caveat, missing read-through)
Cite section, suggest fix.

## What the v10 revisions got right
Specifically: did removing the author pilot, folding the alignment framing, adding the battery sensitivity block, demoting Letta to exploratory, and pruning Twin-2K close the issues prior reviewers flagged? Or did some get over-corrected?

## Missing content
Experiments, citations, or analyses that would substantially strengthen.

## Comparison to the field
Place this against PersonaGym, Twin-2K, LongMemEval, LoCoMo. Where does Beyond Recall stand? What is its distinct contribution?

## Style and presentation
Section flow, redundancy, footnote use, figure captions.

## What I would push back on
If you would push the paper back at peer review, what specifically would you ask for?

Be direct. If you would accept as-is, say so. If you would reject, say so.

PAPER BEGINS:

{paper}
"""


def call_openai(api_key, model_id, prompt, max_tokens=8192, timeout=600):
    """Call OpenAI Chat Completions. Returns (text, error_or_None, response_meta)."""
    url = 'https://api.openai.com/v1/chat/completions'
    body = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': max_tokens,
    }
    # GPT-5.x and o-series models only accept default temperature=1
    # GPT-4o accepts custom temperature
    if model_id.startswith('gpt-4'):
        body['temperature'] = 0.3
        body.pop('max_completion_tokens')
        body['max_tokens'] = max_tokens

    payload = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            usage = data.get('usage', {})
            return text, None, {'model': data.get('model'), 'usage': usage}
    except urllib.error.HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode()[:500]
        except Exception:
            pass
        return None, f'HTTP {e.code}: {body_text}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


def main():
    print('Loading API key...')
    api_key = get_win_env('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: OPENAI_API_KEY not found in user env')
        sys.exit(1)
    print(f'API key loaded ({len(api_key)} chars)')

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens')

    prompt = REVIEW_PROMPT.format(paper=paper)
    print(f'Full prompt: {len(prompt)} chars, ~{len(prompt)//4} tokens')

    # Try models in order
    candidates = ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']
    chosen_model = None
    text = None
    meta = None
    last_error = None

    for model_id in candidates:
        print(f'\nTrying model: {model_id}')
        for attempt in range(2):
            t0 = time.time()
            text, err, meta = call_openai(api_key, model_id, prompt, max_tokens=8192, timeout=600)
            elapsed = time.time() - t0
            if text:
                print(f'  SUCCESS in {elapsed:.1f}s ({len(text)} chars)')
                # Quality gate: must be >= 1000 words
                wc = len(text.split())
                print(f'  Word count: {wc}')
                if wc < 1000:
                    print(f'  WARNING: response only {wc} words, retrying once...')
                    if attempt == 0:
                        time.sleep(5)
                        continue
                    else:
                        print(f'  Still under 1000 words after retry. Will try next model.')
                        text = None
                        last_error = f'short_response_{wc}_words'
                        break
                chosen_model = meta.get('model') or model_id
                break
            else:
                print(f'  FAIL ({elapsed:.1f}s): {err}')
                last_error = err
                if attempt == 0:
                    print('  retrying in 10s...')
                    time.sleep(10)
        if text:
            break

    if not text:
        print(f'\nALL MODELS FAILED. Last error: {last_error}')
        OUT_PATH.write_text(
            f'# v10 Review — FAILED\n\nAll candidate models failed.\nLast error: {last_error}\n',
            encoding='utf-8'
        )
        sys.exit(1)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = (
        f'# Beyond Recall v10 — GPT-5.x Review\n\n'
        f'**Generated:** {ts}\n'
        f'**Model requested chain:** {candidates}\n'
        f'**Model actually used (API response):** `{chosen_model}`\n'
        f'**Paper file:** `docs/beyond_recall_v10_1_draft.md` ({len(paper):,} chars)\n'
        f'**Usage:** {json.dumps(meta.get("usage", {}))}\n'
        f'**Response length:** {len(text)} chars, {len(text.split())} words\n\n'
        f'---\n\n'
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(header + text, encoding='utf-8')
    print(f'\nSaved review: {OUT_PATH}')
    print(f'Model used: {chosen_model}')
    print(f'Words: {len(text.split())}')


if __name__ == '__main__':
    main()
