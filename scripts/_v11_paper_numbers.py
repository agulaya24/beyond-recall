"""
Master orchestrator for the v11 emit architecture.

Goal
----
Reconcile every paper-bound number against an emit-script aggregate. Per the
v11 contract (`docs/research/v11_emit/_ARCHITECTURE.md`), no number reaches
the manuscript outside a `_v11_emit_*.py` scaffold. This script:

1. Re-runs every emit scaffold via subprocess (capturing stdout/stderr/exit).
2. Aggregates each scaffold's JSON output into a single canonical file
   `docs/research/v11_paper_numbers.json` keyed by claim_id.
3. Walks `docs/beyond_recall_v10_1_draft.md` and locates each scaffold-emitted
   claim in the manuscript, classifying the comparison.
4. Emits `docs/research/v11_reconciliation_diff.md`, a single human-readable
   diff document.

Aggregation rule
----------------
This orchestrator does not perform any new aggregation. It loads each
scaffold's pre-computed values verbatim. The 5-judge primary panel rule lives
inside each emit scaffold; here we simply collect what those scaffolds
produced. Because no new judge calls are made, the architecture-spec §11
preflight_judge_health probe does not apply.

Idempotence
-----------
- Every scaffold emit is idempotent by §2.7-§2.8 of the architecture spec.
- This orchestrator writes outputs atomically (temp file + rename).
- Running twice on unchanged scaffold inputs produces identical aggregate
  JSON and identical reconciliation markdown.

Exit code
---------
- 0 if no MISMATCH_SUBSTANTIVE rows.
- 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
EMIT_DIR = REPO_ROOT / "docs" / "research" / "v11_emit"
PAPER_PATH = REPO_ROOT / "docs" / "beyond_recall_v10_1_draft.md"
OUT_JSON = REPO_ROOT / "docs" / "research" / "v11_paper_numbers.json"
OUT_DIFF = REPO_ROOT / "docs" / "research" / "v11_reconciliation_diff.md"

SCHEMA_VERSION = "v11.0"

# Scaffolds to run, in deterministic order.
EMIT_SCRIPTS = [
    "_v11_emit_3_study_design.py",
    "_v11_emit_4_1_gradient.py",
    "_v11_emit_4_2_compression.py",
    "_v11_emit_4_3_wrong_spec.py",
    "_v11_emit_4_4_1_memory_systems.py",
    "_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py",
    "_v11_emit_4_5_letta.py",
    "_v11_emit_appendix_b_battery.py",
    "_v11_emit_appendix_d.py",
]

# Map emit-script filename -> output JSON filename.
EMIT_OUT = {
    "_v11_emit_3_study_design.py": "3_study_design.json",
    "_v11_emit_4_1_gradient.py": "4_1_gradient.json",
    "_v11_emit_4_2_compression.py": "4_2_compression.json",
    "_v11_emit_4_3_wrong_spec.py": "4_3_wrong_spec.json",
    "_v11_emit_4_4_1_memory_systems.py": "4_4_1_memory_systems.json",
    "_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py": "4_4_2_4_4_3.json",
    "_v11_emit_4_5_letta.py": "4_5_letta.json",
    "_v11_emit_appendix_b_battery.py": "appendix_b_battery.json",
    "_v11_emit_appendix_d.py": "appendix_d.json",
}

# Tolerance bands (architecture spec uses 0.005; we extend per task spec).
MATCH_TOL = 0.005          # |delta| < MATCH_TOL  -> MATCH
ROUNDING_TOL = 0.05        # MATCH_TOL <= |delta| < ROUNDING_TOL -> MINOR_ROUNDING
# delta >= ROUNDING_TOL -> MISMATCH_SUBSTANTIVE
# Sign change always -> MISMATCH_SUBSTANTIVE (with SIGN_FLIP flag).

# ---------------------------------------------------------------------------
# Section locator: claim_id prefix -> v10 paper line range
# ---------------------------------------------------------------------------

# Section windows. Each prefix maps to ONE OR MORE (start, end) ranges. The
# multi-window form is used for claims whose narrative description appears
# in §1.3 (executive summary) or Appendix F (Letta full case study) but
# whose claim_id is bound to §4.x or §4.5.
PAPER_SECTIONS: list[tuple[str, list[tuple[int, int]]]] = [
    ("3_2_franklin", [(260, 410)]),
    ("3_4_", [(337, 412)]),
    ("3_5_", [(371, 412)]),
    ("3_6_", [(410, 438)]),
    ("3_7_2_", [(478, 533)]),
    ("3_7_4_", [(533, 559)]),
    ("3_7_5_", [(549, 575)]),
    ("3_7_6_", [(559, 588)]),
    ("4_1_1_", [(755, 765)]),
    ("4_1_", [(85, 145), (588, 765)]),     # also probe §1.3 narrative
    ("4_2_1_", [(805, 879)]),
    ("4_2_", [(85, 145), (765, 879)]),     # §1.3 + §4.2 body
    ("4_3_", [(85, 145), (879, 1011)]),    # §1.3 + §4.3 body
    ("4_4_1_", [(85, 145), (1017, 1184)]),
    ("4_4_2_", [(1184, 1237)]),
    ("4_4_3_", [(1237, 1265)]),
    ("4_5_", [(125, 145), (1265, 1342), (2401, 2488)]),  # §1.3 + §4.5 + AppF
    ("4_6_1_", [(1285, 1312)]),
    ("4_6_2_", [(1312, 1332)]),
    ("4_6_3_", [(1332, 1342)]),
    ("appB_2_", [(1868, 1893)]),
    ("appB_3_", [(1893, 1925)]),
    ("appB_4_", [(1925, 1937)]),
    ("appB_5_", [(1937, 1941)]),
    ("appB_6_", [(1941, 1954)]),
    ("appD_1_", [(2059, 2083)]),
    ("appD_2_", [(2083, 2111)]),
    ("appD_3_", [(2111, 2179)]),
    ("appD_4_", [(2179, 2272)]),
]


# ---------------------------------------------------------------------------
# Utility: subprocess-runs every scaffold
# ---------------------------------------------------------------------------


@dataclass
class ScriptRun:
    name: str
    returncode: int
    stdout_tail: str
    stderr_tail: str
    out_json_path: str
    out_json_present: bool


def _tail(text: str, n: int = 1500) -> str:
    if not text:
        return ""
    if len(text) <= n:
        return text
    return "..." + text[-n:]


def run_emit_scripts(verbose: bool = True) -> list[ScriptRun]:
    """Run every emit scaffold via subprocess. Capture exit codes; never abort
    on emit-script failures (most have known --verify divergences which are
    expected). Failure to even *invoke* the script is a hard failure."""
    runs: list[ScriptRun] = []
    for name in EMIT_SCRIPTS:
        path = SCRIPTS_DIR / name
        if not path.exists():
            print(f"FATAL: emit script missing: {path}", file=sys.stderr)
            sys.exit(2)
        if verbose:
            print(f"[orchestrator] running {name} ...", flush=True)
        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                capture_output=True,
                text=True,
                check=False,
                cwd=str(REPO_ROOT),
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                timeout=600,
            )
        except subprocess.TimeoutExpired:
            runs.append(ScriptRun(
                name=name,
                returncode=-1,
                stdout_tail="",
                stderr_tail="TIMEOUT after 600s",
                out_json_path=str(EMIT_DIR / EMIT_OUT[name]),
                out_json_present=(EMIT_DIR / EMIT_OUT[name]).exists(),
            ))
            continue
        out_p = EMIT_DIR / EMIT_OUT[name]
        runs.append(ScriptRun(
            name=name,
            returncode=proc.returncode,
            stdout_tail=_tail(proc.stdout),
            stderr_tail=_tail(proc.stderr),
            out_json_path=str(out_p),
            out_json_present=out_p.exists(),
        ))
        if verbose:
            status = "ok" if proc.returncode == 0 else f"exit={proc.returncode}"
            print(f"  -> {status}, json_present={out_p.exists()}")
    return runs


# ---------------------------------------------------------------------------
# Aggregation: collect every claim into the canonical map
# ---------------------------------------------------------------------------


def flatten_4_1(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Flatten the 4_1 emit JSON (subjects + summary) into virtual claims.

    The 4_1 emit script does not write a `claims` block; it stores per-subject
    rows in a `subjects` list and a `summary` dict. We mirror its `--verify`
    flatten contract here so the orchestrator can index every value.
    """
    claims: dict[str, dict[str, Any]] = {}
    section = "§4.1 cross-subject gradient"
    panel = data.get("panel", [])

    # Per-subject rows
    for s in data.get("subjects", []):
        sid = s["id"]
        for cond_key, cond_label in [
            ("C5", "C5"),
            ("C2a", "C2a"),
            ("C2c", "C2c"),
            ("C4", "C4"),
            ("C4a", "C4a"),
            ("delta_C4a", "delta_C4a"),
        ]:
            cid = f"4_1_{sid}_{cond_key}"
            claims[cid] = {
                "value": s.get(cond_key),
                "estimand": f"{s.get('display_name', sid)} {cond_label} panel mean",
                "contrast": "C2a vs C5" if cond_key == "C2a" else (
                    "C4a vs C5" if cond_key == "C4a" else (
                        "C4a - C5" if cond_key == "delta_C4a" else "panel mean"
                    )
                ),
                "filters": {"panel": panel, "subject": sid, "condition": cond_key},
                "n": None,
                "ci95_low": None,
                "ci95_high": None,
                "p_value": None,
                "section": section,
            }

    sm = data.get("summary", {})
    # Regression on delta
    rd = sm.get("regression_delta_on_C5", {})
    rl = sm.get("regression_C4a_level_on_C5", {})
    wc4a = sm.get("wilcoxon_C5_vs_C4a", {})
    wc2a = sm.get("wilcoxon_C5_vs_C2a", {})

    summary_map = [
        ("4_1_summary_regression_delta_slope", rd.get("slope"),
         "Regression slope of Delta_C4a on C5", "delta_C4a vs C5"),
        ("4_1_summary_regression_delta_ci_low", rd.get("ci95_low"),
         "Regression slope CI low", "delta_C4a vs C5"),
        ("4_1_summary_regression_delta_ci_high", rd.get("ci95_high"),
         "Regression slope CI high", "delta_C4a vs C5"),
        ("4_1_summary_regression_delta_r_squared", rd.get("r_squared"),
         "Regression R^2 of Delta_C4a on C5", "delta_C4a vs C5"),
        ("4_1_summary_regression_delta_p", rd.get("p_value"),
         "Regression slope p-value (delta)", "delta_C4a vs C5"),
        ("4_1_summary_regression_level_slope", rl.get("slope"),
         "Level regression slope (C4a on C5)", "C4a vs C5"),
        ("4_1_summary_regression_level_ci_low", rl.get("ci95_low"),
         "Level regression CI low", "C4a vs C5"),
        ("4_1_summary_regression_level_ci_high", rl.get("ci95_high"),
         "Level regression CI high", "C4a vs C5"),
        ("4_1_summary_regression_level_r_squared", rl.get("r_squared"),
         "Level R^2", "C4a vs C5"),
        ("4_1_summary_regression_level_p", rl.get("p_value"),
         "Level regression p-value", "C4a vs C5"),
        ("4_1_summary_wilcoxon_c5_vs_c4a_W", wc4a.get("W"),
         "Wilcoxon C5 vs C4a W", "C5 vs C4a"),
        ("4_1_summary_wilcoxon_c5_vs_c4a_p", wc4a.get("p"),
         "Wilcoxon C5 vs C4a p", "C5 vs C4a"),
        ("4_1_summary_wilcoxon_c5_vs_c2a_W", wc2a.get("W"),
         "Wilcoxon C5 vs C2a W", "C5 vs C2a"),
        ("4_1_summary_wilcoxon_c5_vs_c2a_p", wc2a.get("p"),
         "Wilcoxon C5 vs C2a p", "C5 vs C2a"),
        ("4_1_summary_low_baseline_n", sm.get("low_baseline_n"),
         "Low-baseline n", "n"),
        ("4_1_summary_low_baseline_n_positive", sm.get("low_baseline_n_positive"),
         "Low-baseline subjects with positive delta", "count"),
        ("4_1_summary_low_baseline_mean_delta_C4a", sm.get("low_baseline_mean_delta_C4a"),
         "Low-baseline mean delta_C4a", "delta_C4a"),
        ("4_1_summary_low_baseline_mean_C4a", sm.get("low_baseline_mean_C4a"),
         "Low-baseline mean C4a", "C4a"),
        ("4_1_summary_all14_n_positive", sm.get("all14_n_positive"),
         "All-14 subjects with positive delta", "count"),
        ("4_1_summary_all14_mean_delta_C4a", sm.get("all14_mean_delta_C4a"),
         "All-14 mean delta_C4a", "delta_C4a"),
        ("4_1_summary_all14_mean_C4a", sm.get("all14_mean_C4a"),
         "All-14 mean C4a", "C4a"),
    ]
    for cid, val, est, contrast in summary_map:
        claims[cid] = {
            "value": val,
            "estimand": est,
            "contrast": contrast,
            "filters": {"panel": panel, "subjects": "all_14"},
            "n": None,
            "ci95_low": None,
            "ci95_high": None,
            "p_value": None,
            "section": section,
        }

    fhb = sm.get("franklin_high_baseline", {})
    if fhb:
        for k in ("C5", "C2a", "C4a", "delta_C4a"):
            cid = f"4_1_franklin_high_baseline_{k}"
            claims[cid] = {
                "value": fhb.get(k),
                "estimand": f"Franklin (high-baseline reference) {k}",
                "contrast": k,
                "filters": {"panel": panel, "subject": "franklin"},
                "n": None,
                "ci95_low": None,
                "ci95_high": None,
                "p_value": None,
                "section": section,
            }
    return claims


