"""
Beyond Recall v11 -- FINAL CURSORY error-check (2026-04-28).

Author has scoped this as a CURSORY error-check, not a substantive review pass.
The paper is otherwise considered freeze-ready. Goal: catch GLARING errors,
numerical contradictions, internal inconsistencies, broken cross-references,
factual mistakes, undefined terms used in body text, em/en-dash violations,
and stale v10 / v10.1 references.

Reviewers: GPT-5.5 (OpenAI) + Gemini 2.5 Pro (Google) in parallel.
Smaller panel for cursory check; no Mistral / Cerebras / Groq this round.

Input:  docs/beyond_recall_v11_draft.md
Output: docs/reviews/v11_cursory_review_20260428.md
"""

import os
import sys
import json
import time
import re
import subprocess
import datetime
import threading
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_draft.md'
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'v11_cursory_review_20260428.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


PAPER_TEXT = PAPER_PATH.read_text(encoding='utf-8')

PROMPT_TEMPLATE = """You are giving a CURSORY error-check on the Beyond Recall v11 paper draft below. The author wants you to catch only GLARING issues that would prevent credible release. The paper is otherwise considered freeze-ready.

Author has explicitly stated:
- Past framing claims have been wrong; they want caution. They DO NOT want substantive framing recommendations.
- Mean Delta stays primary evaluation metric; per-question phenomena are CONTEXT, not headline.
- No "wins" terminology in paper prose.
- The wins-analysis pipeline is complete; do not relitigate mechanism debates.

In scope (flag these):
- Numerical contradictions (one section says X, another section says Y for the same number)
- Broken cross-references (section pointer points to wrong section, or to a removed section)
- Undefined terms used in body text without prior definition
- Factual mistakes (e.g., wrong citation, wrong year, wrong subject's nationality)
- Internal inconsistencies in claim language
- Claims with em-dashes or en-dashes (the paper has a no-em-dash rule)
- Stale references to v10 / v10.1 specific numbers in places that should now reflect v11

NOT in scope (DO NOT flag):
- Framing preferences
- Structural restructure suggestions
- "I would write this more like..." commentary
- Mechanism speculation
- Recommendations to add new analyses
- Recommendations to change which sections lead the paper
- Anything that would require substantive revision

Use markdown headers for each issue. Format:

## Issue: [one-line summary]
- **Section:** [section name + line number if visible]
- **Verbatim quote:** [paste the offending text]
- **Issue:** [explain what's wrong, briefly]
- **Recommended fix:** [exact replacement text or "remove" or "verify number"]

After the issue list, give a single-line verdict:
- READY-FOR-FREEZE if no glaring issues
- BLOCKING-ISSUES-N if N issues prevent freeze (state N)

Length: terse. 800-1500 words total. Cap each issue at ~100 words.

If you have nothing substantive to flag, say so. The author is fine with a short report.

PAPER BEGINS:

{paper}
"""

PROMPT = PROMPT_TEMPLATE.format(paper=PAPER_TEXT)


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
        'generationConfig': {'maxOutputTokens': 6144, 'temperature': 0.3},
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
        if not text:
            return None, f'empty text: {json.dumps(data)[:500]}', None
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
        text, err, meta = call_openai(api_key, model, PROMPT, max_tokens=4096, timeout=500)
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
        text, err, meta = call_gemini(api_key, model, PROMPT, timeout=500)
        elapsed = time.time() - t0
        if text:
            print(f'[gemini] {model} OK in {elapsed:.0f}s ({len(text)} chars)')
            results['gemini'] = (text, None, meta)
            return
        print(f'[gemini] {model} FAIL ({elapsed:.0f}s): {err[:200] if err else "no text"}')
    results['gemini'] = ('', 'all Gemini candidates failed', None)


def extract_issue_titles(text):
    """Pull '## Issue: ...' lines out of a reviewer response for convergence detection."""
    if not text:
        return []
    titles = []
    for line in text.splitlines():
        m = re.match(r'^##\s+Issue:\s*(.+?)\s*$', line)
        if m:
            titles.append(m.group(1).strip())
    return titles


