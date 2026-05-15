"""Try alternative Groq models with higher TPM limits."""
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


def try_model(section3, api_key, model_id, label):
    payload = json.dumps({
        'model': model_id,
        'messages': [{'role': 'user', 'content': REVIEW_PROMPT.format(section3=section3)}],
        'temperature': 0.3,
        'max_tokens': 4096  # smaller models often have lower output max
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.groq.com/openai/v1/chat/completions',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'  [{label}] OK ({len(text)} chars)')
            return text
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f'  [{label}] {e.code}: {body}')
        return None
    except Exception as e:
        print(f'  [{label}] {e}')
        return None


def main():
    key = get_win_env('GROQ_API_KEY')
    section3 = extract_section3()
    print(f'§3 size: {len(section3)} chars (~{len(section3)//4} tokens, ~13K)')

    # Wait for TPM bucket to refill from previous attempts
    print('Waiting 70s for TPM bucket to refill...')
    time.sleep(70)

    # Try models in order of preference. Higher-TPM tiers on Groq:
    # - openai/gpt-oss-120b (often 30K TPM)
    # - llama-3.1-8b-instant (often 100K TPM, much smaller model)
    # - mixtral-8x7b (deprecated)
    # - llama-3.3-70b-versatile (12K TPM — already failed)
    candidates = [
        ('openai/gpt-oss-120b', 'Groq GPT-OSS 120B'),
        ('meta-llama/llama-4-scout-17b-16e-instruct', 'Groq Llama-4 Scout 17B'),
        ('llama-3.1-8b-instant', 'Groq Llama 3.1 8B Instant'),
    ]
    for model_id, label in candidates:
        print(f'\nTrying {label} ({model_id})...')
        result = try_model(section3, key, model_id, label)
        if result:
            out_path = REVIEWS_DIR / f'sec3_external_review_groq_{DATE_TAG}.md'
            contents = [
                f'# §3 External Review — {label}',
                f'_Generated: {datetime.datetime.now().isoformat()}_',
                f'_Paper: {PAPER_PATH.name}_',
                f'_Section size sent: {len(section3)} chars (full)_',
                f'_Note: Groq Llama 3.3 70B failed on TPM limit (12K/min); fell back to {label}_',
                '',
                '## Prompt sent to provider',
                '',
                '```',
                REVIEW_PROMPT.format(section3=section3),
                '```',
                '',
                '---',
                '',
                '## Provider response (verbatim)',
                '',
                result,
            ]
            out_path.write_text('\n'.join(contents), encoding='utf-8')
            print(f'  wrote {out_path.name}')
            return

    print('\nAll Groq fallbacks failed. Sticking with 3 providers.')


if __name__ == '__main__':
    main()
