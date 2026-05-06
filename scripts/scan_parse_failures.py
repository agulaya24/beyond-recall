"""
Scan every *_judgments_*.json file under results/ and count rows that are
either parse_failure=true or have score=0/None without a real judgment.

Goal: enumerate the full set of rows that need re-judging before §4 drafts.
"""

import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

# Judge names we expect
JUDGE_NAMES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro'}


def is_parse_failure(row):
    """A row is a parse failure if parse_failure=true OR (score in (0, None) AND no raw_response evidence of success)."""
    if row.get('parse_failure') is True:
        return True
    score = row.get('score')
    if score in (0, None):
        return True
    return False


def scan_file(path):
    """Yield (condition, judge, count_pf, total) summaries from one judgment file."""
    try:
        data = json.load(path.open(encoding='utf-8'))
    except Exception:
        try:
            data = json.load(path.open(encoding='latin-1'))
        except Exception as e:
            return [('__ERROR__', str(e), 0, 0)]
    if not isinstance(data, list):
        return []

    # Detect wide-format vs long-format
    if data and all(k in data[0] for k in ('question_id', 'condition', 'judge', 'score')):
        # Standard long format
        agg = defaultdict(lambda: [0, 0])  # (condition, judge) -> [pf, total]
        for r in data:
            cond = r.get('condition', '?')
            judge = r.get('judge', '?')
            agg[(cond, judge)][1] += 1
            if is_parse_failure(r):
                agg[(cond, judge)][0] += 1
        return [(c, j, pf, total) for (c, j), (pf, total) in agg.items()]

    # Wide format? (haiku_score, gemini_score, ...)
    if data and ('haiku_score' in data[0] or 'gemini_score' in data[0]):
        agg = defaultdict(lambda: [0, 0])
        for r in data:
            cond = r.get('condition', '?')
            for col, judge in [('haiku_score', 'haiku'), ('gemini_score', 'gemini_flash'),
                               ('gpt54_score', 'gpt54'), ('gemini_pro_score', 'gemini_pro'),
                               ('sonnet_score', 'sonnet'), ('opus_score', 'opus'),
                               ('gpt4o_score', 'gpt4o')]:
                if col in r:
                    agg[(cond, judge)][1] += 1
                    v = r.get(col)
                    if v in (0, None):
                        agg[(cond, judge)][0] += 1
        return [(c, j, pf, total) for (c, j), (pf, total) in agg.items()]

    return []


def main():
    total_pf = 0
    total_rows = 0
    by_subject = defaultdict(lambda: [0, 0])   # subject -> [pf, total]
    by_judge = defaultdict(lambda: [0, 0])     # judge -> [pf, total]
    by_file = []                               # (path, pf, total)

    per_cell = defaultdict(lambda: [0, 0])     # (subject, condition, judge) -> [pf, total]

    for subj_dir in sorted(RESULTS.iterdir()):
        if not subj_dir.is_dir():
            continue
        subject = subj_dir.name
        if subject in ('judge_calibration', 'multimodel'):
            continue
        for jf in subj_dir.glob('*judgments*.json'):
            summary = scan_file(jf)
            file_pf, file_total = 0, 0
            for (c, j, pf, total) in summary:
                if c == '__ERROR__':
                    print(f'  ERROR {jf}: {j}')
                    continue
                file_pf += pf
                file_total += total
                by_subject[subject][0] += pf
                by_subject[subject][1] += total
                by_judge[j][0] += pf
                by_judge[j][1] += total
                per_cell[(subject, c, j)][0] += pf
                per_cell[(subject, c, j)][1] += total
            if file_total > 0:
                by_file.append((str(jf.relative_to(REPO)), file_pf, file_total))
            total_pf += file_pf
            total_rows += file_total

    print(f'\nTotal rows scanned: {total_rows}')
    print(f'Total parse failures: {total_pf} ({100*total_pf/total_rows:.2f}%)')
    print()

    print('By judge:')
    for judge in sorted(by_judge, key=lambda x: -by_judge[x][0]):
        pf, tot = by_judge[judge]
        print(f'  {judge:<14} {pf:>6} / {tot:>6} ({100*pf/tot:.2f}%)')

    print()
    print('By subject (top 15 by pf count):')
    for subject in sorted(by_subject, key=lambda x: -by_subject[x][0])[:15]:
        pf, tot = by_subject[subject]
        print(f'  {subject:<20} {pf:>6} / {tot:>6} ({100*pf/tot:.2f}%)')

    print()
    print('Top 25 (subject, condition, judge) cells with most parse failures:')
    cells_sorted = sorted(per_cell.items(), key=lambda x: -x[1][0])
    for (s, c, j), (pf, tot) in cells_sorted[:25]:
        if pf == 0:
            break
        print(f'  {s:<20} {c:<45} {j:<14} {pf:>4} / {tot:>4}')

    # Save backfill manifest
    manifest = []
    for (s, c, j), (pf, tot) in cells_sorted:
        if pf > 0:
            manifest.append({
                'subject': s,
                'condition': c,
                'judge': j,
                'parse_failures': pf,
                'total_rows': tot,
                'rerun_needed': pf > 0,
            })
    out = REPO / 'docs' / 'research' / 's114_parse_failure_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f'\nManifest: {out}')


if __name__ == '__main__':
    main()
