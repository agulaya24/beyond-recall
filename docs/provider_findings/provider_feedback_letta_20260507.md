# Letta: Beyond Recall paper findings

This document summarizes everything Beyond Recall (arXiv: pending) observes about Letta. It is a companion to the headline paper and is shared with the Letta team pre-publish. The paper compares four commercial memory systems plus a substrate retrieval layer across 14 subjects, 546 questions, 5-judge primary panel.

---

## 1. Headline summary

Letta has the strongest controlled-aggregate Δ_spec of the four commercial systems we tested on the archival path: +0.20 across 14 main-study subjects, with 12 of 14 improving when a Behavioral Specification is layered on identical retrieval input (§4.4.1, line 1175). Under native ingestion the aggregate softens to −0.02 (5 of 14 improve). The driver we observe is not architectural: Letta's controlled retrieval surfaces only 3 to 5 unique facts inside each top-10 result (dedup ratio 0.34 to 0.47; §4.4.2 line 1298), and on the largest-corpus subject (Bābur) the self-edited stateful block hits an effective ingestion ceiling near 333,000 characters with 35.2% near-paraphrase duplication at sentence cosine ≥ 0.95. Both point to the same engineering signal: a semantic-similarity dedup pass during ingestion would relax the ceiling and likely raise the native-path Δ. On the stateful path (§4.5 / Appendix G; N=3 post-hoc), Letta's self-edited block scores higher than Base Layer's unified-brief variant on all three subjects at matched response model: a small-sample exploratory result, not a replication. We are sharing this document so your team sees the full read before public posting.

---

## 2. Aggregate Δ_spec results: archival and stateful paths

**Archival path (used in the main study).** Five-judge primary panel, 14 subjects, paired C1 (retrieval only) vs C3 (retrieval + Behavioral Specification). Source: §4.4.1, line 1175; emit data at `docs/research/v11_emit/4_4_1_memory_systems.md`.

| Configuration | Δ_spec | Subjects improved | Wilcoxon paired *p* (n=14) |
|---|---:|---:|---:|
| Controlled (identical fact pool input) | +0.20 | 12 / 14 | 0.0017 |
| Native (Letta ingests its own way) | −0.02 | 5 / 14 | 0.4629 |

The controlled aggregate is the strongest of the four commercial systems on this configuration; the native softening is unique to Letta (Mem0, Zep both rise under native ingestion; Supermemory stays roughly flat). The mechanism we surface in §4.4.2 is fact dedup ratio (see Section 5).

**Stateful path (post-hoc exploratory; §4.5, line 1368; full case study in Appendix G).** N=3 subjects (Hamerton, Ebers, Bābur), one Letta version, one response model (Claude Haiku 4.5), 40-question battery per subject. Five-judge primary panel.

| Subject | Corpus (words) | Letta block to Haiku | BL unified brief to Haiku | Δ (Letta − BL) |
|---|---:|---:|---:|---:|
| Hamerton | 25,231 | 3.10 | 2.96 | +0.14 |
| Ebers | 48,161 | 2.76 | 1.72 | +1.05 |
| Bābur | 222,742 | 2.42 | 1.88 | +0.54 |

Robustness rerun against Base Layer's full layered stack (anchors + core + predictions + brief, name-restored): Δ +0.27 / +1.21 / +0.38 on Hamerton / Ebers / Bābur. Direction is invariant across both Base Layer variants. Provenance and rerun script chain at `docs/research/_letta_rerun/` (see `RESULTS.md`, `70_compute_5judge_primary.py`).

---

## 3. Per-question improvement rates (archival path)

From the §4.4.2 footnote `[^memsys-pattern-appendix]` (line 1232) and `docs/research/per_system_anchor_crossing_20260427.json`, restricted to (subject, question) pairs with 5-judge primary coverage on both C1 and C3.

**Letta archival, Hamerton (controlled):** aggregate Δ_spec +0.42; 19 questions show |Δ| ≥ 1.0 increases vs. 7 large decreases; 26 of 39 paired questions cross by ≥ 1.0 anchor (helps outnumber hurts 2.7×). This is the cell that surfaces in Appendix B.11 (line 2197).

