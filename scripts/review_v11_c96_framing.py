"""
Beyond Recall v11 — C96 framing collective review (2026-04-28)

Author wrestling with the §4.1 "Coupling-free reframing" + "Honest reframing"
block. Current version is too technical (rejected by author). Layman v2 reframes
the gradient as a question-level pattern, not a per-subject mean shift.

Sends a focused prompt to GPT-5.5 + Gemini 2.5 Pro in parallel:
  - the proposed §4.1 layman reframing
  - the rubric integer-anchor definitions (§3.6 table)
  - the per-question breakdown (351 low-baseline questions, jump-size distribution)
  - one number discrepancy in §1.3 the author wants triaged

Asks: is the framing fair? Where could it overstate or mislead?

Output: docs/reviews/v11_c96_framing_review_20260428.md
"""

import os
import sys
import json
import time
import subprocess
import datetime
import threading
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v11_c96_framing_review_20260428.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


PROMPT = """You are an experienced reviewer asked to give a fairness check on a §4.1 reframing the author is wrestling with.

CONTEXT
=======
The paper "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization" tests whether a 7,000-token behavioral specification helps language models predict how a specific person would respond to a question, on 14 autobiographers spanning low-to-high pretraining baselines.

The headline §4.1 finding: a regression of per-subject lift (Δ_C4a = C4a − C5) on baseline (C5) yields slope = −0.96. Read at face value this says "the spec helps subjects the model knows least about more than subjects it knows well."

The author had a coupling-aware critic point out that this slope is mechanically pushed toward −1 by the change-score parameterization (Δ on its own baseline), so the −0.96 number is partly arithmetic and partly substantive. To triangulate, three additional analyses were run on the same per-subject (C5, C4a) data:
  1. Level regression of C4a directly on C5: slope = +0.04 [95% CI −0.24, +0.33], R² = 0.008. C4a is essentially flat across the C5 range of 1.02 to 2.77, clustering tightly around its mean of 2.46.
  2. Permutation test (10,000 iterations shuffling C4a across subjects): null distribution for the Δ-on-C5 slope is centered at −0.998 (SD 0.127). The observed −0.960 is not extreme against this null (two-sided p = 0.77).
  3. Subject-level bootstrap (10,000 iterations): CI [−1.254, −0.740] for the Δ-on-C5 slope, [−0.254, +0.260] for the level slope (level CI straddles zero).

The current paper text is dense and technical. The author rejected the most recent "layman" rewrite as still being too jargon-heavy ("mechanical artifact of arithmetic" / "separate the mechanical part from the substantive part" / "treatment-effect-heterogeneity"). The author also flagged that the "C4a clusters around 2.46" framing collapses everything into a per-subject mean and hides the per-question heterogeneity that is the actually-interesting finding: on some questions (especially recall-style questions on low-baseline subjects) the spec produces multi-anchor jumps from "no idea" to "specific, grounded, correct"; on other questions it does little.

PROPOSED §4.1 REFRAMING (LAYMAN V3)
====================================

> **Sanity-checking the gradient.** Read at face value, the headline slope of −0.96 says the spec helps subjects the model knows least about substantially more than subjects it already knows well. That phrasing is misleading. Three follow-up analyses on the same per-subject data show what is actually happening. Detail in Appendix B.7.

> **What is actually happening.** The 2.46 number that summarizes after-spec performance is a per-subject average across roughly 30 to 80 questions. Inside each battery, some questions show large lifts and others do not move much. The pattern is sharpest on low-baseline subjects: on recall-style questions where the model otherwise refuses or guesses off-base, the spec produces multi-anchor jumps from "no idea" to "specific, grounded, correct" (anchor-crossing detail in §4.4.2 and the per-system Pattern 1/2/3 analysis). On questions where the model would not have answered well even with the full source corpus available, the spec does not move the score much. The gradient is the residue of those question-level wins: low-baseline subjects have more questions where the spec can do this work, so their per-subject mean climbs further.

> The cleaner reframing, then, is not "the spec lifts low-baseline subjects more than high-baseline ones" and not "every subject lands at the same ceiling." It is: **on the questions where the spec changes the category of answer, low-baseline subjects have more such questions to be changed.** Subsequent sections that lean on the gradient (§4.4.2, §4.6, §5.5) should be read against this reframing.

RUBRIC INTEGER ANCHORS (FROM §3.6)
==================================

| Score | Meaning |
|---|---|
| 1 | Refusal or irrelevant |
| 2 | Generic, not subject-specific |
| 3 | Partially captures the subject's behavioral pattern |
| 4 | Substantively captures the pattern on multiple dimensions |
| 5 | Captures the behavioral pattern observable in the verbatim ground-truth passage |

A question is said to "cross an integer anchor upward" if its 5-judge primary mean under C4a (facts + spec) lands in a different integer band than its 5-judge primary mean under C5 (no context).

PER-QUESTION BREAKDOWN (351 LOW-BASELINE QUESTIONS, C4a vs C5, 5-judge primary)
==============================================================================

Total questions:        351 (9 low-baseline subjects × 39 questions each)
Crossed UP at all:      193 (55.0%)
Crossed DOWN:            24 (6.8%)
No anchor crossed:      134 (38.2%)
Net upward:             169 (48.1%)

Upward-crossing breakdown by jump size:
  +1 anchor (e.g. 1→2, 2→3, 3→4):  129 questions (36.8%)
  +2 anchors (e.g. 1→3, 2→4):       44 questions (12.5%)
  +3 anchors (e.g. 1→4):            17 questions (4.8%)
  +4 anchors (1→5):                  3 questions (0.9%)

Multi-anchor (≥2): 64 questions (18.2%)
Extreme (≥3 anchors): 20 questions (5.7%)

Per-subject upward-crossing rate ranges from 25.6% (Babur) to 74.4% (Sunity Devee).

NUMBER DISCREPANCY THE AUTHOR HAS FLAGGED
=========================================

Currently §1.3 (callout box) says:

> Multi-anchor jumps (1→3, 1→4, 2→5) appear in roughly 5-10% of questions on the spec conditions: low-frequency but high-magnitude wins the aggregate mean understates.

Actual numbers from the breakdown above:
  1→3: 12.3% (43 questions)
  1→4:  4.8% (17 questions)
  2→5:  0.0% (0 questions, none observed)

The literal sum of "1→3 + 1→4 + 2→5" is 17.1%, not 5-10%. If the intended bundle is "extreme jumps from refusal to substantive-or-better" (≥3 anchors: 1→4 and 1→5), that is 5.7%, which fits the "roughly 5-10%" claim. Author wants advice on which framing to keep.

QUESTIONS FOR YOU
=================

Please answer each in order using markdown headers.

## 1. Is the proposed §4.1 reframing fair?
Specifically the bolded claim "on the questions where the spec changes the category of answer, low-baseline subjects have more such questions to be changed." Does the per-question breakdown above support this claim? Where does it overstate or understate? What would you tighten?

## 2. Is the per-question breakdown in the proposed prose adequate?
The author wants the breakdown of "how many questions does the spec change the category of answer for, and how are those categories defined?" to be visible in the body, not buried in appendix. Does the proposed prose surface this adequately, or should there be an explicit table or sentence-level numbers in the body? If yes, name the specific number(s) that should appear inline.

## 3. The §1.3 5-10% multi-anchor claim — keep, fix, or replace?
Given the discrepancy above, what is the right framing? Options:
  (a) keep "5-10%" and explicitly redefine the bundle as "extreme jumps (≥3 anchors)" = 5.7%
  (b) replace with "Multi-anchor jumps (≥2 anchors) appear in roughly 18% of low-baseline questions"
  (c) split into two numbers: 18% multi-anchor, 6% extreme
  (d) other (specify)
Recommend one. Justify briefly.

## 4. Is "categories" the right word?
The proposed prose says "questions where the spec changes the category of answer." This relies on the reader understanding that a category is defined by the integer anchor band (1, 2, 3, 4, 5). Is "category" clear here or does it need a parenthetical pointer? If the latter, give exact replacement text.

## 5. Anything else that misleads or overstates?
Any other phrasing in the proposed prose that overclaims, understates, or could mislead a reader skimming §4.1? Be specific.

Length: 700-1200 words total. Be direct. The author wants honest direction, not validation.
"""