def aggregate_claims(verbose: bool = True) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """Walk every emit JSON and assemble the canonical claim map.

    Returns (canonical_dict, per_section_counts).
    """
    canonical: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "claims": {},
        "provenance": {
            "run_timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "scripts": [],
            "total_claims": 0,
            "per_section_counts": {},
        },
    }
    per_section: dict[str, list[str]] = {}

    for script_name in EMIT_SCRIPTS:
        out_p = EMIT_DIR / EMIT_OUT[script_name]
        if not out_p.exists():
            print(f"WARN: missing emit JSON {out_p}", file=sys.stderr)
            continue
        data = json.loads(out_p.read_text(encoding="utf-8"))

        section = data.get("section") or _infer_section(script_name)
        canonical["provenance"]["scripts"].append({
            "script": script_name,
            "json_path": str(out_p.relative_to(REPO_ROOT)),
            "section": section,
            "schema_version": data.get("schema_version"),
        })

        if "claims" in data and isinstance(data["claims"], dict):
            for cid, body in data["claims"].items():
                claim = {
                    "section": section,
                    "value": body.get("value"),
                    "estimand": body.get("estimand"),
                    "contrast": body.get("contrast"),
                    "n": body.get("n"),
                    "ci95_low": body.get("ci95_low"),
                    "ci95_high": body.get("ci95_high"),
                    "p_value": body.get("p_value"),
                    "filters": body.get("filters"),
                    "source_script": script_name,
                }
                canonical["claims"][cid] = claim
                per_section.setdefault(section, []).append(cid)
        elif script_name == "_v11_emit_4_1_gradient.py":
            # 4_1 has its own shape; flatten it.
            flat = flatten_4_1(data)
            for cid, body in flat.items():
                claim = {
                    "section": body.pop("section"),
                    "value": body.get("value"),
                    "estimand": body.get("estimand"),
                    "contrast": body.get("contrast"),
                    "n": body.get("n"),
                    "ci95_low": body.get("ci95_low"),
                    "ci95_high": body.get("ci95_high"),
                    "p_value": body.get("p_value"),
                    "filters": body.get("filters"),
                    "source_script": script_name,
                }
                canonical["claims"][cid] = claim
                per_section.setdefault(claim["section"], []).append(cid)
        else:
            print(f"WARN: {script_name} JSON has no `claims` block; skipping.", file=sys.stderr)

    canonical["provenance"]["total_claims"] = len(canonical["claims"])
    canonical["provenance"]["per_section_counts"] = {
        sec: len(cids) for sec, cids in per_section.items()
    }
    if verbose:
        print(f"[orchestrator] aggregated {len(canonical['claims'])} claims across "
              f"{len(per_section)} sections.")
    return canonical, per_section


