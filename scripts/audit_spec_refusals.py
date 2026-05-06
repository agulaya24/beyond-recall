"""
audit_spec_refusals.py
======================

P0-5 — Spec-induced refusal audit across 5 memory-system substrates.

PURPOSE
-------
For every C3-refusal-that-was-not-a-C1-refusal on the low-baseline slice,
classify the refusal into one of four categories:

    (a) EPISTEMIC_HONEST      Retrieved facts are genuinely insufficient;
                              the spec correctly flagged that the model
                              cannot answer.
    (b) SPEC_AXIOM_TRIGGER    The retrieval was actually sufficient, but
                              the spec's honesty/dignity axioms caused a
                              refusal (e.g. refusing to speculate about a
                              deceased person).
    (c) RUBRIC_ARTIFACT       The refusal is epistemically honest AND the
                              judges scored it at the floor (mean <= 1.5),
                              so a good-behavior refusal is lumped in with
                              the wrong-answer bucket.
    (d) SCORED_AS_WRONG_PRED  The judges scored the refusal above 1.5 —
                              refusal still counted as a non-useful
                              prediction, but not at the 1-anchor floor.

INPUT
-----
For each (subject, system) pair on the low-baseline slice:
    results/{global_<subject>|hamerton}/{system}_fullpipeline_results.json
    or {system}_results.json for substrates without an FP variant.

  Low-baseline subjects (9): ebers, sunity_devee, fukuzawa, bernal_diaz,
                             babur, seacole, keckley, yung_wing, hamerton.
  Systems (5): mem0, letta, supermemory, zep, baselayer.

DEFINITION OF SPEC-INDUCED REFUSAL
----------------------------------
Broad rule: the C3 response matches any REFUSAL_PATTERNS anywhere in the
text AND the paired C1 response does not. (Starts-refusal on its own
only produces 6 refusals across all 45 cells — too few to diagnose.)

REFUSAL_PATTERNS is the canonical REFUSAL_RE block from
scripts/classify_hedging.py, used elsewhere in the paper analysis
pipeline. The broad rule is more inclusive, which is appropriate here:
we want to catch mid-response refusals (e.g. "The retrieved facts don't
contain ...") not just verbatim-opening refusals.

CLASSIFIER
----------
Claude Haiku 4.5 is asked to choose among the 4 categories given:
  - question text
  - held-out ground truth
  - the 10 retrieved facts (from C3)
  - the full C3 response (the refusal)
  - the mean score judges assigned to the C3 response

Temperature 0. Single-token category response.

OUTPUT
------
docs/research/spec_refusal_audit.json — raw per-case classifications.
docs/research/spec_refusal_audit.md   — summary report.

BUDGET
------
Inventory (see scripts/_p0b_inventory.py):
    Total broad spec-induced refusals: 81
    Total narrow: 6
    Hard cap: 300
All 81 are classified. Haiku @ ~$0.003/call = ~$0.25 total.

USAGE
-----
    python scripts/audit_spec_refusals.py
"""

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DATA = REPO / 'data'
OUT_JSON = REPO / 'docs' / 'research' / 'spec_refusal_audit.json'
OUT_MD = REPO / 'docs' / 'research' / 'spec_refusal_audit.md'

LOW_BASELINE_SUBJECTS = [
    'ebers', 'sunity_devee', 'fukuzawa', 'bernal_diaz', 'babur',
    'seacole', 'keckley', 'yung_wing', 'hamerton',
]
SYSTEMS = ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']

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

JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']


