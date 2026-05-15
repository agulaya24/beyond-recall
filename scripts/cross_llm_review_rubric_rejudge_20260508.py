"""
Cross-LLM review panel — rubric rejudge robustness check
=========================================================

Sends the rubric-rejudge briefing to 5 frontier LLM reviewers (Mistral Large,
Cerebras Qwen3 235B, Groq Llama 3.3 70B, Gemini 2.5 Pro, GPT-5.5 / OpenAI),
collects per-reviewer responses, saves each to a per-provider markdown file
under docs/research/.

This is a one-shot reproducibility script for the cross-LLM review of the
rubric-rejudge finding (2026-05-08). It is designed to fail soft on any single
provider (per-task constraint: 1-2 failures OK, proceed with the rest).

Usage:
    python scripts/cross_llm_review_rubric_rejudge_20260508.py

Outputs:
    docs/research/cross_llm_review_rubric_rejudge_20260508_<provider>.md  (one per reviewer)

Cost:
    ~$0.05-0.20 total (briefing is ~5k input tokens; replies cap at 4k output tokens)
"""

import datetime
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BRIEFING_PATH = REPO_ROOT / 'docs' / 'reviews' / '_rubric_rejudge_briefing_20260508.md'
OUTPUT_DIR = REPO_ROOT / 'docs' / 'research'
OUTPUT_DIR.mkdir(exist_ok=True)


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_briefing() -> str:
    return BRIEFING_PATH.read_text(encoding='utf-8').strip()


SYSTEM_INSTRUCTION = (
    "You are a rigorous, independent peer reviewer. The paper team is asking for "
    "genuinely independent assessment, not validation. Be direct about both strengths "
    "and weaknesses. Where you cannot judge from the data provided, say so explicitly."
)


def review_mistral(briefing: str, api_key: str) -> str:
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [
            {'role': 'system', 'content': SYSTEM_INSTRUCTION},
            {'role': 'user', 'content': briefing},
        ],
        'temperature': 0.3,
        'max_tokens': 4096,
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0',
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        return data['choices'][0]['message']['content']


def review_cerebras(briefing: str, api_key: str) -> str:
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [
            {'role': 'system', 'content': SYSTEM_INSTRUCTION},
            {'role': 'user', 'content': briefing},
        ],
        'temperature': 0.3,
        'max_tokens': 4096,
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0',
    })
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                return data['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < 2:
                time.sleep(30)
                continue
            raise
    raise RuntimeError(f'Cerebras failed after retries: {last_err}')


def review_groq(briefing: str, api_key: str) -> str:
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [
            {'role': 'system', 'content': SYSTEM_INSTRUCTION},
            {'role': 'user', 'content': briefing},
        ],
        'temperature': 0.3,
        'max_tokens': 4096,
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0',
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        return data['choices'][0]['message']['content']


def review_gemini(briefing: str, api_key: str, model_id: str = 'gemini-2.5-pro') -> str:
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    payload = json.dumps({
        'systemInstruction': {'parts': [{'text': SYSTEM_INSTRUCTION}]},
        'contents': [{'parts': [{'text': briefing}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192},
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.31.0',
    })
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read())
        # Gemini sometimes returns no parts if blocked / truncated; surface that.
        candidates = data.get('candidates', [])
        if not candidates:
            raise RuntimeError(f'Gemini returned no candidates: {data}')
        cand = candidates[0]
        parts = cand.get('content', {}).get('parts', [])
        if not parts:
            raise RuntimeError(f'Gemini returned candidate with no parts (finishReason={cand.get("finishReason")}): {data}')
        return parts[0]['text']


def review_openai(briefing: str, api_key: str) -> str:
    """Try GPT-5.5 family. Fall back through likely model IDs.

    The OpenAI public model family at the time of writing includes gpt-5,
    gpt-5-pro, gpt-4.1, etc. The paper team's prior runs reference GPT-5.5
    via cross-LLM review; we try a sequence of plausible IDs and use the
    first that succeeds.
    """
    candidate_models = ['gpt-5.5', 'gpt-5-pro', 'gpt-5', 'gpt-4.1']
    url = 'https://api.openai.com/v1/chat/completions'
    last_err = None
    for model_id in candidate_models:
        payload = json.dumps({
            'model': model_id,
            'messages': [
                {'role': 'system', 'content': SYSTEM_INSTRUCTION},
                {'role': 'user', 'content': briefing},
            ],
            'temperature': 0.3,
            'max_tokens': 4096,
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0',
        })
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                return f'[model={model_id}]\n\n{text}'
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='replace')[:500] if hasattr(e, 'read') else ''
            last_err = f'{model_id}: HTTP {e.code} {err_body}'
            # 404/400 typically = bad model id; try next
            if e.code in (400, 404):
                continue
            # Some accounts return 400 on unsupported temperature; retry with default
            if 'temperature' in err_body.lower():
                payload2 = json.dumps({
                    'model': model_id,
                    'messages': [
                        {'role': 'system', 'content': SYSTEM_INSTRUCTION},
                        {'role': 'user', 'content': briefing},
                    ],
                    'max_tokens': 4096,
                }).encode('utf-8')
                req2 = urllib.request.Request(url, data=payload2, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}',
                    'User-Agent': 'python-requests/2.31.0',
                })
                try:
                    with urllib.request.urlopen(req2, timeout=180) as resp:
                        data = json.loads(resp.read())
                        text = data['choices'][0]['message']['content']
                        return f'[model={model_id}, temp=default]\n\n{text}'
                except Exception as e2:
                    last_err = f'{model_id} (temp=default): {e2}'
                    continue
            raise
        except Exception as e:
            last_err = f'{model_id}: {e}'
            continue
    raise RuntimeError(f'All OpenAI candidate models failed. Last: {last_err}')


