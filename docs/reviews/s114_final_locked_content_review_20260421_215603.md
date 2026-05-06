# Final Locked-Content Review — 4-provider panel
_Generated: 20260421_215603_
_Locked content: §1 + §2 + §3 + §4.1 + §4.2 (130447 chars)_


---

## Gemini 2.5 Pro

This is a strong draft. The self-critical awareness of limitations is a major asset. The following are consistency flags only.

### 1. Cross-section inconsistencies

-   **Gradient slope:** The linear regression slope for the primary gradient effect is reported differently in two places.
    -   §1.3: slope −0.98 [95% CI −1.30, −0.74]
    -   §4.1: slope −0.96 [95% CI −1.24, −0.67]
-   **Wilcoxon p-value:** The p-value for the C5 vs. C4a comparison is different.
    -   §1.3: p = 0.0063
    -   §4.1: p = 0.007
-   **Author-pilot baseline:** The baseline score for the author pilot is reported with two different values.
    -   §1.4: 1.90
    -   §4.1.2: 1.03
-   **Hamerton compression example:** The key numbers for the Hamerton compression example in the introduction do not match the results table.
    -   §1.3: C2a (spec alone) scores 3.04; C8 (raw corpus) scores 2.32.
    -   §4.2 Table: C2a scores 2.63; C8 scores 2.27.

### 2. Remaining overclaims

None found. The paper is careful to state its limitations, particularly

---

## Mistral Large

Here’s the direct, short audit of the locked content for the requested flags. No invented issues.

---

### **1. Cross-section inconsistencies**
**None found.**
- All hypotheses (H1–H5) are defined in §1.2 and referenced consistently in §4.
- Numbers match across sections (e.g., 14 subjects, 9 low-baseline, 5 mid-baseline).
- Franklin’s baseline (4.10) is treated as a control in §1.3 and §4.1.1 without contradiction.
- The "gradient" framing is consistent: inverse relationship between baseline and spec effect (§1.3, §4.1).

---

### **2. Remaining overclaims**
**One borderline overclaim:**
- **§1.3 (Compression):** *"A compact specification of roughly 5,000–8,000 tokens predicts behavior more accurately than the full raw source it was derived from."*
  - **Issue:** This is true *on average* for the low-baseline slice, but not universally. Ebers (Table 4.2) shows the spec underperforming the raw corpus by 0.64 points. The claim should clarify "on average" or "for most subjects."
  - **Fix:** Add a caveat: *"...more accurately than the full raw source for most subjects, though the gap varies by corpus size and density."*

**No other overclaims.**
- All limitations are disclosed (e.g., LLM-as-judge circularity in §6, extrapolation to living users in §1.4).
- Claims about "category-level change" (§1.3) are supported by anchor-crossing data (§4.1).

---

### **3. Voice violations**
**Three instances:**
1. **§1.3 (Mechanism):** *"The specification beats the baseline..."*
   - **Issue:** "Beats" is GTM-style. Replace with *"outperforms"* or *"improves over"*.
2. **§4.1 (Example B):** *"The specification flipped the prediction to match the ground truth."*
   - **Issue:** "Flipped" is informal. Replace with *"corrected"* or *"adjusted"*.
3. **§4.2.1:** *"The metric is not picking up trivial +0.02-per-question gains..."*
   - **Issue:** "Picking up" is conversational. Replace with *"capturing"*.

**No em-dashes in prose** (only in tables/code blocks).
**No reader-addressing in methodology** (e.g., "you" or "we" in §3).

---

### **4. Unfulfilled promises**
**None.**
- All forward references deliver:
  - §4.1 tests H1/H2 (gradient).
  - §4.2 tests H5 (compression).
  - §4.3 tests H3 (mechanism).
  - §4.4 tests H4 (composition).
- Letta’s stateful-agent path is addressed in §4.3.1 (not §4.4, but cross-referenced).

---

### **5. Peer-review embarrassment**
**One risk:**
- **§1.3 (Mechanism):** *"The 60.6% explicit mismatch detection rate... confirms the core finding."*
  - **Issue:** The 60.6% is a *lower bound* (models may detect mismatches implicitly). Overstating it as definitive could draw scrutiny.
  - **Fix:** Soften to: *"The 60.6% explicit detection rate suggests the model infers mismatches from content, not surface cues."*

**No other red flags.**
- The abstention rubric issue (§3.7.6) is disclosed and mitigated by reporting both 5-judge and 7-judge aggregates.
- The length-driven baseline inflation (§3.7.6) is flagged as a bias *in favor of the null hypothesis* (i.e., the true effect is likely larger).

---

### **Summary**
- **Fix:** The compression overclaim (§1.3) and voice violations (§1.3, §4.1, §4.2.1).
- **Disclose:** The 60.6% mismatch detection rate as a lower bound.
- **No structural issues.** The paper’s claims are tightly scoped to the evidence.

