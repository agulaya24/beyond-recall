# Base Layer (MiniLM-L6-v2 + ChromaDB): C1 vs C3 Paired Response Analysis

**Question:** Base Layer's own retrieval substrate is the paper's open-source "retrieval floor" — the what-can-be-hacked-together baseline. Aggregate spec-delta on low-baseline subjects is +0.13 (positive on 7 of 9 subjects). That's smaller than Mem0 controlled (+0.13 matched), Letta controlled (+0.23), and Zep controlled (+0.20). The paper's stated hypothesis for this gap is that Base Layer's facts+spec prompt template triggers more explicit uncertainty framing than the other systems' templates, blunting the spec's contribution. Does the paired C1 vs C3 data support this, or is something else going on?

**Method:** Mirrors `supermemory_c1_vs_c3_paired_analysis.md` and `mem0_letta_zep_c1_vs_c3_analysis.md`. 5 low-baseline subjects selected for spread: `ebers` and `keckley` for continuity with prior analyses, `hamerton` as the paper's flagship named-subject case (with documented pipeline-tuning bias on Base Layer), `yung_wing` as the strongest paired-delta case, `babur` as the low-C1 large-corpus outlier. Pair responses by `question_id` across `C1_baselayer` (retrieval only) and `C3_baselayer` (retrieval + spec) from `baselayer_results.json`. Compute per-question mean score across the six judges in `baselayer_judgments_merged.json` (haiku, sonnet, opus, gpt4o, gpt54, gemini_flash). Bucket questions into (a) similar |Δ| ≤ 0.3, (b) C3 higher Δ > +0.3, (c) C3 lower Δ < −0.3. Each subject has 39 held-out questions.

Data script: `scripts/analyze_baselayer_c1_vs_c3.py`. Raw candidate bundle: `docs/research/_baselayer_c1_c3_candidates.json`.

---

## 1. Per-subject distribution of paired deltas

| Subject | C1 mean | C3 mean | Δ | C3 higher (>0.3) | similar | C3 lower (<−0.3) | C3 big-win (>1.0) | C3 big-loss (<−1.0) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ebers | 1.76 | 1.84 | +0.08 | 18 | 10 | 11 | 0 | 1 |
| keckley | 2.44 | 2.44 | −0.01 | 18 | 8 | 13 | 3 | 5 |
| hamerton | 2.73 | 2.78 | +0.05 | 16 | 10 | 13 | 8 | 7 |
| yung_wing | 2.23 | 2.56 | **+0.33** | 22 | 7 | 10 | 7 | 2 |
| babur | 1.68 | 1.80 | +0.13 | 20 | 10 | 9 | 4 | 2 |

The same redistribution finding holds: aggregate deltas are mixtures. Even Base Layer's strongest win (yung_wing, +0.33) has 10 questions where the spec hurts by >0.3 and 2 big-losses. Even the near-zero Keckley row has 18 wins and 13 losses, with 5 big-losses — the flat mean conceals large swings in both directions.

**Hamerton is the anomaly** — 8 big-wins *and* 7 big-losses on one subject. Hamerton is also the one low-baseline subject where Base Layer wins C1 outright (2.73 vs Mem0 1.72, Letta 2.56, Zep 1.98; `DATA_REFERENCE.md` §12). The paper notes this as pipeline-tuning bias — Hamerton was the Base Layer development subject — so Hamerton's paired profile here should not be read as representative of Base Layer's retrieval-substrate properties generally.

**Yung_wing is the most positive case.** Its +0.33 aggregate delta comes from 22 questions where C3 wins by >0.3 and 7 big-wins, against 10 losses and only 2 big-losses. This is the cleanest positive profile in the Base Layer sample and is the subject most comparable to Zep's strong subjects in the mlz analysis.

---

## 2. The three failure modes — do they reproduce?

Short answer: yes, all three. The story the Supermemory and mlz analyses told about specification dynamics reproduces on Base Layer's own retrieval substrate.

### 2.1 Structural refusal (Keckley Q21)

**Keckley Q21 — identical penalty to Supermemory.**

| System | C1 mean | C3 mean | Δ |
|---|---:|---:|---:|
| Supermemory (prior) | 3.83 | 1.50 | −2.33 |
| **Base Layer** | **3.33** | **1.00** | **−2.33** |
| Mem0 (prior) | 2.00 | 1.50 | −0.50 |
| Letta (prior) | 1.33 | 2.33 | +1.00 |
| Zep (prior) | 1.83 | 1.33 | −0.50 |

