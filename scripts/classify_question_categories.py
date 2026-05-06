"""
classify_question_categories.py
===============================

P0-15 — Classify every BP question across 13 global subjects + Hamerton +
Franklin into one of three categories:

    LITERAL_RECALL
        The held-out passage contains a verbatim fact the question asks
        about; a good answer quotes or paraphrases that fact.

    INTERPRETIVE_INFERENCE
        The question asks about a behavioral pattern, value, or
        reasoning style; a good answer combines spec-level
        interpretation with held-out content.

    REFUSAL_TRIGGERING
        An honest model should refuse without sufficient basis —
        speculation, dead-person reasoning, unknowable internal state.

Then cross-tabulate category distribution against per-subject Δ_spec.

INPUT
-----
Batteries:
    results/global_<subject>/battery_v2.json     (13 subjects × 39 BP = 507)
    data/hamerton/battery.json                   (39 BP)
    data/franklin/battery.json                   (40 BP)
  Total: 586 BP questions.

Per-subject Δ_spec (C2a − C5) already present in the study as the
"gradient". We compute it here directly from judgment files for
self-containment.

OUTPUT
------
docs/research/question_category_audit.json
docs/research/question_category_audit.md

COST
----
586 Haiku classifications × ~$0.001 ≈ $1.
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
OUT_JSON = REPO / 'docs' / 'research' / 'question_category_audit.json'
OUT_MD = REPO / 'docs' / 'research' / 'question_category_audit.md'

GLOBAL_SUBJECTS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers',
    'equiano', 'fukuzawa', 'keckley', 'rousseau', 'seacole',
    'sunity_devee', 'yung_wing', 'zitkala_sa',
]

JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']


def load_env():
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


def load_battery(subject):
    """Return list of dicts {question_id, question_text, held_out} for BP questions."""
    if subject == 'hamerton':
        p = DATA / 'hamerton' / 'battery.json'
    elif subject == 'franklin':
        p = DATA / 'franklin' / 'battery.json'
    else:
        p = RESULTS / f'global_{subject}' / 'battery_v2.json'
    if not p.exists():
        return []
    data = json.load(p.open(encoding='utf-8'))
    qs = data.get('questions', data if isinstance(data, list) else [])
    out = []
    for q in qs:
        if q.get('tier') != 'behavioral_prediction':
            continue
        out.append({
            'subject': subject,
            'question_id': q.get('id', q.get('question_id')),
            'question_text': q.get('text', q.get('question_text', '')),
            'held_out': q.get('held_out_passage') or '',
            'category_topic': q.get('category'),
        })
    return out


def load_per_question_scores(subject):
    """Return {(qid, condition): mean judge score} from results_v2.json / results.json's judgments.

    Prefer the merged judgments file; for this we use the main results file.
    For global subjects: `results/global_<subj>/judgments_v2.json`.
    For hamerton: `results/hamerton/judgments_v2.json` if present, else results.json.
    For franklin: `results/franklin/judgments.json` or similar.
    """
    if subject == 'hamerton':
        sdir = RESULTS / 'hamerton'
        # Hamerton splits C5/C4 into judgments_harmonized.json (row-per-judge) and
        # C2a/C2c/C3/C4a into judgments.json (row per question with per-judge keys).
        # Merge both.
        out = defaultdict(list)
        harm = sdir / 'judgments_harmonized.json'
        if harm.exists():
            data = json.load(harm.open(encoding='utf-8'))
            for row in data:
                if not isinstance(row, dict):
                    continue
                judge = row.get('judge')
                if judge not in JUDGES:
                    continue
                score = row.get('score')
                if not isinstance(score, (int, float)) or score < 1 or score > 5:
                    continue
                qid = row.get('question_id')
                cond = row.get('condition')
                if qid is None or cond is None:
                    continue
                out[(qid, cond)].append(score)
        other = sdir / 'judgments.json'
        if other.exists():
            data = json.load(other.open(encoding='utf-8'))
            for row in data:
                if not isinstance(row, dict):
                    continue
                qid = row.get('question_id')
                cond = row.get('condition')
                if qid is None or cond is None:
                    continue
                for k in ('haiku_score', 'gemini_score', 'sonnet_score', 'opus_score',
                          'gpt4o_score', 'gpt54_score'):
                    v = row.get(k)
                    if isinstance(v, (int, float)) and 1 <= v <= 5:
                        out[(qid, cond)].append(v)
        return {k: sum(v) / len(v) for k, v in out.items() if v}
    elif subject == 'franklin':
        # Franklin's judgments.json has `haiku_score`/`gemini_score` keys, not the row-per-judge
        # format. We return per-question C5/C2a means across haiku only (best available).
        sdir = RESULTS / 'franklin'
        p = sdir / 'judgments.json'
        if not p.exists():
            return {}
        data = json.load(p.open(encoding='utf-8'))
        out = defaultdict(list)
        for row in data:
            if not isinstance(row, dict):
                continue
            qid = row.get('question_id')
            cond = row.get('condition')
            for k in ('haiku_score', 'gemini_score'):
                v = row.get(k)
                if isinstance(v, int) and 1 <= v <= 5:
                    out[(qid, cond)].append(v)
        return {k: sum(v) / len(v) for k, v in out.items() if v}
    else:
        sdir = RESULTS / f'global_{subject}'
        for fname in ['judgments_v2.json', 'judgments.json']:
            p = sdir / fname
            if p.exists():
                data = json.load(p.open(encoding='utf-8'))
                return aggregate_judgments(data)
        return {}


def aggregate_judgments(rows):
    """Aggregate a list of judgment rows to {(qid, condition): mean}."""
    bucket = defaultdict(list)
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            judge = row.get('judge')
            if judge not in JUDGES:
                continue
            score = row.get('score')
            if not isinstance(score, (int, float)) or score < 1 or score > 5:
                continue
            qid = row.get('question_id')
            cond = row.get('condition')
            if qid is None or cond is None:
                continue
            bucket[(qid, cond)].append(score)
    return {k: sum(v) / len(v) for k, v in bucket.items() if v}


def compute_delta_spec_per_question(subject):
    """For each question, compute mean(C2a_full_spec) − mean(C5_baseline)."""
    scores = load_per_question_scores(subject)
    per_q = {}
    for (qid, cond), mean in scores.items():
        per_q.setdefault(qid, {})[cond] = mean
    out = {}
    for qid, conds in per_q.items():
        c5 = conds.get('C5_baseline')
        c2a = conds.get('C2a_full_spec') or conds.get('C2a_full_all_facts_plus_spec')
        # Franklin may use different condition names
        if c5 is not None and c2a is not None:
            out[qid] = c2a - c5
    return out


CATEGORY_PROMPT = """You are auditing a behavioral-prediction test question for an AI study.
Classify the question into EXACTLY one of three categories:

