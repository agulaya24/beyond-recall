# V11 Emit Architecture

Goal: **no alternate undocumented path by which paper numbers can enter the manuscript.** Every reported number in the Beyond Recall paper is produced by a named, idempotent scaffold script that reads primary data only, with documented aggregation rules, schema validation, and a manifest-based provenance trail.

This doc is the contract every `_v11_emit_*.py` scaffold script must satisfy.

## 1. Locked aggregation rule

The primary-panel aggregation rule (used everywhere unless explicitly noted):

1. Read raw per-judge per-question scores from primary data (judgment JSON files).
2. Filter to 5-judge primary panel: `{haiku, sonnet, opus, gpt4o, gpt54}` (case as stored in JSON).
3. Per-judge per-subject mean = mean of per-question scores within subject.
4. Panel mean per-subject per-condition = mean of per-judge means across the 5 panel members.
5. Cross-subject aggregates (gradient slope, Wilcoxon, etc.) operate on per-subject panel means.

The 7-judge panel (adding `gemini_flash` and `gemini_pro`) is reported as a sensitivity check only, never as a primary aggregate.

## 2. Required structure for every `_v11_emit_*.py` script

```python
"""
Emit script for <SECTION> of the Beyond Recall paper.

Aggregation rule: 5-judge primary (per-judge per-question -> per-judge per-subject mean -> panel mean).
Outputs: docs/research/v11_emit/<section>.json + docs/research/v11_emit/<section>.md
Verification: python <script> --verify  (compares emitted values to current paper text)
"""
```

Every script:
1. **Declares its primary-data inputs** by absolute repo-relative path.
2. **Computes content checksums** (SHA-256) of every input file at run time. Checksums are written into the output JSON's `provenance.input_manifest` block.
3. **Validates schema** on every input judgment file: each record must contain `question_id` (int), `condition` (string), `judge` (string in known set), `score` (numeric in 1-5). Any record missing these fields raises a clear schema error and aborts.
4. **Applies the locked aggregation rule** identically to every claim.
5. **Names every emitted number with a stable claim_id** (e.g., `4_1_slope`, `4_4_1_mem0_low_baseline_delta`). Claim ids are flat strings; no nested keys.
6. **Records per-number provenance**: `{value, inputs, filters, aggregation_rule, contrast, script_version, run_timestamp}`.
7. **Writes outputs atomically** (temp file + rename).
8. **Is idempotent**: running twice on unchanged data produces byte-identical JSON.
9. **Emits a markdown view** for human readers, with a side-by-side comparison column to current paper text (MATCH / MISMATCH(<delta>)).

## 3. Output JSON schema

```json
{
  "schema_version": "v11.0",
  "section": "§4.1",
  "aggregation_rule": "5-judge primary; per-judge per-question -> per-judge per-subject mean -> panel mean across {haiku, sonnet, opus, gpt4o, gpt54}",
  "claims": {
    "<claim_id>": {
      "value": <number>,
      "estimand": "<plain-English description of what is being measured>",
      "contrast": "<e.g., 'C4a vs C5'>",
      "filters": {"panel": [...], "condition": [...], "subjects": [...]},
      "n": <integer>,
      "ci95_low": <number_or_null>,
      "ci95_high": <number_or_null>,
      "p_value": <number_or_null>
    },
    ...
  },
  "provenance": {
    "script": "scripts/_v11_emit_<section>.py",
    "script_version": "<git sha or hand-set version>",
    "run_timestamp": "2026-04-25T...",
    "input_manifest": [
      {"path": "results/global_ebers/judgments_v2.json", "sha256": "<hex>", "size_bytes": <int>, "n_records": <int>},
      ...
    ]
  }
}
```

## 4. Required `--verify` flag behavior

`python scripts/_v11_emit_<section>.py --verify`:
1. Runs the emit.
2. For each claim_id in the JSON, locates the matching number in `docs/beyond_recall_v10_1_draft.md` (or v11 when active) by string match or section anchor.
3. Prints a per-claim diff table: `claim_id | scaffold_value | paper_value | status`.
4. Status is `MATCH` if `|scaffold_value − paper_value| < 0.005`, else `MISMATCH(<delta>)`.
5. Exit code 0 if all match, 1 otherwise.

