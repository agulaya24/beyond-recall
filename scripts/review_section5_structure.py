"""
Beyond Recall v11.6 — §5 Structural Decision Cross-LLM Review
==============================================================
Sends the proposed §5 structural restructure (cold-read outline + drift diff)
plus the current §5, anchoring paper context (§1.3 headlines, §4.7 bridge,
Appendix B.10), confidence catalog, and prior §1-4 review synthesis to four
frontier reviewers. Saves a single review file with one section per reviewer
plus a synthesis paragraph.

Reviewers
---------
1. Mistral Large       (env MISTRAL_API_KEY)
2. GPT-5.5             (env OPENAI_API_KEY) -- model id: gpt-5.5
3. Gemini 2.5 Pro      (env GEMINI_API_KEY) -- retry after §1-4 503
4. Claude Opus 4.7     (env ANTHROPIC_API_KEY) -- model id: claude-opus-4-7

Constraints
-----------
- 5-minute (300s) hard timeout per call. On failure log and skip; no retry loops.
- Strip HTML comments before sending.
- Line ranges anchored to v11.6 (verified): §5 = 1503-1718, §4.7+bridge = 1472-1500,
  §1.3 headlines = 100-135, Appendix B.10 = 2205-2230.

Output
------
- docs/reviews/round_v11_6_section5_structure_<timestamp>.md
"""

import os
import sys
import json
import re
import subprocess
import datetime
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v11_6_draft.md'
CATALOG_PATH = REPO_ROOT / 'docs' / 'research' / 'v11_confidence_catalog_20260428.md'
COLD_READ_OUTLINE_PATH = REPO_ROOT / 'docs' / 'reviews' / 's5_independent_outline_20260501.md'
COLD_READ_DIFF_PATH = REPO_ROOT / 'docs' / 'reviews' / 's5_drift_diff_20260501.md'
PRIOR_REVIEW_PATH = REPO_ROOT / 'docs' / 'reviews' / 'round_v11_5_sections_1_4_20260501_141341.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
REVIEWS_DIR.mkdir(exist_ok=True)

# v11.6 verified line ranges
S5_START, S5_END = 1503, 1718
S4_BRIDGE_START, S4_BRIDGE_END = 1472, 1500
S1_3_START, S1_3_END = 100, 135
B10_START, B10_END = 2205, 2230

CALL_TIMEOUT_SECONDS = 300


def get_win_env(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
            capture_output=True, text=True, timeout=15
        )
        return r.stdout.strip()
    except Exception:
        return ''


def strip_html_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)


def slice_lines(path, start, end):
    """Return inclusive 1-indexed line slice from a text file, comments stripped."""
    raw = path.read_text(encoding='utf-8')
    lines = raw.splitlines()
    chunk = '\n'.join(lines[start - 1:end])
    return strip_html_comments(chunk).strip()


def load_full_file(path):
    return strip_html_comments(path.read_text(encoding='utf-8')).strip()