def call_openai(api_key, model, prompt, max_tokens=4096, timeout=300):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    body = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': max_tokens,
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        text = data['choices'][0]['message']['content']
        return text, None, {'model': data.get('model', model)}
    except urllib.error.HTTPError as e:
        return None, f'HTTPError {e.code}: {e.read().decode("utf-8", errors="replace")[:500]}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


def call_gemini(api_key, model, prompt, timeout=300):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    body = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 8192, 'temperature': 0.3},
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        cands = data.get('candidates', [])
        if not cands:
            return None, f'no candidates: {json.dumps(data)[:500]}', None
        parts = cands[0].get('content', {}).get('parts', [])
        text = ''.join(p.get('text', '') for p in parts)
        return text, None, {'model': model}
    except urllib.error.HTTPError as e:
        return None, f'HTTPError {e.code}: {e.read().decode("utf-8", errors="replace")[:500]}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


results = {}


def run_openai():
    api_key = get_win_env('OPENAI_API_KEY')
    if not api_key:
        results['gpt55'] = ('', 'no API key in user env', None)
        return
    for model in ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']:
        print(f'[gpt55] trying {model}...')
        t0 = time.time()
        text, err, meta = call_openai(api_key, model, PROMPT, max_tokens=4096, timeout=400)
        elapsed = time.time() - t0
        if text:
            print(f'[gpt55] {model} OK in {elapsed:.0f}s ({len(text)} chars)')
            results['gpt55'] = (text, None, meta)
            return
        print(f'[gpt55] {model} FAIL ({elapsed:.0f}s): {err[:200] if err else "no text"}')
    results['gpt55'] = ('', 'all OpenAI candidates failed', None)


