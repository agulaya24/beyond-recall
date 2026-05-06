# §1-§5 Section-Pointer Corrections (v11.8)
_Generated: 20260505_095340_
_Source paper: beyond_recall_v11_8_draft.md_
_Audit basis: section_pointer_audit_v11_8_20260505_094736.md_

## Ground truth: current §5 structure (v11.8)

| § | Title | Line |
|---|---|---:|
| §5.1 | Synthesis: what the seven findings together establish | 1509 |
| §5.2 | Why the gradient is the load-bearing finding | 1521 |
| §5.3 | Retrieval is not interpretation | 1533 |
| §5.4 | Composition with retrieval | 1543 |
| §5.5 | Wrong-spec mechanism and hedging elimination | 1557 |
| §5.6 | Compression and what makes personalization operationally tractable | 1569 |
| §5.7 | Privacy and the case for user-held representation | 1579 |
| §5.8 | Closing argument | 1591 |

The §5 swap (S119) moved several content blocks. Net effect for cross-refs from §1-§5:
- "Population of relevance / low-baseline equity property" content -> now §5.2 (was §5.3 in older drafts)
- "Retrieval-divergence / interpretation distinct from recall" content -> now §5.3 (carry-forward)
- "Composition / serving routes / dynamic activation" content -> now §5.4 (was scattered through §5.5)
- "Wrong-spec mechanism / hedging" content -> now §5.5 (was §5.5 with a different focus, OR §4.3 carry-back)
- "Compression / load-bearing property" content -> §5.6 (NEW subsection added during walk)
- "Privacy / inspectability / user-held" content -> §5.7 (was §5.6)
- "Closing argument" -> §5.8 (was §5.7)

The legacy §5.5 in earlier drafts contained "serving design considerations" (dynamic activation, modifiability, temporality, canonical life events, topic decomposition). That content is no longer in §5.5; some of it lives in §5.4 and §5.6, but most has migrated to §7.4 (Production serving and infrastructure). References in §1-§5 prose pointing to §5.5 for "temporality / serving / dynamic activation" content are stale.

---

## Summary
- Refs reviewed in §1-§5 (ref-line < 1601): **141**
- OK: **136**
- WRONG: **3**
- AMBIGUOUS: **2**

The §5-internal cross-refs (§5.3 -> §5.4, §5.6 -> §5.7) are correct in v11.8. The drift is concentrated in §1 prose pointing back to old §5.5 for temporality content, and in two §1.3 footnote references that pointed at §5.3 for population-of-relevance content (now §5.2).

---

## WRONG (mechanical fix recommended)

| Ref line | Current §ref | Proposed §ref | Prose excerpt | Rationale |
|---:|---|---|---|---|
| 108 | §5.3 | §5.2 | `"Low baseline" means C5 ≤ 2.0 on the 1-5 rubric. This is the population of importance for AI personalization (§1.4, §5.3): on a frontier model serving general AI users, almost everyone falls in or below this band` | The "population of importance / population of relevance" framing is the load-bearing claim of §5.2 ("Why the gradient is the load-bearing finding"), which states verbatim "Every living user of AI now and into the future fits the low-baseline band. The population of relevance for AI personalization is the long tail of users whose private reasoning is not in any training corpus." §5.3 in v11.8 is "Retrieval is not interpretation" and does not carry the population claim. |
| 178 | §5.5 | §7 only | `Subjects whose reasoning shifts substantially across their corpus ... may not be well-represented by a single snapshot specification, which is one reason temporality is a flagged follow-up (§5.5, [§7](#7-future-work)).` | §5.5 in v11.8 ("Wrong-spec mechanism and hedging elimination") does not discuss temporality at all. The temporality follow-up is developed in §7.5 ("Stateful-agent implementations and temporal drift tracking"). Drop the "§5.5" half of the citation; keep §7 (or replace with §7.5 directly). |
| 180 | §5.5 | §7.5 | `This is separate from the stability premise above and adjacent to it, and sits alongside temporality (§5.5) as a follow-up in [§7](#7-future-work).` | Same drift as line 178. Temporality and canonical-life-events follow-ups live in §7.5; §5.5 in v11.8 is wrong-spec/hedging. The natural target for "temporality" is §7.5; "canonical life events" is mentioned in §7.4. Replace §5.5 with §7.5 (or simply drop the §5.5 cite since §7 is already named). |
| 703 | §5.3 | §5.2 | `which is the population of relevance for AI personalization (§1.4, §5.3).` | Same as line 108. "Population of relevance" framing is §5.2's load-bearing claim, not §5.3 (Retrieval is not interpretation). |
| 699 | §5.3 | §5.2 | `AI users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.3), and they are the subjects for whom the lift is largest and the spec is most needed.` | The "users not in any training corpus = the population of relevance / low-baseline by construction" argument is §5.2, not §5.3. §5.3 establishes the retrieval-vs-interpretation separation; it does not argue that low-baseline subjects are the population of relevance. |

