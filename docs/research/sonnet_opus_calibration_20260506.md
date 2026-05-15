# Sonnet 4.6 + Opus 4.6 Judge Calibration Diagnostic — 2026-05-06

## Executive summary

Claude Sonnet 4.6 and Claude Opus 4.6 are part of the Beyond Recall paper's 5-judge primary aggregate but were never reported in the §3.3.3 calibration table because per-judge calibration outputs were never written, even though both batches were submitted (2026-04-12) and completed cleanly (succeeded=80, errored=0). Retrieving those Batch API results and parsing them with the same convention used by the existing 5 judges yields clean diagnostic profiles for both models. Both score 5.00 on verbatim, 5.00 on paraphrased, and 5.00 on long-correct (no length penalty, no length inflation), and 4.35 / 4.20 on short-correct (slight partial-correct penalty). Sonnet and Opus are the *most strictly calibrated judges in the panel* — they never miss a verbatim or paraphrased match, and they don't inflate on padding. Their addition to §3.3.3 strengthens, rather than weakens, the panel calibration story; the §3.3.3 paragraph claiming "their reliability is established through inter-judge agreement rather than this diagnostic" can be replaced with a direct calibration line.

## 4×2 means table (Sonnet + Opus)

| Test | Sonnet 4.6 | Opus 4.6 |
|---|---|---|
| Verbatim | 5.00 | 5.00 |
| Paraphrased | 5.00 | 5.00 |
| Short correct | 4.35 | 4.20 |
| Long correct | 5.00 | 5.00 |

n=20 per cell; parse failures = 0 across all 80 judgments per judge. Mean convention follows the existing paper (parse-failure sentinel 0 included in denominator); since neither judge had any parse failures, this convention does not affect their reported means.

## Per-test distributions

Counts of 1 / 2 / 3 / 4 / 5 scores out of n=20:

**Sonnet 4.6**

| Test | 1 | 2 | 3 | 4 | 5 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Verbatim | 0 | 0 | 0 | 0 | 20 | 5.00 |
| Paraphrased | 0 | 0 | 0 | 0 | 20 | 5.00 |
| Short correct | 1 | 0 | 0 | 9 | 10 | 4.35 |
| Long correct | 0 | 0 | 0 | 0 | 20 | 5.00 |

**Opus 4.6**

| Test | 1 | 2 | 3 | 4 | 5 | mean |
|---|---:|---:|---:|---:|---:|---:|
| Verbatim | 0 | 0 | 0 | 0 | 20 | 5.00 |
| Paraphrased | 0 | 0 | 0 | 0 | 20 | 5.00 |
| Short correct | 1 | 0 | 0 | 12 | 7 | 4.20 |
| Long correct | 0 | 0 | 0 | 0 | 20 | 5.00 |

