"""
Beyond Recall v11 -- Round 2 review of framing-implications report (2026-04-28).

Sends the Round 1 framing report (docs/reviews/framing_implications_20260428.md)
to GPT-5.5 + Gemini 2.5 Pro in parallel for triangulation. The reviewers see
the framing report only, not the paper itself.

Output: docs/reviews/framing_report_round2_review_20260428.md
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
REPORT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'framing_implications_20260428.md'
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'framing_report_round2_review_20260428.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


REPORT_TEXT = REPORT_PATH.read_text(encoding='utf-8')

PROMPT = f"""You are reviewing a framing-implications report on the Beyond Recall paper. The report proposes specific paper-level changes based on a wins-analysis investigation. Your job is to assess whether the proposed pivots are justified by the evidence cited in the report.

Author context:
- Past framing claims have been wrong; caution is the operating principle
- Mean Δ stays the primary evaluation metric; per-question phenomena are CONTEXT, not headline
- The terminology "wins" is not used in paper prose -- replaced with "increases in representational accuracy" or "extreme upward anchor crossings"
- Predicate ablation experiments will run as Phase 2c; results land in appendix

Please answer each question in order using markdown headers.

## 1. Are the 5 APPLY-AS-DRAFTED iterative refinements (Refinements 1-5) justified by evidence?

Refinement 1: §4.2 "What the aggregate numbers hide" subsection
Refinement 2: §4.2 mean Δ numerical reconciliation
Refinement 3: §4.4.2 strengthen Pattern 1/2/3 with Spearman ρ
Refinement 4: §3.6 add half-anchor metric note
Refinement 5: Appendix B Hamerton-leverage at per-question grain

For each, briefly state: justified / partially-justified / not-justified, and one-sentence reason.

## 2. Refinement 6 (cautious mechanism description) -- is REFINE-FIRST the right disposition?

The deeper analysis falsified the heuristic-level pattern-activation claim. The narrower claim that survives is 11 of 60 INFERENCE_CHAIN cases with verdict genuine_inference_via_spec. Should the paper add a body-text statement about even this narrow claim? Or is HOLD-FOR-PHASE-2C-RESULTS the right call?

## 3. Pivot 7 (strong mechanism description, PHASE-2C-DEPENDENT) -- is the pre-condition correctly framed?

The pivot says "the mechanism is predicate activation, not retrieval" should only be added if predicate ablation experiments survive. Is this the right pre-condition? What would the experiments need to show specifically?

## 4. Pivot 8 (two-mechanism story, APPLY-AS-DRAFTED) -- strongest claim?

The two-mechanism story is grounded in Spearman ρ split: spec-on-baseline ρ=0.27 vs spec-on-info-rich ρ≈0.71. The framing report says this is the strongest pivot in the set. Do you agree? What's the strongest objection? Should this enter the paper as a body-text claim or remain a footnote / appendix?

## 5. What's missing from the framing report?

Specific gaps:
- Are there evidence streams the report doesn't address?
- Are there alternative explanations for the data not surfaced?
- Are there pivots that should be added or removed?
- Is the risk treatment honest, or defensive?

## 6. What's overclaimed in the framing report?

Specific instances of language that exceeds what the evidence supports.

## 7. Strongest single objection to the report's overall stance

If you had to flag one thing for the author to reconsider, what is it?

Length: 1500-2500 words total. Be direct. The author wants honest direction, not validation.

REPORT BEGINS:

{REPORT_TEXT}
"""


def call_openai(api_key, model, prompt, max_tokens=8192, timeout=600):
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


def call_gemini(api_key, model, prompt, timeout=600):
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
        text, err, meta = call_openai(api_key, model, PROMPT, max_tokens=8192, timeout=600)
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
        text, err, meta = call_gemini(api_key, model, PROMPT, timeout=600)
        elapsed = time.time() - t0
        if text:
            print(f'[gemini] {model} OK in {elapsed:.0f}s ({len(text)} chars)')
            results['gemini'] = (text, None, meta)
            return
        print(f'[gemini] {model} FAIL ({elapsed:.0f}s): {err[:200] if err else "no text"}')
    results['gemini'] = ('', 'all Gemini candidates failed', None)


def main():
    print(f'[round2-framing] Report: {len(REPORT_TEXT):,} chars')
    print(f'[round2-framing] Prompt: {len(PROMPT):,} chars')
    print(f'[round2-framing] Launching 2 reviewers in parallel...')

    t_oa = threading.Thread(target=run_openai)
    t_gm = threading.Thread(target=run_gemini)
    t_oa.start()
    t_gm.start()
    t_oa.join()
    t_gm.join()

    gpt_text, gpt_err, gpt_meta = results.get('gpt55', ('', 'thread missing', None))
    gem_text, gem_err, gem_meta = results.get('gemini', ('', 'thread missing', None))

    out = []
    out.append(f'# Framing-Implications Report -- Round 2 Cross-LLM Review\n\n')
    out.append(f'_Date: {datetime.datetime.now().strftime("%Y-%m-%d")}_\n')
    out.append(f'_Source report: `docs/reviews/framing_implications_20260428.md`_\n')
    out.append(f'_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_\n\n')
    out.append('---\n\n')
    out.append(f'## Reviewer 1 -- OpenAI ({gpt_meta.get("model") if gpt_meta else "FAILED"})\n\n')
    if gpt_text:
        out.append(gpt_text)
    else:
        out.append(f'_FAILED: {gpt_err}_\n')
    out.append('\n\n---\n\n')
    out.append(f'## Reviewer 2 -- Google ({gem_meta.get("model") if gem_meta else "FAILED"})\n\n')
    if gem_text:
        out.append(gem_text)
    else:
        out.append(f'_FAILED: {gem_err}_\n')
    out.append('\n')

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(''.join(out), encoding='utf-8')
    print(f'\n[round2-framing] Wrote {OUT_PATH} ({sum(len(p) for p in out):,} chars)')

    if not gpt_text and not gem_text:
        print('[round2-framing] BOTH reviewers failed.')
        sys.exit(1)
    if not gpt_text:
        print('[round2-framing] OpenAI failed; Gemini succeeded.')
    if not gem_text:
        print('[round2-framing] Gemini failed; OpenAI succeeded.')


if __name__ == '__main__':
    main()