def run_gemini():
    api_key = get_win_env('GEMINI_API_KEY')
    if not api_key:
        results['gemini'] = ('', 'no API key in user env', None)
        return
    for model in ['gemini-2.5-pro', 'gemini-2.5-flash']:
        print(f'[gemini] trying {model}...')
        t0 = time.time()
        text, err, meta = call_gemini(api_key, model, PROMPT, timeout=400)
        elapsed = time.time() - t0
        if text:
            print(f'[gemini] {model} OK in {elapsed:.0f}s ({len(text)} chars)')
            results['gemini'] = (text, None, meta)
            return
        print(f'[gemini] {model} FAIL ({elapsed:.0f}s): {err[:200] if err else "no text"}')
    results['gemini'] = ('', 'all Gemini candidates failed', None)


def main():
    print(f'[c96-framing] Prompt: {len(PROMPT):,} chars')
    print(f'[c96-framing] Launching 2 reviewers in parallel...')

    t_oa = threading.Thread(target=run_openai)
    t_gm = threading.Thread(target=run_gemini)
    t_oa.start()
    t_gm.start()
    t_oa.join()
    t_gm.join()

    gpt_text, gpt_err, gpt_meta = results.get('gpt55', ('', 'thread missing', None))
    gem_text, gem_err, gem_meta = results.get('gemini', ('', 'thread missing', None))

    out = []
    out.append(f'# C96 §4.1 Reframing — Collective Review\n\n')
    out.append(f'_Date: {datetime.datetime.now().strftime("%Y-%m-%d")}_\n')
    out.append(f'_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_\n\n')
    out.append(f'## Reviewer 1 — OpenAI ({gpt_meta.get("model") if gpt_meta else "FAILED"})\n\n')
    if gpt_text:
        out.append(gpt_text)
    else:
        out.append(f'_FAILED: {gpt_err}_\n')
    out.append('\n\n---\n\n')
    out.append(f'## Reviewer 2 — Google ({gem_meta.get("model") if gem_meta else "FAILED"})\n\n')
    if gem_text:
        out.append(gem_text)
    else:
        out.append(f'_FAILED: {gem_err}_\n')
    out.append('\n')

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(''.join(out), encoding='utf-8')
    print(f'\n[c96-framing] Wrote {OUT_PATH} ({sum(len(p) for p in out):,} chars)')

    if not gpt_text and not gem_text:
        print('[c96-framing] BOTH reviewers failed.')
        sys.exit(1)
    if not gpt_text:
        print('[c96-framing] OpenAI failed; Gemini succeeded.')
    if not gem_text:
        print('[c96-framing] Gemini failed; OpenAI succeeded.')


if __name__ == '__main__':
    main()