REVIEW_PROMPT = """You are reviewing a structural decision for §5 (Discussion) of a research paper. The paper's first four sections have been written and locked; the Discussion has not. The cold-read agent has proposed restructuring §5 from 6 to 8 subsections. The author wants external opinion before committing.

The paper is: "Beyond Recall: Behavioral Specification as the Missing Primitive for AI Personalization"

Read the inputs below and provide structured feedback in this exact format:

## OVERALL VERDICT
One paragraph: does the proposed §5 structure follow appropriately from §1-4 as locked? Is it the right move, the wrong move, or partially-right?

## STRUCTURAL ASSESSMENT
For each proposed subsection, comment on whether it is necessary, well-scoped, in the right order, and well-anchored to §1-4 evidence:
- §5.1 Synthesis lede
- §5.2 Gradient + population-of-relevance
- §5.3 Retrieval is not interpretation (NEW)
- §5.4 Composition with retrieval
- §5.5 Architectural ceilings via Letta (NEW)
- §5.6 Wrong-spec mechanism + hedging
- §5.7 Compression and deployment tractability
- §5.8 Closing argument

## MISSING FROM PROPOSED STRUCTURE
What discussion threads §1-4 demand that the proposed §5 outline does not carry. Cite §X.Y back-references.

## OVERREACH IN PROPOSED STRUCTURE
What the proposed structure goes beyond what §1-4 evidence supports. Reference confidence catalog where relevant.

## ALTERNATIVE STRUCTURES
If a different §5 structure would serve the data better, sketch it here. Otherwise say "the proposed structure is the right one."

## SPECIFIC CONCERNS ABOUT THE TWO NEW SUBSECTIONS
- §5.3 Retrieval is not interpretation: this carries the 7th headline (post-hoc finding). Should it be a §5 subsection at all? At what evidentiary weight?
- §5.5 Architectural ceilings via Letta: this rests on N=3 exploratory data. Should it be a full §5 subsection or a paragraph elsewhere?

## SPECIFIC CONCERNS ABOUT THE TWO CUTS/MOVES
- §5.1 Anti-Pattern dropped: appropriate, or should it be retained in some form?
- §5.5 Practical Implications cut by ~60%, production-architecture proposals to §7: appropriate, or does §5 need to retain more deployment discussion?

## SINGLE MOST IMPORTANT FIX
If only one structural change can be made, which one and why?

Be direct. Not diplomatic. If the structure is right, say so. If wrong, say what's wrong specifically.

---

INPUTS:

[Current §5 (lines {s5_start}-{s5_end} of v11.6 draft)]

{current_s5}

---

[Cold-read independent outline -- proposed §5 structure with per-subsection rationale]

{cold_read_outline}

---

[Cold-read drift diff -- analysis of what is missing/stale/overweighted in current §5 vs proposed]

{cold_read_diff}

---

[Paper context: §1.3 seven headline findings, §4.7 §4-summary bridge, Appendix B.10 pre-registered vs post-hoc table]

### §1.3 Seven headlines (v11.6 lines {s13_start}-{s13_end})

{s1_3}

### §4.7 Summary of §4 and bridge to discussion (v11.6 lines {s47_start}-{s47_end})

{s4_bridge}

### Appendix B.10 Pre-registered vs post-hoc analyses (v11.6 lines {b10_start}-{b10_end})

{appendix_b10}

---

[Confidence catalog -- evidentiary tiers for every claim in the paper]

{confidence_catalog}

---

[Prior multi-LLM §1-4 review -- context on critical issues already flagged and being fixed in §1-4. Read for what reviewers thought of the locked §1-4, NOT to repeat their §1-4 critique here.]

{prior_review_synthesis}
"""


def _http_post_json(url, payload, headers, timeout):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'python-urllib/3',
        **headers,
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def review_mistral(prompt_text, api_key):
    label = 'Mistral Large'
    url = 'https://api.mistral.ai/v1/chat/completions'
    payload = {
        'model': 'mistral-large-latest',
        'messages': [{'role': 'user', 'content': prompt_text}],
        'temperature': 0.3,
        'max_tokens': 8192,
    }
    headers = {'Authorization': f'Bearer {api_key}'}
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, headers, timeout=CALL_TIMEOUT_SECONDS)
        text = data['choices'][0]['message']['content']
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:300]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_openai(prompt_text, api_key):
    label = 'GPT-5.5'
    url_responses = 'https://api.openai.com/v1/responses'
    payload_responses = {
        'model': 'gpt-5.5',
        'input': prompt_text,
        'max_output_tokens': 8192,
    }
    headers = {'Authorization': f'Bearer {api_key}'}
    t0 = time.time()
    try:
        data = _http_post_json(url_responses, payload_responses, headers, timeout=CALL_TIMEOUT_SECONDS)
        text_parts = []
        if 'output_text' in data and isinstance(data['output_text'], str):
            text_parts.append(data['output_text'])
        else:
            for item in data.get('output', []):
                for c in item.get('content', []):
                    if c.get('type') in ('output_text', 'text'):
                        text_parts.append(c.get('text', ''))
        text = '\n'.join(p for p in text_parts if p).strip()
        if not text:
            text = json.dumps(data)[:2000]
        elapsed = time.time() - t0
        print(f'  [{label}] ok via Responses API ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        print(f'  [{label}] Responses API failed ({e.code}): {body[:200]}; trying chat.completions')
    except Exception as e:
        print(f'  [{label}] Responses API failed: {type(e).__name__}: {e}; trying chat.completions')

    url_chat = 'https://api.openai.com/v1/chat/completions'
    payload_chat = {
        'model': 'gpt-5.5',
        'messages': [{'role': 'user', 'content': prompt_text}],
        'max_completion_tokens': 8192,
    }
    t0 = time.time()
    try:
        data = _http_post_json(url_chat, payload_chat, headers, timeout=CALL_TIMEOUT_SECONDS)
        text = data['choices'][0]['message']['content']
        elapsed = time.time() - t0
        print(f'  [{label}] ok via chat.completions ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_gemini(prompt_text, api_key):
    label = 'Gemini 2.5 Pro'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}'
    payload = {
        'contents': [{'parts': [{'text': prompt_text}]}],
        'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8192},
    }
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, {}, timeout=CALL_TIMEOUT_SECONDS)
        candidates = data.get('candidates', [])
        if not candidates:
            msg = f'ERROR: no candidates returned. Response: {json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        parts = candidates[0].get('content', {}).get('parts', [])
        text = '\n'.join(p.get('text', '') for p in parts).strip()
        if not text:
            fr = candidates[0].get('finishReason', 'UNKNOWN')
            msg = f'ERROR: empty text (finishReason={fr}). Raw: {json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def review_anthropic(prompt_text, api_key):
    label = 'Claude Opus 4.7'
    url = 'https://api.anthropic.com/v1/messages'
    payload = {
        'model': 'claude-opus-4-7',
        'max_tokens': 8192,
        'messages': [{'role': 'user', 'content': prompt_text}],
    }
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
    }
    t0 = time.time()
    try:
        data = _http_post_json(url, payload, headers, timeout=CALL_TIMEOUT_SECONDS)
        blocks = data.get('content', [])
        text = '\n'.join(b.get('text', '') for b in blocks if b.get('type') == 'text').strip()
        if not text:
            msg = f'ERROR: empty text. stop_reason={data.get("stop_reason")} raw={json.dumps(data)[:500]}'
            print(f'  [{label}] {msg}')
            return label, msg
        elapsed = time.time() - t0
        print(f'  [{label}] ok ({len(text)} chars, {elapsed:.1f}s)')
        return label, text
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')[:500]
        msg = f'ERROR HTTPError {e.code}: {body}'
        print(f'  [{label}] {msg}')
        return label, msg
    except Exception as e:
        msg = f'ERROR: {type(e).__name__}: {e}'
        print(f'  [{label}] {msg}')
        return label, msg


