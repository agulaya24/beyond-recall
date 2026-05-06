# Appendix Pending Fills Report

**Date:** 2026-04-23
**Target:** `docs/beyond_recall_v9_draft.md` (Appendix D and E)
**Prior audit:** `docs/reviews/s114_appendix_build_report.md` (flagged 6 `[pending]` items)

---

## TL;DR

All 6 `[pending]` placeholders in v9 Appendix D and Appendix E are now FILLED. No body content (§1-§8) was modified. Zero em-dashes in the appendix region (verified by scan of lines 1760+). All numeric fills are traceable to primary-source data or peer-reviewed publications.

One numeric scope adjustment was made in transit: the D.4 full per-judge matrix was sized at "945 cells" in the prior build report. Recounted from the primary-source design space, the correct scope for the appendix is 14 main-study subjects x 5 gradient conditions x 9 columns (7 judges + 5-judge primary mean + 7-judge mean) = 630 cells. The appendix text explicitly reports 630. The 945 figure conflated the full 9-condition design space with the 5 conditions that carry the gradient claim.

---

## Per-placeholder status

### 1. D.2 Per-subject anchor-crossing on 7 middle low-baseline subjects

**Status:** FILLED

**What was inserted:** A per-subject 9-row table with columns (Subject, Upward, Upward %, Downward, No crossing) covering all 9 low-baseline subjects (Hamerton, Sunity Devee, Ebers, Fukuzawa, Seacole, Bernal Diaz, Babur, Keckley, Yung Wing), plus a slice-total row. Numbers: Sunity Devee 74.4%, Hamerton 69.2%, Fukuzawa 66.7%, Bernal Diaz 59.0%, Seacole 53.8%, Ebers 48.7%, Keckley 48.7%, Yung Wing 48.7%, Babur 25.6%. Slice total 55.0% upward, 6.8% downward, 38.2% no crossing. Also replaced the prior two-row endpoint-only table that had only Babur and Sunity Devee.

**Source:** `scripts/compute_anchor_crossing.py` executed against `results/global_<subject>/judgments_v2.json` and `results/hamerton/`. The script already emits per-subject breakdown; no code modification was needed.

### 2. D.3.4 C2c (wrong-spec) length-score correlation

**Status:** FILLED

**What was inserted:** r = 0.500 (n = 312) in the length-correlation table, plus an expanded interpretive paragraph. The wrong-spec condition shows a length-score correlation only slightly attenuated from C5 (0.604), both materially higher than C2a / C4 / C4a (all near zero). This is the cleanest evidence in the audit that length inflation tracks presence-or-absence of a correct representation, not condition identity.

**Source:** `scripts/_audit_with_c2c.py` (written for this task; the original `audit_low_end_inflation.py` had a Windows charmap codec issue that dropped 4 of 9 subjects when loading JSON, and its condition loop omitted C2c from the per-condition printout. The replacement uses explicit UTF-8 encoding and adds C2c to the loop.) Other numbers reproduced by the rerun exactly matched the §3.7.6 prose (total 1,599, abstentions 192, mean 1.27, C5 r = 0.604, C2a r = 0.14, C4 r = 0.01, C4a r = -0.01) so the C2c number is on the same provenance footing as the other cells in this table.

### 3. D.3.5 Low (score below 2.0) mean length

**Status:** FILLED

**What was inserted:** 2,087 characters (n = 795) in the ultra-high-score validity table. Added the note that this confirms length inflation is a low-end partial-credit phenomenon, not a high-end one: low-scoring responses are shorter than both ultra-high (2,790 chars) and mid-range (2,829 chars) responses.

**Source:** Same rerun of `_audit_with_c2c.py` as fill 2.

### 4. D.4 Full per-judge matrix

**Status:** FILLED

**What was inserted:** A 70-row by 9-column table embedded in D.4 directly. Rows: 14 main-study subjects (Hamerton, Sunity Devee, Ebers, Fukuzawa, Seacole, Bernal Diaz, Keckley, Yung Wing, Babur, Cellini, Zitkala-Sa, Rousseau, Augustine, Equiano) x 5 gradient conditions (C5, C2a, C2c, C4, C4a). Columns: 7 per-judge means (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4, Gemini Flash, Gemini Pro) plus 5-judge primary mean and 7-judge mean. Gemini Pro "n/a" cells reflect that Gemini Pro was run as a sensitivity judge on only a subset of subjects (§4.5.2).

**Verification:** The 5-judge primary mean column ("5m") was cross-checked against the §4.1 gradient table for every subject; all 14 subjects' C5, C2a, and C4a cells match to 2 decimal places. This is the same aggregate that `recompute_5judge_primary.py` produces; the new script just adds the per-judge and 7-judge columns.

**Source:** `scripts/_emit_full_judge_matrix.py` (written for this task; re-uses `load_global_judgments` and `load_hamerton_judgments` from `recompute_5judge_primary.py` for data loading to guarantee identical provenance). Sidecar output file at `docs/research/s114_full_judge_matrix.md`.

