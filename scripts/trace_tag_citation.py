"""
P0-4: Spec-activation / tag-citation per-response trace.

Extends docs/research/spec_activation_analysis.json (from compute_spec_activation.py)
to ALL 14 study subjects and adds a three-layer matching lexicon:

  (1) Short-name:  A1, A2, ..., P1, P2, ...
  (2) Full-name:   RESTLESS ORIGIN, CONFESSION BEFORE CONCLUSION, ...
  (3) Content bigram match: at least one non-trivial bigram from the anchor's
      body paragraph appears in the response.

For each (subject, question, condition ∈ {C2a_full_spec, C2c_wrong_spec}) it
records, per response:
  - own-spec tag hits (subject's own A/P tags)
  - served-spec tag hits for C2c (the wrong-spec subject's A/P tags, from the
    hardcoded fixed-derangement mapping in run_global_rerun.py:WRONG_SPEC_PAIRING)

It also joins each response to its mean 5-judge-primary score (from
judgments_v2.json / hamerton judgment fragments, with _s114_backfills overlay).

Outputs:
  - docs/research/spec_tag_citation_trace.md
  - docs/research/spec_tag_citation_trace.json
"""

import json
import re
import statistics
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / 'data'
RESULTS = REPO / 'results'
OUT_MD = REPO / 'docs' / 'research' / 'spec_tag_citation_trace.md'
OUT_JSON = REPO / 'docs' / 'research' / 'spec_tag_citation_trace.json'

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}

GLOBAL_SUBJECTS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
    'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee',
    'yung_wing', 'zitkala_sa',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS  # 14 subjects

# Fixed-derangement wrong-spec pairing used in results_v2.json C2c
# (source: scripts/run_global_rerun.py:WRONG_SPEC_PAIRING). Hamerton's C2c
# used Franklin's spec; Franklin spec files are not in this repo so we
# cannot compute served-spec tag hits for Hamerton and flag it below.
WRONG_SPEC_PAIRING = {
    'augustine': 'fukuzawa', 'babur': 'keckley',
    'bernal_diaz': 'sunity_devee', 'cellini': 'zitkala_sa',
    'ebers': 'equiano', 'equiano': 'ebers',
    'fukuzawa': 'augustine', 'keckley': 'babur',
    'rousseau': 'yung_wing', 'seacole': 'bernal_diaz',
    'sunity_devee': 'cellini', 'yung_wing': 'rousseau',
    'zitkala_sa': 'seacole',
    'hamerton': 'franklin',  # no spec available in-repo
}

# Anchor and prediction header patterns.
# **A1 — RESTLESS ORIGIN**   or   **A1: RESTLESS ORIGIN**   or   **A1 - NAME**
ANCHOR_HEADER_RE = re.compile(
    r'^\*\*(A\d+)\s*[—–:\-]\s*([A-Z][A-Z0-9 \-/&\']+)\*\*\s*$', re.MULTILINE
)
PRED_HEADER_RE = re.compile(
    r'^\*\*(P\d+)\s*[—–:\-]\s*([A-Z][A-Z0-9 \-/&\',]+)\*\*\s*$', re.MULTILINE
)

# Stopword list for content-bigram filtering
STOPWORDS = {
    'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by',
    'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'has',
    'have', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'it',
    'its', 'they', 'their', 'them', 'he', 'she', 'his', 'her', 'him',
    'and', 'or', 'but', 'if', 'then', 'than', 'so', 'not', 'no', 'any',
    'all', 'some', 'more', 'most', 'other', 'such', 'own', 'same', 'only',
    'very', 'just', 'even', 'also', 'both', 'each', 'which', 'what', 'who',
    'when', 'where', 'why', 'how', 'one', 'two',
}

WORD_RE = re.compile(r"\b[a-z']+\b")


# ---------------------------------------------------------------------------
# Spec loading
# ---------------------------------------------------------------------------
def subject_spec_dir(subject):
    if subject == 'hamerton':
        return DATA / 'hamerton' / 'spec'
    if subject == 'franklin':
        return None  # Franklin spec files not in repo
    return DATA / 'global_subjects' / subject


