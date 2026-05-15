# Appendix B (selected per-subject tables, supplementary)

## Cross-reference

This file holds the wide per-subject tables from Appendix B of the Beyond Recall paper that were relocated for length reasons. All scientific content is preserved verbatim. The surrounding prose, headline findings, and footers remain in the main paper at the indicated section pointers.

Cited from the main paper at:
- §3.5 and §B.1 (battery composition rationale and the 10 fixed behavioral-prediction categories).
- §4.1 and §B.6 (battery-composition sensitivity analysis that uses the per-subject category counts).
- §B.2 stub in the main paper points to this file for the 10-category by 15-subject matrix.
- §B.3 stub in the main paper retains the aggregate distribution table; the per-subject distribution table is here.

The Appendix B subsection anchors (§B.2, §B.3) remain in the main paper as stubs so that existing in-text references continue to resolve.

---

## B.2 Per-subject battery composition (10-category by 15-subject matrix)

The following table gives the count of behavioral-prediction questions in each category for each subject. The total column is 39 for the 13 global subjects and Hamerton, and 40 for Franklin. Raw batteries are at `results/global_<subject>/battery_v2.json` (global subjects), `data/hamerton/battery.json` (Hamerton), and `data/franklin/battery.json` (Franklin).

| Subject | decis | val | rel | conf | learn | risk | creat | stress | career | ch_o_t | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| augustine | 6 | 7 | 4 | 5 | 9 | 0 | 3 | 3 | 0 | 2 | 39 |
| babur | 9 | 6 | 8 | 4 | 3 | 1 | 2 | 3 | 2 | 1 | 39 |
| bernal_diaz | 8 | 8 | 4 | 5 | 5 | 3 | 0 | 5 | 0 | 1 | 39 |
| cellini | 5 | 6 | 5 | 4 | 3 | 1 | 4 | 5 | 4 | 2 | 39 |
| ebers | 4 | 8 | 3 | 4 | 6 | 0 | 6 | 3 | 1 | 4 | 39 |
| equiano | 5 | 8 | 4 | 5 | 5 | 1 | 0 | 8 | 0 | 3 | 39 |
| fukuzawa | 8 | 11 | 5 | 5 | 3 | 1 | 1 | 2 | 0 | 3 | 39 |
| keckley | 6 | 7 | 9 | 6 | 4 | 1 | 0 | 3 | 2 | 1 | 39 |
| rousseau | 5 | 6 | 9 | 6 | 5 | 1 | 1 | 4 | 1 | 1 | 39 |
| seacole | 7 | 10 | 7 | 1 | 3 | 1 | 2 | 6 | 2 | 0 | 39 |
| sunity_devee | 4 | 9 | 6 | 5 | 5 | 1 | 1 | 6 | 0 | 2 | 39 |
| yung_wing | 10 | 8 | 3 | 3 | 3 | 1 | 3 | 2 | 5 | 1 | 39 |
| zitkala_sa | 4 | 11 | 6 | 5 | 4 | 0 | 3 | 4 | 0 | 2 | 39 |
| hamerton | 6 | 4 | 6 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 39 |
| franklin | 6 | 6 | 5 | 4 | 3 | 4 | 4 | 3 | 3 | 2 | 40 |
| **Column total** | **93** | **115** | **84** | **66** | **65** | **19** | **34** | **60** | **23** | **27** | **586** |

Columns: decis = decisions, val = values, rel = relationships, conf = conflict, learn = learning, creat = creativity, ch_o_t = change_over_time. Source: battery_v2.json and battery.json files, counted over `tier == "behavioral_prediction"` slices.

---

## B.3 Per-subject behavioral-axis distribution (LITERAL / INTERPRETIVE / REFUSAL-TRIGGERING)

The aggregate distribution is in the main paper at §B.3. The per-subject breakdown follows. Source: `docs/research/question_category_audit.md`.

| Subject | LITERAL | INTERP | REFUSAL | n |
|---|---:|---:|---:|---:|
| augustine | 4 | 33 | 2 | 39 |
| babur | 1 | 25 | 13 | 39 |
| bernal_diaz | 2 | 28 | 9 | 39 |
| cellini | 4 | 27 | 8 | 39 |
| ebers | 2 | 30 | 7 | 39 |
| equiano | 6 | 27 | 6 | 39 |
| fukuzawa | 4 | 27 | 8 | 39 |
| keckley | 4 | 30 | 5 | 39 |
| rousseau | 2 | 32 | 5 | 39 |
| seacole | 8 | 28 | 3 | 39 |
| sunity_devee | 8 | 23 | 8 | 39 |
| yung_wing | 3 | 24 | 12 | 39 |
| zitkala_sa | 2 | 22 | 15 | 39 |
| hamerton | 10 | 10 | 19 | 39 |
| franklin | 0 | 37 | 3 | 40 |
