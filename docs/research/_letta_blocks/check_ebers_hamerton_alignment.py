import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Ebers
p1 = 'C:/Users/Aarik/Anthropic/memory-study-repo/results/global_ebers/results_v2.json'
p2 = 'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_ebers/letta_memory_haiku_results.json'
with open(p1, 'r', encoding='utf-8') as f:
    bl = json.load(f)
with open(p2, 'r', encoding='utf-8') as f:
    letta = json.load(f)['results']
bl_map = {r['question_id']: r['question_text'] for r in bl}
letta_map = {r['question_id']: r['question_text'] for r in letta}
common = sorted(set(bl_map) & set(letta_map))
mismatches = [(q, bl_map[q], letta_map[q]) for q in common if bl_map[q] != letta_map[q]]
print(f'EBERS: {len(common)} common qids, {len(mismatches)} mismatches')
if mismatches:
    for q, b, l in mismatches[:5]:
        print(f'  Q{q}: BL="{b[:80]}" | Letta="{l[:80]}"')

# Hamerton
p1 = 'C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton/fullstack_haiku.json'
p2 = 'C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/run_fullstack_hamerton_20260411_231237/letta_memory_haiku_results.json'
with open(p1, 'r', encoding='utf-8') as f:
    bl = json.load(f)
with open(p2, 'r', encoding='utf-8') as f:
    letta = json.load(f)['results']
bl_map = {r['question_id']: r['question_text'] for r in bl}
letta_map = {r['question_id']: r['question_text'] for r in letta}
common = sorted(set(bl_map) & set(letta_map))
mismatches = [(q, bl_map[q], letta_map[q]) for q in common if bl_map[q] != letta_map[q]]
print(f'\nHAMERTON: {len(common)} common qids, {len(mismatches)} mismatches')
if mismatches:
    for q, b, l in mismatches[:5]:
        print(f'  Q{q}: BL="{b[:80]}" | Letta="{l[:80]}"')
else:
    print('  All questions match!')
