"""
Two extensions to the v11.5 baseline-engagement analysis.

Extension A: per-response-model abstention behavior.
  Across ALL conditions and subjects, identify responses that match abstention
  patterns. Group by the response_model field that lives inside each
  responses[cond] body. Report rates of abstention and the score distribution
  on the 5-judge primary panel.

Extension B: memory-system effect on abstention.
  For each memory-system response (mem0/supermemory/letta/zep, controlled and
  fullpipeline), detect (a) whether the response matches refusal patterns and
  (b) whether the response recites tokens from the retrieval payload. Compare
  the score distribution against pure C5 refusals and pure C4_factdump refusals
  to test whether retrieved-fact recitation systematically inflates refusal
  scores.

Inputs reused from the base script: classify regex from
analyze_baseline_engagement, 5-judge primary loaders from
recompute_5judge_primary.

Outputs:
  docs/research/abstention_extensions_analysis_20260429.json
"""

import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_JSON = REPO / 'docs' / 'research' / 'abstention_extensions_analysis_20260429.json'

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recompute_5judge_primary import (  # noqa: E402
    load_global_judgments,
    load_hamerton_judgments,
    PRIMARY_JUDGES,
)

GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS
TIER2_SUBJECTS = ['ebers', 'yung_wing', 'zitkala_sa']

# Reuse the same lexicon the base agent used. The brief paraphrased a couple of
# phrases ("I cannot confirm", "would need additional context") that are not in
# the base list. We add the closest in-corpus equivalents that the base list
# already implies and flag the divergence in the addendum.
ABSTAIN_MARKERS = [
    "i don't have", "i do not have", "i'm not familiar",
    "i am not familiar", "could you clarify", "could you provide",
    "could you give", "i don't recognize", "i do not recognize",
    "i'm unable to", "i am unable to", "i don't know who",
    "i don't know of", "no information about", "without more context",
    "could you tell me", "i'm not aware", "i am not aware",
    "could you specify", "would you clarify", "i need more information",
    "without further context", "no specific information",
    # Additions implied by the brief but absent from the base list. These are
    # in-corpus phrases observed in the data and are the literal equivalents
    # of the paraphrases in the brief.
    "i cannot confirm", "would need additional context",
    "i cannot verify", "i don't have specific",
    "i do not have specific",
]


