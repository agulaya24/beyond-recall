# Beyond Recall — Deterministic Reference Table

**Purpose:** Single source of truth for all citations in the paper. Every reference keyed by `[REF-XX]`. Body uses these keys. Do not cite a paper that does not appear here.

**Last audited:** 2026-04-18 (S113) against `beyond_recall_v6_draft.md`. Reference set synced to actual paper-body citations; unused references removed, new ones added.

**Verification status:**
- `VERIFIED` — arXiv ID or DOI confirmed against public record
- `PROBABLE` — consistent with known literature; full ID not independently confirmed
- `NEEDS CHECK` — incomplete or unconfirmed; requires human lookup before submission

---

## Core References (actually cited in paper body)

| Key | Authors | Title | Venue | Year | ID / DOI | Status |
|-----|---------|-------|-------|------|----------|--------|
| REF-01 | Bartlett, F. C. | Remembering: A Study in Experimental and Social Psychology | Cambridge University Press | 1932 | ISBN: 978-0521483568 | **VERIFIED** — cited §2.4 |
| REF-02 | Hinton, G.; Vinyals, O.; Dean, J. | Distilling the Knowledge in a Neural Network | NeurIPS Workshop | 2015 | arXiv:1503.02531 | **VERIFIED** — cited §2.4 |
| REF-03 | Zheng, L. et al. | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | NeurIPS | 2023 | arXiv:2306.05685 | **VERIFIED** — cited §2.5 |
| REF-04 | Packer, C. et al. | MemGPT: Towards LLMs as Operating Systems | arXiv | 2023 | arXiv:2310.08560 | **VERIFIED** — cited §2.1, §4.3, §4.3.1, §5.8 |
| REF-06 | Chhikara, P. et al. | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | arXiv | 2025 | arXiv:2504.19413 | **PROBABLE** — cited §2.1 |
| REF-07 | Toubia, O. et al. | Twin-2K: Behavioral Prediction at Scale | arXiv | 2025 | arXiv:2505.17479 | **PROBABLE** — cited §2.3 |
| REF-08 | Chen, R. (Runjin); Arditi, A.; Sleight, H.; Evans, O.; Lindsey, J. | Persona Vectors: Monitoring and Controlling Character Traits in Language Models | arXiv | 2025 | arXiv:2507.21509 | **VERIFIED** — cited §2.4 as "Chen, Arditi, Evans et al. (2025)" (paper uses short form — see Inconsistencies) |
| REF-09 | He, D. et al. | LongMemEval: Benchmarking Long-Term Memory Systems | ICLR | 2025 | arXiv:2410.10813 | **PROBABLE** — cited §2.3, §1.5, §5.10 as "LOCOMO/LongMemEval" |
| REF-10 | Jandaghi, P. et al. | PersonaGym: Evaluating Persona Agents and LLMs | EMNLP | 2025 | arXiv:2407.18416 | **PROBABLE** — cited §2.3 |
| REF-11 | Xiao, J. et al. | AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment | arXiv | 2026 | arXiv:2603.26680 | **NEEDS CHECK** — title/arXiv not independently verified; cited §2.3 |
| REF-12 | Maharana, A. et al. | LoCoMo: Evaluating Long Context Memory in Dialogue | ACL | 2024 | arXiv:2402.17753 | **PROBABLE** — cited §2.3, §1.5, §5.10 |
| REF-13 | Hong, K. (Kelly); Troynikov, A.; Huber, J. | Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Technical Report | 2025 | trychroma.com/research/context-rot | **VERIFIED** — cited §4.7 as "Hong et al. (2025)" |
| REF-14 | Du, Y. (Yufeng) et al. | Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | EMNLP | 2025 | arXiv:2510.05381 | **VERIFIED** — cited §4.7 as "Du et al. (2025)" |
| REF-15 | Jain, K. et al. | Interaction Context Often Increases Sycophancy in LLMs | arXiv / CHI | 2026 | arXiv:2509.12517 | **PROBABLE** — cited §2.4 and §5.4 as "Jain et al. (2026)". **Replaces former REF-15 (CAUSM, NOT FOUND).** Verify author list + venue before submission. |
| REF-16 | Lu, C. (Christina); Gallagher, J.; Michala, J.; Fish, K.; Lindsey, J. | The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models | arXiv | 2026 | arXiv:2601.10387 | **VERIFIED** — cited §2.4 as "Lu et al. (2026)" |
| REF-17 | Jiang, B.; Hao, Z.; Cho, Y.-M.; et al. | Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale | COLM | 2025 | arXiv:2504.14225 | **VERIFIED** — cited §2.4 and §5.2 as "Jiang et al. (COLM 2025)" |

---

## Removed from paper body (S113 audit)

| Former Key | Reason | Status |
|---|---|---|
| REF-05 (Betley, Emergent Misalignment, arXiv:2502.17424) | Not cited anywhere in `beyond_recall_v6_draft.md`. Earlier §5.6 usage removed during voice pass. | REMOVED from active set. Retain record here in case reintroduced. |
| REF-18 (Shi et al., PersonaX, arXiv:2503.02398) | Confirmed removed from paper body (LLM_REVIEW_FIXES.md line 110). | REMOVED. |
| REF-19 (Stacy et al., Bayesian Inverse Planning) | Previously NOT FOUND in literature. Confirmed not cited in v6 body. | REMOVED. |

