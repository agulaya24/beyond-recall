"""Aggregate the 7-judge calibration matrix across all calibration JSONs.

Mean convention. Matches the v11 paper's _v11_emit_3_study_design.py: parse-failure
sentinel 0 is *included* in the mean denominator (not skipped). Skipping 0s would
give a different (higher) Gemini Pro number than the paper reports. Sonnet and Opus
have zero parse failures so the convention does not affect their values.
"""
import json, pathlib
from collections import defaultdict

OUTDIR = pathlib.Path('results/judge_calibration')

sources = {
    'haiku':        ('judgments.json',              'haiku'),
    'gemini_flash': ('judgments.json',              'gemini'),
    'gpt4o':        ('gpt4o_calibration.json',      'gpt4o_score'),
    'gpt54':        ('gpt54_calibration.json',      'gpt54_score'),
    'gemini_pro':   ('gemini_pro_calibration.json', 'gemini_pro_score'),
    'sonnet':       ('sonnet_calibration.json',     'sonnet_score'),
    'opus':         ('opus_calibration.json',       'opus_score'),
}

means = defaultdict(dict)
dists = defaultdict(dict)   # nonzero-only, score 1..5
ns = defaultdict(dict)      # n used in mean (includes parse failures = 0)
n_zero = defaultdict(dict)  # parse-failure count
for jname, (fn, key) in sources.items():
    rows = json.load(open(OUTDIR / fn))
    for test in ['verbatim', 'paraphrased', 'short_correct', 'long_correct']:
        all_scores = [r[key] for r in rows
                      if r.get('test') == test and r.get(key) is not None]
        nz = [s for s in all_scores if s > 0]
        means[jname][test] = sum(all_scores) / len(all_scores) if all_scores else 0
        dists[jname][test] = [nz.count(i) for i in range(1, 6)]
        ns[jname][test] = len(all_scores)
        n_zero[jname][test] = len(all_scores) - len(nz)

print('Test                 Haiku  Sonnet   Opus  GFlash  GPT-4o  GemPro  GPT-5.4')
print('=' * 76)
order = ['haiku', 'sonnet', 'opus', 'gemini_flash', 'gpt4o', 'gemini_pro', 'gpt54']
for test in ['verbatim', 'paraphrased', 'short_correct', 'long_correct']:
    line = f'  {test:<18}'
    for j in order:
        line += f' {means[j][test]:>7.2f}'
    print(line)

print()
print('Distributions ([1,2,3,4,5] counts; parse failures separate):')
for j in order:
    print(f'\n  {j}:')
    for test in ['verbatim', 'paraphrased', 'short_correct', 'long_correct']:
        print(f'    {test:<16} dist={dists[j][test]} n={ns[j][test]} '
              f'parse_fail={n_zero[j][test]} mean={means[j][test]:.2f}')

out = {'means': dict(means), 'dists': dict(dists), 'ns': dict(ns), 'parse_failures': dict(n_zero)}
with open(OUTDIR / '_seven_judge_summary.json', 'w') as f:
    json.dump(out, f, indent=2)
print('\nSaved to', OUTDIR / '_seven_judge_summary.json')
