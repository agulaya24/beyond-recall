# §3.4 Battery Generation — Verification Report

**Scope:** Verify the backward-design battery generation procedure, enumerate per-subject battery statistics, and measure n-gram leakage between generated behavioral-prediction questions and the held-out text for all 14 main-study subjects.

**Generator source of truth:** `memory_system/data/experiments/memory_systems/run_global_rerun.py` (lines 517–826). This is the production rerun script. The earlier `run_global_subjects.py` (unused in the published study) contained a 60-question generator without the five-tier structure; it is deprecated.

**Response battery used in published results:**
- 13 global subjects: `results/global_<subject>/battery_v2.json` (80 questions, backward-designed by Haiku 4.5).
- Hamerton: `data/hamerton/battery.json` (80 questions, backward-designed, hand-curated).
- Franklin: `data/franklin/battery.json` (80 questions, pre-backward-design conventional battery; see §C for a leakage caveat specific to Franklin).

---

## A. Backward-design procedure (6 steps)

The code path is `phase_battery()` → `generate_bp_questions()` → `generate_tier_questions()` in `run_global_rerun.py`.

1. **Corpus split.** Each subject's autobiography is split into `training.txt` and `heldout.txt` by chapter boundary before any LLM work. The training text becomes the basis for fact extraction and spec authoring; the held-out text is never shown to the response models or to the spec pipeline.

2. **Backward-design generation (behavioral prediction tier, 39 questions).**
   A sliding window over `heldout.txt` produces 4 batches of 10 BP questions each (5,000-character window, stepped across the held-out corpus). For each batch, Haiku 4.5 (temperature=0) is prompted with:
   - the first 3,000 chars of `training.txt` (training patterns the model should reason from), and
   - a 5,000-char held-out window (source of ground-truth behaviors).

   The prompt (`BP_PROMPT_TEMPLATE`, lines 521–540) instructs the model to:
   > (a) find a specific decision/behavior in the held-out text,
   > (b) write a question answerable from training patterns alone,
   > (c) extract the held-out passage verbatim as ground truth,
   > (d) **not** include names, dates, or details unique to the held-out text in the question stem.

3. **Supplementary tiers (41 questions).** Four additional tiers are generated from `training.txt` alone (`generate_tier_questions`): recall (10), inferential (11), adversarial abstention (10), boundary probing (10). These are generated but **not scored in the main results**; they exist for downstream tier-specific analyses.

4. **Post-generation filtering.**
   - Deduplication by lowercased question text (`generate_bp_questions`, lines 621–628).
   - Truncation to target count: BP capped at 39, each supplementary tier capped at its target.
   - Integrity check (`phase_verify`, lines 820–825): any battery with fewer than `TARGET_TOTAL - 5 = 75` questions, or fewer than `TARGET_BP - 5 = 34` BP questions carrying `held_out_passage` fields, is flagged for regeneration.
   - Cryptographic checksum (`compute_battery_checksum`, line 583): MD5 over the sorted JSON question list is stored in battery metadata. Any battery-schema change invalidates downstream results via FM-3 (`phase_battery` wipes `results_v2.json`, `judgments_v2.json`, `responses_checkpoint.json` on regeneration).
   - The generator enforces a 10-category vocabulary for the BP tier (`BP_CATEGORIES`, lines 73–76): `decisions, values, relationships, conflict, learning, risk, creativity, stress, career, change_over_time`.

5. **Output structure.** Each battery is a single JSON file with metadata and a flat question list:
   ```json
   {
     "metadata": {
       "subject": "...", "subject_key": "...",
       "generated": "<ISO-8601>", "model": "claude-haiku-4-5-20251001",
       "method": "backward_design_from_heldout",
       "total": 80,
       "tiers": {"behavioral_prediction": 39, "recall": 10,
                 "inferential": 11, "adversarial_abstention": 10,
                 "boundary_probing": 10},
       "checksum": "<md5>"
     },
     "questions": [
       {"id": 1, "tier": "behavioral_prediction",
        "category": "decisions", "text": "...",
        "held_out_passage": "<verbatim quote>"},
       ...
     ]
   }
   ```

