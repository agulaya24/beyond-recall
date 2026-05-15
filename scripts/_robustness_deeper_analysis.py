"""Deeper analysis on the 25-cell rubric-robustness sample.

1. Per-baseline-band Spearman rho + mean D.
2. Spot-check Babur C4a q2 and Equiano C5 q13.
3. Slope / ceiling under new rubric on the 25 cells.
"""
import csv
import json
from pathlib import Path
import statistics

REPO = Path(__file__).resolve().parents[1]
CSV_PATH = REPO / 'docs' / 'research' / 'published_rubric_robustness_check_20260508.csv'

# Subject baselines (C5_baseline 5-judge primary mean) from
# DATA_REFERENCE.md §1 per-subject table. These are study-level baselines, not
# the cell-level scores in our 25-cell sample.
SUBJECT_C5_MEAN = {
    'hamerton': 1.26,
    'global_ebers': 1.02,
    'global_sunity_devee': 1.03,
    'global_yung_wing': 1.88,
    'global_babur': 1.76,
    'global_equiano': 2.77,
}


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def spearman(xs, ys):
    def rank(vs):
        sv = sorted([(v, i) for i, v in enumerate(vs)])
        out = [0.0] * len(vs)
        i = 0
        while i < len(sv):
            j = i
            while j + 1 < len(sv) and sv[j + 1][0] == sv[i][0]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[sv[k][1]] = avg
            i = j + 1
        return out
    return pearson(rank(xs), rank(ys))