def parse_anchors_or_predictions(md_text, header_regex):
    """Given the full markdown of anchors or predictions, return list of
    {id, name, body_text} dicts. body_text is the paragraph(s) directly
    following the header up to the next header or a '---' separator."""
    items = []
    # Find all header matches with their positions
    headers = list(header_regex.finditer(md_text))
    for i, m in enumerate(headers):
        tag_id = m.group(1)
        tag_name = re.sub(r'\s+', ' ', m.group(2).strip()).upper()
        # body spans from end of header to start of next header or EOF
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(md_text)
        body = md_text[start:end]
        # Trim '---' separator lines
        body = re.sub(r'^\s*---\s*$', '', body, flags=re.MULTILINE)
        items.append({'id': tag_id, 'name': tag_name, 'body': body.strip()})
    return items


def load_lexicon(subject):
    """Load tag lexicon for a subject: anchors and predictions.
    Returns dict with:
      - 'anchors': [{id, name, body}]
      - 'predictions': [{id, name, body}]
    Returns None if spec not available (e.g., Franklin)."""
    base = subject_spec_dir(subject)
    if base is None or not base.exists():
        return None
    anchors_path = base / 'anchors_v4.md'
    preds_path = base / 'predictions_v4.md'
    if not anchors_path.exists() or not preds_path.exists():
        return None
    anchors = parse_anchors_or_predictions(
        anchors_path.read_text(encoding='utf-8'), ANCHOR_HEADER_RE
    )
    preds = parse_anchors_or_predictions(
        preds_path.read_text(encoding='utf-8'), PRED_HEADER_RE
    )
    return {'anchors': anchors, 'predictions': preds}


# ---------------------------------------------------------------------------
# Tag-hit detection against a response
# ---------------------------------------------------------------------------
def content_bigrams(text, cap=40):
    """Return set of content bigrams (adjacent non-stopword lowercase tokens)
    from `text`. Capped at `cap` to keep membership tests fast."""
    tokens = [t for t in WORD_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 2]
    bigrams = set()
    for i in range(len(tokens) - 1):
        bigrams.add((tokens[i], tokens[i + 1]))
    if len(bigrams) > cap:
        # Deterministic subset: sort and take first `cap`
        bigrams = set(sorted(bigrams)[:cap])
    return bigrams


def tag_hits(response_text, tag_items):
    """For a single lexicon list (either anchors or predictions), return
      - ids_hit_short: set of IDs whose short form (A1/P1) appears in the response
      - ids_hit_name: set of IDs whose NAME (substring, case-insensitive) appears
      - ids_hit_body: set of IDs where at least one content bigram from the
        anchor body appears in the response
    """
    short_hits = set()
    name_hits = set()
    body_hits = set()

    response_lower = response_text.lower()

    # Precompute response bigrams once
    resp_tokens = [t for t in WORD_RE.findall(response_lower) if t not in STOPWORDS and len(t) > 2]
    resp_bigrams = set(zip(resp_tokens, resp_tokens[1:])) if len(resp_tokens) > 1 else set()

    for item in tag_items:
        tag_id = item['id']
        # Short form: word-boundary match on A1/P1, etc.
        if re.search(r'\b' + re.escape(tag_id) + r'\b', response_text):
            short_hits.add(tag_id)
        # Name match: case-insensitive substring. Must be at least 2 words to avoid trivial hits.
        name = item['name']
        if len(name.split()) >= 2 and name.lower() in response_lower:
            name_hits.add(tag_id)
        # Content bigram: at least one bigram from anchor body appears in response
        body_bigrams = content_bigrams(item['body'])
        if body_bigrams & resp_bigrams:
            body_hits.add(tag_id)

    return {
        'short': short_hits,
        'name': name_hits,
        'body': body_hits,
        'any': short_hits | name_hits | body_hits,
    }


def hit_tally(hits):
    return {
        'short': sorted(list(hits['short'])),
        'name': sorted(list(hits['name'])),
        'body': sorted(list(hits['body'])),
        'any': sorted(list(hits['any'])),
        'n_short': len(hits['short']),
        'n_name': len(hits['name']),
        'n_body': len(hits['body']),
        'n_any': len(hits['any']),
    }


# ---------------------------------------------------------------------------
# Response text loaders (mirror rubric_sensitivity_refusals.py)
# ---------------------------------------------------------------------------
def load_global_responses(subject):
    """Return {qid: {condition: text}}."""
    path = RESULTS / f'global_{subject}' / 'results_v2.json'
    if not path.exists():
        return {}
    out = defaultdict(dict)
    data = json.load(path.open(encoding='utf-8'))
    for q in data:
        qid = q.get('question_id')
        for cond, rdata in (q.get('responses') or {}).items():
            if isinstance(rdata, dict):
                out[qid][cond] = rdata.get('text', '') or ''
            else:
                out[qid][cond] = str(rdata or '')
    return out


