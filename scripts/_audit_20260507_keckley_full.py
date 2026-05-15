"""Full reconciliation of Keckley Q21 across all systems."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUBJ_DIR = REPO / 'results' / 'global_keckley'
BACKFILL_DIR = REPO / 'results' / '_s114_backfills'
PRIMARY = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

systems = {
    'baselayer': ('baselayer', 'C1_baselayer', 'C3_baselayer'),
    'supermemory': ('supermemory', 'C1_supermemory', 'C3_supermemory'),
    'letta': ('letta', 'C1_letta', 'C3_letta'),
    'mem0': ('mem0', 'C1_mem0', 'C3_mem0'),
    'zep': ('zep', 'C1_zep', 'C3_zep'),
}


def load_score(prefix, condition, judge, qid=21):
    """Returns the post-backfill score for a (system, condition, judge, qid) cell."""
    # Check backfill first
    bf_path = BACKFILL_DIR / f'global_keckley__{condition}__{judge}.json'
    if bf_path.exists():
        rows = json.load(bf_path.open(encoding='utf-8'))
        for r in rows:
            if r.get('question_id') == qid:
                if not r.get('parse_failure') and r.get('score') is not None:
                    return ('backfill', r['score'])
                else:
                    bf_failed = True
    # Original
    pj_path = SUBJ_DIR / f'{prefix}_judgments_{judge}.json'
    if not pj_path.exists():
        return ('missing_file', None)
    rows = json.load(pj_path.open(encoding='utf-8'))
    for r in rows:
        if r.get('question_id') == qid and r.get('condition') == condition:
            if r.get('parse_failure'):
                return ('parse_failure_orig', None)
            if r.get('score') in (0, None):
                return ('zero_score', None)
            return ('original', r['score'])
    return ('not_in_file', None)


for sys_name, (prefix, c1_label, c3_label) in systems.items():
    c1_scores = {}
    c3_scores = {}
    for j in PRIMARY:
        s, v = load_score(prefix, c1_label, j)
        c1_scores[j] = (s, v)
        s, v = load_score(prefix, c3_label, j)
        c3_scores[j] = (s, v)
    valid_c1 = [v for s, v in c1_scores.values() if v is not None]
    valid_c3 = [v for s, v in c3_scores.values() if v is not None]
    print(f'\n=== {sys_name} ===')
    print(f'  C1: {c1_scores}')
    print(f'  C3: {c3_scores}')
    if valid_c1 and valid_c3:
        mean_c1 = sum(valid_c1) / len(valid_c1)
        mean_c3 = sum(valid_c3) / len(valid_c3)
        print(f'  C1 mean (n={len(valid_c1)}): {mean_c1:.3f}')
        print(f'  C3 mean (n={len(valid_c3)}): {mean_c3:.3f}')
        print(f'  Delta: {mean_c3 - mean_c1:+.3f}')
        # 3-judge Anthropic subset
        anth_c1 = [c1_scores[j][1] for j in ['haiku', 'sonnet', 'opus'] if c1_scores[j][1] is not None]
        anth_c3 = [c3_scores[j][1] for j in ['haiku', 'sonnet', 'opus'] if c3_scores[j][1] is not None]
        if anth_c1 and anth_c3:
            print(f'  3-judge (haiku/sonnet/opus): C1={sum(anth_c1)/len(anth_c1):.3f}, C3={sum(anth_c3)/len(anth_c3):.3f}, delta={sum(anth_c3)/len(anth_c3) - sum(anth_c1)/len(anth_c1):+.3f}')