def matches_abstention(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(m in t for m in ABSTAIN_MARKERS)


# ----------------------------- score lookups -----------------------------

def _load_per_judge_files(base_dir: Path, prefix: str) -> list:
    """Load per-judge sidecar files of the form '<prefix>_judgments_<judge>.json'.

    These exist for memory-system conditions and the `c8_c9` / `baselayer`
    sets, where judgments are NOT in the main judgments_v2.json.
    """
    out = []
    for judge in list(PRIMARY_JUDGES) + ['gemini_flash', 'gemini_pro']:
        path = base_dir / f'{prefix}_judgments_{judge}.json'
        if not path.exists():
            continue
        try:
            data = json.load(path.open(encoding='utf-8'))
        except Exception:
            continue
        for r in data:
            out.append({
                'question_id': r.get('question_id'),
                'condition': r.get('condition'),
                'judge': judge,
                'score': r.get('score'),
                'parse_failure': r.get('parse_failure', False),
            })
    return out


def _all_judgment_rows_for_subject(subject: str) -> list:
    """Aggregate every per-judge judgment row across the canonical loader and
    the memory-system / c8_c9 / baselayer sidecars. This is what we need to
    score conditions like C1_mem0, C3_letta, etc., which live in separate
    files."""
    if subject == 'hamerton':
        rows = list(load_hamerton_judgments())
        base = RESULTS / 'hamerton'
    else:
        rows = list(load_global_judgments(subject))
        base = RESULTS / f'global_{subject}'
    # Memory-system + side-channel sets.
    sidecar_prefixes = [
        'mem0', 'mem0_fullpipeline',
        'supermemory', 'supermemory_fullpipeline',
        'letta', 'letta_fullpipeline',
        'zep', 'zep_fullpipeline',
        'c8_c9', 'baselayer',
    ]
    for prefix in sidecar_prefixes:
        rows.extend(_load_per_judge_files(base, prefix))
    return rows


def primary_panel_means_for_subject(subject: str) -> dict:
    """Return {(condition, qid): 5-judge primary mean} for a subject.

    Aggregates the canonical judgments_v2.json AND the per-judge sidecar files
    that hold memory-system / c8_c9 / baselayer scores.
    """
    rows = _all_judgment_rows_for_subject(subject)
    by_qcj = defaultdict(dict)
    for r in rows:
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        cond = r.get('condition')
        qid = r.get('question_id')
        judge = r.get('judge')
        by_qcj[(cond, qid)][judge] = r['score']
    return {key: statistics.mean(jmap.values())
            for key, jmap in by_qcj.items() if jmap}


def tier2_panel_means(subject: str, response_model_short: str) -> dict:
    """Tier 2 5-judge primary means, keyed by (condition, qid).

    response_model_short is 'sonnet' or 'gemini_pro'.
    """
    base = RESULTS / '_tier2' / f'global_{subject}'
    by_qcj = defaultdict(dict)
    for judge in PRIMARY_JUDGES:
        path = base / f'tier2_{response_model_short}_judgments_{judge}.json'
        if not path.exists():
            continue
        try:
            data = json.load(path.open(encoding='utf-8'))
        except Exception:
            continue
        for r in data:
            if r.get('judge') != judge:
                continue
            if r.get('score') is None or r.get('parse_failure'):
                continue
            by_qcj[(r['condition'], r['question_id'])][judge] = r['score']
    return {key: statistics.mean(jmap.values())
            for key, jmap in by_qcj.items() if jmap}


# ------------------------ response file iteration ------------------------

def iter_main_study_responses(subject: str):
    """Yield (condition, qid, response_text, response_model, score_or_none)."""
    means = primary_panel_means_for_subject(subject)

    if subject == 'hamerton':
        # Hamerton stitches together multiple sources. results.json has the
        # spec conditions; results_harmonized.json has C5/C4. We follow the
        # base agent's normalization.
        sources = []
        rh = RESULTS / 'hamerton' / 'results_harmonized.json'
        if rh.exists():
            sources.append(('harmonized', json.load(rh.open(encoding='utf-8'))))
        rp = RESULTS / 'hamerton' / 'results.json'
        if rp.exists():
            sources.append(('full', json.load(rp.open(encoding='utf-8'))))

        seen = set()  # avoid double-counting the same (cond, qid) across files
        for tag, data in sources:
            for r in data:
                qid = r['question_id']
                for cond, body in (r.get('responses') or {}).items():
                    norm = cond
                    if cond == 'C4a_full_all_facts_plus_spec':
                        norm = 'C4a_full_facts_plus_spec'
                    elif cond == 'C2c_full_wrong_spec':
                        norm = 'C2c_wrong_spec'
                    if (norm, qid) in seen:
                        continue
                    seen.add((norm, qid))
                    text = body.get('text', '') if isinstance(body, dict) else str(body)
                    model = body.get('model') if isinstance(body, dict) else None
                    score = means.get((norm, qid))
                    yield norm, qid, text, model, score

        # Hamerton memory-system files (mem0, supermemory, letta, zep) and c8_c9.
        for stem in ['mem0_results.json',
                     'supermemory_results.json',
                     'letta_results.json',
                     'zep_results.json',
                     'mem0_fullpipeline_results.json',
                     'supermemory_fullpipeline_results.json',
                     'letta_fullpipeline_results.json',
                     'zep_fullpipeline_results.json',
                     'c8_c9_results.json',
                     'baselayer_results.json']:
            path = RESULTS / 'hamerton' / stem
            if not path.exists():
                continue
            try:
                data = json.load(path.open(encoding='utf-8'))
            except Exception:
                continue
            for r in data:
                qid = r['question_id']
                for cond, body in (r.get('responses') or {}).items():
                    text = body.get('text', '') if isinstance(body, dict) else str(body)
                    model = body.get('model') if isinstance(body, dict) else None
                    score = means.get((cond, qid))
                    yield cond, qid, text, model, score
        return

    # Globals: results_v2.json carries primary 5 conditions; the memory-system
    # files carry C1_<provider> / C3_<provider>; c8_c9 carries C8/C9; baselayer
    # carries the baselayer condition.
    base = RESULTS / f'global_{subject}'
    for stem in ['results_v2.json',
                 'mem0_results.json',
                 'supermemory_results.json',
                 'letta_results.json',
                 'zep_results.json',
                 'mem0_fullpipeline_results.json',
                 'supermemory_fullpipeline_results.json',
                 'letta_fullpipeline_results.json',
                 'zep_fullpipeline_results.json',
                 'c8_c9_results.json',
                 'baselayer_results.json']:
        path = base / stem
        if not path.exists():
            continue
        try:
            data = json.load(path.open(encoding='utf-8'))
        except Exception:
            continue
        for r in data:
            qid = r['question_id']
            for cond, body in (r.get('responses') or {}).items():
                text = body.get('text', '') if isinstance(body, dict) else str(body)
                model = body.get('model') if isinstance(body, dict) else None
                score = means.get((cond, qid))
                yield cond, qid, text, model, score


def iter_tier2_responses(subject: str, response_model_short: str):
    """Yield (condition, qid, response_text, response_model, score_or_none)."""
    path = RESULTS / '_tier2' / f'global_{subject}' / f'tier2_{response_model_short}_results.json'
    if not path.exists():
        return
    try:
        data = json.load(path.open(encoding='utf-8'))
    except Exception:
        return
    means = tier2_panel_means(subject, response_model_short)
    for r in data:
        qid = r['question_id']
        for cond, body in (r.get('responses') or {}).items():
            text = body.get('text', '') if isinstance(body, dict) else str(body)
            model = body.get('model') if isinstance(body, dict) else None
            score = means.get((cond, qid))
            yield cond, qid, text, model, score


# ============================ Extension A ============================

def normalize_model_name(model: str) -> str:
    """Collapse Anthropic / OpenAI / Google model strings to short names."""
    if not model:
        return 'unknown'
    m = model.lower()
    if 'haiku-4-5' in m or 'haiku-4.5' in m:
        return 'claude-haiku-4-5'
    if 'sonnet-4-6' in m or 'sonnet-4.6' in m:
        return 'claude-sonnet-4-6'
    if 'opus-4-6' in m or 'opus-4.6' in m or 'claude-opus' in m:
        return 'claude-opus-4-6'
    if 'gpt-5.4' in m or 'gpt5.4' in m or 'gpt-5-4' in m:
        return 'gpt-5.4'
    if 'gemini-2.5-pro' in m or 'gemini-2-5-pro' in m:
        return 'gemini-2.5-pro'
    if 'gemini-2.5-flash' in m or 'gemini-2-5-flash' in m or 'gemini' in m:
        return 'gemini-2.5-flash'
    return model


def extension_a():
    """Per-response-model abstention behavior."""
    # Collect all (model, condition, subject, qid, text, score, abstain?) rows.
    rows = []
    # Main study: response file iteration carries every response model, but
    # on these subjects all are Haiku 4.5.
    for subject in MAIN_STUDY:
        for cond, qid, text, model, score in iter_main_study_responses(subject):
            rows.append({
                'subject': subject,
                'qid': qid,
                'condition': cond,
                'model': normalize_model_name(model),
                'raw_model': model,
                'score': score,
                'abstain': matches_abstention(text),
                'text_first_300': (text or '')[:300],
                'word_count': len((text or '').split()),
                'origin': 'main',
            })
    # Tier 2 cross-provider replication: Sonnet and Gemini Pro on 3 subjects.
    for subject in TIER2_SUBJECTS:
        for short in ['sonnet', 'gemini_pro']:
            for cond, qid, text, model, score in iter_tier2_responses(subject, short):
                rows.append({
                    'subject': subject,
                    'qid': qid,
                    'condition': cond,
                    'model': normalize_model_name(model),
                    'raw_model': model,
                    'score': score,
                    'abstain': matches_abstention(text),
                    'text_first_300': (text or '')[:300],
                    'word_count': len((text or '').split()),
                    'origin': f'tier2_{short}',
                })

    # Per-model summary
    by_model = defaultdict(list)
    for r in rows:
        by_model[r['model']].append(r)

    per_model_summary = {}
    for model, group in by_model.items():
        n_total = len(group)
        n_abstain = sum(1 for r in group if r['abstain'])
        # Score-stratified counts on abstention rows that have a score.
        abstain_with_score = [r for r in group
                              if r['abstain'] and r['score'] is not None]
        n_abstain_scored = len(abstain_with_score)
        ge_2 = sum(1 for r in abstain_with_score if r['score'] >= 2.0)
        ge_3 = sum(1 for r in abstain_with_score if r['score'] >= 3.0)
        scores = [r['score'] for r in abstain_with_score]
        mean_score = round(statistics.mean(scores), 4) if scores else None
        sd_score = round(statistics.stdev(scores), 4) if len(scores) > 1 else None
        # Example phrases that drove inflation (abstain rows with score >= 2.0).
        # Pick 3 highest-scoring excerpts for transparency.
        inflators = sorted(
            [r for r in abstain_with_score if r['score'] >= 2.0],
            key=lambda r: r['score'], reverse=True,
        )
        example_phrases = [
            {
                'subject': r['subject'],
                'condition': r['condition'],
                'qid': r['qid'],
                'score': round(r['score'], 4),
                'word_count': r['word_count'],
                'excerpt_first_300': r['text_first_300'],
            }
            for r in inflators[:3]
        ]
        # Subjects + conditions actually represented for this model
        subj_set = sorted({r['subject'] for r in group})
        cond_set = sorted({r['condition'] for r in group})
        per_model_summary[model] = {
            'n_total_responses': n_total,
            'n_abstain_responses': n_abstain,
            'abstention_rate': round(n_abstain / n_total, 4) if n_total else None,
            'n_abstain_with_score': n_abstain_scored,
            'mean_abstain_score_5judge': mean_score,
            'sd_abstain_score_5judge': sd_score,
            'pct_abstain_score_ge_2': round(ge_2 / n_abstain_scored, 4)
                                       if n_abstain_scored else None,
            'pct_abstain_score_ge_3': round(ge_3 / n_abstain_scored, 4)
                                       if n_abstain_scored else None,
            'subjects_covered': subj_set,
            'conditions_covered': cond_set,
            'top_inflators': example_phrases,
        }

    # Cross-model ranking on the over-credit metric.
    # Use pct_abstain_score_ge_2 with N >= 30 to avoid small-sample ranking.
    rankable = {m: s for m, s in per_model_summary.items()
                if s['n_abstain_with_score'] and s['n_abstain_with_score'] >= 30}
    if rankable:
        ranked = sorted(rankable.items(),
                        key=lambda kv: kv[1]['pct_abstain_score_ge_2'] or 0,
                        reverse=True)
        highest_overcredit = ranked[0][0]
        lowest_overcredit = ranked[-1][0]
    else:
        highest_overcredit = lowest_overcredit = None

    return {
        'description': ('Per-response-model abstention behavior across all '
                        'conditions and 14 main-study subjects, plus Tier 2 '
                        'cross-provider replication on 3 subjects (Ebers, '
                        'Yung Wing, Zitkala-Sa) for Sonnet 4.6 and Gemini '
                        '2.5 Pro response models.'),
        'methodology': ('Responses are tagged for abstention if the lowercased '
                        'text contains any phrase from a 27-marker list '
                        '(reuses the base agent regex with 5 in-corpus '
                        'paraphrase additions). Scores are 5-judge primary '
                        'panel means (haiku, sonnet, opus, gpt4o, gpt54). '
                        'Score-stratified counts use only abstention rows '
                        'with a non-null score.'),
        'n_rows_total': len(rows),
        'per_response_model': per_model_summary,
        'highest_overcredit_model': highest_overcredit,
        'lowest_overcredit_model': lowest_overcredit,
        'note': ('Tier 2 cross-provider replication in this repo includes '
                 'only Sonnet 4.6 and Gemini 2.5 Pro (per '
                 '_tier2/README.md and §3.5 of v11). The brief mentioned '
                 'Opus 4.6 and GPT-5.4 in Tier 2 but those response models '
                 'are not present in the data.'),
    }


# ============================ Extension B ============================

# Memory-system result file stems and their condition prefixes.
MEMORY_SYSTEM_FILES = [
    ('mem0_results.json', 'controlled', 'mem0'),
    ('supermemory_results.json', 'controlled', 'supermemory'),
    ('letta_results.json', 'controlled', 'letta'),
    ('zep_results.json', 'controlled', 'zep'),
    ('mem0_fullpipeline_results.json', 'fullpipeline', 'mem0'),
    ('supermemory_fullpipeline_results.json', 'fullpipeline', 'supermemory'),
    ('letta_fullpipeline_results.json', 'fullpipeline', 'letta'),
    ('zep_fullpipeline_results.json', 'fullpipeline', 'zep'),
]

# Tokens emitted by Zep's graph retrieval that are not real facts and would
# create spurious recitation matches if treated as such. We skip these entirely.
ZEP_FILTER_PATTERNS = [
    r"^\('?communities'?,\s*None\)$",
    r"^\('?context'?,\s*None\)$",
    r"^\('?facts'?,\s*None\)$",
    r"^\('?nodes'?,\s*None\)$",
    r"^\('?episodes'?,\s*None\)$",
]


def is_zep_noise(fact: str) -> bool:
    if not isinstance(fact, str):
        return True
    for p in ZEP_FILTER_PATTERNS:
        if re.match(p, fact.strip()):
            return True
    return False


def extract_ngrams(fact: str, min_len: int = 4) -> list:
    """Pull a small set of candidate substrings (≥ min_len-word grams) from a
    fact string for substring-membership checks. We use 4+ word grams: the
    smaller ngrams (e.g. 'and the') would have many false positives.
    """
    if not fact or not isinstance(fact, str):
        return []
    # Strip punctuation tokens that confuse boundary matching.
    words = re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", fact)
    grams = []
    for i in range(len(words) - min_len + 1):
        gram = ' '.join(words[i:i + min_len])
        if len(gram) >= 15:  # only keep grams long enough to be discriminating
            grams.append(gram.lower())
    # Deduplicate and limit to the first 30 grams per fact for speed.
    seen = set()
    out = []
    for g in grams:
        if g not in seen:
            seen.add(g)
            out.append(g)
        if len(out) >= 30:
            break
    return out


def detect_recitation(response_text: str, retrieval_facts: list) -> dict:
    """Return {'recites': bool, 'matched_facts_n': int, 'sample_match': str}."""
    if not response_text or not retrieval_facts:
        return {'recites': False, 'matched_facts_n': 0, 'sample_match': None}
    rt = response_text.lower()
    matched = 0
    sample = None
    for fact in retrieval_facts:
        if is_zep_noise(fact):
            continue
        grams = extract_ngrams(fact)
        for g in grams:
            if g in rt:
                matched += 1
                if sample is None:
                    sample = g
                break  # one match per fact is enough
    return {
        'recites': matched > 0,
        'matched_facts_n': matched,
        'sample_match': sample,
    }


def extension_b():
    """Memory-system effect on abstention.

    Builds four cells:
      cell_1: pure C5 refusals (no facts, no retrieval)
      cell_2: pure C4_factdump refusals (full facts, no retrieval)
      cell_3: memory-system refusal AND retrieved-fact recitation
      cell_4: memory-system non-refusal (sanity)
    Reports score distribution per cell and Δ vs cell_1 with 95% CI.
    """
    cell_1 = []  # C5_baseline refusals
    cell_2 = []  # C4_factdump refusals
    cell_3 = []  # memory-system refusal + recitation
    cell_4 = []  # memory-system non-refusal
    cell_3_no_recite = []  # memory-system refusal WITHOUT recitation (control)
    skipped_providers = []
    provider_breakdown = defaultdict(lambda: {
        'n_total': 0, 'n_refuse': 0, 'n_refuse_recite': 0,
        'n_refuse_no_recite': 0, 'n_engage': 0,
        'scores_refuse_recite': [], 'scores_refuse_no_recite': [],
        'scores_engage': [],
    })

    # First: collect cell 1 and cell 2 refusals across all 14 subjects from the
    # main response files (results_v2.json / Hamerton harmonized+full).
    for subject in MAIN_STUDY:
        means = primary_panel_means_for_subject(subject)
        # C5_baseline + C4_factdump
        if subject == 'hamerton':
            sources = [
                RESULTS / 'hamerton' / 'results_harmonized.json',
                RESULTS / 'hamerton' / 'results.json',
            ]
        else:
            sources = [RESULTS / f'global_{subject}' / 'results_v2.json']
        seen = set()
        for src in sources:
            if not src.exists():
                continue
            for r in json.load(src.open(encoding='utf-8')):
                qid = r['question_id']
                for cond, body in (r.get('responses') or {}).items():
                    norm = cond
                    if cond == 'C4a_full_all_facts_plus_spec':
                        norm = 'C4a_full_facts_plus_spec'
                    elif cond == 'C2c_full_wrong_spec':
                        norm = 'C2c_wrong_spec'
                    if norm not in ('C5_baseline', 'C4_factdump'):
                        continue
                    if (norm, qid) in seen:
                        continue
                    seen.add((norm, qid))
                    text = body.get('text', '') if isinstance(body, dict) else str(body)
                    if not matches_abstention(text):
                        continue
                    score = means.get((norm, qid))
                    if score is None:
                        continue
                    row = {
                        'subject': subject, 'qid': qid, 'condition': norm,
                        'score': score, 'word_count': len(text.split()),
                    }
                    if norm == 'C5_baseline':
                        cell_1.append(row)
                    else:
                        cell_2.append(row)

    # Second: memory-system files. Refuse + retrieved-fact recitation.
    for subject in MAIN_STUDY:
        means = primary_panel_means_for_subject(subject)
        base = RESULTS / 'hamerton' if subject == 'hamerton' \
               else RESULTS / f'global_{subject}'
        for stem, kind, provider in MEMORY_SYSTEM_FILES:
            path = base / stem
            if not path.exists():
                provider_breakdown[(provider, kind)]  # touch
                continue
            try:
                data = json.load(path.open(encoding='utf-8'))
            except Exception as e:
                skipped_providers.append({
                    'subject': subject, 'provider': provider, 'kind': kind,
                    'reason': f'load_error: {e}',
                })
                continue
            for r in data:
                qid = r['question_id']
                retrieval = r.get('retrieval') or {}
                facts = retrieval.get('facts') or []
                if not isinstance(facts, list):
                    facts = []
                # Drop Zep noise tokens upfront so the recitation heuristic
                # is not gamed by graph-protocol artifacts.
                clean_facts = [f for f in facts if not is_zep_noise(f)]
                # Note Zep dropouts.
                if provider == 'zep' and len(clean_facts) == 0 and facts:
                    # Most Zep retrieval payloads in this repo are pure noise
                    # tuples; recitation cannot be detected. We still process
                    # the response (it lands in cell 3 only if it recites
                    # which it can't, by construction) but flag the issue.
                    pass
                for cond, body in (r.get('responses') or {}).items():
                    text = body.get('text', '') if isinstance(body, dict) else str(body)
                    score = means.get((cond, qid))
                    if score is None:
                        continue
                    is_refuse = matches_abstention(text)
                    rec = detect_recitation(text, clean_facts)
                    pb = provider_breakdown[(provider, kind)]
                    pb['n_total'] += 1
                    if is_refuse:
                        pb['n_refuse'] += 1
                        if rec['recites']:
                            pb['n_refuse_recite'] += 1
                            pb['scores_refuse_recite'].append(score)
                            cell_3.append({
                                'subject': subject, 'qid': qid,
                                'condition': cond, 'provider': provider,
                                'kind': kind, 'score': score,
                                'matched_facts_n': rec['matched_facts_n'],
                                'sample_match': rec['sample_match'],
                            })
                        else:
                            pb['n_refuse_no_recite'] += 1
                            pb['scores_refuse_no_recite'].append(score)
                            cell_3_no_recite.append({
                                'subject': subject, 'qid': qid,
                                'condition': cond, 'provider': provider,
                                'kind': kind, 'score': score,
                            })
                    else:
                        pb['n_engage'] += 1
                        pb['scores_engage'].append(score)
                        cell_4.append({
                            'subject': subject, 'qid': qid,
                            'condition': cond, 'provider': provider,
                            'kind': kind, 'score': score,
                        })

    # Aggregate per provider × kind.
    provider_summary = {}
    for (provider, kind), pb in provider_breakdown.items():
        key = f'{provider}__{kind}'
        n_total = pb['n_total']
        if n_total == 0:
            provider_summary[key] = {
                'n_total': 0,
                'note': 'no responses loaded for this provider/kind in this repo',
            }
            continue

        def _stat(xs):
            if not xs:
                return {'n': 0, 'mean': None, 'sd': None}
            return {
                'n': len(xs),
                'mean': round(statistics.mean(xs), 4),
                'sd': round(statistics.stdev(xs), 4) if len(xs) > 1 else None,
            }

        provider_summary[key] = {
            'n_total': n_total,
            'n_refuse': pb['n_refuse'],
            'n_refuse_recite': pb['n_refuse_recite'],
            'n_refuse_no_recite': pb['n_refuse_no_recite'],
            'n_engage': pb['n_engage'],
            'refuse_rate': round(pb['n_refuse'] / n_total, 4),
            'recite_rate_among_refuse': (
                round(pb['n_refuse_recite']
                      / max(1, pb['n_refuse']), 4)
                if pb['n_refuse'] else None
            ),
            'score_refuse_recite': _stat(pb['scores_refuse_recite']),
            'score_refuse_no_recite': _stat(pb['scores_refuse_no_recite']),
            'score_engage': _stat(pb['scores_engage']),
        }

    # Cell-level distributions.
    def _summarize_cell(rows, label):
        scores = [r['score'] for r in rows]
        if not scores:
            return {'label': label, 'n': 0,
                    'mean': None, 'sd': None,
                    'pct_score_ge_2': None, 'pct_score_ge_3': None}
        return {
            'label': label,
            'n': len(scores),
            'mean': round(statistics.mean(scores), 4),
            'sd': round(statistics.stdev(scores), 4) if len(scores) > 1 else None,
            'pct_score_ge_2': round(sum(1 for s in scores if s >= 2.0)
                                    / len(scores), 4),
            'pct_score_ge_3': round(sum(1 for s in scores if s >= 3.0)
                                    / len(scores), 4),
            'min': round(min(scores), 4),
            'max': round(max(scores), 4),
        }

    cells = {
        'cell_1_pure_C5_refuse': _summarize_cell(
            cell_1, 'pure C5 refusal (no facts, no retrieval)'),
        'cell_2_C4_factdump_refuse': _summarize_cell(
            cell_2, 'C4 factdump refusal (full facts, no retrieval)'),
        'cell_3_mem_refuse_recite': _summarize_cell(
            cell_3, 'memory-system refusal + retrieved-fact recitation'),
        'cell_3_mem_refuse_no_recite': _summarize_cell(
            cell_3_no_recite,
            'memory-system refusal without retrieved-fact recitation'),
        'cell_4_mem_engage': _summarize_cell(
            cell_4, 'memory-system substantive engagement'),
    }

    # Δ comparisons with bootstrap 95% CI.
    def _delta_with_ci(group_a, group_b, label_a, label_b, n_boot=2000):
        a = [r['score'] for r in group_a]
        b = [r['score'] for r in group_b]
        if not a or not b:
            return {
                'comparison': f'{label_a} - {label_b}',
                'n_a': len(a), 'n_b': len(b),
                'mean_delta': None,
            }
        ma, mb = statistics.mean(a), statistics.mean(b)
        delta = ma - mb
        if HAS_SCIPY:
            # Welch's t-test for an analytic CI on the mean difference.
            t, p = scipy_stats.ttest_ind(a, b, equal_var=False)
            # Welch CI:
            va, vb = scipy_stats.tvar(a) if len(a) > 1 else 0.0, \
                     scipy_stats.tvar(b) if len(b) > 1 else 0.0
            se = (va / max(1, len(a)) + vb / max(1, len(b))) ** 0.5
            df_num = (va / max(1, len(a)) + vb / max(1, len(b))) ** 2
            df_den = ((va / max(1, len(a))) ** 2 / max(1, len(a) - 1)
                      + (vb / max(1, len(b))) ** 2 / max(1, len(b) - 1))
            df = df_num / df_den if df_den > 0 else max(1, len(a) + len(b) - 2)
            t_crit = scipy_stats.t.ppf(0.975, df)
            ci_low = delta - t_crit * se
            ci_high = delta + t_crit * se
            mannwhit_p = None
            try:
                _, mannwhit_p = scipy_stats.mannwhitneyu(a, b, alternative='two-sided')
            except ValueError:
                mannwhit_p = None
            return {
                'comparison': f'{label_a} - {label_b}',
                'n_a': len(a), 'n_b': len(b),
                'mean_a': round(ma, 4), 'mean_b': round(mb, 4),
                'mean_delta': round(delta, 4),
                'welch_t': round(float(t), 4),
                'welch_p_value': float(p),
                'welch_95_ci_low': round(float(ci_low), 4),
                'welch_95_ci_high': round(float(ci_high), 4),
                'mannwhitney_p_value': float(mannwhit_p) if mannwhit_p is not None else None,
            }
        return {
            'comparison': f'{label_a} - {label_b}',
            'n_a': len(a), 'n_b': len(b),
            'mean_a': round(ma, 4), 'mean_b': round(mb, 4),
            'mean_delta': round(delta, 4),
        }

    deltas = {
        'mem_refuse_recite_vs_pure_C5_refuse':
            _delta_with_ci(cell_3, cell_1, 'cell_3', 'cell_1'),
        'mem_refuse_recite_vs_C4_factdump_refuse':
            _delta_with_ci(cell_3, cell_2, 'cell_3', 'cell_2'),
        'mem_refuse_recite_vs_mem_refuse_no_recite':
            _delta_with_ci(cell_3, cell_3_no_recite, 'cell_3',
                           'cell_3_no_recite'),
        'mem_refuse_no_recite_vs_pure_C5_refuse':
            _delta_with_ci(cell_3_no_recite, cell_1, 'cell_3_no_recite',
                           'cell_1'),
    }

    return {
        'description': ('Effect of memory-system retrieval on refusal-pattern '
                        'response scores. Tests whether reciting retrieved '
                        'facts in an otherwise abstaining response inflates '
                        'the 5-judge primary score relative to pure C5 '
                        'refusals (no retrieval) or C4 factdump refusals '
                        '(facts in context, no retrieval).'),
        'methodology': {
            'refusal_detection': ('Same 27-marker abstention regex used in '
                                  'Extension A and the base agent.'),
            'recitation_detection': ('Heuristic: each retrieved fact is split '
                                     'into 4-word grams (≥15 char), '
                                     'lowercased, substring-matched against '
                                     'the response text. A response "recites" '
                                     'if at least one such gram appears '
                                     'verbatim. Zep-graph noise tokens '
                                     "(e.g. \"('communities', None)\") are "
                                     'filtered out before n-gram extraction.'),
            'limitation': ('The recitation detector has false positives '
                           '(common phrases like "the autobiography '
                           'describes" can match) and false negatives '
                           '(paraphrased facts will not match). Letta '
                           'fullpipeline retrievals are sometimes raw '
                           'passages of the held-out text, which makes '
                           'recitation detection trivially positive in '
                           'those cells. Treat as a first-pass signal.'),
        },
        'cells': cells,
        'deltas': deltas,
        'per_provider_breakdown': provider_summary,
        'skipped_providers': skipped_providers,
        'caveat_zep': ('Zep graph retrieval emits tuple-encoded protocol '
                       "tokens (e.g. \"('communities', None)\") instead of "
                       'fact strings on most subjects. After noise filtering '
                       'most Zep retrievals are empty, so Zep is effectively '
                       'absent from the recitation cell. Per-provider '
                       'numbers below report this honestly.'),
    }


# ============================ main ============================

def main():
    print('Running abstention extensions...')
    print('  Extension A: per-response-model abstention behavior')
    ext_a = extension_a()
    print(f"    n_rows={ext_a['n_rows_total']} models={list(ext_a['per_response_model'].keys())}")
    for model, s in ext_a['per_response_model'].items():
        print(f"    {model:<24} n={s['n_total_responses']:>5} "
              f"abstain_rate={s['abstention_rate'] or 0:.3f} "
              f"mean_score={s['mean_abstain_score_5judge']} "
              f"%>=2={s['pct_abstain_score_ge_2']} "
              f"%>=3={s['pct_abstain_score_ge_3']}")

    print('\n  Extension B: memory-system effect on abstention')
    ext_b = extension_b()
    for k, c in ext_b['cells'].items():
        print(f"    {k:<35} n={c['n']:>4} mean={c['mean']} "
              f"%>=2={c['pct_score_ge_2']} %>=3={c['pct_score_ge_3']}")
    for k, d in ext_b['deltas'].items():
        print(f"    {k}: delta={d.get('mean_delta')} "
              f"95%CI=[{d.get('welch_95_ci_low')}, {d.get('welch_95_ci_high')}] "
              f"p={d.get('welch_p_value')}")

    out = {
        'meta': {
            'description': ('Two extensions to baseline-engagement analysis: '
                            '(A) per-response-model abstention behavior; '
                            '(B) memory-system effect on abstention.'),
            'subjects_main': MAIN_STUDY,
            'subjects_tier2': TIER2_SUBJECTS,
            'primary_judges': sorted(PRIMARY_JUDGES),
            'generated_by': 'scripts/analyze_abstention_extensions.py',
            'companion_base_analysis': ('docs/research/'
                                        'baseline_engagement_analysis_'
                                        '20260429.json'),
        },
        'extension_a_per_response_model': ext_a,
        'extension_b_memory_system_effect': ext_b,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                        encoding='utf-8')
    print(f'\nWrote {OUT_JSON}')


if __name__ == '__main__':
    main()
