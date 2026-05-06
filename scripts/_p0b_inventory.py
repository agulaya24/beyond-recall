"""
_p0b_inventory.py
=================

Pre-flight inventory for the P0 batch-2 jobs:
    - Job 1 (spec-induced refusal audit): count C1/C3 refusal pairs
      across 5 substrates x 9 low-baseline subjects before burning API budget.
    - Job 2 (question-category audit): confirm total BP-question count
      across 13 globals + Hamerton + Franklin.
    - Job 3 (judge floor test): confirm the 5-judge primary panel.

No API calls. Pure local computation.
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
DATA = REPO / 'data'

LOW_BASELINE_SUBJECTS = [
    'ebers', 'sunity_devee', 'fukuzawa', 'bernal_diaz', 'babur',
    'seacole', 'keckley', 'yung_wing', 'hamerton',
]

SYSTEMS = ['mem0', 'letta', 'supermemory', 'zep', 'baselayer']

GLOBAL_SUBJECTS = [
    'augustine', 'babur', 'bernal_diaz', 'cellini', 'ebers',
    'equiano', 'fukuzawa', 'keckley', 'rousseau', 'seacole',
    'sunity_devee', 'yung_wing', 'zitkala_sa',
]

# Canonical refusal regex copied from scripts/classify_hedging.py.
REFUSAL_PATTERNS = [
    r"\bI (?:cannot|can't|don't|do not) (?:know|predict|have|be sure)",
    r"\bI (?:have )?no (?:information|data|knowledge|facts)\b",
    r"\bwithout (?:more|additional|the) (?:information|context|facts)\b",
    r"\bThe retrieved facts (?:do not|don't) (?:contain|include|provide|mention|specify)",
    r"\bI must acknowledge\b",
    r"\bcannot determine\b",
    r"\bunable to (?:determine|predict|specify)\b",
    r"\bno specific (?:information|details)\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)

STARTS_REFUSAL_RE = re.compile(
    r"^\s*(?:I (?:cannot|can't|don't|do not)|"
    r"The retrieved facts (?:do not|don't))",
    re.IGNORECASE,
)


def subject_dir(subject):
    if subject == 'hamerton':
        return RESULTS / 'hamerton'
    return RESULTS / f'global_{subject}'


def load_results(subject, system):
    """Load C1/C3 response pairs for (subject, system).

    Returns (records, path, cond_c1, cond_c3) or (None, path, None, None) if unavailable.

    Order of preference:
      1. '{system}_fullpipeline_results.json' with C1_{system}_fp / C3_{system}_fp
      2. '{system}_results.json' with C1_{system} / C3_{system}
    Baselayer has no fullpipeline variant, goes straight to baselayer_results.json.
    """
    sdir = subject_dir(subject)
    if system == 'baselayer':
        p = sdir / 'baselayer_results.json'
        if not p.exists():
            return None, p, None, None
        return json.load(p.open(encoding='utf-8')), p, 'C1_baselayer', 'C3_baselayer'

    fp = sdir / f'{system}_fullpipeline_results.json'
    if fp.exists():
        return json.load(fp.open(encoding='utf-8')), fp, f'C1_{system}_fp', f'C3_{system}_fp'

    # Fall back to non-FP (e.g. Supermemory free-tier re-runs on babur/bernal_diaz)
    alt = sdir / f'{system}_results.json'
    if alt.exists():
        return json.load(alt.open(encoding='utf-8')), alt, f'C1_{system}', f'C3_{system}'

    return None, fp, None, None


def response_text(rec, condition):
    r = rec.get('responses', {}).get(condition)
    if r is None:
        return None
    if isinstance(r, dict):
        return r.get('text') or r.get('response') or ''
    return str(r)


def classify_starts(text):
    return bool(STARTS_REFUSAL_RE.match(text or ''))


def classify_broad(text):
    return bool(text) and bool(REFUSAL_RE.search(text))


def c1_c3_names(system):
    """Return (C1_name, C3_name) depending on whether fullpipeline or baselayer."""
    if system == 'baselayer':
        return (f'C1_{system}', f'C3_{system}')
    return (f'C1_{system}_fp', f'C3_{system}_fp')


def job1_inventory():
    """Inventory spec-induced refusals."""
    print("=" * 60)
    print("JOB 1 — spec-induced refusal inventory")
    print("=" * 60)

    grid_narrow = defaultdict(dict)   # [subject][system] -> count
    grid_broad = defaultdict(dict)
    missing = []
    total_n = 0
    total_narrow = 0
    total_broad = 0
    total_pairs = 0

    for subject in LOW_BASELINE_SUBJECTS:
        for system in SYSTEMS:
            data, path, c1_name, c3_name = load_results(subject, system)
            if data is None:
                missing.append((subject, system, str(path)))
                grid_narrow[subject][system] = None
                grid_broad[subject][system] = None
                continue
            narrow = 0
            broad = 0
            n = 0
            pairs = 0
            for rec in data:
                t1 = response_text(rec, c1_name)
                t3 = response_text(rec, c3_name)
                if t1 is None or t3 is None:
                    continue
                pairs += 1
                n += 1
                # Narrow: C3 starts_refusal but C1 does not
                if classify_starts(t3) and not classify_starts(t1):
                    narrow += 1
                # Broad: C3 has any refusal hit, C1 does not
                if classify_broad(t3) and not classify_broad(t1):
                    broad += 1
            grid_narrow[subject][system] = narrow
            grid_broad[subject][system] = broad
            total_n += n
            total_narrow += narrow
            total_broad += broad
            total_pairs += pairs

    # Print narrow grid
    print("\n[NARROW] Spec-induced refusal = C3 starts with refusal AND C1 does not")
    print(f"{'subject':<15} " + " ".join(f"{s:>12}" for s in SYSTEMS) + "  total")
    for subject in LOW_BASELINE_SUBJECTS:
        row_total = sum(v for v in grid_narrow[subject].values() if v is not None)
        cells = []
        for s in SYSTEMS:
            v = grid_narrow[subject][s]
            cells.append(f"{v if v is not None else '---':>12}")
        print(f"{subject:<15} " + " ".join(cells) + f"  {row_total}")

    # Print broad grid
    print("\n[BROAD] Spec-induced refusal = C3 has any refusal hit AND C1 does not")
    print(f"{'subject':<15} " + " ".join(f"{s:>12}" for s in SYSTEMS) + "  total")
    for subject in LOW_BASELINE_SUBJECTS:
        row_total = sum(v for v in grid_broad[subject].values() if v is not None)
        cells = []
        for s in SYSTEMS:
            v = grid_broad[subject][s]
            cells.append(f"{v if v is not None else '---':>12}")
        print(f"{subject:<15} " + " ".join(cells) + f"  {row_total}")

    print(f"\nTotal paired responses: {total_pairs}")
    print(f"Total narrow spec-induced refusals: {total_narrow}")
    print(f"Total broad spec-induced refusals: {total_broad}")
    print(f"\nMissing files ({len(missing)}):")
    for m in missing[:10]:
        print(f"  {m}")


def job2_inventory():
    """Inventory BP question count across batteries."""
    print("\n" + "=" * 60)
    print("JOB 2 — BP question inventory")
    print("=" * 60)
    total = 0
    for subj in GLOBAL_SUBJECTS:
        p = RESULTS / f'global_{subj}' / 'battery_v2.json'
        if not p.exists():
            print(f"  {subj}: MISSING")
            continue
        d = json.load(p.open(encoding='utf-8'))
        bp = [q for q in d.get('questions', []) if q.get('tier') == 'behavioral_prediction']
        print(f"  {subj}: BP={len(bp)}, total={len(d.get('questions', []))}")
        total += len(bp)

    # Hamerton
    hp = DATA / 'hamerton' / 'battery.json'
    if hp.exists():
        d = json.load(hp.open(encoding='utf-8'))
        qs = d.get('questions', d if isinstance(d, list) else [])
        bp = [q for q in qs if q.get('tier') == 'behavioral_prediction']
        print(f"  hamerton: BP={len(bp)}, total={len(qs)}")
        total += len(bp)
    else:
        print(f"  hamerton: MISSING {hp}")

    # Franklin
    fp = DATA / 'franklin' / 'battery.json'
    if fp.exists():
        d = json.load(fp.open(encoding='utf-8'))
        qs = d.get('questions', d if isinstance(d, list) else [])
        bp = [q for q in qs if q.get('tier') == 'behavioral_prediction']
        print(f"  franklin: BP={len(bp)}, total={len(qs)}")
        total += len(bp)
    else:
        print(f"  franklin: MISSING {fp}")

    print(f"\nTotal BP questions across all batteries: {total}")


def job3_inventory():
    """Panel-confirmation and pricing projection."""
    print("\n" + "=" * 60)
    print("JOB 3 — judge floor test — panel + cost projection")
    print("=" * 60)
    print("5-judge primary panel (from recompute_5judge_primary.py):")
    print("  haiku   -> claude-haiku-4-5-20251001")
    print("  sonnet  -> claude-sonnet-4-6")
    print("  opus    -> claude-opus-4-6")
    print("  gpt4o   -> gpt-4o-2024-08-06")
    print("  gpt54   -> gpt-5.4")
    print()
    # Judge prompt ~= (held_out~400 + response~1500 + scaffolding~200) * 4/3 chars-per-token ~= 2800 chars / 4 ~= 700 tokens
    # More conservative: assume up to 2000 tokens per call
    # Estimated cost per call
    est_costs = {
        'haiku':  0.001,
        'sonnet': 0.008,
        'opus':   0.030,
        'gpt4o':  0.010,
        'gpt54':  0.020,
    }
    diagnostics = 12
    variants = 5
    per_variant = diagnostics * variants
    total_calls_per_judge = per_variant
    total_calls = total_calls_per_judge * 5
    print(f"Plan: {diagnostics} diagnostics x {variants} variants x 5 judges = {total_calls} calls")
    total_cost = 0.0
    for j, cost in est_costs.items():
        c = total_calls_per_judge * cost
        total_cost += c
        print(f"  {j}: ${c:.2f} ({total_calls_per_judge} calls @ ${cost:.3f}/call est)")
    print(f"  ---")
    print(f"  TOTAL estimated: ${total_cost:.2f}")


if __name__ == '__main__':
    job1_inventory()
    job2_inventory()
    job3_inventory()
