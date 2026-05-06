# Full Data Audit — Beyond Recall
_Generated: 2026-04-21 (S114), read-only audit of `memory-study-repo/results/` + referenced external data_

## Executive Summary

- **Clean for gradient headline numbers.** All 14 subject C5/C2a/C4a gradient numbers in DATA_REFERENCE §1 and paper Table 4.1 reproduce exactly from `RESULTS_S113.json` aggregates. Battery files exist and checksum-distinct across all 13 globals + Hamerton + Franklin at 80 total / 39 or 40 behavioral-prediction questions.
- **Clean for Letta stateful block dimensions.** Hamerton 22,472 / Ebers 68,413 / Babur 335,349 chars — exact match to paper §4.3.1 and DATA_REFERENCE §7.
- **BLOCKER — canonical aggregate JSON is not in the public study repo.** `RESULTS_S113.json`, cited by DATA_REFERENCE §K as the single source for every paper number, lives at `memory_system/data/experiments/memory_systems/results/RESULTS_S113.json` — NOT inside `memory-study-repo/`. A Tuesday public clone cannot reproduce DATA_REFERENCE.
- **BLOCKER — Tier 2 data is not in the public study repo.** Paper §3.6 says raw Tier 2 files live at `results/_tier2/`. That directory does not exist. All 6 Tier 2 (subject × response model) result + 6-judge judgment files are at `memory_system/data/experiments/memory_systems/results/global_<subj>/tier2_<model>_*.json`, outside the repo.
- **BLOCKER — wrong-spec v2 data is not in the public study repo.** DATA_REFERENCE §K cites per-subject `wrong_spec_v2_*` files; all 13 subjects' wrong_spec_v2 results + judgments live at `memory_system/data/experiments/memory_systems/results/global_<subj>/wrong_spec_v2_*.json`, outside the repo.
- **HIGH — 12 of 13 globals have 0 valid gpt4o / gpt5.4 / gemini-flash baselayer judgments.** All baselayer_judgments_* files for these three judges on C1_baselayer + C3_baselayer are rate-limit (429) parse failures stored as `score: 0, parse_failure: true`. The paper's reported Base Layer controlled mean Δ = +0.12 (DATA_REFERENCE §3) cannot be reproduced from raw study-repo judgments; recomputing with haiku+sonnet+opus only gives +0.084. Only zitkala_sa and hamerton have full 6-judge baselayer coverage.
- **HIGH — DATA_REFERENCE §10 Tier 2 deltas disagree with RESULTS_S113.json Tier 2 deltas.** Paper and `figures/generate_fig11_tier2_replication.py` use DATA_REFERENCE §10 values (Ebers/Sonnet +1.48, Ebers/Gemini Pro +1.07, etc.); RESULTS_S113.json `tier2_circularity.per_cell` has different numbers (+1.19, +0.03, etc.). Source of the discrepancy must be resolved before §4.8 is drafted.
- **HIGH — aggregation method ambiguity.** Paper §3.7.5 specifies the 5-judge primary panel (h/s/o/gpt4o/gpt54, no Gemini) but the Table 4.1 / DATA_REFERENCE §1 numbers match 6-judge (adds gemini-flash), not 5-judge. Choice must be made explicit before §4 drafting.
- **MEDIUM — score=0 for parse failures propagates through memory-system merged files.** 16 subject×system cells in `*_judgments_merged.json` contain 5-102 score=0 parse_failure rows that inflate zero-density in naive means. Any aggregator that does not filter on `parse_failure == true` or `score > 0` will produce wrong numbers.
- **MEDIUM — 2 JSON files require non-UTF-8 decoding.** `results/judge_calibration/results.json` and `results/multimodel/gpt54_hamerton.json` are cp1252-encoded. They parse successfully under latin-1 but will break strict UTF-8 pipelines.
- **CLEAN — 4 of 5 memory system aggregates reproduce.** Controlled mean Δ recomputed from study repo raw data: Mem0 +0.149 (paper +0.15), Letta +0.246 (paper +0.25), Zep +0.220 (paper +0.22), Supermemory −0.039 (paper −0.04) — all within 0.01 of the paper once `parse_failure == true` rows are filtered. **Base Layer +0.084 (paper +0.12) does NOT reproduce** — study-repo baselayer judgments are effectively 3-judge on 12 of 13 globals.
- **NOTE — Hamerton 3-judge backfill (sonnet/opus/gpt4o on full-stack conditions) is in flight, per the user brief. Do not treat as a gap.** The missing gpt4o for C2a_full_spec / C2c_full_wrong_spec / C3_full_mem0 / C3_full_supermemory / C4a_full_all_facts_plus_spec is this known backfill.

---

## 1. Per-subject file inventory

Standard per-global-subject inventory (111 files). All 13 globals have the same structure. `results/global_<subject>/`:

**Ground-truth + spec + battery (7 files):**
- `battery.json`, `battery_v2.json`, `battery_gpt54.json`, `facts.json`, `heldout.txt`, `spec.md`, `results.json` (legacy), `results_v2.json` (primary responses across 5 direct conditions).

**Spec-effect judgments (3 files):** `judgments.json` (legacy), `judgments_v2.json` (5 conditions × 6 judges × 39 Q), + optional `judgments_v2_gemini_pro2.json` and `judgments_v2_gemini_pro_key2.json` (gemini_pro only, augustine-babur-bernal_diaz only).

**C8/C9 raw corpus (9 files):** `c8_c9_results.json`, `c8_c9_judgments_<judge>.json` × 6, `c8_c9_judgments_merged.json`.

**Memory systems (5 systems × 2 configs × 11 files = 110 files):** per `{system}` ∈ {mem0, letta, supermemory, zep, baselayer} × `{cfg}` ∈ {'', '_fullpipeline'}:
- `{system}{cfg}_ingestion.json` (except baselayer: `baselayer_retrieval.json` instead)
- `{system}{cfg}_extracted.json` (fullpipeline only; written by Mem0/Letta/SM/Zep native ingestion)
- `{system}{cfg}_retrieval.json`
- `{system}{cfg}_results.json`
- `{system}{cfg}_judgments_{judge}.json` × 6 judges
- `{system}{cfg}_judgments_merged.json`

**Totals by subject:**
- global_augustine: **113** files (base 111 + `judgments_v2_gemini_pro2.json` + `judgments_v2_gemini_pro_key2.json`)
- global_babur, ...equiano, fukuzawa, keckley, rousseau, seacole, sunity_devee, yung_wing, zitkala_sa: **111** files (base set)
- global_bernal_diaz, global_ebers, global_cellini: **111** (no gemini_pro extras — gemini_pro only scored 3 subjects)
- hamerton: **111** files. **No `battery.json` / `battery_v2.json` / `battery_gpt54.json` / `facts.json` / `heldout.txt` / `spec.md` in results/hamerton/ — they live in `data/hamerton/` (not `results/hamerton/`).** Hamerton has additional files: `fullstack_haiku.json`, `gemini_pro_judgments.json`, `gpt54_judgments.json`, `opus_judgments.json`, `sonnet_judgments.json`, `judgments_harmonized.json`, `results_harmonized.json` — artifacts of the phased judgment backfill.
- franklin: **3** files only (`fullstack_haiku.json`, `gemini_pro_judgments.json`, `judgments.json`). Full memory-system and spec conditions are not in `results/franklin/`; battery + facts + analysis live in `data/franklin/`.
- franklin_obscure: **1** file only (`fullstack_haiku.json`). Battery + facts in `data/franklin_obscure/`.

**Flag:** Hamerton / Franklin / Franklin_obscure split between `data/<subj>/` (ground truth) and `results/<subj>/` (model output) — unlike globals, which co-locate everything under `results/global_<subj>/`. Not a bug, but a consistency note that consumers of the public release will trip over.

**Additional non-subject files under `results/`:**
- `letta_manifest.json`, `letta_analysis.json`, `mem0_manifest.json`, `mem0_analysis.json`, `supermemory_manifest.json`, `supermemory_analysis.json`, `zep_manifest.json`, `zep_analysis.json` — system-level aggregates. No `baselayer_analysis.json` file exists; asymmetric.
- `multimodel/` — 3 files (`gemini_hamerton.json`, `gpt54_hamerton.json`, `sonnet_hamerton.json`, each Hamerton 80-question response files from Tier 2 response models).
- `judge_calibration/` — 5 files (haiku/gemini_pro/gpt4o/gpt5.4 calibration + combined results.json + judgments.json).

---

## 2. Response coverage matrix

Extracted by counting `responses` keys in `results_v2.json` (globals), `results.json` + `c8_c9_results.json` + `{system}{cfg}_results.json` (Hamerton), and `judgments.json` (Franklin).

| Subject | C5 | C2a | C2c | C4 | C4a | C8 | C9 | C1_mem0 | C3_mem0 | C1_mem0_fp | C3_mem0_fp | C1_letta | C3_letta | C1_letta_fp | C3_letta_fp | C1_supermemory | C3_supermemory | C1_supermemory_fp | C3_supermemory_fp | C1_zep | C3_zep | C1_zep_fp | C3_zep_fp | C1_baselayer | C3_baselayer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| augustine | ✓ 39 | ✓ 39 | ✓ 39 | ✓ 39 | ✓ 39 | ✓ 39 | ✓ 39 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| babur | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ 38* | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| bernal_diaz | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| cellini | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ebers | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| equiano | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| fukuzawa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| keckley | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| rousseau | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| seacole | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| sunity_devee | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| yung_wing | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| zitkala_sa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| hamerton | ✓ | ✓ (full+) | ✓ | ✓ | ✓ (full+) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| franklin | ✗ | ✓ (full) | ✓ (full_wrong) | ✗ | ✓ (full) | ✗ | ✗ | ✗ | ✓ (C3_full_mem0) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ (C3_full_supermemory) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

