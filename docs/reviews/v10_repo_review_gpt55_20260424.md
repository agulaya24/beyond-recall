# Beyond Recall v10 Repo Review — GPT-5.x

**Generated:** 2026-04-24 20:31:50
**Model requested chain:** ['gpt-5.5', 'gpt-5.4', 'gpt-5', 'gpt-4o']
**Model actually used (API response):** `gpt-5.5-2026-04-23`
**Prompt length:** 20,191 chars (~5,047 tokens)
**Usage:** {"prompt_tokens": 5718, "completion_tokens": 3424, "total_tokens": 9142, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 512, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}
**Response length:** 12141 chars, 1543 words

**Attempt log:**
```json
[
  {
    "model": "gpt-5.5",
    "attempt": 1,
    "elapsed_s": 42.6,
    "words": 1543,
    "ok": true
  }
]
```

---

## Verdict

**CRITICAL_FIXES_REQUIRED** — the repo is rich and close in substance, but it is not release-ready because the declared source-of-truth documents contradict the active v10 paper, key provenance paths are broken, and a fresh clone cannot reliably reproduce the headline numbers.

## Highest-impact single improvement

Create a **v10 release freeze/reproducibility pass**: update `README.md`, `ISSUES.md`, `AGENTS.md`, `agents/study-guide.md`, `agents/STUDY_MEMORY.md`, `docs/DATA_REFERENCE.md`, `docs/KEY_FINDINGS.md`, and `docs/PROVENANCE_INDEX.md` so they all name `docs/beyond_recall_v10_draft.md` as canonical, report the same 5-judge primary headline numbers, and point to one documented command/script that regenerates the v10 tables from committed raw judgments.

This single pass would remove most of the credibility risk.

## Critical issues

1. **The “single source of truth” disagrees with the paper.**  
   `docs/DATA_REFERENCE.md` says it wins over the paper, but it reports the stale 7-judge slope:

   - `docs/DATA_REFERENCE.md`: slope **−0.98 [−1.30, −0.74]**
   - `docs/KEY_FINDINGS.md`: slope **−0.98 [−1.30, −0.74]**
   - `docs/beyond_recall_v10_draft.md`: slope **−0.96 [−1.24, −0.67]**

   This is the most damaging issue. A reviewer will reasonably conclude the headline regression is unstable or undocumented, even if the underlying reason is only a stale 7-judge/5-judge transition.

2. **Canonical draft is inconsistent across orientation docs.**

   - `README.md` header says active draft is v9.
   - `README.md` structure block says v8 is current.
   - `AGENTS.md` says v8 is the working draft.
   - `agents/study-guide.md` says v9 is current.
   - `docs/beyond_recall_v10_draft.md` exists and appears to be the actual active paper.
   - `ISSUES.md` does not mention v10.

   This is a first-read embarrassment. The repo looks internally out of sync.

3. **Broken provenance for the Letta stateful-agent case study.**

   `docs/DATA_REFERENCE.md` points to:

   - `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json`

   But that directory is not present. Related artifacts appear instead under:

   - `docs/research/_letta_blocks/`
   - `docs/research/_letta_rerun/`
   - `docs/research/letta_stateful_matched_rerun.md`
   - `docs/research/letta_stateful_deep_read.md`

   Because v10 reports the Letta stateful-agent result as an exploratory case study, this does not necessarily invalidate the main paper, but the broken trace is a public-release blocker unless fixed or explicitly marked historical/obsolete.

4. **Cold reproduction is not currently reliable.**

   Problems include:

   - No root `requirements.txt`, `pyproject.toml`, or `environment.yml`.
   - 42 scripts hardcode `C:/Users/Aarik/...` paths.
   - Some scripts require directories outside the repo, e.g. `hamerton_memory/` and `franklin_clean_memory/`.
   - The script that created `results/RESULTS_S113.json` is unclear.
   - `scripts/recompute_5judge_primary.py` exists but is not clearly surfaced as the canonical v10 recompute path.

5. **Agent/navigation docs point to nonexistent or moved files.**

   Examples:

   - `agents/STUDY_MEMORY.md` references `scripts/run_letta_stateful_test.py` and `scripts/run_letta_memory_as_context.py`, which do not exist.
   - `agents/study-guide.md` points to `docs/beyond_recall_v6_draft.md`, but v6 is under `docs/versions/`.

