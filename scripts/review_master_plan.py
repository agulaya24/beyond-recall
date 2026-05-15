"""
Beyond Recall — Cross-LLM Master Plan Review
Sends the launch checklist + master roadmap + GPT's critique to free API providers.
Asks each to adjudicate GPT's points, find what GPT missed, and flag what to cut.
Usage: python review_master_plan.py
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHECKLIST = REPO_ROOT / 'docs' / 'reviews' / 'launch_execution_checklist_20260507.md'
ROADMAP = REPO_ROOT / 'docs' / 'reviews' / 'master_release_roadmap_20260507.md'
GPT_CRITIQUE = REPO_ROOT / 'docs' / 'reviews' / 'master_plan_gpt_critique_20260514.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


REVIEW_PROMPT = """You are a launch strategist reviewing the release plan for a research paper, "Beyond Recall," about to be posted to arXiv. The author is a solo, non-academic researcher with a live open-source product (Base Layer).

SCOPE: The paper content itself is locked and NOT under review. You are reviewing the LAUNCH AND POST-LAUNCH PLAN ONLY — sequencing, outreach, registries, funding tracks, risk controls. Do not give feedback on the paper's findings or sections.

You are given three documents:
1. LAUNCH EXECUTION CHECKLIST — the linear action queue (Phase 0 pre-launch through Phase 3).
2. MASTER RELEASE ROADMAP — the reference doc behind the checklist.
3. GPT'S CRITIQUE — a prior review of this same plan, with 10 numbered points.

Provide structured feedback in exactly this format:

## GPT POINT-BY-POINT
For each of GPT's 10 numbered points: AGREE / DISAGREE / MODIFY, with one to three sentences of reasoning. Be willing to disagree — if GPT is wrong or overcorrecting, say so.

## WHAT GPT MISSED
Problems in the plan that GPT did not flag. Be specific — cite the phase, item, or section.

## WHAT TO CUT
Items in the plan that should be removed entirely, not just reordered. This is the most important section — be aggressive and specific.

## SEQUENCING ERRORS
Anything ordered wrong: dependencies that are not respected, gates that are too soft or too hard, items that block other items.

## VERDICT
Two to three sentences: is this plan ready to execute once the paper is finalized? What is the single highest-leverage change?

Be direct and specific. Cite item names. Do not be diplomatic.

---

# DOCUMENT 1: LAUNCH EXECUTION CHECKLIST

{checklist}

---

# DOCUMENT 2: MASTER RELEASE ROADMAP

{roadmap}

---

# DOCUMENT 3: GPT'S CRITIQUE

{gpt}
"""


def build_prompt():
    checklist = CHECKLIST.read_text(encoding='utf-8')
    roadmap = ROADMAP.read_text(encoding='utf-8')
    gpt = GPT_CRITIQUE.read_text(encoding='utf-8')
    return REVIEW_PROMPT.format(checklist=checklist, roadmap=roadmap, gpt=gpt)


def review_gemini(prompt, api_key):
    import urllib.request
    results = {}
    for model_id, label in [
        ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
        ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt}]}],
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


def review_mistral(prompt, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'max_tokens': 8192
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


def main():
    print('Loading API keys...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    print('Building prompt...')
    prompt = build_prompt()
    print(f'Prompt: {len(prompt)} chars, ~{len(prompt)//4} tokens\n')

    all_reviews = {}

    print('Sending to Gemini (Flash + Pro)...')
    all_reviews.update(review_gemini(prompt, gemini_key))

    print('Sending to Mistral...')
    all_reviews.update(review_mistral(prompt, mistral_key))

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'master_plan_review_{ts}.md'
    lines = [f'# Master Plan Review — Cross-LLM', f'_Generated: {ts}_\n']
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'Done. {len(all_reviews)} reviews collected.')


if __name__ == '__main__':
    main()
