"""
Compute 5-judge primary (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) and 7-judge
sensitivity aggregate spec deltas for each memory system (Mem0, Letta, Zep,
Supermemory, Base Layer) in:
  - Controlled configuration:  C1_<sys>      vs C3_<sys>       (identical fact pool)
  - Native configuration:      C1_<sys>_fp   vs C3_<sys>_fp    (each system's own ingestion)

Base Layer has no native/fullpipeline variant (it IS the authored pipeline).
Supermemory native has known missing subjects (free-tier ingestion failures);
the script skips-not-crashes and reports effective n.

Aggregation (matches recompute_5judge_primary.py):
  per (subject, condition, judge): mean across questions
  per (subject, condition):        mean across judges in panel
  aggregate:                       mean across subjects (subject = unit of inference)

Outputs:
  docs/research/memory_systems_5judge_primary.md
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
RESULTS = REPO / 'results'
OUT = REPO / 'docs' / 'research' / 'memory_systems_5judge_primary.md'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
GEMINI_JUDGES = {'gemini_flash', 'gemini_pro'}
ALL_JUDGES = PRIMARY_JUDGES | GEMINI_JUDGES
JUDGE_FILES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']
# gemini_pro is often in a separate file or absent

# Subjects ordered by C5 baseline (from recompute_5judge_primary.md)
# 5-judge C5 values are used to define the low-baseline slice
GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS  # 14 subjects

# Low-baseline slice — 9 subjects with 5-judge C5 <= 2.0, matching the rest of the paper
# From docs/research/recompute_5judge_primary.md
LOW_BASELINE_SUBJECTS = {
    'ebers', 'sunity_devee', 'hamerton', 'fukuzawa', 'bernal_diaz',
    'babur', 'seacole', 'keckley', 'yung_wing',
}

SYSTEMS = ['mem0', 'letta', 'zep', 'supermemory', 'baselayer']

# Config-specific condition label patterns
def conditions_for(system, config):
    """Returns (c1_label, c3_label) for a system/config pair."""
    if config == 'controlled':
        return f'C1_{system}', f'C3_{system}'
    elif config == 'native':
        return f'C1_{system}_fp', f'C3_{system}_fp'
    raise ValueError(config)


def subject_results_dir(subject):
    """Resolve per-subject results directory. Hamerton is flat, others are global_*."""
    if subject == 'hamerton':
        return RESULTS / 'hamerton'
    return RESULTS / f'global_{subject}'


def load_memory_system_judgments(subject, system, config):
    """Load all judgment rows for (subject, system, config).

    Files follow:
      controlled: {system}_judgments_{judge}.json
      native:     {system}_fullpipeline_judgments_{judge}.json

    Returns list of {question_id, condition, judge, score, parse_failure}.
    Returns [] if data does not exist.
    """
    d = subject_results_dir(subject)
    rows = []

    if config == 'controlled':
        prefix = system
    elif config == 'native':
        prefix = f'{system}_fullpipeline'
    else:
        raise ValueError(config)

    # Load each per-judge file
    for judge in JUDGE_FILES:
        path = d / f'{prefix}_judgments_{judge}.json'
        if not path.exists():
            continue
        try:
            data = json.load(path.open(encoding='utf-8'))
        except Exception as e:
            print(f'  [WARN] failed to load {path}: {e}')
            continue
        for r in data:
            rows.append({
                'question_id': r.get('question_id'),
                'condition': r.get('condition'),
                'judge': r.get('judge', judge),
                'score': r.get('score'),
                'parse_failure': r.get('parse_failure', False),
            })

    # Optional gemini_pro file (only some subjects)
    gp_path = d / f'{prefix}_judgments_gemini_pro.json'
    if gp_path.exists():
        try:
            data = json.load(gp_path.open(encoding='utf-8'))
            for r in data:
                rows.append({
                    'question_id': r.get('question_id'),
                    'condition': r.get('condition'),
                    'judge': 'gemini_pro',
                    'score': r.get('score', r.get('gemini_pro_score')),
                    'parse_failure': r.get('parse_failure', False),
                })
        except Exception:
            pass

    return rows


def aggregate_per_condition(rows, judge_set):
    """
    Per (condition, judge): mean across questions.
    Per condition: mean across judges in judge_set.
    Returns {condition: mean_score}.
    """
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('score') is None:
            continue
        if r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])

    per_c = defaultdict(list)
    for (c, j), scores in per_jc.items():
        if scores:
            per_c[c].append(statistics.mean(scores))

    return {c: statistics.mean(ms) for c, ms in per_c.items() if ms}


def compute_system_config(system, config, judge_panel):
    """
    For a system × config, compute per-subject (C1, C3, Δ) and aggregates.

    Returns dict with:
      per_subject: {subject: {'c1': x, 'c3': y, 'delta': d}}
      agg: mean Δ across subjects with both C1 and C3
      n: count of subjects included
      positive: count with delta > 0
      low_agg: mean Δ on low-baseline slice
      low_n: count on low-baseline
      low_positive: positive count on low-baseline
      missing: list of subjects with no data
    """
    c1_label, c3_label = conditions_for(system, config)
    per_subject = {}
    missing = []

    for subject in MAIN_STUDY:
        rows = load_memory_system_judgments(subject, system, config)
        if not rows:
            missing.append(subject)
            continue
        means = aggregate_per_condition(rows, judge_panel)
        c1 = means.get(c1_label)
        c3 = means.get(c3_label)
        if c1 is None or c3 is None:
            missing.append(subject)
            continue
        per_subject[subject] = {'c1': c1, 'c3': c3, 'delta': c3 - c1}

    all_deltas = [v['delta'] for v in per_subject.values()]
    agg = statistics.mean(all_deltas) if all_deltas else None
    positive = sum(1 for d in all_deltas if d > 0)

    low_deltas = [v['delta'] for s, v in per_subject.items() if s in LOW_BASELINE_SUBJECTS]
    low_agg = statistics.mean(low_deltas) if low_deltas else None
    low_positive = sum(1 for d in low_deltas if d > 0)

    # Wilcoxon C1 vs C3
    c1_vals = [v['c1'] for v in per_subject.values()]
    c3_vals = [v['c3'] for v in per_subject.values()]
    wil_w, wil_p = None, None
    if HAS_SCIPY and len(c1_vals) >= 5:
        try:
            wil_w, wil_p = scipy_stats.wilcoxon(c1_vals, c3_vals, alternative='two-sided')
        except Exception:
            pass

    return {
        'per_subject': per_subject,
        'agg': agg,
        'n': len(per_subject),
        'positive': positive,
        'low_agg': low_agg,
        'low_n': len(low_deltas),
        'low_positive': low_positive,
        'missing': missing,
        'wil_w': wil_w,
        'wil_p': wil_p,
    }


def main():
    print('\nComputing memory systems spec deltas -- 5-judge primary and 7-judge sensitivity\n')

    results = {}  # {config: {system: {panel: {...}}}}

    for config in ['controlled', 'native']:
        results[config] = {}
        for system in SYSTEMS:
            # Base Layer has no native variant — skip
            if system == 'baselayer' and config == 'native':
                results[config][system] = {'primary_5': None, 'seven_judge': None,
                                           'note': 'No native variant exists — Base Layer IS the authored pipeline'}
                continue
            results[config][system] = {
                'primary_5': compute_system_config(system, config, PRIMARY_JUDGES),
                'seven_judge': compute_system_config(system, config, ALL_JUDGES),
            }
            p5 = results[config][system]['primary_5']
            p7 = results[config][system]['seven_judge']
            agg5 = f'{p5["agg"]:+.3f}' if p5['agg'] is not None else 'n/a'
            agg7 = f'{p7["agg"]:+.3f}' if p7['agg'] is not None else 'n/a'
            print(f'  {config:>10} | {system:<12} | 5j d={agg5} (n={p5["n"]}) | 7j d={agg7} (n={p7["n"]})'
                  + (f' | missing={len(p5["missing"])}' if p5['missing'] else ''))

    # Build markdown report
    lines = []
    lines.append('# Memory Systems Spec Deltas — 5-Judge Primary Recompute')
    lines.append('')
    lines.append('_Generated by `scripts/compute_memory_systems_5judge.py`._')
    lines.append('')
    lines.append('## Method')
    lines.append('')
    lines.append('- **Primary panel (5 judges):** Haiku 4.5, Sonnet 4.6, Opus 4.6, GPT-4o, GPT-5.4.')
    lines.append('- **7-judge sensitivity:** adds Gemini Flash and (where available) Gemini Pro.')
    lines.append('- Per (subject, condition, judge): mean across questions.')
    lines.append('- Per (subject, condition): mean across judges in panel.')
    lines.append('- Aggregate: mean across subjects (subject = unit of inference).')
    lines.append('- Δ_spec = mean(C3) − mean(C1) per subject, then mean across subjects.')
    lines.append('- Low-baseline slice: 9 subjects with 5-judge C5 ≤ 2.0 '
                 '(ebers, sunity_devee, hamerton, fukuzawa, bernal_diaz, babur, seacole, keckley, yung_wing).')
    lines.append('')
    lines.append('**Base Layer Native:** No data. Base Layer IS the authored pipeline; there is no separate '
                 '`baselayer_fullpipeline_*` variant. BL appears only in the controlled column.')
    lines.append('')

    # Controlled table
    lines.append('## Controlled configuration (identical fact pool)')
    lines.append('')
    lines.append('| System | Δ_spec (5-judge) | Subjects + / total | Δ_spec low-baseline (5-judge) | Low-baseline + / total | Wilcoxon W, p (5-judge) |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for system in SYSTEMS:
        info = results['controlled'][system]['primary_5']
        if info is None:
            continue
        agg = f'{info["agg"]:+.3f}' if info['agg'] is not None else 'n/a'
        low_agg = f'{info["low_agg"]:+.3f}' if info['low_agg'] is not None else 'n/a'
        wil = (f'W={info["wil_w"]:.1f}, p={info["wil_p"]:.4f}'
               if info['wil_w'] is not None else 'n/a')
        lines.append(
            f'| {system} | {agg} | {info["positive"]}/{info["n"]} | '
            f'{low_agg} | {info["low_positive"]}/{info["low_n"]} | {wil} |'
        )
    lines.append('')

    # Native table
    lines.append('## Native configuration (each system\'s own ingestion)')
    lines.append('')
    lines.append('| System | Δ_spec (5-judge) | Subjects + / total | Δ_spec low-baseline (5-judge) | Low-baseline + / total | Wilcoxon W, p (5-judge) |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for system in SYSTEMS:
        entry = results['native'][system]
        info = entry.get('primary_5')
        if info is None:
            note = entry.get('note', 'n/a')
            lines.append(f'| {system} | — | — | — | — | _{note}_ |')
            continue
        agg = f'{info["agg"]:+.3f}' if info['agg'] is not None else 'n/a'
        low_agg = f'{info["low_agg"]:+.3f}' if info['low_agg'] is not None else 'n/a'
        wil = (f'W={info["wil_w"]:.1f}, p={info["wil_p"]:.4f}'
               if info['wil_w'] is not None else 'n/a')
        lines.append(
            f'| {system} | {agg} | {info["positive"]}/{info["n"]} | '
            f'{low_agg} | {info["low_positive"]}/{info["low_n"]} | {wil} |'
        )
    lines.append('')

    # 7-judge sensitivity comparison
    lines.append('## 7-judge sensitivity (Gemini-inclusion delta)')
    lines.append('')
    lines.append('Where a subject lacks Gemini Pro data the 7-judge cell falls back to what judges are available (typically 6-judge: primary + Gemini Flash). Same behavior as the gradient recompute.')
    lines.append('')
    lines.append('### Controlled')
    lines.append('')
    lines.append('| System | Δ_spec (5-judge) | Δ_spec (7-judge) | Shift (7j − 5j) |')
    lines.append('|---|---:|---:|---:|')
    for system in SYSTEMS:
        p5 = results['controlled'][system]['primary_5']
        p7 = results['controlled'][system]['seven_judge']
        if p5 is None or p7 is None:
            continue
        d5 = p5['agg']
        d7 = p7['agg']
        if d5 is None or d7 is None:
            continue
        lines.append(f'| {system} | {d5:+.3f} | {d7:+.3f} | {d7 - d5:+.3f} |')
    lines.append('')
    lines.append('### Native')
    lines.append('')
    lines.append('| System | Δ_spec (5-judge) | Δ_spec (7-judge) | Shift (7j − 5j) |')
    lines.append('|---|---:|---:|---:|')
    for system in SYSTEMS:
        entry = results['native'].get(system, {})
        p5 = entry.get('primary_5')
        p7 = entry.get('seven_judge')
        if p5 is None or p7 is None:
            continue
        d5 = p5['agg']
        d7 = p7['agg']
        if d5 is None or d7 is None:
            continue
        lines.append(f'| {system} | {d5:+.3f} | {d7:+.3f} | {d7 - d5:+.3f} |')
    lines.append('')

    # Published comparison (§3 / §4 of DATA_REFERENCE are 7-judge)
    lines.append('## Comparison vs published numbers (7-judge from DATA_REFERENCE §3/§4)')
    lines.append('')
    published = {
        ('controlled', 'mem0'):        {'full': +0.15, 'low': +0.13},
        ('controlled', 'letta'):       {'full': +0.25, 'low': +0.23},
        ('controlled', 'zep'):         {'full': +0.22, 'low': +0.20},
        ('controlled', 'supermemory'): {'full': -0.04, 'low': +0.004},
        ('controlled', 'baselayer'):   {'full': +0.12, 'low': +0.13},
        ('native',     'mem0'):        {'full': +0.38, 'low': +0.38},
        ('native',     'letta'):       {'full': -0.01, 'low': -0.01},
        ('native',     'zep'):         {'full': +0.38, 'low': +0.37},
        ('native',     'supermemory'): {'full': -0.11, 'low': -0.06},
    }
    lines.append('| System | Config | Published 7-judge Δ (full) | Recompute 5-judge Δ (full) | Published 7-judge Δ (low) | Recompute 5-judge Δ (low) |')
    lines.append('|---|---|---:|---:|---:|---:|')
    for config in ['controlled', 'native']:
        for system in SYSTEMS:
            if (config, system) not in published:
                continue
            entry = results[config].get(system, {})
            p5 = entry.get('primary_5') if entry else None
            if p5 is None:
                continue
            pub = published[(config, system)]
            d5 = p5['agg']
            d5_low = p5['low_agg']
            d5_str = f'{d5:+.3f}' if d5 is not None else 'n/a'
            d5_low_str = f'{d5_low:+.3f}' if d5_low is not None else 'n/a'
            lines.append(
                f'| {system} | {config} | {pub["full"]:+.3f} | {d5_str} | '
                f'{pub["low"]:+.3f} | {d5_low_str} |'
            )
    lines.append('')

    # Per-subject detail tables (controlled + native)
    lines.append('## Per-subject detail (5-judge primary)')
    lines.append('')
    for config in ['controlled', 'native']:
        lines.append(f'### {config.capitalize()}')
        lines.append('')
        # Build per-subject row with one column per system
        header = '| Subject | ' + ' | '.join(SYSTEMS) + ' |'
        sep = '|---|' + '|'.join(['---:'] * len(SYSTEMS)) + '|'
        lines.append(header)
        lines.append(sep)
        for subject in MAIN_STUDY:
            row = [subject]
            for system in SYSTEMS:
                entry = results[config].get(system, {})
                p5 = entry.get('primary_5') if entry else None
                if p5 is None:
                    row.append('—')
                    continue
                v = p5['per_subject'].get(subject)
                if v is None:
                    row.append('—')
                else:
                    row.append(f'{v["delta"]:+.3f}')
            lines.append('| ' + ' | '.join(row) + ' |')
        lines.append('')

    # Missing data
    lines.append('## Missing data')
    lines.append('')
    any_missing = False
    for config in ['controlled', 'native']:
        for system in SYSTEMS:
            entry = results[config].get(system, {})
            p5 = entry.get('primary_5') if entry else None
            if p5 is None:
                continue
            if p5['missing']:
                any_missing = True
                lines.append(f'- **{system} ({config}):** missing {len(p5["missing"])} subjects: {", ".join(p5["missing"])}')
    if not any_missing:
        lines.append('_No subjects missing in any cell._')
    lines.append('')

    # Notable outliers
    lines.append('## Notable observations')
    lines.append('')

    # Zep low-baseline
    zep_c = results['controlled'].get('zep', {}).get('primary_5')
    zep_n = results['native'].get('zep', {}).get('primary_5')
    if zep_c and zep_n:
        lines.append(f'- **Zep:** low-baseline positive {zep_c["low_positive"]}/{zep_c["low_n"]} (controlled) '
                     f'and {zep_n["low_positive"]}/{zep_n["low_n"]} (native). Cleanest positive profile.')

    sm_c = results['controlled'].get('supermemory', {}).get('primary_5')
    sm_n = results['native'].get('supermemory', {}).get('primary_5')
    if sm_c and sm_n:
        lines.append(f'- **Supermemory:** controlled aggregate near-zero ({sm_c["agg"]:+.3f}). '
                     f'Native loses {14 - sm_n["n"]} subjects to ingestion failures; effective n={sm_n["n"]}.')

    letta_n = results['native'].get('letta', {}).get('primary_5')
    if letta_n:
        lines.append(f'- **Letta native:** aggregate {letta_n["agg"]:+.3f} — archival-retrieval path. '
                     f'DATA_REFERENCE §7 documents that the stateful-agent path behaves very differently (Hamerton single-subject test).')

    lines.append('- **Base Layer:** Controlled only. Appears as a 5th row for comparability with the other systems under the same fact-pool input; it has no native/fullpipeline variant to compute.')
    lines.append('')

    lines.append('## Data files used')
    lines.append('')
    lines.append('Per subject (hamerton flat, globals under `results/global_<subject>/`):')
    lines.append('- Controlled: `{mem0,letta,zep,supermemory,baselayer}_judgments_{haiku,sonnet,opus,gpt4o,gpt54,gemini_flash}.json`')
    lines.append('- Native:     `{mem0,letta,zep,supermemory}_fullpipeline_judgments_{haiku,sonnet,opus,gpt4o,gpt54,gemini_flash}.json`')
    lines.append('- Optional: `*_judgments_gemini_pro.json` when available.')
    lines.append('')

    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport written: {OUT}')


if __name__ == '__main__':
    main()