## 5. Schema-validation rules per primary-data file

All judgment files (path pattern `results/**/*judgments*.json`) MUST satisfy:
- Top-level: list of records, OR dict with `judgments` key holding a list.
- Each record: required keys `question_id`, `condition`, `judge`, `score`.
- `score` is numeric in [1.0, 5.0].
- `condition` is in the documented condition set: `{C5_baseline, C2a_full_spec, C2c_wrong_spec, C4_factdump, C4a_full_facts_plus_spec, C8, C9, C1_<system>, C3_<system>, C4_<system>, C4a_<system>, ...}`.
- `judge` is in `{haiku, sonnet, opus, gpt4o, gpt54, gemini_flash, gemini_pro}`.

Schema violations abort with a named error referencing the file and the failing record.

## 6. CI drift test

Add `pytest scripts/_v11_emit/test_drift.py` that:
1. For each `_v11_emit_*.py` script, runs the script.
2. Compares scaffold output JSON to a frozen golden snapshot.
3. Fails if any value drifts by more than 0.005 against golden.
4. Goldens are regenerated only by an explicit `--regenerate-golden` flag, with a commit message documenting why.

## 7. Locked condition naming

The canonical condition string set (as stored in primary-data JSON):

| Canonical | Meaning |
|---|---|
| `C5_baseline` | No-context baseline (response model, no spec, no facts) |
| `C2a_full_spec` | Spec only (full layered) |
| `C2c_wrong_spec` | Adversarial wrong-spec control (fixed-pairing v1, max cultural+temporal distance; the −0.25 condition) |
| `C2c_wrong_spec_v2` | Random-derangement wrong-spec control (seed-fixed permutation; the +0.22 condition) |
| `C4_factdump` | All facts as context, no spec |
| `C4a_full_facts_plus_spec` | Facts + spec |
| `C8` | Full raw corpus as context, no spec |
| `C9` | Raw corpus + spec |
| `C1_<system>` | Memory system retrieval only (controlled config) |
| `C3_<system>` | Memory system retrieval + spec (controlled config) |
| `C1_<system>_fp` | Native (full-pipeline) config retrieval only |
| `C3_<system>_fp` | Native (full-pipeline) config retrieval + spec |

Any emit script encountering a non-canonical condition string aborts with a schema error.

## 8. Script naming

| Section | Script |
|---|---|
| §4.1 | `scripts/_v11_emit_4_1_gradient.py` |
| §4.2 | `scripts/_v11_emit_4_2_compression.py` |
| §4.2.1 | `scripts/_v11_emit_4_2_1_improvement_rates.py` |
| §4.3 | `scripts/_v11_emit_4_3_wrong_spec.py` |
| §4.4.1 | `scripts/_v11_emit_4_4_1_memory_systems.py` |
| §4.4.2 | `scripts/_v11_emit_4_4_2_mechanisms.py` |
| §4.4.3 | `scripts/_v11_emit_4_4_3_keckley.py` |
| §4.5 / Appendix F | `scripts/_v11_emit_4_5_letta.py` |
| §4.6.1 | `scripts/_v10_verification/tier2_mechanical_recompute.py` (existing) |
| §6.3 | `scripts/_v10_pipeline_variance.py` (existing) |
| §3.7.6 | `scripts/audit_low_end_inflation.py` (existing) |
| Appendix D | `scripts/_v11_emit_appendix_d.py` |

## 9. Master orchestrator

`scripts/_v11_paper_numbers.py`:
1. Calls every emit script via subprocess.
2. Aggregates all output JSONs into `docs/research/v11_paper_numbers.json` keyed by claim_id.
3. Walks the v10 paper, locates each claim_id's reference in the manuscript, compares.
4. Outputs `docs/research/v11_reconciliation_diff.md` listing every mismatch.
5. Exit code 0 if no mismatches, 1 otherwise.

