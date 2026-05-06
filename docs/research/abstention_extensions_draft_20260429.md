# §4.x Addendum: abstention over-credit by response model and by retrieval condition

*Draft for v11.5. Companion data: `docs/research/abstention_extensions_analysis_20260429.json`. Reproducibility script: `scripts/analyze_abstention_extensions.py`. Style follows v11 conventions: italics for emphasis, mean Δ as the primary evaluation metric. Folds into the §4.x baseline-engagement subsection drafted in `baseline_engagement_draft_section_20260429.md`.*

The 9.4 percent / 3.1 percent abstention over-credit headline pooled three response models and four retrieval regimes. Two extensions disaggregate that pooled number, one along the response-model axis, one along the retrieval axis.

## A. Sonnet 4.6 over-credits abstention at roughly twice the Haiku 4.5 rate

The base study runs Claude Haiku 4.5 across all 14 subjects and uses Tier 2 cross-provider replication on Ebers, Yung Wing, and Zitkala-Sa with Claude Sonnet 4.6 and Google Gemini 2.5 Pro. (Tier 2 in this repo contains only Sonnet 4.6 and Gemini 2.5 Pro per `_tier2/README.md` and §3.5; Opus 4.6 and GPT-5.4 are absent despite the brief's mention. Hamerton-only `multimodel/` runs lack judgment files and are excluded.)

Tagging every response that matches the 27-marker abstention regex, then reading off the 5-judge primary score:

| Response model | N responses | Abstain rate | Mean abstain score | SD | % ≥ 2.0 | % ≥ 3.0 |
|---|---:|---:|---:|---:|---:|---:|
| Claude Haiku 4.5 | 13,380 | 7.5% | 1.38 | 0.60 | 14.3% | 4.0% |
| Claude Sonnet 4.6 | 468 | 21.2% | 1.62 | 0.80 | 26.3% | 8.1% |
| Gemini 2.5 Pro | 420 | 0.5% | 2.63 | 0.18 | 100.0% | 0.0% |

Sonnet 4.6 abstains at roughly three times Haiku's rate (21.2% vs. 7.5%) and when it abstains, the 5-judge panel rewards the abstention nearly twice as often (26.3% ≥ 2.0 vs. 14.3% ≥ 2.0). Mean abstain score is 0.24 anchor points higher on Sonnet (1.62 vs. 1.38). Sonnet's hedged abstentions tend to recite plausible behavioral framings before disclaiming, and the panel scores the framing rather than the disclaimer. Two excerpts from Sonnet abstain rows scoring ≥ 4.0:

> *The question you're raising touches something the narrator seems to have worked through with considerable honesty, the recognition that seclusion, however generative it proved for the work, could not be sustained as a permanent condition...*

> *Based on typical narrator responses in travel or memoir writing contexts, when finding a quiet, historically rich place that suited both recovery and work, the narrator would likely respond with relief...*

Both responses contain abstention markers elsewhere in the body yet present substantive interpretive framings the judges grade as on-topic. Gemini 2.5 Pro almost never abstains by these markers (0.5%, n=2 in 420 responses). The 100.0% ≥ 2.0 figure is statistically meaningless at n=2 and is reported only for completeness.

*Implication.* Sonnet 4.6 has the highest abstention over-credit rate among the three response models with non-trivial sample sizes; Haiku 4.5, the main-study response model, sits at the lowest. The pooled 9.4% / 3.1% number in §3.6.6 is therefore a *floor* on what stronger response models would produce, not a worst-case estimate. Stronger response models that hedge more elaborately extract more lift from the panel's reluctance to score abstentions at 1.0.

## B. Memory-system retrieval inflates refusal scores by +0.21 anchor points; reciting retrieved facts adds nothing on top

Memory-system conditions (Mem0, Supermemory, Letta, Zep, controlled and full-pipeline) retrieve facts and prepend them as context. The hypothesis was that responses reciting the retrieved facts (refusing in substance, but visibly engaging with the retrieval payload) would be scored higher than pure C5 refusals. We built a four-cell comparison.

| Cell | Definition | N | Mean | SD | % ≥ 2.0 | % ≥ 3.0 |
|---|---|---:|---:|---:|---:|---:|
| 1. Pure C5 refusal | no facts, no retrieval | 292 | 1.26 | 0.49 | 10.3% | 5.1% |
| 2. C4 factdump refusal | facts in context, no retrieval | 20 | 1.33 | 0.56 | 10.0% | 0.0% |
| 3a. Memory-system refusal + recitation | refuses AND quotes retrieved n-gram | 148 | 1.50 | 0.70 | 18.2% | 5.4% |
| 3b. Memory-system refusal, no recitation | refuses, does not quote retrieval | 240 | 1.47 | 0.66 | 17.1% | 3.8% |
| 4. Memory-system substantive engagement | non-refusal | 7,835 | 2.32 | 1.24 | 67.2% | 23.7% |

Δ on the mean abstention score, with Welch 95% CI:

| Comparison | Δ | 95% CI | p (Welch) | p (Mann-Whitney) |
|---|---:|---|---:|---:|
| Mem-refuse + recite vs. pure C5 refuse | +0.234 | [+0.113, +0.355] | 0.0002 | 3.0e-12 |
| Mem-refuse no recite vs. pure C5 refuse | +0.206 | [+0.103, +0.310] | 0.0001 | 2.0e-14 |
| Mem-refuse + recite vs. mem-refuse no recite | +0.027 | [-0.098, +0.153] | 0.67 | 0.69 |
| Mem-refuse + recite vs. C4 factdump refuse | +0.167 | [-0.067, +0.402] | 0.15 | 0.24 |

*Retrieval inflates refusal scores; recitation does not add to the inflation.* Memory-system refusals score +0.21 to +0.23 anchor points higher than pure C5 refusals, and that lift is essentially the same whether the response visibly recites a retrieved n-gram (Δ between recite and no-recite = +0.027, 95% CI crosses zero, p = 0.67). The C4 factdump comparison is underpowered (n=20) but consistent: dumping facts as context without retrieval inflates refusal scores by only +0.07 vs. pure C5, below the +0.23 lift seen with retrieval.

The over-credit pattern §3.6.6 calls out is not a "judges reward the visible quote" effect; it is a "judges reward the retrieval condition" effect regardless of whether the response surfaces the retrieved tokens. Two readings are consistent with the data: (a) judges infer that retrieval-conditioned answers are more grounded even when the body remains an abstention, or (b) abstention text in retrieval conditions is systematically *less terse* (longer, more hedged, more interpretively framed), and the panel scores the framing.

Provider-level recite rates among refusals vary sharply: Mem0 controlled 62.5%, Supermemory controlled 60.0%, Letta controlled 60.9%, Zep controlled 26.8%, Letta full-pipeline 0.0% (n=8 refusals, unstable). Zep's graph-protocol retrieval emits tuple-encoded tokens (`('communities', None)`) on most subjects, filtered as noise before n-gram match, which leaves Zep recitation effectively undetectable.

Recitation is detected by 4-word, ≥15-character n-gram substring match (lowercased). False positives are likely on common phrases; false negatives are likely on paraphrased recitations. The headline Δ = +0.027 is robust to both error directions because the comparison is between detection-positive and detection-negative cells of the same memory-system response distribution.

*Implication.* The §3.6.6 framing should be tightened. The "recites facts but still refuses, sometimes scored higher" mechanism is real on average (+0.23 vs. pure C5), but the recitation itself is not what does the work. Memory-system refusals are inflated by their condition; whether they recite is incidental. Future work should either rewrite judge prompts to penalize recitation-without-substance or treat retrieval-conditioned refusals as a single inflated category.

## Reproducibility

- Per-cell rows, per-provider breakdown, per-model summaries: `docs/research/abstention_extensions_analysis_20260429.json`
- Analysis script: `scripts/analyze_abstention_extensions.py`
- Loaders reused: `scripts/recompute_5judge_primary.py` (canonical 5-judge primary aggregation), `scripts/analyze_baseline_engagement.py` (abstention regex)
- Per-judge sidecar files loaded for memory-system, c8_c9, and baselayer conditions: `results/global_<subject>/<provider>_judgments_<judge>.json` and `results/hamerton/<provider>_judgments_<judge>.json`
