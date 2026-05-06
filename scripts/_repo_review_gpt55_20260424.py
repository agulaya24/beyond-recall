"""
Beyond Recall — Repo-level Review by GPT-5.x (2026-04-24).

Sends a structured summary of the memory-study-repo (NOT the paper) to OpenAI
GPT-5.5 (with fallbacks: gpt-5.4, gpt-5, gpt-4o) and asks the model to produce
a public-release readiness review of the repository.

Output: docs/reviews/v10_repo_review_gpt55_20260424.md
"""
import os
import sys
import json
import time
import subprocess
import datetime
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path('C:/Users/Aarik/Anthropic/memory-study-repo')
REVIEWS_DIR = REPO_ROOT / 'docs' / 'reviews'
OUT_PATH = REVIEWS_DIR / 'v10_repo_review_gpt55_20260424.md'


def get_win_env(key: str) -> str:
    r = subprocess.run(
        ['powershell', '-Command',
         f'[System.Environment]::GetEnvironmentVariable("{key}","User")'],
        capture_output=True, text=True
    )
    return r.stdout.strip()


# -----------------------------------------------------------------------------
# Repo summary — built from the survey done in this session.
# -----------------------------------------------------------------------------

REPO_SUMMARY = r"""
# REPO SUMMARY: memory-study-repo (companion repo for Beyond Recall paper)

## 1. High-level state

- **Active paper draft:** `docs/beyond_recall_v10_draft.md` (2,379 lines).
- **Older drafts retained:** v6 (in `docs/versions/`), v7, v8, v9 (in `docs/`).
  Each version has `.md`, `.clean.md`, and `.docx` siblings.
- **License:** Apache 2.0 (`LICENSE` at root, README confirms).
- **Citation:** `CITATION.cff` present.
- **Repo size:** root + agents/ + charts/ + data/ + docs/ + figures/ + results/ + scripts/ + workspace/.

## 2. Top-level layout

```
memory-study-repo/
├── README.md            (14,559 bytes — main entry)
├── ISSUES.md            (P0/P1/P2 tracker, "GREEN" status)
├── AGENTS.md            (10,928 bytes — agent entry doc)
├── CITATION.cff
├── LICENSE              (Apache 2.0)
├── .gitignore
├── agents/
│   ├── study-guide.md   (agent navigation)
│   └── STUDY_MEMORY.md  (study memory)
├── charts/
├── data/
│   ├── README.md
│   ├── hamerton/         (primary subject — battery, facts, spec/)
│   ├── franklin/
│   ├── franklin_obscure/
│   └── global_subjects/  (13 directories: augustine, babur, bernal_diaz, cellini,
│                          ebers, equiano, fukuzawa, keckley, rousseau, seacole,
│                          sunity_devee, yung_wing, zitkala_sa) — each has
│                          battery.json, facts.json, spec_production.md,
│                          anchors_v4.md, core_v4.md, predictions_v4.md, etc.
├── docs/
│   ├── ANALYSIS_PLAN_LOCK.md
│   ├── DATA_REFERENCE.md            ("single source of truth")
│   ├── KEY_FINDINGS.md
│   ├── PROVENANCE_INDEX.md
│   ├── METHODOLOGY.md
│   ├── PAPER_CORRECTIONS.md
│   ├── FILE_NAMING.md
│   ├── PROVIDER_EXPERIENCE_LEDGER.md
│   ├── PROVIDER_ISSUES.md
│   ├── REFERENCE_TABLE.md
│   ├── README.md
│   ├── _pandoc_default_reference.docx, _reference_arxiv_11pt.docx
│   ├── _results_snapshot.txt
│   ├── beyond_recall_v8_draft.{md,clean.md,docx}
│   ├── beyond_recall_v9_draft.{md,clean.md,docx}
│   ├── beyond_recall_v10_draft.{md,clean.md,docx}
│   ├── blog_post_v2.md
│   ├── internal/           (private; not summarized here)
│   ├── research/           (~50 .md + .json files: paired analyses, hedging,
│   │                        spec activation, Letta stateful, etc.;
│   │                        includes _letta_blocks/ and _letta_rerun/ subdirs
│   │                        which hold the Letta stateful-agent test artifacts)
│   ├── reviews/            (~40 review-round artifacts incl. s114 audits,
│   │                        full_paper_gate_review_20260422_173703.md,
│   │                        repo_completeness_audit_20260422_173831.md,
│   │                        s114_repo_quality_audit.md,
│   │                        v9_final_review_cerebras_qwen3_20260424.md,
│   │                        v9_final_review_gemini_pro_20260424.md)
│   └── versions/           (frozen earlier drafts incl. v6)
├── figures/                 (16 figure .pngs + 4 .pdfs +
│                             generate_figures*.py x3 + README)
├── results/
│   ├── README.md
│   ├── RESULTS_S113.json    (consolidated S113 results)
│   ├── _s114_backfills/
│   ├── _tier2/
│   ├── _wrong_spec_v2/
│   ├── franklin/, franklin_legacy_20260411/, franklin_obscure/
│   ├── hamerton/            (~112 files: judgments per condition x judge,
│   │                          baselayer, c8_c9, fullstack_haiku, letta /
│   │                          mem0 / supermemory / zep
│   │                          ingestion, retrieval, results, judgments,
│   │                          fullpipeline_* variants)
│   ├── global_<subject>/     (13 dirs, each ~40-50 files matching the
│   │                          per-subject pattern: battery.json,
│   │                          battery_gpt54.json, facts.json, judgments.json,
│   │                          baselayer/letta/mem0/supermemory/zep
│   │                          judgments per judge, c8_c9 conditions,
│   │                          fullpipeline_*; multimodel responses live in
│   │                          `multimodel/` for Hamerton)
│   ├── judge_calibration/
│   ├── multimodel/          (sonnet_hamerton.json, gpt54_hamerton.json,
│   │                          gemini_hamerton.json, README — Hamerton-only)
│   └── per-system manifest/analysis JSONs at the top level
│       (mem0_manifest.json, mem0_analysis.json, etc.)
├── scripts/                 (145 .py files, plus README.md describing
│                              reproducibility per-script)
└── workspace/               (study_knowledge.db + study_vectors/ — local index)
```

## 3. Key documents and what they say

### 3.1 README.md
- Title and abstract framing: "Base Layer is not a memory system. Layered on top of four commercial ones, it improves all four on the users the model doesn't already know."
- Header banner says: "Active paper draft: `docs/beyond_recall_v9_draft.md`. v8 preserved as reference baseline."
- Repository-structure block in the same README later says: "beyond_recall_v8_draft.md  # Current research paper draft (§1–§8 complete)"
- README does NOT mention v10 anywhere. `docs/beyond_recall_v10_draft.md` exists but is not referenced from README.
- Reproducibility section claims temp=0, SHA-256 corpus checksums, manifests, pre-committed analysis plan.
- Subjects table lists 14 subjects with C5 baselines from 1.03 (Sunity Devee) to 2.93 (Equiano).
- Header section reports gradient slope **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001 on 5-judge primary panel; n=14; 9-of-9 low-baseline; Wilcoxon W=11, p=0.007.

### 3.2 ISSUES.md
- Banner: "Overall health: GREEN. All P0 items resolved as of 2026-04-23."
- P0 RESOLVED list includes: missing reproducibility script `_audit_with_c2c.py` (now restored),
  `License pending` -> Apache 2.0, broken §4.3.1 reference -> §4.5, v9 TOC §6/§8 numbering gap,
  KEY_FINDINGS Spearman ρ correction.
- P1 items still open (5):
  - B5: v8 body still says ρ = 0.89-0.98 in 3 places (v9 corrected to 0.86-0.93).
  - B6: DATA_REFERENCE.md has stale §-references (§7, §4.3.1, §4.8) that don't match v9 numbering.
  - B7: KEY_FINDINGS.md has 13 stale paper-location citations pinned to v6/v8 numbering.
  - B8: PROVENANCE_INDEX.md general v6→v8→v9 body remap mostly undone.
  - B10: docs/README.md points at v8 as "the one to edit"; active editing is v9.
  - B11: docs/research/ (17 files) still v8-anchored.
  - C2: agents/STUDY_MEMORY.md references `scripts/run_letta_stateful_test.py` and `scripts/run_letta_memory_as_context.py` that DO NOT EXIST.
    Actual Letta pipeline is at `docs/research/_letta_rerun/NN_*.py`.
  - C3: agents/study-guide.md:62 points at `docs/beyond_recall_v6_draft.md` (moved to versions/).
  - C4: 42 scripts hardcode `C:/Users/Aarik/...` Windows paths; `run_multimodel_responses.py`
    points at `hamerton_memory/` and `franklin_clean_memory/` dirs OUTSIDE this repo;
    fresh-clone reproduction fails.
- P2 hygiene: stray LaTeX .aux file, Word ~$temp files, empty `scripts/results/global_cellini/`,
  `scripts/__pycache__/` committed, 31 transient `_probe_*.py`/`_check_*.py` scripts, etc.
- Critical: ISSUES.md does not mention v10 at all. The v10 draft was checked in
  but the issue tracker does not yet reflect v10 as the active editing target.

### 3.3 AGENTS.md
- Header says: "Current state (S114, 2026-04-21). Working draft: `docs/beyond_recall_v8_draft.md`."
- Lists v8 as canonical, v7 as superseded, v6 as frozen reference. Does NOT mention v9 or v10.
- "5-judge primary panel changed from 7-judge" decision is captured.
- Several "Read these BEFORE working" pointers reference v8.

### 3.4 agents/study-guide.md
- Says: "current paper draft: `docs/beyond_recall_v9_draft.md` (edit this; v8 and v6 are preserved baselines)".
- Updated more recently than AGENTS.md. Conflicts with AGENTS.md and with README's structure block.
- Does NOT mention v10.

### 3.5 docs/DATA_REFERENCE.md (declared "single source of truth")
- Top header: "Generated 2026-04-18 from results/RESULTS_S113.json (refreshed this session)."
- Claims: "any discrepancy between this document and the paper draft should be resolved in favor of this document."
- §1 gradient table shows the 7-judge S113 numbers (C5 baseline values, e.g. Hamerton C5=1.25, sunity_devee=1.03).
- §2 statistical tests block reports gradient slope **−0.98 [95% CI −1.30, −0.74]** — this is the 7-judge value.
- The v10 paper headline reports slope **−0.96 [95% CI −1.24, −0.67]** — the 5-judge primary value.
- DATA_REFERENCE has a footer note that paper-location anchors were re-synced to v9 on 2026-04-23 but the slope was NOT recomputed in DATA_REFERENCE.
- §K "Provenance" includes a row pointing to `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json`.
  **THIS DIRECTORY DOES NOT EXIST IN THE REPO.** Verified: the parent results/ contains hamerton/, global_*, franklin/, etc., but no `run_fullstack_*` directory.
- The actual Letta stateful files are at:
  `docs/research/_letta_blocks/babur_human_block.txt`, `ebers_human_block.txt`
  `docs/research/_letta_rerun/01_inspect_stateful.py`, ..., `60_rerun_gpt54_letta.py`,
  `5judge_primary_results.json`.

### 3.6 docs/KEY_FINDINGS.md
- Header v9 revision note (2026-04-23) flags the slope and Spearman corrections.
- M1 still reports slope as **−0.98 [95% CI −1.30, −0.74]** — same stale 7-judge value as DATA_REFERENCE.
- v10's value of −0.96 is not reflected in KEY_FINDINGS M1.

### 3.7 docs/PROVENANCE_INDEX.md
- "S113 corrections" header is v8/v9-anchored.
- §4.3.1 row points to "Letta stateful-agent test ... block 22,472 chars; matched-model 3.24 vs C2a 3.04 at 65% context." Source path implied via DATA_REFERENCE §K (broken).
- Various `paper location §X line Y` anchors not yet re-synced to v9 (per ISSUES B8).

### 3.8 docs/research/v10_battery_sensitivity_analysis.md (new this session)
- Documents the v10 §4.1 sensitivity analysis (multiple regression + subset regression).
- Lists per-subject C5 and Δ_C4a values that DIFFER from DATA_REFERENCE §1 by small amounts
  (e.g. Hamerton: DATA_REFERENCE C5 = 1.25, v10 sensitivity table C5 = 1.26;
   Sunity Devee Δ_C4a: DATA_REFERENCE +1.57 vs v10 +1.38).
  This is consistent with 7-judge -> 5-judge primary recompute, but DATA_REFERENCE has not been updated.
- Reports headline reproduces univariate slope = −0.960 [−1.245, −0.675], R² = 0.818, p = 9.1e-6.
- Multiple regression: partial coefficient on C5 stays at −0.880 [−1.127, −0.633] when LITERAL_RECALL fraction is added.
- Subset regression (drop Hamerton legacy battery, n=13): slope still significantly negative.
- Output goes to docs/research/ — there is no link from README, KEY_FINDINGS, or DATA_REFERENCE pointing at the new analysis.

### 3.9 scripts/ (145 Python files)
- `scripts/README.md` lists per-script `Runs standalone? / External paths? / Windows-only?` honestly.
- Most runner scripts are flagged "Windows-only" because they read API keys from
  the user's Windows environment via PowerShell. macOS/Linux instructions are
  provided in the README but not in the scripts themselves.
- Scripts like `run_franklin_judge.py`, `run_multimodel_responses.py`, `sync_to_study_repo.py` rely on
  paths in Aarik's main workspace `C:/Users/Aarik/Anthropic/memory_system/...` —
  documented as "No: depends on data outside this repo."
- New scripts this session: `_v10_battery_sensitivity.py` (clean, no external paths;
  only requires numpy/pandas/statsmodels/scipy and embeds its data inline).
  `review_v10_gpt55.py` (sends v10 paper to OpenAI for review).
- 31 leading-underscore `_probe_*.py` / `_check_*.py` scripts described as "transient"
  but not yet pruned.
- No `requirements.txt` or `pyproject.toml` found at repo root.
  Only references to Python deps are inline in script docstrings (numpy, pandas,
  statsmodels, scipy, mem0ai, letta-client, supermemory, zep-cloud, anthropic, openai, httpx, etc.)

## 4. Reproducibility audit

### 4.1 What CAN be reproduced from the repo
- `_v10_battery_sensitivity.py` is fully self-contained (data inlined). Reproduces v10 §4.1 sensitivity headline.
- `run_baselayer_condition.py` is the lightest cross-platform path to one subject end-to-end (per scripts/README).
- `_audit_with_c2c.py` reproduces D.3.4 (r=0.500, n=312) and D.3.5 (2,087 chars, n=795)
  per `docs/reviews/_p0_c1_closure_report.md`.
- `recompute_5judge_primary.py` exists and is the canonical 5-judge recompute runner.
- All raw judgments are present at `results/<subject>/<system>_judgments_{judge}.json` with
  per-judge breakdown.

### 4.2 What CANNOT be reproduced cold
- `RESULTS_S113.json` consolidation: the script that built it is unclear.
- `letta_stateful_test_result.json` and the rest of the `run_fullstack_hamerton_20260411_231237/`
  directory referenced by DATA_REFERENCE §K do not exist in the repo. Letta stateful artifacts
  are scattered across `docs/research/_letta_blocks/` (text blocks for Babur and Ebers — but no
  Hamerton block file at that path) and `docs/research/_letta_rerun/` (numbered scripts and
  one summary results JSON).
- Any external researcher cloning fresh will hit hardcoded `C:/Users/Aarik/...` paths in 42 scripts.

### 4.3 Sample paper-claim trace (six v10 claims)

| v10 claim | File and status |
|---|---|
| Gradient slope −0.96 [95% CI −1.24, −0.67], N=14, 5-judge primary | Headline value in v10 §4.1 line 684. Reproduced internally by `_v10_battery_sensitivity.py` (univariate). DATA_REFERENCE.md still reports the old 7-judge slope −0.98. |
| 9 of 9 low-baseline subjects improve with spec | Per-subject Δ_C4a at v10 §4.1 lines 727-741. DATA_REFERENCE §1 also lists 9-of-9 but with 7-judge numbers. Underlying judgments exist at `results/global_<subject>/baselayer_judgments_*.json` and `results/hamerton/`; can be recomputed by `recompute_5judge_primary.py`. |
| Wrong-spec content specificity, 60.6% detection rate | v10 §1.3 + §4.3. Source: `scripts/classify_wrong_spec_detection.py` -> `docs/research/wrong_spec_detection_analysis.md`, `docs/research/wrong_spec_detection_raw.json`. Validation sample in `docs/research/wrong_spec_validation_sample.json`. Traceable. |
| Supermemory near-zero aggregate is a mixture | v10 §4.4. Source: `docs/research/supermemory_c1_vs_c3_paired_analysis.md` + `docs/research/supermemory_7judge_aggregate.md`. The paid-tier rerun n=14 numbers are documented at `docs/research/p0_2_supermemory_paid_tier_rerun.md`. Underlying per-question scores at `results/global_<subj>/supermemory_*.json`. Traceable. |
| Letta stateful-agent N=3 exploratory case study (Hamerton +0.20, Ebers +0.75, Babur +0.29) | v10 §4.5. Source: `docs/research/letta_stateful_matched_rerun.md`, `docs/research/letta_stateful_deep_read.md`, `docs/research/_letta_blocks/`, `docs/research/_letta_rerun/`. **DATA_REFERENCE §K and PROVENANCE_INDEX both point to a `results/run_fullstack_hamerton_20260411_231237/` directory that does not exist** — broken trace. |
| Battery sensitivity (multiple regression on LITERAL_fraction; subset regression dropping Hamerton) | New v10 §4.1 block. Source: `scripts/_v10_battery_sensitivity.py` (script self-contained, runs cleanly). Report: `docs/research/v10_battery_sensitivity_analysis.md`. Traceable. |

### 4.4 Documentation coherence

The five canonical orientation docs do not agree on which paper draft is canonical:

| Document | Says canonical draft is |
|---|---|
| `README.md` (header) | v9 |
| `README.md` (structure block) | v8 ("§1-§8 complete") |
| `AGENTS.md` | v8 |
| `agents/study-guide.md` | v9 |
| `agents/STUDY_MEMORY.md` | v8 (per ISSUES C2) |
| `ISSUES.md` | silent on v10 |
| `docs/beyond_recall_v10_draft.md` | exists, is the active draft |

The actual editing target this session is v10. None of the orientation docs say so.

### 4.5 Number consistency

| Metric | DATA_REFERENCE.md | KEY_FINDINGS.md | v10 paper draft |
|---|---|---|---|
| Gradient slope | −0.98 [−1.30, −0.74] | −0.98 [−1.30, −0.74] | **−0.96** [−1.24, −0.67] |
| 9-of-9 low-baseline mean Δ | +1.04 (facts+spec) | +1.04 | **+0.89** (Δ_C4a, 5-judge primary) |
| Hamerton C5 baseline | 1.25 | 1.25 (M1 evidence) | **1.26** (in v10 §4.1 sensitivity block) |
| Sunity Devee Δ_C4a | +1.57 | +1.57 | +1.38 (5-judge) |

DATA_REFERENCE explicitly claims to be the "single source of truth" and to "win" any discrepancy with the paper. As written, this would force the paper to roll back to old 7-judge numbers — opposite of the intent. The intent is that the 5-judge primary recompute supersedes; the documents have not been updated to reflect that.

## 5. Public-release risk indicators

### 5.1 Things a reviewer will hit immediately

1. README points at v9 in one place and v8 in another. v10 — the actual active draft — is invisible.
2. ISSUES.md banner says GREEN but does not list the v10 update. A reviewer will assume v10 is unverified.
3. DATA_REFERENCE numbers don't match the paper, despite the doc's "source of truth" claim. Looks like a numerical inconsistency at first glance.
4. `_v10_battery_sensitivity.py` is undocumented in any orientation file. A reviewer searching for "battery sensitivity" via the searchable index will find the analysis but not the recommendation that this is the canonical sensitivity check.

### 5.2 Things a reviewer would fail to find

1. The Letta stateful-agent test source data, because DATA_REFERENCE points at a missing directory.
2. The v10 acceptance criteria — what is "done" for this revision is undocumented.
3. A `requirements.txt` / `pyproject.toml` / `environment.yml` at root.

### 5.3 Things that look like bad hygiene

1. 31 transient `_probe_*.py` / `_check_*.py` scripts at scripts/ top level.
2. `scripts/__pycache__/` committed.
3. Empty `scripts/results/global_cellini/` directory.
4. Word .docx temp files (`docs/~$yond_recall_v8_draft.docx`, `docs/~WRL2113.tmp`).
5. `docs/beyond_recall_test.aux` LaTeX build artifact.
6. Per ISSUES B12: 271 occurrences of "substrate" terminology used informally as a synonym for "memory system".

## 6. Open questions for review

- Is the README banner-vs-structure-block inconsistency damaging at first read?
- Is the v10 absence from ISSUES.md / AGENTS.md / README.md a launch-blocker?
- Is the DATA_REFERENCE v8/v9 number / v10 paper number split a credibility risk, given that DATA_REFERENCE explicitly calls itself the "source of truth"?
- Is the `letta_stateful_test_result.json` broken trace a launch-blocker?
- Are 145 scripts (with 42 hardcoded Windows paths and no requirements file) an acceptable companion-repo state for a public release alongside arXiv?
- What single most-impactful change would you recommend before public-visible commit?

# END REPO SUMMARY
"""