**Letta archival, full pool (controlled):** 153 of 545 paired questions cross an integer anchor upward (28.1%); 93 cross downward (17.1%); 299 produce no integer-band crossing. Subjects with at least one upward crossing: 14 of 14.

**Letta archival, full pool (native):** 112 of 546 questions cross upward (20.5%); 101 cross downward (18.5%); 333 produce no crossing. The 70 / 70 split on the low-baseline 9-subject scope is the cleanest read on the native softening.

**Stateful path (§4.5).** Per-question Hamerton: paired comparison is matched (39 of 39 question texts identical). The signature is asymmetric: stateful block scores 4–5 on questions where the BL unified brief refuses ("I don't have reliable information about Hamerton's swimming history..."); BL unified brief scores 5 vs stateful 2 on interpretation-heavy composition questions (Q51 guardian-distance dilemma; Q27 self-publishing). Detail at `docs/research/letta_stateful_deep_read.md` §2.1.

---

## 4. Multi-anchor crossings (archival path)

A multi-anchor crossing is a question whose 5-judge primary mean shifts across two or more integer rubric bands when the condition changes. Detail at `docs/research/per_system_anchor_crossing_20260427.md` lines 95–159.

**Letta controlled (low-baseline 9-subject scope):** 26.9% upward / 19.4% downward / 53.7% no crossing. Boundary breakdown: 1→2 (51), 1→3 (16), 2→3 (17), 2→4 (4), 3→4 (6).

**Letta native (low-baseline 9-subject scope):** 19.9% upward / 19.9% downward / 60.1% no crossing. Boundary breakdown: 1→2 (39), 1→3 (1), 1→4 (1), 2→3 (19), 2→4 (2), 3→4 (8).

**Multi-anchor jump count (full 14-subject pool, controlled):** jump-size distribution 1 (120), 2 (28), 3 (4), 4 (1). Total multi-anchor jumps: 33. **Native:** 1 (107), 2 (4), 3 (1). Total multi-anchor jumps: 5. The native config produces an order of magnitude fewer multi-anchor jumps than the controlled config on Letta. The same direction holds on Mem0 and Zep (multi-anchor jump count rises under native), making Letta the only commercial system where multi-anchor jumps fall sharply under native ingestion.

---

## 5. Pattern frequency (§4.4.2 routing)

From §4.4.2, line 1298, and `docs/research/mem0_letta_zep_c1_vs_c3_analysis.md`. Three patterns describe how the specification interacts with retrieval at the per-question level. The Letta-archival reading:

