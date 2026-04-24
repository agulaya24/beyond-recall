# v10 Release-Freeze Pass — Closure Report

**Date:** 2026-04-24
**Trigger:** GPT-5.5 repo review (`docs/reviews/v10_repo_review_gpt55_20260424.md`) flagged 3 P0-class issues plus several P1 hygiene items against the released v10 paper.
**Scope:** Reconcile orientation docs and source-of-truth references with `docs/beyond_recall_v10_draft.md` (5-judge primary panel canonical), repair broken Letta provenance, add reproducibility infrastructure, complete repo hygiene.
**Outcome:** All 3 P0 items closed. Reproducibility infrastructure added (`requirements.txt`, `REPRODUCE.md`). 1 P1 remains: 42 scripts hardcoding `C:/Users/Aarik/...` paths, documented in `REPRODUCE.md` rather than parameterized.

---

## 1. Source-of-truth doc reconciliation (P0)

### 1.1. `docs/DATA_REFERENCE.md`

Full rewrite to v10's 5-judge primary panel as canonical with 7-judge as sensitivity:

- **§1 per-subject gradient table:** replaced with the v10 §4.1 per-subject numbers (line 718 of `docs/beyond_recall_v10_draft.md`). Per-subject columns now show C5 baseline, C2a spec-only, C4a facts+spec, Δ spec, Δ facts+spec, anchor-crossing flag. Columns match v10 §4.1 verbatim.
- **§1 aggregates:** recomputed from the v10 table.
  - All-14 mean Δ_C4a: 7-judge `+0.67` → 5-judge primary `+0.55`
  - All-14 mean Δ_spec: 7-judge `+0.53` → 5-judge primary `+0.43`
  - Low-baseline (n=9) mean Δ_C4a: 7-judge `+1.04` → 5-judge primary `+0.89`
  - Low-baseline mean Δ_spec: 7-judge `+0.84` → 5-judge primary `+0.69`
  - Positive-Δ_C4a count unchanged at 12 of 14 (Zitkala-Sa, Equiano negative)
  - 9 of 9 low-baseline positive: unchanged across panels
  - Mean C4a across all 14 subjects = 2.44 (added; supports the coupling reframing)
- **§2 statistical tests:** 5-judge primary canonical with 7-judge sensitivity called out:
  - Slope: 7-judge `−0.98 [−1.30, −0.74]` → 5-judge primary `−0.96 [−1.24, −0.67]`, R² = 0.82, p < 0.001
  - Wilcoxon C5 vs C4a: 7-judge `W=9.0, p=0.0063` → 5-judge primary `W=11, p=0.007`
  - Wilcoxon C5 vs C2a: 7-judge `W=10.0, p=0.0076` → 5-judge primary `W=10, p=0.005`
  - Spearman ρ: legacy `0.89-0.98` (4-judge Hamerton historical) marked clearly as such; primary `0.86-0.93` across 5-judge panel (10 pairs)
- **§2 battery-composition sensitivity (NEW):** added per v10 §4.1 line 749:
  - Multiple regression on C5 + LITERAL_RECALL fraction: partial slope = `−0.88 [−1.13, −0.63]`, p < 10⁻⁵; LITERAL_RECALL β = `+2.30 [+0.34, +4.26]`, p = 0.026; adjusted R² = 0.87
  - GPT-5.4-battery-only subset (drops Hamerton): slope = `−0.89 [−1.18, −0.61]`, R² = 0.81, p < 10⁻⁴
  - Reproducibility script: `scripts/_v10_battery_sensitivity.py`
- **§2 coupling-free reframing (NEW):** added per v10 §4.1 line 755:
  - Level regression C4a ~ C5: slope = `+0.04 [−0.25, +0.33]`, R² = 0.008, p = 0.76, mean C4a = `2.46`
  - Permutation null on Δ-on-C5 slope (10,000 iterations): centered at −0.998 (SD 0.127); two-sided p = 0.77
  - Subject-level bootstrap (10,000 iterations): Δ-on-C5 slope CI = `[−1.254, −0.740]`; level slope CI = `[−0.254, +0.260]`
  - Honest-reframing prose preserved verbatim from v10 §4.1
  - Reproducibility script: `scripts/_v10_coupling_sensitivity.py`
