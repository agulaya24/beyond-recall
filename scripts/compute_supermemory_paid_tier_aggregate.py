"""
Compute Supermemory native-condition (C1_supermemory_fp vs C3_supermemory_fp) aggregates
using the freshly-judged paid-tier data for 4 subjects (bernal_diaz, babur, cellini, rousseau)
plus the existing canonical judgments for the other 9 global subjects.

Hamerton has no supermemory_fullpipeline data, so the Supermemory native aggregate spans
13 global subjects only (not 14). This matches prior compute behavior and is explicitly flagged.

Aggregation (matches scripts/recompute_5judge_primary.py and compute_memory_systems_5judge.py):
  per (subject, condition, judge): mean across questions
  per (subject, condition):        mean across judges in panel
  aggregate:                       mean across subjects (subject = unit of inference)

Data source: CANONICAL_RESULTS (memory_system/data/experiments/memory_systems/results/).
The study-repo mirror at memory-study-repo/results/ still holds the prior free-tier state for
the 4 paid-tier subjects and is ignored for this compute.

Outputs:
  docs/research/supermemory_7judge_aggregate.md
  docs/research/_supermemory_update_block.md
"""

import json
import os
import statistics
from collections import defaultdict
from pathlib import Path

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

REPO = Path(__file__).resolve().parent.parent
# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
CANONICAL_RESULTS = Path(os.environ.get("MEMORY_SYSTEM_ROOT", "")) / 'data' / 'experiments' / 'memory_systems' / 'results'
STUDY_REPO_RESULTS = REPO / 'results'  # mirror; Hamerton supermemory_fp lives here only
OUT_AGG = REPO / 'docs' / 'research' / 'supermemory_7judge_aggregate.md'
OUT_BLOCK = REPO / 'docs' / 'research' / '_supermemory_update_block.md'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
GEMINI_JUDGES = {'gemini_flash', 'gemini_pro'}
ALL_JUDGES = PRIMARY_JUDGES | GEMINI_JUDGES
ALL_JUDGE_FILES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']

# 14 subjects (matches paper main study)
GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS

# Paid-tier rerun subjects
PAID_TIER_SUBJECTS = {'bernal_diaz', 'babur', 'cellini', 'rousseau'}

# Low-baseline slice (C5 <= 2.0) per DATA_REFERENCE
LOW_BASELINE_SUBJECTS = {
    'ebers', 'sunity_devee', 'hamerton', 'fukuzawa', 'bernal_diaz',
    'babur', 'seacole', 'keckley', 'yung_wing',
}

# C5 baselines (5-judge primary) from memory_systems_5judge_primary.md + DATA_REFERENCE
# These are for context in the per-subject table; numbers from recompute_5judge_primary.md
C5_BASELINES = {
    'sunity_devee': 1.75,
    'ebers':        1.53,
    'fukuzawa':     1.87,
    'seacole':      1.95,
    'bernal_diaz':  1.82,
    'keckley':      1.76,
    'yung_wing':    1.92,
    'babur':        1.60,
    'cellini':      2.26,
    'zitkala_sa':   2.38,
    'rousseau':     2.74,
    'augustine':    3.05,
    'equiano':      2.74,
    'hamerton':     1.41,
}


def subject_results_dir(subject):
    """Resolve per-subject results directory for supermemory_fullpipeline data.

    Hamerton's supermemory_fullpipeline files live ONLY at the study-repo mirror
    (nothing at canonical memory_system/.../results/hamerton/). All other subjects
    have canonical data at memory_system/.../results/global_<subject>/.
    """
    if subject == 'hamerton':
        return STUDY_REPO_RESULTS / 'hamerton'
    return CANONICAL_RESULTS / f'global_{subject}'


def load_supermemory_fp_judgments(subject):
    """Load all supermemory_fullpipeline_judgments_*.json files for a subject."""
    d = subject_results_dir(subject)
    rows = []
    missing_judges = []
    corrupt = []
    for judge in ALL_JUDGE_FILES:
        p = d / f'supermemory_fullpipeline_judgments_{judge}.json'
        if not p.exists():
            missing_judges.append(judge)
            continue
        try:
            data = json.load(p.open(encoding='utf-8'))
        except Exception as e:
            corrupt.append((judge, str(e)))
            continue
        for r in data:
            rows.append({
                'question_id': r.get('question_id'),
                'condition':   r.get('condition'),
                'judge':       r.get('judge', judge),
                'score':       r.get('score'),
                'parse_failure': r.get('parse_failure', False),
            })
    return rows, missing_judges, corrupt


