# Beyond Recall v11 Scaffolding Review (GPT-5.5)

_Generated 2026-04-25 by `scripts/review_v11_scaffolding_gpt55.py`._

**Model:** gpt-5.5-2026-04-23
**Usage:** {"prompt_tokens": 43537, "completion_tokens": 7619, "total_tokens": 51156, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 1420, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}

---

## Bottom line

The v11 architecture is a **good direction**, but it is not yet a release-grade reproducibility contract. It is currently a mix of (i) a strong aspirational spec, (ii) partial emit scaffolding, and (iii) a reconciliation pipeline that has already shown serious paper-locator / running-list failures. I would not freeze v11 until the author closes the Tier 2 coverage hole, fixes the paper-number census, and demonstrates that every emit actually satisfies the contract it claims to satisfy.

The most serious issue is not that 13.7% of claim_ids drift. Drift is expected in a rebuild. The serious issue is that the system still cannot reliably answer: **“Is every number in the manuscript accounted for by a scaffold claim, and is every scaffold claim actually compared to the right manuscript number?”**

Right now, the answer is no.

---

# 1. Architecture soundness

## Is the contract sufficient in principle?

Mostly yes. The architecture spec contains the right core ideas:

- named emit script per paper section;
- primary-data-only inputs;
- locked aggregation rule;
- flat stable `claim_id`s;
- per-number provenance;
- input checksums;
- schema validation;
- atomic outputs;
- idempotency;
- master reconciliation;
- CI drift/golden tests;
- panel-completeness preflight;
- mandatory shared judge invocation.

That is the right kind of infrastructure for a paper with many empirical numbers.

## But the representative script does not satisfy the contract

The representative `_v11_emit_4_1_gradient.py` materially violates or weakens several requirements in the architecture spec.

### Major mismatches

1. **Output schema does not match the declared v11 JSON schema.**  
   The spec requires:

   ```json
   {
     "schema_version": "...",
     "section": "...",
     "aggregation_rule": "...",
     "claims": {
       "<claim_id>": {
         "value": ...,
         "estimand": ...,
         "contrast": ...,
         "filters": ...,
         "n": ...,
         ...
       }
     },
     "provenance": {...}
   }
   ```

   The representative script emits a bespoke structure with `subjects`, `summary`, and nested regression objects. That may be human-readable, but it is not the flat claim-id contract. If other scripts follow this style, the master orchestrator has to infer claims from ad hoc nested structures, which reintroduces unmonitored paths.

2. **No per-number provenance.**  
   The spec requires every number to carry provenance: inputs, filters, aggregation rule, contrast, script version, timestamp. The script gives only coarse script-level provenance. That is not enough to audit individual cells.

3. **No SHA-256 input manifest.**  
   The spec explicitly requires checksums, sizes, and record counts for every input file. The script only records path strings, some of which are brace-glob descriptions rather than actual files.

4. **No real schema validation.**  
   The spec says every judgment file must be validated for required fields, score range, canonical condition, known judge, etc. The representative script delegates to loaders and normalizes legacy conditions. It does not visibly enforce the contract. It tolerates noncanonical condition names by mapping them, whereas the spec says noncanonical condition strings abort.

   The author needs to decide: either legacy normalization is allowed and documented as a preprocessing layer, or the canonical-condition abort rule is false.

5. **`--verify` does not actually locate manuscript numbers.**  
   The script uses hardcoded `PAPER_PER_SUBJECT` and `PAPER_SUMMARY` dictionaries. That is not “locates the matching number in the paper by string match or section anchor.” It is a second hand-maintained source of paper truth. That is exactly the kind of alternate path the architecture claims to eliminate.

6. **No manifest-level proof that primary data only are used.**  
   The script imports `recompute_5judge_primary` and notes that it overlays `_s114_backfills`. That may be legitimate primary data, but the contract needs to explicitly classify these files. Right now, the reader cannot tell whether the script is reading raw judgments, merged judgments, rerun judgments, or derived analysis products.

7. **No script checksum / git SHA.**  
   The script uses a literal `EMIT_DATE`, but there is no code hash or git commit. Idempotent output is useful, but provenance also needs to identify the code version.

