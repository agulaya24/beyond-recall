"""
Beyond Recall v10 — GPT-5.5 Post-Edit Review (2026-04-25)

Thin wrapper around review_v10_gpt55.py that:
- Writes to a fresh-dated review file (does NOT overwrite the 2026-04-24 review)
- Updates the review prompt to mention the SECOND edit pass on top of v10

Run:
    python scripts/review_v10_gpt55_postfix.py
"""

import sys
import json
import time
import datetime
from pathlib import Path

# Import the existing module so we reuse the OpenAI call, env-var load, paper load
import review_v10_gpt55 as base

REPO_ROOT = Path(__file__).parent.parent
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
OUT_PATH = REVIEWS_DIR / 'v10_1_review_gpt55_20260425.md'


REVIEW_PROMPT_POSTFIX = """You are an experienced reviewer for a top empirical ML / HCI venue. Read the full Beyond Recall v10 paper below. Produce a structured review.

This paper has been through extensive revision based on 4 prior cross-LLM reviews + a GPT-5.5 review on 2026-04-24. Notable v10 changes from v9 (already in the prior review's view):
- Author N=1 pilot removed entirely (now relies on 9-of-9 low-baseline subjects + structural extrapolation for the deployment claim)
- Alignment-framing sections (sec 1.5, 5.7) removed for circular reasoning; safety content moved to sec 7.6 future work
- Sec 4.1 added a battery-composition sensitivity block (multiple regression + subset regression). Headline slope = -0.96 [-1.24, -0.67]; under multiple regression controlling for LITERAL_RECALL fraction, partial coefficient on baseline = -0.88 [-1.13, -0.63]; under subset regression dropping Hamerton, slope = -0.89 [-1.18, -0.61]
- Sec 4.5 Letta demoted to exploratory N=3 case study with naming-asymmetry caveat
- LLM-class circularity caveat hoisted to sec 1.3
- Twin-2K demoted to related work only
- Sec 5.5 deployment claims scoped to what was tested

SECOND EDIT PASS (2026-04-25, AFTER the 2026-04-24 GPT-5.5 review). These edits are NEW and you should pay particular attention to whether they are coherent and adequate:
- §4.6.1 Tier 2 (cross-provider replication): demoted to direction-only with explicit sensitivity ranges. The pending-verification disclaimer was removed. New direction-only table with panel ranges. Zitkala-Sa × Gemini Pro is now framed as ~0 (sign-stable null), not −0.55 (the prior reviewer flagged this as overclaim).
- §4.4.2 Supermemory: rebuilt on strict 5-judge primary panel only. New numbers: 110/546 (20.1%); 57 helps / 53 hurts; +1.55 / −1.38 swings (was 89/516, 37/52, +1.45/−1.41 on the audit panel). Table 4.6 footnote rewritten to declare panel asymmetry explicitly.
- §4.3: new per-subject wrong-spec table added (13 rows × c2c v1 + c2c v2 deltas).
- §4.3 / §1.3 / §4.6.2 / §5: random-derangement v2 cascade — old +0.22 → new +0.15 across all references.
- §4.5: named-entity counts updated (Babur 540 → 416, Hamerton Letta 19→26 / BL 19→22). 7-judge sensitivity Δs adjusted (Hamerton +0.20 → +0.09, Babur +0.29 → +0.232).
- §4.2 Table 4.2 compression ratios + means rebuilt; §4.2.1 pairwise table cells updated.
- App B.4 / B.5 / B.6 / D.3.4: numerical updates.
- Verga 2024 reference: arXiv ID `arXiv:2404.18796` added.
- §4.1 line 749 level-CI rounding: −0.25 → −0.24.
- §1.3 Supermemory swings updated to match §4.4.2 numbers.

Your review must follow this exact structure:

## Verdict
One of: CRITICAL_FIXES_REQUIRED / NEEDS_REVISION / READY_WITH_MINOR_FIXES / READY_FOR_ARXIV. One-sentence justification.

## Highest-impact single improvement
What is the ONE thing the author should do next to maximize this paper's impact? Be specific.

## Critical issues (must fix before submission)
Cite section, current claim, suggested fix.

## Needs revision (overclaim, buried caveat, missing read-through)
Cite section, suggest fix.

## What v10 got right
Specifically: did removing the author pilot, folding the alignment framing, adding the battery sensitivity block, demoting Letta to exploratory, and pruning Twin-2K close the issues prior reviewers flagged?

ALSO specifically address the SECOND EDIT PASS:
- Did the §4.6.1 Tier 2 demotion to direction-only adequately address concerns about overclaiming on cross-provider replication?
- Did the §4.4.2 Supermemory rebuild on the 5-judge primary panel close the "panel mismatch" / "audit-panel artifact" concern?
- Are the random-derangement +0.22 → +0.15 cascade and the named-entity count updates (Babur 540 → 416) propagated consistently throughout the paper?

## Missing content
Experiments, citations, or analyses that would substantially strengthen.

## Comparison to the field
Place this against PersonaGym, Twin-2K, LongMemEval, LoCoMo. Where does Beyond Recall stand? What is its distinct contribution?

## Style and presentation
Section flow, redundancy, footnote use, figure captions.

## What I would push back on
If you would push the paper back at peer review, what specifically would you ask for?

Be direct. If you would accept as-is, say so. If you would reject, say so.

PAPER BEGINS:

{paper}
"""


