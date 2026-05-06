"""
Send 3 selected response examples to the 6-provider panel and ask each to
analyze what the specification is doing differently. Transparency notes
for the §4.1 callout boxes.
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

EXAMPLES = [
    {
        'label': 'Example A — Baseline to Facts+Spec (1 → 4 anchor crossing)',
        'subject': 'Ebers',
        'question': "How would Ebers characterize the relationship between self-sacrifice and the success of an educational institution?",
        'ground_truth': "A work is established here which must be built by the hand of God! Implicit devotion and self-sacrifice are needed.",
        'low_label': 'Baseline (no context, score 1.20)',
        'low_text': "I don't have specific information about Ebers's characterization of this relationship in my training data. To give you an accurate answer, I would need to know: 1. Which Ebers you're referring to — there are several notable figures with this surname in educational contexts...",
        'high_label': 'Facts + Spec (score 3.60)',
        'high_text': "Based on the behavioral specification and the facts about Ebers's life, he would characterize this relationship as foundational and inseparable, not instrumental, but constitutive. Self-sacrifice is not a means to institutional success; it is the evidence that success is genuine. Ebers witnessed this directly at Keilhau. Froebel, Langethal, and Middendorf did not sacrifice themselves in order to build a successful school.",
    },
    {
        'label': 'Example B — Facts alone to Facts+Spec (directional correction)',
        'subject': 'Bernal Diaz',
        'question': "When the commander is offered physical assistance during a strenuous activity, what behavior would the author expect from him?",
        'ground_truth': "There were 114 steps to the summit, and, as they feared that Cortes would experience the same fatigue in mounting as Motecusuma had, they were going to assist him by taking hold of his arms. Cortes, however, refused.",
        'low_label': 'Facts alone (no spec, score 2.00)',
        'low_text': "Based on the facts provided about Bernal Diaz del Castillo and his observations of Cortes, the author would expect the commander to accept and participate in the assistance while maintaining leadership and setting an example.",
        'high_label': 'Facts + Spec (score 4.80)',
        'high_text': "Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect Cortes to refuse the assistance and perform the labor himself, particularly if it serves a symbolic or morale-signaling purpose.",
    },
    {
        'label': 'Example C — Facts alone to Facts+Spec (inference where facts appear insufficient)',
        'subject': 'Mary Seacole',
        'question': "How does Mary Seacole typically respond when a delirious patient mistakes her for a family member?",
        'ground_truth': "Poor fellow! I could not undeceive him. I think the fancy happily caused by the touch of a woman's hand soothed his dying hour.",
        'low_label': 'Facts alone (no spec, score 2.80)',
        'low_text': "Based on the complete set of facts provided, there is no specific information about how Mary Seacole typically responds when a delirious patient mistakes her for a family member. While the facts document many aspects of Mary Seacole's nursing practice, they do not address this specific scenario.",
        'high_label': 'Facts + Spec (score 5.00)',
        'high_text': "Based on the behavioral specification and known facts, Mary Seacole's response to this situation would follow a consistent pattern. Primary response: compassionate acceptance. She would not correct the patient in the moment.",
    },
]


PROMPT_TEMPLATE = """You are analyzing response pairs from an AI behavioral-prediction study. For each example below, the same question was asked of the same response model (Claude Haiku 4.5) under two different conditions. Your task is to analyze, in plain English, what specifically changed when the Behavioral Specification was added.

For each example, answer concisely:

1. **What was the lower-scoring response doing (and not doing)?**
2. **What specifically does the higher-scoring response add or do differently?**
3. **Is the improvement driven by: (a) hedge reduction, (b) identity disambiguation, (c) directional correction of a prediction, (d) interpretive inference beyond retrieved facts, or (e) something else? Name the mechanism.**
4. **One-sentence summary of what the specification is doing for this question.**

Be direct. No diplomacy.

---