## 10. Anti-patterns to reject

- **Manual transcription of numbers from analysis docs** into the paper. Any number in the paper that did not come from a `_v11_emit_*.py` script is suspect and must be flagged in `v11_reconciliation_diff.md`.
- **Inline computation in the manuscript** (e.g., "the lift is 2.23 - 1.55 = +0.68"). Compute in a script, emit the result.
- **Ad-hoc aggregation rules** different from §1's locked rule. Any deviation must be declared explicitly in the claim's `aggregation_rule` field and justified in script docstring.
- **Reusing legacy analysis docs as primary data**. Primary data is the per-judge JSON files. Analysis docs are derived; they are not authoritative.

## 11. Pre-flight checks (added 2026-04-25)

The v11 contract assumes every aggregation step reads a panel-complete primary-data set. Two failure modes broke that assumption during the v10 → v11 transition: a GPT-5.4 batch that silently 400-errored across §4.3 wrong_spec_v2 (520 records empty), and parallel failures in §4.4 Base Layer C1/C3 (936 records), §4.2 Bernal Diaz C8/C9 (78 records), and §4.5 Letta Hamerton (39 records). Root cause: ad-hoc judge invocation paths used `max_tokens` instead of `max_completion_tokens` for GPT-5.x. See `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md` for the diagnostic and `docs/reviews/v11_judge_call_controls_implementation_20260425.md` for the controls.

To prevent recurrence, two pre-flight checks are now mandatory:

### 11.1. Health probe before any large batch

Every large-batch (> 50 calls) judging script MUST call `scripts/_v11_validation/preflight_judge_health.py` first and abort on non-zero exit. Bypassing this is a CI failure. The probe sends one canonical 1-to-5 rubric prompt to every model in the panel and asserts a numeric score in [1, 5] within timeout.

### 11.2. Panel-completeness audit on aggregation

Every emit script that aggregates judgment data MUST call `scripts/_v11_validation/check_panel_completeness.py` (or import its scanning logic) and fail loudly on any unwaived `FULL_FAIL` or `SUSPECT` (>5% parse-failure rate) cell. Known-resolved batches go in `docs/research/v11_panel_completeness_waivers.json` with a tracked-in pointer; everything else is a release blocker.

### 11.3. Shared judge-call utility

All new judge-call code MUST import from `scripts/_judge_invocation/`:

```python
from _judge_invocation import call_judge, JudgeAPIError
result = call_judge("openai", "gpt-5.4", system="", user=prompt,
                    max_output_tokens=10, run_id="my_run")
```

The dispatcher routes to `max_completion_tokens` for any OpenAI model id prefixed with `gpt-5`, `o1`, or `o3`. Hand-rolled `httpx.post` calls into `api.openai.com/v1/chat/completions` from new code are a CI failure.

---

This contract is the v11 release-blocker. v10 → arXiv submission is gated on every claim in the paper having a passing `_v11_emit_*.py` scaffold and a passing `--verify` run.

## 12. Status as of 2026-04-25 release-freeze pass

This section records the empirical state of the v11 architecture at the close of the 2026-04-25 release-freeze pass for v10 arXiv submission. v11 contract compliance is **not** a prerequisite for the v10 submission; it is the next-version effort, scoped here for honest disclosure. Sections §1 through §11 describe the contract; this section describes how far the current scripts and audits actually meet it.

### 12.1. Emit-script schema compliance

All eight `_v11_emit_*.py` scripts are MAJOR or BLOCKER offenders against the §2-§3 schema contract, per the 2026-04-25 GPT-5.5 scaffolding review at `docs/reviews/v11_scaffolding_review_gpt55_20260425.md`. Representative case `_v11_emit_4_1_gradient.py` is the explicit BLOCKER reference. Common gap classes:

