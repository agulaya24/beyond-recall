"""
Beyond Recall — §4 Results Restructuring Review (Mistral + Gemini 2.5 Pro)

Sends the full v9 §4 body plus the author's non-negotiable structural decisions
and the 5 open formatting questions to Mistral Large and Gemini 2.5 Pro. Saves
raw responses for synthesis.

Usage:
    python review_section4_structure.py
"""

import json
import os
import subprocess
import sys
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
V9_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v9_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

# §4 spans lines 561-1511 in v9 (verified)
SECTION4_START_LINE = 561
SECTION4_END_LINE = 1511


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_section4():
    text = V9_PATH.read_text(encoding='utf-8')
    lines = text.splitlines()
    # 1-indexed slice
    body = '\n'.join(lines[SECTION4_START_LINE - 1:SECTION4_END_LINE])
    return body


PROMPT_TEMPLATE = """You are advising on the FORMATTING of Section 4 (Results) of a research paper titled "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization."

The author has made several structural decisions ALREADY. These are NOT open for debate. Do not argue against them. Only advise on FORMATTING and SUB-ORGANIZATION given these decisions.

## AUTHOR'S NON-NEGOTIABLE DECISIONS (accept as given)

1. All memory-provider results (Mem0, Supermemory, Zep, Base Layer) stay IN ONE SECTION together. No per-system top-level headings in §4.4.
2. Letta is the ONE exception. It breaks out because it has unique additional testing (archival-retrieval path + stateful-agent self-editing path) and an architecturally distinct memory model.
3. §4.6 "Interpretation vs. Recall" content folds INTO §4.4 (not its own section).
4. Keckley Q21 cross-system refusal stays as a named subsection. Place it within §4.4.
5. §4.5 Robustness moves to END of Results (after the consolidated §4.4 + the Letta §4.7 block).
6. §4.8 Scaling and Practical Implications moves OUT of Results entirely, into Discussion as §5.5 Practical Implications.

DO NOT relitigate any of the six points above. Advise only on the five formatting questions below.

## THE FIVE FORMATTING QUESTIONS

Q1. Within the consolidated §4.4, should per-system results be presented as:
    (a) one flat per-system comparison table plus unified discussion prose,
    (b) a comparison table plus per-system "micro-paragraphs" (1-2 sentences each), or
    (c) something else?

Q2. Where does the Keckley Q21 cross-system refusal sit? Inside §4.4 as a dedicated subsection (e.g. §4.4.2 or §4.4.3), or somewhere else within §4.4?

Q3. Should the §4.6 Pattern 1 / Pattern 2 / Pattern 3 (cross-system mechanism reproduction) content be:
    (a) integrated into §4.4 as a "common mechanisms" subsection,
    (b) pulled forward to §4.3 as an extension of the wrong-spec mechanism section, or
    (c) preserved as §4.4.x its own subsection with reference to per-system variation?

Q4. Given §4.4 will now carry Mem0 + Supermemory + Zep + Base Layer + cross-system mechanisms + Keckley Q21, what is the best subsection ORDERING for reader flow?

Q5. Is there anything in the current §4.4 or §4.6 that should be moved to an APPENDIX instead of integrated (the author prefers a tight body)?

## REQUIRED OUTPUT FORMAT

Respond in exactly this structure:

### Q1. Table format within §4.4
[2-4 sentences. Pick (a), (b), or (c) and say why. No hedging.]

### Q2. Placement of Keckley Q21
[2-4 sentences.]

### Q3. Placement of Pattern 1/2/3 cross-system mechanism analysis
[2-4 sentences. Pick (a), (b), or (c) and say why.]

### Q4. Subsection ordering for reader flow
[One-paragraph justification plus the ordered list.]

### Q5. Appendix candidates
[Bullet list of specific subsections / paragraphs / tables that should go to appendix, or "none" with reasoning.]

### RECOMMENDED SUBSECTION TREE
[Provide a single concrete tree. Format:
§4.1 Title — one-line purpose
§4.2 Title — one-line purpose
§4.3 Title — one-line purpose
§4.4 Title — one-line purpose
  §4.4.1 Title — one-line purpose
  §4.4.2 Title — one-line purpose
  ...
§4.5 Title — one-line purpose
  §4.5.1 Title — one-line purpose
  ...
§4.6 Title — one-line purpose
  ...

Remember: §4.7 Letta stateful-agent breaks out (non-negotiable #2). §4.8 moves out entirely (non-negotiable #6). §4.5 Robustness moves to END of Results (non-negotiable #5). Reflect all of these in the tree. Use whatever final section number is natural for Robustness given it is last.]

### SINGLE BIGGEST RISK WITH THIS RESTRUCTURE
[2-3 sentences. What is the most important thing the author might get wrong when executing this?]

---

## CURRENT §4 RESULTS (v9 draft)

{section4_body}

---

End of §4. Respond in the required output format above. Do not argue against the six non-negotiable decisions.
"""


