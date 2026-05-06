"""Rerun GPT-5.4 judging for wrong_spec_v2 across 13 globals.

Root cause of original failure: judge_tier2.judge_gpt54 used `max_tokens` which
GPT-5.x rejects with HTTP 400. Fix is identical to 60_rerun_gpt54_letta.py:
use `max_completion_tokens` instead.

Outputs (DO NOT overwrite the empty/failed wrong_spec_v2_judgments_gpt54.json):
    results/_wrong_spec_v2/global_<subject>/wrong_spec_v2_judgments_gpt54_rerun_20260425.json

Per-question atomic writes; resumable. temperature=0, model gpt-5.4.

Cost budget: ~$3 (520 calls x ~1100 input tokens x $1.25/M + minimal output).
"""
import json, os, subprocess, time, re, httpx, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSE_BASE = r"C:\Users\Aarik\Anthropic\memory_system\data\experiments\memory_systems\results"

SUBJECTS = [
    'augustine','babur','bernal_diaz','cellini','ebers','equiano','fukuzawa',
    'keckley','rousseau','seacole','sunity_devee','yung_wing','zitkala_sa'
]

# Load API key from User env
r = subprocess.run(['powershell', '-Command',
    "[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')"],
    capture_output=True, text=True)
KEY = r.stdout.strip()
assert KEY, "OPENAI_API_KEY not found"

# Identical prompt template used in judge_tier2.py / judge_wrong_spec_v2.py
JUDGE_PROMPT = """You are evaluating a behavioral prediction against a verbatim ground truth passage.

Question: {question}

Ground truth (what actually happened): {ground_truth}

Response to score: {response}

Score 1-5 based on prediction accuracy:
5 = Predicts the specific outcome or behavior in the ground truth
4 = Predicts the general direction correctly with some specifics
3 = Captures the right domain but not the specific outcome
2 = Addresses the topic but predicts incorrectly
1 = Refuses to answer or is completely off-base

Respond with only the number 1, 2, 3, 4, or 5."""


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'\b([1-5])\b', text.strip())
    return int(m.group(1)) if m else 0


def call_gpt54(prompt):
    """FIXED: uses max_completion_tokens instead of max_tokens."""
    last_err = None
    for attempt in range(5):
        try:
            r = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-5.4",
                    "max_completion_tokens": 10,
                    "temperature": 0,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={
                    "Authorization": f"Bearer {KEY}",
                    "Content-Type": "application/json",
                },
                timeout=60,
            )
            if r.status_code == 429:
                wait = 2 ** (attempt + 2)
                print(f"  429 -> sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = e
            if attempt < 4:
                time.sleep(2 ** (attempt + 1))
            else:
                raise
    raise RuntimeError(f"gpt54 failed after retries: {last_err}")


def atomic_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def load_existing(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    grand_total = 0
    grand_valid = 0
    grand_failed = 0
    for subject in SUBJECTS:
        resp_path = os.path.join(RESPONSE_BASE, f'global_{subject}', 'wrong_spec_v2_results.json')
        out_path = os.path.join(REPO, 'results', '_wrong_spec_v2', f'global_{subject}',
                                'wrong_spec_v2_judgments_gpt54_rerun_20260425.json')

        with open(resp_path, encoding='utf-8') as f:
            results = json.load(f)

        existing = load_existing(out_path)
        done = {j['question_id'] for j in existing}

        to_judge = []
        for q in results:
            qid = q['question_id']
            if qid in done:
                continue
            ho = q.get('held_out_passage', '')
            if not ho:
                continue
            resp = q.get('response', {})
            if not isinstance(resp, dict) or 'error' in resp or 'text' not in resp:
                continue
            to_judge.append((qid, q.get('question_text', ''), ho, resp['text']))

        if not to_judge:
            valid = sum(1 for r in existing if not r.get('parse_failure'))
            print(f'[{subject}] all done, {len(existing)} records, {valid} valid', flush=True)
            grand_total += len(existing)
            grand_valid += valid
            continue

        print(f'[{subject}] {len(to_judge)} to judge (existing {len(existing)})', flush=True)

        consec_fail = 0
        for qid, qt, ho, resp_text in to_judge:
            prompt = JUDGE_PROMPT.format(question=qt, ground_truth=ho, response=resp_text)
            try:
                raw = call_gpt54(prompt)
                score = parse_score(raw)
                rec = {
                    'question_id': qid,
                    'condition': 'C2c_wrong_spec_v2',
                    'judge': 'gpt54',
                    'score': score,
                    'raw': raw.strip()[:100],
                    'parse_failure': score == 0,
                }
                if score == 0:
                    consec_fail += 1
                else:
                    consec_fail = 0
            except Exception as e:
                rec = {
                    'question_id': qid,
                    'condition': 'C2c_wrong_spec_v2',
                    'judge': 'gpt54',
                    'score': 0,
                    'error': str(e)[:300],
                    'parse_failure': True,
                }
                consec_fail += 1
                print(f'  ERROR qid={qid}: {e}', flush=True)
            existing.append(rec)
            # atomic per-question write (resumable)
            atomic_write_json(out_path, existing)
            if consec_fail >= 5:
                print(f'[{subject}] 5 consecutive failures, aborting subject', flush=True)
                break
            time.sleep(0.15)

        valid = sum(1 for r in existing if not r.get('parse_failure'))
        failed = sum(1 for r in existing if r.get('parse_failure'))
        mean = (sum(r['score'] for r in existing if not r.get('parse_failure')) / valid) if valid else 0
        print(f'[{subject}] DONE valid={valid}/{len(existing)} mean={mean:.3f}', flush=True)
        grand_total += len(existing)
        grand_valid += valid
        grand_failed += failed

    print()
    print('='*60)
    print(f'GRAND TOTAL: valid={grand_valid}/{grand_total}, failed={grand_failed}')
    print('='*60)


if __name__ == '__main__':
    main()
