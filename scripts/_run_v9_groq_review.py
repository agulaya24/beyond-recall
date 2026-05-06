"""
One-off Groq review of v9 draft.
Truncates to abstract + §1, optionally adds §4.1 (trimmed) and §5.2.
Saves to docs/reviews/v9_final_review_groq_llama33_YYYYMMDD.md.
"""

import json
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
import datetime
import re

REPO_ROOT = Path(__file__).parent.parent
PAPER_PATH = REPO_ROOT / 'docs' / 'beyond_recall_v9_draft.md'
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
OUT_DATE = datetime.datetime.now().strftime('%Y%m%d')
OUT_PATH = REVIEWS_DIR / f'v9_final_review_groq_llama33_{OUT_DATE}.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command', f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def load_paper():
    text = PAPER_PATH.read_text(encoding='utf-8')
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def extract_by_lines(text, start_line_1based, end_line_1based_exclusive):
    """Inclusive start, exclusive end, 1-based."""
    lines = text.split('\n')
    return '\n'.join(lines[start_line_1based - 1:end_line_1based_exclusive - 1])


PROMPT_TEMPLATE = """You are an experienced reviewer for a strong empirical ML / HCI venue (e.g., ICLR, CHI, ACL Findings). The following is a partial read of the Beyond Recall v9 paper — only the abstract and §1 Introduction fit in context (plus a compressed slice of §4.1 headline results and §5.2 summary bullets for calibration of headline claims). Review what you can see. Do not review or speculate about sections not provided.

Your review should be organized as:

## Critical issues (in visible sections only)
Items that must be fixed before submission. Cite section and specific claim. Be concrete.

## Needs revision (in visible sections only)
Framing or evidence issues where the paper overclaims, buries caveats, or fails to address a reader's natural objection. Cite section and suggest specific wording.

## Missing content
Based on what the abstract / §1 promises, what does a reader reasonably expect to find in the rest of the paper?

## Nice-to-have
Smaller clarity or citation improvements.

## Style
Prose, tone, or structural polish items.

## Verdict on visible material
One of: CRITICAL_FIXES_REQUIRED / NEEDS_REVISION / READY_WITH_MINOR_FIXES / READY (for visible sections only). One-sentence justification.

Specific items to evaluate in the visible sections:
- Is the LLM-class circularity limitation surfaced in the abstract or §1.3?
- §1.5 alignment framing: does the paper define behavioral alignment such that representational accuracy is required and then conclude representational accuracy is necessary for behavioral alignment? If so, is the circularity acknowledged?
- Does §1.4 (real-user extrapolation) lean harder on the N=1 author pilot than the evidence supports?

Be direct. If the abstract or §1 has problems that would hurt the paper's reception, say so.

PAPER (ABSTRACT + §1 ONLY) BEGINS:

{paper}
"""


def call_groq(api_key, content):
    url = 'https://api.groq.com/openai/v1/chat/completions'
    payload = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': content}],
        'temperature': 0.3,
        'max_tokens': 4096
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        return data['choices'][0]['message']['content']