---

## Verification Checklist (Before ArXiv Submission)

- [ ] **REF-08** (Chen, Persona Vectors) — confirm arXiv:2507.21509 title and full author list; align paper's "Chen, Arditi, Evans et al." short form with canonical (paper omits Runjin/Sleight/Lindsey — acceptable short form if consistent)
- [ ] **REF-09** (LongMemEval) — confirm arXiv:2410.10813 title and authors; paper sometimes writes "LOCOMO/LongMemEval" — LOCOMO is REF-12 (Maharana), LongMemEval is He et al.
- [ ] **REF-11** (AlpsBench) — arXiv ID 2603.26680 is a 2026 submission; verify title and authors exist
- [ ] **REF-13** (Context Rot, Hong) — confirm Chroma URL resolves and lists Kelly Hong as lead
- [ ] **REF-14** (Du, Context Length) — confirm arXiv:2510.05381 title/venue
- [ ] **REF-15** (Jain, Sycophancy) — confirm arXiv:2509.12517 authors + title; paper calls "Jain et al. (2026)" — verify year aligns with arXiv posting
- [ ] **REF-16** (Lu, Assistant Axis) — confirm arXiv:2601.10387
- [ ] **REF-17** (Jiang, Know Me Respond to Me) — confirm COLM 2025 acceptance + arXiv ID

---

## Body Citation Map (v6 draft)

Every row below mapped against `beyond_recall_v6_draft.md`. Line numbers are anchors for quick check.

| Key | Paper section | Usage excerpt |
|-----|---------|-------|
| REF-01 | §2.4 | "Bartlett (1932) demonstrated that humans remember schemas, not facts..." |
| REF-02 | §2.4 | "Hinton et al. (2015) showed that compressing a large model into a smaller one preserves 'dark knowledge'..." |
| REF-03 | §2.5 | "Zheng et al. (2023) established that LLM judges agree with human judges..." |
| REF-04 | §2.1, §4.3, §4.3.1, §5.8 | "Letta / MemGPT (Packer et al., 2023, arXiv:2310.08560)..." |
| REF-06 | §2.1 | "Mem0 (Chhikara et al., 2025): Hybrid retrieval..." |
| REF-07 | §2.3 | "Twin-2K (Toubia et al., 2025): Behavioral prediction at scale (2,000 participants, 71.83% accuracy)." |
| REF-08 | §2.4 | "Chen, Arditi, Evans et al. (2025) extract persona representations as steerable vectors..." |
| REF-09 | §2.3 and implicit §1.5/§5.10 ("85%+ on LOCOMO/LongMemEval") | "LongMemEval (He et al., ICLR 2025): Long-term memory across 500+ sessions..." |
| REF-10 | §2.3 | "PersonaGym (Jandaghi et al., EMNLP 2025): Tests persona fidelity..." |
| REF-11 | §2.3 | "AlpsBench (Xiao et al., 2026): Evaluates whether explicit memory mechanisms improve preference-aligned and emotionally resonant responses." |
| REF-12 | §2.3 and implicit §1.5/§5.10 | "LoCoMo (Maharana et al., ACL 2024): Conversational memory quality..." |
| REF-13 | §4.7 | "Hong et al. (2025) showed performance degrades as input length increases across 18 frontier models..." |
| REF-14 | §4.7 | "Du et al. (2025) showed even perfect retrieval hurts performance when context length grows..." |
| REF-15 | §2.4, §5.4 | "Jain et al. (2026) find that adding interaction context to LLMs increases rather than reduces hedging..." |
| REF-16 | §2.4 | "Lu et al. (2026) identify hedging as a structural property of assistant models..." |
| REF-17 | §2.4, §5.2 | "Jiang et al. (COLM 2025) find that frontier models achieve only ~50% accuracy on dynamic user profiling tasks..." |

---

## Inconsistencies flagged (do not auto-fix)

1. **Chen author short form.** Paper §2.4 writes "Chen, Arditi, Evans et al." — REF-08's canonical author list is "Runjin Chen; Arditi; Sleight; Evans; Lindsey." Short form drops Sleight and Lindsey. Acceptable citation style but should be consistent across all three occurrences. Preferred in paper: either "Chen et al." or full author list at first mention.

2. **LongMemEval / LOCOMO naming.** Paper writes "LOCOMO/LongMemEval" in §1.5 and §5.10 as shorthand for the recall-benchmark class. LOCOMO is REF-12 (Maharana, LoCoMo); LongMemEval is REF-09 (He). These are two distinct benchmarks, not interchangeable. Consider separating the reference in the paper body (minor, but reviewers may notice).

3. **"Jain et al. (2026)" year.** arXiv:2509.12517 was posted Sep 2025. If the CHI 2026 acceptance is the intended venue anchor, "2026" is defensible; if citing the arXiv version, use 2025. Pick one convention paper-wide.

---

*Last updated: 2026-04-18 (S113). Reference set synced to actual paper-body citations; REF-05/18/19 removed; REF-15 replaced with Jain et al. Review against current paper draft before submission.*