Base Layer's C3 opens with *"I need to be direct: the behavioral specification and retrieved facts provided do not contain information about Elizabeth visiting or not visiting her mother's grave"* — nearly verbatim the Supermemory C3 phrasing. All three judges in the available panel scored C3 at 1. This is the single most striking reproduction finding in the Base Layer analysis: a substrate-agnostic specification-level dynamic surfacing the same refusal with the same penalty.

It also confirms the mlz analysis's reading that the Q21 refusal tax is a function of C1 strength — Base Layer's C1 is 3.33 (productive speculation, same register as Supermemory's 3.83), and the spec-induced refusal tax is correspondingly large. On systems where C1 already hedges (Mem0, Zep), the tax is small; on Letta, where C1 also refused, the spec's structured refusal actually helped.

### 2.2 Over-theorization on simple questions

**Yung Wing Q31 — C1=3.33, C3=2.00, Δ=−1.33.**

Held-out: *"Mandarin Yung Wing was scarcely able to support the joy of his triumph. For two days, as he has told the writer, he could neither eat nor sleep. He walked on air, and he worshipped God."*

C1 produces a plain, correct prediction: "a complex mixture of emotions" including "relief and vindication," "gratitude." C3 opens: *"his reaction would be characterized by a distinctive emotional signature that holds multiple registers simultaneously rather than collapsing into simple triumph"* and then structures it through "Gratitude as Epistemology." The held-out is "walked on air." The spec-elaborated answer is a theory of gratitude. Same Pareto loss structure as Supermemory's Ebers Q34 and Letta's Ebers Q17.

### 2.3 Default-axiom overfires on counter-example moments

**Ebers Q1 — C1=3.00, C3=2.00, Δ=−1.00.**

Held-out: *"Like the apostle, I would fain proclaim the gospel to all men according to the best of my powers, in order to bring them into close communion with the Redeemer."* (Unconditional, enthusiastic.)

C1: "he would likely respond **positively and earnestly**." Matches the unconditional register.

C3: "genuine receptivity, **but only if the appeal is grounded in lived particularity rather than abstract principle**." The spec's "lived particularity over abstraction" axiom is correct on average but overfires on this specific unconditional-evangelical moment. Same pattern as Mem0's Ebers Q1 and Supermemory's Sunity Devee Q11.

---

## 3. The prompt-hedging hypothesis — partially supported, partially contradicted

The paper's hypothesis predicts Base Layer's C3 responses should show **more** explicit-uncertainty framing than commercial C3 responses because of the facts+spec prompt template. A lexical proxy (search for *"I need to be direct,"* *"I should acknowledge,"* *"I cannot,"* *"I don't know,"* *"the retrieved facts do not,"* *"speculat,"* and 13 related triggers) gives the following direction of effect going C1 → C3:

| Subject | C1 avg triggers | C3 avg triggers | C1 flagged | C3 flagged | Direction |
|---|---:|---:|---:|---:|---|
| ebers | 0.31 | 0.15 | 11/39 | 5/39 | **drops** |
| keckley | 0.23 | 0.08 | 7/39 | 3/39 | **drops** |
| hamerton | 0.41 | 0.69 | 14/39 | 13/39 | rises |
| yung_wing | 0.26 | 0.26 | 10/39 | 8/39 | flat |
| babur | 0.10 | 0.28 | 4/39 | 10/39 | rises |

**Two drops, one flat, two rises.** The hypothesis is not uniformly supported. The direction of C1→C3 hedging change is subject-dependent in a way the prompt-template-alone story does not predict.

A better reading: Base Layer's prompt template produces explicit-uncertainty language when the spec + retrieved facts underdetermine the held-out pattern. On Hamerton and Babur — the two subjects where the spec adds interpretive axioms that often exceed what the retrieved facts can ground — C3 carries *more* "I should flag what I don't know" language than C1. On Ebers and Keckley, the spec is *more grounded* in the subject's documented behavior (these are subjects with more direct autobiographical prose) and C3 actually produces *less* hedging than C1.

The paper's framing that Base Layer's template is a uniformly stronger hedger is **wrong as stated**. The honest framing is: **when the spec cannot be grounded in the retrieval substrate, Base Layer's prompt template surfaces the ungroundedness explicitly**. This is a feature of template transparency, not a template weakness per se.

### Three illustrative responses — explicit uncertainty framing

These are three C3 responses whose openings illustrate the prompt-template pattern the hypothesis is pointing to:

**Hamerton Q21 (London visit) — C3=2.67, C1=4.33, Δ=−1.67.** C3 opens: *"This is a question that requires me to acknowledge what I *don't* know from the retrieved facts, because the behavioral specification makes clear that Hamerton would insist on the distinction between what he actually experienced and what I might conjecture."* The held-out is a plain "most disagreeable place I had ever seen." C1 landed on "significant discomfort and alienation" and scored 4.33. C3's spec-cued epistemic-distinction opening cost 1.67 points.

**Hamerton Q32 (English or foreign wife) — C3=1.00, C1=4.00, Δ=−3.00.** C3 opens: *"This question cannot be answered from the available evidence, and I should flag that directly rather than speculate into the gap."* C1 correctly predicted "foreign woman, particularly a French one" from the documented French affinity. This is the largest single-question loss in the Base Layer sample. The refusal template fired on a question the retrieval could answer.

**Yung_wing Q4 (technical delegation) — C3=3.33, C1=1.00, Δ=+2.33.** C3 opens: *"Based on the behavioral specification and retrieved facts, I need to be direct about what the evidence actually supports and what it does not."* Then **proceeds to produce a correct answer from the spec's axioms** ("She grants autonomy consistent with having vetted competence and then defers to it"). All three available judges scored C3 higher than C1. The same template language that cost Hamerton Q32 three points rewards Yung_wing Q4 by two.

**The key nuance:** explicit-uncertainty framing is not the same as refusal. When the model produces the frame and then answers, scoring improves. When it produces the frame and stops, scoring collapses. Base Layer's prompt template permits both paths. The paper's hypothesis conflates them.

---

## 4. The three-mechanism story reproduces cleanly on Base Layer

### 4.1 Pattern supply — Ebers Q11

C1 (2.00): builds on retrieved facts about Ebers' tenure managing an institution, predicts "active intervention and reform" as generic character trait.

C3 (3.00): *"Ebers does not respond with blanket condemnation. Instead..."* supplies the ideal-vs-reality axiom directly, lands closer to the held-out *"I had come hither full of beautiful ideals... but the very first day made me suspect how many obstacles I should encounter."* Same mechanism as Mem0 Ebers Q11 — retrieval provides biography, spec provides the pattern.

### 4.2 Interpretive recovery — Keckley Q9

Held-out: *"I bathed Mrs. Lincoln's head with cold water, and soothed the terrible tornado as best I could."*

C1 (2.33): "offer practical, consistent support." Generic.

C3 (4.33): *"Immediate Response: Presence and Practical Care."* Names the presence-over-words axiom and applies it. The retrieved facts included no Mrs. Lincoln passage; the spec carried the axiom that produces the correct prediction. Same mechanism as Zep's Seacole Q2.

### 4.3 Structural refusal — Keckley Q21, Hamerton Q32

Documented above (§2.1, §3). The spec's documented-dignity axioms trigger the refusal template; the judges score the refusal as content failure. Reproduces the Supermemory pattern exactly on Keckley Q21 (identical −2.33 Δ), and produces the single largest paired swing in the Base Layer sample on Hamerton Q32 (−3.00).

---

## 5. Open-source-floor question — does Base Layer feel different in kind?

Aarik's framing question: Base Layer is the open-source retrieval substrate — "what can be hacked together." Is Base Layer's C1 a *different kind* of response than the commercial systems' C1s, or the same kind served differently?

**Same kind, different substrate.** Base Layer's C1 responses use the same structural elements as Mem0, Letta, Zep, and Supermemory C1s: markdown headings, bulleted evidence blocks, named facts in quotes, clearly-demarcated "Based on retrieved facts" openings. A reader blind-presented with a Base Layer C1 and a Mem0 C1 could not reliably distinguish them on response form. The differences are on the substrate side: Mem0 retrieves atomic sentences, Letta retrieves duplicated chunks, Zep retrieves stringified edge reprs, Base Layer retrieves semantic-embedding neighbors from ChromaDB. What the generation model does with any of these is structurally the same.

This confirms `KEY_FINDINGS.md` m11 ("Base Layer retrieval is comparable to commercial systems but not superior") from the paired-response side: BL is **not a different category** of retrieval, it is one more instance of the category. The aggregate +0.12 delta reflects ordinary within-category variance — similar to Mem0's +0.15 controlled and Zep's +0.22 controlled — not a substrate-level limitation.

The open-source-floor claim is conservative and correct: a MiniLM embedder plus ChromaDB plus a generation call produces responses in the same band as commercial memory services. The marginal value commercial systems add over Base Layer is small (0.00-0.10 points on average). The Base Layer spec then adds +0.12-0.13 on top of its own retrieval and comparable deltas on top of the commercial retrievers.

---

## 6. Why is Base Layer's spec-delta the smallest of the five systems?

The honest answer, from the paired data:

1. **Base Layer has the lowest C1 mean on three of the five subjects studied** (ebers 1.76, yung_wing 2.23, babur 1.68). This is the opposite of a ceiling effect. The spec has more headroom on Base Layer than on Supermemory. If prompt-template hedging alone predicted a smaller delta, we would expect it to show most on the low-baseline subjects. Instead, the biggest per-question wins also occur on those same subjects (Yung Wing Q4 +2.33, Ebers Q11 +1.00, Babur Q6 +2.00). The spec does work on Base Layer.

2. **The losses are concentrated on a narrow set of question types,** primarily questions where the retrieved facts underdetermine the held-out pattern and the spec's epistemic-humility axioms fire (Hamerton Q32, Hamerton Q21, Keckley Q21, Keckley Q22). These are the same question types that hurt every system's C3; Base Layer is not uniquely bad at them, it just has one or two more of them per subject than the better-performing commercial systems.

3. **On Hamerton specifically, the 7 big-losses are inflated by pipeline-tuning bias.** Hamerton's C1 is 2.73 — the highest of the five subjects and the only subject where Base Layer wins C1 outright. That high C1 creates more headroom-for-loss, which the large-swing profile reflects. Reading Hamerton's paired distribution as representative of Base Layer as-a-system would overstate the losses.

So the paper's prompt-hedging framing captures a real phenomenon on two of the five subjects but misdescribes the overall mechanism. The more accurate summary:

- Base Layer's spec helps on the same population as the commercial systems' specs (low-baseline subjects).
- Base Layer's C1 is comparable to commercial C1s in band and in form.
- Base Layer's C3 losses are concentrated on the same question types as commercial C3 losses (refusal-triggering and counter-example moments) — not on a substrate-specific failure.
- The "prompt-template hedging" effect is real for subjects where spec cannot be retrieval-grounded (Hamerton, Babur), absent or reversed otherwise.

---

## 7. Honest read

The paired analysis supports the paper's core narrative — specification adds interpretive structure above retrieval — and surfaces one claim that should be softened.

**Supported:**
- Aggregate spec-deltas on Base Layer are mixtures of large per-question wins and losses, consistent with the Supermemory and mlz findings.
- The three failure modes (over-theorization, structural refusal, default-axiom errors) reproduce on Base Layer with no substrate-specific additions.
- The three mechanisms (pattern supply, interpretive recovery, structural refusal) reproduce with clean examples on Base Layer's own retrieval.
- Keckley Q21's refusal penalty reproduces with the same Δ as Supermemory (−2.33), which is a strong specification-level finding worth surfacing in the paper.

**Should be softened:**
- The "Base Layer's prompt template uniformly produces more hedging" framing is wrong. The direction of C1→C3 hedging shift is subject-dependent. The honest claim is: *when the spec's axioms cannot be grounded in Base Layer's retrieval, the prompt template surfaces the ungroundedness explicitly, which the content-match rubric sometimes penalizes and sometimes rewards*. Explicit-uncertainty framing is not the same as refusal; Yung Wing Q4 (+2.33 with a "I need to be direct" opening) makes the distinction cleanly.

**One striking example worth surfacing:** Keckley Q21's refusal reproduces on Base Layer with the exact same delta (−2.33) as on Supermemory. Different retrieval substrates, same refusal, same penalty. This is strong evidence that the Q21 refusal is a specification-level dynamic (the documented-dignity and intimate-authority axioms triggering refusal when the subject's internal motive is not recoverable from her own words) rather than a memory-system artifact. It is the single cleanest cross-substrate replication in the study.

**Open-source floor question, answered:** Base Layer is the same kind of retrieval system as the commercial ones, served on different substrate. The paper's conservative framing ("comparable, not superior") is correct. The paired data confirms it from a second angle: not only do the aggregate scores land in the same band, the response forms and failure modes do too. What can be hacked together with MiniLM + ChromaDB + a generation call lands in the same category as what has VC funding behind it.