REVIEW_PROMPT = """You are an experienced reviewer for an open-science repository accompanying an empirical AI research paper. Below is a structured summary of the memory-study-repo, which accompanies the Beyond Recall paper. Produce a review.

## Verdict
One of: CRITICAL_FIXES_REQUIRED / NEEDS_REVISION / READY_WITH_MINOR_FIXES / READY_FOR_PUBLIC. One-sentence justification.

## Highest-impact single improvement
The ONE thing that would most improve the repo's reception. Be specific.

## Critical issues
Anything that would embarrass the project or block reproduction. Cite file paths.

## Reproducibility audit
Can a third party reproduce the headline numbers from raw data + scripts? If not, what's the gap?

## Documentation audit
Are README.md, ISSUES.md, AGENTS.md, STUDY_MEMORY.md, study-guide.md, DATA_REFERENCE.md, KEY_FINDINGS.md, PROVENANCE_INDEX.md telling a coherent story? Do they conflict?

## Code-quality and hygiene
Any obvious code-quality issues, missing dependencies, hardcoded paths, missing requirements.txt, etc.

## Comparison to expected open-science norms
For an arXiv-companion repo at this scale (~120 subjects' worth of artifacts, ~14 main-study subjects, multi-LLM evaluation pipeline), what would a strong reviewer expect that this repo doesn't yet have?

## Risks for public release
What's the worst that could happen when this repo goes public? What should the author check before pushing the public-visible commit?

Be direct. If the repo is ready, say so. If it would be embarrassing to release, say so.

REPO SUMMARY:

{summary}
"""


