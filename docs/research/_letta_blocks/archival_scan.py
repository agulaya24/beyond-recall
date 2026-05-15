import json, sys
from collections import defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parents[3]

# Letta archival pipeline: C1_letta (retrieval only) vs C3_letta (retrieval + spec)
# Per-question swing analysis on Ebers + Hamerton (paper says Ebers Δ=+0.6%, Hamerton Δ=+11.7%)

def load_per_q_scores(path, cond_filter=None):
    """Load per-question, per-judge scores."""
    by_cond = defaultdict(lambda: defaultdict(dict))  # cond -> qid -> judge -> score
    with open(path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    if isinstance(d, list):
        for item in d:
            cond = item.get('condition')
            if cond_filter and cond not in cond_filter: continue
            if item.get('parse_failure') or item.get('score') is None: continue
            qid = item.get('question_id')
            judge = item.get('judge')
            if judge:
                by_cond[cond][qid][judge] = item['score']
    return by_cond

def per_q_means(by_cond):
    """cond -> qid -> mean_across_judges."""
    means = {}
    for cond, qmap in by_cond.items():
        means[cond] = {}
        for qid, judges in qmap.items():
            if judges:
                means[cond][qid] = sum(judges.values())/len(judges)
    return means

# Hamerton
h_path = str(REPO / 'results/hamerton/letta_fullpipeline_judgments_merged.json')
h_bc = load_per_q_scores(h_path)
h_means = per_q_means(h_bc)
print('Hamerton conditions in letta_fullpipeline:', list(h_means.keys()))
# find all conds
h_c1 = [c for c in h_means if 'C1' in c or 'c1' in c]
h_c3 = [c for c in h_means if 'C3' in c or 'c3' in c]
print('H C1 candidates:', h_c1, 'C3:', h_c3)

# Ebers
e_path = str(REPO / 'results/global_ebers/letta_fullpipeline_judgments_merged.json')
e_bc = load_per_q_scores(e_path)
e_means = per_q_means(e_bc)
print('Ebers conditions:', list(e_means.keys()))

# compute aggregate means and per-q swings
for name, means in [('HAMERTON', h_means), ('EBERS', e_means)]:
    print(f'\n=== {name} letta_fullpipeline ===')
    # aggregate
    for cond, qmap in means.items():
        vals = list(qmap.values())
        print(f'  {cond}: n={len(vals)} mean={sum(vals)/max(1,len(vals)):.3f}')
    # find C1/C3 pair
    conds = list(means.keys())
    if len(conds) >= 2:
        # Assume one is "_c1" and one is "_c3" or similar
        c1 = [c for c in conds if 'c1' in c.lower()]
        c3 = [c for c in conds if 'c3' in c.lower()]
        if c1 and c3:
            c1n, c3n = c1[0], c3[0]
            qids = sorted(set(means[c1n]) & set(means[c3n]))
            print(f'  Pair: {c1n} vs {c3n}, {len(qids)} common qids')
            swings = []
            for q in qids:
                delta = means[c3n][q] - means[c1n][q]
                swings.append((q, means[c1n][q], means[c3n][q], delta))
            swings.sort(key=lambda x: x[3])
            print(f'  Agg C1={sum(s[1] for s in swings)/len(swings):.3f}, C3={sum(s[2] for s in swings)/len(swings):.3f}, Δ={sum(s[3] for s in swings)/len(swings):+.3f}')
            # C3 > C1 by > 0.5
            high_pos = [s for s in swings if s[3] > 0.5]
            high_neg = [s for s in swings if s[3] < -0.5]
            print(f'  C3 > C1 by >0.5: {len(high_pos)} questions')
            print(f'  C1 > C3 by >0.5: {len(high_neg)} questions')
            print(f'  Biggest C3>>C1:')
            for s in swings[-5:][::-1]:
                print(f'    Q{s[0]}: C1={s[1]:.2f}, C3={s[2]:.2f}, Δ=+{s[3]:.2f}')
            print(f'  Biggest C1>>C3:')
            for s in swings[:5]:
                print(f'    Q{s[0]}: C1={s[1]:.2f}, C3={s[2]:.2f}, Δ={s[3]:+.2f}')
