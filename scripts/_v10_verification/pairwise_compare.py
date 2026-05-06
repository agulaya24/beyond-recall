"""§4.2.1 pairwise comparison table on low-baseline slice."""
import sys
from pathlib import Path
REPO = Path('C:/Users/Aarik/Anthropic/memory-study-repo')
sys.path.insert(0, str(REPO / 'scripts'))
from _compute_per_question_v2 import per_question_means, CONDITION_MAP

LOW_9 = ['sunity_devee', 'ebers', 'hamerton', 'fukuzawa', 'bernal_diaz',
         'babur', 'seacole', 'keckley', 'yung_wing']

def pairwise(a, b):
    a_higher = b_higher = tie = 0
    for subj in LOW_9:
        means = per_question_means(subj)
        a_qids = {q for (c, q) in means if c == a}
        b_qids = {q for (c, q) in means if c == b}
        qids = a_qids & b_qids
        for qid in qids:
            va = means[(a, qid)]
            vb = means[(b, qid)]
            if va > vb + 1e-9:
                a_higher += 1
            elif vb > va + 1e-9:
                b_higher += 1
            else:
                tie += 1
    total = a_higher + b_higher + tie
    print(f'  {a} vs {b}: {a}_higher={a_higher} ({100*a_higher/total:.1f}%), tie={tie}, {b}_higher={b_higher} ({100*b_higher/total:.1f}%); n={total}')

print('=== Pairwise comparison at question level (low-baseline slice) ===')
pairwise('C8', 'C2a')
pairwise('C9', 'C4a')

# Paper line 845: "Raw corpus (C8) vs. spec alone (C2a) | 190 (54.1%) | 46 | 115 (32.8%)"
# Paper line 846: "Corpus + spec (C9) vs. facts + spec (C4a) | 155 (49.7%) | 42 | 115 (36.9%)"