---

## AMBIGUOUS (manual review needed)

| Ref line | §ref | Prose excerpt | Recommended action |
|---:|---|---|---|
| 1044 | §1.3 (anchor `#13-the-core-finding`) | `28.8% → 0.0% under the strict-pattern classifier, 41.2% → 0.4% under the broader-pattern classifier (rule definitions in [§1.3](#13-the-core-finding) footnote).` | Numeric ref §1.3 is OK (§1.3 footnotes do define hedging rules). The Markdown anchor `#13-the-core-finding` is stale: §1.3 is now titled "What we found", so the auto-generated anchor is `#13-what-we-found`. **Action: update the anchor to `#13-what-we-found`** to keep the link clickable. (Out of strict scope for the §-pointer audit, but worth catching in the same pass.) |
| 567 | §5 (in `stats_update.md` external doc) | `Full matrix in `docs/research/stats_update.md` §5.` | This is a §5 reference to the external file `docs/research/stats_update.md`, NOT the paper. False positive in the mechanical audit. **Action: leave as-is.** |

---

## Verified OK (high-confidence subset)

The following §-refs in §1-§5 prose match their target subsection's actual content. Sample (not exhaustive — see audit report for the full list of 141 verified refs):

| Ref line | §ref | Reason |
|---:|---|---|
| 26 | §2.2 | Memory systems landscape — matches §2.2 title and content |
| 28 | §3.7 | Pipeline definition — matches §3.7 |
| 30 | §2.1 | Benchmark positioning — matches §2.1 |
| 32 | §3.6 | Rubric — matches §3.6 |
| 34 | §2.4 | Sycophancy / Jain et al — matches §2.4 |
| 50 | §4.3 | Wrong-spec — matches §4.3 |
| 52 | §4.2 | Compression — matches §4.2 |
| 56 | §4.4.1, §4.6.5, §4.5, §3.6.6, §4.6.4 | All five post-hoc artifact pointers — match |
| 138 | §1.2 | Population of relevance — defined in §1.2, matches |
| 146 | §5, §7 | "Extended discussion" / "safety, alignment, and deployment implications" — match |
| 264 | §1.3 Mechanism | §1.3 has a Mechanism subsection at line 126 — matches |
| 266 | §1.3 Mechanism, §4.3 | §1.3 Mechanism + §4.3 hedging — both match |
| 1511 (within §5.1) | §4.6 | "robustness checks" — matches §4.6 |
| 1515 (within §5.1) | §7, §4.6 | both match |
| 1529 (within §5.2 footnote) | §4.1 | Treatment-heterogeneity rejected in §4.1 — matches |
| 1539 (within §5.3) | §5.4 | "§5.4 picks up what happens when interpretive layer is composed with memory-system retrieval" — matches §5.4 title "Composition with retrieval" |
| 1545 (within §5.4) | §5.3 | "The implication of §5.3 is..." — matches §5.3 (Retrieval is not interpretation) |
| 1545 (within §5.4) | §4.4.2 | three composition patterns — matches §4.4.2 |
| 1547 (within §5.4 footnote) | §4.4.3 | Keckley Q21 — matches |
| 1553 (within §5.4) | §7.4 | dynamic serving — matches §7.4 |
| 1559 (within §5.5) | §4.3, §4.6.4 | wrong-spec controls + sensitivity — match |
| 1561 (within §5.5) | §2.4 | Jain et al — matches |
| 1563 (within §5.5) | §4.3, §5.3, §7 | Bernal Diaz Q16 (§4.3), retrieval-divergence (§5.3), component ablation (§7) — all match |
| 1565 (within §5.5) | §5.6, §5.7 | Compression next-section + Privacy next-section — both match |
| 1571 (within §5.6) | §4.2 | compression evidence — matches |
| 1573 (within §5.6) | §4.3 | wrong-spec controls — matches |
| 1581 (within §5.7) | §1.4 | inspectability requirement — matches §1.4 ("user-held, portable, inspectable, traceable") |
| 1583 (within §5.7) | §3 | extraction operations described in §3 — matches |
| 1585 (within §5.7) | §1.4, §4.3 | both match |
| 1587 (within §5.7) | §7 | safety/deployment implications — matches §7.6 (and broader §7) |
| 1597 (within §5.8) | §7 | matches |

