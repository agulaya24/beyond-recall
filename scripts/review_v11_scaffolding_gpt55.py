"""
v11 Mechanistic-Check Architecture — GPT-5.5 Review

Sends the v11 emit architecture, reconciliation diff, table-rebuild proposal,
and one representative emit script to GPT-5.5. Asks for an independent
methodology + soundness review of the scaffolding and the results.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCH = REPO / 'docs' / 'research' / 'v11_emit' / '_ARCHITECTURE.md'
DIFF = REPO / 'docs' / 'research' / 'v11_reconciliation_diff.md'
REBUILD = REPO / 'docs' / 'research' / 'v11_table_rebuild_proposal.md'
EMIT_4_1 = REPO / 'scripts' / '_v11_emit_4_1_gradient.py'
JUDGE_UTIL = REPO / 'scripts' / '_judge_invocation' / '__init__.py'
PANEL_AUDIT = REPO / 'docs' / 'research' / 'v11_panel_completeness_audit.csv'
WAIVERS = REPO / 'docs' / 'research' / 'v11_panel_completeness_waivers.json'

OUT = REPO / 'docs' / 'reviews' / 'v11_scaffolding_review_gpt55_20260425.md'


def get_win_env(key):
    r = subprocess.run(
        ['powershell', '-Command',
         f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def read_truncated(path: Path, max_chars: int) -> str:
    if not path.exists():
        return f"[file not found: {path}]"
    text = path.read_text(encoding='utf-8', errors='replace')
    if len(text) > max_chars:
        keep = max_chars - 200
        return text[:keep] + f"\n\n[... truncated; full file is {len(text)} chars ...]\n"
    return text


PROMPT_TEMPLATE = """You are an experienced reviewer of empirical-ML methodology and reproducibility infrastructure. The Beyond Recall paper (a 14-subject behavioral-spec personalization study) is undergoing a v10 → v11 release-freeze. The author built a mechanistic-check scaffolding architecture so every reported number traces to a named, idempotent emit script reading primary-data JSON only.

You are given five artifacts:
1. The architecture spec (`v11_emit/_ARCHITECTURE.md`)
2. The reconciliation diff between scaffold output and v10 paper text (`v11_reconciliation_diff.md`)
3. The table-rebuild proposal that walks the diff section by section (`v11_table_rebuild_proposal.md`)
4. One representative emit script (`_v11_emit_4_1_gradient.py`)
5. The shared judge-invocation utility (`_judge_invocation/__init__.py`)

Plus two ancillary inputs: the panel-completeness audit CSV and the waivers JSON.

Your review:

## 1. Architecture soundness
Is the v11 contract sufficient to make the paper numbers reproducible? What is missing? Where does the contract leak (i.e., a number could still enter the manuscript by an unmonitored path)?

## 2. Aggregation rule
The locked rule is: per-judge × per-question score → per-judge × per-subject mean → panel mean across the 5 primary judges (haiku, sonnet, opus, gpt4o, gpt54). Is this the right aggregation for cross-subject and within-subject claims? Are there claims in the paper that need a *different* rule, and is that rule explicitly declared?

## 3. Reconciliation results
Of the 1,509 claim_ids, 72.2% MATCH, 4.3% MINOR_ROUNDING, 13.7% SUBSTANTIVE. The advisor has clarified that ZERO published-table sign flips remain after rebuild (the 14 'sign flips' in the diff are stale running-list artifacts). Is this conclusion warranted, or should the author do a deeper verification before treating those flips as artifacts?

## 4. Coverage gaps
- §4.6.1 Tier 2 cross-provider replication has NO scaffold coverage.
- The proposal flags 'PAPER_ONLY' (paper-side number with no scaffold claim) at 0 entries. Is the heuristic strong enough? What additional coverage gaps would you expect?

## 5. Tier 1/2/3 application order
The proposal recommends silent cleanup → minor drift → substantive author-decision changes. Is this the correct order, or should some Tier 3 items be elevated/demoted?

## 6. The §4.4.2 panel asymmetry
The §4.4.2 paired-Δ table is on the audit (6-judge) panel by declared note (line 1209). Under strict 5-judge primary the n shifts 507/516 → 546 and percentages shift by 1-2 pp. Should the author rebuild the table on 5-judge primary, or keep on the audit panel with explicit footnote?

## 7. Robustness of the GPT-5.x judge-call controls
The v11 spec requires all judge calls to route through `_judge_invocation/`, which auto-routes `max_completion_tokens` for gpt-5* / o1 / o3 model ids. Is the dispatcher pattern strong enough, and are the pre-flight + panel-completeness audits sufficient guards?

