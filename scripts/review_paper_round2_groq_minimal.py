"""
Beyond Recall - Round 2 MINIMAL Groq-only review.
Groq free tier rejected 30k and 62k char payloads; this sends only the core
focus-area sections (abstract + 4.4 + 4.3.1 + 5.7 + 5.8) to stay under the limit.
"""

import os, json, subprocess, datetime, re, urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v6_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def extract(text, start, end=None):
    s = text.find(start)
    if s < 0: return ''
    if end:
        e = text.find(end, s + len(start))
        if e < 0: return text[s:]
        return text[s:e]
    return text[s:]


def build_minimal_payload():
    text = PAPER_PATH.read_text(encoding='utf-8')
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL).strip()

    parts = [
        '# Beyond Recall - Minimal Excerpts for Focused Round 2 Review\n',
        '[Editor note: These are ONLY the sections targeted by the Round 2 focus questions. Full paper sections 1-3 and most of 4-5 are not included. Answer based on what you see and note where you need more context.]\n',
        extract(text, '## Abstract', '## 1. Introduction'),
        extract(text, '### 4.3.1 A Proper Letta', '### 4.4 Base Layer'),
        extract(text, '### 4.4 Base Layer', '### 4.5 The Wrong-Spec'),
        extract(text, '### 5.7 A First Benchmark', '### 5.8 Architectural Convergence'),
        extract(text, '### 5.8 Architectural Convergence', '### 5.9 The Pipeline Is Anthropic-Family'),
    ]
    return '\n\n'.join(p.strip() for p in parts if p.strip())


PROMPT = """You are a rigorous peer reviewer for a research paper on arXiv. Be direct - not diplomatic.

The paper: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

Below are the CORE FOCUS SECTIONS of the revised Round 2 draft (Abstract + §4.3.1 Letta parity test + §4.4 BL positioning + §5.7 memory-provider axis + §5.8 Letta convergence). Other sections (methodology, related work, most of results, discussion) are NOT included. Answer based on what you see.

Please answer in EXACTLY this format:

## FOCUS-AREA ASSESSMENT

1. **§4.4 framing** - BL is positioned as a behavioral-spec layer with open-source retrieval floor, NOT as a 5th memory provider. Does this land honestly, or does it still read as defensive / conflict-of-interest?

2. **§5.7 framing** - "A First Benchmark on an Axis the Category Wasn't Optimized For" - fair referee or still biased?

3. **Abstract claim disaggregation** (tested / extrapolated / NOT claimed) - clear or muddled?

4. **§4.3.1 Letta parity (Haiku+Letta=3.24 vs Haiku+BL full-stack=3.04, Letta at 65% context)** - handled with humility appropriate for n=1 subject, or over/underclaimed?

5. **Any overclaiming in these sections** - call it out with quoted claim.

## CRITICAL ISSUES
## MINOR ISSUES
## VERDICT
One sentence assessment.

---

EXCERPTS:

{paper}
"""


def main():
    paper = build_minimal_payload()
    print(f'Minimal payload: {len(paper)} chars, ~{len(paper)//4} tokens')

    # Write payload for traceability
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    (REVIEWS_DIR / f'round_02_minimal_payload_{ts}.md').write_text(paper, encoding='utf-8')

    api_key = get_win_env('GROQ_API_KEY')
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': PROMPT.format(paper=paper)}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            print(f'[Groq] done ({len(text)} chars)')
    except Exception as e:
        text = f'ERROR: {e}'
        print(f'[Groq] {text}')

    out_path = REVIEWS_DIR / f'round_02_groq_minimal_{ts}.md'
    out = [
        '# Paper Review - Round 2 (Groq, Minimal Focus Sections)',
        f'_Generated: {ts}_',
        f'_Payload: Abstract + §4.3.1 + §4.4 + §5.7 + §5.8 ({len(paper)} chars)_',
        '',
        '---',
        '',
        '## Groq Llama 3.3 70B (minimal-focus-sections)',
        '',
        text,
    ]
    out_path.write_text('\n'.join(out), encoding='utf-8')
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    main()
