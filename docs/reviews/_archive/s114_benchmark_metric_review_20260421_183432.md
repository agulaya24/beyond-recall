# Benchmark Metric Review — 6-provider panel
_Generated: 20260421_183432_


---

## Gemini 2.5 Flash

Here's my direct advice regarding the proposed metric:

## 1. Is per-question-improvement rate a good candidate benchmark metric for AI personalization? What are its strengths and weaknesses?

**Verdict: No, not as a primary standalone benchmark. It has significant weaknesses that outweigh its strengths for this purpose.**

**Strengths (as proposed by author, and my assessment):**

*   **Direct Interpretability:** "70% of questions improved" is indeed easy for a broad audience to understand. This is its strongest point for communication.
*   **Comparability (claimed):** If studies use vastly different scoring scales (e.g., 1-5 vs. 1-100), a mean score delta is hard to compare directly. An improvement *rate* might be more comparable, assuming the definition of "improvement" (any positive change) is consistent.
*   **Generalizability:** It's a high-level metric that doesn't depend on specific context representations, response models, or populations, making it broadly applicable.
*   **Focus on Breadth of Impact:** It directly answers "how often does personalization help?" which is a valid question about the *reach* of a personalization strategy.

**Weaknesses (critical for a benchmark):**

*   **Ignores Magnitude of Improvement/Worsening:** This is the *fatal flaw* for a primary benchmark. A question improving from a score of 1 to 2 (trivial) counts the same as one improving from 1 to 5 (significant). Similarly, a minor worsening counts the same as a catastrophic failure. This can be highly misleading about the actual utility or harm of a personalization system.
*   **Susceptibility to Gaming:** A system could be optimized to achieve many tiny, insignificant improvements to boost this metric, while potentially ignoring or even worsening performance on harder, more impactful questions.
*   **Loss of Information:** Reducing each question's outcome to a binary (improved/not improved) discards all the rich, granular information from the scoring rubric and the actual scores.
*   **Sensitivity to Baseline Quality:** The "improvement" is always relative to a no-context baseline. If the baseline is already very good, achieving high improvement rates is harder. If the baseline is poor, even trivial personalization might show a high improvement rate. This makes cross-domain comparisons difficult without deep context.
*   **Statistical Ambiguity of "Improvement":** For a question to "improve," the 5-judge primary mean needs to increase. If this difference is small, is it statistically significant? The metric doesn't inherently account for the statistical significance of the per-question change, potentially counting noisy fluctuations as true improvements.
*   **Doesn't Reflect Absolute Quality:** It only tells you about *relative change*, not the overall quality of the predictions. A system could have a high improvement rate but still produce generally poor responses.
*   **Robustness to Judge Noise (rebuttal):** While the author claims robustness, if the true difference between conditions for a question is small, judge noise could easily flip the "improved/worsened" classification for that question, making the aggregated rate itself noisy.

## 2. Are there comparable established metrics in LLM evaluation, information retrieval, or decision-support literature that this parallels or contradicts?

**Parallels:**

*   **Win Rate / Preference Judgments (LLM Evaluation):** This is the closest parallel. In human preference evaluations (e.g., for RLHF), models are often compared head-to-head, and a "win rate" (Model A preferred over Model B X% of the time) is reported. This shares the binary outcome aggregation across instances. The "head-to-head at question level" data you provided is exactly this.
*   **Accuracy (Binary Classification):** If you conceptualize "improvement" as a "correct" outcome of personalization, it's loosely analogous to accuracy.

**Contradicts / Differs Significantly:**