## 8. What I would push back on
If you were the methodology referee at NeurIPS / ICLR D&B, what would you reject this scaffolding for? What gaps would you require closed before accepting?

Be direct. The author specifically wants honesty over diplomacy.

ARTIFACT 1 — ARCHITECTURE SPEC ({arch_chars} chars):
{arch}

ARTIFACT 2 — RECONCILIATION DIFF ({diff_chars} chars):
{diff}

ARTIFACT 3 — TABLE-REBUILD PROPOSAL ({rebuild_chars} chars):
{rebuild}

ARTIFACT 4 — REPRESENTATIVE EMIT SCRIPT _v11_emit_4_1_gradient.py ({emit_chars} chars):
{emit}

ARTIFACT 5 — SHARED JUDGE-INVOCATION UTILITY __init__.py ({util_chars} chars):
{util}

ANCILLARY 1 — PANEL-COMPLETENESS AUDIT CSV ({audit_chars} chars):
{audit}

ANCILLARY 2 — PANEL-COMPLETENESS WAIVERS JSON ({waivers_chars} chars):
{waivers}
"""


def call_openai(api_key, model_id, prompt, max_tokens=12000, timeout=900):
    url = 'https://api.openai.com/v1/chat/completions'
    body = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': max_tokens,
    }
    if model_id.startswith('gpt-4'):
        body['temperature'] = 0.3
        body.pop('max_completion_tokens')
        body['max_tokens'] = max_tokens
    payload = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            usage = data.get('usage', {})
            return text, None, {'model': data.get('model'), 'usage': usage}
    except urllib.error.HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode()[:500]
        except Exception:
            pass
        return None, f'HTTP {e.code}: {body_text}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


def main():
    api_key = get_win_env('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: OPENAI_API_KEY not in user env')
        sys.exit(1)
    print(f'API key loaded ({len(api_key)} chars)')

    arch = read_truncated(ARCH, 25000)
    diff = read_truncated(DIFF, 35000)
    rebuild = read_truncated(REBUILD, 40000)
    emit = read_truncated(EMIT_4_1, 25000)
    util = read_truncated(JUDGE_UTIL, 15000)
    audit = read_truncated(PANEL_AUDIT, 8000)
    waivers = read_truncated(WAIVERS, 4000)

    prompt = PROMPT_TEMPLATE.format(
        arch=arch, arch_chars=len(arch),
        diff=diff, diff_chars=len(diff),
        rebuild=rebuild, rebuild_chars=len(rebuild),
        emit=emit, emit_chars=len(emit),
        util=util, util_chars=len(util),
        audit=audit, audit_chars=len(audit),
        waivers=waivers, waivers_chars=len(waivers),
    )
    print(f'Prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)')

    candidates = ['gpt-5.5', 'gpt-5.4', 'gpt-5']
    text = None
    chosen_model = None
    last_error = None
    meta = None
    for model_id in candidates:
        print(f'\nTrying model: {model_id}')
        for attempt in range(2):
            t0 = time.time()
            text, err, meta = call_openai(api_key, model_id, prompt, max_tokens=12000, timeout=900)
            elapsed = time.time() - t0
            if text:
                wc = len(text.split())
                print(f'  SUCCESS in {elapsed:.1f}s — {len(text)} chars / {wc} words')
                if wc < 800:
                    print(f'  WARNING: only {wc} words. Retrying once...')
                    if attempt == 0:
                        time.sleep(5)
                        continue
                    last_error = f'short_response_{wc}_words'
                    text = None
                    break
                chosen_model = meta.get('model') or model_id
                break
            else:
                print(f'  FAIL ({elapsed:.1f}s): {err}')
                last_error = err
                if attempt == 0:
                    print('  retrying in 10s...')
                    time.sleep(10)
        if text:
            break

    if not text:
        print(f'\nALL MODELS FAILED. Last error: {last_error}')
        OUT.write_text(
            f'# v11 Scaffolding Review — FAILED\n\nLast error: {last_error}\n',
            encoding='utf-8'
        )
        sys.exit(1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Beyond Recall v11 Scaffolding Review (GPT-5.5)\n\n"
        f"_Generated 2026-04-25 by `scripts/review_v11_scaffolding_gpt55.py`._\n\n"
        f"**Model:** {chosen_model}\n"
        f"**Usage:** {json.dumps(meta.get('usage', {}))}\n\n"
        f"---\n\n"
    )
    OUT.write_text(header + text, encoding='utf-8')
    print(f'\nWritten: {OUT}')


if __name__ == '__main__':
    main()