def main():
    print('[postfix] Loading API key...')
    api_key = base.get_win_env('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: OPENAI_API_KEY not found in user env')
        sys.exit(1)
    print(f'[postfix] API key loaded ({len(api_key)} chars)')

    print('[postfix] Loading paper...')
    paper = base.load_paper()
    print(f'[postfix] Paper: {len(paper)} chars, ~{len(paper)//4} tokens')

    prompt = REVIEW_PROMPT_POSTFIX.format(paper=paper)
    print(f'[postfix] Full prompt: {len(prompt)} chars, ~{len(prompt)//4} tokens')

    candidates = ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']
    chosen_model = None
    text = None
    meta = None
    last_error = None

    for model_id in candidates:
        print(f'\n[postfix] Trying model: {model_id}')
        for attempt in range(2):
            t0 = time.time()
            text, err, meta = base.call_openai(api_key, model_id, prompt, max_tokens=8192, timeout=600)
            elapsed = time.time() - t0
            if text:
                print(f'  SUCCESS in {elapsed:.1f}s ({len(text)} chars)')
                wc = len(text.split())
                print(f'  Word count: {wc}')
                if wc < 800:
                    print(f'  WARNING: response only {wc} words (<800), retrying once...')
                    if attempt == 0:
                        time.sleep(5)
                        continue
                    else:
                        print(f'  Still under 800 words after retry. Will try next model.')
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
        print(f'\n[postfix] ALL MODELS FAILED. Last error: {last_error}')
        OUT_PATH.write_text(
            f'# v10 Postfix Review — FAILED\n\nAll candidate models failed.\nLast error: {last_error}\n',
            encoding='utf-8'
        )
        sys.exit(1)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = (
        f'# Beyond Recall v10 — GPT-5.x Post-Edit Review (2026-04-25)\n\n'
        f'**Generated:** {ts}\n'
        f'**Context:** Second-pass review on top of the 2026-04-24 v10 review. '
        f'Covers post-04-24 edits to §4.6.1, §4.4.2, §4.3, §4.5, §4.2, §4.1, §1.3, App B/D, references.\n'
        f'**Model requested chain:** {candidates}\n'
        f'**Model actually used (API response):** `{chosen_model}`\n'
        f'**Paper file:** `docs/beyond_recall_v10_1_draft.md` ({len(paper):,} chars)\n'
        f'**Usage:** {json.dumps(meta.get("usage", {}))}\n'
        f'**Response length:** {len(text)} chars, {len(text.split())} words\n\n'
        f'---\n\n'
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(header + text, encoding='utf-8')
    print(f'\n[postfix] Saved review: {OUT_PATH}')
    print(f'[postfix] Model used: {chosen_model}')
    print(f'[postfix] Words: {len(text.split())}')


if __name__ == '__main__':
    main()