- **§7 Letta stateful-agent test:** rewritten to n=3 generalization (Hamerton + Ebers + Babur), 5-judge primary deltas (+0.14, +1.05, +0.54). Block coherence ceiling at scale (Babur 25.4% verbatim duplication) added. Old Hamerton-only framing removed. Demoted to "exploratory case study" per v10 §4.5 framing.
- **§8 Hamerton compression table:** rewritten to v10 §4.2 5-judge primary numbers (C8=2.27, C9=3.09, C4a=2.77, C4=2.43, C2a=2.63, C5=1.26 on Hamerton; low-baseline aggregate added with mean C8 − C2a gap = +0.22). 7-judge sensitivity values noted inline.
- **§9 judge panel:** restructured to highlight the 5-judge primary vs. sensitivity split with a column showing in-primary status.
- **§K provenance:** every row checked. Letta paths fixed (see §2 below). Hamerton Table 4.2 rewired to actual `results/hamerton/c8_c9_judgments_*.json` files. v10-script paths added (`scripts/_v10_battery_sensitivity.py`, `scripts/_v10_coupling_sensitivity.py`).
- **Header:** "wins over the paper" language removed. New header: "Any discrepancy between this document and the v10 paper draft should be resolved in favor of the v10 paper. v10 is the canonical artifact; this document mirrors v10's 5-judge primary panel and its sensitivity reframing."

### 1.2. `docs/KEY_FINDINGS.md`

Updates targeted at the findings most affected by the panel switch:

- **Header:** now names `docs/beyond_recall_v10_draft.md` as canonical and DATA_REFERENCE as synced to v10's 5-judge primary panel.
- **NEW v10 revision banner:** documents the numerical shifts (slope, all-14 mean Δ_C4a, low-baseline mean Δ_C4a, Spearman ρ correction, §4.5 demotion to exploratory, battery + coupling sensitivities added).
- **M1 (gradient):** rewritten to 5-judge primary with battery + coupling sensitivities. Headline slope `−0.96 [−1.24, −0.67]`, low-baseline mean Δ_C4a `+0.89`, all-14 mean Δ_C4a `+0.55`, 12 of 14 positive (Zitkala-Sa + Equiano negative). 7-judge values explicitly called out as sensitivity.
- **M8 (compression):** rewritten to 5-judge primary Hamerton numbers (C8=2.27, C9=3.09, C2a=2.63, C5=1.26). Token-budget margin updated from +0.51 to +0.20. Low-baseline aggregate added.
- **m6 (Spearman ρ):** prose unchanged (already at 0.86-0.93 from prior pass); paper-location updated to v10 §3.7 / §4.6.

M2-M7 and M9 already cited v10-correct numbers; not modified.

### 1.3. Misleading "wins over the paper" language

The line "Any discrepancy between this document and the paper draft should be resolved in favor of this document" at the bottom of `DATA_REFERENCE.md` was reversed. v10 paper is now the canonical artifact for resolving disagreements.

---

## 2. Letta-stateful provenance trace fix (P0)

### Broken paths (now removed)

- `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json`
- `results/run_fullstack_hamerton_20260411_231237/letta_memory_haiku_judgments_*.json`
- `results/run_fullstack_hamerton_20260411_231237/*_judgments_*.json` (Hamerton Table 4.2 source)

`results/run_fullstack_hamerton_20260411_231237/` does not exist in the repository as committed.

### Replacement paths (now in DATA_REFERENCE §K)

