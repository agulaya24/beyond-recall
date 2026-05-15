"""
Pipeline variance measurement for v10 paper §6.3.

Measures run-to-run variance of the Base Layer pipeline at temperature 0
on three representative subjects spanning the gradient.

Scope: LIGHTER (author + compose only). Extraction is held constant by
reusing each subject's per-environment SQLite state at
ENVS_DIR/<subject>_memory/data/database/memory.db. Each rerun re-runs:

  Step 4 (author_layers --generate all)  : ANCHORS, CORE, PREDICTIONS layers
                                           via Sonnet through structured outputs
                                           and Citations API (T=0 on prose,
                                           default T on JSON-schema predictions).
  Step 5 (cli compose)                   : Unified brief via Opus (T=0).

Steps 1-3 (import, extract, embed) are not rerun. The fact set fed into the
authoring layers is identical across reruns within a subject. The variance
measured here is therefore the variance the authoring + compose stages
introduce on top of a fixed corpus, which is the fragment of pipeline
variance §6.3 most directly speaks to.

Each rerun's spec artifacts are snapshotted to
  data/global_<subject>/_variance_runs/run_<N>/
and are NEVER written over the canonical spec_production.md.

Each rerun's responses + judgments are written to
  results/global_<subject>/_variance_runs/run_<N>_responses.json
  results/global_<subject>/_variance_runs/run_<N>_judgments_<judge>.json

Atomic writes per question, resumable.

Usage:
  python _v10_pipeline_variance.py --subject sunity_devee --rerun 1 --phase spec
  python _v10_pipeline_variance.py --subject sunity_devee --rerun 1 --phase response
  python _v10_pipeline_variance.py --subject sunity_devee --rerun 1 --phase judge
  python _v10_pipeline_variance.py --subject sunity_devee --rerun 1 --phase all
  python _v10_pipeline_variance.py --all   # All 3 subjects, 3 reruns each, full pipeline
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / 'results'
DATA_GLOBAL = REPO / 'data' / 'global_subjects'
# NOTE: global_subject_environments and the memory_system repo both live outside
# this repo. Set ANTHROPIC_ROOT to the directory that contains global_subject_environments,
# and MEMORY_SYSTEM_ROOT to the memory_system repo path. Both default to empty so
# a missing path is obvious.
ENVS_DIR = Path(os.environ.get("ANTHROPIC_ROOT", "")) / 'global_subject_environments'
MEMORY_SYSTEM_ROOT = Path(os.environ.get("MEMORY_SYSTEM_ROOT", ""))
SRC_DIR = MEMORY_SYSTEM_ROOT / 'src'

SUBJECTS = ['sunity_devee', 'yung_wing', 'augustine']
RERUNS = [1, 2, 3]

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

JUDGE_MODELS = {
    'haiku': ('anthropic', 'claude-haiku-4-5-20251001'),
    'sonnet': ('anthropic', 'claude-sonnet-4-6'),
    'opus': ('anthropic', 'claude-opus-4-6'),
    'gpt4o': ('openai', 'gpt-4o'),
    'gpt54': ('openai', 'gpt-5.4'),
}


def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)


def load_user_env(keys):
    """Read User-scope env vars on Windows via PowerShell."""
    env = {}
    for k in keys:
        if os.environ.get(k):
            env[k] = os.environ[k]
            continue
        try:
            r = subprocess.run(
                ['powershell', '-NoProfile', '-Command',
                 f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
                capture_output=True, text=True, timeout=10
            )
            v = (r.stdout or '').strip()
            if v:
                env[k] = v
                os.environ[k] = v
        except Exception as e:
            log(f'  WARN: could not read {k}: {e}')
    return env


def atomic_write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    for attempt in range(3):
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if path.exists():
                os.replace(tmp, path)
            else:
                os.rename(tmp, path)
            return
        except PermissionError:
            time.sleep(2)
            try:
                os.remove(tmp)
            except Exception:
                pass


def load_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.load(p.open(encoding='utf-8'))


# =====================================================================
# PHASE A: SPEC GENERATION (author + compose, snapshot to _variance_runs)
# =====================================================================

def make_pipeline_env(subject):
    """Build env for invoking baselayer.* against the per-subject env."""
    env_dir = ENVS_DIR / f'{subject}_memory'
    env = os.environ.copy()
    env['MEMORY_SYSTEM_ROOT'] = str(env_dir)
    env['BASELAYER_SKIP_COVERAGE_GATE'] = '1'
    env['BASELAYER_SKIP_FACT_FLOOR'] = '1'
    env['BASELAYER_SKIP_EXTRACTION_GATE'] = '1'
    env['BASELAYER_SKIP_MANIFEST_GATE'] = '1'
    env['OPENBLAS_NUM_THREADS'] = '1'
    env['OMP_NUM_THREADS'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    return env, env_dir


def run_author(subject):
    env, env_dir = make_pipeline_env(subject)
    log(f'  [author] generating layers for {subject}...')
    result = subprocess.run(
        [sys.executable, '-m', 'baselayer.author_layers', '--generate', 'all'],
        cwd=str(SRC_DIR), env=env,
        stdout=sys.stdout, stderr=sys.stderr, timeout=3600
    )
    if result.returncode != 0:
        log(f'  AUTHOR FAILED: exit {result.returncode}')
        return False
    return True


def run_compose(subject):
    env, env_dir = make_pipeline_env(subject)
    log(f'  [compose] composing brief for {subject}...')
    result = subprocess.run(
        [sys.executable, '-m', 'baselayer.cli', 'compose'],
        cwd=str(SRC_DIR), env=env,
        stdout=sys.stdout, stderr=sys.stderr, timeout=3600
    )
    if result.returncode != 0:
        log(f'  COMPOSE FAILED: exit {result.returncode}')
        return False
    return True


def build_spec_text(layers_dir):
    """Concatenate layer files into spec_production.md format
    (matching memory_system/data/experiments/memory_systems/run_overnight_pipeline.py:build_spec)."""
    parts = []
    for fname, header in [
        ('anchors_v4.md', '# ANCHORS'),
        ('core_v4.md', '# CORE'),
        ('predictions_v4.md', '# PREDICTIONS'),
        ('brief_v5.md', '# UNIFIED BRIEF'),
    ]:
        p = layers_dir / fname
        if p.exists():
            parts.append(f'{header}\n{p.read_text(encoding="utf-8")}')
    if not parts:
        return None
    return '\n\n'.join(parts)


def snapshot_layers(subject, rerun):
    """Copy current layer files to data/global_<subject>/_variance_runs/run_<N>/."""
    env_dir = ENVS_DIR / f'{subject}_memory'
    layers_dir = env_dir / 'data' / 'identity_layers'
    snap_dir = DATA_GLOBAL / subject / '_variance_runs' / f'run_{rerun}'
    snap_dir.mkdir(parents=True, exist_ok=True)
    layer_files = ['anchors_v4.md', 'core_v4.md', 'predictions_v4.md',
                   'brief_v5.md', 'brief_v5_clean.md']
    snapshotted = []
    for f in layer_files:
        src = layers_dir / f
        if src.exists():
            shutil.copy2(src, snap_dir / f)
            snapshotted.append(f)
    spec_text = build_spec_text(layers_dir)
    if spec_text:
        (snap_dir / 'spec_production.md').write_text(spec_text, encoding='utf-8')
        snapshotted.append('spec_production.md')
    log(f'  [snapshot] {subject} run {rerun}: {snapshotted}')
    return snap_dir


def phase_spec(subject, rerun):
    """Run author + compose, then snapshot. Skip if snapshot already complete."""
    snap_dir = DATA_GLOBAL / subject / '_variance_runs' / f'run_{rerun}'
    spec_path = snap_dir / 'spec_production.md'
    if spec_path.exists() and len(spec_path.read_text(encoding='utf-8')) > 1000:
        log(f'  [spec] {subject} run {rerun}: already done, skip')
        return True
    log(f'  [spec] {subject} run {rerun}: starting')
    if not run_author(subject):
        return False
    if not run_compose(subject):
        return False
    snap_dir = snapshot_layers(subject, rerun)
    return (snap_dir / 'spec_production.md').exists()


# =====================================================================
# PHASE B: RESPONSE GENERATION (C2a, C4a) on existing battery
# =====================================================================

def load_battery(subject):
    """Behavioral-prediction questions only, with held-out passages."""
    bat = load_json(RESULTS / f'global_{subject}' / 'battery_v2.json')
    return [q for q in bat['questions']
            if q['tier'] == 'behavioral_prediction' and q.get('held_out_passage')]


def load_facts_concat(subject):
    """Full extracted fact set, formatted as a bullet list (C4a context)."""
    facts_path = RESULTS / f'global_{subject}' / 'facts.json'
    data = json.load(facts_path.open(encoding='utf-8'))
    if isinstance(data, dict):
        items = data.get('facts', [])
    else:
        items = data
    texts = [f['text'] if isinstance(f, dict) else f for f in items]
    return '\n'.join(f'- {t}' for t in texts)


def load_rerun_spec(subject, rerun):
    p = DATA_GLOBAL / subject / '_variance_runs' / f'run_{rerun}' / 'spec_production.md'
    return p.read_text(encoding='utf-8') if p.exists() else None


def api_call_anthropic(api_key, model, system_prompt, user_message,
                      max_tokens=1024, temperature=0, timeout=180):
    last = None
    for attempt in range(3):
        try:
            kw = {
                'model': model,
                'max_tokens': max_tokens,
                'temperature': temperature,
                'messages': [{'role': 'user', 'content': user_message}],
            }
            if system_prompt:
                kw['system'] = system_prompt
            r = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json=kw,
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                timeout=timeout,
            )
            r.raise_for_status()
            d = r.json()
            return {
                'text': d['content'][0]['text'],
                'input_tokens': d['usage']['input_tokens'],
                'output_tokens': d['usage']['output_tokens'],
                'model': model,
                'temperature': temperature,
            }
        except Exception as e:
            last = e
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise last


def api_call_openai(api_key, model, prompt, max_tokens=8, temperature=0):
    last = None
    for attempt in range(3):
        try:
            r = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={
                    'model': model,
                    'max_completion_tokens': max_tokens,
                    'temperature': temperature,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            last = e
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise last


def phase_response(subject, rerun, api_key):
    """Generate C2a (spec only) and C4a (facts + spec) for the rerun's spec."""
    spec = load_rerun_spec(subject, rerun)
    if not spec:
        log(f'  [response] {subject} run {rerun}: no spec yet, skip')
        return False
    questions = load_battery(subject)
    facts_text = load_facts_concat(subject)

    out_path = RESULTS / f'global_{subject}' / '_variance_runs' / f'run_{rerun}_responses.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_json(out_path) or []
    done = set()
    for r in existing:
        for c in r.get('responses', {}):
            done.add(f"{r['question_id']}_{c}")

    log(f'  [response] {subject} run {rerun}: {len(done)} already done, '
        f'{2 * len(questions) - len(done)} remaining')

    by_id = {r['question_id']: r for r in existing}

    for q in questions:
        qid = q['id']
        if qid not in by_id:
            r = {
                'question_id': qid,
                'question_text': q['text'],
                'held_out_passage': q['held_out_passage'],
                'responses': {},
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
            existing.append(r)
            by_id[qid] = r
        rec = by_id[qid]

        # C2a: spec only
        if f'{qid}_C2a_full_spec' not in done:
            sys_prompt = (
                'The following is a behavioral specification describing your user — '
                'how they think, decide, and act.\n\n'
                '=== BEHAVIORAL SPECIFICATION ===\n' + spec
            )
            try:
                rsp = api_call_anthropic(
                    api_key, RESPONSE_MODEL, sys_prompt, q['text'],
                    max_tokens=1024, temperature=0, timeout=180,
                )
                rec['responses']['C2a_full_spec'] = rsp
                log(f'    Q{qid} C2a: {rsp["output_tokens"]}t')
            except Exception as e:
                log(f'    Q{qid} C2a FAILED: {e}')
                rec['responses']['C2a_full_spec'] = {'error': str(e)}
            atomic_write_json(out_path, existing)

        # C4a: facts + spec
        if f'{qid}_C4a_full_facts_plus_spec' not in done:
            sys_prompt = (
                'The following is a behavioral specification describing your user. '
                'You also have the complete set of known facts.\n\n'
                '=== BEHAVIORAL SPECIFICATION ===\n' + spec + '\n\n'
                '=== ALL KNOWN FACTS ===\n' + facts_text
            )
            try:
                rsp = api_call_anthropic(
                    api_key, RESPONSE_MODEL, sys_prompt, q['text'],
                    max_tokens=1024, temperature=0, timeout=180,
                )
                rec['responses']['C4a_full_facts_plus_spec'] = rsp
                log(f'    Q{qid} C4a: {rsp["output_tokens"]}t')
            except Exception as e:
                log(f'    Q{qid} C4a FAILED: {e}')
                rec['responses']['C4a_full_facts_plus_spec'] = {'error': str(e)}
            atomic_write_json(out_path, existing)
    return True


# =====================================================================
# PHASE C: JUDGE (5-judge primary panel)
# =====================================================================

def judge_prompt(held_out, response_text):
    return (
        'You are evaluating whether a response about a person PREDICTED '
        'what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
        '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
        'Rate 1-5:\n5=Predicts specific outcome\n4=General direction correct\n'
        '3=Right domain wrong outcome\n2=Wrong prediction\n1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def parse_score(text):
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def run_judge(judge_name, prompt, api_keys):
    raw = ''
    try:
        provider, model = JUDGE_MODELS[judge_name]
        if provider == 'anthropic':
            r = api_call_anthropic(
                api_keys['ANTHROPIC_API_KEY'], model, None, prompt,
                max_tokens=8, timeout=60,
            )
            raw = r['text']
        elif provider == 'openai':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], model, prompt)
    except Exception as e:
        return 0, f'ERR: {e}', True
    score = parse_score(raw)
    return score, raw, (score == 0)


