"""
Analyze C5 baseline engagement vs. abstention across 14 main-study subjects.

For each question (subject, qid) computes:
  - C5 baseline mean (5-judge primary panel: haiku, sonnet, opus, gpt4o, gpt54)
  - C4a (full facts + spec) mean on the same panel
  - Lift = C4a - C5
  - Bin: REFUSE / MARGINAL / GENERIC / ENGAGED / STRONG
  - Naming label: full / partial / none (does the question text name the subject?)
  - Disambiguator flag: place / profession / era keyword present?

Outputs:
  docs/research/baseline_engagement_analysis_20260429.json

Reuses the canonical 5-judge load functions from recompute_5judge_primary.py.
"""

import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# Reuse canonical loaders so numbers match the v10.1 / v11 5-judge primary table.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from recompute_5judge_primary import (
    load_global_judgments,
    load_hamerton_judgments,
    PRIMARY_JUDGES,
)

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
OUT_JSON = REPO / 'docs' / 'research' / 'baseline_engagement_analysis_20260429.json'

GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS

# Naming lexicon per subject.
# Each subject has the *full* canonical name plus first-only and last-only tokens.
# A question-text label is computed by checking which token classes are present:
#   FULL    -> question contains the multi-token full name
#   PARTIAL -> question contains only the first-name OR only the last-name
#   NONE    -> no naming token present
#
# Word-boundary matched, case-insensitive.
NAME_LEXICON = {
    'hamerton': {
        'full': ['Philip Hamerton', 'P. G. Hamerton', 'Philip Gilbert Hamerton'],
        'first': ['Philip'],
        'last': ['Hamerton'],
    },
    'sunity_devee': {
        'full': ['Sunity Devee', 'Maharani Sunity Devee'],
        'first': ['Sunity'],
        'last': ['Devee'],
    },
    'ebers': {
        'full': ['Georg Ebers', 'Georg Moritz Ebers'],
        'first': ['Georg'],
        'last': ['Ebers'],
    },
    'fukuzawa': {
        'full': ['Fukuzawa Yukichi', 'Yukichi Fukuzawa'],
        'first': ['Yukichi'],
        'last': ['Fukuzawa'],
    },
    'seacole': {
        'full': ['Mary Seacole', 'Mrs. Seacole', 'Mrs Seacole'],
        'first': ['Mary'],
        'last': ['Seacole'],
    },
    'bernal_diaz': {
        'full': ['Bernal Diaz', 'Bernal Díaz', 'Bernal Diaz del Castillo', 'Bernal Díaz del Castillo'],
        'first': ['Bernal'],
        'last': ['Diaz', 'Díaz', 'del Castillo'],
    },
    'keckley': {
        'full': ['Elizabeth Keckley', 'Elizabeth Keckly'],
        'first': ['Elizabeth'],
        'last': ['Keckley', 'Keckly'],
    },
    'yung_wing': {
        # Chinese name order: Yung is the surname.
        'full': ['Yung Wing'],
        'first': ['Wing'],
        'last': ['Yung'],
    },
    'babur': {
        # Single-token canonical name; treat any mention of "Babur" as FULL.
        'full': ['Babur', 'Zahir-ud-din Muhammad Babur', 'Zahiruddin Babur'],
        'first': [],
        'last': [],
    },
    'cellini': {
        'full': ['Benvenuto Cellini'],
        'first': ['Benvenuto'],
        'last': ['Cellini'],
    },
    'zitkala_sa': {
        'full': ['Zitkala-Sa', 'Zitkala-Ša', 'Zitkala Sa', 'Gertrude Bonnin'],
        'first': ['Gertrude'],
        'last': ['Bonnin'],
    },
    'rousseau': {
        'full': ['Jean-Jacques Rousseau', 'Jean Jacques Rousseau'],
        'first': ['Jean-Jacques', 'Jean Jacques'],
        'last': ['Rousseau'],
    },
    'augustine': {
        # Single-token canonical name.
        'full': ['Augustine of Hippo', 'Saint Augustine', 'St. Augustine', 'Augustine'],
        'first': [],
        'last': [],
    },
    'equiano': {
        'full': ['Olaudah Equiano', 'Gustavus Vassa'],
        'first': ['Olaudah', 'Gustavus'],
        'last': ['Equiano', 'Vassa'],
    },
}

