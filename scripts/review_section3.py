"""
Beyond Recall v11.8 — Section 3 (Study Design) External Review
Sends only §3 (lede + §3.1 through §3.7) to Gemini Pro, Groq, Cerebras, Mistral.
Saves per-provider verbatim responses for downstream synthesis.
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_8_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

DATE_TAG = '20260506'  # Per task spec, literal


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def extract_section3():
    text = PAPER_PATH.read_text(encoding='utf-8')
    lines = text.split('\n')

    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip() == '## 3. Study Design':
            start_idx = i
        elif start_idx is not None and line.strip() == '## 4. Results':
            end_idx = i
            break

    if start_idx is None or end_idx is None:
        raise RuntimeError('Could not locate §3 boundaries.')

    section3 = '\n'.join(lines[start_idx:end_idx]).strip()
    # Strip HTML comments (internal review notes)
    import re
    section3 = re.sub(r'<!--.*?-->', '', section3, flags=re.DOTALL)
    return section3


REVIEW_PROMPT = """You are reviewing Section 3 (Study Design) of a paper titled "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization." Section 3 was just restructured. The new ordering is:

§3.1 Operationalizing representational accuracy (the property)
§3.2 Experimental conditions (what's varied)
§3.3 Scoring rubric with calibrated LLM judge panel
§3.4 Subjects
§3.5 Question battery formation
§3.6 Response models
§3.7 Base Layer Pipeline for the Behavioral Specification

The intent is: experiment design starts with what's being varied (conditions), then how it's measured (rubric+judges), then who/what (subjects, battery, models), then how the artifact is built (pipeline).

Review the section and answer specifically:

1. STRUCTURE: Does the §3.1 -> §3.7 ordering work for a methods section? Specific concerns about forward references (e.g., §3.2 mentioning "14 subjects" before §3.4 introduces them)?
2. CROSS-REFERENCES: Does each cross-reference resolve to the right section semantically? Flag any §X.Y that points somewhere wrong.
3. COMPLETENESS: Anything obviously missing from the methods section that a reviewer would expect?
4. CLARITY/READABILITY: Where does the prose get dense, redundant, or hard to follow?
5. SECTION-LEVEL FLOW: Are the subsection titles, bolded callouts, and tables effective? Anything overstated, understated, or in the wrong place?

Be specific - cite section numbers, line content, and reasoning. Distinguish blocking issues from cosmetic ones. Brief is fine; substance over length.

Section 3 follows below.

---

{section3}
"""


def review_gemini(section3, api_key):
    import urllib.request

    results = {}
    model_id = 'gemini-2.5-pro'
    label = 'Gemini 2.5 Pro'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': REVIEW_PROMPT.format(section3=section3)}]}],
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


def review_groq(section3, api_key):
    import urllib.request
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3)}],
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


def review_cerebras(section3, api_key):
    import urllib.request
    import urllib.error
    import time
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3)}],
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
                body = e.read().decode()[:200]
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


def review_mistral(section3, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3)}],
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


PROVIDER_FILE_KEYS = {
    'Gemini 2.5 Pro': 'gemini_pro',
    'Groq Llama 3.3 70B': 'groq_llama',
    'Cerebras Qwen3 235B': 'cerebras_qwen3',
    'Mistral Large': 'mistral_large',
}


def save_per_provider(all_reviews, prompt_used, section3):
    written = []
    for label, body in all_reviews.items():
        slug = PROVIDER_FILE_KEYS.get(label, label.lower().replace(' ', '_'))
        out_path = REVIEWS_DIR / f'sec3_external_review_{slug}_{DATE_TAG}.md'
        contents = [
            f'# §3 External Review — {label}',
            f'_Generated: {datetime.datetime.now().isoformat()}_',
            f'_Paper: {PAPER_PATH.name}_',
            f'_Section size: {len(section3)} chars_',
            '',
            '## Prompt sent to provider',
            '',
            '```',
            prompt_used,
            '```',
            '',
            '---',
            '',
            '## Provider response (verbatim)',
            '',
            body,
        ]
        out_path.write_text('\n'.join(contents), encoding='utf-8')
        written.append(out_path)
        print(f'  wrote {out_path.name}')
    return written


def main():
    print('Loading API keys from Windows User env...')
    keys = {
        'gemini': get_win_env('GEMINI_API_KEY'),
        'groq': get_win_env('GROQ_API_KEY'),
        'cerebras': get_win_env('CEREBRAS_API_KEY'),
        'mistral': get_win_env('MISTRAL_API_KEY'),
    }
    for k, v in keys.items():
        print(f'  {k}: {"SET" if v else "MISSING"}')

    print('\nExtracting §3...')
    section3 = extract_section3()
    print(f'  §3 size: {len(section3)} chars (~{len(section3)//4} tokens)')

    # Build the literal prompt that will be sent (for archival).
    prompt_used = REVIEW_PROMPT.format(section3=section3)

    all_reviews = {}

    if keys['gemini']:
        print('\nSending to Gemini 2.5 Pro...')
        all_reviews.update(review_gemini(section3, keys['gemini']))
    else:
        print('\nGemini key missing — skipping.')

    if keys['groq']:
        print('\nSending to Groq...')
        all_reviews.update(review_groq(section3, keys['groq']))
    else:
        print('\nGroq key missing — skipping.')

    if keys['cerebras']:
        print('\nSending to Cerebras...')
        all_reviews.update(review_cerebras(section3, keys['cerebras']))
    else:
        print('\nCerebras key missing — skipping.')

    if keys['mistral']:
        print('\nSending to Mistral...')
        all_reviews.update(review_mistral(section3, keys['mistral']))
    else:
        print('\nMistral key missing — skipping.')

    # Count successful providers (response not starting with "ERROR:")
    successful = [label for label, body in all_reviews.items() if not body.startswith('ERROR')]
    failed = [label for label, body in all_reviews.items() if body.startswith('ERROR')]

    print(f'\n--- Summary ---')
    print(f'Successful: {len(successful)}: {successful}')
    print(f'Failed: {len(failed)}: {failed}')

    print('\nSaving per-provider files...')
    save_per_provider(all_reviews, prompt_used, section3)

    if len(successful) < 2:
        print(f'\nWARNING: only {len(successful)} successful providers. Synthesis quality will be limited.')
        sys.exit(1 if len(successful) == 0 else 0)

    print('\nDone. Per-provider files saved. Run synthesis manually.')


if __name__ == '__main__':
    main()