8. **Statistical-method details are underspecified.**  
   Regression CI method, Wilcoxon tie handling, alternative hypothesis, exact/asymptotic behavior, missing-cell policy, and inclusion/exclusion of Franklin are partly embedded in code but not standardized in the contract. These are reproducibility-relevant.

9. **The `expected_n_judgments` block is not an audit.**  
   It is a prose approximation and even contains a dead `pass`. For release-grade scaffolding, expected and observed counts should be machine-computed and claim-linked.

## Where the contract still leaks

Numbers can still enter the manuscript by unmonitored paths through:

1. **Hardcoded paper-value dictionaries inside emit scripts.**  
   These become shadow manuscripts.

2. **Manual table editing.**  
   Unless the manuscript imports generated tables or embeds claim tags, a number can be manually typed and never matched correctly.

3. **Fragile paper-side extraction.**  
   The reconciliation diff already proves that the locator can attach a scaffold claim to the wrong paper number or stale running-list value.

4. **Existing non-v11 scripts.**  
   The architecture table lists existing scripts for §4.6.1, §6.3, §3.7.6. Unless those scripts are upgraded to the v11 schema/provenance/verification contract, they are legacy escape hatches.

5. **Tables, captions, appendix prose, abstract, footnotes, figure labels.**  
   A `PAPER_ONLY = 0` heuristic is not credible unless it is based on a full numeric literal census of the rendered manuscript.

6. **Derived artifacts masquerading as source.**  
   Analysis docs, merged files, rerun files, backfills, and harmonized files need explicit source-of-truth status. “Primary data JSON only” is not precise enough when there are original failed files plus rerun siblings plus merged outputs.

7. **Numbers with non-score estimands.**  
   Token counts, named-entity counts, compression ratios, corpus lengths, question counts, and citation rates are not judgment-score aggregates. They need their own declared primary inputs and validation schemas.

## Minimum architecture fixes before freeze

I would require:

- one enforced JSON Schema for all emit outputs;
- flat `claims` block for every emitted number;
- SHA-256 manifest of actual files, not glob strings;
- code hash / git SHA and dependency/environment hash;
- manuscript claim tags, e.g. `<!-- claim:4_1_slope -->`, or generated tables inserted from JSON;
- full numeric-literal census of the paper;
- no hardcoded paper values inside emit scripts;
- CI test that every manuscript number is either mapped to a claim_id or whitelisted as non-empirical;
- CI test that every claim_id has exactly one intended manuscript target or is explicitly `NON_CLAIM`;
- explicit handling of rerun/backfill/merged files as primary or derived;
- every legacy script upgraded to the v11 contract or excluded from the paper.

---

# 2. Aggregation rule

## Is the locked rule right for cross-subject claims?

Yes, for the main cross-subject score claims it is reasonable:

> per-judge × per-question score → per-judge × per-subject mean → panel mean across five judges → cross-subject analysis on subject-level panel means.

This prevents subjects with more questions from dominating cross-subject estimates. It also gives each judge equal weight within subject and each subject equal weight across subjects. For claims like:

- mean C5/C2a/C4a per subject;
- subject-level Δ;
- cross-subject regression;
- Wilcoxon over subjects;
- low-baseline subject mean;
- all-14 subject mean;

this is the right default.

## But it is not the right rule for every claim

Several paper claims need different estimands.

### 1. Per-question improvement / worsening rates

For §4.2.1 win/tie/loss tables, the estimand is question-level:

- C8 better than C2a on how many questions?
- C9 better than C4a on how many questions?
- low-baseline question-level worsening rate?

That cannot be recovered from per-subject means. The rule should be something like:

> For each subject × question × condition, compute panel mean across judges; compute paired Δ at the question level; classify win/tie/loss; then aggregate counts either pooled over questions or averaged over subjects.

The author must explicitly choose between:

- **pooled question-level rate**: each question equal weight;
- **subject-balanced rate**: compute per-subject rate, then average subjects;
- **judge-balanced question rate**: classify per judge first, then average judges.

These are different. The paper needs to declare which one is used.

### 2. §4.4.2 paired-Δ distribution

The paired-Δ mechanism table is not a cross-subject mean. It counts question-level/spec-vs-no-spec paired swings within memory systems. It needs a specific rule:

- pair by subject, question_id, system, condition pair;
- compute Δ either per judge first or after panel averaging;
- define inclusion of missing pairs;
- define large improvement/regression threshold;
- define panel used.

