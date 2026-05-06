"""
Stats add-on for top-K sensitivity test.

Computes:
- Paired Wilcoxon signed-rank on per-question 5-judge means (C3'-C1') for each K
- Paired Wilcoxon signed-rank on (Delta_K10 - Delta_K140) per-question to test
  whether K=10 Delta differs from K=140 Delta
- Same for K=10 vs K=50, and K=50 vs K=140
- Sign test (counts only) for context

Reads:
    data/topk_test_20260428/_summary.json
"""
import json
from scipy import stats

OUT_DIR = 'C:/Users/Aarik/Anthropic/memory-study-repo/data/topk_test_20260428'

with open(f'{OUT_DIR}/_summary.json', encoding='utf-8') as f:
    summary = json.load(f)

# Per-question deltas at each K
deltas_by_k = {}
for k_str, qmap in summary['per_q_means_per_k'].items():
    k = int(k_str)
    deltas = []
    for qid, scores in qmap.items():
        c1 = scores.get('c1')
        c3 = scores.get('c3')
        if c1 is None or c3 is None:
            continue
        deltas.append((int(qid), c3 - c1))
    deltas_by_k[k] = deltas

# Per-K Wilcoxon: H0 = median of per-question delta is 0
print('=== Per-K paired Wilcoxon signed-rank (median per-q delta == 0) ===')
for k in [10, 50, 140]:
    diffs = [d for _, d in deltas_by_k[k]]
    n = len(diffs)
    n_pos = sum(1 for d in diffs if d > 0)
    n_neg = sum(1 for d in diffs if d < 0)
    n_zero = sum(1 for d in diffs if d == 0)
    try:
        stat, p = stats.wilcoxon([d for d in diffs if d != 0])
    except ValueError as e:
        stat, p = None, None
    median = sorted(diffs)[n // 2]
    mean = sum(diffs) / n
    print(f'  K={k:3d}: n={n}, mean delta={mean:+.3f}, median={median:+.3f}, '
          f'pos={n_pos}, neg={n_neg}, zero={n_zero}, '
          f'W={stat}, p={p:.4f}' if p is not None
          else f'  K={k}: zero diffs')

# Cross-K Wilcoxon: paired on per-question delta values across K
print('\n=== Cross-K paired Wilcoxon (does Delta change as K changes?) ===')
for ka, kb in [(10, 50), (50, 140), (10, 140)]:
    da = dict(deltas_by_k[ka])
    db = dict(deltas_by_k[kb])
    common = sorted(set(da.keys()) & set(db.keys()))
    paired_a = [da[q] for q in common]
    paired_b = [db[q] for q in common]
    diffs = [a - b for a, b in zip(paired_a, paired_b)]
    nz = [d for d in diffs if d != 0]
    if not nz:
        print(f'  K={ka} vs K={kb}: all diffs zero')
        continue
    stat, p = stats.wilcoxon(nz)
    mean_a = sum(paired_a) / len(paired_a)
    mean_b = sum(paired_b) / len(paired_b)
    print(f'  K={ka} vs K={kb}: n_paired={len(common)}, '
          f'mean_delta_K{ka}={mean_a:+.3f}, mean_delta_K{kb}={mean_b:+.3f}, '
          f'W={stat:.1f}, p={p:.4f}')

# Bonus: trend test on C1' across K (does C1' rise with K?)
print('\n=== C1\' trajectory paired tests (does C1\' rise with K?) ===')
c1_by_q_k = {}
for k_str, qmap in summary['per_q_means_per_k'].items():
    k = int(k_str)
    for qid, scores in qmap.items():
        c1_by_q_k.setdefault(int(qid), {})[k] = scores.get('c1')

for ka, kb in [(10, 50), (50, 140), (10, 140)]:
    paired = [(c1_by_q_k[q][ka], c1_by_q_k[q][kb])
              for q in c1_by_q_k
              if c1_by_q_k[q].get(ka) is not None and c1_by_q_k[q].get(kb) is not None]
    diffs = [b - a for a, b in paired]  # positive => C1 rose K_a -> K_b
    nz = [d for d in diffs if d != 0]
    if nz:
        stat, p = stats.wilcoxon(nz)
        print(f'  C1\' K={ka}->K={kb}: n={len(paired)}, '
              f'mean_change={sum(diffs)/len(diffs):+.3f}, '
              f'W={stat:.1f}, p={p:.4f}')

print('\n=== C3\' trajectory paired tests (does C3\' shift with K?) ===')
c3_by_q_k = {}
for k_str, qmap in summary['per_q_means_per_k'].items():
    k = int(k_str)
    for qid, scores in qmap.items():
        c3_by_q_k.setdefault(int(qid), {})[k] = scores.get('c3')

for ka, kb in [(10, 50), (50, 140), (10, 140)]:
    paired = [(c3_by_q_k[q][ka], c3_by_q_k[q][kb])
              for q in c3_by_q_k
              if c3_by_q_k[q].get(ka) is not None and c3_by_q_k[q].get(kb) is not None]
    diffs = [b - a for a, b in paired]
    nz = [d for d in diffs if d != 0]
    if nz:
        stat, p = stats.wilcoxon(nz)
        print(f'  C3\' K={ka}->K={kb}: n={len(paired)}, '
              f'mean_change={sum(diffs)/len(diffs):+.3f}, '
              f'W={stat:.1f}, p={p:.4f}')

# Save stats summary
out = {
    'per_k_wilcoxon_delta_vs_zero': {},
    'cross_k_wilcoxon_delta_diff': {},
}
for k in [10, 50, 140]:
    diffs = [d for _, d in deltas_by_k[k]]
    nz = [d for d in diffs if d != 0]
    stat, p = stats.wilcoxon(nz)
    out['per_k_wilcoxon_delta_vs_zero'][str(k)] = {
        'n': len(diffs), 'n_nonzero': len(nz),
        'mean_delta': sum(diffs) / len(diffs),
        'W': float(stat), 'p_value': float(p),
        'pos': sum(1 for d in diffs if d > 0),
        'neg': sum(1 for d in diffs if d < 0),
        'zero': sum(1 for d in diffs if d == 0),
    }
for ka, kb in [(10, 50), (50, 140), (10, 140)]:
    da = dict(deltas_by_k[ka])
    db = dict(deltas_by_k[kb])
    common = sorted(set(da.keys()) & set(db.keys()))
    paired_a = [da[q] for q in common]
    paired_b = [db[q] for q in common]
    diffs = [a - b for a, b in zip(paired_a, paired_b)]
    nz = [d for d in diffs if d != 0]
    stat, p = stats.wilcoxon(nz)
    out['cross_k_wilcoxon_delta_diff'][f'K{ka}_vs_K{kb}'] = {
        'n_paired': len(common),
        'mean_delta_Ka': sum(paired_a) / len(paired_a),
        'mean_delta_Kb': sum(paired_b) / len(paired_b),
        'W': float(stat), 'p_value': float(p),
    }

with open(f'{OUT_DIR}/_stats.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)
print(f'\nSaved stats to {OUT_DIR}/_stats.json')
