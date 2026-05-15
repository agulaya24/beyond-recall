"""
Bootstrap 95% confidence interval for the §4.1 gradient slope.

Regression: Delta_C4a ~ C5 across the 14 main-study subjects.
Point estimate from v11_emit/4_1_gradient.json: slope = -0.9597, p ~ 9e-6.

Method: 10,000 nonparametric bootstrap resamples of the 14 subjects (with
replacement). For each resample, fit OLS Delta_C4a ~ C5 and record the slope.
Report 2.5 / 50 / 97.5 percentiles.

Outputs:
  docs/research/bootstrap_4_1_gradient_20260507.json  (full distribution + summary)
  docs/research/bootstrap_4_1_gradient_20260507.md    (human-readable report)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "docs" / "research" / "v11_emit" / "4_1_gradient.json"
OUT_JSON = REPO / "docs" / "research" / "bootstrap_4_1_gradient_20260507.json"
OUT_MD = REPO / "docs" / "research" / "bootstrap_4_1_gradient_20260507.md"

N_ITERS = 10_000
SEED = 20260507


def ols_slope(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Return (slope, intercept) for simple OLS of y on x."""
    x_mean = x.mean()
    y_mean = y.mean()
    dx = x - x_mean
    dy = y - y_mean
    denom = float((dx * dx).sum())
    if denom == 0.0:
        return float("nan"), float("nan")
    slope = float((dx * dy).sum() / denom)
    intercept = float(y_mean - slope * x_mean)
    return slope, intercept


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    # Main-study set is N=14; Franklin is the high-baseline reference subject
    # appended to the JSON and is excluded from the §4.1 gradient regression
    # (see provenance.expected_n_judgments distinguishing main14 vs franklin).
    subjects_all = data["subjects"]
    subjects = [s for s in subjects_all if s["id"] != "franklin"]
    ids = [s["id"] for s in subjects]
    C5 = np.array([s["C5"] for s in subjects], dtype=float)
    dC4a = np.array([s["delta_C4a"] for s in subjects], dtype=float)
    n = len(C5)
    assert n == 14, f"expected 14 main-study subjects, got {n}"

    point_slope, point_intercept = ols_slope(C5, dC4a)

    rng = np.random.default_rng(SEED)
    slopes = np.empty(N_ITERS, dtype=float)
    intercepts = np.empty(N_ITERS, dtype=float)
    degenerate = 0
    for i in range(N_ITERS):
        idx = rng.integers(0, n, size=n)
        xb = C5[idx]
        yb = dC4a[idx]
        # If the resample happens to draw all-identical x (extremely unlikely
        # for n=14 with 14 distinct x values, but be defensive), retry once.
        if np.all(xb == xb[0]):
            degenerate += 1
            idx = rng.integers(0, n, size=n)
            xb = C5[idx]
            yb = dC4a[idx]
        s, b = ols_slope(xb, yb)
        slopes[i] = s
        intercepts[i] = b

    pct = np.percentile(slopes, [2.5, 50.0, 97.5])
    ci_low, median, ci_high = float(pct[0]), float(pct[1]), float(pct[2])
    se = float(slopes.std(ddof=1))
    mean_slope = float(slopes.mean())

    excludes_zero = ci_high < 0.0 or ci_low > 0.0
    excludes_neg_half = ci_high < -0.5 or ci_low > -0.5
    frac_below_zero = float((slopes < 0.0).mean())
    frac_below_neg_half = float((slopes < -0.5).mean())

    # Histogram (20 equal-width bins across the empirical range)
    hist_counts, hist_edges = np.histogram(slopes, bins=20)

    summary = {
        "schema_version": "v11.0",
        "analysis": "Bootstrap 95% CI on §4.1 gradient slope",
        "regression": "delta_C4a ~ C5",
        "n_subjects": n,
        "subject_ids": ids,
        "n_iterations": N_ITERS,
        "rng_seed": SEED,
        "degenerate_resamples_retried": degenerate,
        "point_estimate": {
            "slope": point_slope,
            "intercept": point_intercept,
        },
        "bootstrap": {
            "mean_slope": mean_slope,
            "median_slope": median,
            "se_slope": se,
            "ci95_low": ci_low,
            "ci95_high": ci_high,
            "fraction_below_zero": frac_below_zero,
            "fraction_below_neg_0_5": frac_below_neg_half,
        },
        "verdict": {
            "ci_excludes_zero": excludes_zero,
            "ci_excludes_neg_0_5": excludes_neg_half,
        },
        "histogram_20bin": {
            "edges": hist_edges.tolist(),
            "counts": hist_counts.tolist(),
        },
        "full_distribution": slopes.tolist(),
        "provenance": {
            "source_data": "docs/research/v11_emit/4_1_gradient.json",
            "script": "scripts/bootstrap_4_1_gradient_slope.py",
            "timestamp": "2026-05-07",
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Human-readable histogram description
    max_count = int(hist_counts.max()) if hist_counts.size else 0
    bar_scale = 40.0 / max_count if max_count else 0.0
    hist_lines = []
    for c, lo, hi in zip(hist_counts, hist_edges[:-1], hist_edges[1:]):
        bar = "#" * int(round(c * bar_scale))
        hist_lines.append(f"  [{lo:+.3f}, {hi:+.3f})  {c:>5d}  {bar}")
    hist_block = "\n".join(hist_lines)

    md = f"""# Bootstrap 95% CI on §4.1 Gradient Slope

**Date:** 2026-05-07
**Regression:** delta_C4a ~ C5 (5-judge primary panel, N=14 main-study subjects)
**Method:** Nonparametric bootstrap, resample subjects with replacement, OLS slope per iteration
**Iterations:** {N_ITERS:,}
**RNG seed:** {SEED}

## Point estimate (from v11_emit/4_1_gradient.json)

- slope = {point_slope:+.4f}
- intercept = {point_intercept:+.4f}
- (paper: slope = -0.96, p < 1e-5)

## Bootstrap distribution

| Statistic | Value |
|---|---|
| Mean slope | {mean_slope:+.4f} |
| Median slope (50th pct) | {median:+.4f} |
| SE (bootstrap SD) | {se:.4f} |
| 2.5th percentile | {ci_low:+.4f} |
| 97.5th percentile | {ci_high:+.4f} |
| 95% CI | [{ci_low:+.4f}, {ci_high:+.4f}] |
| Fraction of resamples with slope < 0 | {frac_below_zero:.4f} |
| Fraction of resamples with slope < -0.5 | {frac_below_neg_half:.4f} |

## Verdict

- 95% CI excludes zero: **{str(excludes_zero).upper()}**
- 95% CI excludes -0.5 (gradient robust at attenuated magnitude): **{str(excludes_neg_half).upper()}**

## Histogram (20 equal-width bins)

```
  bin range                count  bar (scaled to max)
{hist_block}
```

## Inputs

- N subjects = {n}
- Subjects: {", ".join(ids)}
- Degenerate resamples retried: {degenerate}

## Provenance

- Source data: `docs/research/v11_emit/4_1_gradient.json`
- Script: `scripts/bootstrap_4_1_gradient_slope.py`
- Full distribution: `docs/research/bootstrap_4_1_gradient_20260507.json` (`full_distribution` field)
"""
    OUT_MD.write_text(md, encoding="utf-8")

    print(f"Point estimate slope: {point_slope:+.4f}")
    print(f"Bootstrap median:     {median:+.4f}")
    print(f"95% CI:               [{ci_low:+.4f}, {ci_high:+.4f}]")
    print(f"Excludes 0:           {excludes_zero}")
    print(f"Excludes -0.5:        {excludes_neg_half}")
    print(f"Wrote: {OUT_JSON}")
    print(f"Wrote: {OUT_MD}")


if __name__ == "__main__":
    main()