- Output JSON does not use the flat `claims` map required by §3; scripts emit bespoke nested structures keyed by subject or contrast.
- No per-number provenance block (estimand, contrast, filters, n, CIs) attached to individual values.
- No SHA-256 input manifest; provenance lists path strings, sometimes brace-glob descriptions instead of resolved files.
- No script git SHA or environment hash.
- `--verify` resolves paper values via hardcoded `PAPER_*` dictionaries inside the emit script, not by locating numbers in the manuscript via string match or claim-tag anchor (§4 violation).
- No real schema validation on judgment files; legacy condition strings are silently normalized rather than rejected.
- Statistical-method specifics (CI method, Wilcoxon tie handling, missing-cell policy) embedded in code rather than declared in the contract.

Full per-script gap list and the architecture-level minimum-fix set are in `docs/reviews/v11_scaffolding_review_gpt55_20260425.md` §1 and the "Minimum architecture fixes before freeze" subsection.

### 12.2. Panel-completeness audit status: GREEN

As of 2026-04-25, the panel-completeness audit (`scripts/_v11_validation/check_panel_completeness.py` against `docs/research/v11_panel_completeness_audit.csv`) passes with all 441 unwaived rows resolved. The four cluster classes documented in `docs/research/v11_panel_completeness_waivers.json`:

- **GPT-5.4 wrong-spec-v2 batch failures (13 subjects).** Original FULL_FAIL files preserved; authoritative reruns at `*_rerun_20260425.json` siblings. Closure trace: `docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md`.
- **§4.4 Base Layer C1/C3 GPT-5.4 batches (936 records).** Same root cause; same resolution pattern.
- **§4.2 Bernal Diaz C8/C9 (78 records).** Resolved via the same `max_completion_tokens` fix.
- **§4.5 Letta Hamerton (39 records).** Resolved.

All resolutions go through the shared `scripts/_judge_invocation/` dispatcher (§11.3) which routes GPT-5.x and o1/o3 models to the correct parameter name. The waivers file is the single source of truth for which legacy files are documented exceptions; everything outside the waivers is required to pass.

### 12.3. Reconciliation diff status

Last regenerated 2026-04-25 17:51 UTC at `docs/research/v11_reconciliation_diff.md`. 1,509 claim_ids aggregated:

- **MATCH:** 1,089 (72.2%)
- **MINOR_ROUNDING:** 65 (4.3%)
- **SUBSTANTIVE_MISMATCH:** 206 (13.7%)
- **NON_CLAIM (scaffold-only, no paper cite):** 149
- **SIGN_FLIPS surfaced:** 14, all at the running-list level; zero at the v10 paper-text level (verified directly in `docs/research/v11_table_rebuild_proposal.md` §3 walkthrough)

The 206 substantive mismatches were resolved through the Tier 1 + 2 + 3 paper edits applied 2026-04-25 per the apply order in `docs/research/v11_table_rebuild_proposal.md` §"Implementation note for the author" (Tier 1 silent cleanup → Tier 2 minor numeric drift → Tier 3 author-decision substantive).

### 12.4. §4.6.1 Tier 2 cross-provider replication: demoted to direction-only

§4.6.1 is the only paper section with no current v11 emit-script coverage. Under the audit, published Tier 2 magnitudes could not be reproduced under any aggregation rule tested. Per the 2026-04-25 release-freeze decision, §4.6.1 is **demoted to direction-only with sensitivity ranges**: the paper retains the directional claim (5 of 6 cells reproduce the spec direction across non-Anthropic response models) and reports a sensitivity range across aggregations, but no specific magnitudes carry through as primary results. A dedicated `_v11_emit_tier2.py` scaffold is post-arXiv work.

### 12.5. Known coverage gaps (deferred post-arXiv)

The following architecture compliance gaps are explicit and tracked, not silent:

