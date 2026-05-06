"""
Predicate Ablation Experiment (Phase 2c) — disconfirmation test for the
pattern-predicate activation claim.

Both reviewers in
docs/reviews/pattern_activation_claim_review_20260428.md nominated
predicate-ablation regeneration with reversal control as the highest-priority
disconfirmation test for the strong predicate-mediated mechanism claim.

Sampling
========
For each of 12 to 20 sampled extreme-upward-jump cases, drawn from the 60
unique cases in docs/research/pattern_activation_deep_20260428.json,
stratified by:
  - mechanism category from deep analysis
    (PATTERN_PREDICATE / INFERENCE_CHAIN / mixed-other)
  - question axis (LITERAL_RECALL / INTERPRETIVE_INFERENCE /
    REFUSAL_TRIGGERING)
  - subject (>= 4 distinct, Hamerton capped at 5/16)

Default target: 16 cases = 8 PATTERN_PREDICATE_high + 4 INFERENCE_CHAIN +
4 mixed-other (PATTERN_PREDICATE_medium + UNCLEAR).

Three conditions per case
=========================
1. Original    : full served spec, regenerated under temperature=0 Haiku 4.5.
                 Sanity check: response panel mean should fall within
                 +/-0.5 of the recorded post_mean. Wider drift logged as a
                 stochasticity confound, not a script bug.
2. Ablation 1  : full served spec MINUS the heuristically-identified
                 causal predicate sentence (best_spec_sentence in the deep
                 analysis). Removed surgically and replaced with a length
                 matched neutral biographical filler sentence written by
                 Sonnet (so the spec's predicate density does not drop in
                 a way obvious to the model).
3. Ablation 2  : full served spec WITH the same predicate replaced by its
                 behavioral OPPOSITE, generated via Sonnet API call,
                 length and structure preserved.

Each variant is judged by the 5-judge primary panel
(haiku, sonnet, opus, gpt4o, gpt54). Per-case panel mean = mean of
per-judge scores (require >= 3 valid).

Decision rule (in the report)
=============================
- mean Δ_removal >= 1 anchor   -> STRONG framing supported.
- 0.5 <= mean Δ_removal < 1    -> CAUTIOUS framing only.
- mean Δ_removal < 0.5         -> claim does NOT survive; rater confabulation
                                   alternative is more parsimonious.

Important caveat
================
"Rater-identified causal predicate" in this script is a heuristic proxy:
it is the spec sentence with highest token overlap to the post-response
(see deep_pattern_activation_analysis.py classify_mechanism). It is NOT a
human rating. The reviewer framing assumed a human rater; we're using the
deep_pattern proxy as the most defensible automatic stand-in. Disclose
this in the resulting report.

Safety
======
This script is built but does not auto-run. It prints a banner and exits
unless --go is passed. The smoke run (without --go) loads inputs, computes
the sampling decision, saves it to a JSON file for reproducibility, then
exits 0 with no API calls.

Usage
=====
    python scripts/run_predicate_ablation.py            # smoke; no API calls
    python scripts/run_predicate_ablation.py --go       # actually run
    python scripts/run_predicate_ablation.py --target 14 # sample size
    python scripts/run_predicate_ablation.py --go --resume  # checkpoint resume

Outputs
=======
    docs/research/predicate_ablation_sampling_20260428.json  (sampling decision)
    docs/research/predicate_ablation_results_20260428.json   (full results)
    docs/research/predicate_ablation_results_20260428.md     (markdown report)
    docs/research/_predicate_ablation_checkpoint.json        (resume checkpoint)
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import statistics
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / 'scripts'))

# Reuse loaders / sentence splitter from existing study scripts.
from build_wins_inventory import (  # noqa: E402
    get_response_text,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEEP_PATH = REPO / 'docs' / 'research' / 'pattern_activation_deep_20260428.json'
WINS_PATH = REPO / 'docs' / 'research' / 'wins_inventory_20260428.json'
SAMPLING_OUT = REPO / 'docs' / 'research' / 'predicate_ablation_sampling_20260428.json'
RESULTS_JSON = REPO / 'docs' / 'research' / 'predicate_ablation_results_20260428.json'
RESULTS_MD = REPO / 'docs' / 'research' / 'predicate_ablation_results_20260428.md'
CHECKPOINT_PATH = REPO / 'docs' / 'research' / '_predicate_ablation_checkpoint.json'

HAMERTON_SPEC = REPO / 'data' / 'hamerton' / 'spec' / 'brief_v5_clean.md'
GLOBAL_SPEC_DIR = REPO / 'data' / 'global_subjects'

PRIMARY_JUDGES = ['haiku', 'sonnet', 'opus', 'gpt4o', 'gpt54']

RESPONSE_MODEL = 'claude-haiku-4-5-20251001'
SONNET_MODEL = 'claude-sonnet-4-6'
OPUS_MODEL = 'claude-opus-4-6'
HAIKU_JUDGE_MODEL = 'claude-haiku-4-5-20251001'
SONNET_JUDGE_MODEL = 'claude-sonnet-4-6'
OPUS_JUDGE_MODEL = 'claude-opus-4-6'
GPT4O_MODEL = 'gpt-4o'
GPT54_MODEL = 'gpt-5.4'

RNG_SEED = 20260428
DEFAULT_TARGET = 16
HAMERTON_CAP_FRACTION = 5 / 16  # max 5 of 16

# Mechanism strata
TARGET_STRATA = {
    'PATTERN_PREDICATE_high': 8,
    'INFERENCE_CHAIN': 4,
    'MIXED_OTHER': 4,    # PATTERN_PREDICATE_medium + UNCLEAR
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_FILE = REPO / 'docs' / 'research' / f'_predicate_ablation_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'


def log(msg: str) -> None:
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass


# ---------------------------------------------------------------------------
# API key loading (Windows User env, same pattern as run_global_rerun.py)
# ---------------------------------------------------------------------------

def load_api_keys() -> dict:
    keys = {}
    for k in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GEMINI_API_KEY']:
        try:
            r = subprocess.run(
                ['powershell', '-Command',
                 f"[System.Environment]::GetEnvironmentVariable('{k}','User')"],
                capture_output=True, text=True, timeout=15,
            )
            val = (r.stdout or '').strip()
        except Exception:
            val = ''
        if val:
            os.environ[k] = val
            keys[k] = val
    return keys


# ---------------------------------------------------------------------------
# Atomic JSON I/O
# ---------------------------------------------------------------------------

def atomic_write_json(path: Path, data) -> None:
    tmp_path = str(path) + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if path.exists():
        os.replace(tmp_path, path)
    else:
        os.rename(tmp_path, path)


def load_json(path: Path):
    if not path.exists():
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Spec loading (matches deep_pattern_activation_analysis.load_served_spec)
# ---------------------------------------------------------------------------

def load_served_spec(subject: str) -> str | None:
    if subject == 'hamerton':
        return HAMERTON_SPEC.read_text(encoding='utf-8') if HAMERTON_SPEC.exists() else None
    subj_dir = GLOBAL_SPEC_DIR / subject
    for fn in ('spec_production.md', 'spec.md'):
        p = subj_dir / fn
        if p.exists():
            return p.read_text(encoding='utf-8')
    return None


# ---------------------------------------------------------------------------
# Sentence splitter (same as deep analysis)
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n\n+", text) if len(s.strip()) > 20]


# ---------------------------------------------------------------------------
# Match the truncated best_spec_sentence back to the full sentence in the spec
# ---------------------------------------------------------------------------

TRUNC_MARKER = '... [truncated]'


def strip_trunc(s: str) -> str:
    if s.endswith(TRUNC_MARKER):
        return s[: -len(TRUNC_MARKER)]
    return s


def find_full_spec_sentence(spec_text: str, truncated_key: str) -> str | None:
    """Find the full sentence in spec_text whose prefix matches truncated_key.

    Strategy: split spec into sentences with the same splitter the deep
    analysis used, then try a unique prefix match. Tries 100, 80, 60, 40
    char prefixes of the (de-truncated) key.
    """
    if not spec_text or not truncated_key:
        return None
    key = strip_trunc(truncated_key).strip()
    if not key:
        return None
    # Direct exact match (key wasn't truncated):
    spec_sents = split_sentences(spec_text)
    for s in spec_sents:
        if s == key:
            return s
    # Unique-prefix match: try shrinking prefixes.
    for plen in (120, 100, 80, 60, 40):
        prefix = key[:plen]
        if len(prefix) < 20:
            continue
        matches = [s for s in spec_sents if s.startswith(prefix)]
        if len(matches) == 1:
            return matches[0]
    # Fallback: any substring match in raw spec, then re-extract the sentence.
    if key[:60] in spec_text:
        # Locate and walk forward to a sentence terminator.
        idx = spec_text.find(key[:60])
        # Walk back to start of sentence.
        start = idx
        while start > 0 and spec_text[start - 1] not in '.!?\n':
            start -= 1
        # Walk forward to end of sentence.
        end = idx + 60
        while end < len(spec_text) and spec_text[end] not in '.!?\n':
            end += 1
        if end < len(spec_text):
            end += 1
        sent = spec_text[start:end].strip()
        if len(sent) > 40:
            return sent
    return None


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------

def classify_stratum(case: dict) -> str:
    cat = case['mechanism']['category']
    conf = case['mechanism']['confidence']
    if cat == 'PATTERN_PREDICATE' and conf == 'high':
        return 'PATTERN_PREDICATE_high'
    if cat == 'INFERENCE_CHAIN':
        return 'INFERENCE_CHAIN'
    return 'MIXED_OTHER'  # PATTERN_PREDICATE medium, UNCLEAR


def sample_cases(extreme_jumps: list[dict], target: int, rng: random.Random) -> list[dict]:
    """Stratified sampling. Per stratum: balance axis and subject diversity.

    Returns the selected cases, with stratum field added.
    """
    # Bucket by stratum.
    by_stratum: dict[str, list[dict]] = defaultdict(list)
    for j in extreme_jumps:
        s = classify_stratum(j)
        rec = dict(j)
        rec['_stratum'] = s
        by_stratum[s].append(rec)

    # Scale stratum targets to the requested total if non-default.
    if target == DEFAULT_TARGET:
        targets = dict(TARGET_STRATA)
    else:
        # Proportional rescale.
        total_default = sum(TARGET_STRATA.values())
        targets = {k: max(1, round(v * target / total_default)) for k, v in TARGET_STRATA.items()}
        # Trim to target if we overshoot.
        excess = sum(targets.values()) - target
        for k in list(targets.keys()):
            while excess > 0 and targets[k] > 1:
                targets[k] -= 1
                excess -= 1

    hamerton_cap = max(1, int(round(HAMERTON_CAP_FRACTION * target)))
    selected: list[dict] = []
    hamerton_count = 0

    for stratum, want in targets.items():
        pool = list(by_stratum.get(stratum, []))
        if not pool:
            log(f'  WARN: stratum {stratum} is empty')
            continue
        rng.shuffle(pool)

        # Within-stratum: prefer axis diversity, then subject diversity, then
        # respect hamerton cap.
        picked = []
        seen_axes: set[str] = set()
        seen_subjects: set[str] = set()

        # Pass 1: cover each available axis once if possible.
        axes_in_pool = set(c['axis'] for c in pool)
        for ax in sorted(axes_in_pool):
            for c in pool:
                if c in picked:
                    continue
                if c['axis'] != ax:
                    continue
                if c['subject'] == 'hamerton' and hamerton_count >= hamerton_cap:
                    continue
                picked.append(c)
                seen_axes.add(c['axis'])
                seen_subjects.add(c['subject'])
                if c['subject'] == 'hamerton':
                    hamerton_count += 1
                break
            if len(picked) >= want:
                break

        # Pass 2: fill remaining slots, preferring new subjects.
        remaining_pool = [c for c in pool if c not in picked]
        remaining_pool.sort(key=lambda c: (c['subject'] in seen_subjects, c['subject']))
        for c in remaining_pool:
            if len(picked) >= want:
                break
            if c['subject'] == 'hamerton' and hamerton_count >= hamerton_cap:
                continue
            picked.append(c)
            seen_subjects.add(c['subject'])
            if c['subject'] == 'hamerton':
                hamerton_count += 1

        # Pass 3: if still short, allow hamerton-cap exception only as last resort.
        if len(picked) < want:
            for c in pool:
                if c in picked:
                    continue
                if len(picked) >= want:
                    break
                picked.append(c)
                if c['subject'] == 'hamerton':
                    hamerton_count += 1

        log(f'  {stratum}: picked {len(picked)}/{want} (axes={sorted(seen_axes)}, subjects={sorted(seen_subjects)})')
        selected.extend(picked)

    # Trim or pad to the exact target if needed.
    if len(selected) > target:
        selected = selected[:target]

    return selected


def build_sampling_record(selected: list[dict], extreme_jumps: list[dict],
                           target: int, seed: int) -> dict:
    """Augment selected cases with full-sentence matches and metadata."""
    enriched = []
    unmatched = []
    for c in selected:
        subject = c['subject']
        spec_text = load_served_spec(subject)
        truncated = c['mechanism'].get('best_spec_sentence') or ''
        full = find_full_spec_sentence(spec_text, truncated) if spec_text else None
        if not full:
            unmatched.append({'subject': subject, 'qid': c['qid'],
                              'truncated_key': truncated[:120]})
        enriched.append({
            'subject': subject,
            'qid': c['qid'],
            'axis': c['axis'],
            'mechanism_category': c['mechanism']['category'],
            'mechanism_confidence': c['mechanism']['confidence'],
            'stratum': c['_stratum'],
            'pre_condition': c['pre_condition'],
            'post_condition': c['post_condition'],
            'recorded_post_mean': c['post_mean'],
            'recorded_post_band': c['post_band'],
            'jump': c['jump'],
            'observed_in_pairs': c['observed_in_pairs'],
            'question_text': c['question_text'],
            'held_out_passage': c['held_out_passage'],
            'best_spec_sentence_truncated': truncated,
            'matched_full_sentence': full,
            'matched': full is not None,
            'subject_spec_path': str(HAMERTON_SPEC if subject == 'hamerton'
                                     else GLOBAL_SPEC_DIR / subject / 'spec_production.md'),
        })

    stratum_counts = defaultdict(int)
    subject_counts = defaultdict(int)
    axis_counts = defaultdict(int)
    for e in enriched:
        stratum_counts[e['stratum']] += 1
        subject_counts[e['subject']] += 1
        axis_counts[e['axis']] += 1

    return {
        'date': datetime.now(timezone.utc).isoformat(),
        'seed': seed,
        'target': target,
        'selected_count': len(enriched),
        'matched_count': sum(1 for e in enriched if e['matched']),
        'unmatched_count': len(unmatched),
        'unmatched': unmatched,
        'stratum_targets': TARGET_STRATA,
        'stratum_counts': dict(stratum_counts),
        'subject_distribution': dict(subject_counts),
        'axis_distribution': dict(axis_counts),
        'hamerton_cap_max': max(1, int(round(HAMERTON_CAP_FRACTION * target))),
        'selection_algorithm': 'stratified random; per-stratum axis-first then subject diversity; hamerton capped per fraction; fixed seed',
        'served_spec_definition': {
            'hamerton': str(HAMERTON_SPEC.relative_to(REPO)),
            'globals': 'data/global_subjects/<subject>/spec_production.md',
        },
        'response_model': RESPONSE_MODEL,
        'panel': PRIMARY_JUDGES,
        'selected': enriched,
    }


# ---------------------------------------------------------------------------
# API helpers (mirrors run_global_rerun pattern)
# ---------------------------------------------------------------------------

import httpx  # noqa: E402


def api_call_anthropic(api_key: str, model: str, system_prompt: str | None,
                       user_message: str, max_tokens: int = 1024,
                       temperature: float = 0.0, timeout: int = 180) -> dict:
    last_err = None
    for attempt in range(3):
        try:
            kwargs = {
                'model': model, 'max_tokens': max_tokens,
                'temperature': temperature,
                'messages': [{'role': 'user', 'content': user_message}],
            }
            if system_prompt:
                kwargs['system'] = system_prompt
            resp = httpx.post(
                'https://api.anthropic.com/v1/messages',
                json=kwargs,
                headers={'x-api-key': api_key,
                         'anthropic-version': '2023-06-01',
                         'content-type': 'application/json'},
                timeout=timeout,
            )
            resp.raise_for_status()
            d = resp.json()
            return {
                'text': d['content'][0]['text'],
                'input_tokens': d['usage']['input_tokens'],
                'output_tokens': d['usage']['output_tokens'],
                'model': model,
            }
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f'anthropic call failed after 3 attempts: {last_err}')


def api_call_openai(api_key: str, model: str, prompt: str,
                    max_tokens: int = 8, temperature: float = 0.0,
                    timeout: int = 30) -> str:
    last_err = None
    for attempt in range(3):
        try:
            resp = httpx.post(
                'https://api.openai.com/v1/chat/completions',
                json={'model': model, 'max_completion_tokens': max_tokens,
                      'temperature': temperature,
                      'messages': [{'role': 'user', 'content': prompt}]},
                headers={'Authorization': f'Bearer {api_key}',
                         'Content-Type': 'application/json'},
                timeout=timeout,
            )
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f'openai call failed after 3 attempts: {last_err}')


# ---------------------------------------------------------------------------
# Spec variant construction
# ---------------------------------------------------------------------------

C2A_PREFIX = (
    'The following is a behavioral specification describing your user — '
    'how they think, decide, and act.\n\n'
    '=== BEHAVIORAL SPECIFICATION ===\n'
)


def build_system_prompt(spec_text: str) -> str:
    """Mirror run_global_rerun.build_system_prompt for C2a_full_spec.

    Both the Hamerton runner (run_full_spec_rerun.py) and the globals runner
    (run_global_rerun.py) use this exact prefix for C2a_full_spec; they are
    interoperable.
    """
    return C2A_PREFIX + spec_text


def build_filler_prompt(subject_display: str, target_chars: int) -> str:
    return (
        f'Write a single neutral biographical detail sentence about {subject_display}. '
        f'Target length approximately {target_chars} characters. '
        'No behavioral predicates, no claims about decisions or values, no '
        '"when X they Y" patterns, no "surfaces when..." patterns. '
        'Just one plain factual life detail (date, place, profession, family relation). '
        'Output ONLY the sentence itself with no preamble.'
    )


def build_reversal_prompt(predicate: str) -> str:
    return (
        'Rewrite the following behavioral predicate as its behavioral OPPOSITE. '
        'Preserve sentence structure and approximate length. Negate or invert '
        'the claim about how the person behaves. Keep the same kinds of '
        'connectives ("when", "they", etc.) so the sentence still reads like '
        'a behavioral predicate, only with the opposite content.\n\n'
        f'PREDICATE:\n{predicate}\n\n'
        'Output ONLY the reversed predicate sentence with no preamble.'
    )


def replace_sentence_in_spec(spec_text: str, target_sentence: str,
                              replacement: str | None) -> str:
    """Replace one sentence in spec_text with `replacement` (or remove if None).

    Uses literal substring replacement on the matched full sentence.
    """
    if target_sentence not in spec_text:
        raise RuntimeError(f'target sentence not found in spec: {target_sentence[:80]}...')
    if replacement is None:
        return spec_text.replace(target_sentence, '', 1)
    return spec_text.replace(target_sentence, replacement, 1)


# ---------------------------------------------------------------------------
# Judge helpers
# ---------------------------------------------------------------------------

def judge_prompt(held_out: str, response_text: str) -> str:
    return (
        'You are evaluating whether a response about a person PREDICTED '
        'what actually happened.\n\n'
        '=== HELD-OUT GROUND TRUTH ===\n' + held_out + '\n\n'
        '=== RESPONSE ===\n' + response_text[:1500] + '\n\n'
        'Rate 1-5:\n'
        '5=Predicts specific outcome\n'
        '4=General direction correct\n'
        '3=Right domain wrong outcome\n'
        '2=Wrong prediction\n'
        '1=Refuses or off-base\n\n'
        'Respond with ONLY a single digit (1-5).'
    )


def parse_score(text: str) -> int:
    if not text:
        return 0
    m = re.search(r'[1-5]', text.strip())
    return int(m.group()) if m else 0


def run_judge(judge_name: str, prompt: str, api_keys: dict) -> tuple[int, str, bool]:
    raw = ''
    try:
        if judge_name == 'haiku':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], HAIKU_JUDGE_MODEL,
                                   None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'sonnet':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], SONNET_JUDGE_MODEL,
                                   None, prompt, max_tokens=8, timeout=30)
            raw = r['text']
        elif judge_name == 'opus':
            r = api_call_anthropic(api_keys['ANTHROPIC_API_KEY'], OPUS_JUDGE_MODEL,
                                   None, prompt, max_tokens=8, timeout=60)
            raw = r['text']
        elif judge_name == 'gpt4o':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], GPT4O_MODEL, prompt)
        elif judge_name == 'gpt54':
            raw = api_call_openai(api_keys['OPENAI_API_KEY'], GPT54_MODEL, prompt)
        else:
            return 0, f'unknown judge: {judge_name}', True
    except Exception as e:
        return 0, str(e), True

    score = parse_score(raw)
    return score, raw, (score == 0)


# ---------------------------------------------------------------------------
# Main per-case runner
# ---------------------------------------------------------------------------

def panel_mean(scores_by_judge: dict) -> float | None:
    """Mean over per-judge scores. Require >= 3 valid (>0)."""
    valid = [s for s in scores_by_judge.values() if s and s > 0]
    if len(valid) < 3:
        return None
    return statistics.mean(valid)


def run_one_case(case: dict, api_keys: dict, checkpoint: dict) -> dict:
    """Run all three conditions on one case. Returns the per-case result dict.

    Updates checkpoint in place after each API call so an interrupt is recoverable.
    """
    subject = case['subject']
    qid = case['qid']
    case_key = f'{subject}__{qid}'
    held_out = case['held_out_passage']
    question_text = case['question_text']
    full_sentence = case['matched_full_sentence']
    spec_text = load_served_spec(subject)

    if not full_sentence:
        return {
            'case_key': case_key, 'error': 'no_full_sentence_match',
            'subject': subject, 'qid': qid,
        }
    if not spec_text:
        return {
            'case_key': case_key, 'error': 'no_spec_loaded',
            'subject': subject, 'qid': qid,
        }
    if full_sentence not in spec_text:
        return {
            'case_key': case_key, 'error': 'sentence_not_in_spec_after_match',
            'subject': subject, 'qid': qid,
        }

    rec = checkpoint.setdefault(case_key, {
        'case_key': case_key,
        'subject': subject,
        'qid': qid,
        'axis': case['axis'],
        'stratum': case['stratum'],
        'mechanism_category': case['mechanism_category'],
        'mechanism_confidence': case['mechanism_confidence'],
        'recorded_post_mean': case['recorded_post_mean'],
        'predicate_sentence': full_sentence,
        'predicate_sentence_chars': len(full_sentence),
        'question_text': question_text,
        'held_out_passage': held_out,
        'filler_text': None,
        'reversed_text': None,
        'responses': {},     # {variant: {text, input_tokens, output_tokens, model}}
        'judgments': {},     # {variant: {judge: score}}
        'panel_means': {},   # {variant: mean}
    })

    # Step 1: Sonnet generates the filler sentence (length-matched, neutral).
    if not rec.get('filler_text'):
        display = subject.replace('_', ' ').title()
        if subject == 'hamerton':
            display = 'Hamerton'
        elif subject == 'sunity_devee':
            display = 'Sunity Devee'
        elif subject == 'zitkala_sa':
            display = 'Zitkala-Sa'
        try:
            r = api_call_anthropic(
                api_keys['ANTHROPIC_API_KEY'], SONNET_MODEL, None,
                build_filler_prompt(display, len(full_sentence)),
                max_tokens=400, temperature=0.0, timeout=60,
            )
            rec['filler_text'] = r['text'].strip()
            log(f'    {case_key}: filler {len(rec["filler_text"])}c (target {len(full_sentence)})')
        except Exception as e:
            return {**rec, 'error': f'filler_generation_failed: {e}'}

    # Step 2: Sonnet generates the reversed predicate.
    if not rec.get('reversed_text'):
        try:
            r = api_call_anthropic(
                api_keys['ANTHROPIC_API_KEY'], SONNET_MODEL, None,
                build_reversal_prompt(full_sentence),
                max_tokens=600, temperature=0.0, timeout=60,
            )
            rec['reversed_text'] = r['text'].strip()
            log(f'    {case_key}: reversal {len(rec["reversed_text"])}c')
        except Exception as e:
            return {**rec, 'error': f'reversal_generation_failed: {e}'}

    # Step 3: Build the three spec variants.
    try:
        spec_original = spec_text
        spec_ablated = replace_sentence_in_spec(spec_text, full_sentence, rec['filler_text'])
        spec_reversed = replace_sentence_in_spec(spec_text, full_sentence, rec['reversed_text'])
    except Exception as e:
        return {**rec, 'error': f'spec_construction_failed: {e}'}

    variants = {
        'original': spec_original,
        'ablated': spec_ablated,
        'reversed': spec_reversed,
    }

    # Step 4: Generate Haiku response for each variant.
    for variant, spec_variant in variants.items():
        if rec['responses'].get(variant):
            continue
        sys_prompt = build_system_prompt(spec_variant)
        try:
            r = api_call_anthropic(
                api_keys['ANTHROPIC_API_KEY'], RESPONSE_MODEL,
                sys_prompt, question_text,
                max_tokens=1024, temperature=0.0, timeout=180,
            )
            rec['responses'][variant] = r
            log(f'    {case_key}/{variant}: response {r["output_tokens"]} out tokens')
            atomic_write_json(CHECKPOINT_PATH, checkpoint)
        except Exception as e:
            log(f'    {case_key}/{variant}: response FAILED: {e}')
            rec['responses'][variant] = {'error': str(e)}
            atomic_write_json(CHECKPOINT_PATH, checkpoint)

    # Step 5: Judge each response with the 5-judge primary panel.
    for variant in ('original', 'ablated', 'reversed'):
        resp = rec['responses'].get(variant) or {}
        if 'error' in resp or 'text' not in resp:
            continue
        rec.setdefault('judgments', {}).setdefault(variant, {})
        rec.setdefault('judgments_raw', {}).setdefault(variant, {})
        for judge in PRIMARY_JUDGES:
            if judge in rec['judgments'][variant]:
                continue
            score, raw, failed = run_judge(judge, judge_prompt(held_out, resp['text']), api_keys)
            rec['judgments'][variant][judge] = score
            rec['judgments_raw'][variant][judge] = raw[:80]
            atomic_write_json(CHECKPOINT_PATH, checkpoint)

    # Step 6: Compute panel means.
    for variant in ('original', 'ablated', 'reversed'):
        scores = rec.get('judgments', {}).get(variant, {})
        if scores:
            rec['panel_means'][variant] = panel_mean(scores)

    # Step 7: Per-case deltas.
    om = rec['panel_means'].get('original')
    am = rec['panel_means'].get('ablated')
    rm = rec['panel_means'].get('reversed')
    rec['delta_removal'] = (om - am) if (om is not None and am is not None) else None
    rec['delta_reversal'] = (om - rm) if (om is not None and rm is not None) else None
    rec['original_drift_from_recorded'] = (
        (om - case['recorded_post_mean']) if om is not None else None
    )
    atomic_write_json(CHECKPOINT_PATH, checkpoint)
    return rec


# ---------------------------------------------------------------------------
# Aggregation and report
# ---------------------------------------------------------------------------

def mean_or_none(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def stdev_or_none(xs):
    xs = [x for x in xs if x is not None]
    return statistics.stdev(xs) if len(xs) >= 2 else None


def ci95(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return (None, None)
    m = statistics.mean(xs)
    sd = statistics.stdev(xs)
    se = sd / (len(xs) ** 0.5)
    # Approx 1.96 * se for a 95% CI.
    return (m - 1.96 * se, m + 1.96 * se)


def decide_verdict(mean_removal: float | None) -> str:
    if mean_removal is None:
        return 'INSUFFICIENT_DATA'
    if mean_removal >= 1.0:
        return 'STRONG'
    if mean_removal >= 0.5:
        return 'CAUTIOUS'
    return 'NOT_SUPPORTED'


def aggregate_and_report(per_case: list[dict], sampling_record: dict) -> None:
    deltas_removal = [r.get('delta_removal') for r in per_case]
    deltas_reversal = [r.get('delta_reversal') for r in per_case]

    mean_removal = mean_or_none(deltas_removal)
    mean_reversal = mean_or_none(deltas_reversal)
    sd_removal = stdev_or_none(deltas_removal)
    sd_reversal = stdev_or_none(deltas_reversal)
    ci_removal = ci95(deltas_removal)
    ci_reversal = ci95(deltas_reversal)
    n_eval = sum(1 for d in deltas_removal if d is not None)

    verdict = decide_verdict(mean_removal)

    summary = {
        'date': datetime.now(timezone.utc).isoformat(),
        'sampling_record_path': str(SAMPLING_OUT.relative_to(REPO)),
        'verdict': verdict,
        'n_cases_with_complete_data': n_eval,
        'mean_delta_removal': mean_removal,
        'mean_delta_reversal': mean_reversal,
        'sd_delta_removal': sd_removal,
        'sd_delta_reversal': sd_reversal,
        'ci95_delta_removal': ci_removal,
        'ci95_delta_reversal': ci_reversal,
        'response_model': RESPONSE_MODEL,
        'panel': PRIMARY_JUDGES,
        'per_case': per_case,
    }
    atomic_write_json(RESULTS_JSON, summary)
    log(f'  Saved {RESULTS_JSON}')

    # Markdown report.
    lines = []
    lines.append(f'# Predicate Ablation Results - Phase 2c ({datetime.now().strftime("%Y-%m-%d")})')
    lines.append('')
    lines.append('Heuristic-rater proxy disconfirmation test: see script docstring.')
    lines.append('"Rater-identified causal predicate" = highest-token-overlap spec sentence per the deep_pattern_activation_analysis classifier; not a human rating.')
    lines.append('')
    lines.append(f'## Decision rule outcome: {verdict}')
    lines.append('')
    if mean_removal is not None:
        lines.append(f'- mean Delta_removal across N={n_eval}: {mean_removal:+.3f} anchor points')
    else:
        lines.append('- mean Delta_removal: insufficient data')
    if mean_reversal is not None:
        lines.append(f'- mean Delta_reversal across N={n_eval}: {mean_reversal:+.3f} anchor points')
    if sd_removal is not None:
        lines.append(f'- SD Delta_removal: {sd_removal:.3f}')
    if ci_removal[0] is not None:
        lines.append(f'- 95% CI Delta_removal: [{ci_removal[0]:+.3f}, {ci_removal[1]:+.3f}]')
    lines.append('')
    lines.append('### Decision thresholds')
    lines.append('- mean Delta_removal >= 1.0: STRONG predicate-mediated framing supported')
    lines.append('- 0.5 <= mean Delta_removal < 1.0: CAUTIOUS framing only')
    lines.append('- mean Delta_removal < 0.5: claim does NOT survive; rater-confabulation alternative is more parsimonious')
    lines.append('')

    lines.append('## Per-case results')
    lines.append('')
    lines.append('| Subject | qid | Axis | Mechanism | Original | Ablated | Reversed | dRemoval | dReversal | OrigDrift |')
    lines.append('|---|---:|---|---|---:|---:|---:|---:|---:|---:|')
    for r in per_case:
        om = r.get('panel_means', {}).get('original')
        am = r.get('panel_means', {}).get('ablated')
        rm = r.get('panel_means', {}).get('reversed')
        dr = r.get('delta_removal')
        drv = r.get('delta_reversal')
        drift = r.get('original_drift_from_recorded')
        def f(v):
            return f'{v:.2f}' if v is not None else '---'
        def fs(v):
            return f'{v:+.2f}' if v is not None else '---'
        lines.append(f'| {r["subject"]} | {r["qid"]} | {r["axis"]} | {r["mechanism_category"]} ({r["mechanism_confidence"]}) | {f(om)} | {f(am)} | {f(rm)} | {fs(dr)} | {fs(drv)} | {fs(drift)} |')
    lines.append('')

    # Cases where ablation worked vs didn't.
    worked = [r for r in per_case if r.get('delta_removal') is not None and r['delta_removal'] >= 1.0]
    weak = [r for r in per_case if r.get('delta_removal') is not None and r['delta_removal'] < 0.5]
    lines.append('## Cases where ablation produced >= 1 anchor drop (claim supported)')
    if worked:
        for r in worked:
            lines.append(f'- {r["subject"]} q{r["qid"]} ({r["axis"]}, {r["mechanism_category"]}/{r["mechanism_confidence"]}): dRemoval={r["delta_removal"]:+.2f}, dReversal={r["delta_reversal"]:+.2f}')
    else:
        lines.append('- (none)')
    lines.append('')
    lines.append('## Cases where ablation produced < 0.5 anchor drop (alternative explanation likely)')
    if weak:
        for r in weak:
            lines.append(f'- {r["subject"]} q{r["qid"]} ({r["axis"]}, {r["mechanism_category"]}/{r["mechanism_confidence"]}): dRemoval={r["delta_removal"]:+.2f}, dReversal={r["delta_reversal"]:+.2f}. Possible: latent world knowledge, generic persona enrichment effect, or wrongly-identified predicate.')
    else:
        lines.append('- (none)')
    lines.append('')

    lines.append('## Sanity check: original-condition reproduction drift')
    drifts = [r.get('original_drift_from_recorded') for r in per_case if r.get('original_drift_from_recorded') is not None]
    if drifts:
        big = [d for d in drifts if abs(d) > 1.0]
        lines.append(f'- N reproduced: {len(drifts)}')
        lines.append(f'- mean drift: {statistics.mean(drifts):+.3f}')
        lines.append(f'- max |drift|: {max(abs(d) for d in drifts):.3f}')
        lines.append(f'- cases with |drift| > 1.0: {len(big)} (model stochasticity confound, NOT a script bug)')
    else:
        lines.append('- (no drift data)')
    lines.append('')

    lines.append('## Verdict')
    if verdict == 'STRONG':
        lines.append('The strong predicate-mediated mechanism claim survives this disconfirmation test.')
    elif verdict == 'CAUTIOUS':
        lines.append('The strong claim does not survive in full. Cautious framing only: predicates do measurable work but smaller than 1 anchor on average.')
    elif verdict == 'NOT_SUPPORTED':
        lines.append('The strong claim does NOT survive. Rater-confabulation alternative is more parsimonious: removing the heuristically-identified causal predicate did not reduce performance, suggesting the lift was either generic-persona-enrichment, latent world knowledge, or that the heuristic mis-identified the true enabling content.')
    else:
        lines.append('Insufficient complete-data cases for a verdict.')
    lines.append('')
    lines.append('### What would tighten this further')
    lines.append('- Human rater identification of causal predicate (vs heuristic) on a subset')
    lines.append('- Larger N (e.g. all 47 PATTERN_PREDICATE cases coded and ablated)')
    lines.append('- Irrelevant-predicate control: matched-length but unrelated predicate, to test the "any rich persona text" alternative')
    lines.append('- Ablate two or more candidate predicates per case (the heuristic top-1 may not be the true driver)')
    lines.append('')

    RESULTS_MD.write_text('\n'.join(lines), encoding='utf-8')
    log(f'  Saved {RESULTS_MD}')


# ---------------------------------------------------------------------------
# Banner / smoke / main
# ---------------------------------------------------------------------------

BANNER = """
================================================================
 PREDICATE ABLATION EXPERIMENT - BUILT - NOT YET RUN
