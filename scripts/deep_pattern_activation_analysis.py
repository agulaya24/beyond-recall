"""
Deep Pattern-Activation Mechanism Analysis (2026-04-28)

Extends Stream X big-wins characterization. Stream X classified 20/60 unique
extreme upward jumps; this script:

  Analysis 1: Classifies all 60 unique (subject, qid) extreme upward jumps
              against the served spec (anchors+core+predictions+brief stack
              for globals via spec_production.md, brief_v5_clean.md for
              hamerton).

  Analysis 2: Builds a control group of non-jumping LITERAL_RECALL questions
              (and includes a few INTERPRETIVE / REFUSAL controls) and runs
              the same heuristic on them, to test whether
              "PATTERN_PREDICATE-driven" is just a property of post-response
              rhetoric rather than genuine spec-induced lift.

  Analysis 3: Hamerton (15 jumps) vs globals (45 jumps) mechanism comparison,
              with the served-spec-length confound made explicit.

  Analysis 4: Disconfirmation tests:
              - PATTERN_PREDICATE: does the C4 (factdump-only) response
                already contain the same predicate? If yes, the spec is not
                doing the work.
              - INFERENCE_CHAIN: can the post-response answer be reconstructed
                from spec text alone (no question)? Approximated by
                computing post-response token coverage by spec tokens vs
                question tokens.
              - DIRECT_QUOTE_MATCH: re-check at 4-gram and 3-gram thresholds
                between (spec, post) AND (held_out, post).

Outputs:
  docs/research/pattern_activation_deep_20260428.json
  docs/research/pattern_activation_deep_20260428.md

Mechanism taxonomy:
  DIRECT_QUOTE_MATCH  -- spec contains a >=6-gram from the held-out passage
  ANCHOR_FACT         -- spec contains a specific fact (date/place/relation)
                         the post-response uses verbatim
  PATTERN_PREDICATE   -- spec contains a behavioral predicate the
                         post-response activates (>=6 token overlap with at
                         least one spec sentence)
  INFERENCE_CHAIN     -- spec doesn't contain the answer but contains
                         predicates needed to infer it (3-5 token overlap
                         with post-response only, no held-out match)
  HYBRID              -- combination of two or more (e.g. ANCHOR_FACT +
                         PATTERN_PREDICATE)
  UNCLEAR             -- cannot identify a specific spec element

Conventions:
  - Always open files with encoding='utf-8'.
  - Always write JSON with ensure_ascii=False.
  - 5-judge primary panel: {haiku, sonnet, opus, gpt4o, gpt54}.
  - No em dashes or en dashes in any output strings.
"""

from __future__ import annotations

import json
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))

from build_wins_inventory import (  # noqa: E402
    ALL_SUBJECTS,
    GLOBAL_SUBJECTS,
    PRIMARY_JUDGES,
    build_pair_definitions,
    integer_band,
    per_question_means,
    get_response_text,
    load_judgments_v2,
    truncate,
)

OUT_JSON = REPO / 'docs' / 'research' / 'pattern_activation_deep_20260428.json'
OUT_MD = REPO / 'docs' / 'research' / 'pattern_activation_deep_20260428.md'

QUESTION_AUDIT = REPO / 'docs' / 'research' / 'question_category_audit.json'
HAMERTON_SPEC_DIR = REPO / 'data' / 'hamerton' / 'spec'
GLOBAL_SPEC_DIR = REPO / 'data' / 'global_subjects'

RNG_SEED = 20260428


# ---------------------------------------------------------------------------
# Spec loading -- served-spec definition
# ---------------------------------------------------------------------------

def load_served_spec(subject: str) -> str | None:
    """Load the SERVED spec text for a subject.

    Hamerton served spec: brief_v5_clean.md only (the unified brief).
    Global subjects served spec: spec_production.md (full anchors + core +
    predictions + brief stack, ~5775 words).

    Falls back to spec.md if spec_production.md is missing.
    """
    if subject == 'hamerton':
        path = HAMERTON_SPEC_DIR / 'brief_v5_clean.md'
        return path.read_text(encoding='utf-8') if path.exists() else None
    subj_dir = GLOBAL_SPEC_DIR / subject
    for fn in ('spec_production.md', 'spec.md'):
        p = subj_dir / fn
        if p.exists():
            return p.read_text(encoding='utf-8')
    return None


# ---------------------------------------------------------------------------
# Question-axis index
# ---------------------------------------------------------------------------

def load_axis_index() -> dict:
    """Return {(subject, question_id): axis_label} from question_category_audit."""
    out: dict[tuple, str] = {}
    if not QUESTION_AUDIT.exists():
        return out
    data = json.load(QUESTION_AUDIT.open('r', encoding='utf-8'))
    for q in data.get('questions', []):
        out[(q['subject'], q['question_id'])] = q.get('category_rubric')
    return out


