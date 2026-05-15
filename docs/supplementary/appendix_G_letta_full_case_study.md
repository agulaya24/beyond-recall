# Appendix G — Letta Stateful-Agent: Exploratory Case Study (full)

*Mirrored from beyond_recall_v11.9.1 / earlier v10 drafts. Body summary lives in §4.5 of the paper; the headline result is also in Appendix G of the paper.*

---

> **Headline result on the small sample tested (5-judge primary):** Letta's self-edited memory block scores higher than Base Layer's unified-brief variant on all 3 subjects at matched response model. Hamerton **3.10 vs. 2.96** (Δ +0.14), Ebers **2.76 vs. 1.72** (Δ +1.05), Bābur **2.42 vs. 1.88** (Δ +0.54). A robustness rerun against Base Layer's full layered stack preserves direction (Δ +0.27 / +1.21 / +0.38). The matched-model gap is largest at the mid-corpus subject (Ebers) and smaller at both endpoints; with three data points the shape is consistent with a corpus-size band where the self-edited block is most effective, with degradation as the block grows, or with insufficient interpretive content when the corpus is small. Multi-subject replication is flagged as the highest-priority external falsification (§7.5).

Letta is the one commercial memory system in the study whose architecture supports an alternative to retrieval at query time. Alongside the archival retrieval path tested in §4.4, Letta agents maintain a persistent memory block that the agent itself rewrites during ingestion. This is the stateful-agent design from the original MemGPT paper. It is architecturally distinct from retrieval-based memory: the representation is authored by the agent over the course of reading the source corpus, rather than chunked and indexed for later retrieval. §4.5 examines what that produces on a small set of subjects, with the caveats above. Multi-subject replication across the full gradient, multiple response models, and a comparison against the Base Layer full layered stack (rather than the compressed variant used here) are flagged as follow-ups in §7.5.

---

**Test design.** A fresh Letta agent was initialized and fed the training half of each subject's corpus turn-by-turn. The agent was allowed to self-edit its memory block during ingestion, its native MemGPT behavior. After ingestion, the resulting memory block was extracted and served as context to Claude Haiku 4.5, the response model used throughout the main study. The behavioral-prediction battery was the main-study battery. Three subjects were tested, spanning a 9× corpus-size range:

| Subject | Source corpus | Corpus size (words) | Letta block size (chars) |
|---|---|---:|---:|
| Hamerton | Philip Gilbert Hamerton, *An Autobiography* (training half) | 25,231 | 22,472 |
| Ebers | Georg Ebers, *The Story of My Life* (training half) | 48,161 | 68,413 |
| Bābur | Bābur, *Bābur-nama* (training half) | 222,742 | 335,349 |

The direct comparison: Letta's stateful-path memory block fed to Haiku, vs. Base Layer's full-stack specification fed to the same Haiku, on the same battery and judge panel. Both are interpretive representations delivered as context; the test isolates the representation itself.

---

**Methodological note on the Base Layer condition served here.** The Base Layer side of this matched-rerun loaded the unified brief variant (a ~7K-character synthesized document served as a single artifact) rather than the full layered stack (anchors + core + predictions + brief) that §4.4's controlled and native C2a / C3 conditions use. The unified brief is more compressed on referential detail than the layered stack. A layered-stack rerun on these three subjects would likely narrow the Letta-over-BL gap; whether it narrows to parity or reverses is not measured. The table column header below reflects this: the Base Layer side is the unified brief variant.

**Result (5-judge primary: Haiku, Sonnet, Opus, GPT-4o, GPT-5.4).**

| Subject | Letta block → Haiku | BL unified brief → Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|
| Hamerton | 3.10 | 2.96 | **+0.14** |
| Ebers | 2.76 | 1.72 | **+1.05** |
| Bābur | 2.42 | 1.88 | **+0.54** |

On all three subjects tested, Letta's stateful-path block, served to the same response model as the Base Layer unified brief, produces a higher per-subject mean score than the unified brief. Both representations land well above the retrieval-only baseline at matched response model (§4.4 Letta archival Δ_spec for these subjects: Hamerton near parity with Base Layer retrieval, Ebers +0.31, Bābur near-null).