def load_env():
    """Pull keys from Windows user env into os.environ."""
    for k in ['ANTHROPIC_API_KEY']:
        if os.environ.get(k):
            continue
        r = subprocess.run(
            ['powershell', '-Command',
             f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
            capture_output=True, text=True
        )
        val = r.stdout.strip()
        if val:
            os.environ[k] = val


def subject_dir(subject):
    if subject == 'hamerton':
        return RESULTS / 'hamerton'
    return RESULTS / f'global_{subject}'


def load_results(subject, system):
    sdir = subject_dir(subject)
    if system == 'baselayer':
        p = sdir / 'baselayer_results.json'
        if not p.exists():
            return None, None, None
        return json.load(p.open(encoding='utf-8')), 'C1_baselayer', 'C3_baselayer'
    fp = sdir / f'{system}_fullpipeline_results.json'
    if fp.exists():
        return json.load(fp.open(encoding='utf-8')), f'C1_{system}_fp', f'C3_{system}_fp'
    alt = sdir / f'{system}_results.json'
    if alt.exists():
        return json.load(alt.open(encoding='utf-8')), f'C1_{system}', f'C3_{system}'
    return None, None, None


def load_merged_judgments(subject, system):
    """Return {(qid, condition): mean_score_over_5_judges}."""
    sdir = subject_dir(subject)
    # Determine which merged file to read
    if system == 'baselayer':
        merged_path = sdir / 'baselayer_judgments_merged.json'
    else:
        fp = sdir / f'{system}_fullpipeline_judgments_merged.json'
        alt = sdir / f'{system}_judgments_merged.json'
        merged_path = fp if fp.exists() else alt
    if not merged_path or not merged_path.exists():
        return {}
    data = json.load(merged_path.open(encoding='utf-8'))
    bucket = defaultdict(list)
    for row in data:
        judge = row.get('judge')
        if judge not in JUDGES:
            continue
        score = row.get('score')
        if not isinstance(score, int) or score < 1 or score > 5:
            continue
        qid = row.get('question_id')
        cond = row.get('condition')
        if qid is None or cond is None:
            continue
        bucket[(qid, cond)].append(score)
    return {k: sum(v) / len(v) for k, v in bucket.items() if v}


def response_text(rec, condition):
    r = rec.get('responses', {}).get(condition)
    if r is None:
        return None
    if isinstance(r, dict):
        return r.get('text') or r.get('response') or ''
    return str(r)


def retrieval_facts(rec):
    """Return the list of retrieved facts or a compact string."""
    r = rec.get('retrieval', {})
    if isinstance(r, dict):
        if 'facts' in r and isinstance(r['facts'], list):
            return r['facts']
        # Hamerton has per-system retrieval dicts — pick a facts list if present
        for v in r.values():
            if isinstance(v, dict) and isinstance(v.get('facts'), list):
                return v['facts']
    return []


def is_broad_refusal(text):
    return bool(text) and bool(REFUSAL_RE.search(text))


def find_spec_induced_refusals():
    """Return list of dicts, one per spec-induced refusal case."""
    cases = []
    for subject in LOW_BASELINE_SUBJECTS:
        for system in SYSTEMS:
            data, c1_name, c3_name = load_results(subject, system)
            if data is None:
                continue
            judgments = load_merged_judgments(subject, system)
            for rec in data:
                t1 = response_text(rec, c1_name)
                t3 = response_text(rec, c3_name)
                if t1 is None or t3 is None:
                    continue
                if is_broad_refusal(t3) and not is_broad_refusal(t1):
                    qid = rec.get('question_id')
                    c3_mean = judgments.get((qid, c3_name))
                    c1_mean = judgments.get((qid, c1_name))
                    cases.append({
                        'subject': subject,
                        'system': system,
                        'question_id': qid,
                        'question_text': rec.get('question_text'),
                        'held_out': rec.get('held_out_passage'),
                        'retrieval_facts': retrieval_facts(rec),
                        'c1_response': t1,
                        'c3_response': t3,
                        'c1_mean_score': c1_mean,
                        'c3_mean_score': c3_mean,
                    })
    return cases


CLASSIFY_PROMPT = """You are auditing a single refusal from an AI memory-system study.
Category definitions:

(a) EPISTEMIC_HONEST
    The retrieved facts genuinely do not contain enough material to answer the
    question. The response's refusal is factually correct — there is no way to
    predict the held-out behaviour from what was retrieved. The held-out
    passage contains information that simply is not present or implied in the
    retrieved facts.

(b) SPEC_AXIOM_TRIGGER
    The retrieval actually DOES contain enough material to answer (or at least
    to gesture at the held-out behaviour), but the refusal reads as triggered
    by the spec's honesty/dignity axioms — e.g. refusing to speculate about a
    dead person, refusing without subject-identifying information, refusing
    because of a general caution norm that was absent in the no-spec baseline.
    Use this when the refusal appears conservative rather than warranted.

(c) RUBRIC_ARTIFACT
    The refusal is EPISTEMIC_HONEST (retrieval is truly insufficient) AND the
    judges scored it at or near the 1-anchor floor (mean <= 1.5). Use this
    when the only reason the refusal looks bad is that the judging rubric
    cannot distinguish "honest refusal" from "wrong prediction" and lumps
    them together at score 1.

(d) SCORED_AS_WRONG_PRED
    The refusal is epistemically honest but the judges scored it > 1.5 —
    typically because judges gave partial credit to the refusal's hedged
    commentary. Still not a useful prediction, but not scored at the floor.
    Use this when the response hedges and gets partial credit.

Return ONLY one of: EPISTEMIC_HONEST | SPEC_AXIOM_TRIGGER | RUBRIC_ARTIFACT | SCORED_AS_WRONG_PRED
followed on a new line by a one-sentence justification.

---
QUESTION: {question}

HELD-OUT (ground truth the response did not see): {held_out}

RETRIEVED FACTS (what C3 was given):
{facts}

C3 RESPONSE (the refusal):
{c3}

JUDGES' MEAN SCORE ON THIS RESPONSE: {mean_score}
"""


def classify_case(case, api_key):
    facts_text = "\n".join(f"- {f}" for f in (case['retrieval_facts'] or [])[:10])
    if not facts_text:
        facts_text = "(none reported in retrieval record)"
    mean = case.get('c3_mean_score')
    mean_txt = f"{mean:.2f}" if isinstance(mean, (int, float)) else "unknown"
    prompt = CLASSIFY_PROMPT.format(
        question=(case.get('question_text') or '')[:800],
        held_out=(case.get('held_out') or '')[:800],
        facts=facts_text[:2500],
        c3=(case.get('c3_response') or '')[:1500],
        mean_score=mean_txt,
    )
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': 'claude-haiku-4-5-20251001',
                    'max_tokens': 200,
                    'temperature': 0,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=60,
            )
            if r.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            r.raise_for_status()
            text = r.json()['content'][0]['text'].strip()
            # Parse category from first line
            m = re.search(
                r'\b(EPISTEMIC_HONEST|SPEC_AXIOM_TRIGGER|RUBRIC_ARTIFACT|SCORED_AS_WRONG_PRED)\b',
                text,
            )
            category = m.group(1) if m else 'UNPARSED'
            return category, text
        except Exception as e:
            if attempt == 3:
                return 'ERROR', f'{type(e).__name__}: {e}'
            time.sleep(2 ** (attempt + 1))