def review_mistral(prompt_content, api_key):
    import urllib.request
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt_content}],
        'temperature': 0.3,
        'max_tokens': 16384
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            finish = data['choices'][0].get('finish_reason', 'unknown')
            print(f'  [Mistral Large] done ({len(text)} chars, finish_reason={finish})')
            return {'Mistral Large': text, '_mistral_finish_reason': finish}
    except Exception as e:
        print(f'  [Mistral] ERROR: {e}')
        return {'Mistral Large': f'ERROR: {e}'}


def review_gemini_pro(prompt_content, api_key):
    import urllib.request, urllib.error
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': prompt_content}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 16384}
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            cand = data['candidates'][0]
            text = cand['content']['parts'][0]['text']
            finish = cand.get('finishReason', 'unknown')
            print(f'  [Gemini 2.5 Pro] done ({len(text)} chars, finishReason={finish})')
            return {'Gemini 2.5 Pro': text, '_gemini_finish_reason': finish}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()[:500]
        print(f'  [Gemini 2.5 Pro] HTTP {e.code}: {err_body}')
        return {'Gemini 2.5 Pro': f'ERROR: HTTP {e.code}: {err_body}'}
    except Exception as e:
        print(f'  [Gemini 2.5 Pro] ERROR: {e}')
        return {'Gemini 2.5 Pro': f'ERROR: {e}'}


def save_raw_responses(prompt, responses):
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f's114_section4_raw_responses_{ts}.md'
    lines = ['# V9 §4 Structure Review — Raw Responses', f'_Generated: {ts}_\n']
    lines.append(f'_Prompt length: {len(prompt)} chars_\n')
    lines.append('---\n\n## PROMPT SENT TO BOTH REVIEWERS\n\n')
    lines.append('```\n' + prompt + '\n```\n')
    for model, review in responses.items():
        if model.startswith('_'):
            continue
        lines.append(f'\n---\n\n## {model} Raw Response\n\n{review}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved raw: {out_path}')
    return out_path


def main():
    print('Loading API keys from Windows env...')
    gemini_key = get_win_env('GEMINI_API_KEY')
    mistral_key = get_win_env('MISTRAL_API_KEY')

    if not gemini_key:
        print('Missing GEMINI_API_KEY')
        sys.exit(1)
    if not mistral_key:
        print('Missing MISTRAL_API_KEY')
        sys.exit(1)

    print('Loading §4 body from v9 draft...')
    section4 = load_section4()
    full_prompt = PROMPT_TEMPLATE.format(section4_body=section4)
    print(f'§4 body: {len(section4)} chars')
    print(f'Full prompt: {len(full_prompt)} chars (~{len(full_prompt)//4} tokens)\n')

    responses = {}

    print('Sending to Mistral Large...')
    responses.update(review_mistral(full_prompt, mistral_key))

    print('Sending to Gemini 2.5 Pro...')
    responses.update(review_gemini_pro(full_prompt, gemini_key))

    raw_path = save_raw_responses(full_prompt, responses)
    print(f'\nDone. Raw responses file: {raw_path}')


if __name__ == '__main__':
    main()
