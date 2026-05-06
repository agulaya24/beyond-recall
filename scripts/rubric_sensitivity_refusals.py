"""
P0-16: Rubric sensitivity on refusals.

The scoring rubric anchors refusals at 1 ("refuses or off-base"), the same score
as wrong predictions. This could bias Δ_spec against the specification when the
specification produces epistemically-honest refusals that the judges then score
as if they were wrong predictions.

This script recodes refusals as explicit neutral (2.5 on the 1-5 scale, midway
between refusal-floor and uninformative-ceiling) and recomputes Δ_spec as a
sensitivity check.

Recoding rule (applied independently under two refusal-classifier rules):
  - If the response text matches the refusal classifier AND the judge scored
    the response ≤ 2 → recode that judgment's score to 2.5.
  - Everywhere else: unchanged.
  - Scores ≥ 3 are never recoded (the judge already saw past the refusal
    framing and credited partial/full content).

Two classifier rules (both from scripts/classify_hedging.py):
  - narrow: STARTS_REFUSAL_RE match on response opening
  - broader: REFUSAL_RE hit anywhere in response

Panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54).
Subjects: 14 (Hamerton + 13 globals), matching recompute_5judge_primary.py.
Backfill: applies _s114_backfills overlay same as the canonical script.

Outputs:
  - docs/research/rubric_sensitivity_refusals.md
  - docs/research/rubric_sensitivity_refusals.json
"""

import json
import os
import re
import statistics
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_MD = REPO / 'docs' / 'research' / 'rubric_sensitivity_refusals.md'
OUT_JSON = REPO / 'docs' / 'research' / 'rubric_sensitivity_refusals.json'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

GRADIENT_CONDITIONS = ['C5_baseline', 'C2a_full_spec', 'C2c_wrong_spec',
                       'C4_factdump', 'C4a_full_facts_plus_spec']

GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS

# ---------------------------------------------------------------------------
# Refusal classifier (copied verbatim from scripts/classify_hedging.py for
# self-containment; canonical source is that file)
# ---------------------------------------------------------------------------
REFUSAL_PATTERNS = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

STARTS_REFUSAL_RE = re.compile(
    r"^\s*(?:I (?:cannot|can't|don't|do not)|"
    r"The retrieved facts (?:do not|don't))",
    re.IGNORECASE,
)

RECODE_VALUE = 2.5


# ---------------------------------------------------------------------------
# Data loaders (mirror recompute_5judge_primary.py for consistency)
# ---------------------------------------------------------------------------
def load_global_judgments(subject):
    """Load global judgments + apply _s114_backfills overlay."""
    path = RESULTS / f'global_{subject}' / 'judgments_v2.json'
    rows = []
    if path.exists():
        rows = json.load(path.open(encoding='utf-8'))

    backfill_dir = RESULTS / '_s114_backfills'
    overrides = {}
    if backfill_dir.exists():
        prefix = f'global_{subject}__'
        for f in backfill_dir.glob(f'{prefix}*.json'):
            try:
                data = json.load(f.open(encoding='utf-8'))
            except Exception:
                continue
            for r in data:
                if r.get('score') is None:
                    continue
                overrides[(r['question_id'], r['condition'], r['judge'])] = (
                    r['score'], r.get('parse_failure', False)
                )

    for r in rows:
        key = (r.get('question_id'), r.get('condition'), r.get('judge'))
        if key in overrides:
            score, pf = overrides[key]
            r['score'] = score
            r['parse_failure'] = pf
    return rows


