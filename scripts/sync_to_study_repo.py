"""Sync ALL completed memory system results to the study repo.
Covers: Option A (4 systems), Option B (fullpipeline), Base Layer, C8/C9, core results.
Run after experiments complete: python sync_to_study_repo.py
"""
import json, os, shutil, sys, glob
from datetime import datetime

# NOTE: the source side is the separate (private) memory_system repo. Set
# MEMORY_SYSTEM_ROOT to its path; defaults to empty so a missing path is obvious.
MEMORY_SYSTEM_ROOT = os.environ.get("MEMORY_SYSTEM_ROOT", "")
src_base = os.path.join(MEMORY_SYSTEM_ROOT, 'data/experiments/memory_systems/results')
dst_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
systems = ['mem0', 'letta', 'supermemory', 'zep']
subjects = ['zitkala_sa','hamerton','keckley','yung_wing','seacole','sunity_devee',
            'equiano','augustine','ebers','fukuzawa','cellini','bernal_diaz','rousseau','babur']

JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54', 'gemini_flash']

def src_dir(s):
    if s == 'hamerton':
        return os.path.join(src_base, 'run_fullstack_hamerton_20260411_231237')
    return os.path.join(src_base, f'global_{s}')

def dst_dir(s):
    if s == 'hamerton':
        return os.path.join(dst_base, 'hamerton')
    return os.path.join(dst_base, f'global_{s}')

def sync_file(src, dst, label):
    if not os.path.exists(src):
        return 0
    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
        shutil.copy2(src, dst)
        print(f'  {label}')
        return 1
    return 0

copied = 0
for s in subjects:
    sd = src_dir(s)
    dd = dst_dir(s)
    os.makedirs(dd, exist_ok=True)

    # === Option A: 4 memory systems (controlled, pre-extracted facts) ===
    for sys_name in systems:
        for suffix in ['ingestion', 'retrieval', 'results', 'judgments_merged']:
            copied += sync_file(
                os.path.join(sd, f'{sys_name}_{suffix}.json'),
                os.path.join(dd, f'{sys_name}_{suffix}.json'),
                f'{s}/{sys_name}_{suffix}.json')
        for j in JUDGES:
            copied += sync_file(
                os.path.join(sd, f'{sys_name}_judgments_{j}.json'),
                os.path.join(dd, f'{sys_name}_judgments_{j}.json'),
                f'{s}/{sys_name}_judgments_{j}.json')

    # === Option B: fullpipeline (native extraction) ===
    for sys_name in systems:
        for suffix in ['extracted', 'ingestion', 'retrieval', 'results', 'judgments_merged']:
            copied += sync_file(
                os.path.join(sd, f'{sys_name}_fullpipeline_{suffix}.json'),
                os.path.join(dd, f'{sys_name}_fullpipeline_{suffix}.json'),
                f'{s}/{sys_name}_fullpipeline_{suffix}.json')
        for j in JUDGES:
            copied += sync_file(
                os.path.join(sd, f'{sys_name}_fullpipeline_judgments_{j}.json'),
                os.path.join(dd, f'{sys_name}_fullpipeline_judgments_{j}.json'),
                f'{s}/{sys_name}_fullpipeline_judgments_{j}.json')

    # === Base Layer (5th retrieval system) ===
    for suffix in ['results', 'retrieval', 'judgments_merged']:
        copied += sync_file(
            os.path.join(sd, f'baselayer_{suffix}.json'),
            os.path.join(dd, f'baselayer_{suffix}.json'),
            f'{s}/baselayer_{suffix}.json')
    for j in JUDGES:
        copied += sync_file(
            os.path.join(sd, f'baselayer_judgments_{j}.json'),
            os.path.join(dd, f'baselayer_judgments_{j}.json'),
            f'{s}/baselayer_judgments_{j}.json')

    # === C8/C9 (raw corpus +/- spec) ===
    copied += sync_file(
        os.path.join(sd, 'c8_c9_results.json'),
        os.path.join(dd, 'c8_c9_results.json'),
        f'{s}/c8_c9_results.json')
    copied += sync_file(
        os.path.join(sd, 'c8_c9_judgments_merged.json'),
        os.path.join(dd, 'c8_c9_judgments_merged.json'),
        f'{s}/c8_c9_judgments_merged.json')
    for j in JUDGES:
        copied += sync_file(
            os.path.join(sd, f'c8_c9_judgments_{j}.json'),
            os.path.join(dd, f'c8_c9_judgments_{j}.json'),
            f'{s}/c8_c9_judgments_{j}.json')

    # === Core results (C1-C5 baseline conditions) ===
    for fname in ['results.json', 'judgments.json', 'results_v2.json', 'judgments_v2.json',
                  'results_harmonized.json', 'judgments_harmonized.json',
                  'battery.json', 'battery_v2.json', 'battery_gpt54.json',
                  'facts.json', 'spec.md', 'heldout.txt', 'manifest.json',
                  'fullstack_haiku.json']:
        copied += sync_file(
            os.path.join(sd, fname),
            os.path.join(dd, fname),
            f'{s}/{fname}')

    # === Gemini Pro judgments ===
    for fname in ['gemini_pro_judgments.json', 'judgments_v2_gemini_pro2.json',
                  'judgments_v2_gemini_pro_key2.json', 'gpt54_judgments.json']:
        copied += sync_file(
            os.path.join(sd, fname),
            os.path.join(dd, fname),
            f'{s}/{fname}')

# === Top-level analysis and manifests ===
for sys_name in systems:
    for fname in [f'{sys_name}_manifest.json', f'{sys_name}_analysis.json']:
        copied += sync_file(
            os.path.join(src_base, fname),
            os.path.join(dst_base, fname),
            fname)

# === Provider experience ledger ===
ledger_src = os.path.join(MEMORY_SYSTEM_ROOT, 'data/experiments/memory_systems/PROVIDER_EXPERIENCE_LEDGER.md')
ledger_dst = os.path.join(dst_base, '..', 'docs', 'PROVIDER_EXPERIENCE_LEDGER.md')
if os.path.exists(ledger_src):
    os.makedirs(os.path.dirname(ledger_dst), exist_ok=True)
    copied += sync_file(ledger_src, ledger_dst, 'PROVIDER_EXPERIENCE_LEDGER.md')

print(f'\nSynced {copied} files at {datetime.now().strftime("%H:%M:%S")}')