| Artifact | New path |
|---|---|
| Letta stateful-agent main rerun (n=3, 5-judge primary) | `docs/research/_letta_rerun/5judge_primary_results.json` |
| Letta rerun pipeline scripts | `docs/research/_letta_rerun/{20_run_c2a_named.py, 40_judge_responses.py, 50_aggregate.py, 70_compute_5judge_primary.py}` |
| Per-subject Letta rerun judgments | `docs/research/_letta_rerun/{hamerton,ebers,babur}_judgments_*.json` plus `{ebers,babur}_letta_battery.json` |
| Letta full-stack BL rerun (§4.5 footnote) | `docs/research/_letta_rerun/fullstack_named/5judge_fullstack_results.json` |
| Full-stack BL rerun pipeline | `docs/research/_letta_rerun/fullstack_named/fs_{01..07}_*.py` |
| Per-subject full-stack BL judgments | `docs/research/_letta_rerun/fullstack_named/{hamerton,ebers,babur}_fullstack_judgments_*.json` |
| Raw Letta `human` block dumps | `docs/research/_letta_blocks/{hamerton,ebers,babur}_human_block.txt` |
| Letta paired analysis | `docs/research/_letta_blocks/paired_scores.json`, `compute_paired.py` |
| Summary reports | `docs/research/letta_stateful_matched_rerun.md`, `docs/research/letta_stateful_deep_read.md` |

### Hamerton block dump

GPT-5.5 review's task description hinted at a possible gap on Hamerton's raw block dump. Confirmed present at `docs/research/_letta_blocks/hamerton_human_block.txt` (22,502 bytes). All three subject blocks (Hamerton, Ebers, Babur) are committed.

### Hamerton Table 4.2 source

Rewired to `results/hamerton/c8_c9_judgments_*.json` (per-judge: haiku, sonnet, opus, gpt4o, gpt54, plus `c8_c9_judgments_merged.json`) for the C8/C9 conditions, and `results/hamerton/{judgments.json, sonnet_judgments.json, opus_judgments.json, gpt4o_judgments.json, gpt54_judgments.json}` (and `judgments_harmonized.json` for legacy harmonization) for C2a/C2c/C4a/C5. All files exist in the repo.

---

## 3. Canonical-draft story across orientation docs (P0)

| File | Change |
|---|---|
| `README.md` (top-level) | Header replaced: v10 is canonical. v9, v8 marked as preserved baselines. v6 path corrected to `docs/versions/`. ISSUES-first warning preserved. New REPRODUCE.md pointer added. |
| `README.md` Key Findings #1 | Headline-slope line now reads as 5-judge primary with battery and coupling-sensitivity numbers in the same paragraph. |
| `README.md` Key Findings #4 | Letta stateful-agent demoted to "exploratory" with explicit n=3 framing. |
| `README.md` Key Findings #6 | Robustness block expanded with battery-composition partial slope, GPT-5.4-battery subset slope, coupling-free reframing slope, mean C4a, and corrected Spearman ρ. |
| `README.md` Repository Structure | `docs/` block listed `beyond_recall_v8_draft.md` as current and `beyond_recall_v6_draft.md` at top level; rewritten to put v10 at the top, v9/v8 as preserved baselines, v6 in versions. |
| `README.md` judges line | "7 judges, 3 providers" replaced with "5-judge primary panel" + 7-judge sensitivity callout. |
| `AGENTS.md` Current state | Replaced "S114 voice review in progress" with "v10 release-frozen 2026-04-24" plus headline-numbers summary. |
| `AGENTS.md` What's in this repo | v10 canonical entry, baseline drafts marked as such. |
| `AGENTS.md` Read-these list | Updated to point at v10 paper, v10 release-pass closure, REPRODUCE.md. |
| `AGENTS.md` workflows | "Verify a number" + "Update the paper" workflows updated; v10 release-frozen rule added. |
| `AGENTS.md` What NOT to do | "Don't edit the v6 draft; edit v8" replaced with "Don't edit baseline drafts (v6, v7, v8, v9); v10 is release-frozen." |
| `agents/STUDY_MEMORY.md` Top banner | New v10 banner added. v9 banner preserved underneath as "in progress, late evening 2026-04-23" historical state. |
| `agents/STUDY_MEMORY.md` New v10 section | Documents §4.1.2 author pilot removal, §1.5 / §5.7 alignment fold, battery + coupling sensitivities, §4.5 demotion to exploratory, References / Bibliography append, Spearman ρ correction, headline 5-judge primary numbers. |
| `agents/STUDY_MEMORY.md` Letta script paths | Verified existing references already point at `docs/research/_letta_rerun/` numbered pipeline; no stale `run_letta_stateful_test.py` references remain. |
| `agents/study-guide.md` Current State | v8/v9 wording replaced with v10 release-frozen + 5-judge primary panel notes. |
| `agents/study-guide.md` First Stop for Numbers | DATA_REFERENCE described as v10 5-judge primary canonical with 7-judge sensitivity. |
| `agents/study-guide.md` Directory Layout | v10 canonical, v9/v8 preserved-baselines, v6 in versions. |
| `ISSUES.md` Quick Status banner | Updated to v10 release-freeze pass; P0 closures (8) and P1 closures (8) tabled. |
| `ISSUES.md` P0 — Resolved this session | New section "v10 release-freeze pass (2026-04-24)" with V10-1 through V10-5. |
| `ISSUES.md` P1 — Resolved this session | New section listing B5-B11 + C2 + C3 closures with rationale. C4 (hardcoded paths) preserved as the one remaining P1, with an explicit note that the v10 release-freeze pass documented (not parameterized) the issue in REPRODUCE.md. |
| `ISSUES.md` P2 hygiene | Reorganized: A1, A2, A3 confirmed already absent at start of pass; A4 removed (`scripts/__pycache__/` deleted); other P2 items marked out-of-scope or resolved. New row GIT-1 captures `.gitignore` additions. |