================================================================
This script is the Phase 2c disconfirmation test for the
pattern-predicate activation claim. It will spend API budget
when run with --go.

Estimated calls:
  16 cases * (1 filler + 1 reversal Sonnet) = 32
  16 cases * 3 spec variants * 1 Haiku response = 48
  16 cases * 3 spec variants * 5 judges = 240
  Total: ~320 API calls. Budget: under $5 (mostly Opus judge).

Smoke run (no --go) will:
  1. Load the pattern_activation_deep JSON
  2. Build the stratified sampling decision
  3. Match best_spec_sentence to full sentences in served specs
  4. Save sampling decision to docs/research/predicate_ablation_sampling_20260428.json
  5. Print the planned sampling and exit 0

Pass --go to actually run the experiment.
================================================================
"""


def smoke_run(target: int) -> dict:
    """Build sampling, save it, print plan, exit 0. Zero API calls."""
    log('SMOKE RUN starting (no API calls).')
    deep = load_json(DEEP_PATH)
    if not deep:
        log(f'  ERROR: {DEEP_PATH} not on disk yet. Sampling deferred to first --go run after deeper analysis lands.')
        return {'sampling_deferred': True, 'reason': 'deep_path_missing'}

    extreme_jumps = deep.get('extreme_jumps', [])
    log(f'  Loaded {len(extreme_jumps)} extreme jumps from deep analysis.')

    rng = random.Random(RNG_SEED)
    selected = sample_cases(extreme_jumps, target, rng)
    record = build_sampling_record(selected, extreme_jumps, target, RNG_SEED)
    atomic_write_json(SAMPLING_OUT, record)
    log(f'  Saved sampling decision to {SAMPLING_OUT}')

    log('')
    log(f'  Selected {record["selected_count"]} cases ({record["matched_count"]} matched to full sentence)')
    log(f'  Stratum counts: {record["stratum_counts"]}')
    log(f'  Subject distribution: {record["subject_distribution"]}')
    log(f'  Axis distribution: {record["axis_distribution"]}')
    if record['unmatched_count'] > 0:
        log(f'  WARNING: {record["unmatched_count"]} cases have no full-sentence match (these will fail under --go)')
        for u in record['unmatched']:
            log(f'    unmatched: {u}')
    log('')
    log('Sampling plan (subject/qid/axis/stratum/mechanism/conf/matched):')
    for c in record['selected']:
        flag = 'OK' if c['matched'] else 'NO_MATCH'
        log(f'  {flag:9s} {c["subject"]:>14}  q{c["qid"]:>3}  {c["axis"]:>22}  {c["stratum"]:>22}  {c["mechanism_category"]}/{c["mechanism_confidence"]}')
    log('')
    log('Smoke complete. Pass --go to run the experiment.')
    return record


def go_run(target: int, resume: bool, api_keys: dict) -> None:
    """Full experimental run. Requires API keys."""
    log('=== --go RUN START ===')

    # Load or rebuild the sampling record.
    if SAMPLING_OUT.exists() and resume:
        record = load_json(SAMPLING_OUT)
        log(f'  Resuming from existing sampling record: {SAMPLING_OUT}')
    else:
        deep = load_json(DEEP_PATH)
        if not deep:
            log(f'  ERROR: {DEEP_PATH} not on disk. Cannot run without it.')
            sys.exit(1)
        rng = random.Random(RNG_SEED)
        selected = sample_cases(deep.get('extreme_jumps', []), target, rng)
        record = build_sampling_record(selected, deep.get('extreme_jumps', []), target, RNG_SEED)
        atomic_write_json(SAMPLING_OUT, record)
        log(f'  Wrote sampling record: {SAMPLING_OUT}')

    selected = [c for c in record['selected'] if c['matched']]
    log(f'  Running {len(selected)} matched cases (skipping {record["selected_count"] - len(selected)} unmatched).')

    checkpoint = load_json(CHECKPOINT_PATH) or {}
    log(f'  Loaded checkpoint with {len(checkpoint)} prior case entries.')

    per_case_results = []
    for i, case in enumerate(selected, 1):
        log(f'\n  [{i}/{len(selected)}] {case["subject"]} q{case["qid"]} ({case["stratum"]})')
        try:
            rec = run_one_case(case, api_keys, checkpoint)
        except Exception as e:
            rec = {'case_key': f'{case["subject"]}__{case["qid"]}',
                   'error': f'unhandled_exception: {e}'}
            log(f'    UNHANDLED ERROR: {e}')
        per_case_results.append(rec)
        atomic_write_json(CHECKPOINT_PATH, checkpoint)

    # Aggregate and write report.
    aggregate_and_report(per_case_results, record)
    log('=== --go RUN COMPLETE ===')


def main() -> None:
    parser = argparse.ArgumentParser(description='Predicate Ablation Experiment (Phase 2c)')
    parser.add_argument('--go', action='store_true', help='Actually run the experiment (default: smoke only)')
    parser.add_argument('--target', type=int, default=DEFAULT_TARGET, help='Target number of cases (default 16, range 12-20)')
    parser.add_argument('--resume', action='store_true', help='Reuse the existing sampling JSON instead of rebuilding')
    args = parser.parse_args()

    if args.target < 12 or args.target > 24:
        log(f'  WARNING: --target {args.target} outside recommended 12-20 range; proceeding anyway.')

    print(BANNER)

    if not args.go:
        smoke_run(args.target)
        return

    api_keys = load_api_keys()
    missing = [k for k in ('ANTHROPIC_API_KEY', 'OPENAI_API_KEY') if k not in api_keys]
    if missing:
        log(f'  ERROR: missing API keys: {missing}. Set Windows User env vars and retry.')
        sys.exit(1)

    go_run(args.target, args.resume, api_keys)


if __name__ == '__main__':
    main()
