# Final terminology consistency audit — Beyond Recall v11.8 (2026-05-05)

Source: `docs/beyond_recall_v11_8_draft.md` (3,222 lines)
Audit script: `scripts/_audit_terms_v118.py`
Prior pass: `docs/reviews/term_consistency_v11_8_20260505_130216.md`

---

## Delta from prior pass

The prior pass (`term_consistency_v11_8_20260505_130216.md`) was conducted under a stricter anchor/band policy carried forward from v11.6 ("anchor exclusively for rubric integer-points; band only for baseline-grouping"). That policy has since been relaxed per Aarik: "Anchor and integer can be used interchangeably; band is a fractional range around an anchor. Don't over-mechanize; multiple terms can coexist." Under the relaxed policy, most of the prior pass's 9 anchor/band P0s in §3 / Appendix H are USAGE_CORRECT, not violations. Detail in the per-term audit below; net effect is that the prior P0 list collapses to a near-empty residual.

Edits since prior pass that this audit incorporates:

- §2 walk: "Personalization in this paper's sense" lede paragraph added at L158 with explicit distinction between surface-level and deeper sense.
- Glossary entry **Personalization (this paper's sense)** added at L3211 referencing §2 lede.
- §7.4 / §7.5 canonical-life-events reconciliation (no terminology drift introduced).
- Keckley Q21 swap (no terminology drift introduced).
- Share-zero recompute (no terminology drift introduced).

Status of prior pass's flagged items in v11.8:

| Prior-pass item | v11.8 status |
|---|---|
| L36 lowercase "behavioral specification" body prose | **CLOSED.** Now bolded "Behavioral Specification" capitalized. |
| L1392 lowercase "behavioral specification" body prose | **CLOSED.** Now "Behavioral Specification" capitalized. |
| §3.6.2 / Appendix H anchor/band uses (9 P0s) | **DE-FLAGGED.** Now USAGE_CORRECT under relaxed policy; see audit below. |
| L1044 body-prose em-dash | **CLOSED.** Sentence rewritten with period. |
| L1206 body-prose em-dash | **CLOSED.** Replaced with semicolon. |
| Glossary "Behavioral specification" sentence-case | Unchanged from prior. AMBIGUOUS — glossary convention is sentence-case. P2 cosmetic. |
| Franklin first-mention before §4.1.2 | Unchanged from prior. P1 (carried forward; this audit confirms). |

---

## Per-term audit

| Term | Count | Policy adherence | Notes |
|---|---:|---|---|
| Behavioral Specification (cap) | 69 | USAGE_CORRECT | First-mention §1.1 L28; reintroduction §1.1 L36 capitalized; §5.1 footnote L1525 anchors the term. No drift to lowercase in body prose; all 37 lowercase hits are inside verbatim model-response quotes (Examples in §4.3, App E excerpts). |
| behavioral specifications (plural lc) | 0 | USAGE_CORRECT | Clean. |
| Behavioral Specifications (plural cap) | 0 | USAGE_CORRECT | Clean. |
| the spec / the Spec | 69 | USAGE_CORRECT | Used in concrete-instance contexts (§4 mechanism analysis dominant: 31 hits; §7 follow-ups: 8 hits). Mid-paragraph short form after capitalized Behavioral Specification first-mention. |
| the specification | 106 | USAGE_CORRECT | Long-form variant used freely. |
| interpretive layer | 18 | USAGE_CORRECT | Body-primary structural term in §5 (5 hits). §2.1, §2.2 also use cleanly. |
| the layer | 10 | USAGE_CORRECT | All §5 uses are structural (the interpretive layer being introduced). L143 §1.4 is a single use referring to the surface layer that current memory systems already cover (legitimate distinguishing use; reads cleanly in context). |
| anchor / rubric anchor | 11 | USAGE_CORRECT | Body-primary term for rubric integer-points in §3.6.2 and §4. Cross-anchor interpretation rule established at §3.6.2 L492. |
| band / rubric band / integer band | 4+3+3 = 10 | USAGE_CORRECT under relaxed policy | Used as fractional ranges around an integer anchor. L571 §3.6.4, L869 §4.1.2, L505 §3.6.2 all read as fractional-range uses. Not over-mechanized. Coexists with anchor terminology as the user policy permits. |
| representational accuracy | 55 | USAGE_CORRECT | Consistently AI-side property. Glossary L3215 matches body. |
| interpretation | 44 | USAGE_CORRECT | Consistently human-side property. Glossary L3207 matches body. Distinct from "interpretive layer" (the spec) throughout. |
| Personalization (this paper's sense) | defined L158, L3211 | USAGE_CORRECT but see L108 | §2 lede definition explicitly distinguishes surface vs deeper sense. §1.4 L143 uses "surface-level" qualifier; §1.4 L146 uses "user-held, portable, inspectable, traceable, representation-grade" qualifier. §1.3 footnote L108 ("AI personalization (§1.4, §5.2)") provides §-pointer disambiguation. §5 uses (L1515, L1519, L1531, L1577, L1583) are all in the deeper sense, well-anchored after §2 has set up the term. |
| memory system / provider | 27 / 1 | USAGE_CORRECT | "Memory system" body-primary; "provider" used selectively (Table 2.1 column header at L192). "Providers" (plural) in §4.4.1 ("providers do not converge", L1168) is contextually clearly the four memory providers — paragraph ledes "Cross-system retrieval overlap". No paragraph-internal ambiguity flagged. |
| retrieval | 174 | USAGE_CORRECT | Used as the operation (what comes back from the memory system). §4.4.1 retrieval-divergence finding uses "retrieval" consistently. |
| recall | 65 + 12 cap | USAGE_CORRECT | Used as the benchmark axis (LongMemEval, LOCOMO scores). §2.2 Table 2.1 "Published recall score" column. §5.3 lede ("Recall and preference storage") uses recall cleanly. Distinct from retrieval throughout. |
| Tier 1 / Tier 2 | 4 / 30 | USAGE_CORRECT | Tier 1 main study (Haiku 4.5, all 14 subjects) and Tier 2 cross-provider directional probe (Sonnet 4.6 + Gemini 2.5 Pro on 3 subjects) match glossary L3219. The "5 of 6 cells" arithmetic (2 response models × 3 subjects = 6 cells) is internally consistent. |
| substrate | 10 | USAGE_CORRECT | Refers to retrieval/storage infrastructure (Base Layer's MiniLM-L6-v2 + ChromaDB stack). Not used for high-level architectural framing. |
| framework / frameworks | 11 + 9 | USAGE_CORRECT | Natural English uses ("the framework that person uses to reason", "interpretive framework", "methodology framework"). No drift to architectural framing. |
| Benjamin Franklin / Franklin | 4 / 53 | AMBIGUOUS — carried forward from prior pass as P1 | "Benjamin Franklin" first appears §4.1.2 L869 / L871. "Franklin" appears 6+ times before that (L78 footnote, §3.2.1 distribution table, §3.6, §4 lede). Pre-§4.1.2 uses are forward-references; pragmatic, but a strict first-mention reading would call for "Benjamin Franklin" earlier. No change from prior pass. |
| wins / won | 0 / 0 | USAGE_CORRECT | Clean. Aarik's "no wins terminology" feedback respected. |

---

## P0 violations (publish-day blocking)

**None identified.**

The prior pass's P0 list collapses to zero under the relaxed anchor/band policy and after this session's edits (L36, L1392, L1044, L1206 all closed). The paper is term-consistent at the P0 grain.

---

## P1 (strongly recommended)

### P1-1. §1.3 footnote at L108 first uses "AI personalization" before §2's formal definition

**Location:** L108 footnote `[^low-baseline]` reads: *"...This is the population of importance for AI personalization (§1.4, §5.2): on a frontier model serving general AI users, almost everyone falls in or below this band, even people with substantial public output."*

**Issue:** L108 is the first appearance of "AI personalization" in the paper outside the title. §2 lede at L158 defines "personalization in this paper's sense" — the deeper sense. A skim reader hits L108 in §1.3 before §2 establishes the deeper-sense convention.

**Mitigations already present:** §-pointers `(§1.4, §5.2)` give the reader a destination. §1.4 L146 uses qualifier "personalization infrastructure of the first shape (user-held, portable, inspectable, traceable, representation-grade)". §1.4 L143 explicitly contrasts "Personalization remains surface-level" against the paper's deeper sense.

**Recommendation:** Add a forward-reference to §2 lede in footnote `[^low-baseline]`. Two options:

- Option A (minimal): change `(§1.4, §5.2)` → `(§1.4, §2 lede, §5.2)`.
- Option B (explicit): add a parenthetical: *"...the population of importance for AI personalization (the deeper sense; see §2 lede), on a frontier model serving general AI users..."*

Option A is one-character; Option B is more reader-protective for skim readers. Author's call.

**Verdict:** P1 because L108 is in a footnote (less exposed than body prose) but is the first deeper-sense use without local disambiguator. Easy fix.

### P1-2. §4.7 L1492 "established four findings" with five bullet items

**Location:** L1492: *"§4 established four findings:"*

**Issue:** The bullet list immediately following enumerates **five** findings (gradient, compression, content specificity, memory-system interaction, retrieval divergence). Off-by-one count.

**Cross-reference:** §1.3 ("seven findings") and §5.1 ("seven findings together establish") are mutually consistent: §5.2-§5.6 fold seven §1.3 findings into five subsections (gradient + step-changes → §5.2; retrieval divergence → §5.3; layering → §5.4; wrong-spec + hedging → §5.5; compression → §5.6). The §4.7 "four" likely reflects a stale count from before retrieval divergence was promoted.

**Recommendation:** Change L1492 from "four findings" to "five findings" to match the bullet list as written. (Out of strict terminology scope but flagged because it interacts with the §1.3 / §5.1 / §4.7 finding-count framing.)

**Verdict:** P1 borderline — count error, not a terminology error, but reader-visible at the §4 → §5 transition.

### P1-3. Franklin first-mention pre-§4.1.2 (carried forward)

**Issue:** Per prior pass — body uses "Franklin" (L78 footnote, §3.2.1 table at ~L335, §4 lede L680, §4.1 main results table L777-811) before §4.1.2 L871 first introduces "Benjamin Franklin". A strict first-mention rule would put full name at first body-mention.

**Recommendation:** Change first body-mention (the §3.2.1 table row at ~L335) from "Franklin (known-figure control, not in main study)" to "Benjamin Franklin (known-figure control, not in main study)". §4.1.2 L869 / L871 can stay as-is.

**Verdict:** P1 — readability issue for new readers; doesn't block publish but is a small fix.

---

## P2 (cosmetic)

### P2-1. Glossary entry "Behavioral specification." sentence-case (L3203)

The glossary heading at L3203 is sentence-case (`**Behavioral specification.**`); the body uses the capitalized term "Behavioral Specification" consistently. Glossary convention is sentence-case across all entries (`**Anchors / Core / Predictions.**`, `**Behavioral prediction.**`, `**Multi-anchor crossing.**`, etc.), so this matches glossary convention.

**Recommendation:** Leave as-is. If preferred for term-discipline, could change to `**Behavioral Specification.**` (would be the only deviation from glossary sentence-case convention).

### P2-2. §3.6.2 paragraph-internal mixing of "anchor" and "integer band" terms

L494-L515 of §3.6.2 mixes "single anchor", "single integer band", "rubric integer anchor", and "anchor crossings". Under the relaxed policy this is permissible — the terms can coexist — but a single section using four near-synonymous handles for the same concept can read churn-y to first-time readers.

**Recommendation:** Optional pass to standardize on "anchor" for integer-points and "band" only for fractional ranges within §3.6.2. Per Aarik's "don't over-mechanize" guidance, this is **not** a P0 / P1 — it is stylistic only.

### P2-3. L869 §4.1.2 "Franklin sits a full anchor band above the main study's upper end"

"Anchor band" reads as the fractional region around an integer anchor — this is policy-permitted. Could read as "Franklin sits a full rubric anchor above..." for slightly cleaner integer-distance framing. Author's call.

---

## Glossary cross-check

Every glossary entry in Appendix H (L3191-3221) is used at least once in the body in a way consistent with its definition:

| Glossary term (App H line) | Body usage | Consistency |
|---|---|---|
| 5-judge primary panel (L3195) | §3.6.3, §4 throughout, §6.2 | Consistent |
| 7-judge sensitivity panel (L3197) | §3.6.3, §4.6 | Consistent |
| Anchors / Core / Predictions (L3199) | §3.7 builds out, §2.3 worked example | Consistent |
| Behavioral prediction (L3201) | §1.1, §3.6, §4 | Consistent |
| Behavioral specification (L3203) | Throughout | Consistent (modulo P2-1 capitalization note) |
| Cross-anchor interpretation rule (L3205) | §3.6.2 L492 establishes it; §4 reads through it | Consistent |
| Interpretation (L3207) | §1.1 L28 introduces; §5.3 L1547 develops | Consistent |
| Multi-anchor crossing (L3209) | §3.6.2 L507; §4.1, §4.2 | Consistent |
| Personalization (this paper's sense) (L3211) | §2 lede L158 defines; §1.4 L146 contrasts surface vs deeper; §5 throughout uses deeper sense | Consistent (modulo P1-1 §1 footnote forward-ref) |
| Refusal (abstention) (L3213) | §3.6.6, §4.4.2 Pattern 3 | Consistent |
| Representational accuracy (L3215) | §1.1 L30 introduces; §1.2, §2, §3, §4, §5 throughout | Consistent |
| Specification-effect claim (L3217) | §3.6.4 L559 | Consistent |
| Tier 1 / Tier 2 (L3219) | §3.5, §4.6.1 throughout | Consistent |
| Wrong-spec control (L3221) | §3.4, §4.3 | Consistent |

**§2 lede / glossary cross-link confirmation:** "Personalization (this paper's sense)" entry at L3211 references "§2 lede"; §2 lede at L158 defines the term. Round-trip works.

---

## Summary

- **P0:** 0 items.
- **P1:** 3 items — all small, targeted, non-blocking for publish-day in the strict sense, but worth landing before final freeze.
- **P2:** 3 cosmetic items.

The paper is term-consistent with the locked v11.8 policy. The prior pass's larger P0 list reduces under (a) the relaxed anchor/band policy ("don't over-mechanize"), (b) closed L36 / L1392 capitalization fixes already present in v11.8, and (c) closed L1044 / L1206 em-dash fixes already present in v11.8. Net residual is the 3 P1 items above.

The §2 lede + glossary additions for "Personalization (this paper's sense)" landed correctly. Surface-vs-deeper sense distinction is structurally cleaner in v11.8 than in earlier drafts.
