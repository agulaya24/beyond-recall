# Section 3 "Study Design" — Verification Report

**Target:** `docs/beyond_recall_v8_draft.md` §3 (lines 207-429)
**Cross-reference anchors:** v8 §1.2 (locked, lines 30-76), v8 §1.3, `KEY_FINDINGS.md`, `DATA_REFERENCE.md`
**Generated:** Session 115 (2026-04-17) pre-launch verification
**Overall status:** Mostly clean; several concrete issues flagged for fix before lock.

---

## A. §3 vs. §1.2 Coherence Check

| Claim | §1.2 says | §3 says | Match? | Note |
|---|---|---|---|---|
| Condition C5 (baseline) | "No context… Nothing. Model answers from pretraining alone. Pretraining baseline." | §3.5: "C5 Baseline. Nothing. Floor: what the model knows from pretraining alone." | ✅ Match | — |
| Condition C1 controlled | "Retrieval alone, controlled — Top-k facts from shared fact pool." | §3.5: "C1 Retrieval only. Top-k facts retrieved by the system." | ✅ Match | §3.5 collapses C1 controlled + C1 native into one ID. §1.2 labels them distinctly as "C1" and "C1 native." Minor presentation divergence — §3.5 says "Two ingestion configurations per system: Controlled / Native" just below, so meaning preserved, but the ID nomenclature differs. Recommend adding "(C1 native for each system's own ingestion)" to §3.5. |
| Condition C2a (spec only) | "Spec alone — Behavioral Specification, no retrieval/facts/corpus." | §3.5: "C2a Spec only — Full behavioral specification (~5K tokens)." | ✅ Match | — |
| Condition C2c (wrong spec) | "Two variants: v1 uses Franklin's spec for all other subjects; v2 applies a random derangement, seed-fixed." | §3.5 wrong-spec block: "v1: Franklin's specification applied to each subject. v2: Random derangement. Fixed seed 42." | ✅ Match | Seed number (42) stated in §3.5 but not §1.2; consistent. |
| Condition C3 (retrieval + spec) | "Retrieval + spec, controlled / native" | §3.5: "C3 Retrieval + spec. System's retrieved facts + behavioral specification." | ✅ Match | Same C1/C3 native-distinction presentation caveat as above. |
| Condition C4 (all facts) | "All facts, no spec — every extracted fact." | §3.5: "C4 All facts. All extracted facts, no spec." | ✅ Match | — |
| Condition C4a (facts+spec) | "Facts + specification — every extracted fact plus specification." | §3.5: "C4a Facts + spec. All facts + spec." | ✅ Match | — |
| Condition C8 (raw corpus) | "Raw corpus, no specification — entire training corpus loaded." | §3.5: "C8 Raw corpus, no spec. Full training text (~25K-420K words)." | ✅ Match | — |
| Condition C9 (corpus + spec) | "Corpus + specification — raw training corpus plus specification." | §3.5: "C9 Raw corpus + spec." | ✅ Match | — |
| 1-5 rubric definitions | §1.2 rubric table: 1=Refuses/wholly wrong; 2=Right topic, wrong prediction; 3=Right domain, no specifics; 4=Right direction with specifics; 5=Predicts specific outcome. | §3.7 rubric table: identical anchors; example column differs. | ✅ Match | Anchors identical. Example in §3.7 is Hamerton-London only; §1.2 has no per-row examples. |
| 7-judge panel | "Claude Haiku, Sonnet, and Opus; GPT-4o and GPT-5.4; Gemini Flash and Gemini Pro." | §3.7: "Haiku 4.5, Sonnet 4.6, Opus 4.6 (Anthropic), GPT-4o, GPT-5.4 (OpenAI), Gemini 2.5 Flash, Gemini 2.5 Pro (Google)." | ✅ Match | §3.7 adds version strings; §1.2 omits them. Consistent. |
| 14-subject list | §1.2 chronological enumeration: Augustine, Babur, Bernal Diaz, Cellini, Rousseau, Equiano, Seacole, Keckley, Yung Wing, Hamerton, Fukuzawa, Ebers, Sunity Devee, Zitkala-Sa. | §3.2 baseline-ordered table contains all 14 plus Franklin (known-figure control). | ✅ Match | Both lists contain the same 14 subjects. Franklin is separately labeled as control in §3.2; §1.2 does not mention Franklin in the 14. Consistent. |
| 50/50 train/held-out split | §1.2: "training half was used to generate the specification, to seed each memory system, and to provide the retrievable fact pool. The held-out half was used only to produce behavioral prediction questions. No held-out passage was ever shown to a response model." | §3.2 final paragraph: "source text is split 50/50 into training and held-out chapters. The Behavioral Specification is generated only from the training half. All prediction questions reference behaviors described in the held-out half. **The specification never sees the data it is tested against.**" | ✅ Match | §3.2 adds "chapter-level" split unit; §1.2 leaves unit unspecified. Consistent. |
| Letta two-path distinction | §1.2 "Additional testing for Letta" paragraph explicitly flags archival vs. stateful-self-editing paths. | §3.5 describes memory-system conditions uniformly and does **not** mention Letta's two paths. §3.6 and §3.7 do not either. | ⚠️ Gap | §3 reader alone would miss that Letta is tested on two architectural paths. §3.5 or a new §3.5.1 should cross-reference §4.3.1. See Flagged Issue 3. |
| Wrong-spec v1/v2 | §1.2 describes both variants in the condition table. §1.3 "Mechanism" paragraph uses v1 + v2 data. | §3.5 dedicates a "Wrong-spec control (v1 and v2)" block matching §1.2 description. | ✅ Match | — |

