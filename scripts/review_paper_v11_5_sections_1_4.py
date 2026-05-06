"""
Beyond Recall v11.5 §1-4 Cross-LLM Peer Review
================================================
Sends the locked §1-§4 of the v11.5 paper to four frontier reviewers along
with the v11 confidence catalog as supporting context. Saves a single
review file with one section per reviewer plus a synthesis paragraph.

Reviewers
---------
1. Mistral Large       (env MISTRAL_API_KEY)
2. GPT-5.5             (env OPENAI_API_KEY) — model id: gpt-5.5
3. Gemini 2.5 Pro      (env GEMINI_API_KEY)
4. Claude Opus 4.7     (env ANTHROPIC_API_KEY) — model id: claude-opus-4-7

Cerebras Qwen3 235B is intentionally excluded — §1-4 input exceeds its
context window.

Constraints
-----------
- Each call has a 5-minute (300s) hard timeout. On failure the script
  logs and moves on; no retry loops.
- Strips HTML comments from the paper before sending.
- Stops at the end of §4.7 (line 1495) — does NOT include §5+.

Output
------
- docs/reviews/round_v11_5_sections_1_4_<timestamp>.md
"""

import os
import sys
import json
import re
import subprocess
import datetime
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_5_draft.md'
CATALOG_PATH = REPO_ROOT / 'docs' / 'research' / 'v11_confidence_catalog_20260428.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

# §5 begins at line 1497. We keep everything up to and including line 1495
# (the closing '---' before §5). Use 1495 as the inclusive cutoff.
SECTIONS_1_4_END_LINE = 1495

CALL_TIMEOUT_SECONDS = 300


def get_win_env(key):
    """Read a User env var via PowerShell — needed because Python's os.environ
    on Windows does not always pick up newly-set User-scope variables in this
    shell session."""
    val = os.environ.get(key)
    if val:
        return val
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
            capture_output=True, text=True, timeout=15
        )
        return r.stdout.strip()
    except Exception:
        return ''


def load_paper_sections_1_4():
    """Load lines 1..SECTIONS_1_4_END_LINE, strip HTML comments."""
    raw = PAPER_PATH.read_text(encoding='utf-8')
    lines = raw.splitlines()
    truncated = '\n'.join(lines[:SECTIONS_1_4_END_LINE])
    # Strip HTML comments (internal review notes)
    cleaned = re.sub(r'<!--.*?-->', '', truncated, flags=re.DOTALL)
    return cleaned.strip()


def load_confidence_catalog():
    text = CATALOG_PATH.read_text(encoding='utf-8')
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL).strip()


REVIEW_PROMPT = """You are reviewing the first four sections of a research paper for arXiv submission. Be a rigorous, honest peer reviewer.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

A confidence catalog (source of truth for which claims the authors consider HIGH, MEDIUM, LOW, or UNRESOLVED) is provided below the paper text. Your critique should weight against the claimed confidence level for each item: a HIGH claim that is weakly supported is a critical issue; a LOW claim that is weakly supported is appropriate.

Read the full text below, then provide structured feedback in exactly this format:

## CRITICAL ISSUES
Issues that would cause rejection or significantly undermine the claims. Be specific - cite section and claim.

## MISSING
Important content, analysis, or discussion that is absent from sections 1-4 and should be present.

## NEEDS EXPANSION
Areas that are present but underdeveloped given the claims being made.

## METHODOLOGY CONCERNS
Any issues with experimental design, statistical analysis, or evaluation validity.

## OVERSTATED
Claims that go beyond what the data supports per the confidence catalog.

## UNDERSTATED
Findings that the data supports but sections 1-4 underplay.

## MINOR ISSUES
Small fixes: clarity, framing, wording, flow.

## VERDICT
One paragraph: overall assessment, readiness, and the single most important fix.

Be direct. Do not be diplomatic. If something is wrong, say so clearly. If a section is strong, say that too.

---

PAPER SECTIONS 1-4:

{paper_text}

---

CONFIDENCE CATALOG:

{confidence_catalog}
"""


