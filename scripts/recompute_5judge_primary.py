"""
Recompute all primary results on the 5-judge primary panel (non-Gemini):
Haiku, Sonnet, Opus, GPT-4o, GPT-5.4.

Also computes the 7-judge sensitivity where available. Reports gaps honestly.

Outputs to docs/research/recompute_5judge_primary.md.
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT = REPO / 'docs' / 'research' / 'recompute_5judge_primary.md'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
GEMINI_JUDGES = {'gemini_flash', 'gemini_pro'}
ALL_JUDGES = PRIMARY_JUDGES | GEMINI_JUDGES

GRADIENT_CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                       'C4_factdump', 'C4a_full_facts_plus_spec']

# Global subjects ordered by C5 baseline (reported in DATA_REFERENCE)
GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]

MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS  # 14 subjects


def load_global_judgments(subject):
    """Returns list of {question_id, condition, judge, score} rows, with
    _s114_backfills/ files overlaid on top of the original per-judge data
    for any (question_id, condition, judge) where the backfill has a valid score."""
    path = RESULTS / f'global_{subject}' / 'judgments_v2.json'
    rows = []
    if path.exists():
        rows = json.load(path.open())

    # Load backfill overlay files for this subject
    backfill_dir = RESULTS / '_s114_backfills'
    overrides = {}  # (qid, condition, judge) -> (score, parse_failure)
    if backfill_dir.exists():
        prefix = f'global_{subject}__'
        for f in backfill_dir.glob(f'{prefix}*.json'):
            try:
                data = json.load(f.open())
            except Exception:
                continue
            for r in data:
                if r.get('score') is None:
                    continue
                overrides[(r['question_id'], r['condition'], r['judge'])] = (r['score'], r.get('parse_failure', False))

    # Apply overrides: update in place
    for r in rows:
        key = (r.get('question_id'), r.get('condition'), r.get('judge'))
        if key in overrides:
            score, pf = overrides[key]
            r['score'] = score
            r['parse_failure'] = pf
    return rows


def load_hamerton_judgments():
    """Load Hamerton judgments by merging data across multiple source files.

    Hamerton data is fragmented:
      - judgments_harmonized.json: long format, 7 judges, C5 + C4 only
      - judgments.json: wide format (haiku_score, gemini_score), spec conditions
      - gpt54_judgments.json: long format, gpt54 only, spec conditions
      - gemini_pro_judgments.json: long format, gemini_pro only, spec conditions
      - sonnet_judgments.json, opus_judgments.json, gpt4o_judgments.json: S114 backfill, long format

    Condition-name normalization:
      - Hamerton 'C2c_full_wrong_spec' -> normalized 'C2c_wrong_spec'
      - Hamerton 'C4a_full_all_facts_plus_spec' -> normalized 'C4a_full_facts_plus_spec'
    """
    base = RESULTS / 'hamerton'
    rows = []

    def normalize(cond):
        if cond == 'C2c_full_wrong_spec':
            return 'C2c_wrong_spec'
        if cond == 'C4a_full_all_facts_plus_spec':
            return 'C4a_full_facts_plus_spec'
        return cond

    # 1. Harmonized C5 + C4 long format (7 judges)
    harm = base / 'judgments_harmonized.json'
    if harm.exists():
        for r in json.load(harm.open()):
            rows.append({
                'question_id': r['question_id'],
                'condition': normalize(r['condition']),
                'judge': r['judge'],
                'score': r.get('score'),
                'parse_failure': r.get('parse_failure', False),
            })

    # 2. Wide-format judgments.json: haiku + gemini (flash) for spec conditions
    wide = base / 'judgments.json'
    if wide.exists():
        for r in json.load(wide.open()):
            cond = normalize(r['condition'])
            if 'haiku_score' in r:
                rows.append({
                    'question_id': r['question_id'],
                    'condition': cond,
                    'judge': 'haiku',
                    'score': r['haiku_score'],
                    'parse_failure': False,
                })
            if 'gemini_score' in r:
                rows.append({
                    'question_id': r['question_id'],
                    'condition': cond,
                    'judge': 'gemini_flash',
                    'score': r['gemini_score'],
                    'parse_failure': False,
                })

    # 3. gpt54_judgments.json (long, gpt54_score field)
    gpt54_path = base / 'gpt54_judgments.json'
    if gpt54_path.exists():
        for r in json.load(gpt54_path.open()):
            rows.append({
                'question_id': r['question_id'],
                'condition': normalize(r['condition']),
                'judge': 'gpt54',
                'score': r.get('gpt54_score'),
                'parse_failure': False,
            })

    # 4. gemini_pro_judgments.json (long, gemini_pro_score field)
    gp_path = base / 'gemini_pro_judgments.json'
    if gp_path.exists():
        for r in json.load(gp_path.open()):
            rows.append({
                'question_id': r['question_id'],
                'condition': normalize(r['condition']),
                'judge': 'gemini_pro',
                'score': r.get('gemini_pro_score'),
                'parse_failure': False,
            })

    # 5. S114 backfill (sonnet, opus, gpt4o in long format with 'judge' and 'score' keys)
    for judge in ['sonnet', 'opus', 'gpt4o']:
        p = base / f'{judge}_judgments.json'
        if p.exists():
            for r in json.load(p.open()):
                rows.append({
                    'question_id': r['question_id'],
                    'condition': normalize(r['condition']),
                    'judge': judge,
                    'score': r.get('score'),
                    'parse_failure': r.get('parse_failure', False),
                })

    return rows


def load_hamerton_fullstack():
    """Hamerton has a fullstack_haiku.json that may have the full condition matrix."""
    path = RESULTS / 'hamerton' / 'fullstack_haiku.json'
    if not path.exists():
        return []
    return json.load(path.open())


def mean_or_none(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def aggregate_per_subject_per_condition(rows, judge_set):
    """
    Given a list of {question_id, condition, judge, score} rows and a judge set,
    compute mean-per-judge-across-questions, then mean-across-judges-in-set,
    per (subject, condition).

    Returns {condition: mean_score} for the single subject whose rows were passed.
    """
    # First pass: per-judge per-condition mean across questions
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])

    # Second pass: mean across judges
    per_condition_means = defaultdict(list)
    for (condition, judge), scores in per_jc.items():
        if scores:
            per_condition_means[condition].append(statistics.mean(scores))

    return {c: statistics.mean(ms) for c, ms in per_condition_means.items() if ms}


def judge_coverage_for_subject(rows):
    return set(r['judge'] for r in rows)


def main():
    print(f'\nComputing 5-judge primary aggregates across {len(MAIN_STUDY)} subjects\n')

    subject_data = {}
    coverage_report = {}

    for subject in MAIN_STUDY:
        if subject == 'hamerton':
            rows = load_hamerton_judgments()
            source = 'judgments_harmonized.json'
        else:
            rows = load_global_judgments(subject)
            source = f'global_{subject}/judgments_v2.json'

        if not rows:
            print(f'  [WARN] {subject}: no judgment rows')
            continue

        coverage = judge_coverage_for_subject(rows)
        coverage_report[subject] = {
            'source': source,
            'n_rows': len(rows),
            'judges': sorted(coverage),
            'has_all_primary': PRIMARY_JUDGES.issubset(coverage),
            'has_gemini_flash': 'gemini_flash' in coverage,
            'has_gemini_pro': 'gemini_pro' in coverage,
        }

        # 5-judge primary
        primary_means = aggregate_per_subject_per_condition(rows, PRIMARY_JUDGES)
        # 6-judge (primary + flash)
        six_judge_means = aggregate_per_subject_per_condition(rows, PRIMARY_JUDGES | {'gemini_flash'})
        # 7-judge (primary + both Gemini)
        seven_judge_means = aggregate_per_subject_per_condition(rows, ALL_JUDGES)

        subject_data[subject] = {
            'primary_5': primary_means,
            'six_judge': six_judge_means,
            'seven_judge': seven_judge_means,
        }

        print(f'  {subject}: primary judges={sorted(coverage & PRIMARY_JUDGES)}, gemini={sorted(coverage & GEMINI_JUDGES)}')

    # Build gradient table: per subject, C5 + C2a + C4a for 5-judge primary
    print('\n\nGradient Table (5-judge primary)')
    print(f'{"subject":<15} {"C5":>6} {"C2a":>6} {"C4a":>6} {"d_spec":>8} {"d_c4a":>8}')
    gradient_rows = []
    for subject in MAIN_STUDY:
        if subject not in subject_data:
            continue
        p = subject_data[subject]['primary_5']
        c5 = p.get('C5_baseline')
        c2a = p.get('C2a_full_spec')
        c4a = p.get('C4a_full_facts_plus_spec')
        if c5 is None or c4a is None:
            continue
        delta_spec = (c2a - c5) if c2a is not None else None
        delta_c4a = c4a - c5
        gradient_rows.append({
            'subject': subject,
            'c5': c5, 'c2a': c2a, 'c4a': c4a,
            'delta_spec': delta_spec, 'delta_c4a': delta_c4a,
        })
        ds = f'{delta_spec:+.2f}' if delta_spec is not None else '  ---'
        print(f'{subject:<15} {c5:>6.2f} {(c2a or 0):>6.2f} {c4a:>6.2f} {ds:>8} {delta_c4a:>+8.2f}')

    # Sort by C5 ascending for the gradient view
    gradient_rows.sort(key=lambda r: r['c5'])

    # Linear regression: delta_c4a vs c5 (5-judge primary)
    c5_vals = [r['c5'] for r in gradient_rows]
    delta_c4a_vals = [r['delta_c4a'] for r in gradient_rows]

    if HAS_SCIPY and len(c5_vals) >= 3:
        slope, intercept, r_val, p_val, se = scipy_stats.linregress(c5_vals, delta_c4a_vals)
        r_sq = r_val ** 2
        n = len(c5_vals)
        df = n - 2
        t_crit = scipy_stats.t.ppf(0.975, df)
        ci_low = slope - t_crit * se
        ci_high = slope + t_crit * se

        # Wilcoxon paired tests
        c2a_vals = [r['c2a'] for r in gradient_rows if r['c2a'] is not None]
        c5_for_c2a = [r['c5'] for r in gradient_rows if r['c2a'] is not None]
        c4a_vals = [r['c4a'] for r in gradient_rows]

        w_spec, p_spec = scipy_stats.wilcoxon(c5_for_c2a, c2a_vals, alternative='two-sided')
        w_c4a, p_c4a = scipy_stats.wilcoxon(c5_vals, c4a_vals, alternative='two-sided')
    else:
        slope = intercept = r_sq = p_val = ci_low = ci_high = None
        w_spec = p_spec = w_c4a = p_c4a = None

    # 7-judge (where available) for comparison
    gradient_7j = []
    for subject in MAIN_STUDY:
        if subject not in subject_data:
            continue
        s7 = subject_data[subject]['seven_judge']
        c5 = s7.get('C5_baseline')
        c2a = s7.get('C2a_full_spec')
        c4a = s7.get('C4a_full_facts_plus_spec')
        if c5 is None or c4a is None:
            continue
        gradient_7j.append({
            'subject': subject,
            'c5': c5, 'c2a': c2a, 'c4a': c4a,
            'delta_spec': (c2a - c5) if c2a else None,
            'delta_c4a': c4a - c5,
            'n_judges': len(subject_data[subject]['seven_judge']),  # placeholder, recompute below
        })

    # Better 7-judge: count how many judges actually went into each
    # Use the coverage report directly to note the gap
    gradient_7j.sort(key=lambda r: r['c5'])
    c5_7j = [r['c5'] for r in gradient_7j]
    dc4a_7j = [r['delta_c4a'] for r in gradient_7j]

    if HAS_SCIPY and len(c5_7j) >= 3:
        slope_7j, intercept_7j, r7, p7, se7 = scipy_stats.linregress(c5_7j, dc4a_7j)
        r_sq_7j = r7 ** 2
        n7 = len(c5_7j)
        df7 = n7 - 2
        t_crit7 = scipy_stats.t.ppf(0.975, df7)
        ci_low_7j = slope_7j - t_crit7 * se7
        ci_high_7j = slope_7j + t_crit7 * se7
    else:
        slope_7j = r_sq_7j = p7 = None

    # Write report
    lines = []
    lines.append('# 5-Judge Primary Recompute Report')
    lines.append('')
    lines.append('_Generated by `scripts/recompute_5judge_primary.py`._')
    lines.append('')
    lines.append('## Judge coverage audit')
    lines.append('')
    lines.append('| Subject | Source | All 5 primary? | Flash? | Pro? | Effective panel |')
    lines.append('|---|---|---|---|---|---|')
    for subject, info in coverage_report.items():
        n_judges = len(set(info['judges']) & PRIMARY_JUDGES) + ('Flash' in info['judges'] if False else int(info['has_gemini_flash'])) + int(info['has_gemini_pro'])
        effective = len(set(info['judges']) & ALL_JUDGES)
        lines.append(f'| {subject} | {info["source"]} | {"Yes" if info["has_all_primary"] else "No"} | {"Yes" if info["has_gemini_flash"] else "No"} | {"Yes" if info["has_gemini_pro"] else "No"} | {effective}-judge |')
    lines.append('')

    lines.append('## Gradient table (5-judge primary)')
    lines.append('')
    lines.append('| Subject | C5 | C2a | C4a | Δ spec (C2a-C5) | Δ facts+spec (C4a-C5) |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for r in gradient_rows:
        ds = f'{r["delta_spec"]:+.2f}' if r['delta_spec'] is not None else '---'
        lines.append(f'| {r["subject"]} | {r["c5"]:.2f} | {(r["c2a"] or 0):.2f} | {r["c4a"]:.2f} | {ds} | {r["delta_c4a"]:+.2f} |')

    lines.append('')
    lines.append('## Gradient statistics')
    lines.append('')
    lines.append('**5-judge primary panel:**')
    if slope is not None:
        lines.append(f'- Slope: {slope:.4f}')
        lines.append(f'- Intercept: {intercept:.4f}')
        lines.append(f'- R²: {r_sq:.4f}')
        lines.append(f'- Correlation r: {r_val:.4f}')
        lines.append(f'- p-value (slope): {p_val:.6f}')
        lines.append(f'- 95% CI slope: [{ci_low:.4f}, {ci_high:.4f}]')
        lines.append(f'- N: {len(gradient_rows)}')
        lines.append('')
        lines.append('**Wilcoxon signed-rank (5-judge primary):**')
        if w_spec is not None:
            lines.append(f'- C5 vs C2a: W={w_spec:.1f}, p={p_spec:.6f}')
        if w_c4a is not None:
            lines.append(f'- C5 vs C4a: W={w_c4a:.1f}, p={p_c4a:.6f}')
    lines.append('')

    lines.append('## 7-judge sensitivity')
    lines.append('')
    lines.append('Note: Gemini Pro coverage is partial (3 of 13 globals have it: augustine, babur, bernal_diaz). The 7-judge aggregate uses whatever judges are available per subject; this is not a uniform 7-judge panel.')
    lines.append('')
    lines.append('| Subject | C5 | C2a | C4a | Δ facts+spec |')
    lines.append('|---|---:|---:|---:|---:|')
    for r in gradient_7j:
        lines.append(f'| {r["subject"]} | {r["c5"]:.2f} | {(r["c2a"] or 0):.2f} | {r["c4a"]:.2f} | {r["delta_c4a"]:+.2f} |')

    lines.append('')
    lines.append('**Sensitivity regression stats:**')
    if slope_7j is not None:
        lines.append(f'- Slope: {slope_7j:.4f}')
        lines.append(f'- R²: {r_sq_7j:.4f}')
        lines.append(f'- p-value: {p7:.6f}')
        lines.append(f'- 95% CI: [{ci_low_7j:.4f}, {ci_high_7j:.4f}]')
    lines.append('')

    lines.append('## Comparison vs published v6 numbers (7-judge)')
    lines.append('')
    lines.append('| Metric | Published (7-judge) | Recompute (5-judge primary) | Delta |')
    lines.append('|---|---:|---:|---:|')
    lines.append(f'| Gradient slope | -0.98 | {slope:.2f} | {slope - (-0.98):+.2f} |' if slope else '')
    lines.append(f'| Gradient R² | 0.82 (approx) | {r_sq:.2f} | {r_sq - 0.82:+.2f} |' if slope else '')
    lines.append(f'| Gradient p | <0.001 | {p_val:.6f} | — |' if slope else '')
    lines.append(f'| Wilcoxon C5-C4a W | 9.0 | {w_c4a:.1f} | {w_c4a - 9.0:+.1f} |' if w_c4a else '')
    lines.append(f'| Wilcoxon C5-C4a p | 0.006 | {p_c4a:.6f} | — |' if w_c4a else '')

    low_baseline_rows = [r for r in gradient_rows if r['c5'] <= 2.0]
    low_c4a_mean = statistics.mean(r['delta_c4a'] for r in low_baseline_rows) if low_baseline_rows else 0
    lines.append(f'| Low-baseline (C5≤2) n | 9 | {len(low_baseline_rows)} | {len(low_baseline_rows)-9:+d} |')
    lines.append(f'| Low-baseline mean Δ | +1.04 | {low_c4a_mean:+.3f} | {low_c4a_mean - 1.04:+.3f} |')

    low_positive = sum(1 for r in low_baseline_rows if r['delta_c4a'] > 0)
    lines.append(f'| Low-baseline positive | 9/9 | {low_positive}/{len(low_baseline_rows)} | — |')

    all_positive = sum(1 for r in gradient_rows if r['delta_c4a'] > 0)
    lines.append(f'| All-14 positive | 12/14 | {all_positive}/{len(gradient_rows)} | — |')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\n\nReport written: {OUT}')


if __name__ == '__main__':
    main()