---

## 4. Reproducibility infrastructure (P1)

### `requirements.txt`

Created at repo root. 13 deps captured from import-statement audit of `scripts/*.py` and `docs/research/_letta_rerun/*.py`. Provider SDKs that the paper text mentions but no committed script imports (mem0ai, letta-client, zep-cloud, supermemory, mistralai, cerebras-cloud-sdk, google-generativeai, groq) are explicitly excluded with a comment explaining why; their HTTP-equivalent code lives in upstream `memory_system/`. Lower-bound pins only.

Lines: 30.

Confirmed deps:

- anthropic, openai (SDK clients)
- numpy, pandas, scipy, statsmodels (analysis)
- matplotlib, seaborn (figures)
- sentence-transformers, chromadb (Base Layer retrieval substrate)
- pypandoc, python-docx, markdown (document export)
- httpx, requests (review-script HTTP)

### `REPRODUCE.md`

Created at repo root. 7 sections:

1. Environment (Python 3.12, venv setup)
2. Reproduce §4.1 sensitivity analyses (no API calls; `scripts/_v10_battery_sensitivity.py` + `scripts/_v10_coupling_sensitivity.py` reproduce all v10 §4.1 numbers including the −0.96 univariate, −0.88 partial, −0.89 subset, +0.04 level slope, mean C4a 2.46, permutation null, bootstrap CIs)
3. Higher-cost recomputes (`scripts/recompute_5judge_primary.py`, `scripts/compute_memory_systems_5judge.py`)
4. Letta stateful-agent rerun (pipeline pointers; not on canonical reproduction path)
5. Hardcoded-path inventory (portable scripts vs. scripts requiring manual edits; future cleanup proposal: `BASELAYER_REPO_ROOT` env var)
6. Where the v10 numbers come from (table mapping each v10 numerical claim to its source files / scripts)
7. What is NOT reproducible offline (provider memory-system reruns, cross-LLM review scripts, Word doc export)

Lines: ~140.

---

## 5. Repo hygiene (P2)