**A summary:** All substantive definitions match. The only real coherence gap is that §3 never mentions Letta's two-path distinction that §1.2 and §1.3 both rely on.

---

## B. Technical Identifier Verification

| Identifier | v8 §3 usage | Canonical source | Verdict |
|---|---|---|---|
| Embedding model | "MiniLM-L6-v2 (local)" (§3.3 pipeline table, line 256) | `memory_system/src/baselayer/config.py:98` → `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`. Hugging Face handle is `sentence-transformers/all-MiniLM-L6-v2`. | ❌ Incorrect identifier. Paper says `MiniLM-L6-v2`; canonical is `all-MiniLM-L6-v2`. Also appears correctly as `all-MiniLM-L6-v2` in §1.3 line 96 ("Base Layer … MiniLM-L6-v2 + ChromaDB") and KEY_FINDINGS (which also uses the shortened form). Recommend: replace with "all-MiniLM-L6-v2 (sentence-transformers)" throughout. |
| Vector store | "ChromaDB" (§3.3, §1.3, elsewhere) | Canonical name `ChromaDB` / `chromadb` Python package. Verified. | ✅ Correct. |
| Mem0 SDK | Not explicitly versioned in §3. | Paper relies on arXiv:2504.19413 + 2025 production algorithm. | ✅ No claim to verify in §3. §2.1 holds the primary-source attribution. |
| Letta SDK | Not versioned in §3. "Letta" and archival-API identifiers (`archival_memory_search`, `core_memory_append`, `core_memory_replace`) appear only in §2.1. | Verified against MemGPT paper (Packer et al., arXiv:2310.08560). | ✅ No §3 claim. |
| Supermemory SDK | Not versioned. | — | ✅ No §3 claim. |
| Zep / zep-cloud | Not versioned in §3. Graphiti Apache 2.0 claim made in §2.1. | Verified. | ✅ No §3 claim. |
| Wilcoxon signed-rank | §4.1 cites; §3 does not name the implementation library. | Standard (scipy.stats.wilcoxon implied). | ✅ Standard test, no specific citation required. |
| Krippendorff's alpha (ordinal) | §3.7: "Krippendorff's alpha (ordinal): 0.535 across all 7 judges; 0.659 across the 5 non-Gemini judges." | Standard ordinal-level α (Krippendorff, 2011). Implementation typically `krippendorff` Python package. | ✅ Correct label. Implementation not cited; optional. |
| Spearman rank correlation | §3.7: "pairwise Spearman rho: 0.89-0.98." | Standard (scipy.stats.spearmanr). | ✅ Correct. |
| Claude Haiku 4.5 | §3.6 and §3.7 | API identifier `claude-haiku-4-5` (variant). Name "Haiku 4.5" is the marketing form consistent with recent Anthropic releases. | ✅ Plausible and used consistently across project. |
| Claude Sonnet 4.6 | §3.6 and §3.7 | Marketing form of `claude-sonnet-4-6`. | ✅ Consistent. |
| Claude Opus 4.6 | §3.7 (judge) | Marketing form of `claude-opus-4-6`. | ✅ Consistent. |
| GPT-4o | §3.7 judge; §1.2 judge panel; §2.1 vendor benchmark strings | OpenAI model ID `gpt-4o`. | ✅ Correct. |
| **GPT-4.1** | §3.6 response model row ("OpenAI — GPT-4.1 — Multi-model validation") | Verified: run script `scripts/run_multimodel_responses.py` hard-codes `gpt-4.1`. Result files `results/run_gpt41_franklin_*/` and `results/run_gpt41_hamerton_*/` confirm GPT-4.1 ran on at least Franklin and Hamerton. GPT-4.1 does **not** appear in KEY_FINDINGS or DATA_REFERENCE, suggesting its responses were not judged or rolled up into the main gradient. | ⚠️ Needs disclosure. §3.6 lists GPT-4.1 as one of 6 response models but it does not appear in any reported aggregate. Either (a) it ran only on Hamerton/Franklin and the paper should say so, or (b) it should be removed from the "6 response models" count. See Flagged Issue 1. |
| GPT-5.4 | §3.6 response model; §3.7 judge; §3.4.1 battery generator | Used extensively. Parse-failure note (19%) in §3.7 matches DATA_REFERENCE §9. | ✅ Consistent. |
| Gemini 2.5 Flash | §3.6 response, §3.7 judge | ✅ Correct. Consistent with §1.2 ("Gemini Flash"). |
| Gemini 2.5 Pro | §3.6 response; §3.7 judge with limited coverage note | Coverage caveat in §3.7 matches DATA_REFERENCE §9. | ✅ Consistent. |
| LongMemEval, LOCOMO, LME-S | §3 does not itself cite benchmark arXiv IDs — they are cited in §2.1 and §2.3. | Already verified in `section_2_1_verification.md` and `section_2_3_verification.md`. | ✅ Out of §3 scope. |

