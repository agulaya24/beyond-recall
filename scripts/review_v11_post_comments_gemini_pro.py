"""
Beyond Recall v11 — Gemini 2.5 Pro post-comments collective review.

Parallel to a GPT-5.5 review running in another agent. Triangulates the
§1.3 / §1.4 restructure direction the author is wrestling with after a
rejected v3 lede attempt.

Sends:
  - the full v11 paper draft (docs/beyond_recall_v11_draft.md)
  - a curated subset of the 173-comment review file:
      * Bavani structural notes B1-B10
      * §1.3 line-level cluster (Comments 16-49)
      * §1.4 cluster (Comments 50-52)
      * cross-cutting heavy-hitters: C82, C84, C89, C131, C153, C156
  - a directional prompt asking Gemini to triage the right path

Saves to docs/reviews/v11_post_comments_review_gemini_pro_20260427.md.
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
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_draft.md'
COMMENTS_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v11_comments_extracted_20260427.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

PRIMARY_MODEL = 'gemini-2.5-pro'
FALLBACK_MODEL = 'gemini-2.5-flash'


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


def slice_lines(text, start_1, end_1_inclusive):
    """1-indexed line slice, inclusive on both ends."""
    lines = text.splitlines()
    return '\n'.join(lines[start_1 - 1:end_1_inclusive])


def build_curated_comment_subset():
    """
    Hand-picked load-bearing subset from v11_comments_extracted_20260427.md.
    Line ranges verified against the file structure as of 2026-04-27.
    """
    raw = COMMENTS_PATH.read_text(encoding='utf-8')

    sections = []

    # Bavani notes (B1-B10) — full block including header
    sections.append(("Bavani Notes B1-B10 (structural / cross-cutting)",
                     slice_lines(raw, 12, 145)))

    # §1.3 line-level cluster: Comment 16 (line 552) through Comment 49 end (line 1411)
    sections.append(("§1.3 What we found — Comments 16 to 49 (the rejected-v3 cluster)",
                     slice_lines(raw, 552, 1411)))

    # §1.4 cluster: Comments 50, 51, 52 (lines 1412-1489)
    sections.append(("§1.4 Why the gradient matters — Comments 50, 51, 52",
                     slice_lines(raw, 1412, 1489)))

    # Cross-cutting heavy-hitters (single comments each)
    sections.append(("Cross-cutting C82 (§4.1 — gradient-as-structural-finding framing)",
                     slice_lines(raw, 2204, 2229)))
    sections.append(("Cross-cutting C84 (§4.1 — category-shift framing as headline)",
                     slice_lines(raw, 2256, 2281)))
    sections.append(("Cross-cutting C89 (§4.1 Example C — multi-anchor moves significance)",
                     slice_lines(raw, 2378, 2403)))
    sections.append(("Cross-cutting C131 (§4.4.1 — missing per-memory-system anchor-crossing analysis)",
                     slice_lines(raw, 3402, 3423)))
    sections.append(("Cross-cutting C153 (§5.2 — additivity framing should be per-question pattern, not aggregate)",
                     slice_lines(raw, 3930, 3955)))
    sections.append(("Cross-cutting C156 (§5.4 — Pattern 1/2/3 framing reuse in §4.4)",
                     slice_lines(raw, 4008, 4033)))

    parts = []
    for title, body in sections:
        parts.append(f"\n\n=== {title} ===\n\n{body.strip()}\n")
    return ''.join(parts).strip()


REVIEW_PROMPT = """You are an experienced reviewer asked to give an overall-direction take on a paper revision the author is wrestling with.

Background: the author is reviewing 173 line-level comments on the Beyond Recall v10.1 paper. The assistant helping truncated comment summaries during the review, missed depth in several key comments, and applied a §1.3 rewrite that the author rejected (it lost the gradient-as-structural-finding framing per C82 and the category-shift framing per C84). The author has now asked for collective-review perspectives to help triage the right path.

Your review should answer:

1. Given the §1.3 comment cluster (C16-C49), is the author's proposed v4 lede [shown below] the right direction, or is there a better framing?

Author's proposed v4 lede:
"Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least: on the 9 subjects whose pretraining baseline is low, all 9 improved when the specification was added on top of the extracted facts. Mean lift +0.89 points on the 1-5 rubric; 70.9% of individual questions improved, with a typical improvement of one full rubric category. On the per-question distribution, large category jumps (1->4, 2->5) appear in roughly 5-10% of questions on the spec conditions: low-frequency but high-magnitude wins that the aggregate mean understates. 12 of 14 overall subjects improved."

2. Given the §1.4 comments (C50-C52), should §1.4 be merged into §1.3 as a closing paragraph? Kept separate but reframed away from "Why the gradient matters"? Or restructured another way?

3. Looking at the 173 comments collectively, what are the 3-5 highest-impact restructure moves the author should prioritize?

4. C131 flags missing per-memory-system anchor-crossing analysis. Should this be in §1.3, §4.4.1, or §4.4.2 once computed?

