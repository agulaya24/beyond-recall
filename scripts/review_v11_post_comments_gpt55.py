"""
Beyond Recall v11 — GPT-5.5 Post-Comments Direction Review (2026-04-27)

Sends:
- Full v11 paper draft (`docs/beyond_recall_v11_draft.md`)
- Curated subset of the 183 review items:
    * B1-B10 (Bavani structural notes)
    * C16-C49 (§1.3 cluster, 34 comments)
    * C50-C52 (§1.4 cluster, 3 comments)
    * Cross-cutting heavy-hitters: C82, C84, C89, C131, C153, C156

Asks for an "overall-direction" take on the §1.3 + §1.4 restructure the author
is wrestling with after rejecting the v3 lede.

Reuses the OpenAI integration / model fallback / quality gate from
`review_v10_gpt55.py` (max_completion_tokens, GPT-5.5 model id).

Run:
    python scripts/review_v11_post_comments_gpt55.py
"""

import sys
import json
import time
import datetime
from pathlib import Path

# Reuse OpenAI call + env-var loader from the v10 script
import review_v10_gpt55 as base

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_draft.md'
COMMENTS_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v11_comments_extracted_20260427.md'
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v11_post_comments_review_gpt55_20260427.md'


# Curated comment ranges from the 183-item file (1-based line numbers in the
# extracted markdown). Verified by grep on 2026-04-27.
#
# B1-B10:   lines 16  .. 143  (Bavani structural notes block)
# C16-C49:  lines 552 .. 1411 (§1.3 cluster — 34 comments)
# C50-C52:  lines 1412.. 1489 (§1.4 cluster — 3 comments)
# C82:      lines 2204.. 2229
# C84:      lines 2256.. 2281
# C89:      lines 2378.. 2403
# C131:     lines 3402.. 3423
# C153:     lines 3930.. 3955
# C156:     lines 4008.. 4033
CURATED_RANGES = [
    ('B1-B10 (Bavani structural notes)',         16,   143),
    ('C16-C49 (§1.3 cluster — 34 comments)',     552,  1411),
    ('C50-C52 (§1.4 cluster — 3 comments)',      1412, 1489),
    ('C82 (cross-cutting heavy-hitter)',         2204, 2229),
    ('C84 (cross-cutting heavy-hitter)',         2256, 2281),
    ('C89 (cross-cutting heavy-hitter)',         2378, 2403),
    ('C131 (per-memory-system anchor crossing)', 3402, 3423),
    ('C153 (cross-cutting heavy-hitter)',        3930, 3955),
    ('C156 (cross-cutting heavy-hitter)',        4008, 4033),
]


def load_v11_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
    import re
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text.strip()


def load_curated_comments():
    """Slice the comments file by the curated line ranges and concatenate
    with section dividers. Line numbers are 1-based and inclusive."""
    raw_lines = COMMENTS_PATH.read_text(encoding='utf-8').splitlines()
    parts = []
    parts.append(
        '# Curated comment subset — sent to reviewer\n\n'
        f'_Source: `docs/reviews/v11_comments_extracted_20260427.md` (183 total items)._\n'
        f'_Curated subset includes:_ B1-B10 + C16-C49 + C50-C52 + C82 + C84 + C89 + C131 + C153 + C156.\n'
        f'_Comments NOT included in this subset (the remaining ~135 items C1-C15, C53-C81, C83, C85-C88, C90-C130, C132-C152, C154-C155, C157-C173) — but the reviewer is told this set is curated, not exhaustive._\n\n'
    )
    for label, start, end in CURATED_RANGES:
        parts.append(f'\n\n---\n\n## RANGE: {label} (lines {start}-{end})\n\n')
        # Convert to 0-based slice (start-1 .. end inclusive => end)
        chunk = '\n'.join(raw_lines[start - 1:end])
        parts.append(chunk)
    return ''.join(parts)


REVIEW_PROMPT = """You are an experienced reviewer asked to give an overall-direction take on a paper revision the author is wrestling with.

Background: the author is reviewing 173 line-level comments on the Beyond Recall v10.1 paper. The assistant helping with edits truncated comment summaries during the review, missed depth in several key comments, and applied a §1.3 rewrite that the author rejected. The author has now asked for a "collective review" perspective to help triage the right path.

Specific context the author has flagged:

- The §1.3 v3 lede the author REJECTED was: "The specification improves representational accuracy on subjects the model does not already know well from pretraining." The author said this loses the gradient-as-structural-finding framing (C82) and the category-shift framing (C84).

- The author wants multi-anchor moves (1->4, 2->5) emphasized as wins-at-the-margin (C26).

- C131 flags a missing per-memory-system anchor-crossing analysis.

- §1.4 ("Why the gradient matters") needs reframing toward a "What this implies" closing-thought paragraph (C50-C52).

- The author's PROPOSED v4 lede direction (incorporating the missed comments):

> Adding the Behavioral Specification changes the category of answer the AI produces, not just the number attached to it. The improvement is largest where the model knows the subject least: on the 9 subjects whose pretraining baseline is low, all 9 improved when the specification was added on top of the extracted facts. Mean lift +0.89 points on the 1-5 rubric; 70.9% of individual questions improved, with a typical improvement of one full rubric category. On the per-question distribution, large category jumps (1->4, 2->5) appear in roughly 5-10% of questions on the spec conditions: low-frequency but high-magnitude wins that the aggregate mean understates. 12 of 14 overall subjects improved.

Your review must answer the following sections, in this order, using markdown headers:

## 1. Is the v4 lede the right direction?
Given the §1.3 comment cluster (C16-C49), is the author's proposed v4 lede the right direction, or is there a better framing? Be specific. If you would tweak it, give exact replacement text. If you would restructure, name what to keep, what to cut, what to add.

## 2. §1.4 — merge, reframe, or restructure?
Given the §1.4 comments (C50-C52), should §1.4 be merged into §1.3 as a closing paragraph? Kept separate but reframed away from "Why the gradient matters"? Or restructured another way? Make a recommendation. Justify it from the comment text.

## 3. Top 3-5 highest-impact restructure moves
Looking at the 183 review items collectively (you have a curated set, not all of them, but use what you can see), what are the 3-5 highest-impact restructure moves the author should prioritize? Examples of cross-cutting themes the author has identified: footnote-vs-parenthetical conventions, layman language, section reordering between §3.x subsections, color-coding tables, missing closing statement at end of §4. Rank by paper-level impact, not number-of-comments.

## 4. C131 placement
C131 flags a missing per-memory-system anchor-crossing analysis. Once computed, where should it live: §1.3, §4.4.1, §4.4.2, or somewhere else? Justify briefly.

## 5. Anywhere to start over?
Is there anywhere in the paper the author should "start over" on the section rather than incrementally patch? If yes, name the section and what the new framing should be. If no, say so.

## 6. Weaknesses not in the comments
Specific weaknesses you see in the current paper that aren't covered by any of the existing comments you can see. Be direct. The author wants honest direction, not validation.

Length target: 1500-2500 words. Use markdown headers exactly as numbered above.

Be direct. If the author's v4 lede is right, say so. If it is still wrong, say so and give the right one. The author wants honest direction, not validation.

---

PAPER BEGINS:

{paper}

---

CURATED COMMENT SUBSET BEGINS:

{comments}
"""