---

## C. Flagged Issues (Must Fix Before Lock)

1. **`[Results to be filled in §4.8 after runs complete.]` placeholder in §3.4.1 (line 325).** §4.8 is fully populated. Replace placeholder with a one-line forward reference: *"Result: 5/6 direction matches; circularity defused. Full table in §4.8."* Current placeholder will read as an unfinished paper.

2. **Incorrect embedding-model identifier in §3.3 pipeline table (line 256).** `MiniLM-L6-v2` → `all-MiniLM-L6-v2 (sentence-transformers)`. The shortened form is sometimes used colloquially but the HF handle and `config.py` identifier are `all-MiniLM-L6-v2`. Fix throughout for consistency (§1.3 line 96 also uses the short form).

3. **§3 never introduces Letta's two architectural paths (archival vs. stateful-agent).** §1.2 has a paragraph on this; §1.3 and §4.3.1 build on it. §3.5 treats all memory-system conditions uniformly and a reader of §3 in isolation would not know the main conditions exercise Letta's archival path only, with the stateful path tested separately in §4.3.1. Add a one-sentence flag in §3.5 after the memory-system conditions table: *"Letta is architecturally distinct from the other three systems in that it maintains a self-edited memory block during multi-turn conversation; the conditions above exercise only its archival-retrieval path. The stateful-agent path is tested separately and described in §4.3.1."*

4. **§3.6 lists GPT-4.1 as a response model but it does not appear in any reported aggregate.** Result files confirm GPT-4.1 ran on Hamerton and Franklin only. Either (a) note its limited coverage explicitly (recommended — "GPT-4.1: Hamerton and Franklin only; not aggregated into cross-subject results"), or (b) drop it from §3.6 and describe the multi-model set as 5 response models. Current presentation as "6 response models" implies equal coverage and is not supported by the data.

5. **§3.4.1 Control 1 claim "Full GPT-5.4 batteries are released for independent replication"** — verify this is actually true in the published repo before launch. This is a concrete promise to reviewers; if the batteries are not in the public repo, either release them or soften the claim to "are released with the paper."

6. **§3.7 calibration table is 5-judge, not 7-judge.** The table omits Sonnet 4.6 and Opus 4.6 (missing columns) even though §3.7's prose says "Each judge is calibrated on four diagnostic tests before scoring study responses." Either add Sonnet/Opus columns or add a footnote: *"Sonnet and Opus calibration results in Appendix X; the three Anthropic judges exhibit consistent calibration profiles so we report the most-cited five here."* Leaving this silent is an easy reviewer snag.

7. **§3.5 duplicates the condition table from §1.2 with slightly different column choices.** §1.2's table has three columns (ID / Inputs / Purpose); §3.5 has four (ID / Condition / What model sees / Purpose). Content is consistent, but a reader comparing the two will notice minor phrasing differences ("Nothing" vs "No external information" etc). Consider replacing §3.5's reproduction with a one-line back-reference: *"Condition definitions are as in §1.2; repeated here with implementation detail."*

---

## D. Suggested Content Additions

