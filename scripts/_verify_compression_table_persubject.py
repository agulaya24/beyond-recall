"""Recompute the §4.2 compression table on a consistent per-subject-mean grain.

Reads the locked scaffold output `docs/research/v11_emit/4_2_compression.json`
(produced by `scripts/_v11_emit_4_2_compression.py`, the canonical 5-judge
primary aggregator) and applies the consistent n=9 / n=8 Babur rule.

n=9 vs n=8 rule (CORRECTED after data inspection):
  - C5, C2a, C4, C8, C4a: all 9 low-baseline subjects. Babur's C8 DOES exist
    in the data (run on a 100K-word truncation of his 422,772-word corpus;
    see scaffold provenance note). Delta = condition mean(n=9) - C5 mean(n=9).
  - C9 ONLY: Babur structurally excluded -- no Babur C9 data exists (corpus +
    spec exceeded the response model's context window). Delta = C9 mean(n=8)
    - C5 mean(n=8, Babur-excluded). Row marked n=8.

The task brief assumed both C8 and C9 exclude Babur; the data shows only C9
does. This is documented in the recompute note. Under the corrected rule
every Delta is condition-mean minus a C5 baseline computed over the *same*
subject set, eliminating the asymmetric-exclusion artifact (8-row C5 = 1.52
subtracted from 9-row C2a/C4/C4a in the old table).
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EMIT = REPO / "docs" / "research" / "v11_emit" / "4_2_compression.json"

SUBS9 = ['hamerton', 'sunity_devee', 'ebers', 'fukuzawa', 'bernal_diaz',
         'babur', 'seacole', 'keckley', 'yung_wing']
SUBS8 = [s for s in SUBS9 if s != 'babur']


def main():
    claims = json.loads(EMIT.read_text())["claims"]

    def val(subject, cond):
        return claims[f"4_2_{subject}_{cond}"]["value"]

    def colmean(subjects, cond):
        vs = [val(s, cond) for s in subjects if val(s, cond) is not None]
        return statistics.mean(vs), len(vs)

    print("=== Per-subject panel means (5-judge primary, from locked scaffold) ===")
    print(f"{'subject':<14}{'C5':>8}{'C2a':>8}{'C4':>8}{'C8':>8}{'C4a':>8}{'C9':>8}")
    for s in SUBS9:
        cells = []
        for cond in ['C5', 'C2a', 'C4', 'C8', 'C4a', 'C9']:
            v = val(s, cond)
            cells.append("   n/a  " if v is None else f"{v:8.4f}")
        print(f"{s:<14}" + "".join(cells))
    print()

    c5_9, n5_9 = colmean(SUBS9, 'C5')
    c5_8, n5_8 = colmean(SUBS8, 'C5')
    print(f"C5 mean n=9 (incl Babur)      = {c5_9:.4f}  rounds {round(c5_9, 2)}")
    print(f"C5 mean n=8 (Babur-excluded)  = {c5_8:.4f}  rounds {round(c5_8, 2)}")
    print()

    print("=== CANONICAL TABLE under corrected rule (C8 = n=9, C9 = n=8) ===")
    print(f"{'Cond':<6}{'n':>4}{'Mean':>10}{'rounds':>9}{'Delta':>10}{'rounds':>9}")
    # C5 row
    print(f"{'C5':<6}{9:>4}{c5_9:>10.4f}{round(c5_9,2):>9}{0.0:>10.4f}{'0.00':>9}")
    for cond in ['C2a', 'C4', 'C8', 'C4a']:
        m, n = colmean(SUBS9, cond)
        d = m - c5_9
        print(f"{cond:<6}{n:>4}{m:>10.4f}{round(m,2):>9}{d:>10.4f}{round(d,2):>+9}")
    # C9 only: n=8, vs 8-row C5
    m9, n9 = colmean(SUBS8, 'C9')
    d9 = m9 - c5_8
    print(f"{'C9':<6}{n9:>4}{m9:>10.4f}{round(m9,2):>9}{d9:>10.4f}{round(d9,2):>+9}")
    print()

    c2a_d = colmean(SUBS9, 'C2a')[0] - c5_9
    c8_d = colmean(SUBS9, 'C8')[0] - c5_9
    print(f"CHECK  C2a Delta = {c2a_d:+.4f} -> rounds {round(c2a_d,2):+}  (prose: +0.69)  "
          f"{'OK' if round(c2a_d,2)==0.69 else 'MISMATCH'}")
    print(f"CHECK  C8  Delta = {c8_d:+.4f} -> rounds {round(c8_d,2):+}  (prose: +0.91)  "
          f"{'OK' if round(c8_d,2)==0.91 else 'MISMATCH'}")


if __name__ == '__main__':
    main()