| Target | Outcome |
|---|---|
| `scripts/__pycache__/` | Deleted: `export_v10_to_docx.cpython-312.pyc`, `recompute_5judge_primary.cpython-312.pyc`, plus the `__pycache__/` directory. |
| `docs/~$yond_recall_v8_draft.docx`, `docs/~WRL2113.tmp` | Already absent at start of pass (cleaned in prior hygiene work). Confirmed missing. |
| `docs/beyond_recall_test.aux` | Already absent at start of pass. Confirmed missing. |
| `scripts/results/global_cellini/` | Already absent at start of pass. Confirmed missing. |
| `.gitignore` | Added `*.aux` (LaTeX artifacts) and `~$*` (Word/Office temp). `__pycache__/` and `*.tmp` already covered. |

---

## 6. Hardcoded path audit (P1, documented not fixed)

42 scripts hardcode `C:/Users/Aarik/...` paths. Per the task, these are documented in `REPRODUCE.md` §5 rather than parameterized. The documented split:

- **Portable (no edits required):** All `scripts/_v10_*.py`, `scripts/recompute_5judge_primary.py`, `scripts/compute_*.py`, `scripts/classify_*.py`, all numbered scripts under `docs/research/_letta_rerun/` and its `fullstack_named/` subdirectory.
- **Hardcoded paths (manual edits or env var required):** `scripts/run_multimodel_responses.py`, `scripts/run_franklin_judge.py`, `scripts/sync_to_study_repo.py`, plus the `_probe_*` / `_check_*` / `_diag_*` transient script families.
- **Future cleanup proposal:** single `BASELAYER_REPO_ROOT` environment variable.

---

## 7. Stale agent references (C2, C3)

- **C2 (`agents/STUDY_MEMORY.md` Letta script-path mismatch):** confirmed-not-broken in current STUDY_MEMORY.md. Existing references already point at `docs/research/_letta_rerun/` numbered pipeline (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, etc.). No `run_letta_stateful_test.py` or `run_letta_memory_as_context.py` references remain. C2 closed without further edits.
- **C3 (`agents/study-guide.md:62` v6 pointer):** updated to point at v10 canonical with v9/v8 as preserved baselines and v6 located at `docs/versions/beyond_recall_v6_draft.md`.

---

## 8. Out of scope (deferred)

- §-by-§ remap pass for `docs/research/` files still anchored to v8 numbering. v10 paper is the canonical artifact; research-doc anchors are flagged for a future cleanup in ISSUES.md (B11).
- `docs/PROVENANCE_INDEX.md` v6/S113/S115 layered structure was not rewritten in this pass beyond confirming Letta-stateful artifact paths. The S115 addendum already documents v8-era claims; v10-era claims are covered by DATA_REFERENCE updates and this report.
- Deduplication / archival of `docs/reviews/` top-level vs. `_archive/` files. Out of scope.
- `docs/_results_snapshot.txt` Supermemory n=10 row (B9). Out of scope.
- `scripts/_probe_*.py` / `_check_*.py` (~30 files): kept; deferred per A5.

---

## 9. Summary

3 of 3 P0 items closed. 8 of 9 P1 items closed (C4 hardcoded-paths preserved with documentation rather than fix). All P2 hygiene targets either already absent or resolved.

Reproducibility infrastructure (`requirements.txt`, `REPRODUCE.md`) added; both v10 §4.1 sensitivity scripts (`scripts/_v10_battery_sensitivity.py`, `scripts/_v10_coupling_sensitivity.py`) confirmed self-contained and reproducible from a fresh clone given Python 3.12 + the `requirements.txt` deps.

`docs/DATA_REFERENCE.md` is now the v10 5-judge primary canonical reference; `docs/KEY_FINDINGS.md` aligns to v10 on M1 + M8 + m6; all five orientation docs (`README.md`, `AGENTS.md`, `agents/STUDY_MEMORY.md`, `agents/study-guide.md`, `ISSUES.md`) name `docs/beyond_recall_v10_draft.md` as canonical.

The repo is release-ready against the v10 paper.
