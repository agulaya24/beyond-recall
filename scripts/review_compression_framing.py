"""
§4.2 compression-framing review across 6 providers. Ask each to help
frame the compression finding as confidently as the data supports
without apologizing.
"""

import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'docs' / 'reviews'

PROMPT = """You are helping the author of a behavioral-prediction research paper frame the "compression" section of the results.

## The data (5-judge primary, all numbers on a 1-5 rubric)

Conditions:
- C5 = no context (baseline)
- C2a = spec only (~7K tokens)
- C4 = all extracted facts (~10K tokens)
- C8 = raw training corpus (25K-420K words of source text)
- C4a = facts + spec
- C9 = raw corpus + spec

| Subject | Source (words) | C5 | C2a spec | C4 facts | C8 corpus | C4a facts+spec | C9 corpus+spec |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hamerton | 25,231 | 1.26 | 2.63 | 2.43 | 2.27 | 2.77 | 3.09 |
| Sunity Devee | 67,379 | 1.03 | 2.27 | 2.46 | 2.55 | 2.41 | 2.46 |
| Ebers | 96,174 | 1.02 | 1.54 | 2.02 | 2.18 | 2.07 | 2.16 |
| Fukuzawa | 139,088 | 1.67 | 2.35 | 2.67 | 2.74 | 2.78 | 2.78 |
| Bernal Diaz | 187,315 | 1.70 | 2.27 | 2.41 | 2.55 | 2.48 | 2.53 |
| Babur | 422,772 | 1.76 | 1.91 | 2.03 | 2.05 | 2.01 | n/a |
| Seacole | 62,467 | 1.77 | 2.48 | 2.63 | 2.83 | 2.59 | 2.73 |
| Keckley | 58,742 | 1.84 | 2.43 | 2.39 | 2.50 | 2.44 | 2.49 |
| Yung Wing | 66,459 | 1.88 | 2.22 | 2.13 | 2.42 | 2.40 | 2.50 |

(These are the 9 low-baseline subjects, the paper's population of relevance. The spec averages ~7K tokens across subjects. The corpus ranges from ~8K tokens — Hamerton's translated output — up to ~100K tokens.)

## The honest framing the author is considering

"A compact specification (~7K tokens) reaches comparable behavioral-prediction performance to the full raw corpus (25K-420K words), at roughly 5% of the context size. Across the 9 low-baseline subjects, spec-alone is within 0.3 points of the raw corpus on most. On Hamerton (the smallest-corpus subject), structure substantially exceeds raw text and corpus+spec reaches the study's highest compression-related score (3.09)."

The headline claim is COMPRESSION EFFICIENCY: matching retrieval-style performance at a fraction of the context.

## Tensions the author is working through

1. On 8 of 9 low-baseline subjects, raw corpus (C8) is slightly higher than spec alone (C2a). "Spec beats raw text" is not supportable.
2. Adding spec on top of raw corpus (C9) substantially helps only Hamerton. On most subjects, C9 ≈ C8 (spec does not add value on top of the full corpus).
3. But all conditions lift the baseline substantially — C8 alone is +1 point or more over C5 for most subjects. The AI gets value from context of any kind.
4. The author sometimes forgets the study's good-news story because he's focused on being rigorous.

## Your task

1. Recommend the framing for this section. Is "compression efficiency" the right headline, or is there a stronger defensible claim hiding in this data?
2. Is the Hamerton-as-dramatic-case vs. others-as-comparable-at-fraction dual presentation the right structural choice, or would you lead differently?
3. Should the author worry that on 8 of 9 subjects raw corpus slightly edges spec alone? Or is this misreading the claim the paper is actually making?
4. What is the ONE sentence the author should keep repeating so they remember the good-news story in this data?
5. Any other advice specific to framing this result confidently without overclaiming.

Be direct. No hedging. No diplomacy.

This is the first public version of this work; readers have not seen prior versions. Do NOT recommend explaining past iterations.
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
    out = OUT / f's114_compression_framing_{ts}.md'
    lines = [f'# §4.2 Compression Framing — 6-provider panel', f'_Generated: {ts}_', '']
    for label, text in reviews.items():
        lines.append(f'\n---\n\n## {label}\n\n{text}')
    out.write_text('\n'.join(lines), encoding='utf-8')
    log(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