The locked rule is insufficient here.

### 3. Appendix D anchor crossing

Anchor-crossing claims are inherently threshold / band-transition claims at the question or subject-question level. They need explicit classification rules:

- classify before or after panel mean?
- use exact thresholds or rounded paper scores?
- pooled over questions or subject-balanced?

### 4. Judge-calibration / strictness claims

Per-judge strictness, parse failures, abstention checks, and calibration tests should not collapse across the five-judge panel. Their estimand is per-judge behavior.

### 5. Tier 2 cross-provider replication

Tier 2 is cross-provider replication. It probably needs a provider-level or model-level rule, not the five-primary-judge panel rule.

### 6. Token / compression / named-entity / citation-count claims

These are not judge-score aggregates at all. They need separate primary-data declarations and deterministic parsing/tokenization/entity-counting rules.

## Recommendation

Keep the locked rule as the **primary score-aggregate rule**, but add a table of explicitly named aggregation families:

1. `subject_panel_mean_5judge`;
2. `question_paired_panel_delta_5judge`;
3. `pooled_question_rate_5judge`;
4. `subject_balanced_question_rate_5judge`;
5. `per_judge_diagnostic`;
6. `audit_panel_6judge`;
7. `sensitivity_7judge`;
8. `nonjudgment_deterministic_count`.

Each claim should declare one of these. “Used everywhere unless explicitly noted” is too coarse for this paper.

---

# 3. Reconciliation results and sign flips

The summary says:

- 1,509 claim_ids;
- 72.2% match;
- 4.3% minor rounding;
- 13.7% substantive;
- 149 scaffold-only;
- 14 sign flips surfaced.

The advisor now says the 14 sign flips are stale running-list artifacts and that zero published-table sign flips remain after rebuild.

## Is that conclusion warranted?

Not yet as a release-freeze conclusion.

It may be true. The table-rebuild proposal gives plausible manual explanations:

- §4.1 sign flips appear to be stale regression placeholders;
- §4.3 per-subject wrong-spec sign flips were scaffold-only / never published as a table;
- §4.4.1 Wilcoxon `-0.01` is probably a bad extraction;
- §4.4.3 Keckley Q21 paper lines already match scaffold.

But the reconciliation system itself has demonstrated that it can compare scaffold values against the wrong paper-side value. Therefore the author should not treat this as settled by manual inspection alone.

## What deeper verification is needed?

Before declaring “zero published sign flips,” I would require:

1. **Regenerate the paper-side extraction from the actual current manuscript**, not from a running list.

2. **Attach every extracted number to a line/snippet/span.**  
   The diff should show:

   - claim_id;
   - scaffold value;
   - manuscript value;
   - manuscript file;
   - line number;
   - surrounding text;
   - extraction regex or claim tag.

3. **Search all manuscript locations, not only tables.**  
   Sign flips in abstract, introduction, conclusion, captions, footnotes, and appendix prose matter.

4. **Prove one-to-one mapping for sign-sensitive claims.**  
   For every claim whose scaffold value is signed, assert that all matching manuscript references have the same sign or are explicitly marked stale/nonclaim.

5. **Separate three categories:**

   - published paper claim mismatch;
   - scaffold-only claim;
   - stale running-list mismatch.

6. **Make stale running-list entries fail CI until removed or quarantined.**  
   A stale running list that pollutes reconciliation is not harmless. It directly undermines the audit.

## My judgment

The advisor’s conclusion is plausible but not yet release-grade. Treat the sign flips as **unresolved until machine-verified against the actual manuscript**.

Also: even if no published-table sign flips remain, the §4.3 per-subject wrong-spec sign flips are substantively important if the author adds the proposed per-subject table. They are not publication errors, but they are real scientific content.

---

# 4. Coverage gaps

## §4.6.1 Tier 2 is a hard release blocker

The proposal correctly flags §4.6.1 Tier 2 cross-provider replication as uncovered. That is not a minor gap. It is a whole results table with no v11 scaffold.

Worse, the panel-completeness audit CSV shows many unwaived `FULL_FAIL` rows under `results/_tier2/...`, especially GPT-5.4 judging of Tier 2 Sonnet/Gemini-Pro replication files. These are marked `waived = N`.