*   **Any Magnitude-Based Metric:** This metric fundamentally contradicts the principles behind almost all established quantitative metrics in these fields that aim to capture *how much* better or worse something is.
    *   **Mean Average Precision (MAP), Normalized Discounted Cumulative Gain (NDCG) (Information Retrieval):** These metrics explicitly account for the *position* and *relevance score* of items, emphasizing higher-ranked, more relevant items. They care about magnitude and order.
    *   **RMSE, MAE (Regression/Prediction):** These are all about the *magnitude* of error.
    *   **BLEU, ROUGE, METEOR (NLP Generation):** These are score-based metrics, focusing on the degree of similarity or quality, not just binary improvement.
    *   **Effect Sizes (e.g., Cohen's d):** These quantify the *magnitude* of a difference, which this metric explicitly ignores.
    *   **Statistical Significance Testing (p-values):** While underlying data might be tested, the metric itself is purely descriptive and doesn't convey statistical significance of the overall rate or individual improvements.

## 3. Should the paper explicitly propose this as a benchmark, or present it as an internal reporting metric only?

**Verdict: Present it as an internal reporting metric only, and *very cautiously* suggest it as a *complementary diagnostic* in future work, with strong, explicit caveats about its limitations.**

It is too flawed to be a primary benchmark. Its interpretability is a strength for communicating *one aspect* of performance (breadth of impact), but it's insufficient for robust scientific comparison or optimization. It should not be presented as a standalone benchmark.

## 4. What's the cleanest formulation to put in §1.2 as a secondary outcome and in §8 Future Work as a benchmark proposal?

**§1.2 Secondary Outcome:**

"As a secondary outcome, we report the **per-question improvement rate**, defined as the percentage of questions where the 5-judge primary mean score under a given context condition exceeded the 5-judge primary mean score under the no-context baseline (C5). This metric provides an interpretable measure of the *breadth* of positive impact across the behavioral prediction battery, indicating how frequently personalization led to an improved outcome."

**§8 Future Work (Benchmark Proposal - *if you insist, but I strongly advise against proposing it as a primary benchmark*):**

"We explored the **per-question improvement rate over a

---

## Gemini 2.5 Pro

This is a direct, no-diplomacy analysis.

### 1. Is it a good candidate benchmark metric?

No, not as a primary benchmark. It is a good candidate for a **secondary, supplementary benchmark** to be reported alongside a magnitude-sensitive metric.

**Strengths:**

*   **High Interpretability:** You are correct. "70.9% of questions improved" is immediately understandable to almost any reader, far more so than "a mean score delta of +0.43 on a 5-point Likert scale." This is its single greatest strength.
*   **Scale Independence:** It successfully abstracts away the specific rating scale (1-5, 1-7, 1-100), making it theoretically comparable across studies that use different rubrics. This is a significant advantage over raw score deltas.
*   **Highlights Breadth of Impact:** The metric excels at showing how consistently or broadly an intervention works. A high improvement rate suggests the personalization is helping across a wide range of situations, not just acing a few specific questions.

**Weaknesses:**

*   **Ignores Magnitude:** This is the fatal flaw for a primary benchmark. An improvement from a score of 2.0 to 2.1 (a trivial, likely noise-driven change) is counted identically to an improvement from 2.0 to 5.0 (a profound, game-changing success). A system that makes many tiny, insignificant improvements will score higher than a system that makes fewer, but vastly more important, improvements. This is unacceptable for a primary measure of performance.
*   **High Sensitivity at the Baseline Threshold:** The claim of being "robust to judge noise" is misleading. While it's robust to noise *away* from the baseline, it is acutely sensitive to noise *at* the baseline. If the baseline score is 3.4, a noisy judge rating of 3.5 counts as an "improvement" while 3.3 counts as a "worsening." This can make the metric unstable if many questions have scores very close to the baseline.
*   **Baseline Dependency:** The metric is only as meaningful as the baseline is difficult. It's easy to get a 90% improvement rate over a baseline that is consistently wrong. This makes it difficult to compare a 70% improvement rate on a hard task (with a strong baseline) to a 90% rate on an easy task (with a weak baseline).
*   **Potential for Gaming:** Researchers could be incentivized to "sprinkle a little personalization" everywhere to get tiny, consistent bumps across all questions, rather than focusing on solving the hard problems where personalization truly matters.

**Verdict:** It's a useful diagnostic, not a headline result. It measures the *consistency* of an effect, not its *strength*.

### 2. Are there comparable established metrics?

Yes. This metric is a direct parallel to several well-established concepts.

*   **Statistics (Sign Test):** This metric is effectively a massive sign test. The sign test compares pairs of data to see if the direction of change is consistent, while completely ignoring the magnitude of the change. It's known to be less powerful than tests that use magnitude (like a t-test), but more robust to outliers. Your metric has the same trade-off.
*   **LLM Evaluation (Win Rate):** This is extremely similar to the "win rate" used in head-to-head comparisons like the Chatbot Arena. "Model A beats Model B on X% of prompts." Your metric is a win rate against a fixed opponent: the no-context baseline. This is a strong and very current parallel.
*   **Information Retrieval (Precision):** It has the same spirit as Precision@K (e.g., "what percentage of the top 10 results were relevant?"). It's a simple, interpretable rate that binarizes a more complex reality (some documents are more relevant than others). More advanced IR metrics like nDCG were invented specifically to overcome this limitation by incorporating the *degree* of relevance (i.e., magnitude). Your metric is to "mean score delta" as "Precision" is to "nDCG".

### 3. Propose as benchmark or present as internal metric?

**Propose it explicitly as a benchmark, but frame it carefully as a secondary, complementary one.**

Do not present it as the primary way to measure success. To do so would be naive and would open your paper to valid criticism about ignoring magnitude.

Instead, frame it as part of a recommended *pair* of metrics.
1.  **Primary Metric:** A magnitude-sensitive score (e.g., mean score delta, Cohen's d). This measures the *depth* of improvement.
2.  **Secondary Metric:** The per-question improvement rate. This measures the *breadth* of improvement.

Arguing that both are needed for a complete picture is a strong, sophisticated position. Arguing for your metric alone is weak.

### 4. What's the cleanest formulation?

**For §1.2 (as a secondary outcome):**

> "Our primary outcome is the mean improvement in judge scores over a no-context baseline. As a key secondary outcome, we introduce the **per-question improvement rate**: the percentage of questions where personalization improved the model's score. This metric is designed to measure the *breadth* of the intervention's impact, complementing the primary metric's focus on the *magnitude* of that impact."

**For §8 Future Work (as a benchmark proposal):**

> "We propose the **per-question improvement rate** as a candidate for a standardized secondary benchmark in AI personalization research. While magnitude-aware metrics like mean score delta are essential for measuring the *depth* of an intervention's effect, they can be difficult to compare across studies using different scales or rubrics. The improvement rate, analogous to win-rate in head-to-head model comparisons, is scale-independent and highly interpretable, providing a clear measure of the *breadth* of an intervention's success. We recommend future personalization studies report both a magnitude-aware primary metric and this improvement rate to provide a more complete and comparable picture of performance."

### 5. What could go wrong if other groups adopt this metric? (Failure Modes)

1.  **The Goodhart's Law Failure:** "When a measure becomes a target, it ceases to be a good measure." If this becomes a key benchmark, labs will optimize for it. This would lead to models that make tiny, safe, superficial changes to many answers rather than profound, correct changes to a few. The field would stagnate on shallow, broad improvements.
2.  **Misleading Headlines:** A paper could have a headline result of "90% Improvement Rate!" while the actual average improvement is a statistically insignificant 0.05 points on a 5-point scale. This metric makes it easy to hide a lack of meaningful progress behind a superficially impressive number.
3.  **Ignoring the "Worsening Rate":** The focus on improvement is natural, but the worsening rate is a critical measure of harm and unreliability. A model that improves 80% and worsens 15% is very different from one that improves 80% and worsens 1%. If groups only report the improvement rate, they are hiding critical information about the risks of their personalization method. **Any proposal must insist on reporting the full triad: improve/tie/worsen percentages.**
4.  **Baseline Manipulation:** A researcher could use a deliberately simplistic or poorly-tuned no-context model to make their baseline performance artificially low, thus making their improvement rate look spectacular. This would destroy cross-study comparability.
5.  **Task Inappropriateness:** For some tasks, only a few answers matter. In a medical diagnostic task, improving 99 boilerplate questions by a little is worthless if you fail to improve the one critical question about identifying

---

## Mistral Large

### **1. Is per-question improvement rate a good candidate benchmark metric?**
**Strengths:**
- **Interpretability:** "X% of questions improved" is intuitive and avoids the opacity of mean-score deltas.
- **Robustness to judge noise:** Binary improvement/worsening (with ties) reduces sensitivity to outlier ratings.
- **Comparability across studies:** Doesn’t require matched scales or judge panels, unlike raw score deltas.
- **Generalizability:** Works for any context representation, model, or population.
- **Focus on personalization:** Directly measures whether context helps predict behavior, which is core to the task.

**Weaknesses:**
- **Loss of granularity:** Ignores *how much* improvement occurs (e.g., a 0.1-point gain counts the same as a 2-point gain).
- **Baseline dependence:** The metric is only as good as the no-context baseline. If the baseline is weak or arbitrary, the improvement rate is meaningless.
- **Tie handling:** Ties (13.1% in the data) are ambiguous—are they true ties or noise? The metric doesn’t distinguish.
- **Question selection bias:** If the battery is skewed toward easy/hard questions, the improvement rate may not generalize.
- **No cost-benefit tradeoff:** Doesn’t account for the effort (e.g., token count) required to achieve the improvement.

**Verdict:** It’s a **decent secondary metric**, but a **poor primary benchmark**. It’s useful for quick comparisons but lacks the nuance needed for rigorous evaluation.

---

### **2. Comparable established metrics**
This metric parallels:
- **Win rate (LLM evals):** Common in head-to-head LLM comparisons (e.g., "Model A wins 60% of the time"). Your metric is a win rate against a baseline.
- **Precision/recall in IR:** "Improvement rate" is like precision (fraction of questions where context helped), but without recall (coverage of all possible improvements).
- **Net Promoter Score (NPS):** A coarse, interpretable metric that sacrifices granularity for simplicity.
- **McNemar’s test (statistics):** Used to compare paired binary outcomes (improved vs. not improved).

**Contradictions:**
- **Mean score deltas (e.g., MSE, MAE):** Your metric discards magnitude, which is often critical in behavioral prediction.
- **Rank-based metrics (e.g., NDCG, MRR):** These account for *degree* of improvement, not just binary wins.
- **Effect size metrics (e.g., Cohen’s d):** These standardize improvements, making them comparable across studies—your metric doesn’t.

---

### **3. Benchmark proposal: Explicit or internal?**
**Propose it as a benchmark, but with caveats.**
- **Why?** The field lacks standardized personalization metrics. This is a step toward comparability.
- **How?** Frame it as a **candidate benchmark** (not the benchmark) and emphasize its limitations.
- **Where?** §8 (Future Work) is the right place. §1.2 should mention it as a secondary outcome, not a primary contribution.

**Alternative:** If the paper’s main contribution is the *method* (not the metric), keep it as an internal reporting tool and let the community decide if it’s useful.

---

### **4. Cleanest formulation for §1.2 and §8**
**§1.2 (Secondary Outcome):**
> *"As a secondary outcome, we report the per-question improvement rate over a no-context baseline, defined as the percentage of questions where a condition’s 5-judge mean score exceeds the baseline. This metric offers a robust, interpretable measure of personalization efficacy that is replicable across judge panels and rubrics. In our study, [Condition X] improved 78.6% of questions, while [Condition Y] improved 70.9%."*

**§8 (Future Work):**
> *"We propose the per-question improvement rate as a candidate benchmark for AI personalization research. This metric—computed as the percentage of questions where a context-augmented model outperforms a no-context baseline—has several advantages: (1) interpretability, (2) robustness to judge noise, and (3) comparability across studies. However, it discards magnitude of improvement and depends on the quality of the baseline. Future work should validate this metric against established benchmarks (e.g., mean score deltas, effect sizes) and explore hybrid approaches that combine binary improvement with magnitude-aware metrics."*

---

### **5. Failure modes if adopted**
1. **Gaming the baseline:** Researchers could cherry-pick weak baselines to inflate improvement rates.
2. **Ignoring magnitude:** A model that improves 70% of questions by 0.1 points might be worse than one that improves 50% by 2 points.
3. **Question selection bias:** If the battery is unrepresentative (e.g., too easy/hard), the metric won’t generalize.
4. **Tie ambiguity:** Ties could be treated as "no improvement" or "noise," leading to inconsistent reporting.
5. **Overfitting to judges:** If judges are inconsistent, the metric becomes unreliable (though the 5-judge mean mitigates this).
6. **Token efficiency blindness:** The metric doesn’t penalize models that require massive context (e.g., 420K words) for small gains.
7. **False precision:** "70% improvement" sounds precise but hides uncertainty (e.g., confidence intervals, judge disagreement).
8. **Misaligned incentives:** Researchers may optimize for binary wins rather than meaningful behavioral prediction.

**Worst-case scenario:** The metric becomes the de facto standard, and the field converges on models that win on paper but fail in practice (e.g., overfitting to judge biases, ignoring effect sizes).

---

### **Final Verdict**
- **Good for:** Quick comparisons, secondary reporting, community discussion.
- **Bad for:** Primary benchmarking, high-stakes evaluation, or replacing magnitude-aware metrics.
- **Recommendation:** Propose it as a **candidate benchmark in §8**, but stress its limitations and encourage hybrid metrics (e.g., improvement rate + mean delta). Don’t let it become the sole metric.

---

## Cerebras Qwen3 235B

### 1. **Is per-question improvement rate a good candidate benchmark metric?**

**No. It is not a good candidate benchmark metric in its current form.**

It has *some* useful properties, but it is **fundamentally flawed** as a primary or standalone benchmark for AI personalization. Here's why:

#### ✅ Strengths:
- **Interpretability**: "70% of questions improved" is intuitive and accessible.
- **Robustness to scale differences**: Doesn't require score calibration across studies.
- **Noise resistance**: Binary per-question outcomes reduce sensitivity to judge variance.
- **Actionable insight**: Reveals whether a method *consistently helps more often than it hurts*.

#### ❌ Critical weaknesses:
- **Ignores magnitude of change**: A tiny improvement (e.g., 0.01) counts the same as a massive one; a catastrophic drop (e.g., -2.0) counts the same as a small one. This enables **gaming the metric** via methods that make many small gains and a few large losses.
- **Ties are ambiguous**: How is "tie" defined? ±0.05? ±0.1? This threshold choice dramatically affects results and is rarely reported consistently.
- **Susceptible to floor/ceiling effects**: Questions already near ceiling under baseline can't improve, so improvement rate is capped regardless of method quality.
- **Biased against high-performing baselines**: The better C5 is, the harder it is to improve — so improvement rate penalizes progress on already-hard problems.
- **Noisy aggregation**: Judging "improve/worsen/tie" on a per-question basis with 5 judges introduces substantial uncertainty, especially if inter-rater reliability isn't high.
- **Not monotonic with performance**: You could have a method that increases average accuracy but has a *lower* improvement rate (e.g., if it makes fewer but larger gains).

> **Bottom line**: It captures *directional consistency*, not *performance*. That’s useful context — but dangerous as a benchmark.

---

### 2. **Are there comparable established metrics?**

Yes — and they highlight why this metric is problematic.

#### In **information retrieval**:
- **Precision@k**, **NDCG**, **Mean Reciprocal Rank**: All weight magnitude of improvement.
- **Win rate** (e.g., in pairwise ranking): Used in LLM evals (e.g., MT-Bench), but always **paired with significance testing and effect size**.
- **Relative improvement rate** (e.g., % queries with better MAP): Exists, but considered **diagnostic**, not a benchmark.

#### In **LLM evaluation**:
- **Accuracy delta over baseline**: Standard (e.g., HELM, BIG-bench).
- **Win rates in head-to-head comparisons**: Common (e.g., Chatbot Arena), but only for **relative ranking**, not absolute progress.
- **% of cases where model exceeds threshold**: Seen in clinical/AI decision support (e.g., "in X% of cases, AI reduced diagnostic error").

#### Key contrast:
No major benchmark uses **% improved questions** as a *primary* metric because it discards **how much** better or worse things got. The closest analogs are **win rates**, which are accepted only when paired with statistical rigor and clear pairwise framing.

> This metric is most similar to **win rate**, but misapplied: win rate compares two systems *head-to-head*, not each against a baseline per question.

---

### 3. **Should the paper propose it as a benchmark?**

**No — not as a standalone benchmark.**

✅ **Do**: Present it as a **secondary, diagnostic metric** to complement mean score deltas. It adds interpretability and robustness.

❌ **Don’t**: Elevate it to a proposed benchmark axis without major caveats and validation.

If you *must* propose it, do so **only as a complementary axis**, not a replacement for effect size or mean performance.

---

### 4. **Cleanest formulation for paper**

#### In §1.2 (Secondary Outcome):
> "In addition to mean score improvements, we report the per-question improvement rate over the no-context baseline — i.e., the percentage of questions for which the 5-judge primary mean score increased under the tested condition. This metric provides an interpretable, scale-invariant measure of how consistently a personalization method enhances prediction accuracy across a behavioral battery."

#### In §8 (Future Work):
> "We suggest that the per-question improvement rate — the fraction of test items where a method improves over a no-context baseline — could serve as a complementary benchmark axis in AI personalization research. Its scale invariance and interpretability make it portable across rubrics and judge panels. However, due to its insensitivity to effect magnitude and vulnerability to floor/ceiling effects, it should be used alongside mean performance metrics and with defined thresholds for improvement (e.g., minimal clinically important difference analogs). Standardization of tie-handling and significance testing would be required for cross-study comparability."

---

### 5. **What could go wrong if others adopt this?**

**Failure modes (ranked by severity):**

1. **Gaming via tiny gains + big losses**:
   - A method could boost 70% of questions by 0.01 and destroy 30% by 1.0, yet score highly. Net performance drops, but improvement rate looks great.

2. **Threshold arbitrage**:
   - Labs pick different "tie" windows (±0.05 vs ±0.2) to inflate improvement rates. Results become incomparable.

3. **Ignoring catastrophic errors**:
   - A model that occasionally predicts wildly incorrect behavior (e.g., "this person would steal") might still have high improvement rate if most answers are slightly better.

4. **Discouraging high baselines**:
   - If C5 is strong, improvement rate is capped. Researchers avoid improving baselines to keep room for "improvement."

5. **Floor/ceiling distortion**:
   - Easy/hard questions dominate results not due to method quality, but due to baseline performance.

6. **False sense of progress**:
   - A paper reports "75% improvement rate!" while mean score change is negligible. Readers overestimate impact.

7. **Erosion of metric integrity**:
   - As adoption grows, people drop the "5-judge mean" and use single judges or automated scores, breaking the noise-robustness argument.

---

### Final Verdict:

**This metric is a useful *diagnostic tool*, not a benchmark.**

Proposing it as a benchmark without strong caveats risks **misleading the field**, enabling **metric hacking**, and **diverting attention from actual performance**.

If the goal is benchmarking, focus on:
- **Standardized behavioral batteries**
- **Mean score deltas with error bars**
- **Win rates in head-to-heads**
- **Effect size (e.g., Cohen’s d) over baseline**

Use improvement rate to *illustrate consistency*, not to *measure progress*.

---

## GPT-5.4

Short version: **yes, but only as a secondary benchmark axis, not as the benchmark**. It is useful, interpretable, and fairly portable across studies, but it is too lossy and too gameable to stand alone. If the paper proposes it, it should do so **narrowly and explicitly**: as a **scale-free “breadth of benefit” metric** to accompany mean score, not replace it.

## 1. Is it a good candidate benchmark metric?

### Verdict
**Reasonable secondary benchmark. Bad primary benchmark.**

### Why it’s attractive
This metric captures something real that mean deltas often hide:

- **Breadth of benefit.**  
  “Did personalization help on many questions, or only a few?” is important. A condition that slightly improves 75% of questions is qualitatively different from one that massively improves 10% and harms the rest.

- **Scale-free across studies.**  
  If one paper uses a 1–5 rubric and another uses 0–100, raw deltas are hard to compare. Improvement rate only needs direction.

- **Interpretability.**  
  “Improved on 71% of questions relative to no-context” is immediately understandable.

- **Potentially more stable across judge panels.**  
  If absolute score levels shift across judges but pairwise direction is preserved, sign-based metrics can be more reproducible than raw means.

- **Useful for personalization specifically.**  
  Personalization systems should help broadly, not just on average. This metric directly tests whether gains are widespread.

### Why it is not enough
The weaknesses are serious:

- **It throws away magnitude.**  
  A tiny +0.01 counts the same as a huge +1.0. A tiny harm counts the same as catastrophic failure. That is a major defect.

- **It is threshold-sensitive and noise-sensitive near ties.**  
  If many questions have small score differences, judge noise can flip “improved” to “worsened.” Unless you define a tie band or uncertainty rule, this metric can be unstable.

- **It can reward trivial broad gains over meaningful concentrated gains.**  
  A weak method that nudges many questions slightly upward can beat a method that strongly improves fewer but more important questions.

- **It ignores question importance.**  
  All questions count equally. In behavioral prediction, some questions are much harder, more consequential, or more diagnostic than others.

- **It can be inflated by easy questions.**  
  If the battery contains many easy-to-improve items, the metric looks good even if performance on difficult or high-value items is poor.

- **It depends on the baseline.**  
  “Improvement over no-context” is not a property of the method alone. It is a property of the method relative to a specific baseline model, prompt, and evaluation setup.

- **It is vulnerable to calibration artifacts.**  
  If a condition makes outputs more verbose, more hedged, or more rubric-friendly, judges may score slightly higher on many questions without true behavioral prediction improving.

- **Question-level dependence is ignored.**  
  Questions from the same subject are correlated. Reporting a raw percent over all questions can overstate precision unless analysis clusters by subject.

So: **good descriptive metric, weak standalone benchmark.**

---

## 2. Comparable established metrics

This metric has clear analogues. It is not weird. But it also inherits known limitations from those analogues.

### Closest parallels

#### A. Win rate / pairwise preference rate in LLM evaluation
This is the strongest analogy.

- In LLM evals, people report things like:
  - model A beats model B on X% of prompts
  - pairwise preference win rate from human judges
- Your metric is basically:
  - **condition beats baseline on X% of questions**

Why this matters:
- It is intuitive and robust to scale differences.
- It is widely understood.
- But everyone knows win rate alone is incomplete because it ignores margin and can be gamed by small consistent shifts.

So your proposal is aligned with an established evaluation style, not novel in principle.

#### B. Sign test / proportion of positive paired differences
Statistically, this is basically a descriptive version of a **paired sign test**.

- For each question, compare condition score to baseline score.
- Count positive, zero, negative differences.

This is a standard nonparametric idea:
- robust to scale
- weak assumptions
- but lower information efficiency than using magnitudes

That’s a point in its favor as a benchmark axis, but also a reminder that it should not replace richer analyses.

#### C. “Percentage of queries improved” in information retrieval
IR has long recognized that mean metrics can hide uneven effects. People often report:

- percentage of queries improved
- percentage of topics improved
- win/tie/loss over queries

This is very close to your setup:
- query = question
- system = context condition
- metric = judged quality score

Again, same lesson:
- useful complement
- not sufficient alone

#### D. Decision-support / clinical utility style responder analyses
In medicine and decision-support, people often report:
- proportion of cases improved
- responder rates
- net benefit style summaries

Your metric resembles a responder analysis without a minimum clinically important difference threshold.

That last point matters: in those fields, **plain “any improvement” is often considered too weak**, so they define a meaningful improvement threshold. You may want the same.

### What it contradicts or fails to capture
It runs against the grain of metrics that care about **ranking quality, calibration, or expected utility**.

- In IR, metrics like NDCG and MAP care about where gains occur and how large they are.
- In forecasting/decision support, proper scoring rules care about calibrated probabilities and magnitude of error.
- In LLM eval, average score and pairwise win rate are often both reported because each misses things the other captures.

So this metric does **not** replace score deltas, rank-based metrics, or utility-weighted metrics.

---

## 3. Should the paper explicitly propose this as a benchmark?

### Recommendation
**Yes, but only in a constrained way.**

Do **not** say:
- “We propose per-question improvement rate as a benchmark for AI personalization.”

Say:
- “We propose per-question improvement rate over a no-context baseline as a candidate secondary benchmark axis.”

That wording matters. If you oversell it, reviewers will correctly attack it.

### Why explicit proposal is still worth doing
You have a decent case that this metric is:

- portable across rubrics
- interpretable
- useful for cross-study comparison
- especially relevant to personalization, where broad consistency matters

That is enough to justify a benchmark proposal **as one axis**.

### Why it should not be framed as primary
Because the obvious reviewer response is:
- “This is just a sign statistic.”
- “It ignores effect size.”
- “It is sensitive to noise.”
- “It can be gamed.”

And they’d be right.

So the paper should frame it as:
1. a **secondary outcome in this study**
2. a **candidate benchmark axis for future work**
3. to be reported **alongside** mean score and uncertainty estimates

Not as a replacement benchmark.

---

## 4. Cleanest formulation for §1.2 and §8

## §1.2 Secondary outcome
Use something like this:

> **Secondary outcome: per-question improvement rate over the no-context baseline.**  
> For each question, we compare the mean primary-judge score under a tested condition to the corresponding mean score under the no-context baseline (C5). We then report the proportion of questions that improve, tie, or worsen. This metric summarizes the **breadth of benefit** of a personalization method and is less dependent on the absolute scale of the scoring rubric than mean-score deltas.

If you want one more sentence:

> We treat this as a complement to mean score, not a substitute, because it captures direction of change but not magnitude.

That last clause is important. It preempts criticism.

### Better technical formulation
If you want it cleaner and more general:

> Let \(s_{q}^{(k)}\) denote the mean primary-judge score for question \(q\) under condition \(k\), and \(s_{q}^{(0)}\) the corresponding score under the no-context baseline. We define the per-question improvement rate for condition \(k\) as  
> \[
> \frac{1}{Q}\sum_{q=1}^{Q}\mathbf{1}[s_q^{(k)} > s_q^{(0)}],
> \]
> with ties and worsenings reported analogously.

But if exact equality is rare or noisy, I would strongly recommend not using strict equality in the long run. Better:

> In future benchmark use, ties should be defined using a prespecified indifference band or uncertainty criterion rather than exact equality.

## §8 Future Work benchmark proposal
Use something like this:

> **Candidate benchmark axis for personalization.**  
> We suggest that future AI-personalization studies report, in addition to mean score, the **per-question improvement rate over a standardized no-context baseline**: the percentage of evaluation questions on which a personalized condition scores higher than the same model without user context. This metric is scale-free, directly interpretable, and comparable across studies using different scoring rubrics. It measures the **breadth** of personalization benefit rather than its average magnitude.

Then immediately constrain it:

> We do not view this metric as sufficient on its own. Because it discards effect size and can be sensitive to small score fluctuations, it should be reported alongside mean-score deltas, confidence intervals, and where possible subject-clustered or hierarchical analyses.

That is the cleanest defensible formulation.

---

## 5. What could go wrong if others adopt it?

A lot. Here are the main failure modes.

### 1. Tiny gains get overcredited
A method that produces microscopic score increases on many questions will look great.

Example:
- +0.02 on 80% of questions
- -0.50 on 20%

Improvement rate says 80% improved. That may be a worse system overall.

### 2. Catastrophic harms get hidden
Because magnitude is ignored, severe failures disappear into the same “worsened” bucket as trivial losses.

This is especially bad if personalization occasionally causes major misreads of the user.

### 3. Benchmark gaming via style optimization
Teams may optimize for whatever causes judges to give slight upward nudges:
- more hedging
- more socially desirable wording
- more rubric-aware phrasing
- more generic but safe answers

That can increase “improved” counts without improving true personalization.

### 4. Instability from judge noise
If many question-level differences are small, random variation in judging can flip outcomes.

Without a tie band, the metric can become a noisy sign count.

Fix:
- define a minimum difference threshold
- or use bootstrap / hierarchical uncertainty
- or classify ties using confidence overlap

### 5. Cross-study comparability may be weaker than claimed
Yes, it is more scale-free than mean deltas. But it is still not fully comparable across studies because it depends on:

- battery difficulty
- question wording
- baseline strength
- judge rubric
- subject population
- model family

A 70% improvement rate in one battery may not mean the same thing as 70% in another.

### 6. Easy-question inflation
If a benchmark contains many low-value or redundant questions, systems can rack up high improvement rates by improving easy items.

This is a classic benchmark pathology.

### 7. Correlated questions inflate confidence
Behavioral batteries often contain clusters of related questions per subject. Treating all questions as independent exaggerates effective sample size.

A method may seem very stable because it improved many near-duplicate items.

### 8. Baseline manipulation
Because the metric is “over no-context baseline,” benchmark scores can be moved by changing the baseline prompt or model setup.

A weak baseline makes everyone look good.
A strong baseline compresses gains.

If this becomes a benchmark, the baseline must be tightly standardized.

### 9. Penalizing specialization
A method that gives large gains on the hardest, most behaviorally diagnostic questions but little change elsewhere may look mediocre by improvement rate.

That could discourage work that improves what actually matters.

### 10. Ties become arbitrary
Exact ties on mean judged scores may be rare or depend on decimal precision. Different groups will handle ties differently unless the benchmark specifies:
- exact equality
- tolerance band
- statistical indifference rule

Without standardization, the metric is not reproducible.

### 11. Subject-mix dependence
Your own numbers already show this:
- low-baseline subjects: high improvement rates
- all subjects: lower rates

So the metric is heavily affected by who is in the sample. If benchmark populations differ in baseline predictability, scores won’t transport cleanly.

### 12. It may encourage broad but shallow personalization
Teams may optimize for “slightly better almost everywhere” rather than “substantively better where personalization matters most.”

That is not always the right research incentive.

---

## Bottom-line recommendation

### What the paper should do
- **Report it prominently as a secondary outcome.**
- **Propose it cautiously as a candidate benchmark axis.**
- **Do not present it as a standalone benchmark metric.**

### What the paper should explicitly say
Something like:

- It measures **breadth of improvement**
- It is **scale-free and interpretable**
- It complements, not replaces, mean score
- It should be standardized with:
  - a fixed no-context baseline
  - a prespecified tie rule
  - clustered uncertainty by subject
  - companion magnitude metrics

### If you want the bluntest possible judgment
**As a sole benchmark metric: no.**
**As a secondary benchmark axis: yes, absolutely defensible.**

If you want, I can also draft:
1. a reviewer-proof paragraph for §1.2,  
2. a sharper §8 benchmark proposal, and  
3. a one-sentence caveat block for the limitations section.

---

## Claude Opus 4.6

# Assessment of Per-Question Improvement Rate as a Benchmark Metric

## 1. Is this a good candidate benchmark metric?

**It's a decent secondary metric but a mediocre primary benchmark. Here's why.**

### Strengths

- **Interpretability is real.** "70% of questions improved" is immediately legible to anyone. This is a genuine advantage over reporting that "mean score increased by 0.34 on a 5-point rubric-dependent scale."
- **Ordinal robustness.** By collapsing to improve/tie/worsen, you eliminate sensitivity to how much a rubric point means. This makes cross-study comparison plausible in a way that raw score deltas never will be, because different studies will use different rubrics, different scales, different judge prompts.
- **Replication-friendly.** A new group with a different 5-judge panel, different rubric anchoring, or even a different LLM-as-judge can still report "X% improved" and the numbers are at least on the same conceptual scale.
- **Noise absorption.** Binarizing at the question level absorbs within-question judge variance. A question that goes from 2.8 to 3.2 and a question that goes from 2.8 to 4.6 both count as "improved," which means a single noisy judge can't inflate the magnitude of apparent gains.

### Weaknesses — and these are serious

- **You're throwing away effect size.** This is the core problem. A condition that improves 70% of questions by 0.01 points and worsens 15% by 2.0 points looks great on improvement rate and is actually catastrophic. You **must** pair this with magnitude information or it's misleading. The improvement rate alone is not sufficient.

- **Tie sensitivity.** Your tie rate depends entirely on granularity. With a 5-judge mean on a multi-point scale, exact ties are rare, so almost everything is either "improved" or "worsened." If you had a coarser scale or fewer judges, the tie rate would dominate and the metric would become unstable. This means the metric's behavior is quietly coupled to your measurement resolution, which undermines cross-study comparability — the very thing you're selling.

- **No difficulty weighting.** A question where the baseline already scores 4.8/5.0 and the condition scores 4.9/5.0 counts the same as a question where the baseline scores 1.0 and the condition scores 4.5. The metric treats all questions as equally important. In practice, the hard questions (low baseline) are where personalization matters most.

- **Threshold arbitrariness.** "Improvement" means any positive delta. Why not ε-improvement (must improve by at least 0.5 points)? The choice of threshold = 0 is a design decision that looks natural but is actually arbitrary, and different thresholds would give materially different results. Your 70.9% could drop to 45% with a 0.5-point threshold.

- **Base-rate dependence.** Your own data shows this: low-baseline subjects hit 70.9% improvement, all-14-subjects hit 58.8%. The metric is heavily influenced by how easy the baseline is to beat. If someone runs this on subjects where the no-context baseline already performs well, improvement rates will be low regardless of context quality. This makes cross-population comparison treacherous.

**Bottom line:** Good as a secondary reporting metric. Insufficient as a standalone benchmark. Must be paired with magnitude and worsening-magnitude information.

---

## 2. Comparable established metrics

This metric has clear parallels, and you should cite them:

**Win rate (LLM evaluation).** Chatbot Arena, LMSYS, and most LLM-vs-LLM comparisons report win/tie/loss rates. Your metric is structurally identical: condition A vs. condition B, per-item, binarized outcome. The literature already knows the strengths and limitations of win rates. You should frame your metric explicitly as a **win rate against a no-context baseline** — this is established terminology and will be immediately recognized.

**Mean Reciprocal Rank (MRR) and Precision@k (Information Retrieval).** These are per-query metrics that get averaged. Your metric is analogous to Precision@1 in a sense: "did the system get this question right (better than baseline) or not?" The IR community long ago learned that per-query averages hide variance, which is why they also report per-query analysis, MAP, and NDCG. The lesson: single-number per-query aggregates need distributional backup.

**Proportion of Concordant Pairs (decision-support / clinical prediction).** In clinical decision-support evaluation, people report the fraction of cases where the model's recommendation improved the outcome vs. a standard-of-care baseline. Your metric is this. The clinical literature pairs it with NNT (number needed to treat) and harm rates — analogous to your worsening rate.

**Sign test / binomial test.** Statistically, your improvement rate is the test statistic for a sign test. This is well-established in nonparametric statistics. You should note that the improvement rate has a natural inferential companion: a sign test or binomial test against 50% (chance improvement under null).

**What this parallels and does NOT contradict:** Win rate is widely accepted as a useful secondary metric. Nobody uses it as the sole benchmark. Your proposal is consistent with established practice *if* you position it correctly.

---

## 3. Should the paper explicitly propose this as a benchmark?

**Yes, but with precise scoping.** Here's the framing:

- **Do** propose it as a **standardized secondary reporting metric** — something every AI personalization paper should report alongside whatever primary metric they use.
- **Do not** propose it as a **primary benchmark** or a sufficient standalone measure.
- **Do** propose a **reporting triplet**: (improvement rate, worsening rate, median magnitude of improvement among improved questions). This triplet is replicable, interpretable, and addresses the effect-size blindness problem.

The reason to propose it explicitly rather than keeping it internal: the AI personalization field currently has **no** standardized reporting convention. Someone needs to propose one. A win-rate-style metric against a no-context baseline is a natural Schelling point. If you don't propose it, the field will converge on something worse (probably raw score deltas on incomparable scales).

---

## 4. Cleanest formulations

### §1.2 (Secondary outcome)

> **Per-question improvement rate.** As a secondary outcome, we report the proportion of questions on which a given context condition improves the 5-judge primary mean score relative to the no-context baseline (C5). For each question *q* and condition *c*, we classify the outcome as *improved* (score_c > score_C5), *tied* (score_c = score_C5), or *worsened* (score_c < score_C5), and report the improvement rate, worsening rate, and median improvement magnitude across all questions. This metric parallels win-rate reporting in LLM evaluation (Chatbot Arena; Zheng et al., 2023) and is designed to be comparable across studies that use different rubrics, judge panels, or scoring scales.

### §8 (Future Work — benchmark proposal)

> **Toward a standardized personalization metric.** We propose that AI personalization studies adopt a common secondary reporting convention: the *per-question improvement rate* over a no-context baseline, evaluated on a behavioral-prediction battery. Concretely, we recommend reporting a triplet: (improvement rate, worsening rate, median magnitude of change among improved and worsened questions respectively). This convention has several properties that support cross-study comparison: it is ordinal (insensitive to rubric scale), interpretable without domain knowledge, and structurally identical to win-rate metrics already standard in LLM evaluation. We note important limitations: the metric discards effect-size information, is sensitive to baseline difficulty, and requires a minimum measurement resolution to avoid tie-rate dominance (we recommend ≥5 judges on a ≥4-point scale). We encourage future work to evaluate this metric's stability across judge panels, question batteries, and subject populations, and to establish whether a threshold-adjusted variant (e.g., requiring ≥0.5-point improvement) better discriminates between context conditions.

---

## 5. Failure modes if other groups adopt this metric

**These are real and some are dangerous:**

1. **Gaming via easy baselines.** If the no-context baseline is deliberately made weak (e.g., by using a poorly prompted model, or by selecting subjects the model knows nothing about), improvement rates will be inflated. Groups will be incentivized to choose hard-to-predict subjects or weak baseline prompts to maximize their reported improvement rate. **Mitigation:** Require reporting the baseline mean score alongside the improvement rate.

2. **Ignoring worsening magnitude.** A system that improves 80% of questions by 0.1 points and worsens 20% by 3.0 points will look great. If groups only report improvement rate without the worsening-magnitude companion, harmful personalization systems will look good on paper. **Mitigation:** Mandate the full triplet (improvement rate, worsening rate, median worsening magnitude).

3. **Threshold shopping.** With threshold = 0, any positive delta counts. With threshold = 0.5, fewer questions count. Groups will pick the threshold that makes their system look best. **Mitigation:** Standardize on threshold = 0 as the default, but require sensitivity analysis at ε = {0.25, 0.5, 1.0}.

4. **Tie-rate instability across measurement setups.** A study using 3 judges on a 3-point scale will have many ties. A study using 7 judges on a 7-point scale will have almost none. The "same" metric will behave completely differently. **Mitigation:** Specify minimum measurement resolution (≥5 judges, ≥4-point scale) as a prerequisite for reporting this metric.

5. **Question battery selection bias.** Groups will (consciously or not) select questions where their system improves over baseline. A battery of 20 easy questions will yield different improvement rates than a battery of 20 adversarial questions. **Mitigation:** This is the hardest problem. You need a standardized question battery or at minimum a standardized question-generation protocol. Without it, improvement rates are not comparable across studies even in principle.

6. **Ecological validity collapse.** The metric measures "did the AI predict this behavioral response better with context?" It does not measure "did the personalization actually help the user?" Groups may optimize for improvement rate on prediction batteries while building systems that are useless or harmful in deployment. This is the Goodhart's Law failure mode and it's essentially inevitable if the metric gains traction.

7. **Simpson's paradox across subject types.** Your own data shows that low-baseline subjects have much higher improvement rates than the full population. A study with more low-baseline subjects will report higher improvement rates. If groups don't stratify by baseline difficulty, the metric will conflate "our system is better" with "our subjects were harder for the baseline to predict." **Mitigation:** Require stratified reporting by baseline performance quartile.

---

## Summary recommendation

Propose it. Propose it as a **secondary standardized reporting metric**, not a primary benchmark. Propose the **triplet** (improvement rate, worsening rate, median magnitudes), not the improvement rate alone. Cite win-rate precedent explicitly. Specify minimum measurement requirements. And flag the failure modes in the paper — if you identify them first, you control the narrative and you look rigorous rather than naive.