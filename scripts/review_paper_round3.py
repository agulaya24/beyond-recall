"""
Beyond Recall - Round 3 Cross-LLM Paper Review Script
Reviews the v6 draft (with new Letta scaling n=3 findings, per-system
strengths/weaknesses section, and framing corrections) against free-tier providers.
Usage: python review_paper_round3.py
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

This is Round 3 of recursive review. The authors have already addressed Round 1 and Round 2 critiques. Round 3 has SUBSTANTIAL NEW CONTENT that prior reviewers never saw. Focus your critique on the new material.

WHAT IS NEW SINCE ROUND 2 (you are seeing this for the first time):

A) Section 4.3.1 - Letta stateful-agent scaling finding, now n=3 (Hamerton + Ebers + Babur), spanning a 9x corpus-size range. Key findings: Letta's `human` memory block saturates at ~333,000 characters with ~25% verbatim sentence duplication by the time it hits the API ceiling, and Letta's prediction uplift collapses ~60% from small corpus (+1.99) to large corpus (+0.75). Base Layer's compose step stays 34-40K chars across the same 9x range (corpus-invariant).

B) Section 4.3.2 - NEW per-system strengths/weaknesses read on Mem0, Letta, Supermemory, Zep, Base Layer. First head-to-head benchmark on a non-recall criterion. Reviewers should ask: is this balanced or biased?

C) Section 4.1.1 - Reframing. The "9-of-9 low-baseline" finding has been demoted from headline to sensitivity analysis (pre-registered analysis plan dropped threshold framing). The new headline is the continuous slope: -0.98 [-1.30, -0.74], Wilcoxon p=0.006.

D) Numerical corrections throughout: Table 4.2 Hamerton compression numbers; Section 4.1.2 parse-failure attribution (GPT-5.4 ~19% not Gemini Pro ~40%); Section 4.5 wrong-spec v2 (2.30 not 2.21); Section 4.6 Hamerton C4a (3.22 not 3.28); Section 3.7 Krippendorff alpha (0.535 / 0.659 not 0.723).

E) Section 4.3 retrieval disagreement - re-verified against actual data (93/83/74/53 percent controlled; 100 percent native).

Please read the full paper below, then provide structured feedback. Use these sections EXACTLY:

## FOCUS-AREA ASSESSMENT
Answer each of the following DIRECTLY with evidence from the text:

1. Does Section 4.3.1's Letta scaling finding (335K char ceiling, 25% duplication, 60% uplift collapse from small to large corpora) LAND HONESTLY? Is it framed as a constructive architectural observation, or does it read as a "we win over Letta" hit piece? Quote the flagship sentences and judge them.

2. Does Section 4.3.2's per-system strengths/weaknesses section feel BALANCED across Mem0 / Letta / Supermemory / Zep / Base Layer, or biased toward any system (especially Base Layer)? Call out any asymmetry in the tone or depth of critique per system.

3. Does Section 4.1.1 now correctly LEAD WITH THE CONTINUOUS SLOPE (-0.98, Wilcoxon p=0.006) rather than the 9/9 threshold finding? Is the sensitivity-analysis framing clear enough that a reader will not be confused about which is the headline and which is the robustness check?

4. Any REMAINING OVERCLAIM? Check specifically:
   (a) The flagship sentence in Section 4.3 and the Abstract - does "outperforms" language still appear where it should have been softened?
   (b) Any residual "Base Layer beats memory providers" framing vs. the more honest "different axes" framing?
   (c) Is the Letta uplift-collapse finding (60% drop) presented with honesty about n=3 sample size?

5. Is there anything NEW about Letta scaling that should be ELEVATED to the abstract or introduction but currently sits buried in Section 4.3.1? The scaling result (architectural ceiling + verbatim duplication) is arguably the paper's most novel empirical contribution on the memory-provider axis - does the current draft give it appropriate prominence?

## CRITICAL ISSUES
Issues that would cause rejection or significantly undermine the claims. Be specific - cite section and claim.

## MISSING
Important content, analysis, or discussion that is absent and should be present.

## NEEDS EXPANSION
Areas that are present but underdeveloped given the claims being made.

## METHODOLOGY CONCERNS
Any issues with experimental design, statistical analysis, or evaluation validity - especially around the n=3 Letta scaling test.

## MINOR ISSUES
Small fixes: clarity, framing, wording, flow.

## VERDICT
One sentence: overall assessment and readiness for arXiv submission.

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
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'})
        try:
            with urllib.request.urlopen(req, timeout=240) as resp:
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
    # Groq free tier has HTTP payload limit -- truncate paper to 25k chars
    # and prepend the NEW CONTENT summary so it still reviews the right thing.
    head_marker = '## 4.3.1'
    focus_start = paper.find(head_marker)
    if focus_start < 0:
        focus_start = paper.find('4.3.1')
    if focus_start < 0:
        focus_start = 0
    # Take an early 12k + the focus region (4.3-4.6 band) of ~13k
    early = paper[:12000]
    focus = paper[focus_start:focus_start + 13000] if focus_start > 0 else ''
    paper_trunc = early + '\n\n[...middle sections truncated for API limit...]\n\n' + focus
    if len(paper_trunc) > 25000:
        paper_trunc = paper_trunc[:25000]
    paper_trunc += '\n\n[Paper truncated for API payload limit. Focus your review on the sections visible (abstract/intro + Sections 4.3-4.6 where the new material lives).]'

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
            return {'Groq Llama 3.3 70B (focused subset)': text}
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B (focused subset)': f'ERROR: {e}'}


def review_cerebras(paper, api_key):
    import urllib.request, urllib.error, time
    paper_trunc = paper[:40000] + ('\n\n[Paper truncated - first 40k chars. Full paper is longer; focus review on what you see.]' if len(paper) > 40000 else '')
    url = 'https://api.cerebras.ai/v1/chat/completions'
    # Try qwen3 first (larger context), fall back to llama 3.3
    for model_id, label in [
        ('qwen-3-235b-a22b-instruct-2507', 'Cerebras Qwen3 235B'),
        ('llama-3.3-70b', 'Cerebras Llama 3.3 70B'),
    ]:
        payload = json.dumps({
            'model': model_id,
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
                with urllib.request.urlopen(req, timeout=240) as resp:
                    data = json.loads(resp.read())
                    text = data['choices'][0]['message']['content']
                    print(f'  [{label}] done ({len(text)} chars)')
                    return {label: text}
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    print(f'  [{label}] rate limited, waiting 30s...')
                    time.sleep(30)
                else:
                    body = ''
                    try: body = e.read().decode()[:200]
                    except Exception: pass
                    print(f'  [{label}] ERROR: {e.code}: {body}')
                    break
            except Exception as e:
                print(f'  [{label}] ERROR: {e}')
                break
    return {'Cerebras': 'ERROR: all models failed'}


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
        with urllib.request.urlopen(req, timeout=300) as resp:
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
        'Prompt focus areas (Round 3 - new content since Round 2):',
        '1. Does Section 4.3.1 Letta scaling (n=3, 335K ceiling, 25% duplication, 60% uplift collapse) land honestly?',
        '2. Does Section 4.3.2 per-system strengths/weaknesses feel balanced?',
        '3. Does Section 4.1.1 now lead with continuous slope (-0.98) rather than 9/9?',
        '4. Any remaining overclaim (flagship sentence, outperforms language, n=3 honesty)?',
        '5. Should the Letta scaling result be elevated to abstract/intro?',
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    round_num = 3

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

    if mistral_key:
        print('Sending to Mistral...')
        all_reviews.update(review_mistral(paper, mistral_key))
    else:
        print('Skipping Mistral - no key')

    if cerebras_key:
        print('Sending to Cerebras...')
        all_reviews.update(review_cerebras(paper, cerebras_key))
    else:
        print('Skipping Cerebras - no key')

    if groq_key:
        print('Sending to Groq...')
        all_reviews.update(review_groq(paper, groq_key))
    else:
        print('Skipping Groq - no key')

    out_path = save_results(all_reviews, round_num)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