def main():
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not in environment")

    cases = find_spec_induced_refusals()
    print(f"Found {len(cases)} spec-induced refusals (broad rule)")
    if len(cases) > 300:
        sys.exit(f"BUDGET CAP: {len(cases)} > 300 — aborting. Trim scope.")

    for i, case in enumerate(cases):
        print(f"[{i+1}/{len(cases)}] classifying {case['subject']}/{case['system']} Q{case['question_id']}", flush=True)
        category, raw = classify_case(case, api_key)
        case['category'] = category
        case['classifier_raw'] = raw

    # Write raw JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump({
            'n_cases': len(cases),
            'cases': cases,
            'classifier_model': 'claude-haiku-4-5-20251001',
            'refusal_rule': 'broad (REFUSAL_RE anywhere)',
            'systems': SYSTEMS,
            'subjects': LOW_BASELINE_SUBJECTS,
            'judges_for_mean_score': JUDGES,
        }, f, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_JSON}")

    # Build summary table
    by_sub_sys = defaultdict(lambda: defaultdict(list))  # [category][system] = [cases]
    totals = defaultdict(int)
    for case in cases:
        cat = case['category']
        totals[cat] += 1
        by_sub_sys[cat][case['system']].append(case)

    # Choose representative examples
    examples = {}
    for cat in ['EPISTEMIC_HONEST', 'SPEC_AXIOM_TRIGGER', 'RUBRIC_ARTIFACT', 'SCORED_AS_WRONG_PRED']:
        # pick the case with median C3 response length in this category
        all_cases = [c for c in cases if c.get('category') == cat]
        if not all_cases:
            examples[cat] = None
            continue
        all_cases.sort(key=lambda c: len(c.get('c3_response') or ''))
        examples[cat] = all_cases[len(all_cases) // 2]

    with OUT_MD.open('w', encoding='utf-8') as f:
        f.write("# Spec-Induced Refusal Audit (P0-5)\n\n")
        f.write("_Classifier: `claude-haiku-4-5-20251001`, temperature 0. Refusal rule: broad (any REFUSAL_RE hit in C3 AND no hit in C1 on the same question)._\n\n")
        f.write(f"**Total spec-induced refusals (broad rule) across 9 low-baseline subjects × 5 memory substrates: {len(cases)}.**\n\n")
        f.write("Narrow rule (C3 opens with explicit refusal, C1 does not) produces only 6 cases across the 45 cells — kept in Appendix but not the primary unit here.\n\n")

        f.write("## Category counts\n\n")
        f.write("| Category | n | % of refusals |\n|---|---:|---:|\n")
        for cat in ['EPISTEMIC_HONEST', 'SPEC_AXIOM_TRIGGER', 'RUBRIC_ARTIFACT', 'SCORED_AS_WRONG_PRED', 'UNPARSED', 'ERROR']:
            n = totals.get(cat, 0)
            if n == 0:
                continue
            pct = 100 * n / len(cases) if cases else 0
            f.write(f"| {cat} | {n} | {pct:.1f}% |\n")
        f.write("\n")

        f.write("## Per-substrate breakdown\n\n")
        f.write("| Substrate | EPIST_HON | SPEC_AXIOM | RUBRIC_ART | WRONG_PRED | total |\n")
        f.write("|---|---:|---:|---:|---:|---:|\n")
        for sys_ in SYSTEMS:
            sys_cases = [c for c in cases if c['system'] == sys_]
            eh = sum(1 for c in sys_cases if c.get('category') == 'EPISTEMIC_HONEST')
            sa = sum(1 for c in sys_cases if c.get('category') == 'SPEC_AXIOM_TRIGGER')
            ra = sum(1 for c in sys_cases if c.get('category') == 'RUBRIC_ARTIFACT')
            wp = sum(1 for c in sys_cases if c.get('category') == 'SCORED_AS_WRONG_PRED')
            f.write(f"| {sys_} | {eh} | {sa} | {ra} | {wp} | {len(sys_cases)} |\n")
        f.write("\n")

        f.write("## Per-subject breakdown\n\n")
        f.write("| Subject | EPIST_HON | SPEC_AXIOM | RUBRIC_ART | WRONG_PRED | total |\n")
        f.write("|---|---:|---:|---:|---:|---:|\n")
        for subj in LOW_BASELINE_SUBJECTS:
            sub_cases = [c for c in cases if c['subject'] == subj]
            eh = sum(1 for c in sub_cases if c.get('category') == 'EPISTEMIC_HONEST')
            sa = sum(1 for c in sub_cases if c.get('category') == 'SPEC_AXIOM_TRIGGER')
            ra = sum(1 for c in sub_cases if c.get('category') == 'RUBRIC_ARTIFACT')
            wp = sum(1 for c in sub_cases if c.get('category') == 'SCORED_AS_WRONG_PRED')
            f.write(f"| {subj} | {eh} | {sa} | {ra} | {wp} | {len(sub_cases)} |\n")
        f.write("\n")

        f.write("## Representative examples\n\n")
        for cat in ['EPISTEMIC_HONEST', 'SPEC_AXIOM_TRIGGER', 'RUBRIC_ARTIFACT', 'SCORED_AS_WRONG_PRED']:
            ex = examples.get(cat)
            if not ex:
                f.write(f"### {cat}: none\n\n")
                continue
            f.write(f"### {cat} — {ex['subject']}/{ex['system']} Q{ex['question_id']}\n\n")
            f.write(f"**Question:** {ex['question_text']}\n\n")
            ho = ex.get('held_out') or ''
            f.write(f"**Held-out passage:** {ho[:500]}\n\n")
            mean = ex.get('c3_mean_score')
            mean_txt = f"{mean:.2f}" if isinstance(mean, (int, float)) else 'n/a'
            f.write(f"**C3 response (mean judge score: {mean_txt}):**\n\n> " +
                    (ex.get('c3_response') or '')[:800].replace("\n", "\n> ") + "\n\n")
            f.write(f"**Classifier reasoning:** {ex.get('classifier_raw', '')[:500]}\n\n")

        f.write("## Interpretation\n\n")
        total_nonwrong = totals.get('EPISTEMIC_HONEST', 0) + totals.get('RUBRIC_ARTIFACT', 0)
        total_axiom = totals.get('SPEC_AXIOM_TRIGGER', 0)
        pct_nonwrong = 100 * total_nonwrong / len(cases) if cases else 0
        pct_axiom = 100 * total_axiom / len(cases) if cases else 0
        f.write(
            "Across the 9 low-baseline × 5 memory-substrate cells, the spec turns "
            f"{len(cases)} C1 non-refusals into C3 refusals (broad rule). "
            f"Of these, roughly {pct_nonwrong:.0f}% are EPISTEMIC_HONEST or RUBRIC_ARTIFACT — i.e. the "
            "refusal is correct behaviour that the held-out passage could not be "
            "extracted from retrieval, and the rubric's 1-anchor only floor penalizes "
            "the honest refusal. "
            f"Another {pct_axiom:.0f}% are SPEC_AXIOM_TRIGGER — the retrieval arguably supported an "
            "answer but the spec's honesty/dignity axioms caused the model to hold back. "
            "The tail is SCORED_AS_WRONG_PRED. "
            "For §4.4 (spec mechanism): the spec's honesty axioms trade retrieved-fact coverage "
            "for conservatism, and the study's 1-5 rubric cannot reward the conservatism. "
            "For §7 (safety/alignment overlap): axiom-triggered refusals are a signature of the "
            "spec acting as a policy layer on top of retrieval, not as a retrieval replacement.\n"
        )

    print(f"Wrote {OUT_MD}")


if __name__ == '__main__':
    main()
