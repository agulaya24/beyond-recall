"""Build the per-question parse-failure inventory CSV.

Walks every results/<subject>/*_judgments_<judge>.json file and emits one row
per (subject, condition, question_id, judge) cell where the response failed to
parse to a valid 1-5 score.

Failure classes:
  http_429        — original raw_response contains '429' or 'Too Many Requests'
  http_403        — original raw_response contains '403' or 'Forbidden'
  http_other_err  — raw_response contains 'error' or 'Client error'
  empty_response  — raw_response is empty/whitespace
  no_score_extracted — non-empty raw_response but no integer 1-5 found
  out_of_range    — score is integer outside 1-5
  score_zero      — score=0 or None, no other identifiable cause
  no_response_data — the originating responses file lacks data for that condition+question
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_CSV = REPO / 'docs' / 'research' / 'parse_failure_inventory_20260507.csv'

# Judges to consider
JUDGE_NAMES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro', 'gemini'}


def classify(row):
    """Return failure_class (or 'ok' if not a failure)."""
    score = row.get('score')
    raw = row.get('raw_response') or row.get('raw') or ''
    pf = row.get('parse_failure', False)

    # Determine if this is a failure
    is_failure = pf or score in (0, None)
    if not is_failure and isinstance(score, int) and 1 <= score <= 5:
        return 'ok', raw

    if isinstance(raw, str):
        if '429' in raw or 'Too Many Requests' in raw:
            return 'http_429', raw[:200]
        if '403' in raw or 'Forbidden' in raw:
            return 'http_403', raw[:200]
        if 'Client error' in raw or 'Server error' in raw or '500' in raw or '502' in raw or '503' in raw:
            return 'http_other_err', raw[:200]
        if not raw or raw.strip() == '':
            return 'empty_response', ''
        if not re.search(r'[1-5]', raw):
            return 'no_score_extracted', raw[:200]
    if isinstance(score, int) and (score < 1 or score > 5):
        return 'out_of_range', f'score={score}'
    return 'score_zero', raw[:200] if isinstance(raw, str) else ''


def detect_judge(filename):
    """Extract judge name from filename like 'baselayer_judgments_gpt4o.json'."""
    m = re.search(r'_judgments_(haiku|sonnet|opus|gpt4o|gpt54|gemini_flash|gemini_pro|gemini)(?:\.|_)', filename)
    return m.group(1) if m else None


def detect_subject(subject_dir_name):
    """e.g. 'global_keckley' -> 'global_keckley'; keep raw."""
    return subject_dir_name


def write_inventory():
    rows = []
    files_scanned = 0
    files_skipped = 0

    for subject_dir in sorted(RESULTS.iterdir()):
        if not subject_dir.is_dir():
            continue
        subj = detect_subject(subject_dir.name)
        if subj in ('judge_calibration', 'multimodel', '_s114_backfills', '_tier2', '_wrong_spec_v2',
                    'franklin_legacy_20260411'):
            continue
        for jf in subject_dir.glob('*judgments*.json'):
            # Skip merged files for inventory; they're derived
            if 'merged' in jf.name:
                continue
            judge = detect_judge(jf.name)
            if judge is None:
                continue
            try:
                data = json.load(jf.open(encoding='utf-8'))
            except Exception:
                files_skipped += 1
                continue
            if not isinstance(data, list):
                continue
            files_scanned += 1
            for r in data:
                if not isinstance(r, dict):
                    continue
                if 'condition' not in r or 'question_id' not in r:
                    continue
                # Per-row judge: prefer record's own judge field
                row_judge = r.get('judge', judge)
                cls, excerpt = classify(r)
                if cls == 'ok':
                    continue
                rows.append({
                    'subject': subj,
                    'condition': r.get('condition', '?'),
                    'question_id': r.get('question_id'),
                    'judge': row_judge,
                    'judgment_file_path': str(jf.relative_to(REPO)).replace('\\', '/'),
                    'failure_class': cls,
                    'raw_response_excerpt': excerpt[:200] if isinstance(excerpt, str) else str(excerpt)[:200],
                    'score': r.get('score'),
                })

    # Annotate rescued: cross-check S114 backfills
    backfill_dir = RESULTS / '_s114_backfills'
    rescued_keys = set()  # (subject, condition, qid, judge)
    for f in backfill_dir.glob('*.json'):
        try:
            data = json.load(f.open(encoding='utf-8'))
        except Exception:
            continue
        # filename: subject__condition__judge.json
        m = re.match(r'(.+?)__(.+?)__(.+)\.json', f.name)
        if not m:
            continue
        s, c, j = m.group(1), m.group(2), m.group(3)
        for r in data:
            if isinstance(r, dict) and not r.get('parse_failure') and r.get('score') in (1, 2, 3, 4, 5):
                rescued_keys.add((s, c, r.get('question_id'), j))

    for row in rows:
        key = (row['subject'], row['condition'], row['question_id'], row['judge'])
        row['s114_backfill_rescued'] = key in rescued_keys

    # Write
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ['subject', 'condition', 'question_id', 'judge',
              'judgment_file_path', 'failure_class', 'score',
              'raw_response_excerpt', 's114_backfill_rescued']
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f'Files scanned: {files_scanned}')
    print(f'Files skipped: {files_skipped}')
    print(f'Failure rows: {len(rows)}')
    print(f'Rescued by S114 backfills: {sum(1 for r in rows if r["s114_backfill_rescued"])}')
    print(f'Still unrescued: {sum(1 for r in rows if not r["s114_backfill_rescued"])}')

    # By judge
    by_j = defaultdict(int)
    by_j_unr = defaultdict(int)
    for r in rows:
        by_j[r['judge']] += 1
        if not r['s114_backfill_rescued']:
            by_j_unr[r['judge']] += 1
    print('\nBy judge (total / unrescued):')
    for j in sorted(by_j, key=lambda x: -by_j[x]):
        print(f'  {j:<14} {by_j[j]:>5} / {by_j_unr[j]:>5}')

    # By failure class
    by_c = defaultdict(int)
    by_c_unr = defaultdict(int)
    for r in rows:
        by_c[r['failure_class']] += 1
        if not r['s114_backfill_rescued']:
            by_c_unr[r['failure_class']] += 1
    print('\nBy failure class (total / unrescued):')
    for c in sorted(by_c, key=lambda x: -by_c[x]):
        print(f'  {c:<25} {by_c[c]:>5} / {by_c_unr[c]:>5}')

    print(f'\nWrote {OUT_CSV}')


if __name__ == '__main__':
    write_inventory()