def call_openai(api_key: str, model_id: str, prompt: str,
                max_tokens: int = 8192, timeout: int = 600):
    url = 'https://api.openai.com/v1/chat/completions'
    body = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_completion_tokens': max_tokens,
    }
    if model_id.startswith('gpt-4'):
        body['temperature'] = 0.3
        body.pop('max_completion_tokens')
        body['max_tokens'] = max_tokens

    payload = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'python-requests/2.31.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data['choices'][0]['message']['content']
            usage = data.get('usage', {})
            return text, None, {'model': data.get('model'), 'usage': usage}
    except urllib.error.HTTPError as e:
        body_text = ''
        try:
            body_text = e.read().decode()[:500]
        except Exception:
            pass
        return None, f'HTTP {e.code}: {body_text}', None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}', None


def main():
    print('Loading API key...')
    api_key = get_win_env('OPENAI_API_KEY')
    if not api_key:
        print('ERROR: OPENAI_API_KEY not found in user env')
        sys.exit(1)
    print(f'API key loaded ({len(api_key)} chars)')

    prompt = REVIEW_PROMPT.format(summary=REPO_SUMMARY)
    print(f'Full prompt: {len(prompt)} chars, ~{len(prompt)//4} tokens')

    candidates = ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']
    chosen_model = None
    text = None
    meta = None
    last_error = None
    attempt_log = []

    for model_id in candidates:
        print(f'\nTrying model: {model_id}')
        for attempt in range(2):
            t0 = time.time()
            text_try, err, meta_try = call_openai(
                api_key, model_id, prompt, max_tokens=8192, timeout=600
            )
            elapsed = time.time() - t0
            if text_try:
                wc = len(text_try.split())
                print(f'  SUCCESS in {elapsed:.1f}s ({len(text_try)} chars, {wc} words)')
                attempt_log.append({
                    'model': model_id, 'attempt': attempt + 1,
                    'elapsed_s': round(elapsed, 1), 'words': wc, 'ok': True,
                })
                if wc < 800:
                    print(f'  WARNING: response only {wc} words (<800), retrying once...')
                    if attempt == 0:
                        time.sleep(5)
                        continue
                    else:
                        print('  Still under 800 words after retry. Will try next model.')
                        last_error = f'short_response_{wc}_words'
                        break
                text = text_try
                meta = meta_try
                chosen_model = (meta_try.get('model') if meta_try else None) or model_id
                break
            else:
                print(f'  FAIL ({elapsed:.1f}s): {err}')
                attempt_log.append({
                    'model': model_id, 'attempt': attempt + 1,
                    'elapsed_s': round(elapsed, 1), 'error': err,
                })
                last_error = err
                if attempt == 0:
                    print('  retrying in 10s...')
                    time.sleep(10)
        if text:
            break

    if not text:
        print(f'\nALL MODELS FAILED. Last error: {last_error}')
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(
            (
                f'# v10 Repo Review — FAILED\n\n'
                f'All candidate models failed.\nLast error: {last_error}\n\n'
                f'Attempt log:\n```json\n{json.dumps(attempt_log, indent=2)}\n```\n'
            ),
            encoding='utf-8',
        )
        sys.exit(1)

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = (
        f'# Beyond Recall v10 Repo Review — GPT-5.x\n\n'
        f'**Generated:** {ts}\n'
        f'**Model requested chain:** {candidates}\n'
        f'**Model actually used (API response):** `{chosen_model}`\n'
        f'**Prompt length:** {len(prompt):,} chars (~{len(prompt)//4:,} tokens)\n'
        f'**Usage:** {json.dumps((meta or {}).get("usage", {}))}\n'
        f'**Response length:** {len(text)} chars, {len(text.split())} words\n\n'
        f'**Attempt log:**\n```json\n{json.dumps(attempt_log, indent=2)}\n```\n\n'
        f'---\n\n'
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(header + text, encoding='utf-8')
    print(f'\nSaved review: {OUT_PATH}')
    print(f'Model used: {chosen_model}')
    print(f'Words: {len(text.split())}')


if __name__ == '__main__':
    main()