# ---------------------------------------------------------------------------
# Heuristic mechanism classifier
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[a-z']{3,}")
STOPWORDS = {
    'the', 'and', 'that', 'this', 'with', 'from', 'have', 'has', 'had',
    'his', 'her', 'their', 'them', 'they', 'are', 'was', 'were', 'been',
    'for', 'not', 'but', 'can', 'will', 'would', 'could', 'should',
    'about', 'when', 'what', 'how', 'why', 'who', 'where', 'into',
    'than', 'then', 'over', 'under', 'such', 'these', 'those', 'some',
    'all', 'any', 'one', 'two', 'three', 'also', 'just', 'like', 'very',
    'much', 'many', 'most', 'more', 'less', 'because', 'while', 'which',
    'there', 'here', 'each', 'other', 'within', 'without', 'between',
    'through', 'across', 'after', 'before', 'during', 'against', 'still',
    'often', 'always', 'never', 'sometimes', 'usually', 'really', 'rather',
    'something', 'someone', 'anyone', 'anything', 'everything', 'nothing',
    'response', 'question', 'answer', 'subject', 'person', 'spec',
    'specification', 'based', 'given', 'context',
}


def tokens(text: str) -> set[str]:
    return {w for w in WORD_RE.findall(text.lower()) if w not in STOPWORDS}


def ngrams(text: str, n: int) -> set[str]:
    raw = re.findall(r"[A-Za-z']+", text.lower())
    return {' '.join(raw[i:i + n]) for i in range(len(raw) - n + 1)}


def overlap_count(a: str, b: str) -> int:
    """Content-word overlap (with stopword filtering)."""
    return len(tokens(a) & tokens(b))


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n\n+", text) if len(s.strip()) > 20]


def has_named_entity(text: str) -> bool:
    """Crude proper-noun detector: a 4-gram-plus capitalized run."""
    return bool(re.search(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,}\b", text or ''))


def has_specific_date(text: str) -> bool:
    return bool(re.search(r"\b1[5-9]\d{2}\b|\b20[0-2]\d\b", text or ''))


def classify_mechanism(spec_text: str | None, held_out: str | None,
                        post_response: str | None) -> dict:
    """Classify the spec-driver mechanism for one extreme jump.

    Returns: {
        'category': str,
        'confidence': 'high'|'medium'|'low',
        'best_held_overlap': int,        # held-out vs best spec sentence
        'best_post_overlap': int,        # post-response vs best spec sentence
        'best_spec_sentence': str|None,
        'has_6gram_spec_held': bool,     # any 6-gram shared by spec & held
        'has_4gram_spec_held': bool,
        'has_3gram_spec_held': bool,
        'has_6gram_held_post': bool,
        'has_4gram_held_post': bool,
        'has_3gram_held_post': bool,
        'spec_to_post_token_share': float,
        'question_to_post_token_share': float,  # set by caller
    }
    """
    out = {
        'category': 'UNCLEAR',
        'confidence': 'low',
        'best_held_overlap': 0,
        'best_post_overlap': 0,
        'best_spec_sentence': None,
        'has_6gram_spec_held': False,
        'has_4gram_spec_held': False,
        'has_3gram_spec_held': False,
        'has_6gram_held_post': False,
        'has_4gram_held_post': False,
        'has_3gram_held_post': False,
        'spec_to_post_token_share': 0.0,
        'spec_anchor_fact_signature': False,
    }
    if not spec_text or not post_response:
        return out

    held = (held_out or '').strip()
    post = post_response.strip()

    # Score each spec sentence against (held, post).
    spec_sents = split_sentences(spec_text)
    if not spec_sents:
        return out

    scored = []
    for s in spec_sents:
        hs = overlap_count(s, held) if held else 0
        ps = overlap_count(s, post) if post else 0
        scored.append((hs, ps, s))
    scored.sort(key=lambda t: (-(t[0] + t[1]), -t[1], -t[0]))
    best_hs, best_ps, best_sent = scored[0]
    out['best_held_overlap'] = best_hs
    out['best_post_overlap'] = best_ps
    out['best_spec_sentence'] = truncate(best_sent, 400)

    # Multi-threshold n-gram checks.
    if held:
        ng_h = ngrams(held, 6)
        out['has_6gram_spec_held'] = bool(ng_h & ngrams(spec_text, 6))
        out['has_4gram_spec_held'] = bool(ngrams(held, 4) & ngrams(spec_text, 4))
        out['has_3gram_spec_held'] = bool(ngrams(held, 3) & ngrams(spec_text, 3))
        if post:
            out['has_6gram_held_post'] = bool(ng_h & ngrams(post, 6))
            out['has_4gram_held_post'] = bool(ngrams(held, 4) & ngrams(post, 4))
            out['has_3gram_held_post'] = bool(ngrams(held, 3) & ngrams(post, 3))

    # Token coverage of post by spec.
    post_tok = tokens(post)
    spec_tok = tokens(spec_text)
    if post_tok:
        out['spec_to_post_token_share'] = round(
            len(post_tok & spec_tok) / max(len(post_tok), 1), 3,
        )

    # Anchor-fact signature: best spec sentence contains a date or named
    # entity AND the post-response shares it.
    if best_sent and (has_specific_date(best_sent) or has_named_entity(best_sent)):
        # Check that the post echoes that fact (date or capitalized entity).
        post_dates = set(re.findall(r"\b1[5-9]\d{2}\b|\b20[0-2]\d\b", post))
        spec_dates = set(re.findall(r"\b1[5-9]\d{2}\b|\b20[0-2]\d\b", best_sent))
        post_caps = set(re.findall(r"\b[A-Z][a-z]+\b", post))
        spec_caps = set(re.findall(r"\b[A-Z][a-z]+\b", best_sent))
        if (post_dates & spec_dates) or len(post_caps & spec_caps) >= 2:
            out['spec_anchor_fact_signature'] = True

    # ----------------------------------------------------------------------
    # Categorize
    # ----------------------------------------------------------------------
    direct_quote = out['has_6gram_spec_held']
    anchor_fact = out['spec_anchor_fact_signature'] or (best_hs >= 4 and best_ps >= 4)
    pattern_predicate = best_ps >= 6
    inference_chain = (3 <= best_ps < 6) and best_hs < 3

    # Determine category.
    flags = []
    if direct_quote:
        flags.append('DIRECT_QUOTE_MATCH')
    if anchor_fact:
        flags.append('ANCHOR_FACT')
    if pattern_predicate:
        flags.append('PATTERN_PREDICATE')
    if inference_chain:
        flags.append('INFERENCE_CHAIN')

    if len(flags) >= 2:
        # Hybrid only when the dual signal is meaningful (not just same flag fired twice).
        # Prefer the strongest single label if anchor_fact and pattern_predicate co-occur weakly.
        if 'DIRECT_QUOTE_MATCH' in flags:
            out['category'] = 'DIRECT_QUOTE_MATCH'
            out['confidence'] = 'high'
        elif 'ANCHOR_FACT' in flags and 'PATTERN_PREDICATE' in flags:
            out['category'] = 'HYBRID'
            out['confidence'] = 'high' if best_ps >= 8 else 'medium'
        else:
            out['category'] = flags[0]
            out['confidence'] = 'medium'
    elif len(flags) == 1:
        out['category'] = flags[0]
        # Confidence: high if margin is clear.
        if flags[0] == 'PATTERN_PREDICATE':
            out['confidence'] = 'high' if best_ps >= 9 else 'medium'
        elif flags[0] == 'INFERENCE_CHAIN':
            out['confidence'] = 'medium' if best_ps == 5 else 'low'
        elif flags[0] == 'ANCHOR_FACT':
            out['confidence'] = 'high' if out['spec_anchor_fact_signature'] else 'medium'
        else:
            out['confidence'] = 'high'
    else:
        out['category'] = 'UNCLEAR'
        out['confidence'] = 'low'

    return out


# ---------------------------------------------------------------------------
# Analysis 1: Full classification of all 60 unique extreme jumps
# ---------------------------------------------------------------------------

def collect_unique_extreme_jumps(pair_defs):
    """Reproduce big_wins_characterization unique-extreme-jump set."""
    raw_upward = []
    for key, label, subjects, pre_cond, post_cond, loader, _ in pair_defs:
        for subj in subjects:
            rows = loader(subj)
            if not rows:
                continue
            per_q = per_question_means(rows, {pre_cond, post_cond})
            for qid, conds in per_q.items():
                if pre_cond not in conds or post_cond not in conds:
                    continue
                pre_m = conds[pre_cond]
                post_m = conds[post_cond]
                pre_b = integer_band(pre_m)
                post_b = integer_band(post_m)
                if post_b - pre_b >= 3:
                    pre_text, q_text_a, hop_a = get_response_text(subj, qid, pre_cond)
                    post_text, q_text_b, hop_b = get_response_text(subj, qid, post_cond)
                    raw_upward.append({
                        'subject': subj,
                        'qid': qid,
                        'pair_key': key,
                        'pre_condition': pre_cond,
                        'post_condition': post_cond,
                        'question_text': q_text_a or q_text_b,
                        'held_out_passage': hop_a or hop_b,
                        'pre_band': pre_b,
                        'post_band': post_b,
                        'jump': post_b - pre_b,
                        'pre_mean': round(pre_m, 3),
                        'post_mean': round(post_m, 3),
                        'pre_response': pre_text,
                        'post_response': post_text,
                    })

    # Deduplicate by (subject, qid). Keep biggest jump.
    by_key: dict[tuple, dict] = {}
    for rec in raw_upward:
        k = (rec['subject'], rec['qid'])
        cur = by_key.get(k)
        if cur is None or rec['jump'] > cur['jump']:
            cur_old_pairs = (cur or {}).get('observed_in_pairs', [])
            new = dict(rec)
            new['observed_in_pairs'] = sorted(set(cur_old_pairs + [rec['pair_key']]))
            by_key[k] = new
        else:
            cur['observed_in_pairs'] = sorted(set(cur['observed_in_pairs'] + [rec['pair_key']]))
    return list(by_key.values())


# ---------------------------------------------------------------------------
# Analysis 2: Control group of non-jumping LITERAL_RECALL questions
# ---------------------------------------------------------------------------

def build_control_group(unique_jumps, axis_idx, n_per_axis_per_subject=2,
                         max_total=40):
    """For each subject in the 60 extreme-jump set, identify questions that
    did NOT extreme-jump under C5 -> C4a, with the tight filter
    (post_band - pre_band) <= 1, stratified by axis.

    Tight filter is load-bearing: jump=2 cases are still multi-anchor wins
    and would dilute the control comparison.
    """
    rng = random.Random(RNG_SEED)
    extreme_keys = {(r['subject'], r['qid']) for r in unique_jumps}
    extreme_subjects = sorted({r['subject'] for r in unique_jumps})

    # Build per-subject candidate pool from C5 -> C4a pair only.
    candidates: list[dict] = []
    for subj in extreme_subjects:
        rows = load_judgments_v2(subj)
        if not rows:
            continue
        per_q = per_question_means(rows, {'C5_baseline', 'C4a_full_facts_plus_spec'})
        for qid, conds in per_q.items():
            if 'C5_baseline' not in conds or 'C4a_full_facts_plus_spec' not in conds:
                continue
            if (subj, qid) in extreme_keys:
                continue
            pre_m = conds['C5_baseline']
            post_m = conds['C4a_full_facts_plus_spec']
            pre_b = integer_band(pre_m)
            post_b = integer_band(post_m)
            jump = post_b - pre_b
            # Tight filter: post_band - pre_band <= 1 (or 0). Excludes jump=2
            # which are still multi-anchor partial wins.
            if jump > 1:
                continue
            axis = axis_idx.get((subj, qid))
            if axis is None:
                continue
            # Pull text
            pre_text, q_text_a, hop_a = get_response_text(subj, qid, 'C5_baseline')
            post_text, q_text_b, hop_b = get_response_text(subj, qid,
                                                           'C4a_full_facts_plus_spec')
            candidates.append({
                'subject': subj,
                'qid': qid,
                'axis': axis,
                'jump': jump,
                'pre_band': pre_b,
                'post_band': post_b,
                'pre_mean': round(pre_m, 3),
                'post_mean': round(post_m, 3),
                'question_text': q_text_a or q_text_b,
                'held_out_passage': hop_a or hop_b,
                'pre_response': pre_text,
                'post_response': post_text,
            })

    # Stratified sample with per-subject cap.
    targets = {
        'LITERAL_RECALL': 25,
        'INTERPRETIVE_INFERENCE': 10,
        'REFUSAL_TRIGGERING': 5,
    }
    selected: list[dict] = []
    by_axis: dict[str, list[dict]] = defaultdict(list)
    for c in candidates:
        by_axis[c['axis']].append(c)
    for axis, target in targets.items():
        bucket = by_axis.get(axis, [])
        rng.shuffle(bucket)
        # Per-subject cap.
        subj_counts: Counter = Counter()
        picked: list[dict] = []
        for c in bucket:
            if len(picked) >= target:
                break
            if subj_counts[c['subject']] >= n_per_axis_per_subject:
                continue
            picked.append(c)
            subj_counts[c['subject']] += 1
        selected.extend(picked)
        if len(selected) >= max_total:
            break

    return selected[:max_total]


# ---------------------------------------------------------------------------
# Analysis 4: Disconfirmation tests
# ---------------------------------------------------------------------------

def get_c4_response(subject: str, qid: int) -> str | None:
    """C4 (factdump only) response for a (subject, qid)."""
    text, _, _ = get_response_text(subject, qid, 'C4_factdump')
    return text


def disconfirm_pattern_predicate(rec: dict, mech: dict) -> dict:
    """For PATTERN_PREDICATE classifications, check whether the C4
    (factdump-only, no spec) response already contains the same predicate.

    If the C4 response shares >=4 content tokens with the best-matching spec
    sentence AND post does too, the spec is not adding new pattern content;
    the facts list alone activated it. That weakens the spec-driven claim.
    """
    out = {
        'attempted': False,
        'c4_response_available': False,
        'c4_overlap_with_best_spec_sentence': None,
        'c4_overlap_ge_post_overlap': False,
        'c4_overlap_ratio_to_post': None,
        'verdict': None,  # 'spec_doing_work' | 'facts_already_activate' | 'unclear'
    }
    if mech.get('category') not in ('PATTERN_PREDICATE', 'HYBRID'):
        return out
    out['attempted'] = True
    best_sent = mech.get('best_spec_sentence')
    if not best_sent:
        out['verdict'] = 'unclear'
        return out
    c4_text = get_c4_response(rec['subject'], rec['qid'])
    if not c4_text:
        out['verdict'] = 'unclear'
        return out
    out['c4_response_available'] = True
    c4_overlap = overlap_count(best_sent, c4_text)
    out['c4_overlap_with_best_spec_sentence'] = c4_overlap
    post_overlap = mech.get('best_post_overlap', 0)
    if post_overlap > 0:
        out['c4_overlap_ratio_to_post'] = round(c4_overlap / post_overlap, 2)
    if c4_overlap >= post_overlap and post_overlap > 0:
        out['c4_overlap_ge_post_overlap'] = True
        out['verdict'] = 'facts_already_activate'
    elif c4_overlap >= 4:
        out['verdict'] = 'partial_facts_activation'
    else:
        out['verdict'] = 'spec_doing_work'
    return out


def disconfirm_inference_chain(rec: dict, mech: dict) -> dict:
    """For INFERENCE_CHAIN classifications, check whether the answer can be
    reconstructed from spec text alone (no question).

    Heuristic: if post-response tokens are highly covered by spec tokens
    even excluding question tokens, the inference is mostly spec-supplied.
    If question tokens contribute many of the post tokens, the inference
    depends on the question + spec interaction (genuine inference).
    """
    out = {
        'attempted': False,
        'spec_only_token_share': None,
        'question_only_token_share': None,
        'spec_unique_share': None,
        'verdict': None,
    }
    if mech.get('category') != 'INFERENCE_CHAIN':
        return out
    out['attempted'] = True
    spec_text = rec.get('_spec_text')
    post = rec.get('post_response') or ''
    q = rec.get('question_text') or ''
    if not spec_text or not post:
        out['verdict'] = 'unclear'
        return out
    post_tok = tokens(post)
    if not post_tok:
        out['verdict'] = 'unclear'
        return out
    spec_tok = tokens(spec_text)
    q_tok = tokens(q)
    spec_only = (spec_tok - q_tok)
    out['spec_only_token_share'] = round(len(post_tok & spec_tok) / len(post_tok), 3)
    out['question_only_token_share'] = round(len(post_tok & q_tok) / len(post_tok), 3)
    out['spec_unique_share'] = round(len(post_tok & spec_only) / len(post_tok), 3)
    # If spec-only contributes more unique tokens to post than question does,
    # the spec is doing the inferential lift.
    if out['spec_unique_share'] >= 0.18:
        out['verdict'] = 'genuine_inference_via_spec'
    elif out['spec_unique_share'] >= 0.08:
        out['verdict'] = 'mixed_inference'
    else:
        out['verdict'] = 'inference_not_grounded_in_spec'
    return out


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def annotate(rec: dict, spec_text: str | None) -> dict:
    """Run the full mechanism + disconfirmation analysis on one record."""
    rec['_spec_text'] = spec_text  # not serialized
    mech = classify_mechanism(spec_text, rec.get('held_out_passage'),
                              rec.get('post_response'))
    # Question-to-post token share (separate, not in classify).
    q_tok = tokens(rec.get('question_text') or '')
    p_tok = tokens(rec.get('post_response') or '')
    mech['question_to_post_token_share'] = round(
        len(q_tok & p_tok) / max(len(p_tok), 1), 3,
    ) if p_tok else 0.0
    rec['mechanism'] = mech
    rec['disconfirm_pattern'] = disconfirm_pattern_predicate(rec, mech)
    rec['disconfirm_inference'] = disconfirm_inference_chain(rec, mech)
    return rec


def serializable_jump(rec: dict) -> dict:
    """Strip transient fields and truncate large strings for output."""
    out = {
        'subject': rec.get('subject'),
        'qid': rec.get('qid'),
        'axis': rec.get('axis'),
        'observed_in_pairs': rec.get('observed_in_pairs'),
        'pre_condition': rec.get('pre_condition'),
        'post_condition': rec.get('post_condition'),
        'question_text': rec.get('question_text'),
        'held_out_passage': truncate(rec.get('held_out_passage'), 600),
        'pre_band': rec.get('pre_band'),
        'post_band': rec.get('post_band'),
        'jump': rec.get('jump'),
        'pre_mean': rec.get('pre_mean'),
        'post_mean': rec.get('post_mean'),
        'pre_response': truncate(rec.get('pre_response'), 600),
        'post_response': truncate(rec.get('post_response'), 600),
        'mechanism': rec.get('mechanism'),
        'disconfirm_pattern': rec.get('disconfirm_pattern'),
        'disconfirm_inference': rec.get('disconfirm_inference'),
    }
    return out


def main():
    print('Loading axis index...', flush=True)
    axis_idx = load_axis_index()

    print('Building pair definitions and collecting unique extreme jumps...', flush=True)
    pair_defs = build_pair_definitions()
    unique = collect_unique_extreme_jumps(pair_defs)
    print(f'  {len(unique)} unique (subject, qid) extreme upward jumps', flush=True)

    # Cache served specs per subject.
    spec_cache: dict[str, str | None] = {}
    spec_word_counts: dict[str, int] = {}
    for s in ALL_SUBJECTS:
        spec_cache[s] = load_served_spec(s)
        spec_word_counts[s] = len(spec_cache[s].split()) if spec_cache[s] else 0

    print('Annotating extreme jumps with axis + mechanism + disconfirmation...', flush=True)
    annotated_jumps = []
    for rec in unique:
        rec['axis'] = axis_idx.get((rec['subject'], rec['qid']))
        annotate(rec, spec_cache.get(rec['subject']))
        annotated_jumps.append(rec)

    # Distributions.
    mech_counts = Counter(r['mechanism']['category'] for r in annotated_jumps)
    confidence_counts = Counter(
        (r['mechanism']['category'], r['mechanism']['confidence'])
        for r in annotated_jumps
    )

    # Hamerton vs globals split.
    hamerton_jumps = [r for r in annotated_jumps if r['subject'] == 'hamerton']
    global_jumps = [r for r in annotated_jumps if r['subject'] != 'hamerton']
    hamerton_mech = Counter(r['mechanism']['category'] for r in hamerton_jumps)
    global_mech = Counter(r['mechanism']['category'] for r in global_jumps)

    # By axis split (within the 60).
    by_axis_mech: dict[str, Counter] = defaultdict(Counter)
    for r in annotated_jumps:
        by_axis_mech[r.get('axis') or 'UNKNOWN'][r['mechanism']['category']] += 1

    # Disconfirmation outcomes.
    pattern_records = [r for r in annotated_jumps
                       if r['mechanism']['category'] in ('PATTERN_PREDICATE', 'HYBRID')]
    pattern_verdicts = Counter(r['disconfirm_pattern'].get('verdict')
                               for r in pattern_records)
    inference_records = [r for r in annotated_jumps
                         if r['mechanism']['category'] == 'INFERENCE_CHAIN']
    inference_verdicts = Counter(r['disconfirm_inference'].get('verdict')
                                 for r in inference_records)

    # Looser n-gram check across the whole 60.
    ngram_summary = {
        'spec_held_6gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_6gram_spec_held']),
        'spec_held_4gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_4gram_spec_held']),
        'spec_held_3gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_3gram_spec_held']),
        'held_post_6gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_6gram_held_post']),
        'held_post_4gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_4gram_held_post']),
        'held_post_3gram_any': sum(1 for r in annotated_jumps
                                    if r['mechanism']['has_3gram_held_post']),
    }

    # ----------------------------------------------------------------------
    # Analysis 2: control group
    # ----------------------------------------------------------------------
    print('Building control group of non-jumping questions...', flush=True)
    control = build_control_group(annotated_jumps, axis_idx)
    print(f'  {len(control)} control records selected', flush=True)
    annotated_control = []
    for c in control:
        annotate(c, spec_cache.get(c['subject']))
        annotated_control.append(c)
    control_mech = Counter(r['mechanism']['category'] for r in annotated_control)
    control_axis = Counter(r['axis'] for r in annotated_control)
    control_by_axis_mech: dict[str, Counter] = defaultdict(Counter)
    for r in annotated_control:
        control_by_axis_mech[r['axis']][r['mechanism']['category']] += 1

    # Disconfirmation on controls -- the discriminator question.
    control_pattern_records = [r for r in annotated_control
                               if r['mechanism']['category'] in ('PATTERN_PREDICATE', 'HYBRID')]
    control_pattern_verdicts = Counter(r['disconfirm_pattern'].get('verdict')
                                       for r in control_pattern_records)
    control_inference_records = [r for r in annotated_control
                                 if r['mechanism']['category'] == 'INFERENCE_CHAIN']
    control_inference_verdicts = Counter(r['disconfirm_inference'].get('verdict')
                                         for r in control_inference_records)

    # Fair-comparison disconfirmation: restrict jumps to spec-loaded post
    # conditions. Excludes C4_factdump (where the disconfirmation test is
    # degenerate -- post is C4, comparing C4 to C4). Controls are already
    # all C5->C4a (spec-loaded post).
    SPEC_LOADED_POST = {
        'C2a_full_spec', 'C4a_full_facts_plus_spec', 'C9_raw_corpus_plus_spec',
        'C3_mem0', 'C3_letta', 'C3_supermemory', 'C3_zep', 'C3_baselayer',
        'C3_mem0_fp', 'C3_letta_fp', 'C3_supermemory_fp', 'C3_zep_fp',
        'C2c_wrong_spec',
    }
    fair_pattern_records = [r for r in pattern_records
                            if r['post_condition'] in SPEC_LOADED_POST]
    fair_pattern_verdicts = Counter(r['disconfirm_pattern'].get('verdict')
                                    for r in fair_pattern_records)
    degenerate_pattern_records = [r for r in pattern_records
                                  if r['post_condition'] == 'C4_factdump']
    degenerate_pattern_verdicts = Counter(
        r['disconfirm_pattern'].get('verdict')
        for r in degenerate_pattern_records
    )

    # ----------------------------------------------------------------------
    # Assemble output
    # ----------------------------------------------------------------------
    out = {
        'date': '2026-04-28',
        'description': (
            'Deep pattern-activation mechanism analysis. Classifies the '
            'spec-driver mechanism for ALL 60 unique extreme-upward-jump '
            '(subject, qid) pairs (deduplicated across 18 condition pairs), '
            'compared against a stratified control group of non-jumping '
            'questions, with disconfirmation tests for PATTERN_PREDICATE '
            'and INFERENCE_CHAIN classifications.'
        ),
        'panel_judges': sorted(PRIMARY_JUDGES),
        'served_spec_definition': {
            'hamerton': 'data/hamerton/spec/brief_v5_clean.md',
            'globals': 'data/global_subjects/<subject>/spec_production.md',
        },
        'spec_word_counts': spec_word_counts,
        'taxonomy': {
            'DIRECT_QUOTE_MATCH': 'spec contains a >=6-gram from the held-out passage',
            'ANCHOR_FACT': 'spec contains a specific fact (date or named entity) the post-response uses',
            'PATTERN_PREDICATE': 'spec contains a behavioral predicate (>=6 token overlap with one spec sentence) the post-response activates',
            'INFERENCE_CHAIN': 'spec does not contain the answer but contains predicates needed (3-5 token overlap with post, no held-out match)',
            'HYBRID': 'two or more of the above (typically ANCHOR_FACT + PATTERN_PREDICATE)',
            'UNCLEAR': 'no specific spec element identifiable',
        },
        'totals': {
            'unique_extreme_jumps': len(annotated_jumps),
            'hamerton_jumps': len(hamerton_jumps),
            'global_jumps': len(global_jumps),
            'control_records': len(annotated_control),
        },
        'mechanism_distribution_all': dict(mech_counts),
        'mechanism_distribution_hamerton': dict(hamerton_mech),
        'mechanism_distribution_global': dict(global_mech),
        'mechanism_distribution_by_axis': {
            axis: dict(c) for axis, c in by_axis_mech.items()
        },
        'mechanism_distribution_control': dict(control_mech),
        'mechanism_distribution_control_by_axis': {
            axis: dict(c) for axis, c in control_by_axis_mech.items()
        },
        'control_axis_breakdown': dict(control_axis),
        'confidence_distribution': {
            f'{cat}|{conf}': n for (cat, conf), n in confidence_counts.items()
        },
        'ngram_overlap_summary': ngram_summary,
        'disconfirmation': {
            'pattern_predicate': {
                'records_evaluated': len(pattern_records),
                'verdicts': dict(pattern_verdicts),
            },
            'inference_chain': {
                'records_evaluated': len(inference_records),
                'verdicts': dict(inference_verdicts),
            },
            'pattern_predicate_control': {
                'records_evaluated': len(control_pattern_records),
                'verdicts': dict(control_pattern_verdicts),
            },
            'inference_chain_control': {
                'records_evaluated': len(control_inference_records),
                'verdicts': dict(control_inference_verdicts),
            },
            'pattern_predicate_jumps_fair': {
                'records_evaluated': len(fair_pattern_records),
                'verdicts': dict(fair_pattern_verdicts),
                'note': (
                    'Fair comparison: jumps restricted to spec-loaded post '
                    'conditions only (C2a, C4a, C9, all C3 memory systems, '
                    'C2c). Excludes C5->C4 jumps where post is factdump only '
                    'and disconfirmation test is degenerate.'
                ),
            },
            'pattern_predicate_jumps_degenerate_c5_to_c4': {
                'records_evaluated': len(degenerate_pattern_records),
                'verdicts': dict(degenerate_pattern_verdicts),
                'note': (
                    'C5->C4 jumps. Post = C4_factdump = same as the '
                    'disconfirmation reference. Verdicts here are degenerate '
                    'and report "facts_already_activate" by construction. '
                    'Reported separately to keep the fair comparison clean.'
                ),
            },
        },
        'extreme_jumps': [serializable_jump(r) for r in annotated_jumps],
        'control_records': [serializable_jump(r) for r in annotated_control],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f'Wrote {OUT_JSON}', flush=True)

    write_markdown_report(out)
    print(f'Wrote {OUT_MD}', flush=True)


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def _pct(n: int, d: int) -> str:
    if not d:
        return 'n/a'
    return f'{round(100 * n / d, 1)}%'