5. Is there anywhere the author should "start over" rather than incrementally patch?

6. Specific weaknesses you see in the current paper that aren't covered by any of the existing comments.

Be direct. The author wants honest direction, not validation.

Length: 1500-2500 words.

Paper begins:

{paper}

Comment subset begins:

{comments}
"""


def call_gemini(model_id, paper, comments, api_key, attempt_label=''):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    body_text = REVIEW_PROMPT.format(paper=paper, comments=comments)
    payload = json.dumps({
        'contents': [{'parts': [{'text': body_text}]}],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 16384,
        }
    }).encode('utf-8')
    req = urllib.request.Request(
        url, data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.31.0'},
    )
    print(f'  [{model_id}]{attempt_label} sending ({len(payload)/1024:.1f} KB payload, {len(body_text)} chars)...')
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read())
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise RuntimeError(f'Unexpected response shape: {json.dumps(data)[:1200]}')
    print(f'  [{model_id}]{attempt_label} done ({len(text)} chars)')
    return text, data


def main():
    print('Loading GEMINI_API_KEY from Windows user env...')
    api_key = get_win_env('GEMINI_API_KEY')
    if not api_key:
        print('ERROR: GEMINI_API_KEY not set in Windows user env.')
        sys.exit(1)

    print(f'Loading paper from {PAPER_PATH}...')
    paper = load_paper()
    print(f'Paper: {len(paper)} chars, ~{len(paper)//4} tokens')

    print(f'Building curated comment subset from {COMMENTS_PATH.name}...')
    comments = build_curated_comment_subset()
    print(f'Comment subset: {len(comments)} chars, ~{len(comments)//4} tokens')

    text = None
    raw = None
    used_model = None
    err = None

    # Try Gemini 2.5 Pro first, with one retry on transient failure.
    for attempt in range(2):
        try:
            text, raw = call_gemini(PRIMARY_MODEL, paper, comments, api_key,
                                    attempt_label=f' attempt {attempt+1}')
            used_model = PRIMARY_MODEL
            break
        except Exception as e:
            err = e
            body = ''
            if isinstance(e, urllib.error.HTTPError):
                try:
                    body = e.read().decode()[:1000]
                except Exception:
                    body = '<unreadable body>'
            print(f'  [{PRIMARY_MODEL}] attempt {attempt+1} FAILED: {e} {body}')
            if attempt == 0:
                print('  Retrying in 15s...')
                time.sleep(15)

    # Fallback to Flash if Pro failed.
    if text is None:
        print(f'\nFalling back to {FALLBACK_MODEL}...')
        for attempt in range(2):
            try:
                text, raw = call_gemini(FALLBACK_MODEL, paper, comments, api_key,
                                        attempt_label=f' fallback attempt {attempt+1}')
                used_model = FALLBACK_MODEL
                break
            except Exception as e:
                err = e
                body = ''
                if isinstance(e, urllib.error.HTTPError):
                    try:
                        body = e.read().decode()[:1000]
                    except Exception:
                        body = '<unreadable body>'
                print(f'  [{FALLBACK_MODEL}] attempt {attempt+1} FAILED: {e} {body}')
                if attempt == 0:
                    print('  Retrying in 15s...')
                    time.sleep(15)

    out_path = REVIEWS_DIR / 'v11_post_comments_review_gemini_pro_20260427.md'

    if text is None:
        out_path.write_text(
            f'# Beyond Recall v11 — Gemini Post-Comments Review — FAILED\n\n'
            f'_Generated: {datetime.datetime.now().isoformat()}_\n\n'
            f'Both {PRIMARY_MODEL} and {FALLBACK_MODEL} failed.\n'
            f'Last error: {err}\n',
            encoding='utf-8',
        )
        print(f'\nFAILURE logged to {out_path}')
        sys.exit(2)

    words = len(text.split())
    fallback_note = ''
    if used_model != PRIMARY_MODEL:
        fallback_note = (f'\n**NOTE:** {PRIMARY_MODEL} was rate-limited or failed; '
                         f'this review was produced by the fallback model {used_model}.\n')

    header = (
        f'# Beyond Recall v11 — Gemini Post-Comments Direction Review\n\n'
        f'_Generated: {datetime.datetime.now().isoformat()}_  \n'
        f'_Model: {used_model}_  \n'
        f'_Paper: {PAPER_PATH.name} ({len(paper)} chars)_  \n'
        f'_Curated comment subset: {len(comments)} chars (B1-B10 + C16-C52 + C82, C84, C89, C131, C153, C156)_  \n'
        f'_Response: {len(text)} chars / {words} words_  \n'
        f'{fallback_note}\n'
        f'---\n\n'
    )
    out_path.write_text(header + text, encoding='utf-8')
    print(f'\nSaved: {out_path}')
    print(f'Response: {len(text)} chars, {words} words')
    if words < 800:
        print('WARNING: response under 800 words — flag to user.')


if __name__ == '__main__':
    main()
