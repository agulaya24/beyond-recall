"""Find what subset of judges produces BL Q21 = (2.0, 0.6) for (C1, C3)."""
from itertools import combinations

c1_scores = {'haiku': 5, 'sonnet': 2, 'opus': 3, 'gpt4o': 3, 'gpt54': 4, 'gemini_flash': None, 'gemini_pro': None}
c3_scores = {'haiku': 1, 'sonnet': 1, 'opus': 1, 'gpt4o': 2, 'gpt54': 1, 'gemini_flash': None, 'gemini_pro': None}

valid_judges = [j for j in c1_scores if c1_scores[j] is not None and c3_scores[j] is not None]

print(f'Valid judges: {valid_judges}')
print(f'Target: C1=2.0, C3=0.6')
print()

for n in range(2, len(valid_judges)+1):
    for subset in combinations(valid_judges, n):
        c1 = sum(c1_scores[j] for j in subset) / n
        c3 = sum(c3_scores[j] for j in subset) / n
        # check round(c1*5)/5 == 2.0 etc (within 0.05 due to paper rounding)
        if abs(c1 - 2.0) < 0.1 and abs(c3 - 0.6) < 0.1:
            print(f'MATCH n={n}: {subset} -> C1={c1:.3f}, C3={c3:.3f}, delta={c3-c1:+.3f}')

# Maybe paper uses a different scoring (e.g., scale starts at 0)?
print('\nWith score-1 transform (1-5 scale shifted to 0-4):')
for n in range(2, len(valid_judges)+1):
    for subset in combinations(valid_judges, n):
        c1 = sum(c1_scores[j]-1 for j in subset) / n
        c3 = sum(c3_scores[j]-1 for j in subset) / n
        if abs(c1 - 2.0) < 0.1 and abs(c3 - 0.6) < 0.1:
            print(f'MATCH (shifted) n={n}: {subset} -> C1={c1:.3f}, C3={c3:.3f}, delta={c3-c1:+.3f}')

# Maybe used summary across questions instead of per-question?
print('\nNote: Q21 BL paper says C1=2.0/C3=0.6 with footnote "covers 3 judges (Haiku, Sonnet, Opus)"')
print('  haiku/sonnet/opus C1: ', [c1_scores[j] for j in ['haiku','sonnet','opus']])
print('  haiku/sonnet/opus C3: ', [c3_scores[j] for j in ['haiku','sonnet','opus']])