def count_issues(text):
    return len(extract_issue_titles(text))


def find_verdict(text):
    if not text:
        return 'NO RESPONSE'
    m = re.search(r'\b(READY-FOR-FREEZE|BLOCKING-ISSUES-\d+)\b', text)
    return m.group(1) if m else 'VERDICT NOT FOUND'


def detect_convergence(gpt_text, gem_text):
    """Naive convergence: any two issue titles that share three or more lowercase tokens >= 4 chars."""
    if not gpt_text or not gem_text:
        return []
    gpt_titles = extract_issue_titles(gpt_text)
    gem_titles = extract_issue_titles(gem_text)
    convergent = []
    for gt in gpt_titles:
        gt_tokens = {t.lower() for t in re.findall(r'\w+', gt) if len(t) >= 4}
        for mt in gem_titles:
            mt_tokens = {t.lower() for t in re.findall(r'\w+', mt) if len(t) >= 4}
            shared = gt_tokens & mt_tokens
            if len(shared) >= 3:
                convergent.append((gt, mt, sorted(shared)))
                break
    return convergent


def main():
    print(f'[cursory-v11] Paper: {len(PAPER_TEXT):,} chars')
    print(f'[cursory-v11] Prompt: {len(PROMPT):,} chars')
    print(f'[cursory-v11] Launching 2 reviewers in parallel...')

    t_oa = threading.Thread(target=run_openai)
    t_gm = threading.Thread(target=run_gemini)
    t_oa.start()
    t_gm.start()
    t_oa.join()
    t_gm.join()

    gpt_text, gpt_err, gpt_meta = results.get('gpt55', ('', 'thread missing', None))
    gem_text, gem_err, gem_meta = results.get('gemini', ('', 'thread missing', None))

    gpt_issue_count = count_issues(gpt_text)
    gem_issue_count = count_issues(gem_text)
    gpt_verdict = find_verdict(gpt_text)
    gem_verdict = find_verdict(gem_text)
    convergent = detect_convergence(gpt_text, gem_text)

    out = []
    out.append('# Beyond Recall v11 -- Final Cursory Review\n\n')
    out.append(f'_Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}_\n')
    out.append(f'_Paper: `docs/beyond_recall_v11_draft.md` ({len(PAPER_TEXT):,} chars)_\n')
    out.append(f'_Reviewers: GPT-5.5 (or fallback), Gemini 2.5 Pro (or fallback)_\n')
    out.append(f'_Scope: cursory error-check only -- glaring numerical/cross-ref/factual issues. Not a substantive review._\n\n')

    out.append('## Headline\n\n')
    out.append(f'- **OpenAI verdict:** {gpt_verdict} ({gpt_issue_count} issue headers)\n')
    out.append(f'- **Gemini verdict:** {gem_verdict} ({gem_issue_count} issue headers)\n')
    out.append(f'- **Convergent issues (heuristic title match):** {len(convergent)}\n\n')

    out.append('## Convergent issues\n\n')
    if convergent:
        for gt, mt, shared in convergent:
            out.append(f'- GPT: "{gt}"  /  Gemini: "{mt}"  (shared tokens: {", ".join(shared)})\n')
        out.append('\n')
    else:
        out.append('_No heuristic convergence detected on issue titles. Compare full responses below for substantive overlap._\n\n')

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
    print(f'\n[cursory-v11] Wrote {OUT_PATH} ({sum(len(p) for p in out):,} chars)')
    print(f'[cursory-v11] OpenAI: {gpt_verdict} ({gpt_issue_count} issues)')
    print(f'[cursory-v11] Gemini: {gem_verdict} ({gem_issue_count} issues)')
    print(f'[cursory-v11] Convergent (heuristic): {len(convergent)}')

    if not gpt_text and not gem_text:
        print('[cursory-v11] BOTH reviewers failed.')
        sys.exit(1)
    if not gpt_text:
        print('[cursory-v11] OpenAI failed; Gemini succeeded.')
    if not gem_text:
        print('[cursory-v11] Gemini failed; OpenAI succeeded.')


if __name__ == '__main__':
    main()
