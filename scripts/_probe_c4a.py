"""Check which subject is missing C4a data."""
import json
from pathlib import Path
from collections import Counter

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compute_per_question_v2 import per_question_means, SUBJECTS

for subj in SUBJECTS:
    m = per_question_means(subj)
    c5_q = {q for (c,q) in m if c=='C5'}
    c2a_q = {q for (c,q) in m if c=='C2a'}
    c4_q = {q for (c,q) in m if c=='C4'}
    c4a_q = {q for (c,q) in m if c=='C4a'}
    c8_q = {q for (c,q) in m if c=='C8'}
    c9_q = {q for (c,q) in m if c=='C9'}
    print(f'{subj}: C5={len(c5_q)} C2a={len(c2a_q)} C4={len(c4_q)} C4a={len(c4a_q)} C8={len(c8_q)} C9={len(c9_q)}')