# Disambiguator keywords per subject. These are place, profession, era, or work tokens
# that uniquely or near-uniquely fix the referent of an underspecified name.
DISAMBIGUATORS = {
    'hamerton': ['Victorian', 'painter', 'etching', 'Burnley', 'France', 'Innominato', 'Saone'],
    'sunity_devee': ['Maharani', 'Cooch Behar', 'India', 'Bengal', 'royal', 'palace', 'zenana'],
    'ebers': ['Egyptologist', 'Egypt', 'novelist', 'Munich', 'Leipzig', 'papyrus', 'archaeology'],
    'fukuzawa': ['Meiji', 'Japan', 'Keio', 'samurai', 'Tokyo', 'Edo', 'Nakatsu', 'Western learning'],
    'seacole': ['Crimea', 'Crimean', 'Balaclava', 'Jamaica', 'British Hotel', 'Sebastopol', 'nurse'],
    'bernal_diaz': ['conquistador', 'Cortes', 'Cortés', 'Mexico', 'Tenochtitlan', 'Aztec', 'Spanish'],
    'keckley': ['Lincoln', 'Mary Todd', 'White House', 'modiste', 'dressmaker', 'enslaved', 'St. Louis'],
    'yung_wing': ['Yale', 'Chinese', 'Educational Mission', 'Hartford', 'China', 'Macao', 'Morrison'],
    'babur': ['Mughal', 'Hindustan', 'Samarkand', 'Kabul', 'Fergana', 'Timurid', 'emperor'],
    'cellini': ['Florence', 'goldsmith', 'sculptor', 'Pope', 'Rome', 'Renaissance', 'Medici', 'Perseus'],
    'zitkala_sa': ['Yankton', 'Sioux', 'Dakota', 'boarding school', 'Native', 'reservation', 'White Cloud'],
    'rousseau': ['Geneva', 'philosopher', 'Confessions', 'Madame de Warens', 'Switzerland', 'Enlightenment', 'Emile'],
    'augustine': ['Hippo', 'Confessions', 'Carthage', 'Manichaean', 'bishop', 'Christian', 'Monica', 'Roman Africa'],
    'equiano': ['Igbo', 'African', 'enslaved', 'Middle Passage', 'abolition', 'slave trade', 'Vassa'],
}


def label_naming(question_text: str, lex: dict) -> str:
    """Return 'full', 'partial', or 'none' based on which name tokens occur."""
    qt = question_text or ''
    # Check FULL first: any of the multi-token full-name variants.
    for tok in lex.get('full', []):
        # Multi-token => match as substring with word boundaries on outer ends.
        pattern = r'(?<![A-Za-z])' + re.escape(tok) + r'(?![A-Za-z])'
        if re.search(pattern, qt, re.IGNORECASE):
            return 'full'
    # Check first-only or last-only
    for tok in lex.get('first', []) + lex.get('last', []):
        pattern = r'(?<![A-Za-z])' + re.escape(tok) + r'(?![A-Za-z])'
        if re.search(pattern, qt, re.IGNORECASE):
            return 'partial'
    return 'none'


def has_disambiguator(question_text: str, keywords: list) -> bool:
    qt = question_text or ''
    for kw in keywords:
        pattern = r'(?<![A-Za-z])' + re.escape(kw) + r'(?![A-Za-z])'
        if re.search(pattern, qt, re.IGNORECASE):
            return True
    return False


