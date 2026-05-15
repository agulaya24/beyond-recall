"""Dry-run: just call sample_cells() and print the picks. No API calls."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from published_rubric_robustness_n100_20260508 import sample_cells, EXCLUDED_QIDS_BY_PAPERCOND

cells = sample_cells()
print(f'\n=== {len(cells)} new cells sampled ===\n')

by_subj_cond = {}
for c in cells:
    by_subj_cond.setdefault((c['subject'], c['paper_cond']), []).append(c['qid'])

for (subj, pc), qids in sorted(by_subj_cond.items()):
    excluded = {qid for (s, qid) in EXCLUDED_QIDS_BY_PAPERCOND.get(pc, set()) if s == subj}
    overlap = set(qids) & excluded
    flag = ' [OVERLAP WITH SEED=42!]' if overlap else ''
    print(f'  {subj}/{pc}: qids={sorted(qids)} (excluded seed=42: {sorted(excluded)}){flag}')

# By condition
print('\n=== Cells per condition ===')
by_cond = {}
for c in cells:
    by_cond.setdefault(c['paper_cond'], []).append(c['subject'])
for pc, subjs in sorted(by_cond.items()):
    print(f'  {pc}: {len(subjs)} cells')

# By subject
print('\n=== Cells per subject ===')
by_subj = {}
for c in cells:
    by_subj.setdefault(c['subject'], []).append(c['paper_cond'])
for s, conds in sorted(by_subj.items()):
    print(f'  {s}: {len(conds)} cells (across {len(set(conds))} conditions)')