def phase_judge(subject, rerun, api_keys, judges=None):
    judges = judges or JUDGES
    resp_path = RESULTS / f'global_{subject}' / '_variance_runs' / f'run_{rerun}_responses.json'
    responses = load_json(resp_path)
    if not responses:
        log(f'  [judge] {subject} run {rerun}: no responses, skip')
        return False
    conditions = ['C2a_full_spec', 'C4a_full_facts_plus_spec']

    for judge_name in judges:
        jpath = RESULTS / f'global_{subject}' / '_variance_runs' / f'run_{rerun}_judgments_{judge_name}.json'
        existing = load_json(jpath) or []
        done = {(j['question_id'], j['condition']) for j in existing}

        new_count = 0
        for q_result in responses:
            qid = q_result['question_id']
            held_out = q_result.get('held_out_passage', '')
            if not held_out:
                continue
            for cond in conditions:
                if (qid, cond) in done:
                    continue
                resp = q_result.get('responses', {}).get(cond, {})
                resp_text = resp.get('text', '')
                if not resp_text or 'error' in resp:
                    existing.append({
                        'question_id': qid, 'condition': cond,
                        'judge': judge_name, 'score': 0,
                        'parse_failure': True,
                        'reason': 'no response',
                    })
                    atomic_write_json(jpath, existing)
                    continue
                score, raw, pf = run_judge(judge_name, judge_prompt(held_out, resp_text), api_keys)
                existing.append({
                    'question_id': qid, 'condition': cond,
                    'judge': judge_name, 'score': score,
                    'raw_response': raw if pf else '',
                    'parse_failure': pf,
                })
                new_count += 1
                atomic_write_json(jpath, existing)
        log(f'  [judge] {subject} run {rerun} / {judge_name}: {new_count} new')
    return True