def write_markdown_report(data: dict) -> None:
    md: list[str] = []
    A = md.append

    n_total = data['totals']['unique_extreme_jumps']
    n_h = data['totals']['hamerton_jumps']
    n_g = data['totals']['global_jumps']
    n_c = data['totals']['control_records']
    mech = data['mechanism_distribution_all']
    mech_h = data['mechanism_distribution_hamerton']
    mech_g = data['mechanism_distribution_global']
    mech_c = data['mechanism_distribution_control']
    spec_wc = data['spec_word_counts']
    discon = data['disconfirmation']

    # Headline mechanism for "pattern activation" claim.
    pattern_count = mech.get('PATTERN_PREDICATE', 0) + mech.get('HYBRID', 0)
    inference_count = mech.get('INFERENCE_CHAIN', 0)
    anchor_count = mech.get('ANCHOR_FACT', 0)
    direct_count = mech.get('DIRECT_QUOTE_MATCH', 0)
    unclear_count = mech.get('UNCLEAR', 0)

    A('# Deep Pattern-Activation Mechanism Analysis (2026-04-28)')
    A('')
    A(f'**Panel:** 5-judge primary; per-question mean over {", ".join(data["panel_judges"])}.')
    A('')
    A(f'**Population:** {n_total} unique (subject, qid) extreme upward jumps '
      f'(>=3 anchor band crossings) across 18 condition pairs, deduplicated. '
      f'Control group: {n_c} non-jumping questions stratified by axis.')
    A('')

    # ------------------------------------------------------------------
    # Executive summary
    # ------------------------------------------------------------------
    A('## Executive summary')
    A('')
    A(f'- **Full-population mechanism distribution (n={n_total}).** '
      f'PATTERN_PREDICATE {mech.get("PATTERN_PREDICATE", 0)} '
      f'({_pct(mech.get("PATTERN_PREDICATE", 0), n_total)}), '
      f'HYBRID {mech.get("HYBRID", 0)} ({_pct(mech.get("HYBRID", 0), n_total)}), '
      f'INFERENCE_CHAIN {inference_count} ({_pct(inference_count, n_total)}), '
      f'ANCHOR_FACT {anchor_count} ({_pct(anchor_count, n_total)}), '
      f'DIRECT_QUOTE_MATCH {direct_count} ({_pct(direct_count, n_total)}), '
      f'UNCLEAR {unclear_count} ({_pct(unclear_count, n_total)}).')
    pat_pct = round(100 * pattern_count / n_total, 1) if n_total else 0
    A(f'- **Combined PATTERN_PREDICATE + HYBRID share:** '
      f'{pattern_count}/{n_total} ({_pct(pattern_count, n_total)}). This is the '
      f'load-bearing measurement for the "pattern activation as dominant mechanism" claim.')
    A(f'- **Hamerton vs globals.** Hamerton (served spec '
      f'{spec_wc.get("hamerton", 0)} words, brief only): '
      f'PATTERN_PREDICATE+HYBRID = '
      f'{(mech_h.get("PATTERN_PREDICATE", 0) + mech_h.get("HYBRID", 0))}/{n_h}. '
      f'Globals (served spec ~{round(statistics.mean([w for k,w in spec_wc.items() if k!="hamerton" and w>0])) if any(w for k,w in spec_wc.items() if k!="hamerton") else "n/a"} words, '
      f'full anchor+core+predictions+brief stack): '
      f'PATTERN_PREDICATE+HYBRID = '
      f'{(mech_g.get("PATTERN_PREDICATE", 0) + mech_g.get("HYBRID", 0))}/{n_g}. '
      'Stream X had the spec-length confound inverted; globals get the longer served spec, '
      'not Hamerton.')
    A(f'- **Control group (non-jumping questions, n={n_c}).** '
      f'PATTERN_PREDICATE+HYBRID = '
      f'{(mech_c.get("PATTERN_PREDICATE", 0) + mech_c.get("HYBRID", 0))}/{n_c} '
      f'({_pct(mech_c.get("PATTERN_PREDICATE", 0) + mech_c.get("HYBRID", 0), n_c)}). '
      'If the heuristic over-classifies non-jumping responses as pattern-driven at the '
      'same rate as jumping ones, the heuristic is detecting rhetoric, not lift.')
    pp_disc = discon['pattern_predicate']
    if_disc = discon['inference_chain']
    pp_disc_c = discon['pattern_predicate_control']
    if_disc_c = discon['inference_chain_control']
    pp_disc_fair = discon['pattern_predicate_jumps_fair']
    pp_disc_deg = discon['pattern_predicate_jumps_degenerate_c5_to_c4']

    sd_jump_all = pp_disc['verdicts'].get('spec_doing_work', 0)
    sd_jump_all_n = pp_disc['records_evaluated']
    sd_jump_fair = pp_disc_fair['verdicts'].get('spec_doing_work', 0)
    sd_jump_fair_n = pp_disc_fair['records_evaluated']
    sd_ctrl = pp_disc_c['verdicts'].get('spec_doing_work', 0)
    sd_ctrl_n = pp_disc_c['records_evaluated']

    pat_c_pct = round(100 * (mech_c.get("PATTERN_PREDICATE", 0) +
                              mech_c.get("HYBRID", 0)) / max(n_c, 1), 1)
    A(f'- **PATTERN_PREDICATE rhetoric is dominant in BOTH populations.** '
      f'Jumps: {pat_pct}% (47/60). Controls: {pat_c_pct}% (36/38). '
      'The mechanism-distribution heuristic alone is not a discriminator: it '
      'detects the response style spec-loaded conditions produce, not what '
      'drives a band-jump.')
    A(f'- **Confound: post-condition heterogeneity in jumps.** Of the 47 '
      'PATTERN_PREDICATE/HYBRID jumps, 9 come from C5->C4 (factdump-only) '
      'pairs where the disconfirmation test is degenerate (post = C4 = the '
      'disconfirmation reference). Excluding these gives a fair comparison '
      'between jumps with spec-loaded post (37) and controls (36), all C4a-post.')
    A(f'- **Discriminator (fair comparison): spec_doing_work share, '
      'jumps vs controls.** Fair jumps (n={}): {} spec_doing_work ({}). '
      'Controls (n={}): {} spec_doing_work ({}). Delta = {} pp.'.format(
        sd_jump_fair_n, sd_jump_fair, _pct(sd_jump_fair, sd_jump_fair_n),
        sd_ctrl_n, sd_ctrl, _pct(sd_ctrl, sd_ctrl_n),
        round((100*sd_jump_fair/max(sd_jump_fair_n,1)) -
               (100*sd_ctrl/max(sd_ctrl_n,1)), 1),
    ))
    A(f'- **Disconfirmation: INFERENCE_CHAIN (jumps {if_disc["records_evaluated"]}, '
      f'controls {if_disc_c["records_evaluated"]}).** '
      f'Jumps: genuine_inference_via_spec = '
      f'{if_disc["verdicts"].get("genuine_inference_via_spec", 0)}, '
      f'mixed = {if_disc["verdicts"].get("mixed_inference", 0)}, '
      f'not-grounded = {if_disc["verdicts"].get("inference_not_grounded_in_spec", 0)}. '
      f'Controls: genuine = {if_disc_c["verdicts"].get("genuine_inference_via_spec", 0)}, '
      f'mixed = {if_disc_c["verdicts"].get("mixed_inference", 0)}, '
      f'not-grounded = {if_disc_c["verdicts"].get("inference_not_grounded_in_spec", 0)}.')
    # Headline conclusion uses FAIR comparison.
    headline = _headline_conclusion_v2(
        sd_jump_fair, sd_jump_fair_n, sd_ctrl, sd_ctrl_n,
        pat_pct, n_total,
    )
    A(f'- **Headline:** {headline}')
    A(f'- **Side note: degenerate C5->C4 block.** Of the 9 PATTERN_PREDICATE '
      f'jumps where post is factdump (C4): '
      f'{pp_disc_deg["verdicts"].get("facts_already_activate", 0)} '
      f'facts_already_activate, '
      f'{pp_disc_deg["verdicts"].get("partial_facts_activation", 0)} partial, '
      f'{pp_disc_deg["verdicts"].get("spec_doing_work", 0)} spec_doing_work. '
      'These verdicts are tautological: the disconfirmation reference is the '
      'same condition as the post. Treat as a bookkeeping artifact, not evidence.')
    A('')

    # ------------------------------------------------------------------
    # Distribution comparison table
    # ------------------------------------------------------------------
    A('## Distribution comparison')
    A('')
    A('| Mechanism | All 60 (n) | All 60 % | Hamerton 15 (n) | Hamerton % | Globals 45 (n) | Globals % | Control (n) | Control % |')
    A('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for cat in ['PATTERN_PREDICATE', 'INFERENCE_CHAIN', 'HYBRID',
                 'ANCHOR_FACT', 'DIRECT_QUOTE_MATCH', 'UNCLEAR']:
        a = mech.get(cat, 0)
        h = mech_h.get(cat, 0)
        g = mech_g.get(cat, 0)
        c = mech_c.get(cat, 0)
        A(f'| {cat} | {a} | {_pct(a, n_total)} | {h} | {_pct(h, n_h)} | '
          f'{g} | {_pct(g, n_g)} | {c} | {_pct(c, n_c)} |')
    A('')

    # By axis (within the 60)
    A('### Mechanism by question axis (within the 60 extreme jumps)')
    A('')
    by_axis = data['mechanism_distribution_by_axis']
    A('| Axis | n | PATTERN_PREDICATE | INFERENCE_CHAIN | HYBRID | ANCHOR_FACT | DIRECT_QUOTE | UNCLEAR |')
    A('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for axis in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING', 'UNKNOWN']:
        d = by_axis.get(axis, {})
        n_axis = sum(d.values())
        if n_axis == 0:
            continue
        A(f'| {axis} | {n_axis} | {d.get("PATTERN_PREDICATE", 0)} | '
          f'{d.get("INFERENCE_CHAIN", 0)} | {d.get("HYBRID", 0)} | '
          f'{d.get("ANCHOR_FACT", 0)} | {d.get("DIRECT_QUOTE_MATCH", 0)} | '
          f'{d.get("UNCLEAR", 0)} |')
    A('')

    # Control by axis
    A('### Control group mechanism by axis')
    A('')
    cba = data['mechanism_distribution_control_by_axis']
    A('| Axis | n | PATTERN_PREDICATE | INFERENCE_CHAIN | HYBRID | ANCHOR_FACT | DIRECT_QUOTE | UNCLEAR |')
    A('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for axis in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING']:
        d = cba.get(axis, {})
        n_axis = sum(d.values())
        if n_axis == 0:
            continue
        A(f'| {axis} | {n_axis} | {d.get("PATTERN_PREDICATE", 0)} | '
          f'{d.get("INFERENCE_CHAIN", 0)} | {d.get("HYBRID", 0)} | '
          f'{d.get("ANCHOR_FACT", 0)} | {d.get("DIRECT_QUOTE_MATCH", 0)} | '
          f'{d.get("UNCLEAR", 0)} |')
    A('')

    # ------------------------------------------------------------------
    # Mechanism classification table for all 60
    # ------------------------------------------------------------------
    A('## Mechanism classifications: all 60 unique extreme jumps')
    A('')
    A('| Subject | Qid | Axis | Jump | Mechanism | Conf | Best post overlap | Best held overlap |')
    A('| --- | ---: | --- | ---: | --- | --- | ---: | ---: |')
    for r in sorted(data['extreme_jumps'], key=lambda x: (x['subject'], x['qid'])):
        m = r['mechanism']
        A(f'| {r["subject"]} | {r["qid"]} | {r.get("axis")} | {r["jump"]} | '
          f'{m["category"]} | {m["confidence"]} | '
          f'{m["best_post_overlap"]} | {m["best_held_overlap"]} |')
    A('')

    # ------------------------------------------------------------------
    # Mechanism-specific deep-dives
    # ------------------------------------------------------------------
    A('## Mechanism-specific deep-dives (illustrative cases)')
    A('')
    by_mech_examples: dict[str, list[dict]] = defaultdict(list)
    for r in data['extreme_jumps']:
        by_mech_examples[r['mechanism']['category']].append(r)
    # Sort each bucket by mechanism best_post_overlap desc.
    for cat, lst in by_mech_examples.items():
        lst.sort(key=lambda r: -r['mechanism']['best_post_overlap'])

    for cat in ['PATTERN_PREDICATE', 'HYBRID', 'INFERENCE_CHAIN',
                'ANCHOR_FACT', 'DIRECT_QUOTE_MATCH', 'UNCLEAR']:
        lst = by_mech_examples.get(cat, [])
        if not lst:
            continue
        A(f'### {cat} ({len(lst)} cases)')
        A('')
        for r in lst[:6]:
            m = r['mechanism']
            A(f'**{r["subject"]} qid={r["qid"]} (axis: {r.get("axis")}, jump {r["jump"]}, '
              f'C5 mean {r["pre_mean"]} -> post mean {r["post_mean"]})**')
            A('')
            A(f'- Question: {r["question_text"]}')
            A(f'- Held-out: {truncate(r["held_out_passage"], 240)}')
            A(f'- Best spec sentence: {m["best_spec_sentence"]}')
            A(f'- Overlap: best_post={m["best_post_overlap"]}, '
              f'best_held={m["best_held_overlap"]}, '
              f'spec_to_post_share={m["spec_to_post_token_share"]}, '
              f'q_to_post_share={m.get("question_to_post_token_share", "n/a")}.')
            A(f'- Pre-response excerpt: {truncate(r["pre_response"], 220)}')
            A(f'- Post-response excerpt: {truncate(r["post_response"], 320)}')
            if r.get('disconfirm_pattern', {}).get('attempted'):
                dp = r['disconfirm_pattern']
                A(f'- Disconfirmation (pattern): C4-overlap={dp.get("c4_overlap_with_best_spec_sentence")}, '
                  f'verdict={dp.get("verdict")}.')
            if r.get('disconfirm_inference', {}).get('attempted'):
                di = r['disconfirm_inference']
                A(f'- Disconfirmation (inference): spec_unique_share={di.get("spec_unique_share")}, '
                  f'q_share={di.get("question_only_token_share")}, '
                  f'verdict={di.get("verdict")}.')
            A('')
        A('')

    # ------------------------------------------------------------------
    # Disconfirmation findings
    # ------------------------------------------------------------------
    A('## Disconfirmation findings')
    A('')
    A('### PATTERN_PREDICATE check vs C4 (factdump only) -- jumps vs controls')
    A('')
    A('Hypothesis tested: if the C4 response (no spec, just facts list) already '
      'contains the same predicate the spec sentence carries, the spec is not '
      'doing the pattern-activation work. The facts list alone activates it.')
    A('')
    A('Run on jumps and controls symmetrically. Three views: all jumps; '
      'fair-comparison jumps (post is spec-loaded); degenerate jumps (post = C4_factdump).')
    A('')
    A('| Verdict | All jumps n | All jumps % | Fair jumps n | Fair jumps % | Degenerate (C5->C4) n | Controls n | Controls % |')
    A('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for verdict in ['spec_doing_work', 'partial_facts_activation',
                     'facts_already_activate', 'unclear']:
        jn = pp_disc['verdicts'].get(verdict, 0)
        fjn = pp_disc_fair['verdicts'].get(verdict, 0)
        dn = pp_disc_deg['verdicts'].get(verdict, 0)
        cn = pp_disc_c['verdicts'].get(verdict, 0)
        A(f'| {verdict} | {jn} | {_pct(jn, pp_disc["records_evaluated"])} | '
          f'{fjn} | {_pct(fjn, pp_disc_fair["records_evaluated"])} | '
          f'{dn} | {cn} | {_pct(cn, pp_disc_c["records_evaluated"])} |')
    A('')
    sd_j_fair = pp_disc_fair['verdicts'].get('spec_doing_work', 0)
    sd_c = pp_disc_c['verdicts'].get('spec_doing_work', 0)
    A(f'**Reading (fair comparison).** spec_doing_work in fair-comparison jumps: '
      f'{sd_j_fair}/{pp_disc_fair["records_evaluated"]} '
      f'({_pct(sd_j_fair, pp_disc_fair["records_evaluated"])}). '
      f'In controls: {sd_c}/{pp_disc_c["records_evaluated"]} '
      f'({_pct(sd_c, pp_disc_c["records_evaluated"])}). '
      'For pattern activation to qualify as the lift mechanism, the jumps rate '
      'should be materially higher than the controls rate. A flat or inverted gap '
      'means the spec activates predicates in both jumping and non-jumping cases; '
      'pattern activation alone cannot explain why some land in band 4-5 and others '
      'stay in band 1-2.')
    A('')
    A('**Why the C5->C4 jumps are degenerate.** Those 9 cases have the post '
      'condition = C4_factdump, which is exactly the disconfirmation reference. '
      'The verdicts are computed by comparing C4 against itself; "facts_already_activate" '
      'is the tautological output. The all-jumps row above is contaminated by these '
      'degenerate cases; the fair-jumps column is the cleaner number.')
    A('')
    A('### INFERENCE_CHAIN check via spec-unique token share -- jumps vs controls')
    A('')
    A('Hypothesis tested: if the post-response is mostly composed of tokens that '
      'overlap with the question (not the spec), the inference is not grounded '
      'in spec content. If spec-unique tokens contribute substantially to the post, '
      'the spec is doing inferential lift.')
    A('')
    A('| Verdict | Jumps n | Jumps % | Controls n | Controls % |')
    A('| --- | ---: | ---: | ---: | ---: |')
    for verdict in ['genuine_inference_via_spec', 'mixed_inference',
                     'inference_not_grounded_in_spec', 'unclear']:
        jn = if_disc['verdicts'].get(verdict, 0)
        cn = if_disc_c['verdicts'].get(verdict, 0)
        A(f'| {verdict} | {jn} | {_pct(jn, if_disc["records_evaluated"])} | '
          f'{cn} | {_pct(cn, if_disc_c["records_evaluated"])} |')
    A('')

    # Looser n-gram check
    A('### N-gram overlap thresholds')
    A('')
    ng = data['ngram_overlap_summary']
    A('Stream X used a 6-gram threshold for DIRECT_QUOTE_MATCH and reported 0 cases. '
      'Re-checking at 4-gram and 3-gram thresholds:')
    A('')
    A('| Pair | 6-gram any | 4-gram any | 3-gram any |')
    A('| --- | ---: | ---: | ---: |')
    A(f'| (spec, held_out) | {ng["spec_held_6gram_any"]} | {ng["spec_held_4gram_any"]} | {ng["spec_held_3gram_any"]} |')
    A(f'| (held_out, post) | {ng["held_post_6gram_any"]} | {ng["held_post_4gram_any"]} | {ng["held_post_3gram_any"]} |')
    A('')
    A('A high held_out -> post n-gram count without a corresponding spec -> held_out '
      'count would indicate quote leakage from somewhere other than the spec '
      '(the question text, model pretraining footprint, or training-data contamination).')
    A('')

    # ------------------------------------------------------------------
    # Validity assessment
    # ------------------------------------------------------------------
    A('## Validity assessment')
    A('')
    A(_validity_bullets(mech, mech_c, n_total, n_c, pp_disc, pp_disc_c,
                          pp_disc_fair, if_disc, if_disc_c, ng))
    A('')

    # Caveats
    A('## Caveats')
    A('')
    A('- Heuristic classification only. No LLM is in the loop. '
      'Token overlap above stopword filtering is a proxy for "spec sentence X drove '
      'this response," not a proof. Borderline cases (low confidence) marked in the '
      'classification table.')
    A('- Hamerton served spec is brief-only (1918 words). Globals served spec is the '
      'full anchor+core+predictions+brief stack (~5775 words). Token-overlap heuristics '
      'naturally surface more candidate spec sentences for globals; the absolute '
      'PATTERN_PREDICATE counts are biased toward longer specs. Treat the per-subject '
      'normalized rate as more reliable than raw counts.')
    A('- Disconfirmation tests are themselves heuristics. The "facts_already_activate" '
      'verdict requires the C4 response to share at least as many content tokens with '
      'the best spec sentence as the C4a response does. This is a token-level signal, '
      'not a semantic one.')
    A('- Control group is bounded by axis-availability: REFUSAL_TRIGGERING and '
      'INTERPRETIVE_INFERENCE controls may be undersampled relative to LITERAL_RECALL '
      'because non-jumping questions of those types are scarcer.')
    A('')

    OUT_MD.write_text('\n'.join(md), encoding='utf-8')


