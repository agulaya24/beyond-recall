"""
v11.8 cross-LLM review: full §1 Introduction + full §5 Discussion + focused
guidance on §5.8 Closing argument.

Loads the v11.8 draft, slices §1 (lines 11-149) and §5 (lines 1505-1600),
sends to free-tier providers (Gemini Pro, Groq Llama 3.3 70B, Cerebras Qwen3
235B, Mistral Large) with a tailored review prompt that asks for guidance on
the closing argument specifically.

Saves combined report at docs/reviews/v11_8_intro_s5_closing_<ts>.md.

Usage:
    python review_v11_8_intro_s5_closing.py
"""

import json
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_8_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_sections():
    text = PAPER_PATH.read_text(encoding='utf-8')
    lines = text.splitlines()
    # §1 from "## 1." (line 11) up to but not including "## 2." (line 150)
    s1 = '\n'.join(lines[10:149]).strip()
    # §5 from "## 5." (line 1505) up to but not including "## 6." (line 1601)
    s5 = '\n'.join(lines[1504:1600]).strip()
    return s1, s5


REVIEW_PROMPT = """You are reviewing two sections of a research paper for arXiv submission. Be a rigorous, honest peer reviewer. Your task is to give substantive guidance on the closing argument (Section 5.8) given the introduction and the rest of Section 5 as context.

The paper is: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

The author's central claim, set in §1.1: AI memory has been optimized for recall (finding the right fact for a given query). Recall is one part of memory; how a person interprets the facts and experiences of their life is the part that gives recall its meaning, and the part recall-optimized infrastructure does not measure. The paper proposes "representational accuracy" as the AI-side measure of how well a system captures a specific person's interpretive patterns, and tests whether an authored "Behavioral Specification" can produce it.

Section 5 is the Discussion. The closing argument (§5.8) is the last subsection.

Read §1 INTRODUCTION and §5 DISCUSSION below, then provide structured feedback in this exact format:

## §5.8 CLOSING ARGUMENT — DOES IT LAND?
Direct evaluation of whether the closing argument earns the conclusion the paper is making. Specifically address:
- Does it correctly frame the paper as being about MEMORY (not personalization, not infrastructure)?
- Does it integrate findings rather than restate them?
- Does it bookend the §1 introduction's framing?
- Is it overclaiming or underclaiming relative to the evidence in §5?

## §5.8 SPECIFIC FIXES
Concrete edits to specific sentences or phrases. Cite the offending text and propose alternatives.

## §1 / §5 COHERENCE ISSUES
Any places where the closing fails to harken back to §1, or where it contradicts something in §5.1-§5.7.

## TERMS AND VOICE
Use of canonical terms (interpretation, representational accuracy, behavioral alignment, Behavioral Specification, interpretive layer). Inconsistencies, drift, register problems.

## STRUCTURAL RISK
Anything in the closing that might draw a reviewer's attention as advocacy/pitch rather than research conclusion.

## VERDICT ON §5.8
One paragraph: is it ready to lock, or what needs to change first.

Be direct. Do not be diplomatic. The author wants critical guidance, not validation.

---

§1 INTRODUCTION:

{s1}

---

§5 DISCUSSION:

{s5}
"""


def review_gemini(prompt, api_key):
    import urllib.request
    results = {}
    for model_id, label in [('gemini-2.5-pro', 'Gemini 2.5 Pro')]:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 6144}
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'
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


def review_groq(prompt, api_key):
    import urllib.request
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'max_tokens': 6144
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


def review_cerebras(prompt, api_key):
    import urllib.request, urllib.error, time
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'max_tokens': 6144
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
                body = e.read().decode()[:200] if hasattr(e, 'read') else ''
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_mistral(prompt, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'max_tokens': 6144
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
    groq_key = get_win_env('GROQ_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    print('Loading sections...')
    s1, s5 = load_sections()
    print(f'  §1: {len(s1)} chars (~{len(s1)//4} tokens)')
    print(f'  §5: {len(s5)} chars (~{len(s5)//4} tokens)')
    prompt = REVIEW_PROMPT.format(s1=s1, s5=s5)
    print(f'  prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)\n')

    all_reviews = {}

    if gemini_key:
        print('Sending to Gemini Pro...')
        all_reviews.update(review_gemini(prompt, gemini_key))
    if groq_key:
        print('Sending to Groq...')
        all_reviews.update(review_groq(prompt, groq_key))
    if cerebras_key:
        print('Sending to Cerebras...')
        all_reviews.update(review_cerebras(prompt, cerebras_key))
    if mistral_key:
        print('Sending to Mistral...')
        all_reviews.update(review_mistral(prompt, mistral_key))

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'v11_8_intro_s5_closing_{ts}.md'
    lines = [
        f'# v11.8 Cross-LLM Review — §1 + §5 with focus on §5.8 Closing argument',
        f'_Generated: {ts}_',
        f'_§1 length: {len(s1)} chars; §5 length: {len(s5)} chars_\n'
    ]
    for model, review in all_reviews.items():
        lines.append(f'\n---\n\n## {model}\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'Reviews collected: {len(all_reviews)}')


if __name__ == '__main__':
    main()