# =====================================================================
# PHASE D: AGGREGATE
# =====================================================================

def aggregate_per_rerun(subject, rerun):
    """Aggregate judgments to (mean per condition) across the 5-judge panel,
    using the same hierarchy as recompute_5judge_primary.py: per-judge mean
    across questions, then mean across judges in the panel."""
    from collections import defaultdict
    import statistics

    per_jc = defaultdict(list)
    judge_coverage = set()
    for j in JUDGES:
        jp = (RESULTS / f'global_{subject}' / '_variance_runs'
              / f'run_{rerun}_judgments_{j}.json')
        rows = load_json(jp) or []
        for r in rows:
            if r.get('parse_failure') or r.get('score') in (None, 0):
                continue
            per_jc[(r['condition'], r['judge'])].append(r['score'])
            judge_coverage.add(r['judge'])

    per_condition = defaultdict(list)
    per_jc_means = {}
    for (cond, judge), scores in per_jc.items():
        if scores:
            mu = statistics.mean(scores)
            per_jc_means[(cond, judge)] = mu
            per_condition[cond].append(mu)
    means = {c: statistics.mean(ms) for c, ms in per_condition.items()}
    return {
        'subject': subject, 'rerun': rerun,
        'judges_with_data': sorted(judge_coverage),
        'per_judge_per_condition': {f'{c}__{j}': v for (c, j), v in per_jc_means.items()},
        'means': means,
    }


