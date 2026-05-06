import json
from pathlib import Path
D = Path('C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton')
for f in ['judgments.json','gpt4o_judgments.json','gpt54_judgments.json',
          'gemini_pro_judgments.json','opus_judgments.json','sonnet_judgments.json']:
    d = json.load(open(D/f))
    print(f, list(d[0].keys()))
    print('  sample:', d[0])