def main():
    rows = list(csv.DictReader(CSV_PATH.open(encoding='utf-8')))
    for r in rows:
        for k, v in list(r.items()):
            if k in ('subject', 'paper_cond', 'raw_cond_label'):
                continue
            try:
                r[k] = float(v) if '.' in v else int(v)
            except ValueError:
                pass
        r['subj_c5_baseline'] = SUBJECT_C5_MEAN.get(r['subject'])
        r['baseline_band'] = 'low' if (r['subj_c5_baseline'] is not None and r['subj_c5_baseline'] <= 2.0) else 'high'

    print('=== Per-cell (subject, cond, qid, orig_mean, new_mean, delta, baseline_band) ===')
    for r in sorted(rows, key=lambda x: (x['baseline_band'], x['subject'], x['paper_cond'])):
        print(f"  [{r['baseline_band']:4s}] {r['subject']:<22s} {r['paper_cond']:<12s} q{r['qid']:>3} "
              f"orig={r['orig_mean']:.2f} new={r['new_mean']:.2f} D={r['delta_new_minus_orig']:+.2f}")

    print('\n=== Per-baseline-band stats ===')
    for band in ['low', 'high']:
        sub = [r for r in rows if r['baseline_band'] == band]
        if not sub:
            continue
        deltas = [r['delta_new_minus_orig'] for r in sub]
        orig = [r['orig_mean'] for r in sub]
        new = [r['new_mean'] for r in sub]
        print(f'\n  Band: {band}-baseline (n={len(sub)})')
        print(f'    Subjects: {sorted(set(r["subject"] for r in sub))}')
        print(f'    Spearman rho (orig vs new): {spearman(orig, new):.3f}')
        print(f'    Pearson r (orig vs new):  {pearson(orig, new):.3f}')
        print(f'    Mean D:    {sum(deltas)/len(deltas):+.3f}')
        print(f'    SD D:      {statistics.pstdev(deltas) if len(deltas) > 1 else 0:.3f}')
        print(f'    D range:   [{min(deltas):+.2f}, {max(deltas):+.2f}]')
        print(f'    Median D:  {statistics.median(deltas):+.2f}')

    print('\n=== Per-condition stats (any band) ===')
    by_cond = {}
    for r in rows:
        by_cond.setdefault(r['paper_cond'], []).append(r)
    for pc in sorted(by_cond):
        sub = by_cond[pc]
        deltas = [r['delta_new_minus_orig'] for r in sub]
        orig = [r['orig_mean'] for r in sub]
        new = [r['new_mean'] for r in sub]
        print(f"  {pc}: n={len(sub)} mean_orig={sum(orig)/len(orig):.2f} mean_new={sum(new)/len(new):.2f} mean_D={sum(deltas)/len(deltas):+.3f} rho={spearman(orig, new) if len(set(orig)) > 1 else 'n/a'}")

    # Slope / ceiling under new rubric
    print('\n=== Gradient slope and ceiling under new rubric (C5 vs C4a, 25-cell sample) ===')
    # Compute per-subject mean C5 and C4a under new rubric
    c5 = {r['subject']: r['new_mean'] for r in rows if r['paper_cond'] == 'C5_baseline'}
    c4a = {r['subject']: r['new_mean'] for r in rows if r['paper_cond'] == 'C4a'}
    print('  Per-subject (subject: C5_new, C4a_new, D_new) — note: each subject has only one C5 and one C4a sampled cell:')
    paired_subjs = sorted(set(c5) & set(c4a))
    if paired_subjs:
        for s in paired_subjs:
            print(f'    {s:<22s} C5_new={c5[s]:.2f}  C4a_new={c4a[s]:.2f}  D_new={c4a[s]-c5[s]:+.2f}')
        # Equivalent original numbers
        print('  Per-subject (subject: C5_orig, C4a_orig, D_orig):')
        c5_o = {r['subject']: r['orig_mean'] for r in rows if r['paper_cond'] == 'C5_baseline'}
        c4a_o = {r['subject']: r['orig_mean'] for r in rows if r['paper_cond'] == 'C4a'}
        for s in paired_subjs:
            if s in c5_o and s in c4a_o:
                print(f'    {s:<22s} C5_orig={c5_o[s]:.2f}  C4a_orig={c4a_o[s]:.2f}  D_orig={c4a_o[s]-c5_o[s]:+.2f}')

    print('\n=== Spot-check candidates (largest |D|) ===')
    big = sorted(rows, key=lambda r: abs(r['delta_new_minus_orig']), reverse=True)[:5]
    for r in big:
        print(f"  {r['subject']}/{r['paper_cond']}/q{r['qid']}: orig={r['orig_mean']:.2f} new={r['new_mean']:.2f} D={r['delta_new_minus_orig']:+.2f}")

    # Now write spot-check materials to file (UTF-8) since console is cp1252
    print('\n=== Writing spot-check materials to spotcheck_text.md ===')
    spotcheck = [('global_babur', 'C4a', 2), ('global_equiano', 'C5_baseline', 13), ('global_equiano', 'C4a', 27)]
    out_lines = ['# Spot-check texts for rubric-robustness divergence cells\n']
    for subj, cond, qid in spotcheck:
        sd = REPO / 'results' / subj
        from importlib.machinery import SourceFileLoader
        mod = SourceFileLoader('rrr', str(REPO / 'scripts' / 'published_rubric_robustness_20260508.py')).load_module()
        resp = mod.find_response(sd, qid, cond)
        if not resp:
            out_lines.append(f'## {subj}/{cond}/q{qid}: response not found\n')
            continue
        orig = mod.find_original_scores(sd, qid, resp['raw_cond_label'])
        new_files = list((REPO / 'results' / '_published_rubric_robustness_20260508' / subj).glob(f'{cond}_q{qid}_*.json'))
        new_per_judge = {}
        for f in new_files:
            d = json.loads(f.read_text(encoding='utf-8'))
            new_per_judge[d['judge']] = d.get('paper_rubric_score')
        out_lines.append(f'## {subj} / {cond} / q{qid}\n')
        out_lines.append(f'**Raw condition label:** `{resp["raw_cond_label"]}`')
        out_lines.append(f'**Original 5-judge scores:** {orig}')
        out_lines.append(f'**Paper-rubric 5-judge scores:** {new_per_judge}')
        out_lines.append(f'**Original mean:** {sum(orig.values())/5:.2f}')
        out_lines.append(f'**Paper-rubric mean:** {sum(v for v in new_per_judge.values() if v is not None)/5:.2f}\n')
        out_lines.append('### Question')
        out_lines.append(f'{resp["question_text"]}\n')
        out_lines.append('### Held-out passage')
        out_lines.append(f'{resp["held_out"]}\n')
        out_lines.append('### Response (first 1500 chars)')
        out_lines.append(f'{resp["response_text"][:1500]}\n')
        out_lines.append('---\n')
    out_path = REPO / 'docs' / 'research' / '_spotcheck_rubric_robustness_20260508.md'
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'Wrote: {out_path}')


if __name__ == '__main__':
    main()
