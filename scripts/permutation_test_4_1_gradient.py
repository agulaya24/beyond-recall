"""Permutation test on the §4.1 headline gradient slope (Beyond Recall).

Null hypothesis: there is no real gradient between C5 baseline and Delta_C4a
spec lift across subjects. Under this null, the observed -0.96 slope from
regressing Delta_C4a on C5 should be reproducible by random reassignment of
Delta values to subjects.

Procedure
---------
1. Load the 14-subject (C5, Delta_C4a) pairs from
   docs/research/v11_emit/4_1_gradient.json.
2. Compute observed OLS slope of Delta_C4a ~ C5.
3. Permute Delta_C4a values across subjects 10,000 times (C5 fixed,
   Delta_C4a vector reshuffled). Refit OLS on each permutation.
4. Compute two-sided empirical p-value:
      p = mean(|slope_perm| >= |slope_obs|)
5. Report null mean, null std, and verdict.

This test is distinct from the v10 coupling-sensitivity permutation
(_v10_coupling_sensitivity.py), which permuted the *level* C4a vector to
test the spec-on-baseline coupling null. Here we permute Delta_C4a directly
to test whether the gradient itself is configuration-coincidence.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "docs" / "research" / "v11_emit" / "4_1_gradient.json"
OUT_PATH = (
    REPO_ROOT / "docs" / "research" / "permutation_test_4_1_gradient_20260507.md"
)

RNG_SEED = 20260507
N_PERM = 10_000


def ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    """Plain OLS slope of y on x (no intercept-only edge cases here, n=14)."""
    res = stats.linregress(x, y)
    return float(res.slope)


def main() -> None:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        emit = json.load(f)

    # Headline §4.1 regression uses n=14: Hamerton + 13 globals.
    # Franklin is the high-baseline reference, not part of the regression
    # (per scripts/_v11_emit_4_1_gradient.py line 39-40 and emit summary
    # regression_delta_on_C5.n = 14).
    subjects = [s for s in emit["subjects"] if s["id"] != "franklin"]
    rows = [(s["display_name"], float(s["C5"]), float(s["delta_C4a"])) for s in subjects]
    names = [r[0] for r in rows]
    C5 = np.array([r[1] for r in rows], dtype=float)
    dC4a = np.array([r[2] for r in rows], dtype=float)

    n = len(C5)
    obs_slope = ols_slope(C5, dC4a)
    obs_r = stats.linregress(C5, dC4a).rvalue

    rng = np.random.default_rng(RNG_SEED)
    perm_slopes = np.empty(N_PERM, dtype=float)
    for i in range(N_PERM):
        permuted = rng.permutation(dC4a)
        perm_slopes[i] = ols_slope(C5, permuted)

    abs_obs = abs(obs_slope)
    p_two_sided = float(np.mean(np.abs(perm_slopes) >= abs_obs))
    p_one_sided_neg = float(np.mean(perm_slopes <= obs_slope))

    null_mean = float(perm_slopes.mean())
    null_std = float(perm_slopes.std(ddof=1))
    null_min = float(perm_slopes.min())
    null_max = float(perm_slopes.max())
    q025, q500, q975 = np.quantile(perm_slopes, [0.025, 0.5, 0.975])

    extreme_count = int(np.sum(np.abs(perm_slopes) >= abs_obs))

    print(f"n subjects: {n}")
    print(f"Observed slope (Delta_C4a ~ C5): {obs_slope:+.4f}")
    print(f"Observed Pearson r: {obs_r:+.4f}")
    print(f"Permutations: {N_PERM}")
    print(
        f"Null distribution: mean={null_mean:+.4f}, sd={null_std:.4f}, "
        f"min={null_min:+.4f}, max={null_max:+.4f}"
    )
    print(f"Null 95% interval: [{q025:+.4f}, {q975:+.4f}], median={q500:+.4f}")
    print(
        f"Permutations with |slope| >= |obs| ({abs_obs:.4f}): "
        f"{extreme_count} of {N_PERM}"
    )
    print(f"Two-sided empirical p-value: {p_two_sided:.5f}")
    print(f"One-sided (slope <= obs) p-value: {p_one_sided_neg:.5f}")

    # Persist the markdown report.
    lines = []
    lines.append("# §4.1 Headline-Gradient Permutation Test")
    lines.append("")
    lines.append("**Date:** 2026-05-07")
    lines.append("**Script:** `scripts/permutation_test_4_1_gradient.py`")
    lines.append("**Data:** `docs/research/v11_emit/4_1_gradient.json` (5-judge primary panel)")
    lines.append(f"**Seed:** {RNG_SEED} | **Permutations:** {N_PERM:,}")
    lines.append("")
    lines.append("## Null hypothesis")
    lines.append("")
    lines.append(
        "Under H0, there is no real association between a subject's baseline "
        "(C5) and the spec lift (Delta_C4a). Reassigning Delta_C4a values "
        "to subjects at random should reproduce the observed slope as a "
        "matter of luck."
    )
    lines.append("")
    lines.append("This is *distinct* from the v10 coupling-sensitivity permutation, "
                 "which permuted the level C4a vector to test a spec-on-baseline "
                 "coupling null. Here Delta_C4a is permuted directly.")
    lines.append("")
    lines.append("## Observed statistic")
    lines.append("")
    lines.append(f"- n = {n} subjects (Hamerton + 13 globals; Franklin excluded as high-baseline reference, matching the §4.1 regression)")
    lines.append(f"- OLS slope (Delta_C4a ~ C5): **{obs_slope:+.4f}**")
    lines.append(f"- Pearson r: {obs_r:+.4f}")
    lines.append("")
    lines.append("## Null distribution")
    lines.append("")
    lines.append(f"- Mean: {null_mean:+.4f} (expected ~0 under H0)")
    lines.append(f"- SD: {null_std:.4f}")
    lines.append(f"- Min: {null_min:+.4f}")
    lines.append(f"- Max: {null_max:+.4f}")
    lines.append(f"- Median: {q500:+.4f}")
    lines.append(f"- 95% interval: [{q025:+.4f}, {q975:+.4f}]")
    lines.append("")
    lines.append("## Test result")
    lines.append("")
    lines.append(
        f"- Permutations with |slope| >= |observed| ({abs_obs:.4f}): "
        f"{extreme_count} of {N_PERM:,}"
    )
    lines.append(f"- **Two-sided empirical p-value: {p_two_sided:.5f}**")
    lines.append(f"- One-sided (slope <= observed): {p_one_sided_neg:.5f}")
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    if p_two_sided < 0.001:
        verdict = (
            "The headline gradient slope of -0.96 is **not** a coincidence "
            "of the specific 14-subject configuration. The observed slope "
            "lies far in the tail of the permutation null distribution; "
            f"only {extreme_count} of {N_PERM:,} random reassignments of "
            "Delta_C4a values across subjects produce a slope as extreme. "
            "The negative association between baseline and spec lift survives "
            "permutation testing at p < 0.001."
        )
    elif p_two_sided < 0.05:
        verdict = (
            "The headline gradient slope is unlikely under the null "
            f"(p = {p_two_sided:.4f}), though less decisively than a < 0.001 "
            "result. It survives permutation testing."
        )
    else:
        verdict = (
            f"The headline gradient slope does not survive permutation testing "
            f"(p = {p_two_sided:.4f}). The observed slope is plausible under "
            "random reassignment of Delta_C4a values."
        )
    lines.append(verdict)
    lines.append("")
    lines.append("## Per-subject input")
    lines.append("")
    lines.append("| Subject | C5 | Delta_C4a |")
    lines.append("|---|---:|---:|")
    for name, c5, d in rows:
        lines.append(f"| {name} | {c5:.3f} | {d:+.3f} |")
    lines.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {OUT_PATH}")


if __name__ == "__main__":
    main()
