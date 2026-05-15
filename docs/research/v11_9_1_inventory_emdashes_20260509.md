# v11.9.1 — em-dash inventory

## Em-dash occurrences: 26 line(s), 34 total dashes


### Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization (1)

- L11 (1×): <!-- WALK PROGRESS — INTERNAL TRACKING, REMOVE BEFORE PUBLISH -->

### 2.3 Traceability and reasoning traces (5)

- L245 (2×): > **Response (C2a, excerpt):** *"Based on the behavioral specification, the answer is no, not typically, and not in the way the question assumes. **A2 (Spiritual Integrity Over Social Cost)**^A2 and **A5 (Relational Identity)**^A5 create the relevant dynamic. 
- L256 (1×): > - **A1 — Divine Primacy.** Outcomes are interpreted within a providential logic; the spiritual frame is the master frame.
- L257 (1×): > - **A2 — Spiritual Integrity Over Social Cost.** Conscience and principle outrank social consequence as reasons.
- L258 (1×): > - **A5 — Relational Identity.** Identity is constituted through relationships rather than autonomous selfhood; relational cost is real, not dismissible.
- L259 (1×): > - **P3 — Tension Absorbed, Not Expressed.** Conflicts between principle and relationship are held in place rather than collapsed in either direction.

### 2.4 Cognitive and representational foundations (1)

- L278 (2×): **Chen et al. (2025)** (Chen, Arditi, Sleight, Evans, Lindsey; arXiv:2507.21509) show that the character a model takes on (its "persona") is encoded in specific directions inside the model's internal numeric state — *persona vectors* — and that those direction

### 3.1 Operationalizing representational accuracy via the Behavioral Specification (1)

- L294 (2×): **Representational accuracy is the AI-side property: how faithfully a model's internal model of a specific person captures that person's reasoning patterns.** It is a property of the AI system, not of any specific operationalization. Multiple routes can in pri

### 3.7 Pipeline for the Behavioral Specification (1)

- L749 (1×): **The unified brief.** The compose step integrates the three authored layers (anchors, core, predictions) into a continuous prose synthesis in the third person, similar in length to a short profile of the subject. **The Behavioral Specification served to the r

### 4.1 The cross-subject gradient and its per-question mechanism (8)

- L811 (2×): [^v1-v2-reconciliation]: Two complete batteries exist for each subject in the dataset: an earlier `battery.json` (v1) and the canonical `battery_v2.json` (v2). All headline numbers in §4 — Mean Δ_C4a, gradient, anchor-crossing rates, Wilcoxon test — are comput
- L823 (1×): > **C4a facts + Spec (mean 4.20):** *"This describes **Katsu Rintaro**, who: studied navigation under Dutch officers in Nagasaki (post-1855); served as second-in-command on the Kanrin-maru's trans-Pacific voyage; later became instrumental in negotiating the pe
- L827 (2×): > **What the Spec did.** Without the Spec, the model navigated by surface attribute and lost the referent. With the Spec, it used Fukuzawa's behavioral patterns — particularly his preference for earned over inherited authority — to navigate to the correct subj
- L837 (1×): > The AI gives a confident, fluent answer that gets the direction wrong: it predicts Cortés would accept help. Five judges agree on this — unanimous 2 ("wrong prediction"). The response engages the question and produces a specific prediction, but the predictio
- L839 (2×): > **C4a facts + Spec (mean 4.80):** *"Based on the behavioral specification, when the commander is offered physical assistance during a strenuous activity, the author would expect **Cortes to refuse** the assistance and perform the labor himself — particularly
- L843 (1×): > **What the Spec did.** All facts alone produced a confident, articulate, directionally wrong prediction — the kind of response that looks fine on the page but doesn't match what actually happened. The Spec encoded Cortés' pattern of physical self-reliance an
- L859 (1×): > **What the Spec did.** Where the all-facts dump declined to predict, the Spec generalized from Seacole's documented compassionate-caregiving pattern to the specific untested situation. The pattern was visible in the facts but not explicitly mapped to deliriu
- L893 *[in-table]* (2×): | Franklin | 3.77 | — | 3.37 | 3.65 | −0.13 | — | - |

### 4.1.1 Per-question baseline engagement and the worked rubric example (3)

- L955 *[in-table]* (1×): | Wrong Spec (a Bābur Spec applied to Mary Seacole) | C2c | 1.40 | 1 | *"I appreciate the question, but I need to be direct: I don't have reliable behavioral data on this specific scenario. The specification you've provided describes someone from the 16th-cent
- L958 *[in-table]* (1×): | Spec only (no facts) | C2a | 4.20 | 4 | *"Mary Seacole would likely respond to this situation through the lens of A4 (Proximate Obligation) and A8 (Sympathetic Realism) operating together. She would not correct the patient immediately or harshly. Instead, sh
- L961 (2×): The example traces the *cross-anchor interpretation rule* of §3.3.1 on a single question. C2c (a Bābur Spec wrongly applied to Mary Seacole) explicitly recognizes that the served Spec describes a different person and declines; the response is articulate but th

### 4.1.2 The gradient at the high-baseline end (Franklin reference) (1)

- L971 (1×): **Both Spec-containing conditions score below Franklin's baseline on aggregate, but the Spec still helps on a meaningful subset of questions.** Spec alone drops 0.40 points; the full pipeline (facts + Spec) drops 0.13. The aggregate hides substantial per-quest

### 4.3 Mechanism: Correct Content, Not Format (2)

- L1206 (1×): > > *"I need to be direct: I don't have reliable access to specific statements by Ebers on this question. The behavioral specification you've provided is detailed and rich, but it doesn't contain material where this person directly addresses the relationship b
- L1240 (1×): > > *"The specification you've provided describes someone from the 16th-century Spanish conquest period — the epistemic anchors, loyalty architecture, divine mandate framing, and forward compulsion all point to that historical context. Mary Seacole (1805-1881)

### 4.5 Exploratory case study: Letta stateful-agent (N=3, post-hoc) (1)

- L1535 (1×): > **What explains Letta's lift: named-entity grounding plus content-confidence, not surface-syntactic alignment.** A per-question secondary analysis across all 119 paired questions tested whether Letta's score advantage reflects surface-syntactic alignment wit

### 4.6.4 Statistical-rigor checks on the headline gradient (1)

- L1645 (1×): **Permutation test (10,000 reshuffles of Δ_C4a across subjects, C5 fixed).** Reshuffling the assignment of Spec lifts to subjects produces a null distribution centered at zero (mean ≈ 0.00, SD = 0.29, 95% interval [−0.57, +0.56]). 0 of 10,000 reshuffles produc

### Appendix G. Letta Stateful-Agent: Exploratory Case Study (full) (1)

- L2921 (1×): **Semantic-similarity duplication.** A sentence-embedding analysis (post-hoc, this paper; `scripts/analyze_letta_semantic_duplication.py`, MiniLM-L6-v2, sentence-pair cosine ≥ threshold) shows that the verbatim figure understates the duplication. The self-edit