All 13 globals have 25 conditions × 39 questions responded.

**Gaps:**
- **babur C9_raw_corpus_plus_spec: 38 of 39 questions** (1 question missing) — confirmed. Judgments reflect same 38.
- Franklin has 5 conditions (C2a_full_spec, C2c_full_wrong_spec, C3_full_mem0, C3_full_supermemory, C4a_full_all_facts_plus_spec) × 40 questions. No standalone C1 / memory-system controlled / native configs / C8 / C9 for Franklin. This is intentional per the paper (Franklin is known-figure control), but the "C1 Franklin" statements anywhere in the paper (there are none that I found) would be unsupported.
- Hamerton has the 25-condition global matrix PLUS 5 "full-stack" variants (C2a_full_spec, C2c_full_wrong_spec, C3_full_mem0, C3_full_supermemory, C4a_full_all_facts_plus_spec at 80-question coverage in `results.json`). All present.
- Tier 2 response files (Sonnet and Gemini Pro responses on Ebers/Yung Wing/Zitkala-Sa against GPT-5.4 batteries) are **not in the study repo**; see §9 below.

---

## 3. Judgment coverage matrix

Counting `score != null AND NOT (score == 0 AND parse_failure == true)`.

**Global subjects, main gradient + wrong-spec conditions (C5, C2a, C2c, C4, C4a)** — expected: 39 per (condition, judge).

All 13 globals: **39 / 39 on haiku, sonnet, opus, gpt4o, gpt5.4, gemini-flash** for all 5 conditions. Gemini Pro coverage is partial, as expected per DATA_REFERENCE §9:

| Subject | gemini_pro on C5/C2a/C2c/C4/C4a |
|---|---|
| augustine | 40 per condition (there's 1 duplicate row per condition across the two gemini_pro side-files) |
| babur | 23 per condition (partial) |
| bernal_diaz | 10 per condition (partial) |
| All other 10 globals | 0 (none) |

**Global subjects, memory-system + C8/C9 conditions (20 conditions)** — expected: 39 per (condition, judge) on 6 judges.

- haiku, sonnet, opus: all 39 on all conditions on all 13 globals (except 3 small 1–7 gpt4o gaps on letta — documented below).
- **gpt4o on letta conditions (controlled):** 4 subjects have 1–7 missing: cellini C3_letta (38), fukuzawa C1_letta (38), rousseau C1_letta (36), rousseau C3_letta (35), augustine C3_letta (37), zitkala_sa C1_letta (38), zitkala_sa C3_letta (37). Cause: sporadic OpenAI 429s, not structural.
- **gpt4o, gpt5.4, gemini-flash on baselayer (C1_baselayer + C3_baselayer):** 0/39 valid on 11 of 13 globals (augustine, babur, bernal_diaz, cellini, ebers, equiano, fukuzawa, keckley, rousseau, seacole, sunity_devee, yung_wing) — ALL rows are rate-limit 429 parse failures stored as score=0. Only **zitkala_sa** (all 6 judges clean) and **hamerton** (all 6 judges clean) have full baselayer judgment coverage. **This is a serious gap; see §6 and §11 for implications.**
- **gpt4o, gpt5.4, gemini-flash on C8_raw_corpus (babur, bernal_diaz, rousseau only) and C9_raw_corpus_plus_spec (bernal_diaz, rousseau only):** 0/39 — same 429 pattern.
- **supermemory parse failures (controlled and fullpipeline):** widespread, all 6 judges per cell — 11 subjects have 6-198 score=0 parse-failure rows concentrated on particular questions. supermemory_fullpipeline files also have the 4-subject ingestion failure (C1=0 on babur, bernal_diaz, cellini, rousseau) — consistent with DATA_REFERENCE §3 note about "4 subjects failed free-tier ingestion."

**Hamerton — main gradient (C4_factdump, C5_baseline)** (from `judgments_harmonized.json`):
- haiku, sonnet, opus, gpt4o, gpt5.4, gemini-flash, gemini-pro: all 39 / 39.

**Hamerton — full-stack conditions (C2a_full_spec, C2c_full_wrong_spec, C3_full_mem0, C3_full_supermemory, C4a_full_all_facts_plus_spec)**:
- haiku, gemini-flash (from `judgments.json` wide-format, `gemini_score` column): 39 / 39 each.
- sonnet (from `sonnet_judgments.json`): 39 / 39 on all 5 conditions.
- opus (from `opus_judgments.json`): **38 / 39** on all 5 conditions (1 missing, same question across conditions).
- gpt5.4 (from `gpt54_judgments.json`): 39 / 39.
- gemini-pro (from `gemini_pro_judgments.json`): 39 / 39.
- **gpt4o: 0 / 39 on all 5 full-stack conditions. This is the known in-flight backfill per the user brief. Not flagged.**

**Hamerton — memory-system + C8/C9 conditions:** All 6 judges (non-gemini-pro) at 39 / 39. Gemini-pro not run on these (matches DATA_REFERENCE §9).

**Franklin (40 questions):**
- haiku, gemini-flash: 40 / 40 on all 5 conditions.
- gemini-pro: 40 / 40 on all 5 conditions.
- **sonnet, opus, gpt4o, gpt5.4: 0 / 40 across all conditions — no judgment files exist.** Franklin was judged by only 3 of 7 judges. This may be expected (Franklin as known-figure control, lean judge panel), but worth stating explicitly in the paper.

---

## 4. JSON integrity

**Parse summary:** 1,436 `.json` files under `results/` across 17 subject directories plus top-level. All parse successfully after encoding fallback.

**Strict UTF-8 parse failures (2 files — both cp1252-encoded; parse cleanly under latin-1):**

| File | Encoding | Cause |
|---|---|---|
| `results/judge_calibration/results.json` | cp1252 | `byte 0x97` (em-dash) at position 855 |
| `results/multimodel/gpt54_hamerton.json` | cp1252 | `byte 0x92` (right single quote) at position 288 |

Impact: Any tooling using default UTF-8 (e.g., the study knowledge index builder, Python 3's default `open()` on Windows) will crash on these. Fix: re-save as UTF-8.

No JSON schema errors (malformed JSON) found.

---

## 5. Battery consistency

All 14 subjects have batteries with the expected structure: 80 total questions split into 5 tiers (behavioral_prediction, recall, inferential, adversarial_abstention, boundary_probing).

**Global subjects (source: `results/global_<subj>/battery_v2.json`):**

| Subject | Total | behavioral_prediction | Checksum (first 10) | battery_gpt54.json present |
|---|---:|---:|---|---|
| augustine | 80 | 39 | 0df30b0743 | ✓ |
| babur | 80 | 39 | f814c9ea19 | ✓ |
| bernal_diaz | 80 | 39 | cd7dec92cb | ✓ |
| cellini | 80 | 39 | b91d467776 | ✓ |
| ebers | 80 | 39 | 3f0826c61f | ✓ |
| equiano | 80 | 39 | 5de72ad3e3 | ✓ |
| fukuzawa | 80 | 39 | b2afa02b0c | ✓ |
| keckley | 80 | 39 | 3d3cdaebd7 | ✓ |
| rousseau | 80 | 39 | 7d81bea5b2 | ✓ |
| seacole | 80 | 39 | b3d77fb63d | ✓ |
| sunity_devee | 80 | 39 | 6f2a0a381b | ✓ |
| yung_wing | 80 | 39 | 75832e2d73 | ✓ |
| zitkala_sa | 80 | 39 | 8e8a5e4684 | ✓ |

All 13 checksums are distinct (no copy-paste across subjects). All 13 `battery_gpt54.json` files exist (Control 1 coverage confirmed).

**Hamerton + Franklin (source: `data/<subj>/battery.json`):**

| Subject | Total | behavioral_prediction |
|---|---:|---:|
| hamerton | 80 | **39** |
| franklin | 80 | **40** |
| franklin_obscure | 80 | 40 |

Franklin has 40 behavioral-prediction questions (not 39). The paper and DATA_REFERENCE consistently describe Franklin as 40-question; matches.

**GPT-5.4 regenerated batteries (Control 1):** All 13 global subjects have `battery_gpt54.json`. Hamerton and Franklin do NOT have `battery_gpt54.json`, and per paper §3.6 lines 319 they were intentionally excluded from Control 1. Consistent.

---

## 6. DATA_REFERENCE cross-checks

Source: `memory_system/data/experiments/memory_systems/results/RESULTS_S113.json` (canonical JSON cited by DATA_REFERENCE §K, NOT in study repo).

### Gradient baselines (DATA_REFERENCE §1) — 14 subjects × 3 numbers

All 14 subjects' C5, C2a, C4a values reproduce from RESULTS_S113.json to 2 decimals:

```
subject         paper C5  json C5    paper C2a  json C2a    paper C4a  json C4a
sunity_devee      1.03     1.03       2.47       2.47        2.60       2.60   OK
ebers             1.04     1.04       1.79       1.79        2.34       2.34   OK
hamerton          1.25     1.25       3.04       3.04        3.22       3.22   OK
fukuzawa          1.80     1.80       2.56       2.56        2.99       2.99   OK
seacole           1.85     1.85       2.64       2.64        2.78       2.78   OK
bernal_diaz       1.85     1.85       2.50       2.50        2.67       2.67   OK
keckley           1.91     1.91       2.64       2.64        2.62       2.62   OK
yung_wing         1.96     1.96       2.40       2.40        2.53       2.53   OK
babur             1.98     1.98       2.16       2.16        2.28       2.28   OK
cellini           2.56     2.56       2.72       2.72        2.79       2.79   OK
zitkala_sa        2.60     2.60       2.19       2.19        2.26       2.26   OK
rousseau          2.65     2.65       3.02       3.02        2.74       2.74   OK
augustine         2.79     2.79       2.83       2.83        3.08       3.08   OK
equiano           2.93     2.93       2.70       2.70        2.65       2.65   OK
```

**Aggregation method confirmed.** RESULTS_S113.json aggregation is a **flat mean across all non-parse-failed judgment rows on the full 7-judge panel (partial gemini_pro)**. Babur C5_baseline has n=249 = 39 questions × (6 full judges) + 15 partial gemini_pro rows.

**Inconsistency flagged.** Paper §3.7.5 specifies the primary aggregate as "5-judge (non-Gemini) panel (Haiku, Sonnet, Opus, GPT-4o, GPT-5.4)". RESULTS_S113 / DATA_REFERENCE §1 / paper Table 4.1 all use a flat-7-judge mean that includes Gemini Flash. The 5-judge per-judge mean for babur C5 is **1.76** (not 1.98). The methodology and results sections must be reconciled before §4 drafts lock in.

### Memory system deltas (DATA_REFERENCE §3) — controlled configuration

Recomputed from `memory-study-repo/results/global_<subj>/<system>_judgments_merged.json` by computing C3-mean minus C1-mean per subject, averaging across 14 subjects, filtering parse failures (`score > 0`).

| System | Paper Δ | Recomputed Δ from local merged judgments (filter `parse_failure=true`) | Match? |
|---|---:|---:|---|
| Mem0 | +0.15 | **+0.149** (14 subjects, all 6 judges present) | ✓ |
| Letta | +0.25 | **+0.246** (14 subjects) | ✓ |
| Zep | +0.22 | **+0.220** (14 subjects) | ✓ |
| Supermemory | −0.04 | **−0.039** (14 subjects, parse failures correctly filtered) | ✓ |
| Base Layer | +0.12 | **+0.084** (3-judge effective on 12 of 14 subjects) | ✗ |

Notes:
- **Mem0, Letta, Zep, Supermemory all reproduce from the public study repo** when the `parse_failure == true` flag is used to exclude bad rows. Score=0 parse-failure rows mixed with valid rows was the initial confusion — merged files encode parse failures as `score: 0, parse_failure: true`, so any filter that uses `score > 0` without checking `parse_failure` will get wrong numbers on Supermemory and Base Layer.
- **Base Layer is the one that does NOT reproduce from the public study repo.** S113 shows per-subject C1 values (keckley 2.75, augustine 2.785, cellini 2.164, ebers 2.015, etc.) that differ from local judgments (keckley 2.444, augustine 2.325, cellini 1.949, ebers 1.761). The S113 numbers match a 6-judge panel; local judgments are effectively 3-judge (h/s/o only) for 12 of 13 globals because the gpt4o/gpt5.4/gemini-flash rows on `baselayer_judgments_*.json` are 429 parse failures. **The 6-judge baselayer scores must exist somewhere to produce the S113 aggregates, but they are not in the public study repo.** This must be resolved before public launch.

### Low-baseline memory-system deltas (DATA_REFERENCE §4)

Not spot-checked in detail here, but Mem0 low-baseline +0.13 is consistent with the per-subject tables in mem0_analysis.json.

### Wrong-spec aggregate (DATA_REFERENCE §6)

**NOT VERIFIABLE from study repo.** DATA_REFERENCE §K says wrong-spec v2 data is at `run_fullstack_hamerton_20260411_231237/wrong_spec_v2_judgments_*.json + per-subject`. The `run_fullstack_hamerton_20260411_231237/` directory exists at `memory_system/data/experiments/memory_systems/results/` (outside repo), and all 13 per-subject `wrong_spec_v2_*` JSONs are at `memory_system/data/experiments/memory_systems/results/global_<subj>/wrong_spec_v2_*.json` (outside repo). **Any external reader cannot verify the wrong-spec v2 aggregate from the public repo.**

### Letta stateful block dimensions (DATA_REFERENCE §7)

Measured from `results/docs/research/_letta_blocks/<subj>_human_block.txt`:

| Subject | Paper chars | Measured chars | Match |
|---|---:|---:|---|
| Hamerton | 22,472 | 22,472 | ✓ exact |
| Ebers | 68,413 | 68,413 | ✓ exact |
| Babur | 335,349 | 335,349 | ✓ exact |

Word counts also match (Hamerton 3,167; Ebers 9,593; Babur 44,779).

### Tier 2 cross-provider (DATA_REFERENCE §10 vs RESULTS_S113.json vs figure script)

**Three-way disagreement flagged.** Three sources give three different delta sets:

| Cell | DATA_REFERENCE §10 (paper+fig) | RESULTS_S113.json | PROVENANCE_INDEX.md line 408 |
|---|---:|---:|---:|
| Ebers / Sonnet Δ | +1.48 | +1.188 | +1.48 |
| Ebers / Gemini Pro Δ | +1.07 | +0.033 | +0.23 |
| Yung Wing / Sonnet Δ | +1.91 | +1.849 | +1.91 |
| Yung Wing / Gemini Pro Δ | +1.27 | +0.413 | +0.58 |
| Zitkala-Sa / Sonnet Δ | +1.40 | +1.318 | +1.40 |
| Zitkala-Sa / Gemini Pro Δ | −0.55 | −0.077 | −0.09 |

`generate_fig11_tier2_replication.py` uses DATA_REFERENCE §10 values. PROVENANCE_INDEX marks DATA_REFERENCE §10 as "VERIFIED" but PROVENANCE_INDEX's own in-line delta citations (line 408) differ from DATA_REFERENCE §10 on the Gemini Pro row. **Resolve by recomputing from raw `tier2_*_judgments_*.json` in memory_system/ before Section 4.8 drafts.**

---

## 7. Duplicate / superseded files

**Legacy vs v2 pattern (global subjects):**

| Legacy | v2 | Relationship |
|---|---|---|
| `results_v2.json` | `results.json` (legacy, 40 Q including non-BP tiers) | `results_v2.json` is the primary 39-BP file used in all paper analysis. `results.json` is earlier (larger, includes non-BP tiers). Not contradictory — different scopes. Retain both for traceability. |
| `judgments.json` (legacy wide-format, haiku+gemini_flash only) | `judgments_v2.json` (long-format, 6 judges × 5 spec conditions) | `judgments_v2.json` supersedes `judgments.json` as the spec-condition judgment source. Legacy `judgments.json` is NOT superseded on **Hamerton** (where it holds the full-stack haiku+gemini judgments). |
| `judgments_v2_gemini_pro2.json` / `judgments_v2_gemini_pro_key2.json` | — | Augmented Gemini Pro runs on 3 subjects (augustine gets 40 rows, babur 23, bernal_diaz 10). Partial coverage; consumers must UNION these with `judgments_v2.json` to get all gemini_pro scores. Not superseded. |

**Hamerton-specific legacy:**
- `results.json` (80 questions, 5 full-stack conditions) vs `results_harmonized.json` (39 BP questions, same 5 conditions) — harmonized is a filtered view, not a replacement. Both used in different analyses.
- `judgments.json` (wide-format, haiku+gemini_score, 195 rows × 5 conditions) vs `judgments_harmonized.json` (long-format, 7 judges on C4_factdump + C5_baseline only, 546 rows) — these are two separate judgment phases; they ARE consistent (haiku and gemini overlap and agree).

**Subject specs (globals):** only `spec.md` in `results/global_<subj>/`. No v1/v2 versions in the published tree. Canonical.

**Gemini Pro judgment sidecar files at `results/hamerton/` and `results/franklin/`**: `gemini_pro_judgments.json` is not duplicated; it's the only Gemini Pro judgment file for these subjects. Clean.

No contradictory files detected. The legacy artifacts retain historical audit trail; delete candidates on release cleanup if size matters.

---

## 8. Memory-system data completeness

Each global and Hamerton has both controlled and native configs for all 5 systems (mem0, letta, supermemory, zep, baselayer). Files per (subject, system, config): ingestion (+ extracted for native), retrieval, results, 6 per-judge judgments, 1 merged judgments = ~11 files.

**Per-subject completeness (14 subjects × 5 systems × 2 configs = 140 cells):**

| System | Controlled (14 cells) | Native (14 cells) |
|---|---:|---:|
| Mem0 | **14 / 14 complete** | 14 / 14 complete (1 subject — ebers — has 12 of 234 parse failures) |
| Letta | 14 / 14 complete (6 subjects with 1-7 gpt4o 429 failures) | 14 / 14 complete |
| Supermemory | 14 / 14 complete; parse-failure rows widespread (equiano 168, babur 234, augustine 12 etc.) but recoverable mean via `parse_failure` filter | 14 / 14 complete (10/14 ingested; 4 failed free-tier: babur, bernal_diaz, cellini, rousseau → C1 returns empty responses) |
| Zep | **14 / 14 complete** | **14 / 14 complete** |
| Base Layer | 14 / 14 files present **BUT 12 of 13 globals have 0 valid gpt4o/gpt5.4/gemini-flash rows** — effectively 3-judge coverage for most subjects | 14 / 14 complete |

**Native-config supermemory failure breakdown** (C1_supermemory_fp means on global subjects; values of 0 = failed ingestion):

| Subject | Ingested? | C1_supermemory_fp mean |
|---|---|---:|
| augustine | partial (hours-long delay) | 0.487 |
| babur | failed | 0.000 |
| bernal_diaz | failed | 0.000 |
| cellini | failed | 0.000 |
| ebers | partial | 0.415 |
| equiano | OK | 1.487 (depressed) |
| fukuzawa | partial | 0.372 |
| keckley | OK | 2.581 |
| rousseau | failed | 0.000 |
| seacole | partial | 1.265 |
| sunity_devee | partial | 0.329 |
| yung_wing | OK | 2.521 |
| zitkala_sa | OK | 2.466 |
| hamerton | OK | 2.201 |

DATA_REFERENCE §3 says "4 subjects failed free-tier ingestion" — matches the 4 zero-mean subjects. The partial-ingestion subjects (augustine, ebers, fukuzawa, seacole, sunity_devee) have depressed C1 means but non-zero responses.

---

## 9. Tier 2 / circularity data

**Paper §3.6 (line 395) says:** "Raw response files are in the public repository at `results/global_<subject>/results_v2.json` for the 13 global subjects, `data/<subject>/results.json` for Hamerton and Franklin, and `results/_tier2/` for the Tier 2 runs."

**`results/_tier2/` does not exist in memory-study-repo.** Tier 2 data is at:

```
memory_system/data/experiments/memory_systems/results/global_ebers/tier2_sonnet_results.json
memory_system/data/experiments/memory_systems/results/global_ebers/tier2_gemini_pro_results.json
memory_system/data/experiments/memory_systems/results/global_yung_wing/tier2_sonnet_results.json
memory_system/data/experiments/memory_systems/results/global_yung_wing/tier2_gemini_pro_results.json
memory_system/data/experiments/memory_systems/results/global_zitkala_sa/tier2_sonnet_results.json
memory_system/data/experiments/memory_systems/results/global_zitkala_sa/tier2_gemini_pro_results.json
```

Plus per-judge `tier2_<model>_judgments_<judge>.json` × 6 judges × 6 cells = 36 judgment files. Each Tier 2 results file has 39 questions and 4 conditions (C2a_full_spec, C2c_wrong_spec, C4a_full_facts_plus_spec, C5_baseline).

**Action required:** either copy Tier 2 files into `memory-study-repo/results/_tier2/` before public launch, OR update paper §3.6 line 395 to point to the actual location (and include in the repo release bundle).

Also flagged: `memory_system/...` also contains `tier2_*_results.json.brief_only_backup` files — 18 of them. These are pre-full-stack backups; **do not release**.

Three-way delta disagreement (detailed in §6) must also be resolved.

---

## 10. Letta stateful-agent data

**Memory blocks** at `memory-study-repo/docs/research/_letta_blocks/`:

| File | Size (chars) | Words | Paper claim (DATA_REFERENCE §7) | Match |
|---|---:|---:|---|---|
| `hamerton_human_block.txt` | 22,472 | 3,167 | 22,472 chars / ~3,167 words | ✓ |
| `ebers_human_block.txt` | 68,413 | 9,593 | 68,413 chars / ~9,593 words (paper §4.3.1 Ebers only mentions ~3× Hamerton size) | ✓ |
| `babur_human_block.txt` | 335,349 | 44,779 | 335,349 chars | ✓ |

All three dimensions match the paper exactly.

**Support files** in `_letta_blocks/`: `response_pairs.txt`, `paired_scores.json`, `archival_pairs.txt`, plus extraction scripts. Good for replication.

**Letta re-run data** at `memory-study-repo/docs/research/_letta_rerun/`: per-subject responses, batteries, 7-judge judgments for ebers + babur (20-50_*.py investigation scripts + per-judge JSON). Includes `ebers_judgments_gemini_pro.json` and `babur_judgments_gemini_pro.json`. These are the matched-model haiku-over-Letta-block test described in §4.3.1.

No data gap for the Letta stateful test.

---

## Issues requiring fix before §4 drafting

1. **CRITICAL — Missing data in public repo** (3 categories): Tier 2 response + judgment files; wrong-spec v2 response + judgment files; RESULTS_S113.json canonical aggregates. Either copy these into `memory-study-repo/results/_tier2/`, `memory-study-repo/results/wrong_spec_v2/`, and `memory-study-repo/results/RESULTS_S113.json` respectively, OR update paper §3.6 and DATA_REFERENCE §K to point to the actual external paths and publish those paths in the release.

2. **CRITICAL — Baselayer 6-judge deficit.** 12 of 13 globals have 0 valid gpt4o/gpt5.4/gemini-flash judgments on C1_baselayer + C3_baselayer (all 429 failures). Paper's Base Layer mean Δ = +0.12 is not reproducible from the public data at 6-judge. Options:
   (a) Rerun the 3 missing judges on 12 subjects × 2 conditions × 39 questions = 936 calls (roughly 1-2 hrs of budget).
   (b) Downgrade Base Layer to 3-judge aggregate in the paper and note explicitly.
   (c) Use the 5-judge primary panel (which excludes gemini-flash anyway, so would require only gpt4o + gpt5.4 backfill = 624 calls).

3. **CRITICAL — Tier 2 delta source disagreement.** DATA_REFERENCE §10, PROVENANCE_INDEX §4.8, RESULTS_S113.json `tier2_circularity.per_cell`, and `scripts/generate_fig11_tier2_replication.py` all disagree. Recompute from `memory_system/.../tier2_*_judgments_*.json` raw data before §4.8 drafting and reconcile against paper narrative claims (5/6 positive matches, Zitkala-Sa outlier).

4. **HIGH — Aggregation method mismatch between §3.7.5 and Table 4.1.** §3.7.5 specifies 5-judge primary (no Gemini). Table 4.1 numbers reproduce only under 6-judge (includes gemini-flash) or flat-7-judge. Either change §3.7.5 to state "6-judge primary excluding gemini-pro" OR recompute Table 4.1 and all gradient stats under the 5-judge rule and update.

5. **MEDIUM — Score=0 parse-failure semantics across memory-system merged files.** 16 subject×system×config cells have 5-234 score=0 rows mixed with valid scores. Any downstream consumer that does not filter on `parse_failure == true` will report wrong means (a consumer that only filters `score > 0` can still drop legitimate refusal responses). Once `parse_failure` is filtered, Mem0/Letta/Zep/Supermemory all reproduce the paper. The merged files should use `score: null` for parse failures rather than `score: 0`, OR the analysis code / README must explicitly document the `parse_failure` filtering rule.

6. **MEDIUM — Franklin judge coverage is 3 of 7, not 7 of 7.** sonnet/opus/gpt4o/gpt5.4 never ran on Franklin. DATA_REFERENCE §9 describes "all 7 judges" but Franklin's effective panel is haiku + gemini-flash + gemini-pro. Either rerun missing judges on Franklin OR scope the "7 judges on all subjects" claim to the 13 globals + Hamerton.

7. **MEDIUM — cp1252 JSON files.** `results/judge_calibration/results.json` and `results/multimodel/gpt54_hamerton.json` need re-saving as UTF-8.

8. **MEDIUM — Paper §3.6 path references are wrong.** Line 395 points to `results/_tier2/` (missing). Line 327 says Tier 2 files are "in the same per-subject directories" — inconsistent with 395, and currently false.

9. **LOW — Hamerton opus on full-stack conditions: 38 of 39.** One question missing across all 5 full-stack conditions. Likely same question dropped. Not blocking but worth noting.

10. **LOW — Babur C9_raw_corpus_plus_spec: 38 of 39 responses.** One question is missing a response across C9. Delta between condition means computed on 38 vs 39 observations.

11. **LOW — No `baselayer_analysis.json` aggregate file.** Other 4 systems have them; Base Layer does not. Asymmetric release artifact.

---

## Clean-to-proceed checklist

Items verified to spec and safe to cite in Section 4:

- ✓ Gradient Table 4.1 numbers (14 subjects × C5/C2a/C4a) reproduce from RESULTS_S113.json at 2-decimal precision.
- ✓ Battery coverage: all 14 subjects have 39 (Franklin: 40) behavioral-prediction questions. All 13 globals have GPT-5.4 regenerated batteries for Control 1.
- ✓ Letta stateful memory block character counts (22,472 / 68,413 / 335,349) match paper claims exactly.
- ✓ Mem0 controlled Δ +0.15 reproduces from study-repo raw data (filter `parse_failure`).
- ✓ Letta controlled Δ +0.25 reproduces.
- ✓ Zep controlled Δ +0.22 reproduces.
- ✓ Supermemory controlled Δ −0.04 reproduces.
- ✓ Supermemory native failure on 4 subjects (babur/bernal_diaz/cellini/rousseau) matches DATA_REFERENCE §3 "4 subjects failed free-tier ingestion."
- ✓ Haiku + Sonnet + Opus 3-judge coverage is complete (minor 1-7 question gaps on letta gpt4o) across all 14 subjects × 25 conditions.
- ✓ GPT-5.4 backfill coverage is complete for all 14 subjects × 25 conditions.
- ✓ Gemini Flash coverage is complete except on baselayer C1/C3 (see Issue 2).
- ✓ C8 + C9 raw corpus response and judgment data present and consistent with Table 4.2 (Hamerton).

Items that CANNOT be cited without first resolving an issue above:
- ✗ Base Layer aggregate delta (§4.3, §4.4): Issue 2.
- ✗ Tier 2 table (§4.8): Issues 1 + 3.
- ✗ Wrong-spec v2 aggregate (DATA_REFERENCE §6): Issue 1.
- ✗ "7-judge primary" or "5-judge primary" framing (§3.7.5 vs §4): Issue 4.
- ✗ "All memory-system means computed from" claims at 6-judge: Issue 5.
- ✗ "Reproducible from the public repo" claims: Issue 1.
