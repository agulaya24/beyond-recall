"""
Comprehensive numerical verification for v10 paper.

Reuses load_global_judgments, load_hamerton_judgments from recompute_5judge_primary.
Re-derives all critical numbers from primary data and compares to v10 paper claims.
"""

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

# Reuse loaders from existing recompute script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from recompute_5judge_primary import (
    load_global_judgments, load_hamerton_judgments,
    PRIMARY_JUDGES, GEMINI_JUDGES, ALL_JUDGES,
    aggregate_per_subject_per_condition,
    GLOBAL_SUBJECTS, MAIN_STUDY,
)
from scipy import stats as scipy_stats
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

# === Step 1: build per-subject per-condition 5-judge primary table ===
print('=== Step 1: Per-subject, per-condition 5-judge primary means ===')
subject_data = {}
for subject in MAIN_STUDY:
    if subject == 'hamerton':
        rows = load_hamerton_judgments()
    else:
        rows = load_global_judgments(subject)
    primary = aggregate_per_subject_per_condition(rows, PRIMARY_JUDGES)
    seven = aggregate_per_subject_per_condition(rows, ALL_JUDGES)
    subject_data[subject] = {'5j': primary, '7j': seven, 'rows': rows}

# Print canonical condition columns: C5, C2a, C2c, C4, C4a
print(f'{"subject":<15} {"C5":>6} {"C2a":>6} {"C2c":>6} {"C4":>6} {"C4a":>6}')
for subject in MAIN_STUDY:
    p = subject_data[subject]['5j']
    print(f'{subject:<15} '
          f'{p.get("C5_baseline", 0):>6.2f} '
          f'{p.get("C2a_full_spec", 0):>6.2f} '
          f'{p.get("C2c_wrong_spec", 0):>6.2f} '
          f'{p.get("C4_factdump", 0):>6.2f} '
          f'{p.get("C4a_full_facts_plus_spec", 0):>6.2f}')

# Persist for downstream steps
import csv
csv_path = ROOT / 'scripts/_v10_verification/per_subject_5judge.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['subject', 'C5', 'C2a', 'C2c', 'C4', 'C4a', 'C5_7j', 'C2a_7j', 'C2c_7j', 'C4_7j', 'C4a_7j'])
    for subject in MAIN_STUDY:
        p = subject_data[subject]['5j']
        s = subject_data[subject]['7j']
        w.writerow([subject,
                   p.get('C5_baseline'), p.get('C2a_full_spec'),
                   p.get('C2c_wrong_spec'), p.get('C4_factdump'),
                   p.get('C4a_full_facts_plus_spec'),
                   s.get('C5_baseline'), s.get('C2a_full_spec'),
                   s.get('C2c_wrong_spec'), s.get('C4_factdump'),
                   s.get('C4a_full_facts_plus_spec')])
print(f'\nWrote {csv_path}')

# === Step 2: Gradient regression ===
print('\n=== Step 2: Gradient regression (5-judge primary, 14 main-study subjects) ===')
gradient_rows = []
for subject in MAIN_STUDY:
    p = subject_data[subject]['5j']
    c5 = p.get('C5_baseline')
    c2a = p.get('C2a_full_spec')
    c4a = p.get('C4a_full_facts_plus_spec')
    if c5 is None or c4a is None:
        continue
    gradient_rows.append({
        'subject': subject,
        'c5': c5, 'c2a': c2a, 'c4a': c4a,
        'delta_spec': (c2a - c5) if c2a is not None else None,
        'delta_c4a': c4a - c5,
    })

c5_vals = np.array([r['c5'] for r in gradient_rows])
dc4a_vals = np.array([r['delta_c4a'] for r in gradient_rows])
c2a_vals = np.array([r['c2a'] for r in gradient_rows])
c4a_vals = np.array([r['c4a'] for r in gradient_rows])