1. **Fractional-score guidance in §3.7 (Aarik's ask).** Current §3.7 covers the 1.0→2.5 and 2.5→4.0 transitions. It does **not** cover the specific ranges Aarik asked about (2.9→3.2, 1.5→2.0). Recommend adding a paragraph after the rubric table:

   > *"Fractional scores within a single rubric anchor (e.g., 2.9 → 3.2, both between 'right domain, no specifics' and 'right direction with specifics') reflect within-category sharpening: more questions scored at the higher end of the same qualitative band. These shifts do not represent a category change in the kind of answer produced. Floor-adjacent shifts (e.g., 1.5 → 2.0) are categorically meaningful: 1.5 sits between refusal and topic-orientation; 2.0 means the model has moved off the refusal floor and is engaging with the subject domain on a majority of questions. One-point shifts (e.g., 2.0 → 3.0) cross rubric anchors and are the load-bearing effect size for this paper; anything below that should be read as a distributional shift within a category rather than a category change."*

2. **Methodology-gap disclosures reviewers will press on.** Three gaps a referee will catch on first read:

   - *Subject-selection pool.* §3.2 says subjects were selected across time periods, lengths, geographies — but does not say from how large a candidate pool, using what filtering criteria. Recommend one-sentence disclosure: "Candidates were drawn from Project Gutenberg + Internet Archive public-domain autobiographies meeting length > 20K words and first-person narrative structure; the 14 reported are an expert-selected sample rather than random draws from this pool."

   - *39-BP sampling from 80-question battery.* §3.4 introduces 80 questions across five tiers but does not say how the 39 BP questions are sampled or whether category-balance is enforced across the 10 behavioral categories flagged in §3.4.1. One-sentence disclosure needed.

   - *50/50 split methodology.* §3.2 says "split 50/50 into training and held-out chapters." Reviewers will want to know: chapter-boundary or word-count? Alternate chapters, or first-half/second-half? This is a five-word disclosure.

3. **Session 114 findings from `KEY_FINDINGS.md` (m15–m22) that should surface somewhere in §3 rather than only §4.** The paired C1-vs-C3 analysis (m15), Keckley Q21 spec-level refusal (m16), wrong-spec detection upper bound 60.6% (m20), Aarik baseline pilot C5=1.90 (m22), and Letta archival dedup (m18) are all methodologically consequential. Most live in §4 or §1 appropriately, but §3.4.1 would benefit from a pointer to the wrong-spec detection methodology (§4.5 / m20) rather than leaving the wrong-spec framing only in §3.5's condition row.

4. **Letta stateful-agent methodology section.** Given that §4.3.1 is one of the paper's load-bearing findings (M5, M6, M7), §3 needs either a §3.5.1 "Letta stateful-agent testbed" block describing the 30-turn ingestion methodology, or an explicit forward reference from §3.5 to §4.3.1. Currently §3 does not acknowledge this track at all.

---

## Cross-draft Factual Cross-check (bonus, out of strict §3 scope but relevant)

One discrepancy worth flagging outside §3: §1.3 line 111 names the one Tier 2 mismatch as "Zitkala-Sa × Gemini Pro," but §4.8 Table L821-828 shows the mismatch is "Zitkala-Sa × Sonnet" (Sonnet Δ = +1.40, Haiku Δ = −0.33, direction mismatch). KEY_FINDINGS M9 agrees with §1.3 (Gemini Pro Δ = −0.55). The numbers also disagree: §4.8 has Ebers × Gemini Pro Δ = +0.23 while KEY_FINDINGS reports +1.07. One of the tables is stale. Not a §3 issue, but will surface in any coherent reading.

---

## Summary Checklist for §3 Lock

- [ ] Fill §3.4.1 placeholder with forward-ref to §4.8 (Issue 1).
- [ ] Correct embedding model identifier to `all-MiniLM-L6-v2` (Issue 2).
- [ ] Add Letta two-path flag in §3.5 (Issue 3).
- [ ] Clarify GPT-4.1 coverage in §3.6 or remove from response-model list (Issue 4).
- [ ] Verify GPT-5.4 battery release is actual (Issue 5).
- [ ] Add or footnote Sonnet/Opus calibration columns (Issue 6).
- [ ] Consider collapsing §3.5 condition table to back-reference §1.2 (Issue 7).
- [ ] Add fractional-score guidance paragraph covering 2.9→3.2 and 1.5→2.0 ranges (Addition 1).
- [ ] Disclose subject-selection pool, 39-BP sampling, and 50/50 split unit (Addition 2).
- [ ] Add §3.5.1 or forward-ref for Letta stateful-agent testbed (Addition 4).
