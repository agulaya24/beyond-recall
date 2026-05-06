# §2.3 "Memory and personalization benchmarks" — Primary-Source Verification

**Purpose.** Pre-launch verification of every benchmark citation in v6 §2.3 of *Beyond Recall* against primary sources.
**Date.** 2026-04-17.
**Scope.** Five benchmarks: LongMemEval, PersonaGym, AlpsBench, Twin-2K, LoCoMo.

---

## 0. One-sentence summary for the lead author

Two citations need author correction (**LongMemEval is Wu et al., not He et al.**; **AlpsBench is Xiao et al. 2026 — verified**), one characterization needs softening (**LongMemEval's five dimensions are not "all focused on recall"** — the paper's own framing includes multi-session reasoning, temporal reasoning, knowledge updates, and abstention, which go beyond simple recall), and one number needs correction (**Twin-2K headline accuracy is 71.72%, not 71.83%**).

---

## 1. Verification table

| # | Benchmark | v6 cites | Primary-source authors | Venue + year | arXiv/DOI | Status |
|---|---|---|---|---|---|---|
| 1 | LongMemEval | He et al., ICLR 2025 | **Di Wu**, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, Dong Yu | ICLR 2025 | arXiv:2410.10813; OpenReview: pZiyCaVuti | **NEEDS CORRECTION** — first author is Wu, not He |
| 2 | PersonaGym | Jandaghi et al., EMNLP 2025 | **Vinay Samuel**, Henry Peng Zou, Yue Zhou, Shreyas Chaudhari, Ashwin Kalyan, Tanmay Rajpurohit, Ameet Deshpande, Karthik R. Narasimhan, Vishvak Murahari | Findings of EMNLP 2025 | arXiv:2407.18416; aclanthology.org/2025.findings-emnlp.368 | **NEEDS CORRECTION** — first author is Samuel, not Jandaghi. (Jandaghi et al. is a *different* persona-consistency paper — possibly the author is conflating them.) |
| 3 | AlpsBench | Xiao et al., 2026 | **Jianfei Xiao**, Xiang Yu, Chengbing Wang, Wuqiang Zheng, Xinyu Lin, Kaining Liu, Hongxun Ding, Yang Zhang, Wenjie Wang, Fuli Feng, Xiangnan He | arXiv preprint, 2026-03-09 | arXiv:2603.26680 | **VERIFIED** — first author and year correct. No conference venue yet (preprint). |
| 4 | Twin-2K-500 | Toubia et al., 2025 | **Olivier Toubia**, George Z. Gui, Tianyi Peng, Daniel J. Merlau, Ang Li, Haozhe Chen | arXiv preprint 2025-05-23; also Marketing Science (INFORMS) database report (DOI: 10.1287/mksc.2025.0262) | arXiv:2505.17479 | **VERIFIED AUTHORS/YEAR**; number needs correction |
| 5 | LoCoMo | Maharana et al., ACL 2024 | **Adyasha Maharana**, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, Yuwei Fang | ACL 2024 (Vol. 1 Long Papers) | arXiv:2402.17753; aclanthology.org/2024.acl-long.747 | **VERIFIED** |

---

## 2. Characterization check — per benchmark

### 2.1 LongMemEval — v6 says "500+ sessions and 5 capability dimensions, all focused on recall."

**Primary source (arXiv:2410.10813, ICLR 2025):**
- "500 sessions" is the configuration of **one** of two standard settings — **LongMemEvalM** (~1.5M tokens). The smaller setting, **LongMemEvalS**, is ~115k tokens. Not every problem has 500+ sessions.
- Five core abilities as named by the paper:
  1. Information extraction
  2. Multi-session reasoning (*"synthesize the information across multiple history sessions… aggregation and comparison"*)
  3. Temporal reasoning (*"awareness of the temporal aspects of user information"*)
  4. Knowledge updates (recognizing changes over time)
  5. Abstention (recognizing when information is unavailable)

**Verdict: CHARACTERIZATION IS OVERSTATED.**
- "500+ sessions" is only the M setting, not the benchmark as a whole.
- "All focused on recall" is **not defensible** from the paper. Multi-session reasoning, knowledge updates, and temporal reasoning are explicitly reasoning-beyond-recall categories. Abstention tests calibration/refusal. Only *information extraction* is pure recall.

**Suggested rewrite:**
> "LongMemEval (Wu et al., ICLR 2025) tests long-term memory across chat histories up to 500 sessions (~1.5M tokens) along five dimensions — information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. All five dimensions are evaluated as question-answering over a grounded history; the benchmark does not test behavioral prediction of held-out responses."