slope, intercept, r_val, p_val, se = scipy_stats.linregress(c5_vals, dc4a_vals)
n = len(c5_vals)
df = n - 2
t_crit = scipy_stats.t.ppf(0.975, df)
ci_low = slope - t_crit * se
ci_high = slope + t_crit * se
print(f'N = {n}')
print(f'Slope: {slope:.4f}')
print(f'95% CI: [{ci_low:.4f}, {ci_high:.4f}]')
print(f'R²: {r_val**2:.4f}')
print(f'r: {r_val:.4f}')
print(f'p-value: {p_val:.6e}')

# Wilcoxon signed-rank
print('\n=== Step 2b: Wilcoxon signed-rank ===')
# Paper says: C5 vs C2a: W=10, p=0.005; C5 vs C4a: W=11, p=0.007
# scipy default (mode='auto') reports "min of T+/T-"
w_spec, p_spec = scipy_stats.wilcoxon(c5_vals, c2a_vals)
w_c4a, p_c4a = scipy_stats.wilcoxon(c5_vals, c4a_vals)
print(f'C5 vs C2a:  W={w_spec:.1f}, p={p_spec:.6f}')
print(f'C5 vs C4a:  W={w_c4a:.1f}, p={p_c4a:.6f}')

# Try "exact" mode too
w_spec_e, p_spec_e = scipy_stats.wilcoxon(c5_vals, c2a_vals, method='exact')
w_c4a_e, p_c4a_e = scipy_stats.wilcoxon(c5_vals, c4a_vals, method='exact')
print(f'C5 vs C2a exact:  W={w_spec_e:.1f}, p={p_spec_e:.6f}')
print(f'C5 vs C4a exact:  W={w_c4a_e:.1f}, p={p_c4a_e:.6f}')

# === Step 3: Low-baseline slice mean delta_C4a ===
print('\n=== Step 3: Low-baseline (C5 <= 2.0) slice ===')
low = [r for r in gradient_rows if r['c5'] <= 2.0]
print(f'N = {len(low)} (paper claims 9)')
print(f'Subjects: {[r["subject"] for r in low]}')
mean_dc4a = statistics.mean(r['delta_c4a'] for r in low)
print(f'Mean delta_C4a: {mean_dc4a:+.4f} (paper claims +0.89)')
print(f'Subjects with positive delta: {sum(1 for r in low if r["delta_c4a"] > 0)}/{len(low)}')

# All 14 subjects positive
all14_pos = sum(1 for r in gradient_rows if r['delta_c4a'] > 0)
print(f'\nAll 14: {all14_pos}/14 positive (paper claims 12/14)')

# === Step 4: Wrong-spec analysis on 13 globals ===
print('\n=== Step 4: Wrong-spec analysis (13 global subjects, 5-judge primary) ===')
# For globals, judgments_v2.json contains C2c_wrong_spec (which is C2c v2 random derangement)
# Paper claims:
#   C2c v2 random derangement (13 globals): mean delta vs C5 = +0.22
#   C2c v1 fixed derangement (13 globals): mean delta vs C5 = -0.25
#   C2a (correct spec, 13 globals): mean delta vs C5 = +0.35
# Hamerton has its own wrong-spec (Franklin's spec) which is reported separately

# We have C2c_wrong_spec in judgments_v2 - need to determine if this is v1 or v2
# Per data file: this is the random derangement (v2). Or is it?
deltas_c2a = []
deltas_c2c = []
for subject in GLOBAL_SUBJECTS:
    p = subject_data[subject]['5j']
    c5 = p.get('C5_baseline')
    c2a = p.get('C2a_full_spec')
    c2c = p.get('C2c_wrong_spec')
    if c5 is None: continue
    if c2a is not None:
        deltas_c2a.append(c2a - c5)
    if c2c is not None:
        deltas_c2c.append(c2c - c5)