def _http_post_json(url, payload, headers, timeout):
    """Single helper for blocking JSON POST with timeout."""
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-urllib/3',
        **headers,
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_mistral(prompt_text, api_key):
    label = 'Mistral Large'
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = {
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt_text}],
        'temperature': 0.3,
        'max_tokens': 8192,
    }
    headers = {'Authorization': f'Bearer {api_key}'}
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, headers, timeout=CALL_TIMEOUT_SECONDS)
        text = data['choices'][0]['message']['content']
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:300]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_openai(prompt_text, api_key):
    """GPT-5.5 via OpenAI Responses API. Model id: gpt-5.5."""
    label = 'GPT-5.5'
    # Try Responses API first (preferred for GPT-5 family); fall back to chat.completions.
    url_responses = 'https://api.openai.com/v1/responses'
    payload_responses = {
        'model': 'gpt-5.5',
        'input': prompt_text,
        'max_output_tokens': 8192,
    }
    headers = {'Authorization': f'Bearer {api_key}'}
    t0 = time.time()
    try:
        data = _http_post_json(url_responses, payload_responses, headers, timeout=CALL_TIMEOUT_SECONDS)
        # Responses API: output is list of items; concatenate text from output_text or content blocks
        text_parts = []
        if 'output_text' in data and isinstance(data['output_text'], str):
            text_parts.append(data['output_text'])
        else:
            for item in data.get('output', []):
                for c in item.get('content', []):
                    if c.get('type') in ('output_text', 'text'):
                        text_parts.append(c.get('text', ''))
        text = '\n'.join(p for p in text_parts if p).strip()
        if not text:
            text = json.dumps(data)[:2000]
        elapsed = time.time() - t0
        print(f'  [{label}] ok via Responses API ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        print(f'  [{label}] Responses API failed ({e.code}): {body[:200]}; trying chat.completions')
    except Exception as e:
        print(f'  [{label}] Responses API failed: {type(e).__name__}: {e}; trying chat.completions')

    # Fallback: chat.completions
    url_chat = 'https://api.openai.com/v1/chat/completions'
    payload_chat = {
        'model': 'gpt-5.5',
        'messages': [{'role': 'user', 'content': prompt_text}],
        'max_completion_tokens': 8192,
    }
    t0 = time.time()
    try:
        data = _http_post_json(url_chat, payload_chat, headers, timeout=CALL_TIMEOUT_SECONDS)
        text = data['choices'][0]['message']['content']
        elapsed = time.time() - t0
        print(f'  [{label}] ok via chat.completions ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_gemini(prompt_text, api_key):
    label = 'Gemini 2.5 Pro'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}'
    payload = {
        'contents': [{'parts': [{'text': prompt_text}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192},
    }
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, {}, timeout=CALL_TIMEOUT_SECONDS)
        candidates = data.get('candidates', [])
        if not candidates:
            msg = f'ERROR: no candidates returned. Response: {json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        parts = candidates[0].get('content', {}).get('parts', [])
        text = '\n'.join(p.get('text', '') for p in parts).strip()
        if not text:
            # Sometimes truncation or safety: surface the finishReason
            fr = candidates[0].get('finishReason', 'UNKNOWN')
            msg = f'ERROR: empty text (finishReason={fr}). Raw: {json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_anthropic(prompt_text, api_key):
    label = 'Claude Opus 4.7'
    url = 'https://api.anthropic.com/v1/messages'
    payload = {
        'model': 'claude-opus-4-7',
        'max_tokens': 8192,
        'messages': [{'role': 'user', 'content': prompt_text}],
    }
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
    }
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, headers, timeout=CALL_TIMEOUT_SECONDS)
        blocks = data.get('content', [])
        text = '\n'.join(b.get('text', '') for b in blocks if b.get('type') == 'text').strip()
        if not text:
            msg = f'ERROR: empty text. stop_reason={data.get("stop_reason")} raw={json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def main():
    print('Loading inputs...')
    paper_text = load_paper_sections_1_4()
    catalog_text = load_confidence_catalog()
    print(f'  paper sections 1-4: {len(paper_text)} chars (~{len(paper_text)//4} tokens)')
    print(f'  confidence catalog: {len(catalog_text)} chars (~{len(catalog_text)//4} tokens)')

    prompt_text = REVIEW_PROMPT.format(paper_text=paper_text, confidence_catalog=catalog_text)
    print(f'  combined prompt:    {len(prompt_text)} chars (~{len(prompt_text)//4} tokens)')

    print('\nLoading API keys...')
    keys = {
        'MISTRAL_API_KEY':    get_win_env('MISTRAL_API_KEY'),
        'OPENAI_API_KEY':     get_win_env('OPENAI_API_KEY'),
        'GEMINI_API_KEY':     get_win_env('GEMINI_API_KEY'),
        'ANTHROPIC_API_KEY':  get_win_env('ANTHROPIC_API_KEY'),
    }
    for k, v in keys.items():
        print(f'  {k}: {"SET (len="+str(len(v))+")" if v else "MISSING"}')

    reviews = {}

    if keys['MISTRAL_API_KEY']:
        print('\nMistral Large...')
        label, text = review_mistral(prompt_text, keys['MISTRAL_API_KEY'])
        reviews[label] = text
    else:
        reviews['Mistral Large'] = 'SKIPPED: MISTRAL_API_KEY not set'

    if keys['OPENAI_API_KEY']:
        print('\nGPT-5.5...')
        label, text = review_openai(prompt_text, keys['OPENAI_API_KEY'])
        reviews[label] = text
    else:
        reviews['GPT-5.5'] = 'SKIPPED: OPENAI_API_KEY not set'

    if keys['GEMINI_API_KEY']:
        print('\nGemini 2.5 Pro...')
        label, text = review_gemini(prompt_text, keys['GEMINI_API_KEY'])
        reviews[label] = text
    else:
        reviews['Gemini 2.5 Pro'] = 'SKIPPED: GEMINI_API_KEY not set'

    if keys['ANTHROPIC_API_KEY']:
        print('\nClaude Opus 4.7...')
        label, text = review_anthropic(prompt_text, keys['ANTHROPIC_API_KEY'])
        reviews[label] = text
    else:
        reviews['Claude Opus 4.7'] = 'SKIPPED: ANTHROPIC_API_KEY not set'

    # Save
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'round_v11_5_sections_1_4_{ts}.md'
    succeeded = [k for k, v in reviews.items() if not (v.startswith('ERROR') or v.startswith('SKIPPED'))]
    failed = [k for k, v in reviews.items() if (v.startswith('ERROR') or v.startswith('SKIPPED'))]

    lines = [
        '# Beyond Recall v11.5 — §1-4 Cross-LLM Peer Review',
        f'_Generated: {ts}_',
        f'_Reviewers: {len(reviews)} attempted, {len(succeeded)} succeeded, {len(failed)} failed/skipped_',
        '',
        '**Inputs:**',
        f'- Paper §1-4 ({len(paper_text)} chars / ~{len(paper_text)//4} tokens) from `docs/beyond_recall_v11_5_draft.md` (lines 1-{SECTIONS_1_4_END_LINE}, HTML comments stripped)',
        f'- Confidence catalog ({len(catalog_text)} chars) from `docs/research/v11_confidence_catalog_20260428.md`',
        '',
        f'**Succeeded:** {", ".join(succeeded) if succeeded else "(none)"}',
        f'**Failed/Skipped:** {", ".join(failed) if failed else "(none)"}',
    ]
    for model in ['Mistral Large', 'GPT-5.5', 'Gemini 2.5 Pro', 'Claude Opus 4.7']:
        lines.append('\n---\n')
        lines.append(f'## {model}\n')
        lines.append(reviews.get(model, 'NOT RUN'))

    lines.append('\n---\n')
    lines.append('## Synthesis\n')
    lines.append('_Synthesis paragraph appended after manual or auto-merge step. The orchestrator process writes a placeholder here; see post-run synthesis below._\n')

    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved review file: {out_path}')
    print(f'Succeeded: {len(succeeded)} / {len(reviews)}')
    return out_path


if __name__ == '__main__':
    main()
