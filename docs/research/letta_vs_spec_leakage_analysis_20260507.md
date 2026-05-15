# Per-question texture-leakage analysis: Letta block vs Base Layer Spec

_Beyond Recall §4.5 / Appendix G secondary analysis._
_Generated 2026-05-07 by `scripts/letta_vs_spec_leakage_analysis_20260507.py`._

## Executive summary

The §4.5 paragraph at line 1502 of `beyond_recall_v11_8_draft.md` raises the question of whether Letta's score advantage over the Base Layer Spec on the three-subject case study reflects **interpretive accuracy** or **surface-syntactic alignment with held-out passages Letta ingested**. Two complementary measures applied per question across n=119 paired questions return the same answer: surface-syntactic alignment is not the mechanism.

**The decisive finding is the 5-gram (verbatim-phrase) overlap.** On every single one of 119 questions, on every subject, for both Letta and Spec, the 5-gram overlap with the held-out passage is exactly **0.0%**. Neither system echoes any 5-token sequence verbatim from the held-out passage. The Letta block, despite retaining source-text texture in storage (paper-stated 25.4% verbatim sentence duplication on Babur within the block itself), does not propagate that texture into responses about the held-out questions. The "surface-syntactic alignment" hypothesis as literally stated is fully falsified at the verbatim-phrase grain.

**Three-gram overlap shows the actual mechanism: named-entity grounding.** Mean 3-gram overlap is tiny on both sides (Letta 0.051–0.077%, Spec 0.021–0.063%) and dominated by proper-name sequences ("Frederick William IV", "at my own expense", "the rebel Afghans"). Letta is ≈1.2–2× Spec at this granularity but the absolute values are well under 0.1%. The 3-gram pooled Pearson r against `score_delta` is **−0.046** (essentially zero) and within-subject r's swing through (−0.29, +0.20, +0.04) — no consistent direction.

**MiniLM mean-pooled cosine (semantic / topic alignment) shows the same null at scale.** Mean `cos_letta_heldout − cos_spec_heldout` = +0.011 across 119 questions; pooled Pearson r(score_delta, gap) = +0.243. Within-subject r is +0.44 on Hamerton, +0.25 on Ebers, **−0.25 on Babur**. The largest within-subject correlation (Hamerton +0.44) is on the smallest block (22K chars), not on Babur (335K chars). If texture leakage were driving the result, the relationship should be strongest where the block is largest and most texture-rich. It is not.

**The mechanism the data actually supports** — visible across the qualitative cases — is two-part: (1) Letta's block retains specific named entities that the held-out battery is sometimes built around, and reusing those names produces responses that score well when the question's answer is structured around those entities (Ebers q30: "Frederick William IV", "Langethal", "Middendorf"). (2) Letta speaks with content-confidence; Spec hedges when the predicate scaffold cannot reach the question. When confidence aligns with truth, Letta wins; when confidence is wrong-direction, Spec's hedge wins. The clearest counter-cases are Hamerton q27 (Spec wins +2.4 on a question where Letta is closer to held-out in cosine but predicts the wrong direction on whether Hamerton would self-publish) and Hamerton q51 (Spec wins +3.0 by predicting "stay near guardian" — the held-out resolution).

**Recommendation for §4.5.** Soften the surface-syntactic framing. The "interpretive accuracy or surface-syntactic alignment" framing in the v11.8 §4.5 paragraph is not supported by either the verbatim-phrase test (0.0% overlap on every question) or the topic-alignment test (gap +0.011, weak correlation, sign-flips on Babur). A reframing that names the actual mechanism — named-entity grounding plus content-confidence — is more accurate and survives both measures. The §7.5 generation-time held-out experiment retains its priority but addresses a more refined question: not "do responses echo phrasing" (already answered: no), but "does the block's named-entity stock confer an advantage on questions the entity was central to?"

## Aggregate statistics

### Headline counts

| Metric | Value |
|---|---:|
| N total paired questions | 119 |
| - Hamerton (qid 21–60) | 39 |
| - Ebers (qid 1–40) | 40 |
| - Babur (qid 1–40) | 40 |
| Class A count (cos_letta_spec > 0.75 AND \|delta\| > 1.0) | 29 (24.4%) |
| - Of which Letta wins | 26 |
| - Of which Spec wins | 3 |
| Class A mean texture_gap | +0.011 |
| Class B count (Spec excels: delta < −0.5) | 11 (9.2%) |
| - With positive texture_gap (≥ +0.05) | 3 |
| Class C count (both ≥ 3.0 AND cos_letta_spec < 0.5) | 0 |
| Class C relaxed (cos < 0.6) | 1 (Hamerton q25) |

