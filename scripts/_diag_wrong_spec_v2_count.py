"""Count valid responses to judge across 13 globals for wrong_spec_v2."""
import json, os
subjects=['augustine','babur','bernal_diaz','cellini','ebers','equiano','fukuzawa','keckley','rousseau','seacole','sunity_devee','yung_wing','zitkala_sa']
total_to_judge = 0
for s in subjects:
    resp = f'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_{s}/wrong_spec_v2_results.json'
    data = json.load(open(resp, encoding='utf-8'))
    valid = 0
    for q in data:
        if not q.get('held_out_passage'): continue
        r = q.get('response', {})
        if not isinstance(r, dict): continue
        if 'error' in r or 'text' not in r: continue
        valid += 1
    print(f'{s}: {valid} valid responses with held_out (out of {len(data)})')
    total_to_judge += valid
print('TOTAL valid to judge:', total_to_judge)
print('---')
for s in subjects:
    h = f'results/_wrong_spec_v2/global_{s}/wrong_spec_v2_judgments_haiku.json'
    if os.path.exists(h):
        d = json.load(open(h, encoding='utf-8'))
        valid_h = sum(1 for r in d if not r.get('parse_failure'))
        print(f'{s}: haiku records={len(d)}, valid={valid_h}')