def load_subject_responses(subject: str) -> dict:
    """Return {qid: {condition: response_text}} for the subject."""
    out = {}
    if subject == 'hamerton':
        # Hamerton C5 lives in results_harmonized.json (39 prediction-tier qids).
        rh = RESULTS / 'hamerton' / 'results_harmonized.json'
        if rh.exists():
            for r in json.load(rh.open(encoding='utf-8')):
                qid = r['question_id']
                out.setdefault(qid, {})['question_text'] = r.get('question_text')
                for cond, body in (r.get('responses') or {}).items():
                    if isinstance(body, dict):
                        out[qid][cond] = body.get('text', '')
                    else:
                        out[qid][cond] = str(body)
        # Hamerton C4a lives in results.json (80 qids; 39 of them overlap rh).
        rp = RESULTS / 'hamerton' / 'results.json'
        if rp.exists():
            for r in json.load(rp.open(encoding='utf-8')):
                qid = r['question_id']
                if qid not in out:
                    continue
                # Overlay C4a (and other spec conditions) under normalized name.
                for cond, body in (r.get('responses') or {}).items():
                    norm = cond
                    if cond == 'C4a_full_all_facts_plus_spec':
                        norm = 'C4a_full_facts_plus_spec'
                    elif cond == 'C2c_full_wrong_spec':
                        norm = 'C2c_wrong_spec'
                    if isinstance(body, dict):
                        out[qid][norm] = body.get('text', '')
                    else:
                        out[qid][norm] = str(body)
        return out
    # Globals: results_v2.json carries every condition's response text.
    rv2 = RESULTS / f'global_{subject}' / 'results_v2.json'
    if rv2.exists():
        for r in json.load(rv2.open(encoding='utf-8')):
            qid = r['question_id']
            out.setdefault(qid, {})['question_text'] = r.get('question_text')
            out[qid]['held_out_passage'] = r.get('held_out_passage')
            for cond, body in (r.get('responses') or {}).items():
                if isinstance(body, dict):
                    out[qid][cond] = body.get('text', '')
                else:
                    out[qid][cond] = str(body)
    return out


def per_question_means(rows, condition: str) -> dict:
    """Return {qid: 5-judge primary mean} for the given condition.

    Mean is computed as: per-question, take all 5 primary judges' scores
    (one each), average. If a judge is missing or parse-failed, drop that judge
    for that question only.
    """
    by_qid_judge = defaultdict(dict)
    for r in rows:
        if r.get('condition') != condition:
            continue
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        # Last-write-wins if there are duplicate (qid, judge) pairs.
        by_qid_judge[r['question_id']][r['judge']] = r['score']
    out = {}
    for qid, jmap in by_qid_judge.items():
        if jmap:
            out[qid] = statistics.mean(jmap.values())
    return out


def per_question_judge_count(rows, condition: str) -> dict:
    """Return {qid: number of primary judges contributing} for transparency."""
    by_qid_judge = defaultdict(set)
    for r in rows:
        if r.get('condition') != condition:
            continue
        if r.get('judge') not in PRIMARY_JUDGES:
            continue
        if r.get('score') is None or r.get('parse_failure'):
            continue
        by_qid_judge[r['question_id']].add(r['judge'])
    return {qid: len(s) for qid, s in by_qid_judge.items()}


def bin_score(c5: float) -> str:
    # c5 is mean of up to 5 integer scores in {1..5}, divided by 5.
    # All such means are exactly representable in IEEE 754 (denominators of 5),
    # so direct == comparison against 1.0 is safe and identifies the "all five
    # judges scored 1" case without float-tolerance issues.
    if c5 == 1.00:
        return 'REFUSE'
    if c5 < 2.0:
        return 'MARGINAL'
    if c5 < 3.0:
        return 'GENERIC'
    if c5 < 4.0:
        return 'ENGAGED'
    return 'STRONG'


def classify_response_text(text: str) -> str:
    """Heuristic split for REFUSE-bin C5 responses.

    Categories:
      - 'abstain': honest "I don't have information" / clarification-seeking
      - 'wrong_confident': substantive prediction with no abstention markers
      - 'hedge': mixed -- includes hedges but also makes substantive claims
    """
    if not text:
        return 'abstain'
    t = text.lower()
    # Strong abstention markers.
    abstain_markers = [
        "i don't have", "i do not have", "i'm not familiar",
        "i am not familiar", "could you clarify", "could you provide",
        "could you give", "i don't recognize", "i do not recognize",
        "i'm unable to", "i am unable to", "i don't know who",
        "i don't know of", "no information about", "without more context",
        "could you tell me", "i'm not aware", "i am not aware",
        "could you specify", "would you clarify", "i need more information",
        "without further context", "no specific information",
    ]
    has_abstain = any(m in t for m in abstain_markers)
    # Length heuristic: short answers that include abstention => clean abstain.
    word_count = len(text.split())
    # Strong substantive markers (uses the subject's name + makes claims).
    # If response is long and does not include any abstention marker, treat as wrong_confident.
    if has_abstain and word_count < 200:
        return 'abstain'
    if has_abstain and word_count >= 200:
        return 'hedge'
    if not has_abstain and word_count >= 80:
        return 'wrong_confident'
    return 'hedge'