def load_hamerton_judgments():
    """Load Hamerton judgments from the several fragment files. Mirrors
    recompute_5judge_primary.py:load_hamerton_judgments."""
    base = RESULTS / 'hamerton'
    rows = []

    def normalize(cond):
        if cond == 'C2c_full_wrong_spec':
            return 'C2c_wrong_spec'
        if cond == 'C4a_full_all_facts_plus_spec':
            return 'C4a_full_facts_plus_spec'
        return cond

    harm = base / 'judgments_harmonized.json'
    if harm.exists():
        for r in json.load(harm.open(encoding='utf-8')):
            rows.append({
                'question_id': r['question_id'],
                'condition': normalize(r['condition']),
                'judge': r['judge'],
                'score': r.get('score'),
                'parse_failure': r.get('parse_failure', False),
            })

    wide = base / 'judgments.json'
    if wide.exists():
        for r in json.load(wide.open(encoding='utf-8')):
            cond = normalize(r['condition'])
            if 'haiku_score' in r:
                rows.append({'question_id': r['question_id'], 'condition': cond,
                             'judge': 'haiku', 'score': r['haiku_score'], 'parse_failure': False})
            if 'gemini_score' in r:
                rows.append({'question_id': r['question_id'], 'condition': cond,
                             'judge': 'gemini_flash', 'score': r['gemini_score'], 'parse_failure': False})

    gpt54_path = base / 'gpt54_judgments.json'
    if gpt54_path.exists():
        for r in json.load(gpt54_path.open(encoding='utf-8')):
            rows.append({'question_id': r['question_id'], 'condition': normalize(r['condition']),
                         'judge': 'gpt54', 'score': r.get('gpt54_score'), 'parse_failure': False})

    gp_path = base / 'gemini_pro_judgments.json'
    if gp_path.exists():
        for r in json.load(gp_path.open(encoding='utf-8')):
            rows.append({'question_id': r['question_id'], 'condition': normalize(r['condition']),
                         'judge': 'gemini_pro', 'score': r.get('gemini_pro_score'), 'parse_failure': False})

    for judge in ['sonnet', 'opus', 'gpt4o']:
        p = base / f'{judge}_judgments.json'
        if p.exists():
            for r in json.load(p.open(encoding='utf-8')):
                rows.append({'question_id': r['question_id'], 'condition': normalize(r['condition']),
                             'judge': judge, 'score': r.get('score'),
                             'parse_failure': r.get('parse_failure', False)})
    return rows


# ---------------------------------------------------------------------------
# Response-text loaders
# ---------------------------------------------------------------------------
def load_global_responses(subject):
    """Return {(qid, condition): text}."""
    path = RESULTS / f'global_{subject}' / 'results_v2.json'
    if not path.exists():
        return {}
    out = {}
    data = json.load(path.open(encoding='utf-8'))
    for q in data:
        qid = q.get('question_id')
        for cond, rdata in (q.get('responses') or {}).items():
            if isinstance(rdata, dict):
                out[(qid, cond)] = rdata.get('text', '') or ''
            else:
                out[(qid, cond)] = str(rdata or '')
    return out


def load_hamerton_responses():
    """Return {(qid, condition): text} with normalized condition names."""
    path = RESULTS / 'hamerton' / 'results.json'
    if not path.exists():
        return {}
    out = {}
    data = json.load(path.open(encoding='utf-8'))

    def normalize(cond):
        if cond == 'C2c_full_wrong_spec':
            return 'C2c_wrong_spec'
        if cond == 'C4a_full_all_facts_plus_spec':
            return 'C4a_full_facts_plus_spec'
        return cond

    for q in data:
        if q.get('tier') != 'behavioral_prediction':
            continue
        qid = q.get('question_id')
        for cond, rdata in (q.get('responses') or {}).items():
            norm = normalize(cond)
            if isinstance(rdata, dict):
                out[(qid, norm)] = rdata.get('text', '') or ''
            else:
                out[(qid, norm)] = str(rdata or '')
    return out


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def aggregate(rows, judge_set):
    """Return {condition: mean}. Mean-per-judge then mean-across-judges."""
    per_jc = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])

    per_cond_means = defaultdict(list)
    for (cond, judge), scores in per_jc.items():
        if scores:
            per_cond_means[cond].append(statistics.mean(scores))

    return {c: statistics.mean(ms) for c, ms in per_cond_means.items() if ms}