### Surface-syntactic test (5-gram verbatim phrase overlap)

| Subject | Letta mean / max | Spec mean / max | Pearson r(delta, gap) |
|---|---:|---:|---:|
| Hamerton | **0.0%** / 0.0% | **0.0%** / 0.0% | undefined (zero variance) |
| Ebers | **0.0%** / 0.0% | **0.0%** / 0.0% | undefined (zero variance) |
| Babur | **0.0%** / 0.0% | **0.0%** / 0.0% | undefined (zero variance) |

**Pooled:** 0.0% on all 119 questions on both sides. Pearson r is undefined because there is no variance in the gap. Maximum 5-gram overlap on any single question for any system is 0.0%.

### Short-phrase / named-entity test (3-gram overlap)

| Subject | Letta mean / max (%) | Spec mean / max (%) | Pearson r(delta, gap) | Spearman ρ |
|---|---:|---:|---:|---:|
| Hamerton (n=39) | 0.051 / 0.766 | 0.021 / 0.311 | −0.287 | (n/a) |
| Ebers (n=40) | 0.072 / 1.316 | 0.031 / 0.673 | +0.202 | (n/a) |
| Babur (n=40) | 0.077 / 2.137 | 0.063 / 1.724 | +0.037 | (n/a) |

**Pooled (n=119):** Pearson r = **−0.046**, Spearman ρ = +0.053. Both are statistical zeros at this sample size (SE ≈ 0.09). Within-subject r's are dispersed without a consistent sign. Letta has a small absolute edge in mean 3-gram overlap (≈1.2–2× Spec) but in absolute terms all values are well under 0.1% and the gap does not correlate with `score_delta`.

### Topic-alignment test (MiniLM mean-pooled cosine)

| Subject | mean cos_letta_heldout | mean cos_spec_heldout | mean gap | Pearson r(delta, gap) |
|---|---:|---:|---:|---:|
| Hamerton (n=39) | 0.396 | 0.381 | +0.016 | +0.439 |
| Ebers (n=40) | 0.384 | 0.374 | +0.010 | +0.245 |
| Babur (n=40) | 0.314 | 0.301 | +0.013 | **−0.245** |

**Pooled (n=119):** Pearson r = +0.243, Spearman ρ = +0.183. Hamerton's +0.44 is the only within-subject r meaningfully above zero; Babur's −0.25 is in the opposite direction. Babur — the largest block, the highest verbatim sentence duplication within the block, the subject where texture-leakage should be strongest if the mechanism were the dominant driver — is exactly where the within-subject relationship is weakest and reversed. The Hamerton +0.44 signal is real but small (within-subject SE ≈ 0.16; r = 0.44 is roughly 2.7 SE from zero) and operates on the smallest block.

### Strict leakage signature (a priori test)

- `cos_letta_heldout > 0.7` AND `cos_spec_heldout < 0.4` AND `score_delta > +1.0`: **0 of 119**.
- Relaxed (`cos_letta_heldout > 0.55`, `gap > +0.15`, `delta > +1.0`): **0 of 119**.

The clean leakage signature implied by the §4.5 framing is not present in the data at the case-level.

## Worked examples (4 + 2 supplementary)

The following six examples illustrate the four distinct mechanisms by which Letta and Spec scores diverge. Two for the Letta-wins direction, two for the Spec-wins direction, plus two illustrating the within-subject heterogeneity. All quantitative numbers below are reproducible from the saved CSV.

### Example 1 — Class A, Letta wins by **named-entity reconstruction** (the cleanest leakage-adjacent case)

**Subject:** Ebers, q30. **Class:** A.
**Question:** "How does Ebers characterize the relationship between personal liberal beliefs and public respect for authority?"

**Held-out passage:**
> The time I spent in Keilhau was during the period of the worst reaction, and I now know that our teachers would have sat on the Left in the Prussian Landtag; yet we never heard a disrespectful word spoken of Frederick William IV, and we were instructed to show the utmost respect to the prince of the little country of Rudolstadt to which Keilhau belonged.

**Per-judge scores:**
| | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Letta | 4 | 4 | 4 | 4 | 4 | **4.0** |
| Spec | 2 | 1 | 3 | 2 | 1 | **1.8** |

