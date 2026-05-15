"""
GPT-5.4 judging rerun for Tier 2 response data (S119, 2026-05-07).

Why this exists
---------------
Tier 2 cross-provider replication response files at
``results/_tier2/global_<subject>/tier2_<response_model>_judgments_gpt54.json``
were originally produced before the GPT-5.x ``max_completion_tokens`` fix
(see ``scripts/_judge_invocation/openai_judge_call.py``). All 156 rows in
each existing file are HTTP 400 parse failures. The rest of the paper now
uses 5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54) and
§4.6.1 Tier 2 numbers must be brought into parity by replacing the failed
gpt54 column with real judgments.

Scope
-----
3 subjects (Ebers, Yung Wing, Zitkala-Sa)
x 2 response models (Sonnet 4.6, Gemini 2.5 Pro)
x 39 behavioral_prediction questions
x 4 conditions (C5_baseline, C2a_full_spec, C4a_full_facts_plus_spec, C2c_wrong_spec)
= 936 GPT-5.4 judge calls.

Inputs
------
``results/_tier2/global_<subject>/tier2_<response_model>_results.json`` --
each is a 39-element list with `responses` keyed by condition name.

Outputs
-------
Per (subject, response_model) cell:
  ``results/_tier2/global_<subject>/tier2_<response_model>_judgments_gpt54_rerun_20260507.json``

Schema matches the canonical 5-judge format used by every other primary
judge file in the repo:
    {question_id, condition, judge: 'gpt54', score, raw_response, parse_failure}

The original ``..._judgments_gpt54.json`` files are NOT modified. A separate
aggregate-recompute step will repoint to the rerun files.

Methodology
-----------
- Canonical 5-judge rubric prompt copied verbatim from
  ``judge_hamerton_5judge.py`` (also used by ``backfill_all_parse_failures.py``
  and ``judge_supermemory_paid_rerun_7judge.py``).
- Judge invocation through the shared
  ``scripts/_judge_invocation/openai_judge_call.call_openai_judge``,
  which routes ``gpt-5.4`` to ``max_completion_tokens`` automatically and
  retries 429/5xx with exponential backoff.
- Checkpoint after every 10 successful or attempted calls per cell.
- Resume-safe: on rerun, existing rows in the output file are read and the
  (question_id, condition) pairs are skipped.
- HALT-on-MAJOR-ERROR: AUTH_ERROR or BAD_PARAMETER aborts the whole script
  and reports. Per-call PARSE_FAILURE / TIMEOUT / RATE_LIMITED-after-retries
  are recorded as score=None with the error text and the script continues.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Repo paths
REPO = Path(__file__).resolve().parent.parent
TIER2 = REPO / 'results' / '_tier2'

# Make the shared judge utility importable.
sys.path.insert(0, str(REPO / 'scripts'))
from _judge_invocation.openai_judge_call import (  # noqa: E402
    JudgeAPIError,
    call_openai_judge,
)

# ---------- Run config -------------------------------------------------------

SUBJECTS = ['ebers', 'yung_wing', 'zitkala_sa']
RESPONSE_MODELS = ['sonnet', 'gemini_pro']
CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec', 'C2c_wrong_spec']

JUDGE_NAME = 'gpt54'
JUDGE_MODEL = 'gpt-5.4'
RUN_ID = 'tier2_gpt54_rerun_20260507'

CHECKPOINT_EVERY = 10
MAX_OUTPUT_TOKENS = 10  # plenty for a single digit; matches `judge_floor_test.py`


def log(msg: str) -> None:
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)


def judge_prompt(held_out: str, response_text: str) -> str:
    """Canonical 5-judge primary-panel rubric.

    Identical to scripts/judge_hamerton_5judge.py, scripts/backfill_all_parse_failures.py,
    and scripts/judge_supermemory_paid_rerun_7judge.py.
    """
    return (
        'You are evaluating whether a response about a person PREDICTED '
        'what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
        '=== RESPONSE ===\n' + (response_text or '')[:1500] + '\n\n'
        'Rate 1-5:\n'
        '5=Predicts specific outcome\n'
        '4=General direction correct\n'
        '3=Right domain wrong outcome\n'
        '2=Wrong prediction\n'
        '1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def atomic_write(path: Path, data: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_existing(path: Path) -> tuple[list[dict], set[tuple[int, str]]]:
    if not path.exists():
        return [], set()
    try:
        rows = json.load(path.open(encoding='utf-8'))
    except Exception as e:
        log(f'WARN: failed to load existing {path.name}: {e}; starting fresh')
        return [], set()
    done = {
        (int(r['question_id']), r['condition']) for r in rows
        if r.get('score') is not None and not r.get('parse_failure', False)
    }
    return rows, done


def process_cell(subject: str, response_model: str) -> dict:
    """Run gpt54 judging on one (subject, response_model) cell.

    Returns a small per-cell summary dict.
    """
    cell_dir = TIER2 / f'global_{subject}'
    results_path = cell_dir / f'tier2_{response_model}_results.json'
    out_path = cell_dir / f'tier2_{response_model}_judgments_gpt54_rerun_20260507.json'

    if not results_path.exists():
        log(f'SKIP: {results_path} not found')
        return {'cell': f'{subject}/{response_model}', 'status': 'missing_input'}

    data = json.load(results_path.open(encoding='utf-8'))
    bp = [r for r in data
          if r.get('tier') == 'behavioral_prediction'
          and r.get('held_out_passage')]
    log(f'[{subject}/{response_model}] Loaded {len(bp)} behavioral_prediction questions')

    rows, done = load_existing(out_path)
    if rows:
        log(f'[{subject}/{response_model}] Resuming with {len(rows)} existing rows '
            f'({len(done)} non-failed pairs already done)')

    new_calls = 0
    parse_failures = 0
    api_failures = 0

    for q in bp:
        qid = int(q['question_id'])
        ho = q['held_out_passage']
        responses = q.get('responses') or {}

        for cond in CONDITIONS:
            if (qid, cond) in done:
                continue

            # Drop any pre-existing failed row for this pair so we don't dupe.
            rows = [r for r in rows
                    if not (int(r['question_id']) == qid and r['condition'] == cond)]

            resp = responses.get(cond)
            if not resp or not resp.get('text'):
                log(f'[{subject}/{response_model}] missing response q={qid} cond={cond}; skipping')
                rows.append({
                    'question_id': qid,
                    'condition': cond,
                    'judge': JUDGE_NAME,
                    'score': None,
                    'raw_response': 'MISSING_RESPONSE',
                    'parse_failure': True,
                })
                continue

            prompt = judge_prompt(ho, resp['text'])

            try:
                result = call_openai_judge(
                    model=JUDGE_MODEL,
                    system='',
                    user=prompt,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                    temperature=0.0,
                    timeout_s=60.0,
                    max_retries_429=5,
                    max_retries_5xx=3,
                    run_id=RUN_ID,
                    log=True,
                )
                score = result['score'] or None
                raw = result.get('raw_text') or ''
                row = {
                    'question_id': qid,
                    'condition': cond,
                    'judge': JUDGE_NAME,
                    'score': score,
                    'raw_response': raw[:200],
                    'parse_failure': score is None,
                }
                if score is None:
                    parse_failures += 1
            except JudgeAPIError as e:
                # Halt on auth or BAD_PARAMETER. Anything else, log and continue.
                if e.failure_type in ('AUTH_ERROR', 'BAD_PARAMETER'):
                    atomic_write(out_path, rows)
                    log(f'FATAL: {e.failure_type} on q={qid} cond={cond}: {e}')
                    raise
                api_failures += 1
                log(f'[{subject}/{response_model}] API {e.failure_type} '
                    f'q={qid} cond={cond}: {e}')
                row = {
                    'question_id': qid,
                    'condition': cond,
                    'judge': JUDGE_NAME,
                    'score': None,
                    'raw_response': f'ERR_{e.failure_type}: {str(e)[:160]}',
                    'parse_failure': True,
                }

            rows.append(row)
            new_calls += 1
            if new_calls % CHECKPOINT_EVERY == 0:
                atomic_write(out_path, rows)
                log(f'[{subject}/{response_model}] Progress: {new_calls} new calls, '
                    f'{len(rows)} total rows '
                    f'(parse_failures={parse_failures}, api_failures={api_failures})')

    atomic_write(out_path, rows)
    valid = sum(1 for r in rows
                if r.get('score') is not None and not r.get('parse_failure', False))
    log(f'[{subject}/{response_model}] DONE. {len(rows)} total rows, '
        f'{valid} valid scores, {new_calls} new calls this run. '
        f'Output: {out_path.name}')
    return {
        'cell': f'{subject}/{response_model}',
        'total_rows': len(rows),
        'valid_scores': valid,
        'parse_failures': parse_failures,
        'api_failures': api_failures,
        'new_calls': new_calls,
    }


def main() -> int:
    log('=' * 70)
    log(f'GPT-5.4 Tier 2 judging rerun (run_id={RUN_ID})')
    log(f'  judge model: {JUDGE_MODEL}')
    log(f'  subjects:    {SUBJECTS}')
    log(f'  resp models: {RESPONSE_MODELS}')
    log(f'  conditions:  {CONDITIONS}')
    log(f'  expected calls (full): {len(SUBJECTS) * len(RESPONSE_MODELS) * 39 * len(CONDITIONS)}')
    log('=' * 70)

    # Pre-flight: confirm OPENAI_API_KEY (also pulled from Windows User env by
    # the openai_judge_call module on first call). Probing here gives an early,
    # clearer halt than letting the first real call do it.
    if not os.environ.get('OPENAI_API_KEY'):
        # Trigger the resolver via a no-op probe; if it raises AUTH_ERROR we exit.
        try:
            from _judge_invocation.openai_judge_call import _resolve_api_key
            _resolve_api_key()
        except JudgeAPIError as e:
            log(f'FATAL: {e}')
            return 2

    started = datetime.now()
    summaries = []
    try:
        for subject in SUBJECTS:
            for rm in RESPONSE_MODELS:
                summaries.append(process_cell(subject, rm))
    except JudgeAPIError as e:
        log(f'HALTED: {e.failure_type}: {e}')
        return 3

    elapsed = (datetime.now() - started).total_seconds()
    log('=' * 70)
    log(f'ALL CELLS COMPLETE in {elapsed:.1f}s ({elapsed/60:.1f} min)')
    for s in summaries:
        log(f'  {s}')
    log('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
