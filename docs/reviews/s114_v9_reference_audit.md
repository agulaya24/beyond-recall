# v9 Reference Audit — Post-Restructure Stale References

**Date:** 2026-04-23
**Source file:** `docs/beyond_recall_v9_draft.md` (2,323 lines)
**Purpose:** identify every §N / §N.N / Section N / Figure N reference that became stale under the v9 section restructure.
**Constraint:** audit only — v9 was not modified.

---

## Summary counts

| Category | Count |
|---|---:|
| Total `§N(.N)*` references in v9 | ~215 (most are correct and unchanged) |
| `Section N` / `section N` literal references | 0 |
| `Figure N` references | 3 (all correct: 4.1, 4.2, 4.2.1) |
| **Stale references needing a fix** | **34 across 23 lines** |
| **Ambiguous cases flagged for manual review** | **2** |

Figure 9 / Figure 11 (mentioned as possible stale concerns in the task) do not appear in v9, so that dimension of the audit is clean.

---

## Stale references, grouped

Ordered by line number. Where one line contains several stale refs, they are grouped in one row. "Proposed fix" is the single edit needed; "Reasoning" ties the fix to the new tree.

| # | Line | Current text (excerpt) | Proposed fix | Reasoning |
|---|---:|---|---|---|
| 1 | 64 | `Full methodology and results are in §4.4.1 and §4.7.` | `...in §4.5.` | Letta stateful path is exclusively in new §4.5 now. New §4.4.1 is "Aggregate Performance Across Systems" (archival only); the stateful discussion was removed from §4.4.1. Collapse to a single §4.5 reference. |
| 2 | 121 | `flagged as follow-up in §7.` | `flagged as follow-up in §8.` | §7 no longer exists as a top-level section; old §7 content is now §5.7 Safety Alignment. The referent here is a Future Work follow-up, which lives in §8. Confirm by context: the sentence is about a differentiated battery follow-up, which §8.1 explicitly lists. |
| 3 | 176 | `see §4.3 and §4.4.1 and §4.7` | `see §4.3 and §4.5` | Same collapse as row 1: Letta stateful is only in §4.5. New §4.4.1 no longer covers stateful. Preserve §4.3 (mechanism), replace `§4.4.1 and §4.7` with `§4.5`. |
| 4 | 188 | `prediction as its target, and the framing in this paper is different (§5.2).` | `...is different (§2.3.1).` | Old §5.2 "Recall, prediction, persona" was deleted; its content moved into new §2.3.1 "What Existing Benchmarks Measure vs What Representational Accuracy Tests," which is the section that discusses this Twin-2K framing distinction. New §5.2 is "What the study demonstrates" and does not cover this. |
| 5 | 206 | `...one reason temporality is a flagged follow-up (§4.8, §8).` | `...(§5.5, §8).` | Old §4.8 "Scaling and Practical Implications" is now §5.5 Practical Implications. Temporality is explicitly in new §5.5 ("Temporality: a snapshot representation"). §8 ref is correct. |
| 6 | 208 | `sits alongside temporality (§4.8) as a follow-up in §8.` | `sits alongside temporality (§5.5) as a follow-up in §8.` | Same as row 5. |
| 7 | 238 | `Our hedging-reduction finding (§1.3 Mechanism, §5.5)` | **AMBIGUOUS — flag for manual review** | Old §5.5 was Architectural Convergence; new §5.5 is Practical Implications. Neither owns the hedging finding. Hedging is in §1.3 and §4.3. Author may want `(§1.3 Mechanism, §4.3)` or `(§1.3 Mechanism, §5.4)` (since §5.4 Content specificity and mechanism is the discussion-side home for mechanism). Author must resolve. |
| 8 | 400 | `reported in §4.4.1 and §4.7 alongside other Letta findings` | `reported in §4.5 alongside other Letta findings` | Same collapse as rows 1 and 3: stateful Letta is §4.5 only. |
| 9 | 412 | `Tier 2 results and subject-selection rationale are in §3.4.1 and §4.8.` | `...in §3.4.1 and §4.6.1.` | Old §4.8 did not own Tier 2; the Tier 2 cross-provider replication lives in §4.6.1 (Cross-provider response generation / Tier 2 replication) under new Robustness. §3.4.1 correct. |
| 10 | 506 | `(robustness confirmed in §4.5).` | `(robustness confirmed in §4.6).` | Old §4.5 "Robustness" is now §4.6. |
| 11 | 589-596 | Section 4 TOC bullet list (8 bullets) | Rewrite four bullets; see sub-table below | This is the single most visible block of staleness. The TOC describes §4 as having 8 subsections in old numbering; the new tree has §4.1, §4.2, §4.3, §4.4 (with 4.4.1, 4.4.2, 4.4.3), §4.5, §4.6. See detailed sub-fix below. |
| 12 | 598 | `The 7-judge sensitivity check ... is reported in §4.5.` | `...is reported in §4.6.` | Robustness now §4.6. |
| 13 | 1096 | `described separately in §4.4.1 and §4.7.` | `described separately in §4.5.` | Letta stateful collapse; §4.4.1 is archival only now. |
| 14 | 1208 | `reported separately in §4.5 as an architectural-convergence test` | **Correct as-is** — no change | This sentence already points to §4.5 as the new location. Verify this is intentional (it is consistent with the restructure). |
| 15 | 1295 | `§4.7 asks: if the Behavioral Specification improves prediction...` | `§4.5 asks: if...` | **SELF-REFERENCE**: this sentence is inside the new §4.5 (Architectural Convergence: Letta Stateful-Agent) describing what its own section asks. The old number survived the rename. |
| 16 | 1353 | `The §4.7 matched-model gap may be attributable...` | `The §4.5 matched-model gap...` | Same as row 15 — self-reference inside new §4.5. |
| 17 | 1374 | `§4.5 reports the sensitivity of the core findings to each.` | `§4.6 reports...` | Self-reference inside new §4.6 (Robustness). |
| 18 | 1467 | `per-question analysis (§4.4, §4.6) shows` | `(§4.4.2, §4.4.3)` | Old §4.6 "Interpretation vs. Recall" was folded into new §4.4.2 (Common Mechanisms) + §4.4.3 (Keckley Q21 case study). The per-question mixture analysis lives in those new subsections. `§4.4` is ambiguous — the specific per-question treatment is in 4.4.2/4.4.3. |
| 19 | 1471 | `The target is reachable by more than one architectural path (§4.7).` | `...(§4.5).` | Architectural convergence moved from §4.7 to §4.5. |
| 20 | 1473 | `how AI memory systems should be evaluated (§5.2), ... a general AI-design primitive rather than a Base Layer-specific claim (§5.5)` | Two fixes in one sentence: (a) `(§5.2)` describing memory-system evaluation is **self-reference** — sentence is inside §5.2 itself, the entire sentence needs restructure, see notes; (b) `(§5.5)` for "general AI-design primitive" is wrong — new §5.5 is Practical Implications, not a design-primitive framing | This whole sentence is a roadmap at the end of §5.2 describing subsequent §5 subsections. Current version has `§5.2` pointing at itself (the eval framing is the whole of §5.2) and `§5.5` pointing at old Architectural Convergence (now moved into §4.5). Proposed rewrite: drop the `§5.2` self-ref, and replace `§5.5` with either a pointer to §4.5 (architectural convergence) OR update the description to match new §5.5 (Practical Implications). Author judgment needed on intent. |
| 21 | 1502 | `§4.6 Yung Wing Q31` | `§4.4.2 Yung Wing Q31` | The Yung Wing Q31 example is now in §4.4.2 Pattern 2 cross-system example (verified at line 1250). Old §4.6 no longer exists. |
| 22 | 1505 | `The dynamic-activation proposal in §4.8` | `The dynamic-activation proposal in §5.5` | Dynamic activation is discussed in new §5.5 Practical Implications (lines 1537-1546). |
| 23 | 1515 | `§4.8 in ... identify where the optimum sits for a given deployment and user population.` (the line reads "piecewise component analysis flagged in §4.8") | `...flagged in §5.5.` | Piecewise component analysis is in new §5.5 (line 1583). |
| 24 | 1521 | `§4.1 through §4.7 establish what the Behavioral Specification does and why it works. §4.8 is a practical note...` | `§4.1 through §4.6 establish... §5.5 is a practical note...` | **SELF-REFERENCE inside new §5.5**. Section opens by describing itself using old §4.8 number. Results sections now run §4.1 through §4.6 (§4.7 and §4.8 no longer exist). |
| 25 | 1546 | `Flagged in §8.` | **Correct** | No change. |
| 26 | 1573 | `Flagged in §8.` | **Correct** | No change. |
| 27 | 1620 | `what §5.1 summarizes` | `what §5.2 summarizes` | Old §5.1 "What the study demonstrates" is now §5.2. Sentence is inside §5.6 referring to the summary. New §5.1 is "The Anti-Pattern" which is not a summary of demonstrations. |
| 28 | 1628 | `Component ablation ... Flagged in §8.` (context: "which layer of the specification carries Pattern 1...") | The sentence ends `Flagged in §8.` — correct. **However, earlier in line 1628 reads `§4.8, §5.4, §5.6` from row 8.3** — check | Actually line 1628 is clean on section numbers — Flag for row: already correct. Removed from stale list. |
| 29 | 1636 | `The Letta stateful comparison in §4.7 served Base Layer's unified ...` | `The Letta stateful comparison in §4.5 served...` | §4.7 → §4.5. |
| 30 | 1686 | `The serving-strategy gap ... is in §4.8 and §5.6.` | `...is in §5.5 and §5.6.` | §4.8 → §5.5 (Practical Implications now holds the serving-strategy discussion). |
| 31 | 1698 | `Main-study coverage prioritizes the conditions and subjects central to H1 through H5 (§4.1 through §4.4).` | **Correct as-is** | §4.1-§4.4 still covers H1-H5 in new tree. No change. |
| 32 | 1702 | `§4.4, §4.7` (Letta stateful-agent exploration) | `§4.4, §4.5` | §4.7 → §4.5. |
| 33 | 1722 | `priority authoring-pipeline follow-up (§4.8, §5.4, §5.6).` | `(§5.5, §5.4, §5.6).` | §4.8 → §5.5. |
| 34 | 1724 | `Alongside component ablation: ... (§4.7, §5.5);` and `§4.7 gap on the matched-rerun subjects (§4.7, §5.6).` | Two fixes: `(§4.7, §5.5)` → `(§4.5, §5.5)`; `(§4.7, §5.6)` → `(§4.5, §5.6)` | §4.7 → §4.5 in both occurrences. Note §5.5 stays — it is the correct new Practical Implications reference for deployment-gap discussion. |
| 35 | 1728 | `Five production-realistic serving-layer follow-ups follow directly from §4.8:` | `...follow directly from §5.5:` | §4.8 → §5.5. |
| 36 | 1732 | `canonical life events (automatic detection or user-supplied annotation of within-person behavioral shifts, §5.2)` | `...(within-person behavioral shifts, §2.3.1)` | Canonical life events are introduced in new §2.3.1 (line 208), not in new §5.2. Old §5.2 was deleted. |
| 37 | 1736 | `The §4.7 Letta stateful-agent comparison is N=3 subjects` | `The §4.5 Letta stateful-agent comparison...` | §4.7 → §4.5. |
| 38 | 1737 | `The open question §7 raises` | `The open question §5.7 raises` | Old top-level §7 Safety Alignment is now §5.7. |

