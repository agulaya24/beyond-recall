# v10 §4.6.1 Methodology — External Verification

**Date:** 2026-04-25  
**Generated at:** 2026-04-25 09:22:18  
**Model used:** `gpt-5.5-2026-04-23`  
**Provider chain:** OpenAI -> Gemini 2.5 Pro -> Mistral Large

---

## Exact prompt sent

```
You are an experienced empirical-ML methodology reviewer. The author of an in-progress paper has caught a numerical discrepancy in their §4.6.1 Tier 2 cross-provider replication results. They asked me (Claude Code) to recommend a fix. I am asking you to evaluate whether my recommendation is methodologically sound.

## Situation

The paper's §4.6.1 currently reports Δ_spec values for 6 (subject × response_model) cells testing whether the specification effect reproduces with non-Anthropic response models reading non-Anthropic-generated batteries. The published Δ values are: Ebers × Sonnet +1.48, Ebers × Gemini Pro +1.07, Yung Wing × Sonnet +1.91, Yung Wing × Gemini Pro +1.27, Zitkala-Sa × Sonnet +1.40, Zitkala-Sa × Gemini Pro -0.55.

A mechanical recompute from the raw judgment files (results/_tier2/global_<subject>/tier2_<response_model>_judgments_<judge>.json) using the canonical 5-judge primary aggregation rule (per-judge per-question score → per-judge per-subject mean → panel mean across the five non-Gemini judges Haiku, Sonnet, Opus, GPT-4o, GPT-5.4) gives different numbers regardless of which Δ definition is used:

- Δ_C2a (internal, T2 C2a − T2 C5, 5-judge primary): +0.95 / +0.24 / +1.06 / +0.17 / +0.89 / -0.10
- Δ_C4a (internal, T2 C4a − T2 C5, 5-judge primary): +0.77 / +0.16 / +1.34 / +0.43 / +1.04 / -0.03
- Δ_C4a (T2 C4a − main-study Haiku C5, closest match): +1.45 / +1.61 / +1.00 / +0.91 / +0.31 / +0.10

Mean absolute error from published across all 8 tested definitions ranges 0.598-0.755. Sign matches are 5/6 or 6/6 across every definition. The 5 of 6 directional reproduction is invariant; the magnitudes are not reproducible.

## My recommendation

OPTION C: demote §4.6.1's table to direction-only. Drop the 6 magnitudes. Keep the check/cross direction-match column. Add a footnote pointing at the recompute scaffold and flagging the magnitude discrepancy as a v11 resolution item. The directional claim ("5 of 6 cells reproduce the specification direction across non-Anthropic models") is what the section's argument needs; the magnitudes are doing rhetorical not analytical work.

I considered:
- Option A (replace with delta_C4a internal recompute): requires picking a Delta definition without primary-data confirmation
- Option B (replace with delta_C2a internal recompute): same concern
- Option D (keep magnitudes with footnote disclaiming reproducibility): preserves a number we cannot defend
- Option E (defer to post-arXiv): leaves the inconsistency in the published draft

## My v11 architectural commitment

Going forward, every number in the paper should be produced by a named idempotent scaffold script that reads primary data only. Verification becomes "does the scaffold run correctly," not "is this individual number right." The pattern already exists for the §4.1 sensitivity blocks (`_v10_battery_sensitivity.py`, `_v10_coupling_sensitivity.py`, `_v10_pipeline_variance.py`); v11 extends it to all §4 numbers via a single `_v11_paper_numbers.py` that emits JSON, with the markdown rendered from the JSON via templating.

## What I want you to evaluate

1. Is Option C the right immediate v10 fix given that primary data does not reproduce the published magnitudes via any tested Delta definition? If not, what should it be?
2. Is the directional claim ("5 of 6 cells reproduce direction") a defensible substitute for the published magnitudes given that sign-matches are invariant across all 8 Delta definitions?
3. Is the v11 scaffold architecture the right structural fix for a paper whose central contribution depends on numerical reproducibility?
4. Is there a methodological move I am missing that would let the paper keep magnitudes while remaining honest? (e.g., committing to delta_C2a internal as the canonical Delta, or running a fresh Tier 2 with the locked aggregation)

Be direct. If my recommendation is wrong, say so. If it is right, name the strongest dissent another reviewer might raise so I can prepare for it.

Under 800 words.
```

---

## Reviewer model response

Yes — **Option C is the right immediate v10 fix**, with one modification: do not bury the discrepancy only in a footnote. Put a short explicit note in the §4.6.1 text or table caption saying the previously reported magnitudes are not reproducible from primary judgment files under the documented aggregation rules, so v10 reports only the robust directional result pending v11 scaffolded regeneration.