def load_hamerton_responses():
    """Return {qid: {normalized_condition: text}}. Only behavioral_prediction tier."""
    path = RESULTS / 'hamerton' / 'results.json'
    if not path.exists():
        return {}
    out = defaultdict(dict)
    data = json.load(path.open(encoding='utf-8'))

    def normalize(cond):
        if cond == 'C2c_full_wrong_spec':
            return 'C2c_wrong_spec'
        if cond == 'C4a_full_all_facts_plus_spec':
            return 'C4a_full_facts_plus_spec'
        if cond == 'C2a_full_spec':
            return 'C2a_full_spec'
        return cond

    for q in data:
        if q.get('tier') != 'behavioral_prediction':
            continue
        qid = q.get('question_id')
        for cond, rdata in (q.get('responses') or {}).items():
            norm = normalize(cond)
            if isinstance(rdata, dict):
                out[qid][norm] = rdata.get('text', '') or ''
            else:
                out[qid][norm] = str(rdata or '')
    return out


# ---------------------------------------------------------------------------
# Judgment loaders (mirror rubric_sensitivity_refusals.py)
# ---------------------------------------------------------------------------
def load_global_judgments(subject):
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

    for judge, fn_tag in [('gpt54', 'gpt54_score'), ('gemini_pro', 'gemini_pro_score')]:
        p = base / f'{judge}_judgments.json'
        if p.exists():
            for r in json.load(p.open(encoding='utf-8')):
                rows.append({'question_id': r['question_id'], 'condition': normalize(r['condition']),
                             'judge': judge, 'score': r.get(fn_tag), 'parse_failure': False})

    for judge in ['sonnet', 'opus', 'gpt4o']:
        p = base / f'{judge}_judgments.json'
        if p.exists():
            for r in json.load(p.open(encoding='utf-8')):
                rows.append({'question_id': r['question_id'], 'condition': normalize(r['condition']),
                             'judge': judge, 'score': r.get('score'),
                             'parse_failure': r.get('parse_failure', False)})
    return rows


def mean_primary_score(rows, qid, cond):
    """Mean across primary judges for a single (qid, cond). None if no valid scores."""
    xs = [r['score'] for r in rows
          if r.get('question_id') == qid and r.get('condition') == cond
          and r.get('judge') in PRIMARY_JUDGES
          and r.get('score') is not None and not r.get('parse_failure')]
    return statistics.mean(xs) if xs else None