def build_payload(full_text, mode='full'):
    """
    Layout in v9 draft:
      lines   1- 15 : title block + preamble
      lines  16- 29 : §1.1 (Recall vs interpretation; core hypothesis)
      lines  30- 88 : §1.2 (What We Tested — hypotheses, condition table, subject list, rubric table)
      lines  90-127 : §1.3 (What We Found — gradient, compression, mechanism, additivity, where it hurts, robustness)
      lines 129-135 : §1.4 (Why the Gradient Matters for Real Users)
      lines 137-147 : §1.5 (Behavioral Alignment)
    The prompt's named focus items are §1.3 (circularity), §1.4 (extrapolation), §1.5 (circularity).
    Under a ~4K-5K paper-content-token budget, prioritize §1.1 + §1.3 + §1.4 + §1.5 and compress §1.2.
    """
    if mode == 'full':
        return extract_by_lines(full_text, 1, 148).strip()
    if mode == 'priority':
        # Title + §1.1 (full) + §1.2 compressed (hypothesis names only) + §1.3 + §1.4 + §1.5
        title = extract_by_lines(full_text, 1, 16).strip()
        s11 = extract_by_lines(full_text, 16, 30).strip()
        # §1.2 compressed: just keep the opening paragraph and hypothesis bullet names
        s12_compressed = """### 1.2 What We Tested (compressed for context budget)

14 historical subjects with public-domain autobiographies; training/held-out split per subject. The study tests 5 hypotheses (H1-H5), evaluated across 10 experimental conditions (C1, C1-native, C2a, C2c (wrong-spec), C3, C3-native, C4, C4a, C5 (no-context baseline), C8 (raw corpus), C9 (raw + spec)) and a 5-judge primary LLM panel (Claude Haiku/Sonnet/Opus, GPT-4o, GPT-5.4) plus a 2-Gemini sensitivity panel. Scored on 1-5 interpretive rubric. Primary outcome: mean prediction score. Secondary outcome: per-question win rate against C5. H1: spec improves prediction. H2: effect is inversely proportional to pretraining coverage. H3: benefit is content-specific (wrong-spec control). H4: spec composes additively with commercial memory systems (Mem0, Letta, Supermemory, Zep). H5: compact spec matches raw corpus at a fraction of context. Letta stateful-agent path tested separately on N=3 (§4.5). Low-baseline slice (C5 ≤ 2.0, n=9) treated as population of relevance for real AI users.

[Full §1.2 with hypothesis table, condition table, subject list, and rubric anchors omitted for context budget.]
"""
        s13 = extract_by_lines(full_text, 90, 128).strip()
        s14 = extract_by_lines(full_text, 129, 136).strip()
        s15 = extract_by_lines(full_text, 137, 148).strip()
        return '\n\n'.join([title, s11, s12_compressed.strip(), s13, s14, s15])
    if mode == 'priority_tighter':
        # Even tighter: title + compressed §1.1 + compressed §1.2 + §1.3 headline paragraphs + §1.4 + §1.5
        title = extract_by_lines(full_text, 1, 16).strip()
        s11_compressed = """### 1.1 Recall Is Not Interpretation (compressed)

Current memory systems (Zep, Letta, Mem0, Supermemory) compete on recall benchmarks (LOCOMO, LongMemEval, ~68-85% accuracy). Recall is one part of memory; interpretation — how a specific person processes facts into judgments — is the other. The paper introduces **representational accuracy**: how well an AI system's internal model of a specific person captures that person's interpretive patterns. Core hypothesis: representational accuracy predicts alignment between an AI system's behavior and the intent of the person it serves. Operational test: behavioral prediction on held-out text, scored on a 1-5 interpretive rubric. Tested on 14 historical subjects' autobiographies.
"""
        s12_compressed = """### 1.2 What We Tested (compressed)

14 subjects, 10 conditions (C1/C1-native/C2a/C2c wrong-spec/C3/C3-native/C4/C4a/C5 no-context/C8 raw corpus/C9 raw+spec), 6 response models, 5-judge primary panel + 2-Gemini sensitivity. 5 hypotheses: H1 spec helps, H2 effect inversely proportional to pretraining, H3 content-specific (wrong-spec control), H4 composes with memory systems, H5 compact spec matches raw corpus. Low-baseline slice (C5 ≤ 2.0, n=9) = population of relevance for real users.
"""
        s13 = extract_by_lines(full_text, 90, 128).strip()
        s14 = extract_by_lines(full_text, 129, 136).strip()
        s15 = extract_by_lines(full_text, 137, 148).strip()
        return '\n\n'.join([title, s11_compressed.strip(), s12_compressed.strip(), s13, s14, s15])
    raise ValueError(f'unknown mode {mode}')