### 2.2 PersonaGym — v6 says "tests persona fidelity… consistency of persona presentation, not prediction of held-out behavior."

**Primary source (arXiv:2407.18416, Findings of EMNLP 2025):**
- PersonaGym is "the first dynamic evaluation framework for persona agents," introducing PersonaScore, "a human-aligned automatic metric grounded in decision theory."
- Evaluates 10 LLMs across 200 personas and 10,000 questions.
- Measures whether the LLM acts consistent with an assigned persona, not whether it predicts a real person's responses.

**Verdict: CHARACTERIZATION IS ACCURATE** — but **the author attribution is wrong.** The paper is Samuel et al., not Jandaghi et al. There is a separate Jandaghi paper on persona-consistent LLMs (arXiv:2312.10007, "Faithful Persona-based Conversational Dataset Generation with LLMs"); these two papers are distinct.

**Suggested rewrite:** keep the characterization; change the author-year to **(Samuel et al., Findings of EMNLP 2025)**.

### 2.3 AlpsBench — v6 says "Xiao et al., 2026 … their central finding, that explicit memory mechanisms improve recall but do not inherently guarantee more preference-aligned or emotionally resonant responses, is independently arrived at and complementary to ours."

**Primary source (arXiv:2603.26680, submitted 2026-03-09):**
- Authors: **Jianfei Xiao** et al. (11 authors; full list above). ✓
- Benchmark description: "AlpsBench comprises 2,500 long-term interaction sequences curated from WildChat, paired with human-verified structured memories that encapsulate both explicit and implicit personalization signals." Four tasks: personalized information extraction, updating, retrieval, utilization.
- **Central finding verbatim:** *"while explicit memory mechanisms improve recall, they do not inherently guarantee more preference-aligned or emotionally resonant responses."*

**Verdict: VERIFIED.** Author, year, and characterization are all accurate. The quote in the v6 paraphrase is faithful to the primary source. AlpsBench is a real 2026 arXiv preprint (no conference venue yet) — the v6 paragraph can stand as written.

### 2.4 Twin-2K — v6 says "Behavioral prediction at scale (2,000 participants, 71.83% accuracy). Does not test the effect of compression or the role of interpretive structure."

**Primary source (arXiv:2505.17479):**
- 2,058 participants, 500 questions per person, US sample, four waves. ✓
- Headline accuracy is **71.72%** (text-persona approach with GPT-4.1-mini on holdout). Ratio to test-retest is 87.67%; human test-retest is 81.72%.
- Table 2 in the paper reports 12 methodology variants ranging 67.88% to 71.92%.
- The benchmark is a digital-twin *prediction* benchmark — it is genuinely behavioral prediction, not recall. This is consistent with v6's framing.
- The paper does not evaluate any compression regime on persona material. ✓

**Verdict: NUMBER IS OFF BY 0.11 PERCENTAGE POINTS.** "71.83%" does not appear in the paper; the actual headline is **71.72%**. The characterization otherwise is accurate.

**Possible origin of 71.83%:** Earlier session notes in `MEMORY.md` list "71.83% accuracy at 18:1 compression, p=0.008" — but the "71.83%" there does not appear in Toubia et al.'s paper under any subset breakdown I could find, and Toubia et al. do not test compression. This may be a separate internal replication number that has drifted into the paper. **Recommendation:** change to **71.72%** and cite arXiv:2505.17479 directly, OR if 71.83% comes from an internal replication, move that to Methods/Results and do not attribute it to Toubia et al.

**Suggested rewrite:**
> "Twin-2K-500 (Toubia et al., 2025) tests behavioral prediction at scale — 2,058 participants, ~500 questions each — reaching 71.72% accuracy on holdout items (GPT-4.1-mini, text-persona). It does not test the effect of compression or the role of interpretive structure on prediction."

### 2.5 LoCoMo — v6 says "Conversational memory quality; does not evaluate behavioral reasoning."

**Primary source (arXiv:2402.17753, ACL 2024):**
- "Evaluating Very Long-Term Conversational Memory of LLM Agents."
- Dataset: long-term conversations averaging 300 turns, 9K tokens, up to 35 sessions.
- Tasks: question answering, event summarization, multi-modal dialogue generation.
- Evaluation is grounded in the conversation transcript. There is no behavioral-prediction task (predicting held-out responses by the same person).

**Verdict: ACCURATE.** Characterization is correct. Authors and venue are correct.

