# Beyond Recall — Deterministic Reference Table

**Purpose:** Single source of truth for all citations in the paper. Every reference keyed by `[REF-XX]`. Body uses these keys. Do not cite a paper that does not appear here.

**Verification status:**
- `VERIFIED` — arXiv ID or DOI confirmed against public record  
- `PROBABLE` — consistent with known literature; full ID not independently confirmed  
- `NEEDS CHECK` — incomplete or unconfirmed; requires human lookup before submission  

---

## Core References

| Key | Authors | Title | Venue | Year | ID / DOI | Status |
|-----|---------|-------|-------|------|----------|--------|
| REF-01 | Bartlett, F. C. | Remembering: A Study in Experimental and Social Psychology | Cambridge University Press | 1932 | ISBN: 978-0521483568 | **VERIFIED** |
| REF-02 | Hinton, G.; Vinyals, O.; Dean, J. | Distilling the Knowledge in a Neural Network | NeurIPS Workshop | 2015 | arXiv:1503.02531 | **VERIFIED** |
| REF-03 | Zheng, L. et al. | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | NeurIPS | 2023 | arXiv:2306.05685 | **VERIFIED** |
| REF-04 | Packer, C. et al. | MemGPT: Towards LLMs as Operating Systems | arXiv | 2023 | arXiv:2310.08560 | **VERIFIED** |
| REF-05 | Betley, J. et al. | Emergent Misalignment: Narrow Finetuning Can Produce Broadly Misaligned LLMs | Nature (preprint) | 2025 | arXiv:2502.17424 | **PROBABLE** |
| REF-06 | Chhikara, P. et al. | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | arXiv | 2025 | arXiv:2504.19413 | **PROBABLE** |
| REF-07 | Toubia, O. et al. | Twin-2K: Behavioral Prediction at Scale | arXiv | 2025 | arXiv:2505.17479 | **PROBABLE** |
| REF-08 | Chen, R. (Runjin); Arditi, A.; Sleight, H.; Evans, O.; Lindsey, J. | Persona Vectors: Monitoring and Controlling Character Traits in Language Models | arXiv | 2025 | arXiv:2507.21509 | **VERIFIED** — title corrected; lead author Runjin Chen (not "Y. Chen") |
| REF-09 | LongMemEval (He, D. et al.) | LongMemEval: Benchmarking Long-Term Memory Systems | ICLR | 2025 | arXiv:2410.10813 | **PROBABLE** |
| REF-10 | PersonaGym (Jandaghi, P. et al.) | PersonaGym: Evaluating Persona Agents and LLMs | EMNLP | 2025 | arXiv:2407.18416 | **PROBABLE** |
| REF-11 | Xiao, J. et al. (11 authors) | AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment | arXiv | 2026 | arXiv:2603.26680 | **VERIFIED** — title corrected; "Alignment Beyond Recall" was invented subtitle |
| REF-12 | LoCoMo (Maharana, A. et al.) | LoCoMo: Evaluating Long Context Memory in Dialogue | ACL | 2024 | arXiv:2402.17753 | **PROBABLE** |
| REF-13 | Hong, K. (Kelly); Troynikov, A.; Huber, J. | Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Technical Report | 2025 | trychroma.com/research/context-rot | **VERIFIED** — no arXiv ID (technical report); lead author Kelly Hong (not "J. Hong") |
| REF-14 | Du, Y. (Yufeng) et al. | Context Length Alone Hurts LLM Performance Despite Perfect Retrieval | EMNLP | 2025 | arXiv:2510.05381 | **VERIFIED** — title matches; lead author Yufeng Du (not "Li, N."); venue EMNLP 2025 |
| REF-15 | — | CAUSM: Sycophancy in LLMs is Driven by User Memory | ICLR | 2025 | — | **NOT FOUND** — no paper with this title/acronym at ICLR 2025 verified. Closest: Jain et al., "Interaction Context Often Increases Sycophancy in LLMs," arXiv:2509.12517, CHI 2026 — different title/venue. **Remove from paper or replace.** |
| REF-16 | Lu, C. (Christina); Gallagher, J.; Michala, J.; Fish, K.; Lindsey, J. | The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models | arXiv | 2026 | arXiv:2601.10387 | **VERIFIED** — title corrected; lead author Christina Lu (not "K. Lu") |
| REF-17 | Jiang, B.; Hao, Z.; Cho, Y.-M.; et al. | Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale | COLM | 2025 | arXiv:2504.14225 | **VERIFIED** — actual title different; COLM 2025 confirmed; "50% accuracy" finding is accurate |
| REF-18 | Shi, Y. (Yunxiao); Xu, W.; Zhang, Z.; Zi, X.; Wu, Q.; Xu, M. | PersonaX: A Recommendation Agent Oriented User Modeling Framework for Long Behavior Sequence | arXiv (ACL venue unconfirmed) | 2025 | arXiv:2503.02398 | **PARTIAL** — title corrected; ACL 2025 venue not confirmed in arXiv record |
| REF-19 | — | Modeling Social Cognition as Bayesian Inverse Planning | Cognitive Science | 2024 | — | **NOT FOUND** — no paper matching author "Stacy" + this title + venue verified. **Remove from paper.** |

