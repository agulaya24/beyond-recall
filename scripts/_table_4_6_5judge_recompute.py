"""
Recompute Table 4.6 (§4.4.2) per-row values under strict 5-judge primary panel.

Audit panel = {haiku, sonnet, opus, gpt4o, gpt54, gemini_flash}
Primary panel = {haiku, sonnet, opus, gpt4o, gpt54}  (gemini_flash dropped)

Aggregation:
  per-judge per-question score
    -> per-question per-condition panel mean across the 5 primary judges
       (strict: all 5 must have valid score; otherwise cell is dropped)
    -> Δ_question = panel_mean(C3) − panel_mean(C1)
    -> Aggregate Δ = mean of Δ_question over paired questions
    -> C1 mean = mean of panel_mean(C1) over paired questions
    -> C3 mean = mean of panel_mean(C3) over paired questions

Thresholds:
  Win:                   Δ_question > +0.3
  Loss:                  Δ_question < −0.3
  Large improvement:     Δ_question > +1.0
  Large regression:      Δ_question < −1.0

Reuses load_subject_system + paired-coverage logic from
scripts/_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py.

Read-only: prints the table to stdout. Does NOT modify any paper file.
"""
from __future__ import annotations

import importlib.util
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EMIT_SCRIPT = REPO / 'scripts' / '_v11_emit_4_4_2_4_4_3_mechanisms_keckley.py'

# Dynamic import of the v11 emit module (filename starts with underscore).
_spec = importlib.util.spec_from_file_location('v11_emit_4_4_2', str(EMIT_SCRIPT))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

load_subject_system = _mod.load_subject_system
PRIMARY_JUDGES = _mod.PRIMARY_JUDGES

# Audit-panel reference values from the task brief.
AUDIT_PANEL_TABLE_4_6 = {
    ('mem0',       'yung_wing'): {'agg':  0.35, 'c1': 2.16, 'c3': 2.51, 'wins': 21, 'losses': 12, 'large_imp': 7,  'large_reg': 1, 'n': 39},
    ('mem0',       'keckley'):   {'agg': -0.01, 'c1': 2.64, 'c3': 2.63, 'wins': 14, 'losses': 16, 'large_imp': 1,  'large_reg': 2, 'n': 39},
    ('letta',      'hamerton'):  {'agg':  0.46, 'c1': 2.35, 'c3': 2.81, 'wins': 21, 'losses': 8,  'large_imp': 10, 'large_reg': 2, 'n': 39},
    ('letta',      'keckley'):   {'agg':  0.00, 'c1': 2.70, 'c3': 2.70, 'wins': 11, 'losses': 15, 'large_imp': 3,  'large_reg': 2, 'n': 39},
    ('zep',        'seacole'):   {'agg':  0.52, 'c1': 2.27, 'c3': 2.79, 'wins': 24, 'losses': 8,  'large_imp': 9,  'large_reg': 0, 'n': 39},
    ('zep',        'keckley'):   {'agg':  0.10, 'c1': 2.49, 'c3': 2.59, 'wins': 16, 'losses': 12, 'large_imp': 5,  'large_reg': 3, 'n': 39},
    ('baselayer',  'yung_wing'): {'agg':  0.33, 'c1': 2.23, 'c3': 2.56, 'wins': 22, 'losses': 10, 'large_imp': 7,  'large_reg': 2, 'n': 39},
    ('baselayer',  'keckley'):   {'agg': -0.01, 'c1': 2.44, 'c3': 2.44, 'wins': 18, 'losses': 13, 'large_imp': 3,  'large_reg': 5, 'n': 39},
}

# Display name mapping
SYSTEM_DISPLAY = {
    'mem0':       'Mem0',
    'letta':      'Letta (archival)',
    'zep':        'Zep',
    'baselayer':  'Base Layer',
}

# Row order matches Table 4.6 in the paper.
ROWS = [
    ('mem0',       'yung_wing'),
    ('mem0',       'keckley'),
    ('letta',      'hamerton'),
    ('letta',      'keckley'),
    ('zep',        'seacole'),
    ('zep',        'keckley'),
    ('baselayer',  'yung_wing'),
    ('baselayer',  'keckley'),
]


def per_question_strict_panel_mean(scores_by_judge: dict) -> float | None:
    """Mean across the 5 primary judges only if all are present."""
    vs = [scores_by_judge.get(j) for j in PRIMARY_JUDGES]
    if any(v is None for v in vs):
        return None
    return statistics.mean(vs)


def compute_row(system_data_prefix: str, subject: str) -> dict:
    """Compute one Table 4.6 row under strict 5-judge primary."""
    manifest = []  # discarded; we only need the loaded scores
    ssj = load_subject_system(subject, system_data_prefix, manifest)

    c1_label = f'C1_{system_data_prefix}'
    c3_label = f'C3_{system_data_prefix}'

    # Index by (qid, condition) -> {judge: score}
    per_qcond_judge: dict = defaultdict(dict)
    for (qid, cond, judge), score in ssj.items():
        per_qcond_judge[(qid, cond)][judge] = score

    qids_c1 = {qid for (qid, cond) in per_qcond_judge if cond == c1_label}
    qids_c3 = {qid for (qid, cond) in per_qcond_judge if cond == c3_label}
    paired_qids = sorted(qids_c1 & qids_c3)

    deltas = []
    c1_means = []
    c3_means = []
    wins = losses = large_imp = large_reg = 0
    partial_count = 0

    for qid in paired_qids:
        c1_panel = per_question_strict_panel_mean(per_qcond_judge[(qid, c1_label)])
        c3_panel = per_question_strict_panel_mean(per_qcond_judge[(qid, c3_label)])
        if c1_panel is None or c3_panel is None:
            partial_count += 1
            continue
        delta = c3_panel - c1_panel
        deltas.append(delta)
        c1_means.append(c1_panel)
        c3_means.append(c3_panel)
        if delta > 0.3:
            wins += 1
        elif delta < -0.3:
            losses += 1
        if delta > 1.0:
            large_imp += 1
        elif delta < -1.0:
            large_reg += 1

    return {
        'agg':       statistics.mean(deltas) if deltas else None,
        'c1':        statistics.mean(c1_means) if c1_means else None,
        'c3':        statistics.mean(c3_means) if c3_means else None,
        'wins':      wins,
        'losses':    losses,
        'large_imp': large_imp,
        'large_reg': large_reg,
        'n':         len(deltas),
        'paired_total_with_partial': len(paired_qids),
        'partial_dropped': partial_count,
    }


