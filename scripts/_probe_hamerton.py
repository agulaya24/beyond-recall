import json
from collections import Counter
from pathlib import Path

D = Path('C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton')

for fname in ['judgments.json', 'gpt4o_judgments.json', 'gpt54_judgments.json',
              'gemini_pro_judgments.json', 'judgments_harmonized.json',
              'c8_c9_judgments_merged.json', 'opus_judgments.json',
              'sonnet_judgments.json']:
    fp = D / fname
    if not fp.exists():
        print(f'{fname}: MISSING')
        continue
    data = json.load(open(fp))
    judges = sorted(set(x.get('judge') for x in data))
    conds = sorted(set(x.get('condition') for x in data))
    print(f'{fname}: n={len(data)} judges={judges} conds={conds}')
