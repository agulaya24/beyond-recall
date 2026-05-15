"""
Retry Groq + Cerebras for §3 review with fixes.
- Groq: truncate the prompt aggressively (it returned 413 = payload too large; their max is ~30k tokens of input).
- Cerebras: wait longer, retry with exponential backoff.
"""
import os
import sys
import json
import subprocess
import datetime
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_8_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
DATE_TAG = '20260506'


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
    section3 = '\n'.join(lines[start_idx:end_idx]).strip()
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


def trim_for_groq(section3, target_chars=28000):
    """
    Groq's stated context is large but their HTTP payload limit per request is
    ~32k chars (the 413 error). Trim by cutting Appendix-bound sections most
    aggressively: §3.3.6 footnote tables, §3.5 controls section, §3.6 prompt
    schema. Keep all subsection HEADERS so the structural review is intact.
    """
    if len(section3) <= target_chars:
        return section3

    # Strategy: keep heading + first paragraph of each subsection; trim long
    # footnote-only blocks. Simpler: chop the deepest sub-subsections first.
    text = section3

    # 1. Drop the long judge-calibration "Memory-system effect on abstention"
    #    footnote and its surrounding 100-word paragraph (§3.3.6 deep tail).
    import re
    # Strip all footnote DEFINITIONS (lines starting "[^...]:") which are dense and not needed for structure review.
    lines = text.split('\n')
    pruned = []
    skip_until_blank = False
    for ln in lines:
        if ln.startswith('[^') and ']:' in ln:
            skip_until_blank = True
            continue
        if skip_until_blank:
            if ln.strip() == '':
                skip_until_blank = False
            continue
        pruned.append(ln)
    text = '\n'.join(pruned)

    if len(text) <= target_chars:
        return text + '\n\n[NOTE: Footnote definitions stripped to fit Groq payload limit; section structure and prose intact.]'

    # 2. If still too big, drop the §3.4 subjects table (rows only, keep row 1 + ellipsis).
    lines = text.split('\n')
    in_subjects_table = False
    seen_row_count = 0
    pruned = []
    for ln in lines:
        if '| # | Subject | Source |' in ln:
            in_subjects_table = True
            pruned.append(ln)
            continue
        if in_subjects_table:
            if ln.startswith('| ') and seen_row_count < 3:
                pruned.append(ln)
                seen_row_count += 1
                continue
            elif ln.startswith('| ') and seen_row_count == 3:
                pruned.append('| ... | (11 more subjects, see paper) | ... | ... | ... | ... |')
                seen_row_count += 1
                continue
            elif ln.startswith('| '):
                continue
            else:
                in_subjects_table = False
        pruned.append(ln)
    text = '\n'.join(pruned)

    if len(text) <= target_chars:
        return text + '\n\n[NOTE: Footnote definitions and most subject-table rows trimmed for Groq payload limit; section structure intact.]'

    # 3. Hard truncate as last resort.
    return text[:target_chars] + '\n\n[NOTE: Hard-truncated at ~28k chars for Groq payload limit; review applies to first portion only.]'


def review_groq(section3, api_key):
    section3_trimmed = trim_for_groq(section3, target_chars=28000)
    print(f'  Groq trimmed: {len(section3)} -> {len(section3_trimmed)} chars')
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3_trimmed)}],
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
            return {'Groq Llama 3.3 70B': text}, section3_trimmed
    except Exception as e:
        print(f'  [Groq] ERROR: {e}')
        return {'Groq Llama 3.3 70B': f'ERROR: {e}'}, section3_trimmed


def review_cerebras(section3, api_key):
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3)}],
        'temperature': 0.3,
        'max_tokens': 8192
    }).encode('utf-8')

    waits = [60, 120, 180]  # progressive backoff
    for attempt, wait in enumerate(waits):
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0'
        })
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return {'Cerebras Qwen3 235B': text}
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            if e.code == 429 and attempt < len(waits) - 1:
                print(f'  [Cerebras] 429 attempt {attempt+1}, waiting {wait}s...')
                time.sleep(wait)
            else:
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return {'Cerebras Qwen3 235B': f'ERROR: {e.code}: {body}'}
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return {'Cerebras Qwen3 235B': f'ERROR: {e}'}


PROVIDER_FILE_KEYS = {
    'Groq Llama 3.3 70B': 'groq_llama',
    'Cerebras Qwen3 235B': 'cerebras_qwen3',
}


def save_per_provider(label, body, prompt_used, section3_or_trimmed):
    slug = PROVIDER_FILE_KEYS[label]
    out_path = REVIEWS_DIR / f'sec3_external_review_{slug}_{DATE_TAG}.md'
    contents = [
        f'# §3 External Review — {label}',
        f'_Generated: {datetime.datetime.now().isoformat()}_',
        f'_Paper: {PAPER_PATH.name}_',
        f'_Section size sent: {len(section3_or_trimmed)} chars_',
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
    print(f'  wrote {out_path.name}')


def main():
    keys = {
        'groq': get_win_env('GROQ_API_KEY'),
        'cerebras': get_win_env('CEREBRAS_API_KEY'),
    }
    section3 = extract_section3()
    print(f'§3 size: {len(section3)} chars (~{len(section3)//4} tokens)')

    if keys['groq']:
        print('\nRetrying Groq with payload trim...')
        result, trimmed = review_groq(section3, keys['groq'])
        for label, body in result.items():
            prompt = REVIEW_PROMPT.format(section3=trimmed)
            save_per_provider(label, body, prompt, trimmed)

    if keys['cerebras']:
        print('\nRetrying Cerebras with longer backoff...')
        result = review_cerebras(section3, keys['cerebras'])
        for label, body in result.items():
            prompt = REVIEW_PROMPT.format(section3=section3)
            save_per_provider(label, body, prompt, section3)


if __name__ == '__main__':
    main()