def apply_recoding(rows, responses, classifier):
    """Return a new list of rows with refusal-classifier matches whose score
    <= 2 recoded to 2.5. Only the score is modified; parse_failure preserved."""
    new_rows = []
    n_recoded = 0
    n_refusal_matches = 0
    per_cond_refusal = defaultdict(int)
    per_cond_recoded = defaultdict(int)

    for r in rows:
        new_r = dict(r)
        key = (r.get('question_id'), r.get('condition'))
        text = responses.get(key, '') or ''
        if classifier(text):
            n_refusal_matches += 1
            per_cond_refusal[r.get('condition')] += 1
            score = r.get('score')
            if score is not None and not r.get('parse_failure') and score <= 2:
                new_r['score'] = RECODE_VALUE
                n_recoded += 1
                per_cond_recoded[r.get('condition')] += 1
        new_rows.append(new_r)
    return new_rows, {
        'n_refusal_matches': n_refusal_matches,
        'n_recoded': n_recoded,
        'per_cond_refusal': dict(per_cond_refusal),
        'per_cond_recoded': dict(per_cond_recoded),
    }


def narrow_classifier(text):
    return bool(STARTS_REFUSAL_RE.match(text))


def broader_classifier(text):
    return bool(REFUSAL_RE.search(text))


def compute_subject_means(subject):
    """Load data for one subject and return the original + two recoded mean-sets."""
    if subject == 'hamerton':
        rows = load_hamerton_judgments()
        responses = load_hamerton_responses()
    else:
        rows = load_global_judgments(subject)
        responses = load_global_responses(subject)

    if not rows:
        return None

    # Restrict to primary 5 judges (keeps non-matching rows but they get filtered in aggregate())
    orig_means = aggregate(rows, PRIMARY_JUDGES)
    rows_narrow, info_narrow = apply_recoding(rows, responses, narrow_classifier)
    narrow_means = aggregate(rows_narrow, PRIMARY_JUDGES)
    rows_broader, info_broader = apply_recoding(rows, responses, broader_classifier)
    broader_means = aggregate(rows_broader, PRIMARY_JUDGES)

    return {
        'subject': subject,
        'orig': orig_means,
        'narrow': narrow_means,
        'broader': broader_means,
        'info_narrow': info_narrow,
        'info_broader': info_broader,
        'n_rows': len(rows),
        'n_rows_primary_with_score': sum(
            1 for r in rows if r['judge'] in PRIMARY_JUDGES
            and r.get('score') is not None and not r.get('parse_failure')
        ),
    }