**Surface measures:** 5-gram overlap (Letta vs held-out) = **0.0%**. 3-gram overlap = 0.766% (matched grams: "frederick william iv", "william iv and"). Cosine: cos_letta_heldout = 0.371, cos_spec_heldout = 0.265, cos_letta_spec = 0.767. Texture gap = +0.106.

**Letta opening (verbatim):**
> Ebers demonstrates a nuanced understanding of how personal liberal convictions can coexist with public deference to established authority — a tension he observed directly at the Keilhau Institute during politically charged times in Prussian history... Ebers characterizes his teachers — particularly Langethal, Middendorf, and Barop — as embodying this balance. These educators held liberal tendencies yet maintained respectful attitudes towards authority figures, including Frederick William IV and local rulers.

**Spec opening (verbatim):**
> Ebers doesn't appear to experience these as fundamentally opposed — rather, he operates within a framework where they coexist through deference to legitimate authority combined with private intellectual independence... His parents tested his commitment to his wife for years before approving marriage; rather than rebelling, he accepted this constraint as legitimate exercise of parental prerogative.

**Mechanism reading.** Letta names the entities the held-out passage names — Keilhau, Langethal/Middendorf/Barop, Frederick William IV. Spec reaches for behavioral anchors (deference to parents, deference to wife) that are structurally adjacent but referentially different. The judges agree that Letta's response answers the question; Spec's answer is rated lower because its examples — courtship, child-rearing — are not the canonical Keilhau-political-deference scenario. **Even here, the closest case to leakage in the dataset, the 5-gram overlap is 0.0%.** What is shared is the named-entity stock (3-token proper noun sequences), not phrasing. This is the named-entity-grounding mechanism: the Letta block ingested the Keilhau chapters and retained the entity names; the Spec compresses those entities away because they are not behavioral predicates. When the held-out battery is structured around those entities, Letta has a content advantage that the rubric rewards.

### Example 2 — Class A, **Spec wins** by epistemic flagging on a wrong-direction Letta response

**Subject:** Hamerton, q29. **Class:** A.
**Question:** "When offered a grand opportunity to organize a Lancashire art exhibition by a prominent figure, would Hamerton accept?"

**Held-out passage:**
> I felt the whole weight of my inexperience, and said to myself: "Whatever we do it is certain that mistakes will be committed... All mistakes will be laid to my door." ... I therefore firmly declined.

**Per-judge scores:**
| | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Letta | 1 | 2 | 2 | 2 | 2 | **1.8** |
| Spec | 2 | 4 | 4 | 5 | 4 | **3.8** |

**Surface measures:** 5-gram overlap = 0.0% on both sides. 3-gram overlap = 0.166% Letta, 0.000% Spec. Cosine: cos_letta_heldout = 0.262, cos_spec_heldout = 0.372, cos_letta_spec = 0.767. Texture gap = −0.110.

**Letta:** "Hamerton would likely **accept such an opportunity**, though with characteristic thoughtfulness... Most likely outcome: He would accept, but on his own terms."

**Spec:** "I need to flag immediately: this question asks me to project into a domain where the source material is explicitly thin. Professional institutional work, public-facing curatorial roles, collaborative projects with established figures — these are not well-evidenced... That said, the *tensions* that would activate are legible. [Then enumerates A4 / A5 / A8 / A10 anchors and identifies A8 (Agency Primacy) as the variable that could push him to decline.]"

**Mechanism reading.** Hamerton declined the exhibition. Letta predicts the wrong direction (accept). Spec hedges, lists anchors that push both ways, and surfaces the constraint that produced the actual refusal. The score difference is driven by **directional correctness under uncertainty**, not by texture. This case directly contradicts a texture-leakage causal story: Letta's confident-but-wrong response loses to Spec's epistemic-flagged-and-correct response.

### Example 3 — Class B, **Spec wins** despite Letta being topic-closer to held-out

**Subject:** Hamerton, q27. **Class:** B (Spec excels).
**Question:** "Would Hamerton publish his early poetry at his own expense, and what would the commercial result be?"

**Held-out passage:**
> My volume, "The Isles of Loch Awe and other Poems," appeared the day I came of age... It was published at my own expense, in an edition of two thousand copies, of which exactly eleven were sold in the real literary market.

**Per-judge scores:**
| | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Letta | 2 | 1 | 2 | 2 | 2 | **1.8** |
| Spec | 5 | 3 | 4 | 5 | 4 | **4.2** |

