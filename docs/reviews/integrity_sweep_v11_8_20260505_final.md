# Final integrity sweep — Beyond Recall v11.8 (2026-05-05 evening)

Source: `C:\Users\Aarik\Anthropic\memory-study-repo\docs\beyond_recall_v11_8_draft.md` (3,222 lines; +6 vs. prior sweep at 13:04:38).

---

## Delta from prior sweep (`integrity_sweep_v11_8_20260505_130438.md`)

**Items resolved:**
- L466 broken anchor `#411-per-question-baseline-engagement-and-the-worked-rubric-example` (footnote moved off heading; L819 heading is now clean; in-doc link now at L464). FIXED.
- L665 broken anchor `#8-data-and-code-availability` (link text + anchor reconciled to "Data, code, and reproducibility" / `#8-data-code-and-reproducibility`; in-doc link now at L663). FIXED.

**New items introduced tonight:**
- New footnote `[^share-zero-cut]`: ref at L1168, def at L1170. Properly anchored (def directly follows ref). 1:1 match. CLEAN.
- New `[^companion-data-411]` location: previously on §4.1.1 heading line, now on first-paragraph at L821. Heading at L819 is bare. CLEAN.
- New embedded figure `figures/fig_4_4_1_jaccard_heatmap_v1.png` at L1188. File exists. CLEAN.
- §2.5 confirmed absent from §2 (only §2.1, §2.2, §2.3, §2.4); zero `§2.5` references in body text. CLEAN.

**Carryover items not addressed tonight (same status as prior sweep):**
- L1210 + L1214 "Appendix B.X" (forthcoming). Still flagged in `[^memsys-pattern-appendix]` text. Tracked in `project_v11_paper_active_editing.md` as deferred work.
- L2096 §B.9.3 cosmetic label `[^supermemory-no-retrieval]` (no real footnote with that name). Cosmetic only; renders as literal text inside backticks.
- L2078 "Appendix C / §4.3" content-categorization concern (Appendix C is conditions/models, not wrong-spec). Editorial.

---

## Footnote system: PASS

- 70 unique definitions (vs. 69 in prior sweep, +1 = `share-zero-cut`).
- 70 unique reference names; total ~73 ref instances (some lines carry multiple).
- Orphan refs: **none**. Orphan defs: **none**. Duplicates: **none**.
- `share-zero-cut`: ref L1168 (in §4.4.1 retrieval-overlap paragraph), def L1170 (immediately following). Definition near the citation as required.
- `companion-data-411`: ref L821 (first sentence of §4.1.1 body, off the heading), def L823. Definition near the citation. The §4.1.1 heading at L819 is now clean text.
- All 69 footnotes from prior sweep retained 1:1. Definition-list dump (alphabetical) below — line numbers updated for ones that moved.

```
anchor-crossing-data       L519    franklin-judge-range          L319
baseline-rubric-pointer    L317    gradient-slopes               L699
baseline-thresholds        L98     hedging                       L124
battery-sensitivity-detail L1424   heldout-leakage-audit         L817
benchmark-disputes         L211    jaccard-aggregate-detail      L1192
bimodal-stats              L825    judgments-data                L629
bs-footnote                L1525   keckley-axioms                L1301
c2c-construction           L78     keckley-q21-data              L1299
c9-aggregation             L930    length-by-condition           L605
circularity-data           L373    letta-additional              L80
companion-data-411         L823    letta-arch                    L209
composition-patterns       L1555   letta-recall                  L201
compression-data           L994    letta-second-path             L1139
conditions-data            L412    low-baseline                  L108
core-conditions            L367    mem0-recall                   L199
delta-aggregation          L122    memsys-abstention             L621
derangement-detail         L1432   memsys-pattern-appendix       L1214
example-data               L721    memsys-stats                  L1164
franklin-data              L875    multi-anchor-rates            L949
paired-c1c3-data           L1323   q-improvement-supplemental    L970
per-judge-strictness       L623    response-data                 L446
pre-vs-post-hoc            L56     response-scripts              L444
primary-aggregation        L60     retrieval-overlap-semantic    L1478
robustness-pointer         L813    rubric-abstention-c           L759
share-zero-cut             L1170   spearman-7judge               L565
spec-activation-data       L1040   stats-detail                  L769
statsig                    L120    sycophancy-def                L34
supermemory-scaffold       L1212   tier2-panel                   L1390
tier2-raw-data             L1486   tier2-result-metadata         L1378
treatment-het-fn           L1537   turn-def                      L172
twin2k-persona-size        L170    validity-audit-script         L591
variance-data-paths        L1666   wilcoxon                      L767
within-band-data           L521    wrong-spec-data               L1455
wrong-spec-detection       L1044   wrong-spec-raw-data           L1121
wrong-spec-script          L1016   zep-recall                    L203
```