def main():
    print('[v11-post-comments] Loading API key...')
    api_key = base.get_win_env('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: OPENAI_API_KEY not found in user env')
        sys.exit(1)
    print(f'[v11-post-comments] API key loaded ({len(api_key)} chars)')

    print('[v11-post-comments] Loading v11 paper...')
    paper = load_v11_paper()
    print(f'[v11-post-comments] Paper: {len(paper):,} chars, ~{len(paper)//4:,} tokens')

    print('[v11-post-comments] Loading curated comment subset...')
    comments = load_curated_comments()
    print(f'[v11-post-comments] Comments subset: {len(comments):,} chars, ~{len(comments)//4:,} tokens')

    prompt = REVIEW_PROMPT.format(paper=paper, comments=comments)
    print(f'[v11-post-comments] Full prompt: {len(prompt):,} chars, ~{len(prompt)//4:,} tokens')

    # Sanity gate — warn if we are over 120K tokens (~480K chars)
    if len(prompt) > 480_000:
        print(f'[v11-post-comments] WARNING: prompt may exceed 120K-token target ({len(prompt):,} chars).')

    candidates = ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']
    chosen_model = None
    text = None
    meta = None
    last_error = None

    for model_id in candidates:
        print(f'\n[v11-post-comments] Trying model: {model_id}')
        for attempt in range(2):
            t0 = time.time()
            text, err, meta = base.call_openai(api_key, model_id, prompt, max_tokens=8192, timeout=600)
            elapsed = time.time() - t0
            if text:
                print(f'  SUCCESS in {elapsed:.1f}s ({len(text):,} chars)')
                wc = len(text.split())
                print(f'  Word count: {wc}')
                if wc < 1200:
                    print(f'  WARNING: response only {wc} words (<1200), retrying once...')
                    if attempt == 0:
                        time.sleep(5)
                        continue
                    else:
                        print(f'  Still under 1200 words after retry. Will try next model.')
                        text = None
                        last_error = f'short_response_{wc}_words'
                        break
                chosen_model = meta.get('model') or model_id
                break
            else:
                print(f'  FAIL ({elapsed:.1f}s): {err}')
                last_error = err
                if attempt == 0:
                    print('  retrying in 10s...')
                    time.sleep(10)
        if text:
            break

    if not text:
        print(f'\n[v11-post-comments] ALL MODELS FAILED. Last error: {last_error}')
        OUT_PATH.write_text(
            f'# v11 Post-Comments Review — FAILED\n\nAll candidate models failed.\nLast error: {last_error}\n',
            encoding='utf-8'
        )
        sys.exit(1)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = (
        f'# Beyond Recall v11 — GPT-5.x Post-Comments Direction Review (2026-04-27)\n\n'
        f'**Generated:** {ts}\n'
        f'**Context:** Overall-direction collective review on the §1.3 + §1.4 restructure '
        f'after the v3 lede was rejected. Sent the full v11 paper plus a curated subset of '
        f'review items: B1-B10 + C16-C49 + C50-C52 + C82, C84, C89, C131, C153, C156. '
        f'~135 items NOT sent (kept under 120K tokens).\n'
        f'**Model requested chain:** {candidates}\n'
        f'**Model actually used (API response):** `{chosen_model}`\n'
        f'**Paper file:** `docs/beyond_recall_v11_draft.md` ({len(paper):,} chars)\n'
        f'**Comments file:** `docs/reviews/v11_comments_extracted_20260427.md` (curated subset, {len(comments):,} chars)\n'
        f'**Usage:** {json.dumps(meta.get("usage", {}))}\n'
        f'**Response length:** {len(text):,} chars, {len(text.split()):,} words\n\n'
        f'---\n\n'
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(header + text, encoding='utf-8')
    print(f'\n[v11-post-comments] Saved review: {OUT_PATH}')
    print(f'[v11-post-comments] Model used: {chosen_model}')
    print(f'[v11-post-comments] Words: {len(text.split())}')


if __name__ == '__main__':
    main()