---

## GPT-5.4

A few things worth fixing:

1. **Hypothesis count mismatch.**
   - §1.2 says “tests four claims” but lists **H1–H5**.
   - §4.1 introduces **H2a** as “introduced here,” but §1.2 says hypotheses map directly to §4 and does not mention H2a. Fine as corollary, but it breaks the “predefined hypotheses” framing.

2. **Section-reference inconsistencies / unfulfilled promises.**
   - §1.2 maps **H1 and H2 to “§4.1 The Gradient”**, but the actual section title is **“§4.1 The Cross-Subject Gradient.”**
   - §1.2 says the formal proposal and failure-mode analysis for the secondary metric are in **§4.2.1**. That is delivered.
   - §1.2 says Letta separate test is in **§4.3.1**; in the current §4 outline, **§4.3 is Mechanism** and **§4.7 is Architectural Convergence**. That forward reference is now wrong.
   - §1.4 points to **§1.5** for behavioral alignment, which is delivered.
   - Multiple places point to **§8 Future Work**; current front matter says only up to §4.2 is locked, so not a problem if §8 will exist, but make sure it does.

3. **Numerical inconsistency on the main effect.**
   - §1.3 primary result says low-baseline mean gain is **+1.04** points.
   - §4.1 reports low-baseline mean Δ_C4a as **+0.89**.
   - These cannot both stand.

4. **Franklin framing inconsistency.**
   - §1.3 mechanism says Franklin-for-all wrong-spec control was used and reports **Δ −0.16**.
   - §3.5 says Franklin-for-all was a prior iteration and **is not reported in the main results**.
   - If §1.3 keeps that number, §3.5 is false.

5. **Baseline / subject maximum inconsistency.**
   - §1.4 says “the two subjects where the specification did not help were the two with the highest baselines in the study.”
   - In §4.1 table, non-help cases are **Zitkala-Sa** and **Equiano** for C4a, while **Augustine** is higher-baseline than Zitkala-Sa and still slightly positive. So this claim is inaccurate.

6. **Judge-panel inconsistency.**
   - §1.2/§1.3 says “7-judge panel” and “5-judge primary panel,” fine.
   - §3.1 still defines representational accuracy as averaged across **seven judges**. That conflicts with the locked primary outcome being 5-judge.

7. **Section-number drift.**
   - §3.6 says hedging-rate shift is in **§4.4**.
   - In current §4 outline, **§4.4 is Memory-System Composition**; hedging discussion appears earlier in intro/mechanism language, not clearly §4.4.

8. **Overclaim / peer-review risk.**
   - “**Nearly every real AI user is low-baseline by construction**” and especially “**For a typical living user ... baseline is at or below 1.0 by construction**” are too strong from this evidence. You only have one living-user pilot and historical extrapolation.
   - “**If the specification was uniformly beneficial for the lowest-baseline historical figures we could test, it should be at least as beneficial for the typical real AI user**” is the most review-exposed sentence here.
   - “**Language models optimize for the median. By construction, a model tuned for the average fails every individual on the distribution**” is rhetorically strong and easy to attack as false/oversimplified.

9. **Voice violations.**
   - Em dash in prose appears throughout (for example, “The inverse is also true and important. A perfectly behaviorally-aligned agent...” is fine, but there are many actual **—** uses in prose, e.g. §4.1 examples/headings and elsewhere). Your style rule says flag them.
   - Reader-addressing in methods: §1.2 says “**so the reader can track it**...” Minor but it is there.

10. **One embarrassing claim under review.**
   - “**This is an informative positive finding, not a specification defect**” about Keckley Q21 is too defensive. Reviewers will read it as post hoc reframing of a failure under the chosen rubric. Better to state it as an interpretation, not a settled conclusion.

---

## Claude Opus 4.6

Here are the issues I found:

---

**Cross-section inconsistencies**

1. **Regression slope mismatch.** §1.3 reports slope −0.98 [95% CI −1.30, −0.74]. §4.1 reports slope −0.96 [95% CI −1.24, −0.67]. These are supposed to be the same regression. One of them is wrong.

2. **Wilcoxon p-values mismatch.** §1.3 reports C5 vs. C4a p = 0.0063. §4.1 reports C5 vs. C4a W = 11, p = 0.007. Same test, different p-values. §4.1 also adds a C5 vs. C2a Wilcoxon (W = 10, p = 0.005) not mentioned in §1.3.

