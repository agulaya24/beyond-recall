"""
Emit script for §4.4.1 (Aggregate performance across memory systems) of the Beyond Recall paper.

Aggregation rule: 5-judge primary (per-judge per-question -> per-judge per-subject mean -> panel mean
across {haiku, sonnet, opus, gpt4o, gpt54}). 7-judge sensitivity is reported in the existing
analysis docs but is NOT the primary aggregate per the v11 architecture spec (§1).

Outputs:
  docs/research/v11_emit/4_4_1_memory_systems.json  (per the v11 schema)
  docs/research/v11_emit/4_4_1_memory_systems.md    (side-by-side scaffold-vs-paper view)

Verification: python scripts/_v11_emit_4_4_1_memory_systems.py --verify
              compares emitted values to v10 paper §4.4.1 numbers and exits 1 on any MISMATCH.

PROVENANCE NOTES (load-bearing for this section):

  1. Native condition strings: primary data uses the suffix `_fp` (not `_native` as
     listed in the v11 architecture spec §7). The data is the source of truth; this
     script reads `C1_<system>_fp` / `C3_<system>_fp` and flags the architecture-spec
     correction in the output.

  2. Supermemory native paid-tier rerun (the 4 originally-failed subjects: babur,
     bernal_diaz, cellini, rousseau) was completed on 2026-04-23 and judged through
     all 7 judges. Those judgments live ONLY at the canonical script-local path:
       C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results/global_<subject>/
     and have NOT been mirrored into the study repo. The paper (§4.4.1) and the
     existing scripts/compute_supermemory_paid_tier_aggregate.py read from the
     canonical path for those 4 subjects. This emit script does the same.

  3. Hamerton's supermemory_fullpipeline judgments live ONLY at the study-repo mirror
     (results/hamerton/). Hamerton native is included to match paper coverage (n=14).

  4. Base Layer has no native variant (it IS the authored pipeline). Native-config
     claim_ids for baselayer_substrate are emitted with value=null and an explicit
     note in provenance.

  5. Aggregation parse-failure rule: rows with parse_failure=True are excluded before
     judge means are computed. This matches the existing study-wide convention
     (compute_memory_systems_5judge.py, recompute_5judge_primary.py).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ---------- Paths ----------

REPO = Path(__file__).resolve().parent.parent
STUDY_RESULTS = REPO / 'results'
BACKFILL_DIR = STUDY_RESULTS / '_s114_backfills'
CANONICAL_RESULTS = Path('C:/Users/Aarik/Anthropic/memory_system/data/experiments/memory_systems/results')
OUT_DIR = REPO / 'docs' / 'research' / 'v11_emit'
OUT_JSON = OUT_DIR / '4_4_1_memory_systems.json'
OUT_MD = OUT_DIR / '4_4_1_memory_systems.md'
PAPER = REPO / 'docs' / 'beyond_recall_v10_1_draft.md'

SCRIPT_VERSION = 'v11.0.0-2026-04-25'
SCRIPT_PATH_REL = 'scripts/_v11_emit_4_4_1_memory_systems.py'


# ---------- Locked study constants ----------

PRIMARY_JUDGES = {'haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54'}
GEMINI_JUDGES = {'gemini_flash', 'gemini_pro'}
ALL_JUDGES = PRIMARY_JUDGES | GEMINI_JUDGES
JUDGE_FILES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']
SENSITIVITY_JUDGE_FILES = ['gemini_flash', 'gemini_pro']

# Main study: 14 subjects (Hamerton + 13 globals)
GLOBAL_SUBJECTS = [
    'sunity_devee', 'ebers', 'fukuzawa', 'seacole', 'bernal_diaz',
    'keckley', 'yung_wing', 'babur', 'cellini', 'zitkala_sa',
    'rousseau', 'augustine', 'equiano',
]
MAIN_STUDY = ['hamerton'] + GLOBAL_SUBJECTS

# Low-baseline slice: 9 subjects with 5-judge C5 <= 2.0 (per recompute_5judge_primary.md).
LOW_BASELINE_SUBJECTS = {
    'ebers', 'sunity_devee', 'hamerton', 'fukuzawa', 'bernal_diaz',
    'babur', 'seacole', 'keckley', 'yung_wing',
}

# Systems. Note: paper uses display name "Base Layer substrate" but data prefix is "baselayer".
# Claim ids use the task-specified canonical name "baselayer_substrate" with internal
# data prefix "baselayer".
SYSTEMS = [
    {'claim_key': 'mem0',                'data_prefix': 'mem0',        'display': 'Mem0'},
    {'claim_key': 'letta_archival',      'data_prefix': 'letta',       'display': 'Letta (archival retrieval path)'},
    {'claim_key': 'zep',                 'data_prefix': 'zep',         'display': 'Zep'},
    {'claim_key': 'supermemory',         'data_prefix': 'supermemory', 'display': 'Supermemory'},
    {'claim_key': 'baselayer_substrate', 'data_prefix': 'baselayer',   'display': 'Base Layer substrate'},
]

# Subjects for which Supermemory native paid-tier judgments live at the canonical
# script-local path (NOT the study-repo mirror).
SUPERMEMORY_PAID_TIER_CANONICAL_SUBJECTS = {'babur', 'bernal_diaz', 'cellini', 'rousseau'}


# ---------- Custom errors ----------

class SchemaError(Exception):
    """Raised when an input judgment file fails schema validation."""


class MissingDataError(Exception):
    """Raised when a required primary-data file is missing."""


# ---------- File path resolver ----------

def subject_results_dir_controlled(subject: str) -> Path:
    """Per-subject directory for controlled-config judgments (study repo mirror)."""
    if subject == 'hamerton':
        return STUDY_RESULTS / 'hamerton'
    return STUDY_RESULTS / f'global_{subject}'


def subject_results_dir_native(subject: str, system_data_prefix: str) -> Path:
    """Per-subject directory for native-config (`_fullpipeline_*`) judgments.

    For supermemory native, the 4 paid-tier-rerun subjects live at the canonical
    script-local path; everyone else and all other systems use the study-repo mirror.
    """
    if (system_data_prefix == 'supermemory'
        and subject in SUPERMEMORY_PAID_TIER_CANONICAL_SUBJECTS):
        return CANONICAL_RESULTS / f'global_{subject}'
    if subject == 'hamerton':
        return STUDY_RESULTS / 'hamerton'
    return STUDY_RESULTS / f'global_{subject}'


def judgment_path(subject: str, system_data_prefix: str, config: str, judge: str) -> Path:
    """Resolve the path to a single per-judge judgment JSON file."""
    if config == 'controlled':
        d = subject_results_dir_controlled(subject)
        return d / f'{system_data_prefix}_judgments_{judge}.json'
    elif config == 'native':
        d = subject_results_dir_native(subject, system_data_prefix)
        return d / f'{system_data_prefix}_fullpipeline_judgments_{judge}.json'
    else:
        raise ValueError(f'unknown config: {config}')


# ---------- Schema validation ----------

CANONICAL_CONDITION_PATTERN = re.compile(
    r'^C(?:1|3)_(?:mem0|letta|zep|supermemory|baselayer)(?:_fp)?$'
)


def validate_judgment_record(record: dict, file_path: Path, idx: int, expected_judge: str) -> None:
    """Schema-validate one judgment record. Raises SchemaError on violation."""
    for k in ('question_id', 'condition', 'judge', 'score'):
        if k not in record:
            raise SchemaError(
                f'Missing required key {k!r} in {file_path} record idx={idx}'
            )
    if not isinstance(record['question_id'], int):
        raise SchemaError(
            f'question_id is not int in {file_path} record idx={idx}'
        )
    if not isinstance(record['condition'], str):
        raise SchemaError(
            f'condition is not str in {file_path} record idx={idx}'
        )
    if record['condition'] != '' and not CANONICAL_CONDITION_PATTERN.match(record['condition']):
        # Be strict: §4.4.1 conditions must be one of the C1_/C3_ memory-system labels.
        raise SchemaError(
            f'Non-canonical condition {record["condition"]!r} in {file_path} record idx={idx}'
        )
    if record['judge'] not in (PRIMARY_JUDGES | GEMINI_JUDGES):
        raise SchemaError(
            f'Unknown judge {record["judge"]!r} in {file_path} record idx={idx}'
        )
    score = record['score']
    if not isinstance(score, (int, float)):
        raise SchemaError(
            f'score is not numeric in {file_path} record idx={idx}'
        )
    # parse_failure rows may have score=0; allow that path through validation.
    if not record.get('parse_failure', False):
        if score < 1.0 or score > 5.0:
            # Some files use 0 to indicate parse failure even without the flag set.
            # Accept score==0 only as an implicit parse failure marker; otherwise it is
            # a genuine schema violation.
            if score != 0:
                raise SchemaError(
                    f'score {score} out of [1,5] in {file_path} record idx={idx}'
                )


# ---------- Provenance / manifest ----------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def manifest_entry_for(path: Path, n_records: int) -> dict:
    return {
        'path': str(path),
        'sha256': sha256_of(path),
        'size_bytes': path.stat().st_size,
        'n_records': n_records,
    }


# ---------- Loader ----------

def _load_s114_backfill_overrides(subject: str, system_data_prefix: str, config: str,
                                  judge_files, manifest: list) -> dict:
    """Return {(qid, cond, judge): backfill_record} for any successful S114 backfill
    rerun records covering this (subject, system, config).

    Provenance: S114-S115 batch failures (HTTP 429 rate-limit and HTTP 400
    max_tokens-vs-max_completion_tokens) for memory-system C1/C3 cells were
    rejudged offline; the resulting per-cell judgments are stored in
    `results/_s114_backfills/`. Each file's records are authoritative for the
    (subject, condition, judge) cell it covers.

    Backfills only exist for the controlled config (C1_<sys> / C3_<sys>); the
    native (`_fp`) reruns were not part of the S114 backfill batch. This helper
    therefore returns an empty dict for `config='native'`.
    """
    overrides: dict = {}
    if config != 'controlled':
        return overrides
    if not BACKFILL_DIR.exists():
        return overrides
    for cond_short in ('C1', 'C3'):
        cond = f'{cond_short}_{system_data_prefix}'
        for judge in judge_files:
            fname = f'global_{subject}__{cond}__{judge}.json'
            path = BACKFILL_DIR / fname
            if not path.exists():
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                raise MissingDataError(f'Failed to read backfill {path}: {e}')
            if not isinstance(data, list):
                raise SchemaError(f'Top-level of backfill {path} is not a list')
            n_applied = 0
            for r in data:
                if not isinstance(r, dict):
                    continue
                if r.get('parse_failure', False):
                    continue
                s = r.get('score')
                if s is None or s == 0:
                    continue
                if not (isinstance(s, (int, float)) and 1.0 <= s <= 5.0):
                    continue
                qid = r.get('question_id')
                rcond = r.get('condition')
                rjudge = r.get('judge')
                if qid is None or rcond != cond or rjudge != judge:
                    continue
                # Re-shape into the canonical record schema this script expects.
                overrides[(qid, rcond, rjudge)] = {
                    'question_id': qid,
                    'condition': rcond,
                    'judge': rjudge,
                    'score': float(s),
                    'parse_failure': False,
                    'raw_response': r.get('raw', ''),
                    '_source': 's114_backfill',
                }
                n_applied += 1
            manifest.append({
                **manifest_entry_for(path, len(data)),
                'role': 's114_backfill',
                'records_applied': n_applied,
            })
    return overrides


def load_subject_system_judgments(subject: str, system_data_prefix: str, config: str,
                                   manifest: list, judge_files=JUDGE_FILES) -> list:
    """Load and schema-validate all per-judge judgments for (subject, system, config).

    Adds a manifest entry for every file successfully read. Raises SchemaError for
    any record violating schema (no silent skips). Returns list of records (already
    schema-checked). Returns [] if NO judge files exist for this subject (caller
    decides whether that is acceptable).

    After loading the primary per-judge files, this function applies S114
    backfill overrides from `results/_s114_backfills/` so any (qid, cond, judge)
    cell with a successful rerun supersedes the originally-failed record.
    The override layer is keyed on (question_id, condition, judge); the
    primary record is dropped when an override is present.
    """
    overrides = _load_s114_backfill_overrides(subject, system_data_prefix, config,
                                              judge_files, manifest)
    rows: list = []
    found_any = False
    for judge in judge_files:
        path = judgment_path(subject, system_data_prefix, config, judge)
        if not path.exists():
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise MissingDataError(f'Failed to read {path}: {e}')
        if not isinstance(data, list):
            raise SchemaError(f'Top-level of {path} is not a list')
        for idx, r in enumerate(data):
            validate_judgment_record(r, path, idx, judge)
            key = (r.get('question_id'), r.get('condition'), r.get('judge'))
            if key in overrides:
                continue  # backfill record will be appended below
            rows.append(r)
        manifest.append(manifest_entry_for(path, len(data)))
        found_any = True
    rows.extend(overrides.values())
    return rows


# ---------- Aggregation ----------

def aggregate_per_condition(rows: list, judge_set: set) -> dict:
    """Per (condition, judge): mean across questions (excluding parse_failure rows).
       Per condition: mean across judges in panel. Returns {condition: panel_mean}.
    """
    per_jc: dict = defaultdict(list)
    for r in rows:
        if r['judge'] not in judge_set:
            continue
        if r.get('parse_failure', False):
            continue
        if r.get('score') in (None, 0):
            # score=0 without parse_failure flag is treated as an implicit parse failure
            continue
        per_jc[(r['condition'], r['judge'])].append(r['score'])

    per_c: dict = defaultdict(list)
    for (c, j), scores in per_jc.items():
        if scores:
            per_c[c].append(statistics.mean(scores))

    return {c: statistics.mean(ms) for c, ms in per_c.items() if ms}


def compute_for_system(system: dict, config: str, manifest: list,
                       errors: list) -> dict:
    """Compute per-subject (C1, C3, delta) and aggregates for one system × config.

    Returns dict with the structure used to fill the §4.4.1 claim cells.
    """
    system_data_prefix = system['data_prefix']
    if config == 'native' and system_data_prefix == 'baselayer':
        return {
            'available': False,
            'reason': 'no_native_variant',
            'note': ('Base Layer has no native/fullpipeline variant. The Base Layer '
                     'substrate IS the authored pipeline, so there is no separate '
                     '"native" condition to compare against.'),
        }

    c1_label = f'C1_{system_data_prefix}' + ('_fp' if config == 'native' else '')
    c3_label = f'C3_{system_data_prefix}' + ('_fp' if config == 'native' else '')

    per_subject: dict = {}
    missing: list = []
    for subject in MAIN_STUDY:
        rows = load_subject_system_judgments(subject, system_data_prefix, config, manifest)
        if not rows:
            missing.append(subject)
            continue
        means = aggregate_per_condition(rows, PRIMARY_JUDGES)
        c1 = means.get(c1_label)
        c3 = means.get(c3_label)
        if c1 is None or c3 is None:
            missing.append(subject)
            continue
        per_subject[subject] = {'c1': c1, 'c3': c3, 'delta': c3 - c1}

    deltas_all = [v['delta'] for v in per_subject.values()]
    deltas_low = [v['delta'] for s, v in per_subject.items()
                  if s in LOW_BASELINE_SUBJECTS]

    agg_all = statistics.mean(deltas_all) if deltas_all else None
    agg_low = statistics.mean(deltas_low) if deltas_low else None
    n_pos_all = sum(1 for d in deltas_all if d > 0)
    n_pos_low = sum(1 for d in deltas_low if d > 0)

    # Wilcoxon paired C1 vs C3 -- low-baseline only (matches paper text in §4.4.1)
    wilcoxon_p_low: Optional[float] = None
    wilcoxon_w_low: Optional[float] = None
    # Wilcoxon on the FULL panel (the paper reports this for native Supermemory; reported
    # for completeness on every cell where computable).
    wilcoxon_p_all: Optional[float] = None
    wilcoxon_w_all: Optional[float] = None

    if HAS_SCIPY:
        try:
            c1_low = [v['c1'] for s, v in per_subject.items() if s in LOW_BASELINE_SUBJECTS]
            c3_low = [v['c3'] for s, v in per_subject.items() if s in LOW_BASELINE_SUBJECTS]
            if len(c1_low) >= 5:
                w, p = scipy_stats.wilcoxon(c1_low, c3_low, alternative='two-sided')
                wilcoxon_w_low = float(w)
                wilcoxon_p_low = float(p)
        except Exception as e:  # pragma: no cover -- defensive
            errors.append(f'wilcoxon (low) failed for {system["claim_key"]}/{config}: {e}')
        try:
            c1_all = [v['c1'] for v in per_subject.values()]
            c3_all = [v['c3'] for v in per_subject.values()]
            if len(c1_all) >= 5:
                w2, p2 = scipy_stats.wilcoxon(c1_all, c3_all, alternative='two-sided')
                wilcoxon_w_all = float(w2)
                wilcoxon_p_all = float(p2)
        except Exception as e:  # pragma: no cover
            errors.append(f'wilcoxon (all) failed for {system["claim_key"]}/{config}: {e}')

    return {
        'available': True,
        'per_subject': per_subject,
        'agg_all': agg_all,
        'agg_low': agg_low,
        'n_all': len(deltas_all),
        'n_low': len(deltas_low),
        'n_pos_all': n_pos_all,
        'n_pos_low': n_pos_low,
        'wilcoxon_w_low': wilcoxon_w_low,
        'wilcoxon_p_low': wilcoxon_p_low,
        'wilcoxon_w_all': wilcoxon_w_all,
        'wilcoxon_p_all': wilcoxon_p_all,
        'missing_subjects': missing,
        'c1_label': c1_label,
        'c3_label': c3_label,
    }


# ---------- Claim emission ----------

def make_claim(value, estimand, contrast, panel, conditions, subjects,
               n=None, p_value=None, note=None) -> dict:
    obj = {
        'value': value,
        'estimand': estimand,
        'contrast': contrast,
        'filters': {
            'panel': sorted(panel) if panel else [],
            'condition': conditions,
            'subjects': sorted(subjects) if subjects else [],
        },
        'n': n,
        'ci95_low': None,
        'ci95_high': None,
        'p_value': p_value,
    }
    if note:
        obj['note'] = note
    return obj


def emit_claims(results: dict) -> dict:
    """Build the {claim_id: claim_obj} dict for every system × config × metric."""
    claims: dict = {}

    for system in SYSTEMS:
        key = system['claim_key']
        for config in ('controlled', 'native'):
            r = results[config][key]

            # Pick subject lists for filter labels
            if r.get('available'):
                subjects_all = sorted(r['per_subject'].keys())
                subjects_low = sorted([s for s in r['per_subject'] if s in LOW_BASELINE_SUBJECTS])
            else:
                subjects_all = []
                subjects_low = []

            data_prefix = system['data_prefix']
            if config == 'controlled':
                c1 = f'C1_{data_prefix}'
                c3 = f'C3_{data_prefix}'
            else:
                c1 = f'C1_{data_prefix}_fp'
                c3 = f'C3_{data_prefix}_fp'

            # all-14 delta
            cid = f'4_4_1_{key}_{config}_all14_delta'
            if r.get('available'):
                claims[cid] = make_claim(
                    value=round(r['agg_all'], 6) if r['agg_all'] is not None else None,
                    estimand=f'Mean Δ_spec across {r["n_all"]} subjects ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=subjects_all,
                    n=r['n_all'],
                    p_value=r['wilcoxon_p_all'],
                )
            else:
                claims[cid] = make_claim(
                    value=None,
                    estimand=f'Mean Δ_spec across all 14 subjects ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=[],
                    n=0,
                    note=r.get('note'),
                )

            # low-baseline delta
            cid = f'4_4_1_{key}_{config}_low_baseline_delta'
            if r.get('available'):
                claims[cid] = make_claim(
                    value=round(r['agg_low'], 6) if r['agg_low'] is not None else None,
                    estimand=f'Mean Δ_spec across low-baseline subjects ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=subjects_low,
                    n=r['n_low'],
                    p_value=r['wilcoxon_p_low'],
                )
            else:
                claims[cid] = make_claim(
                    value=None,
                    estimand=f'Mean Δ_spec across low-baseline subjects ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=[],
                    n=0,
                    note=r.get('note'),
                )

            # low-baseline n_positive (count)
            cid = f'4_4_1_{key}_{config}_low_baseline_n_positive'
            if r.get('available'):
                claims[cid] = make_claim(
                    value=r['n_pos_low'],
                    estimand=f'Number of low-baseline subjects with Δ_spec > 0 ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=subjects_low,
                    n=r['n_low'],
                )
            else:
                claims[cid] = make_claim(
                    value=None,
                    estimand=f'Number of low-baseline subjects with Δ_spec > 0 ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=[],
                    n=0,
                    note=r.get('note'),
                )

            # all-14 n_positive (extra metric beyond the 8 task-required ones; useful for paper)
            cid = f'4_4_1_{key}_{config}_all14_n_positive'
            if r.get('available'):
                claims[cid] = make_claim(
                    value=r['n_pos_all'],
                    estimand=f'Number of all-14 subjects with Δ_spec > 0 ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=subjects_all,
                    n=r['n_all'],
                )
            else:
                claims[cid] = make_claim(
                    value=None,
                    estimand=f'Number of all-14 subjects with Δ_spec > 0 ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=[],
                    n=0,
                    note=r.get('note'),
                )

            # Wilcoxon p-value -- the paper text §4.4.1 cites Wilcoxon on the FULL paired
            # panel (n=14 main study, n=10 for supermemory native pre-paid-tier-rerun;
            # the existing analysis script `compute_memory_systems_5judge.py` produces
            # the same numbers paper quotes). Underpowered-on-low-9 is a separate remark
            # in the paper text. We therefore emit the all-14 Wilcoxon as the canonical
            # `wilcoxon_p` claim and stash the low-9 W/p in the JSON for completeness.
            cid = f'4_4_1_{key}_{config}_wilcoxon_p'
            if r.get('available'):
                claim = make_claim(
                    value=r['wilcoxon_p_all'],
                    estimand=(f'Wilcoxon signed-rank paired p-value, full paired panel '
                              f'({config} config, n={r["n_all"]})'),
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=subjects_all,
                    n=r['n_all'],
                    p_value=r['wilcoxon_p_all'],
                )
                # Preserve low-baseline auxiliary stats inside the claim object for traceability
                claim['wilcoxon_w_full'] = r['wilcoxon_w_all']
                claim['wilcoxon_w_low_baseline'] = r['wilcoxon_w_low']
                claim['wilcoxon_p_low_baseline'] = r['wilcoxon_p_low']
                claims[cid] = claim
            else:
                claims[cid] = make_claim(
                    value=None,
                    estimand=f'Wilcoxon signed-rank paired p-value ({config} config)',
                    contrast=f'{c3} − {c1}',
                    panel=PRIMARY_JUDGES,
                    conditions=[c1, c3],
                    subjects=[],
                    n=0,
                    note=r.get('note'),
                )
    return claims


# ---------- Atomic write ----------

def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + '.', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ---------- Markdown view ----------

# v10 paper §4.4.1 reported numbers (row order: mem0, letta, zep, supermemory, baselayer)
# These are PAPER values, not scaffold values; markdown view shows MATCH/MISMATCH.
PAPER_TABLE = {
    'controlled': {
        'mem0':                {'all14_delta': +0.12, 'all14_npos': 10, 'low_delta': +0.10, 'low_npos': 6},
        'letta_archival':      {'all14_delta': +0.20, 'all14_npos': 12, 'low_delta': +0.17, 'low_npos': 8},
        'zep':                 {'all14_delta': +0.19, 'all14_npos': 13, 'low_delta': +0.17, 'low_npos': 9},
        'supermemory':         {'all14_delta': -0.05, 'all14_npos': 5,  'low_delta': -0.01, 'low_npos': 5},
        'baselayer_substrate': {'all14_delta': +0.08, 'all14_npos': 9,  'low_delta': +0.08, 'low_npos': 6},
    },
    'native': {
        'mem0':                {'all14_delta': +0.33, 'all14_npos': 10, 'low_delta': +0.32, 'low_npos': 7},
        'letta_archival':      {'all14_delta': -0.02, 'all14_npos': 5,  'low_delta': -0.04, 'low_npos': 4},
        'zep':                 {'all14_delta': +0.33, 'all14_npos': 13, 'low_delta': +0.30, 'low_npos': 9},
        'supermemory':         {'all14_delta': -0.01, 'all14_npos': 6,  'low_delta': -0.03, 'low_npos': 4},
        'baselayer_substrate': {'all14_delta': None,  'all14_npos': None, 'low_delta': None, 'low_npos': None},
    },
}

PAPER_WILCOXON = {
    # Paper text §4.4.1 quotes Wilcoxon p-values on the FULL paired panel (n=14 main
    # study, n=14 for supermemory native after paid-tier rerun). Where the paper does
    # not quote a number, we leave None and verify reports "paper-not-reported".
    'controlled': {
        'mem0':                None,        # not quoted; paper says non-significant
        'letta_archival':      0.0017,      # quoted: "Letta controlled p = 0.0017"
        'zep':                 0.0004,      # quoted: "Zep controlled p = 0.0004"
        'supermemory':         None,        # not quoted
        'baselayer_substrate': None,        # not quoted
    },
    'native': {
        'mem0':                0.0088,      # quoted: "Mem0 native p = 0.0088"
        'letta_archival':      None,        # not quoted; paper says non-significant
        'zep':                 0.0015,      # quoted: "Zep native p = 0.0015"
        'supermemory':         0.8077,      # quoted: "Supermemory native W = 48.0, p = 0.8077"
        'baselayer_substrate': None,        # native not applicable
    },
}


def fmt_value(v, places=2):
    if v is None:
        return 'N/A'
    return f'{v:+.{places}f}'


def fmt_pct(v, places=2):
    if v is None:
        return 'N/A'
    return f'{v:.{places}f}'


def status_for(scaffold, paper, tol=0.005):
    if scaffold is None and paper is None:
        return 'MATCH (both null)'
    if scaffold is None or paper is None:
        return f'MISMATCH (scaffold={scaffold}, paper={paper})'
    if abs(scaffold - paper) <= tol:
        return 'MATCH'
    return f'MISMATCH (Δ={scaffold - paper:+.4f})'


def render_markdown(results: dict, run_iso: str) -> str:
    lines: list = []
    lines.append('# §4.4.1 Memory Systems: V11 Emit (5-judge primary)')
    lines.append('')
    lines.append(f'_Generated by `{SCRIPT_PATH_REL}` (script_version `{SCRIPT_VERSION}`) at `{run_iso}`._')
    lines.append('')
    lines.append('Aggregation rule (per v11 architecture spec §1):')
    lines.append('1. Read raw per-judge per-question scores from primary data.')
    lines.append('2. Filter to 5-judge primary panel: `{haiku, sonnet, opus, gpt4o, gpt54}`.')
    lines.append('3. Per-judge per-subject mean = mean of per-question scores within subject (parse_failure rows excluded).')
    lines.append('4. Panel mean per-subject per-condition = mean of per-judge means.')
    lines.append('5. Δ_spec per subject = panel mean(C3) − panel mean(C1).')
    lines.append('6. Aggregate Δ_spec = mean across subjects (subject = unit of inference).')
    lines.append('7. Wilcoxon signed-rank: paired C1 vs C3 panel means on the full paired panel (n=14 main study). Low-baseline-only Wilcoxon also computed and stored alongside.')
    lines.append('')
    lines.append('Provenance notes:')
    lines.append('- Native condition strings use `_fp` suffix (data ground truth). The v11 architecture spec §7 lists `_native`; the data uses `_fp`. This script reads `_fp`.')
    lines.append('- Supermemory native paid-tier judgments for {babur, bernal_diaz, cellini, rousseau} live at the canonical script-local path `memory_system/data/experiments/memory_systems/results/global_<subject>/`; this script reads them directly. They are NOT mirrored into the study repo.')
    lines.append('- Hamerton native supermemory data lives only in the study-repo mirror.')
    lines.append('- Base Layer has no native variant; native claim_ids for `baselayer_substrate` are emitted with value=null.')
    lines.append('')

    # ---- Table 1: Controlled ----
    lines.append('## Controlled configuration (5-judge primary, all 14 subjects)')
    lines.append('')
    lines.append('| System | Scaffold Δ (all 14) | Paper Δ (all 14) | Status | Scaffold +/14 | Paper +/14 | Status | Scaffold Δ (low 9) | Paper Δ (low 9) | Status | Scaffold +/9 | Paper +/9 | Status |')
    lines.append('|---|---:|---:|:--:|---:|---:|:--:|---:|---:|:--:|---:|---:|:--:|')
    for system in SYSTEMS:
        key = system['claim_key']
        r = results['controlled'][key]
        if not r.get('available'):
            continue
        ptab = PAPER_TABLE['controlled'][key]
        sa = r['agg_all']
        sl = r['agg_low']
        spa = r['n_pos_all']
        spl = r['n_pos_low']
        lines.append(
            f'| {system["display"]} | {fmt_value(sa)} | {fmt_value(ptab["all14_delta"])} | {status_for(sa, ptab["all14_delta"])} | '
            f'{spa}/{r["n_all"]} | {ptab["all14_npos"]}/14 | {status_for(spa, ptab["all14_npos"])} | '
            f'{fmt_value(sl)} | {fmt_value(ptab["low_delta"])} | {status_for(sl, ptab["low_delta"])} | '
            f'{spl}/{r["n_low"]} | {ptab["low_npos"]}/9 | {status_for(spl, ptab["low_npos"])} |'
        )
    lines.append('')

    # ---- Table 2: Native ----
    lines.append('## Native configuration (5-judge primary)')
    lines.append('')
    lines.append('| System | Scaffold Δ (all) | Paper Δ (all) | Status | Scaffold +/n | Paper +/n | Status | Scaffold Δ (low) | Paper Δ (low) | Status | Scaffold +/low | Paper +/low | Status |')
    lines.append('|---|---:|---:|:--:|---:|---:|:--:|---:|---:|:--:|---:|---:|:--:|')
    for system in SYSTEMS:
        key = system['claim_key']
        r = results['native'][key]
        ptab = PAPER_TABLE['native'][key]
        if not r.get('available'):
            lines.append(f'| {system["display"]} | N/A | N/A | MATCH (both null) | N/A | N/A | MATCH (both null) | N/A | N/A | MATCH (both null) | N/A | N/A | MATCH (both null) |')
            continue
        sa = r['agg_all']
        sl = r['agg_low']
        spa = r['n_pos_all']
        spl = r['n_pos_low']
        lines.append(
            f'| {system["display"]} | {fmt_value(sa)} | {fmt_value(ptab["all14_delta"])} | {status_for(sa, ptab["all14_delta"])} | '
            f'{spa}/{r["n_all"]} | {ptab["all14_npos"]}/{r["n_all"]} | {status_for(spa, ptab["all14_npos"])} | '
            f'{fmt_value(sl)} | {fmt_value(ptab["low_delta"])} | {status_for(sl, ptab["low_delta"])} | '
            f'{spl}/{r["n_low"]} | {ptab["low_npos"]}/{r["n_low"]} | {status_for(spl, ptab["low_npos"])} |'
        )
    lines.append('')

    # ---- Table 3: Wilcoxon p-values (full paired panel; matches paper text) ----
    lines.append('## Wilcoxon signed-rank p-values (full paired panel)')
    lines.append('')
    lines.append('Paper text §4.4.1 quotes Wilcoxon p-values computed on the full paired panel (n=14 main study; n=14 for supermemory native after the paid-tier rerun). The low-baseline-only Wilcoxon is computed for completeness and stored alongside in the JSON as `wilcoxon_p_low_baseline` on each `*_wilcoxon_p` claim.')
    lines.append('')
    lines.append('| System | Config | n | Scaffold p (full) | Paper p (text) | Status | Scaffold p (low-9) |')
    lines.append('|---|---|---:|---:|---:|:--:|---:|')
    for system in SYSTEMS:
        key = system['claim_key']
        for config in ('controlled', 'native'):
            r = results[config][key]
            paper_p = PAPER_WILCOXON[config][key]
            if not r.get('available'):
                lines.append(f'| {system["display"]} | {config} | - | N/A | N/A | MATCH (both null) | N/A |')
                continue
            sp_full = r['wilcoxon_p_all']
            sp_low = r['wilcoxon_p_low']
            paper_str = (f'{paper_p:.4f}' if paper_p is not None else 'not reported in text')
            full_str = (f'{sp_full:.4f}' if sp_full is not None else 'N/A')
            low_str = (f'{sp_low:.4f}' if sp_low is not None else 'N/A')
            if paper_p is None:
                status = 'paper does not report; scaffold computes'
            else:
                status = status_for(sp_full, paper_p)
            lines.append(f'| {system["display"]} | {config} | {r["n_all"]} | {full_str} | {paper_str} | {status} | {low_str} |')
    lines.append('')

    lines.append('## Notes on the cross-check')
    lines.append('')
    lines.append('- Paper-text Wilcoxon p-values in §4.4.1 are on the full paired panel; this is what the scaffold emits in the `*_wilcoxon_p` claim. The low-baseline-only Wilcoxon (n=9) is stored alongside in the JSON as `wilcoxon_p_low_baseline`.')
    lines.append('- For native Supermemory the full panel is n=14 (paid-tier rerun for {babur, bernal_diaz, cellini, rousseau} read from canonical script-local path).')
    lines.append('- Base Layer substrate has no native variant; native claim_ids are emitted with value=null.')
    lines.append('- The single MISMATCH currently surfaced is `4_4_1_letta_archival_controlled_low_baseline_delta`: scaffold +0.1646 vs paper +0.17 (delta -0.0054, just outside the 0.005 tolerance). The existing analysis doc `docs/research/memory_systems_5judge_primary.md` reports the same scaffold value (+0.165). The paper appears to have rounded +0.165 -> +0.17 on display, while the scaffold computes +0.1646 -> +0.16 with standard rounding. Recommended paper edit: report +0.16 to match the underlying number.')
    lines.append('')

    return '\n'.join(lines)


# ---------- Verification against paper ----------

def verify(claims: dict) -> int:
    """Compare scaffold values to PAPER_TABLE and PAPER_WILCOXON. Print MATCH/MISMATCH per claim.

    Returns 0 if all match within 0.005, 1 otherwise.
    """
    print('\n=== --verify: scaffold vs paper section 4.4.1 ===\n')
    print(f'{"claim_id":<60s} {"scaffold":>10s} {"paper":>10s}  status')
    print('-' * 110)
    bad = 0
    total = 0

    def chk(cid, scaffold_v, paper_v, kind='float'):
        nonlocal bad, total
        total += 1
        if paper_v is None and scaffold_v is None:
            status = 'MATCH (both null)'
        elif paper_v is None:
            status = 'paper-not-reported (scaffold computed)'
        elif scaffold_v is None:
            status = f'MISMATCH (scaffold null vs paper={paper_v})'
            bad += 1
        else:
            delta = abs(scaffold_v - paper_v)
            if delta <= 0.005:
                status = 'MATCH'
            elif kind == 'count' and abs(int(scaffold_v) - int(paper_v)) == 0:
                status = 'MATCH'
            else:
                status = f'MISMATCH (delta={scaffold_v - paper_v:+.4f})'
                bad += 1
        sa = ('null' if scaffold_v is None else (f'{scaffold_v:>+10.4f}' if isinstance(scaffold_v, float) else f'{scaffold_v:>10}'))
        pa = ('null' if paper_v is None else (f'{paper_v:>+10.4f}' if isinstance(paper_v, float) else f'{paper_v:>10}'))
        print(f'{cid:<60s} {sa} {pa}  {status}')

    for system in SYSTEMS:
        key = system['claim_key']
        for config in ('controlled', 'native'):
            ptab = PAPER_TABLE[config][key]
            chk(f'4_4_1_{key}_{config}_all14_delta',
                claims[f'4_4_1_{key}_{config}_all14_delta']['value'],
                ptab['all14_delta'])
            chk(f'4_4_1_{key}_{config}_low_baseline_delta',
                claims[f'4_4_1_{key}_{config}_low_baseline_delta']['value'],
                ptab['low_delta'])
            chk(f'4_4_1_{key}_{config}_low_baseline_n_positive',
                claims[f'4_4_1_{key}_{config}_low_baseline_n_positive']['value'],
                ptab['low_npos'], kind='count')
            chk(f'4_4_1_{key}_{config}_all14_n_positive',
                claims[f'4_4_1_{key}_{config}_all14_n_positive']['value'],
                ptab['all14_npos'], kind='count')
            chk(f'4_4_1_{key}_{config}_wilcoxon_p',
                claims[f'4_4_1_{key}_{config}_wilcoxon_p']['value'],
                PAPER_WILCOXON[config][key])

    print('-' * 110)
    print(f'\nTotal claims checked: {total}, MISMATCH count: {bad}')
    return 0 if bad == 0 else 1


# ---------- Main ----------

def main(argv=None) -> int:
    # Force stdout/stderr UTF-8 on Windows where the default cp1252 codec breaks on non-ASCII.
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    parser = argparse.ArgumentParser(description='V11 emit script for section 4.4.1 (memory systems).')
    parser.add_argument('--verify', action='store_true',
                        help='After emitting, compare every claim to the v10 paper §4.4.1 numbers and exit 1 on mismatch.')
    args = parser.parse_args(argv)

    manifest: list = []
    errors: list = []
    results: dict = {'controlled': {}, 'native': {}}

    for system in SYSTEMS:
        for config in ('controlled', 'native'):
            try:
                results[config][system['claim_key']] = compute_for_system(system, config, manifest, errors)
            except (SchemaError, MissingDataError) as e:
                # Hard-fail: schema or missing data is a release-blocking issue.
                print(f'[FATAL] {system["claim_key"]}/{config}: {e}', file=sys.stderr)
                return 2

    claims = emit_claims(results)

    # For idempotency (v11 architecture spec §2 item 8), the run_timestamp is derived
    # deterministically from the manifest content rather than the wall clock. Two runs
    # over identical primary data produce byte-identical output JSON.
    manifest_signature = hashlib.sha256(
        json.dumps(sorted(manifest, key=lambda m: m['path']), sort_keys=True).encode('utf-8')
    ).hexdigest()
    # Format like an ISO-8601 timestamp tag for human readability while remaining deterministic.
    run_iso = f'manifest:{manifest_signature[:16]}'

    output = {
        'schema_version': 'v11.0',
        'section': 'paper.4.4.1',
        'aggregation_rule': ('5-judge primary; per-judge per-question -> per-judge per-subject mean -> '
                             'panel mean across {haiku, sonnet, opus, gpt4o, gpt54}; parse_failure rows excluded; '
                             'subject = unit of inference for cross-subject aggregates.'),
        'claims': claims,
        'provenance': {
            'script': SCRIPT_PATH_REL,
            'script_version': SCRIPT_VERSION,
            'run_timestamp': run_iso,
            'input_manifest': sorted(manifest, key=lambda m: m['path']),
            'notes': [
                ('Native condition strings use `_fp` suffix in primary data (e.g., C1_mem0_fp). '
                 'The v11 architecture spec §7 lists `_native`; the data is the source of truth.'),
                ('Supermemory native paid-tier judgments for babur, bernal_diaz, cellini, rousseau '
                 'live at the canonical script-local path `memory_system/data/experiments/memory_systems/'
                 'results/global_<subject>/` and are read from there directly. They are NOT mirrored '
                 'into the study repo. Hamerton native supermemory data lives only at the study-repo mirror.'),
                ('Base Layer substrate has no native variant; all `4_4_1_baselayer_substrate_native_*` '
                 'claim_ids are emitted with value=null and an explicit note.'),
                ('Score==0 with parse_failure unset is treated as an implicit parse-failure marker and '
                 'excluded from aggregates. This matches study convention.'),
            ],
            'errors_during_run': errors,
        },
    }

    json_text = json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    md_text = render_markdown(results, run_iso)

    atomic_write(OUT_JSON, json_text)
    atomic_write(OUT_MD, md_text)

    print(f'\nEmitted: {OUT_JSON}')
    print(f'Emitted: {OUT_MD}')
    print(f'Total claim_ids: {len(claims)}')

    if args.verify:
        return verify(claims)

    return 0


if __name__ == '__main__':
    sys.exit(main())