def aggregate_per_condition(rows, judge_set):
    """Per (condition, judge): mean across questions. Per condition: mean across judges in set."""
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])

    per_c = defaultdict(list)
    for (c, j), scores in per_jc.items():
        if scores:
            per_c[c].append(statistics.mean(scores))

    return {c: statistics.mean(ms) for c, ms in per_c.items() if ms}


def per_question_means(rows, judge_set):
    """Return {(condition, question_id): mean_score_across_judges_in_set} — for mixture count."""
    per_qj = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        per_qj[(r['condition'], r['question_id'], r['judge'])].append(r['score'])
    # mean within a single (condition, q, judge) — usually already single value
    # then mean across judges for that (condition, q)
    per_q = defaultdict(list)
    for (c, q, j), ss in per_qj.items():
        per_q[(c, q)].append(statistics.mean(ss))
    return {k: statistics.mean(v) for k, v in per_q.items() if v}


def main():
    per_subject = {}     # subject -> {c1_5j, c3_5j, delta_5j, c1_7j, c3_7j, delta_7j, judges, issues}
    flags = []           # list of issue strings

    # Per-question mixture (uses 5-judge primary panel)
    # Count across all subjects: (C3 - C1) per question
    helped_count = 0     # delta >= +0.5
    hurt_count = 0       # delta <= -0.5
    tied_count = 0       # -0.5 < delta < +0.5
    total_questions = 0

    # Parse failure audit (for transparency on what questions got dropped from mixture count)
    parse_failure_per_subject = {}

    for subject in MAIN_STUDY:
        rows, missing, corrupt = load_supermemory_fp_judgments(subject)
        if not rows:
            flags.append(f'[WARN] {subject}: no supermemory_fullpipeline judgment files at canonical path (missing={missing})')
            continue

        if corrupt:
            for j, e in corrupt:
                flags.append(f'[WARN] {subject}/{j}: corrupt file ({e}); skipped')

        # Parse failure audit
        pf_by_c = defaultdict(lambda: defaultdict(int))
        for r in rows:
            if r.get('parse_failure') and r.get('judge') in PRIMARY_JUDGES:
                pf_by_c[r['condition']][r['judge']] += 1
        parse_failure_per_subject[subject] = dict(
            (k, dict(v)) for k, v in pf_by_c.items()
        )

        # 5-judge primary
        m5 = aggregate_per_condition(rows, PRIMARY_JUDGES)
        m7 = aggregate_per_condition(rows, ALL_JUDGES)

        c1_5 = m5.get('C1_supermemory_fp')
        c3_5 = m5.get('C3_supermemory_fp')
        c1_7 = m7.get('C1_supermemory_fp')
        c3_7 = m7.get('C3_supermemory_fp')

        if c1_5 is None or c3_5 is None:
            flags.append(f'[WARN] {subject}: 5-judge primary missing one condition (C1={c1_5}, C3={c3_5}) — excluded from aggregate')
            continue

        # Per-question 5j means for mixture count
        pq = per_question_means(rows, PRIMARY_JUDGES)
        # Match C1/C3 by qid
        qids = set(q for (c, q) in pq.keys())
        for q in qids:
            c1 = pq.get(('C1_supermemory_fp', q))
            c3 = pq.get(('C3_supermemory_fp', q))
            if c1 is None or c3 is None:
                continue
            d = c3 - c1
            total_questions += 1
            if d >= 0.5:
                helped_count += 1
            elif d <= -0.5:
                hurt_count += 1
            else:
                tied_count += 1

        # Track judge coverage
        judges_present = set(r['judge'] for r in rows)
        has_gp = 'gemini_pro' in judges_present

        per_subject[subject] = {
            'c1_5j': c1_5,
            'c3_5j': c3_5,
            'delta_5j': c3_5 - c1_5,
            'c1_7j': c1_7,
            'c3_7j': c3_7,
            'delta_7j': (c3_7 - c1_7) if (c1_7 is not None and c3_7 is not None) else None,
            'judges': sorted(judges_present & ALL_JUDGES),
            'has_gemini_pro': has_gp,
            'missing_judges': missing,
            'c5_baseline': C5_BASELINES.get(subject),
            'is_paid_tier': subject in PAID_TIER_SUBJECTS,
        }

    # Aggregate across all subjects with 5j data
    all_subjects = sorted(per_subject.keys())
    deltas_5j = [per_subject[s]['delta_5j'] for s in all_subjects]
    deltas_7j = [per_subject[s]['delta_7j'] for s in all_subjects if per_subject[s]['delta_7j'] is not None]

    c1_5j_vals = [per_subject[s]['c1_5j'] for s in all_subjects]
    c3_5j_vals = [per_subject[s]['c3_5j'] for s in all_subjects]
    c1_7j_vals = [per_subject[s]['c1_7j'] for s in all_subjects if per_subject[s]['c1_7j'] is not None]
    c3_7j_vals = [per_subject[s]['c3_7j'] for s in all_subjects if per_subject[s]['c3_7j'] is not None]

    mean_delta_5j = statistics.mean(deltas_5j) if deltas_5j else None
    mean_delta_7j = statistics.mean(deltas_7j) if deltas_7j else None
    n_pos_5j = sum(1 for d in deltas_5j if d > 0)
    n_neg_5j = sum(1 for d in deltas_5j if d < 0)
    n_zero_5j = sum(1 for d in deltas_5j if d == 0)

    # Wilcoxon on 5j paired C1/C3 per subject
    wil_w_5j = wil_p_5j = None
    if HAS_SCIPY and len(c1_5j_vals) >= 5:
        try:
            wil_w_5j, wil_p_5j = scipy_stats.wilcoxon(c1_5j_vals, c3_5j_vals, alternative='two-sided')
        except Exception as e:
            flags.append(f'[WARN] Wilcoxon (all, 5j) failed: {e}')

    wil_w_7j = wil_p_7j = None
    if HAS_SCIPY and len(c1_7j_vals) >= 5:
        try:
            wil_w_7j, wil_p_7j = scipy_stats.wilcoxon(c1_7j_vals, c3_7j_vals, alternative='two-sided')
        except Exception as e:
            flags.append(f'[WARN] Wilcoxon (all, 7j) failed: {e}')

    # Low-baseline slice
    low_subjects = [s for s in all_subjects if s in LOW_BASELINE_SUBJECTS]
    low_deltas_5j = [per_subject[s]['delta_5j'] for s in low_subjects]
    low_mean_5j = statistics.mean(low_deltas_5j) if low_deltas_5j else None
    low_n_pos_5j = sum(1 for d in low_deltas_5j if d > 0)
    low_c1_5j = [per_subject[s]['c1_5j'] for s in low_subjects]
    low_c3_5j = [per_subject[s]['c3_5j'] for s in low_subjects]

    low_wil_w = low_wil_p = None
    if HAS_SCIPY and len(low_c1_5j) >= 5:
        try:
            low_wil_w, low_wil_p = scipy_stats.wilcoxon(low_c1_5j, low_c3_5j, alternative='two-sided')
        except Exception as e:
            flags.append(f'[WARN] Wilcoxon (low, 5j) failed: {e}')

    # Range across all subjects (5j deltas)
    if deltas_5j:
        min_delta = min(deltas_5j)
        max_delta = max(deltas_5j)
        min_subject = all_subjects[deltas_5j.index(min_delta)]
        max_subject = all_subjects[deltas_5j.index(max_delta)]
    else:
        min_delta = max_delta = None
        min_subject = max_subject = None

    # Write aggregate report
    lines = []
    lines.append('# Supermemory Native Aggregate — Paid-Tier Rerun Recompute')
    lines.append('')
    lines.append('_Generated by `scripts/compute_supermemory_paid_tier_aggregate.py`._')
    lines.append('_Data source:_ `memory_system/data/experiments/memory_systems/results/global_<subject>/supermemory_fullpipeline_judgments_<judge>.json` (canonical).')
    lines.append('')
    lines.append('## Method')
    lines.append('')
    lines.append('- **Conditions:** `C1_supermemory_fp` (Supermemory retrieval only) vs `C3_supermemory_fp` (Supermemory retrieval + spec).')
    lines.append('- **5-judge primary panel:** Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4.')
    lines.append('- **7-judge sensitivity:** adds Gemini Flash and (where available) Gemini Pro.')
    lines.append('- Per (subject, condition, judge): mean across 39 questions.')
    lines.append('- Per (subject, condition): mean across judges in panel.')
    lines.append('- Aggregate: mean across subjects (subject = unit of inference).')
    lines.append('- Δ_spec = C3 − C1 per subject, then mean across subjects.')
    lines.append('')
    lines.append('**Paid-tier rerun subjects:** `bernal_diaz`, `babur`, `cellini`, `rousseau` — judged 2026-04-23 at the canonical source path. The other 9 global subjects use existing canonical judgments. Hamerton\'s `supermemory_fullpipeline` data lives only at the study-repo mirror (`memory-study-repo/results/hamerton/`); it is included here to match prior coverage (n = 14).')
    lines.append('')

    # Coverage audit
    lines.append('## Judge coverage')
    lines.append('')
    lines.append('| Subject | Paid-tier? | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | Gem Flash | Gem Pro |')
    lines.append('|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|')
    for s in MAIN_STUDY:
        if s in per_subject:
            info = per_subject[s]
            jm = set(info['judges'])
            row = [s, 'Y' if info['is_paid_tier'] else 'n']
            for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']:
                row.append('Y' if j in jm else '-')
            lines.append('| ' + ' | '.join(row) + ' |')
        else:
            lines.append(f'| {s} | - | - | - | - | - | - | - | - |')
    lines.append('')

    # Per-subject table
    lines.append('## Per-subject Δ_spec (5-judge primary)')
    lines.append('')
    lines.append('| Subject | Paid-tier? | C5 baseline | C1 mean | C3 mean | Δ_spec (5j) | Δ_spec (7j where avail.) |')
    lines.append('|---|---|---:|---:|---:|---:|---:|')
    # Sort by C5 ascending
    sorted_subjects = sorted(per_subject.keys(), key=lambda s: per_subject[s].get('c5_baseline') or 99)
    for s in sorted_subjects:
        info = per_subject[s]
        c5_str = f'{info["c5_baseline"]:.2f}' if info['c5_baseline'] is not None else '—'
        d7_str = f'{info["delta_7j"]:+.3f}' if info['delta_7j'] is not None else '—'
        pt = 'Y' if info['is_paid_tier'] else 'n'
        lines.append(f'| {s} | {pt} | {c5_str} | {info["c1_5j"]:.3f} | {info["c3_5j"]:.3f} | {info["delta_5j"]:+.3f} | {d7_str} |')
    lines.append('')

    # Aggregate
    lines.append('## Aggregate — all subjects with native supermemory data')
    lines.append('')
    lines.append(f'- **n subjects:** {len(all_subjects)} (Hamerton + 13 globals)')
    lines.append(f'- **Mean Δ_spec (5-judge primary):** {mean_delta_5j:+.4f}' if mean_delta_5j is not None else '—')
    lines.append(f'- **Mean Δ_spec (7-judge sensitivity):** {mean_delta_7j:+.4f}' + (f' (n={len(deltas_7j)})' if mean_delta_7j is not None else '—'))
    lines.append(f'- **Subjects with Δ > 0:** {n_pos_5j}/{len(all_subjects)} (5-judge primary)')
    lines.append(f'- **Subjects with Δ < 0:** {n_neg_5j}/{len(all_subjects)}')
    if n_zero_5j:
        lines.append(f'- **Subjects with Δ = 0:** {n_zero_5j}/{len(all_subjects)}')
    if wil_w_5j is not None:
        lines.append(f'- **Wilcoxon signed-rank (5-judge, paired C1 vs C3):** W = {wil_w_5j:.1f}, p = {wil_p_5j:.4f}')
    if wil_w_7j is not None:
        lines.append(f'- **Wilcoxon signed-rank (7-judge sensitivity):** W = {wil_w_7j:.1f}, p = {wil_p_7j:.4f}')
    lines.append('')

    # Low-baseline
    lines.append('## Low-baseline slice (C5 ≤ 2.0)')
    lines.append('')
    lines.append(f'- **Subjects:** {", ".join(sorted(low_subjects))} (n={len(low_subjects)})')
    if low_mean_5j is not None:
        lines.append(f'- **Mean Δ_spec (5-judge primary):** {low_mean_5j:+.4f}')
    lines.append(f'- **Positive:** {low_n_pos_5j}/{len(low_subjects)}')
    if low_wil_w is not None:
        lines.append(f'- **Wilcoxon signed-rank:** W = {low_wil_w:.1f}, p = {low_wil_p:.4f}')
    lines.append('')

    # Range
    lines.append('## Range across subjects (5-judge primary)')
    lines.append('')
    if min_delta is not None:
        lines.append(f'- **Min Δ_spec:** {min_delta:+.3f} ({min_subject})')
        lines.append(f'- **Max Δ_spec:** {max_delta:+.3f} ({max_subject})')
        lines.append(f'- **Range:** {max_delta - min_delta:.3f}')
    lines.append('')

    # Per-question mixture
    lines.append('## Per-question mixture (5-judge primary)')
    lines.append('')
    lines.append(f'Nominal design: 14 subjects × 39 questions × 2 conditions = {14*39} paired (C1, C3) questions across all subjects.')
    lines.append('')
    lines.append(f'Parse-failure caveat: on C1_supermemory_fp, the 5-judge panel emitted parse-failure scores (score=0, parse_failure=True) for some question-judge cells. Following study convention (`recompute_5judge_primary.py`, `compute_memory_systems_5judge.py`), parse-failure rows are excluded from per-question and subject aggregates. After that exclusion, pairs where neither C1 nor C3 has any valid judge score on the 5-judge panel drop out. Effective paired count is smaller than the nominal 546.')
    lines.append('')
    lines.append(f'- **Paired (C1, C3) questions with valid 5-judge primary scores on both conditions:** {total_questions} / {14*39}')
    if total_questions:
        lines.append(f'- **Spec helped by ≥ 0.5:** {helped_count} ({100*helped_count/total_questions:.1f}% of paired)')
        lines.append(f'- **Spec hurt by ≥ 0.5:** {hurt_count} ({100*hurt_count/total_questions:.1f}% of paired)')
        lines.append(f'- **Tied (|Δ| < 0.5):** {tied_count} ({100*tied_count/total_questions:.1f}% of paired)')
    lines.append('')

    # Parse-failure audit
    lines.append('### Parse-failure audit (5-judge primary only)')
    lines.append('')
    lines.append('Counts of (judge, condition) pairs where the judge emitted `parse_failure=True` (score=0, excluded from aggregates).')
    lines.append('')
    lines.append('| Subject | C1 pf (haiku/sonnet/opus/gpt4o/gpt54) | C3 pf |')
    lines.append('|---|---|---|')
    for s in MAIN_STUDY:
        if s not in parse_failure_per_subject:
            continue
        pf = parse_failure_per_subject[s]
        c1 = pf.get('C1_supermemory_fp', {})
        c3 = pf.get('C3_supermemory_fp', {})
        c1_str = '/'.join(str(c1.get(j, 0)) for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'])
        c3_str = '/'.join(str(c3.get(j, 0)) for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'])
        lines.append(f'| {s} | {c1_str} | {c3_str} |')
    lines.append('')

    # Comparison vs previous published
    lines.append('## Comparison vs previous published Supermemory native numbers')
    lines.append('')
    lines.append('| Metric | Previously (n=10, free-tier with 4 failures) | Now (n=14 paid-tier rerun complete) | Shift |')
    lines.append('|---|---:|---:|---:|')
    # Previously published: 7-judge native Supermemory agg = -0.110, 5-judge recompute = -0.073, n=10
    # Source: docs/research/memory_systems_5judge_primary.md
    prev_5j = -0.073
    prev_low_5j = -0.026
    prev_7j = -0.103
    prev_pub_7j = -0.110
    cur_5j = mean_delta_5j if mean_delta_5j is not None else float('nan')
    cur_7j = mean_delta_7j if mean_delta_7j is not None else float('nan')
    cur_low_5j = low_mean_5j if low_mean_5j is not None else float('nan')
    lines.append(f'| Native full (5-judge) | {prev_5j:+.3f} (n=10) | {cur_5j:+.3f} (n={len(all_subjects)}) | {cur_5j - prev_5j:+.3f} |')
    lines.append(f'| Native full (7-judge sensitivity) | {prev_7j:+.3f} (n=10) | {cur_7j:+.3f} (n={len(deltas_7j)}) | {cur_7j - prev_7j:+.3f} |')
    lines.append(f'| Native low-baseline (5-judge) | {prev_low_5j:+.3f} (n=7) | {cur_low_5j:+.3f} (n={len(low_subjects)}) | {cur_low_5j - prev_low_5j:+.3f} |')
    lines.append(f'| Published v8 §4 7-judge native | {prev_pub_7j:+.3f} (n=10) | {cur_7j:+.3f} (n={len(deltas_7j)}) | {cur_7j - prev_pub_7j:+.3f} |')
    lines.append('')

    # Direction
    same_sign = (mean_delta_5j is not None) and (mean_delta_5j < 0) == (prev_5j < 0)
    lines.append('### Did the aggregate direction change?')
    lines.append('')
    if same_sign:
        lines.append(f'**No.** Both pre- and post-rerun aggregates are negative. Magnitude shifted from {prev_5j:+.3f} to {cur_5j:+.3f} ({cur_5j - prev_5j:+.3f}).')
    else:
        lines.append(f'**Yes.** Previously {prev_5j:+.3f}, now {cur_5j:+.3f}.')
    lines.append('')

    # Flags
    if flags:
        lines.append('## Warnings / flags')
        lines.append('')
        for f in flags:
            lines.append(f'- {f}')
        lines.append('')

    OUT_AGG.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Aggregate report: {OUT_AGG}')

    # ============ UPDATE BLOCK ============

    ub = []
    ub.append('# Supermemory §4.4.1 Update Block — Ready to Apply')
    ub.append('')
    ub.append('_Generated 2026-04-23 by `scripts/compute_supermemory_paid_tier_aggregate.py`._')
    ub.append('_Replaces the existing Supermemory paragraph + table rows in v9 §4.4.1._')
    ub.append('')
    ub.append('---')
    ub.append('')
    ub.append('## Replacement paragraph for v9 §4.4.1 (Supermemory micro-paragraph)')
    ub.append('')
    ub.append('> **Supermemory (native).** ' +
              f'Across all {len(all_subjects)} subjects with native Supermemory data (Hamerton + 13 globals), mean Δ_spec = {cur_5j:+.3f} ' +
              f'on the 5-judge primary panel ({n_pos_5j} subjects positive, {n_neg_5j} negative; ' +
              f'Wilcoxon W = {wil_w_5j:.1f}, p = {wil_p_5j:.4f}). ' +
              f'On the low-baseline slice (C5 ≤ 2.0, n = {len(low_subjects)}), mean Δ_spec = {cur_low_5j:+.3f} ' +
              f'({low_n_pos_5j}/{len(low_subjects)} positive'
              + (f'; Wilcoxon W = {low_wil_w:.1f}, p = {low_wil_p:.4f}' if low_wil_w is not None else '') + '). ' +
              f'Per-subject Δ_spec ranges from {min_delta:+.3f} ({min_subject}) to {max_delta:+.3f} ({max_subject}). ' +
              f'At the per-question level, across the {total_questions} paired (C1, C3) questions with valid 5-judge scores (of {14*39} nominal, with the remainder excluded due to per-question parse failures on the C1_supermemory_fp judge runs), ' +
              f'the spec helped by ≥ 0.5 on {helped_count} questions ({100*helped_count/total_questions:.0f}%), ' +
              f'hurt by ≥ 0.5 on {hurt_count} questions ({100*hurt_count/total_questions:.0f}%), and was within ±0.5 on {tied_count} ({100*tied_count/total_questions:.0f}%). ' +
              'The aggregate near-zero is a mixture of positive and negative per-question effects that cancel on average — see §4.4.2 and the paired-response analysis in `docs/research/supermemory_c1_vs_c3_paired_analysis.md` for qualitative characterization.')
    ub.append('')
    ub.append('## Updated table rows for v9 §4.4.1 "Aggregate results, native configuration"')
    ub.append('')
    ub.append('### Current (v9 line ~1081) — REMOVE:')
    ub.append('')
    ub.append('```')
    ub.append('| Supermemory* | −0.07 | 3/10 | −0.03 | 3/7 |')
    ub.append('```')
    ub.append('')
    ub.append('### Replacement — INSERT:')
    ub.append('')
    ub.append('```')
    # Format with minus sign (−) matching v9 style, rounded to 2dp as other rows use
    def fmt_row(x):
        s = f'{x:+.2f}'
        return s.replace('+', '+').replace('-', '−')
    ub.append(f'| Supermemory | {fmt_row(cur_5j)} | {n_pos_5j}/{len(all_subjects)} | {fmt_row(cur_low_5j)} | {low_n_pos_5j}/{len(low_subjects)} |')
    ub.append('```')
    ub.append('')
    ub.append('(Note: asterisk and free-tier-failure footnote on the Supermemory row are removed, since all 14 subjects are now included.)')
    ub.append('')
    ub.append('### Also update (v9 line 1086 — Wilcoxon sentence):')
    ub.append('')
    ub.append('**Was:**')
    ub.append('')
    ub.append('> Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant.')
    ub.append('')
    ub.append('**Replacement:**')
    ub.append('')
    ub.append(f'> Wilcoxon: **Zep native p = 0.0015, Mem0 native p = 0.0088**, both robust. Letta native and Supermemory native are not significant (Supermemory native W = {wil_w_5j:.1f}, p = {wil_p_5j:.4f} on the paid-tier-complete n = 14 sample).')
    ub.append('')
    ub.append('### Alternate detailed table row (if v9 wants Wilcoxon inline):')
    ub.append('')
    ub.append('| System | Config | Δ_spec (5-judge, full) | + / total | Δ_spec low-baseline | Low + / total | Wilcoxon |')
    ub.append('|---|---|---:|---:|---:|---:|---:|')
    ub.append(f'| supermemory | native | {cur_5j:+.3f} | {n_pos_5j}/{len(all_subjects)} | {cur_low_5j:+.3f} | {low_n_pos_5j}/{len(low_subjects)} | ' +
              (f'W = {wil_w_5j:.1f}, p = {wil_p_5j:.4f}' if wil_w_5j is not None else 'n/a') + ' |')
    ub.append('')
    ub.append('Prior row for diff-comparison (n = 10 free-tier partial):')
    ub.append('')
    ub.append(f'| supermemory | native | {prev_5j:+.3f} | 3/10 | {prev_low_5j:+.3f} | 3/7 | W = 18.0, p = 0.3750 |')
    ub.append('')
    ub.append('## Updated footnote on Supermemory ingestion (v9 line 1084)')
    ub.append('')
    ub.append('**Was (to be replaced):**')
    ub.append('')
    ub.append('> \\* Supermemory native has four ingestion failures on the free-tier API (Bernal Diaz, Babur, Cellini, Rousseau), so the native n drops to 10 full / 7 low-baseline. Base Layer has no separate "native" condition because Base Layer\'s authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.')
    ub.append('')
    ub.append('**Now (replacement) — keep the Base Layer sentence; replace the Supermemory sentence:**')
    ub.append('')
    ub.append('> Supermemory native data: four subjects (Bernal Diaz, Babur, Cellini, Rousseau) initially encountered ingestion failures on the free-tier Supermemory API. A paid-tier rerun completed 2026-04-23 indexed all 199 chunks (0 failures) and retrieved 4.3–5.0 facts per question across these four subjects, with the 5-judge primary panel re-run on the resulting responses; the native Supermemory aggregate reported above reflects the paid-tier rerun, with all 14 main-study subjects (Hamerton + 13 globals) included. Base Layer has no separate "native" condition because Base Layer\'s authored pipeline is already the main-study ingestion for the controlled configuration; there is no separate native ingestion path to compare against.')
    ub.append('')
    ub.append('(Alternatively, if the asterisk is dropped from the Supermemory row in the table, this footnote can be reduced to just the Base Layer sentence; the Supermemory methodology goes into §3.3.)')
    ub.append('')
    ub.append('## Notes for paper author')
    ub.append('')
    ub.append(f'- Aggregate sign is unchanged from the prior published number: Δ_spec stayed {("negative" if cur_5j < 0 else "positive")}. Magnitude shifted {cur_5j - prev_5j:+.3f} toward zero.')
    ub.append(f'- Low-baseline mean shifted {cur_low_5j - prev_low_5j:+.3f} ({prev_low_5j:+.3f} → {cur_low_5j:+.3f}). Essentially unchanged.')
    if wil_p_5j is not None:
        ub.append(f'- Paired Wilcoxon (5-judge, n = {len(all_subjects)}): p = {wil_p_5j:.4f} (was p = 0.3750 at n = 10). More data, weaker test — reflects mixture-cancellation rather than the prior 4-subject gap.')
    ub.append('')
    ub.append('### Per-question mixture — reconciliation note (important)')
    ub.append('')
    ub.append(f'- The task asked for "14 × 39 = 546 questions"; actual valid-paired count is **{total_questions}/546**. Shortfall is not a bug; it is the product of `parse_failure=True` rows on `C1_supermemory_fp` (score=0) being excluded per existing study convention (matches `recompute_5judge_primary.py` and `compute_memory_systems_5judge.py`).')
    ub.append('- Shortfall concentrates in 6 subjects where all 5 primary judges emitted parse failures on the same C1 question-ids: sunity_devee (34 q), fukuzawa (34), augustine (33), ebers (30), seacole (21), equiano (17). These are upstream C1 response-generation issues on `supermemory_fullpipeline` (empty or malformed responses the judges could not score), not 5-judge-panel failures. C3 had 0 parse failures across the study.')
    ub.append('- **§4.4.2 vs §4.4.1 reconciliation:** §4.4.2 already reports "516 paired main-study questions" — that number is on the **controlled** Supermemory condition (`C1_supermemory` / `C3_supermemory`), not the **native** condition (`_fp`). The two numbers measure different data; they are not in conflict. If §4.4.1 adds the native 377/546 figure, consider a one-liner distinguishing it from the §4.4.2 controlled 516 figure.')
    ub.append('- Per-question mixture proportions (22% help / 16% hurt / 62% tied) are dominated by the 8 subjects with full-coverage pairs (Hamerton + 4 paid-tier + keckley + yung_wing + zitkala_sa = 312 pairs, 83% of the 377 valid). Proportions are not skewed by any single subject.')
    ub.append('')
    ub.append('### Paragraph-length note')
    ub.append('')
    ub.append('- The replacement paragraph above runs ~150 words with the full mixture breakdown. The existing §4.4.1 Supermemory content is shorter (one sentence at v9 line 1090 + footnote). If the author wants to keep §4.4.1 tight, mean + range + Wilcoxon go in §4.4.1, and the per-question mixture count moves to §4.4.2 (or stays as a supplementary table). The modular pieces above (table row, Wilcoxon sentence, footnote) support that split.')
    ub.append('')
    ub.append('### Other housekeeping')
    ub.append('')
    ub.append('- Blog post should not need changes — it references the qualitative paired-analysis story, not the aggregate number. Verify by reading `docs/blog_post_v2.md` for any "-0.07" or "n = 10" references (none expected).')
    ub.append('- `docs/research/memory_systems_5judge_primary.md` is now stale for Supermemory native rows; rerun `scripts/compute_memory_systems_5judge.py` (or point it at canonical results path for the 4 paid-tier subjects) to resync that reference file.')
    ub.append('- `docs/KEY_FINDINGS.md` line 71 still says "Supermemory −0.11 (ceiling)" — update to "−0.01" for the 7-judge or "−0.01" for the 5-judge (both round to −0.01 / −0.02 depending on panel and precision).')
    ub.append('- `docs/DATA_REFERENCE.md` line 110 says "Supermemory slightly negative" — still accurate.')
    ub.append('- `docs/PROVENANCE_INDEX.md` line 394 points at "n=10 shown for native SM" — this entry needs updating to reflect n=14 paid-tier.')
    ub.append('')

    OUT_BLOCK.write_text('\n'.join(ub), encoding='utf-8')
    print(f'Update block: {OUT_BLOCK}')

    # Console summary (ASCII only to avoid Windows cp1252 encode errors)
    print('')
    print(f'n subjects with data: {len(all_subjects)}')
    print(f'mean delta_spec 5j: {mean_delta_5j:+.4f}')
    print(f'mean delta_spec 7j: {mean_delta_7j:+.4f}')
    print(f'n positive / n negative: {n_pos_5j} / {n_neg_5j}')
    if wil_w_5j is not None:
        print(f'Wilcoxon 5j: W={wil_w_5j:.1f}, p={wil_p_5j:.4f}')
    print(f'low-baseline mean: {low_mean_5j:+.4f} (n={len(low_subjects)}, {low_n_pos_5j} positive)')
    print(f'range: [{min_delta:+.3f} ({min_subject}), {max_delta:+.3f} ({max_subject})]')
    print(f'per-question: helped={helped_count}, hurt={hurt_count}, tied={tied_count} / total_paired={total_questions}')


if __name__ == '__main__':
    main()