# =====================================================================
# DRIVER
# =====================================================================

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--subject', default=None, choices=SUBJECTS + [None])
    p.add_argument('--rerun', type=int, default=None, choices=RERUNS + [None])
    p.add_argument('--phase', default='all',
                   choices=['spec', 'response', 'judge', 'aggregate', 'all'])
    p.add_argument('--judge', default=None, help='Single judge name')
    p.add_argument('--all', action='store_true', help='Run all subjects x all reruns')
    args = p.parse_args()

    api_env = load_user_env(['ANTHROPIC_API_KEY', 'OPENAI_API_KEY'])
    if 'ANTHROPIC_API_KEY' not in api_env:
        log('FATAL: ANTHROPIC_API_KEY not set')
        sys.exit(1)

    if args.all:
        targets = [(s, n) for s in SUBJECTS for n in RERUNS]
    elif args.subject and args.rerun:
        targets = [(args.subject, args.rerun)]
    elif args.subject:
        targets = [(args.subject, n) for n in RERUNS]
    else:
        log('FATAL: specify --subject and --rerun, or --all')
        sys.exit(1)

    log(f'Variance runner: {len(targets)} (subject, rerun) pairs, phase={args.phase}')

    judges = [args.judge] if args.judge else JUDGES

    for subject, rerun in targets:
        log(f'\n=== {subject} / run {rerun} ===')
        if args.phase in ('spec', 'all'):
            ok = phase_spec(subject, rerun)
            if not ok:
                log(f'  spec failed for {subject}/{rerun}, skipping rest')
                continue
        if args.phase in ('response', 'all'):
            phase_response(subject, rerun, api_env['ANTHROPIC_API_KEY'])
        if args.phase in ('judge', 'all'):
            phase_judge(subject, rerun, api_env, judges=judges)
        if args.phase in ('aggregate', 'all'):
            agg = aggregate_per_rerun(subject, rerun)
            agg_path = (RESULTS / f'global_{subject}' / '_variance_runs'
                        / f'run_{rerun}_aggregate.json')
            atomic_write_json(agg_path, agg)
            log(f'  [aggregate] means: {agg["means"]}')

    log('DONE')


if __name__ == '__main__':
    main()
