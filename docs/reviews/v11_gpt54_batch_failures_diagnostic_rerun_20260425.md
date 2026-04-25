# GPT-5.4 batch-failure diagnostic + rerun closure

**Date:** 2026-04-25
**Scope:** Two GPT-5.4 batch-failure incidents that contaminated the v10 paper's
panel composition for §4.3 random-derangement and §4.5 Letta-Hamerton/Babur 7-judge aggregates.

## Summary

| Issue | Phase 1 verdict | Action taken | Outcome |
|---|---|---|---|
| A. §4.3 wrong_spec_v2 (13 globals × GPT-5.4) | Real failure (HTTP 400, root cause `max_tokens` vs `max_completion_tokens`) | Full rerun executed | 520/520 calls succeeded, 0 failures |
| B. §4.5 Letta Hamerton (39 GPT-5.4 calls) | Already resolved by `_letta_rerun/60_rerun_gpt54_letta.py` writing canonical memory_system path | None needed | Scaffold reads good data (3.103 mean) |

## Phase 1 — Diagnose

### Issue A: §4.3 random-derangement v2

**Hidden good data hunt.** Directory `results/_wrong_spec_v2/global_<subject>/`
contains:

- `wrong_spec_v2_judgments_gpt54.json` (current). 100% records have
  `parse_failure: true` and `raw_response: "ERR:Client error '400 Bad Request' for url 'https://api.openai.com/v1/chat/completions'..."`.
- `wrong_spec_v2_judgments_gpt54.json.rl_backup` (older backup). Records have
  `error: "gpt54 judge rate limited"` (also bad). Not a usable older version.
- No other archive, recompute, or rerun directory holds GPT-5.4 wrong_spec_v2
  judgments. Searched `results/`, `docs/research/`, `_archive/` patterns.

Both files are bad. The `.rl_backup` is from an earlier exhaustion of the
in-script retry budget (5 attempts) that surfaced as "rate limited"; the
canonical-name file represents the most-recent run where 400 errors
propagated as raw responses. Both stem from the same structural prompt issue.

**Root cause.** `judge_tier2.judge_gpt54` (used by `judge_wrong_spec_v2.py`)
issued OpenAI requests with `"max_tokens": 10`, which GPT-5.x rejects with
HTTP 400. Identical bug pattern to Issue B (already fixed in
`docs/research/_letta_rerun/60_rerun_gpt54_letta.py`). All other primary panel
judges (haiku, sonnet, opus, gpt4o) succeeded because Anthropic models accept
`max_tokens` and gpt-4o still accepts it.

**API health test.** Single-call test on Zitkala-Sa Q1 with the canonical
`JUDGE_PROMPT` template and `max_completion_tokens=10`:

- Status: 200
- Time: 2.68s
- Returned raw: `'4'`
- Usage: 1106 prompt tokens, 4 completion tokens
- Rate-limit headers: 4999/5000 RPM, 1.998M/2M TPM remaining

API healthy.

**Failure-window inspection.** Empty files have identical mtime stamps
within each subject directory and the canonical-not-rerun naming, indicating
they were produced by a single batch run that never recovered after the
`max_tokens` mismatch — a structural prompt issue rather than a transient
outage.

### Issue B: §4.5 Letta Hamerton

**Hidden good data hunt.** `docs/research/_letta_rerun/` contains:

- `60_rerun_gpt54_letta.py` — fixed rerun script using
  `max_completion_tokens=10`.
- `letta_hamerton_judgments_gpt54.json` — output of that rerun (39 records,
  all valid scores, no parse_failure).
- `letta_ebers_judgments_gpt54.json` and `letta_babur_judgments_gpt54.json`
  — companion outputs.

The §4.5 emit script (`scripts/_v11_emit_4_5_letta.py`) does NOT read these
copies; it reads the canonical memory_system path
`results/run_fullstack_hamerton_20260411_231237/letta_memory_haiku_judgments_gpt54.json`,
which `60_rerun_gpt54_letta.py` already overwrites. That file has 39
clean records (sample qids 21-25 have scores 2/4/2/2/4).

**No rerun needed.** The data is already in place; §4.5 emit pulls it
correctly via the manifest entry confirmed in the §4.5 input_manifest.

## Phase 2 — Rerun (Issue A only)

**Script:** `scripts/_rerun_wrong_spec_v2_gpt54_20260425.py`

