"""
Title-only review across 6 providers.

Candidates:
  T1. Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization (current)
  T2. Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
  T3. Beyond Recall: Representing How a Person Reasons for AI Personalization
  T4. Beyond Recall: Measuring Representational Accuracy for AI Personalization
  T5. Beyond Recall: An Interpretive Layer for AI Personalization
  T6. Beyond Recall: The Interpretive Layer AI Personalization Is Missing

Panel: Gemini Flash, Gemini Pro, Mistral Large, Cerebras Qwen3 235B, GPT-5.4, Claude Opus 4.6.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / 'docs' / 'reviews'

PAPER_CONTEXT = """\
This paper is being submitted to arXiv. Brief context:

## What the paper demonstrates
- A short document ("Behavioral Specification") that describes how a specific person reasons.
- Served as context to a response model, it improves held-out behavioral prediction.
- On 14 historical subjects, regression slope on (effect vs. baseline) = −0.96, R² = 0.82, p < 0.001.
- 12 of 14 subjects improve; on the 9 low-baseline subjects (the slice that approximates real living users), 9 of 9 improve with mean gain +0.89 on a 1-5 scale, and 55% of individual responses cross an integer rubric anchor.
- Wrong-spec control: random-derangement specifications score near baseline, confirming content specificity.
- Additive to existing commercial memory systems (Mem0 +0.15, Letta +0.25, Zep +0.22) when the spec is layered on retrieval.

## What the paper does NOT prove
- It doesn't show that no other approach could deliver the same benefit.
- It doesn't demonstrate that this specific specification format is the only fundamental building block needed for AI personalization.
- Sample is 14 public-domain historical figures, not living users.

## Framing tension
The current title uses "Missing Primitive," which makes a strong field-level claim: that this is a fundamental building block AI personalization is missing. Two outside reviewers flagged this as stronger than the paper's empirical demonstration supports. Candidates below adjust the framing.

## The candidates

- **T1.** Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization *(current)*
- **T2.** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization
- **T3.** Beyond Recall: Representing How a Person Reasons for AI Personalization
- **T4.** Beyond Recall: Measuring Representational Accuracy for AI Personalization
- **T5.** Beyond Recall: An Interpretive Layer for AI Personalization
- **T6.** Beyond Recall: The Interpretive Layer AI Personalization Is Missing

## Your task
For each of T1 through T6:
1. Give a one-sentence read of what the title claims and whether the paper supports it.
2. Rate it 1-5 on each of: clarity, defensibility, memorability, appropriateness for arXiv.

Then: name your top pick and your second pick, with a short justification. If you think an alternative title (not in T1-T6) would be stronger, propose it.

Be direct. No diplomacy.
"""


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY',
              'MISTRAL_API_KEY', 'CEREBRAS_API_KEY']:
        r = subprocess.run(
            ['powershell', '-Command',
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


def call_gemini(model, prompt, api_key):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    r = httpx.post(
        url,
        json={'contents': [{'parts': [{'text': prompt}]}],
              'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 4096}},
        timeout=180,
    )
    r.raise_for_status()
    data = r.json()
    return data['candidates'][0]['content']['parts'][0]['text']


def call_mistral(prompt, api_key):
    r = httpx.post(
        'https://api.mistral.ai/v1/chat/completions',
        json={'model': 'mistral-large-latest',
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {api_key}',
                 'Content-Type': 'application/json'},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_cerebras(prompt, api_key):
    r = httpx.post(
        'https://api.cerebras.ai/v1/chat/completions',
        json={'model': 'qwen-3-235b-a22b-instruct-2507',
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {api_key}',
                 'Content-Type': 'application/json'},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_openai(model, prompt, api_key):
    r = httpx.post(
        'https://api.openai.com/v1/chat/completions',
        json={'model': model,
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3,
              'max_completion_tokens': 4096},
        headers={'Authorization': f'Bearer {api_key}',
                 'Content-Type': 'application/json'},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_anthropic(model, prompt, api_key):
    r = httpx.post(
        'https://api.anthropic.com/v1/messages',
        json={'model': model,
              'max_tokens': 4096,
              'temperature': 0.3,
              'messages': [{'role': 'user', 'content': prompt}]},
        headers={'x-api-key': api_key,
                 'anthropic-version': '2023-06-01',
                 'content-type': 'application/json'},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()['content'][0]['text']


def main():
    load_env()
    keys = {k: os.environ.get(k) for k in
            ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY',
             'MISTRAL_API_KEY', 'CEREBRAS_API_KEY']}

    reviews = {}
    prompt = PAPER_CONTEXT

    providers = [
        ('Gemini 2.5 Flash',       lambda: call_gemini('gemini-2.5-flash', prompt, keys['GEMINI_API_KEY'])),
        ('Gemini 2.5 Pro',         lambda: call_gemini('gemini-2.5-pro',   prompt, keys['GEMINI_API_KEY'])),
        ('Mistral Large',          lambda: call_mistral(prompt,            keys['MISTRAL_API_KEY'])),
        ('Cerebras Qwen3 235B',    lambda: call_cerebras(prompt,           keys['CEREBRAS_API_KEY'])),
        ('GPT-5.4',                lambda: call_openai('gpt-5.4', prompt,  keys['OPENAI_API_KEY'])),
        ('Claude Opus 4.6',        lambda: call_anthropic('claude-opus-4-6', prompt, keys['ANTHROPIC_API_KEY'])),
    ]

    for label, fn in providers:
        log(f'Querying {label}...')
        try:
            resp = fn()
            reviews[label] = resp
            log(f'  [{label}] done ({len(resp)} chars)')
        except Exception as e:
            reviews[label] = f'ERROR: {e}'
            log(f'  [{label}] ERROR: {e}')

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = OUT_DIR / f's114_title_panel_{ts}.md'
    lines = [f'# Title Panel Review — 6 providers', f'_Generated: {ts}_',
             '\nCandidates:\n',
             '- **T1.** Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization *(current)*',
             '- **T2.** Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization',
             '- **T3.** Beyond Recall: Representing How a Person Reasons for AI Personalization',
             '- **T4.** Beyond Recall: Measuring Representational Accuracy for AI Personalization',
             '- **T5.** Beyond Recall: An Interpretive Layer for AI Personalization',
             '- **T6.** Beyond Recall: The Interpretive Layer AI Personalization Is Missing',
             '']
    for label, text in reviews.items():
        lines.append(f'\n---\n\n## {label}\n\n{text}')
    out.write_text('\n'.join(lines), encoding='utf-8')
    log(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