print(f'Globals C2a mean delta vs C5 (n={len(deltas_c2a)}): {statistics.mean(deltas_c2a):+.4f} (paper: +0.35)')
print(f'Globals C2c mean delta vs C5 (n={len(deltas_c2c)}): {statistics.mean(deltas_c2c):+.4f}')

# Look for wrong_spec_v2 directory (the v2 random derangement re-run)
print('\n--- Checking for wrong_spec_v2 results ---')
wsv2 = ROOT / 'results/_wrong_spec_v2'
if wsv2.exists():
    print(f'_wrong_spec_v2 exists, contents:')
    for p in sorted(wsv2.iterdir()):
        print(f'  {p.name}')

# === Step 5: 7-judge sensitivity for §4.6.2 ===
print('\n=== Step 5: 7-judge sensitivity (13 global subjects, where applicable) ===')
deltas_c2a_7 = []
deltas_c2c_7 = []
for subject in GLOBAL_SUBJECTS:
    s = subject_data[subject]['7j']
    c5 = s.get('C5_baseline')
    c2a = s.get('C2a_full_spec')
    c2c = s.get('C2c_wrong_spec')
    if c5 is None: continue
    if c2a is not None:
        deltas_c2a_7.append(c2a - c5)
    if c2c is not None:
        deltas_c2c_7.append(c2c - c5)
print(f'Globals 7j C2a delta vs C5: {statistics.mean(deltas_c2a_7):+.4f} (paper: +0.45)')
print(f'Globals 7j C2c delta vs C5: {statistics.mean(deltas_c2c_7):+.4f}')

# === Step 6: Compression table (low-baseline slice) ===
print('\n=== Step 6: Compression table (low-baseline 9 subjects) ===')
# C5, C2a, C4, C4a, C8, C9 means
# C8/C9 for globals are in c8_c9_judgments_*.json files
def load_global_c8c9(subject):
    """Load C8_raw_corpus and C9_raw_corpus_plus_spec judgments for a global subject."""
    base = ROOT / f'results/global_{subject}'
    rows = []
    for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']:
        p = base / f'c8_c9_judgments_{j}.json'
        if p.exists():
            d = json.load(p.open())
            for r in d:
                if isinstance(r, dict):
                    rows.append({
                        'question_id': r.get('question_id'),
                        'condition': r.get('condition'),
                        'judge': j,
                        'score': r.get('score'),
                        'parse_failure': r.get('parse_failure', False),
                    })
    return rows

# Same loader for hamerton (different filename pattern)
def load_hamerton_c8c9():
    base = ROOT / 'results/hamerton'
    rows = []
    for j in ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash', 'gemini_pro']:
        p = base / f'c8_c9_judgments_{j}.json'
        if p.exists():
            d = json.load(p.open())
            for r in d:
                if isinstance(r, dict):
                    rows.append({
                        'question_id': r.get('question_id'),
                        'condition': r.get('condition'),
                        'judge': j,
                        'score': r.get('score'),
                        'parse_failure': r.get('parse_failure', False),
                    })
    return rows

c8c9_data = {}
for subject in MAIN_STUDY:
    if subject == 'hamerton':
        rows = load_hamerton_c8c9()
    else:
        rows = load_global_c8c9(subject)
    c8c9_data[subject] = aggregate_per_subject_per_condition(rows, PRIMARY_JUDGES)