### 1. Immediate v10 fix

Given your facts, the six published Δ magnitudes should not remain in the paper. If no tested Δ definition reproduces them, and the mean absolute error is ~0.6–0.75, those numbers are not defensible as empirical results.

Option A or B would be acceptable only if the paper can justify the chosen estimand independently of the discrepancy. For example: “Tier 2 replication is defined as T2 C2a − T2 C5 under the five-judge primary aggregation rule, because that was the preregistered/internal design contrast.” But if that definition is being selected now because it is one of several plausible reconstructions, then replacing the old numbers with it risks looking like retrofitting.

So the best v10 move is:

- remove the unreproducible magnitudes;
- retain the sign/direction claim only;
- explicitly disclose that magnitude reconstruction failed;
- point to the recompute scaffold;
- state that v11 will regenerate all paper numbers from primary data under a locked estimand.

I would call this **Option C+**: direction-only, but with visible disclosure rather than a quiet footnote.

### 2. Is the directional claim defensible?

Yes, but only as a **qualitative robustness statement**, not as a quantitative replication result.

The fact that the sign pattern is invariant across all eight tested definitions is meaningful. It means the core qualitative result — “most cross-provider cells point in the same direction” — is not an artifact of a single Δ reconstruction.

However, be careful with wording. I would avoid language like:

> “The effect replicates across providers.”

That sounds stronger than the evidence supports, especially because the magnitudes are unstable and some recomputed effects shrink substantially.

Better:

> “Across tested reconstruction definitions, five of six subject × response-model cells preserve the expected specification-effect direction, although the magnitudes reported in the previous table are not reproducible from the primary files and are therefore omitted.”

Also, with only six cells, “5 of 6” is not strong inferential evidence by itself. A sign test is weak here: under a 0.5 null, 5/6 is suggestive but not compelling. The defensibility comes from **robustness across plausible definitions**, not from the count alone.

### 3. Is the v11 scaffold architecture right?

Yes. For this kind of paper, it is not just right; it is necessary.

The v11 principle should be:

> No number appears in the manuscript unless it is emitted by a versioned, idempotent script from primary data or explicitly marked as hand-derived/provisional.

A single `_v11_paper_numbers.py` emitting JSON for templated markdown is the right pattern. I would add the following safeguards:

- frozen input manifests with checksums;
- explicit named estimands for every table/figure;
- schema validation for judgment files;
- CI test that reruns the scaffold and detects manuscript/JSON drift;
- versioned output artifacts committed or archived;
- no manual transcription of numeric values;
- a provenance field for each number: input files, filters, aggregation rule, contrast definition, date, script version.

The architectural goal should be not merely “the numbers can be recomputed,” but “there is no alternate undocumented path by which paper numbers can enter the manuscript.”

### 4. Is there a way to keep magnitudes honestly?

Yes, but not the currently published magnitudes unless you recover their exact provenance.

The honest options are:

1. **Recover the original generating script or logs.**  
   If you can show exactly how the published Δs were produced, you may keep them, but then you must document that estimand. If the procedure is ad hoc or inconsistent with the declared aggregation rule, that becomes a methods issue.

2. **Declare one canonical estimand now and regenerate.**  
   For example, “Tier 2 Δ is T2 C2a − T2 C5 under the five-judge primary aggregation rule.” Then replace the table with those magnitudes. This is acceptable only if the choice is methodologically justified, not chosen because it is convenient.

3. **Report a sensitivity range instead of a single Δ.**  
   Example: “Across eight plausible Δ definitions, five of six cells preserve direction; magnitudes range from X to Y.” This is honest and informative, but more complex.

4. **Run a fresh locked Tier 2.**  
   This is the cleanest way to preserve magnitude claims if §4.6.1 matters substantively. Lock the response models, battery source, judges, aggregation, contrast, and analysis script before running. Then report scaffolded results.

What you should not do is keep the old magnitudes with a disclaimer. That preserves numbers the authors cannot currently defend.

### Strongest dissent you should prepare for

A skeptical reviewer will say:

> “The authors are demoting effect sizes to signs after discovering the effect sizes do not reproduce. That is post hoc outcome weakening.”

That criticism is legitimate. Your defense should be:

- the old magnitudes were removed precisely because they were not defensible;
- the remaining directional claim is explicitly narrower;
- the direction result is invariant across all tested reconstruction definitions;
- v11 will regenerate the full quantitative table from a locked scaffold;
- no unreproducible numbers are being preserved.

So: **your recommendation is methodologically sound**, provided the paper is transparent that this is a demotion of the claim, not merely a formatting change.
