"""
Beyond Recall — pattern-predicate activation claim collective review (2026-04-28)

Sends a focused empirical-claim defensibility prompt to GPT-5.5 + Gemini 2.5 Pro
in parallel. The claim under review:

  "Pattern-predicate activation, not direct quote lookup or anchor-fact recall,
  is the dominant mechanism by which the Behavioral Specification produces
  extreme upward anchor-crossing lifts on prediction questions about subjects
  the model has minimal pretraining footprint on."

Output: docs/reviews/pattern_activation_claim_review_20260428.md
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
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'pattern_activation_claim_review_20260428.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


PROMPT = """You are an experienced empirical reviewer asked to stress-test a specific mechanism claim emerging from the Beyond Recall study.

THE CLAIM UNDER REVIEW
======================
"Pattern-predicate activation, not direct quote lookup or anchor-fact recall, is the dominant mechanism by which the Behavioral Specification produces extreme upward anchor-crossing lifts on prediction questions about subjects the model has minimal pretraining footprint on."

STUDY CONTEXT
=============
The Beyond Recall study tests whether a 7,000-token behavioral specification helps a language model predict how a specific person would respond to a question, on 14 autobiographers. The specification is structured into anchors (epistemic axioms), core (values/dispositions), predictions (forward inferences), and a unified brief synthesizing the layers. The specification contains behavioral predicates (e.g. "evaluates landscapes aesthetically before engaging people"), not biographical facts.