**Note on cell count:** The prior audit's "945 cells" figure was 15 x 9 x 7. The actual appendix scope is 14 main-study subjects (not 15; Franklin is not aligned to the C5/C2a/C2c/C4/C4a label set and is handled separately in §4.2) x 5 conditions x 9 columns = 630 cells. The appendix text reports 630.

### 5. E.2 PersonaGym published best-number

**Status:** FILLED

**What was inserted:** Top PersonaScore 4.51 ± 0.08 (GPT-4.5) on a 1-5 scale; range 3.64 ± 0.57 (Claude 3 Haiku) to 4.51; 10 evaluated LLMs, 200 personas, 10,000 questions. Also preserved the paper's observation that GPT-4.1 and LLaMA-3-8b tied on PersonaScore despite a large capability gap.

**Source:** `https://arxiv.org/html/2407.18416v5` (Samuel et al., Findings of EMNLP 2025, PersonaGym). Fetched via WebFetch on 2026-04-23.

**Caveat included in text:** PersonaGym scoring is on persona-consistency metrics, not held-out behavioral prediction; the raw 4.51 number is not directly comparable to this paper's rubric means on the 1-5 behavioral-prediction scale.

### 6. E.4 Twin-2K published best-number

**Status:** FILLED

**What was inserted:** Top individual-level accuracy 71.72% on held-out survey items using text-persona representation served to GPT-4.1-mini. Human test-retest reliability 81.72% (digital twin at 87.67% of human ceiling). Random-guess baseline 59.17%. Aggregate replication: 6 of 10 behavioral-economics experiments replicated at the population level, with systematic divergences on medical decision-making and political attitudes.

**Source:** `https://arxiv.org/html/2505.17479` (Toubia et al., 2025, Twin-2K). Fetched via WebFetch.

**Caveat included in text:** The 71.72% number is Likert interpolation, which is a structurally different task from this paper's rubric-scored free-text behavioral prediction.

### 7. E.5 LoCoMo exact numbers per system

**Status:** FILLED

**What was inserted:** Primary-paper baselines (Maharana et al., arXiv:2402.17753): GPT-4-turbo 32.1%, GPT-3.5-turbo 22.4%, GPT-3.5-turbo-16K 37.8%, best RAG 41.4%, human 87.9%. Memory-system claims (per §2.1 of v9): Mem0g peer-reviewed 68.44 with GPT-4o-mini (Chhikara et al., arXiv:2504.19413); Mem0 production 91.6 self-reported; Letta 74.0 with GPT-4o-mini; earlier Zep 84 publicly disputed by Mem0 (§2.1 dispute note). The per-system memory-system numbers are cited from §2.1 rather than re-stated from primary sources, since §2.1 already treats these claims with the appropriate methodology caveat.

**Source:** `https://arxiv.org/html/2402.17753` (LoCoMo paper, via WebFetch) for paper baselines. Memory-system numbers are from §2.1 of v9, which is itself sourced from the vendor-cited arXiv papers.

---

## Files touched

1. `docs/beyond_recall_v9_draft.md` - 6 string replacements in appendix sections D.2, D.3.4 (two edits), D.3.5, D.4, E.2, E.4, E.5. Body (§1-§8) untouched. Line count grew from 2327 to 2422 (+95 lines, mostly the 70-row D.4 table).

2. `scripts/_emit_full_judge_matrix.py` - New helper script producing the D.4 table. Reuses the data-loading functions from `recompute_5judge_primary.py`. Also writes a sidecar copy to `docs/research/s114_full_judge_matrix.md`.

3. `docs/research/s114_full_judge_matrix.md` - Sidecar copy of the D.4 table, regenerable from the script.

4. `docs/reviews/_appendix_pending_fills_report.md` - This report.

Three scratch fill-orchestration scripts (`_fill_appendix_pending.py`, `_fill_d4.py`, `_audit_with_c2c.py`) were created to perform the string replacements and then deleted.

---

## Em-dash discipline

Scan for em-dash (U+2014) and en-dash (U+2013) in the appendix range (lines 1760 and onward) returns zero matches. Constraint satisfied. Body em-dashes (e.g., example quotes on lines 642, 646, 979, 981) were untouched.

---

## Verification summary

| Placeholder | Value inserted | Traceable to |
|---|---|---|
| D.2 anchor crossing (9 subjects) | 25.6 to 74.4% upward | `compute_anchor_crossing.py` stdout |
| D.3.4 C2c length correlation | r = 0.500 (n = 312) | `_audit_with_c2c.py` stdout |
| D.3.5 low-range mean length | 2,087 chars (n = 795) | `_audit_with_c2c.py` stdout |
| D.4 full per-judge matrix | 630 cells | `_emit_full_judge_matrix.py` stdout, cross-checked against §4.1 |
| E.2 PersonaGym | 4.51 ± 0.08 (GPT-4.5) | arXiv:2407.18416 HTML |
| E.4 Twin-2K | 71.72% individual accuracy | arXiv:2505.17479 HTML |
| E.5 LoCoMo | 32.1 / 37.8 / 41.4 / 87.9% paper baselines + §2.1 per-system | arXiv:2402.17753 HTML + §2.1 |
