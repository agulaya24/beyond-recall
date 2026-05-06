import json
with open('results/global_babur/supermemory_judgments_merged.json') as f:
    j = json.load(f)
judge_counts = {}
for x in j:
    key = (x['condition'], x['judge'])
    judge_counts[key] = judge_counts.get(key, 0) + 1
for k,v in sorted(judge_counts.items()):
    print(k, v)
print()
# Check a specific qid
by_qid = {}
for x in j:
    by_qid.setdefault(x['question_id'], []).append(x)
print('qid 1 judgments:')
for row in by_qid[1]:
    print(' ', row['condition'], row['judge'], row['score'], 'parse_fail:', row.get('parse_failure'))
