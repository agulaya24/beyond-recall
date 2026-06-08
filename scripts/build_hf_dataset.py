# -*- coding: utf-8 -*-
import os, json, glob
ROOT = r'C:\Users\Aarik\Anthropic\memory-study-repo'
DATA = os.path.join(ROOT, 'data'); RESULTS = os.path.join(ROOT, 'results')
OUT = os.path.join(ROOT, 'hf_dataset_build'); os.makedirs(OUT, exist_ok=True)
def jload(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception as e: print('  ! parse fail', os.path.relpath(p, ROOT), e); return None
subject_dirs = {}
for d in sorted(os.listdir(DATA)):
    p = os.path.join(DATA, d)
    if not os.path.isdir(p): continue
    if d == 'global_subjects':
        for s in sorted(os.listdir(p)):
            sp = os.path.join(p, s)
            if os.path.isdir(sp): subject_dirs[s] = sp
    elif d in ('source_corpora',): continue
    else:
        if any(os.path.exists(os.path.join(p, f)) for f in ('battery.json','facts.json')) or any(glob.glob(os.path.join(p,'*_v4.md'))) or os.path.isdir(os.path.join(p,'spec')):
            subject_dirs[d] = p
print('subjects found:', len(subject_dirs), sorted(subject_dirs))
specs, batteries, facts = [], [], []
SPEC = {'anchors':['anchors_v4.md','anchors*.md'],'core':['core_v4.md','core*.md'],
        'predictions':['predictions_v4.md','predictions*.md'],'brief':['brief_v5_clean.md','brief_v5.md','brief*.md'],
        'full_spec':['spec_production.md','spec.md']}
for subj, sp in subject_dirs.items():
    for layer, pats in SPEC.items():
        found=None
        for d in (sp, os.path.join(sp,'spec')):
            if not os.path.isdir(d): continue
            for pat in pats:
                hits=sorted(glob.glob(os.path.join(d,pat)))
                if hits: found=hits[0]; break
            if found: break
        if found:
            try: specs.append({'subject':subj,'layer':layer,'file':os.path.relpath(found,DATA),'text':open(found,encoding='utf-8').read()})
            except Exception as e: print('  ! spec',subj,layer,e)
    for qf in glob.glob(os.path.join(sp,'battery.json'))+glob.glob(os.path.join(sp,'questions_80*.json')):
        o=jload(qf)
        if isinstance(o,dict) and isinstance(o.get('questions'),list):
            for q in o['questions']:
                if isinstance(q,dict): batteries.append({'subject':subj,'source_file':os.path.basename(qf),**{k:(json.dumps(v) if isinstance(v,(dict,list)) else v) for k,v in q.items()}})
    for ff in glob.glob(os.path.join(sp,'facts.json'))+glob.glob(os.path.join(sp,'*shared_facts.json')):
        o=jload(ff)
        if isinstance(o,dict) and isinstance(o.get('facts'),list):
            for fct in o['facts']:
                if isinstance(fct,dict): facts.append({'subject':subj,'source_file':os.path.basename(ff),**{k:(json.dumps(v) if isinstance(v,(dict,list)) else v) for k,v in fct.items()}})
corpora=[]
scd=os.path.join(DATA,'source_corpora')
if os.path.isdir(scd):
    for f in sorted(glob.glob(os.path.join(scd,'**','*.txt'),recursive=True)):
        try: corpora.append({'file':os.path.relpath(f,scd),'text':open(f,encoding='utf-8').read()})
        except Exception as e: print('  ! corpus',f,e)
results=[]
for rf in glob.glob(os.path.join(RESULTS,'**','*.json'),recursive=True):
    o=jload(rf); rel=os.path.relpath(rf,RESULTS)
    if isinstance(o,dict) and isinstance(o.get('subjects'),dict):
        for subj,metrics in o['subjects'].items():
            results.append({'source_file':rel,'system':o.get('system'),'run_id':o.get('run_id'),'subject':subj,'metrics':json.dumps(metrics) if isinstance(metrics,(dict,list)) else metrics})
    else:
        results.append({'source_file':rel,'system':(o or {}).get('system') if isinstance(o,dict) else None,'raw':json.dumps(o)[:200000] if o is not None else None})
def write(name,rows):
    p=os.path.join(OUT,name+'.jsonl')
    with open(p,'w',encoding='utf-8') as fh:
        for r in rows: fh.write(json.dumps(r,ensure_ascii=False)+'\n')
    print(f'{name}: {len(rows)} rows, {os.path.getsize(p)/1e6:.1f} MB')
    if rows: print('   keys:', list(rows[0].keys())[:10])
print('--- configs ---')
for n,r in [('specifications',specs),('batteries',batteries),('facts',facts),('corpora',corpora),('results',results)]: write(n,r)
print('spec subjects covered:', len(set(s['subject'] for s in specs)))
