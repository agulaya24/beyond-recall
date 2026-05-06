"""
Beyond Recall v11 -- Gemini Pro retry for cursory review (2026-04-28).

Initial run failed: gemini-2.5-pro hit MAX_TOKENS at 6144 because thinking budget
consumed the entire output. Flash succeeded but truncated mid-issue.

This retry: gemini-2.5-pro with maxOutputTokens=16384 and thinkingBudget=0 to
disable thinking and let actual response come through. Fallback to higher
thinking + 24576 cap if that fails.

Output appended/replaced into the existing combined review markdown.
"""

import os
import sys
import json
import time
import re
import subprocess
import datetime
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


def call_gemini(api_key, model, prompt, max_output=16384, thinking_budget=0, timeout=600):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    gen_config = {
        'maxOutputTokens': max_output,
        'temperature': 0.3,
    }
    if thinking_budget is not None:
        gen_config['thinkingConfig'] = {'thinkingBudget': thinking_budget}
    body = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': gen_config,
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        cands = data.get('candidates', [])
        if not cands:
            return None, f'no candidates: {json.dumps(data)[:500]}', None
        finish = cands[0].get('finishReason', '')
        parts = cands[0].get('content', {}).get('parts', [])
        text = ''.join(p.get('text', '') for p in parts)
        usage = data.get('usageMetadata', {})
        if not text:
            return None, f'empty text (finish={finish}, usage={usage})', None
        return text, None, {'model': model, 'finish': finish, 'usage': usage}
    except urllib.error.HTTPError as e:
        return None, f'HTTPError {e.code}: {e.read().decode("utf-8", errors="replace")[:500]}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


def main():
    print(f'[gemini-retry] Paper: {len(PAPER_TEXT):,} chars')
    api_key = get_win_env('GEMINI_API_KEY')
    if not api_key:
        print('[gemini-retry] No GEMINI_API_KEY')
        sys.exit(1)

    # Try Pro with thinking disabled first; if that fails try with high thinking budget + bigger cap.
    attempts = [
        ('gemini-2.5-pro', 16384, 0),
        ('gemini-2.5-pro', 24576, 8192),
        ('gemini-2.5-pro', 32768, 16384),
    ]

    for model, max_out, think in attempts:
        print(f'[gemini-retry] trying {model} max_out={max_out} think={think}...')
        t0 = time.time()
        text, err, meta = call_gemini(api_key, model, PROMPT, max_output=max_out, thinking_budget=think, timeout=600)
        elapsed = time.time() - t0
        if text:
            print(f'[gemini-retry] {model} OK in {elapsed:.0f}s ({len(text)} chars), finish={meta.get("finish")}')
            break
        print(f'[gemini-retry] FAIL ({elapsed:.0f}s): {err[:300] if err else "no text"}')
    else:
        print('[gemini-retry] All attempts failed.')
        sys.exit(1)

    # Replace the Gemini section in the existing combined markdown.
    existing = OUT_PATH.read_text(encoding='utf-8')
    # Split on the divider before Reviewer 2.
    marker = '## Reviewer 2 -- Google'
    idx = existing.find(marker)
    if idx == -1:
        # No prior Gemini section; append.
        new_doc = existing + f'\n\n---\n\n## Reviewer 2 -- Google ({meta["model"]}, retry)\n\n{text}\n'
    else:
        # Keep everything up to (and including) the previous "---\n\n" before Gemini section start.
        head_end = existing.rfind('---', 0, idx)
        head = existing[:head_end + 4]  # include '---\n'
        new_doc = head + f'\n## Reviewer 2 -- Google ({meta["model"]}, retry; finish={meta.get("finish")})\n\n{text}\n'

    # Update headline counts based on new Gemini text.
    def count_issues(t):
        return len([1 for line in t.splitlines() if re.match(r'^##\s+Issue:', line)])

    def find_verdict(t):
        m = re.search(r'\b(READY-FOR-FREEZE|BLOCKING-ISSUES-\d+)\b', t)
        return m.group(1) if m else 'VERDICT NOT FOUND'

    gem_issues = count_issues(text)
    gem_verdict = find_verdict(text)
    print(f'[gemini-retry] Gemini issues: {gem_issues}, verdict: {gem_verdict}')

    # Patch headline lines.
    new_doc = re.sub(
        r'- \*\*Gemini verdict:\*\*.*\n',
        f'- **Gemini verdict:** {gem_verdict} ({gem_issues} issue headers; retry with thinking-budget tuned)\n',
        new_doc, count=1
    )

    OUT_PATH.write_text(new_doc, encoding='utf-8')
    print(f'[gemini-retry] Wrote updated {OUT_PATH} ({len(new_doc):,} chars)')


if __name__ == '__main__':
    main()
