"""Determine which wrong-spec is in judgments_v2.json (v1 vs v2),
and compute the v2 random derangement deltas from _wrong_spec_v2/."""
import json
import statistics
from pathlib import Path
from collections import defaultdict
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from recompute_5judge_primary import (
    load_global_judgments, load_hamerton_judgments,
    PRIMARY_JUDGES, ALL_JUDGES,
    aggregate_per_subject_per_condition,
    GLOBAL_SUBJECTS, MAIN_STUDY,
)

ROOT = Path(__file__).resolve().parents[2]

# Inspect the wrong_spec_v2 manifest
print('=== wrong_spec_v2 manifest ===')
manifest_path = ROOT / 'results/_wrong_spec_v2/wrong_spec_v2_manifest.json'
with open(manifest_path) as f:
    m = json.load(f)
print(json.dumps(m, indent=2)[:3000])

# Now load v2 wrong-spec for each global, compute 5-judge primary mean per subject
print('\n=== v2 (random derangement) deltas vs C5 ===')
deltas_v2 = []
deltas_v2_per_subject = {}
for subject in GLOBAL_SUBJECTS:
    rows = []
    base = ROOT / f'results/_wrong_spec_v2/global_{subject}'
    for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']:
        p = base / f'wrong_spec_v2_judgments_{j}.json'
        if not p.exists():
            print(f'  MISSING {p}')
            continue
        with open(p) as f:
            d = json.load(f)
        for r in d:
            if isinstance(r, dict):
                rows.append({
                    'question_id': r.get('question_id'),
                    'condition': r.get('condition', 'C2c_wrong_spec_v2'),
                    'judge': j,
                    'score': r.get('score'),
                    'parse_failure': r.get('parse_failure', False),
                })
    if not rows:
        continue
    # Get this subject's C5 from regular global judgments
    main_rows = load_global_judgments(subject)
    main_means = aggregate_per_subject_per_condition(main_rows, PRIMARY_JUDGES)
    c5 = main_means.get('C5_baseline')

    v2_means = aggregate_per_subject_per_condition(rows, PRIMARY_JUDGES)
    # v2 condition might be named differently per file - use whichever condition we found
    if not v2_means:
        continue
    # Take the most common condition name
    cond_names = list(v2_means.keys())
    v2_score = list(v2_means.values())[0]  # there should only be one cond

    delta = v2_score - c5
    deltas_v2.append(delta)
    deltas_v2_per_subject[subject] = {'c5': c5, 'v2': v2_score, 'delta': delta, 'cond_names': cond_names}
    print(f'  {subject:<15} C5={c5:.3f} v2={v2_score:.3f} delta={delta:+.3f}  conds={cond_names}')

print(f'\nMean v2 delta (n={len(deltas_v2)}): {statistics.mean(deltas_v2):+.4f} (paper claims +0.22)')

# Also v2 7-judge (PRIMARY + GEMINI_FLASH at minimum, GEMINI_PRO where avail)
print('\n=== v2 (random derangement) 7-judge deltas vs C5 ===')
ALL_J = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro'}
deltas_v2_7j = []
for subject in GLOBAL_SUBJECTS:
    rows = []
    base = ROOT / f'results/_wrong_spec_v2/global_{subject}'
    for j in ALL_J:
        p = base / f'wrong_spec_v2_judgments_{j}.json'
        if not p.exists():
            continue
        with open(p) as f:
            d = json.load(f)
        for r in d:
            if isinstance(r, dict):
                rows.append({
                    'question_id': r.get('question_id'),
                    'condition': r.get('condition', 'C2c_wrong_spec_v2'),
                    'judge': j,
                    'score': r.get('score'),
                    'parse_failure': r.get('parse_failure', False),
                })
    if not rows:
        continue
    main_rows = load_global_judgments(subject)
    main_means_7j = aggregate_per_subject_per_condition(main_rows, ALL_J)
    c5 = main_means_7j.get('C5_baseline')
    v2_means_7j = aggregate_per_subject_per_condition(rows, ALL_J)
    if not v2_means_7j or c5 is None:
        continue
    v2_score = list(v2_means_7j.values())[0]
    delta = v2_score - c5
    deltas_v2_7j.append(delta)
    print(f'  {subject:<15} C5={c5:.3f} v2_7j={v2_score:.3f} delta={delta:+.3f}')
print(f'\nMean v2 7j delta (n={len(deltas_v2_7j)}): {statistics.mean(deltas_v2_7j):+.4f} (paper claims +0.22)')

# Also v1 7-judge using main study judgments
print('\n=== v1 (fixed derangement, judgments_v2.json) 7-judge ===')
deltas_v1_7j = []
for subject in GLOBAL_SUBJECTS:
    main_rows = load_global_judgments(subject)
    means_7j = aggregate_per_subject_per_condition(main_rows, ALL_J)
    c5 = means_7j.get('C5_baseline')
    c2c = means_7j.get('C2c_wrong_spec')
    if c5 is None or c2c is None:
        continue
    deltas_v1_7j.append(c2c - c5)
    print(f'  {subject:<15} C5={c5:.3f} C2c_v1={c2c:.3f} delta={c2c-c5:+.3f}')
print(f'\nMean v1 7j delta (n={len(deltas_v1_7j)}): {statistics.mean(deltas_v1_7j):+.4f} (paper claims -0.21)')

# Hamerton-specific wrong-spec v2 (Franklin)
print('\n=== Hamerton wrong-spec v2 (different file) ===')
hp = ROOT / 'results/_wrong_spec_v2/hamerton_results.json'
if hp.exists():
    with open(hp) as f:
        h = json.load(f)
    print('Type:', type(h).__name__)
    if isinstance(h, list):
        print('Len:', len(h))
        if h: print('First keys:', list(h[0].keys()) if isinstance(h[0], dict) else 'n/a')
    elif isinstance(h, dict):
        print('Keys:', list(h.keys())[:20])

