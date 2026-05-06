# P0 C1 closure report: `_audit_with_c2c.py` rebuild

**Date:** 2026-04-23
**Scope:** Close the final open P0 from `s114_repo_quality_audit.md`. Rebuild the
one-shot audit script whose provenance was cited for Appendix D.3.4 and D.3.5
of the v9 paper draft but that no longer existed in the repo.

## Deliverable

`scripts/_audit_with_c2c.py`, reconstructed. Computes the C2c length-score
correlation and the low-range mean response length that the appendix cites.
Runs to completion on the repo as-is with `python scripts/_audit_with_c2c.py`.

## Reconstructed statistics

Exact script output on the current `results/` tree:

| Statistic | Script value | Appendix value | Source line |
|---|---|---|---|
| D.3.4 C2c length-score r | 0.500 | 0.500 | `docs/beyond_recall_v9_draft.md:2187` |
| D.3.4 C2c n | 312 | 312 | `docs/beyond_recall_v9_draft.md:2187` |
| D.3.5 low-range (< 2.0) mean length | 2,087 chars | 2,087 chars | `docs/beyond_recall_v9_draft.md:2199` |
| D.3.5 low-range n | 795 | 795 | `docs/beyond_recall_v9_draft.md:2199` |

All four load-bearing targets reproduce to the exact decimal printed in the
appendix. Within the task's tolerance (0.01 on r, 10 chars on mean length),
the script has zero discrepancy on the numbers it is cited for.

## Collateral numbers (for cross-reference, not part of the P0 mandate)

The same run also reproduces these values that appear in the surrounding
Appendix D.3 text, matching to 2 to 3 decimal places:

| Quantity | Script | Appendix | Appendix line |
|---|---|---|---|
| Total responses analyzed | 1,599 | 1,599 | 2178 |
| Abstention-pattern match rate | 12.0% | 12.0% | §3.7.6 prose |
| Abstention-like mean primary score | 1.27 | 1.27 | §3.7.6 prose |
| C5 length-score r | 0.604 | 0.604 | 2183 |
| C2a length-score r | 0.144 | 0.14 | 2184 |
| C4 length-score r | 0.009 | 0.01 | 2185 |
| C4a length-score r | -0.013 | -0.01 | 2186 |
| Ultra-high (>= 4.5) mean length | 2,790 chars | 2,790 | 2197 |
| Mid-range (2.5 to 3.5) mean length | 2,829 chars | 2,829 | 2198 |

## Observation, flagged for transparency

The script reports per-condition n values of:

  C5=312, C2a=351, C4=312, C4a=312, C2c=312

The Appendix D.3.4 table (lines 2182 to 2187) reports:

  All=1599, C5=351, C2a=351, C4=351, C4a=351, C2c=312

The C2c cell (312) and the total (1599) match. C2a matches (351). The C5,
C4, and C4a cells in the appendix are 351 while the script produces 312.
The difference is that Hamerton's C5 and C4 responses live in
`results/hamerton/results_harmonized.json`, not `results.json`, and
Hamerton's C4a response is keyed as `C4a_full_all_facts_plus_spec` (not the
normalized form) in `results.json`, so the loop-over-normalized-names skips
those three Hamerton conditions and lands at 8 x 39 = 312 observations per
skipped condition.

This is the same treatment used by the canonical `audit_low_end_inflation.py`.
The per-condition r values in the appendix match what this script produces,
so whichever audit generated the appendix table was running against the
same 312-observation C5 / C4 / C4a slices the script uses here. The 351
values shown in the appendix's n column for C5 / C4 / C4a appear to be a
transcription error in the appendix table itself, not a discrepancy in the
script.

Recommendation: the appendix n values for C5, C4, and C4a rows should be
351 only if Hamerton is merged in from `results_harmonized.json` and
condition-name normalization is applied to `results.json`. A follow-up edit
to either (a) correct those three n values to 312 or (b) expand the
Hamerton response loader and re-run the audit would close the gap. This is
outside the P0 closure scope, so the script matches the original behavior
and flags the observation here rather than silently modifying either the
script or the appendix.

## Provenance now valid for these report lines

In `docs/reviews/_appendix_pending_fills_report.md`:

  - Line 33 ("Source: `scripts/_audit_with_c2c.py` (written for this task...)")
  - Line 41 ("Source: Same rerun of `_audit_with_c2c.py` as fill 2.")
  - Line 95 ("scratch fill-orchestration scripts ... `_audit_with_c2c.py` ... were created to perform the string replacements and then deleted."). Note: only this script is restored; the two other scratch scripts mentioned remain deleted and are not part of any cited provenance.
  - Line 110 (verification row: D.3.4 C2c length correlation -> `_audit_with_c2c.py` stdout)
  - Line 111 (verification row: D.3.5 low-range mean length -> `_audit_with_c2c.py` stdout)

## Script deltas vs `audit_low_end_inflation.py`

Three deltas applied, matching the inventory in the pending-fills report:

1. Explicit `encoding='utf-8'` on every `json.load` via a small helper, to
   avoid the Windows charmap codec issue that dropped 4 of 9 subjects on
   some terminals.
2. `C2c_wrong_spec` added to the per-condition correlation output loop.
   The original stopped at C4a.
3. The n for the low-range (score < 2.0) slice is printed on its own line,
   not embedded inside another stat.

All other aggregation, filtering, and Hamerton handling is unchanged, to
keep the collateral numbers (abstention rate 12%, abstention mean 1.27,
C5 r 0.604, etc.) reproducible on the same provenance.
