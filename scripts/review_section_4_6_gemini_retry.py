"""Retry Gemini 2.5 Pro and Flash for §4.6 review with more tokens and thinkingConfig."""
import json, subprocess, urllib.request, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAYLOAD_PATH = REPO_ROOT / 'docs' / 'reviews' / '_section_4_6_payload.md'
OUT_PATH = REPO_ROOT / 'docs' / 'reviews' / 'section_4_6_gemini_retry.md'


def get_win_env(key):
    r = subprocess.run(['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
                       capture_output=True, text=True)
    return r.stdout.strip()


PROMPT = """You are reviewing §4.6 of a research paper titled "Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization." The section is included below. The paper studies whether a compact behavioral specification can improve AI prediction of how a specific person would respond in novel situations, on top of commercial memory systems (Mem0, Letta, Zep, Supermemory) and an open-source retrieval substrate (Base Layer).

§4.6 Interpretation vs. Recall is the per-question analysis section. Prior sections §4.4 and §4.5 established aggregate numbers per memory system and confirmed robustness across judges and response models. §4.6 is where the paper looks inside the aggregates and explains what's producing them at the per-question level.

Please review §4.6 for:

1. **Understandability.** Is the opening paragraph clear to a reader who has read §1 through §4.5? Does the plain-language explanation of the per-question distribution land, or does it still read as jargon?
2. **Logic.** Are the three mechanisms (pattern supply, over-theorization, structural refusal) clearly distinguished? Does the cross-system reproduction claim hold up given the evidence presented?
3. **Keckley Q21 framing.** Is the "single cleanest cross-substrate replication" claim well-supported by the table? Is the interpretation (property of the specification, not the memory system) defensible?
4. **Table readability.** Does the per-subject paired-delta table communicate "every row is a mixture" effectively? Any columns that should be reordered or dropped?
5. **Logical gaps or claims not supported.** Any sentence in §4.6 that a skeptical reader would flag as unsupported by the data shown?
6. **Voice issues.** Any remaining jargon, GTM-style verbs ("beats", "crushes", "dominates"), em-dashes in prose, or sentences that sound like marketing rather than research.
7. **What's missing.** Any per-question framing question that a reader would expect §4.6 to address but doesn't.

Respond with (a) overall grade A/B/C/D/F for intelligibility and logic, (b) top 3 fixable issues in priority order, (c) anything that would require an expanded experiment to resolve (these go to §8 Future Work; not in scope for §4.6 rewrite).

Keep your response under 1500 words. Be direct.

§4.6 text follows:

{payload}
"""


def call_gemini(model_id, payload, api_key, max_out=8192, thinking_budget=0):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}'
    gen_cfg = {'temperature': 0.3, 'maxOutputTokens': max_out}
    # Attempt to disable "thinking" on Gemini 2.5 Pro by setting thinkingBudget=0 where supported.
    if thinking_budget is not None:
        gen_cfg['thinkingConfig'] = {'thinkingBudget': thinking_budget}
    body = json.dumps({
        'contents': [{'parts': [{'text': PROMPT.format(payload=payload)}]}],
        'generationConfig': gen_cfg
    }).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return f'ERROR (transport): {e}', {}
    try:
        cand = data['candidates'][0]
        if 'content' not in cand or 'parts' not in cand.get('content', {}):
            finish = cand.get('finishReason', '?')
            return f'ERROR (no parts): finishReason={finish}; full={json.dumps(data)[:800]}', data
        parts = cand['content']['parts']
        text = '\n'.join(p.get('text', '') for p in parts if 'text' in p)
        return text, data
    except Exception as e:
        return f'ERROR (parse): {e}; raw={json.dumps(data)[:500]}', data


def main():
    api_key = get_win_env('GEMINI_API_KEY')
    if not api_key:
        print('no GEMINI_API_KEY')
        return
    payload = PAYLOAD_PATH.read_text(encoding='utf-8').strip()
    print(f'payload: {len(payload)} chars')

    out = ['# Gemini retry for §4.6 review\n', f'_Generated: {datetime.datetime.now().isoformat()}_\n']

    # Pro: allow thinking but with much larger max output so thinking + reply fit
    print('Gemini 2.5 Pro (max_out=16384, thinking_budget=-1 dynamic)...')
    text_pro, raw_pro = call_gemini('gemini-2.5-pro', payload, api_key, max_out=16384, thinking_budget=-1)
    print(f'  got {len(text_pro)} chars')
    out.append(f'\n---\n\n## Gemini 2.5 Pro\n\n{text_pro}\n')

    # Flash: retry with larger cap
    print('Gemini 2.5 Flash (max_out=8192, thinking_budget=0 disabled)...')
    text_flash, raw_flash = call_gemini('gemini-2.5-flash', payload, api_key, max_out=8192, thinking_budget=0)
    print(f'  got {len(text_flash)} chars')
    out.append(f'\n---\n\n## Gemini 2.5 Flash\n\n{text_flash}\n')

    OUT_PATH.write_text('\n'.join(out), encoding='utf-8')
    print(f'Saved: {OUT_PATH}')


if __name__ == '__main__':
    main()
