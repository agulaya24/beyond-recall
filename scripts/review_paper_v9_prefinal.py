"""
Beyond Recall v9 — Pre-Final Cross-LLM Review

Sends docs/beyond_recall_v9_draft.md to 4 reviewer providers with a "pre-final"
review prompt and saves raw outputs incrementally to docs/reviews/.

Mirrors scripts/review_paper.py but:
  - Targets v9
  - Includes all 4 providers (Gemini Pro, Mistral Large, Cerebras Qwen3 235B,
    Groq Llama 3.3 70B) with per-provider truncation caps
  - Writes each review to disk as it completes (crash-safe)
  - Custom prompt framed for pre-final review

Usage:
    python review_paper_v9_prefinal.py
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v9_draft.md'
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
    # Strip HTML comments (internal review notes)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


REVIEW_PROMPT = """You are conducting a PRE-FINAL peer review of a research paper that is about to undergo an author read-through before arXiv submission. The paper is substantially locked. We are NOT looking for sweeping structural revisions. We ARE looking for focused, last-mile issues before submission.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

## CONTEXT FOR THIS REVIEW

The paper was restructured tonight. Key restructuring:
  - §4 now has a consolidated §4.4 "Memory-System Composition" with 3 subsections (Aggregate / Mechanisms / Keckley).
  - §4.5 is the Letta Stateful-Agent study.
  - §4.6 is Robustness.
  - §5 (Discussion) has new §5.1 Anti-Pattern, new §5.5 Practical Implications, and new §5.7 Safety (folded from old §7).
  - The flow across these transitions has been audited but may have rough spots — read §4.4 and §5.1/§5.5/§5.7 carefully.

Appendices A-E were just built. The paper cites them at 11 points. Verify the citations are self-consistent if possible (you don't need to read the appendices themselves unless a body claim seems to need them).

## HEADLINE FINDINGS TO STRESS-TEST

Look for any overreach, under-guarding, or numerical inconsistency on:
  (a) The gradient (slope -0.96, p < 0.001) — §4.2 / §4.3.
  (b) The 70.9% improvement rate on low-baseline subjects.
  (c) Supermemory n=14 near-zero aggregate with bimodal per-question distribution — §4.4.
  (d) H6: "author-derangement" result — zero downward crossings across 120 wrong-spec responses on the living-user pilot.

## SPECIFIC CONSISTENCY TO CHECK

The Fukuzawa Q26 example is reported as 4.20 in the body, but an audit recompute got 4.33. If you catch this, flag it. We already know about it and are deferring the fix to the author's read-through — we're not asking you to fix it, just confirming your eyes catch it.

## REVIEW FORMAT

Provide structured feedback in exactly this format:

## VERDICT
One line: READY / READY-WITH-MINOR-FIXES / NEEDS-REVISION. Then one sentence explaining why.

## CRITICAL ISSUES
Anything that would cause a competent peer reviewer to reject or demand major revision. Cite section and exact claim. Be specific. If none, write "None."

## NUMERICAL / LOGICAL INCONSISTENCIES
Specific numbers, p-values, claim conflicts, or stats that don't add up across sections. Include location. This is the highest-priority category for this review round.

## RESTRUCTURE FLOW ISSUES
Focus here on §4.4 (Aggregate / Mechanisms / Keckley subsections), §4.5 Letta, §4.6 Robustness, §5.1 Anti-Pattern, §5.5 Practical Implications, §5.7 Safety. List any paragraph that reads awkwardly, any transition that doesn't land, any redundancy introduced by the consolidation, or any content that now feels misplaced.

## APPENDIX CITATION CHECK
Any place where the body cites an appendix (A-E) but the citation seems misaimed, too vague, or implies content the body does not verify. If none, write "None."

## NEEDS EXPANSION
Content present but underdeveloped given the claims. Only raise this if it's BLOCKING — do not gold-plate.

## NICE TO HAVE
Low-priority improvements. One sentence each.

## STYLE
Wording, clarity, flow nits. One line each.

Be direct. The author reads this tomorrow morning before the final pass. If the paper is ready, say so. If it isn't, name exactly what blocks it.

---

PAPER:

{paper}
"""


def append_section(out_path, model_label, review_text):
    """Append a single reviewer's output to the raw file (crash-safe)."""
    with out_path.open('a', encoding='utf-8') as f:
        f.write(f'\n\n---\n\n## {model_label}\n\n{review_text}\n')
    print(f'  -> written to {out_path.name}')


def review_gemini_pro(paper, api_key, out_path):
    import urllib.request
    label = 'Gemini 2.5 Pro'
    model_id = 'gemini-2.5-pro'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': REVIEW_PROMPT.format(paper=paper)}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192}
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            text = data['candidates'][0]['content']['parts'][0]['text']
            print(f'  [{label}] done ({len(text)} chars)')
            append_section(out_path, label, text)
            return text
    except Exception as e:
        err = f'ERROR: {e}'
        print(f'  [{label}] {err}')
        append_section(out_path, label, err)
        return err


def review_mistral(paper, api_key, out_path):
    """Mistral Large — try full paper first. On payload/context error, retry at 60k chars."""
    import urllib.request
    import urllib.error
    label = 'Mistral Large'

    def _call(paper_text, truncated_note):
        url = 'https://api.mistral.ai/v1/chat/completions'
        body_content = REVIEW_PROMPT.format(paper=paper_text)
        if truncated_note:
            body_content = body_content.replace('PAPER:\n\n', f'PAPER (NOTE: {truncated_note}):\n\n')
        payload = json.dumps({
            'model': 'mistral-large-latest',
            'messages': [{'role': 'user', 'content': body_content}],
            'temperature': 0.3,
            'max_tokens': 4096
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'python-requests/2.31.0'
        })
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            return data['choices'][0]['message']['content']

    # Attempt 1: full paper
    try:
        text = _call(paper, truncated_note=None)
        print(f'  [{label}] done full-length ({len(text)} chars)')
        append_section(out_path, label, text)
        return text
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f'  [{label}] full-length failed: {e}. Retrying at 60k truncation...')
    except Exception as e:
        print(f'  [{label}] full-length failed: {e}. Retrying at 60k truncation...')

    # Attempt 2: 60k truncation
    try:
        truncated = paper[:60000] + '\n\n[Paper truncated for API limit — first 60k chars]'
        text = _call(truncated, truncated_note='truncated to 60k chars due to full-length failure')
        print(f'  [{label}] done truncated ({len(text)} chars)')
        append_section(out_path, label + ' (60k truncation)', text)
        return text
    except Exception as e:
        err = f'ERROR (both attempts failed): {e}'
        print(f'  [{label}] {err}')
        append_section(out_path, label, err)
        return err