**Surface measures:** 5-gram overlap = 0.0% on both sides. 3-gram overlap = 0.766% Letta ("at my own expense"), 0.000% Spec. Cosine: cos_letta_heldout = 0.520, cos_spec_heldout = 0.342, cos_letta_spec = 0.669. Texture gap = +0.178 — one of the largest positive gaps in the dataset.

**Letta:** "Based on the working model, I would likely **not** publish my early poetry at my own expense." [Predicts no publication; commercial result framed as "negligible to ruinous" if published.]

**Spec:** "**He would publish at his own expense.** Several anchors converge here: A10 (Breadth Over Depth), A6 (Mortal Scale), A1 (Self-Authority)... He would not be surprised or wounded by poor sales."

**Mechanism reading.** This is the strongest single counter-evidence against texture-leakage as a causal driver. Letta's response is topic-closer to the held-out (cos = 0.52, well above the 0.40 mean) — both speak in the language of self-publication, commercial doubt, ruined finances. Letta even shares the verbatim 3-gram "at my own expense" with the held-out passage. But Letta's prediction is **wrong in direction**: Hamerton did publish, at his own expense, in an edition of 2,000 copies. The Spec, despite being further from the held-out passage in cosine terms (0.34) and sharing zero verbatim phrases at any granularity, gets the direction correct via anchor reasoning. The judges reward directional correctness over texture similarity. **Topic-similar with shared named entity but wrong-direction loses to topic-distant but right-direction.**

### Example 4 — Class B, **Spec wins** with ceiling-level scores via predicate-scaffold reasoning

**Subject:** Hamerton, q51. **Class:** B (Spec excels).
**Question:** "Given Hamerton's deep affection for his guardian and knowledge of her heart disease, would he choose a distant school or stay near her?"

**Held-out passage:**
> I quickly resolved that as Death would probably soon separate us, and might separate us at any moment, I would keep as much as possible near my guardian during her life.

**Per-judge scores:**
| | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Letta | 2 | 2 | 2 | 2 | 2 | **2.0** |
| Spec | 5 | 5 | 5 | 5 | 5 | **5.0** |

**Surface measures:** 5-gram overlap = 0.0% on both sides. 3-gram overlap = 0.000% on both. Cosine: cos_letta_heldout = 0.226, cos_spec_heldout = 0.341, cos_letta_spec = 0.746. Texture gap = −0.116.

**Letta:** "Hamerton would probably **choose the distant school, but with profound internal conflict and anxiety**..."

**Spec:** "He would stay near her. But the staying would cost him something he would feel acutely... A guardian who has earned his trust through consistent care and whose heart is literally fragile does not become a secondary consideration because a distant school offers superior credentials or prestige."

**Mechanism reading.** Held-out resolves to "stay." All five judges score Spec at the ceiling (5/5) and Letta at 2/5. The Letta block's content-equivalent surface (cos_letta_spec = 0.75) does not save it from the wrong directional answer. The Spec's anchor scaffold ("emotional attachment to a guardian above optimal institutional advancement") aligns exactly with the held-out resolution. This case shows the limit of any texture-driven story: when the question has a clear answer in the held-out passage, the system that gets the direction right wins regardless of similarity metric.

### Example 5 — Class C-relaxed (different paths, similar quality)

**Subject:** Hamerton, q25. **Class:** C (relaxed).
**Question:** "Given Hamerton's difficulty following spoken French at Loch Awe despite years of study, what would he do about it?"

**Held-out passage:**
> This plagued me with an irritating sense of ignorance, so I looked back on my education generally, and found it unsatisfactory... I determined to acquire some substantial knowledge of modern languages, and to begin by learning French over again.

**Scores:** Letta 3.6, Spec 4.0. cos_letta_spec = 0.561 (the lowest such score among questions where both systems pass 3.0).

**Letta:** Predicts active remediation — seek native speakers, methodical practice, French literature, gradual progress. Direct prediction.

**Spec:** Refuses to fabricate a historical answer; requests Hamerton's own testimony as the epistemically superior evidence; offers structural predictions only ("not accept vague explanations," "excavate backward to identify when the formation failed," "treat the problem as one of disciplined, focused practice").

**Mechanism reading.** Both score well; the responses are structurally different. Letta predicts the action. Spec models the *manner* of investigation that would produce the action. Judges reward both. This is the rare case where the rubric tolerates two genuinely different answer shapes for the same question.