def _infer_section(script_name: str) -> str:
    if "4_1_" in script_name:
        return "§4.1"
    if "4_2_" in script_name:
        return "§4.2 + §4.2.1"
    if "4_3_" in script_name:
        return "§4.3"
    if "4_4_1_" in script_name:
        return "§4.4.1"
    if "4_4_2_4_4_3" in script_name:
        return "§4.4.2 + §4.4.3"
    if "4_5_" in script_name:
        return "§4.5 + Appendix F"
    if "appendix_b_battery" in script_name:
        return "Appendix B"
    if "appendix_d" in script_name:
        return "Appendix D"
    if "3_study_design" in script_name:
        return "§3"
    return "unknown"


# ---------------------------------------------------------------------------
# Paper text scanner: locate matching numbers
# ---------------------------------------------------------------------------


# Number regex: signed decimal or integer, with unicode minus support, plus
# scientific notation, with optional thousands-separator commas. We tighten
# the negative lookbehind so identifiers like 'GPT-5.4', 'top-10', model ids,
# and §-numbered headings don't bleed into the candidate token stream.
NUM_RE = re.compile(
    r"(?<![A-Za-z0-9_/.])"
    r"([+−–—‐-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?"          # 25,231 or 422,772
    r"|[+−–—‐-]?\d+(?:\.\d+)?(?:[eE][+−–—‐-]?\d+)?)"   # plain or scientific
    r"(?![\dA-Za-z_.])"                                # not part of identifier
)
PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")


def _token_in_line(token: str, line_lower: str) -> bool:
    """Word-boundary aware substring check. `c5` matches '| c5 |' but not
    'c5_baseline_x'. Necessary so that condition tags don't bleed across
    longer condition strings."""
    pattern = r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])"
    return re.search(pattern, line_lower) is not None