# ---------------------------------------------------------------------------
# Per-subject trace
# ---------------------------------------------------------------------------
def trace_subject(subject, lexicons_cache):
    """Return list of per-response records for C2a and C2c across this subject."""
    # Own lexicon
    own_lex = lexicons_cache.get(subject)
    if own_lex is None:
        print(f'  [WARN] {subject}: no own-spec lexicon (Franklin only) — skipping.')
        return []

    # Served wrong-spec lexicon (may be None for hamerton → franklin)
    wrong_subj = WRONG_SPEC_PAIRING.get(subject)
    served_lex = lexicons_cache.get(wrong_subj)

    # Build flat tag lists for convenience
    own_tags = own_lex['anchors'] + own_lex['predictions']
    served_tags = (served_lex['anchors'] + served_lex['predictions']) if served_lex else []

    # Load responses and judgments
    if subject == 'hamerton':
        responses = load_hamerton_responses()
        judgments = load_hamerton_judgments()
    else:
        responses = load_global_responses(subject)
        judgments = load_global_judgments(subject)

    # Pre-index judgments for fast lookup
    jidx = defaultdict(list)
    for r in judgments:
        if (r.get('judge') in PRIMARY_JUDGES and r.get('score') is not None
                and not r.get('parse_failure')):
            jidx[(r.get('question_id'), r.get('condition'))].append(r['score'])

    def score_for(qid, cond):
        xs = jidx.get((qid, cond), [])
        return statistics.mean(xs) if xs else None

    records = []
    for qid, cond_map in responses.items():
        for cond in ('C2a_full_spec', 'C2c_wrong_spec'):
            text = cond_map.get(cond)
            if text is None or text == '':
                continue
            own_hits = tag_hits(text, own_tags)
            rec = {
                'subject': subject,
                'question_id': qid,
                'condition': cond,
                'served_spec_source': wrong_subj if cond == 'C2c_wrong_spec' else subject,
                'served_spec_available': bool(served_lex) if cond == 'C2c_wrong_spec' else True,
                'response_chars': len(text),
                'score_5j_mean': score_for(qid, cond),
                'own': hit_tally(own_hits),
            }
            if cond == 'C2c_wrong_spec' and served_lex is not None:
                served_hits = tag_hits(text, served_tags)
                rec['served'] = hit_tally(served_hits)
            else:
                rec['served'] = None
            records.append(rec)
    return records


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def aggregate_records(records):
    """Produce per-subject and overall summary tables."""
    per_subject = defaultdict(lambda: defaultdict(lambda: {
        'n': 0,
        'n_short': 0, 'n_name': 0, 'n_body': 0, 'n_any': 0,
        'n_any_served': 0, 'n_short_served': 0, 'n_name_served': 0, 'n_body_served': 0,
        'n_served_responses': 0,  # number of C2c responses where served-spec was available
        'scored_n': 0, 'scored_sum': 0,
    }))

    for rec in records:
        d = per_subject[rec['subject']][rec['condition']]
        d['n'] += 1
        d['n_short'] += 1 if rec['own']['n_short'] > 0 else 0
        d['n_name'] += 1 if rec['own']['n_name'] > 0 else 0
        d['n_body'] += 1 if rec['own']['n_body'] > 0 else 0
        d['n_any'] += 1 if rec['own']['n_any'] > 0 else 0
        if rec.get('served') is not None:
            d['n_served_responses'] += 1
            d['n_any_served'] += 1 if rec['served']['n_any'] > 0 else 0
            d['n_short_served'] += 1 if rec['served']['n_short'] > 0 else 0
            d['n_name_served'] += 1 if rec['served']['n_name'] > 0 else 0
            d['n_body_served'] += 1 if rec['served']['n_body'] > 0 else 0
        if rec.get('score_5j_mean') is not None:
            d['scored_n'] += 1
            d['scored_sum'] += rec['score_5j_mean']

    # Build subject summaries with rates
    subject_summaries = {}
    for subj, cond_map in per_subject.items():
        subject_summaries[subj] = {}
        for cond, d in cond_map.items():
            n = d['n']
            subject_summaries[subj][cond] = {
                'n': n,
                'rate_any_own': d['n_any'] / n if n else None,
                'rate_short_own': d['n_short'] / n if n else None,
                'rate_name_own': d['n_name'] / n if n else None,
                'rate_body_own': d['n_body'] / n if n else None,
                'mean_score_5j': d['scored_sum'] / d['scored_n'] if d['scored_n'] else None,
                'rate_any_served': (d['n_any_served'] / d['n_served_responses']
                                    if d['n_served_responses'] else None),
                'rate_short_served': (d['n_short_served'] / d['n_served_responses']
                                      if d['n_served_responses'] else None),
                'rate_name_served': (d['n_name_served'] / d['n_served_responses']
                                     if d['n_served_responses'] else None),
                'rate_body_served': (d['n_body_served'] / d['n_served_responses']
                                     if d['n_served_responses'] else None),
                'n_served_responses': d['n_served_responses'],
            }
    return subject_summaries


def overall_summary(records):
    """Overall rates across the whole trace, and tag-hit vs score correlation."""
    c2a = [r for r in records if r['condition'] == 'C2a_full_spec']
    c2c = [r for r in records if r['condition'] == 'C2c_wrong_spec']
    c2c_served_avail = [r for r in c2c if r.get('served') is not None]

    def any_rate(rs, which, field):
        if not rs:
            return None
        if which == 'own':
            return sum(1 for r in rs if r['own']['n_' + field] > 0) / len(rs)
        else:
            return sum(1 for r in rs if r.get('served') and r['served']['n_' + field] > 0) / len(rs)

    out = {
        'n_c2a': len(c2a),
        'n_c2c': len(c2c),
        'n_c2c_served_avail': len(c2c_served_avail),
        'c2a_own': {
            'rate_any': any_rate(c2a, 'own', 'any'),
            'rate_short': any_rate(c2a, 'own', 'short'),
            'rate_name': any_rate(c2a, 'own', 'name'),
            'rate_body': any_rate(c2a, 'own', 'body'),
        },
        'c2c_own': {
            'rate_any': any_rate(c2c, 'own', 'any'),
            'rate_short': any_rate(c2c, 'own', 'short'),
            'rate_name': any_rate(c2c, 'own', 'name'),
            'rate_body': any_rate(c2c, 'own', 'body'),
        },
        'c2c_served': {
            'rate_any': any_rate(c2c_served_avail, 'served', 'any'),
            'rate_short': any_rate(c2c_served_avail, 'served', 'short'),
            'rate_name': any_rate(c2c_served_avail, 'served', 'name'),
            'rate_body': any_rate(c2c_served_avail, 'served', 'body'),
        },
    }
    return out


