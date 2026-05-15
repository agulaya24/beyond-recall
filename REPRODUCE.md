# Reproducing the Beyond Recall v12.1 Headline Numbers

This document is the canonical reproduction path for the v12.1 paper. v12.1 is the current canonical draft at `docs/beyond_recall_v12_1_draft.md` (2026-05-13); the numerical claims it makes can be regenerated locally with the scripts and data committed to this repository.

> **Note:** v12.1's headline numbers (slope, R², Wilcoxon, low-baseline mean Δ_C4a, all-14 mean Δ_C4a, wrong-spec deltas, memory-system deltas, Letta n=3) are carried forward unchanged from v10.1, so the reproduction commands below produce the same numerical outputs they did under v10.1 / v11. The script names retain the `_v10_` prefix as frozen artifact identifiers; they reproduce the v12.1 §4.1 numbers. v11 added content (per-question variance, two statistical signatures, predicate ablation, half-anchor metric, held-out leakage rare, Hamerton spec-length confound) registered in the 2026-04-28 data-locking pass; per-claim confidence catalog at `docs/research/v11_confidence_catalog_20260428.md`. **v12.1 standardized the §4.2 compression Δs to the symmetric 9-row computation** (Spec Only Δ +0.68, raw corpus Δ +0.91, All Facts + Spec Δ +0.89; compression-recovery figure 75%); the recompute is documented at `docs/reviews/v12_1_compression_table_recompute_20260513.md`. v12.1 also corrected the 3-anchor crossing rate (5.9% → 5.7%, 20/351) and added a Krippendorff α footnote disclosing a third-party recompute of 0.668 alongside the 0.659 headline. None of these changes affect the §4.1 gradient reproduction commands below. The v10.1 draft at `docs/beyond_recall_v10_1_draft.md` is preserved as historical baseline.

The aim is to make the reasoning behind the v12.1 §4.1 gradient checkable from a clean checkout. Every script listed here runs from committed data; no API calls are required for the core sensitivity analyses.

---

## 1. Environment

Python 3.12 is the version the analysis was developed against. Earlier 3.10+ should also work for the pure-numerical scripts.

```bash
python -m venv .venv
source .venv/bin/activate            # macOS/Linux
# .\.venv\Scripts\Activate.ps1       # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` lower bounds are conservative. If you only need the sensitivity scripts (no API calls, no embeddings), `numpy + pandas + scipy + statsmodels` is enough.

### 1.1. Install the bundled Base Layer pipeline (only needed for API-dependent paths)

The Base Layer pipeline source at the version cited by the paper is bundled in this repository at `./baselayer/` (frozen at v0.2.0). It is only needed for the API-calling reproductions in §3.3 and §4 below; the §2 sensitivity analyses run from committed data and do not require it.

```bash
pip install -e ./baselayer
```

This installs the `baselayer` Python package in editable mode and puts the `baselayer` CLI and `baselayer-mcp` server on your PATH. The bundled copy is independent of the active Base Layer development at https://github.com/agulaya24/BaseLayer; it is pinned here so the reproduction path stays stable as Base Layer evolves. See `baselayer/VENDORED_README.md` for details.

---

## 2. Reproduce the §4.1 sensitivity analyses (no API calls required)

The two §4.1 sensitivity scripts are self-contained: per-subject (C5, Δ_C4a) data is inlined from the v10.1 §4.1 table (carried forward unchanged into v11 §4.1), and they output the numbers cited in the paper.

### 2.1. Battery-composition sensitivity (v11 §4.1; v10.1 §4.1 line 749)

```bash
python scripts/_v10_battery_sensitivity.py
```

Reproduces:

- Univariate gradient slope: **−0.96 [95% CI −1.24, −0.67]**, R² = 0.82, p < 0.001
- Multiple regression on C5 + LITERAL_RECALL fraction: partial slope on baseline = **−0.88 [95% CI −1.13, −0.63]**, p < 10⁻⁵; partial coefficient on LITERAL_RECALL fraction β = +2.30 [+0.34, +4.26], p = 0.026; adjusted R² = 0.87
- Drop-Hamerton subset (all 14 main-study batteries are Haiku-generated; this subset isolates Hamerton's legacy battery, NOT a generator family): slope = **−0.89 [95% CI −1.18, −0.61]**, R² = 0.81, p < 10⁻⁴. The legacy "GPT-5.4-battery subset" wording was incorrect; corrected in v10.1 release-freeze pass 3 and carried into v11.
- Per-subject input frame is printed; manually checkable against the v11 §4.1 table (and the equivalent v10.1 §4.1 table at `docs/beyond_recall_v10_1_draft.md` lines 720-737).

Full report: `docs/research/v10_battery_sensitivity_analysis.md`.

### 2.2. Coupling-free reframing (v11 §4.1; v10.1 §4.1 line 755)

```bash
python scripts/_v10_coupling_sensitivity.py
```

Reproduces:

- Level regression C4a ~ C5: slope = **+0.04 [95% CI −0.25, +0.33]**, R² = 0.008, p = 0.76; mean C4a = **2.46**
- Permutation null on Δ-on-C5 slope (10,000 iterations): centered at −0.998 (SD 0.127); two-sided p = 0.77 against observed −0.960
- Subject-level bootstrap (10,000 iterations): Δ-on-C5 slope CI = [−1.254, −0.740]; level slope CI = [−0.254, +0.260]
- Saves `docs/research/v10_coupling_sensitivity_arrays.npz` for downstream inspection (per-subject frame + bootstrap distributions).

Full report: `docs/research/v10_coupling_sensitivity_analysis.md`.

### 2.3. Random-seed determinism

The coupling script seeds NumPy at `RNG_SEED = 20260424` and runs 10,000 permutations and 10,000 subject-level bootstraps. Output is bit-identical across runs on the same Python + NumPy version. The battery script has no randomness.

---

## 3. Higher-cost recomputes (require API access or large local data)

These are not required to verify the v10.1 headline numbers but reproduce the underlying judgments.

### 3.1. 5-judge primary aggregate over per-judge files

```bash
python scripts/recompute_5judge_primary.py
```

Reads per-judge JSON judgment files under `results/global_<subject>/` and `results/hamerton/`. Aggregates within-judge then across the 5 primary judges (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4). No API calls; runs from committed data.

### 3.2. Memory-system 5-judge primary

```bash
python scripts/compute_memory_systems_5judge.py
```

Same input file family, scoped to `C1_<system>` and `C3_<system>` rows.

### 3.3. End-to-end response generation (API-dependent)

API-calling scripts are out of scope for the canonical v12.1 reproduction path because they cost money and depend on provider availability. Where you need them, the entry points are:

- `scripts/run_full_study.py` (Hamerton)
- `scripts/run_global_subjects.py` (13 globals)
- `scripts/run_global_rerun.py` (memory-system reruns; canonical wrong-spec v1 pairing in WRONG_SPEC_PAIRING constant lines 51-60)
- `scripts/run_multimodel_responses.py` (Tier 2 cross-provider directional probe; 2 response models = Sonnet 4.6 and Gemini 2.5 Pro on 3 subjects, GPT-5.4-generated batteries; Opus + GPT-5.4 in Tier 2 are judges, not response models)

These depend on API keys (Anthropic, OpenAI, Mistral, Cerebras, Groq, Google) and on subject-corpus directories outside this repo (`hamerton_memory/`, `franklin_clean_memory/`, etc., maintained in the upstream `memory_system/` repository).

---

## 4. Letta stateful-agent rerun (v11 §4.5; carried forward from v10.1 §4.5)

The Letta stateful-agent case study is exploratory at n=3 (Hamerton, Ebers, Babur). Pipeline scripts and committed artifacts:

- Main matched-rerun: `docs/research/_letta_rerun/`
  - Pipeline: `20_run_c2a_named.py`, `40_judge_responses.py`, `50_aggregate.py`, `70_compute_5judge_primary.py`
  - Output: `5judge_primary_results.json`
- Full-stack BL rerun (v11 §4.5 footnote): `docs/research/_letta_rerun/fullstack_named/`
  - Pipeline: `fs_01_make_specs.py`, `fs_03_run_responses.py`, `fs_04_judge.py`, `fs_05_aggregate.py`
  - Output: `5judge_fullstack_results.json`, `RESULTS.md`
- Raw Letta `human` memory blocks (Hamerton, Ebers, Babur): `docs/research/_letta_blocks/`
  - Includes `paired_scores.json` and `compute_paired.py` for the §4.5 paired analysis.
- Summary report: `docs/research/letta_stateful_matched_rerun.md`

Running the pipeline requires `letta-client` (not in `requirements.txt` because no committed script imports it directly), API access to a Letta server, and the source corpora.

---

## 5. Hardcoded-path inventory

A subset of scripts was developed against an absolute Windows path and will need manual edits or environment variables before they run from a fresh clone on a different machine. These scripts all live under `scripts/`, and the prefix that needs replacement is `C:/Users/Aarik/Anthropic/...`.

### 5.1. Scripts that run portably (no path edits required)

The following analysis scripts use only relative paths (`Path(__file__).parent.parent / ...`) and run cleanly from any clone:

- `scripts/_v10_battery_sensitivity.py`
- `scripts/_v10_coupling_sensitivity.py`
- `scripts/recompute_5judge_primary.py`
- `scripts/compute_memory_systems_5judge.py`
- `scripts/classify_hedging.py` and the other `classify_*.py` analysis scripts
- `scripts/compute_anchor_crossing.py`, `scripts/compute_hedging_rates.py`, `scripts/compute_spec_activation.py`, `scripts/compute_spec_similarity.py`
- `scripts/compute_wrong_spec_5judge.py`, `scripts/compute_wrong_spec_per_subject.py`
- `scripts/build_review_html.py`, `scripts/build_v8.py` (mostly relative)
- The full numbered chain under `docs/research/_letta_rerun/` and `docs/research/_letta_rerun/fullstack_named/`

### 5.2. Scripts with hardcoded paths

Approximately 42 scripts under `scripts/` reference `C:/Users/Aarik/Anthropic/...` paths. Most are one-off probes (`scripts/_probe_*.py`, `scripts/_check_*.py`) that sit outside the canonical reproduction path. The exceptions worth flagging:

- `scripts/run_multimodel_responses.py`: points at `hamerton_memory/` and `franklin_clean_memory/` directories outside this repository (in the upstream `memory_system/` workspace)
- `scripts/run_franklin_judge.py`: points at upstream Franklin corpora
- `scripts/sync_to_study_repo.py`: points at upstream `memory_system/` repo

To make these portable, the recommended future change is a single `BASELAYER_REPO_ROOT` environment variable that scripts consult before falling back to a default. Until that lands, treat these scripts as archival API-rerun infrastructure.

### 5.3. Probe / check scripts (transient)

The `scripts/_probe_*.py`, `scripts/_check_*.py`, and `scripts/_diag_*.py` families are session-specific scratch. They are kept for provenance but are not on the canonical reproduction path. Do not depend on them.

---

## 6. Where the v12.1 numbers come from

v12.1 carries the v10.1 §4.1 / §4.2 / §4.3 / §4.4 / §4.5 headline numbers forward unchanged. v11-specific additions (per-question variance, two statistical signatures, half-anchor metric, predicate ablation null, held-out leakage rare, Hamerton spec-length confound, pattern-activation heuristic falsified) are registered in DATA_REFERENCE.md, KEY_FINDINGS.md (M15-M21), and PROVENANCE_INDEX.md from the 2026-04-28 data-locking pass. v12.1 standardized the §4.2 compression Δs to the symmetric 9-row computation (recompute at `docs/reviews/v12_1_compression_table_recompute_20260513.md`) and corrected the 3-anchor crossing rate to 5.7% (20/351).

| Number | Where to look |
|---|---|
| §4.1 per-subject (C5, C2a, C4a, Δ) table | `docs/DATA_REFERENCE.md` §1 (5-judge primary); raw at `results/global_<subject>/judgments_v2.json` and `results/hamerton/{sonnet,opus,gpt4o,haiku,gpt54}_judgments.json` |
| §4.1 headline slope, R², p-value | `scripts/_v10_battery_sensitivity.py` (univariate) and `scripts/_v10_coupling_sensitivity.py` (level + permutation + bootstrap). Script names retain `_v10_` prefix as frozen artifact identifiers; they reproduce the v11 §4.1 numbers (unchanged from v10.1). |
| §4.1 sensitivity (LITERAL_RECALL, drop-Hamerton subset) | `scripts/_v10_battery_sensitivity.py` |
| §4.2 compression curve (Hamerton) | `results/hamerton/c8_c9_judgments_*.json` plus per-judge files |
| §4.5 Letta stateful-agent case study | `docs/research/_letta_rerun/5judge_primary_results.json` (matched), `docs/research/_letta_rerun/fullstack_named/5judge_fullstack_results.json` (full-stack BL rerun), `docs/research/letta_stateful_matched_rerun.md` (summary) |
| §3.6 (v11) / §3.7 (v10.1) judge calibration | `results/judge_calibration/*.json` |
| Wrong-spec controls (§4.3; elevated in v11 §4.6.4) | `results/_wrong_spec_v2/`, `scripts/compute_wrong_spec_5judge.py`, `scripts/classify_wrong_spec_detection.py` |
| v11 per-question variance + anchor crossings | `docs/research/wins_inventory_20260428.json`, `docs/research/within_band_shifts_20260428.{json,md}` |
| v11 predicate ablation (Phase 2c) | `docs/research/predicate_ablation_results_20260428.{json,md}` |
| v11 confidence catalog (per-claim source of truth) | `docs/research/v11_confidence_catalog_20260428.md` |

The single source of truth for every number is `docs/DATA_REFERENCE.md`. The v12.1 paper draft is the canonical narrative; where the two disagree, the paper wins.

---

## 6.5. Pre-flight checks before any judge rerun

Before running any large-batch judging script, run the two validation scripts under `scripts/_v11_validation/`. They were added on 2026-04-25 in response to the GPT-5.4 batch-failure incident; both are required gates per `_ARCHITECTURE.md` §11.

### 6.5.1. Judge-panel health probe

```bash
python scripts/_v11_validation/preflight_judge_health.py
```

Sends one canonical 1-to-5 rubric prompt to each model in the panel (haiku, sonnet, opus, gpt4o, gpt54, gemini_flash, gemini_pro) and asserts a numeric score in [1, 5] within timeout. Exit 1 if any required judge fails. Pass `--require-gemini` to make Gemini failures gate as well; default treats them as sensitivity (non-blocking).

### 6.5.2. Panel-completeness audit

```bash
python scripts/_v11_validation/check_panel_completeness.py
```

Scans every `results/**/*judgments*.json` file under the repo and emits `docs/research/v11_panel_completeness_audit.csv` with per-(file, condition, judge) parse-failure rates classified as `CLEAN`, `SUSPECT` (>5%), or `FULL_FAIL` (~100%). Exit 1 if any unwaived non-CLEAN cell exists. Known-resolved batches (such as the §4.3 wrong_spec_v2 originals preserved as evidence after the rerun) live in `docs/research/v11_panel_completeness_waivers.json`.

### 6.5.3. Use the shared judge-call utility

New judging code MUST import from `scripts/_judge_invocation/`:

```python
from _judge_invocation import call_judge, JudgeAPIError

result = call_judge(
    "openai", "gpt-5.4",
    system="", user=prompt,
    max_output_tokens=10, temperature=0.0,
    run_id="my_batch_id",
)
```

The dispatcher selects `max_completion_tokens` automatically for any OpenAI model id prefixed with `gpt-5`, `o1`, or `o3`. Every call appends a JSONL record to `logs/judge_calls/<date>_<run_id>.jsonl` (model, prompt SHA-256, response, success/fail, parameters used). See `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md` for the historical bug and `docs/reviews/v11_judge_call_controls_implementation_20260425.md` for the controls implementation.

---

## 7. Notes on what is NOT reproducible offline

- **Provider memory-system reruns** (Mem0, Letta archival, Supermemory, Zep) require API keys and SDKs not pinned in `requirements.txt`.
- **Cross-LLM paper review scripts** (`scripts/_run_v9_groq_review.py`, `scripts/gate_review_v8.py`, etc.) call Groq, Mistral, Cerebras, Gemini via raw HTTP; provider keys are read from Windows user environment variables (see the `get_win_env` helper inside each script).
- **Word document export** (`docs/beyond_recall_v12_1_draft.docx` if present, or `docs/beyond_recall_v10_1_draft.docx` for the historical baseline) requires `pypandoc` plus a Pandoc binary on PATH.

If you are reproducing the v12.1 §4.1 result from a fresh clone for a paper-review reason, sections 1, 2, and 5 of this document are sufficient. The rest is provenance.