---

## Detail for row 11: §4 TOC bullet list (lines 589–596)

The bullet block must be rewritten. Current vs. proposed:

| Line | Current | Proposed |
|---:|---|---|
| 589 | `**§4.1. The Cross-Subject Gradient.**` | unchanged |
| 590 | `**§4.2. Compression: Structure vs. Raw Text.**` | unchanged |
| 591 | `**§4.3. Mechanism: Content, Not Format.**` | unchanged |
| 592 | `**§4.4. Memory-System Composition.**` | unchanged (or expand to cover 4.4.1/4.4.2/4.4.3 if desired) |
| 593 | `**§4.5. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions?` | **§4.5. Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution. |
| 594 | `**§4.6. Interpretation vs. Recall.** Where does the specification help and where does it hurt at the per-question level?` | **§4.6. Robustness and Sensitivity.** Does the effect hold across response models, judges, and replication conditions? |
| 595 | `**§4.7. Architectural Convergence.** Letta's stateful-agent path independently arrives at a similar solution.` | **DELETE** (content now at §4.5, see row above) |
| 596 | `**§4.8. Scaling and Practical Implications.** Cost, context, and deployment considerations.` | **DELETE** (content now at §5.5, outside §4) |

Net effect: §4 TOC goes from 8 bullets to 6 bullets. §4.6 (old "Interpretation vs. Recall") content is folded into §4.4.2 + §4.4.3 and should either be flagged in the §4.4 bullet or dropped from the TOC.

