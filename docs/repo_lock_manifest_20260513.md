# Repo lock manifest — v12.1 cycle (post-v12.1 draft)

Generated: 2026-05-14T01:48:56.516556Z
Manifest SHA-256: `31975bf3176aeb528911ef40b77acab63858af98acaa5f69bdfe88c621fdc5a5`
Files covered: 4,194
Total bytes: 596,748,836 (569.1 MB)

## Scope

State snapshot of the repo at the v12.1 paper-draft cycle. Captured after v12 and v12.1 paper artifacts landed; paper itself is still under active edit. Prior lock at `docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.{md,json}` is preserved unchanged.

**Excluded paths.** `.git/`, `workspace/study_vectors/`, `__pycache__/`, IDE caches, byte-compiled Python, OS metadata, Word lock-files. Exclusion rules are inherited verbatim from `scripts/generate_repo_lock_manifest_20260510.py` so the two manifests are directly comparable.

## Re-verification

To verify integrity of this snapshot at any later date:

```
python scripts/generate_repo_lock_manifest_20260510.py --verify docs/repo_lock_manifest_20260513.json
```

Returns a per-file diff: PRESENT and matches, CHANGED, MISSING, NEW.

## Companion files

- Full per-file JSON table: `repo_lock_manifest_20260513.json`
- Prior lock (v11.9.7 cycle, 2026-05-10): `docs/reviews/repo_lock_manifest_v11_9_7_cycle_20260510.{md,json}`
- v12.1 diff + integrity report: `docs/reviews/v12_1_repo_lock_report_20260513.md`

## Top-50 largest tracked files

| Size (KB) | Path | SHA-256 (first 12) |
|---|---|---|
| 16,700 | `docs/references/bartlett_1932_remembering.pdf` | `47664de9b2da` |
| 13,304 | `workspace/study_knowledge.db` | `898a93ad5774` |
| 12,926 | `docs/references/jiang_2025_2504.14225_know_me_respond_to_me.pdf` | `24633e985675` |
| 10,855 | `results/global_rousseau/letta_fullpipeline_results.json` | `ddc1c4903487` |
| 10,820 | `results/global_ebers/letta_fullpipeline_results.json` | `badfe421dbd5` |
| 10,685 | `results/global_rousseau/letta_fullpipeline_retrieval.json` | `aebbe0ba8098` |
| 10,637 | `results/global_ebers/letta_fullpipeline_retrieval.json` | `a76075e71135` |
| 10,619 | `results/global_bernal_diaz/letta_fullpipeline_results.json` | `6a20e56c4f11` |
| 10,423 | `results/global_bernal_diaz/letta_fullpipeline_retrieval.json` | `0c96aee2da66` |
| 10,380 | `results/global_cellini/letta_fullpipeline_results.json` | `647afd2709b0` |
| 10,353 | `results/global_augustine/letta_fullpipeline_results.json` | `c163fa2d5dc9` |
| 10,195 | `results/global_cellini/letta_fullpipeline_retrieval.json` | `a2b8a657eaef` |
| 10,174 | `results/global_augustine/letta_fullpipeline_retrieval.json` | `ef7e046777a8` |
| 10,066 | `results/global_fukuzawa/letta_fullpipeline_results.json` | `43cc7cf341b2` |
| 9,902 | `results/global_fukuzawa/letta_fullpipeline_retrieval.json` | `af9b4f4e8805` |
| 9,026 | `results/global_equiano/letta_fullpipeline_results.json` | `78acb0862538` |
| 8,834 | `results/global_equiano/letta_fullpipeline_retrieval.json` | `2daa47af17d0` |
| 7,641 | `results/global_babur/letta_fullpipeline_results.json` | `cf8db18c9b84` |
| 7,430 | `results/global_babur/letta_fullpipeline_retrieval.json` | `4cec06c2e2ca` |
| 7,250 | `results/global_sunity_devee/letta_fullpipeline_results.json` | `5be92e4d31bd` |
| 7,181 | `results/global_yung_wing/letta_fullpipeline_results.json` | `9865d45db6af` |
| 7,075 | `results/global_sunity_devee/letta_fullpipeline_retrieval.json` | `589d9dad0ee2` |
| 6,971 | `results/global_yung_wing/letta_fullpipeline_retrieval.json` | `db4f9e61636d` |
| 6,846 | `results/global_seacole/letta_fullpipeline_results.json` | `683c6d4a11f0` |
| 6,678 | `results/global_seacole/letta_fullpipeline_retrieval.json` | `977aad8c8642` |
| 6,590 | `results/global_keckley/letta_fullpipeline_results.json` | `eb0271b7647d` |
| 6,397 | `results/global_keckley/letta_fullpipeline_retrieval.json` | `99558522e0b1` |
| 5,718 | `results/hamerton/letta_fullpipeline_results.json` | `caa9b4842254` |
| 5,541 | `results/hamerton/letta_fullpipeline_retrieval.json` | `745516922e41` |
| 4,809 | `docs/references/chen_2025_2507.21509_persona_vectors.pdf` | `2879ae0f9592` |
| 4,535 | `docs/references/toubia_2025_2505.17479_twin_2k_500.pdf` | `51cd1884bd75` |
| 4,344 | `docs/references/lu_2026_2601.10387_the_assistant_axis.pdf` | `e9e638ad3057` |
| 3,660 | `results/global_zitkala_sa/letta_fullpipeline_results.json` | `fb2f4c4f217b` |
| 3,537 | `docs/references/samuel_2025_2407.18416_personagym.pdf` | `debe2b78fe9e` |
| 3,461 | `results/global_zitkala_sa/letta_fullpipeline_retrieval.json` | `f4083f1e5604` |
| 3,286 | `docs/references/perez_2022_2212.09251_discovering_language_model_behaviors.pdf` | `7fd476342aba` |
| 3,286 | `docs/versions/_pre_v12_drafts/beyond_recall_v10_1_draft.docx` | `b48e09c88957` |
| 3,228 | `docs/versions/_pre_v11_drafts/beyond_recall_v9_draft.docx` | `e60cb7775fe7` |
| 3,002 | `docs/versions/_archive_pre_v11_9_5/beyond_recall_v11_1_draft.docx` | `6ce979c77169` |
| 3,002 | `docs/versions/_archive_pre_v11_9_5/beyond_recall_v11_draft.docx` | `5ed54ea1152d` |
| 2,855 | `docs/versions/_pre_v11_8_drafts/beyond_recall_v11_6_draft.docx` | `0d6b85f54111` |
| 2,847 | `docs/versions/_pre_v11_8_drafts/beyond_recall_v11_7_draft.docx` | `6df57ca3535b` |
| 2,815 | `docs/versions/_pre_v11_drafts/beyond_recall_v10_1_draft.docx.bak` | `b9bf91ff205d` |
| 2,721 | `data/source_corpora/babur/raw.txt` | `47c48eec4168` |
| 2,687 | `docs/references/jain_2025_2509.12517_interaction_context_sycophancy.pdf` | `31d04a39ed59` |
| 2,587 | `docs/versions/_archive_pre_v11_9_5/beyond_recall_v11_2_draft.docx` | `dd67a9ed9de6` |
| 2,473 | `docs/versions/_pre_v11_drafts/beyond_recall_v8_draft.docx` | `47f38a0d8087` |
| 2,275 | `docs/research/s114_diverse_examples.json` | `e57940ff7bd3` |
| 2,190 | `build/beyond_recall.pdf` | `b07605469fa4` |
| 2,176 | `docs/research/wrong_spec_detection_raw.json` | `fd583e94c183` |