## Reproducibility audit

A third party **cannot yet cleanly reproduce the headline numbers from raw data plus scripts in a fresh clone**.

What is reproducible:

- `scripts/_v10_battery_sensitivity.py` is self-contained and reproduces the v10 sensitivity analysis / univariate slope.
- Raw per-judge judgments appear to be present under `results/<subject>/...`.
- `scripts/recompute_5judge_primary.py` exists and appears to be the intended canonical recompute script.
- `_audit_with_c2c.py` reportedly reproduces the D.3.4/D.3.5 audit numbers.
- Wrong-spec, Supermemory, and several paired analyses are traceable through `docs/research/` artifacts.

Main gaps:

- There is no single documented path from committed raw judgments to the v10 headline table, slope, confidence interval, Wilcoxon test, and 9-of-9 low-baseline claim.
- `docs/DATA_REFERENCE.md` and `docs/KEY_FINDINGS.md` still present older 7-judge numbers.
- The v10 sensitivity script embeds data inline, which is useful for verification but not a raw-data-to-result reproduction pipeline.
- `results/RESULTS_S113.json` has unclear generation provenance.
- The Letta stateful provenance path is broken.
- No dependency/environment file means even clean scripts may fail for avoidable reasons.

Minimum acceptable fix: add a documented `scripts/reproduce_v10_primary.py` or `make reproduce-v10` path that reads committed `results/*judgments*.json`, regenerates the v10 subject table, regression, CI, p-value, low-baseline summary, and writes a machine-readable output that matches the paper.

## Documentation audit

The documentation does **not** currently tell a coherent story.

The major conflict is the canonical-draft/versioning story:

| File | Problem |
|---|---|
| `README.md` | Mentions v9 as active in the header and v8 as current in the structure block; does not mention v10. |
| `ISSUES.md` | Says overall health is GREEN but does not account for v10. Open P1/P2 issues are substantial. |
| `AGENTS.md` | Says v8 is the working draft; does not mention v9/v10. |
| `agents/study-guide.md` | Says v9 is current; does not mention v10. |
| `agents/STUDY_MEMORY.md` | Still contains stale Letta script references and v8-era orientation. |
| `docs/DATA_REFERENCE.md` | Claims to be source of truth but contains stale 7-judge numbers and broken provenance. |
| `docs/KEY_FINDINGS.md` | Still reports stale slope and low-baseline numbers. |
| `docs/PROVENANCE_INDEX.md` | Still contains v6/v8/v9 anchors and broken/misaligned Letta provenance. |

The result is that a reviewer cannot tell whether v8, v9, v10, S113, or S114 is the actual public artifact.

Recommended documentation repair:

1. Declare v10 canonical in every orientation file.
2. Add a short “Version history / what changed from v9 to v10” note.
3. Update `DATA_REFERENCE.md` to the 5-judge primary values or rename/archive it as an S113/7-judge reference.
4. Update `KEY_FINDINGS.md` to match v10.
5. Fix `PROVENANCE_INDEX.md` paths or mark obsolete rows as historical.
6. Add a “Reproduce headline results” section to `README.md`.

## Code-quality and hygiene

The codebase looks like an active research workspace rather than a polished public companion repo.

Main issues:

- **No root dependency specification.**  
  Missing `requirements.txt`, `pyproject.toml`, or `environment.yml`.

- **Hardcoded local Windows paths.**  
  At least 42 scripts use `C:/Users/Aarik/...`. This is acceptable for archived internal scripts only if clearly separated, but not for a public reproducibility surface.

- **Scripts depending on data outside the repo.**  
  Examples include `scripts/run_multimodel_responses.py`, `scripts/run_franklin_judge.py`, and `scripts/sync_to_study_repo.py`.

- **Too many transient scripts at top level.**  
  The 31 `_probe_*.py` / `_check_*.py` files make `scripts/` hard to navigate.

- **Committed build/cache artifacts.**  
  Examples include:
  - `scripts/__pycache__/`
  - `docs/beyond_recall_test.aux`
  - Word temp files such as `docs/~$yond_recall_v8_draft.docx` and `docs/~WRL2113.tmp`
  - empty `scripts/results/global_cellini/`