---

## Ambiguous cases (need author resolution)

### Ambiguous 1 — Line 238 `§5.5` for hedging
The sentence reads: *"Our hedging-reduction finding (§1.3 Mechanism, §5.5) is consistent with this reading..."*. Old §5.5 was Architectural Convergence (no hedging content). New §5.5 is Practical Implications (no hedging content). The hedging analysis lives in §1.3 and §4.3. Author options:
- Drop the `§5.5` reference entirely: *"(§1.3 Mechanism)"*.
- Point it to the mechanism-side discussion: *"(§1.3 Mechanism, §5.4)"* — §5.4 "Content specificity and mechanism" is the discussion-side home for the mechanism story.
- Point it to §4.3: *"(§1.3 Mechanism, §4.3)"* — the Results-side Mechanism section where hedging numbers are reported in the "Hedging evidence carries the same implication" passage (line 958).

### Ambiguous 2 — Line 1473 self-reference structure
The sentence is a roadmap inside new §5.2 describing remaining §5 subsections. The `§5.2` reference inside §5.2 is a self-reference. The `§5.5` reference describes it as a "general AI-design primitive" framing, which no longer matches new §5.5 Practical Implications. Options:
- Rewrite as a clean map: *"The remaining subsections of §5 develop what these results imply for real users outside the sample (§5.3), for the mechanism of interpretation (§5.4), for practical deployment (§5.5), for measurement gaps (§5.6), and for safety alignment (§5.7)."*
- Drop the §5.2 self-reference and update the §5.5 gloss.