"""


def build_prompt():
    parts = [PROMPT_TEMPLATE]
    for i, ex in enumerate(EXAMPLES, 1):
        parts.append(f"\n## {ex['label']}\n")
        parts.append(f"**Subject:** {ex['subject']}\n")
        parts.append(f"**Question:** {ex['question']}\n")
        parts.append(f"**Ground truth (held-out passage, what the subject actually wrote):** {ex['ground_truth']}\n")
        parts.append(f"\n**{ex['low_label']}:**\n> {ex['low_text']}\n")
        parts.append(f"\n**{ex['high_label']}:**\n> {ex['high_text']}\n")
        parts.append("\n---\n")
    return ''.join(parts)


def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def load_env():
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY',
              'MISTRAL_API_KEY', 'CEREBRAS_API_KEY']:
        r = subprocess.run(['powershell', '-Command',
                            f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
                           capture_output=True, text=True)
        v = r.stdout.strip()
        if v:
            os.environ[k] = v


def call_gemini(model, prompt, k):
    r = httpx.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}',
        json={'contents': [{'parts': [{'text': prompt}]}],
              'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 4096}},
        timeout=180)
    r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text']


def call_mistral(prompt, k):
    r = httpx.post(
        'https://api.mistral.ai/v1/chat/completions',
        json={'model': 'mistral-large-latest',
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_cerebras(prompt, k):
    r = httpx.post(
        'https://api.cerebras.ai/v1/chat/completions',
        json={'model': 'qwen-3-235b-a22b-instruct-2507',
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_openai(model, prompt, k):
    r = httpx.post(
        'https://api.openai.com/v1/chat/completions',
        json={'model': model,
              'messages': [{'role': 'user', 'content': prompt}],
              'temperature': 0.3, 'max_completion_tokens': 4096},
        headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_anthropic(model, prompt, k):
    r = httpx.post(
        'https://api.anthropic.com/v1/messages',
        json={'model': model, 'max_tokens': 4096, 'temperature': 0.3,
              'messages': [{'role': 'user', 'content': prompt}]},
        headers={'x-api-key': k, 'anthropic-version': '2023-06-01',
                 'content-type': 'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['content'][0]['text']


def main():
    load_env()
    prompt = build_prompt()
    keys = {k: os.environ.get(k) for k in
            ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY',
             'MISTRAL_API_KEY', 'CEREBRAS_API_KEY']}

    providers = [
        ('Gemini 2.5 Flash', lambda: call_gemini('gemini-2.5-flash', prompt, keys['GEMINI_API_KEY'])),
        ('Gemini 2.5 Pro', lambda: call_gemini('gemini-2.5-pro', prompt, keys['GEMINI_API_KEY'])),
        ('Mistral Large', lambda: call_mistral(prompt, keys['MISTRAL_API_KEY'])),
        ('Cerebras Qwen3 235B', lambda: call_cerebras(prompt, keys['CEREBRAS_API_KEY'])),
        ('GPT-5.4', lambda: call_openai('gpt-5.4', prompt, keys['OPENAI_API_KEY'])),
        ('Claude Opus 4.6', lambda: call_anthropic('claude-opus-4-6', prompt, keys['ANTHROPIC_API_KEY'])),
    ]

    reviews = {}
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
    out = OUT_DIR / f's114_example_analysis_{ts}.md'
    lines = [f'# Response-Example Analysis — 6-provider panel', f'_Generated: {ts}_',
             '\n## Examples reviewed\n', '- A: Ebers Q7 (baseline → facts+spec, 1.20 → 3.60)',
             '- B: Bernal Diaz Q16 (facts → facts+spec, 2.00 → 4.80, directional correction)',
             '- C: Mary Seacole Q2 (facts → facts+spec, 2.80 → 5.00, interpretive inference)',
             '']
    for label, text in reviews.items():
        lines.append(f'\n---\n\n## {label}\n\n{text}')
    out.write_text('\n'.join(lines), encoding='utf-8')
    log(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