**Judge-panel robustness.** The 7-judge sensitivity aggregate (Hamerton +0.093, Ebers +0.746, Bābur +0.232; see `docs/research/letta_stateful_matched_rerun.md` Part 7 appendix) preserves direction on all three subjects. The 5-judge primary values are larger than the 7-judge values on Ebers and Bābur by +0.30 and +0.31 points respectively, because the two Gemini judges were inflating Base Layer scores relative to the calibrated core on those subjects. Excluding Gemini from the aggregate (the paper's 5-judge primary convention; §3.3.3 and §4.6.2) therefore widens the Letta-over-BL gap rather than narrowing it. Hamerton is the exception (5-judge Δ +0.14 vs. 7-judge +0.09), where Gemini inclusion slightly narrowed the gap rather than widening it. In all three cases, the Letta-block-outperforms-BL-Spec direction is stable across panels.

---

**Compression behavior: divergence at large corpora.**

Letta's memory block grew roughly linearly with source corpus size. At the largest subject (Bābur), Letta's API began rejecting ingestion requests at approximately 333,000 characters. After 22 consecutive failed ingestion attempts, the final block measured 335,349 characters. Letta's declared block-size metadata limit is 100,000 characters, unenforced in practice; the effective ceiling on the server side appeared to be a different API-level limit around 333K.

At the ceiling, the block contained **25.4% verbatim sentence duplication** on Bābur, compared to 0% duplication on Hamerton and 0% on Ebers. The self-editing agent rewrites content it has already written when pressed against the ingestion limit, rather than compressing or summarizing. The representation carries corpus-derived narrative at scale but does not preserve the compression property that makes large corpora tractable.

**Semantic-similarity duplication.** A sentence-embedding analysis (post-hoc, this paper; `scripts/analyze_letta_semantic_duplication.py`, MiniLM-L6-v2, sentence-pair cosine ≥ threshold) shows that the verbatim figure understates the duplication. The self-editing agent paraphrases prior sentences as well as repeating them. On Bābur, 73.8% of sentences have a near-duplicate at cosine ≥ 0.80, 56.1% at ≥ 0.85, 41.4% at ≥ 0.90, and 35.2% at the strict ≥ 0.95 threshold (paraphrase-level matches). Ebers shows minor near-paraphrasing (11.5% / 3.3% / 1.1% / 0.5% across the same thresholds). Hamerton shows none at any threshold above 0.80. The pattern matches the verbatim direction. Sample matches at ≥ 0.95 on Bābur include `"Emotional Resilience in Governance: Bābur's personal reflections..."` paired with `"Emotional Resilience in Leadership: Bābur's reflections on challenges..."` (cosine 0.957): same template, slight rewording. The agent's abstention behavior tracks this duplication gradient: on Bābur (most degraded), Letta abstains on 17.9% of held-out questions vs 0% for the Spec; on Ebers, 10.3% vs 5.1%; on Hamerton (least degraded), the rate inverts to 7.7% vs 10.3% — consistent with adaptive recognition of block degradation rather than ceiling-induced confusion. The duplication within the block does *not* propagate as surface-syntactic leakage into responses: a per-question 5-gram overlap test against held-out passages returns 0.0% on every single question for both Letta and Spec (§4.5 mechanism paragraph). The duplication is a within-block artifact of self-editing at the ceiling; the response-level mechanism for Letta's lift is named-entity grounding plus content-confidence. Full per-threshold duplication data at `docs/research/letta_semantic_duplication_20260501.json`; per-subject abstention decomposition at `docs/reviews/letta_vs_spec_abstention_20260507.md`; per-question leakage analysis at `docs/research/letta_vs_spec_leakage_analysis_20260507.md`.

Base Layer's compose step keeps the full-stack specification at 34,000-40,000 characters across the same corpus-size range. At Hamerton, the two representations are the same order of magnitude in size; at Bābur, the Base Layer specification is roughly one-tenth the size of the Letta block. The two systems are prediction-band compatible at small corpora; they diverge on compression at large ones.

**What the ceiling means for deployment.** Served on every query, a 335,000-character Letta block costs roughly 84,000 tokens of context. At current frontier pricing this is materially more per-query cost than the Base Layer specification's ~7,000 tokens (~37,000 characters), and it exceeds the context window on the smaller-context models still common in production (128K token windows struggle when the block alone is two-thirds of the budget, before any conversational state). The duplication observed at the ceiling combines 25.4% verbatim sentence repetition with substantial semantic near-paraphrasing (35.2% of sentences at cosine ≥ 0.95, 56.1% at ≥ 0.85). The block would be functionally much smaller with a deduplication pass. Conservatively (one-of-each-pair removal at ≥ 0.85), roughly 30% of the block is removable; aggressive cluster-collapse deduplication at the same threshold could reach a 50% reduction, taking the block from ~335K to ~170K characters at preserved content. A semantic-similarity deduplication pass on the self-edited block is a tractable post-processing step that this study does not run but recommends. For production deployment, the ceiling, the verbatim duplication, and the additional semantic duplication together argue for representation compactness as a first-class design constraint, not a nice-to-have.

---

**What this exploration does and does not show.**

On N=3 subjects, with one response model and one Letta version, Letta's stateful-path block and Base Layer's unified-brief variant both land above retrieval-only context at matched response model, in a similar prediction band. This is consistent with (though does not establish) the idea that the behavioral-specification target is reachable by representation-production mechanisms outside offline-authored retrieval composition. Establishing that would require multi-subject replication across the full gradient, multiple response models, and a comparison against Base Layer's full layered stack rather than the unified-brief variant tested here. All three are flagged in §7.5.

What the exploration does show is the shape of the engineering tradeoff between the two paths. They differ in how the representation is produced (offline authoring vs. online self-editing), in what it carries (interpretive scaffolding vs. corpus-derived narrative at higher referential density; see content comparison below), and in how it scales (bounded compression vs. an ingestion ceiling observed at ~333K characters on the largest corpus we tested). These are tradeoffs to characterize, not a resolved comparison.

---

**Content comparison: what each representation retains.**

To test whether Letta's higher matched-model score comes from preserving original corpus text the response model could cite, we ran a post-hoc content analysis on the three subjects. The strong form of that hypothesis is refuted. Neither representation is a quote library. Checking what fraction of consecutive five-word sequences in each representation also appears verbatim in the training corpus (a standard overlap check), both representations score under 1%: the Letta block ranges 0.0-1.0% depending on subject, the Base Layer specification scores 0.0% on all three. The same check for consecutive ten-word sequences gives under 0.1% for both. Both representations are LLM-generated rewrites of the corpus in the writing model's own voice, not verbatim extracts.

A refined version of the hypothesis does hold, with the magnitude smaller than first reported. The two representations differ in **referential density**: Letta's rolling summary retains more unique proper nouns, dated events, and named secondary characters than Base Layer's §4.5 specification, and the gap scales with corpus size. On Bābur (the largest corpus), Letta's block carries 416 unique capitalized named-entity tokens vs. Base Layer's 65, a ratio of about **6×**. On Ebers (mid-size), the counts are 53 vs. 34, a ratio of about **1.5×**, closer to parity. Base Layer, by construction, compresses episodes into cross-cutting behavioral patterns with fewer surface referents; the pipeline explicitly anonymizes the subject during authoring and compresses corpus-level specifics into dimensional axioms. Letta's stateful-agent path preserves more of the referential surface while also encoding behavioral patterns. The referential-density gap is real but corpus-dependent rather than uniformly an order of magnitude.

Both representations produce responses that outperform retrieval-only context at matched response model, but they diverge on referential detail. On battery items that reward specific-event recall, Letta has more named entities to cite. On items that reward principled interpretation across episodes, Base Layer's dimensional axioms compete directly. The §4.5 matched-model gap may be attributable in part to the referential-density difference rather than to the self-editing process itself. A Base Layer variant that retains named entities inside the same dimensional scaffold would separate the two effects. Flagged in §7.

**Replication as the load-bearing next step.** The three-subject comparison reported here is not a claim that alternative representation-production architectures reach the interpretive-representation target. It is a case study with direction but not power. Multi-subject replication across the full 14-subject gradient (layered-stack Base Layer vs. Letta stateful, both anonymized to match, multiple response models) is the highest-priority external falsification we can run on §4.5, and is flagged as such in §7.5. If that replication closes the gap at parity, §4.5's direction holds on a wider sample. If it reverses, §4.5's direction was corpus-specific.

Full content analysis at `docs/research/` (see `_content_analysis_results.json` and the N=3 per-subject breakdown). The methodological note on the Base Layer condition is now hoisted above the result Table at the top of this section.

---

**Caveats.**

- N = 3 subjects on this path. Extending across the full 14-subject gradient would let the comparison speak to the population-of-relevance level, not only a selected set of corpus sizes. Flagged in §7.5.
- One response model (Haiku) on both conditions. The comparison is tested at matched response model; whether it holds at other response models is an open question.
- Letta's 333K-character ingestion ceiling is a hard architectural constraint in the current release. For small corpora the two representations are interchangeable in prediction behavior; for large corpora the ceiling is material.
- Base Layer condition used the unified `spec.md` variant for the main §4.5 table. A robustness rerun with the full layered stack (anchors + core + predictions + brief, name-restored to match the §4.5 naming convention) preserves direction on all three subjects (Δ_Letta−BL = +0.27 / +1.21 / +0.38 on Hamerton / Ebers / Bābur; full report at `docs/research/_letta_rerun/fullstack_named/RESULTS.md`). The gap widens at the two smaller corpora and narrows at Bābur, consistent with a Pattern 2 (over-theorization) effect on small corpora rather than a content-volume effect at large corpora. Direction is invariant across both Base Layer Spec forms.
- **Naming asymmetry.** Letta's stateful-agent path ingested the named source corpus and wrote a memory block that references the subject by name throughout. Base Layer's authoring pipeline strips the subject's name during specification authoring (§3.7 anonymization step); the §4.5 comparison restores the name at the surface level only (string substitution on the composed artifact). The two sides of the comparison therefore differ in whether the subject's name is load-bearing during representation production vs. only at serving time. Flagged as a methodological gap in §7.5.

---

**Raw data and scripts.** Letta stateful matched-rerun data at `docs/research/_letta_rerun/{subject}_judgments_{judge}.json`. Generation and scoring scripts live in the same directory as a numbered chain (`20_run_c2a_named.py`, `40_judge_responses.py`, `60_rerun_gpt54_letta.py`, `70_compute_5judge_primary.py`); see the `README.md` inside `docs/research/_letta_rerun/`. Full characterization of block content, duplication behavior, and API responses in `docs/research/letta_stateful_deep_read.md` and `docs/research/letta_stateful_matched_rerun.md`.

---


