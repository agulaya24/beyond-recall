import json
from pathlib import Path
D = Path('C:/Users/Aarik/Anthropic/memory-study-repo/results/hamerton')
d = json.load(open(D/'judgments.json'))
print('judgments.json sample:', d[0])
print('has judge field?', 'judge' in d[0])
print('has response_model?', 'response_model' in d[0])
print('keys:', list(d[0].keys()))
