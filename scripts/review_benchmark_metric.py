"""
6-provider review: is per-question-improvement rate a good candidate
benchmark metric for AI personalization studies?
"""

import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'docs' / 'reviews'

PROMPT = """You are advising the author of a behavioral-prediction AI research paper on whether a specific metric should be proposed as a benchmark for AI personalization work.

## The metric

**Per-question improvement rate over a no-context baseline (5-judge primary mean per question).**

For each question in a behavioral-prediction battery, compute the 5-judge primary mean score under the no-context baseline (C5) and under the tested condition (e.g., C2a = a Behavioral Specification served as context). Count how many questions improve, tie, and worsen. Report as a percentage.

## The data this produces on the current study

Low-baseline subjects (9 subjects, 351 questions):

| Condition vs. C5 baseline | Improvement rate | Worsening rate |
|---|---:|---:|
| Spec only (~7K tokens) | 70.9% | 15.1% |
| Facts only (~10K tokens) | 72.9% | 14.5% |
| Raw corpus (25K-420K words) | 78.3% | 12.8% |
| Facts + spec | 78.6% | 15.1% |

All 14 subjects (546 questions): 58.8% for spec, 65.8% for facts+spec.

Head-to-head at question level: raw corpus beats spec on 54.1% of questions, spec beats corpus on 32.8%, ties 13.1%.

## The author's proposal

Propose this metric — "per-question improvement rate over a no-context baseline, reported on a behavioral-prediction battery" — as a candidate benchmark axis for AI personalization research. The idea is that "X% of questions improved" is:

- easier to replicate across judge panels and rubrics than mean-score deltas
- comparable across studies without requiring matched scales
- directly interpretable (readers know what "70% improvement rate" means)
- robust to judge noise (each question is either improved or not, averaged)
- generalizable to other context representations, response models, or study populations

## Your task

1. Is per-question-improvement rate a good candidate benchmark metric for AI personalization? What are its strengths and weaknesses?
2. Are there comparable established metrics in LLM evaluation, information retrieval, or decision-support literature that this parallels or contradicts?
3. Should the paper explicitly propose this as a benchmark, or present it as an internal reporting metric only?
4. What's the cleanest formulation to put in §1.2 as a secondary outcome and in §8 Future Work as a benchmark proposal?
5. What could go wrong if other groups adopt this metric? Name failure modes.

Be direct. No diplomacy. If you think this is a bad benchmark metric, say so.
"""


def log(m):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {m}', flush=True)


def load_env():
    for k in ['ANTHROPIC_API_KEY','OPENAI_API_KEY','GEMINI_API_KEY','MISTRAL_API_KEY','CEREBRAS_API_KEY']:
        r = subprocess.run(['powershell','-Command',
                            f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
                           capture_output=True, text=True)
        v = r.stdout.strip()
        if v: os.environ[k] = v


def call_gemini(model, prompt, k):
    r = httpx.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}',
        json={'contents': [{'parts': [{'text': prompt}]}],
              'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 4096}},
        timeout=180)
    r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text']


def call_mistral(prompt, k):
    r = httpx.post('https://api.mistral.ai/v1/chat/completions',
        json={'model': 'mistral-large-latest',
              'messages': [{'role':'user','content':prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_cerebras(prompt, k):
    r = httpx.post('https://api.cerebras.ai/v1/chat/completions',
        json={'model':'qwen-3-235b-a22b-instruct-2507',
              'messages':[{'role':'user','content':prompt}],
              'temperature':0.3,'max_tokens':4096},
        headers={'Authorization': f'Bearer {k}','Content-Type':'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_openai(model, prompt, k):
    r = httpx.post('https://api.openai.com/v1/chat/completions',
        json={'model':model,'messages':[{'role':'user','content':prompt}],
              'temperature':0.3,'max_completion_tokens':4096},
        headers={'Authorization': f'Bearer {k}','Content-Type':'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_anthropic(model, prompt, k):
    r = httpx.post('https://api.anthropic.com/v1/messages',
        json={'model':model,'max_tokens':4096,'temperature':0.3,
              'messages':[{'role':'user','content':prompt}]},
        headers={'x-api-key':k,'anthropic-version':'2023-06-01','content-type':'application/json'},
        timeout=180)
    r.raise_for_status()
    return r.json()['content'][0]['text']


def main():
    load_env()
    keys = {k: os.environ.get(k) for k in
            ['ANTHROPIC_API_KEY','OPENAI_API_KEY','GEMINI_API_KEY','MISTRAL_API_KEY','CEREBRAS_API_KEY']}

    providers = [
        ('Gemini 2.5 Flash', lambda: call_gemini('gemini-2.5-flash', PROMPT, keys['GEMINI_API_KEY'])),
        ('Gemini 2.5 Pro', lambda: call_gemini('gemini-2.5-pro', PROMPT, keys['GEMINI_API_KEY'])),
        ('Mistral Large', lambda: call_mistral(PROMPT, keys['MISTRAL_API_KEY'])),
        ('Cerebras Qwen3 235B', lambda: call_cerebras(PROMPT, keys['CEREBRAS_API_KEY'])),
        ('GPT-5.4', lambda: call_openai('gpt-5.4', PROMPT, keys['OPENAI_API_KEY'])),
        ('Claude Opus 4.6', lambda: call_anthropic('claude-opus-4-6', PROMPT, keys['ANTHROPIC_API_KEY'])),
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
    out = OUT / f's114_benchmark_metric_review_{ts}.md'
    lines = [f'# Benchmark Metric Review — 6-provider panel', f'_Generated: {ts}_', '']
    for label, text in reviews.items():
        lines.append(f'\n---\n\n## {label}\n\n{text}')
    out.write_text('\n'.join(lines), encoding='utf-8')
    log(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