---

## Notes on excluded refs

- **HTML comment block at lines 14-21** (FUTURE-WORK NOTE inside `<!-- ... -->`) contains §3.6.2, §3.7, §4.1.1 references. These are author notes, not rendered prose. All three targets exist and the content claims are correct (multi-anchor crossings, Hamerton spec examples, Seacole Q2). Leave as-is.
- **Line 567**: `stats_update.md §5` is a section reference inside an external doc, not a paper ref. Leave as-is.
- **Refs at lines >= 1601 (§6+)**: out of scope per task instructions. They will be reviewed during §6-§9 walks. (Heads-up: spot-check found that §6 prose at lines 1607, 1623, 1637 contains the SAME §5.5/§5.7 drift — ref §5.7 for "open research questions catalogued" and "rubric limitations", and ref §5.5/§5.7 for "serving-strategy gap". §7.4 at line 1702 also says "These five items appear in §5.5" which is now stale. These should be folded into the §6-§9 walk.)

---

## Mechanical fix list (ready to apply)

Three unambiguous edits in §1 prose:

```
File: docs/beyond_recall_v11_8_draft.md

# Fix 1: line 108 (footnote ^low-baseline)
- "(§1.4, §5.3): on a frontier model"
+ "(§1.4, §5.2): on a frontier model"

# Fix 2: line 178 (held-out design footnote prose)
- "temporality is a flagged follow-up (§5.5, [§7](#7-future-work))"
+ "temporality is a flagged follow-up ([§7.5](#75-stateful-agent-implementations-and-temporal-drift-tracking))"
  -- OR if a single §7 cite is preferred for consistency with the rest of the paper:
+ "temporality is a flagged follow-up in [§7](#7-future-work)"

# Fix 3: line 180 (canonical life events para)
- "sits alongside temporality (§5.5) as a follow-up in [§7](#7-future-work)"
+ "sits alongside temporality as a follow-up in [§7](#7-future-work)"
  -- OR if a specific subsection is preferred:
+ "sits alongside temporality (§7.5) as a follow-up in [§7](#7-future-work)"
```

Two unambiguous edits in §4 prose (formally inside §4 = part of "§1-§5" scope):

```
# Fix 4: line 699 (within §4.1 prose)
- "AI users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.3)"
+ "AI users whose private reasoning is not in any training corpus sit at or near the rubric floor by construction (§5.2)"

# Fix 5: line 703 (within §4.1 prose)
- "which is the population of relevance for AI personalization (§1.4, §5.3)."
+ "which is the population of relevance for AI personalization (§1.4, §5.2)."
```

One anchor-target edit (clickable-link bug, not strictly a §-pointer drift):

```
# Fix 6: line 1044 (within §4.3 prose)
- "(rule definitions in [§1.3](#13-the-core-finding) footnote)"
+ "(rule definitions in [§1.3](#13-what-we-found) footnote)"
```

---

## Drift map (for the author's mental model)

| Old §5 subsection (pre-walk) | Content topic | New home in v11.8 |
|---|---|---|
| §5.5 | Serving / dynamic activation / temporality / canonical life events / topic decomposition | Mostly §7.4 (Production serving) and §7.5 (temporal drift). NOT in current §5.5. |
| §5.6 | Privacy / inspectability / user-held | §5.7 (intra-§5 shift) |
| §5.7 | Closing argument | §5.8 (intra-§5 shift) |
| (new) §5.6 | Compression as load-bearing property | Added during walk |

The five WRONG instances all stem from these two pieces of drift:
1. **"Population of relevance" content moved from old §5.3 to new §5.2** (one paragraph reordering during the §5 walk). Lines 108, 699, 703 still cite the old §5.3.
2. **"Temporality / serving design considerations" content evicted from §5.5 entirely**, now lives in §7.4 / §7.5. Lines 178, 180 still cite the old §5.5.

No drift was found in §1->§4 cross-refs; §1.X / §2.X / §3.X / §4.X targets are stable.
