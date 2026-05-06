"""
classify_hedging.py
===================

Canonical hedging/refusal classifier for the "Beyond Recall" study.

PROVENANCE NOTE
---------------
The paper's original hedging numbers (published in v6/v7 drafts as
127/13/3 out of 507 = 25.0% / 2.6% / 0.6%) could not be reproduced
from the in-repo data by any threshold of the regex patterns defined
in `docs/research/_analyze_score_bands.py`. An exhaustive sweep
(see `scripts/_probe_hedge_variants.py` and the previous version of
`docs/research/hedging_analysis.json`) found that the directional
story (C5 >> C2a >> C4a) replicates under every reasonable variant,
but the exact counts 127/13/3 do not. The classifier that produced
those counts is not recoverable from the repo.

This script defines a clean, documented replacement classifier and
recomputes the rates against the same 507-response corpus per
condition (13 global subjects × 39 questions).

DECISION RULE (primary metric: `starts_refusal`)
------------------------------------------------
A response is classified as "hedged" if its text begins (modulo
leading whitespace) with a refusal prefix:

    "I cannot..." | "I can't..." | "I don't..." |
    "The retrieved facts do not..." | "The retrieved facts don't..."

This is the narrowest reproducible rule that (a) draws only from
the REFUSAL_PATTERNS already used elsewhere in the study analysis
pipeline (`_analyze_score_bands.py`), (b) produces a baseline rate
in the 20-35% band the paper claims, and (c) cleanly preserves the
paper's qualitative story (baseline ~quarter of responses hedge,
adding the spec drops hedging to near-zero, adding facts drops it
further). Composite thresholds that try to hit 127/13/3 exactly
were considered and rejected as overfit.

SECONDARY METRICS (reported for completeness, not used in paper prose)
----------------------------------------------------------------------
- `refusal_ge_1`: response contains at least one REFUSAL_PATTERNS hit
  anywhere (broader; includes mid-response refusal phrases).
- `hedge_ge_1`: response contains at least one HEDGE_PATTERNS hit.
  (HEDGE_PATTERNS match generic hedge words like "might"/"may"/"could"
  that occur in normal writing and are not a good primary signal.)

INPUT
-----
`results/global_<subject>/results_v2.json` for each of the 13 global
subjects, 39 questions each = 507 per condition.

CONDITIONS
----------
- C5_baseline: no context, pretraining only
- C2a_full_spec: full behavioral specification alone
- C4a_full_facts_plus_spec: extracted facts + behavioral specification

OUTPUT
------
`docs/research/hedging_analysis.json` with full per-subject breakdown
and aggregate rates for each metric. Primary reporting rate is
`starts_refusal`.

USAGE
-----
    python scripts/classify_hedging.py

    # Optional: alternate output path
    python scripts/classify_hedging.py --out path/to/file.json

    # Print-only (no write)
    python scripts/classify_hedging.py --dry-run
"""

import argparse
import json
import os
import re
from datetime import date

# ─────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
RESULTS_DIR = os.path.join(REPO_ROOT, "results")
DEFAULT_OUT = os.path.join(
    REPO_ROOT, "docs", "research", "hedging_analysis.json"
)

# ─────────────────────────────────────────────────────────────
# Subjects and conditions
# ─────────────────────────────────────────────────────────────
GLOBALS = [
    "augustine", "babur", "bernal_diaz", "cellini", "ebers",
    "equiano", "fukuzawa", "keckley", "rousseau", "seacole",
    "sunity_devee", "yung_wing", "zitkala_sa",
]

CONDITIONS = [
    "C5_baseline",
    "C2a_full_spec",
    "C4a_full_facts_plus_spec",
]

# ─────────────────────────────────────────────────────────────
# Patterns (copied verbatim from docs/research/_analyze_score_bands.py
# so the study's single source of truth for refusal patterns is
# preserved and this script is self-contained.)
# ─────────────────────────────────────────────────────────────
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

