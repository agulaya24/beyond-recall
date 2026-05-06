"""
Wins Inventory: per-question anchor-crossing audit across all condition pairs.

The aggregate Δ values reported in the paper systematically hide multi-anchor
per-question wins (a question jumping from rubric band 1 'refusal' to band 4
'substantive' is interpretively far more significant than a +0.05 mean Δ
suggests). This script builds the per-pair wins inventory across:

  Direct context (judgments_v2.json + results_v2.json):
    1.  C5 -> C2a            (all 14 subjects)
    2.  C5 -> C4             (all 14 subjects)
    3.  C5 -> C4a            (all 14 subjects)
    4.  C5 -> C2c            (all 14 subjects; also includes downward extremes)
    5.  C2a -> C4a           (all 14 subjects)
    6.  C4 -> C4a            (all 14 subjects)

  Corpus (c8_c9_judgments_merged.json + c8_c9_results.json):
    7.  C5 -> C8             (9 low-baseline subjects)
    8.  C5 -> C9             (8 low-baseline subjects; Babur excluded)
    9.  C8 -> C9             (8 low-baseline subjects; Babur excluded)

  Memory systems controlled (<sys>_judgments_merged.json):
    10. C1_mem0        -> C3_mem0        (all 14)
    11. C1_letta       -> C3_letta       (all 14)
    12. C1_supermemory -> C3_supermemory (all 14)
    13. C1_zep         -> C3_zep         (all 14)
    14. C1_baselayer   -> C3_baselayer   (all 14)

  Memory systems native fullpipeline (<sys>_fullpipeline_judgments_merged.json):
    15. C1_mem0_fp        -> C3_mem0_fp        (all 14)
    16. C1_letta_fp       -> C3_letta_fp       (all 14)
    17. C1_supermemory_fp -> C3_supermemory_fp (all 14; some subjects missing)
    18. C1_zep_fp         -> C3_zep_fp         (all 14)

Aggregation: 5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54).
Per-question score = simple mean across the 5 primary judges (require >=3 valid).
Integer band: floor(mean) clipped to [1, 5]; bands [1,2), [2,3), [3,4), [4,5].

Output: docs/research/wins_inventory_20260428.json
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_PATH = REPO / 'docs' / 'research' / 'wins_inventory_20260428.json'

# Make recompute_5judge_primary importable
sys.path.insert(0, str(REPO / 'scripts'))
from recompute_5judge_primary import load_hamerton_judgments  # noqa: E402

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
ALL_SUBJECTS = ['hamerton'] + GLOBAL_SUBJECTS  # 14 total

LOW_BASELINE_FULL = [
    'hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'seacole',
    'bernal_diaz', 'keckley', 'yung_wing', 'babur',
]
LOW_BASELINE_C9 = [s for s in LOW_BASELINE_FULL if s != 'babur']

# Hamerton condition normalization (canonical -> hamerton-internal name).
# Used to translate canonical condition names to the keys actually present
# in hamerton's results.json file.
HAMERTON_CANONICAL_TO_INTERNAL = {
    'C2c_wrong_spec': 'C2c_full_wrong_spec',
    'C4a_full_facts_plus_spec': 'C4a_full_all_facts_plus_spec',
}


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def subject_dir(subject: str) -> Path:
    return RESULTS / 'hamerton' if subject == 'hamerton' else RESULTS / f'global_{subject}'


def safe_load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.load(path.open('r', encoding='utf-8'))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Judgment loaders -- one per file family
# ---------------------------------------------------------------------------

def load_judgments_v2(subject: str):
    """Load main gradient judgments (C5/C2a/C2c/C4/C4a)."""
    if subject == 'hamerton':
        return load_hamerton_judgments()
    return safe_load_json(subject_dir(subject) / 'judgments_v2.json') or []


def load_c8_c9_judgments(subject: str):
    return safe_load_json(subject_dir(subject) / 'c8_c9_judgments_merged.json') or []


def load_system_judgments(subject: str, system: str, fullpipeline: bool):
    suffix = '_fullpipeline' if fullpipeline else ''
    fname = f'{system}{suffix}_judgments_merged.json'
    return safe_load_json(subject_dir(subject) / fname) or []


# ---------------------------------------------------------------------------
# Response loaders -- one per file family, with hamerton special-cases
# ---------------------------------------------------------------------------

def _load_responses_to_index(path: Path):
    """Returns {qid: entry_dict} for a list-of-entries response file."""
    data = safe_load_json(path)
    if not isinstance(data, list):
        return {}
    return {e['question_id']: e for e in data}


_RESPONSE_CACHE: dict[tuple, dict] = {}


def get_response_text(subject: str, qid: int, canonical_condition: str):
    """Return (text, question_text, held_out_passage) for one question/condition.

    Returns (None, None, None) if any piece is unavailable. Handles all the
    hamerton splits and condition-key renaming.
    """
    cache_key = (subject, canonical_condition)
    if cache_key in _RESPONSE_CACHE:
        idx, key_in_file = _RESPONSE_CACHE[cache_key]
    else:
        idx, key_in_file = _resolve_response_file(subject, canonical_condition)
        _RESPONSE_CACHE[cache_key] = (idx, key_in_file)

    if not idx:
        return None, None, None
    entry = idx.get(qid)
    if not entry:
        return None, None, None
    resp_dict = entry.get('responses', {})
    cond_entry = resp_dict.get(key_in_file)
    if cond_entry is None:
        return None, entry.get('question_text'), entry.get('held_out_passage')
    text = cond_entry.get('text') if isinstance(cond_entry, dict) else None
    return text, entry.get('question_text'), entry.get('held_out_passage')


def _resolve_response_file(subject: str, canonical_condition: str):
    """Returns (qid_indexed_dict, key_in_file) for a given (subject, condition).

    The key_in_file is the actual responses[...] dict key used in the file
    (which may differ from the canonical name for hamerton spec conditions).
    """
    sd = subject_dir(subject)

    # Memory-system conditions: <sys>_results.json or <sys>_fullpipeline_results.json
    if canonical_condition.startswith('C1_') or canonical_condition.startswith('C3_'):
        # Strip prefix to find system name.
        rest = canonical_condition.split('_', 1)[1]  # e.g. 'mem0' or 'mem0_fp' or 'letta_fp'
        is_fp = rest.endswith('_fp')
        system = rest[:-3] if is_fp else rest
        suffix = '_fullpipeline' if is_fp else ''
        path = sd / f'{system}{suffix}_results.json'
        return _load_responses_to_index(path), canonical_condition

    if canonical_condition in ('C8_raw_corpus', 'C9_raw_corpus_plus_spec'):
        return _load_responses_to_index(sd / 'c8_c9_results.json'), canonical_condition

    # Gradient conditions: C5/C2a/C2c/C4/C4a
    if subject == 'hamerton':
        # C5/C4 are in results_harmonized.json (canonical keys).
        if canonical_condition in ('C5_baseline', 'C4_factdump'):
            return _load_responses_to_index(sd / 'results_harmonized.json'), canonical_condition
        # C2a/C2c/C4a are in results.json (with potentially renamed keys).
        key_in_file = HAMERTON_CANONICAL_TO_INTERNAL.get(canonical_condition, canonical_condition)
        return _load_responses_to_index(sd / 'results.json'), key_in_file

    # Globals: results_v2.json with canonical keys.
    return _load_responses_to_index(sd / 'results_v2.json'), canonical_condition


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------

def integer_band(mean_score):
    if mean_score is None:
        return None
    if mean_score < 1.0:
        return 0
    if mean_score >= 5.0:
        return 5
    return int(mean_score)


def per_question_means(rows, target_conditions):
    """Build {qid: {cond: mean_score}} requiring >=3 valid primary judges."""
    bucket = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('parse_failure'):
            continue
        if r.get('score') is None:
            continue
        if r.get('condition') not in target_conditions:
            continue
        bucket[r['question_id']][r['condition']].append(r['score'])
    out = {}
    for qid, conds in bucket.items():
        per_q = {}
        for cond, scores in conds.items():
            if len(scores) >= 3:
                per_q[cond] = statistics.mean(scores)
        if per_q:
            out[qid] = per_q
    return out


def truncate(text, n=600):
    if text is None:
        return None
    if len(text) <= n:
        return text
    return text[:n] + '... [truncated]'


def analyze_pair(label, subjects, pre_cond, post_cond, source_loader,
                 collect_downward=False):
    """Compute the wins inventory for one condition pair.

    source_loader: callable(subject) -> list of judgment rows
    collect_downward: if True, also collect top extreme downward jumps
    """
    boundary_counts: dict[str, int] = defaultdict(int)
    multi_anchor_jumps: list[dict] = []  # raw record per >=2-band upward
    extreme_jumps: list[dict] = []  # raw record per >=3-band upward
    extreme_downs: list[dict] = []  # raw record per >=3-band downward
    per_subject_rows = []

    total = up = down = none = 0
    sum_pre = sum_post = 0.0
    delta_count = 0
    missing_subjects = []

    for subj in subjects:
        rows = source_loader(subj)
        if not rows:
            missing_subjects.append(subj)
            continue
        per_q = per_question_means(rows, {pre_cond, post_cond})

        s_total = s_up = s_down = s_none = 0
        s_paired = 0
        for qid, conds in per_q.items():
            if pre_cond not in conds or post_cond not in conds:
                continue
            pre_m = conds[pre_cond]
            post_m = conds[post_cond]
            pre_b = integer_band(pre_m)
            post_b = integer_band(post_m)

            total += 1
            s_total += 1
            s_paired += 1
            sum_pre += pre_m
            sum_post += post_m
            delta_count += 1

            if post_b > pre_b:
                up += 1
                s_up += 1
                jump = post_b - pre_b
                boundary_counts[f'{pre_b}->{post_b}'] += 1
                if jump >= 2:
                    rec = _build_jump_record(subj, qid, pre_b, post_b, pre_m,
                                             post_m, jump, pre_cond, post_cond)
                    multi_anchor_jumps.append(rec)
                    if jump >= 3:
                        extreme_jumps.append(rec)
            elif post_b < pre_b:
                down += 1
                s_down += 1
                drop = pre_b - post_b
                boundary_counts[f'{pre_b}->{post_b} DOWN'] += 1
                if collect_downward and drop >= 3:
                    rec = _build_jump_record(subj, qid, pre_b, post_b, pre_m,
                                             post_m, -drop, pre_cond, post_cond)
                    extreme_downs.append(rec)
            else:
                none += 1
                s_none += 1

        if s_paired > 0:
            per_subject_rows.append({
                'subject': subj,
                'total': s_total,
                'upward': s_up,
                'downward': s_down,
                'no_crossing': s_none,
                'upward_pct': round(100 * s_up / s_total, 1) if s_total else None,
            })
        else:
            missing_subjects.append(subj)

    multi_anchor_count = len(multi_anchor_jumps)
    extreme_count = len(extreme_jumps)

    # Sort jumps for top-N selection.
    # Sort key: (jump desc, pre_mean asc, subject, qid).
    extreme_jumps.sort(key=lambda r: (-r['jump'], r['pre_mean'], r['subject'], r['qid']))
    extreme_downs.sort(key=lambda r: (r['jump'], -r['pre_mean'], r['subject'], r['qid']))
    # ^ for downward, jump is negative. More-negative = bigger drop. Sort ascending = biggest drop first.

    top_extreme = extreme_jumps[:8]
    top_extreme_down = extreme_downs[:8] if collect_downward else []

    n = total or 1  # avoid div-by-zero
    summary = {
        'label': label,
        'pre_condition': pre_cond,
        'post_condition': post_cond,
        'subjects_in_scope': subjects,
        'subjects_with_data': [r['subject'] for r in per_subject_rows],
        'missing_or_empty_subjects': missing_subjects,
        'n_paired_questions': total,
        'upward': up,
        'downward': down,
        'no_crossing': none,
        'upward_pct': round(100 * up / n, 1),
        'downward_pct': round(100 * down / n, 1),
        'no_crossing_pct': round(100 * none / n, 1),
        'net_upward': up - down,
        'net_upward_pct': round(100 * (up - down) / n, 1),
        'multi_anchor_count': multi_anchor_count,
        'multi_anchor_pct': round(100 * multi_anchor_count / n, 1),
        'extreme_count': extreme_count,
        'extreme_pct': round(100 * extreme_count / n, 1),
        'mean_pre': round(sum_pre / delta_count, 3) if delta_count else None,
        'mean_post': round(sum_post / delta_count, 3) if delta_count else None,
        'mean_delta': round((sum_post - sum_pre) / delta_count, 3) if delta_count else None,
        'boundary_breakdown': dict(sorted(boundary_counts.items())),
        'per_subject': per_subject_rows,
        'top_extreme_jumps': top_extreme,
    }

    if collect_downward:
        summary['top_extreme_downward_jumps'] = top_extreme_down

    return summary


def _build_jump_record(subj, qid, pre_b, post_b, pre_m, post_m, jump,
                       pre_cond, post_cond):
    pre_text, q_text_a, hop_a = get_response_text(subj, qid, pre_cond)
    post_text, q_text_b, hop_b = get_response_text(subj, qid, post_cond)
    q_text = q_text_a or q_text_b
    held_out = hop_a or hop_b
    return {
        'subject': subj,
        'qid': qid,
        'question_text': q_text,
        'held_out_passage': held_out,
        'pre_band': pre_b,
        'post_band': post_b,
        'jump': jump,
        'pre_mean': round(pre_m, 3),
        'post_mean': round(post_m, 3),
        'pre_response': truncate(pre_text, 600),
        'post_response': truncate(post_text, 600),
    }


# ---------------------------------------------------------------------------
# Pair definitions
# ---------------------------------------------------------------------------

def build_pair_definitions():
    """Return ordered list of (key, label, subjects, pre_cond, post_cond,
    source_loader, collect_downward)."""
    pairs = []

    # Direct context (judgments_v2.json) -- all 14 subjects
    pairs.append(('C5_to_C2a',
                  'C5 (baseline) -> C2a (full spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C2a_full_spec',
                  load_judgments_v2, False))
    pairs.append(('C5_to_C4',
                  'C5 (baseline) -> C4 (fact dump)',
                  ALL_SUBJECTS, 'C5_baseline', 'C4_factdump',
                  load_judgments_v2, False))
    pairs.append(('C5_to_C4a',
                  'C5 (baseline) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C4a_full_facts_plus_spec',
                  load_judgments_v2, False))
    pairs.append(('C5_to_C2c',
                  'C5 (baseline) -> C2c (wrong spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C2c_wrong_spec',
                  load_judgments_v2, True))  # downward extremes too
    pairs.append(('C2a_to_C4a',
                  'C2a (spec) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C2a_full_spec', 'C4a_full_facts_plus_spec',
                  load_judgments_v2, False))
    pairs.append(('C4_to_C4a',
                  'C4 (factdump) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C4_factdump', 'C4a_full_facts_plus_spec',
                  load_judgments_v2, False))

    # Corpus (c8_c9) -- low-baseline
    pairs.append(('C5_to_C8',
                  'C5 (baseline) -> C8 (raw corpus)',
                  LOW_BASELINE_FULL, 'C5_baseline', 'C8_raw_corpus',
                  _crossfile_C5_to_C8_loader, False))
    pairs.append(('C5_to_C9',
                  'C5 (baseline) -> C9 (corpus + spec)',
                  LOW_BASELINE_C9, 'C5_baseline', 'C9_raw_corpus_plus_spec',
                  _crossfile_C5_to_C9_loader, False))
    pairs.append(('C8_to_C9',
                  'C8 (raw corpus) -> C9 (corpus + spec)',
                  LOW_BASELINE_C9, 'C8_raw_corpus', 'C9_raw_corpus_plus_spec',
                  load_c8_c9_judgments, False))

    # Memory systems controlled
    for sys_name in ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']:
        pairs.append((f'C1_{sys_name}_to_C3_{sys_name}',
                      f'C1_{sys_name} -> C3_{sys_name}',
                      ALL_SUBJECTS, f'C1_{sys_name}', f'C3_{sys_name}',
                      _make_system_loader(sys_name, False), False))

    # Memory systems native fullpipeline
    for sys_name in ['mem0', 'letta', 'supermemory', 'zep']:
        pairs.append((f'C1_{sys_name}_fp_to_C3_{sys_name}_fp',
                      f'C1_{sys_name}_fp -> C3_{sys_name}_fp',
                      ALL_SUBJECTS, f'C1_{sys_name}_fp', f'C3_{sys_name}_fp',
                      _make_system_loader(sys_name, True), False))

    return pairs


def _make_system_loader(system: str, fullpipeline: bool):
    def loader(subject: str):
        return load_system_judgments(subject, system, fullpipeline)
    loader.__name__ = f'load_{system}_{"fp" if fullpipeline else "ctrl"}'
    return loader


def _crossfile_C5_to_C8_loader(subject: str):
    """C5 lives in judgments_v2.json (or hamerton's harmonized loader); C8 lives
    in c8_c9_judgments_merged.json. Pair on qid by concatenating the two row
    sources (the per_question_means filter handles condition selection)."""
    rows = []
    for r in load_judgments_v2(subject):
        if r.get('condition') == 'C5_baseline':
            rows.append(r)
    for r in load_c8_c9_judgments(subject):
        if r.get('condition') == 'C8_raw_corpus':
            rows.append(r)
    return rows


def _crossfile_C5_to_C9_loader(subject: str):
    rows = []
    for r in load_judgments_v2(subject):
        if r.get('condition') == 'C5_baseline':
            rows.append(r)
    for r in load_c8_c9_judgments(subject):
        if r.get('condition') == 'C9_raw_corpus_plus_spec':
            rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------

def cross_check_low_baseline_C5_to_C4a():
    """Reproduce compute_anchor_crossing.py n=351, up=55.0%, down=6.8%,
    multi=18.2%, extreme=5.7%."""
    return analyze_pair('CHECK: C5 -> C4a (low-baseline 9)',
                         LOW_BASELINE_FULL, 'C5_baseline',
                         'C4a_full_facts_plus_spec', load_judgments_v2, False)


def cross_check_low_baseline_C4_to_C4a():
    """Reproduce extended n=351, up=21.9%, down=16.8%, multi=2.6%, extreme=1.1%,
    mean Δ=+0.088."""
    return analyze_pair('CHECK: C4 -> C4a (low-baseline 9)',
                         LOW_BASELINE_FULL, 'C4_factdump',
                         'C4a_full_facts_plus_spec', load_judgments_v2, False)


def cross_check_low_baseline_C8_to_C9():
    """Reproduce extended n=312, up=21.8%, down=18.6%, multi=3.8%, extreme=0.6%,
    mean Δ=+0.088."""
    return analyze_pair('CHECK: C8 -> C9 (low-baseline 8, ex-Babur)',
                         LOW_BASELINE_C9, 'C8_raw_corpus',
                         'C9_raw_corpus_plus_spec', load_c8_c9_judgments, False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('Building wins inventory across 18 pairs...')
    pairs = build_pair_definitions()

    output_pairs = {}
    summary_rows = []
    for key, label, subjects, pre_cond, post_cond, loader, collect_down in pairs:
        print(f'  Analyzing: {label}')
        result = analyze_pair(label, subjects, pre_cond, post_cond, loader,
                              collect_downward=collect_down)
        output_pairs[key] = result
        summary_rows.append((key, result))

    # Cross-checks
    print('\nRunning cross-checks against published anchor-crossing numbers...')
    cc_c4a = cross_check_low_baseline_C5_to_C4a()
    cc_c4_c4a = cross_check_low_baseline_C4_to_C4a()
    cc_c8_c9 = cross_check_low_baseline_C8_to_C9()

    cross_checks = {
        'C5_to_C4a_low_baseline_9': {
            'expected': {'n': 351, 'upward_pct': 55.0, 'downward_pct': 6.8,
                         'multi_anchor_pct': 18.2, 'extreme_pct': 5.7},
            'actual': {'n': cc_c4a['n_paired_questions'],
                       'upward_pct': cc_c4a['upward_pct'],
                       'downward_pct': cc_c4a['downward_pct'],
                       'multi_anchor_pct': cc_c4a['multi_anchor_pct'],
                       'extreme_pct': cc_c4a['extreme_pct']},
        },
        'C4_to_C4a_low_baseline_9': {
            'expected': {'n': 351, 'upward_pct': 21.9, 'downward_pct': 16.8,
                         'multi_anchor_pct': 2.6, 'extreme_pct': 1.1,
                         'mean_delta': 0.088},
            'actual': {'n': cc_c4_c4a['n_paired_questions'],
                       'upward_pct': cc_c4_c4a['upward_pct'],
                       'downward_pct': cc_c4_c4a['downward_pct'],
                       'multi_anchor_pct': cc_c4_c4a['multi_anchor_pct'],
                       'extreme_pct': cc_c4_c4a['extreme_pct'],
                       'mean_delta': cc_c4_c4a['mean_delta']},
        },
        'C8_to_C9_low_baseline_8': {
            'expected': {'n': 312, 'upward_pct': 21.8, 'downward_pct': 18.6,
                         'multi_anchor_pct': 3.8, 'extreme_pct': 0.6,
                         'mean_delta': 0.088},
            'actual': {'n': cc_c8_c9['n_paired_questions'],
                       'upward_pct': cc_c8_c9['upward_pct'],
                       'downward_pct': cc_c8_c9['downward_pct'],
                       'multi_anchor_pct': cc_c8_c9['multi_anchor_pct'],
                       'extreme_pct': cc_c8_c9['extreme_pct'],
                       'mean_delta': cc_c8_c9['mean_delta']},
        },
    }

    out = {
        'date': '2026-04-28',
        'aggregation': '5-judge primary panel; per-question score is simple mean across the 5 primary judges (haiku, sonnet, opus, gpt4o, gpt54). Question included only when both pre and post conditions have >=3 valid (non-null, non-parse-failure) primary-judge scores.',
        'panel_judges': sorted(PRIMARY_JUDGES),
        'integer_band_definition': 'floor(mean) clipped to [1, 5]; bands [1,2), [2,3), [3,4), [4,5]',
        'sort_order_top_extreme_jumps': 'jump desc, pre_mean asc, then subject, qid for stability',
        'cross_checks': cross_checks,
        'pairs': output_pairs,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open('w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f'\nWrote {OUT_PATH}\n')

    # Summary table
    print('=' * 130)
    print(f'{"pair":<32} {"n":>5} {"up%":>6} {"down%":>6} {"none%":>6} {"multi%":>7} {"ext%":>6} {"meanD":>7} {"top_ex":>6}')
    print('-' * 130)
    for key, r in summary_rows:
        n_top = len(r.get('top_extreme_jumps', []))
        md = r.get('mean_delta')
        md_str = f'{md:+.3f}' if md is not None else '  ---'
        print(f'{key:<32} {r["n_paired_questions"]:>5} '
              f'{r["upward_pct"]:>6.1f} {r["downward_pct"]:>6.1f} '
              f'{r["no_crossing_pct"]:>6.1f} {r["multi_anchor_pct"]:>7.1f} '
              f'{r["extreme_pct"]:>6.1f} {md_str:>7} {n_top:>6}')

    print('=' * 130)
    print('\nCross-checks:')
    for cc_key, cc in cross_checks.items():
        exp = cc['expected']
        act = cc['actual']
        ok_n = exp['n'] == act['n']
        ok_up = abs(exp['upward_pct'] - act['upward_pct']) <= 0.2
        ok_md = ('mean_delta' not in exp) or abs(exp['mean_delta'] - act['mean_delta']) <= 0.005
        marker = 'OK' if (ok_n and ok_up and ok_md) else 'CHECK'
        print(f'  [{marker}] {cc_key}')
        print(f'         expected: {exp}')
        print(f'         actual:   {act}')

    # Anomaly report
    print('\nAnomalies / data gaps:')
    any_anomalies = False
    for key, r in summary_rows:
        miss = r.get('missing_or_empty_subjects', [])
        if miss:
            any_anomalies = True
            print(f'  {key}: no/empty paired data for {miss}')
    if not any_anomalies:
        print('  (none)')

    # Headline
    total_extreme_all = sum(r.get('extreme_count', 0) for _, r in summary_rows)
    pair_distribution = sorted(
        [(k, r.get('extreme_count', 0)) for k, r in summary_rows
         if r.get('extreme_count', 0) > 0],
        key=lambda x: -x[1]
    )
    print(f'\nHEADLINE: Across all 18 pairs, {total_extreme_all} paired questions show '
          f'extreme upward jumps (>=3 anchors).')
    print('Distribution by pair (non-zero):')
    for k, c in pair_distribution:
        print(f'   {k}: {c}')


if __name__ == '__main__':
    main()
