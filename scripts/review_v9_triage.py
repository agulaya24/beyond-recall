"""
Beyond Recall — Cross-LLM Triage-Plan Review
Sends the v9 edit-plan triage doc + the full Word-review annotation extract to
the same free-tier providers used for paper review, collects structured feedback
on whether the triage is complete, correctly prioritized, and whether the
ULTRA-HIGH-PRIORITY rerun queue is sufficient.

Usage:
    python review_v9_triage.py [--include-gemini]
"""

import json
import os
import subprocess
import sys
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TRIAGE_PATH = REPO_ROOT / 'docs' / 'reviews' / 's114_v9_edit_plan.md'
ANNOTATIONS_PATH = REPO_ROOT / 'docs' / 'reviews' / 's114_word_annotations.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_inputs():
    triage = TRIAGE_PATH.read_text(encoding='utf-8').strip()
    annotations = ANNOTATIONS_PATH.read_text(encoding='utf-8').strip()
    return triage, annotations


REVIEW_PROMPT = """You are reviewing a TRIAGE DOCUMENT for a research paper revision. Be a rigorous, honest peer reviewer — the author is deciding which of 233 author-annotations to apply and in what order, and is one step away from kicking off expensive data reruns and post-hoc analyses based on this plan.

The paper being revised is "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization" (v8 under review).

You are given TWO inputs:
  1. The RAW ANNOTATIONS extracted from the author's Word review (233 comments + tracked changes).
  2. The TRIAGE DOC the editor produced that buckets those annotations into (Part 0) ultra-high-priority data reruns/analyses, (A) cross-cutting changes, (B) structural/TOC changes, (C) rerun blockers, (D) figure rebuilds, (E) headline-findings list, (F) section-by-section wording fixes.

Your job is NOT to review the paper. Your job is to review the TRIAGE — whether it correctly captures and prioritizes the annotations.

Provide structured feedback in exactly this format:

## CONSENSUS ON PART 0 (ULTRA-HIGH-PRIORITY QUEUE)
For each of P0-1 through P0-12, state: AGREE / DISAGREE / MODIFY. If MODIFY, say specifically what. If any item is missing from Part 0 that should be there (i.e. an annotation in the raw file that warrants a rerun or heavy post-hoc but is not in Part 0), call it out explicitly with the section it came from.

## STRUCTURAL DECISIONS (PART B)
For each of B1-B8, say AGREE / DISAGREE / MODIFY with reasoning. Pay special attention to:
- B1 results-section reorganization (§4.5 moves to end, §4.6/§4.7 fold into §4.4, §4.8 moves out)
- B3 discussion-content belonging in §2 Related Work
- These are irreversible decisions — push back hard if wrong.

## HEADLINE FINDINGS (PART E)
The nine headline findings H1-H9 will drive the abstract, blog post, and outreach. Review each:
- Is the claim accurately scoped?
- Is anything listed that shouldn't be (over-claimed)?
- Is anything missing that should be (under-claimed)?
- Is H6 ("None of the 40 responses got worse") sufficiently guarded against the n=1 living-user sample?

## MISSING ANNOTATIONS
Scan the raw annotation file and identify any annotation that is NOT captured anywhere in the triage doc (Parts 0 / A / B / C / D / E / F). List them with anchor text + section.

## PRIORITY / SEQUENCING CRITIQUE
Is the recommended order-of-operations at the bottom of the triage correct? Should any Part 0 item be downgraded? Any Part F item be upgraded? Is anything blocking something else that isn't captured?

## RISKS THE TRIAGE UNDER-WEIGHTS
Items the editor may be under-prioritizing. Look for: scientific-integrity issues, methodology gaps, claims the author flagged as interesting but that change the paper's framing, items marked "headline" in the raw that aren't in E.

## VERDICT
One paragraph: is this triage safe to greenlight as-is? What must change before the author can kick off Part 0 reruns?

Be direct. The author is deciding whether to launch paid experiments and analyses off this triage today. If something is wrong, say so clearly.

---

RAW ANNOTATIONS:

{annotations}

---

TRIAGE DOC:

{triage}
"""


def review_gemini(prompt_content, api_key):
    import urllib.request, urllib.error
    results = {}
    for model_id, label in [
        ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
        ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
    ]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt_content}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'python-requests/2.31.0'
        })
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


def review_groq(prompt_content, api_key, max_chars=18000):
    import urllib.request
    # Groq strict limit — if too long, truncate annotations portion
    if len(prompt_content) > max_chars:
        prompt_content = prompt_content[:max_chars] + '\n\n[TRUNCATED for Groq payload limit — first {} chars]'.format(max_chars)
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': prompt_content}],
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
            print(f'  [Groq Llama 3.3 70B] done ({len(text)} chars)')
            return {'Groq Llama 3.3 70B': text}
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B': f'ERROR: {e}'}


def review_cerebras(prompt_content, api_key, max_chars=40000):
    import urllib.request, urllib.error, time
    if len(prompt_content) > max_chars:
        prompt_content = prompt_content[:max_chars] + '\n\n[TRUNCATED for Cerebras payload limit — first {} chars]'.format(max_chars)
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': prompt_content}],
        'temperature': 0.3,
        'max_tokens': 8192
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
                print(f'  [Cerebras] ERROR: {e.code}: {e.read().decode()[:100]}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_mistral(prompt_content, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt_content}],
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


def save_results(all_reviews):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f's114_v9_triage_review_{ts}.md'
    lines = ['# V9 Triage Plan — Cross-LLM Consensus Review', f'_Generated: {ts}_\n']
    lines.append(f'_Source triage: {TRIAGE_PATH.name}_')
    lines.append(f'_Source annotations: {ANNOTATIONS_PATH.name}_\n')
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    return out_path


def main():
    include_gemini = '--include-gemini' in sys.argv

    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY') if include_gemini else None
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    required = [('GROQ', groq_key), ('CEREBRAS', cerebras_key), ('MISTRAL', mistral_key)]
    if include_gemini:
        required.insert(0, ('GEMINI', gemini_key))
    missing = [k for k, v in required if not v]
    if missing:
        print(f'Missing keys: {missing}')
        sys.exit(1)

    print('Loading triage + annotations...')
    triage, annotations = load_inputs()
    full_prompt = REVIEW_PROMPT.format(annotations=annotations, triage=triage)
    print(f'Full prompt: {len(full_prompt)} chars (~{len(full_prompt)//4} tokens)')
    print(f'  Annotations: {len(annotations)} chars')
    print(f'  Triage: {len(triage)} chars\n')

    all_reviews = {}

    if include_gemini:
        print('Sending to Gemini (full payload)...')
        all_reviews.update(review_gemini(full_prompt, gemini_key))
    else:
        print('Skipping Gemini (pass --include-gemini to enable)')

    print('Sending to Groq (truncated to 30k)...')
    all_reviews.update(review_groq(full_prompt, groq_key))

    print('Sending to Cerebras (truncated to 40k)...')
    all_reviews.update(review_cerebras(full_prompt, cerebras_key))

    print('Sending to Mistral (full payload)...')
    all_reviews.update(review_mistral(full_prompt, mistral_key))

    out_path = save_results(all_reviews)
    print(f'\nDone. {len(all_reviews)} reviews collected.')
    print(f'Review file: {out_path}')


if __name__ == '__main__':
    main()