---

## Verification Checklist (Before ArXiv Submission)

- [ ] **REF-08** (Chen, Persona Vectors) — search arXiv:2507.21509, confirm title matches
- [ ] **REF-11** (AlpsBench) — search arXiv:2603.26680, confirm authors/title
- [ ] **REF-13** (Context Rot, Hong) — locate Chroma Research blog/paper, confirm URL and author list
- [ ] **REF-14** (Li, context length) — search arXiv:2510.05381, confirm title matches
- [ ] **REF-15** (Jain, CAUSM) — search "CAUSM sycophancy user memory ICLR 2025", find arXiv ID
- [ ] **REF-16** (Lu, Assistant Axis) — search arXiv:2601.10387, confirm title/authors
- [ ] **REF-17** (PersonaMem) — search "PersonaMem COLM 2025 user modeling", find arXiv ID and authors
- [ ] **REF-18** (PersonaX) — search "PersonaX ACL 2025 behavioral profiling", find arXiv ID and authors
- [ ] **REF-19** (Stacy) — search "social cognition Bayesian inverse planning 2024 Cognitive Science", confirm author name

---

## Body Citation Map

Where each reference should appear in the paper:

| Key | Section | Usage |
|-----|---------|-------|
| REF-01 | 2. Related Work | "Bartlett (1932) demonstrated that humans remember schemas..." |
| REF-02 | 2. Related Work | "Hinton et al. (2015) showed that compressing a large model..." |
| REF-03 | 2. Related Work | "Zheng et al. (2023) established that LLM judges agree..." |
| REF-04 | 2. Related Work | "Letta, formerly MemGPT (Packer et al., 2023)..." |
| REF-05 | 5.6 Scope | "Betley et al. (2025) demonstrated that fine-tuning on narrow data produces behavioral shifts..." |
| REF-06 | 2. Related Work | "Mem0 (Chhikara et al., 2025) provides flat embedding retrieval..." |
| REF-07 | 2. Related Work | "Twin-2K (Toubia et al., 2025) tests behavioral prediction at scale..." |
| REF-08 | 2. Related Work | "Chen et al. (2025) extract persona representations as steerable vectors..." |
| REF-09 | 1. Introduction, 2. Related Work | "LongMemEval (ICLR 2025) tests recall..." |
| REF-10 | 2. Related Work | "PersonaGym (EMNLP 2025) tests persona fidelity..." |
| REF-11 | 2. Related Work | "AlpsBench (Xiao et al., 2026) demonstrates that recall does not equal alignment..." |
| REF-12 | 2. Related Work | "LoCoMo (ACL 2024) evaluates conversational memory..." |
| REF-13 | 4.3 Known Figure | "Hong et al. (2025) demonstrated that LLM performance degrades with context length..." |
| REF-14 | 4.3 Known Figure | "Li et al. (2025) showed that context length alone hurts performance..." |
| REF-15 | 5.5 When To Use | "Jain et al. (CAUSM, 2025) found that sycophancy is driven by the model's user memory..." |
| REF-16 | 5.5 When To Use | "Lu et al. (2026) map the helpfulness/harmlessness tradeoff axis..." |
| REF-17 | 5.1 Specification as Tool | "PersonaMem (COLM 2025) found that frontier models fail at 50% of user modeling tasks..." |
| REF-18 | 5.3 Facts Do Not Carry Significance | "PersonaX (ACL 2025) propose decoupled behavioral profiling..." |
| REF-19 | 1. Introduction or 3.3.1 | "Stacy et al. (2024) model social cognition as Bayesian inverse planning..." |

---

*Last updated: 2026-04-13. Review against current paper draft before submission.*