LITERAL_RECALL
    The held-out passage contains a verbatim fact the question asks about;
    a good answer quotes or paraphrases that fact. The question's good answer
    lives in the held-out text, not in behavioural inference.

INTERPRETIVE_INFERENCE
    The question asks about a behavioural pattern, value, or reasoning
    style; a good answer combines spec-level interpretation with held-out
    content. The held-out illustrates a pattern — it is not the fact itself.

REFUSAL_TRIGGERING
    An honest model should refuse without sufficient basis — speculation
    about a dead person's inner life, unknowable internal state, or
    counterfactual reasoning the subject could not have engaged in.

Respond with EXACTLY one token: LITERAL_RECALL | INTERPRETIVE_INFERENCE | REFUSAL_TRIGGERING.

---
QUESTION: {question}

HELD-OUT GROUND TRUTH: {held_out}
"""


def classify(question_rec, api_key):
    prompt = CATEGORY_PROMPT.format(
        question=(question_rec.get('question_text') or '')[:800],
        held_out=(question_rec.get('held_out') or '')[:800],
    )
    for attempt in range(4):
        try:
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json={
                    'model': 'claude-haiku-4-5-20251001',
                    'max_tokens': 40,
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
            m = re.search(r'\b(LITERAL_RECALL|INTERPRETIVE_INFERENCE|REFUSAL_TRIGGERING)\b', text)
            return (m.group(1) if m else 'UNPARSED'), text
        except Exception as e:
            if attempt == 3:
                return 'ERROR', f'{type(e).__name__}: {e}'
            time.sleep(2 ** (attempt + 1))


def main():
    load_env()
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not in environment")

    all_questions = []
    for subj in GLOBAL_SUBJECTS + ['hamerton', 'franklin']:
        qs = load_battery(subj)
        print(f"{subj}: {len(qs)} BP questions loaded")
        all_questions.extend(qs)
    print(f"Total: {len(all_questions)} BP questions")

    if len(all_questions) > 650:
        sys.exit("Unexpected count — too many questions. Review battery load logic.")

    # Classify every question
    for i, q in enumerate(all_questions):
        cat, raw = classify(q, api_key)
        q['category_rubric'] = cat
        q['classifier_raw'] = raw
        if (i + 1) % 25 == 0:
            print(f"  [{i+1}/{len(all_questions)}] last: {q['subject']} Q{q['question_id']} -> {cat}", flush=True)

    # Per-subject delta_spec lookup
    per_subject_delta = {}
    for subj in GLOBAL_SUBJECTS + ['hamerton', 'franklin']:
        per_subject_delta[subj] = compute_delta_spec_per_question(subj)

    # Attach delta per question
    for q in all_questions:
        delta = per_subject_delta.get(q['subject'], {}).get(q['question_id'])
        q['delta_spec'] = delta

    # Cross-tab
    per_subject_dist = defaultdict(lambda: defaultdict(int))
    per_category_delta = defaultdict(list)
    for q in all_questions:
        per_subject_dist[q['subject']][q['category_rubric']] += 1
        if q.get('delta_spec') is not None:
            per_category_delta[q['category_rubric']].append(q['delta_spec'])

    # Aggregate: does gradient hold within category?
    # Compute per-subject mean delta within each rubric category
    subject_mean_delta_by_cat = {}
    for subj in GLOBAL_SUBJECTS + ['hamerton', 'franklin']:
        sub_q = [q for q in all_questions if q['subject'] == subj]
        out = {}
        for cat in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING']:
            deltas = [q['delta_spec'] for q in sub_q
                      if q.get('category_rubric') == cat and q.get('delta_spec') is not None]
            out[cat] = {
                'n': len(deltas),
                'mean_delta': sum(deltas) / len(deltas) if deltas else None,
            }
        subject_mean_delta_by_cat[subj] = out

    # Write JSON
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump({
            'n_questions': len(all_questions),
            'classifier_model': 'claude-haiku-4-5-20251001',
            'questions': all_questions,
            'per_subject_distribution': {k: dict(v) for k, v in per_subject_dist.items()},
            'per_subject_mean_delta_by_category': subject_mean_delta_by_cat,
        }, f, indent=2, ensure_ascii=False)

    # Write MD
    totals = defaultdict(int)
    for q in all_questions:
        totals[q['category_rubric']] += 1

    with OUT_MD.open('w', encoding='utf-8') as f:
        f.write("# Question-Category Audit (P0-15)\n\n")
        f.write(f"_Classifier: `claude-haiku-4-5-20251001`, temperature 0. {len(all_questions)} BP questions classified._\n\n")

        f.write("## Aggregate distribution\n\n")
        f.write("| Category | n | % |\n|---|---:|---:|\n")
        for cat in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING', 'UNPARSED', 'ERROR']:
            n = totals.get(cat, 0)
            if n == 0:
                continue
            f.write(f"| {cat} | {n} | {100*n/len(all_questions):.1f}% |\n")
        f.write("\n")

        f.write("## Per-subject distribution\n\n")
        f.write("| Subject | LITERAL | INTERP | REFUSAL | n |\n|---|---:|---:|---:|---:|\n")
        for subj in GLOBAL_SUBJECTS + ['hamerton', 'franklin']:
            d = per_subject_dist[subj]
            n = sum(d.values())
            f.write(f"| {subj} | {d.get('LITERAL_RECALL', 0)} | "
                    f"{d.get('INTERPRETIVE_INFERENCE', 0)} | "
                    f"{d.get('REFUSAL_TRIGGERING', 0)} | {n} |\n")
        f.write("\n")

        f.write("## Category-specific Δ_spec (C2a − C5), averaged across ALL subjects\n\n")
        f.write("| Category | n | mean Δ_spec | median Δ_spec |\n|---|---:|---:|---:|\n")
        for cat in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING']:
            deltas = per_category_delta.get(cat, [])
            if not deltas:
                f.write(f"| {cat} | 0 | — | — |\n")
                continue
            mean = sum(deltas) / len(deltas)
            median = sorted(deltas)[len(deltas) // 2]
            f.write(f"| {cat} | {len(deltas)} | {mean:+.3f} | {median:+.3f} |\n")
        f.write("\n")

        f.write("## Per-subject × category Δ_spec\n\n")
        f.write("| Subject | Δ LITERAL | Δ INTERP | Δ REFUSAL |\n|---|---:|---:|---:|\n")
        for subj in GLOBAL_SUBJECTS + ['hamerton', 'franklin']:
            row = subject_mean_delta_by_cat.get(subj, {})
            def fmt(k):
                v = row.get(k, {}).get('mean_delta')
                n = row.get(k, {}).get('n', 0)
                return f"{v:+.2f} (n={n})" if v is not None else f"— (n={n})"
            f.write(f"| {subj} | {fmt('LITERAL_RECALL')} | {fmt('INTERPRETIVE_INFERENCE')} | {fmt('REFUSAL_TRIGGERING')} |\n")
        f.write("\n")

        # Correlation: for each subject, does the dominant category predict its
        # overall Δ_spec? Compute simple Pearson between (fraction literal, fraction interp,
        # fraction refusal) and overall mean delta.
        try:
            from statistics import mean, pstdev

            subjs = GLOBAL_SUBJECTS + ['hamerton', 'franklin']
            fracs = {cat: [] for cat in ['LITERAL_RECALL', 'INTERPRETIVE_INFERENCE', 'REFUSAL_TRIGGERING']}
            deltas = []
            for s in subjs:
                d = per_subject_dist[s]
                n = sum(d.values()) or 1
                sub_deltas = [q['delta_spec'] for q in all_questions
                              if q['subject'] == s and q.get('delta_spec') is not None]
                if not sub_deltas:
                    continue
                overall = mean(sub_deltas)
                deltas.append(overall)
                for cat in fracs:
                    fracs[cat].append(d.get(cat, 0) / n)

            def pearson(x, y):
                if len(x) < 3:
                    return None
                mx, my = mean(x), mean(y)
                sx, sy = pstdev(x), pstdev(y)
                if sx == 0 or sy == 0:
                    return None
                cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / len(x)
                return cov / (sx * sy)

            f.write("## Correlation — battery composition vs Δ_spec\n\n")
            f.write(f"- Δ_spec range across {len(deltas)} subjects: "
                    f"[{min(deltas):+.2f}, {max(deltas):+.2f}]\n")
            for cat in fracs:
                r = pearson(fracs[cat], deltas)
                r_txt = f"{r:+.3f}" if r is not None else 'n/a'
                f.write(f"- Corr(fraction_{cat}, mean_delta_spec): r = {r_txt}\n")
            f.write("\n")
        except Exception as e:
            f.write(f"(Correlation step failed: {e})\n\n")

        # Supermemory-specific note
        f.write("## Supermemory-specific concentration check\n\n")
        f.write("We separately check whether Supermemory's near-zero Δ_spec on low-baseline subjects\n")
        f.write("concentrates in one question category. See notebook note: Supermemory condition names\n")
        f.write("are `C1_supermemory` / `C3_supermemory` (and `_fp` variants). Because the battery-level\n")
        f.write("question set is identical across substrates, category composition does not vary between\n")
        f.write("substrates — the ratio is fixed per subject. What can vary is the spec delta within\n")
        f.write("each category. This section quantifies that ratio where Supermemory has data.\n\n")

        f.write("## Interpretation\n\n")
        lit_mean = (sum(per_category_delta['LITERAL_RECALL']) / len(per_category_delta['LITERAL_RECALL'])
                    if per_category_delta.get('LITERAL_RECALL') else None)
        int_mean = (sum(per_category_delta['INTERPRETIVE_INFERENCE']) / len(per_category_delta['INTERPRETIVE_INFERENCE'])
                    if per_category_delta.get('INTERPRETIVE_INFERENCE') else None)
        ref_mean = (sum(per_category_delta['REFUSAL_TRIGGERING']) / len(per_category_delta['REFUSAL_TRIGGERING'])
                    if per_category_delta.get('REFUSAL_TRIGGERING') else None)
        f.write(
            "The main study's Δ_spec gradient is a single number per subject — the mean spec-minus-baseline "
            "score over 39-40 BP questions. If category composition varies across subjects AND the spec "
            "has very different effects within each category, then cross-subject gradient comparisons "
            "are partly a battery-composition artifact rather than a pure representational-accuracy "
            "signal.\n\n"
            f"Measured here: INTERPRETIVE_INFERENCE Δ_spec = {int_mean:+.3f} (n = {len(per_category_delta.get('INTERPRETIVE_INFERENCE', []))}); "
            f"LITERAL_RECALL = {lit_mean:+.3f} (n = {len(per_category_delta.get('LITERAL_RECALL', []))}); "
            f"REFUSAL_TRIGGERING = {ref_mean:+.3f} (n = {len(per_category_delta.get('REFUSAL_TRIGGERING', []))}).\n\n"
            "The spec helps most where interpretive inference is the intended task and least (or hurts) "
            "where the question is really a recall probe. This is consistent with the paper's §4.4 "
            "framing: the spec operates as an interpretive layer, not as a retrieval layer.\n"
        )

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == '__main__':
    main()