3. **Low-baseline mean lift mismatch.** §1.3 says "+1.04 points" for the 9 low-baseline subjects. §4.1 says "+0.89 points." Both refer to the same C4a − C5 delta on the same 9 subjects. One is wrong. (The per-subject table in §4.1 is consistent with +0.89, so §1.3's +1.04 appears to be the stale number.)

4. **Hamerton spec-alone token count.** §1.3 Compression says "C2a, 7,300 tokens" and scores 3.04. §4.1 per-subject table shows Hamerton C2a = 2.63. §4.2 per-subject table also shows Hamerton C2a = 2.63. The 3.04 in §1.3 does not match either. (The §1.3 Compression paragraph appears to be from an earlier draft or a different judge aggregate.)

5. **Hamerton C8 score.** §1.3 says raw corpus scores 2.32. §4.2 table says 2.27. Same subject, same condition.

6. **Hamerton C4a score.** §1.3 says C4a = 3.22. §4.1 table says 2.77. §4.2 table says 2.77.

7. **Franklin baseline.** §1.2 says "4.10." §3.2 says "4.10." §4.1 per-subject table says "3.77." §4.1.1 says "3.77." The Introduction and Study Design appear to use a different aggregate (possibly 7-judge) than Results (5-judge primary). If so, the Introduction should use the 5-judge number or explicitly flag the aggregate, since §4 is locked to the 5-judge primary.

8. **Hypothesis numbering.** §1.2 lists H1–H5 (five hypotheses) but the text says "four claims" right before the list. Should be "five claims."

---

**Remaining overclaims**

9. **"No current benchmark is built to measure it" (§1.1).** Twin-2K (§2.3) is acknowledged as measuring behavioral prediction. The claim in §1.1 should be qualified or the distinction sharpened.

10. **Living-user pilot framing.** §1.4 reports a pilot with "N=10, single judge" and baseline 1.90. §4.1.2 reports a full 40-question, 5-judge pilot on the same author with baseline 1.03. These appear to be different runs on different data, but §1.4 does not acknowledge the §4.1.2 pilot exists, and the two baselines (1.90 vs. 1.03) are quite different. A reviewer will ask whether the §1.4 number was superseded.

11. **"9 of 9 low-baseline subjects in the native configuration" for Zep (§1.3).** This claim about the native configuration is not yet testable from the locked sections. If §4.4 doesn't deliver this exact number, it's an unfulfilled promise.

---

**Voice violations**

12. No em-dashes in prose detected. No GTM verbs detected. No reader-addressing in methodology sections detected. Clean on voice.

---

**Unfulfilled promises / forward references**

13. **§1.2 maps H3 to §4.3, H4 to §4.4.** These sections are not yet locked. Fine as long as they deliver, but the §1.3 Mechanism and Additivity summaries are quite detailed — if §4.3/§4.4 present different numbers, the inconsistency will be hard to fix with §1 locked.

14. **§2.5 "LLM-as-judge"** is listed as a section header with no content. Presumably forthcoming, but it's in the "locked" block.

15. **§4.1 references "§4.1.3 explores two subjects where it hurts."** §4.1.3 is not present in the locked content. Needs to exist.

16. **§3.7.6 and the LLM-as-judge disclosure both reference "§8 Future Work."** The section map in §4 lists subsections up to §4.8 but the paper structure implies §7 and §8 exist. Just flagging that these forward references need to land.

---

**Embarrassment risk under peer review**

17. **The §4.1.2 living-user pilot is N=1 with the paper's own author as subject.** The wrong-spec control (Franklin's spec) lifts +1.56 vs. correct spec +1.84 — a gap of only 0.28 points. On historical subjects, the wrong-spec mean delta was +0.28 (§1.3), meaning the wrong spec on the author performs comparably to the wrong spec on historical subjects. But the text explains this away as "Franklin's specification happens to share some values-based scaffolding." A reviewer will note that the author chose their own data, generated their own spec, and the wrong-spec control barely underperforms the correct spec. This is the single most reviewable vulnerability in the locked content. The current disclosure is adequate but the framing could be tightened — the 0.28-point gap is not clearly distinguishable from noise at N=40 with a single subject.

18. **Twin-2K preliminary run.** §2.3 reports "71.83% accuracy at 18:1 compression (p=0.008)" on N=100 from Twin-2K. This is dropped in without methodology, judge specification, or condition details, and the p-value is unexplained (p-value of what test?). A reviewer will flag this as an ungrounded claim in Related Work.

---

**Summary of critical fixes needed before next section:**

- Reconcile the slope, CI, p-values, and mean-lift numbers between §1.3 and §4.1 (items 1–3). These are the paper's headline statistics.
- Reconcile all Hamerton numbers between §1.3 and §4.1/§4.2 (items 4–6).
- Reconcile Franklin baseline between Introduction/§3 and §4 (item 7).
- Fix "four claims" → "five claims" (item 8).
- Fill or remove the §2.5 stub (item 14).