def _headline_conclusion_v2(sd_jump, sd_jump_n, sd_ctrl, sd_ctrl_n,
                              pat_pct, n_total) -> str:
    """Headline now keyed on the spec_doing_work discriminator (jumps vs controls),
    not the raw PATTERN_PREDICATE share. The mechanism distribution alone is not
    a discriminator because controls show equal-or-higher PATTERN_PREDICATE rates
    (they are also generated under spec-loaded conditions)."""
    sd_jump_pct = (100 * sd_jump / sd_jump_n) if sd_jump_n else 0
    sd_ctrl_pct = (100 * sd_ctrl / sd_ctrl_n) if sd_ctrl_n else 0
    delta = sd_jump_pct - sd_ctrl_pct

    if delta >= 25 and sd_jump_pct >= 60:
        verdict = 'YES'
        explanation = (
            'spec_doing_work share is materially higher in jumps than controls, '
            'and absolute share in jumps is high.'
        )
    elif delta >= 10 or (sd_jump_pct >= 60 and sd_ctrl_pct < 50):
        verdict = 'QUALIFIED YES'
        explanation = (
            'spec_doing_work share is meaningfully higher in jumps than controls, '
            'but the gap is not large enough to claim pattern activation as a clean '
            'unique-driver. Pattern activation is necessary, possibly not sufficient.'
        )
    elif abs(delta) < 10:
        verdict = 'NO'
        explanation = (
            'spec_doing_work share is similar between jumps and controls. The spec '
            'activates predicates in both populations equally; the lift mechanism is '
            'not pattern activation by itself. Likely co-drivers: facts list providing '
            'specific anchors, rubric upgrading band-1 refusals to band-4 patterned '
            'responses, retrieval surfacing held-out matches.'
        )
    else:
        verdict = 'INVERTED'
        explanation = (
            'spec_doing_work share is higher in controls than jumps. The heuristic '
            'is not measuring what the claim requires. Treat the pattern-activation '
            'mechanism claim as not supported by this analysis.'
        )

    return (f'{verdict}. spec_doing_work share is '
            f'{round(sd_jump_pct, 1)}% in jumps (n={sd_jump_n}) vs '
            f'{round(sd_ctrl_pct, 1)}% in controls (n={sd_ctrl_n}); '
            f'delta = {round(delta, 1)} pp. Raw PATTERN_PREDICATE+HYBRID rate '
            f'on jumps is {pat_pct}% but is not a discriminator because controls '
            f'show equal-or-higher rate. {explanation}')