def main():
    print('Loading judgments and responses for 14 main-study subjects...')

    per_question_rows = []
    per_subject_summary = {}

    for subject in MAIN_STUDY:
        if subject == 'hamerton':
            rows = load_hamerton_judgments()
        else:
            rows = load_global_judgments(subject)

        c5 = per_question_means(rows, 'C5_baseline')
        c4a = per_question_means(rows, 'C4a_full_facts_plus_spec')
        c5_judge_n = per_question_judge_count(rows, 'C5_baseline')

        responses = load_subject_responses(subject)
        lex = NAME_LEXICON.get(subject, {})
        disambs = DISAMBIGUATORS.get(subject, [])

        # Build per-question rows. We require both C5 and C4a present.
        bin_counts = defaultdict(int)
        for qid in sorted(set(c5) & set(c4a)):
            qt = (responses.get(qid, {}) or {}).get('question_text') or ''
            c5_text = (responses.get(qid, {}) or {}).get('C5_baseline') or ''
            naming = label_naming(qt, lex)
            disamb = has_disambiguator(qt, disambs)
            c5_mean = c5[qid]
            c4a_mean = c4a[qid]
            lift = c4a_mean - c5_mean
            bin_label = bin_score(c5_mean)
            bin_counts[bin_label] += 1

            row = {
                'subject': subject,
                'question_id': qid,
                'question_text': qt,
                'c5_mean': round(c5_mean, 4),
                'c4a_mean': round(c4a_mean, 4),
                'lift': round(lift, 4),
                'bin': bin_label,
                'naming': naming,
                'has_disambiguator': disamb,
                'c5_judge_count': c5_judge_n.get(qid, 0),
                'c5_response_first_500': (c5_text or '')[:500],
                'c5_response_word_count': len((c5_text or '').split()),
                'c5_response_classification': classify_response_text(c5_text)
                                              if bin_label == 'REFUSE' else None,
            }
            per_question_rows.append(row)

        c5_means = [c5[qid] for qid in sorted(set(c5) & set(c4a))]
        per_subject_summary[subject] = {
            'n_questions': len(c5_means),
            'c5_overall_mean': round(statistics.mean(c5_means), 4) if c5_means else None,
            'bin_distribution': dict(bin_counts),
        }

    # ----- Aggregates -----
    overall_bins = defaultdict(int)
    for r in per_question_rows:
        overall_bins[r['bin']] += 1
    n_total = len(per_question_rows)

    # Naming x bin cross-tab
    naming_bin = defaultdict(lambda: defaultdict(int))
    for r in per_question_rows:
        naming_bin[r['naming']][r['bin']] += 1
    # Convert to plain dicts for JSON.
    naming_bin_out = {n: dict(b) for n, b in naming_bin.items()}

    # Disambiguator x bin cross-tab
    disamb_bin = defaultdict(lambda: defaultdict(int))
    for r in per_question_rows:
        disamb_bin[str(r['has_disambiguator'])][r['bin']] += 1
    disamb_bin_out = {d: dict(b) for d, b in disamb_bin.items()}

    # Engagement rate (C5 mean >= 2.0) by naming and disambiguator.
    def engaged_rate(predicate):
        sub = [r for r in per_question_rows if predicate(r)]
        if not sub:
            return None
        return round(sum(1 for r in sub if r['c5_mean'] >= 2.0) / len(sub), 4)

    engagement_by_naming = {
        n: {
            'n': sum(1 for r in per_question_rows if r['naming'] == n),
            'engaged_rate_c5_ge_2': engaged_rate(lambda r, n=n: r['naming'] == n),
            'engaged_rate_c5_ge_3': round(
                sum(1 for r in per_question_rows
                    if r['naming'] == n and r['c5_mean'] >= 3.0)
                / max(1, sum(1 for r in per_question_rows if r['naming'] == n)),
                4),
            'mean_c5': round(statistics.mean(
                [r['c5_mean'] for r in per_question_rows if r['naming'] == n]), 4)
                if any(r['naming'] == n for r in per_question_rows) else None,
        }
        for n in ['full', 'partial', 'none']
    }

    engagement_by_disamb = {
        d: {
            'n': sum(1 for r in per_question_rows if str(r['has_disambiguator']) == d),
            'engaged_rate_c5_ge_2': engaged_rate(lambda r, d=d: str(r['has_disambiguator']) == d),
            'engaged_rate_c5_ge_3': round(
                sum(1 for r in per_question_rows
                    if str(r['has_disambiguator']) == d and r['c5_mean'] >= 3.0)
                / max(1, sum(1 for r in per_question_rows if str(r['has_disambiguator']) == d)),
                4),
            'mean_c5': round(statistics.mean(
                [r['c5_mean'] for r in per_question_rows if str(r['has_disambiguator']) == d]), 4)
                if any(str(r['has_disambiguator']) == d for r in per_question_rows) else None,
        }
        for d in ['True', 'False']
    }

    # Naming + disambiguator joint cell breakdown
    joint = defaultdict(lambda: {'n': 0, 'mean_c5': 0.0, 'mean_lift': 0.0,
                                  'engaged_n': 0})
    for r in per_question_rows:
        key = f"{r['naming']}__{'disamb' if r['has_disambiguator'] else 'no_disamb'}"
        joint[key]['n'] += 1
        joint[key]['mean_c5'] += r['c5_mean']
        joint[key]['mean_lift'] += r['lift']
        if r['c5_mean'] >= 2.0:
            joint[key]['engaged_n'] += 1
    for key, v in joint.items():
        n = v['n']
        v['mean_c5'] = round(v['mean_c5'] / n, 4) if n else None
        v['mean_lift'] = round(v['mean_lift'] / n, 4) if n else None
        v['engaged_rate_c5_ge_2'] = round(v['engaged_n'] / n, 4) if n else None

    # Lift comparison by bin
    lift_by_bin = defaultdict(list)
    for r in per_question_rows:
        lift_by_bin[r['bin']].append(r['lift'])
    lift_by_bin_summary = {}
    for b, vs in lift_by_bin.items():
        lift_by_bin_summary[b] = {
            'n': len(vs),
            'mean_lift': round(statistics.mean(vs), 4) if vs else None,
            'sd_lift': round(statistics.stdev(vs), 4) if len(vs) > 1 else None,
            'pct_positive': round(sum(1 for v in vs if v > 0) / len(vs), 4)
                            if vs else None,
        }

    # Spearman ρ between C5 and lift, pooled and per subject.
    pooled_c5 = [r['c5_mean'] for r in per_question_rows]
    pooled_lift = [r['lift'] for r in per_question_rows]
    spearman = {}
    if HAS_SCIPY and len(pooled_c5) >= 5:
        rho, p = scipy_stats.spearmanr(pooled_c5, pooled_lift)
        spearman['pooled'] = {'rho': round(float(rho), 4),
                              'p_value': float(p),
                              'n': len(pooled_c5)}
        per_subj_rho = {}
        for subject in MAIN_STUDY:
            sc5 = [r['c5_mean'] for r in per_question_rows if r['subject'] == subject]
            sl = [r['lift'] for r in per_question_rows if r['subject'] == subject]
            if len(sc5) >= 5:
                rho_s, p_s = scipy_stats.spearmanr(sc5, sl)
                per_subj_rho[subject] = {'rho': round(float(rho_s), 4),
                                         'p_value': float(p_s),
                                         'n': len(sc5)}
        spearman['per_subject'] = per_subj_rho

    # Mann-Whitney U: lift in REFUSE bin vs ENGAGED bin
    refuse_lift = lift_by_bin.get('REFUSE', [])
    engaged_lift = lift_by_bin.get('ENGAGED', []) + lift_by_bin.get('STRONG', [])
    refuse_vs_engaged = {}
    if HAS_SCIPY and refuse_lift and engaged_lift:
        u, p = scipy_stats.mannwhitneyu(refuse_lift, engaged_lift,
                                        alternative='two-sided')
        refuse_vs_engaged = {
            'n_refuse': len(refuse_lift),
            'n_engaged_or_strong': len(engaged_lift),
            'mean_lift_refuse': round(statistics.mean(refuse_lift), 4),
            'mean_lift_engaged_or_strong': round(statistics.mean(engaged_lift), 4),
            'mannwhitney_U': float(u),
            'p_value': float(p),
        }

    # Manual inspection: REFUSE-bin classification distribution
    refuse_class = defaultdict(int)
    for r in per_question_rows:
        if r['bin'] == 'REFUSE':
            cls = r.get('c5_response_classification') or 'unknown'
            refuse_class[cls] += 1

    aggregates = {
        'n_questions_total': n_total,
        'overall_bin_distribution': dict(overall_bins),
        'overall_bin_distribution_pct': {b: round(c / n_total, 4)
                                          for b, c in overall_bins.items()},
        'lift_by_bin': lift_by_bin_summary,
        'spearman_rho_c5_vs_lift': spearman,
        'refuse_vs_engaged_lift': refuse_vs_engaged,
        'naming_x_bin': naming_bin_out,
        'disambiguator_x_bin': disamb_bin_out,
        'engagement_by_naming': engagement_by_naming,
        'engagement_by_disambiguator': engagement_by_disamb,
        'naming_disambiguator_joint': dict(joint),
        'refuse_response_classification': dict(refuse_class),
    }

    out = {
        'meta': {
            'description': 'C5 baseline engagement vs. abstention analysis. '
                           'Per-question 5-judge primary panel '
                           '(haiku/sonnet/opus/gpt4o/gpt54). '
                           'Bin definitions: REFUSE c5==1.00, MARGINAL 1<c5<2, '
                           'GENERIC 2<=c5<3, ENGAGED 3<=c5<4, STRONG c5>=4.',
            'subjects': MAIN_STUDY,
            'primary_judges': sorted(PRIMARY_JUDGES),
            'generated_by': 'scripts/analyze_baseline_engagement.py',
        },
        'per_subject_summary': per_subject_summary,
        'aggregates': aggregates,
        'per_question': per_question_rows,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                        encoding='utf-8')

    # Console summary
    print(f'\nWrote {OUT_JSON} ({len(per_question_rows)} question rows).\n')
    print('Overall bin distribution:')
    for b in ['REFUSE', 'MARGINAL', 'GENERIC', 'ENGAGED', 'STRONG']:
        print(f"  {b:<10}: {overall_bins.get(b, 0):3d} "
              f"({overall_bins.get(b, 0) / max(1, n_total) * 100:5.1f}%)")
    print('\nLift by bin (mean +- sd, % positive):')
    for b in ['REFUSE', 'MARGINAL', 'GENERIC', 'ENGAGED', 'STRONG']:
        s = lift_by_bin_summary.get(b)
        if s:
            print(f"  {b:<10}: n={s['n']:3d} mean={s['mean_lift']:+.3f} "
                  f"sd={s['sd_lift'] if s['sd_lift'] is not None else 'NA'} "
                  f"pos={s['pct_positive']:.2%}")
    print('\nSpearman pooled:', spearman.get('pooled'))
    print('Refuse vs engaged Mann-Whitney:', refuse_vs_engaged)
    print('\nNaming x bin (counts):')
    for n, b in naming_bin_out.items():
        print(f'  {n}: {b}')
    print('\nEngagement (% with C5 >= 2.0) by naming:')
    for n, info in engagement_by_naming.items():
        print(f"  {n}: n={info['n']} mean_c5={info['mean_c5']} "
              f"engaged_rate={info['engaged_rate_c5_ge_2']}")
    print('\nRefuse-bin response classification:', dict(refuse_class))


if __name__ == '__main__':
    main()
