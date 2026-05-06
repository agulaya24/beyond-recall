"""
Final collective read of v8's locked content (§1 + §2 + §3 + §4.1 + §4.2).
Ask for any remaining issues before proceeding to §4.3+.
"""

import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
import httpx

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / 'docs' / 'reviews'
DRAFT = REPO / 'docs' / 'beyond_recall_v8_draft.md'


def read_locked_content():
    """Extract just §1 + §2 + §3 + §4.1 + §4.2 from v8 (through §4.2.1)."""
    text = DRAFT.read_text(encoding='utf-8')
    # Find '### 4.3' or *Next: §4.3* marker to cut off
    end_markers = ['### 4.3', '## 5.', '*Next: §4.3*']
    end = len(text)
    for m in end_markers:
        idx = text.find(m)
        if idx > 0:
            end = min(end, idx)
    return text[:end]


PROMPT_TEMPLATE = """You are doing a final consistency + quality check on the locked content of a research paper before the author moves on to the next section. The locked content below covers §1 Introduction, §2 Related Work, §3 Study Design, §4.1 The Cross-Subject Gradient, and §4.2 Compression.

Your task is NOT to rewrite or restructure. Flag only:

1. **Cross-section inconsistencies.** Numbers that don't match across sections. Hypotheses referenced but not defined. Claims that appear in two places with different framings.
2. **Remaining overclaims.** Anywhere the paper promises more than the evidence supports.
3. **Voice violations.** Em-dashes in prose (not in tables / code blocks), GTM-style verbs (beats / crushes / dominates), reader-addressing in methodology sections.
4. **Unfulfilled promises.** Forward references to sections that won't deliver what's promised.
5. **One last check:** is there a claim anywhere that will embarrass the author under peer review?

Be direct. Be short. If you see nothing worth fixing, say so — do not invent issues to seem thorough.

---

LOCKED CONTENT:

{content}
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
        timeout=240)
    r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text']


def call_mistral(prompt, k):
    r = httpx.post('https://api.mistral.ai/v1/chat/completions',
        json={'model': 'mistral-large-latest',
              'messages': [{'role':'user','content':prompt}],
              'temperature': 0.3, 'max_tokens': 4096},
        headers={'Authorization': f'Bearer {k}', 'Content-Type': 'application/json'},
        timeout=240)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_openai(model, prompt, k):
    r = httpx.post('https://api.openai.com/v1/chat/completions',
        json={'model':model,'messages':[{'role':'user','content':prompt}],
              'temperature':0.3,'max_completion_tokens':4096},
        headers={'Authorization': f'Bearer {k}','Content-Type':'application/json'},
        timeout=240)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


def call_anthropic(model, prompt, k):
    r = httpx.post('https://api.anthropic.com/v1/messages',
        json={'model':model,'max_tokens':4096,'temperature':0.3,
              'messages':[{'role':'user','content':prompt}]},
        headers={'x-api-key':k,'anthropic-version':'2023-06-01','content-type':'application/json'},
        timeout=240)
    r.raise_for_status()
    return r.json()['content'][0]['text']


def main():
    load_env()
    keys = {k: os.environ.get(k) for k in
            ['ANTHROPIC_API_KEY','OPENAI_API_KEY','GEMINI_API_KEY','MISTRAL_API_KEY']}

    content = read_locked_content()
    prompt = PROMPT_TEMPLATE.format(content=content)
    log(f'Prompt size: {len(prompt)} chars')

    providers = [
        ('Gemini 2.5 Pro', lambda: call_gemini('gemini-2.5-pro', prompt, keys['GEMINI_API_KEY'])),
        ('Mistral Large', lambda: call_mistral(prompt, keys['MISTRAL_API_KEY'])),
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
    out = OUT / f's114_final_locked_content_review_{ts}.md'
    lines = [f'# Final Locked-Content Review — 4-provider panel', f'_Generated: {ts}_',
             f'_Locked content: §1 + §2 + §3 + §4.1 + §4.2 ({len(content)} chars)_', '']
    for label, text in reviews.items():
        lines.append(f'\n---\n\n## {label}\n\n{text}')
    out.write_text('\n'.join(lines), encoding='utf-8')
    log(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
