"""One-off verification: do the high-baseline globals have full 5-judge
coverage on enough qids per condition to support k=2-3 sampling?

Run once, print counts, then delete or ignore.
"""
import json
from pathlib import Path

CONDITION_ALIASES = {
    'C5_baseline': ['C5_baseline'],
    'C2a': ['C2a_full_spec', 'C2a_spec'],
    'C4a': ['C4a_full_facts_plus_spec', 'C4a_full_all_facts_plus_spec', 'C4a_facts_plus_spec'],
    'C8':  ['C8_raw_corpus'],
    'C9':  ['C9_raw_corpus_plus_spec'],
}
PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
backfill_dir = RESULTS / '_s114_backfills'


def load(p: Path):
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def find_orig(subj_dir: Path, qid: int, raw_cond: str) -> dict:
    out: dict = {}

    def consume(r):
        if not isinstance(r, dict):
            return
        if r.get('question_id') != qid or r.get('condition') != raw_cond:
            return
        j = r.get('judge')
        sc = r.get('score')
        if j and sc not in (None, 0):
            jc = j.lower().replace('-', '').replace('.', '')
            jc = {'haiku': 'haiku', 'sonnet': 'sonnet', 'opus': 'opus',
                  'gpt4o': 'gpt4o', 'gpt54': 'gpt54', 'gpt5': 'gpt54'}.get(jc, jc)
            if jc in PRIMARY_JUDGES:
                out[jc] = sc
        for jname, jc in [('haiku', 'haiku'), ('sonnet', 'sonnet'), ('opus', 'opus'),
                          ('gpt4o', 'gpt4o'), ('gpt54', 'gpt54')]:
            key = f'{jname}_score'
            if key in r and r[key] not in (None, 0):
                out[jc] = r[key]

    for fp in sorted(subj_dir.glob('*.json')):
        n = fp.name.lower()
        if 'retrieval' in n or 'manifest' in n or 'extracted' in n or 'ingestion' in n:
            continue
        if 'results' in n and 'judgments' not in n:
            continue
        d = load(fp)
        if not d or not isinstance(d, list):
            continue
        for r in d:
            consume(r)

    if backfill_dir.exists():
        prefix = subj_dir.name
        for jc in PRIMARY_JUDGES:
            fp = backfill_dir / f'{prefix}__{raw_cond}__{jc}.json'
            if fp.exists():
                d = load(fp)
                if d:
                    for r in d:
                        if r.get('question_id') == qid and r.get('condition') == raw_cond:
                            sc = r.get('score')
                            if sc not in (None, 0):
                                out[jc] = sc
                                break
    return out


def main():
    subjects = ['global_augustine', 'global_cellini', 'global_rousseau', 'global_zitkala_sa',
                'hamerton', 'global_sunity_devee', 'global_ebers', 'global_yung_wing', 'global_babur']
    for subj in subjects:
        sd = RESULTS / subj
        print(f'=== {subj} ===')
        for pc, aliases in CONDITION_ALIASES.items():
            qids_full = []
            qids_partial = []
            qids_seen = set()
            for fname in ['results.json', 'baselayer_results.json', 'c8_c9_results.json',
                          'fullstack_haiku.json', 'results_v2.json']:
                d = load(sd / fname)
                if not d:
                    continue
                for r in d:
                    qid = r.get('question_id')
                    if qid in qids_seen:
                        continue
                    ho = r.get('held_out_passage')
                    if not ho:
                        continue
                    resps = r.get('responses', {})
                    for alias in aliases:
                        if alias in resps:
                            rec = resps[alias]
                            text = rec.get('text', '') if isinstance(rec, dict) else (rec or '')
                            if text and len(text.strip()) > 50:
                                qids_seen.add(qid)
                                scs = find_orig(sd, qid, alias)
                                if all(j in scs for j in PRIMARY_JUDGES):
                                    qids_full.append(qid)
                                else:
                                    qids_partial.append((qid, sorted(scs.keys())))
                                break
            print(f'  {pc}: full={len(qids_full)}, partial={len(qids_partial)}')


if __name__ == '__main__':
    main()