def review_cerebras(paper, api_key, out_path):
    import urllib.request
    import urllib.error
    import time
    label = 'Cerebras Qwen3 235B'
    paper_trunc = paper[:40000] + ('\n\n[Paper truncated — first 40k chars]' if len(paper) > 40000 else '')
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
                print(f'  [{label}] done ({len(text)} chars)')
                append_section(out_path, label + ' (40k truncation)', text)
                return text
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print(f'  [{label}] rate limited, waiting 30s...')
                time.sleep(30)
            else:
                body = ''
                try:
                    body = e.read().decode()[:200]
                except Exception:
                    pass
                err = f'ERROR {e.code}: {body}'
                print(f'  [{label}] {err}')
                append_section(out_path, label, err)
                return err
        except Exception as e:
            err = f'ERROR: {e}'
            print(f'  [{label}] {err}')
            append_section(out_path, label, err)
            return err


def review_groq(paper, api_key, out_path):
    import urllib.request
    import urllib.error
    label = 'Groq Llama 3.3 70B'
    paper_trunc = paper[:18000] + ('\n\n[Paper truncated — first 18k chars]' if len(paper) > 18000 else '')
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
            print(f'  [{label}] done ({len(text)} chars)')
            append_section(out_path, label + ' (18k truncation)', text)
            return text
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode()[:200]
        except Exception:
            pass
        err = f'ERROR {e.code}: {body}'
        print(f'  [{label}] {err}')
        append_section(out_path, label, err)
        return err
    except Exception as e:
        err = f'ERROR: {e}'
        print(f'  [{label}] {err}')
        append_section(out_path, label, err)
        return err


def main():
    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    groq_key = get_win_env('GROQ_API_KEY')

    required = [
        ('GEMINI_API_KEY', gemini_key),
        ('MISTRAL_API_KEY', mistral_key),
        ('CEREBRAS_API_KEY', cerebras_key),
        ('GROQ_API_KEY', groq_key),
    ]
    missing = [k for k, v in required if not v]
    if missing:
        print(f'Missing keys: {missing}')
        sys.exit(1)

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f's114_v9_prefinal_raw_{ts}.md'
    header = (
        f'# Beyond Recall v9 — Pre-Final Cross-LLM Review (Raw)\n'
        f'_Generated: {ts}_\n'
        f'_Source: {PAPER_PATH.name}_\n'
        f'_Paper length: {len(paper)} chars_\n\n'
        f'Reviewers (in order of execution): Gemini 2.5 Pro (full), '
        f'Mistral Large (full -> 60k fallback), Cerebras Qwen3 235B (40k), '
        f'Groq Llama 3.3 70B (18k).\n'
    )
    out_path.write_text(header, encoding='utf-8')
    print(f'Raw output -> {out_path}\n')

    # Order: biggest-context first (Gemini Pro, Mistral), then truncated.
    print('[1/4] Sending to Gemini 2.5 Pro...')
    review_gemini_pro(paper, gemini_key, out_path)

    print('\n[2/4] Sending to Mistral Large...')
    review_mistral(paper, mistral_key, out_path)

    print('\n[3/4] Sending to Cerebras Qwen3 235B (40k)...')
    review_cerebras(paper, cerebras_key, out_path)

    print('\n[4/4] Sending to Groq Llama 3.3 70B (18k)...')
    review_groq(paper, groq_key, out_path)

    print(f'\nDone. Raw review file: {out_path}')
    print('Next: read raw file and author synthesis to s114_v9_prefinal_synthesis.md.')


if __name__ == '__main__':
    main()