# Print compression table for low-baseline slice
print(f'{"subject":<15} {"C5":>6} {"C2a":>6} {"C4":>6} {"C8":>6} {"C4a":>6} {"C9":>6} {"C8-C2a":>8}')
low_subjects_for_compression = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'bernal_diaz', 'babur', 'seacole', 'keckley', 'yung_wing']
all_c5, all_c2a, all_c4, all_c8, all_c4a, all_c9 = [], [], [], [], [], []
for subject in low_subjects_for_compression:
    p = subject_data[subject]['5j']
    cc = c8c9_data.get(subject, {})
    c5 = p.get('C5_baseline')
    c2a = p.get('C2a_full_spec')
    c4 = p.get('C4_factdump')
    c4a = p.get('C4a_full_facts_plus_spec')
    c8 = cc.get('C8_raw_corpus')
    c9 = cc.get('C9_raw_corpus_plus_spec')
    diff = (c8 - c2a) if (c8 is not None and c2a is not None) else None
    line = f'{subject:<15} {(c5 or 0):>6.2f} {(c2a or 0):>6.2f} {(c4 or 0):>6.2f} {(c8 or 0):>6.2f} {(c4a or 0):>6.2f} {("--" if c9 is None else f"{c9:.2f}"):>6} '
    line += f'{("--" if diff is None else f"{diff:+.2f}"):>8}'
    print(line)
    if c5 is not None: all_c5.append(c5)
    if c2a is not None: all_c2a.append(c2a)
    if c4 is not None: all_c4.append(c4)
    if c4a is not None: all_c4a.append(c4a)
    if c8 is not None: all_c8.append(c8)
    if c9 is not None: all_c9.append(c9)
print(f'{"MEAN":<15} {statistics.mean(all_c5):>6.2f} {statistics.mean(all_c2a):>6.2f} {statistics.mean(all_c4):>6.2f} {statistics.mean(all_c8):>6.2f} {statistics.mean(all_c4a):>6.2f} {statistics.mean(all_c9):>6.2f}')
print(f'C8-C2a mean: {statistics.mean(all_c8) - statistics.mean(all_c2a):+.4f} (paper: +0.22)')

# Detailed: per-column means with and without Babur
print('\n=== Compression mean breakdown ===')
print(f'C5 9-subj mean: {statistics.mean(all_c5):.4f} (paper Table 4.2 says 1.52)')
print(f'C2a 9-subj mean: {statistics.mean(all_c2a):.4f} (paper says 2.23)')
print(f'C4 9-subj mean: {statistics.mean(all_c4):.4f} (paper says 2.35)')
print(f'C8 9-subj mean: {statistics.mean(all_c8):.4f} (paper says 2.45)')
print(f'C4a 9-subj mean: {statistics.mean(all_c4a):.4f} (paper says 2.45)')
print(f'C9 8-subj mean (Babur excluded): {statistics.mean(all_c9):.4f} (paper says 2.50)')

# Re-mean after excluding Babur
print('\n--- Without Babur (8 subj) ---')
no_babur_idx = [i for i, s in enumerate(low_subjects_for_compression) if s != 'babur']
def mean_idx(arr, idx):
    return statistics.mean(arr[i] for i in idx) if all(arr[i] is not None for i in idx) else None

# Filter: which positions had each value
c5_nb = [c for s, c in zip(low_subjects_for_compression, all_c5) if s != 'babur'] if False else None  # all_c5 already aligns with subjects in order
# Actually all_c5 is built per subject in iteration order, but only non-None values appended
# Let me rebuild explicitly
print('Per-subject non-Babur:')
for subject in low_subjects_for_compression:
    if subject == 'babur': continue
    p = subject_data[subject]['5j']
    cc = c8c9_data.get(subject, {})
    print(f'  {subject}: C5={p.get("C5_baseline")}, C2a={p.get("C2a_full_spec")}, C4={p.get("C4_factdump")}, C8={cc.get("C8_raw_corpus")}, C4a={p.get("C4a_full_facts_plus_spec")}, C9={cc.get("C9_raw_corpus_plus_spec")}')

# === Step 7: Spec-effect deltas, 7-judge widening ===
print('\n=== Step 7: 7-judge sensitivity (§4.6.2 table) ===')
print('Per-subject 7-judge C2a, C2c, C4a deltas vs C5 (13 globals, 5-judge primary):')
# Already computed
# === Save data ===
print(f'\n=== Stored data; per-subject CSV at {csv_path} ===')