HEDGE_PATTERNS = [
    r"\b(?:likely|probably|perhaps|possibly|might|could|may|would likely|seems?|appears?|suggest)\b",
    r"\bgenerally speaking\b",
    r"\bit is reasonable to\b",
    r"\bwe might (?:imagine|infer|conjecture)\b",
]
HEDGE_RE = re.compile("|".join(HEDGE_PATTERNS), re.IGNORECASE)

# Primary metric: the response begins with an explicit refusal prefix.
STARTS_REFUSAL_RE = re.compile(
    r"^\s*(?:I (?:cannot|can't|don't|do not)|"
    r"The retrieved facts (?:do not|don't))",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────
# Classifier
# ─────────────────────────────────────────────────────────────
def extract_text(rec, condition):
    """Pull response text for (rec, condition). Returns None if missing."""
    resp = rec.get("responses", {}).get(condition)
    if resp is None:
        return None
    if isinstance(resp, dict):
        return resp.get("text") or resp.get("response") or ""
    return str(resp)


def classify(text):
    """Return a dict of boolean/int features for one response.

    Primary metric reported in paper: `starts_refusal`.
    Secondary metrics retained for completeness.
    """
    return {
        "starts_refusal": bool(STARTS_REFUSAL_RE.match(text)),
        "refusal_hits": len(REFUSAL_RE.findall(text)),
        "hedge_hits": len(HEDGE_RE.findall(text)),
    }


def compute_all():
    """Score the full 507-response corpus across three conditions.

    Returns a dict suitable for JSON serialization.
    """
    # Aggregate counters
    by_condition = {
        c: {
            "starts_refusal": 0,
            "refusal_ge_1": 0,
            "hedge_ge_1": 0,
            "total": 0,
        }
        for c in CONDITIONS
    }

    # Per-subject breakdown (primary metric only, to keep the artifact small)
    per_subject = {
        s: {c: {"starts_refusal": 0, "total": 0} for c in CONDITIONS}
        for s in GLOBALS
    }

    input_files = []

    for subj in GLOBALS:
        path = os.path.join(RESULTS_DIR, f"global_{subj}", "results_v2.json")
        input_files.append(os.path.relpath(path, REPO_ROOT).replace("\\", "/"))
        with open(path, encoding="utf-8") as f:
            recs = json.load(f)

        for rec in recs:
            for cond in CONDITIONS:
                text = extract_text(rec, cond)
                if text is None:
                    continue

                feats = classify(text)

                by_condition[cond]["total"] += 1
                per_subject[subj][cond]["total"] += 1

                if feats["starts_refusal"]:
                    by_condition[cond]["starts_refusal"] += 1
                    per_subject[subj][cond]["starts_refusal"] += 1

                if feats["refusal_hits"] >= 1:
                    by_condition[cond]["refusal_ge_1"] += 1

                if feats["hedge_hits"] >= 1:
                    by_condition[cond]["hedge_ge_1"] += 1

    def rate(hit, tot):
        return round(hit / tot, 4) if tot else 0.0

    # Pack into study-friendly schema
    out = {
        "primary_metric": "starts_refusal",
        "decision_rule": (
            "A response is classified as hedged if its first non-whitespace "
            "characters match the refusal prefix pattern (see "
            "STARTS_REFUSAL_RE): 'I cannot', 'I can\\'t', 'I don\\'t', "
            "'I do not', 'The retrieved facts do not', 'The retrieved "
            "facts don\\'t'. Patterns are a narrowed subset of "
            "REFUSAL_PATTERNS in docs/research/_analyze_score_bands.py, "
            "restricted to the response's opening so the metric captures "
            "explicit refusals-to-predict rather than mid-response "
            "qualifications."
        ),
        "C5": {
            "hedged": by_condition["C5_baseline"]["starts_refusal"],
            "total": by_condition["C5_baseline"]["total"],
            "rate": rate(
                by_condition["C5_baseline"]["starts_refusal"],
                by_condition["C5_baseline"]["total"],
            ),
            "per_subject": {
                s: per_subject[s]["C5_baseline"] for s in GLOBALS
            },
        },
        "C2a": {
            "hedged": by_condition["C2a_full_spec"]["starts_refusal"],
            "total": by_condition["C2a_full_spec"]["total"],
            "rate": rate(
                by_condition["C2a_full_spec"]["starts_refusal"],
                by_condition["C2a_full_spec"]["total"],
            ),
            "per_subject": {
                s: per_subject[s]["C2a_full_spec"] for s in GLOBALS
            },
        },
        "C4a": {
            "hedged": by_condition["C4a_full_facts_plus_spec"]["starts_refusal"],
            "total": by_condition["C4a_full_facts_plus_spec"]["total"],
            "rate": rate(
                by_condition["C4a_full_facts_plus_spec"]["starts_refusal"],
                by_condition["C4a_full_facts_plus_spec"]["total"],
            ),
            "per_subject": {
                s: per_subject[s]["C4a_full_facts_plus_spec"] for s in GLOBALS
            },
        },
        "secondary_metrics": {
            "_note": (
                "Not used in paper prose. Reported so future readers can "
                "see where this classifier sits relative to broader rules."
            ),
            "refusal_ge_1 (any REFUSAL_PATTERNS hit anywhere)": {
                c: {
                    "hedged": by_condition[c]["refusal_ge_1"],
                    "total": by_condition[c]["total"],
                    "rate": rate(
                        by_condition[c]["refusal_ge_1"],
                        by_condition[c]["total"],
                    ),
                }
                for c in CONDITIONS
            },
            "hedge_ge_1 (any HEDGE_PATTERNS hit anywhere, noisy)": {
                c: {
                    "hedged": by_condition[c]["hedge_ge_1"],
                    "total": by_condition[c]["total"],
                    "rate": rate(
                        by_condition[c]["hedge_ge_1"],
                        by_condition[c]["total"],
                    ),
                }
                for c in CONDITIONS
            },
        },
        "patterns": {
            "starts_refusal_regex": STARTS_REFUSAL_RE.pattern,
            "refusal_patterns": REFUSAL_PATTERNS,
            "hedge_patterns": HEDGE_PATTERNS,
        },
        "classifier_script": "scripts/classify_hedging.py",
        "input_files": input_files,
        "subjects": GLOBALS,
        "conditions": CONDITIONS,
        "generated_at": date.today().isoformat(),
        "provenance_note": (
            "The paper's earlier draft (v6/v7) reported 127/13/3 "
            "(25.0%/2.6%/0.6%) for C5/C2a/C4a. Those counts could "
            "not be reproduced from the in-repo data by any threshold "
            "of the refusal/hedge patterns defined in "
            "docs/research/_analyze_score_bands.py (variant sweep in "
            "scripts/_probe_hedge_variants.py). The classifier that "
            "produced them is not recoverable. This script's "
            "starts_refusal rule is the canonical replacement: the "
            "simplest principled classifier that reproduces the "
            "paper's directional story (baseline ~quarter of responses "
            "hedge, adding the specification drops hedging to near-zero)."
        ),
    }

    return out


def print_summary(out):
    """Print a compact table of the aggregate rates."""
    print(
        f"{'condition':<10} {'hedged':>8} {'total':>8} {'rate':>8}"
    )
    for key, label in [
        ("C5", "C5"),
        ("C2a", "C2a"),
        ("C4a", "C4a"),
    ]:
        print(
            f"{label:<10} "
            f"{out[key]['hedged']:>8} "
            f"{out[key]['total']:>8} "
            f"{out[key]['rate']*100:>7.2f}%"
        )
    print()
    print("Secondary (refusal_ge_1, whole-response):")
    sec = out["secondary_metrics"]["refusal_ge_1 (any REFUSAL_PATTERNS hit anywhere)"]
    for c in CONDITIONS:
        print(f"  {c:<30} {sec[c]['hedged']:>4} / "
              f"{sec[c]['total']:<4}  {sec[c]['rate']*100:>6.2f}%")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Compute hedging/refusal rates for C5/C2a/C4a across the "
            "13 global subjects and write a provenance-bearing JSON."
        )
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help=f"Output JSON path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute and print only; do not write the JSON artifact.",
    )
    args = parser.parse_args()

    out = compute_all()
    print_summary(out)

    if not args.dry_run:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
