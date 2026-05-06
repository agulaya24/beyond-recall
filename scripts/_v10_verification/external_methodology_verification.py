"""
External LLM verification for v10 §4.6.1 methodology fix + v11 architecture.

Tries OpenAI (GPT-5.5 / latest GPT-5.x) first, falls back to Gemini 2.5 Pro,
then Mistral Large. Saves the response to docs/reviews/ with the model used and
the exact prompt at the top of the file.

Run: python scripts/_v10_verification/external_methodology_verification.py
"""

import datetime
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v10_tier2_methodology_external_verification_20260425.md'


def get_win_env(key: str) -> str:
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


PROMPT = """You are an experienced empirical-ML methodology reviewer. The author of an in-progress paper has caught a numerical discrepancy in their §4.6.1 Tier 2 cross-provider replication results. They asked me (Claude Code) to recommend a fix. I am asking you to evaluate whether my recommendation is methodologically sound.

## Situation

The paper's §4.6.1 currently reports Δ_spec values for 6 (subject × response_model) cells testing whether the specification effect reproduces with non-Anthropic response models reading non-Anthropic-generated batteries. The published Δ values are: Ebers × Sonnet +1.48, Ebers × Gemini Pro +1.07, Yung Wing × Sonnet +1.91, Yung Wing × Gemini Pro +1.27, Zitkala-Sa × Sonnet +1.40, Zitkala-Sa × Gemini Pro -0.55.

A mechanical recompute from the raw judgment files (results/_tier2/global_<subject>/tier2_<response_model>_judgments_<judge>.json) using the canonical 5-judge primary aggregation rule (per-judge per-question score → per-judge per-subject mean → panel mean across the five non-Gemini judges Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) gives different numbers regardless of which Δ definition is used:

- Δ_C2a (internal, T2 C2a − T2 C5, 5-judge primary): +0.95 / +0.24 / +1.06 / +0.17 / +0.89 / -0.10
- Δ_C4a (internal, T2 C4a − T2 C5, 5-judge primary): +0.77 / +0.16 / +1.34 / +0.43 / +1.04 / -0.03
- Δ_C4a (T2 C4a − main-study Haiku C5, closest match): +1.45 / +1.61 / +1.00 / +0.91 / +0.31 / +0.10

Mean absolute error from published across all 8 tested definitions ranges 0.598-0.755. Sign matches are 5/6 or 6/6 across every definition. The 5 of 6 directional reproduction is invariant; the magnitudes are not reproducible.

## My recommendation

OPTION C: demote §4.6.1's table to direction-only. Drop the 6 magnitudes. Keep the check/cross direction-match column. Add a footnote pointing at the recompute scaffold and flagging the magnitude discrepancy as a v11 resolution item. The directional claim ("5 of 6 cells reproduce the specification direction across non-Anthropic models") is what the section's argument needs; the magnitudes are doing rhetorical not analytical work.

I considered:
- Option A (replace with delta_C4a internal recompute): requires picking a Delta definition without primary-data confirmation
- Option B (replace with delta_C2a internal recompute): same concern
- Option D (keep magnitudes with footnote disclaiming reproducibility): preserves a number we cannot defend
- Option E (defer to post-arXiv): leaves the inconsistency in the published draft

## My v11 architectural commitment

Going forward, every number in the paper should be produced by a named idempotent scaffold script that reads primary data only. Verification becomes "does the scaffold run correctly," not "is this individual number right." The pattern already exists for the §4.1 sensitivity blocks (`_v10_battery_sensitivity.py`, `_v10_coupling_sensitivity.py`, `_v10_pipeline_variance.py`); v11 extends it to all §4 numbers via a single `_v11_paper_numbers.py` that emits JSON, with the markdown rendered from the JSON via templating.

## What I want you to evaluate

1. Is Option C the right immediate v10 fix given that primary data does not reproduce the published magnitudes via any tested Delta definition? If not, what should it be?
2. Is the directional claim ("5 of 6 cells reproduce direction") a defensible substitute for the published magnitudes given that sign-matches are invariant across all 8 Delta definitions?
3. Is the v11 scaffold architecture the right structural fix for a paper whose central contribution depends on numerical reproducibility?
4. Is there a methodological move I am missing that would let the paper keep magnitudes while remaining honest? (e.g., committing to delta_C2a internal as the canonical Delta, or running a fresh Tier 2 with the locked aggregation)

Be direct. If my recommendation is wrong, say so. If it is right, name the strongest dissent another reviewer might raise so I can prepare for it.

Under 800 words.
"""