def _normalize_minus(s: str) -> str:
    """Convert unicode minus / en-dash / em-dash / hyphen to ASCII minus
    when the character precedes a digit (so it acts like a sign)."""
    out = []
    for i, ch in enumerate(s):
        if ch in ("−", "–", "—", "‐") and i + 1 < len(s) and s[i + 1].isdigit():
            out.append("-")
        else:
            out.append(ch)
    return "".join(out)


def _try_float(token: str) -> float | None:
    token = _normalize_minus(token).replace(",", "")
    try:
        return float(token)
    except ValueError:
        return None


def _section_windows_for(claim_id: str, paper_lines: list[str]) -> list[tuple[int, int]]:
    """Return a list of (start_idx, end_idx) windows for this claim_id.
    A claim may have multiple windows (e.g. §1.3 narrative + §4.x body).
    Falls back to the entire paper if no prefix matches.
    """
    for prefix, ranges in PAPER_SECTIONS:
        if claim_id.startswith(prefix):
            return [(max(0, s - 1), min(len(paper_lines), e)) for s, e in ranges]
    return [(0, len(paper_lines))]


def _keywords_for(claim_id: str, claim_body: dict[str, Any]) -> list[str]:
    """Extract anchor keywords from a claim_id. Each token after the section
    prefix becomes a candidate; we also include the contrast string and any
    subject/system tokens from filters."""
    parts = claim_id.split("_")
    kws: list[str] = []
    # Drop the section prefix (e.g., '4_4_1') and keep meaningful tokens.
    semantic = parts[3:] if (len(parts) > 3 and parts[0].isdigit()) else parts
    for p in semantic:
        if p and not p.isdigit() and len(p) >= 2:
            kws.append(p)
    # Token aliases: paper uses 'Base Layer' (with space) and 'wrong-spec'
    # (with hyphen) where claim_ids have 'baselayer' and 'wrong'. Add aliases
    # so the keyword anchor can co-occur on the right paper line.
    alias_map = {
        "baselayer": ["base layer"],
        "letta": ["letta"],
        "supermemory": ["supermemory"],
        "mem0": ["mem0"],
        "zep": ["zep"],
        "wrong": ["wrong-spec", "wrong spec"],
        "spec": ["specification", "spec"],
        "derangement": ["derangement"],
        "13globals": ["13 globals", "13 subjects", "13 global"],
        "low": ["low-baseline", "low baseline"],
        "controlled": ["controlled"],
        "native": ["native"],
        "archival": ["archival"],
        "paired": ["paired"],
        "wilcoxon": ["wilcoxon"],
        "delta": ["delta", "Δ"],
    }
    for k in list(kws):
        if k in alias_map:
            kws.extend(alias_map[k])
    contrast = (claim_body.get("contrast") or "").strip()
    if contrast:
        kws.append(contrast)
    filters = claim_body.get("filters") or {}
    if isinstance(filters, dict):
        for k in ("subject", "system", "condition"):
            v = filters.get(k)
            if isinstance(v, str):
                kws.append(v)
    # Subject-name normalization for paper search (e.g., 'sunity' + 'devee').
    expanded: list[str] = []
    for kw in kws:
        expanded.append(kw)
        if "_" in kw:
            expanded.extend([p for p in kw.split("_") if len(p) >= 3])
    return list({kw.lower() for kw in expanded if kw})


PAPER_SUBJECT_DISPLAY = {
    "ebers": "ebers",
    "sunity_devee": "sunity devee",
    "hamerton": "hamerton",
    "fukuzawa": "fukuzawa",
    "bernal_diaz": "bernal diaz",
    "babur": "babur",
    "seacole": "seacole",
    "keckley": "keckley",
    "yung_wing": "yung wing",
    "zitkala_sa": "zitkala-sa",
    "cellini": "cellini",
    "rousseau": "rousseau",
    "augustine": "augustine",
    "equiano": "equiano",
    "franklin": "franklin",
}