A wins inventory across 18 condition pairs identified 60 unique paired questions where the spec produces extreme upward jumps (>=3 rubric anchors, e.g. from band 1 "refusal" to band 4 "substantive"). A 20-question sample was classified into spec-content driver mechanisms using an LLM rater applied to the full spec text + the post-spec response + the held-out ground truth passage:

  PATTERN_PREDICATE (spec contains a behavioral predicate the post-response activates): 12/20
  INFERENCE_CHAIN (spec doesn't contain the answer but contains predicates needed to infer it): 7/20
  ANCHOR_FACT (spec contains a specific fact the post-response uses verbatim): 1/20
  DIRECT_QUOTE_MATCH (>=6-gram overlap between spec and held-out passage): 0/20

QUESTION-AXIS DISTRIBUTION AMONG THE 60 UNIQUE EXTREME JUMPS
============================================================
  LITERAL_RECALL: 28.3% of the 60 wins (panel-wide rate is 10.2%, so 2.77x overrepresented)
  INTERPRETIVE_INFERENCE: 0.75x panel rate
  REFUSAL_TRIGGERING: 0.95x panel rate

PRE-RESPONSE FAILURE MODE AT BASELINE (C5, no context)
=======================================================
  FULL_REFUSAL ("I don't know who that is"): 71.7%
  CLARIFY_REQUEST: 8.3%
  Other (generic, off-base, partial): 20%

So the typical extreme-jump question goes from a baseline refusal to a substantive answer that the LLM rater attributes to a behavioral predicate in the spec, not to a verbatim fact in the spec.

QUESTIONS FOR YOU
=================
Please answer each in order using markdown headers. Be direct. The author wants honest stress-testing, not validation.

## 1. Is the dominant-mechanism claim defensible from the 20-case sample?

The sample distribution (12/20 PATTERN_PREDICATE, 7/20 INFERENCE_CHAIN, 1/20 ANCHOR_FACT, 0/20 DIRECT_QUOTE_MATCH) suggests pattern activation dominates fact-lookup as the driver. Is this a defensible claim from N=20? What sample size would you want for confidence? What disconfirming evidence would change the conclusion?

## 2. What's the alternative hypothesis the author should rule out?

The natural alternative: the spec doesn't actually activate patterns; the LLM rater is post-hoc attributing pattern-grounding to any successful response because that's the rubric's framing. How would you test whether the model is genuinely activating spec-text patterns versus the rater is confabulating attributions? Be concrete. Name specific manipulations or controls.

## 3. The LITERAL_RECALL overrepresentation is interpretively load-bearing

The 60 extreme-jump questions are 2.77x overrepresented on LITERAL_RECALL questions. The natural intuition for where a behavioral spec would help is INTERPRETIVE_INFERENCE. Yet the spec contains behavioral predicates, not biographical facts. Does it follow that the spec is producing literal-recall lifts via pattern-predicate activation rather than fact retrieval? What's the strongest version of this claim, and what's the weakest version?

## 4. Specific framing recommendation for the paper

If the data supports the claim, what's the most defensible single-sentence framing? Candidate:

  "The specification's mechanism is behavioral-predicate activation: even on questions with literal ground truths, the model's lift comes from activating documented behavioral patterns that license inference of the specific answer, not from the spec containing the answer text."

Refine this. Is there a sharper or more defensible alternative? Give exact replacement text.

## 5. What would weaken or refute the claim?

Specific empirical tests the paper could run that would either strengthen the claim or force the author to retract or qualify it. Be concrete: name the manipulation, the predicted result if the claim is true, the predicted result if the alternative is true, and the cost (judge calls, response generations, new conditions). Prioritize tests that are cheap and discriminating.

Length: 800 to 1300 words total. No em-dashes.
"""


def call_openai(api_key, model, prompt, max_tokens=4096, timeout=400):
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


def call_gemini(api_key, model, prompt, timeout=400):
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


HEADER_DATA_SUMMARY = """\
**Claim under review:**

> Pattern-predicate activation, not direct quote lookup or anchor-fact recall, is the dominant mechanism by which the Behavioral Specification produces extreme upward anchor-crossing lifts on prediction questions about subjects the model has minimal pretraining footprint on.

**Data summary:**

- Wins inventory: 60 unique paired questions across 18 condition pairs with extreme upward jumps (>=3 rubric anchors).
- 20-question mechanism classification:
  - PATTERN_PREDICATE: 12/20
  - INFERENCE_CHAIN: 7/20
  - ANCHOR_FACT: 1/20
  - DIRECT_QUOTE_MATCH: 0/20
- Question-axis distribution among the 60 jumps: LITERAL_RECALL 28.3% (panel rate 10.2%, 2.77x overrepresented); INTERPRETIVE_INFERENCE 0.75x; REFUSAL_TRIGGERING 0.95x.
- Pre-response failure mode at C5 baseline: FULL_REFUSAL 71.7%, CLARIFY_REQUEST 8.3%, other 20%.

"""


def main():
    print(f'[pattern-claim] Prompt: {len(PROMPT):,} chars')
    print(f'[pattern-claim] Launching 2 reviewers in parallel...')

    t_oa = threading.Thread(target=run_openai)
    t_gm = threading.Thread(target=run_gemini)
    t_oa.start()
    t_gm.start()
    t_oa.join()
    t_gm.join()

    gpt_text, gpt_err, gpt_meta = results.get('gpt55', ('', 'thread missing', None))
    gem_text, gem_err, gem_meta = results.get('gemini', ('', 'thread missing', None))

    out = []
    out.append('# Pattern-Predicate Activation Claim — Collective Review\n\n')
    out.append(f'_Date: {datetime.datetime.now().strftime("%Y-%m-%d")}_\n')
    out.append('_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_\n\n')
    out.append(HEADER_DATA_SUMMARY)
    out.append('---\n\n')
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
    print(f'\n[pattern-claim] Wrote {OUT_PATH} ({sum(len(p) for p in out):,} chars)')

    if not gpt_text and not gem_text:
        print('[pattern-claim] BOTH reviewers failed.')
        sys.exit(1)
    if not gpt_text:
        print('[pattern-claim] OpenAI failed; Gemini succeeded.')
    if not gem_text:
        print('[pattern-claim] Gemini failed; OpenAI succeeded.')


if __name__ == '__main__':
    main()