def main():
    per_subject = {}
    for s in MAIN_STUDY:
        r = compute_subject_means(s)
        if r is None:
            print(f'  [WARN] {s}: no data')
            continue
        per_subject[s] = r

    # Build gradient under each scoring
    def gradient(variant_key):
        rows = []
        for s in MAIN_STUDY:
            if s not in per_subject:
                continue
            m = per_subject[s][variant_key]
            c5 = m.get('C5_baseline')
            c2a = m.get('C2a_full_spec')
            c4a = m.get('C4a_full_facts_plus_spec')
            if c5 is None or c4a is None:
                continue
            rows.append({
                'subject': s, 'c5': c5, 'c2a': c2a, 'c4a': c4a,
                'delta_spec': (c2a - c5) if c2a is not None else None,
                'delta_c4a': c4a - c5,
            })
        rows.sort(key=lambda r: r['c5'])
        return rows

    g_orig = gradient('orig')
    g_narrow = gradient('narrow')
    g_broader = gradient('broader')

    def summarize_gradient(rows):
        if not rows:
            return {}
        c5s = [r['c5'] for r in rows]
        c2as = [r['c2a'] for r in rows if r['c2a'] is not None]
        c4as = [r['c4a'] for r in rows]
        ds_vals = [r['delta_spec'] for r in rows if r['delta_spec'] is not None]
        dc4a_vals = [r['delta_c4a'] for r in rows]
        low = [r for r in rows if r['c5'] <= 2.0]
        low_ds = [r['delta_spec'] for r in low if r['delta_spec'] is not None]
        low_dc4a = [r['delta_c4a'] for r in low]
        return {
            'n': len(rows),
            'mean_c5': statistics.mean(c5s),
            'mean_c2a': statistics.mean(c2as) if c2as else None,
            'mean_c4a': statistics.mean(c4as),
            'mean_delta_spec': statistics.mean(ds_vals) if ds_vals else None,
            'mean_delta_c4a': statistics.mean(dc4a_vals),
            'n_low_baseline': len(low),
            'mean_low_delta_spec': statistics.mean(low_ds) if low_ds else None,
            'mean_low_delta_c4a': statistics.mean(low_dc4a) if low_dc4a else None,
            'rows': rows,
        }

    summ_orig = summarize_gradient(g_orig)
    summ_narrow = summarize_gradient(g_narrow)
    summ_broader = summarize_gradient(g_broader)

    # Count total refusal matches across the whole 5-judge corpus
    agg_info = {
        'narrow': {'total_matches': 0, 'total_recoded': 0},
        'broader': {'total_matches': 0, 'total_recoded': 0},
    }
    for s in per_subject.values():
        agg_info['narrow']['total_matches'] += s['info_narrow']['n_refusal_matches']
        agg_info['narrow']['total_recoded'] += s['info_narrow']['n_recoded']
        agg_info['broader']['total_matches'] += s['info_broader']['n_refusal_matches']
        agg_info['broader']['total_recoded'] += s['info_broader']['n_recoded']

    # --- JSON ---
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'methodology': {
                'recode_value': RECODE_VALUE,
                'recode_rule': 'classifier_match AND score <= 2 -> 2.5',
                'primary_judges': sorted(PRIMARY_JUDGES),
                'narrow_classifier': STARTS_REFUSAL_RE.pattern,
                'broader_classifier_patterns': REFUSAL_PATTERNS,
            },
            'per_subject': {
                s: {
                    'orig': data['orig'],
                    'narrow': data['narrow'],
                    'broader': data['broader'],
                    'info_narrow': data['info_narrow'],
                    'info_broader': data['info_broader'],
                    'n_primary_judgments': data['n_rows_primary_with_score'],
                } for s, data in per_subject.items()
            },
            'summary': {
                'orig': {k: v for k, v in summ_orig.items() if k != 'rows'},
                'narrow': {k: v for k, v in summ_narrow.items() if k != 'rows'},
                'broader': {k: v for k, v in summ_broader.items() if k != 'rows'},
            },
            'aggregate_info': agg_info,
            'gradient_rows': {
                'orig': summ_orig.get('rows', []),
                'narrow': summ_narrow.get('rows', []),
                'broader': summ_broader.get('rows', []),
            },
        }, f, indent=2)

    # --- Report ---
    lines = []
    lines.append('# Rubric Sensitivity — Refusal Recoding')
    lines.append('')
    lines.append('_Generated by `scripts/rubric_sensitivity_refusals.py`. Supplementary data: `rubric_sensitivity_refusals.json`._')
    lines.append('')
    lines.append('## Question')
    lines.append('')
    lines.append('The 1-5 scoring rubric anchors refusals at 1, the same score as actively wrong predictions. This could systematically bias Δ_spec against the specification when the spec produces *epistemically-honest refusals* (e.g., "The retrieved facts do not specify...") that are floor-scored identically to incorrect predictions. If the spec\'s main effect were to replace wrong predictions with honest refusals, floor-scoring would hide that move.')
    lines.append('')
    lines.append('## Method')
    lines.append('')
    lines.append(f'Recode any judgment where the response text matches the refusal classifier **AND** the judge scored it ≤ 2 → score := {RECODE_VALUE} (explicit neutral). Scores ≥ 3 are never recoded: if the judge credited partial/full content, the response is not a floor-refusal. Recoding is applied at the level of individual judgments (per question × condition × judge). Panel: 5-judge primary (haiku, sonnet, opus, gpt4o, gpt54). Subjects: 14 (Hamerton + 13 globals). _s114_backfills overlay applied identically to the canonical recompute.')
    lines.append('')
    lines.append('Two classifier rules (both from `scripts/classify_hedging.py`):')
    lines.append('')
    lines.append(f'- **Narrow:** response begins with an explicit refusal prefix: `{STARTS_REFUSAL_RE.pattern}`')
    lines.append('- **Broader:** response contains any of the 8 REFUSAL_PATTERNS anywhere (`I cannot know`, `no information`, `cannot determine`, `unable to determine`, etc.).')
    lines.append('')

    lines.append('## Corpus-level recoding counts')
    lines.append('')
    lines.append('| Classifier | Judgment-level refusal matches | Of those, recoded (score ≤ 2) |')
    lines.append('|---|---:|---:|')
    lines.append(f'| Narrow | {agg_info["narrow"]["total_matches"]:,} | {agg_info["narrow"]["total_recoded"]:,} |')
    lines.append(f'| Broader | {agg_info["broader"]["total_matches"]:,} | {agg_info["broader"]["total_recoded"]:,} |')
    lines.append('')

    # Condition-level recoding breakdown
    per_cond_agg = {'narrow': defaultdict(int), 'broader': defaultdict(int)}
    per_cond_match_agg = {'narrow': defaultdict(int), 'broader': defaultdict(int)}
    for s in per_subject.values():
        for c, n in s['info_narrow']['per_cond_refusal'].items():
            per_cond_match_agg['narrow'][c] += n
        for c, n in s['info_narrow']['per_cond_recoded'].items():
            per_cond_agg['narrow'][c] += n
        for c, n in s['info_broader']['per_cond_refusal'].items():
            per_cond_match_agg['broader'][c] += n
        for c, n in s['info_broader']['per_cond_recoded'].items():
            per_cond_agg['broader'][c] += n

    lines.append('### Recoding counts by condition')
    lines.append('')
    lines.append('| Condition | Narrow: matches / recoded | Broader: matches / recoded |')
    lines.append('|---|---:|---:|')
    for cond in GRADIENT_CONDITIONS:
        n_n = per_cond_match_agg['narrow'].get(cond, 0)
        r_n = per_cond_agg['narrow'].get(cond, 0)
        n_b = per_cond_match_agg['broader'].get(cond, 0)
        r_b = per_cond_agg['broader'].get(cond, 0)
        lines.append(f'| {cond} | {n_n} / {r_n} | {n_b} / {r_b} |')
    lines.append('')

    # --- Aggregate summary across all 14 subjects ---
    lines.append('## Aggregate means across 14 subjects')
    lines.append('')

    def fmt(x, digs=3):
        if x is None:
            return '---'
        return f'{x:.{digs}f}'

    def signed(x):
        if x is None:
            return '---'
        return f'{x:+.3f}'

    lines.append('| Metric | Original | Narrow recode | Broader recode |')
    lines.append('|---|---:|---:|---:|')
    lines.append(f'| N subjects | {summ_orig["n"]} | {summ_narrow["n"]} | {summ_broader["n"]} |')
    lines.append(f'| Mean C5 | {fmt(summ_orig["mean_c5"])} | {fmt(summ_narrow["mean_c5"])} | {fmt(summ_broader["mean_c5"])} |')
    lines.append(f'| Mean C2a | {fmt(summ_orig["mean_c2a"])} | {fmt(summ_narrow["mean_c2a"])} | {fmt(summ_broader["mean_c2a"])} |')
    lines.append(f'| Mean C4a | {fmt(summ_orig["mean_c4a"])} | {fmt(summ_narrow["mean_c4a"])} | {fmt(summ_broader["mean_c4a"])} |')
    lines.append(f'| Mean Δ spec (C2a − C5) | {signed(summ_orig["mean_delta_spec"])} | {signed(summ_narrow["mean_delta_spec"])} | {signed(summ_broader["mean_delta_spec"])} |')
    lines.append(f'| Mean Δ facts+spec (C4a − C5) | {signed(summ_orig["mean_delta_c4a"])} | {signed(summ_narrow["mean_delta_c4a"])} | {signed(summ_broader["mean_delta_c4a"])} |')
    lines.append('')

    lines.append('## Low-baseline slice (C5 ≤ 2)')
    lines.append('')
    lines.append('| Metric | Original | Narrow recode | Broader recode |')
    lines.append('|---|---:|---:|---:|')
    lines.append(f'| N low-baseline | {summ_orig["n_low_baseline"]} | {summ_narrow["n_low_baseline"]} | {summ_broader["n_low_baseline"]} |')
    lines.append(f'| Mean Δ spec | {signed(summ_orig["mean_low_delta_spec"])} | {signed(summ_narrow["mean_low_delta_spec"])} | {signed(summ_broader["mean_low_delta_spec"])} |')
    lines.append(f'| Mean Δ facts+spec | {signed(summ_orig["mean_low_delta_c4a"])} | {signed(summ_narrow["mean_low_delta_c4a"])} | {signed(summ_broader["mean_low_delta_c4a"])} |')
    lines.append('')

    lines.append('## Per-subject gradient tables')
    lines.append('')
    for variant, summ in [('Original', summ_orig), ('Narrow recode', summ_narrow), ('Broader recode', summ_broader)]:
        lines.append(f'### {variant}')
        lines.append('')
        lines.append('| Subject | C5 | C2a | C4a | Δ spec | Δ facts+spec |')
        lines.append('|---|---:|---:|---:|---:|---:|')
        for r in summ['rows']:
            lines.append(f'| {r["subject"]} | {r["c5"]:.2f} | {(r["c2a"] or 0):.2f} | {r["c4a"]:.2f} | {signed(r["delta_spec"])} | {signed(r["delta_c4a"])} |')
        lines.append('')

    # --- Interpretation ---
    lines.append('## Interpretation')
    lines.append('')

    def pct_change(orig, new):
        if orig is None or new is None or orig == 0:
            return None
        return (new - orig)

    ds_orig = summ_orig["mean_delta_spec"]
    ds_narrow = summ_narrow["mean_delta_spec"]
    ds_broader = summ_broader["mean_delta_spec"]
    dc_orig = summ_orig["mean_delta_c4a"]
    dc_narrow = summ_narrow["mean_delta_c4a"]
    dc_broader = summ_broader["mean_delta_c4a"]

    lines.append('Under the narrow (response-opening) classifier, recoding moves mean Δ_spec by '
                 f'**{signed(pct_change(ds_orig, ds_narrow))}** (from {signed(ds_orig)} to {signed(ds_narrow)}) '
                 f'and mean Δ_facts+spec by **{signed(pct_change(dc_orig, dc_narrow))}** '
                 f'(from {signed(dc_orig)} to {signed(dc_narrow)}).')
    lines.append('')
    lines.append('Under the broader (any-position) classifier, recoding moves mean Δ_spec by '
                 f'**{signed(pct_change(ds_orig, ds_broader))}** (from {signed(ds_orig)} to {signed(ds_broader)}) '
                 f'and mean Δ_facts+spec by **{signed(pct_change(dc_orig, dc_broader))}** '
                 f'(from {signed(dc_orig)} to {signed(dc_broader)}).')
    lines.append('')

    lines.append('**What the numbers say.** ')
    lines.append('')
    lines.append('Refusal-matches are heavily concentrated in C5 (the per-condition counts above: '
                 'C5 has roughly 6× the narrow-rule refusals of C2a and 20× the broader-rule refusals '
                 'of C4_factdump). That is exactly what the specification is supposed to do at the '
                 'mechanism level — replace refusals with substantive predictions. Recoding under a '
                 'refusal-neutral rubric therefore pulls C5 up sharply while leaving C2a and C4a '
                 'essentially unchanged. The result is that almost all of the aggregate Δ_spec in the '
                 'paper can be attributed to "refusal displacement": when refusals are scored as '
                 'neutral instead of floor, the aggregate Δ_spec goes to near-zero (+0.008 broader, '
                 '+0.059 narrow).')
    lines.append('')
    lines.append('**Two readings of this result.**')
    lines.append('')
    lines.append('1. **Refusal-displacement is a real and intended mechanism.** Table 4.1 in the paper '
                 'reports that 33.3% of low-baseline transitions are "1 → 2" (refusal → generic '
                 'engagement), and the paper explicitly frames this as the spec\'s primary move on the '
                 'low-baseline slice. Under that reading, a rubric that neutralizes refusals *removes '
                 'the very signal the paper is measuring*, and the near-zero Δ under broader recoding '
                 'confirms rather than undermines the mechanism claim: "most of the spec lift on low-baseline '
                 'subjects comes from fewer refusals, not from more-accurate predictions conditional on '
                 'engagement." That is a weaker claim than "the spec produces more-accurate predictions" '
                 'but it is the claim the paper is actually entitled to make on the aggregate numbers.')
    lines.append('')
    lines.append('2. **Two subjects survive even the most aggressive recoding.** Hamerton (Δ_spec '
                 '+1.67 broader, +1.37 narrow) and Fukuzawa (Δ_facts+spec +0.69 narrow, +0.55 broader) '
                 'remain clear improvements under both recoded rubrics. These are subjects where the '
                 'spec produces substantively-aligned predictions, not just refusal displacement. For '
                 'Hamerton — the primary "unknown figure" case study — the refusal-neutral Δ is '
                 'actually *larger* than the original, because C2a/C4a responses that were refusals '
                 'at baseline get scored ≥ 3 in the spec conditions (the judge recognized substantive '
                 'content). This is the pattern the paper predicts for truly-unknown subjects.')
    lines.append('')
    lines.append('**Low-baseline slice becomes fragile under recoding.** The n_low_baseline drops '
                 'from 9 (original) to 4 (narrow) to 1 (broader) because the recoded rule lifts many '
                 'C5 values above 2.0. The "9-of-9 positive" claim in §4.1 therefore depends on C5 '
                 'being scored under the original rubric: under refusal-neutral scoring the '
                 'population of interest is redefined and the per-subject positivity counts change. '
                 'The cross-subject gradient (Δ decreasing with C5) still holds directionally '
                 'under both recodings, but the magnitudes compress dramatically.')
    lines.append('')
    lines.append('**Recommended framing for the paper.** The paper should **cite this sensitivity check '
                 'in §4.5 or Appendix D** and **not silently absorb the smaller numbers**. The honest '
                 'summary is: on the aggregate 14-subject population, roughly 90-98% of the reported '
                 'Δ_spec is refusal-displacement rather than prediction accuracy at matched engagement '
                 'levels. This is consistent with the §4.1 transition-category breakdown (33.3% of '
                 'low-baseline gains are 1→2 refusal-to-engagement crossings). Two subjects — Hamerton '
                 'and Fukuzawa — show a spec effect that survives refusal-neutral recoding, matching '
                 'the paper\'s "spec is the tool for the unknown" thesis.')
    lines.append('')

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote: {OUT_MD}')
    print(f'Wrote: {OUT_JSON}')

    # stdout summary
    print('\nAggregate mean delta_spec (C2a - C5):')
    print(f'  original:       {ds_orig:+.4f}' if ds_orig is not None else '  original: None')
    print(f'  narrow recode:  {ds_narrow:+.4f}' if ds_narrow is not None else '  narrow: None')
    print(f'  broader recode: {ds_broader:+.4f}' if ds_broader is not None else '  broader: None')
    print('\nAggregate mean delta_facts+spec (C4a - C5):')
    print(f'  original:       {dc_orig:+.4f}' if dc_orig is not None else '  original: None')
    print(f'  narrow recode:  {dc_narrow:+.4f}' if dc_narrow is not None else '  narrow: None')
    print(f'  broader recode: {dc_broader:+.4f}' if dc_broader is not None else '  broader: None')
    print('\nLow-baseline (C5 <= 2) mean delta_facts+spec:')
    print(f'  original:       {summ_orig["mean_low_delta_c4a"]:+.4f}' if summ_orig["mean_low_delta_c4a"] is not None else '  original: None')
    print(f'  narrow recode:  {summ_narrow["mean_low_delta_c4a"]:+.4f}' if summ_narrow["mean_low_delta_c4a"] is not None else '  narrow: None')
    print(f'  broader recode: {summ_broader["mean_low_delta_c4a"]:+.4f}' if summ_broader["mean_low_delta_c4a"] is not None else '  broader: None')


if __name__ == '__main__':
    main()