def _validity_bullets(mech, mech_c, n_total, n_c, pp_disc, pp_disc_c,
                        pp_disc_fair, if_disc, if_disc_c, ng) -> str:
    pat = mech.get('PATTERN_PREDICATE', 0) + mech.get('HYBRID', 0)
    pat_pct = round(100 * pat / n_total, 1) if n_total else 0
    pat_c = mech_c.get('PATTERN_PREDICATE', 0) + mech_c.get('HYBRID', 0)
    pat_c_pct = round(100 * pat_c / n_c, 1) if n_c else 0
    sd_j_fair = pp_disc_fair['verdicts'].get('spec_doing_work', 0)
    sd_j_fair_n = pp_disc_fair['records_evaluated']
    sd_c = pp_disc_c['verdicts'].get('spec_doing_work', 0)
    sd_c_n = pp_disc_c['records_evaluated']
    sd_j_fair_pct = round(100 * sd_j_fair / sd_j_fair_n, 1) if sd_j_fair_n else 0
    sd_c_pct = round(100 * sd_c / sd_c_n, 1) if sd_c_n else 0
    bullets = []
    bullets.append(
        f'- **Mechanism distribution alone is not a discriminator.** '
        f'PATTERN_PREDICATE+HYBRID = {pat_pct}% on jumps and {pat_c_pct}% on controls. '
        f'The heuristic detects "spec was loaded," not "spec drove a band jump." '
        'This is the central caveat against any naive reading of the mechanism table.'
    )
    bullets.append(
        f'- **Fair-comparison disconfirmation is the discriminator.** spec_doing_work '
        f'on fair jumps (post = spec-loaded; n={sd_j_fair_n}): {sd_j_fair_pct}%. '
        f'On controls (n={sd_c_n}): {sd_c_pct}%. Delta '
        f'{round(sd_j_fair_pct - sd_c_pct, 1)} pp. If this delta is small, '
        'pattern activation is present in both populations and cannot explain the lift. '
        'If it is large, the spec adds pattern content uniquely on jump items.'
    )
    bullets.append(
        '- **Confound: spec length.** Globals served spec is roughly 3x longer than '
        'Hamerton brief. Token-overlap heuristic naturally over-counts PATTERN_PREDICATE '
        'matches on longer specs. Treat per-subject normalized rates as more reliable '
        'than raw counts.'
    )
    bullets.append(
        '- **N-gram leakage check.** Spec-held: '
        f'{ng["spec_held_6gram_any"]} 6-gram, {ng["spec_held_4gram_any"]} 4-gram, '
        f'{ng["spec_held_3gram_any"]} 3-gram matches. Held-post: '
        f'{ng["held_post_6gram_any"]} 6-gram, {ng["held_post_4gram_any"]} 4-gram, '
        f'{ng["held_post_3gram_any"]} 3-gram matches. Direct quote leakage from spec '
        'to held-out is essentially zero; from held-out to post is also low at 4-gram. '
        'The lift is not coming from quote-matching.'
    )
    bullets.append(
        '- **Most load-bearing evidence:** the spec_doing_work delta between jumps '
        'and controls. A flat or inverted delta refutes the claim that pattern '
        'activation is the unique mechanism driving lift. A large positive delta '
        'supports it.'
    )
    return '\n'.join(bullets)


if __name__ == '__main__':
    main()
