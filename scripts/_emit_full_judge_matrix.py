"""Emit the full per-subject by per-condition by per-judge mean-score matrix
for Appendix D.4 of v9. Writes a Markdown table to stdout and also as a
sidecar file at docs/research/s114_full_judge_matrix.md.

Matrix shape: 14 main-study subjects x 5 conditions (C5, C2a, C2c, C4, C4a)
x (5 primary judges + 2 Gemini) + 5-judge primary mean + 7-judge mean
= 14 x 5 = 70 rows, 9 columns (h, s, o, 4o, 54, gF, gP, 5m, 7m).
Total cells: 70 x 9 = 630. (Not 945; the 945 figure in the build report
conflated 15 subjects x 9 conditions x 7 judges, which is the full design
space; the appendix only needs the 5 primary gradient conditions.)
"""
import json
import sys
import statistics
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recompute_5judge_primary import (
    load_global_judgments, load_hamerton_judgments, GLOBAL_SUBJECTS,
)

REPO = Path(__file__).resolve().parent.parent
OUT_MD = REPO / 'docs' / 'research' / 's114_full_judge_matrix.md'

CONDITIONS = [
    ('C5_baseline', 'C5'),
    ('C2a_full_spec', 'C2a'),
    ('C2c_wrong_spec', 'C2c'),
    ('C4_factdump', 'C4'),
    ('C4a_full_facts_plus_spec', 'C4a'),
]
PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']
GEMINI_JUDGES = ['gemini_flash', 'gemini_pro']
JUDGE_ORDER = PRIMARY_JUDGES + GEMINI_JUDGES
JUDGE_DISPLAY = {
    'haiku': 'H', 'sonnet': 'S', 'opus': 'O',
    'gpt4o': '4o', 'gpt54': '5.4',
    'gemini_flash': 'gF', 'gemini_pro': 'gP',
}

SUBJECT_DISPLAY = {
    'hamerton': 'Hamerton',
    'sunity_devee': 'Sunity Devee',
    'ebers': 'Ebers',
    'fukuzawa': 'Fukuzawa',
    'seacole': 'Seacole',
    'bernal_diaz': 'Bernal Diaz',
    'keckley': 'Keckley',
    'yung_wing': 'Yung Wing',
    'babur': 'Babur',
    'cellini': 'Cellini',
    'zitkala_sa': 'Zitkala-Sa',
    'rousseau': 'Rousseau',
    'augustine': 'Augustine',
    'equiano': 'Equiano',
}

SUBJECTS = ['hamerton'] + GLOBAL_SUBJECTS


def per_judge_mean(rows, condition, judge):
    """Mean score for (condition, judge) across all questions."""
    scores = []
    for r in rows:
        if r.get('judge') != judge:
            continue
        if r.get('condition') != condition:
            continue
        s = r.get('score')
        if s is None or s <= 0:
            continue
        if r.get('parse_failure'):
            continue
        scores.append(s)
    if not scores:
        return None
    return statistics.mean(scores)


def fmt(x):
    if x is None:
        return 'n/a'
    return f'{x:.2f}'


def main():
    # Collect all rows
    all_subject_rows = {}
    for subject in SUBJECTS:
        if subject == 'hamerton':
            rows = load_hamerton_judgments()
        else:
            rows = load_global_judgments(subject)
        all_subject_rows[subject] = rows

    lines = []
    lines.append('# Full per-judge score matrix (Appendix D.4)')
    lines.append('')
    lines.append('Each cell is the per-judge mean score across all behavioral-prediction questions for a (subject, condition, judge) triple. Judges abbreviated: H=Haiku 4.5, S=Sonnet 4.6, O=Opus 4.6, 4o=GPT-4o, 5.4=GPT-5.4, gF=Gemini 2.5 Flash, gP=Gemini 2.5 Pro. 5m = 5-judge primary mean, 7m = 7-judge mean.')
    lines.append('')
    lines.append('"n/a" indicates missing judge-condition coverage (most commonly: Gemini judges not run on C2c or C4 for some subjects; see §4.5.2 on 5-judge vs 7-judge coverage).')
    lines.append('')

    header = '| Subject | Cond | ' + ' | '.join(JUDGE_DISPLAY[j] for j in JUDGE_ORDER) + ' | 5m | 7m |'
    sep = '|---|---|' + '|'.join(['---:'] * (len(JUDGE_ORDER) + 2)) + '|'
    lines.append(header)
    lines.append(sep)

    for subject in SUBJECTS:
        rows = all_subject_rows[subject]
        for cond_key, cond_label in CONDITIONS:
            judge_means = {}
            for judge in JUDGE_ORDER:
                judge_means[judge] = per_judge_mean(rows, cond_key, judge)
            # 5-judge primary mean
            primary_vals = [judge_means[j] for j in PRIMARY_JUDGES if judge_means[j] is not None]
            mean5 = statistics.mean(primary_vals) if len(primary_vals) >= 3 else None
            # 7-judge mean (only when all 7 present)
            all7_vals = [judge_means[j] for j in JUDGE_ORDER if judge_means[j] is not None]
            mean7 = statistics.mean(all7_vals) if len(all7_vals) >= 6 else None

            subj_disp = SUBJECT_DISPLAY.get(subject, subject) if cond_key == 'C5_baseline' else ''
            row = f'| {subj_disp} | {cond_label} | ' + ' | '.join(fmt(judge_means[j]) for j in JUDGE_ORDER) + f' | {fmt(mean5)} | {fmt(mean7)} |'
            lines.append(row)

    lines.append('')
    lines.append(f'Total cells: 14 subjects x 5 conditions x 9 columns = 630. Source: raw per-judge JSON files under `results/global_<subject>/*_judgments_<judge>.json` (global subjects) and `results/hamerton/` (Hamerton), aggregated via `scripts/_emit_full_judge_matrix.py`.')
    out = '\n'.join(lines)
    OUT_MD.write_text(out, encoding='utf-8')
    print(out)
    print(f'\nWrote: {OUT_MD}')


if __name__ == '__main__':
    main()