## Anchor links: PASS

10 in-doc anchor links total (down from 12 in prior sweep; the prior sweep counted L466 + L466 as separate, this sweep treats them as 2 links on L464). All 10 resolve cleanly.

| Line | Anchor | Heading | Status |
|---|---|---|---|
| 38 | `#appendix-h-glossary` | L3191 `## Appendix H. Glossary` | OK |
| 180 | `#7-future-work` | L1684 `## 7. Future Work` | OK |
| 182 | `#7-future-work` | (same) | OK |
| 317 | `#36-evaluation-llm-as-judge-with-calibration` | L450 | OK |
| 464 | `#411-per-question-baseline-engagement-and-the-worked-rubric-example` | L819 | OK (fixed tonight) |
| 464 | `#appendix-d-validity-audit-and-score-distributions` | L2232 | OK |
| 549 | `#4-results` | L669 | OK |
| 645 | `#appendix-a-predicate-vocabulary` | L1814 | OK |
| 661 | `#73-specification-design-and-composition` | L1702 | OK |
| 663 | `#8-data-code-and-reproducibility` | L1746 | OK (fixed tonight) |
| 1046 | `#13-what-we-found` | L104 | OK |

GFM auto-anchor verified for each: lowercase, strip non-[a-z0-9 -], spaces to hyphens. `#411-...` is correct because `4.1.1` collapses dots → `411`. `#8-data-code-and-reproducibility` correctly drops commas in "Data, code, and reproducibility".

## Section pointers: PASS (with one observation)

283 `§X.Y` references in body text. Spot-checked 30+ across §1–§9 and appendices. All resolve to actual section headings.

Specific verifications per checklist:
- §2.5 references in body text: **zero**. §2.5 was successfully removed.
- Orphan §2.1 references to canonical-life-events: **zero**. The string `canonical-life-events` appears nowhere in the paper. The §7.5 canonical-life-events bullet at L1726 is self-contained and §7.4 does not reference it via §2.1.
- §7.4 → §7.5 link at L1714 is valid (both headings exist).
- §5.6 (L1577), §5.7 (L1587), §5.4 (L1551), §4.4.3 (L1295), §4.6.4 (L1428), §6.1–§6.4, §3.6.1–§3.6.6 all verified present.

**Observation (not a break):** L42 says "size and composition per subject in §3.6"; battery composition actually lives in §3.3 (Question Battery Formation, L339) and Appendix B.2 (L1944). This was present in prior drafts and was not introduced tonight.

## Figures: PASS

All 4 embedded figures resolve to existing files in `figures/`:

| Reference | File | Status |
|---|---|---|
| L775 `../figures/fig_4_1_gradient_scatter_v3.png` | exists | OK |
| L900 `../figures/fig_4_2_compression_v3.png` | exists | OK |
| L972 `../figures/fig_4_2_1_question_improvement_rates_v3.png` | exists | OK |
| L1188 `../figures/fig_4_4_1_jaccard_heatmap_v1.png` | exists (NEW tonight) | OK |

Figure 4.4.1 PDF version also present at `figures/fig_4_4_1_jaccard_heatmap_v1.pdf`.

