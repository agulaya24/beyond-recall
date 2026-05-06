"""Probe which classifier variant yields 127/13/3 for C5/C2a/C4a."""
import json
import os
import re

BASE = 'C:/Users/Aarik/Anthropic/memory-study-repo/results'
GLOBALS = ['augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers', 'equiano',
           'fukuzawa', 'keckley', 'rousseau', 'seacole', 'sunity_devee',
           'yung_wing', 'zitkala_sa']

REFUSAL_PATTERNS_A = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
# Expanded list (try adding phrases that draft v6 §5.4 mentions)
REFUSAL_PATTERNS_B = REFUSAL_PATTERNS_A + [
    r"\bcannot definitively\b",
    r"\bdon.?t have enough (?:context|information)\b",
    r"\bdifficult to predict\b",
    r"\bwould depend on many factors\b",
    r"\bwithout speculating\b",
    r"\bI don.?t know\b",
    r"\binsufficient (?:information|context|facts|data)\b",
    r"\bnot enough (?:information|context)\b",
    r"\bwithout more\b",
]

START_RE = re.compile(r"^\s*(?:I (?:cannot|can't|don't)|The retrieved facts (?:do not|don't))", re.IGNORECASE)


def build_re(patterns):
    return re.compile("|".join(patterns), re.IGNORECASE)


CONDS = ['C5_baseline', 'C2a_full_spec', 'C4a_full_facts_plus_spec']
all_texts = {c: [] for c in CONDS}
for subj in GLOBALS:
    path = os.path.join(BASE, f'global_{subj}', 'results_v2.json')
    recs = json.load(open(path, encoding='utf-8'))
    for rec in recs:
        for c in CONDS:
            r = rec.get('responses', {}).get(c)
            if r is None:
                continue
            t = r.get('text', '') if isinstance(r, dict) else str(r)
            all_texts[c].append(t)

ref_a = build_re(REFUSAL_PATTERNS_A)
ref_b = build_re(REFUSAL_PATTERNS_B)

variants = {
    'A:refusal_ge_1': lambda t: len(ref_a.findall(t)) >= 1,
    'A:refusal_ge_2': lambda t: len(ref_a.findall(t)) >= 2,
    'A:starts_refusal': lambda t: bool(START_RE.match(t)),
    'A:starts_or_ref_ge_2': lambda t: bool(START_RE.match(t)) or len(ref_a.findall(t)) >= 2,
    'A:starts_and_ref_ge_2': lambda t: bool(START_RE.match(t)) and len(ref_a.findall(t)) >= 2,
    'B:refusal_ge_1': lambda t: len(ref_b.findall(t)) >= 1,
    'B:refusal_ge_2': lambda t: len(ref_b.findall(t)) >= 2,
    'B:refusal_ge_3': lambda t: len(ref_b.findall(t)) >= 3,
    'B:refusal_ge_4': lambda t: len(ref_b.findall(t)) >= 4,
    'B:starts_refusal': lambda t: bool(START_RE.match(t)),
    'B:starts_or_ref_ge_3': lambda t: bool(START_RE.match(t)) or len(ref_b.findall(t)) >= 3,
    'B:starts_and_ref_ge_1': lambda t: bool(START_RE.match(t)) and len(ref_b.findall(t)) >= 1,
}

print(f'{"variant":<34} {"C5":>8} {"C2a":>8} {"C4a":>8}  target: 127/13/3')
for name, fn in variants.items():
    counts = [sum(1 for t in all_texts[c] if fn(t)) for c in CONDS]
    totals = [len(all_texts[c]) for c in CONDS]
    print(f'{name:<34} {counts[0]:>4}/{totals[0]:<3} {counts[1]:>4}/{totals[1]:<3} {counts[2]:>4}/{totals[2]:<3}')

# Also try: response length-based (very short responses that are just refusals)
def short_refusal(t, max_words=200):
    if len(t.split()) > max_words: return False
    return bool(START_RE.match(t)) or len(ref_b.findall(t)) >= 1

print('\n--- length-constrained variants ---')
for mw in (100, 150, 200, 300, 500):
    counts = [sum(1 for t in all_texts[c] if short_refusal(t, mw)) for c in CONDS]
    print(f'short_refusal (<= {mw} words): {counts[0]}/{counts[1]}/{counts[2]}')

# Also try: refusal fraction by word count (≥5% of text is refusal phrases)
print('\n--- refusal density ---')
def density(t, min_hits=1, min_rate=0.0):
    w = max(1, len(t.split()))
    hits = len(ref_b.findall(t))
    return hits >= min_hits and hits / w * 100 >= min_rate
for rate in (0.5, 1.0, 2.0, 3.0):
    counts = [sum(1 for t in all_texts[c] if density(t, 1, rate)) for c in CONDS]
    print(f'density >= {rate}% ref hits: {counts[0]}/{counts[1]}/{counts[2]}')