### Example 6 — Babur counter-pattern: large block, high duplication, fine-grained question

**Subject:** Babur, q22. **Class:** B (Spec excels) with positive 3-gram and cosine gap.
**Question:** "How does Babur respond to environmental conditions like approaching monsoon rains when conducting military operations?"

**Held-out passage:**
> and as, moreover, the Rains were near, we in our turn wrote and despatched words for peace on the conditions mentioned.

**Scores:** Letta 2.0, Spec 3.0. **Spec wins by 1.0.** cos_letta_heldout = 0.443, cos_spec_heldout = 0.330. Texture gap = +0.113.

**Letta:** Long (4,791 chars) general-purpose discourse on monsoon strategy: strategic adaptation, logistical planning, water management, troop morale, consultation. No mention of peace negotiation in response to rains.

**Spec:** Shorter (1,982 chars) flagged response: "I cannot find explicit documentation of how Babur responds to approaching monsoon rains during military operations." Then: "withdraws rather than fighting to annihilation when conditions become unmanageable" — closer to the held-out's resolution.

**Mechanism reading.** This is the signature pattern that drives Babur's negative within-subject Pearson r on cosine. Babur's Letta block is the largest (335,349 chars, near the API ceiling) and has 25.4% verbatim sentence duplication within the block itself. The block contains a great deal of texture, but the texture is bulk; it floods the response with monsoon-adjacent material that does not converge on the specific peace-negotiation behavior the held-out cites. Spec, working from compressed predicates, lands on "withdraws rather than fighting to annihilation" — which matches the peace-dispatch behavior more directly. **Large block size produces texture-rich-but-unfocused responses that lose to compressed-but-targeted predicate reasoning.** This is the structural reason Babur's within-subject cosine r is negative despite Letta winning aggregate by +0.54.

## Class composition and what it implies

The class structure is itself diagnostic:

- **Class A is dominated by Letta wins (26/29).** Consistent with the aggregate result. Within Class A, sign of `score_delta` aligns with sign of `texture_gap` on 17/29 = 59%, slightly above chance but not driving the result. Class A mean texture_gap = +0.011 — symmetric around zero.
- **Class B (Spec wins by ≥0.5) at 11/119 is large enough to matter.** 9% of questions favor Spec by a margin large enough to be a paper finding. Three Class B cases have positive texture_gap (Letta topic-closer despite losing), directly contradicting any texture-leakage causal story at the case level.
- **Class C (genuinely different paths to similar quality) has only one example at relaxed threshold.** When both systems work, they tend to converge on similar content. The "different paths" framing the §4.5 paragraph implies is rare.

## Should §4.5 incorporate per-question framing?

**Yes — and the framing should explicitly retire the surface-syntactic framing.**

Specific paper-edit recommendations (for the editing instance, not applied here):

1. **§4.5 line 1502 paragraph should be revised.** The "interpretive accuracy or surface-syntactic alignment" framing is not supported. Verbatim phrase overlap with the held-out passage is **0.0% on every question** for both systems. Topic-alignment correlation with `score_delta` is +0.243 pooled but with sign-flips across subjects and a negative correlation on the largest block (Babur, where the mechanism should be strongest if it operates). A reframing is warranted that names the actual mechanism: **named-entity grounding** (the Letta block retains specific people, places, and dates the held-out battery references) plus **content-confidence** (Letta reasons through scenes; Spec hedges when the predicate scaffold cannot reach the question). When confidence aligns with truth, Letta wins; when confidence is wrong-direction, Spec's hedge wins. 9% of questions have Spec winning by ≥0.5, including cases where Letta is topic-closer to the held-out passage but wrong-direction (e.g., Hamerton q27 self-publication: Letta predicts "would not publish" with shared 3-gram "at my own expense"; Spec predicts "publishes" via anchor reasoning; held-out confirms publication).

2. **Add the 5-gram null result as a sentence in body or footnote.** "On the 119-question case study, Letta's responses share zero verbatim 5-token phrases with the held-out passage on every question; the Spec's responses share zero on every question. The systems differ in what scenes they reconstruct and what entities they name, not in surface phrasing." This is a strong, falsifiable, easily-checkable claim that closes the most aggressive form of the surface-syntactic concern.

