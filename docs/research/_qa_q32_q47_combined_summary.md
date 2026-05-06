# Q&A Summary: Q32 (Era/Modernity/Exoticism) + Q47 (Refusal Intent)

_Two small post-hoc analyses against existing study data. No new experiments._

---

## Q32 — Era / modernity / content-exoticism cross-slice

**Author question:** "May be certain autobiographies do better? Maybe more modern ones vs old ones? Maybe ones with less 'craziness' vs others."

**Method:** All 14 main-study subjects classified by (era: pre_1700 / 1700-1900 / post_1900), (language modernity: archaic / modern), and (content exoticism: familiar / marginal-familiar / non-Western). Δ_spec pulled on the same 5-judge primary panel (haiku, sonnet, opus, gpt4o, gpt54) for both §4.1 (C2a-C5, C4a-C5, re-aggregated from raw judgments for panel consistency) and the 5 memory systems (mem0, letta, zep, supermemory, baselayer — from `memory_systems_5judge_primary.md`). Each Δ also residualized on C5 baseline via OLS across all 14 subjects to separate axis effects from baseline collinearity.

**Top-level finding:** Era and modernity are collinear with baseline — the raw "older subjects benefit less" pattern is fully explained by lower C5 baselines, and residualized cross-tabs collapse to within ±0.10 of zero across all five memory systems. The Western-tradition vs non-Western axis (renamed from "exoticism" after the Hamerton sensitivity test) shows a stable residualized gap of +0.15 to +0.25 favoring Western-tradition subjects on 4 of 5 memory systems (Mem0, Letta, Zep, Base Layer; Supermemory flat on both sides). The finding is robust to Hamerton's bucket assignment: moving him from `familiar` to `marginal-familiar` does not collapse the Western-tradition vs non-Western gap. **Decision: §8 Future Work as a named hypothesis, not a main finding. n=4 Western-tradition vs n=10 non-Western is enough to name but not to claim.**

**Report:** `C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/era_modernity_cross_slice.md`
**Data:** `C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/era_modernity_cross_slice.json`
**Script:** `C:/Users/Aarik/Anthropic/memory-study-repo/scripts/classify_subjects_era_modernity.py`

**One-paragraph drop-in for §8 (optional):**
> We examined whether the spec effect varied by subject era (pre-1700 / 1700-1900 / post-1900), language modernity (archaic / modern translation voice), or content domain (Western-tradition / non-Western). After residualizing on C5 baseline to separate axis effects from baseline-collinearity, era and modernity cross-slices collapsed to within ±0.10 of zero across all five memory systems — era and modernity are collinear with baseline and add no variance beyond the gradient. The Western-tradition vs non-Western axis showed a stable residualized gap of +0.15 to +0.25 favoring Western-tradition subjects on 4 of 5 memory systems (Mem0, Letta, Zep, Base Layer), with Supermemory flat at near-zero on both sides. The finding is robust to Hamerton's bucket assignment. With n=4 Western-tradition vs n=10 non-Western, we name this as a hypothesis for future work: the Base Layer spec, authored inside the Western-introspective autobiographical tradition, may transfer its axioms less effectively to subjects outside that tradition at matched baseline knowledge.

---

## Q47 — Refusal-intent classifier on the 81 spec-induced refusals

**Author question:** "Were we asking the model to do something morally reprehensible?" — specifically prompted by the Zitkala-Sa Q18 ventriloquism refusal.

**Method:** Claude Haiku 4.5 classified the 81 spec-induced refusal questions from P0-5 (`spec_refusal_audit.json`) into 5 intent categories: A_IMPERSONATE / B_FABRICATE_TESTIMONY / C_SPEAK_FOR_DEAD / D_PROTECTED_SPECULATION / E_ROUTINE_INFERENCE. Classifier saw question text + held-out passage only (not the C3 response, to avoid anchoring). Cost: ~$0.15 actual (well under the $2 cap).

**Top-level finding:** The data does not support a "spec teaches epistemic integrity on morally-loaded questions" framing. 75 of 81 refusals (93%) are on routine behavioural-prediction questions; inside the SPEC_AXIOM_TRIGGER cell specifically (P0-5's "retrieval was sufficient, the spec caused the refusal anyway"), 40 of 41 (98%) are routine. 0 cases were A_IMPERSONATE, 0 were B_FABRICATE_TESTIMONY. The 6 morally-loaded cases reduce to 3 unique questions repeated across systems (Seacole Q39 religious artwork, Keckley Q21 mother's grave, Hamerton Q41 religious tension).

**Zitkala-Sa Q18 direct probe.** A targeted probe (`scripts/_probe_zitkala_q18.py`) confirms Zitkala-Sa Q18 does not trigger a spec-induced C3 refusal in any of the 5 memory systems (C3 doesn't refuse; C1 doesn't refuse). Inspecting Q18 across the §4.1 conditions reveals what the author was likely remembering: **Q18 itself is a factually malformed question** ("how would Zitkala-Sa demonstrate acceptance of fate when facing execution?" — she was never executed). C2a and C4a refuse on grounds that the factual premise is false (e.g. *"the specification itself cannot be used to construct a false historical narrative"*). This is a correct response to a malformed question, not a spec-induced refusal on a well-posed ventriloquism request. The empirical record cannot support either the strong framing ("spec rejected ventriloquism") or a criticism of the spec on this axis — Q18 is a data-quality outlier in the question battery. A separate adversarial battery with well-posed impersonation/ventriloquism requests would be needed to test the motivating concern.

**Honest paper framing:** The spec's epistemic-humility axioms are a general-purpose conservatism dial, not a targeted moral-integrity mechanism. This matches the §4.4 mechanism claim ("spec trades retrieved-fact coverage for conservatism, and the rubric punishes conservatism") and removes a stronger framing the paper could be tempted to over-claim.

**Report:** `C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/refusal_intent_classification.md`
**Data:** `C:/Users/Aarik/Anthropic/memory-study-repo/docs/research/refusal_intent_classification.json`
**Script:** `C:/Users/Aarik/Anthropic/memory-study-repo/scripts/classify_refusal_intent.py`

---

## Cross-cutting note

Both analyses push against framings the paper could be tempted to adopt but that the data does not support:

- **Q32 pushes against** "older / less modern subjects benefit more from the spec" as a standalone finding — it is baseline-collinear and dissolves under residualization. In its place Q32 surfaces the *opposite*-direction hypothesis: after controlling for baseline, Western-tradition subjects show a +0.15 to +0.25 residualized lift over non-Western subjects at matched baselines on 4 of 5 memory systems. This is a transfer-limit hypothesis about the spec itself (authored inside a specific autobiographical tradition) rather than a subject-side difficulty claim.
- **Q47 pushes against** "the spec teaches the model epistemic integrity on morally-loaded questions." The refusal pattern is conservatism across the board on routine questions (93%). The author's motivating Zitkala-Sa Q18 case turns out to be a factually malformed question, not a well-posed ventriloquism test — so the ventriloquism concern cannot be tested on current data.

Both adjustments are honest and useful. They keep the paper from claiming mechanisms it did not test, and they surface a new (weaker but better-grounded) hypothesis about cross-cultural transfer that is worth naming in Future Work.