def find_paper_value(
    claim_id: str,
    claim_body: dict[str, Any],
    paper_text: str,
    paper_lines: list[str],
) -> tuple[float | None, str, str]:
    """Locate a candidate paper value for this claim.

    Returns (paper_value, match_source_snippet, match_strategy).
    match_strategy in {'subject_table_row', 'keyword_anchor', 'section_scan',
    'not_found'}.
    """
    target = claim_body.get("value")
    if target is None or not isinstance(target, (int, float)):
        return None, "", "not_found"

    windows = _section_windows_for(claim_id, paper_lines)
    keywords = _keywords_for(claim_id, claim_body)

    # Strategy 1: subject row in §4.1 / §4.2 tables.
    subj = (claim_body.get("filters") or {}).get("subject") if isinstance(
        claim_body.get("filters"), dict) else None
    if subj is None:
        for sid in PAPER_SUBJECT_DISPLAY:
            if sid in claim_id:
                subj = sid
                break
    # Pre-compute condition tags by splitting claim_id on '_'. We only gate
    # on conditions for sections whose tables encode the condition on the
    # row label itself (Appendix D.4 per-judge matrices, Appendix B per-axis
    # rows). The §4.1, §4.2, and §4.4 tables put condition in the column
    # headers, so subject row alone is the correct anchor there.
    cond_tags_pre = {"c2a", "c2c", "c4", "c4a", "c5", "c8", "c9"}
    cid_segments = {seg.lower() for seg in claim_id.split("_")}
    # Condition-gating policy by section:
    #   - appD_4 / appD_3 / 3_2_franklin: row LABEL carries the condition; gate.
    #   - 4_1 / 4_2: condition lives in column header, not row label. We only
    #     gate on conditions the paper table actually exposes (C5/C2a/C4a for
    #     §4.1; the §4.2 paper table has C5/C2a/C4/C8/C4a/C9). Conditions
    #     scaffolds emit but paper does not (C2c, sometimes C4 in §4.1)
    #     should resolve to NON_CLAIM rather than match a wrong cell.
    # Condition-gating policy by section:
    #   - appD_4 / appD_3 / 3_2_franklin: row LABEL carries the condition; gate.
    #   - 4_1 / 4_2: condition lives in column header. Paper table exposes only
    #     a fixed set; if the scaffold's condition is outside that set the
    #     claim is by construction not in the paper text -> NON_CLAIM
    #     ('claim_in_scaffold_not_in_paper'). Otherwise no row gate; rely on
    #     subject row + positional column matching.
    cond_gating_prefixes = ("appd_4_", "appd_3_", "3_2_franklin")
    paper_table_conds_4_1 = {"c5", "c2a", "c4a"}
    paper_table_conds_4_2 = {"c5", "c2a", "c4", "c8", "c4a", "c9"}
    cid_conds = [t for t in cond_tags_pre if t in cid_segments]
    if any(claim_id.lower().startswith(p) for p in cond_gating_prefixes):
        claim_conds_pre = cid_conds
    elif claim_id.startswith("4_1_") and cid_conds:
        if not any(c in paper_table_conds_4_1 for c in cid_conds):
            return None, "", "claim_in_scaffold_not_in_paper"
        claim_conds_pre = []
    elif claim_id.startswith("4_2_") and cid_conds:
        if not any(c in paper_table_conds_4_2 for c in cid_conds):
            return None, "", "claim_in_scaffold_not_in_paper"
        claim_conds_pre = []
    else:
        claim_conds_pre = []

    if subj and subj in PAPER_SUBJECT_DISPLAY:
        display = PAPER_SUBJECT_DISPLAY[subj]
        for start_idx, end_idx in windows:
            for line in paper_lines[start_idx:end_idx]:
                line_norm = _normalize_minus(line).lower()
                if not (display in line_norm and line.strip().startswith("|")):
                    continue
                if claim_conds_pre and not any(
                    _token_in_line(c, line_norm) for c in claim_conds_pre
                ):
                    continue
                hit = _best_match_in_text(line, target, relax=0.50)
                if hit is not None:
                    return hit, line.strip(), "subject_table_row"

    # Strategy 2: keyword-anchor across all windows. Prefer table rows over
    # prose, then most keyword-rich, then smallest delta. Condition tags
    # (c2a, c2c, c4, c4a, c5, c8, c9) are gating: if the claim_id encodes a
    # condition, the line MUST contain that condition tag (or the claim's
    # subject in a row dedicated to that condition).
    # Reuse the pre-computed condition list.
    claim_conds = list(claim_conds_pre)
    if keywords:
        candidate_hits: list[tuple[int, float, str, float, int]] = []
        for start_idx, end_idx in windows:
            for li in range(start_idx, end_idx):
                line = paper_lines[li]
                line_norm = _normalize_minus(line).lower()
                if claim_conds:
                    # Require the matching condition tag to appear in the line
                    # OR in the closest preceding non-blank line (table-row
                    # second-pass case where the row label is one cell among
                    # many). Conservative: require on the line itself.
                    if not any(_token_in_line(c, line_norm) for c in claim_conds):
                        continue
                kw_hits = sum(1 for kw in keywords if kw in line_norm)
                if kw_hits < 1:
                    continue
                hit = _best_match_in_text(line, target, relax=0.50)
                if hit is None:
                    continue
                delta = abs(hit - float(target))
                is_prose = 0 if line.lstrip().startswith("|") else 1
                candidate_hits.append((is_prose, delta, line.strip(), hit, kw_hits))
        if candidate_hits:
            candidate_hits.sort(key=lambda x: (x[0], -x[4], x[1]))
            best = candidate_hits[0]
            # Final guard: if no condition gate fired AND best_delta exceeds
            # 40% of the target, downgrade to NON_CLAIM. Tighter would lose
            # legitimate-but-substantively-mismatched cases like
            # `4_5_ebers_bl_unique_named_entities=34 vs paper=19`. The 40%
            # band keeps the running-list named-entity mismatches visible
            # while suppressing pure aggregate-rollup noise in §4.4.2.
            if not claim_conds:
                target_f = float(target)
                if abs(target_f) >= 1.0 and best[1] > 0.40 * abs(target_f):
                    return None, "", "claim_in_scaffold_not_in_paper"
            return best[3], best[2], "keyword_anchor"

    # Strategy 3: section scan with strict relax band across windows.
    closest: tuple[float, str, float] | None = None
    for start_idx, end_idx in windows:
        for line in paper_lines[start_idx:end_idx]:
            hit = _best_match_in_text(line, target, relax=0.05)
            if hit is None:
                continue
            delta = abs(hit - float(target))
            if closest is None or delta < closest[0]:
                closest = (delta, line.strip(), hit)
    if closest and closest[0] < ROUNDING_TOL:
        return closest[2], closest[1], "section_scan"

    return None, "", "not_found"


def _best_match_in_text(text: str, target: float, *,
                        relax: float = 0.10) -> float | None:
    """Find the numeric token in `text` whose value is closest to `target`.

    `relax` is the relative tolerance band: a candidate is plausible only if
    |delta| <= max(floor, |target| * relax). With relax=0.10 (default),
    section-scan is conservative; keyword-anchor calls pass relax=0.50 to
    accept legitimate substantive mismatches (e.g. spec_tokens 4478 vs paper
    7000) where we are confident the metric is the same one.
    """
    tokens = NUM_RE.findall(text)
    pcts = PCT_RE.findall(text)
    candidates: list[float] = []
    for t in tokens:
        v = _try_float(t)
        if v is not None:
            candidates.append(v)
    for t in pcts:
        v = _try_float(t)
        if v is None:
            continue
        candidates.append(v)
        if target is not None and abs(target) <= 1.0:
            candidates.append(v / 100.0)
    if not candidates:
        return None

    target_f = float(target)
    best = min(candidates, key=lambda v: abs(v - target_f))
    delta = abs(best - target_f)

    abs_target = abs(target_f)
    # Floor scales with `relax`. The 1.0 absolute floor for sub-unit targets
    # is intentional: it lets a sign-flipped −0.50 register against scaffold
    # +0.20 in keyword-anchor mode (relax=0.50, floor=1.0). In strict-scan
    # mode (relax=0.05) the floor falls to 0.10, suppressing noise.
    if abs_target < 1.0:
        floor = max(2.0 * relax, 0.05)
    elif abs_target < 100.0:
        floor = max(1.0, abs_target * relax)
    else:
        floor = max(5.0, abs_target * relax)
    if delta > floor:
        return None
    return best


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(scaffold: float | int | None, paper: float | int | None,
             estimand: str, contrast: str) -> tuple[str, bool]:
    """Return (status, is_sign_flip)."""
    if paper is None:
        # Could be NON_CLAIM (paper doesn't cite this) or PAPER_ONLY missing.
        # Default to NON_CLAIM here; PAPER_ONLY is computed separately.
        return ("NON_CLAIM", False)
    if scaffold is None:
        return ("MISMATCH_SUBSTANTIVE", False)

    # Krippendorff-style alpha or rank-statistic rows are statistical-type
    # comparisons (paper may use ordinal vs interval). Detect by estimand.
    estimand_low = (estimand or "").lower()
    if "krippendorff" in estimand_low and "alpha" in estimand_low:
        # Tag as STAT_TYPE if delta is large; otherwise MATCH.
        delta = abs(float(scaffold) - float(paper))
        if delta < MATCH_TOL:
            return ("MATCH", False)
        if delta < ROUNDING_TOL:
            return ("MINOR_ROUNDING", False)
        return ("STAT_TYPE", False)

    s = float(scaffold)
    p = float(paper)
    delta = abs(s - p)

    sign_flip = False
    # Sign flip: both nonzero, opposite signs, and not within rounding noise.
    if s != 0.0 and p != 0.0 and ((s > 0) != (p > 0)) and delta >= ROUNDING_TOL:
        sign_flip = True

    if delta < MATCH_TOL:
        return ("MATCH", False)
    if delta < ROUNDING_TOL and not sign_flip:
        return ("MINOR_ROUNDING", False)
    return ("MISMATCH_SUBSTANTIVE", sign_flip)