def fmt_signed(v, places=2):
    if v is None:
        return 'null'
    return f'{v:+.{places}f}'


def fmt_unsigned(v, places=2):
    if v is None:
        return 'null'
    return f'{v:.{places}f}'


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print('# Table 4.6 (§4.4.2) under strict 5-judge primary panel')
    print()
    print('Panel: {haiku, sonnet, opus, gpt4o, gpt54}  (audit panel had gemini_flash too)')
    print()
    print('## Strict 5-judge primary results')
    print()
    print('| System | Subject | Aggregate Δ | C1 mean | C3 mean | Wins (Δ>0.3) | Losses (Δ<-0.3) | Large improv (Δ>1.0) | Large regr (Δ<-1.0) | Total Qs |')
    print('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|')

    rows = []
    for sp, subj in ROWS:
        r = compute_row(sp, subj)
        rows.append(((sp, subj), r))
        print(f'| {SYSTEM_DISPLAY[sp]} | {subj} | {fmt_signed(r["agg"])} | '
              f'{fmt_unsigned(r["c1"])} | {fmt_unsigned(r["c3"])} | '
              f'{r["wins"]} | {r["losses"]} | {r["large_imp"]} | {r["large_reg"]} | {r["n"]} |')

    print()
    print('## Side-by-side: 5-judge primary vs audit panel (|Δ| per cell)')
    print()
    print('Each cell shows: `5j_value (Δ vs audit = +/-X)`')
    print()
    print('| System | Subject | Aggregate Δ | C1 mean | C3 mean | Wins | Losses | Large improv | Large regr | Total Qs |')
    print('|---|---|---|---|---|---|---|---|---|---|')

    for (sp, subj), r in rows:
        a = AUDIT_PANEL_TABLE_4_6[(sp, subj)]

        def diff(new, old):
            if new is None:
                return f'null (audit {old})'
            return f'{new:+.2f} (Δ={new - old:+.2f})' if isinstance(new, float) else f'{new} (Δ={new - old:+d})'

        agg_cell = f'{r["agg"]:+.2f} (Δ={r["agg"] - a["agg"]:+.2f})' if r['agg'] is not None else 'null'
        c1_cell  = f'{r["c1"]:.2f} (Δ={r["c1"] - a["c1"]:+.2f})' if r['c1'] is not None else 'null'
        c3_cell  = f'{r["c3"]:.2f} (Δ={r["c3"] - a["c3"]:+.2f})' if r['c3'] is not None else 'null'
        wins_cell = f'{r["wins"]} (Δ={r["wins"] - a["wins"]:+d})'
        loss_cell = f'{r["losses"]} (Δ={r["losses"] - a["losses"]:+d})'
        li_cell   = f'{r["large_imp"]} (Δ={r["large_imp"] - a["large_imp"]:+d})'
        lr_cell   = f'{r["large_reg"]} (Δ={r["large_reg"] - a["large_reg"]:+d})'
        n_cell    = f'{r["n"]} (Δ={r["n"] - a["n"]:+d})'
        print(f'| {SYSTEM_DISPLAY[sp]} | {subj} | {agg_cell} | {c1_cell} | {c3_cell} | '
              f'{wins_cell} | {loss_cell} | {li_cell} | {lr_cell} | {n_cell} |')

    print()
    print('## Sign-flips on Aggregate Δ')
    print()
    flipped = []
    for (sp, subj), r in rows:
        a = AUDIT_PANEL_TABLE_4_6[(sp, subj)]
        if r['agg'] is None:
            continue
        # Sign flip = different sign (one positive, one negative). Treat |x|<eps as zero.
        eps = 1e-9
        new_sign = 0 if abs(r['agg']) < eps else (1 if r['agg'] > 0 else -1)
        old_sign = 0 if abs(a['agg']) < eps else (1 if a['agg'] > 0 else -1)
        if new_sign != old_sign and not (new_sign == 0 or old_sign == 0):
            flipped.append((sp, subj, a['agg'], r['agg']))
    if not flipped:
        print('No row has a different sign on Aggregate Δ. (Some rows that were near zero in '
              'the audit panel may now be near zero with different sign at the third decimal, '
              'reported below for completeness.)')
    else:
        for sp, subj, old, new in flipped:
            print(f'- {SYSTEM_DISPLAY[sp]} / {subj}: audit Aggregate Δ = {old:+.2f}, primary 5-judge = {new:+.2f}  -> SIGN FLIP')

    print()
    print('## Diagnostics')
    print()
    print('| System | Subject | Paired Qs (C1∩C3) | Strict-5 dropped | Total kept (n) |')
    print('|---|---|---:|---:|---:|')
    for (sp, subj), r in rows:
        print(f'| {SYSTEM_DISPLAY[sp]} | {subj} | {r["paired_total_with_partial"]} | '
              f'{r["partial_dropped"]} | {r["n"]} |')

    return 0


if __name__ == '__main__':
    sys.exit(main())
