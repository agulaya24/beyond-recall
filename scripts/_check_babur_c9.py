import json
from pathlib import Path
_REPO = Path(__file__).resolve().parents[1]
d = json.load(open(_REPO / 'results' / 'global_babur' / 'c8_c9_results.json',encoding='utf-8'))
print('len:', len(d))
ho_count = sum(1 for r in d if r.get('held_out_passage'))
c8 = sum(1 for r in d if 'C8_raw_corpus' in r.get('responses',{}) and r['responses']['C8_raw_corpus'].get('text'))
c9 = sum(1 for r in d if 'C9_raw_corpus_plus_spec' in r.get('responses',{}) and r['responses']['C9_raw_corpus_plus_spec'].get('text'))
print('held_out present:', ho_count, 'C8 with text:', c8, 'C9 with text:', c9)
for r in d[:3]:
    print('q=', r['question_id'], 'cond keys:', list(r.get('responses',{}).keys()))