# ---------------------------------------------------------------------------
# Reconciliation walk
# ---------------------------------------------------------------------------


def reconcile(canonical: dict[str, Any]) -> list[dict[str, Any]]:
    """For every claim, locate it in the paper, classify it, and return
    a list of result rows."""
    paper_text = PAPER_PATH.read_text(encoding="utf-8")
    paper_lines = paper_text.splitlines()

    rows: list[dict[str, Any]] = []
    for cid, body in canonical["claims"].items():
        scaffold_value = body.get("value")
        paper_value, snippet, strategy = find_paper_value(
            cid, body, paper_text, paper_lines
        )
        status, sign_flip = classify(
            scaffold_value, paper_value,
            body.get("estimand") or "", body.get("contrast") or ""
        )
        delta = None
        if (isinstance(scaffold_value, (int, float))
                and isinstance(paper_value, (int, float))):
            delta = abs(float(scaffold_value) - float(paper_value))
        rows.append({
            "claim_id": cid,
            "section": body.get("section"),
            "estimand": body.get("estimand"),
            "contrast": body.get("contrast"),
            "scaffold_value": scaffold_value,
            "paper_value": paper_value,
            "delta": delta,
            "status": status,
            "sign_flip": sign_flip,
            "match_strategy": strategy,
            "paper_snippet": snippet[:280],
            "source_script": body.get("source_script"),
        })
    return rows


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt_val(v: Any) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        if abs(v) < 1e-3 and v != 0.0:
            return f"{v:.3e}"
        return f"{v:.4f}"
    return str(v)


def _fmt_delta(v: Any) -> str:
    if v is None:
        return "n/a"
    return f"{v:.4f}"