3. **One worked example in body, one in Appendix G.** Body candidate: Example 4 (Hamerton q51 — Spec wins 5.0 vs 2.0 by directional correctness). Strongest single demonstration that the Spec's predicate scaffold can produce ceiling-level accuracy. Appendix candidate: Example 1 (Ebers q30 — Letta wins by named-entity reconstruction). The closest case to leakage in the dataset, presented alongside the 5-gram null and the 3-gram statistic so readers can judge what "leakage" actually looks like at this granularity.

4. **§7.5 generation-time held-out experiment retains its priority but addresses a refined question.** The original framing — "does Letta echo phrasing the held-out passage uses" — has been answered: no. The refined question is: "does the Letta block's named-entity stock confer an advantage on questions whose answer is structured around those entities, in a way that compressed predicate reasoning cannot replicate?" A generation-time held-out (a question whose entities and resolution appear in no source the system processed) would test this directly.

## Open questions for the §7.5 follow-up specification

1. **Generation-time held-out battery design.** Construct questions whose ground-truth resolution and named entities appear in sources the systems were not given. For autobiographical subjects, this means a third-party biography, a contemporaneous letter, or a known later autobiography volume the corpus excluded. Per subject, ten such questions paired against held-out passages from these external sources. Test whether the Letta-vs-Spec gap survives when neither named-entity reuse nor topic alignment is structurally possible.

2. **Paraphrase-resistant rubric.** The current rubric compares responses to held-out *passages*. A version that compares response *direction/decision/inference* to held-out *outcome* (extracted as a structured tag, not free text) would be less susceptible to topic-alignment confounds. Worth piloting on the existing 119-question set as a sensitivity check before the §7.5 experiment.

3. **Block-size ceiling probe.** Babur's negative within-subject cosine r and large block (335K chars) suggests the relationship may be non-monotonic: small blocks (Hamerton, 22K) preserve focus and produce topic-aligned wins; large blocks (Babur, 335K) saturate the response with bulk material that loses on focused questions. A scaling experiment varying block size on a fixed subject would isolate this.

4. **Per-judge texture sensitivity.** Re-run the within-subject Pearson r within each of the 5 judges. If GPT-class judges show a stronger texture-r than Anthropic judges, the rubric is judge-dependent and the result generalizes less. (Not run here; flagged for a follow-up.)

## Provenance

- **Per-question CSV:** `docs/research/letta_vs_spec_per_question_scores_20260507.csv` (119 rows, 26 columns).
- **Summary JSON:** `docs/research/letta_vs_spec_leakage_summary_20260507.json`.
- **Reproducibility script:** `scripts/letta_vs_spec_leakage_analysis_20260507.py` (no API calls; sentence-transformers all-MiniLM-L6-v2 local; runs in 1–2 minutes after model load).
- **Full worked-example response text:** `docs/research/_letta_vs_spec_worked_examples_text.md` (verbatim Letta and Spec responses for the 8 inspected questions).

**Aggregation rule.** Per-question score = mean of available judge scores across the 5-judge primary panel {haiku, sonnet, opus, gpt4o, gpt54}, dropping `parse_failure=True` rows. Drop rule for paired analysis: keep `(subject, qid)` only if both Letta and Spec have at least one valid judge score. Result: **0 questions dropped on any subject** — full 39+40+40 = 119 coverage.

**Reproducibility check.** Per-subject mean Δ in this analysis (Hamerton +0.14, Ebers +1.05, Babur +0.54) match the §4.5 paper's emit-script values within rounding (paper: +0.14, +1.05, +0.54). The per-judge mean cells reproduce; the 119-question total matches the case-study denominator.

**Surface-syntactic measure.** N-gram overlap is computed token-by-token on lowercased word tokens (regex `[a-z]+`, punctuation stripped). For each question, count how many `n`-token sliding windows of the response appear verbatim in the held-out passage's `n`-token window set; report the percentage. The 5-gram threshold is the canonical "verbatim phrase" test from `_v11_emit_4_5_letta.py`. The 3-gram is reported as a sensitivity measure that picks up named-entity sequences and stock phrases.

**Topic-alignment measure.** MiniLM-L6-v2 mean-pooled-by-sentence cosine. Sentences are split via regex `(?<=[.!?])\s+`, embedded individually (batch=32, normalize_embeddings=True), then mean-pooled and L2-normalized. This matches the precedent in `scripts/analyze_letta_semantic_duplication.py`. Chosen for fidelity on long texts (Babur held-out passages and the Letta block exceed MiniLM's 256-token window in single-shot mode).
