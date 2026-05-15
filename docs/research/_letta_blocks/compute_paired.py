import json, os, sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parents[3]
# This script also depends on the separate memory_system repo; set MEMORY_SYSTEM_ROOT to its path.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
MS_RESULTS = os.path.join(MEMORY_SYSTEM_ROOT, 'data/experiments/memory_systems/results')

def load_letta_memory_scores(subj_dir):
    judges = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']
    by_qid = defaultdict(dict)
    for judge in judges:
        p = subj_dir + f'letta_memory_haiku_judgments_{judge}.json'
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if isinstance(d, list):
            for item in d:
                s = item.get('score')
                if s is not None and not item.get('parse_failure'):
                    by_qid[item['question_id']][judge] = s
    return by_qid

def load_bl_scores(bl_paths, cond):
    by_qid = defaultdict(dict)
    for path in bl_paths:
        if not os.path.exists(path): continue
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if isinstance(d, list):
            for item in d:
                if item.get('condition') == cond and not item.get('parse_failure'):
                    qid = item.get('question_id')
                    if item.get('score') is not None:
                        j = item.get('judge')
                        if j:
                            by_qid[qid][j] = item['score']
                    # For hamerton style (haiku_score / gemini_score)
                    if 'haiku_score' in item and item.get('haiku_score') is not None:
                        by_qid[qid]['haiku'] = item['haiku_score']
                    if 'gemini_score' in item and item.get('gemini_score') is not None:
                        by_qid[qid]['gemini_flash'] = item['gemini_score']
    return by_qid

hamerton = {
    'letta_dir': os.path.join(MS_RESULTS, 'run_fullstack_hamerton_20260411_231237') + os.sep,
    'bl_paths': [
        str(REPO / 'results/hamerton/judgments.json'),
        str(REPO / 'results/hamerton/gemini_pro_judgments.json'),
        str(REPO / 'results/hamerton/gpt54_judgments.json'),
    ],
}
ebers = {
    'letta_dir': os.path.join(MS_RESULTS, 'global_ebers') + os.sep,
    'bl_paths': [str(REPO / 'results/global_ebers/judgments_v2.json')],
}
babur = {
    'letta_dir': os.path.join(MS_RESULTS, 'global_babur') + os.sep,
    'bl_paths': [str(REPO / 'results/global_babur/judgments_v2.json')],
}

subjects = [('hamerton', hamerton, 'C2a_full_spec'), ('ebers', ebers, 'C2a_full_spec'), ('babur', babur, 'C2a_full_spec')]

results = {}
for subj_name, cfg, cond in subjects:
    letta = load_letta_memory_scores(cfg['letta_dir'])
    bl = load_bl_scores(cfg['bl_paths'], cond)
    all_judges_letta = set()
    for qs in letta.values():
        all_judges_letta.update(qs.keys())
    all_judges_bl = set()
    for qs in bl.values():
        all_judges_bl.update(qs.keys())
    common = all_judges_letta & all_judges_bl
    print(f'=== {subj_name} ===')
    print(f'  Letta judges seen: {sorted(all_judges_letta)}')
    print(f'  BL judges seen: {sorted(all_judges_bl)}')
    print(f'  Common judges: {sorted(common)}')
    letta_mean = {}
    bl_mean = {}
    for qid, js in letta.items():
        s = [v for j, v in js.items() if j in common]
        if s:
            letta_mean[qid] = sum(s)/len(s)
    for qid, js in bl.items():
        s = [v for j, v in js.items() if j in common]
        if s:
            bl_mean[qid] = sum(s)/len(s)
    qids_both = set(letta_mean) & set(bl_mean)
    print(f'  Questions with both: {len(qids_both)}')
    if not qids_both:
        continue
    l_agg = sum(letta_mean[q] for q in qids_both)/len(qids_both)
    b_agg = sum(bl_mean[q] for q in qids_both)/len(qids_both)
    print(f'  Letta stateful+Haiku mean: {l_agg:.3f}')
    print(f'  BL C2a+Haiku mean: {b_agg:.3f}')
    print(f'  Delta (Letta - BL): {l_agg - b_agg:+.3f}')
    sorted_qids = sorted(qids_both, key=lambda q: letta_mean[q] - bl_mean[q], reverse=True)
    print(f'  Top 8 Letta > BL:')
    for qid in sorted_qids[:8]:
        print(f'    Q{qid}: Letta={letta_mean[qid]:.2f}, BL={bl_mean[qid]:.2f}, delta=+{letta_mean[qid]-bl_mean[qid]:.2f}')
    print(f'  Top 8 BL > Letta:')
    for qid in sorted_qids[-8:][::-1]:
        print(f'    Q{qid}: Letta={letta_mean[qid]:.2f}, BL={bl_mean[qid]:.2f}, delta={letta_mean[qid]-bl_mean[qid]:+.2f}')
    # Save mean data
    results[subj_name] = {
        'letta_mean_per_q': letta_mean,
        'bl_mean_per_q': bl_mean,
        'common_judges': sorted(common),
        'letta_agg': l_agg,
        'bl_agg': b_agg,
        'sorted_by_delta': [(q, letta_mean[q], bl_mean[q], letta_mean[q]-bl_mean[q]) for q in sorted_qids],
    }
    print()

# Save
with open(str(REPO / 'docs/research/_letta_blocks/paired_scores.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, default=str)
print('Saved paired_scores.json')
