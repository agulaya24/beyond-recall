"""
Beyond Recall v9 — Mistral Large full-paper review
One-shot review call with tailored prompt. Saves raw response to docs/reviews/.
"""

import os
import sys
import json
import subprocess
import datetime
import time
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v9_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

# Truncation budget. Mistral Large = 128K token context. Paper is ~346KB (~86K tokens).
# Keep everything through §7 (line 1786) — appendices will be truncated with a note.
# That gives us roughly 260KB of paper + prompt overhead + 4K output budget.
TRUNCATE_AT_LINE = 1787  # cut just before "## Appendix A..."


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    raw = PAPER_PATH.read_text(encoding='utf-8')
    # Strip HTML comments (internal review notes)
    raw = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    lines = raw.splitlines()
    if len(lines) > TRUNCATE_AT_LINE:
        kept = '\n'.join(lines[:TRUNCATE_AT_LINE])
        appendix_note = (
            '\n\n---\n\n'
            '[APPENDICES A-E TRUNCATED FOR API CONTEXT BUDGET. '
            'Appendix A: Predicate Vocabulary. '
            'Appendix B: Question Batteries (B.6 contains the r = +0.646 LITERAL / r = -0.582 INTERPRETIVE correlations against delta_spec referenced in the review checklist). '
            'Appendix C: Conditions, Models, and Memory-System Configurations. '
            'Appendix D: Validity Audit and Score Distributions. '
            'Appendix E: Benchmark Scope Analysis. '
            'Review the main body only; cite appendix contents only where the main body itself references them.]'
        )
        return kept + appendix_note
    return raw


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


def call_mistral(paper, api_key, timeout=300):
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
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
        return data['choices'][0]['message']['content']


def main():
    print('Loading API key...')
    mistral_key = get_win_env('MISTRAL_API_KEY')
    if not mistral_key:
        print('ERROR: MISTRAL_API_KEY not set')
        sys.exit(1)

    print('Loading paper...')
    paper = load_paper()
    print(f'Paper payload: {len(paper)} chars, ~{len(paper)//4} tokens\n')

    print('Calling Mistral Large...')
    response = None
    error = None
    for attempt in [1, 2]:
        try:
            response = call_mistral(paper, mistral_key)
            print(f'  [done] {len(response)} chars response')
            break
        except Exception as e:
            error = e
            print(f'  [attempt {attempt}] ERROR: {e}')
            if attempt == 1:
                print('  retrying in 10s...')
                time.sleep(10)

    ts = datetime.datetime.now().strftime('%Y%m%d')
    out_path = REVIEWS_DIR / f'v9_final_review_mistral_large_{ts}.md'

    if response is None:
        body = f'# v9 Mistral Large Review — FAILED\n\n_Date: {ts}_\n\nBoth attempts failed. Last error:\n\n```\n{error}\n```\n'
        out_path.write_text(body, encoding='utf-8')
        print(f'\nFailure logged: {out_path}')
        sys.exit(2)

    word_count = len(response.split())
    flag = '' if word_count >= 500 else f'\n\n> WARNING: response is {word_count} words (< 500). May be truncated or low-effort.\n'

    header = (
        f'# Beyond Recall v9 — Mistral Large Review\n\n'
        f'_Model: mistral-large-latest_\n'
        f'_Date: {ts}_\n'
        f'_Paper payload: {len(paper)} chars (~{len(paper)//4} tokens). Appendices A-E truncated for context budget._\n'
        f'_Response: {len(response)} chars, {word_count} words_\n'
        f'{flag}\n---\n\n'
    )
    out_path.write_text(header + response, encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'Word count: {word_count}')


if __name__ == '__main__':
    main()