---

## 3. Corrections needed in v6 §2.3 (ordered by severity)

1. **[AUTHOR ERROR] LongMemEval: change "He et al." → "Wu et al."** First author is Di Wu.
2. **[AUTHOR ERROR] PersonaGym: change "Jandaghi et al." → "Samuel et al."** First author is Vinay Samuel. Jandaghi et al. is a *different* persona paper (arXiv:2312.10007) and is not the one described in v6.
3. **[OVERSTATEMENT] LongMemEval "all focused on recall"** — not defensible. Multi-session reasoning, temporal reasoning, knowledge updates, and abstention go beyond pure recall. Soften to "all evaluated as question-answering over a grounded history; no behavioral-prediction task."
4. **[OVERSTATEMENT] LongMemEval "500+ sessions"** — only true for LongMemEvalM. Accurate phrasing: "up to 500 sessions (~1.5M tokens) in the M setting."
5. **[NUMBER] Twin-2K "71.83% accuracy"** — paper reports **71.72%** headline on arXiv v1. 71.83% does not appear in the paper. Change to 71.72% or flag as internal replication.
6. **[VENUE CAVEAT] AlpsBench "2026"** — verified correct. No conference venue yet; cite as "arXiv preprint 2026" to be precise.
7. **[VERIFIED — no change] PersonaGym characterization.** Keep.
8. **[VERIFIED — no change] LoCoMo characterization.** Keep.

---

## 4. Answers to the three specific yes/no items

- **Is AlpsBench a real benchmark in 2026?** YES. arXiv:2603.26680, submitted 2026-03-09. First author Jianfei Xiao. Characterization in v6 (including the "preference-aligned or emotionally resonant" quote) is faithful to the abstract.
- **Is Twin-2K's 71.83% accuracy number correct?** NO. Paper's headline is **71.72%**. 71.83% is not in the paper; may be an internal replication that drifted into the citation.
- **Are all five benchmark citations correct on authors?** NO. LongMemEval is **Wu et al.**, not He et al. PersonaGym is **Samuel et al.**, not Jandaghi et al.

---

## 5. Sources

- [1] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., Yu, D. "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory." ICLR 2025. arXiv:2410.10813. <https://arxiv.org/abs/2410.10813>
- [2] Samuel, V., Zou, H. P., Zhou, Y., Chaudhari, S., Kalyan, A., Rajpurohit, T., Deshpande, A., Narasimhan, K. R., Murahari, V. "PersonaGym: Evaluating Persona Agents and LLMs." Findings of EMNLP 2025. arXiv:2407.18416. <https://arxiv.org/abs/2407.18416>
- [3] Xiao, J., Yu, X., Wang, C., Zheng, W., Lin, X., Liu, K., Ding, H., Zhang, Y., Wang, W., Feng, F., He, X. "AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment." arXiv:2603.26680, 2026-03-09. <https://arxiv.org/abs/2603.26680>
- [4] Toubia, O., Gui, G. Z., Peng, T., Merlau, D. J., Li, A., Chen, H. "Twin-2K-500: A dataset for building digital twins of over 2,000 people based on their answers to over 500 questions." arXiv:2505.17479, 2025-05-23. Also Marketing Science database report, DOI: 10.1287/mksc.2025.0262. <https://arxiv.org/abs/2505.17479>
- [5] Maharana, A., Lee, D.-H., Tulyakov, S., Bansal, M., Barbieri, F., Fang, Y. "Evaluating Very Long-Term Conversational Memory of LLM Agents." ACL 2024 (Vol. 1 Long Papers). arXiv:2402.17753. <https://arxiv.org/abs/2402.17753>, <https://aclanthology.org/2024.acl-long.747/>

---

## 6. Verification limits

- All findings above come from arXiv abstracts + v1 HTML renderings accessed via WebFetch on 2026-04-17. No full PDFs read end-to-end.
- For LongMemEval and Twin-2K, the characterization disputes are grounded in primary-source framing as surfaced through the paper's HTML; if the lead author wants a §-level verbatim quote, a PDF pass is cheap.
- PersonaGym author attribution is firm (verified against ACL Anthology PDF title page snippet + arXiv authors field + GitHub repo README). The "Jandaghi et al." attribution in v6 is almost certainly a cross-wiring with arXiv:2312.10007 ("Faithful Persona-based Conversational Dataset Generation with LLMs" — first author Pegah Jandaghi), which is persona-consistency work but is not PersonaGym.