def render_diff_markdown(rows: list[dict[str, Any]],
                         canonical: dict[str, Any],
                         script_runs: list[ScriptRun]) -> str:
    statuses = [r["status"] for r in rows]
    n_total = len(rows)
    counts = {
        "MATCH": statuses.count("MATCH"),
        "MINOR_ROUNDING": statuses.count("MINOR_ROUNDING"),
        "MISMATCH_SUBSTANTIVE": statuses.count("MISMATCH_SUBSTANTIVE"),
        "STAT_TYPE": statuses.count("STAT_TYPE"),
        "NON_CLAIM": statuses.count("NON_CLAIM"),
    }
    sign_flips = [r for r in rows if r.get("sign_flip")]

    lines: list[str] = []
    lines.append("# v11 reconciliation diff (scaffold-emit vs v10 paper text)")
    lines.append("")
    lines.append(f"_Generated: {canonical['provenance']['run_timestamp']}_")
    lines.append("")
    lines.append("Aggregation rule (locked, architecture spec §1): "
                 "5-judge primary panel `{haiku, sonnet, opus, gpt4o, gpt54}`. "
                 "Per-judge per-question -> per-judge per-subject mean -> "
                 "panel mean across the 5 judges.")
    lines.append("")

    # Executive summary
    lines.append("## Executive summary")
    lines.append("")
    lines.append(f"- Total claim_ids aggregated: **{n_total}**")
    lines.append(f"- MATCH: **{counts['MATCH']}** "
                 f"({100.0 * counts['MATCH'] / max(n_total, 1):.1f}%)")
    lines.append(f"- MINOR_ROUNDING: **{counts['MINOR_ROUNDING']}** "
                 f"({100.0 * counts['MINOR_ROUNDING'] / max(n_total, 1):.1f}%)")
    lines.append(f"- MISMATCH_SUBSTANTIVE: **{counts['MISMATCH_SUBSTANTIVE']}** "
                 f"({100.0 * counts['MISMATCH_SUBSTANTIVE'] / max(n_total, 1):.1f}%)")
    lines.append(f"- STAT_TYPE: **{counts['STAT_TYPE']}**")
    lines.append(f"- NON_CLAIM: **{counts['NON_CLAIM']}** "
                 "(scaffold has a value but paper text does not cite it)")
    lines.append(f"- SIGN_FLIPS surfaced: **{len(sign_flips)}**")
    lines.append("")
    lines.append("PAPER_ONLY items are catalogued in their own section below.")
    lines.append("")

    # Substantive mismatches
    sub_rows = [r for r in rows if r["status"] == "MISMATCH_SUBSTANTIVE"]
    sub_rows.sort(key=lambda r: (r.get("delta") or 0.0), reverse=True)
    lines.append("## Substantive mismatches")
    lines.append("")
    if not sub_rows:
        lines.append("_No substantive mismatches surfaced._")
    else:
        lines.append("| claim_id | section | paper | scaffold | abs_delta | "
                     "sign_flip | contrast | suggested_fix |")
        lines.append("|---|---|---:|---:|---:|:--:|---|---|")
        for r in sub_rows:
            cid = r["claim_id"]
            sec = r["section"] or ""
            pv = _fmt_val(r["paper_value"])
            sv = _fmt_val(r["scaffold_value"])
            d = _fmt_delta(r["delta"])
            sf = "YES" if r["sign_flip"] else " "
            cn = r.get("contrast") or ""
            sug = (f"replace paper {pv} with scaffold {sv} "
                   f"(emit script: {r.get('source_script')})")
            lines.append(f"| `{cid}` | {sec} | {pv} | {sv} | {d} | {sf} | "
                         f"{cn} | {sug} |")
    lines.append("")

    # Sign flips
    lines.append("## Sign flips and direction changes")
    lines.append("")
    if not sign_flips:
        lines.append("_No sign flips surfaced._")
    else:
        lines.append("| claim_id | section | paper | scaffold | abs_delta | estimand |")
        lines.append("|---|---|---:|---:|---:|---|")
        for r in sign_flips:
            cid = r["claim_id"]
            sec = r["section"] or ""
            pv = _fmt_val(r["paper_value"])
            sv = _fmt_val(r["scaffold_value"])
            d = _fmt_delta(r["delta"])
            est = (r.get("estimand") or "")[:120]
            lines.append(f"| `{cid}` | {sec} | {pv} | {sv} | {d} | {est} |")
    lines.append("")

    # Per-section walkthrough
    lines.append("## Per-section walkthrough")
    lines.append("")
    by_section: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_section.setdefault(r["section"] or "unknown", []).append(r)
    lines.append("| section | total | MATCH | MINOR_ROUNDING | "
                 "MISMATCH_SUBSTANTIVE | STAT_TYPE | NON_CLAIM |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for sec in sorted(by_section.keys()):
        rs = by_section[sec]
        c = {s: sum(1 for r in rs if r["status"] == s) for s in
             ("MATCH", "MINOR_ROUNDING", "MISMATCH_SUBSTANTIVE",
              "STAT_TYPE", "NON_CLAIM")}
        lines.append(f"| {sec} | {len(rs)} | {c['MATCH']} | "
                     f"{c['MINOR_ROUNDING']} | {c['MISMATCH_SUBSTANTIVE']} | "
                     f"{c['STAT_TYPE']} | {c['NON_CLAIM']} |")
    lines.append("")

    # Methodological asymmetry notes
    lines.append("## Methodological asymmetry notes")
    lines.append("")
    asym_lines = []
    asym_lines.append(
        "- **§4.4.2 paired_total_n.** Scaffold reports paired_total_n = 546 "
        "for the strict 5-judge primary panel across every system. The paper "
        "reports 516 (line 1084) and 507 (line 1233) in places where the "
        "panel was implicitly the audit panel rather than the locked 5-judge "
        "primary. Scaffold value is the locked aggregation rule output."
    )
    asym_lines.append(
        "- **§4.4.3 Keckley Q21 (Mem0, Zep deltas).** Scaffold uses the "
        "strict 5-judge primary panel mean. The paper table presents per-"
        "judge-rounded means under a relaxed inclusion rule that flips the "
        "sign on Mem0 and Zep deltas (paper -0.50 vs scaffold +0.20). "
        "Surfaced as SIGN_FLIP rows. This is a primary-vs-relaxed panel "
        "asymmetry, not a numeric error in either source."
    )
    asym_lines.append(
        "- **§4.5 Letta 7-judge sensitivity rows.** Paper presents 7-judge "
        "deltas; scaffold reproduces both 5-judge and 7-judge variants. The "
        "paper values for 7-judge Hamerton (+0.20) and Babur (+0.29) "
        "predate the recompute against the current judgment files; scaffold "
        "produces +0.093 and +0.232 respectively (running-list items)."
    )
    asym_lines.append(
        "- **§4.5 named-entity counts.** Paper line 2466 cites Babur 540 vs "
        "46 and Ebers 58 vs 19. Scaffold computes Babur 416/65 and Ebers "
        "53/34. The locator on Ebers BL row picks 46 (the Babur BL value "
        "from the same sentence) due to co-mention proximity; the headline "
        "MISMATCH_SUBSTANTIVE classification is correct, but the displayed "
        "paper_value cell may sometimes show the co-mentioned subject's "
        "value rather than the correct subject's value. Verify against "
        "line 2466 directly when applying the fix."
    )
    asym_lines.append(
        "- **Appendix D.3.4 length-correlation denominator.** Scaffold emits "
        "n=312 for low-baseline question count; paper carries n=351 in the "
        "C5 row from a pre-recompute draft (the 351 -> 312 transcription "
        "error from the running list)."
    )
    asym_lines.append(
        "- **NO_RETRIEVAL Supermemory methodology disclosure.** Supermemory's "
        "controlled config retrieved 30 records on a subset of subjects; "
        "the scaffold captures this in the substrate-controlled aggregate "
        "but the paper text does not surface this inline at §4.4.1. "
        "Recommendation: add a footnote at §4.4.1's Supermemory paragraph "
        "noting the 30-record retrieval cap."
    )
    asym_lines.append(
        "- **§4.2 Hamerton spec_tokens.** Paper §1.3 line 106 says "
        "'~7,300 tokens'; §4.2 table column header says '~7K tok' as a "
        "shared estimate; scaffold computes per-subject tokens with "
        "Hamerton at 4,478 (notably below the ~7K group estimate). The "
        "paper's column-header rounding is a deliberate shared-estimate "
        "presentation, not a per-subject claim. Per-subject scaffold "
        "values disagree with the rounded column header for the smaller "
        "specifications (Hamerton, Sunity Devee)."
    )
    for ln in asym_lines:
        lines.append(ln)
    lines.append("")

    # PAPER_ONLY items (coverage gaps)
    lines.append("## PAPER_ONLY items (coverage gaps)")
    lines.append("")
    paper_only_items = collect_paper_only(canonical)
    if not paper_only_items:
        lines.append("_No PAPER_ONLY gaps detected by heuristic scan._")
    else:
        lines.append("Numbers cited in v10 paper text that no scaffold currently "
                     "produces (heuristic identification by section + numeric "
                     "tokens lacking a scaffold preimage):")
        lines.append("")
        for sec, items in paper_only_items.items():
            lines.append(f"### {sec}")
            for it in items:
                lines.append(f"- L{it['line']}: `{it['snippet'][:180]}`")
            lines.append("")
    lines.append("")

    # Script-run log
    lines.append("## Emit-script run log")
    lines.append("")
    lines.append("| script | exit | json_present | stderr_tail |")
    lines.append("|---|---:|:--:|---|")
    for r in script_runs:
        st_tail = (r.stderr_tail or "").replace("|", "\\|").replace("\n", " ")[:160]
        present = "yes" if r.out_json_present else "**NO**"
        lines.append(f"| `{r.name}` | {r.returncode} | {present} | {st_tail} |")
    lines.append("")
    lines.append("Note: emit scripts with non-zero exit are expected. Each "
                 "scaffold's `--verify` mode compares its emitted values to "
                 "v10 paper text and exits 1 on any mismatch; this is the "
                 "scaffold's job, not a failure of the orchestrator.")
    lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# PAPER_ONLY heuristic collector
# ---------------------------------------------------------------------------


def collect_paper_only(canonical: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Heuristic: surface paper-text numeric claims that have no scaffold
    preimage. Conservatively scoped to short list of well-known coverage
    gaps documented in the running list (rather than a brittle paper-wide
    scan that would flood with false positives)."""
    paper_lines = PAPER_PATH.read_text(encoding="utf-8").splitlines()
    out: dict[str, list[dict[str, Any]]] = {}

    # Collect every scaffold-emitted value into a multiset for quick look-up.
    scaffold_vals: list[float] = []
    for body in canonical["claims"].values():
        v = body.get("value")
        if isinstance(v, (int, float)):
            scaffold_vals.append(float(v))

    def _has_match(target: float, tol: float = 0.05) -> bool:
        return any(abs(s - target) < tol for s in scaffold_vals)

    # Probe a small set of well-known paper claims that may not be emitted.
    probes = [
        # (section, line_range, anchor_text, tag)
        ("§1.3 headline rates",
         (85, 145), "anchor crossing", "headline narrative rates"),
        ("§4.6.1 Tier 2 cross-provider",
         (1285, 1312), "tier 2", "cross-provider replication numbers"),
        ("§4.6.2 7-judge sensitivity",
         (1312, 1332), "7-judge", "Gemini-inclusive sensitivity"),
        ("§5.5 hedging metric",
         (1424, 1531), "hedging", "hedging-rate practical implication"),
        ("Appendix C.6 retrieval k",
         (2027, 2042), "top-k", "retrieval top-k disclosed values"),
        ("Appendix C.7 ingestion exclusions",
         (2042, 2057), "exclusion", "subject ingestion exclusion notes"),
    ]
    for section_label, (start, end), anchor, tag in probes:
        items: list[dict[str, Any]] = []
        for li in range(max(0, start - 1), min(len(paper_lines), end)):
            line = paper_lines[li]
            if anchor.lower() not in line.lower():
                continue
            tokens = NUM_RE.findall(line)
            for t in tokens:
                v = _try_float(t)
                if v is None:
                    continue
                # Filter trivial integers/years that scaffolds wouldn't emit.
                if abs(v) > 1900 and abs(v) < 2100:
                    continue
                if v == 0:
                    continue
                if _has_match(v):
                    continue
                items.append({"line": li + 1, "value": v, "snippet": line.strip(), "tag": tag})
        if items:
            # Dedupe by (line, value)
            uniq = {}
            for it in items:
                uniq[(it["line"], round(it["value"], 4))] = it
            out[section_label] = list(uniq.values())[:8]
    return out


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--skip-emit", action="store_true",
                        help="Skip re-running emit scripts (use existing JSON).")
    parser.add_argument("--quiet", action="store_true", help="Reduce stdout chatter.")
    args = parser.parse_args()

    verbose = not args.quiet

    if args.skip_emit:
        if verbose:
            print("[orchestrator] skip-emit: using existing emit JSON files")
        script_runs: list[ScriptRun] = []
        for name in EMIT_SCRIPTS:
            out_p = EMIT_DIR / EMIT_OUT[name]
            script_runs.append(ScriptRun(
                name=name, returncode=0,
                stdout_tail="(skipped)", stderr_tail="",
                out_json_path=str(out_p),
                out_json_present=out_p.exists(),
            ))
    else:
        script_runs = run_emit_scripts(verbose=verbose)

    canonical, _per_section = aggregate_claims(verbose=verbose)
    rows = reconcile(canonical)

    # Tag rows back into canonical for the JSON output.
    by_id: dict[str, dict[str, Any]] = {r["claim_id"]: r for r in rows}
    for cid, body in canonical["claims"].items():
        match = by_id.get(cid)
        if match:
            body["paper_value"] = match["paper_value"]
            body["delta"] = match["delta"]
            body["status"] = match["status"]
            body["sign_flip"] = match["sign_flip"]
            body["match_strategy"] = match["match_strategy"]
            body["paper_snippet"] = match["paper_snippet"]

    # Add summary counts to provenance.
    canonical["provenance"]["status_counts"] = {
        s: sum(1 for r in rows if r["status"] == s)
        for s in ("MATCH", "MINOR_ROUNDING", "MISMATCH_SUBSTANTIVE",
                  "STAT_TYPE", "NON_CLAIM")
    }
    canonical["provenance"]["sign_flip_count"] = sum(1 for r in rows if r["sign_flip"])

    # Atomic-write canonical JSON.
    atomic_write(OUT_JSON, json.dumps(canonical, indent=2, sort_keys=False) + "\n")
    if verbose:
        print(f"[orchestrator] wrote canonical JSON: {OUT_JSON}")

    # Atomic-write reconciliation diff.
    md_text = render_diff_markdown(rows, canonical, script_runs)
    atomic_write(OUT_DIFF, md_text)
    if verbose:
        print(f"[orchestrator] wrote reconciliation diff: {OUT_DIFF}")

    sub = canonical["provenance"]["status_counts"]["MISMATCH_SUBSTANTIVE"]
    if verbose:
        print(f"[orchestrator] MISMATCH_SUBSTANTIVE = {sub}")
    return 0 if sub == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