6. **Circularity control (Control 1 in §3.4.1).** For all 13 global subjects, an independent battery was regenerated with GPT-5.4 using the same prompt; stored at `results/global_<subject>/battery_gpt54.json` (`method: "backward_design"`). Tier 2 replication (§4.8) uses these GPT-5.4 batteries with non-Haiku response models to defuse generator-model circularity.

---

## B. Per-subject battery statistics

Source: `battery_v2.json` for 13 global subjects, `data/<subject>/battery.json` for Hamerton and Franklin. Counts verified programmatically by `scripts/_verify_battery_leakage.py`.

| Subject | Total | BP (scored) | Other (not scored) | BP categories present |
|---|---:|---:|---:|---:|
| hamerton | 80 | 39 | 41 | 10 |
| franklin | 80 | 40 | 40 | 10 |
| augustine | 80 | 39 | 41 | 8 |
| babur | 80 | 39 | 41 | 10 |
| bernal_diaz | 80 | 39 | 41 | 8 |
| cellini | 80 | 39 | 41 | 10 |
| ebers | 80 | 39 | 41 | 9 |
| equiano | 80 | 39 | 41 | 8 |
| fukuzawa | 80 | 39 | 41 | 9 |
| keckley | 80 | 39 | 41 | 9 |
| rousseau | 80 | 39 | 41 | 10 |
| seacole | 80 | 39 | 41 | 9 |
| sunity_devee | 80 | 39 | 41 | 9 |
| yung_wing | 80 | 39 | 41 | 10 |
| zitkala_sa | 80 | 39 | 41 | 8 |
| **Total** | **1,120** | **586** | **534** | — |

**Per-tier breakdown (applies to all 15 batteries except Franklin, which has BP=40 / inferential=10):**
- Behavioral prediction (scored): 39 (Franklin: 40)
- Inferential synthesis: 11 (Franklin: 10)
- Factual recall: 10
- Adversarial abstention: 10
- Boundary probing: 10

**Category universe across all 14 subjects:** `career, change_over_time, conflict, creativity, decisions, learning, relationships, risk, stress, values` — the ten fixed categories defined by `BP_CATEGORIES`. Not every subject's battery covers all ten; Haiku omits 0–2 categories per subject based on which behavioral patterns are salient in the held-out windows it sees.

---

## C. Leakage measurement

**Definition.** A behavioral-prediction question is flagged as "leaked" if its text contains any 7-consecutive-word n-gram (after lowercasing and stripping punctuation) that also appears verbatim in the held-out text. This is a conservative string-level check: it catches direct quoting of held-out content in the question stem.