def save_review(provider_slug: str, provider_label: str, model_id: str, review_text: str, status: str = 'OK', error: str = '') -> Path:
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out_path = OUTPUT_DIR / f'cross_llm_review_rubric_rejudge_20260508_{provider_slug}.md'
    header = (
        f'# Cross-LLM review — {provider_label}\n\n'
        f'**Model:** `{model_id}`  \n'
        f'**Generated:** {ts}  \n'
        f'**Status:** {status}  \n'
        f'**Briefing:** `docs/reviews/_rubric_rejudge_briefing_20260508.md`  \n'
        f'**Script:** `scripts/cross_llm_review_rubric_rejudge_20260508.py`  \n'
    )
    if error:
        header += f'**Error:** `{error}`  \n'
    body = '\n---\n\n' + (review_text if status == 'OK' else f'_No review obtained. See error above._')
    out_path.write_text(header + body + '\n', encoding='utf-8')
    return out_path


def main():
    print('Loading API keys from Windows User env...')
    keys = {
        'mistral': get_win_env('MISTRAL_API_KEY'),
        'cerebras': get_win_env('CEREBRAS_API_KEY'),
        'groq': get_win_env('GROQ_API_KEY'),
        'gemini': get_win_env('GEMINI_API_KEY'),
        'openai': get_win_env('OPENAI_API_KEY'),
    }
    for name, val in keys.items():
        print(f'  {name}: {"YES" if val else "MISSING"}')

    print(f'\nLoading briefing from {BRIEFING_PATH} ...')
    briefing = load_briefing()
    print(f'  briefing chars: {len(briefing)}, est tokens: {len(briefing)//4}')

    panel = [
        ('mistral_large', 'Mistral Large', 'mistral-large-latest', keys['mistral'], review_mistral),
        ('cerebras_qwen3_235b', 'Cerebras Qwen3 235B', 'qwen-3-235b-a22b-instruct-2507', keys['cerebras'], review_cerebras),
        ('groq_llama_3_3_70b', 'Groq Llama 3.3 70B', 'llama-3.3-70b-versatile', keys['groq'], review_groq),
        ('gemini_2_5_pro', 'Gemini 2.5 Pro', 'gemini-2.5-pro', keys['gemini'], review_gemini),
        ('openai_gpt5', 'OpenAI GPT-5 family', 'gpt-5.5 (with fallback)', keys['openai'], review_openai),
    ]

    summary = []
    for slug, label, model_id, api_key, fn in panel:
        print(f'\n[{label}] sending...')
        if not api_key:
            print('  SKIP: missing API key')
            save_review(slug, label, model_id, '', status='SKIPPED', error='missing API key')
            summary.append((label, 'SKIPPED'))
            continue
        try:
            text = fn(briefing, api_key)
            print(f'  OK ({len(text)} chars)')
            out = save_review(slug, label, model_id, text, status='OK')
            print(f'  saved {out}')
            summary.append((label, 'OK'))
        except Exception as e:
            err_msg = repr(e)[:300]
            # Gemini Pro fallback to Flash if Pro 503s
            if slug == 'gemini_2_5_pro':
                print(f'  Gemini Pro failed: {err_msg}')
                try:
                    print('  Falling back to gemini-2.5-flash...')
                    text = review_gemini(briefing, api_key, model_id='gemini-2.5-flash')
                    print(f'  OK ({len(text)} chars)')
                    save_review('gemini_2_5_flash', 'Gemini 2.5 Flash (fallback)', 'gemini-2.5-flash', text, status='OK_FALLBACK')
                    save_review(slug, label, model_id, '', status='FAILED_FELL_BACK', error=err_msg)
                    summary.append((label, 'FAILED_FELL_BACK_TO_FLASH'))
                    continue
                except Exception as e2:
                    err_msg = f'{err_msg} | flash fallback: {repr(e2)[:200]}'
            print(f'  FAIL: {err_msg}')
            save_review(slug, label, model_id, '', status='FAILED', error=err_msg)
            summary.append((label, 'FAILED'))

    print('\n=== panel summary ===')
    for label, status in summary:
        print(f'  {label}: {status}')


if __name__ == '__main__':
    main()