Under the architecture spec, unwaived `FULL_FAIL` is a release blocker. Therefore §4.6.1 cannot remain as a primary results table unless:

- a dedicated `_v11_emit_4_6_1_tier2.py` is added;
- all Tier 2 primary inputs are complete or explicitly waived;
- the table is regenerated from that emit;
- the paper discloses any remaining incompleteness.

The existing paper note saying “pending verification” is not enough for a release freeze. Either verify it or move it out of the results as preliminary/unverified.

## `PAPER_ONLY = 0` is not credible

Given the reconciliation’s locator bugs, `PAPER_ONLY = 0` should not be trusted.

The heuristic clearly missed or misclassified things. Examples from the proposal:

- running-list values mismatched actual paper lines;
- locator attached Ebers BL value to a nearby Babur co-mention;
- §4.1 regression values compared against stale placeholders;
- §4.4.3 Keckley values were already correct in paper but flagged as mismatches.

If the paper-side extractor can attach wrong values, it can also fail to find paper-only numbers.

## Expected additional coverage gaps

I would expect unmonitored numbers in:

1. abstract and introduction headline claims;
2. conclusion restatements;
3. table captions and notes;
4. appendix prose;
5. footnotes;
6. parenthetical percentages derived from counts;
7. inequalities like `p < 0.001`;
8. rounded ranges like `~7K`, `~33K`, `23×`;
9. denominators inside prose, e.g. “351 questions”;
10. figure labels, if any;
11. confidence intervals;
12. statistical test statistics;
13. token counts and compression ratios;
14. named-entity counts;
15. citation-rate numerators/denominators;
16. sensitivity/audit-panel numbers;
17. calibration and diagnostic numbers in §3;
18. waiver counts and failure counts.

## Required fix

Do a full numeric literal census:

- parse the rendered markdown/manuscript;
- extract every numeric literal, signed number, percentage, p-value, ratio, range, and approximate count;
- ignore only whitelisted non-empirical numerics: section numbers, dates, model names, version numbers, citation years, etc.;
- require every empirical numeric to map to a claim_id;
- require every claim_id to map to a manuscript occurrence or be marked `scaffold_only`.

Until that exists, `PAPER_ONLY = 0` should be considered false reassurance.

---

# 5. Tier 1 / 2 / 3 application order

The proposed order is:

1. silent cleanup;
2. minor drift;
3. substantive author-decision changes.

That is directionally right, but the tier assignments need tightening.

## Correct principle

The order should be:

1. **Fix the verification machinery first.**  
   Remove stale running-list artifacts, fix paper extraction, add claim tags, regenerate the diff.

2. **Then apply safe no-op / exact-match cleanup.**

3. **Then apply minor numeric drift.**

4. **Then resolve substantive scientific or estimand changes.**

5. **Then rerun the full scaffold and paper census from scratch.**

The current proposal jumps too quickly from “manual inspection says stale artifact” to “silent cleanup.” That is dangerous.

## Items I would elevate to Tier 3 / release-blocking

### §4.6.1 Tier 2

Hard Tier 3 / release blocker. No scaffold coverage plus unwaived `FULL_FAIL` audit rows.

### §4.4.2 panel asymmetry

Tier 3. This is not a typo. It is an estimand choice: 5-judge primary vs 6-judge audit panel. Needs author decision and explicit declaration.

### §4.3 wrong-spec random-derangement aggregate

The +0.22 → +0.15 shift is not huge, but it touches a key interpretive claim. Tier 3 or at least high Tier 2. The paper should not silently change a central wrong-spec estimate.

### §4.2 token/compression convention

The `~7K` / actual per-subject token count issue is structural. If the table header implies a shared token count but actual counts vary from 4,478 to 7,349, that needs explicit footnote or table redesign.

### Appendix B narrative drifts

The repeated `+1.71` placeholder pattern and Hamerton axis claims need human review. These are not mere rounding.

### Panel-completeness failures

Any unwaived primary-panel `FULL_FAIL` or `SUSPECT` used by an emit is a release blocker.

## Items that can be Tier 1 only after machine proof

- §4.1 stale regression placeholders;
- §4.4.1 Wilcoxon `-0.01`;
- §4.4.3 Keckley Q21 stale deltas;
- Letta locator bugs;
- Appendix D running-list placeholders.

