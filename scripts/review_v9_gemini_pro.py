"""
Beyond Recall v9 — Gemini 2.5 Pro full-paper review.
One-shot cross-LLM review against the v9 draft with the custom v9 review prompt.
"""

import os
import sys
import json
import re
import time
import subprocess
import datetime
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v9_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

MODEL_ID = 'gemini-2.5-pro'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


REVIEW_PROMPT = """You are an experienced reviewer for a strong empirical ML / HCI venue (e.g., ICLR, CHI, ACL Findings). Read the full Beyond Recall v9 paper below and produce a structured, uncompromising review.

Your review should be organized as:

## Critical issues
Items that must be fixed before submission. Cite section and specific claim. Be concrete.

## Needs revision
Framing or evidence issues where the paper overclaims, buries caveats, or fails to address a reader's natural objection. Cite section and suggest specific wording.

## Missing content
Experiments, analyses, or citations that would substantially strengthen the paper if added before submission.

## Nice-to-have
Smaller clarity or citation improvements. Lower priority.

## Style
Prose, tone, or structural polish items.

## Verdict
One of: CRITICAL_FIXES_REQUIRED / NEEDS_REVISION / READY_WITH_MINOR_FIXES / READY. Plus one-sentence justification.

Specific items to evaluate with your own judgment (do not assume they are done or not done):
- Is the §4.1 gradient slope confounded by battery composition? Appendix B.6 reports r = +0.646 (LITERAL_RECALL) / r = -0.582 (INTERPRETIVE) against Δ_spec.
- Is the LLM-class circularity limitation surfaced prominently enough (abstract, §1.3), or only buried in §4.6 / §6?
- §4.5 Letta: is the exploratory framing calibrated, or does it under- or over-claim given the N=3 data?
- §1.5 and §5.7 alignment framing: does the paper define behavioral alignment such that representational accuracy is required and then conclude representational accuracy is necessary for behavioral alignment? If so, is the circularity acknowledged?
- §5.5 deployment claims: do they match what was tested (static full-spec serving) or read as product positioning?
- Twin-2K references: does the repeated citation across §1, §2.3, §5.6 create an impression of empirical support that the exploratory N=100 run does not justify?
- Run-to-run pipeline variance: §6.3 says specs match ~45% verbatim at temperature 0; is this adequately characterized for the precision of the per-subject claims in §4.1?

Be direct. If you would reject the paper as-is, say so.

PAPER BEGINS:

{paper}
"""


def call_gemini_pro(paper, api_key, attempt_label=''):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': REVIEW_PROMPT.format(paper=paper)}]}],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 16384,
        }
    }).encode('utf-8')
    req = urllib.request.Request(
        url, data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'},
    )
    print(f'  [{MODEL_ID}]{attempt_label} sending ({len(payload)/1024:.1f} KB payload)...')
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read())
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise RuntimeError(f'Unexpected response shape: {json.dumps(data)[:800]}')
    print(f'  [{MODEL_ID}]{attempt_label} done ({len(text)} chars)')
    return text, data


def main():
    print('Loading GEMINI_API_KEY from Windows env...')
    api_key = get_win_env('GEMINI_API_KEY')
    if not api_key:
        print('ERROR: GEMINI_API_KEY not set.')
        sys.exit(1)

    print(f'Loading paper from {PAPER_PATH}...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens')

    text = None
    raw = None
    err = None
    for attempt in range(2):
        try:
            text, raw = call_gemini_pro(paper, api_key, attempt_label=f' attempt {attempt+1}')
            break
        except Exception as e:
            err = e
            body = ''
            if isinstance(e, urllib.error.HTTPError):
                try:
                    body = e.read().decode()[:800]
                except Exception:
                    body = '<unreadable body>'
            print(f'  [{MODEL_ID}] attempt {attempt+1} FAILED: {e} {body}')
            if attempt == 0:
                print('  Retrying in 10s...')
                time.sleep(10)

    ts = datetime.datetime.now().strftime('%Y%m%d')
    out_path = REVIEWS_DIR / f'v9_final_review_gemini_pro_{ts}.md'

    if text is None:
        out_path.write_text(
            f'# Beyond Recall v9 — Gemini 2.5 Pro Review — FAILED\n\n'
            f'_Generated: {datetime.datetime.now().isoformat()}_\n\n'
            f'Error after retry: {err}\n',
            encoding='utf-8',
        )
        print(f'FAILURE logged to {out_path}')
        print('SUMMARY: API call failed; no review produced.')
        sys.exit(2)

    words = len(text.split())
    header = (
        f'# Beyond Recall v9 — Gemini 2.5 Pro Review\n'
        f'_Generated: {datetime.datetime.now().isoformat()}_\n'
        f'_Model: {MODEL_ID}_\n'
        f'_Paper: {PAPER_PATH.name} ({len(paper)} chars)_\n'
        f'_Response: {len(text)} chars / {words} words_\n\n'
        f'---\n\n'
    )
    out_path.write_text(header + text, encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'Response: {len(text)} chars, {words} words')
    if words < 500:
        print('WARNING: response under 500 words — flag to user.')


if __name__ == '__main__':
    main()
