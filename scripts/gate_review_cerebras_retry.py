"""
Retry Cerebras with a head+tail truncation to stay under TPM quota.
"""

import os, sys, json, subprocess, datetime, re, time, urllib.request, urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v8_draft.md'
RAW_PATH = REPO_ROOT / 'docs' / 'reviews' / 'full_paper_gate_review_20260422_173703.md'


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


GATE_PROMPT = """You are doing a gate review of a completed research paper draft before publication. The author wants a final check for factual errors, unsupported claims, internal contradictions, logical gaps, and residual voice issues. The paper has already been through multiple rounds of review; this is the final pass.

Paper title: "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization"

Focus ONLY on:
1. Load-bearing claims not supported by the data shown (cite section + quote)
2. Factual errors or internal contradictions across sections
3. Logical gaps in the argument
4. Remaining voice or marketing-register issues
5. Missing cross-references
6. Structural integrity

Do NOT recommend stylistic preferences, full rewrites, expansions, or §8 Future Work completeness.

Respond with these EXACT sections:

## (a) OVERALL GATE VERDICT
## (b) CRITICAL ISSUES
## (c) MINOR ISSUES
## (d) STRUCTURAL CONCERNS

Paper text (truncated head+tail for size limit):

---

{paper}
"""


def review_cerebras(paper_trunc, api_key):
    url = 'https://api.cerebras.ai/v1/chat/completions'
    payload = json.dumps({
        'model': 'qwen-3-235b-a22b-instruct-2507',
        'messages': [{'role': 'user', 'content': GATE_PROMPT.format(paper=paper_trunc)}],
        'temperature': 0.2,
        'max_tokens': 5000
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=420) as resp:
                data = json.loads(resp.read())
                text = data['choices'][0]['message']['content']
                print(f'  [Cerebras Qwen3 235B] done ({len(text)} chars)')
                return text
        except urllib.error.HTTPError as e:
            body = ''
            try: body = e.read().decode()[:500]
            except Exception: pass
            if e.code == 429 and attempt < 4:
                wait = 90
                print(f'  [Cerebras] rate limited (attempt {attempt+1}/5), waiting {wait}s...')
                time.sleep(wait)
            else:
                print(f'  [Cerebras] ERROR: {e.code}: {body}')
                return f'ERROR: {e.code}: {body}'
        except Exception as e:
            print(f'  [Cerebras] ERROR: {e}')
            return f'ERROR: {e}'
    return 'ERROR: all retries failed'


def main():
    cerebras_key = get_win_env('CEREBRAS_API_KEY')
    if not cerebras_key:
        print('No CEREBRAS_API_KEY')
        return
    paper = load_paper()
    # Aggressive truncation: head 40k + tail 30k = ~17.5k tokens content
    if len(paper) > 70000:
        paper_trunc = (
            paper[:40000]
            + '\n\n[...middle sections truncated for Cerebras TPM limit; review what is visible. Middle sections (approx. §3.6-§4.6) cover methodology details, main gradient results, compression, mechanism, memory-system composition — you may note that you did not see them...]\n\n'
            + paper[-30000:]
        )
    else:
        paper_trunc = paper
    print(f'Truncated paper to {len(paper_trunc)} chars (~{len(paper_trunc)//4} tokens)')
    print('Sending to Cerebras...')
    result = review_cerebras(paper_trunc, cerebras_key)

    existing = RAW_PATH.read_text(encoding='utf-8')
    # Replace the last Cerebras ERROR block with the new result
    addition = f'\n\n---\n\n# CEREBRAS RETRY (head+tail subset, ~17.5k tokens)\n\n## Cerebras Qwen3 235B (head+tail subset)\n\n{result}\n'
    RAW_PATH.write_text(existing + addition, encoding='utf-8')
    print(f'Appended to {RAW_PATH}')


if __name__ == '__main__':
    main()
