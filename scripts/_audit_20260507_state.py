"""
2026-05-07 mechanistic audit — Step 0: assess current state of S114 backfills.

Input: docs/research/s114_parse_failure_manifest.json + results/_s114_backfills/
Output: stdout summary + docs/research/_audit_20260507_remaining_work.json
"""

import json
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / 'docs' / 'research' / 's114_parse_failure_manifest.json'
BACKFILL_DIR = REPO / 'results' / '_s114_backfills'


def main():
    manifest = json.load(MANIFEST.open(encoding='utf-8'))
    print(f'Manifest cells: {len(manifest)}')
    print(f'Total PF in manifest: {sum(e["parse_failures"] for e in manifest)}')

    rescued_total = 0
    unrescued_total = 0
    not_attempted_pf = 0
    not_attempted_cells = 0
    attempted_cells = 0
    unrescued_cells = []
    rescued_cells = []
    not_attempted_list = []

    for entry in manifest:
        s, c, j = entry['subject'], entry['condition'], entry['judge']
        pf = entry['parse_failures']
        bf_path = BACKFILL_DIR / f'{s}__{c}__{j}.json'
        if not bf_path.exists():
            not_attempted_pf += pf
            not_attempted_cells += 1
            not_attempted_list.append((s, c, j, pf))
            continue
        attempted_cells += 1
        try:
            rows = json.load(bf_path.open(encoding='utf-8'))
        except Exception as e:
            print(f'[WARN] {bf_path.name}: {e}')
            continue
        rescued = sum(1 for r in rows if not r.get('parse_failure') and isinstance(r.get('score'), int) and 1 <= r.get('score', 0) <= 5)
        failed = sum(1 for r in rows if r.get('parse_failure') or r.get('score') in (0, None))
        rescued_total += rescued
        unrescued_total += failed
        cell_record = {
            'subject': s, 'condition': c, 'judge': j,
            'manifest_pf': pf, 'rescued': rescued, 'still_failed': failed,
            'total_in_backfill': len(rows),
        }
        if failed > 0:
            unrescued_cells.append(cell_record)
        else:
            rescued_cells.append(cell_record)

    print(f'Attempted cells: {attempted_cells}')
    print(f'Cells fully rescued (no remaining failures): {len(rescued_cells)}')
    print(f'Cells with remaining failures: {len(unrescued_cells)}')
    print(f'Cells never attempted: {not_attempted_cells} (covers {not_attempted_pf} PF rows)')
    print(f'Rescued rows: {rescued_total}')
    print(f'Still-failed rows in attempted cells: {unrescued_total}')
    print()
    print('Top 30 cells with unrescued rows (by remaining failures):')
    for c in sorted(unrescued_cells, key=lambda x: -x['still_failed'])[:30]:
        print(f'  {c["subject"]:<22} {c["condition"]:<35} {c["judge"]:<14} rescued={c["rescued"]:>3} still_failed={c["still_failed"]:>3}')

    # Aggregate remaining work by judge
    rem_by_judge = defaultdict(int)
    for c in unrescued_cells:
        rem_by_judge[c['judge']] += c['still_failed']
    for s, c, j, pf in not_attempted_list:
        rem_by_judge[j] += pf
    print()
    print('Remaining failures by judge (incl. never-attempted):')
    for j, n in sorted(rem_by_judge.items(), key=lambda x: -x[1]):
        print(f'  {j:<14} {n:>5}')

    out = {
        'manifest_cells': len(manifest),
        'attempted_cells': attempted_cells,
        'fully_rescued_cells': len(rescued_cells),
        'unrescued_cells': unrescued_cells,
        'never_attempted_cells': [
            {'subject': s, 'condition': c, 'judge': j, 'manifest_pf': pf}
            for s, c, j, pf in not_attempted_list
        ],
        'rescued_total_rows': rescued_total,
        'still_failed_rows_attempted': unrescued_total,
        'never_attempted_pf_rows': not_attempted_pf,
        'remaining_by_judge': dict(rem_by_judge),
    }
    out_path = REPO / 'docs' / 'research' / '_audit_20260507_remaining_work.json'
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(f'\nWrote {out_path}')


if __name__ == '__main__':
    main()