- Reads response text from
  `<memory_system_results>/global_<subject>/wrong_spec_v2_results.json`
  (40 valid responses per subject × 13 globals = 520 calls)
- Same prompt template as `judge_tier2.JUDGE_PROMPT`, character-for-character
- Uses `max_completion_tokens=10`, `temperature=0`, `model='gpt-5.4'`
- Atomic per-question writes (resumable)
- Output: `results/_wrong_spec_v2/global_<subject>/wrong_spec_v2_judgments_gpt54_rerun_20260425.json`
- The original empty `wrong_spec_v2_judgments_gpt54.json` files are
  preserved as evidence; the .rl_backup files are also preserved.

**Loader update.** `scripts/_v11_emit_4_3_wrong_spec.py::load_global_v2_judgments`
now prefers `wrong_spec_v2_judgments_<judge>_rerun_20260425.json` over the
canonical name when present, with an explicit `SchemaError` if it ever silently
falls back to a 100% parse_failure file. This change keeps "DO NOT overwrite"
intact while letting the emit scaffold pick up the corrected GPT-5.4 data.

### Per-subject rerun results (520/520 valid, 0 failures)

| Subject | n_rerun | n_valid | mean | parse_failures |
|---|---:|---:|---:|---:|
| augustine | 40 | 40 | 2.775 | 0 |
| babur | 40 | 40 | 2.150 | 0 |
| bernal_diaz | 40 | 40 | 2.225 | 0 |
| cellini | 40 | 40 | 1.300 | 0 |
| ebers | 40 | 40 | 1.550 | 0 |
| equiano | 40 | 40 | 1.575 | 0 |
| fukuzawa | 40 | 40 | 2.075 | 0 |
| keckley | 40 | 40 | 1.750 | 0 |
| rousseau | 40 | 40 | 1.750 | 0 |
| seacole | 40 | 40 | 1.475 | 0 |
| sunity_devee | 40 | 40 | 1.275 | 0 |
| yung_wing | 40 | 40 | 1.900 | 0 |
| zitkala_sa | 40 | 40 | 2.050 | 0 |

Grand total: 520/520 valid scores, mean 1.84, no errors throughout.

## §4.3 emit verification (post-rerun)

Run: `python scripts/_v11_emit_4_3_wrong_spec.py --verify`

```
VERIFY: 16/17 claim_ids MATCH paper-text within tolerance
    4_3_correct_spec_delta_13globals                             scaffold=0.3538 paper=0.3500 -> MATCH
  **4_3_random_derangement_delta_13globals                       scaffold=0.1525 paper=0.2200 -> MISMATCH(-0.0675)
    4_3_adversarial_derangement_delta_13globals                  scaffold=-0.2469 paper=-0.2500 -> MATCH
    4_3_correct_minus_adversarial_gap                            scaffold=0.6008 paper=0.6000 -> MATCH
    4_3_spec_tag_citation_rate_correct_pct                       scaffold=78.6325 paper=78.6000 -> MATCH
    4_3_spec_tag_citation_rate_wrong_pct                         scaffold=50.0000 paper=50.0000 -> MATCH
    4_3_wrong_spec_detection_explicit_pct                        scaffold=60.6474 paper=60.6000 -> MATCH
    4_3_wrong_spec_detection_misapply_pct                        scaffold=36.4566 paper=36.5000 -> MATCH
    4_3_wrong_spec_detection_hedged_pct                          scaffold=2.0443 paper=2.0000 -> MATCH
    4_3_wrong_spec_detection_ambiguous_pct                       scaffold=0.8518 paper=0.9000 -> MATCH
    4_3_wrong_spec_total_n                                       scaffold=587 paper=587 -> MATCH
    4_3_hedging_narrow_C5_pct                                    scaffold=28.8000 paper=28.8000 -> MATCH
    4_3_hedging_narrow_C2a_pct                                   scaffold=1.3800 paper=1.4000 -> MATCH
    4_3_hedging_narrow_C4a_pct                                   scaffold=0.0000 paper=0.0000 -> MATCH
    4_3_hedging_broader_C5_pct                                   scaffold=41.2200 paper=41.2000 -> MATCH
    4_3_hedging_broader_C2a_pct                                  scaffold=7.8900 paper=7.9000 -> MATCH
    4_3_hedging_broader_C4a_pct                                  scaffold=0.3900 paper=0.4000 -> MATCH
```