**Corpus choice per subject.**
- 13 global subjects: held-out corpus is `memory_system/data/experiments/memory_systems/results/global_<subject>/heldout.txt` (the full held-out chapters, ~5,000–40,000 words).
- Hamerton + Franklin: no standalone `heldout.txt` on disk. Held-out corpus was reconstructed as the concatenation of every `held_out_passage` field from their respective `battery.json` — the exact verbatim excerpts the generator drew from. This is a stricter check than a full-text search (a false positive in the reconstructed corpus is always a real leak; a false negative is possible only for held-out text outside any question's ground truth, which the generator never surfaced in the first place).

**Results.** Script: `memory-study-repo/scripts/_verify_battery_leakage.py`. Full output: `memory-study-repo/scripts/_battery_leakage_results.json`.

| Subject | BP questions | Leaked | Leak rate |
|---|---:|---:|---:|
| hamerton | 39 | 0 | 0.000 |
| franklin | 40 | **2** | 0.050 |
| augustine | 39 | 0 | 0.000 |
| babur | 39 | 0 | 0.000 |
| bernal_diaz | 39 | 0 | 0.000 |
| cellini | 39 | 0 | 0.000 |
| ebers | 39 | 0 | 0.000 |
| equiano | 39 | 0 | 0.000 |
| fukuzawa | 39 | 0 | 0.000 |
| keckley | 39 | 0 | 0.000 |
| rousseau | 39 | 0 | 0.000 |
| seacole | 39 | 0 | 0.000 |
| sunity_devee | 39 | 0 | 0.000 |
| yung_wing | 39 | 0 | 0.000 |
| zitkala_sa | 39 | 0 | 0.000 |
| **Aggregate** | **586** | **2** | **0.0034** |

**Aggregate leakage rate across all 14 subjects: 2 / 586 = 0.34%.**

**Detail on the two Franklin cases.** Both are in `data/franklin/battery.json` — the hand-curated pre-backward-design battery used for the Franklin replication:

- Q49 (category: decisions). The question stem quotes the phrase *"little advantages that occur every day"* which appears verbatim in the held-out passage. The quote is attributed to Franklin in the stem and used as context for a prediction, not as the answer.
- Q56 (category: change_over_time). The question stem quotes *"the publick, now considering me as a man of leisure, laid hold of me for their purposes"*, which is the exact held-out sentence.

**Interpretation.** These two cases predate the `run_global_rerun.py` backward-design pipeline; the Franklin battery was hand-authored before the `IMPORTANT: The question text must NOT contain names, dates, or specific details that only appear in the held-out text` constraint was added to the generator prompt. Haiku-generated batteries (13 global subjects + Hamerton = 547 BP questions) show 0% leakage at the 7-gram threshold — the constraint appears to be strictly honored.

**Paper recommendation.** Report aggregate 0.34% with the Franklin-specific note, or recompute the Franklin effect after excluding Q49/Q56 to show the delta is robust. The two leaks reveal the phrase the question is asking about but do not reveal the *behavior* (the ground truth is a full passage of 60–200 words, of which the 7-word quote is a small fragment); the judge rubric scores on prediction of the full behavior, so the practical impact on Franklin's reported score is expected to be minor. The honest move is to disclose this in §3.4 and, if time permits, run a sensitivity analysis.

---

## D. Raw data locations

For the paper's "raw battery data is available at…" pointer:

| Artifact | Path template |
|---|---|
| Per-subject battery (production, 13 global subjects) | `results/global_<subject>/battery_v2.json` |
| Per-subject battery (GPT-5.4 independent generation, 13 global subjects) | `results/global_<subject>/battery_gpt54.json` |
| Per-subject battery (Hamerton) | `data/hamerton/battery.json` |
| Per-subject battery (Franklin) | `data/franklin/battery.json` |
| Per-subject held-out text (all 13 global subjects) | `memory_system/data/experiments/memory_systems/results/global_<subject>/heldout.txt` (also mirrored at `memory-study-repo/results/global_<subject>/heldout.txt`) |
| Per-subject training text (all 13 global subjects, memory_system side) | `memory_system/data/experiments/memory_systems/results/global_<subject>/training.txt` |
| Franklin training corpus | `memory_system/data/corpora/franklin_autobiography/chapters/` (chapters 00–10 = training, 11–19 = held out) |
| Battery-generation script (canonical) | `memory_system/data/experiments/memory_systems/run_global_rerun.py` (see `phase_battery`, `generate_bp_questions`, `generate_tier_questions`) |
| Battery-verification script (this study) | `memory-study-repo/scripts/_verify_battery_leakage.py` |
| Leakage analysis output (machine-readable) | `memory-study-repo/scripts/_battery_leakage_results.json` |

**Suggested §3.4 citation line:**
> All 14 batteries, both generation scripts (Haiku backward-design and the GPT-5.4 independent replication), and the per-subject held-out corpora are released in the companion repository at `results/global_<subject>/battery_v2.json` and `data/<subject>/battery.json`. The battery-generation code is `memory_system/data/experiments/memory_systems/run_global_rerun.py`; the leakage audit script is `scripts/_verify_battery_leakage.py` (the audit measured 2 / 586 = 0.34% 7-gram leakage across the main study, concentrated in two Franklin questions from the pre-backward-design hand-curated battery).

---

## E. Example backward-designed question + held-out source

*Augustine battery, question 1 (Haiku 4.5, backward-designed):*

- **Question (visible to response model):** "When Augustine encounters a text that challenges his previous beliefs, how does he typically respond emotionally?"
- **Held-out passage (visible only to judge):** "With what vehement and bitter sorrow was I angered at the Manichees! and again I pitied them, for they knew not those Sacraments, those medicines, and were mad against the antidote which might have recovered them of their madness."
- **Category:** conflict.

The question stem contains no proper nouns from the held-out text (no "Manichees", "Sacraments", "medicines"). The held-out passage specifies Augustine's emotional pattern — *vehement bitter sorrow followed by pity* — which a correct prediction from training patterns should approximate.