## Tables: PASS (with one observation)

Only one explicit "Table X.Y." label in the body: **Table 2.1** at L190 ("Memory system comparison"). All other tables in §3, §4, and the appendices are unlabeled.

References to Table labels in body text:
- L209 (footnote): "Table 2.1" ✓
- L335: "see §4.1 Table 4.1 and §4.6" — §4.1's main table at L757 has no explicit "Table 4.1" label. The reference is descriptive ("the table in §4.1") and not a formal cross-reference. Same convention as prior drafts.
- L1748: "Per-subject Project Gutenberg IDs are listed in §3.2 Table 3.2" — §3.2 table at L296 has no explicit "Table 3.2" label. Same convention.

This is a paper-wide convention (label one table in §2, leave others unlabeled). The body references at L335 and L1748 are descriptive language, not strict cross-references. Not introduced tonight.

## Citation ↔ §9 reference cross-check: PASS

§9 References at L1768–L1806 contains 17 entries. Every inline `arXiv:XXXX.XXXXX` citation in body text matches a §9 entry:

| Inline citation (line) | §9 entry (line) | Match |
|---|---|---|
| L164 arXiv:2402.17753 (Maharana/LOCOMO) | L1786 | OK |
| L164 arXiv:2410.10813 (Wu/LongMemEval) | L1802 | OK |
| L166 arXiv:2505.17479 (Toubia/Twin-2K) | L1798 | OK |
| L168 arXiv:2407.18416 (Samuel/PersonaGym) | L1794 | OK |
| L174 arXiv:2603.26680 (Xiao/AlpsBench) | L1804 | OK |
| L199 arXiv:2504.19413 (Chhikara/Mem0) | L1776 | OK |
| L203 arXiv:2501.13956 (Rasmussen/Zep) | L1792 | OK |
| L262 arXiv:2507.21509 (Chen/Persona vectors) | L1774 | OK |
| L264 arXiv:2504.14225 (Jiang/Know me) | L1782 | OK |
| L266 arXiv:2509.12517 (Jain/Sycophancy) | L1780 | OK |
| L268 arXiv:2601.10387 (Lu/Assistant Axis) | L1784 | OK |
| L1635 arXiv:2306.05685 (Zheng) | L1806 | OK |
| Appendix F arXiv references (L2976, L2994, L3012, L3030, L3056) | matching §9 entries | OK |

§9 contains 5 entries not directly cited inline by arXiv ID: Bartlett 1932 (book, L1772), Hinton 2015 (referenced by name+year at L260, L1778), Packer 2023 (referenced by name+year+MemGPT at L1788), Perez 2022 (referenced inside `[^sycophancy-def]` at L34, L1790), Sharma 2023 (referenced inside `[^sycophancy-def]` at L34, L1796), Verga 2024 (referenced by name+year at L472, L1635, L1800). All present in §9; no orphan entries.

## Dead URLs: 1 P0 (not introduced tonight; pre-existing)

The paper contains very few HTTPS URLs in prose. Only one explicit `https://` URL in body+footnote text:

| URL | Where | Status |
|---|---|---|
| `https://www.letta.com/blog/benchmarking-ai-agent-memory` | L201 footnote `[^letta-recall]` | **HTTP 200 — verified live** (page title "Benchmarking AI Agent Memory: Is a Filesystem All You Need? \| Letta"). Tonight's fix from `benchmarking-llm-judges-...` is correct. |

GitHub repo references in title block and §8:

| Reference | Where | Status |
|---|---|---|
| `github.com/agulaya24/base-layer` (title block, L6) | "Data + Code:" | **HTTP 404** |
| `github.com/agulaya24/memory-study-repo` (title block, L7; also L1748, L1750) | "Study Repository:" + §8 | **HTTP 404** |
| `github.com/agulaya24/BaseLayer` (§8, L1750) | "The Base Layer pipeline source..." | HTTP 200 (case-sensitive: capital "BaseLayer") |
| `github.com/getzep/zep-papers#5` (L211 in `[^benchmark-disputes]`) | issue ref | HTTP 200, issue closed (matches paper claim) |
| `github.com/mem0ai/memory-benchmarks` (L199 in `[^mem0-recall]`) | benchmarks repo | HTTP 200 |