But only after a regenerated manuscript-span diff proves the paper text already matches scaffold.

---

# 6. §4.4.2 panel asymmetry

The §4.4.2 paired-Δ table is currently declared as using a 6-judge audit panel. Under strict 5-judge primary, n shifts from 507/516 to 546/545 and percentages shift by roughly 1–2 pp, while some counts shift more substantially.

## Recommendation: rebuild the main table on the 5-judge primary panel

Because the architecture contract says the five-judge panel is primary “used everywhere unless explicitly noted,” and because §4.4.2 is a main results table, I would rebuild it on the 5-judge primary panel.

Then include the 6-judge audit panel as:

- a footnote;
- a sensitivity row;
- or an appendix table.

## Why I would not keep the audit panel as the main table

Keeping it as the main table creates three problems:

1. **Comparability problem.**  
   Readers will compare §4.4.2 to §4.4.1, §4.1, §4.2, etc. If one central table silently uses a different panel, interpretation becomes brittle.

2. **Contract problem.**  
   The v11 architecture’s purpose is to eliminate ad hoc aggregation. A main table on a different panel undermines that unless the deviation is strongly justified.

3. **Audit/reproducibility problem.**  
   The reconciliation will continue to flag the whole section as mismatched unless the emit explicitly declares `aggregation_rule = audit_panel_6judge` and the paper is tagged accordingly.

## Acceptable alternative

If the author insists on keeping the 6-judge audit panel, the table must have an explicit footnote like:

> This table uses the 6-judge audit panel [list judges], not the 5-judge primary panel used elsewhere. Under the primary 5-judge panel, paired n = 546 for Supermemory/Mem0/Zep/Base Layer and 545 for Letta archival; percentages shift by approximately 1–2 pp. Full 5-judge values are reported in Appendix X.

And the emit script must emit those numbers with a declared non-primary aggregation rule. No implicit exception.

But my preferred choice is: **5-judge in main, 6-judge in sensitivity.**

---

# 7. Robustness of GPT-5.x judge-call controls

## Dispatcher pattern

The shared `_judge_invocation` dispatcher is a good idea and should be mandatory. Centralizing provider invocation is exactly the right response to the GPT-5.4 `max_tokens` / `max_completion_tokens` failure.

But the provided `__init__.py` alone does not prove the control is sufficient. The critical logic is in `openai_judge_call.call_openai_judge`, which is not shown. The dispatcher only routes calls; it does not itself show that GPT-5.x uses `max_completion_tokens`.

## Current strengths

- single public `call_judge` path;
- provider inference by model prefix;
- explicit public result fields including `param_used`;
- architecture bans hand-rolled HTTP calls;
- preflight health probe;
- panel-completeness audit;
- waivers mechanism.

These are all good.

## Weaknesses

1. **Prefix routing can become stale.**  
   Future OpenAI model IDs may not match `gpt-`, `o1`, or `o3`. The system needs tests for all configured model IDs, not only prefixes.

2. **One health prompt is not enough.**  
   A single canonical rubric prompt catches gross endpoint failure, but not:
   - long-context failures;
   - batch-size failures;
   - timeout/rate-limit behavior;
   - parsing failures on realistic outputs;
   - provider-specific safety/refusal behavior;
   - wrong max-token parameter under unusual kwargs.

3. **Preflight must use the exact batch code path.**  
   If the preflight calls `call_judge` but batch scripts use a wrapper or old path, the control fails. CI grep helps, but import-level enforcement is better.

4. **Panel-completeness audit currently shows unresolved failures.**  
   The CSV contains many unwaived `FULL_FAIL` rows:
   - Tier 2 GPT-5.4 replication files;
   - Base Layer C1/C3 files for primary judges;
   - C8/C9 files in some subjects;
   - Gemini files.

   Under the spec, unwaived `FULL_FAIL` means release blocker. So the audit is a good guard, but the current audit output is not green.

5. **Waivers need replacement-file validation.**  
   The wrong-spec-v2 waivers say rerun siblings are authoritative. The emit scripts must prove they read the rerun files, not the failed originals. The waiver should include the replacement path and checksum.