def main():
    api_key = get_win_env('GROQ_API_KEY')
    if not api_key:
        print('ERROR: GROQ_API_KEY not set')
        return 1

    full_text = load_paper()
    print(f'Full paper: {len(full_text)} chars')

    attempts = [
        ('priority: §1.1 + §1.2 compressed + §1.3 full + §1.4 + §1.5', lambda t: build_payload(t, mode='priority')),
        ('priority_tighter: §1.1 compressed + §1.2 compressed + §1.3 full + §1.4 + §1.5', lambda t: build_payload(t, mode='priority_tighter')),
    ]

    last_error = None
    for label, fn in attempts:
        payload_content = fn(full_text)
        prompt = PROMPT_TEMPLATE.format(paper=payload_content)
        print(f'\nAttempt: {label}')
        print(f'  Paper slice: {len(payload_content)} chars')
        print(f'  Full prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)')
        try:
            response_text = call_groq(api_key, prompt)
            print(f'  Response: {len(response_text)} chars')
            header = f"""# Groq Llama 3.3 70B — v9 Final Review

**Generated:** {datetime.datetime.now().isoformat()}
**Model:** llama-3.3-70b-versatile
**Paper:** `docs/beyond_recall_v9_draft.md` (v9, {len(full_text)} chars total)

## Review scope (what the model saw)

**Successful attempt:** `{label}`
**Paper slice sent to model:** {len(payload_content)} chars of {len(full_text)} total ({100*len(payload_content)/len(full_text):.1f}%)
**Groq TPM limit hit:** the free-tier llama-3.3-70b-versatile endpoint is capped at 12,000 tokens per request, so the full §1 (≈10,195 input tokens plus the prompt scaffold) exceeded the limit. The truncation strategy prioritized §1.3, §1.4, and §1.5 — the sections the review prompt specifically asked about — and compressed §1.1 and/or §1.2 into brief summary paragraphs.

Included in the model's view:
- Title block
- §1.1 (compressed or full, depending on attempt)
- §1.2 (compressed into 1-2 summary paragraphs — full condition table, hypothesis table, subject list, and rubric table were not sent)
- §1.3 **What We Found** — full text (gradient result, compression, mechanism, additivity, where spec hurts, robustness, Letta stateful-agent note)
- §1.4 **Why the Gradient Matters for Real Users** — full text (N=1 pilot extrapolation)
- §1.5 **Behavioral Alignment and the Human-AI Interaction Problem** — full text

**Excluded from model's view:** Full §1.2 tables, §2 Related Work, §3 Study Design, §4, §5, §6 Limitations, §7 Future Work, all Appendices.

The review below evaluates only what is listed above.

---

"""
            OUT_PATH.write_text(header + response_text, encoding='utf-8')
            print(f'\nSaved: {OUT_PATH}')
            return 0
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')[:500]
            print(f'  HTTPError {e.code}: {body}')
            last_error = f'HTTP {e.code}: {body}'
            if e.code == 413:
                continue  # try smaller
            else:
                # on non-size error, retry once plain
                print('  Retrying once...')
                try:
                    response_text = call_groq(api_key, prompt)
                    print(f'  Retry succeeded: {len(response_text)} chars')
                    header = f"""# Groq Llama 3.3 70B — v9 Final Review

**Generated:** {datetime.datetime.now().isoformat()} (succeeded on retry)
**Model:** llama-3.3-70b-versatile

**Included:** {label}
**Paper slice sent:** {len(payload_content)} chars of {len(full_text)} total.

---

"""
                    OUT_PATH.write_text(header + response_text, encoding='utf-8')
                    print(f'\nSaved: {OUT_PATH}')
                    return 0
                except Exception as e2:
                    last_error = f'retry failed: {e2}'
                    continue
        except Exception as e:
            print(f'  ERROR: {e}')
            last_error = str(e)
            continue

    # All attempts failed
    fail_msg = f"""# Groq Llama 3.3 70B — v9 Final Review (FAILED)

**Generated:** {datetime.datetime.now().isoformat()}

All attempts failed. Last error: {last_error}
"""
    OUT_PATH.write_text(fail_msg, encoding='utf-8')
    print(f'FAILED. Wrote failure note to {OUT_PATH}')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