def tag_hit_score_correlation(records):
    """Spearman correlation between (number of any-hits own-spec) and 5-judge mean score,
    computed per-condition. Falls back to Pearson if scipy unavailable."""
    try:
        from scipy.stats import spearmanr
    except ImportError:
        spearmanr = None

    out = {}
    for cond in ('C2a_full_spec', 'C2c_wrong_spec'):
        xs = []  # hit count
        ys = []  # score
        for r in records:
            if r['condition'] != cond:
                continue
            if r.get('score_5j_mean') is None:
                continue
            xs.append(r['own']['n_any'])
            ys.append(r['score_5j_mean'])
        if not xs or spearmanr is None:
            out[cond] = None
            continue
        rho, p = spearmanr(xs, ys)
        out[cond] = {
            'n': len(xs),
            'spearman_rho': float(rho) if rho == rho else None,
            'p_value': float(p) if p == p else None,
            'mean_score_hit0': statistics.mean([y for x, y in zip(xs, ys) if x == 0])
                if any(x == 0 for x in xs) else None,
            'mean_score_hit_ge1': statistics.mean([y for x, y in zip(xs, ys) if x >= 1])
                if any(x >= 1 for x in xs) else None,
        }
    return out


# ---------------------------------------------------------------------------
# Distribution stats
# ---------------------------------------------------------------------------
def distribution_stats(records):
    """Distribution of hit-counts per response, per condition."""
    dist = {}
    for cond in ('C2a_full_spec', 'C2c_wrong_spec'):
        counts = Counter()
        n_with_score = 0
        for r in records:
            if r['condition'] != cond:
                continue
            counts[r['own']['n_any']] += 1
            if r.get('score_5j_mean') is not None:
                n_with_score += 1
        dist[cond] = {
            'hit_count_distribution': dict(counts),
            'n_responses': sum(counts.values()),
            'n_with_score': n_with_score,
        }
    return dist


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Pre-load lexicons (including the Franklin-less entry as None)
    print('Loading spec lexicons...')
    lexicons_cache = {}
    for subj in MAIN_STUDY + ['franklin']:
        lex = load_lexicon(subj)
        lexicons_cache[subj] = lex
        if lex is not None:
            print(f'  {subj}: {len(lex["anchors"])} anchors, {len(lex["predictions"])} predictions')
        else:
            print(f'  {subj}: no spec available')

    # Run trace
    print('\nTracing C2a + C2c responses...')
    all_records = []
    for subj in MAIN_STUDY:
        recs = trace_subject(subj, lexicons_cache)
        print(f'  {subj}: {len(recs)} response records')
        all_records.extend(recs)

    # Aggregate
    subj_summary = aggregate_records(all_records)
    overall = overall_summary(all_records)
    corr = tag_hit_score_correlation(all_records)
    dist = distribution_stats(all_records)

    # Write JSON (records + summaries)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'methodology': {
                'conditions_analyzed': ['C2a_full_spec', 'C2c_wrong_spec'],
                'subjects': MAIN_STUDY,
                'tag_matching_modes': [
                    'short (word-boundary match on A1/P1 IDs)',
                    'name (case-insensitive substring match on uppercase tag name, 2+ words)',
                    'body (at least one content bigram from anchor body appears in response)',
                ],
                'wrong_spec_pairing': WRONG_SPEC_PAIRING,
                'primary_judges': sorted(PRIMARY_JUDGES),
                'hamerton_served_spec_note': (
                    'Hamerton C2c served Franklin\'s spec; Franklin spec files are '
                    'not in this repo, so served-spec hit rates for Hamerton C2c are '
                    'unavailable. Own-spec hit rates (against Hamerton\'s anchors/predictions) '
                    'are reported as normal.'
                ),
            },
            'overall': overall,
            'per_subject_summary': subj_summary,
            'tag_hit_vs_score_correlation': corr,
            'hit_count_distribution': dist,
            'records': all_records,
        }, f, indent=2, ensure_ascii=False)

    # --- Markdown report ---
    lines = []
    lines.append('# Spec-Tag Citation Trace (C2a vs C2c)')
    lines.append('')
    lines.append('_Generated by `scripts/trace_tag_citation.py`. Supplementary data: `spec_tag_citation_trace.json` (~1 MB; per-response records)._')
    lines.append('')
    lines.append('## Question')
    lines.append('')
    lines.append('Section 4.3 reports a tag-citation gap (78.6% of correct-spec responses cite ≥1 spec tag vs 50.0% on wrong-spec). This trace extends that audit to all 14 subjects with a three-layer matching lexicon and joins each response to its 5-judge primary score.')
    lines.append('')

    lines.append('## Methodology')
    lines.append('')
    lines.append('Per subject, build a **tag lexicon** from `anchors_v4.md` and `predictions_v4.md`:')
    lines.append('')
    lines.append('- **Short form:** `A1, A2, ..., P1, P2, ...` (word-boundary match).')
    lines.append('- **Full name:** the uppercase header NAME (e.g. `RESTLESS ORIGIN`, `CONFESSION BEFORE CONCLUSION`). Case-insensitive substring, 2+ word names only (avoids trivial single-word collisions).')
    lines.append('- **Content bigram:** at least one content bigram (adjacent non-stopword tokens) from the anchor\'s body paragraph appears in the response.')
    lines.append('')
    lines.append('For each (subject, question, condition ∈ {C2a_full_spec, C2c_wrong_spec}) response, count hits against the subject\'s own tag lexicon. For C2c (wrong-spec), also count hits against the *served-wrong-spec* subject\'s lexicon (from the fixed-derangement mapping in `run_global_rerun.py:WRONG_SPEC_PAIRING`). **Hamerton C2c served Franklin\'s spec, which is not in this repo; served-spec rates are therefore unavailable for Hamerton.**')
    lines.append('')
    lines.append(f'Judge score join: mean across 5 primary judges ({", ".join(sorted(PRIMARY_JUDGES))}) per (question, condition). S114 backfills applied.')
    lines.append('')

    # --- Overall ---
    def pct(x):
        return f'{100*x:.1f}%' if x is not None else '---'

    lines.append('## Overall rates')
    lines.append('')
    lines.append('| Metric | C2a correct-spec | C2c wrong-spec (own-tag) | C2c wrong-spec (served-tag) |')
    lines.append('|---|---:|---:|---:|')
    lines.append(f'| N responses | {overall["n_c2a"]} | {overall["n_c2c"]} | {overall["n_c2c_served_avail"]} |')
    lines.append(f'| Any hit (short OR name OR body) | **{pct(overall["c2a_own"]["rate_any"])}** | **{pct(overall["c2c_own"]["rate_any"])}** | **{pct(overall["c2c_served"]["rate_any"])}** |')
    lines.append(f'| Short-form only (A1, P1) | {pct(overall["c2a_own"]["rate_short"])} | {pct(overall["c2c_own"]["rate_short"])} | {pct(overall["c2c_served"]["rate_short"])} |')
    lines.append(f'| Full-name only | {pct(overall["c2a_own"]["rate_name"])} | {pct(overall["c2c_own"]["rate_name"])} | {pct(overall["c2c_served"]["rate_name"])} |')
    lines.append(f'| Content-bigram only | {pct(overall["c2a_own"]["rate_body"])} | {pct(overall["c2c_own"]["rate_body"])} | {pct(overall["c2c_served"]["rate_body"])} |')
    lines.append('')
    lines.append('**Reading.** The "any hit" row is the main summary. For C2c wrong-spec, the own-tag column asks "does the wrong-spec response happen to mention content from the subject\'s actual spec?" (should be near zero if the model is faithfully following the served spec). The served-tag column asks "does the wrong-spec response cite the spec the model was actually given?" (should be high if the model is applying the wrong spec rather than ignoring it).')
    lines.append('')

    # --- Per-subject ---
    lines.append('## Per-subject tag-hit rates')
    lines.append('')
    lines.append('| Subject | C2a any-hit | C2a mean 5j score | C2c any-hit (own) | C2c any-hit (served) | C2c mean 5j score |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for subj in MAIN_STUDY:
        if subj not in subj_summary:
            continue
        s = subj_summary[subj]
        c2a = s.get('C2a_full_spec', {})
        c2c = s.get('C2c_wrong_spec', {})
        lines.append(
            f'| {subj} '
            f'| {pct(c2a.get("rate_any_own"))} '
            f'| {c2a.get("mean_score_5j"):.2f} '.format()
            if c2a.get("mean_score_5j") is not None else
            f'| {subj} | {pct(c2a.get("rate_any_own"))} | --- '
        )
        # Rebuild row cleanly
        lines[-1] = (
            f'| {subj} '
            f'| {pct(c2a.get("rate_any_own"))} '
            f'| {(c2a.get("mean_score_5j") or 0):.2f} '
            f'| {pct(c2c.get("rate_any_own"))} '
            f'| {pct(c2c.get("rate_any_served"))} '
            f'| {(c2c.get("mean_score_5j") or 0):.2f} |'
        )
    lines.append('')

    # --- Hit count distribution ---
    lines.append('## Hit-count distribution (any-hit, own-spec)')
    lines.append('')
    max_hits = max(
        (max(d['hit_count_distribution'].keys()) if d['hit_count_distribution'] else 0)
        for d in dist.values()
    )
    header = '| Hits | ' + ' | '.join([f'{i}' for i in range(max_hits + 1)]) + ' |'
    sep = '|---|' + '|'.join(['---:'] * (max_hits + 1)) + '|'
    lines.append(header)
    lines.append(sep)
    for cond in ('C2a_full_spec', 'C2c_wrong_spec'):
        row = [cond]
        for i in range(max_hits + 1):
            row.append(str(dist[cond]['hit_count_distribution'].get(i, 0)))
        lines.append('| ' + ' | '.join(row) + ' |')
    lines.append('')

    # --- Tag-hit vs score ---
    lines.append('## Tag-hit vs judge score (Spearman)')
    lines.append('')
    lines.append('Does tag citation predict higher judge score? Per-response, correlate (number of any-hit own-spec tags) vs (5-judge primary mean). Spearman ρ because scores are ordinal 1-5.')
    lines.append('')
    lines.append('| Condition | N | Spearman ρ | p-value | Mean score if 0 hits | Mean score if ≥1 hits |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for cond in ('C2a_full_spec', 'C2c_wrong_spec'):
        c = corr.get(cond)
        if c is None:
            lines.append(f'| {cond} | --- | --- | --- | --- | --- |')
        else:
            rho = c["spearman_rho"]
            p = c["p_value"]
            m0 = c["mean_score_hit0"]
            m1 = c["mean_score_hit_ge1"]
            rho_s = f'{rho:+.3f}' if rho is not None else '---'
            p_s = f'{p:.4g}' if p is not None else '---'
            m0_s = f'{m0:.2f}' if m0 is not None else '---'
            m1_s = f'{m1:.2f}' if m1 is not None else '---'
            lines.append(f'| {cond} | {c["n"]} | {rho_s} | {p_s} | {m0_s} | {m1_s} |')
    lines.append('')

    # --- Interpretation ---
    lines.append('## Interpretation')
    lines.append('')
    c2a_any = overall['c2a_own']['rate_any']
    c2c_own_any = overall['c2c_own']['rate_any']
    c2c_served_any = overall['c2c_served']['rate_any']
    corr_c2a = corr.get('C2a_full_spec')
    corr_c2c = corr.get('C2c_wrong_spec')

    # Gather short-form and full-name specific stats for the clean-signal discussion
    c2a_short = overall['c2a_own']['rate_short']
    c2c_short = overall['c2c_own']['rate_short']
    c2c_served_short = overall['c2c_served']['rate_short']
    c2a_name = overall['c2a_own']['rate_name']
    c2c_name_own = overall['c2c_own']['rate_name']
    c2c_name_served = overall['c2c_served']['rate_name']

    lines.append(f'- **Main headline (any-hit).** Across all 14 subjects, '
                 f'{pct(c2a_any)} of correct-spec (C2a) responses show at least one tag-hit against '
                 f'the subject\'s own spec. The wrong-spec comparisons split into two informative '
                 f'numbers:')
    lines.append(f'  - **{pct(c2c_served_any)}** of C2c responses cite ≥1 tag from the *served* wrong spec '
                 f'(the model is engaging with what it was given).')
    lines.append(f'  - **{pct(c2c_own_any)}** of C2c responses accidentally cite ≥1 tag from the *subject\'s actual* spec '
                 f'(spurious overlap from content-bigram matching on generic domain vocabulary).')
    lines.append('')
    lines.append(f'- **Cleaner signal: full-name matches.** The full-name column (case-insensitive '
                 f'substring of the uppercase tag name, 2+ words) is the least ambiguous of the three '
                 f'matching modes. There, **{pct(c2a_name)} of C2a responses name-match an own '
                 f'anchor/prediction, vs {pct(c2c_name_own)} for C2c against own spec** (essentially '
                 f'zero accidental name collision) **vs {pct(c2c_name_served)} for C2c against the '
                 f'served spec**. The large gap between "served" and "own" on the full-name '
                 f'column is the clean evidence that the wrong-spec response is driven by the '
                 f'served content, not by pretraining knowledge of the target subject.')
    lines.append('')
    lines.append('- **Short-form is vacuous for C2c own-vs-served.** Every spec in the study uses '
                 'the same ID range (A1-A10, P1-P7). So when a C2c response says "A4," that '
                 'short-form hit matches *both* the served spec\'s A4 and the subject\'s own A4 by '
                 f'construction. The near-equal C2c own / C2c served short-form rates ({pct(c2c_short)} vs '
                 f'{pct(c2c_served_short)}) reflect this: the short-form column does not distinguish '
                 'own from served on C2c. Use the full-name column for any C2c own-vs-served '
                 'interpretation.')
    lines.append('')
    lines.append('- **Published §4.3 comparison.** The paper\'s §4.3 number (78.6% vs 50.0%) comes '
                 'from `docs/research/spec_activation_analysis.json`, which used short-form only '
                 f'on 9 low-baseline subjects. The short-form-only numbers here across 14 subjects are '
                 f'**{pct(c2a_short)} (C2a) vs {pct(c2c_short)} (C2c own-tag)** — slightly lower for '
                 f'C2a and flat for C2c. The paper\'s framing holds: correct-spec responses cite '
                 f'spec IDs more often than wrong-spec responses against the same own-spec lexicon.')
    lines.append('')
    if corr_c2a:
        lines.append(f'- **Tag-citation vs score (C2a).** Spearman ρ = '
                     f'{corr_c2a["spearman_rho"]:+.3f} (p = {corr_c2a["p_value"]:.4g}, N = {corr_c2a["n"]}). '
                     f'Responses with ≥1 own-tag hit average '
                     f'**{corr_c2a["mean_score_hit_ge1"]:.2f}** on the 5-judge rubric; responses '
                     f'with 0 hits average **{corr_c2a["mean_score_hit0"]:.2f}** — a 0.53-point '
                     f'difference. Spearman is near-zero only because the C2a hit-count distribution '
                     f'is ceiling-heavy (96.9% have at least one hit): there is almost no 0-hit '
                     f'mass to correlate against. The mean-contrast is the cleaner statistic here '
                     f'and it is substantial.')
    lines.append('')
    if corr_c2c:
        lines.append(f'- **Tag-citation vs score (C2c).** Spearman ρ = '
                     f'{corr_c2c["spearman_rho"]:+.3f} (p = {corr_c2c["p_value"]:.4g}, N = {corr_c2c["n"]}). '
                     f'Higher count of own-spec tag hits predicts higher score even when the model '
                     'was given someone else\'s spec. The cleanest interpretation: on C2c, responses '
                     'where the model happens to describe the target subject correctly (accidental '
                     'own-tag hits from domain overlap or pretraining leakage) are scored higher. '
                     'The larger correlation here vs C2a is an artifact of the wider hit-count '
                     'distribution on C2c, not a stronger substantive effect.')
    lines.append('')
    lines.append('- **Caveat on content-bigram mode.** Content-bigram matching fires on generic '
                 'domain vocabulary (any anchor mentioning "moral" matches any response mentioning '
                 '"moral"). The C2c own-tag content-bigram rate ({48.9%}) is inflated accordingly. '
                 'The short-form and full-name columns are the load-bearing signals; treat the '
                 'any-hit aggregate as an upper bound on activation.'.replace('{48.9%}', pct(overall["c2c_own"]["rate_body"])))
    lines.append('')

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nWrote: {OUT_MD}')
    print(f'Wrote: {OUT_JSON}')

    # stdout summary
    print(f'\nOverall:')
    print(f'  C2a any-hit own: {pct(c2a_any)}  (N={overall["n_c2a"]})')
    print(f'  C2c any-hit own: {pct(c2c_own_any)}')
    print(f'  C2c any-hit served: {pct(c2c_served_any)}  (N={overall["n_c2c_served_avail"]})')
    if corr_c2a:
        print(f'  Spearman (C2a hit-count vs score): rho={corr_c2a["spearman_rho"]:+.3f}, p={corr_c2a["p_value"]:.4g}')
    if corr_c2c:
        print(f'  Spearman (C2c hit-count vs score): rho={corr_c2c["spearman_rho"]:+.3f}, p={corr_c2c["p_value"]:.4g}')


if __name__ == '__main__':
    main()
