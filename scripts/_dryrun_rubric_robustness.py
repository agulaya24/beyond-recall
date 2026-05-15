"""Sanity-check the sampling for the rubric-robustness rerun (no API calls)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from published_rubric_robustness_20260508 import sample_cells, paper_rubric_prompt, PRIMARY_JUDGES

cells = sample_cells()
print(f'Sampled {len(cells)} cells')
print()
by_cond = {}
for c in cells:
    by_cond.setdefault(c['paper_cond'], []).append((c['subject'], c['qid']))
for pc, lst in sorted(by_cond.items()):
    print(f'{pc} (n={len(lst)}): {lst}')
print()
# Validate every cell has all original scores + non-trivial response
for c in cells:
    miss = [j for j in PRIMARY_JUDGES if j not in c['original_scores']]
    txt_len = len(c['response_text'])
    ho_len = len(c['held_out'] or '')
    flag = 'OK' if not miss and txt_len > 50 and ho_len > 5 else f'MISSING={miss} txt={txt_len} ho={ho_len}'
    print(f"{c['subject']}/{c['paper_cond']}/q{c['qid']} ({c['raw_cond_label']}) src={c['response_source_file']:<22s} orig_judges={list(c['original_scores'].keys())} {flag}")

# Print one example prompt
print('\n=== Example paper-rubric prompt for first cell ===\n')
ex = cells[0]
print(paper_rubric_prompt(ex['held_out'], ex['response_text'])[:1500])