- **Local workspace artifacts.**  
  `workspace/study_knowledge.db` and `workspace/study_vectors/` should be reviewed carefully before release. They may be harmless, but vector stores/databases often contain duplicated source text, prompts, notes, or private material.

- **API runner scripts need clearer separation.**  
  There should be a distinction between:
  - reproducibility scripts that run offline from committed data,
  - optional API re-run scripts,
  - historical/internal scripts not expected to run.

The existing `scripts/README.md` is a good sign because it honestly documents many of these limitations. But for public release, the top-level experience still needs to be cleaner.

## Comparison to expected open-science norms

For an arXiv-companion repo of this size and complexity, a strong reviewer would expect:

1. **One canonical public paper draft.**  
   Not v8/v9/v10 ambiguity.

2. **One canonical data reference matching the paper.**  
   If 5-judge primary is the paper’s basis, all headline docs should use 5-judge numbers.

3. **A frozen release manifest.**  
   E.g. `RELEASE_v10.md` or `MANIFEST_v10.json` listing:
   - paper draft,
   - raw data inputs,
   - scripts used,
   - output files,
   - expected hashes/checksums,
   - exact headline numbers.

4. **A documented end-to-end reproduction command.**  
   Even if API reruns are not possible, offline recomputation from committed judgments should be possible.

5. **Dependency/environment file.**  
   Minimum: `requirements.txt`. Better: `pyproject.toml` or `environment.yml`.

6. **Clear distinction between raw data, derived results, and exploratory notes.**

7. **Archived historical drafts moved out of the main path.**  
   Keeping v6/v7/v8/v9 is fine, but the README should not make them look current.

8. **No broken provenance links.**

9. **No local-machine paths in canonical scripts.**

10. **No cache/temp/build artifacts.**

11. **A data dictionary for result JSON schemas.**  
   `DATA_REFERENCE.md` helps, but the repo would benefit from explicit schema notes for judgment files, battery files, facts files, and consolidated result files.

12. **A public-release privacy/security checklist.**  
   Especially because the repo includes API interactions, local workspace indexes, docx files, and internal review material.

## Risks for public release

Worst-case public outcome:

A reviewer opens the repo, sees that `README.md`, `AGENTS.md`, `DATA_REFERENCE.md`, and the v10 paper disagree, tries to trace the Letta result, hits a missing directory, then tries to rerun scripts and encounters hardcoded Windows paths and missing dependencies. The public interpretation becomes: “The paper’s headline numbers are not reproducible and the repo is disorganized,” even if the underlying data are mostly present.

Before pushing the public-visible commit, the author should check:

1. **Numerical consistency**
   - Update `docs/DATA_REFERENCE.md` to v10 5-judge values or explicitly archive it as S113/7-judge.
   - Update `docs/KEY_FINDINGS.md`.
   - Confirm README headline numbers match v10.

2. **Canonical draft consistency**
   - Every orientation doc should say `docs/beyond_recall_v10_draft.md` is canonical.
   - Historical drafts should be clearly labeled historical.

3. **Broken provenance**
   - Fix or remove the nonexistent `results/run_fullstack_hamerton_20260411_231237/letta_stateful_test_result.json` reference.
   - Add a correct Letta stateful provenance note pointing to the actual files.

4. **Fresh-clone reproduction**
   - Add dependency file.
   - Add one offline reproduction script.
   - Test in a clean checkout on a non-author machine/path.

5. **Repo hygiene**
   - Remove `__pycache__`, `.aux`, Word temp files, empty transient dirs, and obvious probe/check scripts unless archived.
   - Move internal or historical scripts to `scripts/archive/` or mark them clearly.

6. **Secret/privacy scan**
   - Search for API keys, tokens, account IDs, provider request IDs, local usernames, private comments, and internal notes.
   - Inspect `workspace/study_knowledge.db` and `workspace/study_vectors/` before publishing.
   - Consider excluding `docs/internal/` from the public release unless intentionally public.

7. **Licensing/data rights**
   - Confirm all subject source texts and derived batteries/facts can be distributed under the repo’s stated Apache 2.0 license or explain exceptions.

Bottom line: the repo is substantively strong and contains a lot of valuable provenance, but it should not be released in the current state. The public release needs a v10 coherence/reproducibility pass first.