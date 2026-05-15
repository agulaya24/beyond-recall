"""
Sonnet + Opus calibration retrieval / runner.

Fills the gap in the Beyond Recall paper's §3.3.3 calibration table for
Claude Sonnet 4.6 and Claude Opus 4.6. The other 5 judges (Haiku, Gemini Flash,
GPT-4o, GPT-5.4, Gemini Pro) have already been run through the same diagnostic.

Pipeline note. The original full-panel calibration script (run_judge_calibration_full_panel.py)
submitted the same 80 calibration items to Sonnet and Opus via the Batch API on 2026-04-12,
using the *same* paraphrased / short / long inputs that GPT-4o and Gemini Pro saw. The
batches completed (succeeded=80 each) but no per-judge JSON was ever written. To preserve
data comparability with the existing 5 judges (same paraphrases, same prompts), this
script *first* attempts to retrieve those batches and only falls back to a fresh run
if the results are unavailable.

Outputs to:
- results/judge_calibration/sonnet_calibration.json
- results/judge_calibration/opus_calibration.json
"""
import json, os, pathlib, subprocess, sys, time
from collections import defaultdict

# Hydrate API key
for k in ['ANTHROPIC_API_KEY']:
    r = subprocess.run(
        ['powershell', '-Command',
         f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
        capture_output=True, text=True)
    val = r.stdout.strip()
    if val:
        os.environ[k] = val

import anthropic
import httpx

client = anthropic.Anthropic()

REPO = pathlib.Path(__file__).resolve().parents[1]
OUTDIR = REPO / 'results' / 'judge_calibration'
OUTDIR.mkdir(parents=True, exist_ok=True)

SONNET_BATCH_ID = 'msgbatch_01KagGcuniVWznK7AqzAwPoY'
OPUS_BATCH_ID = 'msgbatch_01HKfAsEVMuU45FjtADU2v3E'

SONNET_MODEL = 'claude-sonnet-4-6'
OPUS_MODEL = 'claude-opus-4-6'


def parse_score(text):
    """First-digit parse, matching existing diagnostic pattern."""
    text = (text or '').strip()
    return int(text[0]) if text and text[0].isdigit() else 0


def collect_from_batch(batch_id, judge_label):
    """Retrieve batch and return list of {test, qid, <judge>_score}."""
    rows = []
    parse_failures = 0
    score_key = f'{judge_label}_score'
    print(f'  Retrieving batch {batch_id} for {judge_label}...', flush=True)
    for r in client.messages.batches.results(batch_id):
        cid = r.custom_id  # e.g. "verbatim__q21"
        test, q_part = cid.split('__')
        qid = int(q_part.lstrip('q'))
        if r.result.type != 'succeeded':
            score = 0
            parse_failures += 1
        else:
            text = r.result.message.content[0].text
            score = parse_score(text)
            if score == 0:
                parse_failures += 1
        rows.append({'test': test, 'qid': qid, score_key: score})
    return rows, parse_failures


def fresh_run(model_id, judge_label):
    """Fallback: rebuild calibration items and run synchronously."""
    print(f'  Falling back to fresh run for {judge_label} ({model_id})...', flush=True)

    # Reuse the same battery + paraphrasing logic as run_judge_calibration_full_panel.py
    # NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
    # to its path; defaults to empty so the missing-path failure is obvious.
    battery_path = pathlib.Path(os.environ.get("MEMORY_SYSTEM_ROOT", "")) / 'data' / 'experiments' / 'memory_systems' / 'battery' / 'questions_80.json'
    battery = json.load(open(battery_path))
    bp_qs = [q for q in battery['questions']
             if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')][:20]

    def jp(ho, response):
        return ('You are evaluating whether a response about a person PREDICTED '
                'what actually happened.\n\n'
                '=== HELD-OUT GROUND TRUTH ===\n' + ho + '\n\n'
                '=== RESPONSE ===\n' + response + '\n\n'
                'Rate 1-5:\n'
                '5=Predicts specific outcome\n'
                '4=General direction correct\n'
                '3=Right domain wrong outcome\n'
                '2=Wrong prediction\n'
                '1=Refuses or off-base\n\n'
                'Respond with ONLY a single digit (1-5).')

    api_key = os.environ['ANTHROPIC_API_KEY']

    items = []
    for q in bp_qs:
        ho = q['held_out_passage']
        qid = q['id']
        items.append({'test': 'verbatim', 'qid': qid, 'prompt': jp(ho, ho)})
        # Paraphrased
        try:
            resp = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 512,
                      'temperature': 0,
                      'messages': [{'role': 'user',
                                    'content': f'Paraphrase this passage in your own words. '
                                               f'Keep all facts but change wording completely.\n\n{ho}'}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=30)
            para = resp.json()['content'][0]['text']
        except Exception:
            para = ho
        items.append({'test': 'paraphrased', 'qid': qid, 'prompt': jp(ho, para)})
        # Short
        first_sentence = ho.split('.')[0] + '.'
        items.append({'test': 'short_correct', 'qid': qid, 'prompt': jp(ho, first_sentence)})
        # Long
        long_resp = (ho + '\n\nThis behavior is consistent with the subject\'s established patterns '
                     'of careful deliberation, preference for direct experience over abstract '
                     'instruction, and willingness to make unconventional choices when they '
                     'align with deeply held values.')
        items.append({'test': 'long_correct', 'qid': qid, 'prompt': jp(ho, long_resp)})

    rows = []
    parse_failures = 0
    score_key = f'{judge_label}_score'
    for i, item in enumerate(items):
        try:
            resp = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={'model': model_id, 'max_tokens': 8, 'temperature': 0,
                      'messages': [{'role': 'user', 'content': item['prompt']}]},
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=60)
            t = resp.json()['content'][0]['text'].strip()
            score = parse_score(t)
            if score == 0:
                parse_failures += 1
        except Exception:
            score = 0
            parse_failures += 1
        rows.append({'test': item['test'], 'qid': item['qid'], score_key: score})
        if (i + 1) % 20 == 0:
            print(f'    {i + 1}/{len(items)}', flush=True)
    return rows, parse_failures


def report(rows, judge_label):
    score_key = f'{judge_label}_score'
    print(f'\n=== {judge_label.upper()} ===', flush=True)
    for test_name in ['verbatim', 'paraphrased', 'short_correct', 'long_correct']:
        scores = [r[score_key] for r in rows if r['test'] == test_name and r[score_key] > 0]
        avg = sum(scores) / len(scores) if scores else 0
        dist = [scores.count(i) for i in range(1, 6)]
        print(f'  {test_name:<18} mean={avg:.2f} (n={len(scores)}) dist={dist}', flush=True)


def main():
    summary = {}
    for batch_id, judge_label, fallback_model in [
        (SONNET_BATCH_ID, 'sonnet', SONNET_MODEL),
        (OPUS_BATCH_ID,   'opus',   OPUS_MODEL),
    ]:
        try:
            b = client.messages.batches.retrieve(batch_id)
            ok = (b.processing_status == 'ended'
                  and b.request_counts.succeeded > 0
                  and b.request_counts.errored == 0)
            if not ok:
                raise RuntimeError(f'Batch not in usable state: {b.processing_status} '
                                   f'(succeeded={b.request_counts.succeeded}, '
                                   f'errored={b.request_counts.errored})')
            rows, parse_failures = collect_from_batch(batch_id, judge_label)
            source = f'batch:{batch_id}'
        except Exception as e:
            print(f'  Batch retrieval failed for {judge_label}: {e}', flush=True)
            rows, parse_failures = fresh_run(fallback_model, judge_label)
            source = f'fresh:{fallback_model}'

        out = OUTDIR / f'{judge_label}_calibration.json'
        with open(out, 'w') as f:
            json.dump(rows, f, indent=2)
        print(f'  Wrote {out} ({len(rows)} rows, source={source}, parse_failures={parse_failures})',
              flush=True)
        report(rows, judge_label)
        summary[judge_label] = {'rows': rows, 'parse_failures': parse_failures, 'source': source}

    # Combined summary table
    print('\n=== SUMMARY (Sonnet + Opus) ===', flush=True)
    print(f'{"Test":<18} {"Sonnet":>8} {"Opus":>8}', flush=True)
    print('=' * 36, flush=True)
    for test_name in ['verbatim', 'paraphrased', 'short_correct', 'long_correct']:
        sn_scores = [r['sonnet_score'] for r in summary['sonnet']['rows']
                     if r['test'] == test_name and r['sonnet_score'] > 0]
        op_scores = [r['opus_score'] for r in summary['opus']['rows']
                     if r['test'] == test_name and r['opus_score'] > 0]
        sn_avg = sum(sn_scores) / len(sn_scores) if sn_scores else 0
        op_avg = sum(op_scores) / len(op_scores) if op_scores else 0
        print(f'  {test_name:<16} {sn_avg:>8.2f} {op_avg:>8.2f}', flush=True)


if __name__ == '__main__':
    main()
