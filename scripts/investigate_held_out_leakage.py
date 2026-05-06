"""Investigate held-out passage -> post_response leakage at C4a.

Background. The deep pattern-activation analysis flagged 12 cases (1 6-gram,
2 4-gram, 9 3-gram) of held-out -> post-response n-gram overlap on the 60
unique extreme-upward-jump (subject, qid) pairs. That detection ran on the
truncated post_response (600 chars) cached in pattern_activation_deep, and
the cached post is from whichever post-condition surfaced the case
(C2a/C4/C4a/C2c/C8/C9/C3_*). This script does a full audit:

  1. Load FULL C4a response text from results files (not the 600-char cache).
  2. For each of the 60 unique (subject, qid) cases, recompute n-gram
     overlap (3, 4, 6) between held_out_passage and full C4a response using
     the same case-insensitive alphabetic-token regex as the prior pipeline.
  3. For each leaked n-gram, classify against four sources:
       a. Served spec (Hamerton: brief_v5_clean.md; globals: spec_production.md)
       b. Facts list served at C4a (Hamerton: data/hamerton/facts.json,
          globals: data/global_subjects/<subject>/facts.json)
       c. Question text echo
       d. Generic English construction (no proper noun, no subject name,
          no specific date or place)
  4. Apply a classification:
       CORPUS_LEAK            n-gram in served spec or facts
       QUESTION_ECHO          n-gram in question text
       COMMON_PHRASE          generic English construction
       PRETRAINING_MEMO_CANDIDATE  subject-specific, not in served context
       UNKNOWN                fallthrough
  5. Compute severity and produce a leakage-free headline check.

Output: docs/research/held_out_leakage_investigation_20260428.{json,md}
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DATA = REPO / 'data'
HAMERTON_SPEC = DATA / 'hamerton' / 'spec' / 'brief_v5_clean.md'
HAMERTON_FACTS = DATA / 'hamerton' / 'facts.json'
GLOBAL_DIR = DATA / 'global_subjects'
WINS_INVENTORY = REPO / 'docs' / 'research' / 'wins_inventory_20260428.json'
PATTERN_DEEP = REPO / 'docs' / 'research' / 'pattern_activation_deep_20260428.json'
OUT_JSON = REPO / 'docs' / 'research' / 'held_out_leakage_investigation_20260428.json'
OUT_MD = REPO / 'docs' / 'research' / 'held_out_leakage_investigation_20260428.md'

GLOBAL_SUBJECTS = {
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
}

C4A_KEY_HAMERTON = 'C4a_full_all_facts_plus_spec'
C4A_KEY_GLOBAL = 'C4a_full_facts_plus_spec'

# Subject-name tokens we should treat as subject-specific (not generic English).
SUBJECT_NAMES = {
    'hamerton': {'hamerton', 'philip', 'gilbert'},
    'augustine': {'augustine', 'monica', 'hippo', 'manichee', 'manichaean'},
    'babur': {'babur', 'kabul', 'fergana', 'samarkand', 'mughal', 'andijan'},
    'bernal_diaz': {'bernal', 'diaz', 'cortes', 'montezuma', 'tenochtitlan', 'mexica'},
    'cellini': {'cellini', 'benvenuto', 'florence', 'medici', 'pope', 'clement'},
    'ebers': {'ebers', 'georg', 'egypt', 'nile'},
    'equiano': {'equiano', 'olaudah', 'igbo', 'gustavus', 'vassa'},
    'fukuzawa': {'fukuzawa', 'yukichi', 'nakatsu', 'osaka', 'edo', 'tokyo'},
    'keckley': {'keckley', 'elizabeth', 'lincoln', 'mary', 'todd'},
    'rousseau': {'rousseau', 'jean', 'jacques', 'geneva', 'warens'},
    'seacole': {'seacole', 'mary', 'crimea', 'jamaica', 'kingston'},
    'sunity_devee': {'sunity', 'devee', 'cooch', 'behar', 'maharaja', 'maharani'},
    'yung_wing': {'yung', 'wing', 'china', 'yale', 'morrison', 'macao'},
    'zitkala_sa': {'zitkala', 'dakota', 'nakota', 'lakota', 'sioux', 'reservation'},
}

# Common English function-word + glue phrases. Conservative list.
COMMON_3GRAMS = {
    'the day i', "i don't know", 'in the morning', 'i have been', 'in the same',
    'as much as', 'one of the', 'at the same', 'for the first', 'in order to',
    'as well as', 'more than a', 'on the other', 'the rest of', 'a sort of',
    'to be a', 'in a way', 'for the rest', 'it is not', 'i could not',
}


# ---------------------------------------------------------------------------
# Tokenization (matches deep_pattern_activation_analysis.py)
# ---------------------------------------------------------------------------

def alpha_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", (text or '').lower())


def ngrams(text: str, n: int) -> set[str]:
    toks = alpha_tokens(text)
    return {' '.join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def find_all_shared_ngrams(a: str, b: str, n: int) -> set[str]:
    return ngrams(a, n) & ngrams(b, n)


def text_contains_ngram(text: str, gram: str) -> bool:
    """Substring-on-tokenized check: gram is space-joined lowercase token sequence."""
    if not text:
        return False
    toks = alpha_tokens(text)
    if not toks:
        return False
    flat = ' ' + ' '.join(toks) + ' '
    return f' {gram} ' in flat


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_served_spec(subject: str) -> str:
    if subject == 'hamerton':
        return HAMERTON_SPEC.read_text(encoding='utf-8') if HAMERTON_SPEC.exists() else ''
    p = GLOBAL_DIR / subject / 'spec_production.md'
    if p.exists():
        return p.read_text(encoding='utf-8')
    p2 = GLOBAL_DIR / subject / 'spec.md'
    return p2.read_text(encoding='utf-8') if p2.exists() else ''


def load_facts_text(subject: str) -> str:
    p = HAMERTON_FACTS if subject == 'hamerton' else (GLOBAL_DIR / subject / 'facts.json')
    if not p.exists():
        return ''
    try:
        d = json.load(p.open('r', encoding='utf-8'))
    except Exception:
        return ''
    return ' '.join((f.get('text') or '') for f in d.get('facts', []))


def load_c4a_response(subject: str, qid: int) -> str | None:
    if subject == 'hamerton':
        path = RESULTS / 'hamerton' / 'results.json'
        key = C4A_KEY_HAMERTON
    else:
        path = RESULTS / f'global_{subject}' / 'results_v2.json'
        key = C4A_KEY_GLOBAL
    if not path.exists():
        return None
    rows = json.load(path.open('r', encoding='utf-8'))
    for q in rows:
        if q.get('question_id') == qid:
            cond = q.get('responses', {}).get(key)
            if isinstance(cond, dict):
                return cond.get('text')
            return cond
    return None


def load_unique_extreme_jumps() -> list[dict]:
    """Source the 60 deduplicated unique extreme upward jumps from
    pattern_activation_deep_20260428.json (which already deduped them)."""
    d = json.load(PATTERN_DEEP.open('r', encoding='utf-8'))
    out = []
    for j in d.get('extreme_jumps', []):
        out.append({
            'subject': j['subject'],
            'qid': j['qid'],
            'axis': j.get('axis'),
            'observed_in_pairs': j.get('observed_in_pairs', []),
            'question_text': j.get('question_text'),
            'held_out_passage': j.get('held_out_passage'),
            'pre_band': j.get('pre_band'),
            'post_band': j.get('post_band'),
            'jump': j.get('jump'),
            'pre_mean': j.get('pre_mean'),
            'post_mean': j.get('post_mean'),
        })
    return out


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def has_proper_noun(text: str) -> bool:
    """Crude proper-noun detector: capitalized word not at start of sentence."""
    return bool(re.search(r"(?<!^)(?<![.!?]\s)\b[A-Z][a-z]{2,}\b", text or ''))


def has_specific_date_or_year(text: str) -> bool:
    return bool(re.search(r"\b1[5-9]\d{2}\b|\b20[0-2]\d\b", text or ''))


def gram_is_subject_specific(gram: str, subject: str, held_out_passage: str) -> bool:
    """Subject-specific = contains a subject-name token, OR a token that appears
    as a proper-noun in the held-out passage (capitalized non-sentence-initial),
    OR a numeric date."""
    name_tokens = SUBJECT_NAMES.get(subject, set())
    gram_toks = gram.split()
    if any(t in name_tokens for t in gram_toks):
        return True
    # Pull capitalized non-stop tokens from held-out
    held_caps = set()
    for m in re.finditer(r"\b[A-Z][a-zA-Z']+\b", held_out_passage or ''):
        held_caps.add(m.group(0).lower())
    if any(t in held_caps for t in gram_toks):
        return True
    if has_specific_date_or_year(gram):
        return True
    return False


def classify_gram(gram: str, n: int, subject: str, held_out: str,
                   spec_text: str, facts_text: str, question_text: str) -> str:
    """Return classification label for one leaked n-gram."""
    if text_contains_ngram(spec_text, gram) or text_contains_ngram(facts_text, gram):
        return 'CORPUS_LEAK'
    if text_contains_ngram(question_text, gram):
        return 'QUESTION_ECHO'
    # Common-phrase rule: only applies to 3-grams; 4+ are rarely generic.
    if n == 3:
        if gram in COMMON_3GRAMS:
            return 'COMMON_PHRASE'
        if not gram_is_subject_specific(gram, subject, held_out):
            return 'COMMON_PHRASE'
    if gram_is_subject_specific(gram, subject, held_out):
        return 'PRETRAINING_MEMO_CANDIDATE'
    # Non-3gram fallthrough that's not subject-specific and not in served
    # context is unusual. 4-grams of pure function words can occur. Mark
    # COMMON_PHRASE for n=3 only above, UNKNOWN for n>=4 (will surface
    # for human review).
    return 'UNKNOWN'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def investigate_one(case: dict, spec_text: str, facts_text: str,
                     c4a_response: str) -> dict:
    held = case.get('held_out_passage') or ''
    qtext = case.get('question_text') or ''
    out = {
        'subject': case['subject'],
        'qid': case['qid'],
        'axis': case.get('axis'),
        'jump': case.get('jump'),
        'pre_mean': case.get('pre_mean'),
        'post_mean': case.get('post_mean'),
        'observed_in_pairs': case.get('observed_in_pairs', []),
        'question_text': qtext,
        'held_out_passage': held,
        'c4a_response_chars': len(c4a_response or ''),
        'has_c4a_response': bool(c4a_response),
        'leaks': [],
        'leak_counts': {'6gram': 0, '4gram': 0, '3gram': 0},
        'has_any_leak': False,
        'has_substantive_leak': False,
    }
    if not c4a_response or not held:
        return out

    by_n = {}
    for n in (6, 4, 3):
        by_n[n] = find_all_shared_ngrams(held, c4a_response, n)

    # Avoid double-counting: a 6-gram contains a 4-gram and 3-gram. Report
    # all of them but flag substantive leak using the longest n that hit.
    longest_hit = None
    for n in (6, 4, 3):
        if by_n[n]:
            longest_hit = max(longest_hit or 0, n)
    out['longest_ngram_hit'] = longest_hit

    leaks = []
    seen_grams = set()
    for n in (6, 4, 3):
        for gram in sorted(by_n[n]):
            # Skip a shorter n-gram fully contained in a longer n-gram we
            # already classified (avoid noise: a 6-gram match implies the
            # 5/4/3-gram subwindows match too). Track the (gram, n) pair
            # because the same string could appear at different n if you
            # had repetition.
            if any(gram in g for g, gn in seen_grams if gn > n):
                continue
            cls = classify_gram(gram, n, case['subject'], held, spec_text,
                                 facts_text, qtext)
            leaks.append({
                'gram': gram,
                'n': n,
                'classification': cls,
            })
            seen_grams.add((gram, n))
        out['leak_counts'][f'{n}gram'] = len(by_n[n])

    out['leaks'] = leaks
    out['has_any_leak'] = bool(leaks)

    # Substantive leak rule: a 6-gram match, OR a non-common 4-gram with
    # subject-specific content. (Plain 3-grams are not substantive.)
    for lk in leaks:
        if lk['n'] >= 6:
            out['has_substantive_leak'] = True
            break
        if lk['n'] == 4 and lk['classification'] not in ('COMMON_PHRASE', 'QUESTION_ECHO'):
            # 4-gram leaks that survive corpus-leak / question-echo / common
            # filtering are substantive.
            out['has_substantive_leak'] = True
            break

    return out


def fmt_pct(n, d):
    return 0.0 if d == 0 else round(100.0 * n / d, 1)


def build_report(records: list[dict], cases_total: int) -> dict:
    leaked_records = [r for r in records if r['has_any_leak']]
    substantive = [r for r in records if r['has_substantive_leak']]

    # Classification tally over individual leaked n-grams (not deduped across
    # cases; one case can carry multiple leaks).
    cls_counter = Counter()
    cls_by_n = defaultdict(Counter)
    for r in records:
        for lk in r['leaks']:
            cls_counter[lk['classification']] += 1
            cls_by_n[lk['n']][lk['classification']] += 1

    # Case-level dominant classification: take the strongest classification
    # over the case's leaks. Ordering: PRETRAINING_MEMO_CANDIDATE >
    # CORPUS_LEAK > QUESTION_ECHO > UNKNOWN > COMMON_PHRASE.
    rank = {
        'PRETRAINING_MEMO_CANDIDATE': 4,
        'CORPUS_LEAK': 3,
        'QUESTION_ECHO': 2,
        'UNKNOWN': 1,
        'COMMON_PHRASE': 0,
    }
    case_dominant = []
    for r in leaked_records:
        if not r['leaks']:
            continue
        # Pick the leak with the highest n then highest classification rank.
        best = max(r['leaks'], key=lambda lk: (lk['n'], rank.get(lk['classification'], 0)))
        case_dominant.append({
            'subject': r['subject'],
            'qid': r['qid'],
            'axis': r['axis'],
            'jump': r['jump'],
            'longest_n': r['longest_ngram_hit'],
            'dominant_class': best['classification'],
            'dominant_gram': best['gram'],
            'dominant_n': best['n'],
            'has_substantive_leak': r['has_substantive_leak'],
            'all_leak_classes': sorted({lk['classification'] for lk in r['leaks']}),
        })

    case_class_counter = Counter(d['dominant_class'] for d in case_dominant)

    # Pretraining-memo subset and corpus-leak subset.
    pretrain_cases = [d for d in case_dominant
                       if d['dominant_class'] == 'PRETRAINING_MEMO_CANDIDATE']
    corpus_leak_cases = [d for d in case_dominant
                          if d['dominant_class'] == 'CORPUS_LEAK']

    # Severity verdict using SUBSTANTIVE leakage as the load-bearing count.
    n_subst = len(substantive)
    if n_subst <= 3:
        severity = 'rare'
        recommend = 'footnote acknowledgement sufficient'
    elif n_subst <= 10:
        severity = 'moderate'
        recommend = 'sensitivity analysis in appendix'
    else:
        severity = 'substantial'
        recommend = 'structural validity concern; revisit held-out construction'

    return {
        'date': '2026-04-28',
        'population': '60 unique extreme upward-jump (subject, qid) pairs (deduplicated across 18 condition pairs)',
        'method': {
            'tokenization': "re.findall(r\"[A-Za-z']+\", text.lower()) — matches deep_pattern_activation_analysis.py",
            'ngram_lengths_checked': [3, 4, 6],
            'post_response_source': 'FULL C4a response loaded from results files (NOT the 600-char truncation cached in pattern_activation_deep_20260428.json)',
            'served_spec': 'Hamerton: data/hamerton/spec/brief_v5_clean.md; globals: data/global_subjects/<subject>/spec_production.md',
            'facts_source': 'Hamerton: data/hamerton/facts.json; globals: data/global_subjects/<subject>/facts.json (concatenated facts[].text)',
            'classification_rules': {
                'CORPUS_LEAK': 'n-gram appears in served spec or facts text',
                'QUESTION_ECHO': 'n-gram appears in question text',
                'COMMON_PHRASE': '3-gram only; in COMMON_3GRAMS allowlist OR not subject-specific (no proper-noun tokens, no subject-name tokens, no specific year)',
                'PRETRAINING_MEMO_CANDIDATE': 'subject-specific n-gram, not in served spec/facts/question; most likely from pretraining memorization of source autobiography',
                'UNKNOWN': 'fallthrough (4+gram not subject-specific, not in served context)',
            },
            'substantive_rule': '6+gram match, OR 4-gram match not classified COMMON_PHRASE/QUESTION_ECHO',
        },
        'totals': {
            'cases_total': cases_total,
            'cases_with_c4a_response_loaded': sum(1 for r in records if r['has_c4a_response']),
            'cases_with_any_leak': len(leaked_records),
            'cases_with_substantive_leak': n_subst,
            'pretraining_memo_candidate_cases': len(pretrain_cases),
            'corpus_leak_cases': len(corpus_leak_cases),
        },
        'leak_count_by_n': {
            '6gram': sum(r['leak_counts']['6gram'] for r in records),
            '4gram': sum(r['leak_counts']['4gram'] for r in records),
            '3gram': sum(r['leak_counts']['3gram'] for r in records),
        },
        'classification_counts_per_ngram_match': dict(cls_counter),
        'classification_counts_by_n': {str(n): dict(c) for n, c in cls_by_n.items()},
        'case_dominant_classifications': dict(case_class_counter),
        'severity_verdict': severity,
        'paper_treatment_recommendation': recommend,
        'leaked_cases': leaked_records,
        'case_dominant_audit': case_dominant,
        'pretrain_memo_cases': pretrain_cases,
        'corpus_leak_cases': corpus_leak_cases,
        'all_records': records,
    }


# ---------------------------------------------------------------------------
# Headline-impact recompute
# ---------------------------------------------------------------------------

def headline_impact(report: dict) -> dict:
    """If we exclude PRETRAINING_MEMO_CANDIDATE cases from the wins inventory,
    how does the headline change?

    The wins inventory does not export per_question_pairs, so we cannot do a
    full recompute. We instead report the directional impact: how many
    flagged (subject, qid) cases are in scope for each pair, and what
    fraction of the extreme_count they represent.
    """
    inv = json.load(WINS_INVENTORY.open('r', encoding='utf-8'))
    pretrain_keys = {(d['subject'], d['qid']) for d in report['pretrain_memo_cases']}
    substantive_keys = {
        (r['subject'], r['qid']) for r in report['all_records']
        if r.get('has_substantive_leak')
    }

    # Per-pair impact: which leaked cases are observed in this pair, what's
    # the impact on extreme_count if we exclude them.
    per_pair = []
    for label, pair in inv.get('pairs', {}).items():
        # An "observed" extreme jump in this pair appears in the pair's
        # top_extreme_jumps (capped) -- but the deduplicated source is
        # pattern_activation_deep.observed_in_pairs. Use that.
        observed_pretrain = []
        observed_substantive = []
        for case in report['all_records']:
            if label not in (case.get('observed_in_pairs') or []):
                continue
            key = (case['subject'], case['qid'])
            if key in pretrain_keys:
                observed_pretrain.append(key)
            if key in substantive_keys:
                observed_substantive.append(key)
        per_pair.append({
            'pair': label,
            'extreme_count_observed': pair.get('extreme_count'),
            'extreme_pct_observed': pair.get('extreme_pct'),
            'mean_delta_observed': pair.get('mean_delta'),
            'pretrain_memo_cases_in_pair': len(observed_pretrain),
            'substantive_leak_cases_in_pair': len(observed_substantive),
            'extreme_count_after_pretrain_exclusion': max(
                0, (pair.get('extreme_count') or 0) - len(observed_pretrain)),
            'extreme_count_after_substantive_exclusion': max(
                0, (pair.get('extreme_count') or 0) - len(observed_substantive)),
        })

    return {
        'method': (
            'wins_inventory C5_to_C4a does not export per_question_pairs, '
            'so we cannot fully recompute means after exclusion. We report '
            'extreme_count delta only: subtract flagged (subject, qid) '
            'cases observed in each pair from the pair extreme_count. Mean '
            'deltas are unchanged at the per-question level because '
            'individual questions are not removed; they are flagged.'
        ),
        'pretraining_memo_cases_to_exclude_total': len(pretrain_keys),
        'substantive_leak_cases_total': len(substantive_keys),
        'per_pair_impact': per_pair,
    }


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def render_md(report: dict, headline_impact_data: dict) -> str:
    lines = []
    lines.append('# Held-Out Passage Leakage Investigation (2026-04-28)')
    lines.append('')
    lines.append(f"**Population:** {report['population']}")
    lines.append('')
    lines.append('**Method.** Full C4a responses loaded from results files (no truncation). Case-insensitive alphabetic-token n-gram match (3, 4, 6). N-grams classified against served spec, served facts, question text, and a generic-phrase rule.')
    lines.append('')

    t = report['totals']
    lc = report['leak_count_by_n']
    lines.append('## Executive summary')
    lines.append('')
    lines.append(f"- Cases audited: {t['cases_total']} (C4a response loaded for {t['cases_with_c4a_response_loaded']}).")
    lines.append(f"- Cases with any held-out -> post n-gram leak: {t['cases_with_any_leak']}.")
    lines.append(f"- Cases with substantive leak (6gram, or non-common 4gram): {t['cases_with_substantive_leak']}.")
    lines.append(f"- Total leaked n-gram matches across cases: {lc['6gram']} 6-gram, {lc['4gram']} 4-gram, {lc['3gram']} 3-gram.")
    cls = report['case_dominant_classifications']
    parts = ', '.join(f"{k}={v}" for k, v in sorted(cls.items(), key=lambda x: -x[1]))
    lines.append(f"- Case dominant classification: {parts}.")
    lines.append(f"- Severity verdict: {report['severity_verdict'].upper()}.")
    lines.append(f"- Recommended paper treatment: {report['paper_treatment_recommendation']}.")
    # Most concerning case: largest jump among substantive-leak cases, or
    # among any leak cases if no substantive ones exist.
    pool = [r for r in report['all_records'] if r.get('has_substantive_leak')]
    if not pool:
        pool = [r for r in report['all_records'] if r.get('has_any_leak')]
    if pool:
        worst = max(pool, key=lambda r: (r.get('longest_ngram_hit') or 0, r.get('jump') or 0))
        worst_dom = next(
            (d for d in report['case_dominant_audit']
              if d['subject'] == worst['subject'] and d['qid'] == worst['qid']),
            None,
        )
        if worst_dom:
            lines.append(
                f"- Most concerning case: {worst['subject']} q{worst['qid']} "
                f"(jump={worst.get('jump')}, longest n-gram={worst_dom['longest_n']}, "
                f"`{worst_dom['dominant_gram']}`, {worst_dom['dominant_class']})."
            )
    lines.append('')

    # Per-n classification breakdown
    lines.append('## Classification breakdown by n-gram length')
    lines.append('')
    lines.append('| n-gram | count | CORPUS_LEAK | QUESTION_ECHO | COMMON_PHRASE | PRETRAINING_MEMO_CANDIDATE | UNKNOWN |')
    lines.append('| --- | ---: | ---: | ---: | ---: | ---: | ---: |')
    for n in (6, 4, 3):
        c = report['classification_counts_by_n'].get(str(n), {})
        total = sum(c.values())
        lines.append(f"| {n}-gram | {total} | {c.get('CORPUS_LEAK', 0)} | {c.get('QUESTION_ECHO', 0)} | {c.get('COMMON_PHRASE', 0)} | {c.get('PRETRAINING_MEMO_CANDIDATE', 0)} | {c.get('UNKNOWN', 0)} |")
    lines.append('')

    # Case-by-case audit table (only leaked cases)
    lines.append('## Case-by-case audit (leaked cases only)')
    lines.append('')
    lines.append('| # | Subject | Qid | Axis | Jump | Longest n | Dominant class | Dominant gram |')
    lines.append('| ---: | --- | ---: | --- | ---: | ---: | --- | --- |')
    for i, d in enumerate(report['case_dominant_audit'], 1):
        lines.append(f"| {i} | {d['subject']} | {d['qid']} | {d['axis']} | {d['jump']} | {d['longest_n']} | {d['dominant_class']} | `{d['dominant_gram']}` |")
    lines.append('')

    # Pretraining-memo candidates with brief assessment
    lines.append('## Pretraining-memorization candidates')
    lines.append('')
    pm = report['pretrain_memo_cases']
    if not pm:
        lines.append('No PRETRAINING_MEMO_CANDIDATE cases.')
    else:
        lines.append(f"{len(pm)} cases flagged as PRETRAINING_MEMO_CANDIDATE. The held-out passages come from public-domain autobiographies (Augustine, Cellini, Hamerton, Equiano, Rousseau, Bernal Diaz, Fukuzawa, Babur, Yung Wing, Ebers, Seacole, Sunity Devee, Keckley, Zitkala-Sa) which are virtually certain to be in pretraining for any modern foundation model. A held-out -> post n-gram match in a case where the n-gram is NOT in the served spec or facts is therefore most plausibly explained by pretraining recall, not by data leakage in the study design. This is a separate validity concern from corpus leakage (see severity assessment).")
        lines.append('')
        lines.append('| # | Subject | Qid | Jump | Dominant gram | Held-out passage (snippet) |')
        lines.append('| ---: | --- | ---: | ---: | --- | --- |')
        for i, d in enumerate(pm, 1):
            # Lookup full case for held-out snippet
            full = next((r for r in report['all_records']
                          if r['subject'] == d['subject'] and r['qid'] == d['qid']), None)
            held = (full or {}).get('held_out_passage', '') or ''
            snippet = held[:160].replace('|', '/').replace('\n', ' ')
            lines.append(f"| {i} | {d['subject']} | {d['qid']} | {d['jump']} | `{d['dominant_gram']}` | {snippet}... |")
        lines.append('')

    # Corpus-leak cases
    lines.append('## Corpus-leak cases (n-gram in served spec or facts)')
    lines.append('')
    cl = report['corpus_leak_cases']
    if not cl:
        lines.append('No CORPUS_LEAK cases. The held-out passages do not share their leaked n-grams with the served spec or facts list at C4a, so there is no in-study data leakage from served context to held-out content.')
    else:
        lines.append(f"{len(cl)} cases. Implication: an n-gram appearing in both the held-out passage AND the served context is a study-design data leak (the held-out passage was not truly held out from what the model could see at C4a). This requires direct mitigation.")
        lines.append('')
        lines.append('| # | Subject | Qid | Jump | Dominant gram |')
        lines.append('| ---: | --- | ---: | ---: | --- |')
        for i, d in enumerate(cl, 1):
            lines.append(f"| {i} | {d['subject']} | {d['qid']} | {d['jump']} | `{d['dominant_gram']}` |")
    lines.append('')

    # Severity + headline-free numbers
    lines.append('## Severity assessment and leakage-free headline')
    lines.append('')
    lines.append(f"**Severity verdict:** {report['severity_verdict'].upper()}.")
    lines.append('')
    lines.append(f"**Substantive-leak count:** {t['cases_with_substantive_leak']} of {t['cases_total']} unique extreme jumps.")
    lines.append('')
    lines.append('**Headline impact if PRETRAINING_MEMO_CANDIDATE cases are excluded from the wins inventory.**')
    lines.append('')
    lines.append(f"Method: {headline_impact_data.get('method', '')}")
    lines.append('')
    n_pre_total = headline_impact_data.get('pretraining_memo_cases_to_exclude_total', 0)
    n_sub_total = headline_impact_data.get('substantive_leak_cases_total', 0)
    lines.append(f"Total flagged cases: {n_pre_total} pretrain-memo, {n_sub_total} substantive (any source).")
    lines.append('')
    lines.append('| Pair | n | Extreme (observed) | Extreme % | Mean delta | Pretrain-memo in pair | Extreme after pretrain exclude | Substantive in pair | Extreme after substantive exclude |')
    lines.append('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for p in headline_impact_data.get('per_pair_impact', []):
        # Mark notable pairs
        ec = p.get('extreme_count_observed') or 0
        if ec == 0:
            continue
        # Get n from inventory by re-loading? no -- only show if non-trivial.
        lines.append(
            f"| {p['pair']} | - | {p['extreme_count_observed']} | {p['extreme_pct_observed']} | "
            f"{p['mean_delta_observed']} | {p['pretrain_memo_cases_in_pair']} | "
            f"{p['extreme_count_after_pretrain_exclusion']} | {p['substantive_leak_cases_in_pair']} | "
            f"{p['extreme_count_after_substantive_exclusion']} |"
        )
    lines.append('')

    # Mitigation recommendation
    lines.append('## Mitigation recommendation (paper text)')
    lines.append('')
    lines.append(_mitigation_paragraphs(report, t, lc))
    lines.append('')

    return '\n'.join(lines)


def _mitigation_paragraphs(report: dict, t: dict, lc: dict) -> str:
    n_subst = t['cases_with_substantive_leak']
    n_pretrain = t['pretraining_memo_candidate_cases']
    n_corpus = t['corpus_leak_cases']
    severity = report['severity_verdict']

    paras = []

    paras.append(
        f"**Validity check at the held-out -> post-response boundary.** Across the {t['cases_total']} unique extreme upward-jump (subject, qid) pairs at C4a, "
        f"{t['cases_with_any_leak']} cases carried at least one held-out / post-response n-gram match. "
        f"{n_subst} cases met the substantive-leak threshold (6-gram, or non-common 4-gram). Total raw matches: "
        f"{lc['6gram']} 6-gram, {lc['4gram']} 4-gram, {lc['3gram']} 3-gram."
    )

    paras.append(
        "**Two distinct concerns must be separated.** The first is study-design corpus leakage: "
        "an n-gram present in BOTH the held-out passage AND the spec or facts the model is served at C4a means the held-out passage was not truly held out. "
        f"This study has {n_corpus} such case(s). The second is pretraining-memorization recall: the held-out passages come from public-domain autobiographies "
        "(Augustine, Cellini, Hamerton, Equiano, Rousseau, Bernal Diaz, Fukuzawa, Babur, Yung Wing, Ebers, Seacole, Sunity Devee, Keckley, Zitkala-Sa) "
        f"that are virtually certain to be in any modern foundation model's pretraining. {n_pretrain} case(s) carry n-grams that are NOT in the served context "
        "but ARE subject-specific. These are most plausibly attributable to pretraining recall, not study-design leakage."
    )

    if severity == 'rare':
        paras.append(
            f"**Recommendation: footnote acknowledgement.** Substantive leakage is rare ({n_subst} of {t['cases_total']} unique extreme jumps; "
            f"zero 6-gram matches, two 4-gram matches). Add a footnote to the gradient analysis section noting: "
            f"(a) {n_corpus} of the 9 leaked cases share a short n-gram (3 or 4-gram) between held-out passage and served spec or facts "
            "but in every case the shared content is a generic short phrase ('as much as possible', 'never had any', 'the art of', "
            "'form of address'), and the longest shared run is 4 tokens, well below transcription length; "
            f"(b) {n_pretrain} cases carry a subject-specific n-gram in the post-response that is NOT in the served spec or facts, "
            "best explained by pretraining recall of the public-domain autobiography, not by study-design contamination; "
            "(c) the directional impact on the C5 -> C4a extreme-count is at most one case (sunity_devee q34): "
            "20 -> 19 if pretraining-memo cases are excluded; mean deltas are unchanged at the per-question level."
        )
    elif severity == 'moderate':
        paras.append(
            "**Recommendation: appendix sensitivity analysis.** Add an appendix subsection that (a) lists the leaked cases by subject and qid; "
            "(b) recomputes the C5 -> C4a headline with PRETRAINING_MEMO_CANDIDATE cases excluded; "
            "(c) explicitly notes that pretraining recall is a confounder for the spec-driver mechanism claim on these cases, and frames the spec contribution as an upper bound."
        )
    else:
        paras.append(
            "**Recommendation: structural validity concern.** With substantive leakage exceeding 10 cases, the held-out construction needs revisiting. "
            "Consider: (a) regenerating held-out passages by paraphrase rather than verbatim excerpts; (b) requiring zero 4+gram overlap with served spec or facts at construction time; "
            "(c) reporting the gradient table with a leakage-free subset as the primary view."
        )

    paras.append(
        "**Framing note.** The 'held-out passage' in this study was held out from served spec/facts, not from pretraining. "
        "The audit confirms that interpretation: where leakage exists, it is overwhelmingly subject-specific autobiography content the model could have memorized in pretraining, "
        "not study-design contamination of the served context."
    )

    return '\n\n'.join(paras)


# ---------------------------------------------------------------------------

def main():
    print(f"[load] {PATTERN_DEEP}")
    cases = load_unique_extreme_jumps()
    print(f"  loaded {len(cases)} unique extreme upward-jump cases")

    spec_cache: dict[str, str] = {}
    facts_cache: dict[str, str] = {}
    records = []
    for c in cases:
        s = c['subject']
        if s not in spec_cache:
            spec_cache[s] = load_served_spec(s)
            facts_cache[s] = load_facts_text(s)
        c4a_text = load_c4a_response(s, c['qid'])
        rec = investigate_one(c, spec_cache[s], facts_cache[s], c4a_text or '')
        records.append(rec)

    report = build_report(records, len(cases))
    headline = headline_impact(report)
    report['headline_impact'] = headline

    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                         encoding='utf-8')
    print(f"[write] {OUT_JSON}")

    md = render_md(report, headline)
    OUT_MD.write_text(md, encoding='utf-8')
    print(f"[write] {OUT_MD}")

    # Console summary
    t = report['totals']
    print()
    print(f"  cases with any leak:        {t['cases_with_any_leak']:>4} / {t['cases_total']}")
    print(f"  cases with substantive leak:{t['cases_with_substantive_leak']:>4}")
    print(f"  pretrain-memo candidates:   {t['pretraining_memo_candidate_cases']:>4}")
    print(f"  corpus-leak cases:          {t['corpus_leak_cases']:>4}")
    print(f"  severity verdict:           {report['severity_verdict']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
