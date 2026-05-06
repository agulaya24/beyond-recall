"""
Aggregate top-K sensitivity test results into per-K summaries.

Reads:
    data/topk_test_20260428/yung_wing_K{K}_judgments.json
    data/topk_test_20260428/yung_wing_K{K}_retrieval.json
    results/global_yung_wing/baselayer_judgments_merged.json (canonical paper K=10)

Writes:
    data/topk_test_20260428/_summary.json

Prints aggregates to stdout.
"""
import json
import os

OUT_DIR = 'C:/Users/Aarik/Anthropic/memory-study-repo/data/topk_test_20260428'
PRIMARY = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}


def aggregate(k):
    jp = f'{OUT_DIR}/yung_wing_K{k}_judgments.json'
    rp = f'{OUT_DIR}/yung_wing_K{k}_retrieval.json'
    judgments = json.load(open(jp, encoding='utf-8'))

    parse_fails = sum(1 for r in judgments if r.get('parse_failure'))
    coverage = {j: 0 for j in PRIMARY}
    for r in judgments:
        if r['judge'] in PRIMARY and not r.get('parse_failure'):
            coverage[r['judge']] += 1

    c1_scores = [r['score'] for r in judgments
                 if r['condition'] == 'C1_prime' and r['judge'] in PRIMARY
                 and r['score'] > 0]
    c3_scores = [r['score'] for r in judgments
                 if r['condition'] == 'C3_prime' and r['judge'] in PRIMARY
                 and r['score'] > 0]

    c1_mean = sum(c1_scores) / len(c1_scores) if c1_scores else 0
    c3_mean = sum(c3_scores) / len(c3_scores) if c3_scores else 0

    # Per-question 5-judge means
    per_q = {}
    for r in judgments:
        if r['judge'] not in PRIMARY or r['score'] == 0:
            continue
        qid = r['question_id']
        cond = r['condition']
        per_q.setdefault(qid, {}).setdefault(cond, []).append(r['score'])

    per_q_means = {}
    for qid, conds in per_q.items():
        c1m = (sum(conds['C1_prime']) / len(conds['C1_prime'])
               if conds.get('C1_prime') else None)
        c3m = (sum(conds['C3_prime']) / len(conds['C3_prime'])
               if conds.get('C3_prime') else None)
        per_q_means[qid] = (c1m, c3m)

    # Movement breakdown (paired per-question, threshold +/- 0.1)
    up = down = none = 0
    for qid, (c1, c3) in per_q_means.items():
        if c1 is None or c3 is None:
            continue
        diff = c3 - c1
        if diff > 0.1:
            up += 1
        elif diff < -0.1:
            down += 1
        else:
            none += 1

    # Anchor crossings: 5-judge mean crosses 3.0 threshold
    crosses_up = crosses_down = 0
    for qid, (c1, c3) in per_q_means.items():
        if c1 is None or c3 is None:
            continue
        if c1 < 3.0 <= c3:
            crosses_up += 1
        elif c3 < 3.0 <= c1:
            crosses_down += 1

    # Context tokens
    retrieval = json.load(open(rp, encoding='utf-8'))
    toks = [r['context_tokens_cl100k'] for r in retrieval.values()]
    avg_tok = sum(toks) / len(toks)

    return {
        'k': k,
        'k_actual': retrieval[list(retrieval.keys())[0]]['k_actual'],
        'avg_ctx_tokens': avg_tok,
        'min_ctx_tokens': min(toks),
        'max_ctx_tokens': max(toks),
        'c1_mean': c1_mean,
        'c3_mean': c3_mean,
        'delta': c3_mean - c1_mean,
        'c1_n': len(c1_scores),
        'c3_n': len(c3_scores),
        'parse_fails': parse_fails,
        'coverage': coverage,
        'movement_up': up,
        'movement_down': down,
        'movement_none': none,
        'anchor_crossings_up': crosses_up,
        'anchor_crossings_down': crosses_down,
        'per_q_means': per_q_means,
    }


def main():
    results = {}
    for k in [10, 50, 140]:
        results[k] = aggregate(k)
        r = results[k]
        print(f"K={k} (k_actual={r['k_actual']}): "
              f"ctx_tok_avg={r['avg_ctx_tokens']:.0f}  "
              f"C1={r['c1_mean']:.3f}  C3={r['c3_mean']:.3f}  "
              f"delta={r['delta']:+.3f}")
        print(f"   N: C1={r['c1_n']}, C3={r['c3_n']}, parse_fails={r['parse_fails']}, "
              f"coverage={r['coverage']}")
        print(f"   per-q movement (threshold +/-0.1): "
              f"up={r['movement_up']} down={r['movement_down']} none={r['movement_none']}")
        print(f"   anchor crossings (5-judge mean crosses 3.0): "
              f"up={r['anchor_crossings_up']} down={r['anchor_crossings_down']}")

    # Canonical paper K=10 reference
    canonical = json.load(open(
        'C:/Users/Aarik/Anthropic/memory-study-repo/results/global_yung_wing/'
        'baselayer_judgments_merged.json', encoding='utf-8'))
    c1c = [r['score'] for r in canonical
           if r['condition'] == 'C1_baselayer' and r['judge'] in PRIMARY
           and r['score'] > 0]
    c3c = [r['score'] for r in canonical
           if r['condition'] == 'C3_baselayer' and r['judge'] in PRIMARY
           and r['score'] > 0]
    cano_c1 = sum(c1c) / len(c1c)
    cano_c3 = sum(c3c) / len(c3c)
    print(f"\nCanonical paper K=10 (5-judge primary): "
          f"C1={cano_c1:.3f} (n={len(c1c)})  "
          f"C3={cano_c3:.3f} (n={len(c3c)})  "
          f"delta={cano_c3 - cano_c1:+.3f}")

    out = {
        'subject': 'yung_wing',
        'judges': sorted(PRIMARY),
        'k_values': sorted(results.keys()),
        'fact_pool_size': 747,
        'spec_chars': 36793,
        'spec_tokens_cl100k_estimate': 9198,
        'per_k': {str(k): {kk: vv for kk, vv in v.items() if kk != 'per_q_means'}
                  for k, v in results.items()},
        'per_q_means_per_k': {
            str(k): {str(qid): {'c1': c1, 'c3': c3}
                     for qid, (c1, c3) in v['per_q_means'].items()}
            for k, v in results.items()
        },
        'canonical_k10_paper': {
            'c1': cano_c1, 'c3': cano_c3, 'delta': cano_c3 - cano_c1,
            'c1_n': len(c1c), 'c3_n': len(c3c),
            'note': '5-judge primary recompute on canonical Yung Wing baselayer run',
        },
    }
    with open(f'{OUT_DIR}/_summary.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print('\nSaved summary to', f'{OUT_DIR}/_summary.json')


if __name__ == '__main__':
    main()
