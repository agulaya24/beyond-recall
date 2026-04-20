"""
Beyond Recall - Round 2 FOCUSED-SECTIONS review for truncated providers.
Sends only the abstract + sections relevant to the focus areas to Groq/Cerebras,
so they can actually answer the focus questions.
Usage: python review_paper_round2_focused.py
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


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def extract_section(text, start_marker, end_marker=None):
    """Extract a section from start_marker up to end_marker (or end of file)."""
    start = text.find(start_marker)
    if start < 0:
        return ''
    if end_marker:
        end = text.find(end_marker, start + len(start_marker))
        if end < 0:
            return text[start:]
        return text[start:end]
    return text[start:]


def build_focused_payload():
    """Build a focused payload containing only the sections that the focus-area
    questions target, plus Abstract + Section 1 for context."""
    text = PAPER_PATH.read_text(encoding='utf-8')
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL).strip()

    # Sections to include:
    # - Abstract (for claim-disaggregation focus question)
    # - Section 1 intro (for context)
    # - Section 4.3 + 4.3.1 (Letta parity result)
    # - Section 4.4 (BL positioning)
    # - Section 5.7 (memory-provider axis framing)
    # - Section 5.8 (Letta architectural convergence)
    # - Section 6 (Limitations) - important for humility assessment

    abstract = extract_section(text, '## Abstract', '## 1. Introduction')
    intro = extract_section(text, '## 1. Introduction', '## 2. Related Work')
    sec_43 = extract_section(text, '### 4.3 Memory Systems with and Without the Specification', '### 4.4 Base Layer')
    sec_44 = extract_section(text, '### 4.4 Base Layer', '### 4.5 The Wrong-Spec')
    sec_57 = extract_section(text, '### 5.7 A First Benchmark', '### 5.8 Architectural Convergence')
    sec_58 = extract_section(text, '### 5.8 Architectural Convergence', '### 5.9 The Pipeline Is Anthropic-Family')
    limitations = extract_section(text, '## 6. Limitations', '## 7. Future Work')

    parts = [
        '# Beyond Recall - Focused Excerpts for Review\n',
        '[Editor note: The full paper is ~142k chars. These are the sections most relevant to the Round 2 focus areas. Please answer the focus-area questions based on the text below. If you cannot see enough context to judge an item, say so.]\n',
        abstract,
        intro,
        sec_43,
        sec_44,
        sec_57,
        sec_58,
        limitations,
    ]
    payload = '\n\n'.join(p.strip() for p in parts if p.strip())
    return payload


REVIEW_PROMPT = """You are reviewing a research paper for arXiv submission. Be a rigorous, honest peer reviewer. Do not be diplomatic.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

This is Round 2 of recursive review. Below are the ABSTRACT, INTRODUCTION, and KEY SECTIONS (4.3/4.3.1, 4.4, 5.7, 5.8, Limitations) of the revised paper - the sections the Round 2 focus areas target. Earlier full-paper context (related work, methodology, other results) is not included here for length reasons; answer based on what you can see, and flag any question where you need more context.

Please provide structured feedback in EXACTLY this format:

## FOCUS-AREA ASSESSMENT

1. Section 4.4 now positions Base Layer as a behavioral-spec layer with an open-source retrieval floor, NOT as a 5th memory provider competing with Mem0/Letta/Zep/Supermemory. Does this land honestly, or does the section still read as defensive / conflict-of-interest motivated?

2. Section 5.7 ("A First Benchmark on an Axis the Category Wasn't Optimized For") reframes the memory-provider comparison. Does it come across as a fair "referee introducing a new axis" or does it still read as biased against the competing systems?

3. The Abstract disaggregates three kinds of claims (what was tested / what is extrapolated / what is NOT claimed). Is this disaggregation clear and useful, or muddled?

4. Section 4.3.1 reports a Letta stateful-agent matched-response-model parity test (Haiku + Letta memory = 3.24 vs Haiku + Base Layer full-stack = 3.04, Letta at 65% context size). Is this n=1 result handled with appropriate humility, or does the paper overclaim / underclaim from it?

5. Anywhere in these sections that a sharp reviewer would flag as overclaiming - call it out with section number and quoted claim.

## CRITICAL ISSUES
Issues that would cause rejection or significantly undermine the claims, based on what is visible here.

## MISSING
Content that should be in THESE sections but isn't.

## NEEDS EXPANSION
Underdeveloped passages in these sections.

## METHODOLOGY CONCERNS
Any issues visible in 4.3/4.3.1 (Letta test design) or related setup.

## MINOR ISSUES
Clarity / framing / wording fixes for these sections.

## VERDICT
One sentence assessment of the revised framing in these focus sections.

---

PAPER EXCERPTS:

{paper}
"""


def review_groq(paper, api_key):
    import urllib.request
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
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
            print(f'  [Groq Llama 3.3 70B (focused)] done ({len(text)} chars)')
            return {'Groq Llama 3.3 70B (focused-sections)': text}
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B (focused-sections)': f'ERROR: {e}'}


def review_cerebras(paper, api_key, model_id='llama-3.3-70b'):
    import urllib.request, urllib.error, time
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': model_id,
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(paper=paper)}],
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
                print(f'  [Cerebras {model_id} (focused)] done ({len(text)} chars)')
                return {f'Cerebras {model_id} (focused-sections)': text}
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:200]
            except Exception: pass
            if e.code == 429 and attempt < 2:
                print(f'  [Cerebras] rate limited, waiting 30s...')
                time.sleep(30)
            elif e.code == 404 and model_id != 'qwen-3-235b-a22b-instruct-2507':
                print(f'  [Cerebras] 404 on {model_id}, falling back to qwen-3-235b...')
                return review_cerebras(paper, api_key, model_id='qwen-3-235b-a22b-instruct-2507')
            else:
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {f'Cerebras {model_id} (focused-sections)': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {f'Cerebras {model_id} (focused-sections)': f'ERROR: {e}'}


def main():
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    print('Building focused payload...')
    paper = build_focused_payload()
    print(f'Focused payload: {len(paper)} chars, ~{len(paper)//4} tokens')

    # Write payload alongside for traceability
    (REVIEWS_DIR / f'round_02_focused_payload_{ts}.md').write_text(paper, encoding='utf-8')

    print('Loading API keys...')
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')

    all_reviews = {}
    if groq_key:
        print('Sending focused payload to Groq...')
        all_reviews.update(review_groq(paper, groq_key))
    if cerebras_key:
        print('Sending focused payload to Cerebras...')
        all_reviews.update(review_cerebras(paper, cerebras_key))

    out_path = REVIEWS_DIR / f'round_02_focused_{ts}.md'
    lines = [
        f'# Paper Review - Round 2 (Focused Sections)',
        f'_Generated: {ts}_',
        '_Payload: Abstract + Section 1 intro + 4.3/4.3.1 + 4.4 + 5.7 + 5.8 + Limitations_',
        '_Sent to: Groq + Cerebras (providers with payload-size limits)_',
        '',
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'{len(all_reviews)} focused reviews collected.')


if __name__ == '__main__':
    main()