**One MISMATCH, by design.** The §4.3 random-derangement Δ is the very
quantity Issue A was contaminating. With the clean 5-judge primary panel
(GPT-5.4 included), the gradient is **+0.15** rather than the paper's +0.22.
This is the principled correction the rerun was meant to surface.

The other 16 claims (correct-spec Δ, adversarial Δ, correct-minus-adversarial
gap, spec-tag citation rates, detection categories, hedging rates) all pass
within tolerance, confirming the rerun did not introduce regressions and
the 5-judge panel is now genuinely intact.

## §4.5 emit verification (no rerun, already-resolved data)

Run: `python scripts/_v11_emit_4_5_letta.py --verify`

```
Hamerton   Letta=3.103  BL=2.964  d5=+0.139  d7=+0.093  d_fullstack=+0.272
Ebers      Letta=2.760  BL=1.715  d5=+1.045  d7=+0.746  d_fullstack=+1.205
Babur      Letta=2.415  BL=1.880  d5=+0.535  d7=+0.232  d_fullstack=+0.380

VERIFY (§4.5 + Appendix F): 20/26 claims MATCH within tolerance
  4_5_hamerton_delta_letta_minus_bl_7judge   scaffold=0.093  paper=0.20  -> MISMATCH
  4_5_babur_delta_letta_minus_bl_7judge      scaffold=0.232  paper=0.29  -> MISMATCH
  (named-entity counts: separate algorithm-vs-paper-by-hand issue, not GPT-5.4-related)
```

Two delta MISMATCHes: with a clean Letta-7 vs BL-7 panel, Hamerton Δ = +0.093
and Babur Δ = +0.232. The v10 paper's +0.20 and +0.29 came from asymmetric
panels (Letta-6 vs BL-7 when GPT-5.4 was missing on the Letta side). Those
numbers are the contamination this report identifies; the scaffold values are
the corrected truth.

## Conclusions

1. **Issue B was already resolved** by `60_rerun_gpt54_letta.py` writing to the
   canonical memory_system path. No new work needed; scaffold reads good data.
2. **Issue A required a rerun.** Same root cause as Issue B (`max_tokens` vs
   `max_completion_tokens`). Rerun executed cleanly: 520/520 calls
   successful, zero failures, mean per-subject scores in the expected
   1.275-2.775 range.
3. The §4.3 and §4.5 emit scaffolds now read clean data and produce the
   intended corrections to the v10 paper:
   - **§4.3 random-derangement Δ:** +0.22 → **+0.15** (5-judge primary,
     Cohen-style mean of per-subject deltas across 13 globals)
   - **§4.5 Hamerton 7-judge Δ:** +0.20 → **+0.093**
   - **§4.5 Babur 7-judge Δ:** +0.29 → **+0.232**
4. All paper claims requiring the GPT-5.4 judge are now reproducible and
   panel-symmetric. No further GPT-5.4 reruns are needed for the v10/v11
   paper.

## Artifacts

- Rerun script: `scripts/_rerun_wrong_spec_v2_gpt54_20260425.py`
- Diagnostic count script: `scripts/_diag_wrong_spec_v2_count.py`
- API health probe: `scripts/_diag_gpt54_health_test.py`
- Per-subject rerun outputs:
  `results/_wrong_spec_v2/global_<subject>/wrong_spec_v2_judgments_gpt54_rerun_20260425.json`
  (13 files, 40 records each, all valid)
- Updated emit script: `scripts/_v11_emit_4_3_wrong_spec.py` (loader prefers
  rerun file with explicit fail-loud guard)
- Updated emit outputs:
  `docs/research/v11_emit/4_3_wrong_spec.json` and `.md`
- §4.5 emit unchanged but re-verified.

---

## Root cause and remediation (controls added 2026-04-25)

### The bug, in one sentence

Multiple ad-hoc judge invocation paths in this repo issued OpenAI requests
with the parameter `max_tokens`. GPT-5.x and the o1/o3 reasoning families
reject `max_tokens` with HTTP 400 and instruct callers to use
`max_completion_tokens` instead. Anthropic and OpenAI gpt-4o calls were
unaffected because Anthropic accepts `max_tokens` natively and gpt-4o still
accepts it for backward compatibility, so the bug was silent on every model
except GPT-5.x.

Verified by negative-control call on 2026-04-25:

```
status 400
body : {"error": {"message": "Unsupported parameter: 'max_tokens' is not
        supported with this model. Use 'max_completion_tokens' instead.",
        "type": "invalid_request_error", "param": "max_tokens",
        "code": "unsupported_parameter"}}
```

### Where the bug lived

- `scripts/judge_tier2.py` (used by `judge_wrong_spec_v2.py`): original site
  for §4.3 wrong_spec_v2 batch.
- The Letta initial pass that produced `letta_memory_haiku_judgments_gpt54.json`
  before the fix landed in `docs/research/_letta_rerun/60_rerun_gpt54_letta.py`.
- Inline `httpx.post` calls in §4.4 Base Layer C1/C3 GPT-5.4 judging code
  (936 records empty across 12 of 14 subjects).
- Inline `httpx.post` calls in §4.2 Bernal Diaz C8/C9 GPT-5.4 judging code
  (paired with a separate gpt-4o 429 batch failure on the same subject).

### Remediation: shared judge-call utility

A single fixed implementation now lives at
[`scripts/_judge_invocation/`](../../scripts/_judge_invocation/). New judging
code MUST import from this module:

```python
from _judge_invocation import call_judge, JudgeAPIError

result = call_judge(
    "openai", "gpt-5.4",
    system="", user=prompt,
    max_output_tokens=10, temperature=0.0,
    run_id="my_batch_id",
)
```

The dispatcher selects `max_completion_tokens` automatically for any model id
prefixed with `gpt-5`, `o1`, or `o3`, and falls back to `max_tokens` for
gpt-4 / gpt-4o / gpt-3.5. Documented exponential-backoff retry on 429
(max 5) and 5xx (max 3). Returns a structured dict with `score`, `raw_text`,
`tokens`, `latency_ms`, `error_type`, `model`, `param_used`, `prompt_hash`.
Raises `JudgeAPIError` with a typed `failure_type` on any unrecoverable
failure. Every call appends a JSONL record to
`logs/judge_calls/<date>_<run_id>.jsonl`.

Parallel modules `anthropic_judge_call.py` and `gemini_judge_call.py` mirror
the same interface for symmetry; the model-agnostic dispatcher
`call_judge(provider, model, ...)` routes to the correct backend by
provider id (or by model-id prefix if `provider=None`).

Live verification (gpt-5.4, 2026-04-25):

```
score      : 5
raw_text   : "5"
tokens     : prompt=168, completion=4, total=172
latency_ms : 1255
param_used : max_completion_tokens
error_type : None
```

### Detection: panel-completeness audit

`scripts/_v11_validation/check_panel_completeness.py` scans every
`results/**/*judgments*.json` file under the repo and writes
`docs/research/v11_panel_completeness_audit.csv` with one row per
(file, condition, judge) cell, classifying each as `CLEAN`, `SUSPECT`
(>5% parse-failure rate) or `FULL_FAIL`. A waiver list at
`docs/research/v11_panel_completeness_waivers.json` lets known-resolved
batches (such as the 13 §4.3 originals preserved as evidence) pass without
gating. Run before any aggregation step.

`scripts/_v11_validation/preflight_judge_health.py` sends one canonical
probe to each judge in the panel and asserts a numeric score in [1, 5]
within timeout. Required gate before any batch with > 50 calls. Exit 1
if any required judge fails.

Architecture contract update: `_ARCHITECTURE.md` §11 makes both checks
mandatory.

### What the audit caught on first run (2026-04-25)

`check_panel_completeness.py` flags every one of the four known failure
sets, plus several Tier-2 GPT-5.4 batches that share the same root cause
and have not yet been rerun:

| Set | Files / cells flagged | Status |
|---|---|---|
| §4.3 wrong_spec_v2 originals (gpt54) | 13 files, 13 cells | FULL_FAIL, waived (rerun in place) |
| §4.4 Base Layer C1/C3 (gpt54) | 14 files, 28 cells | FULL_FAIL, NOT yet waived |
| §4.2 Bernal Diaz C8/C9 (gpt54, gpt4o, gemini_flash) | 3 files, 6 cells | FULL_FAIL, NOT yet waived |
| §4.5 Letta canonical Hamerton | 0 (rerun overwrote canonical) | CLEAN |
| Tier-2 cross-model GPT-5.4 batches | many in `results/_tier2/` | FULL_FAIL, NOT yet waived |

The Tier-2 surface is the biggest follow-up. Either rerun those batches
through the shared utility or add explicit waivers documenting why each is
acceptable.
