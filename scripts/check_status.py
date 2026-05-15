"""Quick status check for memory systems expansion. Run: python check_status.py"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime

# NOTE: depends on the separate (private) memory_system repo. Set MEMORY_SYSTEM_ROOT
# to its path; defaults to empty so the missing-path failure is obvious.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
base = os.path.join(MEMORY_SYSTEM_ROOT, 'data/experiments/memory_systems/results')
systems = ['mem0', 'letta', 'supermemory', 'zep']
subjects = ['zitkala_sa','hamerton','keckley','yung_wing','seacole','sunity_devee',
            'equiano','augustine','ebers','fukuzawa','cellini','bernal_diaz','rousseau','babur']
fact_counts = {'zitkala_sa':343,'hamerton':462,'keckley':542,'yung_wing':747,'seacole':775,
               'sunity_devee':815,'equiano':1145,'augustine':1146,'ebers':1285,'fukuzawa':1657,
               'cellini':2597,'bernal_diaz':2827,'rousseau':4562,'babur':4815}

def get_dir(s):
    if s == 'hamerton':
        return os.path.join(base, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(base, f'global_{s}')

def get_status(s, sys_name):
    d = get_dir(s)
    # Check for completed results (retrieve/generate/judge phases)
    results = os.path.join(d, f'{sys_name}_results.json')
    judgments = os.path.join(d, f'{sys_name}_judgments_merged.json')
    retrieval = os.path.join(d, f'{sys_name}_retrieval.json')
    ing = os.path.join(d, f'{sys_name}_ingestion.json')
    cp = os.path.join(d, f'{sys_name}_ingestion_checkpoint.json')

    if os.path.exists(judgments):
        return 'JUDGED'
    if os.path.exists(results):
        data = json.load(open(results, encoding='utf-8'))
        return f'GEN({len(data)})'
    if os.path.exists(retrieval):
        data = json.load(open(retrieval, encoding='utf-8'))
        return f'RET({len(data)})'
    if os.path.exists(ing):
        data = json.load(open(ing, encoding='utf-8'))
        v = data.get('verification_passed', False)
        return 'ING-OK' if v else 'ING-FAIL'
    if os.path.exists(cp):
        data = json.load(open(cp, encoding='utf-8'))
        p = data.get('facts_posted',0)
        e = data.get('facts_expected',1)
        return f'{int(p/e*100)}%'
    return '--'

print(f'MEMORY EXPANSION STATUS — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"Subject":20s} {"Facts":>5s} {"Mem0":>8s} {"Letta":>8s} {"SM":>8s} {"Zep":>8s}')
print('-'*55)

totals = {s: {'done':0, 'ingest':0, 'progress':0, 'pending':0} for s in systems}

for s in subjects:
    row = f'{s:20s} {fact_counts[s]:5d}'
    for sys_name in systems:
        st = get_status(s, sys_name)
        row += f' {st:>8s}'

        if st in ('JUDGED',):
            totals[sys_name]['done'] += 1
        elif st.startswith('ING') or st.startswith('GEN') or st.startswith('RET'):
            totals[sys_name]['ingest'] += 1
        elif st.endswith('%'):
            totals[sys_name]['progress'] += 1
        else:
            totals[sys_name]['pending'] += 1
    print(row)

print('-'*55)
print(f'{"TOTALS":20s} {sum(fact_counts.values()):5d}', end='')
for sys_name in systems:
    t = totals[sys_name]
    print(f' {t["done"]}d/{t["ingest"]}i/{t["progress"]}p', end='')
print()
print(f'\nPhase legend: -- pending, N% ingesting, ING-OK ingested, RET(N) retrieved, GEN(N) generated, JUDGED done')