---

## Things confirmed clean (spot-checked, no change needed)

- All `§1.x`, `§2.x` (except the §5.2 → §2.3.1 pointer on L188), `§3.x` references — unchanged sections.
- §4.1, §4.2, §4.3, §4.4 references — numbering preserved.
- §6 and §6.x references — still correct (Limitations).
- §8 and §8.x references — Future Work; all correct.
- Figure references (4.1, 4.2, 4.2.1) — all three correct; no Figure 9 or Figure 11 present in v9.
- `(§3.7.6)`, `(§3.7.2)`, `(§3.7.3)`, `(§3.7.4)` — all unchanged targets.
- Appendix references (A, B, C, D, E) — correct.

---

## Total fixes needed (for batch apply)

- **32 definite fixes** across lines listed above (rows 1–6, 8–13, 15–24, 27, 29–30, 32–38).
- **1 multi-bullet TOC rewrite** at lines 589–596 (row 11).
- **2 ambiguous cases** flagged for author decision (row 7 line 238; row 20 line 1473 restructure).

Highest-priority fixes by visibility:
1. §4 TOC block (L589-596) — readers hit this immediately at the start of Results.
2. §5.2 roadmap self-reference (L1473) — opens the Discussion.
3. §4.5 self-references (L1295, L1353) inside new §4.5 — the section literally misnames itself.
4. §5.5 self-reference (L1521) — opens Practical Implications.
5. §7 → §5.7 at L1737 — anchors the Safety Alignment follow-up.

All other fixes are inline body references that follow a small set of rename rules:
- §4.5 (old Robustness) → §4.6
- §4.6 (old Interpretation vs Recall) → §4.4.2 or §4.4.3 (by context)
- §4.7 (old Letta) → §4.5
- §4.8 (old Scaling) → §5.5
- §5.1 (old What the study demonstrates) → §5.2
- §5.2 (old Recall/prediction/persona) → §2.3.1
- §7 (old Safety) → §5.7