def main():
    print('Loading inputs...')
    current_s5 = slice_lines(PAPER_PATH, S5_START, S5_END)
    s4_bridge = slice_lines(PAPER_PATH, S4_BRIDGE_START, S4_BRIDGE_END)
    s1_3 = slice_lines(PAPER_PATH, S1_3_START, S1_3_END)
    appendix_b10 = slice_lines(PAPER_PATH, B10_START, B10_END)
    cold_read_outline = load_full_file(COLD_READ_OUTLINE_PATH)
    cold_read_diff = load_full_file(COLD_READ_DIFF_PATH)
    catalog_text = load_full_file(CATALOG_PATH)
    prior_review = load_full_file(PRIOR_REVIEW_PATH)

    sizes = {
        'current_s5': len(current_s5),
        'cold_read_outline': len(cold_read_outline),
        'cold_read_diff': len(cold_read_diff),
        's1_3': len(s1_3),
        's4_bridge': len(s4_bridge),
        'appendix_b10': len(appendix_b10),
        'catalog_text': len(catalog_text),
        'prior_review': len(prior_review),
    }
    for k, v in sizes.items():
        print(f'  {k}: {v} chars (~{v//4} tokens)')

    prompt_text = REVIEW_PROMPT.format(
        s5_start=S5_START, s5_end=S5_END,
        s13_start=S1_3_START, s13_end=S1_3_END,
        s47_start=S4_BRIDGE_START, s47_end=S4_BRIDGE_END,
        b10_start=B10_START, b10_end=B10_END,
        current_s5=current_s5,
        cold_read_outline=cold_read_outline,
        cold_read_diff=cold_read_diff,
        s1_3=s1_3,
        s4_bridge=s4_bridge,
        appendix_b10=appendix_b10,
        confidence_catalog=catalog_text,
        prior_review_synthesis=prior_review,
    )
    print(f'\n  combined prompt: {len(prompt_text)} chars (~{len(prompt_text)//4} tokens)')

    print('\nLoading API keys...')
    keys = {
        'MISTRAL_API_KEY':   get_win_env('MISTRAL_API_KEY'),
        'OPENAI_API_KEY':    get_win_env('OPENAI_API_KEY'),
        'GEMINI_API_KEY':    get_win_env('GEMINI_API_KEY'),
        'ANTHROPIC_API_KEY': get_win_env('ANTHROPIC_API_KEY'),
    }
    for k, v in keys.items():
        print(f'  {k}: {"SET (len="+str(len(v))+")" if v else "MISSING"}')

    reviews = {}

    if keys['MISTRAL_API_KEY']:
        print('\nMistral Large...')
        label, text = review_mistral(prompt_text, keys['MISTRAL_API_KEY'])
        reviews[label] = text
    else:
        reviews['Mistral Large'] = 'SKIPPED: MISTRAL_API_KEY not set'

    if keys['OPENAI_API_KEY']:
        print('\nGPT-5.5...')
        label, text = review_openai(prompt_text, keys['OPENAI_API_KEY'])
        reviews[label] = text
    else:
        reviews['GPT-5.5'] = 'SKIPPED: OPENAI_API_KEY not set'

    if keys['GEMINI_API_KEY']:
        print('\nGemini 2.5 Pro...')
        label, text = review_gemini(prompt_text, keys['GEMINI_API_KEY'])
        reviews[label] = text
    else:
        reviews['Gemini 2.5 Pro'] = 'SKIPPED: GEMINI_API_KEY not set'

    if keys['ANTHROPIC_API_KEY']:
        print('\nClaude Opus 4.7...')
        label, text = review_anthropic(prompt_text, keys['ANTHROPIC_API_KEY'])
        reviews[label] = text
    else:
        reviews['Claude Opus 4.7'] = 'SKIPPED: ANTHROPIC_API_KEY not set'

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = REVIEWS_DIR / f'round_v11_6_section5_structure_{ts}.md'
    succeeded = [k for k, v in reviews.items() if not (v.startswith('ERROR') or v.startswith('SKIPPED'))]
    failed = [k for k, v in reviews.items() if (v.startswith('ERROR') or v.startswith('SKIPPED'))]

    lines = [
        '# Beyond Recall v11.6 - §5 Structural Decision Cross-LLM Review',
        f'_Generated: {ts}_',
        f'_Reviewers: {len(reviews)} attempted, {len(succeeded)} succeeded, {len(failed)} failed/skipped_',
        '',
        '**Decision under review:** restructure §5 from current 6 subsections to proposed 8 subsections (cold-read agent #90 deliverable). Two new subsections (§5.3 retrieval-divergence, §5.5 Letta architectural ceilings); current §5.5 Practical Implications cut ~60% with production-architecture proposals moved to §7; §5.1 Anti-Pattern dropped/trimmed; §5.6 What the study does not settle moved to §6 Limitations.',
        '',
        '**Inputs sent to each reviewer:**',
        f'- Current §5 ({sizes["current_s5"]} chars) from `docs/beyond_recall_v11_6_draft.md` lines {S5_START}-{S5_END}',
        f'- Cold-read independent outline ({sizes["cold_read_outline"]} chars) from `docs/reviews/s5_independent_outline_20260501.md`',
        f'- Cold-read drift diff ({sizes["cold_read_diff"]} chars) from `docs/reviews/s5_drift_diff_20260501.md`',
        f'- §1.3 seven headlines ({sizes["s1_3"]} chars) from v11.6 lines {S1_3_START}-{S1_3_END}',
        f'- §4.7 §4-summary bridge ({sizes["s4_bridge"]} chars) from v11.6 lines {S4_BRIDGE_START}-{S4_BRIDGE_END}',
        f'- Appendix B.10 pre-registered/post-hoc table ({sizes["appendix_b10"]} chars) from v11.6 lines {B10_START}-{B10_END}',
        f'- Confidence catalog ({sizes["catalog_text"]} chars) from `docs/research/v11_confidence_catalog_20260428.md`',
        f'- Prior §1-4 review synthesis ({sizes["prior_review"]} chars) from `docs/reviews/round_v11_5_sections_1_4_20260501_141341.md`',
        f'- Combined prompt: {len(prompt_text)} chars (~{len(prompt_text)//4} tokens)',
        '',
        f'**Succeeded:** {", ".join(succeeded) if succeeded else "(none)"}',
        f'**Failed/Skipped:** {", ".join(failed) if failed else "(none)"}',
    ]
    for model in ['Mistral Large', 'GPT-5.5', 'Gemini 2.5 Pro', 'Claude Opus 4.7']:
        lines.append('\n---\n')
        lines.append(f'## {model}\n')
        lines.append(reviews.get(model, 'NOT RUN'))

    lines.append('\n---\n')
    lines.append('## Synthesis\n')
    lines.append('_To be written manually after review run completes; see orchestrator final write._\n')

    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nSaved review file: {out_path}')
    print(f'Succeeded: {len(succeeded)} / {len(reviews)}')
    return out_path


if __name__ == '__main__':
    main()