def call_openai(api_key: str):
    """Try latest GPT-5.x candidates in priority order."""
    url = 'https://api.openai.com/v1/chat/completions'
    candidates = [
        'gpt-5.5',
        'gpt-5.5-preview',
        'gpt-5.4',
        'gpt-5.3',
        'gpt-5.2',
        'gpt-5.1',
        'gpt-5',
    ]
    last_err = None
    for model in candidates:
        # GPT-5.x rejects max_tokens; uses max_completion_tokens. Try the new
        # name first, fall back to old name if a model rejects it.
        body_new = {
            'model': model,
            'messages': [{'role': 'user', 'content': PROMPT}],
            'max_completion_tokens': 2400,
        }
        # Some GPT-5 models also reject non-default temperature; omit it.
        payload = json.dumps(body_new).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'User-Agent': 'python-requests/2.31.0',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                actual_model = data.get('model', model)
                print(f'  [OpenAI {actual_model}] done ({len(text)} chars)')
                return actual_model, text
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')[:300]
            last_err = f'{model}: HTTP {e.code} — {body}'
            print(f'  [OpenAI {model}] {last_err[:200]}')
            # keep trying lower candidates
            continue
        except Exception as e:
            last_err = f'{model}: {e}'
            print(f'  [OpenAI {model}] error: {e}')
            continue
    raise RuntimeError(f'All OpenAI candidates failed. Last: {last_err}')


def call_gemini(api_key: str):
    model_id = 'gemini-2.5-pro'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': PROMPT}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 4096},
    }).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        text = data['candidates'][0]['content']['parts'][0]['text']
        print(f'  [Gemini 2.5 Pro] done ({len(text)} chars)')
        return 'gemini-2.5-pro', text


def call_mistral(api_key: str):
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': PROMPT}],
        'temperature': 0.3,
        'max_tokens': 2400,
    }).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0',
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        text = data['choices'][0]['message']['content']
        print(f'  [Mistral Large] done ({len(text)} chars)')
        return 'mistral-large-latest', text


def main():
    print('Loading API keys from Windows env...')
    openai_key = get_win_env('OPENAI_API_KEY')
    gemini_key = get_win_env('GEMINI_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    model_used = None
    response = None
    fallback_log = []

    # 1. Try OpenAI
    if openai_key:
        try:
            print('Trying OpenAI (GPT-5.x candidates in order)...')
            model_used, response = call_openai(openai_key)
        except Exception as e:
            fallback_log.append(f'OpenAI failed: {e}')
            print(f'OpenAI failed completely: {e}')

    # 2. Fallback Gemini
    if response is None and gemini_key:
        try:
            print('Falling back to Gemini 2.5 Pro...')
            model_used, response = call_gemini(gemini_key)
        except Exception as e:
            fallback_log.append(f'Gemini failed: {e}')
            print(f'Gemini failed: {e}')

    # 3. Fallback Mistral
    if response is None and mistral_key:
        try:
            print('Falling back to Mistral Large...')
            model_used, response = call_mistral(mistral_key)
        except Exception as e:
            fallback_log.append(f'Mistral failed: {e}')
            print(f'Mistral failed: {e}')

    if response is None:
        print('ALL providers failed:')
        for line in fallback_log:
            print(f'  - {line}')
        sys.exit(1)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = []
    header.append('# v10 §4.6.1 Methodology — External Verification')
    header.append('')
    header.append(f'**Date:** 2026-04-25  ')
    header.append(f'**Generated at:** {ts}  ')
    header.append(f'**Model used:** `{model_used}`  ')
    header.append(f'**Provider chain:** OpenAI -> Gemini 2.5 Pro -> Mistral Large')
    if fallback_log:
        header.append('')
        header.append('**Fallback log:**')
        for line in fallback_log:
            header.append(f'- {line}')
    header.append('')
    header.append('---')
    header.append('')
    header.append('## Exact prompt sent')
    header.append('')
    header.append('```')
    header.append(PROMPT.rstrip())
    header.append('```')
    header.append('')
    header.append('---')
    header.append('')
    header.append('## Reviewer model response')
    header.append('')
    header.append(response.strip())
    header.append('')

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text('\n'.join(header), encoding='utf-8')
    print(f'\nSaved: {OUT_PATH}')
    print(f'Model used: {model_used}')


if __name__ == '__main__':
    main()
