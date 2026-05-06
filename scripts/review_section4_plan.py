"""
Beyond Recall — §4 Structure Planning Review

Collects cross-LLM feedback on the paper as written through §3 locked content
and recommendations for §4 Results structure. Emphasis: layman comprehension.

Run: python review_section4_plan.py
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v8_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)


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


REVIEW_PROMPT = """You are reviewing a research paper draft for arXiv submission. The paper is "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization." Only sections 1 through 3 (Introduction through Study Design) are locked. Section 4 (Results) has not been written yet.

Your job has two parts.

## Part 1 — Review the locked content (§1 through §3)

Read the full locked draft below and flag any issues with the framing, methodology, claims, or clarity that will undermine §4 if not addressed first. Be specific: cite section and claim. Use this structure:

### Critical issues in §1-§3
### Clarity / layman-comprehension issues
### Terminology issues
### Framing consistency issues

The author has emphasized that the paper must be understandable to a layperson without sacrificing rigor. It is acceptable for the paper to be longer if clarity requires it.

## Part 2 — Recommend a structure for §4 Results

Given what the paper has established in §1-§3, propose an organization for §4. The prior draft version had eight subsections (gradient, compression, memory systems, Base Layer, hedging, wrong-spec, scaling, Tier 2). You are not required to endorse that structure. Consider:

- What should the §4 narrative spine be?
- What is the ideal first subsection (what opens §4)?
- What load-bearing tables and figures should anchor §4?
- Where should the statistical tests live?
- Where should known-figure reference (Franklin) land?
- How should wrong-spec control results, circularity controls, and hedging sub-findings be placed?
- How should the reader move from primary result to secondary results to robustness?
- Is there an ordering that maximizes layman comprehension without sacrificing rigor?

Give a concrete proposed outline for §4, section by section, with a one-sentence purpose for each.

Be direct. If the prior eight-part structure is wrong, say so. If it is right, say so and explain why.

---

PAPER (§1 through §3 locked):

{paper}
"""


def review_gemini(paper, api_key):
    import urllib.request
    results = {}
    for model_id, label in [
        ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
        ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': REVIEW_PROMPT.format(paper=paper)}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['candidates'][0]['content']['parts'][0]['text']
                results[label] = text
                print(f'  [{label}] done ({len(text)} chars)')
        except Exception as e:
            results[label] = f'ERROR: {e}'
            print(f'  [{label}] ERROR: {e}')
    return results


def review_mistral(paper, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Mistral Large] done ({len(text)} chars)')
            return {'Mistral Large': text}
    except Exception as e:
        print(f'  [Mistral] ERROR: {e}')
        return {'Mistral Large': f'ERROR: {e}'}


def review_cerebras(paper, api_key):
    import urllib.request, urllib.error, time
    paper_trunc = paper[:40000] + ('\n\n[NOTE: paper truncated for API limit; please answer Part 2 based on §1-§2 content as representative, and flag this in your response.]' if len(paper) > 40000 else '')
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                print(f'  [Cerebras] ERROR: {e.code}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_groq(paper, api_key):
    import urllib.request
    paper_trunc = paper[:35000] + ('\n\n[NOTE: paper truncated for API limit; please base Part 2 recommendations on what you can see plus reasonable inference, and flag missing coverage.]' if len(paper) > 35000 else '')
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Groq Llama 3.3 70B] done ({len(text)} chars)')
            return {'Groq Llama 3.3 70B': text}
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B': f'ERROR: {e}'}


def save_results(all_reviews):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f's114_section4_planning_{ts}.md'
    lines = [f'# §4 Structure Planning Review', f'_Generated: {ts}_',
             f'_Paper source: docs/beyond_recall_v8_draft.md (§1-§3 locked)_\n']
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    groq_key = get_win_env('GROQ_API_KEY')

    if not any([gemini_key, mistral_key, cerebras_key, groq_key]):
        print('No API keys found.')
        sys.exit(1)

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    all_reviews = {}

    if gemini_key:
        print('Sending to Gemini (Flash + Pro)...')
        all_reviews.update(review_gemini(paper, gemini_key))

    if mistral_key:
        print('Sending to Mistral Large...')
        all_reviews.update(review_mistral(paper, mistral_key))

    if cerebras_key:
        print('Sending to Cerebras Qwen3 235B...')
        all_reviews.update(review_cerebras(paper, cerebras_key))

    if groq_key:
        print('Sending to Groq Llama 3.3 70B...')
        all_reviews.update(review_groq(paper, groq_key))

    out_path = save_results(all_reviews)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