- **Schema noncompliance of all eight emit scripts** (§12.1).
- **Hardcoded `PAPER_*` dicts inside emits** as the verification ground truth, instead of locating values in the manuscript by claim tag or string match.
- **No SHA-256 input manifest** in `_v11_emit_4_1_gradient.py` or any other emit; primary-data identification is by path string only.
- **No claim-tag injection in the manuscript** (e.g., `<!-- claim:4_1_slope -->` markers). `--verify` cannot reliably attach scaffold claims to specific paper cells without these.
- **No full numeric-literal census tool** for the rendered manuscript. The current `PAPER_ONLY = 0` heuristic is not a guarantee that every paper number is covered by a scaffold claim.
- **§4.6.1 Tier 2 has no emit script** (§12.4).
- **Legacy non-v11 scripts** at `scripts/_v10_verification/tier2_mechanical_recompute.py`, `scripts/_v10_pipeline_variance.py`, `scripts/audit_low_end_inflation.py` are still wired into the §8 script-naming table; they have not been upgraded to the v11 schema or provenance contract.

**Estimated effort to close all of §12.5:** 80-100 hours total. Deferred to post-arXiv v11+ work. v10 arXiv submission proceeds on the basis of the §12.3 reconciliation pass, the §12.2 panel-completeness GREEN, and the §12.4 §4.6.1 demotion.

### 12.6. Release-freeze pass 3 (2026-04-25 evening, post-GPT-5.5-v10.1-review)

Paper version bumped v10 → v10.1. Manuscript paths now `docs/beyond_recall_v10_1_draft.md` + `.docx`. A fresh GPT-5.5 review of v10.1 is at `docs/reviews/v10_1_review_gpt55_20260425.md` (verdict NEEDS_REVISION pre-fix; addressed by this pass).

**Four critical contradictions resolved:**

1. **§4.1 battery-generator wording corrected.** The "13 global subjects = GPT-5.4 batteries" framing was wrong. Ground truth: all 14 main-study batteries are Haiku-generated. The subset regression is a drop-Hamerton check, not a "restrict to GPT-5.4" check. Verified by direct reads of `metadata.model` across `results/global_<subject>/battery_v2.json` for every global subject and Hamerton's `data/hamerton/battery.json`. Verifier: `scripts/_v11_validation/verify_4_1_sensitivity.py` (all numbers reproduce within rounding).
2. **Tier 2 response-model count corrected.** Tier 2 cross-provider replication uses 2 response models (Sonnet 4.6 + Gemini 2.5 Pro), not 4. Opus and GPT-5.4 are Tier 2 judges only; Tier 2 batteries are GPT-5.4-generated. Fixed in §1.2, §1.3, §5.2, §6.2. Verified by file enumeration under `results/_tier2/`.
3. **§4.3 wrong-spec denominator disambiguated.** The 587 paired-question count decomposes as 507 v2 (13 globals × 39 questions) + 80 v1 (Hamerton across all 5 battery tiers). Disambiguated in §1.3 and §4.3. Verified against `docs/research/wrong_spec_detection_raw.json`.
4. **§4.4.2 Table 4.6 rebuilt on strict 5-judge primary panel.** Entire table rebuilt, not just the Aggregate Δ column. Recompute script: `scripts/_table_4_6_5judge_recompute.py`. All 8 rows updated; no sign flips; Aggregate Δs shrink by 0.01 to 0.06; Letta and Hamerton n drops to 38 (one paired question excluded by strict-rule). This closes Tier 3 author-decision item #6 from the table-rebuild proposal.

**Revision-quality items applied:**

- §1.4 and §5.3 living-user wording: "expected by construction" → "closest available proxy".
- §4.1 and §5.5 framing: "C4a ceiling" → "post-spec operating level".
- §5.2 H5 reframed to credit fact extraction.
- §4.4 "3 of 4 commercial systems" softened with appropriate nuance.
- §4.6.1 "not Haiku-specific" softened to "small probe reduces likelihood".
- v10 / v11 nomenclature in paper prose: "v11 mechanistic-check audit" → "verification audit".

**Closure note.** Pass 3 closes the GPT-5.5 v10.1 critical-contradiction set. Items the same review flagged as deferred (human validation, component ablation, hierarchical modeling) are post-arXiv v11+ work and remain catalogued in §12.5. Sections §1 through §11 and the original §12 (passes 1 and 2) are unchanged and still authoritative.