- **Pattern 1 (interpretive supply, lifts the score).** Letta's controlled retrieval emits 10 entries per question with dedup ratio 0.34 to 0.47, meaning the model sees 3 to 5 unique facts in a top-10 list with the most-repeated fact appearing 2.9 to 4.5 times. When those few unique facts align with the specification's interpretive scaffolding, the specification produces large-magnitude lift (Hamerton Q33 controlled: +2.67; Sunity Devee Q10 controlled: +2.33; among the largest single-question swings observed across all 12 system-subject pairs studied, behind only Zep's Seacole Q2 +4.00).

- **Pattern 2 (over-theorization, lowers the score).** When retrieval already supplies the plain answer (less common on Letta archival because of dedup), the specification can pull the response toward interpretive depth the question does not call for. Reproduces on Letta Ebers Q17 (single-line affirmation turned into multi-paragraph evidentiary meditation; analysis at `mem0_letta_zep_c1_vs_c3_analysis.md` §5.5).

- **Pattern 3 (specification-induced refusal, lowers the rubric score).** On Keckley Q21 (cross-system refusal case study, §4.4.3, line 1313), Letta archival's retrieval-only baseline was already at or below 1.4, so the specification's refusal axioms add no measurable rubric penalty (Δ +0.4, within noise). On other systems where retrieval-only was strong (Supermemory −2.0, Base Layer substrate −2.3), the same specification refusal axioms produce large rubric drops. Letta's low retrieval-only floor protects it from Pattern 3 cost.

---

## 6. The Letta semantic-duplication finding (§4.5 + Appendix G)

This is the constructive engineering signal we want to flag most directly. Source: `docs/research/letta_semantic_duplication_20260501.json`; analysis script at `scripts/analyze_letta_semantic_duplication.py`; paper §4.5 line 1380, Appendix G line 3245.

**Method.** Sentence-pair cosine on MiniLM-L6-v2 embeddings (sentence-transformers/all-MiniLM-L6-v2), within a single Letta human memory block. A sentence is "near-duplicate at threshold *t*" if at least one other sentence in the same block has cosine ≥ *t*.

**Per-subject results.**

| Subject | Block size (chars) | Sentences | ≥ 0.80 | ≥ 0.85 | ≥ 0.90 | ≥ 0.95 |
|---|---:|---:|---:|---:|---:|---:|
| Hamerton | 22,472 | 129 | 3.1% | 0.0% | 0.0% | 0.0% |
| Ebers | 68,413 | 364 | 11.5% | 3.3% | 1.1% | 0.5% |
| Bābur | 335,349 | 1,302 | 73.8% | 56.1% | 41.4% | **35.2%** |

The Bābur block reaches the ceiling. Sample matches at ≥ 0.95: `"Emotional Resilience in Governance: Bābur's personal reflections..."` paired with `"Emotional Resilience in Leadership: Bābur's reflections on challenges..."` (cosine 0.957). Same template, slight rewording, both retained.

**Verbatim duplication (separate analysis, paper §4.5 line 1378).** 25.4% verbatim sentence duplication on Bābur, 0% on Hamerton, 0% on Ebers. The verbatim figure understates the duplication: sentence-embedding analysis raises it to 35.2% at the strict ≥ 0.95 threshold.

**Block-size ceiling.** From `docs/research/letta_stateful_matched_rerun.md` §1: last successful ingestion at turn 220 (block size 332,585 chars), first 400 Bad Request at turn 221, 22 consecutive failures through turn 242. Final block fetched post-loop: 335,349 chars. Block metadata advertises `limit=100,000`, but the cap is documentation rather than enforcement; the binding constraint appears to be a server-side request-body cap near 333K chars.

**Implications for the archival path.** Letta archival's controlled retrieval emits high-redundancy top-10 lists (dedup ratio 0.34 to 0.47, only 3 to 5 unique facts; §4.4.2 line 1298) and the native-config aggregate Δ softens to −0.02 (Section 2). The dedup ratio at the archival layer and the near-paraphrase rate at the stateful layer are the same shape of finding at two different stages: ingestion produces structurally redundant content that compresses effective representational depth on both paths.

**Reduction available.** Conservative one-of-each-pair removal at cosine ≥ 0.85 on Bābur removes ~30% of the block. Cluster-collapse at the same threshold could reach ~50% reduction, taking the block from ~335K to ~170K characters at preserved content. At current frontier pricing, this is ~84,000 tokens of context per query on the unprocessed Bābur block versus ~42,000 tokens after dedup. Neither figure includes downstream retrieval cost.

---

## 7. Per-subject view (archival path)

From `docs/research/per_system_anchor_crossing_20260427.json`. Per-subject upward / downward integer-band crossings on Letta archival, 5-judge primary, controlled and native configurations. The 9 low-baseline subjects (used in main-study secondary analyses) are marked.

| Subject | Low-baseline | Controlled up / down / none | Native up / down / none |
|---|:-:|---:|---:|
| Hamerton | yes | 15 / 6 / 17 | 13 / 7 / 19 |
| Augustine | no | 14 / 6 / 19 | 7 / 10 / 22 |
| Bābur | yes | 9 / 5 / 25 | 6 / 7 / 26 |
| Bernal Díaz | yes | 11 / 14 / 14 | 10 / 8 / 21 |
| Cellini | no | 16 / 2 / 21 | 10 / 5 / 24 |
| Ebers | yes | 8 / 5 / 26 | 4 / 6 / 29 |
| Equiano | no | 11 / 9 / 19 | 9 / 8 / 22 |
| Fukuzawa | yes | 9 / 6 / 24 | 6 / 12 / 21 |
| Keckley | yes | 5 / 11 / 23 | 7 / 6 / 26 |
| Rousseau | no | 14 / 3 / 22 | 12 / 3 / 24 |
| Seacole | yes | 14 / 2 / 23 | 8 / 8 / 23 |
| Sunity Devee | yes | 8 / 10 / 21 | 7 / 12 / 20 |
| Yung Wing | yes | 15 / 9 / 15 | 9 / 4 / 26 |
| Zitkala-Ša | no | 4 / 5 / 30 | 4 / 5 / 30 |

**Letta's strongest controlled subjects** (by upward-crossing count): Cellini (16/2), Hamerton (15/6), Yung Wing (15/9), Augustine (14/6), Rousseau (14/3), Seacole (14/2). **Softest:** Zitkala-Ša (4/5), Keckley (5/11), Bernal Díaz (11/14). Zitkala-Ša is one of two subjects (with Equiano) where the specification did not measurably improve prediction in Tier 2 replication; Keckley's down-tilt is explained by the §4.4.3 Keckley Q21 specification-induced refusal case study.

**Native softening is sharpest** on Sunity Devee (7/12), Fukuzawa (6/12), Augustine (7/10). Yung Wing is unusual: 15/9 controlled, 9/4 native (positive net under native, the opposite of the system-wide direction).

---

## 8. Abstention / refusal behavior

From `docs/research/abstention_extensions_draft_20260429.md`. Memory-system retrieval inflates refusal rubric scores by +0.21 to +0.23 anchor points relative to pure C5 refusals (no facts, no retrieval), pooled across all four commercial systems plus Base Layer substrate. Whether the response visibly recites a retrieved n-gram is incidental (Δ recite vs. no-recite = +0.027, 95% CI crosses zero, *p* = 0.67).

Letta controlled: 60.9% of refusals recite a retrieved n-gram. Letta full-pipeline (native): 0.0% (n=8 refusals; sample size unstable). Provider comparison: Mem0 controlled 62.5%, Supermemory controlled 60.0%, Letta controlled 60.9%, Zep controlled 26.8%. Letta sits in the Mem0 / Supermemory band on controlled-config recitation. The +0.21 to +0.23 inflation applies uniformly across systems; the dependent variable is condition, not recitation behavior.

---

## 9. Retrieval divergence (per-pair vs other systems)

From §4.4.1, line 1186; data at `docs/research/retrieval_overlap_analysis_20260501.json`; reproducibility at `scripts/analyze_retrieval_overlap.py`. Pairwise Jaccard similarity is the metric: fraction of facts shared between two systems' top-10 retrievals on the same question, computed on 14 subjects × 39 behavioral-prediction questions × 10 system pairs = 5,460 (system pair, question) instances under the controlled configuration where every system reads the same all-facts pool.

**Letta's pairwise Jaccard rows (controlled, n=546 questions per pair):**

| Pair | Mean Jaccard |
|---|---:|
| Mem0 ↔ Letta | 0.126 |
| Letta ↔ Supermemory | 0.099 |
| Base Layer ↔ Letta | 0.092 |
| Letta ↔ Zep | 0.026 |
| **Letta-pair mean** | **0.086** |

Study-wide mean across all 10 pairs: 0.083 (mean ~8% overlap). Letta sits roughly at the study mean on pairs against Mem0 and Supermemory; the Letta–Zep pair is among the lowest pairs in the study (Zep's graph-traversal scoring overlaps weakly with embedding-similarity rankings).

**Letta retrieval depth note (§4.4.1 line 1208).** Letta's controlled retrieval emits 10 entries per question but only 3.5 unique facts on average; the same fact recurs under graph traversal. Jaccard is computed on unique sets, so duplication does not directly inflate overlap, but it does compress effective retrieval depth.

**Native pipeline.** Native retrievals return heterogeneous objects (Mem0 third-person summaries, Letta raw multi-sentence passages, Supermemory atomic facts, Zep graph rows). Two systems share zero exactly-matching facts on the same question; pairwise overlap drops to 0.000 across all four native pairs. A semantic-similarity check at near-paraphrase threshold raises this only to 0.004; loose topical threshold raises it to 0.016 (§4.6.5 sensitivity grid). The divergence is structural, not a surface-form artifact.

We do not interpret retrieval divergence as evidence any one system is wrong. We name it as a research observation: providers do not converge on relevance given identical input. The follow-up question (at what K does convergence happen, if any) is flagged in §7.

---

## 10. The stateful-path exploration (§4.5)

The §4.5 finding: at matched response model (Haiku 4.5) and 5-judge primary panel, Letta's self-edited memory block scores higher than Base Layer's unified-brief variant on all 3 subjects tested. Direction is preserved on the robustness rerun against Base Layer's full layered stack. The case study is exploratory rather than primary because (a) N=3 subjects, (b) one Letta version, (c) one response model, and (d) the original §4.5 comparison used Base Layer's unified-brief variant, not the full layered stack used in §4.4 main-study conditions.

**What the stateful path's representation looks like (from `letta_stateful_deep_read.md`).** Hamerton (22K chars) and Ebers (68K chars) are rolling narrative paragraphs, one per ingestion chunk, opening with phrases like *"The person reflects on..."* or *"The individual exhibits..."*. Bābur (335K chars) is structurally different: numbered axiom lists with bolded labels (1–10) where the numbering restarts roughly 130 times across appended turns rather than consolidating. The architectural ceiling and the dedup pattern (§6 above) coincide on Bābur.

**Why the §4.5 gap on Ebers reads as Letta-favorable in the paper.** The Base Layer pipeline anonymizes the subject during specification authoring (§3.7); the Haiku response model has near-zero pretraining anchoring on Ebers (C5 baseline 1.04, near rubric floor); the specification's epistemic-honesty axioms compose with anonymization to produce refusal-style responses that score 1 across all 5 judges on multiple questions. Letta's stateful block names the subject directly and carries corpus-derived narrative content, so Haiku has an authoritative source to reason from. The §4.5 gap is partly an interpretive-content axis and partly an anonymization-and-refusal axis.

**What Beyond Recall does not claim from §4.5.** The paper does not claim Letta's stateful path reaches the same target as the Behavioral Specification. It claims direction and shape on a small sample. The load-bearing next step is multi-subject replication across the full 14-subject gradient with both representations name-matched and the full Base Layer layered stack on the comparison side. Flagged as the highest-priority external falsification on §4.5 in §7.5.

**Naming asymmetry caveat (Appendix G line 3281).** Letta's stateful path ingested the named source corpus and wrote a memory block referencing the subject by name throughout. Base Layer's authoring pipeline strips the subject's name during specification authoring; the §4.5 comparison restores the name at the surface level only (string substitution on the composed artifact). The two sides differ in whether the subject's name was load-bearing during representation production vs. only at serving time.

---

## Integration experience

The Beyond Recall study integrated with Letta via a standalone runner script with fresh process per session, bypassing the official Python SDK (letta-client 1.10.2) after `agents.list()` exhibited urllib3/chardet hangs under sustained load. Findings below reflect study-time integration experience.

**API/SDK positives observed during integration:**
- Clean agent lifecycle: create, ingest, search, delete; each agent is an isolated namespace.
- Archival memory search returns well-structured results with timestamps and IDs.
- Pro tier 20-agent allowance was sufficient for 14 subjects with margin.
- Passages-based ingestion suited document text well.

**Issues encountered and workarounds:**
- **SDK init hang.** `from letta_client import Letta` followed by `client.agents.list()` hung after sustained use. Same urllib3 / chardet root cause as Mem0. Workaround: standalone runner script with fresh process per session.
- **Endpoint confusion.** Three possible search endpoints surfaced in documentation: `/passages/search` (404), `/archival-memory/search` (works), and agent message-based retrieval. Documentation did not clearly distinguish them; required testing all three to find the working one.
- **`/passages` endpoint does not exist** despite appearing in some documentation. Working endpoint is `/archival-memory` for both ingest and search.
- **Field name discrepancy.** Ingestion uses `{"text": "..."}` not `{"content": "..."}`; the wrong field name returns 422.
- **Free-tier 3-agent limit.** Could not create more than 3 agents on free tier. Pro tier resolved this with a 20-agent allowance.

**Notes for the Letta team** (verbatim from `memory_system/data/experiments/memory_systems/PROVIDER_EXPERIENCE_LEDGER.md`):

> The agent paradigm is powerful but the API surface area is confusing. Multiple endpoint versions, deprecated routes that still appear in docs, and inconsistent field names between endpoints. A clear "here's the one endpoint for X" guide would save every integrator significant debugging time.

---

## 11. What we think this means for Letta's product roadmap

Constructive framing. We do not write to a product roadmap; these are research hooks Letta's team is best-positioned to operationalize.

- **Dedup-before-write on the stateful path.** The highest-leverage signal we have. A semantic-similarity dedup pass during ingestion (one MiniLM forward pass per turn, cosine threshold ≥ 0.85 against existing block) would relax the 333K-char ceiling pressure on Bābur. One-of-each-pair removal at ≥ 0.85 yields ~30% reduction; cluster-collapse at the same threshold yields ~50%. The append-with-paraphrase fallback at the ceiling (the ~130-restart numbered-axiom pattern on Bābur) suggests the self-editing heuristic does not currently reach for consolidation under pressure.

- **Dedup-before-write on the archival path.** Same direction. The 0.34–0.47 dedup ratio (3–5 unique facts in a top-10) and the controlled-vs-native split (+0.20 → −0.02) track each other: under controlled input the specification has room to add interpretive scaffolding on top of the 3–5 unique facts; under native ingestion the architecture surfaces less unique content and the specification's lift compresses. Compressing redundant facts before they enter the index would likely raise the native-config Δ_spec.

- **Block-size ceiling.** Metadata-advertised `limit=100,000` is not the binding constraint; the server-side request-body cap near 333K chars is. Hit only on Bābur (222K source words). For shorter corpora the ceiling is irrelevant. For long-corpus deployment, per-query token cost and 128K-window-model compatibility both pressure toward compactness.

- **Same dedup move applies on both paths.** The ≥ 0.85 cosine signal is the same shape on archival (3–5 unique facts in a top-10) and stateful (35.2% near-paraphrase at ≥ 0.95). One pass at one pipeline stage could in principle remove both forms of redundancy.

We are happy to share the data (`docs/research/letta_semantic_duplication_20260501.json`) and the script (`scripts/analyze_letta_semantic_duplication.py`).

---

## 12. Limitations and what this study does NOT claim about Letta

- The paper does not benchmark Letta against your published recall benchmarks (LOCOMO 74.0% on GPT-4o-mini, §2.2 Table 2.1 line 184). Behavioral prediction is a different test than recall.
- §4.5 stateful-path work is exploratory: N=3 subjects, one Letta version, one response model. Multi-subject replication across the 14-subject gradient is flagged in §7.5.
- The §4.5 main-table comparison used Base Layer's unified-brief variant; the full-layered-stack robustness rerun preserves direction. Both reported in Appendix G.
- N=14 subjects are historical figures with autobiography corpora, all dead. The population the paper claims (anyone who uses AI) is not directly tested.
- Letta was used through public APIs at standard rates: no fine-tuning, no early-access configurations.
- The naming asymmetry between Base Layer and Letta on the §4.5 comparison (Section 10) is a methodological gap, not a controlled property.
- Pipeline variance on the Base Layer side: 3-subject probe with 3 reruns each yielded pooled SD = 0.10 = 17% of cross-subject SD (§6.3).

---

## 13. Open questions for the Letta team

Research questions you are best-positioned to answer.

1. Has your team internally explored a semantic-similarity dedup pass during the self-edit cycle? At what stage (per-turn, periodic, ceiling-triggered) and with what threshold?
2. Has the ~333K-char effective ingestion ceiling been hit on other long-corpus subjects internally? Is the binding constraint the request-body cap we observed, or a different limit on different deployments?
3. The archival-path dedup ratio (0.34–0.47, 3–5 unique facts in a top-10) is an emergent property of how Letta's retrieval scoring composes with content addition. Is the duplicate-surfacing intentional (visual prominence as a signal of relevance) or an artifact?
4. The append-with-paraphrase pattern at the Bābur ceiling (numbered axiom lists restarting ~130 times rather than consolidating) suggests the self-editing heuristic does not currently reach for cross-block consolidation under context pressure. Is this a known behavior?
5. Would your team be open to a multi-subject collaborative falsification of §4.5 across the 14-subject gradient? We would supply corpora and batteries; you would supply configuration choices and version. We would publish the joint result regardless of direction.
