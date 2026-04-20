import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check if Babur's results_v2.json uses same qids/texts as letta_memory_haiku_results
p1 = 'C:/Users/Aarik/Anthropic/memory-study-repo/results/global_babur/results_v2.json'
p2 = 'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_babur/letta_memory_haiku_results.json'

with open(p1, 'r', encoding='utf-8') as f:
    bl = json.load(f)
with open(p2, 'r', encoding='utf-8') as f:
    letta = json.load(f)['results']

# Build qid -> question_text for each
bl_map = {r['question_id']: r['question_text'] for r in bl}
letta_map = {r['question_id']: r['question_text'] for r in letta}

print('BL qids:', sorted(bl_map.keys())[:10], '...', sorted(bl_map.keys())[-5:])
print('Letta qids:', sorted(letta_map.keys())[:10], '...', sorted(letta_map.keys())[-5:])

common = sorted(set(bl_map) & set(letta_map))
mismatches = []
for q in common:
    if bl_map[q] != letta_map[q]:
        mismatches.append((q, bl_map[q], letta_map[q]))

print(f'\nCommon qids: {len(common)}')
print(f'Mismatches: {len(mismatches)}')
for q, b, l in mismatches[:10]:
    print(f'\nQ{q}:')
    print(f'  BL:    {b[:150]}')
    print(f'  Letta: {l[:150]}')

# Also check if qid 27 was the mismatch
print('\n\nSpecific Q27 check:')
for r in bl:
    if r['question_id'] == 27:
        print(f'BL Q27 text: {r["question_text"]}')
        if 'responses' in r:
            c2a = r['responses'].get('C2a_full_spec', {}).get('text','')
            print(f'C2a text first 300: {c2a[:300]}')

for r in letta:
    if r['question_id'] == 27:
        print(f'LETTA Q27 text: {r["question_text"]}')