**This was not introduced tonight.** The 404s on `agulaya24/base-layer` and `agulaya24/memory-study-repo` are either (a) the repos haven't been pushed publicly yet, or (b) the canonical names differ from what is in the title block. The paper at L1750 uses `agulaya24/BaseLayer` (capital B, no hyphen) which is correct and live; the title block at L6 uses lowercase-hyphenated `agulaya24/base-layer` which 404s. There is also no public `agulaya24/memory-study-repo` (separate study repo). Repo visibility check before publish is required.

## Action list

### P0 — fix before publish

1. **Title-block GitHub URLs return 404.**
   - L6 `github.com/agulaya24/base-layer` → 404. The case-correct repo `agulaya24/BaseLayer` is live.
   - L7 + L1748 + L1750 `github.com/agulaya24/memory-study-repo` → 404. Repo is either still private or never pushed.
   - Decision needed before publish: confirm public repo names and either (a) update title block to match live repo names, or (b) push repos publicly under the names in the title block. Without this, the first thing a reader clicks fails.

### P1 — known-pending, deferred

2. **L1210 + L1214 "Appendix B.X" placeholder.** Per `project_v11_paper_active_editing.md`, table is to be moved out of `[^memsys-pattern-appendix]` into a real Appendix B subsection during appendix walk. Paper text and footnote both still say "forthcoming, to be moved during appendix walk." Same status as prior sweep.

### P2 — cosmetic / editorial

3. **L2096 §B.9.3 footnote-style label `[^supermemory-no-retrieval]`** does not correspond to any real footnote in the paper. Renders as literal text inside backticks. Either rename label to `[^memsys-stats]` (the actual footnote that cites this content at L1164) or drop the bracketed label entirely from B.9 subsection headers. Same status as prior sweep.

4. **L2078 "Appendix C / §4.3" content-categorization.** Wrong-spec content lives in §4.3 + §4.6.4, not Appendix C (which is response models / memory-system configs). Suggest dropping "Appendix C / " from L2078. Editorial. Same status as prior sweep.

5. **L42 "in §3.6" pointer for battery composition.** Battery composition is in §3.3 + Appendix B.2, not §3.6. Pre-existing, not tonight. Editorial.

6. **L335 + L1748 informal "Table X.Y" labels.** §4.1's main table (L757) and §3.2's table (L296) have no explicit `**Table X.Y.**` label, while text references them as "Table 4.1" and "Table 3.2". Either add formal labels or rephrase as "the table in §4.1" / "the §3.2 table". Same convention has held across prior drafts.

7. **L13–L22 HTML comment with author note.** `<!-- FUTURE-WORK NOTE (Aarik 2026-04-30, during §4.1 walk) ... -->` does not render to readers but appears in the source markdown. Not a P0 since it's commented out. Decide whether to remove before final publish.

---

## Summary

Both publish-day click failures from prior sweep are resolved (L466 §4.1.1 anchor and L665 §8 anchor). Footnote system is clean (70/70 1:1, including new `share-zero-cut`). New Figure 4.4.1 file exists. Section-pointer audit found no §2.5 orphans and no canonical-life-events orphans. Citation ↔ §9 cross-check passes 100%. Letta URL fixed and live.

**One P0 remaining:** the title-block GitHub URLs (`agulaya24/base-layer`, `agulaya24/memory-study-repo`) return 404. These are the first link a reader clicks. Repo visibility / canonical-name decision needed before publish.

Pre-existing P1/P2 items (Appendix B.X, B.9.3 cosmetic, L2078 categorization) carry forward unchanged. None block publish per their original tracking notes.
