"""Diagnostic: locate judgments + responses for the conditions used in the
published-rubric robustness check (Option B).

Goal: prove that for every (subject, condition) on a candidate sample we can
recover all 5 primary judges' scores AND the response text + held-out passage.
"""
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'

PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

# Subjects in scope. Hamerton + 4 globals + Franklin (high-baseline reference).
SUBJECTS = {
    'hamerton':       RESULTS / 'hamerton',
    'global_ebers':   RESULTS / 'global_ebers',
    'global_yung_wing': RESULTS / 'global_yung_wing',
    'global_babur':   RESULTS / 'global_babur',
    'global_equiano': RESULTS / 'global_equiano',
    'global_augustine': RESULTS / 'global_augustine',
    'franklin':       RESULTS / 'franklin',
}

# Map each "paper condition" -> (responses_file, judgments_files_pattern).
# We look for 5 conditions: C5_baseline, C2a (full_spec or full), C4a (full_facts_plus_spec or full_all_facts_plus_spec), C8_raw_corpus, C9_raw_corpus_plus_spec.

CONDITION_ALIASES = {
    'C5_baseline': ['C5_baseline'],
    'C2a': ['C2a_full_spec', 'C2a_spec'],
    'C4a': ['C4a_full_facts_plus_spec', 'C4a_full_all_facts_plus_spec', 'C4a_facts_plus_spec'],
    'C8':  ['C8_raw_corpus'],
    'C9':  ['C9_raw_corpus_plus_spec'],
}


def load_jsonl_array(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'  ERR loading {path.name}: {e}')
        return None


def find_responses(subj_dir, qid, paper_cond):
    """Return (response_text, held_out_passage, raw_cond_label, source_file) or None."""
    aliases = CONDITION_ALIASES[paper_cond]
    candidate_files = [
        'results.json',
        'results_v2.json',
        'baselayer_results.json',
        'c8_c9_results.json',
        'fullstack_haiku.json',
    ]
    for fname in candidate_files:
        p = subj_dir / fname
        d = load_jsonl_array(p)
        if not d:
            continue
        for r in d:
            if r.get('question_id') != qid:
                continue
            ho = r.get('held_out_passage')
            resps = r.get('responses', {})
            for alias in aliases:
                if alias in resps:
                    text = resps[alias]
                    if isinstance(text, dict):
                        text = text.get('text', '') or ''
                    if text and len(text.strip()) > 50:
                        return (text, ho, alias, fname)
    return None


def find_judge_scores(subj_dir, qid, paper_cond, raw_cond_label):
    """Return dict[judge -> score]. Look across all judgment files in this dir."""
    out = {}

    # Hamerton has per-judge files <judge>_judgments.json (sonnet, opus, gpt4o)
    # plus haiku in judgments.json (haiku_score) and gpt54 in gpt54_judgments.json.
    # Globals have judgments_v2.json (haiku) and ?? for the rest. Also baselayer_judgments_<judge>.json
    # but those are for C1/C3_baselayer (memory-system view).
    # c8_c9_judgments_<judge>.json for C8/C9.

    # Strategy: scan all .json in subj_dir, look for records matching qid+condition, extract score.
    for fp in sorted(subj_dir.glob('*.json')):
        name = fp.name.lower()
        if 'retrieval' in name or 'manifest' in name or 'extracted' in name or 'ingestion' in name:
            continue
        if 'results' in name and 'judgments' not in name:
            continue
        d = load_jsonl_array(fp)
        if not d or not isinstance(d, list):
            continue
        for r in d:
            if not isinstance(r, dict):
                continue
            if r.get('question_id') != qid:
                continue
            cond = r.get('condition')
            if cond != raw_cond_label:
                continue
            # Try unified schema {judge, score}
            j = r.get('judge')
            sc = r.get('score')
            if j and sc not in (None, 0):
                # Map judge label to canonical
                jc = j.lower().strip()
                jc = {'haiku': 'haiku', 'sonnet': 'sonnet', 'opus': 'opus',
                      'gpt4o': 'gpt4o', 'gpt-4o': 'gpt4o',
                      'gpt54': 'gpt54', 'gpt-5.4': 'gpt54', 'gpt5': 'gpt54',
                      'gemini_flash': 'gemini_flash', 'gemini': 'gemini_flash',
                      'gemini_pro': 'gemini_pro'}.get(jc, jc)
                if jc in PRIMARY_JUDGES:
                    out[jc] = sc
                continue
            # Try wide schema with <judge>_score columns
            for jname, jc in [('haiku', 'haiku'), ('sonnet', 'sonnet'), ('opus', 'opus'),
                               ('gpt4o', 'gpt4o'), ('gpt54', 'gpt54'),
                               ('gemini', 'gemini_flash')]:
                key = f'{jname}_score'
                if key in r and r[key] not in (None, 0):
                    if jc in PRIMARY_JUDGES:
                        out[jc] = r[key]

    # Also check _s114_backfills/<subject>__<cond>__<judge>.json (backfill files)
    backfill_dir = RESULTS / '_s114_backfills'
    if backfill_dir.exists():
        # Naming: global_<subject>__<cond>__<judge>.json or hamerton__<cond>__<judge>.json
        # subject prefix is name of subj_dir (e.g. global_yung_wing or hamerton)
        prefix = subj_dir.name
        for jc in PRIMARY_JUDGES:
            fp = backfill_dir / f'{prefix}__{raw_cond_label}__{jc}.json'
            if fp.exists():
                d = load_jsonl_array(fp)
                if d:
                    for r in d:
                        if r.get('question_id') == qid and r.get('condition') == raw_cond_label:
                            sc = r.get('score')
                            if sc not in (None, 0):
                                out[jc] = sc
                                break
    return out


def main():
    print('Subjects:', list(SUBJECTS))
    print('Paper conditions:', list(CONDITION_ALIASES))
    # For each subject, list available QIDs from canonical responses files, and probe condition coverage.
    for subj, sd in SUBJECTS.items():
        if not sd.exists():
            print(f'!! {subj}: dir missing')
            continue
        print(f'\n== {subj} ({sd}) ==')
        # Pick a few qids to probe
        # Find the qids from results.json / baselayer_results.json
        rj = load_jsonl_array(sd / 'results.json') or load_jsonl_array(sd / 'baselayer_results.json') or load_jsonl_array(sd / 'fullstack_haiku.json')
        if not rj:
            print('  no results json found')
            continue
        # Get tier filter for franklin/hamerton (behavioral_prediction)
        bp = [r for r in rj if r.get('held_out_passage')]
        qids = [r['question_id'] for r in bp]
        print(f'  total q with held_out: {len(qids)}')
        if not qids:
            continue
        probe_qids = qids[:2]
        for qid in probe_qids:
            for pc in CONDITION_ALIASES:
                resp = find_responses(sd, qid, pc)
                if not resp:
                    print(f'  q={qid} cond={pc:<12s} RESPONSE_MISSING')
                    continue
                text, ho, raw_cond, src = resp
                scores = find_judge_scores(sd, qid, pc, raw_cond)
                missing = [j for j in PRIMARY_JUDGES if j not in scores]
                status = 'OK ' if not missing else f'PART (missing: {missing})'
                print(f'  q={qid} cond={pc:<12s} -> {raw_cond:<32s} resp_src={src:<22s} judges={list(scores.keys())} {status}')


if __name__ == '__main__':
    main()
