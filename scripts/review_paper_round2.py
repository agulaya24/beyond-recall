"""
Beyond Recall - Round 2 Cross-LLM Paper Review Script
Reviews the v6 draft against all free-tier providers with a focus-area prompt.
Usage: python review_paper_round2.py
"""

import os
import sys
import json
import subprocess
import datetime
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v6_draft.md'
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
    # Strip HTML comments (internal editorial checklist, review notes)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


REVIEW_PROMPT = """You are reviewing a research paper for arXiv submission. Be a rigorous, honest peer reviewer. Do not be diplomatic. If something is wrong, say so clearly.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

This is Round 2 of recursive review. The authors have already addressed Round 1 critiques and made substantial revisions. You are now looking for issues a sharp reviewer would raise against the CURRENT revised version.

Please read the full paper below, then provide structured feedback. Use these sections EXACTLY:

## FOCUS-AREA ASSESSMENT
Answer each of the following DIRECTLY with evidence from the text:

1. Section 4.4 now positions Base Layer as a behavioral-spec layer with an open-source retrieval floor, NOT as a 5th memory provider competing with Mem0/Letta/Zep/Supermemory. Does this land honestly, or does the section still read as defensive / conflict-of-interest motivated?

2. Section 5.7 ("A First Benchmark on an Axis the Category Wasn't Optimized For") reframes the memory-provider comparison. Does it come across as a fair "referee introducing a new axis" or does it still read as biased against the competing systems?

3. The Abstract disaggregates three kinds of claims (what was tested / what is extrapolated / what is NOT claimed). Is this disaggregation clear and useful, or muddled?

4. Section 4.3.1 reports a Letta stateful-agent matched-response-model parity test (Haiku + Letta memory = 3.24 vs Haiku + Base Layer full-stack = 3.04, Letta at 65% context size). Is this n=1 result handled with appropriate humility, or does the paper overclaim / underclaim from it?

5. Anywhere else in the paper that a sharp reviewer would flag as overclaiming — specifically call it out with section number and quoted claim.

## CRITICAL ISSUES
Issues that would cause rejection or significantly undermine the claims. Be specific — cite section and claim.

## MISSING
Important content, analysis, or discussion that is absent and should be present.

## NEEDS EXPANSION
Areas that are present but underdeveloped given the claims being made.

## METHODOLOGY CONCERNS
Any issues with experimental design, statistical analysis, or evaluation validity.

## MINOR ISSUES
Small fixes: clarity, framing, wording, flow.

## VERDICT
One sentence: overall assessment and readiness for submission.

---

PAPER:

{paper}
"""


def review_gemini(paper, api_key, key_label=''):
    import urllib.request

    results = {}
    for model_id, label in [
        ('gemini-2.5-flash', f'Gemini 2.5 Flash{key_label}'),
        ('gemini-2.5-pro', f'Gemini 2.5 Pro{key_label}'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': REVIEW_PROMPT.format(paper=paper)}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 6144}
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


def review_groq(paper, api_key):
    import urllib.request
    # Groq free tier has HTTP payload limit -- truncate paper to 30k chars (v6 is larger than v5)
    paper_trunc = paper[:30000] + ('\n\n[Paper truncated for API limit - first 30k chars. Full paper is longer; focus review on what you see.]' if len(paper) > 30000 else '')
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


def review_cerebras(paper, api_key):
    import urllib.request, urllib.error, time
    paper_trunc = paper[:40000] + ('\n\n[Paper truncated - first 40k chars. Full paper is longer; focus review on what you see.]' if len(paper) > 40000 else '')
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b',
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
                print(f'  [Cerebras Llama 3.3 70B] done ({len(text)} chars)')
                return {'Cerebras Llama 3.3 70B': text}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                body = ''
                try: body = e.read().decode()[:200]
                except Exception: pass
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {'Cerebras Llama 3.3 70B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Llama 3.3 70B': f'ERROR: {e}'}


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
        with urllib.request.urlopen(req, timeout=240) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [Mistral Large] done ({len(text)} chars)')
            return {'Mistral Large': text}
    except Exception as e:
        print(f'  [Mistral] ERROR: {e}')
        return {'Mistral Large': f'ERROR: {e}'}


def save_results(all_reviews, round_num):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'round_{round_num:02d}_{ts}.md'
    lines = [
        f'# Paper Review - Round {round_num}',
        f'_Generated: {ts}_',
        f'_Paper: {PAPER_PATH.name}_',
        '',
        'Prompt focus areas (Round 2):',
        '1. Does Section 4.4 land honestly, or still read as defensive?',
        '2. Does Section 5.7 come across as fair or still biased?',
        '3. Is the 3-claim disaggregation in the abstract clear and useful?',
        '4. Is the Section 4.3.1 Letta parity result handled with appropriate humility (n=1)?',
        '5. Any overclaiming elsewhere?',
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    round_num = 2

    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    gemini_key_2 = get_win_env('GEMINI_API_KEY_2')
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper path: {PAPER_PATH}')
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    all_reviews = {}

    # Prefer GEMINI_API_KEY_2 if present; fall back to GEMINI_API_KEY
    gk = gemini_key_2 if gemini_key_2 else gemini_key
    if gk:
        print('Sending to Gemini (Flash + Pro)...')
        all_reviews.update(review_gemini(paper, gk))
    else:
        print('Skipping Gemini - no key')

    if groq_key:
        print('Sending to Groq...')
        all_reviews.update(review_groq(paper, groq_key))
    else:
        print('Skipping Groq - no key')

    if cerebras_key:
        print('Sending to Cerebras...')
        all_reviews.update(review_cerebras(paper, cerebras_key))
    else:
        print('Skipping Cerebras - no key')

    if mistral_key:
        print('Sending to Mistral...')
        all_reviews.update(review_mistral(paper, mistral_key))
    else:
        print('Skipping Mistral - no key')

    out_path = save_results(all_reviews, round_num)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
