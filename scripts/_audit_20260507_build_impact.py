"""Build parse_failure_impact_20260507.csv

For each (subject, condition) cell with unrescued parse failures, identify which
paper claims depend on that cell. Uses the v11_emit JSON files + DATA_REFERENCE
+ KEY_FINDINGS as the impact map.

Strategy:
  - Load the inventory CSV
  - Aggregate failures to (subject, condition) cells
  - For each cell, classify into impact tier:
      tier_1_section_4_table  — cell appears in §4.1/§4.2/§4.4 main tables
      tier_2_subsection_text  — cell powers a per-system or per-subject claim
      tier_3_appendix         — cell appears only in appendix tables
      tier_4_no_paper_link    — cell is in pipeline but not cited
  - Look up the relevant paper line numbers
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
INV_CSV = REPO / 'docs' / 'research' / 'parse_failure_inventory_20260507.csv'
OUT_CSV = REPO / 'docs' / 'research' / 'parse_failure_impact_20260507.csv'
PAPER = REPO / 'docs' / 'beyond_recall_v11_8_draft.md'

# Map condition prefix -> impact category
GRADIENT_CONDS = {'C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                  'C4_factdump', 'C4a_full_facts_plus_spec',
                  'C4_full', 'C2a_full', 'C2c_full', 'C4a_full', 'C5_full',
                  'C4a_full_all_facts_plus_spec', 'C2c_full_wrong_spec',
                  'C4_full_factdump', 'C4a_full_facts_plus_spec'}
RETRIEVAL_CONDS = {'C8_raw_corpus', 'C9_raw_corpus_plus_spec'}

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}


def cell_paper_impact(subject, condition, judge_failure_count):
    """Return (paper_line_hint, section, table_or_text, severity).

    severity:
      P0 if affecting an aggregate cell on §4.1, §4.2, §4.4 main tables (5-judge primary)
      P1 if affecting case-study subsection numbers (e.g. §4.4.4 Q21)
      P2 if affecting appendix only
      P3 if affecting 7-judge sensitivity only or no clear link
    """
    # Strip 'global_' prefix
    subj = subject.replace('global_', '')

    if judge_failure_count == 'gemini_flash' or judge_failure_count == 'gemini_pro':
        # Only affects 7-judge sensitivity panel claims
        return ('§4.6 sensitivity', '7-judge sensitivity panel', 'P3', 'gemini-only — affects 7-judge α only')

    if condition in GRADIENT_CONDS:
        return ('§4.1 lines 805-819', '§4.1 gradient table', 'P0',
                f'{condition} appears in §4.1 14-row gradient + abstract / §1.3 callouts')
    if condition in RETRIEVAL_CONDS:
        return ('§4.2.1 / §4.4.1', '§4.2 retrieval-overlap', 'P0',
                f'{condition} powers C8/C9 retrieval-overlap aggregates')
    # Memory system conditions
    for system in ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']:
        if condition == f'C1_{system}' or condition == f'C3_{system}':
            return (f'§4.4.1 line 1290-1303', f'§4.4 memory-systems aggregate ({system})', 'P0',
                    f'{condition} powers controlled-config aggregate Δ for {system}')
        if condition == f'C1_{system}_fullpipeline' or condition == f'C3_{system}_fullpipeline':
            return (f'§4.4.1 line 1290-1303', f'§4.4 memory-systems aggregate ({system}, native)', 'P0',
                    f'{condition} powers native-config aggregate Δ for {system}; SM 4-subject gap noted at line 1304 footnote')
    return ('?', 'unknown', 'P3', 'no clear paper link')


def main():
    rows = list(csv.DictReader(INV_CSV.open(encoding='utf-8')))
    # Filter unrescued only
    unrescued = [r for r in rows if r['s114_backfill_rescued'] != 'True']
    print(f'Total inventory rows: {len(rows)}; unrescued: {len(unrescued)}')

    # Aggregate by (subject, condition)
    cells = defaultdict(lambda: {'judges': defaultdict(int), 'qids': set(), 'classes': defaultdict(int)})
    for r in unrescued:
        key = (r['subject'], r['condition'])
        cells[key]['judges'][r['judge']] += 1
        cells[key]['qids'].add(int(r['question_id']))
        cells[key]['classes'][r['failure_class']] += 1

    impact_rows = []
    for (subj, cond), info in cells.items():
        primary_failed = sum(info['judges'][j] for j in info['judges'] if j in PRIMARY_JUDGES)
        gemini_failed = sum(info['judges'][j] for j in info['judges'] if j.startswith('gemini'))
        n_judges_affected = len(info['judges'])
        # Determine if 5-judge panel is affected
        five_judge_affected = primary_failed > 0
        # Use one judge for impact lookup heuristic
        lookup_judge = 'haiku' if 'haiku' in info['judges'] else next(iter(info['judges']))
        if not five_judge_affected and gemini_failed > 0:
            lookup_judge = 'gemini_flash'
        line, section, severity, notes = cell_paper_impact(subj, cond, lookup_judge)
        impact_rows.append({
            'subject': subj,
            'condition': cond,
            'paper_section': section,
            'paper_line_hint': line,
            'severity': severity,
            'judges_affected': ';'.join(sorted(info['judges'].keys())),
            'primary_judge_failures': primary_failed,
            'gemini_failures': gemini_failed,
            'n_questions_affected': len(info['qids']),
            'failure_classes': ';'.join(f'{c}={n}' for c, n in info['classes'].items()),
            'notes': notes,
        })

    # Write
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ['subject', 'condition', 'paper_section', 'paper_line_hint', 'severity',
              'judges_affected', 'primary_judge_failures', 'gemini_failures',
              'n_questions_affected', 'failure_classes', 'notes']
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted(impact_rows, key=lambda x: (x['severity'], -x['primary_judge_failures'])):
            w.writerow(r)

    print(f'\nUnique (subject, condition) cells with unrescued failures: {len(impact_rows)}')
    sev_count = defaultdict(int)
    for r in impact_rows:
        sev_count[r['severity']] += 1
    print('\nBy severity:')
    for s, n in sorted(sev_count.items()):
        print(f'  {s}: {n}')
    print(f'\nWrote {OUT_CSV}')


if __name__ == '__main__':
    main()
