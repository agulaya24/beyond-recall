# DATA_LOCKS.md — Reported-figure conventions and reconciliation history

This file documents reconciliation decisions for any paper-headline figure where
multiple defensible numbers exist due to rounding, denominator choice, or
aggregation grain. The locked value is what appears in the paper.

Updates land here whenever a paper-cited number is reconciled across drafts so
that a future reader (or agent) checking provenance can trace the choice.

---

## Lock #1: Per-subject mean C4a across N=14 main-study subjects

**Locked value: 2.44.**

Established v11.8, 2026-05-08. Paper-wide reconciliation completed v11.9.8,
2026-05-11. Convergent with multi-reviewer panel critique (Anthropic Claude
deep review v11.9.7 flagged the §B.7.1 residual 2.46).

### Two defensible numbers

| Convention | Source | Value |
|---|---|---|
| **Table-rounded mean** (LOCKED) | Cross-subject mean of the 2-decimal per-subject C4a cells shown in §4.1 / Appendix D.1 table | **2.4393 → 2.44** |
| Un-rounded source mean | Cross-subject mean computed from un-rounded judge means inside `scripts/_v10_coupling_sensitivity.py` before per-subject display rounding | 2.46 |

Both are defensible; the difference is whether the mean is computed before or
after the per-subject rounding step. The paper reports per-subject scores to 2
decimal places in the §4.1 / Appendix D.1 table, so a reader recomputing the
mean from the visible table gets 2.44.

### Why 2.44 is the lock

The reporting convention is to preserve recompute consistency for any reader
who recomputes from the published table. If the paper reported 2.46, a reader
would sum the visible cells, divide by 14, and hit 2.44 — and then have to
chase the discrepancy. 2.44 keeps the paper internally recomputable from its
own display.

### History

| Draft cycle | §4.1 body | §B.7.1 | Notes |
|---|---|---|---|
| v10 | 2.46 | 2.46 | Both pulled from `_v10_coupling_sensitivity.py` summary line |
| v11.5 | 2.46 | 2.46 | Carried forward |
| v11.6 | 2.46 | 2.46 | Carried forward |
| v11.7 | 2.46 | 2.46 | Carried forward |
| **v11.8** | **2.44** | 2.46 | Aarik recomputed §4.1 from table cells (Session 119, 2026-05-08); §B.7.1 left at 2.46 as a pending reconciliation (Task #28) |
| v11.9 | 2.44 | 2.46 | Carried forward unchanged |
| v11.9.1 | 2.44 | 2.46 | Carried forward unchanged |
| v11.9.5 | 2.44 | 2.46 | Carried forward unchanged |
| v11.9.6 | 2.44 | 2.46 | Carried forward unchanged |
| v11.9.7 | 2.44 | 2.46 | Panel review flagged the residual (Anthropic Claude, 2026-05-10) |
| **v11.9.8** | **2.44** | **2.44** | Paper-wide reconciliation complete; data-lock footnote `[^c4a-mean-lock]` added at §B.7.1 |

### Source-file reconciliation (post-launch)

`docs/research/v10_coupling_sensitivity_analysis.md` Section 1 summary line
currently reads `C4a summary: mean 2.46, SD 0.25, min 2.01, max 2.78, range 0.77.`
This is the un-rounded value from the analysis script. The source file is
intentionally preserved as the record of the v10/v11 cycle's compute path; a
future regeneration of that file should add a "Display-rounded mean (paper
convention): 2.44" line alongside the un-rounded statistic so both values are
visible from the source. Post-launch hygiene; not blocking.

### Locked aggregation rule cross-reference

§3.3.5 of the paper locks per-subject as the canonical unit of inference. The
2.44 figure is computed at that grain. The grand-mean alternative (sum all
question-level scores across all subjects, divide by total question count)
would yield a different number that the paper does not report as the lead C4a
summary.

---

## Future locks to add

When a future paper-headline figure faces the same precision-vs-display
problem, document it here. Each lock entry should record:

- The locked value
- The competing defensible value(s)
- Why the lock direction was chosen
- The version history of the disagreement
- The source-file reconciliation plan (if any)
- Cross-reference to the locked aggregation rule (§3.3.5)
