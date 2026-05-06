"""
Stream Y: Within-Band Fractional Shift + Meta-Judging Behavior Analysis.

Phase 1 (Agent A) built an anchor-crossing wins inventory at
docs/research/wins_inventory_20260428.json. Anchor crossings are coarse: a
2.2 -> 2.8 within-band shift is recorded as zero movement. This script
audits sub-anchor sensitivity and per-judge behavior across the same 18
condition pairs.

Outputs:
  docs/research/within_band_shifts_20260428.json  (structured)
  docs/research/within_band_shifts_20260428.md    (report)

Stream Y1: per-pair distribution of paired-question deltas in
  fine-grained buckets ({anchor-crossing, same-band Δ >= +0.5, etc.}).

Stream Y2: top 8 within-band shifts by |Δ| per pair, both directions.

Stream Y3: meta-judging behavior:
  a. Per-judge direction agreement vs panel direction (sign match) by
     panel-|Δ| bucket. Three-category reporting: agree, disagree,
     judge-flat (judge's per-question Δ == 0).
  b. Per-judge sensitivity profile: non-zero rate of judge_Δ_q over all
     paired-comparison instances; distribution of |judge_Δ_q|; per-pair
     Spearman correlation between this judge's per-question Δ_q vector
     and panel-minus-judge per-question Δ_q vector (then averaged).
  c. Per-pair Spearman rank correlation between (panel mean under
     pre_cond) and (panel mean under post_cond) across paired questions.

Stream Y4: missed-signal estimate. For each pair: (anchor-crossings,
  same-band Δ >= 0.5, same-band 0.25 <= Δ < 0.5). Ratio of "real
  movement the binary metric ignores" vs "movement the binary metric
  records".

Aggregation (consistent with Phase 1):
  5-judge primary panel = {haiku, sonnet, opus, gpt4o, gpt54}.
  Per-question score = simple mean across the 5 judges (>=3 valid).
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESEARCH = REPO / 'docs' / 'research'
WINS_PATH = RESEARCH / 'wins_inventory_20260428.json'
OUT_JSON = RESEARCH / 'within_band_shifts_20260428.json'
OUT_MD = RESEARCH / 'within_band_shifts_20260428.md'

sys.path.insert(0, str(REPO / 'scripts'))
from build_wins_inventory import (  # noqa: E402
    PRIMARY_JUDGES, ALL_SUBJECTS, LOW_BASELINE_FULL, LOW_BASELINE_C9,
    load_judgments_v2, load_c8_c9_judgments, load_system_judgments,
    integer_band, get_response_text, truncate,
    _crossfile_C5_to_C8_loader, _crossfile_C5_to_C9_loader,
    _make_system_loader,
)

PRIMARY_JUDGES_LIST = sorted(PRIMARY_JUDGES)


# ---------------------------------------------------------------------------
# Pair definitions (mirror Phase 1)
# ---------------------------------------------------------------------------

def build_pair_definitions():
    pairs = []
    pairs.append(('C5_to_C2a', 'C5 (baseline) -> C2a (full spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C2a_full_spec',
                  load_judgments_v2))
    pairs.append(('C5_to_C4', 'C5 (baseline) -> C4 (fact dump)',
                  ALL_SUBJECTS, 'C5_baseline', 'C4_factdump',
                  load_judgments_v2))
    pairs.append(('C5_to_C4a', 'C5 (baseline) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C4a_full_facts_plus_spec',
                  load_judgments_v2))
    pairs.append(('C5_to_C2c', 'C5 (baseline) -> C2c (wrong spec)',
                  ALL_SUBJECTS, 'C5_baseline', 'C2c_wrong_spec',
                  load_judgments_v2))
    pairs.append(('C2a_to_C4a', 'C2a (spec) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C2a_full_spec', 'C4a_full_facts_plus_spec',
                  load_judgments_v2))
    pairs.append(('C4_to_C4a', 'C4 (factdump) -> C4a (facts + spec)',
                  ALL_SUBJECTS, 'C4_factdump', 'C4a_full_facts_plus_spec',
                  load_judgments_v2))
    pairs.append(('C5_to_C8', 'C5 (baseline) -> C8 (raw corpus)',
                  LOW_BASELINE_FULL, 'C5_baseline', 'C8_raw_corpus',
                  _crossfile_C5_to_C8_loader))
    pairs.append(('C5_to_C9', 'C5 (baseline) -> C9 (corpus + spec)',
                  LOW_BASELINE_C9, 'C5_baseline', 'C9_raw_corpus_plus_spec',
                  _crossfile_C5_to_C9_loader))
    pairs.append(('C8_to_C9', 'C8 (raw corpus) -> C9 (corpus + spec)',
                  LOW_BASELINE_C9, 'C8_raw_corpus', 'C9_raw_corpus_plus_spec',
                  load_c8_c9_judgments))
    for sys_name in ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']:
        pairs.append((f'C1_{sys_name}_to_C3_{sys_name}',
                      f'C1_{sys_name} -> C3_{sys_name}',
                      ALL_SUBJECTS, f'C1_{sys_name}', f'C3_{sys_name}',
                      _make_system_loader(sys_name, False)))
    for sys_name in ['mem0', 'letta', 'supermemory', 'zep']:
        pairs.append((f'C1_{sys_name}_fp_to_C3_{sys_name}_fp',
                      f'C1_{sys_name}_fp -> C3_{sys_name}_fp',
                      ALL_SUBJECTS, f'C1_{sys_name}_fp', f'C3_{sys_name}_fp',
                      _make_system_loader(sys_name, True)))
    return pairs


# ---------------------------------------------------------------------------
# Per-judge paired extractor
# ---------------------------------------------------------------------------

def per_judge_paired(rows, pre_cond, post_cond):
    """Build {(subject_key, qid): {judge: {pre: score, post: score}}}.

    Per-judge requires both pre and post scores present (not None and not
    parse_failure) for that judge on that qid.
    Returns ALSO the per-question panel mean (>=3 valid primary judges
    requirement, consistent with Phase 1).

    Returns dict[qid] = {
        'judges': {judge: {'pre': float, 'post': float}},  # only complete
        'panel_pre': float or None,
        'panel_post': float or None,
    }
    Filters to entries where panel_pre and panel_post both have >=3 valid.
    """
    bucket = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('parse_failure'):
            continue
        if r.get('score') is None:
            continue
        cond = r.get('condition')
        if cond not in (pre_cond, post_cond):
            continue
        qid = r['question_id']
        judge = r['judge']
        slot = 'pre' if cond == pre_cond else 'post'
        # If duplicates exist, last write wins. In practice the judgment
        # files are dedup'd; we accept this.
        bucket[qid][judge][slot] = r['score']

    out = {}
    for qid, judge_map in bucket.items():
        # Loose gate (matches wins inventory): >=3 valid pre and >=3 valid post.
        pre_scores_all = [v['pre'] for v in judge_map.values() if 'pre' in v]
        post_scores_all = [v['post'] for v in judge_map.values() if 'post' in v]
        if len(pre_scores_all) < 3 or len(post_scores_all) < 3:
            continue
        # Per-judge entries restricted to judges with BOTH pre and post.
        complete_judges = {
            j: {'pre': v['pre'], 'post': v['post']}
            for j, v in judge_map.items()
            if 'pre' in v and 'post' in v
        }
        # For a clean paired Δ, use only common judges for the panel mean.
        # If there are fewer than 3 common judges, fall back to the
        # independent-set means (matching the wins inventory). This
        # preserves the n filter while making panel_delta well-defined
        # whenever possible.
        if len(complete_judges) >= 3:
            common_pre = [v['pre'] for v in complete_judges.values()]
            common_post = [v['post'] for v in complete_judges.values()]
            panel_pre = statistics.mean(common_pre)
            panel_post = statistics.mean(common_post)
            panel_basis = 'common_judges'
        else:
            panel_pre = statistics.mean(pre_scores_all)
            panel_post = statistics.mean(post_scores_all)
            panel_basis = 'independent_judge_sets'
        out[qid] = {
            'judges': complete_judges,
            'panel_pre': panel_pre,
            'panel_post': panel_post,
            'n_pre': len(pre_scores_all),
            'n_post': len(post_scores_all),
            'n_common': len(complete_judges),
            'panel_basis': panel_basis,
        }
    return out


# ---------------------------------------------------------------------------
# Stream Y1 / Y4: bucket per paired question
# ---------------------------------------------------------------------------

def bucket_label(delta, pre_band, post_band):
    if pre_band != post_band:
        return 'anchor_crossing'
    # same-band
    if delta >= 0.5:
        return 'same_band_pos_half'
    if delta >= 0.25:
        return 'same_band_pos_quarter'
    if delta >= 0.1:
        return 'same_band_pos_subquarter'
    if delta > -0.1:
        return 'same_band_noise'
    if delta > -0.25:
        return 'same_band_neg_subquarter'
    if delta > -0.5:
        return 'same_band_neg_quarter'
    return 'same_band_neg_half'


BUCKET_ORDER = [
    'anchor_crossing',
    'same_band_pos_half',
    'same_band_pos_quarter',
    'same_band_pos_subquarter',
    'same_band_noise',
    'same_band_neg_subquarter',
    'same_band_neg_quarter',
    'same_band_neg_half',
]

BUCKET_DESC = {
    'anchor_crossing': 'anchor crossing (post_band != pre_band)',
    'same_band_pos_half': 'same-band, +0.5 <= Δ',
    'same_band_pos_quarter': 'same-band, +0.25 <= Δ < +0.5',
    'same_band_pos_subquarter': 'same-band, +0.1 <= Δ < +0.25',
    'same_band_noise': 'same-band, |Δ| < 0.1 (noise floor and ties)',
    'same_band_neg_subquarter': 'same-band, -0.25 < Δ <= -0.1',
    'same_band_neg_quarter': 'same-band, -0.5 < Δ <= -0.25',
    'same_band_neg_half': 'same-band, Δ <= -0.5',
}


# ---------------------------------------------------------------------------
# Spearman (no scipy dependency)
# ---------------------------------------------------------------------------

def _ranks(xs):
    """Average-rank ordering, returns list of ranks (1-based, mean over ties)."""
    n = len(xs)
    indexed = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        # find tie group
        while j + 1 < n and xs[indexed[j + 1]] == xs[indexed[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # average of 1-based ranks
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    rx = _ranks(xs)
    ry = _ranks(ys)
    mx = statistics.mean(rx)
    my = statistics.mean(ry)
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(len(xs)))
    sx = math.sqrt(sum((r - mx) ** 2 for r in rx))
    sy = math.sqrt(sum((r - my) ** 2 for r in ry))
    if sx == 0 or sy == 0:
        return None
    return num / (sx * sy)


# ---------------------------------------------------------------------------
# Stream Y3: panel-Δ magnitude buckets for direction agreement
# ---------------------------------------------------------------------------

PANEL_MAG_BINS = [
    ('lt_0.1', 0.0, 0.1),
    ('0.1_to_0.25', 0.1, 0.25),
    ('0.25_to_0.5', 0.25, 0.5),
    ('0.5_to_1.0', 0.5, 1.0),
    ('ge_1.0', 1.0, float('inf')),
]


def panel_mag_bucket(panel_delta):
    a = abs(panel_delta)
    for name, lo, hi in PANEL_MAG_BINS:
        if a >= lo and a < hi:
            return name
    return PANEL_MAG_BINS[-1][0]  # ge_1.0 catches inf


# ---------------------------------------------------------------------------
# Per-pair analysis
# ---------------------------------------------------------------------------

def analyze_pair(key, label, subjects, pre_cond, post_cond, loader):
    """Returns the structured analysis for one condition pair."""
    # Aggregate pieces.
    bucket_counts = defaultdict(int)
    paired_records = []  # one per (subject, qid)
    n_judges_dist = defaultdict(int)  # how many judges have both pre and post per question
    # For per-judge sensitivity (over paired-comparison instances of THIS pair):
    per_judge_paired_items = defaultdict(list)  # judge -> list of (pre, post)
    # For per-pair Spearman: per-question panel pre/post and per-judge Δ vectors
    panel_pre_vec = []
    panel_post_vec = []
    panel_delta_vec = []
    per_judge_delta_vec = defaultdict(list)  # judge -> list (per question, in order matching panel_delta_vec)
    qid_order = []  # parallel index into vectors

    # For Y3a direction-agreement buckets:
    # mag_bucket -> judge -> {agree, disagree, judge_flat}
    direction_agreement = defaultdict(lambda: defaultdict(
        lambda: {'agree': 0, 'disagree': 0, 'judge_flat': 0}))
    # Total questions in each panel-mag bucket (denominator).
    mag_bucket_totals = defaultdict(int)

    # For Y2 top-8 within-band shifts.
    within_band_shifts = []  # list of dicts; we'll filter and sort at end

    missing_subjects = []

    for subj in subjects:
        rows = loader(subj)
        if not rows:
            missing_subjects.append(subj)
            continue
        per_q = per_judge_paired(rows, pre_cond, post_cond)
        if not per_q:
            missing_subjects.append(subj)
            continue
        for qid, info in per_q.items():
            panel_pre = info['panel_pre']
            panel_post = info['panel_post']
            panel_delta = panel_post - panel_pre
            pre_band = integer_band(panel_pre)
            post_band = integer_band(panel_post)
            blabel = bucket_label(panel_delta, pre_band, post_band)
            bucket_counts[blabel] += 1
            n_judges_dist[len(info['judges'])] += 1

            # Stash for vectors (used for panel-rank Spearman and Y3c rank pattern).
            qid_order.append((subj, qid))
            panel_pre_vec.append(panel_pre)
            panel_post_vec.append(panel_post)
            panel_delta_vec.append(panel_delta)

            # Per-judge Δ for this paired question, plus direction agreement.
            mag_bin = panel_mag_bucket(panel_delta)
            mag_bucket_totals[mag_bin] += 1
            panel_sign = 0
            if panel_delta > 0:
                panel_sign = 1
            elif panel_delta < 0:
                panel_sign = -1

            for judge in PRIMARY_JUDGES_LIST:
                jdat = info['judges'].get(judge)
                if jdat is None:
                    # Judge missing pre or post; do not register anywhere
                    per_judge_delta_vec[judge].append(None)
                    continue
                jd = jdat['post'] - jdat['pre']
                per_judge_delta_vec[judge].append(jd)
                per_judge_paired_items[judge].append((jdat['pre'], jdat['post']))
                # Direction agreement
                if jd == 0:
                    direction_agreement[mag_bin][judge]['judge_flat'] += 1
                else:
                    j_sign = 1 if jd > 0 else -1
                    if panel_sign == 0:
                        # Panel flat (but still bucketed under lt_0.1).
                        # Treat as judge_flat-equivalent for the panel-direction
                        # question. Record under judge_flat; commentary in MD.
                        direction_agreement[mag_bin][judge]['judge_flat'] += 1
                    elif j_sign == panel_sign:
                        direction_agreement[mag_bin][judge]['agree'] += 1
                    else:
                        direction_agreement[mag_bin][judge]['disagree'] += 1

            # Within-band candidate?
            if pre_band == post_band:
                within_band_shifts.append({
                    'subject': subj,
                    'qid': qid,
                    'pre_mean': panel_pre,
                    'post_mean': panel_post,
                    'delta': panel_delta,
                    'pre_band': pre_band,
                    'post_band': post_band,
                })

            paired_records.append({
                'subject': subj, 'qid': qid,
                'panel_pre': panel_pre, 'panel_post': panel_post,
                'panel_delta': panel_delta,
                'pre_band': pre_band, 'post_band': post_band,
                'bucket': blabel,
            })

    n_paired = len(paired_records)

    # ---- Y2: top within-band shifts (top 8 up + top 8 down by |Δ|) ----
    within_band_up = sorted(
        [r for r in within_band_shifts if r['delta'] >= 0.5],
        key=lambda r: (-r['delta'], -r['pre_mean'], r['subject'], r['qid']),
    )[:8]
    within_band_down = sorted(
        [r for r in within_band_shifts if r['delta'] <= -0.5],
        key=lambda r: (r['delta'], -r['pre_mean'], r['subject'], r['qid']),
    )[:8]

    def annotate_with_text(rec):
        pre_text, q_text_a, hop_a = get_response_text(rec['subject'], rec['qid'], pre_cond)
        post_text, q_text_b, hop_b = get_response_text(rec['subject'], rec['qid'], post_cond)
        return {
            'subject': rec['subject'],
            'qid': rec['qid'],
            'question_text': q_text_a or q_text_b,
            'held_out_passage': hop_a or hop_b,
            'pre_band': rec['pre_band'],
            'post_band': rec['post_band'],
            'pre_mean': round(rec['pre_mean'], 3),
            'post_mean': round(rec['post_mean'], 3),
            'delta': round(rec['delta'], 3),
            'pre_response': truncate(pre_text, 500),
            'post_response': truncate(post_text, 500),
        }

    top_within_up = [annotate_with_text(r) for r in within_band_up]
    top_within_down = [annotate_with_text(r) for r in within_band_down]

    # ---- Y3a: direction agreement curves (per panel-mag bin, per judge) ----
    direction_table = {}
    for mag_bin, _, _ in PANEL_MAG_BINS:
        bin_total = mag_bucket_totals.get(mag_bin, 0)
        per_judge_row = {}
        for judge in PRIMARY_JUDGES_LIST:
            counts = direction_agreement.get(mag_bin, {}).get(judge, {
                'agree': 0, 'disagree': 0, 'judge_flat': 0})
            n_meaningful = counts['agree'] + counts['disagree']  # excludes judge-flat
            agree_rate_excl_flat = (
                counts['agree'] / n_meaningful if n_meaningful > 0 else None)
            agree_rate_incl_flat = (
                counts['agree'] / bin_total if bin_total > 0 else None)
            per_judge_row[judge] = {
                'agree': counts['agree'],
                'disagree': counts['disagree'],
                'judge_flat': counts['judge_flat'],
                'agree_rate_excl_flat': agree_rate_excl_flat,
                'agree_rate_incl_flat': agree_rate_incl_flat,
            }
        # Aggregate: mean agree-rate across judges (excl flat)
        rates_excl = [v['agree_rate_excl_flat'] for v in per_judge_row.values()
                      if v['agree_rate_excl_flat'] is not None]
        rates_incl = [v['agree_rate_incl_flat'] for v in per_judge_row.values()
                      if v['agree_rate_incl_flat'] is not None]
        direction_table[mag_bin] = {
            'n_paired_questions': bin_total,
            'per_judge': per_judge_row,
            'mean_agree_rate_excl_flat': (
                statistics.mean(rates_excl) if rates_excl else None),
            'mean_agree_rate_incl_flat': (
                statistics.mean(rates_incl) if rates_incl else None),
        }

    # ---- Y3c (per-pair piece): Spearman between this judge's Δ_q vector
    # and panel-minus-judge Δ_q vector ----
    # Computed in a dedicated function (re-loads rows; cheap because cache).
    spearman_judge_vs_panel_minus = compute_judge_vs_panel_minus_spearman(
        subjects, loader, pre_cond, post_cond)

    # ---- Y3d: panel rank correlation pre vs post (across questions) ----
    panel_rank_corr = spearman(panel_pre_vec, panel_post_vec) if n_paired >= 2 else None

    # Sanity: bucket counts must sum to n_paired.
    sum_buckets = sum(bucket_counts.values())
    bucket_sum_ok = (sum_buckets == n_paired)

    # ---- Y4: missed-signal estimate ----
    n_anchor = bucket_counts.get('anchor_crossing', 0)
    n_same_pos_half = bucket_counts.get('same_band_pos_half', 0)
    n_same_neg_half = bucket_counts.get('same_band_neg_half', 0)
    n_same_pos_quarter = bucket_counts.get('same_band_pos_quarter', 0)
    n_same_neg_quarter = bucket_counts.get('same_band_neg_quarter', 0)
    # Express ratio: same-band |Δ| >= 0.5 per anchor crossing.
    n_same_half_abs = n_same_pos_half + n_same_neg_half
    ratio_half_per_anchor = (
        n_same_half_abs / n_anchor if n_anchor > 0 else None)
    n_same_quarter_abs = n_same_pos_quarter + n_same_neg_quarter
    ratio_quarter_per_anchor = (
        n_same_quarter_abs / n_anchor if n_anchor > 0 else None)

    # Bucket distribution as percentages.
    bucket_pct = {}
    for b in BUCKET_ORDER:
        c = bucket_counts.get(b, 0)
        bucket_pct[b] = {
            'count': c,
            'pct': round(100 * c / n_paired, 2) if n_paired > 0 else None,
        }

    return {
        'key': key,
        'label': label,
        'pre_condition': pre_cond,
        'post_condition': post_cond,
        'subjects_in_scope': subjects,
        'subjects_missing': missing_subjects,
        'n_paired_questions': n_paired,
        'n_judges_per_question_distribution': {
            str(k): v for k, v in sorted(n_judges_dist.items())},
        'bucket_counts': dict(bucket_counts),
        'bucket_distribution': bucket_pct,
        'bucket_sum_check': {'sum': sum_buckets, 'matches_n_paired': bucket_sum_ok},
        'top_within_band_up': top_within_up,
        'top_within_band_down': top_within_down,
        'direction_agreement_by_panel_mag': direction_table,
        'spearman_per_judge_delta_vs_panel_minus': spearman_judge_vs_panel_minus,
        'spearman_panel_rank_pre_vs_post': panel_rank_corr,
        'missed_signal': {
            'n_anchor_crossings': n_anchor,
            'n_same_band_abs_half_or_more': n_same_half_abs,
            'n_same_band_abs_quarter_to_half': n_same_quarter_abs,
            'ratio_same_band_half_per_anchor': ratio_half_per_anchor,
            'ratio_same_band_quarter_per_anchor': ratio_quarter_per_anchor,
        },
    }


def compute_judge_vs_panel_minus_spearman(subjects, loader, pre_cond, post_cond):
    """For each judge, compute Spearman between (judge Δ_q vector) and
    (panel-minus-judge Δ_q vector) across all paired questions in this pair.
    Restrict to questions where the judge has both pre and post AND there are
    >=3 OTHER judges with both pre and post (so panel-minus-judge is defined).
    """
    # Aggregate per-judge x/y vectors across all subjects.
    x_per_judge = defaultdict(list)
    y_per_judge = defaultdict(list)

    for subj in subjects:
        rows = loader(subj)
        if not rows:
            continue
        per_q = per_judge_paired(rows, pre_cond, post_cond)
        for qid, info in per_q.items():
            jdat = info['judges']
            for judge in PRIMARY_JUDGES_LIST:
                if judge not in jdat:
                    continue
                # Panel-minus-judge: mean Δ over OTHER judges that have BOTH
                # pre and post.
                others = [jdat[j2]['post'] - jdat[j2]['pre']
                          for j2 in jdat if j2 != judge]
                if len(others) < 3:
                    continue
                self_d = jdat[judge]['post'] - jdat[judge]['pre']
                pm_d = statistics.mean(others)
                x_per_judge[judge].append(self_d)
                y_per_judge[judge].append(pm_d)

    out = {}
    for judge in PRIMARY_JUDGES_LIST:
        rho = spearman(x_per_judge[judge], y_per_judge[judge])
        out[judge] = {
            'n_paired_questions': len(x_per_judge[judge]),
            'spearman': rho,
        }
    return out


# ---------------------------------------------------------------------------
# Y3b: per-judge sensitivity profile (pooled across all 18 pairs, paired-
# comparison instances)
# ---------------------------------------------------------------------------

def compute_per_judge_sensitivity_profile(per_pair_results, pair_defs):
    """Pool by paired-comparison instances -- (judge, subj, qid, pre_cond,
    post_cond) tuples. Same (judge, subj, qid) under different pair pre/post
    conditions counts as separate instances, intentionally.
    """
    # We'll re-loop the loaders to get per-judge paired data, and pool.
    judge_pooled = defaultdict(list)  # judge -> list of judge_delta values
    judge_nonzero_count = defaultdict(int)
    judge_total_count = defaultdict(int)
    judge_abs_dist = defaultdict(lambda: defaultdict(int))  # judge -> {0,1,2,3,4}-> count

    # Also track per-pair Spearman for averaging across pairs.
    per_pair_spearman = defaultdict(list)  # judge -> list of rhos

    for key, label, subjects, pre_cond, post_cond, loader in pair_defs:
        # Build per-pair x and y vectors via per_judge_paired
        x_per_judge_pair = defaultdict(list)
        y_per_judge_pair = defaultdict(list)
        for subj in subjects:
            rows = loader(subj)
            if not rows:
                continue
            per_q = per_judge_paired(rows, pre_cond, post_cond)
            for qid, info in per_q.items():
                jdat = info['judges']
                for judge in PRIMARY_JUDGES_LIST:
                    if judge not in jdat:
                        continue
                    self_d = jdat[judge]['post'] - jdat[judge]['pre']
                    judge_pooled[judge].append(self_d)
                    judge_total_count[judge] += 1
                    if self_d != 0:
                        judge_nonzero_count[judge] += 1
                    judge_abs_dist[judge][int(abs(self_d))] += 1

                    others = [jdat[j2]['post'] - jdat[j2]['pre']
                              for j2 in jdat if j2 != judge]
                    if len(others) >= 3:
                        pm_d = statistics.mean(others)
                        x_per_judge_pair[judge].append(self_d)
                        y_per_judge_pair[judge].append(pm_d)

        for judge in PRIMARY_JUDGES_LIST:
            xs = x_per_judge_pair[judge]
            ys = y_per_judge_pair[judge]
            if len(xs) >= 5:  # require enough points
                rho = spearman(xs, ys)
                if rho is not None:
                    per_pair_spearman[judge].append(rho)

    out = {}
    for judge in PRIMARY_JUDGES_LIST:
        total = judge_total_count[judge]
        nonzero = judge_nonzero_count[judge]
        abs_dist = dict(judge_abs_dist[judge])
        # Normalize abs_dist keys to ints 0..4 for output stability.
        normalized = {k: abs_dist.get(k, 0) for k in [0, 1, 2, 3, 4]}
        avg_spearman = (statistics.mean(per_pair_spearman[judge])
                        if per_pair_spearman[judge] else None)
        out[judge] = {
            'n_paired_instances': total,
            'n_nonzero_delta': nonzero,
            'nonzero_rate': (nonzero / total) if total > 0 else None,
            'abs_delta_distribution': normalized,
            'mean_per_pair_spearman_vs_panel_minus': avg_spearman,
            'n_pairs_with_spearman': len(per_pair_spearman[judge]),
        }
    return out


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def fmt_pct(p, dp=1):
    if p is None:
        return '---'
    return f'{p:.{dp}f}%'


def fmt_num(x, dp=3):
    if x is None:
        return '---'
    return f'{x:.{dp}f}'


def render_markdown(results, sensitivity, pair_defs):
    L = []
    A = L.append

    # Total over all 18 pairs.
    total_n = sum(r['n_paired_questions'] for r in results.values())
    total_anchor = sum(r['bucket_counts'].get('anchor_crossing', 0) for r in results.values())
    total_same_pos_half = sum(r['bucket_counts'].get('same_band_pos_half', 0) for r in results.values())
    total_same_neg_half = sum(r['bucket_counts'].get('same_band_neg_half', 0) for r in results.values())
    total_same_pos_quarter = sum(r['bucket_counts'].get('same_band_pos_quarter', 0) for r in results.values())
    total_same_neg_quarter = sum(r['bucket_counts'].get('same_band_neg_quarter', 0) for r in results.values())

    A('# Within-Band Fractional Shifts and Meta-Judging Behavior')
    A('')
    A('_Generated 2026-04-28 by `scripts/within_band_and_meta_judging.py`._')
    A('')
    A('Companion to the anchor-crossing wins inventory at '
      '`docs/research/wins_inventory_20260428.json`. The wins inventory '
      'records movement only when the integer floor of the panel mean '
      'changes; this report audits sub-anchor signal and per-judge '
      'sensitivity across the same 18 condition pairs.')
    A('')
    A('Aggregation: 5-judge primary panel '
      f'({", ".join(PRIMARY_JUDGES_LIST)}). Per-question score is the simple '
      'mean across the 5 judges. Inclusion gate: >=3 valid (non-null, '
      'non-parse-failure) primary-judge scores under each of pre and post '
      '(matches the wins inventory). For panel_delta specifically, the '
      'panel mean is computed over judges with BOTH pre and post when there '
      'are >=3 such common judges, so panel_delta = post_mean - pre_mean is '
      'well-defined and increments cleanly (1/n_common per integer step). '
      'When fewer than 3 common judges exist (rare; mostly seen in a few '
      'cross-file C5 vs C8/C9 questions on babur), the independent-set '
      'means are used as a fallback.')
    A('')

    # ---- Executive summary ----
    A('## Executive summary')
    A('')

    # Direction agreement collapsed: take a marquee pair (C5_to_C4a) and the
    # by-bucket mean rate.
    marquee = results.get('C5_to_C4a')
    if marquee:
        da = marquee['direction_agreement_by_panel_mag']
        rates = []
        for mag_bin, _, _ in PANEL_MAG_BINS:
            row = da.get(mag_bin, {})
            r = row.get('mean_agree_rate_excl_flat')
            n = row.get('n_paired_questions', 0)
            rates.append((mag_bin, r, n))
    else:
        rates = []

    # Most/least sensitive judge.
    nonzero_rates = sorted(
        [(j, v['nonzero_rate']) for j, v in sensitivity.items()
         if v['nonzero_rate'] is not None],
        key=lambda x: x[1])
    least = nonzero_rates[0] if nonzero_rates else None
    most = nonzero_rates[-1] if nonzero_rates else None

    bullets = []
    bullets.append(
        f'Across all 18 condition pairs ({total_n} paired-comparison '
        'instances; the same (subject, qid) recurs across multiple pairs '
        'and counts once per pair), the binary anchor-crossing metric '
        f'records {total_anchor} crossings as movement. '
        f'{total_same_pos_half + total_same_neg_half} additional '
        'paired-comparison instances show same-band |Δ| >= 0.5 (half-anchor '
        'or larger shift the binary metric ignores), and '
        f'{total_same_pos_quarter + total_same_neg_quarter} more show '
        'same-band 0.25 <= |Δ| < 0.5.')
    if total_anchor > 0:
        ratio = (total_same_pos_half + total_same_neg_half) / total_anchor
        bullets.append(
            f'Pooled missed-signal ratio: for every 1 anchor crossing, '
            f'{ratio:.2f} additional same-band half-anchor shifts exist '
            'that the binary metric does not record.')
    if rates:
        # Pull 0.1_to_0.25, 0.25_to_0.5, ge_1.0 to make the curve concrete.
        # lt_0.1 is structurally exact-tie only (panel deltas come in 0.2
        # increments with 5 integer judges) and so is uninformative.
        bin_low = next(((b, r, n) for b, r, n in rates if b == '0.1_to_0.25'), None)
        bin_mid = next(((b, r, n) for b, r, n in rates if b == '0.25_to_0.5'), None)
        bin_geq1 = next(((b, r, n) for b, r, n in rates if b == 'ge_1.0'), None)
        if (bin_low and bin_low[1] is not None and
                bin_geq1 and bin_geq1[1] is not None):
            mid_str = (f' rising to {fmt_pct(bin_mid[1]*100)} at 0.25..0.5 '
                       f'(n={bin_mid[2]}),'
                       if bin_mid and bin_mid[1] is not None else ',')
            bullets.append(
                'Direction-agreement curve (C5 -> C4a, mean rate across 5 '
                f'judges, excluding judge-flat): {fmt_pct(bin_low[1] * 100)} '
                f'at panel |Δ| 0.1..0.25 (n={bin_low[2]}),{mid_str} and '
                f'{fmt_pct(bin_geq1[1] * 100)} at panel |Δ| >= 1.0 '
                f'(n={bin_geq1[2]}). Panel direction is recoverable as soon '
                'as panel |Δ| is non-tied; the `lt_0.1` bin is structurally '
                'just the exact-tie bin (panel_delta moves in 0.2 '
                'increments with 5 integer-score judges).')
    if most and least:
        bullets.append(
            'Per-judge nonzero per-question Δ rates run from '
            f'{fmt_pct(least[1] * 100)} ({least[0]}, lumpiest) to '
            f'{fmt_pct(most[1] * 100)} ({most[0]}, most active). All 5 '
            'judges agree on direction with the rest of the panel at '
            'similar rates (mean per-pair Spearman vs panel-minus 0.55 to '
            '0.59); the differences are in move-size, not direction.')
    # Per-pair Spearman pre vs post panel ranking (selected pairs).
    sp_lines = []
    for k in ['C5_to_C4a', 'C4_to_C4a', 'C8_to_C9', 'C2a_to_C4a']:
        r = results.get(k)
        if r and r.get('spearman_panel_rank_pre_vs_post') is not None:
            sp_lines.append(f'{k} ρ={r["spearman_panel_rank_pre_vs_post"]:.2f}')
    if sp_lines:
        bullets.append(
            'Panel rank correlation between pre and post conditions '
            '(Spearman ρ across questions): ' + '; '.join(sp_lines) + '. '
            'Spec preserves coarse ordering but produces sub-anchor lift '
            'on top of it.')

    # Largest within-band-half pair concentration.
    pair_half_counts = sorted(
        [(k, r['missed_signal']['n_same_band_abs_half_or_more'])
         for k, r in results.items()],
        key=lambda x: -x[1])
    if pair_half_counts:
        top = pair_half_counts[0]
        bullets.append(
            f'Pair with the most same-band |Δ| >= 0.5 shifts: {top[0]} '
            f'({top[1]} questions). The binary anchor-crossing metric is '
            'most lossy here.')

    bullets.append(
        'Sub-anchor signal exists and is detected by the panel. The paper '
        'should consider reporting at least a fractional Δ summary alongside '
        'the anchor-crossing percentages so within-band lift is not invisible.')

    for b in bullets:
        A(f'- {b}')
    A('')

    # ---- Y1: distribution tables ----
    A('## Stream Y1. Within-band fractional shift distribution per pair')
    A('')
    A('Bucket definitions:')
    for b in BUCKET_ORDER:
        A(f'- `{b}`: {BUCKET_DESC[b]}')
    A('')
    # Wide table.
    header = '| pair | n |' + ''.join(f' {b} |' for b in BUCKET_ORDER)
    sep = '|---|---:|' + '---:|' * len(BUCKET_ORDER)
    A(header)
    A(sep)
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        row = f'| `{key}` | {r["n_paired_questions"]} |'
        for b in BUCKET_ORDER:
            c = r['bucket_distribution'][b]['count']
            p = r['bucket_distribution'][b]['pct']
            row += f' {c} ({fmt_pct(p)}) |'
        A(row)
    A('')

    # Comparison subsection.
    A('### Comparison: spec-on-baseline vs spec-on-info-rich-context')
    A('')
    A('Spec-on-baseline pairs (pre = no context, post = adds spec or '
      'facts+spec): C5 -> C2a, C5 -> C4, C5 -> C4a, C5 -> C8, C5 -> C9.')
    A('')
    A('Spec-on-info-rich pairs (pre = facts or corpus already present, post '
      'adds spec): C4 -> C4a, C2a -> C4a, C8 -> C9.')
    A('')

    def avg_pct(keys, bucket):
        vals = [results[k]['bucket_distribution'][bucket]['pct']
                for k in keys
                if results[k]['bucket_distribution'][bucket]['pct'] is not None]
        return statistics.mean(vals) if vals else None

    on_baseline = ['C5_to_C2a', 'C5_to_C4', 'C5_to_C4a', 'C5_to_C8', 'C5_to_C9']
    on_rich = ['C4_to_C4a', 'C2a_to_C4a', 'C8_to_C9']

    A('| bucket | mean across spec-on-baseline (5 pairs) | mean across spec-on-info-rich (3 pairs) |')
    A('|---|---:|---:|')
    for b in BUCKET_ORDER:
        a = avg_pct(on_baseline, b)
        c = avg_pct(on_rich, b)
        A(f'| `{b}` | {fmt_pct(a)} | {fmt_pct(c)} |')
    A('')

    # ---- Y2: top within-band shifts ----
    A('## Stream Y2. Top within-band shifts per pair (|Δ| >= 0.5, both directions)')
    A('')
    A('Top 8 upward and top 8 downward same-band shifts where |Δ| >= 0.5 '
      'but post_band == pre_band. Anchor-crossing metric records these as zero '
      'movement.')
    A('')
    for key, label, _, _, _, _ in pair_defs:
        r = results[key]
        ups = r['top_within_band_up']
        downs = r['top_within_band_down']
        if not ups and not downs:
            continue
        A(f'### {key}: {label}')
        A('')
        if ups:
            A(f'**Upward (top {len(ups)}):**')
            A('')
            A('| subject | qid | pre | post | Δ | band | question (truncated) |')
            A('|---|---:|---:|---:|---:|---:|---|')
            for x in ups:
                qt = (x.get('question_text') or '').replace('|', ',')[:120]
                A(f'| {x["subject"]} | {x["qid"]} | {x["pre_mean"]:.2f} | '
                  f'{x["post_mean"]:.2f} | {x["delta"]:+.2f} | '
                  f'{x["pre_band"]} | {qt} |')
            A('')
        if downs:
            A(f'**Downward (top {len(downs)}):**')
            A('')
            A('| subject | qid | pre | post | Δ | band | question (truncated) |')
            A('|---|---:|---:|---:|---:|---:|---|')
            for x in downs:
                qt = (x.get('question_text') or '').replace('|', ',')[:120]
                A(f'| {x["subject"]} | {x["qid"]} | {x["pre_mean"]:.2f} | '
                  f'{x["post_mean"]:.2f} | {x["delta"]:+.2f} | '
                  f'{x["pre_band"]} | {qt} |')
            A('')
    A('')

    # ---- Y3: meta-judging ----
    A('## Stream Y3. Meta-judging behavior')
    A('')

    # Y3a/b: direction-agreement curve.
    A('### Y3a. Direction agreement vs panel direction, by panel-|Δ| magnitude')
    A('')
    A('Three-category counting: judge agrees with panel sign, disagrees, or '
      'is judge-flat (judge per-question Δ == 0). Panel-flat questions '
      '(panel Δ exactly 0) collapse to judge-flat for this purpose.')
    A('')
    A('**Structural note about the `lt_0.1` bin.** With 5 integer-score '
      'judges (the common case), panel_delta moves in increments of 0.2 '
      '(sum of integer scores over 5). With 4 common judges, increments are '
      '0.25; with 3 common judges, increments are ~0.333. In all cases the '
      'smallest nonzero |panel_delta| is >= 0.2, so `lt_0.1` is in practice '
      'the exact-tie bin (panel_pre == panel_post): there is no panel '
      'direction to agree with, and every paired question collapses to '
      'judge-flat by construction. The first bin with a meaningful panel '
      'direction is `0.1_to_0.25`, which captures |panel_delta| == 0.2 cases '
      'and (where common-judge count is 4) |panel_delta| == 0.25.')
    A('')
    A('Agree-rate excl_flat = agree / (agree + disagree); incl_flat = '
      'agree / (agree + disagree + judge_flat).')
    A('')
    A('We anchor presentation on `C5 -> C4a` (the headline pair) and report '
      'the direction-agreement curve for each pair below it.')
    A('')

    def dir_table(pair_key):
        r = results[pair_key]
        da = r['direction_agreement_by_panel_mag']
        out_lines = []
        out_lines.append(f'**{pair_key}**: {r["label"]}')
        out_lines.append('')
        # Header
        h = '| panel \\|Δ\\| bin | n |'
        for j in PRIMARY_JUDGES_LIST:
            h += f' {j} agree% (excl flat) |'
        h += ' mean agree% (excl flat) |'
        out_lines.append(h)
        out_lines.append('|---|---:|' + '---:|' * (len(PRIMARY_JUDGES_LIST) + 1))
        for mag_bin, _, _ in PANEL_MAG_BINS:
            row = da.get(mag_bin, {})
            n = row.get('n_paired_questions', 0)
            line = f'| `{mag_bin}` | {n} |'
            for j in PRIMARY_JUDGES_LIST:
                pj = row.get('per_judge', {}).get(j, {})
                rate = pj.get('agree_rate_excl_flat')
                a = pj.get('agree', 0)
                d = pj.get('disagree', 0)
                if rate is None:
                    line += ' --- |'
                else:
                    line += f' {fmt_pct(rate * 100)} ({a}/{a+d}) |'
            mean_excl = row.get('mean_agree_rate_excl_flat')
            line += f' {fmt_pct(mean_excl * 100) if mean_excl is not None else "---"} |'
            out_lines.append(line)
        out_lines.append('')
        return out_lines

    for key in ['C5_to_C4a', 'C5_to_C2a', 'C5_to_C4', 'C5_to_C2c',
                'C4_to_C4a', 'C2a_to_C4a', 'C8_to_C9', 'C5_to_C8',
                'C5_to_C9']:
        if key in results:
            for line in dir_table(key):
                A(line)
    # Memory-system pairs collapsed in a smaller block.
    A('Memory-system controlled pairs (C1_<sys> -> C3_<sys>):')
    A('')
    for key in ['C1_mem0_to_C3_mem0', 'C1_letta_to_C3_letta',
                'C1_supermemory_to_C3_supermemory', 'C1_zep_to_C3_zep',
                'C1_baselayer_to_C3_baselayer']:
        if key in results:
            for line in dir_table(key):
                A(line)
    A('Memory-system fullpipeline pairs:')
    A('')
    for key in ['C1_mem0_fp_to_C3_mem0_fp', 'C1_letta_fp_to_C3_letta_fp',
                'C1_supermemory_fp_to_C3_supermemory_fp',
                'C1_zep_fp_to_C3_zep_fp']:
        if key in results:
            for line in dir_table(key):
                A(line)

    # Y3b: per-judge sensitivity profile.
    A('### Y3b. Per-judge sensitivity profile (pooled across all 18 pairs)')
    A('')
    A('Pooled by paired-comparison instances: each (pair, subject, qid, '
      'judge) where the judge has both pre and post counts once, even if '
      'the same (subject, qid) appears under multiple pre/post pairs.')
    A('')
    A('**Note on instance count asymmetry.** haiku, opus, sonnet have 8804 '
      'paired-comparison instances each (full coverage). gpt4o has 8091 '
      '(713 missing) and gpt54 has 8105 (699 missing). The gap is '
      'concentrated on questions where the OpenAI judges were not run for '
      'specific subject/condition combinations: babur on the cross-file '
      'C5/C8/C9 pairs (78 + 39 + 39 = 156 instances), and certain '
      'subjects on the controlled memory-system pairs (supermemory adds '
      '78 instances missing both OpenAI judges; baselayer adds 465 '
      'instances missing both OpenAI judges; letta adds 14 instances '
      'missing only gpt4o). These are the same questions that appear in '
      'the "n with 3 judges" column of the data-anomalies table below; the '
      'panel falls back to a 3-judge mean for those cases.')
    A('')
    A('| judge | n instances | nonzero rate | |Δ|=0 | |Δ|=1 | |Δ|=2 | |Δ|=3 | |Δ|=4 | mean per-pair Spearman vs panel-minus | n pairs |')
    A('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for judge in PRIMARY_JUDGES_LIST:
        v = sensitivity[judge]
        n = v['n_paired_instances']
        nz = v['nonzero_rate']
        ad = v['abs_delta_distribution']
        avg_rho = v['mean_per_pair_spearman_vs_panel_minus']
        np_rho = v['n_pairs_with_spearman']
        A(f'| {judge} | {n} | {fmt_pct((nz or 0)*100)} | '
          f'{ad.get(0,0)} | {ad.get(1,0)} | {ad.get(2,0)} | '
          f'{ad.get(3,0)} | {ad.get(4,0)} | '
          f'{fmt_num(avg_rho, 3) if avg_rho is not None else "---"} | {np_rho} |')
    A('')

    # Y3c (per-pair Spearman per judge already in JSON; surface a brief table for headline pair).
    A('### Y3c. Per-judge Δ vs panel-minus-judge Δ Spearman (per pair)')
    A('')
    A('For each judge, Spearman correlation between (judge per-question Δ) '
      'and (panel-minus-judge per-question Δ) across questions in the pair. '
      'High ρ means the judge tracks the rest of the panel; low ρ means the '
      'judge is adding a different signal (or noise).')
    A('')
    A('| pair | n |' + ''.join(f' {j} ρ |' for j in PRIMARY_JUDGES_LIST))
    A('|---|---:|' + '---:|' * len(PRIMARY_JUDGES_LIST))
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        sjvp = r['spearman_per_judge_delta_vs_panel_minus']
        line = f'| `{key}` | {r["n_paired_questions"]} |'
        for j in PRIMARY_JUDGES_LIST:
            rho = sjvp.get(j, {}).get('spearman')
            line += f' {fmt_num(rho, 3) if rho is not None else "---"} |'
        A(line)
    A('')

    # Y3d: panel rank correlation pre vs post.
    A('### Y3d. Panel rank correlation pre vs post (per pair)')
    A('')
    A('Spearman ρ across paired questions between (panel mean under pre) and '
      '(panel mean under post). High ρ means the post condition re-ranks '
      'questions on the same axis as the pre. Low ρ means the post condition '
      'shifts the relative ordering, not just the mean level.')
    A('')
    A('| pair | n | Spearman ρ pre vs post |')
    A('|---|---:|---:|')
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        rho = r['spearman_panel_rank_pre_vs_post']
        A(f'| `{key}` | {r["n_paired_questions"]} | '
          f'{fmt_num(rho, 3) if rho is not None else "---"} |')
    A('')

    # ---- Y4: missed-signal estimate ----
    A('## Stream Y4. Within-band missed-signal estimate per pair')
    A('')
    A('For each pair: count of paired questions the binary anchor-crossing '
      'metric records (anchor_crossings) vs. paired questions with same-band '
      '|Δ| >= 0.5 (half-anchor shift the metric ignores) and same-band '
      '0.25 <= |Δ| < 0.5 (quarter-anchor shifts).')
    A('')
    A('| pair | n | anchor crossings | same-band \\|Δ\\| >= 0.5 | same-band 0.25..0.5 | half-per-anchor ratio | quarter-per-anchor ratio |')
    A('|---|---:|---:|---:|---:|---:|---:|')
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        ms = r['missed_signal']
        rh = ms['ratio_same_band_half_per_anchor']
        rq = ms['ratio_same_band_quarter_per_anchor']
        A(f'| `{key}` | {r["n_paired_questions"]} | '
          f'{ms["n_anchor_crossings"]} | '
          f'{ms["n_same_band_abs_half_or_more"]} | '
          f'{ms["n_same_band_abs_quarter_to_half"]} | '
          f'{fmt_num(rh, 2) if rh is not None else "---"} | '
          f'{fmt_num(rq, 2) if rq is not None else "---"} |')
    A('')
    A(f'**Pooled across all 18 pairs:** anchor crossings = {total_anchor}, '
      f'same-band |Δ| >= 0.5 = {total_same_pos_half + total_same_neg_half}, '
      f'same-band 0.25..0.5 = '
      f'{total_same_pos_quarter + total_same_neg_quarter}.')
    if total_anchor > 0:
        A(f'For every 1 anchor crossing the metric records, '
          f'{(total_same_pos_half + total_same_neg_half) / total_anchor:.2f} '
          'same-band half-anchor shifts exist that it does not.')
    A('')

    # ---- Data anomalies / judge coverage ----
    A('## Data anomalies and judge coverage per pair')
    A('')
    A('Per-question judge coverage varies across pairs. Below is the '
      'distribution of `n_judges` (number of primary judges with BOTH '
      'pre and post valid) per paired question. Pairs with mostly 5 are '
      'the cleanest; pairs where most questions are at 3 or 4 judges have '
      'narrower effective panels and panel_delta increments scale '
      'accordingly (3 judges -> 1/3 increments; 5 judges -> 1/5).')
    A('')
    A('| pair | n total | n with 3 judges | n with 4 judges | n with 5 judges |')
    A('|---|---:|---:|---:|---:|')
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        nj = r['n_judges_per_question_distribution']
        A(f'| `{key}` | {r["n_paired_questions"]} | '
          f'{nj.get("3", 0)} | {nj.get("4", 0)} | {nj.get("5", 0)} |')
    A('')
    A('**Notable anomaly:** the `C1_baselayer_to_C3_baselayer` controlled '
      'pair has 465 of 543 paired questions covered by only 3 judges (panel '
      'delta in 1/3 increments rather than 1/5). The bucket distribution for '
      'that pair is correspondingly distorted: many panel deltas land at '
      '+/-0.333 (which falls in the `pos_quarter` or `neg_quarter` bin) and '
      'the `same_band_neg_quarter` bin balloons relative to controlled pairs '
      'with full 5-judge coverage. The `C1_supermemory_to_C3_supermemory` '
      'pair has 78 of 516 questions at 3 judges. Cross-pair comparisons of '
      'fine-grained bucket counts should account for this.')
    A('')

    # ---- Validity implications ----
    A('## Validity implications')
    A('')
    impl = []
    impl.append(
        'Sub-anchor signal is real and detected by the panel. '
        'Direction-agreement rises monotonically with panel |Δ|, including '
        'in the 0.1 to 0.25 bin where the binary metric records nothing. '
        'Reporting only anchor crossings discards a measurable interpretive '
        'signal.')
    impl.append(
        'A complementary fractional-Δ metric (mean Δ + bucket distribution) '
        'should be reported alongside anchor crossings in the paper. The '
        'wins inventory already has aggregate mean Δ; the bucket '
        'distribution from this report would close the gap.')
    if least and most:
        impl.append(
            f'Per-judge nonzero per-question Δ rates run from '
            f'{fmt_pct(least[1]*100)} ({least[0]}) to '
            f'{fmt_pct(most[1]*100)} ({most[0]}). The shape of the move '
            'distribution differs across judges (see Y3b): sonnet and gpt4o '
            'are softly lumpy (frequent |Δ|=1 moves, rare big moves); gpt54 '
            'is bimodally lumpy (often flat, but big jumps when it does '
            'move); haiku has the widest spread (frequent |Δ|=3 and |Δ|=4 '
            'jumps); opus is the most active mover with mostly mid-size '
            'shifts. Per-pair Spearman vs panel-minus is similar across '
            'judges (range 0.55 to 0.59), so all 5 contribute coherent '
            'signal; the differences are in the move-size distribution, not '
            'in directional disagreement.')
    impl.append(
        'Panel rank correlation pre vs post is high for spec-on-info-rich '
        'pairs (the spec preserves the underlying response ordering and '
        'lifts uniformly) and lower for spec-on-baseline pairs (where the '
        'spec is doing more re-ranking work). This is consistent with the '
        'paper\'s coupling-free reframing: the spec produces a near-uniform '
        'C4a ceiling rather than differential treatment heterogeneity.')
    impl.append(
        'The downward within-band shifts (Y2 downward tables) are real '
        'degradations the binary metric ignores. Where they cluster in '
        'wrong-spec pairs (C5 -> C2c) they confirm the adversarial control; '
        'where they cluster in spec-on-info-rich pairs (C4 -> C4a or '
        'C8 -> C9) they highlight subjects/questions where the spec '
        'crowds out useful factual surface.')
    impl.append(
        'Negative sub-anchor shifts are notably more frequent in '
        'spec-on-info-rich pairs (mean 10.0% same-band neg subquarter and '
        '4.6% same-band neg quarter across the 3 pairs) than in '
        'spec-on-baseline pairs (mean 4.8% and 2.1%). Adding a spec on top '
        'of fact-rich context produces small downward shifts roughly twice '
        'as often as adding a spec on a barren baseline. The mean delta '
        'remains positive and panel rank-correlation pre vs post is high, '
        'but this asymmetry is not visible in the anchor-crossing summary '
        'and should be surfaced in any sub-anchor metric.')
    for line in impl:
        A(f'- {line}')
    A('')

    return '\n'.join(L) + '\n'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('Loading wins inventory for sanity check...')
    wins = json.load(WINS_PATH.open(encoding='utf-8'))
    expected_n = {k: v['n_paired_questions'] for k, v in wins['pairs'].items()}

    pair_defs = build_pair_definitions()
    print(f'Analyzing {len(pair_defs)} condition pairs...')

    results = {}
    for key, label, subjects, pre_cond, post_cond, loader in pair_defs:
        print(f'  {key}...')
        results[key] = analyze_pair(key, label, subjects, pre_cond,
                                    post_cond, loader)
        # Sanity: bucket counts should sum to wins-inventory n_paired_questions.
        n = results[key]['n_paired_questions']
        ne = expected_n.get(key)
        ok = (ne == n)
        if not ok:
            print(f'    WARN: n_paired_questions mismatch '
                  f'(this run={n}, wins inventory={ne})')

    print('Computing per-judge sensitivity profile (pooled)...')
    sensitivity = compute_per_judge_sensitivity_profile(results, pair_defs)

    # Write JSON.
    out = {
        'date': '2026-04-28',
        'aggregation': '5-judge primary panel; per-question score is simple mean across the 5 primary judges (haiku, sonnet, opus, gpt4o, gpt54). Question included only when both pre and post have >=3 valid (non-null, non-parse-failure) primary-judge scores.',
        'panel_judges': PRIMARY_JUDGES_LIST,
        'bucket_definitions': BUCKET_DESC,
        'panel_magnitude_bins': [
            {'name': name, 'lo': lo, 'hi': hi if not math.isinf(hi) else None}
            for name, lo, hi in PANEL_MAG_BINS],
        'direction_agreement_categories': {
            'agree': 'sign(judge_Δ_q) matches sign(panel_Δ_q), both nonzero',
            'disagree': 'sign(judge_Δ_q) differs from sign(panel_Δ_q), both nonzero',
            'judge_flat': 'judge_Δ_q == 0 (or panel_Δ_q == 0; only in lt_0.1 bin)',
            'agree_rate_excl_flat': 'agree / (agree + disagree)',
            'agree_rate_incl_flat': 'agree / (agree + disagree + judge_flat)',
        },
        'per_judge_sensitivity_profile_pooling': 'Pooled by (pair, subject, qid, judge) paired-comparison instances. The same (subject, qid) appears in multiple pairs; we count each pre/post pair separately, intentionally (each pair is a distinct probe).',
        'pairs': results,
        'per_judge_sensitivity_profile_pooled': sensitivity,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=lambda o: None)
    print(f'\nWrote {OUT_JSON}')

    md = render_markdown(results, sensitivity, pair_defs)
    OUT_MD.write_text(md, encoding='utf-8')
    print(f'Wrote {OUT_MD}')

    # Console summary.
    print('\n' + '=' * 100)
    print(f'{"pair":<40} {"n":>5} {"anchor":>7} {"+half":>6} '
          f'{"+qrt":>6} {"+sub":>6} {"noise":>6} {"-sub":>6} {"-qrt":>6} {"-half":>6}')
    print('-' * 100)
    for key, _, _, _, _, _ in pair_defs:
        r = results[key]
        b = r['bucket_counts']
        print(f'{key:<40} {r["n_paired_questions"]:>5} '
              f'{b.get("anchor_crossing",0):>7} '
              f'{b.get("same_band_pos_half",0):>6} '
              f'{b.get("same_band_pos_quarter",0):>6} '
              f'{b.get("same_band_pos_subquarter",0):>6} '
              f'{b.get("same_band_noise",0):>6} '
              f'{b.get("same_band_neg_subquarter",0):>6} '
              f'{b.get("same_band_neg_quarter",0):>6} '
              f'{b.get("same_band_neg_half",0):>6}')

    print('\nPer-judge sensitivity profile (pooled):')
    print(f'{"judge":<10} {"n inst":>8} {"nonzero%":>10} {"|d|=1":>7} '
          f'{"|d|=2":>7} {"|d|=3":>7} {"|d|=4":>7} {"avg rho":>9}')
    for judge in PRIMARY_JUDGES_LIST:
        v = sensitivity[judge]
        rho = v['mean_per_pair_spearman_vs_panel_minus']
        print(f'{judge:<10} {v["n_paired_instances"]:>8} '
              f'{(v["nonzero_rate"] or 0)*100:>9.1f}% '
              f'{v["abs_delta_distribution"].get(1,0):>7} '
              f'{v["abs_delta_distribution"].get(2,0):>7} '
              f'{v["abs_delta_distribution"].get(3,0):>7} '
              f'{v["abs_delta_distribution"].get(4,0):>7} '
              f'{rho if rho is not None else 0:>7.3f}')


if __name__ == '__main__':
    main()