6. **CI ban on hand-rolled calls must be real.**  
   The spec says hand-rolled `httpx.post` calls are a CI failure. That needs an actual test that scans for:
   - `api.openai.com`;
   - `httpx.post`;
   - `requests.post`;
   - direct OpenAI SDK calls;
   - provider SDK calls outside `_judge_invocation`.

## Required judge-control additions

I would require:

- unit tests over all configured model IDs asserting parameter selection;
- integration dry-run per provider/model using the exact batch function;
- result logs storing `param_used`, request ID, prompt hash, model, score, parse status;
- CI grep banning direct provider calls outside the shared module;
- panel-completeness audit scoped to actual emit inputs;
- release failure on any unwaived `FULL_FAIL`/`SUSPECT` used by an emit;
- waiver schema with replacement file path and replacement checksum;
- emit-time assertion that failed original files are not read when waived in favor of reruns.

---

# 8. What I would push back on as a NeurIPS / ICLR D&B methodology referee

If I were reviewing this as methodology/reproducibility infrastructure, I would push back hard on the following.

## 1. The implementation does not satisfy the stated architecture

The spec is strong; the representative script is not compliant. Missing flat claims, missing checksums, missing schema validation, missing per-number provenance, and hardcoded paper values are not small issues.

I would require conformance before accepting the scaffolding as evidence.

## 2. The paper-side reconciliation is not trustworthy yet

The system produced stale sign flips and wrong paper-value matches. That means the central claim “every paper number is accounted for” is not established.

I would require claim tags or generated tables plus a numeric-literal census.

## 3. §4.6.1 is uncovered

A whole results table has no v11 scaffold coverage. The audit CSV also shows unwaived Tier 2 failures. That is an automatic release blocker.

## 4. Panel completeness is not green

The architecture says unwaived `FULL_FAIL` or `SUSPECT` cells block release. The ancillary CSV contains many unwaived `FULL_FAIL` rows. The author must either:

- rerun and replace;
- prove those files are not in any emit input;
- or remove/waive with explicit justification.

Right now, the audit contradicts release readiness.

## 5. Aggregation rules are underspecified for non-cross-subject claims

The locked aggregation rule is fine for subject-level score means, but not for all paper claims. Per-question, per-pair, per-judge, audit-panel, sensitivity-panel, token-count, named-entity, and citation-count claims need separate declared rules.

## 6. The 6-judge §4.4.2 main table undermines the primary-panel contract

I would require the main table to use the 5-judge primary panel, with the 6-judge audit panel moved to sensitivity, unless the authors give a strong methodological reason.

## 7. Legacy scripts are escape hatches

Existing scripts listed in the architecture need to be upgraded to v11 emit compliance. Otherwise the architecture is not paper-wide.

## 8. “Primary data” is ambiguous

The system has original files, harmonized files, merged files, backfills, rerun siblings, and analysis outputs. The paper needs a data lineage graph:

- raw call logs;
- parsed judgment JSON;
- rerun replacements;
- merged/harmonized files;
- emitted claims.

Without that, “primary-data JSON only” is not sufficiently precise.

## 9. Waivers are too informal

Waivers should be machine-actionable and tied to replacement checksums. A prose reason is not enough.

## 10. Statistical reproducibility needs more detail

The emits should record:

- scipy/stats versions;
- regression method;
- CI method;
- Wilcoxon exact/asymptotic/tie handling;
- rounding convention;
- missing-data policy;
- threshold definitions;
- subject inclusion rule.

---

# Final recommendation

Do **not** freeze v11 yet.

I would require the author to close these before release:

1. Add a dedicated v11 emit for §4.6.1 Tier 2 or remove/mark the table as preliminary.
2. Make every emit comply with the declared JSON schema: flat `claims`, per-number provenance, checksums, schema validation.
3. Remove hardcoded paper-value dictionaries from emit scripts.
4. Add manuscript claim tags or generated tables.
5. Run a full numeric-literal census and prove `PAPER_ONLY = 0`.
6. Regenerate sign-flip verification against actual manuscript spans, not running-list artifacts.
7. Resolve §4.4.2 panel choice; preferably rebuild on 5-judge primary.
8. Make panel-completeness audit green for all emit inputs.
9. Validate that waived failed files are not read and rerun files are checksum-pinned.
10. Upgrade legacy scripts to the v11 contract.

The architecture is promising, but the current state is not yet the “no undocumented path” system it claims to be.