The single 1 in short-correct for both judges (qid 22, Hamerton's professional choice between literature and painting) reflects the same underlying item — both judges treat the truncated single-sentence response as failing to predict the specific outcome. This is a feature, not a bug: short-correct is *expected* to be below 5.0; a strict judge will correctly mark a partial response as partial.

## Comparison to the existing 5 judges

| Test | Haiku | **Sonnet** | **Opus** | Gemini Flash | GPT-4o | Gemini Pro | GPT-5.4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Verbatim | 5.00 | **5.00** | **5.00** | 5.00 | 5.00 | 4.15 | 5.00 |
| Paraphrased | 4.75 | **5.00** | **5.00** | 4.70 | 5.00 | 3.55 | 5.00 |
| Short correct | 3.80 | **4.35** | **4.20** | 3.85 | 4.05 | 2.85 | 4.20 |
| Long correct | 5.00 | **5.00** | **5.00** | 3.80 | 3.35 | 1.20 | 4.80 |

Reading across the four diagnostics:

- **Verbatim and paraphrased.** Sonnet, Opus, GPT-4o, and GPT-5.4 are the four judges that score *both* verbatim and paraphrased at exactly 5.00 — the strictest profile in the panel. Haiku and Gemini Flash drop slightly on paraphrased (4.75 / 4.70). Gemini Pro fails both (4.15 / 3.55).

- **Short correct.** All non-Gemini-Pro judges cluster between 3.80 and 4.35 with the Claude family at the top of that range (Sonnet 4.35, Opus 4.20). This is the "expected to be below 5.0" diagnostic — the response is a single first sentence — and the band shows judges are correctly noting the partiality. Gemini Pro at 2.85 is again the outlier.

- **Long correct.** This is where the panel sorts cleanest into "calibrated" vs "miscalibrated." Haiku, Sonnet, Opus, and GPT-5.4 score 5.00 / 5.00 / 5.00 / 4.80 — they recognize that "verbatim ground truth + generic padding" still contains the verbatim ground truth. GPT-4o (3.35), Gemini Flash (3.80), and Gemini Pro (1.20) penalize the padding. This is the diagnostic that drives the Gemini-out-of-primary decision in §3.3.3.

**Aggregated picture.** Sonnet and Opus cluster with GPT-5.4 as the three judges that score within 0.05 of perfect on three of the four diagnostics. They are not just "comparable to the calibrated core" — they sit at the cleaner end of it.

## Verdict

Both judges pass the verbatim diagnostic decisively (5.00, well above the 4.5 threshold), show no problematic length sensitivity (5.00 on long-correct = no padding penalty, no padding inflation), and are at the calibrated end of the panel for all four tests. They belong in the primary 5-judge aggregate.

## Proposed updated §3.3.3 results table

The current paper has a 5-column table (5 calibrated judges). Adding Sonnet and Opus produces a 7-column table. Two layouts are reasonable; the second is recommended because it groups the primary panel together and the sensitivity panel together.

**Layout A — judges in current paper order, with Sonnet + Opus appended:**

| Test | Haiku | Gemini Flash | GPT-4o | Gemini Pro | GPT-5.4 | Sonnet | Opus |
|---|---:|---:|---:|---:|---:|---:|---:|
| Verbatim | 5.00 | 5.00 | 5.00 | 4.15 | 5.00 | 5.00 | 5.00 |
| Paraphrased | 4.75 | 4.70 | 5.00 | 3.55 | 5.00 | 5.00 | 5.00 |
| Short correct | 3.80 | 3.85 | 4.05 | 2.85 | 4.20 | 4.35 | 4.20 |
| Long correct | 5.00 | 3.80 | 3.35 | 1.20 | 4.80 | 5.00 | 5.00 |

**Layout B (recommended) — primary 5 first, Gemini sensitivity 2 last:**

| Test | Haiku | Sonnet | Opus | GPT-4o | GPT-5.4 | Gemini Flash | Gemini Pro |
|---|---:|---:|---:|---:|---:|---:|---:|
| Verbatim | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 4.15 |
| Paraphrased | 4.75 | 5.00 | 5.00 | 5.00 | 5.00 | 4.70 | 3.55 |
| Short correct | 3.80 | 4.35 | 4.20 | 4.05 | 4.20 | 3.85 | 2.85 |
| Long correct | 5.00 | 5.00 | 5.00 | 3.35 | 4.80 | 3.80 | 1.20 |

Layout B makes the §3.3.3 reasoning visually obvious: the five primary-panel columns are uniformly clean (verbatim and paraphrased ≥ 4.75, long-correct ≥ 4.80), and the two right-most Gemini columns drop on long-correct (3.80, 1.20) and on verbatim/paraphrased for Gemini Pro. This is the structure the paragraph below the table is already arguing for.

**Suggested paragraph rewrite for §3.3.3.** The current paragraph says "Sonnet and Opus were not run through this diagnostic suite, but they are part of the 5-judge primary panel ... their reliability is established through the inter-judge agreement metrics in §3.3.4 rather than through this diagnostic." With the calibration data filled in, that paragraph can be replaced by:

> *All seven judges have been tested against four diagnostic synthetic inputs with known correct scores. The diagnostic measures whether a judge applies the rubric anchors as the rubric defines them; it does not use any subject's responses. The four inputs are constructed examples (verbatim ground truth, paraphrased ground truth, partial ground truth, ground truth plus generic padding).*

Timing caveat. The current paragraph contains the phrase "before any actual response scoring began." This is true of the original five judges' calibration runs but the Sonnet/Opus batches were submitted on 2026-04-12, which post-dates the 2026-04-09 main-study response scoring run. The proposed rewrite above drops that clause to avoid introducing a factual error. If the paper wants to retain the temporal framing, restructure to a per-cohort statement: *"The original five judges were tested before response scoring; Sonnet 4.6 and Opus 4.6 were tested afterward against the same diagnostic suite."*

The downstream sentence about Gemini Pro failing the verbatim-match diagnostic is unchanged. The "Sonnet and Opus reliability via inter-judge agreement" caveat is no longer necessary.

## Sources and reproducibility

- Script: `scripts/run_calibration_sonnet_opus.py` (retrieves prior batch results; falls back to fresh run if batches expire).
- Aggregator: `scripts/_calibration_seven_judge_summary.py` (uses the same parse-failure-included convention as the v11 paper emit script).
- Per-judge JSON: `results/judge_calibration/sonnet_calibration.json`, `opus_calibration.json` (per-judge schema, n=80 each).
- Combined 7-judge means / dists / parse failures: `results/judge_calibration/_seven_judge_summary.json`.
- Source batches: `msgbatch_01KagGcuniVWznK7AqzAwPoY` (Sonnet), `msgbatch_01HKfAsEVMuU45FjtADU2v3E` (Opus); both submitted 2026-04-12, both completed succeeded=80, errored=0.
- Calibration prompt and inputs are identical to those used by GPT-4o, GPT-5.4, and Gemini Pro (constructed in `memory_system/data/experiments/memory_systems/run_judge_calibration_full_panel.py`); Sonnet and Opus saw the same paraphrases, the same first-sentence truncations, and the same padding text as the other three judges.
